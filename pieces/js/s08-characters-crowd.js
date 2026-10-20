// =====================================================================
// 8. CHARACTER KIT
// makeCharacter(spec) builds any crew member from a short description.
// Parts are merged into one vertex-coloured mesh per joint (~17 meshes per
// person, all sharing one material), so a full crew stays cheap to draw.
// Spec fields: dept, rank, skin, hair, hairColor, height, build, acc[]
// =====================================================================
// uniform colours, design v3: command red; works and watch gold; survey and infirmary blue-green
// the rec kit's colours (0.81.0): the deck's teal, darker shorts, the coral stripe, white grip socks with coral soles
const REC_KIT = { teal: '#1fa39b', shorts: '#16676a', coral: '#f0795a', sock: '#eef0ea' };
const DEPT = { command: '#b8433a', works: '#d9a441', watch: '#d9a441', survey: '#2f8e98', infirmary: '#2f8e98' };
// departments that share a colour are told apart by the badge: a silver shape with a coloured inlay
const BADGE = {
  command:   { shape: 'diamond', inlay: '#e8c06a' },
  works:     { shape: 'diamond', inlay: '#b5542a' },
  watch:     { shape: 'shield',  inlay: '#2e4a73' },
  survey:    { shape: 'circle',  inlay: '#1d5f73' },
  infirmary: { shape: 'cross',   inlay: '#c8463c' },
};
const DEPT_NAME = { survey: 'Survey', infirmary: 'Infirmary', watch: 'Watch', works: 'Works', command: 'Command' };
const RANK_NAME = ['Junior Officer', 'Officer', 'Department Chief', 'Executive Officer', 'Captain'];
const SKIN = ['#f3cfae', '#e3b08a', '#c98f66', '#a46c4b', '#7d4f35', '#573626'];
const HAIR = { black: '#1d1917', dark: '#3a2820', brown: '#6b4a2f', auburn: '#8c3f22', blonde: '#cfa966', grey: '#9f9a93', white: '#dcd8d0', teal: '#2f7f86' };
const BUILD = { slim: .86, average: 1, broad: 1.18 };
const HAIR_STYLES = ['ponytail', 'short', 'bun', 'curls', 'buzz', 'long', 'bald'];
const ACCESSORIES = ['glasses', 'beard', 'moustache', 'earrings', 'headband', 'apron'];
const LT = .33, LS = .31, ANK = .052, HIP_Y = .70, HIP_W = .655, HIP_OFF = .02;   // leg proportions (local units)

const CHAR_MAT = new THREE.MeshStandardMaterial({ vertexColors: true, roughness: .62, metalness: .04 });
const GEO = { sph: new THREE.SphereGeometry(1, 20, 14), box: new THREE.BoxGeometry(1, 1, 1) };
const _geoCache = {};
const cylG = (rt, rb, h, seg = 14) => { const k = `c${rt.toFixed(4)},${rb.toFixed(4)},${h},${seg}`; return _geoCache[k] || (_geoCache[k] = new THREE.CylinderGeometry(rt, rb, h, seg)); };
const capG = (r, th) => { const k = `s${r},${th}`; return _geoCache[k] || (_geoCache[k] = new THREE.SphereGeometry(r, 20, 12, 0, Math.PI * 2, 0, th)); };
const torG = (r, tube) => { const k = `t${r},${tube}`; return _geoCache[k] || (_geoCache[k] = new THREE.TorusGeometry(r, tube, 6, 20)); };
const shade = (hex, k) => '#' + new THREE.Color(hex).multiplyScalar(k).getHexString();
const _q = new THREE.Quaternion(), _e = new THREE.Euler(), _v = new THREE.Vector3(), _s = new THREE.Vector3();

// queue a primitive on a joint; bake() merges everything later
function part(pv, geo, color, x, y, z, sx = 1, sy = 1, sz = 1, rx = 0, ry = 0, rz = 0) {
  (pv.userData.parts || (pv.userData.parts = [])).push({ geo, c: col(color), m: new THREE.Matrix4().compose(_v.set(x, y, z), _q.setFromEuler(_e.set(rx, ry, rz)), _s.set(sx, sy, sz)) });
}
function bake(root) {
  const joints = []; root.traverse(o => { if (o.userData.parts) joints.push(o); });
  for (const pv of joints) {
    const P = [], N = [], C = [];
    for (const p of pv.userData.parts) {
      const g = (p.geo.index ? p.geo.toNonIndexed() : p.geo.clone()).applyMatrix4(p.m);
      const pa = g.attributes.position.array, na = g.attributes.normal.array;
      for (let i = 0; i < pa.length; i += 3) { P.push(pa[i], pa[i + 1], pa[i + 2]); N.push(na[i], na[i + 1], na[i + 2]); C.push(p.c.r, p.c.g, p.c.b); }
      g.dispose();
    }
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.Float32BufferAttribute(P, 3));
    geo.setAttribute('normal', new THREE.Float32BufferAttribute(N, 3));
    geo.setAttribute('color', new THREE.Float32BufferAttribute(C, 3));
    geo.computeBoundingSphere();
    const mesh = new THREE.Mesh(geo, CHAR_MAT); mesh.castShadow = mesh.receiveShadow = true;
    pv.add(mesh); delete pv.userData.parts;
  }
}

function makeCharacter(spec, finish = bake) {          // finish: what to do with the queued parts (the crowd keeps them)
  const s = Object.assign({ dept: 'survey', rank: 0, skin: 2, hair: 'short', hairColor: 'dark', height: 1, build: 'average', acc: [] }, spec);
  const bw = BUILD[s.build] || 1, skin = SKIN[s.skin] || s.skin, hc = HAIR[s.hairColor] || s.hairColor;
  const civ = s.dept === 'civilian';                     // 0.27.14: guests in plain clothes, a top in their outfit colour, no badge or pips
  // 0.81.0 (rec deck, plans/recdeck-plan.html section 8): kit 'rec' is the rec kit, a teal T-shirt and shorts with a coral
  // stripe, bare arms and legs; socks: true adds the float room's grip socks. Only colours change (and the sleeves end at
  // the elbow), so it's the same one mesh per joint: no extra draw calls. No badge, pips or belt
  const rec = s.kit === 'rec', plain = civ || rec, RK = REC_KIT;
  let uni = civ ? s.outfit || '#7a6a5a' : DEPT[s.dept] || DEPT.survey, uniDk = shade(uni, .66); const has = a => s.acc.includes(a);
  let suit = civ ? shade(uni, .82) : '#27313a', pants = civ ? '#454a52' : '#3a4653', boot = '#16191d', sole = '#3a3f44', gold = '#e8c06a';
  const belt = rec ? RK.shorts : boot;
  if (rec) { uni = suit = RK.teal; uniDk = RK.coral; pants = RK.shorts; boot = skin; sole = shade(skin, .85); }
  if (s.socks) { boot = RK.sock; sole = RK.coral; }
  const shin = rec ? skin : pants, arm = rec ? skin : uni;
  const root = new THREE.Group(); root.scale.setScalar(s.height);
  const rig = { root, legs: [], arms: [], spec: s };
  const pv = (p, x, y, z) => { const g = new THREE.Group(); g.position.set(x, y, z); p.add(g); return g; };

  // legs
  rig.hips = pv(root, 0, HIP_Y, 0);
  part(rig.hips, GEO.sph, pants, 0, -.01, 0, .155 * bw, .095, .115 * bw);
  for (const side of [1, -1]) {
    const thigh = pv(rig.hips, side * .088 * bw, -HIP_OFF, 0);
    part(thigh, GEO.sph, pants, 0, 0, 0, .07 * bw, .07, .07 * bw);
    part(thigh, cylG(.07 * bw, .058 * bw, LT), pants, 0, -LT / 2, 0);
    if (rec) part(thigh, GEO.box, RK.coral, side * .062 * bw, -LT * .3, 0, .012, LT * .5, .03);   // the coral stripe down the shorts
    const knee = pv(thigh, 0, -LT, 0);
    part(knee, GEO.sph, shin, 0, 0, 0, .06 * bw, .06, .062 * bw);
    part(knee, cylG(.057 * bw, .047 * bw, LS), shin, 0, -LS / 2, 0);
    part(knee, cylG(.056 * bw, .06 * bw, .11), boot, 0, -LS + .06, 0);
    const ankle = pv(knee, 0, -LS, 0);
    part(ankle, GEO.sph, boot, 0, -.008, .04, .062 * bw, .042, .115);
    part(ankle, GEO.box, sole, 0, -.045, .035, .1 * bw, .014, .2);
    rig.legs.push({ thigh, knee, ankle, side, off: side > 0 ? 0 : .5 });
  }
  // torso
  rig.torso = pv(rig.hips, 0, .05, 0);
  part(rig.torso, cylG(.153 * bw, .15 * bw, .1, 20), suit, 0, .03, 0);
  part(rig.torso, cylG(.158 * bw, .158 * bw, .045, 20), belt, 0, 0, 0);
  part(rig.torso, GEO.box, rec ? RK.shorts : gold, 0, 0, .158 * bw, .06, .04, .02);
  part(rig.torso, GEO.box, belt, -.12 * bw, -.035, .08 * bw, .07, .08, .05, 0, -.5, 0);
  if (has('apron')) part(rig.torso, GEO.box, '#e8e0cf', 0, -.1, .165 * bw, .25 * bw, .22, .02);
  rig.chest = pv(rig.torso, 0, .07, 0);
  part(rig.chest, cylG(.17 * bw, .155 * bw, .25, 20), suit, 0, .125, 0);
  part(rig.chest, cylG(.183 * bw, .172 * bw, .12, 20), uni, 0, .22, 0);
  part(rig.chest, cylG(.175 * bw, .175 * bw, .015, 20), uniDk, 0, .16, 0);
  part(rig.chest, GEO.sph, uni, 0, .28, 0, .2 * bw, .07, .15 * bw);
  if (has('apron')) part(rig.chest, GEO.box, '#e8e0cf', 0, .06, .162 * bw, .2 * bw, .2, .02);
  else if (!plain) {                                   // department badge, left breast
    const bd = BADGE[s.dept] || BADGE.survey, bx = .085 * bw, bz = .168 * bw, silver = '#dfe4e6';
    if (bd.shape === 'diamond') {
      part(rig.chest, GEO.box, silver, bx, .2, bz, .045, .045, .015, 0, 0, Math.PI / 4);
      part(rig.chest, GEO.box, bd.inlay, bx, .2, bz + .006, .024, .024, .012, 0, 0, Math.PI / 4);
    } else if (bd.shape === 'shield') {
      part(rig.chest, GEO.box, silver, bx, .202, bz, .042, .05, .015);
      part(rig.chest, GEO.box, silver, bx, .174, bz, .026, .026, .015, 0, 0, Math.PI / 4);
      part(rig.chest, GEO.box, bd.inlay, bx, .2, bz + .006, .024, .03, .012);
    } else if (bd.shape === 'circle') {
      part(rig.chest, cylG(.027, .027, .015, 16), silver, bx, .2, bz, 1, 1, 1, Math.PI / 2, 0, 0);
      part(rig.chest, cylG(.015, .015, .012, 16), bd.inlay, bx, .2, bz + .006, 1, 1, 1, Math.PI / 2, 0, 0);
    } else {
      part(rig.chest, GEO.box, silver, bx, .2, bz, .052, .018, .015);
      part(rig.chest, GEO.box, silver, bx, .2, bz, .018, .052, .015);
      part(rig.chest, GEO.box, bd.inlay, bx, .2, bz + .006, .012, .012, .012);
    }
  }
  if (s.pin && !plain) part(rig.chest, cylG(.022, .022, .014, 14), gold, -.085 * bw, .21, .168 * bw, 1, 1, 1, Math.PI / 2, 0, 0);   // 24l (E2): the fault-finder pin, right breast opposite the badge (merged in the chest)
  part(rig.chest, cylG(.075, .085, .05, 16), uniDk, 0, .33, 0);
  for (let i = 0; i < (plain ? 0 : Math.min(4, s.rank + 1)); i++) { const a = .55 + i * .32; part(rig.chest, GEO.sph, gold, Math.sin(a) * .083, .33, Math.cos(a) * .083, .011, .011, .011); }
  part(rig.chest, cylG(.05, .055, .08, 12), skin, 0, .37, 0);
  // head and face
  const h = rig.head = pv(rig.chest, 0, .4, 0);
  part(h, GEO.sph, skin, 0, .13, 0, .155, .17, .155);
  for (const sd of [1, -1]) {
    part(h, GEO.sph, skin, sd * .152, .12, 0, .025, .04, .03);
    part(h, GEO.sph, '#1b1f23', sd * .055, .145, .14, .022, .03, .012);
    part(h, GEO.box, s.hair === 'bald' ? shade(skin, .6) : hc, sd * .056, .188, .138, .05, .012, .012, 0, 0, sd * -.12);
    if (has('earrings')) part(h, GEO.sph, gold, sd * .158, .085, .005, .014, .014, .014);
  }
  part(h, GEO.sph, skin, 0, .11, .155, .02, .025, .02);
  part(h, GEO.box, shade(skin, .7), 0, .072, has('beard') ? .17 : .146, .04, .008, .01);
  // hair
  const cap = (r, th, y, tilt, sy = 1.05) => part(h, capG(r, th), hc, 0, y, -.01, 1, sy, 1, tilt, 0, 0);
  switch (s.hair) {
    case 'ponytail':
      cap(.168, Math.PI * .52, .14, -.38);
      part(h, GEO.sph, hc, .045, .255, .105, .1, .04, .055, 0, 0, .3);
      rig.tail = pv(h, 0, .2, -.13);
      part(rig.tail, GEO.sph, hc, 0, -.01, -.03, .05, .05, .05);
      part(rig.tail, cylG(.03, .03, .025, 10), uni, 0, -.04, -.05, 1, 1, 1, .4, 0, 0);
      part(rig.tail, GEO.sph, hc, 0, -.14, -.07, .045, .11, .045, .3, 0, 0);
      break;
    case 'short':
      cap(.168, Math.PI * .56, .135, -.32);
      part(h, GEO.sph, hc, .03, .262, .1, .11, .045, .06, 0, 0, .35);
      for (const sd of [1, -1]) part(h, GEO.sph, hc, sd * .142, .17, -.01, .035, .07, .09);
      break;
    case 'bun':
      cap(.164, Math.PI * .5, .14, -.42);
      part(h, GEO.sph, hc, 0, .275, -.1, .07, .065, .07);
      part(h, torG(.05, .012), uniDk, 0, .25, -.085, 1, 1, 1, -.9, 0, 0);
      break;
    case 'curls':
      cap(.162, Math.PI * .5, .14, -.35);
      for (let i = 0; i < 16; i++) {
        const th = .15 + (i % 3) * .42, ph = i * 2.4;
        if (Math.cos(ph) > .55 && th > .5) continue;                       // keep the forehead clear
        part(h, GEO.sph, hc, Math.sin(th) * Math.sin(ph) * .16, .14 + Math.cos(th) * .175, Math.sin(th) * Math.cos(ph) * .16 - .015, .06, .06, .06);
      }
      break;
    case 'buzz':
      cap(.165, Math.PI * .5, .135, -.45, 1.07);
      break;
    case 'long':
      cap(.17, Math.PI * .54, .14, -.34);
      part(h, GEO.sph, hc, 0, .02, -.09, .15, .2, .08);
      for (const sd of [1, -1]) part(h, GEO.sph, hc, sd * .13, .06, -.01, .04, .15, .07);
      part(h, GEO.sph, hc, -.04, .26, .1, .1, .04, .06, 0, 0, -.3);
      break;
  }
  // accessories
  if (has('glasses')) {
    for (const sd of [1, -1]) {
      part(h, torG(.036, .007), '#2b2f33', sd * .056, .145, .16);
      part(h, GEO.box, '#2b2f33', sd * .128, .15, .075, .006, .008, .16, 0, sd * .25, 0);
    }
    part(h, GEO.box, '#2b2f33', 0, .15, .162, .03, .007, .007);
  }
  if (has('beard')) {
    part(h, GEO.sph, hc, 0, .06, .07, .13, .085, .1);
    for (const sd of [1, -1]) part(h, GEO.sph, hc, sd * .13, .1, .03, .03, .07, .05);
  }
  if (has('beard') || has('moustache')) part(h, GEO.sph, hc, 0, .088, .152, .05, .015, .022);
  if (has('headband')) part(h, torG(.163, .013), uni, 0, .2, -.01, 1, 1, 1, Math.PI / 2 - .35, 0, 0);
  // arms
  for (const side of [1, -1]) {
    const sh = pv(rig.chest, side * .205 * bw, .27, 0);
    part(sh, GEO.sph, uni, 0, 0, 0, .062 * bw, .062, .062 * bw);
    part(sh, cylG(.052 * bw, .046 * bw, .23), uni, 0, -.115, 0);
    if (rec) part(sh, cylG(.054 * bw, .054 * bw, .03, 12), uniDk, 0, -.2, 0);   // the sleeve's coral hem
    const el = pv(sh, 0, -.23, 0);
    part(el, GEO.sph, arm, 0, 0, 0, .046 * bw, .046, .046 * bw);
    part(el, cylG(.045 * bw, .04 * bw, .2), arm, 0, -.1, 0);
    part(el, cylG(.044 * bw, .044 * bw, .03, 12), rec ? skin : uniDk, 0, -.185, 0);
    const hand = pv(el, 0, -.2, 0);
    part(hand, GEO.sph, skin, 0, -.045, .005, .042 * bw, .052, .036);
    rig.arms.push({ sh, el, hand, side, x: 0, e: -.15 });
  }
  finish(root);
  return rig;
}

// two-bone IK in the leg's swing plane: ankle target (ty, tz) relative to the hip joint
function legIK(leg, ty, tz) {
  let d = Math.hypot(ty, tz); const max = LT + LS - .003;
  if (d > max) { ty *= max / d; tz *= max / d; d = max; }
  const base = Math.atan2(-tz, -ty);
  const a = Math.acos(THREE.MathUtils.clamp((LT * LT + d * d - LS * LS) / (2 * LT * d), -1, 1));
  const k = Math.PI - Math.acos(THREE.MathUtils.clamp((LT * LT + LS * LS - d * d) / (2 * LT * LS), -1, 1));
  leg.thigh.rotation.x = base - a; leg.knee.rotation.x = k;
  return base - a + k;
}
const ss = u => u * u * (3 - 2 * u);
const L = (a, b, k) => a + (b - a) * k;
// one gait cycle = two steps. During stance each foot moves back at exactly walking speed, so feet stay planted.
const STRIDE = .46, STANCE = .6, CYCLE = STRIDE / STANCE, LIFT = .12;
function animateRig(rig, g, dt, t, sk, rnd = R) {      // rnd: the crowd passes each person's own stream, so it never draws on R()
  const w = g.w, p = g.p % 1, TAU = Math.PI * 2;
  const cr = g.crouch || 0;                             // 0.27.7: crouching (animateActivity sets it), the hips lower and the body leans
  const hipY = L(HIP_Y + Math.sin(t * 1.7) * .004, HIP_W + .024 * Math.cos(2 * TAU * (p - .3)), w) - .2 * cr;
  const hipX = L(Math.sin(t * .45) * .012, .026 * Math.cos(TAU * (p - .3)), w);
  rig.hips.position.set(hipX, hipY, 0);
  rig.hips.rotation.z = L(Math.sin(t * .45) * .02, .05 * Math.cos(TAU * (p - .3)), w);
  let zL = 0;
  for (const leg of rig.legs) {
    const q = (p + leg.off) % 1;
    let z, lift = 0, pitch = 0;
    if (q < STANCE) {                                   // planted, rolling heel to toe
      z = STRIDE / 2 - q / STANCE * STRIDE;
      if (q < .08) pitch = L(-.22, 0, q / .08);
      if (q > .42) pitch = ss((q - .42) / .18) * .5;
    } else {                                            // swing: lift, carry forward, reach
      const u = (q - STANCE) / (1 - STANCE);
      z = -STRIDE / 2 + STRIDE * ss(u);
      lift = Math.sin(Math.PI * Math.min(1, u * 1.1)) * LIFT * (1 - .35 * u);
      pitch = u < .35 ? L(.5, 0, u / .35) : L(0, -.22, (u - .35) / .65);
    }
    const ang = legIK(leg, ANK + lift * w - (hipY - HIP_OFF), z * w);
    leg.ankle.rotation.x = -ang + pitch * w;
    leg.thigh.rotation.z = -hipX / hipY - rig.hips.rotation.z + leg.side * .02;
    if (leg.side > 0) zL = z;
  }
  const fl = zL / (STRIDE / 2) * w;
  rig.hips.rotation.y = -.16 * fl;
  rig.chest.rotation.y = .3 * fl;
  g.lean += ((.09 * sk * w + .34 * cr) - g.lean) * Math.min(1, dt * 4);
  rig.torso.rotation.x = g.lean;
  rig.chest.rotation.z = -rig.hips.rotation.z * .7;
  rig.chest.scale.y = 1 + Math.sin(t * 1.7) * .012 * (1 - w);
  for (const a of rig.arms) {
    const fwd = a.side > 0 ? -fl : fl;
    const tx = L(Math.sin(t * 1.1 + a.side) * .03, -.62 * fwd * (.6 + .4 * sk), w);
    const te = L(-.18, -.28 - .55 * Math.max(0, fwd), w);
    a.x += (tx - a.x) * Math.min(1, dt * 11); a.e += (te - a.e) * Math.min(1, dt * 9);
    a.sh.rotation.x = a.x; a.el.rotation.x = a.e;
    a.sh.rotation.z = a.side * L(.1 + Math.sin(t * 1.7) * .012, .08, w);
    a.hand.rotation.x = L(-.1, -.25, w);
    if (a.side < 0 && g.reach > 0) {                    // the right hand reaches forward to a panel; a small push at the top
      const k = g.reach, push = Math.max(0, Math.sin((k - .85) / .15 * Math.PI)) * .06;
      a.sh.rotation.x = L(a.sh.rotation.x, -1.32 - push, k); a.el.rotation.x = L(a.el.rotation.x, -.42 + push, k);
      a.sh.rotation.z = L(a.sh.rotation.z, a.side * -.12, k); a.hand.rotation.x = L(a.hand.rotation.x, .35, k);
    }
  }
  g.lookT -= dt;
  if (g.lookT <= 0) { g.look = rnd() < .4 ? 0 : (rnd() - .5) * 1.2; g.lookT = 2 + rnd() * 4; }
  const yaw = L(g.look, 0, w) - rig.chest.rotation.y - rig.hips.rotation.y;
  rig.head.rotation.y += (yaw - rig.head.rotation.y) * Math.min(1, dt * 5);
  rig.head.rotation.x = L(Math.sin(t * .8) * .03, -g.lean * .8 + .025 * Math.cos(2 * TAU * (p - .35)), w);
  if (rig.tail) {
    const force = w * Math.cos(2 * TAU * (p - .3)) * 4 * sk - g.turn * 2.5 + g.lean * 8;
    g.tailV += (force - g.tail * 35 - g.tailV * 5) * dt; g.tail += g.tailV * dt;
    rig.tail.rotation.x = .1 + g.tail * .25; rig.tail.rotation.z = THREE.MathUtils.clamp(g.turn, -2, 2) * -.08;
  }
}

// =====================================================================
// 8b. CROWD
// Everyone who isn't you or a close crew member is drawn here. Each person
// is the figure makeCharacter builds, at lower detail, and a group of up to
// CROWD_PER people shares one skinned mesh: their joints are its bones. So
// 40 crew cost about 8 draw calls (shadows included) instead of about 700.
//   const h = crowd.add(spec)      spec as makeCharacter takes: dept, rank, skin, hair, hairColor, height, build, acc
//   h.set(pos, face, pose, walkPhase)
//     pos   world {x, y, z}. For sit and lie, y is the seat or mattress top (0: a usual chair or bunk).
//     face  an angle like Walker.face (0 looks toward +z). For lie, the way from head to feet.
//     pose  'walk' | 'stand' | 'sit' | 'lie' | 'work'. Changes blend over about half a second.
//     walkPhase  optional, in gait cycles. Leave it out and the gait follows how far pos moves.
//   crowd.remove(h); crowd.clear(); crowd.near(x, z) finds who's there; crowd.update(dt, t) runs once a frame.
// A person further than CROWD_FAR tiles from the camera's target, or everyone when zoomed far out, is
// drawn with even fewer polygons. Nothing here calls R(): each person has their own random stream.
// =====================================================================
const CROWD_JOINTS = 17, CROWD_BONES = 21;               // per person: 17 joints (hips, legs 6, torso, chest, head, arms 6, ponytail), then 4 prop bones
const CROWD_DETAIL = [{ sph: [10, 7], cap: [10, 5], cyl: 8, tor: [4, 10] }, { sph: [7, 5], cap: [7, 4], cyl: 6, tor: [3, 8] },
  { sph: [5, 4], cap: [5, 3], cyl: 4, tor: [3, 5], min: .03 }];   // 2 (0.27.8): coarse, for big crowds; parts smaller than min (eyes, badges) left out
const CROWD_FAR = 9, CROWD_FAR_ZOOM = .75;
const CROWD_MANY = 70, CROWD_FAR2 = 16;                  // with more than CROWD_MANY people, those further than CROWD_FAR2 (or all, zoomed out) go coarse
const CROWD_GATHER = 40, CROWD_GATHER2 = 12;             // at an event's gathering: more than 40 on the deck, coarse from 12 tiles (0.27.19)
const CROWD_POSE_EVERY = 10, CROWD_POSE_MARGIN = 4;      // 0.27.27: off-screen people are posed every 10th frame; 'on screen' has a 4 m margin
const _poseFr = new THREE.Frustum(), _poseM = new THREE.Matrix4(), _poseS = new THREE.Sphere(), _poseV = new THREE.Vector3(), _poseKeep = new Set();
// 0.27.30: the packed bodies of the last CROWD_KEEP people to leave the deck, by their look (the spec as JSON), so someone
// coming back skips crowdPack (about 1.6 ms each); the same look always packs to the same body
const CROWD_KEPT = new Map(), CROWD_KEEP = 40;
const CROWD_SEAT = { sit: .475, lie: .5 };               // default seat and mattress heights
let CROWD_PER = 0, CROWD_MAT = null, CROWD_EMPTY = null; // made on first use, so a game without a crowd has none of it
const CROWD_REST = new THREE.Object3D();                 // stands in for empty bone slots
const _crowdGeos = new Map();
function crowdGeo(geo, lod) {                            // the same shape, fewer segments
  const k = geo.uuid + lod; let g = _crowdGeos.get(k); if (g) return g;
  const p = geo.parameters, d = CROWD_DETAIL[lod];
  if (geo.type === 'SphereGeometry') g = p.thetaLength < Math.PI ? new THREE.SphereGeometry(p.radius, d.cap[0], d.cap[1], p.phiStart, p.phiLength, p.thetaStart, p.thetaLength) : new THREE.SphereGeometry(p.radius, d.sph[0], d.sph[1]);
  else if (geo.type === 'CylinderGeometry') g = new THREE.CylinderGeometry(p.radiusTop, p.radiusBottom, p.height, Math.min(p.radialSegments, d.cyl));
  else if (geo.type === 'TorusGeometry') g = new THREE.TorusGeometry(p.radius, p.tube, d.tor[0], d.tor[1]);
  else g = geo;
  _crowdGeos.set(k, g); return g;
}
// one person's parts at one level of detail, in their joints' own space: positions, normals, colours, joint numbers, triangles
function crowdPack(joints, lod) {
  const list = []; let nv = 0, ni = 0;
  const min = CROWD_DETAIL[lod].min || 0;
  joints.forEach((j, b) => { for (const p of j.userData.parts) {
    const g = crowdGeo(p.geo, lod);
    if (min) { if (!g.boundingSphere) g.computeBoundingSphere(); if (g.boundingSphere.radius * p.m.getMaxScaleOnAxis() < min) continue; }
    list.push([g, p, b]); nv += g.attributes.position.count; ni += g.index.count;
  } });
  const P = new Float32Array(nv * 3), N = new Float32Array(nv * 3), C = new Float32Array(nv * 3), B = new Uint8Array(nv), I = new Uint32Array(ni);
  const nm = new THREE.Matrix3(), v = new THREE.Vector3(); let o = 0, oi = 0;
  for (const [g, p, b] of list) {
    const pa = g.attributes.position, na = g.attributes.normal, ix = g.index.array; nm.getNormalMatrix(p.m);
    for (let i = 0; i < pa.count; i++) {
      v.fromBufferAttribute(pa, i).applyMatrix4(p.m).toArray(P, (o + i) * 3);
      v.fromBufferAttribute(na, i).applyMatrix3(nm).normalize().toArray(N, (o + i) * 3);
      C[(o + i) * 3] = p.c.r; C[(o + i) * 3 + 1] = p.c.g; C[(o + i) * 3 + 2] = p.c.b; B[o + i] = b;
    }
    for (let i = 0; i < ix.length; i++) I[oi++] = ix[i] + o;
    o += pa.count;
  }
  return { P, N, C, B, I, nv, ni };
}
// ---- activities (Pillar 2, workstream A2): what people do at a place, drawn on any rig ----
// A pose is a base (walk, stand, sit, lie, work) or an activity, or both as 'base:activity' ('sit:call', 'lie:lift').
// An activity alone stands, except that call, read, drink, talk, play and lift sit when y is 0.3 or more (a seat).
// For a standing pose, a y under 0.3 is the floor it stands on (a stage, the treadmill's belt). Unknown poses stand.
// Activities move the arms, head and torso over what the legs are doing, blend in and out like the bases, and may hold
// a prop. Crowd people carry their props inside the crowd's meshes (three prop bones, on each hand and the chest),
// so props cost no draw calls; full rigs get a small mesh on the hand. poseOf(place) gives a place's pose (plan,
// "Activities on places"). animateActivity(o, pose, dt, t, sk, y) poses any rig: the crowd, a FullPerson, or a Walker.
// what a '+modifier' holds: its prop (on the body bone) and how the arms hold it
const HOLDS = { cart: { prop: 'cart', sx: -.62, ex: -.62, sz: -.06, lean: .09 }, cartfull: { prop: 'cartfull', sx: -.62, ex: -.62, sz: -.06, lean: .09 },
  carry: { prop: 'parts', sx: -.42, ex: -1.25, sz: .16, lean: -.04 },
  // 0.27.7: one: only that arm holds it (1 left, -1 right; the other keeps swinging); bone: the prop rides that hand; hx: the
  // wrist; look: the head bends to it. A tray in the mess, a toolbox for the Works crew on a job, a datapad for officers.
  tray: { prop: 'tray', sx: -.36, ex: -1.2, sz: .14, lean: -.02 },
  toolbox: { prop: 'toolbox', bone: 'R', one: -1, sx: .03, ex: -.1, sz: .2, hx: 0 },
  datapad: { prop: 'datapad', bone: 'L', one: 1, sx: -.5, ex: -1.35, sz: .1, hx: .25, look: .28 },
  extinguisher: { prop: 'extinguisher', bone: 'R', one: -1, sx: .03, ex: -.1, sz: .2, hx: 0 },   // the drill's (Pillar 5, 24c): carried by its handle like the toolbox
  // 0.27.13 (Pillar 3, C11): your own device, held in both hands at the chest and read, head down, standing or walking
  device: { prop: 'device', bone: 'L', sx: -.55, ex: -1.4, sz: .1, hx: .3, look: .38 },
  // 0.28.41 (the user's): bursting for the toilet. No prop: both hands clasped low in front, knees in, short quick
  // steps, a little lean and a jiggle on the spot (knees: how far the thighs turn in)
  go: { sx: -.24, ex: -.6, sz: -.34, hx: .6, lean: .14, look: .16, knees: .16 } };
const ACT_OF_TYPE = { gym: 'lift', callhome: 'call', shop: 'browse', music: 'play', garden: 'water', laundry: 'fold', 'work:galley': 'cook' };
const ACT_SEATED = new Set(['call', 'read', 'drink', 'talk', 'play', 'lift', 'row', 'cycle']);
const BASES = new Set(['walk', 'stand', 'sit', 'lie', 'work', 'crouch']);   // crouch (0.27.7): a crouch-walk, for crawlways; it walks like walk
function poseOf(pl) {
  const act = pl.anim || ACT_OF_TYPE[pl.type], base = pl.type === 'bed' ? 'lie' : pl.pose || 'stand';
  if (!act || !ACTS[act]) return base;
  if (base === 'stand' || base === 'work') return act;
  if (base === 'sit' && !pl.anim && pl.type === 'gym') return 'sit:row';             // the gym's one seat is the rower
  if (base === 'sit' && !pl.anim && pl.type !== 'callhome') return base;   // by type, only booths and the gym are busy sitting (the music room's beanbags listen)
  if (base === 'sit' && ACT_SEATED.has(act)) return 'sit:' + act;
  if (base === 'lie' && act === 'lift') return 'lie:lift';
  if (base === 'lie' && act === 'bench') return 'lie:bench';   // 0.47.5: the weight bench (its place says anim: 'bench')
  return base;
}
const _parsed = new Map(), _parsedHi = new Map();          // 0.27.30: seated-height poses in their own map (no key string to build)
function parsePose(pose = 'stand', y = 0) {
  const pm = y >= .3 ? _parsedHi : _parsed; let r = pm.get(pose); if (r) return r;
  const plus = pose.indexOf('+'), mod = plus < 0 ? '' : pose.slice(plus + 1), bare = plus < 0 ? pose : pose.slice(0, plus);
  const cart = HOLDS[mod] ? mod : null;                  // something held: '+cart' (a hover cart, empty), '+cartfull' (loaded), '+carry' (a box of parts), '+tray', '+toolbox', '+datapad'
  const i = bare.indexOf(':'); let base = i < 0 ? bare : bare.slice(0, i), act = i < 0 ? null : bare.slice(i + 1);
  if (i < 0 && ACTS[base]) { act = base; base = act === 'row' || act === 'cycle' || y >= .3 && ACT_SEATED.has(act) ? 'sit' : 'stand'; }
  if (!BASES.has(base)) base = 'stand';
  if (act && !ACTS[act]) act = null;
  pm.set(pose, r = { base, act, cart }); return r;
}
// an arm toward a target: shoulder forward (x, negative is forward), elbow bend, shoulder out (z, toward its own side)
const armTo = (a, s, sx, ex, sz = .1, hx = 0) => {
  a.sh.rotation.x = L(a.sh.rotation.x, sx, s); a.el.rotation.x = L(a.el.rotation.x, ex, s);
  a.sh.rotation.z = L(a.sh.rotation.z, a.side * sz, s); a.hand.rotation.x = L(a.hand.rotation.x, hx, s);
};
// 0.27.40: the height of the cushion under a seated person's knees (world), or 0 when there's none (a bench or chair
// edge, the floor). 0.27.46 (perf 3: the ray down against the deck's merged meshes took 1.5-9 ms each time someone sat,
// 0.60.6's phone regression): no ray. A seat with cushion under the knees says so in its place, cush: <height>, measured
// from 0.27.45's ray for a person of average height; the seat spot is matched by position (so stand-ins get it too)
// 0.27.43 (reviewer 1e: the JS heap stayed 40 MB up): the caches are keyed by a deck-load number, never the deck itself,
// and emptied when a deck unloads (deckUnloaded, from unloadDeck), so nothing here keeps an old deck's meshes alive
const SEAT_RC = { gen: 1, cushK: null };
function deckUnloaded() {
  SEAT_RC.gen++; SEAT_RC.cushK = null;
  if (typeof tableTrays !== 'undefined') { for (const h of tableTrays.eaters) h.eating = false; tableTrays.eaters.length = 0; tableTrays.ownOf = 0; tableTrays.own = null; tableTrays.n = -1; }
}
function seatCushion(o, sy) {
  const p = o.pos, c = o.cush || (o.cush = { x: NaN, z: NaN, r: NaN, gen: 0, v: 0 });
  if (c.x === p.x && c.z === p.z && c.r === o.face && c.gen === SEAT_RC.gen) return c.v;
  c.x = p.x; c.z = p.z; c.r = o.face; c.gen = SEAT_RC.gen; c.v = 0;
  const S = SEAT_RC;
  if (!S.cushK) { S.cushK = []; for (const q of deckDef.places || []) if (q.cush) { const sp = placeSpot(q.id); S.cushK.push(sp.x, sp.z, q.cush); } }   // numbers only (0.27.43)
  for (let i = 0; i < S.cushK.length; i += 3) if (Math.abs(S.cushK[i] - p.x) < .05 && Math.abs(S.cushK[i + 1] - p.z) < .05) { c.v = S.cushK[i + 2]; break; }
  return c.v;
}
// 0.27.36: where empty hands rest when seated (on the lap), and the weight shift of anyone standing at work
const SIT_LAP = { sx: -.2, ex: -1.05, sz: -.08, hx: .15 };
function workSway(rig, s, tt, shift) {
  rig.hips.position.x = L(rig.hips.position.x, .018 * shift, s); rig.hips.rotation.z = L(rig.hips.rotation.z, .035 * shift, s);
  rig.chest.rotation.z = L(rig.chest.rotation.z, -.03 * shift, s); rig.chest.rotation.y = L(rig.chest.rotation.y, .12 * Math.sin(tt * .37), s);
  rig.head.rotation.y = L(rig.head.rotation.y, .18 * Math.sin(tt * .9), s);
}
const WORK_SWAY = new Set(['cook', 'wash', 'fold', 'water', 'pay']);   // standing jobs that get the same weight shift
const pulse = (t, period, len, ph = 0) => { const u = ((t + ph) % period) / len; return u < 1 ? Math.sin(Math.PI * u) : 0; };   // a bump of len seconds every period
// each activity: the props it holds (R right hand, L left hand, C chest) and how it moves. s is its blend weight,
// a.side is 1 for the left arm and -1 for the right. b is the base ('stand', 'sit' or 'lie'); ph is the person's phase.
const ACTS = {
  row: { f(r, s, t, b, ph, h, seat) {                    // the rower: legs drive, the body swings back, the arms pull in last
    const u = (t * .42 + ph) % 1, c = u < .4 ? ss(u / .4) : 1 - ss((u - .4) / .6), pull = THREE.MathUtils.clamp((c - .35) / .65, 0, 1);
    const hz = L(.12, -.2, c), hy = r.hips.position.y, foot = .3 / h;   // the seat slides; the feet stay on the footrests
    r.hips.position.z = L(r.hips.position.z, hz, s);
    for (const leg of r.legs) {
      const t0 = leg.thigh.rotation.x, k0 = leg.knee.rotation.x, a0 = leg.ankle.rotation.x;
      const ang = legIK(leg, ANK + foot - (hy - HIP_OFF), .52 - hz);
      leg.thigh.rotation.x = L(t0, leg.thigh.rotation.x, s); leg.knee.rotation.x = L(k0, leg.knee.rotation.x, s); leg.ankle.rotation.x = L(a0, -ang - .3, s);
    }
    r.torso.rotation.x = L(r.torso.rotation.x, L(.35, -.25, c), s);
    for (const a of r.arms) armTo(a, s, L(-1.3, .25, pull), L(-.1, -1.7, pull), .12, .1);
    r.head.rotation.x = L(r.head.rotation.x, L(-.2, .15, c), s);
  } },
  cycle: { f(r, s, t, b, ph, h) {                        // 0.38.28: the exercise bike: feet round the pedals, hands on the bars, a lean forward
    const hy = r.hips.position.y;
    for (const leg of r.legs) {
      const th = (t * 5 + ph * 6.283) + (leg === r.legs[0] ? 0 : Math.PI);
      const t0 = leg.thigh.rotation.x, k0 = leg.knee.rotation.x, a0 = leg.ankle.rotation.x;
      const ang = legIK(leg, ANK + (.32 - .13 * Math.sin(th)) / h - (hy - HIP_OFF), (.35 + .13 * Math.cos(th)) / h);   // 0.47.5 (playtest): pedalling forward, down the front
      leg.thigh.rotation.x = L(t0, leg.thigh.rotation.x, s); leg.knee.rotation.x = L(k0, leg.knee.rotation.x, s); leg.ankle.rotation.x = L(a0, -ang, s);
    }
    r.torso.rotation.x = L(r.torso.rotation.x, .32, s);
    for (const a of r.arms) armTo(a, s, -1.15, -.35, .1, .1);
    r.head.rotation.x = L(r.head.rotation.x, -.2, s);
  } },
  run: { f(r, s, t) {                                    // the legs run in place (the gait, in animateActivity); arms bent and pumping
    for (const a of r.arms) { a.el.rotation.x = L(a.el.rotation.x, -1.5, s); a.sh.rotation.z = L(a.sh.rotation.z, a.side * .12, s); }
    r.torso.rotation.x = L(r.torso.rotation.x, .1, s);
  } },
  bench: { props: { R: 'barbell' }, f(r, s, t, b, ph) {           // 0.47.5 (playtest): the bench press: the rack's bar in both hands, down to the chest and up, together
    const c = .5 - .5 * Math.cos(t * 1.5 + ph); if (s > .5) BENCH_BAR.t = performance.now();   // the rack's own bar hides while it's in someone's hands
    for (const a of r.arms) armTo(a, s, L(-.75, -1.5, c), L(-1.45, -.05, c), .42, .2);
    r.head.rotation.x = L(r.head.rotation.x, -.05, s);
  } },
  lift: { props: { R: 'dumbbell', L: 'dumbbell' }, f(r, s, t, b, ph) {
    for (const a of r.arms) {
      const c = .5 - .5 * Math.cos(t * 2.4 + ph + (a.side > 0 ? Math.PI : 0));
      if (b === 'lie') armTo(a, s, L(-.7, -1.5, c), L(-1.5, -.05, c), .25, .2);   // a press, straight up from the bench
      else armTo(a, s, -.12, L(-.25, -2.3, c), .14, .2);                            // curls, one arm then the other
    }
  } },
  call: { props: { R: 'receiver' }, f(r, s, t, b, ph) {
    const [L_, R_] = [r.arms.find(a => a.side > 0), r.arms.find(a => a.side < 0)], g = pulse(t, 7, 2.2, ph);
    armTo(R_, s, -.75, -2.45, .55, .3);                   // the receiver to the ear
    armTo(L_, s, L(b === 'sit' ? SIT_LAP.sx : -.1, -.7, g) + Math.sin(t * 3) * .1 * g, L(b === 'sit' ? SIT_LAP.ex : -.2, -1.3, g), b === 'sit' ? L(SIT_LAP.sz, .12, g) : .12, b === 'sit' ? L(SIT_LAP.hx, 0, g) : 0);   // and a gesture now and then
    r.head.rotation.z = L(r.head.rotation.z, -.12, s); r.head.rotation.x = L(r.head.rotation.x, .08, s);
  } },
  browse: { props: { L: 'basket' }, f(r, s, t, b, ph) {
    const [L_, R_] = [r.arms.find(a => a.side > 0), r.arms.find(a => a.side < 0)], reach = pulse(t, 6, 2.4, ph);
    armTo(L_, s, -.05, -.2, .22);                         // the basket on a hanging arm
    armTo(R_, s, L(-.15, -1.35, reach), L(-.25, -.35, reach), .1, L(0, .4, reach));   // reaching to a shelf
    r.head.rotation.y = L(r.head.rotation.y, Math.sin(t * .5 + ph) * .55, s);         // looking along the shelves
    r.head.rotation.x = L(r.head.rotation.x, .05 - .2 * reach, s);
  } },
  pay: { props: { R: 'card', L: 'basket' }, f(r, s, t, b, ph) {
    const [L_, R_] = [r.arms.find(a => a.side > 0), r.arms.find(a => a.side < 0)], tap = pulse(t, 3, .6, ph);
    armTo(L_, s, -.05, -.2, .22);
    armTo(R_, s, -.85 - .15 * tap, -.75 + .25 * tap, .02, .3);
    r.head.rotation.x = L(r.head.rotation.x, .3, s);
  } },
  play: { props: { C: 'guitar' }, seatedProps: {}, f(r, s, t, b, ph) {
    const [L_, R_] = [r.arms.find(a => a.side > 0), r.arms.find(a => a.side < 0)];
    if (b === 'sit') {                                    // keys: both hands forward, moving along the keyboard
      for (const a of r.arms) armTo(a, s, -.75, -.85, .06 + .1 * Math.sin(t * 1.1 + a.side + ph), .35 + .12 * Math.sin(t * 9 + a.side * 2));
      r.head.rotation.x = L(r.head.rotation.x, .25 + .05 * Math.sin(t * 2), s); r.torso.rotation.x = L(r.torso.rotation.x, .06 + .04 * Math.sin(t * 1.3), s);
    } else {                                              // a guitar: left hand up the neck, right hand strumming
      armTo(L_, s, -.85, -1.05, .45, .2);
      armTo(R_, s, -.35, -1.55 + .22 * Math.sin(t * 8 + ph), -.05, .1);
      r.head.rotation.x = L(r.head.rotation.x, .2, s); r.head.rotation.y = L(r.head.rotation.y, .35, s);
    }
  } },
  water: { props: { R: 'can' }, f(r, s, t, b, ph) {
    const [L_, R_] = [r.arms.find(a => a.side > 0), r.arms.find(a => a.side < 0)];
    armTo(R_, s, -.75, -.35, .1 + .2 * Math.sin(t * .7 + ph), -.45);   // the can held out and tipped, swept slowly along the bed
    armTo(L_, s, -.1, -.3, .12);
    r.head.rotation.x = L(r.head.rotation.x, .4, s); r.torso.rotation.x = L(r.torso.rotation.x, .12, s);
  } },
  cook: { props: { R: 'spoon', L: 'pan' }, f(r, s, t, b, ph) {
    const [L_, R_] = [r.arms.find(a => a.side > 0), r.arms.find(a => a.side < 0)], chop = ((t + ph) % 12) > 8;
    if (chop) armTo(R_, s, -.75, -.95 + .4 * Math.abs(Math.sin(t * 9)), .05, .2);   // chopping
    else armTo(R_, s, -.7 + .12 * Math.cos(t * 3.2), -1.0, .08 + .14 * Math.sin(t * 3.2), .2);   // stirring
    armTo(L_, s, -.6, -.95, .16, .1);                     // a hand on the pan
    r.head.rotation.x = L(r.head.rotation.x, .35, s); r.torso.rotation.x = L(r.torso.rotation.x, .08, s);
  } },
  wash: { props: { R: 'sponge', L: 'plate' }, f(r, s, t, b, ph) {
    for (const a of r.arms) armTo(a, s, -.6 + .07 * Math.cos(t * 5 + a.side), -.95, .04 + .07 * Math.sin(t * 5 + a.side), .25);
    r.head.rotation.x = L(r.head.rotation.x, .4, s); r.torso.rotation.x = L(r.torso.rotation.x, .14, s);
  } },
  fold: { props: { R: 'cloth' }, f(r, s, t, b, ph) {
    const u = pulse(t, 4, 2, ph);                         // lift, bring together, lay down
    for (const a of r.arms) armTo(a, s, L(-.7, -1.0, u), L(-.8, -1.4, u), L(.12, -.12, u), .3);
    r.head.rotation.x = L(r.head.rotation.x, .32, s); r.torso.rotation.x = L(r.torso.rotation.x, .1, s);
  } },
  drink: { props: { R: 'glass' }, f(r, s, t, b, ph) {
    const [L_, R_] = [r.arms.find(a => a.side > 0), r.arms.find(a => a.side < 0)], sip = pulse(t, 8, 1.8, ph);
    armTo(R_, s, L(-.5, -.8, sip), L(-1.3, -2.15, sip), .14, .25);
    if (b === 'sit') armTo(L_, s, SIT_LAP.sx, SIT_LAP.ex, SIT_LAP.sz, SIT_LAP.hx); else armTo(L_, s, -.15, -.3, .14);   // 0.27.36: the free hand on the lap
    r.head.rotation.x = L(r.head.rotation.x, -.1 * sip, s);
  } },
  read: { props: { R: 'book' }, f(r, s, t, b, ph) {
    const turn = pulse(t, 14, .8, ph);
    for (const a of r.arms) armTo(a, s, -.55, -1.7 + (a.side > 0 ? .3 * turn : 0), -.14, .35);
    r.head.rotation.x = L(r.head.rotation.x, .45, s);
  } },
  punch: { f(r, s, t, b, ph) {                          // 0.27.15: at the punch bag, guard up, jabs one hand then the other, a little bounce
    const u = (t * 1.6 + ph) % 2, side = u < 1 ? -1 : 1, jab = pulse(u % 1, 1, .35);
    for (const a of r.arms) { const j = a.side === side ? jab : 0; armTo(a, s, L(-1.05, -1.5, j), L(-2.1, -.15, j), .18, .2); }
    r.chest.rotation.y = L(r.chest.rotation.y, side * -.25 * jab, s); r.torso.rotation.x = L(r.torso.rotation.x, .12, s);
    r.hips.position.y += Math.abs(Math.sin(t * 6 + ph)) * .012 * s; r.head.rotation.x = L(r.head.rotation.x, .1, s);
  } },
  stretch: { f(r, s, t, b, ph) {                         // 0.27.15: on the mat, a slow reach overhead with a lean to each side, then a fold to the toes
    const u = ((t + ph) % 12) / 12, fold = u > .62 ? Math.sin(Math.PI * (u - .62) / .38) : 0, lean = u < .62 ? Math.sin(u / .62 * Math.PI * 2) : 0;
    for (const a of r.arms) armTo(a, s, L(L(-2.9, -2.6, Math.abs(lean)), -.25, fold), L(-.15, -.05, fold), L(.08, 0, fold), 0);
    r.torso.rotation.z = L(r.torso.rotation.z, .28 * lean, s); r.torso.rotation.x = L(r.torso.rotation.x, 1.15 * fold, s);
    r.head.rotation.x = L(r.head.rotation.x, -.15 + .3 * fold, s);
  } },
  talk: { f(r, s, t, b, ph) {
    if (b === 'sit') {                                    // 0.47.5 (playtest, "seated arm-waving"): seated, the hands stay on the lap; now and then one opens a little
      for (const a of r.arms) { const g = pulse(t, 9 + 2 * a.side, 1.8, ph + a.side * 4.1); armTo(a, s, L(SIT_LAP.sx, -.42, g), L(SIT_LAP.ex, -1.2, g), L(SIT_LAP.sz, .1, g), L(SIT_LAP.hx, -.15, g)); }
      r.head.rotation.x = L(r.head.rotation.x, .05 * Math.sin(t * 2.3 + ph), s); r.head.rotation.y = L(r.head.rotation.y, .2 * Math.sin(t * .4 + ph), s);
      return;
    }
    for (const a of r.arms) {
      const g = pulse(t, 5 + a.side, 1.6, ph + a.side * 1.7);
      armTo(a, s, L(b === 'sit' ? SIT_LAP.sx : -.08, -.75, g) + .1 * g * Math.sin(t * 4), L(b === 'sit' ? SIT_LAP.ex : -.25, -1.3, g), L(b === 'sit' ? SIT_LAP.sz : .12, .3, g), L(b === 'sit' ? SIT_LAP.hx : 0, -.3, g));
    }
    r.head.rotation.x = L(r.head.rotation.x, .05 * Math.sin(t * 2.3 + ph), s);
    r.head.rotation.y = L(r.head.rotation.y, .2 * Math.sin(t * .4 + ph), s);
  } },
};
const CROWD_ANIMS = new Set(Object.keys(ACTS));        // the activities drawn: anything else stands (for the schedules to check)
// props, in their bone's own space (a hand: the wrist at 0, fingers toward -y; the chest: its base at 0, front +z).
// Built the first time they're needed, from the character kit's primitives; colours through col(); no R().
const PROP_BONE = { R: 0, L: 1, C: 2, B: 3 };            // B: the body, at the feet facing forward (a cart)
const PROP_KIT = {
  barbell(p) { const a = BENCH_BAR.rz, c = Math.cos(a), n = Math.sin(a); for (const [x, geo, colr] of [[0, cylG(.014, .014, 1.5, 8), '#a4aeb4'], [-.62, cylG(.15, .15, .045, 14), '#2b2f33'], [.62, cylG(.15, .15, .045, 14), '#2b2f33']]) part(p, geo, colr, (BENCH_BAR.dx + x) * c, -.055 + (BENCH_BAR.dx + x) * n, .01, 1, 1, 1, 0, 0, Math.PI / 2 + a); },   // 0.47.5: the bench's bar, centred between the hands
  dumbbell(p) { part(p, cylG(.012, .012, .17, 8), '#a4aeb4', 0, -.055, .01, 1, 1, 1, 0, 0, Math.PI / 2); for (const x of [-.07, .07]) part(p, cylG(.04, .04, .035, 10), '#2b2f33', x, -.055, .01, 1, 1, 1, 0, 0, Math.PI / 2); },
  receiver(p) { part(p, GEO.box, '#2b2f33', 0, -.07, .045, .04, .17, .045, .3); part(p, GEO.sph, '#2b2f33', 0, -.15, .07, .03, .025, .03); },
  basket(p) { part(p, GEO.box, '#2a9d8f', 0, -.2, .02, .24, .12, .16); part(p, GEO.box, '#1f6f66', 0, -.11, .02, .015, .1, .015); },
  card(p) { part(p, GEO.box, '#e8c06a', 0, -.1, .035, .055, .08, .006); },
  guitar(p) {
    part(p, GEO.sph, '#d9a35b', -.05, .02, .23, .17, .19, .055); part(p, GEO.sph, '#d9a35b', .07, .12, .22, .12, .12, .05);
    part(p, cylG(.04, .04, .012, 12), '#3a2820', -.03, .05, .278, 1, 1, 1, Math.PI / 2);
    part(p, GEO.box, '#5a3424', .27, .22, .23, .42, .045, .025, 0, 0, .38);
  },
  can(p) { part(p, cylG(.07, .08, .15, 10), '#3f7a5a', 0, -.14, .06); part(p, GEO.box, '#3f7a5a', 0, -.11, .19, .025, .025, .2, .6); part(p, GEO.box, '#2f5e46', 0, -.05, .06, .015, .06, .1); },
  spoon(p) { part(p, GEO.box, '#a4aeb4', 0, -.06, -.08, .016, .016, .2); part(p, GEO.sph, '#a4aeb4', 0, -.06, -.18, .03, .03, .02); },
  fork(p) { part(p, GEO.box, '#a4aeb4', 0, -.06, -.07, .014, .012, .17); part(p, GEO.box, '#a4aeb4', 0, -.06, -.175, .034, .008, .05); },   // 0.27.38: eating at the mess
  pan(p) { part(p, GEO.box, '#2b2f33', 0, -.12, 0, .025, .17, .025); part(p, cylG(.12, .1, .05, 14), '#3a3f44', 0, -.31, -.02, 1, 1, 1, Math.PI / 2); },
  sponge(p) { part(p, GEO.box, '#e9c46a', 0, -.08, .03, .07, .035, .05); },
  plate(p) { part(p, cylG(.11, .11, .014, 14), '#e8ebe8', 0, -.09, .07, 1, 1, 1, Math.PI / 2); },
  cloth(p) { part(p, GEO.box, '#e9e1d0', .08, -.12, .02, .26, .18, .006); },
  glass(p) { part(p, cylG(.033, .028, .1, 10), '#f0a640', 0, -.07, .06, 1, 1, 1, -Math.PI / 2); },
  cart(p) {                                              // a hover cart pushed ahead: the handle at the hands, the bed in front, glowing underneath
    part(p, GEO.box, '#d9a441', 0, .5, .78, .56, .16, .82); part(p, GEO.box, '#9ff3e6', 0, .405, .78, .5, .03, .74);
    for (const x of [-.24, .24]) part(p, GEO.box, '#a4aeb4', x, .72, .4, .035, .42, .035);
    part(p, GEO.box, '#a4aeb4', 0, .92, .4, .52, .035, .035);
  },
  parts(p) {                                             // a small crate of parts carried in both hands at the chest
    part(p, GEO.box, '#7a6a52', 0, .98, .36, .34, .22, .24); part(p, GEO.box, '#e9c46a', 0, .98, .484, .14, .07, .008); part(p, GEO.box, '#a4aeb4', .06, 1.1, .34, .06, .04, .14);
  },
  cartfull(p) { PROP_KIT.cart(p); part(p, GEO.box, '#7a6a52', -.1, .7, .7, .3, .24, .3); part(p, GEO.box, '#e3eff4', .12, .67, .92, .26, .18, .26); part(p, GEO.box, '#e9c46a', .02, .67, .7, .1, .06, .01); },
  tray(p) {                                              // a mess tray carried at the waist: a plate of dinner and a mug
    part(p, GEO.box, '#c9ccc4', 0, .97, .38, .46, .025, .32); part(p, cylG(.09, .09, .012, 14), '#e8ebe8', -.08, .99, .38);
    part(p, GEO.sph, '#c88a3a', -.08, 1.0, .38, .06, .018, .05); part(p, cylG(.03, .028, .07, 10), '#d06a3a', .13, 1.017, .35);
  },
  toolbox(p) {                                           // a red toolbox hanging from the hand by its handle
    part(p, GEO.box, '#c0392b', 0, -.23, .01, .1, .15, .34); part(p, GEO.box, '#8e2a20', 0, -.165, .01, .104, .03, .344);
    part(p, GEO.box, '#2b2f33', 0, -.105, .01, .03, .025, .17); for (const z of [-.06, .08]) part(p, GEO.box, '#2b2f33', 0, -.13, z, .02, .05, .02);
  },
  device(p) {                                            // the player's handheld: a dark bezel, its screen glowing in the device's phosphor colour
    part(p, GEO.box, '#1b1f24', -.03, -.1, .035, .17, .21, .02); part(p, GEO.box, devicePhosphor(), -.03, -.1, .046, .14, .15, .006);
    part(p, GEO.box, '#e8a04c', .035, -.19, .046, .012, .012, .006);   // the power light
  },
  extinguisher(p) {                                      // a red extinguisher hanging from the hand: the cylinder, its grey valve, a black hose (24c's drill)
    part(p, cylG(.055, .055, .3, 10), '#c0392b', 0, -.26, .01); part(p, cylG(.03, .04, .05, 8), '#8f979c', 0, -.09, .01);
    part(p, GEO.box, '#1d2226', .045, -.2, .04, .018, .2, .018);
  },
  datapad(p) {                                           // a datapad on the palm, its screen lit
    part(p, GEO.box, '#2b2f33', 0, -.1, .03, .14, .2, .015); part(p, GEO.box, '#7fd4e6', 0, -.1, .039, .12, .17, .006);
  },
  book(p) { part(p, GEO.box, '#8c3f22', .09, -.08, .05, .17, .22, .035, .2); part(p, GEO.box, '#efe9dc', .09, -.08, .07, .15, .2, .008, .2); },
};
// the device's screen colour: one shared value, the device skin's ink (section 19's DEVICE_SKIN.ink, else the CSS
// --crt-ink on the page), else the Wren's cyan. Read when the prop is first built.
function devicePhosphor() {
  const v = typeof DEVICE_SKIN !== 'undefined' && DEVICE_SKIN && DEVICE_SKIN.ink || getComputedStyle(document.documentElement).getPropertyValue('--crt-ink').trim();
  return /^#[0-9a-f]{6}$/i.test(v) ? v : '#6ff0dc';
}
const PROP_UNLIT = { device: true };                     // full rigs draw these props unlit, so the screen glows (still one mesh)
let PROP_BASIC = null;
const _propParts = {}, _propPacks = {}, _propGeos = {};
function propParts(kind) {
  if (_propParts[kind]) return _propParts[kind];
  const g = new THREE.Group(); PROP_KIT[kind](g); return (_propParts[kind] = g.userData.parts);
}
function propPack(kind, lod, bone) {                    // for the crowd: packed like a body part, on prop bone `bone`
  const k = kind + lod + bone; if (_propPacks[k]) return _propPacks[k];
  const j = new THREE.Group(); j.userData.parts = propParts(kind);
  const q = crowdPack([j], lod); q.B.fill(CROWD_JOINTS + bone); return (_propPacks[k] = q);
}
function propGeo(kind) {                                 // for full rigs: a plain vertex-coloured geometry
  if (_propGeos[kind]) return _propGeos[kind];
  const j = new THREE.Group(); j.userData.parts = propParts(kind); const q = crowdPack([j], 0), geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(q.P, 3)); geo.setAttribute('normal', new THREE.BufferAttribute(q.N, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(q.C, 3)); geo.setIndex(new THREE.BufferAttribute(q.I, 1)); geo.computeBoundingSphere();
  return (_propGeos[kind] = geo);
}
// the props someone holds now: a key like 'R:dumbbell L:dumbbell', or ''
const _propKeys = {}, _holdKeys = {}, _cartKeys = {};     // 0.27.30: made once, not every frame
function propKeyOf(act, base) {
  const m = _propKeys[base] || (_propKeys[base] = {}); if (m[act] !== undefined) return m[act];
  const A = act && ACTS[act], P = A && (base === 'sit' && A.seatedProps || A.props);
  return (m[act] = P ? Object.entries(P).map(([b, k]) => b + ':' + k).join(' ') : '');
}
const _propList = new Map();
const propList = key => _propList.get(key) || (_propList.set(key, key ? key.split(' ').map(s => { const [b, k] = s.split(':'); return [PROP_BONE[b], k]; }) : []), _propList.get(key));
// full rigs and Walkers: small meshes on the hand or chest (each its own copy, so the rig can dispose it)
function rigProps(o, key) {
  for (const m of o.propMeshes || []) { m.parent.remove(m); m.geometry.dispose(); }
  o.propMeshes = [];
  const R_ = o.rig.arms.find(a => a.side < 0).hand, L_ = o.rig.arms.find(a => a.side > 0).hand;
  if (!o.bodyProps) { o.bodyProps = new THREE.Group(); o.bodyProps.scale.setScalar(1 / o.rig.spec.height); o.rig.root.add(o.bodyProps); }
  const at = [R_, L_, o.rig.chest, o.bodyProps];
  for (const [b, kind] of propList(key)) {
    const unlit = PROP_UNLIT[kind] && (PROP_BASIC || (PROP_BASIC = new THREE.MeshBasicMaterial({ vertexColors: true })));
    const m = new THREE.Mesh(propGeo(kind).clone(), unlit || CHAR_MAT); m.castShadow = true; m.receiveShadow = !unlit;
    if (o.obj) m.userData.walker = o;                   // a Walker's prop taps as the Walker
    at[b].add(m); o.propMeshes.push(m);
  }
}
// pose a rig for one frame: the gait (animateRig), the base pose, the activity and its props.
// o: a CrowdPerson, a FullPerson or a Walker (anything with rig, g and h). t already includes the person's own offset.
// sk: walking speed 0..1, as animateRig takes. y: the seat (sit, lie) or the floor (standing) height, as for set().
// With pose 'stand' or 'walk' it does exactly what animateRig alone does, so a Walker can call it in animateRig's place.
function animateActivity(o, pose, dt, t, sk, y = 0) {
  const rig = o.rig, g = o.g, h = o.h, { base, act, cart } = parsePose(pose, y);
  const rnd = o.rnd || o.prnd || (o.prnd = (() => { let sd = 7907; return () => (sd = (sd * 16807) % 2147483647) / 2147483647; })());
  const k = o.k || (o.k = {}), ph = o.ph !== undefined ? o.ph : (o.ph = (g.t0 || 0) * 3.7 % 10);
  if (act === 'run') {                                   // running in place: the gait at a run, with nowhere to go
    g.w = o.fresh ? 1 : g.w + (1 - g.w) * Math.min(1, dt * 6); g.p += dt * 1.9; sk = 1;
  }
  g.crouch = k.crouch ? ss(k.crouch) : 0;
  animateRig(rig, g, dt, t, sk, o.rnd || R);
  const cartKey = cart ? _cartKeys[cart] || (_cartKeys[cart] = '+' + cart) : null;
  if (act && ACTS[act].root) o.rootOn = true;           // 0.81.0: a rec move that places the whole body (recRoot)
  if (k[base] === undefined) k[base] = 0; if (act && k[act] === undefined) k[act] = 0; if (cartKey && k[cartKey] === undefined) k[cartKey] = 0;
  for (const key in k) { const on = +(key === base || key === act || key === cartKey); k[key] = o.fresh ? on : k[key] + (on - k[key]) * Math.min(1, dt * 5); }
  const seat = base === 'sit' || base === 'lie' ? (y > 0 ? y : CROWD_SEAT[base]) : 0;
  if (k.sit > .001) {                                    // on a bench or chair: feet on the floor, forearms on the table, eating now and then
    const s = ss(k.sit), sy = seat || CROWD_SEAT.sit, hy = Math.max(sy / h + .09, HIP_OFF + .45);
    rig.hips.position.y = L(rig.hips.position.y, hy, s); rig.hips.position.x *= 1 - s;
    rig.hips.rotation.y *= 1 - s; rig.hips.rotation.z *= 1 - s;
    // 0.27.40 (the user: "people sitting in booths and on couches clip right through the seat"): the legs are too short to
    // reach the floor with level thighs, so the feet-on-the-floor pose slopes the thighs down, through a deep cushion. Where
    // there's cushion under the knees (seatCushion: one ray, kept until the person moves) the thighs stay just above it
    // and the shins hang; on a bench or chair, whose front edge is under the knees, the feet stay on the floor as before
    const cu = o.pos && sy < .62 ? seatCushion(o, sy) : 0, kh = cu ? Math.min(hy - .01, (cu + .055 * h) / h) : 0, th = cu ? Math.asin(Math.min(.9, (hy - kh) / LT)) : 0;
    for (const leg of rig.legs) {
      const t0 = leg.thigh.rotation.x, k0 = leg.knee.rotation.x, a0 = leg.ankle.rotation.x;
      const ang = cu ? legIK(leg, -(LT * Math.sin(th) + LS * .97), LT * Math.cos(th) + .03)
        : legIK(leg, ANK + (sy > .62 ? (sy - .5) / h : 0) - (hy - HIP_OFF), .3);   // on a high stool the feet rest on its ring (0.27.11)
      leg.thigh.rotation.x = L(t0, leg.thigh.rotation.x, s); leg.knee.rotation.x = L(k0, leg.knee.rotation.x, s);
      leg.ankle.rotation.x = L(a0, -ang, s); leg.thigh.rotation.z = L(leg.thigh.rotation.z, leg.side * .05, s);
    }
    rig.torso.rotation.x = L(rig.torso.rotation.x, .02, s); rig.chest.rotation.y *= 1 - s; rig.chest.rotation.z *= 1 - s;
    // 0.27.36 (the user: "their hands are up like they are holding something"): with nothing in them the hands rest on the
    // lap, elbows soft. Now and then one hand shifts on the knee (the timer the old empty-handed 'eating' used).
    // 0.27.38: a diner with a tray in front of them (o.eating, set by tableTrays) eats: hands at the table, a fork in the
    // right hand, and on that timer a bite
    if (o.eatT === undefined) { o.eat = 0; o.eatT = 2 + rnd() * 6; }
    o.eatT -= dt; if (o.eatT < 0) { o.eat += dt / 1.6; if (o.eat >= 1) { o.eat = 0; o.eatT = 3 + rnd() * 7; } }
    const shift = Math.sin(Math.PI * o.eat) * s;
    for (const a of rig.arms) {
      if (o.eating) {
        armTo(a, s, -.5, -1.2, .14, .2);
        if (a.side < 0 && shift > 0) { a.sh.rotation.x = L(a.sh.rotation.x, -.75, shift); a.el.rotation.x = L(a.el.rotation.x, -2.1, shift); }
        continue;
      }
      armTo(a, s, SIT_LAP.sx, SIT_LAP.ex, SIT_LAP.sz, SIT_LAP.hx);
      if (a.side < 0 && shift > 0) { a.sh.rotation.x = L(a.sh.rotation.x, SIT_LAP.sx - .18, shift); a.el.rotation.x = L(a.el.rotation.x, SIT_LAP.ex - .25, shift); }
    }
    rig.head.rotation.x = L(rig.head.rotation.x, o.eating ? .2 - shift * .12 : .1 + shift * .06, s);
  }
  if (k.work > .001) {                                   // busy at a panel, a bench or a counter
    // 0.27.36 (the user: "less stiff"): each person has their own way of working (wv, from their phase) and their own pace,
    // so a row of them never moves in step. 0: at a panel, hands at chest height tapping and sliding, a glance up at the
    // screen; 1: at a bench, hands low, one steadying while the other works, a reach for a tool; 2: adjusting, a hand up
    // and out to a valve or a rack. All of them: the weight moves from foot to foot, the body leans in and eases back,
    // and the eyes go between the hands and the work
    const s = ss(k.work), v = o.wv !== undefined ? o.wv : (o.wv = Math.floor(ph * 3.3) % 3), tt = t * (.85 + ph % 1 * .3) + ph;
    const glance = pulse(tt, 5.5, 1.3), reach = pulse(tt + 2, v === 2 ? 6.5 : 9, 1.8), shift = Math.sin(tt * .55);
    workSway(rig, s, tt, shift);
    rig.torso.rotation.x = L(rig.torso.rotation.x, .08 + .05 * Math.sin(tt * .7) - .04 * glance, s);
    rig.head.rotation.x = L(rig.head.rotation.x, L(v === 0 ? .2 : .34, -.02, glance), s);
    for (const a of rig.arms) {
      const own = tt * (a.side > 0 ? 1.7 : 2.3) + a.side, main = a.side < 0;   // the right hand does most of it
      if (v === 0) armTo(a, s, -1.0 + .05 * Math.sin(own), -.9 + .15 * Math.sin(own * 1.6), -.02 + .06 * Math.sin(own * .5), .3);
      else armTo(a, s, -.7 + (main ? .06 : .02) * Math.sin(own), -1.0 + (main ? .14 : .04) * Math.sin(own * 1.3), main ? .02 : .08, .25);
      if (main && reach > 0) {
        if (v === 2) armTo(a, s * reach, -1.75, -.45, .32, .2);      // up and out
        else if (v === 1) armTo(a, s * reach, -1.05, -.35, .3, .1);  // to the side, for a tool
        else armTo(a, s * reach, -1.35, -.4, .04, .35);              // up the panel
      }
    }
    if (v === 2) rig.head.rotation.x = L(rig.head.rotation.x, -.15, s * reach);
  }
  if (k.lie > .001) {                                    // on the back, legs straight, arms by the sides
    const s = ss(k.lie);
    rig.hips.position.y = L(rig.hips.position.y, HIP_Y, s);
    for (const leg of rig.legs) for (const j of [leg.thigh, leg.knee, leg.ankle]) j.rotation.x *= 1 - s;
    for (const a of rig.arms) { a.sh.rotation.x = L(a.sh.rotation.x, .04, s); a.el.rotation.x = L(a.el.rotation.x, -.12, s); a.sh.rotation.z = L(a.sh.rotation.z, a.side * .1, s); }
    rig.torso.rotation.x *= 1 - s; rig.head.rotation.x = L(rig.head.rotation.x, -.12, s);
  }
  if (k.crouch > .001) {                                 // crouched: arms a little forward and out, the head up to see ahead
    const s = ss(k.crouch);
    for (const a of rig.arms) { a.sh.rotation.x -= .3 * s; a.el.rotation.x -= .45 * s; a.sh.rotation.z += a.side * .1 * s; }
    rig.head.rotation.x -= .32 * s;
  }
  for (const key in k) if (ACTS[key] && k[key] > .001 && !(key === 'talk' && o.eating && base === 'sit')) ACTS[key].f(rig, ss(k[key]), t, base, ph, h, seat || CROWD_SEAT.sit);   // eating: the talk waits
  if (act && base === 'stand' && WORK_SWAY.has(act) && k[act] > .001) { const tt = t * (.85 + ph % 1 * .3) + ph; workSway(rig, ss(k[act]) * .7, tt, Math.sin(tt * .55)); }   // 0.27.36
  for (const hk in HOLDS) if (k['+' + hk] > .001 && base !== 'sit' && base !== 'lie') {   // hands on the cart's handle, or round the box
    const H = HOLDS[hk], s = ss(k['+' + hk]), busy = act ? ss(k[act] || 0) : base === 'work' ? ss(k.work || 0) : 0, w = s * (1 - busy);   // loading or unloading ('work+cart') keeps its own arms
    for (const a of rig.arms) if (!H.one || a.side === H.one) armTo(a, w, H.sx, H.ex, H.sz, H.hx !== undefined ? H.hx : .35);
    if (H.lean !== undefined) rig.torso.rotation.x = L(rig.torso.rotation.x, H.lean, s);
    if (H.look) rig.head.rotation.x = L(rig.head.rotation.x, H.look, w);
    if (H.knees) for (const leg of rig.legs) {           // '+go': knees together, the stride shortened, a jiggle when still
      leg.thigh.rotation.x *= 1 - .45 * s; leg.knee.rotation.x *= 1 - .3 * s;
      leg.thigh.rotation.z = L(leg.thigh.rotation.z, -leg.side * H.knees, s);
      leg.knee.rotation.z = L(leg.knee.rotation.z, leg.side * H.knees * 1.6, s);
      leg.knee.rotation.x -= Math.max(0, Math.sin(t * 11 + leg.side * 1.6)) * .14 * s * (1 - sk);
    }
  }
  const pk = act && k[act] > .5 ? propKeyOf(act, base) : '', hk = cart && HOLDS[cart].prop && base !== 'sit' && base !== 'lie' ? _holdKeys[cart] || (_holdKeys[cart] = (HOLDS[cart].bone || 'B') + ':' + HOLDS[cart].prop) : '';
  const ek = !pk && o.eating && base === 'sit' && k.sit > .5 ? 'R:fork' : '';   // 0.27.38: a fork while eating
  const key = pk && hk ? pk + ' ' + hk : pk || hk || ek;     // activity props appear halfway in; a cart at once
  if (key !== (o.propKey || '')) {
    o.propKey = key;
    if (o.propBones) { if (o.chunk) o.chunk.dirty = true; }   // the crowd: rebuilt into its group's mesh
    else rigProps(o, key);
  }
  return { base, act, seat };
}
class CrowdPerson {
  constructor(spec, n) {
    let root = null;
    this.rig = makeCharacter(spec, r => { root = r; }); this.spec = this.rig.spec; this.h = this.spec.height;
    this.rig.root.rotation.order = 'YXZ';                // turn to face, after lying down
    this.joints = []; root.traverse(o => { if (o.userData.parts) this.joints.push(o); });
    this.look = JSON.stringify(this.rig.spec); const kept = CROWD_KEPT.get(this.look);   // 0.27.30: back on the deck: the body packed last time
    if (kept) { CROWD_KEPT.delete(this.look); this.geo = kept.geo; this.jparts = kept.jparts; }
    else {
      this.geo = [0, 1].map(l => crowdPack(this.joints, l));
      this.jparts = this.joints.map(j => j.userData.parts);  // kept for the coarse detail, packed only if a big crowd needs it
    }
    for (const j of this.joints) delete j.userData.parts;
    const hand = side => this.rig.arms.find(a => a.side === side).hand;   // prop bones: right hand, left hand, chest
    this.propBones = [hand(-1), hand(1), this.rig.chest, this.rig.root].map(j => { const b = new THREE.Object3D(); j.add(b); return b; }); this.propKey = '';
    this.propBones[3].scale.setScalar(1 / this.h);          // the cart keeps its size whatever the person's height
    let sd = 7919 * (n + 1) % 2147483647;
    this.rnd = () => (sd = (sd * 16807) % 2147483647) / 2147483647;
    this.g = { p: 0, w: 0, turn: 0, look: 0, lookT: this.rnd() * 3, tail: 0, tailV: 0, lean: 0, t0: this.rnd() * 20 };
    this.k = { sit: 0, lie: 0, work: 0 }; this.eat = 0; this.eatT = 2 + this.rnd() * 6;
    this.pos = new THREE.Vector3(); this.face = 0; this.rot = 0; this.pose = 'stand'; this.phase = undefined;
    this.moved = 0; this.fresh = true; this.lod = 0; this.chunk = null; this.slot = -1;
  }
  packOf(l) { return this.geo[l] || (this.geo[l] = crowdPack(this.jparts.map(parts => ({ userData: { parts } })), l)); }
  set(pos, face, pose = 'stand', walkPhase) {
    if (!this.fresh) this.moved += Math.hypot(pos.x - this.pos.x, pos.z - this.pos.z);
    this.pos.set(pos.x, pos.y || 0, pos.z); this.face = face; this.pose = pose; this.phase = walkPhase;
  }
  update(dt, t) {
    const g = this.g, rig = this.rig, h = this.h, { base, act } = parsePose(this.pose, this.pos.y), walking = base === 'walk' || base === 'crouch';
    const prev = this.rot; let df = this.face - this.rot; df = Math.atan2(Math.sin(df), Math.cos(df));
    this.rot = this.fresh ? this.face : this.rot + df * Math.min(1, dt * 8);
    g.turn += ((this.rot - prev) / Math.max(dt, 1e-3) - g.turn) * Math.min(1, dt * 10);
    const sk = walking ? (this.phase !== undefined ? 1 : Math.min(1, this.moved / Math.max(dt, 1e-3) / (1.2 * Math.sqrt(h)))) : 0;
    if (this.phase !== undefined) g.p = this.phase; else { g.p += this.moved / (CYCLE * h); if (!walking && act !== 'run' && g.w < .02) g.p = 0; }
    this.moved = 0;
    if (act !== 'run') g.w = this.fresh ? (walking ? 1 : 0) : g.w + ((walking ? 1 : 0) - g.w) * Math.min(1, dt * (walking ? 6 : 7));
    if (this.lookOff) rig.head.rotation.x += this.lookOff;   // 0.27.19: last frame's look up, taken off again
    animateActivity(this, this.pose, dt, t + g.t0, sk, this.pos.y);
    this.lookOff = base === 'lie' ? 0 : .5 * feelLook(g.t0); rig.head.rotation.x -= this.lookOff;   // a jolt: everyone looks up a moment
    const lie = ss(this.k.lie || 0), fx = Math.sin(this.rot), fz = Math.cos(this.rot), off = .76 * h * lie;
    const floor = base === 'sit' || base === 'lie' || this.pos.y >= .3 ? 0 : this.pos.y;   // standing on a stage or a treadmill
    const root = rig.root;
    root.position.set(this.pos.x + fx * off, L(floor, (this.pos.y > 0 ? this.pos.y : CROWD_SEAT[base] || CROWD_SEAT.sit) + .17 * h, lie), this.pos.z + fz * off);   // as before 0.27.0, getting out of bed
    root.rotation.set(-Math.PI / 2 * lie, this.rot, 0);
    if (this.rootOn) recRoot(this, root, t + g.t0);       // 0.81.0: in the water, up the wall, tumbling (8c)
    root.updateMatrixWorld(true);
    this.fresh = false;
  }
}
class CrowdChunk {
  constructor() {
    this.slots = new Array(CROWD_PER).fill(null); this.dirty = false; this.sphere = new THREE.Sphere();
    const n = CROWD_PER * CROWD_BONES, inv = []; for (let i = 0; i < n; i++) inv.push(new THREE.Matrix4());
    this.skel = new THREE.Skeleton(new Array(n).fill(CROWD_REST), inv);
    this.mesh = new THREE.SkinnedMesh(CROWD_EMPTY, CROWD_MAT); this.mesh.bind(this.skel, new THREE.Matrix4());
    this.mesh.castShadow = this.mesh.receiveShadow = true; this.mesh.visible = false;
    this.mesh.raycast = () => {};                        // taps go through crowd.near, not the mesh
    scene.add(this.mesh);
  }
  put(p, i) {
    this.slots[i] = p; p.chunk = this; p.slot = i; this.dirty = true;
    for (let b = 0; b < CROWD_BONES; b++) this.skel.bones[i * CROWD_BONES + b] = (b < CROWD_JOINTS ? p.joints[b] : p.propBones[b - CROWD_JOINTS]) || CROWD_REST;
  }
  take(p) {
    this.slots[p.slot] = null; this.dirty = true;
    for (let b = 0; b < CROWD_BONES; b++) this.skel.bones[p.slot * CROWD_BONES + b] = CROWD_REST;
    p.chunk = null; p.slot = -1;
  }
  rebuild() {                                            // only when someone joins, leaves, changes detail or picks up a prop
    // 0.27.28: the arrays and GPU buffers are kept and reused (half as big again when they grow), the skin weights
    // written once, and only the slots from the first one that changed are written and uploaded (from the lowest change
    // since the mesh was last drawn: pv, pi, reset by onBeforeRender, which comes after the upload). Same triangles, same order.
    this.dirty = false;
    const packs = p => [p.packOf(p.lod), ...propList(p.propKey).map(([b, kind]) => propPack(kind, p.lod, b))];
    const lay = this.slots.map(p => p ? packs(p) : null); let nv = 0, ni = 0;
    for (const qs of lay) if (qs) for (const q of qs) { nv += q.nv; ni += q.ni; }
    this.nv = nv; this.ni = ni;
    if (!nv) { this.mesh.geometry = CROWD_EMPTY; if (this.geo) this.geo.dispose(); this.geo = this.buf = this.lay = null; return; }
    let A = this.buf;
    if (!A || nv > A.cv || ni > A.ci) {
      const cv = Math.ceil(nv * 1.5), ci = Math.ceil(ni * 1.5);
      A = this.buf = { cv, ci, P: new Float32Array(cv * 3), N: new Float32Array(cv * 3), C: new Float32Array(cv * 3),
        SI: new Uint16Array(cv * 4), SW: new Uint8Array(cv * 4), I: cv > 65535 ? new Uint32Array(ci) : new Uint16Array(ci) };
      for (let i = 0; i < cv; i++) A.SW[i * 4] = 255;
      if (this.geo) this.geo.dispose();
      const geo = this.geo = new THREE.BufferGeometry();
      geo.setAttribute('position', new THREE.BufferAttribute(A.P, 3)); geo.setAttribute('normal', new THREE.BufferAttribute(A.N, 3));
      geo.setAttribute('color', new THREE.BufferAttribute(A.C, 3));
      geo.setAttribute('skinIndex', new THREE.BufferAttribute(A.SI, 4)); geo.setAttribute('skinWeight', new THREE.BufferAttribute(A.SW, 4, true));
      geo.setIndex(new THREE.BufferAttribute(A.I, 1)); geo.boundingSphere = this.sphere;
      this.lay = null; this.mesh.onBeforeRender = () => { this.pv = this.pi = Infinity; };
    }
    const old = this.lay, same = (x, y) => x === y || !!x && !!y && x.length === y.length && x.every((q, k) => q === y[k]);
    let s0 = 0, o = 0, oi = 0;
    if (old) for (; s0 < lay.length && same(old[s0], lay[s0]); s0++) if (lay[s0]) for (const q of lay[s0]) { o += q.nv; oi += q.ni; }
    const o0 = o, oi0 = oi;
    for (let s = s0; s < lay.length; s++) {
      if (!lay[s]) continue;
      const b0 = s * CROWD_BONES;
      for (const q of lay[s]) {
        A.P.set(q.P, o * 3); A.N.set(q.N, o * 3); A.C.set(q.C, o * 3);
        for (let i = 0; i < q.nv; i++) A.SI[(o + i) * 4] = b0 + q.B[i];
        for (let i = 0; i < q.ni; i++) A.I[oi++] = q.I[i] + o;
        o += q.nv;
      }
    }
    this.lay = lay; const pv = this.pv = Math.min(this.pv === undefined ? Infinity : this.pv, o0), pi = this.pi = Math.min(this.pi === undefined ? Infinity : this.pi, oi0);
    const at = this.geo.attributes;
    for (const [x, n] of [[at.position, 3], [at.normal, 3], [at.color, 3], [at.skinIndex, 4]]) { x.updateRange.offset = pv * n; x.updateRange.count = (nv - pv) * n; x.needsUpdate = true; }
    const ix = this.geo.index; ix.updateRange.offset = pi; ix.updateRange.count = ni - pi; ix.needsUpdate = true;
    this.geo.setDrawRange(0, ni); this.mesh.geometry = this.geo;
  }
}
const crowd = {
  people: [], chunks: [], visible: true, made: 0,
  add(spec) {
    if (!CROWD_MAT) {
      CROWD_MAT = new THREE.MeshStandardMaterial({ vertexColors: true, roughness: .62, metalness: .04, skinning: true });   // as CHAR_MAT
      CROWD_EMPTY = new THREE.BufferGeometry();
      // one bone texture holds any number of bones; without float textures, fit a group into the shader's uniforms
      CROWD_PER = renderer.capabilities.floatVertexTextures ? 12 : Math.max(1, Math.floor(Math.floor((renderer.capabilities.maxVertexUniforms - 20) / 4) / CROWD_BONES) - 1);
    }
    const p = new CrowdPerson(spec, this.made++);
    let c = this.chunks.find(c => c.slots.includes(null)); if (!c) this.chunks.push(c = new CrowdChunk());
    c.put(p, c.slots.indexOf(null)); this.people.push(p);
    return p;
  },
  remove(p) {
    if (!p || !p.chunk) return;
    p.chunk.take(p); this.people.splice(this.people.indexOf(p), 1);
    CROWD_KEPT.delete(p.look); CROWD_KEPT.set(p.look, { geo: p.geo, jparts: p.jparts });   // the newest last; the oldest go past CROWD_KEEP
    for (const k of CROWD_KEPT.keys()) { if (CROWD_KEPT.size <= CROWD_KEEP) break; CROWD_KEPT.delete(k); }
  },
  clear() { for (const p of this.people.slice()) this.remove(p); },
  near(x, z, r = .45) {                                  // who's standing (or sitting) at a spot, for taps
    let best = null, bd = r;
    for (const p of this.people) { const d = Math.hypot(p.pos.x - x, p.pos.z - z); if (d < bd) { bd = d; best = p; } }
    return best;
  },
  update(dt, t) {
    machineFx.tick(dt, t);                               // wear and faults on the machines (0.27.9)
    gardenView.tick(t);                                  // the garden's crops grow with the galley's beds (0.27.23)
    tableTrays.tick();                                   // trays on the mess tables in front of seated diners (0.27.37)
    deviceHook(); bubbles.tick(dt);                      // the device pose's hook and chatter bubbles (0.27.13)
    if (CROWD_DEMO) CROWD_DEMO.tick(dt, t);
    if (POSE_DEMO) POSE_DEMO.tick(dt, t);
    if (REC_DEMO) REC_DEMO.tick(dt, t);
    if (SEAT_DEMO) SEAT_DEMO.tick(dt, t);
    if (!this.chunks.length) return;
    // 0.27.19: at a ship-wide event's gathering on this deck (FEEL_S.gather: the storm's all-clear party), the coarse
    // level of detail starts nearer (CROWD_GATHER2 tiles) once the deck holds more than CROWD_GATHER people
    const gather = FEEL_S.gather && this.people.length > CROWD_GATHER, many = this.people.length > CROWD_MANY || gather;
    const allFar = camera.zoom < CROWD_FAR_ZOOM, far2 = gather ? CROWD_GATHER2 : CROWD_FAR2;
    // 0.27.27: posing (the body's place and its limbs) is the crowd's main cost, and in a busy room at the usual zoom most people are off
    // screen. Each frame only those in view, with a CROWD_POSE_MARGIN margin that covers shadows thrown on screen from
    // just outside, are posed; the rest every CROWD_POSE_EVERY frames with the time they missed. Anyone the player is
    // talking to or following (a crew agent's talking or esc), a new person, and everyone after the camera turns or
    // zooms are posed at once, so an off-screen body waits at most 9 frames. Posing uses each person's own random stream and writes only their rig (root and limbs): nothing the sim reads.
    const az0 = this.poseAz, zm0 = this.poseZoom; this.poseAz = az; this.poseZoom = camera.zoom; this.poseN = (this.poseN || 0) + 1;
    const all = az0 === undefined || Math.abs(az - az0) > .002 || zm0 !== camera.zoom;
    if (!all) { _poseFr.setFromProjectionMatrix(_poseM.multiplyMatrices(camera.projectionMatrix, camera.matrixWorldInverse)); _poseKeep.clear(); for (let i = 0; i < DECK_CREW.length; i++) { const a = DECK_CREW[i]; if (a.h && (a.talking > 0 || a.esc)) _poseKeep.add(a.h); } }
    this.people.forEach((p, i) => {
      const d = Math.hypot(p.pos.x - target.x, p.pos.z - target.z);
      let lod = allFar || d > CROWD_FAR + (p.lod ? -.5 : .5) ? 1 : 0;
      if (many && lod && (allFar || d > far2 + (p.lod === 2 ? -.5 : .5))) lod = 2;   // only in a big crowd: normal play never gets here
      if (lod !== p.lod) { p.lod = lod; p.chunk.dirty = true; }
      p.poseDt = (p.poseDt || 0) + dt;
      if (all || p.fresh || p.chunk.dirty || (this.poseN + i) % CROWD_POSE_EVERY === 0 || _poseKeep.has(p) || _poseFr.intersectsSphere(_poseS.set(_poseV.set(p.pos.x, 1, p.pos.z), CROWD_POSE_MARGIN))) {
        p.update(Math.min(p.poseDt, .5), t); p.poseDt = 0;
      }
    });
    for (const c of this.chunks) {
      if (c.dirty) c.rebuild();
      const sl = c.slots; let n = 0; for (let i = 0; i < sl.length; i++) if (sl[i]) n++;   // 0.27.30: counted, not filtered into a new array each frame
      c.mesh.visible = this.visible && n > 0;
      if (!n) continue;
      const s = c.sphere.center.set(0, 0, 0); for (let i = 0; i < sl.length; i++) if (sl[i]) s.add(sl[i].rig.root.position); s.divideScalar(n);
      let r = 0; for (let i = 0; i < sl.length; i++) { const p = sl[i]; if (p) r = Math.max(r, p.rig.root.position.distanceTo(s) + 1.9 * p.h); }
      c.sphere.radius = r;
    }
  },
  stats() {
    let verts = 0, tris = 0;
    for (const c of this.chunks) if (c.mesh.geometry !== CROWD_EMPTY) { verts += c.nv; tris += c.ni / 3; }
    return { people: this.people.length, chunks: this.chunks.length, perChunk: CROWD_PER, verts, tris, far: this.people.filter(p => p.lod).length, coarse: this.people.filter(p => p.lod === 2).length };
  },
};

// ---- machine looks (0.27.9, answers pass rows 2 and 3): wear and faults, drawn on the machines. Section 17's
// machineLook(id) says what a machine shows: { state, blink, dim, drip, flicker }, each 0..1 or true. Without it nothing is
// drawn. All the machines on the deck share four instanced meshes: red lamps that blink, drips, dark plates over
// screens, and light glows that flicker. That's at most 4 draw calls, none while all is well, no shadows, no R().
// Where: from the machine's `at` and `face`, or its optional look: { lamp, drip, light: [dx, y, dz], screen: [dx, y, dz, w, h] }.
// dx and dz are tiles from the centre of `at` (dx to the right as you face its front, dz out of its front), y and w, h in
// metres. On Deck 3 the garden's leaves also yellow while its irrigation pumps or nutrient dosing are poor or failing.
// ?looks in the address turns every effect on, on every machine, to check where they go.
// 0.27.10: while a deck's light relays flicker, some of its lamps stutter (lamps(t), called by the main loop after
// applyLight). And a shower someone is using sprays (one more instanced mesh, hidden when no one showers): thin and
// patchy while the ship's water or heat is below 50, worse below 25. ----
const MACHINE_FX_ALL = urlFlag('looks') !== null, MACHINE_FX_MAX = 64, MACHINE_WILT = col('#a08a3c');
const machineFx = {
  deck: undefined, list: [], next: 0, mesh: null, o: new THREE.Object3D(), lightIds: [], lampFl: 0, showers: [], weak: 0, sprayMesh: null, nextS: 0,
  make() {                                               // made the first time a machine shows something
    const mk = (geo, c, opacity) => {
      const m = new THREE.InstancedMesh(geo, new THREE.MeshBasicMaterial({ color: col(c), transparent: opacity < 1, opacity, depthWrite: opacity >= 1 }), MACHINE_FX_MAX);
      m.frustumCulled = false; m.visible = false; m.count = 0; m.raycast = () => {}; scene.add(m); return m;
    };
    this.mesh = { lamp: mk(new THREE.SphereGeometry(.06, 10, 8), '#ff3b30', 1), drip: mk(new THREE.SphereGeometry(.022, 6, 5), '#9fd8ff', .85),
      screen: mk(new THREE.BoxGeometry(1, 1, .006), '#05080c', .62), light: mk(new THREE.SphereGeometry(.13, 10, 8), '#fff1c4', .6) };
  },
  spots(n) {                                             // the deck's machines, and where each effect goes
    this.deck = n; this.list = []; this.next = 0; this.lightIds = []; this.lampFl = 0;
    this.showers = n === null ? [] : (DECKS[n].places || []).filter(p => p.type === 'shower')   // where each shower's spray falls
      .map(p => ({ id: p.id, x: (p.xy ? p.xy[0] : p.at[0] + .5) - OX, z: (p.xy ? p.xy[1] : p.at[1] + .5) - OZ }));
    if (typeof machineLook !== 'function' && !MACHINE_FX_ALL || typeof machineList !== 'function') return;
    this.lightIds = machineList().filter(m => m.deck === n && m.kind === 'lights').map(m => m.id);   // stand-ins too: the deck's light relays
    for (const m of machineList()) {
      if (m.deck !== n || m.stub || !m.at) continue;
      const a = { s: 0, n: Math.PI, e: Math.PI / 2, w: -Math.PI / 2 }[m.face] || 0, c = cellPos(m.at[0], m.at[1]), lk = m.look || {};
      const front = m.panel && (m.panel[0] !== m.at[0] || m.panel[1] !== m.at[1]) ? .45 : -.25;   // its front: on the tile's edge, or against the wall
      const at = ([dx, y, dz]) => new THREE.Vector3(c.x + dx * Math.cos(a) + dz * Math.sin(a), y, c.z - dx * Math.sin(a) + dz * Math.cos(a));
      this.list.push({ id: m.id, a, ph: this.list.length * .37, look: null,
        lamp: at(lk.lamp || [0, 1.2, front]), drip: at(lk.drip || [0, .9, front + .06]), light: at(lk.light || [0, 2.1, front]),
        screen: lk.screen ? { p: at(lk.screen), w: lk.screen[3], h: lk.screen[4] } : null });
    }
  },
  wilt(n) {                                              // the garden's plants yellow while its irrigation or dosing is poor or failing
    let w = 0;
    for (const s of n === 3 ? this.list : []) if (/irrigation|nutrient/.test(s.id)) w = Math.max(w, { poor: .45, failing: 1 }[MACHINE_FX_ALL ? 'failing' : (s.look || {}).state] || 0);
    if (w === (this.wilted || 0)) return;
    this.wilted = w;                                     // GD.leaves are the garden kit's (and the promenade planters'): only on Deck 3
    if (!this.leafBase) this.leafBase = GD.leaves.map(m => m.color.clone());
    GD.leaves.forEach((m, i) => m.color.copy(this.leafBase[i]).lerp(MACHINE_WILT, w * .65));
  },
  lamps(t) {                                             // after applyLight: a third of the lamps (two thirds when failing) stutter
    if (!this.lampFl) return;
    LAMPS.forEach((L, i) => {
      if (i % 3 && !(this.lampFl >= 1 && i % 3 === 1)) return;
      const hh = Math.sin(Math.floor(t * 9) * 12.9898 + i * 78.233) * 43758.5453;
      if (hh - Math.floor(hh) < .5 * Math.min(1, this.lampFl)) L.l.intensity *= .15;
    });
  },
  spray(t) {                                             // showers in use: streaks falling from the head; fewer and patchy when water or heat is poor
    if (!this.showers.length || typeof placeBusy !== 'function') { if (this.sprayMesh) this.sprayMesh.visible = false; return; }
    const on = this.showers.filter(s => placeBusy(s.id));
    if (on.length && t >= this.nextS) {
      this.nextS = t + .5;
      const sys = typeof shipSystems === 'function' ? shipSystems() : null, q = sys ? Math.min(sys.water, sys.heat) : 100;
      this.weak = q < 25 ? 1 : q < 50 ? .5 : 0;
    }
    if (!on.length) { if (this.sprayMesh) this.sprayMesh.visible = false; return; }
    if (!this.sprayMesh) {
      this.sprayMesh = new THREE.InstancedMesh(new THREE.CylinderGeometry(.012, .012, .28, 3), new THREE.MeshBasicMaterial({ color: col('#e6f7ff'), transparent: true, opacity: .7, depthWrite: false }), 120);
      this.sprayMesh.frustumCulled = false; this.sprayMesh.raycast = () => {}; scene.add(this.sprayMesh);
    }
    const m = this.sprayMesh, o = this.o, per = this.weak >= 1 ? 4 : this.weak ? 7 : 12; let c = 0;
    on.forEach((s, j) => {
      if (this.weak) { const hh = Math.sin(Math.floor(t * 3) * 12.9898 + j * 78.233) * 43758.5453; if (hh - Math.floor(hh) < .3 + .3 * this.weak) return; }   // sputtering
      for (let k = 0; k < per && c < 120; k++) {
        const a = k * 2.4, r = .04 + .14 * ((k * .618) % 1), u = (t * 2.3 + k * .37) % 1;
        o.position.set(s.x + Math.cos(a) * r, 1.9 - u * 1.75, s.z + Math.sin(a) * r); o.rotation.set(0, 0, 0); o.scale.set(1, 1, 1); o.updateMatrix();
        m.setMatrixAt(c++, o.matrix);
      }
    });
    m.count = c; m.visible = c > 0; m.instanceMatrix.needsUpdate = true;
  },
  tick(dt, t) {
    const n = deckDef ? deckDef.num : null;
    if (n !== this.deck) this.spots(n);
    this.spray(t);
    if (t >= this.next && (this.list.length || this.wilted || this.lightIds.length)) {   // the machines' state, twice a second
      this.next = t + .5;
      for (const s of this.list) s.look = MACHINE_FX_ALL ? { blink: 1, dim: 1, drip: 1, flicker: 1 } : machineLook(s.id) || null;
      this.lampFl = 0; for (const id of this.lightIds) { const lk = MACHINE_FX_ALL ? { flicker: 1 } : machineLook(id) || {}; this.lampFl = Math.max(this.lampFl, lk.flicker === true ? 1 : +lk.flicker || 0); }
      this.wilt(n);
    }
    if (!this.list.length) { if (this.mesh) for (const k in this.mesh) this.mesh[k].visible = false; return; }
    const v = x => x === true ? 1 : Math.max(0, Math.min(1, +x || 0)), cnt = { lamp: 0, drip: 0, screen: 0, light: 0 }, o = this.o;
    let any = false;
    const put = (k, p, sx, sy, sz, ry, dy = 0) => {
      if (cnt[k] >= MACHINE_FX_MAX) return;
      o.position.set(p.x, p.y + dy, p.z); o.rotation.set(0, ry, 0); o.scale.set(sx, sy, sz); o.updateMatrix();
      this.mesh[k].setMatrixAt(cnt[k]++, o.matrix);
    };
    for (const s of this.list) {
      const lk = s.look; if (!lk) continue;
      const blink = v(lk.blink), dim = v(lk.dim), drip = v(lk.drip), fl = v(lk.flicker);
      if (!(blink || dim && s.screen || drip || fl)) continue;
      if (!this.mesh) this.make();
      any = true;
      if (blink && (t * (.6 + blink) + s.ph) % 1 < .5) put('lamp', s.lamp, 1, 1, 1, s.a);   // faster the worse it is
      if (dim && s.screen) put('screen', s.screen.p, s.screen.w, s.screen.h, 1, s.a);
      if (drip) {                                        // a drop falls every so often; more often the worse the leak
        const per = 2.4 - 1.6 * drip, fall = Math.sqrt(2 * s.drip.y / 9.8);
        for (const k of [0, .5]) { const u = ((t + s.ph * 3 + k * per) % per) / fall; if (u < 1) put('drip', s.drip, 1, 1.5, 1, 0, -s.drip.y * u * u); }
      }
      if (fl) {                                          // on, with stutters: a hash of the moment, never R()
        const hh = Math.sin(Math.floor(t * 11) * 12.9898 + s.ph * 78.233) * 43758.5453;
        if (hh - Math.floor(hh) > .45 * fl) put('light', s.light, 1, 1, 1, 0);
      }
    }
    if (!this.mesh) return;
    for (const k in this.mesh) { const m = this.mesh[k]; m.count = cnt[k]; m.visible = any && cnt[k] > 0; m.instanceMatrix.needsUpdate = true; }
  },
};

// ---- how a ship-wide event feels on your deck (0.27.19, Pillar 3 C7). Section 18's eventFeel calls shipFeel(kinds, len)
// for a felt moment: 'jolt' (a short light camera shake and a flash of ion light in the windows), 'lightsDip' (every
// light dips and comes back), 'flicker' (then it flickers for the rest of len seconds). shipFeelFrame(t, dt) runs every
// frame from the main loop, after applyLight and the camera: the event's mood by phase (FEEL_MOODS: in the storm the
// space outside shifts to violet and teal with slow drifting bands, and the ship's light cools a little), the odd
// flicker while eventMod('effect', 'flicker'), and emergency lighting while section 17's blackoutAt has this deck
// dark: the lights cut out for a second, then come back dim red-amber, and flicker back to normal at the end.
// Visual only, in real time; never the simulation, never R(). Reduced motion: no shake, and flickers become soft dips.
// With no event on, it returns at once and changes nothing.
const FEEL_CALM = matchMedia('(prefers-reduced-motion: reduce)').matches;
const FEEL_MOODS = {                                     // by event id: its mood (0-1) in each phase, and its colours
  ionStorm: { phases: { warning: .15, onset: .75, escalation: 1 }, a: col('#7a3cff'), b: col('#19d6c8'), light: col('#a99cff'), bg: col('#4a2488') },
};
const FEEL_EMERG = col('#ff7a3c'), FEEL_WHITE = new THREE.Color(1, 1, 1);
const FEEL_S = { t0: -1, until: -1, kinds: [], mood: 0, moodT: 0, def: null, flick: false, dark: false, darkT: -99, check: -1, deck: undefined, first: true, gather: false };
function shipFeel(kinds, len = 4) { const s = FEEL_S; s.t0 = simNow() / 1000; s.until = s.t0 + len; s.kinds = kinds.slice(); }
// ---- the garden view (0.27.23, with the galley's working garden, section 16): the crops on Deck 3's raised beds and
// bean trellises grow with the galley's beds (SHIP.galley.garden.beds: [crop, grown, days]): bare soil just after a
// pick, seedlings, then full and fruiting when ripe. The kits record each plant (GARDEN_PLOTS, o.live) instead of
// building it; here they're drawn as instances, one InstancedMesh per shape and material, culled with the garden.
// Looked at about once a second; the matrices are only rewritten when a bed's growth has moved on. The nth bed of a
// crop on the deck is the galley's nth bed of it; beds with no place in the garden (the third bean bed, the root
// vegetables) aren't shown. The grow racks' microgreens and the flower beds stay as they were. Plants in a tall piece
// (the bean trellises) get their own copies of the materials, in that room's fade list, so they fade with it (0.27.24).
// 0.27.37 (the user: "look how many crew members don't have trays"): a seated diner who has a tray (section 10's
// meal.served && meal.tray, read only) has it on the table in front of them: the tray in one of the mess's three
// colours, a plate and a mug, like yours (TRAY_ON). All of them are two instanced meshes (2 draw calls; no shadows; the
// trays' colours are set while the count is full, since r128 sizes the colour buffer by the count). A long table's own
// tray and cup (section 4b's longTable) stands in for the diner's at the one seat it's in front of. They're
// placed again only when someone sits down or gets up, checked every 15th frame.
const tableTrays = {
  tray: null, ware: null, n: 0, sig: 0, fr: 0, MAX: 96, d: new THREE.Object3D(), c: null, own: null, ownOf: null, eaters: [],
  make() {
    const tray = new THREE.BoxGeometry(.42, .02, .3), plate = new THREE.CylinderGeometry(.09, .09, .016, 16), cup = new THREE.CylinderGeometry(.035, .03, .08, 10);
    plate.translate(-.06, .018, .02); cup.translate(.13, .05, -.07);
    const ware = new THREE.BufferGeometry(), P = [], N = [], I = [];   // the plate and the mug as one shape
    for (const g of [plate, cup]) { const o = P.length / 3; P.push(...g.attributes.position.array); N.push(...g.attributes.normal.array); for (const i of g.index.array) I.push(i + o); g.dispose(); }
    ware.setAttribute('position', new THREE.Float32BufferAttribute(P, 3)); ware.setAttribute('normal', new THREE.Float32BufferAttribute(N, 3)); ware.setIndex(I);
    this.tray = new THREE.InstancedMesh(tray, std('#ffffff', .5), this.MAX); this.ware = new THREE.InstancedMesh(ware, MESS.white, this.MAX);
    this.c = MESS.trays.map(m => m.color.clone()); for (let k = 0; k < this.MAX; k++) this.tray.setColorAt(k, this.c[0]);
    for (const m of [this.tray, this.ware]) { m.count = 0; m.castShadow = false; m.receiveShadow = true; m.frustumCulled = false; m.raycast = () => {}; m.visible = false; scene.add(m); }
  },
  tick() {
    if (++this.fr % 15 !== 1) return;
    const on = typeof DECK_CREW !== 'undefined' && deckDef && deckDef.num === 3 && (typeof crewOn === 'undefined' || crewOn);
    let sig = 0, n = 0;
    if (on) for (let k = 0; k < DECK_CREW.length && n < this.MAX; k++) {
      const a = DECK_CREW[k], m = a.meal, sp = a.spot;
      if (!m || !m.served || !m.tray || !a.settled || !sp || sp.pose !== 'sit' || sp.room !== 'M') continue;
      sig = (sig * 31 + k * 977 + (sp.x * 100 | 0)) | 0; n++;
    }
    if (n === this.n && sig === this.sig) return;
    this.n = n; this.sig = sig;
    for (const h of this.eaters) h.eating = false;      // 0.27.38: who eats (animateActivity: hands at the table, a fork, bites)
    this.eaters.length = 0;
    if (n) for (let k = 0; k < DECK_CREW.length; k++) {
      const a = DECK_CREW[k], m = a.meal, sp = a.spot;
      if (m && m.served && m.tray && a.settled && sp && sp.pose === 'sit' && sp.room === 'M') { a.h.eating = true; this.eaters.push(a.h); }
    }
    if (!this.tray) { if (!n) return; this.make(); }
    if (this.ownOf !== SEAT_RC.gen) {                    // the long tables' own trays, where they are on this deck (as longTable puts them)
      this.ownOf = SEAT_RC.gen; this.own = []; const b = ROOM_BOX.M;
      if (b) for (const [x, z] of [[2.6, 1.0], [7.4, 1.0], [2.6, 4.0], [7.4, 4.0]]) { const d = this.d; d.position.set(X0(b.i0) + x, 0, Z0(b.j0) + z); d.rotation.set(0, FACING.n || 0, 0); d.updateMatrixWorld(); this.own.push(d.localToWorld(new THREE.Vector3(.4, 0, .22))); }
    }
    let i = 0;
    if (n) for (let k = 0; k < DECK_CREW.length && i < n; k++) {
      const a = DECK_CREW[k], m = a.meal, sp = a.spot;
      if (!m || !m.served || !m.tray || !a.settled || !sp || sp.pose !== 'sit' || sp.room !== 'M') continue;
      const f = sp.face || 0, x = sp.x + Math.sin(f) * TRAY_REACH, z = sp.z + Math.cos(f) * TRAY_REACH, d = this.d;
      if (this.own.some(o => Math.hypot(o.x - x, o.z - z) < .3)) continue;   // the table's own tray is theirs
      d.position.set(x, .78, z); d.rotation.set(0, f, 0); d.updateMatrix();
      this.tray.setMatrixAt(i, d.matrix); this.ware.setMatrixAt(i, d.matrix); this.tray.setColorAt(i, this.c[idHash(a.p.id) % this.c.length]); i++;
    }
    for (const m of [this.tray, this.ware]) { m.count = i; m.visible = i > 0; m.instanceMatrix.needsUpdate = true; }
    this.tray.instanceColor.needsUpdate = true;
  },
};
const gardenView = {
  root: null, list: [], key: '', next: 0, m: new THREE.Matrix4(), p: new THREE.Matrix4(), v: new THREE.Vector3(), s: new THREE.Vector3(), q: new THREE.Quaternion(),
  make() {                                               // the deck's instanced meshes, once per deck build
    this.root = deckRoot; this.list = []; this.key = ''; this.next = 0; if (!deckRoot || !GARDEN_PLOTS.length) return;
    deckRoot.updateMatrixWorld(true);
    const geo = { leaf: LEAF_GEO, ball: new THREE.SphereGeometry(1, 10, 7), pod: new THREE.CylinderGeometry(.012, .01, .14, 5) }, by = new Map(), box = new THREE.Box3();
    const tallOf = P => { for (let o = P.g.parent; o; o = o.parent) { const t = TALL.find(t => t.g === o); if (t) return t; } return null; };
    for (const P of GARDEN_PLOTS) for (const sl of P.slots) {
      const t = tallOf(P), k = sl.geo + '|' + sl.mat.uuid + '|' + (t ? TALL.indexOf(t) : '');
      let b = by.get(k);
      if (!b) {                                          // in a tall piece (the trellises): its own copy of the material, faded with the room (0.27.24)
        const mat = t ? sl.mat.clone() : sl.mat; if (t) { mat.userData.base = { op: sl.mat.opacity, tr: sl.mat.transparent }; t.mats.push(mat); }
        by.set(k, b = { geo: sl.geo, mat, items: [] });
      }
      b.items.push({ P, sl }); box.expandByPoint(this.v.set(sl.x, sl.y, sl.z).applyMatrix4(P.g.matrixWorld));
    }
    const sphere = box.getBoundingSphere(new THREE.Sphere()); sphere.radius += 1;
    for (const b of by.values()) {
      const g = geo[b.geo].clone(); g.boundingSphere = sphere.clone();   // culled with the garden as a whole
      const im = new THREE.InstancedMesh(g, b.mat, b.items.length); im.castShadow = im.receiveShadow = true; im.raycast = () => {};
      deckRoot.add(im); this.list.push({ im, items: b.items });
    }
  },
  grown(P) {                                             // a plot's growth, 0 (just picked) to 1 (ripe); 1 without the galley's beds
    const G = SHIP.galley && SHIP.galley.garden, ci = typeof GARDEN_CROPS !== 'undefined' ? GARDEN_CROPS.findIndex(c => c.id === P.crop) : -1;
    if (!G || ci < 0) return 1;
    const b = G.beds.filter(x => x[0] === ci)[P.n]; return b ? Math.min(1, b[1] / GARDEN_CROPS[ci].days) : 1;
  },
  tick(t) {
    if (this.root !== deckRoot) this.make();
    if (!this.list.length || t < this.next) return;
    this.next = t + 1;
    const gr = new Map(GARDEN_PLOTS.map(P => [P, this.grown(P)])), key = [...gr.values()].map(x => Math.round(x * 50)).join();
    if (key === this.key) return;
    this.key = key;
    for (const { im, items } of this.list) {
      items.forEach(({ P, sl }, i) => {
        const g = gr.get(P), lf = g < .03 ? 0 : .3 + .7 * Math.min(1, g / .75), f = sl.fruit ? (g < .6 ? 0 : (g - .6) / .4) * lf : lf;
        if (!f) { im.setMatrixAt(i, LEAF_HIDE); return; }
        this.m.compose(this.v.set(sl.x, P.base + (sl.y - P.base) * lf, sl.z), this.q, this.s.set(sl.sx * f, sl.sy * f, sl.sz * f));
        im.setMatrixAt(i, this.p.multiplyMatrices(P.g.matrixWorld, this.m));
      });
      im.instanceMatrix.needsUpdate = true;
    }
  },
};
// a jolt's look up (0-1), for 8b's people: each a beat apart (by their animation offset), up for about two seconds
function feelLook(t0) {
  const s = FEEL_S; if (!s.kinds.includes('jolt')) return 0;
  const e = simNow() / 1000 - s.t0 - .25 - (t0 % 1) * .5;
  return e <= 0 || e > 3 ? 0 : e < .4 ? ss(e / .4) : e < 2.2 ? 1 : 1 - ss((e - 2.2) / .8);
}
const feelHash = (a, b) => { const h = Math.sin(a * 12.9898 + b * 78.233) * 43758.5453; return h - Math.floor(h); };
function shipFeelFrame(t, dt) {
  const s = FEEL_S, now = simNow() / 1000, dn = deckDef ? deckDef.num : null;
  if (now >= s.check || dn !== s.deck) {                 // twice a second: the event's phase, its flicker, this deck's blackout
    s.check = now + .5;
    const ev = typeof eventNow === 'function' ? eventNow() : null, md = ev && FEEL_MOODS[ev.id];
    if (md) s.def = md;
    s.moodT = md ? md.phases[ev.phase] || 0 : 0;
    s.flick = !!(ev && typeof eventMod === 'function' && eventMod('effect', 'flicker'));
    const bo = ev && typeof blackoutAt === 'function' ? blackoutAt(shipNow()) : null, dark = !!bo && bo.deck === dn;
    if (dark !== s.dark || dn !== s.deck) s.darkT = dn !== s.deck || s.first ? -99 : now;   // arriving on a dark deck: no cut-out
    s.dark = dark; s.deck = dn;
    const e = ev && SHIP.event, sd = e && SHIP_EVENTS[e.id], tn = shipNow();   // one of the event's gatherings on this deck, now (for 8b's crowd)
    s.gather = !!sd && (sd.moments || []).some(mo => mo.gathering && mo.where && mo.where.deck === dn && (at => tn >= at - 30 && tn < at + (mo.len || 60) + 30)((e.startDay - 1 + mo.at[0]) * 1440 + mo.at[1]));
    if (s.first) { s.mood = s.moodT; s.first = false; }
  }
  s.mood += (s.moodT - s.mood) * Math.min(1, dt * .4); if (Math.abs(s.mood - s.moodT) < .002) s.mood = s.moodT;
  const se = now - s.t0, felt = now < s.until, de = now - s.darkT;
  if (!s.mood && !felt && !s.flick && !s.dark && de > 2) { SKY.mat.uniforms.uWash.value = 0; return; }
  const has = k => felt && s.kinds.includes(k);
  let k = 1, emerg = s.dark ? 1 : 0, flash = 0;
  // a felt moment: the shake, the dip, then flickers
  if (has('jolt') && se < .8 && !FEEL_CALM) {
    const a = 5 * (1 - se / .8) ** 2 * (camera.top - camera.bottom) / camera.zoom / renderer.domElement.height;   // about 5 pixels
    camera.position.addScaledVector(_r, a * Math.sin(se * 58)).addScaledVector(_u, a * .7 * Math.sin(se * 43 + 1)); camera.updateMatrixWorld();
  }
  if (has('jolt') && se < .9) flash = 1 - se / .9;
  if (has('lightsDip')) k = se < .25 ? 1 - se / .25 * .65 : se < 1.4 ? .35 : Math.min(1, .35 + (se - 1.4) * .45);
  if (has('flicker') && se > 1.4) k *= FEEL_CALM ? .9 + .1 * Math.cos(se * 2) : feelHash(Math.floor(se * 8), 3) < .3 ? .55 : 1;
  // the odd flicker while the event's 'flicker' effect is on (about one in 30 tenths of a second)
  if (s.flick && !felt && !FEEL_CALM && feelHash(Math.floor(now * 9), 7) < .035) k *= .68;
  // emergency lighting: cut out, then dim red-amber; at the end it flickers back
  if (s.dark && de < 1.1) { k *= FEEL_CALM ? 1 - Math.min(1, de) * .9 : .08; emerg = de / 1.1; }
  else if (s.dark && de < 1.9 && !FEEL_CALM && feelHash(Math.floor(de * 12), 5) < .5) k *= .15;
  else if (!s.dark && de < .9) emerg = FEEL_CALM ? 1 - de / .9 : feelHash(Math.floor(de * 12), 6) < .5 ? 1 : 0;
  // the mood: the space outside and the ship's light
  const m = s.mood, d = s.def;
  if (m && d) {
    hemi.color.lerp(d.light, .28 * m); sun.color.lerp(d.light, .3 * m); sun.intensity *= 1 - .12 * m;
    scene.background.lerp(d.bg, .7 * m);
  }
  const U = SKY.mat.uniforms;
  if (d && (m || flash)) { U.uWash.value = .55 * m + .9 * flash * Math.max(m, .3); U.uT.value = t; U.uA.value.copy(d.a); U.uB.value.copy(d.b); }
  else U.uWash.value = 0;
  if (emerg) {
    const e = emerg; hemi.color.lerp(FEEL_EMERG, .62 * e); hemi.intensity *= 1 - .58 * e; sun.color.lerp(FEEL_EMERG, .6 * e); sun.intensity *= 1 - .85 * e;
    for (const L of LAMPS) L.l.intensity *= 1 - .75 * e;
  }
  if (k < 1) { hemi.intensity *= k; sun.intensity *= k; for (const L of LAMPS) L.l.intensity *= k; }
}

// ---- seeing yourself use the device (0.27.13, Pillar 3 C11): when section 19's deviceOn('open'|'close', fn) exists,
// opening the device sets player.deviceOut and the player raises it ('+device', HOLDS), closing puts it away. Hooked
// on the first frame it's there, so nothing happens without it. Something already in your hands wins.
let deviceHooked = false;
function deviceHook() {
  if (deviceHooked || typeof deviceOn !== 'function' || typeof player === 'undefined' || !player) return;
  deviceHooked = true;
  deviceOn('open', () => { player.deviceOut = true; }); deviceOn('close', () => { player.deviceOut = false; });
  try { deviceOn('phosphor', devicePropRecolour); } catch (e) {}   // 0.27.16: the screen follows a phosphor change in Settings
}
function devicePropRecolour() {                          // forget the built prop; anyone holding it gets the new one next frame
  if (_propGeos.device) _propGeos.device.dispose(); delete _propParts.device; delete _propGeos.device;
  for (const k of Object.keys(_propPacks)) if (k.startsWith('device')) delete _propPacks[k];
  if (typeof player !== 'undefined' && player && /device/.test(player.propKey || '')) player.propKey = null;
  for (const p of crowd.people) if (/device/.test(p.propKey || '') && p.chunk) p.chunk.dirty = true;
}

// ---- chatter bubbles (0.27.13, Pillar 3 C5, for section 20): bubbleSay(who, text, secs) shows a small speech bubble
// over someone's head for a few seconds. who: a crowd handle, a FullPerson or a Walker (anything with pos or obj, and
// h), or a point { x, y, z }. At most BUBBLE_MAX on screen (the oldest goes); a new line from the same person
// replaces theirs. Plain DOM (no draw calls), placed each frame from the 3D position; hidden off screen, when zoomed far
// out, or while bubbles.hidden (a dialogue panel). bubbleClear() removes them all. ----
const BUBBLE_MAX = 2;
// 0.47.9 (playtest: "bubbles shake or jump between two spots", on a phone): placed in place(), from the main loop just before the
// frame is drawn, with the camera already moved for this frame (they were placed in crowd.update, before the camera followed you, so
// each one lagged by however far the camera moved that frame, and on a phone's uneven frames that lag changed every frame); placed
// with a fractional-pixel transform, not whole-pixel left/top; and two overlapping bubbles keep their order and their stacking until
// they are clearly apart (pair, below). tick(dt) only counts their time down (crowd.update, while the ship runs)
const bubbles = { list: [], hidden: false, el: null, v: new THREE.Vector3(), on: [], pair: null,
  tick(dt) {
    for (const b of this.list.slice()) { b.t -= dt; if (b.t <= 0) { b.el.remove(); this.list.splice(this.list.indexOf(b), 1); } }
  },
  place() {
    if (!this.list.length) { this.pair = null; return; }
    const on = this.on, now = performance.now(), dts = this.at ? Math.min(.1, (now - this.at) / 1000) : 1, ease = Math.min(1, dts * 10), lim = 900 * dts; on.length = 0; this.at = now;   // lim: a slide never goes faster than 900 px a second (0.47.10)
    for (const b of this.list) {
      const w = b.who, p = w.pos || (w.obj && w.obj.position) || w, h = w.h || 1;
      const seat = w.pos && w.pos.y >= .3 ? w.pos.y : 0;   // seated: above the head on the seat; standing: above a standing head
      this.v.set(p.x, seat ? seat + 1.15 * h : (w.pos ? w.pos.y : w.obj ? w.obj.position.y : p.y || 0) + 2.0 * h, p.z).project(camera);
      const vis = !this.hidden && this.v.z < 1 && Math.abs(this.v.x) < 1 && this.v.y < .95 && this.v.y > -1;   // any zoom the camera allows (0.27.18)
      b.el.style.display = vis ? '' : 'none';
      if (!vis) continue;
      if (!b.w) { b.w = b.el.offsetWidth; b.hh = b.el.offsetHeight + (b.card.classList.contains('named') ? 10 : 0); }   // measured once (0.43.30), not every frame
      const hw = b.w / 2 + 8; b.ax = (this.v.x + 1) / 2 * innerWidth; b.x = Math.min(innerWidth - hw, Math.max(hw, b.ax)); b.y = b.ay = (1 - this.v.y) / 2 * innerHeight;
      on.push(b);
    }
    // 0.43.30: two bubbles that would cover each other move apart sideways, as far as their tails can still reach their
    // speakers, and if that isn't enough the older one sits higher
    if (on.length === 2) {
      // the same two as last frame keep their left-to-right order unless their speakers are clearly the other way round now,
      // and once stacked they stay stacked until they'd be 12 px apart side by side (0.47.9: no flipping from frame to frame)
      const P = this.pair && this.pair.l && on.includes(this.pair.l) && on.includes(this.pair.r) ? this.pair : null;
      const keep = P && P.r.ax - P.l.ax > -24, [a, c] = keep ? [P.l, P.r] : on[0].ax <= on[1].ax ? on : [on[1], on[0]], top = b => b.y - 9 - b.hh;
      const overY = () => Math.min(a.y, c.y) - Math.max(top(a), top(c)) + 6, overX = () => a.x + a.w / 2 - (c.x - c.w / 2) + 6;
      let stack = false;
      if (overY() > 0 && overX() > 0) {
        const fit = b => { const r = b.w / 2 - 18, hw = b.w / 2 + 8; b.x = Math.min(innerWidth - hw, Math.max(hw, Math.min(b.ax + r, Math.max(b.ax - r, b.x)))); };
        const d = overX() / 2; a.x -= d; c.x += d; fit(a); fit(c);
        stack = overX() > (keep && P.stack ? -12 : 0);
      } else stack = !!(keep && P.stack && overX() > -12 && overY() > -12);
      if (stack) { const old = on[0], other = on[1]; old.y = Math.min(old.y, top(other) - 6); }
      this.pair = { l: a, r: c, stack };
    } else this.pair = null;
    for (const b of on) {                                // a change of layout (side by side, stacked) slides in over a few frames; the speaker is followed exactly
      const ox = b.x - b.ax, oy = b.y - b.ay, step = d => Math.max(-lim, Math.min(lim, d * ease)); b.ox = b.ox === undefined ? ox : b.ox + step(ox - b.ox); b.oy = b.oy === undefined ? oy : b.oy + step(oy - b.oy);
      const hw = b.w / 2 + 8; b.x = Math.min(innerWidth - hw, Math.max(hw, b.ax + b.ox)); b.y = b.ay + b.oy;
    }
    for (const b of on) {
      b.el.style.transform = 'translate3d(' + b.x.toFixed(1) + 'px,' + b.y.toFixed(1) + 'px,0) translate(-50%,calc(-100% - 9px))'; b.el.style.opacity = Math.min(1, b.t * 2, (b.life - b.t) * 4).toFixed(2);
      const tx = Math.max(18 - b.w / 2, Math.min(b.w / 2 - 18, b.ax - b.x)).toFixed(0) + 'px';   // the tail still points at the speaker when the card is moved
      if (tx !== b.tx) { b.tx = tx; b.card.style.setProperty('--tx', tx); }
    }
  },
};
// 0.43.30: the speaker's name and department come from the crew on the deck (or who.p); a point or a stranger gets no tag
const BUBBLE_DEPT = { command: '#a83a32', helm: '#2f6aa3', comms: '#6a4fa3', survey: '#23808a', infirmary: '#2c8460', works: '#a3600f', watch: '#7a6618',
  galley: '#8f5a2e', garden: '#4a7f2c', store: '#4f6c8c', civilian: '#5f6b75', guest: '#86578a' };
function bubblePerson(who) {
  if (who.p && who.p.name) return who.p;
  if (typeof DECK_CREW !== 'undefined') for (let k = 0; k < DECK_CREW.length; k++) if (DECK_CREW[k].h === who) return DECK_CREW[k].p;
  return null;
}
function bubbleSay(who, text, secs = 4.5) {
  if (!who || !text) return null;
  if (!bubbles.el) { bubbles.el = document.createElement('div'); bubbles.el.style.cssText = 'position:fixed;inset:0;pointer-events:none;z-index:2;overflow:hidden'; document.body.appendChild(bubbles.el); }
  for (const b of bubbles.list.filter(b => b.who === who)) { b.el.remove(); bubbles.list.splice(bubbles.list.indexOf(b), 1); }
  while (bubbles.list.length >= BUBBLE_MAX) bubbles.list.shift().el.remove();
  const el = document.createElement('div'), card = document.createElement('div'), p = bubblePerson(who);
  el.className = 'bubw'; el.style.display = 'none'; card.className = 'bub';
  if (p) { const tag = document.createElement('span'); tag.className = 'who'; tag.textContent = p.name; tag.style.setProperty('--dc', BUBBLE_DEPT[p.dept] || BUBBLE_DEPT.civilian); card.appendChild(tag); card.classList.add('named'); }
  card.appendChild(document.createTextNode(text)); el.appendChild(card); bubbles.el.appendChild(el);
  const b = { who, text, el, card, t: secs, life: secs, w: 0, hh: 0, tx: '', ax: 0, x: 0, y: 0 }; bubbles.list.push(b); return b;
}
function bubbleClear() { for (const b of bubbles.list) b.el.remove(); bubbles.list.length = 0; }

// ---- pose lineup: ?poses in the address starts you on Deck 3's promenade at 10:30, with one of the crew doing each
// pose and activity in two rows, labelled, on stools and benches where they sit or lie. Like ?crowd, it never touches
// your save. Without the flag none of this exists. ----
const POSE_DEMO = (() => {
  if (urlFlag('poses') === null) return null;
  const POSES = ['stand', 'walk', 'work', 'sit', 'lie', 'run', 'row', 'lift', 'lie:lift', 'call', 'sit:call', 'browse',
    'pay', 'play', 'sit:play', 'water', 'cook', 'wash', 'fold', 'drink', 'sit:drink', 'read', 'sit:read', 'talk',
    'walk+tray', 'walk+toolbox', 'walk+datapad', 'crouch', 'stand+device', 'walk+device', 'punch', 'stretch', 'stand+go', 'walk+go', 'lie:bench', 'sit:talk', 'cycle'];
  const NAMES = { 'lie:lift': 'lift (mat)', 'lie:bench': 'bench press', 'sit:talk': 'talk (seated)', 'sit:call': 'call (seated)', 'sit:play': 'play (keys)', 'sit:drink': 'drink (seated)', 'sit:read': 'read (seated)', row: 'row' };
  let here = [], furn = null, labels = null, started = false;
  const v = new THREE.Vector3();
  function fill() {
    const people = ROSTER.filter(p => !p.story), seatH = .49;
    furn = new THREE.Group(); scene.add(furn);
    labels = document.createElement('div'); labels.style.cssText = 'position:fixed;inset:0;pointer-events:none;z-index:2';
    document.body.appendChild(labels);
    let n = 0, m = 0;                                    // upright poses in two rows east of the lift; the two lying ones on benches to the west
    here = POSES.map(pose => {
      const { base, act } = parsePose(pose, 0), lie = base === 'lie', k = lie ? m++ : n++;
      const x = lie ? X0(14) + .5 : X0(23) + .75 + (k % 15) * 1.15, z = lie ? Z0(10) + .4 + k * 1.2 : Z0(k < 15 ? 9 : 12) + .5;
      const seated = base === 'sit' || act === 'row', lying = base === 'lie';
      const g = new THREE.Group(); g.position.set(x, 0, z); furn.add(g);
      if (lying) KIT.bench(g, { w: 1.6 }); else if (seated) { const st = new THREE.Group(); st.position.z = act === 'row' ? -.05 : 0; g.add(st); KIT.stool(st); }
      const h = crowd.add(rosterSpec(people[(POSES.indexOf(pose) * 7) % people.length]));
      const el = document.createElement('div'); el.textContent = NAMES[pose] || pose;
      el.style.cssText = 'position:absolute;transform:translate(-50%,-100%);font-size:12px;padding:2px 7px;border-radius:999px;background:rgba(13,21,33,.72);color:#e8eef0;white-space:nowrap';
      labels.appendChild(el);
      return { pose, h, el, x, z, y: lying ? .5 : seated ? seatH : 0, face: lying ? Math.PI / 2 : 0 };
    });
  }
  function clear() {
    for (const e of here) crowd.remove(e.h); here = [];
    if (furn) { scene.remove(furn); furn.traverse(o => { if (o.isMesh) o.geometry.dispose(); }); furn = null; }
    if (labels) { labels.remove(); labels = null; }
  }
  return {
    tick(dt, t) {
      if (!started) {
        started = true;
        if (deckDef.num !== 3) goToDeck(3);
        setShipNow((SHIP.time.day - 1) * 1440 + 10 * 60 + 30); nightT = nightAt(); updateClock();
        const c = cellPos(27, 11); player.obj.position.copy(c); player.face = player.obj.rotation.y = 0; target.copy(c).setY(.7);
        toast('Pose lineup', 'Every pose and activity the crew can show, in two rows along the promenade. Walk along them, rotate and zoom. This lineup doesn\'t touch your save.');
      }
      const on = deckDef.num === 3;
      if (on && !here.length) fill(); else if (!on && here.length) clear();
      for (const e of here) {
        e.h.set({ x: e.x, y: e.y, z: e.z }, e.face, e.pose, /^(walk|crouch)/.test(e.pose) ? t * 1.1 : undefined);   // walking in place
        v.set(e.x, 1.85, e.z).project(camera);
        const vis = v.z < 1 && Math.abs(v.x) < 1.1 && Math.abs(v.y) < 1.1;
        e.el.style.display = vis ? '' : 'none';
        if (vis) { e.el.style.left = ((v.x + 1) / 2 * innerWidth).toFixed(0) + 'px'; e.el.style.top = ((1 - v.y) / 2 * innerHeight).toFixed(0) + 'px'; }
      }
    },
  };
})();

// ---- the rec moves lineup (0.81.0, the rec deck animation engineer): ?recposes in the address goes to the rec deck at
// 10:30 and shows every rec pose on the concourse in rec kit, labelled, with a swimmer, a kayaker, a climber and a
// floater going round on stand-in water and wall (the movers, 8c). A test spot only: never saves; remove with the rooms' own. ----
const REC_DEMO = (() => {
  if (!REC_DECK || urlFlag('recposes') === null) return null;   // dev only, and never while the rec deck is dormant
  const STILL = [['tread', .9], ['kayak', .45], ['climb', .7], ['ring', 1.1], ['lower', .8], ['float', 1.0], ['sit:cheer', .48], ['sit:clap', .48], ['sit:groan', .48], ['walk+towel', 0], ['stand', 0], ['stand', 0, 'grip socks']];
  const MOVES = [{ kind: 'swim', path: [[5.6, 9.6], [15.4, 9.6]], y: .35 }, { kind: 'kayak', path: [[24.4, 7.9], [28.6, 7.9, 1], [28.6, 10.1], [24.4, 10.1]], y: .35 },
    { kind: 'climb', at: [4.35, 8.5], face: 'w', top: 2.3 }, { kind: 'float', at: [11.5, 8.4], r: .5, top: 1.4 }];
  let here = [], furn = null, labels = null, started = false;
  const v = new THREE.Vector3();
  function fill() {
    const people = ROSTER.filter(p => !p.story);
    furn = new THREE.Group(); scene.add(furn);
    const water = new THREE.MeshStandardMaterial({ color: col('#3fb6c4'), roughness: .3 }), rock = new THREE.MeshStandardMaterial({ color: col('#b0703c'), roughness: .9 });
    const slab = (m, x0, x1, z0, z1, y0, y1) => { const b = new THREE.Mesh(new THREE.BoxGeometry(x1 - x0, y1 - y0, z1 - z0), m); b.position.set((x0 + x1) / 2 - OX, (y0 + y1) / 2, (z0 + z1) / 2 - OZ); furn.add(b); };
    slab(water, 4.8, 16.2, 9.15, 10.05, .012, .35); slab(water, 23.6, 29.4, 7.3, 10.7, .012, .35); slab(rock, 4.03, 4.13, 7.9, 9.1, .012, 3.4);
    labels = document.createElement('div'); labels.style.cssText = 'position:fixed;inset:0;pointer-events:none;z-index:2';
    document.body.appendChild(labels);
    const label = t => { const el = document.createElement('div'); el.textContent = t; el.style.cssText = 'position:absolute;transform:translate(-50%,-100%);font-size:12px;padding:2px 7px;border-radius:999px;background:rgba(13,21,33,.72);color:#e8eef0;white-space:nowrap'; labels.appendChild(el); return el; };
    here = STILL.map(([pose, y, name], i) => {
      const x = 5.6 + i * .95 - OX, z = 7.55 - OZ;
      if (/^sit/.test(pose)) { const g = new THREE.Group(); g.position.set(x, 0, z); furn.add(g); KIT.stool(g); }
      const h = crowd.add({ ...rosterSpec(people[(i * 7) % people.length]), kit: 'rec', socks: !!name || pose === 'float' });
      if (pose === 'float') h.rig.star = .8;
      return { pose, h, el: label(name || pose), x, y, z, face: 0 };
    }).concat(MOVES.map((M, i) => {
      const h = crowd.add({ ...rosterSpec(people[(i * 11 + 3) % people.length]), kit: 'rec', socks: M.kind === 'float' }), p = recXZ(M.path ? M.path[0] : M.at);
      return { A: { o: { move: M }, def: { mins: 1e9 }, done: 0, x: p.x, z: p.z, y: 0, face: 0, body: h }, h, el: label(M.kind) };
    }));
  }
  function clear() {
    for (const e of here) crowd.remove(e.h); here = [];
    if (furn) { scene.remove(furn); furn.traverse(o => { if (o.isMesh) o.geometry.dispose(); }); furn = null; }
    if (labels) { labels.remove(); labels = null; }
  }
  return {
    tick(dt, t) {
      if (!started) {
        started = true;
        if (deckDef.num !== 7) goToDeck(7);
        setShipNow((SHIP.time.day - 1) * 1440 + 10 * 60 + 30); nightT = nightAt(); updateClock();
        const c = cellPos(11, 10); player.obj.position.copy(c); player.face = player.obj.rotation.y = Math.PI; target.copy(c).setY(.7);
        toast('Rec moves', 'Every rec deck pose, in rec kit along the concourse, with a swimmer, a kayaker, a climber and a floater on stand-in water. Doesn\'t touch your save.');
      }
      const on = deckDef.num === 7;
      if (on && !here.length) fill(); else if (!on && here.length) clear();
      for (const e of here) {
        let x, y, z;
        if (e.A) {
          const A = e.A; if (A.mv && A.mv.done) A.mv = null;
          const pose = recMoveStep(A, dt, t) || 'stand'; e.h.set({ x: A.x, y: A.y, z: A.z }, A.face, pose); x = A.x; y = A.y; z = A.z;
        } else { e.h.set({ x: e.x, y: e.y, z: e.z }, e.face, e.pose, /^walk/.test(e.pose) ? t * 1.1 : undefined); x = e.x; y = e.y; z = e.z; }
        v.set(x, y + 1.9, z).project(camera);
        const vis = v.z < 1 && Math.abs(v.x) < 1.1 && Math.abs(v.y) < 1.1;
        e.el.style.display = vis ? '' : 'none';
        if (vis) { e.el.style.left = ((v.x + 1) / 2 * innerWidth).toFixed(0) + 'px'; e.el.style.top = ((1 - v.y) / 2 * innerHeight).toFixed(0) + 'px'; }
      }
    },
  };
})();

// ---- seat check (0.27.11): ?seats in the address puts a stand-in on every seat place of the deck you're on (pose
// 'sit', at placeSpot's spot, height and facing, exactly where the crew would sit), labelled with the place's id, at
// 10:30 when most of the crew are at work (seats with crew on them show two people). For checking place data (xy, y, face) against the furniture. Never saves. ----
const SEAT_DEMO = (() => {
  if (urlFlag('seats') === null) return null;
  let here = [], labels = null, deck = null, started = false;
  const v = new THREE.Vector3();
  function clear() { for (const e of here) crowd.remove(e.h); here = []; if (labels) { labels.remove(); labels = null; } }
  return {
    tick(dt, t) {
      if (!started) { started = true; setShipNow((SHIP.time.day - 1) * 1440 + 10 * 60 + 30); nightT = nightAt(); updateClock(); toast('Seat check', 'Everyone sits where the crew would, on every seat on this deck, labelled with its place. Take the lift to check another deck. This doesn\'t touch your save.'); }
      if (deckDef.num !== deck && typeof placeSpot === 'function') {
        clear(); deck = deckDef.num;
        labels = document.createElement('div'); labels.style.cssText = 'position:fixed;inset:0;pointer-events:none;z-index:2'; document.body.appendChild(labels);
        const people = ROSTER.filter(p => !p.story);
        here = (deckDef.places || []).filter(p => p.pose === 'sit').map((p, i) => {
          const sp = placeSpot(p.id), h = crowd.add(rosterSpec(people[(i * 7) % people.length]));
          const el = document.createElement('div'); el.textContent = p.id;
          el.style.cssText = 'position:absolute;transform:translate(-50%,-100%);font-size:10px;padding:1px 5px;border-radius:999px;background:rgba(13,21,33,.72);color:#e8eef0;white-space:nowrap';
          labels.appendChild(el); return { sp, h, el };
        });
      }
      for (const e of here) {
        e.h.set({ x: e.sp.x, y: e.sp.y, z: e.sp.z }, e.sp.face, 'sit');
        v.set(e.sp.x, 1.5, e.sp.z).project(camera);
        const vis = v.z < 1 && Math.abs(v.x) < 1.05 && Math.abs(v.y) < 1.05 && camera.zoom > 1.2;
        e.el.style.display = vis ? '' : 'none';
        if (vis) { e.el.style.left = ((v.x + 1) / 2 * innerWidth).toFixed(0) + 'px'; e.el.style.top = ((1 - v.y) / 2 * innerHeight).toFixed(0) + 'px'; }
      }
    },
  };
})();

// ---- crowd demo: ?crowd=40 in the address (any number up to 76, or up to 151 for a ship-wide event) puts that many of the real crew in Deck 3 at dinner,
// and starts you there by the lift at 18:30. The demo never touches your save: ?crowd works as ?nosave does (section 13).
// Who: ROSTER (section 9) through rosterSpec, leaving out Rina and Brennan, who are already on Deck 3 as full rigs.
// Where: Deck 3's own places, in this order: the servery queue, the grab shelf, two galley stations, three people
// walking the mess hall aisles, the 44 mess seats (shuffled), then the 22 benches; past 76 (0.27.8), the lounge seats, the
// garden, the gym and the store, doing what's done there, and some crew twice. Over 70, the far ones go coarse
// (CROWD_MANY). Without the flag none of this exists. ----
const CROWD_DEMO = (() => {
  const m = /^(\d+)$/.exec(urlFlag('crowd') || ''); if (!m) return null;   // ?crowd=40 or #crowd-40
  const want = Math.min(+m[1], 151);
  let sd = 4242; const rnd = () => (sd = (sd * 16807) % 2147483647) / 2147483647;
  const shuffle = a => { for (let i = 0; i < a.length; i++) { const j = i + Math.floor(rnd() * (a.length - i)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
  // real crew, day shift first; read when the demo starts, since the roster is defined after this section
  const looks = () => shuffle(ROSTER.filter(p => !['rina', 'brennan'].includes(p.id)))
    .sort((a, b) => (a.shift === 'night') - (b.shift === 'night')).map(rosterSpec);
  const FACE = { s: 0, n: Math.PI, e: Math.PI / 2, w: -Math.PI / 2 };
  const SEAT_Y = { 'mess-seat': .475, bench: .48 };      // seat tops (the round tables' chairs are .495)
  function spots() {
    const P = DECKS[3].places || [], of = (t, n) => P.filter(p => p.type === t).slice(0, n);
    const b = ROOM_BOX.M, rounds = [[2.0, 6.9], [5.2, 6.9], [8.4, 6.9]].map(([x, z]) => [b.i0 + x, b.j0 + z]);   // round tables, in tiles
    const at = p => {
      const [x, z] = p.xy || [p.at[0] + .5, p.at[1] + .5];
      let face = FACE[p.face] || 0, y = SEAT_Y[p.type] || 0;
      const r = p.type === 'mess-seat' && rounds.find(([cx, cz]) => Math.hypot(cx - x, cz - z) < 1.1);
      if (r) { face = Math.atan2(r[0] - x, r[1] - z); y = .495; }   // a round table's chair faces the table, not a compass point
      return { x: x - OX, z: z - OZ, face, pose: p.pose, y };
    };
    return [...of('servery-queue'), ...of('grab-shelf'), ...of('work:galley', 2)].map(at)
      .concat([0, 1, 2].map(i => ({ loop: i / 3, pose: 'walk' })))
      .concat(shuffle(of('mess-seat').map(at)), of('bench').map(at))
      .concat(['lounge-seat', 'garden', 'gym', 'shop'].flatMap(t => of(t, 99)).map(p => ({ ...at(p), pose: poseOf(p) })));
  }
  // the walkers' loop round the mess hall's aisles, in room tiles
  const LOOP = [[.5, 2.5], [9.6, 2.5], [9.6, 5.3], [.5, 5.3]];
  function onLoop(u) {
    const b = ROOM_BOX.M, x0 = X0(b.i0), z0 = Z0(b.j0), seg = LOOP.map((p, i) => { const q = LOOP[(i + 1) % LOOP.length]; return Math.hypot(q[0] - p[0], q[1] - p[1]); });
    let d = (u % 1) * seg.reduce((a, b) => a + b, 0);
    for (let i = 0; i < LOOP.length; i++) {
      if (d <= seg[i]) { const p = LOOP[i], q = LOOP[(i + 1) % LOOP.length], k = d / seg[i]; return { x: x0 + L(p[0], q[0], k), z: z0 + L(p[1], q[1], k), face: Math.atan2(q[0] - p[0], q[1] - p[1]) }; }
      d -= seg[i];
    }
  }
  let LOOK = null, here = [], started = false, hud = null, ft = 16.7, last = performance.now();
  return {
    tick(dt, t) {
      if (!started) {                                    // start on Deck 3 at 18:30, by the lift
        started = true; LOOK = looks();
        if (deckDef.num !== 3) goToDeck(3);
        setShipNow((SHIP.time.day - 1) * 1440 + 18 * 60 + 30); nightT = nightAt(); updateClock();
        toast('Crowd demo', `${want} of the crew on Deck 3 at dinner: the mess hall is to the north-east of the lift. The line at the top shows the draw calls and the frame time. This demo doesn't touch your save.`);
        hud = document.createElement('div'); hud.className = 'clock'; document.querySelector('.hud').appendChild(hud);
      }
      const on = deckDef.num === 3;
      if (on && !here.length) {
        here = spots().slice(0, want).map((s, i) => ({ s, h: crowd.add(LOOK[i % LOOK.length]) }));
      } else if (!on && here.length) { for (const e of here) crowd.remove(e.h); here = []; }
      crowd.visible = typeof crewOn === 'undefined' || crewOn;
      for (const e of here) {
        if (e.s.pose === 'walk') { const q = onLoop(e.s.loop + t * .9 / 28); e.h.set({ x: q.x, y: 0, z: q.z }, q.face, 'walk'); }
        else e.h.set({ x: e.s.x, y: e.s.y || 0, z: e.s.z }, e.s.face, e.s.pose);
      }
      const now = performance.now(); ft += (now - last - ft) * .05; last = now;
      if (hud) { const st = crowd.stats(); hud.textContent = `Crowd ${st.people} (${st.coarse} coarse) · ${renderer.info.render.calls} draw calls · ${(st.tris / 1000).toFixed(0)}k triangles · ${ft.toFixed(1)} ms a frame`; }
    },
  };
})();

