// =====================================================================
// DECK 6: ENGINEERING (step 6e: turn 1 the shell, turn 2 the engine room, turn 3 the reactor and engine control,
// turn 4 the watch room, the lobby and the deck's warm light; 0.11.0 the engine room opened, the watch room moved and enlarged)
// From plans/deck6-plan.html. The bottom of the ship: the engine room fills the flat stern, the reactor the bow,
// with the foot of the spine, the overlook, the watch room and engine control between. No windows anywhere.
// The engine room is open through the overlook; engine control and the reactor are locked rooms you look into through glass.
// =====================================================================
DECKS[6] = {
  num: 6, name: 'Engineering', seed: 60661, hazard: true,
  blurb: 'Engine room, reactor, power junctions', arrive: 'The overlook is aft, onto the engine room. Engine control and the reactor are forward. Mind the heat.',
  lift: [19, 6],
  // car rows 4-6, trunks row 3 above it, ladder row 7: the same world spot as every deck. The spine ends here.
  map: [
    '..EEEEEEEEEEcccccccccccccccRRRRR....',
    '..EEEEEEEEEEOOOO++++++jjjjjRRRRRRR..',
    '..EEEEEEEEEEOOOO++++++jjjjjRRRRRRRR.',
    '..EEEEEEEEEEOOOO++YY+++++++RRRRRRRR.',
    '..EEEEEEEEEEOOOO++@@++KKKKKRRRRRRRRR',
    '..EEEEEEEEEEOOOO++@@++KKKKKRRRRRRRRR',
    '..EEEEEEEEEEOOOO++@@++KKKKKRRRRRRRRR',
    '..EEEEEEEEEESSSS++ZZ++KKKKKRRRRRRRRR',
    '..EEEEEEEEEESSSS++++++++JJJRRRRRRRR.',
    '..EEEEEEEEEESSSS++++++++JJJRRRRRRRR.',
    '..EEEEEEEEEESSSS++++++++JJJRRRRRRR..',
    '..EEEEEEEEEECCCCCCCCCCCCCCCRRRRR....',
  ],
  // doors, in game edge keys. door: open to all. closed: shut, with tap text. hatch: service access.
  // glass: an inner window. lift: the main lift (one wide door each side).
  doors: {
    'v,18,4': 'lift', 'v,18,5': 'lift', 'v,18,6': 'lift', 'v,20,4': 'lift', 'v,20,5': 'lift', 'v,20,6': 'lift',   // one wide door each side
    'h,18,3': 'glass', 'h,19,3': 'glass',                     // the foot of the trunks, behind glass above the car
    'h,18,8': 'hatch', 'h,19,8': 'glass',                     // the bottom of the ladder, with its hatch
    'v,16,5': 'door', 'v,16,6': 'door', 'v,16,4': 'glass',  // onto the overlook
    'v,12,1': 'glass', 'v,12,2': 'glass', 'v,12,3': 'glass', 'v,12,4': 'glass', 'v,12,6': 'glass',   // the overlook's window onto the engine room...
    'v,12,5': 'door',                                                            // ...and the door down onto the coil floor
    'v,16,9': 'door', 'v,16,7': 'glass', 'v,16,8': 'glass',   // the watch room, off the lobby, with glass onto it...
    'v,12,7': 'glass', 'v,12,8': 'glass', 'v,12,9': 'glass', 'v,12,10': 'glass',   // ...and its own window onto the coils
    'v,22,5': 'closed', 'v,22,4': 'glass', 'v,22,6': 'glass', // engine control, glass onto the lobby
    'v,27,4': 'glass', 'v,27,5': 'glass', 'v,27,6': 'glass', 'v,27,7': 'glass', // engine control's window onto the reactor
    'v,27,3': 'closed',                                       // the reactor's shielded door, at the end of the lobby's alcove
    'h,17,1': 'hatch', 'h,17,11': 'hatch',                    // down into the port and starboard crawlways
    'v,22,2': 'hatch', 'v,24,9': 'hatch',                     // the two power junctions, both off the lobby
  },
  // which room each shut door or hatch leads into (its tap text is that room's 'tap')
  sealed: { 'v,22,5': 'K', 'v,27,3': 'R' },
  plates: [['v,16,3', 'e', 'Overlook'], ['v,22,7', 'w', 'Engine control'], ['v,16,10', 'e', 'Watch room'], ['h,23,3', 's', 'Junction'], ['h,26,4', 'n', 'Reactor']],
  rooms: {
    '+': { name: 'Lift lobby', floor: 'lobby', hall: true },
    '@': { name: 'Main lift', floor: 'lift' },
    Y: { name: 'Spine trunks', floor: 'grate', spine: true }, Z: { name: 'Spine ladder', floor: 'grate', spine: true },
    O: { name: 'Engine overlook', floor: 'steel' },
    S: { name: 'Engine watch room', floor: 'wood' },
    E: { name: 'Engine room', floor: 'grate' },
    // locked, but seen through glass
    K: { name: 'Engine control', floor: 'plate', tap: 'Engine control. Tier 3 access, once power work opens. You can see the board through the glass.' },
    R: { name: 'Reactor', floor: 'grate', tap: 'The reactor\'s shielded door, with radiation trefoils painted either side. Tier 4 access, and only on a team job.' },
    // utility rooms (Pillar 2, 0.30.4): floors that draw no random numbers, so the rest of the deck is unchanged
    c: { name: 'Port crawlway', floor: 'grate', still: true },
    C: { name: 'Starboard crawlway', floor: 'grate', still: true },
    j: { name: 'Port power junction', floor: 'plate', still: true },
    J: { name: 'Starboard power junction', floor: 'plate', still: true },
  },
  windows: [],
  closedDoors: {
    'h,18,8': { t: 'Spine ladder', x: 'The bottom of the maintenance ladder. It runs the whole height of the ship from here to the bridge. Tier 2 access.' },
  },
  hull: { sternX: 2, stern: 1, bowFrom: 27, bowLen: 8.6, byFace: true },   // flat stern with tight corners for the drive, a short blunt bow; one hull piece per facing (0.27.3: was 234 pieces)
  // service hatches into the utility rooms (0.30.4): the player and Works crew pass (see hatchPassable)
  service: [{ key: 'h,17,1', tier: 3 }, { key: 'h,17,11', tier: 3 }, { key: 'v,22,2', tier: 3 }, { key: 'v,24,9', tier: 3 }],   // crawlways and junctions, tier 3 (0.30.12)
  crawl: [0, 11].flatMap(j => Array.from({ length: 15 }, (_, k) => (12 + k) + ',' + j)),   // (0.30.12) the crawlways' tiles: crouch-walk here
  // machines (Pillar 2; format as on Deck 4): wall-mounted ones have `at` on their panel tile
  machines: [
    { id: '6-junction-1', kind: 'junction', at: [24, 1], room: 'j', face: 's', panel: [24, 2], look: { lamp: [0.5, 1.2, 0.13], drip: [0.5, 0.9, 0.18] } },
    { id: '6-junction-2', kind: 'junction', at: [26, 9], room: 'J', face: 'w', panel: [25, 9], look: { lamp: [0, 1.2, 0.13], drip: [0, 0.9, 0.18] } },
    { id: '6-conduit-1', kind: 'conduit', at: [22, 0], room: 'c', face: 's', panel: [22, 0] },
    { id: '6-conduit-2', kind: 'conduit', at: [22, 11], room: 'C', face: 'n', panel: [22, 11] },
  ],
  // places (Pillar 1): every spot where a crew member does something, for the schedules. Data only: nothing draws them.
  // { id, type, at: [col, row], face, pose, room }. Seats and beds sit on furniture tiles and are reached from the tile beside them;
  // face is the way the person faces there. deck_check.py checks every place can be reached.
  places: [
    { id: '6-control-1', type: 'work:engine', at: [25, 5], face: 'e', pose: 'sit', room: 'K', xy: [25.42, 5.37], y: 0.5 },
    { id: '6-control-2', type: 'work:engine', at: [25, 6], face: 'e', pose: 'sit', room: 'K', xy: [25.58, 6.63], y: 0.5 },
    { id: '6-watch-1', type: 'work:engine', at: [12, 8], face: 'w', pose: 'sit', room: 'S', xy: [13.01, 8.1], y: 0.44, cush: 0.44 },
    { id: '6-watch-2', type: 'work:engine', at: [12, 9], face: 'w', pose: 'sit', room: 'S', xy: [13.01, 9.9], y: 0.44, cush: 0.44 },
    { id: '6-engine-1', type: 'work:engine', at: [4, 4], face: 's', pose: 'work', room: 'E' },
    { id: '6-engine-2', type: 'work:engine', at: [7, 7], face: 'n', pose: 'work', room: 'E' },
    { id: '6-engine-3', type: 'work:engine', at: [3, 8], face: 'w', pose: 'work', room: 'E' },
    { id: '6-bench-1', type: 'bench', at: [14, 3], face: 'w', pose: 'sit', room: 'O', xy: [14.4, 3.5], y: 0.48 },
    { id: '6-bench-2', type: 'bench', at: [18, 10], face: 'n', pose: 'sit', room: '+' },
    { id: '6-bench-3', type: 'bench', at: [22, 8], face: 's', pose: 'sit', room: '+', xy: [22.5, 8.4], y: 0.48 },
    { id: '6-bench-4', type: 'bench', at: [23, 8], face: 's', pose: 'sit', room: '+', xy: [23.5, 8.4], y: 0.48 },
    { id: '6-lift-1', type: 'lift-wait', at: [16, 3], face: 'e', pose: 'stand', room: '+' },
    { id: '6-lift-2', type: 'lift-wait', at: [16, 7], face: 'e', pose: 'stand', room: '+' },
    { id: '6-lift-3', type: 'lift-wait', at: [21, 3], face: 'w', pose: 'stand', room: '+' },
    { id: '6-lift-4', type: 'lift-wait', at: [21, 7], face: 'w', pose: 'stand', room: '+' },
    // utility rooms (0.30.4): one work:works place on each machine's panel tile, facing the machine
    { id: '6-junction-1-svc', machine: '6-junction-1', type: 'work:works', at: [24, 2], face: 'n', pose: 'work', room: 'j' },
    { id: '6-junction-2-svc', machine: '6-junction-2', type: 'work:works', at: [25, 9], face: 'e', pose: 'work', room: 'J' },
    { id: '6-conduit-1-svc', machine: '6-conduit-1', type: 'work:works', at: [22, 0], face: 'n', pose: 'work', room: 'c' },
    { id: '6-conduit-2-svc', machine: '6-conduit-2', type: 'work:works', at: [22, 11], face: 's', pose: 'work', room: 'C' },
  ],
  markings: [[3, 4, 8, 4]],                                     // keep-clear round the row of coils
  light: { sky: col('#ffd2a6'), sun: col('#ffc48c'), hemi: .8, sunI: .78 },   // warmer and dimmer than the decks above
  dress(d) {
    for (const [key, tw, text] of d.plates) placeOnEdge('plate', key, tw, { text });
    for (const [key, tw] of [['v,18,7', 'w'], ['v,20,7', 'e']]) placeOnEdge('liftPanel', key, tw);
    placeOnEdge('deckDirectory', 'v,16,8', 'e', { it: IT('Deck directory', 'Seven decks, top to bottom. Bridge, Command & Science, Commons, Quarters, the Recreation Deck (R), Operations, Engineering. You are here: Engineering, the bottom of the line.') });
    // the foot of the spine: the trunks start behind glass above the car, the ladder ends behind glass below it
    for (const r of ['Y', 'Z', 'K', 'R']) NO_FADE.add(r);             // the locked rooms behind glass stay solid
    place('Y', 'spineTrunks', 1, .5, 'n', { it: { t: 'Foot of the trunks', x: 'The power and air trunks start their climb here, insulated and warm to the touch through the glass. Everything every deck runs on goes up these.', see: true } });
    place('Z', 'spineLadder', 1, .5, 'n', { it: SPINE_IT.ladder });
    // the engine room, through the door from the overlook: the drive housing across the stern, three drive coils down
    // the middle cycling one after another behind a rail, copper feeds between them, and open aisles either side.
    // Room-local: the coils block rows 5-6 from x 1 to 8; rows 1-4 and 7-10 and column 9 (inside the door) stay clear.
    place('E', 'driveHousing', .55, 6, 'w', { w: 8.6, it: IT('The drive', 'The drive housing fills the whole stern. Its mouth glows as the coils feed it, and the deck hums in time.') });
    ['The first coil takes the reactor\'s power and starts the cycle.', 'The middle coil. Its windings were replaced last refit; you can tell by the brighter copper.', 'The last coil, nearest the window. When all three glow in turn, the drive is happy.']
      .forEach((x, k) => place('E', 'driveCoil', 2.6 + k * 2.5, 6, 'n', { ph: -k * 2.1, it: IT('Drive coil ' + (k + 1), x) }));
    for (const x of [1.4, 3.85, 6.35]) place('E', 'pipeRun', x, 6, 'n', { w: 1.0, y: 2.4 });
    for (const z of [4.85, 7.15]) place('E', 'overlookRail', 5.1, z, 'n', { w: 7.6 });   // a rail either side of the coils
    // the overlook: a rail along the window, open at the engine room door; a bench facing the coils; the first-week board
    place('O', 'overlookRail', .2, 2.0, 'w', { w: 3.7 }); place('O', 'overlookRail', .2, 5.5, 'w', { w: .8 });
    place('O', 'bench', 2.3, 2.5, 'e', { snug: true, it: IT('Bench', 'Facing the coils. People come down here to think, because nobody can hear you over the hum.') });
    placeWall('O', 'notices', 'n', 2.0, { hitW: 1.0, it: IT('First week', 'A list of names under COME AND SEE THE ENGINE. Every new crew member is on it. Yours has been added in pencil.') });
    // the reactor fills the bow, seen through engine control's window: the shield drum and its coolant loop
    place('R', 'reactorDrum', 4.4, 6, 'n', { loop: 3.0, it: { t: 'The reactor', x: 'The core sits inside that drum, behind more shielding than anything else aboard. The green glow is the safe kind. Everyone says so, a bit too quickly.', see: true } });
    // engine control: the board along the reactor window, two chairs facing it, and the mimic panel of the ship's power
    place('K', 'controlBoard', 4.45, 2, 'e', { w: 3.4, it: { t: 'Engine control board', x: 'Reactor output, coil temperatures, coolant flow and the drive, all on one desk. One of the amber lights has been amber for a week, and someone has taped a note to it: KNOWN.', see: true } });
    for (const z of [1.2, 2.8]) place('K', 'chair', 3.4, z, 'w');
    placeWall('K', 'mimicPanel', 'n', 2.5, { hitW: 3.0, it: { t: 'Mimic panel', x: 'The whole ship\'s power on one board: the reactor, both junctions and a line up to every deck. Deck 3\'s line is amber; the galley ovens are drawing hard.', see: true } });
    // the reactor door at the end of the alcove: a radiation sign either side
    for (const [key, tw] of [['h,26,3', 's'], ['h,26,4', 'n']]) placeOnEdge('trefoil', key, tw, { it: IT('Radiation sign', 'Painted either side of the reactor\'s shielded door. Tier 4, and only ever on a team job.') });
    // the watch room (4 x 4, the overlook's south end): two armchairs and a tea table at the window onto the coils,
    // the kettle in the corner, a lamp, a panel heater nobody needs and a shelf of old engine logs. The door is on the lobby side.
    place('S', 'rug', 1.9, 2.0, 'n', { tex: rugLounge, w: 2.8, d: 3.0 });
    place('S', 'armchair', .9, 1.1, 'e', { fab: M.mustard, it: IT('Armchair', 'The engine watch\'s chair, facing the coils. From here you can see every one of them and hear them through the floor.') });
    place('S', 'armchair', .9, 2.9, 'e', { fab: M.mustard, it: IT('Armchair', 'Worn in exactly one place. Whoever has the night watch sits here.') });
    place('S', 'teaTable', .7, 2.0, 'n', { it: IT('Tea table', 'Two mugs and a watch log, open at tonight. The coils on the other side of the glass do most of the talking.') });
    place('S', 'dispenser', 3.55, .35, 'n', { it: IT('Kettle', 'Hot water on tap, a tin of tea and a mug for every Works tech who ever stood a watch.') });
    place('S', 'floorLamp', 3.6, 3.6, 'n', { light: true });
    placeWall('S', 'heater', 's', 2.0, { hitW: 1.0, it: IT('Heater', 'Switched on, on the warmest deck in the ship. Nobody knows why; nobody turns it off.') });
    placeWall('S', 'logShelf', 'n', 1.0, { hitW: .9, it: IT('Engine logs', 'Years of watch logs in grey and gold binders. One entry, underlined: QUIET NIGHT. COILS SANG.') });
    // the lobby: coolant risers in its corners (steaming at a joint), and a bench facing the lift
    for (const [x, z] of [[.35, .35], [5.65, .35], [.35, 9.65], [7.65, 9.65]]) place('+', 'coolantRiser', x, z, 'n', { it: IT('Coolant riser', 'Coolant on its way up from the reactor loop. Warm to the touch, and the reason this lobby never needs a heater.') });
    place('+', 'bench', 2.5, 9.55, 's', { snug: true, it: IT('Bench', 'Warm, because everything down here is. People wait here for the lift and doze off.') });
    place('+', 'bench', 7.0, 7.3, 'n', { snug: true, it: IT('Bench', 'Under engine control\'s wall. You can hear the operators arguing about coolant through it.') });
    // ---- utility rooms (Pillar 2, 0.30.4). Last in dress() and free of R(), so nothing above them changes ----
    // the power junctions: a row of breaker cabinets in each, where the reactor's power splits for the decks above
    place('j', 'breakerCabinet', 3.0, .345, 'n', { w: 3.76, it: IT('Main breakers, port', 'Where the reactor\'s power splits for the decks above. Four cabinets, one per pair of decks, and a spare that hums.') });
    place('J', 'breakerCabinet', 2.66, 1.5, 'e', { w: 2.76, it: IT('Main breakers, starboard', 'The second junction: if the port side trips, this one carries the ship. Every label is laminated twice.') });
    placeWall('j', 'workLight', 's', 3.5); placeWall('J', 'workLight', 'n', 1.5);
    // the crawlways: cable trays along the hull, and an inspection box halfway along
    for (let x = 1.5; x < 15; x += 3) { place('c', 'cableTray', x, .3, 'n', { w: 3 }); place('C', 'cableTray', x, .7, 'n', { w: 3 }); }   // in short pieces, so the one near you fades the run
    placeWall('c', 'conduitBox', 'n', 10.5, { it: IT('Inspection box', 'Halfway along the port crawlway. Open it and you can test every feed to the decks above.') });
    placeWall('C', 'conduitBox', 's', 10.5, { it: IT('Inspection box', 'Halfway along the starboard crawlway. Someone has left a torch on top of it, still on.') });
    // lived-in touches (0.30.12): a mug on the port breakers, a sign in the starboard junction
    place('j', 'mug', 1.2, .3, 'n', { y: 1.995, tall: true });
    placeWall('J', 'plate', 'n', .6, { text: 'Sign in, sign out' });
  },
};
for (const [key, r] of Object.entries(DECKS[6].sealed)) DECKS[6].closedDoors[key] = { t: DECKS[6].rooms[r].name, x: DECKS[6].rooms[r].tap };

// ---- Deck 1 kit (made at load, no R()). Kept in its own block: materials in BRG, pieces added to KIT and WALL_KIT ----
const BRG = {
  duct: std('#7f9aa3', .4, .45),
  // the brass plate on the trunk head
  trunkPlate: new THREE.MeshBasicMaterial({ toneMapped: false, map: tex(256, 96, (c, w, h) => {
    c.fillStyle = '#b8913e'; c.fillRect(0, 0, w, h); c.strokeStyle = '#6e5420'; c.lineWidth = 5; c.strokeRect(5, 5, w - 10, h - 10);
    c.fillStyle = '#3a2c12'; c.font = '700 26px system-ui,sans-serif'; c.textAlign = 'center'; c.fillText('CSV WREN', w / 2, 40);
    c.font = '600 18px system-ui,sans-serif'; c.fillText('TRUNK HEAD  ·  DECK 1', w / 2, 72);
    for (const x of [16, w - 16]) for (const y of [16, h - 16]) { c.beginPath(); c.arc(x, y, 4, 0, Math.PI * 2); c.fill(); }
  }, 1, 1) }),
  // the viewscreen: deep space with a soft nebula and a far planet. Stars come from a fixed hash, not R().
  // It wraps sideways and scrolls slowly (the offset is turned through SPINS, see bridgeViewscreen).
  sky: new THREE.MeshBasicMaterial({ toneMapped: false, map: tex(1024, 256, (c, w, h) => {
    const gr = c.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, '#060a16'); gr.addColorStop(.5, '#0b1428'); gr.addColorStop(1, '#070b18');
    c.fillStyle = gr; c.fillRect(0, 0, w, h);
    for (const [x, y, r, col_] of [[180, 120, 150, 'rgba(90,70,160,.22)'], [330, 150, 110, 'rgba(60,140,170,.16)'], [700, 90, 170, 'rgba(150,70,120,.14)'], [880, 170, 120, 'rgba(70,110,190,.16)']])
      for (const dx of [-w, 0, w]) { const n = c.createRadialGradient(x + dx, y, 0, x + dx, y, r); n.addColorStop(0, col_); n.addColorStop(1, 'rgba(0,0,0,0)'); c.fillStyle = n; c.fillRect(x + dx - r, y - r, r * 2, r * 2); }
    let s = 1101; const hash = () => (s = (s * 48271) % 2147483647) / 2147483647;
    for (let k = 0; k < 520; k++) { const x = hash() * w, y = hash() * h, b = hash(), r = b > .96 ? 1.6 : b > .8 ? 1.1 : .7;
      c.fillStyle = b > .9 ? '#fff4dc' : b > .6 ? '#dfe9ff' : 'rgba(200,215,255,.6)'; c.beginPath(); c.arc(x, y, r, 0, Math.PI * 2); c.fill(); }
    const px = 610, py = 150, pr = 34, pg = c.createRadialGradient(px - 12, py - 12, 4, px, py, pr);
    pg.addColorStop(0, '#d7b98a'); pg.addColorStop(.7, '#8a6a4a'); pg.addColorStop(1, '#2a1f18'); c.fillStyle = pg; c.beginPath(); c.arc(px, py, pr, 0, Math.PI * 2); c.fill();
    c.strokeStyle = 'rgba(230,210,170,.45)'; c.lineWidth = 2; c.beginPath(); c.ellipse(px, py, pr * 1.8, pr * .35, -.25, 0, Math.PI * 2); c.stroke();
    c.strokeStyle = 'rgba(95,214,198,.18)'; c.lineWidth = 1; for (let y = 0; y < h; y += 4) { c.beginPath(); c.moveTo(0, y + .5); c.lineTo(w, y + .5); c.stroke(); }   // faint scan lines
  }) }),
  bezel: std('#1e252c', .45, .35),
  // the command ring and stations
  leather: std('#8e2f2c', .5, .05), leatherDark: std('#3a3f48', .55, .05), frame: std('#2a3138', .4, .55), console: std('#252d35', .5, .35),
  brass: std('#c9a24a', .35, .75), stepGlow: std('#9ff3e6', .4, 0, { emissive: col('#5fd6c6'), emissiveIntensity: 1.1 }),
};
// station screens, drawn at load from fixed numbers (no R()): a title bar in the station's colour over a readout
function stationScreen(title, hue, kind) {
  return new THREE.MeshBasicMaterial({ toneMapped: false, map: tex(256, 160, (c, w, h) => {
    c.fillStyle = '#0b141b'; c.fillRect(0, 0, w, h);
    c.fillStyle = hue; c.fillRect(0, 0, w, 24); c.fillStyle = '#0b141b'; c.font = '700 15px system-ui,sans-serif'; c.fillText(title, 10, 17);
    c.strokeStyle = hue; c.fillStyle = hue; c.lineWidth = 2;
    if (kind === 'helm') {                               // the course: range rings, a heading line and the next waypoint
      for (const r of [22, 44, 66]) { c.beginPath(); c.arc(128, 150, r * 1.5, Math.PI * 1.15, Math.PI * 1.85); c.stroke(); }
      c.beginPath(); c.moveTo(128, 150); c.lineTo(150, 40); c.stroke(); c.beginPath(); c.arc(150, 40, 5, 0, Math.PI * 2); c.fill();
    } else if (kind === 'bars') {                        // levels: power, air, water, comms
      [.82, .64, .9, .45, .7, .58].forEach((v, k) => { c.globalAlpha = .85; c.fillRect(16 + k * 38, 140 - v * 100, 24, v * 100); });
    } else if (kind === 'wave') {                        // a signal trace
      c.beginPath(); for (let x = 0; x < w; x += 4) { const y = 92 + Math.sin(x * .09) * 22 * Math.sin(x * .013 + 1); x ? c.lineTo(x, y) : c.moveTo(x, y); } c.stroke();
    } else {                                             // lines of a list, one highlighted
      for (let k = 0; k < 6; k++) { c.globalAlpha = k === 2 ? 1 : .5; c.fillRect(12, 36 + k * 20, [180, 140, 200, 120, 160, 90][k], 8); }
    }
    c.globalAlpha = 1;
  }, 1, 1) });
}
BRG.helm = stationScreen('HELM', '#5fd6c6', 'helm'); BRG.ops = stationScreen('OPS', '#e9c46a', 'bars');
BRG.watch = stationScreen('WATCH', '#9fb8ff', 'list'); BRG.survey = stationScreen('SURVEY', '#8fd18a', 'wave');
BRG.works = stationScreen('WORKS', '#f0a640', 'bars'); BRG.comms = stationScreen('COMMS', '#d98ad1', 'wave');
Object.assign(WALL_KIT, {
  briefingScreen(g) {                                    // the observation room's wall screen
    box(1.7, 1.0, .05, BRG.frame, 0, 1.55, .03, g);
    const p = new THREE.Mesh(new THREE.PlaneGeometry(1.6, .9), BRG.briefing); p.position.set(0, 1.55, .061); g.add(p);
    box(.5, .03, .06, BRG.brass, 0, 1.02, .04, g);
  },
});
// the observation room's wall screen, set up for a briefing: the Wren in profile and an agenda
BRG.briefing = new THREE.MeshBasicMaterial({ toneMapped: false, map: tex(384, 216, (c, w, h) => {
  c.fillStyle = '#0d1a22'; c.fillRect(0, 0, w, h);
  c.fillStyle = '#e8c06a'; c.font = '700 20px system-ui,sans-serif'; c.fillText('BRIEFING', 18, 32);
  c.fillStyle = '#a9c4bf'; c.font = '500 13px system-ui,sans-serif'; c.fillText('CSV WREN  ·  OBSERVATION', 120, 31);
  c.strokeStyle = '#5fd6c6'; c.lineWidth = 2; c.beginPath(); c.moveTo(30, 120); c.lineTo(210, 120); c.quadraticCurveTo(250, 120, 252, 140); c.quadraticCurveTo(250, 160, 210, 160); c.lineTo(30, 160); c.closePath(); c.stroke();
  for (let k = 1; k < 6; k++) { c.beginPath(); c.moveTo(30, 160 - k * 8 + 0); c.lineTo(205, 160 - k * 8); c.globalAlpha = .25; c.stroke(); c.globalAlpha = 1; }
  c.fillStyle = '#e8c06a'; c.beginPath(); c.arc(232, 128, 4, 0, Math.PI * 2); c.fill();
  c.fillStyle = '#d7e4e1'; c.font = '500 12px system-ui,sans-serif';
  ['1  Course and weather', '2  Deck reports', '3  Works: this week', '4  Any other business'].forEach((t, k) => c.fillText(t, 270, 92 + k * 22));
  c.fillStyle = '#5fd6c6'; c.fillRect(18, 190, 120, 4); c.fillStyle = '#3a4a52'; c.fillRect(138, 190, 228, 4);
}, 1, 1) });
Object.assign(BRG, {
  table: std('#4a2f22', .45, .05), books: ['#b4553f', '#d9c79b', '#3f6e8c', '#56466a', '#2a9d8f'].map(c => std(c, .8)), tea: std('#e9e1d0', .35), teaBlue: std('#3f6e8c', .4), gold: std('#c9a24a', .3, .8),
  tankGlass: std('#cfe8ee', .05, 0, { transparent: true, opacity: .22, depthWrite: false }),
  tankWater: std('#2f8fa3', .1, 0, { emissive: col('#1f6f86'), emissiveIntensity: .6, transparent: true, opacity: .55, depthWrite: false }),
});
// The bridge viewscreen: a strip just inside the bow hull, following its curve between bearings a0 and a1 (degrees on
// the bow ellipse, 0 dead ahead), over the hull pieces of room rk only. Each piece's share is added to that hull piece,
// so it drops with it for the cutaway and shows as a lit band at knee height.
function bridgeViewscreen(rk, a0, a1, y0 = .55, y1 = 2.35) {
  const span = 6;                                        // metres of wall per width of the picture
  const t = BRG.sky.map; t.repeat.set(1 / span, H / (y1 - y0)); t.offset.y = -y0 / (y1 - y0);
  const piece = new Map(); for (const hr of HULL_RUNS) if (hr.room === rk) for (const e of hr.edges) piece.set(e.cx.toFixed(4) + ',' + e.cz.toFixed(4), hr);
  const groups = [];
  HULL_SEGS.forEach((s, k) => {
    const mx = (s.ax + s.bx) / 2, mz = (s.az + s.bz) / 2; if (mx < HULL.bowFrom) return;
    const a = Math.atan2((mz - D / 2) / (D / 2), (mx - HULL.bowFrom) / HULL.bowLen) * 180 / Math.PI, hr = piece.get((mx - OX).toFixed(4) + ',' + (mz - OZ).toFixed(4));
    if (a < a0 || a > a1 || !hr) return;
    const last = groups[groups.length - 1];
    if (last && last.hr === hr && last.ix[last.ix.length - 1] === k) last.ix.push((k + 1) % HULL_PTS.length); else groups.push({ hr, ix: [k, (k + 1) % HULL_PTS.length] });
  });
  let arc = 0;
  for (const { hr, ix } of groups) {
    const bz = [BRG.bezel, BRG.bezel, BRG.bezel], vs = new THREE.Group(), pic = hullStrip(ix, y0, y1, T / 2 + .04, T / 2 - .03, [BRG.sky, BRG.bezel, BRG.bezel], { arc0: arc, shadow: false });
    pic.userData.noShadow = true; vs.add(pic);
    vs.add(hullStrip(ix, y0 - .1, y0 + .02, T / 2 + .08, T / 2 - .02, bz));   // bezel under and over the picture
    vs.add(hullStrip(ix, y1 - .02, y1 + .1, T / 2 + .08, T / 2 - .02, bz));
    mergeMeshes(vs); hr.g.add(vs);                       // two draw calls a piece: the picture and the bezel
    for (let n = 0; n < ix.length - 1; n++) arc += HULL_SEGS[ix[n]].l;
  }
  SPINS.push({ o: { rotation: t.offset }, ax: 'x', w: .004 });   // SPINS turns o.rotation[ax]; here that's the picture's offset, so it drifts
}
Object.assign(KIT, {
  tapSpot() { return { w: .6, d: .6, noBlock: true }; },     // nothing to see: a tap target for something built elsewhere (the viewscreen)
  // the Captain's chair: red leather, a high back, armrests with small panels. o.small: a plainer seat for the others
  commandChair(g, o = {}) {
    const s = o.small, lth = s ? BRG.leatherDark : BRG.leather;
    cyl(.26, .3, .06, BRG.frame, 0, .03, 0, g, 18); cyl(.06, .06, .36, BRG.frame, 0, .24, 0, g, 10);
    box(s ? .54 : .62, .12, s ? .5 : .58, lth, 0, .48, 0, g);
    box(s ? .52 : .6, s ? .55 : .8, .12, lth, 0, s ? .82 : .95, -.26, g).rotation.x = -.1;
    if (!s) box(.4, .18, .13, lth, 0, 1.42, -.31, g).rotation.x = -.1;
    for (const x of [-1, 1]) {
      box(.08, .07, s ? .4 : .5, BRG.frame, x * (s ? .3 : .35), .68, .02, g);
      if (!s) box(.07, .02, .2, x < 0 ? WM.screen : WM.screenAmber, x * .35, .72, .1, g);
    }
    return { w: s ? .6 : .75, d: s ? .55 : .65, noBlock: o.noBlock };
  },
  // helm and ops: a free-standing desk, its screen sloped toward whoever sits behind it (front, +z)
  bridgeConsole(g, o = {}) {
    box(.86, .68, .48, BRG.console, 0, .34, -.02, g);
    const top = new THREE.Mesh(new THREE.BoxGeometry(.9, .05, .56), [BRG.frame, BRG.frame, o.screen, BRG.frame, BRG.frame, BRG.frame]);
    top.position.set(0, .74, 0); top.rotation.x = .32; top.castShadow = top.receiveShadow = true; g.add(top);
    box(.9, .04, .06, BRG.brass, 0, .66, .26, g);
    for (let k = 0; k < 4; k++) box(.06, .025, .05, k % 2 ? WM.navGreen : WM.red, -.18 + k * .12, .7, .17, g).rotation.x = .32;
    return { w: .9, d: .6 };
  },
  // a rear station against a wall: a sloped desk with a screen, and an upright screen above it
  rearStation(g, o = {}) {
    const w = o.w || 1.0;
    box(w, .72, .55, BRG.console, 0, .36, 0, g);
    const top = new THREE.Mesh(new THREE.BoxGeometry(w, .05, .5), [BRG.frame, BRG.frame, o.screen, BRG.frame, BRG.frame, BRG.frame]);
    top.position.set(0, .79, .02); top.rotation.x = .3; top.castShadow = top.receiveShadow = true; g.add(top);
    box(w, .62, .08, BRG.frame, 0, 1.18, -.23, g);
    const up = new THREE.Mesh(new THREE.BoxGeometry(w - .16, .46, .02), [BRG.frame, BRG.frame, BRG.frame, BRG.frame, o.screen, BRG.frame]);
    up.position.set(0, 1.2, -.185); g.add(up);
    box(w, .03, .04, BRG.brass, 0, .74, .27, g);
    return { w, d: .6 };
  },
  // the conference table for ten: a dark wood racetrack along local z, a brass inlay, two pedestals, water and tablets
  confTable(g) {
    const L = 3.4, r = .7, s = new THREE.Shape();
    s.moveTo(-r, -L / 2); s.lineTo(-r, L / 2); s.absarc(0, L / 2, r, Math.PI, 0, true); s.lineTo(r, -L / 2); s.absarc(0, -L / 2, r, 0, Math.PI, true);
    const top = new THREE.Mesh(new THREE.ExtrudeGeometry(s, { depth: .06, bevelEnabled: false, curveSegments: 16 }), BRG.table);
    top.rotation.x = Math.PI / 2; top.position.y = .79; top.castShadow = top.receiveShadow = true; g.add(top);
    box(.06, .016, L + .9, BRG.brass, 0, .788, 0, g);
    for (const z of [-1.1, 1.1]) { box(.34, .74, .9, BRG.frame, 0, .37, z, g); box(.7, .04, 1.1, BRG.frame, 0, .02, z, g); }
    cyl(.07, .06, .24, BRG.tankGlass, 0, .915, -.25, g, 14);
    for (const [x, z] of [[-.42, -1.6], [.42, -.6], [-.42, .4], [.42, 1.4]]) { box(.2, .012, .28, WM.screen, x, .797, z, g).rotation.y = x < 0 ? .1 : -.1; }
    for (const [x, z] of [[-.3, -1.0], [.3, 0], [-.3, 1.0]]) cyl(.035, .03, .1, BRG.tankGlass, x, .845, z, g, 10);
    return { w: 1.4, d: L + 2 * r };
  },
  // the Captain's tea, on a low sideboard: a pot, cups and a tin
  teaSideboard(g) {
    box(.9, .75, .42, BRG.table, 0, .375, 0, g); box(.94, .04, .46, BRG.frame, 0, .76, 0, g);
    for (const x of [-.22, .22]) box(.02, .3, .01, BRG.gold, x, .45, .215, g);
    soft(BRG.teaBlue, -.15, .88, 0, .11, .1, .11, g); box(.04, .03, .1, BRG.teaBlue, -.15, .92, .11, g).rotation.x = -.6;
    for (const [x, z] of [[.12, -.08], [.26, .06], [.12, .1]]) cyl(.04, .035, .07, BRG.tea, x, .815, z, g, 12);
    cyl(.07, .07, .14, BRG.gold, .32, .85, -.1, g, 14);
    return { w: .9, d: .46 };
  },
  // the ready room desk: wood with two pedestals, a tablet, a mug and a model of the Wren; the Captain sits at +z
  readyDesk(g) {
    box(1.5, .06, .72, BRG.table, 0, .76, 0, g);
    for (const x of [-.52, .52]) box(.42, .74, .64, BRG.table, x, .37, 0, g);
    box(.62, .5, .03, BRG.table, 0, .48, -.32, g);
    box(.3, .015, .22, WM.screen, -.3, .797, .14, g).rotation.y = .2;
    cyl(.045, .04, .1, BRG.teaBlue, .45, .84, .12, g, 14);
    const ship = new THREE.Group(); ship.position.set(.25, .79, -.18); ship.rotation.y = .5; g.add(ship);
    box(.06, .04, .02, BRG.frame, 0, .02, 0, ship); box(.22, .05, .07, M.trim, 0, .065, 0, ship); soft(M.trim, .11, .065, 0, .05, .025, .035, ship);
    return { w: 1.5, d: .72 };
  },
  // the Admiral's aquarium: a cabinet, the tank, weed, gravel, and one slow orange fish
  aquarium(g) {
    box(1.0, .7, .46, BRG.table, 0, .35, 0, g);
    box(.96, .05, .44, BRG.frame, 0, .725, 0, g); box(.96, .05, .44, BRG.frame, 0, 1.27, 0, g);
    box(.92, .46, .4, BRG.tankWater, 0, 1.0, 0, g);
    box(.96, .52, .44, BRG.tankGlass, 0, 1.0, 0, g);
    box(.9, .05, .38, GD.stone2, 0, .775, 0, g);
    for (const [x, h] of [[-.32, .3], [-.22, .22], [.3, .34]]) soft(M.leaf, x, .8 + h / 2, -.08, .04, h / 2, .04, g);
    soft(GD.fish, .05, 1.02, .02, .07, .045, .03, g); soft(GD.fish, -.03, 1.02, .02, .03, .035, .012, g);
    glow('#7fd8ff', 1.1, 0, 1.0, .1, g, .25);
    return { w: 1.0, d: .46 };
  },
  // the ready room's bookshelf: like the cabins' one, but its books share a few materials and come from a fixed pattern
  readyShelf(g) {
    box(1.2, 1.9, .05, BRG.table, 0, .95, -.15, g);                                  // an open carcass: back, sides, top and plinth
    for (const x of [-.58, .58]) box(.04, 1.9, .35, BRG.table, x, .95, 0, g);
    box(1.2, .04, .35, BRG.table, 0, 1.88, 0, g); box(1.2, .1, .35, BRG.table, 0, .05, 0, g);
    for (let s = 0; s < 4; s++) {
      box(1.12, .03, .3, M.slateDark, 0, .2 + s * .42, .01, g);
      let x = -.5, k = s * 7;
      while (x < .45) { const bw = .05 + (k * 37 % 5) * .01, bh = .22 + (k * 53 % 7) * .02; box(bw, bh, .22, BRG.books[k % 5], x + bw / 2, .215 + s * .42 + bh / 2, .02, g); x += bw + .01; if (k % 9 === 4) x += .12; k++; }
    }
    return { w: 1.2, d: .35, tall: true };
  },
  // the bridge washroom: a compact toilet and a small basin with a mirror
  compactToilet(g) {
    cyl(.17, .13, .4, M.ceramic, 0, .2, .06, g, 18); box(.34, .3, .15, M.ceramic, 0, .56, -.2, g);
    box(.06, .03, .03, M.metal, .1, .73, -.2, g);
    return { w: .4, d: .56 };
  },
  smallBasin(g) {
    box(.5, .1, .4, M.ceramic, 0, .82, 0, g); cyl(.15, .12, .05, KM.basin, 0, .855, .03, g, 18);
    cyl(.06, .08, .78, M.ceramic, 0, .39, -.05, g, 14);
    box(.03, .14, .03, M.metal, 0, .94, -.15, g); box(.03, .03, .09, M.metal, 0, 1.0, -.11, g);
    box(.44, .56, .02, KM.mirror, 0, 1.5, -.18, g); box(.5, .62, .02, M.slateDark, 0, 1.5, -.195, g);
    return { w: .5, d: .4 };
  },
  trunkHead(g) {                                         // where the trunks end: a manifold across both ducts under the ceiling, its plate facing the lobby glass
    box(1.8, .5, .72, BRG.duct, 0, 2.38, 0, g);
    for (const x of [-.5, .5]) cyl(.37, .37, .08, WM.paintDark, x, 2.1, 0, g, 24);
    box(.56, .23, .02, WM.paintDark, 0, 2.38, -.37, g);
    const p = new THREE.Mesh(new THREE.PlaneGeometry(.5, .19), BRG.trunkPlate); p.position.set(0, 2.38, -.385); p.rotation.y = Math.PI; g.add(p);
    return { w: 2, d: 1, noBlock: true };
  },
});

