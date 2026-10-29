# OP1: renderer.render's own cost without the software graphics process: (1) GL calls a frame by name, (2) render()
# timed with the GL calls that send work (draws, uniforms, uploads, binds) made no-ops, so only three.js's JavaScript
# and the call overhead are left (SwiftShader can block inside a call while it draws; a phone's GPU doesn't the same way).
#   python3 render_split.py BUILD.html [SCENE_REGEX] [VIEW]
import sys, os, re, json, statistics as st
pc = open('/home/user/Cadet-game/perf_check.py').read(); __file__ = '/home/user/Cadet-game/perf_check.py'
exec(pc.split("SCENE_JS = r")[0])
SCENE_JS = re.search(r'SCENE_JS = r"""(.*?)"""', pc, re.S)[1]
V = {'portrait': (390, 844, 1.5), 'wide': (390, 844, .7), 'land': (844, 390, 1.15), 'fold': (412, 960, 1.5)}
vw, vh, zoom = V[sys.argv[3] if len(sys.argv) > 3 else 'wide']
J = r"""(() => {
  const gl = renderer.getContext(), P = Object.getPrototypeOf(gl), now = Object.getPrototypeOf(performance).now.bind(performance), px = new Uint8Array(4);
  const names = Object.getOwnPropertyNames(P).filter(k => { const d = Object.getOwnPropertyDescriptor(P, k); return d && typeof d.value === 'function'; });
  const SEND = /^(draw|uniform|bufferSubData|bufferData|texImage|texSubImage|pixelStorei|bindVertexArray|bindBuffer|bindTexture|activeTexture|vertexAttrib|enable|disable|useProgram|blend|depth|cull|colorMask|stencil|viewport|scissor|clear|bindFramebuffer|frontFace|polygonOffset|lineWidth)/;
  const count = {}, orig = {}; let stub = false;
  for (const k of names) { const f = gl[k]; orig[k] = f; gl[k] = function () { count[k] = (count[k] || 0) + 1; if (stub && SEND.test(k)) return undefined; return f.apply(gl, arguments); }; }
  const sync = () => orig.readPixels.call(gl, 0, 0, 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, px);
  const rr = renderer.render.bind(renderer); let mode = 'real', times = [];
  renderer.render = (s, c) => { if (window.__skip) return; sync(); const a = now(); stub = mode === 'stub'; rr(s, c); stub = false; times.push(now() - a); sync(); };
  window.__rs = (m, n) => { mode = m; times = []; for (const k in count) delete count[k]; for (let i = 0; i < n; i++) window.__step(1, 1000 / 30); const c = Object.entries(count).sort((a, b) => b[1] - a[1]); return { times, calls: c.reduce((s, x) => s + x[1], 0) / n, top: c.slice(0, 12).map(([k, v]) => k + ' ' + Math.round(v / n)) }; };
})()"""
with sync_playwright() as pw:
    for sc in SCENES:
        if not re.search(sys.argv[2] if len(sys.argv) > 2 else 'Sunday dinner', sc['name']): continue
        g = Game(pw, sys.argv[1], vw, vh)
        g.page.evaluate(f"s => window.__sc(s)({json.dumps(sc)})", SCENE_JS)
        g.ev(f"camera.zoom = {zoom}; camera.updateProjectionMatrix()"); g.step(90); g.ev(J)
        for m in ('real', 'stub', 'real', 'stub'):
            r = g.ev(f"__rs('{m}', 30)"); t = r['times']
            print(f"{sc['name'][:40]:40} {m}: render() median {st.median(t):.2f} ms (min {min(t):.2f}, max {max(t):.2f}); GL calls a frame {r['calls']:.0f}: {', '.join(r['top'])}" if m == 'real' else f"{'':40} {m}: render() median {st.median(t):.2f} ms (min {min(t):.2f}, max {max(t):.2f})", flush=True)
        g.close()
