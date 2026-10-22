# RV6: load time and JS heap without #dev, for a build with and without DM_DAYS (5 loads each, alternating)
import sys, os, re, pathlib, time
from playwright.sync_api import sync_playwright
WORK = pathlib.Path(os.environ.get('CADET_WORK', '/tmp/cadet-work')); THREE = (WORK / 'three/package/build/three.min.js').read_text()
builds = sys.argv[1:]
res = {b: [] for b in builds}
with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--enable-precise-memory-info', '--js-flags=--expose-gc'])
    for k in range(5):
        for bp in builds:
            ctx = br.new_context(viewport={'width': 390, 'height': 844}); pg = ctx.new_page()
            pg.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
            t0 = time.time(); pg.goto('file://' + os.path.abspath(bp)); pg.wait_for_load_state('load'); t1 = time.time()
            pg.wait_for_timeout(1500)
            nav = pg.evaluate("(() => { const n = performance.getEntriesByType('navigation')[0]; return [Math.round(n.domContentLoadedEventEnd), Math.round(n.loadEventEnd)]; })()")
            heap = pg.evaluate("(() => { if (window.gc) gc(); return performance.memory ? performance.memory.usedJSHeapSize : null; })()")
            dm = pg.evaluate("typeof DEVMODE !== 'undefined' ? DEVMODE : 'n/a'")
            res[bp].append((nav, heap)); print(os.path.basename(bp), 'dcl/load ms', nav, 'heap MB', round(heap / 1e6, 2), 'devmode', dm, flush=True)
            ctx.close()
for bp, r in res.items():
    import statistics as st
    print(os.path.basename(bp), 'median load ms', st.median(x[0][1] for x in r), 'median heap MB', round(st.median(x[1] for x in r) / 1e6, 2), 'file KB', os.path.getsize(bp) // 1024)
