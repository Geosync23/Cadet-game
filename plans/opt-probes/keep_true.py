# keep compiled shaders across deck changes: first frame after each change, timed WITH a real wait (readPixels) so
# SwiftShader's queued drawing isn't billed to the next sync point. Rows: build ms + first frame ms (incl. wait), programs.
import sys, os, re, time
src = open('/home/user/Cadet-game/cadet_test.py').read().split("import sys, json, hashlib")[0]
exec(src)
from playwright.sync_api import sync_playwright
W, H = (int(x) for x in (sys.argv[3] if len(sys.argv) > 3 else '390x844').split('x'))
KEEP = """(() => { const seen = new Set(); window.__keepTick = () => { for (const p of renderer.info.programs) if (!seen.has(p)) { seen.add(p); p.usedTimes++; } }; })()"""
J = """([n, keep]) => { const T = () => new Event('x').timeStamp; const gl = __sc('renderer.getContext()'); const px = new Uint8Array(4), wait = () => gl.readPixels(0, 0, 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, px);
  wait(); const a = T(); __sc('goToDeck(' + n + ')'); const b = T(); window.__skip = false; __step(1, 33); wait(); if (keep) __sc('__keepTick()'); const d = T();
  __step(1, 33); wait(); const e = T();
  return [Math.round(b - a), Math.round(d - b), Math.round(e - d), __sc('renderer.info.programs.length')]; }"""
mode = sys.argv[2] if len(sys.argv) > 2 else 'both'
with sync_playwright() as pw:
    for keep in ((False, True) if mode == 'both' else (mode == 'keep',)):
        g = Game(pw, sys.argv[1], W, H)
        if keep and 'keepShaders' not in open(sys.argv[1]).read(): g.ev(KEEP); g.ev('__keepTick()')
        elif keep: keep = False   # the build keeps them itself
        for lap in (1, 2, 3):
            rows = [g.page.evaluate(J, [n, keep]) for n in (3, 5, 2, 1, 6, 7, 4)]
            print('keep ' if keep or mode == 'keep' else 'plain', f'{W}x{H} lap {lap}:', ' | '.join(f'D{n} {r[0]}+{r[1]} ({r[2]}) p{r[3]}' for n, r in zip((3, 5, 2, 1, 6, 7, 4), rows)), '| first frames', sum(r[1] for r in rows), 'ms; next frames', sum(r[2] for r in rows), flush=True)
        g.close()
