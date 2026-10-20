// =====================================================================
// 4c. BUILD AND UNLOAD A DECK
// buildDeck(def) makes def the current deck: fills the state in 4a, puts
// all of the deck's 3D under deckRoot, then furnishes it with def.dress().
// unloadDeck() takes the current deck apart again.
// Rule: shared kit must be made before the first buildDeck(). Anything a
// build creates belongs to that deck and is freed when it unloads.
// =====================================================================
function buildDeck(def) {
  deckDef = def;
  // three.js numbers every geometry, material and texture in order; whatever this build makes comes after these
  deckMark = { geo: new THREE.BufferGeometry().id, mat: new THREE.Material().id, tex: new THREE.Texture().id };
  seed = def.seed;                                       // a deck comes out the same every time it's built
  deckRoot = new THREE.Group(); scene.add(deckRoot);
  ROOMS = def.rooms; WINDOWS = def.windows; HULL = def.hull;
  DOORS = Object.assign({}, def.doors); CLOSED_DOORS = Object.assign({}, def.closedDoors);
  for (const key of shipDeck(def.num).open) if (DOORS[key] === 'closed' || DOORS[key] === 'hatch') { DOORS[key] = 'door'; delete CLOSED_DOORS[key]; }   // unlocked since
  W = def.map[0].length; D = def.map.length; WALL_K = def.tall || 1; H = 2.8 * WALL_K;
  OX = def.lift[0] - LIFT_AT[0]; OZ = def.lift[1] - LIFT_AT[1];
  LAMPS = []; STEAM = []; DUST = []; glows.length = 0;

  // ---- hull outline ----
  HULL_PTS = [];          // closed outline, clockwise on screen: port side, bow, starboard side, stern
  {
    const add = (x, z) => { const p = HULL_PTS[HULL_PTS.length - 1]; if (!p || Math.hypot(p[0] - x, p[1] - z) > 1e-3) HULL_PTS.push([x, z]); };
    const r = HULL.stern, st = .125, x0 = HULL.sternX;
    for (let x = x0 + r; x < HULL.bowFrom; x += st) add(x, 0);
    for (let k = 0; k <= 72; k++) { const a = -Math.PI / 2 + Math.PI * k / 72; add(HULL.bowFrom + HULL.bowLen * Math.cos(a), D / 2 + D / 2 * Math.sin(a)); }
    for (let x = HULL.bowFrom; x > x0 + r; x -= st) add(x, D);
    for (let k = 0; k <= 12; k++) { const a = Math.PI / 2 + Math.PI / 2 * k / 12; add(x0 + r + r * Math.cos(a), D - r + r * Math.sin(a)); }
    for (let z = D - r; z > r; z -= st) add(x0, z);
    for (let k = 0; k < 12; k++) { const a = Math.PI + Math.PI / 2 * k / 12; add(x0 + r + r * Math.cos(a), r + r * Math.sin(a)); }
  }
  HULL_SEGS = HULL_PTS.map(([ax, az], k) => {
    const [bx, bz] = HULL_PTS[(k + 1) % HULL_PTS.length], dx = bx - ax, dz = bz - az, l = Math.hypot(dx, dz);
    return { ax, az, bx, bz, dx, dz, l2: l * l, l, nx: -dz / l, nz: dx / l };   // n points into the deck
  });
  MAP = def.map.map((row, j) => [...row].map((c, i) => tileInHull(i, j) ? c : '.').join(''));
  STAND = new Set();         // tiles whose centre sits well inside the hull, where people can stand
  for (let j = 0; j < D; j++) for (let i = 0; i < W; i++) if (hullDist(i + .5, j + .5) > .45) STAND.add(i + ',' + j);
  for (const [key, type] of Object.entries(DOORS)) {          // locked rooms say what they are
    if ((type !== 'closed' && type !== 'hatch') || CLOSED_DOORS[key] || !def.lockedRoom || (def.service || []).some(sv => (sv.key || sv) === key)) continue;
    const [k, a, b] = key.split(','), i = +a, j = +b, r = (k === 'h' ? [roomAt(i, j - 1), roomAt(i, j)] : [roomAt(i - 1, j), roomAt(i, j)]).find(r => r && !ROOMS[r].hall);
    if (r) CLOSED_DOORS[key] = def.lockedRoom(r);
  }
  ROOM_BOX = {};                                           // per room: first tile and size
  for (let j = 0; j < D; j++) for (let i = 0; i < W; i++) {
    const r = roomAt(i, j); if (!r) continue;
    const b = ROOM_BOX[r] || (ROOM_BOX[r] = { i0: i, j0: j, i1: i, j1: j });
    b.i0 = Math.min(b.i0, i); b.j0 = Math.min(b.j0, j); b.i1 = Math.max(b.i1, i); b.j1 = Math.max(b.j1, j);
  }

  // ---- edges ----
  EDGES = new Map();
  for (let j = 0; j <= D; j++) for (let i = 0; i < W; i++) addEdge(`h,${i},${j}`, true, i, j, roomAt(i, j - 1), roomAt(i, j));
  for (let j = 0; j < D; j++) for (let i = 0; i <= W; i++) addEdge(`v,${i},${j}`, false, i, j, roomAt(i - 1, j), roomAt(i, j));
  for (const sv of def.service || []) { const key = sv.key || sv, e = EDGES.get(key); if (e && e.type === 'hatch') { e.service = true; e.tier = sv.tier || 0; delete CLOSED_DOORS[key]; } }   // service hatches (see hatchPassable); an entry is a key, or { key, tier } (0.30.12)

  // ---- floor: one texture for the whole deck, with wall shading baked in ----
  const PX = 64;
  const FTW = W * PX > 2048 ? 4096 : 2048, FTH = D * PX > 1024 ? 2048 : 1024;
  const deckFloorTex = tex(FTW, FTH, (g) => {
    g.fillStyle = '#1c2128'; g.fillRect(0, 0, FTW, FTH);
    for (let j = 0; j < D; j++) for (let i = 0; i < W; i++) {
      const r = roomAt(i, j), x = i * PX, y = j * PX, st = ROOMS[r];
      if (def.floorSeeds && i === def.floorSeeds.col && j < def.floorSeeds.rows.length) seed = def.floorSeeds.rows[j];   // a deck whose floor changed west of this column keeps its old grain (and its later random sequence) east of it
      if (!r) continue;
      if (st.void) { g.fillStyle = '#23272d'; g.fillRect(x, y, PX, PX); continue; }
      if (st.rec) { recFloor(g, st.floor, i, j, x, y, PX); continue; }   // the rec deck's floors (0.80.0): no R()
      const v = st.floor === 'lift' || st.spine || st.still ? 0 : (R() - .5) * 8;   // the lift car (and `still` floors, such as utility rooms built later) draw nothing from the deck's random sequence, so the rest of the deck is unchanged
      if (st.floor === 'warm') {
        if ((i % 2 === 0) && (j % 2 === 0)) { g.fillStyle = '#4a413a'; g.fillRect(x, y, PX * 2, PX * 2); }
        g.fillStyle = `rgb(${132 + v},${118 + v},${104 + v})`; g.fillRect(x + (i % 2 ? 0 : 2), y + (j % 2 ? 0 : 2), PX - 2, PX - 2);
        if (i % 2 === 0 && j % 2 === 0) { g.strokeStyle = 'rgba(0,0,0,.08)'; g.lineWidth = 2; g.strokeRect(x + 14, y + 14, PX * 2 - 28, PX * 2 - 28); }
      } else if (st.floor === 'plate') {
        g.fillStyle = '#3b4148'; g.fillRect(x, y, PX, PX);
        g.fillStyle = `rgb(${112 + v},${119 + v},${124 + v})`; g.fillRect(x + 2, y + 2, PX - 4, PX - 4);
        g.fillStyle = 'rgba(255,255,255,.06)'; g.fillRect(x + 2, y + 2, PX - 4, 2);
        g.fillStyle = 'rgba(0,0,0,.07)'; for (let a = 10; a < PX - 8; a += 14) for (let b = 10; b < PX - 8; b += 14) g.fillRect(x + a, y + b, 6, 2);
      } else if (st.floor === 'wood') {
        for (let k = 0; k < 4; k++) {
          const pv = (R() - .5) * 18;
          g.fillStyle = `rgb(${128 + pv},${92 + pv * .8},${64 + pv * .6})`; g.fillRect(x, y + k * 16, PX, 15);
          g.fillStyle = 'rgba(40,24,14,.35)'; g.fillRect(x, y + k * 16 + 15, PX, 1);
          if (R() < .4) g.fillRect(x + Math.floor(R() * PX), y + k * 16, 1.5, 15);
        }
      } else if (st.floor === 'mess') {
        const alt = (i + j) % 2;
        g.fillStyle = '#5a4e44'; g.fillRect(x, y, PX, PX);
        for (let a = 0; a < 2; a++) for (let b = 0; b < 2; b++) {
          g.fillStyle = (a + b + alt) % 2 ? `rgb(${190 + v},${172 + v},${142 + v})` : `rgb(${168 + v},${144 + v},${112 + v})`;
          g.fillRect(x + a * 32 + 1, y + b * 32 + 1, 30, 30);
        }
      } else if (st.floor === 'tile') {
        g.fillStyle = '#7d898c'; g.fillRect(x, y, PX, PX);
        for (let a = 0; a < 4; a++) for (let b = 0; b < 4; b++) {
          const t = (R() - .5) * 10; g.fillStyle = `rgb(${190 + t},${201 + t},${200 + t})`; g.fillRect(x + a * 16 + 1, y + b * 16 + 1, 14, 14);
        }
      } else if (st.floor === 'steel' || st.floor === 'haul' || st.floor === 'bay') {
        // diamond plate: raised bars in alternating directions, lit on one edge
        const base = st.floor === 'bay' ? 92 : 104;
        g.fillStyle = '#3c4249'; g.fillRect(x, y, PX, PX);
        g.fillStyle = `rgb(${base + v},${base + 6 + v},${base + 12 + v})`; g.fillRect(x + 1, y + 1, PX - 2, PX - 2);
        g.lineWidth = 2.5;
        for (let a = 0; a < 4; a++) for (let b = 0; b < 4; b++) {
          const px0 = x + a * 16 + 4, py0 = y + b * 16 + 4, d = (a + b) % 2;
          g.strokeStyle = 'rgba(0,0,0,.22)'; g.beginPath(); g.moveTo(px0 + 1, py0 + (d ? 9 : 1)); g.lineTo(px0 + 9, py0 + (d ? 1 : 9)); g.stroke();
          g.strokeStyle = 'rgba(255,255,255,.13)'; g.beginPath(); g.moveTo(px0, py0 + (d ? 8 : 0)); g.lineTo(px0 + 8, py0 + (d ? 0 : 8)); g.stroke();
        }
      } else if (st.floor === 'lift') {
        g.fillStyle = '#272d33'; g.fillRect(x, y, PX, PX);
        g.fillStyle = `rgb(${58 + v},${64 + v},${70 + v})`; for (let k = 4; k < PX; k += 10) g.fillRect(x, y + k, PX, 4);
        g.fillStyle = 'rgba(255,255,255,.06)'; for (let k = 4; k < PX; k += 10) g.fillRect(x, y + k, PX, 1);
      } else if (st.floor === 'grate') {
        // open grating over a dark duct: bars every 8 px, a cross bar every half tile
        g.fillStyle = '#15191d'; g.fillRect(x, y, PX, PX);
        g.fillStyle = `rgb(${96 + v},${103 + v},${110 + v})`;
        for (let k = 0; k < PX; k += 8) g.fillRect(x, y + k, PX, 3);
        for (let k = 0; k < PX; k += 32) g.fillRect(x + k, y, 3, PX);
        g.fillStyle = 'rgba(255,255,255,.08)'; for (let k = 0; k < PX; k += 8) g.fillRect(x, y + k, PX, 1);
      } else if (st.floor === 'deck') {
        // the promenade: pale ash planks running fore and aft, with the guide stripe and an inlaid light line by the walls
        g.fillStyle = '#4a4239'; g.fillRect(x, y, PX, PX);
        for (let k = 0; k < 4; k++) {
          const pv = (R() - .5) * 14, off = ((j * 4 + k) * 23) % PX;
          g.fillStyle = `rgb(${172 + pv},${156 + pv * .9},${130 + pv * .8})`; g.fillRect(x, y + k * 16, PX, 15);
          g.fillStyle = 'rgba(60,44,30,.3)'; g.fillRect(x, y + k * 16 + 15, PX, 1); g.fillRect(x + off, y + k * 16, 1.5, 15);
        }
        const hall = (a, b) => { const r2 = roomAt(a, b); return r2 && ROOMS[r2].hall; };
        if (!hall(i, j - 1)) { g.fillStyle = 'rgba(95,214,198,.55)'; g.fillRect(x, y + 10, PX, 3); g.fillStyle = 'rgba(255,236,190,.5)'; g.fillRect(x, y + 18, PX, 2); }
        if (!hall(i, j + 1)) { g.fillStyle = 'rgba(95,214,198,.55)'; g.fillRect(x, y + PX - 13, PX, 3); g.fillStyle = 'rgba(255,236,190,.5)'; g.fillRect(x, y + PX - 20, PX, 2); }
      } else if (st.floor === 'gym') {
        // poured rubber with coloured flecks
        g.fillStyle = `rgb(${46 + v},${51 + v},${57 + v})`; g.fillRect(x, y, PX, PX);
        for (let k = 0; k < 14; k++) { const c = R(); g.fillStyle = c < .5 ? 'rgba(200,210,215,.25)' : c < .8 ? 'rgba(95,214,198,.3)' : 'rgba(233,196,106,.3)'; g.fillRect(x + R() * PX, y + R() * PX, 2, 2); }
        if (i % 3 === 0) { g.fillStyle = 'rgba(0,0,0,.25)'; g.fillRect(x, y, 2, PX); }
      } else if (st.floor === 'garden') {
        // soft grass: a deep green with short blades in lighter and darker greens, and the odd clover
        g.fillStyle = `rgb(${58 + v},${96 + v},${54 + v})`; g.fillRect(x, y, PX, PX);
        for (let k = 0; k < 46; k++) {
          const bx = x + R() * PX, by = y + R() * PX, c = R();
          g.fillStyle = c < .4 ? 'rgba(140,196,96,.55)' : c < .75 ? 'rgba(30,64,36,.45)' : 'rgba(190,222,120,.4)';
          g.fillRect(bx, by, 1.5, 4 + R() * 4);
        }
        if (R() < .25) { g.fillStyle = 'rgba(240,240,220,.6)'; g.beginPath(); g.arc(x + R() * PX, y + R() * PX, 1.6, 0, 6.3); g.fill(); }
      } else if (st.floor === 'bridge') {
        // the bridge (Deck 1): deep blue-grey carpet tiles with a fine woven rib and a dark seam
        g.fillStyle = `rgb(${46 + v * .4},${53 + v * .4},${68 + v * .4})`; g.fillRect(x, y, PX, PX);
        g.fillStyle = 'rgba(170,196,230,.05)'; for (let k = 2; k < PX; k += 6) g.fillRect(x, y + k, PX, 2);
        g.fillStyle = 'rgba(0,0,0,.22)'; g.fillRect(x, y, PX, 1); g.fillRect(x, y, 1, PX);
      } else if (st.floor === 'corridor' || st.floor === 'lobby' || st.floor === 'carpet') {
        const carpet = st.floor === 'carpet';
        if (carpet) {
          g.fillStyle = `rgb(${88 + v * .4},${82 + v * .4},${110 + v * .4})`; g.fillRect(x, y, PX, PX);
          g.fillStyle = 'rgba(255,230,190,.06)';
          g.beginPath(); g.moveTo(x + 32, y + 18); g.lineTo(x + 46, y + 32); g.lineTo(x + 32, y + 46); g.lineTo(x + 18, y + 32); g.closePath(); g.fill();
        } else {
          g.fillStyle = '#3a424b'; g.fillRect(x, y, PX, PX);
          g.fillStyle = st.floor === 'lobby' ? `rgb(${76 + v},${96 + v},${98 + v})` : `rgb(${78 + v},${86 + v},${95 + v})`; g.fillRect(x + 1, y + 1, PX - 2, PX - 2);
          if (i % 4 === 0) { g.fillStyle = 'rgba(0,0,0,.18)'; g.fillRect(x, y, 2, PX); }
        }
        // guide stripe along any side that meets a wall: teal in the junior wing, amber on the officers' carpet
        const hall = (a, b) => { const r2 = roomAt(a, b); return r2 && ROOMS[r2].hall; };
        g.fillStyle = carpet ? 'rgba(233,196,106,.5)' : 'rgba(95,214,198,.55)';
        if (!hall(i, j - 1)) g.fillRect(x, y + 12, PX, 3);
        if (!hall(i, j + 1)) g.fillRect(x, y + PX - 15, PX, 3);
      }
    }
    if (def.hazard) paintHazards(g, PX, def);
    if (def.floorArt) def.floorArt(g, PX);               // a deck's own inlays (Deck 1's command ring); drawn before the wall shading
    if (ROOM_BOX['@']) {                                 // a gold edge round the lift car floor
      const b = ROOM_BOX['@']; g.strokeStyle = 'rgba(217,164,65,.8)'; g.lineWidth = 5;
      g.strokeRect(b.i0 * PX + 6, b.j0 * PX + 6, (b.i1 - b.i0 + 1) * PX - 12, (b.j1 - b.j0 + 1) * PX - 12);
    }
    // soft shading along every wall, so rooms feel grounded
    const sh = 22;
    for (const e of EDGES.values()) {
      if (e.type === 'door' || e.type === 'lift' || e.type === 'open' || e.type === 'hull') continue;
      const px = e.horiz ? e.i * PX : e.i * PX, py = e.j * PX;
      const shadeSide = (x0, y0, x1, y1, rx, ry, rw, rh) => { const r = g.createLinearGradient(x0, y0, x1, y1); r.addColorStop(0, 'rgba(0,0,0,.34)'); r.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = r; g.fillRect(rx, ry, rw, rh); };
      if (e.horiz) { shadeSide(0, py, 0, py + sh, px, py, PX, sh); shadeSide(0, py, 0, py - sh, px, py - sh, PX, sh); }
      else { shadeSide(px, 0, px + sh, 0, px, py, sh, PX); shadeSide(px, 0, px - sh, 0, px - sh, py, sh, PX); }
    }
    // and along the hull: clip to the outline, then stroke it so only the inside darkens
    g.save(); g.beginPath(); HULL_PTS.forEach(([x, z], k) => k ? g.lineTo(x * PX, z * PX) : g.moveTo(x * PX, z * PX)); g.closePath(); g.clip();
    for (const [lw, a] of [[64, .09], [40, .1], [20, .12]]) { g.lineWidth = lw; g.strokeStyle = `rgba(0,0,0,${a})`; g.stroke(); }
    g.restore();
  });
  deckFloorTex.wrapS = deckFloorTex.wrapT = THREE.ClampToEdgeWrapping; deckFloorTex.repeat.set(1, 1);
  HULL_NRM = HULL_PTS.map((p, k) => {                       // smooth inward normal at each outline point
    const a = HULL_SEGS[(k - 1 + HULL_SEGS.length) % HULL_SEGS.length], b = HULL_SEGS[k];
    let nx = a.nx + b.nx, nz = a.nz + b.nz; const l = Math.hypot(nx, nz) || 1; nx /= l; nz /= l;
    const m = 1 / Math.max(.5, nx * b.nx + nz * b.nz); return { nx, nz, m };
  });
  {
    const ring = hullRing(-HULL_OUT), tris = THREE.ShapeUtils.triangulateShape(ring.map(([x, z]) => new THREE.Vector2(x, z)), []);
    const P = [], U = [], N = [];
    for (const t of tris) {
      let [a, b, c] = t; const A = ring[a], B = ring[b], C = ring[c];
      if ((B[0] - A[0]) * (C[1] - A[1]) - (B[1] - A[1]) * (C[0] - A[0]) > 0) [b, c] = [c, b];   // face up
      for (const k of [a, b, c]) { const [x, z] = ring[k]; P.push(x - OX, 0, z - OZ); N.push(0, 1, 0); U.push(x * PX / FTW, 1 - z * PX / FTH); }
    }
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.Float32BufferAttribute(P, 3)); geo.setAttribute('normal', new THREE.Float32BufferAttribute(N, 3)); geo.setAttribute('uv', new THREE.Float32BufferAttribute(U, 2));
    floor = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({ map: deckFloorTex, roughness: .75 })); floor.receiveShadow = true; deckRoot.add(floor);
    const shape = new THREE.Shape(hullRing(-HULL_OUT - .12).map(([x, z]) => new THREE.Vector2(x - OX, z - OZ)));
    const slab = new THREE.Mesh(new THREE.ExtrudeGeometry(shape, { depth: .3, bevelEnabled: false, curveSegments: 1 }), M.slateDark);
    slab.rotation.x = Math.PI / 2; slab.position.y = -.04; slab.receiveShadow = true; deckRoot.add(slab);
  }

  // ---- walls, door frames and posts ----
  edgeList = [...EDGES.values()].filter(e => e.type !== 'hull');
  // inner walls that run into a curved stretch of hull are cut short, running just into the hull wall
  for (const e of edgeList) {
    const ax = e.i, az = e.j, bx = e.horiz ? e.i + 1 : e.i, bz = e.horiz ? e.j : e.j + 1;
    const ina = hullDist(ax, az) > 0, inb = hullDist(bx, bz) > 0;
    e.wx = e.cx; e.wz = e.cz; e.sx = 1;
    if (ina === inb) continue;
    const [x0, z0, x1, z1] = ina ? [ax, az, bx, bz] : [bx, bz, ax, az];
    let lo = 0, hi = 1;
    for (let k = 0; k < 20; k++) { const m = (lo + hi) / 2; if (hullDist(x0 + (x1 - x0) * m, z0 + (z1 - z0) * m) > 0) lo = m; else hi = m; }
    const len = Math.min(1, lo + .3);
    e.sx = len / SEG > 1 ? 1 : len; e.wx = x0 + (x1 - x0) * len / 2 - OX; e.wz = z0 + (z1 - z0) * len / 2 - OZ;
  }
  wallEdges = edgeList.filter(e => e.type === 'wall');
  frameEdges = edgeList.filter(e => e.type !== 'wall' && e.type !== 'window');   // doors, lifts, hatches and glass all carry a header
  glassEdges = edgeList.filter(e => e.type === 'glass' || e.type === 'pass'); sillIM = paneIM = null;   // a pass is glass with no pane
  if (glassEdges.length) {
    const sm = [capMat, capMat, M.trim, capMat, wallMat, wallMat]; sillIM = new THREE.InstancedMesh(packGroups(sillGeo, sm), sm, glassEdges.length);
    paneIM = new THREE.InstancedMesh(paneGeo, paneMat, glassEdges.length);
    glassEdges.forEach((e, k) => e.ginst = k);
    sillIM.castShadow = sillIM.receiveShadow = true; deckRoot.add(sillIM, paneIM);
  }
  const wm = [capMat, capMat, capMat, capMat, wallMat, wallMat];   // 0.27.20: packGroups, 6 calls to 2
  wallIM = new THREE.InstancedMesh(packGroups(wallGeo, wm), wm, wallEdges.length);
  hdrIM = new THREE.InstancedMesh(packGroups(hdrGeo, wm), wm, frameEdges.length);
  wallEdges.forEach((e, k) => e.inst = k); frameEdges.forEach((e, k) => e.hinst = k);
  // posts at every corner where walls meet
  POSTS = [];
  for (let j = 0; j <= D; j++) for (let i = 0; i <= W; i++) {
    const touch = [`h,${i - 1},${j}`, `h,${i},${j}`, `v,${i},${j - 1}`, `v,${i},${j}`].map(wallE).filter(Boolean);
    if (!touch.length || !inHull(i, j)) continue;           // where a wall meets the hull, the hull wall covers its end
    const solid = !liftJoint(touch) && touch.some(e => e.type !== 'open' && !(e.type === 'window' && touch.every(t => t.type === 'window')));
    POSTS.push({ cx: X0(i), cz: Z0(j), full: solid, s: 1, touch });
  }
  // wall runs: straight stretches of wall between two junctions. A run drops as one
  // piece, so a room's wall never comes down halfway, and posts follow the walls they join.
  RUNS = [];
  for (const horiz of [true, false]) {
    const lines = horiz ? D + 1 : W + 1, len = horiz ? W : D;
    for (let L = 0; L < lines; L++) {
      let run = null;
      for (let k = 0; k <= len; k++) {
        const e = k < len ? wallE(horiz ? `h,${k},${L}` : `v,${L},${k}`) : null;
        if (run && (!e || junction(horiz ? k : L, horiz ? L : k, horiz))) { finishRun(run); run = null; }
        if (!e) continue;
        if (!run) run = { edges: [], out: e.out };
        run.edges.push(e); e.run = run;
      }
    }
  }
  fullPosts = POSTS.filter(p => p.full); hdrPosts = POSTS.filter(p => !p.full);
  postIM = new THREE.InstancedMesh(postGeo, capMat, fullPosts.length);
  hpostIM = new THREE.InstancedMesh(hpostGeo, capMat, hdrPosts.length);
  for (const im of [wallIM, hdrIM, postIM, hpostIM]) { im.castShadow = im.receiveShadow = true; deckRoot.add(im); }
  writeWalls();

  // ---- door leaves ----
  // Lift edges side by side make one wide door: a single pair of leaves across both, built on the first edge.
  DOOR_OBJS = [];
  const liftNext = (e, d) => { const n = EDGES.get(e.horiz ? `h,${e.i + d},${e.j}` : `v,${e.i},${e.j + d}`); return n && n.type === 'lift' ? n : null; };
  for (const e of frameEdges) {
    if (e.type === 'open' || e.type === 'glass' || e.type === 'pass' || (e.type === 'lift' && liftNext(e, -1))) continue;
    const run = [e]; if (e.type === 'lift') for (let n = liftNext(e, 1); n; n = liftNext(n, 1)) run.push(n);
    const last = run[run.length - 1], span = SEG + run.length - 1, cx = (e.cx + last.cx) / 2, cz = (e.cz + last.cz) / 2;
    const g = new THREE.Group(); g.position.set(cx, 0, cz); g.rotation.y = e.horiz ? 0 : Math.PI / 2; deckRoot.add(g);
    const mats = e.type === 'lift' ? liftLeafMats : e.type === 'hatch' ? hatchLeafMats : leafMats, leaves = [];
    for (const sd of [-1, 1]) {
      const m = mats[sd < 0 ? 0 : 1];
      const leaf = new THREE.Mesh(new THREE.BoxGeometry(span / 2, 2.2, .07), HIT_MAT); leaf.userData.leaf = { m, sx: span / 2 };   // drawn by DOOR_LEAVES
      leaf.position.set(sd * span / 4, 1.1, sd * .012); g.add(leaf); leaves.push(leaf);
    }
    if (e.type === 'door' || e.type === 'lift') {
      const th = new THREE.Mesh(new THREE.BoxGeometry(span - .1, .02, .1), thrMat); th.position.set(0, .01, 0); deckRoot.add(th); th.position.add(g.position); th.rotation.y = g.rotation.y;
    }
    const hit = new THREE.Mesh(new THREE.BoxGeometry(span, 2.2, .3), new THREE.MeshBasicMaterial({ visible: false })); hit.position.y = 1.1; g.add(hit);
    if (CLOSED_DOORS[e.key]) hit.userData.closedDoor = e.key;
    if ((YOU_LOCKS[def.num] || []).some(L => L.keys.includes(e.key))) hit.userData.youLock = e.key;   // 0.47.11: shut to you until let in
    if (e.type === 'lift') hit.userData.liftDoor = e.key;
    DOOR_OBJS.push({ e, g, leaves, open: 0, passable: e.type === 'door' || e.type === 'lift', svc: !!e.service, cx, cz, span });
  }
  DOOR_LEAVES = [];                                      // 0.27.21: one InstancedMesh per leaf material (2 draw calls each, not 2 a leaf)
  for (const m of new Set(DOOR_OBJS.flatMap(d => d.leaves.map(l => l.userData.leaf.m)))) {
    const list = DOOR_OBJS.flatMap(d => d.leaves).filter(l => l.userData.leaf.m === m);
    const im = new THREE.InstancedMesh(DOOR_LEAF_GEO, [capMat, capMat, capMat, capMat, m, m], list.length);
    im.castShadow = true; im.frustumCulled = false; im.raycast = () => {}; deckRoot.add(im); DOOR_LEAVES.push({ im, list });
  }

  // ---- the hull wall: a thick ribbon along the outline, split into runs by the room inside it ----
  // Each run is its own mesh so it can drop for the cutaway. Windows are openings in the ribbon,
  // so they follow the curve: sill, head trim, mullions, glass, and space beyond.
  HULL_RUNS = []; HULL_MESHES = [];
  {
    const NS = HULL_SEGS.length;
    // which room each stretch of hull belongs to
    const segRoom = HULL_SEGS.map(s => {
      const mx = (s.ax + s.bx) / 2, mz = (s.az + s.bz) / 2;
      for (const d of [.6, 1.1, 1.6]) { const r = roomAt(Math.floor(mx + s.nx * d), Math.floor(mz + s.nz * d)); if (r) return r; }
      return null;
    });
    let k0 = 0; while (k0 < NS && segRoom[k0] === segRoom[(k0 - 1 + NS) % NS]) k0++;
    if (k0 === NS) k0 = 0;
    const runs = [];
    for (let n = 0; n < NS; n++) {
      const k = (k0 + n) % NS;
      if (!runs.length || runs[runs.length - 1].room !== segRoom[k]) runs.push({ room: segRoom[k], segs: [] });
      runs[runs.length - 1].segs.push(k);
    }
    const isWin = (w, run, k, s0, s1, sMid) => {
      if (sMid - s0 < .4 || s1 - sMid < .4) return false;   // keep clear of the corners
      const s = HULL_SEGS[k], mx = (s.ax + s.bx) / 2, mz = (s.az + s.bz) / 2;
      if (w.room) return run.room === w.room;
      if (w.side === 'n') return mz < .01 && mx > w.a && mx < w.b;
      if (w.side === 's') return mz > D - .01 && mx > w.a && mx < w.b;
      if (w.side === 'w') return mx < HULL.sternX + .01 && mz > w.a && mz < w.b;
      return false;
    };
    const faceMats = [wallMat, hullOutMat, capMat], trimMats = [M.trim, M.trim, M.trim], darkMats = [M.slateDark, M.slateDark, M.slateDark];
    for (const run of runs) {
      // arc lengths along the run, and window flags
      let acc = 0; const sA = run.segs.map(k => { const v = acc; acc += HULL_SEGS[k].l; return v; }), total = acc;
      const win = run.segs.map((k, n) => { const m = sA[n] + HULL_SEGS[k].l / 2; const w = WINDOWS.find(w => isWin(w, run, k, 0, total, m)); return w || null; });
      // a run is split again wherever the hull turns to face a new way (fore, aft, port, starboard), so
      // each piece can follow the camera on its own. R() is still drawn once per span, as before.
      const faceOf = k => { const s = HULL_SEGS[k]; return Math.abs(s.nx) >= Math.abs(s.nz) ? (s.nx > 0 ? 1 : 0) : (s.nz > 0 ? 3 : 2); };
      const FACE = [[1, 0], [-1, 0], [0, 1], [0, -1]];      // outward: bow, stern, +z side, -z side
      // (part[] is overwritten with piece numbers as it goes, so older decks split far more often than they need to;
      // a deck with hull.byFace compares the facings themselves and gets one piece per facing. Decks 3-6 keep the old split.)
      const part = run.segs.map(faceOf), fc = part.slice(), parts = [];
      run.segs.forEach((k, n) => { if (!n || (HULL.byFace ? fc[n] !== fc[n - 1] : part[n] !== part[n - 1])) parts.push({ face: part[n], g: new THREE.Group(), decor: new THREE.Group(), segs: [] }); parts[parts.length - 1].segs.push(k); part[n] = parts.length - 1; });
      for (const p of parts) { deckRoot.add(p.g); deckRoot.add(p.decor); }
      // split into spans of wall or window
      let n = 0;
      while (n < run.segs.length) {
        const w = win[n]; let e = n; while (e < run.segs.length && win[e] === w) e++;
        const idx = run.segs.slice(n, e).map(k => k); idx.push((run.segs[e - 1] + 1) % NS);
        const arc0 = sA[n], len = (e < run.segs.length ? sA[e] : total) - arc0;
        // the span's pieces, one per facing it crosses
        const pieces = []; for (let a = n; a < e;) { let b = a; while (b < e && part[b] === part[a]) b++; const ix = run.segs.slice(a, b); ix.push((run.segs[b - 1] + 1) % NS); pieces.push({ p: parts[part[a]], ix, arc: sA[a] }); a = b; }
        if (!w) for (const pc of pieces) pc.p.g.add(hullStrip(pc.ix, 0, H, T / 2, -HULL_OUT, faceMats, { arc0: pc.arc }));
        else {
          R();                                          // (once painted space behind the glass; the draw keeps the random sequence)
          for (const pc of pieces) {
            const { g, decor } = pc.p, ix = pc.ix, arc = pc.arc;
            g.add(hullStrip(ix, 0, 1.0, T / 2, -HULL_OUT, faceMats, { arc0: arc }));
            g.add(hullStrip(ix, 2.2, H, T / 2, -HULL_OUT, faceMats, { arc0: arc }));
            decor.add(hullStrip(ix, .985, 1.1, T / 2 + .18, T / 2 - .12, trimMats, { arc0: arc }));        // sill
            decor.add(hullStrip(ix, 2.17, 2.28, T / 2 + .06, T / 2 - .12, trimMats, { arc0: arc }));       // head trim
            const glass = hullStrip(ix, 1.0, 2.2, .005, -.005, [glassMat, glassMat, glassMat], { shadow: false }); glass.castShadow = false; decor.add(glass);
          }
          // mullions about every metre, each with the piece it stands in
          const nm = Math.max(1, Math.round(len)), pts = idx.map(k => HULL_PTS[k]);
          for (let q = 1; q < nm; q++) {
            const target = len * q / nm; let walked = 0, kk = 0;
            while (kk < idx.length - 2 && walked + HULL_SEGS[idx[kk]].l < target) { walked += HULL_SEGS[idx[kk]].l; kk++; }
            const sg = HULL_SEGS[idx[kk]], t = Math.min(1, (target - walked) / sg.l), x = sg.ax + sg.dx * t, z = sg.az + sg.dz * t;
            const mu = box(.05, 1.18, .08, M.trim, x - OX, 1.6, z - OZ, parts[part[n + kk]].decor); mu.rotation.y = Math.atan2(sg.dx, sg.dz);
          }
          if (w.dust) {
            const mk = Math.floor(idx.length / 2), mid = HULL_SEGS[idx[mk]], d = makeDust(len);
            d.position.set(mid.ax + mid.nx * T / 2 - OX, 0, mid.az + mid.nz * T / 2 - OZ); d.rotation.y = Math.atan2(mid.nx, mid.nz); parts[part[Math.min(e - 1, n + mk)]].decor.add(d);
          }
        }
        n = e;
      }
      for (const p of parts) {
        mergeMeshes(p.g);                                 // 0.27.20: one mesh per material for each piece (was one per strip); the decor is merged below
        p.g.traverse(o => { if (o.isMesh) HULL_MESHES.push(o); });
        // the hull doesn't follow you: pieces facing the camera stay low, the rest stay up
        let ox = 0, oz = 0; const edges = [];
        p.segs.forEach((k, q) => { const s = HULL_SEGS[k]; ox -= s.nx * s.l; oz -= s.nz * s.l; edges.push({ cx: s.ax + s.dx / 2 - OX, cz: s.az + s.dz / 2 - OZ }); });
        const ol = Math.hypot(ox, oz) || 1;
        const hr = { edges, out: [ox / ol, oz / ol], face: FACE[p.face], g: p.g, decor: p.decor, s: 1, cut: false, room: run.room };
        HULL_RUNS.push(hr); RUNS.push(hr);
      }
    }
    // wall decor and windows hung on hull edges follow the hull run they belong to
    for (const e of EDGES.values()) {
      if (e.type !== 'hull') continue;
      let best = null, bd = 1e9;
      for (const hr of HULL_RUNS) for (const p of hr.edges) { const d = (p.cx - e.cx) ** 2 + (p.cz - e.cz) ** 2 + (e.out && (hr.face[0] !== e.out[0] || hr.face[1] !== e.out[1]) ? 4 : 0); if (d < bd) { bd = d; best = hr; } }
      e.hrun = best;
    }
  }

  // ---- solid blocks over areas you can't enter ----
  VOID_BLOCKS = [];
  for (const [i, j, w, d] of Object.entries(ROOM_BOX).filter(([k]) => ROOMS[k].void).map(([, b]) => [b.i0, b.j0, b.i1 - b.i0 + 1, b.j1 - b.j0 + 1])) {
    const t = hatchTex.clone(); t.needsUpdate = true; t.repeat.set(w / 2, d / 2);
    const top = new THREE.MeshStandardMaterial({ map: t, roughness: .9 });
    const vm = [capMat, capMat, top, capMat, capMat, capMat], m = new THREE.Mesh(packGroups(new THREE.BoxGeometry(w - .21, H - .03, d - .21), vm), vm);
    m.geometry.translate(0, (H - .03) / 2, 0); m.position.set(X0(i) + w / 2, 0, Z0(j) + d / 2); m.receiveShadow = true; deckRoot.add(m);
    VOID_BLOCKS.push({ m, cx: m.position.x, cz: m.position.z, s: 1 });
  }

  // ---- furnish ----
  staticRoot = new THREE.Group(); deckRoot.add(staticRoot);
  BLOCKED = new Set(); SNUG = new Map(); ITEMS = []; WALL_DECOR = []; SPOTS = []; SPINS = []; PULSES = []; MOVERS = []; GARDEN_PLOTS = [];
  TALL = []; TALL_BY_ROOM = {}; NO_FADE = new Set();
  def.dress(def);
  buildCurves(def);
  if (ROOM_BOX['@']) {                                   // every deck's lift car: panel and handrail on the far wall, a light strip opposite
    placeWall('@', 'carPanel', 'n', 1.5, { hitW: .5, it: { t: 'Lift panel', x: '', lift: true } });
    placeWall('@', 'carPanel', 's', .5, { hitW: .5, it: { t: 'Lift panel', x: '', lift: true } });   // 0.38.26: a second panel opposite, in front of the west column (panelTiles)
    placeWall('@', 'handrail', 'n', .55);
    placeWall('@', 'workLight', 's', 1.0);
  }
  while (LAMPS.length < LAMP_SLOTS) addLamp(deckRoot, 0, -3, 0, .01, 0, 0);   // dark spares under the floor

  mergeMeshes(staticRoot);
  // tall pieces: give each its own copies of its materials (textures stay shared), then merge it on its own
  for (const t of TALL) {
    const clones = new Map();
    const cl = m => { if (!clones.has(m)) { const c = m.clone(); c.userData.base = { op: m.opacity, tr: m.transparent }; clones.set(m, c); } return clones.get(m); };
    t.g.traverse(o => { if (o.isMesh && !o.userData.noMerge) o.material = Array.isArray(o.material) ? o.material.map(cl) : cl(o.material); });
    mergeMeshes(t.g); t.mats = [...clones.values()]; t.src = new Map([...clones].map(([b, c]) => [c, b]));
  }
  tallCombine();
  for (const d of WALL_DECOR) mergeMeshes(d.g);
  for (const hr of HULL_RUNS) mergeMeshes(hr.decor);
  shadowStandIns();                                      // 0.27.25: shadows drawn from a few stand-ins, not every piece (0.27.33: built over the next frames)
  freezeStill();                                         // 0.27.26: furniture and wall pieces stop recomputing their place every frame
  for (const it of ITEMS) it.hit.userData.item = it;
}
// Working-deck floor markings: gold-and-charcoal bands across every doorway onto a steel floor,
// painted lanes down the haulway, and the shuttle pad. Drawn into the deck's floor texture.
const HAZARD_FLOORS = new Set(['steel', 'haul', 'bay', 'grate', 'lobby']);
function hazardBand(g, x, y, w, h, along) {
  g.save(); g.beginPath(); g.rect(x, y, w, h); g.clip();
  g.fillStyle = '#23272c'; g.fillRect(x, y, w, h); g.fillStyle = '#d9a441';
  const L = along ? w : h, S = along ? h : w;
  for (let k = -S; k < L + S; k += 16) {
    g.beginPath();
    if (along) { g.moveTo(x + k, y + h); g.lineTo(x + k + 8, y + h); g.lineTo(x + k + 8 + h, y); g.lineTo(x + k + h, y); }
    else { g.moveTo(x + w, y + k); g.lineTo(x + w, y + k + 8); g.lineTo(x, y + k + 8 + w); g.lineTo(x, y + k + w); }
    g.closePath(); g.fill();
  }
  g.restore();
}
function paintHazards(g, PX, def) {
  const B = 12;                                          // band depth either side of a door, in texture pixels
  for (const [key, type] of Object.entries(DOORS)) {
    if (type === 'glass' || type === 'pass') continue;
    const [k, a, b] = key.split(','), i = +a, j = +b, sides = k === 'h' ? [[i, j - 1, -1], [i, j, 1]] : [[i - 1, j, -1], [i, j, 1]];
    for (const [si, sj, sg] of sides) {
      const r = roomAt(si, sj); if (!r || ROOMS[r].void || !HAZARD_FLOORS.has(ROOMS[r].floor)) continue;
      if (k === 'h') hazardBand(g, i * PX + 3, sg < 0 ? j * PX - B : j * PX, PX - 6, B, true);
      else hazardBand(g, sg < 0 ? i * PX - B : i * PX, j * PX + 3, B, PX - 6, false);
    }
  }
  for (const [r, st] of Object.entries(ROOMS)) {
    const bx = ROOM_BOX[r]; if (!bx) continue;
    if (st.floor === 'haul') {                             // two gold lanes and a dashed centre line, aft to the pad
      const x0 = bx.i0 * PX, x1 = (bx.i1 + 1) * PX, y0 = bx.j0 * PX, y1 = (bx.j1 + 1) * PX, ym = (y0 + y1) / 2;
      g.fillStyle = 'rgba(217,164,65,.75)'; g.fillRect(x0, y0 + 14, x1 - x0, 4); g.fillRect(x0, y1 - 18, x1 - x0, 4);
      g.fillStyle = 'rgba(230,236,232,.45)'; for (let x = x0 + 6; x < x1; x += 28) g.fillRect(x, ym - 2, 16, 4);
    }
    if (st.pad) {                                          // the landing pad: a hazard-banded square, a ring and a centre cross
      const [pi, pj, pw, pd] = st.pad, x = pi * PX, y = pj * PX, w = pw * PX, h = pd * PX;
      g.fillStyle = '#2c3238'; g.fillRect(x, y, w, h);
      hazardBand(g, x, y, w, 18, true); hazardBand(g, x, y + h - 18, w, 18, true);
      hazardBand(g, x, y, 18, h, false); hazardBand(g, x + w - 18, y, 18, h, false);
      const cx = x + w / 2, cy = y + h / 2, rr = Math.min(w, h) / 2 - 46;
      g.strokeStyle = 'rgba(217,164,65,.8)'; g.lineWidth = 6; g.beginPath(); g.arc(cx, cy, rr, 0, Math.PI * 2); g.stroke();
      g.strokeStyle = 'rgba(230,236,232,.55)'; g.lineWidth = 5;
      g.beginPath(); g.moveTo(cx - 34, cy); g.lineTo(cx + 34, cy); g.moveTo(cx, cy - 34); g.lineTo(cx, cy + 34); g.stroke();
    }
  }
  // keep-clear outlines around machines: [i, j, tiles wide, tiles deep]
  for (const [i, j, w, d] of def.markings || []) {
    const x = i * PX + 6, y = j * PX + 6, ww = w * PX - 12, hh = d * PX - 12, b = 9;
    hazardBand(g, x, y, ww, b, true); hazardBand(g, x, y + hh - b, ww, b, true);
    hazardBand(g, x, y, b, hh, false); hazardBand(g, x + ww - b, y, b, hh, false);
  }
}
// Remove the current deck and free everything its build made: geometry, materials, and textures
// (canvases are shrunk too, so a big floor texture doesn't linger on a phone). Shared kit has ids
// below the deck's watermarks and is left alone. Sprites share one geometry in three.js, so theirs is skipped.
function unloadDeck() {
  if (!deckRoot) return;
  const geos = new Set(), mats = new Set(), texs = new Set();
  deckRoot.traverse(o => {
    if (o.geometry && !o.isSprite && o.geometry.id > deckMark.geo) geos.add(o.geometry);
    for (const m of [].concat(o.material || [])) if (m.id > deckMark.mat) mats.add(m);
    if (o.isInstancedMesh) o.dispose();
  });
  for (const m of mats) for (const v of Object.values(m)) if (v && v.isTexture && v.id > deckMark.tex) texs.add(v);
  geos.forEach(g => g.dispose()); mats.forEach(m => m.dispose());
  for (const t of texs) { t.dispose(); const c = t.userData && t.userData.c; if (c && c === t.image) c.width = c.height = 0; }
  scene.remove(deckRoot);
  deckRoot = staticRoot = floor = wallIM = hdrIM = postIM = hpostIM = sillIM = paneIM = null; glassEdges = [];
  LAMPS = []; STEAM = []; DUST = []; SPINS = []; PULSES = []; MOVERS = []; TALL = []; ITEMS = []; WALL_DECOR = []; DOOR_OBJS = []; HULL_RUNS = []; HULL_MESHES = []; VOID_BLOCKS = []; DOOR_LEAVES = []; SHADOW_PROXY = []; SHADOW_JOB = null;
  if (typeof deckUnloaded === 'function') deckUnloaded();   // 0.27.43: section 8b's per-deck caches let go of the old deck
  RUNS = []; POSTS = []; edgeList = []; wallEdges = []; frameEdges = []; fullPosts = []; hdrPosts = []; glows.length = 0;
  CURVES = []; CURVE_SEGS = [];
}

