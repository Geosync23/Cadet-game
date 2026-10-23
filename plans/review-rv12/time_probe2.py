# RV12: real time of rebuilding Day 0's plans (5 rebuilds per ev, timed from Python), plain vs live goodnight
import sys, time
GAME, CT = sys.argv[1], sys.argv[2]
exec(open(CT + '/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    g = Game(pw, GAME, 390, 844); g.step(3)
    g.ev("localStorage.clear()"); g.ev("newGameStart(true)"); g.step(5)
    try: g.page.fill('form input[maxlength="24"]', 'Sam'); g.page.click('form button'); g.step(5)
    except Exception as e: print('sign:', str(e)[:80])
    g.ev("window.__k = SHIP.intro.done.free")
    out = {}
    for name, js in [('plain', "delete SHIP.intro.done.free"), ('free1910', "SHIP.intro.done.free = -1440 + 1150"), ('free1820', "SHIP.intro.done.free = -1440 + 1100"), ('plain2', "delete SHIP.intro.done.free")]:
        g.ev(js); r = []
        for rep in range(3):
            t = time.perf_counter(); g.ev("(() => { for (let i = 0; i < 5; i++) { SHIP_DAYS.delete(0); shipDay(0); } return 1; })()"); r.append(round((time.perf_counter() - t) / 5 * 1000))
        out[name] = r
    g.ev("if (__k === undefined) delete SHIP.intro.done.free; else SHIP.intro.done.free = __k; SHIP_DAYS.delete(0)")
    print('ms per Day 0 rebuild:', out)
    g.close()
