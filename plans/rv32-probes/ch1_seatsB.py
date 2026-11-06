# RV32 probe (0.99.7, CH1 note 4): people seated at the seats CH1 moved (crowd people, the place's own pose and anim, at
# placeSpot's spot), rendered from beside and in front. Usage (repo root): ch1_seatsB.py BUILD.html OUTPREFIX
import sys, base64, json, math
sys.argv, (BUILD, OUT) = [sys.argv[0]], sys.argv[1:3]
exec(open('cadet_test.py').read().split('\ndef run(')[0])
SEATS = [(3, '3-infirmary-1'), (3, '3-infirmary-4'), (3, '3-lounge-25'), (3, '3-bench-17'), (2, '2-armchair-1'), (2, '2-armchair-4'),
         (2, '2-comms-5'), (5, '5-office-1'), (5, '5-tea-1'), (4, '4-common-4'), (7, '7-stand-1'), (7, '7-stand-30'), (7, '7-seat-40'), (7, '7-sim-1'), (7, '7-booth-1')]
FILL = r'''(([deck, id]) => { if (deckDef.num !== deck) goToDeck(deck); crowd.clear && crowd.clear(); const s = placeSpot(id), pl = PLACE_OF.get(id); if (!s) return null;
  const pose = (typeof poseOf === 'function' ? poseOf(pl) : null) || s.pose || 'sit'; const h = crowd.add({ dept: 'works', hair: 'short', skin: 2 });
  h.set({ x: s.x, y: s.y || 0, z: s.z }, s.face, pose); for (let k = 0; k < 40; k++) crowd.update(1 / 30, k / 30);
  return [+s.x.toFixed(3), +(s.y || 0).toFixed(3), +s.z.toFixed(3), +s.face.toFixed(3), pose, s.fy === undefined ? null : s.fy]; })'''
SHOT = r'''(([px, py, pz, tx, ty, tz]) => { const cam = new THREE.PerspectiveCamera(40, 1, .05, 80); cam.position.set(px, py, pz); cam.lookAt(tx, ty, tz);
  player.obj.visible = false; const old = renderer.getSize(new THREE.Vector2()); renderer.setSize(360, 360, false); renderer.render(scene, cam);
  const u = renderer.domElement.toDataURL('image/png'); renderer.setSize(old.x, old.y, false); player.obj.visible = true; return u; })'''
res = {}
with sync_playwright() as pw:
    g = Game(pw, BUILD); g.step(5)
    for deck, sid in SEATS:
        s = g.ev(FILL + '(' + json.dumps([deck, sid]) + ')'); res[sid] = s
        if not s: continue
        x, y, z, f = s[0], s[1], s[2], s[3]; fx, fz = math.sin(f), math.cos(f)
        for view, (dx, dy, dz) in {'front': (fx * 1.5 + fz * .5, 1.2, fz * 1.5 - fx * .5), 'side': (fz * 1.4, .9, -fx * 1.4)}.items():
            u = g.ev(SHOT + '(' + json.dumps([x + dx, y + dy, z + dz, x, y + .35, z]) + ')')
            open(f'{OUT}_{sid}_{view}.png', 'wb').write(base64.b64decode(u.split(',')[1]))
    print(json.dumps(res)); print('errors', g.errors[:5])
