import sys, json
CC = sys.argv[1]; GAMEF = sys.argv[2]; sys.argv = [CC, GAMEF, 'none']
__file__ = CC; exec(open(CC).read().split('\nwith sync_playwright() as pw:')[0])
on = with_switch(GAME.read_text(), True)
with sync_playwright() as pw:
    r = Run(pw, on, 'dbgm2', mode='pad', plug={}, w=390, h=844)
    r.ev("SHIP.device.settings.tips = false"); r.step(10); r.press('B'); r.step(2)
    r.ev("goToDeck(3, null)"); r.step(60)
    ids = r.ev("[...PLACE_OF.values()].filter(p => p.type === 'mess-seat').map(p => p.id)")
    got, miss = [], []
    for sid in ids:
        sp = r.ev(f"(() => {{ const s = placeSpot('{sid}'); return {{ x: s.x, z: s.z }}; }})()")
        r.ev(f"({STAND_BY})({json.dumps(sp)})"); r.step(72)
        ks = r.ev("padTargets().map(x => x.key)")
        (got if 'place:' + sid in ks else miss).append(sid)
    print(GAMEF, 'mess seats offered', len(got), 'of', len(ids), 'missed:', miss)
    r.close()
