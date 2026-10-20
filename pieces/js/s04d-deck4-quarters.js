// =====================================================================
// DECK 4: QUARTERS. Generated from deck4-plan.html (the plan's tile map, minus its
// empty margin rows). Junior wing aft, lift lobby midships, officers' corridor forward.
// =====================================================================
DECKS[4] = {
  num: 4, name: 'Quarters', seed: 48211,
  blurb: 'Bunks, cabins, washrooms', arrive: 'Junior wing aft, officers\' corridor forward. Your bunk is in Bunk 1.',
  lift: [21, 10],                                  // the lift car's centre in tile units: lines the deck up with the others
  map: [
    '..ppppaaaaabbbbbcccccsssAAAEEEIIIMMMQQQUUUxx......',
    '..ppppaaaaabbbbbcccccsssAAAEEEIIIMMMQQQUUUxxxx....',
    '..ppppaaaaabbbbbcccccsssAAAEEEIIIMMMQQQUUUxxxxx...',
    '..ppppaaaaabbbbbcccccsssAAAEEEIIIMMMQQQUUUxxxxxx..',
    '..================++++++--------------------nnnnn.',
    '..================++++++--------------------nnnnn.',
    '..jjjjjjeeeeeggggg++YY++BBBFFFJJJNNNRRRVVV--nnnnn.',
    '..jjjjjjeeeeeggggg++YY++BBBFFFJJJNNNRRRVVV--nnnnnn',
    '..jjjjjjeeeeeggggg++@@++BBBFFFJJJNNNRRRVVV--nnnnnn',
    '..jjjjjjeeeeeggggg++@@++BBBFFFJJJNNNRRRVVV--nnnnnn',
    '..jjjjjjfffffhhhhh++@@++CCCGGGKKKOOOSSSWWW--nnnnnn',
    '..jjjjjjfffffhhhhh++ZZ++CCCGGGKKKOOOSSSWWW--nnnnnn',
    '..jjjjjjfffffhhhhh++ZZ++CCCGGGKKKOOOSSSWWW--nnnnnn',
    '..jjjjjjfffffhhhhh++ZZ++CCCGGGKKKOOOSSSWWW--nnnnn.',
    '..================++++++--------------------nnnnn.',
    '..================++++++--------------------nnnnn.',
    '..qqqqdddddlllluuuktttttDDDHHHLLLPPPTTTXXXyyyyyy..',
    '..qqqqdddddlllluuuktttttDDDHHHLLLPPPTTTXXXyyyyy...',
    '..qqqqdddddlllluuuktttttDDDHHHLLLPPPTTTXXXyyyy....',
    '..qqqqdddddlllluuuktttttDDDHHHLLLPPPTTTXXXyy......',
  ],
  // doors: generated from the Deck 4 plan. 'closed' doors stay shut and say why (closedDoors); 'lift' is the main lift
  doors: {
    'h,25,4': 'closed', 'h,25,6': 'closed', 'h,25,14': 'closed', 'h,25,16': 'closed', 'h,28,4': 'closed',
    'h,28,6': 'closed', 'h,28,14': 'closed', 'h,28,16': 'closed', 'h,31,4': 'closed', 'h,31,6': 'closed',
    'h,31,14': 'closed', 'h,31,16': 'closed', 'h,34,4': 'closed', 'h,34,6': 'closed', 'h,34,14': 'closed',
    'h,34,16': 'closed', 'h,37,4': 'closed', 'h,37,6': 'closed', 'h,37,14': 'closed', 'h,37,16': 'closed',
    'h,40,4': 'closed', 'h,40,6': 'closed', 'h,40,14': 'closed', 'h,40,16': 'closed', 'h,8,4': 'door',
    'h,13,4': 'door', 'h,17,4': 'door', 'h,8,16': 'door', 'h,10,6': 'door', 'h,10,14': 'door', 'h,15,6': 'door',
    'h,15,14': 'door', 'h,4,14': 'door', 'h,4,6': 'door', 'h,18,16': 'hatch', 'h,12,16': 'door', 'h,3,4': 'door',
    'h,3,16': 'door', 'h,21,4': 'hatch', 'h,20,16': 'hatch', 'h,15,16': 'hatch', 'h,43,4': 'closed',
    'h,43,16': 'hatch', 'v,44,9': 'door', 'v,44,10': 'door', 'v,20,10': 'lift', 'v,20,9': 'lift', 'v,20,8': 'lift', 'v,22,10': 'lift', 'v,22,9': 'lift', 'v,22,8': 'lift',
    // the spine: glass onto the air and power trunks above the car and the ladder well below it; a hatch down the ladder
    'v,20,6': 'glass', 'v,22,6': 'glass', 'h,20,6': 'glass', 'h,21,6': 'glass',
    'v,20,12': 'glass', 'v,20,13': 'glass', 'v,22,12': 'glass', 'v,22,13': 'glass', 'h,21,14': 'glass', 'h,20,14': 'hatch',
  },
  // door plates [edge, the side the corridor is on, text]
  plates: [
    ['h,4,4', 's', 'Washroom'], ['h,9,4', 's', 'Bunk 1'], ['h,14,4', 's', 'Bunk 2'], ['h,16,4', 's', 'Bunk 3'],
    ['h,23,4', 's', 'Scrubbers'], ['h,26,4', 's', 'Guest 4-02'], ['h,29,4', 's', '4-06'], ['h,32,4', 's', '4-10'],
    ['h,35,4', 's', '4-14'], ['h,38,4', 's', '4-18'], ['h,41,4', 's', '4-22'], ['h,42,4', 's', 'Supply'],
    ['h,5,6', 'n', 'Common room'], ['h,5,14', 's', 'Common room'], ['h,11,6', 'n', 'Bunk 5'],
    ['h,14,6', 'n', 'Bunk 7'], ['h,19,16', 'n', 'Utility'], ['h,26,6', 'n', 'Guest 4-04'], ['h,29,6', 'n', 'Guest 4-08'],
    ['h,32,6', 'n', '4-12'], ['h,35,6', 'n', '4-16'], ['h,38,6', 'n', '4-20'], ['h,41,6', 'n', 'Spare 4-24'],
    ['h,11,14', 's', 'Bunk 6'], ['h,14,14', 's', 'Bunk 8'], ['h,26,14', 's', 'Guest 4-03'], ['h,29,14', 's', 'Guest 4-07'],
    ['h,32,14', 's', '4-11'], ['h,35,14', 's', '4-15'], ['h,38,14', 's', '4-19'], ['h,41,14', 's', 'Spare 4-23'],
    ['h,4,16', 'n', 'Washroom'], ['h,9,16', 'n', 'Bunk 4'], ['h,13,16', 'n', 'Laundry'], ['h,16,16', 'n', 'Stores'],
    ['h,21,16', 'n', 'Heating'], ['h,26,16', 'n', 'Guest 4-01'], ['h,29,16', 'n', '4-05'], ['h,32,16', 'n', '4-09'],
    ['h,35,16', 'n', '4-13'], ['h,38,16', 'n', '4-17'], ['h,41,16', 'n', '4-21'], ['h,42,16', 'n', 'Utility'],
    ['v,44,8', 'w', 'Music room'],
  ],
  sconces: [['h,19,4', 's'], ['h,20,4', 's'], ['h,27,4', 's'], ['h,36,4', 's'], ['h,39,4', 's'], ['h,44,4', 's'], ['h,19,16', 'n'], ['h,23,16', 'n'], ['h,27,16', 'n'], ['h,36,16', 'n'], ['h,39,16', 'n'], ['h,44,16', 'n']],
  // six guest cabins nearest the lift (the first column, and the inner pair of the second): guests come and go, so they
  // don't walk the corridor's length. Two spares at the quiet music-room end. The other sixteen are officers'.
  guests: {
    A: 'Guest cabin. Currently a visiting hydrologist\'s, here to look at the water recycler. Her boots are drying outside the door.',
    B: 'Guest cabin. A passenger bound for the next station, who keeps to himself and plays chess against the terminal.',
    C: 'Guest cabin. A navigator from another ship, on her way home. She has already learned everyone\'s name.',
    D: 'Guest cabin. A survey specialist who came aboard for the nebula. Crates of her instruments wait in the cargo hold.',
    F: 'Guest cabin. A delegation\'s secretary, travelling ahead of the delegation. He writes everything down.',
    G: 'Guest cabin. A mechanic off a salvage tug, waiting for parts. She has offered to help the Works crew twice already.',
  },
  spares: ['V', 'W'],
  cabins: [['A', '4-02'], ['B', '4-04'], ['C', '4-03'], ['D', '4-01'], ['E', '4-06'], ['F', '4-08'], ['G', '4-07'], ['H', '4-05'], ['I', '4-10'], ['J', '4-12'], ['K', '4-11'], ['L', '4-09'], ['M', '4-14'], ['N', '4-16'], ['O', '4-15'], ['P', '4-13'], ['Q', '4-18'], ['R', '4-20'], ['S', '4-19'], ['T', '4-17'], ['U', '4-22'], ['V', '4-24'], ['W', '4-23'], ['X', '4-21']],
  rooms: {
    '=': { name: 'Junior corridor', floor: 'corridor', hall: true },
    '+': { name: 'Lift lobby', floor: 'lobby', hall: true },
    '-': { name: 'Officers\' corridor', floor: 'carpet', hall: true },
    n: { name: 'Music room', floor: 'wood' },                          // soundproofed, at the end of the officers' corridor
    '#': { name: 'Spine', void: true },
    '@': { name: 'Main lift', floor: 'lift' },
    Y: { name: 'Spine trunks', floor: 'grate', spine: true }, Z: { name: 'Spine ladder', floor: 'grate', spine: true },
    j: { name: 'Junior common room', floor: 'wood' },
    p: { name: 'Port washroom', floor: 'tile' }, q: { name: 'Starboard washroom', floor: 'tile' }, l: { name: 'Laundry', floor: 'tile' },
    // utility rooms (Pillar 2, 0.30.2): floors that draw no random numbers, so the rest of the deck is unchanged
    u: { name: 'Junior stores', floor: 'plate', still: true }, k: { name: 'Utility closet', floor: 'plate', still: true },
    s: { name: 'Air scrubbers', floor: 'steel', still: true }, t: { name: 'Heating plant', floor: 'steel', still: true },
    x: { name: 'Port supply closet', floor: 'plate' }, y: { name: 'Starboard utility closet', floor: 'plate' },
  },
  // hull windows: a stretch of a flat side ('n' port, 's' starboard, 'w' stern) from a to b, or every hull wall of a room
  windows: ['j', 'a', 'b', 'c', 'd', 'n', 'A', 'D', 'E', 'H', 'I', 'L', 'M', 'P', 'Q', 'T', 'U', 'X'].map(room => ({ room })),
  // doors that stay shut, and what they say when you tap them (locked rooms are filled in by lockedRoom)
  closedDoors: {
    'h,20,14': { t: 'Spine ladder', x: 'The maintenance ladder runs the whole height of the ship, beside the lift. Crawlways branch off it on every deck. Tier 2 access.' },
    'h,43,4': { t: 'Port supply closet', x: 'Bulbs, filters and cleaning kit for the officers\' wing.' },
  },
  // service hatches into the utility rooms (0.30.2): the player and Works crew pass (see hatchPassable)
  // tier (0.30.12): who may go in, once the systems engineer's rule reads it: 1 closets and stores, 2 plant rooms, 3 batteries and junctions
  service: [{ key: 'h,21,4', tier: 2 }, { key: 'h,20,16', tier: 2 }, { key: 'h,18,16', tier: 1 }, { key: 'h,15,16', tier: 1 }, { key: 'h,43,16', tier: 1 }],   // scrubbers, heating, junior closet, stores, officers' closet y (0.30.5)
  // machines (Pillar 2): at = the machine's tile in front of its panel; face = the way its front faces (toward the panel);
  // panel = where a Works tech stands, with a work:works place '<id>-svc' on it. look (0.30.13): where section 8b's wear lamp and
  // drips go, fitted to each piece's front (format in DEV_NOTES "Machine looks")
  machines: [
    { id: '4-scrubber-1', kind: 'scrubber', at: [21, 1], room: 's', face: 's', panel: [21, 2], look: { lamp: [0, 1.2, 0.34], drip: [0, 0.9, 0.39] } },
    { id: '4-scrubber-2', kind: 'scrubber', at: [23, 1], room: 's', face: 's', panel: [23, 2], look: { lamp: [0, 1.2, 0.34], drip: [0, 0.9, 0.39] } },
    { id: '4-heater-1', kind: 'heater', at: [22, 18], room: 't', face: 'w', panel: [21, 18], look: { lamp: [0, 1.2, 0.22], drip: [0, 0.9, 0.27] } },
    { id: '4-pump-1', kind: 'heatpump', at: [19, 18], room: 't', face: 'e', panel: [20, 18], look: { lamp: [0, 0.45, 0.33], drip: [0, 0.42, 0.38] } },
    { id: '4-pump-2', kind: 'heatpump', at: [19, 19], room: 't', face: 'e', panel: [20, 19], look: { lamp: [0, 0.45, 0.33], drip: [0, 0.42, 0.38] } },
    { id: '4-junction-1', kind: 'lights', at: [18, 19], room: 'k', face: 'n', panel: [18, 18], look: { lamp: [0, 1.2, 0.13], drip: [0, 0.9, 0.18] } },
    { id: '4-junction-2', kind: 'lights', at: [42, 19], room: 'y', face: 'n', panel: [42, 18], look: { lamp: [0, 1.2, 0.13], drip: [0, 0.9, 0.18] } },
    // the laundry's four washers (C9, 0.38.8): real machines in place of section 17's stand-ins (same ids), Washer 1 by the door end
    { id: '4-washer-1', kind: 'washer', at: [14, 19], room: 'l', face: 'n', panel: [14, 18], look: { lamp: [0, .75, .34], drip: [0, .12, .37], light: [0, .95, .34] } },
    { id: '4-washer-2', kind: 'washer', at: [13, 19], room: 'l', face: 'n', panel: [13, 18], look: { lamp: [0, .75, .34], drip: [0, .12, .37], light: [0, .95, .34] } },
    { id: '4-washer-3', kind: 'washer', at: [12, 19], room: 'l', face: 'n', panel: [12, 18], look: { lamp: [0, .75, .34], drip: [0, .12, .37], light: [0, .95, .34] } },
    { id: '4-washer-4', kind: 'washer', at: [11, 19], room: 'l', face: 'n', panel: [11, 18], look: { lamp: [0, .75, .34], drip: [0, .12, .37], light: [0, .95, .34] } },
  ],
  hull: { sternX: 2, stern: 1.5, bowFrom: 40, bowLen: 9.6, byFace: true },   // stern line, stern corner radius, where the bow curve starts, how far it reaches; one hull piece per facing (0.30.11)
  // 0.17.1: the bunk rooms grew, so the floor painter draws a different count of random numbers west of column 21. At column 21
  // of each row it picks up the value 0.17.0 had there, so the officers' wing floor, and everything built after the floor
  // (windows, furniture), come out exactly as before.
  floorSeeds: { col: 21, rows: [711683755, 1759808167, 1216786317, 1518978406, 1394564237, 428409510, 1513525194, 1949355503, 2060744245, 1234811932,
    1316166146, 2027868013, 1757106567, 84604698, 286774954, 2116181630, 1012310116, 1910995577, 818977669, 1104626985] },
  // what a locked room's door says when you tap it
  // places (Pillar 1): every spot where a crew member does something, for the schedules. Data only: nothing draws them.
  // { id, type, at: [col, row], face, pose, room }. Seats and beds sit on furniture tiles and are reached from the tile beside them;
  // face is the way the person faces there. deck_check.py checks every place can be reached.
  // Beds: 4-B<room>-<berth> (1-6) for the junior bunks (two berths per bunk, both on the bunk's tile), 4-01..4-24 for the cabins
  // (guest and spare cabins too, though the roster won't use them). Every cabin's wash pod is a shower place, 4-xx-wash.
  places: [
    { id: '4-B1-1', type: 'bed', at: [6, 1], face: 's', pose: 'lie', room: 'a' },
    { id: '4-B1-2', type: 'bed', at: [6, 1], face: 's', pose: 'lie', room: 'a' },
    { id: '4-B1-3', type: 'bed', at: [8, 1], face: 's', pose: 'lie', room: 'a' },
    { id: '4-B1-4', type: 'bed', at: [8, 1], face: 's', pose: 'lie', room: 'a' },
    { id: '4-B1-5', type: 'bed', at: [10, 1], face: 's', pose: 'lie', room: 'a' },
    { id: '4-B1-6', type: 'bed', at: [10, 1], face: 's', pose: 'lie', room: 'a' },
    { id: '4-B2-1', type: 'bed', at: [11, 1], face: 's', pose: 'lie', room: 'b' },
    { id: '4-B2-2', type: 'bed', at: [11, 1], face: 's', pose: 'lie', room: 'b' },
    { id: '4-B2-3', type: 'bed', at: [13, 1], face: 's', pose: 'lie', room: 'b' },
    { id: '4-B2-4', type: 'bed', at: [13, 1], face: 's', pose: 'lie', room: 'b' },
    { id: '4-B2-5', type: 'bed', at: [15, 1], face: 's', pose: 'lie', room: 'b' },
    { id: '4-B2-6', type: 'bed', at: [15, 1], face: 's', pose: 'lie', room: 'b' },
    { id: '4-B3-1', type: 'bed', at: [16, 1], face: 's', pose: 'lie', room: 'c' },
    { id: '4-B3-2', type: 'bed', at: [16, 1], face: 's', pose: 'lie', room: 'c' },
    { id: '4-B3-3', type: 'bed', at: [18, 1], face: 's', pose: 'lie', room: 'c' },
    { id: '4-B3-4', type: 'bed', at: [18, 1], face: 's', pose: 'lie', room: 'c' },
    { id: '4-B3-5', type: 'bed', at: [20, 1], face: 's', pose: 'lie', room: 'c' },
    { id: '4-B3-6', type: 'bed', at: [20, 1], face: 's', pose: 'lie', room: 'c' },
    { id: '4-B4-1', type: 'bed', at: [6, 18], face: 'n', pose: 'lie', room: 'd' },
    { id: '4-B4-2', type: 'bed', at: [6, 18], face: 'n', pose: 'lie', room: 'd' },
    { id: '4-B4-3', type: 'bed', at: [8, 18], face: 'n', pose: 'lie', room: 'd' },
    { id: '4-B4-4', type: 'bed', at: [8, 18], face: 'n', pose: 'lie', room: 'd' },
    { id: '4-B4-5', type: 'bed', at: [10, 18], face: 'n', pose: 'lie', room: 'd' },
    { id: '4-B4-6', type: 'bed', at: [10, 18], face: 'n', pose: 'lie', room: 'd' },
    { id: '4-B5-1', type: 'bed', at: [8, 8], face: 'n', pose: 'lie', room: 'e' },
    { id: '4-B5-2', type: 'bed', at: [8, 8], face: 'n', pose: 'lie', room: 'e' },
    { id: '4-B5-3', type: 'bed', at: [10, 8], face: 'n', pose: 'lie', room: 'e' },
    { id: '4-B5-4', type: 'bed', at: [10, 8], face: 'n', pose: 'lie', room: 'e' },
    { id: '4-B5-5', type: 'bed', at: [12, 8], face: 'n', pose: 'lie', room: 'e' },
    { id: '4-B5-6', type: 'bed', at: [12, 8], face: 'n', pose: 'lie', room: 'e' },
    { id: '4-B6-1', type: 'bed', at: [8, 11], face: 's', pose: 'lie', room: 'f' },
    { id: '4-B6-2', type: 'bed', at: [8, 11], face: 's', pose: 'lie', room: 'f' },
    { id: '4-B6-3', type: 'bed', at: [10, 11], face: 's', pose: 'lie', room: 'f' },
    { id: '4-B6-4', type: 'bed', at: [10, 11], face: 's', pose: 'lie', room: 'f' },
    { id: '4-B6-5', type: 'bed', at: [12, 11], face: 's', pose: 'lie', room: 'f' },
    { id: '4-B6-6', type: 'bed', at: [12, 11], face: 's', pose: 'lie', room: 'f' },
    { id: '4-B7-1', type: 'bed', at: [13, 8], face: 'n', pose: 'lie', room: 'g' },
    { id: '4-B7-2', type: 'bed', at: [13, 8], face: 'n', pose: 'lie', room: 'g' },
    { id: '4-B7-3', type: 'bed', at: [15, 8], face: 'n', pose: 'lie', room: 'g' },
    { id: '4-B7-4', type: 'bed', at: [15, 8], face: 'n', pose: 'lie', room: 'g' },
    { id: '4-B7-5', type: 'bed', at: [17, 8], face: 'n', pose: 'lie', room: 'g' },
    { id: '4-B7-6', type: 'bed', at: [17, 8], face: 'n', pose: 'lie', room: 'g' },
    { id: '4-B8-1', type: 'bed', at: [13, 11], face: 's', pose: 'lie', room: 'h' },
    { id: '4-B8-2', type: 'bed', at: [13, 11], face: 's', pose: 'lie', room: 'h' },
    { id: '4-B8-3', type: 'bed', at: [15, 11], face: 's', pose: 'lie', room: 'h' },
    { id: '4-B8-4', type: 'bed', at: [15, 11], face: 's', pose: 'lie', room: 'h' },
    { id: '4-B8-5', type: 'bed', at: [17, 11], face: 's', pose: 'lie', room: 'h' },
    { id: '4-B8-6', type: 'bed', at: [17, 11], face: 's', pose: 'lie', room: 'h' },
    // 0.38.25 (the user's "junior officers lie crosswise"): a cabin's bed runs north-south with its pillow at the north wall, so
    // the sleeper faces 's' like the bunks (they were 'e', across the bed)
    { id: '4-02', type: 'bed', at: [24, 1], face: 's', pose: 'lie', room: 'A' },
    { id: '4-04', type: 'bed', at: [24, 7], face: 's', pose: 'lie', room: 'B' },
    { id: '4-03', type: 'bed', at: [24, 11], face: 's', pose: 'lie', room: 'C' },
    { id: '4-01', type: 'bed', at: [24, 17], face: 's', pose: 'lie', room: 'D' },
    { id: '4-06', type: 'bed', at: [27, 1], face: 's', pose: 'lie', room: 'E' },
    { id: '4-08', type: 'bed', at: [27, 7], face: 's', pose: 'lie', room: 'F' },
    { id: '4-07', type: 'bed', at: [27, 11], face: 's', pose: 'lie', room: 'G' },
    { id: '4-05', type: 'bed', at: [27, 17], face: 's', pose: 'lie', room: 'H' },
    { id: '4-10', type: 'bed', at: [30, 1], face: 's', pose: 'lie', room: 'I' },
    { id: '4-12', type: 'bed', at: [30, 7], face: 's', pose: 'lie', room: 'J' },
    { id: '4-11', type: 'bed', at: [30, 11], face: 's', pose: 'lie', room: 'K' },
    { id: '4-09', type: 'bed', at: [30, 17], face: 's', pose: 'lie', room: 'L' },
    { id: '4-14', type: 'bed', at: [33, 1], face: 's', pose: 'lie', room: 'M' },
    { id: '4-16', type: 'bed', at: [33, 7], face: 's', pose: 'lie', room: 'N' },
    { id: '4-15', type: 'bed', at: [33, 11], face: 's', pose: 'lie', room: 'O' },
    { id: '4-13', type: 'bed', at: [33, 17], face: 's', pose: 'lie', room: 'P' },
    { id: '4-18', type: 'bed', at: [36, 1], face: 's', pose: 'lie', room: 'Q' },
    { id: '4-20', type: 'bed', at: [36, 7], face: 's', pose: 'lie', room: 'R' },
    { id: '4-19', type: 'bed', at: [36, 11], face: 's', pose: 'lie', room: 'S' },
    { id: '4-17', type: 'bed', at: [36, 17], face: 's', pose: 'lie', room: 'T' },
    { id: '4-22', type: 'bed', at: [39, 1], face: 's', pose: 'lie', room: 'U' },
    { id: '4-24', type: 'bed', at: [39, 7], face: 's', pose: 'lie', room: 'V' },
    { id: '4-23', type: 'bed', at: [39, 11], face: 's', pose: 'lie', room: 'W' },
    { id: '4-21', type: 'bed', at: [39, 17], face: 's', pose: 'lie', room: 'X' },
    { id: '4-01-wash', type: 'shower', at: [26, 19], face: 'w', pose: 'stand', room: 'D' },
    { id: '4-02-wash', type: 'shower', at: [26, 3], face: 'w', pose: 'stand', room: 'A' },
    { id: '4-03-wash', type: 'shower', at: [26, 13], face: 'w', pose: 'stand', room: 'C' },
    { id: '4-04-wash', type: 'shower', at: [26, 9], face: 'w', pose: 'stand', room: 'B' },
    { id: '4-05-wash', type: 'shower', at: [29, 19], face: 'w', pose: 'stand', room: 'H' },
    { id: '4-06-wash', type: 'shower', at: [29, 3], face: 'w', pose: 'stand', room: 'E' },
    { id: '4-07-wash', type: 'shower', at: [29, 13], face: 'w', pose: 'stand', room: 'G' },
    { id: '4-08-wash', type: 'shower', at: [29, 9], face: 'w', pose: 'stand', room: 'F' },
    { id: '4-09-wash', type: 'shower', at: [32, 19], face: 'w', pose: 'stand', room: 'L' },
    { id: '4-10-wash', type: 'shower', at: [32, 3], face: 'w', pose: 'stand', room: 'I' },
    { id: '4-11-wash', type: 'shower', at: [32, 13], face: 'w', pose: 'stand', room: 'K' },
    { id: '4-12-wash', type: 'shower', at: [32, 9], face: 'w', pose: 'stand', room: 'J' },
    { id: '4-13-wash', type: 'shower', at: [35, 19], face: 'w', pose: 'stand', room: 'P' },
    { id: '4-14-wash', type: 'shower', at: [35, 3], face: 'w', pose: 'stand', room: 'M' },
    { id: '4-15-wash', type: 'shower', at: [35, 13], face: 'w', pose: 'stand', room: 'O' },
    { id: '4-16-wash', type: 'shower', at: [35, 9], face: 'w', pose: 'stand', room: 'N' },
    { id: '4-17-wash', type: 'shower', at: [38, 19], face: 'w', pose: 'stand', room: 'T' },
    { id: '4-18-wash', type: 'shower', at: [38, 3], face: 'w', pose: 'stand', room: 'Q' },
    { id: '4-19-wash', type: 'shower', at: [38, 13], face: 'w', pose: 'stand', room: 'S' },
    { id: '4-20-wash', type: 'shower', at: [38, 9], face: 'w', pose: 'stand', room: 'R' },
    { id: '4-21-wash', type: 'shower', at: [41, 19], face: 'w', pose: 'stand', room: 'X' },
    { id: '4-22-wash', type: 'shower', at: [41, 3], face: 'w', pose: 'stand', room: 'U' },
    { id: '4-23-wash', type: 'shower', at: [41, 13], face: 'w', pose: 'stand', room: 'W' },
    { id: '4-24-wash', type: 'shower', at: [41, 9], face: 'w', pose: 'stand', room: 'V' },
    { id: '4-shower-p1', type: 'shower', at: [2, 0], face: 'n', pose: 'stand', room: 'p' },
    { id: '4-shower-p2', type: 'shower', at: [4, 0], face: 'n', pose: 'stand', room: 'p' },
    { id: '4-toilet-p1', type: 'toilet', at: [5, 0], face: 's', pose: 'sit', room: 'p', xy: [5.35, 0.5], y: 0.4 },
    { id: '4-shower-q1', type: 'shower', at: [4, 19], face: 's', pose: 'stand', room: 'q' },
    { id: '4-shower-q2', type: 'shower', at: [5, 19], face: 's', pose: 'stand', room: 'q' },
    { id: '4-toilet-q1', type: 'toilet', at: [2, 19], face: 'n', pose: 'sit', room: 'q', xy: [2.65, 19.5], y: 0.4 },
    // 0.38.35: where people wait for a shower (the social engineer's shower queue), first then second, facing the stalls
    { id: '4-shower-queue-p1', type: 'shower-queue', at: [4, 2], face: 'n', pose: 'stand', room: 'p' },
    { id: '4-shower-queue-p2', type: 'shower-queue', at: [4, 3], face: 'n', pose: 'stand', room: 'p' },
    { id: '4-shower-queue-q1', type: 'shower-queue', at: [3, 18], face: 's', pose: 'stand', room: 'q' },
    { id: '4-shower-queue-q2', type: 'shower-queue', at: [3, 17], face: 's', pose: 'stand', room: 'q' },
    { id: '4-basin-p1', type: 'basin', at: [3, 2], face: 'w', pose: 'stand', room: 'p' },
    { id: '4-basin-p2', type: 'basin', at: [3, 3], face: 'w', pose: 'stand', room: 'p' },
    { id: '4-basin-q1', type: 'basin', at: [4, 16], face: 'e', pose: 'stand', room: 'q' },
    { id: '4-basin-q2', type: 'basin', at: [4, 17], face: 'e', pose: 'stand', room: 'q' },
    { id: '4-laundry-1', type: 'laundry', at: [14, 18], face: 's', pose: 'stand', room: 'l' },
    { id: '4-laundry-2', type: 'laundry', at: [13, 18], face: 's', pose: 'stand', room: 'l' },
    { id: '4-laundry-3', type: 'laundry', at: [12, 18], face: 's', pose: 'stand', room: 'l' },
    { id: '4-laundry-4', type: 'laundry', at: [11, 18], face: 's', pose: 'stand', room: 'l' },
    { id: '4-laundry-5', type: 'laundry', at: [13, 17], face: 'e', pose: 'stand', room: 'l' },
    { id: '4-laundry-6', type: 'laundry', at: [12, 17], face: 'w', pose: 'stand', room: 'l' },
    { id: '4-common-1', type: 'common-room', at: [2, 9], face: 'e', pose: 'sit', room: 'j', window: true, y: 0.52 },
    { id: '4-common-2', type: 'common-room', at: [2, 10], face: 'e', pose: 'sit', room: 'j', window: true, y: 0.52 },
    { id: '4-common-3', type: 'common-room', at: [2, 11], face: 'e', pose: 'sit', room: 'j', window: true, y: 0.52 },
    { id: '4-common-4', type: 'common-room', at: [7, 9], face: 'w', pose: 'sit', room: 'j', xy: [7.41, 9.64], y: 0.44, cush: 0.44 },
    { id: '4-common-5', type: 'common-room', at: [7, 10], face: 'w', pose: 'sit', room: 'j', xy: [7.41, 10.5], y: 0.44, cush: 0.44 },
    { id: '4-common-6', type: 'common-room', at: [5, 8], face: 's', pose: 'sit', room: 'j', xy: [5.5, 7.89], y: 0.44, cush: 0.44 },
    { id: '4-common-7', type: 'common-room', at: [5, 12], face: 'n', pose: 'sit', room: 'j', xy: [5.42, 12.11], y: 0.44, cush: 0.44 },
    // the card-table stools: on the four stool tops round the table (centre 3.15, 7.1), facing it in degrees (0.30.17; 0 south, 90 east)
    { id: '4-common-8', type: 'common-room', at: [3, 6], face: 0, pose: 'sit', room: 'j', xy: [3.15, 6.45], y: 0.49 },
    { id: '4-common-9', type: 'common-room', at: [3, 8], face: 180, pose: 'sit', room: 'j', xy: [3.15, 7.75], y: 0.49 },
    { id: '4-common-10', type: 'common-room', at: [2, 7], face: 90, pose: 'sit', room: 'j', xy: [2.5, 7.1], y: 0.49 },
    { id: '4-common-11', type: 'common-room', at: [4, 7], face: 270, pose: 'sit', room: 'j', xy: [3.8, 7.1], y: 0.49 },
    { id: '4-common-kettle', type: 'common-room', at: [7, 7], face: 'n', pose: 'stand', room: 'j' },
    { id: '4-music-1', type: 'music', anim: 'play', at: [44, 5], face: 'e', pose: 'sit', room: 'n', xy: [44.87, 5.35], y: 0.55, event: 'late-piano' },   // the piano bench (late piano, 0.38.14: the Captain's)
    { id: '4-music-2', type: 'music', at: [45, 7], face: 112.9, pose: 'sit', room: 'n', xy: [45.5, 7.5], y: 0.42, cush: 0.319 },
    { id: '4-music-3', type: 'music', at: [45, 8], face: 95.7, pose: 'sit', room: 'n', xy: [45.5, 8.5], y: 0.42, cush: 0.319 },
    { id: '4-music-4', type: 'music', at: [45, 11], face: 72.8, pose: 'sit', room: 'n', xy: [45.5, 11.5], y: 0.42, cush: 0.319 },
    { id: '4-music-5', type: 'music', at: [46, 11], face: 55.6, pose: 'sit', room: 'n', xy: [46.5, 11.5], y: 0.42, cush: 0.319 },
    { id: '4-music-records', type: 'music', at: [45, 14], face: 's', pose: 'stand', room: 'n' },
    { id: '4-bench-1', type: 'bench', at: [18, 6], face: 'e', pose: 'sit', room: '+', xy: [18.4, 6.5], y: 0.48 },
    { id: '4-bench-2', type: 'bench', at: [18, 7], face: 'e', pose: 'sit', room: '+', xy: [18.4, 7.5], y: 0.48 },
    { id: '4-bench-3', type: 'bench', at: [23, 6], face: 'w', pose: 'sit', room: '+', xy: [23.6, 6.5], y: 0.48 },
    { id: '4-bench-4', type: 'bench', at: [23, 7], face: 'w', pose: 'sit', room: '+', xy: [23.6, 7.5], y: 0.48 },
    { id: '4-lift-1', type: 'lift-wait', at: [18, 8], face: 'e', pose: 'stand', room: '+' },
    { id: '4-lift-2', type: 'lift-wait', at: [18, 10], face: 'e', pose: 'stand', room: '+' },
    { id: '4-lift-3', type: 'lift-wait', at: [23, 8], face: 'w', pose: 'stand', room: '+' },
    { id: '4-lift-4', type: 'lift-wait', at: [23, 10], face: 'w', pose: 'stand', room: '+' },
    // utility rooms (0.30.2): one work:works place on each machine's panel tile, facing the machine
    { id: '4-scrubber-1-svc', machine: '4-scrubber-1', type: 'work:works', at: [21, 2], face: 'n', pose: 'work', room: 's' },
    { id: '4-scrubber-2-svc', machine: '4-scrubber-2', type: 'work:works', at: [23, 2], face: 'n', pose: 'work', room: 's' },
    { id: '4-heater-1-svc', machine: '4-heater-1', type: 'work:works', at: [21, 18], face: 'e', pose: 'work', room: 't' },
    { id: '4-pump-1-svc', machine: '4-pump-1', type: 'work:works', at: [20, 18], face: 'w', pose: 'work', room: 't' },
    { id: '4-pump-2-svc', machine: '4-pump-2', type: 'work:works', at: [20, 19], face: 'w', pose: 'work', room: 't' },
    { id: '4-junction-1-svc', machine: '4-junction-1', type: 'work:works', at: [18, 18], face: 's', pose: 'work', room: 'k' },
    { id: '4-junction-2-svc', machine: '4-junction-2', type: 'work:works', at: [42, 18], face: 's', pose: 'work', room: 'y' },
    { id: '4-washer-1-svc', machine: '4-washer-1', type: 'work:works', at: [14, 18], xy: [14.5, 18.75], face: 's', pose: 'work', room: 'l' },
    { id: '4-washer-2-svc', machine: '4-washer-2', type: 'work:works', at: [13, 18], xy: [13.5, 18.75], face: 's', pose: 'work', room: 'l' },
    { id: '4-washer-3-svc', machine: '4-washer-3', type: 'work:works', at: [12, 18], xy: [12.5, 18.75], face: 's', pose: 'work', room: 'l' },
    { id: '4-washer-4-svc', machine: '4-washer-4', type: 'work:works', at: [11, 18], xy: [11.5, 18.75], face: 's', pose: 'work', room: 'l' },
  ],
  // the officer whose bed is in cabin num ('4-06'), from ROSTER (0.30.12); none for guest and spare cabins
  officer(num) { return /^4-\d\d$/.test(num) && typeof ROSTER !== 'undefined' ? ROSTER.find(p => p.bed === num) || null : null; },
  lockedRoom(r) {
    const num = (this.cabins.find(c => c[0] === r) || [])[1], who = this.officer(num);
    return { t: who ? who.name + ', ' + num : this.rooms[r].name, x: this.guests[r] || (this.spares.includes(r) ? 'Spare. Stripped and empty, ready for whoever comes aboard next.' : who ? who.role.split(',')[0] + '. The cabin\'s locked, and not yours. Yet.' : 'An officer\'s cabin. Locked, and not yours. Yet.') };
  },
  dress(d) {
    // ---- Deck 4, junior wing ----
    const night = [[M.plum, M.plum], [M.slate, M.plum], [M.plum, M.slate]];
    const bunkText = {
      a: ['Tomas has taped a star map to the underside of the top bunk.', 'Your bunk. You lost the coin toss for the bottom one.', 'Lukas\'s bunk, and the empty berth above it: the only spare bed on the ship.'],
      b: ['Pell sleeps on top and talks in his sleep. Mostly about engines.', 'Rina\'s bunk. A stack of medical journals doubles as a pillow.', 'Both berths made up tight, two pairs of boots lined up underneath.'],
      c: ['Someone has hung a tiny paper lantern from the top rail.'],
      d: ['A guitar case under the bottom bunk. Nobody has heard it played.'],
      h: ['Curtain drawn. Someone on the night shift is asleep in there. Tiptoe.', 'Night shift. A sign says DAY SHIFT: PLEASE WHISPER.', 'Blackout blind down. Both berths belong to the night shift.'],
    };
    for (const k of 'abcdefgh') furnish(k, 'bunkRoom', { blankets: k === 'h' ? night : undefined, its: (bunkText[k] || []).map(x => IT('Bunk', x)),
      wardrobe: k === 'a' ? { ...IT('Your wardrobe', 'Your locker by the door, with your name on a strip of tape. Clean clothes on the left, and a hook for the hamper.'), wardrobe: '4-B1-4' } : undefined });   // 0.38.24: your wardrobe (DECKS[4].wardrobes)
    furnish('p', 'washroom'); furnish('q', 'washroom');   // two showers and a toilet each (0.27.45: the user kept the showers)
    wallFixed('=', 'valvePanel', 'n', VALVE_PANELS[4].along, { hitW: 1.5, it: { ...IT('Pipe valves', 'Three valves on the junior wing\'s water line, numbered from upstream. Close the one before a leak.'), valves: 4 } });   // 0.47.0: incidents (m6)
    furnish('l', 'laundry');
    // junior common room (6 x 8): stern windows, a sofa facing them, a Tiles table and a kettle
    place('j', 'rug', 3.3, 4, 'n', { tex: rugLounge, w: 2.6, d: 3.4 });
    place('j', 'windowSeat', .38, 4, 'w', { w: 3.6, it: IT('Window seat', 'The stern view: everywhere the Wren has already been.') });
    place('j', 'sofa', 5.3, 4, 'e', { w: 2.2, fab: M.tealFab, it: IT('Sofa', 'It sags in exactly the right places, and someone has always left a jumper on it.') });
    place('j', 'coffeeTable', 3.3, 4, 'n');
    place('j', 'armchair', 3.3, 2.0, 'n', { fab: M.plum });
    place('j', 'armchair', 3.3, 6.0, 's', { fab: M.mustard });
    place('j', 'cardTable', 1.15, 1.1, 'n', { tiles: true, it: { ...IT('Tiles table', 'A game of Tiles is always about to start. Rina has never lost here.'), tiles: 4 } });   // tiles: DECKS[4].tiles (0.38.24)
    place('j', 'dispenser', 5.5, .38, 'n', { it: IT('Kettle', 'It never fully cools. Chef Brennan refills the biscuit tin when nobody is looking.') });
    place('j', 'bookshelf', 5.3, 7.7, 's', { it: IT('Swap shelf', 'Take a book, leave a book. Mostly thrillers and one very battered star atlas.') });
    place('j', 'plant', .5, 7.5, 's', { big: true });
    place('j', 'floorLamp', 1.3, 7.5, 's', { light: true });
    placeWall('j', 'poster', 'e', 6.9, { tex: makeChartPoster('#1f2b22', '#e9c46a', 'Junior wing chores'), it: IT('Chore rota', 'Whose turn it is to clean the washrooms. Pell has swapped his twice.') });
    placeWall('j', 'sconce', 'e', 1.2);

    // ---- officers' wing: furnished, and locked until you're promoted (SHIP remembers unlocked doors) ----
    const guestKeys = Object.keys(d.guests);
    for (const [k] of d.cabins) furnish(k, 'officerCabin', { locked: roomLocked(k), spare: d.spares.includes(k), guest: d.guests[k] ? guestKeys.indexOf(k) + 1 : 0,
      bed: d.guests[k] ? IT('Guest bed', 'Fresh linen still folded at the foot, and a travel case beside it. Guests rarely unpack all the way.') : d.spares.includes(k) ? IT('Bare bed', 'Stripped to the mattress. Clean linen comes up from the junior stores when someone is due.') : undefined });

    // ---- the music room (6 x 12): a low stage round the bow windows, the piano by the north windows ----
    // Room-local positions; map x = 44 + local x, map z = 4 + local z. The stage hugs the bow, an inset in from the hull.
    {
      const x0 = 47.2, z0 = 7.2, z1 = 12.8, inset = .42, top = .16;
      const arc = HULL_PTS.map(([x, z], k) => [x + HULL_NRM[k].nx * inset * HULL_NRM[k].m, z + HULL_NRM[k].nz * inset * HULL_NRM[k].m])
        .filter(([x, z]) => x > x0 && z > z0 && z < z1);
      const sh = new THREE.Shape(); sh.moveTo(x0 - OX, z0 - OZ); sh.lineTo(arc[0][0] - OX, z0 - OZ);
      for (const [x, z] of arc) sh.lineTo(x - OX, z - OZ);
      sh.lineTo(arc[arc.length - 1][0] - OX, z1 - OZ); sh.lineTo(x0 - OX, z1 - OZ); sh.closePath();
      const geo = new THREE.ExtrudeGeometry(sh, { depth: top, bevelEnabled: false }); geo.rotateX(Math.PI / 2); geo.translate(0, top, 0);
      const stage = new THREE.Mesh(geo, [MUS.stage, M.slateDark]); stage.receiveShadow = true; stage.castShadow = true; staticRoot.add(stage);
      for (let j = 7; j <= 12; j++) for (let i = 46; i <= 49; i++) if (i + .5 > x0 && inHull(i + .5, j + .5)) BLOCKED.add(i + ',' + j);
      const up = gr => { gr.position.y = top; return gr; };
      up(place('n', 'drumKit', 4.45, 6.0, 'e', { it: IT('Drum kit', 'The soundproofing went in the week after the drums came aboard. Nobody calls that a coincidence.') }));
      up(place('n', 'amp', 4.75, 4.1, 'e', { big: true, it: IT('Amp', 'Turned down to two. A note taped to it says ELEVEN IS NOT A NUMBER ON THIS SHIP.') }));
      up(place('n', 'guitarStand', 3.75, 4.0, 'e', { electric: true, it: IT('Electric guitar', 'Red, battered, and signed inside the pickguard by everyone who has ever played it.') }));
      up(place('n', 'micStand', 3.55, 7.0, 'e', { it: IT('Microphone', 'Friday sessions: anyone can play, everyone has to clap. Rina sings once a year and nobody is allowed to film it.') }));
      up(place('n', 'guitarStand', 3.75, 8.0, 'e', { it: IT('Acoustic guitar', 'The ship\'s guitar. It belongs to nobody, which means it belongs to everybody, which means it is never in tune.') }));
      up(place('n', 'amp', 4.7, 8.0, 'e'));
    }
    place('n', 'stageLight', 2.6, 3.5, 'w', { turn: -.5, light: true });
    place('n', 'stageLight', 2.6, 9.5, 'w', { turn: .6 });
    place('n', 'grandPiano', 2.3, 1.1, 'e', { it: IT('Grand piano', 'Lashed to the deck for every jump. Captain Marrow plays it late on Thursdays, and nobody claps until she nods.') });
    place('n', 'pianoBench', .95, 1.1, 'e');                // you stand at the bench to play
    place('n', 'beanbag', 1.5, 3.5, 'w', { turn: .4, fab: MUS.fab[2] });
    place('n', 'beanbag', 1.5, 4.5, 'w', { turn: .1, fab: MUS.fab[0] });
    place('n', 'beanbag', 1.5, 7.5, 'w', { turn: -.3, fab: MUS.fab[1], it: IT('Beanbags', 'The front row. Already dented to fit.') });
    place('n', 'beanbag', 2.5, 7.5, 'w', { turn: -.6, fab: MUS.fab[3] });
    place('n', 'recordCabinet', 1.3, 11.75, 's', { it: IT('Record player', 'Real records, carried aboard one or two at a time. There is a waiting list for the good ones, and Commander Vance keeps it.') });
    for (const a of [1.5, 2.5, 3.5]) placeWall('n', 'acoustic', 'w', a, { k: a * 2 });
    for (const a of [8.5, 9.5, 10.5]) placeWall('n', 'acoustic', 'w', a, { k: a * 2 + 1, it: a === 9.5 ? IT('Soundproofing', 'Fabric panels on every inner wall. The officers\' corridor sleeps through anything now. Mostly.') : undefined });
    placeWall('n', 'instrumentHooks', 's', 1.3, { it: IT('Instrument rail', 'A ukulele, a violin and a tambourine. Borrow anything, bring it back before breakfast.') });
    {
      const gig = tex(200, 280, (g, w, h) => {
        g.fillStyle = '#21182f'; g.fillRect(0, 0, w, h);
        const sun = g.createRadialGradient(100, 120, 4, 100, 120, 90); sun.addColorStop(0, '#f2b45e'); sun.addColorStop(.5, 'rgba(194,59,51,.55)'); sun.addColorStop(1, 'rgba(33,24,47,0)');
        g.fillStyle = sun; g.fillRect(0, 0, w, h);
        g.strokeStyle = '#efe3c8'; g.lineWidth = 3; for (let k = 0; k < 5; k++) { g.beginPath(); g.moveTo(30, 150 + k * 9); g.lineTo(170, 150 + k * 9); g.stroke(); }
        g.fillStyle = '#efe3c8'; g.font = '700 30px system-ui,sans-serif'; g.textAlign = 'center'; g.fillText('FRIDAY', 100, 60); g.fillText('SESSIONS', 100, 94);
        g.fillStyle = '#f2b45e'; g.font = '600 15px system-ui,sans-serif'; g.fillText('20:00, music room', 100, 222);
        g.fillStyle = '#b9a9c9'; g.font = '12px system-ui,sans-serif'; g.fillText('Anyone plays. Everyone claps.', 100, 248);
      });
      placeWall('n', 'poster', 's', 3.3, { tex: gig, it: IT('Gig poster', 'FRIDAY SESSIONS, 20:00. Underneath, in three hands: bring biscuits / not the dry ones / Chef Brennan\'s or nothing.') });
    }

    // ---- the bow-end closets: supplies, seen from above when the walls drop ----
    place('x', 'shelving', .3, 2.3, 'w'); place('x', 'crate', 2.0, 3.35, 's'); place('x', 'crate', 2.8, 3.35, 's');
    place('y', 'shelving', .3, 1.7, 'w'); place('y', 'crate', 2.0, .65, 'n');

    // ---- door plates, corridor lights, the lift ----
    // (0.30.12) an officer's cabin plate carries their name, with the cabin number and rank underneath (ROSTER's plate: { rank, name }; before
    // that's in, their name and role)
    let home = null; try { home = SHIP.works && SHIP.works.home; } catch (e) { home = null; }   // 0.47.11: your own cabin's plate (Step 3: 4-23 once you're an officer)
    for (const [key, tw, text] of d.plates) { if (home && text === 'Spare ' + home) { let nm = 'Cadet'; try { nm = (SHIP.player && SHIP.player.name) || nm; } catch (e) {} placeOnEdge('namePlate', key, tw, { text: nm, sub: home + '  ·  Works Officer' }); continue; } const who = d.officer(text); placeOnEdge(who ? 'namePlate' : 'plate', key, tw, who ? { text: (who.plate || who).name, sub: text + '  ·  ' + (who.plate ? who.plate.rank : who.role.split(',')[0]) } : { text }); }
    for (const [key, tw] of d.sconces) placeOnEdge('sconce', key, tw);
    // more lights wherever a corridor wall is free: at least two tiles apart, never on a door or plate
    {
      const used = new Set([...d.plates.map(p => p[0]), ...d.sconces.map(p => p[0])]);
      for (const [j, tw] of [[4, 's'], [6, 'n'], [14, 's'], [16, 'n']]) {
        let last = -9;
        for (let i = 2; i < 44; i++) {
          const key = `h,${i},${j}`, e = EDGES.get(key), hall = roomAt(i, tw === 's' ? j : j - 1);
          if (used.has(key)) { last = i; continue; }
          if (!e || e.type !== 'wall' || !hall || !ROOMS[hall].hall || i - last < 3) continue;
          placeOnEdge('sconce', key, tw); used.add(key); last = i;
        }
      }
    }
    // notice boards in the lobby, where everyone waits for the lift
    placeOnEdge('notices', 'v,18,8', 'e'); placeOnEdge('notices', 'h,22,4', 's'); placeOnEdge('notices', 'h,22,16', 'n');
    for (const [key, tw] of [['v,20,7', 'w'], ['v,22,7', 'e']]) placeOnEdge('plate', key, tw, { text: 'Lift' });
    for (const [key, tw] of [['v,20,11', 'w'], ['v,22,11', 'e']]) placeOnEdge('liftPanel', key, tw);
    // the spine, behind glass: trunks above the car (two rows now the car has grown), the ladder below it
    for (const r of ['Y', 'Z']) NO_FADE.add(r);
    place('Y', 'spineTrunks', 1, 1.5, 'n', { it: SPINE_IT.trunks });
    place('Y', 'trunkJunction', 1, .6, 'n', { it: { t: 'Trunk junction', x: 'Where Deck 4 takes its air and power off the spine. Two valves, one status box, and a label that says DO NOT in three languages.', see: true } });
    place('Z', 'spineLadder', 1, .5, 'n', { it: SPINE_IT.ladder });
    place('Z', 'harnessRack', 1, 2.3, 'n');
    // the lobbies either side of the lift: somewhere to sit, a plant, a directory
    place('+', 'bench', .3, 3.0, 'w', { snug: true, it: IT('Bench', 'For waiting for the lift, or pretending to while someone finishes in the washroom.') });
    place('+', 'plant', .45, 9.55, 'w', { band: '#5fd6c6' });
    place('+', 'bench', 5.7, 3.0, 'e', { snug: true, it: IT('Bench', 'Officers wait here. They wait more upright than the juniors do.') });
    place('+', 'plant', 5.55, 9.55, 'e', { band: '#c45a3f' });
    placeOnEdge('deckDirectory', 'v,24,8', 'w', { it: IT('Deck directory', 'Seven decks, top to bottom. Bridge, Command & Science, Commons, Quarters, the Recreation Deck (R), Operations, Engineering. You are here: Quarters.') });
    // ---- utility rooms (Pillar 2, 0.30.2). Last in dress() and free of R(), so nothing above them changes ----
    // air scrubbers: two units on the port hull, a duct riser between them, the duct across the ceiling
    for (const [x, n] of [[.5, 1], [2.5, 2]]) place('s', 'utilScrubber', x, 1.0, 'n', { it: IT('Air scrubber ' + n, 'One of the two units that keep Deck 4\'s air clean. The filter drawer is at the front; the screen shows how full it is.') });
    place('s', 'ductRiser', 1.5, .5, 'n');
    place('s', 'ductRun', 1.5, .8, 'n', { w: 2.9 });
    placeWall('s', 'filterRack', 'e', 3.4, { it: IT('Spare filters', 'Scrubber filters, ready to swap. There are always fewer than the list says.') });
    placeWall('s', 'workLight', 's', 2.5);
    // heating plant: the exchanger on the starboard hull, two pumps by the closet wall, an expansion tank, pipes overhead
    place('t', 'heatExchanger', 4.0, 2.5, 'e', { nozzles: [-.25, .75], it: IT('Heat exchanger', 'Deck 4\'s heat: warm water from the plant below, through the tubes, out to every cabin. The gauge reads warm, mostly.') });
    for (const [z, n] of [[2.5, 1], [3.5, 2]]) place('t', 'circPump', .5, z, 'w', { it: IT('Circulation pump ' + n, n === 1 ? 'The duty pump. It hums.' : 'The standby pump. It waits.') });
    place('t', 'expansionTank', 4.5, .5, 'n');
    for (const z of [2.25, 3.25]) place('t', 'pipeLine', 2.25, z, 'n', { w: 3.5, y: 2.5, r: .14 });   // from each pump's riser to the exchanger's nozzle
    placeWall('t', 'workLight', 'n', 3.0);
    // utility closets: the junior wing's breakers at the hull end, its light relays on the wall; the officers' cabinet in y
    place('k', 'breakerCabinet', .5, 3.65, 's', { w: .7, it: IT('Breaker cabinet', 'The junior wing\'s power junction. Every bunk-room light on Deck 4 aft runs through here.') });
    placeWall('k', 'relayBoard', 'w', 2.0, { it: IT('Light relays', 'Twelve relays, twelve little lights. One of them flickers if you stare at it.') });
    place('y', 'breakerCabinet', .5, 3.65, 's', { w: .7, it: IT('Breaker cabinet', 'The officers\' wing power junction, tucked into the narrow end of the closet.') });
    // junior stores: shelves on three sides
    for (const z of [1.5, 2.5, 3.5]) place('u', 'utilShelf', .33, z, 'w');
    for (const x of [1.5, 2.5]) place('u', 'utilShelf', x, 3.67, 's');
    placeWall('u', 'workLight', 'n', 2.5);
    // lived-in touches (0.30.12): a radio left on in the heating plant, a mug on the junior closet's breakers, the scrubber crew's calendar
    place('t', 'radio', .5, 3.5, 'w', { y: .56, turn: .3 });
    place('k', 'mug', .68, 3.6, 's', { y: 1.995, tall: true });
    placeWall('s', 'calendar', 'w', 3.2, { upTo: 16, ring: 20 });
    // Pillar 4 (seat 8, 0.38.9): the keepsake shelf above berth 4's bunk (yours), last so nothing above moves
    placeWall('a', 'keepsakeShelf', 'n', 2.5, { hitW: .9, it: IT('Your shelf', 'A plank above your bunk, just within reach from the top berth. Empty for now. People on the Wren tend to fill theirs.') });
    placeWall('W', 'keepsakeShelf', 'n', .5, { hitW: .9, it: IT('Shelf', 'A plank above the bed, waiting for whoever moves in.') });   // 0.47.11: 4-23, the officer's cabin you move to (Step 3)
  },
};
'abcdefgh'.split('').forEach((k, n) => { DECKS[4].rooms[k] = { name: 'Bunk ' + (n + 1) + (k === 'h' ? ', night shift' : ''), floor: 'plate' }; });
for (const [k, num] of DECKS[4].cabins) DECKS[4].rooms[k] = { name: (DECKS[4].guests[k] ? 'Guest cabin ' : DECKS[4].spares.includes(k) ? 'Spare cabin ' : 'Cabin ') + num, floor: 'warm' };

// the spine's trunks and ladder, the same on every deck
const SPINE_IT = {
  trunks: { t: 'Spine trunks', x: 'The ship\'s main air ducts and power conduits, rising through every deck beside the lift. When something upstream fails, this is where you trace it.', see: true },
  ladder: { t: 'Spine ladder', x: 'The maintenance ladder, all seven decks of it. Works techs use it when the lift is down, or when they\'re in a hurry and feeling brave.', see: true },
};

