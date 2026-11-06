// CH1's seat probe (0.99.7 note 4). Paste into a game page's scope (cadet_test's window.__sc) on a loaded deck: for every
// sit place it rays down through the seated body's footprint (BODY: [forward, sideways] from the spot) and reports places
// with something solid inside the body or no seat top at the spot's height, and the smallest nudge that clears them.
// Faded groups (the promenade planters) aren't under deckRoot, so their benches report seat: null; check those by eye.
(() => { const rc = new THREE.Raycaster(), out = [], dn = new THREE.Vector3(0, -1, 0);
  const meshes = []; deckRoot.traverse(o => { if (o.isMesh && o.visible && o.material !== HIT_MAT && !o.userData.noMerge) meshes.push(o); });
  let near = meshes; const bs = new THREE.Sphere();
  const hit = (x, y, z, far) => { rc.set(new THREE.Vector3(x, y, z), dn); rc.far = far; const h = rc.intersectObjects(near, false)[0]; return h ? h.point.y : null; };
  const BODY = [[-.15, 0], [-.12, .1], [-.12, -.1], [0, .16], [0, -.16], [-.06, .15], [-.06, -.15], [.06, .13], [.06, -.13], [0, 0], [.08, 0]];
  const score = (sp, df, dl) => { const fx = Math.sin(sp.face), fz = Math.cos(sp.face), rx = fz, rz = -fx, y = sp.y; let n = 0, worst = 0;
    for (const [f, l] of BODY) { const x = sp.x + fx * (f + df) + rx * (l + dl), z = sp.z + fz * (f + df) + rz * (l + dl), h = hit(x, y + .7, z, .62);
      if (h !== null) { n++; worst = Math.max(worst, h - y); } }
    const c = hit(sp.x + fx * df + rx * dl, y + .3, sp.z + fz * df + rz * dl, .6);   // the seat under the hips
    return { n, worst: +worst.toFixed(2), seat: c === null ? null : +(c - y).toFixed(3) }; };
  for (const p of deckDef.places || []) { if (p.pose !== 'sit' || /toilet/.test(p.type) || p.y === undefined && !SEAT_Y[p.type]) continue; const sp = placeSpot(p.id); if (!sp || !sp.y) continue;
    near = meshes.filter(m => { if (!m.geometry.boundingSphere) m.geometry.computeBoundingSphere(); bs.copy(m.geometry.boundingSphere).applyMatrix4(m.matrixWorld); return Math.hypot(bs.center.x - sp.x, bs.center.z - sp.z) < bs.radius + .6; });
    const s0 = score(sp, 0, 0); if (!s0.n && s0.seat !== null && Math.abs(s0.seat) < .02) continue;
    let best = null;
    for (let df = -.04; df <= .17; df += .03) for (let dl = -.15; dl <= .16; dl += .03) { const s = score(sp, df, dl); if (s.n || s.seat === null || Math.abs(s.seat) > .1) continue;
      const cost = Math.hypot(df, dl); if (!best || cost < best.cost - 1e-9) best = { cost, df: +df.toFixed(2), dl: +dl.toFixed(2), seat: s.seat }; }
    out.push([p.id, p.type, sp.y, s0, best]); }
  return out; })()
