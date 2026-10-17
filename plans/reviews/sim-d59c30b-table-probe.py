# sim 0.26.41: the Sunday long table (day 7) from the plans: when diners join the line and sit, per meal tradition
import sys
exec(open('cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1]); ev = g.ev
    for d in (7, 14):
        print(d, ev("""((d) => { const B = (d - 1) * 1440, on = eventsOn(d).filter(e => e.ev.meal), out = {};
          for (const e of on) { const sits = [], qs = [];
            for (const p of schedPeople()) { const P = planDay(p, d); const k = P.findIndex(s => s.tag && s.tag.startsWith('ev-' + e.id) && s.placeId); if (k < 0) continue;
              sits.push(P[k].from - B); const q = P.slice(0, k).reverse().find(s => s.tag === 'queue'); if (q) qs.push(q.from - B); }
            sits.sort((a, b) => a - b); qs.sort((a, b) => a - b);
            const at = f => sits.length ? hhmm(sits[Math.min(sits.length - 1, Math.floor(f * sits.length))]) : null;
            out[e.id] = { from: hhmm(e.from), n: sits.length, lineOpens: qs.length ? hhmm(qs[0]) : null, half: at(.5), ninety: at(.9), last: sits.length ? hhmm(sits[sits.length - 1]) : null }; }
          return out; })(""" + str(d) + ")"))
    g.close()
