import sys
src = open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..', '..', 'cadet_test.py')).read().split("a, shots = run(")[0]
sv = sys.argv; sys.argv = ['x']; exec(src); sys.argv = sv
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1])
    g.ev("skipTo(6*1440+18*60+25); goToDeck(3)"); g.step(150)
    print(g.ev("""(() => { let n = 0, tt = 0; const f = SEAT_RC.rc.intersectObjects.bind(SEAT_RC.rc); SEAT_RC.rc.intersectObjects = (...a) => { n++; return f(...a); };
      const now = () => Performance.prototype.now.call(performance); const ag = DECK_CREW.find(a => a.settled && a.spot && a.spot.pose === "sit"); let tm = []; for (let k = 0; k < 5; k++) { ag.h.cush = null; const t0 = now(); seatCushion(ag.h, ag.spot.y || .475); tm.push(+(now() - t0).toFixed(2)); } window.__tm = tm;
      let sig = 0; const tk = tableTrays.tick.bind(tableTrays); let changes = 0, last = tableTrays.sig; tableTrays.tick = () => { tk(); if (tableTrays.sig !== last) { changes++; last = tableTrays.sig; } };
      window.__skip = true; window.__step(300, 1000 / 30); window.__skip = false; return JSON.stringify({ rayMs: __tm, raysPerFrame: n / 300, trayChanges: changes, list: SEAT_RC.list && SEAT_RC.list.length }); })()"""))
    g.close()
