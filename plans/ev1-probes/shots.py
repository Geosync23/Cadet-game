import sys
exec(open("/home/user/Cadet-game/cadet_test.py").read().split("a, shots = run(")[0])
S = sys.argv[2]
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844); g.step(3)
    if g.ev("typeof GUIDE_ON !== 'undefined' && GUIDE_ON"): g.ev("GUIDE.tq.length = 0; guideToast = () => false")
    # reading corner Day 21
    g.ev("skipTo(20 * 1440 + 16 * 60 + 2); goToDeck(3); const b = ROOM_BOX.L; player.obj.position.copy(cellPos(Math.floor((b.i0 + b.i1) / 2), Math.floor((b.j0 + b.j1) / 2))); target.copy(player.obj.position).setY(.7)")
    g.step(30*4)
    g.ev("(() => { const e = eventsOn(21).find(x => x.id === 'reading-corner'); tradJoinMinute(shipNow()); const a = DECK_CREW.find(c => c.p && c.p.id === 'kowalczyk') || DECK_CREW.find(c => c.p && evTagId(c.tag||'') === 'reading-corner'); return tradJoin(e, a); })()")
    for k in range(90):
        g.step(30)
        if g.ev("!!DIALOGUE"): break
    g.page.screenshot(path=S + '/read-card.png')
    g.ev('null')
    for j in range(4):
        if g.ev("(() => { if (!DIALOGUE) return 2; const v = dialogueView(); return v && v.choices ? 1 : 0; })()"): g.ev("dialogueChoose(1)"); break
        g.ev("dialogueNext()"); g.step(3)
    for j in range(4):
        if g.ev("!!DIALOGUE"): g.ev("dialogueNext()"); g.step(3)
    # Saturday jigsaw Day 6
    g.ev("skipTo(5 * 1440 + 11 * 60); goToDeck(1); const b = ROOM_BOX[Object.keys(ROOMS).find(k => /Observation room/.test(ROOMS[k].name || ROOMS[k]))] ; if (b) { player.obj.position.copy(cellPos(Math.floor((b.i0 + b.i1) / 2), Math.floor((b.j0 + b.j1) / 2))); target.copy(player.obj.position).setY(.7); }")
    g.step(30*6); g.page.screenshot(path=S + '/sat-jigsaw.png')
    print(g.ev("[deckDef.num, roomAt(...player.here()), DECK_CREW.filter(c => c.p && evTagId(c.tag||'') === 'big-jigsaw').map(c => c.p.id)]"))
    print(g.errors[:3]); g.close()
