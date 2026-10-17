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
    print(f"Tier locks (a tier-3 hatch): {mu['tiers']}")
    if not (mu['ran'] and mu['running'] and .25 < mu['extra'] < .35 and mu['crewSame'] and not mu['broken'] and not mu['plainUse'] and not mu['none']): fail('machineUse')
    if not mu['shapeOk'] or mu['twice'] or (mu['late'] and mu['lateLanded'] is False) or mu['mails'] > 28: fail("Stores' Mail")
    tt = mu['tiers']
    if tt and (not tt['you'] or not tt['youTier1'] or tt['junior'] or tt['senior'] is False): fail('tier locks')   # 0.27.35: the player passes every tier

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
      const small = j => forYou(j) && !j.leave && j.cargo !== 'meals';
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
          f"{wk['firstMorning']} at 08:00 on day 1 ({wk['emptyStart']} empty hours before that), at most {wk['maxHeld']} held; days off{' (stand-in rule)' if wk['stand'] else ''}: held {wk['offHeld']}, "
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
