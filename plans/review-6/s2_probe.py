# PR6 s2_probe: EV4's S2 (2ec6f17) and the mess-only dimming (f9eeb72), on a copy with EVENTS_ON and SHORT_FRIDAY on, 390x844:
#  1. on paper (whereIs) Marrow and Vance, Day 12 15:20-17:10: off the bridge for the address 15:30/15:45 to 16:50, back after;
#     how many planned in the address at 16:05; the same plans after a reload at 16:10;
#  2. live on the rec deck 15:55-16:10: crew in the auditorium, Marrow and Vance there, draw calls;
#  3. Day 13 18:25: FEEL_S.lamp .85 in the mess hall, back to 0 on the plaza, .85 again in the mess.
# was PR4: EV4's props (96bb2c6): the lantern supper only (part b of s37_probe), with the lanterns and the low light;
# was: EV3's storm S3/S5/S7 (d3bf237), live, switched on, at 390x844:
#  a. S7 Friday Day 12 17:05 in the mess near Lukas: his moment opens ("Sixty"), reply 0 holds the lantern job; no
#     Lukas Mail at 20:50; the lantern job yours when it posts Saturday 14:00;
#  b. S5 the lantern supper, Saturday Day 13: from 17:40 frames played in the mess to 18:40: crew in the mess hall,
#     Brennan there and Lukas not, staying in off, draw calls (phones: under 450), a shot;
#  c. S3 Day 12 15:00 on Deck 7: a rec tap refused with the storm words.
import os, sys, json, re, pathlib
os.environ.setdefault('CADET_WORK', '/tmp/cadet-work')
exec(open('/home/user/cadet-game/plans/review-6/pp.py').read())
path = sys.argv[1]; OUT = pathlib.Path('/home/user/cadet-game/plans/review-6/shots'); OUT.mkdir(exist_ok=True)
save = {'v': 2, 'build': 'x', 'time': {'day': 12, 'min': 900}, 'player': {'deck': 3, 'tile': [20, 10], 'facing': 0}, 'ship': {'decks': {}, 'eventLog': [], 'evFrom': 0}, 'crew': {}}
pw = sync_playwright().start()
b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME'), args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
ctx = b.new_context(viewport={'width': 390, 'height': 844}, has_touch=True); pg = ctx.new_page(); errs = []
pg.on('pageerror', lambda e: errs.append(str(e)))
pg.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
pg.add_init_script(INIT + "try { if (!sessionStorage.getItem('seeded')) { sessionStorage.setItem('seeded', '1'); localStorage.clear(); localStorage.setItem('starship-cadet-save', " + json.dumps(json.dumps(save)) + "); localStorage.setItem('starship-cadet-arrived', '1'); } } catch (e) {}")
(WORK / 'test').mkdir(parents=True, exist_ok=True)
tmp = WORK / 'test' / '_s2_on.html'; tmp.write_text(instrument(pathlib.Path(path).read_text()))
pg.goto('file://' + str(tmp) + '?debug'); pg.wait_for_function('window.__sc !== undefined || window.__err', timeout=90000)
pg.add_style_tag(content='.bub{animation:none!important}')
ev = lambda s: pg.evaluate('s => window.__sc(s)', s)
step = lambda n: pg.evaluate(f'window.__step({n}, 1000/30)')
step(20); res = {}
PUT = """((deck, rx) => { if (deckDef.num !== deck) goToDeck(deck); const R = DECKS[deck].rooms, key = Object.keys(R).find(k => rx.test(R[k].name || ''));
  const pl = DECKS[deck].places.find(p => p.room === key && p.type !== 'callhome') || DECKS[deck].places.find(p => p.room === key); const c = pl.at, P = cellPos(...c), o = nearestOpen(P.x, P.z, player) || c;
  player.obj.position.copy(cellPos(...o)); player.path.length = 0; target.copy(player.obj.position).setY(.7); return [key, R[key].name]; })"""
PAPER = """(() => { const P = id => ROSTER.find(p => p.id === id), out = {};
  for (const id of ['marrow', 'vance']) { const p = P(id); out[id] = [];
    for (let m = 15 * 60 + 20; m <= 17 * 60 + 10; m += 5) { const w = whereIs(p, 11 * 1440 + m); out[id].push(hhmm(m) + ' ' + (w ? w.deck + ':' + (w.placeId || w.act) + (w.tag ? '#' + w.tag : '') : '-')); } }
  out.at1605 = ROSTER.filter(p => { const w = whereIs(p, 11 * 1440 + 965); return w && w.tag && /address/.test(w.tag); }).length;
  return out; })()"""
r1 = ev(PAPER); res['paper'] = r1
for k in ('marrow', 'vance'): print(k, r1[k], flush=True)
print('at 16:05 planned at the address', r1['at1605'], flush=True)
# 2. live: to the rec deck auditorium, 15:55 to 16:10
ev("skipTo(11 * 1440 + 15 * 60 + 55)"); step(5); print('aud', ev(PUT + "(7, /^Auditorium$/)"), flush=True)
dc = []
for k in range(20):
    step(60)
    if k % 5 == 4:
        r = ev("""(() => { const R = DECKS[7].rooms, inA = DECK_CREW.filter(a => a.p && a.h && (() => { const c = [Math.round(a.x + OX), Math.round(a.z + OZ)]; const k = roomAt(...c); return k && R[k] && /^Auditorium$/.test(R[k].name || ''); })());
          window.__skip = false; window.__step(1, 16); return [clockText(), inA.length, inA.some(a => a.p.id === 'marrow'), inA.some(a => a.p.id === 'vance'), renderer.info.render.calls]; })()""")
        dc.append(r); print('  ', r, flush=True)
res['live'] = dc
pg.screenshot(path=str(OUT / 's2_address.png'), timeout=180000)
# the reload: plans the same after a save and reload mid-address
ev("saveGame()"); pg.reload(); pg.wait_for_function('window.__sc !== undefined || window.__err', timeout=90000); step(20)
r2 = ev(PAPER); res['reloadSame'] = all(r1[k] == r2[k] for k in ('marrow', 'vance', 'at1605')); print('reload same plans', res['reloadSame'], flush=True)
# 3. the lantern supper's light, by room
ev("skipTo(12 * 1440 + 18 * 60 + 25)"); step(5)
lamp = []
for rx in ['/^Mess hall$/', '/^Promenade$/', '/^Mess hall$/']:
    print('put', ev(PUT + "(3, " + rx + ")"), flush=True); step(120)
    lamp.append([rx, ev("[clockText(), +FEEL_S.lamp.toFixed(2), DRESS.on.has('lanternMess'), roomAt(...player.here())]")]); print('  ', lamp[-1], flush=True)
    if rx == '/^Promenade$/': pg.screenshot(path=str(OUT / 's2_plaza_supper.png'), timeout=180000)
res['lamp'] = lamp
ok = (lamp[0][1][1] > .8 and lamp[1][1][1] < .05 and lamp[2][1][1] > .8 and res['reloadSame'] and max(x[4] for x in dc) < 450
      and any(x[2] for x in dc) and any(x[3] for x in dc))
print('RESULT', res); print('errors', errs[:5]); print('S2', 'OK' if ok and not errs else 'CHECK')
b.close(); pw.stop()
