# opt #7: layout reads per frame at phone size: who calls getBoundingClientRect / offsetWidth / matchMedia each frame
import sys, os, re, json, collections
src = open('/home/user/Cadet-game/cadet_test.py').read().split("import sys, json, hashlib")[0]
exec(src)
from playwright.sync_api import sync_playwright
SCENE_JS = re.search(r'SCENE_JS = r"""(.*?)"""', open('/home/user/Cadet-game/perf_check.py').read(), re.S)[1]
LRHOOK = r"""(() => { window.__lr = {}; const who = () => { const s = new Error().stack.split('\n')[3] || ''; const m = s.match(/at (\S+)/); return m ? m[1] : '?'; };
  const E = Element.prototype, g = E.getBoundingClientRect; E.getBoundingClientRect = function () { const k = 'gbcr ' + who(); __lr[k] = (__lr[k] || 0) + 1; return g.call(this); };
  const mm = window.matchMedia; window.matchMedia = function (q) { const k = 'mm ' + who(); __lr[k] = (__lr[k] || 0) + 1; return mm.call(window, q); };
  for (const p of ['offsetWidth', 'offsetHeight', 'scrollWidth', 'clientWidth']) { const d = Object.getOwnPropertyDescriptor(HTMLElement.prototype, p) || Object.getOwnPropertyDescriptor(Element.prototype, p); if (!d) continue;
    Object.defineProperty(HTMLElement.prototype, p, { get() { const k = p + ' ' + who(); __lr[k] = (__lr[k] || 0) + 1; return d.get.call(this); }, configurable: true }); }
})()"""
with sync_playwright() as pw:
    for (w, h) in ((390, 844), (844, 390)):
        errs = []
        try: g = Game(pw, sys.argv[1], w, h, errs)
        except Exception as e: print('START FAIL', e, errs); continue
        g.page.evaluate("s => window.__sc(s)({name:'dinner', day:7, time:'18:30', deck:3, room:'^Mess'})", SCENE_JS); g.step(60)
        g.ev(LRHOOK); N = 300; g.page.evaluate(f'window.__skip = true; window.__step({N}, 1000/30); window.__skip = false')
        r = g.ev('window.__lr'); print(f'== {w}x{h}: layout reads per frame over {N} frames')
        for k, v in sorted(r.items(), key=lambda x: -x[1])[:16]: print(f'  {v / N:6.2f}  {k}')
        g.close()
