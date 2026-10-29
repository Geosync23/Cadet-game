# RV26: SD3 title music in a real flow on a copy with the title switched on (TITLE_ON / TITLE_EARLY true).
import os, sys, json, pathlib, time, re
from playwright.sync_api import sync_playwright
GAME = pathlib.Path(sys.argv[1]); WORK = pathlib.Path(os.environ.get('CADET_WORK', '/tmp/cadet-work'))
THREE = (WORK / 'three/package/build/three.min.js').read_text()
src = GAME.read_text().replace('const TITLE_ON = false;', 'const TITLE_ON = true;').replace('const TITLE_EARLY = false;', 'const TITLE_EARLY = true;')
i = src.rfind('})();'); src = src[:i] + "window.__sc = s => eval(s);\n" + src[i:]
f = WORK / 'test' / f'_tm_{os.getpid()}.html'; f.write_text(src)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get('CADET_CHROME'), args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--autoplay-policy=no-user-gesture-required'])
    pg = b.new_page(viewport={'width': 390, 'height': 844}); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
    pg.goto('file://' + str(f) + '?title&nosave&sound&soundlog')
    pg.wait_for_function('window.__sc !== undefined', timeout=90000); time.sleep(2)
    S = "[document.getElementById(\"title\").className, (TITLE.music ? 1 : 0), window.__mk || 0, SND.ctx ? +SND.ctx.currentTime.toFixed(2) : null, typeof INTRO !== 'undefined' ? 1 : 0, PAUSE.on, TITLE.on, FREEZE.frozen, SND.bus && SND.bus.hum ? +SND.bus.hum.gain.value.toFixed(4) : null, SND.ctx ? SND.ctx.state : null, SND.titleOn, SND.titleSnd.list.length, SND.titleSnd.hush, SND.log ? SND.log.filter(x => /^title|^hum/.test(x.name)).map(x => x.name) : null, hhmm(SHIP.time.min)]"
    pg.evaluate('window.__mk = 1'); print('loaded', pg.evaluate('s => window.__sc(s)', S))
    pg.mouse.click(195, 120); time.sleep(0.4); print('0.4s', pg.evaluate('s => window.__sc(s)', S)); time.sleep(3.6)   # a tap on the title (not a button)
    print('tapped', pg.evaluate('s => window.__sc(s)', S))
    time.sleep(6); print('later', pg.evaluate('s => window.__sc(s)', S))
    pg.click('#tiNew')
    for k in range(6): time.sleep(2); print('new game +' + str(2 * k + 2), pg.evaluate('s => window.__sc(s)', S))
    print('errors', errs[:3]); b.close()
f.unlink(missing_ok=True)
