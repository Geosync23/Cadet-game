import sys
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844)
    g.ev("skipTo(3 * 1440 + 13 * 60 + 57); goToDeck(3); const tl = ROOM_TILES['=']; player.obj.position.copy(cellPos(...tl[(tl.length/2)|0]))"); g.step(10)
    for k in range(6):
        g.ev("skipTo(Math.floor(shipNow()) + 1)"); g.step(20)
        print(g.ev("JSON.stringify([Math.round(SHIP.time.min), roomAt(...player.here()), goalNow() && goalNow().label, TJ_NOW && TJ_NOW.lead, (() => { const a = DECK_CREW.find(c => c.p.id === 'sato'); if (!a) return 'sato off deck'; return [a.spot && a.spot.id, Math.round(Math.hypot(a.x - player.obj.position.x, a.z - player.obj.position.z))]; })()])"))
    g.page.screenshot(path='/tmp/rv33/merge/ll_prom.png')
