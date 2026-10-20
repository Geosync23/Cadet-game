// =====================================================================
// 4e. THE REC DECK (DECKS[7], shown as R; the rec deck architect, 0.80.x; plans/recdeck-plan.html v3)
// Phase 1 (the user's rule): the deck and its animations for the player only. `playerOnly` keeps it out of the crew's
// schedules, the blackouts and the meeting places until crew are let in. Every floor here draws no R() (recFloor),
// and its kit makes its materials when the deck is built (recMats), so nothing at load changes and the deck is
// freed whole when you leave.
// =====================================================================
const recHash = (i, j, k) => { const x = Math.sin(i * 127.1 + j * 311.7 + k * 74.7) * 43758.5453; return x - Math.floor(x); };
function recFloor(g, kind, i, j, x, y, PX) {
  const hall = (a, b) => { const r2 = roomAt(a, b); return r2 && ROOMS[r2].hall; }, sameRoom = (a, b) => roomAt(a, b) === roomAt(i, j);
  const edge = (a, b) => ROOMS[roomAt(i, j)].hall ? !hall(a, b) : !sameRoom(a, b);   // a stripe where the floor meets a wall
  const fleck = (n, cs) => { for (let k = 0; k < n; k++) { g.fillStyle = cs[k % cs.length]; g.fillRect(x + recHash(i, j, k) * (PX - 2), y + recHash(i, j, k + 31) * (PX - 2), 2, 2); } };
  if (kind === 'concourse') {                            // the concourse and foyer (0.80.10, the user's: calmer, classier): two-tone terrazzo, an inlaid band at the walls; plain chips, cream and greys (0.82.4, the user's)
    g.fillStyle = (i + j) % 2 ? '#4d5759' : '#535e60'; g.fillRect(x, y, PX, PX);
    for (let k = 0; k < 22; k++) { const c = recHash(i, j, k + 50); g.fillStyle = c < .45 ? 'rgba(232,226,214,.35)' : c < .7 ? 'rgba(196,200,196,.3)' : c < .85 ? 'rgba(140,150,150,.32)' : 'rgba(20,24,28,.35)'; const r = 1 + recHash(i, j, k + 80) * 2.2; g.fillRect(x + recHash(i, j, k + 110) * (PX - 3), y + recHash(i, j, k + 140) * (PX - 3), r, r); }
    g.fillStyle = 'rgba(0,0,0,.12)'; if (i % 3 === 0) g.fillRect(x, y, 1, PX); if (j % 3 === 0) g.fillRect(x, y, PX, 1);   // thin joints every third tile
    if (edge(i, j - 1)) { g.fillStyle = '#c99a4a'; g.fillRect(x, y + 10, PX, 2); g.fillStyle = 'rgba(31,163,155,.8)'; g.fillRect(x, y + 14, PX, 3); }
    if (edge(i, j + 1)) { g.fillStyle = '#c99a4a'; g.fillRect(x, y + PX - 12, PX, 2); g.fillStyle = 'rgba(240,121,90,.75)'; g.fillRect(x, y + PX - 17, PX, 3); }
  } else if (kind === 'sport') {                         // charcoal sports floor; the neon stripes, cyan to port and magenta to starboard
    g.fillStyle = '#2a2e35'; g.fillRect(x, y, PX, PX);
    fleck(8, ['rgba(80,230,255,.16)', 'rgba(255,90,200,.14)', 'rgba(220,225,230,.12)']);
    if (i % 4 === 0) { g.fillStyle = 'rgba(0,0,0,.2)'; g.fillRect(x, y, 2, PX); }
    if (edge(i, j - 1)) { g.fillStyle = 'rgba(80,230,255,.9)'; g.fillRect(x, y + 9, PX, 4); g.fillStyle = 'rgba(80,230,255,.25)'; g.fillRect(x, y + 6, PX, 10); }
    if (edge(i, j + 1)) { g.fillStyle = 'rgba(255,79,216,.9)'; g.fillRect(x, y + PX - 13, PX, 4); g.fillStyle = 'rgba(255,79,216,.25)'; g.fillRect(x, y + PX - 16, PX, 10); }
  } else if (kind === 'tile' || kind === 'pooltile') {   // small glazed tiles: pale aqua on the pool deck, pale grey-green in the changing rooms and washroom
    const pool = kind === 'pooltile';
    g.fillStyle = pool ? '#6f9aa0' : '#7f8c8a'; g.fillRect(x, y, PX, PX);
    for (let a = 0; a < 4; a++) for (let b = 0; b < 4; b++) {
      const t = (recHash(i * 4 + a, j * 4 + b, 3) - .5) * 12;
      g.fillStyle = pool ? `rgb(${170 + t},${214 + t},${216 + t})` : `rgb(${196 + t},${206 + t},${200 + t})`; g.fillRect(x + a * 16 + 1, y + b * 16 + 1, 14, 14);
    }
  } else if (kind === 'court') {                         // the Lightdisc court's black floor (its lines come with the court, 0.80.2)
    g.fillStyle = '#0c0f14'; g.fillRect(x, y, PX, PX);
    g.fillStyle = 'rgba(120,160,200,.06)'; g.fillRect(x, y, PX, 1); g.fillRect(x, y, 1, PX);
    if (i <= 5 || i >= 15) { g.fillStyle = i <= 5 ? 'rgba(255,154,60,.07)' : 'rgba(80,230,255,.07)'; g.fillRect(x, y, PX, PX); }   // each player's zone, by their baseline
  } else if (kind === 'stand') {
    g.fillStyle = '#2e333b'; g.fillRect(x, y, PX, PX); fleck(5, ['rgba(255,255,255,.08)']);
  } else if (kind === 'violet') {                        // the auditorium's deep violet carpet with small gold diamonds
    g.fillStyle = '#33264f'; g.fillRect(x, y, PX, PX);
    g.fillStyle = 'rgba(233,196,106,.16)'; g.beginPath(); g.moveTo(x + 32, y + 24); g.lineTo(x + 40, y + 32); g.lineTo(x + 32, y + 40); g.lineTo(x + 24, y + 32); g.closePath(); g.fill();
  } else if (kind === 'pad') {                           // the float room's soft coral padding, in squares
    g.fillStyle = '#b8665c'; g.fillRect(x, y, PX, PX);
    for (let a = 0; a < 2; a++) for (let b = 0; b < 2; b++) { g.fillStyle = (a + b + i + j) % 2 ? '#e3907f' : '#eaa093'; g.fillRect(x + a * 32 + 2, y + b * 32 + 2, 28, 28); }
  } else if (kind === 'river') {                         // the river hall's slate floor, under the banks (0.80.4)
    g.fillStyle = '#4a5654'; g.fillRect(x, y, PX, PX); fleck(10, ['rgba(160,190,170,.18)', 'rgba(20,30,28,.25)']);
  } else {                                               // 'svc': service rooms, plain steel plate
    g.fillStyle = '#353b42'; g.fillRect(x, y, PX, PX);
    g.fillStyle = '#5d666e'; g.fillRect(x + 2, y + 2, PX - 4, PX - 4);
    g.fillStyle = 'rgba(0,0,0,.08)'; for (let a = 10; a < PX - 8; a += 14) for (let b = 10; b < PX - 8; b += 14) g.fillRect(x + a, y + b, 6, 2);
  }
  if (kind !== 'sport' && kind !== 'concourse' && !sameRoom(i, j - 1) && !hall(i, j - 1) && (kind === 'pooltile' || kind === 'pad')) { g.fillStyle = 'rgba(80,230,255,.5)'; g.fillRect(x, y + 4, PX, 3); }   // the cyan stripe runs on into the port rooms
}
// the auditorium's 76 seats (0.80.1): six raked rows (columns 35-40, back to front, each step 0.2 lower), three blocks
// with two aisles at rows 5 and 12. Pure numbers, so the seats' places can be data like every deck's
const REC_SEATS = (() => {
  const out = [], blocks = [[2, 5, 3], [6, 12, 7], [13, 16, 3]];
  for (let r = 0; r < 6; r++) blocks.forEach(([z0, z1, n], b) => {
    if (r === 5 && b !== 1) n = 2;                       // the front row's side blocks are one seat short: 76 in all
    for (let k = 0; k < n; k++) out.push({ col: 35 + r, h: Math.round((1 - r * .2) * 100) / 100, x: 35 + r + .55, z: z0 + (z1 - z0) * (k + .5) / n, aisle: b === 0 || (b === 1 && k < 4) ? 5 : 12 });
  });
  return out;
})();
const REC_BLOCKS = [[2, 5], [6, 12], [13, 16]];          // the seat blocks' rows (z from, to)
const REC_STAGE = { front: 7.65, back: 11.2, rz: 8.6 };   // room-local: the stage's front edge at the centre line, the bow arc's radii
Object.assign(KIT, {
  // the rake: one solid step per row and block (no holes, nothing on the floor's plane), and the seats on them, facing the stage
  recRake(g) {
    for (let r = 0; r < 5; r++) for (const [z0, z1] of REC_BLOCKS) { const h = 1 - r * .2; box(1, h, z1 - z0 - .02, RK.rake, r + 1.5, h / 2, (z0 + z1) / 2, g); box(.04, .03, z1 - z0 - .02, RK.gold, r + 1.98, h + .005, (z0 + z1) / 2, g); }
    for (const s of REC_SEATS) {
      const x = s.x - 34, y = s.h;
      box(.44, .1, .5, RK.seat, x + .05, y + .42, s.z, g);              // the cushion
      box(.08, .56, .5, RK.seat, x - .2, y + .74, s.z, g);              // the back
      box(.12, .37, .3, RK.seatDark, x + .02, y + .185, s.z, g);         // the pedestal
      box(.012, .06, .12, RK.gold, x - .246, y + .88, s.z, g);           // the gold number, on the back of the seat
    }
    return { w: .1, d: .1, noBlock: true };
  },
  // the stage: a curved platform across the bow, its back following the hull and its front bowing out toward the seats
  recStage(g) {
    const S = REC_STAGE, th = Math.acos(8 / S.back), sh = new THREE.Shape(), zA = 9 - S.rz * Math.sin(th), zB = 9 + S.rz * Math.sin(th);
    sh.moveTo(8, zA); sh.quadraticCurveTo(2 * S.front - 8, 9, 8, zB);
    for (let k = 0; k <= 24; k++) { const a = th - 2 * th * k / 24; sh.lineTo(S.back * Math.cos(a), 9 + S.rz * Math.sin(a)); }
    const geo = new THREE.ExtrudeGeometry(sh, { depth: .55, bevelEnabled: false, curveSegments: 16 });
    const m = new THREE.Mesh(geo, [RK.stageTop, RK.stageSide]); m.rotation.x = Math.PI / 2; m.position.y = .55; m.castShadow = m.receiveShadow = true; g.add(m);
    // 0.84.8: the stage light pools (the lectern, centre stage, the piano), one mesh; recShow sets each pool's brightness
    const P = REC_POOLS, pos = [], uv = [], ix = [];
    P.forEach(([x, z, r], k) => { for (const [u, v] of [[0, 0], [1, 0], [1, 1], [0, 1]]) { pos.push(x + (u - .5) * 2 * r, .58, z + (v - .5) * 2 * r); uv.push(u, v); } ix.push(k * 4, k * 4 + 2, k * 4 + 1, k * 4, k * 4 + 3, k * 4 + 2); });
    const pg = new THREE.BufferGeometry(); pg.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); pg.setAttribute('uv', new THREE.Float32BufferAttribute(uv, 2));
    pg.setAttribute('color', new THREE.Float32BufferAttribute(new Array(P.length * 12).fill(0), 3)); pg.setIndex(ix);
    const pm = new THREE.Mesh(pg, new THREE.MeshBasicMaterial({ map: glowTex, vertexColors: true, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false, toneMapped: false }));
    pm.raycast = () => {}; pm.renderOrder = 2; pm.userData.noMerge = true; g.add(pm); REC_SHOW.pools = pm; recPoolsSet();
    return { w: .1, d: .1, noBlock: true };
  },
  // the lighting truss over the stage on two gold towers, with six lamps aimed at the stage
  recTruss(g, o) {
    const L = o.len, y = H - .75;
    for (const z of [-L / 2, L / 2]) { box(.16, y + .1, .16, RK.truss, 0, .55 + (y - .55) / 2, z, g); box(.4, .05, .4, RK.truss, 0, .575, z, g); }
    for (const [x, yy] of [[-.2, y], [.2, y], [-.2, y + .35], [.2, y + .35]]) box(.05, .05, L, RK.truss, x, yy, 0, g);
    for (let k = 0; k <= 12; k++) { const z = -L / 2 + L * k / 12; box(.4, .03, .03, RK.truss, 0, y, z, g); box(.03, .35, .03, RK.truss, k % 2 ? -.2 : .2, y + .175, z, g); }
    for (let k = 0; k < 6; k++) { const z = -L / 2 + L * (k + .5) / 6, c = cyl(.09, .12, .26, RK.black, -.05, y - .2, z, g, 12); c.rotation.z = -.7; }
    return { w: .5, d: L, tall: true };
  },
  recLectern(g) {
    box(.56, 1.0, .4, RK.wood, 0, .55 + .5, 0, g); box(.62, .05, .48, RK.wood, 0, 1.58, .03, g).rotation.x = -.18;
    box(.3, .03, .22, RK.gold, 0, 1.18, .205, g);                       // the ship's crest on its front
    return { w: .62, d: .48 };
  },
  // the film screen's housing, rolled up under the truss; 0.84.8: its cloth unrolls for films (recShow, section 8c)
  recScreen(g, o) {
    box(.24, .24, o.len, RK.black, 0, H - .3, 0, g); box(.04, .05, o.len - .2, RK.screen, .09, H - .45, 0, g);
    const piv = new THREE.Group(), sh = H - 1.45; piv.position.set(.06, H - .45, 0); piv.userData.noMerge = true; g.add(piv);   // it moves: kept out of the deck's merge
    RK.film = new THREE.MeshBasicMaterial({ color: col('#e8e6df'), toneMapped: false });
    box(.02, sh, o.len - .3, RK.film, 0, -sh / 2, 0, piv); box(.05, .05, o.len - .25, RK.black, 0, -sh, 0, piv);   // the cloth and its weighted bottom bar
    for (const c of piv.children) { c.userData.noMerge = true; c.castShadow = false; }   // the merge looks at each mesh, not its group
    REC_SHOW.piv = piv; piv.scale.y = Math.max(.001, REC_SHOW.scr); piv.visible = REC_SHOW.scr > .002;
    return { w: .3, d: o.len, noBlock: true };
  },
  // 0.84.12 (RA's places 7-ring-1..8 and 7-stool-1): a ring of eight chairs for a small Wren talk and the chief's stool,
  // out on the stage only while the show is 'talk' (recShowSet); merged into a mesh or two, kept out of the deck's merge
  recRing(g, o) {
    const rg = new THREE.Group(); g.add(rg);
    for (let k = 0; k < 8; k++) {
      const a = 2 * Math.PI * k / 8, c = new THREE.Group(), x = o.r * Math.cos(a), z = o.r * Math.sin(a); c.position.set(x, 0, z); c.rotation.y = Math.atan2(-x, -z); rg.add(c); KIT.chair(c);
    }
    const st = new THREE.Group(); st.position.set(o.stool[0], 0, o.stool[1]); rg.add(st); KIT.stool(st);
    mergeMeshes(rg); for (const m of rg.children) { m.userData.noMerge = true; m.raycast = () => {}; }
    REC_SHOW.ring = rg; rg.visible = REC_SHOW.state === 'talk';
    return { w: .1, d: .1, noBlock: true };
  },
  recHit(g, o) { return { w: o.w, d: o.d, noBlock: true }; },   // a tap target over something drawn elsewhere
});
Object.assign(WALL_KIT, {
  // the REC DEC neon over the auditorium's doors: pink letters on a dark backing, drawn once per visit
  recNeon(g) {
    const t = tex(512, 160, (c, w, h) => {
      c.fillStyle = '#1a1220'; c.fillRect(0, 0, w, h);
      c.font = '800 96px system-ui,sans-serif'; c.textAlign = 'center'; c.lineJoin = 'round';
      c.strokeStyle = 'rgba(255,79,216,.35)'; c.lineWidth = 18; c.strokeText('REC DEC', w / 2, 116);
      c.strokeStyle = '#ff6fe0'; c.lineWidth = 6; c.strokeText('REC DEC', w / 2, 116); c.fillStyle = '#ffd6f6'; c.fillText('REC DEC', w / 2, 116);
    });
    const p = new THREE.Mesh(new THREE.PlaneGeometry(2.4, .75), new THREE.MeshBasicMaterial({ map: t, toneMapped: false })); p.position.set(0, H - .5, .06); g.add(p);
    box(2.5, .85, .05, RK.black, 0, H - .5, .025, g);
  },
  recPoster(g) {
    const t = tex(256, 360, (c, w, h) => {
      c.fillStyle = '#26183f'; c.fillRect(0, 0, w, h); c.fillStyle = '#ff6fe0'; c.fillRect(0, 0, w, 10); c.fillStyle = '#50e6ff'; c.fillRect(0, h - 10, w, 10);
      c.textAlign = 'center'; c.fillStyle = '#ffe9a8'; c.font = '800 40px system-ui,sans-serif'; c.fillText('THE', w / 2, 90); c.fillText('REC DEC', w / 2, 136);
      c.fillStyle = '#e8eef0'; c.font = '600 22px system-ui,sans-serif'; ['Pool', 'Rivers', 'Climbing wall', 'Float room', 'Lightdisc'].forEach((l, k) => c.fillText(l, w / 2, 190 + k * 28));
      c.fillStyle = '#50e6ff'; c.font = '700 22px system-ui,sans-serif'; c.fillText('Open 06:00 to midnight', w / 2, 336);
    });
    const p = new THREE.Mesh(new THREE.PlaneGeometry(.8, 1.12), new THREE.MeshStandardMaterial({ map: t, roughness: .8 })); p.position.set(0, 1.55, .045); g.add(p);
    box(.86, 1.18, .04, RK.gold, 0, 1.55, .02, g);
  },
});
// the stands (0.80.2): three stepped benches along the court's inboard side (rows 11-12), in three blocks with aisles at
// columns 6 and 14 (in from the concourse's doors). One seat a tile on each tier: 33 in all
const REC_STANDS = [[4, 6], [7, 14], [15, 17]], REC_TIER = [{ z: 11.33, h: .7 }, { z: 11.99, h: .35 }, { z: 12.65, h: 0 }];
const REC_STAND_SEATS = REC_STANDS.flatMap(([c0, c1]) => REC_TIER.flatMap((t, k) => Array.from({ length: c1 - c0 }, (_, q) => ({ col: c0 + q, tier: k, h: t.h, z: t.z, aisle: c0 + q < 10 ? 6 : 14 }))));
Object.assign(KIT, {
  recStands(g) {
    for (const [c0, c1] of REC_STANDS) {
      const w = c1 - c0, x = (c0 + c1) / 2 - 4;
      REC_TIER.forEach((t, k) => {
        if (t.h) box(w - .04, t.h, .66, RK.standStep, x, t.h / 2, t.z - 11, g);
        box(w - .1, .06, .36, RK.bench, x, t.h + .42, t.z - 11 + .06, g);                       // the plank
        for (let q = 0; q < w; q++) box(.08, .39, .26, RK.black, c0 + q + .5 - 4, t.h + .195, t.z - 11 + .06, g);   // its legs, one a seat
      });
    }
    return { w: .1, d: .1, noBlock: true };
  },
  // the court: glowing lines (cyan at the bow end, orange at the stern), the force-field net across the middle and the
  // side walls, faint until the disc hits them. Room-local: the court is 13 x 5
  recCourt(g) {
    const ln = (m, w, d, x, z) => box(w, .014, d, m, x, .007, z, g);
    ln(RK.lineOrange, .07, 4.4, .6, 2.5); ln(RK.lineCyan, .07, 4.4, 12.4, 2.5);                  // the baselines
    for (const z of [.3, 4.7]) { ln(RK.lineOrange, 5.9, .06, 3.55, z); ln(RK.lineCyan, 5.9, .06, 9.45, z); }   // the sidelines, each end its colour
    ln(RK.lineWhite, .05, 4.4, 6.5, 2.5);
    for (const x of [2.6, 10.4]) ln(x < 6 ? RK.lineOrange : RK.lineCyan, .04, 4.4, x, 2.5);     // the edge of each player's zone
    // the net: a shimmering field from a post at each side, glowing along its top
    for (const z of [.18, 4.82]) cyl(.05, .06, 1.3, RK.black, 6.5, .65, z, g, 10);
    const net = new THREE.Mesh(new THREE.PlaneGeometry(4.6, 1.05), RK.net); net.position.set(6.5, .6, 2.5); net.rotation.y = Math.PI / 2; net.userData.noMerge = net.userData.noShadow = true; g.add(net);
    box(.03, .03, 4.6, RK.lineWhite, 6.5, 1.14, 2.5, g);
    // the side walls: a faint field along each side, the length of the court
    for (const z of [.12, 4.88]) { const f = new THREE.Mesh(new THREE.PlaneGeometry(12.8, 1.1), RK.field); f.position.set(6.5, .58, z); f.userData.noMerge = f.userData.noShadow = true; g.add(f); }
    return { w: .1, d: .1, noBlock: true };
  },
});
const REC_BOARD = { tex: null };                         // the scoreboard's canvas texture, for section 23b's live score (0.82.0)
Object.assign(WALL_KIT, {
  // the Lightdisc panel by the court's gate (0.80.7): where you'll ask someone to play. A post and a small lit screen
  recPlayPanel(g) {
    const t = tex(256, 160, (c, w, h) => {
      c.fillStyle = '#05070b'; c.fillRect(0, 0, w, h); c.strokeStyle = '#50e6ff'; c.lineWidth = 4; c.strokeRect(4, 4, w - 8, h - 8);
      c.textAlign = 'center'; c.fillStyle = '#e8eef0'; c.font = '700 24px system-ui,sans-serif'; c.fillText('LIGHTDISC', w / 2, 48);
      c.fillStyle = '#50e6ff'; c.font = '700 22px system-ui,sans-serif'; c.fillText('ASK SOMEONE', w / 2, 92); c.fillText('TO PLAY', w / 2, 120);
    });
    box(.08, 1.25, .08, RK.black, 0, .625, .14, g); box(.5, .34, .06, RK.black, 0, 1.4, .14, g);
    const p = new THREE.Mesh(new THREE.PlaneGeometry(.44, .28), new THREE.MeshBasicMaterial({ map: t, toneMapped: false })); p.position.set(0, 1.4, .175); g.add(p);
  },
  // the scoreboard on the court's stern wall, high up (it's two storeys of wall); section 23b redraws its canvas (REC_BOARD) during a game
  recScoreboard(g) {
    const t = tex(512, 224, (c, w, h) => {
      c.fillStyle = '#05070b'; c.fillRect(0, 0, w, h); c.strokeStyle = '#2a3340'; c.lineWidth = 6; c.strokeRect(3, 3, w - 6, h - 6);
      c.textAlign = 'center'; c.fillStyle = '#e8eef0'; c.font = '700 30px system-ui,sans-serif'; c.fillText('LIGHTDISC', w / 2, 44);
      c.font = '800 112px system-ui,sans-serif'; c.fillStyle = '#ff9a3c'; c.fillText('0', w * .27, 168); c.fillStyle = '#50e6ff'; c.fillText('0', w * .73, 168);
      c.fillStyle = '#e8eef0'; c.font = '800 80px system-ui,sans-serif'; c.fillText(':', w / 2, 158);
      c.font = '600 20px system-ui,sans-serif'; c.fillStyle = '#ff9a3c'; c.fillText('STERN', w * .27, 204); c.fillStyle = '#50e6ff'; c.fillText('BOW', w * .73, 204);
    });
    const p = new THREE.Mesh(new THREE.PlaneGeometry(2.8, 1.22), new THREE.MeshBasicMaterial({ map: t, toneMapped: false })); p.position.set(0, H - .72, .09); g.add(p); REC_BOARD.tex = t;
    box(2.95, 1.34, .08, RK.black, 0, H - .72, .04, g);   // over the emitter room's hatch
  },
});
// water (0.80.3, plan section 10): one small shader for the pool and the rivers. Slow moving caustics over two colours,
// and on the rivers white foam streaming along the flow. No texture and no R(); colours through col() as uniforms; its
// clock only ticks while it's drawn (onBeforeRender), so water off-screen costs nothing
function recWater(deep, shallow, o = {}) {
  const U = { uT: { value: 0 }, uDeep: { value: col(deep) }, uShallow: { value: col(shallow) }, uFoam: { value: o.foam || 0 }, uFlow: { value: o.flow || 0 }, uA: { value: o.alpha || .84 } };
  const m = new THREE.ShaderMaterial({ uniforms: U, transparent: true, depthWrite: false,
    vertexShader: 'varying vec3 vW; varying vec2 vUv; void main() { vec4 w = modelMatrix * vec4(position, 1.0); vW = w.xyz; vUv = uv; gl_Position = projectionMatrix * viewMatrix * w; }',
    fragmentShader: `uniform float uT, uFoam, uFlow, uA; uniform vec3 uDeep, uShallow; varying vec3 vW; varying vec2 vUv;
      void main() {
        vec2 p = vW.xz * 1.6; p.x -= uT * uFlow;
        float a = sin(p.x * 1.3 + uT * .8 + sin(p.y * 1.1 + uT * .5)) + sin(p.y * 1.7 - uT * .6 + sin(p.x * .9 - uT * .4));
        float b = sin(p.x * 2.3 - p.y * 1.4 + uT * 1.1) * .5;
        float caus = smoothstep(.35, 0.0, abs(a + b));                       // thin bright lines where the waves cross
        vec3 c = mix(uDeep, uShallow, .5 + .25 * a) + caus * .28;
        if (uFoam > 0.0) {                                                   // the white water: streaks running with the flow
          float f = sin(p.x * 3.1 + sin(p.y * 4.3) * 1.5) * sin(p.y * 6.7 + p.x * .7) + sin(p.x * 5.3 - p.y * 2.1);
          c = mix(c, vec3(.95, .98, 1.0), clamp(uFoam * smoothstep(.6, 1.6, f), 0.0, .85));
        }
        gl_FragColor = vec4(c, uA);
        #include <tonemapping_fragment>
        #include <encodings_fragment>
      }` });
  m.userData.U = U; return m;
}
const recWaterMesh = (geo, m) => { const w = new THREE.Mesh(geo, m); w.userData.noMerge = w.userData.noShadow = true; w.receiveShadow = false; w.castShadow = false; w.raycast = () => {};
  w.onBeforeRender = () => { m.userData.U.uT.value = performance.now() / 1000; }; return w; };
// the Wren in mosaic for the pool floor: a canvas drawn once per visit from fixed shapes (no R())
function recMosaic() {
  return tex(512, 320, (c, w, h) => {
    c.fillStyle = '#8fd3d6'; c.fillRect(0, 0, w, h);
    for (let y = 0; y < h; y += 16) for (let x = 0; x < w; x += 16) { const t = Math.round((recHash(x, y, 5) - .5) * 14); c.fillStyle = `rgb(${150 + t},${214 + t},${216 + t})`; c.fillRect(x + 1, y + 1, 14, 14); }
    const tileFill = (pts, colr) => { c.save(); c.beginPath(); pts.forEach(([x, y], k) => k ? c.lineTo(x, y) : c.moveTo(x, y)); c.closePath(); c.clip();
      for (let y = 0; y < h; y += 16) for (let x = 0; x < w; x += 16) { c.fillStyle = colr; c.fillRect(x + 1, y + 1, 14, 14); } c.restore(); };
    tileFill([[90, 120], [330, 104], [420, 140], [440, 160], [420, 180], [330, 216], [90, 200], [70, 160]], '#24507a');   // the hull, bow to the right
    tileFill([[110, 104], [180, 70], [210, 104]], '#24507a'); tileFill([[110, 216], [180, 250], [210, 216]], '#24507a');   // the nacelles' fins
    tileFill([[330, 136], [400, 148], [400, 172], [330, 184]], '#e9c46a');                                                  // the bridge's glow
    tileFill([[60, 140], [76, 140], [76, 180], [60, 180]], '#ff9a3c');                                                      // the drive
  });
}
Object.assign(KIT, {
  // the pool (0.80.3, R4; four lanes from 0.80.7, plan v4): raised, so nothing is cut out of the deck. A tiled rim 0.42
  // high round a basin floor with the Wren mosaic, water just under the rim, four lanes between orange-and-white ropes,
  // and steps down in the stern-inboard corner. Room-local, the basin runs x 0.8-8.2 and z 0.9-4.5 (deck x 23.8-31.2)
  recPool(g) {
    const x0 = .8, x1 = 8.2, z0 = .9, z1 = 4.5, H = .42, t = .22, cx = (x0 + x1) / 2, cz = (z0 + z1) / 2, L = x1 - x0, Wd = z1 - z0;
    for (const z of [z0 + t / 2, z1 - t / 2]) box(L, H, t, RK.rim, cx, H / 2, z, g);
    for (const x of [x0 + t / 2, x1 - t / 2]) box(t, H, Wd - 2 * t, RK.rim, x, H / 2, cz, g);
    for (const z of [z0 - .02, z1 + .02]) box(L + .08, .05, .1, RK.coping, cx, H + .025, z + (z < cz ? .05 : -.05), g);   // the coping round the top
    for (const x of [x0 - .02, x1 + .02]) box(.1, .05, Wd, RK.coping, x + (x < cx ? .05 : -.05), H + .025, cz, g);
    const floor = new THREE.Mesh(new THREE.BoxGeometry(L - 2 * t, .03, Wd - 2 * t), [RK.poolSide, RK.poolSide, RK.mosaic, RK.poolSide, RK.poolSide, RK.poolSide]);
    floor.position.set(cx, .015, cz); floor.userData.noMerge = true; g.add(floor);
    for (let k = 0; k < 3; k++) box(1.0, .3 - k * .1, .3, RK.poolSide, x0 + t + .5, (.3 - k * .1) / 2 + .03, z1 - t - .15 - k * .3, g);   // the steps, down from the inboard rim at the stern end
    const water = recWaterMesh(new THREE.PlaneGeometry(L - 2 * t, Wd - 2 * t), RK.poolOwn); water.rotation.x = -Math.PI / 2; water.position.set(cx, .35, cz); g.add(water);   // 0.84.4 (rec engineer B): its own copy of the water, so recSigns can cloud the pool and not the river
    for (const z of [1.8, 2.7, 3.6]) for (let k = 0; k < 16; k++) {   // the lane ropes: floats in runs of orange and white
      const s = (L - 2 * t) / 16, f = cyl(.045, .045, s * .9, k % 4 < 2 ? RK.ropeOrange : RK.ropeWhite, x0 + t + s * (k + .5), .35, z, g, 8); f.rotation.z = Math.PI / 2;
    }
    return { w: .1, d: .1, noBlock: true };
  },
  recLounger(g) {
    box(.62, .12, 1.7, RK.loungerFrame, 0, .3, 0, g); for (const [x, z] of [[-.26, -.75], [.26, -.75], [-.26, .75], [.26, .75]]) box(.05, .3, .05, RK.loungerFrame, x, .15, z, g);
    box(.56, .07, 1.1, RK.loungerPad, 0, .4, .25, g); box(.56, .07, .62, RK.loungerPad, 0, .58, -.55, g).rotation.x = -.6;
    return { w: .62, d: 1.7 };
  },
});
Object.assign(WALL_KIT, {
  recFirstAid(g) {
    box(.5, .6, .14, RK.aidWhite, 0, 1.35, .07, g); box(.3, .08, .01, RK.aidRed, 0, 1.4, .145, g); box(.08, .3, .01, RK.aidRed, 0, 1.4, .145, g);
    cyl(.05, .05, .04, RK.aidRed, .3, 1.15, .06, g, 12).rotation.x = Math.PI / 2;                       // the alarm button beside it
  },
});
// the river hall (0.80.4, R5). Room-local (the hall's box starts at column 1): the rivers are one raised loop round a
// rock island, x 3.0-13.6 and z 0.5-5.6. The fast white-water run is along the windows (north), the slow return channel
// on the inboard side (south), joined at both ends; a wave gate across the fast run at the bow end. The walkway runs
// along the concourse glass (row 6) and up the bow end (column 15) to the changing rooms' door; the climbing wall fills
// the stern end, its foot clear (local x 0-2.8)
const RIV = { x0: 3.0, x1: 13.6, z0: .5, z1: 5.6, in0: 4.6, in1: 12.0, iz0: 2.1, iz1: 4.0 };
const REC_ROUTES = 4, REC_WALL = { x: .35, z0: 2.0, z1: 6.6 };
function recQuads(rects, y) {                            // one flat geometry from rectangles [x0, z0, x1, z1] (a water surface in one draw)
  const P = [], N = [], U = [], I = [];
  rects.forEach(([a, b, c, d], k) => { P.push(a, y, b, c, y, b, c, y, d, a, y, d); for (let q = 0; q < 4; q++) N.push(0, 1, 0); U.push(0, 0, 1, 0, 1, 1, 0, 1); const o = k * 4; I.push(o, o + 2, o + 1, o, o + 3, o + 2); });
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(P, 3)); g.setAttribute('normal', new THREE.Float32BufferAttribute(N, 3)); g.setAttribute('uv', new THREE.Float32BufferAttribute(U, 2)); g.setIndex(I); return g;
}
Object.assign(KIT, {
  recRiver(g) {
    const R_ = RIV, rh = .46, t = .2;
    // the outer bank, grey-green fake rock, and the river bed under the water
    box(R_.x1 - R_.x0, rh, t, RK.rock, (R_.x0 + R_.x1) / 2, rh / 2, R_.z0 - t / 2, g); box(R_.x1 - R_.x0 + 2 * t, rh, t, RK.rock, (R_.x0 + R_.x1) / 2, rh / 2, R_.z1 + t / 2, g);
    box(t, rh, R_.z1 - R_.z0 + t, RK.rock, R_.x0 - t / 2, rh / 2, (R_.z0 + R_.z1) / 2 - t / 2, g); box(t, rh, R_.z1 - R_.z0 + t, RK.rock, R_.x1 + t / 2, rh / 2, (R_.z0 + R_.z1) / 2 - t / 2, g);
    box(R_.x1 - R_.x0, .03, R_.z1 - R_.z0, RK.riverBed, (R_.x0 + R_.x1) / 2, .015, (R_.z0 + R_.z1) / 2, g);
    // the island: a long rock bank with boulders and ferns
    box(R_.in1 - R_.in0, .62, R_.iz1 - R_.iz0, RK.rock, (R_.in0 + R_.in1) / 2, .31, (R_.iz0 + R_.iz1) / 2, g);
    for (let k = 0; k < 9; k++) { const x = R_.in0 + .5 + k * .85, z = R_.iz0 + .35 + recHash(k, 1, 7) * 1.2, s = .28 + recHash(k, 2, 7) * .22; soft(k % 3 ? RK.rock : RK.rockDark, x, .62, z, s * 1.4, s, s, g); }
    for (let k = 0; k < 7; k++) { const x = R_.in0 + .9 + k * 1.05, z = R_.iz0 + .5 + recHash(k, 3, 7) * .9;
      for (let q = 0; q < 5; q++) { const a = q * 1.257 + k, f = box(.07, .02, .5, RK.fern, x + Math.sin(a) * .18, .72, z + Math.cos(a) * .18, g); f.rotation.set(-.5 * Math.cos(a), a, .5 * Math.sin(a), 'YXZ'); } }
    // the water: the fast run and the bow end foam white, the return channel and the stern end run slow
    const fast = recWaterMesh(recQuads([[R_.x0, R_.z0, R_.x1, R_.iz0], [R_.in1, R_.iz0, R_.x1, R_.iz1]], .36), RK.riverFast);
    const slow = recWaterMesh(recQuads([[R_.x0, R_.iz1, R_.x1, R_.z1], [R_.x0, R_.iz0, R_.in0, R_.iz1]], .36), RK.poolWater);   // the pool's own water (0.82.5)
    g.add(fast, slow);
    // the wave gate across the fast run near the bow end: two steel posts, a beam with the gate's lights, a ramp under the water
    for (const z of [R_.z0 - .05, R_.iz0 + .05]) box(.16, 1.7, .16, RK.steel, 11.3, .85, z, g);
    box(.22, .2, R_.iz0 - R_.z0 + .3, RK.steel, 11.3, 1.7, (R_.z0 + R_.iz0) / 2, g); box(.04, .05, R_.iz0 - R_.z0, RK.gateLight, 11.19, 1.66, (R_.z0 + R_.iz0) / 2, g);
    box(.9, .1, R_.iz0 - R_.z0 - .04, RK.steel, 11.5, .26, (R_.z0 + R_.iz0) / 2, g).rotation.z = .12;
    // the kayak dock on the inboard bank by the doors, and three kayaks out on the water
    box(2.4, .08, .9, RK.dock, 10.4, .5, R_.z1 - .3, g); for (let k = 0; k < 8; k++) box(.02, .012, .86, RK.dockDark, 9.3 + k * .3, .545, R_.z1 - .3, g);
    recKayak(g, 10.4, .66, R_.z1 - .3, Math.PI / 2 + .03, RK.kayak[3]);   // the green kayak up on the dock (0.80.8, the user's: no kayaks left in the water; one is on it only while someone paddles)
    return { w: .1, d: .1, noBlock: true };
  },
  // the kayak rack on the bow end wall: four kayaks on two arms, red, yellow, blue and green, paddles alongside
  recKayakRack(g) {
    for (const z of [-1.0, 1.0]) { box(.08, 1.6, .08, RK.steel, .15, .8, z, g); for (const y of [.45, .85, 1.25]) box(.5, .05, .06, RK.steel, -.05, y, z, g); }   // east (wall) side is +x
    for (let k = 0; k < 3; k++) recKayak(g, -.1, .52 + k * .4, 0, 0, RK.kayak[k]);
    for (let k = 0; k < 3; k++) { box(.04, .04, 2.0, RK.paddle, .05, 1.5 + k * .06, 0, g); for (const e of [-1, 1]) box(.03, .16, .09, RK.kayak[(k + 1) % 4], .05, 1.5 + k * .06, e * 1.0, g); }
    return { w: .5, d: 2.6, tall: true };
  },
  // the climbing wall: ochre and rust panels from the floor to the roof, four routes of coloured holds (one instanced
  // mesh, coloured per hold), an auto-belay at the top of each with its rope down, and the brass bell at the very top
  recClimbWall(g) {
    const W_ = REC_WALL, len = W_.z1 - W_.z0, top = H - .12, zc = (W_.z0 + W_.z1) / 2;
    box(.3, top, len, RK.wallOchre, W_.x, top / 2, zc, g);
    for (let k = 0; k < 6; k++) { const p = box(.06, .7 + recHash(k, 4, 9) * .9, .9, RK.wallRust, W_.x + .17, .6 + k * (top - 1.3) / 5, W_.z0 + .5 + recHash(k, 5, 9) * (len - 1), g); p.rotation.x = (recHash(k, 6, 9) - .5) * .3; }
    const holds = [], cols = [RK.holdC[0], RK.holdC[1], RK.holdC[2], RK.holdC[3]];
    for (let r = 0; r < REC_ROUTES; r++) for (let k = 0; k < 11; k++) holds.push([W_.x + .19, .35 + k * (top - .7) / 10, W_.z0 + len * (r + .5) / REC_ROUTES + (recHash(r, k, 11) - .5) * .7, r]);
    const im = new THREE.InstancedMesh(new THREE.IcosahedronGeometry(.07, 0), RK.hold, holds.length), m4 = new THREE.Matrix4();
    holds.forEach(([x, y, z, r], k) => { m4.makeScale(1, .8 + recHash(k, 1, 13) * .5, 1.2); m4.setPosition(x, y, z); im.setMatrixAt(k, m4); im.setColorAt(k, cols[r]); });
    im.userData.noMerge = true; im.castShadow = true; g.add(im);
    box(.08, .08, len - .2, RK.steel, W_.x + .3, top - .12, zc, g);   // two auto-belays on a rail along the top (plan v4: two climb at once)
    for (const r of [1, 2]) { const z = W_.z0 + len * (r + .5) / REC_ROUTES; box(.2, .22, .2, RK.belay, W_.x + .3, top - .3, z, g); }
    // the bell, on a bracket at the very top between the middle routes
    box(.5, .06, .06, RK.brass, W_.x + .3, top - .05, zc, g); const bell = cyl(.09, .2, .26, RK.brass, W_.x + .5, top - .25, zc, g, 16); cyl(.03, .03, .05, RK.brass, W_.x + .5, top - .1, zc, g, 8);
    return { w: .4, d: len, noBlock: true };
  },
});
function recKayak(g, x, y, z, rot, m) {                  // a kayak: a long pointed hull, a dark cockpit rim (no R())
  const k = new THREE.Group(); k.position.set(x, y, z); k.rotation.y = rot; g.add(k);
  soft(m, 0, 0, 0, .3, .13, 1.3, k); cyl(.17, .17, .05, RK.black, 0, .1, .1, k, 14);
}
Object.assign(KIT, {
  // the float room (0.80.5, R6): soft coral padding on its walls and slow light orbs drifting round the room (one
  // instanced mesh in a group that turns, via SPINS). Room-local, 8 x 6; the lobby's glass is the north side
  recFloatRoom(g) {
    for (const [x, z, w, d] of [[4, 5.83, 7.7, .14], [.17, 3.1, .14, 5.5], [7.83, 3.1, .14, 5.5]]) for (let k = 0; k < 2; k++)
      box(w, .44, d, k % 2 ? RK.padA : RK.padB, x, .24 + k * .46, z, g);                        // padded panels, waist high (taller ones hid the room from the camera)
    const orbs = new THREE.Group(); orbs.position.set(4, 0, 3); g.add(orbs);
    const im = new THREE.InstancedMesh(new THREE.SphereGeometry(.13, 12, 8), RK.orb, 9), m4 = new THREE.Matrix4();
    for (let k = 0; k < 9; k++) { const a = k * .698, r = 1.2 + recHash(k, 2, 17) * 1.4; m4.makeTranslation(Math.cos(a) * r, 1.1 + recHash(k, 3, 17) * (H - 1.6), Math.sin(a) * r * .7); im.setMatrixAt(k, m4); }
    im.userData.noMerge = true; im.castShadow = false; orbs.add(im); SPINS.push({ o: orbs, ax: 'y', w: .12 });
    return { w: .1, d: .1, noBlock: true };
  },
  recProjector(g) {
    box(.08, .9, .08, RK.black, 0, .45, 0, g); box(.5, .28, .4, RK.black, 0, 1.04, 0, g); cyl(.08, .09, .1, RK.steel, 0, 1.06, .24, g, 14).rotation.x = Math.PI / 2;
    return { w: .5, d: .4 };
  },
});
// the concourse's showpieces (0.80.8, the user's: "not nearly fun looking enough"): the big REC DEC sign on a gantry
// across the concourse by the lift, bunting, murals, a signpost and a trophy case. Canvases drawn per visit, no R()
Object.assign(KIT, {
  recBigSign(g, o) {
    const half = o.span / 2, y = H - 1.0;
    for (const z of [-half, half]) { box(.12, y + .55, .12, RK.black, 0, (y + .55) / 2, z, g); box(.3, .04, .3, RK.black, 0, .02, z, g); }
    box(.14, .1, o.span, RK.black, 0, y + .55, 0, g);
    const t = tex(1024, 300, (c, w, h) => {
      c.fillStyle = '#120b1c'; c.fillRect(0, 0, w, h); c.strokeStyle = '#50e6ff'; c.lineWidth = 8; c.shadowColor = '#50e6ff'; c.shadowBlur = 24; c.strokeRect(16, 16, w - 32, h - 32);
      c.textAlign = 'center'; c.font = '900 168px system-ui,sans-serif'; c.shadowColor = '#ff4fd8'; c.shadowBlur = 40;
      c.lineWidth = 10; c.strokeStyle = '#ff4fd8'; c.strokeText('REC DEC', w / 2, 192); c.fillStyle = '#ffe3fa'; c.fillText('REC DEC', w / 2, 192);
      c.shadowBlur = 16; c.shadowColor = '#50e6ff'; c.fillStyle = '#bff6ff'; c.font = '700 34px system-ui,sans-serif'; c.fillText('THE RECREATION DECK  ·  OPEN 06:00 TO MIDNIGHT', w / 2, 258);
    });
    const m = new THREE.MeshBasicMaterial({ map: t, toneMapped: false });
    for (const s of [1, -1]) { const p = new THREE.Mesh(new THREE.PlaneGeometry(o.span - .3, (o.span - .3) * 300 / 1024), m); p.rotation.y = s * Math.PI / 2; p.position.set(s * .06, y, 0); g.add(p); }
    box(.08, (o.span - .2) * 300 / 1024, o.span - .2, RK.black, 0, y, 0, g);
    return { w: .2, d: o.span, noBlock: true };
  },
  // a string of pennants across the concourse, four colours, sagging a little
  recBunting(g, o) {
    const n = 11, half = o.span / 2, cs = [RK.flagA, RK.flagB, RK.flagC, RK.flagD], tri = new THREE.Shape(); tri.moveTo(-.11, 0); tri.lineTo(.11, 0); tri.lineTo(0, -.24); tri.closePath();
    const geo = new THREE.ShapeGeometry(tri);
    for (let k = 0; k < n; k++) { const u = (k + .5) / n, z = -half + o.span * u, y = H - .55 - .35 * 4 * u * (1 - u); const f = new THREE.Mesh(geo, cs[k % 4]); f.position.set(0, y, z); f.rotation.y = Math.PI / 2; g.add(f); }
    const line = box(.012, .012, o.span, RK.black, 0, H - .55 - .17, 0, g); line.scale.y = 1;
    return { w: .1, d: o.span, noBlock: true };
  },
  recSignpost(g) {
    box(.08, 2.3, .08, RK.black, 0, 1.15, 0, g);
    [['POOL  ·  AUDITORIUM  →', '#50e6ff'], ['←  RIVERS  ·  WALL  ·  COURT', '#ff9a3c'], ['FLOAT ROOM  ↓', '#ff6fe0']].forEach(([txt, c_], k) => {
      const t = tex(512, 80, (c, w, h) => { c.fillStyle = '#16181c'; c.fillRect(0, 0, w, h); c.fillStyle = c_; c.fillRect(0, 0, 10, h); c.fillStyle = '#f4f4f0'; c.font = '700 34px system-ui,sans-serif'; c.textBaseline = 'middle'; c.fillText(txt, 28, h / 2 + 2); });
      const p = new THREE.Mesh(new THREE.BoxGeometry(1.25, .2, .04), [RK.black, RK.black, RK.black, RK.black, new THREE.MeshBasicMaterial({ map: t, toneMapped: false }), RK.black]); p.position.set(.1, 2.0 - k * .28, .07); g.add(p);
    });
    return { w: .3, d: .3, noBlock: true };
  },
  recTrophyCase(g, o) {
    const w = o.w || 1.4;
    box(w, .9, .45, RK.black, 0, .45, 0, g); box(w, .06, .47, RK.gold, 0, .93, 0, g);
    box(w, .9, .04, RK.black, 0, 1.41, -.2, g);   // the back panel
    for (let k = 0; k < 3; k++) { const x = -w / 2 + w * (k + .5) / 3; cyl(.05, .03, .08, RK.gold, x, 1.0, .05, g, 10); cyl(.09 - k * .015, .04, .2 + k * .04, RK.gold, x, 1.14 + k * .02, .05, g, 12); }
    box(w + .02, .02, .47, RK.gold, 0, 1.87, 0, g);
    return { w, d: .47 };
  },
});
Object.assign(WALL_KIT, {
  // a bold painted mural: diagonal bands in the deck's colours and the five things you can do here
  recMural(g, o) {
    const W_ = o.w || 1.9, Hh = W_ * .5;
    const t = tex(512, 256, (c, w, h) => {
      const cs = ['#1fa39b', '#ff6f61', '#ffd23f', '#50e6ff', '#ff4fd8', '#2a1d45'];
      c.fillStyle = '#2a1d45'; c.fillRect(0, 0, w, h);
      for (let k = -2; k < 9; k++) { c.fillStyle = cs[(k + 6) % 5]; c.beginPath(); c.moveTo(k * 70, h); c.lineTo(k * 70 + 40, h); c.lineTo(k * 70 + 40 + h * .6, 0); c.lineTo(k * 70 + h * .6, 0); c.closePath(); c.fill(); }
      c.fillStyle = 'rgba(18,11,28,.72)'; c.fillRect(0, h * .3, w, h * .4);
      c.textAlign = 'center'; c.fillStyle = '#ffffff'; c.font = '900 40px system-ui,sans-serif'; c.fillText(o.text || 'SWIM · PADDLE · CLIMB', w / 2, h * .5 + 14);
    });
    const p = new THREE.Mesh(new THREE.PlaneGeometry(W_, Hh), new THREE.MeshBasicMaterial({ map: t, toneMapped: false })); p.position.set(o.off || 0, o.y || 2.45, .03); g.add(p);
  },
});
// the rec deck's machines (0.84.0, rec engineer B; plans/recdeck-plan.html section 6): { id, kind, at, room, face, panel, look? }
// like every deck's, each with a work:works place at its panel (pushed after DECKS[7]). section 17 lists them only while
// REC_DECK is on (machineList), so a dormant rec deck wears nothing, posts nothing and sends nobody down
const REC_MACHINES = [
  { id: '7-pool-filter-1', kind: 'poolfilter', at: [33, 1], room: 'p', face: 'w', panel: [32, 1] },
  { id: '7-pool-filter-2', kind: 'poolfilter', at: [33, 5], room: 'p', face: 'w', panel: [32, 5] },
  { id: '7-pool-dosing', kind: 'pooldoser', at: [33, 3], room: 'p', face: 'w', panel: [32, 3], look: { lamp: [.25, 1.2, .45], drip: [.25, .9, .51], light: [.25, 2.1, .45] } },
  { id: '7-pool-heat', kind: 'poolheat', at: [33, 3], room: 'p', face: 'w', panel: [32, 4], look: { lamp: [-.25, 1.2, .45], drip: [-.25, .9, .51], light: [-.25, 2.1, .45] } },
  { id: '7-river-pump-1', kind: 'riverpump', at: [1, 7], room: 'r', face: 'e', panel: [2, 7] },
  { id: '7-river-pump-2', kind: 'riverpump', at: [1, 10], room: 'r', face: 'e', panel: [2, 10] },
  { id: '7-wave-gate', kind: 'wavegate', at: [12, 1], room: 'K', face: 'e', panel: [15, 1], look: { lamp: [0, 1.6, -.2], drip: [0, .5, -.15], light: [0, 2.4, -.2] } },
  { id: '7-wall-holds', kind: 'wallholds', at: [1, 5], room: 'K', face: 'e', panel: [2, 5], look: { lamp: [0, 1.5, .15], drip: [0, .6, .2], light: [0, 2.6, .15] } },
  { id: '7-belay-1', kind: 'belay', at: [1, 3], room: 'K', face: 'e', panel: [2, 3], look: { lamp: [0, 3.0, .2], drip: [0, 2.8, .25], light: [0, 3.4, .2] } },
  { id: '7-belay-2', kind: 'belay', at: [1, 4], room: 'K', face: 'e', panel: [2, 4], look: { lamp: [0, 3.0, .2], drip: [0, 2.8, .25], light: [0, 3.4, .2] } },
  { id: '7-aud-lights', kind: 'stagelights', at: [28, 13], room: 'b', face: 'e', panel: [29, 13] },
  { id: '7-aud-sound', kind: 'soundrack', at: [28, 15], room: 'b', face: 'e', panel: [29, 15] },
  { id: '7-aud-seats', kind: 'seathinges', at: [40, 7], room: 'A', face: 'e', panel: [41, 7], look: { lamp: [0, .6, .2], drip: [0, .4, .25], light: [0, 1.4, .2] } },
  { id: '7-court-net', kind: 'courtnet', at: [1, 12], room: 'e', face: 'e', panel: [2, 12] },
  { id: '7-court-board', kind: 'scoreboard', at: [1, 14], room: 'e', face: 'e', panel: [2, 14] },
  { id: '7-grav-plates', kind: 'gravplate', at: [30, 17], room: 'b', face: 'n', panel: [30, 17] },
];
const REC_FACE_BACK = { n: 's', s: 'n', e: 'w', w: 'e' };
// the crew's places (RA, 0.83.0, plan v5 section 9 "Capacity and busyness"): what they do here and where they wait for a
// turn. Swimming: one per lane (4), at the shallow end; kayaks: 3 on the slow channel (you make the 4th); the wall: 2
// auto-belays (routes red and blue); the float room: 6; and the waiting spots: the loungers and the pool's edge, the dock's
// beach, the pebble beach under the wall, the lobby glass by the float room. The stands' seats by the gate are the court's
// queue (schedData's '7|rec-courtq'). anim is section 8c's pose (section 8b's ACTS) for whoever is there
const REC_CREW_PLACES = [
  ...[1.35, 2.25, 3.15, 4.05].map((z, k) => ({ id: '7-lane-' + (k + 1), type: 'rec:lane', at: [24, Math.floor(z)], walk: [23, Math.floor(z)], xy: [24.6, z], y: .35, face: 'e', pose: 'stand', anim: 'swim', room: 'P',
    move: { kind: 'swim', path: [[24.6, z], [30.5, z]], y: .35, phase: k * .25 } })),   // move: rec engineer B's crew moves (0.84.6), looped while settled
  ...[[24.4, 6.55], [27.6, 6.55], [29.6, 6.55]].map(([x, z], k) => ({ id: '7-lounger-' + (k + 1), type: 'rec:poolq', at: [Math.floor(x), 6], walk: [Math.floor(x), 5], xy: [x, z - .1], y: .42, face: 'n', pose: 'sit', room: 'P' })),
  ...[25.6, 28.6].map((x, k) => ({ id: '7-pooledge-' + (k + 1), type: 'rec:poolq', at: [Math.floor(x), 5], xy: [x, 5.05], y: .42, face: 'n', pose: 'sit', room: 'P' })),
  ...[9.4, 7.4, 5.4].map((x, k) => ({ id: '7-kayak-' + (k + 1), type: 'rec:kayak', at: [Math.floor(x), 4], walk: [Math.floor(x) + 1, 6], xy: [x, 4.85], y: .36, face: 'w', pose: 'stand', anim: 'kayak', room: 'K',
    move: { kind: 'kayak', path: [[11.4, 4.85], [4.8, 4.85], [4.8, 1.3], [13.8, 1.3, 1], [13.8, 4.85, 1]], y: .36, phase: k / 3 } })),   // 15r's REC_LOOP (not readable yet here)
  ...[13, 14].map((c, k) => ({ id: '7-dockq-' + (k + 1), type: 'rec:kayakq', at: [c, 6], face: 'n', pose: 'stand', room: 'K' })),
  ...[3.725, 4.875].map((z, k) => ({ id: '7-climb-' + (k + 1),   // under the two belays (routes 2 and 3 of 4: B2's)
   type: 'rec:climb', at: [2, Math.floor(z)], xy: [1.95, z], face: 'w', pose: 'stand', anim: 'climb', room: 'K',
    move: { kind: 'climb', at: [1.95, z], face: 'w', top: 1.39, rest: 4, phase: k * .5 } })),   // top: 15r's H - 2.25 with the deck's 1.3 walls
  ...[3, 5].map((r, k) => ({ id: '7-beach-' + (k + 1), type: 'rec:climbq', at: [3, r], face: 'w', pose: 'stand', room: 'K' })),
  ...[[18.5, 13.5], [20.5, 13.3], [22.5, 13.5], [18.5, 16.2], [20.5, 16.4], [22.5, 16.2]].map(([x, z], k) => ({ id: '7-float-' + (k + 1), type: 'rec:float', at: [Math.floor(x), Math.floor(z)], xy: [x, z], face: k < 3 ? 's' : 'n', pose: 'stand', anim: 'float', room: 'F',
    move: { kind: 'float', at: [x, z], r: .6, top: 2.0 } })),
  ...[20, 21].map((c, k) => ({ id: '7-floatq-' + (k + 1), type: 'rec:floatq', at: [c, 11], face: 's', pose: 'stand', room: '+' })),
  // the changing rooms (crew change for the pool and the kayaks, as you do): two lockers either side of yours, two showers
  ...[[18.0, 18], [20.7, 20]].map(([x, c], k) => ({ id: '7-locker-' + (k + 1), type: 'rec:locker', at: [c, 1], xy: [x, 1.25], face: 'n', pose: 'stand', anim: 'browse', room: 'w' })),
  ...[17.65, 18.9].map((x, k) => ({ id: '7-rshower-' + (k + 1), type: 'rec:shower', at: [17, 2], xy: [x, 3.35], face: 's', pose: 'stand', anim: 'wash', room: 'w' })),
  // the traditions' places (0.83.2): the Wren talks' ring of eight chairs on the stage (schedData's '7|rec-ring'; the
  // chairs themselves are the auditorium's dressing), the chief's stool at the stage's front, the Captain's lectern and the
  // Commander behind her, two acts' spots and the piano for talent night, and Maeve's chair at the booth's lighting desk
  ...Array.from({ length: 8 }, (_, k) => { const a = k / 8 * 2 * Math.PI, x = 43.7 + Math.cos(a) * 1.05, z = 9.0 + Math.sin(a) * 1.05;
    return { id: '7-ring-' + (k + 1), type: 'rec:seat', ring: true, at: [Math.floor(x), Math.floor(z)], walk: [41, Math.max(3, Math.min(14, Math.floor(z)))], xy: [+x.toFixed(2), +z.toFixed(2)], y: 1.05,
      face: Math.round(Math.atan2(43.7 - x, 9.0 - z) * 180 / Math.PI), pose: 'sit', room: 'A' }; }),
  { id: '7-stool-1', type: 'rec:stool', at: [42, 9], walk: [41, 9], xy: [42.35, 9.0], y: 1.04, face: 'w', pose: 'sit', room: 'A' },
  { id: '7-lectern-1', type: 'rec:lectern', at: [43, 7], walk: [41, 7], xy: [43.3, 7.3], y: .55, face: 'w', pose: 'stand', room: 'A', move: { kind: 'address' } },   // the spots and moves: rec engineer B2's (0.84.9)
  { id: '7-lectern-2', type: 'rec:lectern', at: [43, 8], walk: [41, 8], xy: [43.95, 8.4], y: .55, face: 'w', pose: 'stand', room: 'A' },
  { id: '7-act-1', type: 'rec:act', at: [43, 9], walk: [41, 9], xy: [43.3, 9.6], y: .55, face: 'w', pose: 'stand', room: 'A', move: { kind: 'perform', act: 'sing' } },   // at the mic
  { id: '7-act-2', type: 'rec:act', at: [43, 10], walk: [41, 10], xy: [43.3, 10.2], y: .55, face: 'w', pose: 'stand', room: 'A', move: { kind: 'perform', act: 'juggle' } },
  { id: '7-act-piano', type: 'rec:act', at: [43, 11], walk: [41, 11], xy: [43.0, 11.3], y: 1.1, face: 's', pose: 'sit', anim: 'play', room: 'A', move: { kind: 'perform', act: 'piano' } },   // the bench by the side-on piano
  { id: '7-booth-1', type: 'rec:booth', works: true, at: [32, 12], xy: [32.85, 12.6], y: .45, face: 'e', pose: 'sit', room: 'b' },
  // the regatta's crowd (the gather venue 'river-banks', DECKS[7].gathers): the beach, the concourse's glass, the bank by the
  // rack; Chief Holt's spot with his horn on the dock (lead 1)
  { id: '7-river-banks-lead-1', type: 'event', gather: 'river-banks', lead: 1, at: [11, 6], xy: [11.6, 6.35], face: 0, pose: 'stand', room: 'K' },
  ...[[2, 6], [3, 6], [4, 6], [5, 6], [7, 6], [9, 6], [12, 6], [15, 1], [15, 2], [15, 3], [15, 4], [15, 5], [16, 1], [16, 2], [16, 4], [16, 5]].map(([c, r], k) => ({ id: '7-river-banks-crowd-' + (k + 1), type: 'event', gather: 'river-banks', at: [c, r], face: r === 6 ? 'n' : 'w', pose: 'stand', room: 'K' })),
  ...[5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15].map((c, k) => ({ id: '7-river-banks-crowd-' + (17 + k), type: 'event', gather: 'river-banks', at: [c, 7], face: 'n', pose: 'stand', room: '=' })),
];
DECKS[7] = {
  num: 7, name: 'Recreation', seed: 70771, tall: 1.3, playerOnly: !REC_DECK, open: [6, 24],   // 0.83.0 (RA): the crew come when the deck is switched on
  blurb: 'Auditorium, court, pool, rivers', arrive: 'The concourse runs stern to bow: the rivers and the court aft, the pool and the auditorium forward.',
  lift: [20, 9],
  // car on columns 19-20, rows 7-9; trunks behind glass on row 6, the ladder on row 10: the same world spot as every deck
  map: [
    '..KKKKKKKKKKKKKKKwwwwwwPPPPPPPPPppAAAA........',
    '.KKKKKKKKKKKKKKKKwwwwwwPPPPPPPPPppAAAAAA......',
    '.KKKKKKKKKKKKKKKKwwwwwwPPPPPPPPPppAAAAAAAA....',
    '.KKKKKKKKKKKKKKKKwwwwwwPPPPPPPPPppAAAAAAAAA...',
    '.KKKKKKKKKKKKKKKKkkkkkkPPPPPPPPPppAAAAAAAAAA..',
    '.KKKKKKKKKKKKKKKKkkkkkkPPPPPPPPPppAAAAAAAAAAA.',
    '.KKKKKKKKKKKKKKKK++YY++PPPPPPPPPppAAAAAAAAAAA.',
    '.rrr=============++@@++=======ffffAAAAAAAAAAA.',
    '.rrr=============++@@++=======ffffAAAAAAAAAAAA',
    '.rrr=============++@@++=======ffffAAAAAAAAAAAA',
    '.rrr=============++ZZ++=======ffffAAAAAAAAAAA.',
    '.eeeTTTTTTTTTTTTT++++++==uuubbbbbbAAAAAAAAAAA.',
    '.eeeTTTTTTTTTTTTTFFFFFFFFuuubbbbbbAAAAAAAAAAA.',
    '.eeeCCCCCCCCCCCCCFFFFFFFFuuubbbbbbAAAAAAAAAA..',
    '.eeeCCCCCCCCCCCCCFFFFFFFFuuubbbbbbAAAAAAAAA...',
    '.eeeCCCCCCCCCCCCCFFFFFFFFuuubbbbbbAAAAAAAA....',
    '.eeeCCCCCCCCCCCCCFFFFFFFFuuubbbbbbAAAAAA......',
    '..eeCCCCCCCCCCCCCFFFFFFFFuuubbbbbbAAAA........',
  ],
  // the plan's DOORSR. Changes: the court's gate is at h,14,13 (the stands' bow aisle; the plan had h,10,13, which the benches fill), and v,19,10 and v,21,10 are solid wall (not glass), so the lift's call panels sit beside
  // the doors as on every deck. pass: a counter opening (the kit hire desk) or a rail with no pane (the court's).
  doors: {
    'v,19,7': 'lift', 'v,19,8': 'lift', 'v,19,9': 'lift', 'v,21,7': 'lift', 'v,21,8': 'lift', 'v,21,9': 'lift',   // one wide door each side
    'v,19,6': 'glass', 'v,21,6': 'glass',                    // the trunks, behind glass above the car
    'h,19,11': 'glass', 'h,20,11': 'hatch',                  // the ladder, with its hatch
    'h,17,6': 'pass', 'h,18,6': 'pass', 'h,22,6': 'door',    // kit hire: the counter onto the lobby, and its door
    'h,21,4': 'door',                                        // kit hire through to the changing rooms
    'v,17,1': 'door', 'v,17,2': 'glass',                     // changing rooms to the river hall (the wet way)
    'v,23,2': 'door', 'v,23,1': 'glass',                     // changing rooms to the pool (the wet way)
    'h,9,7': 'door', 'h,10,7': 'door', 'h,5,7': 'glass', 'h,6,7': 'glass', 'h,7,7': 'glass', 'h,8,7': 'glass',
    'h,11,7': 'glass', 'h,12,7': 'glass', 'h,13,7': 'glass', 'h,14,7': 'glass', 'h,15,7': 'glass',   // the river hall's viewing glass
    'v,4,8': 'hatch',                                        // river pump room, off the concourse's aft end
    'h,6,11': 'door', 'h,14,11': 'door', 'h,7,11': 'glass', 'h,8,11': 'glass', 'h,9,11': 'glass', 'h,10,11': 'glass',
    'h,11,11': 'glass', 'h,12,11': 'glass', 'h,13,11': 'glass', 'h,15,11': 'glass',   // the stands, behind glass on the concourse
    'h,10,13': 'pass', 'h,4,13': 'pass', 'h,5,13': 'pass', 'h,6,13': 'pass', 'h,7,13': 'pass', 'h,8,13': 'pass', 'h,9,13': 'pass',
    'h,11,13': 'pass', 'h,12,13': 'pass', 'h,13,13': 'pass', 'h,14,13': 'door', 'h,15,13': 'pass', 'h,16,13': 'pass',   // the court's rail and its gate (0.80.2: at column 14, the stands' bow aisle, near your baseline)
    'v,4,15': 'hatch',                                       // the court's emitter room
    'h,26,7': 'door', 'h,23,7': 'glass', 'h,24,7': 'glass', 'h,25,7': 'glass', 'h,27,7': 'glass', 'h,28,7': 'glass', 'h,29,7': 'glass',   // the pool's gallery
    'v,32,3': 'hatch',                                       // pool plant, from the pool deck
    'v,34,7': 'door', 'v,34,8': 'door', 'v,34,9': 'door', 'v,34,10': 'door',   // foyer into the auditorium: four wide doors
    'h,26,11': 'door',                                       // washroom
    'h,18,12': 'door', 'h,17,12': 'glass', 'h,21,12': 'glass', 'h,22,12': 'glass', 'h,23,12': 'glass', 'h,24,12': 'glass',   // float room
    'h,31,11': 'hatch', 'v,34,12': 'glass', 'v,34,11': 'hatch',   // rec utility room: from the foyer, the booth window and the stage door
  },
  plates: [['h,21,6', 's', 'Recreation Deck'], ['h,22,4', 's', 'Changing rooms'], ['h,16,7', 's', 'River hall'], ['h,5,11', 'n', 'Stands'],
    ['h,30,7', 's', 'Pool gallery'], ['h,25,11', 'n', 'Washroom'], ['h,19,12', 'n', 'Float room']],
  rooms: {
    '=': { name: 'Concourse', floor: 'concourse', hall: true, rec: true },
    '+': { name: 'Lift lobby', floor: 'concourse', hall: true, rec: true },
    f: { name: 'Foyer', floor: 'concourse', hall: true, rec: true },
    '@': { name: 'Main lift', floor: 'lift' },
    Y: { name: 'Spine trunks', floor: 'grate', spine: true }, Z: { name: 'Spine ladder', floor: 'grate', spine: true },
    A: { name: 'Auditorium', floor: 'violet', rec: true },
    C: { name: 'Lightdisc court', floor: 'court', rec: true },
    T: { name: 'Stands', floor: 'stand', rec: true },
    K: { name: 'River hall', floor: 'river', rec: true },
    P: { name: 'Pool', floor: 'pooltile', rec: true },
    F: { name: 'Float room', floor: 'pad', rec: true },
    w: { name: 'Changing rooms', floor: 'tile', rec: true },
    k: { name: 'Kit hire', floor: 'sport', rec: true },
    u: { name: 'Washroom', floor: 'tile', rec: true },
    // service rooms: Works and you, through hatches (their machines come with the systems engineer; section 6 of the plan)
    b: { name: 'Rec utility room', floor: 'svc', rec: true, still: true },
    r: { name: 'River pump room', floor: 'svc', rec: true, still: true },
    p: { name: 'Pool plant', floor: 'svc', rec: true, still: true },
    e: { name: 'Emitter room', floor: 'svc', rec: true, still: true },
  },
  windows: ['P', 'K', 'A'].map(room => ({ room })),
  closedDoors: {
    'h,20,11': { t: 'Spine ladder', x: 'The maintenance ladder, up to Quarters and down to Operations, through the rec deck on the way. Tier 2 access.' },
  },
  hull: { sternX: 1, stern: 2, bowFrom: 34, bowLen: 11.6, byFace: true },
  service: [{ key: 'v,4,8', tier: 2 }, { key: 'v,4,15', tier: 2 }, { key: 'v,32,3', tier: 1 }, { key: 'h,31,11', tier: 1 }, { key: 'v,34,11', tier: 1 }],
  machines: REC_MACHINES,                                // 0.84.0 (rec engineer B): section 6's machines, above
  // the auditorium's seats (0.80.1): reached from the aisle beside their row; a type no crew code knows, so they stay the player's
  places: REC_SEATS.map((s, k) => ({ id: '7-seat-' + (k + 1), type: 'rec:seat', at: [s.col, Math.floor(s.z)], walk: [s.col, s.aisle], face: 'e', pose: 'sit', anim: 'slump', room: 'A', xy: [s.x, s.z], y: Math.round((s.h + .47) * 100) / 100 }))   // slump: rec engineer B's seated pose (0.83.2)
    // the stands' 33 seats (0.80.2), facing the court, reached from the aisle at column 6 or 14
    .concat(REC_STAND_SEATS.map((s, k) => ({ id: '7-stand-' + (k + 1), type: 'rec:seat', at: [s.col, s.tier ? 12 : 11], walk: [s.aisle, s.tier ? 12 : 11], face: 's', pose: 'sit', room: 'T', xy: [s.col + .5, s.z + .02], y: Math.round((s.h + .45) * 100) / 100, move: { kind: 'fan' } })))   // fan: B's cheer, clap and groan together
    // the concourse's two beanbags (0.80.9, the user's): lounge seats like the music room's, so crew can use them in phase 2
    .concat([[5, 5.5, 7.45], [6, 6.6, 7.55]].map(([c, x, z], k) => ({ id: '7-beanbag-' + (k + 1), type: 'lounge-seat', at: [c, 7], walk: [c, 8], face: 's', pose: 'sit', anim: 'slump', room: '=', xy: [x, z], y: .42, cush: .32 })))
    .concat(REC_CREW_PLACES),
  dress(d) {
    recMats();
    for (const [key, tw, text] of d.plates) placeOnEdge('plate', key, tw, { text });
    for (const [key, tw] of [['v,19,10', 'w'], ['v,21,10', 'e']]) placeOnEdge('liftPanel', key, tw);
    placeOnEdge('deckDirectory', 'h,20,12', 'n', { it: IT('Deck directory', 'Seven decks, top to bottom. Bridge, Command & Science, Commons, Quarters, the Recreation Deck (R), Operations, Engineering. You are here: the Recreation Deck, between Quarters and Operations.') });
    for (const r of ['Y', 'Z']) NO_FADE.add(r);
    place('Y', 'spineTrunks', 1, .5, 'n', { it: SPINE_IT.trunks });
    place('Z', 'spineLadder', 1, .5, 'n', { it: { t: 'Spine ladder', x: 'The maintenance ladder, passing through on its way from Quarters down to Operations.', see: true } });
    // kit hire (6 x 2): self-serve shelves on the back wall, the counter at the lobby's opening, a returns bin and the sign
    for (const x of [.7, 1.95, 3.2]) place('k', 'shelving', x, .33, 'n', { it: IT('Kit shelves', 'Rec kit in every size, towels, helmets, buoyancy vests, paddles, climbing shoes and harnesses, disc gloves and grip socks. Nobody staffs it: take what you need.') });
    place('k', 'counter', 1.0, 1.62, 's', { it: IT('Kit hire', 'A self-serve counter onto the lobby. Someone has left a single flipper on it.') });
    place('k', 'hamper', 5.45, .4, 'n', { snug: true, it: IT('Returns bin', 'Wet towels and used kit go in here. It is always fuller than it should be.') });
    placeWall('k', 'plate', 'e', .5, { text: 'PUT IT BACK' });
    // changing rooms (6 x 4): lockers on the hull wall, a bench down the middle, two showers in the aft corner, lost property
    for (const x of [1.0, 2.35, 3.7]) place('w', 'locker', x, .42, 'n', { it: IT('Lockers', 'Rec deck lockers. Yours is whichever one is free; the keys are on stretchy wristbands.') });
    place('w', 'bench', 2.6, 2.5, 'n', { w: 2.2, snug: true, it: IT('Bench', 'Wet, always. Someone has written SIT HERE on a towel.') });
    for (const x of [.65, 1.9]) place('w', 'showerStall', x, 3.38, 's', { it: IT('Shower', 'A quick rinse before the pool and after it. The hot water takes a moment to remember.') });
    place('w', 'footlocker', 5.35, .32, 'n', { it: IT('Lost property', 'Odd socks, a single earring, three water bottles, and a goggle strap with no goggles.') });
    // washroom (3 x 7): four stalls on the bow side, a row of basins opposite
    for (const z of [1.9, 3.1, 4.3, 5.5]) place('u', 'toiletStall', 2.45, z, 'e');
    place('u', 'basinCounter', .38, 3.5, 'w', { w: 2.6, it: IT('Basins', 'A long row of basins for the interval queue.') });
    // the concourse: a towel bin by the lobby (0.80.2: its two benches went; the stands fill that glass now)
    // 0.80.8 (the user's: livelier, busier): the REC DEC gantry sign by the lift, bunting, murals, beanbags, plants, benches,
    // a water station and a drinks fridge, a trophy case, a signpost; all along the edges, clear of every door and the lanes' middle
    place('+', 'recBigSign', .6, 3.0, 'n', { span: 3.4,   // 0.82.8 (the user's): the lift's stern side again, but in the lobby, in front of the wall that hid it (0.82.5 had it east of the lift)
      it: IT('REC DEC', 'A gantry across the concourse with REC DEC in pink neon, two storeys up. You can see it the moment the lift doors open.') });
    place('=', 'recBunting', 8.5, 2.0, 'n', { span: 3.8 });   // 0.80.9 (the user's: a little too busy): one string, and fewer things below
    for (const [x, z, f] of [[1.5, .5, RK.padA], [2.6, .6, RK.kayak[1]]]) place('=', 'beanbag', x, z, 'n', { fab: f, it: IT('Beanbag', 'A big squashy beanbag, still warm. Someone is always about to get up from it.') });
    for (const [x, z] of [[.4, .35], [25.6, .35]]) place('=', 'plant', x, z, 'n');
    place('=', 'dispenser', 11.5, 3.65, 's', { it: IT('Water station', 'Cold water and a stack of cups. A sign says DRINK BEFORE YOU CLIMB.') });
    place('=', 'drinksFridge', 25.5, 3.6, 's', { it: IT('Drinks fridge', 'Fizzy lime, cold tea and something blue called RIPTIDE.') });
    place('=', 'recTrophyCase', 23.9, 3.7, 's', { w: 1.4, it: IT('Trophy case', 'Three gold cups and an empty shelf, waiting for this season\'s winners.') });
    placeOnEdge('recMural', 'v,4,9', 'e', { w: 1.9, off: -.5, text: 'SWIM · PADDLE · CLIMB', it: IT('Mural', 'A bold mural in teal, coral and neon: SWIM, PADDLE, CLIMB.') });
    place('+', 'recSignpost', 4.4, 5.4, 'n',   // 0.82.5: in the lobby's open floor, its boards clear of the wall (was 5.6, 5.5)
      { it: IT('Signpost', 'Pool and auditorium forward, rivers, wall and court aft, the float room through the glass.') });
    place('=', 'hamper', 12.4, .45, 'n', { snug: true, it: IT('Towel bin', 'For wet towels from the river hall. It smells of chlorine and good intentions.') });
    // the auditorium (0.80.1, R2): the rake and its 76 seats, the stage against the bow windows, the truss, lectern, piano and screen
    const rake = []; for (let c = 1; c <= 6; c++) for (const [z0, z1] of REC_BLOCKS) for (let z = z0; z < z1; z++) rake.push([c, z]);
    place('A', 'recRake', 0, 0, 'n', { block: rake });
    REC_BLOCKS.forEach(([z0, z1], b) => place('A', 'recHit', 3.5, (z0 + z1) / 2, 'n', { w: 6, d: z1 - z0, hitH: 1.6, it: IT('Seats', ['The side seats by the hull: a good view of the piano, and nobody climbing over you.', 'The middle block. Deep violet seats with gold numbers on their backs, all facing the stage and the stars behind it.', 'The side seats on the starboard side, nearest the booth window. The sound is best here, they say.'][b]) }));
    const stage = []; for (let j = 0; j < 18; j++) for (let c = 8; c < 12; c++) { const v = (j + .5 - 9) / REC_STAGE.rz; if (Math.abs(v) < 1 && c + .5 < REC_STAGE.back * Math.sqrt(1 - v * v)) stage.push([c, j]); }
    place('A', 'recStage', 0, 0, 'n', { block: stage });
    place('A', 'recHit', 9.3, 9, 'n', { w: 2.6, d: 9, hitH: .8, it: IT('Stage', 'A curved stage across the bow, and behind it nothing but the windows and the stars. Every show here is played against them.') });
    place('A', 'recTruss', 9.6, 9, 'n', { len: 8, it: IT('Lighting truss', 'A gold truss over the stage on two towers, with six lamps aimed down. The booth runs them.') });
    place('A', 'recScreen', 10.3, 9, 'n', { len: 6 });
    place('A', 'recRing', 9.7, 9, 'n', { r: 1.05, stool: [-1.35, 0] }).position.y = .55;   // 0.84.12: RA's ring (deck 43.7, 9.0) and stool (42.35, 9.0)
    { const ms = place('A', 'micStand', 8.95, 9.6, 'e', { it: IT('Microphone', 'A mic stand at centre stage. Talent night\'s first act always adjusts it, and the second puts it back.') });   // 0.84.9: perform's mic (the music room's kit)
      ms.position.y = .55; mergeMeshes(ms); ms.traverse(m => { if (m.isMesh) m.userData.noMerge = true; }); REC_SHOW.mic = ms; ms.visible = REC_SHOW.state !== 'talk'; }   // 0.84.12: put aside for a talk (it stood in the ring)
    place('A', 'recLectern', 8.8, 7.3, 'e', { it: IT('Lectern', 'The Captain\'s lectern, with the Wren\'s crest on the front. The microphone is bent at exactly her height.') });
    place('A', 'grandPiano', 9.0, 12.6, 's', { it: IT('Grand piano', 'A black grand piano at stage left, lid propped. Someone keeps it tuned, and nobody admits to it.') }).position.y = .55;
    place('A', 'pianoBench', 9.0, 11.25, 's').position.y = .55;   // 0.84.9: talent night's pianist sits here (perform { act: 'piano' }); the piano turned side-on (was 9.4, 12.4 facing w: no room for a bench on the curve)
    // the foyer: the REC DEC neon over the four doors, the deck's poster, a bench
    placeWall('f', 'recNeon', 'e', 2.0, { hitW: 2.4, it: IT('REC DEC', 'A curved pink neon over the auditorium\'s doors. The official sign, RECREATION DECK, was too long to fit.') });
    placeWall('f', 'recPoster', 'n', 2.5, { it: IT('Poster', 'THE REC DEC: pool, rivers, climbing wall, float room, Lightdisc. Open 06:00 to midnight.') });
    place('f', 'bench', 2.9, 3.55, 's', { w: 1.6, snug: true, it: IT('Bench', 'Outside the auditorium doors. Good for waiting, and for hearing the piano through them.') });
    // the Lightdisc court and its stands (0.80.2, R3): lines, the net and side fields, the scoreboard (static), the benches
    place('C', 'recCourt', 0, 0, 'n');
    place('C', 'recHit', 6.5, 2.5, 'n', { w: 12.6, d: 4.6, hitH: .3, it: IT('Lightdisc court', 'A black court with glowing lines, cyan at the bow end and orange at the stern, and a shimmering force-field net across the middle. Tap it, or the panel by the gate, to ask someone down to play.') });
    placeWall('C', 'recScoreboard', 'w', 2.5, { hitW: 2.8, it: IT('Scoreboard', 'Two storeys of scoreboard on the stern wall. It keeps the score of the game on the court.') });
    placeOnEdge('recPlayPanel', 'h,15,13', 's', { it: IT('Ask someone to play', 'A panel by the court gate: ASK SOMEONE TO PLAY.') });
    // 0.80.10 (the user's): the stands look straight onto the court: its rail is a low kick board, no header, no posts above it
    for (let i = 4; i <= 16; i++) { const e = EDGES.get('h,' + i + ',13'); if (e) e.rail = true; }
    for (const p of POSTS) if (p.touch.every(e => e.rail)) p.rail = true;
    writeWalls();
    const stands = []; for (const [c0, c1] of REC_STANDS) for (let c = c0; c < c1; c++) stands.push([c - 4, 0], [c - 4, 1]);
    place('T', 'recStands', 0, 0, 'n', { block: stands });
    // the pool (0.80.3, R4): the raised basin with its water, lanes and mosaic; loungers on the inboard side; the first-aid point
    const pool = []; for (let c = 1; c <= 7; c++) for (let z = 1; z <= 4; z++) pool.push([c, z]);
    place('P', 'recPool', 0, 0, 'n', { block: pool });
    place('P', 'recHit', 4.5, 2.7, 'n', { w: 7.4, d: 3.6, hitH: .5, it: IT('Pool', 'Four short lanes under the hull windows, with the Wren in mosaic on the bottom and the stars beside you. Warm, and very blue.') });
    for (const x of [1.4, 4.6, 6.6]) place('P', 'recLounger', x, 6.55, 'e', { it: IT('Lounger', 'A lounger by the pool, facing the windows. Still damp from someone.') });
    placeWall('P', 'recFirstAid', 'e', 5.6, { it: IT('First-aid point', 'A first-aid kit, a foil blanket and an alarm button that rings in the infirmary. There\'s no lifeguard; this, and the shallow end, are the safety.') });
    // the river hall (0.80.4, R5): the river loop, the island, the wave gate, the dock and kayaks, the rack, the climbing wall and bell
    const river = []; for (let c = 3; c <= 13; c++) for (let z = 0; z <= 5; z++) river.push([c, z]);
    place('K', 'recRiver', 0, 0, 'n', { block: river });
    place('K', 'recHit', 8.3, 1.3, 'n', { w: 10.6, d: 1.6, hitH: .5, it: IT('White water', 'The fast run, along the windows: white water over a hidden ramp, kayakers bracing through the standing wave by the gate.') });
    place('K', 'recHit', 8.3, 4.8, 'n', { w: 10.6, d: 1.6, hitH: .5, it: IT('River', 'The slow return channel, wide and green-blue, where you get your breath back before the next lap.') });
    place('K', 'recHit', 10.4, 5.3, 'n', { w: 2.4, d: .9, hitH: .7, it: IT('Kayak dock', 'A wooden dock on the bank, a pebble beach beside it, and kayaks bumping gently at the edge.') });
    place('K', 'recHit', 11.3, 1.3, 'n', { w: .5, d: 2.0, hitH: 1.8, it: IT('Wave gate', 'A steel gate across the fast run that kicks up a standing wave. Its lights go blue when it\'s running.') });
    place('K', 'recKayakRack', 15.6, 3.7, 'n', { it: IT('Kayak rack', 'Red, yellow and blue kayaks on the rack, paddles and helmets alongside. The green one is always out.') });
    place('K', 'recClimbWall', 0, 0, 'n', { block: [2, 3, 4, 5, 6].map(z => [0, z]) });
    place('K', 'recHit', .55, 4.3, 'n', { w: .6, d: 4.6, hitH: 2.4, it: IT('Climbing wall', 'Ochre and rust rock from the floor to the roof: four routes in red, yellow, blue and green holds, an auto-belay at the top of each, and the brass bell at the very top.') });
    // the float room (0.80.5, R6): padding, drifting light orbs, the gravity sign
    place('F', 'recFloatRoom', 0, 0, 'n');
    place('F', 'recHit', 4, 3, 'n', { w: 7.4, d: 5.4, hitH: .4, it: IT('Float room', 'Soft coral padding, slow light orbs, and the gravity turned down to about a fifth. Everyone who goes in comes out grinning.') });
    placeOnEdge('plate', 'h,19,12', 's', { text: 'GRAVITY 0.2 g' });
    // the service rooms (0.80.5, R6), Works and you through their hatches. TODO (phase 2, the systems engineer): their
    // machines entries (the plan's section 6: 7-river-pump-1/-2, 7-pool-filter-1/-2, 7-pool-dosing, 7-pool-heat, 7-court-net,
    // 7-court-board, 7-aud-lights, 7-aud-sound, 7-grav-plates...) with panel tiles and work:works places
    for (const z of [.95, 3.05]) place('r', 'pumpSkid', .7, z, 'w', { it: IT('River pump', 'One of two big current pumps that drive the rivers round. The fast run needs both.') });
    place('r', 'utilShelf', 2.2, .25, 'n', { it: IT('Pump spares', 'Impellers, seals and a bearing in its box, labelled in Maeve\'s capitals.') });
    placeWall('r', 'workLight', 'e', 3.5);
    for (const z of [1.2, 5.6]) place('p', 'filterBank', 1.5, z, 'e', { it: IT('Pool filter', 'A sand filter for the pool. Seventy-five people, and they all shed.') });
    place('p', 'circPump', 1.55, 3.5, 'e', { it: IT('Water balance', 'The pool\'s doser and its heat exchanger\'s pump, side by side. The top-up water comes down from the recycler.') });
    for (const z of [1.0, 2.0]) place('e', 'powerCabinet', .3, z, 'w', { it: IT('Emitter power', 'The court\'s force-field power units, humming a little higher than anything else aboard.') });
    place('e', 'relayBank', .35, 3.6, 'w', { w: 1.6, it: IT('Emitters', 'The net and side-wall emitters\' controls, and the scoreboard\'s driver.') });
    placeWall('e', 'workLight', 'e', 1.5);
    place('b', 'controlBoard', 5.55, 1.6, 'e', { w: 1.6, it: IT('Lighting desk', 'The booth\'s lighting desk, under the window onto the stage. Every fader is labelled; two are labelled DON\'T.') });
    place('b', 'chair', 4.85, 1.6, 'w');
    place('b', 'recProjector', 5.4, 3.0, 'e', { it: IT('Projector', 'The auditorium\'s projector, aimed through the booth window at the screen over the stage.') });
    place('b', 'relayBank', .35, 2.5, 'w', { w: 2.0, it: IT('Dimmer racks', 'The stage lights\' dimmers, rack after rack.') });
    for (const z of [4.3, 5.3]) place('b', 'powerCabinet', .3, z, 'w', { it: IT('Sound rack', 'Amplifiers and the lectern microphone\'s receiver.') });
    placeWall('b', 'relayBoard', 's', 2.0, { it: IT('Gravity plates', 'The float room\'s gravity plate controller, set to 0.2 g, with its cooling beside it.') });
    place('b', 'expansionTank', 3.5, 6.55, 's');
    place('b', 'dispenser', 4.55, 6.6, 's', { it: IT('Kettle', 'A kettle and a tin of tea for whoever runs the lights.') });
    place('b', 'medCabinet', 5.5, 6.6, 's', { it: IT('First-aid locker', 'Plasters, cold packs and a sign: FLOAT ROOM BUMPS GO IN THE BOOK.') });
    place('b', 'utilShelf', 5.6, 4.6, 'e', { it: IT('Seat spares', 'Hinges, springs and a box of gold seat numbers.') });
    REC_STANDS.forEach(([c0, c1], b) => place('T', 'recHit', (c0 + c1) / 2 - 4, 1, 'n', { w: c1 - c0, d: 2, hitH: 1.3, it: IT('Stands', ['Three stepped benches at the stern end, by the scoreboard.', 'The middle of the stands: three stepped benches, right on the net. The best seats for a close game.', 'Three stepped benches at the bow end, by the gate onto the court.'][b]) }));
  },
};
// 0.84.0 (rec engineer B): a work:works place at each machine's panel, facing it (panelPlace finds them; schedules and placesOf skip them)
DECKS[7].places.push(...REC_MACHINES.map(m => ({ id: m.id + '-svc', machine: m.id, type: 'work:works', at: m.panel.slice(), face: m.panel[0] === m.at[0] && m.panel[1] === m.at[1] ? REC_FACE_BACK[m.face] : m.panel[0] > m.at[0] ? 'w' : m.panel[0] < m.at[0] ? 'e' : m.panel[1] > m.at[1] ? 'n' : 's', pose: 'work', room: m.room })));
// the rec deck's gather venues (RA, 0.83.2): their spots are REC_CREW_PLACES' 'event' places with `gather` (section 4d's
// loop that makes other decks' spots has run before this deck is defined, so these are written out)
DECKS[7].gathers = { 'river-banks': { name: 'the river hall', focus: [9.0, 3.0], rooms: 'K=', seats: [], also: [], lead: [] } };
// the rec deck's materials, made when the deck is built (so they are freed with it)
let RK = null;
function recMats() {
  RK = {
    seat: std('#4a2f86', .8), seatDark: std('#22192f', .7, .2), gold: std('#d9b45a', .35, .7), rake: std('#2b2140', .9),
    stageTop: M.wood, stageSide: std('#1d1630', .7), truss: std('#c9a24a', .4, .7), black: std('#16181c', .6, .3), wood: std('#6b4a32', .6), screen: std('#e8e6df', .9),
    standStep: std('#3a404a', .85), bench: std('#c9783a', .6),
    rim: std('#d8e6e4', .45), coping: std('#f2f0ea', .4), poolSide: std('#6fc3c9', .4), mosaic: new THREE.MeshStandardMaterial({ map: recMosaic(), roughness: .4 }),
    poolWater: recWater('#1f8fa6', '#4fd0dc', { alpha: 1 }), poolOwn: recWater('#1f8fa6', '#4fd0dc', { alpha: 1 }), ropeOrange: std('#ff8a3a', .5), ropeWhite: std('#f4f4f0', .5),
    rock: std('#6f8a7c', .9), rockDark: std('#4f6559', .9), riverBed: std('#6fc3c9', .4), fern: std('#3f8a4a', .8),
    riverFast: recWater('#1f8fa6', '#4fd0dc', { foam: .9, flow: 1.4, alpha: 1 }),   // 0.82.5 (the user's: still two looks): one water, opaque so the bed under it can't tint it; the fast run adds only its foam
      // 0.80.9: the pool's water (the user's: they didn't match)
    steel: std('#8a959c', .4, .6), gateLight: new THREE.MeshBasicMaterial({ color: col('#50e6ff'), toneMapped: false }), dock: std('#a0703f', .7), dockDark: std('#5a3d22', .8),
    kayak: ['#e0412f', '#f2c230', '#2f6fe0', '#3fbf5a'].map(c => std(c, .45, .1)), paddle: std('#2a2f36', .5, .3),
    wallOchre: std('#c08a3e', .95), wallRust: std('#9a4a28', .95), hold: std('#ffffff', .6), holdC: ['#ff4f6d', '#ffd23f', '#3fa9ff', '#5ee06a'].map(col),
    belay: std('#30363d', .5, .4), rope: std('#ff8a3a', .7), brass: std('#d9a441', .3, .8),
    loungerFrame: std('#e8e8e2', .4, .3), padA: std('#e3907f', .95), padB: std('#d77f73', .95),
    orb: new THREE.MeshBasicMaterial({ color: col('#ffd0e4'), toneMapped: false }),
    flagA: std('#ff6f61', .7, 0, { side: THREE.DoubleSide }), flagB: std('#ffd23f', .7, 0, { side: THREE.DoubleSide }), flagC: std('#50e6ff', .7, 0, { side: THREE.DoubleSide }), flagD: std('#ff4fd8', .7, 0, { side: THREE.DoubleSide }), loungerPad: std('#2f9fb0', .8), aidWhite: std('#f2f2ee', .5), aidRed: std('#d8322e', .5),
    lineOrange: new THREE.MeshBasicMaterial({ color: col('#ff9a3c'), toneMapped: false }), lineCyan: new THREE.MeshBasicMaterial({ color: col('#50e6ff'), toneMapped: false }),
    lineWhite: new THREE.MeshBasicMaterial({ color: col('#e8eef0'), toneMapped: false }),
    net: new THREE.MeshBasicMaterial({ color: col('#bfe6ff'), transparent: true, opacity: .2, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide, toneMapped: false }),
    field: new THREE.MeshBasicMaterial({ color: col('#50e6ff'), transparent: true, opacity: .05, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide, toneMapped: false }),
  };
  PULSES.push({ m: RK.net, key: 'opacity', base: .14, amp: .16, w: 3.1, ph: 0 }, { m: RK.field, key: 'opacity', base: .03, amp: .04, w: 1.3, ph: 1 });   // the net shimmers, the side fields breathe
}

