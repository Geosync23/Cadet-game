# RV29: Day 73 ~20:10, Card night and the tasting table on at once: standing in each joinable tradition's room, does the join
# (TJ_NOW, the arrow's goal) name that one? (TR1's overlap shape; after TB3 + TB4 merge.) usage: overlap73.py WT BUILD [DAY MIN]
import sys, json, types
from playwright.sync_api import sync_playwright
src = open(sys.argv[1] + '/cadet_test.py').read(); src = src[:src.index('import sys, json, hashlib')]
ct = types.ModuleType('ct'); exec(src, ct.__dict__)
D, M = (int(sys.argv[3]), int(sys.argv[4])) if len(sys.argv) > 4 else (73, 20 * 60 + 10)
with sync_playwright() as pw:
    g = ct.Game(pw, sys.argv[2])
    g.ev(f"skipTo({(D - 1) * 1440 + M - 3}); SHIP.device.settings.tips = true"); g.step(20)
    on = g.ev(f"eventsOn({D}).filter(e => tradJoinable(e) && e.from <= {M} && {M} < e.to).map(e => [e.id, [...(e.rooms || (e.rooms = eventRooms(e.ev)))]])")
    print('on now:', on)
    for eid, rooms in on:
        for r in rooms:
            dk, rk = r.split('|')
            g.ev(f"(() => {{ if (deckDef.num !== {dk}) goToDeck({dk}, null); const tl = ROOM_TILES['{rk}'], c = cellPos(...tl[Math.floor(tl.length / 2)]); player.obj.position.copy(cellPos(...nearestOpen(c.x, c.z, player))); player.stop(); }})()")
            for _ in range(4): g.step(30)
            print(f'  in {eid} room {r}:', g.ev("JSON.stringify({ m: hhmm(SHIP.time.min % 1440), tj: TJ_NOW && [TJ_NOW.e.id, TJ_NOW.lead], mark: !!(TJ_MARK && TJ_MARK.style.display === 'block'), goal: typeof IX_GOAL !== 'undefined' && IX_GOAL ? IX_GOAL.label : null })"))
    print('errors', g.errors[:3]); g.close()
