import sys, json
src = open('cadet_test.py').read().split('import sys, json, hashlib')[0]
exec(src)
from playwright.sync_api import sync_playwright
J = "JSON.stringify([1,2,3,5,8].map(d => schedPeople().map(p => [p.id, planDay(p, d)])))"
res = []
with sync_playwright() as pw:
    for b in sys.argv[1:3]:
        g = Game(pw, b); res.append(json.loads(g.ev(J))); g.close()
A, B = res
n = 0
for di, (da, db) in enumerate(zip(A, B)):
    for (pa, xa), (pb, xb) in zip(da, db):
        if xa != xb:
            for i, (sa, sb) in enumerate(zip(xa, xb)):
                if sa != sb:
                    ka = {k: v for k, v in sa.items() if sa.get(k) != sb.get(k)} if isinstance(sa, dict) else sa
                    kb = {k: v for k, v in sb.items() if sa.get(k) != sb.get(k)} if isinstance(sb, dict) else sb
                    n += 1
                    if n <= 25: print('day', [1,2,3,5,8][di], pa, i, ka, '->', kb)
            if len(xa) != len(xb): print('len', pa, len(xa), len(xb))
print('total step diffs', n)
