# Does a persistent browser profile keep compiled shaders between launches (Chrome's GPU shader disk cache)?
import sys, os, re, time, shutil
src = open('/home/user/Cadet-game/cadet_test.py').read().split("import sys, json, hashlib")[0]
exec(src)
from playwright.sync_api import sync_playwright
ARGS = ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist']
html = instrument(pathlib.Path(sys.argv[1]).read_text()); tmp = WORK / 'test' / '_sc.html'; tmp.write_text(html)
UD = '/tmp/opt-ud'; shutil.rmtree(UD, ignore_errors=True)
def once(pw, persistent, extra=[]):
    if persistent: ctx = pw.chromium.launch_persistent_context(UD, executable_path=os.environ.get('CADET_CHROME'), args=ARGS + extra, viewport={'width': 900, 'height': 760}, device_scale_factor=1); page = ctx.pages[0] if ctx.pages else ctx.new_page()
    else: b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME'), args=ARGS + extra); ctx = b; page = b.new_page(viewport={'width': 900, 'height': 760}, device_scale_factor=1)
    page.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
    page.add_init_script(INIT)
    t = time.time(); page.goto('file://' + str(tmp) + '?nosave&debug'); page.wait_for_function('window.__sc !== undefined', timeout=120000, polling=50); a = time.time() - t
    # a deck change and one drawn frame (new materials compile)
    t = time.time(); page.evaluate("() => { window.__sc('goToDeck(3)'); window.__step(1, 33); }"); d = time.time() - t
    ctx.close(); return round(a, 1), round(d, 1)
with sync_playwright() as pw:
    print('fresh profile each time:', [once(pw, False) for _ in range(2)])
    print('persistent profile:', [once(pw, True) for _ in range(3)])
    shutil.rmtree(UD, ignore_errors=True)
    print('persistent + --enable-gpu-shader-disk-cache:', [once(pw, True, ['--enable-gpu-shader-disk-cache']) for _ in range(3)])
