# RV8 probe: meal traditions on paper, days 0-21: per tradition tag, how many seated, and the most leaving in one minute
# (and in five). p_leave.py GAME CT_DIR
import sys, json
exec(open(sys.argv[2] + '/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 900, 760); g.step(3)
    r = g.ev(r"""(() => { const out = [];
      for (let d = 0; d <= 21; d++) { const day = shipDay(d), by = new Map();
        for (const [id, segs] of day.plans) for (const s of segs) if (s.tag && /^ev-/.test(s.tag) && /dinner|breakfast|supper|meal|eat|sit/i.test(String(s.act))) { if (!by.has(s.tag)) by.set(s.tag, []); by.get(s.tag).push([s.from, s.to]); }
        for (const [tag, L] of by) { const leave = new Map(); for (const [, to] of L) { const m = Math.round(to); leave.set(m, (leave.get(m) || 0) + 1); }
          const ms = [...leave.keys()].sort((a, b) => a - b); let w1 = 0, w5 = 0; for (const m of ms) { w1 = Math.max(w1, leave.get(m)); let c = 0; for (const k of ms) if (k >= m && k < m + 5) c += leave.get(k); w5 = Math.max(w5, c); }
          const B = (d - 1) * 1440, hh = x => { const v = ((x - B) % 1440 + 1440) % 1440; return String(Math.floor(v / 60)).padStart(2, '0') + ':' + String(Math.round(v % 60)).padStart(2, '0'); };
          out.push([d, tag, L.length, w1, w5, hh(Math.min(...L.map(x => x[1]))), hh(Math.max(...L.map(x => x[1])))]); } }
      return out; })()""")
    for x in r: print('  day %2d %-34s seated %2d  most in a minute %2d, in 5 min %2d, first up %s, last up %s' % tuple(x))
    print('errors', g.errors[:3]); g.close()
