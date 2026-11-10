# RV36: where the pilot who gave you their pod goes, minute by minute (Day 3). usage: sim_giver.py ON.html SHOT
import sys, json
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("a, shots = run(")[0])
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844); g.step(3)
    if g.ev("typeof GUIDE_ON !== 'undefined' && GUIDE_ON"): g.ev("GUIDE.tq.length = 0; guideToast = () => false")
    g.ev("skipTo(2 * 1440 + 19 * 60 + 40); goToDeck(7); const b = ROOM_BOX.S; player.obj.position.copy(cellPos(Math.floor((b.i0 + b.i1) / 2), Math.floor((b.j0 + b.j1) / 2))); target.copy(player.obj.position).setY(.7)")
    g.step(30*8); g.ev("tradJoinTap(DECK_CREW.find(c => c.p && c.p.id === 'raman'))"); g.step(10)
    for i in range(4):
        if g.ev("!!DIALOGUE"): g.ev("dialogueNext()"); g.step(3)
    for i in range(14):
        g.step(30*2)
        print(g.ev("(() => { const c = DECK_CREW.find(c => c.p && c.p.id === 'santos-zofia'); return [hhmm(SHIP.time.min % 1440), ACT && ACT.kind, c ? [+(c.x||0).toFixed(2), +(c.z||0).toFixed(2), c.goalId, c.spot && c.spot.id, c.state || c.mode || '', c.anim || ''] : 'not on deck']; })()"))
        if i == 5: g.page.screenshot(path=sys.argv[2])
    print(g.errors[:3]); g.close()
