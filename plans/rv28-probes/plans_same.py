# RV28: switch off = 0.99.3 on paper: every crew member's planDay for Days 1..N, hashed per day, in each build.
import sys, os, types, json
os.environ.setdefault('CADET_CHROME', '/opt/pw-browsers/chromium')
from playwright.sync_api import sync_playwright
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../cadet_test.py')).read(); src = src[:src.index('import sys, json, hashlib')]
ct = types.ModuleType('ct'); exec(src, ct.__dict__)
N = int(os.environ.get('DAYS', '30'))
JS = r"""(N => { const out = {}; const h = s => { let x = 0; for (let i = 0; i < s.length; i++) x = (x * 31 + s.charCodeAt(i)) | 0; return x; };
  for (let d = 1; d <= N; d++) { let s = ''; for (const p of schedPeople()) s += p.id + JSON.stringify(planDay(p, d).map(x => [x.from, x.to, x.act, x.placeId, x.tag, x.deck])); out[d] = h(s); } return out; })"""
res = []
with sync_playwright() as pw:
    for f in sys.argv[1:3]:
        g = ct.Game(pw, f); res.append(g.page.evaluate('n => window.__sc("(" + %s + ")(" + n + ")")' % json.dumps(JS), N)); print(f[-50:], 'errors', g.errors[:3]); g.close()
diff = [d for d in res[0] if res[0][d] != res[1][d]]
print('days differing:', diff or 'none', '(of', N, ')')
