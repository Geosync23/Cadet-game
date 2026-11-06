import sys, json
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    for path in sys.argv[1:]:
        g = Game(pw, path, 900, 760)
        g.ev("(() => { skipTo(5 * 1440 + 600); goToDeck(3, null); return 1; })()"); g.step(60)
        r = g.ev("JSON.stringify({ n: DECK_CREW.length, garden: DECK_CREW.filter(a => a.spot && /garden|tend|bed/i.test(a.spot.id || '')).length })")
        print(path.split('/')[-1], r); g.close()
