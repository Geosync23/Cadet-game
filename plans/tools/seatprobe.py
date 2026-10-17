# every seat place on every deck: a stand-in sits there; hips and knees vs the surface under them
import sys, json, collections
src = open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..', '..', 'cadet_test.py')).read().split("a, shots = run(")[0]
sv = sys.argv; sys.argv = ['x']; exec(src); sys.argv = sv
from playwright.sync_api import sync_playwright
SETUP = """(() => { crowd.clear && 0; window.__st = []; let n = 0;
  for (const pl of DECKS[deckDef.num].places || []) { const pose = poseOf(pl); if (!/^sit/.test(pose) && !(pl.pose === 'sit')) continue; const sp = placeSpot(pl.id); if (!sp) continue;
    const h = crowd.add(rosterSpec(ROSTER[(n++ * 7) % ROSTER.length])); h.set({ x: sp.x, y: sp.y || 0, z: sp.z }, sp.face, /^sit/.test(pose) ? pose : 'sit'); __st.push([h, sp, pl, pose]); }
  return __st.length; })()"""
TICK = "for (const [h, sp, pl, pose] of __st) h.set({ x: sp.x, y: sp.y || 0, z: sp.z }, sp.face, /^sit/.test(pose) ? pose : 'sit')"
MEAS = """(() => { const out = [], v = new THREE.Vector3(), w = new THREE.Vector3(), m4 = new THREE.Matrix4(), rc = new THREE.Raycaster(), all = [];
  deckRoot.traverse(o => { if (o.isMesh && !o.isSkinnedMesh && !o.isInstancedMesh && !(SHADOW_PROXY.some(p => p.mesh === o))) all.push(o); });
  const surf = (x, y, z) => { rc.set(w.set(x, y, z), new THREE.Vector3(0, -1, 0)); rc.far = 1.5; const hs = rc.intersectObjects(all, false); return hs.length ? hs[0].point.y : null; };
  const lowOf = (p, j) => { const ji = p.joints.indexOf(j); let l = Infinity; for (const q of p.jparts[ji] || []) { const b = q.geo.boundingBox || (q.geo.computeBoundingBox(), q.geo.boundingBox); m4.multiplyMatrices(j.matrixWorld, q.m);
    for (let c = 0; c < 8; c++) { v.set(c & 1 ? b.max.x : b.min.x, c & 2 ? b.max.y : b.min.y, c & 4 ? b.max.z : b.min.z).applyMatrix4(m4); l = Math.min(l, v.y); } } return l; };
  for (const [h, sp, pl, pose] of __st) { h.rig.root.updateMatrixWorld(true);
    const hips = h.rig.hips.getWorldPosition(new THREE.Vector3()), legs = h.rig.legs.map(l => l.knee.getWorldPosition(new THREE.Vector3()));
    const thighs = h.rig.legs.map(l => l.thigh), sH = surf(hips.x, hips.y + .25, hips.z);
    const thLow = Math.min(...thighs.map(t => lowOf(h, t))), kneeS = legs.map(k => surf(k.x, k.y + .1, k.z));
    out.push({ id: pl.id, type: pl.type, pose, y: sp.y || 0, seatHit: sH === null ? null : +sH.toFixed(3), thighLow: +thLow.toFixed(3), hipY: +hips.y.toFixed(3), kneeS: kneeS.map(s => s === null ? null : +s.toFixed(3)), kneeY: legs.map(k => +k.y.toFixed(3)) }); }
  return JSON.stringify(out); })()"""
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1]); res = []
    g.ev("crewOn = false; crowd.visible = true; for (const c of crew) c.setActive(false);")
    for d in [1, 2, 3, 4, 5, 6]:
        g.ev(f"goToDeck({d}); deckCrewClear && deckCrewClear();"); n = g.ev(SETUP)
        for k in range(25): g.ev(TICK); g.step(2)
        res += [dict(r, deck=d) for r in json.loads(g.ev(MEAS))]
        g.ev("for (const [h] of __st) crowd.remove(h)")
    g.close()
json.dump(res, open(sys.argv[2], 'w'))
by = collections.defaultdict(list)
for r in res:
    if r['seatHit'] is None: continue
    by[r['type']].append(round(r['thighLow'] - r['seatHit'], 3))
for t, gaps in sorted(by.items()): print(f'{t:16} n={len(gaps):3} thigh-vs-seat min {min(gaps):+.3f} max {max(gaps):+.3f}')
print('no surface found:', sum(1 for r in res if r['seatHit'] is None), 'of', len(res))
