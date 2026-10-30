# opt #8: the Speed card in Dev mode at the phone and TriFold sizes: open the sheet, the Speed tab, frames drawn, text + shot
import sys, os, re, json, pathlib
src = open('/home/user/Cadet-game/cadet_test.py').read().split("import sys, json, hashlib")[0]
exec(src)
from playwright.sync_api import sync_playwright
OUT = pathlib.Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
TMP = WORK / 'test' / '_speed.html'; TMP.write_text(instrument(pathlib.Path(sys.argv[1]).read_text()))
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    for (w, h, dpr) in [tuple(float(v) if '.' in v else int(v) for v in x.split('x')) for x in (sys.argv[3].split(',') if len(sys.argv) > 3 else ['390x844x3', '412x960x2.625', '792x1080x2'])]:
        ctx = b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=dpr); pg = ctx.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: m.type == 'error' and errs.append(m.text))
        pg.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
        pg.add_init_script(INIT); pg.goto('file://' + str(TMP) + '#dev'); pg.wait_for_function('window.__sc !== undefined', timeout=90000)
        pg.add_style_tag(content='*,*::before,*::after{transition:none!important;animation:none!important}')
        ev = lambda s: pg.evaluate('s => window.__sc(s)', s)
        pg.evaluate('window.__step(10, 1000 / 30)')
        if pg.locator('text=Sign and go aboard').count(): pg.fill('form input', 'Ada'); pg.click('text=Sign and go aboard'); pg.evaluate('window.__step(30, 1000 / 30)')
        ev('goToDeck(3)'); pg.evaluate('window.__step(20, 1000 / 30)')
        ev('devmodeOpen(true); DM_UI.tab = "speed"; devmodeDraw()'); pg.evaluate('window.__step(40, 1000 / 30)')
        if w == 390:   # turn the phone: a second size in the list
            pg.set_viewport_size({'width': h, 'height': w}); pg.evaluate('window.__step(10, 1000 / 30)'); pg.set_viewport_size({'width': w, 'height': h}); pg.evaluate('window.__step(40, 1000 / 30)')
        txt = ev('devmodeSpeedLines().join("\\n")')
        pg.screenshot(path=str(OUT / f'speed-{w}x{h}.png'), scale='css', timeout=180000)
        print(f'== {w}x{h} dpr {dpr}', 'errors', errs[:3]); print(txt)
        ctx.close()
    b.close()
