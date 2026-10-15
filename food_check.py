# Starship Cadet: food check (keep in the repo, next to day_check.py)
# The galley (section 16) over whole ship days with ?nosave, deterministically:
#   food is ready when each serving window opens (06:00 and 17:00), and the grab shelf has something on it
#   nobody waits more than WAIT_MAX ship minutes for food, and nobody gives up
#   portions and grab items taken equal the crew who came to eat
#   the dish pit clears: no dirty plates and none still out at the end of the day
#   the cold store never runs dry, with its daily top-up
#   the rota: a chef up by 04:45 and at the stoves by 05:00, an early and a late hand every day, no station
#   held by two people at once
#   the same start gives the same days, and the live galley (galleyAdvance) matches the report
#   on Deck 3: food in the pans while serving, covers when they're empty, takePortion, draw calls under BUDGET
#   once the schedules use the rota (section 14's hook): galley staff are where the rota puts them
# Setup and environment as for cadet_test.py.
# Run:  python3 food_check.py BUILD.html [DAY] [DAYS]     (DAY defaults to 1, DAYS to 7)
import sys, json
exec(open(__file__.replace('food_check.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright

DAY = int(sys.argv[2]) if len(sys.argv) > 2 else 1
DAYS = int(sys.argv[3]) if len(sys.argv) > 3 else 7
WAIT_MAX = 5
READY_MIN = 10
BUDGET = 450

ok = True
def fail(msg):
    global ok
    ok = False
    print('  FAIL', msg)

with sync_playwright() as pw:
    g = Game(pw, sys.argv[1])
    g.ev("window.__realTick = tickShip; tickShip = () => {}")
    g.ev("player.steer = null; player.stop()")
    print(f"Days {DAY}-{DAY + DAYS - 1} from {g.ev(f'WEEKDAYS[weekday({DAY})]')}, {g.ev('schedPeople().length')} people, {g.ev('galleyStaff().length')} galley staff")

    # 1. the days
    rep = g.ev(f"galleyReport({DAY}, {DAYS})")
    for st in rep:
        d, r = st['day'], st['ready']
        print(f"Day {d} ({g.ev(f'WEEKDAYS[weekday({d})]')}): came to eat {st['ate']}, hot {st['eaten']}, grab {st['grabbed']}; ready at 06:00 {r['breakfast']['portions']}"
              f" (+{r['breakfast']['grab']} grab), at 17:00 {r['dinner']['portions']}; waited {st['waited']}, longest {st['maxWait']} min {st['maxWho']};"
              f" cooked {st['cooked']}, baked {st['baked']}, wasted {st['waste']}; cold store low {st['coldMin']}, end {st['end']['cold']}")
        print('  staff:', ', '.join(f"{s['id']} {s['role']}" + (f" up {s['wake'] // 60:02d}:{s['wake'] % 60:02d}" if s['wake'] is not None else '') for s in st['staff']))
        for meal in ('breakfast', 'dinner'):
            if r[meal]['portions'] < READY_MIN: fail(f"day {d}: only {r[meal]['portions']} portions ready when {meal} opened")
        if r['breakfast']['grab'] <= 0: fail(f"day {d}: grab shelf empty at 06:00")
        if st['maxWait'] > WAIT_MAX: fail(f"day {d}: {st['maxWho']} waited {st['maxWait']} minutes")
        if st['missed']: fail(f"day {d}: gave up waiting: {st['missed'][:6]}")
        if st['ate'] != st['eaten'] + st['grabbed']: fail(f"day {d}: {st['ate']} came to eat, {st['eaten'] + st['grabbed']} got food")
        if st['end']['dirty'] or st['end']['inUse'] or st['end']['wait']: fail(f"day {d}: at midnight {st['end']}")
        if st['coldOut']: fail(f"day {d}: the cold store ran dry ({st['coldOut']} times)")
        roles = [s['role'] for s in st['staff']]
        chef = [s for s in st['staff'] if s['role'] == 'chef']
        if not chef or chef[0]['wake'] > 285 or chef[0]['first'] > 300: fail(f"day {d}: no chef up by 04:45 and cooking by 05:00: {chef}")
        if 'early' not in roles or 'late' not in roles: fail(f"day {d}: roles {roles}")

    # 2. no station held by two people at once
    clash = g.ev(f"""(() => {{ const out = [];
      for (let d = {DAY}; d < {DAY + DAYS}; d++) {{ const b = [];
        for (const [id, x] of galleyRota(d)) for (const k of x.blocks) if (k.placeId) b.push([k.placeId, k.from, k.to, id]);
        for (const x of b) for (const y of b) if (x !== y && x[0] === y[0] && x[1] < y[2] && y[1] < x[2]) out.push(d + ' ' + x[0] + ' ' + x[3] + '/' + y[3]); }}
      return out; }})()""")
    print('Stations double-booked:', len(clash))
    if clash: fail(f"stations: {clash[:6]}")

    # 3. the same start gives the same days; the live galley matches the report
    a = json.dumps(rep, sort_keys=True)
    b = json.dumps(g.ev(f"(() => {{ GALLEY_EV.clear(); GALLEY_ROTA.clear(); SHIP_DAYS.clear(); shipDay({DAY} + 4); galleyRota({DAY} + 2); return galleyReport({DAY}, {DAYS}); }})()"), sort_keys=True)
    print('The same days twice:', a == b)
    if a != b: fail('the galley came out differently the second time')
    live = g.ev(f"(() => {{ SHIP.galley = null; galleyAdvance(({DAY} - 1) * 1440); const S = galleyAdvance({DAY} * 1440 - 1); return {{ cold: S.cold.meals, servery: S.servery.portions, grab: S.grab.items, dirty: S.dirty, inUse: S.inUse, pots: S.pots.length, wait: S.wait.length }}; }})()")
    print('Live galley matches the report:', live == rep[0]['end'])
    if live != rep[0]['end']: fail(f"live {live} vs report {rep[0]['end']}")

    # 4. Deck 3: what you see, and the player eating
    B = (DAY - 1) * 1440
    vis = {}
    g.ev(f"setShipNow({B} + 6 * 60 + 30); SHIP.galley = null; goToDeck(3); (() => {{ const c = cellPos(32, 6); player.obj.position.copy(c); target.copy(c).setY(.7); }})()")
    for t, name in [(6 * 60 + 30, '06:30'), (9 * 60, '09:00'), (18 * 60, '18:00')]:
        g.ev(f"setShipNow({B} + {t}); deckCrewFill()")
        g.step(3)
        vis[name] = g.ev("({ calls: renderer.info.render.calls, p: SHIP.galley.servery.portions, dirty: SHIP.galley.dirty, food: GV && GV.food ? GV.food.count : -1, covers: GV && GV.covers ? GV.covers.count : -1, plates: GV && GV.plates ? GV.plates.count : -1, text: galleyText() })")
        print(f"Deck 3 at {name}: {vis[name]}")
        if vis[name]['calls'] > BUDGET: fail(f"{name}: {vis[name]['calls']} draw calls")
        if vis[name]['p'] > 0 and vis[name]['food'] != 5 or vis[name]['p'] == 0 and vis[name]['covers'] != 5: fail(f"{name}: pans don't match the servery")
    eat = g.ev(f"(() => {{ setShipNow({B} + 6 * 60 + 40); const a = galleyAdvance(shipNow()).servery.portions, ok = takePortion('player'); return [a, ok, SHIP.galley.servery.portions]; }})()")
    print('The player eats at 06:40:', eat)
    if not (eat[1] and eat[2] == eat[0] - 1): fail(f"takePortion: {eat}")
    rt = g.ev("(() => { const s = galleySave(); const was = JSON.stringify(SHIP.galley); galleyLoad(JSON.parse(JSON.stringify(s))); const same = JSON.stringify(SHIP.galley) === was; const bad = galleyLoad({ junk: 1 }); galleyLoad(s); return [same, bad]; })()")
    print('Save and load:', rt)
    if rt != [True, False]: fail(f"galleySave / galleyLoad: {rt}")

    # 5. once the schedules use the rota: galley staff are at the rota's stations
    hooked = g.ev(f"galleyStaff().some(p => planDay(p, {DAY}).some(s => s.act === 'work' && s.from < {B} + 330))")
    if not hooked: print('Schedules: not using the rota yet (section 14 hook to come); skipped')
    else:
        off = g.ev(f"""(() => {{ const out = [];
          for (const p of galleyStaff()) for (const k of galleyDay(p, {DAY}).blocks) {{ const w = whereIs(p, {B} + (k.from + k.to) / 2);
            if (w.deck !== 3 || w.placeId !== k.placeId) out.push(p.id + ' ' + hhmm(k.from) + ' ' + k.placeId + ' -> ' + w.deck + ' ' + w.placeId); }}
          return out; }})()""")
        print("Galley staff at the rota's stations (mid-block):", 'all' if not off else f"{len(off)} not")
        if off: fail(f"rota vs plans: {off[:6]}")

    print('errors', g.errors[:5])
    if g.errors: ok = False
    print('FOOD CHECK OK' if ok else 'FOOD CHECK FAILED')
    g.close()
