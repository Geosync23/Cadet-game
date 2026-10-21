# Real time spent inside WebGL calls during load, by call (wraps the context prototypes before the game starts)
import sys, os, time, re, json
src = open('/home/user/Cadet-game/cadet_test.py').read().split("import sys, json, hashlib")[0]
exec(src)
WRAP = """(() => { const now = performance.now.bind(performance); window.__rn = now; window.__glt = {}; window.__t0 = now();
  for (const C of [WebGLRenderingContext, WebGL2RenderingContext]) for (const k of Object.getOwnPropertyNames(C.prototype)) {
    const d = Object.getOwnPropertyDescriptor(C.prototype, k); if (!d || typeof d.value !== 'function') continue; const f = d.value;
    C.prototype[k] = function () { const a = now(); try { return f.apply(this, arguments); } finally { const e = window.__glt[k] || (window.__glt[k] = [0, 0]); e[0] += now() - a; e[1]++; } };
  }
  document.addEventListener('DOMContentLoaded', () => { window.__dcl = now(); });
})();"""
from playwright.sync_api import sync_playwright
f = sys.argv[1]; vw, vh = int(sys.argv[2]), int(sys.argv[3])
html = instrument(pathlib.Path(f).read_text())
# mark the script start and end of kit and deck build with real time: inject after the IIFE opens and before loop() is first called
html = html.replace("(() => {\n/* ====", "(() => { window.__js0 = window.__rn();\n/* ====", 1)
html = html.replace("drawScreen(0); applyLight(0); loop();", "window.__js1 = window.__rn(); drawScreen(0); applyLight(0); window.__js2 = window.__rn(); loop(); window.__js3 = window.__rn();", 1)
tmp = WORK / 'test' / '_gl.html'; tmp.write_text(html)
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME'), args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    page = b.new_page(viewport={'width': vw, 'height': vh}, device_scale_factor=1)
    page.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
    page.add_init_script(WRAP); page.add_init_script(INIT)
    t0 = time.time(); page.goto('file://' + str(tmp) + '?nosave&debug', wait_until='commit')
    page.wait_for_function('window.__sc !== undefined', timeout=120000, polling=50); t1 = time.time()
    r = page.evaluate("() => ({ js0: __js0 - __t0, js1: __js1 - __t0, js2: __js2 - __t0, js3: __js3 - __t0, dcl: (window.__dcl || 0) - __t0, gl: __glt })")
    print(f'{f} {vw}x{vh} wall {t1-t0:.2f}s')
    print(f"  script starts {r['js0']/1e3:.2f}s (HTML + three.js + parse/compile of the game script before it runs)")
    print(f"  kit + deck build + everything at load: {(r['js1']-r['js0'])/1e3:.2f}s")
    print(f"  first frame (loop + render): {(r['js3']-r['js2'])/1e3:.2f}s")
    gl = sorted(r['gl'].items(), key=lambda kv: -kv[1][0])
    print('  WebGL time ' + f"{sum(v[0] for v in r['gl'].values())/1e3:.2f}s: " + ', '.join(f'{k} {v[0]/1e3:.2f}s x{v[1]}' for k, v in gl[:8]))
    b.close()
