# PR6 (party_probe, from PR4's props_probe): the all-clear party, Day 14 19:30-20:30 in the bow lounge, switched on, 390x844:
# crew in the lounge, at most its places, draw calls at the default zoom and at ZOOM_MIN (0.7 on a phone), a shot.
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
save = {'v': 2, 'build': 'x', 'time': {'day': 14, 'min': 1080}, 'player': {'deck': 3, 'tile': [20, 10], 'facing': 0}, 'ship': {'decks': {}, 'eventLog': [], 'evFrom': 0}, 'crew': {}}
pw = sync_playwright().start()
b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME'), args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
ctx = b.new_context(viewport={'width': 390, 'height': 844}, has_touch=True); pg = ctx.new_page(); errs = []
pg.on('pageerror', lambda e: errs.append(str(e)))
pg.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
pg.add_init_script(INIT + "try { if (!sessionStorage.getItem('seeded')) { sessionStorage.setItem('seeded', '1'); localStorage.clear(); localStorage.setItem('starship-cadet-save', " + json.dumps(json.dumps(save)) + "); localStorage.setItem('starship-cadet-arrived', '1'); } } catch (e) {}")
(WORK / 'test').mkdir(parents=True, exist_ok=True)
tmp = WORK / 'test' / '_party_on.html'; tmp.write_text(instrument(pathlib.Path(path).read_text()))
pg.goto('file://' + str(tmp) + '?debug'); pg.wait_for_function('window.__sc !== undefined || window.__err', timeout=90000)
pg.add_style_tag(content='.bub{animation:none!important}')
ev = lambda s: pg.evaluate('s => window.__sc(s)', s)
step = lambda n: pg.evaluate(f'window.__step({n}, 1000/30)')
step(20); res = {}
PUT = """((deck, rx) => { if (deckDef.num !== deck) goToDeck(deck); const R = DECKS[deck].rooms, key = Object.keys(R).find(k => rx.test(R[k].name || ''));
  const pl = DECKS[deck].places.find(p => p.room === key && p.type !== 'callhome') || DECKS[deck].places.find(p => p.room === key); const c = pl.at, P = cellPos(...c), o = nearestOpen(P.x, P.z, player) || c;
  player.obj.position.copy(cellPos(...o)); player.path.length = 0; target.copy(player.obj.position).setY(.7); return [key, R[key].name]; })"""
ev("skipTo(13 * 1440 + 19 * 60 + 20)"); step(5); print('lounge', ev(PUT + "(3, /^Bow lounge$/)"), flush=True)
dc = []
RD = """(() => { const R = DECKS[3].rooms, inL = DECK_CREW.filter(a => a.p && a.h && (() => { const c = [Math.round(a.x + OX), Math.round(a.z + OZ)]; const k = roomAt(...c); return k && R[k] && /^Bow lounge$/.test(R[k].name || ''); })());
  window.__skip = false; const z0 = camera.zoom; window.__step(1, 16); const c1 = renderer.info.render.calls; setZoom(ZOOM_MIN); window.__step(1, 16); const c2 = renderer.info.render.calls; setZoom(z0);
  return [clockText(), inL.length, c1, c2, +ZOOM_MIN.toFixed(2)]; })()"""
for k in range(30):
    step(60)
    if k % 5 == 4:
        r = ev(RD); dc.append(r); print('  ', r, flush=True)
pg.screenshot(path=str(OUT / 'party_390.png'), timeout=180000)
mx = max(max(x[2], x[3]) for x in dc); peak = max(x[1] for x in dc)
print('RESULT', {'peak': peak, 'maxcalls': mx}); print('errors', errs[:5]); print('PARTY', 'OK' if mx < 450 and not errs else 'CHECK')
b.close(); pw.stop()
