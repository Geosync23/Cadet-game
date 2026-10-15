# Starship Cadet: machine check (keep in the repo, next to day_check.py)
# Runs the ship's machines (section 17) on paper for DAYS ship days with ?nosave and checks, deterministically:
#   with no repairs: conditions only ever fall; nothing is faulty in the first two days; some machines are broken
#   by the end, but the slow ones (reactor, hull, array) are not; ship health falls but stays above 0; every
#   machine's effects stay in range (multipliers, mood)
#   the same ship wears the same way: run twice; one big jump against hour by hour against odd minutes;
#   with the schedule caches cleared
#   with an ideal crew (the day shift services anything worn, a few machines an hour): nothing ever gets past
#   worn, and ship health stays at 90 or more
#   with the real Works crew claiming jobs on paper (B2, B3): nothing breaks, ship health stays at 85 or more,
#   shelves never go below zero, deliveries get carried to storage, easy jobs wait for you first, nobody does two
#   jobs at once or a job outside their work block, jobWhere agrees with the jobs, and it's the same every way
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
      const sg = cur.segs.find(x => x.tag === 'job' || x.tag === 'restock'), w = jobWhere(schedPeople().find(p => p.id === cur.claimedBy), sg.from);
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
  out.jobList = J.map(j => ({ id: j.id, kind: j.kind, status: j.status, by: j.claimedBy, urgency: j.urgency, posted: j.posted, found: j.found, start: j.start, end: j.end, done: j.done, made: j.made || 0, tier: jobTier(j), cargo: j.cargo || null }));
  // nobody on two jobs at once; every job inside its person's work block (whereIs says work all through)
  const byWho = {}; out.overlap = []; out.offShift = [];
  for (const j of J) if (j.segs && j.claimedBy !== 'you') {
    (byWho[j.claimedBy] = byWho[j.claimedBy] || []).push([j.start, j.end]);
    const p = ppl.get(j.claimedBy);
    for (let m = j.start; m < j.end; m += 5) { const w = whereIs(p, m); if (w.act !== 'work') { out.offShift.push(j.id + ' ' + p.id + ' ' + w.act); break; } }
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
    n = g.ev("machineList().length")
    stubs = g.ev("machineList().filter(m => m.stub).length")
    print(f"{n} machines ({stubs} stand-ins), {DAYS} days")

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
    c = g.ev("(() => { SHIP_DAYS.clear(); MACH_USE.clear(); MACH_NORM = null; return 1; })()") and run()
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
    early = [j['id'] for j in done if j['tier'] <= 1 and j['urgency'] < 2 and j['start'] < j['found'] + 180]
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

    # 5. your side: a job you claim is left to you
    y = g.ev("""(() => {
      JOBS_ON = true; MACH_HOUR = null; MACH_SEEN = -1; setShipNow(4 * 1440 + 9 * 60); machinesNow();
      const o = SHIP.machines['3-oven-1']; o.cond = 40; o.state = machineState(40);       // the oven acts up
      setShipNow(4 * 1440 + 10 * 60); machinesNow();
      const j = jobsBoard().find(x => x.machine === '3-oven-1' && !x.claimedBy);
      if (!j) return { none: true };
      const id = j.id, before = SHIP.machines[j.machine].cond, claimed = claimJob(id);
      setShipNow(5 * 1440 + 12 * 60); machinesNow();
      const still = SHIP.jobs.find(x => x.id === id), mine = still && still.claimedBy === 'you' && still.status === 'claimed';
      const fin = finishJob(id), after = SHIP.machines[j.machine].cond;
      const took = takePart('relay'), stock = SHIP.stores.relay;
      return { id, claimed, mine, fin, before, after, took, stock };
    })()""")
    print(f"Your job: {y}")
    if y.get('none') or not (y['claimed'] and y['mine'] and y['fin'] and y['after'] >= 90): fail('claiming and finishing a job yourself')

    # 6. the save
    rt = g.ev("""(() => {
      JOBS_ON = true; MACH_HOUR = null; MACH_SEEN = -1; setShipNow(6 * 1440 + 11 * 60 + 17); machinesNow();
      const s = { player: { deck: 4, tile: [0, 0], facing: 0 }, ship: { decks: {} }, crew: {} }; SAVE_EXTRA.forEach(f => f(s));
      const all = () => JSON.stringify([machinesNow(), SHIP.jobs, SHIP.stores, SHIP.hold]);
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
