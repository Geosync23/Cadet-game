# RN1: day_check's crowd logic with true upload bytes (WebGL2 range, not the whole array) and a real wait (readPixels) after each drawn frame.
# python3 buf_true.py BUILD.html [DECK]. Columns: hh:mm view subCalls fullMB realMB subMs bufData bdMB frameMs waitBefore waitAfter
# true bytes per bufferSubData call (WebGL2 form: srcOffset, length), real time via Event.timeStamp
import sys, os, re, json, time
src = open('/home/user/Cadet-game/cadet_test.py').read().split("import sys, json, hashlib")[0]
exec(src)
DAYSIM = re.search(r'SIM = r"""(.*?)"""', open('/home/user/Cadet-game/day_check.py').read(), re.S)[1]
from playwright.sync_api import sync_playwright
deck = int(sys.argv[2]) if len(sys.argv) > 2 else 3
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1])
    g.page.evaluate("""() => { const gl = window.__sc('renderer.getContext()'); const T = () => new Event('x').timeStamp;
      window.__bu = { webgl2: !!window.__sc('renderer.capabilities.isWebGL2'), n: 0, bytes: 0, sub: 0, full: 0, real: 0, ms: 0, msD: 0 };
      const P = Object.getPrototypeOf(gl); const bd = P.bufferData, bs = P.bufferSubData;
      gl.bufferData = function (t, d, u) { const t0 = T(); window.__bu.n++; window.__bu.bytes += d && d.byteLength || 0; const r = bd.apply(this, arguments); window.__bu.msD += T() - t0; return r; };
      gl.bufferSubData = function (t, o, d, so, len) { const t0 = T(); const B = window.__bu; B.sub++; B.full += d.byteLength;
        B.real += arguments.length >= 5 ? len * d.BYTES_PER_ELEMENT : arguments.length === 4 ? d.byteLength - so * d.BYTES_PER_ELEMENT : d.byteLength;
        const r = bs.apply(this, arguments); const dt = T() - t0; B.ms += dt; if (dt > 40) (B.slow || (B.slow = [])).push([Math.round(dt), t === 34963 ? 'IDX' : 'ARR', d.constructor.name, d.length, o, so, len, gl.getParameter(t === 34963 ? 34965 : 34964) && 1]); return r; }; }""")
    g.ev("window.__realTick = tickShip; tickShip = () => {}"); g.ev("player.steer = null; player.stop()")
    sim = DAYSIM.replace("window.__skip = false; window.__step(1, 1);", "window.__skip = false; const b0 = {...window.__bu}; const gl = renderer.getContext(); const f0 = new Event('x').timeStamp; gl.readPixels(0, 0, 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, new Uint8Array(4)); const fin0 = new Event('x').timeStamp - f0; const t0 = new Event('x').timeStamp; window.__step(1, 1); const f1 = new Event('x').timeStamp; gl.readPixels(0, 0, 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, new Uint8Array(4)); const fin1 = new Event('x').timeStamp - f1; const B = window.__bu; (window.__bl || (window.__bl = [])).push([hhmm(now - B0), view, B.sub - b0.sub, ((B.full - b0.full)/1e6).toFixed(2), ((B.real - b0.real)/1e6).toFixed(2), (B.ms - b0.ms).toFixed(0), B.n - b0.n, ((B.bytes - b0.bytes)/1e6).toFixed(2), (f1 - t0).toFixed(0), fin0.toFixed(0), fin1.toFixed(0)]);").replace("const B = (day", "const B0 = (day - 1) * 1440, B = (day")
    t = time.time(); out = g.page.evaluate("s => window.__sc(s)({ n: %d, day: 1, step: 0.05, draw: true })" % deck, sim); el = time.time() - t
    print('wall', round(el, 1), 'totals', g.page.evaluate('window.__bu'))
    print('hh:mm view subCalls fullMB realMB subMs bufData bdMB frameMs finBefore finAfter')
    for r in g.page.evaluate('window.__bl'): print(r)
    [print(x) for x in g.page.evaluate('window.__bu.slow || []')]
    print('crowd', g.ev('JSON.stringify(crowd.stats())'), g.ev('JSON.stringify(crowd.chunks.map(c => c.buf ? [c.nv, c.buf.cv, c.ni, c.buf.ci] : null))'))
    g.close()
