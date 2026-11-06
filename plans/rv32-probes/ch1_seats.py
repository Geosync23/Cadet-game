# RV32 probe (0.99.7, CH1 note 35): the auditorium seats on the rec deck filled with crowd people in 'sit:slump', rendered
# from beside a row and from the front, plus the two beanbags. Usage (repo root): ch1_seats.py BUILD.html OUTPREFIX
import sys, base64, json
sys.argv, (BUILD, OUT) = [sys.argv[0]], sys.argv[1:3]
exec(open('cadet_test.py').read().split('\ndef run(')[0])
FILL = r'''(() => { goToDeck(7); const out = [];
  for (const id of ['7-seat-1','7-seat-2','7-seat-3','7-seat-4','7-seat-5','7-seat-6','7-seat-7','7-seat-8','7-seat-9','7-seat-10','7-seat-11','7-seat-12','7-beanbag-1','7-beanbag-2']) {
    const s = placeSpot(id); if (!s) continue; const h = crowd.add({ dept: 'works', hair: 'short', skin: 2 }); h.set({ x: s.x, y: s.y || 0, z: s.z }, s.face, 'sit:slump'); out.push([id, +s.x.toFixed(2), +(s.y||0).toFixed(2), +s.z.toFixed(2), +s.face.toFixed(2)]); }
  return out; })()'''
SHOT = r'''(([px, py, pz, tx, ty, tz]) => { const cam = new THREE.PerspectiveCamera(35, 1.5, .05, 80); cam.position.set(px, py, pz); cam.lookAt(tx, ty, tz);
  player.obj.visible = false; const old = renderer.getSize(new THREE.Vector2()); renderer.setSize(600, 400, false); renderer.render(scene, cam);
  const u = renderer.domElement.toDataURL('image/png'); renderer.setSize(old.x, old.y, false); player.obj.visible = true; return u; })'''
with sync_playwright() as pw:
    g = Game(pw, BUILD); g.step(5)
    seats = g.ev(FILL); print(seats)
    for k in range(40): g.ev('crowd.update(1/30, %f)' % (k / 30))
    for (name, sid) in [('seat1', 0), ('seat5', 4), ('bean', 12)]:
        if sid >= len(seats): continue
        _, x, y, z, f = seats[sid]
        import math
        fx, fz = math.sin(f), math.cos(f)       # facing direction (0 looks toward +z)
        for view, (dx, dy, dz) in {'front': (fx * 1.6, 1.1, fz * 1.6), 'side': (fz * 1.6, 1.0, -fx * 1.6), 'high': (fx * 1.2 + fz * .8, 2.2, fz * 1.2 - fx * .8)}.items():
            u = g.ev(SHOT + '(' + json.dumps([x + dx, y + dy, z + dz, x, y + .55, z]) + ')')
            open(f'{OUT}_{name}_{view}.png', 'wb').write(base64.b64decode(u.split(',')[1]))
    print('errors', g.errors[:5])
