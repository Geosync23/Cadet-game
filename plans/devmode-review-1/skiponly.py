import sys, os, json
os.environ.setdefault('CADET_CHROME','/opt/pw-browsers/chromium')
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844); g.step(3)
    r = g.ev(r"""(() => { const o = [];
      for (let d = 1; d <= 30; d++) { for (let m = 360; m <= 1380; m += 30) { const t = (d - 1) * 1440 + m; if (t > shipNow()) skipTo(t); }
        const c = SHIP.career; o.push([d, c.ms, c.st, c.go, c.n, c.end, Math.round(careerWork())]); }
      return { o, n: SHIP_TRADITIONS.length, flags: SHIP_TRADITIONS.filter(t => t.flag || (t.when && t.when.flag)).map(t => t.id) }; })()""")
    for row in r['o']: print(row)
    print(r['n'], r['flags']); g.close()
