# opt #6: at load, split each grain() call into getImageData / the loop / putImageData (real time)
import sys, os, re, json, pathlib
src = open('/home/user/Cadet-game/cadet_test.py').read().split("import sys, json, hashlib")[0]
exec(src)
from playwright.sync_api import sync_playwright
S = pathlib.Path(sys.argv[1]).read_text()
S = S.replace("const d = g.getImageData(0, 0, w, h), p = d.data", "const __T = () => new Event('x').timeStamp, __a = __T(); const d = g.getImageData(0, 0, w, h), __b = __T(), p = d.data", 1)
S = S.replace("  g.putImageData(d, 0, 0);\n}", "  const __c = __T(); g.putImageData(d, 0, 0); (window.__gs = window.__gs || []).push([w, h, Math.round(__b - __a), Math.round(__c - __b), Math.round(__T() - __c)]);\n}", 1)
tmp = pathlib.Path(sys.argv[2]); tmp.write_text(S)
with sync_playwright() as pw:
    g = Game(pw, str(tmp), 390, 844)
    r = g.page.evaluate("window.__gs")
    for x in r: print(x)
    print('sum get/loop/put ms', [sum(x[k] for x in r) for k in (2, 3, 4)])
    g.close()
