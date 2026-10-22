import sys, re, pathlib, json
from playwright.sync_api import sync_playwright
EX = pathlib.Path('/tmp/cadet-work/three/package')
PAGE = (pathlib.Path(__file__).parent / '../tea-corner-look-test.html').read_text()
SKEL = '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"></head><body>' + PAGE + '</body></html>'
pathlib.Path('/tmp/cadet-work/lt.html').write_text(SKEL)
def route(r):
    u = r.request.url
    if 'three.min.js' in u: return r.fulfill(path=str(EX / 'build/three.min.js'), content_type='application/javascript')
    m = re.search(r'three@0\.128\.0/(examples/js/.*\.js)', u)
    if m: return r.fulfill(path=str(EX / m.group(1)), content_type='application/javascript')
    if 'fonts.g' in u: return r.abort()
    return r.continue_()
sizes = [tuple(map(int, s.split('x'))) for s in (sys.argv[1] if len(sys.argv) > 1 else '412x960').split(',')]
levels = [int(c) for c in (sys.argv[2] if len(sys.argv) > 2 else '012')]
cam = sys.argv[3] if len(sys.argv) > 3 else 'close'
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path='/opt/pw-browsers/chromium', args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    for (w, h) in sizes:
        p = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=1)
        errs = []
        p.on('console', lambda m: m.type in ('error', 'warning') and errs.append(m.text))
        p.on('pageerror', lambda e: errs.append(str(e)))
        p.route('**/*', route)
        p.goto('file:///tmp/cadet-work/lt.html')
        p.wait_for_function('window.__look', timeout=60000)
        p.evaluate(f"__look.setCam('{cam}')")
        for lv in levels:
            p.evaluate(f'__look.setLevel({lv})'); p.wait_for_timeout(2500)
            p.screenshot(path=f'L{lv}_{w}x{h}_{cam}.png')
            print(w, h, lv, json.dumps(p.evaluate('__look.stats()')))
        print('errors', errs[:6])
        p.close()
    b.close()
