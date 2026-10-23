# RV12: wall-clock cost of rebuilding Day 0's plans with and without the live goodnight (Date.now, not the virtual clock)
import sys
GAME, CT = sys.argv[1], sys.argv[2]
exec(open(CT + '/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    g = Game(pw, GAME, 390, 844); g.step(3)
    g.ev("localStorage.clear()"); g.ev("newGameStart(true)"); g.step(5)
    try: g.page.fill('form input[maxlength="24"]', 'Sam'); g.page.click('form button'); g.step(5)
    except Exception as e: print('sign:', str(e)[:80])
    r = g.ev("""(() => { const out = {};
      const time = () => { const a = []; for (let i = 0; i < 5; i++) { SHIP_DAYS.delete(0); const t = Date.now(); shipDay(0); a.push(Date.now() - t); } return a; };
      const k = SHIP.intro.done.free; delete SHIP.intro.done.free; out.plain = time();
      SHIP.intro.done.free = -1440 + 1150; out.free1910 = time();
      SHIP.intro.done.free = -1440 + 1100; out.free1820 = time();
      if (k === undefined) delete SHIP.intro.done.free; else SHIP.intro.done.free = k; SHIP_DAYS.delete(0);
      out.introOn = typeof introOn === 'function' && introOn(); return out; })()""")
    print(r)
    g.close()
