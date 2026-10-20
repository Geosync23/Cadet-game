/* =====================================================================
   STARSHIP CADET: CSV Wren                           build 0.64.2
   Cozy starship life sim. Single file, three.js r128, no image assets.

   FILE MAP
    1. SETUP            renderer, scene, seeded random
    2. TEXTURES         every texture is drawn in code (canvas)
    3. MATERIALS        shared materials and small mesh helpers
    4. DECK             art kit, deck builder, deck definitions (DECKS)
    5. LIGHTING         lights plus day and night presets
    6. CAMERA           isometric orthographic camera, pixel-snapped
    7. GRID             tile grid and A* pathfinding
    8. CHARACTER KIT    makeCharacter(spec), leg IK, walk animation
    8b. CROWD           crowd.add(spec): many crew in a few draw calls; ?crowd=40 demo
    9. CREW DATA        one line per crew member
   10. WALKERS          movement, yielding, room-based crew brain
   11. INTERACTION/UI   tapping, toasts, buttons
   12. MAIN LOOP
   13. SHIP TIME & SAVE the clock, day and night, saving (sits after 5)
   14. SCHEDULES        planDay, whereIs: where all the crew are (after 13)
   15. PLAYER NEEDS     needs, activities, walking speed, the device (after 14)
   15b. INTERACTIONS    more places to use, the job board, the goal pointer (after 15)
   16. GALLEY & FOOD    the galley rota, cooking, the servery, plates (after 14)
   17. MACHINES & JOBS  machines, wear, systems, ship health, effects on people (after 14)
   19. DEVICE           your device: apps (deviceApp) and the skin that draws them (before 15)
   24. WORK             your Works career: the ladder, training, tools, reputation (after 23)

   RULES THAT KEEP IT WORKING ON PHONES
   - Never let two surfaces share a plane. Overlap solids instead, or keep
     faces at least 0.005 apart. Coplanar faces flicker on mobile GPUs.
   - Colours are written as sRGB hex and passed through col().
   - 1 unit = 1 floor tile. Rooms sit on a tile grid; furniture blocks tiles.
   ===================================================================== */
// =====================================================================
// 1. SETUP
// =====================================================================
let W = 0, D = 0, OX = 0, OZ = 0;         // the current deck's size in tiles, and where its tile (0,0) sits in the world (set by buildDeck)
let H = 2.8, WALL_K = 1; const T = 0.2;   // wall height and thickness; H is 2.8 × the deck's `tall` (the rec deck's double-height walls, 0.80.0), set by buildDeck
const col = h => new THREE.Color(h).convertSRGBToLinear();
const small = Math.min(innerWidth, innerHeight) < 700;

const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false, powerPreference: 'high-performance' });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.setSize(innerWidth, innerHeight);
renderer.outputEncoding = THREE.sRGBEncoding;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.05;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
document.body.appendChild(renderer.domElement);
const scene = new THREE.Scene();
scene.background = new THREE.Color('#151d2c');
const maxAniso = renderer.capabilities.getMaxAnisotropy();

let seed = 11;
const R = () => (seed = (seed * 16807) % 2147483647) / 2147483647;

// =====================================================================
// 2. TEXTURES (procedural)
// =====================================================================
function tex(w, h, draw, rx = 1, ry = 1, srgb = true) {
  const c = document.createElement('canvas'); c.width = w; c.height = h;
  const g = c.getContext('2d'); draw(g, w, h);
  const t = new THREE.CanvasTexture(c);
  t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(rx, ry);
  if (srgb) t.encoding = THREE.sRGBEncoding;
  t.anisotropy = maxAniso;
  t.userData = { g, c };
  return t;
}
function grain(g, w, h, amt) {
  const d = g.getImageData(0, 0, w, h), p = d.data;
  for (let i = 0; i < p.length; i += 4) { const n = (R() - .5) * amt; p[i] += n; p[i + 1] += n; p[i + 2] += n; }
  g.putImageData(d, 0, 0);
}

const wallTex = tex(128, 360, (g, w, h) => {
  const u = h / H;
  g.fillStyle = '#b2bcb7'; g.fillRect(0, 0, w, h);
  const gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, 'rgba(255,255,255,.07)'); gr.addColorStop(1, 'rgba(0,0,0,.06)');
  g.fillStyle = gr; g.fillRect(0, 0, w, h);
  const wy = h - 0.9 * u;
  g.fillStyle = '#56656f'; g.fillRect(0, wy, w, h - wy);
  for (let y = wy + 14; y < h - 6; y += 16) { g.fillStyle = 'rgba(0,0,0,.2)'; g.fillRect(0, y, w, 2); g.fillStyle = 'rgba(255,255,255,.06)'; g.fillRect(0, y + 2, w, 1); }
  g.fillStyle = '#36434b'; g.fillRect(0, wy - 7, w, 7); g.fillStyle = 'rgba(255,255,255,.2)'; g.fillRect(0, wy - 7, w, 1.5);
  g.fillStyle = 'rgba(45,55,60,.55)'; g.fillRect(0, 0, 2, wy - 7); g.fillStyle = 'rgba(255,255,255,.35)'; g.fillRect(2, 0, 1, wy - 7);
  const hs = h - 2.0 * u; g.fillStyle = 'rgba(45,55,60,.45)'; g.fillRect(0, hs, w, 2); g.fillStyle = 'rgba(255,255,255,.3)'; g.fillRect(0, hs + 2, w, 1);
  g.fillStyle = '#8f9b9b'; g.fillRect(0, 0, w, 0.16 * u);
  g.fillStyle = 'rgba(60,70,76,.5)';
  [[10, hs - 10], [w - 10, hs - 10], [10, hs + 12], [w - 10, hs + 12]].forEach(([x, y]) => { g.beginPath(); g.arc(x, y, 2, 0, 7); g.fill(); });
  grain(g, w, h, 9);
});

function fabric(base, line, step, diag) {
  return tex(256, 256, (g, w, h) => {
    g.fillStyle = base; g.fillRect(0, 0, w, h);
    g.globalAlpha = .08;
    for (let y = 0; y < h; y += 2) { g.fillStyle = y % 4 ? '#000' : '#fff'; g.fillRect(0, y, w, 1); }
    g.globalAlpha = 1;
    if (line) {
      g.strokeStyle = line; g.lineWidth = 2; g.setLineDash([6, 4]);
      for (let k = -h; k < w + h; k += step) {
        g.beginPath();
        if (diag) { g.moveTo(k, 0); g.lineTo(k + h, h); g.moveTo(k + h, 0); g.lineTo(k, h); }
        else { g.moveTo(0, k); g.lineTo(w, k); }
        g.stroke();
      }
    }
    grain(g, w, h, 16);
  });
}
const blanketTex = fabric('#2d5d72', 'rgba(220,240,240,.28)', 64, true); blanketTex.repeat.set(2, 2);
const creamTex = fabric('#ece4d4', null);
const mustardTex = fabric('#c99642', 'rgba(255,240,200,.25)', 32, false);
const tealFabTex = fabric('#2b8a83', null);
const plumTex = fabric('#56466a', 'rgba(255,255,255,.12)', 40, false);

const woodTex = tex(256, 64, (g, w, h) => {
  g.fillStyle = '#8a5b3d'; g.fillRect(0, 0, w, h);
  for (let i = 0; i < 26; i++) {
    g.strokeStyle = `rgba(${R() < .5 ? '60,35,20' : '170,120,80'},${.15 + R() * .25})`; g.lineWidth = .5 + R() * 1.5;
    const y0 = R() * h, a = R() * 4; g.beginPath(); g.moveTo(0, y0);
    for (let x = 0; x <= w; x += 16) g.lineTo(x, y0 + Math.sin(x / 40 + i) * a);
    g.stroke();
  }
  grain(g, w, h, 10);
});

function makeRug([base, a, b, c]) {
  return tex(320, 260, (g, w, h) => {
    g.fillStyle = base; g.fillRect(0, 0, w, h);
    const band = (i, col, lw) => { g.strokeStyle = col; g.lineWidth = lw; g.strokeRect(i, i, w - 2 * i, h - 2 * i); };
    band(10, a, 8); band(22, b, 2); band(30, c, 3);
    g.save(); g.beginPath(); g.rect(40, 40, w - 80, h - 80); g.clip();
    for (let x = 40; x < w; x += 30) for (let y = 40; y < h; y += 30) {
      g.fillStyle = ((x + y) / 30) % 2 < 1 ? a : c; g.globalAlpha = .82;
      g.beginPath(); g.moveTo(x + 15, y + 4); g.lineTo(x + 26, y + 15); g.lineTo(x + 15, y + 26); g.lineTo(x + 4, y + 15); g.closePath(); g.fill();
      g.globalAlpha = 1; g.fillStyle = base; g.beginPath(); g.moveTo(x + 15, y + 10); g.lineTo(x + 20, y + 15); g.lineTo(x + 15, y + 20); g.lineTo(x + 10, y + 15); g.closePath(); g.fill();
    }
    g.restore();
    g.globalAlpha = .1; for (let y = 0; y < h; y += 2) { g.fillStyle = '#000'; g.fillRect(0, y, w, 1); } g.globalAlpha = 1;
    grain(g, w, h, 22);
  });
}
function makeChartPoster(bg, accent, title) {
  return tex(200, 280, (g, w, h) => {
    g.fillStyle = bg; g.fillRect(0, 0, w, h);
    for (let i = 0; i < 60; i++) { g.fillStyle = `rgba(255,255,255,${R() * .6})`; g.fillRect(R() * w, R() * 220, 1.5, 1.5); }
    g.strokeStyle = accent; g.lineWidth = 2; g.beginPath();
    for (let k = 0; k < 6; k++) { const x = 25 + k * 30, y = 60 + Math.sin(k * 1.7) * 50 + 60; k ? g.lineTo(x, y) : g.moveTo(x, y); }
    g.stroke();
    g.strokeStyle = 'rgba(255,255,255,.2)'; g.lineWidth = 1; g.strokeRect(10, 10, w - 20, 220);
    g.fillStyle = '#e8efe9'; g.font = '600 14px system-ui,sans-serif'; g.fillText(title, 16, 254);
  });
}
const glowTex = tex(64, 64, (g, w, h) => {
  const r = g.createRadialGradient(32, 32, 0, 32, 32, 32);
  r.addColorStop(0, 'rgba(255,255,255,1)'); r.addColorStop(.25, 'rgba(255,255,255,.55)'); r.addColorStop(1, 'rgba(255,255,255,0)');
  g.fillStyle = r; g.fillRect(0, 0, w, h);
}, 1, 1, false);
const fadeTex = tex(8, 64, (g, w, h) => {
  const r = g.createLinearGradient(0, 0, 0, h); r.addColorStop(0, 'rgba(255,255,255,.9)'); r.addColorStop(1, 'rgba(255,255,255,0)');
  g.fillStyle = r; g.fillRect(0, 0, w, h);
}, 1, 1, false);
const blobTex = tex(64, 64, (g) => {
  const r = g.createRadialGradient(32, 32, 0, 32, 32, 32);
  r.addColorStop(0, 'rgba(0,0,0,.55)'); r.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = r; g.fillRect(0, 0, 64, 64);
}, 1, 1, false);
// nebulaTex and starTex are no longer shown (windows look at the real sky), but drawing them keeps R()'s sequence
const nebulaTex = tex(512, 256, (g, w, h) => {
  const bg = g.createLinearGradient(0, 0, 0, h); bg.addColorStop(0, '#070b1f'); bg.addColorStop(1, '#1b1338');
  g.fillStyle = bg; g.fillRect(0, 0, w, h);
  [[120, 80, 140, 'rgba(60,170,170,.28)'], [300, 200, 180, 'rgba(160,70,170,.22)'], [420, 60, 120, 'rgba(70,90,200,.25)']].forEach(([x, y, r, c]) => {
    const n = g.createRadialGradient(x, y, 0, x, y, r); n.addColorStop(0, c); n.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = n; g.fillRect(0, 0, w, h);
  });
  const px = 350, py = 165, pr = 62;
  const p = g.createRadialGradient(px - 25, py - 25, 5, px, py, pr);
  p.addColorStop(0, '#f6c47a'); p.addColorStop(.6, '#c7783c'); p.addColorStop(1, '#5a2a1e');
  g.fillStyle = p; g.beginPath(); g.arc(px, py, pr, 0, 7); g.fill();
  g.save(); g.beginPath(); g.arc(px, py, pr, 0, 7); g.clip();
  g.globalAlpha = .25; g.strokeStyle = '#ffe2b0';
  for (let i = -3; i <= 3; i++) { g.lineWidth = 3; g.beginPath(); g.ellipse(px, py + i * 16, pr, 6, 0, 0, 7); g.stroke(); }
  g.globalAlpha = 1;
  const sh = g.createRadialGradient(px + 40, py + 40, 10, px + 30, py + 30, pr * 1.2);
  sh.addColorStop(0, 'rgba(5,5,20,.85)'); sh.addColorStop(1, 'rgba(5,5,20,0)'); g.fillStyle = sh; g.fillRect(0, 0, w, h);
  g.restore();
  g.strokeStyle = 'rgba(255,200,140,.35)'; g.lineWidth = 3; g.beginPath(); g.arc(px, py, pr + 2, Math.PI * .9, Math.PI * 1.6); g.stroke();
}, 1, 1, true);
const starTex = tex(512, 256, (g, w, h) => {
  for (let i = 0; i < 260; i++) {
    const s = R() < .08 ? 1.6 : .7 + R() * .6;
    g.fillStyle = `rgba(255,255,255,${.35 + R() * .65})`; g.beginPath(); g.arc(R() * w, R() * h, s, 0, 7); g.fill();
  }
}, 1, 1, true);

const posterTex = tex(200, 280, (g, w, h) => {
  g.fillStyle = '#16223d'; g.fillRect(0, 0, w, h);
  for (let i = 0; i < 70; i++) { g.fillStyle = `rgba(255,255,255,${R() * .7})`; g.fillRect(R() * w, R() * 220, 1.5, 1.5); }
  const pts = [[30, 190], [62, 150], [95, 160], [120, 110], [150, 120], [172, 60]];
  g.strokeStyle = '#59d4c4'; g.lineWidth = 2; g.setLineDash([5, 4]); g.beginPath(); pts.forEach(([x, y], i) => i ? g.lineTo(x, y) : g.moveTo(x, y)); g.stroke(); g.setLineDash([]);
  pts.forEach(([x, y], i) => { g.fillStyle = i === pts.length - 1 ? '#f2b45e' : '#cfeeea'; g.beginPath(); g.arc(x, y, i === pts.length - 1 ? 6 : 3.5, 0, 7); g.fill(); });
  g.strokeStyle = 'rgba(207,238,234,.25)'; g.lineWidth = 1; g.strokeRect(10, 10, w - 20, 220);
  g.fillStyle = '#e8efe9'; g.font = '600 15px system-ui,sans-serif'; g.fillText('Wren survey route', 16, 254);
  g.fillStyle = '#8aa3b0'; g.font = '11px system-ui,sans-serif'; g.fillText('Frontier tour, year one', 16, 270);
});

const lockerTex = tex(140, 210, (g, w, h) => {
  g.fillStyle = '#4b5861'; g.fillRect(0, 0, w, h);
  g.fillStyle = 'rgba(0,0,0,.35)'; g.fillRect(w / 2 - 1, 6, 2, h - 12);
  g.strokeStyle = 'rgba(0,0,0,.3)'; g.lineWidth = 2; g.strokeRect(5, 5, w - 10, h - 10);
  g.fillStyle = '#2a9d8f'; g.fillRect(5, 22, w - 10, 6);
  g.fillStyle = '#c9d2d2'; g.fillRect(w / 2 - 12, h * .48, 4, 22); g.fillRect(w / 2 + 8, h * .48, 4, 22);
  for (let i = 0; i < 5; i++) { g.fillStyle = 'rgba(0,0,0,.3)'; g.fillRect(14, 40 + i * 6, 40, 2); g.fillRect(w - 54, 40 + i * 6, 40, 2); }
  grain(g, w, h, 10);
});
const doorTex = tex(120, 220, (g, w, h) => {
  g.fillStyle = '#4f5d66'; g.fillRect(0, 0, w, h);
  g.fillStyle = 'rgba(0,0,0,.4)'; g.fillRect(w / 2 - 1.5, 0, 3, h);
  g.fillStyle = '#5fd6c6'; g.fillRect(w / 2 - 22, h * .45, 4, 36); g.fillRect(w / 2 + 18, h * .45, 4, 36);
  g.strokeStyle = 'rgba(255,255,255,.12)'; g.lineWidth = 2; g.strokeRect(8, 8, w / 2 - 14, h - 16); g.strokeRect(w / 2 + 6, 8, w / 2 - 14, h - 16);
  grain(g, w, h, 8);
});

const screenTex = tex(256, 160, () => {}, 1, 1, true);
function drawScreen(t) {
  const { g } = screenTex.userData, w = 256, h = 160;
  g.fillStyle = '#0b2629'; g.fillRect(0, 0, w, h);
  g.fillStyle = '#134347'; g.fillRect(0, 0, w, 24);
  g.fillStyle = '#c5f4ec'; g.font = '600 13px system-ui,sans-serif'; g.fillText('Duty board', 10, 16);
  g.fillStyle = '#6fb8ae'; g.font = '11px system-ui,sans-serif'; g.fillText('Day shift', 190, 16);
  const rows = ['Service galley oven', 'Replace corridor lamp', 'Restock scrubber filters'];
  rows.forEach((r, i) => {
    const y = 42 + i * 22;
    g.strokeStyle = '#5fd6c6'; g.lineWidth = 1.5; g.strokeRect(10, y - 9, 10, 10);
    if (i === 0) { g.fillStyle = '#5fd6c6'; g.fillRect(12.5, y - 6.5, 5, 5); }
    g.fillStyle = i === 0 ? '#7da7a2' : '#d6efeb'; g.font = '11px system-ui,sans-serif'; g.fillText(r, 28, y);
  });
  g.strokeStyle = 'rgba(95,214,198,.25)'; g.strokeRect(10, 108, w - 20, 42);
  g.strokeStyle = '#5fd6c6'; g.lineWidth = 2; g.beginPath();
  for (let x = 0; x <= w - 24; x += 3) {
    const y = 129 + Math.sin(x * .07 + t * 3) * 9 * Math.sin(x * .013 + t * .7) + Math.sin(x * .23 - t * 5) * 2;
    x ? g.lineTo(12 + x, y) : g.moveTo(12 + x, y);
  }
  g.stroke();
  screenTex.needsUpdate = true;
}
const clockTex = tex(128, 48, () => {}, 1, 1, true);
function drawClock(s) {
  const { g } = clockTex.userData;
  g.fillStyle = '#081014'; g.fillRect(0, 0, 128, 48);
  g.fillStyle = '#ffb35c'; g.font = '600 30px system-ui,sans-serif'; g.textAlign = 'center'; g.fillText(s, 64, 35);
  clockTex.needsUpdate = true;
}

// =====================================================================
// 3. MATERIALS & HELPERS
// =====================================================================
const std = (c, r = .7, m = 0, extra = {}) => new THREE.MeshStandardMaterial(Object.assign({ color: col(c), roughness: r, metalness: m }, extra));
const M = {
  slate: std('#45525b', .55, .25), slateDark: std('#2b343b', .75, .15), trim: std('#d4dad6', .5, .1),
  cream: new THREE.MeshStandardMaterial({ map: creamTex, roughness: .95 }),
  wood: new THREE.MeshStandardMaterial({ map: woodTex, roughness: .5 }),
  blanket: new THREE.MeshStandardMaterial({ map: blanketTex, roughness: .95 }),
  plum: new THREE.MeshStandardMaterial({ map: plumTex, roughness: .95 }),
  mustard: new THREE.MeshStandardMaterial({ map: mustardTex, roughness: .95 }),
  tealFab: new THREE.MeshStandardMaterial({ map: tealFabTex, roughness: .95 }),
  ceramic: std('#e6e0d3', .35, 0), leaf: std('#4c8a57', .7, 0), leaf2: std('#6ba86a', .7, 0),
  metal: std('#a4aeb4', .3, .75), glass: std('#cfe8ee', .1, 0, { transparent: true, opacity: .32 }),
  dark: std('#161c21', .4, .3),
};
const box = (w, h, d, mat, x, y, z, p = scene) => { const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mat); m.position.set(x, y, z); m.castShadow = m.receiveShadow = true; p.add(m); return m; };
const cyl = (rt, rb, h, mat, x, y, z, p = scene, seg = 24) => { const m = new THREE.Mesh(new THREE.CylinderGeometry(rt, rb, h, seg), mat); m.position.set(x, y, z); m.castShadow = m.receiveShadow = true; p.add(m); return m; };
const soft = (mat, x, y, z, sx, sy, sz, p = scene) => { const m = new THREE.Mesh(new THREE.SphereGeometry(1, 24, 16), mat); m.scale.set(sx, sy, sz); m.position.set(x, y, z); m.castShadow = m.receiveShadow = true; p.add(m); return m; };
const glows = [];
function glow(c, size, x, y, z, p = scene, op = .8) {
  const m = new THREE.SpriteMaterial({ map: glowTex, color: col(c), transparent: true, opacity: op, blending: THREE.AdditiveBlending, depthWrite: false });
  const s = new THREE.Sprite(m); s.scale.set(size, size, 1); s.position.set(x, y, z); p.add(s); glows.push(s); return s;
}

