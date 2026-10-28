# RV25: perf_check's own timing (best of 3 batches of 20 frames, rendering skipped) for Sunday dinner, PAD_ON true vs false,
# alternated 4 times each in fresh pages. Usage: pad_time.py BUILD.html
import sys, os, re, json
G = os.path.abspath(sys.argv[1])
exec(open(os.path.join(os.path.dirname(G), 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
src = open(G).read(); off = src.replace('const PAD_ON = true;', 'const PAD_ON = false;', 1); assert off != src
pon = WORK / 'test' / '_rv25_padon.html'; pon.write_text(src); poff = WORK / 'test' / '_rv25_padoff.html'; poff.write_text(off)
M = r"""(n => { window.__skip = true; let js = 1e9; const now = window.__realNow || (() => performance.now());
  for (let k = 0; k < 3; k++) { const a = now(); window.__step(n, 1000 / 30); js = Math.min(js, (now() - a) / n); } window.__skip = false; return +js.toFixed(2); })"""
with sync_playwright() as pw:
    res = {'on': [], 'off': []}
    for rep in range(4):
        for tag, path in (('on', pon), ('off', poff)):
            g = Game(pw, str(path)); g.page.set_viewport_size({'width': 390, 'height': 844})
            g.ev("skipTo(6 * 1440 + 18 * 60 + 30); if (deckDef.num !== 3) goToDeck(3)"); g.step(30)
            g.ev("(() => { const k = Object.keys(ROOM_BOX).find(k => ROOMS[k] && /^Mess/i.test(ROOMS[k].name)), b = ROOM_BOX[k], c = cellPos(Math.floor((b.i0 + b.i1) / 2), Math.floor((b.j0 + b.j1) / 2)); player.obj.position.copy(cellPos(...nearestOpen(c.x, c.z, player))); })()"); g.step(30)
            import time
            g.page.evaluate('window.__skip = true'); best = 1e9
            for k in range(3):
                a = time.perf_counter(); g.page.evaluate('window.__step(20, 1000 / 30)'); best = min(best, (time.perf_counter() - a) * 1000 / 20)
            g.page.evaluate('window.__skip = false'); res[tag].append(round(best, 2)); g.close()
        print(rep, res, flush=True)
    for t in res: print(t, 'min', min(res[t]), 'median', sorted(res[t])[len(res[t]) // 2])
