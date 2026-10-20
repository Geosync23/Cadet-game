// =====================================================================
// DECK 2: COMMAND & SCIENCE (step 6e: turn 1 the shell, turn 2 the bedrooms, turn 3 the Captain's quarters and the senior corridor,
// turn 4 science, the Watch office and the sensor array;
// Pillar 2: 0.32.2 the utility rooms)
// From plans/deck2-plan.html (Sketch 8), on Deck 3's outline with rounder stern corners. The deck splits at the lift:
// the senior quarters aft, round a looped carpeted corridor (fifteen locked bedrooms, the Captain's across the stern),
// science forward, off a four-wide corridor that ends at the sensor array behind glass in the nose.
// =====================================================================
// ---- Deck 2 kit (made at load, no R()) ----
const D2 = {
  brass: std('#c9a24a', .35, .75), navy: std('#1d2740', .6, .1),
};
Object.assign(WALL_KIT, {
  // a brass nameplate on the header above a bedroom door: gold letters on navy, in a brass frame
  brassPlate(g, o) {
    if (o.sub) {                                         // 0.32.3: an officer's plate, name over rank (answer 27)
      const t = tex(256, 80, (c, w, h) => {
        c.fillStyle = '#1d2740'; c.fillRect(0, 0, w, h); c.strokeStyle = '#d9b45a'; c.lineWidth = 3; c.strokeRect(5, 5, w - 10, h - 10);
        c.fillStyle = '#ecd08a'; c.textAlign = 'center';
        let f = 26; do c.font = '600 ' + f + 'px Georgia,serif'; while (c.measureText(o.text).width > w - 26 && --f > 14);
        c.fillText(o.text, w / 2, 38); c.font = 'italic 17px Georgia,serif'; c.fillStyle = '#d9b45a'; c.fillText(o.sub, w / 2, 63);
      });
      const p = new THREE.Mesh(new THREE.PlaneGeometry(.56, .175), new THREE.MeshBasicMaterial({ map: t, toneMapped: false }));
      p.position.set(0, 2.5, .04); g.add(p); box(.62, .235, .035, D2.brass, 0, 2.5, .0175, g); return;
    }
    const t = tex(256, 64, (c, w, h) => {
      c.fillStyle = '#1d2740'; c.fillRect(0, 0, w, h); c.strokeStyle = '#d9b45a'; c.lineWidth = 3; c.strokeRect(5, 5, w - 10, h - 10);
      c.fillStyle = '#ecd08a'; c.font = '600 27px Georgia,serif'; c.textAlign = 'center'; c.fillText(o.text, w / 2, 42);
    });
    const p = new THREE.Mesh(new THREE.PlaneGeometry(.56, .14), new THREE.MeshBasicMaterial({ map: t, toneMapped: false }));
    p.position.set(0, 2.5, .04); g.add(p); box(.62, .2, .035, D2.brass, 0, 2.5, .0175, g);
  },
});
// a bedroom's plate (0.32.3, answer 27): name over rank from the roster (read at dress time, so section 9 is in). The crew
// designer's `plate: { rank, name }` (0.16.6) wins where a roster entry has one; before that, the rank and name are worked out
// here. Rooms with nobody's plate (the visitors' rooms) keep the plate's own text.
const D2_RANK = { captain: 'Captain', xo: 'Executive Officer', chief: 'Department Chief', senior: 'Senior Officer' };
function d2Plate(room, text) {
  const all = typeof ROSTER !== 'undefined' ? ROSTER.concat(typeof ROSTER_GUESTS !== 'undefined' ? ROSTER_GUESTS : []) : [];
  const p = all.find(q => q.bed === '2-' + room);
  if (p && p.plate && p.plate.name) return { text: p.plate.name, sub: p.plate.rank };
  return p && D2_RANK[p.rank] ? { text: p.name.replace(/^(Captain|Commander|Chief) /, ''), sub: D2_RANK[p.rank] } : { text };
}
// bedrooms (0.9.2): shared materials only, so fifteen furnished rooms merge into a handful of draw calls
Object.assign(D2, {
  woodDark: std('#3e2a1f', .6), linen: std('#efe9dc', .9), duvet: std('#e4e7ea', .9), leather: std('#5a3324', .55),
  fabs: { navy: std('#2c3a5e', .9), sage: std('#6f8a6a', .9), wine: std('#6b2f3a', .9), teal: std('#2f6f73', .9), sand: std('#b9a27a', .9), slate: std('#4a5568', .9) },
  shade: std('#f1e4c8', .8, 0, { emissive: col('#ffcf8a'), emissiveIntensity: .55 }),
  books: ['#7a2f2f', '#2c4a6e', '#c9a24a', '#3f6b4f', '#e3dccb', '#5a3f6e'].map(c => std(c, .8)),
  paper: std('#f1ece0', .9), towel: std('#f6f4ee', .95), china: std('#dfe8ec', .3), screenPanel: std('#efe2c6', .85),
  model: std('#cfd6da', .4, .5), cord: std('#c8463c', .7),
  frost: std('#dcebf0', .15, 0, { transparent: true, opacity: .5, depthWrite: false }), tray: std('#e8ebe8', .35),
  rugs: [['#2c375e', '#c9a24a', '#e9dfc7', '#6b2f3a'], ['#3b4a3f', '#c9a24a', '#ece4d4', '#2f6f73'], ['#5a2f3a', '#d9b45a', '#efe3c8', '#2c3a5e']]
    .map(c => new THREE.MeshStandardMaterial({ map: makeRug(c), roughness: 1 })),
});
Object.assign(KIT, {
  // a double bed with an upholstered headboard, a nightstand and lamp either side
  suiteBed(g, o = {}) {
    const f = o.fab || D2.fabs.navy, b = o.wide ? 1.8 : 1.5, n = b / 2 + .25;       // o.wide: the Captain's
    box(b, .3, 2.1, D2.woodDark, 0, .15, .05, g); box(b - .08, .18, 2.0, D2.linen, 0, .39, .05, g);
    box(b - .02, .08, 1.45, D2.duvet, 0, .51, .37, g); box(b + .02, .05, .42, f, 0, .56, .82, g);
    for (const x of [-b / 4 - .01, b / 4 + .01]) soft(D2.linen, x, .56, -.72, .3, .08, .15, g);
    box(b + .2, 1.05, .12, f, 0, .72, -1.04, g); box(b + .24, .05, .14, M.wood, 0, 1.27, -1.04, g);
    for (const x of [-n, n]) {
      box(.44, .48, .4, M.wood, x, .24, -.86, g); box(.4, .02, .02, D2.brass, x, .36, -.65, g);
      cyl(.04, .06, .26, D2.brass, x, .61, -.9, g, 10); cyl(.09, .12, .14, D2.shade, x, .8, -.9, g, 16);
    }
    if (o.swans) for (const x of [-.25, .25]) { soft(D2.towel, x, .62, .45, .14, .07, .1, g); box(.04, .18, .04, D2.towel, x, .72, .37, g).rotation.x = -.3; }
    return { w: 2 * n + .44, d: 2.2 };
  },
  // a low futon for the Envoy: no headboard, a quilt in her own colours
  futon(g, o = {}) {
    box(1.5, .14, 2.1, M.wood, 0, .07, 0, g); box(1.4, .14, 2.0, D2.linen, 0, .21, 0, g);
    box(1.44, .05, 1.3, o.fab || D2.fabs.teal, 0, .3, .32, g); soft(D2.linen, 0, .32, -.75, .4, .07, .15, g);
    return { w: 1.5, d: 2.1 };
  },
  // a writing desk: terminal, brass lamp, and whatever its owner leaves on it
  suiteDesk(g, o = {}) {
    box(1.2, .05, .55, M.wood, 0, .75, 0, g);
    box(.4, .72, .5, D2.woodDark, .38, .36, 0, g); box(.04, .72, .5, D2.woodDark, -.56, .36, 0, g);
    const mon = new THREE.Mesh(new THREE.BoxGeometry(.5, .32, .03), [M.dark, M.dark, M.dark, M.dark, screenMat, M.dark]);
    mon.position.set(-.15, 1.0, -.18); g.add(mon); box(.04, .16, .04, M.slateDark, -.15, .84, -.2, g);
    cyl(.05, .06, .02, D2.brass, .42, .785, -.12, g, 12); cyl(.012, .012, .3, D2.brass, .42, .93, -.12, g, 6); cyl(.07, .1, .1, D2.shade, .42, 1.1, -.12, g, 14);
    if (o.papers) [[-.3, .04, .3], [.05, .1, -.4], [.2, -.05, .7], [-.05, .12, -.1]].forEach(([x, z, r], k) => { const p = box(.24, .012 + k * .006, .32, D2.paper, x, .785 + k * .012, z, g); p.rotation.y = r; });
    if (o.model) { box(.26, .06, .08, D2.model, .1, .85, .1, g); for (const z of [.04, .16]) box(.1, .04, .04, D2.model, .02, .85, z, g); }
    if (o.kettle) { cyl(.07, .08, .16, D2.brass, -.45, .86, .1, g, 12); cyl(.04, .035, .08, D2.china, -.3, .82, .14, g, 10); }
    return { w: 1.2, d: .55 };
  },
  // the en-suite: a frosted glass shower and basin in a brass frame, lighter to look over than a wash pod
  ensuite(g) {
    box(1.0, .06, 1.0, D2.tray, 0, .03, 0, g);
    box(.96, 1.9, .03, D2.frost, 0, 1.0, -.47, g); box(.03, 1.9, .96, D2.frost, -.47, 1.0, 0, g); box(.03, 1.9, .96, D2.frost, .47, 1.0, 0, g); box(.96, 1.9, .03, D2.frost, 0, 1.0, .47, g);
    for (const [x, z] of [[-.49, -.49], [.49, -.49], [-.49, .49], [.49, .49]]) box(.04, 1.98, .04, D2.brass, x, .99, z, g);
    for (const z of [-.49, .49]) box(1.02, .04, .04, D2.brass, 0, 1.98, z, g);
    for (const x of [-.49, .49]) box(.04, .04, 1.02, D2.brass, x, 1.98, 0, g);
    cyl(.02, .02, .5, D2.brass, -.3, 1.6, -.4, g, 6); cyl(.08, .06, .03, D2.brass, -.3, 1.85, -.32, g, 12);
    box(.42, .1, .3, D2.tray, .2, .82, -.3, g); cyl(.012, .012, .7, D2.brass, .2, .47, -.38, g, 6); box(.36, .3, .02, KM.mirror, .2, 1.3, -.445, g);
    box(.24, .04, .16, D2.towel, -.25, .9, .3, g);
    // a compact toilet against the +x glass, facing -x (0.32.6: the toilet places had nothing to sit on); seat top .42
    box(.13, .34, .36, D2.china, .39, .57, .2, g); cyl(.16, .12, .36, D2.china, .22, .2, .2, g, 14); box(.34, .03, .34, D2.china, .23, .405, .2, g);
    return { w: 1.0, d: 1.0, tall: true };
  },
  // a wardrobe in wood, with brass pulls
  suiteWardrobe(g) {
    box(.9, 1.9, .55, D2.woodDark, 0, .95, 0, g);
    for (const sx of [-.215, .215]) { box(.41, 1.78, .03, M.wood, sx, .95, .29, g); box(.02, .2, .03, D2.brass, sx - Math.sign(sx) * .16, 1.0, .31, g); }
    box(.94, .05, .59, M.wood, 0, 1.92, 0, g);
    return { w: .9, d: .55, tall: true };
  },
  suiteChair(g) {
    box(.5, .08, .48, D2.leather, 0, .46, 0, g); box(.5, .55, .08, D2.leather, 0, .8, -.22, g).rotation.x = .1;
    cyl(.03, .03, .38, D2.brass, 0, .23, 0, g, 8); box(.46, .03, .05, M.slateDark, 0, .03, 0, g); box(.05, .03, .46, M.slateDark, 0, .03, 0, g);
    return { w: .5, d: .5, noBlock: true };
  },
  // a low bookcase; the books come from a fixed pattern, not R(), so they never shift a texture
  suiteShelf(g, o = {}) {
    box(1.0, 1.15, .32, M.wood, 0, .575, 0, g); box(.92, 1.05, .02, D2.woodDark, 0, .58, -.14, g);
    for (let s = 0; s < 3; s++) {
      box(.92, .025, .28, D2.woodDark, 0, .06 + s * .36, .01, g);
      let x = -.44;
      for (let k = 0; x < .4; k++) { const bw = .04 + (k * 37 + s * 11) % 5 * .012, bh = .2 + (k * 23 + s * 7) % 4 * .025; box(bw, bh, .2, D2.books[(k + s * 2) % 6], x + bw / 2, .075 + s * .36 + bh / 2, .02, g); x += bw + .008; if ((k + s) % 7 === 5) x += .1; }
    }
    if (o.trophy) { box(.16, .04, .1, D2.woodDark, .25, 1.17, 0, g); cyl(.05, .03, .14, D2.brass, .25, 1.26, 0, g, 10); }
    return { w: 1.0, d: .32 };
  },
  suitePlant(g) {
    cyl(.2, .15, .38, M.ceramic, 0, .19, 0, g); cyl(.205, .2, .05, D2.brass, 0, .3, 0, g);
    for (let i = 0; i < 9; i++) { const a = i / 9 * Math.PI * 2, l = soft(i % 2 ? M.leaf : M.leaf2, Math.sin(a) * .14, .55, Math.cos(a) * .14, .05, .26, .1, g); l.rotation.set(Math.cos(a) * .7, 0, -Math.sin(a) * .7); }
    return { w: .4, d: .4 };
  },
  suiteRug(g, o) {
    const r = new THREE.Mesh(new THREE.BoxGeometry(o.w, .025, o.d), [M.slateDark, M.slateDark, D2.rugs[o.k || 0], M.slateDark, M.slateDark, M.slateDark]);
    r.position.y = .0125; r.userData.noShadow = true; g.add(r);
    return { w: o.w, d: o.d, noBlock: true };
  },
  // the Envoy's low tea table, a Veyli tea set on it, cushions round it
  lowTable(g) {
    cyl(.45, .45, .05, M.wood, 0, .3, 0, g, 28); cyl(.32, .36, .26, D2.woodDark, 0, .14, 0, g, 20);
    soft(D2.china, 0, .41, 0, .1, .08, .1, g); cyl(.012, .012, .1, D2.china, .1, .42, 0, g, 6).rotation.z = -.9;
    for (let k = 0; k < 4; k++) { const a = k * Math.PI / 2 + .4; cyl(.035, .03, .05, D2.china, Math.sin(a) * .25, .35, Math.cos(a) * .25, g, 10); }
    return { w: .9, d: .9 };
  },
  cushion(g, o = {}) { soft(o.fab || D2.fabs.teal, 0, .1, 0, .3, .1, .3, g); return { w: .6, d: .6, noBlock: true }; },
  // a folding screen: three panels in a zigzag
  sleepScreen(g) {
    for (let k = -1; k <= 1; k++) {
      const p = new THREE.Group(); p.position.set(k * .56, 0, k ? .1 : 0); p.rotation.y = k * .35; g.add(p);
      box(.58, 1.7, .04, D2.screenPanel, 0, .9, 0, p); box(.6, .05, .06, M.wood, 0, 1.77, 0, p); for (const x of [-.29, .29]) box(.04, 1.75, .05, M.wood, x, .88, 0, p);
    }
    return { w: 1.8, d: .4, tall: true };
  },
});
// furnish a bedroom from its door. Bedroom doors are 'closed', so roomFrame can't find them: the door is named here.
// Layouts are drawn with the door in the left half of the door wall, and mirrored when it's in the right half.
function d2Frame(rk, doorKey) {
  const b = ROOM_BOX[rk], Wr = b.i1 - b.i0 + 1, Dr = b.j1 - b.j0 + 1, [k, a, c] = doorKey.split(','), i = +a, j = +c;
  const side = k === 'h' ? (j === b.j0 ? 'n' : 's') : (i === b.i0 ? 'w' : 'e'), at = k === 'h' ? i - b.i0 + .5 : j - b.j0 + .5, ns = side === 'n' || side === 's';
  return {
    U: ns ? Wr : Dr, V: ns ? Dr : Wr,
    toL: { s: (u, v) => [u, Dr - v], n: (u, v) => [Wr - u, v], w: (u, v) => [v, u], e: (u, v) => [Wr - v, Dr - u] }[side],
    wall: { s: { back: 'n', left: 'w', right: 'e', front: 's' }, n: { back: 's', left: 'e', right: 'w', front: 'n' },
            w: { back: 'e', left: 'n', right: 's', front: 'w' }, e: { back: 'w', left: 's', right: 'n', front: 'e' } }[side],
    doorU: { s: at, n: Wr - at, w: at, e: Dr - at }[side],
  };
}
function d2Suite(rk, doorKey, o = {}) {
  NO_FADE.add(rk);
  const F = d2Frame(rk, doorKey), U = F.U, V = F.V, flip = F.doorU > U / 2, dU = flip ? U - F.doorU : F.doorU, P = [];
  const bed = { kind: 'suiteBed', u: U / 2, v: V - 1.2, o: { fab: o.fab, swans: o.swans, it: o.bed } };
  const desk = (u, v, back, chairU) => P.push({ kind: 'suiteDesk', u, v, back, o: { papers: o.papers, model: o.model, kettle: o.kettle, it: o.desk } },
    { kind: 'suiteChair', u: chairU, v, back: back === 'left' ? 'right' : 'left' });
  if (o.inner) {                                       // 4 x 4, no windows: bed to the back, wash pod and wardrobe by the door
    bed.u = U - 1.5; P.push(bed);
    P.push({ kind: 'ensuite', u: U - .6, v: .6, back: 'right' }, { kind: 'suiteWardrobe', u: .375, v: .65, back: 'left' });
    if (o.armchairs) P.push({ kind: 'armchair', u: .53, v: 2.3, back: 'left', o: { fab: o.fab } });
    else desk(.375, 2.5, 'left', .95);
    P.push({ kind: 'suiteRug', u: 1.9, v: 1.25, o: { w: 1.4, d: .9, k: o.rug } });
  } else if (U <= 3) {                                 // 3 x 5 by the lift: wardrobe by the door, wash pod and desk either side
    P.push(bed, { kind: 'suiteWardrobe', u: U - .375, v: .65, back: 'right' }, { kind: 'ensuite', u: .6, v: 1.95, back: 'left' });
    desk(U - .375, 2.05, 'right', U - .95);
    P.push({ kind: 'suiteRug', u: 1.5, v: 1.35, o: { w: 1.0, d: 1.5, k: o.rug } });
  } else {                                             // 4 x 5 on the hull: bed under the windows, desk on the far wall
    P.push(bed, { kind: 'ensuite', u: U - .6, v: .6, back: 'right' });
    desk(U - .375, 2.05, 'right', U - 1.0);
    if (dU >= 1.4) P.push({ kind: 'suiteWardrobe', u: .375, v: .65, back: 'left' }, { kind: 'armchair', u: .53, v: 2.15, back: 'left', o: { fab: o.fab } });
    else P.push({ kind: 'suiteWardrobe', u: 1.6, v: .375, back: 'front' }, { kind: 'armchair', u: .53, v: 2.2, back: 'left', o: { fab: o.fab } });   // v 2.2 keeps the way in from the door open
    P.push({ kind: 'suiteShelf', u: .26, v: 3.85, back: 'left', o: { trophy: o.trophy } }, { kind: 'suitePlant', u: U - .4, v: V - .4 });
    P.push({ kind: 'suiteRug', u: U / 2 + .1, v: 1.55, o: { w: 1.9, d: 1.3, k: o.rug } });
  }
  for (const p of P) {
    const u = flip ? U - p.u : p.u, back = flip && (p.back === 'left' || p.back === 'right') ? (p.back === 'left' ? 'right' : 'left') : (p.back || 'back');
    const [lx, lz] = F.toL(u, p.v); place(rk, p.kind, lx, lz, F.wall[back], p.o || {});
  }
}
// the Captain's quarters and the senior corridor (0.9.3)
Object.assign(D2, {
  candle: std('#fff3d6', .6, 0, { emissive: col('#ffd9a0'), emissiveIntensity: .8 }), wine: std('#5a1a24', .2, 0, { transparent: true, opacity: .85 }),
  globe: std('#3f6e8c', .5), land: std('#c9b27a', .7), inlay: std('#2f4a3e', .6),
  // the Wren's past captains, painted at load (no R()): a dark ground, a lit face, a uniform collar
  portraits: [['#2b2233', '#c99b7a', '#2c3a5e', '#c9a24a'], ['#1f2b2a', '#e0b896', '#6b2f3a', '#c9a24a'], ['#2e2a22', '#8f6a50', '#2f6f73', '#d9d2c2']].map(([bg, skin, coat, trim]) =>
    new THREE.MeshStandardMaterial({ roughness: .7, map: tex(160, 200, (c, w, h) => {
      const gr = c.createRadialGradient(80, 70, 10, 80, 90, 120); gr.addColorStop(0, '#5a4a3a'); gr.addColorStop(1, bg); c.fillStyle = gr; c.fillRect(0, 0, w, h);
      c.fillStyle = coat; c.beginPath(); c.moveTo(20, h); c.quadraticCurveTo(30, 128, 80, 122); c.quadraticCurveTo(130, 128, 140, h); c.fill();
      c.fillStyle = trim; c.fillRect(60, 150, 40, 5); c.fillRect(102, 160, 14, 10);
      c.fillStyle = skin; c.fillRect(70, 104, 20, 22); c.beginPath(); c.ellipse(80, 82, 24, 30, 0, 0, Math.PI * 2); c.fill();
      c.fillStyle = 'rgba(0,0,0,.25)'; c.beginPath(); c.ellipse(88, 86, 12, 26, 0, 0, Math.PI * 2); c.fill();
    }) })),
});
Object.assign(KIT, {
  // the Captain's dining table: seats eight, with candles, a runner and places laid; o.light hangs the deck's lamp over it
  diningTable(g, o = {}) {
    box(1.1, .06, 3.0, M.wood, 0, .76, 0, g); box(.28, .06, 2.6, D2.fabs.wine, 0, .795, 0, g);
    for (const z of [-.95, .95]) { box(.18, .7, .18, D2.woodDark, 0, .38, z, g); box(.7, .05, .5, D2.woodDark, 0, .025, z, g); }
    for (const z of [-.6, 0, .6]) { cyl(.04, .05, .04, D2.brass, 0, .84, z, g, 10); cyl(.02, .02, .18, D2.candle, 0, .95, z, g, 8); }
    const seat = (x, z, r) => {
      const c = new THREE.Group(); c.position.set(x, 0, z); c.rotation.y = r; g.add(c);
      box(.46, .06, .44, D2.fabs.wine, 0, .47, 0, c); box(.46, .6, .06, D2.woodDark, 0, .8, -.22, c);
      for (const [sx, sz] of [[-.2, -.18], [.2, -.18], [-.2, .18], [.2, .18]]) box(.04, .45, .04, D2.woodDark, sx, .22, sz, c);
      cyl(.11, .11, .01, D2.china, x * .6, .797, Math.abs(z) > 1.5 ? z * .75 : z, g, 16);
    };
    for (const z of [-1.0, 0, 1.0]) { seat(-.82, z, Math.PI / 2); seat(.82, z, -Math.PI / 2); }
    seat(0, -1.78, 0); seat(0, 1.78, Math.PI);
    if (o.light) addLamp(g, 0, 2.0, 0, 6, .35, 1.7);
    return { w: 1.9, d: 4.0 };
  },
  sideboard(g) {
    box(1.6, .82, .48, D2.woodDark, 0, .41, 0, g); box(1.66, .04, .52, M.wood, 0, .84, 0, g);
    for (const x of [-.4, .4]) box(.7, .6, .02, M.wood, x, .42, .245, g);
    for (const x of [-.1, .1]) box(.02, .14, .02, D2.brass, x, .45, .26, g);
    cyl(.07, .09, .26, D2.wine, -.45, .99, 0, g, 12); cyl(.025, .025, .08, D2.wine, -.45, 1.15, 0, g, 8);
    for (const x of [-.22, -.12]) cyl(.035, .025, .1, D2.china, x, .91, .08, g, 10);
    box(.22, .28, .03, D2.brass, .45, 1.0, -.1, g).rotation.x = -.15;
    return { w: 1.6, d: .52 };
  },
  // the Captain's desk: a partner desk with a leather top, a terminal and a brass lamp
  captainDesk(g) {
    box(1.8, .06, .85, M.wood, 0, .76, 0, g); box(1.5, .005, .6, D2.inlay, 0, .792, 0, g);
    for (const x of [-.62, .62]) { box(.48, .72, .78, D2.woodDark, x, .36, 0, g); for (const y of [.2, .45, .66]) box(.04, .03, .02, D2.brass, x, y, .4, g); }
    const mon = new THREE.Mesh(new THREE.BoxGeometry(.56, .34, .03), [M.dark, M.dark, M.dark, M.dark, screenMat, M.dark]);
    mon.position.set(-.35, 1.02, -.25); g.add(mon); box(.04, .16, .04, M.slateDark, -.35, .86, -.27, g);
    cyl(.05, .06, .02, D2.brass, .6, .8, -.2, g, 12); cyl(.012, .012, .32, D2.brass, .6, .96, -.2, g, 6); cyl(.08, .11, .11, D2.shade, .6, 1.15, -.2, g, 14);
    [[.15, .1, .4], [.3, .05, -.2]].forEach(([x, z, r], k) => box(.24, .012 + k * .01, .32, D2.paper, x, .8 + k * .012, z, g).rotation.y = r);
    return { w: 1.8, d: .85 };
  },
  // a drawn curtain on a brass rail: closes off the sleeping alcove
  alcoveCurtain(g, o = {}) {
    const w = o.w || 2.6, n = Math.round(w / .2);
    box(w + .1, .04, .04, D2.brass, 0, 2.3, 0, g);
    for (let k = 0; k < n; k++) box(w / n + .01, 2.2, .05, o.fab || D2.fabs.wine, -w / 2 + (k + .5) * w / n, 1.18, k % 2 ? .035 : -.035, g);
    return { w, d: .15 };
  },
  globe(g) {
    cyl(.18, .22, .04, D2.woodDark, 0, .02, 0, g, 16); cyl(.03, .03, .7, D2.woodDark, 0, .37, 0, g, 8);
    const s = soft(D2.globe, 0, .92, 0, .22, .22, .22, g); s.rotation.z = .4;
    soft(D2.land, .08, .98, .1, .1, .08, .1, g); soft(D2.land, -.1, .86, -.06, .09, .1, .08, g);
    const ring = new THREE.Mesh(new THREE.TorusGeometry(.25, .012, 6, 28), D2.brass); ring.position.y = .92; ring.rotation.set(0, Math.PI / 2, .4); g.add(ring);
    return { w: .5, d: .5 };
  },
  // a narrow console against a corridor wall, with flowers
  consoleTable(g, o = {}) {
    box(.9, .04, .3, M.wood, 0, .82, 0, g); box(.86, .1, .26, D2.woodDark, 0, .75, 0, g);
    for (const x of [-.4, .4]) for (const z of [-.1, .1]) cyl(.015, .012, .7, D2.brass, x, .35, z, g, 6);
    cyl(.07, .05, .22, D2.china, -.15, .95, 0, g, 12);
    for (let k = 0; k < 5; k++) { const a = k * 1.256; soft(GD.flowers[(k + (o.k || 0)) % 5], -.15 + Math.sin(a) * .07, 1.12 + k % 2 * .04, Math.cos(a) * .07, .05, .05, .05, g); }
    for (const a of [.6, 2.4, 4.2]) soft(M.leaf, -.15 + Math.sin(a) * .05, 1.07, Math.cos(a) * .05, .03, .08, .02, g).rotation.z = Math.sin(a) * .6;
    box(.2, .03, .14, D2.paper, .22, .855, 0, g).rotation.y = .2;
    return { w: .9, d: .3 };
  },
});
Object.assign(WALL_KIT, {
  // a portrait of one of the Wren's past captains, in a gilt frame
  portrait(g, o = {}) {
    box(.62, .76, .04, D2.brass, 0, 1.55, .02, g);
    const p = new THREE.Mesh(new THREE.PlaneGeometry(.52, .66), D2.portraits[o.k || 0]); p.position.set(0, 1.55, .045); g.add(p);
  },
  // a brass wall lamp with a warm shade
  brassSconce(g) {
    box(.12, .26, .03, D2.brass, 0, 1.85, .015, g); cyl(.012, .012, .12, D2.brass, 0, 1.8, .08, g, 6).rotation.x = Math.PI / 2;
    cyl(.07, .1, .14, D2.shade, 0, 1.9, .14, g, 14);
    glow('#ffcf8a', .7, 0, 1.92, .16, g, .5);
  },
  // the brass knocker on the Captain's door (nobody uses it)
  knocker(g) {
    const r = new THREE.Mesh(new THREE.TorusGeometry(.07, .014, 8, 20), D2.brass); r.position.set(0, 1.32, -.04); g.add(r);
    box(.08, .06, .02, D2.brass, 0, 1.42, -.05, g);
  },
});
// science, the Watch office and the sensor array (0.9.4)
Object.assign(D2, {
  labWhite: std('#e6eae8', .45), labTop: std('#2b3238', .4, .1), steel: std('#aab4b8', .3, .7), probe: std('#e9ecea', .35, .2),
  dish: std('#dfe4e6', .45, .15, { side: THREE.DoubleSide }), headset: std('#1d2226', .5), blueThing: std('#6fb8ff', .2, 0, { emissive: col('#3f8cff'), emissiveIntensity: 1.1 }),
  // the chart room's table top: a glowing star chart, drawn at load from a fixed hash (no R())
  chart: new THREE.MeshBasicMaterial({ toneMapped: false, map: tex(512, 352, (c, w, h) => {
    c.fillStyle = '#0c1a2a'; c.fillRect(0, 0, w, h);
    c.strokeStyle = 'rgba(120,200,255,.18)'; c.lineWidth = 1; for (let x = 0; x < w; x += 32) { c.beginPath(); c.moveTo(x, 0); c.lineTo(x, h); c.stroke(); } for (let y = 0; y < h; y += 32) { c.beginPath(); c.moveTo(0, y); c.lineTo(w, y); c.stroke(); }
    for (let k = 0; k < 140; k++) { const x = (k * 197) % w, y = (k * 83 + (k * k) % 61) % h; c.fillStyle = k % 9 ? 'rgba(220,240,255,.75)' : '#ffd98a'; c.fillRect(x, y, k % 5 ? 2 : 3, k % 5 ? 2 : 3); }
    c.strokeStyle = '#e8c06a'; c.lineWidth = 2; c.setLineDash([6, 5]); c.beginPath(); c.moveTo(40, 300); c.bezierCurveTo(150, 240, 260, 260, 330, 160); c.bezierCurveTo(380, 90, 440, 80, 480, 40); c.stroke(); c.setLineDash([]);
    for (const [x, y, r] of [[40, 300, 8], [200, 252, 7], [330, 160, 7], [480, 40, 9]]) { c.strokeStyle = '#5fd6c6'; c.beginPath(); c.arc(x, y, r, 0, Math.PI * 2); c.stroke(); }
    c.fillStyle = '#a9d4f0'; c.font = '600 16px system-ui,sans-serif'; c.fillText('FRONTIER SURVEY, SECTOR 7', 16, 24);
  }) }),
  // a paper star chart for the walls
  paperChart: new THREE.MeshStandardMaterial({ roughness: .9, map: tex(160, 200, (c, w, h) => {
    c.fillStyle = '#e9e0c8'; c.fillRect(0, 0, w, h); c.strokeStyle = '#8a6a45'; c.lineWidth = 3; c.strokeRect(6, 6, w - 12, h - 12);
    c.strokeStyle = 'rgba(60,60,80,.5)'; c.lineWidth = 1; c.beginPath(); c.arc(80, 100, 60, 0, Math.PI * 2); c.stroke(); c.beginPath(); c.arc(80, 100, 35, 0, Math.PI * 2); c.stroke();
    for (let k = 0; k < 40; k++) { c.fillStyle = '#2c3a5e'; c.fillRect(20 + (k * 53) % 120, 40 + (k * 31) % 120, 2, 2); }
    c.strokeStyle = '#6b2f3a'; c.beginPath(); c.moveTo(40, 70); c.lineTo(70, 90); c.lineTo(110, 80); c.lineTo(125, 130); c.stroke();
  }) }),
  // the signal board's waveforms and the racks' status lights
  wave: new THREE.MeshBasicMaterial({ toneMapped: false, map: tex(512, 96, (c, w, h) => {
    c.fillStyle = '#081418'; c.fillRect(0, 0, w, h);
    for (const [y, col_, f] of [[24, '#5fd6c6', .07], [52, '#e8c06a', .11], [78, '#7fb8ff', .05]]) { c.strokeStyle = col_; c.lineWidth = 2; c.beginPath(); for (let x = 0; x < w; x += 2) c.lineTo(x, y + Math.sin(x * f) * 8 * Math.sin(x * .013)); c.stroke(); }
  }) }),
  rack: new THREE.MeshBasicMaterial({ toneMapped: false, map: tex(64, 192, (c, w, h) => {
    c.fillStyle = '#1b2228'; c.fillRect(0, 0, w, h);
    for (let y = 8; y < h; y += 16) { c.fillStyle = '#2b343b'; c.fillRect(4, y, w - 8, 12); for (let k = 0; k < 5; k++) { c.fillStyle = ['#5fd6c6', '#7dffb0', '#e8c06a', '#5fd6c6', '#7fb8ff'][(y / 16 + k) % 5]; c.fillRect(8 + k * 10, y + 4, 4, 4); } }
  }) }),
});
Object.assign(KIT, {
  chartTable(g) {
    box(2.6, .78, 1.8, D2.woodDark, 0, .39, 0, g); box(2.72, .06, 1.92, M.wood, 0, .81, 0, g);
    const t = new THREE.Mesh(new THREE.PlaneGeometry(2.4, 1.64), D2.chart); t.rotation.x = -Math.PI / 2; t.position.y = .845; t.userData.noShadow = true; g.add(t);
    glow('#7fc8ff', 2.4, 0, 1.0, 0, g, .18);
    return { w: 2.72, d: 1.92 };
  },
  // pigeonholes of rolled charts
  chartRack(g, o = {}) {
    const w = o.w || 2.0, cols = Math.round(w / .33);
    box(w, 2.0, .4, D2.woodDark, 0, 1.0, -.02, g);
    for (let r = 0; r < 6; r++) for (let q = 0; q < cols; q++) {
      const x = -w / 2 + (q + .5) * w / cols, y = .2 + r * .3, n = (r * 7 + q * 3) % 4;
      box(w / cols - .03, .26, .02, M.wood, x, y + .02, .18, g);
      for (let k = 0; k < n; k++) cyl(.035, .035, .42, k % 2 ? D2.paper : D2.screenPanel, x - .07 + k * .06, y - .02 + (k % 2) * .05, .05, g, 8).rotation.x = Math.PI / 2;
    }
    return { w, d: .44, tall: true };
  },
  // a lab bench: white cabinets, a dark resin top, glassware, and (o.scope) a microscope
  labBench(g, o = {}) {
    const w = o.w || 2.2;
    box(w, .86, .66, D2.labWhite, 0, .43, 0, g); box(w + .04, .05, .7, D2.labTop, 0, .885, 0, g);
    for (let x = -w / 2 + .3; x < w / 2 - .2; x += .55) box(.02, .7, .01, D2.labTop, x + .27, .43, .335, g);
    for (let k = 0; k < 5; k++) cyl(.025, .025, .14, LNG.bottles[k], -w / 2 + .3 + k * .07, .98, -.18, g, 8);
    box(.4, .03, .1, D2.steel, -w / 2 + .44, .925, -.18, g);
    if (o.scope !== false) { box(.18, .04, .22, D2.labTop, w / 2 - .45, .93, 0, g); box(.05, .34, .05, D2.labTop, w / 2 - .45, 1.1, -.08, g); cyl(.03, .03, .18, D2.steel, w / 2 - .45, 1.2, .0, g, 8).rotation.x = .5; }
    if (o.centrifuge) { cyl(.18, .2, .2, D2.labWhite, .1, 1.0, 0, g, 18); cyl(.16, .16, .02, D2.steel, .1, 1.11, 0, g, 18); }
    return { w, d: .7 };
  },
  // a double-sided island with a reagent shelf over it
  labIsland(g, o = {}) {
    const w = o.w || 3.4;
    box(w, .86, 1.2, D2.labWhite, 0, .43, 0, g); box(w + .04, .05, 1.26, D2.labTop, 0, .885, 0, g);
    for (const x of [-w / 2 + .1, w / 2 - .1]) box(.05, .9, .05, D2.steel, x, 1.36, 0, g);
    box(w - .1, .03, .3, D2.steel, 0, 1.8, 0, g);
    for (let k = 0; k < 9; k++) cyl(.04, .04, .16, LNG.bottles[k % 6], -w / 2 + .4 + k * (w - .8) / 8, 1.9, 0, g, 8);
    for (const z of [-.3, .3]) { box(.36, .02, .26, D2.paper, -.6, .915, z, g); cyl(.05, .04, .12, LNG.bottles[2], .5, .97, z, g, 10); }
    if (o.centrifuge) { cyl(.18, .2, .2, D2.labWhite, 1.0, 1.0, .25, g, 18); cyl(.16, .16, .02, D2.steel, 1.0, 1.11, .25, g, 18); }
    return { w, d: 1.26 };
  },
  // the sample scanner: a cabinet with a glowing chamber
  sampleScanner(g) {
    box(.9, 1.5, .8, D2.labWhite, 0, .75, 0, g); box(.6, .5, .02, D2.labTop, 0, 1.0, .41, g);
    box(.52, .42, .02, MED.screen, 0, 1.0, .42, g); box(.3, .18, .03, WM.screen, .2, 1.4, .41, g);
    glow('#4fd8c4', .9, 0, 1.0, .5, g, .3);
    return { w: .9, d: .8, tall: true };
  },
  // a glass-fronted shelf of odd things from the frontier, one of them blue and glowing
  specimenShelf(g) {
    box(1.2, 1.8, .45, D2.woodDark, 0, .9, 0, g); box(1.1, 1.7, .02, D2.labTop, 0, .9, -.2, g);
    for (let s = 0; s < 4; s++) {
      box(1.1, .02, .4, D2.steel, 0, .15 + s * .42, 0, g);
      for (let k = 0; k < 4; k++) { const m = s === 2 && k === 1 ? D2.blueThing : LNG.bottles[(s + k) % 6]; cyl(.07, .07, .2 + (k % 2) * .06, m, -.4 + k * .27, .27 + s * .42 + (k % 2) * .03, 0, g, 12); }
    }
    box(1.14, 1.74, .02, D2.frost, 0, .9, .225, g);
    return { w: 1.2, d: .45, tall: true };
  },
  // the observatory's telescope on a brass pier, aimed out of the bow windows
  brassTelescope(g) {
    cyl(.32, .4, .12, D2.woodDark, 0, .06, 0, g, 20); cyl(.12, .16, 1.0, D2.brass, 0, .6, 0, g, 16);
    const h = new THREE.Group(); h.position.set(0, 1.15, 0); h.rotation.x = -.6; g.add(h);
    cyl(.12, .14, 1.7, D2.fabs.navy, 0, 0, .1, h, 18).rotation.x = Math.PI / 2;
    for (const z of [-.6, .9]) cyl(.15, .15, .06, D2.brass, 0, 0, z, h, 18).rotation.x = Math.PI / 2;
    cyl(.04, .03, .2, D2.brass, 0, .14, -.5, h, 8);
    return { w: .9, d: .9 };
  },
  // a comms desk for two: screens, headsets, a microphone
  commsDesk(g) {
    box(2.0, .05, .7, M.wood, 0, .75, 0, g); for (const x of [-.95, .95]) box(.06, .73, .62, M.slate, x, .365, 0, g);
    for (const x of [-.5, .5]) {
      const mon = new THREE.Mesh(new THREE.BoxGeometry(.6, .36, .03), [M.dark, M.dark, M.dark, M.dark, screenMat, M.dark]); mon.position.set(x, 1.05, -.22); g.add(mon);
      box(.04, .18, .04, M.slateDark, x, .87, -.24, g);
      const hs = new THREE.Mesh(new THREE.TorusGeometry(.09, .015, 6, 16, Math.PI), D2.headset); hs.position.set(x + .3, .79, .12); hs.rotation.x = -Math.PI / 2; g.add(hs);
      for (const sx of [-.09, .09]) cyl(.04, .04, .03, D2.fabs.teal, x + .3 + sx, .79, .12, g, 10);
    }
    cyl(.05, .06, .02, M.slateDark, 0, .785, .05, g, 10); cyl(.008, .008, .2, D2.steel, 0, .88, .05, g, 6);
    return { w: 2.0, d: .7 };
  },
  // the signal board along the comms room's windows
  signalBoard(g, o = {}) {
    const w = o.w || 4.6;
    box(w, .8, .6, M.slate, 0, .4, 0, g); box(w + .04, .05, .64, M.slateDark, 0, .825, 0, g);
    const sc = new THREE.Mesh(new THREE.PlaneGeometry(w - .3, .34), D2.wave); sc.position.set(0, 1.08, -.26); g.add(sc);
    box(w - .2, .44, .04, M.slateDark, 0, 1.08, -.3, g);
    for (let k = 0; k < Math.floor(w / .3); k++) box(.06, .03, .06, k % 3 ? WM.navGreen : WM.screenAmber, -w / 2 + .2 + k * .3, .86, .15, g);
    return { w, d: .64 };
  },
  // a fume hood: a cabinet with a glass sash and a duct to the deckhead
  fumeHood(g) {
    box(1.2, .86, .75, D2.labWhite, 0, .43, 0, g); box(1.24, .05, .79, D2.labTop, 0, .885, 0, g);
    box(1.2, 1.0, .04, D2.labWhite, 0, 1.41, -.355, g); for (const x of [-.58, .58]) box(.04, 1.0, .75, D2.labWhite, x, 1.41, 0, g);
    box(1.2, .3, .75, D2.labWhite, 0, 2.06, 0, g); box(1.1, .05, .02, WM.lightStrip, 0, 1.88, .3, g);
    box(1.12, .6, .02, D2.frost, 0, 1.4, .36, g); box(1.12, .04, .04, D2.steel, 0, 1.1, .37, g);
    box(.3, .55, .3, D2.steel, 0, 2.48, -.1, g);
    for (let k = 0; k < 3; k++) cyl(.03, .03, .16, LNG.bottles[k + 1], -.3 + k * .2, .99, -.1, g, 8);
    return { w: 1.24, d: .79, tall: true };
  },
  gloveBox(g) {
    box(1.2, .86, .7, D2.steel, 0, .43, 0, g); box(1.1, .6, .6, D2.steel, 0, 1.18, -.04, g);
    box(1.0, .46, .02, D2.frost, 0, 1.2, .265, g);
    for (const x of [-.25, .25]) { const r = new THREE.Mesh(new THREE.TorusGeometry(.09, .025, 8, 18), D2.headset); r.position.set(x, 1.12, .27); g.add(r); }
    return { w: 1.2, d: .7 };
  },
  // a survey probe in its cradle
  probeCradle(g, o = {}) {
    for (const z of [-.7, .7]) { box(.7, .4, .12, WM.paintDark, 0, .2, z, g); box(.5, .06, .16, WM.paintGold, 0, .42, z, g); }
    const p = cyl(.26, .26, 1.6, D2.probe, 0, .62, 0, g, 18); p.rotation.x = Math.PI / 2;
    const n = new THREE.Mesh(new THREE.ConeGeometry(.26, .5, 18), D2.probe); n.rotation.x = Math.PI / 2; n.position.set(0, .62, 1.05); n.castShadow = true; g.add(n);
    for (const z of [-.5, .3]) cyl(.27, .27, .06, D2.brass, 0, .62, z, g, 18).rotation.x = Math.PI / 2;
    for (let k = 0; k < 4; k++) { const a = k * Math.PI / 2; box(.04, .3, .3, WM.paintDark, Math.sin(a) * .3, .62 + Math.cos(a) * .3, -.75, g).rotation.z = -a; }
    return { w: 1.0, d: 2.2 };
  },
  // a launch tube's breech, against the hull
  launchTube(g) {
    box(.9, 1.2, .3, WM.paintDark, 0, .6, -.05, g);
    const r = new THREE.Mesh(new THREE.TorusGeometry(.32, .06, 10, 24), WM.paintGold); r.position.set(0, .7, .12); g.add(r);
    cyl(.3, .3, .04, M.dark, 0, .7, .1, g, 24).rotation.x = Math.PI / 2;
    box(.12, .1, .04, WM.navGreen, .32, 1.15, .12, g);
    return { w: .9, d: .4 };
  },
  // signal processors: a row of racks with status lights
  signalRacks(g, o = {}) {
    const n = o.n || 3;
    for (let k = 0; k < n; k++) {
      const x = (k - (n - 1) / 2) * .72;
      box(.7, 2.0, .6, M.slateDark, x, 1.0, 0, g);
      const f = new THREE.Mesh(new THREE.PlaneGeometry(.56, 1.7), D2.rack); f.position.set(x, 1.0, .305); g.add(f);
    }
    return { w: n * .72, d: .6, tall: true };
  },
  // the comms mast's base: a heavy column through the deckhead, with cable trays
  mastBase(g) {
    cyl(.8, .9, .3, WM.paintDark, 0, .15, 0, g, 24); cyl(.45, .5, H, D2.steel, 0, H / 2, 0, g, 20);
    for (const y of [.8, 1.6, 2.4]) cyl(.52, .52, .08, WM.paintGold, 0, y, 0, g, 20);
    for (const a of [0, 2.1, 4.2]) box(.12, H - .4, .1, M.slateDark, Math.sin(a) * .56, H / 2 + .1, Math.cos(a) * .56, g);
    return { w: 1.8, d: 1.8, tall: true };
  },
  // the main sensor dish: a pedestal and a turntable carrying the dish, turning slowly (SPINS); its feed glows and
  // breathes (PULSES). o.light hangs the deck's second lamp over it, blue.
  sensorDish(g, o = {}) {
    cyl(.9, 1.1, .4, WM.paintDark, 0, .2, 0, g, 28); cyl(.45, .6, .7, D2.steel, 0, .75, 0, g, 20);
    const ring = new THREE.Mesh(new THREE.TorusGeometry(.95, .05, 8, 40), WM.paintGold); ring.rotation.x = Math.PI / 2; ring.position.y = .41; g.add(ring);
    const tt = new THREE.Group(); tt.position.y = 1.1; g.add(tt);
    cyl(.6, .6, .12, D2.steel, 0, 0, 0, tt, 24);
    for (const x of [-.55, .55]) box(.1, .9, .3, WM.paintDark, x, .45, 0, tt);
    const dish = new THREE.Group(); dish.position.y = .8; dish.rotation.x = -.85; tt.add(dish);
    const pts = []; for (let k = 0; k <= 12; k++) { const r = k / 12 * 1.5; pts.push(new THREE.Vector2(r, r * r * .22)); }
    const bowl = new THREE.Mesh(new THREE.LatheGeometry(pts, 36), D2.dish); bowl.rotation.x = Math.PI / 2; bowl.position.z = -.1; dish.add(bowl);
    cyl(.3, .4, .25, WM.paintDark, 0, 0, -.25, dish, 16).rotation.x = Math.PI / 2;
    for (let k = 0; k < 3; k++) { const a = k * Math.PI * 2 / 3, s = box(.04, .04, 1.25, D2.steel, Math.sin(a) * .5, Math.cos(a) * .5, .6, dish); s.rotation.set(-Math.cos(a) * .38, Math.sin(a) * .38, 0); }
    const feedM = std('#bfe3ff', .3, 0, { emissive: col('#4f9cff'), emissiveIntensity: 1 });
    cyl(.12, .08, .3, feedM, 0, 0, 1.2, dish, 14).rotation.x = Math.PI / 2;
    mergeMeshes(tt); noMergeAll(tt);
    const s = glow('#6fb0ff', 1.4, 0, 2.4, .6, g, .3);
    SPINS.push({ o: tt, ax: 'y', w: .12 });
    PULSES.push({ m: feedM, key: 'emissiveIntensity', base: .5, amp: 1.0, w: .9, ph: 0 }, { m: s.material, key: 'opacity', base: .12, amp: .3, w: .9, ph: 0 });
    if (o.light) { addLamp(g, 0, 2.6, 0, 7, .6, 1.5); LAMPS[LAMPS.length - 1].l.color.copy(col('#8fb8ff')); }
    return { w: 2.4, d: 2.4, tall: true };
  },
  // the sample that hums when nobody's looking: a sealed jar whose glow breathes
  humJar(g) {
    box(.5, .7, .5, D2.steel, 0, .35, 0, g);
    const m = std('#b9ffd8', .2, 0, { emissive: col('#4fe09a'), emissiveIntensity: 1, transparent: true, opacity: .85 });
    cyl(.16, .16, .36, m, 0, .9, 0, g, 16); cyl(.18, .18, .05, D2.steel, 0, 1.1, 0, g, 16);
    const s = glow('#7dffb0', .8, 0, .9, 0, g, .3);
    PULSES.push({ m, key: 'emissiveIntensity', base: .4, amp: .9, w: 2.3, ph: 0 }, { m: s.material, key: 'opacity', base: .1, amp: .3, w: 2.3, ph: 0 });
    return { w: .5, d: .5 };
  },
});
Object.assign(WALL_KIT, {
  starChart(g) {
    box(.7, .86, .04, D2.woodDark, 0, 1.5, .02, g);
    const p = new THREE.Mesh(new THREE.PlaneGeometry(.6, .76), D2.paperChart); p.position.set(0, 1.5, .045); g.add(p);
  },
});
// the utility rooms (0.32.2): the lab gas plant, the utility closet and the cable crawl. Shared materials, no R().
Object.assign(D2, {
  bottles: ['#3f7a5a', '#8a97a0', '#3a5f8a', '#c86b4a'].map(c => std(c, .4, .3)),
  gauge: new THREE.MeshBasicMaterial({ toneMapped: false, map: tex(64, 64, (c, w, h) => {
    c.fillStyle = '#e9e6dc'; c.beginPath(); c.arc(32, 32, 30, 0, Math.PI * 2); c.fill();
    c.strokeStyle = '#2b343b'; c.lineWidth = 3; c.stroke();
    c.strokeStyle = '#c8463c'; c.lineWidth = 6; c.beginPath(); c.arc(32, 32, 22, -.4, .5); c.stroke();
    c.strokeStyle = '#1d2226'; c.lineWidth = 3; c.beginPath(); c.moveTo(32, 32); c.lineTo(14, 22); c.stroke();
  }) }),
  pipe: std('#9aa6ad', .35, .6), conduit: std('#5c6870', .5, .4), led: std('#7dffb0', .3, 0, { emissive: col('#3ad07a'), emissiveIntensity: 1 }),
  amber: std('#ffc970', .3, 0, { emissive: col('#f0a640'), emissiveIntensity: .9 }),
  cables: ['#2b343b', '#c8463c', '#e9c46a', '#3a5f8a'].map(c => std(c, .7)),
});
Object.assign(KIT, {
  // a rack of four gas bottles, chained to a steel frame
  gasRack(g) {
    box(.9, .05, .45, D2.steel, 0, .025, 0, g); for (const x of [-.43, .43]) box(.04, 1.4, .04, D2.steel, x, .7, -.18, g);
    for (const y of [.6, 1.15]) box(.9, .03, .03, D2.steel, 0, y, -.18, g);
    for (let k = 0; k < 4; k++) { const x = -.31 + k * .21; cyl(.09, .09, 1.2, D2.bottles[k], x, .65, 0, g, 14); soft(D2.bottles[k], x, 1.25, 0, .09, .06, .09, g); cyl(.03, .03, .1, D2.steel, x, 1.33, 0, g, 8); }
    return { w: .9, d: .45, tall: true };
  },
  // the regulator manifold: a board of gauges and valves, with the lab lines leaving through the deck
  gasManifold(g) {
    box(.9, 1.5, .08, D2.labTop, 0, .95, -.18, g);
    for (let k = 0; k < 3; k++) { const x = -.28 + k * .28; const d = new THREE.Mesh(new THREE.CircleGeometry(.08, 20), D2.gauge); d.position.set(x, 1.45, -.135); g.add(d); cyl(.09, .09, .03, D2.steel, x, 1.45, -.15, g, 20).rotation.x = Math.PI / 2;
      box(.06, .5, .06, D2.pipe, x, 1.05, -.1, g); const v = new THREE.Mesh(new THREE.TorusGeometry(.06, .015, 6, 14), WM.paintGold); v.position.set(x, .95, -.05); g.add(v); }
    box(.82, .06, .06, D2.pipe, 0, .78, -.1, g);
    for (const x of [-.3, 0, .3]) box(.05, .78, .05, D2.pipe, x, .39, -.1, g);
    box(.3, .14, .02, WM.screen, .25, 1.75, -.13, g);
    return { w: .9, d: .4 };
  },
  // the extractor fan for the labs' fume hoods: a housing with a round grille and its duct up to the deckhead
  extractor(g) {
    box(.9, 1.2, .55, D2.labWhite, 0, .6, 0, g);
    cyl(.34, .34, .04, D2.steel, 0, .65, .28, g, 24).rotation.x = Math.PI / 2;
    for (let k = 0; k < 5; k++) box(.6 - Math.abs(k - 2) * .12, .02, .02, D2.labTop, 0, .5 + k * .075, .31, g);
    box(.4, H - 1.2, .4, D2.steel, 0, (H + 1.2) / 2, -.05, g);
    box(.12, .06, .02, D2.led, .32, 1.1, .28, g);
    return { w: .9, d: .55, tall: true };
  },
  // the deck's breaker cabinet: rows of breakers behind a door left open, a hazard band at the foot
  powerCabinet(g) {
    box(.9, 2.0, .5, M.slateDark, 0, 1.0, 0, g); box(.92, .12, .52, WM.hazard, 0, .06, 0, g);
    for (let r = 0; r < 6; r++) for (let q = 0; q < 6; q++) box(.1, .14, .03, r === 2 && q === 4 ? D2.amber : M.slate, -.3 + q * .12, .55 + r * .22, .26, g);
    for (let r = 0; r < 6; r++) box(.03, .03, .02, D2.led, .38, .6 + r * .22, .27, g);
    const door = box(.44, 1.8, .03, M.slate, -.62, 1.0, .1, g); door.rotation.y = -1.1;
    return { w: .9, d: .5, tall: true };
  },
  // the light relay rack: rows of relays with a lamp each, ticking over at dusk and dawn
  lightRelayRack(g) {
    box(.8, 1.8, .5, M.slateDark, 0, .9, 0, g);
    for (let r = 0; r < 8; r++) { box(.66, .14, .04, M.slate, 0, .3 + r * .19, .26, g); for (let q = 0; q < 4; q++) box(.04, .04, .02, (r + q) % 5 ? D2.led : D2.amber, -.24 + q * .16, .3 + r * .19, .29, g); }
    return { w: .8, d: .5, tall: true };
  },
  // a bundle of conduits from deck to deckhead
  conduits(g) {
    for (let k = 0; k < 4; k++) cyl(.05, .05, H, D2.conduit, -.18 + k * .12, H / 2, 0, g, 10);
    for (const y of [.5, 1.4, 2.3]) box(.56, .05, .14, D2.steel, 0, y, 0, g);
    return { w: .6, d: .2 };
  },
  // cable trays along a wall at knee and shoulder height, the array's cables in them: the crawl's low ceiling
  crawlCableTray(g, o = {}) {
    const w = o.w || 2;
    for (const y of [.45, 1.35]) {
      box(w, .03, .32, D2.steel, 0, y, 0, g); box(w, .1, .02, D2.steel, 0, y + .05, .16, g);
      for (let k = 0; k < 4; k++) { const c = cyl(.035, .035, w, D2.cables[k], 0, y + .05, -.11 + k * .07, g, 8); c.rotation.z = Math.PI / 2; }
    }
    box(w, .04, .04, D2.steel, 0, 1.7, .1, g);
    return { w, d: .34, noBlock: true };
  },
  // the signal repeater: a finned box that lifts the array's signal for the long run aft
  signalRepeater(g) {
    box(.7, .8, .5, M.slate, 0, .4, 0, g);
    for (let k = 0; k < 7; k++) box(.02, .6, .12, D2.steel, -.3 + k * .1, .45, -.28, g);
    box(.4, .1, .02, WM.screen, 0, .65, .26, g); for (let k = 0; k < 3; k++) box(.04, .04, .02, D2.led, -.12 + k * .12, .5, .26, g);
    return { w: .7, d: .5 };
  },
  // the array feed junction: where the dish's cables come through the bulkhead and split
  arrayFeed(g) {
    box(.7, 1.0, .4, M.slateDark, 0, .7, 0, g); box(.74, .06, .44, WM.paintGold, 0, 1.22, 0, g);
    for (let k = 0; k < 4; k++) { cyl(.04, .04, .1, D2.steel, -.24 + k * .16, 1.3, 0, g, 8); cyl(.03, .03, .2, D2.cables[k], -.24 + k * .16, .16, .1, g, 8); }
    box(.3, .1, .02, D2.amber, 0, .85, .21, g);
    return { w: .7, d: .4 };
  },
  // lived-in touches in the utility rooms (0.32.3, answer 31): a mug someone left, signs, the closet calendar
  d2Mug(g, o = {}) {
    const x = o.x || 0, y = o.y || 0, z = o.z || 0, m = o.m || D2.china;
    cyl(.04, .035, .09, m, x, y + .045, z, g, 10); box(.015, .05, .03, m, x + .048, y + .05, z, g); cyl(.034, .034, .005, D2.coffee, x, y + .088, z, g, 10);
    return { w: .12, d: .12, noBlock: true };
  },
});
// made at load from fixed text, no R(): each is one shared material
const d2Paper = (w, h, draw) => new THREE.MeshBasicMaterial({ map: tex(w, h, draw), toneMapped: false });
const d2SignMat = (text, bg, fg) => d2Paper(256, 96, (c, w, h) => {
  c.fillStyle = bg; c.fillRect(0, 0, w, h); c.strokeStyle = fg; c.lineWidth = 6; c.strokeRect(8, 8, w - 16, h - 16);
  c.fillStyle = fg; c.textAlign = 'center'; let f = 30; do c.font = '700 ' + f + 'px Arial,sans-serif'; while (c.measureText(text).width > w - 36 && --f > 12); c.fillText(text, w / 2, 48 + f * .36);
});
Object.assign(D2, {
  coffee: std('#3b2416', .3), mugRed: std('#b8433a', .5),
  flames: d2SignMat('NO NAKED FLAMES', '#f4f1ea', '#c0392b'), head: d2SignMat('MIND YOUR HEAD', '#f2c94c', '#1b1b1f'),
  calendar: d2Paper(128, 160, (c, w, h) => {
    c.fillStyle = '#f6f3ec'; c.fillRect(0, 0, w, h); c.fillStyle = '#2f6f73'; c.fillRect(0, 0, w, 52);
    c.fillStyle = '#f6f3ec'; c.font = '700 18px Arial,sans-serif'; c.textAlign = 'center'; c.fillText('THE WREN', w / 2, 22);
    c.font = '13px Arial,sans-serif'; c.fillText('Concord Survey', w / 2, 42);
    c.strokeStyle = '#9aa3a8'; c.lineWidth = 1;
    for (let r = 0; r < 5; r++) for (let q = 0; q < 7; q++) {
      const x = 8 + q * 16, y = 60 + r * 19; c.strokeRect(x, y, 16, 19);
      if (r * 7 + q < 16) { c.strokeStyle = '#c0392b'; c.beginPath(); c.moveTo(x + 3, y + 3); c.lineTo(x + 13, y + 16); c.stroke(); c.strokeStyle = '#9aa3a8'; }
    }
    c.fillStyle = '#c0392b'; c.beginPath(); c.arc(8 + 4 * 16 + 8, 60 + 3 * 19 + 9.5, 7, 0, 7); c.fill();
  }),
});
Object.assign(WALL_KIT, {
  d2Sign(g, o) { const p = new THREE.Mesh(new THREE.PlaneGeometry(.5, .19), o.m); p.position.set(0, o.y || 1.6, .02); g.add(p); },
  // the closet's corner: a calendar with the days crossed off, a steel shelf with someone's mug and a roll of tape
  d2Nook(g) {
    const p = new THREE.Mesh(new THREE.PlaneGeometry(.32, .4), D2.calendar); p.position.set(0, 1.62, .02); g.add(p);
    box(.5, .025, .18, D2.steel, 0, 1.12, .09, g); for (const x of [-.2, .2]) box(.02, .1, .14, D2.steel, x, 1.06, .08, g);
    KIT.d2Mug(g, { x: -.1, y: 1.1325, z: .09, m: D2.mugRed });
    cyl(.05, .05, .05, D2.cord, .14, 1.16, .09, g, 12).rotation.x = Math.PI / 2;
  },
});
DECKS[2] = {
  num: 2, name: 'Command & Science', seed: 20219,
  blurb: 'Senior quarters, Survey labs, Watch office', arrive: 'Senior quarters out of the stern door, so keep it down. Science out of the bow door.',
  lift: [20, 11],                                  // car rows 9-11, trunks row 8 above it, ladder row 12: the same world spot as every deck
  map: [
    '...XXXXXOOOOIIIIVVVSSSSWWWWKKKKKKLLLLLLggJJJJ.......',
    '..XXXXXXOOOOIIIIVVVSSSSWWWWKKKKKKLLLLLLggJJJJAA.....',
    '..XXXXXXOOOOIIIIVVVSSSSWWWWKKKKKKLLLLLLggJJJJAAA....',
    '..XXXXXXOOOOIIIIVVVSSSSWWWWKKKKKKLLLLLLggJJJJAAAA...',
    '..XXXXXXOOOOIIIIVVVSSSSWWWWKKKKKKLLLLLLggJJJJAAAAA..',
    '..CCCCC----------++++++WWWWKKKKKKLLLLLLggJJJJAAAAAA.',
    '..CCCCC----------++++++WWWWKKKKKKLLLLLLggJJJJAAAAAA.',
    '..CCCCC--NNNNGGGG++++++WWWWKKKKKKLLLLLLggJJJJAAAAAA.',
    '..CCCCC--NNNNGGGG++YY++WWWWKKKKKKLLLLLLggJJJJAAAAAAA',
    '..CCCCC--NNNNGGGG++@@++======================AAAAAAA',
    '..CCCCC--NNNNGGGG++@@++======================AAAAAAA',
    '..CCCCC--DDDDUUUU++@@++======================AAAAAAA',
    '..CCCCC--DDDDUUUU++ZZ++======================AAAAAAA',
    '..CCCCC--DDDDUUUU++++++wwQQQQQQFFFMMMMMMMPPPPAAAAAAA',
    '..CCCCC--DDDDUUUU++++++wwQQQQQQFFFMMMMMMMPPPPAAAAAA.',
    '..CCCCC----------++++++wwQQQQQQFFFMMMMMMMPPPPAAAAAA.',
    '..CCCCC----------++++++wwQQQQQQFFFMMMMMMMPPPPAAAAAA.',
    '..EEEEEETTTTBBBBHHHRRRRuuQQQQQQFFFMMMMMMMPPPPAAAAA..',
    '..EEEEEETTTTBBBBHHHRRRRuuQQQQQQFFFMMMMMMMPPPPAAAA...',
    '..EEEEEETTTTBBBBHHHRRRRuuQQQQQQFFFMMMMMMMPPPPAAA....',
    '..EEEEEETTTTBBBBHHHRRRRuuQQQQQQFFFMMMMMMMPPPPAA.....',
    '...EEEEETTTTBBBBHHHRRRRuuQQQQQQFFFnnnnnnnPPPP.......',
  ],
  // doors, in game edge keys. door: open to all. closed: shut, with tap text. hatch: service access.
  // glass: an inner window. lift: the main lift (one wide door each side).
  doors: {
    'v,19,9': 'lift', 'v,19,10': 'lift', 'v,19,11': 'lift', 'v,21,9': 'lift', 'v,21,10': 'lift', 'v,21,11': 'lift',   // stern door to the quarters, bow door to science
    'h,19,8': 'glass', 'h,20,8': 'glass', 'v,19,8': 'glass', 'v,21,8': 'glass',   // the trunks, behind glass above the car
    'h,19,13': 'hatch', 'h,20,13': 'glass',                   // the ladder, behind glass, with its hatch
    // the quarters: every bedroom has its own door onto the loop or the lobby
    'v,7,10': 'closed',                                       // the Captain's quarters, off the middle of the gallery
    'h,7,5': 'closed', 'h,9,5': 'closed', 'h,13,5': 'closed', 'h,17,5': 'closed', 'h,19,5': 'closed',      // port hull: Vance, Works Chief, Infirmary Chief, Dr. Sato, Second Officer
    'h,7,17': 'closed', 'h,9,17': 'closed', 'h,13,17': 'closed', 'h,17,17': 'closed', 'h,19,17': 'closed', // starboard hull: Envoy Saruth, Chief Holt, visitors' suite, Senior Helm Officer, Comms Chief
    'h,10,7': 'closed', 'h,14,7': 'closed',                   // inside the loop, facing port: Counsellor, Senior Watch Officer
    'h,10,15': 'closed', 'h,14,15': 'closed',                 // inside the loop, facing starboard: Deputy Survey Chief, visitors' cabin
    // the science side of the lobby
    'v,23,7': 'door', 'v,23,6': 'glass', 'v,23,8': 'glass',   // the Watch office, glass onto the science lobby (its plate is on v,23,5)
    'v,23,14': 'door',                                        // washroom
    'h,23,17': 'hatch',                                       // utility closet, through the washroom
    // science
    'h,29,9': 'door', 'h,28,9': 'glass', 'h,30,9': 'glass', 'h,31,9': 'glass',   // the chart room
    'h,35,9': 'door', 'h,34,9': 'glass', 'h,36,9': 'glass', 'h,37,9': 'glass',   // the Survey lab, glass onto the science corridor
    'v,39,4': 'hatch',                                        // the lab gas plant, from the Survey lab
    'h,43,9': 'door', 'h,42,9': 'glass', 'h,44,9': 'glass',   // the observatory
    'h,27,13': 'door', 'h,26,13': 'glass', 'h,28,13': 'glass', 'h,29,13': 'glass',   // the comms room
    'h,32,13': 'closed',                                      // the specimen store
    'h,36,13': 'door', 'h,35,13': 'glass', 'h,37,13': 'glass', 'h,38,13': 'glass',   // the sample lab
    'h,37,21': 'hatch',                                       // down into the cable crawl, from the sample lab
    'h,43,13': 'closed',                                      // the probe bay
    'v,45,10': 'glass', 'v,45,11': 'glass', 'v,45,12': 'glass', 'v,45,9': 'closed',   // the array: a window at the end of the corridor, and its shut door
  },
  // which room each shut door or hatch leads into (its tap text is that room's 'tap')
  sealed: {
    'v,7,10': 'C', 'h,7,5': 'X', 'h,9,5': 'O', 'h,13,5': 'I', 'h,17,5': 'V', 'h,19,5': 'S',
    'h,7,17': 'E', 'h,9,17': 'T', 'h,13,17': 'B', 'h,17,17': 'H', 'h,19,17': 'R',
    'h,10,7': 'N', 'h,14,7': 'G', 'h,10,15': 'D', 'h,14,15': 'U',
    'h,23,17': 'u', 'v,39,4': 'g', 'h,32,13': 'F', 'h,37,21': 'n', 'h,43,13': 'P', 'v,45,9': 'A',
  },
  service: ['h,23,17', 'v,39,4', 'h,37,21'],   // the utility rooms' hatches: the player and Works crew pass (0.32.2)
  // machines (0.32.2, plans/pillar2-plan.md "Machines and jobs"): each one's panel tile carries a work:works place.
  // Kinds are the registry's (MACHINE_KINDS); ids keep the old stand-ins' where it's the same machine.
  machines: [
    { id: '2-gasplant-1', kind: 'gasplant', at: [40, 3], room: 'g', face: 'w', panel: [39, 3] },
    { id: '2-extractor-1', kind: 'scrubber', at: [40, 7], room: 'g', face: 'w', panel: [39, 7] },
    { id: '2-breaker-1', kind: 'powerjunction', at: [24, 18], room: 'u', face: 'w', panel: [23, 18] },
    { id: '2-junction-1', kind: 'junction', at: [24, 20], room: 'u', face: 'w', panel: [23, 20] },
    { id: '2-repeater-1', kind: 'relay', at: [34, 21], room: 'n', face: 'e', panel: [35, 21] },
    { id: '2-feed-1', kind: 'relay', at: [40, 21], room: 'n', face: 'w', panel: [39, 21] },
    { id: '2-array-1', kind: 'array', at: [48, 11], room: 'A', face: 'w', panel: [46, 11] },
    { id: '2-racks-1', kind: 'relay', at: [47, 4], room: 'A', face: 's', panel: [47, 5] },
    { id: '2-racks-2', kind: 'relay', at: [47, 17], room: 'A', face: 'n', panel: [47, 16] },
  ],
  // bedrooms: a brass plate over each door [door, the corridor side, name]
  nameplates: [
    ['v,7,10', 'e', 'Capt. Marrow'], ['h,7,5', 's', 'Cdr. Vance'], ['h,9,5', 's', 'Works Chief'], ['h,13,5', 's', 'Infirmary Chief'], ['h,17,5', 's', 'Dr. Sato'], ['h,19,5', 's', 'Second Officer'],
    ['h,7,17', 'n', 'Envoy Saruth'], ['h,9,17', 'n', 'Chief Holt'], ['h,13,17', 'n', 'Visitors'], ['h,17,17', 'n', 'Senior Helm'], ['h,19,17', 'n', 'Comms Chief'],
    ['h,10,7', 'n', 'Counsellor'], ['h,14,7', 'n', 'Watch Officer'], ['h,10,15', 's', 'Survey Deputy'], ['h,14,15', 's', 'Visitors'],
  ],
  // science and the lobby: the usual plates beside the doors
  plates: [
    ['v,23,5', 'w', 'Watch office'], ['v,23,13', 'w', 'Washroom'],
    ['h,27,9', 's', 'Chart room'], ['h,33,9', 's', 'Survey lab'], ['h,41,9', 's', 'Observatory'],
    ['h,25,13', 'n', 'Comms'], ['h,31,13', 'n', 'Specimens'], ['h,34,13', 'n', 'Sample lab'], ['h,41,13', 'n', 'Probe bay'],
  ],
  rooms: {
    '-': { name: 'Senior corridor', floor: 'carpet', hall: true },
    '+': { name: 'Lift lobby', floor: 'lobby', hall: true },
    '=': { name: 'Science corridor', floor: 'corridor', hall: true },
    '@': { name: 'Main lift', floor: 'lift' },
    Y: { name: 'Spine trunks', floor: 'grate', spine: true }, Z: { name: 'Spine ladder', floor: 'grate', spine: true },
    W: { name: 'Watch office', floor: 'plate' },
    w: { name: 'Washroom', floor: 'tile' },
    K: { name: 'Chart room', floor: 'wood' },
    L: { name: 'Survey lab', floor: 'tile' },
    Q: { name: 'Comms room', floor: 'plate' },
    M: { name: 'Sample lab', floor: 'tile' },
    J: { name: 'Observatory', floor: 'wood' },
    // bedrooms: locked, and not yours
    C: { name: 'Captain\'s quarters', floor: 'wood', tap: 'Captain Marrow\'s quarters. There\'s a brass knocker nobody uses; the Captain prefers the comm.' },
    X: { name: 'Commander Vance\'s cabin', floor: 'wood', tap: 'Commander Vance\'s cabin. The nameplate is perfectly level. Someone checked.' },
    O: { name: 'Works Chief\'s cabin', floor: 'wood', tap: 'The Works Chief\'s cabin. Your boss lives here when not in the glass office on Deck 5. Knock only if something is on fire.' },
    I: { name: 'Infirmary Chief\'s cabin', floor: 'wood', tap: 'The Infirmary Chief\'s cabin. A sign on the door: IF YOU ARE BLEEDING, DECK 3.' },
    V: { name: 'Dr. Sato\'s cabin', floor: 'wood', tap: 'Dr. Sato\'s cabin. It smells faintly of her terrible tea.' },
    T: { name: 'Chief Holt\'s cabin', floor: 'wood', tap: 'Chief Holt\'s cabin, right next door to the Envoy. Holt asked for it.' },
    H: { name: 'Senior Helm Officer\'s cabin', floor: 'wood', tap: 'The Senior Helm Officer\'s cabin. A model of the Wren sits on the door\'s little shelf.' },
    S: { name: 'Second Officer\'s cabin', floor: 'wood', tap: 'The Second Officer\'s cabin. Third in command, and first to be woken.' },
    N: { name: 'Counsellor\'s cabin', floor: 'wood', tap: 'The Ship\'s Counsellor\'s cabin. A note on the door: OFFICE HOURS ON DECK 3. HERE, ONLY IF IT CAN\'T WAIT.' },
    R: { name: 'Comms Chief\'s cabin', floor: 'wood', tap: 'The Comms Chief\'s cabin. A headset hangs on the door handle, just in case.' },
    G: { name: 'Senior Watch Officer\'s cabin', floor: 'wood', tap: 'The Senior Watch Officer\'s cabin. Holt\'s deputy, and the only one who can make him laugh.' },
    D: { name: 'Deputy Survey Chief\'s cabin', floor: 'wood', tap: 'The Deputy Survey Chief\'s cabin. There\'s a star chart taped over the nameplate.' },
    // visitors: locked
    E: { name: 'Guest cabin', floor: 'wood', tap: 'Envoy Saruth\'s door. A knot of Veyli cord hangs from the handle: visitors by invitation only.' },
    B: { name: 'Visitors\' suite', floor: 'wood', tap: 'The visitors\' suite, made up and empty, for inspectors, visiting captains and anyone the Concord sends.' },
    U: { name: 'Visitors\' cabin', floor: 'wood', tap: 'A second visitors\' cabin, made up and empty. Fresh towels, folded into swans by someone with time on their hands.' },
    // locked, but seen through glass
    A: { name: 'Sensor array', floor: 'grate', tap: 'The ship\'s sensor and comms array, in the nose: the dish, the mast\'s base and the signal racks. Tier 3 access. You can watch it through the window beside this door.' },
    F: { name: 'Specimen store', floor: 'steel', tap: 'Frozen samples from the frontier, labelled in Dr. Sato\'s handwriting. Survey staff only.' },
    P: { name: 'Probe bay', floor: 'steel', tap: 'Survey probes in their cradles beside the launch tubes, charged and waiting. Survey staff only.' },
    // sealed until their tier
    // utility rooms (0.32.2): built, behind service hatches (`service`); their floors draw no random numbers (`still`)
    u: { name: 'Utility closet', floor: 'plate', still: true, tap: 'Deck 2\'s power junction and light relays. Tier 1 access, once the job list is running.' },
    g: { name: 'Lab gas plant', floor: 'grate', still: true, tap: 'Gas bottles in racks, regulators and the lines that feed both labs.' },
    n: { name: 'Cable crawl', floor: 'grate', still: true, tap: 'A low crawl along the starboard hull, carrying the array\'s cables aft.' },
  },
  windows: ['C', 'X', 'O', 'I', 'V', 'S', 'E', 'T', 'B', 'H', 'R', 'W', 'K', 'L', 'J', 'Q'].map(room => ({ room })),
  closedDoors: {
    'h,19,13': { t: 'Spine ladder', x: 'The maintenance ladder runs the whole height of the ship, beside the lift. Crawlways branch off it on every deck. Tier 2 access.' },
  },
  hull: { sternX: 2, stern: 3, bowFrom: 40, bowLen: 11.6, byFace: true },   // Deck 3's hull, with rounder stern corners; one hull piece per facing
  light: { sky: col('#e9e6ff'), sun: col('#fff0dc'), hemi: .94, sunI: .96 },   // calm: a touch cooler in the shade, a touch softer in the sun
  // places (0.19.1, 0.19.2, 0.32.1, 0.32.2): every spot where a crew member does something, for the schedules (plans/pillar1-plan.md, "Places").
  // anim (0.32.1, plans/pillar2-plan.md "Activities on places"): read, talk or drink. The chart room's and observatory's seats are common-room, for free time,
  // except two chart room window seats kept as lounge-seat for tea breaks. Service spots (work:works) name their machine.
  // Data only: nothing draws them. at is [column, row]; face is the way the person faces. Beds are '2-<room letter>'.
  // A bedroom's places are its resident's own: the room has a bed place, and only that bed's owner should be sent there.
  places: [
    // the Captain's quarters
    { id: '2-C', type: 'bed', at: [4, 6], face: 's', pose: 'lie', room: 'C' }, { id: '2-shower-15', type: 'shower', at: [6, 5], face: 's', pose: 'stand', room: 'C' },
    { id: '2-basin-15', type: 'basin', at: [6, 5], face: 's', pose: 'stand', room: 'C' }, { id: '2-toilet-15', type: 'toilet', at: [6, 5], face: 'w', pose: 'sit', room: 'C', xy: [6.64, 5.8], y: 0.42 },
    { id: '2-captable-1', type: 'lounge-seat', at: [5, 10], face: 'w', pose: 'sit', room: 'C', xy: [5.25, 10.5], y: 0.5, anim: 'talk', cush: 0.5 },
    { id: '2-captable-2', type: 'lounge-seat', at: [5, 11], face: 'w', pose: 'sit', room: 'C', xy: [5.25, 11.5], y: 0.5, anim: 'talk', cush: 0.5 },
    { id: '2-captable-3', type: 'lounge-seat', at: [3, 12], face: 'e', pose: 'sit', room: 'C', y: 0.5, anim: 'talk' },
    { id: '2-captable-4', type: 'lounge-seat', at: [5, 12], face: 'w', pose: 'sit', room: 'C', xy: [5.25, 12.5], y: 0.5, anim: 'talk', cush: 0.5 },
    { id: '2-captable-5', type: 'lounge-seat', at: [4, 9], face: 's', pose: 'sit', room: 'C', xy: [4.45, 9.5], y: 0.5, anim: 'talk', cush: 0.5 },
    { id: '2-captable-6', type: 'lounge-seat', at: [4, 13], face: 'n', pose: 'sit', room: 'C', xy: [4.42, 13.26], y: 0.5, anim: 'talk' },
    { id: '2-windowseat-1', type: 'lounge-seat', at: [2, 12], face: 'e', pose: 'sit', room: 'C', y: 0.52, anim: 'read', window: true },
    { id: '2-windowseat-2', type: 'lounge-seat', at: [2, 10], face: 'e', pose: 'sit', room: 'C', y: 0.52, anim: 'read', window: true },
    { id: '2-command-1', type: 'work:command', at: [4, 15], face: 'n', pose: 'sit', room: 'C', xy: [4.43, 15.37], y: 0.5, anim: 'read', cush: 0.5 },
    { id: '2-armchair-11', type: 'lounge-seat', at: [2, 15], face: 'e', pose: 'sit', room: 'C', xy: [2.54, 15.5], y: 0.44, anim: 'read', cush: 0.44 },
    // Vance
    { id: '2-X', type: 'bed', at: [6, 1], face: 's', pose: 'lie', room: 'X' }, { id: '2-armchair-9', type: 'lounge-seat', at: [3, 2], face: 'e', pose: 'sit', room: 'X', xy: [3.04, 2.63], y: 0.44, anim: 'read', cush: 0.44 },
    { id: '2-armchair-10', type: 'lounge-seat', at: [5, 2], face: 'w', pose: 'sit', room: 'X', xy: [5.25, 2.65], y: 0.44, anim: 'read', cush: 0.44 },
    { id: '2-desk-11', type: 'lounge-seat', at: [2, 4], face: 'w', pose: 'sit', room: 'X', xy: [2.8, 4.5], y: 0.5, anim: 'read' }, { id: '2-shower-13', type: 'shower', at: [6, 4], face: 'n', pose: 'stand', room: 'X' },
    { id: '2-basin-13', type: 'basin', at: [6, 4], face: 'n', pose: 'stand', room: 'X' }, { id: '2-toilet-13', type: 'toilet', at: [5, 4], face: 'e', pose: 'sit', room: 'X', xy: [5.96, 4.2], y: 0.42 },
    // Works Chief
    { id: '2-O', type: 'bed', at: [10, 1], face: 's', pose: 'lie', room: 'O' }, { id: '2-shower-1', type: 'shower', at: [11, 4], face: 'w', pose: 'stand', room: 'O' },
    { id: '2-basin-1', type: 'basin', at: [11, 4], face: 'w', pose: 'stand', room: 'O' }, { id: '2-toilet-1', type: 'toilet', at: [11, 4], face: 'n', pose: 'sit', room: 'O', xy: [11.2, 4.64], y: 0.42 },
    { id: '2-desk-1', type: 'lounge-seat', at: [11, 2], face: 'e', pose: 'sit', room: 'O', xy: [11.16, 2.79], y: 0.5, anim: 'read' },
    { id: '2-armchair-1', type: 'lounge-seat', at: [8, 2], face: 'e', pose: 'sit', room: 'O', xy: [8.42, 2.63], y: 0.44, anim: 'read', cush: 0.44 },
    // Infirmary Chief
    { id: '2-I', type: 'bed', at: [14, 1], face: 's', pose: 'lie', room: 'I' }, { id: '2-shower-2', type: 'shower', at: [15, 4], face: 'w', pose: 'stand', room: 'I' },
    { id: '2-basin-2', type: 'basin', at: [15, 4], face: 'w', pose: 'stand', room: 'I' }, { id: '2-toilet-2', type: 'toilet', at: [15, 4], face: 'n', pose: 'sit', room: 'I', xy: [15.2, 4.64], y: 0.42 },
    { id: '2-desk-2', type: 'lounge-seat', at: [15, 2], face: 'e', pose: 'sit', room: 'I', xy: [15.16, 2.79], y: 0.5, anim: 'read' },
    { id: '2-armchair-2', type: 'lounge-seat', at: [12, 2], face: 'e', pose: 'sit', room: 'I', xy: [12.42, 2.63], y: 0.44, anim: 'read', cush: 0.44 },
    // Dr. Sato
    { id: '2-V', type: 'bed', at: [17, 1], face: 's', pose: 'lie', room: 'V' }, { id: '2-shower-3', type: 'shower', at: [16, 3], face: 'e', pose: 'stand', room: 'V' },
    { id: '2-basin-3', type: 'basin', at: [16, 3], face: 'e', pose: 'stand', room: 'V' }, { id: '2-toilet-3', type: 'toilet', at: [16, 2], face: 's', pose: 'sit', room: 'V', xy: [16.8, 2.81], y: 0.42 },
    { id: '2-desk-3', type: 'lounge-seat', at: [18, 2], face: 'e', pose: 'sit', room: 'V', xy: [18.22, 2.78], y: 0.5, anim: 'read' },
    // Second Officer
    { id: '2-S', type: 'bed', at: [21, 1], face: 's', pose: 'lie', room: 'S' }, { id: '2-shower-4', type: 'shower', at: [22, 4], face: 'w', pose: 'stand', room: 'S' },
    { id: '2-basin-4', type: 'basin', at: [22, 4], face: 'w', pose: 'stand', room: 'S' }, { id: '2-toilet-4', type: 'toilet', at: [22, 4], face: 'n', pose: 'sit', room: 'S', xy: [22.2, 4.64], y: 0.42 },
    { id: '2-desk-4', type: 'lounge-seat', at: [22, 2], face: 'e', pose: 'sit', room: 'S', xy: [22.16, 2.79], y: 0.5, anim: 'read' },
    { id: '2-armchair-3', type: 'lounge-seat', at: [19, 2], face: 'e', pose: 'sit', room: 'S', xy: [19.43, 2.6], y: 0.44, anim: 'read', cush: 0.44 },
    // Envoy Saruth (visitor)
    { id: '2-E', type: 'bed', at: [6, 20], face: 'n', pose: 'lie', room: 'E' }, { id: '2-cushion-1', type: 'lounge-seat', at: [4, 19], face: 's', pose: 'sit', room: 'E', xy: [4.24, 19.65], y: 0.18, anim: 'drink', cush: 0.176 },
    { id: '2-cushion-2', type: 'lounge-seat', at: [4, 18], face: 's', pose: 'sit', room: 'E', xy: [4.3, 18.35], y: 0.18, anim: 'drink' },
    { id: '2-cushion-3', type: 'lounge-seat', at: [3, 18], face: 's', pose: 'sit', room: 'E', xy: [3.4, 18.5], y: 0.18, anim: 'drink' },
    { id: '2-cushion-4', type: 'lounge-seat', at: [3, 19], face: 's', pose: 'sit', room: 'E', xy: [3.35, 19.5], y: 0.19, anim: 'drink' }, { id: '2-shower-14', type: 'shower', at: [5, 17], face: 's', pose: 'stand', room: 'E' },
    { id: '2-basin-14', type: 'basin', at: [5, 17], face: 's', pose: 'stand', room: 'E' }, { id: '2-toilet-14', type: 'toilet', at: [6, 17], face: 'w', pose: 'sit', room: 'E', xy: [6.14, 17.8], y: 0.42 },
    // Holt
    { id: '2-T', type: 'bed', at: [10, 20], face: 'n', pose: 'lie', room: 'T' }, { id: '2-shower-5', type: 'shower', at: [11, 17], face: 'w', pose: 'stand', room: 'T' },
    { id: '2-basin-5', type: 'basin', at: [11, 17], face: 'w', pose: 'stand', room: 'T' }, { id: '2-toilet-5', type: 'toilet', at: [11, 17], face: 'n', pose: 'sit', room: 'T', xy: [11.2, 17.84], y: 0.42 },
    { id: '2-desk-5', type: 'lounge-seat', at: [11, 19], face: 'e', pose: 'sit', room: 'T', xy: [11.16, 19.21], y: 0.5, anim: 'read' },
    { id: '2-armchair-4', type: 'lounge-seat', at: [8, 19], face: 'e', pose: 'sit', room: 'T', xy: [8.43, 19.37], y: 0.44, anim: 'read', cush: 0.44 },
    // visitors' suite
    { id: '2-B', type: 'bed', at: [14, 20], face: 'n', pose: 'lie', room: 'B' }, { id: '2-shower-6', type: 'shower', at: [15, 17], face: 'w', pose: 'stand', room: 'B' },
    { id: '2-basin-6', type: 'basin', at: [15, 17], face: 'w', pose: 'stand', room: 'B' }, { id: '2-toilet-6', type: 'toilet', at: [15, 17], face: 'n', pose: 'sit', room: 'B', xy: [15.2, 17.84], y: 0.42 },
    { id: '2-desk-6', type: 'lounge-seat', at: [15, 19], face: 'e', pose: 'sit', room: 'B', xy: [15.16, 19.21], y: 0.5, anim: 'read' },
    { id: '2-armchair-5', type: 'lounge-seat', at: [12, 19], face: 'e', pose: 'sit', room: 'B', xy: [12.43, 19.37], y: 0.44, anim: 'read', cush: 0.44 },
    // Senior Helm
    { id: '2-H', type: 'bed', at: [17, 20], face: 'n', pose: 'lie', room: 'H' }, { id: '2-shower-7', type: 'shower', at: [18, 18], face: 'w', pose: 'stand', room: 'H' },
    { id: '2-basin-7', type: 'basin', at: [18, 18], face: 'w', pose: 'stand', room: 'H' }, { id: '2-toilet-7', type: 'toilet', at: [18, 19], face: 'n', pose: 'sit', room: 'H', xy: [18.2, 19.19], y: 0.42 },
    { id: '2-desk-7', type: 'lounge-seat', at: [16, 19], face: 'w', pose: 'sit', room: 'H', xy: [16.78, 19.22], y: 0.5, anim: 'read' },
    // Comms Chief
    { id: '2-R', type: 'bed', at: [21, 20], face: 'n', pose: 'lie', room: 'R' }, { id: '2-shower-8', type: 'shower', at: [22, 17], face: 'w', pose: 'stand', room: 'R' },
    { id: '2-basin-8', type: 'basin', at: [22, 17], face: 'w', pose: 'stand', room: 'R' }, { id: '2-toilet-8', type: 'toilet', at: [22, 17], face: 'n', pose: 'sit', room: 'R', xy: [22.2, 17.84], y: 0.42 },
    { id: '2-desk-8', type: 'lounge-seat', at: [22, 19], face: 'e', pose: 'sit', room: 'R', xy: [22.16, 19.21], y: 0.5, anim: 'read' },
    { id: '2-armchair-6', type: 'lounge-seat', at: [19, 19], face: 'e', pose: 'sit', room: 'R', xy: [19.43, 19.4], y: 0.44, anim: 'read', cush: 0.44 },
    // Counsellor
    { id: '2-N', type: 'bed', at: [11, 9], face: 'n', pose: 'lie', room: 'N' }, { id: '2-shower-9', type: 'shower', at: [12, 7], face: 'w', pose: 'stand', room: 'N' },
    { id: '2-basin-9', type: 'basin', at: [12, 7], face: 'w', pose: 'stand', room: 'N' }, { id: '2-toilet-9', type: 'toilet', at: [12, 7], face: 'n', pose: 'sit', room: 'N', xy: [12.2, 7.84], y: 0.42 },
    { id: '2-armchair-7', type: 'lounge-seat', at: [9, 9], face: 'e', pose: 'sit', room: 'N', xy: [9.43, 9.5], y: 0.44, anim: 'read', cush: 0.44 },
    // Senior Watch Officer
    { id: '2-G', type: 'bed', at: [15, 9], face: 'n', pose: 'lie', room: 'G' }, { id: '2-shower-10', type: 'shower', at: [16, 7], face: 'w', pose: 'stand', room: 'G' },
    { id: '2-basin-10', type: 'basin', at: [16, 7], face: 'w', pose: 'stand', room: 'G' }, { id: '2-toilet-10', type: 'toilet', at: [16, 7], face: 'n', pose: 'sit', room: 'G', xy: [16.2, 7.84], y: 0.42 },
    { id: '2-desk-9', type: 'lounge-seat', at: [13, 9], face: 'w', pose: 'sit', room: 'G', xy: [13.8, 9.5], y: 0.5, anim: 'read' },
    // Deputy Survey Chief
    { id: '2-D', type: 'bed', at: [11, 12], face: 's', pose: 'lie', room: 'D' }, { id: '2-shower-11', type: 'shower', at: [12, 14], face: 'w', pose: 'stand', room: 'D' },
    { id: '2-basin-11', type: 'basin', at: [12, 14], face: 'w', pose: 'stand', room: 'D' }, { id: '2-toilet-11', type: 'toilet', at: [12, 14], face: 'n', pose: 'sit', room: 'D', xy: [12.2, 14.64], y: 0.42 },
    { id: '2-desk-10', type: 'lounge-seat', at: [9, 12], face: 'w', pose: 'sit', room: 'D', xy: [9.8, 12.5], y: 0.5, anim: 'read' },
    // visitors' cabin
    { id: '2-U', type: 'bed', at: [15, 12], face: 's', pose: 'lie', room: 'U' }, { id: '2-shower-12', type: 'shower', at: [16, 14], face: 'w', pose: 'stand', room: 'U' },
    { id: '2-basin-12', type: 'basin', at: [16, 14], face: 'w', pose: 'stand', room: 'U' }, { id: '2-toilet-12', type: 'toilet', at: [16, 14], face: 'n', pose: 'sit', room: 'U', xy: [16.2, 14.64], y: 0.42 },
    { id: '2-armchair-8', type: 'lounge-seat', at: [13, 12], face: 'e', pose: 'sit', room: 'U', xy: [13.42, 12.5], y: 0.44, anim: 'read', cush: 0.44 },
    // the Watch office
    { id: '2-watch-1', type: 'work:watch', at: [24, 1], face: 's', pose: 'work', room: 'W' }, { id: '2-watch-2', type: 'work:watch', at: [25, 1], face: 's', pose: 'work', room: 'W' },
    { id: '2-watch-3', type: 'work:watch', at: [26, 1], face: 's', pose: 'work', room: 'W' }, { id: '2-watch-4', type: 'work:watch', at: [25, 6], face: 'w', pose: 'sit', room: 'W', xy: [25, 6], y: 0.5 },
    { id: '2-watch-5', type: 'work:watch', at: [25, 3], face: 'e', pose: 'stand', room: 'W' },
    // the washroom
    { id: '2-wctoilet-1', type: 'toilet', at: [24, 13], face: 'w', pose: 'sit', room: 'w', xy: [24.5, 13.6], y: 0.4 }, { id: '2-wctoilet-2', type: 'toilet', at: [24, 16], face: 'w', pose: 'sit', room: 'w', xy: [24.5, 16.4], y: 0.4 },
    { id: '2-wcbasin-1', type: 'basin', at: [24, 15], face: 'w', pose: 'stand', room: 'w' },
    // the chart room
    { id: '2-survey-1', type: 'work:survey', at: [29, 2], face: 's', pose: 'sit', room: 'K', xy: [29.28, 2.89], y: 0.49, anim: 'read' },
    { id: '2-survey-2', type: 'work:survey', at: [30, 2], face: 's', pose: 'sit', room: 'K', xy: [30.72, 2.89], y: 0.49, anim: 'read' },
    { id: '2-survey-3', type: 'work:survey', at: [29, 5], face: 'n', pose: 'sit', room: 'K', xy: [29.3, 5.65], y: 0.49, anim: 'read' },
    { id: '2-survey-4', type: 'work:survey', at: [30, 5], face: 'n', pose: 'sit', room: 'K', xy: [30.7, 5.65], y: 0.49, anim: 'read' }, { id: '2-survey-5', type: 'work:survey', at: [31, 4], face: 'w', pose: 'work', room: 'K' },
    { id: '2-windowseat-3', type: 'lounge-seat', at: [28, 0], face: 's', pose: 'sit', room: 'K', y: 0.52, anim: 'read', window: true },
    { id: '2-windowseat-4', type: 'lounge-seat', at: [30, 0], face: 's', pose: 'sit', room: 'K', y: 0.52, anim: 'read', window: true },
    { id: '2-windowseat-5', type: 'common-room', at: [31, 0], face: 's', pose: 'sit', room: 'K', y: 0.52, anim: 'read', window: true },
    { id: '2-armchair-12', type: 'common-room', at: [27, 7], face: 'e', pose: 'sit', room: 'K', xy: [27.5, 7.5], y: 0.44, anim: 'read', cush: 0.44 },
    // the Survey lab
    { id: '2-survey-6', type: 'work:survey', at: [33, 1], face: 's', pose: 'work', room: 'L' }, { id: '2-survey-7', type: 'work:survey', at: [35, 1], face: 's', pose: 'work', room: 'L' },
    { id: '2-survey-8', type: 'work:survey', at: [36, 1], face: 's', pose: 'work', room: 'L' }, { id: '2-survey-9', type: 'work:survey', at: [37, 1], face: 's', pose: 'work', room: 'L' },
    { id: '2-survey-10', type: 'work:survey', at: [35, 3], face: 's', pose: 'sit', room: 'L', xy: [35.08, 3.35], y: 0.49 }, { id: '2-survey-11', type: 'work:survey', at: [37, 3], face: 's', pose: 'sit', room: 'L', xy: [37.08, 3.35], y: 0.49 },
    { id: '2-survey-12', type: 'work:survey', at: [35, 5], face: 'n', pose: 'sit', room: 'L', xy: [35.08, 5.65], y: 0.49 }, { id: '2-survey-13', type: 'work:survey', at: [37, 5], face: 'n', pose: 'sit', room: 'L', xy: [37.08, 5.65], y: 0.49 },
    { id: '2-survey-14', type: 'work:survey', at: [34, 6], face: 'e', pose: 'work', room: 'L' }, { id: '2-survey-15', type: 'work:survey', at: [34, 2], face: 'e', pose: 'work', room: 'L' },
    // the sample lab
    { id: '2-survey-17', type: 'work:survey', at: [36, 14], face: 's', pose: 'sit', room: 'M', xy: [36.28, 14.89], y: 0.49 }, { id: '2-survey-18', type: 'work:survey', at: [38, 14], face: 's', pose: 'sit', room: 'M', xy: [38.58, 14.84], y: 0.49 },
    { id: '2-survey-19', type: 'work:survey', at: [36, 17], face: 'n', pose: 'sit', room: 'M', xy: [36.24, 17.35], y: 0.49 }, { id: '2-survey-20', type: 'work:survey', at: [38, 17], face: 'n', pose: 'sit', room: 'M', xy: [38.57, 17.37], y: 0.49 },
    { id: '2-survey-21', type: 'work:survey', at: [35, 19], face: 'n', pose: 'work', room: 'M' }, { id: '2-survey-22', type: 'work:survey', at: [36, 19], face: 'n', pose: 'work', room: 'M' },
    { id: '2-survey-23', type: 'work:survey', at: [39, 19], face: 'n', pose: 'work', room: 'M' }, { id: '2-survey-24', type: 'work:survey', at: [35, 18], face: 'e', pose: 'work', room: 'M' },
    // the observatory
    { id: '2-windowseat-6', type: 'common-room', at: [41, 1], face: 's', pose: 'sit', room: 'J', xy: [41.5, 1.2], y: 0.52, anim: 'read', window: true, event: 'observatory-night' },
    { id: '2-windowseat-7', type: 'common-room', at: [43, 1], face: 's', pose: 'sit', room: 'J', xy: [43.5, 1.2], y: 0.52, anim: 'read', window: true, event: 'observatory-night' },
    { id: '2-survey-16', type: 'work:survey', at: [42, 5], face: 's', pose: 'work', room: 'J' },
    { id: '2-beanbag-1', type: 'common-room', at: [42, 6], face: 28.6, pose: 'sit', room: 'J', xy: [42, 6.8], y: 0.39, anim: 'talk', event: 'observatory-night', cush: 0.319 },
    { id: '2-beanbag-2', type: 'common-room', at: [43, 7], face: -17.2, pose: 'sit', room: 'J', xy: [43.2, 7.4], y: 0.4, anim: 'talk', event: 'observatory-night', cush: 0.319 },
    // observatory night (0.32.3, answer 25): one evening a week off-duty crew gather here (the sim engineer schedules it).
    // Everything tagged event 'observatory-night' is the gathering: the bench and beanbag seats above, and these, which are
    // type 'event' so the everyday habits leave them alone. window: by the bow glass.
    { id: '2-obsnight-1', type: 'event', at: [42, 1], face: 's', pose: 'sit', room: 'J', xy: [42.6, 1.2], y: 0.52, anim: 'talk', window: true, event: 'observatory-night', calm: true },
    { id: '2-obsnight-2', type: 'event', at: [44, 1], face: 'n', pose: 'stand', room: 'J', window: true, event: 'observatory-night' },
    { id: '2-obsnight-3', type: 'event', at: [41, 2], face: 'n', pose: 'stand', room: 'J', anim: 'talk', event: 'observatory-night' },
    { id: '2-obsnight-4', type: 'event', at: [41, 3], face: 'e', pose: 'stand', room: 'J', anim: 'talk', event: 'observatory-night' },
    { id: '2-obsnight-5', type: 'event', at: [43, 3], face: 'w', pose: 'stand', room: 'J', anim: 'talk', event: 'observatory-night' },
    { id: '2-obsnight-6', type: 'event', at: [44, 5], face: 'w', pose: 'sit', room: 'J', y: 0.18, anim: 'talk', event: 'observatory-night', calm: true },
    { id: '2-obsnight-7', type: 'event', at: [44, 6], face: 'w', pose: 'sit', room: 'J', y: 0.18, anim: 'talk', event: 'observatory-night', calm: true },
    // the comms room
    { id: '2-comms-1', type: 'work:comms', at: [29, 20], face: 'n', pose: 'work', room: 'Q' }, { id: '2-comms-2', type: 'work:comms', at: [26, 20], face: 'n', pose: 'work', room: 'Q' },
    { id: '2-comms-3', type: 'work:comms', at: [26, 15], face: 's', pose: 'sit', room: 'Q', xy: [26.84, 15.79], y: 0.5, anim: 'talk', cush: 0.5 },
    { id: '2-comms-4', type: 'work:comms', at: [27, 15], face: 's', pose: 'sit', room: 'Q', xy: [27.16, 15.79], y: 0.5, anim: 'talk', cush: 0.5 },
    { id: '2-comms-5', type: 'work:comms', at: [28, 15], face: 's', pose: 'sit', room: 'Q', xy: [28.65, 15.76], y: 0.5, anim: 'talk', cush: 0.5 },
    { id: '2-comms-6', type: 'work:comms', at: [29, 15], face: 's', pose: 'sit', room: 'Q', xy: [29.65, 15.76], y: 0.5, anim: 'talk', cush: 0.5 },
    { id: '2-comms-7', type: 'work:comms', at: [26, 18], face: 's', pose: 'sit', room: 'Q', xy: [26.18, 18.35], y: 0.5, anim: 'talk' },
    { id: '2-comms-8', type: 'work:comms', at: [27, 18], face: 's', pose: 'sit', room: 'Q', xy: [27.18, 18.35], y: 0.5, anim: 'talk' },
    { id: '2-comms-9', type: 'work:comms', at: [28, 18], face: 's', pose: 'sit', room: 'Q', xy: [28.64, 18.36], y: 0.5, anim: 'talk' },
    { id: '2-comms-10', type: 'work:comms', at: [29, 18], face: 's', pose: 'sit', room: 'Q', xy: [29.64, 18.36], y: 0.5, anim: 'talk' },
    // the lobby
    { id: '2-bench-1', type: 'bench', at: [21, 16], face: 'n', pose: 'sit', room: '+', xy: [21.5, 16.6], y: 0.48 }, { id: '2-watch-6', type: 'work:watch', at: [22, 6], face: 'w', pose: 'stand', room: '+' },
    { id: '2-liftwait-1', type: 'lift-wait', at: [17, 9], face: 'e', pose: 'stand', room: '+' }, { id: '2-liftwait-2', type: 'lift-wait', at: [22, 9], face: 'w', pose: 'stand', room: '+' },
    { id: '2-liftwait-3', type: 'lift-wait', at: [17, 10], face: 'e', pose: 'stand', room: '+' }, { id: '2-liftwait-4', type: 'lift-wait', at: [22, 10], face: 'w', pose: 'stand', room: '+' },
    { id: '2-liftwait-5', type: 'lift-wait', at: [17, 11], face: 'e', pose: 'stand', room: '+' }, { id: '2-liftwait-6', type: 'lift-wait', at: [22, 11], face: 'w', pose: 'stand', room: '+' },
    // the senior corridor
    { id: '2-watch-7', type: 'work:watch', at: [8, 10], face: 'w', pose: 'stand', room: '-' },
    // the science corridor
    { id: '2-bench-2', type: 'bench', at: [24, 9], face: 's', pose: 'sit', room: '=', xy: [24.5, 9.4], y: 0.48 }, { id: '2-bench-3', type: 'bench', at: [25, 9], face: 's', pose: 'sit', room: '=', xy: [25.5, 9.4], y: 0.48 },
    { id: '2-bench-4', type: 'bench', at: [40, 12], face: 'n', pose: 'sit', room: '=', xy: [40.5, 12.6], y: 0.48 }, { id: '2-bench-5', type: 'bench', at: [39, 12], face: 'n', pose: 'sit', room: '=', xy: [39.5, 12.6], y: 0.48 },
    { id: '2-watch-8', type: 'work:watch', at: [44, 11], face: 'e', pose: 'stand', room: '=' },
    // the lab gas plant
    { id: '2-works-1', type: 'work:works', at: [39, 3], face: 'e', pose: 'work', room: 'g', machine: '2-gasplant-1' },
    { id: '2-works-2', type: 'work:works', at: [39, 7], face: 'e', pose: 'work', room: 'g', machine: '2-extractor-1' },
    // the utility closet
    { id: '2-works-3', type: 'work:works', at: [23, 18], face: 'e', pose: 'work', room: 'u', machine: '2-breaker-1' },
    { id: '2-works-4', type: 'work:works', at: [23, 20], face: 'e', pose: 'work', room: 'u', machine: '2-junction-1' },
    // the cable crawl
    { id: '2-works-5', type: 'work:works', at: [35, 21], face: 'w', pose: 'work', room: 'n', machine: '2-repeater-1' },
    { id: '2-works-6', type: 'work:works', at: [39, 21], face: 'e', pose: 'work', room: 'n', machine: '2-feed-1' },
    // the sensor array
    { id: '2-works-7', type: 'work:works', at: [46, 11], face: 'e', pose: 'work', room: 'A', machine: '2-array-1' },
    { id: '2-works-8', type: 'work:works', at: [47, 5], face: 'n', pose: 'work', room: 'A', machine: '2-racks-1' },
    { id: '2-works-9', type: 'work:works', at: [47, 16], face: 's', pose: 'work', room: 'A', machine: '2-racks-2' },
  ],
  dress(d) {
    for (const [key, tw, text] of d.plates) placeOnEdge('plate', key, tw, { text });
    for (const [key, tw, text] of d.nameplates) placeOnEdge('brassPlate', key, tw, d2Plate(d.sealed[key], text));
    for (const [key, tw] of [['v,19,12', 'w'], ['v,21,12', 'e']]) placeOnEdge('liftPanel', key, tw);
    placeOnEdge('deckDirectory', 'v,17,10', 'e', { it: IT('Deck directory', 'Seven decks, top to bottom. Bridge, Command & Science, Commons, Quarters, the Recreation Deck (R), Operations, Engineering. You are here: Command & Science, one below the bridge.') });
    // the spine behind glass: the trunks above the car, the ladder below it
    for (const r of ['Y', 'Z']) NO_FADE.add(r);
    place('Y', 'spineTrunks', 1, .5, 'n', { it: SPINE_IT.trunks });
    place('Z', 'spineLadder', 1, .5, 'n', { it: SPINE_IT.ladder });
    // the lobby ring: a bench by the washroom, plants in the far corners, clear of every doorway and both ends of the loop
    place('+', 'bench', 4.5, 11.68, 's', { snug: true, it: IT('Bench', 'Somewhere to wait for the lift without looking as if you are waiting outside the Captain\'s door.') });
    for (const [x, z, band] of [[5.55, .45, '#c9a24a'], [5.55, 11.55, '#c9a24a']]) place('+', 'plant', x, z, 'n', { band, big: true });
    // ---- the bedrooms (turn 2): locked, furnished, and seen from above when the walls drop. A tap on the bed or desk
    // says something about who lives there, without walking (the door stays shut).
    const SEE = (t, x) => ({ t, x, see: true });
    d2Suite('O', 'h,9,5', { fab: D2.fabs.sand, rug: 1, bed: SEE('The Works Chief\'s bed', 'Made with hospital corners. A spare hard hat on the nightstand, just in case.'), desk: SEE('The Works Chief\'s desk', 'The job list on the terminal, and your name on it somewhere. Probably near the bottom, for now.') });
    d2Suite('I', 'h,13,5', { fab: D2.fabs.teal, rug: 1, bed: SEE('The Infirmary Chief\'s bed', 'A comm on the pillow, set to wake for anything from Deck 3.'), desk: SEE('Medical journals', 'A stack of them, bookmarked, with notes in the margins in very small writing.') });
    d2Suite('V', 'h,17,5', { fab: D2.fabs.sage, rug: 0, papers: true, kettle: true, bed: SEE('Dr. Sato\'s bed', 'A field guide to frontier lichens, face down on the pillow.'), desk: SEE('Dr. Sato\'s desk', 'Buried in survey printouts and a kettle that is never quite cold. Her terrible tea, in a tin marked TEA (GOOD).') });
    d2Suite('S', 'h,19,5', { fab: D2.fabs.slate, rug: 2, bed: SEE('The Second Officer\'s bed', 'Two alarm clocks, set a minute apart, for the night watch.'), desk: SEE('The Second Officer\'s desk', 'The night watch rota, and a mug that says THIRD IN COMMAND, FIRST TO BE WOKEN.') });
    d2Suite('T', 'h,9,17', { fab: D2.fabs.wine, rug: 2, bed: SEE('Chief Holt\'s bed', 'Squared away. A pair of boots under it, polished, side by side.'), desk: SEE('Chief Holt\'s desk', 'Patrol reports in a neat pile, and a note: ASK THE ENVOY ABOUT THE CORD. DON\'T.') });
    d2Suite('B', 'h,13,17', { fab: D2.fabs.navy, rug: 0, swans: true, bed: SEE('Visitors\' suite', 'Made up for whoever the Concord sends next. Two towel swans on the bed, beak to beak.') });
    d2Suite('H', 'h,17,17', { fab: D2.fabs.navy, rug: 1, model: true, bed: SEE('The Senior Helm Officer\'s bed', 'A sleep mask with stars on it.'), desk: SEE('A model of the Wren', 'Hand-built, every hull plate scored in. The helm officer flies the real one on the day watch.') });
    d2Suite('R', 'h,19,17', { fab: D2.fabs.teal, rug: 2, bed: SEE('The Comms Chief\'s bed', 'A spare headset on the nightstand. Calls home don\'t keep office hours.'), desk: SEE('The Comms Chief\'s desk', 'A queue of messages waiting to go out, sorted by how far they have to travel.') });
    d2Suite('N', 'h,10,7', { inner: true, armchairs: true, fab: D2.fabs.sage, rug: 1, bed: SEE('The Counsellor\'s cabin', 'An armchair by the door and a box of tissues within reach of it. Even off duty.') });
    d2Suite('G', 'h,14,7', { inner: true, fab: D2.fabs.wine, rug: 2, bed: SEE('The Senior Watch Officer\'s bed', 'A night-watch sleeper: blackout blind, earplugs, and a sign on the wall that says LATER.'), desk: SEE('The Watch Officer\'s desk', 'A chessboard mid-game. Holt is losing, by the look of it.') });
    d2Suite('D', 'h,10,15', { inner: true, fab: D2.fabs.navy, rug: 0, papers: true, bed: SEE('The Deputy Survey Chief\'s bed', 'A star chart pinned to the wall where a window would be.'), desk: SEE('The Survey deputy\'s desk', 'Sample logs, cross-referenced in three colours. Dr. Sato\'s handwriting in the fourth.') });
    d2Suite('U', 'h,14,15', { inner: true, armchairs: true, fab: D2.fabs.sand, rug: 1, swans: true, bed: SEE('Visitors\' cabin', 'Made up and empty. Fresh towels, folded into swans by someone with time on their hands.') });
    // Commander Vance's corner cabin (6 x 5, the stern corner rounded off): bed under the port windows, two chairs squared to a table
    NO_FADE.add('X');
    place('X', 'suiteBed', 4.4, 1.2, 'n', { fab: D2.fabs.navy, it: SEE('Commander Vance\'s bed', 'Made so tight you could bounce a coin on it. Someone probably has.') });
    place('X', 'suiteRug', 2.15, 2.75, 'n', { w: 3.0, d: 1.5, k: 0 });
    place('X', 'armchair', 1.15, 2.75, 'w', { fab: D2.fabs.navy }); place('X', 'armchair', 3.15, 2.75, 'e', { fab: D2.fabs.navy });
    place('X', 'coffeeTable', 2.15, 2.75, 'w');
    place('X', 'suiteDesk', .375, 4.3, 'w', { it: SEE('Commander Vance\'s desk', 'Pens in a row, by length. The ship\'s rowing leaderboard, printed out, with one name circled.') }); place('X', 'suiteChair', .95, 4.3, 'e');
    place('X', 'suiteShelf', 2.1, 4.74, 's', { trophy: true }); place('X', 'ensuite', 4.2, 4.4, 's'); place('X', 'suiteWardrobe', 5.625, 2.2, 'e');
    place('X', 'suitePlant', 2.6, .9, 'n');
    // Envoy Saruth's corner cabin, mirroring Vance's: a low futon behind a screen, a tea table on the floor with cushions round it
    NO_FADE.add('E');
    place('E', 'futon', 4.4, 3.85, 's', { fab: D2.fabs.teal, it: SEE('The Envoy\'s futon', 'Low, firm and very neatly made. A Veyli sleeping screen stands beside it.') });
    place('E', 'sleepScreen', 3.2, 3.4, 'w');
    place('E', 'suiteRug', 1.9, 2.0, 'n', { w: 2.4, d: 2.2, k: 1 });
    place('E', 'lowTable', 1.9, 2.0, 'n', { it: SEE('Veyli tea table', 'Low, round, with a tea set for five. Veyli tea is taken kneeling, in silence, and takes an hour. Holt has been invited twice.') });
    for (let k = 0; k < 5; k++) { const a = k * Math.PI * 2 / 5 + .3; place('E', 'cushion', 1.9 + Math.sin(a) * .82, 2.0 + Math.cos(a) * .82, 'n', { fab: k % 2 ? D2.fabs.teal : D2.fabs.sand }); }
    place('E', 'ensuite', 3.9, .6, 'n'); place('E', 'suiteWardrobe', 5.625, 2.0, 'e');
    place('E', 'suitePlant', .6, .5, 'n');
    // ---- the Captain's quarters (turn 3): 5 x 12 across the stern, windows all along it. The sleeping alcove at the port
    // end behind a curtain, the dining table in the middle by the door, the study lined with books at the starboard end.
    NO_FADE.add('C');
    place('C', 'suiteBed', 2.3, 1.2, 'n', { wide: true, fab: D2.fabs.wine, it: SEE('The Captain\'s bed', 'Behind a heavy curtain. A book face down on the nightstand, and a comm beside it that is never switched off.') });
    place('C', 'ensuite', 4.4, .6, 'n'); place('C', 'suiteWardrobe', .375, 1.6, 'w'); place('C', 'suitePlant', .4, .4, 'n');
    place('C', 'alcoveCurtain', 1.75, 3.0, 'n', { w: 3.2 });
    place('C', 'telescope', .7, 4.0, 'w');
    place('C', 'suiteRug', 2.3, 6.4, 'n', { w: 2.6, d: 4.6, k: 2 });
    place('C', 'diningTable', 2.3, 6.4, 'n', { light: true, it: SEE('The Captain\'s table', 'Laid for eight. The Captain hosts the senior crew here, and the Envoy when she accepts. Nobody sits in the Captain\'s chair, even when she\'s late.') });
    place('C', 'windowSeat', .38, 6.4, 'w', { w: 2.6 });
    place('C', 'sideboard', 4.64, 7.6, 'e');
    // low shelves all round the study, so the room still shows from the usual camera
    for (const x of [.65, 1.7, 2.75, 3.8]) place('C', 'suiteShelf', x, 11.74, 's', { it: x === 1.7 ? SEE('The Captain\'s books', 'Real books, carried aboard one at a time over thirty years. Histories, poetry, and a shelf of very old star atlases.') : undefined });
    for (const z of [9.6, 10.65]) place('C', 'suiteShelf', 4.74, z, 'e', { trophy: z > 10 });
    place('C', 'captainDesk', 2.25, 9.4, 'n', { it: SEE('The Captain\'s desk', 'The day\'s reports in a neat stack, a fountain pen, and a photograph turned face down.') });
    place('C', 'suiteChair', 2.25, 10.2, 's');
    place('C', 'armchair', .65, 10.6, 'w', { fab: D2.fabs.wine }); place('C', 'globe', .5, 9.0, 'n');
    placeOnEdge('knocker', 'v,7,10', 'e');
    // ---- the senior corridor: brass wall lamps, the Wren's past captains along the gallery, flowers on the consoles ----
    for (const [key, tw] of [['h,11,5', 's'], ['h,15,5', 's'], ['h,12,7', 'n'], ['h,16,7', 'n'], ['h,12,15', 's'], ['h,16,15', 's'], ['h,11,17', 'n'], ['h,15,17', 'n'], ['v,7,9', 'e'], ['v,7,11', 'e']])
      placeOnEdge('brassSconce', key, tw);
    placeOnEdge('portrait', 'v,7,7', 'e', { k: 0, it: IT('Captain Ilse Varga', 'The Wren\'s first captain, who took her out of the yards forty years ago. Nobody remembers her smiling, but the frame has been polished every week since.') });
    placeOnEdge('portrait', 'v,7,13', 'e', { k: 1, it: IT('Captain Adaeze Moro', 'Captain of the Wren through the long blockade. A note on the frame: SHE GOT EVERYONE HOME.') });
    placeOnEdge('portrait', 'v,9,8', 'w', { k: 2, it: IT('Captain Hal Brenner', 'He commissioned the music room, and a grand piano nobody knew how to lash down. Captain Marrow plays it now.') });
    placeOnEdge('portrait', 'v,9,13', 'w', { k: 0, it: IT('Captain Odile Marrow', 'The current captain, painted the year she took command. She asked for it to hang last in line, where it is easy to take down.') });
    place('-', 'consoleTable', 1.75, 3.5, 'e', { snug: true, k: 0 }); place('-', 'consoleTable', 1.75, 8.5, 'e', { snug: true, k: 2 });
    // ---- the Watch office (turn 4): status board under the windows, the duty desk facing the glass onto the lobby ----
    place('W', 'controlBoard', 2.0, .45, 'n', { w: 3.4, it: IT('Status board', 'Every door, hatch and lift on the ship, and who badged through it last. Green is fine. Amber is someone propping a door open again.') });
    place('W', 'desk', 1.3, 6.0, 'w', { it: IT('Duty desk', 'Facing the glass, so the Watch sees everyone who rides the lift. The docking log lies open: one shuttle out, one shuttle back, all signed for.') });
    place('W', 'chair', 2.0, 6.0, 'e');
    place('W', 'locker', 3.6, 3.0, 'e', { it: IT('Watch lockers', 'Jackets, torches and the spare comms. One locker is labelled HOLT and has never been seen open.') });
    place('W', 'dispenser', 3.55, 5.0, 'e', { it: IT('Coffee', 'The Watch runs on it. The machine has a name, KEVIN, and a maintenance record longer than yours.') });
    place('W', 'crate', 3.3, 8.45, 's', { it: IT('Lost property', 'Full for a year: one glove, three mugs, a ukulele string, a datapad nobody will claim and a sock with a story.') });
    placeWall('W', 'notices', 'e', 6.8, { hitW: 1.0, it: IT('Patrol rota', 'Who walks which deck, and when. Your name is pencilled in for nothing yet. Someone has drawn a small star next to it.') });
    // ---- the washroom ----
    // two stalls and a basin along the far wall, laid by hand: the washroom template boxed in two of its three toilets in a room this narrow
    for (const z of [.7, 3.3]) place('w', 'toiletStall', 1.35, z, 'e', { it: z < 1 ? IT('Toilet', 'Vacant. The little green light is the most trusted instrument on the ship.') : undefined });
    place('w', 'basinCounter', 1.625, 2.0, 'e', { w: .9, n: 1, it: IT('Basin', 'One mirror, one tap, and a sign asking the labs not to rinse samples here.') });
    placeWall('w', 'towels', 'w', 3.1);
    // ---- the chart room: the glowing chart table, pigeonholes of rolled charts, a seat under the windows ----
    place('K', 'chartTable', 3.0, 4.3, 'n', { it: IT('Chart table', 'The frontier, glowing from underneath. The Wren\'s route is a dotted gold line; the circles are survey stops. Three done, four to go.') });
    for (const [x, z] of [[2.2, 2.95], [3.8, 2.95], [2.2, 5.65], [3.8, 5.65]]) place('K', 'stool', x, z, 'n');
    place('K', 'chartRack', 5.68, 4.3, 'e', { w: 2.0, it: IT('Chart pigeonholes', 'Rolled charts, every one labelled. Some are older than the ship, copied by hand from older ships.') });
    place('K', 'windowSeat', 3.0, .38, 'n', { w: 3.4, it: IT('Window seat', 'Port windows, to check the real thing against the chart. A good quiet place to sit, and nobody minds if you do.') });
    place('K', 'armchair', .6, 7.6, 'w', { fab: D2.fabs.navy }); place('K', 'globe', 5.4, 7.7, 'n'); place('K', 'suitePlant', 5.55, 1.2, 'n');
    for (const a of [3.0, 6.0]) placeWall('K', 'starChart', 'w', a, { it: a === 3.0 ? IT('Star chart', 'Hand-inked, with the constellations as they look from out here, which is not how they look from anywhere you grew up.') : undefined });
    // ---- the Survey lab: benches under the windows, an island, the scanner and the specimen shelf ----
    for (const x of [1.5, 4.1]) place('L', 'labBench', x, .45, 'n', { w: 2.2, it: x === 1.5 ? IT('Lab bench', 'Microscopes, slides and a stack of survey cores waiting to be logged. Everything is labelled, including the label maker.') : undefined });
    place('L', 'labIsland', 3.0, 4.5, 'n', { w: 3.4, it: IT('Bench island', 'Reagents on the shelf above, notes on the bench below. Dr. Sato\'s side is the tidy one, which surprises everyone.') });
    for (const [x, z] of [[2.0, 3.35], [4.0, 3.35], [2.0, 5.65], [4.0, 5.65]]) place('L', 'stool', x, z, 'n');
    place('L', 'sampleScanner', .5, 6.8, 'w', { it: IT('Sample scanner', 'Put a sample in, close the lid, wait. It hums a little tune when it\'s done. Nobody programmed it to.') });
    place('L', 'specimenShelf', .33, 2.8, 'w', { it: IT('Specimen shelf', 'Odd things from the frontier, in jars. A label on the blue one: DO NOT LICK THE BLUE ONE. Someone has added: AGAIN.') });
    place('L', 'coldShelf', 5.67, 7.3, 'e');
    // ---- the observatory: a cushioned bench under the bow windows, the telescope, star charts, beanbags for the night ----
    place('J', 'windowSeat', 1.4, 1.0, 'n', { w: 2.4, it: IT('Cushioned bench', 'Under the bow windows. Off-duty crew sneak in here at night and pretend they came to look at the stars. They did.') });
    place('J', 'brassTelescope', 2.0, 4.4, 'n', { turn: -.5, it: IT('Telescope', 'A brass telescope on a pier, aimed out of the bow. Survey uses it by day. A note on the eyepiece: PUT IT BACK ON THE NEBULA WHEN YOU\'RE DONE.') });
    for (const a of [3.5, 6.5]) placeWall('J', 'starChart', 'w', a);
    place('J', 'beanbag', 1.0, 6.8, 'n', { turn: .5, fab: MUS.fab[1] }); place('J', 'beanbag', 2.2, 7.4, 'n', { turn: -.3, fab: MUS.fab[3] });
    for (const [z, f] of [[5.5, 'sage'], [6.5, 'wine']]) place('J', 'cushion', 3.5, z, 'e', { fab: D2.fabs[f] });   // floor cushions for observatory night (0.32.3)
    // ---- the comms room: the signal board along the windows, two rows of headset desks ----
    place('Q', 'signalBoard', 3.0, 8.55, 's', { w: 4.8, it: IT('Signal board', 'Every message in and out, as a line of light. The slow gold wave is a call home on its way out, weeks from arriving.') });
    for (const z of [3.6, 5.9]) for (const x of [1.5, 4.3]) {
      place('Q', 'commsDesk', x, z, 's', { it: z === 3.6 && x === 1.5 ? IT('Comms desk', 'Two screens, two headsets. Every recorded call from the Deck 3 booths passes through here on its way home, and nobody listens in. That\'s the rule.') : undefined });
      for (const dx of [-.5, .5]) place('Q', 'chair', x + dx, z - .7, 'n');
    }
    placeWall('Q', 'clocks', 'w', 2.0, { hitW: 1.5, it: IT('Clocks', 'Ship time, and how long a message takes to reach home and back. Right now, eleven weeks.') });
    placeWall('Q', 'msgBoard', 'e', 2.5, { hitW: 1.0, it: IT('Outgoing queue', 'Messages waiting for the next relay window. Yours would go on here, if you wrote one.') });
    place('Q', 'suitePlant', 5.55, .45, 'n');
    // ---- the specimen store (locked): frosted cabinets, a freezer, and a sample that hums ----
    NO_FADE.add('F');
    for (const z of [1.6, 3.2, 4.8, 6.4]) place('F', 'coldShelf', .33, z, 'w');
    place('F', 'humJar', 2.3, 7.9, 'n', { it: SEE('A humming sample', 'Sealed, labelled in Dr. Sato\'s hand, and glowing faintly green. It hums when nobody is looking. Everyone has checked.') });
    // ---- the sample lab: an island with centrifuges, fume hoods and a glove box at the back, a cold cabinet ----
    place('M', 'labIsland', 3.4, 3.1, 'n', { w: 4.0, centrifuge: true, it: IT('Sample bench', 'Centrifuges and racks of sample tubes. Quieter than the Survey lab, and colder.') });
    for (const [x, z] of [[2.2, 1.95], [4.6, 1.95], [2.2, 4.25], [4.6, 4.25]]) place('M', 'stool', x, z, 'n');
    for (const x of [1.0, 2.3]) place('M', 'fumeHood', x, 7.55, 's', { it: x === 1.0 ? IT('Fume hood', 'Anything that smells goes in here. The extractor is fed by the lab gas plant, through the Survey lab\'s hatch.') : undefined });
    place('M', 'gloveBox', 5.2, 7.6, 's', { it: IT('Glove box', 'For samples that must never touch the air, or you. The gloves are big enough for Holt.') });
    place('M', 'coldShelf', 6.67, 4.5, 'e');
    place('M', 'labBench', .45, 5.5, 'w', { w: 1.8, scope: false });
    // ---- the probe bay (locked): three probes in cradles, nose to their launch tubes ----
    NO_FADE.add('P');
    for (const x of [.8, 2.0, 3.2]) place('P', 'probeCradle', x, 4.0, 'n', { it: x === 2.0 ? SEE('Survey probes', 'Three probes in their cradles, charged and waiting, noses to the launch tubes in the starboard bow.') : undefined });
    for (const x of [.8, 2.0, 3.2]) place('P', 'launchTube', x, 7.6, 's');
    // ---- the sensor array (locked, seen through the window at the end of the corridor) ----
    NO_FADE.add('A');
    place('A', 'sensorDish', 3.2, 10.5, 'n', { turn: Math.PI / 2, light: true, it: SEE('Sensor dish', 'The main sensor dish, turning slowly under blue light, listening to the whole frontier at once. Tier 3, when the array opens.') });
    place('A', 'signalRacks', 1.9, 3.8, 'n', { n: 3, it: SEE('Signal processors', 'Racks of them, blinking. Everything the dish hears goes through here before anyone on the bridge sees it.') });
    place('A', 'signalRacks', 1.9, 16.2, 's', { n: 3 });
    place('A', 'mastBase', 5.4, 10.5, 'n', { it: SEE('Comms mast', 'The base of the comms mast, running up through the bridge to the outside. Every call home leaves the ship up this.') });
    // ---- the science corridor: benches, plants and two notice boards ----
    place('=', 'bench', 2.0, .3, 'n', { snug: true, it: IT('Bench', 'Outside the Watch office. People who sit here tend to get asked what they\'re waiting for.') });
    place('=', 'bench', 17.0, 3.7, 's', { snug: true });
    for (const [x, z] of [[9.5, .4], [10.5, 3.6]]) place('=', 'suitePlant', x, z, 'n');
    placeOnEdge('notices', 'h,38,9', 's', { it: IT('Survey board', 'This week\'s samples, the next survey stop and a sign-up sheet for observatory nights. The waiting list is long.') });
    placeOnEdge('notices', 'h,30,13', 'n', { it: IT('Comms notices', 'Relay windows for messages home, and a reminder: KEEP IT KIND, IT TAKES WEEKS TO ARRIVE.') });
    // ---- the utility rooms (0.32.2, plans/deck2-plan.html "Utility rooms"): Works crew and the player come in through
    // the service hatches. Each machine has a panel tile in front of it, where someone stands to service it.
    // the lab gas plant: bottle racks along the observatory side, the regulator manifold and the labs' extractor fan
    for (const z of [.5, 1.5, 2.5, 5.5, 6.5]) place('g', 'gasRack', 1.675, z, 'e', { it: z === 1.5 ? IT('Gas bottles', 'Nitrogen, argon and a calibration mix, chained in racks. Empty ones get a chalk cross and go down to the hold.') : undefined });
    place('g', 'gasManifold', 1.7, 3.5, 'e', { it: IT('Regulator manifold', 'Three gauges and three valves: the lab gas lines for the Survey lab and the sample lab. The middle needle sits a little low. It always has.') });
    place('g', 'extractor', 1.625, 7.5, 'e', { it: IT('Extractor fan', 'Pulls the fumes out of both labs\' hoods and up the duct. When it labours, the sample lab smells of whatever Survey is cooking.') });
    place('g', 'conduits', 1.8, 8.5, 'e');
    // the utility closet: Deck 2's breaker cabinet and the light relays, conduits at both ends
    place('u', 'powerCabinet', 1.65, 1.5, 'e', { it: IT('Breaker cabinet', 'Every circuit on Deck 2, labelled in two hands. One breaker is taped over: CAPTAIN\'S KETTLE. DO NOT.') });
    place('u', 'lightRelayRack', 1.65, 3.5, 'e', { it: IT('Light relays', 'They click over at dusk and dawn and run every lamp on the deck. A lazy one leaves a corridor flickering.') });
    for (const z of [.5, 4.5]) place('u', 'conduits', 1.8, z, 'e');
    // the cable crawl: trays along the hull carrying the array's cables aft, the repeater at one end, the feed at the other
    place('n', 'crawlCableTray', 3.5, .73, 's', { w: 5.0 });
    place('n', 'signalRepeater', .35, .5, 'w', { it: IT('Signal repeater', 'Lifts the array\'s signal for the long run aft to the comms room. Warm to the touch, and humming.') });
    place('n', 'arrayFeed', 6.7, .5, 'e', { it: IT('Array feed', 'Where the dish\'s cables come through the bulkhead and split for the racks. Each one labelled, in Dr. Sato\'s handwriting, naturally.') });
    // lived-in touches (0.32.3): a sign in the gas plant, the calendar nook in the closet, a sign and a forgotten mug in the crawl
    placeWall('g', 'd2Sign', 'w', 6.5, { m: D2.flames });
    placeWall('u', 'd2Nook', 'w', 2.5);
    placeWall('n', 'd2Sign', 'n', 2.5, { m: D2.head, y: 1.15 });
    place('n', 'd2Mug', .45, .5, 'w', { y: .8 });
  },
};
for (const [key, r] of Object.entries(DECKS[2].sealed)) DECKS[2].closedDoors[key] = { t: DECKS[2].rooms[r].name, x: DECKS[2].rooms[r].tap };

