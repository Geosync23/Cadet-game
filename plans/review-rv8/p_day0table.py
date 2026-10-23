# RV8 probe: Day 0's Sunday table, seated count every 5 minutes 18:00-20:10 (the table's seats, tagged or not). p_day0table.py GAME CT_DIR
import sys
exec(open(sys.argv[2] + '/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 900, 760); g.step(3)
    r = g.ev(r"""(() => { const d = 0, B = (d - 1) * 1440, day = shipDay(d), pl = new Set(), out = [];
      for (const [, segs] of day.plans) for (const s of segs) if (s.tag && /^ev-sunday-table/.test(s.tag) && s.placeId) pl.add(s.placeId);
      for (let m = 18 * 60; m <= 20 * 60 + 10; m += 5) { let n = 0; for (const [, segs] of day.plans) if (segs.some(s => pl.has(s.placeId) && s.from <= B + m && s.to > B + m)) n++; out.push(String(Math.floor(m / 60)) + ':' + String(m % 60).padStart(2, '0') + ' ' + n); }
      return [pl.size, out.join('  ')]; })()""")
    print('table seats', r[0]); print(r[1]); g.close()
