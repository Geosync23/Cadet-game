# RN1: Sunday dinner in the mess hall (perf_check scene, room fixed), 600 drawn frames, true upload bytes per frame.
import sys, os, re, json, time
src = open('/home/user/Cadet-game/cadet_test.py').read().split("import sys, json, hashlib")[0]
exec(src)
SCENE_JS = re.search(r'SCENE_JS = r"""(.*?)"""', open('/home/user/Cadet-game/perf_check.py').read(), re.S)[1].replace("at = nearestOpen(Math.floor((b.i0 + b.i1) / 2), Math.floor((b.j0 + b.j1) / 2), player)", "c0 = cellPos(Math.floor((b.i0 + b.i1) / 2), Math.floor((b.j0 + b.j1) / 2)), at = nearestOpen(c0.x, c0.z, player)")
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844)
    g.page.evaluate("s => window.__sc(s)({name:'dinner', day:7, time:'18:30', deck:3, room:'^Mess'})", SCENE_JS)
    g.ev("camera.zoom = 1.5; camera.updateProjectionMatrix()"); g.step(90)
    g.page.evaluate("""() => { const gl = window.__sc('renderer.getContext()'); window.__bu = { n: 0, bytes: 0, sub: 0, subBytes: 0, max: 0 };
      const P = Object.getPrototypeOf(gl); const bd = P.bufferData, bs = P.bufferSubData;
      gl.bufferData = function (t, d, u) { window.__bu.n++; window.__bu.bytes += d && d.byteLength || 0; return bd.apply(this, arguments); };
      gl.bufferSubData = function (t, o, d, so, len) { window.__bu.sub++; window.__bu.subBytes += arguments.length >= 5 ? len * d.BYTES_PER_ELEMENT : d.byteLength; return bs.apply(this, arguments); }; }""")
    N = 600; per = []
    t = time.time()
    for k in range(N):
        b0 = g.page.evaluate('window.__bu.subBytes + window.__bu.bytes'); g.page.evaluate('window.__step(1, 1000/30)'); per.append(g.page.evaluate('window.__bu.subBytes + window.__bu.bytes') - b0)
    el = time.time() - t
    per.sort()
    print(f'{N} drawn frames at Sunday dinner (wall {el:.1f}s): upload MB total {sum(per)/1e6:.1f}, mean {sum(per)/N/1e3:.0f} KB/frame, median {per[N//2]/1e3:.0f} KB, p95 {per[int(N*.95)]/1e3:.0f} KB, max {per[-1]/1e6:.2f} MB, frames with any upload {sum(1 for x in per if x)}')
    print(g.page.evaluate('window.__bu')); print('room', g.ev("(r => r ? ROOMS[r].name : '?')(roomAt(...player.here()))"))
    print('crowd buffers', g.ev("JSON.stringify(crowd.stats())"))
    g.close()
