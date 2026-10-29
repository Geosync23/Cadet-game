# OP1: a scratch copy where grain() during load only records (canvas, seed) and jumps the seed ahead exactly
# (Lehmer: seed' = seed * 16807^pixels mod 2^31-1), then all the noise is added in one batch just before the first
# frame. Same seeds, same noise; prints the load split and a hash of every grained canvas's pixels for both builds.
import sys, os, re, time, json
src = open('/home/user/Cadet-game/cadet_test.py').read().split("import sys, json, hashlib")[0]
exec(src)
from playwright.sync_api import sync_playwright
G = pathlib.Path(sys.argv[1]).read_text()
OLD = "function grain(g, w, h, amt) {\n"
assert G.count(OLD) == 1
NEW = """const GRAIN_LATER = []; let GRAIN_DEFER = true;
function grainJump(s, n) { let r = 1n, b = 16807n, e = BigInt(n), m = 2147483647n; while (e > 0n) { if (e & 1n) r = r * b % m; b = b * b % m; e >>= 1n; } return Number(BigInt(s) * r % m); }
let GRAIN_FL = false; function grainFlush() { GRAIN_DEFER = false; GRAIN_FL = true; const q = GRAIN_LATER.splice(0); for (const [g, w, h, amt, s] of q) { const k = seed; seed = s; grain(g, w, h, amt); seed = k; } GRAIN_FL = false; }
function grain(g, w, h, amt) {
  if (GRAIN_DEFER) { GRAIN_LATER.push([g, w, h, amt, seed]); seed = grainJump(seed, w * h); window.__gc = (window.__gc || []).concat([g]); return; }
  if (!GRAIN_FL) window.__gc = (window.__gc || []).concat([g]);
"""
B = G.replace(OLD, NEW).replace("drawScreen(0); applyLight(0); loop();", "grainFlush(); drawScreen(0); applyLight(0); loop();", 1)
A = G.replace(OLD, OLD.replace('{\n', '{ window.__gc = (window.__gc || []).concat([g]);\n'))
WRAP = """(() => { const now = performance.now.bind(performance); window.__t0 = now(); window.__rn = now; })();"""
HASH = """(() => { let out = []; for (const g of window.__gc) { const d = g.getImageData(0, 0, g.canvas.width, g.canvas.height).data; let h = 0; for (let i = 0; i < d.length; i++) h = (h * 31 + d[i]) | 0; out.push(h); } return [out.length, out.join(',')]; })()"""
for name, html in (('A', A), ('B', B)): (WORK / 'test' / f'_gd_{name}.html').write_text(instrument(html.replace("drawScreen(0); applyLight(0); loop();", "window.__js1 = window.__rn(); drawScreen(0); applyLight(0); loop(); window.__js3 = window.__rn();", 1)))
with sync_playwright() as pw:
    res = {'A': [], 'B': []}; hashes = {}
    for k in range(int(sys.argv[2]) if len(sys.argv) > 2 else 4):
        for name in ('A', 'B') if k % 2 == 0 else ('B', 'A'):
            b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME'), args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
            page = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
            page.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
            page.add_init_script(WRAP); page.add_init_script(INIT)
            t0 = time.time(); page.goto('file://' + str(WORK / 'test' / f'_gd_{name}.html') + '?nosave&debug', wait_until='commit')
            page.wait_for_function('window.__sc !== undefined', timeout=120000, polling=50); t1 = time.time()
            r = page.evaluate("() => [__js1 - __t0, __js3 - __js1]")
            res[name].append((round(t1 - t0, 2), round(r[0] / 1e3, 2), round(r[1] / 1e3, 2)))
            if name not in hashes: hashes[name] = page.evaluate("() => window.__sc(" + json.dumps(HASH) + ")")
            b.close()
    for n in 'AB': print(n, 'wall / script to first frame / first frame (s):', res[n])
    print('grained canvases', hashes['A'][0], hashes['B'][0], 'pixels identical:', hashes['A'] == hashes['B'])
