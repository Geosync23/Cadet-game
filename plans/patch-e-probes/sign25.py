import sys; sys.path.insert(0, '/home/user/Cadet-game/plans/patch-plan-probes')
from pp import *
g = start('?nosave&debug'); g.step(5)
g.ev("goToDeck(2)"); g.step(5)
r = g.ev("(() => { const it = ITEMS.find(i => /directory/i.test(i.t || '')); const p = new THREE.Vector3(); it.g.getWorldPosition(p); return [p.x, p.z, it.x]; })()")
print(r)
g.ev(f"player.obj.position.set({r[0]}+0.6, 0, {r[1]}+0.6); target.copy(player.obj.position).setY(.7); camera.zoom = 4; camera.updateProjectionMatrix()"); g.secs(2)
g.page.screenshot(path=sys.argv[1]); g.close()
