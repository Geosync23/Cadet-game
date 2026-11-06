import sys
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844)
    for where in ['A', 'out']:
        g.ev("skipTo(4 * 1440 + 16 * 60 + 8); goToDeck(7); const tl = ROOM_TILES['A']; player.obj.position.copy(cellPos(...tl[(tl.length/2)|0]))" if where == 'A' else "skipTo(4 * 1440 + 16 * 60 + 8); goToDeck(3)")
        g.step(30)
        t0 = g.ev("shipNow()"); g.step(300); t1 = g.ev("shipNow()")
        print(where, 'ship minutes per 10 real s:', round(t1 - t0, 2), 'room', g.ev("roomAt(...player.here())"), 'rate', g.ev("typeof CL997_RATE !== 'undefined' ? CL997_RATE : 'n/a'"))
