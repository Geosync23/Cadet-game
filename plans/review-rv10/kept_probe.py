# RV10: which days carry 'kept' split seats, and where lead() would have cut them (four weeks of plans, on paper)
import sys, os, re, pathlib, json
GAME, CT = sys.argv[1], sys.argv[2]
exec(open(CT + '/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    g = Game(pw, GAME, 390, 844)
    r = g.ev("""(() => { const out = {};
      for (let d = 0; d <= 28; d++) { const P = shipDay(d).plans; let n = 0, ex = [];
        for (const [id, segs] of P) segs.forEach((s, i) => { if (s.kept) { n++; if (ex.length < 3) ex.push([id, s.from % 1440, s.to % 1440, s.act, s.placeId, (segs[i + 1] || {}).act]); } });
        if (n) out[d] = [n, ex]; }
      return out; })()""")
    print(json.dumps(r))
    g.close()
