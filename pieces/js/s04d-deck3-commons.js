// =====================================================================
// DECK 3: COMMONS (step 6d, turn 1: the shell)
// From deck3-plan.html. A promenade runs stern to bow down the middle, with the lift in a plaza halfway along.
// Rooms are walkable and named but not furnished yet: the mess hall and galley come in turn 2, the lounge
// in turn 3, and the infirmary, garden, gym, store and booths in turn 4.
// =====================================================================
DECKS[3] = {
  num: 3, name: 'Commons', seed: 30307,
  blurb: 'Mess hall, lounge, garden', arrive: 'The promenade runs stern to bow. Mess hall and galley to port, the garden aft, the lounge in the bow.',
  lift: [20, 11],                                  // car rows 9-11, ladder row 12: the same world spot as Decks 4 and 5
  map: [
    '..GGGGGGGGGGIIIIIIIIIIIMMMMMMMMMMMMCCCCggLLLL.......',
    '..GGGGGGGGGGIIIIIIIIIIIMMMMMMMMMMMMCCCCggLLLLLL.....',
    '..GGGGGGGGGGIIIIIIIIIIIMMMMMMMMMMMMCCCCggLLLLLLL....',
    '..GGGGGGGGGGIIIIIIIIIIIMMMMMMMMMMMMKKKKKKLLLLLLLL...',
    '..GGGGGGGGGGIIIIIIIIIIIMMMMMMMMMMMMKKKKKKLLLLLLLLL..',
    '..GGGGGGGGGGIIIIIIIIIIIMMMMMMMMMMMMKKKKKKLLLLLLLLLL.',
    '..GGGGGGGGGGXXXXX++++++MMMMMMMMMMMMKKKKKKLLLLLLLLLL.',
    '..GGGGGGGGGGXXXXX++++++MMMMMMMMMMMMKKKKKKLLLLLLLLLL.',
    '..GGGGGGGGGGXXXXX++++++MMMMMMMMMMMMKKKKKKLLLLLLLLLLL',
    '..GGGGGGGGGG=====++@@++==================LLLLLLLLLLL',
    '..GGGGGGGGGG=====++@@++==================LLLLLLLLLLL',
    '..GGGGGGGGGG=====++@@++==================LLLLLLLLLLL',
    '..GGGGGGGGGG=====++ZZ++==================LLLLLLLLLLL',
    '..GGGGGGGGGGRRRRR++++++FFFFFFFFFSSSSBBBBBLLLLLLLLLLL',
    '..GGGGGGGGGGRRRRR++++++FFFFFFFFFSSSSBBBBBLLLLLLLLLL.',
    '..GGGGGGGGGGRRRRR++++++FFFFFFFFFSSSSBBBBBLLLLLLLLLL.',
    '..GGGGGGGGGGRRRRRwwwwwwFFFFFFFFFSSSSBBBBBLLLLLLLLLL.',
    '..iiiiGGGGGGRRRRRwwwwwwFFFFFFFFFSSSSBBBBBLLLLLLLLL..',
    '..iiiiGGGGGGRRRRRwwwwwwFFFFFFFFFSSSSBBBBBLLLLLLLL...',
    '..iiiiGGGGGGRRRRRwwwwwwFFFFFFFFFSSSSBBBBBLLLLLLL....',
    '..iiiiGGGGGGRRRRRwwwwwwFFFFFFFFFSSSSBBBBBLLLLLL.....',
    '..iiiiGGGGGGRRRRRwwwwwwFFFFFFFFFSSSSBBBBBLLLL.......',
  ],
  doors: {
    'v,19,9': 'lift', 'v,19,10': 'lift', 'v,19,11': 'lift', 'v,21,9': 'lift', 'v,21,10': 'lift', 'v,21,11': 'lift',
    'h,19,13': 'glass', 'h,20,13': 'hatch',                                                // the ladder, behind glass, with its hatch
    'v,12,10': 'door', 'v,12,11': 'door', 'v,12,9': 'glass', 'v,12,12': 'glass',          // glass doors into the garden at the promenade's aft end
    'h,19,6': 'door', 'h,20,6': 'door', 'h,18,6': 'glass', 'h,21,6': 'glass',            // infirmary: wide doors off the plaza
    'h,14,6': 'door',                                                                       // ward to exam room
    'v,23,7': 'door',                                                                       // mess hall from the plaza
    'h,25,9': 'door', 'h,26,9': 'door', 'h,31,9': 'door', 'h,32,9': 'door',               // mess hall onto the promenade...
    'h,24,9': 'glass', 'h,27,9': 'glass', 'h,28,9': 'glass', 'h,29,9': 'glass', 'h,30,9': 'glass', 'h,33,9': 'glass', 'h,34,9': 'glass',   // ...glass between
    'v,35,4': 'pass', 'v,35,5': 'pass', 'v,35,6': 'pass', 'v,35,8': 'door',             // the serving counter, and the staff door
    'h,38,9': 'door',                                                                       // galley back door: carts from the lift
    'h,36,3': 'door', 'h,39,3': 'hatch',                                                    // walk-in cold store; galley plant
    'v,41,6': 'door',                                                                       // galley to the back of the bar
    'v,41,10': 'door', 'v,41,11': 'door', 'v,41,9': 'glass', 'v,41,12': 'glass',          // lounge doors at the promenade's bow end
    'h,27,13': 'door', 'h,24,13': 'glass', 'h,25,13': 'glass', 'h,29,13': 'glass', 'h,30,13': 'glass',   // gym, with windows on the promenade
    'h,33,13': 'door', 'h,34,13': 'glass',                                                  // crew store and its shop window
    'h,38,13': 'door',                                                                      // call-home booths
    'h,20,16': 'door',                                                                      // washrooms
    'v,17,14': 'hatch', 'h,3,17': 'hatch',                                                  // recycler from the plaza; irrigation from the garden
  },
  sealed: { 'h,39,3': 'g', 'v,17,14': 'R', 'h,3,17': 'i' },
  // Pillar 2 A5b: the three utility rooms are built (plans/deck3-plan.html, "Utility rooms"). Their hatches are service hatches:
  // the player and Works crew pass, everyone else doesn't (see hatchPassable).
  service: [{ key: 'h,39,3', tier: 1 }, { key: 'v,17,14', tier: 2 }, { key: 'h,3,17', tier: 2 }],   // galley plant (a fan closet), water recycler, irrigation (answers pass row 4)
  plates: [
    ['h,17,6', 's', 'Infirmary'], ['h,23,9', 's', 'Mess hall'], ['h,37,9', 's', 'Galley'], ['h,26,13', 'n', 'Gym'],
    ['h,32,13', 'n', 'Store'], ['h,37,13', 'n', 'Call booths'], ['h,21,16', 'n', 'Washrooms'], ['h,19,9', 'n', 'Lift'],
  ],
  rooms: {
    '=': { name: 'Promenade', floor: 'deck', hall: true },
    '+': { name: 'Lift plaza', floor: 'lobby', hall: true },
    '@': { name: 'Main lift', floor: 'lift' },
    Z: { name: 'Spine ladder', floor: 'grate', spine: true },
    M: { name: 'Mess hall', floor: 'mess' },
    K: { name: 'Galley', floor: 'tile' },
    C: { name: 'Cold store', floor: 'steel' },
    L: { name: 'Bow lounge', floor: 'wood' },
    I: { name: 'Infirmary', floor: 'tile' },
    X: { name: 'Exam room', floor: 'tile' },
    G: { name: 'Hydroponics garden', floor: 'garden' },
    w: { name: 'Washrooms', floor: 'tile' },
    F: { name: 'Gym', floor: 'gym' },
    S: { name: 'Crew store', floor: 'warm' },
    B: { name: 'Call-home booths', floor: 'warm' },
    // sealed until their tier
    g: { name: 'Galley plant', floor: 'grate', still: true, tap: 'Extractor fans, the dishwasher pumps and the cold store\'s chillers. Tier 1 access, once the job list is running.' },
    R: { name: 'Water recycler', floor: 'steel', still: true, tap: 'Every deck\'s water comes back here, gets cleaned and goes out again. When it struggles, the showers on Deck 4 run weak.' },
    i: { name: 'Irrigation room', floor: 'steel', still: true, tap: 'Nutrient tanks and pumps for the garden.' },
  },
  windows: ['M', 'L', 'I', 'G', 'F', 'B'].map(room => ({ room })),
  closedDoors: {
    'h,20,13': { t: 'Spine ladder', x: 'The maintenance ladder runs the whole height of the ship, beside the lift. Crawlways branch off it on every deck. Tier 2 access.' },
  },
  hull: { sternX: 2, stern: 2, bowFrom: 40, bowLen: 11.6, byFace: true },   // one hull piece per facing: smooth stripes (answers pass, row 33)
  // the bow lounge's curves: the bar sweeping out from the aft wall round the galley door, and two planted glass
  // screens on one arc, splitting the lively bar end from the quiet window end with the way through left open
  curves: [
    { kind: 'bar', arc: [41, 5.6, 2.6, -90, 90], out: -1, it: { t: 'The bar', x: 'A curved bar in dark wood with a brass foot rail, lit from underneath. Stocked from the galley through the door behind it. Juice, tea and a short list of things the Captain approves of.', bar: true } },   // bar: the bar order's tap (0.38.24)
    { kind: 'glass', arc: [40, 11, 7, -38, -23], it: { t: 'Glass screen', x: 'Planted low, glass above: it keeps the bar\'s noise at the bar end without hiding the view.' } },
    { kind: 'glass', arc: [40, 11, 7, 23, 38] },
  ],
  // Pillar 1 places (workstream 3b, data only: nothing draws them yet). Every spot where someone does something, in the
  // plan's format, plus two fields: xy, the exact spot in tile units (a seat can sit off its tile's centre, and a tile can
  // hold two seats), and walk, the tile a person walks to first (the place's own tile when it's walkable, otherwise the
  // nearest reachable tile in the same room, within 2.5 m). Generated from the furniture's own positions, then kept as fixed data.
  // the machines in Deck 3's utility rooms and galley (Pillar 2 plan, "Machines and jobs"); each has a work:works place on its panel tile
  machines: [
    { id: '3-oven-1', kind: 'oven', at: [37, 3], room: 'K', face: 's', panel: [37, 4], look: { lamp: [0, 1.2, .41], drip: [0, .9, .45], light: [0, 2.1, .41] } },
    { id: '3-oven-2', kind: 'oven', at: [38, 3], room: 'K', face: 's', panel: [38, 4], look: { lamp: [0, 1.2, .41], drip: [0, .9, .45], light: [0, 2.1, .41] } },
    { id: '3-range-1', kind: 'range', at: [40, 4], room: 'K', face: 'w', panel: [39, 4], look: { lamp: [0, .85, .37], drip: [0, .82, .41], light: [0, 2.1, .37] } },
    { id: '3-galleyplant-1', kind: 'galleyplant', at: [39, 0], room: 'g', face: 's', panel: [39, 1], look: { lamp: [0, 1.2, .35], drip: [0, .9, .39], light: [0, 2.1, .35] } },
    { id: '3-chiller-1', kind: 'chiller', at: [40, 1], room: 'g', face: 'w', panel: [39, 2], look: { lamp: [0, 1.2, .32], drip: [0, .9, .36], light: [0, 2.1, .32] } },
    { id: '3-recycler-1', kind: 'recycler', at: [12, 15], room: 'R', face: 'e', panel: [14, 16],
      look: { lamp: [-1, 1.62, .98], drip: [-1, .9, 1.04], light: [-1, 2.1, .98], screen: [-1, 1.3, .975, .34, .22] } },   // on the control head, between the tanks
    { id: '3-filter-1', kind: 'filter', at: [12, 19], room: 'R', face: 'e', panel: [13, 19], look: { lamp: [0, 1.2, .32], drip: [0, .9, .36], light: [0, 2.1, .32] } },
    { id: '3-pump-1', kind: 'pump', at: [16, 16], room: 'R', face: 'w', panel: [15, 17], look: { lamp: [0, 1.2, .8], drip: [0, .9, .84], light: [0, 2.1, .8] } },
    { id: '3-uv-1', kind: 'uv', at: [12, 13], room: 'R', face: 's', panel: [14, 13], look: { lamp: [0, 1.13, .15], drip: [0, .9, .19], light: [0, 2.1, .15] } },
    { id: '3-lights-1', kind: 'lights', at: [16, 15], room: 'R', face: 'w', panel: [16, 15] },
    { id: '3-nutrient-1', kind: 'nutrient', at: [5, 18], room: 'i', face: 'w', panel: [4, 18], look: { lamp: [0, 1.2, .7], drip: [0, .9, .74], light: [0, 2.1, .7] } },
    { id: '3-irrigation-1', kind: 'irrigation', at: [5, 20], room: 'i', face: 'w', panel: [4, 20], look: { lamp: [0, .96, .6], drip: [0, .9, .64], light: [0, 2.1, .6] } },
    // the garden's grow racks (C9, 0.38.6, for the systems engineer): kind 'growlight', the north four racks and the south two
    { id: '3-growlight-1', kind: 'growlight', at: [5, 0], room: 'G', face: 's', panel: [5, 1], look: { lamp: [-.4, 1.55, .17], drip: [-.4, .4, .2], light: [-.4, 2.05, .17] } },
    { id: '3-growlight-2', kind: 'growlight', at: [8, 21], room: 'G', face: 'n', panel: [8, 20], look: { lamp: [.4, 1.55, .18], drip: [.4, .4, .21], light: [.4, 2.05, .18] } },
  ],
  places: [
    { id: '3-bench-1', type: 'bench', at: [22, 14], xy: [22.7, 14.15], walk: [22, 13], face: 'w', pose: 'sit', room: '+' },
    { id: '3-bench-2', type: 'bench', at: [22, 14], xy: [22.7, 14.85], walk: [21, 14], face: 'w', pose: 'sit', room: '+' },
    { id: '3-bench-3', type: 'bench', at: [17, 7], xy: [17.3, 7.85], walk: [17, 8], face: 'e', pose: 'sit', room: '+' },
    { id: '3-bench-4', type: 'bench', at: [17, 7], xy: [17.3, 7.15], walk: [17, 6], face: 'e', pose: 'sit', room: '+' },
    { id: '3-bench-5', type: 'bench', at: [28, 10], xy: [28.95, 10.48], walk: [28, 9], face: 'n', pose: 'sit', room: '=' },
    { id: '3-bench-6', type: 'bench', at: [30, 10], xy: [30.05, 10.48], walk: [30, 9], face: 'n', pose: 'sit', room: '=' },
    { id: '3-bench-7', type: 'bench', at: [28, 11], xy: [28.95, 11.52], walk: [28, 12], face: 's', pose: 'sit', room: '=' },
    { id: '3-bench-8', type: 'bench', at: [30, 11], xy: [30.05, 11.52], walk: [30, 12], face: 's', pose: 'sit', room: '=' },
    { id: '3-bench-9', type: 'bench', at: [34, 10], xy: [34.95, 10.48], walk: [34, 9], face: 'n', pose: 'sit', room: '=' },
    { id: '3-bench-10', type: 'bench', at: [36, 10], xy: [36.05, 10.48], walk: [36, 9], face: 'n', pose: 'sit', room: '=' },
    { id: '3-bench-11', type: 'bench', at: [34, 11], xy: [34.95, 11.52], walk: [34, 12], face: 's', pose: 'sit', room: '=' },
    { id: '3-bench-12', type: 'bench', at: [36, 11], xy: [36.05, 11.52], walk: [36, 12], face: 's', pose: 'sit', room: '=' },
    { id: '3-bench-13', type: 'bench', at: [14, 9], xy: [14.25, 9.32], walk: [14, 10], face: 's', pose: 'sit', room: '=' },
    { id: '3-bench-14', type: 'bench', at: [14, 9], xy: [14.95, 9.32], walk: [15, 9], face: 's', pose: 'sit', room: '=' },
    { id: '3-bench-15', type: 'bench', at: [14, 12], xy: [14.95, 12.68], walk: [15, 12], face: 'n', pose: 'sit', room: '=' },
    { id: '3-bench-16', type: 'bench', at: [14, 12], xy: [14.25, 12.68], walk: [14, 11], face: 'n', pose: 'sit', room: '=' },
    { id: '3-mess-1', type: 'mess-seat', at: [24, 0], xy: [24.25, 0.38], walk: [23, 1], face: 's', pose: 'sit', window: true, room: 'M' },
    { id: '3-mess-2', type: 'mess-seat', at: [24, 1], xy: [24.25, 1.62], walk: [23, 1], face: 'n', pose: 'sit', room: 'M' },
    { id: '3-mess-3', type: 'mess-seat', at: [25, 0], xy: [25.15, 0.38], walk: [23, 1], face: 's', pose: 'sit', window: true, room: 'M' },
    { id: '3-mess-4', type: 'mess-seat', at: [25, 1], xy: [25.15, 1.62], walk: [25, 2], face: 'n', pose: 'sit', room: 'M' },
    { id: '3-mess-5', type: 'mess-seat', at: [26, 0], xy: [26.05, 0.38], walk: [27, 0], face: 's', pose: 'sit', window: true, room: 'M' },
    { id: '3-mess-6', type: 'mess-seat', at: [26, 1], xy: [26.05, 1.62], walk: [26, 2], face: 'n', pose: 'sit', room: 'M' },
    { id: '3-mess-7', type: 'mess-seat', at: [26, 0], xy: [26.95, 0.38], walk: [27, 0], face: 's', pose: 'sit', window: true, room: 'M' },
    { id: '3-mess-8', type: 'mess-seat', at: [26, 1], xy: [26.95, 1.62], walk: [27, 1], face: 'n', pose: 'sit', room: 'M' },
    { id: '3-mess-9', type: 'mess-seat', at: [29, 0], xy: [29.05, 0.38], walk: [28, 0], face: 's', pose: 'sit', window: true, room: 'M' },
    { id: '3-mess-10', type: 'mess-seat', at: [29, 1], xy: [29.05, 1.62], walk: [28, 1], face: 'n', pose: 'sit', room: 'M' },
    { id: '3-mess-11', type: 'mess-seat', at: [29, 0], xy: [29.95, 0.38], walk: [28, 0], face: 's', pose: 'sit', window: true, room: 'M' },
    { id: '3-mess-12', type: 'mess-seat', at: [29, 1], xy: [29.95, 1.62], walk: [29, 2], face: 'n', pose: 'sit', room: 'M' },
    { id: '3-mess-13', type: 'mess-seat', at: [30, 0], xy: [30.85, 0.38], walk: [32, 0], face: 's', pose: 'sit', window: true, room: 'M' },
    { id: '3-mess-14', type: 'mess-seat', at: [30, 1], xy: [30.85, 1.62], walk: [30, 2], face: 'n', pose: 'sit', room: 'M' },
    { id: '3-mess-15', type: 'mess-seat', at: [31, 0], xy: [31.75, 0.38], walk: [32, 0], face: 's', pose: 'sit', window: true, room: 'M' },
    { id: '3-mess-16', type: 'mess-seat', at: [31, 1], xy: [31.75, 1.62], walk: [32, 1], face: 'n', pose: 'sit', room: 'M' },
    { id: '3-mess-17', type: 'mess-seat', at: [24, 3], xy: [24.25, 3.38], walk: [23, 3], face: 's', pose: 'sit', room: 'M' },
    { id: '3-mess-18', type: 'mess-seat', at: [24, 4], xy: [24.25, 4.62], walk: [23, 4], face: 'n', pose: 'sit', room: 'M' },
    { id: '3-mess-19', type: 'mess-seat', at: [25, 3], xy: [25.15, 3.38], walk: [25, 2], face: 's', pose: 'sit', room: 'M' },
    { id: '3-mess-20', type: 'mess-seat', at: [25, 4], xy: [25.15, 4.62], walk: [25, 5], face: 'n', pose: 'sit', room: 'M' },
    { id: '3-mess-21', type: 'mess-seat', at: [26, 3], xy: [26.05, 3.38], walk: [26, 2], face: 's', pose: 'sit', room: 'M' },
    { id: '3-mess-22', type: 'mess-seat', at: [26, 4], xy: [26.05, 4.62], walk: [26, 5], face: 'n', pose: 'sit', room: 'M' },
    { id: '3-mess-23', type: 'mess-seat', at: [26, 3], xy: [26.95, 3.38], walk: [27, 3], face: 's', pose: 'sit', room: 'M' },
    { id: '3-mess-24', type: 'mess-seat', at: [26, 4], xy: [26.95, 4.62], walk: [27, 4], face: 'n', pose: 'sit', room: 'M' },
    { id: '3-mess-25', type: 'mess-seat', at: [29, 3], xy: [29.05, 3.38], walk: [28, 3], face: 's', pose: 'sit', room: 'M' },
    { id: '3-mess-26', type: 'mess-seat', at: [29, 4], xy: [29.05, 4.62], walk: [28, 4], face: 'n', pose: 'sit', room: 'M' },
    { id: '3-mess-27', type: 'mess-seat', at: [29, 3], xy: [29.95, 3.38], walk: [29, 2], face: 's', pose: 'sit', room: 'M' },
    { id: '3-mess-28', type: 'mess-seat', at: [29, 4], xy: [29.95, 4.62], walk: [29, 5], face: 'n', pose: 'sit', room: 'M' },
    { id: '3-mess-29', type: 'mess-seat', at: [30, 3], xy: [30.85, 3.38], walk: [30, 2], face: 's', pose: 'sit', room: 'M' },
    { id: '3-mess-30', type: 'mess-seat', at: [30, 4], xy: [30.85, 4.62], walk: [30, 5], face: 'n', pose: 'sit', room: 'M' },
    { id: '3-mess-31', type: 'mess-seat', at: [31, 3], xy: [31.75, 3.38], walk: [32, 3], face: 's', pose: 'sit', room: 'M' },
    { id: '3-mess-32', type: 'mess-seat', at: [31, 4], xy: [31.75, 4.62], walk: [32, 4], face: 'n', pose: 'sit', room: 'M' },
    { id: '3-mess-33', type: 'mess-seat', at: [25, 7], xy: [25.57, 7.47], walk: [26, 7], face: -135, pose: 'sit', room: 'M' },
    { id: '3-mess-34', type: 'mess-seat', at: [25, 6], xy: [25.57, 6.33], walk: [25, 5], face: -45, pose: 'sit', room: 'M' },
    { id: '3-mess-35', type: 'mess-seat', at: [24, 6], xy: [24.43, 6.33], walk: [24, 5], face: 45, pose: 'sit', room: 'M' },
    { id: '3-mess-36', type: 'mess-seat', at: [24, 7], xy: [24.43, 7.47], walk: [23, 7], face: 135, pose: 'sit', room: 'M' },
    { id: '3-mess-37', type: 'mess-seat', at: [28, 7], xy: [28.91, 7.27], walk: [29, 7], face: -118, pose: 'sit', room: 'M' },
    { id: '3-mess-38', type: 'mess-seat', at: [28, 6], xy: [28.57, 6.19], walk: [28, 5], face: -28, pose: 'sit', room: 'M' },
    { id: '3-mess-39', type: 'mess-seat', at: [27, 6], xy: [27.49, 6.53], walk: [27, 6], face: 62, pose: 'sit', room: 'M' },
    { id: '3-mess-40', type: 'mess-seat', at: [27, 7], xy: [27.83, 7.61], walk: [27, 7], face: 152, pose: 'sit', room: 'M' },
    { id: '3-mess-41', type: 'mess-seat', at: [32, 7], xy: [32.19, 7.05], walk: [32, 7], face: -101, pose: 'sit', room: 'M' },
    { id: '3-mess-42', type: 'mess-seat', at: [31, 6], xy: [31.55, 6.11], walk: [31, 5], face: -11, pose: 'sit', room: 'M' },
    { id: '3-mess-43', type: 'mess-seat', at: [30, 6], xy: [30.61, 6.75], walk: [30, 6], face: 79, pose: 'sit', room: 'M' },
    { id: '3-mess-44', type: 'mess-seat', at: [31, 7], xy: [31.25, 7.69], walk: [30, 7], face: 169, pose: 'sit', room: 'M' },
    { id: '3-grab-1', type: 'grab-shelf', at: [33, 7], xy: [33.85, 7.5], walk: [33, 7], face: 'e', pose: 'stand', room: 'M' },
    { id: '3-galley-1', type: 'work:galley', at: [39, 3], xy: [39.79, 3.6], walk: [39, 3], face: 'e', pose: 'work', anim: 'cook', room: 'K' },
    { id: '3-galley-2', type: 'work:galley', at: [39, 4], xy: [39.79, 4.5], walk: [39, 4], face: 'e', pose: 'work', anim: 'cook', room: 'K' },
    { id: '3-galley-3', type: 'work:galley', at: [39, 5], xy: [39.79, 5.4], walk: [39, 5], face: 'e', pose: 'work', anim: 'cook', room: 'K' },
    { id: '3-galley-4', type: 'work:galley', at: [38, 4], xy: [38, 4.25], walk: [38, 4], face: 'n', pose: 'work', anim: 'cook', room: 'K' },
    { id: '3-galley-5', type: 'work:galley', at: [37, 5], xy: [37.5, 5.2], walk: [37, 4], face: 's', pose: 'work', anim: 'cook', room: 'K' },
    { id: '3-galley-6', type: 'work:galley', at: [38, 6], xy: [38.5, 6.8], walk: [38, 7], face: 'n', pose: 'work', anim: 'cook', room: 'K' },
    { id: '3-galley-7', type: 'work:galley', at: [39, 8], xy: [39.75, 8], walk: [39, 8], face: 'e', pose: 'work', anim: 'wash', room: 'K' },
    { id: '3-galley-8', type: 'work:galley', at: [35, 3], xy: [35.5, 3.5], walk: [35, 3], face: 's', pose: 'sit', anim: 'read', room: 'K' },
    { id: '3-lounge-1', type: 'lounge-seat', at: [42, 2], xy: [42.07, 2.67], walk: [42, 2], face: -20, pose: 'sit', anim: 'drink', y: .8, room: 'L' },
    { id: '3-lounge-2', type: 'lounge-seat', at: [43, 3], xy: [43.01, 3.21], walk: [43, 3], face: -40, pose: 'sit', anim: 'drink', y: .8, room: 'L' },
    { id: '3-lounge-3', type: 'lounge-seat', at: [43, 4], xy: [43.7, 4.04], walk: [43, 3], face: -60, pose: 'sit', anim: 'drink', y: .8, room: 'L' },
    { id: '3-lounge-4', type: 'lounge-seat', at: [44, 5], xy: [44.07, 5.06], walk: [44, 5], face: -80, pose: 'sit', anim: 'drink', y: .8, room: 'L' },
    { id: '3-lounge-5', type: 'lounge-seat', at: [44, 6], xy: [44.07, 6.14], walk: [44, 6], face: -100, pose: 'sit', anim: 'drink', y: .8, room: 'L' },
    { id: '3-lounge-6', type: 'lounge-seat', at: [43, 7], xy: [43.7, 7.16], walk: [44, 7], face: -120, pose: 'sit', anim: 'drink', y: .8, room: 'L' },
    { id: '3-lounge-7', type: 'lounge-seat', at: [43, 7], xy: [43.01, 7.99], walk: [43, 8], face: -140, pose: 'sit', anim: 'drink', y: .8, room: 'L' },
    { id: '3-lounge-8', type: 'lounge-seat', at: [42, 8], xy: [42.07, 8.53], walk: [42, 8], face: -160, pose: 'sit', anim: 'drink', y: .8, room: 'L' },
    { id: '3-lounge-9', type: 'lounge-seat', at: [46, 3], xy: [46.11, 3.35], walk: [46, 3], face: -145, pose: 'sit', anim: 'drink', y: .79, room: 'L' },
    { id: '3-lounge-10', type: 'lounge-seat', at: [45, 2], xy: [45.56, 2.41], walk: [46, 2], face: 26, pose: 'sit', anim: 'drink', window: true, y: .79, room: 'L' },
    { id: '3-lounge-11', type: 'lounge-seat', at: [45, 1], xy: [45.24, 1.99], walk: [44, 2], face: -99, pose: 'sit', anim: 'drink', window: true, y: .79, room: 'L' },
    { id: '3-lounge-12', type: 'lounge-seat', at: [44, 1], xy: [44.18, 1.73], walk: [43, 1], face: 72, pose: 'sit', anim: 'drink', window: true, y: .79, room: 'L' },
    { id: '3-lounge-13', type: 'lounge-seat', at: [41, 15], xy: [41.57, 15.3], walk: [41, 13], face: 'n', pose: 'sit', anim: 'talk', y: .54, room: 'L' },
    { id: '3-lounge-14', type: 'lounge-seat', at: [42, 15], xy: [42.23, 15.3], walk: [43, 15], face: 'n', pose: 'sit', anim: 'talk', y: .54, room: 'L' },
    { id: '3-lounge-15', type: 'lounge-seat', at: [41, 13], xy: [41.57, 13.9], walk: [41, 13], face: 's', pose: 'sit', anim: 'talk', y: .54, room: 'L' },
    { id: '3-lounge-16', type: 'lounge-seat', at: [42, 13], xy: [42.23, 13.9], walk: [42, 13], face: 's', pose: 'sit', anim: 'talk', y: .54, room: 'L' },
    { id: '3-lounge-17', type: 'lounge-seat', at: [41, 17], xy: [41.57, 17.3], walk: [43, 17], face: 'n', pose: 'sit', anim: 'talk', y: .54, room: 'L' },
    { id: '3-lounge-18', type: 'lounge-seat', at: [42, 17], xy: [42.23, 17.3], walk: [43, 17], face: 'n', pose: 'sit', anim: 'talk', y: .54, room: 'L' },
    { id: '3-lounge-19', type: 'lounge-seat', at: [41, 15], xy: [41.57, 15.9], walk: [43, 15], face: 's', pose: 'sit', anim: 'talk', y: .54, room: 'L' },
    { id: '3-lounge-20', type: 'lounge-seat', at: [42, 15], xy: [42.23, 15.9], walk: [43, 15], face: 's', pose: 'sit', anim: 'talk', y: .54, room: 'L' },
    { id: '3-lounge-21', type: 'lounge-seat', at: [41, 19], xy: [41.57, 19.3], walk: [41, 20], face: 'n', pose: 'sit', anim: 'talk', y: .54, room: 'L' },
    { id: '3-lounge-22', type: 'lounge-seat', at: [42, 19], xy: [42.23, 19.3], walk: [42, 20], face: 'n', pose: 'sit', anim: 'talk', y: .54, room: 'L' },
    { id: '3-lounge-23', type: 'lounge-seat', at: [41, 17], xy: [41.57, 17.9], walk: [43, 17], face: 's', pose: 'sit', anim: 'talk', y: .54, room: 'L' },
    { id: '3-lounge-24', type: 'lounge-seat', at: [42, 17], xy: [42.23, 17.9], walk: [43, 17], face: 's', pose: 'sit', anim: 'talk', y: .54, room: 'L' },
    { id: '3-lounge-25', type: 'lounge-seat', at: [48, 11], xy: [47.84, 11.8], walk: [48, 11], face: 'e', pose: 'sit', anim: 'talk', room: 'L', cush: 0.44 },
    { id: '3-lounge-26', type: 'lounge-seat', at: [48, 11], xy: [47.84, 11], walk: [48, 11], face: 'e', pose: 'sit', anim: 'talk', room: 'L', cush: 0.44 },
    { id: '3-lounge-27', type: 'lounge-seat', at: [48, 10], xy: [47.84, 10.2], walk: [48, 10], face: 'e', pose: 'sit', anim: 'talk', room: 'L', cush: 0.44 },
    { id: '3-lounge-28', type: 'lounge-seat', at: [49, 9], xy: [49.61, 8.9], walk: [49, 9], face: -8.6, pose: 'sit', anim: 'read', room: 'L', cush: 0.44 },
    { id: '3-lounge-29', type: 'lounge-seat', at: [49, 12], xy: [49.61, 13.1], walk: [49, 12], face: -171.4, pose: 'sit', anim: 'read', room: 'L', cush: 0.44 },
    { id: '3-lounge-30', type: 'lounge-seat', at: [46, 4], xy: [46.77, 4.83], walk: [46, 5], face: 51.6, pose: 'sit', anim: 'read', room: 'L', cush: 0.44 },
    { id: '3-lounge-31', type: 'lounge-seat', at: [48, 6], xy: [48.53, 6.82], walk: [48, 7], face: -128.4, pose: 'sit', anim: 'read', room: 'L', cush: 0.44 },
    { id: '3-lounge-32', type: 'lounge-seat', at: [46, 17], xy: [46.77, 17.17], walk: [46, 16], face: 128.4, pose: 'sit', anim: 'read', room: 'L', cush: 0.44 },
    { id: '3-lounge-33', type: 'lounge-seat', at: [48, 15], xy: [48.53, 15.18], walk: [48, 14], face: -51.6, pose: 'sit', anim: 'read', room: 'L', cush: 0.44 },
    { id: '3-lounge-34', type: 'lounge-seat', at: [50, 8], xy: [50.7, 8.02], walk: [50, 8], face: 'w', pose: 'stand', room: 'L' },
    { id: '3-tend-1', type: 'garden', at: [4, 1], xy: [4.4, 1.13], walk: [4, 1], face: 'n', pose: 'work', anim: 'water', room: 'G' },
    { id: '3-tend-2', type: 'garden', at: [6, 1], xy: [6.4, 1.13], walk: [6, 1], face: 'n', pose: 'work', anim: 'water', room: 'G' },
    { id: '3-tend-3', type: 'garden', at: [8, 1], xy: [8.4, 1.13], walk: [8, 1], face: 'n', pose: 'work', anim: 'water', room: 'G' },
    { id: '3-tend-4', type: 'garden', at: [10, 1], xy: [10.4, 1.13], walk: [10, 1], face: 'n', pose: 'work', anim: 'water', room: 'G' },
    { id: '3-tend-5', type: 'garden', at: [7, 20], xy: [7.4, 20.85], walk: [7, 20], face: 's', pose: 'work', anim: 'water', room: 'G' },
    { id: '3-tend-6', type: 'garden', at: [9, 20], xy: [9.4, 20.85], walk: [9, 20], face: 's', pose: 'work', anim: 'water', room: 'G' },
    { id: '3-tend-7', type: 'garden', at: [5, 3], xy: [5.4, 3.6], walk: [5, 3], face: 'n', pose: 'work', anim: 'water', room: 'G' },
    { id: '3-tend-8', type: 'garden', at: [8, 3], xy: [8, 3.6], walk: [8, 3], face: 'n', pose: 'work', anim: 'water', room: 'G' },
    { id: '3-tend-9', type: 'garden', at: [10, 3], xy: [10.6, 3.6], walk: [10, 3], face: 'n', pose: 'work', anim: 'water', room: 'G' },
    { id: '3-tend-10', type: 'garden', at: [5, 6], xy: [5.4, 6.15], walk: [5, 6], face: 'n', pose: 'work', anim: 'water', room: 'G' },
    { id: '3-tend-11', type: 'garden', at: [8, 6], xy: [8, 6.15], walk: [8, 6], face: 'n', pose: 'work', anim: 'water', room: 'G' },
    { id: '3-tend-12', type: 'garden', at: [10, 6], xy: [10.6, 6.15], walk: [10, 6], face: 'n', pose: 'work', anim: 'water', room: 'G' },
    { id: '3-tend-13', type: 'garden', at: [5, 16], xy: [5.4, 16.25], walk: [5, 16], face: 'n', pose: 'work', anim: 'water', room: 'G' },
    { id: '3-tend-14', type: 'garden', at: [8, 16], xy: [8, 16.25], walk: [8, 16], face: 'n', pose: 'work', anim: 'water', room: 'G' },
    { id: '3-tend-15', type: 'garden', at: [10, 16], xy: [10.6, 16.25], walk: [10, 16], face: 'n', pose: 'work', anim: 'water', room: 'G' },
    { id: '3-tend-16', type: 'garden', at: [8, 19], xy: [8, 19.65], walk: [8, 19], face: 'n', pose: 'work', anim: 'water', room: 'G' },
    { id: '3-tend-17', type: 'garden', at: [10, 19], xy: [10.6, 19.65], walk: [10, 19], face: 'n', pose: 'work', anim: 'water', room: 'G' },
    // gardeners at work (C9, 0.38.6): standing at the racks and beds, watering; free tiles that aren't tend spots
    { id: '3-gardenwork-1', type: 'work:garden', at: [7, 1], xy: [7.1, 1.15], face: 'n', pose: 'stand', anim: 'water', room: 'G' },   // the north racks
    { id: '3-gardenwork-2', type: 'work:garden', at: [9, 1], xy: [9.1, 1.15], face: 'n', pose: 'stand', anim: 'water', room: 'G' },
    { id: '3-gardenwork-3', type: 'work:garden', at: [4, 4], xy: [4.5, 4.4], face: 's', pose: 'stand', anim: 'water', room: 'G' },   // the beds
    { id: '3-gardenwork-4', type: 'work:garden', at: [8, 4], xy: [8, 4.4], face: 's', pose: 'stand', anim: 'water', room: 'G' },
    { id: '3-gardenwork-5', type: 'work:garden', at: [5, 14], xy: [5, 14.4], face: 's', pose: 'stand', anim: 'water', room: 'G' },
    { id: '3-crates-1', type: 'storage', at: [9, 12], face: 'e', pose: 'stand', room: 'G' },   // where garden crates are picked up, by the glass doors
    { id: '3-garden-1', type: 'garden', at: [6, 8], xy: [6.15, 8.45], walk: [5, 8], face: 's', pose: 'sit', room: 'G' },
    { id: '3-garden-2', type: 'garden', at: [6, 8], xy: [6.85, 8.45], walk: [7, 8], face: 's', pose: 'sit', room: 'G' },
    { id: '3-garden-3', type: 'garden', at: [6, 13], xy: [6.85, 13.55], walk: [7, 13], face: 'n', pose: 'sit', room: 'G' },
    { id: '3-garden-4', type: 'garden', at: [6, 13], xy: [6.15, 13.55], walk: [5, 13], face: 'n', pose: 'sit', room: 'G' },
    { id: '3-garden-5', type: 'garden', at: [3, 11], xy: [3.7, 11.35], walk: [4, 11], face: 'e', pose: 'sit', room: 'G' },
    { id: '3-garden-6', type: 'garden', at: [3, 10], xy: [3.7, 10.65], walk: [4, 10], face: 'e', pose: 'sit', room: 'G' },
    { id: '3-visit-1', type: 'bench', at: [14, 2], xy: [14.5, 2.5], walk: [14, 2], face: 's', pose: 'sit', room: 'I' },
    { id: '3-visit-2', type: 'bench', at: [18, 2], xy: [18.5, 2.5], walk: [18, 2], face: 's', pose: 'sit', room: 'I' },
    { id: '3-infirmary-1', type: 'work:infirmary', at: [22, 3], xy: [22.55, 3.8], walk: [22, 3], face: 'e', pose: 'sit', room: 'I' },
    { id: '3-infirmary-2', type: 'work:infirmary', at: [21, 0], xy: [21.98, 0.9], walk: [21, 0], face: 'e', pose: 'work', room: 'I' },
    { id: '3-infirmary-3', type: 'work:infirmary', at: [13, 7], xy: [13.05, 7.45], walk: [13, 7], face: 's', pose: 'work', room: 'X' },
    { id: '3-infirmary-4', type: 'work:infirmary', at: [16, 7], xy: [16.3, 7.15], walk: [16, 7], face: 'n', pose: 'sit', room: 'X' },
    { id: '3-infirmary-5', type: 'work:infirmary', at: [16, 2], xy: [16.5, 2.4], walk: [16, 2], face: 'n', pose: 'stand', room: 'I' },   // ward round, between the middle beds
    { id: '3-infirmary-6', type: 'work:infirmary', at: [13, 4], xy: [13.05, 4.4], walk: [13, 4], face: 'w', pose: 'work', room: 'I' },   // the supplies shelf
    // patients (C9, 0.38.4): the four ward beds, for anyone the sim sends to the infirmary (storm survivors, the sick). Type
    // 'patient-bed', so nobody sleeps here at night and no plan uses them day to day; you get in from the south
    { id: '3-ward-1', type: 'patient-bed', at: [13, 1], xy: [13.5, 1.12], walk: [13, 2], face: 's', pose: 'lie', y: .69, room: 'I' },
    { id: '3-ward-2', type: 'patient-bed', at: [15, 1], xy: [15.5, 1.12], walk: [15, 2], face: 's', pose: 'lie', y: .69, room: 'I' },
    { id: '3-ward-3', type: 'patient-bed', at: [17, 1], xy: [17.5, 1.12], walk: [17, 2], face: 's', pose: 'lie', y: .69, room: 'I' },
    { id: '3-ward-4', type: 'patient-bed', at: [19, 1], xy: [19.5, 1.12], walk: [19, 2], face: 's', pose: 'lie', y: .69, room: 'I' },
    { id: '3-toilet-1', type: 'toilet', at: [22, 21], xy: [22.18, 21.5], walk: [22, 20], face: 'n', pose: 'sit', y: .4, room: 'w' },
    { id: '3-toilet-2', type: 'toilet', at: [20, 21], xy: [20.73, 21.5], walk: [20, 20], face: 'n', pose: 'sit', y: .4, room: 'w' },
    { id: '3-toilet-3', type: 'toilet', at: [19, 21], xy: [19.27, 21.5], walk: [19, 20], face: 'n', pose: 'sit', y: .4, room: 'w' },
    { id: '3-toilet-4', type: 'toilet', at: [17, 21], xy: [17.83, 21.5], walk: [17, 20], face: 'n', pose: 'sit', y: .4, room: 'w' },
    { id: '3-basin-1', type: 'basin', at: [21, 16], xy: [21.93, 16.7], walk: [21, 16], face: 'e', pose: 'stand', room: 'w' },
    { id: '3-basin-2', type: 'basin', at: [21, 17], xy: [21.93, 17.7], walk: [21, 17], face: 'e', pose: 'stand', room: 'w' },
    { id: '3-gym-1', type: 'gym', at: [24, 20], xy: [24.5, 20.5], walk: [24, 19], face: 's', pose: 'stand', anim: 'run', y: 0.16, room: 'F' },
    { id: '3-gym-2', type: 'gym', at: [25, 20], xy: [25.85, 20.5], walk: [25, 19], face: 's', pose: 'stand', anim: 'run', y: 0.16, room: 'F' },   // 0.38.28: moved west for a fourth treadmill
    { id: '3-gym-3', type: 'gym', at: [28, 20], xy: [28.5, 20.5], walk: [28, 19], face: 's', pose: 'stand', anim: 'run', y: 0.16, room: 'F' },
    { id: '3-gym-4', type: 'gym', at: [30, 20], xy: [30.6, 20.2], walk: [31, 20], face: 's', pose: 'sit', anim: 'row', y: .43, room: 'F', cush: 0.34 },
    { id: '3-gym-5', type: 'gym', at: [30, 15], xy: [30.92, 15.6], walk: [30, 15], face: 'e', pose: 'stand', room: 'F' },
    { id: '3-gym-6', type: 'gym', at: [29, 16], xy: [29.4, 16], walk: [28, 15], face: 'e', pose: 'lie', anim: 'bench', room: 'F' },   // 0.47.5: the bench press
    { id: '3-gym-7', type: 'gym', at: [23, 15], xy: [23.85, 15.6], walk: [23, 15], face: 's', pose: 'lie', room: 'F', y: .035 },   // 0.27.39: on the floor mat (top .015; the back sits within about 2 cm, by build), not the default bed height (the user: "they hover")
    { id: '3-gym-8', type: 'gym', at: [24, 15], xy: [24.6, 15.6], walk: [24, 15], face: 's', pose: 'lie', room: 'F', y: .035 },
    { id: '3-gym-9', type: 'gym', at: [25, 15], xy: [25.35, 15.6], walk: [25, 15], face: 's', pose: 'lie', room: 'F', y: .035 },
    { id: '3-shop-1', type: 'shop', at: [32, 16], xy: [32.96, 16], walk: [33, 15], face: 'w', pose: 'stand', anim: 'browse', room: 'S' },
    { id: '3-shop-2', type: 'shop', at: [32, 17], xy: [32.96, 17.4], walk: [33, 17], face: 'w', pose: 'stand', anim: 'browse', room: 'S' },
    { id: '3-shop-3', type: 'shop', at: [32, 18], xy: [32.96, 18.8], walk: [33, 18], face: 'w', pose: 'stand', anim: 'browse', room: 'S' },
    { id: '3-shop-4', type: 'shop', at: [35, 17], xy: [35.04, 17.4], walk: [34, 17], face: 'e', pose: 'stand', anim: 'browse', room: 'S' },
    { id: '3-shop-5', type: 'shop', at: [35, 18], xy: [35.04, 18.8], walk: [34, 18], face: 'e', pose: 'stand', anim: 'browse', room: 'S' },
    { id: '3-store-1', type: 'work:store', at: [35, 14], xy: [35.55, 14.85], walk: [35, 14], face: 'w', pose: 'stand', room: 'S' },   // behind the till
    { id: '3-shop-6', type: 'shop', at: [34, 20], xy: [34, 20.85], walk: [34, 20], face: 's', pose: 'stand', anim: 'browse', room: 'S' },
    { id: '3-shop-7', type: 'shop', at: [34, 14], xy: [34.15, 14.85], walk: [34, 14], face: 'e', pose: 'stand', anim: 'pay', room: 'S' },   // paying at the till (A5b)
    { id: '3-shop-8', type: 'shop', at: [32, 14], xy: [32.4, 14.25], walk: [32, 14], face: 'n', pose: 'stand', anim: 'browse', room: 'S' },   // taking a basket by the door
    { id: '3-gym-10', type: 'gym', at: [31, 14], xy: [31.5, 14.05], walk: [31, 14], face: 'n', pose: 'stand', anim: 'drink', room: 'F' },   // the water dispenser
    // Pillar 3 (C9, 0.38.2): the rowing pair, the punch bag and the extra mat. 'punch' and 'stretch' are the performance engineer's standing poses (8b, 0.27.15; plain stand until merged)
    { id: '3-gym-11', type: 'gym', at: [24, 17], xy: [24, 17.4], walk: [25, 17], face: 's', pose: 'sit', anim: 'row', y: .43, room: 'F', cush: 0.34 },
    { id: '3-gym-12', type: 'gym', at: [24, 17], xy: [24.8, 17.4], walk: [25, 17], face: 's', pose: 'sit', anim: 'row', y: .43, room: 'F', cush: 0.34 },
    { id: '3-gym-13', type: 'gym', at: [29, 17], xy: [29.8, 17.5], face: 'e', pose: 'stand', anim: 'punch', room: 'F' },
    { id: '3-gym-14', type: 'gym', at: [27, 17], xy: [27.9, 17.15], face: 's', pose: 'stand', anim: 'stretch', room: 'F' },   // at the mat's head, 1.3 m of mat in front
    // 0.38.28 (0.60.7): the fourth treadmill, and two exercise bikes facing the promenade windows (on the saddle, facing the bars)
    { id: '3-gym-15', type: 'gym', at: [27, 20], xy: [27.2, 20.5], walk: [27, 19], face: 's', pose: 'stand', anim: 'run', y: 0.16, room: 'F' },
    { id: '3-gym-16', type: 'gym', at: [28, 14], xy: [28.5, 14.2], walk: [28, 15], face: 'n', pose: 'sit', anim: 'cycle', y: .62, room: 'F' },
    { id: '3-gym-17', type: 'gym', at: [29, 14], xy: [29.5, 14.2], walk: [30, 14], face: 'n', pose: 'sit', anim: 'cycle', y: .62, room: 'F' },
    // the machines' panels: where a Works tech stands to service each one (A5b)
    { id: '3-oven-1-panel', type: 'work:works', at: [37, 4], xy: [37.5, 4.3], walk: [37, 4], face: 'n', pose: 'work', machine: '3-oven-1', room: 'K' },
    { id: '3-oven-2-panel', type: 'work:works', at: [38, 4], xy: [38.5, 4.3], walk: [38, 4], face: 'n', pose: 'work', machine: '3-oven-2', room: 'K' },
    { id: '3-range-1-panel', type: 'work:works', at: [39, 4], xy: [39.7, 4.5], walk: [39, 4], face: 'e', pose: 'work', machine: '3-range-1', room: 'K' },
    { id: '3-galleyplant-1-panel', type: 'work:works', at: [39, 1], xy: [39.5, 1.3], walk: [39, 1], face: 'n', pose: 'work', machine: '3-galleyplant-1', room: 'g' },
    { id: '3-chiller-1-panel', type: 'work:works', at: [39, 2], xy: [39.7, 2.5], walk: [39, 2], face: 'e', pose: 'work', machine: '3-chiller-1', room: 'g' },
    { id: '3-recycler-1-panel', type: 'work:works', at: [14, 16], xy: [14.3, 16.5], walk: [14, 16], face: 'w', pose: 'work', machine: '3-recycler-1', room: 'R' },
    { id: '3-filter-1-panel', type: 'work:works', at: [13, 19], xy: [13.3, 19.5], walk: [13, 19], face: 'w', pose: 'work', machine: '3-filter-1', room: 'R' },
    { id: '3-pump-1-panel', type: 'work:works', at: [15, 17], xy: [15.7, 17.5], walk: [15, 17], face: 'e', pose: 'work', machine: '3-pump-1', room: 'R' },
    { id: '3-uv-1-panel', type: 'work:works', at: [14, 13], xy: [14.5, 13.3], walk: [14, 13], face: 'n', pose: 'work', machine: '3-uv-1', room: 'R' },
    { id: '3-lights-1-panel', type: 'work:works', at: [16, 15], xy: [16.7, 15.5], walk: [16, 15], face: 'e', pose: 'work', machine: '3-lights-1', room: 'R' },
    { id: '3-nutrient-1-panel', type: 'work:works', at: [4, 18], xy: [4.7, 18.5], walk: [4, 18], face: 'e', pose: 'work', machine: '3-nutrient-1', room: 'i' },
    { id: '3-irrigation-1-panel', type: 'work:works', at: [4, 20], xy: [4.7, 20.5], walk: [4, 20], face: 'e', pose: 'work', machine: '3-irrigation-1', room: 'i' },
    { id: '3-growlight-1-panel', type: 'work:works', at: [5, 1], xy: [5.4, 1.15], walk: [5, 1], face: 'n', pose: 'work', machine: '3-growlight-1', room: 'G' },
    { id: '3-growlight-2-panel', type: 'work:works', at: [8, 20], xy: [8.4, 20.8], walk: [8, 20], face: 's', pose: 'work', machine: '3-growlight-2', room: 'G' },
    { id: '3-callhome-1', type: 'callhome', at: [36, 21], xy: [36.62, 21.15], walk: [36, 20], face: 's', pose: 'sit', anim: 'call', y: .53, room: 'B' },
    { id: '3-callhome-2', type: 'callhome', at: [37, 21], xy: [37.84, 21.15], walk: [37, 20], face: 's', pose: 'sit', anim: 'call', y: .53, room: 'B' },
    { id: '3-callhome-3', type: 'callhome', at: [39, 21], xy: [39.06, 21.15], walk: [39, 20], face: 's', pose: 'sit', anim: 'call', y: .53, room: 'B' },
    { id: '3-callhome-4', type: 'callhome', at: [40, 21], xy: [40.28, 21.15], walk: [40, 20], face: 's', pose: 'sit', anim: 'call', y: .53, room: 'B' },
    { id: '3-bench-17', type: 'bench', at: [38, 16], xy: [38, 15.89], walk: [37, 17], face: 's', pose: 'sit', room: 'B', cush: 0.44 },
    { id: '3-bench-18', type: 'bench', at: [39, 16], xy: [39, 15.89], walk: [38, 17], face: 's', pose: 'sit', room: 'B', cush: 0.44 },
    { id: '3-lift-1', type: 'lift-wait', at: [17, 9], xy: [17.5, 9.5], walk: [17, 9], face: 'e', pose: 'stand', room: '+' },
    { id: '3-lift-2', type: 'lift-wait', at: [17, 10], xy: [17.5, 10.5], walk: [17, 10], face: 'e', pose: 'stand', room: '+' },
    { id: '3-lift-3', type: 'lift-wait', at: [17, 11], xy: [17.5, 11.5], walk: [17, 11], face: 'e', pose: 'stand', room: '+' },
    { id: '3-lift-4', type: 'lift-wait', at: [22, 9], xy: [22.5, 9.5], walk: [22, 9], face: 'w', pose: 'stand', room: '+' },
    { id: '3-lift-5', type: 'lift-wait', at: [22, 10], xy: [22.5, 10.5], walk: [22, 10], face: 'w', pose: 'stand', room: '+' },
    { id: '3-lift-6', type: 'lift-wait', at: [22, 11], xy: [22.5, 11.5], walk: [22, 11], face: 'w', pose: 'stand', room: '+' },
    { id: '3-queue-1', type: 'servery-queue', at: [33, 3], xy: [33.55, 3.5], walk: [33, 3], face: 'e', pose: 'stand', room: 'M' },
    { id: '3-queue-2', type: 'servery-queue', at: [33, 4], xy: [33.55, 4.5], walk: [33, 4], face: 'e', pose: 'stand', room: 'M' },
    { id: '3-queue-3', type: 'servery-queue', at: [33, 5], xy: [33.55, 5.5], walk: [33, 5], face: 'e', pose: 'stand', room: 'M' },
    { id: '3-queue-4', type: 'servery-queue', at: [33, 6], xy: [33.55, 6.5], walk: [33, 6], face: 'e', pose: 'stand', room: 'M' },
    { id: '3-galley-pass', type: 'work:galley', at: [35, 5], xy: [35.5, 5.5], walk: [35, 5], face: 'w', pose: 'work', room: 'K' },
    { id: '3-cold-1', type: 'storage', anim: 'browse', at: [36, 1], face: 'n', pose: 'stand', room: 'C' },   // unloading a cart onto the cold shelves (B3)
    { id: '3-cold-2', type: 'storage', anim: 'browse', at: [37, 1], face: 'n', pose: 'stand', room: 'C' },
  ],
  dress(d) {
    for (const [key, tw, text] of d.plates) placeOnEdge('plate', key, tw, { text });
    for (const [key, tw] of [['v,19,12', 'w'], ['v,21,12', 'e']]) placeOnEdge('liftPanel', key, tw);
    placeOnEdge('deckDirectory', 'h,20,9', 'n', { it: IT('Deck directory', 'Seven decks, top to bottom. Bridge, Command & Science, Commons, Quarters, the Recreation Deck (R), Operations, Engineering. You are here: Commons.') });
    placeOnEdge('notices', 'h,22,16', 'n', { it: IT('Notice board', 'The week\'s menu, a sign-up sheet for the gym rota, and a card that says CALL YOUR MOTHER in three different hands.') });
    // the ladder, behind glass below the car
    NO_FADE.add('Z');
    place('Z', 'spineLadder', 1, .5, 'n', { it: SPINE_IT.ladder });
    // the plaza: somewhere to wait, and plants at the corners
    place('+', 'bench', 5.7, 8.5, 'e', { snug: true, it: IT('Bench', 'Where people wait for whoever is always last to breakfast.') });
    place('+', 'bench', .3, 1.5, 'w', { snug: true, it: IT('Bench', 'Facing the infirmary doors, which makes it the worried-friend bench.') });
    for (const [x, z, band] of [[.45, 9.55, '#5fd6c6'], [5.55, .45, '#d9a441'], [5.55, 9.55, '#c45a3f']]) place('+', 'plant', x, z, 'n', { band, big: true });
    // the promenade: big plants by the garden doors and the lounge doors
    for (const [x, z] of [[.45, .45], [.45, 3.55], [28.55, .45], [28.55, 3.55]]) place('=', 'plant', x, z, 'n', { big: true, band: '#5fd6c6' });
    // planter islands down the middle (rows 10-11, three columns each), between the doorways, so every door keeps a straight way across;
    // the route kiosk where the promenade leaves the plaza; benches either side of the garden doors
    place('=', 'planterIsland', 17.5, 2, 'n', { snug: true, fadeGroup: '=:a', fruit: true, flowers: 2, it: IT('Lemon tree', 'A little lemon tree in a planter, with a bench on each side. The gardeners water it from a can, because it is not technically the garden.') });
    place('=', 'planterIsland', 23.5, 2, 'n', { snug: true, fadeGroup: '=:b', it: IT('Planter', 'Marigolds this month, after a vote at the mess hall. The losing side wanted cacti, and has not let it go.') });
    place('=', 'routeKiosk', 12.5, 2, 'w', { block: [[12, 1], [12, 2]], it: IT('Route map', 'The Wren\'s tour, drawn as a dotted line across the frontier. Three survey stops done, four to go. The little ship on the map is smudged where people keep touching it.') });
    place('=', 'bench', 2.6, .32, 'n', { snug: true, it: IT('Bench', 'By the garden doors. It smells of tomatoes and wet soil here, which some people like a lot.') });
    place('=', 'bench', 2.6, 3.68, 's', { snug: true });
    for (const [x, z, band] of [[1.3, .4, '#d9a441'], [3.9, .4, '#c45a3f'], [1.3, 3.6, '#c45a3f'], [3.9, 3.6, '#d9a441']]) place('=', 'plant', x, z, 'n', { band });

    // ---- mess hall: four long tables of eight under the port windows, three round tables of four by the promenade.
    // The line runs down the galley wall: trays, the servery, grab-and-go. Drinks at the far end. 44 seats.
    const MT = [['Long table', 'Seats eight. The engineers take this one every morning and argue about pumps.'],
      ['Long table', 'Scratched initials on the bench: R + P, inside a lopsided heart. Nobody admits to it.'],
      ['Long table', 'The table nearest the servery. Always the first full and the last empty.'],
      ['Long table', 'Officers tend to sit here. Not a rule, just a habit nobody breaks.']];
    [[2.6, 1.0], [7.4, 1.0], [2.6, 4.0], [7.4, 4.0]].forEach(([x, z], k) => place('M', 'longTable', x, z, 'n', { it: IT(...MT[k]) }));
    [[2.0, 6.9], [5.2, 6.9], [8.4, 6.9]].forEach(([x, z], k) => place('M', 'roundTable', x, z, 'n', { turn: k * .3, it: k === 1 ? IT('Round table', 'Four chairs, two orange and two teal. Good for quiet talks and for spreading out a card game.') : undefined }));
    place('M', 'drinksStation', 11.6, 1.0, 'e', { it: IT('Drinks station', 'Three juices, a tea urn that is never allowed to run dry, and a stack of mugs. Someone has labelled the orange one "probably orange".') });
    // 0.38.25 (the user's): no tray return; diners leave their trays on the table and the galley crew clear them (kit trayReturn kept, unused)
    place('M', 'trayStack', 11.65, 3.5, 'e', { it: IT('Trays and cutlery', 'The start of the line. Take a tray, take a fork, keep moving.') });
    place('M', 'servery', 11.45, 5.5, 'e', { it: IT('Servery', 'The hot line, under heat lamps. Breakfast from 06:00 to 09:00, dinner from 17:00 to 20:30. The galley hands it through the counter behind.') });
    place('M', 'grabShelf', 11.6, 7.5, 'e', { live: true, it: IT('Grab and go', 'Rolls, fruit and juice, chilled, for anyone running late. It empties fast at 07:55.') });
    wallFixed('=', 'valvePanel', 'n', VALVE_PANELS[3].along, { hitW: 1.5, it: { ...IT('Pipe valves', 'Three valves on the Commons\' water line, numbered from upstream. Close the one before a leak.'), valves: 3 } });   // 0.47.0: incidents (m6)
    wallFixed('K', 'alarmPanel', 'w', 4.5, { hitW: .7, it: { ...IT('Extractor alarm', 'The galley extractor\'s alarm and, beside it, the switch that opens the vents. Brennan has views on how often it goes off.'), alarm: true, vent: true } });
    placeWall('M', 'spiceShelf', 'e', SPICES.along, { hitW: 1.3, it: IT('Spice shelf', 'A shelf over the drinks for spices brought from home. Brennan says it will fill up. Brennan is patient.') });   // 0.38.31
    placeWall('M', 'menuBoard', 'e', 3.5, { hitW: 1.2, it: IT('Menu board', 'Two meals a day: breakfast 06:00 to 09:00, dinner 17:00 to 20:30. Today: Brennan\'s spiced lentils.') });
    placeWall('M', 'notices', 'w', 4.5, { hitW: 1.0, it: IT('Mess notices', 'This week\'s birthdays, the galley rota, and a polite note about taking mugs back to the mess.') });
    for (const x of [.45, 5.0]) place('M', 'plant', x, .45, 'n', { band: '#c86b4a' });   // under the windows, out of the aisles

    // ---- the serving counter, from both sides ----
    [4, 5, 6].forEach((j, k) => placeOnEdge('passShelf', `v,35,${j}`, 'w', { plate: k === 1 ? 0 : k === 2 ? 2 : 0 }));

    // ---- galley: ranges along the bow wall, ovens by the cold store, the prep island in the middle, the dish pit by the back door ----
    place('K', 'galley', 5.54, 1.5, 'e', { w: 2.8, it: IT('Ranges', 'Six burners and a flat-top, under a hood that roars. Something is always simmering. Chef Brennan cooks by ear.') });
    place('K', 'ovenStack', 3.0, .45, 'n', { it: IT('Ovens', 'Two tall ovens. The top left one runs hot, and only Chef Brennan knows by how much. It\'s on the Works job board.') });
    place('K', 'prepIsland', 3.0, 3.0, 'n', { it: IT('Prep island', 'A steel table, a chopping board and a knife nobody else is allowed to use.') });
    place('K', 'dishPit', 5.55, 5.0, 'e', { it: IT('Dish pit', 'A deep sink, a sprayer and the dish machine. The worst job in the galley, and the best place to hear gossip.') });
    place('K', 'stool', .5, .5, 'n', { it: IT('Stool', 'Chef Brennan\'s. She sits on it exactly once a day, after dinner, with tea.') });
    placeWall('K', 'shelf', 's', 1.5);

    // ---- cold store: frosted shelving along the hull, the chest freezer, crates up from the cargo hold ----
    [.75, 2.0, 3.25].forEach((x, k) => place('C', 'coldShelf', x, .33, 'n', { it: k === 1 ? IT('Cold shelves', 'Milk, cheese, eggs, and a whole shelf of things labelled FEN in thick pen. Breath fogs in here.') : undefined }));
    place('C', 'chestFreezer', 3.55, 2.0, 'e', { it: IT('Chest freezer', 'Frozen stock and a tub of ice cream with someone\'s name on it, crossed out, then written back.') });
    place('C', 'crate', .45, 1.6, 'w', { it: IT('Crates', 'Up from the cargo hold by hover cart. One says FRAGILE: EGGS, with three exclamation marks.') });
    place('C', 'crate', .45, 2.5, 'w', { turn: .12 });

    // ---- bow lounge. The bar end: the curved bar round the galley door, high tables to port, booths to starboard.
    // The window end, past the glass screens: a sofa and armchairs facing the bow, two quiet corners, a telescope.
    place('L', 'backBar', .33, 3.9, 'w', { it: IT('Back bar', 'Bottles in every colour against a mirror. Most of them are juice. The ones that aren\'t, the Captain keeps a list of.') });
    place('L', 'backBar', .33, 7.85, 'w');
    place('L', 'barTaps', 2.6, 5.6, 'w', { turn: 0 });
    for (let k = 0; k < 8; k++) {                         // stools round the outside of the bar, facing in
      const a = (-70 + k * 20) * Math.PI / 180, x = Math.cos(a) * 3.12, z = 5.6 + Math.sin(a) * 3.12;
      place('L', 'barStool', x, z, 'n', { turn: Math.atan2(-Math.cos(a), -Math.sin(a)) });
    }
    place('L', 'highTable', 4.8, 2.9, 'n', { it: IT('High table', 'Where people stand when they say they\'re only staying for one.') });
    place('L', 'highTable', 3.7, 1.9, 'n', { turn: .8 });
    const BF = [LNG.navy, LNG.rust, LNG.olive];
    [14.6, 16.6, 18.6].forEach((z, k) => place('L', 'booth', .85, z, 'w', { fab: BF[k], k: k + 1, it: [
      IT('Booth', 'The good booth. Claimed by whoever gets off shift first.'),
      IT('Booth', 'Someone has carved a tiny Wren into the table edge, very neatly.'),
      IT('Booth', 'The quiet booth at the end. People come here to talk about things.')][k] }));
    // the window end
    place('L', 'rug', 8.1, 11, 'w', { tex: rugCabin, w: 3.8, d: 3.2 });
    place('L', 'sofa', 6.95, 11, 'w', { w: 2.4, fab: LNG.navy, it: IT('Sofa', 'Facing the bow windows and nothing else. The best seat on the ship, and everyone knows it.') });
    place('L', 'coffeeTable', 8.4, 11, 'w');
    place('L', 'armchair', 8.6, 9.0, 'n', { turn: -.15, fab: LNG.rust });
    place('L', 'armchair', 8.6, 13.0, 's', { turn: .15, fab: LNG.rust });
    place('L', 'floorLamp', 6.3, 9.4, 'n', { light: true });
    for (const [z, sd] of [[6.0, -1], [16.0, 1]]) {        // two quiet corners by the windows, port and starboard
      place('L', 'teaTable', 6.6, z, 'n');
      place('L', 'armchair', 5.85, z + sd * 1.1, sd < 0 ? 'n' : 's', { turn: sd * -.9, fab: LNG.olive });
      place('L', 'armchair', 7.45, z - sd * .75, sd < 0 ? 's' : 'n', { turn: sd * -.9, fab: LNG.olive });
      place('L', 'floorLamp', 5.7, z - sd * .6, 'n');
    }
    place('L', 'telescope', 9.2, 7.6, 'w', { turn: -.7, it: IT('Telescope', 'Pointed at a smudge of stars off the bow. A note taped to it says PLEASE DO NOT RE-AIM. Under it, in different writing: re-aimed.') });
    for (const z of [9.55, 12.45]) place('L', 'plant', .45, z, 'w', { big: true, band: '#c9a24a' });
    // ---- hydroponics garden: racks of greens under pink grow lights along both hulls, raised beds of salad, herbs,
    // tomatoes and flowers, two little fruit trees, a trellis on the stern wall and one by the recycler, the herb wall
    // by the door, and in the middle a pond with benches round it and a stepping-stone path from the promenade.
    const G = 'G';
    [2.4, 4.4, 6.4, 8.4].forEach((x, k) => place(G, 'growRack', x, .38, 'n', { fadeGroup: 'G:racksN', it: k === 1 ? IT('Grow racks', 'Three tiers of lettuce, pea shoots and microgreens under pink light. It looks strange, and the plants love it.') : undefined }));
    [5.4, 7.4].forEach((x, k) => place(G, 'growRack', x, 21.6, 's', { fadeGroup: 'G:racksS', it: k ? IT('Grow racks', 'Starboard side: spinach, chard and a tray labelled EXPERIMENTAL that nobody will explain.') : undefined }));
    place(G, 'moss', 1.2, 2.2, 'n', { r: .8 });
    place(G, 'citrusTree', 1.2, 2.2, 'n', { it: IT('Orange tree', 'Eleven oranges this year. Chef Brennan has counted them, and so has everyone else.') });
    place(G, 'moss', 9.4, 20.6, 'n', { r: .7 });
    place(G, 'citrusTree', 9.4, 20.6, 'n', { lemon: true, it: IT('Lemon tree', 'Grown from a pip by someone long since transferred. The galley gets every lemon.') });
    const BED = { greens: 'Salad bed', herbs: 'Herb bed', tomato: 'Tomatoes', flowers: 'Flower bed' };
    const BEDX = { greens: 'Lettuce in neat rows. Picked at dawn, in the mess by breakfast.', herbs: 'Basil, mint, thyme and coriander. The galley takes a handful every afternoon.',
      tomato: 'Vines up their stakes and fruit going red. Everyone eats one straight off the plant. Everyone denies it.', flowers: 'Not for eating. For bees, if we had them, and for people, who we do.' };
    [[3.4, 2.75, 'greens'], [6.0, 2.75, 'herbs'], [8.6, 2.75, 'greens'], [3.4, 5.3, 'tomato'], [6.0, 5.3, 'flowers'], [8.6, 5.3, 'tomato'],
     [3.4, 15.4, 'flowers'], [6.0, 15.4, 'greens'], [8.6, 15.4, 'herbs'], [6.0, 18.8, 'greens'], [8.6, 18.8, 'tomato']].forEach(([x, z, crop], k) =>
      place(G, 'raisedBed', x, z, 'n', { crop, live: { greens: 'greens', herbs: 'herbs', tomato: 'tomatoes' }[crop], butterflies: crop === 'flowers', it: [0, 1, 3, 4].includes(k) ? IT(BED[crop], BEDX[crop]) : undefined }));
    place(G, 'trellis', .3, 5.0, 'w', { live: 'beans', it: IT('Bean trellis', 'Runner beans up a frame against the stern windows, so the beans get the stars.') });
    place(G, 'trellis', 9.75, 16.5, 'e', { live: 'beans' });
    placeWall(G, 'herbWall', 'e', 7.5, { hitW: 1.6, it: IT('Herb wall', 'Pockets of herbs by the door, labelled FOR THE GALLEY in Chef Brennan\'s writing. Take a sprig and she will know.') });
    // the pond, its benches and the path
    place(G, 'moss', 4.5, 11.0, 'n', { r: 1.75 });
    place(G, 'pond', 4.5, 11.0, 'n', { it: IT('Pond', 'Three fish, two lily pads per fish, and a stone that bubbles. The fish are called Port, Starboard and Steve.') });
    place(G, 'bench', 4.5, 8.45, 'n', { it: IT('Bench', 'The best seat in the garden: the pond in front, the stars behind.') });
    place(G, 'bench', 4.5, 13.55, 's'); place(G, 'bench', 1.7, 11.0, 'w');
    place(G, 'gardenLamp', 6.7, 9.2, 'n', { light: true }); place(G, 'gardenLamp', 2.4, 13.3, 'n');
    const stones = [[9.4, 11], [8.5, 11.25], [7.6, 10.95], [6.75, 11.15]];
    for (let k = 0; k < 12; k++) { const a = k / 12 * Math.PI * 2; if (k === 9 || k === 3 || k === 6) continue; stones.push([4.5 + Math.cos(a) * 1.65, 11 + Math.sin(a) * 1.65]); }
    stones.push([5.6, 8.4], [6.3, 7.6], [7.0, 6.8], [5.9, 13.7], [6.5, 14.4], [3.0, 13.8], [2.5, 14.6]);
    for (const [x, z] of stones) place(G, 'stepStone', x, z, 'n');
    // a real tree by the pond, and ground cover spilling into every corner and along the walls
    place(G, 'bigTree', 2.5, 8.7, 'n', { it: IT('The garden tree', 'Planted the year the Wren launched. Its fronds just reach the pond, and the fish like the shade.') });
    for (const [x, z, r, v] of [[2.4, 8.7, .9, 0], [.7, 9.6, .6, 1], [.7, 12.6, .6, 2], [7.4, 9.6, .5, 3], [7.4, 12.6, .55, 4], [9.5, 3.9, .45, 0], [.6, 3.3, .5, 2],
      [2.0, 16.4, .5, 1], [9.6, 14.6, .45, 3], [4.5, 21.3, .5, 4], [9.6, 18.0, .4, 2], [6.2, 7.6, .4, 1], [3.0, 7.0, .45, 0], [8.4, 7.0, .45, 3]])
      place(G, 'groundCover', x, z, 'n', { r, v });
    // bushes and blooms to fill every corner
    for (const [x, z, s, b] of [[9.45, 9.45, .8, 1], [9.45, 12.55, .8, 3], [.6, 7.7, 1.3, 0], [.6, 14.3, 1.3, 2], [2.9, 9.4, .7, 4], [6.4, 12.7, .7, 0],
      [4.5, 19.6, .8, 1], [9.4, 13.7, .8, 2], [.6, 16.2, .8, 0]]) place(G, 'bush', x, z, 'n', { size: s, bloom: b, v: Math.round(x + z) });
    place(G, 'pollen', 6.0, 4.0, 'n', { w: 7, d: 4 }); place(G, 'pollen', 6.0, 16.6, 'n', { w: 7, d: 4 }); place(G, 'pollen', 4.5, 11, 'n', { w: 3, d: 3 });

    // ---- infirmary: four beds under the port windows, the front desk by the wide doors, the medicine cabinet ----
    [1.5, 3.5, 5.5, 7.5].forEach((x, k) => place('I', 'medBed', x, 1.12, 'n', { curtain: k === 1 || k === 2, it: [
      IT('Bed 1', 'Made up tight enough to bounce a coin. Rina does them every morning whether anyone is ill or not.'),
      IT('Bed 2', 'Curtain half drawn. Nobody in it, but the monitor is on, out of habit.'),
      IT('Bed 3', 'The one by the cabinet. Whoever is in it gets the best stories from Rina.'),
      IT('Bed 4', 'Nearest the door, for anyone who just needs a lie-down and a glass of water.')][k] }));
    for (const x of [2.5, 6.5]) place('I', 'chair', x, 2.5, 'n', { turn: .3 });
    place('I', 'medDesk', 9.9, 3.8, 'e', { it: IT('Front desk', 'A terminal, a bell, and a jar of mints that refills itself, or so Rina claims.') });
    place('I', 'chair', 10.55, 3.8, 'w');
    place('I', 'medCabinet', 10.68, .9, 'e', { it: IT('Medicine cabinet', 'Glass-fronted and locked. Labels in two colours: one for every day, one for please don\'t.') });
    place('I', 'shelving', .3, 4.4, 'w', { it: IT('Supplies', 'Bandages, splints, blankets and a box marked SPARE THERMOMETERS that is somehow always empty.') });
    place('I', 'plant', 9.2, .45, 'n', { band: '#2f8e98' });
    placeWall('I', 'notices', 'w', 2.5, { hitW: 1.0, it: IT('Health notices', 'Wash your hands. Drink water. Sleep. A rota for check-ups, and a cartoon of a germ in a Works hard hat.') });
    // exam room
    place('X', 'examBed', 1.35, 2.2, 's', { it: IT('Exam bed', 'Paper on the bed and a scanner on an arm overhead. The doctor checks whoever is run-down in here.') });
    place('X', 'deskSmall', 4.3, .45, 'n'); place('X', 'chair', 4.3, 1.15, 's');
    place('X', 'plant', 4.6, 2.55, 'e', { band: '#2f8e98' });

    // ---- washrooms ----
    furnish('w', 'washroom', { toilets: true, bench: false });   // 0.38.27 (the user's): no bench in here

    // ---- gym: treadmills and the rower facing the starboard windows, weights by the store wall, mats in the corner ----
    // (Pillar 2, the Deck 6 architect: `place` names the place on each machine, so its belt or seat moves while someone uses it)
    [1.5, 2.85, 5.5, 4.2].forEach((x, k) => place('F', 'treadmill', x, 7.55, 's', { place: '3-gym-' + (k < 3 ? k + 1 : 15), it: k === 1 ? IT('Treadmills', 'Facing the windows, so you can run towards the stars and never get any closer.') : undefined }));   // 0.38.28: a fourth (3-gym-15); the second moved west
    place('F', 'rower', 7.6, 7.4, 's', { place: '3-gym-4', it: IT('Rowing machine', 'The ship\'s most argued-over leaderboard is taped to it. Vance is top. Vance taped it there.') });
    place('F', 'weightRack', 8.62, 2.6, 'e', { it: IT('Weights', 'Dumbbells from light to ridiculous. The ridiculous ones have never been moved.') });
    place('F', 'weightBench', 6.4, 3.0, 'w');
    place('F', 'gymMats', 1.6, 2.6, 'n', { it: IT('Stretching mats', 'Three mats, a ball and a roller. Mostly used for lying down and calling it stretching.') });
    placeWall('F', 'gymMirror', 'w', 3.0);
    place('F', 'dispenser', 8.5, .35, 'n', { it: IT('Water', 'Cold water and a stack of cups. The cups are always gone by 18:00.') });
    placeWall('F', 'notices', 'e', 6.0, { hitW: 1.0, it: IT('Gym rota', 'Sign-up sheet for the treadmills. Someone has written their name in every slot and been crossed out.') });
    place('F', 'plant', .45, .45, 'n', { band: '#e9c46a' });

    // ---- crew store: shelves both sides, the counter, a fridge of drinks at the back, and the window display ----
    for (const z of [3.0, 4.4, 5.8]) place('S', 'shopShelf', .31, z, 'w', { fadeGroup: 'S:w', it: z === 4.4 ? IT('Shelves', 'Toothpaste, socks, snacks, birthday cards and batteries, in no order anyone has worked out.') : undefined });
    for (const z of [4.4, 5.8]) place('S', 'shopShelf', 3.69, z, 'e', { fadeGroup: 'S:e' });
    // the counter stands out from the east wall, so whoever's on the till stands behind it (0.31.2: the store is staffed)
    place('S', 'counter', 2.85, 2.5, 'e', { it: IT('Counter', 'Whoever\'s on the counter scans your badge. The honesty box is for the hours nobody is.') });
    place('S', 'till', 2.85, 1.85, 'e', { it: IT('Till', 'The storekeeper taps your badge on the pad and the screen thanks you by name. It has never once been wrong about the price of socks.') });   // A5b
    place('S', 'basketStack', .4, .5, 'n', { it: IT('Baskets', 'Wire baskets in department colours. Take one, fill it, pay at the till.') });
    // ---- the utility rooms (A5b; plans/deck3-plan.html "Utility rooms"). Water recycler R starts at (12, 13), galley plant g at
    // (39, 0), irrigation room i at (2, 17). A walkway runs from each hatch past every machine's panel.
    place('R', 'recyclerTanks', 1.0, 3.5, 'w', { it: IT('Water recycler', 'Two settling tanks, a control head between them, and a sight glass you can watch the water level in. Every deck\'s water comes through here.') });
    place('R', 'filterBank', .55, 6.95, 'w', { it: IT('Filter bank', 'Six cartridges in a rack. Swapping them is the job everyone learns first and nobody likes.') });
    place('R', 'pumpSkid', 4.3, 4.0, 'e', { it: IT('Circulation pumps', 'Two pumps on one skid, pushing clean water up the spine to every deck. You can feel them through the floor.') });
    place('R', 'uvUnit', 1.0, .4, 'n', { it: IT('UV steriliser', 'A lamp tube in a steel sleeve, glowing blue through the slot. The last step before the tanks.') });
    place('R', 'cleanTank', 4.2, 7.5, 'e', { it: IT('Clean-water tank', 'Full to the line on the gauge. Everything the ship drinks and washes in waits here first.') });
    place('R', 'risers', 4.0, .3, 'n', { it: IT('Risers', 'Clean water up, used water down, through the spine to every deck.') });
    place('R', 'sump', 1.0, 8.55, 's');
    placeWall('R', 'relayBox', 'e', 2.5, { it: IT('Light relays', 'Deck 3\'s light relays: every lamp from the garden to the lounge runs through this box.') });
    placeWall('R', 'wallCalendar', 'n', 2.5, { it: IT('Calendar', 'A paper calendar, days crossed off in three different pens. Filter day is circled every week, with a frowning face.') });
    placeWall('R', 'radioShelf', 'w', 5.4, { it: IT('Radio', 'Somebody\'s radio, tuned low to a music channel from home, and a mug of tea gone cold beside it.') });
    placeWall('R', 'handSign', 's', 2.5, { it: IT('Sign', 'Hand-lettered: MIND THE SUMP. Underneath, smaller: seriously.') });
    place('g', 'extractorUnit', 1.0, .45, 'n', { it: IT('Extractor fans', 'The galley hoods\' fan, its motor and the grease filters. It hums all day and roars at mealtimes.') });
    place('g', 'chillerUnit', 1.55, 2.0, 'e', { it: IT('Chiller', 'The cold store\'s chiller, with the dishwasher pumps tucked in beside it.') });
    placeWall('g', 'handSign', 'w', 2.2, { it: IT('Sign', 'IF THE FAN STICKS: KNOCK TWICE, THEN CALL WORKS. In the chef\'s handwriting.') });
    place('i', 'nutrientTanks', 3.3, 2.0, 'e', { it: IT('Nutrient tanks', 'Two tanks of garden feed and the dosing unit that mixes them. It smells faintly of tomato leaves.') });
    place('i', 'irrigationPump', 3.4, 3.9, 'e', { it: IT('Irrigation pump', 'The pump and a row of valves, one for each part of the garden.') });
    place('i', 'headerPipes', .25, 1.5, 'w');
    placeWall('i', 'wallCalendar', 'n', 3.4, { it: IT('Planting calendar', 'Sowing and feeding days for every bed in the garden, in the gardeners\' neat print.') });
    place('S', 'drinksFridge', 2.0, 8.55, 's', { it: IT('Drinks fridge', 'Fizzy drinks in colours not found in nature. The orange one sells out first.') });
    place('S', 'shopDisplay', 2.5, .5, 'n', { it: IT('Window display', 'This week: new socks in department colours, and a single, expensive jar of real honey.') });

    // ---- call-home booths: four cubicles under the starboard windows, a waiting sofa, clocks and the message queue ----
    [.62, 1.84, 3.06, 4.28].forEach((x, k) => place('B', 'callBooth', x, 8.3, 's', { live: k === 1 || k === 3, it: [
      IT('Booth 1', 'Free. A box of tissues, a pair of headphones and the stars through the window.'),
      IT('Booth 2', 'Someone is recording a message. The screen shows a child\'s drawing held up to a camera, light-years away.'),
      IT('Booth 3', 'Free. A note stuck to the screen: SAY THE THING YOU MEANT TO SAY.'),
      IT('Booth 4', 'Playing a message on loop, volume low. Whoever it is for has stepped out to compose themselves.')][k] }));
    place('B', 'sofa', 2.5, 3.0, 'n', { w: 2.0, fab: LNG.olive, it: IT('Waiting sofa', 'Where people wait for a booth, and sometimes sit for a while after.') });
    placeWall('B', 'clocks', 'e', 3.0, { hitW: 1.5, it: IT('Three clocks', 'Ship time, home time, and how long a message takes to get there. The third one is the hardest to look at.') });
    placeWall('B', 'postcardBox', ...POSTCARDS.box, { hitW: .5, it: IT('Post box', 'Cards and letters home go in here and out with the next mail run. Eklund empties it, and reads none of them. He says.') });   // 0.38.31
    placeWall('B', 'writingLedge', ...POSTCARDS.ledge, { hitW: 1.8, it: IT('Writing ledge', 'Blank postcards, a pot of pens, and just enough room to lean on while you think of what to say.') });
    placeWall('B', 'msgBoard', 'w', 3.0, { hitW: 1.0, it: IT('Messages waiting', 'Who has something from home. Vance has two. Your line says none yet.') });
    for (const x of [.45, 4.55]) place('B', 'plant', x, .45, 'n', { band: '#d9a441' });
    // ---- Pillar 3 (C9, 0.38.2): more gym kit, last so nothing above moves; none of it calls R() ----
    [1.0, 1.8].forEach((x, k) => place('F', 'rower', x, 4.6, 's', { place: '3-gym-' + (11 + k), it: k ? IT('Rowing machines', 'A matched pair, side by side, so two people can race. Somebody always says it isn\'t a race.') : undefined }));
    place('F', 'punchBag', 7.5, 4.5, 'e', { place: '3-gym-13', it: IT('Punch bag', 'Patched with tape in three places. The Watch crew say it helps them think. The Works crew say it helps them not think.') });
    place('F', 'gymMat', 4.9, 4.6, 's', { it: IT('Stretching mat', 'One more mat, rolled out in the middle of the room, for people who want to stretch where everyone can see them do it.') });
    [5.5, 6.5].forEach((x, k) => place('F', 'exerciseBike', x, .95, 'n', { place: '3-gym-' + (16 + k), it: k ? undefined : IT('Exercise bikes', 'Two bikes facing the promenade, so everyone walking past can see how hard you aren\'t pedalling.') }));   // 0.38.28
    // ---- the galley's root beds and third bean bed (C9, 0.38.7), grown by section 8b's garden view; last, since raisedBed and trellis draw R() ----
    [[8.1, 8.9, 'e'], [8.1, 13.15, 'e'], [5.7, 17.45, 'n']].forEach(([x, z, b], k) => place('G', 'raisedBed', x, z, b, { crop: 'roots', live: 'roots', it: k ? undefined : IT('Root beds', 'Carrots, beets and turnips, a month from seed to the galley. Chef Brennan pulls one up every few days to check, and pretends she\'s only weeding.') }));
    place('G', 'trellis', .3, 14.8, 'w', { live: 'beans', it: IT('Bean trellis', 'A second frame of runner beans against the stern windows. The galley wanted more beans. The galley always wants more beans.') });
    // ---- Pillar 4, seat 8 (0.38.10): the seedling stand in the garden's north-east corner (Sowing morning) and the bow lounge's Tiles station ----
    place('G', 'seedlingStand', 9.63, .42, 'n', { yours: DECKS[3].seedlings.yours, it: IT('Seedlings', 'A little stepped stand of pots by the grow racks: one seedling for everyone who came to the last Sowing morning. One pot is only soil, waiting.') });
    place('L', 'tilesTable', 3.5, 18.5, 'n', { it: IT('Tiles station', 'A Tiles board, always set up, a tray of spare tiles and two stools. Sit down and someone usually sits down opposite.') });
  },

};
for (const [key, r] of Object.entries(DECKS[3].sealed)) DECKS[3].closedDoors[key] = { t: DECKS[3].rooms[r].name, x: DECKS[3].rooms[r].tap };

