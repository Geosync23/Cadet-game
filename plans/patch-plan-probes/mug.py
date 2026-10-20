# #30 (the mug in your hands), a mock-up only: adds a 'mug' prop and hold at runtime in a scratch run (the game file is
# not changed) and shoots the player holding it at phone size, at the phone's default zoom (1.5) and the widest (0.7).
from pp import *
g = start('?nosave&debug'); g.step(10)
print(g.ev(r"""(() => {
  PROP_KIT.mug = p => {   // a cream mug, cocoa 0.005 below the rim, a handle overlapping the wall (no shared faces)
    part(p, cylG(.042, .038, .095, 12), '#efe6d4', 0, -.075, .065, 1, 1, 1, -Math.PI / 2);
    part(p, cylG(.036, .036, .006, 12), '#6b3e22', 0, -.075, .0225, 1, 1, 1, -Math.PI / 2);
    part(p, GEO.box, '#efe6d4', .05, -.075, .07, .02, .016, .05);
  };
  HOLDS.mug = { prop: 'mug', bone: 'R', one: -1, sx: -.45, ex: -1.25, sz: .1, hx: .25, look: .12 };
  ixHold = () => 'mug';
  return [player.here(), deckDef.num, renderer.info.render.calls];
})()"""))
g.step(30); c1 = g.ev('renderer.info.render.calls'); g.snap('30-mug-zoom15')  # (not kept)
g.ev("ixHold = () => false"); g.step(30); c0 = g.ev('renderer.info.render.calls')
g.ev("ixHold = () => 'mug'; camera.zoom = .7; camera.updateProjectionMatrix()"); g.step(30); g.snap('30-mug-zoom07')
g.ev("camera.zoom = 3; camera.updateProjectionMatrix()"); g.step(30); g.snap('30-mug-mockup')
print('draw calls with the mug', c1, 'without', c0, g.errors[:3])
g.close()
