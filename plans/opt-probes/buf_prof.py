import sys, os, re, json, time, collections
src = open('/home/user/Cadet-game/cadet_test.py').read().split("import sys, json, hashlib")[0]
exec(src)
DAYSIM = re.search(r'SIM = r"""(.*?)"""', open('/home/user/Cadet-game/day_check.py').read(), re.S)[1]
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1])
    # count buffer uploads and bytes per drawn frame, with the JS stack of the biggest
    g.page.evaluate("""() => { const gl = window.__sc('renderer.getContext()'); window.__bu = { n: 0, bytes: 0, sub: 0, subBytes: 0, frames: 0 };
      const P = Object.getPrototypeOf(gl); const bd = P.bufferData, bs = P.bufferSubData;
      gl.bufferData = function (t, d, u) { window.__bu.n++; window.__bu.bytes += d && d.byteLength || 0; return bd.apply(this, arguments); };
      gl.bufferSubData = function (t, o, d) { window.__bu.sub++; window.__bu.subBytes += d && d.byteLength || 0; return bs.apply(this, arguments); }; }""")
    g.ev("window.__realTick = tickShip; tickShip = () => {}"); g.ev("player.steer = null; player.stop()")
    sim = DAYSIM.replace("window.__skip = false; window.__step(1, 1);", "window.__skip = false; const b0 = {...window.__bu}; const a0 = performance.__rn ? 0 : 0; window.__step(1, 1); window.__bu.frames++; (window.__bl || (window.__bl = [])).push([hhmm(now - B), view, window.__bu.sub - b0.sub, window.__bu.subBytes - b0.subBytes, window.__bu.n - b0.n, window.__bu.bytes - b0.bytes]);")
    t = time.time(); out = g.page.evaluate("s => window.__sc(s)({ n: 3, day: 9, step: 0.05, draw: true })", sim); el = time.time() - t
    print('wall', round(el, 1), 'totals', g.page.evaluate('window.__bu'))
    for r in g.page.evaluate('window.__bl')[:60]: print(r)
    g.close()
