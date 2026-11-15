# per-frame cost by deck and time: ms of game code a frame (no drawing), CPU profile top functions, bytes allocated a frame
import sys; sys.path.insert(0, '' + __import__('os').path.dirname(__import__('os').path.abspath(__file__)) + ''); from g import *
GAME = sys.argv[1]; SC = [(2, '10:00', 5), (2, '12:40', 3), (2, '20:30', 4), (2, '20:30', 7), (2, '10:00', 1), (2, '10:00', 2), (2, '10:00', 6), (2, '03:00', 4)]
if len(sys.argv) > 2: SC = [SC[int(k)] for k in sys.argv[2].split(',')]
with sync_playwright() as pw:
    for day, tm, deck in SC:
        g = Game(pw, GAME); h, m = map(int, tm.split(':'))
        g.ev(f"skipTo({(day - 1) * 1440 + h * 60 + m}); if (deckDef.num !== {deck}) goToDeck({deck})"); g.step(120)
        g.step(1, draw=True); info = g.ev("({calls: renderer.info.render.calls, tris: renderer.info.render.triangles, people: crowd.stats().people, geo: renderer.info.memory.geometries, tex: renderer.info.memory.textures, walkers: walkers.length, deckCrew: typeof DECK_CREW !== 'undefined' ? DECK_CREW.length : null})")
        best = 1e9
        for k in range(4):
            t = g.page.evaluate("(() => { window.__skip = true; const a = window.__realNow(); window.__step(60, 1000/30); window.__skip = false; return (window.__realNow() - a) / 60; })()"); best = min(best, t)
        tot, top = g.profile(lambda: g.step(600))
        g.gc(); ab, atop = g.alloc(lambda: g.step(300))
        print(f"\n== Day {day} {tm} deck {deck}: {json.dumps(info)}  js {best:.2f} ms/frame (best of 4x60)  alloc {ab / 300 / 1024:.1f} KB/frame  errors {g.errors[:2]}")
        print('  cpu (ms over 600 frames):', '; '.join(f"{k} {v:.0f}" for v, k in top[:22]))
        print('  alloc (KB over 300 frames):', '; '.join(f"{k} {v / 1024:.0f}" for v, k in atop[:16]))
        g.close()
