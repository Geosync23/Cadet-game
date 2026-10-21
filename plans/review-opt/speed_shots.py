# OR1: the Dev sheet's Speed tab at phone sizes (390x844, 360x740, the TriFold folded 412x960 and turned 960x412).
#   python3 speed_shots.py BUILD.html OUTDIR
import sys, os, re, pathlib
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("import sys, json, hashlib")[0])
from playwright.sync_api import sync_playwright
OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
tmp = WORK / 'test' / '_speed_shots.html'; tmp.write_text(instrument(pathlib.Path(sys.argv[1]).read_text()))
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    for w, h in ((390, 844), (360, 740), (412, 960), (960, 412)):
        ctx = b.new_context(viewport={'width': w, 'height': h}); pg = ctx.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript')); pg.add_init_script(INIT)
        pg.goto('file://' + str(tmp) + '#dev'); pg.wait_for_function('window.__sc !== undefined', timeout=90000)
        pg.evaluate('window.__step(20, 33)')
        if pg.locator('text=Sign and go aboard').count(): pg.fill('form input', 'Ada'); pg.click('text=Sign and go aboard'); pg.evaluate('window.__step(30, 33)')
        pg.click('.hud'); pg.evaluate('window.__step(2, 33)'); pg.click('#dmSheet .dmTabs button[data-tab="speed"]'); pg.evaluate('window.__step(40, 33)')
        over = pg.evaluate("(() => { const s = document.getElementById('dmSheet').getBoundingClientRect(); return [...document.querySelectorAll('#dmSheet *')].filter(e => { const r = e.getBoundingClientRect(); return r.width && (r.right > innerWidth + .5 || r.left < -.5); }).map(e => e.tagName + '.' + e.className).slice(0, 5); })()")
        tabs = pg.evaluate("[...document.querySelectorAll('#dmSheet .dmTabs button')].map(b => { const r = b.getBoundingClientRect(); return [b.textContent, Math.round(r.left), Math.round(r.top), Math.round(r.width), Math.round(r.height)]; })")
        pg.screenshot(path=f'{OUT}/speed_{w}x{h}.png'); print(w, h, 'tabs', tabs, 'wider than the screen:', over, 'errors', errs[:2], flush=True); ctx.close()
    b.close()
