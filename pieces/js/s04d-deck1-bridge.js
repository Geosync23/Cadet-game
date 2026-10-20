// =====================================================================
// DECK 1: BRIDGE (step 6e, builds 0.8.x; scaled up in 0.12.x)
// From plans/deck1-plan.html (Sketch 2). The top of the ship and the smallest deck: the bridge fills the bow, the
// observation room (also the conference room) the stern, with the lift lobby, the trunk head and the
// top of the ladder between. The ready room is locked and tucked aft of the bridge to port, beside the lobby;
// the washroom mirrors it to starboard. The service spaces are sealed until their tier.
// =====================================================================
DECKS[1] = {
  num: 1, name: 'Bridge', seed: 10109,
  blurb: 'Bridge, ready room, observation room', arrive: 'The bridge is forward of the lift, the observation room aft. People talk quietly up here.',
  lift: [8, 6],
  // car rows 4-6, trunks row 3 above it, ladder row 7: the same world spot as every deck. The spine ends here.
  // 22 x 12, world x -12..10 and z -6..6: well inside Deck 2 (52 x 22) below it.
  map: [
    '..OOOOkkkkRRRBBBBB....',
    '.OOOOOkkkkRRRBBBBBBB..',
    '.OOOOO++++RRRBBBBBBBB.',
    '.OOOOO+YY+RRRBBBBBBBBB',
    '.OOOOO+@@+BBBBBBBBBBBB',
    '.OOOOO+@@+BBBBBBBBBBBB',
    '.OOOOO+@@+BBBBBBBBBBBB',
    '.OOOOO+ZZ+BBBBBBBBBBBB',
    '.OOOOO++++wwwBBBBBBBBB',
    '.OOOOOuuuuwwwBBBBBBBB.',
    '.OOOOOuuuucccccBBBBB..',
    '..OOOOuuuuccccccBB....',
  ],
  // doors, in game edge keys. door: open to all. closed: shut, with tap text. hatch: service access.
  // glass: an inner window. lift: the main lift (one wide door each side).
  doors: {
    'v,7,4': 'lift', 'v,7,5': 'lift', 'v,7,6': 'lift', 'v,9,4': 'lift', 'v,9,5': 'lift', 'v,9,6': 'lift',   // one wide door each side
    'h,7,3': 'glass', 'h,8,3': 'glass',                       // the trunk head, behind glass above the car
    'h,7,8': 'hatch', 'h,8,8': 'glass',                       // the top of the ladder, with its hatch
    'v,10,5': 'door', 'v,10,6': 'door', 'v,10,4': 'glass', 'v,10,7': 'glass',   // bridge doors, straight ahead of the bow-side lift door
    'v,6,5': 'door', 'v,6,6': 'door', 'v,6,4': 'glass', 'v,6,7': 'glass',       // glass doors into the observation room, aft
    'h,11,4': 'closed',                                       // the ready room, from the aft edge of the bridge
    'v,10,8': 'door',                                         // bridge washroom, from the lobby
    'h,6,2': 'hatch', 'h,9,9': 'hatch',                       // utility closet; relay room
    'h,14,10': 'hatch',                                       // floor hatch by the Works station, down into the sub-floor crawl
    'v,10,10': 'hatch',                                       // relay room into the sub-floor crawl (A5b)
  },
  // which room each shut door or hatch leads into (its tap text is that room's 'tap')
  sealed: { 'h,11,4': 'R', 'h,6,2': 'k', 'h,9,9': 'u', 'h,14,10': 'c', 'v,10,10': 'c' },
  // Pillar 2 A5b: the utility spaces are built (plans/deck1-plan.html, "Utility rooms"); their hatches are service hatches
  service: [{ key: 'h,6,2', tier: 1 }, { key: 'h,9,9', tier: 3 }, { key: 'h,14,10', tier: 3 }, { key: 'v,10,10', tier: 3 }],   // closet; relay room, crawl (answers pass row 4)
  crawl: ['10,10', '11,10', '12,10', '13,10', '14,10'],   // the sub-floor crawl's walkable tiles: crouch tiles (answers pass, row 29)
  plates: [['v,10,3', 'w', 'Bridge'], ['v,6,3', 'e', 'Observation'], ['h,12,4', 's', 'Ready room']],
  rooms: {
    '+': { name: 'Bridge lobby', floor: 'lobby', hall: true },
    '@': { name: 'Main lift', floor: 'lift' },
    Y: { name: 'Spine trunks', floor: 'grate', spine: true }, Z: { name: 'Spine ladder', floor: 'grate', spine: true },
    B: { name: 'Bridge', floor: 'bridge' },
    O: { name: 'Observation room', floor: 'wood' },
    w: { name: 'Bridge washroom', floor: 'tile' },
    // locked, not yours
    R: { name: 'Ready room', floor: 'wood', tap: 'The Captain\'s ready room. The door is shut, and you have not been sent for.' },
    // sealed until their tier
    k: { name: 'Utility closet', floor: 'grate', still: true, tap: 'Deck 1\'s light relays and the lobby\'s power junction. Tier 1 access, once the job list is running.' },
    u: { name: 'Relay room', floor: 'grate', still: true, tap: 'Racks of bridge relays, clicking under blue status lights, and the way down into the sub-floor.' },
    c: { name: 'Sub-floor crawl', floor: 'grate', still: true, tap: 'A low crawl under the rear stations, from the relay room.' },
  },
  windows: ['O', 'R'].map(room => ({ room })),
  closedDoors: {
    'h,7,8': { t: 'Spine ladder', x: 'The top of the maintenance ladder. It runs the whole height of the ship, beside the lift, and this is where it ends. Tier 2 access.' },
  },
  hull: { sternX: 1, stern: 3, bowFrom: 15, bowLen: 6.6, byFace: true },   // a short, round hull: big stern corners, a blunt elliptical bow; one hull piece per facing
  light: { sky: col('#d4e2ff'), sun: col('#dfe8ff'), hemi: .96, sunI: .9 },   // cooler than the decks below
  // the command ring, inlaid in the carpet (the ring is faked: no sunken floor). A darker well, shaded under its edge,
  // a brass step edge with a teal light line outside it, and a faint inner circle round the Captain's chair.
  ring: [17, 6, 2.0],
  // the command rail: a curved rail in dark wood behind the ring, open at both sides and forward
  curves: [
    { kind: 'bar', arc: [17, 6, 2.4, 130, 230], out: 1, it: { t: 'Command rail', x: 'A curved rail in dark wood round the back of the command ring. The rear stations\' crew lean on it during briefings; the Captain pretends not to notice.' } },
  ],
  floorArt(g, PX) {
    const [i, j, r0] = this.ring, cx = i * PX, cy = j * PX, r = r0 * PX, arc = (rr) => { g.beginPath(); g.arc(cx, cy, rr, 0, Math.PI * 2); };
    g.fillStyle = 'rgba(8,12,22,.32)'; arc(r); g.fill();
    const sh = g.createRadialGradient(cx, cy, r * .7, cx, cy, r); sh.addColorStop(0, 'rgba(0,0,0,0)'); sh.addColorStop(1, 'rgba(0,0,0,.38)'); g.fillStyle = sh; arc(r); g.fill();
    g.strokeStyle = '#b8913e'; g.lineWidth = 7; arc(r); g.stroke();
    g.strokeStyle = 'rgba(255,236,190,.35)'; g.lineWidth = 2; arc(r + 4); g.stroke();
    g.strokeStyle = 'rgba(95,214,198,.6)'; g.lineWidth = 3; arc(r + 12); g.stroke();
    g.strokeStyle = 'rgba(184,145,62,.35)'; g.lineWidth = 2; arc(r * .42); g.stroke();
    // the floor hatch down into the sub-floor crawl, beside the Works station: a plate with hazard edges and a recessed handle
    const [hi, hj] = this.floorHatch, hx = hi * PX + 12, hy = hj * PX + 10, hw = PX - 22;
    g.fillStyle = '#2c333a'; g.fillRect(hx, hy, hw, hw);
    hazardBand(g, hx, hy, hw, 6, true); hazardBand(g, hx, hy + hw - 6, hw, 6, true); hazardBand(g, hx, hy, 6, hw, false); hazardBand(g, hx + hw - 6, hy, 6, hw, false);
    g.fillStyle = 'rgba(0,0,0,.45)'; g.fillRect(hx + hw / 2 - 9, hy + hw / 2 - 3, 18, 6); g.fillStyle = 'rgba(255,255,255,.12)'; g.fillRect(hx + 7, hy + 7, hw - 14, 1);
  },
  floorHatch: [14, 9],
  // Pillar 1 places (workstream 3b, data only: nothing draws them yet). Every spot where someone does something, in the
  // plan's format, plus two fields: xy, the exact spot in tile units (a seat can sit off its tile's centre, and a tile can
  // hold two seats), and walk, the tile a person walks to first (the place's own tile when it's walkable, otherwise the
  // nearest reachable tile in the same room, within 2.5 m). Generated from the furniture's own positions, then kept as fixed data.
  // the machines in Deck 1's utility spaces (Pillar 2 plan, "Machines and jobs"); each has a work:works place on its panel tile
  machines: [
    { id: '1-relay-1', kind: 'relay', at: [6, 9], room: 'u', face: 's', panel: [7, 10], look: { lamp: [0, 1.2, .23], drip: [0, .9, .27], light: [0, 2.1, .23] } },
    { id: '1-relay-2', kind: 'relay', at: [6, 11], room: 'u', face: 'n', panel: [8, 10], look: { lamp: [0, 1.2, .23], drip: [0, .9, .27], light: [0, 2.1, .23] } },
    { id: '1-junction-1', kind: 'junction', at: [8, 0], room: 'k', face: 's', panel: [8, 1], look: { lamp: [0, 1.2, .13], drip: [0, .9, .17], light: [0, 2.1, .13] } },
    { id: '1-lights-1', kind: 'lights', at: [6, 0], room: 'k', face: 's', panel: [7, 1], look: { lamp: [0, 1.2, .13], drip: [0, .9, .17], light: [0, 2.1, .13] } },
    { id: '1-databus-1', kind: 'databus', at: [12, 11], room: 'c', face: 'n', panel: [12, 10], look: { lamp: [0, .53, .21], drip: [0, .5, .25], light: [0, 2.1, .21] } },
  ],
  places: [
    { id: '1-command-1', type: 'work:command', at: [16, 6], xy: [16.8, 6], walk: [17, 5], face: 'e', pose: 'sit', y: .54, room: 'B' },
    { id: '1-command-2', type: 'work:command', at: [16, 4], xy: [16.8, 4.85], walk: [17, 4], face: 'e', pose: 'sit', y: .54, room: 'B' },
    { id: '1-command-3', type: 'work:command', at: [16, 7], xy: [16.8, 7.15], walk: [17, 7], face: 'e', pose: 'sit', y: .54, room: 'B' },
    { id: '1-helm-1', type: 'work:helm', at: [18, 5], xy: [18.5, 5.45], walk: [18, 4], face: 'e', pose: 'sit', y: .54, room: 'B' },
    { id: '1-ops-1', type: 'work:ops', at: [18, 6], xy: [18.5, 6.55], walk: [18, 7], face: 'e', pose: 'sit', y: .54, room: 'B' },
    { id: '1-watch-1', type: 'work:watch', at: [13, 1], xy: [13.92, 1.5], walk: [14, 1], face: 'w', pose: 'sit', y: .54, room: 'B' },
    { id: '1-survey-1', type: 'work:survey', at: [13, 2], xy: [13.92, 2.5], walk: [14, 2], face: 'w', pose: 'sit', y: .54, room: 'B' },
    { id: '1-comms-1', type: 'work:comms', at: [13, 8], xy: [13.92, 8.5], walk: [14, 8], face: 'w', pose: 'sit', y: .54, room: 'B' },
    { id: '1-works-1', type: 'work:works', at: [13, 9], xy: [13.92, 9.5], walk: [14, 9], face: 'w', pose: 'sit', y: .54, room: 'B' },
    { id: '1-conf-1', type: 'common-room', at: [2, 4], xy: [2.35, 4], walk: [2, 4], face: 'e', pose: 'sit', anim: 'talk', y: .54, room: 'O' },
    { id: '1-conf-2', type: 'common-room', at: [4, 4], xy: [4.65, 4], walk: [4, 4], face: 'w', pose: 'sit', anim: 'talk', y: .54, room: 'O' },
    { id: '1-conf-3', type: 'common-room', at: [2, 5], xy: [2.35, 5], walk: [2, 5], face: 'e', pose: 'sit', anim: 'talk', y: .54, room: 'O' },
    { id: '1-conf-4', type: 'common-room', at: [4, 5], xy: [4.65, 5], walk: [4, 5], face: 'w', pose: 'sit', anim: 'talk', y: .54, room: 'O' },
    { id: '1-conf-5', type: 'common-room', at: [2, 6], xy: [2.35, 6], walk: [2, 6], face: 'e', pose: 'sit', anim: 'talk', y: .54, room: 'O' },
    { id: '1-conf-6', type: 'common-room', at: [4, 6], xy: [4.65, 6], walk: [4, 6], face: 'w', pose: 'sit', anim: 'talk', y: .54, room: 'O' },
    { id: '1-conf-7', type: 'common-room', at: [2, 7], xy: [2.35, 7], walk: [2, 7], face: 'e', pose: 'sit', anim: 'talk', y: .54, room: 'O' },
    { id: '1-conf-8', type: 'common-room', at: [4, 7], xy: [4.65, 7], walk: [4, 7], face: 'w', pose: 'sit', anim: 'talk', y: .54, room: 'O' },
    { id: '1-conf-9', type: 'common-room', at: [2, 8], xy: [2.35, 8], walk: [2, 8], face: 'e', pose: 'sit', anim: 'talk', y: .54, room: 'O' },
    { id: '1-conf-10', type: 'common-room', at: [4, 8], xy: [4.65, 8], walk: [4, 8], face: 'w', pose: 'sit', anim: 'talk', y: .54, room: 'O' },
    { id: '1-window-1', type: 'lounge-seat', at: [1, 7], xy: [1.38, 7.2], walk: [2, 7], face: 'e', pose: 'sit', anim: 'read', window: true, y: .52, room: 'O' },
    { id: '1-window-2', type: 'lounge-seat', at: [1, 6], xy: [1.38, 6.4], walk: [2, 6], face: 'e', pose: 'sit', anim: 'read', window: true, y: .52, room: 'O' },
    { id: '1-window-3', type: 'lounge-seat', at: [1, 5], xy: [1.38, 5.6], walk: [2, 5], face: 'e', pose: 'sit', anim: 'read', window: true, y: .52, room: 'O' },
    { id: '1-window-4', type: 'lounge-seat', at: [1, 4], xy: [1.38, 4.8], walk: [2, 4], face: 'e', pose: 'sit', anim: 'read', window: true, y: .52, room: 'O' },
    { id: '1-tea-1', type: 'common-room', at: [5, 8], xy: [5.02, 8.9], walk: [4, 8], face: 'e', pose: 'stand', anim: 'drink', room: 'O' },
    // answers pass row 24: places for the sim engineer's scheduled events (type 'event', never handed out on their own; section 14 lists them by `event`)
    // The shift handover at 06:00 and 18:00: officers gather round the aft of the command ring, facing it.
    { id: '1-handover-1', type: 'event', event: 'handover', at: [12, 4], face: 'e', pose: 'stand', anim: 'talk', room: 'B' },
    { id: '1-handover-2', type: 'event', event: 'handover', at: [12, 7], face: 'e', pose: 'stand', anim: 'talk', room: 'B' },
    { id: '1-handover-3', type: 'event', event: 'handover', at: [14, 3], face: 's', pose: 'stand', anim: 'talk', room: 'B' },
    { id: '1-handover-4', type: 'event', event: 'handover', at: [15, 3], face: 's', pose: 'stand', anim: 'talk', room: 'B' },
    { id: '1-handover-5', type: 'event', event: 'handover', at: [14, 8], face: 'n', pose: 'stand', anim: 'talk', room: 'B' },
    { id: '1-handover-6', type: 'event', event: 'handover', at: [15, 8], face: 'n', pose: 'stand', anim: 'talk', room: 'B' },
    // The Captain's evening walk through the observation room, stops in order: in from the glass doors, the three windows, a cup of tea.
    { id: '1-walk-1', type: 'event', event: 'walk', at: [5, 3], face: 'w', pose: 'stand', room: 'O' },
    { id: '1-walk-2', type: 'event', event: 'walk', at: [2, 1], face: 'n', pose: 'stand', window: true, room: 'O' },
    { id: '1-walk-3', type: 'event', event: 'walk', at: [1, 3], face: 'w', pose: 'stand', window: true, room: 'O' },
    { id: '1-walk-4', type: 'event', event: 'walk', at: [2, 10], face: 's', pose: 'stand', window: true, room: 'O' },
    { id: '1-walk-5', type: 'event', event: 'walk', at: [4, 9], face: 'e', pose: 'stand', anim: 'drink', room: 'O' },
    { id: '1-toilet-1', type: 'toilet', at: [12, 9], xy: [12.56, 9.45], walk: [11, 9], face: 'w', pose: 'sit', y: .4, room: 'w' },
    { id: '1-basin-1', type: 'basin', at: [12, 8], xy: [12.5, 8.92], walk: [11, 8], face: 'n', pose: 'stand', room: 'w' },
    { id: '1-lift-1', type: 'lift-wait', at: [6, 2], xy: [6.5, 2.5], walk: [6, 2], face: 's', pose: 'stand', room: '+' },
    { id: '1-lift-2', type: 'lift-wait', at: [9, 2], xy: [9.5, 2.5], walk: [9, 2], face: 's', pose: 'stand', room: '+' },
    { id: '1-lift-3', type: 'lift-wait', at: [6, 8], xy: [6.5, 8.5], walk: [6, 8], face: 'n', pose: 'stand', room: '+' },
    { id: '1-lift-4', type: 'lift-wait', at: [7, 8], xy: [7.5, 8.5], walk: [7, 8], face: 'n', pose: 'stand', room: '+' },
    { id: '1-ready-1', type: 'work:command', at: [11, 1], xy: [11.5, 1.3], walk: [10, 1], face: 's', pose: 'sit', anim: 'read', y: .54, room: 'R' },   // the Captain's desk chair: the ready room's door is a closed door, which crew open
    // the machines' panels (A5b)
    { id: '1-relay-1-panel', type: 'work:works', at: [7, 10], xy: [7.5, 10.3], walk: [7, 10], face: 'n', pose: 'work', machine: '1-relay-1', room: 'u' },
    { id: '1-relay-2-panel', type: 'work:works', at: [8, 10], xy: [8.5, 10.7], walk: [8, 10], face: 's', pose: 'work', machine: '1-relay-2', room: 'u' },
    { id: '1-junction-1-panel', type: 'work:works', at: [8, 1], xy: [8.5, 1.3], walk: [8, 1], face: 'n', pose: 'work', machine: '1-junction-1', room: 'k' },
    { id: '1-lights-1-panel', type: 'work:works', at: [7, 1], xy: [7.5, 1.3], walk: [7, 1], face: 'n', pose: 'work', machine: '1-lights-1', room: 'k' },
    { id: '1-databus-1-panel', type: 'work:works', at: [12, 10], xy: [12.5, 10.7], walk: [12, 10], face: 's', pose: 'work', machine: '1-databus-1', room: 'c' },
  ],
  dress(d) {
    for (const [key, tw, text] of d.plates) placeOnEdge('plate', key, tw, { text });
    for (const [key, tw] of [['v,7,7', 'w'], ['v,9,7', 'e']]) placeOnEdge('liftPanel', key, tw);
    placeOnEdge('deckDirectory', 'h,8,2', 's', { it: IT('Deck directory', 'Seven decks, top to bottom. Bridge, Command & Science, Commons, Quarters, the Recreation Deck (R), Operations, Engineering. You are here: Bridge, the top of the line.') });
    // the top of the spine: the trunks end behind glass above the car, the ladder behind glass below it
    for (const r of ['Y', 'Z', 'R']) NO_FADE.add(r);
    place('Y', 'spineTrunks', 1, .5, 'n', { it: { t: 'Trunk head', x: 'The power and air trunks end here, in a trunk head with a brass plate: CSV WREN, TRUNK HEAD, DECK 1. Everything the bridge runs on comes up these.', see: true } });
    place('Y', 'trunkHead', 1, .5, 'n');
    // the viewscreen across the bow, and something to tap in front of it
    bridgeViewscreen('B', -60, 60);
    // the command ring: the Captain's chair with a seat either side, helm and ops just forward, and a brass step edge
    // with a light line round the well (the ring is faked: the floor stays flat). Ring centre: tile (17, 6); B starts at col 10.
    const ring = curvePoints({ arc: [d.ring[0], d.ring[1], d.ring[2], -180, 180] });
    staticRoot.add(curveStrip(ring, -.01, .03, -.05, .05, [BRG.brass, BRG.brass, BRG.brass]));
    const lit = curveStrip(ring, -.01, .012, .06, .085, [BRG.stepGlow, BRG.stepGlow, BRG.stepGlow]); lit.castShadow = false; staticRoot.add(lit);
    place('B', 'commandChair', 6.8, 6, 'w', { block: [[6, 5], [6, 6], [5, 5], [5, 6]], it: IT('The Captain\'s chair', 'Red leather, worn pale on the right armrest where the Captain drums her fingers. Nobody else sits in it. Not even for a photo.') });
    for (const [z, t, x] of [[4.85, 'First officer\'s seat', 'The Commander\'s seat, at the Captain\'s left. A tablet is tucked down the side cushion.'], [7.15, 'Guest seat', 'The seat at the Captain\'s right, for whoever has been invited up. Today, nobody.']])
      place('B', 'commandChair', 6.8, z, 'w', { small: true, block: [[6, z < 6 ? 4 : 7]], it: IT(t, x) });
    for (const [z, scr, t, x] of [[5.45, BRG.helm, 'Helm', 'The helm: course, speed and the next waypoint, plotted in teal. The heading hasn\'t changed in three days.'], [6.55, BRG.ops, 'Ops', 'Operations: power, air, water and comms, all on one desk. Every bar in the green, for once.']]) {
      place('B', 'bridgeConsole', 9.4, z, 'e', { screen: scr, it: IT(t, x) });
      place('B', 'commandChair', 8.5, z, 'w', { small: true, block: [[8, z < 6 ? 5 : 6]] });
    }
    // the rear stations, in two banks facing the bow: Watch and Survey against the ready room's side wall, Comms and Works
    // against the washroom's, Works beside the floor hatch. Each has a seat facing it, and the aisles round them stay open.
    for (const [x, z, back, scr, t, txt] of [
      [3.4, 1.5, 'w', BRG.watch, 'Watch station', 'The watch officer\'s board: who\'s on shift, where, and what\'s due. Your name is on it, in the Works column.'],
      [3.4, 2.5, 'w', BRG.survey, 'Survey station', 'Sensor returns from the array on Deck 2. A long, slow wave that the survey team calls "the ship breathing".'],
      [3.4, 8.5, 'w', BRG.comms, 'Comms station', 'Incoming and outgoing traffic. A queue of call-home messages from Deck 3, waiting for the next relay window.'],
      [3.4, 9.5, 'w', BRG.works, 'Works station', 'The Works board, mirrored from the job list on Deck 5. Bridge jobs are marked in gold; the sub-floor hatch is right beside it.'],
    ]) {
      place('B', 'rearStation', x, z, back, { screen: scr, w: .94, it: IT(t, txt) });
      const o = { n: [0, .7, 's'], s: [0, -.7, 'n'], w: [.52, 0, 'e'] }[back];
      place('B', 'commandChair', x + o[0], z + o[1], o[2], { small: true, noBlock: true });
    }
    // the observation room (also the conference room): the table for ten, the briefing screen on the lobby wall, the window
    // seat across the stern, the Captain's tea, a lamp and two plants. O starts at column 1, so room-local x is tile x - 1.
    place('O', 'confTable', 2.5, 6, 'n', { it: IT('Conference table', 'Ten seats, a brass line down the middle, and a ring on the wood where somebody once put down a hot mug. Briefings happen here.') });
    for (const z of [4.0, 5.0, 6.0, 7.0, 8.0]) for (const [x, b] of [[1.35, 'w'], [3.65, 'e']]) place('O', 'commandChair', x, z, b, { small: true, noBlock: true });
    placeWall('O', 'briefingScreen', 'e', 2.5, { hitW: 1.6, it: IT('Wall screen', 'Set up for the next briefing: the Wren in profile and four items on the agenda. Item three is about the Works. Item three is about you.') });
    place('O', 'windowSeat', .38, 6, 'w', { w: 3.6, it: IT('Window seat', 'The best seat on the ship. From here you look aft along the whole length of the Wren, with the stars sliding away behind.') });
    place('O', 'teaSideboard', 4.67, 8.9, 'e', { it: IT('The Captain\'s tea', 'A blue teapot, three cups and a tin with a handwritten label: NOT FOR BRIEFINGS. On quiet afternoons the Captain takes her tea at the window seat.') });
    place('O', 'floorLamp', .55, 2.45, 'n', { light: true });
    for (const z of [.6, 11.4]) place('O', 'plant', 4.45, z, 'n', { big: true, band: '#c9a24a' });
    // the ready room (3 x 4), locked: the desk facing the door, the Captain's chair behind it and two for visitors, the
    // bookshelf, and the Admiral's aquarium. R starts at column 10; its door is in the middle of its bridge side.
    place('R', 'readyDesk', 1.5, 2.1, 's', { it: { t: 'The Captain\'s desk', x: 'A tidy desk, a model of the Wren, and a mug that says WORLD\'S OKAYEST CAPTAIN. A gift, apparently.', see: true } });
    place('R', 'commandChair', 1.5, 1.3, 'n', { it: { t: 'Desk chair', x: 'The Captain\'s other chair. It faces the door, so she sees who comes in.', see: true } });
    for (const x of [.6, 2.4]) place('R', 'chair', x, 3.2, 's');
    place('R', 'aquarium', .36, .9, 'w', { it: { t: 'The Admiral', x: 'One slow orange fish in a well-kept tank. The Admiral has outlasted two refits and a first officer.', see: true } });
    place('R', 'readyShelf', 2.72, .9, 'e', { it: { t: 'Bookshelf', x: 'Star charts, old logbooks, a field guide to Veyli customs, and a paperback with every page dog-eared.', see: true } });
    // the bridge washroom (3 x 2): a small basin and a compact toilet down its far wall, both reached from the middle. w starts at column 10.
    place('w', 'compactToilet', 2.62, 1.45, 'e', { it: IT('Toilet', 'Compact, spotless, and the only one on Deck 1. The watch is grateful.') });
    place('w', 'smallBasin', 2.5, .32, 'n', { it: IT('Basin', 'A small basin and a mirror. Someone has stuck a note to the glass: STRAIGHTEN YOUR COLLAR.') });
    place('B', 'tapSpot', 10.4, 6, 'e', { it: { t: 'Viewscreen', x: 'The whole bow wall is a screen. Right now it shows what\'s ahead: stars, a smudge of nebula, and a ringed planet the navigator swears is on the way to nowhere.' } });
    place('Z', 'spineLadder', 1, .5, 'n', { it: SPINE_IT.ladder });
    // ---- the utility spaces (A5b; plans/deck1-plan.html "Utility rooms"): closet k from (6, 0), relay room u from (6, 9),
    // sub-floor crawl c from (10, 10). A walkway runs from each hatch past every machine's panel.
    place('u', 'relayBank', 1.5, .35, 'n', { w: 2.8, it: IT('Relay racks', 'The helm and ops circuits, clicking softly under blue status lights.') });
    place('u', 'relayBank', 2.0, 2.65, 's', { w: 3.8, it: IT('Relay racks', 'The viewscreen, comms and the rear stations. One light has blinked amber since before anyone can remember.') });
    place('k', 'cabinet', 1.0, .3, 'n', { it: IT('Light relays', 'Every lamp and light strip on Deck 1, the bridge\'s mood light included.') });
    place('k', 'cabinet', 3.0, .3, 'n', { breakers: true, it: IT('Power junction', 'Deck 1\'s breakers, fed from the trunk head next door.') });
    place('c', 'dataBus', 3.0, 1.65, 's', { it: IT('Data bus', 'Where every bridge station\'s cables meet. Mind your head.') });
    place('c', 'floorCableTray', 1.0, 1.7, 's'); place('c', 'floorCableTray', 5.0, 1.7, 's');
    placeWall('k', 'mugRail', 's', 2.8, { it: IT('Mug rail', 'Three mugs on hooks. The red one says BRIDGE CREW, and nobody admits it\'s theirs.') });
    placeWall('u', 'wallCalendar', 'w', 1.5, { it: IT('Calendar', 'Relay checks ticked off week by week. Someone has drawn a small rocket on payday.') });
    placeWall('c', 'handSign', 'n', 1.5, { it: IT('Sign', 'MIND YOUR HEAD. Three dents in the plate above it suggest people don\'t.') });
    placeOnEdge('healthBoard', 'h,10,4', 's', { hitW: .84, it: IT('Ship health', 'Every system aboard at a glance. The Captain reads it first thing, before the coffee.') });   // the bridge's board, in the vestibule (answers pass rows 2-3)
  },
};
for (const [key, r] of Object.entries(DECKS[1].sealed)) DECKS[1].closedDoors[key] = { t: DECKS[1].rooms[r].name, x: DECKS[1].rooms[r].tap };

