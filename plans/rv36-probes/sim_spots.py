# RV36: the sim bay's places and who's at each, with positions, while a pilot has given you their pod (Day 3 19:52)
import sys
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("a, shots = run(")[0])
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844); g.step(3)
    if g.ev("typeof GUIDE_ON !== 'undefined' && GUIDE_ON"): g.ev("GUIDE.tq.length = 0; guideToast = () => false")
    g.ev("skipTo(2 * 1440 + 19 * 60 + 40); goToDeck(7); const b = ROOM_BOX.S; player.obj.position.copy(cellPos(Math.floor((b.i0 + b.i1) / 2), Math.floor((b.j0 + b.j1) / 2))); target.copy(player.obj.position).setY(.7)")
    g.step(30*8); g.ev("tradJoinTap(DECK_CREW.find(c => c.p && c.p.id === 'raman'))"); g.step(10)
    for i in range(4):
        if g.ev("!!DIALOGUE"): g.ev("dialogueNext()"); g.step(3)
    g.step(30*12)
    for r in g.ev("[...PLACE_OF.values()].filter(q => /^7-sim/.test(q.id)).map(q => { const c = heldBy(q.id); return [q.id, q.at, q.pose, c && c.p ? c.p.id : '-']; })"): print(r)
    for r in g.ev("DECK_CREW.filter(c => c.p && Math.hypot(c.x - 6, c.z - 3) < 6).map(c => [c.p.id, +c.x.toFixed(2), +c.z.toFixed(2), c.spot && c.spot.id, c.goalId, c.pose || c.anim || ''])"): print(r)
    print(g.ev("[+player.obj.position.x.toFixed(2), +player.obj.position.z.toFixed(2)]"), g.errors[:3]); g.close()
