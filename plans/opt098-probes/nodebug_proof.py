# OP1, 0.98 turn 1: open OLD and NEW without ?debug (the way a player does; every check uses ?debug), alternating, and
# compare: the time to the first picture, the shader-check setting, and the picture itself after 60 frames (pixel for pixel).
#   python3 nodebug_proof.py OLD.html NEW.html [ROUNDS]
import sys, os, re, time, io
src = open('/home/user/Cadet-game/cadet_test.py').read().split("import sys, json, hashlib")[0]; exec(src)
from playwright.sync_api import sync_playwright
import numpy as np
from PIL import Image
WRAP = "(() => { const now = performance.now.bind(performance); window.__t0 = now(); window.__rn = now; })();"
paths = {}
for tag, f in (('OLD', sys.argv[1]), ('NEW', sys.argv[2])):
    h = instrument(pathlib.Path(f).read_text()).replace("drawScreen(0); applyLight(0); loop();", "window.__js1 = window.__rn(); drawScreen(0); applyLight(0); loop(); window.__js3 = window.__rn();", 1)
    paths[tag] = WORK / 'test' / f'_nd_{tag}.html'; paths[tag].write_text(h)
res = {'OLD': [], 'NEW': []}; shots = {}
with sync_playwright() as pw:
    for k in range(int(sys.argv[3]) if len(sys.argv) > 3 else 4):
        for tag in (('OLD', 'NEW') if k % 2 == 0 else ('NEW', 'OLD')):
            b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME'), args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
            page = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
            page.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
            page.add_init_script(WRAP); page.add_init_script(INIT)
            page.goto('file://' + str(paths[tag]) + '?nosave', wait_until='commit')
            page.wait_for_function('window.__sc !== undefined', timeout=120000, polling=50)
            ff, chk = page.evaluate("() => [__js3 - __js1, window.__sc('renderer.debug.checkShaderErrors')]")
            res[tag].append((round(ff / 1e3, 2), chk))
            if tag not in shots:
                page.add_style_tag(content='#toast,.nf{opacity:0!important} *,*::before,*::after{transition:none!important;animation:none!important}')
                page.evaluate("window.__step(60, 1000 / 30)")
                import base64; cdp = page.context.new_cdp_session(page); shots[tag] = np.asarray(Image.open(io.BytesIO(base64.b64decode(cdp.send('Page.captureScreenshot', {'format': 'png'})['data']))).convert('RGB')).astype(int)
            b.close()
for t in res: print(t, 'first picture s / shader checks:', res[t])
d = np.abs(shots['OLD'] - shots['NEW'])
print('picture after 60 frames, no ?debug:', 'IDENTICAL' if d.max() == 0 else f'{(d.max(axis=2) > 0).sum()} pixels differ, max {d.max()}')
