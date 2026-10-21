# OR1's probe for opt #6: every grain() call (at load, on every deck's build, a lap later): its canvas's pixels after
# (FNV-1a) and the seed after. Two builds must log the same.   python3 grain_all.py OLD.html NEW.html
import sys, os, re, pathlib, hashlib, json
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("import sys, json, hashlib")[0])
from playwright.sync_api import sync_playwright
W = "function grain(g, w, h, amt) { const r = grain__(g, w, h, amt), p = g.getImageData(0, 0, w, h).data; let x = 2166136261; for (let i = 0; i < p.length; i++) { x ^= p[i]; x = Math.imul(x, 16777619) >>> 0; } (window.__gl = window.__gl || []).push([w, h, amt, x, seed]); return r; }\nfunction grain__(g, w, h, amt) {"
res = {}
with sync_playwright() as pw:
    for tag, path in (('old', sys.argv[1]), ('new', sys.argv[2])):
        s = open(path).read(); assert s.count('function grain(g, w, h, amt) {') == 1
        p = WORK / 'test' / f'_grain_{tag}.html'; p.write_text(s.replace('function grain(g, w, h, amt) {', W, 1))
        errs = []; g = Game(pw, str(p), 390, 844, errs); log = [('load', g.ev('(() => { const L = window.__gl; window.__gl = []; return L; })()'))]
        for n in (1, 2, 3, 5, 6, 7, 4, 1, 2, 3, 5, 6, 7, 4):
            g.ev(f'goToDeck({n})'); log.append((f'D{n}', g.ev('(() => { const L = window.__gl; window.__gl = []; return L; })()'), g.ev('seed')))
        res[tag] = log; g.close()
        print(tag, 'grain calls', sum(len(x[1]) for x in log), 'md5', hashlib.md5(json.dumps(log).encode()).hexdigest()[:12], 'errors', errs[:3], flush=True)
print('GRAIN IDENTICAL' if res['old'] == res['new'] else 'GRAIN DIFFERS: ' + str([i for i, (a, b) in enumerate(zip(res['old'], res['new'])) if a != b][:5]))
