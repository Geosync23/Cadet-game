// =====================================================================
// 4d. DECK DEFINITIONS
// One block per deck. Map keys are rooms; ROOM flags: hall (opens into
// other halls with no wall), void (sealed, drawn as a solid block).
// =====================================================================
const DECKS = {};
// =====================================================================
// UTILITY ROOMS KIT (Pillar 2, A5a: the Deck 6 architect). The insides of the sealed service rooms on
// Decks 4, 5 and 6: machines a Works tech stands in front of, and the ducts, pipes and shelves around them.
// Made at load and placed at the very end of a deck's dress(), with no R() anywhere, so nothing else on a
// deck shifts. A machine's front (+z) faces its panel tile, where its work:works place is.
// =====================================================================
const UT = {
  body: std('#7b8790', .5, .35), shell: std('#4d7d84', .45, .4), cab: std('#5d6a73', .5, .35), door: std('#6f7c85', .45, .35),
  louvre: std('#2b3238', .6, .3), filter: std('#e2dcc2', .9), duct: std('#a9b4ba', .4, .55), tank: std('#c45a3f', .5, .3),
  window: std('#1d2a30', .2, .2, { emissive: col('#16323c'), emissiveIntensity: .6 }),
};
Object.assign(KIT, {
  // an air scrubber: a tall housing on a plinth, louvres above the filter drawer, a fill screen, a collar up into the duct
  utilScrubber(g) {
    box(.9, .1, 1.6, WM.paintDark, 0, .05, 0, g);
    box(.86, 2.0, 1.5, UT.body, 0, 1.1, -.02, g);
    for (let k = 0; k < 6; k++) box(.7, .04, .03, UT.louvre, 0, 1.35 + k * .12, .74, g);
    box(.7, .5, .04, UT.filter, 0, .55, .745, g); box(.3, .04, .05, WM.steel, 0, .74, .78, g);
    box(.24, .13, .02, WM.screen, .2, 1.14, .74, g); box(.05, .05, .02, WM.navGreen, -.22, 1.14, .74, g);
    cyl(.22, .22, .6, UT.duct, 0, 2.4, -.2, g, 16);
    return { w: .9, d: 1.6, tall: true };
  },
  // ducting: a run along the ceiling (o.w long), or a riser floor to ceiling
  ductRun(g, o = {}) {
    const w = o.w || 1, y = o.y || 2.5;
    box(w, .34, .34, UT.duct, 0, y, 0, g);
    for (let x = -w / 2 + .3; x < w / 2; x += 1) box(.04, .4, .4, WM.steel, x, y, 0, g);
    return { w, d: .34, noBlock: true, tall: true };
  },
  ductRiser(g) {
    box(.46, H, .46, UT.duct, 0, H / 2, 0, g);
    for (const y of [.4, 1.4, 2.4]) box(.52, .05, .52, WM.steel, 0, y, 0, g);
    return { w: .5, d: .5, tall: true };
  },
  // a heat exchanger: a long shell on two saddles, banded, with flow and return nozzles up to the ceiling and a control box
  heatExchanger(g, o = {}) {
    for (const x of [-.75, .75]) box(.25, .45, 1.0, WM.paintDark, x, .225, 0, g);
    cyl(.55, .55, 2.0, UT.shell, 0, 1.0, 0, g, 24).rotation.z = Math.PI / 2;
    for (const x of [-1.0, 1.0]) soft(UT.shell, x, 1.0, 0, .18, .55, .55, g);
    for (const x of [-.55, 0, .55]) cyl(.57, .57, .06, WM.steel, x, 1.0, 0, g, 24).rotation.z = Math.PI / 2;
    for (const x of o.nozzles || [-.6, .6]) cyl(.12, .12, 1.2, ENG.copper, x, 2.15, 0, g, 12);
    box(.5, .45, .15, UT.cab, 0, .85, .6, g); box(.3, .14, .02, WM.screenAmber, 0, .95, .68, g); box(.05, .05, .02, WM.navGreen, .17, .75, .68, g);
    cyl(.08, .08, .03, M.trim, .55, 1.35, .55, g, 16).rotation.x = Math.PI / 2;
    return { w: 2.6, d: 1.6, tall: true };
  },
  // a circulation pump: motor and volute on a base plate, the outlet straight up to the ceiling
  circPump(g) {
    box(.75, .1, .6, WM.paintDark, 0, .05, 0, g);
    cyl(.2, .2, .5, UT.shell, -.12, .35, 0, g, 18).rotation.z = Math.PI / 2;
    cyl(.22, .22, .18, UT.body, .25, .35, 0, g, 18).rotation.z = Math.PI / 2;
    cyl(.07, .07, 2.3, ENG.copper, .25, 1.6, 0, g, 10);
    cyl(.07, .07, .4, ENG.copper, .25, .35, -.3, g, 10).rotation.x = Math.PI / 2;
    box(.05, .05, .02, WM.navGreen, -.12, .58, .2, g);
    return { w: .8, d: .7 };
  },
  // a red expansion tank on three legs
  expansionTank(g) {
    for (let k = 0; k < 3; k++) { const a = k * 2.09; cyl(.025, .025, .5, WM.steel, Math.cos(a) * .22, .25, Math.sin(a) * .22, g, 6); }
    cyl(.3, .3, .9, UT.tank, 0, .95, 0, g, 20); for (const y of [.5, 1.4]) soft(UT.tank, 0, y, 0, .3, .12, .3, g);
    cyl(.05, .05, 1.3, ENG.copper, 0, 2.15, 0, g, 8);
    return { w: .7, d: .7, tall: true };
  },
  // breaker cabinets, side by side (o.w wide): doors with a window onto the breakers, status lights, a label, a hazard kick plate
  breakerCabinet(g, o = {}) {
    const w = o.w || .8, n = Math.max(1, Math.round(w / .8)), dw = w / n;
    box(w, 2.0, .45, UT.cab, 0, 1.0, 0, g);
    box(w, .08, .47, WM.hazard, 0, .04, 0, g);
    for (let k = 0; k < n; k++) {
      const x = -w / 2 + dw * (k + .5);
      box(dw - .06, 1.8, .02, UT.door, x, 1.02, .235, g);
      box(dw * .55, .55, .012, UT.window, x, 1.35, .248, g);
      for (let q = 0; q < 3; q++) box(.04, .04, .012, q === k % 3 ? WM.screenAmber : WM.navGreen, x - .1 + q * .1, 1.72, .248, g);
      box(.03, .18, .04, WM.steel, x + dw * .36, 1.0, .25, g);
      box(dw * .4, .07, .01, KM.label, x, .55, .248, g);
    }
    return { w, d: .45, tall: true };
  },
  // store shelving with a fixed pattern of boxes and folded linen (no R(), unlike the deck shelving)
  utilShelf(g) {
    for (const sx of [-.45, .45]) for (const sz of [-.17, .17]) box(.04, 1.9, .04, M.metal, sx, .95, sz, g);
    const cols = [KM.label, KM.teal, M.trim, KM.panel, KM.gold, M.cream], ws = [.18, .24, .14, .2, .16];
    for (let k = 0; k < 4; k++) {
      const y = .12 + k * .55; box(.94, .03, .38, M.slateDark, 0, y, 0, g);
      let x = -.4, q = k;
      while (x < .3) { const w = ws[q % 5], h = .12 + (q * 7 % 5) * .04; box(w, h, .28, cols[(q * 3 + k) % 6], x + w / 2, y + .015 + h / 2, 0, g); x += w + .03; q++; }
    }
    return { w: .95, d: .4, tall: true };
  },
});
Object.assign(WALL_KIT, {
  // a light-relay board: rows of relays and their lights
  relayBoard(g) {
    box(.7, .9, .06, UT.cab, 0, 1.45, .03, g);
    for (let r = 0; r < 3; r++) for (let c = 0; c < 4; c++) {
      box(.1, .14, .06, WM.steel, -.24 + c * .16, 1.7 - r * .24, .08, g);
      box(.03, .03, .01, (r + c) % 4 ? WM.navGreen : WM.screenAmber, -.24 + c * .16, 1.8 - r * .24, .115, g);
    }
  },
  // spare filter cartridges on a wall rack
  filterRack(g) {
    box(.8, .04, .26, WM.steel, 0, 1.2, .13, g);
    for (const x of [-.26, 0, .26]) box(.22, .32, .2, UT.filter, x, 1.38, .12, g);
    box(.3, .08, .01, KM.label, 0, 1.6, .02, g);
  },
});

// ---- Deck 5's utility rooms (0.30.3): the air plant, manifold room, battery room, cart bay, cargo hold and pipe galleries ----
Object.assign(UT, {
  cell: std('#7fd6e0', .12, 0, { emissive: col('#2a8f9a'), emissiveIntensity: .55 }), bubble: std('#eafcff', .2, 0, { emissive: col('#bff4ff'), emissiveIntensity: .8 }),
  charge: std('#7dffb0', .3, 0, { emissive: col('#2fe07a'), emissiveIntensity: .9 }), cellCase: std('#3b4a52', .55, .3),
  pipes: ['#c45a3f', '#2f8e98', '#e9c46a', '#5a7fbf', '#8fbf6a'].map(c => std(c, .45, .3)), wheel: std('#c4372a', .5, .3),
  cart: std('#d9a441', .55, .2), cartGlow: std('#9ff3e6', .3, 0, { emissive: col('#4fd8c4'), emissiveIntensity: 1.1 }),
});
Object.assign(KIT, {
  // a bank of oxygen cells: three glowing columns of electrolyte with bubbles, in a frame, piped up into the ceiling
  o2Bank(g) {
    box(1.8, .12, .7, WM.paintDark, 0, .06, 0, g); box(1.8, .1, .7, WM.paintDark, 0, 2.05, 0, g);
    for (const x of [-.6, 0, .6]) {
      cyl(.22, .22, 1.8, UT.cell, x, 1.05, 0, g, 18);
      for (let k = 0; k < 4; k++) soft(UT.bubble, x + ((k * 37) % 9 - 4) * .025, .45 + k * .38, .12, .035, .035, .035, g);
      cyl(.05, .05, .7, M.metal, x, 2.45, 0, g, 8);
    }
    for (const x of [-.9, .9]) box(.06, 2.0, .06, M.metal, x, 1.05, .3, g);
    box(.3, .14, .02, WM.screen, .55, .3, .36, g);
    return { w: 1.8, d: .7, tall: true };
  },
  // the electrolyser: stacked cell plates in a long housing, a water feed in, oxygen (blue) and hydrogen (white) out overhead
  electrolyser(g) {
    box(1.7, .1, 1.6, WM.paintDark, 0, .05, 0, g);
    box(1.6, 1.5, 1.3, UT.body, 0, .85, -.05, g);
    for (let k = 0; k < 9; k++) box(.05, 1.1, 1.0, UT.shell, -.6 + k * .15, .85, .62, g);
    box(.5, .3, .04, WM.screen, .45, 1.45, .62, g); box(.05, .05, .02, WM.navGreen, .1, 1.45, .62, g);
    cyl(.09, .09, 1.2, UT.pipes[1], -.4, 2.2, -.2, g, 10); cyl(.07, .07, 1.2, M.trim, .3, 2.2, -.2, g, 10);
    cyl(.06, .06, .7, M.metal, -.75, .5, .4, g, 8).rotation.z = Math.PI / 2;
    return { w: 1.8, d: 1.8, tall: true };
  },
  // a main scrubber stack: a banded column with an access panel, sized for one tile
  scrubberStack(g) {
    cyl(.36, .38, 2.3, UT.body, 0, 1.15, 0, g, 20);
    for (const y of [.3, 1.2, 2.1]) cyl(.4, .4, .06, WM.steel, 0, y, 0, g, 20);
    box(.4, .6, .06, UT.filter, 0, .75, .35, g); box(.2, .1, .02, WM.screen, 0, 1.45, .37, g);
    cyl(.18, .18, .6, UT.duct, 0, 2.5, 0, g, 12);
    return { w: .8, d: .8, tall: true };
  },
  // the valve manifold: colour-coded pipes rising from a header, each with its red wheel and a tag
  valveManifold(g, o = {}) {
    const w = o.w || 3.6, n = Math.round(w / .45);
    box(w, .3, .3, WM.paintDark, 0, .55, -.1, g);
    for (let k = 0; k < n; k++) {
      const x = -w / 2 + (k + .5) * w / n, m = UT.pipes[k % 5];
      cyl(.07, .07, H - .7, m, x, (H + .7) / 2, -.12, g, 10);
      const wh = new THREE.Mesh(new THREE.TorusGeometry(.1, .02, 6, 14), UT.wheel); wh.position.set(x, 1.15 + (k % 2) * .25, .08); g.add(wh);
      box(.03, .03, .16, WM.steel, x, 1.15 + (k % 2) * .25, 0, g);
      box(.09, .05, .01, KM.label, x, .9, .06, g);
    }
    box(.5, .3, .04, WM.screen, 0, 1.75, .06, g);
    return { w, d: .6, tall: true };
  },
  // a pressure vessel: a tall rounded tank on a skirt, with a gauge
  pressureTank(g, o = {}) {
    const r = o.r || .7;
    cyl(r * .86, r * .93, .3, WM.paintDark, 0, .15, 0, g, 24);
    cyl(r, r, 1.7, UT.shell, 0, 1.15, 0, g, 24); soft(UT.shell, 0, 2.0, 0, r, .3, r, g);
    cyl(.1, .1, .03, M.trim, 0, 1.4, r, g, 16).rotation.x = Math.PI / 2;
    cyl(.07, .07, .6, ENG.copper, 0, 2.45, 0, g, 8);
    return { w: r * 2 + .1, d: r * 2 + .1, tall: true };
  },
  // a battery bank: two rows of cells with charge bars, bus bars along the top
  batteryBank(g, o = {}) {
    const w = o.w || 1.76;
    box(w, .1, .78, WM.paintDark, 0, .05, 0, g);
    for (let r = 0; r < 2; r++) for (let k = 0; k < 4; k++) {
      const x = -w / 2 + (k + .5) * w / 4, z = -.19 + r * .38;
      box(w / 4 - .06, 1.0, .32, UT.cellCase, x, .6, z, g);
      if (r) box(.06, .7 * (.55 + ((k * 3) % 4) * .15), .02, UT.charge, x, .25 + .35 * (.55 + ((k * 3) % 4) * .15), z + .17, g);
    }
    for (const z of [-.19, .19]) box(w, .04, .06, ENG.copper, 0, 1.13, z, g);
    return { w, d: .78, tall: true };
  },
  // a hover-cart dock: a charging post on a floor plate, and a cart parked on it
  cartDock(g, o = {}) {
    box(1.7, .02, .85, WM.hazard, 0, .01, 0, g);
    box(.2, 1.2, .2, WM.paintDark, 0, .6, -.3, g); box(.16, .1, .03, WM.screen, 0, 1.0, -.19, g);
    const cart = new THREE.Group(); g.add(cart);              // the parked cart, kept whole so it can hide while it's out (cartDockLive)
    box(1.4, .22, .62, UT.cart, 0, .5, .05, cart); box(1.3, .04, .5, UT.cartGlow, 0, .37, .05, cart);
    for (const x of [-.6, .6]) box(.06, .5, .06, WM.steel, x, .85, -.2, cart);
    box(1.26, .05, .05, WM.steel, 0, 1.1, -.2, cart);
    cyl(.02, .02, .4, WM.rubber, .05, .7, -.25, g, 6);
    if (o.dock) { noMergeAll(cart); if (typeof cartDockLive === 'function') cartDockLive(cart, o.dock); }   // section 17 (B3) hides it while the cart is out
    return { w: 1.7, d: .85 };
  },
  // a heavy cargo rack: two levels of crates and drums, fixed pattern
  cargoRack(g) {
    for (const x of [-.9, 0, .9]) box(.08, 1.9, .7, WM.paintGold, x, .95, 0, g);
    for (const y of [.12, 1.0]) box(1.86, .06, .7, WM.paintDark, 0, y, 0, g);
    for (let k = 0; k < 4; k++) {
      const x = -.65 + k * .43 - (k > 1 ? 0 : 0), y = k % 2 ? 1.03 : .15;
      box(.36, .5, .5, KM.crate, -.45 + (k % 2) * .9, y + .25, 0, g);
      cyl(.17, .17, .5, k % 2 ? UT.pipes[1] : UT.pipes[0], .45 - (k % 2) * .9, (k % 2 ? .15 : 1.03) + .25, 0, g, 12);
    }
    return { w: 1.9, d: .7, tall: true };
  },
  // a plain pipe along a wall or ceiling (o.w long, o.r thick, o.m a material)
  pipeLine(g, o = {}) {
    const w = o.w || 1, r = o.r || .08, y = o.y || 2.4;
    cyl(r, r, w, o.m || ENG.copper, 0, y, 0, g, 10).rotation.z = Math.PI / 2;
    for (let x = -w / 2 + .5; x < w / 2; x += 1.5) box(.04, .1, r * 2 + .06, WM.steel, x, y, 0, g);
    return { w, d: r * 2, noBlock: true, tall: true };
  },
});
Object.assign(WALL_KIT, {
  // a valve station on a gallery wall: a short manifold, three wheels and a gauge
  valveStation(g) {
    box(.8, .16, .12, WM.paintDark, 0, 1.0, .08, g);
    for (let k = 0; k < 3; k++) {
      cyl(.05, .05, 1.4, UT.pipes[k], -.25 + k * .25, 1.7, .1, g, 8);
      const wh = new THREE.Mesh(new THREE.TorusGeometry(.08, .016, 6, 12), UT.wheel); wh.position.set(-.25 + k * .25, 1.25, .2); g.add(wh);
    }
    cyl(.07, .07, .03, M.trim, .38, 1.5, .1, g, 14).rotation.x = Math.PI / 2;
  },
});

// ---- Deck 6's utility rooms (0.30.4): the power junctions and the crawlways ----
Object.assign(KIT, {
  // a cable tray along a crawlway wall: a ladder tray with three bundled cables, on brackets (o.w long)
  cableTray(g, o = {}) {
    const w = o.w || 1, y = o.y || 2.3;
    box(w, .03, .32, WM.steel, 0, y, 0, g);
    for (const z of [-.15, .15]) box(w, .07, .02, WM.steel, 0, y + .03, z, g);
    for (let k = 0; k < 3; k++) cyl(.035, .035, w, [UT.pipes[0], WM.rubber, UT.pipes[2]][k], 0, y + .055, -.09 + k * .09, g, 6).rotation.z = Math.PI / 2;
    for (let x = -w / 2 + .5; x < w / 2; x += 1.5) box(.04, .3, .04, WM.paintDark, x, y + .15, -.17, g);
    return { w, d: .34, noBlock: true, tall: true };   // tall: it fades with the cutaway, so it never hides the room behind
  },
});
Object.assign(WALL_KIT, {
  // an inspection box on a crawlway wall: a hinged grey box, cable glands below, two lights and a test socket
  conduitBox(g) {
    box(.5, .6, .16, UT.cab, 0, 1.4, .08, g);
    box(.44, .54, .02, UT.door, 0, 1.4, .17, g);
    for (let k = 0; k < 3; k++) cyl(.03, .03, .4, WM.rubber, -.15 + k * .15, .9, .08, g, 6);
    box(.04, .04, .01, WM.navGreen, -.1, 1.6, .185, g); box(.04, .04, .01, WM.screenAmber, 0, 1.6, .185, g);
    cyl(.035, .035, .02, M.trim, .12, 1.6, .185, g, 10).rotation.x = Math.PI / 2;
    box(.2, .05, .01, KM.label, 0, 1.25, .185, g);
  },
});

// ---- The answers pass (0.30.12): officers' name plates on Deck 4, and lived-in touches in the utility rooms ----
// All made at dress time from shared materials, no R(). Small pieces merge with the room; each sign and calendar is two draw calls at most.
Object.assign(WALL_KIT, {
  // a cabin door plate with its officer's name, and their cabin and role underneath (the same size as 'plate')
  namePlate(g, o) {
    const t = tex(256, 64, (c, w, h) => {
      c.fillStyle = '#0f2a2c'; c.fillRect(0, 0, w, h); c.strokeStyle = '#5fd6c6'; c.lineWidth = 3; c.strokeRect(4, 4, w - 8, h - 8);
      c.textAlign = 'center'; c.fillStyle = '#c5f4ec'; c.font = '600 22px system-ui,sans-serif'; c.fillText(o.text, w / 2, 31, w - 20);
      c.fillStyle = '#7fc9bd'; c.font = '500 14px system-ui,sans-serif'; c.fillText(o.sub, w / 2, 52, w - 20);
    });
    const p = new THREE.Mesh(new THREE.PlaneGeometry(.64, .16), new THREE.MeshBasicMaterial({ map: t, toneMapped: false }));
    p.position.set(0, 1.85, .045); g.add(p); box(.68, .2, .04, M.slateDark, 0, 1.85, .02, g);
  },
  // a paper wall calendar: this month, the days so far crossed off, one ringed (o.ring)
  calendar(g, o = {}) {
    const t = tex(96, 128, (c, w, h) => {
      c.fillStyle = '#f1ece0'; c.fillRect(0, 0, w, h); c.fillStyle = '#b8433a'; c.fillRect(0, 0, w, 22);
      c.fillStyle = '#f1ece0'; c.font = '700 13px system-ui,sans-serif'; c.textAlign = 'center'; c.fillText(o.month || 'MONTH 7', w / 2, 16);
      for (let k = 0; k < 35; k++) {
        const x = 7 + (k % 7) * 12, y = 30 + Math.floor(k / 7) * 19;
        c.fillStyle = '#c9c2b2'; c.fillRect(x, y, 10, 15);
        if (k < (o.upTo || 0)) { c.strokeStyle = '#3b4a52'; c.lineWidth = 1.5; c.beginPath(); c.moveTo(x + 1, y + 1); c.lineTo(x + 9, y + 14); c.moveTo(x + 9, y + 1); c.lineTo(x + 1, y + 14); c.stroke(); }
        if (k === o.ring) { c.strokeStyle = '#b8433a'; c.lineWidth = 2; c.beginPath(); c.arc(x + 5, y + 7.5, 7, 0, Math.PI * 2); c.stroke(); }
      }
    });
    const p = new THREE.Mesh(new THREE.PlaneGeometry(.3, .4), new THREE.MeshStandardMaterial({ map: t, roughness: .9 }));
    p.position.set(0, o.y || 1.5, .012); g.add(p);
  },
});
Object.assign(KIT, {
  // a work radio, left on: a small dark box with a grille, a glowing dial and a bent aerial. Sits on whatever is at o.y.
  radio(g, o = {}) {
    const y = o.y || 0;
    box(.3, .16, .1, M.slateDark, 0, y + .08, 0, g);
    box(.12, .1, .012, WM.steel, -.06, y + .085, .053, g);
    box(.08, .03, .012, WM.screenAmber, .08, y + .12, .053, g);
    cyl(.018, .018, .015, M.metal, .08, y + .06, .056, g, 8).rotation.x = Math.PI / 2;
    const a = cyl(.006, .006, .34, M.metal, .11, y + .3, -.02, g, 4); a.rotation.z = -.35;
    return { w: .3, d: .1, noBlock: true };
  },
  // a mug someone left behind, on whatever is at o.y
  mug(g, o = {}) {
    const y = o.y || 0;
    cyl(.04, .036, .09, M.ceramic, 0, y + .045, 0, g, 12);
    const h = new THREE.Mesh(new THREE.TorusGeometry(.025, .007, 5, 10, Math.PI), M.ceramic); h.position.set(.04, y + .045, 0); h.rotation.z = -Math.PI / 2; g.add(h);
    return { w: .1, d: .08, noBlock: true, tall: !!o.tall };   // tall: it fades with the cabinet it sits on
  },
});

// ---- The answers pass (0.30.12): the Ship health board (machine wear is drawn by section 8b's machineFx) ----
// healthBoard: a wall screen listing the ship's systems and their condition, from section 17's shipHealthRows() (or, until
// that's in, shipSystems() and shipHealth()). Redrawn when the machines change or the ship hour turns; nothing else.
const HEALTH_NAME = { air: 'Air', water: 'Water', power: 'Power', heat: 'Heat', food: 'Food', waste: 'Waste & laundry', hull: 'Hull', comms: 'Comms & sensors', propulsion: 'Propulsion', transport: 'Lift & doors', rec: 'Rec deck' };
function healthRows() {
  if (typeof shipHealthRows === 'function') return shipHealthRows() || [];
  if (typeof shipSystems !== 'function') return [];
  const sys = shipSystems(); return SYSTEMS.map(k => ({ name: HEALTH_NAME[k] || k, value: sys[k] }));
}
function drawHealthBoard(t) {
  const got = healthRows(), ship = got.find(r => r.key === 'ship'), rows = got.filter(r => r.key !== 'ship').slice(0, 10);   // the whole ship is the header
  const { g: c, c: cv } = t.userData, w = cv.width, h = cv.height;
  const all = ship ? ship.value : typeof shipHealth === 'function' && typeof shipSystems === 'function' ? shipHealth() : null;
  const tone = v => v >= 75 ? '#5fd6c6' : v >= 50 ? '#e8c06a' : v >= 25 ? '#e8873a' : '#e0503f';
  c.textAlign = 'left'; c.fillStyle = '#0c1a1f'; c.fillRect(0, 0, w, h);
  c.fillStyle = '#e8c06a'; c.font = '700 24px system-ui,sans-serif'; c.fillText('SHIP HEALTH', 16, 34);
  if (all !== null) { c.textAlign = 'right'; c.fillStyle = tone(all); c.font = '700 24px system-ui,sans-serif'; c.fillText(Math.round(all) + '%', w - 16, 34); c.textAlign = 'left'; }
  c.fillStyle = 'rgba(95,214,198,.35)'; c.fillRect(16, 46, w - 32, 2);
  rows.forEach((r, k) => {
    const y = 58 + k * 38, v = Math.max(0, Math.min(100, +r.value || 0));
    c.fillStyle = '#e8f4f1'; c.font = '600 17px system-ui,sans-serif'; c.fillText(r.name, 16, y + 16, w - 90);
    c.textAlign = 'right'; c.fillStyle = tone(v); c.font = '600 16px system-ui,sans-serif'; c.fillText(Math.round(v) + '%', w - 16, y + 16); c.textAlign = 'left';
    c.fillStyle = '#16303a'; c.fillRect(16, y + 22, w - 32, 8);
    c.fillStyle = tone(v); c.fillRect(16, y + 22, (w - 32) * v / 100, 8);
    const note = r.note || r.worst;                          // section 17's rows name their worst machine
    if (note) { c.fillStyle = '#93b8b2'; c.font = '500 12px system-ui,sans-serif'; c.textAlign = 'right'; c.fillText(note, w - 70, y + 16, w - 200); c.textAlign = 'left'; }
  });
  if (!rows.length) { c.fillStyle = '#7fa9a3'; c.font = '500 18px system-ui,sans-serif'; c.fillText('No readings yet.', 16, 90); }
  t.needsUpdate = true;
}
Object.assign(WALL_KIT, {
  healthBoard(g) {
    const t = tex(320, 440, (c, w, h) => { c.fillStyle = '#0c1a1f'; c.fillRect(0, 0, w, h); });   // portrait: it fits beside the job board
    const p = new THREE.Mesh(new THREE.PlaneGeometry(.74, 1.02), new THREE.MeshBasicMaterial({ map: t, toneMapped: false }));
    p.position.set(0, 1.5, .075); g.add(p);                  // the frame's face is at .065
    box(.84, 1.12, .07, WM.paintDark, 0, 1.5, .03, g);
    box(.84, .05, .1, WM.paintGold, 0, 2.08, .05, g);
    let rev = null, hr = null, wait = 0;
    const redraw = () => { const r = typeof MACH_REV !== 'undefined' ? MACH_REV : 0, q = Math.floor(SHIP.time.min / 60); if (r !== rev || q !== hr) { rev = r; hr = q; drawHealthBoard(t); } };
    redraw();
    MOVERS.push({ place: null, tick(dt) { if ((wait -= dt) > 0) return; wait = 1; redraw(); } });   // a look once a second
  },
});


