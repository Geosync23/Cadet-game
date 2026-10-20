// =====================================================================
// 14. SCHEDULES
// Where everyone is, at any ship minute, on any deck, drawn or not.
//   planDay(person, day) -> [{ from, to, act, deck, type, placeId, fromDeck?, tag? }, ...] covering the day,
//                           from and to in absolute ship minutes (shipNow()'s units), back to back
//   whereIs(person, t)   -> { deck, act, type, placeId, moving, fromDeck, until } at absolute ship minute t
//   peopleOn(deck, t)    -> everyone whereIs puts on that deck at t, with where
//   runDay(day, step, fn) and dayReport(day): step a whole day with no drawing (for day_check.py)
// A ship day is planned for everyone at once (shipDay), one person after another in wake-up order, so each
// takes only places nobody holds: a place is never double-booked, and someone who finds the showers or the
// servery full waits a few minutes, then makes do. Beds are always the person's own; work stations are fixed
// per person and shift (schedDesks). Every choice comes from schedU(seed, day, k), a hash, so the same crew and
// places always give the same day. Variety, in layers: the rota and days off; the shape of the weekday
// (WEEK_SHAPE); seeded jitter (waking 5-25 minutes either way, meal lengths, lingering); habits (HABITS in
// section 9); and choices weighted by need (gym, calls home, laundry).
// It reads ROSTER (+ ROSTER_GUESTS) from section 9 and each deck's places from DECKS[n].places. Nothing here
// calls R() or draws anything.
// =====================================================================
const SCHED_COMMUTE = 2;                                 // a lift ride, ship minutes; you're on the new deck after it
const MEALS = { breakfast: [360, 540], dinner: [1020, 1230] };   // breakfast to 09:00 since the day shift starts then (0.71.1; was to 08:00)
const SHIFTS = { day: [540, 1020], night: [1260, 360] }; // 09:00-17:00 (the user's playtest answer, 0.71.1; was 08:00), 21:00-06:00 (into the next day)
// the shape of each weekday (0 = Monday)
const WEEK_SHAPE = [
  { early: 10 },                                         // Monday: all-hands briefing, the day shift starts 10 minutes early
  {},
  { drill: 900 },                                        // Wednesday: a drill at 15:00; anyone off duty musters by the lift for 15 minutes
  { inspect: true },                                     // Thursday: bunk inspection, juniors tidy their bunks after washing
  { late: 30 },                                          // Friday: bedtimes 30 minutes later
  { late: 20 },                                          // Saturday: a little later too
  { lieIn: 30 },                                         // Sunday: anyone off duty lies in 30 minutes longer
];
// where leisure happens: [deck, place type, weight]. Habits add their favourites; options with no places are skipped
// who: 'junior', 'officer' (anyone above junior) or 'deck2' (officers, and anyone who works on Deck 2)
const LEISURE = [[3, 'lounge-seat', 3], [3, 'garden', 2], [3, 'bench', 2], [4, 'common-room', 2, 'junior'], [4, 'music', 1], [4, 'bench', .5],
  [1, 'common-room', 1, 'officer'], [1, 'lounge-seat', .5, 'officer'], [2, 'lounge-seat', 1.5, 'deck2'], [2, 'bench', .5, 'deck2'], [2, 'common-room', 1.5, 'deck2']];
const HABIT_LEISURE = {
  'garden-lover': [[3, 'garden', 8]], 'lounge-regular': [[3, 'lounge-seat', 8]], 'common-room': [[4, 'common-room', 8, 'junior']],
  'music': [[4, 'music', 8]], 'window-seat': [[1, 'window', 4], [2, 'window', 4], [3, 'window', 6], [4, 'window', 4], [5, 'window', 2]], 'quiet-corner': [[3, 'lounge-seat', 4], [1, 'common-room', 3], [2, 'lounge-seat', 4]],
};
// what someone does at a place (plans/pillar2-plan.md, "Activities on places"): the place's `anim`, else by type
// (the music room is listening unless someone plays: the musician habit sets 'play'; poseOf in 8b agrees)
const PLACE_ANIM = { gym: 'lift', callhome: 'call', shop: 'browse', laundry: 'fold', 'work:galley': 'cook' };
const placeAnim = pl => pl ? pl.anim || PLACE_ANIM[pl.type] || (pl.type === 'garden' && pl.pose === 'stand' ? 'water' : null) : null;
// needs, 0-100, 100 = fully met (the plan's "Needs"). Crew needs are on paper: crewNeeds(person, t) reads them off
// the plans, and needsEst(person, day) is the start-of-day estimate that steers the day's choices (below)
const NEEDS = ['hunger', 'energy', 'hygiene', 'fitness', 'social'];
const SOCIAL_TYPES = new Set(['mess-seat', 'lounge-seat', 'common-room', 'music', 'garden', 'bench', 'gym', 'shop', 'servery-queue']);
// the most people Deck 3 holds in the evening (17:00-24:00) before leisure goes elsewhere; meals aren't capped.
// Infinity: no cap (about 64-73 at the peak). Set it to what the crowd can draw there.
const DECK3_EVENING_MAX = Infinity;
const LINE_WALK = [4, .55, [33, 4]];                    // the walk to the servery line (0.26.30): ship minutes for serving and getting to a seat, a tile's walk (CREW_SPEED), the line
// the Works crew's tea and biscuits (the user's playtest answer, 0.71.1; it replaces their random 10:00-14:00 tea and the
// "half ten" tea): from 13:00 in the Deck 5 tea corner (its lounge seats, 5-tea-1..3), a slot of `dur` minutes starting
// at 13:00, 13:15, 13:30 or 13:45 (seeded per person and day), waiting up to `wait` for a place. Most go (odds; the
// tea-break habit always; workaholics now and then). For others: tea is out from WORKS_TEA.at to WORKS_TEA.until
const WORKS_TEA = { at: 780, until: 840, step: 15, slots: 4, dur: 15, wait: 8, odds: .75, busy: .3 };
const worksTeaOn = t => { const m = ((t % 1440) + 1440) % 1440; return m >= WORKS_TEA.at && m < WORKS_TEA.until; };   // t: absolute ship minutes (any day: the caller checks it's a workday)
const STOPS = new Set(['queue', 'grab', 'drill', 'inspection', 'tea', 'toilet', 'hands', 'lift', 'pay', 'break']);   // short stops that never stretch to fill time
const RANK_ORDER = ['captain', 'xo', 'chief', 'senior', 'officer', 'junior', 'guest'];

// ---- data access (read at call time, so section 9's ROSTER and every deck's places are in by then) ----
let SCHED_DATA = null;
function schedData() {
  if (SCHED_DATA) return SCHED_DATA;
  const people = ROSTER.concat(ROSTER_GUESTS, guestPeople(), typeof ROSTER_RESERVE !== 'undefined' ? ROSTER_RESERVE : [])   // and the visitors aboard for a few days (Pillar 3), and the crew still to come (Pillar 4)
    .filter(p => !p.player);                             // you live your own day
  const places = [];
  // a machine's panel place isn't handed out as a desk (A5b). Event places (an `event` field) are listed by event
  // below; those only for an event (type 'event', or Deck 1's handover and walk) are kept out of everyday use, while
  // everyday seats an event also uses (the observatory's window seats) stay in it
  const EVENT_ONLY = new Set(['handover', 'walk']), evPlaces = [];
  for (const n of Object.keys(DECKS).map(Number)) if (!DECKS[n].playerOnly) for (const p of (DECKS[n].places || [])) if (!p.machine) (p.event && (p.type === 'event' || EVENT_ONLY.has(p.event)) ? evPlaces : places).push({ ...p, deck: n });
  const byId = new Map(places.concat(evPlaces).map(p => [p.id, p]));
  // private places: one named after a bed ('4-05-wash') belongs to whoever sleeps there, and so does any place
  // in a room with a bed place in it (an en-suite, a desk, an armchair). In a room of several beds (a bunk room)
  // it's shared by the people who sleep there. owner: placeId -> [bed ids]
  const beds = new Set(people.map(p => p.bed).concat(places.filter(p => p.type === 'bed').map(p => p.id)));
  const roomBeds = new Map();
  for (const p of places) if (p.type === 'bed' && p.room) { const k = p.deck + '|' + p.room; if (!roomBeds.has(k)) roomBeds.set(k, []); roomBeds.get(k).push(p.id); }
  const owner = new Map();
  for (const p of places) {
    if (p.type === 'bed') continue;
    for (let i = p.id.lastIndexOf('-'); i > 0; i = p.id.lastIndexOf('-', i - 1)) if (beds.has(p.id.slice(0, i))) { owner.set(p.id, [p.id.slice(0, i)]); break; }
    if (!owner.has(p.id) && p.room && roomBeds.has(p.deck + '|' + p.room)) owner.set(p.id, roomBeds.get(p.deck + '|' + p.room));
  }
  const nat = (a, b) => a.id.localeCompare(b.id, 'en', { numeric: true });
  const shared = new Map();                              // 'deck|type' -> the places anyone may use, in id order
  // (a till, anim 'pay', is listed as type 'pay' on its deck rather than under its own type, so browsers don't stop at it)
  for (const p of places) if (!owner.has(p.id) && p.type !== 'bed') { const k = p.deck + '|' + (p.anim === 'pay' ? 'pay' : p.type); if (!shared.has(k)) shared.set(k, []); shared.get(k).push(p); }
  for (const l of shared.values()) l.sort(nat);
  const own = new Map();                                 // bed -> its own places
  for (const [id, bs] of owner) for (const b of bs) { if (!own.has(b)) own.set(b, []); own.get(b).push(byId.get(id)); }
  const desks = schedDesks(people.filter(p => !p.replaces), shared);   // an arrival takes the desk of the one they replace, so no one else's moves
  for (const p of people) if (p.replaces && desks.has(p.replaces)) desks.set(p.id, desks.get(p.replaces));
  // stations nobody on the day shift has, outside locked rooms: someone from that department stands in each day
  const taken = new Set(people.filter(p => p.shift !== 'night').map(p => desks.get(p.id)));
  const spare = [...shared.entries()].filter(([k]) => /\|work:/.test(k)).flatMap(([, l]) => l)
    .filter(pl => !taken.has(pl.id) && !schedRoomLocked(pl.deck, pl.room) && !pl.machine && !(galleyRotaOn() && pl.type === 'work:galley') && pl.type !== 'work:garden');
  // the new habits' places: treadmills (gym, anim 'run'), the garden's standing spots (tending), the bar's seats
  // (anim 'drink'), and the observatory on Deck 2
  for (const n of Object.keys(DECKS).map(Number)) {
    const sub = (key, list) => { if (list.length) shared.set(n + '|' + key, list); };
    const obs = Object.entries(DECKS[n].rooms || {}).filter(([, r]) => /observatory/i.test(r.name || '')).map(([k]) => k);
    sub('gym-run', (shared.get(n + '|gym') || []).filter(pl => pl.anim === 'run'));
    sub('garden-tend', (shared.get(n + '|garden') || []).filter(pl => pl.pose === 'stand'));
    sub('bar', (shared.get(n + '|lounge-seat') || []).filter(pl => pl.anim === 'drink'));
    sub('observatory', ['lounge-seat', 'bench', 'common-room'].flatMap(t => shared.get(n + '|' + t) || []).filter(pl => obs.includes(pl.room)));
    // gatherings' places (answers 24 and 25): anything with `event: 'handover' | 'walk' | 'observatory-night'`, as
    // n|@handover and so on, in id order (the Captain walks them in that order). Type 'event' places serve nothing else
    const evs = new Map(); for (const pl of places.concat(evPlaces)) if (pl.deck === n && pl.event) { if (!evs.has(pl.event)) evs.set(pl.event, []); evs.get(pl.event).push(pl); }
    // and a venue's crowd spots (the deck architect's `gather` places, not the lead's) as n|@gather-<venue>: the shuttle bay's for farewell friends (0.26.38)
    for (const pl of places) if (pl.deck === n && pl.gather && !pl.lead) { const k = 'gather-' + pl.gather; if (!evs.has(k)) evs.set(k, []); evs.get(k).push(pl); }
    for (const [ev, l] of evs) sub('@' + ev, l.sort(nat));
    if (n === 7) {                                       // the rec deck (RA, 0.83.0): its seats by room, and the court's queue (the stands' front row by the gate)
      const rs = shared.get('7|rec:seat') || [];
      sub('rec-stand', rs.filter(pl => pl.room === 'T')); sub('rec-aud', rs.filter(pl => pl.room === 'A' && !pl.ring)); sub('rec-ring', rs.filter(pl => pl.ring));
      sub('rec-courtq', rs.filter(pl => pl.room === 'T' && pl.at[1] === 11 && pl.at[0] >= 12));
    }
    sub('window', [...new Set([...shared.entries()].filter(([k]) => k.startsWith(n + '|') && !/\|work:/.test(k)).flatMap(([, l]) => l))].filter(pl => pl.window));   // answer 21: seats by a window
  }
  if (typeof eventPools === 'function') eventPools(shared);   // section 18: the events' own place lists
  const deskIds = new Set(desks.values());               // the desks someone has (desks aren't booked in occ)
  SCHED_DATA = { people, places, byId, owner, shared, own, desks, spare, deskOf: id => deskIds.has(id) };
  return SCHED_DATA;
}
const deckOf = id => +String(id).split('-')[0];
// a locked room: one whose every door is 'closed' (the ready room, a bedroom), read from the deck's map and doors
function schedRoomLocked(n, room) {
  const def = DECKS[n], at = (i, j) => (def.map[j] || '')[i];
  const doors = Object.entries(def.doors || {}).filter(([k]) => { const [o, i, j] = k.split(','); return (o === 'v' ? [at(+i - 1, +j), at(+i, +j)] : [at(+i, +j - 1), at(+i, +j)]).includes(room); });
  return doors.length > 0 && doors.every(([, t]) => t === 'closed');
}
// work stations: fixed per person and shift. In rank order, each takes the next station of their type on their
// work deck; when those run out, any other workstation on the deck nobody on that shift has, outside locked
// rooms (bedrooms' places are private already); else none (null)
function schedDesks(people, shared) {
  const desks = new Map(), used = new Map();
  const order = people.filter(p => p.work && !(galleyRotaOn() && p.dept === 'galley') && p.dept !== 'garden').sort((a, b) => RANK_ORDER.indexOf(a.rank) - RANK_ORDER.indexOf(b.rank) || (a.id < b.id ? -1 : 1));
  for (const pass of [0, 1]) for (const p of order) {
    if (desks.has(p.id) && desks.get(p.id)) continue;
    const pool = (pass === 0 ? shared.get(p.work.deck + '|' + p.work.place) || []
      : [...shared.entries()].filter(([k]) => k.startsWith(p.work.deck + '|work:')).flatMap(([, l]) => l).filter(pl => !schedRoomLocked(pl.deck, pl.room)))
      .filter(pl => !pl.machine && !(galleyRotaOn() && pl.type === 'work:galley') && pl.type !== 'work:garden');   // machine panels are for servicing (B2); the galley and the garden book their own
    // a desk is taken for a shift, or, for people with rota.hours, only for those hours (the storekeepers share the till)
    const hrs = p.rota && p.rota.hours, clash = (a, b) => !a || !b || a.some(([x, y]) => b.some(([u, v]) => x < v && u < y));
    const d = pool.find(pl => !(used.get(p.shift + '|' + pl.id) || []).some(h => clash(h, hrs)));
    if (d) (used.get(p.shift + '|' + d.id) || used.set(p.shift + '|' + d.id, []).get(p.shift + '|' + d.id)).push(hrs || null);
    desks.set(p.id, d ? d.id : null);
  }
  return desks;
}

// ---- seeded choices: schedU(seed, day, k) is uniform in [0, 1), the same every time for the same inputs ----
function schedU(seed, day, k) {
  let h = (seed | 0) ^ Math.imul(day + 7, 0x9E3779B1) ^ Math.imul(k + 13, 0x85EBCA77);
  h = Math.imul(h ^ h >>> 16, 0x7FEB352D); h = Math.imul(h ^ h >>> 15, 0x846CA68B); h ^= h >>> 16;
  return (h >>> 0) / 4294967296;
}
const isWorkDay = (p, d) => !!p.work && !((p.rota && p.rota.offDays) || []).includes(weekday(d));
// your shift's start (Pillar 4, for section 20's reputation): on a work day, the first minute from 09:00 (DAY_SHIFT[0]) that you're in
// a Works room on Deck 5, simNote('shiftStart', { late: minutes after 09:00 }); not there by 12:30, { late: 120,
// missed: true }. Once a day (the flag 'shiftSent' holds the day, so a reload doesn't send it again)
function shiftTick() {
  const d = SHIP.time.day, m = SHIP.time.min;
  if (m < DAY_SHIFT[0] || flag('shiftSent') === d || !playerShiftOn(d)) return;
  let here = false;
  try { here = typeof careerAtWork === 'function' ? careerAtWork() : deckDef.num === 5 && (DECKS[5].places || []).some(pl => pl.type === 'work:works' && pl.room === roomAt(...player.here())); } catch (e) { here = false; }   // clocked in (the career engineer's time clock, 0.61.13)
  if (!here && m < (typeof CAREER !== 'undefined' ? CAREER.missBy : 600)) return;   // the career engineer's time clock (0.61.17): missed only if not clocked in by 12:30, as the career counts it
  flagSet('shiftSent', d);
  const inAt = typeof careerClockedIn === 'function' && careerClockedIn(d) ? SHIP.career.ci % 1440 : m;   // late by the clock-in time
  simNote('shiftStart', here ? { late: Math.max(0, Math.round(inAt - DAY_SHIFT[0])) } : { late: 120, missed: true });
}
// whether you (the player) are on shift on day d: your own rota, like a Works junior's (ROSTER_PLAYER.rota.offDays,
// section 9: Saturday and Sunday off). A day off has no shift and no jobs expected; the job board stays open. Read
// when used (ROSTER_PLAYER comes later in the file); before it exists, Saturday and Sunday are the days off
function playerShiftOn(d) {
  if (typeof careerOff === 'function' && careerOff(d)) return false;   // a leave or sick day, or let go (the career engineer, 0.61.0)
  try { return isWorkDay(ROSTER_PLAYER, d); } catch (e) { return weekday(d) < 5; }
}
// The galley rota (section 16, the galley engineer). galleyDay(person, day) -> null | { role, wake, bedBy,
// blocks: [{ from, to, placeId, task }], meals: { breakfast: [from, to], dinner: [from, to] } }, minutes from that
// day's midnight. role null is a day off. Each block (a stint at one station) is a work segment there; touching
// stints make one stretch of work; a given meal is a normal meal (queue, then a seat) between those times; a meal
// not given is the normal one in its window; bedBy caps that night's bedtime. If only the older galleyShift(person,
// day) -> [[from, to, placeId?, task?], ...] exists, that's used instead. Consulted only for day-shift galley staff.
// A work day in blocks, for anyone whose hours aren't the plain shift: galley staff (their rota), and anyone with
// rota.hours ([[from, to], ...] in minutes from midnight, on their work days, at their own desk: the storekeepers)
function shiftBlocks(p, d) {
  if (p.shift === 'night') return null;
  if (p.dept === 'garden') {                             // the garden crew: gardenDay, below, shaped like galleyDay
    const g = gardenDay(p, d); if (!g) return null;
    const blocks = g.role ? g.blocks.map(x => [x.from, x.to, x.placeId || null, x.task || null]) : [];
    return { blocks: blocks.length ? blocks : null, wake: g.wake, bedBy: g.bedBy, meals: g.meals || {} };
  }
  const hrs = p.rota && p.rota.hours;
  if (p.dept !== 'galley' || !(typeof galleyDay === 'function' || typeof galleyShift === 'function')) {
    if (!Array.isArray(hrs) || !hrs.length || !isWorkDay(p, d)) return null;
    return { blocks: hrs.filter(x => x[1] > x[0]).map(x => [x[0], x[1], null, null]).sort((x, y) => x[0] - y[0]), wake: null, bedBy: null, meals: null, desk: true };
  }
  if (typeof galleyDay === 'function') {
    const g = galleyDay(p, d); if (!g) return null;
    const blocks = g.role && Array.isArray(g.blocks) ? g.blocks.filter(x => x.to > x.from).map(x => [x.from, x.to, x.placeId || null, x.task || null]) : [];
    return { blocks: blocks.length ? blocks.sort((x, y) => x[0] - y[0]) : null, wake: g.wake == null ? null : g.wake, bedBy: g.bedBy == null ? null : g.bedBy, meals: g.meals || {} };
  }
  if (typeof galleyShift === 'function' && isWorkDay(p, d)) {
    const b = galleyShift(p, d);
    if (Array.isArray(b) && b.length && b.every(x => x[1] > x[0])) return { blocks: b.map(x => [x[0], x[1], x[2] || null, x[3] || null]).sort((x, y) => x[0] - y[0]), wake: null, bedBy: null, meals: null };
  }
  return null;
}
const galleyRotaOn = () => typeof galleyDay === 'function';   // the galley books its own stations
// ---- the garden crew (the working garden, with the galley engineer's crops and yields) ----
// gardenDay(p, d) -> null | { role, wake, bedBy, blocks: [{ from, to, placeId, task }], meals }, galleyDay's shape, for
// dept 'garden' (null for anyone else; role null on their days off, rota.offDays). A work day is their own hours: the
// rota.hoursOn item whose `days` hold today's weekday (the senior gardener covering the others' days off), else
// rota.hours, else 07:00-15:30. 'tend' at their own bed station (the deck architect's 'work:garden' places on Deck 3,
// one each; until those exist, the garden's standing spots, held so nobody else stands there; if theirs is taken, the
// next free one along the beds), and whoever is on at 10:00 does the day's 'pick' 10:00-10:45 there. The galley takes
// the pick at its end and posts the carry as a job (section 17's gardenCarry). On a harvest morning (section 18's
// 'harvest') the gardeners on duty lead it from their stations for its whole window instead of the pick (the senior,
// rota.team 'senior', is the lead). Meals at the normal times (an early or late stint eats at the station when it
// covers a whole meal window, as the galley does). gardenCrew(d) -> [{ id, pick, harvest, lead, hours }] for the
// galley's yields. Pure (rota, places and the traditions only); nothing changes while nobody is in dept 'garden'.
const GARDEN_SHIFT = [420, 930], GARDEN_PICK = [600, 645];
const gardenSpots = () => {
  const P = (DECKS[3] && DECKS[3].places) || [], nat = (a, b) => a.id.localeCompare(b.id, 'en', { numeric: true });
  const w = P.filter(pl => pl.type === 'work:garden' && !pl.machine).sort(nat);
  return w.length ? w : P.filter(pl => pl.type === 'garden' && pl.pose !== 'sit' && pl.anim === 'water').sort(nat);
};
const gardeners = d => schedPeople().filter(p => p.dept === 'garden' && p.shift !== 'night' && isWorkDay(p, d)).sort((a, b) => (a.id < b.id ? -1 : 1));
function gardenDay(p, d) {
  if (p.dept !== 'garden' || p.shift === 'night') return null;
  if (!isWorkDay(p, d)) return { role: null, wake: null, bedBy: null, blocks: [], meals: {} };
  const crew = gardeners(d), i = Math.max(0, crew.indexOf(p)), spots = gardenSpots();
  const own = spots.length ? spots[(i * Math.max(1, Math.floor(spots.length / Math.max(1, crew.length)))) % spots.length].id : null;
  let hv = null;
  try { hv = typeof eventsOn === 'function' && eventsOn(d).find(e => e.id === 'harvest') || null; } catch (e) { hv = null; }
  // their hours today: the rota.hoursOn item whose `days` hold today's weekday (covering someone's days off), else
  // rota.hours, else 07:00-15:30
  const r = p.rota || {}, oi = Array.isArray(r.hoursOn) ? r.hoursOn.find(x => x && Array.isArray(x.days) && x.days.includes(weekday(d))) : null, on = oi && oi.hours;
  const hrs = (Array.isArray(on) && on.length ? on : Array.isArray(r.hours) && r.hours.length ? r.hours : [GARDEN_SHIFT])
    .filter(x => x[1] > x[0]).slice().sort((x, y) => x[0] - y[0]);
  const [p0, p1] = hv ? [hv.from, hv.to] : GARDEN_PICK, blocks = [];
  const add = (from, to, placeId, task) => { if (to > from) blocks.push({ from, to, placeId, task }); };
  for (const [a, b] of hrs) {
    if (p0 >= a && p0 < b) {                             // on at the pick (or the harvest): pick, then back to the beds
      const e1 = Math.min(p1, b);
      add(a, p0, own, 'tend'); add(p0, e1, own, hv ? 'harvest' : 'pick'); add(e1, b, own, 'tend');
    } else add(a, b, own, 'tend');
  }
  return { role: 'gardener', wake: null, bedBy: null, blocks, meals: {} };
}
const gardenCrew = d => gardeners(d).map(p => { const b = gardenDay(p, d).blocks, f = t => { const x = b.find(y => y.task === t); return x ? [x.from, x.to] : null; };
  return { id: p.id, pick: f('pick') || f('harvest'), harvest: !!f('harvest'), lead: !!(p.rota && p.rota.team === 'senior'), hours: b.reduce((n, x) => n + x.to - x.from, 0) }; });
// a person's plans for a day before anyone else is considered: when they mean to wake and go to bed, and whether they work
// ---- appointments (Pillar 3, C3): the crew side of the device's Appointments ----
// SHIP.device.appts (section 19, the device engineer; saved there): { id, with: [crewId | 'guest:id' | 'place:id'],
// at: absolute ship minutes, len, where: placeId, kind: 'social'|'work'|'checkup'|'meeting'|'summons'|'invite',
// status: 'asked'|'yes'|'no'|'kept'|'missed', by }.
// apptReply(p, a): what someone says when asked, from their real day: { answer: 'yes'|'later'|'no', at, text }.
// An accepted one ('yes') is laid over their plan by whereIs (apptWhere): they go there, ride the lift if need be,
// and wait APPT_WAIT ship minutes; if you come ('kept', apptTick) they stay the whole `len`, else they go back to
// their day ('missed'). Nobody is punished for a missed one. Nothing here touches the plans (planWhere, dayReport).
const APPT_WAIT = 15;
const apptList = () => typeof SHIP !== 'undefined' && SHIP.device && Array.isArray(SHIP.device.appts) ? SHIP.device.appts : [];
const apptOn = a => !!a && (a.status === 'yes' || a.status === 'kept') && isFinite(a.at) && !!a.where && Array.isArray(a.with);
const apptPlace = a => { const d = deckOf(a.where), pl = (DECKS[d] && DECKS[d].places || []).find(q => q.id === a.where); return pl ? { ...pl, deck: d } : null; };
// each person's own place at it (0.71.2, for the officer ceremony's guests): a.places = { [id]: placeId } on the same
// deck, else the appointment's place as before
const apptPlaceOf = (a, id) => { const w = a.places && typeof a.places[id] === 'string' ? a.places[id] : null; if (!w) return apptPlace(a); const d = deckOf(w), pl = (DECKS[d] && DECKS[d].places || []).find(q => q.id === w); return pl ? { ...pl, deck: d } : apptPlace(a); };
// is p free from a to b (absolute minutes)? Free time, standing about, or (for work, a check-up or a summons) their
// own shift on the appointment's deck; never asleep, eating, at an event or at another appointment
function apptFree(p, a, from, to) {
  const pl = apptPlace(a), workOk = /^(work|checkup|summons|meeting)$/.test(a.kind || '');
  for (let t = from; t < to; t += 5) {
    const w = planWhere(p, t); if (!w) return false;
    const ok = (w.act === 'leisure' || w.act === 'off') && !(w.tag && /^ev-|^(drill|handover|stroll)$/.test(w.tag))
      || workOk && w.act === 'work' && pl && w.deck === pl.deck;
    if (!ok) return false;
  }
  return !apptList().some(o => o !== a && o.id !== a.id && apptOn(o) && o.with.includes(p.id) && o.at < to && from < o.at + (o.len || 30));
}
function apptReply(p, a) {
  const len = a.len || 30, C = SCHED_COMMUTE + 10, who = shortName(p);   // the lift and most of a walk
  if (!p || !apptPlace(a)) return { answer: 'no', at: null, text: who + ': "Where\'s that?"' };
  if (apptFree(p, a, a.at - C, a.at + len)) return { answer: 'yes', at: a.at, text: who + ': "See you at ' + hhmm(a.at % 1440) + '."' };
  const dayEnd = Math.floor(a.at / 1440) * 1440 + 22 * 60;
  for (let t = Math.ceil((a.at + 30) / 30) * 30; t + len <= dayEnd; t += 30)
    if (apptFree(p, a, t - C, t + len)) return { answer: 'later', at: t, text: who + ': "Can\'t then. How about ' + hhmm(t % 1440) + '?"' };
  return { answer: 'no', at: null, text: who + ': "Sorry, not today."' };
}
// where someone with an accepted appointment is (whereIs asks this first); null when none applies at t
function apptWhere(p, t) {
  for (const a of apptList()) {
    if (!apptOn(a) || !a.with.includes(p.id)) continue;
    const end = a.at + (a.status === 'kept' || a.occ ? (a.len || 30) : APPT_WAIT), pl = apptPlaceOf(a, p.id); if (!pl) continue;   // an occasion's host (section 18 via apptAdd, `occ`) stays the whole time, you or no you (0.26.34)
    // they set off in time to be there at a.at: the walk from the lift (about 1.3 x the straight line, at CREW_SPEED)
    const lift = DECKS[pl.deck].lift || pl.at, walk = Math.ceil(1.3 * Math.hypot(pl.at[0] - lift[0], pl.at[1] - lift[1]) / 1.15 * SHIP_RATE) + 1;   // ship minutes
    const go = a.at - walk, C = SCHED_COMMUTE;
    if (t < go - C - 3 || t >= end) continue;
    if (t < go - C) return null;                         // still finishing what they were doing
    const w = planWhere(p, go - C - 1);
    if (t < go && w && w.deck !== pl.deck)               // a lift ride if they're on another deck
      return { deck: pl.deck, act: 'commute', type: 'lift', placeId: null, moving: true, fromDeck: w.deck, from: go - C, until: go, tag: 'appt' };
    return { deck: pl.deck, act: 'appt', type: pl.type, placeId: pl.id, moving: false, fromDeck: undefined, from: go, until: end, tag: 'appt', anim: pl.anim || null };
  }
  return null;
}
// every ship minute (section 13's clock): you came (within 2 tiles of the place, on its deck, before they gave up) -> 'kept'; else 'missed'
function apptTick() {
  const now = shipNow();
  for (const a of apptList()) {
    if (a.status !== 'yes' || !isFinite(a.at) || now < a.at - 2) continue;
    const pl = apptPlace(a);
    if (pl && typeof deckDef !== 'undefined' && deckDef.num === pl.deck && typeof player !== 'undefined') {
      const c = cellPos(...pl.at); if (Math.hypot(player.obj.position.x - c.x, player.obj.position.z - c.z) < 2.2) { a.status = 'kept'; a.keptAt = now; simNote('apptKept', { id: a.id, with: a.with }); continue; }
    }
    if (now >= a.at + APPT_WAIT) { a.status = 'missed'; simNote('apptMissed', { id: a.id, with: a.with }); }
  }
}
// ---- doors for invitations and summons (C3, C10): the ready room, Deck 2 bedrooms, officers' cabins ----
// doorOpenFor(room, who, t, deck): a locked room is open to you ('player') and to the crew in the appointment while an
// accepted invitation or summons to a place in it runs (from 15 minutes before to 15 after it ends). False otherwise:
// with no appointments it changes nothing. Section 4's edgeBlocks asks it for 'closed' doors; section 10 opens the door.
function doorOpenFor(room, who, t = shipNow(), deck = typeof deckDef !== 'undefined' ? deckDef.num : null) {
  if ((who === 'player' || who === 'you' || (who && who.isPlayer)) && deck === 4 && room && room === ((DECKS[4].places || []).find(q => q.id === playerBed()) || {}).room) return true;   // your own cabin (0.71.2: 4-23 once you're an Officer, SHIP.works.home): your key opens it
  if ((who === 'player' || who === 'you' || (who && who.isPlayer)) && typeof occasionDoorOpen === 'function' && occasionDoorOpen(deck, room, t)) return true;   // section 18's occasions: a summons, the Captain's table
  if ((who === 'player' || who === 'you' || (who && who.isPlayer)) && typeof jobDoorOpen === 'function' && jobDoorOpen(deck, room)) return true;   // section 15: your job's next stop is in there (0.28.52)
  if ((who === 'player' || who === 'you' || (who && who.isPlayer)) && typeof worksHomeOpen === 'function' && worksHomeOpen(deck, room)) return true;   // section 24p: your own cabin, once you're an officer
  for (const a of apptList()) {
    if (!apptOn(a) || !/^(invite|summons|meeting|checkup|work|social)$/.test(a.kind || 'social')) continue;
    const pl = apptPlace(a); if (!pl || pl.deck !== deck || pl.room !== room) continue;
    if (t < a.at - 15 || t > a.at + (a.len || 30) + 15) continue;
    if (who === 'player' || (who && who.isPlayer) || a.with.includes((who && (who.p || who).id) || who)) return true;
  }
  return false;
}
// ---- guests (Pillar 3, C8): visitors aboard for a few days, from the crew designer's GUESTS (section 9) ----
// GUESTS: [{ id, name, spec | looks, role, cabin (their bed place id), arrive, leave (days of the year, 1-364; a
// stay may cross the year's end), template, work?, habits? }]. Event guests have arrive and leave null, and `event`
// and `stay` (days) instead: section 18 says when they're aboard through eventGuestDays(g) -> [arrive, leave] in
// ship days, or null; until it does, they're away. A guest lives off duty, from their GUEST_TEMPLATES entry
// (section 9): `day` places until 17:00 and `evening` ones after, as [deck, type, weight] (types with no places
// skipped), ['cabin', w] (resting in their own cabin) or ['work', w] (their own `work` place); a survivor has
// `firstDay` for their first `first` days; `wake` and `bed` are the times they get up and turn in. They come aboard
// at 10:00 on `arrive` (by the shuttle bay, Deck 5) and leave at 10:00 on `leave`; before and after, they're 'away'
// (deck 0: on no deck, so no one draws them). Nothing changes without GUESTS.
const GUEST_AT = 600;                                    // arrivals and departures, 10:00
const guestTpl = p => p.guest && typeof GUEST_TEMPLATES !== 'undefined' && GUEST_TEMPLATES[p.template] || null;
const strSeed = str => { let h = 2166136261; for (const c of String(str)) h = Math.imul(h ^ c.charCodeAt(0), 16777619); return h >>> 0; };
function guestPeople() {
  if (typeof GUESTS === 'undefined' || !Array.isArray(GUESTS)) return [];
  return GUESTS.filter(g => g && g.id && (g.cabin || g.bed)).map(g => ({ ...g, looks: g.looks || g.spec, rank: 'guest', dept: g.dept || 'guest', shift: 'day',
    rota: { offDays: [] }, work: null, guestWork: g.work || null, bed: g.bed || g.cabin, habits: g.habits || [], seed: g.seed || strSeed(g.id), guest: true }));
}
// where a guest's stay stands on ship day d: 'away', 'arrive', 'leave' or 'in' (aboard all day); crew are always 'in'.
// Stays from the data are days of the year; an event guest's are ship days from section 18
function guestStay(p, d) {
  if (!p.guest) return crewStay(p, d);
  let a = p.arrive, l = p.leave, y = d;
  if (a == null) { const ev = typeof eventGuestDays === 'function' ? eventGuestDays(p) : null; if (!ev) return 'away'; [a, l] = ev; }
  else y = ((d - 1) % 364 + 364) % 364 + 1;              // the day of the year (day 0, the arrival Sunday, is the last of the year before)
  if (y === a) return 'arrive';
  if (y === l) return 'leave';
  return (a <= l ? y > a && y < l : y > a || y < l) ? 'in' : 'away';   // a <= l, or across the year's end
}
// crew coming and going (Pillar 4): the crew designer's `aboard: [fromDay, toDay]` (either end null for open; missing
// or null for always). They leave on toDay at 15:00 by the shuttle bay and arrive on fromDay at 17:40 off the
// Sunday shuttle (ROSTER_ROTATIONS lists the days); an arrival `replaces` a leaver, taking their bed and desk.
// Pure (roster data only), so any day planned early or again agrees. crewLeaving(p) / crewArriving(p): those days, or null
const ROTA_OFF = 900, ROTA_ON = 1060, ROTA_WAIT = 30;  // a transfer: off at 15:00 (waiting in the shuttle bay from 14:30), on at 17:40
function crewStay(p, d) {
  const ab = p.aboard; if (!Array.isArray(ab)) return 'in';
  const [a, l] = ab;
  if (a != null && d < a || l != null && d > l) return 'away';
  if (a != null && d === a) return 'arrive';
  if (l != null && d === l) return 'leave';
  return 'in';
}
const crewLeaving = p => Array.isArray(p && p.aboard) ? p.aboard[1] : null;
const crewArriving = p => Array.isArray(p && p.aboard) ? p.aboard[0] : null;
// who's aboard on day d, who has left and who has arrived by then (the save's `crew`, the device's Roster)
function crewState(d) {
  const P = schedPeople().filter(p => !p.guest), st = p => crewStay(p, d);
  return { aboard: P.filter(p => st(p) !== 'away').map(p => p.id),
    left: P.filter(p => crewLeaving(p) != null && crewLeaving(p) < d).map(p => ({ id: p.id, day: crewLeaving(p) })),
    arrived: P.filter(p => crewArriving(p) != null && crewArriving(p) <= d).map(p => ({ id: p.id, day: crewArriving(p) })) };
}
const aboard = (p, d) => guestStay(p, d) !== 'away';
const aboardAllDay = (p, d) => guestStay(p, d) === 'in';
// a guest template's list as leisure options: 'cabin' is rest, 'work' their own work place. Weights count double,
// so the template outweighs a habit or two (a window-seat habit alone weighs 20)
const guestOpts = (p, list, bedDeck) => (list || []).map(o => o[0] === 'cabin' ? [bedDeck, 'rest', 2 * o[1]]
  : o[1] === 'work:infirmary' && p.template === 'survivor' && guestWard(o[0]) ? [o[0], 'patient-bed', 2 * o[2]]   // a patient: the ward's beds when the deck has them
  : o[0] === 'work' ? (p.guestWork ? [p.guestWork.deck, p.guestWork.place, 2 * o[1]] : null) : [o[0], o[1], 2 * o[2]]).filter(Boolean);
const guestWard = n => (schedData().shared.get(n + '|patient-bed') || []).length > 0;
// which day of their stay day d is for a guest: 1 on the day they arrive (counted up to `max`; past it, max + 1)
const guestDayNo = (p, d, max = 7) => { for (let i = 0; i < max; i++) if (guestStay(p, d - i) === 'arrive') return i + 1; return max + 1; };
// a guest's day on an arrival or departure day: away until 10:00 then the shuttle bay, or the shuttle bay then away
function guestTrim(p, d, segs, spot) {
  if (aboardAllDay(p, d)) return segs;
  const B = (d - 1) * 1440, away = (from, to) => ({ from, to, act: 'away', deck: 0, type: null, placeId: null });
  if (!aboard(p, d)) return [away(B, B + 1440)];
  const arriving = guestStay(p, d) === 'arrive', cut = B + (p.guest ? GUEST_AT : arriving ? ROTA_ON : ROTA_OFF), out = [];   // crew: off at 15:00, on at 17:40
  if (arriving) {
    out.push(away(B, cut), { from: cut, to: cut + 10, act: 'off', deck: 5, type: null, placeId: null, tag: 'arrive' });
    for (const s of segs) if (s.to > cut + 10) out.push({ ...s, from: Math.max(s.from, cut + 10) });
  } else if (p.guest) {
    for (const s of segs) if (s.from < cut - 10) out.push({ ...s, to: Math.min(s.to, cut - 10) });
    out.push({ from: cut - 10, to: cut, act: 'off', deck: 5, type: null, placeId: null, tag: 'leave' }, away(cut, B + 1440));
  } else {                                               // crew: from 14:30 they wait in the shuttle bay (after their farewell there), boarding at 15:00
    const w0 = cut - ROTA_WAIT;
    for (const s of segs) if (s.from < w0) out.push({ ...s, to: Math.min(s.to, w0) });
    const last = out[out.length - 1], bay = (schedData().shared.get('5|event') || []).filter(pl => /shuttle-bay-crowd/.test(pl.id));
    const placeId = spot || (last && last.deck === 5 && /shuttle-bay/.test(last.placeId || '') ? last.placeId : bay.length ? bay[strSeed(p.id) % bay.length].id : null);   // spot: held for them by shipDay (0.26.38)
    if (last && last.deck !== 5 && last.to - last.from > SCHED_COMMUTE) { last.to = w0 - SCHED_COMMUTE; out.push({ from: w0 - SCHED_COMMUTE, to: w0, act: 'commute', deck: 5, type: 'lift', placeId: null, fromDeck: last.deck }); }
    out.push({ from: w0, to: cut, act: 'off', deck: 5, type: null, placeId, tag: 'leave' }, away(cut, B + 1440));
  }
  return out;
}
// ---- habits that change slowly (answer 18): a few changes a month, the same in every game ----
// From the second week on, each week has 0, 1 or 2 changes (about 3.5 a month): someone takes up a habit
// (a junior starts running, someone takes to the observatory) or drops one (stops going to the bar). Each is
// picked with schedU from the week alone, so the ship's history is the same however it's played; a change lands
// on its day and holds from then on. habitsOn(p, d) is the person's habits on day d (section 9's list plus the
// changes so far); everything in this section reads habits through it. SHIP.habitLog is the changes up to today,
// [{ day, id, add and/or drop, shift (which habitShifts item), text }], saved with the game (a saved log is kept as it was for the weeks it covers).
const HABIT_TAKE = {                                     // habit -> who might take it up, and how it's said
  runner: [p => p.rank === 'junior' || p.dept === 'works', 'has taken up running'],
  'gym-regular': [() => true, 'has started going to the gym after shift'],
  stargazer: [() => true, 'has started going up to the observatory in the evenings'],
  gardener: [() => true, 'has started helping out in the garden'],
  'tea-break': [p => p.shift !== 'night', 'has taken to a mid-shift tea break'],
  'calls-home': [() => true, 'has been calling home more often'],
  shopper: [() => true, 'has become a regular at the crew store'],
  'window-seat': [() => true, 'has taken a liking to the window seats'],
  'lounge-regular': [p => p.rank !== 'junior', 'spends evenings in the bow lounge now'],
  'early-to-bed': [() => true, 'has started turning in early'],
};
const HABIT_DROP = {
  'bar-regular': 'has stopped going to the bar', runner: 'has given up running', 'gym-regular': 'has dropped the gym',
  'night-owl': 'has been turning in earlier', 'late-sleeper': 'has been getting up earlier', 'skips-breakfast': 'has started eating breakfast',
  'lingers-at-meals': 'eats quicker these days', 'tea-break': 'has dropped the mid-shift tea', workaholic: 'has stopped staying late',
  'early-to-bed': 'has been staying up later', shopper: 'hardly goes to the store now',
};
const HABIT_WEEKS = [[]];                                // week w (days 7w+1 .. 7w+7) -> its changes; week 0 has none
let HABIT_SAVED = null;                                  // the saved log, kept for the weeks it covers
function habitWeek(w) {
  while (HABIT_WEEKS.length <= w) {
    const k = HABIT_WEEKS.length, ppl = schedPeople().filter(q => !q.guest && !q.replaces), out = [], d0 = 7 * k + 1;   // never a guest or someone still to come
    if (HABIT_SAVED && HABIT_SAVED.some(c => c.day > 7 * k + 7)) { HABIT_WEEKS.push(HABIT_SAVED.filter(c => c.day >= d0 && c.day < d0 + 7)); continue; }
    const U = j => schedU(9100, k, j), n = U(0) < .35 ? 0 : U(0) < .8 ? 1 : 2;
    // the crew designer's own changes first (ROSTER[i].habitShifts: [{ add?, drop?, why }], why a whole sentence),
    // any still valid and not yet used; four times in five one of those, else anyone from the lists below
    const used = new Set(); for (let j = 1; j < k; j++) for (const c of HABIT_WEEKS[j]) if (c.shift) used.add(c.id + '|' + c.shift);
    const valid = (p, has) => (p.habitShifts || []).map((x, j) => [x, j]).filter(([x, j]) => !used.has(p.id + '|' + j) && (x.add || x.drop) && (!x.add || !has.includes(x.add)) && (!x.drop || has.includes(x.drop)));
    for (let i = 0; i < n && ppl.length; i++) {
      const day = d0 + Math.floor(U(20 + i) * 7), own = ppl.filter(q => !out.some(c => c.id === q.id) && valid(q, habitsOn(q, d0 - 1)).length);
      if (own.length && U(50 + i) < .8) {
        const p = own[Math.floor(U(10 + i) * own.length)], v = valid(p, habitsOn(p, d0 - 1)), [x, j] = v[Math.floor(U(40 + i) * v.length)];
        out.push({ day, id: p.id, ...(x.add ? { add: x.add } : {}), ...(x.drop ? { drop: x.drop } : {}), shift: j, text: x.why || shortName(p) + ' ' + (x.add ? (HABIT_TAKE[x.add] || [0, 'has a new habit'])[1] : HABIT_DROP[x.drop] || 'has dropped a habit') + '.' });
        continue;
      }
      const p = ppl[Math.floor(U(10 + i) * ppl.length)];
      if (out.some(c => c.id === p.id)) continue;
      const has = habitsOn(p, d0 - 1), drops = has.filter(h => HABIT_DROP[h]);
      const takes = Object.keys(HABIT_TAKE).filter(h => !has.includes(h) && HABIT_TAKE[h][0](p));
      const drop = drops.length && (U(30 + i) < .4 || !takes.length);
      if (drop) { const h = drops[Math.floor(U(40 + i) * drops.length)]; out.push({ day, id: p.id, drop: h, text: shortName(p) + ' ' + HABIT_DROP[h] + '.' }); }
      else if (takes.length) { const h = takes[Math.floor(U(40 + i) * takes.length)]; out.push({ day, id: p.id, add: h, text: shortName(p) + ' ' + HABIT_TAKE[h][1] + '.' }); }
    }
    HABIT_WEEKS.push(out.sort((a, b) => a.day - b.day));
  }
  return HABIT_WEEKS[w];
}
function habitsOn(p, d) {
  let hs = p.habits || [];
  for (let w = 1; w <= Math.floor((d - 1) / 7); w++) for (const c of habitWeek(w)) if (c.id === p.id && c.day <= d) {
    if (c.drop) hs = hs.filter(h => h !== c.drop);
    if (c.add && !hs.includes(c.add)) hs = hs.concat(c.add);
  }
  const rh = REC_ON && recHabit(p); if (rh && !hs.includes(rh)) hs = hs.concat(rh);   // the rec deck's habits (RA, 0.83.0): never in HABIT_TAKE or HABIT_DROP, so the weekly changes are as before
  return hs;
}
Object.defineProperty(SHIP, 'habitLog', { get: () => { const d = SHIP.time.day, out = []; for (let w = 1; w <= Math.floor((d - 1) / 7); w++) out.push(...habitWeek(w).filter(c => c.day <= d)); return out; }, enumerable: false });
SAVE_EXTRA.push(save => { save.habitLog = SHIP.habitLog; });
if (SAVED && Array.isArray(SAVED.habitLog) && SAVED.habitLog.every(c => c && c.day >= 8 && typeof c.id === 'string')) HABIT_SAVED = SAVED.habitLog;
// ---- gatherings: what a person goes to on day d, besides their own plans ----
// The ship's events (birthdays, observatory night, quiz night and the rest) are section 18's (the events engineer):
// its eventPlan(p, d) gives [{ id, from, to, opts, tag, anim, min }] in minutes from midnight, already filtered to
// who goes. Section 14 keeps the Deck 1 routines (answer 24). leisureUntil stops a free-time block at a gathering's
// `at` and takes its place, as it does for the Wednesday drill; anyone at the gym or gone to bed misses it.
// birthdaysOn(d) is a helper for section 18: ROSTER[i].birthday is a ship day of the year, 1-364.
const BDAY_CACHE = new Map();
function birthdaysOn(d) {                                // everyone (not the player) whose birthday is ship day d
  if (!BDAY_CACHE.has(d)) BDAY_CACHE.set(d, schedPeople().filter(p => isBirthday(p, (d - 1) * 1440)));
  return BDAY_CACHE.get(d);
}
// a meal tradition (the Sunday long table, the harvest supper...) goes through the servery line like any meal, a tray
// and all (the user, after 0.60.4): each diner sets off between TRAD_LINE[1] and [0] minutes before its table time, so
// the line opens about half an hour early and the table fills as they're served (two served at once, LINE_COUNTER)
const TRAD_LINE = [8, 30];
function gatherings(p, d, F) {
  const U = k => schedU(p.seed, d, k), out = [];
  if (typeof eventPlan === 'function') for (const e of eventPlan(p, d) || []) {   // a host (host: true) is there 5 minutes early
    const early = e.host ? 5 : 0;
    const q = e.meal ? TRAD_LINE[0] + Math.round((TRAD_LINE[1] - TRAD_LINE[0]) * U(530)) : 0;   // a meal tradition: through the line first, set off q minutes early (0.26.41)
    out.push({ at: e.from - early - q, dur: e.to - e.from + early + q, where: e.opts, tag: e.tag, anim: e.anim, min: e.min || 20, host: !!e.host, meal: e.meal || null, act: e.meal || undefined, q: e.meal ? q : 0 });   // a meal tradition (meal: 'dinner' | 'breakfast') is that meal
  }
  // social B2's farewell friends (20c's farewellCrew(leaver, d) -> ids, pure per day): on a crew member's last day, each
  // of their friends who is free stands with them in the shuttle bay while they wait to board, 14:30-15:00 (0.26.38)
  if (!p.guest && typeof farewellCrew === 'function') {
    const S = schedData(), bye = S.people.filter(q => q !== p && !q.guest && crewLeaving(q) === d && aboard(q, d));
    if (bye.some(q => { try { return (farewellCrew(q, d) || []).includes(p.id); } catch (e) { return false; } }) || (typeof careerSendOff === 'function' && careerSendOff(d).includes(p.id)))   // or your own send-off, let go (0.61.0)
      out.push({ at: ROTA_OFF - ROTA_WAIT, dur: ROTA_WAIT, where: [[5, '@gather-shuttle-bay']], tag: 'farewell', anim: 'talk', min: 20 });
  }
  if (F.night && F.works) return out;                    // on the night shift tonight: the ship's events still (eventFree keeps them clear of the shift), not Deck 1's routines (0.26.31)
  // answer 24, Deck 1: the evening handover at the command ring (places with `event: 'handover'`) at 18:00, for the
  // Captain and the Commander on their work days and any bridge crew who work late; and the Captain's evening walk
  // through the observation room (places with `event: 'walk'`, visited in id order), most evenings
  if (F.works && !F.night && (p.rank === 'captain' || p.rank === 'xo' || (p.work && p.work.deck === 1 && habitsOn(p, d).includes('workaholic'))))
    out.push({ at: 1075, dur: 15, where: [[1, '@handover']], tag: 'handover', act: 'work' });
  if (p.rank === 'captain' && !(F.night && F.works) && U(514) < .75) out.push({ at: 1170 + Math.round(30 * U(515)), dur: 4, where: [[1, '@walk']], tag: 'stroll', walk: true });
  return out;
}
// ---- ship-wide events' routines (Pillar 3, C7): section 18's SHIP_EVENTS[id].routines and needs ----
// evDay(d): the day in 10-minute slots (an event's phases start on the 10 minutes), each null or { rules, sleep, social,
// startDay }: rules is section 18's eventRoutines(t), the whole list in force (eventMod('routine', key) finds only
// the first match), sleep and social the needs' multipliers (eventMod('needs', ...)). Read through eventNow, which is pure for any minute, so a day planned ahead or again agrees with play.
// Cached per day; shipDay clears the cache and the plans when the running event or the log of past ones changes.
// The rules: doubleShift (schedFrame: the day shift works on to 20:30 with dinner at the station, the night shift to
// 07:15, so the bridge is never empty and the two never meet at a shared desk), patrol (the Watch walks the decks in turn), closed (take() passes those places by), stayIn (that
// share of free time in their own quarters), rush (a call owed: a booth at the first chance in `at`). Inert with no event.
const EV_DAY = new Map(); let EV_SIG = '';
// evSig's parts, compared without building its string (shipDay asks on every whereIs: the garbage count, 0.26.40)
const EV_K = [null, null, -1, null];
function evChanged() {
  const e = SHIP.event, a = e ? e.id : '', b = e ? e.startDay : '', c = SHIP.eventLog ? SHIP.eventLog.length : 0, i = typeof introSig === 'function' ? introSig() : '';
  if (a === EV_K[0] && b === EV_K[1] && c === EV_K[2] && i === EV_K[3]) return false;
  EV_K[0] = a; EV_K[1] = b; EV_K[2] = c; EV_K[3] = i; return true;
}
const evSig = () => (SHIP.event ? SHIP.event.id + '@' + SHIP.event.startDay : '') + '/' + (SHIP.eventLog ? SHIP.eventLog.length : 0)
  + (typeof introSig === 'function' ? '/' + introSig() : '');   // section 21: the intro's state (on, skipped, ended) changes who's busy
function evDay(d) {
  if (EV_DAY.has(d)) return EV_DAY.get(d);
  let out = null;
  try {                                                  // before section 18 has run: nothing, and nothing kept
    if (typeof eventNow !== 'function' || typeof EV_READY === 'undefined') return null;
    for (let i = 0; i < 144; i++) {
      const t = (d - 1) * 1440 + i * 10, now = eventNow(t); if (!now) continue;
      const rules = typeof eventRoutines === 'function' && eventRoutines(t).length ? eventRoutines(t) : null;
      const sleep = eventMod('needs', 'sleep', t), social = eventMod('needs', 'social', t);
      if (rules || sleep || social) (out || (out = new Array(144).fill(null)))[i] = { rules: rules || [], sleep: sleep || 1, social: social || 1, startDay: d - now.day };
    }
  } catch (e) { return null; }
  EV_DAY.set(d, out);
  if (EV_DAY.size > 40) EV_DAY.delete(EV_DAY.keys().next().value);
  return out;
}
const evAt = abs => { const d = Math.floor(abs / 1440) + 1, sl = evDay(d); return sl ? sl[Math.max(0, Math.min(143, Math.floor((abs - (d - 1) * 1440) / 10)))] : null; };
const evWho = (who, p) => !who || who === 'all' || who === 'dept:' + p.dept;
const evRule = (abs, rule, p) => { const e = evAt(abs); return e && e.rules.find(r => r.rule === rule && (!p || evWho(r.who, p))) || null; };
// a place closed at ship minute abs: where 'type:<type>' or '<deck>|<room key>'
const evClosed = (pl, abs) => { const e = evAt(abs); return !!e && e.rules.some(r => r.rule === 'closed' && (r.where === 'type:' + pl.type || r.where === pl.deck + '|' + pl.room)); };
// owed a call when comms come back: section 18's callOwed (the calls-home crew and about a third of the rest)
const evOwed = (p, e, d) => p.rank !== 'guest' && (typeof callOwed === 'function' ? callOwed(p, e.startDay) : habitsOn(p, d).includes('calls-home') || schedU(p.seed, e.startDay, 601) < .33);
function schedFrame(p, d) {
  const U = k => schedU(p.seed, d, k), H = new Set(habitsOn(p, d)), shape = WEEK_SHAPE[weekday(d)];
  const gp = shiftBlocks(p, d), works = galleyRotaOn() && p.dept === 'galley' && p.shift !== 'night' ? !!(gp && gp.blocks) : isWorkDay(p, d);   // the rota decides galley days off
  const jit = k => (U(k) < .5 ? -1 : 1) * (5 + 20 * U(k + 1));              // 5-25 minutes either way
  const wa = H.has('workaholic');
  const gt = guestTpl(p);                                                   // a guest keeps their template's hours
  let bed = (gt ? gt.bed : 1365) + jit(3) + (shape.late || 0);              // about 22:45
  if (H.has('early-to-bed')) bed -= 30 + 30 * U(5);
  if (H.has('night-owl')) bed += 30 + 30 * U(5);
  const next = shiftBlocks(p, d + 1);                      // an early galley start tomorrow means an early night
  if (gp && gp.bedBy != null) bed = Math.min(bed, gp.bedBy);
  if (next && next.blocks) bed = Math.min(bed, (next.wake != null ? next.wake : next.blocks[0][0] - 35) - 410 + 1440);
  bed = Math.round(Math.min(1430, bed));
  const f = { U, H, shape, works, bed, night: p.shift === 'night' };
  if (f.night) { f.workStart = 1260 - (wa ? Math.round(15 + 15 * U(7)) : 0); f.workEnd = 360 + (wa ? Math.round(15 + 15 * U(8)) : 0); }
  else { f.workStart = SHIFTS.day[0] - (shape.early || 0) - (wa ? Math.round(15 + 15 * U(7)) : 0); f.workEnd = SHIFTS.day[1] + (wa ? Math.round(5 + 10 * U(8)) : 0); }   // workaholics stay on to 17:05-17:15 (was to 17:30; the user's 'make the crew finish work on time', 0.71.1)
  if (works && p.work && evRule(f.night ? d * 1440 + 360 : (d - 1) * 1440 + f.workEnd, 'doubleShift', p)) {   // a ship-wide event's double shift (C7)
    f.double = true; f.workEnd = f.night ? Math.max(f.workEnd, 435) : Math.max(f.workEnd, Math.min(1230, bed - 45));   // the gaps closed, never past the other shift's start (desks are shared)
  }
  let wake = gt ? gt.wake - 45 - 45 * U(13) + jit(10) : 330 + Math.round(105 * U(10));   // 05:30-07:15 (the user's playtest 2, 0.71.5: earlier and varied, spread evenly so the washrooms aren't all at once; was 05:15-06:15 in 0.71.3; a guest's lie-in is in their template)
  if (!gt && p.rota && (p.rota.team === 'bar' || p.rota.relief === 'bar')) wake += 45;   // the bar runs to 23:00: its staff keep their old lie-in (0.71.3; else under 6 hours' sleep)
  if (H.has('early-riser')) wake -= 30 + 15 * U(12);
  if (H.has('late-sleeper')) wake += 15 + 15 * U(12);
  if (!works) wake += 45 + 45 * U(13) + (shape.lieIn || 0);
  if (works && !f.night) wake = Math.min(wake, f.workStart - 45);
  const rh = REC_ON && !f.night ? recHostEarly(p, d, works && f.workStart) : null; if (rh != null) wake = Math.min(wake, rh);   // a rec tradition's host is up for it (Rina's Dawn swim; RA, 0.83)
  f.wake = Math.round(wake);
  return f;
}
// The day's choices are steered by the person's needs at the start of the day. To stay deterministic and quick,
// that estimate is read from what their habits alone would have had them do on the days before (the "base"
// choices, which don't depend on needs), never from the needs-steered plans themselves: so planning any day
// looks back a fixed few days, not all the way to day 1.
const GYM_BASE = (p, dd) => habitsOn(p, dd).includes('gym-regular') ? (isWorkDay(p, dd) ? .8 : .6) : .12;
const CALL_BASE = (p, dd) => habitsOn(p, dd).includes('calls-home') ? (isWorkDay(p, dd) ? .3 : .9) : .06;
const SHOP_BASE = (p, dd) => habitsOn(p, dd).includes('shopper') ? (isWorkDay(p, dd) ? .35 : .8) : isWorkDay(p, dd) ? .1 : .45;
function needsEst(p, d) {
  const since = (k, base) => { for (let i = 1; i <= 7; i++) if (schedU(p.seed, d - i, k) < base(p, d - i)) return i; return 8; };
  const F = schedFrame(p, d), P = schedFrame(p, d - 1);
  const slept = F.night ? 450 : F.wake + 1440 - P.bed;
  const cl = v => Math.max(0, Math.min(100, Math.round(v)));
  return { hunger: 60, energy: cl(slept / 480 * 100), hygiene: 70, fitness: cl(105 - 9 * since(60, GYM_BASE)), social: cl(100 - 9 * since(62, CALL_BASE) - (p.rank === 'guest' ? 20 : 0)) };
}
// choices weighted by need: a habit's pull on a day, raised when it hasn't happened for a few days
function schedWants(p, d, k, base) {
  const did = dd => schedU(p.seed, dd, k) < base(dd);
  return did(d) || (base(d) > .2 && !did(d - 1) && !did(d - 2) && !did(d - 3));
}

// ---- the rec deck's crew (RA, 0.83.x; plans/recdeck-plan.html v5 section 9; brief-recdeck "RA") ----
// Only with REC_DECK on (DECKS[7].playerOnly lifted); with it off nothing here runs and every plan is as before.
// Habits: about a third of the crew (and the story crew who host a rec tradition) have one of REC_HABITS, layered over
// section 9's in habitsOn (recHabit: schedU key 1030, the person's seed, so the same people every game; never a guest).
// A visit (schedBuild's recVisit) only ever takes the place of time they'd have spent resting in their own bunk or
// cabin (a leisure block whose pick was 'rest'), starting and ending exactly when that rest would, so nobody's day off
// the rec deck moves and the Commons keep every visitor they had (the user's "Commons needs to be busy"). A visit: the
// ride down, for the pool and kayaks a locker (rec kit, 2 minutes), a turn of 20-40 minutes at a free place of the kind
// (REC_DO), waiting up to REC_Q minutes at its waiting spots first, else something else or back to rest; a shower and
// the locker after the wet ones; the ride up. Open 06:00 to midnight (DECKS[7].open). At most REC_CAP on the deck (the
// plans' count, occ.rec): 15 on evenings (17:00 on) and weekends, 6 on weekday daytimes; gatherings are exempt.
// Keys: 1030 (who has a habit, and which), 1031-1034 (a visit: go or not, what, how long, which place first)
const REC_ON = REC_DECK;
const REC_HABITS = { swimmer: 'swim', kayaker: 'kayak', climber: 'climb', 'disc-player': 'disc', floater: 'float', 'film-buff': 'watch' };
const REC_HABIT_TEXT = {
  swimmer: 'Swims lengths in the rec dec pool, mornings or evenings.', kayaker: 'Paddles the rec dec rivers after shift.',
  climber: 'Climbs the rec dec wall and rings the bell.', 'disc-player': 'A Lightdisc pick-up game on the rec dec after shift.',
  floater: 'Unwinds in the rec dec float room.', 'film-buff': 'Never misses film night; watches from the stands in between.',
};
// the story crew who host the rec traditions keep theirs; Maeve Volkov's is her round of the deck's machines (round 2)
const REC_HABIT_FIX = { rina: 'swimmer', holt: 'kayaker', tomas: 'climber', vance: 'climber', pell: 'disc-player', oduya: 'floater', nandakumar: 'floater' };
// a habit by what the person already likes: gym-regulars and runners to the pool, wall and rivers; musicians and the
// common room to the films; the rest to anything. [habit, weight]
const REC_LIKES = [[h => h.includes('gym-regular') || h.includes('runner'), [['swimmer', 3], ['climber', 3], ['kayaker', 2], ['disc-player', 2]]],
  [h => h.includes('music') || h.includes('musician') || h.includes('common-room'), [['film-buff', 3], ['disc-player', 1], ['floater', 1]]],
  [() => true, [['swimmer', 2], ['kayaker', 1.5], ['climber', 1.5], ['disc-player', 2], ['floater', 1.5], ['film-buff', 1]]]];
const REC_SHARE = .3;                                    // with the fixed ones, about a third of the crew
function recHabit(p) {
  if (!REC_ON || !p || p.guest || p.rank === 'guest' || p.player) return null;
  if (REC_HABIT_FIX[p.id]) return REC_HABIT_FIX[p.id];
  if (schedU(p.seed, 0, 1030) >= REC_SHARE) return null;
  const opts = REC_LIKES.find(([f]) => f(p.habits || []))[1], tot = opts.reduce((a, o) => a + o[1], 0);
  let r = schedU(p.seed, 1, 1030) * tot; for (const [h, w] of opts) if ((r -= w) < 0) return h;
  return opts[opts.length - 1][0];
}
// what a visit does: the place type, its waiting spots' type, the anim (the place's own when null), wet: rec kit first
const REC_DO = {
  swim: { type: 'rec:lane', q: 'rec:poolq', wet: true }, kayak: { type: 'rec:kayak', q: 'rec:kayakq', wet: true },
  climb: { type: 'rec:climb', q: 'rec:climbq' }, float: { type: 'rec:float', q: 'rec:floatq' },
  disc: { type: 'rec:disc', q: 'rec-courtq' }, watch: { type: 'rec-stand' }, bean: { type: 'lounge-seat' },
};
// the host of an early rec tradition (Dawn swim, Slow stretch) wakes in time for it: the latest wake that lets them go, or null
function recHostEarly(p, d, shiftAt) {                  // shiftAt: their shift's start today (false on a day off): no use waking for one that clashes
  if (typeof EV_READY === 'undefined' || !EV_READY || !REC_TRAD_ON) return null;   // section 18 not run yet (EV_READY is a var: safe to ask before)
  for (const ev of REC_TRADS) if (ev.host === p.id && ev.at[0] < 600 && !(shiftAt && ev.at[1] > shiftAt - 15) && evDue(ev.when, d)) return ev.at[0] - (ev.wake != null ? ev.wake : 60) - 25;   // time for the toilet and a wash first
  return null;
}
const REC_ROUND = { who: 'volkov-maeve', at: [600, 690], stops: 5, mins: 6 };   // her round: from 10:00-11:30, five machines, six minutes each
const REC_CAP = { busy: 15, quiet: 6 }, REC_Q = 10, REC_TURN = [20, 40];
const recCap = (d, m) => weekday(d) >= 5 || m >= 1020 || m < 540 ? REC_CAP.busy : REC_CAP.quiet;   // weekday daytime (09:00-17:00) is quiet
// a visit's odds from a rest block: with a habit, most of them; without, now and then the stands, a beanbag or the float room
const REC_ODDS = { habit: .9, habitOff: .9, casual: .35, away: .6 };   // away: the share of those for a pick on another deck than the Commons (Deck 4's rooms, the officers' lounges)

// ---- seating by friendship: section 20's affinityPlan (pure, memoised); nothing changes without it ----
const SEAT_SOCIAL = new Set(['mess-seat', 'lounge-seat', 'bench']);
// a person's friends (affinity 30+) and those they don't get on with (-30 or less) on day d, aboard or not; guests have
// none. section 20's affinityPlan(a, b, d) reads its weekly snapshot (fixed and saved a week ahead), so a day planned
// early or again gets the same answer; cached per person and day
function seatMates(p, S, d) {
  if (typeof affinityPlan !== 'function' || p.guest) return null;
  const c = S.mates || (S.mates = new Map()), key = p.id + '|' + d; if (c.has(key)) return c.get(key);
  if (c.size > 6000) c.clear();
  const m = { fr: [], foe: [] };
  try { for (const q of S.people) if (q !== p && !q.guest) { const a = affinityPlan(p, q, d); if (a >= 30) m.fr.push(q.id); else if (a <= -30) m.foe.push(q.id); } }
  catch (e) { return null; }                             // section 20 not loaded yet: seat as before
  c.set(key, m); return m;
}
// the seats (mess, lounge, bench) within 2 tiles of a place, on its deck
function seatNear(S, id) {
  const c = S.seatNear || (S.seatNear = new Map()); if (c.has(id)) return c.get(id);
  const pl = S.byId.get(id), xy = q => q.xy || [q.at[0] + .5, q.at[1] + .5], out = [];
  if (pl) { const [x, z] = xy(pl); for (const t of SEAT_SOCIAL) for (const q of S.shared.get(pl.deck + '|' + t) || []) { const [qx, qz] = xy(q); if (Math.hypot(qx - x, qz - z) <= 2) out.push(q.id); } }
  c.set(id, out); return out;
}
// ---- one person's day, taking places from `occ` (placeId -> [[from, to], ...] in absolute minutes) ----
function schedBuild(p, d, occ, S) {
  const F = schedFrame(p, d), P = schedFrame(p, d - 1), U = F.U, H = F.H, B = (d - 1) * 1440, C = SCHED_COMMUTE;
  const rot = occ.rot && occ.rot.get(p.id);                // a day standing in at another station (shipDay's rotation)
  const bedDeck = deckOf(p.bed), desk = rot ? rot.id : S.desks.get(p.id) || null, wd = rot ? rot.deck : p.work && p.work.deck;
  const wtype = rot ? rot.type : p.work && p.work.place, deskAnim = placeAnim(desk && S.byId.get(desk));
  const N = needsEst(p, d);                               // the needs that steer today's choices
  const EVD = evDay(d), shut = EVD && EVD.some(e => e && e.rules.some(r => r.rule === 'closed'));   // a ship-wide event today (C7)
  const segs = []; let t = 0, deck = bedDeck;
  const deck3Full = (a, b) => { const h = occ.heads; for (let m = Math.max(a, 1020); m < Math.min(b, 1440); m++) if (h[m] >= DECK3_EVENING_MAX) return true; return false; };
  // free from a to b (minutes from midnight). An event's own places are held for it from 5 minutes before it starts
  // until it ends (occ.res, shipDay): only someone taking the place for that event (`tag` 'ev-<id>' or 'ev-<id>-<anim>') may
  // use them then, so ordinary free time doesn't fill the room before the guests are planned
  const isFree = (id, a, b, tag) => !(occ.get(id) || []).some(([x, y]) => x < B + b && B + a < y)
    && !(occ.res && (occ.res.get(id) || []).some(([x, y, ev]) => x < B + b && B + a < y && !(tag && (tag === 'ev-' + ev || tag.startsWith('ev-' + ev + '-')))));
  const hold = (id, a, b) => {                           // [from, to, who]; occ.who: who -> [[from, to, placeId]] (seating by friendship)
    if (!occ.has(id)) occ.set(id, []); occ.get(id).push([B + a, B + b, p.id]);
    if (occ.who) (occ.who.get(p.id) || occ.who.set(p.id, []).get(p.id)).push([B + a, B + b, id]);
  };
  // seating by friendship (Pillar 3, with section 20's affinityPlan, pure): at a mess table, a lounge or a bench, a
  // seat within 2 tiles of a friend already planned there (affinity 30+) comes first, and one next to someone they
  // don't get on with (-30 or less) last. Without affinityPlan, or with nobody either way, seats are chosen as before
  const mates = SEAT_SOCIAL && occ.who && seatMates(p, S, d);
  const seg = (act, to, type, placeId, extra) => { if (to > t) segs.push({ from: t, to, act, deck, type, placeId, ...extra }); t = Math.max(t, to); };
  const go = dk => {
    if (dk === deck) return;
    const l = segs[segs.length - 1];                      // a minute waiting by the lift, from the end of what you were doing
    if (l && l.to === t && l.to - l.from > 6 && ['leisure', 'breakfast', 'dinner', 'gym', 'callhome', 'off'].includes(l.act) && !STOPS.has(l.tag)) {
      const lw = (S.shared.get(deck + '|lift-wait') || []).find(pl => isFree(pl.id, t - 1, t));
      if (lw) { l.to = t - 1; hold(lw.id, t - 1, t); segs.push({ from: t - 1, to: t, act: 'off', deck, type: 'lift-wait', placeId: lw.id, tag: 'lift' }); }
    }
    const from = deck; deck = dk; seg('commute', t + C, 'lift', null, { fromDeck: from });
  };
  // stay a little longer where you are (a free place stays held; a busy one, or none, becomes standing about)
  const linger = to => {
    if (to <= t) return;
    const l = segs[segs.length - 1];
    const solo = id => id === p.bed || (S.owner.get(id) || []).length === 1;   // yours alone: nobody else can want it
    const deskTwin = (id, a, b) => S.people.some(q => q !== p && S.desks.get(q.id) === id && aboard(q, d) && ((shiftBlocks(q, d) || {}).blocks || []).some(([x, y]) => x < b && a < y));   // the desk's other shift is on then
    if (l && l.act !== 'commute' && l.act !== 'wash' && !(l.act === 'work' && l.placeId && deskTwin(l.placeId, t, to)) && !STOPS.has(l.tag) && l.to === t && l.deck === deck && (!l.placeId || solo(l.placeId) || isFree(l.placeId, t, to))) {   // not past the shift's end at a desk the next shift shares
      if (l.placeId && !solo(l.placeId)) hold(l.placeId, t, to);
      l.to = to; t = to;
    } else if (deck === bedDeck) seg('off', to, 'bed', p.bed); else seg('off', to, null, null);
  };
  // take a free place of one of `opts` ([deck, type] pairs, best first) for `dur` minutes, waiting up to `wait`
  // (a gathering's crowd spots, `gather` places from the deck architect, fill in their order: nearest the focus first)
  // where you are first; `by` caps the end, `min` is the shortest stay worth having. Returns the place or null.
  const take = (act, opts, dur, o = {}) => {
    for (const [dk, type] of opts) {
      if (dk === 3 && act === 'leisure' && !o.event && DECK3_EVENING_MAX < Infinity && deck3Full(t + (deck !== 3 ? C : 0), o.by !== undefined ? o.by : t + dur)) continue;
      const ownL = (S.own.get(p.bed) || []).filter(pl => pl.type === type && pl.deck === dk);
      let pool = ownL.length ? ownL : (S.shared.get(dk + '|' + type) || []);
      if (!pool.length) continue;
      const soc = mates && SEAT_SOCIAL.has(type) && (mates.fr.length || mates.foe.length);
      const fav = pool[0].gather ? 0 : Math.floor(pool.length * (U(40 + type.length) < .7 ? schedU(p.seed, 0, 41 + type.length) : U(42 + type.length)));
      const arrive = t + (dk !== deck ? C : 0), wait = o.wait || 0;
      if (pool[0].gather && p.partner && occ.who) {      // couples stand together in a crowd: the spots nearest your partner's first, if they're already there (0.26.38)
        const ids = new Set(pool.map(q => q.id)), at = (occ.who.get(p.partner) || []).find(([x, y, id]) => ids.has(id) && x < B + arrive + dur && B + arrive < y), q0 = at && S.byId.get(at[2]);
        if (q0) { const xy = q => q.xy || [q.at[0] + .5, q.at[1] + .5], [x0, z0] = xy(q0), dist = q => Math.hypot(xy(q)[0] - x0, xy(q)[1] - z0); pool = pool.slice().sort((a, b) => dist(a) - dist(b)); }
      }
      for (let s = arrive; s <= arrive + wait; s++) {
        let end = s + dur; if (o.by !== undefined) end = Math.min(end, o.by);
        if (end - s < (o.min || Math.min(dur, 10))) break;
        let pref = null, avoid = null;
        if (soc) {                                       // the seats beside friends (pref) and beside people to avoid, now
          const near = (ids, set) => { for (const q of ids) for (const [x, y, pid] of occ.who.get(q) || []) if (x < B + end && B + s < y) for (const n of seatNear(S, pid)) set.add(n); return set; };
          pref = near(mates.fr, new Set()); avoid = near(mates.foe, new Set());
          if (!pref.size && !avoid.size) pref = avoid = null;
        }
        for (let j = 0; j < (pref ? 3 * pool.length : pool.length); j++) {
          const i = j % pool.length, pass = Math.floor(j / pool.length);
          const pl = pool[(fav + i) % pool.length], mine = ownL.length > 0 && S.owner.get(pl.id).length === 1;
          if (pref && (pass === 0 ? !pref.has(pl.id) || avoid.has(pl.id) : pass === 1 ? pref.has(pl.id) || avoid.has(pl.id) : !avoid.has(pl.id))) continue;
          if (!mine && !isFree(pl.id, s, end, o.tag)) continue;
          if (shut && evClosed(pl, B + s)) continue;          // closed for the event
          if (act === 'leisure' && type.startsWith('work:') && (S.deskOf(pl.id) || (occ.rotIds && occ.rotIds.has(pl.id)))) continue;   // a guest at a work type: never someone's desk, nor today's stand-in's
          if (o.queue && s - arrive >= SHOWER_Q) { go(dk); seg('off', s, 'booth-queue', null, { tag: o.queue }); }   // a wait worth queueing for: in the line by the place (0.71.4, the booths)
          else { linger(s - (dk !== deck ? C : 0)); go(dk); }
          if (!mine) hold(pl.id, s, end);
          const an = o.anim || placeAnim(pl), ex = {}; if (o.tag) ex.tag = o.tag; if (an) ex.anim = an;
          seg(act, end, pl.type, pl.id, ex);
          return pl.id;
        }
      }
    }
    return null;
  };
  const desk1 = to => seg('work', to, wtype, desk, deskAnim ? { anim: deskAnim } : undefined);
  // a ship-wide event's patrol (C7): spells at their own station, between them a quarter of an hour at another deck's
  // lift lobby or a bench, the decks in turn. The rides count as the shift (tag 'patrol')
  const patrolTag = () => { const l = segs[segs.length - 1]; if (l && l.act === 'commute') l.tag = 'patrol'; };
  const patrol = to => {
    const ring = [3, 4, 5, 1, 6, 2], k0 = Math.floor(6 * U(119));
    for (let n = 0; t < to; n++) {
      desk1(Math.min(to, t + 30 + Math.round(20 * U(120 + n % 20))));
      if (to - t < 2 * C + 25) { desk1(to); break; }
      const dk = ring[(k0 + n) % 6]; if (dk === wd) continue;
      go(dk); patrolTag();
      if (!take('work', [[dk, 'lift-wait'], [dk, 'bench']], 15, { tag: 'patrol', min: 5, by: to - C })) seg('work', t + 10, null, null, { tag: 'patrol' });
      go(wd); patrolTag();
    }
  };
  const work = to => (EVD && to > t && evRule(B + t, 'patrol', p) ? patrol(to) : desk1(to));
  const workAt = (pid, task, to) => {                    // a galley stint: its own station and task
    const pl = pid && S.byId.get(pid);                   // tea on the stool takes the stool's own pose; the dish pit is 'wash'
    const an = pl && pl.anim || (task === 'tea' ? null : task === 'wash' ? 'wash' : placeAnim(pl) || (p.dept === 'galley' ? 'cook' : null)), ex = {};
    if (an) ex.anim = an; if (task) ex.tag = task;
    seg('work', to, pl ? pl.type : wtype, pid, ex);
  };
  const toilet = k => {                                  // a toilet on the deck you're on, then hands at a basin; nothing if they're busy
    if (!take('wash', [[deck, 'toilet']], 3 + Math.round(3 * U(k)), { wait: 4, tag: 'toilet', min: 2 })) return false;
    take('wash', [[deck, 'basin']], 1, { tag: 'hands', min: 1 });   // no waiting: both busy, skip it
    return true;
  };
  // the shift from now to `to`, with its breaks: tea (the habit, or about one day in three for anyone) on a seat
  // or bench on the work deck, and a toilet break most days. The Works crew on Deck 5 have no random tea: the 13:00
  // tea and biscuits in the tea corner instead (WORKS_TEA, 0.71.1), most of them, a quarter of an hour each, staggered
  const clocks = p.dept === 'works' && wd === 5 && p.shift !== 'night' && (S.shared.get('5|timeclock') || []).length > 0;   // the Works crew clock in and out (the career engineer, 0.61.13)
  const shiftWithBreaks = to => {
    const br = [];
    if (clocks) take('work', [[5, 'timeclock']], 1, { wait: 6, min: 1, tag: 'clock' });   // a short queue at the clock
    const wt = p.dept === 'works' && wd === 5 && p.shift !== 'night';
    if (wt) { if (H.has('tea-break') || U(31) < (H.has('workaholic') ? WORKS_TEA.busy : WORKS_TEA.odds)) br.push([WORKS_TEA.at + WORKS_TEA.step * Math.floor(WORKS_TEA.slots * U(30)), 'wtea']); }
    else if (H.has('tea-break') || U(31) < .35) br.push([600 + Math.round(240 * U(30)), 'tea']);
    if (U(32) < .6) br.push([540 + Math.round(400 * U(33)), 'toilet']);
    if (F.double) br.push([1050 + Math.round(30 * U(36)), 'staff']);   // a double shift (C7): dinner at the station
    if (REC_ON && p.id === REC_ROUND.who && wd === 5) br.push([REC_ROUND.at[0] + Math.round((REC_ROUND.at[1] - REC_ROUND.at[0]) * schedU(p.seed, d, 1039)), 'recRound']);   // Maeve's round of the rec deck's machines (0.83.2, RA)
    const ru = EVD && evRule(B + 600, 'rush'), ra = ru && (ru.at || [600, 1080]);
    if (ru && !called && evOwed(p, evAt(B + 600), d)) br.push([Math.max(ra[0], t + 15) + Math.round((Math.min(ra[1], to) - 60 - Math.max(ra[0], t + 15)) * U(37)), 'call']);
    for (const [bt, kind] of br.sort((a, b) => a[0] - b[0])) {
      if (bt <= t + 10 || bt >= to - 25) continue;
      work(bt);
      if (kind === 'tea') { if (!take('leisure', [[wd, 'lounge-seat'], [wd, 'bench']], 15, { tag: 'tea' })) work(t + 15); }
      else if (kind === 'wtea') { if (!take('leisure', [[5, 'lounge-seat']], WORKS_TEA.dur, { tag: 'tea', wait: WORKS_TEA.wait, min: 8, anim: 'drink' })) work(t + 5); }   // the tea corner full: back to the job
      else if (kind === 'staff') seg('dinner', t + 20, wtype, desk, { tag: 'staff' });
      else if (kind === 'recRound') recRound(to);
      else if (kind === 'call') {                       // to the booths and back on the shift's time (tag 'rush')
        called = true; const n0 = segs.length;
        if (take('callhome', [[3, 'callhome']], 20, { wait: 20, min: 10, tag: 'rush' })) { go(wd); for (let i = n0; i < segs.length; i++) if (segs[i].act === 'commute' || segs[i].tag === 'lift') segs[i].tag = 'rush'; }
        else work(t + 5);
      }
      else toilet(34);
    }
    work(to);
    if (clocks) take('work', [[5, 'timeclock']], 1, { wait: 20, min: 1, tag: 'clock' });   // out as the shift ends: the whole day crew at one clock after 17:00, so a longer queue than the morning's (X3, 0.71.7: with 0.71.5's mornings 6 minutes let only 6 of 11 out; they finish up at their station meanwhile)
  };
  // showers in the evening: the habit, or about one day in three for anyone else
  const eveShower = H.has('evening-shower') || U(90) < .3;
  // the shower queue (0.36.91, plan-0607): a wait of SHOWER_Q+ minutes for a shower is spent in the washroom, not on
  // the bunk: the wait before the shower becomes a 'shower-queue' stop (a free place of that type in the same room
  // when the deck architect has them, else no place: section 10 stands them inside the washroom door, tag 'showerq')
  const showerQueue = (t0, id) => {
    const pl = S.byId.get(id), i = segs.length - 1, w = segs[i], pv = segs[i - 1];
    if (!pl || !w || w.placeId !== id || !pv || pv.to !== w.from || pv.act === 'commute' || w.from - t0 < SHOWER_Q) return;
    const q = (S.shared.get(bedDeck + '|shower-queue') || []).find(x => x.room === pl.room && isFree(x.id, t0, w.from));
    if (pv.from >= t0) segs.splice(i - 1, 1); else pv.to = t0;   // the wait was added on the end of what they were doing
    if (q) hold(q.id, t0, w.from);
    segs.splice(segs.indexOf(w), 0, { from: t0, to: w.from, act: 'wash', deck: bedDeck, type: 'shower-queue', placeId: q ? q.id : null, tag: 'showerq' });
  };
  const wash = (k, evening) => {                         // a shower (queueing if need be), else a basin, else in your own room
    const dur = evening || !eveShower ? 7 + Math.round(5 * U(k)) : 5;
    const type = dur === 5 ? 'basin' : 'shower', t0 = t, d0 = deck, got = take('wash', [[bedDeck, type]], dur, { wait: 25 });
    if (got && type === 'shower' && d0 === bedDeck) showerQueue(t0, got);
    if (!got && !take('wash', [[bedDeck, type === 'shower' ? 'basin' : 'shower']], 5, { wait: 15 })) {
      go(bedDeck); seg('wash', t + 6, 'bed', p.bed, { tag: 'room' });
    }
  };
  const grab = (meal, k) => {                            // grab-and-go: two minutes at the shelf, or the servery
    if (!take(meal, [[3, 'grab-shelf']], 2, { wait: 4, tag: 'grab' }) && !take(meal, [[3, 'servery-queue']], 3, { wait: 6, tag: 'grab' })) { go(3); seg(meal, t + 3, null, null, { tag: 'grab' }); }
  };
  // a sit-down meal: queue at the servery, then a seat; `by` is when it has to end
  const meal = (meal, k, by) => {
    let dur = 22 + Math.round(15 * U(k)); if (H.has('lingers-at-meals')) dur += 15 + Math.round(10 * U(k + 1));
    const l = segs[segs.length - 1], from = deck === 3 && l && l.placeId && S.byId.get(l.placeId), at = from ? from.at : DECKS[3].lift;
    const walk = Math.round(LINE_WALK[0] + (Math.abs(at[0] - LINE_WALK[2][0]) + Math.abs(at[1] - LINE_WALK[2][1])) * LINE_WALK[1]);   // to the line, which section 10 walks, from the lift or where you are on Deck 3
    if (by - (t + (deck !== 3 ? C : 0)) < 15 + walk) return grab(meal, k);   // the walk, the queue stop and 12 minutes sat
    go(3); seg(meal, t + walk, null, null, { tag: 'queue' });   // (0.26.30) the galley still takes the food 2 minutes into the meal's first segment
    take(meal, [[3, 'servery-queue']], 3, { wait: walk ? 0 : 8, tag: 'queue', min: 1 });   // no waiting for it after the walk: a wait would split the meal
    if (!take(meal, [[3, 'mess-seat']], dur, { wait: 5, by, min: 12 }) && !take(meal, [[3, 'lounge-seat'], [3, 'bench']], dur, { wait: 5, by, min: 12 })) {
      go(3); seg(meal, Math.min(by, t + dur), null, null);
    }
  };
  // leisure options for this person, weighted: places on the deck you're on count four times, the one you just
  // left counts for little; [bedDeck, 'rest'] is time in your own bunk or cabin
  let lastLeisure = null, called = false;
  const leisureOpts = k => {
    const junior = p.rank === 'junior', senior = !junior && p.rank !== 'guest', gt = guestTpl(p);
    const tired = (N.energy < 70 ? 2 : 1) * (N.social < 50 ? .5 : 1);   // tired: rest more; lonely: less
    const opts = (gt ? guestOpts(p, t >= 1020 ? gt.evening : gt.first && guestDayNo(p, d) <= gt.first && gt.firstDay || gt.day, bedDeck) : LEISURE)   // a guest: their template's places (Pillar 3)
      .concat(...habitsOn(p, d).map(h => HABIT_LEISURE[h] || []))
      .filter(([dk, type, w, who]) => type === 'rest' || (!who || (who === 'junior' ? junior : who === 'deck2' ? senior || wd === 2 : senior)) && (S.shared.get(dk + '|' + type) || []).length)
      .map(o => o[1] === 'rest' ? [o[0], o[1], o[2] * tired] : o)
      .concat(gt ? [] : [[bedDeck, 'rest', 3 * tired]])
      .map(([dk, type, w]) => [dk, type, w * (dk === deck ? 4 : 1) * (dk + '|' + type === lastLeisure ? .2 : 1)]);
    const tot = opts.reduce((a, o) => a + o[2], 0); let r = U(k) * tot, i = 0;
    while (i < opts.length - 1 && (r -= opts[i][2]) > 0) i++;
    return opts.slice(i).concat(opts.slice(0, i)).map(o => [o[0], o[1]]);   // the pick first, then the rest
  };
  // a visit to the rec deck in place of a rest block that would run to `to` (RA, 0.83.0; see REC_HABITS): true when one
  // is planned (then t is where the ride back up starts). Never past the deck's hours, never over the deck's cap
  let recN = 0;
  const recVisit = (to, odds = 1, ride = null) => {   // ride: { a0, go } when the ride down is already planned (recSwap)
    if (!REC_ON || !occ.rec || p.rank === 'guest' || p.guest) return false;
    const n = recN++, vu = j => schedU(p.seed + 7919 * n, d, 1031 + j), hab = Object.keys(REC_HABITS).find(h => H.has(h));
    let kind = null;
    if (hab && vu(0) < odds * (F.works ? REC_ODDS.habit : REC_ODDS.habitOff)) kind = REC_HABITS[hab];
    else if (vu(0) > 1 - odds * REC_ODDS.casual) kind = ['watch', 'bean', 'float'][Math.floor(vu(1) * 3)];
    if (!kind) return false;
    const sh = typeof recPlanShut === 'function' ? recPlanShut(d, occ) : null;   // rec engineer B's machines (0.84.6): what's shut or off, as the day's plan sees it (RC, 0.64.1)
    if (sh && (kind === 'disc' && sh.court || kind === 'float' && sh.float || kind === 'climb' && !sh.belays || kind === 'swim' && sh.pool && vu(5) < .7 || kind === 'kayak' && sh.river && vu(5) < .5)) return false;
    const R = REC_DO[kind], wet = !!R.wet, pre = wet ? 2 : 0, post = wet ? 6 : 0, dur = REC_TURN[0] + Math.round((REC_TURN[1] - REC_TURN[0]) * vu(2));
    const a0 = ride ? ride.a0 : t + C, open = DECKS[7].open, last = Math.min(to - C - post, open[1] * 60 - 15);
    if (a0 < open[0] * 60 || last - (a0 + pre) < 15) return false;
    const pool = (S.shared.get('7|' + R.type) || []).filter((q, b) => !(kind === 'climb' && sh && ((sh.belayOff || [])[b] || sh.route === b + 1))); if (!pool.length) return false;   // not under a tagged-out belay or a taped route
    const capOk = (a, b) => { for (let m = a; m < b; m++) if (occ.rec[m] + 1 > recCap(d, m)) return false; return true; };
    const free1 = (type, a, b) => (S.shared.get('7|' + type) || []).find(pl => isFree(pl.id, a, b)) || null;
    // the place and the turn: the earliest start within REC_Q minutes; Lightdisc: the bow end (7-disc-1, your baseline) only
    // to join a game already waiting (someone on 7-disc-2 for the same minutes), else the stern end, waiting for someone
    // (reviewer R6's fix, 0.83.2: a lone player had stood on your baseline)
    let pl = null, s0 = 0, e0 = 0;
    if (kind === 'disc') {
      const d2 = pool.find(q => q.id === '7-disc-2'), d1 = pool.find(q => q.id === '7-disc-1');
      for (const [x, y] of (d2 && occ.get(d2.id)) || []) { const a = x - B, b = Math.min(y - B, last); if (a >= a0 && a <= a0 + REC_Q && b - a >= 15 && isFree(d1.id, a, b)) { pl = d1; s0 = a; e0 = b; break; } }
      if (!pl && d2 && isFree(d2.id, a0, Math.min(a0 + dur, last))) { pl = d2; s0 = a0; e0 = Math.min(a0 + dur, last); }
    } else {
      const off = Math.floor(pool.length * vu(3));
      for (let s = a0 + pre; s <= a0 + pre + REC_Q && !pl; s++) {
        const e = Math.min(s + dur, last); if (e - s < 15) break;
        for (let i = 0; i < pool.length; i++) { const q = pool[(off + i) % pool.length]; if (isFree(q.id, s, e)) { pl = q; s0 = s; e0 = e; break; } }
      }
    }
    if (!pl || !capOk(a0 - C, e0 + post)) return false;   // full, or a long wait: they go elsewhere (rest as before). From the ride down: it's counted on the rec deck (RE20, 0.64.1: day 5 had 16 at 22:22)
    if (ride) ride.go(); else if (deck !== bedDeck) go(7); else { deck = 7; seg('commute', t + C, 'lift', null, { fromDeck: bedDeck }); }   // from their bunk: the ride alone (no wait by Deck 4's lift, so nobody else's day moves)
    const stop = (act, until, type, tag, anim) => {      // a short stop at a free place of that type, else standing about
      const q = type && free1(type, t, until); if (q) hold(q.id, t, until);
      seg(act, until, q ? q.type : null, q ? q.id : null, anim ? { tag, anim } : { tag });
    };
    if (wet) stop('wash', t + 2, 'rec:locker', 'rec-change', 'browse');
    if (s0 > t + 1 && R.q) stop('leisure', s0, R.q, 'rec-wait'); else if (s0 > t) linger(s0);
    hold(pl.id, s0, e0); seg('leisure', e0, pl.type, pl.id, { tag: 'rec-' + kind, ...(placeAnim(pl) ? { anim: placeAnim(pl) } : {}) });
    if (wet) { stop('wash', t + 4, 'rec:shower', 'rec-shower', 'wash'); stop('wash', t + 2, 'rec:locker', 'rec-change', 'browse'); }
    // time left before the ride up: stay on, watching from the stands or on a beanbag (under the cap), else head back
    const end = Math.min(to - C, open[1] * 60 - 15);
    if (end - t >= 15 && capOk(t, end)) { const q = free1(vu(4) < .6 ? 'rec-stand' : 'lounge-seat', t, end) || free1('rec-stand', t, end); if (q) { hold(q.id, t, end); seg('leisure', end, q.type, q.id, { tag: 'rec-watch' }); } }
    return true;
  };
  // Maeve Volkov's round (the plan's "Maeve's deck"; RA, 0.83.2): mid-morning on her workdays, down to the rec deck and a look
  // at REC_ROUND.stops of its machines' work places (rec engineer B's '<machine>-svc', in id order from a seeded start, key
  // 1039), a few minutes each (tag 'round'), then back to her own desk; work time all of it. None while those aren't built
  const recRound = to => {
    const svc = ((DECKS[7] && DECKS[7].places) || []).filter(pl => pl.type === 'work:works' && pl.machine).sort((a, b) => a.id.localeCompare(b.id, 'en', { numeric: true }));
    const n = Math.min(REC_ROUND.stops, svc.length), need = 2 * C + n * REC_ROUND.mins; if (!n || to - t < need + 20) return;
    const k0 = Math.floor(schedU(p.seed + 1, d, 1039) * svc.length);
    const n0 = segs.length;                                // the rides down and back are on her shift's time too (tag 'round'; RE20, 0.64.1)
    go(7); for (let i = 0; i < n; i++) { const pl = svc[(k0 + i) % svc.length]; if (isFree(pl.id, t, t + REC_ROUND.mins)) hold(pl.id, t, t + REC_ROUND.mins); seg('work', t + REC_ROUND.mins, pl.type, pl.id, placeAnim(pl) ? { tag: 'round', anim: placeAnim(pl) } : { tag: 'round' }); }
    go(wd); for (let i = n0; i < segs.length; i++) if (segs[i].act === 'commute') segs[i].tag = 'round';
  };
  // a leisure block taken off the Commons (Deck 4's rooms, the officers' lounges): sometimes the rec deck instead. The place
  // stays held for the block and the ride back ends there, so everyone else's day and this person's own afterwards come
  // out exactly as without the rec deck; only the block itself is spent on the rec deck (RA, 0.83.0)
  const recSwap = L => {
    if (!L || L.act !== 'leisure' || !L.placeId || L.deck === 3 || L.deck === 7 || L.to - L.from < 2 * C + 25) return;
    segs.pop(); const pv = segs[segs.length - 1], rode = pv && pv.act === 'commute' && pv.to === L.from && pv.deck === L.deck, t0 = t, d0 = deck;
    t = L.from; const a0 = rode ? L.from : L.from + C;
    const ok = recVisit(L.to, REC_ODDS.away, { a0, go: () => { const f = deck; deck = 7; if (rode) pv.deck = 7; else seg('commute', t + C, 'lift', null, { fromDeck: f }); } });
    if (!ok) { segs.push(L); t = t0; deck = d0; return; }
    const from = deck; deck = L.deck; seg('commute', t + C, 'lift', null, { fromDeck: from });
    if (t < L.to) seg(L.act, L.to, L.type, L.placeId, { ...(L.tag ? { tag: L.tag } : {}), ...(L.anim ? { anim: L.anim } : {}) });
  };
  // leisure until `end`: blocks of 30-100 minutes; the Wednesday drill musters anyone off duty by the lift, and a
  // block stops for a gathering (a birthday, observatory night) when one is due
  const meet = gatherings(p, d, F);
  // nothing else starts across a gathering: the gym, a call home and the other errands wait (or are dropped) when one
  // begins within `span` minutes, and dinner moves before or after it (Pillar 4: a host always gets to their own event)
  const clear = span => !meet.some(e => !e.done && e.at < t + span && e.at + e.dur > t);
  // a meal tradition's meal (0.26.41): the walk to the servery line and its queue stop, as meal() plans them, then the
  // tradition's seat (tag ev-<id>) for the rest of it, so section 10 hands a tray at the counter as at any meal
  const tradMeal = (e, end) => {
    const l = segs[segs.length - 1], from = deck === 3 && l && l.placeId && S.byId.get(l.placeId), at = from ? from.at : DECKS[3].lift;
    const walk = Math.round(LINE_WALK[0] + (Math.abs(at[0] - LINE_WALK[2][0]) + Math.abs(at[1] - LINE_WALK[2][1])) * LINE_WALK[1]);
    go(3); seg(e.meal, t + walk, null, null, { tag: 'queue' });
    take(e.meal, [[3, 'servery-queue']], 3, { wait: 0, tag: 'queue', min: 1 });
    if (!take(e.act, e.where, e.at + e.dur - t, { wait: 5, by: end, min: e.min || 15, tag: e.tag, anim: e.anim, event: true })) seg(e.meal, Math.min(end, t + 20), null, null);   // no seat at it: eat where they stand (the galley's counted them)
  };
  const leisureUntil = (end, k) => {
    for (let n = 0; end - t >= 20 && n < 12; n++) {
      for (const e of meet) if (!e.done && e.meal && t > e.at && t < e.at + e.dur - (e.min || 20) && end - t >= (e.min || 20)) {   // late for a meal tradition (the handover ran on): join it while there's time to eat
        e.done = true; tradMeal(e, end);                 // through the line too (reviewer 1d, 0.26.42)
      }
      if (REC_ON) for (const e of meet) if (!e.done && /^ev-rec-/.test(e.tag || '') && t >= e.at && t < e.at + (e.host ? Math.max(10, e.dur / 2) : 10) && end - t >= Math.min(25, e.dur)) {   // a rec tradition due right now goes first (0.83.1, RA: one starting the minute a block ended was missed)
        e.done = true; take(e.act || 'leisure', e.where, e.dur, { wait: 5, by: end, min: e.min || (e.dur < 20 ? 5 : 15), tag: e.tag, anim: e.anim, event: true });
      }
      if (end - t < 20) break;
      let to = Math.min(end, t + 30 + Math.round(70 * U(k + n * 3)));
      if (end - to < 20) to = end;
      if (F.shape.drill && t < F.shape.drill && to > F.shape.drill) to = F.shape.drill;
      for (const e of meet) if (!e.done && t < e.at && to > e.at) to = e.at;
      if (U(k + n * 3 + 2) < .12) toilet(k + n * 3 + 2);
      const opts = leisureOpts(k + n * 3 + 1), pick = opts[0];
      lastLeisure = pick[0] + '|' + pick[1];
      let rang = false;                                  // a ship-wide event (C7): a call owed when comms come back, or staying in
      if (EVD) {
        const ru = evRule(B + t, 'rush'), ra = ru && (ru.at || [600, 1080]);
        if (ru && !called && t >= ra[0] && t < ra[1] - 20 && evOwed(p, evAt(B + t), d)) { called = true; rang = !!take('callhome', [[3, 'callhome']], 20 + Math.round(15 * U(63)), { wait: 30, min: 12, by: to, tag: 'rush', queue: 'boothq' }); }
      }
      const si = !rang && EVD && evRule(B + t, 'stayIn', p);
      const n0 = segs.length;
      if (!rang && ((si && schedU(p.seed, d, 700 + k + n) < si.share) || pick[1] === 'rest' || !take('leisure', opts.filter(o => o[1] !== 'rest'), 1440, { by: to, min: 15 }))) {
        if (deck !== bedDeck && to - t < C + 15) linger(to); else { if (pick[1] === 'rest' && !si) recVisit(to); go(bedDeck); seg('leisure', Math.max(t, to), 'bed', p.bed, { tag: 'rest' }); }   // rest, or the rec deck in its place (RA, 0.83.0)
      } else if (REC_ON && !rang && !si && segs.length > n0) recSwap(segs[segs.length - 1]);
      if (F.shape.drill && t === F.shape.drill) { if (!take('off', [[deck, 'lift-wait']], 15, { tag: 'drill' })) seg('off', t + 15, null, null, { tag: 'drill' }); }
      for (const e of meet) if (!e.done && t >= e.at && t < e.at + (e.host ? Math.max(10, e.dur / 2) : 10) && end - t >= Math.min(25, e.dur)) {
        e.done = true;
        if (e.walk) { for (const pl of S.shared.get(e.where[0].join('|')) || []) if (isFree(pl.id, t + (deck !== pl.deck ? C : 0), t + (deck !== pl.deck ? C : 0) + e.dur) && end - t > e.dur + C) { go(pl.deck); hold(pl.id, t, t + e.dur); seg('leisure', t + e.dur, pl.type, pl.id, { tag: e.tag }); } }
        else if (e.meal && e.q) tradMeal(e, end);       // a meal tradition: the line first (0.26.41), then its table with the tray
        else take(e.act || 'leisure', e.where, e.dur, { wait: 5, by: end, min: e.min || (e.dur < 20 ? 5 : 15), tag: e.tag, anim: e.anim, event: true });
      }
    }
    linger(end);
  };
  const specials = (k, offDay) => {                      // needs: the gym, a call home, the weekly wash
    const out = [];
    if (p.template === 'survivor') return out;            // a rescued guest rests: no gym, no shopping
    // the gym is likelier the lower fitness is, a call home the lonelier someone is
    const gym = () => take('gym', [[3, 'gym']], 40 + Math.round(20 * U(61)), { wait: 15, min: 25 });
    if (schedU(p.seed, d, 60) < GYM_BASE(p, d) + (100 - N.fitness) / 100 * .9) out.push(gym);
    if (schedU(p.seed, d, 62) < CALL_BASE(p, d) + (100 - N.social) / 100 * .6) out.push(() => take('callhome', [[3, 'callhome']], 20 + Math.round(15 * U(63)), { wait: 10, min: 12, queue: 'boothq' }));
    if (schedU(p.seed, d, 66) < SHOP_BASE(p, d)) out.push(() => {   // the crew store: browse the shelves, then pay at the till if there is one
      if (take('leisure', [[3, 'shop']], 10 + Math.round(12 * U(67)), { wait: 5, min: 8, tag: 'shop' })) take('leisure', [[3, 'pay']], 2, { wait: 6, min: 1, tag: 'pay' });
    });
    if (offDay && p.rota && p.rota.offDays && weekday(d) === p.rota.offDays[0]) out.push(() => take('leisure', [[4, 'laundry']], 30 + Math.round(15 * U(64)), { wait: 15, min: 20, tag: 'laundry' }));
    if (out[0] === gym && U(68) < .5) out.push(out.shift());   // half the time the gym waits until after dinner (the 17:00 rush)
    // the rooms' regulars (HABITS, section 9): a run on the treadmill (before dinner), and after dinner the music
    // room's instruments, tending the garden, a drink at the bar, the observatory
    const wk = F.works;
    if (H.has('runner') && U(100) < (wk ? .7 : .6)) out.unshift(() => take('gym', [[3, 'gym-run'], [3, 'gym']], 25 + Math.round(15 * U(101)), { wait: 10, min: 15, tag: 'run' }));
    if (H.has('musician') && U(102) < (weekday(d) === 3 && p.rank === 'captain' ? 1 : .55)) out.push(() => take('leisure', [[4, 'music']], 45 + Math.round(30 * U(103)), { wait: 10, min: 25, tag: 'play', anim: 'play' }));
    if (H.has('gardener') && U(104) < .6) out.push(() => take('leisure', [[3, 'garden-tend'], [3, 'garden']], 30 + Math.round(30 * U(105)), { wait: 5, min: 20, tag: 'tend' }));
    if (H.has('bar-regular') && U(106) < .75) out.push(() => take('leisure', [[3, 'bar'], [3, 'lounge-seat']], 30 + Math.round(30 * U(107)), { wait: 5, min: 20, tag: 'bar', anim: 'drink' }));
    if (H.has('stargazer') && U(108) < .5) out.push(() => take('leisure', [[2, 'observatory'], [2, 'lounge-seat']], 45 + Math.round(45 * U(109)), { wait: 5, min: 25, tag: 'stars' }));
    return out;
  };
  // the evening: specials, dinner, leisure, then to bed (or to the night shift at workStart)
  const evening = (sp, until, toWork, ateDinner) => {
    if (/^work:(works|engine)$/.test(wtype) && F.works && !F.night && t >= F.workEnd && t < F.workEnd + 5)   // Works crew wash up after the shift
      take('wash', U(35) < .3 ? [[wd, 'shower'], [wd, 'basin']] : [[wd, 'basin']], U(35) < .3 ? 8 : 3, { wait: 4, min: 2, tag: 'hands' });
    let dinnerAt = Math.max(t, H.has('late-diner') ? 1165 + Math.round(15 * U(70)) : 1030 + Math.round(70 * U(70)));
    // answer 11: some days (about 2 in 5) half the day shift heads straight for dinner when the shift ends: a rush at the servery
    if (!H.has('late-diner') && F.works && !F.night && schedU(9200, d, 0) < .4 && U(73) < .5) dinnerAt = Math.max(t, F.workEnd + 3 + Math.round(10 * U(74)));
    const ho = meet.find(e => e.tag === 'handover'); if (ho && dinnerAt < ho.at + ho.dur && S.shared.has('1|@handover')) dinnerAt = ho.at + ho.dur;   // eat after the handover
    let dinnerBy = 1440;                                 // dinner before a gathering ends when it starts (a grab if that's too soon)
    for (const e of meet) if (e !== ho && !e.done && !e.meal && e.at < dinnerAt + 40 && e.at + e.dur > dinnerAt) {   // dinner clear of a gathering: after it if there's time, else before
      if (e.at + e.dur + 25 <= MEALS.dinner[1]) dinnerAt = Math.max(dinnerAt, e.at + e.dur);
      else { dinnerAt = Math.max(t, Math.min(dinnerAt, e.at - 45)); dinnerBy = Math.min(dinnerBy, e.at); }
    }
    const mt = !ateDinner && meet.find(e => e.meal === 'dinner' && !e.done && e.at + 10 > t && e.at < until - 30);   // a meal tradition: going is their dinner
    if (mt) { dinnerAt = Math.max(t, mt.at + mt.dur); dinnerBy = 1440; }
    if (sp.length && t + 45 < dinnerAt && clear(70)) sp.shift()();
    leisureUntil(Math.min(dinnerAt, until - 40), 71);
    if (mt && segs.some(s => s.act === 'dinner' && s.tag === mt.tag)) ateDinner = true;   // they got a seat at it (else the ordinary dinner after)
    if (ateDinner) {}
    else if (t < MEALS.dinner[1] - 15) meal('dinner', 72, Math.min(MEALS.dinner[1], until - (toWork ? C : 0), dinnerBy));
    else grab('dinner', 72);
    while (sp.length && t < until - 60 && clear(70)) sp.shift()();
    if (toWork) { leisureUntil(until - C, 80); go(wd); work(1440); return; }
    const showerT = eveShower ? 22 : 0;
    leisureUntil(until - showerT - C, 80);
    if (showerT) wash(81, true);
    go(bedDeck); if (U(82) < .4) toilet(82);
    linger(Math.max(t, until));
    seg('sleep', 1440, 'bed', p.bed);
  };
  const morning = (k, by) => {                           // the toilet, a wash, tidy for inspection, breakfast (sit-down or grab)
    if (U(k + 7) < .5) toilet(k + 7);
    // not everyone goes the same way to breakfast (the user's playtest 2, 0.71.5): about 3 in 10 straight there and
    // wash after, 2 in 10 a short workout first, 2 in 10 a coffee or a read after the wash, the rest wash and go
    const sty = U(k + 13), quiet = !F.shape.inspect && !H.has('skips-breakfast') && !meet.some(e => !e.done && e.at < by + 150 && e.at + e.dur > t);
    if (quiet && sty < .3 && by - t >= 100) {
      meal('breakfast', k + 5, by - 45);
      if (by - t >= 45) wash(k); else if (by - t >= 15) take('wash', [[bedDeck, 'basin']], 5, { wait: 5 });
      return;
    }
    if (quiet && sty < .5 && by - t >= 80) take('gym', [[3, 'gym']], 15 + Math.round(10 * U(k + 14)), { wait: 5, min: 12, by: by - 50 });
    wash(k);
    if (quiet && sty >= .5 && sty < .7 && by - t >= 95) leisureUntil(t + 20 + Math.round(20 * U(k + 14)), k + 15);
    if (F.shape.inspect && /^4-B/.test(p.bed)) { go(bedDeck); seg('off', t + 10, 'bed', p.bed, { tag: 'inspection' }); }
    const pre = meet.find(e => !e.meal && !e.done && (e.at >= t || REC_ON && /^ev-rec-/.test(e.tag || '') && e.at + e.dur - t >= (e.min || 20)) && e.at + e.dur <= by - (REC_ON && /^ev-rec-/.test(e.tag || '') ? 8 : 25));   // a rec one (Dawn swim) already begun still counts (0.83.1)   // a gathering before breakfast (Sunrise stretch, Pick-your-own; 0.36.86): to it, then breakfast
    if (pre) leisureUntil(pre.at + pre.dur, k + 11);
    const mb = meet.find(e => e.meal === 'breakfast' && !e.done && e.at + 10 > t && e.at < by + 150);   // a meal tradition (the long breakfast) is their breakfast
    if (mb) { leisureUntil(mb.at + mb.dur, k + 9); if (segs.some(s => s.act === 'breakfast' && s.tag === mb.tag)) return; if (t >= by - 5) { grab('breakfast', k + 3); return; } }
    if (H.has('skips-breakfast') && U(k + 1) < .7) { if (!pre) linger(Math.max(t, by - 8 - Math.round(10 * U(k + 2)))); grab('breakfast', k + 3); return; }
    const want = Math.max(MEALS.breakfast[0], by - 30 - Math.round(100 * U(k + 4)) - (H.has('lingers-at-meals') ? 15 : 0));   // spread over the morning (playtest 2: not everyone at 08:00-08:30)
    if (want > t + C + 5 && !pre) linger(want - (deck !== 3 ? C : 0));   // after a gathering: straight to breakfast (waiting would only stretch the gathering)
    meal('breakfast', k + 5, by);
  };

  const GP = !F.night && shiftBlocks(p, d), GB = GP && GP.blocks;
  if (GB) {
    // the galley rota: stints at the galley's stations (each its own place and task), free time between, meals at
    // the times the rota gives (or in their window, around the work), and a staff meal at the station only when
    // the work covers a whole window and the rota gives no time for it
    const early = GB[0][0] < 420;
    seg('sleep', Math.max(GP.wake != null ? GP.wake : early ? GB[0][0] - 35 : F.wake, P.bed + 410 - 1440), 'bed', p.bed);
    if (early) wash(20); else morning(20, Math.min(MEALS.breakfast[1], GB[0][0] - C));
    const ate = { breakfast: !early }, given = GP.meals || {};
    GB.forEach(([a, b, pid, task], i) => {
      if (!pid && GP.desk) pid = desk;
      if (t < a) {                                        // a gap before this stint
        for (const m of ['breakfast', 'dinner']) {
          if (ate[m]) continue;
          const w = given[m];
          if (w && w[0] >= t && w[1] <= a) { if (w[0] - C > t) leisureUntil(w[0] - C, 90 + i); meal(m, 92 + i, w[1]); ate[m] = true; }
          else if (!w) { const [w0, w1] = MEALS[m]; if (Math.min(w1, a - C) - Math.max(w0, t + C) >= 20) { if (t + C < w0) leisureUntil(w0 - C, 90 + i); meal(m, 92 + i, Math.min(w1, a - C)); ate[m] = true; } }
        }
        if (t < a - C) leisureUntil(a - C, 94 + i);          // back a ride early, wherever the free time took them
      }
      go(wd); linger(a);                                 // early: wait for the stint (someone else may be at that station)
      if (p.dept === 'garden' && pid && !isFree(pid, Math.max(t, a), Math.min(b, 1440))) {   // someone already stands there: the next free spot along the beds
        const alt = task === 'carry' ? [] : gardenSpots(); pid = (alt.find(pl => isFree(pl.id, Math.max(t, a), Math.min(b, 1440))) || {}).id || null;
      }
      if (p.dept === 'garden' && pid) hold(pid, Math.max(t, a), Math.min(b, 1440));
      if (!given.breakfast && !given.dinner) for (const m of ['breakfast', 'dinner']) {   // no time given and none free: eat at the station
        const [, w1] = MEALS[m];
        if (!ate[m] && Math.max(a, t) <= w1 - 30 && b >= w1 - 10 && !GB.some(x => x[0] > b && x[0] < w1)) { workAt(pid, task, w1 - 30); seg(m, w1 - 10, pid && S.byId.get(pid) ? S.byId.get(pid).type : wtype, pid, { tag: 'staff' }); ate[m] = true; }
      }
      workAt(pid, task, Math.min(b, 1440));
    });
    if (t < 1440) evening(specials(50, false), Math.max(t + 30, F.bed), false, ate.dinner);
  } else if (!F.night) {
    seg('sleep', Math.max(F.wake, P.bed + 410 - 1440), 'bed', p.bed);
    if (F.works) {
      const ws = F.workStart, we = F.workEnd;
      morning(20, ws - (wd !== 3 ? C : 0) - 1 - (clocks ? CLOCK_EARLY : 0));   // a minute in hand for the wait by the lift; the Works crew come early enough to clock in before the shift starts (0.27.48: they queued at the clock past 08:00, so worked 535-539 of 540)
      go(wd);
      shiftWithBreaks(we);
      evening(specials(50, false), F.bed, false, F.double);
    } else {
      morning(20, MEALS.breakfast[1]);
      const sp = specials(50, true);
      let end0 = t + 30 + Math.round(60 * U(55)); const rg = REC_ON && meet.find(e => !e.done && /^ev-rec-/.test(e.tag || '') && e.at >= t && e.at < end0 + 30);   // a rec one this morning (the regatta, Slow stretch): the block runs on through it (0.83.1)
      if (rg) end0 = Math.max(end0, rg.at + rg.dur);
      leisureUntil(end0, 56);
      while (sp.length > 1) { const f = sp.shift(); if (clear(70)) f(); leisureUntil(t + 40 + Math.round(80 * U(57 + sp.length)), 58 + sp.length * 4); }
      evening(sp, F.bed, false);
    }
  } else {
    // night shift: the shift that began last night runs to 06:00, then breakfast and sleep through the day
    if (P.works) {
      deck = wd;
      if (wd === 1 && P.workEnd >= 60) { work(P.workEnd - 15); take('work', [[1, '@handover']], 15, { by: P.workEnd, min: 5, tag: 'handover' }); }   // the night watch hands over at the ring
      work(P.workEnd);
      meal('breakfast', 20, MEALS.breakfast[1]);
      wash(25, true); go(bedDeck);                       // a shower after the night's work, then bed
      seg('sleep', t + 420 + Math.round(30 * U(26)), 'bed', p.bed);
      const sp = specials(50, !F.works);
      evening(sp, F.works ? F.workStart : F.bed, F.works);
    } else {
      seg('sleep', Math.max(400 + Math.round(50 * U(21)), P.bed + 410 - 1440), 'bed', p.bed);
      morning(22, MEALS.breakfast[1]);
      const sp = specials(50, true);
      if (F.works) {                                     // back on tonight: a long nap in the afternoon
        if (sp.length) sp.shift()();
        leisureUntil(Math.max(t, 770 + Math.round(30 * U(27))), 28);
        go(bedDeck); seg('sleep', t + 240, 'bed', p.bed);
        evening(sp, F.workStart, true);
      } else {
        leisureUntil(t + 30 + Math.round(60 * U(55)), 56);
        while (sp.length > 1) { const f = sp.shift(); if (clear(70)) f(); leisureUntil(t + 40 + Math.round(80 * U(57)), 58); }
        evening(sp, F.bed, false);
      }
    }
  }
  // tidy: absolute times, neighbours with the same act and place joined
  const out = [];
  for (const s of segs) {
    const l = out[out.length - 1];
    if (l && l.act === s.act && l.placeId === s.placeId && l.deck === s.deck && l.tag === s.tag && l.to === B + s.from) l.to = B + s.to;
    else out.push({ ...s, from: B + s.from, to: B + s.to });
  }
  return out;
}

// ---- needs on paper: a person's needs at ship minute t, worked out from their plans over the week before ----
// hunger: a sit-down meal fills it, grab-and-go half; it drains over about 18 hours. energy: sleep restores about
// 14 an hour; awake it drains over about 26 hours. hygiene: a shower fills it, a basin a little; it drains over
// about 48 hours, faster in the gym. fitness: the gym adds 35; it drains about 8 a day. social: company
// (meals, the lounge, common room, garden, gym...) adds 15 an hour and a call home 35; alone it drains slowly.
function crewNeeds(p, t) {
  const n = { hunger: 70, energy: 70, hygiene: 70, fitness: 70, social: 70 }, cl = v => Math.max(0, Math.min(100, v));
  const d1 = Math.floor(t / 1440) + 1;
  for (let d = d1 - 7; d <= d1; d++) for (const s of planDay(p, d)) {
    if (s.from >= t) break;
    const h = (Math.min(s.to, t) - s.from) / 60, type = s.type, tag = s.tag;
    // the ship's state where they were (section 17): drains run faster, restores give back less, e.g. a weak shower
    const fx = typeof shipEffectsAt === 'function' ? shipEffectsAt(s.deck, s.from) : null;
    const dr = k => fx && fx.drain && fx.drain[k] || 1, rs = k => fx && fx.restore && fx.restore[k] !== undefined ? fx.restore[k] : 1;
    const up = (k, to) => { n[k] = cl(n[k] + Math.max(0, to - n[k]) * rs(k)); };   // restore toward `to`, scaled
    n.hunger = cl(n.hunger - 5.5 * h * dr('hunger')); n.fitness = cl(n.fitness - .35 * h * dr('fitness'));
    const ev = evAt(s.from);                              // a ship-wide event: sleep refills slower, company is missed sooner (C7)
    if (s.act === 'sleep') up('energy', n.energy + 14 * h * (ev ? ev.sleep : 1)); else n.energy = cl(n.energy - 3.8 * h * dr('energy'));
    n.hygiene = cl(n.hygiene - 2.1 * h * dr('hygiene'));
    if ((s.act === 'breakfast' || s.act === 'dinner') && tag !== 'queue') up('hunger', tag === 'grab' ? 50 : 100);
    if (s.act === 'wash' && tag !== 'toilet') up('hygiene', type === 'shower' ? 100 : n.hygiene + 15);
    if (s.act === 'gym') { up('fitness', n.fitness + (h >= .4 ? 35 : 15)); n.hygiene = cl(n.hygiene - 10); }
    if (s.act === 'callhome') up('social', n.social + 35);
    else if (SOCIAL_TYPES.has(type) || /^work:/.test(type)) up('social', n.social + 15 * h); else n.social = cl(n.social - 2.5 * h * dr('social') * (ev ? ev.social : 1));
  }
  for (const k of NEEDS) n[k] = Math.round(n[k]);
  return n;
}
// ---- how the crew feel (answers 16 and 22): a mood from their needs and the ship, and a line for the tap toast ----
// crewMood(p, t): 0-100, the needs averaged (the low ones count double), plus the ship's mood where they are
// (shipEffectsAt(deck, t).mood, 0 to -30: faltering machines and a run-down ship), plus a birthday lift, plus a
// little of the day's own temper (schedU, so the same person on the same day is the same). Pure: it only reads.
const shortName = p => { const w = p.name.split(' '); return /^(Captain|Commander|Dr\.|Chief|Chef|Lt\.?|Lieutenant|Ensign)$/.test(w[0]) && w.length > 2 ? w[0] + ' ' + w[w.length - 1] : w[0]; };
const isBirthday = (p, t) => !!p.birthday && ((Math.floor(t / 1440) % 364) + 1) === p.birthday;
function crewMood(p, t) {
  const n = crewNeeds(p, t); let a = 0, w = 0;
  for (const k of NEEDS) { const x = n[k], k2 = x < 40 ? 2 : 1; a += x * k2; w += k2; }
  const wh = planWhere(p, t), fx = typeof shipEffectsAt === 'function' && wh ? shipEffectsAt(wh.deck, t) : null;
  const m = a / w + (fx ? fx.mood : 0) + (isBirthday(p, t) ? 15 : 0) + 12 * (schedU(p.seed, Math.floor(t / 1440) + 1, 500) - .5);
  return Math.round(Math.max(0, Math.min(100, m)));
}
const FEEL_LOW = {                                       // a need under 30: what you notice (two ways of saying it)
  energy: ['looks tired', 'stifles a yawn'], hunger: ['looks hungry', 'keeps glancing at the time'],
  hygiene: ['could do with a shower', 'looks a bit rumpled'], fitness: ['looks restless', 'stretches a stiff back'],
  social: ['seems a bit lonely', 'seems glad of the company'],
};
// crewFeeling(p, t): one short line, or null when there's nothing to notice. In order: a birthday; the ship's
// trouble where they are when it weighs on them (grumbling about the showers); the lowest need under 30; a very
// good or a low mood.
function crewFeeling(p, t) {
  const who = shortName(p), U = k => schedU(p.seed, Math.floor(t / 1440) + 1, k), pick = (a, k) => a[Math.floor(U(k) * a.length)];
  if (isBirthday(p, t)) return 'It\'s ' + who + '\'s birthday today.';
  const wh = planWhere(p, t), fx = typeof shipEffectsAt === 'function' && wh ? shipEffectsAt(wh.deck, t) : null;
  if (fx && fx.mood <= -3 && fx.notes && fx.notes.length) {
    const worst = { minor: 1, noticeable: 2, serious: 3 }, nt = fx.notes.slice().sort((a, b) => worst[b.stage] - worst[a.stage])[0];
    return who + ' ' + pick(['grumbles', 'complains', 'sighs'], 501) + ' that ' + nt.text[0].toLowerCase() + nt.text.slice(1).replace(/;.*$/, '') + '.';
  }
  const n = crewNeeds(p, t), low = NEEDS.filter(k => n[k] < 30).sort((a, b) => n[a] - n[b])[0];
  if (low) return who + ' ' + pick(FEEL_LOW[low], 502) + '.';
  const m = crewMood(p, t);
  if (m >= 85) return who + ' ' + pick(['is in good spirits', 'is humming a tune', 'seems cheerful'], 503) + '.';
  if (m < 40) return who + ' ' + pick(['seems a bit low', 'is quiet today'], 504) + '.';
  return null;
}
// how much each place type is used over `days` days from day d0: per 'deck type', the number of places, how many
// of them were used, the uses, the hours, and how many different people (day_check's "rooms in use")
function roomsInUse(d0, days = 7) {
  const S = schedData(), T = {};
  for (const pl of S.places) { const k = pl.deck + ' ' + pl.type; (T[k] = T[k] || { places: 0, used: new Set(), uses: 0, min: 0, people: new Set() }).places++; }
  for (let d = d0; d < d0 + days; d++) for (const p of S.people) for (const s of planDay(p, d)) {
    const pl = s.placeId && S.byId.get(s.placeId); if (!pl) continue;
    const t = T[pl.deck + ' ' + pl.type]; if (!t) continue;   // an event's own place (type 'event', the Deck 1 routines): not an everyday type
    t.uses++; t.min += s.to - s.from; t.used.add(pl.id); t.people.add(p.id);
  }
  return Object.entries(T).sort().map(([k, t]) => ({ k, places: t.places, used: t.used.size, uses: t.uses, hours: Math.round(t.min / 60), people: t.people.size }));
}

// the places the crew's jobs (section 17) took them to: per 'deck type', visits and different places, from the jobs
// on the books now (claimed or done in the last two days); null before there are any
function jobVisits() {
  if (typeof SHIP === 'undefined' || !Array.isArray(SHIP.jobs)) return null;
  const S = schedData(), byId = new Map(); for (const n in DECKS) for (const p of DECKS[n].places || []) byId.set(p.id, { ...p, deck: +n });
  const T = {};
  for (const j of SHIP.jobs) for (const s of j.segs || []) if (s.placeId) {
    const pl = S.byId.get(s.placeId) || byId.get(s.placeId); if (!pl) continue;
    const t = T[pl.deck + ' ' + pl.type + (pl.machine ? ' (panel)' : '')] || (T[pl.deck + ' ' + pl.type + (pl.machine ? ' (panel)' : '')] = { visits: 0, places: new Set() });
    t.visits++; t.places.add(pl.id);
  }
  return Object.entries(T).sort().map(([k, t]) => ({ k, visits: t.visits, places: t.places.size }));
}

// ---- the whole ship's day, planned once and kept (the last few days) ----
const SHIP_DAYS = new Map();
function shipDay(d) {
  if (evChanged()) { EV_SIG = evSig(); EV_DAY.clear(); SHIP_DAYS.clear(); }   // a ship-wide event began or ended: plan again (C7)
  const was = SHIP_DAYS.get(d); if (was && !(was.occ.recAt != null && !was.occ.recSet && recSettled(was.occ.recAt))) return was;   // planned before its rec hour was settled: plan again (RC, 0.64.1)
  const S = schedData(), occ = new Map(), plans = new Map();
  // the day's stand-ins: for each spare station, one person from its department (day shift, working today) works there
  occ.rot = new Map();
  occ.who = new Map();                                   // who -> the places they hold (seating by friendship)
  S.spare.forEach((pl, i) => {
    const dept = pl.type.slice(5), c = S.people.filter(p => p.dept === dept && p.shift !== 'night' && isWorkDay(p, d) && !occ.rot.has(p.id) && !shiftBlocks(p, d) && aboardAllDay(p, d));
    if (c.length) occ.rot.set(c[Math.floor(schedU(strSeed(pl.id), d, 7) * c.length)].id, { deck: pl.deck, id: pl.id, type: pl.type });   // by the station's id, so a new station never reshuffles the others
  });
  occ.rotIds = new Set([...occ.rot.values()].map(r => r.id));   // today's stand-in stations (a guest never takes one)
  const wakeAt = p => { const F = schedFrame(p, d); return F.night ? (schedFrame(p, d - 1).works ? 360 : F.wake) : F.wake; };
  // an event's host (section 18's eventPlan, host: true: Pell at his own show) is planned first, so their seat is theirs
  const host = typeof eventsOn === 'function' && eventsOn(d).some(e => e.ev.host) ? new Set(S.people.filter(p => eventPlan(p, d).some(e => e.host)).map(p => p.id)) : null;
  const order = S.people.slice().sort((a, b) => (host ? host.has(b.id) - host.has(a.id) : 0) || wakeAt(a) - wakeAt(b) || (a.id < b.id ? -1 : 1));
  occ.heads = new Int16Array(1440);                      // how many the plans so far put on Deck 3, minute by minute
  if (REC_ON) occ.rec = new Int16Array(1440);            // and on the rec deck (RA, 0.83.0: its cap, REC_CAP)
  // section 18's events: each event's own places are held for it (occ.res: placeId -> [[from, to, eventId]], not a
  // booking, so dayReport never counts them) from 5 minutes before it starts until it ends (releasing them 15 minutes
  // in let early planners take seats later guests wanted: the jam stayed empty). The places: eventPlaces(e)
  // (section 18), else its tagged places and rooms and its first pool
  occ.res = new Map();
  const mealEv = new Set();                              // today's meal traditions (their diners are planned first; 0.26.32)
  if (typeof eventsOn === 'function') for (const e of eventsOn(d)) {
    const ids = typeof eventPlaces === 'function' ? (eventPlaces(e) || []).slice()
      : typeof eventOpts === 'function' ? eventOpts(e.ev, { rank: 'officer' })   // its tagged places and rooms, and its first pool (the event's own room)
        .filter(([n, k]) => /^(@|ev:)/.test(k) || (e.ev.where[0] && e.ev.where[0].pool === k && e.ev.where[0].deck === n)).flatMap(([n, k]) => (S.shared.get(n + '|' + k) || []).map(pl => pl.id)) : [];
    if (!ids.length && e.ev.meal && Array.isArray(e.ev.where)) {   // a meal tradition (the Sunday long table): as many of its seats as are coming, in id order, so the ordinary diners don't fill them
      const n = S.people.filter(p => aboard(p, d) && (eventPlan(p, d) || []).some(x => x.id === e.id)).length, nat = (a, b) => a.id.localeCompare(b.id, 'en', { numeric: true });
      for (const w of e.ev.where) { const rx = w.room ? new RegExp(w.room instanceof RegExp ? w.room.source : String(w.room), 'i') : null, rooms = (DECKS[w.deck] || {}).rooms || {};
        for (const ty of w.types || []) ids.push(...(S.shared.get(w.deck + '|' + ty) || []).filter(pl => !rx || rx.test((rooms[pl.room] || {}).name || '')).sort(nat).map(pl => pl.id)); }
      ids.splice(n); mealEv.add(e.id);
    }
    for (const id of new Set(ids)) { if (!occ.res.has(id)) occ.res.set(id, []); occ.res.get(id).push([(d - 1) * 1440 + e.from - 5, (d - 1) * 1440 + e.to, e.id]); }
  }
  // section 21's named seats (Calder's across from yours) are held for whoever has them before anyone is planned, so an
  // earlier riser never takes one (introLay books it; no 'ev-' tag matches 'intro:<id>', so nobody else may) (0.26.32)
  if (typeof introPlan === 'function') for (const p of S.people) {
    let add = null; try { add = introPlan(p, d); } catch (e) { add = null; }
    for (const e of Array.isArray(add) ? add : []) if (e && e.placeId && !e.alts && e.to > e.from) {
      if (!occ.res.has(e.placeId)) occ.res.set(e.placeId, []);
      occ.res.get(e.placeId).push([(d - 1) * 1440 + Math.max(0, e.from), (d - 1) * 1440 + Math.min(1440, e.to), 'intro:' + p.id]);
      // the arrival dinner (section 21's chief step, seats: you, the escort, the Chief): with the Chief's seat, yours and the
      // escort's are held too, from the table step (Torres sits you down first) to the Chief's end, so nobody else plans to
      // sit there ('intro:player' is nobody's) and introLay sits the escort in his (0.26.39, build master 2's day-0 find)
      const st = e.tag === 'intro-chief' && typeof introStepById === 'function' ? introStepById('chief') : null, tb = st && introStepById('table');
      if (st && st.seats) for (const [who, id] of Object.entries(st.seats)) if (id !== e.placeId && S.byId.has(id)) {
        const owner = who === 'you' ? 'player' : typeof INTRO_ESCORT !== 'undefined' && who === INTRO_ESCORT ? (SHIP.intro && SHIP.intro.escort) || who : who;
        const a = Math.max(0, Math.min(e.from, tb && tb.at != null ? tb.at - INTRO_EARLY : e.from));
        if (!occ.res.has(id)) occ.res.set(id, []);
        occ.res.get(id).push([(d - 1) * 1440 + a, (d - 1) * 1440 + Math.min(1440, e.to), 'intro:' + owner]);
      }
    }
  }
  // crew leaving today wait in the shuttle bay 14:30-15:00 (guestTrim): each one's spot is held for them before anyone is
  // planned ('leave:<id>', which no tag matches), so their farewell friends stand round them, never in it (0.26.38)
  const leave = new Map(), bayL = (S.shared.get('5|event') || []).filter(pl => /shuttle-bay-crowd/.test(pl.id));
  for (const p of S.people) if (!p.guest && bayL.length && guestStay(p, d) === 'leave') {
    const id = (bayL.find(pl => ![...leave.values()].includes(pl.id)) || bayL[0]).id; leave.set(p.id, id);   // the front spots, nearest the shuttle
    if (!occ.res.has(id)) occ.res.set(id, []); occ.res.get(id).push([(d - 1) * 1440 + ROTA_OFF - ROTA_WAIT, (d - 1) * 1440 + ROTA_OFF, 'leave:' + p.id]);
  }
  // a meal tradition's diners are planned next (after any hosts), and then its held seats are let go (their own bookings
  // keep theirs), so ordinary diners use the seats nobody took, or left early, not the lounge (reviewer 1b, 0.26.32)
  const goer = mealEv.size ? new Set(S.people.filter(p => aboard(p, d) && (eventPlan(p, d) || []).some(x => mealEv.has(x.id))).map(p => p.id)) : null;
  if (goer) order.sort((a, b) => (host ? host.has(b.id) - host.has(a.id) : 0) || goer.has(b.id) - goer.has(a.id));   // stable: wake order within each
  let trimmed = !goer;
  for (const p of order) {
    if (!trimmed && !goer.has(p.id) && !(host && host.has(p.id))) {
      trimmed = true;
      for (const [id, rs] of occ.res) occ.res.set(id, rs.filter(([x, y, ev]) => !mealEv.has(ev)));
    }
    const plan = introLay(p, d, occ, guestTrim(p, d, aboard(p, d) ? schedBuild(p, d, occ, S) : [], leave.get(p.id))); plans.set(p.id, plan);   // a guest away has no day here
    for (const s of plan) if (s.deck === 3 || s.deck === 7 && occ.rec) for (let m = Math.max(0, s.from - (d - 1) * 1440); m < Math.min(1440, s.to - (d - 1) * 1440); m++) (s.deck === 3 ? occ.heads : occ.rec)[m]++;
  }
  const day = { d, plans, occ };
  SHIP_DAYS.set(d, day);
  for (const k of SHIP_DAYS.keys()) if (k < d - 9 || k > d + 2) SHIP_DAYS.delete(k);   // needs look back a week
  return day;
}
function planDay(person, day) { return shipDay(day).plans.get(person.id) || []; }
// the arrival's beats (Pillar 4, section 21's introPlan(p, d) -> [{ from, to, deck, placeId?, act?, tag?, anim? }],
// minutes from that day's midnight): laid over the person's planned day as fixed blocks, the way an accepted
// appointment is, so the escort and the teachers are really busy then (whereIs, needs, dayReport all see it). The
// escort's steps on the deck come from section 10's lead and follow (escortPlan), not from here. A block's place is
// held in occ. Pure: introPlan reads the intro's saved state only, and shipDay plans again when that changes (introSig)
// introPlan(p, d): section 21's introBeats(p.id, d) -> [{ id, at, until, where }] (day minutes) as blocks. where:
// { deck, tile, room } (the arrival evening: at the place in that room nearest the tile, e.g. a mess seat by your
// table for Calder; the escort's is only a stand-in, since section 10's escort does the walking),
// { deck, room } (a week beat: the first free place in that room, by id, nobody's own and nobody's desk) or 'seek'
// (section 20's seek finds you: nothing planned). [] when the intro is off
const STAFF_ONLY = new Set(['bar-staff']);              // behind the bar: the bartender's alone, never a beat's place (0.36.91; Pell's d4-quiz landed on 3-bar-1)
const INTRO_EARLY = 5;
const SHOWER_Q = 3;                                      // ship minutes: a shorter wait for a shower isn't worth queueing for                                   // minutes early to a named seat (the Chief at your table)
function introPlan(p, d) {
  if (typeof introBeats !== 'function') return null;
  let beats = null; try { beats = introBeats(p.id, d); } catch (e) { return null; }
  if (!Array.isArray(beats) || !beats.length) return null;
  const S = schedData(), nat = (a, b) => a.id.localeCompare(b.id, 'en', { numeric: true });
  return beats.filter(x => x && x.where && x.where !== 'seek' && x.until > x.at).map(x => {
    const w = x.where, rooms = (DECKS[w.deck] && DECKS[w.deck].rooms) || {};
    const inRoom = q => q.deck === w.deck && (q.room === w.room || (rooms[q.room] && rooms[q.room].name === w.room)) && q.type !== 'bed' && !STAFF_ONLY.has(q.type) && !S.owner.has(q.id) && !S.deskOf(q.id) && !q.machine;
    const cand = S.places.filter(inRoom).sort(nat), dist = q => w.tile ? Math.hypot(q.at[0] - w.tile[0], q.at[1] - w.tile[1]) : 0;
    const near = w.tile ? cand.filter(q => q.type !== 'event').sort((a, b) => dist(a) - dist(b)) : cand;   // a tile: the places nearest it first
    const pl = w.placeId && S.byId.get(w.placeId) ? S.byId.get(w.placeId) : near[0];   // a named place (Calder's seat across from yours)
    const seat = !!(w.placeId && pl), alts = w.placeId ? null : near.map(q => q.id);   // introLay takes the first of these free then
    return { from: seat ? x.at - INTRO_EARLY : x.at, to: x.until, deck: w.deck, placeId: pl ? pl.id : null, alts, tag: 'intro-' + x.id };   // a named seat: there and sitting when it starts
  });
}
function introLay(p, d, occ, segs) {
  let add = null;
  try { add = typeof introPlan === 'function' ? introPlan(p, d) : null; } catch (e) { add = null; }
  const B = (d - 1) * 1440, byId = schedData().byId;
  // a seat shipDay held for you that none of your beats sits you in (the escort's at the arrival dinner): sit there for
  // the whole hold, and a beat of yours that overlaps it takes that seat, not a stand-in (0.26.39)
  const mine = [];
  if (occ.res) for (const [id, rs] of occ.res) for (const [x, y, ev] of rs) if (ev === 'intro:' + p.id && y > B && x < B + 1440) mine.push([id, x, y]);
  const named = Array.isArray(add) ? add : (add = []);
  for (const [id, x, y] of mine) if (!named.some(e => e && e.placeId === id && !e.alts)) { const pl = byId.get(id); if (pl) named.unshift({ from: x - B, to: y - B, deck: pl.deck, placeId: id, alts: null, tag: 'intro-seat' }); }
  if (!add.length) return segs;
  let out = segs.slice();
  for (const e of add.filter(e => e && e.to > e.from).sort((a, b) => a.from - b.from)) {
    const a = B + Math.max(0, e.from), b = B + Math.min(1440, e.to), cut = [];
    const free = id => !(occ.get(id) || []).some(([x, y]) => x < b && a < y)   // never a place someone already has then (Calder and Torres at Monday's briefing),
      && !(occ.res && (occ.res.get(id) || []).some(([x, y, ev]) => x < b && a < y && ev !== 'intro:' + p.id));   // nor one held for someone else (Calder's named seat) or an event (reviewer 1, 0.26.37)
    const near = (u, v) => { const q = byId.get(u), r = byId.get(v); return !!q && !!r && q.deck === r.deck && Math.hypot(q.at[0] - r.at[0], q.at[1] - r.at[1]) <= 2.5; };
    const held = e.alts && e.alts.length && mine.find(([id, x, y]) => x < b && a < y && near(e.alts[0], id));   // your held seat, if it's then and where this beat sits you anyway (0.26.39)
    const pid = held ? held[0] : e.alts && e.alts.length ? e.alts.find(free) || null : e.placeId, pl = pid ? byId.get(pid) : null;   // none free: there, standing
    for (const x of out) {
      if (x.to <= a || x.from >= b) { cut.push(x); continue; }
      if (x.from < a) cut.push({ ...x, to: a });
      if (x.to > b) cut.push({ ...x, from: b });
    }
    const seg = { from: a, to: b, act: e.act || 'intro', deck: e.deck != null ? e.deck : pl ? pl.deck : 0, type: pl ? pl.type : null, placeId: pl ? pl.id : null, tag: e.tag || 'intro' };
    if (e.anim) seg.anim = e.anim;
    cut.sort((x, y) => x.from - y.from);
    const prev = cut.filter(x => x.to <= a).pop();          // coming from another deck: the lift ride comes out of what they were doing
    if (prev && prev.to === a && prev.deck && seg.deck && prev.deck !== seg.deck && prev.to - prev.from > SCHED_COMMUTE) {
      prev.to = a - SCHED_COMMUTE; cut.push({ from: a - SCHED_COMMUTE, to: a, act: 'commute', deck: seg.deck, type: 'lift', placeId: null, fromDeck: prev.deck });
    }
    const next = cut.find(x => x.from >= b);                // and back afterwards: the ride comes out of what's next
    if (next && next.from === b && next.deck && seg.deck && next.deck !== seg.deck && next.act !== 'commute' && next.to - next.from > SCHED_COMMUTE) {
      next.from = b + SCHED_COMMUTE; cut.push({ from: b, to: b + SCHED_COMMUTE, act: 'commute', deck: next.deck, type: 'lift', placeId: null, fromDeck: seg.deck });
    }
    cut.push(seg); cut.sort((x, y) => x.from - y.from); out = cut;
    if (pl && e.tag !== 'intro-seat') { if (!occ.has(pl.id)) occ.set(pl.id, []); occ.get(pl.id).push([a, b, p.id]); if (occ.who) (occ.who.get(p.id) || occ.who.set(p.id, []).get(p.id)).push([a, b, pl.id]); }
  }
  return out;
}
// whereIs: where someone is at ship minute t. A job they've claimed (section 17's jobWhere: to the parts shelf, the
// machine's panel and back) is laid over their plan; otherwise it's the plan (planWhere). Anything that needs the
// plan alone (section 17's jobRun, which fits jobs into it) calls planWhere, never whereIs: whereIs from inside
// machinesNow would run an hour's jobs twice. The flag stops jobWhere reaching jobWhere again through whereIs.
let JOB_WHERE_BUSY = false;
function whereIs(person, t) {
  if (typeof liftHeld === 'function' && liftHeld(t) && typeof roofWait === 'function') { const lw = roofWait(person, t); if (lw) return lw; }   // 24s: the car held for the roof job: crew who need another deck wait by the lift
  const es = escortWhere(person, t); if (es) return es;   // section 21's escort goes where you go (section 10 walks them)
  const cv = comeWhere(person, t); if (cv) return cv;       // a visit (crewComeTo): to a place on your deck, then back
  const tw = typeof tradWhere === 'function' ? tradWhere(person, t) : null; if (tw) return tw;   // section 18: a tradition's walk in one line (0.70.0)
  const ap = apptWhere(person, t); if (ap) return withHold(person, ap, false);   // an accepted appointment comes first
  if (typeof jobWhere === 'function' && !JOB_WHERE_BUSY) {
    JOB_WHERE_BUSY = true; let j;
    try { j = jobWhere(person, t); } finally { JOB_WHERE_BUSY = false; }
    if (j) return withHold(person, j, true);
  }
  return withHold(person, planWhere(person, t), false);
}
// the escort (Pillar 4): while section 21's escortPlan(p, t) gives { mode: 'lead'|'follow'|'wait', to: placeId | [c, r] }
// for someone, they're on your deck (crossing decks with you: they step out of the lift after you), at `to` if it's a
// place there. Only in play (the deck you're on); plans never see it. Section 10's CrewAgent walks them (escortStep)
function escortPlanOf(p, t) {
  if (typeof escortPlan !== 'function' && typeof worksEscort !== 'function' && !CREW_SCENE.size) return null;     // (before section 10 has run, deckDef and player don't exist yet)
  try { if (!deckDef || !player) return null; const e = (typeof escortPlan === 'function' ? escortPlan(p, t) : null) || (typeof worksEscort === 'function' ? worksEscort(p, t) : null) || crewSceneOf(p, t); return e && /^(lead|follow|wait)$/.test(e.mode) ? e : null; } catch (e) { return null; }   // worksEscort: section 24's teachers (0.44.3); crewScene: stage directions (0.71.2)
}
function escortWhere(p, t) {
  const e = escortPlanOf(p, t); if (!e) return null;
  let pl = null; try { pl = typeof e.to === 'string' ? PLACE_OF.get(e.to) : null; } catch (x) { pl = null; }   // a place id here (or a { deck, tile | room })
  const deck = e.mode === 'wait' && e.to && e.to.deck != null ? e.to.deck : deckDef.num;   // waiting on another deck: there; else with you
  return { deck, act: 'intro', type: pl ? pl.type : null, placeId: pl ? e.to : null, moving: false, from: t - 1, until: t + 1, tag: 'escort', escort: e, hold: e.hold || null };
}
// stage directions (0.71.2, the sim side of the first promotion, plans/mechanics/promotion-officer.html): crewScene(id,
// { mode, to, until, hold }) has someone lead, follow or wait (escortStep's modes) until `until` (absolute ship minutes),
// e.g. holding 'carry' (the box). `to`: a place id, or { deck, tile } (a tile on another deck: they're there when you
// come). Asked by escortPlanOf after section 21's escortPlan and section 24's worksEscort. Live only, nothing saved
const CREW_SCENE = new Map();
function crewScene(id, o = {}) {
  id = id && (id.id || id); if (!id || !/^(lead|follow|wait)$/.test(o.mode || 'wait')) return false;
  CREW_SCENE.set(id, { mode: o.mode || 'wait', to: o.to || null, until: Number.isFinite(o.until) ? o.until : shipNow() + 30, hold: o.hold || null, pace: o.pace });
  return true;
}
function crewSceneEnd(id) { CREW_SCENE.delete(id && (id.id || id)); }
function crewSceneOf(p, t) {
  const s = CREW_SCENE.size && CREW_SCENE.get(p.id); if (!s) return null;
  if (t >= s.until) { CREW_SCENE.delete(p.id); return null; }
  let to = s.to;                                         // a place on another deck: there, by its tile (escortWhere only looks places up on this deck)
  if (typeof to === 'string' && typeof deckOf === 'function') { const d = deckOf(to), pl = DECKS[d] && (DECKS[d].places || []).find(q => q.id === to); if (pl && (typeof deckDef === 'undefined' || d !== deckDef.num)) to = { deck: d, tile: pl.at }; }
  return { mode: s.mode, to, hold: s.hold, pace: s.pace, scene: true };
}
// crewGather(ids, focus, { deck, until, hold }) -> the ids placed: each waits on their own open tile in a ring round
// `focus` (a place id: its walk-to tile; or a [c, r] tile on `deck`), in its room, nearest first, facing you. The tiles
// are picked from the deck's map when it's the deck you're on, else from DECKS (walls aside, never a blocked tile)
function crewGather(ids, focus, o = {}) {
  const sp = typeof focus === 'string' ? (Object.keys(DECKS).map(Number).map(n => [n, (DECKS[n].places || []).find(q => q.id === focus)]).find(x => x[1]) || []) : [];
  const deck = Number.isFinite(o.deck) ? o.deck : sp[0], at = Array.isArray(focus) ? focus : sp[1] ? (typeof placeSpot === 'function' && deckDef.num === deck && placeSpot(focus) ? placeSpot(focus).walk : sp[1].at) : null;
  if (!Number.isFinite(deck) || !at) return [];
  const here = typeof deckDef !== 'undefined' && deckDef.num === deck;
  const D = DECKS[deck], rm = (i, j) => here ? roomAt(i, j) : (D.map && D.map[j] && D.map[j][i] && D.map[j][i] !== '.' ? D.map[j][i] : null), open = (i, j) => here ? free(i, j) : !!rm(i, j);   // off this deck: any tile of the room (section 10 walks them to the nearest open one)
  const room = rm(at[0], at[1]), tiles = [];
  for (let k = 1; k <= 3 && tiles.length < ids.length; k++) for (let dj = -k; dj <= k; dj++) for (let di = -k; di <= k; di++) {
    if (Math.max(Math.abs(di), Math.abs(dj)) !== k) continue;
    const c = at[0] + di, r = at[1] + dj; if (open(c, r) && rm(c, r) === room) tiles.push([c, r]);
  }
  tiles.sort((a, b) => Math.hypot(a[0] - at[0], a[1] - at[1]) - Math.hypot(b[0] - at[0], b[1] - at[1]) || a[1] - b[1] || a[0] - b[0]);
  const out = [];
  ids.forEach((id, k) => { if (tiles[k] && crewScene(id, { mode: 'wait', to: { deck, tile: tiles[k] }, until: o.until, hold: o.hold })) out.push(id && (id.id || id)); });
  return out;
}
// the Works crew cheer you by the job board after Calder's office (Day 10, about 11:10-11:25): those on shift who are
// on Deck 5 at work and not out on a job. Returns their ids
function worksGather(until = shipNow() + 15) {
  const t = shipNow();
  const ids = ROSTER.filter(p => p.dept === 'works' && p.id !== 'you').filter(p => { const w = whereIs(p, t); return w && w.deck === 5 && w.act === 'work' && !w.moving && !w.job; }).map(p => p.id);
  const out = crewGather(ids, '5-jobboard-1', { until }); CHEER = out.length ? { ids: out, until, said: new Set() } : null; return out;
}
// your box on the way to 4-23 (Day 10, 17:05): Tomas and Pell wait by its door on Deck 4 holding it
function boxCarry(until = shipNow() + 40) { return crewGather(['tomas', 'pell'], [41, 14], { deck: 4, until, hold: 'carry' }); }
// the officer ceremony's guests (Day 11, 17:15, Deck 1's observation room): C2's occasion books one appointment at
// 07:00 (id 'promoCeremony@<day>', with the Captain, Vance, Calder, Torres and promoGuests' friends); this gives each of
// them their own seat at the conference table (a.places, saved with the appointment), so section 14's apptWhere brings
// them by lift and seats them instead of piling onto one place
const CEREMONY_SEATS = ['1-conf-1', '1-conf-2', '1-conf-3', '1-conf-4', '1-conf-5', '1-conf-6', '1-conf-7', '1-conf-8'];
function ceremonySeat(day) {
  const a = apptList().find(x => /^promoCeremony@/.test(String(x.occ || x.id)) && Math.floor(x.at / 1440) + 1 === day); if (!a || a.places) return a || null;
  const places = {}; a.with.forEach((id, k) => { if (CEREMONY_SEATS[k]) places[id] = CEREMONY_SEATS[k]; }); a.places = places; return a;
}
// the sim side of the first promotion (plans/mechanics/promotion-officer.html; C2's 24 core says when): the Works crew
// round the board for a quarter of an hour from simNote('promoted'); Tomas and Pell with your box by 4-23 from
// simNote('moveStart'); Tomas's goodbye once 4-23 is yours; the ceremony's seats (promoTick, each ship minute, from
// section 20's social tick). Live and once a day per step (PROMO_LIVE), except the seats, saved with the appointment
const PROMO_LIVE = new Set(), promoOnce = k => { const key = k + '@' + SHIP.time.day; if (PROMO_LIVE.has(key)) return false; PROMO_LIVE.add(key); return true; };
if (typeof onSim === 'function') {
  onSim('promoted', n => { const t = Number.isFinite(n && n.t) ? n.t : shipNow(); if (shipNow() - t <= 15 && promoOnce('gather')) worksGather(t + 15); });
  onSim('moveStart', n => { const t = Number.isFinite(n && n.t) ? n.t : shipNow(); if (shipNow() - t <= 45 && playerBed() !== '4-23' && promoOnce('box')) boxCarry(t + 45); });
}
function promoTick() {
  const day = SHIP.time.day;
  if (SHIP.time.min >= 420 && apptList().length && !PROMO_LIVE.has('seat@' + day) && ceremonySeat(day)) PROMO_LIVE.add('seat@' + day);
  if (!PROMO_LIVE.has('box@' + day) || typeof DECK_CREW === 'undefined') return;
  const pp = player.obj.position, near = id => { const a = DECK_CREW.find(x => x.p.id === id); return a && Math.hypot(a.x - pp.x, a.z - pp.z) < 4 ? a : null; };
  if (!PROMO_LIVE.has('boxsaid@' + day)) {             // Tomas or Pell says a word as you come up to them with the box
    const a = [near('tomas'), near('pell')].find(x => x && x.hold === 'carry');
    if (a && promoOnce('boxsaid')) { const l = socLine(a.p, 'work', { t: shipNow(), flags: { 'promo.box': true } }); if (l) bubbleSay(a.h, l.text, 5); }
  }
  const a = playerBed() === '4-23' && near('tomas');
  if (a && promoOnce('bye')) {                           // the box is in: Tomas's goodbye as a bunkmate, then off they go
    const l = socLine(a.p, 'work', { t: shipNow(), flags: { 'promo.bye': true } }); bubbleSay(a.h, l ? l.text : 'Don\'t be a stranger, Officer.', 6);
    for (const [id, tile] of [['tomas', [40, 14]], ['pell', [42, 14]]]) crewScene(id, { mode: 'wait', to: { deck: 4, tile }, until: shipNow() + 2 });
  }
}
// crewComeTo(p, placeId, onArrive, { until }) (Pillar 4: visits, friends walking over): a crew member walks to a
// place on the deck you're on (by lift if they're elsewhere), onArrive(agent) is called once when they get there, and
// at `until` (ship minutes; default an hour from now, never past 22:00, quiet hours) or when the returned function is
// called, they go back to their own plan. Live only: their plan on paper is unchanged and nothing is saved.
// p: a person or an id. Calling it again for the same person replaces the visit; placeId null ends it
const COME_TO = new Map();
function crewComeTo(p, placeId, onArrive, o = {}) {
  const id = p && (p.id || p); if (!id) return () => {};
  if (!placeId) { COME_TO.delete(id); return () => {}; }
  const now = shipNow(), quiet = (Math.floor(now / 1440)) * 1440 + 1320;
  const v = { placeId, onArrive: typeof onArrive === 'function' ? onArrive : null, until: Math.min(o.until != null ? o.until : now + 60, now < quiet ? quiet : now + 60), arrived: false };
  COME_TO.set(id, v);
  return () => { if (COME_TO.get(id) === v) COME_TO.delete(id); };
}
function comeWhere(p, t) {
  const v = COME_TO.size && COME_TO.get(p.id); if (!v) return null;
  if (t >= v.until) { COME_TO.delete(p.id); return null; }
  let N = null; try { N = deckDef.num; } catch (e) { return null; }
  return { deck: N, act: 'visit', type: null, placeId: v.placeId, moving: false, from: t - 1, until: v.until, tag: 'visit', visit: v };
}
// what someone carries (answer 23; the performance engineer draws it from the pose's '+hold'): what the job or plan
// says first (a cart, parts), else a toolbox for Works crew out on a job, a datapad for officers at the handover, on
// the Captain's walk or on a tea break. A meal's tray isn't planned: section 10 hands it over at the servery (mealStep)
const OFFICER_RANKS = new Set(['officer', 'senior', 'chief', 'xo', 'captain']);
function withHold(p, w, job) {
  if (!w || w.hold && !(job && (w.tag === 'load' || w.tag === 'unload'))) return w;   // at the hold or the shelves the crate is in their hands, not the cart (the reviewer's fix to 0.71.3, 0.71.5)
  const h = job && (w.tag === 'load' || w.tag === 'unload') ? 'carry'   // loading or unloading cargo: a crate in their hands (the user's playtest 2, 0.71.3)
    : job && p.dept === 'works' ? 'toolbox'
    : OFFICER_RANKS.has(p.rank) && (w.tag === 'handover' || w.tag === 'stroll' || w.tag === 'tea') ? 'datapad' : null;
  return h ? { ...w, hold: h } : w;
}
function planWhere(person, t) {
  const segs = planDay(person, Math.floor(t / 1440) + 1);
  let a = 0, b = segs.length - 1;
  while (a < b) { const m = (a + b + 1) >> 1; if (segs[m].from <= t) a = m; else b = m - 1; }
  const s = segs[a];
  return s ? { deck: s.deck, act: s.act, type: s.type, placeId: s.placeId, moving: s.act === 'commute', fromDeck: s.fromDeck, from: s.from, until: s.to, tag: s.tag, anim: s.anim } : null;
}
const schedPeople = () => schedData().people;
const peopleOn = (deck, t) => schedPeople().map(p => ({ p, w: whereIs(p, t) })).filter(x => x.w && x.w.deck === deck);
// step a whole day with no drawing: fn(t, [{ p, w }, ...]) every `step` ship minutes
function runDay(day, step = 1, fn) {
  const ppl = schedPeople();
  for (let t = (day - 1) * 1440; t < day * 1440; t += step) fn(t, ppl.map(p => ({ p, w: whereIs(p, t) })));
}
// what day_check.py checks, for one day: own-bed sleep in the 24 hours from 18:00 the evening before, meals,
// shift minutes worked, places held by two people at once, gaps in a plan, and how many people each deck holds
function dayReport(day) {
  const S = schedData(), B = (day - 1) * 1440, rep = { day, people: S.people.length, short: [], meals: [], work: [], double: [], gaps: [], unplaced: {}, peak: {} };
  for (const p of S.people) {
    if (!aboardAllDay(p, day) || !aboardAllDay(p, day - 1)) continue;   // a guest arriving, leaving or away: not a full day to judge
    const segs = planDay(p, day - 1).concat(planDay(p, day));
    let sleep = 0;
    for (const s of segs) if (s.act === 'sleep' && s.placeId === p.bed) sleep += Math.max(0, Math.min(s.to, B + 1080) - Math.max(s.from, B - 360));
    if (sleep < 360) rep.short.push(p.id + ' ' + sleep);
    const today = planDay(p, day);
    const meals = new Set(today.filter(s => s.act === 'breakfast' || s.act === 'dinner').map(s => s.act));
    if (meals.size < 2) rep.meals.push(p.id + ' ' + [...meals]);
    const gp = shiftBlocks(p, day), gb = gp && gp.blocks;
    if (gb || (isWorkDay(p, day) && !(galleyRotaOn() && p.dept === 'galley'))) {   // the whole shift worked (breaks and a galley staff meal count)
      const iv = gb ? gb.map(([a, b]) => [B + a, B + Math.min(b, 1440)]) : [p.shift === 'night' ? [B + 1260, B + 1440 + 360] : [B + SHIFTS.day[0], B + SHIFTS.day[1]]];
      const both = planDay(p, day).concat(planDay(p, day + 1)).filter(s => s.act === 'work' || ['tea', 'toilet', 'hands', 'staff', 'patrol', 'rush', 'round'].includes(s.tag) || /^intro/.test(s.tag || ''));   // an intro beat on shift is work too
      for (const [a, b] of iv) {
        const worked = both.reduce((n, s) => n + Math.max(0, Math.min(s.to, b) - Math.max(s.from, a)), 0);
        if (worked < b - a) rep.work.push(p.id + ' ' + worked + '/' + (b - a));
      }
    }
    for (let i = 0; i < today.length; i++) {
      const s = today[i];
      if (i ? s.from !== today[i - 1].to : s.from !== B) rep.gaps.push(p.id + '@' + s.from);
      if (!s.placeId && s.act !== 'commute' && s.tag !== 'queue') rep.unplaced[s.act] = (rep.unplaced[s.act] || 0) + 1;
    }
    if (!today.length || today[today.length - 1].to !== B + 1440) rep.gaps.push(p.id + ' end');
  }
  for (const [id, iv] of shipDay(day).occ) {
    const v = iv.slice().sort((x, y) => x[0] - y[0]);
    for (let i = 1; i < v.length; i++) if (v[i][0] < v[i - 1][1]) rep.double.push(id + '@' + v[i][0]);
  }
  // beds and work stations aren't in occ: a bed is only ever its owner's, and no two people work at one station
  // at the same time (desks are fixed per shift; the galley's stations are booked by its rota)
  const bedOf = new Map(), atWork = new Map();
  for (const p of S.people) for (const s of planDay(p, day)) if (s.placeId) {
    if (s.type === 'bed') {                              // a bed is its owner's: two people in it at once is wrong (a transfer hands it over on the day)
      const l = bedOf.get(s.placeId) || bedOf.set(s.placeId, []).get(s.placeId), o = l.find(x => x[2] !== p.id && x[0] < s.to && s.from < x[1]);
      if (o) rep.double.push(s.placeId + ' ' + o[2] + '/' + p.id); l.push([s.from, s.to, p.id]);
    }
    else if (s.act === 'work' && /^work:/.test(s.type)) (atWork.get(s.placeId) || atWork.set(s.placeId, []).get(s.placeId)).push([s.from, s.to, p.id]);
  }
  for (const [id, v] of atWork) { v.sort((x, y) => x[0] - y[0]); for (let i = 1; i < v.length; i++) if (v[i][0] < v[i - 1][1] && v[i][2] !== v[i - 1][2]) rep.double.push(id + ' ' + v[i - 1][2] + '/' + v[i][2] + '@' + hhmm(v[i][0] % 1440)); }
  for (let t = B; t < B + 1440; t += 5) {
    const n = {}; for (const p of S.people) { const w = planWhere(p, t); n[w.deck] = (n[w.deck] || 0) + 1; }
    for (const k in n) if (!rep.peak[k] || n[k] > rep.peak[k][0]) rep.peak[k] = [n[k], hhmm(t - B)];
  }
  return rep;
}
// sleeping (sleepUntil) and other jumps: plan the days you skip into, so arriving anywhere is instant
SIM_ADVANCE.push((from, to) => { shipDay(Math.floor(to / 1440) + 1); });

