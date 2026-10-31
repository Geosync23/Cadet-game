# TR1: two joinable traditions on one deck at once: standing in each one's room, does the join (TJ_NOW, the arrow) name that one?
# Day 6 15:40 Deck 3: Tiles ladder (bow lounge L) vs Cook-along (galley K). Usage: overlap_probe.py BUILD.html
import sys, json
sys.argv, ARGS = sys.argv[:1], sys.argv[1:]
exec(open("/home/user/cadet-game/cadet_test.py").read().split("a, shots = run(")[0].replace("timeout=60000", "timeout=240000"))
with sync_playwright() as pw:
    g = Game(pw, ARGS[0], 900, 760)
    g.ev("skipTo(5 * 1440 + 15 * 60 + 38); goToDeck(3, null); SHIP.device.settings.tips = true"); g.step(20)
    for room in ['L', 'K', 'L']:
        g.ev("(() => { const tl = ROOM_TILES['%s'], c = cellPos(...tl[Math.floor(tl.length / 2)]); player.obj.position.set(c.x, 0, c.z); player.stop(); })()" % room)
        for _ in range(4): g.step(30)
        print(room, g.ev("JSON.stringify({ m: hhmm(SHIP.time.min % 1440), tj: TJ_NOW && [TJ_NOW.e.id, TJ_NOW.lead], goal: typeof IX_GOAL !== 'undefined' && IX_GOAL ? IX_GOAL.label : null, on: eventsOn(6).filter(e => tradJoinable(e) && SHIP.time.min >= e.from && SHIP.time.min < e.to).map(e => e.id) })"))
    print('errors', g.errors[:3]); g.close()
