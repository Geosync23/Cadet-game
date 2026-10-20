// =====================================================================
// 4. DECK: art kit, deck builder, deck definitions
// A deck is data in DECKS: its tile map, rooms, doors, hull, windows, and a
// dress() that furnishes it. buildDeck(def) makes one of them the current
// deck. Walls sit on the edges between different rooms, furniture is placed
// per room in room-local units, and everything static is merged into a
// handful of meshes at the end.
//   4a  the current deck: state that buildDeck() fills, and helpers that read it
//   4b  shared kit: materials, textures, furniture, templates (made once)
//   4c  buildDeck()
//   4d  deck definitions
// =====================================================================

// =====================================================================
// THE SHIP: state that outlives any one deck. A deck is rebuilt from its
// definition plus this, so leaving a deck loses nothing. Per deck for now:
// doors that have been unlocked. Machines, supplies and wear join in step 7.
// =====================================================================
const SHIP = { decks: {} };
const shipDeck = n => SHIP.decks[n] || (SHIP.decks[n] = { open: new Set() });
// the rec deck (0.80.0, plans/recdeck-plan.html section 11): internal key 7, shown as R, between Decks 4 and 5. Lists that show
// or loop over decks for the player go in DECK_ORDER; a deck's name on screen comes from deckWord (never "Deck 7")
// REC_DECK (0.82.7, the user's order via lead 14): the one switch for the rec deck. false keeps it dormant: no R on the lift
// or in Maps, goToDeck(7) does nothing, a save left on it wakes on Deck 4; DECKS[7] is playerOnly, so nothing else changes
const REC_DECK = true;                                   // 0.63.2r: merged dormant (the user's, via lead 15); 0.84.11 (rec engineer B2, the brief's last step): switched on, open from Day 1
const DECK_ORDER = REC_DECK ? [1, 2, 3, 4, 7, 5, 6] : [1, 2, 3, 4, 5, 6];
// 0.84.8: the auditorium's show (section 8c's recShow); here so the deck's build can read them
const REC_POOLS = [[8.85, 7.3, .95], [9.35, 9.6, 1.25], [9.1, 11.6, 1.0]];   // the stage's light pools [x, z, radius], the auditorium's coordinates
const REC_SHOWS = {
  film: { dim: .62, scr: 1, pools: [0, 0, 0] }, talk: { dim: .3, scr: 0, pools: [1, .25, 0] },
  allhands: { dim: .28, scr: 0, pools: [1, .5, 0] }, talent: { dim: .5, scr: 0, pools: [.45, 1, .8] },
};
const REC_SHOW = { state: null, dim: 0, scr: 0, piv: null, pools: null, ring: null, mic: null };
const deckLabel = n => +n === 7 ? 'R' : String(n);
const deckWord = n => +n === 7 ? 'Rec deck' : 'Deck ' + n;
const deckIn = n => +n === 7 ? 'the rec deck' : 'Deck ' + n;   // 0.84.2 (lead 18): a deck's name mid-sentence ("on the rec deck"); deckWord for labels and signs

// =====================================================================
// 4a. THE CURRENT DECK
// Everything in this block belongs to the deck you are on. buildDeck()
// replaces all of it, so nothing here may be kept between decks.
// =====================================================================
// The ship frame: every deck is placed so its lift car's centre (def.lift, in tile units) sits here.
// That keeps the spine lined up from deck to deck. It's Deck 4's lift, left where it always was.
const LIFT_AT = [-4, 0];
let deckDef = null, deckRoot = null;          // the deck's definition, and the group that holds all of its 3D
let deckMark = null;                          // id watermarks taken as the deck began building (see unloadDeck)
let ROOMS = {}, DOORS = {}, CLOSED_DOORS = {}, WINDOWS = [], HULL = null;
let MAP = [], STAND = new Set(), ROOM_BOX = {}, EDGES = new Map();
let HULL_PTS = [], HULL_SEGS = [], HULL_NRM = [];
let floor = null, edgeList = [], wallEdges = [], frameEdges = [], wallIM = null, hdrIM = null;
let POSTS = [], RUNS = [], fullPosts = [], hdrPosts = [], postIM = null, hpostIM = null;
let DOOR_OBJS = [], HULL_RUNS = [], HULL_MESHES = [], VOID_BLOCKS = [], DOOR_LEAVES = [];
const _leafM = new THREE.Matrix4(), _leafS = new THREE.Matrix4(), LEAF_HIDE = new THREE.Matrix4().makeScale(0, 0, 0);
function doorLeavesSync() {                              // each frame, before the render: the leaves where the doors put them
  for (const d of DOOR_OBJS) d.g.updateMatrixWorld(true);
  for (const { im, list } of DOOR_LEAVES) {
    list.forEach((l, k) => im.setMatrixAt(k, l.visible ? _leafM.multiplyMatrices(l.matrixWorld, _leafS.makeScale(l.userData.leaf.sx, 1, 1)) : LEAF_HIDE));
    im.instanceMatrix.needsUpdate = true;
  }
}
let staticRoot = null, BLOCKED = new Set(), ITEMS = [], WALL_DECOR = [], SPOTS = [];
let TALL = [], TALL_BY_ROOM = {}, NO_FADE = new Set();   // tall furniture fades a room at a time; locked rooms stay solid
let LAMPS = [], STEAM = [], DUST = [], SPINS = [];   // SPINS: parts that turn (fan rotors, gears): { o, ax, w }
let MOVERS = [];                                       // parts that move only while their place is in use (Pillar 2): { place, tick(dt, on) }
let PULSES = [];                                       // glow that breathes (drive coils): { m, key, base, amp, w, ph }, m[key] = base + amp * (0..1)

// =====================================================================
// HULL: the deck's outline in tile units (x 0..W, z 0..D). Flat port and
// starboard sides run along the top and bottom of the map; the stern is
// flat with rounded corners and the bow is rounded. The hull wall, windows,
// floor, slab and collision all follow it. Tiles the hull cuts off entirely
// drop out of the map; tiles it only clips keep their room, and their floor
// is trimmed to the curve.
// =====================================================================
const hullL = z => { const d = Math.min(z, D - z), r = HULL.stern; return HULL.sternX + (d < r ? r - Math.sqrt(Math.max(0, r * r - (r - d) ** 2)) : 0); };
const hullR = z => { const v = (z - D / 2) / (D / 2); return HULL.bowFrom + HULL.bowLen * Math.sqrt(Math.max(0, 1 - v * v)); };
const inHull = (x, z) => z > 0 && z < D && x > hullL(z) && x < hullR(z);
// signed distance from the hull line, positive inside (the hull is convex, so the nearest side wins)
function hullDist(x, z) {
  let best = 1e9;
  for (const s of HULL_SEGS) {
    const t = Math.max(0, Math.min(1, ((x - s.ax) * s.dx + (z - s.az) * s.dz) / s.l2));
    best = Math.min(best, Math.hypot(x - s.ax - s.dx * t, z - s.az - s.dz * t));
  }
  return inHull(x, z) ? best : -best;
}
const tileInHull = (i, j) => [[.15, .15], [.85, .15], [.15, .85], [.85, .85]].some(([a, b]) => inHull(i + a, j + b));
const roomAt = (i, j) => (i < 0 || j < 0 || i >= W || j >= D || MAP[j][i] === '.') ? null : MAP[j][i];
const isVoid = (i, j) => { const r = roomAt(i, j); return !r || !!ROOMS[r].void || !STAND.has(i + ',' + j); };
const X0 = i => i - OX, Z0 = j => j - OZ;               // world position of tile edges
// is every door into this room shut? Locked rooms keep their furniture solid (and cheap)
function roomLocked(rk) {
  for (const [key, type] of Object.entries(DOORS)) {
    if (type === 'closed' || type === 'hatch') continue;
    const [k, a, b] = key.split(','), i = +a, j = +b;
    if ((k === 'h' ? [roomAt(i, j - 1), roomAt(i, j)] : [roomAt(i - 1, j), roomAt(i, j)]).includes(rk)) return false;
  }
  return true;
}
// who: the player (or a crew member) a path or a collision is for; a service hatch is open only to those it lets through
// 0.47.11 (Pillar 5 Step 3, for the career seat C2): doors shut to you, and only you, until something lets you in. YOU_LOCKS[deck]:
// [{ keys, open(key), tap(key) }]. Deck 1's bridge doors ask C2's bridgeBarred(edge) (section 20: not invited, no appointment, not
// already inside); without it, a bridgeInvitedNow() if defined; with neither they
// are open, as before (h,14,10: the floor hatch up from the sub-floor crawl, the back way in). A locked one blocks your walking and your paths (edgeBlocks), doesn't slide open as you come up to it, and
// a tap on it says why (youLockTap(key) -> { t, x }; the line is W2's `bridge.permission` when it's baked). The crew pass as ever
const YOU_LOCKS = { 1: [{ keys: ['v,10,5', 'v,10,6', 'h,14,10'], open: key => typeof bridgeBarred === 'function' ? !bridgeBarred(EDGES.get(key)) : (typeof bridgeInvitedNow !== 'function' || !!bridgeInvitedNow()),   // 0.47.12: C2's rule (section 20) when it's there
  tap: key => { let r = null; try { r = typeof bridgeDoorTap === 'function' ? bridgeDoorTap(key) : null; } catch (e) { r = null; } if (r) return r;   // C2's words first (section 20)
    let x = null; try { x = typeof careerText === 'function' && careerText('bridge.permission'); } catch (e) { x = null; } return { t: 'Bridge', x: x || 'The bridge is for the watch on duty. You\'ll need an invitation before you can go in.' }; } }] };
function youLock(key, who) {
  if (!who || !(who === 'player' || who.isPlayer || (typeof player !== 'undefined' && who === player)) || !deckDef) return null;
  const L = YOU_LOCKS[deckDef.num]; if (!L) return null;
  for (let k = 0; k < L.length; k++) if (L[k].keys.includes(key) && !L[k].open(key)) return L[k];
  return null;
}
const youLockTap = key => { const L = youLock(key, 'player'); return L ? L.tap(key) : null; };
const edgeBlocks = (e, who) => e && (!!youLock(e.key, who) || e.type !== 'door' && e.type !== 'open' && e.type !== 'lift' && !(e.service && hatchPassable(e.key, who))
  && !(e.type === 'closed' && who && typeof doorOpenFor === 'function' && (e.horiz ? [[e.i, e.j - 1], [e.i, e.j]] : [[e.i - 1, e.j], [e.i, e.j]]).some(c => doorOpenFor(roomAt(...c), who))));   // section 14: invited in
// Service hatches (Pillar 2): a deck lists in `service` the hatches into utility rooms whose insides are built.
// The player and Works crew pass them; everyone else, and every other hatch (the spine ladder's), treats them as walls.
// crewPath (section 10) asks this for each person. Tier locks (answer 4): a hatch with a `tier` lets through only
// those of that tier or more (hatchTier, section 17: Works crew by rank). The player passes them all (0.27.35).
function hatchPassable(key, who) {
  const e = EDGES.get(key); if (!e || !e.service || !who) return false;
  if (who === 'player' || who.isPlayer) return true;   // 0.27.35, the user: you can enter any utility space from the start (job tiers are still progression)
  if (e.tier > 1 && typeof hatchTier === 'function' && hatchTier(who) < e.tier) return false;
  return (who.p || who).dept === 'works';
}
// the corner between two lift edges in a line: the middle of one wide lift doorway
const liftJoint = touch => touch.length === 2 && touch.every(t => t.type === 'lift') && touch[0].horiz === touch[1].horiz;
const wallE = key => { const e = EDGES.get(key); return e && e.type !== 'hull' ? e : null; };   // inner walls only
function addEdge(key, horiz, i, j, a, b) {
  if (a === b) return;
  const va = !a || ROOMS[a].void, vb = !b || ROOMS[b].void;
  if (va && vb) return;                                  // nothing to see between solid areas
  const onHull = !a || !b || !inHull(horiz ? i + .5 : i, horiz ? j : j + .5);   // the hull ribbon draws these
  const type = onHull ? 'hull' : (DOORS[key] || (ROOMS[a].hall && ROOMS[b].hall ? 'open' : 'wall'));
  EDGES.set(key, { key, horiz, i, j, type, cx: horiz ? X0(i) + .5 : X0(i), cz: horiz ? Z0(j) : Z0(j) + .5, s: 1, hull: !a || !b,
    out: !a ? (horiz ? [0, -1] : [-1, 0]) : (!b ? (horiz ? [0, 1] : [1, 0]) : null), decor: [] });
}
// the hull outline pushed out by a distance (the floor runs under the hull wall, the slab a little past it)
const HULL_OUT = .45;                                     // the hull wall's outer face sits this far outside the line
const hullRing = off => HULL_PTS.map(([x, z], k) => [x + HULL_NRM[k].nx * off * HULL_NRM[k].m, z + HULL_NRM[k].nz * off * HULL_NRM[k].m]);
const junction = (i, j, horiz) => horiz ? !!(wallE(`v,${i},${j - 1}`) || wallE(`v,${i},${j}`)) : !!(wallE(`h,${i - 1},${j}`) || wallE(`h,${i},${j}`));
function finishRun(r) {
  r.cx = r.edges.reduce((a, e) => a + e.cx, 0) / r.edges.length; r.cz = r.edges.reduce((a, e) => a + e.cz, 0) / r.edges.length;
  r.cut = false; RUNS.push(r);
}
// ---- curved inner walls (0.6.4): smooth walls and counters drawn over the tile grid, the way the hull is.
// A deck lists them in `curves`. Each has an arc, [cx, cz, r, a0, a1] in tiles and degrees (0 points to the bow,
// 90 to starboard), or pts, [[x, z], ...] in tiles (a smooth line through them), and a kind:
//   wall: a full-height wall that drops with the cutaway like any inner wall
//   glass: a planter base with a curved glass screen and a rail on top
//   bar: a counter, with its foot rail and under-glow on the side named by out (1 is the arc's outside)
//   planter: a low planter wall, planted along its top
// Tiles whose centres lie close to the line are blocked, and walkers are pushed off the line itself.
let CURVES = [], CURVE_SEGS = [];
let SNUG = new Map();                                    // tile -> the true footprint of a snug piece on it: paths still avoid the tile, but you can walk right up to the piece
const curveWallMat = (() => { const t = wallTex.clone(); t.wrapS = THREE.RepeatWrapping; t.needsUpdate = true; return new THREE.MeshStandardMaterial({ map: t, roughness: .85, metalness: .05 }); })();
const CURVE_MAT = {
  planter: std('#4a3a2e', .7), soil: std('#2c2219', 1), leaf: [std('#4c8a57', .7), std('#6ba86a', .7), std('#3f7a4f', .7)],
  bar: std('#4a2e22', .55, .05), brass: std('#c9a24a', .35, .75), glow: std('#ffcf8a', .4, 0, { emissive: col('#ffb45a'), emissiveIntensity: 1.3 }),
  screen: std('#cfe8ee', .08, 0, { transparent: true, opacity: .18, depthWrite: false, side: THREE.DoubleSide }),
};
function curvePoints(c) {
  let P = [];
  if (c.arc) {
    const [cx, cz, r, a0, a1] = c.arc, n = Math.max(6, Math.ceil(Math.abs(a1 - a0) / 5));
    for (let k = 0; k <= n; k++) { const a = (a0 + (a1 - a0) * k / n) * Math.PI / 180; P.push([cx + Math.cos(a) * r, cz + Math.sin(a) * r]); }
  } else {
    const p = c.pts, at = k => p[Math.max(0, Math.min(p.length - 1, k))];
    for (let k = 0; k < p.length - 1; k++) for (let u = 0; u < 8; u++) {      // Catmull-Rom through the points
      const t = u / 8, [a, b, d, e] = [at(k - 1), at(k), at(k + 1), at(k + 2)], f = q => .5 * (2 * b[q] + (-a[q] + d[q]) * t + (2 * a[q] - 5 * b[q] + 4 * d[q] - e[q]) * t * t + (-a[q] + 3 * b[q] - 3 * d[q] + e[q]) * t * t * t);
      P.push([f(0), f(1)]);
    }
    P.push(p[p.length - 1]);
  }
  return P.map(([x, z]) => [x - OX, z - OZ]);
}
// a strip along the line P from height y0 to y1, between offsets o0 < o1 (along the left normal): two faces, a top and end caps
function curveStrip(P, y0, y1, o0, o1, mats) {
  const n = P.map((p, k) => { const a = P[Math.max(0, k - 1)], b = P[Math.min(P.length - 1, k + 1)], l = Math.hypot(b[0] - a[0], b[1] - a[1]) || 1; return [-(b[1] - a[1]) / l, (b[0] - a[0]) / l]; });
  const pos = [], uv = [], groups = [[], [], []];
  const quad = (g, A, B, C, Dd, nrm, uvs) => {                         // corners in order round the quad; wound to face nrm
    const ux = B[0] - A[0], uy = B[1] - A[1], uz = B[2] - A[2], vx = Dd[0] - A[0], vy = Dd[1] - A[1], vz = Dd[2] - A[2];
    const cx = uy * vz - uz * vy, cy = uz * vx - ux * vz, cz = ux * vy - uy * vx;
    let v = [A, B, C, A, C, Dd], t = [uvs[0], uvs[1], uvs[2], uvs[0], uvs[2], uvs[3]];
    if (cx * nrm[0] + cy * nrm[1] + cz * nrm[2] < 0) { v = [A, C, B, A, Dd, C]; t = [uvs[0], uvs[2], uvs[1], uvs[0], uvs[3], uvs[2]]; }
    groups[g].push(...v.map((q, k) => [q, t[k]]));
  };
  let arc = 0;
  for (let k = 0; k < P.length - 1; k++) {
    const [ax, az] = P[k], [bx, bz] = P[k + 1], na = n[k], nb = n[k + 1], l = Math.hypot(bx - ax, bz - az), mid = [(na[0] + nb[0]) / 2, 0, (na[1] + nb[1]) / 2];
    const pt = (x, z, nn, o, y) => [x + nn[0] * o, y, z + nn[1] * o];
    const u0 = arc / SEG, u1 = (arc + l) / SEG, v0 = y0 / H, v1 = y1 / H;
    quad(0, pt(ax, az, na, o0, y0), pt(bx, bz, nb, o0, y0), pt(bx, bz, nb, o0, y1), pt(ax, az, na, o0, y1), [-mid[0], 0, -mid[2]], [[u0, v0], [u1, v0], [u1, v1], [u0, v1]]);
    quad(1, pt(ax, az, na, o1, y0), pt(bx, bz, nb, o1, y0), pt(bx, bz, nb, o1, y1), pt(ax, az, na, o1, y1), mid, [[u0, v0], [u1, v0], [u1, v1], [u0, v1]]);
    quad(2, pt(ax, az, na, o0, y1), pt(bx, bz, nb, o0, y1), pt(bx, bz, nb, o1, y1), pt(ax, az, na, o1, y1), [0, 1, 0], [[0, 0], [1, 0], [1, 1], [0, 1]]);
    arc += l;
  }
  for (const [k, sg] of [[0, -1], [P.length - 1, 1]]) {                      // end caps
    const [x, z] = P[k], nn = n[k], j = sg < 0 ? 1 : P.length - 2, d = [P[k][0] - P[j][0], 0, P[k][1] - P[j][1]];
    const c = (o, y) => [x + nn[0] * o, y, z + nn[1] * o];
    quad(2, c(o0, y0), c(o1, y0), c(o1, y1), c(o0, y1), d, [[0, 0], [1, 0], [1, 1], [0, 1]]);
  }
  const geo = new THREE.BufferGeometry(), all = [];
  groups.forEach((gr, gi) => { geo.addGroup(all.length, gr.length, gi); all.push(...gr); });
  geo.setAttribute('position', new THREE.Float32BufferAttribute(all.flatMap(q => q[0]), 3));
  geo.setAttribute('uv', new THREE.Float32BufferAttribute(all.flatMap(q => q[1]), 2));
  geo.computeVertexNormals();
  const m = new THREE.Mesh(geo, mats); m.castShadow = m.receiveShadow = true; return m;
}
function buildCurves(def) {
  CURVES = []; CURVE_SEGS = [];
  for (const c0 of def.curves || []) {
    const c = { ...c0, P: curvePoints(c0), g: new THREE.Group(), s: 1 }, P = c.P, out = c.out || 1;
    deckRoot.add(c.g); CURVES.push(c);
    let half = .3;
    if (c.kind === 'wall') {
      half = T / 2;
      c.g.add(curveStrip(P, 0, H, -T / 2, T / 2, [curveWallMat, curveWallMat, capMat]));
      for (const p of [P[0], P[P.length - 1]]) box(T + .02, H, T + .02, capMat, p[0], H / 2, p[1], c.g);
      const edges = []; for (let k = 0; k < P.length; k += 3) edges.push({ cx: P[k][0], cz: P[k][1] });
      c.run = { edges, out: null, curve: c, cut: false }; RUNS.push(c.run);
    } else if (c.kind === 'glass' || c.kind === 'planter') {
      half = .25;
      const hgt = c.kind === 'glass' ? .8 : .7;
      c.g.add(curveStrip(P, 0, hgt, -.25, .25, [CURVE_MAT.planter, CURVE_MAT.planter, CURVE_MAT.soil]));
      for (let k = 1; k < P.length - 1; k += 2) {                            // leaves along the top, in a steady pattern
        const L = CURVE_MAT.leaf[k % 3], sz = .16 + (k % 3) * .05;
        soft(L, P[k][0], hgt + sz * .6, P[k][1], sz, sz * .8, sz, c.g);
      }
      if (c.kind === 'glass') {
        const sc = curveStrip(P, hgt, 2.05, -.015, .015, [CURVE_MAT.screen, CURVE_MAT.screen, CURVE_MAT.screen]); sc.castShadow = false; c.g.add(sc);
        c.g.add(curveStrip(P, 2.05, 2.1, -.04, .04, [CURVE_MAT.brass, CURVE_MAT.brass, CURVE_MAT.brass]));
        for (const p of [P[0], P[P.length - 1]]) cyl(.035, .035, 2.1 - hgt, CURVE_MAT.brass, p[0], (hgt + 2.1) / 2, p[1], c.g, 10);
      }
    } else if (c.kind === 'bar') {
      half = .32;
      const o = out > 0 ? 1 : -1, lo = o > 0 ? -.28 : -.38, hi = o > 0 ? .38 : .28;   // the top overhangs on the customers' side
      c.g.add(curveStrip(P, .06, 1.03, -.28, .28, [CURVE_MAT.bar, CURVE_MAT.bar, CURVE_MAT.bar]));
      c.g.add(curveStrip(P, 1.03, 1.1, lo, hi, [M.wood, M.wood, M.wood]));
      c.g.add(curveStrip(P, 0, .06, -.3, .3, [M.slateDark, M.slateDark, M.slateDark]));
      c.g.add(curveStrip(P, .2, .24, o * .4 - .02, o * .4 + .02, [CURVE_MAT.brass, CURVE_MAT.brass, CURVE_MAT.brass]));   // foot rail
      const gl = curveStrip(P, .06, .1, o * .29 - .01, o * .29 + .01, [CURVE_MAT.glow, CURVE_MAT.glow, CURVE_MAT.glow]); gl.castShadow = false; c.g.add(gl);
    }
    // the line blocks walking
    for (let k = 0; k < P.length - 1; k++) CURVE_SEGS.push({ ax: P[k][0], az: P[k][1], bx: P[k + 1][0], bz: P[k + 1][1], h: half });
    const xs = P.map(p => p[0]), zs = P.map(p => p[1]);
    for (let j = Math.floor(Math.min(...zs) + OZ) - 1; j <= Math.floor(Math.max(...zs) + OZ) + 1; j++)
      for (let i = Math.floor(Math.min(...xs) + OX) - 1; i <= Math.floor(Math.max(...xs) + OX) + 1; i++) {
        if (curveDist(X0(i) + .5, Z0(j) + .5, c) < half + .3) BLOCKED.add(i + ',' + j);
      }
    if (c.it) {                                                              // tappable at its middle, from the side named by out
      const k = Math.floor(P.length / 2), a = P[Math.max(0, k - 1)], b = P[Math.min(P.length - 1, k + 1)], l = Math.hypot(b[0] - a[0], b[1] - a[1]) || 1;
      const nx = -(b[1] - a[1]) / l * out, nz = (b[0] - a[0]) / l * out, hg = new THREE.Group();
      hg.position.set(P[k][0], 0, P[k][1]); hg.rotation.y = Math.atan2(nx, nz); deckRoot.add(hg);
      const hit = new THREE.Mesh(new THREE.BoxGeometry(1.4, 1.2, half * 2 + .1), HIT_MAT); hit.position.y = .6; hit.userData.noMerge = true; hg.add(hit);
      ITEMS.push({ ...c.it, hit, g: hg, front: hg.rotation.y, depth: half * 2 });
    }
  }
}
function curveDist(x, z, c) {
  let best = 1e9;
  for (let k = 0; k < c.P.length - 1; k++) {
    const [ax, az] = c.P[k], [bx, bz] = c.P[k + 1], dx = bx - ax, dz = bz - az, l2 = dx * dx + dz * dz || 1e-9;
    const t = THREE.MathUtils.clamp(((x - ax) * dx + (z - az) * dz) / l2, 0, 1);
    best = Math.min(best, Math.hypot(x - ax - dx * t, z - az - dz * t));
  }
  return best;
}
// build a vertical strip along outline points idx (wrapping), from height y0 to y1, between two offsets from the line
function hullStrip(idx, y0, y1, offIn, offOut, mats, o = {}) {
  const P = [], N = [], U = [], groups = [[], [], []];   // 0 inner face, 1 outer face, 2 caps
  const pt = (k, off) => { const [x, z] = HULL_PTS[k], n = HULL_NRM[k]; return [x + n.nx * off * n.m - OX, z + n.nz * off * n.m - OZ]; };
  const quad = (g, v, nrm, uv) => {                       // v: 4 corners [x,y,z], wound to face nrm
    const e1 = [v[1][0] - v[0][0], v[1][1] - v[0][1], v[1][2] - v[0][2]], e2 = [v[2][0] - v[0][0], v[2][1] - v[0][1], v[2][2] - v[0][2]];
    const cx = e1[1] * e2[2] - e1[2] * e2[1], cy = e1[2] * e2[0] - e1[0] * e2[2], cz = e1[0] * e2[1] - e1[1] * e2[0];
    const flip = cx * nrm[0][0] + cy * nrm[0][1] + cz * nrm[0][2] < 0, order = flip ? [0, 2, 1, 0, 3, 2] : [0, 1, 2, 0, 2, 3];
    for (const q of order) groups[g].push([...v[q], ...nrm[q], ...uv[q]]);
  };
  let arc = o.arc0 || 0;
  for (let n = 0; n < idx.length - 1; n++) {
    const a = idx[n], b = idx[n + 1], ai = pt(a, offIn), bi = pt(b, offIn), ao = pt(a, offOut), bo = pt(b, offOut);
    const na = [HULL_NRM[a].nx, 0, HULL_NRM[a].nz], nb = [HULL_NRM[b].nx, 0, HULL_NRM[b].nz], len = HULL_SEGS[a].l, u0 = arc, u1 = arc + len;
    quad(0, [[ai[0], y0, ai[1]], [bi[0], y0, bi[1]], [bi[0], y1, bi[1]], [ai[0], y1, ai[1]]], [na, nb, nb, na], [[u0, y0 / H], [u1, y0 / H], [u1, y1 / H], [u0, y1 / H]]);
    const neg = v => v.map(c => -c);
    quad(1, [[ao[0], y0, ao[1]], [bo[0], y0, bo[1]], [bo[0], y1, bo[1]], [ao[0], y1, ao[1]]], [neg(na), neg(nb), neg(nb), neg(na)], [[u0, y0 / H], [u1, y0 / H], [u1, y1 / H], [u0, y1 / H]]);
    const up = [0, 1, 0], dn = [0, -1, 0];
    quad(2, [[ai[0], y1, ai[1]], [bi[0], y1, bi[1]], [bo[0], y1, bo[1]], [ao[0], y1, ao[1]]], [up, up, up, up], [[0, 0], [1, 0], [1, 1], [0, 1]]);
    if (y0 > 0) quad(2, [[ai[0], y0, ai[1]], [bi[0], y0, bi[1]], [bo[0], y0, bo[1]], [ao[0], y0, ao[1]]], [dn, dn, dn, dn], [[0, 0], [1, 0], [1, 1], [0, 1]]);
    arc = u1;
  }
  for (const [k, sgn] of [[idx[0], -1], [idx[idx.length - 1], 1]]) {   // end caps
    const s = HULL_SEGS[k], t = [s.dx / s.l * sgn, 0, s.dz / s.l * sgn], i = pt(k, offIn), q = pt(k, offOut);
    quad(2, [[i[0], y0, i[1]], [q[0], y0, q[1]], [q[0], y1, q[1]], [i[0], y1, i[1]]], [t, t, t, t], [[0, 0], [1, 0], [1, 1], [0, 1]]);
  }
  const geo = new THREE.BufferGeometry(), A = [], Nn = [], Uv = []; let start = 0;
  groups.forEach((g, gi) => { for (const v of g) { A.push(v[0], v[1], v[2]); Nn.push(v[3], v[4], v[5]); Uv.push(v[6], v[7]); } geo.addGroup(start, g.length, gi); start += g.length; });
  geo.setAttribute('position', new THREE.Float32BufferAttribute(A, 3)); geo.setAttribute('normal', new THREE.Float32BufferAttribute(Nn, 3)); geo.setAttribute('uv', new THREE.Float32BufferAttribute(Uv, 2));
  geo.computeBoundingSphere();
  const m = new THREE.Mesh(geo, mats); m.castShadow = o.shadow !== false; m.receiveShadow = true; return m;
}

// =====================================================================
// 4b. SHARED KIT
// Materials, textures and builders every deck uses. Made once, never
// rebuilt, and never disposed with a deck.
// =====================================================================
// ---- shared bits the kit uses ----
const screenMat = new THREE.MeshBasicMaterial({ map: screenTex, toneMapped: false });
const clockMat = new THREE.MeshBasicMaterial({ map: clockTex, toneMapped: false });
const lockerMat = new THREE.MeshStandardMaterial({ map: lockerTex, roughness: .55, metalness: .25 });
const lampShadeMat = std('#2a9d8f', .5, .2, { side: THREE.DoubleSide });
const HIT_MAT = new THREE.MeshBasicMaterial({ visible: false });
const glassMat = new THREE.MeshBasicMaterial({ color: col('#9fd3ff'), transparent: true, opacity: .07, depthWrite: false });

// ---- the sky: two layers of stars over the empty space round the ship, drifting aft as the Wren flies.
// A screen-sized quad just inside the far plane, so stars only show where nothing else has drawn.
// It has its own random sequence, so no kit texture shifts, and it lives in the scene, not a deck.
const SKY = (() => {
  let sd = 4242; const r = () => (sd = (sd * 16807) % 2147483647) / 2147483647;
  const layer = (n, r0, r1, big) => {
    const c = document.createElement('canvas'); c.width = c.height = 512; const g = c.getContext('2d');
    for (let i = 0; i < n; i++) {
      const x = r() * 512, y = r() * 512, rad = r() < big ? r1 : r0 + r() * (r1 - r0) * .5, a = .35 + r() * .65, h = r();
      const rgb = h < .14 ? '255,214,170' : h < .3 ? '186,212,255' : '255,255,255';
      for (const ox of [-512, 0, 512]) for (const oy of [-512, 0, 512]) {   // drawn wrapped, so the tile has no seams
        const gr = g.createRadialGradient(x + ox, y + oy, 0, x + ox, y + oy, rad);
        gr.addColorStop(0, `rgba(${rgb},${a})`); gr.addColorStop(.45, `rgba(${rgb},${a * .55})`); gr.addColorStop(1, `rgba(${rgb},0)`);
        g.fillStyle = gr; g.fillRect(x + ox - rad, y + oy - rad, rad * 2, rad * 2);
      }
    }
    const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.generateMipmaps = false; t.minFilter = THREE.LinearFilter; return t;
  };
  const mat = new THREE.ShaderMaterial({
    uniforms: { tFar: { value: layer(320, 1.1, 1.8, .03) }, tNear: { value: layer(70, 1.6, 2.8, .12) }, uFar: { value: new THREE.Vector2() }, uNear: { value: new THREE.Vector2() }, uPR: { value: 1 }, uK: { value: .8 },
      uWash: { value: 0 }, uT: { value: 0 }, uA: { value: new THREE.Color() }, uB: { value: new THREE.Color() } },   // 0.27.19: an event's mood (section 8b's shipFeelFrame)
    vertexShader: 'void main() { gl_Position = vec4(position.xy, .9999, 1.0); }',
    fragmentShader: `uniform sampler2D tFar, tNear; uniform vec2 uFar, uNear; uniform float uPR, uK, uWash, uT; uniform vec3 uA, uB;
      void main() {
        vec2 p = gl_FragCoord.xy / uPR;
        vec4 a = texture2D(tFar, (p + uFar) / 512.0), b = texture2D(tNear, (p + uNear) / 512.0);
        vec3 c = (a.rgb * a.a * .6 + b.rgb * b.a) * uK;
        if (uWash > 0.0) {                               // slow broad bands of ion light drifting across space
          float w1 = .5 + .5 * sin(p.x * .0042 + p.y * .0061 + uT * .23), w2 = .5 + .5 * sin(p.y * .0053 - p.x * .0021 - uT * .17 + 1.7);
          c = c * mix(vec3(1.0), uA * 1.6 + .45, .35 * min(uWash, 1.0)) + uWash * .75 * (uA * w1 * w1 * w1 + uB * w2 * w2 * w2 * w2);
        }
        gl_FragColor = vec4(c, 1.0);
      }`,
    transparent: true, blending: THREE.AdditiveBlending, depthWrite: false,
  });
  const m = new THREE.Mesh(new THREE.PlaneGeometry(2, 2), mat);
  m.frustumCulled = false; m.renderOrder = 1e6; m.raycast = () => {}; scene.add(m);
  const calm = matchMedia('(prefers-reduced-motion: reduce)').matches;
  return { m, mat, far: new THREE.Vector2(), near: new THREE.Vector2(), speed: calm ? .25 : 1 };
})();
const LAMP_SLOTS = 2;                                    // point lights per deck: the most any deck uses (Deck 4); raise it if a deck needs more
function addLamp(parent, x, y, z, dist, day, night) {
  const l = new THREE.PointLight(0xffc98a, 1, dist, 2); l.position.set(x, y, z); parent.add(l); LAMPS.push({ l, day, night });
}
function addSteam(parent, x, y, z) { for (let i = 0; i < 3; i++) STEAM.push({ s: glow('#ffffff', .12, x, y, z, parent, 0), x, y, i }); }
function makeDust(len) {
  const n = 60, pos = new Float32Array(n * 3), seeds = [];
  for (let i = 0; i < n; i++) { pos[i * 3] = (R() - .5) * len * 1.1; pos[i * 3 + 1] = .4 + R() * 1.9; pos[i * 3 + 2] = .3 + R() * 1.8; seeds.push(R() * 10); }
  const geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  const p = new THREE.Points(geo, new THREE.PointsMaterial({ map: glowTex, size: .05, color: col('#cfe4ff'), transparent: true, opacity: .55, blending: THREE.AdditiveBlending, depthWrite: false }));
  DUST.push({ geo, seeds, n }); return p;
}

// walls, door frames and posts (instanced: a few draw calls for the whole deck)
const capMat = std('#262e35', .8, .1);
const wallMat = new THREE.MeshStandardMaterial({ map: wallTex, roughness: .85, metalness: .05 });
const SEG = 1 - T, HDR = H - 2.2, RAIL_H = .45;
const wallGeo = new THREE.BoxGeometry(SEG, H, T); wallGeo.translate(0, H / 2, 0);
const postGeo = new THREE.BoxGeometry(T, H, T); postGeo.translate(0, H / 2, 0);
const hdrGeo = new THREE.BoxGeometry(SEG, HDR, T);
const hpostGeo = new THREE.BoxGeometry(T, HDR, T);
const _mx = new THREE.Matrix4(), _qy = new THREE.Quaternion(), _up = new THREE.Vector3(0, 1, 0);
const _pos = new THREE.Vector3(), _scl = new THREE.Vector3();
function setInst(im, k, x, y, z, rot, sy, sx = 1) {
  const gone = sy < .002;                                 // fully lowered: zero scale, so nothing is left floating
  _qy.setFromAxisAngle(_up, rot); _mx.compose(_pos.set(x, y, z), _qy, _scl.set(gone ? 0 : sx, gone ? 0 : sy, gone ? 0 : 1)); im.setMatrixAt(k, _mx);
}
function writeWalls() {
  // a tall deck (0.80.0): walls and headers stretch to H when up, and come down to the usual low wall when cut away
  const ts = s => WALL_K === 1 ? s : s * (1 + (WALL_K - 1) * Math.max(0, (s - .12) / .88)), HK = WALL_K === 1 ? 1 : (H - 2.2) / HDR;
  for (const e of wallEdges) setInst(wallIM, e.inst, e.wx, 0, e.wz, e.horiz ? 0 : Math.PI / 2, ts(e.s), e.sx);
  for (const e of frameEdges) { const k = e.rail ? 0 : THREE.MathUtils.clamp((e.s - .5) / .5, 0, 1); setInst(hdrIM, e.hinst, e.cx, 2.2 + HDR * HK / 2, e.cz, e.horiz ? 0 : Math.PI / 2, k * HK); }
  fullPosts.forEach((p, k) => setInst(postIM, k, p.cx, 0, p.cz, 0, p.rail ? RAIL_H / 2.8 : ts(p.s)));   // e.rail / p.rail: a low rail (the rec deck's court, 0.80.10)
  hdrPosts.forEach((p, k) => { const s = p.rail ? 0 : THREE.MathUtils.clamp((p.s - .5) / .5, 0, 1); setInst(hpostIM, k, p.cx, 2.2 + HDR * HK / 2, p.cz, 0, s * HK); });
  for (const im of [wallIM, hdrIM, postIM, hpostIM]) im.instanceMatrix.needsUpdate = true;
  if (sillIM) {
    for (const e of glassEdges) {
      setInst(sillIM, e.ginst, e.cx, 0, e.cz, e.horiz ? 0 : Math.PI / 2, e.rail ? RAIL_H / SILL : Math.min(1, e.s * H / SILL));
      setInst(paneIM, e.ginst, e.cx, (SILL + 2.2) / 2, e.cz, e.horiz ? 0 : Math.PI / 2, e.type === 'pass' ? 0 : THREE.MathUtils.clamp((e.s - .5) / .5, 0, 1));
    }
    sillIM.instanceMatrix.needsUpdate = paneIM.instanceMatrix.needsUpdate = true;
  }
}

// door leaves (sliding), lift doors, thresholds
const liftTex = tex(120, 220, (g, w, h) => {
  g.fillStyle = '#5b6770'; g.fillRect(0, 0, w, h);
  g.fillStyle = 'rgba(0,0,0,.45)'; g.fillRect(w / 2 - 1.5, 0, 3, h);
  g.fillStyle = '#e8c06a'; g.fillRect(8, 10, w - 16, 4);
  g.strokeStyle = 'rgba(255,255,255,.14)'; g.lineWidth = 2; for (let y = 30; y < h; y += 24) { g.beginPath(); g.moveTo(8, y); g.lineTo(w - 8, y); g.stroke(); }
  grain(g, w, h, 8);
});
const leafMats = [0, .5].map(o => { const t = doorTex.clone(); t.needsUpdate = true; t.repeat.set(.5, 1); t.offset.set(o, 0); return new THREE.MeshStandardMaterial({ map: t, roughness: .5, metalness: .3 }); });
const liftLeafMats = [0, .5].map(o => { const t = liftTex.clone(); t.needsUpdate = true; t.repeat.set(.5, 1); t.offset.set(o, 0); return new THREE.MeshStandardMaterial({ map: t, roughness: .4, metalness: .45 }); });
const thrMat = new THREE.MeshBasicMaterial({ color: col('#5fd6c6'), toneMapped: false });
// service hatches: heavy charcoal leaves with gold-and-charcoal hazard bands (no random grain, so the kit's sequence is unchanged)
const hatchLeafTex = tex(120, 220, (g, w, h) => {
  g.fillStyle = '#3a4047'; g.fillRect(0, 0, w, h);
  for (const [y0, hh] of [[0, 26], [h - 30, 30]]) {
    g.save(); g.beginPath(); g.rect(0, y0, w, hh); g.clip();
    g.fillStyle = '#262b30'; g.fillRect(0, y0, w, hh); g.fillStyle = '#d9a441';
    for (let k = -hh; k < w + hh; k += 18) { g.beginPath(); g.moveTo(k, y0 + hh); g.lineTo(k + 9, y0 + hh); g.lineTo(k + 9 + hh, y0); g.lineTo(k + hh, y0); g.closePath(); g.fill(); }
    g.restore();
  }
  g.fillStyle = 'rgba(0,0,0,.45)'; g.fillRect(w / 2 - 1.5, 0, 3, h);
  g.strokeStyle = 'rgba(255,255,255,.12)'; g.lineWidth = 2; g.strokeRect(10, 40, w / 2 - 18, h - 84); g.strokeRect(w / 2 + 8, 40, w / 2 - 18, h - 84);
  g.fillStyle = '#c9b98a'; g.fillRect(w / 2 - 20, h * .46, 6, 26); g.fillRect(w / 2 + 14, h * .46, 6, 26);
});
const hatchLeafMats = [0, .5].map(o => { const t = hatchLeafTex.clone(); t.needsUpdate = true; t.repeat.set(.5, 1); t.offset.set(o, 0); return new THREE.MeshStandardMaterial({ map: t, roughness: .6, metalness: .35 }); });
// 0.27.21: every door leaf on a deck is drawn by one InstancedMesh per leaf material (doorLeavesSync), from this
// one shared box, 1 m wide and stretched to each leaf's width. The leaves themselves stay as invisible boxes for taps.
const DOOR_LEAF_GEO = packGroups(new THREE.BoxGeometry(1, 2.2, .07), [capMat, capMat, capMat, capMat, null, null]);
// inner glass walls: a wall-textured sill to 1 m, a pane, and the usual header above 2.2 m
const SILL = 1.0;
const sillGeo = new THREE.BoxGeometry(SEG, SILL, T); sillGeo.translate(0, SILL / 2, 0);
{ const uv = sillGeo.attributes.uv; for (let q = 0; q < uv.count; q++) uv.setY(q, uv.getY(q) * SILL / H); }   // the wall texture's lower metre
const paneGeo = new THREE.BoxGeometry(SEG, 2.2 - SILL, .04);
const paneMat = std('#bfe3f0', .05, .1, { transparent: true, opacity: .2, depthWrite: false });
let glassEdges = [], sillIM = null, paneIM = null;

// the hull wall: windows are open to the sky beyond the glass
const hullOutMat = std('#3a454d', .7, .3);

// solid blocks over areas you can't enter (the spine and service rooms)
const hatchTex = tex(128, 128, (g, w, h) => {
  g.fillStyle = '#2a3037'; g.fillRect(0, 0, w, h);
  g.strokeStyle = 'rgba(255,255,255,.05)'; g.lineWidth = 6;
  for (let k = -h; k < w; k += 22) { g.beginPath(); g.moveTo(k, h); g.lineTo(k + h, 0); g.stroke(); }
});

const KM = {
  tile: std('#cfd9d8', .35), panel: std('#8fa3a6', .5), partition: std('#9aa9b0', .5), soap: std('#e9c46a', .6),
  vacant: std('#7dffb0', .3, 0, { emissive: col('#3ad07a'), emissiveIntensity: .9 }),
  basin: std('#7f9aa3', .2), mirror: std('#b5cdd4', .12, .1, { emissive: col('#2c4048'), emissiveIntensity: .4 }),
  washer: std('#e3e5e0', .45, .1), drum: std('#3d6f80', .15, .2, { emissive: col('#1b4a57'), emissiveIntensity: .5 }),
  hamper: std('#56466a', .9), label: std('#e9c46a', .5),
  gold: std('#d9a441', .85), red: std('#b8433a', .85), teal: std('#2f8e98', .85),     // uniform cloth
  pod: std('#d6dbd8', .6), podDoor: std('#bfc8c6', .5),
  // the WC sign on toilet stall doors (0.27.42): drawn at load, no R()
  wcSign: std('#ffffff', .5, 0, { map: tex(128, 128, (c, w, h) => {
    c.fillStyle = '#2b6f9e'; c.fillRect(0, 0, w, h); c.strokeStyle = '#eef4f6'; c.lineWidth = 8; c.strokeRect(8, 8, w - 16, h - 16);
    c.fillStyle = '#eef4f6'; c.font = '800 62px system-ui,sans-serif'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText('WC', 64, 68);
  }) }),
  crate: std('#7a6a52', .85), cork: std('#a0764e', .95), paper: std('#ece4d4', .9), note: std('#e9c46a', .9),
};
// =====================================================================
// ART KIT: furniture builders. Each builds in local units: origin at the
// centre of its footprint on the floor, back toward -z, front toward +z.
// Return { w, d } footprint (plus optional extras).
// =====================================================================
// Works kit materials: steel, paint, screens and hazard stripes, shared by every working deck
const hazardTex = tex(64, 64, (g, w, h) => {
  g.fillStyle = '#23272c'; g.fillRect(0, 0, w, h); g.fillStyle = '#d9a441';
  for (let k = -h; k < w + h; k += 32) { g.beginPath(); g.moveTo(k, h); g.lineTo(k + 16, h); g.lineTo(k + 16 + h, 0); g.lineTo(k + h, 0); g.closePath(); g.fill(); }
});
const toolBoardTex = tex(360, 200, (g, w, h) => {
  g.fillStyle = '#3b464d'; g.fillRect(0, 0, w, h);
  g.fillStyle = 'rgba(0,0,0,.35)'; for (let y = 8; y < h; y += 14) for (let x = 8; x < w; x += 14) g.fillRect(x, y, 3, 3);   // pegboard holes
  const outline = (draw) => { g.save(); g.strokeStyle = 'rgba(232,192,106,.55)'; g.lineWidth = 3; g.translate(3, 3); draw(); g.stroke(); g.restore(); };
  const tool = (c, draw) => { g.fillStyle = c; draw(); g.fill(); outline(draw); };
  // spanners, a hammer, screwdrivers, pliers, a coil of cable and a gap where something's missing
  for (let k = 0; k < 5; k++) tool('#b9c3c8', () => { g.beginPath(); g.rect(22 + k * 22, 30, 8, 70 + k * 12); g.arc(26 + k * 22, 30, 11, 0, Math.PI * 2); });
  tool('#c45a3f', () => { g.beginPath(); g.rect(150, 26, 50, 20); g.rect(170, 46, 10, 90); });
  for (let k = 0; k < 4; k++) { tool(['#e9c46a', '#2f8e98', '#c45a3f', '#e9c46a'][k], () => { g.beginPath(); g.rect(222 + k * 18, 28, 12, 42); }); tool('#b9c3c8', () => { g.beginPath(); g.rect(226 + k * 18, 70, 4, 50); }); }
  tool('#2f8e98', () => { g.beginPath(); g.moveTo(300, 30); g.lineTo(318, 30); g.lineTo(330, 120); g.lineTo(316, 120); g.closePath(); g.moveTo(340, 30); g.lineTo(322, 30); g.lineTo(310, 120); g.lineTo(324, 120); g.closePath(); });
  g.strokeStyle = '#d9a441'; g.lineWidth = 5; for (let k = 0; k < 4; k++) { g.beginPath(); g.arc(70, 160, 18 + k * 5, 0, Math.PI * 2); g.stroke(); }
  g.strokeStyle = 'rgba(232,192,106,.6)'; g.lineWidth = 3; g.setLineDash([6, 5]); g.strokeRect(150, 150, 70, 34); g.setLineDash([]);   // the missing one
  g.fillStyle = 'rgba(232,192,106,.85)'; g.font = '600 13px system-ui,sans-serif'; g.fillText('WHO HAS IT?', 152, 196);
});
const WM = {
  steel: std('#8e989e', .35, .6), steelTop: std('#b3bcc0', .28, .7), paintGold: std('#c99a3e', .55, .2), paintDark: std('#333b42', .6, .25),
  hazard: new THREE.MeshStandardMaterial({ map: hazardTex, roughness: .7 }),
  screen: std('#9ff3e6', .3, 0, { emissive: col('#4fd8c4'), emissiveIntensity: 1.0 }),
  screenAmber: std('#ffd28a', .3, 0, { emissive: col('#f0a640'), emissiveIntensity: 1.0 }),
  red: std('#e0503f', .4, 0, { emissive: col('#c4372a'), emissiveIntensity: .8 }),
  rubber: std('#1d2226', .9, 0), bottleGreen: std('#3f7a5a', .4, .3), bottleGrey: std('#8a9298', .4, .4),
  curtain: std('#e08a2c', .7, 0, { transparent: true, opacity: .55, side: THREE.DoubleSide, depthWrite: false }),
  tarp: std('#7c8a78', .95, 0), lightStrip: std('#e6f4ff', .3, 0, { emissive: col('#cfe8ff'), emissiveIntensity: 1.2 }),
  toolBoard: new THREE.MeshStandardMaterial({ map: toolBoardTex, roughness: .8 }),
  fabGlow: std('#7ff0e0', .2, 0, { emissive: col('#3cc9b5'), emissiveIntensity: 1.1, transparent: true, opacity: .75 }),
  hull: std('#e3e5df', .42, .15), hullDark: std('#5b656c', .5, .3), cockpit: std('#1d2f3a', .1, .3, { emissive: col('#16323c'), emissiveIntensity: .6 }),
  engine: std('#ffb35c', .3, 0, { emissive: col('#f08a2c'), emissiveIntensity: .9 }), navRed: std('#ff6b5a', .3, 0, { emissive: col('#ff3b2a'), emissiveIntensity: 1.2 }),
  navGreen: std('#7dffb0', .3, 0, { emissive: col('#2fe07a'), emissiveIntensity: 1.2 }), doorSteel: std('#8a949a', .45, .45),
};
// a toothed gear outline, extruded; teeth of the same pitch mesh whatever the size
function gearGeo(r, n, depth, holes = 0) {
  const sh = new THREE.Shape(), rr = r * .86, da = Math.PI * 2 / n;
  for (let k = 0; k < n; k++) {
    const a0 = k * da;
    [[rr, a0], [r, a0 + da * .2], [r, a0 + da * .45], [rr, a0 + da * .65]].forEach(([rad, a], q) => {
      const x = Math.cos(a) * rad, y = Math.sin(a) * rad; if (k === 0 && q === 0) sh.moveTo(x, y); else sh.lineTo(x, y);
    });
  }
  sh.closePath();
  const hub = new THREE.Path(); hub.absarc(0, 0, r * .16, 0, Math.PI * 2, true); sh.holes.push(hub);
  for (let k = 0; k < holes; k++) { const a = k * Math.PI * 2 / holes, h = new THREE.Path(); h.absarc(Math.cos(a) * r * .5, Math.sin(a) * r * .5, r * .17, 0, Math.PI * 2, true); sh.holes.push(h); }
  const g = new THREE.ExtrudeGeometry(sh, { depth, bevelEnabled: false, curveSegments: 8 }); g.translate(0, 0, -depth / 2); return g;
}
const noMergeAll = o => o.traverse(m => { if (m.isMesh) m.userData.noMerge = true; });
// ---- the music room's materials (Deck 4 bow) ----
const MUS = {
  lacquer: std('#15171c', .22, .15), keysW: std('#efe9dc', .4), keysB: std('#1b1b1f', .3), harp: std('#c9a14e', .35, .7),
  shell: std('#a3392e', .3, .15), head: std('#ece6d6', .6), chrome: std('#c9ced3', .25, .85), brass: std('#d6ad55', .28, .85),
  spruce: std('#d9a35b', .45), rosewood: std('#5a3424', .6), violin: std('#8e3f1c', .35), red: std('#c23b33', .3, .1),
  grille: std('#2a2724', 1), amp: std('#25282d', .7), vinyl: std('#121214', .3), label: std('#d9573f', .6), cab: std('#7a5233', .65),
  stage: std('#3d3029', .7), lens: std('#ffe7b8', .3, 0, { emissive: col('#ffb84d'), emissiveIntensity: 1.3 }),
  fab: ['#2a9d8f', '#6b4a7a', '#c99642', '#3c4f6b'].map(c => std(c, .95)),
};
// a grand piano's outline from above: straight bass side on the left, curved bentside on the right, keys at the front (+y)
function pianoSlab(depth, mat) {
  const sh = new THREE.Shape();
  sh.moveTo(-.72, .72); sh.lineTo(.72, .72); sh.lineTo(.72, .2);
  sh.bezierCurveTo(.72, -.25, .25, -.3, .05, -.6); sh.bezierCurveTo(-.12, -.85, -.3, -.95, -.5, -.95); sh.lineTo(-.72, -.95); sh.closePath();
  const geo = new THREE.ExtrudeGeometry(sh, { depth, bevelEnabled: false, curveSegments: 10 });
  geo.rotateX(Math.PI / 2); geo.translate(0, depth, 0);                // shape y becomes z; the slab sits on y = 0
  const m = new THREE.Mesh(geo, mat); m.castShadow = m.receiveShadow = true; return m;
}
const KIT = {
  // ---- music room ----
  grandPiano(g) {
    const c = pianoSlab(.3, MUS.lacquer); c.position.y = .6; g.add(c);
    const harp = pianoSlab(.012, MUS.harp); harp.scale.set(.88, 1, .88); harp.position.set(0, .905, -.02); g.add(harp);   // the gold frame under the lid
    box(1.36, .08, .2, MUS.lacquer, 0, .66, .8, g);                                       // key bed
    box(1.3, .03, .16, MUS.keysW, 0, .715, .8, g);
    for (let k = 0; k < 35; k++) if ([0, 1, 3, 4, 5].includes(k % 7)) box(.02, .025, .09, MUS.keysB, -.65 + (k + 1) * (1.3 / 36), .74, .76, g);
    for (const x of [-.68, .68]) box(.04, .12, .22, MUS.lacquer, x, .7, .8, g);           // cheek blocks
    box(.62, .22, .02, MUS.lacquer, 0, 1.0, .6, g).rotation.x = -.25;                     // music desk
    box(.4, .26, .006, M.cream, 0, 1.03, .615, g).rotation.x = -.25;                       // sheet music
    for (const [x, z] of [[-.62, .62], [.62, .62], [-.45, -.8]]) cyl(.05, .04, .6, MUS.lacquer, x, .3, z, g, 12);
    box(.12, .4, .04, MUS.lacquer, 0, .25, .55, g);                                       // pedal lyre
    for (const x of [-.05, 0, .05]) box(.025, .02, .1, MUS.brass, x, .04, .6, g);
    const hinge = new THREE.Group(); hinge.position.set(-.72, .9, 0); hinge.rotation.z = .55; g.add(hinge);   // the lid, propped open
    const lid = pianoSlab(.025, MUS.lacquer); lid.position.x = .72; hinge.add(lid);
    box(.025, .47, .025, MUS.lacquer, .04, 1.135, -.15, g);                               // prop stick
    return { w: 1.45, d: 1.9, tall: true };
  },
  pianoBench(g) {
    box(.8, .07, .36, MUS.lacquer, 0, .46, 0, g); box(.76, .05, .32, M.plum, 0, .52, 0, g);
    for (const x of [-.35, .35]) for (const z of [-.14, .14]) box(.04, .44, .04, MUS.lacquer, x, .22, z, g);
    return { w: .8, d: .36 };
  },
  drumKit(g) {
    const drum = (r, h, x, y, z, rx = 0, rz = 0) => {
      const d = new THREE.Group(); d.position.set(x, y, z); d.rotation.set(rx, 0, rz); g.add(d);
      cyl(r, r, h, MUS.shell, 0, 0, 0, d, 20);
      for (const sy of [-1, 1]) cyl(r + .012, r + .012, .025, MUS.chrome, 0, sy * h / 2, 0, d, 20);
      cyl(r - .004, r - .004, .006, MUS.head, 0, h / 2 + .016, 0, d, 20);
      return d;
    };
    const kick = drum(.27, .32, 0, .29, .2, Math.PI / 2);                                // bass drum on its side, head to the room
    cyl(.1, .1, .006, MUS.shell, 0, .19, 0, kick, 20);                                    // a ring on the front head
    box(.08, .03, .16, M.slateDark, 0, .02, -.08, g);                                     // kick pedal
    drum(.11, .13, -.15, .72, .1, -.35); drum(.12, .14, .17, .72, .1, -.35);              // rack toms, tipped to the player
    drum(.16, .11, -.34, .6, -.2, -.12); cyl(.012, .012, .55, MUS.chrome, -.34, .27, -.2, g, 8);   // snare on its stand
    drum(.17, .26, .38, .42, -.16);                                                       // floor tom
    for (const [x, z] of [[.5, -.06], [.27, -.06], [.38, -.3]]) cyl(.01, .01, .3, MUS.chrome, x, .15, z, g, 6);
    // hi-hat, crash and ride
    cyl(.012, .012, .95, MUS.chrome, -.6, .47, -.05, g, 8);
    cyl(.17, .17, .008, MUS.brass, -.6, .92, -.05, g, 24); cyl(.17, .17, .008, MUS.brass, -.6, .955, -.05, g, 24);
    cyl(.012, .012, 1.22, MUS.chrome, -.42, .61, .38, g, 8); cyl(.2, .2, .008, MUS.brass, -.42, 1.24, .38, g, 24).rotation.x = .25;
    cyl(.012, .012, 1.1, MUS.chrome, .56, .55, .26, g, 8); cyl(.23, .23, .008, MUS.brass, .56, 1.12, .26, g, 24).rotation.z = -.2;
    // the throne
    cyl(.16, .16, .07, M.slateDark, 0, .5, -.52, g, 18); cyl(.025, .025, .46, MUS.chrome, 0, .24, -.52, g, 8);
    for (let k = 0; k < 3; k++) { const a = k * 2.094; box(.02, .02, .3, MUS.chrome, Math.sin(a) * .12, .02, -.52 + Math.cos(a) * .12, g).rotation.y = a; }
    return { w: 1.4, d: 1.3, tall: true };
  },
  guitarStand(g, o = {}) {
    const el = o.electric, body = el ? MUS.red : MUS.spruce;
    for (const sx of [-1, 1]) box(.03, .03, .36, M.slateDark, sx * .12, .02, .02, g).rotation.y = sx * .45;
    box(.03, .6, .03, M.slateDark, 0, .3, -.1, g).rotation.x = -.18;
    const gt = new THREE.Group(); gt.position.set(0, .1, .02); gt.rotation.x = -.2; g.add(gt);
    soft(body, 0, .25, 0, el ? .17 : .21, el ? .19 : .22, .05, gt);                       // lower bout
    soft(body, 0, .52, 0, el ? .12 : .16, .15, .05, gt);                                   // upper bout
    if (el) { box(.1, .16, .012, M.dark, .05, .3, .05, gt); box(.12, .025, .012, MUS.chrome, 0, .22, .052, gt); }
    else { const hole = cyl(.06, .06, .012, M.dark, 0, .46, .049, gt, 18); hole.rotation.x = Math.PI / 2; box(.14, .025, .012, MUS.rosewood, 0, .18, .051, gt); }
    box(.05, .55, .03, MUS.rosewood, 0, .9, 0, gt); box(.08, .15, .03, el ? M.dark : MUS.rosewood, 0, 1.24, -.01, gt);
    return { w: .5, d: .45, tall: true };
  },
  amp(g, o = {}) {
    const k = o.big ? 1.25 : 1;
    box(.6 * k, .5 * k, .3, MUS.amp, 0, .25 * k, 0, g);
    box(.5 * k, .32 * k, .02, MUS.grille, 0, .21 * k, .151, g);
    box(.56 * k, .06, .02, M.trim, 0, .44 * k, .151, g);
    for (let q = 0; q < 5; q++) cyl(.018, .018, .03, M.cream, (-.2 + q * .08) * k, .44 * k, .17, g, 10).rotation.x = Math.PI / 2;
    box(.18, .03, .05, M.slateDark, 0, .5 * k + .015, 0, g);
    glow('#ff6b5a', .1, .24 * k, .44 * k, .19, g, .9);
    return { w: .6 * k, d: .3 };
  },
  micStand(g) {
    for (let q = 0; q < 3; q++) { const a = q * 2.094; box(.02, .02, .32, MUS.chrome, Math.sin(a) * .13, .02, Math.cos(a) * .13, g).rotation.y = a; }
    cyl(.012, .012, 1.3, MUS.chrome, 0, .65, 0, g, 8);
    const boom = new THREE.Group(); boom.position.set(0, 1.3, 0); boom.rotation.x = .35; g.add(boom);
    box(.02, .02, .36, MUS.chrome, 0, 0, .14, boom);
    const mic = cyl(.022, .016, .13, M.dark, 0, 0, .36, boom, 10); mic.rotation.x = Math.PI / 2;
    soft(MUS.chrome, 0, 0, .44, .035, .035, .035, boom);
    return { w: .4, d: .4 };
  },
  stageLight(g, o = {}) {
    for (let q = 0; q < 3; q++) { const a = q * 2.094; const l = box(.025, .025, .5, M.slateDark, Math.sin(a) * .16, .2, Math.cos(a) * .16, g); l.rotation.set(.6, a, 0, 'YXZ'); }
    cyl(.02, .02, 1.45, M.slateDark, 0, .78, 0, g, 8);
    const can = new THREE.Group(); can.position.set(0, 1.55, 0); can.rotation.x = Math.PI / 2 + .5; g.add(can);
    cyl(.1, .12, .24, M.slateDark, 0, 0, 0, can, 16); cyl(.1, .1, .02, MUS.lens, 0, .125, 0, can, 16);
    box(.3, .02, .02, M.slateDark, 0, -.02, 0, can);
    glow('#ffc970', .7, 0, 1.47, .15, g, .7);
    if (o.light) addLamp(g, 0, 1.3, .9, 5.5, .6, 1.9);
    return { w: .45, d: .45, tall: true };
  },
  beanbag(g, o = {}) {                                   // 0.27.44: shallower (front .3 ahead, was .4), so a sitter's knees reach its front
    soft(o.fab || MUS.fab[0], 0, .2, -.07, .4, .22, .3, g); soft(o.fab || MUS.fab[0], 0, .34, -.25, .32, .22, .15, g);
    return { w: .8, d: .8 };
  },
  recordCabinet(g) {
    box(1.4, .6, .44, MUS.cab, 0, .3, 0, g);
    box(1.3, .46, .02, M.slateDark, 0, .3, .226, g);                                      // the open shelf
    const spine = ['#d9573f', '#e9c46a', '#2a9d8f', '#efe3c8', '#3c4f6b', '#8e3f1c', '#6b4a7a', '#1b1b1f'].map(c => std(c, .8));
    for (let k = 0; k < 30; k++) { const h = .34 + (k * 37 % 5) * .012; box(.034, h, .03, spine[k * 5 % 8], -.6 + k * .041, .1 + h / 2, .245, g); }
    box(.46, .08, .36, M.wood, -.32, .64, 0, g);                                           // turntable
    cyl(.15, .15, .02, MUS.vinyl, -.34, .69, 0, g, 24); cyl(.045, .045, .01, MUS.label, -.34, .703, 0, g, 16);
    box(.02, .015, .2, MUS.chrome, -.14, .71, .03, g).rotation.y = .35;
    for (const x of [.25, .55]) { box(.22, .3, .22, MUS.amp, x, .75, 0, g); cyl(.06, .06, .02, MUS.grille, x, .73, .115, g, 16).rotation.x = Math.PI / 2; }
    return { w: 1.4, d: .44 };
  },
  bedDouble(g) {
    box(1.4, .32, 2.2, M.slate, 0, .16, 0, g); box(1.32, .16, 2.12, M.cream, 0, .4, 0, g);
    box(1.4, .08, 1.5, M.blanket, 0, .51, .33, g); box(1.42, .1, .26, std('#d9d2c2', .95), 0, .53, -.49, g);
    box(.04, .36, 1.5, M.blanket, .7, .36, .33, g); soft(M.cream, 0, .56, -.8, .5, .08, .18, g);
    box(1.4, .95, .1, M.plum, 0, .7, -1.05, g); box(1.46, .06, .14, M.wood, 0, 1.2, -1.03, g);
    return { w: 1.4, d: 2.2 };
  },
  bedSingle(g, o = {}) {
    const bl = o.blanket || M.blanket;
    box(1.0, .32, 2.0, M.slate, 0, .16, 0, g); box(.94, .15, 1.94, M.cream, 0, .395, 0, g);
    if (o.stripped) box(.9, .02, 1.9, GUEST.ticking, 0, .465, 0, g);            // a spare: bare mattress, no bedding
    else {
      box(1.0, .07, 1.3, bl, 0, .5, .32, g); box(1.02, .09, .24, std('#d9d2c2', .95), 0, .52, -.44, g);
      soft(M.cream, 0, .54, -.72, .36, .07, .16, g);
    }
    if (o.linen) { box(.52, .06, .36, GUEST.sheet, 0, .56, .72, g); box(.46, .05, .3, GUEST.towel, .02, .61, .72, g); }   // fresh linen, still folded
    box(1.0, .8, .08, o.head || M.slate, 0, .62, -.96, g);
    return { w: 1.0, d: 2.0 };
  },
  bunk(g, o = {}) {
    for (const [y, bl] of [[.32, o.low || M.blanket], [1.42, o.high || M.tealFab]]) {
      box(.96, .1, 1.96, M.slate, 0, y, 0, g); box(.9, .13, 1.9, M.cream, 0, y + .115, 0, g);
      box(.96, .06, 1.25, bl, 0, y + .2, .3, g); soft(M.cream, 0, y + .22, -.72, .32, .06, .15, g);
    }
    for (const sx of [-.46, .46]) for (const sz of [-.96, .96]) box(.06, 1.95, .06, M.slateDark, sx, .975, sz, g);
    box(.96, .2, .04, M.slateDark, 0, 1.78, .96, g); box(.04, .2, 1.9, M.slateDark, .46, 1.68, 0, g);
    for (let k = 0; k < 4; k++) box(.04, .03, .32, M.metal, .5, .75 + k * .26, .7, g);
    box(.04, 1.1, .04, M.metal, .5, 1.08, .55, g); box(.04, 1.1, .04, M.metal, .5, 1.08, .85, g);
    return { w: 1.0, d: 2.0, tall: true };
  },
  nightstand(g, o = {}) {
    box(.44, .44, .4, M.wood, 0, .22, 0, g);
    box(.38, .02, .02, M.trim, 0, .3, .2, g);
    if (o.clock) {
      const clk = new THREE.Mesh(new THREE.BoxGeometry(.24, .1, .07), [M.dark, M.dark, M.dark, M.dark, clockMat, M.dark]);
      clk.position.set(-.02, .5, .02); clk.rotation.y = .5; g.add(clk);
      box(.12, .16, .02, M.trim, .08, .52, -.12, g).rotation.y = .9;
    }
    return { w: .44, d: .4 };
  },
  desk(g, o = {}) {
    box(2.2, .06, .66, M.wood, 0, .75, 0, g);
    box(.5, .72, .6, M.slate, .82, .36, 0, g); box(.04, .72, .6, M.slate, -1.06, .36, 0, g);
    box(.46, .02, .02, M.trim, .82, .5, .305, g); box(.46, .02, .02, M.trim, .82, .25, .305, g);
    box(.06, .28, .06, M.slateDark, -.1, .92, -.14, g);
    const mon = new THREE.Mesh(new THREE.BoxGeometry(.92, .58, .04), [M.dark, M.dark, M.dark, M.dark, screenMat, M.dark]);
    mon.position.set(-.1, 1.28, -.12); mon.rotation.x = -.05; g.add(mon);
    box(.5, .02, .16, M.slateDark, -.15, .79, .12, g);
    cyl(.045, .04, .1, std('#e9e1d0', .4), .45, .83, .14, g, 16);
    box(.22, .03, .3, std('#3f6e8c', .8), -.75, .795, .05, g).rotation.y = .3;
    const lamp = new THREE.Group(); lamp.position.set(.85, .78, -.1); g.add(lamp);
    cyl(.09, .1, .03, M.slateDark, 0, .015, 0, lamp);
    box(.025, .45, .025, M.metal, 0, .24, 0, lamp).rotation.z = .25;
    box(.025, .32, .025, M.metal, -.17, .52, 0, lamp).rotation.z = 1.2;
    const sh = new THREE.Mesh(new THREE.ConeGeometry(.11, .14, 20, 1, true), lampShadeMat); sh.position.set(-.3, .5, 0); sh.rotation.z = .5; lamp.add(sh);
    glow('#ffd59a', .55, -.33, .45, 0, lamp, .9);
    glow('#5fd6c6', 1.3, -.1, 1.28, .05, g, .18);
    if (o.light) addLamp(g, .5, 1.15, .1, 3.6, .5, 2.3);
    return { w: 2.2, d: .66 };
  },
  chair(g) {
    box(.5, .08, .48, M.tealFab, 0, .46, 0, g);
    box(.48, .5, .07, M.tealFab, 0, .78, -.24, g).rotation.x = .08;
    cyl(.03, .03, .38, M.metal, 0, .23, 0, g, 12);
    box(.5, .03, .05, M.slateDark, 0, .03, 0, g); box(.05, .03, .5, M.slateDark, 0, .03, 0, g);
    return { w: .5, d: .5, noBlock: true };
  },
  locker(g) {
    const lk = new THREE.Mesh(new THREE.BoxGeometry(1.3, 2.1, .6), [M.slate, M.slate, capMat, M.slate, lockerMat, M.slate]);
    lk.position.y = 1.05; g.add(lk);
    glow('#5fd6c6', .2, 0, 1.75, .32, g, .9);
    return { w: 1.3, d: .6, tall: true };
  },
  footlocker(g) {
    box(.8, .38, .4, M.slate, 0, .19, 0, g); box(.82, .04, .42, M.slateDark, 0, .4, 0, g);
    box(.1, .06, .02, M.metal, 0, .3, .205, g);
    return { w: .8, d: .4 };
  },
  plant(g, o = {}) {
    const s = o.big ? 1.35 : 1;
    cyl(.2 * s, .15 * s, .38 * s, M.ceramic, 0, .19 * s, 0, g);
    cyl(.205 * s, .2 * s, .05 * s, std(o.band || '#2a9d8f', .5), 0, .3 * s, 0, g);
    cyl(.18 * s, .18 * s, .03, std('#3b2a20', 1), 0, .39 * s, 0, g);
    for (let i = 0; i < 9; i++) {
      const a = i / 9 * Math.PI * 2, l = soft(i % 2 ? M.leaf : M.leaf2, Math.sin(a) * .14 * s, .55 * s, Math.cos(a) * .14 * s, .05 * s, .26 * s, .1 * s, g);
      l.rotation.set(Math.cos(a) * .7, 0, -Math.sin(a) * .7);
    }
    soft(M.leaf, 0, .6 * s, 0, .05 * s, .3 * s, .08 * s, g);
    return { w: .4 * s, d: .4 * s };
  },
  rug(g, o) {
    const m = new THREE.MeshStandardMaterial({ map: o.tex, roughness: 1 });
    const r = new THREE.Mesh(new THREE.BoxGeometry(o.w, .025, o.d), [M.slateDark, M.slateDark, m, M.slateDark, M.slateDark, M.slateDark]);
    r.position.y = .0125; r.castShadow = false; r.userData.noShadow = true; g.add(r);
    return { w: o.w, d: o.d, noBlock: true };
  },
  windowSeat(g, o = {}) {
    const w = o.w || 2;
    box(w, .42, .56, M.slate, 0, .21, 0, g);
    box(w - .04, .1, .52, M.mustard, 0, .47, 0, g);
    soft(M.mustard, -w * .27, .66, -.14, .3, .18, .1, g).rotation.z = .15;
    soft(M.tealFab, w * .22, .64, -.14, .26, .16, .09, g).rotation.z = -.2;
    if (w > 2.5) soft(M.plum, w * .02, .62, -.15, .24, .15, .09, g);
    soft(M.plum, .05, .56, .05, .18, .04, .14, g);
    return { w, d: .56 };
  },
  sofa(g, o = {}) {
    const f = o.fab || M.tealFab, w = o.w || 2;          // 0.27.44: the seat ends .12 ahead of centre (was .425), so knees reach its front; d unchanged
    box(w, .3, .54, M.slateDark, 0, .15, -.155, g);
    box(w - .3, .14, .41, f, 0, .37, -.085, g);
    box(w, .5, .2, f, 0, .55, -.32, g);
    for (const sd of [-1, 1]) box(.16, .55, .555, f, sd * (w / 2 - .08), .4, -.1475, g);
    soft(M.mustard, -w * .28, .58, -.12, .2, .16, .07, g).rotation.z = .2;
    return { w, d: .85 };
  },
  armchair(g, o = {}) {
    const f = o.fab || M.plum;                            // 0.27.44: the seat ends .125 ahead of centre (was .41), so knees reach its front; d unchanged
    box(.86, .3, .53, M.slateDark, 0, .15, -.145, g);
    box(.56, .14, .395, f, 0, .37, -.0725, g);
    box(.86, .52, .2, f, 0, .55, -.31, g);
    for (const sd of [-1, 1]) box(.15, .52, .54, f, sd * .355, .41, -.14, g);
    return { w: .86, d: .82 };
  },
  coffeeTable(g) {
    box(1.2, .05, .6, M.wood, 0, .38, 0, g);
    for (const sx of [-.52, .52]) for (const sz of [-.24, .24]) box(.05, .36, .05, M.slateDark, sx, .18, sz, g);
    box(.3, .04, .22, std('#b4553f', .8), -.2, .42, .02, g).rotation.y = .3;
    cyl(.05, .045, .1, std('#e9e1d0', .4), .3, .45, -.05, g, 16);
    return { w: 1.2, d: .6 };
  },
  teaTable(g) {
    cyl(.42, .42, .05, M.wood, 0, .42, 0, g, 32);
    cyl(.05, .07, .38, M.slateDark, 0, .2, 0, g, 12);
    cyl(.24, .26, .03, M.slateDark, 0, .015, 0, g, 24);
    cyl(.05, .045, .1, std('#2a9d8f', .4), .12, .5, .06, g, 16);
    box(.24, .04, .32, std('#b4553f', .8), -.12, .465, -.05, g).rotation.y = -.4;
    addSteam(g, .12, .56, .06);
    return { w: .84, d: .84 };
  },
  pouf(g, o = {}) { soft(o.fab || M.tealFab, 0, .2, 0, .3, .2, .3, g); return { w: .6, d: .6 }; },
  stool(g) {
    cyl(.18, .18, .06, M.tealFab, 0, .46, 0, g, 18); cyl(.03, .03, .42, M.metal, 0, .22, 0, g, 10); cyl(.16, .18, .02, M.slateDark, 0, .01, 0, g, 18);
    return { w: .36, d: .36, noBlock: true };
  },
  tilesTable(g) {                                        // the bow lounge's Tiles station: a square table, a board always set up, two stools (Pillar 4, seat 8)
    box(.72, .04, .72, LNG.wood, 0, .7, 0, g); cyl(.05, .06, .68, M.slateDark, 0, .34, 0, g, 12); cyl(.26, .28, .03, M.slateDark, 0, .015, 0, g, 20);
    const b = new THREE.Mesh(TILES_KIT.geo, TILES_KIT.mat); b.scale.set(.44, 1, .44); b.position.set(0, .722, 0); b.receiveShadow = true; g.add(b);
    box(.16, .05, .08, LNG.wood, .26, .747, -.28, g);    // the tray of spare tiles
    for (const sd of [-1, 1]) { cyl(.17, .17, .06, LNG.rust, sd * .6, .46, 0, g, 16); cyl(.025, .025, .43, LNG.brass, sd * .6, .215, 0, g, 8); cyl(.14, .16, .02, M.slateDark, sd * .6, .01, 0, g, 16); }
    return { w: .72, d: .72 };
  },
  cardTable(g, o = {}) {                                 // o.tiles (0.38.34): a Tiles board set up on it instead of the cards (R() drawn as before)
    box(.9, .05, .9, std('#2f5e4f', .9), 0, .72, 0, g);
    if (o.tiles) { const b = new THREE.Mesh(TILES_KIT.geo, TILES_KIT.mat); b.scale.set(.44, 1, .44); b.position.set(0, .746, 0); b.receiveShadow = true; g.add(b); }
    box(.94, .04, .94, M.wood, 0, .69, 0, g);
    cyl(.06, .08, .66, M.slateDark, 0, .34, 0, g, 12); cyl(.3, .32, .03, M.slateDark, 0, .015, 0, g, 20);
    const cardCols = ['#f1ece2', '#e9c46a', '#5fd6c6', '#e07a5f'];
    for (let k = 0; k < 9; k++) { const t = (R() - .5) * .5; if (!o.tiles) box(.08, .006, .12, std(cardCols[k % 4], .6), (k % 3 - 1) * .14, .75, (Math.floor(k / 3) - 1) * .16, g).rotation.y = t; }
    for (const [x, z] of [[0, -.65], [0, .65], [-.65, 0], [.65, 0]]) {
      const s = new THREE.Group(); s.position.set(x, 0, z); g.add(s); KIT.stool(s);
    }
    return { w: .94, d: .94 };
  },
  messTable(g) {
    box(2.4, .06, .8, std('#d8cfbf', .5), 0, .74, 0, g);
    box(2.3, .04, .7, M.slateDark, 0, .69, 0, g);
    for (const sx of [-1, 1]) box(.08, .68, .5, M.slateDark, sx * 1.0, .34, 0, g);
    for (const sz of [-.7, .7]) { box(2.3, .07, .34, M.wood, 0, .44, sz, g); for (const sx of [-.95, .95]) box(.07, .42, .28, M.slateDark, sx, .21, sz, g); }
    for (let k = 0; k < 3; k++) cyl(.05, .045, .1, std(['#2a9d8f', '#e9e1d0', '#d96a2e'][k], .4), -.7 + k * .65, .82, (k % 2 ? .2 : -.18), g, 14);
    box(.36, .02, .26, std('#e9e1d0', .5), .35, .78, .12, g);
    return { w: 2.4, d: 1.8 };
  },
  galley(g, o = {}) {
    const w = o.w || 4;
    box(w, .86, .66, M.slate, 0, .43, .02, g);
    for (let k = 0; k < Math.floor(w / .6); k++) box(.02, .7, .01, M.slateDark, -w / 2 + .6 * (k + 1) - .3, .42, .36, g);
    box(w + .04, .05, .72, std('#b9c1c4', .3, .6), 0, .885, 0, g);
    box(w, .7, .06, std('#dfe5e3', .4, .1), 0, 1.26, -.31, g);
    box(.9, .02, .5, M.dark, -w / 2 + 1.0, .92, .02, g);
    for (const [x, c] of [[-w / 2 + .78, '#9aa6ad'], [-w / 2 + 1.22, '#c86b4a']]) {
      cyl(.14, .13, .2, std(c, .3, .6), x, 1.03, .02, g, 18); addSteam(g, x, 1.15, .02);
    }
    box(1.1, .3, .5, M.metal, -w / 2 + 1.0, 2.0, -.08, g);
    box(.5, .4, .4, M.slateDark, w / 2 - .5, 1.11, -.05, g);
    for (let k = 0; k < 5; k++) cyl(.035, .03, .12, std(['#e9e1d0', '#2a9d8f', '#d96a2e', '#e9c46a', '#7a5aa8'][k], .4), -.2 + k * .14, .97, .2, g, 12);
    if (o.light) addLamp(g, -w / 2 + 1, 1.7, .5, 5, .6, 1.8);
    return { w, d: .7 };
  },
  servingCounter(g, o = {}) {
    const w = o.w || 3;
    box(w, .95, .5, std('#7a5aa8', .6), 0, .475, 0, g);
    box(w + .1, .05, .62, M.wood, 0, .975, 0, g);
    for (let k = 0; k < 4; k++) soft(std(['#e9c46a', '#c86b4a', '#8fbf6a', '#e9e1d0'][k], .6), -w / 2 + .45 + k * (w - .9) / 3, 1.05, .05, .13, .06, .13, g);
    return { w, d: .62 };
  },
  dispenser(g) {
    box(.8, 1.7, .5, M.slate, 0, .85, 0, g);
    box(.6, .5, .02, std('#123b3e', .3, 0, { emissive: col('#1e6a66'), emissiveIntensity: .9 }), 0, 1.25, .26, g);
    box(.5, .3, .2, M.dark, 0, .55, .2, g);
    glow('#5fd6c6', .8, 0, 1.25, .35, g, .3);
    return { w: .8, d: .5 };
  },
  bookshelf(g) {
    box(1.2, 1.9, .35, M.wood, 0, .95, 0, g);
    box(1.1, 1.8, .02, M.slateDark, 0, .95, -.15, g);
    const cols = ['#b4553f', '#d9c79b', '#3f6e8c', '#e3dfd2', '#56466a', '#2a9d8f', '#e9c46a'];
    for (let s = 0; s < 4; s++) {
      box(1.1, .03, .3, M.slateDark, 0, .2 + s * .45, .01, g);
      let x = -.5;
      while (x < .45) { const bw = .05 + R() * .05, bh = .22 + R() * .14; box(bw, bh, .22, std(cols[Math.floor(R() * cols.length)], .8), x + bw / 2, .215 + s * .45 + bh / 2, .02, g); x += bw + .01; if (R() < .12) x += .12; }
    }
    return { w: 1.2, d: .35, tall: true };
  },
  // ---- washroom, laundry and cabin pieces (room templates) ----
  showerStall(g) {
    box(1.2, .1, 1.1, M.ceramic, 0, .05, 0, g);                                    // tray
    box(1.2, 2.2, .05, KM.tile, 0, 1.1, -.525, g);                                 // tiled back
    box(.05, 2.2, 1.1, KM.panel, -.575, 1.1, 0, g); box(.05, 2.2, 1.1, KM.panel, .575, 1.1, 0, g);
    const gl = box(1.1, 1.85, .025, M.glass, 0, 1.03, .53, g); gl.userData.noShadow = true;
    box(1.2, .05, .06, M.metal, 0, 2.0, .53, g);                                   // door rail
    box(.04, .5, .04, M.metal, 0, 1.75, -.48, g); box(.03, .04, .14, M.metal, 0, 2.0, -.44, g);
    cyl(.08, .06, .03, M.metal, 0, 1.98, -.37, g, 16);                             // shower head
    box(.14, .02, .1, M.metal, .36, 1.2, -.46, g); box(.08, .05, .06, KM.soap, .36, 1.24, -.46, g);
    return { w: 1.2, d: 1.1, tall: true };
  },
  toiletStall(g) {
    box(.05, 1.9, 1.1, KM.partition, -.575, 1.05, 0, g); box(.05, 1.9, 1.1, KM.partition, .575, 1.05, 0, g);   // raised off the floor
    box(1.1, 1.9, .05, KM.partition, 0, 1.05, .525, g);                            // door
    box(.04, .14, .04, M.metal, .38, 1.05, .565, g);
    box(.12, .05, .02, KM.vacant, .38, 1.32, .555, g);                             // the trusted green light
    box(.36, .36, .02, KM.wcSign, 0, 1.6, .555, g);                                // WC, so it doesn't read as a shower (0.27.42)
    for (const sx of [-.575, .575]) box(.06, .12, .06, M.metal, sx, .06, .45, g);
    cyl(.18, .14, .4, M.ceramic, 0, .2, -.15, g, 18); box(.36, .3, .14, M.ceramic, 0, .55, -.45, g);
    return { w: 1.2, d: 1.1, tall: true };
  },
  basinCounter(g, o = {}) {
    const w = o.w || 1.8, n = o.n || 2;
    box(w, .78, .48, M.slate, 0, .39, .02, g);                                     // cabinet
    box(w + .04, .06, .55, M.ceramic, 0, .81, 0, g);                               // counter
    for (let k = 0; k < n; k++) {
      const x = -w / 2 + (k + .5) * w / n;
      cyl(.17, .13, .06, M.ceramic, x, .855, .03, g, 20); cyl(.12, .12, .02, KM.basin, x, .89, .03, g, 20);
      box(.03, .16, .03, M.metal, x, .92, -.2, g); box(.03, .03, .1, M.metal, x, .99, -.16, g);
      box(w / n - .14, .62, .03, KM.mirror, x, 1.48, -.255, g); box(w / n - .08, .68, .02, M.slateDark, x, 1.48, -.27, g);
      glow('#fff2d6', .7, x, 1.86, -.2, g, .35);
    }
    return { w, d: .55 };
  },
  bench(g, o = {}) {
    const w = o.w || 1.4;
    box(w, .06, .38, M.wood, 0, .45, 0, g);
    for (const sx of [-w / 2 + .1, w / 2 - .1]) box(.06, .42, .32, M.slateDark, sx, .21, 0, g);
    return { w, d: .38 };
  },
  washer(g) {
    box(.88, .9, .72, KM.washer, 0, .45, 0, g);
    box(.88, .06, .72, M.slateDark, 0, .92, 0, g);                                 // top
    box(.8, .12, .02, M.dark, 0, .8, .365, g);                                     // controls
    const ring = cyl(.25, .25, .04, M.metal, 0, .42, .37, g, 24); ring.rotation.x = Math.PI / 2;
    const drum = cyl(.2, .2, .05, KM.drum, 0, .42, .38, g, 24); drum.rotation.x = Math.PI / 2;
    glow('#7dffb0', .14, .3, .8, .39, g, .9);
    return { w: .88, d: .72 };
  },
  hamper(g) {
    box(.7, .75, .5, KM.hamper, 0, .375, 0, g);
    box(.74, .05, .54, M.slateDark, 0, .77, 0, g);
    soft(KM.gold, -.12, .8, 0, .2, .08, .14, g); soft(KM.red, .14, .79, .05, .18, .07, .13, g); soft(KM.teal, .02, .83, -.08, .16, .07, .12, g);
    box(.4, .08, .02, KM.label, 0, .6, .255, g);
    return { w: .7, d: .5 };
  },
  uniformRack(g) {
    for (const sx of [-.75, .75]) box(.05, 1.8, .05, M.metal, sx, .9, 0, g);
    box(1.6, .04, .42, M.slateDark, 0, .03, 0, g);
    box(1.56, .03, .03, M.metal, 0, 1.73, 0, g);                                   // rail
    ['gold', 'gold', 'teal', 'red', 'gold', 'teal', 'gold'].forEach((c, k) => {
      const x = -.6 + k * .2;
      box(.012, .1, .012, M.metal, x, 1.67, 0, g);
      box(.07, .62, .34, KM[c], x, 1.3, 0, g); box(.072, .2, .342, M.dark, x, .92, 0, g);
    });
    box(1.5, .04, .38, M.wood, 0, .36, 0, g);                                      // shelf of folded spares
    ['gold', 'teal', 'red'].forEach((c, k) => { for (let q = 0; q < 3; q++) box(.3, .05, .26, KM[c], -.48 + k * .48, .405 + q * .045, 0, g); });
    return { w: 1.6, d: .45, tall: true };
  },
  foldingTable(g, o = {}) {
    const w = o.w || 1.4;
    box(w, .05, .6, M.trim, 0, .86, 0, g);
    for (const sx of [-w / 2 + .06, w / 2 - .06]) box(.05, .84, .5, M.slate, sx, .42, 0, g);
    [['gold', -.4, 3], ['teal', -.05, 2], ['red', .32, 3]].forEach(([c, x, n]) => { for (let q = 0; q < n; q++) box(.3, .05, .24, KM[c], x, .905 + q * .045, .02, g); });
    return { w, d: .6 };
  },
  deskSmall(g, o = {}) {
    box(1.1, .05, .55, M.wood, 0, .75, 0, g);
    box(.04, .73, .5, M.slate, -.52, .365, 0, g); box(.36, .73, .5, M.slate, .35, .365, 0, g);
    const mon = new THREE.Mesh(new THREE.BoxGeometry(.6, .38, .03), [M.dark, M.dark, M.dark, M.dark, o.bare ? M.dark : screenMat, M.dark]);
    mon.position.set(-.12, 1.06, -.16); g.add(mon);
    box(.04, .2, .04, M.slateDark, -.12, .85, -.18, g);
    box(.36, .02, .12, M.slateDark, -.12, .79, .08, g);
    if (!o.bare) {                                       // a bare desk (spare cabins): screen off, no mug
      cyl(.04, .035, .09, M.ceramic, .36, .825, .1, g, 12);
      glow('#5fd6c6', .9, -.12, 1.06, -.1, g, .15);
    }
    return { w: 1.1, d: .55 };
  },
  wardrobe(g) {
    box(.9, 2.0, .55, M.slate, 0, 1.0, 0, g);
    for (const sx of [-.215, .215]) { box(.41, 1.88, .03, M.wood, sx, 1.0, .29, g); box(.03, .22, .03, M.metal, sx - Math.sign(sx) * .16, 1.05, .31, g); }
    box(.92, .05, .57, M.slateDark, 0, 2.0, 0, g);
    return { w: .9, d: .55, tall: true };
  },
  washPod(g) {
    box(1.0, 2.2, .05, KM.pod, 0, 1.1, -.475, g);
    box(.05, 2.2, 1.0, KM.pod, -.475, 1.1, 0, g); box(.05, 2.2, 1.0, KM.pod, .475, 1.1, 0, g);
    box(1.0, .05, 1.0, KM.pod, 0, 2.2, 0, g);
    box(.9, 2.05, .05, KM.podDoor, 0, 1.04, .475, g);                              // sliding door
    box(.04, .3, .03, M.metal, .3, 1.05, .51, g);
    box(.3, .06, .02, KM.vacant, 0, 1.95, .505, g);
    return { w: 1.0, d: 1.0, tall: true };
  },
  telescope(g) {
    for (let k = 0; k < 3; k++) { const a = k * Math.PI * 2 / 3, l = box(.03, 1.1, .03, M.metal, Math.sin(a) * .2, .52, Math.cos(a) * .2, g); l.rotation.set(Math.cos(a) * .36, 0, -Math.sin(a) * .36); }
    box(.08, .08, .08, M.slateDark, 0, 1.06, 0, g);
    const tube = cyl(.07, .09, .9, M.trim, .12, 1.25, .05, g, 16); tube.rotation.z = -1.0;
    cyl(.095, .095, .06, M.slateDark, .5, 1.5, .05, g, 16).rotation.z = -1.0;
    cyl(.03, .03, .12, M.dark, -.25, 1.02, .05, g, 10).rotation.z = -1.0;
    return { w: .6, d: .6 };
  },
  shelving(g) {
    for (const sx of [-.57, .57]) for (const sz of [-.2, .2]) box(.04, 1.9, .04, M.metal, sx, .95, sz, g);
    for (let k = 0; k < 4; k++) {
      const y = .12 + k * .55; box(1.18, .03, .44, M.slateDark, 0, y, 0, g);
      let x = -.5; while (x < .42) { const w = .14 + R() * .16, h = .14 + R() * .22; box(w, h, .3, [KM.label, KM.teal, KM.panel, M.trim, KM.gold][Math.floor(R() * 5)], x + w / 2, y + .015 + h / 2, 0, g); x += w + .03; }
    }
    return { w: 1.2, d: .45, tall: true };
  },
  crate(g) {
    box(.7, .5, .5, KM.crate, 0, .25, 0, g);
    for (const y of [.12, .38]) box(.72, .05, .52, M.slateDark, 0, y, 0, g);
    box(.3, .08, .02, KM.label, 0, .25, .255, g);
    return { w: .7, d: .5 };
  },
  // a Works bench: steel top, drawers, a vice, a half-opened unit and a task lamp
  workbench(g, o = {}) {
    const w = o.w || 1.8;
    box(w, .06, .8, WM.steelTop, 0, .9, 0, g);
    for (const sx of [-w / 2 + .06, w / 2 - .06]) for (const sz of [-.33, .33]) box(.06, .87, .06, WM.paintDark, sx, .435, sz, g);
    box(w - .1, .03, .7, WM.steel, 0, .22, 0, g);
    box(.52, .66, .72, WM.paintDark, w / 2 - .32, .55, 0, g);
    for (const y of [.33, .55, .77]) box(.46, .015, .02, WM.paintGold, w / 2 - .32, y, .365, g);
    box(.22, .12, .16, WM.steel, -w / 2 + .2, .99, .3, g); box(.06, .06, .2, WM.paintGold, -w / 2 + .2, .99, .44, g);   // vice
    box(.46, .2, .34, KM.panel, -.05, 1.03, -.08, g);                                // a unit on the bench, lid off
    box(.46, .02, .3, KM.panel, -.08, 1.2, -.3, g).rotation.x = -1.1;
    box(.3, .03, .2, WM.screen, .32, .945, .12, g).rotation.x = -.25;                // diagnostic slate
    box(.08, .04, .06, WM.red, -.18, 1.15, -.04, g);
    cyl(.02, .02, .55, WM.paintDark, w / 2 - .15, 1.2, -.32, g, 8);                  // task lamp
    box(.22, .06, .12, WM.paintDark, w / 2 - .25, 1.47, -.24, g);
    glow('#e8f6ff', .55, w / 2 - .27, 1.42, -.2, g, .45);
    return { w, d: .8 };
  },
  // the lathe: a long bed on a cabinet, a chuck, a tailstock, a glass chip guard and hazard paint at the base
  lathe(g) {
    box(2.0, .62, .62, WM.paintDark, 0, .31, 0, g);
    box(2.02, .1, .64, WM.hazard, 0, .05, 0, g);
    for (const z of [-.1, .1]) box(1.7, .06, .08, WM.steelTop, .05, .68, z, g);
    box(.46, .5, .58, WM.paintGold, -.74, .9, 0, g); box(.46, .06, .6, WM.paintDark, -.74, 1.18, 0, g);
    const ch = cyl(.16, .16, .14, WM.steel, -.44, .92, 0, g, 20); ch.rotation.z = Math.PI / 2;
    const wp = cyl(.05, .05, .9, WM.steelTop, 0, .92, 0, g, 14); wp.rotation.z = Math.PI / 2;
    box(.24, .32, .3, WM.paintGold, .62, .86, 0, g); const qu = cyl(.035, .035, .16, WM.steel, .46, .92, 0, g, 10); qu.rotation.z = Math.PI / 2;
    box(.2, .18, .2, WM.steel, .1, .78, .16, g);                                     // tool post
    const gd = box(1.1, .5, .02, M.glass, 0, 1.0, .3, g); gd.rotation.x = -.15; gd.userData.noShadow = true;
    box(.3, .22, .06, WM.paintDark, -.74, .95, .32, g);
    box(.06, .06, .02, WM.screen, -.82, .99, .355, g); box(.06, .06, .02, WM.red, -.68, .99, .355, g);
    return { w: 2.0, d: .7 };
  },
  // the parts fabricator: a cabinet with a glowing print bed behind glass
  fabricator(g) {
    box(1.1, 1.62, .88, KM.pod, 0, .81, 0, g);
    box(1.12, .08, .9, WM.paintGold, 0, 1.6, 0, g);
    box(.8, .62, .04, WM.paintDark, 0, 1.0, .43, g);
    box(.72, .54, .02, WM.fabGlow, 0, 1.0, .455, g).userData.noShadow = true;
    box(.3, .08, .3, WM.steelTop, 0, .78, .2, g);
    box(.14, .1, .14, WM.screenAmber, .05, .87, .2, g);                              // a part, half printed
    box(.26, .16, .03, WM.screen, .3, 1.42, .45, g);
    box(1.0, .1, .7, WM.hazard, 0, .05, 0, g);
    glow('#7ff0e0', .9, 0, 1.0, .55, g, .35);
    return { w: 1.1, d: .9, tall: true };
  },
  // the welding bench: a steel table, an amber screen behind it, a mask and two gas bottles
  weldBench(g) {
    box(1.4, .06, .78, WM.steel, -.1, .85, 0, g);
    for (const sx of [-.74, .54]) for (const sz of [-.32, .32]) box(.06, .82, .06, WM.paintDark, sx, .41, sz, g);
    for (const sx of [-.8, .6]) box(.04, 1.8, .04, WM.paintDark, sx, .9, -.38, g);
    const cu = new THREE.Mesh(new THREE.PlaneGeometry(1.36, 1.0), WM.curtain); cu.position.set(-.1, 1.4, -.38); cu.userData.noShadow = true; g.add(cu);
    box(1.44, .04, .04, WM.paintDark, -.1, 1.9, -.38, g);
    box(.26, .22, .1, WM.paintDark, -.45, .99, .1, g); box(.18, .07, .02, WM.screenAmber, -.45, 1.01, .16, g);   // mask
    box(.5, .06, .2, WM.steelTop, .12, .91, .05, g);                                 // a bracket being welded
    cyl(.11, .11, 1.1, WM.bottleGreen, .78, .55, -.18, g, 16); cyl(.11, .11, 1.0, WM.bottleGrey, .78, .5, .12, g, 16);
    cyl(.05, .05, .08, WM.steel, .78, 1.14, -.18, g, 10); cyl(.05, .05, .08, WM.steel, .78, 1.04, .12, g, 10);
    return { w: 1.8, d: .86 };
  },
  // the storage check-out counter: a terminal, a sign-out log and a bell nobody rings
  counter(g) {
    box(1.8, .92, .6, WM.paintDark, 0, .46, 0, g);
    box(1.86, .05, .66, WM.steelTop, 0, .945, 0, g);
    box(1.8, .06, .02, WM.paintGold, 0, .7, .305, g);
    box(.5, .32, .04, WM.paintDark, -.45, 1.15, -.1, g).rotation.x = -.2;
    box(.44, .26, .02, WM.screen, -.45, 1.15, -.075, g).rotation.x = -.2;
    box(.3, .02, .4, KM.paper, .3, .98, .02, g).rotation.y = .2;
    cyl(.05, .07, .05, KM.label, .7, .995, .1, g, 14);
    return { w: 1.8, d: .6 };
  },
  // a sign hung from the ceiling over the end of an aisle
  aisleSign(g, o = {}) {
    const t = tex(256, 64, (c, w, h) => {
      c.fillStyle = '#23272c'; c.fillRect(0, 0, w, h); c.fillStyle = '#d9a441'; c.fillRect(0, 0, 10, h); c.fillRect(w - 10, 0, 10, h);
      c.fillStyle = '#f2e3b8'; c.font = '700 28px system-ui,sans-serif'; c.textAlign = 'center'; c.fillText(o.text || '', w / 2, 43);
    });
    const p = new THREE.Mesh(new THREE.PlaneGeometry(.92, .23), new THREE.MeshBasicMaterial({ map: t, toneMapped: false }));
    p.position.set(0, 2.3, .03); g.add(p);
    box(.96, .27, .04, WM.paintDark, 0, 2.3, 0, g);
    for (const x of [-.38, .38]) box(.015, .3, .015, WM.steel, x, 2.58, 0, g);
    return { w: .2, d: .2, noBlock: true };
  },
  // something under a tarp in the back corner that nobody remembers ordering
  tarpHeap(g) {
    box(.7, .5, .5, KM.crate, 0, .25, 0, g);
    soft(WM.tarp, 0, .78, 0, .42, .34, .3, g);
    box(.16, .1, .02, KM.label, .18, .32, .255, g);
    return { w: .7, d: .5 };
  },
  // the shuttle Tern, big enough to walk inside (0.38.18, plans/shuttle-plan.md): nose at +z, the side door and its ramp on
  // +x. 2.9 x 6 m, the cabin floor flush with the deck, roof at 2.4 m: an aisle down the middle (pz -2..2), benches either
  // side, the cockpit at the nose, lockers across the tail. The roof and the hull above 1 m are one group (o.roof gets it)
  // that hides while you're inside; the ramp (o.ramp gets its hinge) is the door, upright when closed, lying almost flat
  // when open. Both are merged on their own and kept out of the deck's merge. No R().
  shuttle(g, o = {}) {
    // 0.38.33 (the user's "very boxy"): the same cabin, sleeker outside: the sides run straight to z 2.1, then taper to the nose
    // (half-width 1.12 at the front), the windscreen rakes back to the roof, the roof's edges are softened, the fins sweep
    // back, a dark canopy line runs aft from the windscreen, and the red and teal lines follow the taper. Same materials.
    const NZ = 2.1, NF = 3.05, NW = 1.12, NA = Math.atan2(1.39 - NW, NF - NZ), NL = Math.hypot(1.39 - NW, NF - NZ) + .04;
    // 0.47.4 (Tern pass 2, plans/tern-pass2.md): the tail tapers like the nose, over a shorter run (straight from z TZ, half-width TW at the back)
    const TZ = -2.45, TF = -3.05, TW = 1.12, TA = Math.atan2(1.39 - TW, TZ - TF), TL = Math.hypot(1.39 - TW, TZ - TF) + .04;
    const slab = (pts, y, h, mat, p, bev) => {             // a flat piece drawn in plan ([x, z] corners), from y up h (bev: bevelled edges)
      const sh = new THREE.Shape(); pts.forEach(([x, z], k) => k ? sh.lineTo(x, -z) : sh.moveTo(x, -z));
      const geo = new THREE.ExtrudeGeometry(sh, bev ? { depth: h - 2 * bev, bevelEnabled: true, bevelThickness: bev, bevelSize: bev, bevelSegments: 1 } : { depth: h, bevelEnabled: false });
      if (bev) geo.translate(0, 0, bev);
      const m = new THREE.Mesh(geo, mat); m.rotation.x = -Math.PI / 2; m.position.y = y; m.castShadow = m.receiveShadow = true; p.add(m); return m;
    };
    const mirror = q => [...q, ...q.slice().reverse().map(([x, z]) => [-x, z])];   // the +x half's corners, nose to tail -> the whole outline
    const side = (y, h, mat, gx, roofG) => {             // a hull side at x = gx, from y to y + h; the +x side has the door gap (pz -.97 to -.03)
      const parts = gx > 0 ? [[TZ - .02, -.97], [-.03, NZ + .02]] : [[TZ - .02, NZ + .02]];
      for (const [z0, z1] of parts) box(.12, h, z1 - z0, mat, gx, y + h / 2, (z0 + z1) / 2, roofG);
      const sd = Math.sign(gx), off = Math.abs(gx) - 1.39;   // and the nose piece, angled in (off: a line laid on the hull's face)
      box(.12, h, TL, mat, sd * ((1.39 + TW) / 2 + off * Math.cos(TA)), y + h / 2, (TZ + TF) / 2 - off * Math.sin(TA), roofG).rotation.y = sd * TA;   // the tail piece, angled in
      const cx = sd * ((1.39 + NW) / 2 + off * Math.cos(NA)), cz = (NZ + NF) / 2 + off * Math.sin(NA);
      if (y + h < 1.6) { box(.12, h, NL, mat, cx, y + h / 2, cz, roofG).rotation.y = -sd * NA; return; }
      const sh = new THREE.Shape();                      // the upper hull's nose piece: its top slopes down with the windscreen
      sh.moveTo(-NL / 2, y); sh.lineTo(NL / 2, y); sh.lineTo(NL / 2, 1.56); sh.lineTo(-NL / 2, y + h); sh.lineTo(-NL / 2, y);
      const geo = new THREE.ExtrudeGeometry(sh, { depth: .12, bevelEnabled: false }); geo.translate(0, 0, -.06);
      const m = new THREE.Mesh(geo, mat); m.position.set(cx, 0, cz); m.rotation.y = -Math.PI / 2 - sd * NA; m.castShadow = m.receiveShadow = true; roofG.add(m);
    };
    slab(mirror([[1.05, 2.95], [1.33, NZ], [1.33, TZ], [1.05, -2.95]]), 0, .02, WM.steel, g);   // the cabin floor, inside the taper
    for (const gx of [-1.39, 1.39]) { side(0, 1.0, WM.hull, gx, g); side(.86, .08, KM.red, gx + Math.sign(gx) * .012, g); }   // lower hull, a red line at the top
    box(2.3, 1.0, .12, WM.hull, 0, .5, -2.99, g); box(2.3, 1.0, .12, WM.hull, 0, .5, 2.99, g);   // tail and nose, lower
    box(.5, .42, 4.0, WM.hullDark, -1.05, .21, 0, g); box(.46, .08, 3.9, KM.teal, -1.05, .46, 0, g); box(.08, .6, 4.0, WM.hullDark, -1.29, .76, 0, g);   // the north bench
    for (const [z, l] of [[1.0, 2.0], [-1.5, 1.0]]) { box(.5, .42, l, WM.hullDark, 1.05, .21, z, g); box(.46, .08, l - .1, KM.teal, 1.05, .46, z, g); box(.08, .6, l, WM.hullDark, 1.29, .76, z, g); }   // the south benches, either side of the door
    slab(mirror([[1.33, -2.05], [1.33, TZ], [1.06, -2.93]]), 0, 1.9, WM.hullDark, g); for (const x of [-.66, 0, .66]) box(.6, .04, .02, WM.steel, x, 1.2, -2.04, g);   // the lockers across the tail, and their handles
    box(2.0, .03, .03, WM.lightStrip, 0, 1.75, -2.04, g); box(2.0, .03, .03, WM.lightStrip, 0, .79, 2.48, g);   // cabin lights: over the lockers and along the console's edge (glow, no lamp)
    box(2.2, .8, .45, WM.paintDark, 0, .4, 2.72, g); for (const x of [-.55, .55]) { box(.5, .02, .3, WM.screen, x, .81, 2.7, g); cyl(.2, .2, .1, KM.teal, x, .45, 2.3, g, 14); cyl(.05, .05, .4, WM.steel, x, .2, 2.3, g, 8); }   // the cockpit: console, screens, two seats
    for (const sx of [-.62, .62]) {                     // engine pods faired into the tail: a long pod, a steel nozzle, the glow set inside it
      for (const [rt, rb, l, mat, z] of [[.34, .3, .5, WM.hullDark, -3.28], [.3, .27, .08, WM.steel, -3.58], [.22, .22, .02, WM.engine, -3.635]]) cyl(rt, rb, l, mat, sx, 1.0, z, g, 18).rotation.x = Math.PI / 2;
    }
    box(.6, .34, .5, WM.hullDark, 0, 1.0, -3.28, g);                                       // the fairing between the pods
    for (const sd of [-1, 1]) { box(.62, .07, 1.0, WM.hull, sd * 1.72, .75, -2.3, g).rotation.y = sd * .5; box(.06, .12, .12, sd < 0 ? WM.navRed : WM.navGreen, sd * 1.98, .75, -2.62, g); }   // stub wings, swept back; nav lights at the tips
    // the roof group: the hull above 1 m, windows, livery, windscreen, roof and fin
    const R = new THREE.Group(); g.add(R);
    for (const gx of [-1.39, 1.39]) { side(1.0, 1.3, WM.hull, gx, R); side(1.08, .12, KM.teal, gx + Math.sign(gx) * .012, R); for (const z of [-1.5, -.5, .5, 1.5]) if (!(gx > 0 && z === -.5)) box(.03, .32, .5, WM.cockpit, gx + Math.sign(gx) * .065, 1.6, z, R); }
    box(.12, .3, .94, WM.hull, 1.39, 2.15, -.5, R);                                             // over the door
    box(2.3, 1.3, .12, WM.hull, 0, 1.65, -2.99, R);
    box(2.3, .58, .12, WM.hull, 0, 1.28, 2.99, R);                                               // the nose under the windscreen
    {                                                    // the windscreen: from the nose (y 1.54) raked back to the roof, as wide as the tapering sides
      const sh = new THREE.Shape(), Lw = Math.hypot(.77, NF - .05 - NZ - .02);
      sh.moveTo(-NW - .01, 0); sh.lineTo(NW + .01, 0); sh.lineTo(1.37, Lw); sh.lineTo(-1.37, Lw); sh.lineTo(-NW - .01, 0);
      const ws = new THREE.Mesh(new THREE.ExtrudeGeometry(sh, { depth: .03, bevelEnabled: false }), WM.cockpit);
      ws.position.set(0, 1.54, NF - .05); ws.rotation.x = -Math.atan2(NF - .05 - NZ - .02, .77); ws.castShadow = true; R.add(ws);
    }
    slab(mirror([[1.45, NZ], [1.45, TZ], [1.18, TF]]), 2.3, .1, WM.hull, R);                // the roof (back from the windscreen), tapering at the tail
    slab(mirror([[.45, 1.55], [.75, .8], [.75, -1.8], [.5, -2.35]]), 2.38, .14, WM.hull, R, .04);   // its raised spine, narrowing at both ends, edges bevelled
    for (const sd of [-1, 1]) {                         // the roof's edges, softened, round the tail too; the nose and tail corners rounded
      box(.17, .17, NZ - TZ, WM.hull, sd * 1.36, 2.32, (NZ + TZ) / 2, R).rotation.z = Math.PI / 4;
      box(.17, .17, TL, WM.hull, sd * ((1.45 + TW + .06) / 2 - .09 * Math.cos(TA)), 2.32, (TZ + TF) / 2 + .09 * Math.sin(TA), R).rotation.set(0, sd * TA, Math.PI / 4);
      for (const z of [2.99, -2.99]) { box(.15, 1.0, .15, WM.hull, sd * 1.12, .5, z, g).rotation.y = Math.PI / 4; box(.15, z > 0 ? .56 : 1.3, .15, WM.hull, sd * 1.12, z > 0 ? 1.28 : 1.65, z, R).rotation.y = Math.PI / 4; }
    }
    box(2.2, .17, .17, WM.hull, 0, 2.32, -2.96, R).rotation.x = Math.PI / 4;
    box(.9, .03, .52, WM.cockpit, 0, 2.415, NZ - .24, R); box(.9, .03, 2.4, WM.cockpit, 0, 2.535, .4, R);   // the canopy line, aft from the windscreen
    box(.08, .55, 1.1, WM.hull, 0, 2.62, -2.55, R).rotation.x = -.5; box(.09, .14, .55, KM.teal, 0, 2.78, -2.72, R).rotation.x = -.5;   // the fin, swept back
    const name = tex(256, 64, (c, w, h) => { c.fillStyle = '#1c3d44'; c.font = '700 40px system-ui,sans-serif'; c.fillText('TERN', 8, 44); c.font = '600 18px system-ui,sans-serif'; c.fillText('CSV WREN · 1', 130, 42); });
    const nm = new THREE.Mesh(new THREE.PlaneGeometry(1.3, .32), new THREE.MeshBasicMaterial({ map: name, transparent: true, toneMapped: false }));
    nm.position.set(1.47, 1.95, 1.4); nm.rotation.y = Math.PI / 2; nm.userData.noShadow = true; R.add(nm);
    mergeMeshes(R); for (const m of R.children) m.userData.noMerge = true;
    // the ramp: hinged at the door's foot, upright (closed) or lying out over the bay floor (open)
    const P = new THREE.Group(); P.position.set(1.42, .1, -.5); g.add(P);
    box(.06, 1.88, .92, WM.steel, 0, .94, 0, P); for (let k = 0; k < 6; k++) box(.02, .03, .8, WM.paintDark, .04, .25 + k * .3, 0, P);   // ribs on the outer face
    mergeMeshes(P); for (const m of P.children) m.userData.noMerge = true;
    if (o.roof) o.roof(R); if (o.ramp) o.ramp(P);
    return { w: 2.9, d: 6.1, tall: true };
  },
  // the bay doors: the flat stern hull, two heavy leaves in a hazard frame, a warning lamp over the seam
  bayDoors(g, o = {}) {
    const w = o.w || 10, hh = H - .12;
    for (const sx of [-1, 1]) {
      box(w / 2 - .06, hh, .16, WM.doorSteel, sx * w / 4, hh / 2, .08, g);
      for (let k = 1; k < 6; k++) box(w / 2 - .2, .05, .04, WM.paintDark, sx * w / 4, k * hh / 6, .18, g);
    }
    box(w - .1, .34, .04, WM.hazard, 0, .3, .18, g);                                          // a hazard band across the foot
    box(.06, hh, .05, WM.lightStrip, 0, hh / 2, .2, g);                                        // the seam
    box(w + .3, .22, .22, WM.hazard, 0, hh - .02, .1, g);
    for (const sx of [-1, 1]) box(.22, hh, .22, WM.hazard, sx * (w / 2 + .04), hh / 2, .1, g);
    box(.3, .14, .14, WM.navRed, 0, hh - .26, .25, g); glow('#ff4a3a', .6, 0, hh - .26, .36, g, .55);
    return { w, d: .3, noBlock: true };
  },
  // the bay door gear: a big gear driving a small one, a ram, and the door leaf parked in its pocket. Kit +z faces the window.
  doorGear(g) {
    box(3.0, H - .1, .3, WM.doorSteel, .45, (H - .1) / 2, -1.3, g);                           // the leaf, stowed (clear of the hull's curved corner)
    for (let k = 1; k < 6; k++) box(2.9, .05, .04, WM.paintDark, .45, k * (H - .1) / 6, -1.13, g);
    box(.14, 2.3, .14, WM.paintDark, .2, 1.15, -.65, g); box(.14, 2.3, .14, WM.paintDark, -1.55, 1.6, -.65, g);   // frame
    box(2.0, .14, .14, WM.paintDark, -.65, 2.3, -.65, g);
    const big = new THREE.Mesh(gearGeo(.9, 24, .14, 5), WM.paintGold); big.position.set(.2, 1.15, -.5); big.castShadow = true; g.add(big);
    const small = new THREE.Mesh(gearGeo(.45, 12, .14, 0), WM.steelTop); small.position.set(-1.0, 1.55, -.5);   // pitch circles touch small.castShadow = true; g.add(small);
    small.rotation.z = Math.PI / 12;
    for (const [x, y] of [[.2, 1.15], [-1.0, 1.55]]) { const a = cyl(.09, .09, .4, WM.steel, x, y, -.55, g, 12); a.rotation.x = Math.PI / 2; }
    noMergeAll(big); noMergeAll(small);
    SPINS.push({ o: big, ax: 'z', w: .22 }, { o: small, ax: 'z', w: -.44 });
    const ram = cyl(.13, .13, 1.6, WM.paintDark, 1.0, .55, .35, g, 14); ram.rotation.z = Math.PI / 2;   // hydraulic ram
    const rod = cyl(.05, .05, 1.0, WM.steelTop, 1.0 - 1.25, .55, .35, g, 10); rod.rotation.z = Math.PI / 2;
    box(.3, .5, .3, WM.hazard, 1.85, .25, .35, g);
    return { w: 4.0, d: 3.0, noBlock: true };
  },
  // the fan: a ring, a shroud behind it, a five-blade rotor turning slowly. Kit +z faces the window.
  bigFan(g) {
    const cy = 1.45, R0 = 1.28;
    const ring = new THREE.Mesh(new THREE.TorusGeometry(R0, .1, 10, 40), WM.paintGold); ring.position.set(0, cy, .25); g.add(ring);
    const shroud = new THREE.Mesh(new THREE.CylinderGeometry(R0, 1.0, .5, 32, 1, true), std('#77828a', .5, .35, { side: THREE.DoubleSide }));
    shroud.rotation.x = -Math.PI / 2; shroud.position.set(0, cy, -.12); g.add(shroud);
    cyl(.5, .5, .06, WM.paintDark, 0, cy, -.38, g, 24).rotation.x = Math.PI / 2;   // the duct mouth behind the rotor
    const rotor = new THREE.Group(); rotor.position.set(0, cy, .1); g.add(rotor);
    cyl(.24, .24, .3, WM.paintDark, 0, 0, 0, rotor, 18).rotation.x = Math.PI / 2;
    for (let k = 0; k < 5; k++) {
      const arm = new THREE.Group(); arm.rotation.z = k * Math.PI * 2 / 5; rotor.add(arm);
      const b = box(.36, 1.0, .04, WM.steelTop, 0, .7, 0, arm); b.rotation.y = .38;
    }
    noMergeAll(rotor); SPINS.push({ o: rotor, ax: 'z', w: .85 });
    for (const sx of [-.9, .9]) box(.16, cy - .9, .3, WM.paintDark, sx, (cy - .9) / 2, .2, g);
    box(2.4, .12, .6, WM.hazard, 0, .06, .2, g);
    return { w: 2.8, d: 1.4, noBlock: true };
  },
  // the bay control booth: a console angled at the pad, a chair, a stack of flight logs
  boothConsole(g) {
    box(1.6, .8, .55, WM.paintDark, 0, .4, 0, g);
    const top = box(1.64, .05, .6, WM.steelTop, 0, .83, .05, g); top.rotation.x = .18;
    for (const x of [-.45, .45]) { const sc = box(.6, .38, .04, WM.screen, x, 1.12, -.12, g); sc.rotation.x = -.2; }
    box(.3, .02, .2, WM.screenAmber, 0, .9, .15, g);
    box(.25, .06, .3, KM.paper, .65, .87, .12, g);
    return { w: 1.6, d: .6 };
  },
  // The spine runs through every deck at the same place beside the lift car. These two pieces fill the one
  // row next to the car (kit origin = that row's centre, the back against the car), so they line up deck to deck.
  // Decks with more spine room add their own fittings around them.
  // ---- the hydroponics garden ----
  raisedBed(g, o = {}) {                                 // a timber bed of soil, planted by o.crop; greens and herbs get a grow light
    const w = o.w || 1.8, crop = o.crop || 'greens', L = GD.leaves;
    const P = o.live ? plantSlots(g, o.live, .475) : null, lf = P ? P.leaf : leaf, sf = P ? P.soft : soft;   // o.live: section 8b's garden view grows them (0.27.23)
    box(w, .46, .9, GD.bed, 0, .23, 0, g); box(w - .1, .03, .8, GD.soil, 0, .46, 0, g);
    for (const x of [-w / 2 + .02, w / 2 - .02]) box(.06, .5, .92, GD.post, x, .25, 0, g);
    const nx = Math.floor((w - .2) / .3);
    for (let r = 0; r < 2; r++) for (let k = 0; k < nx; k++) {
      const x = -w / 2 + .22 + k * (w - .44) / Math.max(1, nx - 1), z = r ? .2 : -.2, j = R();
      if (crop === 'greens') { lf(L[(k + r) % 2 ? 2 : 4], x, .56, z, .16 + j * .03, .11, .16, g); lf(L[1], x, .62, z, .08, .06, .08, g); }
      else if (crop === 'herbs') { lf(L[(k * 3 + r) % 5], x, .56 + j * .04, z, .07, .1 + j * .05, .07, g); lf(L[(k + 1) % 5], x + .06, .54, z + .04, .05, .07, .05, g); }
      else if (crop === 'flowers') { leaf(L[1], x, .54, z, .1, .07, .1, g); leaf(GD.flowers[(k + r * 2) % 5], x + (j - .5) * .05, .64 + j * .05, z, .055, .045, .055, g); }
      else if (crop === 'roots') { lf(L[(k + r) % 2 ? 1 : 3], x, .58 + j * .02, z, .05, .13 + j * .04, .05, g); sf(GD.orange, x, .49, z, .045, .03, .045, g); }   // feathery tops, orange shoulders in the soil (0.38.7)
      else if (crop === 'tomato') {
        if (k % 2) continue;
        cyl(.012, .012, 1.3, GD.post, x, 1.1, z, g, 6);
        for (let h = 0; h < 4; h++) lf(L[(h + k) % 5], x + (R() - .5) * .1, .65 + h * .26, z + (R() - .5) * .1, .14, .12, .14, g);
        for (let h = 0; h < 3; h++) if (R() < .8) sf(GD.tomato, x + (R() - .5) * .18, .7 + h * .3, z + .1, .04, .04, .04, g);
      }
    }
    if (crop === 'greens' || crop === 'herbs') {
      for (const x of [-w / 2 + .05, w / 2 - .05]) box(.04, 1.35, .04, GD.post, x, 1.1, -.42, g);
      box(w, .05, .14, M.slateDark, 0, 1.78, -.3, g); box(w - .1, .02, .08, GD.led, 0, 1.75, -.28, g);
      glow('#ff7ae0', .9, 0, 1.6, -.25, g, .35);
    }
    if (o.butterflies) {                                 // two butterflies circling the flowers
      const piv = new THREE.Group(); piv.position.set(0, .95, 0); g.add(piv); SPINS.push({ o: piv, ax: 'y', w: .7 });
      for (let k = 0; k < 2; k++) {
        const b = new THREE.Group(); b.position.set(k ? .5 : -.35, k * .25, k ? .15 : -.1); piv.add(b);
        for (const sd of [-1, 1]) { const wg = new THREE.Mesh(new THREE.PlaneGeometry(.07, .05), GD.wing[k]); wg.position.x = sd * .035; wg.rotation.y = sd * .5; b.add(wg); }
      }
    }
    return { w, d: .9 };
  },
  growRack(g) {                                          // three tiers of trays under pink grow lights
    for (const x of [-.86, .86]) for (const z of [-.25, .25]) box(.04, 2.0, .04, M.metal, x, 1.0, z, g);
    for (let t = 0; t < 3; t++) {
      const y = .35 + t * .6;
      box(1.72, .08, .5, M.slateDark, 0, y, 0, g);
      for (let k = 0; k < 7; k++) for (const z of [-.12, .12]) leaf(GD.leaves[(k + t + (z > 0 ? 1 : 0)) % 5], -.72 + k * .24, y + .1, z, .1, .07 + R() * .04, .1, g);
      box(1.6, .02, .08, GD.led, 0, y + .5, 0, g);
    }
    glow('#ff7ae0', .8, 0, 1.2, .1, g, .3);
    return { w: 1.8, d: .6, tall: true };
  },
  seedlingStand(g, o = {}) {                             // three timber steps of pots, a seedling in each but o.yours (Pillar 4, seat 8: Sowing morning)
    for (let t = 0; t < 3; t++) {                        // front step lowest; plank tops at .28, .52, .76
      const y = .26 + t * .24, z = .17 - t * .17;
      box(.62, .04, .2, GD.bed, 0, y, z, g);
      for (const x of [-.31, .31]) box(.03, y + .01, .18, GD.post, x, (y + .01) / 2, z, g);   // the stepped sides, under the plank's ends
      for (let k = 0; k < 4; k++) {
        const i = t * 4 + k, x = -.225 + k * .15, top = y + .02;
        cyl(.055, .042, .1, GD.pot, x, top + .05, z, g, 10); cyl(.05, .05, .012, GD.soil, x, top + .1, z, g, 10);   // the soil heaped just over the rim
        if (i === o.yours) continue;
        const s = .7 + ((i * 7 + 3) % 5) * .12;          // sown the same morning, grown a little differently
        leaf(GD.leaves[(i + t) % 5], x - .018 * s, top + .13 + .02 * s, z, .03 * s, .045 * s, .03 * s, g);
        leaf(GD.leaves[(i + 2) % 5], x + .02 * s, top + .14 + .025 * s, z + .01, .028 * s, .04 * s, .028 * s, g);
        if (s > 1) leaf(GD.leaves[(i + 4) % 5], x, top + .17 + .03 * s, z - .01, .024 * s, .035 * s, .024 * s, g);
      }
    }
    return { w: .64, d: .58 };
  },
  trellis(g, o = {}) {                                   // a climbing frame lost under beans and vines
    for (const x of [-.75, .75]) box(.05, 2.0, .05, GD.post, x, 1.0, 0, g);
    for (const y of [.6, 1.2, 1.9]) box(1.55, .03, .03, GD.post, 0, y, 0, g);
    box(1.6, .3, .35, GD.bed, 0, .15, 0, g);
    const P = o.live ? plantSlots(g, o.live, .3) : null, lf = P ? P.leaf : leaf, pd = P ? P.pod : cyl;   // o.live: grown by section 8b (0.27.23)
    for (let k = 0; k < 16; k++) lf(GD.leaves[k % 5], -.7 + R() * 1.4, .4 + R() * 1.6, (R() - .5) * .2, .12 + R() * .08, .12, .1, g);
    for (let k = 0; k < 8; k++) pd(.012, .01, .14, GD.bean, -.6 + R() * 1.2, .6 + R() * 1.2, .08, g, 5);
    for (let k = 0; k < 5; k++) lf(GD.flowers[k % 5], -.6 + R() * 1.2, .6 + R() * 1.3, .1, .04, .04, .04, g);
    return { w: 1.6, d: .4, tall: true };
  },
  citrusTree(g, o = {}) {                                // a little orange (or lemon) tree in a big pot
    const fruit = o.lemon ? GD.lemon : GD.orange;
    cyl(.42, .34, .55, GD.pot, 0, .275, 0, g, 18); cyl(.38, .38, .03, GD.soil, 0, .54, 0, g, 18);
    cyl(.05, .07, 1.1, GD.post, 0, 1.05, 0, g, 8);
    for (let k = 0; k < 9; k++) { const a = k * .7, r = k ? .38 : 0; leaf(GD.leaves[k % 3 + 1], Math.sin(a) * r, 1.75 + (k % 3) * .14, Math.cos(a) * r, .34, .3, .34, g); }
    for (let k = 0; k < 9; k++) { const a = k * 1.3; soft(fruit, Math.sin(a) * .5, 1.55 + (k % 4) * .14, Math.cos(a) * .5, .055, .055, .055, g); }
    return { w: 1.0, d: 1.0, tall: true };
  },
  bush(g, o = {}) {                                      // a low leafy clump; o.size scales it
    const s = o.size || 1, n = 5 + Math.floor(R() * 3);
    for (let k = 0; k < n; k++) { const a = k / n * 6.28 + R(), r = .18 * s; leaf(GD.leaves[(k + (o.v || 0)) % 5], Math.sin(a) * r, .25 * s + R() * .15 * s, Math.cos(a) * r, .26 * s, .24 * s, .26 * s, g); }
    leaf(GD.leaves[2], 0, .45 * s, 0, .22 * s, .2 * s, .22 * s, g);
    if (o.bloom) for (let k = 0; k < 6; k++) leaf(GD.flowers[(k + o.bloom) % 5], (R() - .5) * .5 * s, .4 * s + R() * .2 * s, (R() - .5) * .5 * s, .045, .045, .045, g);
    return { w: .8 * s, d: .8 * s };
  },
  pond(g) {                                              // a round pool: stone rim, lily pads, a few fish, a bubbling stone
    const rim = new THREE.Mesh(new THREE.CylinderGeometry(1.15, 1.2, .22, 32, 1, true), GD.stone); rim.position.y = .11; g.add(rim);
    const lip = new THREE.Mesh(new THREE.RingGeometry(.98, 1.16, 32), GD.stone2); lip.rotation.x = -Math.PI / 2; lip.position.y = .22; g.add(lip);
    const inner = new THREE.Mesh(new THREE.CylinderGeometry(.99, .99, .2, 32, 1, true), GD.stone); inner.position.y = .11; inner.material.side = THREE.DoubleSide; g.add(inner);
    cyl(.98, .98, .02, GD.dark, 0, .02, 0, g, 28); cyl(.98, .98, .02, GD.water, 0, .16, 0, g, 28);
    for (let k = 0; k < 5; k++) { const a = k * 1.25, r = .55 + (k % 2) * .2; const p = cyl(.14, .14, .01, GD.pad, Math.sin(a) * r, .2, Math.cos(a) * r, g, 10); p.castShadow = false; }
    leaf(GD.flowers[2], Math.sin(1.25) * .75, .23, Math.cos(1.25) * .75, .05, .03, .05, g);
    for (let k = 0; k < 3; k++) { const a = k * 2.1 + .5; soft(GD.fish, Math.sin(a) * .4, .12, Math.cos(a) * .4, .07, .025, .03, g).rotation.y = a; }
    leaf(GD.stone2, .2, .25, -.15, .18, .14, .16, g); glow('#bfefff', .5, .2, .4, -.15, g, .35);
    for (let k = 0; k < 10; k++) { const a = k * .63; leaf(GD.stone2, Math.sin(a) * 1.15, .22, Math.cos(a) * 1.15, .1, .05, .1, g); }
    return { w: 2.3, d: 2.3 };
  },
  bigTree(g) {                                           // a proper tree, planted in the ground, its canopy over the pond
    for (let k = 0; k < 5; k++) { const a = k * 1.26; const r = cyl(.05, .09, .5, GD.post, Math.sin(a) * .2, .1, Math.cos(a) * .2, g, 6); r.rotation.set(Math.cos(a) * .9, 0, -Math.sin(a) * .9); }
    cyl(.12, .2, 2.0, GD.post, 0, 1.0, 0, g, 10);
    for (const [a, l] of [[.5, .8], [2.6, .7], [4.4, .75]]) { const b = cyl(.05, .08, l, GD.post, Math.sin(a) * .25, 1.8, Math.cos(a) * .25, g, 6); b.rotation.set(Math.cos(a) * .7, 0, -Math.sin(a) * .7); }
    for (let k = 0; k < 16; k++) { const a = k * 2.4, r = .35 + (k % 4) * .28; leaf(GD.leaves[k % 5], Math.sin(a) * r, 2.2 + (k % 3) * .22 - r * .15, Math.cos(a) * r, .42, .36, .42, g); }
    for (let k = 0; k < 10; k++) { const a = k * .63, r = 1.15; leaf(GD.leaves[(k + 2) % 5], Math.sin(a) * r, 1.75 - (k % 2) * .25, Math.cos(a) * r, .14, .4, .14, g); }   // trailing fronds
    return { w: .9, d: .9, tall: true };
  },
  groundCover(g, o = {}) {                               // a carpet of low leaves and a few flowers, spilling across the floor
    const r = o.r || .8; cyl(r, r, .02, GD.leaves[3], 0, .01, 0, g, 16).castShadow = false;
    const n = Math.round(r * 12);
    for (let k = 0; k < n; k++) { const a = k * 2.4, d = Math.sqrt((k + .5) / n) * r * .9; leaf(GD.leaves[k % 5], Math.sin(a) * d, .08, Math.cos(a) * d, .14, .08 + (k % 3) * .03, .14, g); }
    for (let k = 0; k < n / 3; k++) { const a = k * 1.9 + 1, d = Math.sqrt((k + .5) / n * 3) * r * .8; leaf(GD.flowers[(k + (o.v || 0)) % 5], Math.sin(a) * d, .17, Math.cos(a) * d, .04, .035, .04, g); }
    return { w: r * 1.6, d: r * 1.6, noBlock: !o.block };
  },
  stepStone(g) { const m = cyl(.26, .28, .04, GD.stone2, 0, .02, 0, g, 12); m.castShadow = false; return { w: .5, d: .5, noBlock: true }; },
  moss(g, o = {}) { const m = cyl(o.r || .9, o.r || .9, .02, GD.leaves[3], 0, .01, 0, g, 18); m.castShadow = false; return { w: .2, d: .2, noBlock: true }; },
  gardenLamp(g, o = {}) {                                // a tall post with a warm globe
    cyl(.14, .16, .04, M.slateDark, 0, .02, 0, g, 14); cyl(.03, .03, 2.1, GD.post, 0, 1.06, 0, g, 8);
    const gb = soft(GD.ledW, 0, 2.15, 0, .13, .13, .13, g); gb.castShadow = false; glow('#fff1d0', 1.0, 0, 2.15, 0, g, .5);
    if (o.light) addLamp(g, 0, 2.0, 0, 6.5, .5, 1.7);
    return { w: .3, d: .3, noBlock: true };
  },
  pollen(g, o = {}) { g.add(makePollen(o.w || 3, o.d || 2)); return { w: .1, d: .1, noBlock: true }; },
  // ---- the infirmary and exam room ----
  medBed(g, o = {}) {                                    // a bed with a monitor, a drip stand and a curtain on a rail
    box(.9, .1, 1.95, MED.frame, 0, .5, 0, g); for (const x of [-.4, .4]) for (const z of [-.9, .9]) cyl(.025, .025, .5, MED.frame, x, .25, z, g, 8);
    box(.86, .14, 1.9, MED.mattress, 0, .62, 0, g); box(.88, .05, 1.2, MED.sheet, 0, .7, .3, g); soft(MED.white, 0, .74, -.72, .3, .07, .16, g);
    box(.9, .55, .05, MED.frame, 0, .8, -.98, g);
    box(.32, .24, .04, M.slateDark, .62, 1.45, -.85, g); box(.26, .16, .01, MED.screen, .62, 1.46, -.828, g); cyl(.02, .02, 1.3, MED.frame, .62, .7, -.88, g, 6);
    cyl(.015, .015, 1.7, MED.frame, -.6, .85, -.6, g, 6); soft(MED.sheet, -.6, 1.6, -.6, .06, .1, .04, g);
    if (o.curtain) {                                     // the rail round the foot, the curtain half drawn
      box(.02, .02, 2.2, MED.frame, .58, 2.2, .1, g); box(1.2, .02, .02, MED.frame, 0, 2.2, 1.2, g);
      const c = new THREE.Mesh(new THREE.PlaneGeometry(1.0, 1.8), MED.curtain); c.position.set(.58, 1.3, .55); c.rotation.y = Math.PI / 2; g.add(c);
    }
    return { w: .95, d: 2.0 };
  },
  medDesk(g) {                                           // the front desk: a curved-front counter, a terminal, a bell
    box(1.6, 1.0, .55, MED.white, 0, .5, 0, g); box(1.66, .05, .62, M.wood, 0, 1.02, 0, g);
    box(1.6, .06, .02, MED.cross, 0, .8, .28, g);
    box(.5, .32, .04, M.slateDark, -.35, 1.25, -.12, g); box(.44, .26, .01, MED.screen, -.35, 1.25, -.095, g);
    cyl(.05, .06, .05, MESS.trays[2], .45, 1.07, .1, g, 12);
    return { w: 1.6, d: .6 };
  },
  medCabinet(g) {                                        // a glass-fronted cabinet of medicines, with a red cross
    box(1.0, 1.9, .45, MED.white, 0, .95, 0, g); box(.9, 1.0, .02, M.glass, 0, 1.35, .23, g);
    for (let k = 0; k < 3; k++) { const y = .95 + k * .32; box(.9, .02, .38, MED.frame, 0, y, 0, g); for (let q = 0; q < 6; q++) cyl(.04, .04, .12, SHOP.goods[(q + k) % 8], -.35 + q * .14, y + .07, 0, g, 8); }
    box(.24, .07, .02, MED.cross, 0, 1.75, .235, g); box(.07, .24, .02, MED.cross, 0, 1.75, .235, g);
    return { w: 1.0, d: .45, tall: true };
  },
  examBed(g) {                                           // a padded table with a paper roll and a scanner arm over it
    box(1.9, .7, .6, MED.white, 0, .35, 0, g); box(1.9, .12, .7, MED.mattress, 0, .76, 0, g); box(1.4, .01, .5, MED.paper, .2, .83, 0, g);
    cyl(.07, .07, .62, MED.paper, -.9, .8, 0, g, 12).rotation.x = Math.PI / 2;
    cyl(.04, .04, 1.9, MED.frame, .85, 1.2, -.42, g, 8); box(1.0, .05, .05, MED.frame, .4, 2.12, -.3, g);
    box(.5, .12, .3, M.slateDark, -.05, 2.04, -.1, g); box(.4, .02, .2, MED.screen, -.05, 1.97, -.1, g);
    return { w: 1.9, d: .7 };
  },
  // ---- the gym ----
  treadmill(g, o = {}) {
    box(.8, .14, 1.8, GYM.frame, 0, .07, 0, g); const belt = box(.6, .02, 1.6, GYM.rubber, 0, .15, .05, g);
    for (const x of [-.36, .36]) box(.05, 1.15, .06, GYM.frame, x, .65, -.82, g);
    box(.76, .32, .14, GYM.frame, 0, 1.25, -.8, g); const scr = box(.5, .2, .02, MED.screen, 0, 1.28, -.72, g);
    for (const x of [-.36, .36]) box(.04, .04, .5, GYM.chrome, x, 1.0, -.6, g);
    if (o.place) {                                       // Pillar 2: the belt runs and the console brightens while someone is on it (MOVERS)
      const bt = beltTex.clone(); bt.needsUpdate = true;
      belt.material = new THREE.MeshStandardMaterial({ map: bt, roughness: .9 }); belt.userData.noMerge = true;
      const sm = MED.screen.clone(); scr.material = sm; scr.userData.noMerge = true;
      let v = 0;
      MOVERS.push({ place: o.place, tick(dt, on) {
        if (!on && v === 0) return;
        v += ((on ? 1 : 0) - v) * Math.min(1, dt * 3); if (!on && v < .01) v = 0;
        bt.offset.y = (bt.offset.y + dt * v * 2.4) % 1; sm.emissiveIntensity = 1 + v * 1.4;
      } });
    }
    return { w: .8, d: 1.9 };
  },
  rower(g, o = {}) {
    box(.16, .08, 2.1, GYM.chrome, 0, .3, 0, g); box(.4, .1, .4, GYM.frame, 0, .26, .95, g);
    cyl(.24, .24, .16, GYM.frame, 0, .42, -.92, g, 20).rotation.z = Math.PI / 2; const seat = box(.3, .06, .3, GYM.rubber, 0, .4, .2, g);
    for (const x of [-.18, .18]) box(.12, .03, .2, GYM.frame, x, .3, -.55, g);
    const bar = box(.5, .03, .03, GYM.accent, 0, .55, -.7, g);
    if (o.place) {                                       // Pillar 2: the seat slides while someone rows (MOVERS); the handle comes with them (playtest 2, 0.71.3)
      seat.userData.noMerge = true; bar.userData.noMerge = true;
      let v = 0, ph = 0;
      MOVERS.push({ place: o.place, tick(dt, on) {
        if (!on && v === 0) return;
        v += ((on ? 1 : 0) - v) * Math.min(1, dt * 3); if (!on && v < .01) v = 0;
        ph += dt * 3.2; seat.position.z = .2 + Math.sin(ph) * .32 * v;
        bar.position.z = -.7 + (Math.sin(ph) + 1) * .3 * v; bar.position.y = .55 + (Math.sin(ph) + 1) * .06 * v;   // pulled in to the chest as the seat slides back, out again on the return
      } });
    }
    return { w: .6, d: 2.2 };
  },
  weightRack(g) {                                        // dumbbells on two rails, plates on the side
    for (const x of [-.75, .75]) box(.05, .9, .5, GYM.frame, x, .45, 0, g);
    for (const [y, z] of [[.45, .12], [.8, -.08]]) {
      box(1.5, .04, .2, GYM.frame, 0, y, z, g);
      for (let k = 0; k < 6; k++) { const x = -.6 + k * .24, s = .05 + k * .008; for (const sd of [-1, 1]) cyl(s, s, .06, GYM.plate, x + sd * .07, y + .07, z, g, 10).rotation.z = Math.PI / 2; cyl(.015, .015, .14, GYM.chrome, x, y + .07, z, g, 6).rotation.z = Math.PI / 2; }
    }
    return { w: 1.6, d: .55 };
  },
  weightBench(g) {
    box(.32, .1, 1.2, GYM.teal, 0, .45, 0, g); for (const z of [-.5, .5]) box(.3, .4, .06, GYM.frame, 0, .2, z, g);
    for (const x of [-.55, .55]) box(.05, 1.2, .05, GYM.frame, x, .6, -.45, g);
    const bar = new THREE.Group(); bar.position.set(0, 1.15, -.45); g.add(bar);   // 0.47.5: the bar and its plates, one piece that hides while it's in a lifter's hands (BENCH_BAR)
    cyl(.018, .018, 1.6, GYM.chrome, 0, 0, 0, bar, 8).rotation.z = Math.PI / 2;
    for (const x of [-.68, .68]) { cyl(.18, .18, .05, GYM.plate, x, 0, 0, bar, 16).rotation.z = Math.PI / 2; }
    noMergeAll(bar); BENCH_BAR.g = bar; bar.children[0].onBeforeRender = () => { const on = performance.now() - BENCH_BAR.t > 500; for (const m of bar.children) m.scale.setScalar(on ? 1 : 1e-4); };
    return { w: 1.3, d: 1.3 };
  },
  gymMats(g) {                                           // three mats, a ball and a roller in the stretching corner
    for (let k = 0; k < 3; k++) { const m = box(.6, .015, 1.7, GYM.mat[k], (k - 1) * .75, .008, 0, g); m.castShadow = false; }
    soft(GYM.mat[1], 1.75, .32, .5, .32, .32, .32, g); cyl(.07, .07, .4, GYM.mat[2], 1.6, .07, -.4, g, 10).rotation.z = Math.PI / 2;   // 0.27.41: the ball and roller clear of the end mat (edge 1.05) and of a lifter's feet there
    return { w: 2.6, d: 1.8, noBlock: true };
  },
  // ---- the crew store ----
  shopShelf(g) {                                         // shelves of bright little boxes and jars
    for (const x of [-.58, .58]) box(.04, 1.8, .42, M.slateDark, x, .9, 0, g); box(1.2, 1.8, .03, M.slate, 0, .9, -.2, g);
    for (let k = 0; k < 4; k++) {
      const y = .15 + k * .45; box(1.16, .03, .4, M.wood, 0, y, 0, g);
      let x = -.52; while (x < .45) { const w = .1 + R() * .12, h = .12 + R() * .18, c = SHOP.goods[Math.floor(R() * 8)]; if (R() < .3) cyl(w / 2, w / 2, h, c, x + w / 2, y + .015 + h / 2, .05, g, 10); else box(w, h, .26, c, x + w / 2, y + .015 + h / 2, .03, g); x += w + .02; }
    }
    return { w: 1.2, d: .42, tall: true };
  },
  drinksFridge(g) {                                      // a glass-door fridge of fizzy drinks, lit from inside
    box(1.0, 1.9, .65, M.slateDark, 0, .95, 0, g); box(.9, 1.7, .02, SHOP.glowW, 0, .95, -.28, g);
    for (let k = 0; k < 4; k++) { const y = .3 + k * .4; box(.88, .02, .5, M.metal, 0, y, 0, g); for (let q = 0; q < 6; q++) cyl(.035, .035, .16, SHOP.goods[(q * 3 + k) % 8], -.35 + q * .14, y + .09, .05, g, 8); }
    box(.92, 1.75, .02, M.glass, 0, .95, .33, g); box(.03, .6, .04, M.metal, .4, 1.1, .36, g);
    return { w: 1.0, d: .65, tall: true };
  },
  shopDisplay(g) {                                       // the window display: a little table of this week's things
    cyl(.4, .4, .04, M.wood, 0, .7, 0, g, 20); cyl(.04, .04, .68, M.slateDark, 0, .35, 0, g, 8);
    box(.18, .22, .12, SHOP.goods[0], -.15, .83, 0, g); box(.14, .14, .14, SHOP.goods[1], .12, .79, .08, g); soft(SHOP.goods[4], .1, .78, -.15, .06, .06, .06, g);
    box(.22, .14, .01, MED.paper, -.05, .98, -.12, g);
    return { w: .8, d: .8 };
  },
  // ---- the call-home booths ----
  callBooth(g, o = {}) {                                 // a cubicle with a small desk under the window, a screen, a stool and tissues
    for (const x of [-.55, .55]) box(.05, 1.9, 1.3, MED.white, x, .95, 0, g);
    box(1.04, .04, .45, M.wood, 0, .78, -.42, g); box(1.04, .05, .04, M.slateDark, 0, .74, -.2, g);
    const sc = box(.5, .32, .03, M.slateDark, 0, 1.08, -.5, g); sc.rotation.x = -.15; const ss = box(.44, .26, .01, o.live ? MED.screen : M.dark, 0, 1.08, -.48, g); ss.rotation.x = -.15;
    box(.14, .06, .1, M.slateDark, -.3, .83, -.4, g); box(.14, .08, .1, MED.paper, .3, .84, -.42, g);
    cyl(.2, .2, .06, MESS.chairB, 0, .5, .15, g, 16); cyl(.03, .03, .47, M.metal, 0, .25, .15, g, 8);
    const hp = new THREE.Mesh(new THREE.TorusGeometry(.08, .012, 6, 14, Math.PI), M.slateDark); hp.position.set(-.3, .95, -.4); g.add(hp);
    return { w: 1.15, d: 1.3 };
  },
  // ---- the promenade ----
  planterIsland(g, o = {}) {                             // a planter down the middle of the promenade: a tree, flowers,
    const cl = PROM.clad, L = GD.leaves, fl = o.flowers || 0;   // a bench facing each lane, a warm strip under the seats
    box(2.4, .42, .66, cl, 0, .21, 0, g); box(2.48, .05, .74, PROM.rim, 0, .445, 0, g); box(2.32, .03, .58, GD.soil, 0, .465, 0, g);
    for (const sz of [-1, 1]) {
      box(2.2, .05, .3, M.wood, 0, .42, sz * .52, g);
      for (const x of [-1.02, 1.02]) box(.05, .4, .26, PROM.frame, x, .2, sz * .52, g);
      const st = box(2.1, .02, .03, GD.ledW, 0, .05, sz * .38, g); st.castShadow = false;
    }
    cyl(.05, .08, 1.9, GD.post, 0, 1.4, 0, g, 8);         // the tree: a slim trunk and a round crown, held up high
    for (let k = 0; k < 11; k++) { const a = k * 2.4, r = k ? .15 + (k % 3) * .13 : 0; leaf(L[1 + k % 2], Math.sin(a) * r, 2.45 + (k % 4) * .09 - r * .25, Math.cos(a) * r * .8, .28, .24, .25, g); }
    if (o.fruit) for (let k = 0; k < 6; k++) { const a = k * 1.7 + .4; soft(GD.lemon, Math.sin(a) * .36, 2.3 + (k % 3) * .11, Math.cos(a) * .3, .04, .04, .04, g); }
    for (let k = 0; k < 16; k++) {                       // flowers and greenery round the trunk
      const x = -1.05 + (k >> 1) * .3, z = k % 2 ? .16 : -.16;
      if (Math.abs(x) < .15) continue;
      leaf(L[1 + k % 2], x, .53, z, .1, .08, .1, g);
      leaf(PROM.bloom[fl + k % 2], x + .02, .6, z, .04, .035, .04, g);
    }
    return { w: 2.48, d: 1.34, tall: true };
  },
  routeKiosk(g) {                                        // a two-sided screen on a post: the Wren's route across the frontier
    const t = tex(256, 340, (c, w, h) => {
      c.fillStyle = '#0b1424'; c.fillRect(0, 0, w, h);
      for (let k = 0; k < 90; k++) {                     // stars from a fixed hash, so the deck's random sequence is untouched
        const hx = Math.abs(Math.sin(k * 12.9898) * 43758.5453) % 1, hy = Math.abs(Math.sin(k * 78.233) * 12543.123) % 1;
        c.fillStyle = `rgba(230,240,255,${.25 + (k % 5) * .12})`; c.fillRect(hx * w, 40 + hy * 220, 1.6, 1.6);
      }
      const veyli = c.createRadialGradient(205, 120, 5, 205, 120, 90); veyli.addColorStop(0, 'rgba(201,120,214,.35)'); veyli.addColorStop(1, 'rgba(201,120,214,0)');
      c.fillStyle = veyli; c.fillRect(0, 30, w, 240);
      c.fillStyle = '#e8c06a'; c.font = '700 20px system-ui,sans-serif'; c.fillText('THE TOUR', 16, 30);
      const P = [[30, 230], [70, 200], [96, 150], [140, 160], [168, 112], [205, 96], [226, 60]];
      c.setLineDash([5, 5]); c.strokeStyle = 'rgba(95,214,198,.55)'; c.lineWidth = 2; c.beginPath(); P.forEach(([x, y], k) => k ? c.lineTo(x, y) : c.moveTo(x, y)); c.stroke();
      c.setLineDash([]); c.strokeStyle = '#5fd6c6'; c.lineWidth = 3; c.beginPath(); P.slice(0, 4).forEach(([x, y], k) => k ? c.lineTo(x, y) : c.moveTo(x, y)); c.stroke();
      for (const [x, y] of P) { c.fillStyle = '#a9c4bf'; c.beginPath(); c.arc(x, y, 3.5, 0, 6.29); c.fill(); }
      c.fillStyle = '#f2c94c'; c.beginPath(); c.arc(140, 160, 7, 0, 6.29); c.fill();
      c.font = '600 12px system-ui,sans-serif'; c.fillStyle = '#f2c94c'; c.fillText('WREN', 150, 178);
      c.fillStyle = '#7fa9a3'; c.fillText('Concord space', 14, 258); c.fillStyle = '#c99ad6'; c.fillText('Veyli reaches', 160, 40 + 14);
      c.fillStyle = '#a9c4bf'; c.font = '500 13px system-ui,sans-serif'; c.fillText('Survey stops: 3 of 7', 16, h - 44);
      c.fillStyle = '#7fa9a3'; c.font = '500 12px system-ui,sans-serif'; c.fillText('Next: the Harrow drift', 16, h - 22);
    });
    const sm = new THREE.MeshBasicMaterial({ map: t, toneMapped: false });
    box(.12, 1.0, .12, PROM.frame, 0, .5, 0, g); box(.5, .05, .34, PROM.frame, 0, .025, 0, g);
    box(.72, .92, .1, PROM.frame, 0, 1.45, 0, g); box(.76, .04, .14, PROM.brass, 0, 1.93, 0, g);
    for (const sz of [-1, 1]) { const p = new THREE.Mesh(new THREE.PlaneGeometry(.62, .82), sm); p.position.set(0, 1.45, sz * .056); if (sz < 0) p.rotation.y = Math.PI; g.add(p); }
    return { w: .76, d: .4 };
  },
  // ---- Deck 3 bow lounge ----
  booth(g, o = {}) {                                     // two high-backed benches facing across a table, against a wall
    const f = o.fab || LNG.navy;
    for (const sd of [-1, 1]) {
      box(.5, .42, 1.4, LNG.wood, sd * .7, .21, .05, g);
      box(.46, .12, 1.36, f, sd * .7, .48, .05, g);
      box(.14, 1.25, 1.4, f, sd * .9, .66, .05, g);
      box(.16, .06, 1.42, LNG.wood, sd * .9, 1.31, .05, g);
    }
    box(.86, .05, 1.1, LNG.wood, 0, .74, .1, g); cyl(.05, .05, .7, M.metal, 0, .37, .1, g, 10); box(.5, .03, .5, M.slateDark, 0, .015, .1, g);
    cyl(.05, .045, .09, MESS.white, -.15, .8, .2, g, 12); cyl(.04, .04, .14, LNG.bottles[o.k || 0], .2, .84, -.05, g, 10);
    const lamp = cyl(.09, .12, .12, LNG.shade, 0, 1.55, -.6, g, 14); lamp.castShadow = false; glow('#ffd59a', .55, 0, 1.5, -.55, g, .4);
    return { w: 1.94, d: 1.5 };
  },
  backBar(g) {                                           // shelves of bottles in front of a mirror, lit from below
    box(1.6, .9, .45, LNG.wood, 0, .45, 0, g); box(1.64, .04, .5, LNG.brass, 0, .92, 0, g);
    box(1.5, 1.0, .03, LNG.mirror, 0, 1.55, -.2, g);
    for (let k = 0; k < 2; k++) {
      const y = 1.22 + k * .42; box(1.5, .03, .22, LNG.wood, 0, y, -.1, g);
      for (let q = 0; q < 8; q++) { const h = .2 + ((q + k) % 3) * .04; cyl(.035, .035, h, LNG.bottles[(q + k * 3) % 6], -.62 + q * .18, y + .015 + h / 2, -.1, g, 10); }
    }
    box(1.5, .02, .04, CURVE_MAT.glow, 0, 1.2, -.02, g);
    return { w: 1.6, d: .45, tall: true };
  },
  barTaps(g) {                                           // a brass tap tower on the bar top
    box(.5, .04, .16, LNG.brass, 0, 1.12, 0, g); box(.5, .3, .05, LNG.brass, 0, 1.28, 0, g);
    for (let k = 0; k < 4; k++) { box(.03, .12, .03, M.dark, -.18 + k * .12, 1.36, .05, g); box(.04, .06, .06, LNG.bottles[k], -.18 + k * .12, 1.45, .05, g); }
    box(.4, .015, .14, M.slateDark, 0, 1.11, .12, g);
    return { w: .5, d: .2, noBlock: true };
  },
  barStool(g) {
    cyl(.19, .19, .07, LNG.rust, 0, .76, 0, g, 18); cyl(.03, .03, .72, LNG.brass, 0, .38, 0, g, 10);
    const ring = new THREE.Mesh(new THREE.TorusGeometry(.15, .012, 6, 18), LNG.brass); ring.rotation.x = Math.PI / 2; ring.position.y = .3; g.add(ring);
    cyl(.17, .19, .02, M.slateDark, 0, .01, 0, g, 18);
    return { w: .38, d: .38, noBlock: true };
  },
  highTable(g) {                                         // a tall round table by the bar, with two stools
    cyl(.38, .38, .04, LNG.wood, 0, 1.06, 0, g, 24); cyl(.04, .04, 1.04, LNG.brass, 0, .53, 0, g, 10); cyl(.24, .26, .03, M.slateDark, 0, .015, 0, g, 20);
    for (const a of [.6, 3.6]) {
      const x = Math.sin(a) * .55, z = Math.cos(a) * .55;
      cyl(.17, .17, .06, LNG.rust, x, .76, z, g, 16); cyl(.025, .025, .72, LNG.brass, x, .38, z, g, 8);
    }
    cyl(.04, .035, .14, LNG.bottles[2], .1, 1.15, .05, g, 10);
    return { w: .8, d: .8 };
  },
  // ---- Deck 3 mess hall: long tables of eight, round tables of four, the servery line ----
  longTable(g) {                                         // 3.6 m, a bench each side: seats eight
    box(3.6, .06, .9, MESS.top, 0, .74, 0, g);
    box(3.5, .04, .8, M.slateDark, 0, .69, 0, g);
    for (const x of [-1.5, 0, 1.5]) box(.08, .66, .5, M.slateDark, x, .34, 0, g);
    for (const sz of [-.62, .62]) {
      box(3.5, .07, .32, M.wood, 0, .44, sz, g);
      for (const x of [-1.55, 0, 1.55]) box(.07, .41, .26, M.slateDark, x, .2, sz, g);
    }
    for (const x of [-.9, .9]) {                         // condiment caddies
      box(.26, .05, .14, M.slateDark, x, .79, 0, g);
      for (let k = 0; k < 3; k++) cyl(.025, .025, .1, [MESS.food.red, MESS.trays[2], MESS.white][k], x - .08 + k * .08, .86, 0, g, 10);
    }
    box(.42, .02, .3, MESS.trays[0], .4, .78, .22, g); cyl(.04, .035, .09, MESS.white, .55, .83, .2, g, 12);
    return { w: 3.6, d: 1.56 };
  },
  roundTable(g) {                                        // a pedestal table with four chairs
    cyl(.55, .55, .05, MESS.top, 0, .74, 0, g, 28); cyl(.56, .56, .03, M.slateDark, 0, .705, 0, g, 28);
    cyl(.05, .05, .68, M.metal, 0, .36, 0, g, 12); cyl(.3, .32, .03, M.slateDark, 0, .015, 0, g, 20);
    for (let k = 0; k < 4; k++) {
      const a = k * Math.PI / 2 + Math.PI / 4, c = new THREE.Group(); c.position.set(Math.sin(a) * .8, 0, Math.cos(a) * .8); c.rotation.y = a + Math.PI; g.add(c);
      const m = k % 2 ? MESS.chairB : MESS.chair;
      box(.46, .07, .44, m, 0, .46, 0, c); box(.44, .42, .06, m, 0, .74, -.22, c).rotation.x = .08;
      cyl(.03, .03, .4, M.metal, 0, .23, 0, c, 10); cyl(.17, .19, .02, M.slateDark, 0, .01, 0, c, 16);
    }
    cyl(.04, .035, .09, MESS.white, .15, .81, -.1, g, 12);
    return { w: 1.1, d: 1.1 };
  },
  servery(g) {                                           // the hot line: food pans under heat lamps, a sneeze guard, the tray slide
    box(3, .88, .7, WM.steel, 0, .44, 0, g); box(3.04, .05, .74, WM.steelTop, 0, .905, 0, g);
    for (let k = 0; k < 5; k++) {
      const x = -1.2 + k * .6;
      box(.5, .06, .36, M.dark, x, .94, -.05, g); box(.46, .03, .32, MESS.pans[k], x, .965, -.05, g);
      if (k === 1 || k === 4) addSteam(g, x, 1.02, -.05);
    }
    for (const x of [-1.45, 1.45]) cyl(.02, .02, .5, M.metal, x, 1.17, -.05, g, 8);
    box(2.9, .06, .14, M.slateDark, 0, 1.43, -.05, g); box(2.8, .02, .1, MESS.heat, 0, 1.4, -.05, g);
    const gl = box(2.9, .32, .02, M.glass, 0, 1.18, .2, g); gl.rotation.x = -.35; gl.userData.noShadow = true;
    box(3, .04, .22, WM.steelTop, 0, .82, .46, g);
    for (const x of [-1.3, 0, 1.3]) box(.04, .04, .2, M.metal, x, .79, .38, g);
    return { w: 3, d: .9 };
  },
  trayStack(g) {                                         // where the line starts: trays and cutlery
    box(.7, .8, .5, WM.steel, 0, .4, 0, g); box(.72, .04, .52, WM.steelTop, 0, .82, 0, g);
    for (let k = 0; k < 9; k++) box(.48, .02, .34, MESS.trays[k % 3], -.08, .85 + k * .022, -.04, g);
    box(.18, .14, .3, M.slateDark, .24, .91, .02, g);
    for (let k = 0; k < 3; k++) box(.015, .1, .015, M.metal, .2 + k * .04, 1.0, .02, g);
    return { w: .7, d: .5 };
  },
  trayReturn(g) {                                        // a rack for dirty trays, never quite empty
    for (const x of [-.42, .42]) for (const z of [-.24, .24]) cyl(.018, .018, 1.5, M.metal, x, .75, z, g, 8);
    for (let k = 0; k < 6; k++) {
      const y = .15 + k * .24; box(.86, .02, .5, M.metal, 0, y, 0, g);
      if (k > 0 && k !== 3) { box(.46, .02, .34, MESS.trays[k % 3], -.1, y + .02, 0, g); cyl(.035, .03, .08, MESS.white, .12, y + .06, .05, g, 10); }
    }
    return { w: .9, d: .55, tall: true };
  },
  drinksStation(g) {                                     // juice, the tea urn and the cups
    box(1.6, .86, .6, M.slate, 0, .43, 0, g); box(1.64, .05, .64, WM.steelTop, 0, .885, 0, g);
    for (let k = 0; k < 3; k++) {
      const x = -.6 + k * .3;
      box(.22, .12, .22, M.slateDark, x, .97, -.1, g); cyl(.1, .1, .34, MESS.juice[k], x, 1.2, -.1, g, 16); box(.03, .05, .05, M.dark, x, 1.0, .03, g);
    }
    cyl(.14, .15, .44, WM.steel, .45, 1.13, -.08, g, 18); cyl(.06, .06, .05, M.dark, .45, 1.38, -.08, g, 12);
    box(.04, .04, .06, WM.red, .45, 1.0, .08, g);
    for (let k = 0; k < 5; k++) cyl(.04, .035, .06, MESS.white, .72, .93 + k * .045, .12, g, 12);
    return { w: 1.6, d: .6 };
  },
  // open chiller: rolls, fruit and juice for anyone running late. With o.live (Deck 3), the wraps and rolls rows (k = 2, 3) are
  // handed to the galley's galleyShelfRows(g, ys) when section 16 defines it (a function declaration, so it exists at load),
  // and drawn from its stock there; without it they're drawn as before.
  grabShelf(g, o = {}) {
    for (const x of [-.43, .43]) box(.04, 1.85, .6, M.slateDark, x, .925, 0, g);
    box(.9, .06, .6, M.slateDark, 0, 1.82, 0, g); box(.86, 1.7, .03, MESS.chill, 0, .95, -.28, g);
    box(.9, .14, .6, M.slateDark, 0, .07, 0, g);
    const F = MESS.food;
    const live = o.live && typeof galleyShelfRows === 'function';
    for (let k = 0; k < 4; k++) {
      const y = .35 + k * .38; box(.82, .02, .5, M.metal, 0, y, 0, g);
      if (live && k >= 2) continue;
      for (let q = 0; q < 4; q++) {
        const x = -.3 + q * .2;
        if (k === 0) cyl(.035, .035, .16, MESS.juice[q % 3], x, y + .09, .05, g, 10);
        else if (k === 1) soft([F.red, F.green, F.orange, F.red][q], x, y + .05, .06, .045, .045, .045, g);
        else soft(k === 2 ? F.wrap : F.bread, x, y + .05, .04, .08, .04, .05, g);
      }
    }
    box(.86, .12, .04, MESS.heat, 0, 1.68, .29, g);
    if (live) galleyShelfRows(g, [.35 + 2 * .38, .35 + 3 * .38]);   // shelf heights of the wraps and rolls rows, in the shelf's own frame
    return { w: .9, d: .6, tall: true };
  },
  // ---- the galley ----
  ovenStack(g) {                                         // two tall ovens, windows glowing
    for (const x of [-.4, .4]) {
      box(.78, 2.0, .7, WM.steel, x, 1.0, 0, g);
      for (const y of [.62, 1.42]) { box(.66, .62, .02, M.slateDark, x, y, .36, g); box(.42, .3, .02, MESS.ovenWin, x, y + .04, .37, g); box(.5, .03, .04, M.metal, x, y + .27, .39, g); }
      box(.6, .08, .02, WM.screenAmber, x, 1.88, .36, g);
    }
    return { w: 1.6, d: .7, tall: true };
  },
  prepIsland(g) {                                        // the big steel table where everything gets chopped
    box(2.0, .05, .9, WM.steelTop, 0, .9, 0, g); box(1.9, .03, .8, WM.steel, 0, .25, 0, g);
    for (const x of [-.95, .95]) for (const z of [-.4, .4]) box(.05, .9, .05, WM.steel, x, .45, z, g);
    box(.5, .03, .34, M.wood, -.5, .94, .12, g); box(.22, .01, .03, M.metal, -.42, .96, .2, g);
    const F = MESS.food;
    soft(F.red, -.66, .99, .05, .05, .05, .05, g); soft(F.red, -.58, .99, -.02, .045, .045, .045, g);
    soft(F.green, .1, 1.0, -.15, .12, .08, .11, g);
    for (let k = 0; k < 3; k++) { const c = cyl(.025, .018, .22, F.orange, .45 + k * .06, .94, .15, g, 8); c.rotation.z = Math.PI / 2; }
    cyl(.2, .19, .26, WM.steel, .55, 1.06, -.2, g, 20);
    for (const x of [-.5, .3]) cyl(.17, .17, .22, WM.steel, x, .38, 0, g, 18);   // pots on the shelf underneath
    return { w: 2, d: .9 };
  },
  dishPit(g) {                                           // sink, sprayer and the dish machine, always steaming
    box(1.8, .86, .7, WM.steel, 0, .43, 0, g); box(1.84, .05, .74, WM.steelTop, 0, .885, 0, g);
    box(.68, .02, .48, M.dark, -.45, .9, 0, g);
    cyl(.02, .02, .4, M.metal, -.45, 1.1, -.28, g, 8); box(.02, .02, .2, M.metal, -.45, 1.3, -.18, g);
    box(.72, .72, .64, WM.steel, .48, 1.26, 0, g); box(.5, .3, .02, M.dark, .48, 1.3, .33, g); box(.6, .04, .04, M.metal, .48, 1.55, .34, g);
    addSteam(g, .48, 1.7, 0);
    for (let k = 0; k < 6; k++) { const p = cyl(.11, .11, .015, MESS.white, -.2 + k * .035 - .55, 1.03, -.18, g, 18); p.rotation.x = Math.PI / 2 - .1; }
    return { w: 1.8, d: .7 };
  },
  // ---- the cold store ----
  coldShelf(g) {                                         // wire shelving, frosted boxes, a chill in the air
    for (const sx of [-.57, .57]) for (const sz of [-.2, .2]) box(.04, 1.9, .04, M.metal, sx, .95, sz, g);
    const C = [MESS.frost, MESS.ice, KM.label, MESS.frost, KM.crate, MESS.ice];
    for (let k = 0; k < 4; k++) {
      const y = .12 + k * .55; box(1.18, .02, .44, M.metal, 0, y, 0, g);
      for (let q = 0; q < 3; q++) { const h = .2 + ((k + q) % 3) * .06; box(.32, h, .32, C[(k * 3 + q) % C.length], -.38 + q * .38, y + .01 + h / 2, 0, g); box(.34, .015, .34, MESS.frost, -.38 + q * .38, y + h + .02, 0, g); }
    }
    glow('#bfe3ff', .7, 0, 1.6, .25, g, .25);
    return { w: 1.2, d: .45, tall: true };
  },
  chestFreezer(g) {
    box(1.2, .8, .7, MESS.white, 0, .4, 0, g); box(1.22, .06, .72, MESS.frost, 0, .83, 0, g);
    box(.5, .03, .03, M.metal, 0, .74, .36, g); box(.12, .05, .01, WM.screen, .45, .7, .355, g);
    return { w: 1.2, d: .7 };
  },
  spineTrunks(g) {                                       // two air ducts with power conduits between them, floor to ceiling
    for (const x of [-.5, .5]) {
      cyl(.3, .3, H, std('#7f9aa3', .4, .45), x, H / 2, 0, g, 24);
      for (const y of [.1, H / 2, H - .1]) cyl(.36, .36, .07, WM.paintDark, x, y, 0, g, 24);
      box(.42, .14, .03, KM.teal, x, 1.7, .31, g);
    }
    for (const [x, z, m] of [[-.08, -.12, WM.paintGold], [.08, -.12, WM.paintDark], [0, .1, WM.paintGold]]) cyl(.065, .065, H, m, x, H / 2, z, g, 10);
    return { w: 2, d: 1, noBlock: true };
  },
  spineLadder(g) {                                       // the ladder against the car wall, a hole in the deck under it, a cage and a rail
    box(1.0, .03, .78, std('#0b0e12', .9, 0), 0, .016, 0, g);
    for (const [w, d, x, z] of [[1.2, .1, 0, -.44], [1.2, .1, 0, .44], [.1, .98, -.55, 0], [.1, .98, .55, 0]]) box(w, .035, d, WM.hazard, x, .02, z, g);
    for (const x of [-.24, .24]) box(.05, H, .05, WM.steelTop, x, H / 2, -.36, g);
    for (let y = .3; y < H; y += .3) box(.48, .03, .03, WM.steel, 0, y, -.36, g);
    for (let y = 1.0; y < H; y += .5) { const r = new THREE.Mesh(new THREE.TorusGeometry(.36, .02, 6, 20, Math.PI), WM.paintGold); r.rotation.x = Math.PI / 2; r.position.set(0, y, -.36); g.add(r); }
    return { w: 2, d: 1, noBlock: true };
  },
  // Deck 4's spine has room for a trunk junction: a branch duct into the deck, valve wheels and a status box
  trunkJunction(g) {
    box(1.7, .5, .5, std('#7f9aa3', .4, .45), 0, 2.2, -.3, g);
    for (const x of [-.5, .5]) { const v = cyl(.16, .16, .04, WM.red, x, 1.3, .1, g, 18); v.rotation.x = Math.PI / 2; cyl(.04, .04, .4, WM.steel, x, 1.3, -.1, g, 8).rotation.x = Math.PI / 2; }
    box(.5, .8, .3, WM.paintDark, 0, 1.1, -.35, g);
    box(.4, .1, .02, WM.screen, 0, 1.35, -.19, g);
    for (let k = 0; k < 3; k++) box(.06, .06, .02, k === 2 ? WM.screenAmber : WM.screen, -.12 + k * .12, 1.15, -.19, g);
    return { w: 1.8, d: .7, noBlock: true };
  },
  harnessRack(g) {                                       // climbing harnesses and helmets on a free-standing rack, for the ladder
    box(1.2, .06, .06, WM.steel, 0, 1.7, -.05, g);
    for (const x of [-.6, .6]) { box(.05, 1.7, .05, WM.paintDark, x, .85, -.05, g); box(.3, .04, .3, WM.paintDark, x, .02, -.05, g); }
    for (let k = 0; k < 3; k++) {
      const x = -.4 + k * .4;
      box(.04, .12, .04, WM.steel, x, 1.64, 0, g);
      box(.22, .55, .05, [WM.paintGold, KM.teal, WM.paintGold][k], x, 1.3, .03, g);
      soft(KM.label, x, 1.82, .05, .13, .09, .13, g);
    }
    return { w: 1.2, d: .2, noBlock: true };
  },
  travelCase(g, o = {}) {
    const c = GUEST.cases[(o.k || 0) % GUEST.cases.length];
    box(.42, .58, .24, c, 0, .33, 0, g);
    for (const y of [.18, .48]) box(.43, .04, .25, M.slateDark, 0, y, 0, g);
    box(.04, .16, .04, M.metal, -.07, .7, 0, g); box(.04, .16, .04, M.metal, .07, .7, 0, g); box(.18, .03, .05, M.slateDark, 0, .78, 0, g);
    for (const x of [-.15, .15]) cyl(.03, .03, .03, M.dark, x, .03, -.08, g, 8).rotation.z = Math.PI / 2;
    box(.12, .08, .01, KM.label, .1, .4, .125, g);
    return { w: .42, d: .24, noBlock: true };
  },
  floorLamp(g, o = {}) {
    cyl(.16, .18, .03, M.slateDark, 0, .015, 0, g, 18); cyl(.02, .02, 1.5, M.metal, 0, .76, 0, g, 8);
    const sh = new THREE.Mesh(new THREE.CylinderGeometry(.14, .22, .26, 20, 1, true), std('#e9dcc0', .8, 0, { side: THREE.DoubleSide, emissive: col('#ffcf8a'), emissiveIntensity: .35 }));
    sh.position.y = 1.55; g.add(sh);
    glow('#ffd59a', 1.0, 0, 1.5, 0, g, .5);
    if (o.light) addLamp(g, 0, 1.4, 0, 4.5, .4, 1.6);
    return { w: .4, d: .4, noBlock: true };
  },
  // ---- Deck 6: the engine room ----
  // a drive coil: copper windings round a glowing core, in a steel cage on a plinth, with a conduit to the deckhead.
  // The core's glow breathes (PULSES); o.ph sets its phase, so a row of coils cycles one after another.
  driveCoil(g, o = {}) {
    const core = std('#ffb35c', .35, 0, { emissive: col('#f08a2c'), emissiveIntensity: 1 });
    cyl(1.0, 1.08, .22, ENG.plinth, 0, .11, 0, g, 28);
    const band = new THREE.Mesh(new THREE.TorusGeometry(1.02, .035, 6, 36), WM.paintGold); band.rotation.x = Math.PI / 2; band.position.y = .23; g.add(band);
    cyl(.42, .42, 1.9, core, 0, 1.17, 0, g, 20).userData.noMerge = true;   // kept out of the fade's material copies, so it keeps pulsing
    for (let k = 0; k < 7; k++) { const r = new THREE.Mesh(new THREE.TorusGeometry(.6, .085, 8, 28), ENG.copper); r.rotation.x = Math.PI / 2; r.position.y = .45 + k * .26; r.castShadow = true; g.add(r); }
    for (let k = 0; k < 4; k++) { const a = k * Math.PI / 2 + Math.PI / 4; box(.06, 2.14, .06, WM.steel, Math.sin(a) * .78, 1.28, Math.cos(a) * .78, g); }
    cyl(.8, .8, .16, ENG.housing, 0, 2.4, 0, g, 28);
    cyl(.18, .18, H - 2.46, ENG.housing, 0, (2.46 + H) / 2, 0, g, 12);
    const s = glow('#ffb066', 2.6, 0, 1.2, 0, g, .3);
    PULSES.push({ m: core, key: 'emissiveIntensity', base: .6, amp: .9, w: 1.4, ph: o.ph || 0 }, { m: s.material, key: 'opacity', base: .12, amp: .3, w: 1.4, ph: o.ph || 0 });
    return { w: 2.16, d: 2.16, tall: true };
  },
  // the drive housing across the stern: a ribbed block with the drive's glowing mouth in the middle. Kit x runs along it.
  driveHousing(g, o = {}) {
    const w = o.w || 8.6, mouth = std('#ffc27a', .35, 0, { emissive: col('#f08a2c'), emissiveIntensity: 1 });
    box(w, 2.1, .8, ENG.housing, 0, 1.05, 0, g);
    box(w + .1, .14, .9, WM.paintDark, 0, 2.15, 0, g);
    for (let x = -w / 2 + .4; x <= w / 2 - .3; x += .9) box(.1, 2.0, .86, WM.steel, x, 1.0, 0, g);
    box(w, .1, .04, WM.hazard, 0, .05, .44, g);
    const ring = new THREE.Mesh(new THREE.TorusGeometry(.75, .12, 10, 32), WM.steelTop); ring.position.set(0, 1.1, .45); g.add(ring);
    cyl(.66, .66, .06, mouth, 0, 1.1, .42, g, 28).rotation.x = Math.PI / 2;
    for (const x of [-w / 2 + 1.4, w / 2 - 1.4]) cyl(.32, .32, .06, ENG.copper, x, 1.3, .43, g, 20).rotation.x = Math.PI / 2;
    PULSES.push({ m: mouth, key: 'emissiveIntensity', base: .5, amp: .6, w: .7, ph: 0 });
    return { w, d: .9 };
  },
  // a horizontal pipe along kit x at height o.y, for feeds between the drive and the coils
  pipeRun(g, o = {}) {
    const w = o.w || 1, r = o.r || .14;
    cyl(r, r, w, ENG.copper, 0, o.y || 2.4, 0, g, 12).rotation.z = Math.PI / 2;
    return { w, d: r * 2, noBlock: true };
  },
  // a raised catwalk along kit x: a steel deck on legs, gold rails both sides
  catwalk(g, o = {}) {
    const w = o.w || 4, d = .8, y = .38;
    box(w, .06, d, ENG.walk, 0, y - .03, 0, g);
    for (let x = -w / 2 + .3; x < w / 2; x += 1.2) for (const z of [-.3, .3]) box(.08, y - .04, .08, WM.paintDark, x, (y - .04) / 2, z, g);
    for (const z of [-d / 2 + .03, d / 2 - .03]) {
      box(w, .04, .04, WM.paintGold, 0, y + .95, z, g); box(w, .03, .03, WM.paintGold, 0, y + .5, z, g);
      for (let x = -w / 2 + .05; x < w / 2; x += 1) box(.04, .95, .04, WM.paintGold, x, y + .47, z, g);
      box(.04, .95, .04, WM.paintGold, w / 2 - .05, y + .47, z, g);
    }
    return { w, d };
  },
  // a rail along a window, waist high, on posts about a metre apart. Kit x runs along it; walkers pass right by it.
  overlookRail(g, o = {}) {
    const w = o.w || 3, n = Math.max(1, Math.round(w));
    cyl(.025, .025, w, WM.steelTop, 0, 1.05, 0, g, 10).rotation.z = Math.PI / 2;
    box(w, .03, .03, WM.steel, 0, .55, 0, g);
    for (let k = 0; k <= n; k++) box(.05, 1.05, .05, WM.steel, -w / 2 + .03 + (w - .06) * k / n, .525, 0, g);
    return { w, d: .1, noBlock: true };
  },
  // the reactor: a ribbed shield drum on a plinth, a band of ports glowing green, the core showing through a ring
  // on top, conduits to the deckhead, and the coolant loop round it all on short stands. Its glow breathes slowly.
  reactorDrum(g, o = {}) {
    const loop = o.loop || 3.0, core = std('#4fbf7f', .3, 0, { emissive: col('#2fbf6f'), emissiveIntensity: 1 });
    cyl(2.3, 2.4, .3, ENG.plinth, 0, .15, 0, g, 40);
    const band = new THREE.Mesh(new THREE.TorusGeometry(2.32, .05, 6, 48), WM.paintGold); band.rotation.x = Math.PI / 2; band.position.y = .31; g.add(band);
    cyl(2.0, 2.0, 2.2, ENG.shield, 0, 1.38, 0, g, 40);
    for (let k = 0; k < 16; k++) { const a = k * Math.PI / 8; box(.12, 2.2, .14, ENG.housing, Math.sin(a) * 2.02, 1.38, Math.cos(a) * 2.02, g).rotation.y = a; }
    for (let k = 0; k < 8; k++) { const a = k * Math.PI / 4 + Math.PI / 16; box(.34, .14, .06, core, Math.sin(a) * 2.03, 1.55, Math.cos(a) * 2.03, g).rotation.y = a; }
    cyl(2.1, 2.1, .14, ENG.housing, 0, 2.53, 0, g, 40);
    cyl(1.2, 1.2, .06, core, 0, 2.61, 0, g, 32);
    const rim = new THREE.Mesh(new THREE.TorusGeometry(1.25, .07, 8, 32), WM.steelTop); rim.rotation.x = Math.PI / 2; rim.position.y = 2.62; g.add(rim);
    for (const [x, z] of [[.9, 0], [-.45, .78], [-.45, -.78]]) cyl(.16, .16, H - 2.56, ENG.housing, x, (2.56 + H) / 2, z, g, 12);
    const lp = new THREE.Mesh(new THREE.TorusGeometry(loop, .16, 10, 64), ENG.pipe); lp.rotation.x = Math.PI / 2; lp.position.y = .75; lp.castShadow = true; g.add(lp);
    for (let k = 0; k < 8; k++) {
      const a = k * Math.PI / 4; box(.12, .62, .12, WM.paintDark, Math.sin(a) * loop, .31, Math.cos(a) * loop, g);
      if (k % 2 === 0) { cyl(.12, .12, loop - 2.0, ENG.pipe, Math.sin(a) * (loop + 2.0) / 2, .75, Math.cos(a) * (loop + 2.0) / 2, g, 10).quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), new THREE.Vector3(Math.sin(a), 0, Math.cos(a))); }   // spokes from the drum to the loop
    }
    const s = glow('#7dffb0', 2.4, 0, 2.9, 0, g, .3);
    PULSES.push({ m: core, key: 'emissiveIntensity', base: .7, amp: .5, w: .45, ph: 0 }, { m: s.material, key: 'opacity', base: .15, amp: .2, w: .45, ph: 0 });
    return { w: (loop + .2) * 2, d: (loop + .2) * 2, tall: true };
  },
  // engine control's board: a long desk with a sloped face of screens and switches. Kit x runs along it; operators sit on +z.
  controlBoard(g, o = {}) {
    const w = o.w || 3.4;
    box(w, .72, .6, ENG.console, 0, .36, -.05, g);
    const top = box(w, .06, .5, ENG.console, 0, .82, -.02, g); top.rotation.x = .35;
    for (let x = -w / 2 + .35; x < w / 2 - .2; x += .7) {
      const sc = box(.5, .02, .3, (Math.round((x + w) * 10) % 3) ? WM.screen : WM.screenAmber, x, .86, -.04, g); sc.rotation.x = .35;
      for (let k = 0; k < 3; k++) box(.05, .03, .05, k === 1 ? WM.red : WM.navGreen, x - .12 + k * .12, .79, .18, g).rotation.x = .35;
    }
    box(w, .45, .06, ENG.console, 0, 1.08, -.31, g);
    return { w, d: .7 };
  },
  // a coolant riser: a lagged pipe floor to deckhead with a valve wheel, a gauge, and a wisp of steam at a joint
  coolantRiser(g) {
    cyl(.16, .16, H, ENG.pipe, 0, H / 2, 0, g, 14);
    for (const y of [.3, 1.4, 2.5]) cyl(.21, .21, .1, ENG.housing, 0, y, 0, g, 14);
    const wheel = new THREE.Mesh(new THREE.TorusGeometry(.16, .025, 6, 18), WM.red); wheel.position.set(0, 1.15, .3); g.add(wheel);
    box(.05, .05, .14, WM.steel, 0, 1.15, .22, g);
    cyl(.07, .07, .04, M.trim, 0, 1.65, .19, g, 16).rotation.x = Math.PI / 2;
    addSteam(g, 0, 2.55, .22);
    return { w: .45, d: .45, tall: true };
  },
};
// wall-mounted pieces: built against a wall, origin on the wall's inner face, front toward +z
const WALL_KIT = {
  mimicPanel(g) {                                        // engine control's map of the ship's power
    box(3.1, 1.06, .04, M.slateDark, 0, 1.75, .02, g);
    const p = new THREE.Mesh(new THREE.PlaneGeometry(3.0, 1.0), ENG.mimic); p.position.set(0, 1.75, .045); g.add(p);
  },
  heater(g) {                                            // a panel heater nobody needs, down here
    box(.9, .55, .08, M.trim, 0, .45, .04, g);
    for (let k = 0; k < 6; k++) box(.1, .5, .03, M.slate, -.375 + k * .15, .45, .095, g);
    box(.9, .04, .1, M.slateDark, 0, .745, .05, g);
  },
  logShelf(g) {                                          // a short shelf of old engine logs in grey and gold binders
    box(.8, .04, .24, M.wood, 0, 1.5, .12, g);
    for (let k = 0; k < 8; k++) box(.07, .26 + (k % 3) * .02, .2, k % 3 ? WM.paintDark : WM.paintGold, -.32 + k * .08, 1.65 + (k % 3) * .01, .12, g);
  },
  trefoil(g) {                                           // a radiation sign
    box(.42, .42, .03, M.slateDark, 0, 1.6, .015, g);
    const p = new THREE.Mesh(new THREE.PlaneGeometry(.38, .38), ENG.trefoil); p.position.set(0, 1.6, .035); g.add(p);
  },
  notices(g) {
    box(1.0, .7, .04, KM.cork, 0, 1.5, .03, g); box(1.06, .76, .03, M.slateDark, 0, 1.5, .015, g);
    [[-.3, 1.62, KM.paper, 0.1], [.05, 1.66, KM.note, -.08], [.32, 1.55, KM.paper, .05], [-.25, 1.36, KM.note, .12], [.12, 1.38, KM.paper, -.04]]
      .forEach(([x, y, m, r]) => { box(.24, .3, .01, m, x, y, .055, g).rotation.z = r; box(.03, .03, .02, KM.red, x, y + .13, .062, g); });
  },
  towels(g) {
    box(.9, .03, .03, M.metal, 0, 1.35, .06, g);
    [['teal', -.3], ['gold', 0], ['red', .3]].forEach(([c, x]) => box(.24, .55, .03, KM[c], x, 1.08, .075, g));
  },
  shelf(g) {
    box(1.7, .05, .26, M.wood, 0, 1.72, .13, g);
    [[-.73, .3, '#b4553f'], [-.63, .26, '#d9c79b'], [-.55, .33, '#3f6e8c'], [-.47, .28, '#e3dfd2'], [-.39, .24, '#56466a']].forEach(([x, h, c]) => box(.07, h, .2, std(c, .8), x, 1.745 + h / 2, .13, g));
    const wren = new THREE.Group(); wren.position.set(.3, 1.86, .13); g.add(wren);
    const hull = cyl(.035, .05, .42, M.trim, 0, 0, 0, wren, 16); hull.rotation.z = Math.PI / 2;
    box(.12, .015, .2, M.trim, -.02, 0, 0, wren);
    [-1, 1].forEach(s => { const pod = cyl(.022, .022, .22, M.slate, -.08, .02, s * .11, wren, 12); pod.rotation.z = Math.PI / 2; });
    glow('#5fd6c6', .12, .21, 0, 0, wren, .9);
    box(.18, .1, .12, M.slateDark, .3, 1.795, .13, g); box(.1, .2, .1, std('#56463a', .9), .7, 1.845, .13, g);
  },
  samples(g) {
    box(1.3, .05, .28, M.wood, 0, 1.6, .14, g);
    [['#5fe0cf', -.5], ['#ffb35c', -.2], ['#b88cff', .1], ['#8fe07a', .4]].forEach(([c, x]) => {
      cyl(.05, .05, .1, std(c, .3, 0, { emissive: col(c), emissiveIntensity: 1.4 }), x, 1.68, .14, g, 16);
      cyl(.065, .065, .2, M.glass, x, 1.725, .14, g, 16).userData.noShadow = true;
      cyl(.07, .07, .03, M.metal, x, 1.84, .14, g, 16);
      glow(c, .45, x, 1.72, .2, g, .55);
    });
    const rock = new THREE.Mesh(new THREE.DodecahedronGeometry(.08), std('#7d7468', .9)); rock.position.set(.62, 1.68, .14); g.add(rock);
  },
  // soundproofing: fabric squares in four colours
  acoustic(g, o = {}) {
    for (let r = 0; r < 3; r++) for (let c = 0; c < 2; c++) box(.42, .42, .05, MUS.fab[(r + c + (o.k || 0)) % 4], c ? .23 : -.23, 1.05 + r * .45, .03, g);
  },
  // a rail of instruments on hooks: ukulele, violin and bow, tambourine
  instrumentHooks(g) {
    box(1.3, .06, .05, M.wood, 0, 1.95, .03, g);
    soft(MUS.spruce, -.42, 1.45, .08, .1, .12, .035, g); soft(MUS.spruce, -.42, 1.62, .08, .075, .09, .035, g); box(.035, .3, .02, MUS.rosewood, -.42, 1.82, .08, g);
    soft(MUS.violin, 0, 1.42, .08, .11, .12, .035, g); soft(MUS.violin, 0, 1.62, .08, .09, .1, .035, g); box(.03, .26, .02, M.dark, 0, 1.82, .08, g);
    box(.012, .7, .012, MUS.rosewood, .14, 1.58, .07, g).rotation.z = -.2;
    const tam = new THREE.Group(); tam.position.set(.43, 1.62, .07); tam.rotation.x = Math.PI / 2; g.add(tam);
    cyl(.13, .13, .05, M.wood, 0, 0, 0, tam, 20); cyl(.118, .118, .062, M.cream, 0, 0, 0, tam, 20);
    for (let q = 0; q < 4; q++) { const a = q * 1.571 + .4; box(.04, .015, .04, MUS.brass, Math.sin(a) * .13, 0, Math.cos(a) * .13, tam); }
  },
  readingLamp(g) { box(.16, .1, .1, M.trim, 0, 1.4, .05, g); glow('#ffcf8a', .5, 0, 1.37, .14, g, .7); },
  herbWall(g) {                                          // pockets of herbs for the galley, under a little label
    box(1.6, 1.3, .06, GD.post, 0, 1.35, .03, g);
    for (let r = 0; r < 4; r++) for (let k = 0; k < 5; k++) {
      const x = -.6 + k * .3, y = .85 + r * .32;
      box(.24, .1, .1, GD.bed, x, y, .1, g); leaf(GD.leaves[(r + k) % 5], x, y + .1, .12, .1, .09 + ((r * k) % 3) * .02, .07, g);
    }
    box(.5, .08, .02, MED.paper, 0, 2.08, .07, g);
  },
  gymMirror(g) { box(1.9, 1.6, .04, M.slateDark, 0, 1.25, .02, g); box(1.8, 1.5, .02, GYM.mirror, 0, 1.25, .045, g); },
  clocks(g) {                                            // three clocks: ship time, home time, and the message delay
    box(1.5, .5, .04, M.slateDark, 0, 1.85, .02, g);
    [['SHIP', '#5fd6c6'], ['HOME', '#e8c06a'], ['DELAY', '#c86b4a']].forEach(([t, c], k) => {
      const x = -.48 + k * .48; cyl(.17, .17, .03, MED.white, x, 1.9, .05, g, 20).rotation.x = Math.PI / 2;
      box(.02, .12, .01, std(c, .5), x, 1.94, .07, g); box(.09, .02, .01, M.dark, x + .04, 1.9, .07, g);
    });
  },
  msgBoard(g) {                                          // the message queue: who has something waiting
    const t = tex(256, 160, (c, w, h) => {
      c.fillStyle = '#0d1a1f'; c.fillRect(0, 0, w, h);
      c.fillStyle = '#e8c06a'; c.font = '700 18px system-ui,sans-serif'; c.fillText('MESSAGES WAITING', 14, 28);
      c.font = '500 14px system-ui,sans-serif';
      [['Vance', 'home, 2 new'], ['Rina', 'sister, 1 new'], ['Pell', 'mum, 3 new'], ['You', 'none yet']].forEach(([n, x], k) => {
        c.fillStyle = k === 3 ? '#7fa9a3' : '#e8f4f1'; c.fillText(n, 14, 58 + k * 24); c.fillStyle = '#9fd9cf'; c.fillText(x, 100, 58 + k * 24);
      });
    });
    const p = new THREE.Mesh(new THREE.PlaneGeometry(.9, .56), new THREE.MeshBasicMaterial({ map: t, toneMapped: false })); p.position.set(0, 1.6, .045); g.add(p);
    box(.96, .62, .04, M.slateDark, 0, 1.6, .02, g);
  },
  menuBoard(g) {                                         // the mess hall's board: two meals, and today's
    const t = tex(320, 200, (c, w, h) => {
      c.fillStyle = '#1d2a2a'; c.fillRect(0, 0, w, h);
      c.fillStyle = '#e8c06a'; c.font = '700 24px system-ui,sans-serif'; c.fillText('MESS', 18, 34);
      c.fillStyle = '#9fd9cf'; c.font = '600 15px system-ui,sans-serif'; c.fillText('Breakfast  06:00 - 09:00', 18, 66); c.fillText('Dinner  17:00 - 20:30', 18, 90);
      c.fillStyle = '#e8eef0'; c.font = '500 15px system-ui,sans-serif';
      ['Today: Brennan\'s spiced lentils', 'Fresh rolls, garden greens', 'Grab & go by the line'].forEach((l, k) => c.fillText(l, 18, 126 + k * 24));
      c.fillStyle = '#c86b4a'; c.fillRect(18, 186, 60, 3);
    });
    const p = new THREE.Mesh(new THREE.PlaneGeometry(1.2, .75), new THREE.MeshBasicMaterial({ map: t, toneMapped: false })); p.position.set(0, 1.78, .045); g.add(p);
    box(1.28, .83, .04, M.slateDark, 0, 1.78, .02, g);
  },
  passShelf(g, o = {}) {                                  // the serving counter's top, through the wall, with a heat lamp over it
    box(.86, .05, T + .44, WM.steelTop, 0, SILL + .025, -T / 2, g);
    box(.8, .05, .1, M.slateDark, 0, 2.13, -T / 2, g); box(.74, .02, .07, MESS.heat, 0, 2.1, -T / 2, g);
    if (o.plate) { cyl(.12, .1, .03, MESS.white, -.15, SILL + .065, -T / 2 + .05, g, 18); soft(MESS.pans[o.plate % 5], -.15, SILL + .09, -T / 2 + .05, .07, .03, .07, g); }
  },
  poster(g, o = {}) {
    const p = new THREE.Mesh(new THREE.PlaneGeometry(.8, 1.12), new THREE.MeshStandardMaterial({ map: o.tex || posterTex, roughness: .8 }));
    p.position.set(0, 1.55, .045); g.add(p);
    box(.86, 1.18, .04, M.slateDark, 0, 1.55, .02, g);
  },
  comm(g) {
    box(.36, .5, .06, M.slateDark, 0, 1.35, .03, g);
    box(.26, .32, .02, std('#123b3e', .3, 0, { emissive: col('#1e6a66'), emissiveIntensity: .8 }), 0, 1.38, .07, g);
    glow('#5fd6c6', .6, 0, 1.38, .12, g, .25);
  },
  sconce(g) {
    box(.22, .3, .08, M.trim, 0, 1.9, .04, g);
    glow('#ffcf8a', .9, 0, 1.95, .12, g, .55);
  },
  workLight(g) {
    box(.56, .07, .12, M.slateDark, 0, 2.05, .06, g);
    box(.5, .03, .08, WM.lightStrip, 0, 2.01, .07, g);
    glow('#d8f0ff', .8, 0, 1.98, .14, g, .35);
  },
  plate(g, o) {
    const t = tex(256, 64, (c, w, h) => {
      c.fillStyle = '#0f2a2c'; c.fillRect(0, 0, w, h); c.strokeStyle = '#5fd6c6'; c.lineWidth = 3; c.strokeRect(4, 4, w - 8, h - 8);
      c.fillStyle = '#c5f4ec'; c.font = '600 26px system-ui,sans-serif'; c.textAlign = 'center'; c.fillText(o.text, w / 2, 42);
    });
    const p = new THREE.Mesh(new THREE.PlaneGeometry(.64, .16), new THREE.MeshBasicMaterial({ map: t, toneMapped: false }));
    p.position.set(0, 1.85, .045); g.add(p); box(.68, .2, .04, M.slateDark, 0, 1.85, .02, g);
  },
  // the Works job board: home of the shared job list. Its cards are the deck's until section 17 draws the live list.
  jobBoard(g, o = {}) {
    const cards = o.cards || [];
    const t = tex(640, 300, (c, w, h) => {
      c.fillStyle = '#0c1a1f'; c.fillRect(0, 0, w, h);
      c.fillStyle = '#e8c06a'; c.font = '700 26px system-ui,sans-serif'; c.fillText('WORKS  ·  JOB BOARD', 22, 40);
      c.fillStyle = '#7fa9a3'; c.font = '500 17px system-ui,sans-serif'; c.textAlign = 'right'; c.fillText(cards.length + ' open  ·  day shift', w - 22, 40); c.textAlign = 'left';
      c.fillStyle = 'rgba(95,214,198,.35)'; c.fillRect(22, 54, w - 44, 2);
      cards.forEach(([title, where, state, pri], k) => {
        const x = 22 + (k % 2) * 304, y = 70 + Math.floor(k / 2) * 74;
        c.fillStyle = '#16303a'; c.fillRect(x, y, 292, 62);
        c.fillStyle = { urgent: '#e0503f', soon: '#e8c06a', routine: '#5fd6c6' }[pri] || '#5fd6c6'; c.fillRect(x, y, 7, 62);
        c.fillStyle = '#e8f4f1'; c.font = '600 20px system-ui,sans-serif'; c.fillText(title, x + 18, y + 26);
        c.fillStyle = '#93b8b2'; c.font = '500 15px system-ui,sans-serif'; c.fillText(where + '  ·  ' + state, x + 18, y + 49);
      });
    });
    if (typeof jobBoardLive === 'function') jobBoardLive(t);   // section 17 keeps it up to date with the real job list
    const p = new THREE.Mesh(new THREE.PlaneGeometry(2.6, 1.22), new THREE.MeshBasicMaterial({ map: t, toneMapped: false }));
    p.position.set(0, 1.55, .075); g.add(p);                 // the frame's face is at .065
    box(2.74, 1.36, .07, WM.paintDark, 0, 1.55, .03, g);
    box(2.74, .05, .1, WM.paintGold, 0, 2.25, .05, g);
    glow('#5fd6c6', 2.2, 0, 1.55, .2, g, .12);
  },
  // pegboard of tools with painted outlines, one of them missing
  toolWall(g) {
    const p = new THREE.Mesh(new THREE.PlaneGeometry(1.8, 1.0), WM.toolBoard); p.position.set(0, 1.5, .05); g.add(p);
    box(1.88, 1.08, .05, WM.paintDark, 0, 1.5, .02, g);
    box(1.9, .05, .2, WM.steel, 0, .98, .1, g);                                    // little shelf of tins under it
    for (const [x, m] of [[-.7, KM.label], [-.55, WM.bottleGrey], [.62, KM.teal]]) cyl(.05, .05, .12, m, x, 1.07, .12, g, 12);
  },
  carPanel(g) {
    box(.34, .66, .05, M.slateDark, 0, 1.3, .025, g);
    box(.24, .1, .02, WM.screen, 0, 1.55, .055, g);
    const btn = std('#e8c06a', .3, 0, { emissive: col('#e8c06a'), emissiveIntensity: .6 });
    for (let k = 0; k < 6; k++) box(.07, .07, .02, btn, -.06 + (k % 2) * .12, 1.4 - Math.floor(k / 2) * .11, .055, g);
  },
  handrail(g) {
    const r = cyl(.025, .025, .9, WM.steelTop, 0, .95, .09, g, 10); r.rotation.z = Math.PI / 2;
    for (const x of [-.4, .4]) box(.03, .03, .08, WM.steel, x, .95, .045, g);
  },
  // the deck directory by the lift: every deck, top to bottom (the rec deck's R row while it's on, 0.84.0)
  deckDirectory(g) {
    const t = tex(200, 260, (c, w, h) => {
      c.fillStyle = '#0d1a1f'; c.fillRect(0, 0, w, h);
      c.fillStyle = '#e8c06a'; c.font = '700 20px system-ui,sans-serif'; c.fillText('CSV WREN', 16, 30);
      const rows = [['1', 'Bridge'], ['2', 'Command & Science'], ['3', 'Commons'], ['4', 'Quarters'], ['5', 'Operations'], ['6', 'Engineering']], dy = REC_DECK ? 27 : 32;
      if (REC_DECK) rows.splice(4, 0, ['R', 'Recreation']);   // 0.84.0 (rec engineer B): the rec deck's row, between 4 and 5
      rows.forEach(([n, name], k) => {
        const y = 62 + k * dy, here = n === deckLabel(deckDef.num);
        if (here) { c.fillStyle = 'rgba(95,214,198,.18)'; c.fillRect(8, y - (REC_DECK ? 19 : 21), w - 16, REC_DECK ? 25 : 29); }
        c.fillStyle = here ? '#5fd6c6' : '#e8c06a'; c.font = '700 17px system-ui,sans-serif'; c.fillText(n, 16, y);
        c.fillStyle = here ? '#e8f4f1' : '#a9c4bf'; c.font = '500 15px system-ui,sans-serif'; c.fillText(name, 38, y);
      });
      c.fillStyle = '#7fa9a3'; c.font = '500 12px system-ui,sans-serif'; c.fillText('You are on ' + (deckDef.num === 7 ? 'the Recreation Deck' : deckWord(deckDef.num)), 16, h - 12);
    });
    const p = new THREE.Mesh(new THREE.PlaneGeometry(.6, .78), new THREE.MeshBasicMaterial({ map: t, toneMapped: false })); p.position.set(0, 1.45, .045); g.add(p);
    box(.66, .84, .04, M.slateDark, 0, 1.45, .02, g);
  },
  liftPanel(g) {
    box(.18, .3, .05, M.slateDark, 0, 1.25, .025, g);
    for (const y of [1.32, 1.2]) box(.07, .07, .02, std('#e8c06a', .3, 0, { emissive: col('#e8c06a'), emissiveIntensity: .7 }), 0, y, .06, g);
  },
};

// 0.47.5: the weight bench's bar: hidden (scaled to nothing) for half a second after anyone presses it (ACTS.bench); dx centres the held bar between the hands
const BENCH_BAR = { g: null, t: -1e9, dx: .3, rz: .42 };   // rz: the grip's spread, undone so the bar lies level
// ---- placing things ----
const FACING = { n: 0, w: Math.PI / 2, e: -Math.PI / 2, s: Math.PI };   // which wall the back of a piece is against
// place a floor piece in room-local units (0,0 = room's top-left corner)
function place(roomKey, kind, lx, lz, back = 'n', o = {}) {
  const b = ROOM_BOX[roomKey], g = new THREE.Group();
  g.position.set(X0(b.i0) + lx, 0, Z0(b.j0) + lz); g.rotation.y = (FACING[back] || 0) + (o.turn || 0); staticRoot.add(g);
  const fp = KIT[kind](g, o);
  if (fp.tall && !NO_FADE.has(roomKey)) {
    const fk = o.fadeGroup || roomKey;                   // a room fades as one, unless pieces name their own group (storage aisles)
    let t = TALL_BY_ROOM[fk];
    if (!t) { t = TALL_BY_ROOM[fk] = { g: new THREE.Group(), pts: [], o: 1 }; deckRoot.add(t.g); TALL.push(t); }
    staticRoot.remove(g); t.g.add(g); t.pts.push({ x: g.position.x, z: g.position.z, w: Math.max(fp.w, fp.d) });
  }
  // block the tiles under the footprint
  const sw = (back === 'w' || back === 'e') ? fp.d : fp.w, sd = (back === 'w' || back === 'e') ? fp.w : fp.d;
  if (!fp.noBlock && !o.noBlock) {
    const box = o.snug && [g.position.x - sw / 2, g.position.x + sw / 2, g.position.z - sd / 2, g.position.z + sd / 2];
    for (let j = 0; j < D; j++) for (let i = 0; i < W; i++) {
      const cx = X0(i) + .5, cz = Z0(j) + .5;
      if (Math.abs(cx - g.position.x) <= sw / 2 + .08 && Math.abs(cz - g.position.z) <= sd / 2 + .08) {
        BLOCKED.add(i + ',' + j);
        if (box) { const k = i + ',' + j; SNUG.set(k, (SNUG.get(k) || []).concat([box])); }
      }
    }
  }
  for (const k of (o.block || [])) BLOCKED.add((b.i0 + k[0]) + ',' + (b.j0 + k[1]));
  if (o.it) {
    const hit = new THREE.Mesh(new THREE.BoxGeometry(fp.w, o.hitH || 1.2, fp.d), HIT_MAT);
    hit.position.y = (o.hitH || 1.2) / 2; hit.userData.noMerge = true; g.add(hit);
    ITEMS.push({ ...o.it, hit, g, front: FACING[back] + (o.turn || 0), depth: fp.d });
  }
  return g;
}
// place a wall piece on the inner face of a wall: room-local position along that wall
function placeWall(roomKey, kind, wall, along, o = {}) {
  const b = ROOM_BOX[roomKey], g = new THREE.Group();
  let x, z, key;
  if (wall === 'n') { x = X0(b.i0) + along; z = Z0(b.j0) + T / 2; key = `h,${b.i0 + Math.floor(along)},${b.j0}`; }
  if (wall === 's') { x = X0(b.i0) + along; z = Z0(b.j1 + 1) - T / 2; key = `h,${b.i0 + Math.floor(along)},${b.j1 + 1}`; }
  if (wall === 'w') { x = X0(b.i0) + T / 2; z = Z0(b.j0) + along; key = `v,${b.i0},${b.j0 + Math.floor(along)}`; }
  if (wall === 'e') { x = X0(b.i1 + 1) - T / 2; z = Z0(b.j0) + along; key = `v,${b.i1 + 1},${b.j0 + Math.floor(along)}`; }
  g.position.set(x, 0, z); g.rotation.y = FACING[wall]; deckRoot.add(g);
  WALL_KIT[kind](g, o);
  const e = EDGES.get(o.edge || key);
  WALL_DECOR.push({ g, e });
  if (o.it) {
    const hit = new THREE.Mesh(new THREE.BoxGeometry(o.hitW || .9, 1.2, .3), HIT_MAT); hit.position.set(0, 1.5, .15); hit.userData.noMerge = true; g.add(hit);
    ITEMS.push({ ...o.it, hit, g, front: FACING[wall], depth: .1, wall: true });
  }
  return g;
}
function placeOnEdge(kind, key, toward, o = {}) {        // a wall piece on an edge, facing the side named by toward
  const e = EDGES.get(key); if (!e) return;
  const [k, a, b] = key.split(','), i = +a, j = +b, g = new THREE.Group();
  if (k === 'h') { g.position.set(X0(i) + .5, 0, Z0(j) + (toward === 's' ? T / 2 : -T / 2)); g.rotation.y = toward === 's' ? 0 : Math.PI; }
  else { g.position.set(X0(i) + (toward === 'e' ? T / 2 : -T / 2), 0, Z0(j) + .5); g.rotation.y = toward === 'e' ? Math.PI / 2 : -Math.PI / 2; }
  deckRoot.add(g); WALL_KIT[kind](g, o); WALL_DECOR.push({ g, e });
  if (o.it) {                                            // tappable, like placeWall's pieces
    const hit = new THREE.Mesh(new THREE.BoxGeometry(o.hitW || .9, 1.2, .3), HIT_MAT); hit.position.set(0, 1.5, .15); hit.userData.noMerge = true; g.add(hit);
    ITEMS.push({ ...o.it, hit, g, front: g.rotation.y, depth: .1, wall: true });
  }
}

// =====================================================================
// ROOM CONTENTS (room-local units; inner wall faces sit 0.1 in from tile edges)
// =====================================================================
const rugCabin = makeRug(['#2c375e', '#d0a04b', '#e9dfc7', '#3c9a92']);
const rugLounge = makeRug(['#6b2f3a', '#e9c46a', '#efe3c8', '#2a9d8f']);
const rugBunk = makeRug(['#2f4a3e', '#c9a46a', '#e3dccb', '#7a5aa8']);
const rugSato = makeRug(['#3b3550', '#8fbf9a', '#e9e1d0', '#c86b4a']);
const IT = (t, x) => ({ t, x });
// Deck 4's guest and spare cabins (0.14.0)
const GUEST = {
  cases: ['#6b2f3a', '#2c4a6e', '#3f6b4f', '#8a6446'].map(c => std(c, .55, .1)),
  sheet: std('#f2efe6', .9), towel: std('#9fcfd6', .95), ticking: std('#c9cfd6', .9),
};
const LNG = {
  navy: std('#2c3a5e', .9), rust: std('#b4553f', .9), olive: std('#6b6a3a', .9), cream: std('#e9dfc7', .9),
  wood: std('#5a3a28', .55), brass: std('#c9a24a', .35, .75), mirror: std('#8fa7ad', .1, .3, { emissive: col('#2c3a40'), emissiveIntensity: .5 }),
  bottles: ['#3f7a5a', '#b4553f', '#e9c46a', '#6a8aa6', '#7a5aa8', '#d9e6e0'].map(c => std(c, .15, .1, { transparent: true, opacity: .85, emissive: col(c), emissiveIntensity: .25 })),
  shade: std('#e9dcc0', .8, 0, { emissive: col('#ffcf8a'), emissiveIntensity: .5 }),
};
const MESS = {
  top: std('#ece4d4', .45), chair: std('#d96a2e', .6), chairB: std('#2a9d8f', .6),
  pans: ['#e9c46a', '#c86b4a', '#8fbf6a', '#e9e1d0', '#8a5a3a'].map(c => std(c, .55)),
  trays: [std('#d96a2e', .5), std('#2a9d8f', .5), std('#e9c46a', .5)],
  heat: std('#ffb46b', .4, 0, { emissive: col('#ff9a3c'), emissiveIntensity: 1.1 }),
  chill: std('#eef8ff', .3, 0, { emissive: col('#bfe3ff'), emissiveIntensity: .7 }),
  frost: std('#e3eff4', .45), ice: std('#bcd9e6', .25, .1), white: std('#e8ebe8', .4, .05),
  juice: ['#f0a640', '#c4372a', '#9ad06a'].map(c => std(c, .2, 0, { transparent: true, opacity: .8 })),
  ovenWin: std('#2a1a12', .2, 0, { emissive: col('#ff7a2a'), emissiveIntensity: .55 }),
  food: { red: std('#c4372a', .5), green: std('#5f9e4a', .6), orange: std('#e0802c', .5), bread: std('#c99a5e', .8), wrap: std('#e9e1d0', .6) },
};
// ---- Deck 3, turn 4: the garden, infirmary, gym, store and booths (made at load, no R()) ----
const LEAF_GEO = new THREE.IcosahedronGeometry(1, 1);     // low-poly foliage: a garden's worth stays cheap
const leaf = (mat, x, y, z, sx, sy, sz, p) => { const m = new THREE.Mesh(LEAF_GEO, mat); m.scale.set(sx, sy, sz); m.position.set(x, y, z); m.castShadow = m.receiveShadow = true; p.add(m); return m; };
const GD = {
  leaves: ['#3f7a4f', '#4c8a57', '#6ba86a', '#2f6a44', '#86b85a'].map(c => std(c, .75)),
  lime: std('#9ccf5a', .7), dark: std('#24553a', .8),
  flowers: ['#e86a9a', '#f2c94c', '#f4f1e8', '#9b6ad6', '#ef7f45'].map(c => std(c, .6)),
  tomato: std('#d8412f', .45), orange: std('#f0952e', .45), lemon: std('#f2d84c', .45), bean: std('#5f9e3a', .6),
  soil: std('#3a2a1e', 1), bed: std('#7a5a3e', .8), stone: std('#9a9c94', .9), stone2: std('#b5b3a8', .9),
  led: std('#ff8ae6', .4, 0, { emissive: col('#ff4fd8'), emissiveIntensity: 1.4 }),
  ledW: std('#fff6e6', .4, 0, { emissive: col('#ffe9c4'), emissiveIntensity: 1.2 }),
  water: std('#2f8fa3', .08, .1, { emissive: col('#14535f'), emissiveIntensity: .5, transparent: true, opacity: .85 }),
  pad: std('#3f8a4a', .6), fish: std('#f08a2e', .4), pot: std('#b4553f', .8), post: std('#5a4636', .7),
  wing: ['#f2c94c', '#e86a9a', '#7ac7e8'].map(c => std(c, .6, 0, { side: THREE.DoubleSide })),
};
// a Tiles board (Pillar 4, seat 8): a game half played on a 6 x 6 grid, painted on one canvas. tilesBoardGeo() is a unit
// box 2 cm thick standing on y 0, its top showing the board and its sides the frame, so a board is one material and one
// draw call (and Tiles night's boards one InstancedMesh). Made at load, no R().
function tilesBoardGeo() {
  const g = new THREE.BoxGeometry(1, .02, 1), uv = g.attributes.uv; g.translate(0, .01, 0);
  for (let v = 0; v < uv.count; v++) if (v < 8 || v >= 12) uv.setXY(v, .02, .02);   // every face but the top (+y) takes the frame's colour
  return g;
}
const TILES_KIT = { tex: tex(256, 256, (c, w, h) => {   // the approved design (plans/tiles-plan.html, 0.38.17): a game at its start
  c.fillStyle = '#03141a'; c.fillRect(0, 0, w, h); c.strokeStyle = '#2f6f68'; c.lineWidth = 3; c.strokeRect(8, 8, w - 16, h - 16);   // the frame
  const S = 38, O = 14, cell = (i, j) => [O + i * S, O + j * S];
  for (let j = 0; j < 6; j++) for (let i = 0; i < 6; i++) { c.fillStyle = (i + j) % 2 ? '#061d22' : '#0a2a30'; c.fillRect(...cell(i, j), S, S); }
  c.setLineDash([3, 4]); c.lineWidth = 1.5;                // the home rows, two at each end
  c.strokeStyle = 'rgba(76,195,181,.5)'; c.strokeRect(O, O + 4 * S, 6 * S, 2 * S); c.strokeStyle = 'rgba(159,180,196,.45)'; c.strokeRect(O, O, 6 * S, 2 * S);
  const mark = (k, x, y) => {                             // circle, triangle or star on a tile
    c.setLineDash([]); c.lineWidth = 1.4; c.strokeStyle = '#0b1420'; c.beginPath();
    if (k === 0) { c.fillStyle = '#5fd3c6'; c.arc(x, y, 8, 0, Math.PI * 2); }
    else if (k === 1) { c.fillStyle = '#f08a6c'; c.moveTo(x, y - 9); c.lineTo(x + 9, y + 7); c.lineTo(x - 9, y + 7); c.closePath(); }
    else { c.fillStyle = '#f2c14e'; for (let p = 0; p < 10; p++) { const a = -Math.PI / 2 + p * Math.PI / 5, r = p % 2 ? 4 : 9; c.lineTo(x + Math.cos(a) * r, y + Math.sin(a) * r); } c.closePath(); }
    c.fill(); c.stroke();
  };
  const round = (x, y, s, r) => { c.beginPath(); c.moveTo(x + r, y); c.arcTo(x + s, y, x + s, y + s, r); c.arcTo(x + s, y + s, x, y + s, r); c.arcTo(x, y + s, x, y, r); c.arcTo(x, y, x + s, y, r); c.closePath(); };
  const marks = [0, 1, 2, 2, 1, 0, 1, 2, 0, 0, 2, 1];      // both sides the same set, mirrored
  for (let k = 0; k < 12; k++) {
    const i = k % 6, jl = k < 6 ? 5 : 4, jd = 5 - jl, [xl, yl] = cell(i, jl), [xd, yd] = cell(5 - i, jd);
    round(xl + 3, yl + 3, S - 6, 6); c.setLineDash([]); c.fillStyle = '#e9f1ee'; c.fill(); c.strokeStyle = '#ffffff'; c.lineWidth = 1.2; c.stroke(); mark(marks[k], xl + S / 2, yl + S / 2);   // yours: light
    round(xd + 4, yd + 4, S - 8, 6); c.fillStyle = '#142233'; c.fill(); c.setLineDash([4, 3]); c.strokeStyle = '#9fb4c4'; c.lineWidth = 2; c.stroke(); mark(marks[k], xd + S / 2, yd + S / 2);   // theirs: dark, a dashed edge
  }
}) };
TILES_KIT.mat = new THREE.MeshStandardMaterial({ map: TILES_KIT.tex, roughness: .7 }); TILES_KIT.geo = tilesBoardGeo();
const MED = {
  white: std('#eef1ef', .45), frame: std('#b9c2c6', .3, .6), mattress: std('#dfe9ec', .8), sheet: std('#c9e2e6', .85),
  curtain: std('#9fcfd6', .8, 0, { transparent: true, opacity: .8, side: THREE.DoubleSide }), cross: std('#c8463c', .5),
  screen: std('#9ff3e6', .3, 0, { emissive: col('#4fd8c4'), emissiveIntensity: 1.0 }), paper: std('#f4f1e8', .9),
};
// a treadmill belt: dark rubber with lighter slats, so you can see it run (made at load, no R())
const beltTex = tex(32, 64, (g, w, h) => { g.fillStyle = '#1d2226'; g.fillRect(0, 0, w, h); g.fillStyle = '#353d43'; for (let y = 0; y < h; y += 8) g.fillRect(0, y, w, 2); }, 1, 4);
const GYM = {
  rubber: std('#1d2226', .9), frame: std('#2b343b', .5, .4), accent: std('#e9c46a', .5), teal: std('#2a9d8f', .6),
  mat: ['#2a9d8f', '#7a5aa8', '#d96a2e'].map(c => std(c, .9)), plate: std('#22282d', .5, .3), chrome: std('#c7cfd3', .25, .8),
  mirror: std('#a9c3c9', .08, .4, { emissive: col('#2c4048'), emissiveIntensity: .35 }),
};
const PROM = {                                             // the promenade's planters and kiosk
  clad: std('#8a6446', .75), rim: std('#d4c7a8', .6), frame: std('#2b343b', .5, .35), brass: std('#c9a24a', .35, .7),
  bloom: ['#f2c94c', '#ef7f45', '#e86a9a', '#f4f1e8'].map(c => std(c, .6)),
};
const SHOP = { goods: ['#e86a9a', '#f2c94c', '#2a9d8f', '#d96a2e', '#7a5aa8', '#e9e1d0', '#5f9e3a', '#c8463c'].map(c => std(c, .6)), glowW: std('#f4fbff', .3, 0, { emissive: col('#dff2ff'), emissiveIntensity: .8 }) };
// ---- Deck 6: the engine room (made at load, no R()) ----
const ENG = {
  copper: std('#b8733a', .35, .8), housing: std('#59646b', .5, .45), plinth: std('#2f363c', .6, .4), walk: std('#4a535a', .6, .5),
  shield: std('#7d878c', .55, .35), pipe: std('#9fb7c2', .35, .55), console: std('#2b333a', .55, .3),
  // engine control's mimic panel: the reactor, its two junctions, and a line up to every deck
  mimic: new THREE.MeshBasicMaterial({ toneMapped: false, map: tex(512, 170, (c, w, h) => {
    c.fillStyle = '#0d1a1f'; c.fillRect(0, 0, w, h);
    c.strokeStyle = '#7dffb0'; c.lineWidth = 4; c.beginPath(); c.arc(70, 100, 34, 0, Math.PI * 2); c.stroke();
    c.fillStyle = 'rgba(125,255,176,.35)'; c.beginPath(); c.arc(70, 100, 20, 0, Math.PI * 2); c.fill();
    c.strokeStyle = '#e8c06a'; c.lineWidth = 3;
    for (const y of [70, 130]) { c.beginPath(); c.moveTo(104, 100); c.lineTo(150, y); c.lineTo(200, y); c.stroke(); c.strokeRect(200, y - 12, 34, 24); }
    for (let k = 0; k < 6; k++) {
      const x = 270 + k * 38, live = k !== 3;
      c.strokeStyle = live ? '#5fd6c6' : '#f0a640'; c.beginPath(); c.moveTo(234, k % 2 ? 130 : 70); c.lineTo(x, k % 2 ? 130 : 70); c.lineTo(x, 26); c.stroke();
      c.fillStyle = live ? '#5fd6c6' : '#f0a640'; c.font = '700 18px system-ui,sans-serif'; c.fillText(String(6 - k), x - 5, 20);
    }
    c.fillStyle = '#a9c4bf'; c.font = '500 13px system-ui,sans-serif'; c.fillText('CSV WREN  POWER', 20, 22); c.fillText('REACTOR', 40, 158);
  }, 1, 1) }),
  // the radiation sign either side of the reactor door
  trefoil: new THREE.MeshBasicMaterial({ toneMapped: false, map: tex(128, 128, (c, w, h) => {
    c.fillStyle = '#e8c06a'; c.fillRect(0, 0, w, h); c.strokeStyle = '#1d2226'; c.lineWidth = 6; c.strokeRect(6, 6, w - 12, h - 12);
    c.fillStyle = '#1d2226'; c.beginPath(); c.arc(64, 64, 9, 0, Math.PI * 2); c.fill();
    for (let k = 0; k < 3; k++) { const a = -Math.PI / 2 + k * Math.PI * 2 / 3; c.beginPath(); c.moveTo(64, 64); c.arc(64, 64, 46, a - Math.PI / 6, a + Math.PI / 6); c.arc(64, 64, 15, a + Math.PI / 6, a - Math.PI / 6, true); c.closePath(); c.fill(); }
  }, 1, 1) }),
};
function makePollen(w, d, n = 40) {                        // drifting motes over the beds
  const pos = new Float32Array(n * 3), seeds = [];
  for (let i = 0; i < n; i++) { pos[i * 3] = (R() - .5) * w; pos[i * 3 + 1] = .5 + R() * 1.6; pos[i * 3 + 2] = (R() - .5) * d; seeds.push(R() * 10); }
  const geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  const p = new THREE.Points(geo, new THREE.PointsMaterial({ map: glowTex, size: .06, color: col('#f2ffb8'), transparent: true, opacity: .7, blending: THREE.AdditiveBlending, depthWrite: false }));
  DUST.push({ geo, seeds, n }); return p;
}

// =====================================================================
// ROOM TEMPLATES
// A template furnishes a room from its size and where its door is, so the
// same few lines work for every bunk room, washroom, laundry and cabin.
// Templates work in a room frame: u runs along the door wall, left to right
// as you walk in; v runs from the door wall (0) to the back wall (V).
// Walls are named back, left, right and front in that frame.
// =====================================================================
function roomFrame(rk) {
  const b = ROOM_BOX[rk], Wr = b.i1 - b.i0 + 1, Dr = b.j1 - b.j0 + 1;
  let side = 's', at = Wr / 2;
  for (const [key, type] of Object.entries(DOORS)) {
    if (type !== 'door' && type !== 'open') continue;
    const [k, a, c] = key.split(','), i = +a, j = +c;
    if (k === 'h' && i >= b.i0 && i <= b.i1 && (j === b.j0 || j === b.j1 + 1)) { side = j === b.j0 ? 'n' : 's'; at = i - b.i0 + .5; break; }
    if (k === 'v' && j >= b.j0 && j <= b.j1 && (i === b.i0 || i === b.i1 + 1)) { side = i === b.i0 ? 'w' : 'e'; at = j - b.j0 + .5; break; }
  }
  const ns = side === 'n' || side === 's';
  return {
    U: ns ? Wr : Dr, V: ns ? Dr : Wr,
    toL: { s: (u, v) => [u, Dr - v], n: (u, v) => [Wr - u, v], w: (u, v) => [v, u], e: (u, v) => [Wr - v, Dr - u] }[side],
    wall: { s: { back: 'n', left: 'w', right: 'e', front: 's' }, n: { back: 's', left: 'e', right: 'w', front: 'n' },
            w: { back: 'e', left: 'n', right: 's', front: 'w' }, e: { back: 'w', left: 's', right: 'n', front: 'e' } }[side],
    doorU: { s: at, n: Wr - at, w: at, e: Dr - at }[side],
  };
}
function furnish(rk, name, o = {}) {
  const F = roomFrame(rk);
  if (o.locked) NO_FADE.add(rk);
  for (const p of TEMPLATES[name](F.U, F.V, F, o)) {
    if (p.wall) {                                       // wall piece: 'at' is u on back/front walls, v on left/right
      const [lx, lz] = (p.wall === 'back' || p.wall === 'front') ? F.toL(p.at, p.wall === 'back' ? F.V : 0) : F.toL(p.wall === 'left' ? 0 : F.U, p.at);
      const w = F.wall[p.wall];
      placeWall(rk, p.kind, w, (w === 'n' || w === 's') ? lx : lz, p.o || {});
    } else {
      const [lx, lz] = F.toL(p.u, p.v), back = F.wall[p.back || 'back'];
      const g = place(rk, p.kind, lx, lz, back, p.o || {});
      if (p.spot) SPOTS.push({ room: rk, tag: p.spot, x: g.position.x, z: g.position.z, front: FACING[back] + ((p.o && p.o.turn) || 0) });
    }
  }
}
const TEMPLATES = {
  // double bunks with heads to the back wall, footlockers at their feet, lockers by the door; a table if there's room
  bunkRoom(U, V, F, o) {
    const out = [], n = o.bunks || Math.max(1, Math.min(3, Math.floor((U - .2) / 1.3)));
    const bl = o.blankets || [[M.blanket, M.mustard], [M.plum, M.tealFab], [M.blanket, M.plum]];
    for (let k = 0; k < n; k++) {
      const u = (k + .5) * U / n, [low, high] = bl[k % bl.length];
      out.push({ kind: 'bunk', u, v: V - 1.1, spot: 'bed', o: { low, high, it: (o.its || [])[k] || IT('Bunk', 'Two berths, two footlockers, one ladder.') } });
      out.push({ kind: 'footlocker', u, v: V - 2.35 });
      if (k) out.push({ wall: 'back', kind: 'sconce', at: k * U / n });
    }
    const fz = V - 2.6;                                  // depth left in front of the footlockers
    if (fz >= 1.35) {
      const lv = Math.max(.75, Math.min(1.6, fz - .7));
      out.push({ kind: 'locker', u: .4, v: lv, back: 'left', spot: 'cleanUniforms', o: o.wardrobe ? { it: o.wardrobe } : undefined });   // o.wardrobe: this one's a bed's wardrobe (0.38.24)
      out.push({ kind: 'locker', u: U - .4, v: lv, back: 'right', spot: 'cleanUniforms' });
    }
    if (V >= 6) {
      const tv = (fz + 1.3) / 2;
      out.push({ kind: 'rug', u: U / 2, v: tv, o: { tex: rugBunk, w: 2.4, d: 2.0 } });
      out.push({ kind: 'teaTable', u: U / 2, v: tv, o: { it: o.table } });
      out.push({ kind: 'stool', u: U / 2 - .75, v: tv }, { kind: 'stool', u: U / 2 + .75, v: tv });
      for (const pu of [.45, U - .45]) if (Math.abs(pu - F.doorU) > 1) out.push({ kind: 'plant', u: pu, v: .45, back: 'front', o: { band: '#d9a441' } });
    }
    if (o.poster) out.push({ wall: 'right', kind: 'poster', at: V - 2.6, o: o.poster });
    return out;
  },
  // stalls along the back (showers, then o.wc toilets, default one), basins on the left, a bench and towels on the right
  washroom(U, V, F, o) {
    const out = [], n = Math.max(2, Math.floor((U - .2) / 1.25)), slot = (U - .2) / n, len = Math.min(2.0, V - 1.6), mid = .2 + len / 2;
    for (let k = 0; k < n; k++) {
      const shower = !o.toilets && k < n - (o.wc || 1);   // public washrooms (Deck 3) are all toilets
      out.push({ kind: shower ? 'showerStall' : 'toiletStall', u: .1 + slot * (k + .5), v: V - .65, spot: shower ? 'shower' : 'toilet',
        o: { it: shower ? IT('Shower', 'Hot water on a timer. The timer is generous until the recycler on Deck 3 has a bad day.')
                        : IT('Toilet', 'Vacant. The little green light is the most trusted instrument on the ship.') } });
    }
    out.push({ kind: 'basinCounter', u: .375, v: mid, back: 'left', spot: 'basin', o: { w: len, n: len > 1.5 ? 2 : 1, it: IT('Basins', 'One mirror each and a long-running argument about toothpaste caps.') } });
    if (o.bench !== false) out.push({ kind: 'bench', u: U - .3, v: mid, back: 'right', o: { w: Math.min(1.4, len) } });   // o.bench false: none (0.38.27)
    out.push({ wall: 'right', kind: 'towels', at: mid });
    out.push({ wall: 'right', kind: 'sconce', at: Math.min(V - 1.4, mid + len / 2 + .3) });
    return out;
  },
  // washers along the back, clean uniforms on the left, folding on the right, the laundry drop by the door
  laundry(U, V, F, o) {
    const out = [], n = Math.max(1, Math.floor((U - .2) / .92)), slot = (U - .2) / n, sv = Math.max(.9, (V - 2) / 2);
    const notes = ['Running a gold load. Works uniforms get the dirtiest.', 'Finished. Someone will come for these eventually.',
                   'Thumps a little on the spin cycle. Worth keeping an eye on.', 'Idle, door open, smelling faintly of soap.'];
    for (let k = 0; k < n; k++) out.push({ kind: 'washer', u: .1 + slot * (k + .5), v: V - .46, spot: 'washer', o: { it: IT('Washer ' + (k + 1), notes[k % 4]) } });
    for (let k = 1; k <= 2; k++) out.push({ wall: 'back', kind: 'sconce', at: k * U / 3 });
    out.push({ kind: 'uniformRack', u: .325, v: sv, back: 'left', spot: 'cleanUniforms', o: { it: IT('Clean uniforms', 'Pressed and sorted by department. Take your size and leave the rest tidy.') } });
    out.push({ kind: 'foldingTable', u: U - .4, v: sv, back: 'right', spot: 'fold', o: { it: IT('Folding table', 'Somebody folds the gold ones into perfect squares. Nobody admits to it.') } });
    out.push({ kind: 'hamper', u: F.doorU < U / 2 ? F.doorU + 1.05 : F.doorU - 1.05, v: .35, back: 'front', spot: 'laundryDrop', o: { it: IT('Laundry drop', 'Grubby uniforms go in here. Every shift, ideally.') } });
    return out;
  },
  // compact officer cabin: bed and desk at the back, wardrobe and wash pod either side of the door
  // o.guest: lived in by someone passing through (fresh linen, a travel case). o.spare: stripped bed, bare desk, no poster
  officerCabin(U, V, F, o) {
    const out = [
      { kind: 'bedSingle', u: .62, v: V - 1.1, spot: 'bed', o: { blanket: M.plum, stripped: o.spare, linen: !!o.guest, it: o.bed || IT('Bed', 'A real mattress and a door that closes. This is what the first promotion buys you.') } },
      { kind: 'deskSmall', u: U - .65, v: V - .375, spot: 'desk', o: { bare: o.spare, it: IT('Desk', o.spare ? 'Wiped down and switched off, waiting for the next arrival.' : 'A terminal, a lamp, and just enough room for one mug.') } },
      { kind: 'chair', u: U - .65, v: V - 1.05, o: { turn: Math.PI } },
      { kind: 'wardrobe', u: .375, v: .65, back: 'left', spot: 'cleanUniforms', o: { it: IT('Wardrobe', 'Two clean uniforms and a jacket for the cold decks.') } },
      { kind: 'washPod', u: U - .6, v: .6, back: 'right', spot: 'shower', o: { it: IT('Wash pod', 'Shower, basin and toilet in one tidy cubicle. Small, private, and all yours.') } },
      { wall: 'left', kind: 'readingLamp', at: V - .6 },
      { wall: 'right', kind: 'poster', at: (1.1 + V - .65) / 2, o: o.poster || {} },
    ];
    if (o.spare) out.pop();
    if (o.guest) out.push({ kind: 'travelCase', u: .62, v: V - 2.35, o: { k: o.guest } });
    return out;
  },
};

// ---- merge everything static into a few meshes ----
// 0.27.23: a garden kit with o.live records its plants here instead of building them (section 8b's gardenView grows
// them with the galley's beds). Same calls in the same order, so R() is drawn exactly as before. GARDEN_PLOTS is the
// deck's list: { g, crop, n (the nth bed of that crop on the deck), base (soil height), slots }
let GARDEN_PLOTS = [];
function plantSlots(g, crop, base) {
  const P = { g, crop, n: GARDEN_PLOTS.filter(p => p.crop === crop).length, base, slots: [] }; GARDEN_PLOTS.push(P);
  const fruit = m => m === GD.tomato || m === GD.bean || GD.flowers.includes(m);
  const put = (geo, mat, x, y, z, sx, sy, sz) => { P.slots.push({ geo, mat, x, y, z, sx, sy, sz, fruit: fruit(mat) }); };
  return { leaf: (mat, x, y, z, sx, sy, sz) => put('leaf', mat, x, y, z, sx, sy, sz), soft: (mat, x, y, z, sx, sy, sz) => put('ball', mat, x, y, z, sx, sy, sz),
    pod: (rt, rb, h, mat, x, y, z) => put('pod', mat, x, y, z, 1, 1, 1) };
}
// 0.27.20: neighbouring faces of one geometry that share a material become one group, so a door leaf's box (four
// edge faces, then two faces) draws in 2 calls, not 6, in the picture and in the shadows. Same triangles in the same
// order, so nothing on screen changes.
function packGroups(geo, mats) {
  const out = [];
  for (const gr of geo.groups) { const p = out[out.length - 1]; if (p && mats[p.materialIndex] === mats[gr.materialIndex] && p.start + p.count === gr.start) p.count += gr.count; else out.push({ ...gr }); }
  geo.groups = out; return geo;
}
// 0.27.22: tall furniture is drawn together: one mesh per material (and shadow flag) for the whole deck, made from
// every room's merged pieces in room order, with one more copy of the material made like each room's own (so it
// doesn't pulse or wilt with the shared one, as before). A room that is fading or faded (t.o below 1) shows its own
// meshes again, and the deck-wide mesh skips that room's stretch (tallSync, each frame after the fades). Opaque only.
let TALL_ALL = [], TALL_KEY = null;
function tallCombine() {
  const buckets = new Map(); TALL_ALL = []; TALL_KEY = null;
  TALL.forEach((t, ti) => {
    t.own = [];
    for (const o of t.g.children.slice()) {
      const base = o.isMesh && !o.userData.noMerge && !Array.isArray(o.material) && t.src.get(o.material);
      if (!base || base.transparent || base.opacity < 1) continue;
      const key = base.uuid + (o.castShadow ? '' : '-ns');
      let b = buckets.get(key); if (!b) buckets.set(key, b = { mat: base.clone(), shadow: o.castShadow, P: [], N: [], U: [], ranges: [] });
      const a = o.geometry.attributes, n = a.position.count;
      b.ranges.push([ti, b.P.length / 3, n]); for (const [d, s] of [[b.P, a.position], [b.N, a.normal], [b.U, a.uv]]) for (const v of s.array) d.push(v);
      o.visible = false; t.own.push(o);
    }
  });
  for (const b of buckets.values()) {
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.Float32BufferAttribute(b.P, 3)); geo.setAttribute('normal', new THREE.Float32BufferAttribute(b.N, 3));
    geo.setAttribute('uv', new THREE.Float32BufferAttribute(b.U, 2)); geo.computeBoundingSphere();
    const mesh = new THREE.Mesh(geo, [b.mat]); mesh.castShadow = b.shadow; mesh.receiveShadow = true; mesh.raycast = () => {}; deckRoot.add(mesh);
    TALL_ALL.push({ mesh, ranges: b.ranges });
  }
  tallSync();
}
// 0.27.25: shadow stand-ins. The shadow pass drew every furniture mesh, wall piece and hull piece again, one draw per
// material, more draws than the picture itself. A shadow only needs the shape, so after the build their triangles are
// copied, positions only, into a few plain meshes, and the originals stop casting:
//   - things that never move (the merged furniture, the tall pieces): one stand-in per 10 x 10 tile block;
//   - wall pieces: one per wall run, shown only while that run's pieces are up (they drop with the cutaway together);
//   - hull pieces, their decor and the curved walls: one per piece, following its height as the cutaway lowers it.
// One per face side as well, since the shadow pass follows each material's side. The stand-ins are hidden except while
// the shadow pass runs (the main pass has already picked what it draws), so they never reach the picture. Same depth
// from the same triangles, so the same shadows. Left alone: instanced things (walls, door leaves, plants, the crowd),
// anything marked noMerge (it moves), and materials with alphaTest or their own shadowSide.
// 0.27.33: built a slice at a time. buildDeck only lists what will cast through a stand-in (cheap); shadowStep, once a
// frame from the main loop, does the triangle work, SHADOW_STEP vertices a frame, counting first and then filling, as
// before. Until the last stand-in is ready nothing changes: the originals keep casting their own shadows. Then they all
// switch in one go, to stand-ins with the same triangles in the same order as when this was done in one go.
let SHADOW_PROXY = [], SHADOW_JOB = null;
const SHADOW_STEP = 40000;                               // vertices a frame (each is read twice: counting, then filling)
const SHADOW_PROXY_MAT = [THREE.FrontSide, THREE.BackSide, THREE.DoubleSide].map(side => new THREE.MeshBasicMaterial({ side }));
function shadowStandIns() {
  SHADOW_PROXY = []; SHADOW_JOB = null;
  deckRoot.updateMatrixWorld(true);
  const items = [], seen = new Set(), inv = new THREE.Matrix4();
  // a mesh to copy into the stand-ins, in frame's own space (world when frame is null). key names its bucket; null means
  // by the 10 x 10 tile block each triangle's middle falls in
  const take = (m, frame, key, follow, vis) => {
    if (seen.has(m) || !m.isMesh || m.isInstancedMesh || m.isSkinnedMesh || !m.castShadow || m.userData.noMerge) return;
    const mats = Array.isArray(m.material) ? m.material : [m.material], side = mats[0].side;
    if (mats.some(x => x.alphaTest > 0 || x.shadowSide != null || !x.visible || x.side !== side)) return;
    for (let p = m.parent; p && p !== frame && p !== deckRoot; p = p.parent) if (p.userData.noMerge) return;
    seen.add(m);
    items.push({ m, side, key, follow, vis, m4: new THREE.Matrix4().multiplyMatrices(frame ? inv.copy(frame.matrixWorld).invert() : inv.identity(), m.matrixWorld) });
  };
  const own = [];
  for (const m of staticRoot.children) take(m, null, null);
  for (const b of TALL_ALL) take(b.mesh, null, null);
  for (const t of TALL) for (const o of t.own || []) { own.push(o); seen.add(o); }   // a fading room's own meshes: the stand-ins cast for them
  const runs = new Map();
  for (const d of WALL_DECOR) {
    const run = d.e && (d.e.type === 'hull' ? d.e.hrun : d.e.run);
    if (!run) { d.g.traverse(m => take(m, null, null)); continue; }
    if (!runs.has(run)) runs.set(run, { id: 'w' + runs.size, vis: d.g });
    const r = runs.get(run); d.g.traverse(m => take(m, null, r.id, null, r.vis));
  }
  HULL_RUNS.forEach((hr, k) => {
    hr.g.traverse(m => take(m, hr.g, 'h' + k, hr.g, hr.g));
    hr.decor.traverse(m => take(m, hr.decor, 'hd' + k, hr.decor, hr.decor));
  });
  CURVES.forEach((c, k) => c.g.traverse(m => take(m, c.g, 'cv' + k, c.g, c.g)));
  SHADOW_JOB = { root: deckRoot, items, own, buckets: new Map(), fill: false, i: 0, t: 0 };
}
// the next SHADOW_STEP vertices of the job; at the end of the filling, the stand-ins go in and the originals stop casting
function shadowStep() {
  const J = SHADOW_JOB; if (!J) return;
  if (J.root !== deckRoot) { SHADOW_JOB = null; return; }
  const v = SHADOW_V, tri = SHADOW_TRI, CELL = 10;
  let left = SHADOW_STEP;
  while (left > 0 && J.i < J.items.length) {
    const it = J.items[J.i], P = it.m.geometry.attributes.position, I = it.m.geometry.index, n = I ? I.count : P.count;
    let lx = NaN, lz = NaN, lb = null, t = J.t;
    for (; t + 2 < n && left > 0; t += 3, left -= 3) {
      let cx = 0, cz = 0;
      for (let k = 0; k < 3; k++) { v.fromBufferAttribute(P, I ? I.getX(t + k) : t + k).applyMatrix4(it.m4); tri[k * 3] = v.x; tri[k * 3 + 1] = v.y; tri[k * 3 + 2] = v.z; cx += v.x; cz += v.z; }
      let b;
      if (it.key !== null) b = lb || (lb = J.buckets.get(it.side + '|' + it.key));
      else { const ix = Math.floor(cx / 3 / CELL), iz = Math.floor(cz / 3 / CELL); if (ix === lx && iz === lz) b = lb; else { lx = ix; lz = iz; b = lb = J.buckets.get(it.side + '|c' + ix + ',' + iz); } }
      if (!b) { const id = it.side + '|' + (it.key !== null ? it.key : 'c' + lx + ',' + lz); J.buckets.set(id, b = lb = { side: it.side, n: 0, P: null, at: 0, follow: it.follow, vis: it.vis, lo: [Infinity, Infinity, Infinity], hi: [-Infinity, -Infinity, -Infinity], c: null, r2: 0 }); }
      // the bounding sphere as computeBoundingSphere makes it, worked out on the way: the box while counting, the radius while filling
      if (!J.fill) { b.n += 9; for (let k = 0; k < 9; k++) { const q = tri[k], a = k % 3; if (q < b.lo[a]) b.lo[a] = q; if (q > b.hi[a]) b.hi[a] = q; } }
      else { b.P.set(tri, b.at); b.at += 9; for (let k = 0; k < 9; k += 3) { const dx = b.c[0] - tri[k], dy = b.c[1] - tri[k + 1], dz = b.c[2] - tri[k + 2]; b.r2 = Math.max(b.r2, dx * dx + dy * dy + dz * dz); } }
    }
    if (t + 2 < n) { J.t = t; return; }
    J.i++; J.t = 0;
  }
  if (J.i < J.items.length) return;
  if (!J.fill) { J.fill = true; J.i = 0; for (const b of J.buckets.values()) { b.P = new Float32Array(b.n); b.c = [0, 1, 2].map(a => (b.lo[a] + b.hi[a]) * .5); } return; }
  for (const b of J.buckets.values()) {
    const geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.BufferAttribute(b.P, 3).onUpload(function () { this.array = null; }));   // once on the GPU the copy here isn't needed
    geo.boundingSphere = new THREE.Sphere(new THREE.Vector3(...b.c), Math.sqrt(b.r2));
    const mesh = new THREE.Mesh(geo, SHADOW_PROXY_MAT[b.side]); mesh.castShadow = true; mesh.receiveShadow = false; mesh.visible = false;
    mesh.matrixAutoUpdate = false; mesh.raycast = () => {}; deckRoot.add(mesh); SHADOW_PROXY.push({ mesh, follow: b.follow, vis: b.vis });
  }
  for (const it of J.items) { it.m.castShadow = false; it.m.userData.shadowProxy = true; }
  for (const o of J.own) o.castShadow = false;
  SHADOW_JOB = null;
}
const SHADOW_V = new THREE.Vector3(), SHADOW_TRI = new Float32Array(9);
// 0.27.26: three.js recomputes every object's place in the world every frame unless told it doesn't move. After the
// build, the furniture (staticRoot), the tall pieces (TALL) and the wall pieces (WALL_DECOR) are marked so
// (matrixAutoUpdate off, their matrix computed once), except anything that moves: noMerge parts and everything under
// them (gym seats, the punch bag, rotors), SPINS targets, STEAM puffs, and the groups that hold any of those. Hull, doors, curved
// walls and void blocks change size with the cutaway and are left alone. Children added later keep updating themselves.
function freezeStill() {
  const keep = new Set();
  const mark = o => { for (let p = o; p && p !== deckRoot; p = p.parent) keep.add(p); };
  for (const sp of SPINS) if (sp.o && sp.o.isObject3D) mark(sp.o);
  for (const st of STEAM) mark(st.s);                   // steam puffs rise every frame
  const roots = [staticRoot, ...TALL.map(t => t.g), ...WALL_DECOR.map(d => d.g)];
  for (const r of roots) r.traverse(o => { if (o.userData.noMerge) mark(o); });
  const freeze = o => {
    if (o.userData.noMerge) return;                     // it, and all under it, keep moving
    if (!keep.has(o)) { o.updateMatrix(); o.matrixAutoUpdate = false; }
    for (const c of o.children) freeze(c);
  };
  for (const r of roots) freeze(r);
}
const shownChain = o => { for (let p = o; p; p = p.parent) if (!p.visible) return false; return true; };
{ const sm = renderer.shadowMap, draw = sm.render.bind(sm);   // the stand-ins show only to the shadow pass, each where its original is
  sm.render = (...a) => {
    for (const p of SHADOW_PROXY) { p.mesh.visible = !p.vis || shownChain(p.vis); if (p.follow) p.mesh.matrixWorld.copy(p.follow.matrixWorld); }
    try { draw(...a); } finally { for (const p of SHADOW_PROXY) p.mesh.visible = false; }
  }; }
function tallSync() {
  let key = ''; TALL.forEach((t, i) => { if (t.o !== 1) key += i + ','; });
  if (key === TALL_KEY) return;
  TALL_KEY = key; const out = new Set(key.split(',').filter(Boolean).map(Number));
  TALL.forEach((t, i) => { for (const o of t.own || []) o.visible = out.has(i); });
  for (const b of TALL_ALL) {
    const gr = [];
    for (const [ti, start, count] of b.ranges) { if (out.has(ti)) continue; const p = gr[gr.length - 1]; if (p && p.start + p.count === start) p.count += count; else gr.push({ start, count, materialIndex: 0 }); }
    b.mesh.geometry.groups = gr; b.mesh.visible = gr.length > 0;
  }
}
function mergeMeshes(root) {
  root.updateMatrixWorld(true);
  const inv = new THREE.Matrix4().copy(root.matrixWorld).invert(), m4 = new THREE.Matrix4();
  const buckets = new Map(), done = [];
  root.traverse(o => {
    if (!o.isMesh || o.userData.noMerge) return;
    const mats = Array.isArray(o.material) ? o.material : [o.material];
    const g = o.geometry.index ? o.geometry.toNonIndexed() : o.geometry.clone();
    g.applyMatrix4(m4.multiplyMatrices(inv, o.matrixWorld));
    const groups = Array.isArray(o.material) ? g.groups : [{ start: 0, count: g.attributes.position.count, materialIndex: 0 }];
    const P = g.attributes.position.array, Nn = g.attributes.normal.array, U = g.attributes.uv ? g.attributes.uv.array : null;
    for (const gr of groups) {
      const mat = mats[gr.materialIndex]; if (!mat) continue;
      const key = mat.uuid + (o.userData.noShadow ? '-ns' : '');
      let b = buckets.get(key); if (!b) buckets.set(key, b = { mat, P: [], N: [], U: [], shadow: !o.userData.noShadow });
      for (let v = gr.start; v < gr.start + gr.count; v++) {
        b.P.push(P[v * 3], P[v * 3 + 1], P[v * 3 + 2]); b.N.push(Nn[v * 3], Nn[v * 3 + 1], Nn[v * 3 + 2]);
        if (U) b.U.push(U[v * 2], U[v * 2 + 1]); else b.U.push(0, 0);
      }
    }
    g.dispose(); done.push(o);
  });
  for (const o of done) o.parent.remove(o);
  for (const b of buckets.values()) {
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.Float32BufferAttribute(b.P, 3));
    geo.setAttribute('normal', new THREE.Float32BufferAttribute(b.N, 3));
    geo.setAttribute('uv', new THREE.Float32BufferAttribute(b.U, 2));
    geo.computeBoundingSphere();
    const mesh = new THREE.Mesh(geo, b.mat); mesh.castShadow = b.shadow; mesh.receiveShadow = true; root.add(mesh);
  }
}

