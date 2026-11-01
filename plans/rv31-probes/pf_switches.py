# RV31: PF1's four picture switches. A fresh page (device pixel ratio 2) with no token, #pfpr.pfsh.pfcap.pfaa, #pfcap-30:
# pixel ratio, shadow map size, antialias, renders in 120 frames of a 120 Hz screen, ship clock moves, no page errors.
#   python3 plans/rv31-probes/pf_switches.py BUILD.html
import sys
exec(open('cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
Q = "[renderer.getPixelRatio(), sun.shadow.mapSize.x, renderer.getContext().getContextAttributes().antialias, shipNow()]"
html = instrument(pathlib.Path(sys.argv[1]).read_text()); tmp = WORK / 'test' / '_rv31_pfsw.html'; tmp.write_text(html)
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    errs = []
    for h in ('', '#pfpr.pfsh.pfcap.pfaa', '#pfcap-30'):
        p = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2); p.on('pageerror', lambda e: errs.append(str(e)))
        p.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript')); p.add_init_script(INIT)
        p.goto('file://' + str(tmp) + '?nosave&debug' + h); p.wait_for_function('window.__sc !== undefined', timeout=60000)
        ev = lambda s: p.evaluate('s => window.__sc(s)', s)
        a = ev(Q); ev("window.__n = 0; (() => { const r = renderer.render.bind(renderer); renderer.render = (s, c) => { window.__n++; r(s, c); }; })()")
        p.evaluate("window.__step(120, 1000/120)")
        print(h or '(none)', 'pixelRatio, shadow, antialias:', a[:3], '| renders in 120 frames at 120 Hz:', ev('window.__n'), '| clock moved:', round(ev('shipNow()') - a[3], 2))
        p.close()
    print('page errors', errs[:3]); b.close()
tmp.unlink()
