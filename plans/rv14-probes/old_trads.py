# RV14 (2026-10-25): with the weekend traditions on, the old traditions are as on the base build, days 1..N.
# Lead 35's rule: same days, times, places (where) and hosts; who goes may shift, but no old tradition loses more than 2
# people on any day. (Each tradition's people minimum is left to the weekend check.)
# Run: python3 plans/rv14-old_trads.py BASE.html NEW_ON.html [DAYS]   (setup as cadet_test.py)
import sys, json, pathlib
HERE = pathlib.Path(__file__).resolve().parent.parent / 'cadet_test.py'
__file__ = str(HERE)
exec(open(HERE).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
N = int(sys.argv[3]) if len(sys.argv) > 3 else 56
JS = """(() => { const W = typeof WEEKEND_TRADS !== 'undefined' ? WEEKEND_TRADS : new Set(); const out = {};
  for (let d = 1; d <= %d; d++) { out[d] = eventsOn(d).filter(e => !W.has(e.id)).map(e => {
      const came = schedPeople().filter(p => planDay(p, d).some(s => evTagId(s.tag) === e.id)).map(p => p.id).sort();
      return [e.id, e.from, e.to, JSON.stringify(e.ev.where || null), e.ev.host || null, came]; }).sort(); }
  return JSON.stringify(out); })()""" % N
res = []
with sync_playwright() as pw:
    for b in sys.argv[1:3]:
        g = Game(pw, b, 900, 760); res.append(json.loads(g.ev(JS))); g.close()
a, b = res; bad = 0; shifts = 0
for d in map(str, range(1, N + 1)):
    ea = {x[0]: x for x in a[d]}; eb = {x[0]: x for x in b[d]}
    for k in sorted(set(ea) | set(eb)):
        x, y = ea.get(k), eb.get(k)
        if not x or not y or x[:5] != y[:5]:
            bad += 1; print('FAIL day %s %s: days/times/places/host differ\n   base %s\n   new  %s' % (d, k, x and x[:5], y and y[:5])); continue
        lost, gained = sorted(set(x[5]) - set(y[5])), sorted(set(y[5]) - set(x[5]))
        if lost or gained: shifts += 1; print('  day %s %s: %d -> %d (lost %s, gained %s)' % (d, k, len(x[5]), len(y[5]), lost, gained))
        if len(lost) > 2: bad += 1; print('FAIL day %s %s loses %d people (at most 2)' % (d, k, len(lost)))
print('OLD TRADITIONS OK (%d shifts within the rule)' % shifts if not bad else 'OLD TRADITIONS FAILED (%d)' % bad)
sys.exit(1 if bad else 0)
