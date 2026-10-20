import sys, os, time, json
os.environ.setdefault('CADET_CHROME','/opt/pw-browsers/chromium')
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844); g.step(3)
    for d in [5, 3, 4, 5, 4]:
        t0 = time.time(); g.ev(f"goToDeck({d})"); print('goToDeck', d, round(time.time()-t0, 2), 's')
    print(g.ev("(() => { const c = SHIP.career || careerInit(); return { leave: c.l, max: CAREER.max, every: CAREER.every }; })()"))
    g.close()
