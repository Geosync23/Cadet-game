# opt #5 option B, in a scratch copy only: unloadDeck also takes the old deck's tree apart. Measures the array storage
# after a tour (vs as now) and whether any object of an unloaded deck ever comes back into the scene (a shared piece).
import sys, os, re, json, pathlib
src = open('/home/user/Cadet-game/cadet_test.py').read().split("import sys, json, hashlib")[0]
exec(src)
from playwright.sync_api import sync_playwright
BASE = pathlib.Path(sys.argv[1]).read_text()
a = "  scene.remove(deckRoot);\n  deckRoot = staticRoot = floor"
assert BASE.count(a) == 1
TRACK = "  (window.__old = window.__old || new WeakSet()); deckRoot.traverse(o => window.__old.add(o)); (window.__oldN = (window.__oldN || 0) + 1);\n"
CUT = "  { const all = []; deckRoot.traverse(o => all.push(o)); for (const o of all) { o.parent = null; o.children = []; } }\n"
def variant(cut):
    S = BASE.replace(a, TRACK + (CUT if cut else '') + a, 1)
    p = WORK / 'test' / f'_detach{int(cut)}.html'; p.write_text(S); return str(p)
CHECK = "(() => { let back = 0, names = []; scene.traverse(o => { if (window.__old && window.__old.has(o)) { back++; if (names.length < 8) names.push(o.type + ':' + (o.name || '') + ':' + (o.parent && o.parent.type)); } }); return [back, names]; })()"
with sync_playwright() as pw:
    for cut in (False, True):
        g = Game(pw, variant(cut), 390, 844); g.ev("window.__realTick = tickShip; tickShip = () => {}")
        cdp = g.page.context.new_cdp_session(g.page)
        backs = []
        for lap in (1, 2):
            for n in (3, 5, 2, 1, 6, 7, 4):
                g.ev(f'goToDeck({n})'); g.step(3); backs.append(g.ev(CHECK))
        cdp.send('HeapProfiler.collectGarbage'); cdp.send('HeapProfiler.collectGarbage'); u = cdp.send('Runtime.getHeapUsage')
        print('cut' if cut else 'now', f"after 2 tours on Deck 4: heap {u['usedSize'] / 1048576:.1f} MB, array storage {u['backingStorageSize'] / 1048576:.1f} MB; old-deck objects back in the scene: max {max(b[0] for b in backs)}", [b for b in backs if b[0]][:2], 'errors', g.errors[:3], flush=True)
        g.close()
