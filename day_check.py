# Starship Cadet: day check (keep in the repo, next to cadet_test.py and deck_check.py)
# Fast-forwards one whole ship day with ?nosave and checks, deterministically:
#   the schedules (dayReport): everyone sleeps at least 6 hours in their own bed, eats twice and works their
#   whole shift; no place is held by two people at once; no gaps in anyone's day
#   the crew on every deck, minute by minute (the CrewAgents, with no drawing): nobody stuck for more than 10 ship
#   minutes; nobody settles in a place someone else is settled in; nobody lies in a bed that isn't theirs;
#   nobody is left with no way to their place; everyone whereIs puts on the deck is there (or on the way)
#   draw calls: a frame drawn every ship hour on every deck, by the lift and over the crowd, peak under BUDGET
#   the same start gives the same day: the plans, and Deck 4's crew at the end of the day, twice over
#   rooms in use over the week (every place type, with those nobody used listed) and the crew's needs through the day
# Setup and environment as for cadet_test.py.
# Run:  python3 day_check.py BUILD.html [DAY]     (DAY defaults to 1, a Monday)
import sys, json
exec(open(__file__.replace('day_check.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright

DAY = int(sys.argv[2]) if len(sys.argv) > 2 else 1
BUDGET = 450
STEP = 0.05                    # real seconds a step (the main loop's longest frame): 0.03 ship minutes at SHIP_RATE 0.6

# run one deck through the day: the crew logic only, a step at a time; every ship hour, draw a frame or two
SIM = r"""(async ({ n, day, step, draw }) => {
  const B = (day - 1) * 1440, perMin = Math.round(1 / (step * SHIP_RATE)), perHour = perMin * 60, out = { deck: n, stuck: 0, stuckWho: '', shared: 0, sharedWho: [], notOwnBed: [], noPath: [], missing: 0, peakCrew: 0, calls: [], unexpected: [] };
  setShipNow(B); goToDeck(n);
  const own = new Map(schedPeople().map(p => [p.id, p.bed]));
  for (let k = 0; B + k * step * SHIP_RATE < B + 1440; k++) {
    setShipNow(B + k * step * SHIP_RATE);
    updateDeckCrew(step);
    const now = shipNow(), held = new Map();
    for (const a of DECK_CREW) {
      if (a.stuckMax > out.stuck) { out.stuck = a.stuckMax; out.stuckWho = a.p.id + ' ' + hhmm(now - B); }
      if (a.noPath && !out.noPath.includes(a.p.id)) out.noPath.push(a.p.id);
      if (a.settled && a.spot) {
        if (held.has(a.spot.id)) { out.shared++; const w = a.spot.id + ' ' + held.get(a.spot.id) + '/' + a.p.id; if (out.sharedWho.length < 6 && !out.sharedWho.some(x => x.startsWith(w))) out.sharedWho.push(w + ' from ' + hhmm(now - B)); }
        held.set(a.spot.id, a.p.id);
        if (a.spot.pose === 'lie' && PLACE_OF.get(a.spot.id) && PLACE_OF.get(a.spot.id).type === 'bed' && a.spot.id !== own.get(a.p.id)) out.notOwnBed.push(a.p.id + ' in ' + a.spot.id);
      }
    }
    out.peakCrew = Math.max(out.peakCrew, DECK_CREW.length);
    if (k % perMin === 0) {                                   // every ship minute: is everyone due here here?
      const here = new Set(DECK_CREW.map(a => a.p.id));
      for (const p of schedPeople()) { const w = whereIs(p, now); if (w.deck === n && w.act !== 'commute' && now - w.from > 1 && !here.has(p.id)) out.missing++; }
    }
    if (draw && k % perHour === 0) {                         // every ship hour: a frame by the lift and one over the crowd
      for (const view of ['lift', 'crowd']) {
        let c = view === 'lift' ? cellPos(...nearestOpen(LIFT_AT[0], LIFT_AT[1], player)) : null;
        if (!c) { if (!DECK_CREW.length) continue; c = new THREE.Vector3(DECK_CREW.reduce((s, a) => s + a.x, 0) / DECK_CREW.length, 0, DECK_CREW.reduce((s, a) => s + a.z, 0) / DECK_CREW.length); }
        player.obj.position.copy(c); target.copy(c).setY(.7);
        window.__skip = false; window.__step(1, 1);         // one real frame through the main loop (it also ticks the clock a hair)
        out.calls.push([hhmm(now - B), view, renderer.info.render.calls, DECK_CREW.length]);
      }
      setShipNow(B + k * step * SHIP_RATE);
    }
  }
  out.end = DECK_CREW.map(a => [a.p.id, Math.round(a.x * 1000), Math.round(a.z * 1000), a.pose]).sort().join('|');
  return out;
})"""

ok = True
def fail(msg):
    global ok
    ok = False
    print('  FAIL', msg)

with sync_playwright() as pw:
    g = Game(pw, sys.argv[1])
    # stop the game's own loop from moving anything between our steps: we drive the crew ourselves
    g.ev("window.__realTick = tickShip; tickShip = () => {}")
    g.ev("player.steer = null; player.stop()")
    print(f"Day {DAY} ({g.ev(f'WEEKDAYS[weekday({DAY})]')}), {g.ev(f'schedPeople().filter(p => aboard(p, {DAY})).length')} people aboard ({g.ev(f'schedPeople().filter(p => p.guest && aboard(p, {DAY})).length')} of them guests)")

    # 1. the schedules
    r = g.ev(f"dayReport({DAY})")
    print('Schedules:', 'sleep < 6 h', len(r['short']), '| meals < 2', len(r['meals']), '| shift short', len(r['work']), '| double-booked', len(r['double']), '| gaps', len(r['gaps']))
    for k in ('short', 'meals', 'work', 'double', 'gaps'):
        if r[k]: fail(f"{k}: {r[k][:8]}")
    print('  peak headcount by deck:', ', '.join(f"{d}: {v[0]} at {v[1]}" for d, v in sorted(r['peak'].items())))
    if r['unplaced']: print('  moments with no place (standing about):', r['unplaced'])

    # rooms in use: every place type over the week from DAY (types nobody used are listed, not failed)
    rooms = g.ev(f"roomsInUse({DAY}, 7)")
    unused = [x['k'] for x in rooms if not x['uses']]
    few = [f"{x['k']} ({x['people']})" for x in rooms if x['uses'] and x['people'] < 3]
    print(f"Rooms in use over the week from day {DAY}: {len(rooms) - len(unused)} of {len(rooms)} place types (deck and type) used")
    print('  never used:', ', '.join(unused) or 'none')
    print('  used by fewer than 3 people:', ', '.join(few) or 'none')
    # crew needs on paper through the day (lowest and middle value of each)
    nd = g.ev(f"""(() => {{ const out = []; for (const hm of [390, 720, 1140, 1380]) {{ const all = schedPeople().filter(p => aboardAllDay(p, {DAY})).map(p => crewNeeds(p, ({DAY} - 1) * 1440 + hm));
      out.push(hhmm(hm) + '  ' + NEEDS.map(k => {{ const v = all.map(n => n[k]).sort((a, b) => a - b); return k + ' ' + v[0] + '/' + v[v.length >> 1]; }}).join('  ')); }} return out; }})()""")
    print('Crew needs (lowest/middle):'); [print('  ' + l) for l in nd]

    # 2. the same start gives the same plans
    a = g.ev(f"(() => {{ SHIP_DAYS.clear(); return JSON.stringify(schedPeople().map(p => planDay(p, {DAY}))); }})()")
    b = g.ev(f"(() => {{ SHIP_DAYS.clear(); shipDay({DAY} + 3); shipDay({DAY} - 1); return JSON.stringify(schedPeople().map(p => planDay(p, {DAY}))); }})()")
    print('Plans the same twice:', a == b)
    if a != b: fail('plans differ between runs')

    # 3. every deck through the day
    decks = g.ev("Object.keys(DECKS).map(Number)")
    for n in decks:
        o = g.page.evaluate(f"s => window.__sc(s)({{ n: {n}, day: {DAY}, step: {STEP}, draw: true }})", SIM)
        peak = max([c[2] for c in o['calls']] or [0])
        print(f"Deck {n}: up to {o['peakCrew']} crew, worst stuck {o['stuck']:.1f} ship min ({o['stuckWho']}), draw calls peak {peak} (budget {BUDGET})")
        busiest = sorted(o['calls'], key=lambda c: -c[2])[:2]
        print('  busiest frames:', ', '.join(f"{c[0]} {c[1]} {c[2]} calls, {c[3]} crew" for c in busiest))
        if o['stuck'] > 10: fail(f"deck {n}: {o['stuckWho']} stuck {o['stuck']:.1f} ship minutes")
        if o['shared']: fail(f"deck {n}: two people settled in one place {o['shared']} times: {o['sharedWho']}")
        if o['notOwnBed']: fail(f"deck {n}: in someone else's bed: {sorted(set(o['notOwnBed']))[:6]}")
        if o['noPath']: fail(f"deck {n}: no way to their place: {o['noPath'][:8]}")
        if o['missing']: fail(f"deck {n}: someone due on the deck wasn't there ({o['missing']} person-minutes)")
        if peak > BUDGET: fail(f"deck {n}: {peak} draw calls")

    # jobs (section 17): the machine panels and other places the crew's jobs took them to, from the day just run
    jv = g.ev("typeof jobVisits === 'function' ? jobVisits() : null")
    if jv is not None:
        print('Job visits (jobs on the books after the day):', ', '.join(f"{x['k']}: {x['visits']} at {x['places']}" for x in jv) or 'none')

    # 4. the same day twice on the crew's own deck (both runs without drawing: a drawn frame also runs the game's loop)
    o1 = g.page.evaluate(f"s => window.__sc(s)({{ n: 4, day: {DAY}, step: {STEP}, draw: false }})", SIM)
    o2 = g.page.evaluate(f"s => window.__sc(s)({{ n: 4, day: {DAY}, step: {STEP}, draw: false }})", SIM)
    print('Deck 4 the same twice:', o1['end'] == o2['end'])
    if o1['end'] != o2['end']: fail('Deck 4 came out differently the second time')

    print('errors', g.errors[:5])
    if g.errors: ok = False
    print('DAY CHECK OK' if ok else 'DAY CHECK FAILED')
    g.close()
