// =====================================================================
// 17. MACHINES & JOBS
// The ship's machines, how they wear, and what that does to the ship and the people aboard. So far (0.33.x, B1)
// it's data and logic only: nothing here draws anything or calls R().
//   MACHINE_KINDS       what each kind is: its system, how long it lasts, what wears it, what it does when it falters
//   machineList()       every machine aboard: DECKS[n].machines ({ id, kind, at, room, face, panel }), or the
//                       stand-ins in STUB_MACHINES on a deck that has none yet
//   machinesNow()       SHIP.machines brought up to date: SHIP.machines[id] = { cond: 0-100, state, lastService }
//   machineState(cond)  'healthy' | 'worn' | 'faulty' | 'failing' | 'broken'
//   shipSystems()       air, water, power, heat, food, waste, hull, comms, propulsion: 0-100 each, with the
//                       dependencies (power feeds everything; water feeds the garden, the garden the galley)
//   shipHealth()        the systems blended into one score, 0-100
//   shipEffects(deck)   what the machines do to people on a deck now: needs, mood, walking, cooking, the lift
//   serviceMachine(id)  put a machine right (the job list, B2; machine_check.py's ideal crew)
// Wear runs on paper, one ship hour at a time, from the schedules (section 14): the ovens with the meals, the
// washers with the laundry and the day's uniforms, the lift with every ride, the scrubbers with the people on
// their deck, the recycler with every wash, and everything a little with time. Worn machines wear faster. Each
// hour's wear has a little variety from schedU(machine, hour), so the same ship wears the same way however the
// game is played: one big jump or minute by minute. Nothing moves until something asks (machinesNow); the save
// asks every ship hour.
// =====================================================================
// kinds: sys = the system it belongs to; life = days from 100 to 0 at normal use, never serviced; time = the share
// of wear that comes with time (the rest comes with use); use = what wears it (a counter from machUseDay, measured
// against an average day, so it follows the schedules as they change); scope = where its effects are felt
// ('deck': its own deck, 'ship': everywhere); w = its weight in its system; tier = who may work on it (design
// doc, "Works progression"; a machine may carry its own `tier`); part = what a repair needs (B3)
const MACHINE_KINDS = {
  oven:        { name: 'Oven',              sys: 'food',       life: 10, time: .2, use: 'cook',   scope: 'ship', w: 2, tier: 1, part: 'element' },
  range:       { name: 'Range',             sys: 'food',       life: 12, time: .2, use: 'cook',   scope: 'ship', w: 2, tier: 1, part: 'element' },
  galleyplant: { name: 'Galley plant',      sys: 'food',       life: 14, time: .5, use: 'meal',   scope: 'ship', w: 1, tier: 1, part: 'fan belt' },
  extractor:   { name: 'Galley extractor',  sys: 'food',       life: 14, time: .5, use: 'cook',   scope: 'ship', w: 1, tier: 1, part: 'fan belt' },
  chiller:     { name: 'Cold store chiller', sys: 'food',      life: 16, time: .7, use: 'meal',   scope: 'ship', w: 2, tier: 1, part: 'compressor' },
  washer:      { name: 'Washer',            sys: 'waste',      life: 12, time: .1, use: 'loads',  scope: 'ship', w: 1, tier: 1, part: 'pump' },
  lift:        { name: 'Main lift',         sys: 'transport',  life: 16, time: .3, use: 'ride',   scope: 'ship', w: 1, tier: 1, part: 'relay' },
  lights:      { name: 'Light relays',      sys: 'power',      life: 18, time: .6, use: 'heads',  scope: 'deck', w: 1, tier: 1, part: 'relay' },
  junction:    { name: 'Power junction',    sys: 'power',      life: 28, time: 1,                 scope: 'ship', w: 2, tier: 3, part: 'breaker' },
  scrubber:    { name: 'Air scrubber',      sys: 'air',        life: 11, time: .4, use: 'heads',  scope: 'deck', w: 2, tier: 2, part: 'filter' },
  heater:      { name: 'Heating plant',     sys: 'heat',       life: 18, time: .6, use: 'heads',  scope: 'deck', w: 2, tier: 2, part: 'valve' },
  recycler:    { name: 'Water recycler',    sys: 'water',      life: 14, time: .3, use: 'water',  scope: 'ship', w: 3, tier: 2, part: 'membrane' },
  filter:      { name: 'Water filter bank', sys: 'water',      life: 9,  time: .3, use: 'water',  scope: 'ship', w: 2, tier: 2, part: 'cartridge' },
  heatpump:    { name: 'Heating pumps',     sys: 'heat',       life: 18, time: .6, use: 'heads',  scope: 'deck', w: 1, tier: 2, part: 'pump' },
  valve:       { name: 'Pipe valves',       sys: 'water',      life: 30, time: 1,                 scope: 'ship', w: 1, tier: 2, part: 'valve' },
  o2cell:      { name: 'Oxygen cells',      sys: 'air',        life: 18, time: .8, use: 'heads',  scope: 'ship', w: 2, tier: 2, part: 'oxygen cell' },
  electrolyser: { name: 'Electrolyser',     sys: 'air',        life: 20, time: 1,                 scope: 'ship', w: 2, tier: 2, part: 'membrane' },
  inverter:    { name: 'Inverter',          sys: 'power',      life: 28, time: 1,                 scope: 'ship', w: 2, tier: 3, part: 'breaker' },
  conduit:     { name: 'Power conduit',     sys: 'power',      life: 32, time: 1,                 scope: 'ship', w: 1, tier: 3, part: 'cable' },
  cartdock:    { name: 'Cart dock',         sys: 'transport',  life: 20, time: 1,                 scope: 'ship', w: 1, tier: 1, part: 'relay' },
  pump:        { name: 'Circulation pumps', sys: 'water',      life: 18, time: .5, use: 'water',  scope: 'ship', w: 2, tier: 2, part: 'pump' },
  uv:          { name: 'UV steriliser',     sys: 'water',      life: 20, time: .5, use: 'water',  scope: 'ship', w: 1, tier: 2, part: 'uv lamp' },
  irrigation:  { name: 'Irrigation pumps',  sys: 'water',      life: 18, time: .8, use: 'garden', scope: 'ship', w: 1, tier: 2, part: 'pump' },
  nutrient:    { name: 'Nutrient dosing',   sys: 'food',       life: 16, time: .6, use: 'garden', scope: 'ship', w: 1, tier: 2, part: 'nutrient pack' },
  growlight:   { name: 'Grow lights',       sys: 'food',       life: 14, time: .9, use: 'garden', scope: 'ship', w: 1, tier: 1, part: 'lamp' },   // the garden's grow racks (0.33.34)
  airplant:    { name: 'Air plant',         sys: 'air',        life: 20, time: 1,                 scope: 'ship', w: 3, tier: 2, part: 'filter' },
  fan:         { name: 'Main fan',          sys: 'air',        life: 24, time: 1,                 scope: 'ship', w: 2, tier: 2, part: 'bearing' },
  manifold:    { name: 'Manifold',          sys: 'heat',       life: 24, time: 1,                 scope: 'ship', w: 2, tier: 2, part: 'valve' },
  gasplant:    { name: 'Lab gas plant',     sys: 'comms',      life: 20, time: .5, use: 'heads',  scope: 'deck', w: 1, tier: 2, part: 'regulator' },
  battery:     { name: 'Battery bank',      sys: 'power',      life: 28, time: 1,                 scope: 'ship', w: 2, tier: 3, part: 'cell' },
  relay:       { name: 'Bridge relays',     sys: 'comms',      life: 24, time: .7, use: 'heads',  scope: 'ship', w: 2, tier: 3, part: 'relay' },
  databus:     { name: 'Bridge data bus',   sys: 'comms',      life: 24, time: 1,                 scope: 'ship', w: 1, tier: 3, part: 'signal card' },
  array:       { name: 'Sensor array',      sys: 'comms',      life: 40, time: 1,                 scope: 'ship', w: 2, tier: 3, part: 'signal card' },
  damper:      { name: 'Duct dampers',      sys: 'air',        life: 30, time: 1,                 scope: 'ship', w: 1, tier: 2, part: 'relay' },   // the air line's two duct dampers (0.33.55, plans/mechanics/architect-air-line.html)
  doorgear:    { name: 'Bay door gear',     sys: 'hull',       life: 40, time: 1,                 scope: 'ship', w: 1, tier: 2, part: 'seal' },
  hullseal:    { name: 'Hull seals',        sys: 'hull',       life: 32, time: 1,                 scope: 'ship', w: 2, tier: 3, part: 'seal' },
  reactor:     { name: 'Reactor',           sys: 'power',      life: 60, time: 1,                 scope: 'ship', w: 3, tier: 4, part: 'control rod' },
  coil:        { name: 'Drive coil',        sys: 'propulsion', life: 30, time: 1,                 scope: 'ship', w: 1, tier: 4, part: 'coil winding' },
  // the rec deck's (0.84.0, rec engineer B; plan section 6): their own 'rec' system, felt on that deck only; use 'heads' (people on the deck)
  poolfilter:  { name: 'Pool filter',       sys: 'rec',        life: 20, time: .4, use: 'heads',  scope: 'deck', w: 2, tier: 1, part: 'cartridge' },
  pooldoser:   { name: 'Pool dosing',       sys: 'rec',        life: 24, time: .6, use: 'heads',  scope: 'deck', w: 1, tier: 2, part: 'relay' },
  poolheat:    { name: 'Pool heat exchanger', sys: 'rec',      life: 28, time: .6, use: 'heads',  scope: 'deck', w: 1, tier: 2, part: 'valve' },
  riverpump:   { name: 'River pump',        sys: 'rec',        life: 24, time: .5, use: 'heads',  scope: 'deck', w: 2, tier: 2, part: 'bearing' },
  wavegate:    { name: 'Wave gate',         sys: 'rec',        life: 30, time: .5, use: 'heads',  scope: 'deck', w: 1, tier: 2, part: 'seal' },
  wallholds:   { name: 'Climbing holds',    sys: 'rec',        life: 16, time: .3, use: 'heads',  scope: 'deck', w: 1, tier: 1, part: 'seal' },   // a chore: tighten and reset a route
  belay:       { name: 'Auto-belay',        sys: 'rec',        life: 26, time: .4, use: 'heads',  scope: 'deck', w: 2, tier: 2, part: 'bearing' },
  stagelights: { name: 'Stage lights',      sys: 'rec',        life: 26, time: .6, use: 'heads',  scope: 'deck', w: 1, tier: 1, part: 'lamp' },
  soundrack:   { name: 'Sound rack',        sys: 'rec',        life: 32, time: .7, use: 'heads',  scope: 'deck', w: 1, tier: 2, part: 'cable' },
  seathinges:  { name: 'Seat hinges',       sys: 'rec',        life: 20, time: .3, use: 'heads',  scope: 'deck', w: 1, tier: 1, part: 'bearing' },   // a chore: a few seats at a time
  courtnet:    { name: 'Court emitters',    sys: 'rec',        life: 32, time: .7, use: 'heads',  scope: 'deck', w: 2, tier: 3, part: 'breaker' },
  scoreboard:  { name: 'Scoreboard',        sys: 'rec',        life: 28, time: .7, use: 'heads',  scope: 'deck', w: 1, tier: 1, part: 'lamp' },
  gravplate:   { name: 'Gravity plates',    sys: 'rec',        life: 40, time: .8, use: 'heads',  scope: 'deck', w: 2, tier: 3, part: 'signal card' },
};
MACHINE_KINDS.powerjunction = MACHINE_KINDS.junction;    // the old name for a power junction, still on Deck 2's 2-breaker-1
const MACHINE_STATES = ['healthy', 'worn', 'faulty', 'failing', 'broken'];
const machineState = c => c >= 75 ? 'healthy' : c >= 50 ? 'worn' : c >= 25 ? 'faulty' : c >= 10 ? 'failing' : 'broken';
const MACHINE_SEV = { healthy: 0, worn: 0, faulty: .35, failing: .7, broken: 1 };   // how hard a state is felt
const SYSTEMS = ['air', 'water', 'power', 'heat', 'food', 'waste', 'hull', 'comms', 'propulsion', 'transport'];
const SYSTEM_W = { air: 3, water: 2, power: 3, heat: 2, food: 2, waste: 1, hull: 2, comms: 1, propulsion: 1, transport: 1 };   // their weight in ship health
if (REC_DECK) { SYSTEMS.push('rec'); SYSTEM_W.rec = 1; }   // 0.84.0 (rec engineer B, lead 18's call): the rec deck's machines, only while it's switched on
// stand-ins until the architects add DECKS[n].machines with the utility rooms (A5): [id, kind, room]. Their
// `at` and `panel` are the room's middle tile; the lift is at the lift. A stand-in drops out as soon as its deck
// has a real machine with its id or in its room. Decks 1 and 3 use the bridge architect's agreed ids.
const STUB_MACHINES = {
  1: [['1-lights-1', 'lights', 'k'], ['1-junction-1', 'junction', 'k'], ['1-relay-1', 'relay', 'u'], ['1-relay-2', 'relay', 'u'], ['1-databus-1', 'databus', 'c']],
  2: [['2-lights-1', 'lights', 'u'], ['2-gasplant-1', 'gasplant', 'g'], ['2-array-1', 'array', 'A']],
  3: [['3-oven-1', 'oven', 'K'], ['3-oven-2', 'oven', 'K'], ['3-range-1', 'range', 'K'], ['3-extractor-1', 'extractor', 'g'], ['3-chiller-1', 'chiller', 'g'],
      ['3-recycler-1', 'recycler', 'R'], ['3-filter-1', 'filter', 'R'], ['3-pump-1', 'pump', 'R'], ['3-uv-1', 'uv', 'R'], ['3-lights-1', 'lights', 'R'],
      ['3-irrigation-1', 'irrigation', 'i'], ['3-nutrient-1', 'nutrient', 'i'], ['3-growlight-1', 'growlight', 'G'], ['3-growlight-2', 'growlight', 'G']],
  4: [['4-scrubber-1', 'scrubber', 's'], ['4-scrubber-2', 'scrubber', 's'], ['4-heater-1', 'heater', 't'], ['4-lights-1', 'lights', 'k'],
      ['4-washer-1', 'washer', 'l'], ['4-washer-2', 'washer', 'l'], ['4-washer-3', 'washer', 'l'], ['4-washer-4', 'washer', 'l']],
  5: [['5-mainlift-1', 'lift', null], ['5-airplant-1', 'airplant', 'a'], ['5-airplant-2', 'airplant', 'a'], ['5-fan-1', 'fan', 'F'],
      ['5-manifold-1', 'manifold', 'n'], ['5-lights-1', 'lights', 'u'], ['5-battery-1', 'battery', 'y'], ['5-doorgear-1', 'doorgear', 'd']],
  6: [['6-reactor-1', 'reactor', 'R'], ['6-coil-1', 'coil', 'E'], ['6-coil-2', 'coil', 'E'], ['6-coil-3', 'coil', 'E'],
      ['6-junction-1', 'junction', 'j'], ['6-junction-2', 'junction', 'J'], ['6-hullseal-1', 'hullseal', 'c'], ['6-hullseal-2', 'hullseal', 'C']],
};
// a room's middle tile: the room's tile nearest its centre
function machRoomTile(n, room) {
  const map = DECKS[n].map, ts = [];
  map.forEach((row, j) => { for (let i = 0; i < row.length; i++) if (row[i] === room) ts.push([i, j]); });
  if (!ts.length) return null;
  const ci = ts.reduce((a, t) => a + t[0], 0) / ts.length, cj = ts.reduce((a, t) => a + t[1], 0) / ts.length;
  return ts.reduce((b, t) => (t[0] - ci) ** 2 + (t[1] - cj) ** 2 < (b[0] - ci) ** 2 + (b[1] - cj) ** 2 ? t : b);
}
const machSeed = id => { let h = 2166136261; for (let i = 0; i < id.length; i++) h = Math.imul(h ^ id.charCodeAt(i), 16777619); return h | 0; };
let MACH_LIST = null;
function machineList() {
  if (MACH_LIST) return MACH_LIST;
  MACH_LIST = [];
  for (const n of Object.keys(DECKS).map(Number).sort()) {
    if (n === 7 && !REC_DECK) continue;                 // 0.84.0: a dormant rec deck has no machines (nothing wears, posts or sends crew down)
    const own = (DECKS[n].machines || []).map(m => ({ ...m })), ids = new Set(own.map(m => m.id)), rooms = new Set(own.map(m => m.room));
    const list = own.concat((STUB_MACHINES[n] || []).filter(([id, , room]) => !ids.has(id) && !rooms.has(room))
      .map(([id, kind, room]) => { const at = room ? machRoomTile(n, room) : DECKS[n].lift.slice(); return { id, kind, at, room, face: 's', panel: at, stub: true }; }));
    for (const m of list) if (MACHINE_KINDS[m.kind]) MACH_LIST.push({ ...m, deck: n, seed: machSeed(m.id) });
  }
  return MACH_LIST;
}
const machineById = id => machineList().find(m => m.id === id);

// ---- use, from the schedules: per ship hour of a day, how much of each thing happened (cached, last few days) ----
//   meal: meals begun; cook: people cooking (galleyCooks, section 16), or before that meals this hour and next;
//   ride: lift rides; water: showers (1) and other washes, toilets and hand-washing (.25 each); loads: laundry
//   visits plus yesterday's shift uniforms (washed 06:00-10:00); heads[n]: person-hours on deck n; garden:
//   person-hours in the garden. Read from shipDay(d) (and the galley rota), so it's the same however often it's asked.
const MACH_USE = new Map();
function machUseDay(d) {
  if (MACH_USE.has(d)) return MACH_USE.get(d);
  const B = (d - 1) * 1440, z = () => new Float32Array(24);
  const u = { meal: z(), cook: z(), ride: z(), water: z(), loads: z(), garden: z(), heads: {} };
  for (const n of Object.keys(DECKS)) u.heads[n] = z();
  const { plans, occ } = shipDay(d), byId = schedData().byId;
  if (occ.use) return occ.use;                           // a provisional plan's use, worked out once (planning it again makes a new occ; R8's fix, RE20 0.64.1)
  let workedYesterday = 0;
  for (const p of schedPeople()) if (isWorkDay(p, d - 1)) workedYesterday++;
  for (const segs of plans.values()) for (const s of segs) {
    const h = Math.floor((s.from - B) / 60);
    if (s.from >= B && h < 24) {
      if ((s.act === 'breakfast' || s.act === 'dinner') && s.tag !== 'queue') u.meal[h]++;
      if (s.act === 'commute') u.ride[h]++;
      if (s.act === 'wash') u.water[h] += s.type === 'shower' ? 1 : .25;
      if (s.tag === 'laundry') u.loads[h]++;
    }
    const pl = s.placeId && byId.get(s.placeId);
    for (let m = Math.max(s.from, B); m < Math.min(s.to, B + 1440);) {
      const h2 = Math.floor((m - B) / 60), e = Math.min(s.to, B + (h2 + 1) * 60);
      if (u.heads[s.deck]) u.heads[s.deck][h2] += (e - m) / 60;
      if (pl && pl.type === 'garden') u.garden[h2] += (e - m) / 60;
      m = e;
    }
  }
  if (typeof galleyCooks === 'function') for (let m = 0; m < 1440; m++) u.cook[Math.floor(m / 60)] += galleyCooks(B + m) / 60;
  else for (let h = 0; h < 24; h++) u.cook[h] = u.meal[h] + (h < 23 ? u.meal[h + 1] : 0);
  for (let h = 6; h < 10; h++) u.loads[h] += workedYesterday / 4 / 6;           // a load holds about six uniforms
  if (occ.recAt != null && !occ.recSet) return occ.use = u;   // a plan to be made again (recPlanShut): not kept (RC, 0.64.1)
  MACH_USE.set(d, u);
  for (const k of MACH_USE.keys()) if (k < d - 3 || k > d + 1) MACH_USE.delete(k);
  return u;
}
// an average day's use of each counter (heads per deck): the mean of days 1-7, worked out once. Use is measured
// against it, so a machine wears at its `life` on an average day however busy the schedules make the ship.
// Working it out plans seven days (about 80 ms), so it's done a day at a time in the background soon after load
// (machNormWarm), and kept in the save for this build; a read before it's done finishes it there and then. The
// days are added in the same order either way, so the result is exactly the same.
let MACH_NORM = null, MACH_NORM_PART = null;
function machNormStep() {                               // one more day of the average; true once it's done
  if (MACH_NORM) return true;
  const P = MACH_NORM_PART || (MACH_NORM_PART = { d: 1, norm: { heads: {} } }), norm = P.norm, sum = a => a.reduce((x, y) => x + y, 0) / 7;
  const u = machUseDay(P.d++);
  for (const k in u) if (k === 'heads') { for (const n in u.heads) norm.heads[n] = (norm.heads[n] || 0) + sum(u.heads[n]); } else norm[k] = (norm[k] || 0) + sum(u[k]);
  if (P.d > 7) { MACH_NORM = norm; MACH_NORM_PART = null; return true; }
  return false;
}
function machNorm() { while (!machNormStep()); return MACH_NORM; }
function machNormWarm() { try { if (!machNormStep()) setTimeout(machNormWarm, 40); } catch (e) { /* tried again on first use */ } }
setTimeout(machNormWarm, 300);                           // after the whole script has run (it reads the roster and places)
// how hard machine m was used in absolute ship hour h, against an average day (1 = an average hour)
function machUse(m, h) {
  const K = MACHINE_KINDS[m.kind];
  if (!K.use || K.time >= 1) return 1;
  const u = machUseDay(Math.floor(h / 24) + 1), i = (h % 24 + 24) % 24, N = machNorm();   // day 0's hours are negative (0.26.31)
  const v = K.use === 'heads' ? u.heads[m.deck][i] : u[K.use][i], nm = K.use === 'heads' ? N.heads[m.deck] : N[K.use];
  return nm > 0 ? v * 24 / nm : 1;
}
// one hour's wear for machine m at condition c: its life's share of the hour, split between time and use,
// faster as it wears (up to half as fast again near 0), with a little variety from the hour
function machWear(m, h, c) {
  const K = MACHINE_KINDS[m.kind];
  const base = 100 / (K.life * 24), use = K.time + (1 - K.time) * machUse(m, h);
  return base * use * (1 + .5 * (1 - c / 100)) * (.6 + .8 * schedU(m.seed, h, 7)) * eventWear(K.sys, h) * eventWear(m.kind, h);
}
// a ship-wide event's wear (Pillar 3, C7: section 18's eventMod('wear', key, minute) -> a multiplier, null for no
// change; pure for any minute, so the machines catching up see the event as it was). key: a system ('power') or a
// machine kind ('chiller'); machWear asks both. 1 with no event
function eventWear(key, h) {
  if (typeof eventMod !== 'function') return 1;
  const v = eventMod('wear', key, h * 60);
  return typeof v === 'number' && v > 0 && v < 20 ? v : 1;
}

// ---- the machines' state: SHIP.machines[id] = { cond, state, lastService }, brought up to date hour by hour ----
SHIP.machines = {};
SHIP.upkeep = {};                                        // the ship meters' upkeep left undone, by system (0.33.57; machinesReset fills it)
const CART_RUNS = new Map(), CART_PENDING = [];         // food runs set by cartClaim (by hour), and those not yet on the job list
// ship notes from section 17 (simNote, section 13's bus) wait here and go out once the hours have run or your action is
// done (simFlush), never from inside jobsHour: a listener may read the jobs or the schedules
const SIM_Q = [];
// each stamped with when it happened: the hour being run (SIM_AT, set by machinesNow's loop), else now (your own actions)
let SIM_AT = null;
const simLater = (kind, d) => { if (typeof simNote === 'function') SIM_Q.push([kind, { ...(d || {}), t: d && Number.isFinite(d.t) ? d.t : SIM_AT != null ? SIM_AT : shipNow() }]); };
function simFlush() { while (SIM_Q.length) { const [k, d] = SIM_Q.shift(); simNote(k, d); } }
let MACH_HOUR = null, MACH_SEEN = -1, MACH_REV = 0;     // the first ship hour not yet run; the last time asked; a counter of changes
const machFresh = m => Math.round((70 + 30 * schedU(m.seed, 0, 1)) * 10) / 10;   // a new game: 70-100, a few already worn
function machinesReset(hour) {
  SHIP.machines = {};
  for (const m of machineList()) { const c = machFresh(m); SHIP.machines[m.id] = { cond: c, state: machineState(c), lastService: null }; }
  jobsReset(); MACH_HIST.clear(); MACH_HOUR = hour; MACH_REV++; SHIP.upkeep = { ...UPKEEP_START };
  for (const [k, v] of SHIP_DAYS) if (v.occ.recAt != null) { SHIP_DAYS.delete(k); MACH_USE.delete(k); }   // plans that read the old record (recPlanShut; RC, 0.64.1)
  SHIP.short = {}; for (const k in MACH_EXTRA) delete MACH_EXTRA[k]; for (const k in MACH_RUN) delete MACH_RUN[k];
}
// a new game (section 13's newGameStart, 0.26.31): the machines and jobs start afresh at once, whichever way the clock
// moved, so the old game's jobs never carry over and jobs reserved right after (section 21) aren't wiped by a rewind
function machinesNew() {
  machinesReset(Math.floor(shipNow() / 60)); MACH_SEEN = shipNow(); LIFT_STUCK = null;
  CART_RUNS.clear(); CART_PENDING.length = 0; SIM_Q.length = 0;
}
// run the ship's hours up to and including this one: each hour, the jobs (jobsHour), then that hour's wear.
// A clock earlier than the machines' (New game) starts afresh
let MACH_IN = false;                                     // inside the hour loop: a call from jobsHour's hooks (ladderTick) reads as it stands (0.33.45)
// a loaded save's jobs of a kind this build doesn't have (a sub-block left out) are dropped, once, at the first run: by then
// section 24 has registered its kinds (0.33.47)
let JOBS_TIDY = false;
function jobsTidy() { JOBS_TIDY = true; SHIP.jobs = SHIP.jobs.filter(j => j.kind === 'restock' || j.kind === 'favour' || j.kind === 'chore' || !!JOB_KINDS[j.kind] || (j.kind in JOB_TYPES && !!j.machine)); }
function machinesNow() {
  if (MACH_IN) return SHIP.machines;
  if (!JOBS_TIDY) jobsTidy();
  const t = shipNow();
  if (CART_PENDING.length && MACH_HOUR !== null && MACH_HOUR * 60 > t) cartPost();
  if (MACH_HOUR !== null && t >= MACH_SEEN && MACH_HOUR * 60 > t) { MACH_SEEN = t; return SHIP.machines; }   // up to date: the common case
  const now = Math.floor(shipNow() / 60), start = Math.floor(((SHIP_START.day - 1) * 1440 + SHIP_START.min) / 60);
  if (MACH_HOUR === null || shipNow() < MACH_SEEN) machinesReset(Math.min(start, now));
  MACH_SEEN = shipNow();
  const list = machineList();
  for (const m of list) if (!SHIP.machines[m.id]) { const c = machFresh(m); SHIP.machines[m.id] = { cond: c, state: machineState(c), lastService: null }; }
  if (now >= MACH_HOUR) MACH_REV++;
  MACH_IN = true;
  try { for (; MACH_HOUR <= now; MACH_HOUR++) {
    SIM_AT = MACH_HOUR * 60;                             // notes from this hour say so, however late they go out
    if (JOBS_ON) jobsHour(MACH_HOUR);
    for (const m of list) {
      const s = SHIP.machines[m.id];
      s.cond = Math.max(0, s.cond - machWear(m, MACH_HOUR, s.cond) * (1 + .1 * Math.abs(s.drift || 0)) - (MACH_EXTRA[m.id] || 0));
      s.state = machineState(s.cond);
      driftHour(m, s, MACH_HOUR);
    }
    machRecord(MACH_HOUR); upkeepHour();
    for (const k in MACH_EXTRA) delete MACH_EXTRA[k];
  } } finally { MACH_IN = false; }
  SIM_AT = null;
  if (CART_PENDING.length) cartPost();
  simFlush();
  return SHIP.machines;
}
// put a machine right: condition back to `to` (100: as new), serviced now
function serviceMachine(id, to = 100) {
  const s = machinesNow()[id]; if (!s) return false;
  s.cond = Math.max(s.cond, Math.min(100, to)); s.state = machineState(s.cond); s.lastService = shipNow(); machRecord(MACH_HOUR - 1); MACH_REV++;
  return true;
}

// ---- systems and ship health ----
// how well a machine does its job at a condition: fully while healthy, nearly while worn, badly when faulty,
// hardly when failing, not at all when broken (a straight line between these points)
const MACH_WORKS = [[0, 0], [10, 20], [25, 50], [50, 85], [75, 100], [100, 100]];
function machWorks(c) {
  for (let i = 1; i < MACH_WORKS.length; i++) { const [a, x] = MACH_WORKS[i - 1], [b, y] = MACH_WORKS[i]; if (c <= b) return x + (y - x) * (c - a) / (b - a); }
  return 100;
}
// drift (0.33.48, plans/mechanics/m5-tuning.html): a tunable machine's setting wanders. SHIP.machines[id].drift, -3..+3 (0 or
// missing: settled). From TUNE_FROM (Day 4 06:00), and only once section 24e's 'tune' job kind is in the build (with
// no way to settle it, a drift would stay for ever), each ship hour a settled one drifts when schedU(seed, hour, 868) <
// TUNE_P (about one a day ship-wide over the ten tunable machines) by 1-3 either way (key 869). A drift of 2 or more posts
// a 'tune' job (found 1-6 hours later); a calibrate chore on any drifted machine becomes its tune job. A drifted machine
// works DRIFT_COND condition points lower per step (machEff: the systems, effects and the hour's record) and wears 10%
// faster per step; its look: high flickers (blinks, a cart dock), low dims. tuneSet(id, v) sets it (clamped; MACH_REV++;
// simNote('tuned', { machine }) when it settles); machineDrift(id)
const TUNABLE = new Set(['oven', 'range', 'lights', 'cartdock']), TUNE_FROM = 3 * 1440 + 360, TUNE_P = .007, DRIFT_COND = 8;
const TUNE_LEAVE = 120;                                 // a tune job is held for you two hours of the shift, then the crew's (0.33.54, M2: "a drifted machine never waits on you")
const driftOn = () => !!JOB_KINDS.tune;
const machEff = s => Math.max(0, s.cond - DRIFT_COND * Math.abs(s.drift || 0));
const machineDrift = id => { const s = SHIP.machines[id]; return s && s.drift || 0; };
function tuneSet(id, v) {
  const s = SHIP.machines[id], m = machineById(id); if (!s || !m || !(TUNABLE.has(m.kind) || s.drift && Math.round(v) === 0) || !Number.isFinite(v)) return false;   // any drift can be settled (0.33.58: the test job's fan)
  const was = s.drift || 0, d = Math.max(-3, Math.min(3, Math.round(v)));
  if (d) s.drift = d; else delete s.drift;
  MACH_REV++; if (MACH_HOUR !== null) machRecord(MACH_HOUR - 1);   // the effects follow at once
  if (was && !d && typeof simNote === 'function') simNote('tuned', { machine: id, t: shipNow() });
  return true;
}
// one hour's drift for a machine (in the hour loop, after its wear)
function driftHour(m, s, h) {
  if (s.drift || !TUNABLE.has(m.kind) || h * 60 < TUNE_FROM || !driftOn() || schedU(m.seed, h, 868) >= TUNE_P) return;
  const u = schedU(m.seed, h, 869); s.drift = (u < .5 ? -1 : 1) * (1 + Math.floor((u * 2 % 1) * 3));
}
// the conditions now, as { id: cond } (the systems and effects are worked out from one of these); a drifted machine counts lower (0.33.48)
function machConds() { const st = machinesNow(), c = {}; for (const id in st) c[id] = machEff(st[id]); return c; }
// a system's own score: how well its machines work, weighted, pulled toward the worst of them
function systemOwn(sys, c) {
  const ms = machineList().filter(m => MACHINE_KINDS[m.kind].sys === sys);
  if (!ms.length) return 100;
  let a = 0, w = 0, lo = 100;
  for (const m of ms) { const x = machWorks(c[m.id] ?? 100), k = MACHINE_KINDS[m.kind].w; a += x * k; w += k; lo = Math.min(lo, x); }
  return .6 * a / w + .4 * lo;
}
// every system with the dependencies: power feeds everything but the hull; water feeds the garden and the garden
// the galley (food); waste and laundry need water too. A feeding system only drags the others down once it's below 75.
function systemsFrom(c) {
  const own = {}; for (const s of SYSTEMS) own[s] = systemOwn(s, c);
  const pf = Math.min(1, .5 + .5 * own.power / 75), wf = Math.min(1, own.water / 75), r = x => Math.round(x * 10) / 10;
  const out = { power: r(own.power) };
  for (const s of SYSTEMS) if (s !== 'power' && s !== 'hull') out[s] = own[s] * pf;
  out.food *= .7 + .3 * wf; out.waste *= .8 + .2 * wf; out.hull = own.hull;
  for (const s of SYSTEMS) out[s] = r(out[s]);
  return out;
}
const shipSystems = () => systemsFrom(machConds());
function shipHealth(sys = shipSystems()) {
  let a = 0, w = 0; for (const s of SYSTEMS) { a += sys[s] * SYSTEM_W[s]; w += SYSTEM_W[s]; }
  return Math.round(a / w * 10) / 10;
}

// ---- consequences: what a faltering machine does to the people on a deck ----
// Each kind's effect at full strength (broken); faulty is felt at .35 of it and failing at .7, a worn machine not
// at all (design doc, "Consequences": minor, noticeable, serious). Several machines of a kind count by their
// average (one broken washer of four is a quarter of the trouble). Multipliers: restore = how much an action
// gives back (a shower's hygiene), drain = how fast a need runs down, walk = walking speed, cook = cooking time,
// lift = ride time, spoil = how fast the cold store's food spoils. mood = points off a 0-100 mood. local: felt
// only on the machine's own deck.
// the decks a branch machine feeds (the air line's dampers: architect-air-line.html)
const MACH_BRANCH = { '5-damper-1': [1, 2, 3], '5-damper-2': [4, 5, 6] };
const MACHINE_FX = {
  oven:        { cook: .5, restore: { hunger: .15 }, mood: 2, text: 'Meals run late' },
  range:       { cook: .4, restore: { hunger: .1 }, mood: 2, text: 'Meals run late' },
  galleyplant: { cook: .25, mood: 2, text: 'The galley is hot and smoky' },
  extractor:   { cook: .25, mood: 2, text: 'The galley is hot and smoky' },
  chiller:     { spoil: 1, mood: 1, text: 'The cold store runs warm' },
  washer:      { drain: { hygiene: .3 }, mood: 4, text: 'Uniforms come back grubby' },
  lift:        { lift: 1, mood: 2, text: 'The lift runs slow' },
  lights:      { walk: .12, mood: 3, text: 'The lights flicker and dim' },
  junction:    { walk: .06, mood: 2, text: 'The power browns out', local: true },
  powerjunction: { walk: .06, mood: 2, text: 'The power browns out', local: true },   // Deck 6's lights hang off its junctions
  scrubber:    { drain: { energy: .4 }, mood: 6, text: 'The air is stuffy' },
  airplant:    { drain: { energy: .25 }, mood: 4, text: 'The air is stale everywhere' },
  fan:         { drain: { energy: .15 }, mood: 2, text: 'The air hardly moves' },
  heater:      { restore: { energy: .3 }, mood: 5, text: 'Cold cabins' },
  manifold:    { restore: { hygiene: .2 }, mood: 2, text: 'The water runs lukewarm and the pipes knock' },
  recycler:    { restore: { hygiene: .4 }, mood: 4, text: 'Showers run weak' },
  filter:      { restore: { hygiene: .2 }, mood: 2, text: 'The water runs cloudy' },
  pump:        { restore: { hygiene: .4 }, mood: 3, text: 'Showers run weak' },
  valve:       { mood: 1, text: 'A pipe drips somewhere' },
  damper:      { mood: 1, text: 'The duct air is weak', branch: true },   // as the valves, on its branch's decks only (MACH_BRANCH)
  o2cell:      { drain: { energy: .2 }, mood: 3, text: 'The air feels thin' },
  electrolyser: { drain: { energy: .15 }, mood: 2, text: 'The air feels thin' },
  heatpump:    { restore: { energy: .15 }, mood: 2, text: 'The radiators run lukewarm' },
  uv:          { mood: 2, text: 'The water tastes of chlorine' },
  irrigation:  { mood: 2, text: 'The garden droops' },
  nutrient:    { mood: 2, text: 'The garden wilts' },
  growlight:   { mood: 1, text: 'The garden lights are dim' },
  relay:       { mood: 1, text: 'Bridge stations flicker', local: true },
  databus:     { mood: 1, text: 'Bridge stations flicker', local: true },
};
const STAGE = { faulty: 'minor', failing: 'noticeable', broken: 'serious' };
// the effects on `deck` of conditions `c` ({ id: cond }; null: everything as new)
function fxFrom(deck, c) {
  const one = () => ({ hunger: 1, energy: 1, hygiene: 1, fitness: 1, social: 1 });
  const fx = { deck, restore: one(), drain: one(), walk: 1, cook: 1, lift: 1, spoil: 1, mood: 0, health: 100, notes: [] };
  if (!c) return fx;
  const groups = new Map();                             // kind -> machines whose effects reach this deck
  for (const m of machineList()) {
    const F = MACHINE_FX[m.kind]; if (!F) continue;
    if ((MACHINE_KINDS[m.kind].scope === 'deck' || F.local) && m.deck !== deck) continue;
    if (F.branch && MACH_BRANCH[m.id] && !MACH_BRANCH[m.id].includes(deck)) continue;   // a duct damper reaches its own decks (0.33.55)
    if (!groups.has(m.kind)) groups.set(m.kind, []); groups.get(m.kind).push(m);
  }
  const stateOf = id => machineState(c[id] ?? 100);
  for (const [kind, ms] of groups) {
    const F = MACHINE_FX[kind], sev = ms.reduce((a, m) => a + MACHINE_SEV[stateOf(m.id)], 0) / ms.length;
    if (!sev) continue;
    for (const k in F.restore || {}) fx.restore[k] *= 1 - F.restore[k] * sev;
    for (const k in F.drain || {}) fx.drain[k] *= 1 + F.drain[k] * sev;
    if (F.walk) fx.walk *= 1 - F.walk * sev;
    if (F.cook) fx.cook *= 1 + F.cook * sev;
    if (F.lift) fx.lift *= 1 + F.lift * sev;
    if (F.spoil) fx.spoil *= 1 + F.spoil * sev;
    fx.mood -= F.mood * sev;
    for (const m of ms) { const st = stateOf(m.id); if (STAGE[st]) fx.notes.push({ machine: m.id, kind, state: st, stage: STAGE[st], text: F.text }); }
  }
  // the ship as a whole: low power dims every deck, and a run-down ship gets everyone down (serious)
  const sys = systemsFrom(c), health = shipHealth(sys);
  if (sys.power < 50) { fx.walk *= 1 - .1 * (1 - sys.power / 50); fx.notes.push({ machine: null, kind: 'power', state: null, stage: 'noticeable', text: 'Power is low; the ship is dim' }); }
  if (health < 70) fx.mood -= 10 * (70 - health) / 70;
  fx.mood = Math.max(-30, Math.round(fx.mood * 10) / 10);
  fx.health = health;
  return fx;
}
// shipEffects(deck): the effects now. It brings the machines up to the present first (machinesNow), as any read
// does; don't call it while the schedules are being planned (the plans feed the wear).
// shipEffectsAt(deck, t): the effects at ship minute t, from the hour-by-hour record of the last 8 days. Pure: it
// never runs the machines. Hours after the last one run use the latest; hours before the record use its first;
// with no record at all (nothing has asked yet, as under ?nosave) everything is as new. For anything replayed
// over past times (the crew's paper needs, the galley's minute-by-minute food).
let FX_CACHE = new Map(), FX_REV = -1;
function shipEffects(deck) {
  machinesNow();
  if (FX_REV !== MACH_REV) { FX_CACHE = new Map(); FX_REV = MACH_REV; }
  if (!FX_CACHE.has(deck)) FX_CACHE.set(deck, fxFrom(deck, machConds()));
  const fx = FX_CACHE.get(deck);
  return liftStuckNow() ? { ...fx, lift: fx.lift * LIFT_STUCK_X } : fx;   // a stuck lift (m6's incident, 0.33.49)
}
// incidents' machine side (0.33.49, plans/mechanics/m6-incidents.html; section 24f runs the incident). machineFault(id, cond =
// 40): a machine set faulty when its incident starts (never raised; its repair is posted by the hour's jobs as any fault's,
// and machineFound finds it at once). liftStuck(on, until?): the lift's rides LIFT_STUCK_X slower while it's stuck (till
// `until`, default 40 minutes on; not saved: 24f calls it again after a load). jointJobPost({ deck, placeId, title?,
// leave?, reserved? }) -> job id: the burst's fix, a Tier 1 joint job at the burst (a seal, 20 minutes), posted now
const LIFT_STUCK_X = 3;
let LIFT_STUCK = null;
const liftStuckNow = () => LIFT_STUCK !== null && shipNow() < LIFT_STUCK;
function liftStuck(on, until) { LIFT_STUCK = on ? (Number.isFinite(until) ? until : shipNow() + 40) : null; MACH_REV++; return liftStuckNow(); }
function machineFault(id, cond = 40) {
  machinesNow(); const s = SHIP.machines[id]; if (!s || !Number.isFinite(cond)) return false;
  s.cond = Math.min(s.cond, Math.max(0, cond)); s.state = machineState(s.cond); MACH_REV++; if (MACH_HOUR !== null) machRecord(MACH_HOUR - 1);
  return true;
}
function jointJobPost(o = {}) {
  machinesNow(); const pl = placeById(o.placeId); if (!pl) return null;
  const t = shipNow(), id = 'chore-joint:' + pl.id + '@' + Math.floor(t);
  if (SHIP.jobs.some(j => j.id === id)) return id;
  SHIP.jobs.push({ id, machine: null, deck: pl.deck, room: pl.room, kind: 'chore', chore: 'joint', target: pl.id, title: o.title || 'Replace a burst joint: ' + (roomName(pl.deck, pl.room) || 'corridor'),
                   bring: null, tier: 1, stops: [{ deck: pl.deck, placeId: pl.id, mins: 20, tag: 'joint' }], urgency: 1, leave: o.leave || null, posted: t, found: t, claimedBy: null,
                   parts: ['seal'], status: 'open', ...(o.reserved ? { reserved: o.reserved } : {}), ...(o.incident ? { incident: o.incident } : {}) });
  MACH_REV++; return id;
}
const MACH_HIST = new Map(), MACH_HIST_DAYS = 8;          // hour -> { id: cond } once that hour has run
let FX_AT = new Map(), FX_AT_REV = -1;
function machRecord(h) {
  const c = {}; for (const id in SHIP.machines) c[id] = machEff(SHIP.machines[id]);
  MACH_HIST.set(h, c);
  for (const k of MACH_HIST.keys()) if (k < h - MACH_HIST_DAYS * 24) MACH_HIST.delete(k); else break;
}
// the recorded hour to read for minute t: its own, else the latest before it, else the record's first
function histHour(t) {
  let h = Math.floor(t / 60);
  if (!MACH_HIST.has(h) && MACH_HIST.size) { const ks = [...MACH_HIST.keys()]; h = h < ks[0] ? ks[0] : Math.min(h, ks[ks.length - 1]); if (!MACH_HIST.has(h)) h = ks.filter(k => k <= h).pop(); }
  return h;
}
function shipEffectsAt(deck, t) {
  if (FX_AT_REV !== MACH_REV) { FX_AT = new Map(); FX_AT_REV = MACH_REV; }
  const h = histHour(t), key = deck + '|' + h;
  if (!FX_AT.has(key)) FX_AT.set(key, fxFrom(deck, MACH_HIST.get(h) || null));
  return FX_AT.get(key);
}
// what crew notice on the rec deck (0.84.2, rec engineer B; plans/recdeck-plan.html section 6). recShutAt(t) -> { pool, river, belays,
// route, court, board, float, lights, mic } at ship minute t: pool null | 'cloudy' (a filter) | 'sting' (the dosing) | 'cold' (the heat),
// the first of those that's faulty or worse (under 50, machineState); river null | 'slack' (a pump) | 'flat' (the wave gate); belays,
// how many auto-belays work (0-2); route 0-3, the route roped off while the holds want their chore (fixed till they're serviced), or
// null; court, the emitters down (no Lightdisc); board null | 'pixels' (faulty) | 'nonsense' (failing or worse); float, the gravity
// plates down (the float room shut); lights null | 'dim' | 'flicker' the board's way; mic, the sound rack down. Pure, like
// shipEffectsAt: the hour-by-hour record (histHour), never machinesNow, so the schedules may ask while planning; cached on MACH_REV
// and the hour; frozen (don't change it). All clear with no rec machines (REC_DECK off) or no record. recShut(): now (machinesNow first)
const REC_OK = Object.freeze({ pool: null, river: null, belays: 2, belayOff: Object.freeze([false, false]), route: null, court: false, board: null, float: false, lights: null, mic: false });   // belayOff (0.84.12): belay 1, belay 2 tagged out (belay n is over route n)
let REC_SHUT = new Map(), REC_SHUT_REV = -1;
function recShutAt(t) {
  if (!REC_DECK) return REC_OK;
  if (REC_SHUT_REV !== MACH_REV) { REC_SHUT = new Map(); REC_SHUT_REV = MACH_REV; }
  const h = histHour(t); if (REC_SHUT.has(h)) return REC_SHUT.get(h);
  const c = MACH_HIST.get(h); if (!c) { REC_SHUT.set(h, REC_OK); return REC_OK; }
  const cd = id => Number.isFinite(c[id]) ? c[id] : 100, bad = id => cd(id) < 50, lvl = id => !bad(id) ? 0 : cd(id) < 25 ? 2 : 1;
  const hs = SHIP.machines['7-wall-holds'], ls = hs && Number.isFinite(hs.lastService) ? Math.floor(hs.lastService / 60) : 0;
  const r = Object.freeze({ pool: bad('7-pool-filter-1') || bad('7-pool-filter-2') ? 'cloudy' : bad('7-pool-dosing') ? 'sting' : bad('7-pool-heat') ? 'cold' : null,
    river: bad('7-river-pump-1') || bad('7-river-pump-2') ? 'slack' : bad('7-wave-gate') ? 'flat' : null,
    belays: (bad('7-belay-1') ? 0 : 1) + (bad('7-belay-2') ? 0 : 1), belayOff: Object.freeze([bad('7-belay-1'), bad('7-belay-2')]), route: bad('7-wall-holds') ? ((machSeed('7-wall-holds') ^ ls) >>> 0) % REC_ROUTES : null,
    court: bad('7-court-net'), board: [null, 'pixels', 'nonsense'][lvl('7-court-board')], float: bad('7-grav-plates'),
    lights: [null, 'dim', 'flicker'][lvl('7-aud-lights')], mic: bad('7-aud-sound') });
  REC_SHUT.set(h, r); return r;
}
function recShut() { machinesNow(); return recShutAt(shipNow()); }
// the rec deck as the crew's plans for day d see it (RC, 0.64.1; BM9's find): recShutAt at 22:00 the evening before (hour
// (d - 1) * 24 - 2), settled once the 23:00 hour has run (a repair rewrites the hour before the one running), so a day's
// plan never depends on when it was made. Not settled yet (a day planned the day before, as the jobs and the evening
// Mail do, a new game's first day, the days before a load): all clear, and the plan is made again once it is (occ.recAt,
// occ.recSet; machUseDay doesn't keep its use till then). machinesReset drops the plans that read the old record
const recSettled = h => MACH_HOUR !== null && h <= MACH_HOUR - 2 && MACH_HIST.has(h);
function recPlanShut(d, occ) {
  if (!REC_DECK) return REC_OK;
  const h = (d - 1) * 24 - 2, ok = recSettled(h); if (occ) { occ.recAt = h; occ.recSet = ok; }
  return ok ? recShutAt(h * 60) : REC_OK;
}
// one machine, for the job board and the device (B2): its definition, kind and state together
function machineInfo(id) {
  const m = machineById(id); if (!m) return null;
  return { ...m, ...MACHINE_KINDS[m.kind], ...machinesNow()[id] };
}

// ---- what the machines look like, and the ship's health board (0.33.17: answers 2, 3, 7 and 22) ----
// machineLook(id) -> { state, blink, dim, drip, flicker, running, cond, kind }, for deck dressing and effects (the
// architects and the performance engineer draw it): state 'fine' (healthy) | 'worn' | 'poor' (faulty) | 'failing'
// (failing or broken); dim 0-1, how far its screens and lamps dim; blink, a failing panel's warm-red blink; drip, a
// water machine leaking (poor or worse); flicker 0-1, how often the lights it feeds flicker (light relays, power
// junctions, bridge relays); running, started by a tap (machineUse) and still going. null for an unknown id.
// deckLook(deck) -> { dim, flicker, spray, wilt, drip }: the signs a whole deck shows, from shipEffects: lights
// dimmed and flickering, shower spray (1 = full, weaker below), garden plants wilting (0-1), pipes dripping.
// Both read the machines now (machinesNow) and are cached until anything changes; ask once a ship minute, not
// every frame, and never from inside the schedules' planning.
const LOOK_OF = { healthy: 'fine', worn: 'worn', faulty: 'poor', failing: 'failing', broken: 'failing' };
const LOOK_DIM = { fine: 0, worn: .15, poor: .35, failing: .65 };
const LOOK_WET = new Set(['recycler', 'filter', 'pump', 'uv', 'valve', 'irrigation', 'manifold', 'heatpump', 'poolfilter', 'poolheat', 'riverpump', 'wavegate']);   // the rec deck's from 0.84.1
const LOOK_LIT = { lights: 1, junction: .6, powerjunction: .6, relay: .5, databus: .4, stagelights: 1, courtnet: .6, scoreboard: .5, gravplate: .4 };   // the rec deck's from 0.84.1
let LOOKS = new Map(), LOOKS_REV = -1;
const MACH_RUN = {};                                     // id -> ship minute a tap-started run ends (machineUse)
function machineLook(id) {
  const st = machinesNow()[id], m = st && machineById(id); if (!m) return null;
  if (LOOKS_REV !== MACH_REV) { LOOKS = new Map(); LOOKS_REV = MACH_REV; }
  const running = (MACH_RUN[id] || 0) > shipNow();
  const key = id + (running ? '+' : ''); if (LOOKS.has(key)) return LOOKS.get(key);
  const state = LOOK_OF[st.state], bad = state === 'poor' ? .35 : state === 'failing' ? (st.state === 'broken' ? 1 : .7) : 0;
  const look = { state, blink: state === 'failing', dim: LOOK_DIM[state], drip: LOOK_WET.has(m.kind) && bad > 0 || (m.kind === 'valve' && state === 'worn'),
                 flicker: Math.round((LOOK_LIT[m.kind] || 0) * bad * 100) / 100, running, cond: Math.round(st.cond), kind: m.kind };
  const dr = st.drift || 0;                              // a drifted setting shows (0.33.48): high flickers (a dock blinks), low dims
  if (dr) { look.drift = dr; if (dr > 0 && m.kind === 'cartdock') look.blink = true; else if (dr > 0) look.flicker = Math.max(look.flicker, Math.round(.2 * dr * 100) / 100); else look.dim = Math.max(look.dim, .12 * -dr); }
  LOOKS.set(key, look); return look;
}
function deckLook(deck) {
  const fx = shipEffects(deck);
  if (LOOKS_REV !== MACH_REV) { LOOKS = new Map(); LOOKS_REV = MACH_REV; }
  const bo = blackoutAt(shipNow()), dark = !!bo && bo.deck === deck;
  const key = 'deck' + deck + (dark ? ':dark' : ''); if (LOOKS.has(key)) return LOOKS.get(key);
  let flicker = 0, drip = false, wilt = 0;
  for (const m of machineList()) {
    const L = machineLook(m.id); if (!L) continue;
    if (L.flicker && m.deck === deck) flicker = Math.max(flicker, L.flicker);
    if (L.drip && m.deck === deck) drip = true;
    if ((m.kind === 'irrigation' || m.kind === 'nutrient' || m.kind === 'growlight') && m.deck === deck) wilt = Math.max(wilt, MACHINE_SEV[machinesNow()[m.id].state]);
  }
  const look = { dim: Math.round((1 - fx.walk) * 300) / 100, flicker, spray: Math.round(fx.restore.hygiene * 100) / 100, wilt, drip, dark };
  look.dim = Math.min(1, look.dim);
  LOOKS.set(key, look); return look;
}
// the "Ship health" board (the bridge, Deck 1, and the Works bay, Deck 5; the architects draw it): the ship first,
// then each system, worst first. shipHealthRows() -> [{ key, name, value 0-100, state, worst }]: state as
// machineLook's; worst: the system's worst machine that isn't fine, as 'Air scrubber 2, Deck 4', or null
const SYSTEM_NAME = { air: 'Air', water: 'Water', power: 'Power', heat: 'Heat', food: 'Galley and food', waste: 'Waste and laundry', hull: 'Hull',
                      comms: 'Comms and sensors', propulsion: 'Drive', transport: 'Lift and doors', rec: 'Rec deck' };
// ---- the ship meters (0.33.57, Pillar 5 Step 3; the user, 2026-10-18: ship health "starts a little lower, so you can see your
// impact", and every job you do helps at least one meter, often several) ----
// A meter is a Ship health board row: its system's score from the machines (shipSystems, which every effect reads, as
// before) less its upkeep, SHIP.upkeep[sys]: points of small upkeep left undone (scuffed panels, dusty ducts, loose
// fittings) that the machines' effects never feel. A new game starts with UPKEEP_START (ship health about 75: most systems
// worn, a few fine, none failing); upkeep builds up again UPKEEP_CREEP points a day per system (a share each ship hour, up
// to UPKEEP_CAP), and each job you do takes a step off its systems (UPKEEP_STEP by size: [main, each related]): its main
// system (a registered kind's def.sys, else its machine's, else its stops' machines', else JOB_SYS by kind) and the
// related ones (SYS_RELATED); what they can't take (their upkeep all done) goes to the system with the most left.
// j.meters = [{ key, name, gain }] (biggest first, the main system first on a tie; gain: what the meter rose, upkeep and
// machine together, one decimal) is kept on the job for the turn-in (C2) and the panel's "+N" (U). The crew's jobs put machines
// right, as before, but leave the upkeep: that's what you add. shipMeters(sys?) -> { sys: 0-100 }. An older save starts
// with no upkeep (its meters read as before).
const UPKEEP_START = { air: 28, water: 30, power: 30, heat: 34, food: 8, waste: 32, hull: 6, comms: 30, propulsion: 4, transport: 30 };
const UPKEEP_CREEP = 1, UPKEEP_CAP = 40;
const UPKEEP_STEP = { small: [3, 2], repair: [5, 2], overhaul: [7, 3] };
const SYS_RELATED = { air: ['heat'], water: ['food', 'waste'], power: ['transport'], heat: ['air'], food: ['waste'], waste: ['water'],
  hull: ['air'], comms: ['power'], propulsion: ['power'], transport: ['power'] };
const JOB_SYS = { lamp: 'power', vent: 'air', delivery: 'transport', joint: 'water', restock: 'transport', haul: 'transport', drill: 'hull',
  rounds: 'power', incident: 'hull', garden: 'food', secure: 'hull', clean: 'waste', tea: 'food', check: 'hull', fetch: 'transport', carry: 'transport',
  set: 'hull', patch: 'hull', team: 'water' };
function shipMeters(sys = shipSystems()) { const out = {}; for (const k of SYSTEMS) out[k] = Math.round(Math.max(0, sys[k] - (SHIP.upkeep[k] || 0)) * 10) / 10; return out; }
function upkeepHour() { for (const k of SYSTEMS) SHIP.upkeep[k] = Math.min(UPKEEP_CAP, (SHIP.upkeep[k] || 0) + UPKEEP_CREEP / 24); }
// the systems a job helps: [main, ...related]
function jobMeterSys(j) {
  const K = jobKindOf(j), sysOf = id => { const m = id && machineById(id); return m ? MACHINE_KINDS[m.kind].sys : null; };
  let main = K && K.sys || sysOf(j.machine);
  if (!main) { const c = {}; for (const x of j.stops || []) { const pl = x.placeId && placeById(x.placeId), k = pl && sysOf(pl.machine); if (k) c[k] = (c[k] || 0) + 1; }
    main = Object.keys(c).sort((a, b) => c[b] - c[a] || SYSTEMS.indexOf(a) - SYSTEMS.indexOf(b))[0] || null; }
  if (!main) main = j.cargo === 'meals' ? 'food' : JOB_SYS[j.chore] || JOB_SYS[j.kind] || 'hull';
  return [main, ...(SYS_RELATED[main] || [])];
}
function meterStep(j, before) {
  const sys = jobMeterSys(j), [a, b] = UPKEEP_STEP[j.kind === 'repair' ? 'repair' : j.kind === 'overhaul' || j.kind === 'team' ? 'overhaul' : 'small'];
  const order = sys.slice(), up = k => SHIP.upkeep[k] || 0, take = (k, n) => { const x = Math.min(up(k), n); SHIP.upkeep[k] = up(k) - x; return n - x; };
  let left = 0; sys.forEach((k, i) => { left += take(k, i ? b : a); });
  while (left > 1e-9) {                                  // what its own systems can't take (their upkeep's done) goes where most is left
    const k = SYSTEMS.reduce((best, x) => up(x) > up(best) ? x : best, SYSTEMS[0]); if (!(up(k) > 0)) break;
    if (!order.includes(k)) order.push(k); left = take(k, left);
  }
  MACH_REV++;
  const after = shipMeters(), keys = order.concat(SYSTEMS.filter(k => !order.includes(k)));
  j.meters = keys.map(k => ({ key: k, name: SYSTEM_NAME[k], gain: Math.round((after[k] - before[k]) * 10) / 10 })).filter(x => x.gain >= .5).sort((x, y) => y.gain - x.gain || keys.indexOf(x.key) - keys.indexOf(y.key));
  return j.meters;
}
// the bridge room (Deck 1's 'B') is closed to you till you're invited (the user, 2026-10-18; C2's SHIP.bridgeInvited, false in
// older saves): no job there is offered to you or can be taken by you, unless it's held for you; the crew take them as before;
// the Wednesday manifest leaves the bridge's crate out till then (0.33.57)
const bridgeShut = () => !SHIP.bridgeInvited;
const inBridge = (deck, room) => deck === 1 && room === 'B';
function bridgeJob(j) {
  if (inBridge(j.deck, j.room)) return true;
  const m = j.machine && machineById(j.machine); if (m && inBridge(m.deck, m.room)) return true;
  for (const x of j.stops || []) { const pl = x.placeId && placeById(x.placeId); if (pl && inBridge(pl.deck, pl.room)) return true; }
  return false;
}
const bridgeBars = j => bridgeShut() && !heldForYou(j) && bridgeJob(j);
const healthState = v => v >= 90 ? 'fine' : v >= 70 ? 'worn' : v >= 45 ? 'poor' : 'failing';
function machineLabel(m) {
  const K = MACHINE_KINDS[m.kind], n = machineList().filter(x => x.kind === m.kind && x.deck === m.deck).length > 1 ? ' ' + m.id.split('-').pop() : '';
  return K.name + n + ', ' + deckIn(m.deck);
}
function shipHealthRows() {
  const sys = shipMeters(), st = machinesNow(), health = shipHealth(sys);   // the meters: the machines less the upkeep (0.33.57)
  const rows = SYSTEMS.map(k => {
    const ms = machineList().filter(m => MACHINE_KINDS[m.kind].sys === k && st[m.id].state !== 'healthy').sort((a, b) => st[a.id].cond - st[b.id].cond);
    return { key: k, name: SYSTEM_NAME[k], value: Math.round(sys[k]), state: healthState(sys[k]), worst: ms.length ? machineLabel(ms[0]) : null };
  }).sort((a, b) => a.value - b.value || SYSTEMS.indexOf(a.key) - SYSTEMS.indexOf(b.key));
  return [{ key: 'ship', name: 'Ship health', value: Math.round(health), state: healthState(health), worst: null }].concat(rows);
}
// the ship's mood for the crew (answer 22, with the sim engineer's crewMood): shipMoodAt(deck, t) -> { mood, health,
// about }: mood is points off (0 to -30, as shipEffects), about what they grumble about ('the showers'), or null
// while all is well. Pure (shipEffectsAt): safe inside the schedules and replays.
const GRUMBLE = { recycler: 'the showers', pump: 'the showers', filter: 'the cloudy water', uv: 'the water', manifold: 'the lukewarm water',
  scrubber: 'the stuffy air', airplant: 'the stale air', fan: 'the stale air', o2cell: 'the thin air', electrolyser: 'the thin air',
  heater: 'the cold cabins', heatpump: 'the cold', washer: 'the laundry', oven: 'late meals', range: 'late meals', galleyplant: 'the galley',
  extractor: 'the galley', chiller: 'the food', lights: 'the lights', junction: 'the brownouts', powerjunction: 'the brownouts', lift: 'the slow lift',
  irrigation: 'the garden', nutrient: 'the garden', growlight: 'the garden', relay: 'the bridge stations', databus: 'the bridge stations', valve: 'the dripping pipes' };
const STAGE_RANK = { minor: 1, noticeable: 2, serious: 3 };
function shipMoodAt(deck, t) {
  const fx = shipEffectsAt(deck, t);
  const weight = n => STAGE_RANK[n.stage] * 100 + ((MACHINE_FX[n.kind] || {}).mood || 0);   // the most serious, then what upsets most
  let best = null; for (const n of fx.notes) if (!best || weight(n) > weight(best)) best = n;
  const about = best ? GRUMBLE[best.kind] || (best.kind === 'power' ? 'the low power' : null) : fx.health < 70 ? 'the state of the ship' : null;
  return { mood: fx.mood, health: fx.health, about };
}
// the cold store's chiller (answer 7, with the galley engineer): chillerAt(t) -> { cond, state, spoil }: spoil is the
// share of the cold store's meals lost each ship hour (0 while it works well; up to CHILL_SPOIL when broken). Pure,
// from the hour-by-hour record, like shipEffectsAt; as new with no record. The galley bins the food and sends the Mail.
const CHILL_SPOIL = .05;
function chillerAt(t) {
  const ms = machineList().filter(m => m.kind === 'chiller'); if (!ms.length) return { cond: 100, state: 'healthy', spoil: 0 };
  const c = MACH_HIST.get(histHour(t)), cond = Math.min(...ms.map(m => c ? c[m.id] ?? 100 : 100)), w = machWorks(cond);
  return { cond: Math.round(cond * 10) / 10, state: machineState(cond), spoil: w >= 85 ? 0 : Math.round(CHILL_SPOIL * (85 - w) / 85 * 10000) / 10000 };
}

// the garden's growing conditions (0.33.34, for the galley engineer's working garden): gardenAt(t) -> { water, feed,
// light }, each 0-1 (1: all good). water: the irrigation pumps, held back by the rest of the water system once it's
// below 75 ("water feeds the garden"); feed: the nutrient dosing; light: the grow racks' lights, held back by power
// the same way. Each by how well its worst machine works: 1 while it's worn or better, then machWorks scaled (about .59 at
// the top of faulty, .24 failing, 0 broken; 0.33.35: before, a worn machine gave .85-1 and the galley's beds grew slower)
// Pure: it reads the hour-by-hour record (all good with none yet), so it's safe in the galley's replays
function gardenAt(t) {
  const c = MACH_HIST.get(histHour(t)) || {}, ms = machineList();
  const works = kind => { const xs = ms.filter(m => m.kind === kind); return xs.length ? Math.min(1, Math.min(...xs.map(m => machWorks(c[m.id] ?? 100))) / 85) : 1; };
  const feeds = (sys, own) => { const c2 = { ...c }; for (const m of ms) if (m.kind === own) c2[m.id] = 100; return Math.min(1, systemOwn(sys, c2) / 75); };
  const r = x => Math.round(x * 1000) / 1000;
  return { water: r(works('irrigation') * feeds('water', 'irrigation')), feed: r(works('nutrient')), light: r(works('growlight') * feeds('power', 'growlight')) };
}

// ---- tapping a machine (answer 5, 0.33.18): machineUse(id, who) -> { text, ran, until } ----
// What a tap on a machine does (the player engineer's tap calls it; the architects' item text comes first). Every
// machine gives a line about itself and its condition. One with a use (a washer, an oven or the range, the galley
// extractor, the main fan, the lights, the lift's call panel) starts: it runs for its minutes (machineLook's
// `running`), and your use wears it a little, at the next ship hour (MACH_EXTRA, saved). A broken one doesn't start.
// who: 'you', or a crew member's id (their use is already in the schedules, so it adds no wear).
const MACHINE_USES = {
  washer:    { mins: 45, wear: .3,  go: 'You start a load. It fills and begins to churn.' },
  oven:      { mins: 20, wear: .2,  go: 'You switch it on to warm through.' },
  range:     { mins: 15, wear: .15, go: 'A ring glows to life under your hand.' },
  extractor: { mins: 15, wear: .1,  go: 'You turn the extractor up. It roars, then settles.' },
  fan:       { mins: 30, wear: .1,  go: 'You run the main fan up to boost. The air starts to move.' },
  lights:    { mins: 1,  wear: .05, go: 'You cycle the deck lights. They blink off and come back up.' },
  lift:      { mins: 1,  wear: .05, go: 'You call the lift. Somewhere below, it starts to move.' },
};
const USE_STATE = { healthy: 'in good order', worn: 'showing its age, due a service', faulty: 'playing up', failing: 'barely working', broken: 'broken' };
const USE_HOW = { faulty: ' It sounds rough.', failing: ' It shudders and whines; it won\'t last.' };
const MACH_EXTRA = {};                                   // id -> condition points your use takes off at the next hour
function machineUse(id, who = 'you') {
  const st = machinesNow()[id], m = st && machineById(id);
  if (!m) return { text: null, ran: false, until: null };
  const U = MACHINE_USES[m.kind], line = machineLabel(m).split(',')[0] + ': ' + USE_STATE[st.state] + '.';
  const job = SHIP.jobs.find(j => j.machine === id && j.status !== 'done' && j.found <= shipNow());
  const onBoard = job ? job.claimedBy === 'you' ? ' It\'s your job.' : ' It\'s on the job board.' : '';
  if (!U) return { text: line + onBoard, ran: false, until: null };
  if (st.state === 'broken') return { text: line + ' Nothing happens.' + onBoard, ran: false, until: null };
  const until = shipNow() + U.mins;
  MACH_RUN[id] = Math.max(MACH_RUN[id] || 0, until);
  if (who === 'you') MACH_EXTRA[id] = (MACH_EXTRA[id] || 0) + U.wear;
  MACH_REV++;
  return { text: line + ' ' + U.go + (USE_HOW[st.state] || '') + onBoard, ran: true, until };
}

// ---- supplies running short (answer 6, 0.33.18): from the numbers, told by Mail ----
// The weekly delivery is sometimes late (about one week in five, by a day or two: deliveryLate, from the week).
// Stores sends Mail (section 15's mailSend, when it's there) when the delivery is late, when a part nobody can make
// runs out (NO_MAKE: once, until it's restocked), and when the hold's food falls under two days' worth. SHIP.short remembers what's
// been told (saved).
const DELIVERY_SEED = machSeed('delivery'), FOOD_LOW = 300;
const deliveryLate = d => { const wk = d - weekday(d); return wk <= 1 ? 0 : schedU(DELIVERY_SEED, wk, 11) < .2 ? 1 + Math.floor(2 * schedU(DELIVERY_SEED, wk, 12)) : 0; };   // never in the first week: your first is Day 3 (0.33.42)
const DAY_NAME = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
const plural = p => (/s$/.test(p) ? p : p.replace(/([^aeiou])y$/, '$1ie') + 's').replace(/^uv /, 'UV ');
SHIP.short = {};
function mail(t, subject, body) { if (typeof mailSend === 'function') mailSend({ at: t, from: 'Stores', subject, body }); }
function suppliesHour(t, d) {
  const S = SHIP.short;
  if (weekday(d) === DELIVERY.day && (t / 60) % 24 === DELIVERY.hour && deliveryLate(d))
    mail(t, 'The supply shuttle is late', 'This week\'s delivery won\'t make Wednesday. It\'s due ' + DAY_NAME[DELIVERY.day + deliveryLate(d)] + ' at 10:00. Go easy on the shelves till then.');
  for (const k of NO_MAKE) {                            // parts the machine shop can make are never short for long
    if ((SHIP.stores[k] || 0) > 0) { delete S[k]; continue; }
    if (S[k]) continue;
    S[k] = t;
    mail(t, 'Out of ' + plural(k), 'Main storage on Deck 5 has run out of ' + plural(k) + ', and the machine shop can\'t make them. Jobs that need one wait for the delivery.');
  }
  if (cartsCarryFood() && SHIP.hold.meals !== undefined) {
    if (SHIP.hold.meals >= FOOD_LOW) delete S.meals;
    else if (!S.meals) { S.meals = t; mail(t, 'Food stores low', 'The cargo hold is down to ' + SHIP.hold.meals + ' meals, under two days\' worth. The galley will stretch it till the delivery.'); }
  }
}

// ---- B2: the job list. SHIP.jobs = [{ id, machine, deck, kind, urgency, posted, found, claimedBy, parts, status, ... }] ----
// Every hour (jobsHour, inside machinesNow, before that hour's wear): finished jobs put their machine right, the
// weekly delivery lands in the hold, a job is posted for each machine that needs one (or brought up to date as it
// gets worse), and the crew on shift claim what they can. All of it on paper, from the schedules: a claim is a run
// of segments (to Deck 5 storage for the parts, the lift, the machine's panel, back to the desk) that jobWhere()
// lays over the person's plan. Nothing here draws.
//   jobs by machine state: worn -> service (found on rounds a few hours later, not straight onto the board);
//   faulty -> repair; failing -> repair, urgent; broken -> overhaul (longer, more parts)
//   status: 'open' (on the board), 'waiting' (no parts and none can be made), 'claimed', 'done'
//   kind 'restock': a hover cart from the cargo hold to storage (cargo 'stores') or to Deck 3's cold store ('meals')
const JOB_TYPES = {                                      // work: minutes at the panel (more for higher tiers); restore: condition after
  service:  { work: 20, restore: 100, parts: 1 },
  repair:   { work: 45, restore: 95,  parts: 2 },
  overhaul: { work: 90, restore: 90,  parts: 3 },
  chore:    { work: 15, restore: 0,   parts: 0 },        // chores (0.33.19): their own stops and minutes; this is for readers of a job's work
};
// job kinds with steps (0.33.47, foundation 17.5), so Pillar 5's mechanics never edit section 17: section 24's sub-blocks
// register theirs at load. jobKindAdd(kind, def), def = { tier, junior?, only?, work, parts?, text?, stops(j) -> [{ deck,
// placeId, mins, tag, how?, opts? }], post(h, jobs)?, done(j, t, by), stepDone?(j, k, res, t), crew: { can(p), mins }, side?, veto? }:
// post runs each ship hour in jobsHour (push jobMake(kind, {...}) results; it must not call machinesNow's readers);
// done is what finishing it does (by: 'you' or a crew id); the crew do it as a walk through its stops in crew.mins
// (a number, or a function of the job), if crew.can(p). A stop's `how`: 'hold' | 'look' | 'carry' | 'choose' | 'turn' |
// 'wait' (default 'hold'; section 15's workStep runs them), `opts` its data. jobStepDone(id, k, res) keeps res on the
// job (j.res[k], saved) and passes it to stepDone. A registered job also keeps its stops' plain fields in j.stops, so a
// reader that lists a chore's stops lists its; jobByStops(j): a job done stop by stop (a chore, a favour or a registered kind)
const JOB_KINDS = {};
function jobKindAdd(kind, def) {
  if (!kind || JOB_TYPES[kind] && !JOB_KINDS[kind] || !def || typeof def.stops !== 'function' || typeof def.done !== 'function') return false;
  JOB_KINDS[kind] = def; JOB_TYPES[kind] = { work: def.work || 15, restore: 0, parts: (def.parts || []).length };
  return true;
}
const jobKindOf = j => j && JOB_KINDS[j.kind] || null;
const jobByStops = j => !!j && (j.kind === 'chore' || j.kind === 'favour' || !!JOB_KINDS[j.kind]);
const jobSide = j => !!(JOB_KINDS[j.kind] && JOB_KINDS[j.kind].side);   // def.side: taken beside your board job, never lapses (the drill; M1's ask)
const plainStop = x => ({ deck: x.deck, placeId: x.placeId || null, mins: x.mins || 0, tag: x.tag || 'job', ...(x.how ? { how: x.how } : {}), ...(x.hold ? { hold: x.hold } : {}) });
function kindStops(j) { const K = jobKindOf(j); if (!K) return j.stops || []; try { return K.stops(j) || []; } catch (e) { return j.stops || []; } }
// a registered kind's job, ready to push: jobMake(kind, { id?, machine?, deck, room?, title, h (the hour), urgency?, ... })
function jobMake(kind, o = {}) {
  const K = JOB_KINDS[kind], t = Number.isFinite(o.h) ? o.h * 60 : shipNow(), { h, ...rest } = o;
  const j = { id: o.id || kind + ':' + (o.machine || o.target || 'job') + '@' + Math.floor(t / 60), machine: null, deck: null, room: null, kind, title: K && K.text || kind, tier: K && K.tier || 1,
              urgency: 0, leave: null, posted: t, found: t, claimedBy: null, parts: (K && K.parts || []).slice(), status: 'open', ...(K && K.junior ? { junior: true } : {}), ...(K && K.only ? { only: K.only } : {}), ...rest };
  j.stops = kindStops(j).map(plainStop);
  return j;
}
const JOB_FOR = { worn: 'service', faulty: 'repair', failing: 'repair', broken: 'overhaul' };
// what can go wrong with each machine (0.33.46, foundation 17.4; plans/mechanics/fault-tables.html, Tier 1, approved by
// the lead). FAULT_CAUSES[kind] = [{ id, part | setting | load, w, shows, sign, when, still, from?, band? }]: part: the
// part that fixes it (every one is in STOCK); setting: fixed by tuning (M5; until it's in, the kind's own part); load:
// the machine is fine and something else pulls on it (head-scratchers only: never a real fault's cause); w: how common
// (3 often, 2 sometimes, 1 rarely); shows: the job card's symptom; sign: what you see up close; when: 'always' | 'peak' |
// 'warm' | 'after-use' | 'touched' | 'at-time'; still: the machine's line when the wrong part goes in; from: the first ship
// day it can be the cause (settings: Day 4); band: the first tier it can be the cause in (2: Officer, 3: Senior Officer).
// The words are the first drafts of the Works writer's content/works/faults.lines (key: kind + '.' + id). A kind with no
// table behaves as before (its own part, no cause)
const FAULT_CAUSES = {
  oven: [
    { id: 'element', part: 'element', w: 3, shows: 'runs cool', sign: 'cool all over, slow to heat', when: 'always', still: 'New element in. Still cool by the door.' },
    { id: 'seal', part: 'seal', w: 2, shows: 'runs cool', sign: 'cool by the door; you feel heat at the gap', when: 'always', still: 'Fresh seal. Still slow to heat all over.' },
    { id: 'belt', part: 'fan belt', w: 1, shows: 'runs cool', sign: 'hot at the back, cool at the front; a squeal at start', when: 'after-use', still: 'New belt. Still cool.' },
    { id: 'drift', setting: true, w: 2, shows: 'runs hot|runs cool', sign: 'the glow stutters (hot) or the screen dims (cool)', when: 'always', from: 4 },
    { id: 'junction', load: '3-junction', w: 1, shows: 'runs cool', sign: 'fine at breakfast, cool at dinner', when: 'peak', band: 2 } ],
  range: [
    { id: 'element', part: 'element', w: 3, shows: 'a ring is weak', sign: 'one ring slow, the others fine', when: 'always', still: 'New element. That ring\'s still weak: it clicks, no heat.' },
    { id: 'relay', part: 'relay', w: 2, shows: 'a ring is weak', sign: 'it clicks but sometimes won\'t heat', when: 'touched', still: 'New relay. Still slow to heat.' },
    { id: 'drift', setting: true, w: 2, shows: 'runs hot', sign: 'every ring too fierce; Brennan complains', when: 'always', from: 4 } ],
  galleyplant: [
    { id: 'belt', part: 'fan belt', w: 3, shows: 'weak draw', sign: 'a squeal, the belt shiny', when: 'after-use', still: 'New belt. Still weak: the grille\'s caked.' },
    { id: 'filter', part: 'filter', w: 2, shows: 'weak draw', sign: 'grease on the grille, quiet fan', when: 'always', still: 'Clean filter. Still weak, and it squeals.' },
    { id: 'bearing', part: 'bearing', w: 1, shows: 'noisy', sign: 'a grinding hum', when: 'always', still: 'New belt. Still grinding.' } ],
  extractor: [
    { id: 'belt', part: 'fan belt', w: 3, shows: 'weak draw', sign: 'a squeal at start, smoke lingers', when: 'after-use', still: 'New belt. Still weak: the hood\'s filter\'s black.' },
    { id: 'filter', part: 'filter', w: 2, shows: 'weak draw', sign: 'grease dripping at the hood\'s edge', when: 'always', still: 'Clean filter. Still weak, and it squeals.' },
    { id: 'relay', part: 'relay', w: 1, shows: 'stops and starts', sign: 'clicks, runs, stops', when: 'warm', still: 'New belt. Still stops and starts.' } ],
  chiller: [
    { id: 'compressor', part: 'compressor', w: 2, shows: 'runs warm', sign: 'a laboured hum that never stops', when: 'always', still: 'New compressor. Still warm: frost round the door.' },
    { id: 'seal', part: 'seal', w: 3, shows: 'runs warm', sign: 'frost round the door frame', when: 'after-use', still: 'Fresh seal. Still warm, and it hums all night.' },
    { id: 'bearing', part: 'bearing', w: 1, shows: 'runs warm', sign: 'warm at the back shelves, a rattle', when: 'always', still: 'New bearing. Still warm by the door.' },
    { id: 'sensor', part: 'signal card', w: 1, shows: 'milk going off', sign: 'the display says 3°, the back shelf feels warmer', when: 'always', still: 'New compressor. Display still says 3°; still warm.', band: 3 } ],
  washer: [
    { id: 'pump', part: 'pump', w: 3, shows: 'leaks', sign: 'a puddle under it, the pump housing damp', when: 'after-use', still: 'New pump. Still drips at the door.' },
    { id: 'seal', part: 'seal', w: 2, shows: 'leaks', sign: 'drips at the door during the spin', when: 'after-use', still: 'Fresh seal. Still a puddle under it.' },
    { id: 'valve', part: 'valve', w: 2, shows: 'leaks', sign: 'water left in the drum after the cycle', when: 'after-use', still: 'New valve. Still a puddle under it.' },
    { id: 'bearing', part: 'bearing', w: 1, shows: 'loud spin', sign: 'a rumble, the machine walks on the floor', when: 'after-use', still: 'New pump. Still rumbles.' },
    { id: 'relay', part: 'relay', w: 1, shows: 'stops mid-cycle', sign: 'stops, clicks, starts again', when: 'warm', still: 'New pump. Still stops mid-cycle.' } ],
  lift: [
    { id: 'relay', part: 'relay', w: 3, shows: 'slow, stops at decks', sign: 'pauses before the doors open', when: 'warm', still: 'New bearing. Still pauses at the doors.' },
    { id: 'bearing', part: 'bearing', w: 2, shows: 'judders', sign: 'a grinding in the shaft between decks', when: 'always', still: 'New relay. Still judders between decks.' },
    { id: 'breaker', part: 'breaker', w: 1, shows: 'stops between decks', sign: 'stalls, then the breaker light', when: 'peak', still: 'New relay. It still stalls at shift change.' } ],
  lights: [
    { id: 'relay', part: 'relay', w: 3, shows: 'lights flicker', sign: 'the whole room\'s lights, worse after an hour', when: 'warm', still: 'New lamp. Still flickers, the whole room.' },
    { id: 'lamp', part: 'lamp', w: 2, shows: 'lights flicker', sign: 'one lamp only', when: 'always', still: 'New relay. That one lamp still flickers.' },
    { id: 'breaker', part: 'breaker', w: 1, shows: 'lights out', sign: 'a whole run dark; the breaker\'s lamp lit', when: 'peak', still: 'New relay. Dark again at dinner.' },
    { id: 'cable', part: 'cable', w: 1, shows: 'lights flicker', sign: 'flickers when the door slams', when: 'touched', still: 'New relay. Still flickers when the door goes.', band: 2 },
    { id: 'drift', setting: true, w: 2, shows: 'lights flicker|lights dim', sign: 'fast flicker everywhere (high) or a sag (low)', when: 'always', from: 4 } ],
  cartdock: [
    { id: 'relay', part: 'relay', w: 2, shows: 'charges slow', sign: 'the lamp blinks, then holds', when: 'warm', still: 'New cell. Still blinks before it charges.' },
    { id: 'cell', part: 'cell', w: 2, shows: 'charges slow', sign: 'the cart\'s gauge never gets past three quarters', when: 'always', still: 'New relay. Still stops at three quarters.' },
    { id: 'cable', part: 'cable', w: 1, shows: 'won\'t charge', sign: 'charges only if you jiggle the plug', when: 'touched', still: 'New relay. Still only if you jiggle it.' },
    { id: 'drift', setting: true, w: 2, shows: 'charges slow', sign: 'the screen dims', when: 'always', from: 4 } ],
  growlight: [
    { id: 'lamp', part: 'lamp', w: 3, shows: 'a rack is dim', sign: 'a row of pink lamps gone pale', when: 'always', still: 'New relay. Still pale along that row.' },
    { id: 'relay', part: 'relay', w: 2, shows: 'a rack is dim', sign: 'the whole rack flickers off and on', when: 'warm', still: 'New lamps. The rack still cuts out.' },
    { id: 'drift', setting: true, w: 1, shows: 'lights at the wrong hours', sign: 'on at night, off at noon', when: 'at-time', from: 4 } ],
  // Tier 2 (0.33.55): the air line's duct dampers (fault-tables.html; line: 'air' marks a cause tracing reads along the air line)
  damper: [
    { id: 'relay', part: 'relay', w: 3, shows: 'stuffy air on its decks', sign: 'the flap clicks but stays half shut, worse once warm', when: 'warm', still: 'New bearing. The flap still clicks and stays half shut.', line: 'air' },
    { id: 'bearing', part: 'bearing', w: 2, shows: 'stuffy air on its decks', sign: 'the flap judders and sits half open, all day', when: 'always', still: 'New relay. The flap still judders.', line: 'air' },
    { id: 'seal', part: 'seal', w: 1, shows: 'a whistle in the duct', sign: 'a whistle at the duct mouth', when: 'always', still: 'New relay. Still whistles.' } ],
  // the rest of Tier 2 (0.33.56, fault-tables.html, approved by the user 2026-10-18). No `band` on their part causes: the page's
  // "never before T2" is the player meeting them, and a Tier 2 machine's jobs are above you till then anyway (jobTier); the
  // crew's causes come from the same table ("before that Tier 2 machines still fault as now"). A load is never picked
  scrubber: [
    { id: 'filter', part: 'filter', w: 3, shows: 'stuffy air|rattles', sign: 'a grey grille; the intake buzzes all day', when: 'always', still: 'Clean filter. Still rattles once it\'s run all day.', line: 'air' },
    { id: 'bearing', part: 'bearing', w: 2, shows: 'rattles', sign: 'a whine that builds through the evening', when: 'warm', still: 'New bearing. Still rattles when the door goes.' },
    { id: 'panel', part: 'seal', w: 1, shows: 'rattles', sign: 'the housing buzzes when the door goes', when: 'touched', still: 'Fresh gasket on the panel. Still rattles, door or no door.' },
    { id: 'drift', setting: true, w: 2, shows: 'stuffy air', sign: 'the hum\'s off pitch; the grille\'s clean', when: 'always', from: 4, band: 2 } ],   // M5 stage 2; till then the filter fixes it
  heater: [
    { id: 'valve', part: 'valve', w: 3, shows: 'cold cabins', sign: 'one branch\'s pipe cold to the touch, the rest warm', when: 'always', still: 'New valve. Still lukewarm everywhere, and it knocks.', line: 'heat' },
    { id: 'pump', part: 'pump', w: 2, shows: 'cold cabins', sign: 'every pipe lukewarm; a knock in the plant', when: 'always', still: 'New pump. That one branch is still cold.', line: 'heat' },
    { id: 'relay', part: 'relay', w: 1, shows: 'cold cabins', sign: 'warm, then cold for an hour: it clicks off and on', when: 'warm', still: 'New valve. Still goes cold after it\'s run a while.', line: 'heat' } ],
  recycler: [
    { id: 'membrane', part: 'membrane', w: 3, shows: 'low output', sign: 'the output gauge low all day; a brown film in the sight glass', when: 'always', still: 'New membrane. Output still sinks after 18:00.', line: 'water' },
    { id: 'pump', part: 'pump', w: 2, shows: 'low output', sign: 'fine in the morning; the gauge sinks after 18:00', when: 'peak', still: 'New pump. Output still low all day; the glass is brown.', line: 'water' },
    { id: 'valve', part: 'valve', w: 1, shows: 'low output', sign: 'the outlet pipe shudders; the gauge flickers', when: 'always', still: 'New valve. Output still low; the glass is brown.', line: 'water' },
    { id: 'seal', part: 'seal', w: 1, shows: 'a drip', sign: 'a wet ring on the floor under it', when: 'after-use', still: 'Fresh seal. Still a wet ring under it.' } ],
  filter: [
    { id: 'cartridge', part: 'cartridge', w: 3, shows: 'low flow', sign: 'one housing\'s gauge in the red, all day', when: 'always', still: 'New cartridge. Flow still low: the floor\'s damp.', line: 'water' },
    { id: 'seal', part: 'seal', w: 2, shows: 'low flow', sign: 'a damp floor under one housing, a faint hiss', when: 'after-use', still: 'Fresh seal. Flow still low; one gauge\'s in the red.', line: 'water' },
    { id: 'valve', part: 'valve', w: 1, shows: 'cloudy water', sign: 'clear first thing, cloudy by the busy hours', when: 'peak', still: 'New valve. Still clouds by the afternoon.' } ],
  uv: [
    { id: 'lamp', part: 'uv lamp', w: 3, shows: 'water tastes off', sign: 'a dull blue glow in the window', when: 'always', still: 'New relay. The glow\'s still dull.' },
    { id: 'relay', part: 'relay', w: 2, shows: 'water tastes off', sign: 'the glow blinks off and on once it\'s warm', when: 'warm', still: 'New lamp. It still blinks off once it\'s warm.' },
    { id: 'seal', part: 'seal', w: 1, shows: 'low flow', sign: 'water beading on the housing, a drip', when: 'after-use', still: 'Fresh seal. Flow still low.', line: 'water' } ],
  pump: [
    { id: 'pump', part: 'pump', w: 3, shows: 'low flow', sign: 'fine in the morning; labours after 18:00', when: 'peak', still: 'New seal. Still labours in the evening.', line: 'water' },
    { id: 'seal', part: 'seal', w: 2, shows: 'low flow', sign: 'a drip under the shaft, low all day', when: 'always', still: 'New pump. Still drips under the shaft.', line: 'water' },
    { id: 'bearing', part: 'bearing', w: 1, shows: 'noisy', sign: 'a grinding, worse after a long run', when: 'warm', still: 'New pump. Still grinding.' },
    { id: 'irrigation', load: '3-irrigation-1', w: 1, shows: 'low flow', sign: 'low only while the garden\'s being watered', when: 'with:irrigation', line: 'water', band: 2 } ],   // P1's later form only
  valve: [
    { id: 'valve', part: 'valve', w: 3, shows: 'low flow on its branch', sign: 'its branch\'s decks weak; the handle\'s stiff', when: 'always', still: 'Fresh seal. That branch is still weak.', line: 'water' },
    { id: 'seal', part: 'seal', w: 2, shows: 'a drip', sign: 'a drip from the gland, a wet floor', when: 'always', still: 'New valve. Still drips.' } ],
  heatpump: [
    { id: 'pump', part: 'pump', w: 3, shows: 'cold cabins', sign: 'a knock; both outlets lukewarm all day', when: 'always', still: 'New valve. Both outlets still lukewarm; it knocks.', line: 'heat' },
    { id: 'bearing', part: 'bearing', w: 2, shows: 'cold cabins', sign: 'a whine, and the radiators cool off after hours of running', when: 'warm', still: 'New pump. Still cools off by evening, and whines.', line: 'heat' },
    { id: 'valve', part: 'valve', w: 2, shows: 'cold cabins', sign: 'one outlet hot, the other cold', when: 'always', still: 'New pump. One outlet still cold.', line: 'heat' } ],
  manifold: [
    { id: 'valve', part: 'valve', w: 3, shows: 'one deck cold', sign: 'that deck\'s pipe cold at the manifold, all day', when: 'always', still: 'Fresh seal. That deck\'s still cold.', line: 'heat' },
    { id: 'regulator', part: 'regulator', w: 2, shows: 'cabins cold at night', sign: 'fine by day; the gauge drops after 22:00', when: 'at-time', still: 'New valve. Still cold after 22:00.', line: 'heat' },
    { id: 'seal', part: 'seal', w: 1, shows: 'a drip', sign: 'a hiss and a wet floor under a joint', when: 'always', still: 'New valve. Still hisses.' } ],
  o2cell: [
    { id: 'cell', part: 'oxygen cell', w: 3, shows: 'air thin', sign: 'one cell\'s lamp amber; the gauge low all day', when: 'always', still: 'New regulator. One lamp\'s still amber.', line: 'air' },
    { id: 'regulator', part: 'regulator', w: 2, shows: 'air thin', sign: 'a hiss, then the gauge jumps; worst at the busy hours', when: 'peak', still: 'New cell. Still hisses and jumps when everyone\'s up.', line: 'air' },
    { id: 'relay', part: 'relay', w: 1, shows: 'stops and starts', sign: 'the cells click off and on once warm', when: 'warm', still: 'New cell. Still clicks off and on.' } ],
  electrolyser: [
    { id: 'membrane', part: 'membrane', w: 3, shows: 'air thin', sign: 'bubbles slow in the sight glass, all day', when: 'always', still: 'New cell. Bubbles still slow.', line: 'air' },
    { id: 'cell', part: 'cell', w: 2, shows: 'air thin', sign: 'strong in the morning, fading by evening', when: 'warm', still: 'New membrane. Still fades by evening.', line: 'air' },
    { id: 'relay', part: 'relay', w: 1, shows: 'stops and starts', sign: 'clicks off, then on again', when: 'warm', still: 'New membrane. Still stops and starts.' } ],
  irrigation: [
    { id: 'pump', part: 'pump', w: 3, shows: 'dry beds', sign: 'every bed damp, none wet; the pump hums low', when: 'always', still: 'New valve. Every bed\'s still only damp.' },
    { id: 'valve', part: 'valve', w: 2, shows: 'dry beds', sign: 'one bed bone dry, the rest fine', when: 'always', still: 'New pump. That one bed\'s still dry.' },
    { id: 'nozzles', part: 'filter', w: 1, shows: 'dry beds', sign: 'spits, then nothing', when: 'after-use', still: 'New pump. Still spits, then nothing.' } ],   // the strainer in the line (M14 cleans them)
  nutrient: [
    { id: 'pack', part: 'nutrient pack', w: 3, shows: 'yellow leaves', sign: 'the pack\'s window empty', when: 'always', still: 'New pump. The window\'s still empty.' },
    { id: 'pump', part: 'pump', w: 2, shows: 'yellow leaves', sign: 'the pack full, the dosing line barely ticks', when: 'always', still: 'New pack. The line still barely ticks.' },
    { id: 'regulator', part: 'regulator', w: 1, shows: 'brown leaf tips', sign: 'a white crust on the tray edges', when: 'always', still: 'New pack. Still a crust on the trays.' } ],
  airplant: [
    { id: 'filter', part: 'filter', w: 3, shows: 'stuffy air ship-wide', sign: 'a grey filter face; the intake pulls hard', when: 'always', still: 'New belt. Filter face still grey.', line: 'air' },
    { id: 'belt', part: 'fan belt', w: 2, shows: 'stuffy air ship-wide', sign: 'a squeal at shift change, weak for the next hour', when: 'peak', still: 'Clean filter. Still squeals at shift change.', line: 'air' },
    { id: 'bearing', part: 'bearing', w: 1, shows: 'noisy', sign: 'a rumble from the plant', when: 'warm', still: 'New belt. Still rumbles.' } ],
  fan: [
    { id: 'bearing', part: 'bearing', w: 3, shows: 'stuffy air ship-wide', sign: 'a rumble in the duct', when: 'warm', still: 'New belt. Still rumbles.', line: 'air' },
    { id: 'belt', part: 'fan belt', w: 2, shows: 'stuffy air ship-wide', sign: 'a squeal; the belt shiny', when: 'always', still: 'New bearing. Still squeals.', line: 'air' },
    { id: 'relay', part: 'relay', w: 1, shows: 'stops', sign: 'stops, clicks, starts', when: 'warm', still: 'New bearing. Still stops.', line: 'air' } ],
  gasplant: [
    { id: 'regulator', part: 'regulator', w: 3, shows: 'low lab gas', sign: 'the gauge wanders all day', when: 'always', still: 'Fresh seal. The gauge still wanders.' },
    { id: 'seal', part: 'seal', w: 2, shows: 'low lab gas', sign: 'a hiss at a joint; soapy water bubbles', when: 'always', still: 'New regulator. Still hisses at the joint.' },
    { id: 'valve', part: 'valve', w: 1, shows: 'low lab gas', sign: 'fine until someone opens a bench tap, then it drops', when: 'touched', still: 'New regulator. Still drops when a tap opens.' } ],
  // the rec deck's (0.84.1, rec engineer B; plans/recdeck-plan.html section 6). Deck 7 has no crew hours yet, so no 'peak' or
  // 'after-use' causes (they'd never show); first drafts of the words, for the writers
  poolfilter: [
    { id: 'cartridge', part: 'cartridge', w: 3, shows: 'the pool is cloudy', sign: 'the gauge high, the water milky past the shallow end', when: 'always', still: 'Fresh cartridge. Still dripping.' },
    { id: 'seal', part: 'seal', w: 2, shows: 'a drip under the housing', sign: 'a wet ring on the floor under the housing', when: 'always', still: 'New seal. The water\'s still milky.', line: 'pool' } ],   // line: 0.84.5 (rec engineer B), the pool line's traced leak
  pooldoser: [
    { id: 'drift', setting: true, w: 2, shows: 'stinging eyes|a green tinge', sign: 'the reading wanders; the swimmers come out red-eyed', when: 'always', from: 4 },
    { id: 'relay', part: 'relay', w: 2, shows: 'the dose has stopped', sign: 'the pump clicks but doesn\'t run', when: 'touched', still: 'New relay. It runs, but the reading\'s still off.' } ],
  poolheat: [
    { id: 'valve', part: 'valve', w: 3, shows: 'the pool runs cold', sign: 'the return pipe barely warm', when: 'always', still: 'New valve. Still cold in the morning.' },
    { id: 'regulator', part: 'regulator', w: 1, shows: 'the pool runs cold', sign: 'warm by day, cold first thing', when: 'at-time', still: 'New regulator. The pipe\'s still cold.' } ],
  riverpump: [
    { id: 'bearing', part: 'bearing', w: 3, shows: 'the current pulses', sign: 'a rumble you feel through the grating', when: 'always', still: 'New bearing. The current\'s still slack.' },
    { id: 'impeller', part: 'pump', w: 2, shows: 'the fast run goes slack', sign: 'quiet, but the gauge reads low', when: 'warm', still: 'New impeller. Still rumbling.' } ],
  wavegate: [
    { id: 'relay', part: 'relay', w: 2, shows: 'no standing wave', sign: 'the gate lights blue but the gate doesn\'t move', when: 'touched', still: 'New relay. Still a slick by the post.' },
    { id: 'seal', part: 'seal', w: 2, shows: 'a slick on the bank', sign: 'oily water round the gate\'s post', when: 'always', still: 'Fresh seal. Still no wave.' } ],
  wallholds: [
    { id: 'hold', part: 'seal', w: 3, shows: 'a hold spins underfoot', sign: 'a hold turns in your hand; its bolt\'s washer has split', when: 'always', still: 'New washer. Another hold\'s still loose.' } ],
  belay: [
    { id: 'brake', part: 'bearing', w: 3, shows: 'it lowers too fast', sign: 'the line pays out with a whine', when: 'always', still: 'New brake bearing. Still a bit fast: the tag\'s out too.' },
    { id: 'tag', setting: true, w: 2, shows: 'inspection due', sign: 'the inspection tag has run out', when: 'always', from: 4 } ],
  stagelights: [
    { id: 'lamp', part: 'lamp', w: 3, shows: 'a stage light is out', sign: 'one lamp in the truss dark', when: 'always', still: 'New lamp. The rig still flickers.' },
    { id: 'relay', part: 'relay', w: 2, shows: 'the whole rig flickers', sign: 'every lamp stutters at once', when: 'warm', still: 'New relay. That lamp\'s still dark.', band: 2 } ],
  soundrack: [
    { id: 'amp', part: 'regulator', w: 2, shows: 'a hum', sign: 'a low hum from every speaker, louder warm', when: 'warm', still: 'New regulator. The mic still cuts out.' },
    { id: 'cable', part: 'cable', w: 3, shows: 'the lectern mic cuts out', sign: 'the mic drops when the cable\'s touched', when: 'touched', still: 'New cable. Still humming.' } ],
  seathinges: [
    { id: 'hinge', part: 'bearing', w: 3, shows: 'a seat won\'t fold', sign: 'a seat stuck down, and a squeak from its neighbours', when: 'always', still: 'New pin in. The next one along still squeaks.' } ],
  courtnet: [
    { id: 'coil', part: 'coil winding', w: 2, shows: 'the net flickers', sign: 'the net stutters, then drops for a breath', when: 'warm', still: 'New coil. The walls still fade.' },
    { id: 'power', part: 'breaker', w: 2, shows: 'the side walls fade', sign: 'the side fields dim, the power units whine', when: 'always', still: 'New breaker. The net still flickers.' } ],
  scoreboard: [
    { id: 'panel', part: 'lamp', w: 3, shows: 'dead pixels in the scores', sign: 'a dark block in the home score', when: 'always', still: 'New panel. Still scrambled.' },
    { id: 'driver', part: 'signal card', w: 2, shows: 'the board shows nonsense', sign: 'the names scramble', when: 'warm', still: 'New card. Still a dark block.', band: 2 } ],
  gravplate: [
    { id: 'controller', part: 'signal card', w: 2, shows: 'gravity creeps back up', sign: 'the gauge drifts toward 1 g', when: 'always', still: 'New controller. The cooling\'s still hot.' },
    { id: 'cooling', part: 'pump', w: 2, shows: 'the room closes itself', sign: 'the cooling loop hot to the touch', when: 'warm', still: 'New pump. Gravity still creeps.' } ],
  doorgear: [                                            // no door gear in DECKS today (a stand-in on Deck 5); kept for when one is real
    { id: 'seal', part: 'seal', w: 3, shows: 'bay doors slow', sign: 'a draught at the frame', when: 'always', still: 'New bearing. Still a draught at the frame.' },
    { id: 'bearing', part: 'bearing', w: 2, shows: 'bay doors slow', sign: 'a judder as they move, worse after a few runs', when: 'after-use', still: 'Fresh seal. Still judders.' },
    { id: 'relay', part: 'relay', w: 1, shows: 'doors stop halfway', sign: 'stop halfway, click, then go', when: 'warm', still: 'New bearing. Still stops halfway.' } ],
};
const FAULT_T2 = ['scrubber', 'heater', 'recycler', 'filter', 'uv', 'pump', 'valve', 'heatpump', 'manifold', 'o2cell', 'electrolyser', 'irrigation', 'nutrient', 'airplant', 'fan', 'damper', 'gasplant', 'doorgear'];
// a real fault's cause (17.4): picked when its repair or overhaul is posted (from Day 2), from the causes allowed that day
// (a setting from its `from` day, a band from that tier; never a load), weighted by w; schedU key 855. faultCause(j) -> the
// cause or null; faultShows(j) -> the job card's symptom (one of a setting's two, by the job)
function faultPick(m, h, only) {                         // only(c): a further test (0.33.59: a traced fault's causes on its line)
  const C = FAULT_CAUSES[m.kind], d = Math.floor(h / 24) + 1; if (!C || d < WORKS_REAL_FROM) return null;
  const ok = C.filter(c => !c.load && (!c.from || d >= c.from) && (!c.band || playerTier() >= c.band) && (!only || only(c))), sum = ok.reduce((a, c) => a + c.w, 0);
  if (!sum) return null;
  let u = schedU(m.seed, h, 855) * sum; for (const c of ok) if ((u -= c.w) < 0) return c;
  return ok[ok.length - 1];
}
const faultCause = j => j && j.cause && j.machine && (FAULT_CAUSES[(machineById(j.machine) || {}).kind] || []).find(c => c.id === j.cause) || null;
const faultShows = j => { const c = faultCause(j); if (!c) return null; const xs = c.shows.split('|'); return xs[(machSeed(j.id) >>> 0) % xs.length]; };
// a machine job's parts: the kind's own, the first one the cause's part (a setting fixed by the kind's part until tuning, M5, is in)
const faultParts = (m, kind, c) => { const ps = Array(JOB_TYPES[kind].parts).fill(MACHINE_KINDS[m.kind].part); if (c && c.part) ps[0] = c.part; return ps; };
const JOB_URGENCY = { worn: 0, faulty: 1, failing: 2, broken: 3 };
const CREW_TIER = { junior: 2, officer: 3, senior: 3, chief: 4, xo: 4, captain: 4 };   // what Works crew may work on
const ENGINE_KINDS = new Set(['reactor', 'coil']);      // the engine crew's, at any tier; nobody else's
const PLAYER_TIER = 1;                                  // you, for now (design doc, "Works progression")
// your tier (0.33.44, Pillar 5 foundation 17.1): section 24's SHIP.works.tier once there is one, else PLAYER_TIER
const playerTier = () => (SHIP.works && SHIP.works.tier) || PLAYER_TIER;
// ranks (0.33.45, foundation 17.2): a job may be a junior job (j.junior: the food cart, hauling, the bunk inspection) or kept
// for a rank (j.only: 'senior' | 'specialist'; saved on the job). You're SHIP.works.rank (section 24; 'junior' till then), the
// crew their roster rank (chief, xo and captain count as senior, the engine crew as specialist). rankOk(who, j): who
// ('you', a person or a crew id) may do j. A junior job is held for you only while you're a junior (forYou)
const RANKS = ['junior', 'officer', 'senior', 'specialist'];
const playerRank = () => (SHIP.works && RANKS.includes(SHIP.works.rank) && SHIP.works.rank) || 'junior';
const crewRank = p => jobCrew(p) === 'engine' ? 'specialist' : ['senior', 'chief', 'xo', 'captain'].includes(p.rank) ? 'senior' : p.rank === 'officer' ? 'officer' : 'junior';
function rankOf(who) {
  if (who === 'you' || who === 'player' || (who && who.isPlayer)) return playerRank();
  const p = typeof who === 'string' ? schedPeople().find(x => x.id === who) : who && (who.p || who);
  return p ? crewRank(p) : 'junior';
}
const rankOk = (who, j) => !j.only || RANKS.indexOf(rankOf(who)) >= RANKS.indexOf(j.only);
const CREW_LEAVE = 180;                                 // crew leave easy, routine jobs this long for you before taking them
// more real faults (0.33.46, foundation 17.3): from Day 2 on your shift days, for machines at your tier, REAL_SHARE of the
// worn machines (schedU key 856, by machine and hour) wore on unseen: their job is found (2-24 hours later, as a service's
// would be, plus FIND_LATE) as a fault, the machine at the top of faulty, its cause picked then. (Delaying the services
// alone, the page's first knob, left the first week's board thin and no faults before Day 5: machine_check 5o, the lead.)
// A repair below urgent is held for you FAULT_LEAVE minutes of the day shift (not CREW_LEAVE) and never shared out
// (shareOut). Days 0-1, your days off and the arrival's jobs are as before
const WORKS_REAL_FROM = 2, FIND_LATE = 0, FAULT_LEAVE = 240, REAL_SHARE = .45;
const realFor = (m, d) => d >= WORKS_REAL_FROM && playerShiftOn(d) && !ENGINE_KINDS.has(m.kind) && jobTier({ machine: m.id }) <= playerTier();
const realRepair = j => j.kind === 'repair' && j.urgency === 1 && !!j.machine && !j.reserved && realFor(machineById(j.machine), Math.floor(j.found / 1440) + 1);
const YOU_KEEP = 720;                                   // a job you take goes back on the board after 12 ship hours with no progress (touchJob)
const JOB_FETCH = 10, JOB_MAKE = 60, JOB_RIDE = 2;       // minutes: fetching parts; making one in the machine shop; a lift ride
// supplies (B3): what main storage keeps of each part (topped up by the weekly delivery), and the parts nobody can
// make in the machine shop. Deliveries come on Wednesdays at 10:00 into the cargo hold.
const STOCK = { lamp: 10, element: 6, 'fan belt': 4, compressor: 2, pump: 4, relay: 6, filter: 8, cartridge: 8, 'uv lamp': 3, 'nutrient pack': 4, valve: 4,
                membrane: 3, bearing: 3, regulator: 3, cell: 3, 'oxygen cell': 3, breaker: 3, cable: 4, 'signal card': 2, seal: 4, 'control rod': 2, 'coil winding': 2 };
const NO_MAKE = new Set(['filter', 'cartridge', 'membrane', 'uv lamp', 'nutrient pack', 'cell', 'oxygen cell', 'control rod']);
const DELIVERY = { day: 2, hour: 10, meals: 1200 };     // weekday (0 = Monday), hour; the hold's meals topped up to this (a week and a bit)
// the delivery as crates in the cargo hold (0.33.42, the plan for 0.60.7): CRATE_PARTS parts a crate; a hover cart pulls in
// up to CART_CRATES; unloading it is held for you till DELIVERY_KEEP (14:00) on a day you're on shift, then the crew do it
const CRATE_PARTS = 8, CART_CRATES = 4, DELIVERY_KEEP = 14 * 60;
// cart runs of food to the cold store (the galley engineer's numbers): one a day on the day shift when it's under
// CART_DAILY, and one at any hour when it's under CART_URGENT; each carries up to CART_MEALS, never past the store's
// cap; the meals land CART_RUN minutes after the hour (later when the lift is slow)
const CART_MEALS = 150, CART_DAILY = 250, CART_URGENT = 90, CART_RUN = 40;
const coldCap = () => typeof FOOD !== 'undefined' && FOOD.coldCap > 0 ? FOOD.coldCap : 300;
// food comes by cart only once the galley says so (section 16's FOOD.restock: 'rule' is its own 10:30 top-up, 'carts' is ours)
const cartsCarryFood = () => typeof FOOD !== 'undefined' && FOOD.restock === 'carts' && !!(SHIP.galley && SHIP.galley.cold);
SHIP.jobs = []; SHIP.stores = {}; SHIP.hold = {}; SHIP.manifest = []; SHIP.misplaced = null;
let JOBS_ON = true;                                     // machine_check turns the crew's jobs off to see the ship unrepaired
function jobsReset() { SHIP.jobs = []; SHIP.stores = { ...STOCK }; SHIP.hold = {}; SHIP.manifest = []; SHIP.misplaced = null; }
// the panel's place, if an architect has put one there ({ machine: id } on a place). Read from the decks: the
// schedules leave panel places out of their own list (they're never anyone's desk)
let PANELS = null;
function panelPlace(id) {
  if (!PANELS) { PANELS = new Map(); for (const n in DECKS) for (const p of DECKS[n].places || []) if (p.machine) PANELS.set(p.machine, p.id); }
  return PANELS.get(id) || null;
}
// a job's tier: its own (a chore's), else its machine's, and never below the tier of the rooms it takes you into
// (a machine in a tier-2 plant room is tier 2 work, whatever its kind: 0.33.19)
const jobTier = j => { const m = j.machine && machineById(j.machine), base = j.tier || (m ? m.tier || MACHINE_KINDS[m.kind].tier : 1);
  return Math.max(base, m ? roomTier(m.deck, m.room) : 0, ...(JOB_KINDS[j.kind] ? kindStops(j) : j.stops || []).map(st => placeTier(st.placeId))); };
// the tier of the hatches into a room (section 4's { key, tier } service entries), 0 if none: worked out from the
// deck's map, so it doesn't need the deck built. A hatch's tier belongs to the room behind it (the `still` utility
// room, else the one that isn't a hall), not the corridor it opens off
const ROOM_TIER = new Map();
function roomTier(n, room) {
  const k = n + room; if (ROOM_TIER.has(k)) return ROOM_TIER.get(k);
  const D = DECKS[n], at = (i, j) => D && D.map[j] && D.map[j][i];
  let tier = 0;
  for (const sv of (D && D.service) || []) if (sv.tier > 0) {
    const [o, i, j] = sv.key.split(','), a = +i, b = +j, two = o === 'h' ? [at(a, b - 1), at(a, b)] : [at(a - 1, b), at(a, b)], R = r => D.rooms[r] || {};
    const behind = two.filter(r => R(r).still).length ? two.filter(r => R(r).still) : two.filter(r => !R(r).hall);   // the utility room, not the corridor
    if (behind.includes(room)) tier = Math.max(tier, sv.tier);
  }
  ROOM_TIER.set(k, tier); return tier;
}
let PLACE_IDX = null;
const placeById = id => { if (!PLACE_IDX) { PLACE_IDX = new Map(); for (const n in DECKS) for (const p of DECKS[n].places || []) PLACE_IDX.set(p.id, { ...p, deck: +n }); } return id && PLACE_IDX.get(id) || null; };
const placeTier = id => { const p = placeById(id); return p ? roomTier(p.deck, p.room) : 0; };
// tier locks (answer 4, 0.33.18): who may pass a service hatch with a `tier` (section 4's hatchPassable): you at your
// tier (playerTier()), Works crew by rank (CREW_TIER: the same tiers as the machines behind the hatches, so juniors
// reach the plant rooms their jobs are in), the engine crew anywhere (they keep the reactor and coils). A `tier` on
// the person (deck_check's stand-in) wins
function hatchTier(who) {
  if (who === 'player' || who.isPlayer) return playerTier();
  if (who.tier > 0) return who.tier;
  const p = who.p || who;
  if (p.tier > 0) return p.tier;
  return jobCrew(p) === 'engine' ? 4 : CREW_TIER[p.rank] || 1;
}
// jobs left for you (0.33.16): the crew take urgent and big jobs, and everything above your tier, at once; a small
// job at your tier waits CREW_LEAVE minutes of the day shift after it's found (one found in the evening waits for
// your morning), a food run an hour. leaveEnd(j): the minute the crew may take it
// 0.33.32 (the user's "the job board never has any jobs"): 3 ship hours are only 5 real minutes, so a small job is
// now held to the end of the shift its wait runs out in, and at most HOLD_MAX at once (jobsHour lets the oldest go,
// j.released). On your days off (playerShiftOn, Saturday and Sunday) nothing is held: the crew take it then.
const DAY_SHIFT = [540, 1020];                           // 09:00-17:00, when you're on shift (08:00 until the playtest's 0.44.14, the user's)
const HOLD_MAX = 4;                                      // small jobs held for you at once, at most (6 until 0.33.40, the plan for 0.60.7; 3 until 0.44.16, the playtest's "a few more jobs on the board")
// every third or so new small job goes to the crew at once (shareOut, jobsHour), unless that would leave you fewer than
// SHARE_KEEP held on the board: so you see the Works crew doing the jobs you do ("Bea on it")
const SHARE_EVERY = 3, SHARE_KEEP = 2;
let SHARE_ON = true;                                    // machine_check turns it off where it needs a job left for you
const forYou = j => j.urgency < 2 && jobTier(j) <= playerTier() && !(j.machine && ENGINE_KINDS.has(machineById(j.machine).kind)) && rankOk('you', j) && (!j.junior || playerRank() === 'junior') && !bridgeBars(j);
function leaveEnd(j) {
  if (!forYou(j) || j.released) return j.found;
  if (j.cargo === 'meals') return j.found + 60;
  if (j.cargo === 'stores') { const d0 = Math.floor(j.found / 1440) * 1440; return playerShiftOn(d0 / 1440 + 1) && j.found < d0 + DELIVERY_KEEP ? d0 + DELIVERY_KEEP : j.found; }   // the delivery (0.33.42)
  let t = j.found, left = j.leave || (realRepair(j) ? FAULT_LEAVE : CREW_LEAVE);
  for (let k = 0; k < 14 && left > 0; k++) {
    const d0 = Math.floor(t / 1440) * 1440;
    if (!playerShiftOn(d0 / 1440 + 1)) return t;         // your day off: the crew take it
    const a = Math.max(t, d0 + DAY_SHIFT[0]), n = Math.min(left, d0 + DAY_SHIFT[1] - a);
    if (n > 0) { left -= n; t = a + n; }
    if (left > 0) t = d0 + 1440;
    else if (!j.leave) t = Math.max(t, d0 + DAY_SHIFT[1]);   // held to the end of that shift
  }
  return t;
}
// a person's job laid over their plan: the segments of a claim at minute t, or null if it doesn't fit inside the
// work block they're in (not mid-ride, not on a tea break)
// jobRun reads planWhere (section 14): the plan alone, without jobs, so claiming never asks whereIs
// where parts are fetched and made: the Deck 6 architect's storage places on Deck 5 (main storage's shelves and the
// machine shop), the first one free of other jobs for the time, or nowhere (stand where you are) if none
const FETCH_AT = ['5-parts-1', '5-parts-2', '5-parts-3', '5-parts-4'], MAKE_AT = ['5-make-1', '5-make-2'];
// for the hover carts: beside the docks, in the cargo hold, in Deck 3's cold store (asked of the architects; skipped till they're in)
const CART_AT = ['5-cart-1', '5-cart-2'], HOLD_AT = ['5-hold-1', '5-hold-2'], COLD_AT = ['3-cold-1', '3-cold-2'];
const loadAt = j => j.cargo === 'stores' ? ['5-delivery-1'].concat(HOLD_AT) : HOLD_AT;   // the delivery loads at its crates (the Deck 6 architect's 0.38.35), when that place is in
// the shelves to try for a part: the one that stocks it first (the places' `stock`), then the rest
function shelvesFor(part) {
  const st = id => ((DECKS[5].places || []).find(p => p.id === id) || {}).stock || [];
  return FETCH_AT.filter(id => st(id).includes(part)).concat(FETCH_AT.filter(id => !st(id).includes(part)));
}
function storagePlace(ids, a, b) {
  const known = new Set(Object.values(DECKS).flatMap(d => (d.places || []).map(p => p.id)));
  for (const id of ids) if (known.has(id) && !SHIP.jobs.some(j => j.segs && j.status === 'claimed' && j.segs.some(s => s.placeId === id && s.from < b && a < s.to))) return id;
  return null;
}
// a place the crew may stand at for a chore's stop (0.33.40, so deliveries and vents happen where they are): one you
// stand at, not a machine's or storage (those have their own rules), nobody's plan has them there at its start, middle
// or end, and no other job is using it then. Else they work where they are, as before
function placeFreeFor(id, a, b) {
  const pl = placeById(id); if (!pl || !(pl.pose === 'stand' || pl.pose === 'work') || pl.type === 'event') return false;
  if (SHIP.jobs.some(j => j.segs && j.status === 'claimed' && j.segs.some(s => s.placeId === id && s.from < b && a < s.to))) return false;
  return !schedPeople().some(q => [a, (a + b) / 2, b - 1].some(x => { const w = planWhere(q, x); return w && w.placeId === id; }));
}
function jobRun(p, j, t, makeMin) {
  const w = planWhere(p, t);
  if (!w || w.act !== 'work' || w.moving || w.tag === 'tea') return null;
  const home = w.deck, segs = []; let c = t, dk = home;
  const go = d => { if (d !== dk) { segs.push({ from: c, to: c + JOB_RIDE, act: 'commute', deck: d, fromDeck: dk, type: 'lift', placeId: null }); c += JOB_RIDE; dk = d; } };
  const at = (min, tag, placeId = null) => { segs.push({ from: c, to: c + min, act: 'work', deck: dk, type: 'job', placeId, tag }); c += min; };
  if (j.kind === 'restock') {
    // a hover cart: from its dock, to the hold to load, then to the cold store (Deck 3) or the shelves, back to the dock
    // hold: the cart in hand for the crowd to draw (the performance engineer's): 'cart' empty, 'cartfull' loaded
    go(5);
    // the same dock out and back: one whose cart isn't already out on another run (about an hour, at most)
    const known = new Set((DECKS[5].places || []).map(p => p.id));
    const dock = CART_AT.find(id => known.has(id) && !SHIP.jobs.some(o => o.kind === 'restock' && o.segs && o.status === 'claimed' && o.segs[0] && o.segs.some(sg => sg.tag === 'cart' && sg.placeId === id) && o.start < c + 60 && c < o.end)) || null;
    const s0 = segs.length; at(4, 'cart', dock); at(10, 'load', storagePlace(loadAt(j), c, c + 10));
    const s1 = segs.length;
    if (j.cargo === 'meals') { go(3); at(15, 'unload', storagePlace(COLD_AT, c, c + 15)); }
    else at(20, 'unload', storagePlace(FETCH_AT, c, c + 20));
    const s2 = segs.length;
    if (j.cargo === 'meals') go(5);
    at(4, 'cart', dock);
    segs.forEach((sg, i) => { if (i >= s0) sg.hold = i >= s1 && i < s2 ? 'cartfull' : 'cart'; });
  } else if (jobKindOf(j)) {
    // a registered kind (0.33.47): parts if it needs any, then its stops, in crew.mins all told (shared out by the stops' minutes)
    const K = jobKindOf(j), sts = kindStops(j), mins = typeof K.crew.mins === 'function' ? K.crew.mins(j) : K.crew.mins || sts.reduce((a, x) => a + (x.mins || 0), 0) || 15;
    const of = sts.reduce((a, x) => a + (x.mins || 1), 0) || 1;
    if (j.parts.length) { go(5); at(JOB_FETCH, 'fetch', storagePlace(shelvesFor(j.parts[0]), c, c + JOB_FETCH)); if (makeMin) at(makeMin, 'make', storagePlace(MAKE_AT, c, c + makeMin)); }
    for (const st of sts) { const pl = placeById(st.placeId), n = Math.max(1, Math.round(mins * (st.mins || 1) / of)), s0 = segs.length; go(st.deck); at(n, st.tag || 'job', pl && (pl.machine ? st.placeId : pl.type === 'storage' ? storagePlace([st.placeId], c, c + n) : placeFreeFor(st.placeId, c, c + n) ? st.placeId : null)); if (st.hold) for (let i = s0; i < segs.length; i++) segs[i].hold = st.hold; }   // stop.hold: what's in their hands on the way and there (M1's carts)
  } else if (j.kind === 'chore') {
    // a chore: parts from storage if it needs any, then its stops in order (a delivery picks up, then drops off)
    if (j.parts.length) { go(5); at(JOB_FETCH, 'fetch', storagePlace(shelvesFor(j.parts[0]), c, c + JOB_FETCH)); if (makeMin) at(makeMin, 'make', storagePlace(MAKE_AT, c, c + makeMin)); }
    // the crew stand at a stop's place only if it's a machine's panel or a storage spot nobody else's job is using;
    // anywhere else (someone's desk, a seat, a lobby) they work where they are, so they never take a person's place
    const crewAt = (id, a, b) => { const pl = placeById(id); return !pl ? null : pl.machine ? id : pl.type === 'storage' ? storagePlace([id], a, b) : placeFreeFor(id, a, b) ? id : null; };
    const s0 = segs.length;
    for (const st of j.stops) { go(st.deck); at(st.mins, st.tag, crewAt(st.placeId, c, c + st.mins)); }
    if (j.chore === 'trays' || j.chore === 'garden') { const p0 = segs.findIndex((sg, i) => i >= s0 && sg.tag === 'pickup'); if (p0 >= 0) segs.forEach((sg, i) => { if (i > p0) sg.hold = 'cartfull'; }); }   // a cart of trays in hand
    if (j.chore === 'delivery') { const p0 = segs.findIndex((sg, i) => i >= s0 && sg.tag === 'pickup'), d0 = segs.findIndex((sg, i) => i > p0 && sg.tag === 'drop'); if (p0 >= 0) segs.forEach((sg, i) => { if (i > p0 && (d0 < 0 || i <= d0)) sg.hold = 'carry'; }); }   // the box in their arms from the pickup till it's set down at the drop (0.33.40; they walk there in the drop's own minutes)
  } else {
    const m = machineById(j.machine), K = MACHINE_KINDS[m.kind];
    go(5);
    const shelves = shelvesFor(j.parts[0]);
    if (makeMin) { at(JOB_FETCH, 'fetch', storagePlace(shelves, c, c + JOB_FETCH)); at(makeMin, 'make', storagePlace(MAKE_AT, c, c + makeMin)); }
    else at(JOB_FETCH, 'fetch', storagePlace(shelves, c, c + JOB_FETCH));
    go(m.deck); at(Math.round(JOB_TYPES[j.kind].work * (1 + .25 * (K.tier - 1)) * (j.logged ? .9 : 1)), 'job', panelPlace(m.id));   // j.logged: 24n's handover, 10% quicker
  }
  const done = c; go(home);
  return c <= w.until ? { segs, done, end: c } : null;
}
// a job is finished: its machine put right, or its cargo moved
function jobFinish(j, t, by) {
  j.status = 'done'; j.doneAt = t; j.doneBy = by;
  if (by === 'you' && j.event && typeof eventMine === 'function') eventMine('jobs', 1);   // your part in the event (section 18)
  if (!j.workDone) jobEffect(j, t, by);                  // a job you turn in already did its work (0.33.23)
}
// what finishing a job does to the ship: its machine put right, its cargo moved, a chore's effect
function jobEffect(j, t, by) {                           // your job (not a favour) also steps up the ship meters it helps (0.33.57)
  if (by !== 'you' || j.kind === 'favour' || j.meters) return jobDo(j, t, by);
  const before = shipMeters(); jobDo(j, t, by); meterStep(j, before);
}
function jobDo(j, t, by) {
  if (j.chore === 'garden' && by === 'you' && j.dropAt === undefined && typeof galleyCarryLand === 'function') galleyCarryLand(j.id);   // finished without ticking off the drop: they land now
  if (jobKindOf(j)) { try { jobKindOf(j).done(j, t, by); } catch (e) { console.warn('job kind ' + j.kind, e); } return; }   // a registered kind does its own (0.33.47)
  if (j.kind === 'chore' || j.kind === 'favour') { choreDone(j, t); return; }
  if (j.machine) {
    const s = SHIP.machines[j.machine], was = s && s.state;
    if (s) { s.cond = Math.max(s.cond, JOB_TYPES[j.kind].restore); s.state = machineState(s.cond); s.lastService = t; }
    if (s && by) simLater('repair', { who: by, machine: j.machine, state: was, job: j.kind, deck: j.deck, id: j.id, t: SIM_AT != null ? Math.max(t, SIM_AT) : t });   // never before the hour being run (social A's catch-up reads from there; 0.26.32); the state it was in; job: service, repair or overhaul (a payload never says kind: that's the note's own)
  } else if (j.cargo === 'meals') {
    // the meals left the hold when the run was set (cartClaim) and the galley lands them (section 16): at arriveAt
    // for the crew's runs, and when you unload for yours (0.33.19: cartWaiting held them till now)
    if (by === 'you' && typeof galleyCartLand === 'function') galleyCartLand(Math.floor(j.posted / 60));
  } else {
    for (const k in SHIP.hold) if (k !== 'meals') { SHIP.stores[k] = (SHIP.stores[k] || 0) + SHIP.hold[k]; delete SHIP.hold[k]; }
    for (const k in j.onCart || {}) SHIP.stores[k] = (SHIP.stores[k] || 0) + j.onCart[k];   // what you'd loaded and not unloaded (0.33.42)
    delete j.onCart;
  }
}
const jobCrew = p => p.work && (p.work.place === 'work:works' ? 'works' : p.work.place === 'work:engine' ? 'engine' : null);
function jobsHour(h) {
  const t = h * 60, jobs = SHIP.jobs, d = Math.floor(h / 24) + 1;
  for (const j of jobs) if (j.kind === 'team' && j.claimedBy === 'you' && j.status === 'claimed' && !j.youIn && !j.workDone && t >= j.start + TEAM_WAIT) teamYouOut(j.id);   // you didn't come (0.33.58)
  // 1. finished jobs (the crew's; yours finish when you finish them, or go back on the board after YOU_KEEP)
  for (const j of jobs) if (j.status === 'claimed' && j.claimedBy !== 'you' && j.done <= t) jobFinish(j, j.done, j.claimedBy);
  for (const j of jobs) if (j.kind === 'favour' && j.status !== 'done' && j.expires && t >= j.expires && !j.workDone) { j.status = 'done'; j.doneAt = t; j.doneBy = null; j.lapsed = true; }
  for (const j of jobs) if (j.claimedBy === 'you' && j.status === 'claimed' && j.kind !== 'favour' && !jobSide(j) && !j.workDone && !heldForYou(j) && t - Math.max(j.start, j.touched || 0) >= YOU_KEEP) { j.claimedBy = null; j.status = 'open'; delete j.start; delete j.touched; jobNote(j, 'lapse'); abandonNote(j); }
  reservedHour(t, jobs);
  // 2. the weekly delivery: storage topped up to STOCK, and a week of meals once the galley keeps a cold store
  if (weekday(d) === DELIVERY.day + deliveryLate(d) && h % 24 === DELIVERY.hour) {
    for (const k in STOCK) { const n = STOCK[k] - (SHIP.stores[k] || 0) - (SHIP.hold[k] || 0); if (n > 0) SHIP.hold[k] = (SHIP.hold[k] || 0) + n; }
    if (cartsCarryFood()) SHIP.hold.meals = Math.max(SHIP.hold.meals || 0, DELIVERY.meals);
    if (haulOn()) SHIP.manifest = manifestFor(d);         // the rest of the delivery, for 24d's manifest run (0.33.50)
  }
  if (haulOn() && weekday(d) === 3 && h % 24 === 6) SHIP.misplaced = misplacedFor(d);   // Thursday's stocktake (0.33.50)
  // between deliveries the machine shop makes what it can (0.33.41): at 15:00, one more of each part it can make that's
  // under half on its shelf (the filters and the like wait for Wednesday)
  if (h % 24 === 15) for (const k in STOCK) if (!NO_MAKE.has(k) && (SHIP.stores[k] || 0) < STOCK[k] / 2) SHIP.stores[k] = (SHIP.stores[k] || 0) + 1;
  // 3. post a job for each machine that needs one, or bring an unclaimed one up to date
  const open = new Map(); for (const j of jobs) if (j.status !== 'done' && !jobByStops(j)) open.set(j.machine || 'restock:' + j.cargo, j);
  for (const m of machineList()) {
    const st = SHIP.machines[m.id].state, kind = JOB_FOR[st], j = open.get(m.id);
    if (j && (j.status === 'claimed' || heldForYou(j))) continue;
    if (!kind) { if (j) jobFinish(j, t, null); continue; }   // put right some other way: the job goes
    if (j) {
      if (JOB_URGENCY[st] > j.urgency) {
        if (kind !== 'service' && !j.cause) { const c = faultPick(m, h); if (c) j.cause = c.id; }   // a service gone on to a fault: its cause now (0.33.46)
        j.kind = kind; j.urgency = JOB_URGENCY[st]; j.parts = faultParts(m, kind, faultCause(j)); j.found = Math.min(j.found, t);
        if (j.cause && kind === 'repair' && typeof caseOffer === 'function') caseOffer(j, h);   // 24k (0.33.47)
      }
      continue;
    }
    const found = kind === 'service' ? t + 60 * Math.round(2 + 22 * schedU(m.seed, h, 9)) + (realFor(m, d) ? FIND_LATE : 0) : t;
    // REAL_SHARE of them wore on unseen: found as a fault (the machine at the top of faulty), its cause picked now
    const late = kind === 'service' && realFor(m, d) && schedU(m.seed, h, 856) < REAL_SHARE && !jobs.some(x => x.machine === m.id && heldForYou(x));   // never a machine kept for a reserved (training, test) job
    if (late) { const s = SHIP.machines[m.id]; s.cond = Math.min(s.cond, 49); s.state = machineState(s.cond); }
    const kd = late ? 'repair' : kind, tl = kd === 'repair' ? traceFor(m, h) : null, cause = kd === 'service' ? null : faultPick(m, h, tl ? c => c.line === tl : null);   // traced: a cause on the line (0.33.59)
    jobs.push({ id: m.id + '@' + h, machine: m.id, deck: m.deck, kind: kd, urgency: JOB_URGENCY[late ? 'faulty' : st], posted: t, found, claimedBy: null,
                parts: faultParts(m, kd, cause), status: 'open', ...(cause ? { cause: cause.id } : {}), ...(late ? { late: true } : {}), ...(tl && cause ? { symptom: traceSymptom(tl, m.id) } : {}) });
    if (tl && cause) simLater('traced', { line: tl, machine: m.id, id: m.id + '@' + h });
    if (cause && typeof caseOffer === 'function') caseOffer(jobs[jobs.length - 1], h);   // 24k's case engine may make it a head-scratcher (0.33.47)
  }
  const restock = (cargo, deck) => { if (!open.has('restock:' + cargo)) jobs.push({ id: 'restock-' + cargo + '@' + h, machine: null, deck, kind: 'restock', cargo, urgency: 1, posted: t, found: t, claimedBy: null, parts: [], status: 'open' }); };
  if (Object.keys(SHIP.hold).some(k => k !== 'meals' && SHIP.hold[k] > 0)) restock('stores', 5);
  if (driftOn()) for (const m of machineList()) if (Math.abs(machineDrift(m.id)) >= 2 && !jobs.some(x => x.machine === m.id && x.drift && heldForYou(x))) tunePost(m, h, jobs, t + 60 * (1 + Math.floor(6 * schedU(m.seed, h, 869))));   // drift: a tune job (0.33.48)
  // (food runs come from cartClaim, the one rule the galley and the job list share: see cartPost)
  choresHour(h, jobs);
  for (const k in JOB_KINDS) if (JOB_KINDS[k].post) { try { JOB_KINDS[k].post(h, jobs); } catch (e) { console.warn('job kind ' + k, e); } }   // registered kinds post their own (0.33.47)
  eventJobsHour(h, jobs);
  // a food run nobody took goes unseen (its meals landed long ago, in the galley's books): before the claims
  for (const j of jobs) if ((j.cargo === 'meals' || j.chore === 'garden') && j.status === 'open' && t >= j.found + CART_GONE) { j.status = 'done'; j.doneAt = t; j.doneBy = null; }
  // 4. the crew on shift claim jobs: the most urgent first; each goes to the free crew member with the lowest
  // tier that may do it. Easy routine jobs wait CREW_LEAVE for you first.
  // busy till their last job's route ends, the walk back included: a job done at j.done still has them walking to j.end (0.33.38)
  const busy = new Map(); for (const j of jobs) if (j.claimedBy && j.claimedBy !== 'you' && j.end > t && j.kind !== 'team') busy.set(j.claimedBy, Math.max(busy.get(j.claimedBy) || 0, j.end));   // a team job's crew: by its window (teamClash)
  const crew = schedPeople().filter(jobCrew).sort((a, b) => (CREW_TIER[a.rank] || 0) - (CREW_TIER[b.rank] || 0) || (a.id < b.id ? -1 : 1));
  showHour(h, jobs);
  shareOut(t, jobs);
  // at most HOLD_MAX small jobs held for you: past that, the oldest go to the crew now (0.33.32)
  // which are kept (0.33.45, foundation 24.4): section 24's worksBand() puts services first at New and Steady, repairs first at
  // Trusted and Relied on; without it (or at Reliable), the newest first as before
  const band = typeof worksBand === 'function' ? worksBand() : null, pref = band === 'new' || band === 'steady' ? 'service' : band === 'trusted' || band === 'relied' ? 'repair' : null;
  const held = jobs.filter(j => j.status === 'open' && !j.claimedBy && !j.leave && !j.cargo && j.found <= t && t < leaveEnd(j))
    .sort((a, b) => (pref ? (b.kind === pref) - (a.kind === pref) : 0) || b.found - a.found || (a.id < b.id ? -1 : 1));
  // a mechanic's job held for you (a registered kind: a round, a tune, a haul, the drill; an incident's joint) takes one of those places (0.33.53, M2's ask: jobs
  // left for you stay 3-6 a day with the mechanics in); at least one ordinary job is still held
  const mech = jobs.filter(j => (jobKindOf(j) || j.chore === 'joint') && j.status === 'open' && !j.claimedBy && j.found <= t && (heldForYou(j) || (forYou(j) && t < leaveEnd(j)))).length;   // rounds, tuning, hauling, the drill, an incident's joint (the lead)
  for (const j of held.slice(Math.max(1, HOLD_MAX - mech))) j.released = true;
  const todo = jobs.filter(j => (j.status === 'open' || j.status === 'waiting') && !j.claimedBy && j.found <= t && t >= leaveEnd(j) && !heldForYou(j))
    .sort((a, b) => b.urgency - a.urgency || a.found - b.found || (a.id < b.id ? -1 : 1));
  for (const j of todo) if (j.machine && !j.unclaimed && !j.released && forYou(j) && leaveEnd(j) > j.found) { j.unclaimed = true; simLater('jobUnclaimed', { machine: j.machine, dept: null, id: j.id }); }
  for (const j of todo) {
    const missing = [], have = { ...SHIP.stores };
    for (const p of j.parts) { if (have[p] > 0) have[p]--; else missing.push(p); }
    if (missing.some(p => NO_MAKE.has(p)) && jobByStops(j)) { j.status = 'done'; j.doneAt = t; j.doneBy = null; continue; }   // a chore isn't worth the wait
    if (missing.some(p => NO_MAKE.has(p))) { j.status = 'waiting'; j.why = 'needs ' + missing.find(p => NO_MAKE.has(p)); continue; }
    const engine = j.machine && ENGINE_KINDS.has(machineById(j.machine).kind), tier = jobTier(j);
    for (const p of crew) {
      if (j.crew && p.id !== j.crew && t < j.found + 60) continue;   // a job placed for someone (SHOW_JOBS): theirs for its first hour
      if (jobKindOf(j) && !(jobKindOf(j).crew && jobKindOf(j).crew.can && jobKindOf(j).crew.can(p))) continue;   // a registered kind: who may (0.33.47)
      if ((busy.get(p.id) || 0) > t || jobCrew(p) !== (engine ? 'engine' : 'works') || (!engine && (CREW_TIER[p.rank] || 0) < tier) || !rankOk(p, j)) continue;   // a job kept for a rank waits for one (0.33.45)
      const run = jobRun(p, j, t, missing.length * JOB_MAKE);
      if (!run || teamClash(p.id, t, run.end)) continue;   // not into a team job they're in (0.33.58)
      for (const k of j.parts) if (SHIP.stores[k] > 0) SHIP.stores[k]--;
      if (SHIP.misplaced && j.parts.includes(SHIP.misplaced.part)) SHIP.misplaced = null;   // a fetch finds it on the wrong shelf and puts it right
      Object.assign(j, { claimedBy: p.id, status: 'claimed', start: t, segs: run.segs, done: run.done, end: run.end, made: missing.length });
      delete j.why; busy.set(p.id, run.end);
      break;
    }
  }
  suppliesHour(t, d);
  const bo = blackoutHour(h); if (bo && typeof eventScore === 'function') eventScore('blackout', bo.to - bo.from);
  if (typeof eventScore === 'function' && coldCabinsHour(h)) eventScore('coldCabins', 1);
  // done jobs are kept two days, for the board's history
  SHIP.jobs = jobs.filter(j => j.status !== 'done' || j.doneAt > t - 2880);
  if (typeof ladderTick === 'function') ladderTick(h);   // section 24's ladder, once a ship hour (0.33.45): it may reserve jobs (machinesNow is re-entry safe)
}
// ---- chores (0.33.19, the user's "more jobs for the job board") ----
// Small jobs that don't wait for a machine to wear: lamps, vents, calibrations, deliveries between decks,
// inspection rounds, small faults, filter swaps and seal checks. CHORES is the table: each type has its title, its
// tier (raised by the rooms it goes into: jobTier), minutes at each stop, parts to bring, how many a day (`per`), and
// where it can happen (`where()` -> candidates: { key, title, deck, room, machine?, stops: [{ deck, placeId, mins, tag }] }).
// The `per`s are tuned so about 5-6 jobs a day wait for you in all (machine jobs, cart runs and chores: the lead,
// 2026-10-16, from the user's "enough work, not overwhelming"; raised about 1 a day in 0.44.16, mostly the crew-tier filters and seals, the playtest's "a few more jobs on the
// board now that crew take jobs too", with HOLD_MAX 4: the board ~6.5 on a shift, ~3.5 of them yours to take). Each day's chores come from schedU (the type's seed, the day): the same ship gets the same jobs. Posted at their
// hour (07:00-18:00), one open at a time per place; small ones at your tier wait for you like any other (leaveEnd;
// a type may set its own `leave`, in minutes of the day shift). Finishing one does what it says (choreDone): a
// calibration or a filter swap helps its machine, a vent helps the deck's air, a round finds worn machines early.
const placesOf = (types, decks) => Object.keys(DECKS).filter(n => (!decks || decks.includes(+n)) && !DECKS[n].playerOnly).flatMap(n => (DECKS[n].places || []).filter(p => types.includes(p.type) && !p.machine).map(p => ({ ...p, deck: +n })));
const roomName = (n, r) => ((DECKS[n].rooms[r] || {}).name || '').toLowerCase();
const panelStop = (m, mins, tag) => ({ deck: m.deck, placeId: panelPlace(m.id), mins, tag });
const choreMachines = kinds => machineList().filter(m => kinds.includes(m.kind) && panelPlace(m.id));
const lobbyish = () => placesOf(['lift-wait', 'laundry']).filter((p, i, a) => a.findIndex(q => q.deck === p.deck && q.room === p.room) === i);
const DELIVERIES = [
  { key: 'linen', from: '5-parts-1', to: '4-laundry-1', title: 'Take clean linen to the laundry', bring: 'a crate of linen' },
  { key: 'medical', from: '5-parts-1', to: '3-infirmary-6', title: 'Take medical supplies to the infirmary', bring: 'a box of medical supplies' },
  { key: 'store', from: '5-parts-1', to: '3-shop-8', title: 'Restock the ship\'s store', bring: 'a crate of stock' },
  { key: 'bridge', from: '5-parts-1', to: '1-works-1', title: 'Take spares up to the bridge', bring: 'a box of bridge spares' },
  { key: 'galley', from: '5-hold-1', to: '3-cold-1', title: 'Take dry goods to the galley', bring: 'a sack of dry goods' },
];
const CHORES = {
  lamp:      { tier: 1, per: .6, parts: ['lamp'], text: 'Replace a lamp',
               where: () => lobbyish().map(p => ({ key: p.id, title: 'Replace a lamp: ' + roomName(p.deck, p.room), deck: p.deck, room: p.room, stops: [{ deck: p.deck, placeId: p.id, mins: 15, tag: 'lamp' }] })) },
  vent:      { tier: 1, per: .5, parts: [], text: 'Clean a vent', helps: { kinds: ['scrubber', 'airplant', 'fan'], by: 4 },
               where: () => lobbyish().concat(placesOf(['garden']).slice(0, 1)).map(p => ({ key: p.id, title: 'Clean a vent: ' + roomName(p.deck, p.room), deck: p.deck, room: p.room, stops: [{ deck: p.deck, placeId: p.id, mins: 20, tag: 'vent' }] })) },
  calibrate: { tier: 1, per: .8, parts: [], text: 'Calibrate', helps: { self: 6 },
               where: () => choreMachines(['oven', 'range', 'chiller', 'galleyplant', 'extractor', 'washer', 'cartdock', 'relay', 'databus', 'array', 'gasplant'])
                 .map(m => ({ key: m.id, title: 'Calibrate the ' + machineLabel(m).split(',')[0].toLowerCase(), deck: m.deck, room: m.room, machine: m.id, tier: MACHINE_KINDS[m.kind].tier, stops: [panelStop(m, 15, 'calibrate')] })) },
  delivery:  { tier: 1, per: .6, parts: [], text: 'Delivery',
               where: () => DELIVERIES.filter(r => placeById(r.from) && placeById(r.to)).map(r => { const a = placeById(r.from), b = placeById(r.to);
                 return { key: r.key, title: r.title + ', ' + deckIn(b.deck), deck: b.deck, room: b.room, bring: r.bring, stops: [{ deck: a.deck, placeId: a.id, mins: 5, tag: 'pickup' }, { deck: b.deck, placeId: b.id, mins: 10, tag: 'drop' }] }; }) },
  round:     { tier: 1, per: .4, parts: [], text: 'Inspection round', finds: true,
               where: () => [3, 4, 5].map(n => { const ms = choreMachines(['oven', 'range', 'chiller', 'galleyplant', 'cartdock', 'washer']).filter(m => m.deck === n), ps = ms.length >= 2 ? ms.slice(0, 3).map(m => panelStop(m, 5, 'inspect')) : lobbyish().filter(p => p.deck === n).slice(0, 3).map(p => ({ deck: n, placeId: p.id, mins: 5, tag: 'inspect' }));
                 return ps.length ? { key: 'deck' + n, title: 'Inspection round, ' + deckIn(n), deck: n, room: (placeById(ps[0].placeId) || {}).room, stops: ps } : null; }).filter(Boolean) },
  fault:     { tier: 1, per: .4, parts: [], text: 'Small fault', leave: 30,
               where: () => choreMachines(['lights', 'cartdock', 'washer', 'extractor']).map(m => ({ key: m.id, title: (m.kind === 'lights' ? 'Reset a tripped breaker: ' : m.kind === 'cartdock' ? 'Free a jammed cart dock: ' : 'Clear a fault: ') + machineLabel(m).split(',')[0].toLowerCase(), deck: m.deck, room: m.room, machine: m.id, stops: [panelStop(m, 10, 'fault')] })) },
  filter:    { tier: 2, per: 1.4, parts: ['filter'], text: 'Swap the filters', helps: { self: 10 },
               where: () => choreMachines(['scrubber', 'airplant', 'o2cell']).map(m => ({ key: m.id, title: 'Swap the filters: ' + machineLabel(m).split(',')[0].toLowerCase(), deck: m.deck, room: m.room, machine: m.id, tier: 2, stops: [panelStop(m, 20, 'filter')] })) },
  joint:     { tier: 1, per: 0, parts: ['seal'], text: 'Burst joint', where: () => [] },   // posted by an incident only (jointJobPost, 0.33.49)
  seal:      { tier: 2, per: 1, parts: [], text: 'Check a pressure seal', helps: { self: 5 },
               where: () => choreMachines(['hullseal', 'doorgear', 'valve', 'manifold']).map(m => ({ key: m.id, title: 'Check a pressure seal: ' + machineLabel(m).split(',')[0].toLowerCase(), deck: m.deck, room: m.room, machine: m.id, tier: 2, stops: [panelStop(m, 15, 'seal')] })) },
};
let CHORE_WHERE = null;
const choreWhere = k => (CHORE_WHERE || (CHORE_WHERE = Object.fromEntries(Object.keys(CHORES).map(c => [c, CHORES[c].where()]))))[k];
// the day's chores: [{ hour, kind, cand }] from the type's seed and the day
const CHORE_DAYS = new Map();
function choresOfDay(d) {
  if (CHORE_DAYS.has(d)) return CHORE_DAYS.get(d);
  const out = [];
  for (const kind of Object.keys(CHORES)) {
    const C = CHORES[kind], cs = choreWhere(kind), seed = machSeed('chore:' + kind); if (!cs.length) continue;
    const n = Math.floor(C.per) + (schedU(seed, d, 1) < C.per % 1 ? 1 : 0);
    for (let k = 0; k < n; k++) out.push({ hour: 7 + Math.floor(12 * schedU(seed, d, 10 + k)), kind, cand: cs[Math.floor(cs.length * schedU(seed, d, 30 + k))] });
  }
  if (d === SHIP_START.day) for (const c of out.slice().sort((a, b) => a.hour - b.hour).slice(0, 2)) c.hour = 6;   // your first morning: two on the board from the start (0.33.32; 06:00 from 0.33.33)
  CHORE_DAYS.set(d, out); for (const k of CHORE_DAYS.keys()) if (k < d - 2) CHORE_DAYS.delete(k);
  return out;
}
// a drifted machine's tune job (section 24e's kind), once: "Tune: Oven 2 (runs hot)"
function tunePost(m, h, jobs, found) {
  if (jobs.some(x => x.kind === 'tune' && x.machine === m.id && x.status !== 'done')) return null;
  const d = machineDrift(m.id), dc = (FAULT_CAUSES[m.kind] || []).find(c => c.setting), w = dc ? dc.shows.split('|') : [], word = d > 0 ? w[0] : w[w.length - 1];
  const j = jobMake('tune', { id: 'tune:' + m.id + '@' + h, machine: m.id, deck: m.deck, room: m.room, h, found, leave: TUNE_LEAVE, tier: jobTier({ machine: m.id }), title: 'Tune: ' + machineTitle(m.id) + (word ? ' (' + word + ')' : '') });
  jobs.push(j); return j;
}
function choresHour(h, jobs) {
  const d = Math.floor(h / 24) + 1, t = h * 60;
  for (const c of choresOfDay(d)) if (c.hour === (h % 24 + 24) % 24) {   // (day 0's hours are negative)
    const C = CHORES[c.kind], key = c.kind + ':' + c.cand.key;
    if (c.kind === 'calibrate' && c.cand.machine && machineDrift(c.cand.machine) && driftOn()) { tunePost(machineById(c.cand.machine), h, jobs, t); continue; }   // a drifted machine's calibration is its tuning (0.33.48)
    if (jobs.some(j => j.kind === 'chore' && j.status !== 'done' && j.chore + ':' + j.target === key)) continue;
    if (C.parts.some(k => (SHIP.stores[k] || 0) < STOCK[k] / 2)) continue;   // not while its parts run low: repairs come first
    jobs.push({ id: 'chore-' + key + '@' + h, machine: c.cand.machine || null, deck: c.cand.deck, room: c.cand.room, kind: 'chore', chore: c.kind, target: c.cand.key,
                title: c.cand.title, bring: c.cand.bring || null, tier: Math.max(C.tier, c.cand.tier || 0), stops: c.cand.stops.map(st => ({ ...st })),
                urgency: C.leave ? 1 : 0, leave: C.leave || null, posted: t, found: t, claimedBy: null, parts: C.parts.slice(), status: 'open' });
  }
}
// ---- the Works crew at work where you'll see them (0.33.40, the plan for 0.60.7) ----
// SHOW_JOBS: on Days 1 and 2 two small crew jobs are placed for you to see: a junior cleaning a vent by Deck 4's lift
// in the morning (09:00-10:15), and a delivery into the Works bay after lunch. Never held for you: the named junior takes it (j.crew,
// for its first hour; then any of the crew). showJob(day) -> { id, who, title, deck, place, from, to } | null for
// onboarding's lines ("That's Bea on the vent"): the day's job and who's on it, once it's claimed
const SHOW_JOBS = [
  { key: 'vent', day: 1, hour: 9, crew: 'silva-bea', chore: 'vent', title: 'Clean a vent: lift lobby', stops: [{ placeId: '4-lift-1', mins: 75, tag: 'vent' }] },   // 09:00-10:15: as the Monday briefing ends, when you and Zeke come down (0.33.43; 08:00-08:42 before; kept at 09:00 for the 09:00 shift, 0.44.14: at 10:00 Bea's already on a job)
  { key: 'tools', day: 2, hour: 13, crew: 'silva-bea', chore: 'delivery', title: 'Take new tools to the Works bay, Deck 5', bring: 'a box of tools',
    stops: [{ placeId: '5-hold-1', mins: 5, tag: 'pickup' }, { placeId: '5-bench-1', mins: 15, tag: 'drop' }] },
];
function showHour(h, jobs) {
  const d = Math.floor(h / 24) + 1, t = h * 60;
  for (const S of SHOW_JOBS) {
    if (S.day !== d || S.hour !== (h % 24 + 24) % 24 || S.stops.some(x => !placeById(x.placeId))) continue;
    const id = 'show-' + S.key + '@' + h, last = placeById(S.stops[S.stops.length - 1].placeId);
    if (jobs.some(j => j.id === id)) continue;
    jobs.push({ id, machine: null, deck: last.deck, room: last.room, kind: 'chore', chore: S.chore, target: S.key, title: S.title, bring: S.bring || null, tier: 1,
                stops: S.stops.map(x => ({ deck: placeById(x.placeId).deck, ...x })), urgency: 0, leave: null, posted: t, found: t, claimedBy: null, parts: [], status: 'open',
                crew: S.crew, released: true, shown: S.key });
  }
}
function showJob(day) {
  machinesNow();
  const j = SHIP.jobs.find(x => x.shown && Math.floor(x.posted / 1440) + 1 === day && x.claimedBy && x.claimedBy !== 'you'); if (!j) return null;
  const last = j.stops[j.stops.length - 1], seg = (j.segs || []).find(s => s.tag === last.tag);
  return { id: j.id, key: j.shown, who: j.claimedBy, title: j.title, deck: last.deck, place: seg && seg.placeId || null, from: j.start, to: j.done };
}
// every SHARE_EVERY-th new small job (by its id, so the same every way) goes to the crew at once, while at least SHARE_KEEP
// others are still held for you; j.shared marks it, with that count (once looked at, j.shareSeen)
function shareOut(t, jobs) {
  const heldNow = j => j.status === 'open' && !j.claimedBy && !j.released && !j.cargo && !heldForYou(j) && forYou(j) && j.found <= t && t < leaveEnd(j);
  for (const j of jobs) {
    if (j.shareSeen || j.status !== 'open' || j.claimedBy || j.found > t || j.cargo || heldForYou(j) || !forYou(j) || realRepair(j)) continue;
    j.shareSeen = true;
    if (!SHARE_ON || j.released || ((machSeed(j.id) >>> 0) % SHARE_EVERY)) continue;
    const n = jobs.filter(x => x !== j && heldNow(x)).length;
    if (n >= SHARE_KEEP) { j.released = true; j.shared = n; }   // j.shared: how many others were held for you then
  }
}
// a chore done: what it does to the ship
function choreDone(j, t) {
  const C = CHORES[j.chore] || {}, H = C.helps, bump = (id, by) => { const s = SHIP.machines[id]; if (s) { s.cond = Math.min(100, s.cond + by); s.state = machineState(s.cond); s.lastService = t; } };
  if (H && H.self && j.machine) bump(j.machine, H.self);
  if (j.chore === 'calibrate' && j.machine && SHIP.machines[j.machine]) delete SHIP.machines[j.machine].drift;   // calibrating settles a drift (0.33.48)
  if (H && H.kinds) for (const m of machineList()) if (H.kinds.includes(m.kind) && m.deck === j.deck) bump(m.id, H.by);
  if (C.finds) for (const x of SHIP.jobs) if (x.status !== 'done' && x.found > t && x.machine && (machineById(x.machine) || {}).deck === j.deck) x.found = t;
}

// ---- food by cart (B3, with the galley engineer): one rule, cartClaim, used by the galley's replays and live step
// alike, so they always agree. cartClaim(t, cold, { replay }) -> null | { meals, arriveAt }: whether a cart run sets
// off on the hour of t with the cold store at `cold`, how many meals it carries and when they land. The galley adds
// them to its cold store at arriveAt; section 17 only takes them out of the hold and puts the run on the job list.
// A replay ({ replay: true }) is pure and assumes the hold is stocked. A live call is the same rule, limited by
// what's in the hold, and it's remembered for its hour (asking again gives the same run): it takes the meals out
// of the hold and queues the run for the job list (cartPost).
function cartClaim(t, cold, o = {}) {
  if (!(cold >= 0)) return null;
  const h = Math.floor(t / 60), hr = (h % 24 + 24) % 24;
  if (!o.replay && CART_RUNS.has(h)) return CART_RUNS.get(h);
  let run = null;
  if (cold < CART_URGENT || (hr >= 9 && hr < 17 && cold < CART_DAILY)) {
    let meals = Math.min(CART_MEALS, coldCap() - cold);
    if (!o.replay) { if (SHIP.hold.meals === undefined) SHIP.hold.meals = DELIVERY.meals; meals = Math.min(meals, SHIP.hold.meals); }
    const fx = typeof shipEffectsAt === 'function' ? shipEffectsAt(5, h * 60) : null, lift = fx && fx.lift > 1 ? fx.lift : 1;
    if (meals > 0) run = { meals, arriveAt: h * 60 + CART_RUN + Math.round(6 * (lift - 1)) };
  }
  if (o.replay) return run;
  CART_RUNS.set(h, run);
  for (const k of CART_RUNS.keys()) if (k < h - 6) CART_RUNS.delete(k);
  if (run) { SHIP.hold.meals -= run.meals; CART_PENDING.push({ h, ...run, urgent: cold < CART_URGENT }); }
  return run;
}
// the run on the job list: the free Works crew member on shift with the lowest tier pushes the cart (dock, hold,
// lift, cold store, back); with nobody free it goes unseen. Since 0.33.16 a run that isn't urgent, set off on the
// day shift, waits an hour on the board for you (leaveEnd); then the crew take it (jobsHour), and one nobody takes
// in CART_GONE minutes goes unseen. The galley's books land the meals at arriveAt whoever pushes the cart.
const CART_GONE = 240;
function cartPost() {
  while (CART_PENDING.length) {
    const r = CART_PENDING.shift(), t = r.h * 60, id = 'restock-meals@' + r.h;
    if (SHIP.jobs.some(j => j.id === id)) continue;
    const j = { id, machine: null, deck: 3, kind: 'restock', cargo: 'meals', meals: r.meals, urgency: r.urgent ? 2 : 1, posted: t, found: t, claimedBy: null, parts: [], status: 'open', lands: r.arriveAt };
    SHIP.jobs.push(j);
    // a run set while time jumped (sleep, a skip) and only reaching the list now has already arrived in the galley's
    // books: it's history, never a job for anyone now (0.33.20: three stale runs once took both carts at once)
    if (r.arriveAt <= shipNow()) { j.status = 'done'; j.doneAt = r.arriveAt; j.doneBy = null; MACH_REV++; continue; }
    const md = t % 1440;
    if (!r.urgent && md >= DAY_SHIFT[0] && md < DAY_SHIFT[1]) { MACH_REV++; continue; }   // left for you first
    const busy = new Map(); for (const x of SHIP.jobs) if (x.status === 'claimed' && x.claimedBy !== 'you') busy.set(x.claimedBy, Math.max(busy.get(x.claimedBy) || 0, x.end));
    const crew = schedPeople().filter(p => jobCrew(p) === 'works').sort((a, b) => (CREW_TIER[a.rank] || 0) - (CREW_TIER[b.rank] || 0) || (a.id < b.id ? -1 : 1));
    for (const p of crew) {
      if ((busy.get(p.id) || 0) > t) continue;
      const run = jobRun(p, j, t, 0); if (!run) continue;
      Object.assign(j, { claimedBy: p.id, status: 'claimed', start: t, segs: run.segs, done: run.done, end: run.end, made: 0 });
      break;
    }
    if (!j.claimedBy) { j.status = 'done'; j.doneAt = r.arriveAt; j.doneBy = null; }
    MACH_REV++;
  }
}
// the galley's question (0.33.19, with the galley engineer's 0.29.13): is hour h's food run still on its way? True
// only while it's yours and not yet unloaded; then the galley holds its meals past arriveAt. A run just sitting on the
// board lands at arriveAt as in the galley's replays (0.33.20: holding those too kept the cold store low, so every
// hour ordered another run and the hold ran dry). Live play only: never in replays
const yourCartRun = h => SHIP.jobs.find(x => x.id === 'restock-meals@' + h && x.status === 'claimed' && x.claimedBy === 'you' && !x.workDone) || null;
function cartWaiting(h) { return !!yourCartRun(h); }
// (meals on their way, yours included, are counted by the galley when it asks cartClaim: section 16's 0.29.17; the
// galley owns the cold store's accounting, so section 17 doesn't add them too: 0.33.22)
// where a job puts someone at minute t, shaped like whereIs (plus `job`), or null. whereIs (section 14) asks this
// first, so the crew on the deck walk to their jobs (0.33.7). Off (jobWhere.on) until section 17 has run, and in
// test copies that want the plain plans.
let JOB_IDX = null, JOB_IDX_REV = -1;
function jobWhere(person, t) {
  if (!jobWhere.on) return null;
  machinesNow();
  if (JOB_IDX_REV !== MACH_REV) {
    JOB_IDX = new Map(); JOB_IDX_REV = MACH_REV;
    for (const j of SHIP.jobs) if (j.segsBy && j.status !== 'done') { for (const c in j.segsBy) { if (!JOB_IDX.has(c)) JOB_IDX.set(c, []); JOB_IDX.get(c).push(j); } }   // a team job: each member at their spot (0.33.58)
    else if (j.segs && j.claimedBy !== 'you') { if (!JOB_IDX.has(j.claimedBy)) JOB_IDX.set(j.claimedBy, []); JOB_IDX.get(j.claimedBy).push(j); }
  }
  const js = JOB_IDX.get(person.id); if (!js) return null;   // most people: no job, and no empty list made for them (0.26.40)
  for (let i = 0; i < js.length; i++) { const j = js[i], sg = j.segsBy ? j.segsBy[person.id] : j.segs; for (let k = 0; k < sg.length; k++) { const s = sg[k]; if (s.from <= t && t < s.to)
    return { deck: s.deck, act: s.act, type: s.type, placeId: s.placeId, moving: s.act === 'commute', fromDeck: s.fromDeck, from: s.from, until: s.to, tag: s.tag, job: j.id, hold: s.hold }; } }
  return null;
}
// ---- your side of the job list (the device and the board come later, with the player engineer) ----
// the board: jobs found and not done, the most urgent first
function jobsBoard() { machinesNow(); const t = shipNow(); return SHIP.jobs.filter(j => j.status !== 'done' && j.kind !== 'favour' && j.found <= t && !(typeof caseHidden === 'function' && caseHidden(j))).sort((a, b) => b.urgency - a.urgency || a.found - b.found); }
// your jobs on the ship notes bus (Pillar 4, for onboarding's Settling-in and the social side): simNote('job', { id,
// step, reserved, ... }) when you take one ('take'), tick off a stop ('stop', with k and its tag), finish its work ('done'),
// turn it in ('turnin'), give it up ('drop') or leave it till it lapses ('lapse', sent once the hour has run). reserved:
// jobReserve's slot, or 0. Inert until section 13's simNote is in
function jobNote(j, step, o) { if (j.kind !== 'favour') simLater('job', { id: j.id, step, reserved: j.reserved || 0, job: j.chore || j.kind, machine: j.machine || null, ...o }); }
// for the social side's reputation and memories (social A): a job of yours you gave up or let lapse unfinished
// (jobAbandoned), and a machine's job left for you that went to the crew because you didn't take it (jobUnclaimed,
// once a job, only for a job that was really held for you on your shift). dept: null, the social side works it out
// from the machine (repDeptOf). A repair done (simNote('repair')) is sent by jobEffect
const abandonNote = j => { if (j.kind !== 'favour' && !j.workDone) simLater('jobAbandoned', { machine: j.machine || null, dept: null, id: j.id }); };
function claimJob(id) {
  const j = jobsBoard().find(x => x.id === id);
  if (!j || j.claimedBy || (!jobSide(j) && SHIP.jobs.some(x => x.claimedBy === 'you' && x.status === 'claimed' && x.kind !== 'favour' && !jobSide(x))) || (playerTier() < jobTier(j) && !heldForYou(j)) || !rankOk('you', j) || (j.machine && ENGINE_KINDS.has(machineById(j.machine).kind)) || bridgeBars(j)) return false;
  j.claimedBy = 'you'; j.status = 'claimed'; j.start = shipNow(); delete j.segs; delete j.done; delete j.end; MACH_REV++; jobNote(j, 'take'); simFlush(); return true;   // no crew route left on it
}
function dropJob(id) {
  const j = SHIP.jobs.find(x => x.id === id && x.claimedBy === 'you' && x.status === 'claimed');
  if (!j) return false; j.claimedBy = null; j.status = 'open'; delete j.start; MACH_REV++; jobNote(j, 'drop'); abandonNote(j); simFlush(); return true;
}
// take a part off the storage shelf (you carry it; carrying is the player engineer's), or put one back
function takePart(part) { machinesNow(); if (!(SHIP.stores[part] > 0)) return false; SHIP.stores[part]--; if (SHIP.misplaced && SHIP.misplaced.part === part) SHIP.misplaced = null; MACH_REV++; return true; }
function returnPart(part) { if (typeof part !== 'string' || !part) return false; machinesNow(); SHIP.stores[part] = (SHIP.stores[part] || 0) + 1; MACH_REV++; return true; }
// progress on your job (a part fitted, repair minutes done): the 12-hour lapse counts from the last progress
function touchJob(id) { const j = SHIP.jobs.find(x => x.id === id && x.claimedBy === 'you' && x.status === 'claimed'); if (!j) return false; j.touched = shipNow(); return true; }
function finishJob(id) {
  machinesNow(); const j = SHIP.jobs.find(x => x.id === id && x.claimedBy === 'you' && x.status === 'claimed');
  if (!j) return false;
  const was = j.workDone;
  if (TURN_IN) { if (!j.workDone) { jobEffect(j, shipNow(), 'you'); j.workDone = shipNow(); } }   // done, awaiting turn-in
  else jobFinish(j, shipNow(), 'you');
  machRecord(MACH_HOUR - 1); MACH_REV++;
  if (!was) jobNote(j, 'done'); if (!TURN_IN) jobNote(j, 'turnin'); simFlush(); return true;
}
// turning jobs in at the board (0.33.23, for the interactions engineer and plans/pillar3-plan.md "Jobs: take and turn in
// at the board"). Your job's stops are ticked off with jobStepDone; after the last one (or finishJob) its work is done:
// the machine is put right, the lamp works, the meals land (j.workDone, the minute). It stays yours (no 12-hour
// lapse), off the board, and myJob() still gives it, until you turn it in at a job board (turnInJob), which completes
// it. TURN_IN off (for now): finishJob completes your job at once, as before, so section 15 needn't change; on:
// finishJob only does the work, and turnInJob completes it. The lead turns it on when the board's Turn in lands.
let TURN_IN = true;                                      // on from 0.37.3: 15b's job board has Turn it in (the lead)
// jobStepDone(id, stepIndex) -> { ok, left, done }: a stop of your job done (stepIndex into jobStops(j), fetch
// included); left: stops still to do; done: its work is done (after the last stop), awaiting turn-in
function jobStepDone(id, k, res) {
  machinesNow(); const j = SHIP.jobs.find(x => x.id === id && x.claimedBy === 'you' && x.status === 'claimed');
  const n = j ? jobStops(j).length : 0;
  if (!j || !(k >= 0 && k < n) || (j.kind === 'favour' && k === n - 1)) return { ok: false, left: n, done: !!(j && j.workDone) };   // a favour goes back by favourTurnIn
  const K = jobKindOf(j); let kr;
  if (K && K.stepDone) { try { kr = K.stepDone(j, k, res || null, shipNow()); } catch (e) { console.warn('job kind ' + j.kind, e); } }
  if (K && K.veto && kr === false) { simFlush(); return { ok: false, left: n - (j.stepsDone || []).length, done: !!j.workDone, retry: true }; }   // def.veto: a wrong pick leaves the stop to do again (M2's)
  if (res && typeof res === 'object') { (j.res || (j.res = {}))[k] = JSON.parse(JSON.stringify(res)); }   // a step's result ({ pick }, { value }): kept for the kind's done (0.33.47)
  j.stepsDone = [...new Set([...(j.stepsDone || []), k])].sort((a, b) => a - b); j.touched = shipNow();
  if (jobStops(j)[k].step === 'drop' && j.dropAt === undefined) {
    j.dropAt = shipNow();                                // a delivery's arrival (traysArrivedAt, carryArrivedAt)
    if (j.chore === 'garden' && typeof galleyCarryLand === 'function') galleyCarryLand(j.id);   // the crates land in the cold store now (section 16)
  }
  const left = n - j.stepsDone.length - (j.kind === 'favour' && !j.stepsDone.includes(n - 1) ? 1 : 0);   // a favour's last step is handing it back
  const fresh = !j.workDone;
  if (!left && !j.workDone && typeof caseFitted === 'function' && caseFitted(j)) { MACH_REV++; simFlush(); return { ok: true, left: n, done: false, wrong: true }; }   // 24k: the wrong fix, the machine not put right (0.33.47)
  if (!left && !j.workDone) { jobEffect(j, shipNow(), 'you'); j.workDone = shipNow(); machRecord(MACH_HOUR - 1); }
  MACH_REV++; jobNote(j, 'stop', { k, tag: jobStops(j)[k].step }); if (fresh && j.workDone) jobNote(j, 'done'); simFlush();
  return { ok: true, left, done: !!j.workDone, ...(typeof kr === 'string' ? { say: kr } : {}) };   // say: the kind's words after the step (P's, for M1)
}
// turnInJob(id) -> true | false: at a job board, a job whose work is done is complete
function turnInJob(id) {
  machinesNow(); const j = SHIP.jobs.find(x => x.id === id && x.claimedBy === 'you' && x.status === 'claimed' && x.workDone && x.kind !== 'favour');
  if (!j) return false; jobFinish(j, shipNow(), 'you'); MACH_REV++; jobNote(j, 'turnin'); simFlush(); return true;
}

// ---- event jobs (Pillar 3, C7): a ship-wide event's `jobs` data, posted on the job board for its phase ----
// SHIP_EVENTS.<id>.jobs = { <phase>: [ { id?, kind, title?, where?, place?, machine?, deck?, tier?, mins?, parts?,
// urgency?, leave? }, ... ] } (section 18, the events engineer). Each is posted once per event and phase when
// eventNow() says so, tagged `event: <id>`, as a chore: a kind from CHORES with no place picks one of its own places;
// otherwise `place` (a place id), `machine` (its panel) or `where` (a word in a room's name, or a place type) says where.
// The crew take them as usual; small ones at your tier wait `leave` minutes (default 60) of the day shift for you.
// postEventJob(spec, { event, forYou }) posts one now (a meeting's choice: forYou claims it for you).
const eventDef = id => typeof SHIP_EVENTS === 'undefined' ? null : Array.isArray(SHIP_EVENTS) ? SHIP_EVENTS.find(e => e.id === id) || null : SHIP_EVENTS[id] || null;
const EVENT_JOB_TEXT = { secure: 'Secure loose things', check: 'Check', fetch: 'Fetch', carry: 'Carry', clean: 'Clean up', set: 'Set up', patch: 'Patch', tea: 'Bring tea' };
// one stop of section 18's event jobs: { placeId } | { deck, room: RegExp, types } | { deck, machine: kind }, plus mins, tag
function eventStopOf(x) {
  const out = st => st && { deck: st.deck, placeId: st.placeId || null, mins: x.mins || 15, tag: x.tag || 'event', at: st.at || null, room: st.room, machine: st.machine };
  if (x.placeId) { const pl = placeById(x.placeId); return pl ? out({ deck: pl.deck, placeId: pl.id, room: pl.room }) : null; }
  if (x.machine) {                                       // its kind on that deck, else one whose id names it (Deck 5's junction carries its lights)
    const on = m => !x.deck || m.deck === x.deck, named = m => m.id.split('-')[1] === x.machine;
    const m = [m => m.kind === x.machine && panelPlace(m.id), m => m.kind === x.machine, m => named(m) && panelPlace(m.id), named].reduce((f, test) => f || machineList().find(m => on(m) && test(m)), null);
    return m ? out({ deck: m.deck, placeId: panelPlace(m.id), room: m.room, at: m.panel.slice(), machine: m.id }) : null; }
  if (x.room) {
    const D = DECKS[x.deck]; if (!D) return null;
    const rx = x.room instanceof RegExp ? x.room : new RegExp(String(x.room), 'i'), rooms = Object.keys(D.rooms).filter(r => rx.test(D.rooms[r].name || ''));
    const pl = (D.places || []).find(p => rooms.includes(p.room) && !p.machine && (!x.types || x.types.includes(p.type)));
    if (pl) return out({ deck: x.deck, placeId: pl.id, room: pl.room });
    const at = rooms.length && machRoomTile(x.deck, rooms[0]); return at ? out({ deck: x.deck, room: rooms[0], at }) : null;
  }
  return null;
}
function eventStop(spec) {
  const pl = spec.place && placeById(spec.place); if (pl) return { deck: pl.deck, placeId: pl.id, room: pl.room };
  const m = spec.machine && machineById(spec.machine); if (m) return { deck: m.deck, placeId: panelPlace(m.id), room: m.room, machine: m.id, at: m.panel.slice() };
  const w = String(spec.where || '').toLowerCase(); if (!w) return null;
  for (const n of Object.keys(DECKS).map(Number).filter(n => (!spec.deck || n === spec.deck) && !DECKS[n].playerOnly)) {
    const D = DECKS[n], rooms = Object.keys(D.rooms).filter(r => (D.rooms[r].name || '').toLowerCase().includes(w));
    const ps = (D.places || []).filter(p => !p.machine && (rooms.includes(p.room) || p.type === w));
    const stand = ps.find(p => /lift-wait|storage|laundry|garden|shop/.test(p.type)) || ps[0];
    if (stand) return { deck: n, placeId: stand.id, room: stand.room };
    if (rooms.length) { const at = machRoomTile(n, rooms[0]); if (at) return { deck: n, placeId: null, room: rooms[0], at }; }
  }
  return null;
}
function eventJob(spec, ev, t, key) {
  let where = null, title = spec.title, machine = null, stops;
  if (Array.isArray(spec.stops)) {                        // section 18's shape: its own stops
    stops = spec.stops.map(eventStopOf); if (!stops.length || stops.some(x => !x)) return null;
    const last = stops[stops.length - 1]; where = { deck: last.deck, room: last.room };
    stops = stops.map(({ room, machine, ...x }) => x);
  } else if (CHORES[spec.kind] && !spec.place && !spec.machine && !spec.where) {
    const cs = choreWhere(spec.kind); if (!cs.length) return null;
    const c = cs[Math.abs(machSeed(key)) % cs.length]; title = title || c.title; machine = c.machine || null; where = { deck: c.deck, room: c.room }; stops = c.stops.map(x => ({ ...x }));
  } else {
    const st = eventStop(spec); if (!st) return null;
    machine = st.machine || null; where = st;
    stops = [{ deck: st.deck, placeId: st.placeId, mins: spec.mins || 20, tag: spec.kind || 'event', at: st.at || null }];
    title = title || (EVENT_JOB_TEXT[spec.kind] || 'Event job') + (st.room ? ': ' + roomName(st.deck, st.room) : '');
  }
  return { id: key, machine, deck: where.deck, room: where.room, kind: 'chore', chore: spec.kind, target: spec.id || spec.kind, event: ev, eventJob: spec.id || null, title,
           bring: spec.bring || null, tier: spec.tier || 1, stops, urgency: spec.urgency ?? 1, leave: spec.leave ?? 60, posted: t, found: t,
           claimedBy: null, parts: (spec.parts || []).slice(), status: 'open' };
}
function eventJobsHour(h, jobs) {
  if (typeof eventNow !== 'function') return;
  const t = h * 60, ev = eventNow(t); if (!ev || !ev.id) return;
  // the phase's list: section 18's eventMod('jobs') (which carries a phase's list on until one clears), else the
  // event's jobs[phase]. Each job is posted once per run of the event (its start day in the key), at its `at` minute
  const viaMod = typeof eventMod === 'function' ? eventMod('jobs', undefined, t) : null;
  const def = eventDef(ev.id), list = Array.isArray(viaMod) ? viaMod : def && def.jobs && def.jobs[ev.phase]; if (!Array.isArray(list)) return;
  const start = Math.floor(t / 1440) - (ev.day || 0);
  list.forEach((spec, k) => {
    if (Number.isFinite(spec.at) && Math.floor((t % 1440) / 60) !== Math.floor(spec.at / 60)) return;   // only in the hour of its minute (afterglow's 08:00 is the next morning)
    const key = 'event:' + ev.id + ':' + (spec.id || ev.phase + k) + '@' + start;
    if (jobs.some(j => j.id === key)) return;
    const j = eventJob(spec, ev.id, Number.isFinite(spec.at) ? Math.max(t, Math.floor(t / 1440) * 1440 + spec.at) : t, key); if (!j) return;
    jobs.push(j);
    // you volunteered for it at the meeting before it went up (section 18 sets SHIP.event.mine['wants:<job id>']): it's
    // yours as it's posted, if you aren't on another board job (claimed directly: claimJob would re-enter the hour)
    const E = typeof SHIP !== 'undefined' && SHIP.event, mine = jobs.some(x => x.claimedBy === 'you' && x.status === 'claimed' && x.kind !== 'favour');
    if (spec.id && E && E.id === ev.id && E.mine && E.mine['wants:' + spec.id] && !mine) Object.assign(j, { claimedBy: 'you', status: 'claimed', start: j.posted });
  });
}
function postEventJob(spec, o = {}) {
  machinesNow(); const ev = o.event || (typeof eventNow === 'function' && eventNow() ? eventNow().id : 'event');
  const key = 'event:' + ev + ':' + (spec.id || spec.kind) + '@' + Math.floor(shipNow());
  const j = eventJob(spec, ev, shipNow(), key); if (!j) return null;
  SHIP.jobs.push(j); MACH_REV++;
  if (o.forYou) claimJob(j.id);
  return j.id;
}

// blackouts (Pillar 3, C7: section 18's eventMod('effect', 'blackouts')): while it's on, now and then one deck goes to
// emergency lighting for 15-60 minutes, likelier the worse the power (from the conditions at the hour's start). At most
// one an hour, inside its hour, so only ever one deck at a time. blackoutHour(h) -> { deck, from, to } | null is pure;
// jobsHour scores each one as the event's 'blackout' thread (eventScore('blackout', minutes)) as its hour is run;
// blackoutAt(t) -> the blackout at minute t or null; deckLook(deck).dark while it's that deck's
const BLACKOUT_SEED = machSeed('blackout');
function blackoutHour(h) {
  if (typeof eventMod !== 'function' || eventMod('effect', 'blackouts', h * 60) !== true) return null;
  const c = MACH_HIST.get(histHour((h - 1) * 60)), power = c ? systemsFrom(c).power : 100, u = k => schedU(BLACKOUT_SEED, h, k);
  if (u(1) >= .15 + .45 * (1 - power / 100)) return null;
  const decks = Object.keys(DECKS).map(Number).filter(n => !DECKS[n].playerOnly && n !== 7).sort(), deck = decks[Math.floor(u(2) * decks.length)], len = 15 + Math.floor(46 * u(3));
  const from = h * 60 + Math.floor(u(4) * (61 - len));
  return { deck, from, to: from + len };
}
// cold guest cabins (0.33.31, the diplomatic visit's 'coldCabins' thread): an hour while guests are aboard (section
// 18's eventMod('effect', 'guests')) with Deck 4's heating poor (its heating plant or heating pumps faulty or worse
// at the hour's start). Pure; jobsHour scores each such hour as eventScore('coldCabins', 1)
function coldCabinsHour(h) {
  if (typeof eventMod !== 'function' || eventMod('effect', 'guests', h * 60) !== true) return false;
  const c = MACH_HIST.get(histHour((h - 1) * 60));
  return machineList().some(m => m.deck === 4 && (m.kind === 'heater' || m.kind === 'heatpump') && (c ? c[m.id] ?? 100 : 100) < 50);
}
function blackoutAt(t) { const b = blackoutHour(Math.floor(t / 60)); return b && t >= b.from && t < b.to ? b : null; }

// trays by cart (Pillar 3, C7, with the galley engineer's 0.29.18): an event asks for trays, the galley plates them
// and calls cartTrays({ trays, at, to: 'bridge' }) (live, once a day): a job to push them from the servery (Deck 3) to
// `to` (a word in a room's name, 'bridge' by default). Left for you first (30 minutes of the day shift: they're hot),
// then a crew member. Nothing lands anywhere: the galley has taken the portions already. -> the job's id, or null
function cartTrays(o = {}) {
  machinesNow();
  const at = Number.isFinite(o.at) ? o.at : shipNow(), key = 'trays:' + (o.to || 'bridge') + '@' + Math.floor(at / 1440);
  if (SHIP.jobs.some(j => j.id === key)) return key;
  const from = placesOf(['grab-shelf', 'servery-queue'], [3])[0], to = eventStop({ where: o.to || 'bridge', deck: o.to ? undefined : 1 });
  if (!from || !to) return null;
  const n = Math.max(1, Math.round(o.trays || 1));
  SHIP.jobs.push({ id: key, machine: null, deck: to.deck, room: to.room, kind: 'chore', chore: 'trays', target: o.to || 'bridge', event: o.event || null,
                   title: 'Take ' + n + ' tray' + (n > 1 ? 's' : '') + ' up to the ' + (roomName(to.deck, to.room) || o.to || 'bridge'), bring: 'a cart of ' + n + ' hot trays',
                   tier: 1, stops: [{ deck: 3, placeId: from.id, mins: 5, tag: 'pickup' }, { deck: to.deck, placeId: to.placeId, mins: 10, tag: 'drop', at: to.at || null }],
                   urgency: 1, leave: 30, posted: at, found: at, claimedBy: null, parts: [], status: 'open' });
  MACH_REV++; return key;
}

// garden crates (0.33.34, for the galley engineer's working garden): the galley harvests and calls gardenCarry({ at,
// crates, title? }) (live): a job to carry the crates by hover cart from the garden to the cold store (3-cold-1/2).
// Left for you first (60 minutes of the day shift; none on your days off), then a crew member; one nobody takes in
// CART_GONE minutes counts as carried. -> the job's id ('garden@<minute>'), or null. carryWaiting(id, t) says whether
// the crates are still on their way (the galley holds them till then); carryArrivedAt(id) when they got there. When
// you tick off the drop at the cold store, the galley's galleyCarryLand(id) lands them at once (jobStepDone)
const GARDEN_PICKUP = ['3-crates-1'];                    // the architect's pickup place, when it's in; else the garden spot nearest the glass doors
function gardenPickup() {
  const ps = DECKS[3] && DECKS[3].places || [], own = ps.find(p => GARDEN_PICKUP.includes(p.id));
  if (own) return own;
  const g = ps.filter(p => p.type === 'garden' && !p.machine && p.pose !== 'sit'), d = p => (p.at[0] - 11) ** 2 + (p.at[1] - 10) ** 2;
  return g.sort((a, b) => d(a) - d(b) || (a.id < b.id ? -1 : 1))[0] || null;
}
function gardenCarry(o = {}) {
  machinesNow();
  const at = Math.floor(Number.isFinite(o.at) ? o.at : shipNow()), key = 'garden@' + at;
  if (SHIP.jobs.some(j => j.id === key)) return key;
  const from = gardenPickup(), to = placeById(COLD_AT[0]) ? COLD_AT[0] : null;
  if (!from || !to) return null;
  const n = Math.max(1, Math.round(o.crates || 1));
  SHIP.jobs.push({ id: key, machine: null, deck: 3, room: placeById(to).room, kind: 'chore', chore: 'garden', target: 'cold', crates: n,
                   title: o.title || 'Carry ' + n + ' crate' + (n > 1 ? 's' : '') + ' from the garden to the cold store', bring: 'a hover cart for ' + n + ' crate' + (n > 1 ? 's' : ''),
                   tier: 1, stops: [{ deck: 3, placeId: from.id, mins: 5, tag: 'pickup' }, { deck: 3, placeId: to, mins: 8, tag: 'drop' }],
                   urgency: 0, leave: 60, posted: at, found: at, claimedBy: null, parts: [], status: 'open' });
  MACH_REV++; return key;
}
// when a garden run's crates reached the cold store: a crew run, the end of its drop-off; yours, when you ticked it
// off; one nobody took, when it was given up. null while on the way. Reads the job list only
function carryArrivedAt(id) {
  const j = SHIP.jobs.find(x => x.id === id && x.chore === 'garden');
  if (!j) return null;
  if (j.claimedBy && j.claimedBy !== 'you') { const d = (j.segs || []).filter(sg => sg.tag === 'drop').pop(); return d ? d.to : j.doneAt ?? null; }
  if (j.claimedBy === 'you') return j.dropAt ?? j.workDone ?? (j.status === 'done' ? j.doneAt : null);
  return j.status === 'done' ? j.doneAt : null;
}
// carryWaiting(id, t = now) -> true while the crates aren't at the cold store yet (an unknown id: false)
function carryWaiting(id, t = shipNow()) {
  if (!SHIP.jobs.some(x => x.id === id && x.chore === 'garden')) return false;
  const a = carryArrivedAt(id); return a === null || a > t;
}

// when the day's trays reached `to` (0.33.28, for the galley's bridgeHungry score): the ship minute they arrived, or
// null while they haven't. A crew run: the end of its drop-off (planned when it's claimed, so compare with the minute
// you ask about); yours: when you ticked off the drop-off (jobStepDone) or finished the job. It reads the job list only
function traysArrivedAt(day, to = 'bridge') {
  const j = SHIP.jobs.find(x => x.id === 'trays:' + to + '@' + (day - 1));   // day: the ship day (1 = Day 1); cartTrays keys by day - 1
  if (!j) return null;
  if (j.claimedBy && j.claimedBy !== 'you') { const d = (j.segs || []).filter(sg => sg.tag === 'drop').pop(); return d ? d.to : j.doneAt ?? null; }
  if (j.claimedBy === 'you') return j.dropAt ?? j.workDone ?? (j.status === 'done' ? j.doneAt : null);
  return null;
}

// ---- reserved jobs (Pillar 4, for the onboarding engineer's first week) ----
// jobReserve(kind, day, at, slot) -> id | null: a real Tier 1 fault, due on cue, held for you. A machine of `kind`
// (a machine kind like 'lights' or 'washer', or a machine id) that has a panel place and is at your tier (Deck 4
// first; any such machine if none of that kind), not one another reserved job is on, goes faulty at `at` (minutes from
// midnight) on ship day `day`, and its repair job is on the board from then, "asked for you": the crew never take it
// and it never lapses, until the end of your shift that day (o.until, a ship minute, to say otherwise), when it's
// released as an ordinary job. It needs a part off the shelf and a part made in the machine shop (its stops: fetch,
// make, job; j.make names the made part). slot: 1-3 (onboarding's: Monday's shadow shift, Monday afternoon, Tuesday's
// solo job), carried as j.reserved and in simNote('job'). Asking again for a slot replaces its job if it isn't
// taken yet. jobReserved(slot) -> id | null; jobRelease(slot?) releases one (or all) not yet taken. No R(); nothing
// happens unless it's called.
const RESERVE_MAKE = 'bracket';                          // the part you make in the machine shop for a reserved job
const RESERVE_MAKE_MINS = 30;                            // how long you take to make it (j.makeMins, read by section 15; a first lesson, 0.33.37)
const heldForYou = j => (!!j.reserved && !j.freed && j.status !== 'done') || (typeof caseHeld === 'function' && j.status !== 'done' && !!caseHeld(j));   // 24k: a case's job is kept for you while it runs (0.33.47)
function jobReserve(kind, day, at, slot = 1, o = {}) {
  machinesNow();
  const due = (day - 1) * 1440 + at, until = Number.isFinite(o.until) ? o.until : (day - 1) * 1440 + DAY_SHIFT[1];
  const old = SHIP.jobs.find(j => j.reserved === slot && heldForYou(j));
  if (old && old.claimedBy) return old.id;
  if (old) SHIP.jobs = SHIP.jobs.filter(j => j !== old);
  const busy = new Set(SHIP.jobs.filter(heldForYou).map(j => j.machine)), byId = machineById(kind);
  const ok = m => !m.stub && panelPlace(m.id) && jobTier({ machine: m.id }) <= (o.tier || playerTier()) && !ENGINE_KINDS.has(m.kind);   // o.tier: a test job's machine may be above yours (0.33.45)
  const all = machineList().filter(ok).sort((a, b) => (a.deck === 4 ? 0 : 1) - (b.deck === 4 ? 0 : 1) || (a.id < b.id ? -1 : 1));
  const d4 = all.filter(m => m.deck === 4), free = xs => xs.find(m => !busy.has(m.id));   // Deck 4 first, a free one first, the kind asked for first
  const pick = byId && ok(byId) ? byId : free(d4.filter(m => m.kind === kind)) || free(d4) || d4.find(m => m.kind === kind) || d4[0] || free(all.filter(m => m.kind === kind)) || free(all) || all[0];
  if (!pick) return null;
  SHIP.jobs = SHIP.jobs.filter(j => !(j.machine === pick.id && j.status === 'open' && !j.claimedBy && !j.reserved));   // its own ordinary job, if any: this one stands for it
  const id = 'reserve' + slot + ':' + pick.id + '@' + due;
  SHIP.jobs.push({ id, machine: pick.id, deck: pick.deck, kind: 'repair', urgency: 1, posted: due, found: due, until, reserved: slot, make: RESERVE_MAKE, makeMins: RESERVE_MAKE_MINS,
                   claimedBy: null, parts: [MACHINE_KINDS[pick.kind].part, RESERVE_MAKE], status: 'open', ...(o.train ? { train: o.train } : {}) });
  const oc = o.cause && (FAULT_CAUSES[pick.kind] || []).find(c => c.id === o.cause);   // o.cause (24k, 0.33.47): a reserved fault with that cause, its part, nothing to make
  if (oc) { const J = SHIP.jobs[SHIP.jobs.length - 1]; J.cause = oc.id; J.parts = faultParts(pick, 'repair', oc); delete J.make; delete J.makeMins; }
  if (Number.isFinite(o.drift) && Math.round(o.drift)) SHIP.jobs[SHIP.jobs.length - 1].drift = Math.max(-3, Math.min(3, Math.round(o.drift)));   // o.drift (0.33.58, the Tier 2 test job): a setting off too, from when it faults (any kind; tuneSet settles it)
  MACH_REV++; return id;
}
// ---- the lines: water, heat and air (0.33.59, plans/mechanics/m9-tracing.html and architect-air-line.html; section 17's part
// of M9: 24i, seat M3, has the pipe kit, the reading step and the training) ----
// MACHINE_LINKS[line] = the machines in order, upstream to downstream: an id, [ids side by side] (one step: the lower of
// them), or { id: [decks] } (the branches at the end: each feeds those decks). LINE_ENDS[line][branch id] = the deck
// machines after a branch (the air line's deck scrubbers). Where the pipes run (seat S's check, 2026-10-19): water from the
// Deck 3 water recycler room (recycler, filter bank, UV steriliser, the Deck 3 pump) down the spine's trunks to the Deck 5
// manifold room (the two Deck 5 pumps), then the port pipe gallery (5-valve-1, up to Decks 1-3) and the starboard pipe
// gallery (5-valve-2, Decks 4-6); the garden's irrigation pump (3-irrigation-1, Deck 3 irrigation room) draws on the Deck
// 3 pipe after 3-pump-1 (LINE_DRAWS: P1's load, never a step of the line). Heat from the Deck 4 heating plant (the heater
// and its two pumps) down the spine to the Deck 5 manifold room (5-manifold-1), which splits it to every deck's loop. Air
// from the Deck 5 air plant (electrolyser, oxygen cells, the two air plant stacks) through the hatch to the Fan hall
// (5-fan-1, the dampers), then the ducts under the main corridor and up and down the spine: damper 1 to Decks 1-3 (Deck
// 2's scrubber in the lab gas plant room at its end), damper 2 to Decks 4-6 (Deck 4's air scrubbers). lineOn(line): every
// machine on it is real (else the line is skipped: tracing works with the others). lineOf(id) -> line | null.
// lineFlow(line, id, before?) -> 0-1: the flow read at a machine, the product of every step's share from the top through its
// own (before: up to the step before it; lineShare: worn passes it all, a fault on the line at most LINE_CUT), null off the line; flowWord(f): 'full' (.8+), 'low' (.5+), 'very
// low'. lineDecks(line, id): the decks it feeds. Traced faults (M9): a Tier 2 repair on a line machine, posted while
// you're an Officer or above and trained in tracing (section 24's SHIP.works.tr.m9 set; worksTrained is its setter), at your tier, is traced about half
// the time (schedU(machSeed(id), day, 878) < .5): its cause is picked only among causes with that `line`, and j.symptom
// = { line, decks, deck } (deck: the one the card names, Deck 4 if it's among them) makes the card name the symptom
// ("Showers weak on Deck 4", SYMPTOM_TEXT; the Works writer's lines can replace it), with no machine or place shown until
// traceMark finds it. traceMark(jobId, machineId) -> { before, after, word } | null (24i, at each reading): kept in j.read
// (saved); reading the job's own machine sets j.traceFound. Fixing it is an ordinary repair, which closes the symptom's
// job. simNote('traced', { line, machine, id }) when one posts
const MACHINE_LINKS = {
  water: ['3-recycler-1', '3-filter-1', '3-uv-1', '3-pump-1', ['5-pump-1', '5-pump-2'], { '5-valve-1': [1, 2, 3], '5-valve-2': [4, 5, 6] }],
  heat: ['4-heater-1', ['4-pump-1', '4-pump-2'], '5-manifold-1'],
  air: ['5-electrolyser-1', ['5-o2-1', '5-o2-2'], ['5-scrubber-1', '5-scrubber-2'], '5-fan-1', { '5-damper-1': [1, 2, 3], '5-damper-2': [4, 5, 6] }],
  ...(REC_DECK ? { pool: [['7-pool-filter-1', '7-pool-filter-2'], '7-pool-heat', '7-pool-dosing'] } : {}),   // 0.84.5 (rec engineer B): the rec deck's pool plant (room p), from the pool through the filters, the heat exchanger and the dosing back; only while REC_DECK is on
};
const LINE_ENDS = { air: { '5-damper-1': ['2-extractor-1'], '5-damper-2': ['4-scrubber-1', '4-scrubber-2'] } };
const LINE_DRAWS = { '3-irrigation-1': { line: 'water', after: '3-pump-1' } };
const LINE_DECKS = [1, 2, 3, 4, 5, 6];
const SYMPTOM_TEXT = { water: 'Showers weak', heat: 'Cold cabins', air: 'Stuffy air', pool: 'Water dripping from the ceiling in main storage' };   // pool: 0.84.5 (rec engineer B)
const LINE_SHOWS = { pool: [5] };                        // 0.84.5 (rec engineer B): the decks a line's fault shows on when they aren't the ones it feeds (traceSymptom): the pool plant's leak drips through to Deck 5's main storage, under it
// a line's ids, in order (branches and ends included)
const lineIds = line => (MACHINE_LINKS[line] || []).flatMap(s => typeof s === 'string' ? [s] : Array.isArray(s) ? s : Object.keys(s).flatMap(b => [b, ...((LINE_ENDS[line] || {})[b] || [])]));
const lineOn = line => !!MACHINE_LINKS[line] && lineIds(line).every(id => { const m = machineById(id); return !!m && !m.stub; });
const lineOf = id => Object.keys(MACHINE_LINKS).find(l => lineIds(l).includes(id)) || null;
// the steps from the top of the line through the one with `id`: [[ids], ...], or null
function linePath(line, id) {
  const out = [];
  for (const s of MACHINE_LINKS[line] || []) {
    if (typeof s === 'string' || Array.isArray(s)) { const ids = typeof s === 'string' ? [s] : s; out.push(ids); if (ids.includes(id)) return out; continue; }
    for (const b of Object.keys(s)) { if (b === id) return out.concat([[b]]); const ends = (LINE_ENDS[line] || {})[b] || []; if (ends.includes(id)) return out.concat([[b], ends]); }
  }
  return null;
}
function lineDecks(line, id) {
  const S = (MACHINE_LINKS[line] || []).find(s => s && typeof s === 'object' && !Array.isArray(s));
  if (S) for (const b of Object.keys(S)) { if (b === id) return S[b].slice(); const ends = (LINE_ENDS[line] || {})[b] || []; if (ends.includes(id)) { const m = machineById(id); return m ? [m.deck] : S[b].slice(); } }
  return LINE_DECKS.slice();
}
// one machine's share of the flow on `line`: healthy or worn, all of it (a worn machine still works); faulty or worse, as well as
// it works (machWorks); with an open job whose cause cuts this line, at most LINE_CUT (so the reading at it says low even
// just past worn); with a cause that doesn't (a bearing, a drip), all of it: that cause only ever shows on its own machine
const LINE_CUT = .6;
function lineShare(line, id, c) {
  const cond = c[id] ?? 100; if (cond >= 50) return 1;
  const j = SHIP.jobs.find(x => x.machine === id && x.cause && x.status !== 'done' && !jobByStops(x)), cs = j && faultCause(j);
  if (cs) return cs.line === line ? Math.min(machWorks(cond) / 100, LINE_CUT) : 1;
  return machWorks(cond) / 100;
}
function lineFlow(line, id, before) {
  const p = linePath(line, id); if (!p) return null;
  const c = machConds(); let f = 1;
  for (let k = 0; k < p.length - (before ? 1 : 0); k++) f *= Math.min(...p[k].map(x => lineShare(line, x, c)));
  return Math.round(f * 1000) / 1000;
}
const flowWord = f => f >= .8 ? 'full' : f >= .5 ? 'low' : 'very low';
// is a repair on m, posted in hour h, traced? (a line machine, the line real, you an Officer trained in tracing, at your tier, about half)
function traceFor(m, h) {
  const line = lineOf(m.id), d = Math.floor(h / 24) + 1;
  return !!line && lineOn(line) && playerTier() >= 2 && !!(SHIP.works && SHIP.works.tr && SHIP.works.tr.m9 !== undefined) && jobTier({ machine: m.id }) <= playerTier()
    && (FAULT_CAUSES[m.kind] || []).some(c => c.line === line) && schedU(machSeed(m.id), d, 878) < .5 ? line : null;
}
function traceSymptom(line, id) { const decks = LINE_SHOWS[line] ? LINE_SHOWS[line].slice() : lineDecks(line, id); return { line, decks, deck: decks.includes(4) ? 4 : decks[0] }; }
const traceHidden = j => !!(j && j.symptom && !j.traceFound);
function traceTitle(j) {                                 // the Works writer's trace.symptom.<line> line when it's in (M3's ask)
  const fb = (SYMPTOM_TEXT[j.symptom.line] || 'A fault') + ' on ' + deckIn(j.symptom.deck);
  return typeof worksText === 'function' ? worksText('trace.symptom.' + j.symptom.line, fb, { deck: j.symptom.deck, where: '' }) : fb;
}
function traceMark(jobId, id) {
  const j = SHIP.jobs.find(x => x.id === jobId && x.symptom && x.status !== 'done'); if (!j) return null;
  const line = j.symptom.line, after = lineFlow(line, id); if (after === null) return null;
  const before = lineFlow(line, id, true);
  j.read = [...new Set([...(j.read || []), id])].slice(-12); if (id === j.machine) j.traceFound = true; MACH_REV++;   // the last 12 readings
  return { before, after, word: flowWord(after) };
}
// ---- team jobs (0.33.58, plans/mechanics/m8-team-jobs.html, section 17's part; 24h, seat M2, plans the week's and runs the steps) ----
// A big job three or four Works crew do together at a set time. teamJobPost({ machine, start, mins, team: [crew ids], lead?,
// you?, spots?, steps?, title?, found?, parts? }) -> id | null posts kind 'team' on `machine` (an id): j.team (the crew in it),
// j.lead (o.lead, else the first), j.start, j.mins, j.spots ({ crew id | 'you': place id }; default the machine's team spots
// '<machine id less its number>-team-<k>' in order, yours the next, else its panel place), j.segsBy ({ crew id: segments }:
// the lift by `start`, their spot till it's done, the lift back), j.done, j.end. Anyone not at work all through it, or
// already in a team job then, is left out (fewer than two left: null). With `you` (24h asks for Officers and up) it's
// yours (claimedBy 'you', a side job: beside your board job, it never lapses) and your stops are `steps` (24h's: [{ deck,
// placeId, mins, tag, how, opts }]) or one hold at your spot; else it's the lead's. teamYouOut(id): you didn't come (24h
// calls it 15 minutes after the start; jobsHour does it by the next hour, TEAM_WAIT): your steps go to the lead and it
// takes TEAM_SLOW longer. The crew in a team job take no other job that would overlap it (teamClash), and jobWhere puts
// each at their spot. Finishing it (the lead's, at j.done; yours, when your stops are done) puts the machine right
// (TEAM_RESTORE, an overhaul's); with j.youIn set (24h: you were at your spot) you get the meters' step (an overhaul's)
// even when the lead finishes it. simNote('team', ...) is 24h's. Nothing here posts a team job by itself
const TEAM_WAIT = 15, TEAM_SLOW = 1.2, TEAM_RESTORE = 90;
function teamSpots(id) {
  const m = machineById(id), pre = id.replace(/-\d+$/, '') + '-team-'; if (!m) return [];
  return (DECKS[m.deck].places || []).filter(p => p.id.startsWith(pre)).map(p => p.id).sort((a, b) => parseInt(a.slice(pre.length), 10) - parseInt(b.slice(pre.length), 10));
}
// a crew id already in a team job that overlaps minutes [a, b)
const teamClash = (cid, a, b) => SHIP.jobs.some(j => j.kind === 'team' && j.status !== 'done' && j.segsBy && j.segsBy[cid] && j.segsBy[cid][0].from < b && a < j.end);
function teamSegs(p, deck, placeId, a, b) {
  const w = planWhere(p, a - JOB_RIDE), w2 = planWhere(p, b - 1);
  if (!w || w.act !== 'work' || w.moving || !w2 || w2.act !== 'work') return null;
  const home = w.deck, segs = [];
  if (home !== deck) segs.push({ from: a - JOB_RIDE, to: a, act: 'commute', deck, fromDeck: home, type: 'lift', placeId: null });
  segs.push({ from: a, to: b, act: 'work', deck, type: 'job', placeId, tag: 'team' });
  if (home !== deck) segs.push({ from: b, to: b + JOB_RIDE, act: 'commute', deck: home, fromDeck: deck, type: 'lift', placeId: null });
  return segs;
}
function teamJobPost(o = {}) {
  machinesNow(); const m = o.machine && machineById(o.machine); if (!m || !Number.isFinite(o.start) || !(o.mins > 0)) return null;
  const id = o.id || 'team:' + m.id + '@' + Math.floor(o.start);
  if (SHIP.jobs.some(j => j.id === id)) return id;
  const ppl = new Map(schedPeople().map(p => [p.id, p])), spots = teamSpots(m.id), panel = panelPlace(m.id), done = o.start + Math.round(o.mins), team = [], segsBy = {}, at = {};
  for (const cid of o.team || []) {
    const p = ppl.get(cid); if (!p || team.includes(cid) || teamClash(cid, o.start - JOB_RIDE, done + JOB_RIDE)) continue;
    const pl = o.spots && o.spots[cid] || spots[team.length] || panel, sg = teamSegs(p, m.deck, pl, o.start, done); if (!sg) continue;
    team.push(cid); segsBy[cid] = sg; at[cid] = pl;
  }
  if (team.length < 2) return null;
  const lead = o.lead && team.includes(o.lead) ? o.lead : team[0], you = !!o.you, t = shipNow(), found = Number.isFinite(o.found) ? o.found : t;
  if (you) at.you = o.spots && o.spots.you || spots[team.length] || spots[spots.length - 1] || panel;
  const j = { id, machine: m.id, deck: m.deck, room: m.room, kind: 'team', title: o.title || 'Team job: ' + machineTitle(m.id), tier: 2, team, lead, spots: at, segsBy, segs: segsBy[lead],
              start: o.start, mins: done - o.start, done, end: Math.max(...team.map(c => segsBy[c][segsBy[c].length - 1].to)), urgency: 0, leave: null, posted: found, found,
              claimedBy: you ? 'you' : lead, status: 'claimed', parts: (o.parts || []).slice(), ...(o.steps ? { steps: o.steps.map(x => ({ ...x })) } : {}), ...(you ? { you: true } : {}) };
  j.stops = kindStops(j).map(plainStop);
  SHIP.jobs.push(j); MACH_REV++; return id;
}
function teamYouOut(id) {
  const j = SHIP.jobs.find(x => x.id === id && x.kind === 'team' && x.claimedBy === 'you' && x.status === 'claimed' && !x.workDone); if (!j) return false;
  const ext = Math.round(j.mins * (TEAM_SLOW - 1));
  for (const c of j.team) { let past = false; for (const s of j.segsBy[c]) { if (past) { s.from += ext; s.to += ext; } else if (s.tag === 'team') { s.to += ext; past = true; } } }
  j.done += ext; j.end += ext; j.claimedBy = j.lead; j.youOut = true; MACH_REV++; return true;
}
jobKindAdd('team', { tier: 2, side: true, work: 0, text: 'Team job', veto: true,   // veto + stepDone: 24h keeps your turns in the lead's order (M2's teamStepDone)
  stepDone: (j, k, res, t) => typeof teamStepDone === 'function' ? teamStepDone(j, k, res, t) : true,
  stops: j => j.steps || (j.spots && j.spots.you ? [{ deck: j.deck, placeId: j.spots.you, mins: Math.min(j.mins || 10, 10), tag: 'team', how: 'hold' }] : []),
  done(j, t, by) {
    const before = by !== 'you' && j.youIn && !j.meters ? shipMeters() : null, s = SHIP.machines[j.machine];
    if (s) { s.cond = Math.max(s.cond, TEAM_RESTORE); s.state = machineState(s.cond); s.lastService = t; }
    if (before) meterStep(j, before);
  },
  crew: { can: () => false, mins: 0 } });   // the crew never claim one: they're put in it (teamJobPost)
// machineFound(id, by = 'you') -> { id, fresh } | null (0.33.47, for 24a's rounds: m1-rounds.html): you noticed a machine
// that isn't healthy. Its job is found now (one not yet seen, a service's 2-24 hours or a fault worn on unseen), or posted
// if it has none; fresh: it wasn't on the board till now (then j.foundBy = by, and simNote('found', { machine, by, id })).
// A machine already on the board gives its job, not fresh; a healthy one null
function machineFound(id, by = 'you') {
  machinesNow(); const m = machineById(id), s = m && SHIP.machines[id]; if (!s || !JOB_FOR[s.state]) return null;
  const t = shipNow(), h = Math.floor(t / 60);
  let j = SHIP.jobs.find(x => x.machine === id && x.status !== 'done' && !jobByStops(x) && x.kind !== 'restock');
  if (j && j.found <= t) return { id: j.id, fresh: false };
  if (!j) {
    const kind = JOB_FOR[s.state], cause = kind === 'service' ? null : faultPick(m, h);
    j = { id: m.id + '@' + h, machine: m.id, deck: m.deck, kind, urgency: JOB_URGENCY[s.state], posted: t, found: t, claimedBy: null, parts: faultParts(m, kind, cause), status: 'open', ...(cause ? { cause: cause.id } : {}) };
    SHIP.jobs.push(j);
  }
  j.found = t; j.foundBy = by; MACH_REV++;
  if (typeof simNote === 'function') simNote('found', { machine: id, by, id: j.id, t });
  return { id: j.id, fresh: true };
}
// jobSetPart(id, part) (24k's scanner): your job's first part becomes `part` (a part in STOCK), e.g. the part you chose
function jobSetPart(id, part) { const j = SHIP.jobs.find(x => x.id === id && x.status !== 'done'); if (!j || !(part in STOCK) || !j.parts.length) return false; j.parts[0] = part; MACH_REV++; return true; }
function jobReserved(slot) { const j = SHIP.jobs.find(x => x.reserved === slot && x.status !== 'done'); return j ? j.id : null; }
function jobRelease(slot) { let n = 0; for (const j of SHIP.jobs) if (heldForYou(j) && !j.claimedBy && (slot === undefined || j.reserved === slot)) { j.freed = j.released = true; n++; } if (n) MACH_REV++; return n; }
// each hour (jobsHour): a reserved job's machine goes faulty in the hour it's due; one not taken by its `until` is released
function reservedHour(t, jobs) {
  for (const j of jobs) if (j.reserved && heldForYou(j)) {   // reserved jobs only (a case's held job is 24k's)
    if (!j.faulted && j.found < t + 60) { const s = SHIP.machines[j.machine]; if (s) { s.cond = Math.min(s.cond, 40); s.state = machineState(s.cond); if (j.drift) s.drift = j.drift; } j.faulted = true; }
    if (!j.claimedBy && t >= j.until) j.freed = j.released = true;   // an ordinary job now, for the crew at once (leaveEnd)
  }
}

// ---- favours (Pillar 3, C7, for the social engineer): personal jobs, accepted and handed back in person ----
// favourPost({ from: crewId, title, kind?, place?, machine?, where?, deck?, stops?, parts?, mins?, bring?, expires? })
// -> id: a favour someone asks of you, offered (never on the board, never taken by the crew). favourAccept(id) makes it
// yours (alongside a board job: the one-at-a-time rule is for board jobs). Its stops are done with jobStepDone, the
// last step being 'return' to the person (jobStops gives { step: 'return', person }); once the stops are done its
// work is done (j.workDone), and favourTurnIn(id) at the person completes it. favoursOf(crewId), myFavours().
// An offered or accepted favour not done by `expires` (default a day and a half) lapses. Saved with the jobs.
function favourPost(o = {}) {
  machinesNow(); if (!o.from) return null;
  const t = shipNow(), key = 'favour:' + o.from + '@' + Math.floor(t);
  const st = o.stops ? null : eventStop(o);
  const stops = o.stops ? o.stops.map(x => ({ ...x })) : st ? [{ deck: st.deck, placeId: st.placeId, mins: o.mins || 10, tag: o.kind || 'favour', at: st.at || null }] : [];
  SHIP.jobs.push({ id: key, machine: st && st.machine || o.machine || null, deck: stops[0] ? stops[0].deck : null, room: st && st.room || null, kind: 'favour', chore: o.kind || null,
                   from: o.from, title: o.title || 'A favour', bring: o.bring || null, tier: 1, stops, urgency: 0, posted: t, found: t, claimedBy: null,
                   parts: (o.parts || []).slice(), status: 'offered', expires: o.expires || t + 2160 });
  MACH_REV++; return key;
}
const favourById = id => SHIP.jobs.find(j => j.id === id && j.kind === 'favour') || null;
function favourAccept(id) { machinesNow(); const j = favourById(id); if (!j || j.status !== 'offered') return false; j.status = 'claimed'; j.claimedBy = 'you'; j.start = shipNow(); MACH_REV++; return true; }
function favourDecline(id) { const j = favourById(id); if (!j || j.status !== 'offered') return false; j.status = 'done'; j.doneAt = shipNow(); j.doneBy = null; j.declined = true; MACH_REV++; return true; }
function favourTurnIn(id) {
  machinesNow(); const j = favourById(id);
  if (!j || j.status !== 'claimed' || j.claimedBy !== 'you') return false;
  if (!j.workDone) { if (j.stops.length) return false; jobEffect(j, shipNow(), 'you'); j.workDone = shipNow(); }   // a favour with no stops (a word, a hand)
  j.stepsDone = [...new Set([...(j.stepsDone || []), jobStops(j).length - 1])]; jobFinish(j, shipNow(), 'you'); MACH_REV++; return true;
}
const favoursOf = crewId => SHIP.jobs.filter(j => j.kind === 'favour' && j.from === crewId && j.status !== 'done');
const myFavours = () => SHIP.jobs.filter(j => j.kind === 'favour' && j.claimedBy === 'you' && j.status === 'claimed');

// ---- the device's jobs section (0.33.9): the board in your pocket. The device itself is section 15's placeholder
// (device.addSection); this only lists jobs and lets you claim or drop one. Doing it, at the machine's panel,
// comes with the player engineer's repair activity (finishJob). ----
function myJob() { return SHIP.jobs.find(j => j.claimedBy === 'you' && j.status === 'claimed' && j.kind !== 'favour' && !jobSide(j)) || null; }
const mySideJobs = () => SHIP.jobs.filter(j => j.claimedBy === 'you' && j.status === 'claimed' && jobSide(j));   // a side kind's jobs (the drill), beside your board job
// where your job takes you, in order (0.33.16, for the player engineer's walk): [{ step, places: [place ids, the
// first free one best], deck }]. A machine job: parts from the shelves, then its panel. A cart run: a cart from a
// dock, load in the hold, unload at the cold store (or the shelves), the cart back. Places not built yet are left out.
function jobStops(j) {
  const out = jobStopsOf(j), done = new Set((j && j.stepsDone) || []);
  out.forEach((x, k) => { x.done = done.has(k) || !!(j && j.workDone); });
  return out;
}
function jobStopsOf(j) {
  const known = new Set(Object.values(DECKS).flatMap(d => (d.places || []).map(p => p.id))), st = (step, ids, deck) => ({ step, places: ids.filter(id => known.has(id)), deck });
  if (!j) return [];
  const how = xs => xs.map(x => ({ ...x, how: x.how || 'hold', opts: x.opts || null }));   // each stop's work step (0.33.47): 'hold' unless its kind says
  if (jobKindOf(j)) return how((j.parts.length ? [st('fetch', shelvesFor(j.parts[0]), 5)] : []).concat(kindStops(j).map(x => ({ step: x.tag || 'job', places: x.placeId && known.has(x.placeId) ? [x.placeId] : [], deck: x.deck, mins: x.mins, at: x.at || null, how: x.how, opts: x.opts }))));
  return how(jobStopsBase(j, known, st));
}
function jobStopsBase(j, known, st) {
  if (j.kind === 'chore' || j.kind === 'favour') return (j.parts.length ? [st('fetch', shelvesFor(j.parts[0]), 5)] : []).concat(j.stops.map(x => ({ step: x.tag, places: x.placeId && known.has(x.placeId) ? [x.placeId] : [], deck: x.deck, mins: x.mins, at: x.at || null })),
    j.kind === 'favour' ? [{ step: 'return', places: [], deck: null, person: j.from }] : []);
  if (j.kind === 'restock') { const meals = j.cargo === 'meals'; return [st('cart', CART_AT, 5), st('load', loadAt(j), 5), st('unload', meals ? COLD_AT : FETCH_AT, meals ? 3 : 5), st('return', CART_AT, 5)]; }
  if (traceHidden(j) && typeof traceStops === 'function') return traceStops(j, known);   // 24i: a traced fault's reading stop till it's found (0.33.60)
  const m = machineById((typeof caseAt === 'function' && caseAt(j)) || j.machine); if (!m) return [];   // 24k: a P1 case's stop is the called suspect's machine, before a call the line's top (0.55.16)
  const pp = panelPlace(m.id);
  return [st('fetch', shelvesFor(j.parts[0]), 5)].concat(j.make ? [{ ...st('make', MAKE_AT, 5), part: j.make }] : [], [{ step: 'job', places: pp ? [pp] : [], deck: m.deck, at: m.panel, room: m.room }]);
}
function jobsSection(el) {
  const line = (txt, cls) => { const p = document.createElement('p'); p.textContent = txt; if (cls) p.className = cls; el.appendChild(p); return p; };
  const button = (txt, fn) => { const b = document.createElement('button'); b.type = 'button'; b.textContent = txt; b.style.cssText = 'margin:0 2px 8px;padding:4px 10px;font-size:12.5px'; b.onclick = () => { fn(); device.refresh(); }; el.appendChild(b); return b; };
  const board = jobsBoard(), mine = myJob();
  if (mine) {
    const [title, where, state] = jobCard(mine), m = mine.machine && !traceHidden(mine) && machineById(mine.machine);   // a traced fault: no room till it's found
    line('Yours: ' + title + ', ' + where + '.', 'devtime');
    if (jobByStops(mine) && mine.kind !== 'favour') {
      const stops = mine.stops.map(st => { const p = placeById(st.placeId); return (st.tag === 'pickup' ? 'pick up ' + (mine.bring || 'the load') + ' in the ' : st.tag === 'drop' ? 'drop it in the ' : '') + (p ? roomName(p.deck, p.room) || 'room' : 'room') + ' on ' + deckIn(st.deck); });
      line(mine.title + '. ' + (mine.parts.length ? 'Bring ' + mine.parts.map(k => 'a ' + k).join(', ') + ' from ' + (shelfName(mine.parts[0]) ? 'the ' + shelfName(mine.parts[0]) + ' shelf in ' : '') + 'main storage on Deck 5. ' : '') + 'Go to: ' + stops.join(', then ') + '.');
    } else if (m) {
      const need = {}; for (const k of mine.parts) need[k] = (need[k] || 0) + 1;
      line('Needs ' + Object.entries(need).map(([k, n]) => n + ' × ' + k + ' (' + (shelfName(k) ? 'the ' + shelfName(k) + ' shelf, ' + (SHIP.stores[k] || 0) + ' there' : k === mine.make ? 'you make it' : (SHIP.stores[k] || 0) + ' in storage') + ')').join(', ') + '. Parts are in main storage on Deck 5; the job is in the ' + ((DECKS[m.deck].rooms[m.room] || {}).name || 'room').toLowerCase() + ' on ' + deckIn(m.deck) + '.');
    } else line(mine.cargo === 'meals' ? 'Take a hover cart from the Cart bay on Deck 5, load ' + (mine.meals || 'the') + ' meals in the cargo hold, and take them up to the cold store on Deck 3. Then bring the cart back.'
      : 'Take a hover cart from the Cart bay on Deck 5. In the cargo hold tap the crates' + (partsCrates() ? ' (' + partsCrates() + ' there)' : '') + ' and the cart pulls them in; in main storage tap any shelf and it unloads itself. Then bring the cart back.');
    button('Drop it', () => dropJob(mine.id));
  }
  const open = board.filter(j => !j.claimedBy);
  if (!open.length && !mine) line('Nothing on the board. Enjoy it while it lasts.');
  for (const j of open.slice(0, 5)) {
    const [title, where, state, pri] = jobCard(j), canTake = !mine && jobTier(j) <= playerTier() && !(j.machine && ENGINE_KINDS.has(machineById(j.machine).kind));
    const p = line((pri === 'urgent' ? '! ' : '') + title + ' · ' + where + ' · ' + state + (canTake ? '' : jobTier(j) > playerTier() ? ' (tier ' + jobTier(j) + ')' : ''));
    if (canTake) button('Take it', () => claimJob(j.id));
  }
  if (open.length > 5) line('And ' + (open.length - 5) + ' more on the board in the Works bay.');
}
if (typeof device !== 'undefined' && device.addSection) device.addSection('jobs', 'Jobs', jobsSection);

// openJobs(forWho = 'you') (0.33.19, for the interactions engineer's job board and arrow): the jobs on the board
// that forWho may take now, most urgent first: [{ id, title, kind, deck, at, room, place, tier, mins, parts, bring,
// urgency, state }]. at: the tile [i, j] of the main stop (the machine's panel, the drop-off, the first stop), place:
// its place id or null. Take one with claimJob(id); finish it with finishJob(id); jobStops(job) gives the way there.
function openJobs(forWho = 'you') {
  const you = forWho === 'you', tier = you ? playerTier() : hatchTier(forWho);
  return jobsBoard().filter(j => !j.claimedBy && j.status !== 'waiting' && (jobTier(j) <= tier || (you && heldForYou(j))) && rankOk(forWho, j) && !(you && j.machine && ENGINE_KINDS.has(machineById(j.machine).kind)) && (you || !heldForYou(j)) && !(you && bridgeBars(j))).map(j => {
    const [title, where, state] = jobCard(j), m = j.machine && machineById(j.machine);
    const stops = jobStops(j).filter(x => x.step !== 'fetch'), main = jobByStops(j) ? stops[stops.length - 1] : j.kind === 'restock' ? stops[2] : stops[0];
    const place = main && main.places[0] || null, pl = placeById(place);
    const mins = jobKindOf(j) ? kindStops(j).reduce((a, x) => a + (x.mins || 0), 0) : j.kind === 'chore' ? j.stops.reduce((a, x) => a + x.mins, 0) : j.kind === 'restock' ? 33 : Math.round(JOB_TYPES[j.kind].work * (1 + .25 * (jobTier(j) - 1)));
    const verb = { service: 'Service', repair: 'Repair', overhaul: 'Overhaul' }[j.kind];
    const o = { id: j.id, title: jobByStops(j) ? j.title : verb ? verb + ': ' + title : title, kind: j.chore || j.kind, deck: main ? main.deck : j.deck, at: pl ? pl.at.slice() : m ? m.panel.slice() : main && main.at ? main.at.slice() : null,
             room: pl ? pl.room : m ? m.room : j.room || null, place, tier: jobTier(j), mins, parts: j.parts.slice(), bring: j.bring || (j.kind === 'restock' ? 'a hover cart' : null), urgency: j.urgency, state, where, event: j.event || null, asked: heldForYou(j) };
    if (traceHidden(j)) Object.assign(o, { deck: j.symptom.deck, at: null, room: null, place: null, symptom: { ...j.symptom } });   // a traced fault: where it shows, not the machine (0.33.59)
    return o;
  });
}

// ---- the shelves (0.33.41, the plan for 0.60.7, "The right part from the right shelf") ----
// Each part lives on one shelf in main storage, Deck 5: the shelf place whose `stock` lists it (the Deck 6 architect's
// 5-parts-1..4: Lights, Filters, Plumbing, Galley parts), and lamps on Lights. shelfOf(part) -> place id | null;
// shelfName(place id or part) -> 'Lights' | ...; shelfStock(id) -> [{ part, n, of, low }] (of: what the shelf keeps,
// STOCK; low: under half); shelfLine(id): that in words, for a tap; shelfTapped(it): the shelf a tapped item is (by its
// name), or null. Your job's parts come off their own shelf (section 15's jobTap and 15b's ixChoreTap ask
// shelfWant/shelfWrong): the arrow points at it, it glows while you need something from it (shelfGlowTick, one mesh,
// Deck 5 only), and tapping another shelf costs nothing: it says where, and the right one flares
const SHELF_NAME = { '5-parts-1': 'Lights', '5-parts-2': 'Filters', '5-parts-3': 'Plumbing', '5-parts-4': 'Galley parts' };
const SHELF_MORE = { lamp: '5-parts-1' };                // parts no shelf's stock list names
function shelfOf(part) { return FETCH_AT.find(id => ((placeById(id) || {}).stock || []).includes(part)) || SHELF_MORE[part] || null; }
const shelfName = x => SHELF_NAME[x] || SHELF_NAME[shelfOf(x)] || null;
function shelfParts(id) { const st = ((placeById(id) || {}).stock || []).slice(); for (const k in SHELF_MORE) if (SHELF_MORE[k] === id && !st.includes(k)) st.push(k); return st; }
function shelfStock(id) { machinesNow(); return shelfParts(id).map(part => { const n = SHIP.stores[part] || 0, of = STOCK[part] || 0; return { part, n, of, low: n < of / 2 }; }); }
const shelfLine = id => shelfStock(id).map(x => plural(x.part) + ' ' + x.n + ' of ' + x.of + (x.n === 0 ? ' (none left)' : x.low ? ' (low)' : '')).join(', ') + '.';
function shelfTapped(it) { const name = it && it.t; return Object.keys(SHELF_NAME).find(id => SHELF_NAME[id] === name) || null; }
// the part your job needs next from the shelves (one that's there), or null: its parts, less what you've fitted or carry
// and any you make yourself (j.make)
function shelfNeed() {
  const j = typeof myJob === 'function' ? myJob() : null; if (!j || j.workDone || !j.parts || !j.parts.length) return null;
  const P = SHIP.player || {}, need = j.parts.slice(), less = ((P.work && P.work.job === j.id && P.work.fitted) || []).concat(P.carry || []);
  for (const p of less) { const i = need.indexOf(p); if (i >= 0) need.splice(i, 1); }
  return need.find(p => p !== j.make && SHIP.stores[p] > 0 && shelfOf(p)) || null;
}
const shelfWant = () => { const p = shelfNeed(); return p ? shelfOf(p) : null; };
let SHELF_FLASH = 0;
// a tap on the wrong shelf (or the counter) while your job needs something from another: nothing lost, it says where
// and the right shelf flares for a moment. True if it was the wrong one (the tap's done); false: go ahead and fetch
function shelfWrong(it) {
  const part = shelfNeed(), want = part && shelfOf(part), at = shelfTapped(it);
  if (!want || at === want) return false;
  SHELF_FLASH = performance.now() + 2500;
  const Ps = plural(part), name = SHELF_NAME[want];
  toast(it.t, (at ? 'No ' + Ps + ' on the ' + SHELF_NAME[at] + ' shelf. ' : '') + Ps.charAt(0).toUpperCase() + Ps.slice(1) + ' are on the ' + name + ' shelf: it\'s lit up for you.');
  return true;
}
// the glow: one see-through amber box round the shelf you want, while you need something from it and you're on Deck 5. Made on
// first use (no R()), kept for good and hidden elsewhere; it never shares a plane (padded, lifted off the floor)
let SHELF_GLOW = null;
function shelfGlowTick() {
  const want = typeof deckDef !== 'undefined' && deckDef && deckDef.num === 5 ? shelfWant() : null;
  if (!want) { if (SHELF_GLOW) SHELF_GLOW.mesh.visible = false; return; }
  if (!SHELF_GLOW) {
    const mat = new THREE.MeshBasicMaterial({ color: col(0xffa526), transparent: true, opacity: .3, depthWrite: false });
    SHELF_GLOW = { mesh: new THREE.Mesh(new THREE.BoxGeometry(1, 1, 1), mat), def: null, id: null };
    SHELF_GLOW.mesh.renderOrder = 2; scene.add(SHELF_GLOW.mesh);
  }
  const G = SHELF_GLOW, m = G.mesh;
  if (G.def !== deckDef || G.id !== want) {
    G.def = deckDef; G.id = want;
    const box = new THREE.Box3(), b = new THREE.Box3();
    for (const it of ITEMS) if (it.t === SHELF_NAME[want] && it.g) box.union(b.setFromObject(it.g));
    if (box.isEmpty()) { G.id = null; m.visible = false; return; }
    const c = box.getCenter(new THREE.Vector3()), sz = box.getSize(new THREE.Vector3());
    m.scale.set(sz.x + .12, sz.y + .1, sz.z + .12); m.position.set(c.x, (sz.y + .1) / 2 + .02, c.z);
  }
  const now = performance.now(), fl = now < SHELF_FLASH;
  m.material.opacity = fl ? .5 + .16 * Math.sin(now / 90) : .34 + .08 * Math.sin(now / 420);
  m.visible = true;
}

// ---- the Wednesday delivery as crates (0.33.42, the plan for 0.60.7, "Stores and the lift") ----
// The delivery lands in the cargo hold at 10:00 on Wednesdays (jobsHour; never late in your first week, so your first is
// Day 3) as crates: holdCrates() -> how many (CRATE_PARTS parts each; meals aren't crates). Its job, "Unload the
// Wednesday delivery", waits for you till 14:00 on a shift day (leaveEnd; on your days off the crew take it at once).
// Your run (section 15's cart): take a hover cart, and in the hold cartLoadHold(jobId) pulls in up to CART_CRATES crates
// (-> how many; the parts ride on the job, j.onCart, so they're saved); at any shelf in main storage
// cartUnloadShelves(jobId) -> { parts, left } puts every part on its own shelf; left: crates still in the hold (a
// second trip). holdCratesLive(group, k): the Deck 6 architect's crate stack hands each crate (k = 1, 2, ...) as Deck 5
// is built, and worksTick shows the first holdCrates() of them
const holdParts = () => Object.keys(SHIP.hold).filter(k => k !== 'meals').reduce((a, k) => a + (SHIP.hold[k] || 0), 0);
function partsCrates() { machinesNow(); return Math.ceil(holdParts() / CRATE_PARTS); }   // the parts crates (the unload's); holdCrates also counts the manifest's (0.33.50)
function holdCrates() { return partsCrates() + manifestCrates(); }
// the manifest (0.33.50, plans/mechanics/m4-hauling.html; 24d's manifest run): with each Wednesday delivery, while 24d's 'haul'
// kind is in the build, 2-4 crates for the rest of the ship: SHIP.manifest = [{ id, dest, n }] (id a DELIVERIES key, dest its
// drop place: the architect's <n>-<room>-drop when it's there, else the delivery's own), schedU(week, k, 866). Kept apart
// from SHIP.hold (a count of parts the unload shelves). manifestCrates(); manifestTake(id) -> the crate, out of the hold
// (24d loads it). The stocktake's misplaced part: on Thursdays at 06:00, about one week in two, SHIP.misplaced = { part, on }
// (a part in stock, sitting on another shelf; key 867); a fetch of that part (yours or the crew's) or misplacedFix() puts it right
const haulOn = () => !!JOB_KINDS.haul;
const MANIFEST_DROP = { linen: '4-laundry-drop', medical: '3-infirmary-drop', store: '3-store-drop', galley: '3-galley-drop', bridge: '1-bridge-drop' };
function manifestFor(d) {
  const wk = Math.floor((d - 1) / 7), seed = machSeed('manifest'), all = DELIVERIES.filter(r => (placeById(MANIFEST_DROP[r.key]) || placeById(r.to)) && !(r.key === 'bridge' && bridgeShut()));   // the bridge's crate waits for your invite (0.33.57)
  const pool = all.slice(), out = [], n = Math.min(pool.length, 2 + Math.floor(3 * schedU(seed, wk, 866)));
  for (let k = 0; k < n; k++) { const r = pool.splice(Math.floor(pool.length * schedU(seed, wk * 8 + k + 1, 866)), 1)[0]; out.push({ id: r.key, dest: placeById(MANIFEST_DROP[r.key]) ? MANIFEST_DROP[r.key] : r.to, n: 1 }); }
  return out;
}
const manifestCrates = () => (SHIP.manifest || []).reduce((a, c) => a + (c.n || 0), 0);
function manifestTake(id) { const c = (SHIP.manifest || []).find(x => x.id === id && x.n > 0); if (!c) return null; c.n--; if (!c.n) SHIP.manifest = SHIP.manifest.filter(x => x !== c); MACH_REV++; return { id: c.id, dest: c.dest }; }
function misplacedFor(d) {
  const wk = Math.floor((d - 1) / 7), seed = machSeed('misplaced');
  if (schedU(seed, wk, 867) >= .5) return null;
  const parts = Object.keys(STOCK).filter(k => SHIP.stores[k] > 0 && shelfOf(k)), shelves = FETCH_AT.filter(id => placeById(id));
  if (!parts.length || shelves.length < 2) return null;
  const part = parts[Math.floor(parts.length * schedU(seed, wk * 3 + 1, 867))], others = shelves.filter(id => id !== shelfOf(part));
  return { part, on: others[Math.floor(others.length * schedU(seed, wk * 3 + 2, 867))] };
}
function misplacedFix() { if (!SHIP.misplaced) return false; SHIP.misplaced = null; MACH_REV++; return true; }
function cartLoadHold(id) {
  machinesNow(); const j = SHIP.jobs.find(x => x.id === id && x.cargo === 'stores' && x.claimedBy === 'you' && x.status === 'claimed'); if (!j) return 0;
  let room = CART_CRATES * CRATE_PARTS - Object.values(j.onCart || {}).reduce((a, n) => a + n, 0); if (room <= 0) return 0;
  const was = holdParts(); j.onCart = j.onCart || {};
  for (const k of Object.keys(SHIP.hold).filter(k => k !== 'meals').sort()) { const n = Math.min(room, SHIP.hold[k] || 0); if (!n) continue; j.onCart[k] = (j.onCart[k] || 0) + n; SHIP.hold[k] -= n; room -= n; if (!SHIP.hold[k]) delete SHIP.hold[k]; }
  MACH_REV++; return Math.ceil(was / CRATE_PARTS) - Math.ceil(holdParts() / CRATE_PARTS);
}
function cartUnloadShelves(id) {
  machinesNow(); const j = SHIP.jobs.find(x => x.id === id && x.cargo === 'stores' && x.claimedBy === 'you' && x.status === 'claimed'); if (!j) return { parts: 0, left: partsCrates() };
  let n = 0; for (const k in j.onCart || {}) { SHIP.stores[k] = (SHIP.stores[k] || 0) + j.onCart[k]; n += j.onCart[k]; }
  delete j.onCart; MACH_REV++; touchJob(id); return { parts: n, left: partsCrates() };
}
const HOLD_CRATES = { def: null, groups: new Map(), n: -1 };
function holdCratesLive(group, k) { if (HOLD_CRATES.def !== deckDef) { HOLD_CRATES.def = deckDef; HOLD_CRATES.groups = new Map(); HOLD_CRATES.n = -1; } HOLD_CRATES.groups.set(k, group); }
function holdCratesTick() {
  const H = HOLD_CRATES; if (H.def !== deckDef || !H.groups.size) return;
  const n = holdCrates(); if (n === H.n) return;
  H.n = n; for (const [k, g] of H.groups) g.visible = k <= n;
}

// ---- the Works bay job board (Deck 5), live (0.33.8) ----
// The jobBoard kit (section 4b) hands its canvas texture to jobBoardLive as the deck is built (one inert line);
// worksTick (main loop) redraws it whenever the job list changes, in the kit's own look. Up to six cards: the
// most urgent first. Nothing here calls R() or makes geometry; the board's draw calls are unchanged.
let JOB_BOARD = null;
function jobBoardLive(t) { JOB_BOARD = { t, def: deckDef, rev: -1, min: -1 }; worksTick(); }
const JOB_PRI = ['routine', 'soon', 'urgent', 'urgent'];
const JOB_WORD = { service: 'service due', repair: 'repair', overhaul: 'broken: overhaul' };
// a machine's name on a card: its kind's name, and its number when its deck has more than one ("Washer 2"); no symptom (0.33.52)
function machineTitle(id) { const m = machineById(id); if (!m) return null; return MACHINE_KINDS[m.kind].name + (machineList().filter(x => x.kind === m.kind && x.deck === m.deck).length > 1 ? ' ' + m.id.split('-').pop() : ''); }
function jobCard(j) {
  const who = j.claimedBy === 'you' ? 'you' : j.claimedBy ? ((schedPeople().find(p => p.id === j.claimedBy) || {}).name || '').split(' ')[0] : null;
  if (jobKindOf(j)) return [j.title.split(':')[0], deckWord(j.deck) + (j.room && roomName(j.deck, j.room) ? ' · ' + roomName(j.deck, j.room) : ''),
    j.status === 'waiting' ? j.why : who ? who + ' on it' : heldForYou(j) ? 'asked for you' : jobKindOf(j).text || j.kind, JOB_PRI[j.urgency] || 'routine'];
  if (j.kind === 'chore') return [j.title.split(':')[0], deckWord(j.deck) + (j.room && roomName(j.deck, j.room) ? ' · ' + roomName(j.deck, j.room) : ''),
    j.status === 'waiting' ? j.why : who ? who + ' on it' : (CHORES[j.chore] || {}).text || 'chore', j.leave ? 'soon' : 'routine'];
  if (j.kind === 'restock') return [j.cargo === 'meals' ? 'Food to the cold store' : weekday(Math.floor(j.found / 1440) + 1) === DELIVERY.day ? 'Unload the Wednesday delivery' : 'Unload the delivery', j.cargo === 'meals' ? 'Hold to Deck 3' : 'Deck 5 · cargo hold', who ? who + ' on it' : j.cargo === 'meals' ? 'hover cart' : 'hover cart, ' + partsCrates() + (partsCrates() === 1 ? ' crate' : ' crates'), JOB_PRI[j.urgency]];
  if (j.case && typeof caseCard === 'function') { const cc = caseCard(j); if (cc) return cc; }   // 24k: a P1 case's card names the line's symptom, not the machine (0.55.16)
  const m = machineById(j.machine), room = (DECKS[m.deck].rooms[m.room] || {}).name;
  if (traceHidden(j)) return [traceTitle(j), deckWord(j.symptom.deck) + ' · the ' + j.symptom.line + ' line', (j.urgency === 2 ? 'failing: urgent' : JOB_WORD[j.kind]) + (who ? ', ' + who + ' on it' : ''), JOB_PRI[j.urgency]];   // a traced fault (0.33.59)
  const state = j.status === 'waiting' ? j.why : (j.urgency === 2 ? 'failing: urgent' : JOB_WORD[j.kind]) + (who ? ', ' + who + ' on it' : heldForYou(j) ? ', asked for you' : '');
  return [machineTitle(m.id) + (faultShows(j) ? ' (' + faultShows(j) + ')' : ''), deckWord(m.deck) + (room ? ' · ' + room.toLowerCase() : ''), state, JOB_PRI[j.urgency]];   // a real fault says what everyone notices (0.33.46)
}
function drawJobBoard(t) {
  const { g: c, c: cv } = t.userData, w = cv.width, h = cv.height, now = shipNow() % 1440;
  const jobs = jobsBoard(), cards = jobs.slice(0, 6).map(jobCard);
  c.textAlign = 'left';
  c.fillStyle = '#0c1a1f'; c.fillRect(0, 0, w, h);
  c.fillStyle = '#e8c06a'; c.font = '700 26px system-ui,sans-serif'; c.fillText('WORKS  ·  JOB BOARD', 22, 40);
  c.fillStyle = '#7fa9a3'; c.font = '500 17px system-ui,sans-serif'; c.textAlign = 'right';
  c.fillText(jobs.length + ' open  ·  ' + (now >= DAY_SHIFT[0] && now < DAY_SHIFT[1] ? 'day shift' : 'night shift'), w - 22, 40); c.textAlign = 'left';
  c.fillStyle = 'rgba(95,214,198,.35)'; c.fillRect(22, 54, w - 44, 2);
  cards.forEach(([title, where, state, pri], k) => {
    const x = 22 + (k % 2) * 304, y = 70 + Math.floor(k / 2) * 74;
    c.fillStyle = '#16303a'; c.fillRect(x, y, 292, 62);
    c.fillStyle = { urgent: '#e0503f', soon: '#e8c06a', routine: '#5fd6c6' }[pri] || '#5fd6c6'; c.fillRect(x, y, 7, 62);
    c.fillStyle = '#e8f4f1'; c.font = '600 20px system-ui,sans-serif'; c.fillText(title, x + 18, y + 26, 266);
    c.fillStyle = '#93b8b2'; c.font = '500 15px system-ui,sans-serif'; c.fillText(where + '  ·  ' + state, x + 18, y + 49, 266);
  });
  if (!cards.length) { c.fillStyle = '#7fa9a3'; c.font = '500 20px system-ui,sans-serif'; c.fillText('Nothing on the board. The Chief says it never lasts.', 22, 110); }
  if (jobs.length > 6) { c.fillStyle = '#7fa9a3'; c.font = '500 15px system-ui,sans-serif'; c.textAlign = 'right'; c.fillText('+ ' + (jobs.length - 6) + ' more', w - 22, h - 10); c.textAlign = 'left'; }
  t.needsUpdate = true;
}
// the main loop's step (section 12): redraw the board on Deck 5 when the jobs change (or each ship hour, for the shift)
function worksTick() {
  const B = JOB_BOARD, D = CART_DOCKS;
  shelfGlowTick(); holdCratesTick();
  if (B && B.def === deckDef) {
    machinesNow();
    const hr = Math.floor(shipNow() / 60);
    if (B.rev !== MACH_REV || B.min !== hr) { B.rev = MACH_REV; B.min = hr; drawJobBoard(B.t); }
  }
  if (REC_DECK && deckDef && deckDef.num === 7) recSigns();   // 0.84.4 (rec engineer B): the rec deck's signs, when the machines change
  if (D.def === deckDef && D.groups.size) {                // a docked cart is hidden while it's out on a run
    const m = Math.floor(shipNow());
    if (m !== D.min) { D.min = m; const out = cartsOut(shipNow()); for (const [n, g] of D.groups) g.visible = !out.has(n); }
  }
}
// the rec deck's signs (0.84.2, rec engineer B; plans/recdeck-plan.html section 6, from recShut): the pool goes milky when it's cloudy (a
// green tinge when it stings; its own water's uniforms, RK.poolOwn), a red tag on each tagged-out belay and at the foot of its route,
// red-and-white tape across a roped-off route (one merged mesh per colour, remade when they change), FLOAT ROOM CLOSED on legs against the
// float room's glass, the court's net and side fields off (their materials). Made the first time they
// show, in deckRoot (the deck's unload frees them); nothing while all's well; checked when MACH_REV or the hour moves; no R()
const REC_SIGNS = { root: null, rev: -1, hr: -1, key: '', tags: null, mats: null, plate: null };
function recSigns() {
  const S = REC_SIGNS, hr = Math.floor(shipNow() / 60);
  if (S.root !== deckRoot) Object.assign(S, { root: deckRoot, rev: -1, key: '', tags: null, mats: null, plate: null });
  if (S.rev === MACH_REV && S.hr === hr || !RK) return;
  const r = recShut(), c = MACH_HIST.get(histHour(shipNow())) || {}; S.rev = MACH_REV; S.hr = hr;
  const shut = [1, 2].filter(n => (c['7-belay-' + n] ?? 100) < 50);   // the belays tagged out (recShut's own reading): belay 1 is over route 1, belay 2 over route 2
  const key = [r.pool, shut, r.route, r.court, r.float].join('|'); if (key === S.key) return; S.key = key;
  const U = RK.poolOwn.userData.U, look = { cloudy: ['#8fb3b0', '#d6e4de'], sting: ['#2a9a86', '#86dcb0'] }[r.pool] || ['#1f8fa6', '#4fd0dc'];
  U.uDeep.value.copy(col(look[0])); U.uShallow.value.copy(col(look[1]));
  RK.net.visible = RK.field.visible = !r.court;
  if (S.tags) { deckRoot.remove(S.tags); S.tags.traverse(o => { if (o.geometry) o.geometry.dispose(); }); S.tags = null; }
  if (shut.length || r.route !== null) {
    const M_ = S.mats || (S.mats = { red: std('#d8322e', .6), white: std('#f2f2ee', .6) }), b = ROOM_BOX.K, g = new THREE.Group(), W_ = REC_WALL, len = W_.z1 - W_.z0, top = H - .12;
    g.position.set(X0(b.i0), 0, Z0(b.j0)); const zr = k => W_.z0 + len * (k + .5) / REC_ROUTES;
    for (const n of shut) { box(.03, .2, .12, M_.red, W_.x + .43, top - .5, zr(n), g); box(.03, .26, .18, M_.red, W_.x + .22, 1.3, zr(n), g); }   // on the belay's front, and on the wall at eye height (clear of its panels)
    if (r.route !== null) for (let k = 0; k < 6; k++) box(.02, .06, len / REC_ROUTES / 6 - .01, k % 2 ? M_.white : M_.red, W_.x + .62, 1.0, zr(r.route) - len / REC_ROUTES / 2 + len / REC_ROUTES * (k + .5) / 6, g);   // the tape, a hand in front of the holds
    mergeMeshes(g); g.traverse(o => { if (o.isMesh) o.castShadow = false; }); g.userData.noMerge = true; deckRoot.add(g); S.tags = g;
  }
  if (r.float && !S.plate) {                             // a sign on legs against the float room's glass, by its door: both faces, so it reads from either side and stays up when the cutaway lowers the glass
    const g = new THREE.Group(); g.position.set(X0(17) + .5, 0, Z0(12) - .22); recClosedSign(g, { text: 'FLOAT ROOM CLOSED', sub: 'gravity plates' });
    mergeMeshes(g); g.traverse(o => { if (o.isMesh) o.castShadow = false; }); g.userData.noMerge = true; deckRoot.add(g); S.plate = g;
  }
  if (S.plate) S.plate.visible = r.float;
}
// a closed sign on two legs (recSigns): red-bordered, the words in two lines on both faces (one canvas, made when it's first shown), the board between them
function recClosedSign(g, o) {
  const t = tex(512, 160, (c, w, h) => {
    c.fillStyle = '#1a1214'; c.fillRect(0, 0, w, h); c.strokeStyle = '#e0412f'; c.lineWidth = 10; c.strokeRect(8, 8, w - 16, h - 16);
    c.textAlign = 'center'; c.fillStyle = '#ffe9e4'; c.font = '800 50px system-ui,sans-serif'; c.fillText(o.text, w / 2, 76, w - 44);
    c.fillStyle = '#ff9a8a'; c.font = '600 32px system-ui,sans-serif'; c.fillText(o.sub || '', w / 2, 124, w - 44);
  });
  const m = new THREE.MeshBasicMaterial({ map: t, toneMapped: false }), geo = new THREE.PlaneGeometry(.9, .28);
  for (const sd of [1, -1]) { const p = new THREE.Mesh(geo, m); p.position.set(0, 1.2, sd * .025); p.rotation.y = sd > 0 ? 0 : Math.PI; g.add(p); }   // 5 mm off the board's faces
  box(.96, .34, .04, M.slateDark, 0, 1.2, 0, g); for (const x of [-.42, .42]) box(.04, 1.03, .04, M.slateDark, x, .515, 0, g);
}
// the Cart bay's two docks (0.33.15): the cartDock kit hands each parked cart's group to cartDockLive as Deck 5 is
// built (the Deck 6 architect's inert hook); worksTick hides it while that dock's cart is out
const CART_DOCKS = { def: null, groups: new Map(), min: -1 };
function cartDockLive(group, dock) {
  if (CART_DOCKS.def !== deckDef) { CART_DOCKS.def = deckDef; CART_DOCKS.groups = new Map(); }
  CART_DOCKS.groups.set(dock, group); CART_DOCKS.min = -1;
}
// which docks' carts are out at minute t: a claimed run's dock (its first stop, 5-cart-N), from taking it to putting it back
function cartsOut(t) {
  machinesNow();
  const out = new Set();
  for (const j of SHIP.jobs) if (j.kind === 'restock' && j.segs && j.status === 'claimed' && j.claimedBy !== 'you') {   // yours: SHIP.player.cart, below
    const cs = j.segs.filter(s => s.tag === 'cart'); if (cs.length < 2) continue;
    if (t >= cs[0].to && t < cs[cs.length - 1].to) out.add(+String(cs[0].placeId || '5-cart-1').split('-').pop() || 1);
  }
  const pc = SHIP.player && SHIP.player.cart;              // the cart you have out (the player engineer's 0.28.11)
  if (pc && pc.dock) out.add(+String(pc.dock).split('-').pop() || 1);
  return out;
}

// ---- saving: the save's ship.machines = { id: [cond, lastService] }, ship.machineHour, ship.jobs, ship.stores, ship.hold ----
SAVE_EXTRA.push(s => {
  const st = machinesNow(), out = {};
  for (const id in st) out[id] = st[id].drift ? [st[id].cond, st[id].lastService, st[id].drift] : [st[id].cond, st[id].lastService];   // in full, so a reload wears on exactly as before; a drift third (0.33.48)
  s.ship.machines = out; s.ship.machineHour = MACH_HOUR;
  if (MACH_NORM) s.ship.machineNorm = { build: GAME_BUILD, norm: MACH_NORM };   // the average day, so a reload needn't work it out
  s.ship.jobs = SHIP.jobs; s.ship.stores = SHIP.stores; s.ship.hold = SHIP.hold;
  if (SHIP.manifest && SHIP.manifest.length) s.ship.manifest = SHIP.manifest; if (SHIP.misplaced) s.ship.misplaced = SHIP.misplaced;   // 0.33.50
  s.ship.short = SHIP.short; s.ship.machineUse = { ...MACH_EXTRA };   // 0.33.18: what Stores has told you; your use not yet worn in
  s.ship.upkeep = { ...SHIP.upkeep };                    // 0.33.57: the ship meters' upkeep
});
// a save without machines (or with nonsense) leaves them to start afresh; machines the save doesn't know start
// fresh; ids it has that are gone are dropped
function machinesLoad(s) {
  const sh = s && s.ship;
  if (!sh || !sh.machines || typeof sh.machines !== 'object' || !Number.isInteger(sh.machineHour) || sh.machineHour > Math.floor(shipNow() / 60) + 1) return false;
  machinesReset(sh.machineHour); MACH_SEEN = shipNow();
  const mn = sh.machineNorm;                             // the average day, if this build saved it
  if (mn && mn.build === GAME_BUILD && mn.norm && typeof mn.norm === 'object' && mn.norm.heads && typeof mn.norm.heads === 'object') MACH_NORM = mn.norm;
  const MACH_RENAMED = { '5-lift-1': '5-mainlift-1' };   // 0.33.47: the main lift's old id (also the Deck 5 lift-wait place's); its open jobs drop and re-post
  for (const [id0, v] of Object.entries(sh.machines)) {
    const id = MACH_RENAMED[id0] && !(MACH_RENAMED[id0] in sh.machines) ? MACH_RENAMED[id0] : id0;
    if (!SHIP.machines[id] || !Array.isArray(v) || !(v[0] >= 0 && v[0] <= 100)) continue;
    SHIP.machines[id] = { cond: v[0], state: machineState(v[0]), lastService: Number.isFinite(v[1]) ? v[1] : null };
    const dr = Number.isFinite(v[2]) ? Math.max(-3, Math.min(3, Math.round(v[2]))) : 0; if (dr) SHIP.machines[id].drift = dr;   // a drift (0.33.48); an older save: settled
  }
  // jobs and supplies (0.33.1): a save before them starts with an empty list and full shelves
  const obj = o => o && typeof o === 'object' && !Array.isArray(o);
  machRecord(sh.machineHour - 1);
  if (Array.isArray(sh.jobs)) SHIP.jobs = sh.jobs.filter(j => obj(j) && typeof j.id === 'string' && (j.machine === null || SHIP.machines[j.machine]) && typeof j.kind === 'string');   // kinds are checked at the first run (jobsTidy, 0.33.47): section 24 registers its own after this
  if (Array.isArray(sh.manifest)) SHIP.manifest = sh.manifest.filter(c => obj(c) && typeof c.id === 'string' && typeof c.dest === 'string' && Number.isInteger(c.n) && c.n > 0 && c.n < 10).map(c => ({ id: c.id, dest: c.dest, n: c.n }));   // 0.33.50; older saves: none
  if (obj(sh.misplaced) && sh.misplaced.part in STOCK && typeof sh.misplaced.on === 'string') SHIP.misplaced = { part: sh.misplaced.part, on: sh.misplaced.on };
  for (const k of ['stores', 'hold']) if (obj(sh[k])) for (const [p, n] of Object.entries(sh[k])) if (Number.isInteger(n) && n >= 0) SHIP[k][p] = n;
  if (obj(sh.short)) for (const [p, n] of Object.entries(sh.short)) if (Number.isFinite(n)) SHIP.short[p] = n;
  if (obj(sh.machineUse)) for (const [id0, n] of Object.entries(sh.machineUse)) { const id = MACH_RENAMED[id0] || id0; if (SHIP.machines[id] && n > 0 && n < 50) MACH_EXTRA[id] = n; }
  SHIP.upkeep = {}; if (obj(sh.upkeep)) for (const k of SYSTEMS) if (Number.isFinite(sh.upkeep[k])) SHIP.upkeep[k] = Math.max(0, Math.min(UPKEEP_CAP, sh.upkeep[k]));   // 0.33.57; an older save: none (its meters read as before)
  JOBS_TIDY = false; return true;
}
machinesLoad(SAVED);
jobWhere.on = true;                                      // crew go to their jobs (whereIs asks jobWhere)

