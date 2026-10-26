import sys, os
G = sys.argv[1]; OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
exec(open(os.path.join(os.path.dirname(G), 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
src = open(G).read().replace('const P926_APPT = true;', 'const EV_VESSEL_ON = true;\nconst P926_APPT = true;', 1)
vp = WORK / 'test' / '_rv21_vsky2.html'; vp.write_text(src)
STUB = open('/tmp/rv21/probe/stub.js').read()
with sync_playwright() as pw:
  for (w, h) in ((390, 844), (900, 760)):
    g = Game(pw, str(vp), w, h)
    g.ev(STUB); g.ev("if (typeof GUIDE_ON !== 'undefined' && GUIDE_ON) { GUIDE.tq.length = 0; guideToast = () => false; }")
    g.ev("skipTo(28 * 1440 + 1055); SHIP.event = null; eventStart('veyliVessel', 27); goToDeck(3)")
    tiles = g.ev("(() => { const t = ROOM_TILES['L'].slice().sort((a, b) => b[0] - a[0]); return { n: t.length, maxI: t[0][0], minI: t[t.length-1][0], bowFrom: deckDef.hull && deckDef.hull.bowFrom, W }; })()")
    print(w, h, tiles)
    picks = g.ev("(() => { const t = ROOM_TILES['L'].slice().sort((a, b) => b[0] - a[0] || a[1] - b[1]); const n = t.length; return [t[0], t[Math.floor(n * .1)], t[Math.floor(n * .25)], t[Math.floor(n / 2)], t[n - 1]]; })()")
    for k, (i, j) in enumerate(picks):
        g.ev(f"(() => {{ setShipNow(28 * 1440 + 1060.6); EV_MIN = -1; eventsTick(); const c = cellPos({i}, {j}); player.obj.position.copy(cellPos(...nearestOpen(c.x, c.z, player))); player.stop(); target.copy(player.obj.position).setY(.7); }})()")
        g.step(40)
        info = g.ev("({ sky: !!VSKY.m, P: VSKY.m ? VSKY.m.material.uniforms.uP.value.toArray().map(Math.round) : null, S: VSKY.m ? Math.round(VSKY.m.material.uniforms.uS.value) : null, at: player.here() })")
        on = info['P'] and 0 <= info['P'][0] <= w and 0 <= info['P'][1] <= h
        print(f'  tile {i},{j}', info, 'ON SCREEN' if on else 'off screen')
        g.shot(f'{OUT}/bow_{w}_{k}.png')
    print('errors', g.errors[:4]); g.close()
