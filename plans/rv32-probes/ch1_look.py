# RV32 probe (0.99.7, CH1 notes 1 and 37): close-up renders of heads (hair) and feet, makeCharacter people and crowd people,
# with a magenta skin so skin showing through hair can be counted. Usage (from the repo root, cadet_test.py beside it):
#   python3 plans/rv32-probes/ch1_look.py BUILD.html OUTPREFIX
# Writes OUTPREFIX_<hair>_<who>_<view>.png and prints the magenta pixel count above the brow for each.
import sys, os, base64, json
sys.argv, (BUILD, OUT) = [sys.argv[0]], sys.argv[1:3]
src = open('cadet_test.py').read().split('\ndef run(')[0]
exec(src)
JS = r'''(([hair, who, view, foot]) => {
  const pp = player.obj.position, x0 = pp.x, z0 = pp.z;
  const spec = { hair, hairColor: '#202020', skin: '#ff00ff', dept: 'works' };
  let obj, h;
  if (who === 'crew') { const rig = makeCharacter(spec); obj = rig.root; obj.position.set(x0, 0, z0); scene.add(obj); obj.updateMatrixWorld(true); }
  else { h = crowd.add(spec); h.set({ x: x0, y: 0, z: z0 }, 0, 'stand'); crowd.update(1 / 30, 1); crowd.update(1 / 30, 1.1); }
  const cam = new THREE.PerspectiveCamera(22, 1, .05, 50);
  const hy = foot ? .06 : 1.62, r = foot ? .9 : .75;
  const V = { back: [0, .25, -1], top: [0, 1.6, -.4], side: [1, .3, 0], front: [0, .1, 1], game: [.55, 1.2, .55] }[view];
  const n = Math.hypot(...V); cam.position.set(x0 + V[0] / n * r, hy + V[1] / n * r, z0 + V[2] / n * r); cam.lookAt(x0, hy, z0);
  player.obj.visible = false;
  const old = renderer.getSize(new THREE.Vector2()); renderer.setSize(320, 320, false);
  renderer.render(scene, cam);
  const gl = renderer.getContext(), px = new Uint8Array(320 * 320 * 4); gl.readPixels(0, 0, 320, 320, gl.RGBA, gl.UNSIGNED_BYTE, px);
  const url = renderer.domElement.toDataURL('image/png');
  let mag = 0; for (let i = 0; i < px.length; i += 4) { const r_ = px[i], g = px[i + 1], b = px[i + 2]; if (r_ > 90 && b > 90 && g < .55 * Math.min(r_, b)) mag++; }
  renderer.setSize(old.x, old.y, false); player.obj.visible = true;
  if (obj) scene.remove(obj); if (h) crowd.remove(h);
  return { url, mag };
})'''
res = {}
with sync_playwright() as pw:
    g = Game(pw, BUILD); g.step(20)
    for hair in ['short', 'buzz', 'curls', 'bun', 'ponytail', 'long']:
        for who in ['crew', 'crowd']:
            for view in ['back', 'top', 'side', 'front', 'game']:
                o = g.ev(JS + json.dumps([[hair, who, view, False]]).replace('[[', '([', 1)[0:0] + '(' + json.dumps([hair, who, view, False]) + ')')
                open(f'{OUT}_{hair}_{who}_{view}.png', 'wb').write(base64.b64decode(o['url'].split(',')[1]))
                res[f'{hair} {who} {view}'] = o['mag']
    for who in ['crew', 'crowd']:
        for view in ['side', 'game', 'front']:
            o = g.ev(JS + '(' + json.dumps(['short', who, view, True]) + ')')
            open(f'{OUT}_feet_{who}_{view}.png', 'wb').write(base64.b64decode(o['url'].split(',')[1]))
    print('errors', g.errors[:5])
print(json.dumps(res))
