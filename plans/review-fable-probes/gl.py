import sys; sys.path.insert(0, '' + __import__('os').path.dirname(__import__('os').path.abspath(__file__)) + ''); from g import *
HOOK = r"""(() => { const gl = renderer.getContext(); window.__g = {}; const add = (k, b) => { const o = window.__g[k] || (window.__g[k] = { n: 0, bytes: 0 }); o.n++; o.bytes += b || 0; };
  for (const f of ['bufferData', 'bufferSubData']) { const o = gl[f].bind(gl); gl[f] = (...a) => { const d = f === 'bufferData' ? a[1] : a[2]; add(f, d && d.byteLength || 0); return o(...a); }; }
  for (const f of ['texImage2D', 'texSubImage2D']) { const o = gl[f].bind(gl); gl[f] = (...a) => { const s = a[a.length - 1]; let b = 0; if (s && s.byteLength) b = s.byteLength; else if (s && s.width) b = s.width * s.height * 4; else if (a.length >= 9 && typeof a[3] === 'number') b = a[3] * a[4] * 4; add(f, b); return o(...a); }; }
  for (const f of ['drawElements', 'drawArrays', 'drawElementsInstanced', 'drawArraysInstanced', 'useProgram', 'uniformMatrix4fv', 'uniform3f', 'uniform1f', 'bindTexture', 'generateMipmap']) { const o = gl[f].bind(gl); gl[f] = (...a) => { add(f, 0); return o(...a); }; } })()"""
with sync_playwright() as pw:
    for day, tm, deck in [(1, '18:30', 3), (2, '10:00', 4), (2, '03:00', 4)]:
        g = Game(pw, sys.argv[1]); h, m = map(int, tm.split(':')); g.ev(f"skipTo({(day - 1) * 1440 + h * 60 + m}); if (deckDef.num !== {deck}) goToDeck({deck})"); g.step(200); g.step(30, draw=True); g.ev(HOOK); g.ev('window.__g = {}')
        g.step(30, draw=True); r = g.page.evaluate('window.__g')
        print(f"Day {day} {tm} deck {deck}, {g.ev('crowd.stats().people')} people, standing still; per drawn frame:", '  '.join(f"{k} {v['n'] / 30:.1f}" + (f" ({v['bytes'] / 30 / 1024:.0f} KB)" if v['bytes'] else '') for k, v in sorted(r.items())))
        g.close()
