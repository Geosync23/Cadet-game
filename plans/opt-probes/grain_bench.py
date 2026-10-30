# opt #6: the grain painter, old vs candidates, on the game's own page: the same canvas painted the same way, the same seed;
# pixels and the seed after must match; time per call (best of 5) at the sizes the game paints
import sys, os, re, json
src = open('/home/user/Cadet-game/cadet_test.py').read().split("import sys, json, hashlib")[0]
exec(src)
from playwright.sync_api import sync_playwright
CANDS = {
 'old': """(g, w, h, amt) => { const d = g.getImageData(0, 0, w, h), p = d.data; for (let i = 0; i < p.length; i += 4) { const n = (R() - .5) * amt; p[i] += n; p[i + 1] += n; p[i + 2] += n; } g.putImageData(d, 0, 0); }""",
 'mers': """(g, w, h, amt) => { const d = g.getImageData(0, 0, w, h), p = d.data, L = p.length; let s = seed;
   for (let i = 0; i < L; i += 4) { const x = s * 16807, hi = Math.floor(x / 2147483648); s = x - hi * 2147483648 + hi; if (s >= 2147483647) s -= 2147483647;
     const n = (s / 2147483647 - .5) * amt; p[i] += n; p[i + 1] += n; p[i + 2] += n; } seed = s; g.putImageData(d, 0, 0); }""",
 'local': """(g, w, h, amt) => { const d = g.getImageData(0, 0, w, h), p = d.data, L = p.length; let s = seed;
   for (let i = 0; i < L; i += 4) { s = (s * 16807) % 2147483647; const n = (s / 2147483647 - .5) * amt; p[i] += n; p[i + 1] += n; p[i + 2] += n; } seed = s; g.putImageData(d, 0, 0); }""",
}
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844)
    for (w, h, amt) in [(128, 360, 9), (512, 512, 16), (1024, 1024, 10), (4096, 2048, 8)]:
        res = {}
        for name, fn in CANDS.items():
            r = g.ev(f"""(() => {{ const f = {fn}; const T = () => new Event('x').timeStamp; let best = 1e9, out = null;
              for (let k = 0; k < 5; k++) {{ const c = document.createElement('canvas'); c.width = {w}; c.height = {h}; const x = c.getContext('2d');
                x.fillStyle = '#7a8a90'; x.fillRect(0, 0, {w}, {h}); x.fillStyle = 'rgba(250,10,10,.5)'; x.fillRect(3, 3, {w} / 3, {h} / 2); x.fillStyle = '#000'; x.fillRect(0, 0, 5, 5); x.fillStyle = '#fff'; x.fillRect(6, 0, 5, 5);
                const s0 = seed; seed = 12345 + k; const a = T(); f(x, {w}, {h}, {amt}); const t = T() - a; const s1 = seed; seed = s0;
                if (k === 0) {{ const p = x.getImageData(0, 0, {w}, {h}).data; let hsh = 2166136261; for (let i = 0; i < p.length; i++) {{ hsh ^= p[i]; hsh = Math.imul(hsh, 16777619) >>> 0; }} out = hsh + ':' + s1; }}
                best = Math.min(best, t); }}
              return [Math.round(best * 10) / 10, out]; }})()""")
            res[name] = r
        print(f'{w}x{h} amt {amt}:', ' | '.join(f'{k} {v[0]} ms {v[1]}' for k, v in res.items()), 'SAME' if len({v[1] for v in res.values()}) == 1 else 'DIFFERENT', flush=True)
    g.close()
