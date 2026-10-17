import sys, json, os
src = open('cadet_test.py').read().split('import sys, json, hashlib')[0]
exec(src)
from playwright.sync_api import sync_playwright
out = {}
with sync_playwright() as pw:
    for b in sys.argv[1:]:
        g = Game(pw, b); r = {}
        for n in (2, 3, 4, 5, 6):
            g.ev(f"goToDeck({n})"); g.step(3)
            r[n] = g.ev("(() => (deckDef.places||[]).map(p => { const s = placeSpot(p.id); return [p.id, s && s.walk ? s.walk.join(',') : null]; }))()")
        r['plans'] = g.ev("(() => { const s = JSON.stringify([1,2,3,5,8].map(d => schedPeople().map(p => [p.id, planDay(p, d)]))); let h = 0; for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) | 0; return [h, s.length]; })()")
        out[b] = r; g.close()
json.dump(out, open('probe.json', 'w'))
A, B = sys.argv[1], sys.argv[2]
for n in ('2', '3', '4', '5', '6'):
    a = dict(out[A][int(n)] if int(n) in out[A] else out[A][n]); bb = dict(out[B][int(n)] if int(n) in out[B] else out[B][n])
    diff = [(k, a.get(k), bb.get(k)) for k in set(a) | set(bb) if a.get(k) != bb.get(k)]
    print('deck', n, 'places', len(a), len(bb), 'walk diffs', diff)
for b in sys.argv[1:]: print(b, 'plans', out[b]['plans'])
