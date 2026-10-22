import sys, json
CC = sys.argv[1]; GAMEF = sys.argv[2]; sys.argv = [CC, GAMEF, 'none']
__file__ = CC; exec(open(CC).read().split('\nwith sync_playwright() as pw:')[0])
on = with_switch(GAME.read_text(), True)
with sync_playwright() as pw:
    r = Run(pw, on, 'dbgm', mode='pad', plug={}, w=390, h=844)
    r.ev("SHIP.device.settings.tips = false"); r.step(10); r.press('B'); r.step(2)
    r.ev("goToDeck(3, null)"); r.step(60)
    print(GAMEF, r.ev("[...PLACE_OF.values()].filter(p => p.type === 'mess-seat').length"), r.ev("padPlaces().filter(([p]) => p.type === 'mess-seat').length"),
          r.ev("[...PLACE_OF.values()].filter(p => p.type === 'mess-seat').slice(0,2).map(p => [p.id, !!FLOOR_ACTS[p.type], SIT_TYPES.has(p.type), p.pose, PRIVATE_TYPES.has(p.type), privatePlace(p)])"))
    sp = r.ev("(() => { const s = placeSpot('3-mess-1'); return { x: s.x, z: s.z }; })()")
    r.ev(f"({STAND_BY})({json.dumps(sp)})"); r.step(72)
    print(r.ev("padTargets().map(x => x.key + ' ' + x.d.toFixed(2))"))
    r.close()
