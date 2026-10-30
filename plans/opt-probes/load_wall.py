import sys, os, time
src = open('/home/user/Cadet-game/cadet_test.py').read().split("import sys, json, hashlib")[0]
exec(src)
from playwright.sync_api import sync_playwright
for f in sys.argv[1:]:
    for k in range(3):
        with sync_playwright() as pw:
            t0 = time.time(); g = Game(pw, f); t1 = time.time()
            g.page.reload(); g.page.wait_for_function('window.__sc !== undefined', timeout=120000, polling=50); t2 = time.time()
            # first steps on the fresh page (shaders for crowd etc.)
            g.step(30); t3 = time.time(); g.step(30); t4 = time.time()
            calls = g.ev('renderer.info.render.calls')
            print(f'{f}: open {t1-t0:.1f}s reload {t2-t1:.1f}s step30#1 {t3-t2:.1f}s step30#2 {t4-t3:.2f}s calls {calls}', flush=True)
            g.close()
