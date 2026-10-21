# OR1's probe for opt #5: with the old deck's tree taken apart on unload, play on and watch for any object of an
# unloaded deck back in the scene (a shared piece emptied), and for errors. The build as given (events off) and a copy
# with EVENTS_ON made true. 1) the arrival evening from load, 6000 frames, checked every 300; 2) at five times over
# Days 0-7, every deck in turn, 90 frames each, checked after each; 3) 2 ship days skipped on Deck 3, then a tour.
#   python3 detach_play.py BUILD.html
import sys, os, re, pathlib, json
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("import sys, json, hashlib")[0])
from playwright.sync_api import sync_playwright
S = pathlib.Path(sys.argv[1]).read_text()
a = "  scene.remove(deckRoot);\n"
assert S.count(a) == 1
S = S.replace(a, "  (window.__old = window.__old || new WeakSet()); deckRoot.traverse(o => window.__old.add(o)); window.__oldN = (window.__oldN || 0) + 1;\n" + a, 1)
CHECK = "(() => { let back = 0, names = []; scene.traverse(o => { if (window.__old && window.__old.has(o)) { back++; if (names.length < 6) names.push(o.type + ':' + (o.name || '') ); } }); return [back, names, window.__oldN || 0]; })()"
bad = 0
with sync_playwright() as pw:
    for tag, src in (('off', S), ('EVENTS_ON', re.sub(r'const EVENTS_ON = false;', 'const EVENTS_ON = true;', S, count=1))):
        p = WORK / 'test' / f'_detach_play_{tag}.html'; p.write_text(src); errs = []
        g = Game(pw, str(p), 390, 844, errs); log = []
        for k in range(20):
            g.step(300); r = g.ev(CHECK); log.append(('arrival', k, g.ev('deckDef.num'), r[0]))
            if r[0]: print('BACK', tag, 'arrival', r); bad += 1
        for d, m in ((0, 19 * 60), (2, 7 * 60 + 10), (4, 20 * 60 + 30), (5, 16 * 60 + 10), (7, 18 * 60 + 30)):
            g.ev(f'setShipNow({d * 1440 + m})')
            for n in (3, 5, 2, 1, 6, 7, 4):
                g.ev(f'goToDeck({n}); updateDeckCrew(0.05)'); g.step(90); r = g.ev(CHECK); log.append((d, m, n, r[0]))
                if r[0]: print('BACK', tag, d, m, n, r); bad += 1
        g.ev('goToDeck(3)'); g.ev('skipTo(shipNow() + 1440 * 2)'); g.step(60)
        for n in (5, 2, 1, 6, 7, 4, 3):
            g.ev(f'goToDeck({n}); updateDeckCrew(0.05)'); g.step(90); r = g.ev(CHECK)
            if r[0]: print('BACK', tag, 'after skip', n, r); bad += 1
        print(tag, 'checks', len(log) + 7, 'decks unloaded', g.ev('window.__oldN'), 'errors', errs[:4], flush=True)
        if errs: bad += 1
        g.close()
print('DETACH PLAY OK' if not bad else f'DETACH PLAY: {bad} problem(s)')
