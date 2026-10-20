// ---- Big gatherings (Pillar 3, C9, 0.38.0; plans/pillar3-plan.md "Gatherings of more than 70 crew") ----
// The venues where a crowd (an all-clear, a party, a greeting, a festival) can stand, one table per deck:
//   <venue>: { name, focus: [x, z] (tile units: where the crowd looks), rooms (the venue's own room letters),
//     seats (place types in those rooms that count too), also (venues to spill into after these),
//     lead: [[x, z, face], ...] (the front: lead 1 is the speaker, the rest beside them; face in degrees from south toward east),
//     at: 'c,r ...' (the standing spots: the venue's rooms nearest the focus first, then the rooms next door) }
// Doorways, lift doors and every existing place's tile are left clear. At load each spot becomes a place
// { id: '<deck>-<venue>-crowd-<n>' (or -lead-<n>), type: 'event', gather: venue, lead?, at, xy, face (toward the focus), pose: 'stand', room },
// so deck_check checks them like any place. No `event` tag and type 'event': no plan uses them day to day.
// gatherSpots(venue) -> the places in the order to fill them (leads, then nearest first, then the spill rooms and the
// `also` venues), each with its deck. Section 14's gathering() and section 18's meetings read it; nothing else does.
// Ship-wide event venues: 'works-bay' (Calder's storm briefing at the job board), 'observation' (the Captain's
// all-clear), 'bow-lounge' (the party), 'shuttle-bay' (the greeting), and 'mess' and 'plaza' (the big ones).
DECKS[3].gathers = {
  'plaza': { name: 'the lift plaza and promenade', focus: [23.5, 10.5], rooms: '+=', seats: ['bench'], also: [],
    lead: [[23.5, 10.5, 90]],   // on the plaza east of the lift, facing down the promenade
    at: '23,9 23,11 24,9 25,10 23,12 22,8 25,11 22,12 24,12 21,8 21,12 25,12 26,10 26,11 21,7 20,8 26,12 21,13 27,10 27,9 27,11 20,7 21,6 19,8 19,7 19,13 20,14 18,8 18,12 21,15 19,14 18,7 18,13 29,9 17,12 29,12 18,6 18,14 19,15 17,13 16,10 16,9 16,11 18,15 16,12 15,10 31,10 15,11 31,11 31,12 32,10 32,11 32,12 13,10 33,10 33,9 13,11 33,11 35,9 35,12 37,10 37,9 37,11 37,12 38,10 38,11 39,10 39,9 39,11 39,12' },
  'mess': { name: 'the mess hall', focus: [33.5, 8.2], rooms: 'M', seats: ['mess-seat'], also: ['plaza'],
    lead: [[33.5, 8.25, -127]],   // by the servery, facing the tables
    at: '32,6 32,5 30,8 29,8 29,6 28,8 33,2 32,2 27,8 31,2 27,5 33,1 26,6 28,2 33,0 27,2 24,8 23,8 23,6 23,5 24,2 23,2' },
  'bow-lounge': { name: 'the bow lounge', focus: [44.5, 10.5], rooms: 'L', seats: ['lounge-seat'], also: ['plaza'],
    lead: [[44.5, 10.5, 90]],   // the open floor between the bar and the windows
    at: '44,9 43,10 45,10 44,11 43,9 45,9 43,11 45,11 44,8 42,10 46,10 44,12 45,8 42,9 46,9 42,11 46,11 43,12 45,12 42,12 46,12 44,13 47,9 43,13 45,13 47,8 47,12 44,14 48,9 43,14 47,7 47,13 42,6 46,6 48,8 48,12 48,13 47,14 44,15 45,5 42,5 49,8 46,15 41,5 49,7 49,13 44,4 50,10 44,16 45,4 50,9 50,11 43,16 45,16 42,4 50,12 48,5 49,6 49,14 47,4' },
};
DECKS[5].gathers = {
  'shuttle-bay': { name: 'the shuttle bay', focus: [5.5, 11.9], rooms: 'S', seats: [], also: [],
    lead: [[5.0, 12.4, 180], [6.0, 12.4, 180], [5.5, 11.35, 0]],   // the foot of the Tern's ramp (0.38.18: the walk-in Tern's): the Captain (lead 1) and Envoy Saruth, facing the Speaker or whoever arrives (lead 3)
    at: '4,10 4,11 4,12 7,12 3,10 8,10 3,11 8,11 3,9 8,9 5,13 8,8 4,13 2,10 9,10 9,11 2,9 9,9 5,14 6,14 8,7 4,14 7,14 1,10 1,11 1,9 8,6 5,15 6,15 1,8 5,5 6,5 4,15 7,15 4,5 7,5 9,6 1,7 3,5 8,5 1,6 5,4 6,4 2,5 9,5 4,4 7,4 3,4 8,4 1,5 9,4 5,3 6,3 4,3 7,3 3,3 8,3 1,4 2,3 9,3 5,2 6,2 4,2 7,2 1,3 3,2 8,2 2,2 9,2 5,1 6,1 4,1 7,1 1,2 3,1 8,1 2,1 9,1 5,0 6,0 1,1 4,0 7,0 3,0 8,0 2,0 9,0 10,9 11,9 11,8 10,6 11,7 12,8 11,6 12,7 13,9 12,6 13,8 13,7 13,6 14,9 14,8 14,7 14,6 15,8 15,7 16,9 20,8' },
  'works-bay': { name: 'the Works bay', focus: [16.5, 1.6], rooms: 'w', seats: [], also: [],
    lead: [[16.6, 0.7, 0], [17.6, 1.0, -25], [14.4, 0.8, 25]],   // the Chief beside the job board (lead 1), two techs either side
    at: '16,1 16,2 17,2 15,0 17,0 16,3 14,1 18,1 17,3 18,0 16,4 15,4 17,4 13,2 13,0 19,0 14,4 18,4' },
};
DECKS[1].gathers = {
  'observation': { name: 'the observation room', focus: [5.3, 2.5], rooms: 'O', seats: ['common-room', 'lounge-seat'], also: [],
    lead: [[5.3, 2.5, -90], [5.3, 1.5, -110]],   // the Captain by the wall screen, the XO beside her
    at: '4,2 4,1 4,3 3,2 5,4 3,1 3,3 4,0 2,2 2,3 5,7 3,8 5,9 1,8 3,9 2,9 5,10 4,10 3,10 4,11 6,3 7,2 8,2 9,3 6,7 9,7 8,8' },
};
for (const n of Object.keys(DECKS)) for (const [v, g] of Object.entries(DECKS[n].gathers || {})) {
  const d = DECKS[n], P = d.places || (d.places = []), room = (c, r) => d.map[r][c];
  const face = (x, z) => Math.round(Math.atan2(g.focus[0] - x, g.focus[1] - z) * 180 / Math.PI);
  g.lead.forEach(([x, z, f], i) => P.push({ id: `${n}-${v}-lead-${i + 1}`, type: 'event', gather: v, lead: i + 1, at: [Math.floor(x), Math.floor(z)], xy: [x, z], face: f, pose: 'stand', room: room(Math.floor(x), Math.floor(z)) }));
  g.at.split(' ').forEach((s, i) => {
    const [c, r] = s.split(',').map(Number), x = c + .5 + ((c * 37 + r * 11) % 7 - 3) * .04, z = r + .5 + ((c * 13 + r * 29) % 7 - 3) * .04;   // a little off centre, so a crowd doesn't stand in rows
    P.push({ id: `${n}-${v}-crowd-${i + 1}`, type: 'event', gather: v, at: [c, r], xy: [+x.toFixed(2), +z.toFixed(2)], face: face(x, z), pose: 'stand', room: room(c, r) });
  });
}
const GATHER_SPOTS = new Map();
function gatherVenue(v) { for (const n of Object.keys(DECKS)) if ((DECKS[n].gathers || {})[v]) return { deck: +n, ...DECKS[n].gathers[v] }; return null; }
function gatherSpots(v) {
  if (GATHER_SPOTS.has(v)) return GATHER_SPOTS.get(v);
  const g = gatherVenue(v); if (!g) return [];
  const [fx, fz] = g.focus, P = DECKS[g.deck].places, seen = new Set(), out = [];
  const near = l => l.map(p => [Math.hypot((p.xy ? p.xy[0] : p.at[0] + .5) - fx, (p.xy ? p.xy[1] : p.at[1] + .5) - fz), p])
    .sort((a, b) => a[0] - b[0] || (a[1].id < b[1].id ? -1 : 1)).map(e => e[1]);
  const add = l => { for (const p of l) if (!seen.has(p.id)) { seen.add(p.id); out.push({ ...p, deck: g.deck }); } };
  const crowd = P.filter(p => p.gather === v && !p.lead || g.seats.includes(p.type) && g.rooms.includes(p.room) && !p.machine);
  add(P.filter(p => p.gather === v && p.lead).sort((a, b) => a.lead - b.lead));
  add(near(crowd.filter(p => g.rooms.includes(p.room)))); add(near(crowd.filter(p => !g.rooms.includes(p.room))));
  for (const a of g.also) add(near(gatherSpots(a).filter(p => !p.lead)));
  GATHER_SPOTS.set(v, out);
  return out;
}

// ---- Visitable rooms (Pillar 3, C9, 0.38.2; plans/pillar3-plan.md Part 4, "progression hooks") ----
// Rooms the player enters only when invited or summoned: section 14's doorOpenFor (the sim engineer) opens `door` for
// the appointment's window; every other time the door stays as it is. One table per deck:
//   visits: { <id>: { name, room, door, host (the host's place), places: [place ids: the first is yours, then the other guests] } }
// The ready room's guest places are new here (type 'event', visit: id, so nobody uses them day to day); the Captain's
// table uses its own seats: the Captain at the north end, you at the south end. visitSpots(id) -> { deck, name, room,
// door, host: place, places: [place, ...] }, each place with its deck.
DECKS[1].places.push(
  { id: '1-ready-visit-1', type: 'event', visit: 'ready-room', at: [11, 3], xy: [11.5, 3.05], face: 'n', pose: 'stand', room: 'R' },   // in front of the desk: summoned
  { id: '1-ready-visit-2', type: 'event', visit: 'ready-room', at: [10, 3], xy: [10.6, 3.2], face: 'n', pose: 'sit', y: .5, room: 'R' },   // the two chairs by the door
  { id: '1-ready-visit-3', type: 'event', visit: 'ready-room', at: [12, 3], xy: [12.4, 3.2], face: 'n', pose: 'sit', y: .5, room: 'R' },
  { id: '1-ready-visit-4', type: 'event', visit: 'ready-room', at: [10, 2], xy: [10.5, 1.9], face: 'n', pose: 'stand', room: 'R' },      // looking into the Admiral's tank
);
DECKS[1].visits = { 'ready-room': { name: 'the Captain\'s ready room', room: 'R', door: 'h,11,4', host: '1-ready-1', places: ['1-ready-visit-1', '1-ready-visit-2', '1-ready-visit-3', '1-ready-visit-4'] },
  // the conference table (Part 4): a briefing at the observation room's table, whoever presents standing by the wall screen,
  // you at the far end. The room has open glass doors, so there's nothing to unlock (door: null)
  conference: { name: 'the conference table', room: 'O', door: null, host: '1-observation-lead-1', places: ['1-conf-10', '1-conf-1', '1-conf-2', '1-conf-3', '1-conf-4', '1-conf-5', '1-conf-6', '1-conf-7', '1-conf-8', '1-conf-9'] } };
DECKS[2].visits = { 'captain-table': { name: 'the Captain\'s table', room: 'C', door: 'v,7,10', host: '2-captable-5', places: ['2-captable-6', '2-captable-1', '2-captable-2', '2-captable-4', '2-captable-3'] } };
// ---- Pillar 4, seat 8 (0.38.9; plans/pillar4-plan.md, Part 6 and the social plan's interfaces): the arrival evening ----
// keepsakes: the shelf above your bunk (Bunk 1, berth 4's bunk); `slots` are where section 8b's one instanced keepsake mesh
// puts each gift (tile units for x and z, metres for y); `place` is where you stand to look at it (yours: its id starts
// with your bed's). mugRack: the Works tea corner's rack; `yours` is the free hook's mug spot. CALM_TYPES / placeCalm(p):
// where people sit and talk (the social plan's where: ['calm']): seats of those types, unless a place says calm: false.
DECKS[4].places.push({ id: '4-B1-4-keepsake', type: 'event', at: [9, 0], xy: [9.25, .8], face: -127, pose: 'stand', room: 'a' });
DECKS[4].keepsakes = { room: 'a', bed: '4-B1-4', place: '4-B1-4-keepsake', slots: [8.14, 8.28, 8.43, 8.57, 8.72, 8.86].map(x => [x, 2.17, .2]), trophy: [8.79, 2.17, .13] };   // trophy: the Tiles trophy's spot, at the back (0.38.17)
// 0.47.11 (Pillar 5 Step 3, seat A): the places the Step 3 pages ask for. All type `event` (inert: nobody's day plan uses them).
// Team jobs (m8-team-jobs): spots by each machine, `event: 'team-job'`, `works: true` (Works crew and you), `team: <machine id>`;
// spot 1 is the lead's (by the panel or between the machines), the others round the machine. DECKS[n].teamSpots[machine] lists them.
// The office meeting (promotion-officer, the summons): `5-office-visit-1` (you, beside Calder's desk) and `5-office-stand-1`
// (Calder, standing, to hand you the badge); her chair is `5-office-1`. The ceremony (Deck 1's observation room, by the stern
// windows): `1-ceremony-captain`, `1-ceremony-you`, `1-ceremony-guest-1..6` (Vance and Calder first, at your sides), `event: 'ceremony'`.
// Your cabin as an officer (4-23): `4-23-keepsake` and DECKS[4].homeKeepsakes['4-23'] (the shelf above its bed, the same shape as
// DECKS[4].keepsakes, for section 8b when your things move); its door plate shows your name once SHIP.works.home is '4-23'.
{
  const team = (n, room, machine, spots) => {
    (DECKS[n].teamSpots = DECKS[n].teamSpots || {})[machine] = spots.map((_, k) => `${machine.replace(/-\d+$/, '')}-team-${k + 1}`);
    spots.forEach(([c, r, face], k) => DECKS[n].places.push({ id: DECKS[n].teamSpots[machine][k], type: 'event', event: 'team-job', team: machine, works: true, at: [c, r], face, pose: 'stand', anim: 'work', room }));
  };
  team(3, 'R', '3-recycler-1', [[14, 15, 'w'], [14, 17, 'w'], [13, 14, 's'], [15, 15, 'w']]);
  team(4, 'l', '4-washer-1', [[14, 18, 'n'], [12, 18, 'n'], [11, 18, 'n']]);   // all four washers in a row
  team(5, 'n', '5-manifold-1', [[35, 14, 's'], [37, 14, 's'], [36, 13, 's']]);
  team(4, 't', '4-heater-1', [[21, 17, 'e'], [21, 19, 'e'], [20, 17, 'e']]);
  team(4, 's', '4-scrubber-1', [[22, 2, 'n'], [21, 3, 'n'], [23, 3, 'n']]);      // both stacks: spot 1 stands between them
}
DECKS[5].places.push(
  { id: '5-office-visit-1', type: 'event', event: 'office', at: [12, 1], xy: [12.4, 1.35], face: 'w', pose: 'stand', room: 'o' },
  { id: '5-office-stand-1', type: 'event', event: 'office', at: [10, 1], xy: [10.6, 1.35], face: 'e', pose: 'stand', room: 'o' },
);
{
  const fx = 2.95, fz = 2.5, at = (c, r, x, z) => ({ at: [c, r], xy: [x, z], face: Math.round(Math.atan2(fx - x, fz - z) * 180 / Math.PI) });
  DECKS[1].places.push(
    { id: '1-ceremony-captain', type: 'event', event: 'ceremony', at: [2, 2], xy: [2.45, 2.5], face: 'e', pose: 'stand', room: 'O' },
    { id: '1-ceremony-you', type: 'event', event: 'ceremony', at: [3, 2], xy: [3.4, 2.5], face: 'w', pose: 'stand', room: 'O' },
    ...[[3, 1, 3.45, 1.45], [3, 3, 3.45, 3.55], [4, 1, 4.4, 1.6], [4, 3, 4.4, 3.4], [4, 2, 4.5, 2.5], [5, 2, 5.4, 2.5]].map(([c, r, x, z], k) =>
      ({ id: '1-ceremony-guest-' + (k + 1), type: 'event', event: 'ceremony', ...at(c, r, x, z), pose: 'stand', room: 'O' })),
  );
}
DECKS[4].places.push({ id: '4-23-keepsake', type: 'event', at: [40, 10], xy: [40.1, 10.8], face: -139, pose: 'stand', room: 'W' });
DECKS[4].homeKeepsakes = { '4-23': { room: 'W', bed: '4-23', place: '4-23-keepsake', slots: [39.14, 39.28, 39.43, 39.57, 39.72, 39.86].map(x => [x, 2.17, 10.2]), trophy: [39.79, 2.17, 10.13] } };
// 0.53.4 (Pillar 5 Step 4, seat E3: the places turn): the places the Step 4 pages ask for, so the side jobs can rely on them.
// All type `event` with `event: 'side'` (or 'leak'): inert, nobody's day plan uses them; `works: true` on the ones behind a service hatch (you and Works crew).
// M10 workshop: `5-shop-board` (the order board, machine shop north wall), `5-shop-lathe`, `5-shop-fab`. M11 tool upkeep:
// `5-bench-you` (your bench under the Works bay window), `5-tool-rack` (the team's shared tools: the tool wall). M12 logbook:
// `5-works-terminal` (by the Works bay notice board). The stocktake (step4-stages) uses Step 2's `5-stock-1..4` (one per
// storage aisle, in DECKS[5].shelves' order): nothing new.
// M13 leak hunting: `n-leak-1..4` on Decks 3-5 (`event: 'leak'`; DECKS[n].leakJoints lists them in the same order): at
// plumbing in public rooms and corridors (stage 1), except Deck 5's last two, `gallery: true`, behind the Tier 2 hatches in the
// pipe galleries by the two valves (stage 2). Each: `joint` the dripping joint on the wall in front of you ([x, y, z], tiles for
// x and z, metres for y), `wall` its wall, `damp: [x, z, wall]` where the damp patch goes on that wall, `puddle: [x, z]` a floor
// spot 2-3 tiles off in the same room where the drip runs to, with its own place `n-leakp-k` (`puddlePlace`, `event: 'leakp'`).
// M14 irrigation: `3-rack-1..3` in front of the garden's three north grow racks, west first (DECKS[3].growRacks; `rack` is the
// rack's front centre). Off shift: cabin 4-23's four spots `4-23-rug`, `-desk`, `-shelf` (beside the keepsakes), `-ledge` (a
// small wall ledge towards the door, for a plant: there's no window) in DECKS[4].cabinSpots['4-23'] ({ place, at: [x, y, z]
// where a thing would sit }); `2-telescope` at the observatory's brass telescope.
{
  const ev = (id, room, c, r, face, o = {}) => ({ id, type: 'event', event: 'side', at: [c, r], face, pose: 'stand', room, ...o });
  const wallAt = (c, r, face, y = .45) => ({ n: [c + .5, y, r + .08], s: [c + .5, y, r + .92], w: [c + .08, y, r + .5], e: [c + .92, y, r + .5] })[face];
  const leaks = (n, list) => list.forEach(([room, c, r, face, [pc, pr], gallery], k) => {
    const id = `${n}-leak-${k + 1}`, j = wallAt(c, r, face);
    DECKS[n].places.push(ev(id, room, c, r, face, { event: 'leak', anim: 'work', ...(gallery ? { works: true, gallery: true } : {}) }),
      ev(`${n}-leakp-${k + 1}`, room, pc, pr, face, { event: 'leakp', ...(gallery ? { works: true } : {}) }));   // at the puddle, looking towards the joint's wall
    (DECKS[n].leakJoints = DECKS[n].leakJoints || []).push({ place: id, puddlePlace: `${n}-leakp-${k + 1}`, room, wall: face, joint: j, damp: [j[0], j[2], face], puddle: [pc + .5, pr + .5], ...(gallery ? { gallery: true } : {}) });
  });
  DECKS[5].places.push(
    ev('5-shop-board', 'f', 22, 9, 'n', { xy: [22.0, 9.5] }),
    ev('5-shop-lathe', 'f', 22, 12, 'w', { anim: 'work' }),
    ev('5-shop-fab', 'f', 25, 9, 'e', { anim: 'work' }),
    ev('5-bench-you', 'w', 11, 4, 'w', { anim: 'work', xy: [11.25, 4.3] }),
    ev('5-tool-rack', 'w', 18, 1, 'n'),
    ev('5-works-terminal', 'w', 17, 1, 'n', { xy: [17.65, 1.5] }),
  );
  leaks(3, [['w', 17, 19, 'w', [19, 18]], ['K', 35, 3, 'w', [36, 5]], ['G', 2, 12, 'w', [4, 12]], ['=', 23, 9, 'n', [25, 10]]]);   // washrooms, galley, garden, promenade
  leaks(4, [['p', 5, 1, 'e', [3, 1]], ['q', 5, 18, 'e', [3, 18]], ['l', 14, 18, 'e', [12, 17]], ['=', 10, 4, 'n', [12, 5]]]);       // the two washrooms, laundry, junior corridor
  leaks(5, [['q', 21, 4, 'w', [23, 4]], ['=', 27, 8, 's', [25, 7]], ['g', 27, 0, 'n', [30, 0], true], ['h', 30, 15, 's', [32, 15], true]]);   // Works washroom, main corridor; the galleries
  DECKS[3].growRacks = [4.4, 6.4, 8.4].map((x, k) => {
    DECKS[3].places.push(ev('3-rack-' + (k + 1), 'G', Math.floor(x), 1, 'n', { anim: 'work', xy: [x, 1.1] })); return { place: '3-rack-' + (k + 1), rack: [x, .78] };
  });
  DECKS[4].places.push(
    ev('4-23-rug', 'W', 40, 12, 'n', { xy: [40.5, 12.6] }),
    ev('4-23-desk', 'W', 41, 11, 'n', { xy: [41.0, 11.45] }),
    ev('4-23-shelf', 'W', 40, 10, -139, { xy: [40.1, 10.8] }),
    ev('4-23-ledge', 'W', 39, 12, 'w', { xy: [39.6, 12.45] }),
  );
  DECKS[4].cabinSpots = { '4-23': { rug: { place: '4-23-rug', at: [40.5, .01, 12.0] }, desk: { place: '4-23-desk', at: [41.15, .76, 10.45] },
    shelf: { place: '4-23-shelf', at: [40.2, 2.17, 10.2] }, ledge: { place: '4-23-ledge', at: [39.12, 1.15, 12.45] } } };
  DECKS[2].places.push(ev('2-telescope', 'J', 43, 5, 'n', { xy: [43.2, 5.25] }));
}
DECKS[5].mugRack = { room: 't', yours: [21.8, 1.44, 2.83] };
const CALM_TYPES = ['lounge-seat', 'common-room', 'garden', 'bench', 'mess-seat', 'music'];
const placeCalm = p => !!p && (p.calm !== undefined ? !!p.calm : CALM_TYPES.includes(p.type) && p.pose === 'sit' && !p.machine);
// 0.38.10: seedlings: the garden's seedling stand (kit seedlingStand, north-east corner by the grow racks); `pots` are the
// twelve pots' soil tops (x and z in tiles, y in metres), front step first, west to east; `yours` is the empty pot, where
// Sowing morning's trace seedlingYours (DECK_DRESS) plants your seedling; `place` is where you stand to plant and tend it.
// tiles: the bow lounge's Tiles station (kit tilesTable; places `station`, west stool then east) and its board's centre;
// `boards` are Tiles night's boards, one on every lounge table ([x, y (the table top), z, turn, size, seats]: the three booths,
// the two high tables, the coffee table, the two tea tables), drawn by DECK_DRESS.tilesNight. tilesSeats(k) -> board k's
// seats, at least two each, the two who play first (k = 'station' for the station's own two). The board kit is TILES_KIT
// (section 23, the Tiles game, owns the name TILES).
// The new places are type 'event' with an event tag ('sowing', 'tiles'), so nobody uses them day to day (crew plans unchanged).
DECKS[3].places.push(
  { id: '3-seedlings-1', type: 'event', event: 'sowing', at: [11, 1], xy: [11.6, 1.2], face: 'n', pose: 'stand', anim: 'water', room: 'G' },   // in front of the stand
  { id: '3-tiles-1', type: 'event', event: 'tiles', at: [43, 18], xy: [43.9, 18.5], face: 'e', pose: 'sit', anim: 'talk', y: .49, calm: true, room: 'L' },   // the station's stools
  { id: '3-tiles-2', type: 'event', event: 'tiles', at: [45, 18], xy: [45.1, 18.5], face: 'w', pose: 'sit', anim: 'talk', y: .49, calm: true, room: 'L' },
);
// 0.38.11: twelve lantern places on the promenade's two outer lanes (Lantern walk: crew stand under the lanterns, facing
// the middle), event-tagged like the rest. (The postbox and its place went with Letters evening: 0.62.0, 0.62.5.)
DECKS[3].places.push(
  ...[26, 28, 30, 32, 34, 36, 38].map(c => [c, 9]).concat([28, 30, 34, 36, 38].map(c => [c, 12])).map(([c, r], k) =>
    ({ id: '3-lantern-' + (k + 1), type: 'event', event: 'lantern-walk', at: [c, r], xy: [c + .5, r === 9 ? 9.45 : 12.55], face: r === 9 ? 's' : 'n', pose: 'stand', anim: 'talk', room: '=' })),
);
// 0.38.14: places for the monthly traditions, tagged with their ids: open lab (Deck 2's Survey lab, round the island and
// at the benches) and bridge hour (Deck 1, behind the stations, facing the viewscreen). Standing, type 'event'. (Rummage
// day's were taken out in 0.38.16: the user cut it.)
{
  const at = (deck, ev, room, list, fx, fz) => list.forEach(([c, r, f], k) => DECKS[deck].places.push({ id: `${deck}-${ev}-${k + 1}`, type: 'event', event: ev, at: [c, r], xy: [c + .5, r + .5],
    face: f !== undefined ? f : Math.round(Math.atan2(fx - c - .5, fz - r - .5) * 180 / Math.PI), pose: 'stand', anim: 'talk', room }));
  at(2, 'open-lab', 'L', [[36, 3], [36, 5], [34, 3], [34, 5], [33, 4], [38, 5], [34, 1, 'n'], [38, 2, 'n']], 36, 4.5);
  at(1, 'bridge-hour', 'B', [[15, 2], [16, 2], [17, 2], [18, 2], [15, 9], [16, 9], [17, 9], [18, 9], [17, 3], [17, 8]], 21.5, 6);
}
// 0.38.18: the walk-in Tern (plans/shuttle-plan.md). DECKS[5].tern: the tiles it blocks (`block`), its aisle and the
// door's well (walkable inside), the ramp's tiles and its foot, and where a new game can start you (`start`: in the aisle,
// facing the door). ternRamp(open, secs) opens (true) or closes (false) the ramp over secs seconds (default 2.5; it
// snaps when you're on another deck). It won't close while anyone is on the ramp or in the well: it returns false, and
// a close already moving waits. ternRampOpen() -> 0 (closed) to 1 (open); while it's less than half open the door's well
// is blocked. The ramp isn't saved: every load starts it open, as the Tern always was. ternInside() -> true while you're
// in the aisle or the well: then, or while the Tern fades because you're behind it (both only where you stand), its roof
// and upper hull hide. ternClear() -> true when nobody stands in the well or on the ramp (for closing it behind you).
DECKS[5].tern = { block: [[2, 6], [2, 7], [2, 8], [3, 6], [4, 6], [5, 6], [6, 6], [7, 6], [7, 7], [3, 8], [4, 8], [6, 8], [7, 8]],
  aisle: [[3, 7], [4, 7], [5, 7], [6, 7]], well: [5, 8], ramp: [[5, 9], [5, 10]], foot: [5, 11], start: { tile: [5, 7], face: 0 } };
DECKS[5].places.push(
  { id: '5-tern-seat-1', type: 'event', event: 'tern', at: [4, 8], xy: [4.5, 8.55], walk: [4, 7], face: 'n', pose: 'sit', y: .5, room: 'S' },   // the bench by the door
  { id: '5-tern-aisle-1', type: 'event', event: 'tern', at: [5, 7], xy: [5.5, 7.5], face: 's', pose: 'stand', room: 'S' },               // inside, facing the door
  { id: '5-tern-ramp-top', type: 'event', event: 'tern', at: [5, 9], xy: [5.5, 9.35], face: 's', pose: 'stand', room: 'S' },            // the top of the ramp (the bag step)
  { id: '5-tern-ramp-foot', type: 'event', event: 'tern', at: [5, 11], xy: [5.5, 11.3], face: 'n', pose: 'stand', room: 'S' },          // where the escort waits
);
const TERN = { open: 1, target: 1, secs: 2.5, roof: null, hinge: null, root: null };
function ternRamp(open, secs = 2.5) {                  // -> false (and nothing changes) when asked to close with someone on the ramp or in the door's well
  if (!open && !ternClear()) return false;
  TERN.target = open ? 1 : 0; TERN.secs = Math.max(.1, secs); if (!TERN.root || TERN.root !== deckRoot || !deckDef || deckDef.num !== 5) TERN.open = TERN.target;
  return true;
}
const ternRampOpen = () => TERN.open;
const ternAt = () => { if (typeof player === 'undefined' || !player || !player.obj) return null; const p = player.obj.position; return [Math.floor(p.x + OX), Math.floor(p.z + OZ)]; };
function ternInside() { const t = DECKS[5].tern, c = ternAt(); return !!c && deckDef && deckDef.num === 5 && (t.aisle.concat([t.well])).some(([i, j]) => i === c[0] && j === c[1]); }
function ternClear() {
  const t = DECKS[5].tern, tiles = new Set([t.well].concat(t.ramp).map(c => c.join(',')));
  const on = (x, z) => tiles.has(Math.floor(x + OX) + ',' + Math.floor(z + OZ));
  if (typeof walkers !== 'undefined' && walkers.some(w => w && w.active && w.obj && on(w.obj.position.x, w.obj.position.z))) return false;   // you (and any old walker)
  return !(typeof DECK_CREW !== 'undefined' && deckDef && deckDef.num === 5 && DECK_CREW.some(a => a && isFinite(a.x) && on(a.x, a.z)));   // the scheduled crew and the escort (0.38.21)
}
const ternRoof = R => { TERN.roof = R; };
function ternHinge(P) {                                  // the kit hands over the ramp's hinge: snap to where it should be, then animate it once a frame
  TERN.hinge = P; TERN.root = deckRoot; TERN.open = TERN.target;
  const well = DECKS[5].tern.well.join(','), pose = () => { const k = TERN.open, e = k * k * (3 - 2 * k); P.rotation.z = -1.62 * e; if (k < .5) BLOCKED.add(well); else BLOCKED.delete(well); };   // the well shuts once it's half closed, so nobody gets caught in it
  pose();
  MOVERS.push({ place: null, tick(dt) {
    if (TERN.open !== TERN.target && (TERN.target > TERN.open || ternClear())) { const d = dt / TERN.secs; TERN.open = TERN.target > TERN.open ? Math.min(1, TERN.open + d) : Math.max(0, TERN.open - d); pose(); }   // closing waits while anyone steps on it
    const t = TALL_BY_ROOM.S; if (TERN.roof) TERN.roof.visible = !(ternInside() || (t && t.o < 1));
  } });
}
// 0.38.20: extra seats for the Sunday table and the harvest supper (the mess seats 44, so 48 with these): a chair at
// each end of the four long tables. 4 places `3-longtable-1..4`, type 'event' with event: 'long-table': they're there every
// day but nobody uses them unless a tradition's where: names them; DECK_DRESS.longTables and .harvestTables draw the chairs
// while the tradition is on (MESS_EXTRA lists the furniture, room-local to the mess hall). 0.62.0 (the user's "just don't
// do it"): the promenade trestle (0.38.23) is gone; extra seats only ever appear inside the mess, and diners past them
// eat an ordinary dinner later.
const MESS_EXTRA = { heads: [[.42, 1.0, 1], [.42, 4.0, 1], [9.58, 1.0, -1], [9.58, 4.0, -1]] };   // heads: [x, z, the way they face (+1 east)]
DECKS[3].places.push(...[[23.42, 1.0, 90], [23.42, 4.0, 90], [32.58, 1.0, -90], [32.58, 4.0, -90]].map(([x, z, f], k) =>
  ({ id: '3-longtable-' + (k + 1), type: 'event', event: 'long-table', at: [Math.floor(x), Math.floor(z)], xy: [x, z], face: f, pose: 'sit', y: .47, room: 'M' })));
DECKS[3].seedlings = { room: 'G', place: '3-seedlings-1', yours: 1, pots: [0, 1, 2].flatMap(t => [0, 1, 2, 3].map(k => [+(11.405 + k * .15).toFixed(3), +(.386 + t * .24).toFixed(3), +(.59 - t * .17).toFixed(2)])) };
DECKS[3].tiles = { room: 'L', station: ['3-tiles-1', '3-tiles-2'], board: [44.5, .722, 18.5],
  boards: [[42.25, .765, 14.52, 0, .26, [16, 14, 15, 13]], [42.25, .765, 16.52, 0, .26, [20, 18, 19, 17]], [42.25, .765, 18.52, 0, .26, [24, 22, 23, 21]],
    [45.7, 1.08, 2.84, 0, .26, [10, 9]], [44.587, 1.08, 1.93, .8, .26, [12, 11]],
    [49.4, .405, 10.895, 0, .26, [26, 28, 29]], [47.6, .445, 6.27, 0, .24, [31, 30]], [47.6, .445, 16.27, 0, .24, [32, 33]]].map(b => (b[5] = b[5].map(n => '3-lounge-' + n), b)) };
function tilesSeats(k) {
  const T3 = DECKS[3].tiles;
  if (k === 'j') return DECKS[4].tiles.station.slice();   // the junior common room's Tiles table (0.38.24)
  return k === 'station' ? T3.station.slice() : T3.boards[k] ? T3.boards[k][5].slice() : [];
}
// 0.38.24 (0.60.7, deck architect 4; DEV_NOTES "Places for 0.60.7"): the new places' data. All inert until a seat uses them:
// the bar's staff and order spots are new types nobody's pool reads, your wardrobe's place is owned by your bed.
// bar: the bow lounge bar. staff: behind the counter (the middle, then by the galley door), facing the stools; order: standing
// between two stools at the counter, facing it. The bar's tap item has bar: true.
DECKS[3].places.push(
  { id: '3-bar-1', type: 'bar-staff', at: [42, 5], xy: [42.45, 5.6], face: 90, pose: 'stand', anim: 'work', room: 'L' },
  { id: '3-bar-2', type: 'bar-staff', at: [41, 6], xy: [41.55, 6.45], face: 70, pose: 'stand', anim: 'work', room: 'L' },
  { id: '3-bar-order-1', type: 'bar-order', at: [44, 5], xy: [44.2, 5.6], face: -90, pose: 'stand', room: 'L' },
  { id: '3-bar-order-2', type: 'bar-order', at: [43, 3], xy: [43.45, 3.55], face: -50, pose: 'stand', room: 'L' },
);
DECKS[3].bar = { room: 'L', staff: ['3-bar-1', '3-bar-2'], order: ['3-bar-order-1', '3-bar-order-2'] };
// wardrobes: bed -> its wardrobe (the locker by the door in Bunk 1 for yours; its item has wardrobe: <bed>) and where you
// stand to use it, facing it
DECKS[4].places.push({ id: '4-B1-4-wardrobe', type: 'event', at: [7, 3], xy: [7.15, 3.25], face: 'w', pose: 'stand', room: 'a' });
DECKS[4].wardrobes = { '4-B1-4': { room: 'a', place: '4-B1-4-wardrobe' } };
// tiles on Deck 4: the junior common room's card table is a Tiles table (its item has tiles: 4). The four stools stay
// everyday seats (type common-room); station is the pair facing across the table, seats all four
DECKS[4].tiles = { room: 'j', station: ['4-common-8', '4-common-9'], seats: ['4-common-8', '4-common-9', '4-common-10', '4-common-11'], board: [3.15, .746, 7.1] };   // board: its centre, on the felt (0.38.34)
// shelves: main storage's four shelves on Deck 5 (place: where you stand to take a part, group: the shelving's fade group;
// every shelving piece of a shelf has shelf: <id>). shelfItems(id) -> that shelf's tap items on the deck you're on ([] elsewhere)
DECKS[5].shelves = [{ id: 'lights', name: 'Lights', place: '5-parts-1', group: 'r:Lights' }, { id: 'filters', name: 'Filters', place: '5-parts-2', group: 'r:Filters' },
  { id: 'plumbing', name: 'Plumbing', place: '5-parts-3', group: 'r:Plumbing' }, { id: 'galley', name: 'Galley parts', place: '5-parts-4', group: 'r:Galley parts' }];
// delivery (0.38.29; 0.38.35 the systems engineer's shape): the Wednesday crates in the cargo hold's clear floor, slots [x, z, y,
// turn] (deck tiles, floor ones first), the tiles they block while out, and where you (or a storekeeper) stand to load them.
// As Deck 5 is built, deliveryCratesBuild() makes one group per slot (one textured box, its own mesh, hidden) and hands each to
// section 17's holdCratesLive(group, k) (k = 1..4), which shows the first holdCrates() of them. Once a frame (MOVERS) the
// shown ones block their tiles and the stack's one tap ('Wednesday delivery', delivery: true) is there while any is shown
DECKS[5].delivery = { room: 'c', place: '5-delivery-1', slots: [[16.25, 12.9, 0, .04], [16.97, 12.92, 0, -.05], [16.3, 12.88, .5, -.08], [16.93, 12.9, .5, .1]], block: [[16, 12], [17, 12]] };
DECKS[5].places.push({ id: '5-delivery-1', type: 'event', event: 'delivery', at: [15, 12], xy: [15.55, 12.9], face: 90, pose: 'stand', anim: 'lift', room: 'c' });
// the beam (0.38.30, Name on the beam): the Works bay's cross beam along the top of its hull wall, painted with names: the
// Works crew aboard (the roster) and some who served before (BEAM.past). WALL_KIT.nameBeam draws it (a canvas, no R(); 2 draw
// calls); your own name, freshly painted at its west end (BEAM.yours, along the wall from the room's west edge), is DECK_DRESS.nameYours,
// shown by the trace { id: 'nameYours', day }. 5-beam-1: where you paint (under the west end, facing it); 5-beam-2..8: the
// Works crew watching, facing the same spot. All type 'event', event 'name-beam'.
const BEAM = { room: 'w', along: 7.0, len: 7.8, y: 2.42, yours: 3.6,   // the bay's hull wall runs from along 3 (the Chief's office) to 11
  past: ['Ada', 'Lars', 'Mireille', 'Tom', 'Celine', 'Ivar', 'Juno', 'Kemi', 'Petra', 'Luis', 'Harpreet', 'Gil', 'Rosa', 'Mateo', 'Yuki', 'Otto'],   // 0.47.6 (playtest): first names, all of them
  // 0.47.6 (playtest): the west end (the first 2.5 m, 650 of the canvas's 2048 px) is kept for the four newest, a 2 x 2 grid: slot 0 is
  // yours (DECK_DRESS.nameYours), slots 1-3 the Works hands who join later (DECK_DRESS.nameNew, the traces { id: 'nameNew', day, name })
  slots: [[3.72, .085], [4.98, .085], [3.72, -.085], [4.98, -.085]], clear: 650 };
const firstName = n => String(n || '').trim().split(/\s+/)[0] || 'Cadet';
Object.assign(WALL_KIT, {
  nameBeam(g) {
    const names = BEAM.past.slice(0, 8).concat((typeof ROSTER === 'undefined' ? [] : ROSTER.filter(p => !p.player && p.dept === 'works').slice(0, 14).map(p => firstName(p.name))), BEAM.past.slice(8)), C = ['#f4efe2', '#e8c06a', '#7fd6c8', '#f0a37a'];
    const t = tex(2048, 128, (c, w, h) => {
      c.fillStyle = '#3a4248'; c.fillRect(0, 0, w, h);
      c.fillStyle = 'rgba(0,0,0,.18)'; for (let x = 0; x < w; x += 196) c.fillRect(x, 0, 3, h);   // the plate seams
      let x = BEAM.clear, row = 0;                       // the west end is left clear for the newest names (yours, and later hands')
      names.forEach((n, k) => {
        c.font = (k % 3 ? 'italic 600 ' : '700 ') + (row ? 40 : 42) + 'px Georgia,serif'; const tw = c.measureText(n).width;
        if (x + tw > w - 20) { row++; x = BEAM.clear + (row % 2) * 60; }
        if (row > 1) return;
        c.fillStyle = C[k % 4]; c.fillText(n, x, row ? 108 : 52); x += tw + 36 + (k * 7) % 23;
      });
    });
    const p = new THREE.Mesh(new THREE.PlaneGeometry(BEAM.len, .34), new THREE.MeshBasicMaterial({ map: t })); p.position.set(0, BEAM.y, .126); g.add(p);
    box(BEAM.len, .34, .04, WM.paintDark, 0, BEAM.y, .1, g);                                   // the web, the names on its face
    for (const dy of [-.19, .19]) box(BEAM.len + .02, .04, .22, WM.steel, 0, BEAM.y + dy, .11, g);   // the flanges
  },
});
DECKS[5].places.push(
  { id: '5-beam-1', type: 'event', event: 'name-beam', at: [13, 0], xy: [13.6, .75], face: 180, pose: 'stand', anim: 'work', room: 'w' },
  ...[[14, 1], [15, 1], [16, 1], [17, 1], [13, 2], [12, 3], [13, 3]].map(([c, r], k) => ({ id: '5-beam-' + (k + 2), type: 'event', event: 'name-beam', at: [c, r], xy: [c + .5, r + .5],
    face: Math.round(Math.atan2(13.6 - c - .5, .75 - r - .5) * 180 / Math.PI), pose: 'stand', anim: 'talk', room: 'w' })),
);
// 0.47.6 (playtest): Sunrise stretch moves to the garden: 3-stretchg-1 is the leader's, on the east side facing the group; 3-stretchg-2..8
// stand in two loose rows across the open floor between the beds (rows 7-9), facing the leader. Type 'event', event 'stretch-garden' (its own tag, so they stay unused until the traditions
// engineer points Sunrise stretch at them: the tradition fills its spots from every place tagged 'sunrise-stretch', the old 3-stretch-*)
DECKS[3].places.push(
  { id: '3-stretchg-1', type: 'event', event: 'stretch-garden', at: [11, 8], xy: [11.35, 8.5], face: 'w', pose: 'stand', anim: 'stretch', room: 'G' },
  ...[[9, 7], [8, 7], [7, 7], [8, 8], [9, 9], [8, 9], [7, 9]].map(([c, r], k) => ({ id: '3-stretchg-' + (k + 2), type: 'event', event: 'stretch-garden', at: [c, r],
    xy: [c + .5 + (r === 8 ? .2 : 0), r + .5], face: Math.round(Math.atan2(11.35 - c - .5, 8.5 - r - .5) * 180 / Math.PI), pose: 'stand', anim: 'stretch', room: 'G' })),
);
// 0.38.31: the spice shelf (Spice shelf supper): a plank on the mess hall's galley wall over the drinks station, its jars
// drawn by DECK_DRESS.spiceJars (SPICES.slots: x along the shelf, up to 12). The postcard box and a writing ledge (Postcard
// night) in the call-home booths' room: places 3-postcard-1..3 at the ledge (standing, writing), 3-postcard-4 at the box.
const SPICES = { room: 'M', wall: 'e', along: 1.0, y: 1.62, slots: [-.55, -.45, -.35, -.25, -.15, -.05, .05, .15, .25, .35, .45, .55] };
const POSTCARDS = { room: 'B', box: ['e', 5.0], ledge: ['w', 5.6] };
Object.assign(WALL_KIT, {
  spiceShelf(g) {                                        // a plank on two brackets, and a painted label under it
    box(1.3, .03, .16, M.wood, 0, SPICES.y, .08, g);
    for (const x of [-.5, .5]) box(.03, .14, .12, M.slateDark, x, SPICES.y - .085, .06, g);
    const t = tex(256, 32, (c, w, h) => { c.fillStyle = '#5a3b26'; c.fillRect(0, 0, w, h); c.fillStyle = '#f2e3c4'; c.font = '600 20px Georgia,serif'; c.textAlign = 'center'; c.fillText('Spices from home', w / 2, 23); });
    const p = new THREE.Mesh(new THREE.PlaneGeometry(.6, .075), new THREE.MeshBasicMaterial({ map: t })); p.position.set(0, SPICES.y - .07, .162); g.add(p);
    box(.62, .085, .02, M.slateDark, 0, SPICES.y - .07, .15, g);
  },
  postcardBox(g) {                                       // a red post box on the wall, a slot and a little collection plate
    box(.36, .5, .2, std('#b83a2e', .5), 0, 1.15, .1, g);
    box(.38, .04, .22, std('#8c2a21', .5), 0, 1.42, .11, g);
    box(.22, .025, .02, M.slateDark, 0, 1.28, .205, g);                             // the slot
    const t = tex(128, 64, (c, w, h) => { c.fillStyle = '#f2e3c4'; c.fillRect(0, 0, w, h); c.fillStyle = '#8c2a21'; c.font = '700 18px system-ui,sans-serif'; c.textAlign = 'center'; c.fillText('POST', w / 2, 26); c.font = '500 13px system-ui,sans-serif'; c.fillText('next mail run', w / 2, 48); });
    const p = new THREE.Mesh(new THREE.PlaneGeometry(.2, .1), new THREE.MeshBasicMaterial({ map: t })); p.position.set(0, 1.08, .202); g.add(p);
  },
  writingLedge(g) {                                      // a narrow ledge to write on, a pot of pens and a stack of blank cards
    box(1.8, .04, .26, M.wood, 0, 1.0, .13, g);
    for (const x of [-.8, .8]) box(.04, .2, .2, M.slateDark, x, .88, .1, g);
    cyl(.04, .035, .1, std('#2a9d8f', .6), -.6, 1.07, .12, g, 10);
    for (const x of [-.63, -.59, -.57]) box(.008, .14, .008, M.slateDark, x, 1.12, .12, g);
    for (let k = 0; k < 4; k++) box(.15, .006, .1, std('#f4efe2', .8), .5 + k * .002, 1.024 + k * .006, .13, g);
  },
});
DECKS[3].places.push(
  ...[17, 18, 19].map((r, k) => ({ id: '3-postcard-' + (k + 1), type: 'event', event: 'postcard-night', at: [36, r], xy: [36.55, r + .5], face: -90, pose: 'stand', anim: 'work', room: 'B' })),
  { id: '3-postcard-4', type: 'event', event: 'postcard-night', at: [40, 18], xy: [40.45, 18.0], face: 90, pose: 'stand', room: 'B' },
);
// 0.38.32: the new traditions' places on Deck 3, all type 'event' (inert): Lap of the Wren (3-lap-1..12, the promenade loop in
// walking order: east along the mess side, back west along the gym side, round the lift plaza; each faces the next), Sunrise
// stretch (3-stretch-1..8 on the promenade's outer lanes, facing the glass, anim 'stretch') and Cook-along (3-cookalong-1..6 in
// the mess, two rows back from the servery line, facing the pass; it's during dinner, so not on the line's own tiles)
{
  const lap = [[23, 10], [27, 9], [31, 9], [34, 9], [38, 9], [40, 10], [38, 12], [34, 12], [31, 12], [27, 12], [23, 11], [22, 10]];
  const deg = (dx, dz) => Math.round(Math.atan2(dx, dz) * 180 / Math.PI);
  DECKS[3].places.push(
    ...lap.map(([c, r], k) => { const [nc, nr] = lap[(k + 1) % lap.length]; return { id: '3-lap-' + (k + 1), type: 'event', event: 'lap-of-the-wren', at: [c, r], xy: [c + .5, r + .5], face: deg(nc - c, nr - r), pose: 'stand', anim: 'talk', room: roomOfTile(3, c, r) }; }),
    ...[[24, 9], [25, 9], [33, 9], [39, 9], [25, 12], [27, 12], [33, 12], [39, 12]].map(([c, r], k) => ({ id: '3-stretch-' + (k + 1), type: 'event', event: 'stretch-promenade', at: [c, r], xy: [c + .5, r === 9 ? 9.4 : 12.6], face: r === 9 ? 'n' : 's', pose: 'stand', anim: 'stretch', room: '=' })),
    ...[[32, 2], [32, 3], [32, 5], [32, 6], [33, 2], [33, 7]].map(([c, r], k) => ({ id: '3-cookalong-' + (k + 1), type: 'event', event: 'cook-along', at: [c, r], xy: [c + .5, r + .5], face: 90, pose: 'stand', anim: 'talk', room: 'M' })),
  );
}
function roomOfTile(n, i, j) { return (DECKS[n].map[j] || '')[i]; }
const DELIVERY_MAT = new THREE.MeshStandardMaterial({ roughness: .8, map: tex(128, 128, (c, w, h) => {   // made at load, no R()
  c.fillStyle = '#4f6f86'; c.fillRect(0, 0, w, h); c.fillStyle = '#2f3f4c'; c.fillRect(18, 0, 10, h); c.fillRect(w - 28, 0, 10, h);   // the straps
  c.fillStyle = '#e07a3c'; c.fillRect(42, 0, w - 84, 22); c.fillStyle = 'rgba(0,0,0,.25)'; c.fillRect(0, h - 4, w, 4); }) });   // the orange band
function deliveryCratesBuild() {
  const D = DECKS[5].delivery, groups = [], tiles = D.block.map(([i, j]) => i + ',' + j), mine = new Set();
  D.slots.forEach(([x, z, y, tn], k) => {
    const grp = new THREE.Group(); grp.position.set(X0(0) + x, y, Z0(0) + z); grp.rotation.y = tn; grp.visible = false; deckRoot.add(grp);
    const m = new THREE.Mesh(new THREE.BoxGeometry(.66, .5, .52), DELIVERY_MAT); m.position.y = .25; m.castShadow = m.receiveShadow = true; m.userData.noMerge = true; grp.add(m);
    groups.push(grp); if (typeof holdCratesLive === 'function') holdCratesLive(grp, k + 1);
  });
  const cx = X0(0) + (D.slots[0][0] + D.slots[1][0]) / 2, cz = Z0(0) + (D.slots[0][1] + D.slots[1][1]) / 2;
  const hit = new THREE.Mesh(new THREE.BoxGeometry(1.4, 1.0, .6), HIT_MAT); hit.userData.noMerge = true; hit.position.set(cx, -10, cz); deckRoot.add(hit);
  const item = { t: 'Wednesday delivery', x: '', hit, g: hit, front: 0, depth: .6, wall: false, delivery: true }; hit.userData.item = item; ITEMS.push(item);
  let shown = -1;
  MOVERS.push({ place: null, tick() {
    const n = groups.filter(q => q.visible).length; if (n === shown) return; shown = n;
    hit.position.y = n ? .5 : -10;
    item.x = n + (n === 1 ? ' crate' : ' crates') + ' up from the supply run, still sealed, orange bands on. They go to main storage by hover cart.';
    for (const t of tiles) { if (n && !BLOCKED.has(t)) { BLOCKED.add(t); mine.add(t); } else if (!n && mine.has(t)) { BLOCKED.delete(t); mine.delete(t); } }
  } });
  return groups;
}
// ---- Pillar 5 Steps 1-2, seat A (deck architect 4, 0.47.0; DEV_NOTES "Places for Pillar 5 Steps 1-2") ----
// All type 'event' with an event tag, so nobody's plans change. Wall kit made per deck build, no R(); colours through std().
// drill (m3, Deck 5): the extinguisher bracket by the Works bay's west door (its extinguisher hides while you carry one:
// drillExtShow(false)), the hatch to the utility closet, the bulkhead wheel by the east door, the closet's breaker cabinet,
// and six muster spots facing the job board
DECKS[5].places.push(
  { id: '5-drill-ext', type: 'event', event: 'drill', at: [15, 5], xy: [15.5, 5.45], face: 's', pose: 'stand', room: 'w' },
  { id: '5-drill-hatch', type: 'event', event: 'drill', at: [19, 9], xy: [19.5, 9.4], face: 's', pose: 'stand', room: '+' },
  { id: '5-drill-door', type: 'event', event: 'drill', at: [18, 5], xy: [18.5, 5.45], face: 's', pose: 'stand', anim: 'work', room: 'w' },
  { id: '5-drill-breaker', type: 'event', event: 'drill', works: true, at: [19, 11], xy: [19.6, 11.35], face: 'e', pose: 'stand', anim: 'work', room: 'u' },
  ...[14, 15, 16, 17, 18, 19].map((c, k) => ({ id: '5-muster-' + (k + 1), type: 'event', event: 'drill', at: [c, 4], xy: [c + .5, 4.5], face: 'n', pose: 'stand', room: 'w' })),
);
DECKS[5].drill = { ext: '5-drill-ext', hatch: '5-drill-hatch', door: '5-drill-door', breaker: '5-drill-breaker', muster: [1, 2, 3, 4, 5, 6].map(k => '5-muster-' + k) };
// inspection (m3, Deck 4): where the duty officer stands in each bunk room, just inside its door, facing the bunks
DECKS[4].inspect = {};
for (const [r, c, j, f] of [['a', 8, 3, 'n'], ['b', 13, 3, 'n'], ['c', 17, 3, 'n'], ['d', 8, 16, 's'], ['e', 10, 6, 's'], ['f', 10, 13, 'n'], ['g', 15, 6, 's'], ['h', 15, 13, 'n']]) {
  DECKS[4].places.push({ id: '4-inspect-' + r, type: 'event', event: 'inspection', at: [c, j], xy: [c + .5, j + .5], face: f, pose: 'stand', room: r });
  DECKS[4].inspect[r] = '4-inspect-' + r;
}
// hauling (m4): a drop spot just inside each stop's door, with room for the cart beside you; the stocktake's spots, one in front
// of each storage shelf (the order of DECKS[5].shelves: Lights, Filters, Plumbing, Galley parts), beside the 5-parts-N spots
const HAUL_DROPS = { laundry: '4-laundry-drop', infirmary: '3-infirmary-drop', store: '3-store-drop', galley: '3-galley-drop', bridge: '1-bridge-drop' };
DECKS[4].places.push({ id: '4-laundry-drop', type: 'event', event: 'haul', at: [12, 17], xy: [12.5, 17.5], face: 'n', pose: 'stand', room: 'l' });
DECKS[3].places.push(
  { id: '3-infirmary-drop', type: 'event', event: 'haul', at: [19, 5], xy: [19.5, 5.5], face: 'n', pose: 'stand', room: 'I' },
  { id: '3-store-drop', type: 'event', event: 'haul', at: [33, 14], xy: [33.5, 14.5], face: 's', pose: 'stand', room: 'S' },
  { id: '3-galley-drop', type: 'event', event: 'haul', at: [37, 8], xy: [37.5, 8.5], face: 'n', pose: 'stand', room: 'K' },
);
DECKS[1].places.push({ id: '1-bridge-drop', type: 'event', event: 'haul', at: [11, 6], xy: [11.5, 6.5], face: 'e', pose: 'stand', room: 'B' });
DECKS[5].places.push(...[[26, 4], [28, 3], [30, 3], [32, 5]].map(([c, r], k) => ({ id: '5-stock-' + (k + 1), type: 'event', event: 'stocktake', at: [c, r], xy: [c + .5, r + .5], face: 'e', pose: 'stand', anim: 'browse', room: 'r' })));
// incidents (m6). A burst pipe on Decks 3, 4, 5: each corridor has a pipe panel (wall kit valvePanel: three wheels on a pipe,
// tap item valves: n) with n-valve-panel in front of it and n-valve-1..3 at the wheels; the water runs from valve 1 to 3 and on
// down the corridor (DECKS[n].valveLine, upstream first), and n-wet-1..2 are the puddle spots downstream. The lift's brake
// (wall kit liftBrake, item brake: true) is in Deck 5's utility closet by the ladder; the galley's extractor alarm and the vent
// switch (wall kit alarmPanel, items alarm: true and vent: true) are on the galley's west wall by the staff door
// works: true on a place behind a service hatch (the utility closet's breaker and brake): reached by Works crew and you, as Works
const VALVE_PANELS = { 3: { room: '=', wall: 'n', along: 3.8, tiles: [15, 15, 16], row: 9, wet: [[16, 10], [15, 11]] },
  4: { room: '=', wall: 'n', along: 4.0, tiles: [5, 6, 6], row: 4, wet: [[10, 5], [11, 5]] },
  5: { room: '=', wall: 'n', along: 9.0, tiles: [29, 30, 30], row: 7, wet: [[32, 8], [33, 7]] } };
for (const n of [3, 4, 5]) {
  const V = VALVE_PANELS[n], x0 = Math.min(...DECKS[n].map.map(r => r.indexOf(V.room)).filter(i => i >= 0)) + V.along;   // the panel's centre on the deck (tile units)
  DECKS[n].places.push({ id: n + '-valve-panel', type: 'event', event: 'incident', at: [Math.floor(x0), V.row], xy: [x0, V.row + .45], face: 'n', pose: 'stand', room: V.room },
    ...[-.6, 0, .6].map((dx, k) => ({ id: n + '-valve-' + (k + 1), type: 'event', event: 'incident', at: [V.tiles[k], V.row], xy: [+(x0 + dx).toFixed(2), V.row + .4], face: 'n', pose: 'stand', anim: 'work', room: V.room })),
    ...V.wet.map(([c, r], k) => ({ id: n + '-wet-' + (k + 1), type: 'event', event: 'incident', at: [c, r], xy: [c + .5, r + .5], face: 'n', pose: 'stand', room: V.room })));
  DECKS[n].valveLine = [1, 2, 3].map(k => n + '-valve-' + k); DECKS[n].wet = [1, 2].map(k => n + '-wet-' + k);
}
DECKS[5].places.push({ id: '5-lift-brake', type: 'event', event: 'incident', works: true, at: [19, 10], xy: [19.4, 10.5], face: 'w', pose: 'stand', anim: 'work', room: 'u' });
DECKS[3].places.push(
  { id: '3-extractor-alarm', type: 'event', event: 'incident', at: [35, 7], xy: [35.45, 7.3], face: 'w', pose: 'stand', anim: 'work', room: 'K' },
  { id: '3-vent-1', type: 'event', event: 'incident', at: [35, 7], xy: [35.45, 7.75], face: 'w', pose: 'stand', anim: 'work', room: 'K' },
);
const DRILL_EXT = { m: null };
const drillExtShow = on => { if (DRILL_EXT.m) DRILL_EXT.m.visible = !!on; };   // the bracket's extinguisher, while you (or nobody) carry one
// the kits (0.47.2, the lead: at most +2 draw calls a deck): built into the deck's merged static geometry by wallFixed(), in
// materials the decks already draw (WM, M), no painted labels, so they add almost nothing. Only the bracket's extinguisher is
// its own mesh (it hides while carried). Unlike placeWall's pieces they don't lower with their wall
function wallFixed(rk, kind, wall, along, o = {}) {
  const b = ROOM_BOX[rk], g = new THREE.Group();
  if (wall === 'n') g.position.set(X0(b.i0) + along, 0, Z0(b.j0) + T / 2);
  if (wall === 's') g.position.set(X0(b.i0) + along, 0, Z0(b.j1 + 1) - T / 2);
  if (wall === 'w') g.position.set(X0(b.i0) + T / 2, 0, Z0(b.j0) + along);
  if (wall === 'e') g.position.set(X0(b.i1 + 1) - T / 2, 0, Z0(b.j0) + along);
  g.rotation.y = FACING[wall]; staticRoot.add(g);
  WALL_KIT[kind](g, o);
  if (o.it) {
    const hit = new THREE.Mesh(new THREE.BoxGeometry(o.hitW || .9, 1.2, .3), HIT_MAT); hit.position.set(0, 1.25, .15); hit.userData.noMerge = true; g.add(hit);
    ITEMS.push({ ...o.it, hit, g, front: FACING[wall], depth: .1, wall: true });
  }
  return g;
}
Object.assign(WALL_KIT, {                               // each stands on the floor against its wall, so it reads as furniture when the wall is lowered
  ductDamper(g, o = {}) {                                // 0.47.3: a square duct section out of the wall on two legs, its flap lever, a plate with o.n red ticks
    for (const x of [-.3, .3]) box(.06, 1.62, .06, M.slateDark, x, .81, .32, g);
    box(.6, .6, .5, UT.duct, 0, 1.92, .25, g); box(.68, .68, .04, WM.steel, 0, 1.92, .51, g);   // the duct and its flange (proud of the duct's face)
    cyl(.03, .03, .1, WM.steel, .38, 1.92, .3, g, 8).rotation.z = Math.PI / 2; box(.04, .34, .04, WM.red, .45, 1.8, .3, g).rotation.z = .35;   // the flap's spindle and lever
    box(.66, .05, .05, M.slateDark, 0, 1.45, .32, g); box(.34, .12, .015, WM.steel, 0, 1.45, .353, g);   // a crossbar and its plate, standing off it
    for (let t = 0; t < (o.n || 1); t++) box(.025, .08, .012, WM.red, (t - ((o.n || 1) - 1) / 2) * .045, 1.45, .364, g);
  },
  extBracket(g) {                                        // an extinguisher stand: a post with a red sign, the extinguisher in its bracket
    box(.06, 1.42, .06, M.slateDark, 0, .71, .05, g); box(.3, .03, .2, M.slateDark, 0, .015, .1, g);
    box(.22, .04, .14, M.slateDark, 0, .62, .12, g); box(.24, .12, .02, WM.red, 0, 1.32, .09, g);
    const e = cyl(.075, .075, .46, WM.red, 0, .87, .15, g, 14); e.userData.noMerge = true; DRILL_EXT.m = e;
  },
  bulkheadWheel(g) {                                     // the bulkhead door's dogging wheel on a pedestal by the door
    box(.12, 1.0, .12, M.slateDark, 0, .5, .08, g); box(.34, .03, .24, M.slateDark, 0, .015, .1, g);
    box(.44, .44, .06, M.slateDark, 0, 1.15, .06, g);
    const w = new THREE.Mesh(new THREE.TorusGeometry(.17, .025, 8, 20), WM.red); w.position.set(0, 1.15, .16); g.add(w);
    box(.34, .03, .03, WM.red, 0, 1.15, .16, g); box(.03, .34, .03, WM.red, 0, 1.15, .16, g);
  },
  valvePanel(g) {                                        // a valve rack: a pipe on two legs with three valve wheels; red ticks count 1, 2, 3 from upstream
    for (const x of [-.82, .82]) box(.06, 1.3, .06, M.slateDark, x, .65, .1, g);
    const pipe = cyl(.05, .05, 1.76, WM.steel, 0, 1.25, .1, g, 10); pipe.rotation.z = Math.PI / 2;
    box(1.5, .2, .03, M.slateDark, 0, 1.47, .05, g);
    [-.6, 0, .6].forEach((x, k) => {
      cyl(.035, .035, .12, WM.steel, x, 1.25, .17, g, 8).rotation.x = Math.PI / 2;
      const w = new THREE.Mesh(new THREE.TorusGeometry(.09, .018, 6, 16), WM.red); w.position.set(x, 1.25, .24); g.add(w);
      for (let t = 0; t <= k; t++) box(.025, .08, .012, WM.red, x + (t - k / 2) * .045, 1.47, .071, g);   // 6 mm proud of the strip (.065)
    });
  },
  liftBrake(g) {                                         // the lift's manual brake release: a cabinet from the floor and a big wheel
    box(.5, 1.3, .3, M.slateDark, 0, .65, .15, g);
    const w = new THREE.Mesh(new THREE.TorusGeometry(.22, .03, 8, 22), WM.red); w.position.set(0, 1.0, .36); g.add(w);
    box(.44, .03, .03, WM.red, 0, 1.0, .36, g); cyl(.05, .05, .1, WM.steel, 0, 1.0, .33, g, 10).rotation.x = Math.PI / 2;
  },
  alarmPanel(g) {                                        // the extractor's alarm (a red lamp, a reset key) and the vent switch, on a post
    box(.06, 1.2, .06, M.slateDark, 0, .6, .05, g); box(.3, .03, .2, M.slateDark, 0, .015, .1, g);
    box(.7, .36, .05, M.slateDark, 0, 1.35, .07, g);
    cyl(.05, .05, .04, WM.red, -.22, 1.45, .11, g, 12).rotation.x = Math.PI / 2; box(.08, .05, .03, WM.steel, -.22, 1.28, .105, g);
    box(.04, .14, .05, WM.red, .23, 1.3, .115, g);       // the vent switch's lever
  },
});
function shelfIt(name, x) { const sh = DECKS[5].shelves.find(q => q.name === name); return { ...IT(name, x), shelf: sh ? sh.id : undefined }; }
const shelfItems = id => (deckDef && deckDef.num === 5 ? ITEMS.filter(it => it.shelf === id) : []);
function visitSpots(id) {
  for (const n of Object.keys(DECKS)) {
    const v = (DECKS[n].visits || {})[id]; if (!v) continue;
    const pl = pid => { const p = DECKS[n].places.find(q => q.id === pid); return p ? { ...p, deck: +n } : null; };
    return { deck: +n, name: v.name, room: v.room, door: v.door, host: pl(v.host), places: v.places.map(pl).filter(Boolean) };
  }
  return null;
}

// ---- Event dressing and traces (Pillar 3, C9, 0.38.1; plans/pillar3-plan.md "How outcomes are scored", "How you learn") ----
// Props that appear only while an event asks for them: sign-up sheets on the mess and Works boards, the storm crew's
// signed roster in the Works tea corner, a scorch mark and a taped panel in Deck 1's relay room, the bow lounge party.
//   DECK_DRESS[id] = { deck, what, make(g, o) -> the tap item { t, x, at: [x, y, z], w, h, d, front, more?, block? } }
//                    (more: extra floor taps with the same text; block: [[i, j], ...] deck tiles blocked while it's out)
//   dressShow(list)  section 18 calls it (once a ship minute is plenty, like eventsDecor): list = ids, or { id, title,
//                    lines } to write on a sheet or banner. Only the current deck's are drawn; it does nothing when the
//                    list hasn't changed, and puts them back after a deck change. Never called: nothing shows (inert).
//   dressingOn()     -> the ids drawn now
// No R(); every colour through col(); no shadows; each one merged to a few draw calls (the party: 5); not in the
// collision grid; wall pieces lower with their wall, like placeWall's. Ids follow section 18's trace names.
const DRESS = { root: null, key: '', on: new Map() }, DRESS_MATS = {};
const dressMat = c => DRESS_MATS[c] || (DRESS_MATS[c] = new THREE.MeshStandardMaterial({ color: col(c), roughness: .8 }));
// a group on a room's wall (room-local `along`, as placeWall) or floor (room-local x, z); y up, local +z into the room
function dressAt(g, room, wall, a, b = 0) {
  const r = ROOM_BOX[room], s = new THREE.Group(); let key = null;
  if (wall === 'floor') s.position.set(X0(r.i0) + a, 0, Z0(r.j0) + b);
  else {
    if (wall === 'n') { s.position.set(X0(r.i0) + a, 0, Z0(r.j0) + T / 2); key = `h,${r.i0 + Math.floor(a)},${r.j0}`; }
    if (wall === 's') { s.position.set(X0(r.i0) + a, 0, Z0(r.j1 + 1) - T / 2); key = `h,${r.i0 + Math.floor(a)},${r.j1 + 1}`; }
    if (wall === 'w') { s.position.set(X0(r.i0) + T / 2, 0, Z0(r.j0) + a); key = `v,${r.i0},${r.j0 + Math.floor(a)}`; }
    if (wall === 'e') { s.position.set(X0(r.i1 + 1) - T / 2, 0, Z0(r.j0) + a); key = `v,${r.i1 + 1},${r.j0 + Math.floor(a)}`; }
    s.rotation.y = FACING[wall];
  }
  s.userData.edge = key && EDGES.get(key); g.add(s); return s;
}
const dressBox = (s, w, h, d, c, x, y, z) => { const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), dressMat(c)); m.position.set(x, y, z); s.add(m); return m; };
// a sheet of paper pinned to a wall: a heading, a title and numbered lines (names written in), on a canvas
function dressSheet(s, o, z, y) {
  const lines = o.lines || [], t = tex(256, 330, (c, w, h) => {
    c.fillStyle = '#f4efe2'; c.fillRect(0, 0, w, h);
    c.fillStyle = '#c45a3f'; c.font = '700 22px system-ui,sans-serif'; c.fillText(o.head || 'SIGN UP', 16, 34);
    c.fillStyle = '#2b2b2b'; c.font = '600 15px system-ui,sans-serif';
    String(o.title || 'Volunteers wanted').split('\n').slice(0, 2).forEach((l, k) => c.fillText(l, 16, 60 + k * 19));
    for (let k = 0; k < 8; k++) {
      const y0 = 112 + k * 26; c.fillStyle = '#9aa7b0'; c.fillRect(34, y0 + 4, w - 52, 1);
      c.fillStyle = '#6b7780'; c.font = '500 13px system-ui,sans-serif'; c.fillText((k + 1) + '.', 14, y0);
      if (lines[k]) { c.fillStyle = '#1f3c6e'; c.font = 'italic 500 16px Georgia,serif'; c.fillText(lines[k], 38, y0); }
    }
  });
  const p = new THREE.Mesh(new THREE.PlaneGeometry(.32, .42), new THREE.MeshBasicMaterial({ map: t, toneMapped: false })); p.position.set(0, y, z + .014); s.add(p);
  dressBox(s, .34, .44, .012, '#d8d0bd', 0, y, z);                  // the backing, .008 behind the paper
  dressBox(s, .03, .03, .02, '#c45a3f', 0, y + .18, z + .016);       // the pin, through the paper
}
const dressNames = (dept, n) => typeof ROSTER === 'undefined' ? [] : ROSTER.filter(p => !p.player && (!dept || p.dept === dept)).slice(0, n).map(p => p.name.split(' ').slice(-1)[0]);
const MESS_LONG = [[2.6, 1.0], [7.4, 1.0], [2.6, 4.0], [7.4, 4.0]];   // the mess hall's long tables (room-local), their tops at .77
// the extra seats' furniture (0.38.20), one wood colour, so one more draw call: a chair at each long table's end (drawn
// in the mess's room-local frame; the promenade trestle went in 0.62.0)
function messExtra(s) {
  const W = '#7a5a3e';
  for (const [x, z, f] of MESS_EXTRA.heads) { dressBox(s, .42, .05, .42, W, x, .45, z); dressBox(s, .06, .5, .42, W, x - f * .19, .72, z); for (const dx of [-.17, .17]) for (const dz of [-.17, .17]) dressBox(s, .04, .43, .04, W, x + dx, .215, z + dz); }
}
const DECK_DRESS = {
  signupMess: { deck: 3, what: 'a sign-up sheet beside the mess menu board', make(g, o) {
    dressSheet(dressAt(g, 'M', 'e', 2.55), o, .016, 1.75);
    return { t: 'Sign-up sheet', x: (o.title || 'Volunteers wanted').replace(/\n/g, ', ') + '. ' + ((o.lines || []).length ? (o.lines || []).length + ' names so far.' : 'Nobody has signed yet.'), wall: ['M', 'e', 2.55], y: 1.75 };
  } },
  signupWorks: { deck: 5, what: 'a sign-up sheet pinned to the corner of the Works job board', make(g, o) {
    dressSheet(dressAt(g, 'w', 'n', 6.65), o, .088, 1.12);           // in front of the board's screen (.075)
    return { t: 'Sign-up sheet', x: (o.title || 'Volunteers wanted').replace(/\n/g, ', ') + '. ' + ((o.lines || []).length ? (o.lines || []).length + ' names so far.' : 'Nobody has signed yet.'), wall: ['w', 'n', 6.65], y: 1.12 };
  } },
  stormRosterTeaCorner: { deck: 5, what: 'the storm crew\'s signed duty roster, framed by the tea', make(g, o) {
    const s = dressAt(g, 't', 'e', 1.6), names = o.lines || dressNames('works', 8);
    dressBox(s, .52, .64, .03, '#5a3b26', 0, 1.5, .015);             // the frame
    const t = tex(256, 320, (c, w, h) => {
      c.fillStyle = '#f2ecdc'; c.fillRect(0, 0, w, h);
      c.fillStyle = '#2b2b2b'; c.font = '700 17px system-ui,sans-serif'; c.fillText(o.head || 'STORM DUTY ROSTER', 16, 30);
      c.fillStyle = '#6b7780'; c.font = '500 12px system-ui,sans-serif'; c.fillText(o.title || 'Works, through the ion storm', 16, 50);
      names.slice(0, 9).forEach((n, k) => { c.fillStyle = '#1f3c6e'; c.font = 'italic 500 16px Georgia,serif'; c.fillText(n, 22 + (k % 2) * 112, 84 + Math.floor(k / 2) * 34);
        c.strokeStyle = '#3f8f5a'; c.lineWidth = 2; c.beginPath(); const x = 14 + (k % 2) * 112, y = 80 + Math.floor(k / 2) * 34; c.moveTo(x - 6, y - 4); c.lineTo(x - 2, y); c.lineTo(x + 4, y - 9); c.stroke(); });
      c.fillStyle = '#c45a3f'; c.font = 'italic 600 15px Georgia,serif'; c.fillText('Thank you all. M. Calder', 16, h - 22);
    });
    const p = new THREE.Mesh(new THREE.PlaneGeometry(.44, .56), new THREE.MeshBasicMaterial({ map: t, toneMapped: false })); p.position.set(0, 1.5, .036); s.add(p);
    return { t: 'Storm duty roster', x: 'Everyone who worked the ion storm signed it, and the Chief framed it by the tea. Someone has drawn a little lightning bolt next to her name.', wall: ['t', 'e', 1.6], y: 1.5 };
  } },
  relayScorch: { deck: 1, what: 'a scorch mark on the relay room floor, where a relay arced in the storm', make(g) {
    const s = dressAt(g, 'u', 'floor', 1.9, 1.45);                  // the walkway between the banks
    [[.72, .5, '#5a3c26', .012], [.5, .36, '#2a211b', .018], [.28, .2, '#100d0b', .024]].forEach(([rx, rz, c, y], k) => {
      const m = new THREE.Mesh(new THREE.CircleGeometry(1, 14), dressMat(c)); m.rotation.x = -Math.PI / 2; m.scale.set(rx, rz, 1); m.position.set(k * .05, y, -k * .03); s.add(m); });
    return { t: 'Scorch mark', x: 'A black scorch across the deck plates, where a relay arced in the ion storm. Nobody has managed to scrub it out, and the Works crew have stopped trying.', floor: ['u', 1.9, 1.45] };
  } },
  tapedPanel: { deck: 1, what: 'an access panel in the relay room, taped shut after the storm', make(g) {
    const s = dressAt(g, 'u', 'w', 1.5);                            // under the calendar, between the two relay banks
    dressBox(s, .62, .52, .03, '#6f7a80', 0, .55, .015);             // the panel (face at .03)
    dressBox(s, .78, .07, .006, '#e8c06a', 0, .55, .039).rotation.z = .62;   // hazard tape, crossed: the strips .005 apart
    dressBox(s, .78, .07, .006, '#e8c06a', 0, .55, .05).rotation.z = -.62;
    dressBox(s, .16, .11, .004, '#f4efe2', .18, .38, .062);         // a note
    return { t: 'Taped panel', x: 'An access panel taped shut with hazard tape. The note says DO NOT OPEN: WAITING ON PARTS. The ion storm cooked whatever is behind it.', wall: ['u', 'w', 1.5], y: .55 };
  } },
  veyliCordSculpture: { deck: 3, what: 'the Veyli delegation\'s gift: a cord sculpture hung on the bow lounge wall between the booths', make(g) {
    const s = dressAt(g, 'L', 'w', 17.6), C = ['#c45a3f', '#e8c06a', '#2a9d8f'];   // the diplomatic visit's trace (section 18, when it goes smoothly)
    dressBox(s, .05, .05, .16, '#c9a24a', 0, 2.3, .08);                // a bracket off the wall
    const ring = new THREE.Mesh(new THREE.TorusGeometry(.3, .022, 8, 28), dressMat('#c9a24a')); ring.position.set(0, 2.0, .18); s.add(ring);   // the brass ring, upright
    dressBox(s, .012, .14, .012, '#c9a24a', 0, 2.37, .18);             // and the cord it hangs by
    for (let k = 0; k < 9; k++) {                                         // nine knotted cords from the ring's lower half, longest in the middle
      const a = Math.PI * (1.12 + k * .095), x = Math.cos(a) * .3, y = 2.0 + Math.sin(a) * .3, len = .45 + .4 * Math.sin(Math.PI * (k + .5) / 9), z = .15 + (k % 3) * .03;
      const c = new THREE.Mesh(new THREE.CylinderGeometry(.008, .008, len, 5), dressMat(C[k % 3])); c.position.set(x, y - len / 2, z); s.add(c);
      for (const f of [.45, 1]) { const b = new THREE.Mesh(new THREE.SphereGeometry(f === 1 ? .03 : .02, 8, 6), dressMat(C[(k + 1) % 3])); b.position.set(x, y - len * f, z); s.add(b); }
    }
    return { t: 'Veyli cord sculpture', x: 'A gift from the Veyli delegation: knotted cords in three colours, hung from a brass ring. Envoy Saruth says each knot is a promise, and that it would be rude to count them.', wall: ['L', 'w', 17.6], y: 1.9, w: .7, h: 1.0 };
  } },
  // Pillar 4, seat 8 (0.38.10). seedlingYours: a lasting trace from your first Sowing morning (SHIP.traces gets
  // { id: 'seedlingYours', day }: the day you planted it). It grows by how long ago that was, looked at whenever Deck 3 is built.
  seedlingYours: { deck: 3, what: 'your seedling in the garden\'s seedling stand, with your name on a stake', make(g, o) {
    const S3 = DECKS[3].seedlings, r = ROOM_BOX.G, [px, py, pz] = S3.pots[S3.yours], x = px - r.i0, z = pz - r.j0, s = dressAt(g, 'G', 'floor', 0, 0);
    const today = typeof shipNow === 'function' ? Math.floor(shipNow() / 1440) + 1 : 1, age = Math.max(0, today - (o.day || today));
    const st = age < 7 ? 0 : age < 28 ? 1 : age < 91 ? 2 : 3, h = [.03, .07, .13, .22][st], n = [2, 4, 6, 8][st], k = [.6, .85, 1.1, 1.4][st];
    const stem = new THREE.Mesh(new THREE.CylinderGeometry(.004 * k, .005 * k, h, 5), dressMat('#4c8a57')); stem.position.set(x, py + h / 2, z); s.add(stem);
    for (let i = 0; i < n; i++) {                        // leaves in pairs up the stem, each pair turned a quarter
      const a = i * Math.PI / 2 + (i % 2) * Math.PI, y = py + h * (.35 + .65 * Math.floor(i / 2) / Math.max(1, n / 2 - 1)), l = new THREE.Mesh(new THREE.SphereGeometry(1, 6, 4), dressMat(i % 2 ? '#6ba86a' : '#4c8a57'));
      l.scale.set(.022 * k, .009 * k, .012 * k); l.rotation.y = a; l.position.set(x + Math.cos(a) * .02 * k, Math.min(y, py + h), z - Math.sin(a) * .02 * k); s.add(l);
    }
    dressBox(s, .006, .12, .006, '#a07a4f', x + .03, py + .04, z + .028);       // the stake, pushed into the soil
    dressBox(s, .05, .028, .005, '#f4efe2', x + .03, py + .1, z + .034);        // and its tag, your name on it
    const say = ['Two leaves, barely up. You check on it more often than it needs.', 'Four true leaves now, leaning toward the grow lights like everything else in here.',
      'A proper little plant. Someone waters it on the days you forget.', 'It has outgrown its pot twice, and the gardeners keep finding it a bigger one.'][st];
    return { t: 'Your seedling', x: 'Planted on your first Sowing morning, your name on the stake. ' + say, floor: ['G', x, z], y: py + .08, w: .2, h: .25, d: .2 };
  } },
  // tilesNight: Tuesday's Tiles night (section 18 lists it while the night is on): a board on every lounge table, one
  // InstancedMesh (one draw call, no shadow), from DECKS[3].tiles.boards
  tilesNight: { deck: 3, what: 'Tiles night: a Tiles board on every table in the bow lounge', make(g) {
    const B = DECKS[3].tiles.boards, r = ROOM_BOX.L, s = dressAt(g, 'L', 'floor', 0, 0), m = new THREE.Matrix4(), q = new THREE.Quaternion(), up = new THREE.Vector3(0, 1, 0);
    const mat = new THREE.MeshStandardMaterial({ map: TILES_KIT.tex.clone(), roughness: .7 }); mat.map.needsUpdate = true;   // its own copies, which dressHide disposes
    const im = new THREE.InstancedMesh(tilesBoardGeo(), mat, B.length); im.userData.noMerge = true; im.frustumCulled = false;
    B.forEach(([x, y, z, turn, w], k) => im.setMatrixAt(k, m.compose(new THREE.Vector3(x - r.i0, y + .002, z - r.j0), q.setFromAxisAngle(up, turn), new THREE.Vector3(w, 1, w))));
    s.add(im);
    const tap = ([x, y, z]) => ({ floor: ['L', x - r.i0, z - r.j0], y: y + .05, w: .3, h: .1, d: .3 });   // a tap on every board ('Tiles board': section 23 seats you there)
    return { t: 'Tiles board', x: 'Tiles night: a board on every table, and a game going on most of them. Rina is defending her title, and saying so.', ...tap(B[5]), more: B.filter((b, k) => k !== 5).map(tap) };
  } },
  // 0.38.14. mugYours: a lasting trace from your new hand's tea ({ id: 'mugYours', day } in SHIP.traces): your own mug on
  // the free hook of the Works tea corner's rack (DECKS[5].mugRack). On the rack's wall, so it lowers with it. 1 draw call.
  mugYours: { deck: 5, what: 'your own mug on the Works tea corner\'s rack', make(g) {
    const s = dressAt(g, 't', 's', 1.1), m = dressMat('#3d6fa8'), x = .3;   // the sixth hook, as in the mugRack kit
    const c = new THREE.Mesh(new THREE.CylinderGeometry(.036, .032, .08, 12), m); c.position.set(x, 1.44, .075); s.add(c);
    const h = new THREE.Mesh(new THREE.BoxGeometry(.012, .04, .02), m); h.position.set(x + .042, 1.44, .075); s.add(h);
    return { t: 'Your mug', x: 'Blue, on the sixth hook, with your name on the bottom in Chief Calder\'s handwriting. Nobody else uses it. Nobody would dare.', wall: ['t', 's', 1.1], y: 1.44, w: .2, h: .2 };
  } },
  // 0.38.15: the tradition designers' decor on Deck 3 (each during its tradition's window; ids agreed with the traditions
  // engineer). longTables: the Sunday table (a runner and two jugs on each long table, 2 draw calls); harvestTables: the
  // harvest supper (burlap runners and baskets of tomatoes and squash, 3); cupBoard: the department cup in the gym (a chalk
  // scoreboard on an easel, o.lines = the teams' scores, and the cup on a plinth, 3); talentStage: talent night (a low
  // riser on the lounge's open floor, a mic stand and a string of bulbs, 3); yearsEnd: Year's end (the Captain's lectern
  // and small lights along the bow windows, 2).
  longTables: { deck: 3, what: 'the long table (the Sunday table, the farewell supper): runners and jugs down the mess\'s long tables, and extra seats', make(g) {
    const s = dressAt(g, 'M', 'floor', 0, 0); messExtra(s);
    for (const [x, z] of MESS_LONG) {
      dressBox(s, 3.3, .004, .32, '#c45a3f', x, .772, z);
      for (const dx of [-.4, .4]) { const j = new THREE.Mesh(new THREE.CylinderGeometry(.05, .06, .17, 12), dressMat('#e9e1d0')); j.position.set(x + dx, .855, z + .06); s.add(j); dressBox(s, .015, .1, .05, '#e9e1d0', x + dx + .065, .87, z + .06); }
    }
    return { t: 'The long table', x: 'Runners down every long table, jugs of water at each one and an extra chair at each end. Chef Brennan seats people next to the people they like, and claims it is an accident.', floor: ['M', MESS_LONG[0][0], MESS_LONG[0][1]], y: .9, w: 1.2, h: .3, d: .5 };
  } },
  harvestTables: { deck: 3, what: 'the harvest supper: burlap runners and baskets from the garden on the long tables', make(g) {
    const s = dressAt(g, 'M', 'floor', 0, 0), C = ['#d8412f', '#f0952e']; messExtra(s);
    MESS_LONG.forEach(([x, z], t) => {
      dressBox(s, 3.3, .004, .36, '#a8875a', x, .772, z);
      [-.45, .45].forEach((dx, b) => {
        const k = new THREE.Mesh(new THREE.CylinderGeometry(.14, .11, .1, 12), dressMat('#a8875a')); k.position.set(x + dx, .82, z + .05); s.add(k);
        for (let i = 0; i < 5; i++) { const a = i * 1.26 + t, r = i ? .065 : 0, f = new THREE.Mesh(new THREE.SphereGeometry(i ? .038 : .045, 8, 6), dressMat(C[(i + b + t) % 2])); f.position.set(x + dx + Math.cos(a) * r, .885 + (i ? 0 : .02), z + .05 + Math.sin(a) * r); s.add(f); }
      });
    });
    return { t: 'Harvest supper', x: 'Burlap down the long tables and baskets from the garden on every one: tomatoes, squash, whatever the beds gave. Everything on the plates tonight was grown on this deck.', floor: ['M', MESS_LONG[0][0], MESS_LONG[0][1]], y: .9, w: 1.2, h: .3, d: .5 };
  } },
  cupBoard: { deck: 3, what: 'the department cup: a chalk scoreboard on an easel and the cup on its plinth, in the gym', make(g, o) {
    const s = dressAt(g, 'F', 'floor', 0, 0), x = .5, z = 6.0;   // by the west wall, past the rowers, facing into the room
    for (const dz of [-.3, .3]) { const l = dressBox(s, .04, 1.5, .04, '#5a3b26', x - .05, .75, z + dz); l.rotation.z = .1; }
    dressBox(s, .03, .03, .7, '#5a3b26', x + .04, .62, z);       // the chalk ledge
    const t = tex(256, 200, (c, w, h) => {
      c.fillStyle = '#1f2b26'; c.fillRect(0, 0, w, h); c.fillStyle = '#efe9dc'; c.font = '700 22px system-ui,sans-serif'; c.fillText('DEPARTMENT CUP', 16, 32);
      c.font = '500 17px system-ui,sans-serif'; (o.lines || ['Works', 'Watch', 'Survey', 'Bridge', 'Commons']).slice(0, 6).forEach((l, k) => c.fillText(l, 22, 64 + k * 24));
    });
    const b = new THREE.Mesh(new THREE.PlaneGeometry(.66, .52), new THREE.MeshBasicMaterial({ map: t, toneMapped: false })); b.position.set(x + .03, .93, z); b.rotation.set(0, Math.PI / 2, -.1); s.add(b);
    dressBox(s, .3, .7, .3, '#5a3b26', x, .35, z - .85);            // the plinth, and the cup on it
    const cup = new THREE.Mesh(new THREE.CylinderGeometry(.09, .04, .14, 14), dressMat('#e8c06a')); cup.position.set(x, .84, z - .85); s.add(cup);
    const st = new THREE.Mesh(new THREE.CylinderGeometry(.06, .07, .07, 14), dressMat('#e8c06a')); st.position.set(x, .735, z - .85); s.add(st);
    for (const sd of [-1, 1]) dressBox(s, .02, .07, .012, '#e8c06a', x, .85, z - .85 + sd * .1);   // the handles
    return { t: 'The department cup', x: 'A rowing relay, one department against another, and Vance keeping score in chalk. The cup is a mug glued to a stand. Nobody has ever wanted anything more.', floor: ['F', x, z], y: .95, w: .3, h: .7, d: .8 };
  } },
  talentStage: { deck: 3, what: 'talent night: a low stage, a mic stand and a string of bulbs on the bow lounge\'s open floor', make(g) {
    const s = dressAt(g, 'L', 'floor', 0, 0), x = 4.2, z = 10.5;   // facing the bar, between the two planted screens
    dressBox(s, 1.2, .18, 1.8, '#5a3b26', x, .09, z);
    const disc = new THREE.Mesh(new THREE.CylinderGeometry(.12, .12, .02, 12), dressMat('#2b2b2b')); disc.position.set(x - .25, .19, z); s.add(disc);
    dressBox(s, .016, 1.35, .016, '#2b2b2b', x - .25, .87, z); dressBox(s, .02, .02, .14, '#2b2b2b', x - .29, 1.5, z).rotation.y = Math.PI / 2;   // the stand and its boom
    const mic = new THREE.Mesh(new THREE.SphereGeometry(.03, 8, 6), dressMat('#2b2b2b')); mic.position.set(x - .37, 1.52, z); s.add(mic);
    for (const dz of [-.88, .88]) dressBox(s, .03, 2.2, .03, '#2b2b2b', x + .55, 1.1, z + dz);   // two poles at the back, and the bulbs strung between
    dressBox(s, .008, .008, 1.76, '#2b2b2b', x + .55, 2.18, z);
    const bm = new THREE.MeshBasicMaterial({ color: col('#ffd27a'), toneMapped: false });
    for (let k = 0; k < 7; k++) { const f = (k + .5) / 7, b = new THREE.Mesh(new THREE.SphereGeometry(.035, 8, 6), bm); b.position.set(x + .55, 2.1 - .12 * 4 * f * (1 - f), z - .88 + 1.76 * f); s.add(b); }
    return { t: 'Talent night', x: 'A low stage, one mic and a string of bulbs. Musicians first, then anyone brave. The applause is guaranteed. The quality is not.', floor: ['L', x, z], y: .4, w: 1.2, h: .5, d: 1.8 };
  } },
  yearsEnd: { deck: 3, what: 'Year\'s end: the Captain\'s lectern and small lights along the bow windows', make(g) {
    const s = dressAt(g, 'L', 'floor', 0, 0), r = ROOM_BOX.L, x = 45.05 - r.i0, z = 10.5 - r.j0;   // just in front of the lounge's lead spot, facing her
    dressBox(s, .36, .04, .3, '#5a3b26', x, .02, z); dressBox(s, .12, 1.0, .12, '#5a3b26', x, .52, z);
    const top = dressBox(s, .42, .04, .5, '#5a3b26', x - .02, 1.08, z); top.rotation.z = .3;   // sloped toward her
    const bm = new THREE.MeshBasicMaterial({ color: col('#fff1c9'), toneMapped: false });
    const M3 = DECKS[3].map, inL = (x, z) => (M3[Math.floor(z)] || '')[Math.floor(x)] === 'L';
    for (let k = 0; k <= 30; k++) {                      // along the bow windows: out from the lounge's middle until the floor ends, then back 30 cm
      const a = (-60 + k * 4) * Math.PI / 180; let rr = 4; while (rr < 14 && inL(41 + (rr + .05) * Math.cos(a), 10.5 + (rr + .05) * Math.sin(a))) rr += .05;
      const b = new THREE.Mesh(new THREE.SphereGeometry(.025, 6, 5), bm); b.position.set(41 + (rr - .3) * Math.cos(a) - r.i0, 1.3 + .06 * Math.abs(Math.sin(k * 1.3)), 10.5 + (rr - .3) * Math.sin(a) - r.j0); s.add(b);
    }
    return { t: 'Year\'s end', x: 'A lectern for the Captain and little lights all along the bow windows. She reads from the year\'s log, the good days and the hard ones, and then the letters from Midtour come back.', floor: ['L', x, z], y: .8, w: .5, h: 1.2, d: .5 };
  } },
  // 0.38.16. openLab: open lab on Deck 2: two trays of samples on the Survey lab's island and a tent card, OPEN LAB, in the
  // middle of it (the island's top at .91). 3 draw calls.
  openLab: { deck: 2, what: 'open lab: trays of samples and an OPEN LAB card on the Survey lab\'s island', make(g) {
    const s = dressAt(g, 'L', 'floor', 3.0, 4.5);        // the island's centre
    [[-1.25, .22], [1.15, -.22]].forEach(([x, z], k) => {
      dressBox(s, .34, .02, .22, '#eef1ef', x, .921, z);
      for (let i = 0; i < 6; i++) { const d = new THREE.Mesh(new THREE.CylinderGeometry(.03, .03, .018, 10), dressMat(i % 2 ? '#5fd6c6' : '#7a9a5a')); d.position.set(x - .1 + (i % 3) * .1, .94, z + (i < 3 ? -.05 : .05)); s.add(d); }
    });
    const t = tex(256, 96, (c, w, h) => { c.fillStyle = '#f4efe2'; c.fillRect(0, 0, w, h); c.fillStyle = '#1f3c6e'; c.font = '800 40px system-ui,sans-serif'; c.textAlign = 'center'; c.fillText('OPEN LAB', w / 2, 52); c.font = '500 17px system-ui,sans-serif'; c.fillText('ask us anything', w / 2, 80); });
    const cm = new THREE.MeshBasicMaterial({ map: t, toneMapped: false });
    for (const sd of [1, -1]) { const p = new THREE.Mesh(new THREE.PlaneGeometry(.32, .12), cm); p.position.set(0, .97, sd * .03); p.rotation.set(-sd * .45, sd > 0 ? 0 : Math.PI, 0); s.add(p); }   // a tent card, readable from both sides
    return { t: 'Open lab', x: 'Dr. Sato\'s open lab: trays of samples from the last survey, a card saying OPEN LAB, and the Survey team pretending they are not delighted to be asked about rocks.', floor: ['L', 3.0, 4.5], y: 1.0, w: .6, h: .3, d: .4 };
  } },
  // 0.38.17. tilesTrophy: a lasting trace once you first beat Rina at Tiles (section 23 pushes { id: 'tilesTrophy', day }
  // to SHIP.traces): a small gold trophy at the back of your keepsake shelf, between slots 5 and 6
  // (DECKS[4].keepsakes.trophy), clear of the keepsakes in front. On the shelf's wall, so it lowers with it. 1 draw call.
  tilesTrophy: { deck: 4, what: 'your Tiles trophy on the keepsake shelf above your bunk', make(g) {
    const s = dressAt(g, 'a', 'n', 2.5), [tx, ty, tz] = DECKS[4].keepsakes.trophy, x = tx - (ROOM_BOX.a.i0 + 2.5), z = tz - (Z0(ROOM_BOX.a.j0) + T / 2 + OZ), m = dressMat('#e8c06a');
    const add = (geo, y) => { const k = new THREE.Mesh(geo, m); k.position.set(x, ty + y, z); s.add(k); };
    add(new THREE.BoxGeometry(.04, .014, .036), .007); add(new THREE.CylinderGeometry(.005, .007, .035, 6), .031); add(new THREE.CylinderGeometry(.022, .01, .04, 10), .068);
    return { t: 'Tiles trophy', x: 'A little gold cup: the day you beat Rina at Tiles. She says she let you win. She has never let anyone win.', wall: ['a', 'n', 2.5], y: 2.25, w: .2, h: .2 };
  } },
  // 0.38.11. tastingTable: Brennan's tasting table on Wednesday's dinner (o.title: the dish; o.lines: up to five lines in
  // chalk, the votes so far): the chalkboard by the mess door and a tray of tasting cups and a bowl of vote tokens on the
  // end of a long table. 5 draw calls.
  tastingTable: { deck: 3, what: 'Brennan\'s tasting table: a chalkboard, a tray of tasting cups and a bowl of vote tokens', make(g, o) {
    const b = dressAt(g, 'M', 'w', 2.9), dish = o.title || 'Something new from the galley';
    dressBox(b, .62, .5, .03, '#5a3b26', 0, 1.5, .015); dressBox(b, .62, .03, .06, '#5a3b26', 0, 1.235, .045);   // the frame, and the chalk ledge
    const t = tex(256, 200, (c, w, h) => {
      c.fillStyle = '#1f2b26'; c.fillRect(0, 0, w, h); c.fillStyle = '#efe9dc'; c.font = '700 22px system-ui,sans-serif'; c.fillText('TASTING TABLE', 16, 32);
      c.font = 'italic 600 17px Georgia,serif'; String(dish).split('\n').slice(0, 2).forEach((l, k) => c.fillText(l, 16, 62 + k * 21));
      c.font = '500 15px system-ui,sans-serif'; (o.lines || ['Try a cup, then vote:', 'gold token: on the menu', 'white token: back to the galley']).slice(0, 5).forEach((l, k) => c.fillText(l, 16, 112 + k * 19));
    });
    const pl = new THREE.Mesh(new THREE.PlaneGeometry(.56, .44), new THREE.MeshBasicMaterial({ map: t, toneMapped: false })); pl.position.set(0, 1.5, .032); b.add(pl);
    const s = dressAt(g, 'M', 'floor', 1.3, 4.0);        // the west end of the third long table (its top at .77)
    dressBox(s, .5, .02, .3, '#5a3b26', 0, .781, 0);
    for (let k = 0; k < 8; k++) { const c = new THREE.Mesh(new THREE.CylinderGeometry(.022, .018, .035, 8), dressMat('#f4f1e8')); c.position.set(-.2 + (k % 4) * .085, .809, k < 4 ? -.07 : .07); s.add(c); }
    const bowl = new THREE.Mesh(new THREE.CylinderGeometry(.06, .045, .04, 12), dressMat('#f4f1e8')); bowl.position.set(.16, .811, 0); s.add(bowl);
    [[-.02, -.015], [.015, .02], [.025, -.02], [-.025, .02], [0, 0]].forEach(([x, z]) => { const k = new THREE.Mesh(new THREE.CylinderGeometry(.012, .012, .006, 8), dressMat('#e9c46a')); k.position.set(.16 + x, .832, z); s.add(k); });
    return { t: 'Tasting table', x: 'Brennan\'s tasting table. ' + String(dish).replace(/\n/g, ' ') + '. Take a cup, then drop a token in the bowl: gold if it should go on the menu.', wall: ['M', 'w', 2.9], y: 1.5 };
  } },
  // lanternWalk: the Lantern walk at dusk: paper lanterns on strings down both sides of the promenade, one InstancedMesh of
  // lanterns (unlit, so they glow), the strings merged, and a basket of spares at the lift plaza: 3 draw calls, no shadows.
  lanternWalk: { deck: 3, what: 'paper lanterns strung down both sides of the promenade', make(g) {
    const r = ROOM_BOX['='], s = dressAt(g, '=', 'floor', 0, 0), pts = [], C = ['#ffb35c', '#ff8a5c', '#ffd27a', '#f2c94c'];
    for (const [x0, x1] of [[12.5, 16.6], [23.5, 39.7]]) for (const z of [9.35, 12.65]) {
      dressBox(s, x1 - x0 + .4, .01, .01, '#3a3a3a', (x0 + x1) / 2 - r.i0, 2.34, z - r.j0);   // the string
      for (let x = x0; x <= x1; x += 1.15) { const y = 2.12 + .06 * Math.sin(x * 2.1); pts.push([x - r.i0, y, z - r.j0]); dressBox(s, .006, 2.34 - y - .16, .006, '#3a3a3a', x - r.i0, (2.34 + y + .16) / 2, z - r.j0); }
    }
    const hung = pts.length, bx = 22.9 - r.i0, bz = 12.6 - r.j0;    // 0.38.16: and a basket of spares where the promenade meets the lift plaza
    const bk = new THREE.Mesh(new THREE.CylinderGeometry(.3, .24, .32, 14), dressMat('#a8875a')); bk.position.set(bx, .16, bz); s.add(bk);
    [[0, 0], [.13, .08], [-.12, .07], [.05, -.13], [-.08, -.1]].forEach(([dx, dz], k) => pts.push([bx + dx, .38 + (k ? 0 : .06), bz + dz]));
    const im = new THREE.InstancedMesh(new THREE.SphereGeometry(1, 10, 8), new THREE.MeshBasicMaterial({ toneMapped: false }), pts.length), m = new THREE.Matrix4(), q = new THREE.Quaternion(), sc = new THREE.Vector3(.13, .17, .13), sb = new THREE.Vector3(.11, .13, .11);
    pts.forEach(([x, y, z], k) => { im.setMatrixAt(k, m.compose(new THREE.Vector3(x, y, z), q, k < hung ? sc : sb)); im.setColorAt(k, col(C[k % 4])); });
    im.userData.noMerge = true; im.frustumCulled = false; s.add(im);
    return { t: 'Lanterns', x: 'Paper lanterns all the way down the promenade, one for every name on the crew list, and a few spares for the ones who have left.', floor: ['=', pts[12][0], pts[12][2]], y: pts[12][1], w: .3, h: .4, d: .3 };
  } },
  // 0.38.31: spiceJars: the jars on the mess hall's spice shelf, one more after each Spice shelf supper. A trace ({ id:
  // 'spiceJars', day, n }): n jars when given, else one for each week since day (from the first supper), up to 12. 4 draw calls
  spiceJars: { deck: 3, what: 'spice jars from home on the mess hall\'s spice shelf', make(g, o) {
    const s = dressAt(g, SPICES.room, SPICES.wall, SPICES.along), C = ['#b5432a', '#d9a521', '#6e7f3a', '#7a4a2a', '#b5432a', '#3a2f2a'];
    const n = Math.max(1, Math.min(SPICES.slots.length, Math.round(o.n || (1 + Math.floor(Math.max(0, SHIP.time.day - (o.day || SHIP.time.day)) / 7)))));
    for (let k = 0; k < n; k++) {
      const x = SPICES.slots[(k * 5) % SPICES.slots.length], h = .08 + (k % 3) * .015;
      const j = new THREE.Mesh(new THREE.CylinderGeometry(.032, .032, h, 10), dressMat(C[k % 3])); j.position.set(x, SPICES.y + .015 + h / 2, .08); s.add(j);
      const l = new THREE.Mesh(new THREE.CylinderGeometry(.034, .034, .02, 10), dressMat('#c9a64a')); l.position.set(x, SPICES.y + .025 + h, .08); s.add(l);
    }
    return { t: 'Spice shelf', x: n + (n === 1 ? ' jar' : ' jars') + ' on the shelf, each brought from home by someone aboard, labelled in their handwriting. Brennan cooks with three of them at every Spice shelf supper.', wall: [SPICES.room, SPICES.wall, SPICES.along], y: SPICES.y + .1, w: 1.3, h: .3 };
  } },
  // 0.38.30: nameYours: a lasting trace from Name on the beam: your name, freshly painted at the beam's west end. 1 draw call
  nameYours: { deck: 5, what: 'your name, freshly painted on the Works bay\'s beam', make(g) {
    const [sa, sy] = BEAM.slots[0], s = dressAt(g, BEAM.room, 'n', sa), name = firstName(SHIP.player && SHIP.player.name);   // 0.47.6: your first name, in slot 0
    const t = tex(256, 40, (c, w, h) => { c.fillStyle = '#f8f4ea'; c.font = '700 32px Georgia,serif'; const tw = Math.min(w - 8, c.measureText(name).width); c.fillText(name, (w - tw) / 2, 30, w - 8); });
    const p = new THREE.Mesh(new THREE.PlaneGeometry(1.2, .1875), new THREE.MeshBasicMaterial({ map: t, transparent: true, toneMapped: false })); p.position.set(0, BEAM.y + sy, .138); s.add(p);
    return { t: 'Your name', x: 'Your name on the beam, the paint still bright, at the end of the row. Every new hand gets one. Yours will fade like the others, slowly, and somebody will touch it up.', wall: [BEAM.room, 'n', sa], y: BEAM.y + sy, w: 1.2, h: .2 };
  } },
  // 0.47.6 (playtest): nameNew: the Works hands who joined after you, painted beside your name (slots 1-3, the newest three, in the
  // order they came). Every { id: 'nameNew', day, name } in SHIP.traces, on one canvas: 1 draw call
  nameNew: { deck: 5, what: 'the newest Works hands\' names, painted on the beam beside yours', make(g) {
    const list = (SHIP.traces || []).filter(x => x && x.id === 'nameNew' && x.name).slice(-3), [a0] = BEAM.slots[1], [a1] = BEAM.slots[2], mid = (a0 + a1) / 2;
    const s = dressAt(g, BEAM.room, 'n', mid), span = a0 - a1 + 1.2;   // one plane over slots 1-3 (slot 0's corner stays clear)
    const t = tex(512, 80, (c, w, h) => { c.font = '700 32px Georgia,serif'; list.forEach((x, k) => { const [sa, sy] = BEAM.slots[k + 1], n = firstName(x.name);
      const cx = (sa - mid + span / 2) / span * w, tw = Math.min(w * 1.2 / span - 8, c.measureText(n).width); c.fillStyle = ['#f8f4ea', '#e8c06a', '#7fd6c8'][k];
      c.fillText(n, cx - tw / 2, sy > 0 ? 30 : 70, w * 1.2 / span - 8); }); });
    const p = new THREE.Mesh(new THREE.PlaneGeometry(span, .375), new THREE.MeshBasicMaterial({ map: t, transparent: true, toneMapped: false })); p.position.set(0, BEAM.y, .132); s.add(p);   // 6 mm in front of the beam's names, 6 mm behind yours (0.47.8, R2: at least 5 mm)
    return { t: 'New names', x: 'The newest names on the beam, beside yours: ' + list.map(x => firstName(x.name)).join(', ') + '. The paint is still bright.', wall: [BEAM.room, 'n', mid], y: BEAM.y, w: span, h: .4 };
  } },
  partyLounge: { deck: 3, what: 'party decorations in the bow lounge: bunting, balloons and a banner', make(g, o) {
    const s = dressAt(g, 'L', 'floor', 0, 0), C = ['#c45a3f', '#e8c06a', '#5fd6c6'], y = 2.2;
    const pts = [[41.4, 9.0], [46.44, 8.27], [46.44, 13.73], [41.4, 13.0]].map(([x, z]) => [x - ROOM_BOX.L.i0, z - ROOM_BOX.L.j0]);
    for (let k = 0; k < 3; k++) {                                     // three strings of bunting, sagging a little
      const [a, b] = [pts[k], pts[k + 1]], len = Math.hypot(b[0] - a[0], b[1] - a[1]), n = Math.round(len / .32), ang = Math.atan2(b[0] - a[0], b[1] - a[1]);
      for (let i = 0; i <= n; i++) {
        const f = i / n, x = a[0] + (b[0] - a[0]) * f, z = a[1] + (b[1] - a[1]) * f, sag = .22 * 4 * f * (1 - f);
        if (i < n) { const m = dressBox(s, .012, .012, len / n + .01, '#e9e1d0', x + (b[0] - a[0]) / n / 2, y - .22 * 4 * (f + .5 / n) * (1 - f - .5 / n), z + (b[1] - a[1]) / n / 2); m.rotation.y = ang; }
        if (i > 0 && i < n) { const p = new THREE.Mesh(new THREE.ConeGeometry(.085, .17, 3), dressMat(C[(i + k) % 3])); p.rotation.set(Math.PI, Math.PI / 2 - ang, 0); p.scale.z = .25; p.position.set(x, y - sag - .095, z); s.add(p); }
      }
    }
    for (const [x, z] of [[41.7, 8.9], [46.44, 8.27], [46.44, 13.73]].map(([x, z]) => [x - ROOM_BOX.L.i0, z - ROOM_BOX.L.j0]))   // balloons, three to a bunch
      [[0, 2.32, 0], [.17, 2.22, .06], [-.1, 2.18, .14]].forEach(([dx, by, dz], k) => {
        const b = new THREE.Mesh(new THREE.SphereGeometry(.13, 12, 9), dressMat(C[k])); b.scale.y = 1.18; b.position.set(x + dx, by, z + dz); s.add(b);
        dressBox(s, .008, by - 1.0, .008, '#e9e1d0', x + dx * .4, (by + 1.0) / 2 - .1, z + dz * .4); });
    const t = tex(512, 112, (c, w, h) => { c.fillStyle = '#1f3c6e'; c.fillRect(0, 0, w, h); c.fillStyle = '#e8c06a'; c.fillRect(0, 8, w, 4); c.fillRect(0, h - 12, w, 4);
      const l = String(o.title || 'WELL DONE, WREN!').toUpperCase().replace(/\n/g, ' ');
      c.fillStyle = '#f4efe2'; c.font = '800 46px system-ui,sans-serif'; const fs = Math.min(46, Math.floor(46 * (w - 36) / c.measureText(l).width));
      c.font = '800 ' + fs + 'px system-ui,sans-serif'; c.textAlign = 'center'; c.fillText(l, w / 2, 56 + fs / 3); });
    const bm = new THREE.MeshBasicMaterial({ map: t, toneMapped: false }), [bx, bz] = [46.44 - ROOM_BOX.L.i0, 11 - ROOM_BOX.L.j0];
    for (const side of [1, -1]) { const p = new THREE.Mesh(new THREE.PlaneGeometry(1.8, .39), bm); p.position.set(bx + side * .006, 1.86, bz); p.rotation.y = side * Math.PI / 2; s.add(p); }   // both sides, 12 mm apart
    return { t: 'Party decorations', x: 'Bunting from the bar to the windows, balloons that are already starting to droop, and a banner: ' + String(o.title || 'Well done, Wren!') + '.', floor: ['L', bx, bz], y: 1.86, w: .3, h: .5, d: 1.8 };
  } },
};
function dressHide(id) {
  const e = DRESS.on.get(id); if (!e) return;
  const shared = new Set(Object.values(DRESS_MATS).concat(HIT_MAT));   // the cached colours and the tap boxes' stay; a piece's own materials go (0.38.13)
  e.g.parent && e.g.parent.remove(e.g); e.g.traverse(o => { if (o.geometry) o.geometry.dispose(); if (o.material && !shared.has(o.material)) { if (o.material.map) o.material.map.dispose(); o.material.dispose(); } });
  for (const k of e.blocked || []) BLOCKED.delete(k);
  ITEMS = ITEMS.filter(it => !e.items.includes(it)); WALL_DECOR = WALL_DECOR.filter(d => !e.decor.includes(d));
  DRESS.on.delete(id);
}
function dressShow(list) {
  if (!deckRoot) return;
  const want = new Map((list || []).map(x => typeof x === 'string' ? [x, {}] : [x.id, x]).filter(([id]) => DECK_DRESS[id] && DECK_DRESS[id].deck === deckDef.num));
  if (DRESS.root !== deckRoot) { DRESS.root = deckRoot; DRESS.on.clear(); DRESS.key = ''; }   // a new deck: the old groups went with it
  const key = JSON.stringify([...want]); if (key === DRESS.key) return;
  DRESS.key = key;
  for (const id of [...DRESS.on.keys()]) if (!want.has(id) || DRESS.on.get(id).o !== JSON.stringify(want.get(id))) dressHide(id);
  for (const [id, o] of want) {
    if (DRESS.on.has(id)) continue;
    const g = new THREE.Group(), it = DECK_DRESS[id].make(g, o), decor = [];
    deckRoot.add(g);
    for (const s of g.children) { mergeMeshes(s); s.traverse(m => { if (m.isMesh) { m.castShadow = false; m.receiveShadow = true; } }); if (s.userData.edge) { const d = { g: s, e: s.userData.edge }; WALL_DECOR.push(d); decor.push(d); } }
    // the tap: a hit box on the wall piece or over the floor spot, like place()'s and placeWall()'s
    const hit = new THREE.Mesh(new THREE.BoxGeometry(it.w || .6, it.h || (it.floor ? .1 : .6), it.d || .3), HIT_MAT); hit.userData.noMerge = true;
    const host = it.wall ? g.children[0] : g; let front = 0;
    if (it.wall) { hit.position.set(0, it.y, .15); front = FACING[it.wall[1]]; }
    else { const r = ROOM_BOX[it.floor[0]]; hit.position.set(X0(r.i0) + it.floor[1], it.y || .05, Z0(r.j0) + it.floor[2]); }
    host.add(hit);
    const item = { t: it.t, x: it.x, hit, g: host, front, depth: it.wall ? .1 : .6, wall: !!it.wall, ...(it.tag || {}) }; hit.userData.item = item; ITEMS.push(item);   // tag: fields for the tap handlers (0.38.29)
    const items = [item];
    for (const m of it.more || []) {                     // 0.38.17: more floor taps with the same text (Tiles night: one on every board)
      const r = ROOM_BOX[m.floor[0]], h2 = new THREE.Mesh(new THREE.BoxGeometry(m.w || .6, m.h || .1, m.d || .3), HIT_MAT); h2.userData.noMerge = true;
      h2.position.set(X0(r.i0) + m.floor[1], m.y || .05, Z0(r.j0) + m.floor[2]); g.add(h2);
      const i2 = { t: it.t, x: it.x, hit: h2, g, front: 0, depth: .6, wall: false, ...(it.tag || {}) }; h2.userData.item = i2; ITEMS.push(i2); items.push(i2);
    }
    const blocked = (it.block || []).map(([i, j]) => i + ',' + j).filter(k => !BLOCKED.has(k)); for (const k of blocked) BLOCKED.add(k);   // 0.38.23: tiles it stands on, blocked while it's out
    DRESS.on.set(id, { g, item, items, decor, blocked, o: JSON.stringify(o) });
  }
  if (typeof refreshPickables === 'function') refreshPickables();
}
const dressingOn = () => [...DRESS.on.keys()];

