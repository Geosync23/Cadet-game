import sys
exec(open("/home/user/Cadet-game/cadet_test.py").read().split("a, shots = run(")[0])
S = sys.argv[2]
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844)
    g.page.set_viewport_size({'width': 390, 'height': 844})
    g.step(3)
    if g.ev("typeof GUIDE_ON !== 'undefined' && GUIDE_ON"): g.ev("GUIDE.tq.length = 0; guideToast = () => false")
    g.ev("skipTo(3 * 1440 + 14 * 60 + 7); goToDeck(1); const b = ROOM_BOX[Object.keys(ROOMS).find(k => /^Observation room/.test(ROOMS[k].name))]; player.obj.position.copy(cellPos(Math.floor((b.i0 + b.i1) / 2), Math.floor((b.j0 + b.j1) / 2))); target.copy(player.obj.position).setY(.7)")
    g.step(30)
    base = g.ev("[hemi.color.getHexString(), +hemi.intensity.toFixed(3)]")
    g.page.screenshot(path=S + '/blink-before.png')
    seen = []
    for k in range(260):
        g.step(1)
        r = g.ev("[SHIP.time.min|0, FEEL_S.kinds.join(), hemi.color.getHexString(), +hemi.intensity.toFixed(3), +(simNow()/1000 - FEEL_S.t0).toFixed(2)]")
        if 'beacon' in r[1]:
            seen.append(r)
            if len(seen) == 12: g.page.screenshot(path=S + '/blink-peak.png')
    print('base', base); print('first', seen[:1], 'n', len(seen))
    for r in seen[::6]: print(r)
    print('toast', g.ev("document.getElementById('toast') && document.getElementById('toast').textContent.slice(0, 120)"))
    print('felt key', g.ev("SHIP.event && SHIP.event.mine['felt:lastLightBlink']"), g.errors[:3])
    g.close()
