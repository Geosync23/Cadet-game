# RV32 probe (0.99.7, CH1 note 10): Deck 4 closet 'y' (officers' wing breaker cabinet, 4-junction-2) seen from outside the hull,
# from above and from inside, and the machine's fault lamp. Usage (repo root): ch1_relay.py BUILD.html OUTPREFIX
import sys, base64, json
sys.argv, (BUILD, OUT) = [sys.argv[0]], sys.argv[1:3]
exec(open('cadet_test.py').read().split('\ndef run(')[0])
INFO = r'''(() => { const tl = ROOM_TILES['y']; let x = 0, z = 0; for (const [i, j] of tl) { const c = cellPos(i, j); x += c.x; z += c.z; } x /= tl.length; z /= tl.length;
  const m = DECKS[4].machines.find(q => q.id === '4-junction-2');
  // where the hull is: the nearest hull point to the room's centre
  let hb = null; for (const p of HULL_PTS) { const d = Math.hypot((p.x ?? p[0]) - x, (p.z ?? p[1]) - z); if (!hb || d < hb[0]) hb = [d, p.x ?? p[0], p.z ?? p[1]]; }
  return { tiles: tl, cx: x, cz: z, look: m && m.look, hull: hb }; })()'''
SHOT = r'''(([px, py, pz, tx, ty, tz]) => { const cam = new THREE.PerspectiveCamera(40, 1.5, .05, 80); cam.position.set(px, py, pz); cam.lookAt(tx, ty, tz);
  const old = renderer.getSize(new THREE.Vector2()); renderer.setSize(600, 400, false); renderer.render(scene, cam);
  const u = renderer.domElement.toDataURL('image/png'); renderer.setSize(old.x, old.y, false); return u; })'''
with sync_playwright() as pw:
    g = Game(pw, BUILD); g.ev('SHIP.device && SHIP.device.settings && 0'); g.step(5)
    inf = g.ev(INFO); print(json.dumps(inf)); print('fault', g.ev("(() => { try { machineFault('4-junction-2'); return 1; } catch (e) { return String(e); } })()")); g.step(10)
    cx, cz = inf['cx'], inf['cz']; hx, hz = inf['hull'][1], inf['hull'][2]
    cx, cz = 17.5, 9.5   # the cabinet (ITEMS 'Breaker cabinet' at x 17.5, z 9.65 / 9.3 on); the hull is the deck's z = 10 edge
    views = {'outside': (cx + 1.5, 1.4, cz + 3.0, cx, 1.0, cz), 'outside_hi': (cx - 1.0, 3.5, cz + 2.6, cx, .8, cz), 'top': (cx, 6, cz - 1.2, cx, 0, cz), 'inside': (cx - .3, 1.7, cz - 2.2, cx, 1.0, cz)}
    for k, v in views.items():
        u = g.ev(SHOT + '(' + json.dumps(list(v)) + ')'); open(f'{OUT}_{k}.png', 'wb').write(base64.b64decode(u.split(',')[1]))
    print('errors', g.errors[:5])
