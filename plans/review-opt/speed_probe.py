# OR1's probe for opt #8 (the Dev Speed card). Two builds: the build, and a copy with the card's three wrappers taken out
# (the `if (DEVMODE) { const now = ...` block made `if (false)`). Each: a Dev game (#dev, real saving, 390x844), signed,
# 600 frames, Deck 3 and back to Deck 4 by goToDeck and by the lift's own path, 600 frames more; then the Dev save, the
# clock, where you stand and every walker's place must be the same in both (the wrappers change nothing they wrap).
# On the build: the Speed tab's lines at 390x844, turned 844x390, the TriFold 412x960; every size listed; the last deck
# change filled; Copy and Start again; no errors. Without #dev: no wrappers (render, rAF and goToDeck are the game's own).
#   python3 speed_probe.py BUILD.html
import sys, os, re, json, pathlib, hashlib
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("import sys, json, hashlib")[0])
from playwright.sync_api import sync_playwright
src = pathlib.Path(sys.argv[1]).read_text()
blk = "if (DEVMODE) {\n  const now = () => performance.now(), rr = renderer.render.bind(renderer)"
assert src.count(blk) == 1
B = {'card': src, 'bare': src.replace(blk, "if (false) {\n  const now = () => performance.now(), rr = renderer.render.bind(renderer)", 1)}
STATE = r"""(() => { const p = player.obj.position, r = v => Math.round(v * 1e4);
  const sv = JSON.parse(localStorage.getItem('starship-cadet-save-dev') || 'null'); if (sv && sv.ship && sv.ship.career) sv.ship.career.gs = 'x';   // gs: a new game's own seed (Date.now, Math.random), different every game
  return { save: JSON.stringify(sv), t: shipNow(), deck: deckDef.num, at: [r(p.x), r(p.z)],
    walk: walkers.map(w => [w.spec.name, r(w.obj.position.x), r(w.obj.position.z), w.goal]) }; })()"""
out = {}
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    for tag, html in B.items():
        ctx = b.new_context(viewport={'width': 390, 'height': 844}); errs = []
        tmp = WORK / 'test' / f'_speed_{tag}.html'; tmp.write_text(instrument(html))
        pg = ctx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: m.type == 'error' and errs.append(m.text))
        pg.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript')); pg.add_init_script(INIT)
        ev = lambda s: pg.evaluate('s => window.__sc(s)', s)
        step = lambda n: pg.evaluate(f'window.__step({n}, {1000 / 30})')
        pg.goto('file://' + str(tmp) + '#dev'); pg.wait_for_function('window.__sc !== undefined', timeout=90000); ev("(() => { const rr = renderer.render.bind(renderer); renderer.render = (s, c) => { if (window.__draw) rr(s, c); }; })()"); step(20)   # no drawing (devmode_check's way), after the card's wrapper
        if pg.locator('text=Sign and go aboard').count(): pg.fill('form input', 'Ada'); pg.click('text=Sign and go aboard'); step(30)
        step(600); ev('goToDeck(3)'); step(200); ev('goToDeck(4)'); step(600)
        out[tag] = ev(STATE); out[tag]['errs'] = errs[:]
        (WORK / 'test' / f'_speed_save_{tag}.json').write_text(out[tag]['save'] or '')
        if tag == 'card':
            pg.evaluate('window.__draw = true'); ev('DM_UI.open = true; DM_UI.tab = "speed"; devmodeDraw()'); step(40)
            lines = {}
            for w, h in ((390, 844), (844, 390), (412, 960)):
                pg.set_viewport_size({'width': w, 'height': h}); step(40); ev('devmodeSpeedText()')
                lines[f'{w}x{h}'] = ev("document.getElementById('dmSpeed').textContent")
            out['lines'] = lines
            out['copy'] = ev("typeof devmodeSpeedLines() === 'object' && devmodeSpeedLines().length")
            ev("DM_SPEED.fr = []; DM_SPEED.k = 0"); step(5); out['restart'] = ev('DM_SPEED.fr.length')
            out['errs2'] = errs[:]
        ctx.close()
    ctx = b.new_context(viewport={'width': 390, 'height': 844}); pg = ctx.new_page(); tmp = WORK / 'test' / '_speed_card.html'
    pg.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript')); pg.add_init_script(INIT)
    pg.goto('file://' + str(tmp)); pg.wait_for_function('window.__sc !== undefined', timeout=90000)
    out['off'] = pg.evaluate("s => window.__sc(s)", "[DEVMODE, /rr\\(sc, cam\\)/.test(renderer.render.toString()), /cb !== loop/.test(window.requestAnimationFrame.toString()), /go\\.apply/.test(goToDeck.toString()), DM_SPEED.sizes.length]")
    ctx.close(); b.close()
a, c = out['bare'], out['card']
for k in ('save', 't', 'deck', 'at', 'walk'):
    print(k, 'SAME' if a[k] == c[k] else 'DIFFERS', hashlib.md5(json.dumps(a[k]).encode()).hexdigest()[:10], hashlib.md5(json.dumps(c[k]).encode()).hexdigest()[:10])
print('errors bare', a['errs'][:3], 'card', out['errs2'][:3])
for k, v in out['lines'].items(): print('==', k); print(v)
print('lines', out['copy'], 'after Start again + 5 frames:', out['restart'], 'off (DEVMODE, render wrapped, rAF wrapped, goToDeck wrapped, sizes):', out['off'])
same = all(a[k] == c[k] for k in ('save', 't', 'deck', 'at', 'walk'))
sizes = all(s in out['lines']['412x960'] for s in ('390 x 844', '844 x 390', '412 x 960'))
print('SPEED PROBE OK' if same and sizes and not out['errs2'] and out['off'] == [False, False, False, False, 0] and a['save'] else 'SPEED PROBE FAILED')
