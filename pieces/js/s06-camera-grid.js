// =====================================================================
// 6. CAMERA
// =====================================================================
const camera = new THREE.OrthographicCamera(-1, 1, 1, -1, 16, 46);
let az = Math.PI / 4, azT = az;
const target = new THREE.Vector3(0, .7, 0);
function frame() {
  const a = innerWidth / innerHeight, vh = Math.max(8.4, 11.6 / a);
  Object.assign(camera, { left: -vh * a / 2, right: vh * a / 2, top: vh / 2, bottom: -vh / 2 });
  camera.updateProjectionMatrix();
}
const _r = new THREE.Vector3(), _u = new THREE.Vector3();
function placeCam() {
  const el = .62;
  // 0.27.18: how far the view reaches along the line of sight; zoomed far out (mostly on tall phones) the near and far
  // planes move out with it, so the deck is never sliced off. At the usual zooms it's the old 16 to 46 at 30.
  const reach = (camera.top - camera.bottom) / 2 / camera.zoom / Math.tan(el) + 4, dist = Math.max(30, reach + 2);
  const near = reach > 14 ? dist - reach : 16, far = reach > 14 ? dist + reach : 46;
  if (camera.near !== near || camera.far !== far) { camera.near = near; camera.far = far; camera.updateProjectionMatrix(); }
  camera.position.set(target.x + dist * Math.cos(el) * Math.sin(az), target.y + dist * Math.sin(el), target.z + dist * Math.cos(el) * Math.cos(az));
  camera.lookAt(target); camera.updateMatrixWorld();
  const wpp = (camera.top - camera.bottom) / camera.zoom / renderer.domElement.height;   // snap to device pixels
  _r.setFromMatrixColumn(camera.matrixWorld, 0); _u.setFromMatrixColumn(camera.matrixWorld, 1);
  const pr = camera.position.dot(_r), pu = camera.position.dot(_u);
  camera.position.addScaledVector(_r, Math.round(pr / wpp) * wpp - pr).addScaledVector(_u, Math.round(pu / wpp) * wpp - pu);
  camera.updateMatrixWorld();
}
frame();
camera.zoom = innerWidth / innerHeight < .8 ? 1.5 : 1.15; camera.updateProjectionMatrix();
// 0.27.18 (the user: a decent zoom out, but no visible culling): the widest zoom is 0.55, or 0.7 on a tall screen
// (which already sees far more of the deck top to bottom); shadows and the near and far planes follow the zoom.
const ZOOM_MAX = 2.4; let ZOOM_MIN = .55;
const fitZoomMin = () => { ZOOM_MIN = innerWidth / innerHeight < .8 ? .7 : .55; if (camera.zoom < ZOOM_MIN) { camera.zoom = ZOOM_MIN; camera.updateProjectionMatrix(); } };
fitZoomMin();
addEventListener('resize', () => { renderer.setSize(innerWidth, innerHeight); frame(); fitZoomMin(); });

// =====================================================================
// 7. GRID & PATHFINDING
// Tiles are blocked by furniture and solid areas; edges are blocked by
// walls, windows and locked doors. Diagonal steps never cut a corner.
// =====================================================================
const cellPos = (i, j) => new THREE.Vector3(X0(i) + .5, 0, Z0(j) + .5);
const free = (i, j) => i >= 0 && j >= 0 && i < W && j < D && !isVoid(i, j) && !BLOCKED.has(i + ',' + j);
function edgeOpen(i, j, i2, j2, who) {
  const key = i2 !== i ? `v,${Math.max(i, i2)},${j}` : `h,${i},${Math.max(j, j2)}`;
  return !edgeBlocks(EDGES.get(key), who);
}
let ROOM_TILES = {};                                     // per room: the tiles people can stand on (the crew brain picks from these)
function indexRoomTiles() {
  ROOM_TILES = {};
  for (let j = 0; j < D; j++) for (let i = 0; i < W; i++) if (free(i, j)) (ROOM_TILES[roomAt(i, j)] || (ROOM_TILES[roomAt(i, j)] = [])).push([i, j]);
}
// 0.27.29 (the performance engineer): findPath is the same search as findPathScan below, made fast. The open tiles sit
// in a binary heap ordered by (f, the order each tile was first added), which is exactly the tile the scan picks (the
// lowest f, the earliest in its list on a tie), so every path is the same tile for tile. Tiles are numbers (i * D + j) in
// typed arrays kept between calls (a stamp says which call wrote them), and free() and edgeOpen() are asked at most once
// per tile or edge in a call. A start or goal off the grid goes to findPathScan.
const FP_DIRS = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]], _fp = { n: 0, gen: 0 };
const onGrid = c => Number.isInteger(c[0]) && Number.isInteger(c[1]) && c[0] >= 0 && c[1] >= 0 && c[0] < W && c[1] < D;
function findPath(s, g, avoid, who) {
  if (!onGrid(s) || !onGrid(g)) return findPathScan(s, g, avoid, who);
  const N = W * D, F = _fp;
  if (F.n !== N) Object.assign(F, { n: N, gen: 0, st: new Int32Array(N), cl: new Int32Array(N), dist: new Float64Array(N), f: new Float64Array(N),
    seq: new Int32Array(N), prev: new Int32Array(N), hp: new Int32Array(N), heap: new Int32Array(N), fs: new Int32Array(N), fv: new Uint8Array(N),
    es: new Int32Array(N * 2), ev: new Uint8Array(N * 2) });
  const gen = ++F.gen, { st, cl, dist, f, seq, prev, hp, heap, fs, fv, es, ev } = F, g0 = g[0], g1 = g[1], gi = g0 * D + g1;
  const hx = (i, j) => Math.hypot(i - g0, j - g1);
  const isFree = (i, j) => { if (i < 0 || j < 0 || i >= W || j >= D) return false; const k = i * D + j; if (fs[k] !== gen) { fs[k] = gen; fv[k] = free(i, j) ? 1 : 0; } return fv[k] === 1; };
  const edge = (i, j, i2, j2) => {                      // edgeOpen, keyed as it keys EDGES: a vertical edge by (max i, j), a horizontal one by (i, max j)
    const k = i2 !== i ? (Math.max(i, i2) * D + j) * 2 : (i * D + Math.max(j, j2)) * 2 + 1;
    if (es[k] !== gen) { es[k] = gen; ev[k] = edgeOpen(i, j, i2, j2, who) ? 1 : 0; } return ev[k] === 1;
  };
  let av = null;
  if (avoid && avoid.size) { av = new Set(); for (const k of avoid) { const [a, b] = String(k).split(',').map(Number); if (onGrid([a, b])) av.add(a * D + b); } }
  let hn = 0, sq = 0;
  const less = (a, b) => f[a] < f[b] || f[a] === f[b] && seq[a] < seq[b];
  const up = k => { const x = heap[k]; while (k > 0) { const q = (k - 1) >> 1, y = heap[q]; if (!less(x, y)) break; heap[k] = y; hp[y] = k; k = q; } heap[k] = x; hp[x] = k; };
  const down = k => { const x = heap[k]; for (;;) { let c = 2 * k + 1; if (c >= hn) break; if (c + 1 < hn && less(heap[c + 1], heap[c])) c++; if (!less(heap[c], x)) break; heap[k] = heap[c]; hp[heap[k]] = k; k = c; } heap[k] = x; hp[x] = k; };
  const si = s[0] * D + s[1];
  st[si] = gen; dist[si] = 0; f[si] = 0 + hx(s[0], s[1]); seq[si] = sq++; prev[si] = -1; heap[hn++] = si; hp[si] = 0;
  while (hn) {
    const c = heap[0], last = heap[--hn]; if (hn) { heap[0] = last; hp[last] = 0; down(0); }
    cl[c] = gen;
    if (c === gi) break;
    const c0 = (c / D) | 0, c1 = c - c0 * D;
    for (const [di, dj] of FP_DIRS) {
      const n0 = c0 + di, n1 = c1 + dj;
      if (!isFree(n0, n1)) continue;
      const n = n0 * D + n1;
      if (av && av.has(n) || cl[n] === gen) continue;
      if (di && dj) {
        if (!isFree(c0 + di, c1) || !isFree(c0, c1 + dj)) continue;
        if (!edge(c0, c1, c0 + di, c1) || !edge(c0 + di, c1, n0, n1) || !edge(c0, c1, c0, c1 + dj) || !edge(c0, c1 + dj, n0, n1)) continue;
      } else if (!edge(c0, c1, n0, n1)) continue;
      const nd = dist[c] + (di && dj ? 1.414 : 1);
      if (st[n] !== gen) { st[n] = gen; dist[n] = nd; f[n] = nd + hx(n0, n1); seq[n] = sq++; prev[n] = c; heap[hn] = n; hp[n] = hn++; up(hn - 1); }
      else if (nd < dist[n]) { dist[n] = nd; f[n] = nd + hx(n0, n1); prev[n] = c; up(hp[n]); }
    }
  }
  if (st[gi] !== gen) return null;
  const path = []; for (let k = gi; prev[k] >= 0;) { k = prev[k]; path.push([(k / D) | 0, k % D]); }
  path.reverse(); path.push(g);
  return path.slice(1);
}
// the search before 0.27.29: the open list scanned for the lowest f each step
function findPathScan(s, g, avoid, who) {
  const key = (i, j) => i + ',' + j, dist = new Map([[key(...s), 0]]), prev = new Map(), open = [s], closed = new Set();
  const hx = (a) => Math.hypot(a[0] - g[0], a[1] - g[1]);
  while (open.length) {
    let bi = 0, bf = Infinity;
    for (let k = 0; k < open.length; k++) { const f = dist.get(key(...open[k])) + hx(open[k]); if (f < bf) { bf = f; bi = k; } }
    const c = open.splice(bi, 1)[0], ck = key(...c);
    if (closed.has(ck)) continue; closed.add(ck);
    if (c[0] === g[0] && c[1] === g[1]) break;
    for (const [di, dj] of [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]]) {
      const n = [c[0] + di, c[1] + dj], nk = key(...n);
      if (!free(...n) || (avoid && avoid.has(nk)) || closed.has(nk)) continue;
      if (di && dj) {
        if (!free(c[0] + di, c[1]) || !free(c[0], c[1] + dj)) continue;
        if (!edgeOpen(c[0], c[1], c[0] + di, c[1], who) || !edgeOpen(c[0] + di, c[1], n[0], n[1], who) ||
            !edgeOpen(c[0], c[1], c[0], c[1] + dj, who) || !edgeOpen(c[0], c[1] + dj, n[0], n[1], who)) continue;
      } else if (!edgeOpen(c[0], c[1], n[0], n[1], who)) continue;
      const nd = dist.get(ck) + (di && dj ? 1.414 : 1);
      if (!dist.has(nk) || nd < dist.get(nk)) { dist.set(nk, nd); prev.set(nk, c); open.push(n); }
    }
  }
  const gk = key(...g); if (!dist.has(gk)) return null;
  const path = [g]; let k = gk; while (prev.has(k)) { const p = prev.get(k); path.unshift(p); k = key(...p); }
  return path.slice(1);
}

// free movement (press and hold): a circle pushed out of blocked tiles, walls and door frames
const BODY_R = .2;
function pushOutBox(p, minx, maxx, minz, maxz, r) {
  const qx = Math.max(minx, Math.min(p.x, maxx)), qz = Math.max(minz, Math.min(p.z, maxz));
  const dx = p.x - qx, dz = p.z - qz, d = Math.hypot(dx, dz);
  if (d >= r) return;
  if (d < 1e-5) {                                        // centre inside the box: leave by the nearest side
    const l = p.x - minx, rr = maxx - p.x, tp = p.z - minz, b = maxz - p.z, m = Math.min(l, rr, tp, b);
    if (m === l) p.x = minx - r; else if (m === rr) p.x = maxx + r; else if (m === tp) p.z = minz - r; else p.z = maxz + r;
    return;
  }
  p.x = qx + dx / d * r; p.z = qz + dz / d * r;
}
const wallish = e => e && e.type !== 'open' && e.type !== 'hull';
// furniture and closed-off areas block as squares; tiles the hull only clips are left to pushOutHull
const solidTile = (i, j) => { const r = roomAt(i, j); return !r || !!ROOMS[r].void || BLOCKED.has(i + ',' + j); };
const innerBlocks = (e, who) => edgeBlocks(e, who) && e.type !== 'hull';
function pushOutHull(p, r) {                             // keep a body inside the hull wall's inner face
  const need = r + T / 2;
  for (const s of HULL_SEGS) {
    const x = p.x + OX, z = p.z + OZ, t = ((x - s.ax) * s.dx + (z - s.az) * s.dz) / s.l2;
    if (t < -.02 || t > 1.02) continue;
    const d = (x - s.ax) * s.nx + (z - s.az) * s.nz;
    if (d < need && d > -1) { p.x += s.nx * (need - d); p.z += s.nz * (need - d); }
  }
}
function collide(p, r, who) {
  for (let pass = 0; pass < 2; pass++) {
    const ci = Math.floor(p.x + OX), cj = Math.floor(p.z + OZ);
    for (let j = cj - 1; j <= cj + 2; j++) for (let i = ci - 1; i <= ci + 2; i++) {
      if (j <= cj + 1 && i <= ci + 1 && solidTile(i, j)) {
        const sn = SNUG.get(i + ',' + j);                 // snug pieces push you off their own outline, not the whole tile
        if (sn) for (const b of sn) pushOutBox(p, b[0], b[1], b[2], b[3], r);
        else pushOutBox(p, X0(i), X0(i + 1), Z0(j), Z0(j + 1), r);
      }
      if (i <= ci + 1 && innerBlocks(EDGES.get(`h,${i},${j}`), who)) pushOutBox(p, X0(i), X0(i + 1), Z0(j) - T / 2, Z0(j) + T / 2, r);
      if (j <= cj + 1 && innerBlocks(EDGES.get(`v,${i},${j}`), who)) pushOutBox(p, X0(i) - T / 2, X0(i) + T / 2, Z0(j), Z0(j + 1), r);
      const touch = [`h,${i - 1},${j}`, `h,${i},${j}`, `v,${i},${j - 1}`, `v,${i},${j}`].map(k => EDGES.get(k));
      if (touch.some(wallish) && !liftJoint(touch.filter(Boolean))) { const c = (1 - SEG) / 2 + .02; pushOutBox(p, X0(i) - c, X0(i) + c, Z0(j) - c, Z0(j) + c, r); }
    }
    for (const sg of CURVE_SEGS) {                       // curved walls and counters
      if (Math.abs(p.x - sg.ax) > 2 || Math.abs(p.z - sg.az) > 2) continue;
      const dx = sg.bx - sg.ax, dz = sg.bz - sg.az, l2 = dx * dx + dz * dz || 1e-9, t = THREE.MathUtils.clamp(((p.x - sg.ax) * dx + (p.z - sg.az) * dz) / l2, 0, 1);
      const qx = sg.ax + dx * t, qz = sg.az + dz * t, ex = p.x - qx, ez = p.z - qz, d = Math.hypot(ex, ez), m = sg.h + r;
      if (d < m && d > 1e-6) { p.x = qx + ex / d * m; p.z = qz + ez / d * m; }
    }
    pushOutHull(p, r);
  }
}

