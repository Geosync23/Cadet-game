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
#   on Deck 3: food in the pans while serving, covers when they're empty, the grab shelf's stock (when the shelf is
#   live), takePortion, draw calls under BUDGET
#   hover carts (B3): with FOOD.restock 'carts', a week fed by cartClaim never runs short; two days with none does
#   with an empty cold store, people wait at the servery, each in their own spot (galleyHold)
#   once the schedules use the rota (section 14's hook): galley staff are where the rota puts them
#   spoilage (0.29.11): nothing spoils with the chiller fine; with it broken (a stand-in chillerAt), food is binned
#   at the 09:00 and 21:00 checks, the bin shows by the dish pit, Mail gets a note, and a week still never runs short
#   the menu (0.29.11): Friday's treat has a pudding, Sunday's dinner is the crew's top vote, Wednesday's favourite isn't
#   on the week's menu already, the servery and the menu board say what's on
#   busy windows (0.29.12): queues only inside a day's galleyBusy windows (a rush, a slow oven), up to BUSY_WAIT_MAX
#   minutes there and WAIT_MAX elsewhere, nobody gives up, and over the days at least one rush forms a queue
#   birthday cakes (0.29.12): with a stand-in birthday, a cake is baked, shown on the servery from 19:30, gone by 21:30,
#   and named on the board, in galleyText and in Mail
# Setup and environment as for cadet_test.py.
# Run:  python3 food_check.py BUILD.html [DAY] [DAYS]     (DAY defaults to 1, DAYS to 7)
import sys, json
exec(open(__file__.replace('food_check.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright

DAY = int(sys.argv[2]) if len(sys.argv) > 2 else 1
DAYS = int(sys.argv[3]) if len(sys.argv) > 3 else 7
WAIT_MAX = 5
BUSY_WAIT_MAX = 25
READY_MIN = 10
BUDGET = 450

def wait_ok(st, mw=None):                # waits within the limits: longer only inside the day's busy windows
    busy = {b['meal'] for b in st['busy']}
    mm = mw or st['mealMax']
    return all(mm[m] <= (BUSY_WAIT_MAX if m in busy else WAIT_MAX) for m in ('breakfast', 'dinner'))

ok = True
def fail(msg):
    global ok
    ok = False
    print('  FAIL', msg)

with sync_playwright() as pw:
    g = Game(pw, sys.argv[1])
    g.ev("window.__realTick = tickShip; tickShip = () => {}")
    g.ev("player.steer = null; player.stop()")
    print('Food reaches the cold store by:', g.ev("FOOD.restock === 'carts' && typeof cartClaim === 'function' ? 'hover cart only (cartClaim)' : 'the 10:30 top-up'"))
    print(f"Days {DAY}-{DAY + DAYS - 1} from {g.ev(f'WEEKDAYS[weekday({DAY})]')}, {g.ev('schedPeople().length')} people, {g.ev('galleyStaff().length')} galley staff")

    # 1. the days
    rep = g.ev(f"galleyReport({DAY}, {DAYS})")
    for st in rep:
        d, r = st['day'], st['ready']
        print(f"Day {d} ({g.ev(f'WEEKDAYS[weekday({d})]')}): came to eat {st['ate']}, hot {st['eaten']}, grab {st['grabbed']}; ready at 06:00 {r['breakfast']['portions']}"
              f" (+{r['breakfast']['grab']} grab), at 17:00 {r['dinner']['portions']}; waited {st['waited']}, longest {st['maxWait']} min {st['maxWho']};"
              f" cooked {st['cooked']}, baked {st['baked']}, wasted {st['waste']}, spoiled {st['spoiled']}; cold store low {st['coldMin']}, end {st['end']['cold']}")
        print('  staff:', ', '.join(f"{s['id']} {s['role']}" + (f" up {s['wake'] // 60:02d}:{s['wake'] % 60:02d}" if s['wake'] is not None else '') for s in st['staff']))
        for meal in ('breakfast', 'dinner'):
            if r[meal]['portions'] < READY_MIN: fail(f"day {d}: only {r[meal]['portions']} portions ready when {meal} opened")
        if r['breakfast']['grab'] <= 0: fail(f"day {d}: grab shelf empty at 06:00")
        if st['busy']: print('  busy:', ', '.join(f"{b['kind']} at {b['meal']}" for b in st['busy']), f"- longest wait breakfast {st['mealMax']['breakfast']}, dinner {st['mealMax']['dinner']} min")
        if not wait_ok(st): fail(f"day {d}: {st['maxWho']} waited {st['maxWait']} minutes ({st['mealMax']}, busy {st['busy']})")
        if st['missed']: fail(f"day {d}: gave up waiting: {st['missed'][:6]}")
        if st['ate'] != st['eaten'] + st['grabbed']: fail(f"day {d}: {st['ate']} came to eat, {st['eaten'] + st['grabbed']} got food")
        if st['end']['dirty'] or st['end']['inUse'] or st['end']['wait']: fail(f"day {d}: at midnight {st['end']}")
        if st['coldOut']: fail(f"day {d}: the cold store ran dry ({st['coldOut']} times)")
        if st['spoiled']: fail(f"day {d}: {st['spoiled']} meals spoiled with the chiller as new")
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
    # (with section 17's cartWaiting off: here the machines and jobs don't run, so a run left on the board for you
    # would wait all day; holding it for you is checked in 4g)
    live = g.ev(f"""(() => {{ const cw = typeof cartWaiting === 'function' ? cartWaiting : undefined; window.__cw = cw; window.__sc('cartWaiting = undefined');
      SHIP.galley = null; galleyAdvance(({DAY} - 1) * 1440); const S = galleyAdvance({DAY} * 1440 - 1); const out = {{ cold: S.cold.meals, servery: S.servery.portions, grab: S.grab.items, dirty: S.dirty, inUse: S.inUse, pots: S.pots.length, wait: S.wait.length }};
      window.__sc('cartWaiting = window.__cw'); SHIP.galley = null; return out; }})()""")
    print('Live galley matches the report:', live == rep[0]['end'])
    if live != rep[0]['end']: fail(f"live {live} vs report {rep[0]['end']}")

    # 4. Deck 3: what you see, and the player eating
    B = (DAY - 1) * 1440
    vis = {}
    g.ev(f"setShipNow({B} + 6 * 60 + 30); SHIP.galley = null; goToDeck(3); (() => {{ const c = cellPos(32, 6); player.obj.position.copy(c); target.copy(c).setY(.7); }})()")
    for t, name in [(6 * 60 + 30, '06:30'), (9 * 60, '09:00'), (18 * 60, '18:00')]:
        g.ev(f"setShipNow({B} + {t}); deckCrewFill()")
        g.step(3)
        vis[name] = g.ev("({ calls: renderer.info.render.calls, p: SHIP.galley.servery.portions, dirty: SHIP.galley.dirty, food: GV && GV.food ? GV.food.count : -1, covers: GV && GV.covers ? GV.covers.count : -1, plates: GV && GV.plates ? GV.plates.count : -1, grab: SHIP.galley.grab.items, shelf: GV && GV.grab ? GV.grab.count : -1, text: galleyText() })")
        print(f"Deck 3 at {name}: {vis[name]}")
        if vis[name]['calls'] > BUDGET: fail(f"{name}: {vis[name]['calls']} draw calls")
        if vis[name]['shelf'] >= 0 and vis[name]['shelf'] != min(8, -(-vis[name]['grab'] // 2)): fail(f"{name}: grab shelf shows {vis[name]['shelf']} for {vis[name]['grab']} items")
        if vis[name]['p'] > 0 and vis[name]['food'] != 5 or vis[name]['p'] == 0 and vis[name]['covers'] != 5: fail(f"{name}: pans don't match the servery")
    eat = g.ev(f"(() => {{ setShipNow({B} + 6 * 60 + 40); const a = galleyAdvance(shipNow()).servery.portions, ok = takePortion('player'); return [a, ok, SHIP.galley.servery.portions]; }})()")
    print('The player eats at 06:40:', eat)
    q = g.ev(f"(() => {{ setShipNow({B} + 18 * 60); const j = galleyJoin('player'), early = galleyTurn('player'); setShipNow(j.turnAt + .01); const on = galleyTurn('player'), ate = takePortion('player'); return [j.ahead, early, on, ate, galleyTurn('player'), free(...j.at)]; }})()")
    print('The player queues at 18:00 (ahead, turn too soon, turn, ate, turn after, spot free):', q)
    if q[1:] != [False, True, True, False, True]: fail(f"galleyJoin / galleyTurn: {q}")
    if not (eat[1] and eat[2] == eat[0] - 1): fail(f"takePortion: {eat}")
    # an empty cold store: no food at breakfast, so people wait at the servery, each in their own spot
    hold = g.ev(f"""(() => {{ const was = FOOD.restock; FOOD.restock = 'rule'; setShipNow({B} + 6 * 60 + 40); SHIP.galley = null; galleyAdvance({B}); SHIP.galley.cold.meals = 0; SHIP.galley.grab.items = 0;
      galleyAdvance({B} + 6 * 60 + 40); const S = SHIP.galley, ids = S.wait.map(w => w[0]);
      const spots = schedPeople().filter(p => ids.includes(p.id)).map(p => galleyHold(p, shipNow()));
      const named = spots.filter(x => x), out = {{ waiting: ids.length, named: named.length, distinct: new Set(named).size, nulls: spots.filter(x => x === null).length,
        others: schedPeople().filter(p => !ids.includes(p.id)).some(p => galleyHold(p, shipNow()) !== undefined) }};
      SHIP.galley = null; FOOD.restock = was; return out; }})()""")
    print('Cold store empty at 06:40 (no deliveries):', hold)
    if not hold['waiting'] or hold['named'] != hold['distinct'] or hold['named'] != min(4, hold['waiting']) or hold['others']: fail(f"galleyHold: {hold}")
    rt = g.ev("(() => { const s = galleySave(); const was = JSON.stringify(SHIP.galley); galleyLoad(JSON.parse(JSON.stringify(s))); const same = JSON.stringify(SHIP.galley) === was; const bad = galleyLoad({ junk: 1 }); galleyLoad(s); return [same, bad]; })()")
    print('Save and load:', rt)
    if rt != [True, False]: fail(f"galleySave / galleyLoad: {rt}")

    # 4b. hover carts (B3): the cold store fed only by cartClaim. Section 17's rule when it's there, else a stand-in of
    # the agreed rule (a daily run from 09:00 when under 250, an urgent one under 90; carry up to 150, never past the
    # cap; 40 minutes on the way). A week with no shortage, then no carts on days 2 and 3, to show the shortage and the queue
    carts = g.ev(f"""(() => {{ const real = typeof cartClaim === 'function', was = FOOD.restock;
      if (!real) window.__sc("cartClaim = (t, cold) => {{ const md = t % 1440, n = Math.min(150, FOOD.coldCap - cold); return n > 0 && (cold < 90 || (cold < 250 && md >= 540 && md < 1020)) ? {{ meals: n, arriveAt: t + 40 }} : null; }}");
      FOOD.restock = 'carts';
      for (const E of GALLEY_EV.values()) E.k = 0;
      const week = galleyReport({DAY}, {DAYS}).map(st => ({{ coldOut: st.coldOut, coldMin: st.coldMin, maxWait: st.maxWait, mealMax: st.mealMax, busy: st.busy, delivered: st.delivered, ready: st.ready }}));
      const keep = cartClaim, d2 = {DAY} + 1; cartClaim = (t, c, o) => [d2, d2 + 1].includes(Math.floor(t / 1440) + 1) ? null : keep(t, c, o);
      const missed = galleyReport({DAY}, 4).map(st => ({{ coldOut: st.coldOut, coldMin: st.coldMin, maxWait: st.maxWait, waited: st.waited, missed: st.missed.length }}));
      if (real) cartClaim = keep; else window.__sc("cartClaim = undefined"); FOOD.restock = was; return {{ real, week, missed }}; }})()""")
    print('Carts' + (' (section 17)' if carts['real'] else ' (stand-in rule)') + ':', ', '.join(f"day {DAY + k}: low {w['coldMin']}, in {w['delivered']}, wait {w['maxWait']}" for k, w in enumerate(carts['week'])))
    print('  no carts on days 2 and 3:', carts['missed'])
    if any(w['coldOut'] or not wait_ok(w) or w['ready']['breakfast']['portions'] < READY_MIN or w['ready']['dinner']['portions'] < READY_MIN for w in carts['week']): fail('carts: the cold store ran short')
    if not any(m['coldOut'] for m in carts['missed']): fail('carts: two missed days should run the cold store dry')

    # 4c. spoilage: a broken chiller for a week, through a stand-in chillerAt (section 17's, 0.33.17: spoil 0.05 an hour
    # at its worst), which the galley reads before shipEffectsAt
    sp = g.ev(f"""(() => {{ window.__keepCh = typeof chillerAt === 'function' ? chillerAt : undefined; window.__sc("chillerAt = t => ({{ cond: 0, state: 'broken', spoil: .05 }})");
      const week = galleyReport({DAY}, {DAYS}).map(st => ({{ spoiled: st.spoiled, coldOut: st.coldOut, coldMin: st.coldMin, maxWait: st.maxWait, mealMax: st.mealMax, busy: st.busy }}));
      const mail = []; window.__keepMail = window.mailSend; window.__sc("mailSend = x => window.__mailBox.push(x)"); window.__mailBox = mail;
      SHIP.galley = null; setShipNow({B} + 1440 + 9 * 60 + 30); goToDeck(3); galleyAdvance(shipNow()); galleyTick();
      const out = {{ week, mail: mail.map(x => x.subject + ' ' + x.at + ': ' + x.body), bin: SHIP.galley.bin, bags: GV && GV.bin ? GV.bin.count : -1, text: galleyText('cold') }};
      window.__sc("chillerAt = window.__keepCh; mailSend = window.__keepMail"); SHIP.galley = null; return out; }})()""")
    print('Chiller broken for a week, spoiled a day:', [w['spoiled'] for w in sp['week']], 'cold store low:', [w['coldMin'] for w in sp['week']])
    print('  at 09:30 on day', DAY + 1, '- bin', sp['bin'], 'bags', sp['bags'], '|', sp['text'])
    print('  mail:', sp['mail'][:2])
    if not all(w['spoiled'] > 0 for w in sp['week']): fail('spoilage: a broken chiller spoiled nothing on some day')
    if any(w['coldOut'] or not wait_ok(w) for w in sp['week']): fail('spoilage: the cold store ran short with carts running')
    if not sp['bin'] or sp['bags'] < 1: fail(f"spoilage: nothing in the bin by the dish pit at 09:30: {sp}")
    if not sp['mail'] or 'binned' not in sp['mail'][0]: fail('spoilage: no Mail about the binned food')

    # 4d. the menu: two weeks
    mn = g.ev(f"""(() => {{ const out = [];
      for (let d = {DAY}; d < {DAY} + 14; d++) {{ const M = galleyMenu(d), wk = [...Array(7)].map((_, k) => d - weekday(d) + k).filter(x => x !== d && weekday(x) !== 6).map(x => galleyMenu(x).dinner);
        out.push({{ d, wd: weekday(d), b: M.breakfast, dinner: M.dinner, note: M.note, pudding: M.pudding || null, top: M.votes ? M.votes[0] : null, max: M.votes ? Math.max(...M.votes.map(v => v[1])) : 0, clash: weekday(d) === 2 && wk.includes(M.dinner) }}); }}
      return out; }})()""")
    for x in mn: print(f"  {x['d']}: {x['b']} / {x['dinner']}" + (f" ({x['note']})" if x['note'] else ''))
    for x in mn:
        if '.' in x['dinner'] or '.' in x['b']: fail(f"menu: a full stop in a dish name: {x}")
        if x['wd'] == 4 and not x['pudding']: fail(f"menu: Friday {x['d']} has no pudding")
        if x['wd'] == 6 and (not x['top'] or x['top'][0] != x['dinner'] or x['top'][1] != x['max']): fail(f"menu: Sunday {x['d']} isn't the top vote: {x}")
        if x['clash']: fail(f"menu: Wednesday {x['d']}'s favourite is already on the week's menu")
    bd = g.ev(f"""(() => {{ setShipNow({B} + 18 * 60); goToDeck(3); galleyTick(); const mb = ITEMS.find(x => x.t === 'Menu board');
      return {{ text: galleyText('servery'), dinner: galleyMenu({DAY}).dinner, board: GV && GV.boardDay, tap: mb ? mb.x : '' }}; }})()""")
    print('Menu at 18:00:', bd['text'], '| board:', bd['tap'][:90])
    if not bd['text'].startswith(('Serving: ' + bd['dinner'] + '.', 'The pans')) or not str(bd['board']).startswith(f"{DAY}|") or bd['dinner'] not in bd['tap']: fail(f"menu: servery or board: {bd}")

    # 4e. busy windows over four weeks: queues only in them, nobody gives up, and rushes make queues
    bz = g.ev(f"""(() => {{ for (const E of GALLEY_EV.values()) E.k = 0;
      return galleyReport({DAY}, 28).map(st => ({{ day: st.day, busy: st.busy, mealMax: st.mealMax, waited: st.waited, missed: st.missed.length }})); }})()""")
    rush = [x for x in bz if any(b['kind'] == 'rush' for b in x['busy'])]
    slow = [x for x in bz if any(b['kind'] == 'slow' for b in x['busy'])]
    print(f"Busy windows over 28 days: {len(rush)} rushes (queued {sum(x['waited'] for x in rush)}, longest {max([x['mealMax']['dinner'] for x in rush] or [0])} min),"
          f" {len(slow)} slow ovens (longest {max([max(x['mealMax'].values()) for x in slow] or [0])} min); calm days' longest {max([max(x['mealMax'].values()) for x in bz if not x['busy']] or [0])} min")
    for x in bz:
        if not wait_ok(x): fail(f"busy: day {x['day']} waits {x['mealMax']} with {x['busy']}")
        if x['missed']: fail(f"busy: day {x['day']}: {x['missed']} gave up")
    if not rush or not any(x['waited'] for x in rush): fail('busy: no rush made a queue')
    # the first rush day: 17:00 to 18:30 in 5-minute steps, for a minute with a queue the servery's text mentions
    q = g.ev(f"""(() => {{ const d = [...Array(28)].map((_, k) => {DAY} + k).find(d => galleyBusy(d).some(b => b.kind === 'rush'));
      SHIP.galley = null; let hit = null, seen = 0;
      for (let t = 17 * 60; t <= 18 * 60 + 30 && !hit; t += 5) {{ setShipNow((d - 1) * 1440 + t); galleyAdvance(shipNow()); const n = SHIP.galley.wait.length, x = galleyText('servery'); if (n) seen++; if (n && x.includes('waiting')) hit = [hhmm(t), n, x]; }}
      SHIP.galley = null; return [d, hit, seen]; }})()""")
    print('A rush, 17:00-18:30 every 5 minutes (day, first queue the servery mentions, minutes with a queue):', q)
    if not q[1]: fail(f"busy: no queue in the servery's text during a rush: {q}")

    # 4f. a birthday cake: the first birthday from DAY on (ROSTER's), else a stand-in on day DAY + 2 for the first crew member
    ck = g.ev(f"""(() => {{ const real = ROSTER.some(x => x.birthday), first = [...Array(364)].map((_, k) => {DAY} + k).find(d => galleyBirthdays(d).length);
      const p = real ? galleyBirthdays(first)[0] : schedPeople().slice().sort((a, b) => a.id < b.id ? -1 : 1)[0], had = p.birthday, d = real ? first : {DAY} + 2, B = (d - 1) * 1440, out = {{ day: d }};
      if (!real) p.birthday = ((d - 1) % 364) + 1;
      const mail = []; window.__keepMail = window.mailSend; window.__sc("mailSend = x => window.__mailBox.push(x)"); window.__mailBox = mail;
      for (const E of GALLEY_EV.values()) E.k = 0; out.cakes = galleyReport(d, 1)[0].cakes;
      SHIP.galley = null; goToDeck(3);
      for (const [t, k] of [[14 * 60, 'before'], [18 * 60, 'dinner'], [19 * 60 + 45, 'out'], [21 * 60 + 45, 'gone']]) {{
        setShipNow(B + t); galleyTick(); out[k] = {{ cake: !!(SHIP.galley.cake && SHIP.galley.cake.out), shown: !!(GV && GV.cake && GV.cake.visible), candles: GV && GV.candles ? GV.candles.count : -1, text: galleyText('servery') }}; }}
      out.board = galleyBoard(d); out.mail = mail.map(x => x.subject + ': ' + x.body); out.name = p.name; out.real = real;
      window.__sc("mailSend = window.__keepMail"); if (had === undefined) delete p.birthday; else p.birthday = had; GALLEY_EV.clear(); SHIP.galley = null; return out; }})()""")
    print('Birthday cake for', ck['name'] + (f" on day {ck['day']} (ROSTER's birthdays)" if ck['real'] else ' (stand-in birthday)') + ':', 'baked', ck['cakes'], '| 19:45:', ck['out']['text'])
    print('  shown at 14:00/18:00/19:45/21:45:', [ck[k]['shown'] for k in ('before', 'dinner', 'out', 'gone')], '| mail:', ck['mail'][:1])
    if ck['cakes'] != 1 or [ck[k]['shown'] for k in ('before', 'dinner', 'out', 'gone')] != [False, False, True, False] or ck['out']['candles'] != 10: fail(f"cake: {ck}")
    if 'birthday' not in ck['board'] or 'cake' not in ck['out']['text'].lower() or not any('Cake tonight' in m for m in ck['mail']): fail(f"cake: board, text or mail: {ck}")

    # 4f2. section 18's events (0.29.15): a cake for an event with cake: true (Founding Day) and the birthday gathering's
    # time in the Mail; fresh salad on a harvest day's menu. A stand-in eventsOn when section 18 isn't in the build
    ev = g.ev(f"""(() => {{ const real = typeof eventsOn === 'function', keep = real ? eventsOn : undefined, fd = {DAY} + 3, hv = {DAY} + 5;
      if (!real) window.__sc(`eventsOn = d => d === ${{fd}} ? [{{ id: 'founding', name: 'Founding Day', from: 1170, to: 1290, ev: {{ cake: true }}, honorees: [] }}] : d === ${{hv}} ? [{{ id: 'harvest', name: 'Harvest morning', from: 570, to: 690, ev: {{}}, honorees: [] }}] : []`);
      const days = real ? [...Array(364)].map((_, k) => {DAY} + k) : [fd, hv];
      const f = days.find(d => !galleyBirthdays(d).length && eventsOn(d).some(e => e.cake || (e.ev && e.ev.cake))), h = days.find(d => eventsOn(d).some(e => e.id === 'harvest'));
      GALLEY_MENU.clear(); for (const E of GALLEY_EV.values()) E.k = 0;
      const out = {{ real, f, h }};
      if (f) {{ out.cakes = galleyReport(f, 1)[0].cakes; out.board = galleyBoard(f); const mail = []; window.__keepMail = window.mailSend; window.__mailBox = mail; window.__sc("mailSend = x => window.__mailBox.push(x)");
        setShipNow((f - 1) * 1440 + 19 * 60 + 45); SHIP.galley = null; galleyAdvance(shipNow()); out.text = galleyText('servery'); out.mail = mail.map(x => x.body); window.__sc("mailSend = window.__keepMail"); }}
      const b = [...Array(364)].map((_, k) => {DAY} + k).find(d => galleyBirthdays(d).length && eventsOn(d).some(e => e.id === 'birthday'));
      out.gather = b ? galleyCake(b).gather : null;
      if (h) out.salad = galleyMenu(h).note;
      if (!real) window.__sc("eventsOn = undefined"); GALLEY_MENU.clear(); GALLEY_EV.clear(); SHIP.galley = null; return out; }})()""")
    print('Events' + (' (section 18)' if ev['real'] else ' (stand-in eventsOn)') + ':', ev)
    if ev['real'] and not ev['f']: print("  no event with cake: true in section 18 yet: the event cake isn't checked")
    elif not ev['f'] or ev['cakes'] != 1 or 'cake' not in ev['text'].lower() or 'happy' not in ev['board'] or not ev['mail']: fail(f"event cake: {ev}")
    if not ev['h'] or 'salad' not in (ev['salad'] or ''): fail(f"harvest salad: {ev}")
    if ev['real'] and ev['gather'] is None: fail('birthday gathering time not read from eventsOn')

    # 4h. ship-wide events (C7, 0.29.18): section 18's eventMod('galley', key), read on the hour. A stand-in
    # eventModAt for the ion storm's peak on day DAY + 9 (storm stew, quicker pots, 1.5 x the grab shelf, 6 trays for
    # the bridge) and a formal dinner on day DAY + 10 (a batch of 12, 8 extra portions). Inert with no event: the
    # days above already ran with eventNow null (or no section 18)
    evg = g.ev(f"""(() => {{ const keepAt = typeof eventModAt === 'function' ? eventModAt : undefined, keepTr = typeof cartTrays === 'function' ? cartTrays : undefined;
      const storm = {DAY} + 9, dinner = {DAY} + 10, sent = []; window.__sent = sent;
      window.__evs = {{ [storm]: {{ menu: 'stormStew', cook: .75, grab: 1.5, trays: 6 }}, [dinner]: {{ batch: {{ meals: 12, label: 'the Envoy’s dinner' }}, extra: 8 }} }};
      window.__sc("eventModAt = (t, kind, key) => {{ const e = window.__evs[Math.floor(t / 1440) + 1]; return kind === 'galley' && e && e[key] !== undefined ? e[key] : null; }}; cartTrays = o => window.__sent.push(o)");
      for (const E of GALLEY_EV.values()) E.k = 0;
      const plain = galleyReport(storm - 1, 1)[0], rep = galleyReport(storm, 2);
      SHIP.galley = null; setShipNow((storm - 1) * 1440 + 18 * 60 + 30); galleyAdvance(shipNow());
      const out = {{ plainCooked: plain.cooked, plainBaked: plain.baked, storm: {{ cooked: rep[0].cooked, baked: rep[0].baked, trays: rep[0].trays, maxWait: rep[0].maxWait, missed: rep[0].missed.length }},
        dinner: {{ batch: rep[1].batch, cooked: rep[1].cooked, maxWait: rep[1].maxWait }}, dish: SHIP.galley.servery.dish, text: galleyText('servery'), sent: sent.length ? sent[0] : null }};
      setShipNow((dinner - 1) * 1440 + 16 * 60); galleyAdvance(shipNow()); out.batchText = galleyText('servery'); out.cold = SHIP.galley.cold.meals;
      window.__sc("eventModAt = window.__keepAt; cartTrays = window.__keepTr"); window.__keepAt = keepAt; window.__keepTr = keepTr;
      SHIP.galley = null; GALLEY_EV.clear(); return out; }})()""")
    print('Events (stand-in eventModAt): storm', evg['storm'], 'dish', repr(evg['dish']), 'trays sent', evg['sent'])
    print('  ', evg['text'][:150], '| formal dinner', evg['dinner'], '|', evg['batchText'][-80:])
    if evg['dish'] != 'storm stew' or evg['storm']['trays'] != 6 or not evg['sent'] or evg['sent'].get('trays') != 6 or 'bridge' not in evg['text']: fail(f"storm: {evg}")
    if evg['storm']['missed'] or evg['storm']['maxWait'] > BUSY_WAIT_MAX: fail(f"storm: waits {evg['storm']}")
    if evg['dinner']['batch'] != 12 or 'Envoy' not in evg['batchText']: fail(f"formal dinner: {evg['dinner']} {evg['batchText']}")

    # 4g. your cart run (0.29.13): while section 17's cartWaiting(hour) says the run is yours and not unloaded, its
    # meals wait past arriveAt; galleyCartLand(hour) lands them when you unload. A stand-in cartWaiting until it's there
    yc = g.ev(f"""(() => {{ const real = typeof cartWaiting === 'function', keep = real ? cartWaiting : null, mine = new Set();
      window.__mine = mine; window.__sc("cartWaiting = h => window.__mine.has(h)");
      const D0 = {B} + 40 * 1440; if (typeof CART_RUNS !== 'undefined') CART_RUNS.clear();   // a day no other test has asked about
      setShipNow(D0); SHIP.galley = null; galleyAdvance(shipNow()); SHIP.galley.cold.meals = 200;
      let h = null; for (let t = D0 + 9 * 60; t < D0 + 17 * 60 && h === null; t += 60) {{ setShipNow(t - 1); galleyAdvance(t - 1); mine.clear(); mine.add(t / 60); setShipNow(t); galleyAdvance(t); if (SHIP.galley.carts.some(c => c[2] === t / 60)) h = t / 60; }}
      if (h === null) return {{ real, h }};
      const c = SHIP.galley.carts.find(c => c[2] === h), meals = c[1];
      setShipNow(c[0] + 150); const before = galleyAdvance(shipNow()).cold.meals, waiting = SHIP.galley.carts.some(c => c[2] === h), runs = SHIP.galley.carts.length;
      const landed = galleyCartLand(h), after = SHIP.galley.cold.meals, again = galleyCartLand(h);
      window.__sc("cartWaiting = " + (real ? 'window.__keepWait' : 'undefined')); window.__keepWait = keep; if (real) cartWaiting = keep;
      SHIP.galley = null; return {{ real, h, meals, waiting, runs, landed, gained: after - before, again }}; }})()""")
    print('Your cart run (stand-in cartWaiting' + (', section 17 has its own' if yc['real'] else '') + '):', yc)
    if yc['h'] is None or not yc['waiting'] or yc['runs'] != 1 or yc['landed'] != yc['meals'] or yc['gained'] != yc['meals'] or yc['again'] != 0: fail(f"your cart run: {yc}")
    pb = g.ev("(() => { if (typeof ROSTER_PLAYER === 'undefined' || !ROSTER_PLAYER.birthday) return null; const d = ROSTER_PLAYER.birthday; return [d, galleyBoard(d).match(/happy birthday[^!]*!/)[0], galleyWhose(galleyBirthdays(d))]; })()")
    print('Your birthday:', pb if pb else 'not in ROSTER_PLAYER yet')
    if pb and pb[2] != 'your': fail(f"your birthday: {pb}")

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
