# opt #6: how many grain() calls at load and per deck build, their pixels and their real time
import sys, os, re, json, pathlib
src = open('/home/user/Cadet-game/cadet_test.py').read().split("import sys, json, hashlib")[0]
exec(src)
from playwright.sync_api import sync_playwright
S = pathlib.Path(sys.argv[1]).read_text()
a = 'function grain(g, w, h, amt) {'
assert a in S
S = S.replace(a, "function grain(g, w, h, amt) { const __t = new Event('x').timeStamp; try { return grain0(g, w, h, amt); } finally { const __e = new Event('x').timeStamp - __t, __p = g.getImageData(0, 0, w, h).data; let __h = 2166136261; for (let __i = 0; __i < __p.length; __i++) { __h ^= __p[__i]; __h = Math.imul(__h, 16777619) >>> 0; } (window.__gr = window.__gr || []).push([w * h, __e, __h, seed]); } }\nfunction grain0(g, w, h, amt) {", 1)
tmp = pathlib.Path(sys.argv[2]); tmp.write_text(S)
with sync_playwright() as pw:
    g = Game(pw, str(tmp), 390, 844)
    r = g.page.evaluate("window.__gr"); print('FP', json.dumps([x[2:] for x in r]), 'seed after load', g.ev('seed')); print('at load:', len(r), 'calls,', sum(x[0] for x in r), 'px,', round(sum(x[1] for x in r)), 'ms')
    g.page.evaluate("window.__gr = []")
    for n in (1, 2, 3, 5, 6, 7, 4):
        g.ev(f"goToDeck({n})"); r = g.page.evaluate("window.__gr"); print(f'D{n}:', len(r), 'calls', sum(x[0] for x in r), 'px', round(sum(x[1] for x in r)), 'ms'); g.page.evaluate("window.__gr = []")
    g.close()
