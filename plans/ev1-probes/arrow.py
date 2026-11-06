import sys
exec(open("/home/user/Cadet-game/cadet_test.py").read().split("a, shots = run(")[0])
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844); g.step(3)
    g.ev("skipTo(3 * 1440 + 9 * 60 + 5); careerClock(shipNow(), true)"); g.step(5)
    ST = "[SHIP.time.min|0, careerClockedIn(4), lightEasyNow(), (() => { const x = ixWorkStep(); return x && x.label; })(), typeof GUIDE !== 'undefined' && GUIDE_ON ? (GUIDE.asks || GUIDE.q || []).length : 'noguide', IX_GOAL && IX_GOAL.label, roomAt(...player.here())]"
    for t, lounge in [(13*60+55, False), (14*60+5, False), (14*60+5, True), (14*60+35, True)]:
        g.ev(f"skipTo(3 * 1440 + {t}); goToDeck({3 if lounge else 5})" + ("; { const b = ROOM_BOX.L; player.obj.position.copy(cellPos(Math.floor((b.i0 + b.i1) / 2), Math.floor((b.j0 + b.j1) / 2))); target.copy(player.obj.position).setY(.7); }" if lounge else ""))
        g.step(30*2)
        print(t//60, t%60, 'lounge' if lounge else 'works', g.ev(ST))
    print(g.errors[:3]); g.close()
