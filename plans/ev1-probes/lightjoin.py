import sys
exec(open("/home/user/Cadet-game/cadet_test.py").read().split("a, shots = run(")[0])
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844); g.step(3)
    if g.ev("typeof GUIDE_ON !== 'undefined' && GUIDE_ON"): g.ev("GUIDE.tq.length = 0; guideToast = () => false")
    g.ev("skipTo(3 * 1440 + 13 * 60 + 58); goToDeck(3); const b = ROOM_BOX.L; player.obj.position.copy(cellPos(Math.floor((b.i0 + b.i1) / 2), Math.floor((b.j0 + b.j1) / 2))); target.copy(player.obj.position).setY(.7)")
    g.step(30*8)
    print(g.ev("tradJoinMinute(shipNow()), [TJ_NOW && TJ_NOW.e.id, TJ_NOW && TJ_NOW.lead, IX_GOAL && IX_GOAL.label, document.getElementById('tjMark') && document.getElementById('tjMark').textContent]"))
    print(g.ev("(() => { const a = DECK_CREW.find(c => c.p && c.p.id === 'sato'); return tradJoinTap ? tradJoinTap(a) : null; })()"))
    g.step(30*10)
    print(g.ev("[ACT && ACT.kind, SHIP.events.joined.filter(k => /lastLight/.test(k)), document.getElementById('toast') && document.getElementById('toast').textContent.slice(0, 160)]"))
    g.page.screenshot(path=sys.argv[2]); print(g.errors[:3]); g.close()
