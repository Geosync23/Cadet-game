import sys, json
__file__ = '/tmp/rv14/wk/cadet_test.py'
exec(open('/tmp/rv14/wk/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 900, 760)
    print(g.ev("""(() => { const out = []; for (const e0 of SHIP_TRADITIONS.filter(t => P926_NEW.has(t.id))) for (let d = 1; d <= 112; d++) { const e = eventsOn(d).find(x => x.id === e0.id); if (!e) continue;
      const came = schedPeople().filter(p => planDay(p, d).some(s => evTagId(s.tag) === e.id)).map(p => p.id);
      out.push([e.id, d, (e.from/60|0)+':'+String(e.from%60).padStart(2,'0'), e.ev.host, came.includes(e.ev.host), came.length]); }
      return JSON.stringify(out); })()"""))
    print(g.errors[:3]); g.close()
