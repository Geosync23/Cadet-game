import sys, os, re, json
src = open('/home/user/Cadet-game/cadet_test.py').read().split("import sys, json, hashlib")[0]
exec(src)
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844)
    g.ev("setShipNow(6 * 1440 + 18 * 60 + 30); goToDeck(3); updateDeckCrew(.05)"); g.step(5)
    print(g.ev("""(() => { const p = crowd.people[0]; let n = 0, meshes = 0, vis = 0, used = 0; const bones = new Set(p.chunk.skel.bones);
      p.rig.root.traverse(o => { n++; if (o.isMesh) meshes++; if (o.visible) vis++; if (bones.has(o)) used++; });
      const kinds = {}; p.rig.root.traverse(o => { kinds[o.type] = (kinds[o.type] || 0) + 1; });
      return JSON.stringify({ people: crowd.people.length, nodes: n, meshes, visible: vis, bonesUsed: used, joints: p.joints.length, kinds, inScene: !!p.rig.root.parent, parent: p.rig.root.parent && p.rig.root.parent.type, matrixAutoUpdate: p.rig.root.matrixAutoUpdate }); })()"""))
    g.close()
