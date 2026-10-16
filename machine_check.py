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
#   food runs in live play (0.33.21): the crew take every food run soon after its wait (5f)
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
RUN = r"""(({ days, mode, crew, perHour }) => {
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
    (byWho[j.claimedBy] = byWho[j.claimedBy] || []).push([j.start, j.end]);
    const p = ppl.get(j.claimedBy);
    for (let m = j.start; m < j.end; m += 5) { const w = planWhere(p, m); if (w.act !== 'work') { out.offShift.push(j.id + ' ' + p.id + ' ' + w.act); break; } }
  }
  for (const who in byWho) { const v = byWho[who].sort((a, b) => a[0] - b[0]); for (let i = 1; i < v.length; i++) if (v[i][0] < v[i - 1][1]) out.overlap.push(who); }
  // the overlay: someone mid-job is where the job says
  out.endJobs = JSON.stringify([SHIP.jobs, SHIP.stores, SHIP.hold]);
  JOBS_ON = true;
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

    run = lambda **o: g.page.evaluate("([s, o]) => window.__sc(s)(o)", [RUN, {'days': DAYS, 'mode': 'hour', 'crew': False, 'perHour': CREW_PER_HOUR, **o}])

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
      const k3 = takeable();
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
    if tt and (tt['you'] or not tt['youTier1'] or tt['junior'] or tt['senior'] is False): fail('tier locks')

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
