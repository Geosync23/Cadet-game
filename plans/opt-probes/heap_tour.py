# opt #5: the JS heap (after a full GC, CDP Runtime.getHeapUsage) after load and after each deck, two tours; plus the
# GPU-side counts. Shows which first visits keep memory.
import sys, os, re, json
src = open('/home/user/Cadet-game/cadet_test.py').read().split("import sys, json, hashlib")[0]
exec(src)
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844); g.ev("window.__realTick = tickShip; tickShip = () => {}")
    cdp = g.page.context.new_cdp_session(g.page)
    def heap():
        cdp.send('HeapProfiler.collectGarbage'); cdp.send('HeapProfiler.collectGarbage')
        u = cdp.send('Runtime.getHeapUsage'); m = g.ev('[renderer.info.memory.geometries, renderer.info.memory.textures, renderer.info.programs.length]')
        pm = g.page.evaluate('performance.memory ? [performance.memory.usedJSHeapSize, performance.memory.totalJSHeapSize] : null')
        ab = g.ev("(() => { let n = 0, b = 0; const seen = new Set(); return null; })()")
        return round(u['usedSize'] / 1048576, 1), m, {k: round(v / 1048576, 1) for k, v in u.items()}, [round(x / 1048576, 1) for x in pm] if pm else None
    prev = heap()[0]; print('after load', heap())
    for lap in (1, 2):
        for n in (3, 5, 2, 1, 6, 7, 4):
            g.ev(f'goToDeck({n})'); g.step(3); h, m, u, pm = heap(); print(f'lap {lap} D{n}: heap {h} MB ({h - prev:+.1f}), geo/tex/progs {m}, usage {u}, performance.memory {pm}', flush=True); prev = h
    g.close()
