// =====================================================================
// DECK 5: OPERATIONS. Map, doors and hull straight from deck5-plan.html (sketch 2,
// game format). The working deck: shuttle bay and cargo aft, the lift and the
// Works complex midships, the ship's air machinery in the bow. Steel plate and
// grating, hazard bands at doorways, cool work lights, very few windows.
// Door types: door, closed (shut, tap text), hatch (a shut service hatch), glass
// (an inner window: sill, pane, header), lift.
// =====================================================================
DECKS[5] = {
  num: 5, name: 'Operations', seed: 50517, hazard: true,
  blurb: 'Works bay, storage, shuttle bay', arrive: 'The Works bay is through the doors either side of the lift. The shuttle bay is aft, down the haulway.',
  lift: [18, 8],
  map: [
    '.SSSSSSSSSooowwwwwwwwtttggggggggggaaaaaaaaaa',
    '.SSSSSSSSSooowwwwwwwwtttrrrrrrrrrraaaaaaaaaa',
    '.SSSSSSSSSooowwwwwwwwtttrrrrrrrrrraaaaaaaaaa',
    '.SSSSSSSSSwwwwwwwwwwwqqqrrrrrrrrrraaaaaaaaaa',
    '.SSSSSSSSSwwwwwwwwwwwqqqrrrrrrrrrraaaaaaaaaa',
    '.SSSSSSSSSwwwwwwwwwwwqqqrrrrrrrrrrFFFFFFFFFF',
    '.SSSSSSSSS_____++@@++qqqrrrrrrrrrrFFFFFFFFFF',
    '.SSSSSSSSS_____++@@++=============FFFFFFFFFF',
    '.SSSSSSSSS_____++@@++=============FFFFFFFFFF',
    '.SSSSSSSSS_____++ZZ++fffffffyyyyyyFFFFFFFFFF',
    '.SSSSSSSSScccccccccuufffffffyyyyyyFFFFFFFFFF',
    '.SSSSSSSSScccccccccuufffffffyyyyyynnnnnnnnnn',
    '.dddSSSSSScccccccccmmfffffffyyyyyynnnnnnnnnn',
    '.dddSSSSbbcccccccccmmfffffffyyyyyynnnnnnnnnn',
    '.dddSSSSbbcccccccccmmfffffffyyyyyynnnnnnnnnn',
    '.dddSSSSbbcccccccccmmhhhhhhhhhhhhhnnnnnnnnnn',
  ],
  doors: {
    'v,17,6': 'lift', 'v,17,7': 'lift', 'v,17,8': 'lift', 'v,19,6': 'lift', 'v,19,7': 'lift', 'v,19,8': 'lift',
    'h,16,6': 'door', 'h,19,6': 'door',                         // lobby into the Works bay, one beside each lift door
    'v,10,7': 'door', 'v,10,8': 'door',                         // haulway onto the shuttle pad: the way in when you arrive
    'v,21,1': 'door', 'h,22,7': 'door', 'h,26,7': 'door', 'h,24,9': 'door',   // tea corner (from the bay), washroom, storage, machine shop
    'v,13,1': 'closed', 'h,30,9': 'hatch', 'h,12,10': 'door', 'v,10,12': 'hatch', 'h,8,13': 'closed',   // battery room; cargo hold (its shuttle-bay hatch a service hatch since 0.30.12)
    'v,34,7': 'closed', 'h,38,5': 'hatch', 'h,38,11': 'hatch',                          // the machine rooms in the bow
    'h,19,10': 'hatch', 'v,19,13': 'hatch', 'h,2,12': 'hatch', 'h,32,1': 'hatch', 'v,34,0': 'hatch', 'h,25,15': 'hatch', 'v,34,15': 'hatch',
    'v,10,3': 'glass', 'v,10,4': 'glass', 'v,10,5': 'glass',   // the Works bay window onto the shuttle pad
    'v,10,0': 'glass', 'v,10,1': 'glass', 'v,10,2': 'glass',   // the Chief's office sees the pad too...
    'h,10,3': 'glass', 'h,11,3': 'glass', 'h,12,3': 'glass', 'v,13,0': 'glass', 'v,13,2': 'glass',   // ...and the bay floor
    'v,8,13': 'glass', 'v,8,14': 'glass', 'v,8,15': 'glass', 'h,9,13': 'glass',                      // the control booth over the pad
    'v,4,13': 'glass', 'v,4,14': 'glass',                       // watch the door gear turn
    'v,34,8': 'glass',                                          // the fan hall window at the end of the main corridor
  },
  // which room each shut door or hatch leads into (its tap text is that room's 'tap')
  sealed: {
    'v,13,1': 'o', 'h,8,13': 'b', 'v,34,7': 'F', 'h,2,12': 'd', 'h,38,11': 'F',

  },
  plates: [
    ['h,15,6', 's', 'Works bay'], ['h,20,6', 's', 'Works bay'], ['h,21,7', 's', 'Washroom'], ['h,25,7', 's', 'Storage'],
    ['h,23,9', 'n', 'Machine shop'], ['h,29,9', 'n', 'Batteries'], ['h,11,10', 'n', 'Cargo hold'], ['h,20,10', 'n', 'Utility'],
    ['v,10,6', 'e', 'Shuttle bay'], ['v,10,9', 'w', 'Lift'],
  ],
  workLights: [['h,11,6', 's'], ['h,13,6', 's'], ['h,23,7', 's'], ['h,28,7', 's'], ['h,32,7', 's'], ['h,22,9', 'n'], ['h,27,9', 'n'], ['h,32,9', 'n'], ['h,10,10', 'n'], ['h,14,10', 'n']],
  rooms: {
    '_': { name: 'Haulway', floor: 'haul', hall: true },
    '+': { name: 'Lift lobby', floor: 'lobby', hall: true },
    '=': { name: 'Main corridor', floor: 'grate', hall: true },
    '#': { name: 'Spine', void: true },
    '@': { name: 'Main lift', floor: 'lift' },
    Y: { name: 'Spine trunks', floor: 'grate', spine: true }, Z: { name: 'Spine ladder', floor: 'grate', spine: true },
    S: { name: 'Shuttle bay', floor: 'bay', pad: [2, 4, 6, 8] },
    w: { name: 'Works bay', floor: 'steel' },
    t: { name: 'Tea corner', floor: 'wood' },
    q: { name: 'Works washroom', floor: 'tile' },
    r: { name: 'Main storage', floor: 'steel' },
    f: { name: 'Machine shop', floor: 'steel' },
    // locked, but seen through glass
    o: { name: 'Works Chief\'s office', floor: 'plate', tap: 'Glass on two sides, so the Chief can see the whole bay and the shuttle pad. Locked while the Chief is out.' },
    b: { name: 'Bay control booth', floor: 'plate', tap: 'Launch and landing controls, behind glass over the pad. Watch staff only.' },
    d: { name: 'Bay door gear', floor: 'grate', tap: 'Giant gears and hydraulic rams. When the bay opens, the doors slide into a pocket here. Watch the gears through the window.' },
    F: { name: 'Fan hall', floor: 'grate', tap: 'The ship\'s lungs: one huge fan pushing air under the main corridor and up the spine to every deck. Tier 2 access, through the hatch from the air plant. You can watch it through the corridor window too.' },
    // utility rooms (Pillar 2, 0.30.3): floors that draw no random numbers, so the rest of the deck is unchanged
    c: { name: 'Cargo hold', floor: 'steel', still: true },
    m: { name: 'Cart bay', floor: 'steel', still: true },
    u: { name: 'Utility closet', floor: 'plate', still: true },
    g: { name: 'Port pipe gallery', floor: 'grate', still: true },
    h: { name: 'Starboard pipe gallery', floor: 'grate', still: true },
    a: { name: 'Air plant', floor: 'steel', still: true },
    n: { name: 'Manifold room', floor: 'steel', still: true },
    y: { name: 'Battery room', floor: 'plate', still: true },
  },
  windows: ['t', 'o', 'b'].map(room => ({ room })),
  closedDoors: {},
  hull: { sternX: 1, stern: 1.5, bowFrom: 34, bowLen: 9.6, byFace: true },   // one hull piece per facing (0.30.11)
  // service hatches into the utility rooms (0.30.3): the player and Works crew pass (see hatchPassable)
  // (the air plant and manifold room open off the pipe galleries; since 0.47.3 the air plant's hatch opens into the Fan hall, the manifold room's stays sealed)
  // (0.30.12) with a tier each: 1 closets, stores and the cargo hold, 2 plant rooms and pipe galleries, 3 batteries. The cargo hold's
  // shuttle-bay hatch (v,10,12) is open to the player and Works crew; everyone else still goes round by the haulway.
  service: [{ key: 'v,34,0', tier: 2 }, { key: 'v,34,15', tier: 2 }, { key: 'h,30,9', tier: 3 }, { key: 'h,19,10', tier: 1 }, { key: 'v,19,13', tier: 1 },
    { key: 'h,32,1', tier: 2 }, { key: 'h,25,15', tier: 2 }, { key: 'v,10,12', tier: 1 },   // air plant, manifold, batteries, closet, cart bay, galleries, hold
    { key: 'h,38,5', tier: 2 }],                         // 0.47.3 (Pillar 5 Step 3, the air line): the Fan hall, through the air plant
  // machines (Pillar 2; format as on Deck 4): wall-mounted ones have `at` on their panel tile
  machines: [
    { id: '5-o2-1', kind: 'o2cell', at: [35, 0], room: 'a', face: 's', panel: [35, 1], look: { lamp: [0.5, 1.2, 0.37], drip: [0.5, 0.9, 0.42] } },
    { id: '5-o2-2', kind: 'o2cell', at: [37, 0], room: 'a', face: 's', panel: [37, 1], look: { lamp: [0.5, 1.2, 0.37], drip: [0.5, 0.9, 0.42] } },
    { id: '5-electrolyser-1', kind: 'electrolyser', at: [35, 2], room: 'a', face: 'e', panel: [36, 2], look: { lamp: [-0.62, 1.2, 0.67], drip: [-0.62, 0.9, 0.72] } },
    { id: '5-scrubber-1', kind: 'airplant', at: [39, 4], room: 'a', face: 'n', panel: [39, 3] },
    { id: '5-scrubber-2', kind: 'airplant', at: [40, 4], room: 'a', face: 'n', panel: [40, 3] },
    { id: '5-manifold-1', kind: 'manifold', at: [36, 15], room: 'n', face: 'n', panel: [36, 14], look: { lamp: [-0.5, 1.2, 0.05], drip: [-0.5, 0.9, 0.1] } },
    { id: '5-pump-1', kind: 'pump', at: [34, 11], room: 'n', face: 'e', panel: [35, 11], look: { lamp: [0, 0.45, 0.33], drip: [0, 0.42, 0.38] } },
    { id: '5-pump-2', kind: 'pump', at: [34, 12], room: 'n', face: 'e', panel: [35, 12], look: { lamp: [0, 0.45, 0.33], drip: [0, 0.42, 0.38] } },
    { id: '5-battery-1', kind: 'battery', at: [28, 11], room: 'y', face: 's', panel: [28, 12], look: { lamp: [0.5, 1.03, 0.42], drip: [0.5, 0.9, 0.47] } },
    { id: '5-battery-2', kind: 'battery', at: [33, 11], room: 'y', face: 's', panel: [33, 12], look: { lamp: [-0.5, 1.03, 0.42], drip: [-0.5, 0.9, 0.47] } },
    { id: '5-battery-3', kind: 'battery', at: [28, 13], room: 'y', face: 's', panel: [28, 14], look: { lamp: [0.5, 1.03, 0.42], drip: [0.5, 0.9, 0.47] } },
    { id: '5-battery-4', kind: 'battery', at: [33, 13], room: 'y', face: 's', panel: [33, 14], look: { lamp: [-0.5, 1.03, 0.42], drip: [-0.5, 0.9, 0.47] } },
    { id: '5-inverter-1', kind: 'inverter', at: [33, 9], room: 'y', face: 's', panel: [33, 10], look: { lamp: [0, 1.2, 0.13], drip: [0, 0.9, 0.18] } },
    { id: '5-junction-1', kind: 'lights', at: [20, 11], room: 'u', face: 'w', panel: [19, 11], look: { lamp: [0, 1.2, 0.13], drip: [0, 0.9, 0.18] } },
    { id: '5-cartdock-1', kind: 'cartdock', at: [20, 12], room: 'm', face: 'w', panel: [19, 12], look: { lamp: [0.5, 1.08, 0.51], drip: [0.5, 0.9, 0.56] } },
    { id: '5-cartdock-2', kind: 'cartdock', at: [20, 15], room: 'm', face: 'w', panel: [19, 15], look: { lamp: [-0.5, 1.08, 0.51], drip: [-0.5, 0.9, 0.56] } },
    { id: '5-valve-1', kind: 'valve', at: [28, 0], room: 'g', face: 's', panel: [28, 0] },
    { id: '5-valve-2', kind: 'valve', at: [29, 15], room: 'h', face: 'n', panel: [29, 15] },
    // 0.47.3 (Pillar 5 Step 3, plans/mechanics/architect-air-line.html): the air line's middle and its two branches
    { id: '5-fan-1', kind: 'fan', at: [36, 8], room: 'F', face: 's', panel: [36, 9] },
    { id: '5-damper-1', kind: 'damper', at: [34, 6], room: 'F', face: 'e', panel: [34, 6] },   // Upper decks, 1-3
    { id: '5-damper-2', kind: 'damper', at: [34, 9], room: 'F', face: 'e', panel: [34, 9] },   // Lower decks, 4-6
  ],
  // places (Pillar 1): every spot where a crew member does something, for the schedules. Data only: nothing draws them.
  // { id, type, at: [col, row], face, pose, room }. Seats and beds sit on furniture tiles and are reached from the tile beside them;
  // face is the way the person faces there. deck_check.py checks every place can be reached.
  places: [
    { id: '5-bench-1', type: 'work:works', at: [14, 3], face: 'n', pose: 'work', room: 'w' },
    { id: '5-bench-2', type: 'work:works', at: [15, 3], face: 'n', pose: 'work', room: 'w' },
    { id: '5-bench-3', type: 'work:works', at: [18, 3], face: 'n', pose: 'work', room: 'w' },
    { id: '5-bench-4', type: 'work:works', at: [19, 3], face: 'n', pose: 'work', room: 'w' },
    { id: '5-jobboard-1', type: 'work:works', at: [15, 1], face: 'n', pose: 'stand', room: 'w' },
    { id: '5-timeclock-1', type: 'timeclock', at: [20, 0], xy: [20.6, .5], face: 'n', pose: 'stand', room: 'w' },   // the time clock (0.61.13), past the tool wall by the tea corner door: crew clock in and out here
    { id: '5-toolwall-1', type: 'work:works', at: [19, 1], face: 'n', pose: 'stand', room: 'w' },
    { id: '5-stool-1', type: 'work:works', at: [11, 3], face: 'e', pose: 'sit', room: 'w', xy: [11.57, 3.63], y: 0.49 },
    { id: '5-office-1', type: 'work:works', at: [11, 1], face: 'n', pose: 'sit', room: 'o', xy: [11.5, 1.4], y: 0.5, cush: 0.5 },
    { id: '5-tea-1', type: 'lounge-seat', at: [23, 0], face: 'w', pose: 'sit', room: 't', window: true, xy: [23.66, 0.6], y: 0.44, cush: 0.44 },
    { id: '5-tea-2', type: 'lounge-seat', at: [21, 0], face: 'e', pose: 'sit', room: 't', window: true, xy: [21.64, 0.64], y: 0.49 },
    { id: '5-tea-3', type: 'lounge-seat', at: [21, 1], face: 's', pose: 'stand', room: 't' },
    { id: '5-toilet-2', type: 'toilet', at: [21, 3], face: 's', pose: 'sit', room: 'q', xy: [21.9, 3.5], y: 0.4 },   // 0.38.27: was the shower (5-shower-1)
    { id: '5-toilet-1', type: 'toilet', at: [23, 3], face: 's', pose: 'sit', room: 'q', xy: [23.3, 3.5], y: 0.4 },
    { id: '5-basin-1', type: 'basin', at: [22, 5], face: 'w', pose: 'stand', room: 'q' },
    { id: '5-basin-2', type: 'basin', at: [22, 6], face: 'w', pose: 'stand', room: 'q' },
    { id: '5-store-1', type: 'work:works', at: [25, 4], face: 'w', pose: 'work', room: 'r' },
    { id: '5-aisle-1', type: 'work:works', at: [28, 3], face: 'w', pose: 'work', room: 'r' },
    { id: '5-aisle-2', type: 'work:works', at: [30, 3], face: 'w', pose: 'work', room: 'r' },
    { id: '5-shop-1', type: 'work:works', at: [22, 11], face: 'w', pose: 'work', room: 'f' },
    { id: '5-shop-2', type: 'work:works', at: [26, 10], face: 'n', pose: 'work', room: 'f' },
    { id: '5-shop-3', type: 'work:works', at: [26, 11], face: 'e', pose: 'work', room: 'f' },
    { id: '5-shop-4', type: 'work:works', at: [23, 13], face: 'n', pose: 'work', room: 'f' },
    { id: '5-shop-5', type: 'work:works', at: [24, 13], face: 'n', pose: 'work', room: 'f' },
    // fetching and making parts (0.30.8, for the systems engineer's jobs): not desks, so the planner never hands them out as work stations
    { id: '5-parts-1', type: 'storage', anim: 'browse', stock: ['relay', 'breaker', 'cable', 'cell', 'signal card', 'coil winding'], at: [26, 2], face: 'e', pose: 'stand', room: 'r' },   // the Lights shelves
    { id: '5-parts-2', type: 'storage', anim: 'browse', stock: ['filter', 'cartridge', 'membrane', 'oxygen cell', 'uv lamp'], at: [28, 5], face: 'e', pose: 'stand', room: 'r' },   // Filters
    { id: '5-parts-3', type: 'storage', anim: 'browse', stock: ['pump', 'valve', 'seal', 'nutrient pack', 'regulator'], at: [30, 5], face: 'e', pose: 'stand', room: 'r' },   // Plumbing
    { id: '5-parts-4', type: 'storage', anim: 'browse', stock: ['element', 'fan belt', 'compressor', 'bearing', 'control rod'], at: [32, 3], face: 'e', pose: 'stand', room: 'r' },   // Galley parts
    { id: '5-make-1', type: 'storage', anim: 'work', at: [22, 12], face: 'w', pose: 'work', room: 'f' },     // at the lathe
    { id: '5-make-2', type: 'storage', anim: 'work', at: [25, 9], face: 'e', pose: 'work', room: 'f' },      // beside the fabricator
    // restock runs (0.30.10, for the systems engineer's B3): loading a cart in the cargo hold, and taking or returning one at its dock
    { id: '5-hold-1', type: 'storage', anim: 'lift', at: [16, 11], face: 'e', pose: 'stand', room: 'c' },   // by the crate stack
    { id: '5-hold-2', type: 'storage', anim: 'lift', at: [13, 14], face: 's', pose: 'stand', room: 'c' },   // at the racks
    { id: '5-cart-1', type: 'storage', at: [19, 13], face: 'e', pose: 'stand', room: 'm' },                 // beside cart dock 1
    { id: '5-cart-2', type: 'storage', at: [19, 14], face: 'e', pose: 'stand', room: 'm' },                 // beside cart dock 2
    { id: '5-bay-1', type: 'work:works', at: [4, 9], face: 'n', pose: 'work', room: 'S' },
    { id: '5-bay-2', type: 'work:works', at: [7, 9], face: 'n', pose: 'work', room: 'S' },
    { id: '5-bay-3', type: 'work:works', at: [2, 4], face: 'w', pose: 'work', room: 'S' },
    { id: '5-booth-1', type: 'work:watch', at: [8, 14], face: 'e', pose: 'sit', room: 'b', xy: [8.75, 14.5], y: 0.5, cush: 0.5 },
    { id: '5-lift-1', type: 'lift-wait', at: [15, 6], face: 'e', pose: 'stand', room: '+' },
    { id: '5-lift-2', type: 'lift-wait', at: [15, 9], face: 'e', pose: 'stand', room: '+' },
    { id: '5-lift-3', type: 'lift-wait', at: [20, 6], face: 'w', pose: 'stand', room: '+' },
    { id: '5-lift-4', type: 'lift-wait', at: [20, 9], face: 'w', pose: 'stand', room: '+' },
    // utility rooms (0.30.3): one work:works place on each machine's panel tile, facing the machine
    { id: '5-o2-1-svc', machine: '5-o2-1', type: 'work:works', at: [35, 1], face: 'n', pose: 'work', room: 'a' },
    { id: '5-o2-2-svc', machine: '5-o2-2', type: 'work:works', at: [37, 1], face: 'n', pose: 'work', room: 'a' },
    { id: '5-electrolyser-1-svc', machine: '5-electrolyser-1', type: 'work:works', at: [36, 2], face: 'w', pose: 'work', room: 'a' },
    { id: '5-scrubber-1-svc', machine: '5-scrubber-1', type: 'work:works', at: [39, 3], face: 's', pose: 'work', room: 'a' },
    { id: '5-scrubber-2-svc', machine: '5-scrubber-2', type: 'work:works', at: [40, 3], face: 's', pose: 'work', room: 'a' },
    { id: '5-manifold-1-svc', machine: '5-manifold-1', type: 'work:works', at: [36, 14], face: 's', pose: 'work', room: 'n' },
    { id: '5-pump-1-svc', machine: '5-pump-1', type: 'work:works', at: [35, 11], face: 'w', pose: 'work', room: 'n' },
    { id: '5-pump-2-svc', machine: '5-pump-2', type: 'work:works', at: [35, 12], face: 'w', pose: 'work', room: 'n' },
    { id: '5-battery-1-svc', machine: '5-battery-1', type: 'work:works', at: [28, 12], face: 'n', pose: 'work', room: 'y' },
    { id: '5-battery-2-svc', machine: '5-battery-2', type: 'work:works', at: [33, 12], face: 'n', pose: 'work', room: 'y' },
    { id: '5-battery-3-svc', machine: '5-battery-3', type: 'work:works', at: [28, 14], face: 'n', pose: 'work', room: 'y' },
    { id: '5-battery-4-svc', machine: '5-battery-4', type: 'work:works', at: [33, 14], face: 'n', pose: 'work', room: 'y' },
    { id: '5-inverter-1-svc', machine: '5-inverter-1', type: 'work:works', at: [33, 10], face: 'n', pose: 'work', room: 'y' },
    { id: '5-junction-1-svc', machine: '5-junction-1', type: 'work:works', at: [19, 11], face: 'e', pose: 'work', room: 'u' },
    { id: '5-cartdock-1-svc', machine: '5-cartdock-1', type: 'work:works', at: [19, 12], face: 'e', pose: 'work', room: 'm' },
    { id: '5-cartdock-2-svc', machine: '5-cartdock-2', type: 'work:works', at: [19, 15], face: 'e', pose: 'work', room: 'm' },
    { id: '5-valve-1-svc', machine: '5-valve-1', type: 'work:works', at: [28, 0], face: 'n', pose: 'work', room: 'g' },
    { id: '5-valve-2-svc', machine: '5-valve-2', type: 'work:works', at: [29, 15], face: 's', pose: 'work', room: 'h' },
    { id: '5-fan-1-svc', machine: '5-fan-1', type: 'work:works', at: [36, 9], face: 'n', pose: 'work', room: 'F' },
    { id: '5-damper-1-svc', machine: '5-damper-1', type: 'work:works', at: [34, 6], face: 'w', pose: 'work', room: 'F' },
    { id: '5-damper-2-svc', machine: '5-damper-2', type: 'work:works', at: [34, 9], face: 'w', pose: 'work', room: 'F' },
  ],
  markings: [[21, 10, 2, 3], [25, 9, 3, 2], [26, 11, 2, 2], [35, 7, 3, 2]],   // keep-clear outlines: lathe, fabricator, welding bench, the main fan (0.47.3)
  dress(d) {
    for (const [key, tw, text] of d.plates) placeOnEdge('plate', key, tw, { text });
    for (const [key, tw] of d.workLights) placeOnEdge('workLight', key, tw);
    for (const [key, tw] of [['v,17,9', 'w'], ['v,19,9', 'e']]) placeOnEdge('liftPanel', key, tw);

    // Works bay: the job board and tool wall on the hull side, two benches, parts racks by the tea corner, kit lockers by the lobby doors
    placeWall('w', 'jobBoard', 'n', 5.6, { hitW: 2.6, cards: [
      ['Scrubber 2', 'Deck 4 · air', 'filter due', 'soon'], ['Galley oven', 'Deck 3 · galley', 'worn', 'soon'],
      ['Washer 3', 'Deck 4 · laundry', 'thumps on spin', 'routine'], ['Lamp, cabin 4-07', 'Deck 4', 'flickering', 'routine'],
      ['Lift doors', 'Deck 5', 'monthly service', 'routine'], ['Restock filters', 'Deck 5 · storage', 'shelf low', 'routine'] ],
      it: IT('Job board', 'Every fault, service and restock aboard ends up here, and anyone on duty can claim one. Quiet today, which the Chief says never lasts.') });
    placeWall('w', 'toolWall', 'n', 9.3, { hitW: 1.8, it: IT('Tool wall', 'Every tool has a painted outline, so you can see at a glance what\'s out. Something is always out.') });
    place('w', 'workbench', 5.2, 2.45, 'n', { it: IT('Workbench', 'A scrubber control unit with its lid off, halfway through a test. Whoever was on it has gone for tea.') });
    place('w', 'workbench', 8.7, 2.45, 'n', { w: 1.6, it: IT('Workbench', 'Clamped in the vice: a door motor from Deck 4, waiting for a new bearing.') });
    for (const z of [3.85, 5.2]) place('w', 'locker', 10.6, z, 'e', { it: IT('Kit lockers', 'Overalls, gloves, a hard hat and a torch for every Works tech. Yours has your name on a strip of tape.') });
    place('w', 'shelving', 10.66, 2.62, 'e', { it: IT('Parts racks', 'The bits you need ten times a day: fuses, seals, bulbs and filters. The tea corner hides behind them.') });
    place('w', 'crate', .55, 5.55, 's'); place('w', 'crate', 1.35, 5.6, 's', { turn: .2 });
    place('w', 'stool', 1.6, 3.7, 'w');
    place('w', 'workbench', .42, 4.3, 'w', { w: 1.2, it: IT('Your bench', 'A short bench under the bay window, with a view of the shuttle pad. An officer\'s, so it\'s yours.') });   // 0.53.4: 5-bench-you (M11)
    placeWall('w', 'nameBeam', 'n', BEAM.along, { it: IT('The beam', 'The cross beam over the Works bay, painted with the name of everyone who has served in Works, in whatever paint was to hand. The oldest ones have been touched up so often they stand out from the steel.') });   // 0.38.30: Name on the beam (BEAM)
    placeWall('w', 'notices', 'n', 7.65, { hitW: 1.0, it: IT('Notice board', 'Shift swaps, a lost-and-found glove, and a sign-up sheet for the Works quiz night. Chef Brennan is listed as \'judge, by force\'.') });
    // the Chief's office, seen through glass
    NO_FADE.add('o');
    place('o', 'desk', 1.5, .45, 'n');
    place('o', 'chair', 1.5, 1.25, 's');
    place('o', 'plant', 2.55, 2.5, 'e', { band: '#d9a441' });

    // tea corner: a little table by the porthole, an armchair and a stool, one warm lamp, a hot-water dispenser
    place('t', 'rug', 1.6, 1.2, 'n', { tex: rugLounge, w: 2.2, d: 1.8 });
    place('t', 'teaTable', 1.55, .7, 'n', { it: IT('Tea table', 'Two mugs, both cold, by the porthole. Works tea is strong enough to stand a spanner in.') });
    place('t', 'armchair', 2.55, .75, 'e', { it: IT('Armchair', 'Shaped exactly like whoever sits here most. Probably Pell.') });
    place('t', 'stool', .75, .7, 'w');
    place('t', 'floorLamp', 2.6, 2.55, 'e', { light: true });
    place('t', 'plant', 1.5, 2.6, 's', { band: '#d9a441' });
    place('t', 'dispenser', .5, 2.6, 's', { it: IT('Hot water', 'Always on. The Works crew would mutiny over anything else.') });

    // washroom
    furnish('q', 'washroom', { toilets: true });           // 0.38.27 (the user's): two toilets, no shower (showers are on Decks 2 and 4)

    // main storage: four aisles sorted by system, the counter by the door, and a dusty back corner
    place('r', 'counter', .4, 4.0, 'w', { it: IT('Check-out counter', 'Sign out what you take. The log says three filters left yesterday and nobody signed for them.') });
    [['Lights', 3.5], ['Filters', 5.5], ['Plumbing', 7.5], ['Galley parts', 9.67]].forEach(([name, x]) => {
      for (const z of [1.6, 2.8, 4.0]) place('r', 'shelving', x, z, 'e', { fadeGroup: 'r:' + name, it: shelfIt(name, { Lights: 'Bulbs, strips and spare lamp heads, sorted by deck.', Filters: 'Air filters in three sizes. The scrubber ones go fastest.',
        Plumbing: 'Seals, valves and pipe joints. One box is labelled DO NOT.', 'Galley parts': 'Oven elements, fan belts and a whole shelf for Chef Brennan\'s mixer.' }[name]) });   // shelfIt: tagged shelf: <id> (0.38.24)
      place('r', 'aisleSign', x, 4.85, 'n', { text: name });
    });
    place('r', 'tarpHeap', 9.45, .5, 'n', { it: IT('Under a tarp', 'A decorative fountain, still in its crate. Nobody remembers ordering it. The label says Deck 2.') });

    // machine shop: lathe, fabricator, welding bench, a bench in the middle and a rack of stock
    place('f', 'lathe', .45, 2.6, 'w', { it: IT('Lathe', 'For turning a shaft or a bushing when storage hasn\'t got one. Slower than fetching, but it never runs out.') });
    place('f', 'fabricator', 5.5, .55, 'n', { it: IT('Parts fabricator', 'Prints small parts from stock. Something is half finished in there, glowing faintly.') });
    place('f', 'weldBench', 6.45, 3.3, 'e', { it: IT('Welding bench', 'Mask, gas and a bracket that needs one more seam. The screen keeps the glare off everyone else.') });
    place('f', 'workbench', 3.3, 3.5, 'n', { w: 1.6, it: IT('Workbench', 'Drawings for a pump housing, weighed down with a coffee mug.') });
    place('f', 'shelving', 1.2, 5.55, 's', { it: IT('Bar stock', 'Rods, plate and tube for the lathe and the fabricator.') });
    wallFixed('f', 'notices', 'n', 1.0, { hitW: 1.0, it: IT('Order board', 'Little orders from the crew: a hook, a bracket, a stand for something. Pinned up on Mondays.') });   // 0.53.4: 5-shop-board (M10)

    // shuttle bay: the Tern on its pad, nose to the bay doors; floodlights along the hull; crates waiting for the cargo hold
    place('S', 'shuttle', 4.0, 7.5, 'e', { noBlock: true, block: DECKS[5].tern.block.map(([i, j]) => [i - 1, j]), roof: ternRoof, ramp: ternHinge });   // 0.38.18: the walk-in Tern (tiles x 2-7, rows 6-8)
    place('S', 'tapSpot', 1.5, 7.5, 'e', { hitH: 2.3, it: IT('Shuttle Tern', 'The Wren\'s shuttle. It brought you aboard, and one day it\'ll take you out on away jobs. The benches still smell of the last crew\'s coffee.') });   // the tap, on the cockpit: a tap inside the cabin walks you there
    for (const x of [1.5, 4.5, 7.5]) placeWall('S', 'workLight', 'n', x);
    place('S', 'crate', 6.4, 13.55, 's'); place('S', 'crate', 5.55, 13.6, 's', { turn: -.15 }); place('S', 'crate', 6.4, 12.9, 's', { turn: .1 });
    // the booth, the door gear and the fan hall: locked, seen through glass
    for (const r of ['b', 'd', 'F']) NO_FADE.add(r);
    place('b', 'boothConsole', 1.55, 1.5, 'e');
    place('b', 'chair', .9, 1.5, 'w');
    // the bay doors stand against the stern hull, so they hide with it when the cutaway lowers it
    const bd = place('S', 'bayDoors', .14, 6.7, 'w', { w: 10.2, it: IT('Bay doors', 'The whole stern of the bay opens to space. When it does, everyone stays behind the yellow line and the air goes somewhere first.') });
    staticRoot.remove(bd); deckRoot.add(bd); WALL_DECOR.push({ g: bd, e: EDGES.get('v,1,6') });
    place('d', 'doorGear', 1.5, 2.0, 'w');               // stays put: you watch it through the window
    // the spine: the ladder below the car, as on Deck 4. The trunks run behind the car's back wall here.
    NO_FADE.add('Z');
    place('Z', 'spineLadder', 1, .5, 'n', { it: SPINE_IT.ladder });
    place('F', 'bigFan', 2.6, 3.0, 'n', { block: [[1, 2], [2, 2], [3, 2], [1, 3], [2, 3], [3, 3]], it: IT('Main fan', 'The ship\'s lungs. Every deck\'s air comes through these five blades. Its panel is on the walkway in front.') });   // faces the default camera; the corridor window sees it side-on (0.47.3: you can walk in, so it blocks its tiles)
    // ---- utility rooms (Pillar 2, 0.30.3). Last in dress() and free of R(), so nothing above them changes ----
    // air plant: the electrolyser on the stern wall feeds two banks of oxygen cells on the port hull; two scrubber stacks on the Fan hall wall
    place('a', 'electrolyser', 1.02, 3.0, 'w', { it: IT('Electrolyser', 'Splits water into oxygen and hydrogen. The oxygen goes to the cells; the hydrogen goes somewhere you are told not to worry about.') });
    for (const [x, n] of [[2.0, 1], [4.0, 2]]) place('a', 'o2Bank', x, .47, 'n', { it: IT('Oxygen cells ' + n, 'Three glass columns, bubbling. The air every deck breathes starts here.') });
    for (const [x, n] of [[5.5, 1], [6.5, 2]]) place('a', 'scrubberStack', x, 4.5, 's', { it: IT('Main scrubber ' + n, 'One of the two big stacks that take the stale air back from every deck.') });
    place('a', 'ductRiser', 7.5, 4.5, 'n');
    place('a', 'pipeLine', 2.5, 1.3, 'n', { w: 3.0, y: 2.5, r: .14 });
    placeWall('a', 'workLight', 's', 6.5);
    // manifold room: the valve wall along the starboard hull, two water pumps on the stern wall, a pressure tank in the bow corner
    place('n', 'valveManifold', 3.0, 4.58, 's', { w: 3.6, it: IT('Valve manifold', 'Every deck\'s water, colour-coded. Fault tracing starts here: follow the colour, find the deck.') });
    for (const [z, n] of [[.5, 1], [1.5, 2]]) place('n', 'circPump', .5, z, 'w', { it: IT('Water pump ' + n, n === 1 ? 'The duty pump for the water main.' : 'The standby pump. Someone has written SPARE on it in marker.') });
    place('n', 'pressureTank', 7.5, .5, 'n', { r: .42, it: IT('Pressure tank', 'Keeps the water main steady when everyone showers at once, which is every morning at 06:30.') });
    place('n', 'pipeLine', 4.0, .5, 'n', { w: 7.0, y: 2.5, r: .14 });
    placeWall('n', 'workLight', 'n', 2.5);
    // battery room: four banks in two rows, the charge controller by the door, and the sign
    for (const [x, z, n] of [[1.0, 2.5, 1], [5.0, 2.5, 2], [1.0, 4.5, 3], [5.0, 4.5, 4]]) place('y', 'batteryBank', x, z, 'n', { it: IT('Battery bank ' + n, 'Eight big cells and their charge bars. The bars should all be green.') });
    place('y', 'breakerCabinet', 5.5, .345, 'n', { w: .76, it: IT('Charge controller', 'Decides which bank charges and which one rests. Its fan is the only sound in here.') });
    placeWall('y', 'plate', 'w', 1.5, { text: 'Tools out of pockets' });
    placeWall('y', 'workLight', 's', 3.0);
    // utility closet: the deck's power junction and its light relays
    place('u', 'breakerCabinet', 1.66, 1.5, 'e', { w: .7, it: IT('Breaker cabinet', 'Deck 5\'s power junction. The Works bay alone has its own row.') });
    wallFixed('w', 'extBracket', 's', 5.5, { hitW: .4, it: { ...IT('Fire extinguisher', 'Red, full, and checked every week: the tag says so. It comes off the bracket for the fire drill.'), drill: 'ext' } });   // 0.47.0: the drill (m3)
    wallFixed('w', 'bulkheadWheel', 's', 8.5, { hitW: .5, it: { ...IT('Bulkhead wheel', 'Four turns closes and dogs the bulkhead door by the bay. You turn it for the pressure drill, and hope never for real.'), drill: 'door' } });
    wallFixed('u', 'liftBrake', 'w', .5, { hitW: .6, it: { ...IT('Lift brake', 'The main lift\'s manual brake release, by the ladder. Turn it to let a stuck car down to the next deck.'), brake: true } });   // 0.47.0: incidents (m6)
    wallFixed('=', 'valvePanel', 'n', VALVE_PANELS[5].along, { hitW: 1.5, it: { ...IT('Pipe valves', 'Three valves on the main water line, numbered from upstream. Close the one before a leak.'), valves: 5 } });
    wallFixed('F', 'ductDamper', 'w', 1.5, { n: 1, hitW: .8, it: IT('Duct damper 1', 'Upper decks, 1-3. The flap that sends the fan\'s air up the spine to the decks above.') });   // 0.47.3: the air line (Step 3)
    wallFixed('F', 'ductDamper', 'w', 4.5, { n: 2, hitW: .8, it: IT('Duct damper 2', 'Lower decks, 4-6. The flap that sends the fan\'s air down to the decks below.') });
    placeWall('u', 'relayBoard', 'n', 1.5, { it: IT('Light relays', 'Deck 5\'s lights. The shuttle bay floods have a relay to themselves.') });
    // cart bay: two docks with a cart charging on each
    for (const [z, n] of [[1.0, 1], [3.0, 2]]) place('m', 'cartDock', 1.45, z, 'e', { dock: n, it: IT('Cart dock ' + n, n === 1 ? 'A hover hand cart, charging. The sticker says I BRAKE FOR NOBODY.' : 'A hover hand cart, charging, with a crate strap still hooked on.') });
    placeWall('m', 'workLight', 'w', 3.5);
    // cargo hold: heavy racks along the starboard hull, crate stacks by the walls, a clear floor for the carts
    for (const x of [1.0, 3.0, 5.0, 7.0]) place('c', 'cargoRack', x, 5.54, 's');
    for (const [x, z, tn] of [[7.5, .45, 0], [8.4, .45, .12], [7.6, 1.2, -.1], [8.4, 1.3, 0], [4.5, .4, .05], [5.3, .45, -.08], [.45, 4.5, .1]]) place('c', 'crate', x, z, 'n', { turn: tn });
    for (const x of [2.5, 6.5]) placeWall('c', 'workLight', 'n', x);
    deliveryCratesBuild();                               // the Wednesday delivery's crates, hidden until section 17 shows them (0.38.35)
    // pipe galleries: pipe runs along the hull, and a valve station halfway along each
    for (const [r, n, z0] of [['g', 10, .2], ['h', 13, .8]]) for (let x = 0; x < n; x += 2.5) {   // in short pieces, so the one near you fades the run
      const w = Math.min(2.5, n - x);
      place(r, 'pipeLine', x + w / 2, z0, 'n', { w, y: 2.35, r: .09 });
      place(r, 'pipeLine', x + w / 2, z0, 'n', { w, y: .35, r: .07, m: UT.pipes[1] });
    }
    placeWall('g', 'valveStation', 'n', 4.5, { it: IT('Valve station', 'Halfway along the port gallery: three valves and a gauge. Close the blue one and storage gets no water.') });
    placeWall('h', 'valveStation', 's', 8.5, { it: IT('Valve station', 'Halfway along the starboard gallery. The gauge has a sticky note: TAP IT.') });
    // the Ship health board (0.30.12), on the hull wall between the Chief's office glass and the job board
    placeWall('w', 'timeClock', 'n', 10.6, { hitW: .6, it: IT('Time clock', 'Clock in when your shift starts and out when it ends. Your card is the one with your name on it, in pencil.') });   // 0.61.13
    placeWall('w', 'healthBoard', 'n', 3.6, { hitW: .84, it: IT('Ship health', 'Every system aboard, how well it\'s running right now. When a bar goes amber, the job board fills up. When it goes red, the Chief stops drinking her tea.') });
    // lived-in touches (0.30.12): a sign in the air plant, the cart bay's calendar, a mug on the closet's breakers
    placeWall('a', 'plate', 'w', 1.0, { text: 'No naked flames' });
    placeWall('m', 'calendar', 'w', .5, { upTo: 9, ring: 12 });
    place('u', 'mug', 1.7, 1.3, 'e', { y: 1.995, tall: true });
    placeWall('t', 'mugRack', 's', 1.1, { hitW: .8, it: IT('Mug rack', 'Six hooks over the hot water, a Works mug on five of them. The sixth hook is empty. Nobody says whose it is.') });   // Pillar 4 (seat 8, 0.38.9)
  },
};
for (const [key, r] of Object.entries(DECKS[5].sealed)) DECKS[5].closedDoors[key] = { t: DECKS[5].rooms[r].name, x: DECKS[5].rooms[r].tap };

// ---- Wall kit for Pillar 4's arrival evening (seat 8, 0.38.9, the deck architect; made at load, no R(), existing materials) ----
Object.assign(WALL_KIT, {
  keepsakeShelf(g) {                                     // a plank above your bunk's head, for the keepsakes friends give you (8b draws them)
    box(.92, .04, .2, M.wood, 0, 2.15, .1, g);
    for (const x of [-.38, .38]) box(.03, .12, .16, M.slateDark, x, 2.07, .09, g);
  },
  mugRack(g) {                                           // six hooks over the hot water, five Works mugs and one free hook (yours, one day)
    box(.72, .1, .03, M.wood, 0, 1.55, .015, g);
    [KM.red, KM.teal, KM.gold, M.cream, KM.teal, null].forEach((m, k) => {
      const x = -.3 + k * .12; cyl(.008, .008, .05, M.metal, x, 1.52, .045, g, 6).rotation.x = Math.PI / 2;
      if (m) { cyl(.036, .032, .08, m, x, 1.44, .075, g, 12); box(.012, .04, .02, m, x + .042, 1.44, .075, g); }
    });
  },
});
// ---- the time clock (0.61.13, the career engineer; made at load, no R(), existing materials): a small console on the
// Works bay wall with a green screen and a rack of time cards beside it. You and the Works crew clock in and out here
Object.assign(WALL_KIT, {
  timeClock(g) {
    box(.34, .44, .07, M.slateDark, -.08, 1.42, .035, g);   // the console
    box(.22, .1, .02, KM.vacant, -.08, 1.53, .08, g);       // its screen
    box(.12, .05, .03, M.metal, -.08, 1.33, .085, g);       // the card slot
    box(.16, .5, .04, M.metal, .2, 1.4, .02, g);            // the card rack
    for (let k = 0; k < 5; k++) box(.1, .08, .012, KM.paper, .2, 1.22 + k * .09, .046, g);   // time cards
  },
});
// ---- Gym kit (Pillar 3, C9, 0.38.2, the deck architect; made at load, no R()): a punch bag on its stand and a single stretching mat ----
Object.assign(KIT, {
  punchBag(g, o = {}) {                                  // a stand with an arm, and a bag that swings while someone's punching (MOVERS)
    box(.6, .04, .9, GYM.plate, 0, .02, 0, g);           // the base plate
    box(.08, 2.3, .08, GYM.frame, 0, 1.15, -.38, g); box(.06, .06, .52, GYM.frame, 0, 2.27, -.12, g);   // the post, and the arm out over the bag
    const pv = new THREE.Group(); pv.position.set(0, 2.24, .1); g.add(pv);
    cyl(.012, .012, .3, GYM.mat[2], 0, -.15, 0, pv, 6); cyl(.17, .17, .85, GYM.mat[2], 0, -.725, 0, pv, 14);   // the strap and the bag, one material
    mergeMeshes(pv); for (const m of pv.children) m.userData.noMerge = true;   // one mesh, kept out of the deck's merge so it can swing
    if (o.place) {
      let v = 0, ph = 0;
      MOVERS.push({ place: o.place, tick(dt, on) {
        if (!on && v === 0) return;
        v += ((on ? 1 : 0) - v) * Math.min(1, dt * 3); if (!on && v < .01) { v = 0; pv.rotation.x = 0; return; }
        ph += dt * 4.4; pv.rotation.x = Math.max(0, Math.sin(ph)) * .14 * v;   // knocked back, swings home
      } });
    }
    return { w: .6, d: .9 };
  },
  gymMat(g) {                                            // one stretching mat, rolled out
    const m = box(.6, .015, 1.7, GYM.mat[1], 0, .008, 0, g); m.castShadow = false;
    return { w: .6, d: 1.7, noBlock: true };
  },
  // 0.38.28: an exercise bike, the rider facing -z (the handlebars and flywheel); the saddle's top at .62, .25 behind the
  // centre; the crank at (0, .32, -.1). No R(). With o.place the flywheel turns while someone rides (MOVERS)
  exerciseBike(g, o = {}) {
    box(.42, .05, 1.0, GYM.frame, 0, .025, -.05, g);                                   // the foot rail
    box(.06, .5, .06, GYM.frame, 0, .33, .22, g); box(.04, .1, .04, GYM.chrome, 0, .55, .24, g);   // the seat post
    box(.22, .05, .26, GYM.rubber, 0, .595, .25, g);                                   // the saddle
    box(.08, .55, .08, GYM.frame, 0, .42, -.4, g).rotation.x = -.25;                   // the stem, leaning back
    box(.46, .04, .04, GYM.chrome, 0, .95, -.3, g); box(.16, .1, .03, MED.screen, 0, .9, -.36, g);   // the bars and a little screen
    box(.38, .16, .08, GYM.frame, 0, .32, -.1, g);                                     // the crank housing
    for (const x of [-.13, .13]) box(.03, .03, .16, GYM.accent, x, .32, -.1, g);       // the pedals' arms
    const fw = cyl(.2, .2, .07, GYM.accent, 0, .26, -.48, g, 20); fw.rotation.z = Math.PI / 2;   // the flywheel
    if (o.place) {
      fw.userData.noMerge = true; let v = 0;
      MOVERS.push({ place: o.place, tick(dt, on) {
        if (!on && v === 0) return;
        v += ((on ? 1 : 0) - v) * Math.min(1, dt * 3); if (!on && v < .01) v = 0;
        fw.rotation.x = (fw.rotation.x + dt * v * 6) % (Math.PI * 2);
      } });
    }
    return { w: .45, d: 1.1 };
  },
});
// ---- Deck 3 kit (A5b, the bridge architect; made at load, no R()): the crew store's till and baskets ----
Object.assign(KIT, {
  till(g) {                                              // a badge scanner and a little screen, standing on the store counter
    box(.36, .05, .3, WM.paintDark, 0, 1.0, 0, g);                 // overlaps the counter top (.97), never level with it
    const sc = box(.3, .2, .03, WM.paintDark, 0, 1.13, -.08, g); sc.rotation.x = -.25;
    const ss = box(.26, .16, .01, WM.screen, 0, 1.13, -.063, g); ss.rotation.x = -.25;
    box(.12, .02, .1, MED.screen, .09, 1.03, .07, g);    // the badge pad
    return { w: .36, d: .3, noBlock: true };
  },
  basketStack(g) {                                       // shopping baskets, stacked by the door
    for (let k = 0; k < 4; k++) {
      const y = .04 + k * .09, m = SHOP.goods[[2, 3, 0, 2][k]];
      box(.42, .02, .3, m, 0, y, 0, g);
      for (const x of [-.2, .2]) box(.02, .16, .3, m, x, y + .08, 0, g);
      for (const z of [-.14, .14]) box(.42, .16, .02, m, 0, y + .08, z, g);
    }
    const h = cyl(.012, .012, .3, M.metal, 0, .5, 0, g, 6); h.rotation.x = Math.PI / 2;
    return { w: .45, d: .34 };
  },
});
// ---- utility rooms on Decks 1 and 3 (A5b; made at load, no R()). Only materials these decks already draw, so the
// rooms add few draw calls. Every piece's back is local -z (against a wall); its front, where someone works, is +z.
const pipeX = (r, len, m, x, y, z, g) => { const p = cyl(r, r, len, m, x, y, z, g, 10); p.rotation.z = Math.PI / 2; return p; };
const pipeZ = (r, len, m, x, y, z, g) => { const p = cyl(r, r, len, m, x, y, z, g, 10); p.rotation.x = Math.PI / 2; return p; };
const statusLights = (g, x0, y, z, n, k0 = 0) => { for (let k = 0; k < n; k++) box(.05, .05, .02, (k + k0) % 4 === 3 ? WM.screenAmber : WM.screen, x0 + k * .09, y, z, g); };
Object.assign(KIT, {
  recyclerTanks(g) {                                     // the water recycler: two settling tanks with sight glasses, a control head between
    for (const x of [-.7, .7]) {
      box(1.1, .08, 1.1, M.slateDark, x, .04, -.05, g);
      cyl(.5, .5, 2.05, WM.steel, x, 1.1, -.05, g, 20);
      for (const y of [.45, 1.15, 1.85]) cyl(.53, .53, .06, M.slateDark, x, y, -.05, g, 20);
      soft(WM.steelTop, x, 2.12, -.05, .5, .16, .5, g);
      box(.08, 1.1, .04, GD.water, x, 1.15, .46, g);   // the sight glass, sunk into the tank wall
    }
    box(.42, .95, .3, WM.paintDark, 0, 1.05, .3, g); box(.34, .22, .02, MED.screen, 0, 1.3, .455, g);
    statusLights(g, -.13, 1.05, .455, 4);
    pipeX(.08, 1.5, M.metal, 0, 1.95, -.05, g);
    return { w: 2.6, d: 1.4, tall: true };
  },
  filterBank(g) {                                        // the filter bank: white cartridges between two steel headers
    box(1.9, 1.6, .06, M.slateDark, 0, .85, -.4, g);
    for (const y of [.24, 1.5]) box(1.9, .14, .6, WM.steel, 0, y, -.08, g);
    for (let k = 0; k < 6; k++) cyl(.1, .1, 1.16, M.ceramic, -.75 + k * .3, .87, -.04, g, 12);
    cyl(.08, .08, .03, M.trim, .82, 1.72, .2, g, 14).rotation.x = Math.PI / 2;
    return { w: 1.9, d: .9 };
  },
  pumpSkid(g) {                                          // two circulation pumps on one skid, their outlets rising to a header
    box(1.8, .12, 1.1, M.slateDark, 0, .06, 0, g);
    for (const x of [-.45, .45]) {
      pipeZ(.22, .6, WM.paintDark, x, .45, .15, g); pipeZ(.28, .22, WM.steel, x, .45, -.28, g);
      cyl(.07, .07, 1.65, M.metal, x, 1.35, -.32, g, 10);
    }
    pipeX(.08, 1.3, M.metal, 0, 2.18, -.32, g);
    box(.3, .3, .04, WM.paintDark, 0, 1.05, .25, g); statusLights(g, -.09, 1.1, .275, 3);
    return { w: 1.8, d: 1.2 };
  },
  uvUnit(g) {                                            // the UV steriliser: a lamp tube in a steel sleeve, glowing through a slot
    pipeX(.19, 1.6, WM.steel, 0, 1.1, 0, g);
    box(.7, .07, .03, MED.screen, 0, 1.1, .185, g);
    for (const x of [-.6, .6]) box(.07, 1.05, .32, M.slateDark, x, .52, -.06, g);
    box(.42, .3, .2, WM.paintDark, 0, .56, -.12, g);
    return { w: 1.8, d: .7 };
  },
  cleanTank(g) {                                         // the clean-water tank, with a level gauge and a manway on top
    box(2.4, 1.6, 1.2, WM.steel, 0, .82, 0, g);
    for (const y of [.42, 1.3]) box(2.44, .06, 1.24, M.slateDark, 0, y, 0, g);
    box(.08, 1.2, .03, GD.water, .9, .85, .61, g);
    cyl(.26, .26, .06, M.slateDark, 0, 1.64, 0, g, 18);
    return { w: 2.6, d: 1.4 };
  },
  risers(g) {                                            // two water risers, floor to deckhead, up the spine
    for (const x of [-.45, .45]) {
      cyl(.13, .13, 2.74, M.metal, x, 1.37, 0, g, 12);
      for (const y of [.6, 1.6, 2.5]) cyl(.18, .18, .06, M.slateDark, x, y, 0, g, 12);
    }
    const w = new THREE.Mesh(new THREE.TorusGeometry(.14, .025, 6, 16), WM.red); w.position.set(.45, 1.15, .17); g.add(w);
    return { w: 1.8, d: .5 };
  },
  sump(g) {                                              // the drain sump: a low grated pit with a little pump
    box(1.8, .06, .8, M.slateDark, 0, .03, 0, g);
    for (let k = 0; k < 7; k++) box(1.6, .03, .04, M.metal, 0, .075, -.3 + k * .1, g);
    cyl(.12, .12, .3, WM.paintDark, .6, .2, 0, g, 12);
    return { w: 1.8, d: .8 };
  },
  extractorUnit(g) {                                     // the galley plant: the hood ducts' fan, its motor and the grease filters
    pipeZ(.4, .5, WM.steel, -.4, 1.5, 0, g);
    box(.6, .85, .5, WM.steel, -.4, 2.3, -.1, g);
    box(.7, .5, .08, M.metal, .5, 1.45, .25, g);
    box(.4, .45, .4, WM.paintDark, .5, .62, 0, g); box(1.9, .1, .7, M.slateDark, 0, .05, 0, g);
    statusLights(g, .4, .8, .205, 3);
    return { w: 1.9, d: .8 };
  },
  chillerUnit(g) {                                       // the cold store's chiller, with the dishwasher pumps beside it
    box(.8, .7, .6, WM.paintDark, -.45, .35, 0, g); box(.24, .14, .02, WM.screen, -.45, .55, .31, g);
    box(.9, 1.25, .3, M.metal, .42, .9, -.15, g);
    for (let k = 0; k < 6; k++) box(.86, .02, .04, M.slateDark, .42, .4 + k * .2, .02, g);
    for (const x of [-.65, -.3]) cyl(.13, .13, .32, WM.steel, x, .88, .05, g, 12);
    return { w: 1.9, d: .8 };
  },
  nutrientTanks(g) {                                     // two nutrient tanks and the dosing unit that mixes the garden's feed
    for (const x of [-.45, .45]) {
      cyl(.38, .38, 1.3, WM.steel, x, .7, -.05, g, 18); cyl(.4, .4, .06, M.slateDark, x, 1.0, -.05, g, 18);
      box(.06, .8, .02, GD.water, x, .72, .34, g);
    }
    box(.36, .5, .24, WM.paintDark, 0, 1.15, .32, g); statusLights(g, -.09, 1.25, .445, 3);
    return { w: 1.9, d: 1.2 };
  },
  irrigationPump(g) {                                    // the garden's pump and the valve manifold out to the beds and racks
    box(1.5, .12, .9, M.slateDark, 0, .06, 0, g);
    pipeZ(.2, .55, WM.paintDark, -.35, .42, .1, g); pipeZ(.25, .2, WM.steel, -.35, .42, -.25, g);
    pipeX(.07, 1.4, M.metal, 0, .95, -.3, g);
    for (let k = 0; k < 4; k++) { const v = new THREE.Mesh(new THREE.TorusGeometry(.07, .015, 6, 12), WM.red); v.position.set(-.45 + k * .3, 1.1, -.3); v.rotation.x = Math.PI / 2; g.add(v); cyl(.02, .02, .14, M.metal, -.45 + k * .3, 1.02, -.3, g, 6); }
    return { w: 1.6, d: 1.0 };
  },
  headerPipes(g) {                                       // three header pipes along a wall, on brackets
    for (const y of [.5, .9, 1.3]) pipeX(.07, 2.6, M.metal, 0, y, 0, g);
    for (const x of [-1.1, 0, 1.1]) box(.06, 1.5, .22, M.slateDark, x, .75, -.06, g);
    return { w: 2.6, d: .4 };
  },
  relayBank(g, o = {}) {                                 // a bank of relay cabinets with blue status lights; o.w wide (was relayRack, which Deck 2's kit also names)
    const w = o.w || 2.8;
    box(w, 2.0, .6, M.slateDark, 0, 1.0, 0, g);
    for (let x = -w / 2 + .32; x < w / 2 - .2; x += .62) { box(.56, 1.8, .02, WM.paintDark, x, 1.0, .31, g); statusLights(g, x - .2, 1.72, .325, 5, Math.round(x * 10)); statusLights(g, x - .2, 1.6, .325, 5, Math.round(x * 7) + 1); }
    return { w, d: .6, tall: true };
  },
  cabinet(g, o = {}) {                                   // a wall cabinet: breakers (o.breakers) or relay lights
    box(1.8, 1.8, .5, M.slateDark, 0, .9, 0, g); box(1.7, 1.6, .02, WM.paintDark, 0, .95, .26, g);
    if (o.breakers) for (const y of [.65, .9, 1.15, 1.4]) box(1.4, .1, .03, M.metal, 0, y, .27, g);
    else for (const y of [.8, 1.0, 1.2, 1.4]) statusLights(g, -.6, y, .275, 14, Math.round(y * 10));
    box(.4, .12, .02, WM.paintGold, 0, 1.62, .275, g);
    return { w: 1.8, d: .5, tall: true };
  },
  dataBus(g) {                                           // the bridge data bus: a low junction box where every station's cables meet
    box(1.6, .6, .5, M.slateDark, 0, .3, 0, g); box(1.5, .5, .02, WM.paintDark, 0, .32, .26, g);
    for (let k = 0; k < 6; k++) cyl(.03, .03, .1, M.metal, -.6 + k * .24, .55, .26, g, 8).rotation.x = Math.PI / 2;
    statusLights(g, -.3, .2, .275, 8);
    [WM.paintGold, WM.paintDark].forEach((m, k) => pipeX(.04, 1.8, m, 0, .64, -.12 + k * .17, g));   // cables out to the trays
    return { w: 1.8, d: .6 };
  },
  floorCableTray(g) {                                    // a cable tray on legs, bundles of cable along it (was cableTray, which clashed with Deck 6's wall tray)
    box(1.8, .05, .45, M.metal, 0, .3, 0, g);
    for (const x of [-.8, .8]) box(.05, .28, .4, M.slateDark, x, .14, 0, g);
    [WM.paintGold, WM.red, WM.paintDark].forEach((m, k) => pipeX(.035, 1.8, m, 0, .36, -.12 + k * .12, g));
    return { w: 1.8, d: .5 };
  },
});
Object.assign(WALL_KIT, {
  relayBox(g) {                                          // a wall-mounted light relay box, its conduit running up to the deckhead
    box(.6, .5, .16, WM.paintDark, 0, 1.5, .08, g); statusLights(g, -.18, 1.6, .17, 5);
    box(.3, .06, .02, WM.paintGold, 0, 1.38, .17, g);
    cyl(.035, .035, 1.05, M.metal, 0, 2.27, .08, g, 8);
  },
  // lived-in touches for the utility rooms (answers pass, row 31): made from shared materials, nothing coplanar
  wallCalendar(g) {                                      // a paper wall calendar, this month's days crossed off (not the Deck 6 architect's calendar)
    box(.42, .56, .01, KM.paper, 0, 1.55, .02, g); box(.42, .12, .01, KM.red, 0, 1.77, .03, g);
    for (let k = 0; k < 9; k++) box(.04, .04, .006, M.slateDark, -.15 + (k % 5) * .075, 1.62 - Math.floor(k / 5) * .075, .029, g);
    cyl(.012, .012, .03, M.metal, 0, 1.86, .02, g, 6).rotation.x = Math.PI / 2;
  },
  handSign(g) {                                          // a hand-lettered card, taped up at the corners
    box(.38, .25, .01, KM.note, 0, 1.45, .02, g);
    [[-.03, .28, 1.51], [-.06, .22, 1.455], [0, .26, 1.4]].forEach(([x, w, y]) => box(w, .018, .006, M.slateDark, x, y, .028, g));   // the lettering
    for (const x of [-.17, .17]) box(.07, .025, .012, M.ceramic, x, 1.57, .03, g);
  },
  radioShelf(g) {                                        // a little wall shelf: someone's radio, a mug and a flask
    box(.62, .03, .2, M.wood, 0, 1.15, .1, g);
    box(.26, .15, .1, WM.paintDark, -.12, 1.24, .1, g); box(.1, .1, .01, M.slateDark, -.18, 1.24, .155, g);
    box(.05, .02, .01, WM.screenAmber, -.06, 1.27, .155, g);
    cyl(.006, .006, .32, M.metal, -.03, 1.43, .08, g, 4).rotation.z = -.35;
    cyl(.04, .035, .09, M.ceramic, .1, 1.21, .1, g, 10); box(.015, .05, .03, M.ceramic, .148, 1.21, .1, g);
    cyl(.035, .035, .2, M.metal, .23, 1.265, .1, g, 10);
  },
  mugRail(g) {                                           // a hook rail by the door, mugs hanging from it
    box(.5, .03, .03, M.metal, 0, 1.62, .03, g);
    [[-.15, M.ceramic], [.0, KM.teal], [.15, KM.red]].forEach(([x, m]) => {
      cyl(.04, .035, .09, m, x, 1.53, .07, g, 10); box(.012, .05, .02, M.metal, x, 1.6, .045, g);
    });
  },
});

