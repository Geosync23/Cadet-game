# Starship Cadet: machine check (keep in the repo, next to day_check.py)
# Runs the ship's machines (section 17) on paper for DAYS ship days with ?nosave and checks, deterministically:
#   every machine in DECKS[n].machines is of a kind section 17 knows
#   with no repairs: conditions only ever fall; nothing is faulty in the first two days; some machines are broken
#   by the end, but the slow ones (reactor, hull, array) are not; ship health falls but stays above 0; every
#   machine's effects stay in range (multipliers, mood)
#   the same ship wears the same way: run twice; one big jump against hour by hour against odd minutes;
#   with the schedule caches cleared
#   with an ideal crew (the day shift services anything worn, a few machines an hour): nothing ever gets past
#   worn, and ship health stays at 90 or more
#   with the real Works crew claiming jobs on paper (B2, B3): nothing breaks, ship health stays at 85 or more,
#   shelves never go below zero, deliveries get carried to storage, easy jobs wait for you first (CREW_LEAVE minutes
#   of the day shift; it reports how many a day are left for the player, aiming at 3 to 6), nobody does two
#   jobs at once or a job outside their work block, jobWhere agrees with the jobs, and it's the same every way
#   the looks (0.33.17): machineLook, deckLook and the Ship health board's rows in range; shipMoodAt and chillerAt
#   pure and in step with shipEffectsAt
#   tapping a machine, Stores' Mail and tier locks (0.33.18): see 5d below
#   chores and openJobs (0.33.19): see 5e below
#   turning jobs in at the board (0.33.23): jobStepDone, the work-done state, turnInJob (5g)
#   event hooks and favours (Pillar 3, C7, 0.33.24): eventMod wear, event jobs, favours (5h)
#   food runs in live play (0.33.21): the crew take every food run soon after its wait (5f)
#   the board through a week (0.33.32): jobs for you on every weekday shift, none held on your days off (5i)
#   the garden (0.33.34): grow lights, gardenAt, the crate run and carryWaiting (5j)
#   reserved jobs and job notes (Pillar 4): jobReserve, jobRelease, simNote('job', 'repair', 'jobAbandoned', 'jobUnclaimed') (5k)
#   the Works crew at work (0.33.40): the two placed jobs on Days 1 and 2, every third small job to the crew at once (5l)
#   the shelves and the Wednesday delivery (0.33.41-0.33.42): the right shelf, the machine shop, crates, two trips, 14:00 (5m)
#   your side: a job you claim is left to you, and finishing it puts the machine right
#   the save: machines, jobs and supplies written by the save hook and read back by machinesLoad come out the
#   same, and run on the same afterwards
#   play (the player's needs read shipEffects every ship minute) never runs the machines ahead of the clock, and
#   reading shipEffects is cheap; shipEffectsAt gives back what shipEffects said over the last 7 days, and reading
#   it changes nothing
# Setup and environment as for cadet_test.py.
# Run:  python3 machine_check.py BUILD.html [DAYS]     (DAYS defaults to 14)
import sys, json, time
exec(open(__file__.replace('machine_check.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright

DAYS = int(sys.argv[2]) if len(sys.argv) > 2 else 14
SLOW = ('reactor', 'hullseal', 'array', 'doorgear')     # kinds that must not break in DAYS days unrepaired
CREW_PER_HOUR = 3                                       # jobs the ideal day shift finishes each hour, 08:00-17:00

# run the machines from a fresh ship at Day 1 06:00 for `days` days. mode: 'hour' (ask every ship hour),
# 'jump' (ask once at the end), 'odd' (ask at odd minutes); crew: service worn machines on the day shift
RUN = r"""(({ days, mode, crew, perHour, events }) => {
  // ordinary wear: ship-wide events (the ion storm, due day 10 of a new game) off unless asked for; put back at the end
  if (!events) window.__sc("window.__evRun = [typeof eventNow === 'function' ? eventNow : undefined, typeof eventMod === 'function' ? eventMod : undefined]; if (window.__evRun[0]) eventNow = () => null; if (window.__evRun[1]) eventMod = () => null");
  const t0 = (SHIP_START.day - 1) * 1440 + SHIP_START.min, end = t0 + days * 1440;
  JOBS_ON = crew === 'real'; MACH_HOUR = null; MACH_SEEN = -1; setShipNow(t0); machinesNow();
  const out = { daily: [], first: {}, rising: [], worst: {}, minHealth: 100, fx: [], jobs: 0, maxOpen: 0, minStock: 99, waiting: 0 };
  const seen = new Map();
  const list = machineList(), prev = {};
  for (const m of list) prev[m.id] = SHIP.machines[m.id].cond;
  const look = t => {
    const st = SHIP.machines;
    for (const m of list) {
      const s = st[m.id];
      if (!crew && s.cond > prev[m.id] + 1e-9) out.rising.push(m.id + ' ' + hhmm(t % 1440));
      prev[m.id] = s.cond;
      const k = MACHINE_STATES.indexOf(s.state);
      if (!(m.id in out.worst) || k > out.worst[m.id]) out.worst[m.id] = k;
      if (!out.first[m.id]) out.first[m.id] = {};
      if (!(s.state in out.first[m.id])) out.first[m.id][s.state] = Math.round((t - t0) / 144) / 10;
    }
    out.minHealth = Math.min(out.minHealth, shipHealth());
    for (const j of SHIP.jobs) seen.set(j.id, j);
    const cur = SHIP.jobs.find(j => j.segs && j.status === 'claimed' && j.claimedBy !== 'you');
    if (cur) {
      const sg = cur.segs.find(x => x.act === 'work' && x.tag !== 'fetch' && x.tag !== 'make') || cur.segs[0], w = jobWhere(schedPeople().find(p => p.id === cur.claimedBy), sg.from);
      out.overlay = (out.overlay !== false) && !!w && w.deck === sg.deck && w.job === cur.id;
    }
    out.maxOpen = Math.max(out.maxOpen, SHIP.jobs.filter(j => j.status !== 'done' && j.found <= t).length);
    out.waiting += SHIP.jobs.filter(j => j.status === 'waiting').length;
    for (const k in SHIP.stores) out.minStock = Math.min(out.minStock, SHIP.stores[k]);
  };
  if (mode === 'jump') { setShipNow(end); machinesNow(); look(end); }
  else for (let t = t0; t <= end; t += mode === 'odd' ? 37 : 60) {
    setShipNow(t); machinesNow(); look(t);
    const min = t % 1440;
    if (crew === 'ideal' && min >= 480 && min < 1020) {
      const due = list.filter(m => SHIP.machines[m.id].state !== 'healthy').sort((a, b) => SHIP.machines[a.id].cond - SHIP.machines[b.id].cond);
      for (const m of due.slice(0, perHour)) { serviceMachine(m.id); out.jobs++; }
    }
    if ((t - t0) % 1440 === 1080) {                      // every day at midnight: a snapshot
      const sys = shipSystems();
      out.daily.push({ day: SHIP.time.day, health: shipHealth(sys), sys, cond: Object.fromEntries(list.map(m => [m.id, Math.round(SHIP.machines[m.id].cond * 10) / 10])) });
      for (const n of Object.keys(DECKS)) { const f = shipEffects(+n); out.fx.push({ deck: +n, t, restore: f.restore, drain: f.drain, walk: f.walk, cook: f.cook, lift: f.lift, spoil: f.spoil, mood: f.mood, notes: f.notes.length, json: JSON.stringify(f) }); }
    }
  }
  setShipNow(end); machinesNow(); look(end);
  out.final = Object.fromEntries(list.map(m => [m.id, SHIP.machines[m.id].cond]));
  out.states = Object.fromEntries(list.map(m => [m.id, SHIP.machines[m.id].state]));
  out.kinds = Object.fromEntries(list.map(m => [m.id, m.kind]));
  out.effects4 = shipEffects(4); out.effects3 = shipEffects(3);
  // shipEffectsAt: the record gives back what shipEffects said at the time (the last 8 days), and reading it
  // changes nothing
  const rev = MACH_REV, hour = MACH_HOUR;
  out.atBad = out.fx.filter(f => f.t >= end - 7 * 1440 && JSON.stringify(shipEffectsAt(f.deck, f.t)) !== f.json).map(f => f.deck + '@' + f.t);
  out.atPure = MACH_REV === rev && MACH_HOUR === hour;
  // the jobs, for the real crew's checks
  const J = [...seen.values()], ppl = new Map(schedPeople().map(p => [p.id, p]));
  out.jobList = J.map(j => ({ id: j.id, kind: j.kind, status: j.status, by: j.claimedBy, urgency: j.urgency, posted: j.posted, found: j.found, start: j.start, end: j.end, done: j.done, made: j.made || 0, tier: jobTier(j), cargo: j.cargo || null, leave: leaveEnd(j) }));
  // jobs left for the player: at your tier, on the board unclaimed for an hour or more of the day shift
  const dayMin = (a, b) => { let n = 0; for (let m = Math.ceil(a); m < b; m++) { const md = m % 1440; if (md >= DAY_SHIFT[0] && md < DAY_SHIFT[1]) n++; } return n; };
  out.leftForYou = J.filter(j => j.found <= end && jobTier(j) <= PLAYER_TIER && !(j.machine && ENGINE_KINDS.has(machineById(j.machine).kind))
    && dayMin(j.found, Math.min(end, j.start ?? j.doneAt ?? end)) >= 60).length;
  // nobody on two jobs at once; every job inside its person's work block (whereIs says work all through)
  const byWho = {}; out.overlap = []; out.offShift = [];
  for (const j of J) if (j.segs && j.claimedBy !== 'you') {
    (byWho[j.claimedBy] = byWho[j.claimedBy] || []).push([j.start, j.end, j.id, j.done, j.status]);
    const p = ppl.get(j.claimedBy);
    for (let m = j.start; m < j.end; m += 5) { const w = planWhere(p, m); if (w.act !== 'work') { out.offShift.push(j.id + ' ' + p.id + ' ' + w.act); break; } }
  }
  for (const who in byWho) { const v = byWho[who].sort((a, b) => a[0] - b[0]); for (let i = 1; i < v.length; i++) if (v[i][0] < v[i - 1][1]) out.overlap.push(who + " " + JSON.stringify([v[i - 1], v[i]])); }
  // the overlay: someone mid-job is where the job says
  out.endJobs = JSON.stringify([SHIP.jobs, SHIP.stores, SHIP.hold]);
  JOBS_ON = true;
  if (!events) window.__sc("if (window.__evRun[0]) eventNow = window.__evRun[0]; if (window.__evRun[1]) eventMod = window.__evRun[1]");
  return out;
})"""

ok = True
def fail(msg):
    global ok
    ok = False
    print('  FAIL', msg)

with sync_playwright() as pw:
    g = Game(pw, sys.argv[1])
    g.ev("player.steer = null; player.stop()")
    g.ev("if (typeof TURN_IN !== 'undefined') TURN_IN = false")   # TURN_IN on in the build from 0.37.3; these checks assume it off, 5g turns it on itself
    # 0. nothing runs unless asked: a while of play with ?nosave leaves the machines untouched
    g.step(60)
    # since 0.40.2 the player's needs read shipEffects every ship minute, so play runs the machines; they must
    # never run ahead of the clock, and a read in the same hour must be cheap
    st = g.ev("""(() => {
      const nowH = Math.floor(shipNow() / 60), ran = MACH_HOUR !== null;
      return { ran, upToDate: !ran || MACH_HOUR === nowH + 1, nowH, hour: MACH_HOUR };
    })()""")
    import time as _t
    t = _t.time(); g.ev("(() => { for (let k = 0; k < 2000; k++) shipEffects(4); return 1; })()"); same_hour_us = (_t.time() - t) / 2000 * 1e6
    t = _t.time(); g.ev("(() => { setShipNow(shipNow() + 60); shipEffects(4); return 1; })()"); new_hour_ms = (_t.time() - t) * 1000
    print(f"Play ran the machines: {st['ran']}, never ahead of the clock: {st['upToDate']}; shipEffects in the same hour about {same_hour_us:.0f} us, at a new hour {new_hour_ms:.0f} ms")
    if not st['upToDate']: fail(f"machines ran ahead of the clock: hour {st['hour']} at {st['nowH']}")
    pure = g.ev("(() => { const r = MACH_REV, h = MACH_HOUR; for (let d = 1; d <= 6; d++) shipEffectsAt(d, shipNow() - 500); return MACH_REV === r && MACH_HOUR === h; })()")
    if not pure: fail('shipEffectsAt changed the machines')
    g.ev("window.__realTick = tickShip; tickShip = () => {}")
    unknown = g.ev("Object.keys(DECKS).flatMap(n => (DECKS[n].machines || []).filter(m => !MACHINE_KINDS[m.kind]).map(m => m.id + ' (' + m.kind + ')'))")
    if unknown: fail(f"machines of kinds section 17 doesn't know (they'd be left out): {unknown}")
    noPanel = g.ev("machineList().filter(m => !m.stub && !panelPlace(m.id)).map(m => m.id)")
    if noPanel: print('  real machines with no panel place yet:', noPanel)
    n = g.ev("machineList().length")
    stubs = g.ev("machineList().filter(m => m.stub).length")
    print(f"{n} machines ({n - stubs} from the decks, {stubs} stand-ins), {DAYS} days")

    run = lambda **o: g.page.evaluate("([s, o]) => window.__sc(s)(o)", [RUN, {'days': DAYS, 'mode': 'hour', 'crew': False, 'perHour': CREW_PER_HOUR, 'events': False, **o}])

    # 1. no repairs
    t = time.time(); a = run()
    print(f"No repairs ({time.time() - t:.1f} s):")
    print('  ship health by day:', ' '.join(f"{d['health']:.0f}" for d in a['daily']))
    last = a['daily'][-1]['sys']
    print('  systems at the end:', ', '.join(f"{k} {v:.0f}" for k, v in last.items()))
    kinds = {}
    for mid, k in a['kinds'].items(): kinds.setdefault(k, []).append(mid)
    print('  by kind: first day faulty / failing / broken (median), and the end')
    for k, ids in kinds.items():
        def med(st):
            v = sorted(a['first'][i].get(st, 99) for i in ids); x = v[len(v) // 2]
            return '-' if x == 99 else f"{x:.1f}"
        print(f"    {k:14} {med('faulty'):>5} {med('failing'):>5} {med('broken'):>5}   end {min(a['final'][i] for i in ids):5.1f} {a['states'][ids[0]]}")
    if a['rising']: fail(f"condition rose with no repairs: {a['rising'][:5]}")
    early = [i for i in a['first'] if any(v < 2 for s, v in a['first'][i].items() if s in ('faulty', 'failing', 'broken'))]
    if early: fail(f"faulty within two days: {early}")
    broken = [i for i, s in a['states'].items() if s == 'broken']
    print(f"  at the end: {len(broken)} broken, " + ', '.join(f"{s} {sum(1 for x in a['states'].values() if x == s)}" for s in ('healthy', 'worn', 'faulty', 'failing')))
    if DAYS >= 14 and not broken: fail('nothing broke in two weeks with no repairs')
    slow = [i for i in a['states'] if a['kinds'][i] in SLOW and a['states'][i] in ('failing', 'broken')]
    if slow: fail(f"slow machines failing: {slow}")
    hs = [d['health'] for d in a['daily']]
    if not (hs[-1] < hs[0] and hs[-1] > 0): fail(f"ship health {hs[0]} -> {hs[-1]}")
    bad = [f for f in a['fx'] if not (all(0 < v <= 1 for v in f['restore'].values()) and all(1 <= v < 3 for v in f['drain'].values())
           and .5 < f['walk'] <= 1 and 1 <= f['cook'] < 3 and 1 <= f['lift'] < 3 and 1 <= f['spoil'] < 3 and -30 <= f['mood'] <= 0)]
    if bad: fail(f"effects out of range: {bad[:2]}")
    e4 = a['effects4']
    print(f"  Deck 4 at the end: hygiene restore x{e4['restore']['hygiene']:.2f}, energy drain x{e4['drain']['energy']:.2f}, energy restore x{e4['restore']['energy']:.2f}, walk x{e4['walk']:.2f}, mood {e4['mood']}")
    for nt in e4['notes'][:12]: print(f"    {nt['stage']:10} {nt['text']} ({nt['machine']}, {nt['state']})")
    e3 = a['effects3']
    print(f"  Deck 3 at the end: cook x{e3['cook']:.2f}, hunger restore x{e3['restore']['hunger']:.2f}, lift x{e3['lift']:.2f}, mood {e3['mood']}")

    print(f"  shipEffectsAt matches the last 7 days: {not a['atBad']}, reads change nothing: {a['atPure']}")
    if a['atBad'] or not a['atPure']: fail(f"shipEffectsAt: {a['atBad'][:4]} pure {a['atPure']}")
    # 2. the same every way
    b = run()
    j = run(mode='jump')
    o = run(mode='odd')
    c = g.ev("(() => { SHIP_DAYS.clear(); MACH_USE.clear(); MACH_NORM = null; MACH_NORM_PART = null; return 1; })()") and run()
    same = lambda x, y: all(abs(x['final'][i] - y['final'][i]) < 1e-9 for i in x['final'])
    print('The same twice:', same(a, b), '| one jump:', same(a, j), '| odd minutes:', same(a, o), '| caches cleared:', same(a, c))
    for name, x in (('twice', b), ('jump', j), ('odd minutes', o), ('caches cleared', c)):
        if not same(a, x): fail(f"wear differs ({name})")

    # 3. an ideal crew
    i = run(crew='ideal')
    worst = max(i['worst'].values())
    print(f"Ideal crew ({CREW_PER_HOUR} jobs an hour on the day shift): {i['jobs']} jobs, worst state {['healthy', 'worn', 'faulty', 'failing', 'broken'][worst]}, lowest ship health {i['minHealth']:.1f}")
    print('  ship health by day:', ' '.join(f"{d['health']:.0f}" for d in i['daily']))
    if worst > 1: fail('a machine got past worn with an ideal crew')
    if i['minHealth'] < 90: fail(f"ship health fell to {i['minHealth']} with an ideal crew")

    # 4. the real Works crew, claiming jobs on paper
    r = run(crew='real')
    worst = max(r['worst'].values())
    J = r['jobList']; done = [j for j in J if j['status'] == 'done' and j['by'] not in (None, 'you')]
    kinds = {}
    for j in done: kinds[j['kind']] = kinds.get(j['kind'], 0) + 1
    waits = sorted((j['start'] - j['found']) / 60 for j in done if j['kind'] in ('repair', 'overhaul'))
    print(f"Real Works crew: {len(done)} jobs done ({', '.join(f'{k} {v}' for k, v in sorted(kinds.items()))}), {sum(j['made'] for j in done)} parts made in the machine shop")
    print(f"  worst state {['healthy', 'worn', 'faulty', 'failing', 'broken'][worst]}, lowest ship health {r['minHealth']:.1f}, at most {r['maxOpen']} jobs on the board, lowest shelf {r['minStock']}, job-hours waiting for parts {r['waiting']}")
    if waits: print(f"  repairs claimed after {waits[len(waits) // 2]:.1f} h (median), {waits[-1]:.1f} h at worst")
    print('  ship health by day:', ' '.join(f"{d['health']:.0f}" for d in r['daily']))
    early = [j['id'] for j in done if j['start'] < j['leave']]
    print(f"  jobs left for the player (your tier, on the board an hour or more of the day shift): {r['leftForYou']}, {r['leftForYou'] / DAYS:.1f} a day")
    restocks = [j for j in done if j['kind'] == 'restock']
    print(f"  restock runs {len(restocks)}, nobody on two jobs at once: {not r['overlap']}, every job inside its work block: {not r['offShift']}, overlay matches: {r.get('overlay')}")
    if worst > 3: fail('a machine broke with the Works crew on the job')
    if r['minHealth'] < 85: fail(f"ship health fell to {r['minHealth']} with the Works crew on the job")
    if r['minStock'] < 0: fail('a shelf went below zero')
    if early: fail(f"crew took easy jobs before leaving them for you: {early[:4]}")
    if r['overlap']: fail(f"two jobs at once: {r['overlap'][:4]}")
    if r['offShift']: fail(f"jobs outside the work block: {r['offShift'][:4]}")
    if DAYS >= 7 and not restocks: fail('no restock after a delivery')
    if r.get('overlay') is not True: fail('jobWhere disagrees with the job')
    r2 = run(crew='real', mode='jump'); r3 = run(crew='real', mode='odd'); r4 = run(crew='real')
    js = lambda x: x['endJobs']
    print('  the same twice:', same(r, r4) and js(r) == js(r4), '| one jump:', same(r, r2) and js(r) == js(r2), '| odd minutes:', same(r, r3) and js(r) == js(r3))
    for name, x in (('twice', r4), ('jump', r2), ('odd minutes', r3)):
        if not (same(r, x) and js(r) == js(x)): fail(f"jobs differ ({name})")

    # 4b. what the machines look like (0.33.17): machineLook and deckLook in range for every machine and deck, a
    # failing machine blinks and a fine one doesn't; the Ship health board's rows; shipMoodAt and chillerAt are pure
    # and agree with shipEffectsAt (a chiller working well spoils nothing, a worse one more)
    lk = g.ev("""(() => {
      JOBS_ON = false; MACH_HOUR = null; MACH_SEEN = -1; const bad = [], t0 = (SHIP_START.day - 1) * 1440 + SHIP_START.min;
      const states = ['fine', 'worn', 'poor', 'failing'];
      for (const day of [1, 5, 10]) {
        setShipNow(t0 + day * 1440); machinesNow();
        for (const m of machineList()) {
          const L = machineLook(m.id), st = SHIP.machines[m.id].state;
          if (!L || !states.includes(L.state) || !(L.dim >= 0 && L.dim <= 1) || !(L.flicker >= 0 && L.flicker <= 1) || typeof L.drip !== 'boolean'
              || L.blink !== (st === 'failing' || st === 'broken') || (st === 'healthy' && (L.state !== 'fine' || L.dim || L.flicker || L.drip))) bad.push(day + ' ' + m.id + ' ' + JSON.stringify(L));
        }
        for (const n of Object.keys(DECKS)) { const D = deckLook(+n); if (!(D.dim >= 0 && D.dim <= 1 && D.flicker >= 0 && D.flicker <= 1 && D.spray > 0 && D.spray <= 1 && D.wilt >= 0 && D.wilt <= 1)) bad.push(day + ' deck ' + n + ' ' + JSON.stringify(D)); }
      }
      const rows = shipHealthRows(), rowsOk = rows.length === SYSTEMS.length + 1 && rows[0].key === 'ship' && rows.every(r => r.value >= 0 && r.value <= 100 && states.includes(r.state));
      const rev = MACH_REV, hour = MACH_HOUR; let moodBad = 0, chill = [], about = null;
      for (let t = shipNow() - 5 * 1440; t <= shipNow(); t += 180) {
        for (const n of Object.keys(DECKS)) { const M = shipMoodAt(+n, t); if (M.mood !== shipEffectsAt(+n, t).mood || M.mood < -30 || M.mood > 0 || (M.mood < 0 && !M.about && M.health >= 70)) moodBad++; if (+n === 4 && M.about) about = M.about; }
        chill.push(chillerAt(t));
      }
      const chillOk = chill.every(c => c.spoil >= 0 && c.spoil <= CHILL_SPOIL && (machWorks(c.cond) >= 85) === (c.spoil === 0));
      const pure = MACH_REV === rev && MACH_HOUR === hour;
      setShipNow(t0); JOBS_ON = true;
      return { bad: bad.slice(0, 4), nBad: bad.length, rowsOk, rows: rows.slice(0, 4).map(r => r.name + ' ' + r.value + ' ' + r.state + (r.worst ? ' (' + r.worst + ')' : '')), moodBad, about, chillOk, chillEnd: chill[chill.length - 1], pure };
    })()""")
    print(f"Looks: {lk['nBad']} out of range, board rows ok {lk['rowsOk']}: {lk['rows']}; crew grumble about {lk['about']}; chiller at day 10 {lk['chillEnd']}; pure {lk['pure']}")
    if lk['nBad'] or not lk['rowsOk']: fail(f"machineLook / deckLook / shipHealthRows: {lk['bad']}")
    if lk['moodBad'] or not lk['chillOk'] or not lk['pure']: fail('shipMoodAt / chillerAt')

    # 4c. the ion storm (section 18, when the build has one due in DAYS days): the runs above are ordinary wear, with
    # events off. With the storm on, comms (and power) wear harder than without it; with the real Works crew the sensor
    # array never gets past faulty, and the storm's comms wear shows on the job list
    storm = g.ev("typeof eventNow === 'function' && typeof SHIP_EVENTS === 'object' && !!SHIP_EVENTS.ionStorm && !SHIP_EVENTS.ionStorm.draft")
    if storm:
        sa = run(events=True)
        comms = [i for i in sa['kinds'] if g.ev(f"MACHINE_KINDS[{json.dumps(sa['kinds'][i])}].sys") == 'comms']
        harder = [i for i in comms if sa['final'][i] < a['final'][i] - 1e-9 or a['final'][i] == 0]
        sr = run(crew='real', events=True)
        arr = [i for i in sr['kinds'] if sr['kinds'][i] == 'array']
        arrWorst = max((sr['worst'][i] for i in arr), default=0)
        arrJobs = [j for j in sr['jobList'] if j['id'].split('@')[0] in arr]
        print(f"Ion storm on: comms machines worn harder than without it {len(harder)}/{len(comms)}; no repairs, the array ends {[sa['states'][i] for i in arr]}; with the Works crew the array's worst {['healthy', 'worn', 'faulty', 'failing', 'broken'][arrWorst]}, its jobs {[(j['kind'], j['status']) for j in arrJobs]}, lowest ship health {sr['minHealth']:.1f}")
        if len(harder) < len(comms) or not comms: fail('the storm should wear comms harder')
        if arrWorst > 2: fail('the sensor array got past faulty in the storm with the Works crew on the job')
    else:
        print('Ion storm: not in this build (or still a draft); skipped')

    # 5. your side: a job you claim is left to you
    y = g.ev("""(() => {
      if (typeof SHARE_ON !== 'undefined') SHARE_ON = false;   // 0.33.40: no job of yours handed to the crew at once here (5l tests that)
      JOBS_ON = true; MACH_HOUR = null; MACH_SEEN = -1; setShipNow(4 * 1440 + 9 * 60); machinesNow();
      const o = SHIP.machines['3-oven-1']; o.cond = 40; o.state = machineState(40);       // the oven acts up
      setShipNow(4 * 1440 + 10 * 60); machinesNow();
      const j = jobsBoard().find(x => x.machine === '3-oven-1' && !x.claimedBy);
      if (!j) return { none: true };
      const id = j.id, before = SHIP.machines[j.machine].cond, claimed = claimJob(id);
      setShipNow(4 * 1440 + 19 * 60); machinesNow();
      const still = SHIP.jobs.find(x => x.id === id), mine = still && still.claimedBy === 'you' && still.status === 'claimed';
      const fin = finishJob(id), after = SHIP.machines[j.machine].cond;
      if (typeof turnInJob === 'function') turnInJob(id);   // with the board's Turn in on, a finished job is yours until you hand it in (one at a time)
      const took = takePart('relay'), stock = SHIP.stores.relay;
      // one job at a time; one you leave goes back on the board after 12 ship hours
      // the next job you can take, waiting up to a day for one to be found
      const takeable = () => { for (let n = 0; n < 24; n++) { const x = jobsBoard().find(x => !x.claimedBy && jobTier(x) <= PLAYER_TIER && x.machine && !ENGINE_KINDS.has(machineById(x.machine).kind)); if (x) return x; setShipNow(shipNow() + 60); } return null; };
      const k = takeable();
      let lapse = null, oneAtATime = null;
      if (k) { claimJob(k.id); const k2 = jobsBoard().find(x => !x.claimedBy && x.id !== k.id && jobTier(x) <= PLAYER_TIER); oneAtATime = !k2 || !claimJob(k2.id);
               setShipNow(shipNow() + 13 * 60); machinesNow(); const back = SHIP.jobs.find(x => x.id === k.id); lapse = !back || back.claimedBy !== 'you'; }
      // progress keeps it yours: touched 10 hours in, it's still yours 13 hours after the claim
      let kept = null;
      if (typeof playerShiftOn === 'function') { let d = Math.floor(shipNow() / 1440) + 1; while (!playerShiftOn(d)) d++; if (d > Math.floor(shipNow() / 1440) + 1) { setShipNow((d - 1) * 1440 + 9 * 60); machinesNow(); } }   // on your days off the crew take every job: try on a shift day
      // none waiting (with the crew's rota, they may have claimed them all): make one, as the oven above
      const breakOne = () => { for (const m of machineList()) { const s = SHIP.machines[m.id];
          if (ENGINE_KINDS.has(m.kind) || m.id === '3-oven-1' || !s || s.cond < 60) continue;
          s.cond = 40; s.state = machineState(40); setShipNow(shipNow() + 60); machinesNow();
          const x = jobsBoard().find(x => x.machine === m.id && !x.claimedBy && jobTier(x) <= PLAYER_TIER); if (x) return x; } return null; };
      const k3 = takeable() || breakOne();
      if (k3 && claimJob(k3.id)) { setShipNow(shipNow() + 600); touchJob(k3.id); setShipNow(shipNow() + 180); machinesNow(); const b = SHIP.jobs.find(x => x.id === k3.id); kept = !!b && b.claimedBy === 'you'; dropJob(k3.id); }
      const s0 = SHIP.stores.relay || 0, ret = returnPart('relay') && SHIP.stores.relay === s0 + 1;
      if (typeof SHARE_ON !== 'undefined') SHARE_ON = true;
      return { id, claimed, mine, fin, before, after, took, stock, oneAtATime, lapse, kept, ret };
    })()""")
    print(f"Your job: {y}")
    if y.get('none') or not (y['claimed'] and y['mine'] and y['fin'] and y['after'] >= 90): fail('claiming and finishing a job yourself')
    if y.get('oneAtATime') is not True or y.get('lapse') is not True: fail('one job at a time, and a job left 12 hours goes back')
    if y.get('kept') is not True or not y.get('ret'): fail('touchJob keeps a job in progress yours; returnPart puts a part back')

    # 5b. food by cart: cartClaim is one rule, pure in replays, the same twice live, and never past the store's cap
    ck = g.ev("""(() => {
      const rev = MACH_REV, hold = SHIP.hold.meals, a = [];
      for (let t = 1440; t < 1440 * 3; t += 60) for (const cold of [0, 60, 89, 90, 150, 249, 250, 300]) a.push(JSON.stringify(cartClaim(t, cold, { replay: true })));
      const b = []; for (let t = 1440; t < 1440 * 3; t += 60) for (const cold of [0, 60, 89, 90, 150, 249, 250, 300]) b.push(JSON.stringify(cartClaim(t, cold, { replay: true })));
      const pure = MACH_REV === rev && SHIP.hold.meals === hold && a.join() === b.join();
      let overCap = 0, urgentMissed = 0, nightDaily = 0;
      for (let t = 1440; t < 1440 * 3; t += 60) for (const cold of [0, 60, 89, 150, 249, 280]) {
        const r = cartClaim(t, cold, { replay: true }), hr = (t / 60) % 24;
        if (r && cold + r.meals > coldCap()) overCap++;
        if (!r && cold < CART_URGENT) urgentMissed++;
        if (r && cold >= CART_URGENT && (hr < 9 || hr >= 17)) nightDaily++;
      }
      return { pure, overCap, urgentMissed, nightDaily };
    })()""")
    print(f"Food by cart: replays pure {ck['pure']}, over the cap {ck['overCap']}, urgent runs missed {ck['urgentMissed']}, daily runs off the day shift {ck['nightDaily']}")
    if not ck['pure'] or ck['overCap'] or ck['urgentMissed'] or ck['nightDaily']: fail('cartClaim')

    # 5c. the cart run as your job (0.33.16): a food run on the day shift that isn't urgent waits an hour for you;
    # you can take it and finish it; one you leave goes to the crew after the hour; an urgent one goes to them at once
    cr = g.ev("""(() => {
      JOBS_ON = true; MACH_HOUR = null; MACH_SEEN = -1; setShipNow(2 * 1440 + 10 * 60); machinesNow();
      const live = (t, cold) => { setShipNow(t); const r = cartClaim(t, cold); machinesNow(); return r && SHIP.jobs.find(j => j.id === 'restock-meals@' + Math.floor(t / 60)); };
      const a = live(2 * 1440 + 10 * 60, 200), waits = !!a && !a.claimedBy && a.urgency < 2;
      const ha = a && Math.floor(a.posted / 60), w0 = !!a && cartWaiting(ha);
      setShipNow(shipNow() + 20); const took = !!a && claimJob(a.id), stops = jobStops(a).map(x => x.step).join(' '), w1 = !!a && cartWaiting(ha);
      const fin = took && finishJob(a.id) && SHIP.jobs.find(j => j.id === a.id).doneBy === 'you', w2 = !!a && cartWaiting(ha);
      const b = live(2 * 1440 + 13 * 60, 200), leftThen = !!b && !b.claimedBy;
      setShipNow(2 * 1440 + 14 * 60); machinesNow(); const crewTook = !!b && !!b.claimedBy && b.claimedBy !== 'you' && b.start >= b.found + 60;
      const c = live(2 * 1440 + 15 * 60, 50), urgentNow = !!c && !!c.claimedBy && c.claimedBy !== 'you';
      const waitingOk = !w0 && w1 && !w2 && !!b && !cartWaiting(Math.floor(b.posted / 60));   // cartWaiting: only while it's yours (0.33.20), released once done
      return { waits, took, fin, stops, leftThen, crewTook, urgentNow, waitingOk };
    })()""")
    print(f"Cart run as your job: {cr}")
    if not all(cr[k] for k in ('waits', 'took', 'fin', 'leftThen', 'crewTook', 'urgentNow', 'waitingOk')) or cr['stops'] != 'cart load unload return': fail('the cart run as your job')

    # 5d. tapping a machine (0.33.18): one with a use starts, shows as running, and your use wears it a little at the
    # next hour (a crew member's adds nothing); a broken one doesn't start; one without a use only says how it is.
    # Supplies: Stores' Mail (late deliveries, parts nobody can make running out, food low) has the shared shape and
    # isn't sent twice for one shortage; a late week's delivery lands on its late day. Tier locks: a hatch with a tier
    # keeps you (Tier 1) out and lets Works crew of that rank in.
    mu = g.ev("""(() => {
      const t0 = (SHIP_START.day - 1) * 1440 + SHIP_START.min;
      const wearAt = (tap, who) => { JOBS_ON = false; MACH_HOUR = null; MACH_SEEN = -1; setShipNow(t0 + 30); machinesNow(); const r = tap ? machineUse('4-washer-1', who) : null;
        const run = machineLook('4-washer-1').running; setShipNow(t0 + 150); machinesNow(); return [SHIP.machines['4-washer-1'].cond, r, run]; };
      const [plain] = wearAt(false), [yours, r, running] = wearAt(true, 'you'), [crews] = wearAt(true, 'olu');
      const extra = plain - yours, crewSame = Math.abs(plain - crews) < 1e-9;
      const b = SHIP.machines['3-oven-1']; b.cond = 5; b.state = machineState(5); MACH_REV++;
      const broken = machineUse('3-oven-1'), plainUse = machineUse('4-scrubber-1'), none = machineUse('no-such-machine');
      // Mail over 28 days with the real crew
      SHIP.mail = [];                                      // Stores' Mail, through section 15's mailSend (none without it)
      JOBS_ON = true; MACH_HOUR = null; MACH_SEEN = -1; setShipNow(t0); machinesNow();
      let lateLanded = null;
      for (let t = t0; t <= t0 + 28 * 1440; t += 60) {
        setShipNow(t); machinesNow();
        const d = SHIP.time.day, md = t % 1440;
        if (deliveryLate(d) && weekday(d) === DELIVERY.day + deliveryLate(d) && md === DELIVERY.hour * 60 + 60) lateLanded = SHIP.jobs.some(j => j.kind === 'restock' && j.cargo === 'stores' && Math.abs(j.posted - (t - 60)) < 1) || Object.keys(SHIP.hold).some(k => k !== 'meals');
      }
      const sent = (SHIP.mail || []).filter(m => m.from === 'Stores').sort((a, b) => a.at - b.at || a.id - b.id);
      const shapeOk = sent.every(m => Number.isFinite(m.at) && typeof m.subject === 'string' && typeof m.body === 'string' && m.body.length > 20);
      const subj = sent.map(m => m.subject), late = sent.filter(m => /late/.test(m.subject)).length;
      let twice = 0; for (let i = 1; i < sent.length; i++) if (sent.slice(0, i).some(o => o.subject === sent[i].subject && sent[i].at - o.at < 60)) twice++;
      // tier locks, on a scratch copy of one service hatch
      const e = [...EDGES.values()].find(x => x.service), was = e && e.tier;
      let tiers = null;
      if (e) { e.tier = 3; const works = schedPeople().filter(p => p.dept === 'works'), jr = works.find(p => p.rank === 'junior'), sr = works.find(p => (CREW_TIER[p.rank] || 0) >= 3);
               tiers = { you: hatchPassable(e.key, 'player'), junior: jr ? hatchPassable(e.key, jr) : null, senior: sr ? hatchPassable(e.key, sr) : null };
               e.tier = 1; tiers.youTier1 = hatchPassable(e.key, 'player'); if (was) e.tier = was; else delete e.tier; }
      setShipNow(t0); JOBS_ON = true;
      return { extra, ran: r.ran, running, text: r.text, crewSame, broken: broken.ran, brokenText: broken.text, plainUse: plainUse.ran, none: none.ran,
               mails: sent.length, late, lateLanded, shapeOk, twice, subj: subj.slice(0, 6), tiers };
    })()""")
    print(f"Tapping a machine: '{mu['text']}' ran {mu['ran']}, running {mu['running']}, extra wear {mu['extra']:.3f}, a crew member's adds none {mu['crewSame']}; broken starts {mu['broken']} ('{mu['brokenText']}'); no use starts {mu['plainUse']}")
    print(f"Stores' Mail over 28 days: {mu['mails']} ({mu['late']} late deliveries, landed on the late day {mu['lateLanded']}), shape ok {mu['shapeOk']}, sent twice {mu['twice']}: {mu['subj']}")
    print(f"Tier locks (a tier-3 hatch; you pass every hatch since 0.27.35, crew by rank): {mu['tiers']}")
    if not (mu['ran'] and mu['running'] and .25 < mu['extra'] < .35 and mu['crewSame'] and not mu['broken'] and not mu['plainUse'] and not mu['none']): fail('machineUse')
    if not mu['shapeOk'] or mu['twice'] or (mu['late'] and mu['lateLanded'] is False) or mu['mails'] > 28: fail("Stores' Mail")
    tt = mu['tiers']
    # 0.27.35 (the user, 2026-10-17): the player passes every service hatch whatever its tier; crew still pass by rank
    if tt and (not tt['you'] or not tt['youTier1'] or tt['junior'] or tt['senior'] is False): fail('tier locks')

    # 5e. chores (0.33.19): many kinds of job, every stop a real place, tier-1 ones only in rooms you can enter;
    # openJobs gives what you may take, in the shared shape; you can take a chore and finish it, and it does its work
    ch = g.ev("""(() => {
      const t0 = (SHIP_START.day - 1) * 1440 + SHIP_START.min, kinds = {}, badStop = [], badTier = [];
      for (let d = 1; d <= 14; d++) for (const c of choresOfDay(d)) {
        kinds[c.kind] = (kinds[c.kind] || 0) + 1;
        for (const st of c.cand.stops) if (!placeById(st.placeId)) badStop.push(c.kind + ' ' + c.cand.key);
        const tier = Math.max(CHORES[c.kind].tier, c.cand.tier || 0, ...c.cand.stops.map(st => placeTier(st.placeId)));
        if (tier < Math.max(...c.cand.stops.map(st => placeTier(st.placeId)))) badTier.push(c.kind + ' ' + c.cand.key);
      }
      JOBS_ON = true; MACH_HOUR = null; MACH_SEEN = -1; let o = [], seen = new Set();
      for (let t = t0 + 1440 + 180; t < t0 + 4 * 1440; t += 60) { setShipNow(t); machinesNow(); for (const x of openJobs()) { if (!seen.has(x.id)) { seen.add(x.id); o.push(x); } } }
      const keys = ['id', 'title', 'kind', 'deck', 'at', 'room', 'place', 'tier', 'mins', 'parts', 'bring', 'urgency', 'state'];
      const shapeBad = o.filter(x => !keys.every(k => k in x) || !(x.tier <= PLAYER_TIER) || !(x.mins > 0) || !Array.isArray(x.at) || !(x.deck >= 1)).map(x => x.id);
      const openKinds = [...new Set(o.map(x => x.kind))];
      // take a chore and finish it
      const chore = () => openJobs().find(x => ['calibrate', 'delivery', 'lamp', 'vent', 'round', 'fault'].includes(x.kind));
      let c = null; for (let n = 0; n < 48 && !(c = chore()); n++) { setShipNow(shipNow() + 60); machinesNow(); }   // wait up to two days for one
      let took = null, fin = null, stops = null, helped = null;
      if (c) { const j = SHIP.jobs.find(x => x.id === c.id), before = j.machine ? SHIP.machines[j.machine].cond : null;
               took = claimJob(c.id); stops = jobStops(j).map(x => x.step + '@' + (x.places[0] || '-')).join(' ');
               fin = finishJob(c.id) && SHIP.jobs.find(x => x.id === c.id).doneBy === 'you'; helped = before === null || SHIP.machines[j.machine].cond >= before; }
      setShipNow(t0);
      return { kinds, badStop: badStop.slice(0, 4), badTier: badTier.slice(0, 4), seen: o.length, shapeBad: shapeBad.slice(0, 4), openKinds, c: c && c.title, took, fin, stops, helped,
               sample: o.slice(0, 4).map(x => x.title + ' (Deck ' + x.deck + ', ' + x.mins + ' min' + (x.parts.length ? ', bring ' + x.parts.join(' ') : x.bring ? ', ' + x.bring : '') + ')') };
    })()""")
    print(f"Chores over 14 days: {ch['kinds']}; stops not real places {ch['badStop']}, tiers below their rooms {ch['badTier']}")
    print(f"openJobs (days 2-4): {ch['seen']} jobs you could take, kinds {ch['openKinds']}, bad shape {ch['shapeBad']}; e.g. {ch['sample']}")
    print(f"  took '{ch['c']}': {ch['took']}, stops {ch['stops']}, finished {ch['fin']}, did its work {ch['helped']}")
    if len(ch['kinds']) < 7 or ch['badStop'] or ch['badTier'] or ch['shapeBad'] or len(ch['openKinds']) < 5: fail('chores and openJobs')
    if not (ch['took'] and ch['fin'] and ch['helped']): fail('taking and finishing a chore')

    # 5g. turning jobs in (0.33.23, with TURN_IN on for the test): a chore's stops ticked off one by one with
    # jobStepDone; after the last its work is done (the effect happens) but it stays yours, past the 12-hour lapse and
    # off openJobs, until turnInJob completes it; finishJob only does the work. Off again afterwards
    ti = g.ev("""(() => {
      const t0 = (SHIP_START.day - 1) * 1440 + SHIP_START.min;
      JOBS_ON = true; MACH_HOUR = null; MACH_SEEN = -1; setShipNow(t0 + 1440 + 180); machinesNow(); TURN_IN = true;
      let c = null; for (let n = 0; n < 72 && !(c = openJobs().find(x => x.kind === 'delivery' || x.kind === 'lamp' || x.kind === 'vent' || x.kind === 'round')); n++) { setShipNow(shipNow() + 60); machinesNow(); }
      if (!c) { TURN_IN = false; return { none: true }; }
      claimJob(c.id); const j = SHIP.jobs.find(x => x.id === c.id), n = jobStops(j).length, steps = [];
      for (let k = 0; k < n; k++) steps.push(jobStepDone(c.id, k));
      const marked = jobStops(j).every(x => x.done), workDone = !!j.workDone, mine = myJob() && myJob().id === c.id;
      setShipNow(shipNow() + 13 * 60); machinesNow();
      const kept = j.claimedBy === 'you' && j.status === 'claimed', offBoard = !openJobs().some(x => x.id === c.id), bad = jobStepDone(c.id, 99).ok === false;
      const tin = turnInJob(c.id), done = j.status === 'done' && j.doneBy === 'you', again = turnInJob(c.id);
      // a machine job: finishJob does the work, turnInJob completes it
      let m = null; for (let n2 = 0; n2 < 48 && !(m = openJobs().find(x => x.kind === 'service')); n2++) { setShipNow(shipNow() + 60); machinesNow(); }
      let mOk = null; if (m) { claimJob(m.id); const mj = SHIP.jobs.find(x => x.id === m.id); finishJob(m.id); const fixed = SHIP.machines[mj.machine].cond >= 99 && mj.status === 'claimed' && !!mj.workDone; mOk = fixed && turnInJob(m.id) && mj.status === 'done'; }
      TURN_IN = false; setShipNow(t0);
      return { kind: c.kind, n, left: steps.map(x => x.left).join(','), lastDone: steps[n - 1].done, marked, workDone, mine, kept, offBoard, bad, tin, done, again, mOk };
    })()""")
    print(f"Turning jobs in: {ti}")
    if ti.get('none') or not all(ti[k] for k in ('lastDone', 'marked', 'workDone', 'mine', 'kept', 'offBoard', 'bad', 'tin', 'done')) or ti['again'] or ti['mOk'] is False: fail('turning jobs in')

    # 5h. event hooks and favours (Pillar 3, C7, 0.33.24), with a stand-in event (section 18's eventNow, eventMod and
    # SHIP_EVENTS put back afterwards): an event's wear multiplies only its system; its jobs are posted once for the
    # phase, tagged and tiered, and the crew take them; favours stay off the board and away from the crew, are accepted,
    # stepped and handed back, and lapse if left; with no event nothing changes (the runs above)
    evr = g.ev("""(() => {
      const t0 = (SHIP_START.day - 1) * 1440 + SHIP_START.min, run = d => { JOBS_ON = false; MACH_HOUR = null; MACH_SEEN = -1; setShipNow(t0); machinesNow(); setShipNow(t0 + d * 1440); machinesNow(); return { ...Object.fromEntries(Object.entries(SHIP.machines).map(([k, v]) => [k, v.cond])) }; };
      const plain = run(3);
      window.__sc("window.__keepEv = [typeof eventNow === 'function' ? eventNow : undefined, typeof eventMod === 'function' ? eventMod : undefined]");
      window.__ev = { id: 'mcStorm', phase: 'onset', day: 0 }; window.__ev0 = Math.floor(t0 / 1440);   // the event's day counts on, as section 18's does
      const def = { id: 'mcStorm', jobs: { onset: [ { id: 'lounge', kind: 'secure', where: 'lounge', tier: 1 }, { kind: 'vent' }, { id: 'bat', kind: 'check', machine: machineList().find(m => MACHINE_KINDS[m.kind].sys === 'power' && m.kind !== 'lights').id, tier: 3 },
        { id: 'packs', title: 'Carry packs to the junction', tier: 1, stops: [{ placeId: '5-parts-1', mins: 5, tag: 'pickup' }, { deck: 5, machine: 'junction', mins: 10, tag: 'drop' }] } ] } };   // the last in section 18's stop shape
      if (Array.isArray(SHIP_EVENTS)) SHIP_EVENTS.push(def); else SHIP_EVENTS.mcStorm = def;
      window.__scored = {}; window.__mine = {};
      window.__sc("window.__keepEv.push(typeof eventScore === 'function' ? eventScore : undefined, typeof eventMine === 'function' ? eventMine : undefined); eventNow = (t = shipNow()) => window.__ev && { ...window.__ev, day: Math.floor(t / 1440) - window.__ev0 }; eventMod = (k, key) => !window.__ev ? null : k === 'wear' && key === 'power' ? 2 : k === 'effect' && key === 'blackouts' ? true : null; eventScore = (k, n) => { window.__scored[k] = (window.__scored[k] || 0) + n; }; eventMine = (k, n) => { window.__mine[k] = (window.__mine[k] || 0) + n; }");
      const storm = run(3);
      const sys = id => MACHINE_KINDS[machineById(id).kind].sys;
      const fasterPower = Object.keys(plain).filter(id => sys(id) === 'power').every(id => storm[id] < plain[id] - 1e-9 || plain[id] === 0);
      const othersSame = Object.keys(plain).filter(id => sys(id) !== 'power').every(id => Math.abs(storm[id] - plain[id]) < 1e-9);
      const keepEvent = SHIP.event; SHIP.event = { id: 'mcStorm', startDay: 1, phase: 'onset', threads: {}, mine: { 'wants:lounge': true } };   // you volunteered for 'lounge'
      JOBS_ON = true; MACH_HOUR = null; MACH_SEEN = -1; setShipNow(t0 + 60); machinesNow();
      const volunteered = (SHIP.jobs.find(j => j.event === 'mcStorm' && j.eventJob === 'lounge') || {}).claimedBy === 'you'; SHIP.event = keepEvent;   // yours as it went up (left 12 hours, it would go back on the board)
      setShipNow(t0 + 1440); machinesNow(); setShipNow(t0 + 1440 + 600); machinesNow();
      for (const j of SHIP.jobs) if (j.event === 'mcStorm' && j.claimedBy === 'you') dropJob(j.id);
      const ej = SHIP.jobs.filter(j => j.event === 'mcStorm'), once = ej.length === 4 && new Set(ej.map(j => j.id)).size === 4;
      const packs = ej.find(j => j.target === 'packs'), packsOk = !!packs && packs.stops.length === 2 && packs.stops[1].deck === 5 && packs.eventJob === 'packs';
      // blackouts while the effect is on: at most one an hour, 15-60 minutes, scored as the 'blackout' thread
      const bos = []; for (let h = Math.floor((t0 + 1440) / 60); h <= Math.floor((t0 + 1440 + 600) / 60); h++) { const b = blackoutHour(h); if (b) bos.push(b); }
      const boOk = bos.every(b => b.to - b.from >= 15 && b.to - b.from <= 60 && Math.floor(b.from / 60) === Math.floor((b.to - 1) / 60)) && (window.__scored.blackout || 0) >= bos.reduce((a, b) => a + b.to - b.from, 0);
      const tagged = ej.every(j => j.tier >= 1 && j.title && j.stops.length), crewTook = ej.filter(j => j.claimedBy && j.claimedBy !== 'you').length;
      window.__ev = null;                                    // the event over: no more posted
      setShipNow(t0 + 1440 + 900); machinesNow(); const after = SHIP.jobs.filter(j => j.event === 'mcStorm').length;
      // an event job you complete counts as yours (eventMine('jobs'))
      const mineJob = postEventJob({ id: 'mine', kind: 'vent' }, { event: 'mcStorm', forYou: true }), mineOk = !!mineJob && finishJob(mineJob) && window.__mine.jobs === 1;
      // favours
      const f = favourPost({ from: schedPeople()[0].id, title: 'A tray for a friend', where: 'mess', kind: 'tea' });
      const offBoard = !jobsBoard().some(j => j.id === f) && !openJobs().some(x => x.id === f);
      setShipNow(shipNow() + 180); machinesNow(); const crewLeft = !favourById(f).claimedBy;
      const acc = favourAccept(f), steps = jobStops(favourById(f)).map(x => x.step).join(' '), backEarly = jobStepDone(f, jobStops(favourById(f)).length - 1).ok;
      const s0 = jobStepDone(f, 0), tin = favourTurnIn(f), done = favourById(f).status === 'done' && favourById(f).doneBy === 'you';
      const g2 = favourPost({ from: schedPeople()[1].id, title: 'Find my datapad', where: 'gym' });
      setShipNow(shipNow() + 3000); machinesNow(); const lapsed = favourById(g2).status === 'done' && favourById(g2).lapsed;
      // trays by cart (0.33.25): posted once a day, left for you half an hour, then the crew push a cart of trays to the bridge
      const tid = cartTrays({ trays: 6, at: shipNow(), to: 'bridge' }), tid2 = cartTrays({ trays: 6, at: shipNow(), to: 'bridge' }), tj = SHIP.jobs.find(j => j.id === tid);
      const trayOk = !!tj && tid === tid2 && tj.stops[1].deck === 1 && openJobs().some(x => x.id === tid);
      let trayCrew = null; for (let n = 0; n < 30 && !(tj.claimedBy); n++) { setShipNow(shipNow() + 60); machinesNow(); }
      trayCrew = !!tj.claimedBy && tj.claimedBy !== 'you' && (tj.segs || []).some(sg => sg.hold === 'cartfull');
      // traysArrivedAt (0.33.28): the crew's drop-off end; yours, the minute you tick off the drop-off
      const tday = Math.floor(tj.posted / 1440) + 1, tAt = traysArrivedAt(tday), tdrop = tj.segs.filter(sg => sg.tag === 'drop').pop();
      let tMine = null;
      { const yid = cartTrays({ trays: 2, at: shipNow() + 1440, to: 'bridge' }); setShipNow(shipNow() + 1440); machinesNow(); const yj = SHIP.jobs.find(j => j.id === yid);
        if (yj && claimJob(yid)) { const before = traysArrivedAt(tday + 1); jobStepDone(yid, 0); setShipNow(shipNow() + 30); jobStepDone(yid, 1); tMine = before === null && traysArrivedAt(tday + 1) === shipNow(); dropJob(yid); } }
      const trayArrive = tAt === tdrop.to && tMine !== false;
      // cold cabins (0.33.31): with guests aboard, each hour Deck 4's heating is faulty or worse scores 'coldCabins'
      window.__sc("eventMod = (k, key) => !window.__ev ? null : k === 'effect' && key === 'guests' ? true : null");
      const htr = machineList().find(m => m.deck === 4 && (m.kind === 'heater' || m.kind === 'heatpump'));
      let coldOk = null;
      if (htr) { window.__ev = { id: 'mcStorm', phase: 'onset', day: 0 }; window.__scored = {}; JOBS_ON = true; MACH_HOUR = null; MACH_SEEN = -1; setShipNow(t0); machinesNow();
        const warm = (setShipNow(t0 + 180), machinesNow(), window.__scored.coldCabins || 0);
        SHIP.machines[htr.id].cond = 30; SHIP.machines[htr.id].state = machineState(30); machRecord(MACH_HOUR - 1); MACH_REV++;
        setShipNow(t0 + 360); machinesNow(); const cold = window.__scored.coldCabins || 0;
        window.__ev = null; setShipNow(t0 + 540); machinesNow(); const gone = window.__scored.coldCabins || 0;
        coldOk = warm === 0 && cold >= 2 && gone === cold; }
      // put it all back
      window.__sc("eventNow = window.__keepEv[0]; eventMod = window.__keepEv[1]; eventScore = window.__keepEv[2]; eventMine = window.__keepEv[3]");
      if (Array.isArray(SHIP_EVENTS)) SHIP_EVENTS.splice(SHIP_EVENTS.indexOf(def), 1); else delete SHIP_EVENTS.mcStorm;
      SHIP.jobs = SHIP.jobs.filter(j => j.event !== 'mcStorm' && j.kind !== 'favour' && j.chore !== 'trays'); setShipNow(t0); JOBS_ON = true;
      return { fasterPower, othersSame, once, tagged, crewTook, after, titles: ej.map(j => j.title + ' (tier ' + j.tier + ')'), offBoard, crewLeft, acc, steps, backEarly, s0: s0.done, tin, done, lapsed, trayOk, trayCrew, trayArrive, tMine, volunteered, coldOk, packsOk, blackouts: bos.length, blackoutMin: window.__scored.blackout || 0, boOk, mineOk };
    })()""")
    print(f"Event hooks and favours: {evr}")
    if not (evr['fasterPower'] and evr['othersSame'] and evr['once'] and evr['tagged'] and evr['after'] == 4 and evr['packsOk'] and evr['volunteered'] and evr['coldOk'] is not False and evr['boOk'] and evr['mineOk'] and evr['offBoard'] and evr['crewLeft'] and evr['acc']
            and evr['steps'].endswith('return') and not evr['backEarly'] and evr['s0'] and evr['tin'] and evr['done'] and evr['lapsed'] and evr['trayOk'] and evr['trayCrew'] and evr['trayArrive']): fail('event hooks and favours')

    # 5f. food runs in live play (0.33.21): the galley stepping live and the job list together for six days, nobody
    # pushing carts for you: every food run is taken by the crew (or goes unseen) within 2 hours of its hour's wait,
    # never sits open for days; the cold store never runs empty and the hold isn't drained by repeat orders
    fr = g.ev("""(() => {
      if (typeof galleyAdvance !== 'function' || !cartsCarryFood || typeof FOOD === 'undefined' || FOOD.restock !== 'carts') return { skipped: true };
      const t0 = (SHIP_START.day - 1) * 1440 + SHIP_START.min;
      JOBS_ON = true; MACH_HOUR = null; MACH_SEEN = -1; SHIP.galley = null; setShipNow(t0); machinesNow(); galleyAdvance(t0);
      let late = [], coldMin = 1e9, holdMin = 1e9, runs = new Set(), claimed = new Set();
      for (let t = t0 + 1440; t <= t0 + 7 * 1440; t += 10) {
        setShipNow(t); galleyAdvance(t); machinesNow();
        coldMin = Math.min(coldMin, SHIP.galley.cold.meals); if (SHIP.hold.meals !== undefined) holdMin = Math.min(holdMin, SHIP.hold.meals);
        for (const j of SHIP.jobs) if (j.cargo === 'meals') { runs.add(j.id); if (j.claimedBy && j.claimedBy !== 'you') claimed.add(j.id); if (j.status === 'open' && t > leaveEnd(j) + 120) late.push(j.id + ' open at ' + hhmm(t % 1440) + ' day ' + SHIP.time.day); }
      }
      setShipNow(t0); SHIP.galley = null;
      return { runs: runs.size, crew: claimed.size, late: [...new Set(late)].slice(0, 4), coldMin, holdMin };
    })()""")
    print(f"Food runs in live play, 6 days: {fr}")
    if not fr.get('skipped') and (fr['late'] or fr['coldMin'] <= 0 or fr['holdMin'] < 100 or fr['runs'] < 5 or fr['runs'] > 30 or fr['crew'] < fr['runs'] / 2): fail('food runs in live play')

    # 5i. the board through a week (0.33.32, the user's "the job board never has any jobs", and two days off a week):
    # the real crew for a Monday-to-Sunday week, nobody taking jobs for you. On a weekday's day shift there's
    # nearly always something for you (openJobs), from the game's first hour (06:00 on day 1) on; never more than HOLD_MAX small jobs held
    # for you. On Saturday and Sunday (playerShiftOn; a stand-in Monday-to-Friday rule if section 14's still says
    # every day) nothing is held: the crew take your kind of job, and you can still take one from the board.
    wk = g.ev("""(() => {
      const realOn = playerShiftOn, stand = [1, 2, 3, 4, 5, 6, 7].every(d => playerShiftOn(d));
      if (stand) window.__sc("playerShiftOn = d => weekday(d) < 5");
      const t0 = (SHIP_START.day - 1) * 1440 + SHIP_START.min;
      JOBS_ON = true; MACH_HOUR = null; MACH_SEEN = -1; setShipNow(t0); machinesNow();
      const small = j => forYou(j) && !j.leave && !j.cargo;   // the delivery (cargo 'stores') isn't one of them from 0.33.42: it waits till 14:00 on its own rule
      const out = { stand, emptyStart: 0, firstMorning: null, empty: 0, hours: 0, sum: 0, maxHeld: 0, offHeld: [], offCrew: 0, offTook: null, offOpen: 0 };
      for (let t = t0; t < t0 + 7 * 1440; t += 60) {
        setShipNow(t); machinesNow();
        const d = SHIP.time.day, m = t % 1440, open = SHIP.jobs.filter(j => j.status === 'open' && !j.claimedBy && j.found <= t);
        out.maxHeld = Math.max(out.maxHeld, open.filter(j => small(j) && t < leaveEnd(j)).length);
        if (playerShiftOn(d)) {
          if (m >= DAY_SHIFT[0] && m < DAY_SHIFT[1]) { const n = openJobs('you').length; out.hours++; out.sum += n; if (!n) out.empty++; if (d === SHIP_START.day && m === DAY_SHIFT[0]) out.firstMorning = n; }
          if (d === SHIP_START.day && m < DAY_SHIFT[0] && m >= SHIP_START.min && !openJobs('you').length) out.emptyStart++;
        } else {
          for (const j of open) if (small(j) && t < leaveEnd(j)) out.offHeld.push(j.id + ' on day ' + d);
          out.offOpen += openJobs('you').length;
          if (out.offTook === null && openJobs('you').length) { const id = openJobs('you')[0].id; out.offTook = claimJob(id) && dropJob(id); }
        }
      }
      out.offCrew = SHIP.jobs.filter(j => small(j) && j.claimedBy && j.claimedBy !== 'you' && !playerShiftOn(Math.floor(j.found / 1440) + 1)).length;
      out.offHeld = [...new Set(out.offHeld)].slice(0, 4); out.mean = Math.round(out.sum / out.hours * 10) / 10;
      if (stand) playerShiftOn = realOn;
      setShipNow(t0);
      return out;
    })()""")
    print(f"The board through a week: weekday day shift {wk['mean']} jobs for you on average, {wk['empty']} of {wk['hours']} hours with none, "
          f"{wk['firstMorning']} at the shift's start on day 1 ({wk['emptyStart']} empty hours before that), at most {wk['maxHeld']} held; days off{' (stand-in rule)' if wk['stand'] else ''}: held {wk['offHeld']}, "
          f"crew took {wk['offCrew']} of your kind, you could take one {wk['offTook']} ({wk['offOpen']} job-hours open)")
    if wk['mean'] < 2 or wk['empty'] > wk['hours'] / 10 or not wk['firstMorning'] or wk['emptyStart'] or wk['maxHeld'] > g.ev("HOLD_MAX") or wk['offHeld'] or wk['offCrew'] < 1 or (wk['offOpen'] and wk['offTook'] is not True):
        fail('the board through a week')

    # 5j. the garden (0.33.34, for the galley engineer's working garden): grow lights are machines like any other;
    # gardenAt(t) is pure, all 1 while the garden's machines are worn or better (a fresh ship), and falls when the irrigation, dosing or grow
    # lights are broken (only that one); gardenCarry posts one crate run (asking twice gives the same id), it waits
    # for you, then a crew member takes it, carryWaiting is true until the drop-off ends and false after; yours lands
    # through the galley's galleyCarryLand (a stand-in here if section 16 hasn't one) when you tick off the drop
    gd = g.ev("""(() => {
      const t0 = (SHIP_START.day - 1) * 1440 + SHIP_START.min;
      JOBS_ON = true; MACH_HOUR = null; MACH_SEEN = -1; setShipNow(t0 + 180); machinesNow();
      const out = { lights: machineList().filter(m => m.kind === 'growlight').map(m => m.id) };
      const g0 = gardenAt(shipNow()), r0 = MACH_REV, g1 = gardenAt(shipNow()); out.fine = g0; out.pure = MACH_REV === r0 && JSON.stringify(g0) === JSON.stringify(g1);
      const broke = {};
      for (const kind of ['irrigation', 'nutrient', 'growlight']) {
        const save = JSON.stringify(SHIP.machines);
        for (const m of machineList()) if (m.kind === kind) { SHIP.machines[m.id].cond = 0; SHIP.machines[m.id].state = 'broken'; }
        machRecord(MACH_HOUR - 1); broke[kind] = gardenAt(shipNow());
        SHIP.machines = JSON.parse(save); machRecord(MACH_HOUR - 1);
      }
      out.broke = broke;
      // a crate run at 09:00 on day 1: waits for you, then the crew
      setShipNow(t0 + 180); const id = gardenCarry({ crates: 3 }), id2 = gardenCarry({ crates: 3, at: t0 + 180 });
      out.id = id; out.same = id === id2; out.forYou = openJobs('you').some(x => x.id === id); out.waiting0 = carryWaiting(id);
      let arrived = null, claimedBy = null;
      for (let t = t0 + 180; t < t0 + 180 + 600; t += 10) { setShipNow(t); machinesNow(); const j = SHIP.jobs.find(x => x.id === id); claimedBy = j.claimedBy; if (!carryWaiting(id)) { arrived = t; break; } }
      out.claimedBy = claimedBy; out.arrived = arrived !== null; out.after = arrived !== null && carryArrivedAt(id) <= arrived && carryWaiting(id, carryArrivedAt(id) - 1);
      // yours: take one, tick off the pickup and the drop
      const real = typeof galleyCarryLand === 'function' ? galleyCarryLand : null, landed = [];
      if (!real) window.__sc("galleyCarryLand = id => { window.__landed.push(id); return 1; }"); else window.__sc("window.__gcl = galleyCarryLand; galleyCarryLand = id => { window.__landed.push(id); return window.__gcl(id); }");
      window.__landed = landed;
      const mine = gardenCarry({ crates: 2 }); for (const j of SHIP.jobs) if (j.claimedBy === 'you') { j.claimedBy = null; j.status = 'open'; }
      out.took = claimJob(mine); const st = jobStops(SHIP.jobs.find(x => x.id === mine));
      out.stops = st.map(x => x.step).join(' ');
      const wBefore = carryWaiting(mine); st.forEach((x, k) => jobStepDone(mine, k));
      out.mineWaiting = [wBefore, carryWaiting(mine)]; out.landed = window.__landed.slice();
      if (!real) window.__sc("galleyCarryLand = undefined"); else window.__sc("galleyCarryLand = window.__gcl");
      SHIP.jobs = SHIP.jobs.filter(j => j.id !== mine && j.id !== id); setShipNow(t0);
      return out;
    })()""")
    print(f"The garden: grow lights {gd['lights']}; gardenAt all fine {gd['fine']}, pure {gd['pure']}; broken: {gd['broke']}")
    print(f"  crate run {gd['id']}: once {gd['same']}, for you first {gd['forYou']}, taken by {gd['claimedBy']}, arrived {gd['arrived']}, carryWaiting till then {gd['after']}; "
          f"yours: took {gd['took']}, stops '{gd['stops']}', waiting before/after the drop {gd['mineWaiting']}, landed {gd['landed']}")
    b = gd['broke']
    if (len(gd['lights']) < 1 or gd['fine'] != {'water': 1, 'feed': 1, 'light': 1} or not gd['pure']
        or not (b['irrigation']['water'] == 0 and b['irrigation']['feed'] == gd['fine']['feed'] and b['irrigation']['light'] == gd['fine']['light'])
        or not (b['nutrient']['feed'] == 0 and b['nutrient']['water'] == gd['fine']['water']) or not (b['growlight']['light'] == 0 and b['growlight']['water'] == gd['fine']['water'])
        or not gd['same'] or not gd['forYou'] or not gd['claimedBy'] or gd['claimedBy'] == 'you' or not gd['arrived'] or not gd['after']
        or not gd['took'] or gd['mineWaiting'] != [True, False] or len(gd['landed']) != 1):
        fail('the garden')

    # 5k. reserved jobs and job notes (Pillar 4, for onboarding's first week; simNote a stand-in here if section 13's
    # isn't in): three slots on onboarding's cues; each a real machine with a panel, at your tier; not on the board
    # before it's due, then faulty and "asked for you"; the crew never take one and see none; yours never lapses; its
    # stops are fetch, make, job; one not taken is released at the end of your shift and the crew take it then.
    # Notes: take, a stop with its tag, done, turnin, all with the slot; an ordinary job you leave lapses with a note
    rs = g.ev("""(() => {
      const t0 = (SHIP_START.day - 1) * 1440 + SHIP_START.min, notes = [];
      const real = typeof simNote === 'function' ? simNote : null;
      window.__notes = notes; window.__sc("window.__sn0 = typeof simNote === 'function' ? simNote : undefined; simNote = (k, d) => { window.__notes.push([k, d]); if (window.__sn0) window.__sn0(k, d); }");
      JOBS_ON = true; MACH_HOUR = null; MACH_SEEN = -1; setShipNow(t0); machinesNow();
      for (const j of SHIP.jobs) if (j.claimedBy === 'you') { j.claimedBy = null; j.status = 'open'; }
      const a = jobReserve('lights', 1, 480, 1), b = jobReserve('washer', 1, 780, 2), c = jobReserve('lights', 2, 465, 3), a2 = jobReserve('lights', 1, 480, 1);
      const J = id => SHIP.jobs.find(j => j.id === id), out = { ids: [a, b, c], again: a === a2, looked: [1, 2, 3].map(jobReserved).join() === [a, b, c].join() };
      out.machines = [a, b, c].map(id => J(id).machine); out.makeMins = [a, b, c].map(id => J(id).makeMins); out.panels = out.machines.every(id => panelPlace(id)); out.tiers = [a, b, c].map(id => jobTier(J(id)));
      setShipNow(t0 + 60); machinesNow(); out.early = openJobs('you').some(x => x.id === a);
      setShipNow(t0 + 125); machinesNow();
      const oa = openJobs('you').find(x => x.id === a); out.onBoard = !!oa; out.asked = !!(oa && oa.asked); out.faulty = SHIP.machines[J(a).machine].state;
      out.crewSee = schedPeople().filter(jobCrew).some(p => openJobs(p).some(x => x.id === a));
      out.took = claimJob(a); out.stops = jobStops(J(a)).map(x => x.step).join(' ');
      // on (never backwards: that's a new game) to day 2 16:00: slot 2, never taken, is held to 17:00 on day 1, then the crew take it
      let crewBefore = false, crewAfter = null;
      for (let t = t0 + 150; t < t0 + 34 * 60; t += 30) {
        setShipNow(t); machinesNow(); const j = J(b);
        if (j && j.claimedBy && j.claimedBy !== 'you') { if (t < (t0 - 360) + 1020) crewBefore = true; else if (crewAfter === null) crewAfter = hhmm(t % 1440) + ' day ' + SHIP.time.day; }
        if (t === t0 + 150 + 14 * 60) out.kept = J(a).claimedBy === 'you';
      }
      jobStops(J(a)).forEach((x, k) => jobStepDone(a, k)); out.turned = turnInJob(a);
      out.crewBefore = crewBefore; out.crewAfter = crewAfter; out.released = jobRelease(3) === 1 && !heldForYou(J(c) || {});
      const mine = notes.filter(([k, d]) => k === 'job' && d.id === a).map(([k, d]) => d.step + (d.tag ? ':' + d.tag : '') + '/' + d.reserved);
      out.notes = mine.join(' ');
      // an ordinary job left for 12 hours lapses, with a note
      const o = openJobs('you').find(x => !x.asked); out.lapse = null;
      if (o) { claimJob(o.id); setShipNow(shipNow() + 13 * 60); machinesNow(); out.lapse = notes.some(([k, d]) => k === 'job' && d.id === o.id && d.step === 'lapse') && notes.some(([k, d]) => k === 'jobAbandoned' && d.id === o.id); }
      // for the social side: repairs (yours, with the state it was in, and the crew's), a job you drop, jobs left for you that went to the crew
      const o2 = openJobs('you')[0]; out.dropAb = o2 ? claimJob(o2.id) && dropJob(o2.id) && notes.some(([k, d]) => k === 'jobAbandoned' && d.id === o2.id) : null;
      const rep = notes.filter(([k]) => k === 'repair').map(([k, d]) => d);
      out.repairYou = rep.filter(d => d.who === 'you').map(d => d.machine + ':' + d.state).join(); out.repairCrew = rep.filter(d => d.who !== 'you').length;
      out.unclaimed = notes.filter(([k]) => k === 'jobUnclaimed').length; out.unclaimedOnce = new Set(notes.filter(([k]) => k === 'jobUnclaimed').map(([k, d]) => d.id)).size === out.unclaimed;
      out.badShape = notes.filter(([k, d]) => (k === 'repair' && !(d.who && d.machine && d.state)) || ((k === 'jobAbandoned' || k === 'jobUnclaimed') && !('machine' in d && 'dept' in d))).length;
      window.__sc("simNote = window.__sn0"); if (!window.__sn0) window.__sc("simNote = undefined");
      SHIP.jobs = SHIP.jobs.filter(j => !j.reserved); for (const j of SHIP.jobs) if (j.claimedBy === 'you') { j.claimedBy = null; j.status = 'open'; }
      setShipNow(t0);
      return out;
    })()""")
    print(f"Reserved jobs: {rs['ids']} on {rs['machines']} (tiers {rs['tiers']}, panels {rs['panels']}, make minutes {rs['makeMins']}); asking again {rs['again']}, looked up {rs['looked']}")
    print(f"  slot 1: early {rs['early']}, on the board {rs['onBoard']} asked {rs['asked']}, machine {rs['faulty']}, crew see it {rs['crewSee']}, took {rs['took']}, stops '{rs['stops']}', "
          f"kept past 14 h {rs['kept']}, turned in {rs['turned']}; notes '{rs['notes']}'")
    print(f"  slot 2 untaken: crew before 17:00 {rs['crewBefore']}, crew took it {rs['crewAfter']}; slot 3 released {rs['released']}; an ordinary job's lapse noted (job and jobAbandoned) {rs['lapse']}")
    print(f"  social notes: your repairs {rs['repairYou']}, the crew's {rs['repairCrew']}, a dropped job abandoned {rs['dropAb']}, jobUnclaimed {rs['unclaimed']} (once each {rs['unclaimedOnce']}), bad shape {rs['badShape']}")
    if (len(set(rs['ids'])) != 3 or not rs['again'] or not rs['looked'] or not rs['panels'] or max(rs['tiers']) > 1 or rs['machines'][0] == rs['machines'][1]
        or rs['early'] or not rs['onBoard'] or not rs['asked'] or rs['faulty'] not in ('faulty', 'failing') or rs['crewSee'] or not rs['took']
        or rs['stops'] != 'fetch make job' or rs['makeMins'] != [30, 30, 30] or not rs['kept'] or not rs['turned'] or rs['crewBefore'] or not rs['crewAfter'] or not rs['released'] or rs['lapse'] is False or rs['dropAb'] is False or not rs['repairYou'].endswith(':faulty') or rs['repairCrew'] < 1 or rs['unclaimed'] < 1 or not rs['unclaimedOnce'] or rs['badShape']
        or not all(x in rs['notes'].split() for x in ['take/1', 'stop:fetch/1', 'stop:make/1', 'stop:job/1', 'done/1', 'turnin/1'])):
        fail('reserved jobs and job notes')

    # 5l. the Works crew at work (0.33.40, the plan for 0.60.7): a fresh ship's first two days have the two crew jobs placed
    # for you to see (SHOW_JOBS: the vent by Deck 4's lift on Day 1's morning, a delivery into the Works bay on Day 2 after
    # lunch), each taken by the named junior or another of the crew, standing at its place, the delivery's box carried
    # from the pickup to the drop and showJob(day) saying so; through a week about every third small job goes to the crew
    # at once (j.shared), never while fewer than SHARE_KEEP others are held for you, and none of those is ever held
    if g.ev("typeof SHOW_JOBS === 'undefined'"):
        print("Works crew at work: not in this build (skipped)")
    else:
        cw = g.ev("""(() => {
          const t0 = (SHIP_START.day - 1) * 1440 + SHIP_START.min;
          JOBS_ON = true; MACH_HOUR = null; MACH_SEEN = -1; setShipNow(t0); machinesNow();
          const out = { show: {}, shared: 0, small: 0, keptLow: [], heldShared: [] };
          for (let t = t0; t < t0 + 7 * 1440; t += 60) {
            setShipNow(t); machinesNow();
            for (const j of SHIP.jobs) if (j.shareSeen && !j.__seen) { j.__seen = true; out.small++; if (!j.shared) continue; out.shared++; if (j.shared < SHARE_KEEP) out.keptLow.push(j.id); if (t < leaveEnd(j)) out.heldShared.push(j.id); }
            for (const d of [1, 2]) if (!out.show[d]) { const s = showJob(d); if (s) { const j = SHIP.jobs.find(x => x.id === s.id); out.show[d] = { who: s.who, place: s.place, deck: s.deck, carry: (j.segs || []).some(sg => sg.hold === 'carry'), dropCarry: (j.segs || []).some(sg => sg.tag === 'drop' && sg.hold === 'carry'), stand: (j.segs || []).some(sg => sg.placeId === s.place && sg.tag !== 'pickup') }; } }
          }
          out.keptLow = out.keptLow.slice(0, 4); out.heldShared = out.heldShared.slice(0, 4);
          setShipNow(t0);
          return out;
        })()""")
        s1, s2 = cw['show'].get('1') or {}, cw['show'].get('2') or {}
        print(f"Works crew at work: Day 1 {s1}, Day 2 {s2}; shared at once {cw['shared']} of {cw['small']} small jobs in the week, "
              f"with fewer than {g.ev('SHARE_KEEP')} others held {cw['keptLow']}, a shared one held for you {cw['heldShared']}")
        if (not s1 or s1['place'] != '4-lift-1' or not s1['stand'] or not s2 or not s2['place'] or s2['deck'] != 5 or not s2['carry'] or not s2['dropCarry']
                or cw['shared'] < 1 or cw['shared'] > cw['small'] * .6 or cw['keptLow'] or cw['heldShared']):
            fail('the Works crew at work')

    # 5m. the shelves and the Wednesday delivery (0.33.41-0.33.42, the plan for 0.60.7): every part has its own shelf,
    # a job's fetch stop starts at it, shelfNeed/shelfWrong send you to it (any other shelf: wrong, nothing taken), the
    # machine shop tops up what it can at 15:00; the delivery is never late in the first week, lands as crates at
    # Wednesday 10:00, waits for you till 14:00 (the crew don't touch it), your cart pulls in up to CART_CRATES and a shelf
    # unloads them (a second trip when there are more), and one left alone goes to the crew at 14:00 and gets done
    if g.ev("typeof shelfOf === 'undefined' || typeof holdCrates === 'undefined'"):
        print("Shelves and the delivery: not in this build (skipped)")
    else:
        sd = g.ev("""(() => {
          if (typeof SHARE_ON !== 'undefined') SHARE_ON = false;
          const t0 = (SHIP_START.day - 1) * 1440 + SHIP_START.min, out = {};
          JOBS_ON = true; MACH_HOUR = null; MACH_SEEN = -1; setShipNow(t0); machinesNow();
          out.noShelf = Object.keys(STOCK).filter(k => !shelfOf(k) || !shelfStock(shelfOf(k)).some(x => x.part === k));
          out.lineOk = Object.keys(SHELF_NAME).every(id => /^[a-zA-Z ]+ \\d+ of \\d+/.test(shelfLine(id)));
          // a machine job: its fetch stop starts at its part's shelf; the shelves send you there
          const m = machineList().find(x => !x.stub && panelPlace(x.id) && jobTier({ machine: x.id }) <= PLAYER_TIER && !ENGINE_KINDS.has(x.kind) && shelfOf(MACHINE_KINDS[x.kind].part) !== '5-parts-1');
          const s = SHIP.machines[m.id]; s.cond = 40; s.state = machineState(40); setShipNow(t0 + 120); machinesNow();
          const j = SHIP.jobs.find(x => x.machine === m.id && x.status !== 'done'), part = MACHINE_KINDS[m.kind].part, want = shelfOf(part);
          out.claimed = !!j && !j.claimedBy && claimJob(j.id);
          out.stopFirst = j && jobStops(j)[0].places[0] === want;
          out.need = shelfNeed() === part && shelfWant() === want;
          const was = SHIP.stores[part];
          out.wrong = shelfWrong({ t: 'Lights' }) === true && SHIP.stores[part] === was;
          out.right = shelfWrong({ t: SHELF_NAME[want] }) === false;
          if (j) dropJob(j.id);
          out.noNeed = shelfNeed() === null;
          // the machine shop: a part it can make, run down, is one up after 15:00; one it can't stays
          const mk = Object.keys(STOCK).find(k => !NO_MAKE.has(k)), nm = [...NO_MAKE][0];
          setShipNow(t0 + 8 * 60 + 1); machinesNow(); SHIP.stores[mk] = 0; SHIP.stores[nm] = 0; MACH_REV++;
          setShipNow(t0 + 9 * 60 + 30); machinesNow(); out.shop = [SHIP.stores[mk], SHIP.stores[nm]];
          // the first week's delivery: Day 3, 10:00, crates, held for you till 14:00
          out.lateWeek1 = [1, 2, 3, 4, 5, 6, 7].some(d => deliveryLate(d));
          setShipNow(2 * 1440 + 10 * 60 + 5); machinesNow();
          const dj = SHIP.jobs.find(x => x.cargo === 'stores' && x.status !== 'done');
          out.crates = (typeof partsCrates === 'function' ? partsCrates() : holdCrates()); out.dj = !!dj && Math.floor(dj.found / 1440) + 1 === 3 && dj.found % 1440 === 600;
          out.title = dj && jobCard(dj)[0]; out.keep = dj && leaveEnd(dj) % 1440 === DELIVERY_KEEP;
          setShipNow(2 * 1440 + 13 * 60 + 30); machinesNow(); out.crewBefore = !!dj.claimedBy;
          // two trips: more than a cart's worth in the hold
          SHIP.hold.seal = (SHIP.hold.seal || 0) + 20; MACH_REV++; const crates = (typeof partsCrates === 'function' ? partsCrates() : holdCrates());
          out.took = claimJob(dj.id);
          const l1 = cartLoadHold(dj.id), u1 = cartUnloadShelves(dj.id), l2 = cartLoadHold(dj.id), u2 = cartUnloadShelves(dj.id);
          out.trips = [crates, l1, u1.left, l2, u2.left]; out.emptied = (typeof partsCrates === 'function' ? partsCrates() : holdCrates()) === 0 && !Object.keys(SHIP.hold).some(k => k !== 'meals' && SHIP.hold[k] > 0);
          out.fin = finishJob(dj.id); if (typeof turnInJob === 'function') turnInJob(dj.id);
          // the next week's, left alone: the crew take it at 14:00 and it's done by the evening
          setShipNow(9 * 1440 + 10 * 60 + 5); machinesNow();
          const k = SHIP.jobs.find(x => x.cargo === 'stores' && x.status !== 'done');
          if (k) { setShipNow(9 * 1440 + 13 * 60 + 55); machinesNow(); out.k0 = !!k.claimedBy; setShipNow(9 * 1440 + 14 * 60 + 5); machinesNow(); out.k1 = k.claimedBy; out.cartRun = !!(k.segs || []).some(sg => sg.hold === 'cartfull');
                   setShipNow(9 * 1440 + 20 * 60); machinesNow(); out.k2 = k.status === 'done' && (typeof partsCrates === 'function' ? partsCrates() : holdCrates()) === 0; }
          if (typeof SHARE_ON !== 'undefined') SHARE_ON = true;
          setShipNow(t0);
          return out;
        })()""")
        print(f"Shelves and the delivery: {sd}")
        if (sd['noShelf'] or not sd['lineOk'] or not sd['claimed'] or not sd['stopFirst'] or not sd['need'] or not sd['wrong'] or not sd['right'] or not sd['noNeed']
                or sd['shop'] != [1, 0] or sd['lateWeek1'] or not sd['crates'] or not sd['dj'] or sd['title'] != 'Unload the Wednesday delivery' or not sd['keep'] or sd['crewBefore']
                or not sd['took'] or sd['trips'][1] != g.ev('CART_CRATES') or sd['trips'][2] < 1 or sd['trips'][4] != 0 or not sd['emptied'] or not sd['fin']
                or sd.get('k0') is not False or not sd.get('k1') or not sd.get('cartRun') or not sd.get('k2')):
            fail('the shelves and the Wednesday delivery')

    # 5n. ranks and the ladder's hook (Pillar 5 foundation 17.1, 17.2, 17.6; 0.33.45): playerTier() and playerRank() from
    # section 24's SHIP.works (1 and junior without it); a job kept for seniors is never taken by a junior crew member or by
    # you, and a senior takes it; a junior job is held for you while you're a junior, and after a promotion isn't held but is
    # still yours to take; a reserved test job on a tier-2 machine (o.tier, o.train) is yours while it's held; ladderTick(h)
    # runs once each ship hour, after the claims, and may reserve a job from there
    if g.ev("typeof rankOk === 'function'"):
        rk = g.ev("""(() => {
          const t0 = (SHIP_START.day - 1) * 1440 + SHIP_START.min, out = {};
          JOBS_ON = true; MACH_HOUR = null; MACH_SEEN = -1; SHIP.works = null; setShipNow(t0 + 180); machinesNow();
          for (const j of SHIP.jobs) if (j.claimedBy === 'you') { j.claimedBy = null; j.status = 'open'; }
          out.tier = playerTier(); out.rank = playerRank();
          const crew = schedPeople().filter(jobCrew), rc = {}; for (const p of crew) rc[crewRank(p)] = (rc[crewRank(p)] || 0) + 1; out.ranks = rc;
          const t = shipNow(), mk = (id, o) => { const j = { id, machine: null, deck: 4, room: (placeById('4-lift-1') || {}).room, kind: 'chore', chore: 'vent', target: id, title: 'Clean a vent: test', tier: 1,
            stops: [{ deck: 4, placeId: '4-lift-1', mins: 10, tag: 'vent' }], urgency: 0, leave: null, posted: t, found: t, claimedBy: null, parts: [], status: 'open', ...o }; SHIP.jobs.push(j); MACH_REV++; return j; };
          const sen = mk('test-senior', { only: 'senior', released: true, shareSeen: true }), jun = mk('test-junior', { junior: true, shareSeen: true });
          out.youSenior = openJobs('you').some(x => x.id === sen.id); out.claimSenior = claimJob(sen.id);
          out.juniorFor = forYou(jun); out.juniorOpen = openJobs('you').some(x => x.id === jun.id);
          SHIP.works = { tier: 1, rank: 'officer' }; out.rankOfficer = playerRank(); out.juniorForOfficer = forYou(jun); out.juniorOpenOfficer = openJobs('you').some(x => x.id === jun.id);
          SHIP.works = { tier: 2, rank: 'junior' }; out.tier2 = playerTier(); SHIP.works = null;
          // the ladder's hook: once an hour, after the claims; a reserve from inside it (slot 20, a tier-2 machine)
          const calls = []; let rid = null;
          window.__lt = h => { calls.push(h); if (rid === null && h === Math.floor(t / 60) + 2) rid = jobReserve('scrubber', SHIP.time.day, (h % 24) * 60 + 30, 20, { tier: 2, train: 't2', until: SHIP.time.day * 1440 + 1440 }) || 'none'; };
          window.__sc("window.__lt0 = typeof ladderTick === 'function' ? ladderTick : undefined; ladderTick = h => { window.__lt(h); if (window.__lt0) window.__lt0(h); }");   // section 24's own, if it's in, still runs
          let who = null;
          for (let m = t + 60; m <= t + 8 * 60; m += 60) { setShipNow(m); machinesNow(); if (sen.claimedBy && !who) who = sen.claimedBy; }
          window.__sc("if (window.__lt0) ladderTick = window.__lt0; else ladderTick = undefined");
          out.calls = calls.length; out.callsSeq = calls.every((h, i) => !i || h === calls[i - 1] + 1);
          out.seniorBy = who ? crewRank(schedPeople().find(p => p.id === who)) : null;
          const R = SHIP.jobs.find(j => j.id === rid); out.rid = rid; out.rTier = R ? jobTier(R) : null; out.rTrain = R ? R.train : null; out.rHeld = R ? heldForYou(R) : null;
          for (const j of SHIP.jobs) if (j.claimedBy === 'you' && j.status === 'claimed') { j.claimedBy = null; j.status = 'open'; }
          out.rClaim = R ? claimJob(R.id) : null; out.rOpen = R ? true : null;
          SHIP.jobs = SHIP.jobs.filter(j => !j.reserved && !j.id.startsWith('test-')); for (const j of SHIP.jobs) if (j.claimedBy === 'you') { j.claimedBy = null; j.status = 'open'; }
          setShipNow(t0);
          return out;
        })()""")
        print(f"Ranks (0.33.45): tier {rk['tier']} rank {rk['rank']} (with SHIP.works tier 2: {rk['tier2']}, rank officer: {rk['rankOfficer']}); Works crew by rank {rk['ranks']}")
        print(f"  senior-only: on your board {rk['youSenior']}, you claimed {rk['claimSenior']}, taken by a {rk['seniorBy']}; junior job held for you {rk['juniorFor']} (on the board {rk['juniorOpen']}), as an officer held {rk['juniorForOfficer']} on the board {rk['juniorOpenOfficer']}")
        print(f"  ladderTick: {rk['calls']} calls in 8 h, hour by hour {rk['callsSeq']}; its reserve {rk['rid']}: tier {rk['rTier']}, train {rk['rTrain']}, held {rk['rHeld']}, you claimed it {rk['rClaim']}")
        if (rk['tier'] != 1 or rk['rank'] != 'junior' or rk['tier2'] != 2 or rk['rankOfficer'] != 'officer' or rk['youSenior'] or rk['claimSenior']
            or rk['seniorBy'] not in ('senior', 'specialist') or not rk['juniorFor'] or not rk['juniorOpen'] or rk['juniorForOfficer'] or not rk['juniorOpenOfficer']
            or rk['calls'] != 8 or not rk['callsSeq'] or not rk['rid'] or rk['rid'] == 'none' or rk['rTier'] != 2 or rk['rTrain'] != 't2' or not rk['rHeld'] or not rk['rClaim']):
            fail('ranks and the ladder hook')

    # 5o. more real faults and their causes (Pillar 5 foundation 17.3-17.4; plans/mechanics/fault-tables.html; 0.33.46):
    # every Tier 1 kind has a table, every part is in STOCK, no two causes of a kind share both card and sign; the pick is
    # the same twice, never a load, a setting only from Day 4, and over many hours every allowed cause comes up, the
    # commonest most. Then the real crew with a scripted steady player (from Day 2, on each shift hour with nothing in
    # hand, takes the top job on the board and finishes it in its minutes): of the machine jobs you do, 40-60% are
    # repairs, 3-6 jobs a shift day, ship health 85+, nothing broken, every repair from Day 2 has a cause, and Days 0-1
    # have none
    if g.ev("typeof FAULT_CAUSES === 'object'"):
        fc = g.ev("""(() => {
          const out = { missing: [], badPart: [], dup: [], dist: {}, noShow: [], order: [], loadPicked: 0, earlyDrift: 0 };
          const T1 = ['oven', 'range', 'galleyplant', 'extractor', 'chiller', 'washer', 'lift', 'lights', 'cartdock', 'growlight'];
          for (const k of T1) if (!FAULT_CAUSES[k]) out.missing.push(k);
          for (const k in FAULT_CAUSES) { const seen = new Set();
            for (const c of FAULT_CAUSES[k]) { if (c.part && !(c.part in STOCK)) out.badPart.push(k + '.' + c.id); const key = c.shows + '/' + c.sign; if (seen.has(key)) out.dup.push(k + '.' + c.id); seen.add(key); } }
          // the pick, for one machine of each kind with a table, over 40 days of hours
          for (const k in FAULT_CAUSES) {
            const m = machineList().find(x => x.kind === k); if (!m) continue;
            const n = {}; for (let h = 24; h < 24 * 41; h++) { const c = faultPick(m, h), c2 = faultPick(m, h); if (c !== c2) out.same = false; if (!c) continue;
              if (c.load) out.loadPicked++; if (c.setting && Math.floor(h / 24) + 1 < 4) out.earlyDrift++; n[c.id] = (n[c.id] || 0) + 1; }
            out.dist[k] = n;
            const allowed = FAULT_CAUSES[k].filter(c => !c.load && !c.band);
            for (const c of allowed) if (!n[c.id]) out.noShow.push(k + '.' + c.id);
            const top = allowed.filter(c => c.w === Math.max(...allowed.map(x => x.w))).map(c => c.id), most = Object.entries(n).sort((a, b) => b[1] - a[1])[0];
            if (most && !top.includes(most[0])) out.order.push(k + ': ' + most[0]);
          }
          if (out.same === undefined) out.same = true;
          return out;
        })()""")
        print(f"Fault tables (0.33.46): {len(fc['dist'])} kinds; missing Tier 1 {fc['missing']}, parts not in STOCK {fc['badPart']}, card and sign shared {fc['dup']}")
        print(f"  the pick: the same twice {fc['same']}, loads picked {fc['loadPicked']}, settings before Day 4 {fc['earlyDrift']}, causes never picked {fc['noShow']}, commonest not the most often {fc['order']}")
        print('  ' + '; '.join(k + ' ' + ' '.join(f"{c}:{n}" for c, n in v.items()) for k, v in fc['dist'].items()))
        if fc['missing'] or fc['badPart'] or fc['dup'] or not fc['same'] or fc['loadPicked'] or fc['earlyDrift'] or fc['noShow'] or fc['order']:
            fail('the fault tables')
        STEADY = r"""(() => {
          window.__sc("window.__evSt = [typeof eventNow === 'function' ? eventNow : undefined, typeof eventMod === 'function' ? eventMod : undefined]; if (window.__evSt[0]) eventNow = () => null; if (window.__evSt[1]) eventMod = () => null");
          const t0 = (SHIP_START.day - 1) * 1440 + SHIP_START.min, end = t0 + DAYS * 1440, out = { days: {}, minHealth: 100, worst: 0, noCause: [], early: [], causes: {}, held: 0 };
          JOBS_ON = true; MACH_HOUR = null; MACH_SEEN = -1; SHIP.works = null; setShipNow(t0); machinesNow();
          let mine = null, until = 0; const seen = new Map();
          for (let t = t0; t <= end; t += 30) {
            setShipNow(t); machinesNow();
            out.minHealth = Math.min(out.minHealth, shipHealth());
            for (const m of machineList()) out.worst = Math.max(out.worst, MACHINE_STATES.indexOf(SHIP.machines[m.id].state));
            for (const j of SHIP.jobs) seen.set(j.id, j);
            if (mine && t >= until) { const j = SHIP.jobs.find(x => x.id === mine); if (j && j.claimedBy === 'you' && j.status === 'claimed') { jobStops(j).forEach((x, k) => jobStepDone(j.id, k)); finishJob(j.id); } mine = null; }
            const d = SHIP.time.day, md = t % 1440;
            if (!mine && d >= 2 && playerShiftOn(d) && md >= DAY_SHIFT[0] && md < DAY_SHIFT[1]) {
              const o = openJobs('you')[0];
              if (o && claimJob(o.id)) { mine = o.id; until = t + Math.max(30, o.mins + 20); const D = out.days[d] || (out.days[d] = { all: 0, machine: 0, repair: 0, service: 0 }); D.all++;
                const j = SHIP.jobs.find(x => x.id === o.id); if (['service', 'repair', 'overhaul'].includes(j.kind)) { D.machine++; D[j.kind === 'service' ? 'service' : 'repair']++; } }
            }
          }
          for (const j of seen.values()) if (j.machine && (j.kind === 'repair' || j.kind === 'overhaul') && !j.reserved) {
            const d = Math.floor(j.posted / 1440) + 1, k = machineById(j.machine).kind;
            if (d < 2 && j.cause) out.early.push(j.id);
            if (d >= 2 && FAULT_CAUSES[k] && !j.cause) out.noCause.push(j.id);
            if (j.cause) out.causes[k + '.' + j.cause] = (out.causes[k + '.' + j.cause] || 0) + 1;
          }
          out.sig = JSON.stringify([...seen.values()].filter(j => j.cause).map(j => j.id + ':' + j.cause).sort());
          for (const j of SHIP.jobs) if (j.claimedBy === 'you') { j.claimedBy = null; j.status = 'open'; }
          window.__sc("if (window.__evSt[0]) eventNow = window.__evSt[0]; if (window.__evSt[1]) eventMod = window.__evSt[1]");
          setShipNow(t0);
          return out;
        })()""".replace('DAYS', str(DAYS))
        st = g.ev(STEADY); st2 = g.ev(STEADY)
        days = sorted(st['days'].items(), key=lambda kv: int(kv[0]))
        mach = sum(v['machine'] for k, v in days); rep = sum(v['repair'] for k, v in days); alln = sum(v['all'] for k, v in days)
        share = 100 * rep / mach if mach else 0; per = alln / len(days) if days else 0
        print(f"  a steady player, Days 2-{DAYS}: {alln} jobs on {len(days)} shift days ({per:.1f} a day), machine jobs {mach}, repairs {rep} ({share:.0f}%)")
        print('    by day (all/machine/repairs): ' + ' '.join(f"{k}:{v['all']}/{v['machine']}/{v['repair']}" for k, v in days))
        print(f"    lowest ship health {st['minHealth']:.1f}, worst state {MSTATES[st['worst']] if 'MSTATES' in dir() else st['worst']}, repairs from Day 2 without a cause {st['noCause'][:4]}, causes on Days 0-1 {st['early'][:4]}, the same twice {st['sig'] == st2['sig']}")
        print('    causes seen: ' + ' '.join(f"{k}:{v}" for k, v in sorted(st['causes'].items())))
        if not (40 <= share <= 60): fail(f"repairs are {share:.0f}% of the machine jobs a steady player does (want 40-60%)")
        if not (3 <= per <= 6): fail(f"a steady player does {per:.1f} jobs a shift day (want 3-6)")
        if st['minHealth'] < 85 or st['worst'] >= 4: fail('ship health or a broken machine with the steady player')
        if st['sig'] != st2['sig']: print('    first run only', sorted(set(json.loads(st['sig'])) - set(json.loads(st2['sig'])))[:6], 'second only', sorted(set(json.loads(st2['sig'])) - set(json.loads(st['sig'])))[:6])
        if st['noCause'] or st['early'] or st['sig'] != st2['sig']: fail('causes missing, early or not the same twice')

    # 5p. job kinds with steps (Pillar 5 foundation 17.5; 0.33.47) and machineFound (for m1-rounds): a test kind
    # registered with jobKindAdd posts its own job each hour it wants; one you don't take the crew do (crew.can, crew.mins,
    # its stops as segments) and its done runs with their id; one you take shows its stops' steps (how, opts) and every
    # other job's stops say 'hold'; jobStepDone keeps each step's result for done ('you'); a built-in kind can't be
    # registered over; the save keeps a registered job (with its results) and drops one whose kind isn't in the build.
    # machineFound: a worn machine's unseen job is found now (fresh, j.foundBy, simNote('found')); again, not fresh; healthy: null
    if g.ev("typeof jobKindAdd === 'function'"):
        jk = g.ev("""(() => {
          const t0 = (SHIP_START.day - 1) * 1440 + SHIP_START.min, out = {}, done = [], steps = [], notes = [];
          JOBS_ON = true; MACH_HOUR = null; MACH_SEEN = -1; SHIP.works = null; setShipNow(t0 + 1440 + 180); machinesNow();
          for (const j of SHIP.jobs) if (j.claimedBy === 'you') { j.claimedBy = null; j.status = 'open'; }
          const H0 = Math.floor(shipNow() / 60) + 1, room = (placeById('4-lift-1') || {}).room;
          out.overBuiltIn = jobKindAdd('repair', { stops: () => [], done: () => {} });
          out.added = jobKindAdd('testkind', { tier: 1, work: 20, text: 'Test run',
            stops: j => [{ deck: 4, placeId: '4-lift-1', mins: 10, tag: 'look', how: 'look', hold: 'cart', opts: { marks: ['fine', 'worn'] } }, { deck: 4, placeId: '4-laundry-1', mins: 10, tag: 'pick', how: 'choose', opts: { options: ['a', 'b'] } }],
            post: (h, jobs) => { if ((h === H0 || h === H0 + 1) && !jobs.some(x => x.id === 'tk@' + h)) jobs.push(jobMake('testkind', { h, id: 'tk@' + h, deck: 4, room, title: 'Test run: Deck 4', ...(h === H0 ? { released: true } : { shareSeen: true, leave: 480 }) })); },   // B: its own hold (outside HOLD_MAX and the band's order)
            done: (j, t, by) => done.push([j.id, by, JSON.stringify(j.res || {})]), stepDone: (j, k, res) => steps.push([j.id, k, res && res.pick]),
            crew: { can: p => jobCrew(p) === 'works', mins: 30 } });
          let crewJob = null;
          const m0 = shipNow(); for (let m = m0 + 60; m <= m0 + 4 * 60; m += 60) { setShipNow(m); machinesNow(); }
          const A = SHIP.jobs.find(j => j.id === 'tk@' + H0), B = SHIP.jobs.find(j => j.id === 'tk@' + (H0 + 1));
          out.posted = [!!A, !!B]; out.aBy = A && A.claimedBy; out.aSegs = A && A.segs ? A.segs.filter(x => x.type === 'job').map(x => x.tag + '@' + x.placeId).join(' ') : null;
          out.aHold = A && A.segs ? A.segs.filter(x => x.hold).map(x => x.tag + ':' + x.hold).join(' ') : null;
          out.aMins = A && A.segs ? A.segs.filter(x => x.type === 'job').reduce((a, x) => a + x.to - x.from, 0) : null;
          out.aDone = done.filter(d => d[0] === (A && A.id)).map(d => d[1] === A.claimedBy).join();
          out.bHeld = B && !B.claimedBy; out.card = B ? jobCard(B).join(' / ') : null; out.open = B ? openJobs('you').some(x => x.id === B.id) : null;
          out.claim = B ? claimJob(B.id) : null;
          out.stops = B ? jobStops(B).map(x => x.step + ':' + x.how + (x.opts ? '+opts' : '')).join(' ') : null;
          const other = SHIP.jobs.find(j => j.kind === 'chore' || j.kind === 'service' || j.kind === 'repair'); out.otherHow = other ? [...new Set(jobStops(other).map(x => x.how))].join() : null;
          if (B) { jobStepDone(B.id, 0, { pick: 'worn' }); const r = jobStepDone(B.id, 1, { pick: 'b' }); out.workDone = r.done; out.res = JSON.stringify(B.res); out.youDone = done.filter(d => d[0] === B.id).map(d => d[1] + ' ' + d[2]).join(); out.steps = steps.filter(x => x[0] === B.id).map(x => x[1] + ':' + x[2]).join(' '); }
          // the save: a registered job (with its results) stays; one of an unknown kind goes
          const s = { player: { deck: 4, tile: [0, 0], facing: 0 }, ship: { decks: {} }, crew: {} }; SAVE_EXTRA.forEach(f => f(s));
          s.ship.jobs.push({ id: 'gone@1', machine: null, deck: 4, kind: 'nosuchkind', urgency: 0, posted: 0, found: 0, claimedBy: null, parts: [], status: 'open' });
          const back = JSON.parse(JSON.stringify(s)); MACH_HOUR = null; machinesLoad(back); machinesNow();
          const B2 = SHIP.jobs.find(j => B && j.id === B.id); out.saveKeeps = !!B2 && JSON.stringify(B2.res) === out.res; out.saveDrops = !SHIP.jobs.some(j => j.id === 'gone@1');
          if (B2) finishJob(B2.id);
          delete JOB_KINDS.testkind; delete JOB_TYPES.testkind; SHIP.jobs = SHIP.jobs.filter(j => j.kind !== 'testkind');
          // machineFound
          window.__fn = notes; window.__sc("window.__sn1 = typeof simNote === 'function' ? simNote : undefined; simNote = (k, d) => { if (k === 'found') window.__fn.push(d); if (window.__sn1) window.__sn1(k, d); }");
          const mm = machineList().find(m => !m.stub && !ENGINE_KINDS.has(m.kind) && SHIP.machines[m.id].state === 'healthy' && !SHIP.jobs.some(j => j.machine === m.id && j.status !== 'done'));
          out.healthy = machineFound(mm.id);
          SHIP.machines[mm.id].cond = 60; SHIP.machines[mm.id].state = machineState(60); setShipNow(shipNow() + 60); machinesNow();
          const jw = SHIP.jobs.find(j => j.machine === mm.id && j.status !== 'done'); if (jw) jw.found = shipNow() + 600;   // not yet seen
          const f1 = machineFound(mm.id), f2 = machineFound(mm.id), jf = SHIP.jobs.find(j => j.id === (f1 && f1.id));
          out.found = [f1 && f1.fresh, f2 && f2.fresh, jf && jf.found <= shipNow(), jf && jf.foundBy, notes.length, notes[0] && notes[0].machine === mm.id && notes[0].by === 'you'];
          window.__sc("simNote = window.__sn1"); if (!window.__sn1) window.__sc("simNote = undefined");
          for (const j of SHIP.jobs) if (j.claimedBy === 'you') { j.claimedBy = null; j.status = 'open'; }
          setShipNow(t0);
          return out;
        })()""")
        print(f"Job kinds (0.33.47): registered {jk['added']} (over a built-in {jk['overBuiltIn']}), posted {jk['posted']}; untaken: {jk['aBy']} at {jk['aSegs']} ({jk['aMins']} min, held {jk['aHold']}), done by them {jk['aDone']}")
        print(f"  yours: held {jk['bHeld']}, card '{jk['card']}', on your board {jk['open']}, claimed {jk['claim']}, stops '{jk['stops']}', other jobs' steps {jk['otherHow']}; done {jk['workDone']}, results {jk['res']}, done for you '{jk['youDone']}', stepDone '{jk['steps']}'")
        print(f"  save keeps it {jk['saveKeeps']}, drops an unknown kind {jk['saveDrops']}; machineFound: healthy {jk['healthy']}, [fresh, again, found now, by, notes, note ok] {jk['found']}")
        if (not jk['added'] or jk['overBuiltIn'] or jk['posted'] != [True, True] or not jk['aBy'] or jk['aBy'] == 'you' or not jk['aSegs'] or '4-lift-1' not in (jk['aSegs'] or '') or jk['aMins'] != 30 or jk['aDone'] != 'true' or 'look:cart' not in (jk['aHold'] or '') or 'pick:' in (jk['aHold'] or '')
            or not jk['bHeld'] or not jk['open'] or not jk['claim'] or jk['stops'] != 'look:look+opts pick:choose+opts' or jk['otherHow'] != 'hold' or not jk['workDone']
            or jk['res'] != '{"0":{"pick":"worn"},"1":{"pick":"b"}}' or not jk['youDone'].startswith('you {') or jk['steps'] != '0:worn 1:b' or not jk['saveKeeps'] or not jk['saveDrops']
            or jk['healthy'] is not None or jk['found'] != [True, False, True, 'you', 1, True]):
            fail('job kinds with steps, or machineFound')

    # 5q. hooks for 24k and M1 (0.33.47): caseOffer is called for each posted fault with a cause; caseHeld keeps a job from the
    # crew; caseFitted turns your last stop into a wrong fix (not done, the machine not put right); a side kind (def.side) is
    # taken beside your board job and isn't myJob; an old save's main lift '5-lift-1' loads as '5-mainlift-1' with its wear
    if g.ev("typeof jobSide === 'function'"):
        hk = g.ev("""(() => {
          const t0 = (SHIP_START.day - 1) * 1440 + SHIP_START.min, out = {}, offered = [];
          JOBS_ON = true; MACH_HOUR = null; MACH_SEEN = -1; SHIP.works = null; setShipNow(t0); machinesNow();
          for (const j of SHIP.jobs) if (j.claimedBy === 'you') { j.claimedBy = null; j.status = 'open'; }
          // stand-ins swapped in through the game's scope (24k's own, if it's in, is kept and put back after)
          const swap = (name, fn) => { window['__f_' + name] = fn; window.__sc("window.__o_" + name + " = typeof " + name + " === 'function' ? " + name + " : undefined; " + name + " = (...a) => window.__f_" + name + "(...a)"); };
          const unswap = name => window.__sc("if (window.__o_" + name + ") " + name + " = window.__o_" + name + "; else " + name + " = undefined");
          swap('caseOffer', (j, h) => offered.push([j.id, j.cause, h]));
          let held = null; swap('caseHeld', j => j.id === held); swap('caseHidden', () => false);
          setShipNow(t0 + 5 * 1440); machinesNow();
          out.offered = offered.length; out.offeredOk = offered.every(o => o[1] && SHIP.jobs.concat([]).length >= 0);
          unswap('caseOffer');
          const tt = shipNow(), mk = id => { const j = { id, machine: null, deck: 4, room: (placeById('4-lift-1') || {}).room, kind: 'chore', chore: 'vent', target: id, title: 'Clean a vent: test', tier: 1,
            stops: [{ deck: 4, placeId: '4-lift-1', mins: 10, tag: 'vent' }], urgency: 0, leave: null, posted: tt, found: tt, claimedBy: null, parts: [], status: 'open', shareSeen: true }; SHIP.jobs.push(j); MACH_REV++; return j; };
          held = mk('test-case').id; const J = SHIP.jobs.find(j => j.id === held);
          if (J) { J.released = true; J.urgency = 1; }
          setShipNow(shipNow() + 3 * 60); machinesNow(); out.crewTook = J ? !!(J.claimedBy && J.claimedBy !== 'you') : null;
          out.claim = J ? claimJob(J.id) : null;
          swap('caseFitted', j => j.id === held);
          const n = J ? jobStops(J).length : 0, mid = J && J.machine ? SHIP.machines[J.machine].cond : null; let r = null;
          for (let k = 0; k < n; k++) r = jobStepDone(J.id, k);
          out.wrong = r && r.wrong === true && r.done === false && !J.workDone; out.condSame = J && J.machine ? SHIP.machines[J.machine].cond <= mid + 1e-9 : true;
          unswap('caseFitted'); unswap('caseHeld'); unswap('caseHidden'); if (J) dropJob(J.id);
          // a side kind
          jobKindAdd('testside', { side: true, text: 'Side test', stops: () => [{ deck: 4, placeId: '4-lift-1', mins: 5, tag: 'hold' }], done: () => {}, crew: { can: () => false, mins: 5 } });
          const b = mk('test-board'); out.board = claimJob(b.id);
          SHIP.jobs.push(jobMake('testside', { id: 'side@1', deck: 4, title: 'Side test' })); MACH_REV++;
          out.side = claimJob('side@1'); out.myJob = myJob() && myJob().id === (b && b.id); out.sides = mySideJobs().filter(j => j.kind === 'testside').map(j => j.id).join();   // only the test's (24c's drill may be yours too)
          delete JOB_KINDS.testside; delete JOB_TYPES.testside; SHIP.jobs = SHIP.jobs.filter(j => j.id !== 'side@1' && !j.id.startsWith('test-'));
          for (const j of SHIP.jobs) if (j.claimedBy === 'you') { j.claimedBy = null; j.status = 'open'; }
          // the lift's old id in a save
          const sv = { player: { deck: 4, tile: [0, 0], facing: 0 }, ship: { decks: {} }, crew: {} }; SAVE_EXTRA.forEach(f => f(sv));
          const lift = sv.ship.machines['5-mainlift-1']; out.hadNew = !!lift;
          if (lift) { sv.ship.machines['5-lift-1'] = [33.5, lift[1]]; delete sv.ship.machines['5-mainlift-1']; }
          MACH_HOUR = null; machinesLoad(JSON.parse(JSON.stringify(sv))); out.liftCond = SHIP.machines['5-mainlift-1'] && SHIP.machines['5-mainlift-1'].cond; out.noOld = !SHIP.machines['5-lift-1'];
          setShipNow(t0);
          return out;
        })()""")
        print(f"Hooks for 24k and M1 (0.33.47): caseOffer {hk['offered']} faults; a held case job: crew took it {hk['crewTook']}, you claimed {hk['claim']}, wrong fix {hk['wrong']} (machine not put right {hk['condSame']}); side job beside a board job {hk['side']} (board {hk['board']}, myJob the board's {hk['myJob']}, side jobs {hk['sides']}); old lift id read as the new {hk['liftCond']} (old gone {hk['noOld']})")
        if (hk['offered'] < 1 or hk['crewTook'] is not False or not hk['claim'] or not hk['wrong'] or not hk['condSame'] or not hk['side'] or not hk['board'] or not hk['myJob'] or hk['sides'] != 'side@1'
            or not hk['hadNew'] or hk['liftCond'] != 33.5 or not hk['noOld']):
            fail('hooks for 24k and M1')

    # 5r. drift (m5-tuning's section 17 part, 0.33.48), with a stand-in 'tune' kind (24e's isn't in this build): none without
    # the kind, none before Day 4 06:00; about one a day after; a drift of 2+ gets a tune job the crew do; ship health within
    # 2 of the run without drift; the same twice and in one jump; the look follows tuneSet both ways; the save keeps a drift
    # and a save without drifts loads settled
    if g.ev("typeof tuneSet === 'function'"):
        DR = r"""((stand, mode) => {
          window.__sc("window.__evD = [typeof eventNow === 'function' ? eventNow : undefined, typeof eventMod === 'function' ? eventMod : undefined]; if (window.__evD[0]) eventNow = () => null; if (window.__evD[1]) eventMod = () => null");
          const own = JOB_KINDS.tune;
          // a stand-in 'tune' kind when 24e's isn't in the build
          const standIn = { text: 'Tune', stops: j => [{ deck: j.deck, placeId: panelPlace(j.machine), mins: 15, tag: 'tune', how: 'turn' }], done: (j, t, by) => tuneSet(j.machine, 0), crew: { can: p => jobCrew(p) === 'works', mins: 15 } };
          if (own && !stand) delete JOB_KINDS.tune;           // 24e's own kind, when it's in, is the one measured (M2)
          if (stand && !own) { JOB_KINDS.tune = standIn; JOB_TYPES.tune = JOB_TYPES.tune || { work: 15, restore: 0, parts: 0 }; }
          const t0 = (SHIP_START.day - 1) * 1440 + SHIP_START.min, out = { first: null, starts: 0, minHealth: 100, tunes: 0, tunedByCrew: 0, sig: [] };
          JOBS_ON = true; MACH_HOUR = null; MACH_SEEN = -1; SHIP.works = null; setShipNow(t0); machinesNow();
          const prev = {};
          const look = t => { for (const m of machineList()) { const d = machineDrift(m.id); if (d && !prev[m.id]) { out.starts++; if (out.first === null) out.first = t; out.sig.push(m.id + '@' + Math.floor(t / 60) + ':' + d); } prev[m.id] = d; } out.minHealth = Math.min(out.minHealth, shipHealth()); };
          if (mode === 'jump') { setShipNow(t0 + 14 * 1440); machinesNow(); }
          else for (let t = t0; t <= t0 + 14 * 1440; t += 60) { setShipNow(t); machinesNow(); look(t); }
          const J = SHIP.jobs.filter(j => j.kind === 'tune'); out.tunes = J.length; out.tunedByCrew = J.filter(j => j.status === 'done' && j.doneBy && j.doneBy !== 'you').length; out.titles = [...new Set(J.map(j => j.title))].slice(0, 4);
          out.end = JSON.stringify(Object.fromEntries(machineList().map(m => [m.id, [Math.round(SHIP.machines[m.id].cond * 1000), machineDrift(m.id)]])));
          delete JOB_KINDS.tune; if (own) JOB_KINDS.tune = own; else delete JOB_TYPES.tune;
          SHIP.jobs = SHIP.jobs.filter(j => j.kind !== 'tune');
          window.__sc("if (window.__evD[0]) eventNow = window.__evD[0]; if (window.__evD[1]) eventMod = window.__evD[1]");
          setShipNow(t0);
          return out;
        })"""
        d0 = g.ev(DR + "(false, 'hour')"); d1 = g.ev(DR + "(true, 'hour')"); d2 = g.ev(DR + "(true, 'hour')"); d3 = g.ev(DR + "(true, 'jump')")
        lk = g.ev("""(() => {
          const t0 = (SHIP_START.day - 1) * 1440 + SHIP_START.min; JOBS_ON = true; MACH_HOUR = null; MACH_SEEN = -1; setShipNow(t0); machinesNow();
          const ov = '3-oven-1', dk = '5-cartdock-1', L = id => { const x = machineLook(id); return [x.flicker, x.dim, x.blink, x.drift || 0]; };
          const out = { before: L(ov) }; tuneSet(ov, 2); out.hot = L(ov); tuneSet(ov, -2); out.cool = L(ov); out.eff = Math.round(machConds()[ov] - SHIP.machines[ov].cond);
          tuneSet(dk, 1); out.dock = L(dk); out.clamp = (tuneSet(ov, 9), machineDrift(ov)); out.notTunable = tuneSet('5-airplant-1', 1);
          const s = { player: { deck: 4, tile: [0, 0], facing: 0 }, ship: { decks: {} }, crew: {} }; SAVE_EXTRA.forEach(f => f(s));
          out.saved = s.ship.machines[ov]; MACH_HOUR = null; machinesLoad(JSON.parse(JSON.stringify(s))); out.loaded = [machineDrift(ov), machineDrift(dk)];
          for (const id in s.ship.machines) s.ship.machines[id] = s.ship.machines[id].slice(0, 2); MACH_HOUR = null; machinesLoad(JSON.parse(JSON.stringify(s)));
          out.old = machineList().some(m => machineDrift(m.id)); tuneSet(ov, 0); tuneSet(dk, 0); out.after = L(ov); out.settled = !machineDrift(ov);
          setShipNow(t0); return out;
        })()""")
        hh = lambda t: None if t is None else f"day {t // 1440 + 1} {t % 1440 // 60:02d}:00"
        print(f"Drift (0.33.48): without the tune kind {d0['starts']} drifts; with a stand-in {d1['starts']} in 14 days (first {hh(d1['first'])}), tune jobs {d1['tunes']} ({d1['tunedByCrew']} done by the crew), e.g. {d1['titles']}")
        print(f"  lowest ship health {d1['minHealth']:.1f} (without drift {d0['minHealth']:.1f}); the same twice {d1['sig'] == d2['sig'] and d1['end'] == d2['end']}, one jump {d1['end'] == d3['end']}")
        print(f"  looks [flicker, dim, blink, drift]: settled {lk['before']}, +2 {lk['hot']}, -2 {lk['cool']} (works {lk['eff']} points lower), dock +1 {lk['dock']}, clamped to {lk['clamp']}, a fan refused {not lk['notTunable']}; after settling {lk['after']}")
        print(f"  save: {lk['saved']} loads as {lk['loaded']}; a save without drifts loads settled {not lk['old']}")
        if (d0['starts'] or not d1['starts'] or d1['first'] < g.ev("TUNE_FROM") or not (5 <= d1['starts'] <= 25) or not d1['tunes'] or not d1['tunedByCrew']
            or d1['minHealth'] < d0['minHealth'] - 2 or d1['sig'] != d2['sig'] or d1['end'] != d2['end'] or d1['end'] != d3['end']
            or not lk['hot'][0] > lk['before'][0] or not lk['cool'][1] > lk['before'][1] or lk['eff'] != -16 or lk['dock'][2] is not True or lk['clamp'] != 3 or lk['notTunable']
            or lk['saved'][2:] != [3] or lk['loaded'] != [3, 1] or lk['old'] or lk['after'] != lk['before'] or not lk['settled']):
            fail('drift')

    # 5s. incidents' machine side (m6-incidents, 0.33.49): machineFault sets a machine faulty (never raises it) and its repair
    # follows within the hour (machineFound finds it at once); liftStuck makes rides 3 times slower until it ends; a burst's
    # joint job is a Tier 1 chore at the place, one seal, 20 minutes, on your board, and the crew fit it when you leave it
    if g.ev("typeof jointJobPost === 'function'"):
        inc = g.ev("""(() => {
          const t0 = (SHIP_START.day - 1) * 1440 + SHIP_START.min, out = {};
          JOBS_ON = true; MACH_HOUR = null; MACH_SEEN = -1; setShipNow(t0 + 7 * 1440 + 240); machinesNow();
          for (const j of SHIP.jobs) if (j.claimedBy === 'you') { j.claimedBy = null; j.status = 'open'; }
          const L = '5-mainlift-1', G = '3-galleyplant-1';
          out.fault = machineFault(L); out.state = SHIP.machines[L].state; out.cond = SHIP.machines[L].cond;
          const c0 = SHIP.machines[G].cond; machineFault(G, 90); out.notRaised = SHIP.machines[G].cond === Math.min(c0, 90);
          const f = machineFound(L); const J = SHIP.jobs.find(j => j.id === (f && f.id)); out.found = !!(f && J && J.kind === 'repair');
          const before = shipEffects(5).lift; out.stuck = liftStuck(true); out.liftX = Math.round(shipEffects(5).lift / before * 100) / 100;
          setShipNow(shipNow() + 45); out.over = !liftStuckNow() && shipEffects(5).lift === shipEffects(5).lift;
          liftStuck(true); liftStuck(false); out.off = !liftStuckNow();
          const id = jointJobPost({ placeId: '4-lift-1', leave: 60 }), jj = SHIP.jobs.find(j => j.id === id);
          out.joint = jj ? [jj.tier, jj.parts.join(), jj.stops.map(x => x.mins + '@' + x.placeId).join(), jobCard(jj)[2]] : null;
          out.onBoard = openJobs('you').some(x => x.id === id);
          const m0 = shipNow(); for (let m = m0 + 60; m <= m0 + 8 * 60; m += 60) { setShipNow(m); machinesNow(); }
          out.crew = jj && jj.claimedBy && jj.claimedBy !== 'you' ? jj.status : null;
          SHIP.jobs = SHIP.jobs.filter(j => j.chore !== 'joint');
          setShipNow(t0); return out;
        })()""")
        print(f"Incidents (0.33.49): machineFault {inc['fault']} -> {inc['state']} ({inc['cond']}), never raised {inc['notRaised']}, its repair found {inc['found']}; lift stuck {inc['stuck']} x{inc['liftX']}, over after 40 min {inc['over']}, off {inc['off']}")
        print(f"  joint job [tier, parts, stops, card] {inc['joint']}, on your board {inc['onBoard']}, the crew's when left: {inc['crew']}")
        if (not inc['fault'] or inc['state'] != 'faulty' or inc['cond'] > 40 or not inc['notRaised'] or not inc['found'] or not inc['stuck'] or inc['liftX'] != 3 or not inc['over'] or not inc['off']
            or not inc['joint'] or inc['joint'][:3] != [1, 'seal', '20@4-lift-1'] or not inc['onBoard'] or inc['crew'] not in ('claimed', 'done')):
            fail("incidents' machine side")

    # 5t. hauling's section 17 part (m4-hauling, 0.33.50), with a stand-in 'haul' kind: without the kind no manifest and no
    # misplaced part; with it each Wednesday delivery brings 2-4 manifest crates to real drop places, counted by holdCrates
    # but not by the unload (partsCrates); manifestTake loads one; on Thursdays about one week in two a part sits on a
    # shelf not its own until a fetch or misplacedFix; the save keeps both; the same twice
    if g.ev("typeof manifestFor === 'function'"):
        HL = r"""((stand) => {
          const own = JOB_KINDS.haul;
          if (stand && !own) jobKindAdd('haul', { junior: true, text: 'Haul', stops: () => [], done: () => {}, crew: { can: () => false, mins: 30 } });
          if (!stand && own) delete JOB_KINDS.haul;
          if (stand && own) JOB_KINDS.haul = { ...own, post: undefined };   // 24d's own: no runs while the arm reads the hold (put back after)
          const t0 = (SHIP_START.day - 1) * 1440 + SHIP_START.min, out = { weeks: [], thursdays: 0, misplaced: [], badDest: [] };
          JOBS_ON = true; MACH_HOUR = null; MACH_SEEN = -1; setShipNow(t0); machinesNow();
          for (let w = 0; w < 4; w++) {
            setShipNow(t0 + (w * 7 + 2) * 1440 + 255); machinesNow();          // Wednesday 10:15
            const M = (SHIP.manifest || []).map(c => c.id + '>' + c.dest); out.weeks.push(M.join(' '));
            for (const c of SHIP.manifest || []) if (!placeById(c.dest)) out.badDest.push(c.dest);
            if (w === 0) { out.crates = [holdCrates(), partsCrates(), manifestCrates()]; const c0 = (SHIP.manifest || [])[0]; out.take = c0 ? JSON.stringify(manifestTake(c0.id)) : null; out.after = manifestCrates(); }
            setShipNow(t0 + (w * 7 + 3) * 1440 + 120); machinesNow();          // Thursday 08:00
            out.thursdays++; if (SHIP.misplaced) { const x = SHIP.misplaced; out.misplaced.push(x.part + '@' + x.on); if (x.on === shelfOf(x.part)) out.badDest.push('own shelf ' + x.part); }
            if (out.saved === undefined && SHIP.misplaced) { const s = { player: { deck: 4, tile: [0, 0], facing: 0 }, ship: { decks: {} }, crew: {} }; SAVE_EXTRA.forEach(f => f(s)); const was = JSON.stringify([SHIP.manifest, SHIP.misplaced]); MACH_HOUR = null; machinesLoad(JSON.parse(JSON.stringify(s))); out.saved = JSON.stringify([SHIP.manifest, SHIP.misplaced]) === was; const p = SHIP.misplaced.part; out.fetchFixes = takePart(p) && !SHIP.misplaced; returnPart(p); }
          }
          if (stand && !own) { delete JOB_KINDS.haul; delete JOB_TYPES.haul; } else if (own) JOB_KINDS.haul = own;
          SHIP.manifest = []; SHIP.misplaced = null; setShipNow(t0);
          return out;
        })"""
        h0 = g.ev(HL + "(false)"); h1 = g.ev(HL + "(true)"); h2 = g.ev(HL + "(true)")
        print(f"Hauling (0.33.50): without the haul kind manifests {[w for w in h0['weeks'] if w]}, misplaced {h0['misplaced']}; with a stand-in: {h1['weeks']}")
        print(f"  week 1 crates [all, parts, manifest] {h1.get('crates')}, took {h1.get('take')}, then {h1.get('after')}; misplaced on {len(h1['misplaced'])} of {h1['thursdays']} Thursdays {h1['misplaced']}; bad {h1['badDest']}; save keeps them {h1.get('saved')}, a fetch puts it right {h1.get('fetchFixes')}; the same twice {h1 == h2}")
        sizes = [len(w.split()) for w in h1['weeks']]
        if (any(h0['weeks']) or h0['misplaced'] or not all(2 <= n <= 4 for n in sizes) or h1['badDest'] or not h1.get('crates') or h1['crates'][0] != h1['crates'][1] + h1['crates'][2]
            or not h1.get('take') or h1['after'] != h1['crates'][2] - 1 or not (1 <= len(h1['misplaced']) <= 3) or h1 != h2 or h1.get('saved') is not True or h1.get('fetchFixes') is not True):
            fail('hauling: the manifest and the misplaced part')

    # 5u. the air line's dampers and the Tier 2 fault tables (Step 3, 0.33.56; architect-air-line.html, fault-tables.html Tier 2):
    # 5-fan-1 and both dampers are real machines with panel places; a broken damper is felt on its own branch's decks only
    # (damper 1: Decks 1-3, damper 2: Decks 4-6) and the other's decks are as before; every Tier 2 kind in MACHINE_KINDS has
    # a table; every cause's line is water, heat or air; within a kind no two causes share both card and sign (5o checks
    # every kind); and on paper over 40 days every Tier 2 machine's part causes all come up, the commonest most, never a load
    if g.ev("typeof FAULT_T2 === 'object'"):
        t2 = g.ev("""(() => {
          const out = { real: {}, panels: {}, branch: {}, missing: [], badLine: [], noShow: [], order: [], loads: 0, kinds: 0 };
          for (const id of ['5-fan-1', '5-damper-1', '5-damper-2']) { const m = machineById(id); out.real[id] = !!m && !m.stub; out.panels[id] = !!panelPlace(id); }
          for (const k of FAULT_T2) if (MACHINE_KINDS[k] && !FAULT_CAUSES[k]) out.missing.push(k);
          for (const k of FAULT_T2) for (const c of FAULT_CAUSES[k] || []) if (c.line && !['water', 'heat', 'air'].includes(c.line)) out.badLine.push(k + '.' + c.id);
          for (const k of FAULT_T2) { const m = machineList().find(x => x.kind === k); if (!m || !FAULT_CAUSES[k]) continue; out.kinds++;
            const n = {}; for (let h = 24; h < 24 * 41; h++) { const c = faultPick(m, h); if (!c) continue; if (c.load) out.loads++; n[c.id] = (n[c.id] || 0) + 1; }
            const allowed = FAULT_CAUSES[k].filter(c => !c.load && !c.band);
            for (const c of allowed) if (!n[c.id]) out.noShow.push(k + '.' + c.id);
            const top = allowed.filter(c => c.w === Math.max(...allowed.map(x => x.w))).map(c => c.id), most = Object.entries(n).sort((a, b) => b[1] - a[1])[0];
            if (most && !top.includes(most[0])) out.order.push(k + ': ' + most[0]); }
          // the dampers' reach: each broken in turn on a fresh ship, the notes per deck
          const t0 = (SHIP_START.day - 1) * 1440 + SHIP_START.min;
          for (const id of ['5-damper-1', '5-damper-2']) {
            JOBS_ON = false; MACH_HOUR = null; MACH_SEEN = -1; setShipNow(t0); machinesNow(); machineFault(id, 5);
            out.branch[id] = Object.keys(DECKS).map(Number).filter(n => shipEffects(n).notes.some(x => x.machine === id));
          }
          JOBS_ON = true; MACH_HOUR = null; MACH_SEEN = -1; setShipNow(t0);
          return out;
        })()""")
        print(f"Air line and Tier 2 tables (0.33.56): real {t2['real']}, panels {t2['panels']}; a broken damper is felt on decks {t2['branch']}")
        print(f"  {t2['kinds']} Tier 2 kinds with a machine; missing tables {t2['missing']}, bad lines {t2['badLine']}, causes never picked {t2['noShow']}, commonest not the most often {t2['order']}, loads picked {t2['loads']}")
        if (not all(t2['real'].values()) or not all(t2['panels'].values()) or t2['branch'].get('5-damper-1') != [1, 2, 3] or t2['branch'].get('5-damper-2') != [4, 5, 6]
            or t2['missing'] or t2['badLine'] or t2['noShow'] or t2['order'] or t2['loads']):
            fail('the air line and the Tier 2 fault tables')

    # 5v. the ship meters and the bridge room (Step 3, 0.33.57; the user's "starts a little lower, so you can see your impact"):
    # a fresh ship's board reads about 75 (72-79), none failing, one or more fine, while the machines' own health (what the
    # effects read) is 90+; untended, every meter only falls a little each day; a steady player (5o's) gets j.meters on every
    # job they finish, biggest first, the biggest a visible step (1+), and the board rises well above its start (85+ by the
    # end); the same twice. A job in the bridge room (Deck 1, B) isn't offered to you or yours to take till SHIP.bridgeInvited,
    # then it is; the crew can take it; the Wednesday manifest has no bridge crate till then. The save keeps the upkeep, and a
    # save without it loads with none
    if g.ev("typeof shipMeters === 'function'"):
        MV = r"""(() => {
          window.__sc("window.__evMv = [typeof eventNow === 'function' ? eventNow : undefined, typeof eventMod === 'function' ? eventMod : undefined]; if (window.__evMv[0]) eventNow = () => null; if (window.__evMv[1]) eventMod = () => null");
          const t0 = (SHIP_START.day - 1) * 1440 + SHIP_START.min, end = t0 + DAYS * 1440, out = { jobs: 0, noMeters: [], small: [], notMain: [], byDay: [] };
          JOBS_ON = true; MACH_HOUR = null; MACH_SEEN = -1; SHIP.works = null; setShipNow(t0); machinesNow();
          const rows = shipHealthRows(); out.start = rows[0].value; out.startRows = rows.slice(1).map(r => r.name + ' ' + r.value + ' ' + r.state); out.machine0 = shipHealth();
          out.failing = rows.filter(r => r.state === 'failing').length; out.fine = rows.slice(1).filter(r => r.state === 'fine').length;
          const m0 = shipMeters(); JOBS_ON = false; setShipNow(t0 + 1440); machinesNow(); const m1 = shipMeters();
          out.creep = SYSTEMS.filter(k => SHIP.upkeep[k] < UPKEEP_START[k] - 1e-9 || SHIP.upkeep[k] > UPKEEP_START[k] + UPKEEP_CREEP * 26 / 24 + 1e-9);   // the start hour's share too
          out.creepDrop = Math.round((shipHealth(m0) - shipHealth(m1)) * 10) / 10;
          JOBS_ON = true; MACH_HOUR = null; MACH_SEEN = -1; setShipNow(t0); machinesNow();
          let mine = null, until = 0;
          for (let t = t0; t <= end; t += 30) {
            setShipNow(t); machinesNow();
            if (mine && t >= until) { const j = SHIP.jobs.find(x => x.id === mine); if (j && j.claimedBy === 'you' && j.status === 'claimed') { jobStops(j).forEach((x, k) => jobStepDone(j.id, k)); finishJob(j.id);
                out.jobs++; const ms = j.meters || [], main = jobMeterSys(j)[0];
                if (!ms.length) out.noMeters.push(j.id); else { if (!SYSTEMS.includes(main)) out.notMain.push(j.id + ' ' + main); if (ms[0].gain < 1) out.small.push(j.id + ' ' + ms[0].gain); } } mine = null; }
            const d = SHIP.time.day, md = t % 1440;
            if (md === 1080) out.byDay.push(Math.round(shipHealthRows()[0].value));
            if (!mine && d >= 2 && playerShiftOn(d) && md >= DAY_SHIFT[0] && md < DAY_SHIFT[1]) { const o = openJobs('you')[0]; if (o && claimJob(o.id)) { mine = o.id; until = t + Math.max(30, o.mins + 20); } }
          }
          out.end = shipHealthRows()[0].value; out.sig = JSON.stringify([SHIP.upkeep, out.byDay]);
          for (const j of SHIP.jobs) if (j.claimedBy === 'you') { j.claimedBy = null; j.status = 'open'; }
          window.__sc("if (window.__evMv[0]) eventNow = window.__evMv[0]; if (window.__evMv[1]) eventMod = window.__evMv[1]");
          return out;
        })()""".replace('DAYS', str(DAYS))
        mv = g.ev(MV); mv2 = g.ev(MV)
        print(f"Ship meters (0.33.57): a fresh ship reads {mv['start']} (machines {mv['machine0']}), failing {mv['failing']}, fine {mv['fine']}: {mv['startRows']}")
        print(f"  untended a day: upkeep out of step {mv['creep']}, the board down {mv['creepDrop']}; a steady player: {mv['jobs']} jobs, without meters {mv['noMeters'][:4]}, main system unknown {mv['notMain'][:4]}, a step under 1 {mv['small'][:4]}")
        print(f"  the board by day {mv['byDay']}, at the end {mv['end']}; the same twice {mv['sig'] == mv2['sig']}")
        if not (72 <= mv['start'] <= 79) or mv['failing'] or not mv['fine'] or mv['machine0'] < 90 or mv['creep'] or not (0 < mv['creepDrop'] < 4):
            fail('the ship meters at the start')
        if not mv['jobs'] or mv['noMeters'] or mv['notMain'] or mv['small'] or mv['end'] < 85 or mv['sig'] != mv2['sig']:
            fail('the ship meters: your jobs')
        br = g.ev("""(() => {
          const t0 = (SHIP_START.day - 1) * 1440 + SHIP_START.min, out = {};
          JOBS_ON = true; MACH_HOUR = null; MACH_SEEN = -1; SHIP.works = null; setShipNow(t0 + 1440 + 180); machinesNow();
          const was = SHIP.bridgeInvited, pl = placeById('1-works-1'), id = 'chore-test:bridge';
          SHIP.jobs.push({ id, machine: null, deck: 1, room: 'B', kind: 'chore', chore: 'delivery', title: 'Test: spares to the bridge', bring: null, tier: 1, stops: [{ deck: 1, placeId: pl.id, mins: 10, tag: 'drop' }], urgency: 0, leave: null, posted: shipNow(), found: shipNow(), claimedBy: null, parts: [], status: 'open' });
          SHIP.bridgeInvited = false; out.offeredShut = openJobs('you').some(o => o.id === id); out.forYouShut = forYou(SHIP.jobs.find(j => j.id === id)); out.claimShut = claimJob(id);
          out.crew = openJobs('teague-theo').some(o => o.id === id) || openJobs(schedPeople().find(p => jobCrew(p) === 'works').id).some(o => o.id === id);
          SHIP.bridgeInvited = true; out.offeredOpen = openJobs('you').some(o => o.id === id); out.claimOpen = claimJob(id);
          dropJob(id); SHIP.jobs = SHIP.jobs.filter(j => j.id !== id);
          const weeks = n => [...Array(n).keys()].map(w => manifestFor(w * 7 + 3).map(c => c.id));
          SHIP.bridgeInvited = false; out.manShut = weeks(8).flat().filter(k => k === 'bridge').length;
          SHIP.bridgeInvited = true; out.manOpen = weeks(8).flat().filter(k => k === 'bridge').length;
          if (was === undefined) delete SHIP.bridgeInvited; else SHIP.bridgeInvited = was;
          // the save: the upkeep goes out and comes back; an older save (no upkeep) loads with none
          SHIP.upkeep.air = 12.345;
          const s = { player: { deck: 4, tile: [0, 0], facing: 0 }, ship: { decks: {} }, crew: {} }; SAVE_EXTRA.forEach(f => f(s));
          const before = JSON.stringify(SHIP.upkeep); MACH_HOUR = null; machinesLoad(JSON.parse(JSON.stringify(s))); out.saved = JSON.stringify(SHIP.upkeep) === before;
          const old = JSON.parse(JSON.stringify(s)); delete old.ship.upkeep; MACH_HOUR = null; machinesLoad(old); out.oldNone = Object.keys(SHIP.upkeep).length === 0;
          MACH_HOUR = null; MACH_SEEN = -1; setShipNow(t0);
          return out;
        })()""")
        print(f"  the bridge room: shut {[br['offeredShut'], br['forYouShut'], br['claimShut']]} (offered, for you, taken), the crew's {br['crew']}; invited {[br['offeredOpen'], br['claimOpen']]}; bridge crates in 8 weeks shut {br['manShut']}, invited {br['manOpen']}; save keeps the upkeep {br['saved']}, an older save none {br['oldNone']}")
        if br['offeredShut'] or br['forYouShut'] or br['claimShut'] or not br['crew'] or not br['offeredOpen'] or not br['claimOpen'] or br['manShut'] or not br['manOpen'] or not br['saved'] or not br['oldNone']:
            fail('the bridge room and the upkeep in the save')

    # 5w. team jobs (m8-team-jobs.html, section 17's part, 0.33.58): a team job posted the day before (Day 11, the recycler, 09:30,
    # 40 minutes, four Works crew at work then, with you): each member is at their spot through it (jobWhere), takes no other
    # job that overlaps it, and is back to their own plan after; you not coming: by the next hour it's the lead's and takes
    # 20% longer, then the lead finishes it and the machine is put right (90+); with you: your stop done puts it right and
    # gives the meters an overhaul's step; you at your spot (j.youIn) and the lead finishing: the step too; the save keeps it
    # (jobWhere the same after a reload); the same twice. And the Tier 2 test job (promotion-officer.html): jobReserve on
    # 4-scrubber-1 with cause filter and drift +2: faulty and drifted at 08:00, its part the filter, no tune job of its own,
    # tuneSet settles the drift (and won't set a scrubber's)
    if g.ev("typeof teamJobPost === 'function'"):
        TM = r"""((mode) => {
          const out = { mode }, d = 11, start = (d - 1) * 1440 + 570, mins = 40;
          JOBS_ON = true; MACH_HOUR = null; MACH_SEEN = -1; SHIP.works = null; setShipNow((d - 2) * 1440 + 960); machinesNow();
          const crew = schedPeople().filter(p => jobCrew(p) === 'works' && (CREW_TIER[p.rank] || 0) >= 2).filter(p => { const a = planWhere(p, start - 5), b = planWhere(p, start + mins + 15); return a && a.act === 'work' && !a.moving && b && b.act === 'work'; }).slice(0, 3).map(p => p.id);
          machineFault('3-recycler-1', 45);
          const id = teamJobPost({ machine: '3-recycler-1', start, mins, team: crew, you: mode !== 'crew', title: 'Recycler membrane change' });
          const j = () => SHIP.jobs.find(x => x.id === id);
          out.id = id; out.team = j() && j().team.length; out.lead = j() && j().lead; out.claimed = j() && j().claimedBy; out.stops = j() && jobStops(j()).length;
          const ppl = new Map(schedPeople().map(p => [p.id, p]));
          out.atSpot = (j() ? j().team : []).every(c => { const w = jobWhere(ppl.get(c), start + 10); return w && w.job === id && w.deck === 3 && w.placeId === j().spots[c]; });
          out.after = (j() ? j().team : []).every(c => { const w = jobWhere(ppl.get(c), j().end + 1); return !w || w.job !== id; });
          // the save keeps it, and jobWhere reads the same after a reload
          const s = { player: { deck: 4, tile: [0, 0], facing: 0 }, ship: { decks: {} }, crew: {} }; SAVE_EXTRA.forEach(f => f(s));
          MACH_HOUR = null; machinesLoad(JSON.parse(JSON.stringify(s)));
          out.saved = !!j() && j().team.every(c => { const w = jobWhere(ppl.get(c), start + 10); return w && w.job === id; });
          // run through the day; your side by mode
          for (let t = (d - 2) * 1440 + 1020; t <= start + 300; t += 30) {
            setShipNow(t); machinesNow();
            if (mode === 'you' && t >= start && j()) j().youIn = true;   // at your spot from the start
            if (mode === 'you' && t >= start + 30 && j() && j().claimedBy === 'you' && !j().workDone) { jobStops(j()).forEach((x, k) => jobStepDone(id, k)); jobFinish(j(), shipNow(), 'you'); }
            if (mode === 'in' && t >= start && j() && !j().youIn) { j().youIn = true; teamYouOut(id); }
          }
          const J = j(); out.status = J && J.status; out.doneBy = J && J.doneBy; out.youOut = !!(J && J.youOut); out.long = J ? J.done - J.start : 0; out.cond = SHIP.machines['3-recycler-1'].cond;
          out.meters = J && J.meters ? J.meters.length : 0;
          // nobody in it on another job that overlaps it
          out.overlap = SHIP.jobs.filter(x => x.id !== id && x.segs && J && J.team.includes(x.claimedBy) && x.start < J.end && J.segsBy[x.claimedBy][0].from < x.end).map(x => x.id + ' ' + x.claimedBy);
          out.sig = JSON.stringify(J);
          MACH_HOUR = null; MACH_SEEN = -1; setShipNow((SHIP_START.day - 1) * 1440 + SHIP_START.min);
          return out;
        })"""
        tc = g.ev(TM + "('crew')"); tc2 = g.ev(TM + "('crew')"); ty = g.ev(TM + "('you')"); ti = g.ev(TM + "('in')"); tn = g.ev(TM + "('out')")
        for r in (tc, ty, ti, tn):
            print(f"Team job ({r['mode']}): {r['id']}, team {r['team']}, lead {r['lead']}, claimed by {r['claimed']}, your stops {r['stops']}; at their spots {r['atSpot']}, back after {r['after']}, kept in the save {r['saved']}; "
                  f"{r['status']} by {r['doneBy']} (you out {r['youOut']}, {r['long']} min), recycler {r['cond']:.0f}, meters {r['meters']}, overlapping jobs {r['overlap'][:3]}")
        print(f"  the same twice {tc['sig'] == tc2['sig']}")
        bad = []
        for r in (tc, ty, ti, tn):
            if not r['id'] or (r['team'] or 0) < 2 or not r['atSpot'] or not r['after'] or not r['saved'] or r['status'] != 'done' or r['cond'] < 90 or r['overlap']: bad.append(r['mode'])
        if tc['claimed'] == 'you' or tc['doneBy'] != tc['lead'] or tc['meters'] or tc['long'] != 40: bad.append('crew only')
        if ty['claimed'] != 'you' or ty['doneBy'] != 'you' or not ty['meters'] or ty['youOut']: bad.append('with you')
        if ti['doneBy'] != ti['lead'] or not ti['meters'] or ti['long'] != 48: bad.append('you at your spot, the lead finishing')
        if not tn['youOut'] or tn['doneBy'] != tn['lead'] or tn['meters'] or tn['long'] != 48: bad.append('you not coming')
        if tc['sig'] != tc2['sig']: bad.append('not the same twice')
        if bad: fail('team jobs: ' + ', '.join(bad))
        tj = g.ev("""(() => {
          const out = {}, d = 9, t0 = (SHIP_START.day - 1) * 1440 + SHIP_START.min;
          JOBS_ON = true; MACH_HOUR = null; MACH_SEEN = -1; SHIP.works = null; setShipNow((d - 1) * 1440 + 360); machinesNow();
          const id = jobReserve('4-scrubber-1', d, 480, 20, { tier: 2, train: 't2', until: (d - 1) * 1440 + 900, cause: 'filter', drift: 2 });
          setShipNow((d - 1) * 1440 + 490); machinesNow();
          const j = SHIP.jobs.find(x => x.id === id), s = SHIP.machines['4-scrubber-1'];
          out.id = id; out.state = s.state; out.drift = s.drift || 0; out.cause = j && j.cause; out.parts = j && j.parts; out.held = j && heldForYou(j);
          out.tune = SHIP.jobs.some(x => x.kind === 'tune' && x.machine === '4-scrubber-1');
          out.setOne = tuneSet('4-scrubber-1', 1); out.settle = tuneSet('4-scrubber-1', 0); out.after = machineDrift('4-scrubber-1'); out.again = tuneSet('4-scrubber-1', 2);
          jobRelease(20); MACH_HOUR = null; MACH_SEEN = -1; setShipNow(t0);
          return out;
        })()""")
        print(f"Tier 2 test job: {tj['id']}, {tj['state']}, drift {tj['drift']}, cause {tj['cause']}, parts {tj['parts']}, held {tj['held']}, its own tune job {tj['tune']}; tuneSet to 1 {tj['setOne']}, to 0 {tj['settle']} (then {tj['after']}), to 2 again {tj['again']}")
        if not tj['id'] or tj['state'] != 'faulty' or tj['drift'] != 2 or tj['cause'] != 'filter' or not tj['parts'] or tj['parts'][0] != 'filter' or not tj['held'] or tj['tune'] or tj['setOne'] or not tj['settle'] or tj['after'] or tj['again']:
            fail('the Tier 2 test job')

    # 5x. the lines and traced faults (m9-tracing.html, architect-air-line.html; 0.33.59): every line names only real machines
    # with panel places, all three on; on a ship with every line machine put right, one machine faulty at a time: the flow
    # reads full above it and on the other branch, and low at it and below it (its twin side by side too), and the reading
    # before it is full; Day 12's training fault (5-valve-2) is found reading the middle (5-pump-1: full) then 5-valve-2 (low
    # after, full before). Traced faults, with you an Officer trained in tracing (SHIP.works.tr.m9 set) and the real crew
    # for twice DAYS days: about half (25-75%) of the line repairs at your tier are traced; each one's cause cuts its line, its card
    # names the symptom and not the machine, openJobs shows no place; none before you're trained; traceMark keeps its readings
    # and finds it at its own machine (which reads low there); finishing it puts the machine right and closes it; the same twice
    if g.ev("typeof MACHINE_LINKS === 'object'"):
        ln = g.ev("""(() => {
          const out = { on: {}, notReal: [], noPanel: [], bad: [], train: null };
          const t0 = (SHIP_START.day - 1) * 1440 + SHIP_START.min;
          for (const l in MACHINE_LINKS) { out.on[l] = lineOn(l); for (const id of lineIds(l)) { const m = machineById(id); if (!m || m.stub) out.notReal.push(id); else if (!panelPlace(id)) out.noPanel.push(id); } }
          JOBS_ON = false; MACH_HOUR = null; MACH_SEEN = -1; setShipNow(t0); machinesNow();
          for (const l in MACHINE_LINKS) for (const x of lineIds(l)) {
            for (const id of lineIds(l)) serviceMachine(id);
            machineFault(x, 30);
            const px = linePath(l, x), step = px[px.length - 1], below = id => { const p = linePath(l, id); return p.length >= px.length && JSON.stringify(p.slice(0, px.length - 1)) === JSON.stringify(px.slice(0, -1)) && p[px.length - 1].some(y => step.includes(y)); };
            for (const id of lineIds(l)) { const f = lineFlow(l, id), low = below(id) || step.includes(id); if (low ? f >= .8 : f < .99) out.bad.push(l + ': ' + x + ' bad, ' + id + ' reads ' + f); }
            if (lineFlow(l, x, true) < .99) out.bad.push(l + ': before ' + x + ' ' + lineFlow(l, x, true));
          }
          for (const id of lineIds('water')) serviceMachine(id);
          machineFault('5-valve-2', 35);
          out.train = [flowWord(lineFlow('water', '5-pump-1')), flowWord(lineFlow('water', '5-valve-2', true)), flowWord(lineFlow('water', '5-valve-2')), flowWord(lineFlow('water', '5-valve-1'))];
          JOBS_ON = true; MACH_HOUR = null; MACH_SEEN = -1; setShipNow(t0);
          return out;
        })()""")
        print(f"Lines (0.33.59): on {ln['on']}, not real {ln['notReal']}, no panel {ln['noPanel']}; one bad machine at a time: wrong readings {ln['bad'][:5]}; Day 12's (5-pump-1, before/after 5-valve-2, 5-valve-1): {ln['train']}")
        if not all(ln['on'].values()) or ln['notReal'] or ln['noPanel'] or ln['bad'] or ln['train'] != ['full', 'full', 'low', 'full']:
            fail('the lines and lineFlow')
        TR = r"""((trained) => {
          window.__sc("window.__evTr = [typeof eventNow === 'function' ? eventNow : undefined, typeof eventMod === 'function' ? eventMod : undefined]; if (window.__evTr[0]) eventNow = () => null; if (window.__evTr[1]) eventMod = () => null");
          const t0 = (SHIP_START.day - 1) * 1440 + SHIP_START.min, end = t0 + 2 * DAYS * 1440, out = { line: 0, traced: 0, badCause: [], showsMachine: [], placeShown: [], decks: [] };
          JOBS_ON = true; MACH_HOUR = null; MACH_SEEN = -1; SHIP.works = null; setShipNow(t0); machinesNow();
          if (typeof worksInit === 'function') worksInit(WORKS_START); if (!SHIP.works) SHIP.works = {}; SHIP.works.tier = 2; SHIP.works.rank = 'officer';   // an Officer from the start
          SHIP.works.tr = { ...(SHIP.works.tr || {}) }; if (trained) SHIP.works.tr.m9 = 1; else delete SHIP.works.tr.m9;   // trained in tracing (24's record) or not
          const seen = new Map();
          for (let t = t0; t <= end; t += 60) {
            setShipNow(t); machinesNow();
            for (const j of SHIP.jobs) if (!seen.has(j.id)) seen.set(j.id, j);
            for (const o of openJobs('you')) { const j = seen.get(o.id); if (j && j.symptom && (o.at || o.place || o.room)) out.placeShown.push(o.id); }
            const j = !out.cardNow && SHIP.jobs.find(x => x.symptom && x.status === 'open' && !x.claimedBy && x.found <= t && !SHIP.jobs.some(y => y.claimedBy === 'you' && y.status === 'claimed'));
            if (j) {                                       // the first one open: readings, then fixing it
              out.cardNow = jobCard(j)[0]; const ids = lineIds(j.symptom.line); out.mid = traceMark(j.id, ids[Math.floor(ids.length / 2)]); out.own = traceMark(j.id, j.machine); out.read = j.read.length; out.found = !!j.traceFound;
              out.claim = claimJob(j.id); jobStops(j).forEach((x, k) => jobStepDone(j.id, k)); out.fin = finishJob(j.id); out.cond = SHIP.machines[j.machine].cond; out.closed = j.status === 'done';
            }
          }
          for (const j of seen.values()) if (j.machine && j.kind === 'repair' && !j.reserved && Math.floor(j.posted / 1440) + 1 >= WORKS_REAL_FROM) {
            const m = machineById(j.machine), l = lineOf(m.id); if (!l || jobTier(j) > 2 || !(FAULT_CAUSES[m.kind] || []).some(c => c.line === l)) continue;
            out.line++; if (!j.symptom) continue; out.traced++;
            const c = faultCause(j); if (!c || c.line !== j.symptom.line || j.symptom.line !== l) out.badCause.push(j.id + ' ' + (c && c.id));
            const card = jobCard(j); if (!j.traceFound && j.status !== 'done' && card[0].includes(machineTitle(m.id))) out.showsMachine.push(j.id);
            out.decks.push(j.symptom.deck);
          }
          out.sig = JSON.stringify([...seen.values()].filter(x => x.symptom).map(x => x.id + ':' + x.cause + ':' + x.symptom.deck).sort());
          for (const x of SHIP.jobs) if (x.claimedBy === 'you') { x.claimedBy = null; x.status = 'open'; }
          SHIP.works = null;
          window.__sc("if (window.__evTr[0]) eventNow = window.__evTr[0]; if (window.__evTr[1]) eventMod = window.__evTr[1]");
          setShipNow(t0);
          return out;
        })"""
        TR = TR.replace('DAYS', str(DAYS))
        tr = g.ev(TR + "(true)"); tr2 = g.ev(TR + "(true)"); tu = g.ev(TR + "(false)")
        share = 100 * tr['traced'] / tr['line'] if tr['line'] else 0
        print(f"  traced faults ({2 * DAYS} days, an Officer): {tr['traced']} of {tr['line']} line repairs at your tier ({share:.0f}%), decks named {sorted(set(tr['decks']))}; cause off its line {tr['badCause'][:3]}, card shows the machine {tr['showsMachine'][:3]}, openJobs shows a place {tr['placeShown'][:3]}")
        print(f"  one: '{tr.get('cardNow')}', read the middle {tr.get('mid')}, its own {tr.get('own')}, readings kept {tr.get('read')}, found {tr.get('found')}; claimed {tr.get('claim')}, fixed {tr.get('fin')} ({tr.get('cond')}), closed {tr.get('closed')}; untrained: {tu['traced']} traced; the same twice {tr['sig'] == tr2['sig']}")
        if (not tr['line'] or not (25 <= share <= 75) or tr['badCause'] or tr['showsMachine'] or tr['placeShown'] or tu['traced'] or tr['sig'] != tr2['sig']
            or not tr.get('cardNow') or not tr.get('found') or (tr.get('own') or {}).get('word') == 'full' or not tr.get('fin') or (tr.get('cond') or 0) < 90 or not tr.get('closed')):
            fail('traced faults')

    # 6. the save
    rt = g.ev("""(() => {
      JOBS_ON = true; MACH_HOUR = null; MACH_SEEN = -1; setShipNow(6 * 1440 + 11 * 60 + 17); machinesNow();
      machineUse('4-washer-1');                            // your use not yet worn in rides in the save
      const s = { player: { deck: 4, tile: [0, 0], facing: 0 }, ship: { decks: {} }, crew: {} }; SAVE_EXTRA.forEach(f => f(s));
      const all = () => JSON.stringify([machinesNow(), SHIP.jobs, SHIP.stores, SHIP.hold, SHIP.short, MACH_EXTRA]);
      const before = all();
      const back = () => JSON.parse(JSON.stringify(s)); MACH_HOUR = null;
      const ok = machinesLoad(back()), after = all();
      const junk = [machinesLoad(null), machinesLoad({ ship: { machines: 5, machineHour: 3 } }), machinesLoad({ ship: { machines: {}, machineHour: 1e9 } })];
      setShipNow(9 * 1440); const later1 = all(); setShipNow(6 * 1440 + 11 * 60 + 17); machinesLoad(back()); setShipNow(9 * 1440); const later2 = all();
      return { ok, same: before === after && later1 === later2, junk, n: Object.keys(s.ship.machines).length, hour: s.ship.machineHour, jobs: s.ship.jobs.length };
    })()""")
    print(f"Save round trip: {rt['n']} machines and {rt['jobs']} jobs at hour {rt['hour']}, read back {rt['ok']}, the same {rt['same']}, junk refused {not any(rt['junk'])}")
    if not (rt['ok'] and rt['same']) or any(rt['junk']): fail('the save round trip')

    print('errors', g.errors[:5])
    if g.errors: ok = False
    print('MACHINE CHECK OK' if ok else 'MACHINE CHECK FAILED')
    g.close()
