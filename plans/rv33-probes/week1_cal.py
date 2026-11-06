# RV33 probe: the first week's calendar on a fresh save with the intro ON (lead 49's rule).
# Lists, for Days 0-8: traditions/events (eventsOn), the events base's beats (evBeatsOn), call-in meetings (evMeetsOn),
# the intro week's beats (INTRO_WEEK with a time span), and flags every time overlap between things the player is asked
# to be at. Run from the repo root:  python3 plans/rv33-probes/week1_cal.py BUILD.html [--json OUT]
import sys, json, os
exec(open('cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
build = sys.argv[1]
DUMP = r"""(() => {
  const hm = m => String(Math.floor(m/60)).padStart(2,'0') + ':' + String(m%60).padStart(2,'0');
  const out = {};
  for (let d = 0; d <= 8; d++) {
    const items = [];
    try { for (const e of eventsOn(d)) items.push({ kind: 'trad', id: e.id, name: e.name, from: e.from, to: e.to, who: (e.ev.host || e.ev.leader || '') + '' , names: e.names }); } catch (x) { items.push({ kind: 'ERR', id: 'eventsOn ' + x }); }
    try { if (typeof evBeatsOn === 'function') for (const b of evBeatsOn(d)) items.push({ kind: 'beat', id: (b.id || b.kind) + '', from: b.from, to: b.to }); } catch (x) { items.push({ kind: 'ERR', id: 'evBeatsOn ' + x }); }
    try { if (typeof evMeetsOn === 'function') for (const m of evMeetsOn(d)) items.push({ kind: 'meet', id: m.event + ':' + m.id, from: m.at, to: m.at + m.len }); } catch (x) { items.push({ kind: 'ERR', id: 'evMeetsOn ' + x }); }
    for (const b of INTRO_WEEK) if (b.day === d && b.until) items.push({ kind: 'intro', id: b.id, from: b.at, to: b.until, who: b.who || '' });
    items.sort((a, b) => a.from - b.from);
    for (const i of items) { i.span = hm(i.from) + '-' + hm(i.to); }
    out[d] = { weekday: typeof weekday === 'function' ? weekday(d) : null, items };
  }
  return out;
})()"""
with sync_playwright() as pw:
    g = Game(pw, build)
    g.ev('localStorage.clear()'); g.ev('newGameStart(true)'); g.step(5)
    cal = g.ev(DUMP)
    errs = g.ev('window.__err || null')
print('build', build, 'page error:', errs)
SOFT = {'d1-shadow', 'd1-lead', 'd3-pell', 'd4-favour', 'd1-zeke-dinner'}   # the shift itself and seek-anywhere beats
clashes = []
for d in sorted(cal, key=int):
    c = cal[d]; print('\nDay %s (weekday %s)' % (d, c['weekday']))
    for i in c['items']: print('  %-6s %-11s %s %s' % (i['kind'], i['span'], i['id'], i.get('names') or ''))
    its = [i for i in c['items'] if i['kind'] != 'ERR']
    for a in range(len(its)):
        for b in range(a + 1, len(its)):
            x, y = its[a], its[b]
            if x['from'] < y['to'] and y['from'] < x['to'] and not (x['id'] in SOFT or y['id'] in SOFT):
                clashes.append((int(d), x['kind'] + ':' + x['id'] + ' ' + x['span'], y['kind'] + ':' + y['id'] + ' ' + y['span']))
print('\nOVERLAPS (shift and seek beats left out):')
for c in clashes: print('  Day %d: %s  x  %s' % c)
print('none' if not clashes else '%d overlaps' % len(clashes))
if '--json' in sys.argv: json.dump(cal, open(sys.argv[sys.argv.index('--json') + 1], 'w'), indent=1)
