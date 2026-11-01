exec(open('/tmp/pf/scripts/common.py').read())
from playwright.sync_api import sync_playwright
path=sys.argv[1]; D=int(sys.argv[2]); H=int(sys.argv[3]); names=sys.argv[4].split(',')
SCENE=open('/tmp/pf/scripts/long.py').read().split('SCENE=r"""')[1].split('"""')[0].replace("10 * 60", str(H-1)+" * 60 + 58")
WRAP="(names => { window.__W = {}; const ok = []; for (const n of names) { let f; try { f = eval(n); } catch (e) { continue; } if (typeof f !== 'function') continue; try { eval(n + ' = function (...a) { const t = window.__realNow(); try { return f.apply(this, a); } finally { window.__W[n] = (window.__W[n] || 0) + window.__realNow() - t; } }'); } catch (e) { delete window.__W[n]; } } return names.filter(n => { try { return eval(n).toString().includes('window.__realNow'); } catch (e) { return false; } }); })"
FR=r"""(n => { window.__skip = true; const out = []; for (let k = 0; k < n; k++) { window.__W = {}; const t0 = SHIP.time.min, a = window.__realNow(); window.__step(1, 1000 / 30); const v = window.__realNow() - a; if (v > 15) out.push([k, hhmm(t0), +v.toFixed(1), Object.entries(window.__W).filter(x => x[1] > 2).map(x => [x[0], +x[1].toFixed(1)]).sort((a, b) => b[1] - a[1])]); } window.__skip = false; return out; })"""
with sync_playwright() as pw:
    g=Game(pw,path,390,844); g.page.evaluate(REALNOW)
    g.page.evaluate(f"s => window.__sc(s)({D})", SCENE); g.step(30)
    print('wrapped', g.page.evaluate("([s, n]) => window.__sc(s)(n)", [WRAP, names]))
    for r in g.page.evaluate("s => window.__sc(s)(250)", FR): print(r)
