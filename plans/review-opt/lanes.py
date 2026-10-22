# OR2: every walker's drawn lane on each deck (CrewAgent.lane), and WALK_LANE
import sys, json
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("import sys, json, hashlib")[0])
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844); out = {}
    g.ev("setShipNow(9 * 60)")
    for n in (1, 2, 3, 4, 5, 6, 7):
        g.ev(f"goToDeck({n}); updateDeckCrew(0.05)"); g.step(2)
        out[n] = g.ev("DECK_CREW.map(a => +a.lane.toFixed(3))")
    w = g.ev("WALK_LANE"); g.close()
allv = [v for vs in out.values() for v in vs]
print('WALK_LANE', w, 'walkers', len(allv), 'min', min(allv), 'max', max(allv), 'outside +-WALK_LANE', sum(abs(v) > w + 1e-9 for v in allv))
