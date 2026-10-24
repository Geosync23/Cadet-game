import sys
exec(open('/home/user/w-g8/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844); g.step(3)
    g.ev("setShipNow(8 * 60 + 40); goToDeck(3)"); g.step(30)
    g.ev("""(() => { const S = window.__up = { short: [], long: [] }, st = new Map(), track = new Map(); const f0 = window.__step;
      window.__rec = function () {
        for (const c of DECK_CREW) { if (!c.h || !c.h.pos) continue; const p = c.h.pos, was = st.get(c);
          if (was && was.settled && !c.settled) track.set(c, { n: 0, last: [p.x, p.z], from: was.at, max: Math.hypot(p.x - was.at[0], p.z - was.at[1]), hop: Math.hypot(c.x - was.lx, c.z - was.lz) });
          else { const t = track.get(c); if (t) { const m = Math.hypot(p.x - t.last[0], p.z - t.last[1]); if (m > t.max) t.max = m; t.last = [p.x, p.z]; if (++t.n >= 30) { (t.hop > 1.2 ? S.long : S.short).push([c.p.id, +t.hop.toFixed(2), +t.max.toFixed(3)]); track.delete(c); } } }
          st.set(c, { settled: c.settled, at: [p.x, p.z], lx: c.x, lz: c.z }); }
      }; })()""")
    for k in range(24):
        g.ev("(() => { window.__skip = true; for (let i = 0; i < 100; i++) { window.__step(1, 1000 / 30); window.__rec(); } window.__skip = false; })()")
    s = g.ev("window.__up")
    sh, lo = s['short'], s['long']
    print('short get-ups', len(sh), 'biggest drawn move in one frame', max([x[2] for x in sh] or [0]), sh[:5])
    print('long get-ups', len(lo), 'biggest drawn move in one frame', max([x[2] for x in lo] or [0]), lo[:5])
    g.close()
