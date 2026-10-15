# Starship Cadet: machine check (keep in the repo, next to day_check.py)
# Runs the ship's machines (section 17) on paper for DAYS ship days with ?nosave and checks, deterministically:
#   with no repairs: conditions only ever fall; nothing is faulty in the first two days; some machines are broken
#   by the end, but the slow ones (reactor, hull, array) are not; ship health falls but stays above 0; every
#   machine's effects stay in range (multipliers, mood)
#   the same ship wears the same way: run twice; one big jump against hour by hour against odd minutes;
#   with the schedule caches cleared
#   with an ideal crew (the day shift services anything worn, a few machines an hour): nothing ever gets past
#   worn, and ship health stays at 90 or more
#   the save: machines written by the save hook and read back by machinesLoad come out the same
#   nothing runs unless asked: a game left running with ?nosave never touches the machines
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
  MACH_HOUR = null; MACH_SEEN = -1; setShipNow(t0); machinesNow();
  const out = { daily: [], first: {}, rising: [], worst: {}, minHealth: 100, fx: [], jobs: 0 };
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
  };
  if (mode === 'jump') { setShipNow(end); machinesNow(); look(end); }
  else for (let t = t0; t <= end; t += mode === 'odd' ? 37 : 60) {
    setShipNow(t); machinesNow(); look(t);
    const min = t % 1440;
    if (crew && min >= 480 && min < 1020) {
      const due = list.filter(m => SHIP.machines[m.id].state !== 'healthy').sort((a, b) => SHIP.machines[a.id].cond - SHIP.machines[b.id].cond);
      for (const m of due.slice(0, perHour)) { serviceMachine(m.id); out.jobs++; }
    }
    if ((t - t0) % 1440 === 1080) {                      // every day at midnight: a snapshot
      const sys = shipSystems();
      out.daily.push({ day: SHIP.time.day, health: shipHealth(sys), sys, cond: Object.fromEntries(list.map(m => [m.id, Math.round(SHIP.machines[m.id].cond * 10) / 10])) });
      for (const n of Object.keys(DECKS)) { const f = shipEffects(+n); out.fx.push({ deck: +n, restore: f.restore, drain: f.drain, walk: f.walk, cook: f.cook, lift: f.lift, mood: f.mood, notes: f.notes.length }); }
    }
  }
  setShipNow(end); machinesNow(); look(end);
  out.final = Object.fromEntries(list.map(m => [m.id, SHIP.machines[m.id].cond]));
  out.states = Object.fromEntries(list.map(m => [m.id, SHIP.machines[m.id].state]));
  out.kinds = Object.fromEntries(list.map(m => [m.id, m.kind]));
  out.effects4 = shipEffects(4); out.effects3 = shipEffects(3);
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
    inert = g.ev("MACH_HOUR === null")
    print('Untouched by play (?nosave):', inert)
    if not inert: fail('the machines ran without being asked')
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
           and .5 < f['walk'] <= 1 and 1 <= f['cook'] < 3 and 1 <= f['lift'] < 3 and -30 <= f['mood'] <= 0)]
    if bad: fail(f"effects out of range: {bad[:2]}")
    e4 = a['effects4']
    print(f"  Deck 4 at the end: hygiene restore x{e4['restore']['hygiene']:.2f}, energy drain x{e4['drain']['energy']:.2f}, energy restore x{e4['restore']['energy']:.2f}, walk x{e4['walk']:.2f}, mood {e4['mood']}")
    for nt in e4['notes'][:12]: print(f"    {nt['stage']:10} {nt['text']} ({nt['machine']}, {nt['state']})")
    e3 = a['effects3']
    print(f"  Deck 3 at the end: cook x{e3['cook']:.2f}, hunger restore x{e3['restore']['hunger']:.2f}, lift x{e3['lift']:.2f}, mood {e3['mood']}")

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
    i = run(crew=True)
    worst = max(i['worst'].values())
    print(f"Ideal crew ({CREW_PER_HOUR} jobs an hour on the day shift): {i['jobs']} jobs, worst state {['healthy', 'worn', 'faulty', 'failing', 'broken'][worst]}, lowest ship health {i['minHealth']:.1f}")
    print('  ship health by day:', ' '.join(f"{d['health']:.0f}" for d in i['daily']))
    if worst > 1: fail('a machine got past worn with an ideal crew')
    if i['minHealth'] < 90: fail(f"ship health fell to {i['minHealth']} with an ideal crew")

    # 4. the save
    rt = g.ev("""(() => {
      const s = { ship: {} }; SAVE_EXTRA.forEach(f => f(s));
      const before = JSON.stringify(machinesNow());
      const back = JSON.parse(JSON.stringify(s)); MACH_HOUR = null;
      const ok = machinesLoad(back), after = JSON.stringify(machinesNow());
      const junk = [machinesLoad(null), machinesLoad({ ship: { machines: 5, machineHour: 3 } }), machinesLoad({ ship: { machines: {}, machineHour: 1e9 } })];
      return { ok, same: before === after, junk, n: Object.keys(s.ship.machines).length, hour: s.ship.machineHour };
    })()""")
    print(f"Save round trip: {rt['n']} machines at hour {rt['hour']}, read back {rt['ok']}, the same {rt['same']}, junk refused {not any(rt['junk'])}")
    if not (rt['ok'] and rt['same']) or any(rt['junk']): fail('the save round trip')

    print('errors', g.errors[:5])
    if g.errors: ok = False
    print('MACHINE CHECK OK' if ok else 'MACHINE CHECK FAILED')
    g.close()
