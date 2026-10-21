# PR5: turns 7-8 live, real save at 390x844. A: the 15:20 heads-up once (and not again after a real reload), the
# clock's Friday words. B: after the address, who is still on Deck 7 at 17:10 while planned elsewhere, and why.
import os, sys, json, re, pathlib
S = '/tmp/claude-0/-home-user/a4344e06-66ec-50a3-8125-a9cc15d32fe0/scratchpad'
exec(open(S + '/probe/pp.py').read())
path = sys.argv[1]; OUT = pathlib.Path(S + '/probe/shots')
save = {'v': 2, 'build': 'x', 'time': {'day': 5, 'min': 15 * 60 + 16}, 'player': {'deck': 5, 'tile': [20, 4], 'facing': 0}, 'ship': {'decks': {}, 'eventLog': []}, 'crew': {}}
pw = sync_playwright().start()
b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME'), args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
pg = b.new_context(viewport={'width': 390, 'height': 844}, has_touch=True).new_page(); errs = []
pg.on('pageerror', lambda e: errs.append(str(e)))
pg.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
pg.add_init_script(INIT + "try { if (!sessionStorage.getItem('seeded')) { sessionStorage.setItem('seeded', '1'); localStorage.clear(); localStorage.setItem('starship-cadet-save', " + json.dumps(json.dumps(save)) + "); localStorage.setItem('starship-cadet-arrived', '1'); } } catch (e) {}")
tmp = WORK / 'test' / '_r5_78.html'; tmp.write_text(instrument(pathlib.Path(path).read_text()))
def load():
    pg.goto('file://' + str(tmp) + '?debug', timeout=240000); pg.wait_for_function('window.__sc !== undefined || window.__err', timeout=240000)
ev = lambda s: pg.evaluate('s => window.__sc(s)', s)
step = lambda n: pg.evaluate(f'window.__step({n}, 1000/30)')
HOOK = "window.__toasts = window.__toasts || []; if (!window.__th) { window.__th = 1; const t0 = toast; toast = (t, x) => { window.__toasts.push([t, x, clockText()]); t0(t, x); }; }"
load(); step(5); ev(HOOK); print('loaded', ev("clockText()"), ev("[playerShiftOn(5), FRI.hu]"), flush=True)
for k in range(200):
    step(20)
    if ev("SHIP.time.min") >= 923: break
print('A at', ev("clockText()"), 'toasts', ev("window.__toasts"), 'hu', ev("FRI.hu"), flush=True)
ev("saveGame()"); load(); step(3); ev(HOOK)
for k in range(100):
    step(20)
    if ev("SHIP.time.min") >= 928: break
print('A after reload', ev("clockText()"), 'toasts', ev("window.__toasts"), 'hu', ev("FRI.hu"), flush=True)
print('A clock words', ev("[friClock('onshift', 540), friClock('didout', 935), friClock('didout', 935) && null]"), flush=True)
# B
ev("goToDeck(7)"); ev("skipTo(4 * 1440 + 16 * 60 + 47)"); step(5)
for k in range(300):
    step(20)
    if ev("SHIP.time.min") >= 1030: break
W = """(() => { const t = shipNow(), c = cellPos(...DECKS[7].lift); return DECK_CREW.filter(a => { const w = a.p && whereIs(a.p, t); return w && w.deck !== 7; }).map(a => { const w = whereIs(a.p, t);
  return [a.p.id, a.pose, +Math.hypot(a.x - c.x, a.z - c.z).toFixed(1), roomAt(...cellAt(a.x, a.z)), w.deck, w.act || w.tag || '', a.path ? a.path.length : null]; }); })()"""
print('B', ev("clockText()"), json.dumps(ev(W)), flush=True)
pg.screenshot(path=str(OUT / 'fr78_d5_1710.png'))
print('errors', errs[:4])
