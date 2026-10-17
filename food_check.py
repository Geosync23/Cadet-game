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
    live = g.ev(f"""(() => {{ const cw = typeof cartWaiting === 'function' ? cartWaiting : undefined; window.__cw = cw; window.__sc('cartWaiting = undefined'); GALLEY_TEST.gardenCarry = () => null;
      SHIP.galley = null; galleyAdvance(({DAY} - 1) * 1440); const S = galleyAdvance({DAY} * 1440 - 1); const out = {{ cold: S.cold.meals, servery: S.servery.portions, grab: S.grab.items, dirty: S.dirty, inUse: S.inUse, pots: S.pots.length, wait: S.wait.length }};
      window.__sc('cartWaiting = window.__cw'); GALLEY_TEST.gardenCarry = null; SHIP.galley = null; return out; }})()""")
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
      const f = days.find(d => !galleyBirthdays(d).length && eventsOn(d).some(e => (e.cake || (e.ev && e.ev.cake)) && !(e.ev && ((e.ev.ties && e.ev.ties.decor === 'cake') || (Array.isArray(e.ev.where) && e.ev.where.length && e.ev.where.every(w => w.deck !== 3)))))), h = days.find(d => eventsOn(d).some(e => e.id === 'harvest'));
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

    # 4h. ship-wide events (C7, 0.29.18): section 18's eventModAt / eventMod('galley', key, t), read on the hour. Stand-ins
    # through GALLEY_TEST (section 18's and 17's functions may be consts) for the ion storm's escalation on day DAY + 9 (storm stew, quicker pots, 1.5 x the grab shelf, 6 trays for
    # the bridge) and a formal dinner on day DAY + 10 (a batch of 12, 8 extra portions). Inert with no event: the
    # days above already ran with eventNow null (or no section 18)
    evg = g.ev(f"""(() => {{
      const storm = {DAY} + 9, dinner = {DAY} + 10, sent = []; window.__sent = sent;
      window.__evs = {{ [storm]: {{ menu: 'stormStew', cook: .75, grab: 1.5, trays: 6 }}, [dinner]: {{ batch: {{ meals: 12, label: 'the Envoy’s dinner' }}, extra: 8 }} }};
      GALLEY_TEST.eventMod = (kind, key, t) => {{ const e = window.__evs[Math.floor(t / 1440) + 1]; return kind === 'galley' && e && e[key] !== undefined ? e[key] : null; }};
      GALLEY_TEST.cartTrays = o => window.__sent.push(o);
      for (const E of GALLEY_EV.values()) E.k = 0;
      const plain = galleyReport(storm - 1, 1)[0], rep = galleyReport(storm, 2);
      SHIP.galley = null; setShipNow((storm - 1) * 1440 + 18 * 60 + 30); galleyAdvance(shipNow());
      const out = {{ plainCooked: plain.cooked, plainBaked: plain.baked, storm: {{ cooked: rep[0].cooked, baked: rep[0].baked, trays: rep[0].trays, maxWait: rep[0].maxWait, missed: rep[0].missed.length }},
        dinner: {{ batch: rep[1].batch, cooked: rep[1].cooked, maxWait: rep[1].maxWait }}, dish: SHIP.galley.servery.dish, text: galleyText('servery'), sent: sent.length ? sent[0] : null }};
      setShipNow((dinner - 1) * 1440 + 16 * 60); galleyAdvance(shipNow()); out.batchText = galleyText('servery'); out.cold = SHIP.galley.cold.meals;
      GALLEY_TEST.eventMod = GALLEY_TEST.cartTrays = null;
      SHIP.galley = null; GALLEY_EV.clear(); return out; }})()""")
    print('Events (stand-ins in GALLEY_TEST): storm', evg['storm'], 'dish', repr(evg['dish']), 'trays sent', evg['sent'])
    print('  ', evg['text'][:150], '| formal dinner', evg['dinner'], '|', evg['batchText'][-80:])
    if evg['dish'] != 'storm stew' or evg['storm']['trays'] != 6 or not evg['sent'] or evg['sent'].get('trays') != 6 or 'bridge' not in evg['text']: fail(f"storm: {evg}")
    if evg['storm']['missed'] or evg['storm']['maxWait'] > BUSY_WAIT_MAX: fail(f"storm: waits {evg['storm']}")
    if evg['dinner']['batch'] != 12 or 'Envoy' not in evg['batchText']: fail(f"formal dinner: {evg['dinner']} {evg['batchText']}")

    # 4i. the storm's galley threads (0.29.21), with section 18: a real event started on day DAY + 20, its galley read
    # through GALLEY_TEST (trays on that day, a broken chiller): spoiled meals and hours the bridge waits for trays are scored
    if g.ev("typeof eventStart === 'function' && typeof eventScore === 'function' && typeof SHIP_EVENTS !== 'undefined' && !!SHIP_EVENTS.ionStorm"):
        th = g.ev(f"""(() => {{ const d = {DAY} + 20, keep = SHIP.event; eventStart('ionStorm', d - 2);
          GALLEY_TEST.eventMod = (kind, key, t) => kind === 'galley' && key === 'trays' && Math.floor(t / 1440) + 1 === d ? 6 : null;
          window.__keepCh2 = typeof chillerAt === 'function' ? chillerAt : undefined; window.__sc("chillerAt = t => ({{ cond: 0, state: 'broken', spoil: .05 }})");
          GALLEY_TEST.cartTrays = () => null;                  // no cart run, so no delivery report: the count stops at 18:00
          SHIP.galley = null; setShipNow((d - 1) * 1440 + 22 * 60); galleyAdvance(shipNow()); const once = JSON.stringify(SHIP.event.threads);
          SHIP.galley = null; galleyAdvance(shipNow()); const out = {{ threads: {{ ...SHIP.event.threads }}, again: JSON.stringify(SHIP.event.threads) === once }};
          // with a run and its delivery report: the trays reach the bridge at 18:45, or never
          const hungry = arrive => {{ eventStart('ionStorm', d - 2); GALLEY_SCORED.clear(); GALLEY_TEST.cartTrays = () => 'trays:bridge@test'; GALLEY_TEST.traysArrivedAt = () => arrive;
            SHIP.galley = null; galleyAdvance(shipNow()); return SHIP.event.threads.bridgeHungry || 0; }};
          out.late = hungry((d - 1) * 1440 + 18 * 60 + 45); out.never = hungry(null);
          GALLEY_TEST.cartTrays = GALLEY_TEST.traysArrivedAt = null; GALLEY_SCORED.clear();
          window.__sc("chillerAt = window.__keepCh2"); GALLEY_TEST.eventMod = null; SHIP.event = keep; SHIP.galley = null; return out; }})()""")
        print('Storm threads scored by the galley on one day (spoiled meals, hours the bridge waited for trays; the same again after a fresh start):', th)
        print('  bridgeHungry by 22:00 with a delivery report: trays at 18:45', th['late'], '| never', th['never'])
        if not th['threads'].get('spoiled') or th['threads'].get('bridgeHungry') != 6 or not th['again'] or th['late'] != 7 or th['never'] != 11: fail(f"storm threads: {th}")
    else: print('Storm threads: no section 18 with the ion storm in this build; skipped')

    # 4j. the garden (0.29.23): four weeks with stand-ins through GALLEY_TEST: a good garden, a dry one (water .3), and
    # one nobody tends (gardenDay gives no one hours). Produce is picked daily and on harvest mornings, used before stored
    # meals, and a poor garden gives less while nobody goes hungry
    gd = g.ev(f"""(() => {{ const run = (at, day) => {{ GALLEY_TEST.gardenAt = at; GALLEY_TEST.gardenDay = day; GARDEN_COND.clear(); for (const E of GALLEY_EV.values()) E.k = 0;
        const r = galleyReport({DAY}, 28), sum = k => r.reduce((a, st) => a + st[k], 0);
        return {{ picked: sum('picked'), fresh: sum('fresh'), binned: sum('produceBinned'), delivered: sum('delivered'), missed: r.reduce((a, st) => a + st.missed.length, 0), coldOut: sum('coldOut'),
          harvest: r.filter(st => gardenHarvestDay(st.day)).map(st => st.picked), daily: r.filter(st => !gardenHarvestDay(st.day)).map(st => st.picked) }}; }};
      const ok = () => ({{ water: 1, feed: 1, light: 1 }});   // the machines as new; the real gardenAt is shown alongside
      const good = run(ok, null), dry = run(t => ({{ water: .3, feed: 1, light: 1 }}), null), alone = run(ok, () => null), real = run(null, null);
      GALLEY_TEST.gardenAt = GALLEY_TEST.gardenDay = null; GARDEN_COND.clear(); return {{ good, dry, alone, real }}; }})()""")
    for k in ('good', 'dry', 'alone', 'real'):
        x = gd[k]; print(f"Garden, 28 days, {k}: picked {x['picked']} ({x['picked'] / 28:.1f} a day; harvest mornings {x['harvest']}), cooked fresh {x['fresh']}, binned {x['binned']}, cart meals in {x['delivered']}, missed {x['missed']}")
    G0, Gd, Ga = gd['good'], gd['dry'], gd['alone']
    if not (20 <= G0['picked'] / 28 <= 40) or G0['fresh'] < .9 * G0['picked'] or min(G0['harvest'] or [0]) < 100 or sum(1 for x in G0['daily'] if x) < .75 * len(G0['daily']): fail(f"garden, good: {G0}")
    if Gd['picked'] > .5 * G0['picked'] or Ga['picked'] > .6 * G0['picked']: fail(f"garden: a poor garden should give much less: dry {Gd['picked']}, untended {Ga['picked']}, good {G0['picked']}")
    if Gd['delivered'] <= G0['delivered']: fail(f"garden: a dry garden should need more meals by cart ({Gd['delivered']} vs {G0['delivered']})")
    if any(x['missed'] or x['coldOut'] for x in (G0, Gd, Ga, gd['real'])): fail('garden: someone went without food')

    # 4k. the garden's carry, crew and Mail (0.29.24): the crates wait while the carry job (a stand-in) says so and land
    # when it's done or when you unload (galleyCarryLand); no gardener on duty means no daily pick; a dry harvest morning
    # sends a Mail
    gk = g.ev(f"""(() => {{ const d = {DAY} + 1, B = (d - 1) * 1440, posted = [], held = new Set(); const mail = []; window.__mailBox = mail; window.__keepMail = window.mailSend; window.__sc("mailSend = x => window.__mailBox.push(x)");
      GALLEY_TEST.gardenCarry = o => {{ posted.push(o); const id = 'garden@' + o.at; held.add(id); return id; }}; GALLEY_TEST.carryWaiting = id => held.has(id);
      SHIP.galley = null; setShipNow(B + 11 * 60); galleyAdvance(shipNow()); const out = {{ posted: posted.map(o => o.title), waiting: SHIP.galley.garden.crates.length, produce: produceMeals(SHIP.galley) }};
      out.landed = galleyCarryLand(posted.length ? 'garden@' + posted[0].at : 'none'); out.again = galleyCarryLand(posted.length ? 'garden@' + posted[0].at : 'none'); out.text = galleyText('garden');
      GALLEY_TEST.gardenCarry = GALLEY_TEST.carryWaiting = null; GALLEY_TEST.gardenCrew = () => [];
      SHIP.galley = null; GARDEN_COND.clear(); galleyAdvance(shipNow()); out.noCrew = SHIP.galley.garden.crates.length + produceMeals(SHIP.galley);
      GALLEY_TEST.gardenCrew = null; GALLEY_TEST.gardenAt = () => ({{ water: .2, feed: 1, light: 1 }}); GARDEN_COND.clear();
      const h = [...Array(28)].map((_, k) => {DAY} + k).find(x => gardenHarvestDay(x) && x > {DAY} + 7);
      SHIP.galley = null; setShipNow((h - 15) * 1440); galleyAdvance(shipNow()); setShipNow((h - 1) * 1440 + 12 * 60); galleyAdvance(shipNow()); out.thin = mail.filter(x => x.subject === 'A thin harvest').map(x => x.body);
      GALLEY_TEST.gardenAt = null; GARDEN_COND.clear(); window.__sc("mailSend = window.__keepMail"); SHIP.galley = null; return out; }})()""")
    print('Garden carry:', gk['posted'][:1], '| crates waiting', gk['waiting'], '| landed', gk['landed'], 'then', gk['again'], '| no gardener on duty:', gk['noCrew'])
    print('  ', gk['text'], '| thin harvest Mail:', gk['thin'][:1])
    if not gk['posted'] or not gk['waiting'] or gk['landed'] <= 0 or gk['again'] != 0 or gk['noCrew'] != 0 or not gk['thin']: fail(f"garden carry: {gk}")

    # 4l. the diplomatic visit's formal dinner (0.29.25): herbs from the garden's stock, or 'noHerbs'; late minutes when
    # worn ovens slow it ('dinnersLate'). A stand-in event through GALLEY_TEST, live, with a running event to score
    if g.ev("typeof eventStart === 'function' && typeof SHIP_EVENTS !== 'undefined' && Object.keys(SHIP_EVENTS).length > 0"):
        fd = g.ev(f"""(() => {{ const d = {DAY} + 30, keep = SHIP.event, id = Object.keys(SHIP_EVENTS)[0]; const run = (herbs, slow) => {{
            eventStart(id, d - 1); SHIP.event.threads = {{}}; GALLEY_SCORED.clear();
            GALLEY_TEST.eventMod = (kind, key, t) => kind === 'galley' && Math.floor(t / 1440) + 1 === d ? ({{ batch: {{ meals: 10, label: 'the Veyli dinner' }}, herbs: true }})[key] ?? null : null;
            SHIP.galley = null; setShipNow((d - 1) * 1440 + 14 * 60); galleyAdvance(shipNow()); SHIP.galley.cold.produce = herbs ? [[1, 6, d]] : [];
            if (slow) window.__keepFx3 = shipEffectsAt, window.__sc("shipEffectsAt = (deck, t) => ({{ ...window.__keepFx3(deck, t), cook: 2 }})");
            setShipNow((d - 1) * 1440 + 16 * 60); galleyAdvance(shipNow()); if (slow) window.__sc("shipEffectsAt = window.__keepFx3");
            return {{ threads: {{ ...SHIP.event.threads }}, batch: SHIP.galley.batch, text: galleyText('servery') }}; }};
          const out = {{ fine: run(true, false), noHerbs: run(false, false), late: run(true, true) }};
          GALLEY_TEST.eventMod = null; SHIP.event = keep; SHIP.galley = null; GALLEY_SCORED.clear(); return out; }})()""")
        print('Formal dinner: with herbs', fd['fine']['threads'], '| without', fd['noHerbs']['threads'], '| worn ovens', fd['late']['threads'], '|', fd['late']['text'][-90:])
        if fd['fine']['threads'].get('noHerbs') or fd['fine']['threads'].get('dinnersLate') or fd['noHerbs']['threads'].get('noHerbs') != 1 or fd['late']['threads'].get('dinnersLate', 0) <= 0: fail(f"formal dinner: {fd}")

    # 4m. the traditions (0.29.26): section 18's tradTies('galley', d), here a stand-in through GALLEY_TEST. A long
    # breakfast (pancakes, serving to 10:00, the morning rota runs on), a harvest supper (all from the garden), a
    # farewell supper's favourite; with the real traditions (once combined) the same is shown, not stood in for
    clr = "GALLEY_TIES.clear(); GALLEY_MENU.clear(); GALLEY_ROTA.clear(); GALLEY_EV.clear(); SHIP_DAYS.clear();"
    tr = g.ev(f"""(() => {{ let sat = {DAY} + 50; while (weekday(sat) !== 5) sat++; const sup = sat + 2, fw = sat + 3, who = schedPeople().slice().sort((a, b) => a.id < b.id ? -1 : 1)[3];
      GALLEY_TEST.tradTies = (kind, d) => kind !== 'galley' ? [] : d === sat ? [{{ id: 'long-breakfast', tie: {{ meal: 'breakfast', dish: 'pancakes', until: '10:00' }} }}]
        : d === sup ? [{{ id: 'harvest-supper', tie: {{ meal: 'dinner', dish: 'harvest-supper', batch: 60 }} }}] : d === fw ? [{{ id: 'farewell-supper', honorees: [who], tie: {{ meal: 'dinner', dish: 'favourite' }} }}] : [];
      {clr}
      const M = galleyMenu(sat), rota = galleyRota(sat), roles = [...rota.values()].filter(x => x.role), blk = r => (roles.find(x => x.role === r) || {{ blocks: [] }}).blocks;
      const cookTo = Math.max(...blk('chef').filter(b => b.from < 840 && (b.task === 'cook' || b.task === 'prep')).map(b => b.to)), lineTo = Math.max(...blk('early').filter(b => b.from < 600 && b.from >= 360 && (b.task === 'serve' || b.task === 'wash')).map(b => b.to));
      const rep = galleyReport(sat, 4), at = (st, h) => st.hours.find(x => x[0] === h);
      SHIP.galley = null; setShipNow((sat - 1) * 1440 + 9 * 60 + 15); const txt = galleyText('servery'), board = galleyBoard(sat);
      const out = {{ sat, breakfast: M.breakfast, bnote: M.bnote, end: galleyServeEnd(sat, 'breakfast'), close: galleyClose(sat, 'breakfast'), endSun: galleyServeEnd(sat + 1, 'breakfast'), cookTo, lineTo,
        at0915: at(rep[0], '09:00'), txt, board: board.slice(0, 120), supper: galleyMenu(sup), farewell: galleyMenu(fw), fav: galleyFav(who),
        days: rep.map(st => ({{ day: st.day, ate: st.ate, got: st.eaten + st.grabbed, missed: st.missed.length, end: st.end, fresh: st.fresh, mealMax: st.mealMax, busy: st.busy }})) }};
      GALLEY_TEST.tradTies = null; {clr} SHIP.galley = null;
      out.real = typeof tradTies === 'function' ? [...Array(21)].map((_, k) => {DAY} + k).map(d => [d, Object.keys(galleyTies(d)).map(m => m + ':' + (galleyTies(d)[m].dish || galleyTies(d)[m].extra || '') + (galleyTies(d)[m].until ? '-' + galleyTies(d)[m].until : '')).join(' ')]).filter(x => x[1]) : null;
      return out; }})()""")
    print(f"Long breakfast (stand-in, day {tr['sat']}): {tr['breakfast']} ({tr['bnote']}); serving to {tr['end']}, leftovers at {tr['close']} (Sunday {tr['endSun']}); chef cooks to {tr['cookTo']}, early hand on the line to {tr['lineTo']}; 09:00 {tr['at0915']}")
    print('  ', tr['txt'][:150], '|', tr['board'])
    print(f"Harvest supper (stand-in): {tr['supper']['dinner']} ({tr['supper']['note']}) | farewell supper: {tr['farewell']['dinner']} ({tr['farewell']['note']}), favourite {tr['fav']}")
    for x in tr['days']: print(f"   day {x['day']}: came {x['ate']}, got {x['got']}, missed {x['missed']}, fresh {x['fresh']}, longest {x['mealMax']}")
    print('Real traditions with galley ties, 21 days:', tr['real'] if tr['real'] else 'none (section 18 has no galley ties yet)')
    if tr['breakfast'] != 'pancakes, fruit and syrup' or tr['end'] != 600 or tr['close'] != 630 or tr['endSun'] != 480 or tr['cookTo'] < 560 or tr['lineTo'] != 600: fail(f"long breakfast: {tr}")
    if 'long breakfast' not in tr['txt'] or 'long breakfast' not in tr['board'] or not tr['at0915'] or tr['at0915'][2] + tr['at0915'][6] <= 0: fail(f"long breakfast texts or food at 09:00: {tr['txt']} | {tr['board']} | {tr['at0915']}")
    if not tr['supper']['dinner'].startswith('the harvest supper') or not tr['supper'].get('supper') or tr['farewell']['dinner'] != tr['fav']: fail(f"suppers: {tr['supper']} {tr['farewell']}")
    for x in tr['days']:
        if x['missed'] or x['ate'] != x['got'] or x['end']['dirty'] or x['end']['inUse'] or x['end']['wait'] or not wait_ok(x, x['mealMax']): fail(f"traditions, day {x['day']}: {x}")

    # 4n. Brennan's tasting table (0.29.27, the vote section 18's tally since 0.29.29): a stand-in Wednesday (tradTies
    # 'galley' extra: 'tasting', and its 'tally') for the cooking: 20 tastes an hour before, two for each taster, the
    # rest wasted, the week's two choices, the plates on Deck 3. With section 18's tallies (tallyOf) and a real tasting
    # table: the galley shows the tally's dishes and votes, your token goes through tallyVote once, and Sunday's side
    # is the tally's winner
    ts = g.ev(f"""(() => {{ let wed = {DAY} + 60; while (weekday(wed) !== 2) wed++; const CH = ['herb-flatbread', 'pickled-beans', 'tomato-jam-oatcakes', 'root-crisps', 'miso-greens', 'bean-fritters', 'carrot-ginger-soup', 'chilli-lime-corn'];
      GALLEY_TEST.tradTies = (kind, d) => d === wed ? (kind === 'galley' ? [{{ id: 'tasting-stand-in', from: 1095, to: 1155, tie: {{ meal: 'dinner', extra: 'tasting', batch: 20 }} }}] : kind === 'tally' ? [{{ id: 'tasting-stand-in', tie: {{ kind: 'tasting', choices: CH }} }}] : []) : [];
      {clr} GALLEY_TASTE.clear();
      const z0 = galleyTasting(wed), rep = galleyReport(wed, 1)[0], B = (wed - 1) * 1440, out = {{ wed, choices: z0.choices, voters: z0.voters.length, winner0: z0.winner, note: galleyMenu(wed).note,
        rep: {{ tastes: rep.tastes, tasted: rep.tasted, missed: rep.missed.length, ate: rep.ate, got: rep.eaten + rep.grabbed }} }};
      SHIP.galley = null; setShipNow(B + 17 * 60); galleyTick(); out.before = galleyText('tasting');
      setShipNow(B + 18 * 60 + 20); galleyTick(); out.text = galleyText('servery'); out.plates = GV && GV.taste ? GV.taste.count : -1; out.left = SHIP.galley.tasting && SHIP.galley.tasting.left;
      setShipNow(B + 19 * 60 + 40); galleyTick(); out.gone = SHIP.galley.tasting; out.plates3 = GV && GV.taste ? GV.taste.count : -1;
      GALLEY_TEST.tradTies = null; {clr} GALLEY_TASTE.clear(); SHIP.galley = null;
      if (typeof tallyOf === 'function') {{                  // the real one
        const rw = [...Array(28)].map((_, k) => {DAY} + 7 + k).find(d => galleyTasting(d)), keepVotes = JSON.stringify(SHIP.events.votes || {{}});
        if (rw) {{
          const z = galleyTasting(rw), r = tallyOf(z.id, rw), RB = (rw - 1) * 1440;
          out.real = {{ day: rw, choices: z.choices, votes: z.votes, tally: r && r.choices.map(c => r.counts[c]), tallyChoices: r && r.choices, winner: z.winner, voters: z.voters.length, n: r && r.n }};
          setShipNow(RB + 18 * 60 + 20); galleyTick(); out.real.left = SHIP.galley.tasting && SHIP.galley.tasting.left;
          out.real.vote = galleyVote(z.choices[1]); out.real.again = galleyVote(0); const z1 = galleyTasting(rw); out.real.you = z1.you; out.real.votes1 = z1.votes; out.real.after = SHIP.galley.tasting && SHIP.galley.tasting.left;
          setShipNow(RB + 19 * 60 + 20); galleyTick(); out.real.result = galleyText('tasting');
          const sun = rw + 4, tl = typeof tallyLast === 'function' ? tallyLast(z.id, sun) : null; out.real.sun = {{ side: galleyMenu(sun).side, note: galleyMenu(sun).note, tallyLast: tl && tl.winner, sideTie: !!(galleyTies(sun).dinner && galleyTies(sun).dinner.side) }};
        }}
        SHIP.events.votes = JSON.parse(keepVotes); GALLEY_MENU.clear(); SHIP.galley = null;
      }}
      return out; }})()""".replace('{clr}', clr))
    print(f"Tasting table (stand-in, day {ts['wed']}): {ts['choices']}, {ts['voters']} tasters, winner {ts['winner0']}; report {ts['rep']}")
    print(f"   menu note: {ts['note']} | 17:00 {ts['before']}")
    print(f"   18:20: {ts['text'][-110:]} | plates {ts['plates']}, left {ts['left']} | 19:40 gone {ts['gone']}, plates {ts['plates3']}")
    r = ts['rep']
    if ts['choices'] != [c.replace('-', ' ') for c in ['herb-flatbread', 'pickled-beans', 'tomato-jam-oatcakes', 'root-crisps', 'miso-greens', 'bean-fritters', 'carrot-ginger-soup', 'chilli-lime-corn'][(2 * ((ts['wed'] - 1) // 7)) % 8:][:2]]: fail(f"tasting choices: {ts['choices']}")
    if r['tastes'] != 20 or r['tasted'] != min(20, 2 * ts['voters']) or r['missed'] or r['ate'] != r['got']: fail(f"tasting report: {r}")
    if 'tasting table' not in ts['note'] or ts['plates'] != 4 or ts['plates3'] != 0 or ts['gone'] is not None or ts['winner0'] is not None: fail(f"tasting table: {ts}")
    R = ts.get('real')
    if R:
        print(f"   real (section 18's tally), day {R['day']}: {R['choices']}, votes {R['votes']} (tally {R['tallyChoices']} {R['tally']}, {R['n']} went; {R['voters']} came to taste) -> {R['winner']}")
        print(f"   your vote {R['vote']}, again {R['again']}, you {R['you']}, votes {R['votes1']}, tastes {R['left']} -> {R['after']} | {R['result']} | Sunday {R['sun']}")
        if [c.replace('-', ' ') for c in R['tallyChoices'][:2]] != R['choices'] or R['votes'] != R['tally'][:2] or not R['vote'] or R['again'] or R['you'] != 1 or R['votes1'][1] != R['votes'][1] + 1: fail(f"tasting with the tally: {R}")
        if R['left'] is not None and R['after'] != max(0, R['left'] - 2): fail(f"your tastes: {R}")
        if R['sun']['sideTie'] and (R['sun']['side'] != (R['sun']['tallyLast'] or '').replace('-', ' ') or "Wednesday's winner" not in R['sun']['note']): fail(f"Sunday's side: {R['sun']}")
    else: print('   no section 18 tally with a tasting table in this build: the vote is not checked')

    # 4o. late meals (0.29.28): simNote('lateMeal', { who, meal, late, how, deck }) live, once per person and meal; heard
    # here with onSim. You: from the grab shelf after dinner's serving ended, and after a 15-minute queue. Crew: an
    # empty cold store makes them give up ('missed'). The report counts what would be posted on ordinary days
    if g.ev("typeof onSim === 'function' && typeof simNote === 'function'"):
        lm = g.ev(f"""(() => {{ const heard = []; window.__late = heard; onSim('lateMeal', x => window.__late.push(x)); const d = {DAY} + 70, B = (d - 1) * 1440, out = {{}};
          SHIP.galley = null; setShipNow(B + 20 * 60 + 45); galleyAdvance(shipNow()); SHIP.galley.grab.items = 5; SHIP.galley.servery.portions = 0; heard.length = 0;
          out.ate = takePortion('player'); out.again = takePortion('player'); out.grabNotes = heard.splice(0);
          SHIP.galley = null; setShipNow(B + 1440 + 17 * 60 + 5); galleyAdvance(shipNow()); heard.length = 0; galleyJoin('player'); setShipNow(B + 1440 + 17 * 60 + 20); galleyAdvance(shipNow()); heard.length = 0; SHIP.galley.servery.portions = Math.max(1, SHIP.galley.servery.portions);
          out.queued = takePortion('player'); out.queueNotes = heard.splice(0);
          SHIP.galley = null; setShipNow(B + 2880 + 17 * 60 + 25); galleyAdvance(shipNow()); heard.length = 0; out.onTime = takePortion('player'); out.onTimeNotes = heard.splice(0);
          SHIP.galley = null; setShipNow(B + 4 * 60); galleyAdvance(shipNow()); SHIP.galley.cold.meals = 0; SHIP.galley.cold.produce = []; SHIP.galley.carts = []; SHIP.galley.servery.portions = 0; SHIP.galley.grab.items = 0; heard.length = 0;
          const keepClaim = typeof cartClaim === 'function'; FOOD.restock = 'none'; setShipNow(B + 9 * 60 + 30); galleyAdvance(shipNow()); FOOD.restock = 'carts';
          out.crew = heard.splice(0); out.kinds = [...new Set(out.crew.map(x => x.how + ' ' + x.meal))];
          window.__late = []; SHIP.galley = null; return out; }})()""")
        print(f"Late meals: you at 20:45 from the shelf {lm['grabNotes']} (a second time: {len(lm['grabNotes']) == 1 and lm['again']}) | after a 15-minute queue {lm['queueNotes']} | on time {lm['onTimeNotes']}")
        print(f"   crew with an empty galley: {len(lm['crew'])} notes, {lm['kinds']}, e.g. {lm['crew'][:2]}")
        gn, qn = lm['grabNotes'], lm['queueNotes']
        if len(gn) != 1 or {k: gn[0].get(k) for k in ('who', 'meal', 'late', 'how', 'deck')} != {'who': 'you', 'meal': 'dinner', 'late': 15, 'how': 'grab', 'deck': 3} or gn[0].get('dish', 0) is not None: fail(f"late meal from the shelf: {gn}")
        if len(qn) != 1 or qn[0]['who'] != 'you' or qn[0]['late'] != 15 or qn[0]['how'] != 'servery' or not qn[0].get('dish') or lm['onTimeNotes']: fail(f"late meal after a queue: {qn} / on time {lm['onTimeNotes']}")
        if not lm['crew'] or any(x['how'] != 'missed' or x['meal'] != 'breakfast' or x['who'] == 'you' for x in lm['crew']) or len({x['who'] for x in lm['crew']}) != len(lm['crew']): fail(f"crew late meals: {lm['crew'][:5]}")
    else: print('Late meals: no simNote/onSim (section 13) in this build; skipped')
    print('Late meals the report would post, by day:', [st['late'] for st in rep])

    # 4p. your place in the queue (0.29.31, the user's report on 0.60.1): on Deck 3, "ahead of you" is the crew really
    # standing at the queue spots (DECK_CREW), never people only planned to be there; your turn comes GALLEY_SERVE.you
    # plus GALLEY_SERVE.each a person (a minute each in a rush). Played with frames: a normal dinner, then an empty
    # galley where the waiters stand in the line
    qq = []
    g.ev("window.__sc('tickShip = window.__realTick')")   # ship time runs with the frames here
    g.ev(f"setShipNow({B} + 17 * 60 + 8); SHIP.galley = null; goToDeck(3); (() => {{ const c = cellPos(32, 6); player.obj.position.copy(c); target.copy(c).setY(.7); }})(); deckCrewFill()")
    probe = """(() => { const now = shipNow(), Q = new Set(GALLEY_QUEUE), d = Math.floor(now / 1440) + 1, md = Math.floor(now) - (d - 1) * 1440;
      const standing = DECK_CREW.filter(a => a.spot && Q.has(a.spot.id) && Math.hypot(a.x - a.spot.x, a.z - a.spot.z) < GALLEY_SERVE.near).length;
      const planned = schedPeople().filter(p => { const w = whereIs(p, now); return w.deck === 3 && w.tag === 'queue'; }).length;
      const rush = galleyEvents(d).busy.some(b => b.kind === 'rush' && md >= b.from && md < b.to);
      const line = typeof servLine === 'function' ? servLine().length : standing, ahead = galleyAhead(now, 'probe');
      return [hhmm(md), line, planned, ahead, +(GALLEY_SERVE.you + ahead * galleyServeMins(now)).toFixed(2), rush, SHIP.galley.wait.length]; })()"""
    for k in range(20):
        g.step(30); qq.append(g.ev(probe))
    g.ev(f"setShipNow({B} + 17 * 60 + 40); galleyAdvance(shipNow()); SHIP.galley.cold.meals = 0; SHIP.galley.cold.produce = []; SHIP.galley.servery.portions = 0; SHIP.galley.grab.items = 0; SHIP.galley.pots = []; SHIP.galley.carts = []; deckCrewFill()")
    empty = []
    for k in range(25):
        g.step(30); empty.append(g.ev(probe))
    # your own turn, played: join at 17:12 with frames running, until galleyTurn (without section 10's line; with it,
    # player_check plays your turn in the real line)
    if not g.ev("typeof servLine === 'function'"): g.ev(f"SHIP.galley = null; setShipNow({B} + 17 * 60 + 12); galleyAdvance(shipNow()); deckCrewFill(); window.__j = galleyJoin('tester')")
    mine = None
    if not g.ev("typeof servLine === 'function'"):
        n = 0
        while n < 300 and not g.ev("galleyTurn('tester')"): g.step(3); n += 3
        mine = g.ev("[window.__j.ahead, +(shipNow() - window.__j.since).toFixed(2)]")
        g.ev("galleyLeave('tester')")
    g.ev("SHIP.galley = null; window.__sc('tickShip = () => {}')")
    print('Queue at dinner (time, standing at the queue spots, planned in a queue stop, ahead shown, minutes to your turn, rush, galley waiting):', qq[::4])
    print('  with an empty galley:', empty[::5])
    if mine: print(f"  your turn, joining at 17:12: {mine[0]} ahead, served after {mine[1]} ship minutes ({mine[1] / 0.6:.1f} real seconds)")
    print('  longest line seen:', max(r[1] for r in qq + empty))
    for r in qq + empty:
        if r[3] != r[1] or (r[1] > 4 and not g.ev("typeof servLine === 'function'")) or abs(r[4] - (1 + r[3] * (1 if r[5] else 0.6))) > .01: fail(f"queue: {r}")
    if not any(r[1] for r in empty): print('  (nobody reached a queue spot in this run: the crew walking to the line is section 10\'s, being rebuilt by sim engineer 3)')
    if mine and mine[1] > 1 + mine[0] * 1 + 0.2: fail(f"your turn: {mine}")

    # 4q. section 10's live line (sim engineer 3's lineJoin / lineSpot / lineFront / lineLeave), stood in for here: you
    # take the spot it gives, your turn comes GALLEY_SERVE.you after you reach the counter (never before), takePortion
    # leaves the line; galleyServeMins / galleyCanServe for section 10's serving
    ln = g.ev(f"""(() => {{ const real = typeof lineJoin === 'function', line = ['cook-a', 'cook-b']; window.__line = line;
      if (!real) window.__sc("lineJoin = id => {{ if (!window.__line.includes(id)) window.__line.push(id); }}; lineSpot = id => ({{ at: [33, 6 - window.__line.indexOf(id)], xy: [33.5, 6.5 - window.__line.indexOf(id)], face: 's' }}); lineFront = id => window.__line[0] === id; lineLeave = id => {{ const k = window.__line.indexOf(id); if (k >= 0) window.__line.splice(k, 1); }}");
      SHIP.galley = null; const B = {B} + 1440 * 2; setShipNow(B + 17 * 60 + 30); galleyAdvance(shipNow()); SHIP.galley.servery.portions = Math.max(5, SHIP.galley.servery.portions);
      const j = galleyJoin('player'), out = {{ real, line: j.line, at: j.at, notYet: galleyTurn('player') }};
      line.shift(); line.shift(); out.front = lineFront('player'); out.atFront = galleyTurn('player'); setShipNow(shipNow() + .6); out.soon = galleyTurn('player'); setShipNow(shipNow() + .45); out.served = galleyTurn('player');
      out.ate = takePortion('player'); out.left = line.slice(); out.mins = galleyServeMins(); out.can = galleyCanServe();
      SHIP.galley.servery.portions = 0; SHIP.galley.grab.items = 0; out.cannot = galleyCanServe();
      if (!real) window.__sc("lineJoin = lineSpot = lineFront = lineLeave = undefined");
      SHIP.galley = null; return out; }})()""")
    print('Live line (stand-in for section 10' + ('; section 10 has its own' if ln['real'] else '') + '):', ln)
    if not ln['real'] and (not ln['line'] or ln['at'] != [33, 4] or ln['notYet'] or not ln['front'] or ln['atFront'] or ln['soon'] or not ln['served'] or not ln['ate'] or ln['left'] or ln['mins'] not in (0.6, 1) or not ln['can'] or ln['cannot']): fail(f"live line: {ln}")

    # 4g. your cart run (0.29.13): while section 17's cartWaiting(hour) says the run is yours and not unloaded, its
    # meals wait past arriveAt; galleyCartLand(hour) lands them when you unload. A stand-in cartWaiting until it's there
    yc = g.ev(f"""(() => {{ const real = typeof cartWaiting === 'function', keep = real ? cartWaiting : null, mine = new Set();
      window.__mine = mine; window.__sc("cartWaiting = h => window.__mine.has(h)");
      const D0 = {B} + 40 * 1440; if (typeof CART_RUNS !== 'undefined') CART_RUNS.clear();   // a day no other test has asked about
      if (SHIP.hold) SHIP.hold.meals = 1200;                 // earlier live tests may have used the hold's meals
      setShipNow(D0); SHIP.galley = null; galleyAdvance(shipNow()); SHIP.galley.cold.meals = 200; SHIP.galley.cold.produce = [];
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
