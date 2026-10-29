# RV27: title music level over time after the real wake tap (an analyser on SND.bus.master), 1 s steps.
# Usage: CADET_WORK=... CADET_CHROME=... python3 tm_level.py GAME [seconds]
import os, sys, pathlib, time, re
from playwright.sync_api import sync_playwright
GAME = pathlib.Path(sys.argv[1]); SECS = int(sys.argv[2]) if len(sys.argv) > 2 else 40
WORK = pathlib.Path(os.environ.get('CADET_WORK', '/tmp/cadet-work'))
THREE = (WORK / 'three/package/build/three.min.js').read_text()
src = GAME.read_text()
i = src.rfind('})();'); src = src[:i] + "window.__sc = s => eval(s);\n" + src[i:]
f = WORK / 'test' / f'_tml_{os.getpid()}.html'; f.write_text(src)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get('CADET_CHROME'), args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    pg = b.new_page(viewport={'width': 390, 'height': 844}); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
    pg.goto('file://' + str(f) + '?title&nosave&sound')
    pg.wait_for_function('window.__sc !== undefined', timeout=120000); time.sleep(2)
    print('before', pg.evaluate('s => window.__sc(s)', '[document.getElementById("title").className, SND.ctx ? SND.ctx.state : null]'))
    pg.mouse.click(195, 420)   # the wake tap (a real gesture)
    t0 = time.time(); pg.wait_for_function('window.__sc("!!SND.ctx")', timeout=20000); print('ctx at', round(time.time() - t0, 1))
    pg.evaluate('s => window.__sc(s)', "(() => { const a = SND.ctx.createAnalyser(); a.fftSize = 8192; SND.bus.master.connect(a); window.__an = a; window.__buf = new Float32Array(a.fftSize); })()")
    rows = []
    while time.time() - t0 < SECS:
        r = pg.evaluate('s => window.__sc(s)', "(() => { __an.getFloatTimeDomainData(__buf); let s = 0; for (const v of __buf) s += v * v; const db = 10 * Math.log10(s / __buf.length + 1e-12); return [+db.toFixed(1), document.getElementById('title').className, SND.ctx.state, +SND.ctx.currentTime.toFixed(1), SND.titleOn]; })()")
        rows.append((round(time.time() - t0, 1), r)); print(rows[-1], flush=True); time.sleep(1)
    print('errors', errs[:3]); b.close()
f.unlink(missing_ok=True)
