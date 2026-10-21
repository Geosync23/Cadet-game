# opt #4 proof: two laps of every deck, then a third lap with a screenshot on each deck, in two builds, at two sizes;
# programs alive after each deck; pixels compared old vs new; memory (geometries, textures) after each lap.
import sys, os, re, json
src = open('/home/user/Cadet-game/cadet_test.py').read().split("import sys, json, hashlib")[0]
exec(src)
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
OUT = sys.argv[3]; os.makedirs(OUT, exist_ok=True)
DECKS = (3, 5, 2, 1, 6, 7, 4)
res = {}
with sync_playwright() as pw:
    for tag, path in (('old', sys.argv[1]), ('new', sys.argv[2])):
        for W, H in ((390, 844), (844, 390)):
            g = Game(pw, path, W, H); g.ev("window.__realTick = tickShip; tickShip = () => {}"); g.ev("setShipNow(18 * 60 + 15)")
            rows = []
            for lap in (1, 2, 3):
                for n in DECKS:
                    g.ev(f"goToDeck({n}); updateDeckCrew(0.05)"); g.step(3)
                    rows.append(g.ev('renderer.info.programs.length'))
                    if lap == 3: g.shot(f'{OUT}/{tag}_{W}x{H}_D{n}.png')
                rows.append('mem ' + g.ev("JSON.stringify([renderer.info.memory.geometries, renderer.info.memory.textures])"))
            res[(tag, W)] = rows; print(tag, f'{W}x{H}', rows, flush=True)
            g.close()
bad = 0
for W, H in ((390, 844), (844, 390)):
    for n in DECKS:
        a = np.asarray(Image.open(f'{OUT}/old_{W}x{H}_D{n}.png').convert('RGB'), dtype=int); b = np.asarray(Image.open(f'{OUT}/new_{W}x{H}_D{n}.png').convert('RGB'), dtype=int)
        d = np.abs(a - b).max(axis=2); k = int((d > 0).sum()); bad += k
        print(f'{W}x{H} D{n}: differing px {k} max {int(d.max())}')
print('DECK SHOTS IDENTICAL' if not bad else 'DECK SHOTS DIFFER')
