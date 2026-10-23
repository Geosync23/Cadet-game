# RV10: live, Day 0 18:38 on Deck 3: set the goodnight at 18:40 and watch the crew whose current place changes
import sys, os, re, pathlib, json
GAME, CT = sys.argv[1], sys.argv[2]
exec(open(CT + '/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    g = Game(pw, GAME, 390, 844); g.step(3)
    g.ev("localStorage.clear()"); g.ev("newGameStart(true)"); g.step(5)
    try: g.page.fill('form input[maxlength="24"]', 'Sam'); g.page.click('form button'); g.step(5)
    except Exception as e: print('sign:', str(e)[:80])
    g.ev("(() => { goToDeck(3); setShipNow(-1440 + 1118); deckCrewFill(); })()"); g.step(150)
    W = "(() => { const o = {}; for (const a of DECK_CREW) if (a.p) o[a.p.id] = [a.goalId || null, +a.x.toFixed(2), +a.z.toFixed(2), !!a.settled]; return o; })()"
    s0 = g.ev(W); t0 = g.ev("clockText()")
    g.ev("SHIP.intro.done.free = Math.floor(shipNow())"); g.step(5); s1 = g.ev(W)
    for _ in range(4): g.step(60)
    s2 = g.ev(W); t2 = g.ev("clockText()")
    moved = {k: [s0[k], s1.get(k), s2.get(k)] for k in s0 if k in s2 and s0[k][3] and s0[k][0] != s2[k][0]}
    print(t0, '->', t2, 'on deck', len(s0), 'settled before', sum(1 for v in s0.values() if v[3]))
    for k, v in moved.items(): print('  ', k, v)
    g.close()
