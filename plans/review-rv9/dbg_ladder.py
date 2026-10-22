import sys, json
CC = sys.argv[1]; GAMEF = sys.argv[2]; sys.argv = [CC, GAMEF, 'none']
__file__ = CC; exec(open(CC).read().split('\nwith sync_playwright() as pw:')[0])
on = with_switch(GAME.read_text(), True)
INFO = """(() => { const e = ladderHatch(), lr = ladderRoom(), L = ladderAt(); return { on: LADDER_ON, hatch: e ? [e.cx, e.cz, e.type, Object.keys(CLOSED_DOORS).filter(k => EDGES.get(k) === e)] : null,
  room: lr ? [lr.i, lr.j] : null, ladder: L ? [L.x, L.z] : null, deck: deckDef.num, me: [player.obj.position.x, player.obj.position.z] }; })()"""
with sync_playwright() as pw:
    for deck in (4, 3):
        r = Run(pw, on, 'dbgl', mode='pad', plug={}, w=390, h=844)
        r.ev("SHIP.device.settings.tips = false"); r.step(10); r.press('B'); r.step(2)
        if deck != 4: r.ev(f"goToDeck({deck}, null)"); r.step(60)
        inf = r.ev(INFO); print(GAMEF, 'deck', deck, inf)
        if inf['hatch']:
            for k, (ox, oz) in enumerate(((0, 0), (1.2, 0), (-1.2, 0), (0, 1.2), (0, -1.2))):
                r.ev(f"({STAND_BY})({json.dumps({'x': inf['hatch'][0] + ox, 'z': inf['hatch'][1] + oz})})"); r.step(72)
                keys = r.ev("padTargets().map(x => x.key.startsWith('item:') ? x.key + ' ' + ITEMS[+x.key.slice(5)].t : x.key)")
                h = r.ev(HINT)
                print('  by the hatch', (ox, oz), 'targets', keys, 'hint', h)
            # what the pad's padWhat says over the hatch door's screen points
            sc = r.ev("""(() => { const e = ladderHatch(); const out = {}; for (let y = .2; y < 2.2; y += .2) { const s = padScreen(e.cx, y, e.cz); if (s) { const w = padWhat(s[0], s[1], 'x'); out[w] = (out[w] || 0) + 1; } } return out; })()""")
            print('  padWhat at the hatch middle, 10 heights:', sc)
        # A on whatever is offered with the ladder words, then where are we
        r.close()
