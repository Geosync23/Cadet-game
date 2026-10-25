import sys, json
__file__ = '/tmp/rv14/wk/cadet_test.py'
exec(open('/tmp/rv14/wk/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 900, 760)
    for d, who in [(63, 'cruz-tove'), (104, 'alvarez-luca')]:
        print(d, who, g.ev("""(() => { const p = schedPeople().find(x => x.id === '%s'), d = %d; const e = eventsOn(d).find(x => /garden-walk|window-sketch/.test(x.id));
          const pl = planDay(p, d).map(s => [s.at, s.dur, s.from, s.to, s.tag || s.kind || s.act]).filter(x => (x[0] || x[2] || 0) < 900);
          return JSON.stringify({ ev: e && [e.id, e.from, e.to], arrive: e ? evArrive(p, d, e) : null, others: eventsOn(d).filter(x => x.from < 900 && x.to > 360).map(x => [x.id, x.from, x.to, x.ev.host || null]), plan: pl }); })()""" % (who, d)))
    g.close()
