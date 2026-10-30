# opt #6 probe: tex() canvases with willReadFrequently (drawn on the CPU) vs as now: every tex canvas's pixels after load
# and after building every deck, the seed, and the load time / grain time / deck build times
import sys, os, re, json, pathlib, time
src = open('/home/user/Cadet-game/cadet_test.py').read().split("import sys, json, hashlib")[0]
exec(src)
from playwright.sync_api import sync_playwright
BASE = pathlib.Path(sys.argv[1]).read_text()
def variant(wrf):
    S = BASE.replace("const g = c.getContext('2d'); draw(g, w, h);", "const g = c.getContext('2d'" + (", { willReadFrequently: true }" if wrf else "") + "); (window.__texs = window.__texs || []).push(c); draw(g, w, h);", 1)
    S = S.replace("function grain(g, w, h, amt) {", "function grain(g, w, h, amt) { const __t = new Event('x').timeStamp; try { return grain0(g, w, h, amt); } finally { window.__gt = (window.__gt || 0) + new Event('x').timeStamp - __t; } }\nfunction grain0(g, w, h, amt) {", 1)
    p = pathlib.Path(sys.argv[2]) / f'_wrf{int(wrf)}.html'; p.write_text(S); return str(p)
FPJS = """(() => { const out = []; for (const c of window.__texs) { if (!c.width || !c.height) { out.push('freed'); continue; } const p = c.getContext('2d').getImageData(0, 0, c.width, c.height).data; let h = 2166136261; for (let i = 0; i < p.length; i++) { h ^= p[i]; h = Math.imul(h, 16777619) >>> 0; } out.push(c.width + 'x' + c.height + ':' + h); } return out; })()"""
res = {}
with sync_playwright() as pw:
    for wrf in (False, True):
        path = variant(wrf)
        t = time.time(); g = Game(pw, path, 390, 844); load = time.time() - t
        gt = g.page.evaluate('window.__gt'); fp0 = g.page.evaluate(FPJS)
        builds = []
        for n in (1, 2, 3, 5, 6, 7, 4):
            builds.append(g.page.evaluate("n => { const a = new Event('x').timeStamp; __sc('goToDeck(' + n + ')'); return Math.round(new Event('x').timeStamp - a); }", n))
        fp1 = g.page.evaluate(FPJS); seed = g.ev('seed')
        res[wrf] = (fp0, fp1, seed)
        print('wrf' if wrf else 'now', f'load {load:.1f} s, grain {gt:.0f} ms, builds {builds}, {len(fp1)} canvases, seed {seed}', flush=True)
        g.close()
a, b = res[False], res[True]
print('at load: canvases differing', sum(x != y for x, y in zip(a[0], b[0])), 'of', len(a[0]))
print('after decks: canvases differing', sum(x != y for x, y in zip(a[1], b[1])), 'of', len(a[1]), [ (x, y) for x, y in zip(a[1], b[1]) if x != y][:6])
print('seed same' if a[2] == b[2] else 'SEED DIFFERS')
