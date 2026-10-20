// =====================================================================
// 11. INTERACTION & UI
// =====================================================================
let pickables = [];                                      // what a tap can hit; rebuilt whenever the deck changes
function refreshPickables() { pickables = [floor, wallIM, ...(sillIM ? [sillIM, paneIM] : []), ...HULL_MESHES, ...ITEMS.map(i => i.hit), ...DOOR_OBJS.map(d => d.g), ...crew.map(c => c.obj)]; }
refreshPickables();

const toastEl = document.getElementById('toast'); let toastTimer;
function toast(t, x) {
  TOAST_AT = performance.now();                          // section 15's quiet moments (0.28.48)
  document.getElementById('tt').textContent = t; document.getElementById('tx').textContent = x;
  toastEl.classList.add('show'); clearTimeout(toastTimer); toastTimer = setTimeout(() => toastEl.classList.remove('show'), 5600);
}
document.getElementById('deck').textContent = deckWord(deckDef.num) + ', CSV Wren';
if (SAVED) toast(deckWord(deckDef.num) + ', CSV Wren', welcomeBack());
else toast('Deck 4, CSV Wren', 'You wake in Bunk 1, in the junior wing. Tap to walk somewhere, or press and hold to walk toward your finger. Tap anything or anyone to look closer.');

const marker = new THREE.Mesh(new THREE.RingGeometry(.22, .28, 32), new THREE.MeshBasicMaterial({ color: col('#5fd6c6'), transparent: true, opacity: 0, depthWrite: false, toneMapped: false }));
marker.rotation.x = -Math.PI / 2; marker.position.y = .06; scene.add(marker);
function playerGo(goal, cb) {
  if (!goal || !player.goTo(goal, cb)) return false;
  const p = cellPos(...goal); marker.position.x = p.x; marker.position.z = p.z; marker.material.opacity = .9; marker.scale.setScalar(1);
  return true;
}
// walk up to a thing: the open tile in front of it, then face it
function approach(center, frontAngle, depth, done) {
  const fx = Math.sin(frontAngle), fz = Math.cos(frontAngle);
  const goal = nearestOpen(center.x + fx * (depth / 2 + .55), center.z + fz * (depth / 2 + .55), player);
  const finish = () => { player.face = Math.atan2(center.x - player.obj.position.x, center.z - player.obj.position.z); done(); };
  if (goal && K(goal) === K(player.here()) && !player.path.length) { finish(); return; }
  playerGo(goal, finish);
}
const ray = new THREE.Raycaster(), ndc = new THREE.Vector2(), _wp = new THREE.Vector3();
ray.camera = camera;
function isShown(o) { while (o) { if (!o.visible) return false; o = o.parent; } return true; }
function pick(cx, cy) {
  ndc.set(cx / innerWidth * 2 - 1, -(cy / innerHeight) * 2 + 1); ray.setFromCamera(ndc, camera);
  return ray.intersectObjects(pickables, true).find(h => !h.object.isSprite && !h.object.isPoints && isShown(h.object) && !(h.object.userData.walker && h.object.userData.walker.isPlayer));
}
// the two tiles either side of a door edge, with the angle you face it from: [i, j, angle]
const doorSides = e => e.horiz ? [[e.i, e.j - 1, Math.PI], [e.i, e.j, 0]] : [[e.i - 1, e.j, -Math.PI / 2], [e.i, e.j, Math.PI / 2]];
// stand on whichever side of a door you can reach (north or west first)
function reachableSide(e) {
  const sides = doorSides(e), here = player.here();
  return sides.find(([i, j]) => free(i, j) && (K([i, j]) === K(here) || !!findPath(here, [i, j], null, player))) || sides[0];
}
function tap(cx, cy) {
  if (ride) return;
  if (FREEZE.frozen) { if (!PAUSE.on && PAUSE.tilesTap) PAUSE.tilesTap(); return; }   // nothing on the deck moves while frozen (0.28.50): mid-Tiles, the board comes back
  if (!liftEl.hidden) { closeLiftPanel(); return; }       // a tap outside the panel puts it away
  if (tapCrew(cx, cy)) return;                           // a crew member (section 10)
  const h = pick(cx, cy); if (!h) return;
  const ud = h.object.userData;
  if (ud.walker && ud.walker.active) {
    const who = ud.walker, s = who.spec;
    who.stop(); who.talking = 6; who.faceToward(player); player.faceToward(who);
    toast(s.name, `${DEPT_NAME[s.dept]}, ${RANK_NAME[s.rank]}. ${s.bio}`);
    if (typeof playerChat === 'function') playerChat(s);  // section 15
    return;
  }
  if (ud.item && ud.item.lift) { enterLift(); return; }
  if (ud.item && ud.item.see) { if (typeof jobSpotTap === 'function' && jobSpotTap(h.point)) return; toast(ud.item.t, ud.item.x); return; }   // seen through glass: nothing to walk to (but your job's stop past it: section 15, 0.28.52)
  if (ud.item) {
    const it = ud.item; it.hit.getWorldPosition(_wp);
    if (playerTap(it, _wp.clone(), h.point)) return;     // section 15: eat, shower, work out, call home, shop
    approach(_wp.clone(), it.front, it.depth, () => { if (!offerSleep(_wp)) toast(it.t, it.x); });   // offerSleep: section 13
    return;
  }
  if (ud.liftDoor) { enterLift(); return; }
  if (ud.youLock) { const c = youLockTap(ud.youLock); if (c) { const e = EDGES.get(ud.youLock); approach(new THREE.Vector3(e.cx, 0, e.cz), reachableSide(e)[2], 0, () => toast(c.t, c.x)); return; } }   // 0.47.11
  if (ud.closedDoor) {
    const e = EDGES.get(ud.closedDoor), c = CLOSED_DOORS[ud.closedDoor];
    approach(new THREE.Vector3(e.cx, 0, e.cz), reachableSide(e)[2], 0, () => toast(c.t, c.x));
    return;
  }
  if (typeof playerFloorTap === 'function' && playerFloorTap(h.point)) return;   // section 15: a treadmill, seat or booth with no description of its own
  playerGo(nearestOpen(h.point.x, h.point.z, player));
}

// pointer: tap to walk somewhere, press and hold to walk toward your finger, pinch or wheel to zoom
const pts = new Map(); let downAt = null, pinch0 = 0, zoom0 = 1, steering = false;
const HOLD_MS = 240, HOLD_PX = 14, groundPlane = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0), _gp = new THREE.Vector3();
function endSteer() { steering = false; player.steer = null; }
// called every frame from the main loop
function updateSteer() {
  if (!steering && downAt && pts.size === 1) {
    const [x, y] = pts.values().next().value;
    if (performance.now() - downAt[2] > HOLD_MS || Math.hypot(x - downAt[0], y - downAt[1]) > HOLD_PX) { steering = true; player.stop(); }
  }
  if (!steering) return;
  if (pts.size !== 1) { endSteer(); return; }
  const [x, y] = pts.values().next().value;
  ndc.set(x / innerWidth * 2 - 1, -(y / innerHeight) * 2 + 1); ray.setFromCamera(ndc, camera);
  if (!ray.ray.intersectPlane(groundPlane, _gp)) return;
  const pp = player.obj.position, dx = _gp.x - pp.x, dz = _gp.z - pp.z, d = Math.hypot(dx, dz);
  player.steer = d < .3 ? { x: 0, z: 0, k: 0 } : { x: dx / d, z: dz / d, k: Math.min(1, .45 + (d - .3) * .6) };
  marker.position.x = _gp.x; marker.position.z = _gp.z; marker.material.opacity = Math.max(marker.material.opacity, .45);
}
const cv = renderer.domElement;
const setZoom = z => { camera.zoom = THREE.MathUtils.clamp(z, ZOOM_MIN, ZOOM_MAX); camera.updateProjectionMatrix(); };
cv.addEventListener('pointerdown', e => {
  if (ride) return;
  pts.set(e.pointerId, [e.clientX, e.clientY]);
  if (pts.size === 1) downAt = [e.clientX, e.clientY, performance.now()];
  if (pts.size === 2) { const [a, b] = [...pts.values()]; pinch0 = Math.hypot(a[0] - b[0], a[1] - b[1]); zoom0 = camera.zoom; downAt = null; endSteer(); }
});
cv.addEventListener('pointermove', e => {
  if (pts.has(e.pointerId)) pts.set(e.pointerId, [e.clientX, e.clientY]);
  if (pts.size === 2) { const [a, b] = [...pts.values()]; setZoom(zoom0 * Math.hypot(a[0] - b[0], a[1] - b[1]) / pinch0); }
  else if (!pts.size && e.pointerType === 'mouse') {
    const h = pick(e.clientX, e.clientY), u = h && h.object.userData;
    cv.style.cursor = u && (u.item || u.closedDoor || u.liftDoor || (u.walker && !u.walker.isPlayer)) ? 'pointer' : 'default';
  }
});
const up = e => {
  if (steering) endSteer();
  else if (downAt && pts.size === 1 && Math.hypot(e.clientX - downAt[0], e.clientY - downAt[1]) < HOLD_PX && performance.now() - downAt[2] <= HOLD_MS) { tapUpAt = e.timeStamp; tap(e.clientX, e.clientY); }
  pts.delete(e.pointerId); if (!pts.size) downAt = null;
};
// 0.60.5, the ghost tap (the user: "I click the elevator controls and it selects a floor"): a tap on the deck can open a
// card at once (the lift panel when you're already at it, a conversation). The browser's own click for that same tap
// comes after the pointerup and, on a phone, lands on whatever is now under the finger: a deck button. So for GHOST_MS
// after a tap on the deck, real clicks on anything but the deck are swallowed. Times are the events' own (real) clock;
// scripted clicks (not isTrusted) and keys are never touched.
const GHOST_MS = 350; let tapUpAt = -1e9;
addEventListener('click', e => { if (e.isTrusted && e.target !== cv && e.timeStamp - tapUpAt < GHOST_MS) { e.stopImmediatePropagation(); e.preventDefault(); } }, true);
cv.addEventListener('pointerup', up); cv.addEventListener('pointercancel', e => { pts.delete(e.pointerId); downAt = null; endSteer(); });
cv.addEventListener('contextmenu', e => e.preventDefault());   // long-press must not open a menu
cv.addEventListener('wheel', e => { e.preventDefault(); setZoom(camera.zoom * (e.deltaY > 0 ? .92 : 1.08)); }, { passive: false });

// buttons
const toggle = (btn, on) => { btn.setAttribute('aria-pressed', on); btn.style.opacity = on ? 1 : .55; };
const shadBtn = document.getElementById('shad');
shadBtn.onclick = () => {
  renderer.shadowMap.enabled = !renderer.shadowMap.enabled;
  scene.traverse(o => { if (o.material) [].concat(o.material).forEach(m => m.needsUpdate = true); });
  toggle(shadBtn, renderer.shadowMap.enabled);
};
const crewBtn = document.getElementById('crew'); let crewOn = true;
crewBtn.onclick = () => { crewOn = !crewOn; crew.forEach(c => c.setActive(crewOn && c.deck === deckDef.num)); crowd.visible = crewOn; toggle(crewBtn, crewOn); };
// inner walls: 'auto' drops the ones in your way, 'down' lowers them all, 'up' keeps them all up. The hull has its own rule.
let wallsMode = 'auto', wallsLow = false;
const wallsBtn = document.getElementById('walls');
const WALL_MODES = { auto: ['Walls', 'Walls: auto. Tap for all walls down', 'down'], down: ['Walls down', 'Walls: all down. Tap for all walls up', 'up'], up: ['Walls up', 'Walls: all up. Tap for automatic walls', 'auto'] };
wallsBtn.onclick = () => {
  wallsMode = WALL_MODES[wallsMode][2]; wallsLow = wallsMode === 'down';
  const [label, aria] = WALL_MODES[wallsMode]; wallsBtn.querySelector('span').textContent = label; wallsBtn.setAttribute('aria-label', aria);
};
document.getElementById('rot').onclick = () => { azT += Math.PI / 2; };
const lightBtn = document.getElementById('light');
lightBtn.onclick = debugSkip;                            // a debug control (?debug): section 13
const clockEl = document.getElementById('clock'), roomEl = document.getElementById('room');
function updateClock() {
  const night = nightAt() > .5;
  clockEl.textContent = clockText(); drawClock(hhmm(SHIP.time.min));
  hudFit();
  // too long for its line (0.35.36; 0.28.57, the user's "the clock is cut off" on a phone): a phone always gets the short
  // form, "Day 3 · Wed 06:00"; anything still too long drops to "D3 · Wed 06:00", then "Wed 06:00"
  const wd = WEEKDAYS[weekday(SHIP.time.day)].slice(0, 3), tm = hhmm(SHIP.time.min), rg = document.createRange();
  const hs = getComputedStyle(hudEl), room = parseFloat(hs.maxWidth) - parseFloat(hs.paddingLeft) - parseFloat(hs.paddingRight) - parseFloat(hs.borderLeftWidth) - parseFloat(hs.borderRightWidth);
  const over = () => { rg.selectNodeContents(clockEl); return isFinite(room) ? rg.getBoundingClientRect().width > room - 1 : clockEl.scrollWidth > clockEl.clientWidth + 1; };   // the text's exact width against the widest the box may grow, a pixel to spare (0.28.59: scrollWidth rounds, so a cut-off by a fraction of a pixel read as a fit)
  const phone = typeof matchMedia === 'function' && matchMedia('(max-width:720px),(max-height:500px)').matches;
  // (0.28.59: a larger system font, Android's text size in the Claude app) a slightly smaller clock before the day goes
  clockEl.style.fontSize = '';
  const D = SHIP.time.day, steps = [['Day ' + D + ' · ' + wd + ' ' + tm], ['D' + D + ' · ' + wd + ' ' + tm], ['D' + D + ' · ' + wd + ' ' + tm, '11px'], [wd + ' ' + tm, '11px']];
  for (const [t, f] of steps) { if (!phone && !over()) break; clockEl.textContent = t; if (f) clockEl.style.fontSize = f; if (!over()) break; }
  hudBelow();
  lightBtn.querySelector('span').textContent = night ? 'Day' : 'Night';
  lightBtn.setAttribute('aria-label', night ? 'Debug: sleep until 07:40' : 'Debug: skip to 21:40');
}
// 0.35.39 (reviewer 2b): the place and clock may use all the room up to the nearest button beside them (8px clear),
// measured on resize and each minute; the CSS caps stay as the fallback
const hudEl = document.querySelector('.hud');
// the Device button, Pause and the needs strip sit under the place-and-clock box (0.28.59): when a large system font makes
// the box taller than usual, they move down with it (at the usual sizes nothing moves)
function hudBelow() {
  const db = document.getElementById('devBtn'); if (!hudEl || !db) return;
  db.style.top = ''; const ns = document.getElementById('needStrip'); if (ns) ns.style.top = '';
  const gap = hudEl.getBoundingClientRect().bottom + 6 - db.getBoundingClientRect().top;
  if (gap > 0) db.style.top = Math.ceil(db.getBoundingClientRect().top + gap) + 'px';
  const ng = ns ? db.getBoundingClientRect().bottom + 8 - ns.getBoundingClientRect().top : 0;   // and the strip under a taller Device button
  if (ng > 0) ns.style.top = Math.ceil(ns.getBoundingClientRect().top + ng) + 'px';
  if (typeof pausePlace === 'function') pausePlace();
}
function hudFit() {
  if (!hudEl) return; hudEl.style.maxWidth = '';
  const h = hudEl.getBoundingClientRect(); let right = innerWidth - 12;
  for (const b of document.querySelectorAll('.controls button')) { if (!b.offsetWidth) continue; const r = b.getBoundingClientRect(); if (r.top < h.bottom + 4 && r.left > h.left) right = Math.min(right, r.left - 8); }
  hudEl.style.maxWidth = Math.max(120, Math.floor(right - h.left)) + 'px';
}
updateClock();
addEventListener('resize', () => updateClock());          // 0.35.36: the clock's length follows the screen's width
let lastRoom = null;

// ---- changing decks: you step out by the lift on deck n. The lift will call this (milestone step 6c). ----
const deckEl = document.getElementById('deck');
function goToDeck(n, at) {
  if (n === 7 && !REC_DECK) return;                      // the rec deck is dormant (REC_DECK)
  endSteer(); player.stop();
  for (const c of crew) c.setActive(false);
  deckCrewClear();
  unloadDeck(); buildDeck(DECKS[n]); indexRoomTiles();
  player.deck = n;
  // at: where you stood in the lift car on the old deck. Decks line up, so it's the same spot in this deck's car.
  if (at && free(...cellAt(at.x, at.z))) player.obj.position.set(at.x, 0, at.z);
  else { const c = nearestOpen(LIFT_AT[0], LIFT_AT[1], player); if (c) player.obj.position.copy(cellPos(c[0], c[1])); }
  for (const w of crew) if (w.deck === n && crewOn) w.setActive(true);
  deckCrewFill();                                        // section 10: the scheduled crew on this deck
  target.copy(player.obj.position).setY(.7);
  refreshPickables(); deckEl.textContent = deckWord(n) + ', CSV Wren'; lastRoom = null;
  marker.material.opacity = 0; applyLight(nightT);
  saveGame();                                            // section 13: save on every deck change
}

// ---- the main lift: tap a lift door for the deck panel. A ride opens the doors, you step in, they close,
// the view fades, the new deck is built behind the black, and the doors open on it. Timed by the game clock. ----
const DECK_NAMES = { 1: 'Bridge', 2: 'Officers\' quarters and science',   /* 0.72.5 (playtest 2, item 18): was 'Command & Science' */ 3: 'Commons', 4: 'Quarters', 5: 'Operations', 6: 'Engineering', 7: 'Recreation' };
const liftEl = document.getElementById('lift'), liftList = document.getElementById('liftList'), fadeEl = document.getElementById('fade');
let ride = null, liftReturn = null;
const inLift = () => roomAt(...player.here()) === '@';
const liftDoors = () => DOOR_OBJS.filter(d => d.e.type === 'lift');
// The panels: one on the car's back wall in front of its east column, and (0.38.26, the user's) one on the front wall in
// front of its west column. Tapping a lift door or a panel walks you in and up to the nearer one, then opens the deck list.
// Choosing a deck: you reach out and press, and the ride starts. panelTiles() -> [[i, j, x, z], ...]: each panel's tile
// and the point on the wall you face (world); panelTile() -> the nearer panel's tile (null with no car)
const panelTiles = () => { const b = ROOM_BOX['@']; return b ? [[b.i0 + 1, b.j0, X0(b.i0) + 1.5, Z0(b.j0)], [b.i0, b.j1, X0(b.i0) + .5, Z0(b.j1) + 1]] : []; };
function panelNear() {
  const p = player.obj.position, l = panelTiles();
  return l.length ? l.slice().sort((a, b) => Math.hypot(a[2] - p.x, a[3] - p.z) - Math.hypot(b[2] - p.x, b[3] - p.z)) : [];
}
const panelTile = () => { const l = panelNear(); return l.length ? [l[0][0], l[0][1]] : null; };
let panelAt = null;                                      // the panel you're going to (for facing it)
function facePanel() { const p = player.obj.position, pn = panelAt || panelNear()[0]; if (pn) player.face = Math.atan2(pn[2] - p.x, pn[3] - p.z); }
function toPanel(done) {
  const here = player.here(), l = panelNear(); if (!l.length) return;
  const at = () => { facePanel(); done(); };
  for (const pn of l) {                                  // the nearer panel, else the other if someone's at it
    const pt = [pn[0], pn[1]]; panelAt = pn;
    if (K(pt) === K(here) && !player.path.length) { at(); return; }
    if (free(...pt) && !occupiedBy(player).has(K(pt)) && findPath(here, pt, null, player)) { playerGo(pt, at); return; }
  }
  const pt = [l[0][0], l[0][1]]; panelAt = l[0];
  // someone's at both panels: the free car tile nearest the nearer one, and reach from there
  const tiles = (ROOM_TILES['@'] || []).filter(c => K(c) === K(here) || findPath(here, c, null, player));
  if (!tiles.length) return;
  const goal = tiles.sort((a, b) => Math.hypot(a[0] - pt[0], a[1] - pt[1]) - Math.hypot(b[0] - pt[0], b[1] - pt[1]))[0];
  if (K(goal) === K(here) && !player.path.length) at(); else playerGo(goal, at);
}
function enterLift() {
  if (ride) return;
  if (typeof roofLiftTap === 'function' && roofLiftTap()) return;   // 24s: the lift roof job (Thursdays 15:30-16:30), or the car held for it
  toPanel(openLiftPanel);
}
function pressPanel(n) {
  toPanel(() => { player.press = { t: 0, fired: false, cb: () => startRide(n) }; });
}
function openLiftPanel() {
  liftReturn = document.activeElement; liftList.textContent = '';
  for (const n of DECK_ORDER) {                         // R (the rec deck) between 4 and 5 (0.80.0)
    const here = n === deckDef.num, built = !!DECKS[n], b = document.createElement('button');
    b.className = 'deckbtn' + (here ? ' here' : ''); b.disabled = here || !built;
    const i = document.createElement('i'), sp = document.createElement('span'), t = document.createElement('b'), sm = document.createElement('small');
    i.textContent = deckLabel(n); t.textContent = DECK_NAMES[n]; sm.textContent = here ? 'You are here' : built ? DECKS[n].blurb : 'Not built yet';
    sp.append(t, sm); b.append(i, sp);
    const gl = typeof goalNow === 'function' ? goalNow() : null, goal = !!(gl && gl.deck === n && !here && built);   // 0.28.58 (0.60.6a, the user's): the deck your goal arrow wants
    if (goal) { b.classList.add('goal'); const g = document.createElement('em'); g.textContent = '→ Goal'; b.appendChild(g); }
    b.setAttribute('aria-label', `${deckWord(n)}, ${DECK_NAMES[n]}: ${sm.textContent}` + (goal ? '. Your goal is here' + (gl.label ? ': ' + gl.label : '') : ''));
      b.onclick = () => { closeLiftPanel(); pressPanel(n); };
    liftList.appendChild(b);
  }
  liftEl.hidden = false; toastEl.classList.remove('show');
  (liftList.querySelector('button.goal') || liftList.querySelector('button:not(:disabled)') || document.getElementById('liftStay')).focus();   // the goal's deck first (0.28.58)
}
function closeLiftPanel() { liftEl.hidden = true; if (liftReturn && liftReturn.focus) liftReturn.focus(); }
document.getElementById('liftStay').onclick = closeLiftPanel;
addEventListener('keydown', e => { if (e.key === 'Escape' && !liftEl.hidden) closeLiftPanel(); });
function startRide(n) {
  if (!inLift()) return;
  endSteer(); player.stop(); toastEl.classList.remove('show');
  ride = { n, t: 0, at: player.obj.position.clone(), face: player.face, swapped: false };
}
// seconds along a ride: the doors close, the view fades, the new deck is built behind the black, it fades back, the doors open
const RIDE = { shut: .55, dark: .95, light: 1.35, done: 1.8 };
function updateRide(dt) {
  const r = ride; r.t += dt; const T_ = r.t;
  for (const d of liftDoors()) d.force = T_ >= RIDE.light && r.swapped ? 1 : 0;
  if (!r.swapped) {
    fadeEl.style.opacity = THREE.MathUtils.clamp((T_ - RIDE.shut) / (RIDE.dark - RIDE.shut), 0, 1);
    if (T_ >= RIDE.dark) {
      goToDeck(r.n, r.at); player.face = player.obj.rotation.y = r.face;
      for (const d of liftDoors()) { d.open = 0; d.force = 0; }
      r.swapped = true;
    }
  } else {
    fadeEl.style.opacity = THREE.MathUtils.clamp(1 - (T_ - RIDE.dark) / (RIDE.light - RIDE.dark), 0, 1);
    if (T_ >= RIDE.done) {
      for (const d of liftDoors()) delete d.force;      // back to opening for whoever's near
      fadeEl.style.opacity = 0; ride = null;
      toast(deckWord(deckDef.num) + ', ' + deckDef.name, deckDef.arrive || '');
    }
  }
}
// ---- the car held for maintenance (M17, seat E4 on the lift owner's behalf, 0.53.9; plans/mechanics/m17-lift-roof.html).
// liftHold(on, until?): from now till `until` (absolute ship minutes; default an hour) nobody can call the car (the panel
// stays shut: enterLift asks 24s first); liftHold(false) lets it go at once. liftHeld(t?) -> is it held at ship minute t
// (default now): section 14's whereIs asks it (crew who need another deck wait by the lift till it's let go). The hold
// is kept after its end, so replays over that hour see it; not saved (a load lets it go). var, not let: section 14 may
// ask before this line has run
var LIFT_HOLD = null;
function liftHold(on, until) { LIFT_HOLD = on ? { from: shipNow(), until: Number.isFinite(until) ? until : shipNow() + 60 } : LIFT_HOLD && liftHeld() ? { ...LIFT_HOLD, until: shipNow() } : LIFT_HOLD; return liftHeld(); }
function liftHeld(t) { if (!LIFT_HOLD) return false; if (!Number.isFinite(t)) t = shipNow(); return t >= LIFT_HOLD.from && t < LIFT_HOLD.until; }

// =====================================================================
// 12. MAIN LOOP
// =====================================================================
const HRUN_EDGES = { of: null, n: -1, list: [] };          // 0.27.31: see the wall cut below
const clock = new THREE.Clock(); let scrT = 0;
function loop() {
  const dt = Math.min(clock.getDelta(), .05), t = clock.elapsedTime;
  const run = !freezeSync();                             // section 15's pause (0.28.48) and a game of Tiles (0.28.50): nothing moves and ship time stands still; the view still draws
  if (!run) clock.elapsedTime -= dt;                     // the frame clock too, so poses and blinks carry on where they stopped (0.28.50)
  if (run) {
  updateSteer();
  // 0.27.32: the per-frame loops here count through their arrays (a for...of here made an iterator result every step, about 600 a frame)
  for (let k = 0; k < walkers.length; k++) if (walkers[k].active) walkers[k].update(dt, t);
  playerUpdate(dt, t);                                   // section 15: needs, walking speed, activities
  updateDeckCrew(dt);                                    // section 10: the scheduled crew
  crowd.update(dt, t);
  if (REC_CREW_ROPES) recCrewRopes();                    // 0.84.6: the crew's belay lines, on the posed bodies (8c)
  if (REC_JUGGLE.m || REC_JUGGLE.n) recCrewBalls();      // 0.84.9: a juggler's balls (8c)
  simTimers();                                           // section 13's simTimeout (0.28.50)
  }
  shadowStep();                                          // 0.27.33: the shadow stand-ins, a slice a frame after a deck change

  // camera follows you
  az += (azT - az) * Math.min(1, dt * 6);
  const pp = typeof ACT !== 'undefined' && ACT && ACT.o && ACT.o.follow && ACT.body && ACT.phase === 'do' ? { x: ACT.x, z: ACT.z } : player.obj.position;   // 0.80.8: a rec deck activity that moves you round the room (floating, paddling) takes the camera with it
  target.x += (pp.x - target.x) * Math.min(1, dt * 3); target.z += (pp.z - target.z) * Math.min(1, dt * 3);
  placeCam(); placeSun(target);

  // cutaway: wall runs between the camera and you drop to knee height, a whole run at a time
  const cx = Math.sin(az), cz = Math.cos(az), k7 = Math.min(1, dt * 7);
  // a run drops if any part of it stands in front of you and near your line of sight
  const rx = Math.cos(az), rz = -Math.sin(az);
  const hides = e => (e.cx - pp.x) * cx + (e.cz - pp.z) * cz > .25 && Math.abs((e.cx - pp.x) * rx + (e.cz - pp.z) * rz) < 3.5;
  // the hull: pieces facing the camera (lower and right on screen) stay low, the far ones (upper and left) stay up
  for (let k = 0; k < RUNS.length; k++) { const r = RUNS[k]; r.cut = r.face ? r.face[0] * cx + r.face[1] * cz > 0
    : wallsMode === 'up' ? false : wallsLow || (r.out && r.out[0] * cx + r.out[1] * cz > .3) || r.edges.some(hides); }
  for (let k = 0; k < edgeList.length; k++) { const e = edgeList[k]; e.s += ((e.run.cut ? .12 : 1) - e.s) * k7; }
  for (let k = 0; k < CURVES.length; k++) { const c = CURVES[k]; if (c.run) { c.s += ((c.run.cut ? .12 : 1) - c.s) * k7; c.g.scale.y = c.s; } }
  for (let k = 0; k < POSTS.length; k++) { const p = POSTS[k]; let m = -Infinity; for (let i = 0; i < p.touch.length; i++) m = Math.max(m, p.touch[i].s); p.s = m; }   // 0.27.31: no array each frame
  writeWalls();
  for (let k = 0; k < HULL_RUNS.length; k++) { const hr = HULL_RUNS[k]; hr.s += ((hr.cut ? .12 : 1) - hr.s) * k7; hr.g.scale.y = hr.s; hr.decor.visible = hr.s > .9; }
  if (HRUN_EDGES.of !== EDGES || HRUN_EDGES.n !== EDGES.size) { HRUN_EDGES.of = EDGES; HRUN_EDGES.n = EDGES.size; HRUN_EDGES.list = [...EDGES.values()].filter(e => e.hrun); }
  for (let k = 0, L = HRUN_EDGES.list; k < L.length; k++) L[k].s = L[k].hrun.s;       // 0.27.31: the edges that follow a hull run, listed once per deck (was a Map walk each frame)
  for (let k = 0; k < DOOR_OBJS.length; k++) DOOR_OBJS[k].g.scale.y = DOOR_OBJS[k].e.s;
  for (let k = 0; k < TALL.length; k++) {               // tall furniture fades when it would hide you
    const t = TALL[k]; let hides = false;
    for (let j = 0; j < t.pts.length && !hides; j++) { const p = t.pts[j], dep = (p.x - pp.x) * cx + (p.z - pp.z) * cz; hides = dep > .3 && dep < 4.5 && Math.abs((p.x - pp.x) * rx + (p.z - pp.z) * rz) < .5 + p.w / 2; }
    const goal = !wallsLow && hides ? .22 : 1;
    if (Math.abs(t.o - goal) < .002) continue;
    t.o += (goal - t.o) * k7; if (Math.abs(t.o - goal) < .01) t.o = goal;
    const fade = t.o < .99;
    for (let j = 0; j < t.mats.length; j++) {
      const m = t.mats[j]; m.opacity = m.userData.base.op * t.o; m.depthWrite = !fade;
      const tr = fade || m.userData.base.tr; if (m.transparent !== tr) { m.transparent = tr; m.needsUpdate = true; }
    }
  }
  for (let k = 0; k < WALL_DECOR.length; k++) { const d = WALL_DECOR[k]; d.g.visible = d.e ? d.e.s > .9 : true; }
  for (let k = 0; k < VOID_BLOCKS.length; k++) {
    const v = VOID_BLOCKS[k];
    const b = v.m.geometry.boundingBox || (v.m.geometry.computeBoundingBox(), v.m.geometry.boundingBox);
    const dep = (x, z) => (v.cx + x - pp.x) * cx + (v.cz + z - pp.z) * cz, near = Math.max(dep(b.min.x, b.min.z), dep(b.max.x, b.min.z), dep(b.min.x, b.max.z), dep(b.max.x, b.max.z));
    v.s += ((wallsLow || (wallsMode === 'auto' && near > .25) ? .12 : 1) - v.s) * k7; v.m.scale.y = v.s;
  }

  if (run && ride) updateRide(dt);
  // doors slide open for anyone nearby (lift doors only when a ride opens them, and they drop into the floor)
  for (let k = 0; k < DOOR_OBJS.length; k++) {
    const d = DOOR_OBJS[k], crewAt = d.force === undefined && crewNearDoor(d);   // section 10: crew open doors (and their own locked ones)
    if (!d.passable && !d.svc && d.force === undefined && d.open < 1e-4 && !crewAt) continue;
    let walk = false; if (d.force === undefined && !crewAt && (d.passable || d.svc)) for (let j = 0; j < walkers.length && !walk; j++) { const w = walkers[j]; walk = w.active && !youLock(d.e.key, w) && Math.hypot(w.obj.position.x - d.cx, w.obj.position.z - d.cz) < 1.15 + (d.span - SEG) / 2; }
    const near = d.force !== undefined ? d.force > 0 : crewAt || walk;
    d.open += ((near ? 1 : 0) - d.open) * Math.min(1, dt * (d.force !== undefined ? 5 : d.svc ? 4 : 8));   // a service hatch is heavier
    if (d.e.type === 'lift') for (let j = 0; j < d.leaves.length; j++) { const l = d.leaves[j]; l.position.y = 1.1 - d.open * 2.3; l.visible = d.open < .995; }   // lift doors sink into the floor
    else for (let j = 0; j < d.leaves.length; j++) d.leaves[j].position.x = (j ? 1 : -1) * (d.span / 4 + d.open * d.span / 2 * .92);
  }

  if (REC_SHOW.state || REC_SHOW.dim || REC_SHOW.scr) recShowTick(dt, t);   // 0.84.8: the auditorium's show (8c); nothing while there's none
  nightT += (nightAt() - nightT) * Math.min(1, dt * 1.8); applyLight(nightT);
  doorLeavesSync(); tallSync();                          // section 4: door leaves (0.27.21) and tall furniture (0.27.22), drawn together
  if (typeof machineFx !== 'undefined') { machineFx.lamps(t); shipFeelFrame(t, dt); }   // section 8b: lamps stutter while the deck's light relays flicker (0.27.10); a ship-wide event's feel (0.27.19)

  // ambient life
  // stars outside: the sky drifts aft across the screen, with a touch of parallax as the camera follows you.
  // Windows are open to it, so the stars you see through them are the same ones.
  {
    const ax = -_r.x, ay = -_u.x, l = Math.hypot(ax, ay) || 1, wpp = (camera.top - camera.bottom) / camera.zoom / innerHeight;
    const v = dt * SKY.speed / l, px = target.dot(_r) / wpp, py = target.dot(_u) / wpp, U = SKY.mat.uniforms;
    SKY.far.x = (SKY.far.x - ax * v * 7) % 512; SKY.far.y = (SKY.far.y - ay * v * 7) % 512;
    SKY.near.x = (SKY.near.x - ax * v * 18) % 512; SKY.near.y = (SKY.near.y - ay * v * 18) % 512;
    U.uFar.value.set(SKY.far.x + px * .03, SKY.far.y + py * .03); U.uNear.value.set(SKY.near.x + px * .08, SKY.near.y + py * .08);
    U.uPR.value = renderer.getPixelRatio();
  }
  if (run) for (const D_ of DUST) {                       // still while frozen (0.28.54, reviewer 1f)
    const a = D_.geo.attributes.position.array;
    for (let i = 0; i < D_.n; i++) { a[i * 3 + 1] += Math.sin(t * .3 + D_.seeds[i]) * .0015; a[i * 3] += Math.cos(t * .2 + D_.seeds[i]) * .001; }
    D_.geo.attributes.position.needsUpdate = true;
  }
  for (let k = 0; k < SPINS.length; k++) { const sp = SPINS[k]; sp.o.rotation[sp.ax] += sp.w * dt; }
  if (MOVERS.length && run) { const pb = typeof placeBusy === 'function' ? placeBusy : null; for (let k = 0; k < MOVERS.length; k++) MOVERS[k].tick(dt, !!(pb && pb(MOVERS[k].place))); }   // section 10's placeBusy
  for (const p of PULSES) p.m[p.key] = p.base + p.amp * (.5 + .5 * Math.sin(t * p.w + p.ph));
  for (let q = 0; q < STEAM.length; q++) { const s = STEAM[q], k = (t * .35 + s.i / 3) % 1; s.s.position.y = s.y + k * .45; s.s.position.x = s.x + Math.sin(t + s.i * 2) * .03; s.s.material.opacity = Math.sin(k * Math.PI) * .22; s.s.scale.setScalar(.1 + k * .18); }
  marker.material.opacity *= 1 - dt * 2.2; marker.scale.setScalar(1 + (1 - marker.material.opacity) * .3);
  scrT += dt; if (scrT > .1) { scrT = 0; drawScreen(t); }
  if (run) {
  tickShip(dt);                                          // section 13: the ship's clock
  galleyTick();                                          // section 16: the galley, on paper and on Deck 3
  worksTick();                                           // section 17: the Works bay job board
  eventsTick();                                          // section 18: the ship's events (Mail, decor, joining in)
  socialTick();                                          // section 20: the crew's social life, on paper
  if (typeof introTick === 'function') introTick();      // section 21: the arrival evening (nothing with the intro off)
  if (typeof worksCareerTick === 'function') worksCareerTick();   // section 24: your Works career (the ladder, training moments)
  }
  const r = roomAt(...player.here()); if (r && r !== lastRoom) { lastRoom = r; roomEl.textContent = ROOMS[r].name; if (typeof recRoomIn === 'function') recRoomIn(r); }

  discFrame();                                           // section 23b: a game of Lightdisc on the court (0.82.0), frozen or not
  camera.updateMatrixWorld(); bubbles.place();           // 0.47.9: the speech bubbles, with this frame's camera (they shook on phones)
  renderer.render(scene, DISC.cam || camera);
  requestAnimationFrame(loop);
}
drawScreen(0); applyLight(0); loop();
