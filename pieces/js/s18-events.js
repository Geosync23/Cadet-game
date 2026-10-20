// =====================================================================
// 18. SHIP EVENTS
// The ship's small traditions: quiz night, the music jam, observatory night, birthdays, the Sunday swap meet...
// To the player they're "ship traditions" (the user's name, 2026-10-16); the big story ones are "ship-wide events".
// Small, recurring and ambient. The crew who are free simply go; the player joins by being in the room.
//   SHIP_TRADITIONS        the table: when, the time, where (pools of places), who, what they do, the Mail and the tap lines
//   eventsOn(day)      -> [{ id, name, ev, day, from, to, honorees }] the events that day (minutes from midnight)
//   eventPlan(p, day)  -> [{ id, from, to, opts: [[deck, pool], ...], tag, anim, min }] what section 14 slots into
//                         that person's leisure time (minutes from midnight; [] most days). Read once per schedBuild
//   eventPools(shared) adds each event's pools ('deck|ev:<id>:<n>') to schedData's shared places (section 14 hook)
//   eventPlaces(e)     -> the place ids section 14 holds for the event's window (tagged, and `hold`: default the first pool)
//   eventLine(p, t)    -> a line for the tap toast ("Coming to the quiz tonight?"), or null
//   SHIP_EVENTS        the ship-wide events (Pillar 3), an object by id; see "ship-wide events" below
//   eventsTick()       the main loop: the Mail the evening before, decor on the deck during an event, the player joining
// Every choice is a hash (schedU, k 320-333: section 14 uses 500-515 and 9100/9200, section 16 301 and 310 up); nothing here calls R(), and nothing reads planDay or whereIs
// while plans are being made. Events only ever take leisure time: shifts, meals and sleep are untouched, and anyone
// who finds the room full just carries on with their evening.
// =====================================================================
const shipYearDay = d => (d - 1) % 364 + 1;                  // the ship's year: 52 weeks of 7 days, Day 1 a Monday
// when: { weekday } (0 = Monday) | { every, on } (days with d % every === on) | { yearDay } | { birthday: true }
// Pillar 4's rhythms (evDue): { every: 'week' | '2weeks' | '4weeks', weekday, week? } (week 1 = the cycle's first, counted
// from Day 1), { every: 'quarter', week, weekday } or { every: 'quarter', quarterDay }, { every: 'year', dayOfYear } or
// { every: 'year', week, weekday }, { after: 'arrival', days } (days after you came aboard; 0 = that day) or { after:
// 'arrival', weekday, nth? } (the nth such weekday after it; 1 = the first). Any of them may add season: 'sowing' | [..],
// from: day, until: day. Quarters and years start on Day 1 (a Monday), so nothing by quarter or year falls before it.
// at: [from, to] in minutes from midnight. where: [{ deck, pool } | { deck, room, types, ids? }, ...], best first;
// `room` is a regexp on the room's name, `types` the place types taken from it, `ids` an optional regexp on place ids,
// `who: 'officer'` keeps a pool to officers and up (Deck 1). Places tagged event: '<id>' come first, when there are any.
// who(p, d, ctx): the chance (0-1) a person who's free goes. anim(p): what they do there (an activity in 8b's ACTS),
// or null for the place's own pose. k: the event's own hash key (never reuse one). prio: the higher wins a clash.
// jitter: each person leaves up to that many minutes before `to`; early: the honorees come that much early.
// hold: the `where` entries whose places section 14 keeps for those going (default [0]; [] for none).
// cake: true asks the galley (section 16) to bake that day; its cake replaces our decor 'cake' prop.
// decor: props on the deck while it's on (eventDecor). mail: the evening before at 18:00 (text, from). ask: the tap
// line before it; here: the tap line during it; thanks: the toast when the player joins.
// invite (Pillar 4, for section 20's invitations): { host: crew id, odds: the chance that day that someone going asks
// you (the host first, when they're going), line: what they say }. Data only; section 20 decides who and when.
const SHIP_TRADITIONS = [
  // Gym club (0.34.51, was Running club; the id stays 'running' for the saves and the lines): every kind of machine,
  // and it always leaves two free (spare), so there's one for you; the player engineer makes you a member (section 15)
  { id: 'running', name: 'Gym club', k: 320, when: { weekday: 0 }, at: [1155, 1200], min: 20, spare: 2,
    where: [{ deck: 3, pool: 'gym' }],
    who: (p, d) => evHas(p, d, 'runner') ? .9 : evHas(p, d, 'gym-regular') ? .55 : .06, anim: () => null,
    from: 'Rina Deshi', mail: 'Gym club tomorrow at 19:15 in the gym. Every machine\'s in use, and there\'s always one for you. Soup after. That\'s the rule.',
    invite: { host: 'rina', odds: .3, line: 'Gym club after dinner. Come and grab a machine with us? Nobody gets left behind.' },
    ask: 'Gym club tonight. There\'s a machine with your name on it.', here: 'Swap with me after this one? I want the rower.', thanks: 'You join Gym club. Every machine is whirring, someone counts down the last minute, and there\'s soup after.' },   // the head writer's words (claude/writer-0607 c2b1b6a, trad-words/running.words)
  { id: 'observatory-night', name: 'Observatory night', k: 321, when: { weekday: 5 }, at: [1275, 1355], jitter: 30, min: 25,
    where: [{ deck: 2, room: /^Observatory$/, types: ['common-room', 'lounge-seat', 'bench'] }, { deck: 2, room: /^Chart room$/, types: ['common-room', 'lounge-seat'] },
      { deck: 2, room: /^Science corridor$/, types: ['bench'] }],
    who: (p, d) => evHas(p, d, 'stargazer') ? 1 : .3, anim: () => null,
    from: 'Dr. Imra Sato', mail: 'Observatory night tomorrow from 21:15, Deck 2. The scopes are open to everyone. Dress warm; the observatory never is.',
    invite: { host: 'sato', odds: .2, line: 'Observatory night, after nine. The nebula is showing off. Come up to Deck 2.' },
    ask: 'Observatory night later. Sato says the nebula is showing off.', here: 'Look at that. Never gets old.', thanks: 'You join the stargazers in the dark. Someone points out a pulsar.' },
  { id: 'quiz', name: 'Quiz night', k: 322, when: { weekday: 3 }, at: [1200, 1290], min: 25,
    where: [{ deck: 3, room: /^Bow lounge$/, types: ['lounge-seat'] }],
    host: 'tomas',   // 0.34.52: the question master always goes (he asks the quiz game's questions)
    who: (p, d) => p.id === 'tomas' ? 1 : evHas(p, d, 'bar-regular') ? .8 : evHas(p, d, 'lounge-regular') ? .7 : .25, anim: (p, d) => evHas(p, d, 'bar-regular') ? 'drink' : 'talk',
    from: 'Tomas Lind', mail: 'Quiz night tomorrow, 20:00 in the bow lounge. Teams of four. Question master: me. No looking things up on the ship\'s library, Survey.',
    invite: { host: 'tomas', odds: .5, line: 'Quiz tonight. We need someone who knows the engines. You in?' },
    ask: 'Coming to the quiz tonight? We need someone who knows the engines.', here: 'Shh, the next question is the tie-breaker.', thanks: 'You squeeze onto a quiz team. You get one right about the reactor, and the table cheers.' },
  { id: 'works-tea', name: 'Works Friday tea', k: 323, when: { weekday: 4 }, at: [1125, 1170], min: 20,
    where: [{ deck: 5, room: /^Tea corner$/, types: ['lounge-seat'] }, { deck: 5, room: /^(Works bay|Machine shop|Main storage)$/, types: ['work:works'], free: true }],
    who: (p, d) => p.dept === 'works' ? .8 : 0, anim: (p, d) => p.seed % 3 ? 'drink' : 'wash',
    from: 'Chief Ines Calder', mail: 'Friday tea in the Works bay after dinner: tools cleaned, the week\'s jobs off the board, and the good biscuits.',
    invite: { host: 'calder', odds: .4, line: 'Friday tea in the Works bay after dinner. You\'re Works now; that means you.' },
    ask: 'Friday tea after dinner. Bring your spanners; they need a wipe.', here: 'Pass the rag. And a biscuit.', thanks: 'You wipe down tools with the Works crew over tea. Calder nods at the clean board.' },
  { id: 'jam', name: 'Music jam', k: 324, when: { weekday: 4 }, at: [1185, 1275], min: 25,
    where: [{ deck: 4, pool: 'music' }],
    who: (p, d) => evHas(p, d, 'musician') ? .95 : evHas(p, d, 'music') ? .65 : .04, anim: (p, d) => evHas(p, d, 'musician') ? 'play' : null,
    from: 'The music room', mail: 'Friday jam tomorrow from 19:45 in the music room, Deck 4. Bring an instrument, or just your ears.',
    ask: 'Jam in the music room tonight. Come and listen.', here: 'This is the good bit.', thanks: 'You sit in on the Friday jam. Somebody hands you a tambourine.' },
  { id: 'film', name: 'Film night', k: 325, when: { weekday: 5 }, at: [1200, 1320], min: 30, unflag: 'rec.filmMoved',   // 0.83.2 (RA): to the rec deck's auditorium (rec-film) once the first all-hands is held
    where: [{ deck: 4, pool: 'common-room' }],
    who: (p, d) => p.rank !== 'junior' ? 0 : evHas(p, d, 'common-room') ? .8 : .3, anim: () => null,
    from: 'Pell Okafor', mail: 'Film night tomorrow, 20:00 in the junior common room. It\'s my turn to choose, so: the one with the space whales again.',
    invite: { host: 'pell', odds: .4, line: 'Film night. Space whales, again. Save me from watching it alone?' },
    ask: 'Film night later. Pell picked the space whales one again.', here: 'Shh. This is the whale bit.', thanks: 'You find a spot for film night. The space whales are as good as Pell said.' },
  { id: 'market', name: 'Sunday swap meet', k: 326, when: { weekday: 6 }, at: [630, 750], min: 20,
    where: [{ deck: 3, room: /^Promenade$/, types: ['bench'] }, { deck: 3, room: /^Lift plaza$/, types: ['bench'] }],
    who: (p, d) => evHas(p, d, 'shopper') ? .8 : .22, anim: () => 'talk', decor: 'stalls',
    from: 'The crew store', mail: 'Sunday swap meet on the promenade tomorrow, 10:30 to 12:30. Bring what you don\'t need; take what you do.',
    ask: 'Swap meet on Sunday. I\'m trading my spare socks for anything.', here: 'Anyone want a slightly used chess set?', thanks: 'You browse the swap meet stalls and come away with a slightly bent paperback.' },
  { id: 'harvest', name: 'Harvest morning', k: 327, when: { every: 14, on: 6 }, at: [570, 690], min: 25,
    where: [{ deck: 3, pool: 'garden-tend' }, { deck: 3, pool: 'garden' }],
    who: (p, d) => evHas(p, d, 'gardener') ? .95 : evHas(p, d, 'garden-lover') ? .8 : .12, anim: () => 'water',
    from: 'Chef Auda Brennan', mail: 'Harvest morning in the hydroponics garden tomorrow, 09:30. Many hands, quick picking. Fresh salad with dinner.',
    invite: { host: 'brennan', odds: .3, line: 'Harvest in the garden at half nine. Many hands, quick picking. Coming?' },
    ask: 'Harvest in the garden this morning. Fresh salad tonight.', here: 'These tomatoes are huge this time.', thanks: 'You help pick the harvest. Your hands smell of tomato leaves all morning.' },
  { id: 'birthday', name: 'Birthday', k: 328, when: { birthday: true }, at: [1215, 1270], jitter: 15, early: 5, min: 20, prio: 2,
    where: [{ deck: 3, room: /^Mess hall$/, types: ['mess-seat'], ids: /^3-mess-([1-9]|1[0-6])$/ }, { deck: 3, pool: 'mess-seat' }, { deck: 3, pool: 'lounge-seat' }, { deck: 3, pool: 'bench' }],
    who: (p, d, c) => c.honorees.includes(p) ? 1 : c.honorees.some(h => h.dept === p.dept) ? .8 : c.honorees.some(h => bedRoom(h) === bedRoom(p)) ? .7 : .45,
    anim: () => 'talk', decor: 'cake', cake: true,
    from: 'Matthias Oduya', mail: c => 'Tomorrow is ' + c.names + '\'s birthday. Chef Brennan is baking; cake in the mess hall at 20:15.',
    ask: c => 'Cake in the mess at quarter past eight, for ' + c.names + '.', here: c => 'Happy birthday, ' + c.first + '!', thanks: c => 'You join the birthday table and sing for ' + c.names + '. The cake is lemon.' },
  { id: 'hull-lights', name: 'Hull-lights evening', k: 329, when: { every: 28, on: 24 }, at: [1260, 1320], min: 25, hold: [],
    where: [{ deck: 3, room: /^Bow lounge$/, types: ['lounge-seat'] }, { deck: 1, room: /^Observation room$/, types: ['common-room', 'lounge-seat'], who: 'officer' },
      { deck: 3, room: /^Promenade$/, types: ['bench'] }],
    who: () => .4, anim: () => null,
    from: 'Commander Teo Vance', mail: 'Hull-lights evening tomorrow at 21:00: the running lights cycle through every colour they have. Best seen from the bow lounge windows.',
    ask: 'Hull lights tonight. The bow windows are the best seats.', here: 'There goes the green. My favourite.', thanks: 'You watch the hull lights run through their colours from the window.' },
  { id: 'founding', name: 'Founding Day', k: 330, when: { yearDay: 100 }, at: [1170, 1290], min: 30, prio: 3, hold: [],
    where: [{ deck: 3, pool: 'mess-seat' }, { deck: 3, room: /^Bow lounge$/, types: ['lounge-seat'] }],
    who: () => .85, anim: () => 'talk', decor: 'cake', cake: true,
    from: 'Captain Odile Marrow', mail: 'Tomorrow is the Wren\'s Founding Day. Everyone off duty to the mess hall at 19:30 for cake and a few words. I promise to keep them few.',
    ask: 'Founding Day! Cake in the mess at half seven.', here: 'To the Wren.', thanks: 'You raise a cup in the mess hall. To the Wren.' },
  { id: 'quiet-watch', name: 'The quiet watch', k: 331, when: { yearDay: 300 }, at: [1290, 1335], min: 25, hold: [],
    where: [{ deck: 1, room: /^Observation room$/, types: ['common-room', 'lounge-seat'], who: 'officer' }, { deck: 2, room: /^Observatory$/, types: ['common-room'] },
      { deck: 3, room: /^Bow lounge$/, types: ['lounge-seat'] }],
    who: () => .55, anim: () => null,
    from: 'Matthias Oduya', mail: 'The quiet watch is tomorrow evening at 21:30: a little while at the windows for the people we miss. Come if you like; nobody needs to say anything.',
    ask: 'The quiet watch is tonight. I\'ll be at the bow windows.', here: '...', thanks: 'You sit quietly at the window with the others for a while.' },
];
const evHas = (p, d, h) => (typeof habitsOn === 'function' ? habitsOn(p, d) || [] : p.habits || []).includes(h);   // habits change over time (section 14)
const bedRoom = p => String(p.bed).replace(/-\d+$/, '');   // '4-B1-2' -> '4-B1': bunkmates
const evText = (x, c, p) => typeof x === 'function' ? x(c, p) : x;   // p: the person speaking (tap lines), when there is one
// the ship's year has four seasons of 13 weeks, named for the garden (Pillar 4): season(d) -> 'sowing' | 'greening' |
// 'harvest' | 'lanterns'; seasonOf(d) -> { id, name, day (1-91), week (1-13) }. Day 0 (your arrival) is Lanterns' last
const SEASONS = [{ id: 'sowing', name: 'Sowing' }, { id: 'greening', name: 'Greening' }, { id: 'harvest', name: 'Harvest' }, { id: 'lanterns', name: 'Lanterns' }];
const evYearDay = d => ((d - 1) % 364 + 364) % 364 + 1;   // like shipYearDay, and right for day 0 too
function seasonOf(d) { const yd = evYearDay(d), q = Math.floor((yd - 1) / 91), qd = yd - q * 91; return { ...SEASONS[q], day: qd, week: Math.floor((qd - 1) / 7) + 1 }; }
const season = d => SEASONS[Math.floor((evYearDay(d) - 1) / 91)].id;
// the day you came aboard: section 21's when it's in (Pillar 4), else day 0 (a new game starts the evening before Day 1)
const evArrival = () => typeof introArrival === 'function' ? introArrival() : 0;
const EV_CYCLE = { week: 1, '2weeks': 2, '4weeks': 4 };
// crew rotation days (Pillar 4; the crew designer's ROSTER_ROTATIONS, the Sunday shuttle): when.rotation = n (n days
// from a rotation day: before it the leavers are honoured, from it on the arrivals) or 'after' with a weekday (the first
// such day after it: the arrivals). -> the honoured ids that day, or null (pure)
function evRotation(w, d) {
  let rots; try { rots = ROSTER_ROTATIONS; } catch (e) { return null; }   // the roster loads after us
  for (const r of rots || []) {
    if (w.rotation === 'after' ? d > r.day && d - r.day <= 7 && weekday(d) === w.weekday : d === r.day + w.rotation) return w.rotation !== 'after' && w.rotation < 0 ? r.out : r.in;
  }
  return null;
}
function evDue(w, d) {
  if (w.from != null && d < w.from || w.until != null && d > w.until) return false;
  if (w.season && ![].concat(w.season).includes(season(d))) return false;
  const wd = weekday(d), yd = shipYearDay(d);
  if (w.rota) return !!(TRAD_ROTA[w.rota] && TRAD_ROTA[w.rota](d));   // 0.83 (RA): a rota the game keeps (the Wren talks)
  if (w.after) {                                         // personal: counted from the day you arrived
    const a = w.after === 'arrival' ? evArrival() : null; if (a == null || d < a) return false;
    if (w.days != null) return d === a + w.days;
    return d > a && wd === w.weekday && Math.ceil((d - a) / 7) === (w.nth || 1);
  }
  if (typeof w.every === 'string') {
    const wk = Math.floor((d - 1) / 7), n = EV_CYCLE[w.every];
    if (n) return [].concat(w.weekday).includes(wd) && (wk % n + n) % n + 1 === (w.week || 1);
    if (d < 1) return false;
    if (w.every === 'quarter') { const qd = (yd - 1) % 91 + 1; return w.quarterDay != null ? qd === w.quarterDay : wd === w.weekday && Math.floor((qd - 1) / 7) + 1 === (w.week || 1); }
    if (w.every === 'year') return w.dayOfYear != null ? yd === w.dayOfYear : wd === w.weekday && Math.floor((yd - 1) / 7) + 1 === (w.week || 1);
    return false;
  }
  return [].concat(w.weekday).includes(wd) || (w.every && d % w.every === w.on) || w.yearDay === yd;   // weekday: one or a list
}
// The loader (Pillar 4): each baked tradition becomes a SHIP_TRADITIONS entry (one with the same id is replaced), so the
// tradition designers' .trad files (content/traditions) need no code. content_gen.py (the dialogue engineer's) bakes
// them into TRADITIONS { id: tradition } in section 22's generated block, each field through plans/trad_parse.py's
// parse_field (the grammar: plans/trad-format.md). Rules are data:
// who: [[cond, chance], ...] and anim: 'act' | [[cond, act], ...], the first cond that holds wins (who: else 0). A cond
// is words joined by '+' (all must hold): everyone, host, honoree, juniors, officers, friends-of-host, friends-of-honoree,
// dept-of-honoree, bunk-of-honoree, night-shift,
// day-shift (or shift:<x>), a crew id, a
// department, a habit, or id:/dept:/habit:/rank:<x>. Texts: text.<kind> = [{ text, tone? }] (mail, ask, here, thanks,
// chatter), one picked per person and day; placeholders {trad} {host} {names} {first} {season} {weekday} {time}; a
// line whose placeholder can't be filled is skipped. TRAD_ERRORS lists what didn't load or resolve (events_check reads it)
const TRAD_ERRORS = [];
const TRAD_WORDS = new Map();                            // a bare word's meaning, worked out once (the roster loads after us)
function tradWord(w) {
  if (TRAD_WORDS.has(w)) return TRAD_WORDS.get(w);
  let r = null; const m = /^(id|dept|habit|rank):(.+)$/.exec(w);
  if (m) r = [m[1], m[2]];
  else if (schedPeople().some(p => p.id === w)) r = ['id', w];
  else if (schedPeople().some(p => p.dept === w)) r = ['dept', w];
  else if (typeof HABITS !== 'undefined' && HABITS[w]) r = ['habit', w];
  if (!r) TRAD_ERRORS.push('unknown word "' + w + '"');
  TRAD_WORDS.set(w, r); return r;
}
function tradIs(cond, p, d, c, host) {
  return cond.split('+').every(w => {
    if (w === 'everyone') return true;
    if (w === 'host') return !!host && p.id === host;
    if (w === 'honoree') return !!(c && c.honorees && c.honorees.includes(p));
    if (w === 'juniors') return p.rank === 'junior';
    if (w === 'officers') return p.rank !== 'junior' && p.rank !== 'guest';
    if (w === 'night-shift' || w === 'day-shift') return (p.shift === 'night') === (w === 'night-shift');
    if (/^shift:/.test(w)) return p.shift === w.slice(6);
    if (/-of-honoree$/.test(w)) { const hs = c && c.honorees || []; if (!hs.length || hs.includes(p)) return false;   // a birthday's or a rotation's people
      return w === 'dept-of-honoree' ? hs.some(h => h.dept === p.dept) : w === 'bunk-of-honoree' ? hs.some(h => bedRoom(h) === bedRoom(p))
        : w === 'friends-of-honoree' && typeof affinityPlan === 'function' && hs.some(h => affinityPlan(h.id, p.id, d) >= 40); }
    if (w === 'friends-of-host') return !!host && host !== p.id && typeof affinityPlan === 'function' && affinityPlan(host, p.id, d) >= 40;   // pure: plans never read live state
    const r = tradWord(w); if (!r) return false;
    return r[0] === 'id' ? p.id === r[1] : r[0] === 'dept' ? p.dept === r[1] : r[0] === 'rank' ? p.rank === r[1] : evHas(p, d, r[1]);
  });
}
const tradRule = (rules, p, d, c, host, none) => { for (const [cond, v] of rules) if (tradIs(cond, p, d, c, host)) return v; return none; };
const evFirst = name => name.split(' ').slice(-2)[0];   // 'Chef Auda Brennan' -> 'Auda'
function tradFill(text, t, c, p) {
  let ok = true;
  const hs = c && c.honorees && p ? c.honorees.filter(h => h !== p) : [];   // {first}: with several honorees, each speaker names one of them (by hash)
  const first = hs.length && c.honorees.length > 1 ? evFirst(hs[Math.floor(schedU(p.seed + 104729, c.day, t.k) * hs.length)].name) : c && c.first;
  const out = text.replace(/\{(\w+)\}/g, (all, k) => {
    const h = t.host && schedPeople().find(p => p.id === t.host);
    const v = k === 'trad' ? t.name : k === 'host' ? h && evFirst(h.name) : k === 'names' ? c && c.names : k === 'first' ? first
      : k === 'season' ? c && seasonOf(c.day).name : k === 'weekday' ? c && WEEKDAYS[weekday(c.day)] : k === 'time' ? c && hhmm(c.from) : null;
    if (!v) ok = false; return v || '';
  });
  return ok ? out : null;
}
function tradText(t, kind, c, p) {
  const self = p ? p.name.split(' ').slice(-2).map(w => new RegExp('\\b' + w + '\\b')) : [];   // nobody talks about themselves by name
  const l = ((t.text || {})[kind] || []).map(x => tradFill(typeof x === 'string' ? x : x.text || x.t || '', t, c, p)).filter(x => x && !self.some(r => r.test(x)));
  return l.length ? l[Math.floor(schedU((p ? p.seed : 0) + 7919, c ? c.day : 0, t.k) * l.length)] : null;   // per person and day
}
function tradLoad(t) {
  if (!t || typeof t.id !== 'string' || !Number.isInteger(t.k) || !t.when || !Array.isArray(t.at) || !Array.isArray(t.where) || !t.where.length || !Array.isArray(t.who)) {
    TRAD_ERRORS.push('tradition ' + (t && t.id) + ' is missing id, k, when, at, where or who'); return null;
  }
  const has = kind => !!((t.text || {})[kind] || []).length;
  let checked = false;
  const words = () => { if (checked) return; checked = true; for (const [c] of t.who.concat(Array.isArray(t.anim) ? t.anim : [])) for (const w of c.split('+')) if (!/^(everyone|host|honoree|juniors|officers|friends-of-host|(friends|dept|bunk)-of-honoree|night-shift|day-shift|shift:.+)$/.test(w)) tradWord(w); };
  return {
    id: t.id, name: t.name || t.id, k: t.k, when: t.when, at: t.at.slice(), min: t.min || 20, prio: t.prio || 0, jitter: t.jitter || 0, early: t.early || 0,
    hold: t.hold, cake: !!t.cake, decor: t.decor || null, host: t.host || null, ties: t.ties || null, invite: t.invite || null, trace: t.trace || null, meal: t.meal || null, flag: t.flag || null, text: t.text || {}, baked: true,
    wake: t.wake, afterShift: !!t.afterShift, spare: t.spare, venue: t.venue || null,   // 0.34.51: early mornings, straight from shift, places left free
    unflag: t.unflag || null, stay: Array.isArray(t.stay) ? t.stay.slice() : null, quiet: t.quiet || null,   // 0.83 (RA): until a flag, drifting in and out, no Mail on the career's big days
    where: t.where.map(w => w.room ? { ...w, room: new RegExp(w.room), ids: w.ids ? new RegExp(w.ids) : undefined } : { ...w }),
    who: (p, d, c) => { words(); return tradRule(t.who, p, d, c, t.host, 0); },
    anim: (p, d) => typeof t.anim === 'string' ? t.anim : Array.isArray(t.anim) ? tradRule(t.anim, p, d, null, t.host, null) : null,
    get from() { const p = t.from && schedPeople().find(q => q.id === t.from); return p ? p.name : t.from || 'The Wren'; },
    mail: has('mail') ? c => tradText(t, 'mail', c) : null, ask: has('ask') ? (c, p) => tradText(t, 'ask', c, p) : null,
    here: has('here') ? (c, p) => tradText(t, 'here', c, p) : null, thanks: c => tradText(t, 'thanks', c) || 'You join in for a while.',
    chatter: (c, p) => tradText(t, 'chatter', c, p),
  };
}
// ---- the rec deck's traditions (RA, 0.83.x; plans/rec-traditions-plan.html FINAL on claude/p5-design; brief-recdeck R11) ----
// Hand-written here with stand-in words, so the rules live in one place; the writer's content/traditions/<id>.trad with
// the same id (and the same rules) replaces each one's words when it's baked. Only with REC_DECK on. Hash keys k 486-499
// (486-491 weekly, 492-499 the rest). They're budgeted among themselves (evBudget): one at a time in a room, and never
// moving one of the ship's other traditions. REC_BIG: the career's big days and the storm (days after you arrive, the
// traditions plan's skips): no talk then, and the weekly sport ones send no Mail nudge (quiet: 'career')
const REC_BIG = [1, 4, 5, 9, 10, 11, 15, 16, 22, 23, 26];
const recBigDay = d => REC_BIG.includes(d - evArrival());
const TRAD_ROTA = {};                                     // when: { rota: name } -> TRAD_ROTA[name](d) (the Wren talks)
// the Wren talks (the traditions plan's rota): small chats Mondays and Thursdays 19:00-19:40 in a ring of chairs on the stage,
// a chief's talk every two weeks on a Thursday (from Day 18) 19:00-19:45 in the seats, and Day 8's one-off big Monday
// (Sato, after the creature). None on REC_BIG days. Days after you arrive. Lead 17's call 4: the engine, and the rota's
// first four talks for now; the rest of the rota (later: true) comes with its words. recTalk(d) -> { size, by, title } | null
const REC_TALKS = [
  [8, 'chief', 'sato', 'What lives between the stars'], [18, 'chief', 'calder', 'The Wren\'s first refit'], [25, 'small', 'tomas', 'Reading a route'],
  [29, 'small', 'esposito-yara', 'Where every crate goes'],
  [32, 'chief', 'holt', 'The oldest log in the Watch office', true], [36, 'small', 'volkov-maeve', 'How the float room floats', true],
  [39, 'small', 'torres-zeke', 'How a drive coil sings', true], [43, 'small', 'brennan', 'A spice for every port', true], [46, 'chief', 'ferreira', 'Messages that came home late', true],
];
function recTalk(d) {
  if (typeof SHIP !== 'undefined' && SHIP.rec && SHIP.rec.talk.mine === d) return { size: 'small', by: 'you', title: 'What I learned in my first month' };   // yours (recMyTalk)
  const n = d - evArrival(), r = REC_TALKS.find(x => x[0] === n && !x[4]);
  return r && schedPeople().some(p => p.id === r[2]) ? { size: r[1], by: r[2], title: r[3] } : null;
}
TRAD_ROTA['wren-small'] = d => { const t = recTalk(d); return !!t && t.size === 'small'; };
TRAD_ROTA['wren-chief'] = d => { const t = recTalk(d); return !!t && t.size === 'chief'; };
const recSpeaker = (p, d) => { const t = recTalk(d); return !!t && t.by === p.id; };
const recIs = (p, d, h) => evHas(p, d, h);
const REC_TRADS = [
  { id: 'rec-wso', name: 'Winner Stays On', k: 486, when: { weekday: 6, from: 7 }, at: [690, 990], min: 30, stay: [40, 120], hold: [2],
    where: [{ deck: 7, pool: 'rec-stand' }, { deck: 7, pool: 'lounge-seat' }, { deck: 7, pool: 'rec:disc' }], host: 'pell',   // the court itself held for it (nobody's pick-up game), its players put there by wsoWhere
    whereFor: (p, d, o) => o.filter(([, k]) => k !== 'rec:disc'),
    who: (p, d) => p.id === 'pell' ? 1 : recIs(p, d, 'disc-player') ? .9 : recIs(p, d, 'film-buff') ? .55 : .45, anim: () => 'cheer',
    from: 'Pell Okafor', mail: 'Winner Stays On tomorrow, 11:30 to 16:30 on the Lightdisc court. Chalk your name on the board by the gate. I\'ll be on. I\'m always on.',
    ask: 'Winner Stays On today. My name\'s already on the board.', here: 'Next! Who\'s next?', thanks: 'You find a spot in the stands for Winner Stays On. Pell rings his hand bell for every new game.' },
  { id: 'rec-dawn-swim', name: 'Dawn swim', k: 488, when: { weekday: [1, 3], from: 2 }, at: [375, 405], min: 20, wake: 15, quiet: 'career',
    where: [{ deck: 7, pool: 'rec:lane' }, { deck: 7, pool: 'rec:poolq' }], host: 'rina',
    who: (p, d) => p.id === 'rina' ? 1 : recIs(p, d, 'swimmer') ? .85 : recIs(p, d, 'early-riser') ? .5 : .03, anim: () => null,
    from: 'Rina Deshi', mail: 'Dawn swim tomorrow, 06:15 in the rec dec pool. Before the infirmary opens. The water\'s warm; getting in is the hard part.',
    ask: 'Dawn swim in the morning? Before the infirmary opens.', here: 'Two more lengths. Then breakfast.', thanks: 'You swim a few lengths with Rina while the stars slide past the hull windows.' },
  { id: 'rec-paddle-club', name: 'Paddle club', k: 489, when: { weekday: 2, from: 3 }, at: [1110, 1170], min: 25, quiet: 'career',
    where: [{ deck: 7, pool: 'rec:kayak' }, { deck: 7, pool: 'rec:kayakq' }], host: 'holt',
    who: (p, d) => p.id === 'holt' ? 1 : recIs(p, d, 'kayaker') ? .8 : .04, anim: () => null,
    from: 'Chief Bram Holt', mail: 'Paddle club tomorrow, 18:30 in the river hall. The slow loop first. Helmets on. Yes, you.',
    ask: 'Paddle club tonight. Holt counts the helmets.', here: 'Lean into it. Don\'t fight the water.', thanks: 'You paddle the slow loop with Paddle club while Chief Holt watches the water like a hawk.' },
  { id: 'rec-wall-night', name: 'Wall night', k: 491, when: { weekday: 1, from: 2 }, at: [1110, 1185], min: 25, quiet: 'career',
    where: [{ deck: 7, pool: 'rec:climb' }, { deck: 7, pool: 'rec:climbq' }], host: 'tomas',
    who: (p, d) => p.id === 'tomas' ? 1 : recIs(p, d, 'climber') ? .85 : .05, anim: () => null,
    from: 'Tomas Lind', mail: 'Wall night tomorrow, 18:30 at the climbing wall. I\'ll belay. Ring the bell and your name goes on the season\'s board.',
    ask: 'Wall night later. Ring the bell and you\'re on the board.', here: 'Left foot. No, your other left.', thanks: 'You climb at Wall night with Tomas on the rope. The bell rings out across the river hall.' },
  { id: 'rec-float-hour', name: 'Float hour', k: 492, when: { weekday: 2, from: 3 }, at: [1290, 1335], min: 20, quiet: 'career',
    where: [{ deck: 7, pool: 'rec:float' }, { deck: 7, pool: 'rec:floatq' }], host: 'oduya',
    who: (p, d) => p.id === 'oduya' ? 1 : recIs(p, d, 'floater') ? .85 : .04, anim: () => null,
    from: 'Matthias Oduya', mail: 'Float hour tomorrow, 21:30 in the float room. The orbs go down, the music goes on, and nobody talks. You\'ll sleep better.',
    ask: 'Float hour tonight. No talking. That\'s the whole point.', here: '...', thanks: 'You drift in the dimmed float room with quiet music. Nobody says a word, and it\'s lovely.' },
  { id: 'rec-slow-stretch', name: 'Slow stretch', k: 493, when: { weekday: 6, from: 7 }, at: [480, 525], min: 20, wake: 15, quiet: 'career', spare: 0,
    where: [{ deck: 7, pool: 'rec:float' }], host: 'nandakumar',
    who: (p, d) => p.id === 'nandakumar' ? 1 : recIs(p, d, 'floater') ? .75 : recIs(p, d, 'early-riser') ? .3 : .08, anim: () => null,
    from: 'Dr. Priya Nandakumar', mail: 'Slow stretch tomorrow, 08:00 in the float room: a gentle stretch at a fifth of a g. Doctor\'s orders, and the doctor\'s coming.',
    ask: 'Slow stretch in the morning? At a fifth of a g, even I can touch my toes.', here: 'Slower. Slower still.', thanks: 'You stretch slowly at a fifth of a g with Dr. Nandakumar. Your back thanks you all day.' },
  // every four weeks (0.83.2): the regatta (from Day 21), talent night (from Day 14), the Lightdisc Cup (from Day 28, in
  // Winner Stays On's place: the higher prio wins the court)
  { id: 'rec-regatta', name: 'River regatta', k: 490, when: { every: '4weeks', weekday: 6, week: 3 }, at: [570, 660], min: 30, hold: [], prio: 1,
    venue: 'river-banks', where: [{ deck: 7, pool: 'rec:kayak' }, { deck: 7, pool: 'rec:kayakq' }], host: 'holt',
    whereFor: (p, d, o) => regattaPaddler(p, d) ? o.filter(([, k]) => k !== 'ev:rec-regatta').concat(o.filter(([, k]) => k === 'ev:rec-regatta')) : o.filter(([, k]) => k === 'ev:rec-regatta'),   // the kayakers paddle the heats, everyone else watches from the banks
    who: (p, d) => p.id === 'holt' ? 1 : recIs(p, d, 'kayaker') ? .9 : .3, anim: () => 'cheer',
    from: 'Chief Bram Holt', mail: 'The river regatta tomorrow, 09:30 in the river hall. Heats of four round the loop; I start each one with the horn. Watch from the bank, or paddle the fun heat.',
    ask: 'Regatta this morning. Holt\'s got the horn.', here: 'Go on! Paddle!', thanks: 'You cheer from the bank as the heats race round the loop. Holt\'s horn makes everyone jump.' },
  { id: 'rec-talent-night', name: 'Talent night', k: 497, when: { every: '4weeks', weekday: 6, week: 2 }, skip: d => Math.abs(shipYearDay(d) - 152) < 7, at: [1170, 1290], min: 40, hold: [], prio: 1,   // skip: never within a week of the yearly one (lead 18)
    where: [{ deck: 7, pool: 'rec-aud' }, { deck: 7, pool: 'rec:act' }, { deck: 7, pool: 'rec:booth' }, { deck: 7, pool: 'rec:lectern' }], host: 'ferreira',
    whereFor: (p, d, o) => o.filter(([, k]) => p.id === 'volkov-maeve' ? k === 'rec:booth' : p.id === 'ferreira' ? k === 'rec:lectern' : recIs(p, d, 'musician') ? k === 'rec:act' || k === 'rec-aud' : k === 'rec-aud'),
    who: (p, d) => p.id === 'ferreira' || p.id === 'volkov-maeve' ? 1 : recIs(p, d, 'musician') ? .85 : recIs(p, d, 'film-buff') ? .7 : .4, anim: p => p.id === 'volkov-maeve' ? null : 'clap',
    from: 'Comms Chief Lucia Ferreira', mail: 'Talent night tomorrow, 19:30 in the auditorium. Songs, the piano, a juggling Works tech, and whoever\'s brave. Sign up on the sheet in the foyer.',
    ask: 'Talent night tonight! The sign-up sheet\'s nearly full.', here: 'Give them a big hand!', thanks: 'You find a seat for talent night. Every act gets a cheer, even the one that goes wrong.' },
  { id: 'rec-cup', name: 'Lightdisc Cup', k: 487, when: { every: '4weeks', weekday: 6, week: 4 }, at: [690, 990], min: 30, stay: [60, 150], hold: [2], prio: 2,
    where: [{ deck: 7, pool: 'rec-stand' }, { deck: 7, pool: 'lounge-seat' }, { deck: 7, pool: 'rec:disc' }], host: 'pell',
    whereFor: (p, d, o) => o.filter(([, k]) => k !== 'rec:disc'),
    who: (p, d) => p.id === 'pell' ? 1 : recIs(p, d, 'disc-player') ? .95 : .5, anim: () => 'cheer',
    from: 'Pell Okafor', mail: 'The Lightdisc Cup tomorrow, 11:30 on the court, instead of Winner Stays On. Every department sends its best. Enter at the gate.',
    ask: 'Cup day! Works has to beat the Watch this time.', here: 'That was in! That was IN!', thanks: 'You squeeze into the stands for the Cup. The department songs are louder than the games.' },
  // Saturdays: film night in the auditorium, once it has moved (flag rec.filmMoved, set by the first Captain's all-hands)
  { id: 'rec-film-night', name: 'Film night', k: 496, when: { weekday: 5 }, at: [1200, 1335], min: 30, flag: 'rec.filmMoved',
    where: [{ deck: 7, pool: 'rec-aud' }], host: 'pell',
    who: (p, d) => recIs(p, d, 'film-buff') ? .9 : p.rank === 'junior' ? (evHas(p, d, 'common-room') ? .8 : .35) : .2, anim: () => null,
    from: 'Pell Okafor', mail: 'Film night tomorrow, 20:00 in the auditorium on the big screen. Popcorn from the galley. My pick, so: whales.',
    ask: 'Film night in the auditorium. A screen that big!', here: 'Shh. This is the good bit.', thanks: 'You take a violet seat for film night. The screen comes down over the stars and the house lights go out.' },
  // the Captain's all-hands: the first Monday of each season, once the first has been held (with the first ship-wide event)
  { id: 'rec-all-hands', name: 'Captain\'s all-hands', k: 498, when: { every: 'quarter', week: 1, weekday: 0 }, at: [1065, 1090], min: 20, flag: 'rec.allHands', prio: 3, hold: [],
    where: [{ deck: 7, pool: 'rec:lectern' }, { deck: 7, pool: 'rec-aud' }], host: 'marrow',
    whereFor: (p, d, o) => o.filter(([, k]) => (p.id === 'marrow' || p.id === 'vance') === (k === 'rec:lectern')),
    who: (p, d) => p.id === 'marrow' || p.id === 'vance' ? 1 : p.rank === 'guest' ? 0 : .95, anim: () => null,
    from: 'Captain Odile Marrow', mail: 'All hands tomorrow at 17:45 in the auditorium: the season ahead, and a few thank-yous. Dinner straight after.',
    ask: 'All-hands before dinner. The Captain\'s doing the season.', here: 'Shh, she\'s starting.', thanks: 'You find a seat for the all-hands. The Captain looks round the room, and a few names get called out.' },
  // the Wren talks (TRAD_ROTA above): the small ones in the ring on the stage, the chiefs' in the seats with the speaker on the stool
  { id: 'rec-wren-talk', name: 'Wren talk', k: 494, when: { rota: 'wren-small' }, at: [1140, 1180], min: 25,
    where: [{ deck: 7, pool: 'rec-ring' }], spare: 1, first: (p, d) => recSpeaker(p, d),
    who: (p, d) => recSpeaker(p, d) ? 1 : p.rank === 'junior' ? .14 : .08, anim: () => 'talk',
    from: 'The Wren talks', mail: c => { const t = recTalk(c.day), q = t && schedPeople().find(p => p.id === t.by); return q ? 'A Wren talk tomorrow at 19:00, on the auditorium stage: ' + shortName(q) + ', "' + t.title + '". Tea from the kettle. Anyone can ask anything.' : 'A Wren talk tomorrow at 19:00 on the auditorium stage.'; },
    ask: 'Coming to the talk tonight? On the stage, with tea.', here: 'Ooh, good question.', thanks: 'You pull up a chair in the ring on the stage. The talk is easy and the tea is hot.' },
  { id: 'rec-chiefs-talk', name: 'Chief\'s talk', k: 495, when: { rota: 'wren-chief' }, at: [1140, 1185], min: 30, prio: 1,
    where: [{ deck: 7, pool: 'rec:stool' }, { deck: 7, pool: 'rec-aud' }],
    whereFor: (p, d, o) => o.filter(([, k]) => recSpeaker(p, d) === (k === 'rec:stool')),
    who: (p, d) => recSpeaker(p, d) ? 1 : p.rank === 'guest' ? 0 : .5, anim: () => null,
    from: 'The Wren talks', mail: c => { const t = recTalk(c.day), q = t && schedPeople().find(p => p.id === t.by); return q ? 'A chief\'s talk tomorrow at 19:00 in the auditorium: ' + shortName(q) + ', "' + t.title + '". About twenty-five minutes, then questions.' : 'A chief\'s talk tomorrow at 19:00 in the auditorium.'; },
    ask: 'The chief\'s talk tonight. Everyone\'s going.', here: 'Shh. This is the best bit.', thanks: 'You find a seat for the chief\'s talk. The house lights are half up, and the story is a good one.' },
];
const REC_TRAD_ON = REC_DECK;                            // the rec deck's traditions with the deck (day_check flips this line to see the deck's everyday use alone)
if (REC_TRAD_ON) for (const ev of REC_TRADS) SHIP_TRADITIONS.push(ev);
// Winner Stays On's court (RA, 0.83.1): who plays whom, worked out on paper from who's in the stands. Games of WSO_GAME
// ship minutes from the start; the winner stays on, the next challenger is whoever has waited longest in the stands
// (Pell first, when he's there); each game is Lightdisc's own ldPaper, a quick game (to 5) between the two crew levels,
// seeded by the day and the game (key 1037). Three wins in a row put a name on the foyer's board (recBoard('wso')).
// wsoCourt(d) -> { games: [{ a, b, from, to, w }], three: [ids] } (minutes from midnight), pure and kept per day; tradWhere
// puts the two on court at their baselines (7-disc-1 bow, 7-disc-2 stern) while their game is on. A day with no WSO: null
const WSO_GAME = 15, WSO_COURT = new Map();               // a game with the walk on and off (0.83.2: 8 was shorter than the walk from the stands)
function wsoCourt(d) {
  if (WSO_COURT.has(d)) return WSO_COURT.get(d);
  const e = REC_DECK && eventsOn(d).find(x => x.id === 'rec-wso' || x.id === 'rec-cup'), out = e && e.id === 'rec-wso' ? { games: [], three: [] } : null;
  if (out) {
    const B = (d - 1) * 1440, seg = new Map();
    for (const p of schedPeople()) { const s = planDay(p, d).find(x => x.tag && x.tag.startsWith('ev-rec-wso')); if (s) seg.set(p.id, [s.from - B, s.to - B]); }
    const here = (id, a, b) => { const x = seg.get(id); return !!x && x[0] <= a && x[1] >= b; };
    const since = new Map(); let champ = null, run = 0, side = 1;   // side: the champion's end (1 = 7-disc-1 by the gate, 2 = the stern); the winner stays where they are
    for (let T = e.from; T + WSO_GAME <= e.to; T += WSO_GAME) {
      if (champ && !here(champ, T, T + WSO_GAME)) { champ = null; run = 0; }
      const q = [...seg.keys()].filter(id => id !== champ && here(id, T, T + WSO_GAME)).sort((x, y) => (y === 'pell') - (x === 'pell') || (since.get(x) ?? seg.get(x)[0]) - (since.get(y) ?? seg.get(y)[0]) || (x < y ? -1 : 1));
      if (!champ) { champ = q.shift() || null; run = 0; side = 1; }
      const ch = q.shift(); if (!champ || !ch) continue;
      const r = ldPaper({ seed: Math.floor(schedU(d, T, 1037) * 4294967296), quick: true, you: ldLevel(champ), them: ldLevel(ch) });
      const w = r.winner === 0 ? champ : ch, l = w === champ ? ch : champ;
      out.games.push({ a: champ, b: ch, from: T, to: T + WSO_GAME, w, at1: side === 1 ? champ : ch });
      since.set(l, T + WSO_GAME);                          // back of the queue
      if (w !== champ) side = 3 - side;
      run = w === champ ? run + 1 : 1; champ = w;
      if (run === 3 && !out.three.includes(w)) out.three.push(w);
    }
  }
  WSO_COURT.set(d, out); if (WSO_COURT.size > 20) WSO_COURT.delete(WSO_COURT.keys().next().value);
  return out;
}
// SHIP.rec (RA, 0.83.1): the rec deck's lasting state, saved as save.rec and read back defensively (recClean), so an older
// save starts with nothing held yet. ah: the day of the first Captain's all-hands (null until then), film: the day film
// night moved to the auditorium, wso / bell / cup: the boards' names, [[id, day], ...] ('you' for you; the bell board
// keeps the season's), pc: your Paddle club visits, talk: { heard: [ids], asked: [ids], mine: day | null }
function recClean(s) {
  const r = s && typeof s === 'object' ? s : {}, day = v => Number.isInteger(v) && v >= 0 ? v : null;
  const names = l => Array.isArray(l) ? l.filter(x => Array.isArray(x) && typeof x[0] === 'string' && x[0].length < 40 && Number.isInteger(x[1])).slice(-40) : [];
  const ids = l => Array.isArray(l) ? l.filter(x => typeof x === 'string' && x.length < 40).slice(-40) : [];
  const t = r.talk && typeof r.talk === 'object' ? r.talk : {};
  return { ah: day(r.ah), film: day(r.film), wso: names(r.wso), bell: names(r.bell), cup: names(r.cup), reg: names(r.reg), pc: Number.isInteger(r.pc) && r.pc >= 0 ? r.pc : 0,
    talk: { heard: ids(t.heard), asked: ids(t.asked), mine: day(t.mine) } };
}
SHIP.rec = recClean(SAVED && SAVED.rec);
SAVE_EXTRA.push(sv => { sv.rec = JSON.parse(JSON.stringify(SHIP.rec)); });
onSim('newGame', () => { SHIP.rec = recClean(null); });
const recBoardAdd = (k, id, d) => { const l = SHIP.rec[k]; if (!l.some(x => x[0] === id && (k !== 'bell' || season(x[1]) === season(d)))) l.push([id, d]); if (l.length > 40) l.shift(); };
// a board's names now: the foyer's Winner Stays On board (three in a row), the season's bell board (Wall night), the Cup's winners
function recBoard(k, d = SHIP.time.day) { return (SHIP.rec[k] || []).filter(x => k !== 'bell' || season(x[1]) === season(d)).map(x => x[0]); }
// at the end of each: the boards fill (the crew's from the day's plans; yours when you joined)
onSim('tradition', x => {
  if (!REC_DECK || !x || !/^rec-/.test(x.id || '')) return;
  if (x.id === 'rec-wso') { const c = wsoCourt(x.day); for (const id of (c && c.three) || []) recBoardAdd('wso', id, x.day); }
  if (x.id === 'rec-wall-night') { for (const p of schedPeople()) if (planDay(p, x.day).some(s => s.type === 'rec:climb' && evTagId(s.tag) === x.id)) recBoardAdd('bell', p.id, x.day); if (x.you) recBoardAdd('bell', 'you', x.day); }
  if (x.id === 'rec-paddle-club' && x.you) SHIP.rec.pc++;
  if (x.id === 'rec-wall-night') { const names = recBoard('bell', x.day).map(id => id === 'you' ? 'you' : shortName(schedPeople().find(p => p.id === id) || { name: id })).join(', ');
    if (names) recMail(x.at, 'Tomas Lind', x.you ? 'mail.rec.bellboard.you' : 'mail.rec.bellboard', 'The bell board', 'This season\'s bell board in the foyer: ' + names + '.', { text: names }); }
  if (x.id === 'rec-regatta') { const w = regattaWinner(x.day); if (w) { recBoardAdd('reg', w, x.day); const n = shortName(schedPeople().find(p => p.id === w) || { name: w }); recMail(x.at, 'Chief Bram Holt', 'mail.rec.regatta.won', 'The regatta', n + ' won the regatta. The pennant is up over the dock.', { name: n }); } }
  if (x.id === 'rec-cup') { const c = cupBracket(x.day), you = REC.cup && REC.cup.day === x.day && REC.cup.won; if (you || c && c.winner) { recBoardAdd('cup', you ? 'you' : c.winner, x.day);
    const n = you ? 'you' : shortName(schedPeople().find(p => p.id === c.winner) || { name: c.winner }); recMail(x.at, 'Pell Okafor', 'mail.rec.cup.won', 'The Lightdisc Cup', 'The Lightdisc Cup goes to ' + n + '. The foyer\'s board has the name.', { name: n }); } }
});
// the first Captain's all-hands (lead 17's call 1: no invented trigger): the first address of the first ship-wide event.
// From then on the season's all-hands come on the first Monday of each season (rec-all-hands, flag rec.allHands), and film
// night moves to the auditorium for good (rec-film-night, flag rec.filmMoved), the junior common room a quiet Saturday after;
// a note for the writers' Mail (simNote('recMoved'))
// the writer's words for the rec deck's Mail (W3's banks/mail-rec.lines: mail.rec.*), else the stand-in; "subject | body" or a body
const recWords = (key, standIn, ctx) => (typeof quizText === 'function' && quizText(key, SHIP.time.day, ctx)) || standIn;
const recMail = (at, from, key, subject, standIn, ctx) => {
  if (typeof mailSend !== 'function') return;
  const w = recWords(key, standIn, ctx), i = w.indexOf(' | ');
  mailSend({ at, from, subject: i > 0 ? w.slice(0, i) : subject, body: i > 0 ? w.slice(i + 3) : w, quiet: true });
};
function recFirstAllHands(at) {
  const d = Math.floor(at / 1440) + 1; SHIP.rec.ah = d; SHIP.rec.film = d;
  flagSet('rec.allHands', d); flagSet('rec.filmMoved', d);
  if (typeof simNote === 'function') simNote('recMoved', { day: d, what: 'film' });
  recMail(at, 'Pell Okafor', 'mail.rec.film.moved', 'Film night has moved', 'Film night is in the auditorium from this Saturday: the big screen, the violet seats and popcorn from the galley. The junior common room is all yours for a quiet Saturday.');
}
// the regatta's winner (heats of four on paper, the pennant): among those who paddled at it, seeded by the day (key 1038)
const regattaPaddler = (p, d) => p.id !== 'holt' && (evHas(p, d, 'kayaker') || schedU(p.seed, d, 1038) < .4);   // the rest watch from the banks
function regattaWinner(d) {
  const ids = schedPeople().filter(p => regattaPaddler(p, d) && planDay(p, d).some(s => evTagId(s.tag) === 'rec-regatta')).map(p => p.id).sort();
  return ids.length ? ids[Math.floor(schedU(d, 0, 1038) * ids.length)] : null;
}
// the Lightdisc Cup's bracket (lead 17's call 2: singles; you and a friend both enter): eight from those in the stands, the
// disc-players first, then by hash (key 1039); three rounds of full games on paper (ldPaper, to 7). cupBracket(d) -> {
// rounds: [[[a, b, w], ...], ...], winner } | null. Your matches are live (REC.cup); a win of yours takes your opponent's place
const CUP_MEMO = new Map();
function cupBracket(d) {
  if (CUP_MEMO.has(d)) return CUP_MEMO.get(d);
  const e = REC_DECK && eventsOn(d).find(x => x.id === 'rec-cup'); let out = null;
  if (e) {
    const went = schedPeople().filter(p => planDay(p, d).some(s => evTagId(s.tag) === 'rec-cup'));
    let field = went.map(p => [evHas(p, d, 'disc-player') ? 0 : 1, schedU(p.seed, d, 1039), p.id]).sort((a, b) => a[0] - b[0] || a[1] - b[1]).slice(0, 8).map(x => x[2]);
    if (field.length >= 2) {
      out = { rounds: [], winner: null };
      for (let r = 0; field.length > 1; r++) {
        const next = [], round = [];
        for (let i = 0; i < field.length; i += 2) {
          if (i + 1 >= field.length) { next.push(field[i]); continue; }   // a bye
          const g = ldPaper({ seed: Math.floor(schedU(d, r * 8 + i, 1039) * 4294967296), quick: false, you: ldLevel(field[i]), them: ldLevel(field[i + 1]) });
          const w = g.winner === 0 ? field[i] : field[i + 1]; round.push([field[i], field[i + 1], w]); next.push(w);
        }
        out.rounds.push(round); field = next;
      }
      out.winner = field[0];
    }
  }
  CUP_MEMO.set(d, out); if (CUP_MEMO.size > 8) CUP_MEMO.delete(CUP_MEMO.keys().next().value);
  return out;
}
// crew v crew on the court (0.83.2): who's playing now, for the live game when you're watching (the drawing and the
// poses are rec engineer B's: their code steps ldNew({ seed, quick: true, you: ldLevel(a), them: ldLevel(b) }) from `from`)
// and the day's pick-up games on paper (two crew whose plans have them on the two baselines at once). recCourtNow(t) ->
// { a (7-disc-1), b (7-disc-2), from, to, seed, wso } | null; recPickups(d) -> [{ a, b, from, to, w }] (ldPaper, key 1037)
function recCourtNow(t = shipNow()) {
  const d = Math.floor(t / 1440) + 1, B = (d - 1) * 1440, m = t - B;
  const c = weekday(d) === 6 ? wsoCourt(d) : null, g = c && c.games.find(x => x.from <= m && m < x.to);
  if (g) return { a: g.at1, b: g.at1 === g.a ? g.b : g.a, from: B + g.from, to: B + g.to, seed: Math.floor(schedU(d, g.from, 1037) * 4294967296), wso: true };
  const x = recPickups(d).find(x => x.from <= m && m < x.to);
  return x ? { a: x.a, b: x.b, from: B + x.from, to: B + x.to, seed: x.seed, wso: false } : null;
}
const PICKUPS = new Map();
function recPickups(d) {
  if (PICKUPS.has(d)) return PICKUPS.get(d);
  const B = (d - 1) * 1440, at = id => schedPeople().flatMap(p => planDay(p, d).filter(s => s.placeId === id).map(s => [p.id, s.from - B, s.to - B])), out = [];
  for (const [a, x, y] of at('7-disc-1')) for (const [b, u, v] of at('7-disc-2')) {
    const from = Math.max(x, u), to = Math.min(y, v); if (to - from < 5) continue;
    const seed = Math.floor(schedU(d, from, 1037) * 4294967296), r = ldPaper({ seed, quick: true, you: ldLevel(a), them: ldLevel(b) });
    out.push({ a, b, from, to, seed, w: r.winner === 0 ? a : b });
  }
  PICKUPS.set(d, out); if (PICKUPS.size > 10) PICKUPS.delete(PICKUPS.keys().next().value);
  return out;
}
function wsoWhere(p, t) {                                // the two on court now (null for anyone else)
  const d = Math.floor(t / 1440) + 1; if (!REC_DECK || weekday(d) !== 6 || (typeof DISC !== 'undefined' && DISC.g)) return null;   // while you play, the pair waits in the stands
  const c = wsoCourt(d); if (!c) return null;
  const m = t - (d - 1) * 1440, g = c.games.find(x => x.from <= m && m < x.to && (x.a === p.id || x.b === p.id)); if (!g) return null;
  return { deck: 7, act: 'leisure', type: 'rec:disc', placeId: g.at1 === p.id ? '7-disc-1' : '7-disc-2', moving: false, from: (d - 1) * 1440 + g.from, until: (d - 1) * 1440 + g.to, tag: 'ev-rec-wso-disc', anim: null };
}
const TRAD_SRC = (() => { try { if (typeof TRADITIONS !== 'undefined') return TRADITIONS; } catch (e) { /* not baked */ } TRAD_ERRORS.push('no TRADITIONS block in the build (section 22)'); return []; })();
const TRAD_LIST = Array.isArray(TRAD_SRC) ? TRAD_SRC : Object.keys(TRAD_SRC).sort().map(id => ({ id, ...TRAD_SRC[id] }));
for (const t of TRAD_LIST) {
  const ev = tradLoad(t); if (!ev) continue;
  if (!REC_DECK && ev.where.every(w => w.deck === 7)) continue;   // the rec deck's own (0.83, RA): only with the deck switched on
  const r = REC_TRADS.find(x => x.id === ev.id);           // one of the rec deck's: the writer's file brings the words; the rules stay REC_TRADS' (whereFor, first, the rota)
  if (r) { for (const k of ['from', 'mail', 'ask', 'here', 'thanks', 'chatter', 'text', 'invite']) { const ds = Object.getOwnPropertyDescriptor(ev, k); if (ds && (ds.get || ds.value != null)) Object.defineProperty(r, k, ds); } r.baked = true; continue; }
  const i = SHIP_TRADITIONS.findIndex(x => x.id === ev.id);
  if (i >= 0) SHIP_TRADITIONS[i] = ev; else SHIP_TRADITIONS.push(ev);
}
// birthdays: ROSTER[i].birthday (a day of the year, 1-364, section 9) when it's there; until then a stand-in, spread
// so about one falls each week, in id order
let EV_BDAYS = null;
function birthdayOf(p) {
  if (Number.isInteger(p.birthday) && p.birthday >= 1 && p.birthday <= 364) return p.birthday;
  if (!EV_BDAYS) {
    const ppl = schedPeople().filter(q => q.rank !== 'guest').slice().sort((a, b) => a.id < b.id ? -1 : 1);
    EV_BDAYS = new Map(ppl.map((q, i) => [q.id, 1 + Math.floor((i + .5) * 364 / ppl.length + 3 * schedU(q.seed, 0, 333)) % 364]));
  }
  return EV_BDAYS.get(p.id) || null;
}
// gatherings shaped like traditions, so they reach the plans through the same door (eventPlan): a ship-wide event's
// gathering moments (when: { ship: <event id>, day: <its day 0..> }) and one-offs (when: { date: <ship day> }).
// They carry no Mail of their own (the event's address and Mail announce them, or the one-off's caller).
// venue: the deck architect's gather venue (gatherSpots, non-lead spots) as the first pool when it's in the build
const EV_SHIPWIDE = [];
// (filled after SHIP_EVENTS, below: evShipwide)
// one-offs (section 20's story beats: Pell's show), saved in SHIP.events.oneOffs; see eventOneOff
function evOneOffDefs() {
  return ((typeof SHIP !== 'undefined' && SHIP.events && SHIP.events.oneOffs) || []).map(r => r.def || (r.def = {
    id: r.id, name: r.name, k: 341, when: { date: r.day }, host: r.host || null, at: r.at, min: 20, prio: 1, hold: r.hold || [0], venue: r.venue || null,
    where: r.where.map(w => w.room ? { ...w, room: new RegExp(w.room) } : { ...w }),
    who: (p, d) => p.id === r.host ? 1 : Math.min(1, (r.chance || .2) + (r.host && typeof affinityPlan === 'function' ? Math.max(0, affinityPlan(r.host, p.id, d)) / 100 * .6 : 0)),   // pure
    anim: p => p.id === r.host && r.hostAnim ? r.hostAnim : r.anim || null, early: 0,
    from: r.from || null, mail: r.mail || null, ask: r.ask || null, here: r.here || null, thanks: r.thanks || 'You join in for a while.' }));
}
const evTable = () => SHIP_TRADITIONS.concat(EV_SHIPWIDE, evOneOffDefs());
// the events on a day: when it's due, and for a birthday who it's for (one gathering for everyone that day)
const EV_DAYS = new Map();
let EV_ARR = null;
function eventsOn(d) {
  const arr = evArrival() + '|' + SHIP_TRADITIONS.filter(e => e.flag || e.unflag).map(e => typeof flag === 'function' && (e.flag && flag(e.flag) ? 1 : 0) + (e.unflag && flag(e.unflag) ? 2 : 0)).join('');
  if (arr !== EV_ARR) {                                  // section 21 set the day you came aboard, or a tradition's flag was set
    if (EV_ARR !== null && typeof SHIP_DAYS !== 'undefined') { const today = Math.floor(shipNow() / 1440) + 1; for (const x of [...SHIP_DAYS.keys()]) if (x > today) SHIP_DAYS.delete(x); }   // later plans are made again
    EV_ARR = arr; EV_DAYS.clear(); EV_DROPPED.clear(); EV_GOERS.clear();
    try { TALLY_MEMO.clear(); } catch (e) { /* not made yet at load */ }   // who went, and so the votes, change with a flag
  }
  if (EV_DAYS.has(d)) return EV_DAYS.get(d);
  const out = [], yd = shipYearDay(d);
  for (const ev of evTable()) {
    const w = ev.when; let honorees = [];
    if (w.birthday) { honorees = schedPeople().filter(p => birthdayOf(p) === yd && (typeof aboard !== 'function' || (aboard(p, d) && (typeof guestStay !== 'function' || guestStay(p, d) !== 'leave')))); if (!honorees.length) continue; }   // only crew aboard that evening (reserve crew aren't yet; a leaver's gone by 15:00)
    else if (w.rotation != null) { const ids = evRotation(w, d) || []; honorees = schedPeople().filter(p => ids.includes(p.id) && (!w.dept || p.dept === w.dept) && (typeof aboard !== 'function' || aboard(p, d))); if (!honorees.length) continue; }   // a rotation's leavers or arrivals
    else if (w.ship) { const o = typeof eventOn === 'function' ? eventOn(d) : null; if (!o || o.id !== w.ship || o.day !== w.day) continue; }
    else if (w.date) { if (d !== w.date) continue; }
    else if (!evDue(w, d)) continue;
    if (ev.flag && !(typeof flag === 'function' && flag(ev.flag))) continue;   // waits for a story beat (bridge hour: 'bridge.invited')
    if (ev.unflag && typeof flag === 'function' && flag(ev.unflag)) continue;
    if (ev.skip && ev.skip(d)) continue;                   // 0.83.2 (RA): a day it stands down (the rec talent night near the yearly one)   // 0.83 (RA): until a flag (film night in the junior common room, until it moves)
    if (!w.ship && typeof eventPauses === 'function' && eventPauses(ev, d)) continue;   // a ship-wide event's quiet days
    const names = honorees.map(p => p.name).join(', ').replace(/, ([^,]*)$/, ' and $1');   // 'A and B', 'A, B and C'
    out.push({ id: ev.id, name: ev.name, ev, day: d, from: ev.at[0], to: ev.at[1], honorees, names, first: honorees.length ? honorees[0].name.split(' ').slice(-2)[0] : '' });
  }
  const drop = evBudget(out); if (drop.length) { EV_DROPPED.set(d, drop.map(e => e.id)); for (const e of drop) out.splice(out.indexOf(e), 1); }
  EV_DAYS.set(d, out);
  for (const k of EV_DAYS.keys()) if (k < d - 30 || k > d + 30) EV_DAYS.delete(k);
  return out;
}
// the voice budget for traditions (0.34.51, 0.60.7: 2-3 a day, overlaps you choose between): at most two at once, and
// never two at once in the same room (any room in their `where`; a pool counts as its room, EV_POOL_ROOM). Before
// 0.60.7 it was at most two an evening and never two at once on a deck. The higher prio wins, then the rarer rhythm (yearly over seasonal over every few
// weeks over weekly), then the earlier start, then the table's order. Birthdays are never moved and don't count; nor do a ship-wide event's
// gatherings and one-offs (the event already quiets the traditions it must). EV_DROPPED: day -> the ids left out
const EV_DROPPED = new Map();
const evRare = w => w.after ? 5 : w.rotation != null ? 4 : w.yearDay || w.every === 'year' ? 4 : w.every === 'quarter' ? 3 : w.every === '4weeks' || w.every >= 28 ? 2 : w.every === '2weeks' || w.every >= 14 ? 1 : 0;
const evDecks = ev => ev.where.map(w => w.deck);
const EV_POOL_ROOM = { gym: 'gym', 'gym-run': 'gym', music: 'music room', garden: 'hydroponics garden', 'garden-tend': 'hydroponics garden', 'common-room': 'junior common room', 'mess-seat': 'mess hall', 'lounge-seat': 'bow lounge' };
const evRooms = ev => ev.where.map(w => w.deck + '|' + (w.room ? w.room.source.replace(/^\^|\$$/g, '').replace(/\\/g, '').toLowerCase() : EV_POOL_ROOM[w.pool] || w.pool));
// an evening's tradition starts at 17:00 or later and runs past 18:00 (one-week-aboard's tea after shift, 17:15-17:55, doesn't)
const evEvening = e => e.from >= 1020 && e.to > 1080;
function evBudget(list) {
  const rank = e => SHIP_TRADITIONS.indexOf(e.ev), recOnly = e => e.ev.where.every(w => w.deck === 7);
  // the rec deck's own (0.83, RA) are budgeted among themselves (one at a time in a room), so the ship's others never change
  const rec = list.filter(e => rank(e) >= 0 && !e.ev.when.birthday && recOnly(e)), t = list.filter(e => rank(e) >= 0 && !e.ev.when.birthday && !recOnly(e));
  const recDrop = []; if (rec.length) { rec.sort((a, b) => (b.ev.prio || 0) - (a.ev.prio || 0) || evRare(b.ev.when) - evRare(a.ev.when) || a.from - b.from || rank(a) - rank(b));
    const kept = []; for (const e of rec) { const rooms = evRooms(e.ev); if (kept.some(k => k.from < e.to && e.from < k.to && evRooms(k.ev).some(r => rooms.includes(r)))) recDrop.push(e); else kept.push(e); } }
  t.sort((a, b) => (b.ev.prio || 0) - (a.ev.prio || 0) || evRare(b.ev.when) - evRare(a.ev.when) || a.from - b.from || rank(a) - rank(b));   // then the earlier start
  const keep = [], drop = [];
  for (const e of t) {
    const over = keep.filter(k => k.from < e.to && e.from < k.to), rooms = evRooms(e.ev);
    const clash = over.some(k => evRooms(k.ev).some(r => rooms.includes(r)));   // never two at once in one room
    const crowd = [e, ...over].some(x => x.from >= e.from && over.filter(k => k.from <= x.from && x.from < k.to).length >= 2);   // at most two at once
    if (clash || crowd) drop.push(e); else keep.push(e);
  }
  return drop.concat(recDrop);
}
// ties (Pillar 4): what a tradition asks of other sections, kept as data on it: ties = { galley: { dish, batch, meal },
// garden: 'sow' | 'tend' | 'harvest', decor: '<id>', tally: { kind, choices } }. Each owner reads only its own kind:
// tradTies(kind, d) -> [{ id, name, from, to, tie }] for that day (pure; [] on most days)
// tallies (Pillar 4): a vote or a score kept for a week. ties.tally = { kind, choices: [..], per?: how many a time
// (rotating through the list by week), mode?: 'teams' (each goer scores for their department's team) }. Crew who went
// vote by hash (pure: the same every time); your vote (tallyVote, saved) counts one more. tallyOf(id, d) -> { id, day,
// choices, counts, winner, you, n } | null; tallyLast(id, d) -> the most recent one on or before d (the galley reads
// Wednesday's tasting winner on Sunday). Without choices (Tiles night's) it's null: the Tiles engineer keeps those results
const TALLY_TEAMS = { bridge: ['command', 'helm', 'comms'], commons: ['galley', 'infirmary', 'store', 'garden', 'civilian'] };
const TALLY_MEMO = new Map();
const tallyLabel = c => String(c).replace(/-/g, ' ');
function tallyOf(id, d) {
  const e = eventsOn(d).find(x => x.id === id), t = e && e.ev.ties && e.ev.ties.tally; if (!t || !t.choices) return null;
  const you = (SHIP.events.votes || {})[id + '@' + d] || null, key = id + '@' + d + '@' + you;
  if (TALLY_MEMO.has(key)) return TALLY_MEMO.get(key);
  const all = [].concat(t.choices), per = Math.min(t.per || all.length, all.length), n = Math.floor((d - 1) / 7);
  const choices = per >= all.length ? all : Array.from({ length: per }, (_, i) => all[((n * per + i) % all.length + all.length) % all.length]);
  const counts = Object.fromEntries(choices.map(c => [c, 0]));
  const went = schedPeople().filter(p => planDay(p, d).some(s => evTagId(s.tag) === id));
  for (const p of went) {
    if (t.mode === 'teams') { const c = choices.find(c => p.dept === c || (TALLY_TEAMS[c] || []).includes(p.dept)); if (c) counts[c]++; }
    else counts[choices[Math.floor(schedU(p.seed + 31, d, e.ev.k) * choices.length)]]++;
  }
  if (you && counts[you] != null) counts[you]++;
  const r = { id, day: d, choices, counts, winner: choices.reduce((a, c) => counts[c] > counts[a] ? c : a, choices[0]), you, n: went.length };
  if (TALLY_MEMO.size > 60) TALLY_MEMO.clear();
  TALLY_MEMO.set(key, r); return r;
}
function tallyLast(id, d) { for (let x = d; x > d - 120; x--) { const r = tallyOf(id, x); if (r) return r; } return null; }
// your vote, on the day, before the window ends (for the device or a tap); returns true when counted
function tallyVote(id, choice, t = shipNow()) {
  const d = Math.floor(t / 1440) + 1, e = eventsOn(d).find(x => x.id === id), r = tallyOf(id, d);
  if (!e || !r || !r.choices.includes(choice) || t - (d - 1) * 1440 >= e.to) return false;
  SHIP.events.votes[id + '@' + d] = choice; return true;
}
const tradTies = (kind, d) => eventsOn(d).filter(e => e.ev.ties && e.ev.ties[kind] != null).map(e => ({ id: e.id, name: e.name, from: e.from, to: e.to, tie: e.ev.ties[kind] }));
// tradOn(id, t) -> { id, name, day, from, to } (absolute ship minutes) while that tradition is on at minute t, else null
// (pure).
const tradOn = (id, t = shipNow()) => { const d = Math.floor(t / 1440) + 1, B = (d - 1) * 1440, e = eventsOn(d).find(x => x.id === id);
  return e && t >= B + e.from && t < B + e.to ? { id: e.id, name: e.name, day: d, from: B + e.from, to: B + e.to } : null; };
// the pools: for each `where` with a room, the shared places of those types in that room (not in a locked room; with
// `free`, not anyone's work station), as 'deck|ev:<id>:<n>'; places tagged event: '<id>' as 'deck|ev:<id>'
function eventPools(shared, desks) {
  if (!EV_READY) return;                                 // called before section 18 has run: the caches are cleared at its end
  if (!desks) desks = schedDesks(ROSTER.concat(ROSTER_GUESTS).filter(p => !p.player), shared);
  const taken = new Set(desks.values());
  for (const ev of evTable()) {
    const tagged = new Map();
    if (ev.venue && typeof gatherVenue === 'function') { const g = gatherVenue(ev.venue), l = g ? (shared.get(g.deck + '|event') || []).filter(pl => pl.gather === ev.venue && !pl.lead) : []; if (l.length) tagged.set(g.deck, l); }   // the architect's crowd spots
    for (const l of shared.values()) for (const pl of l) if (pl.event === ev.id) (tagged.get(pl.deck) || tagged.set(pl.deck, []).get(pl.deck)).push(pl);
    for (const [n, l] of tagged) shared.set(n + '|ev:' + ev.id, [...new Set(l)]);
    ev.where.forEach((w, i) => {
      if (!w.room) return;
      const rooms = DECKS[w.deck].rooms || {};
      const l = w.types.flatMap(t => shared.get(w.deck + '|' + t) || []).filter(pl => rooms[pl.room] && w.room.test(rooms[pl.room].name || '')
        && !schedRoomLocked(w.deck, pl.room) && (!w.ids || w.ids.test(pl.id)) && !(w.free && taken.has(pl.id)) && !pl.machine);
      if (l.length) shared.set(w.deck + '|ev:' + ev.id + ':' + i, l);
    });
  }
}
// the pools an event uses for a person, best first: [[deck, key], ...]
function eventOpts(ev, p) {
  const S = schedData(), senior = p.rank !== 'junior' && p.rank !== 'guest', out = [];
  for (const n of Object.keys(DECKS).map(Number)) for (const k of ['@' + ev.id, 'ev:' + ev.id]) if ((S.shared.get(n + '|' + k) || []).length) { out.push([n, k]); break; }
  ev.where.forEach((w, i) => {
    if (w.who === 'officer' && !senior) return;
    const key = w.room ? 'ev:' + ev.id + ':' + i : w.pool;
    if ((S.shared.get(w.deck + '|' + key) || []).length) out.push([w.deck, key]);
  });
  return out;
}
// the places section 14 holds for the event's window (only those going may take them): its tagged places and the
// `where` entries listed in `hold` (default: the first). A big or casual event holds none (hold: []), so dinner and
// the rest of the evening go on around it
function eventPlaces(e) {
  const S = schedData(), ev = e.ev || e, ids = new Set(), hold = ev.hold || [0];
  for (const n of Object.keys(DECKS).map(Number)) for (const k of ['@' + ev.id, 'ev:' + ev.id]) for (const pl of S.shared.get(n + '|' + k) || []) ids.add(pl.id);
  ev.where.forEach((w, i) => { if (hold.includes(i)) for (const pl of S.shared.get(w.deck + '|' + (w.room ? 'ev:' + ev.id + ':' + i : w.pool)) || []) ids.add(pl.id); });
  return [...ids];
}
// free for the whole window: awake, off duty (the shift, the galley rota's stints, a night worker's day's sleep)
// (wake: how long after waking they can be there, default 60; the early traditions say 15, 0.34.51)
function eventFree(p, d, a, b, wake = 60) {
  const F = schedFrame(p, d), P = schedFrame(p, d - 1), over = (x, y) => a < y && x < b;
  if (b > F.bed - 20) return false;
  if (F.night) { if (P.works && (over(0, P.workEnd) || a < 900)) return false; if (F.works && over(F.workStart - 10, 1440)) return false; }
  else {
    if (a < F.wake + wake) return false;
    const gp = shiftBlocks(p, d);
    if (gp && gp.blocks) { if (gp.blocks.some(([x, y]) => over(x - 15, y + 15))) return false; }
    else if (F.works && over(F.workStart - 15, F.workEnd + 15)) return false;
  }
  return true;
}
// when someone free and willing gets there (null: they don't go). afterShift (0.34.51, the end-of-shift traditions):
// a day worker whose shift ends inside the window comes straight from it, 2 minutes after (section 14 lets them join
// up to 10 minutes late, so the clock, a wash and the toilet fit; a later start kept them waiting at the time clock,
// which blocked it for the rest: leave_check), if `min` is still left; a host 15 minutes after, with 5 left (section
// 14 seats a host first, and their end of shift can run past a 10-minute window)
// stay (0.83, RA: Winner Stays On's five hours): each goer comes for ev.stay minutes somewhere in the window, so they need
// be free for only that part of it (keys 1035, 1036 on the person's seed and the tradition's k)
function evStay(p, d, e) {
  const st = e.ev.stay, len = Math.min(e.to - e.from, st[0] + Math.round((st[1] - st[0]) * schedU(p.seed + e.ev.k, d, 1035)));
  const from = e.from + Math.round((e.to - e.from - len) * schedU(p.seed + e.ev.k, d, 1036)); return [from, from + len];
}
function evArrive(p, d, e) {
  const ev = e.ev;
  if (!(schedU(p.seed, d, ev.k) < ev.who(p, d, e))) return null;
  if (ev.stay && ev.host !== p.id) { const [a, b] = evStay(p, d, e); return eventFree(p, d, a, b, ev.wake) ? a : null; }
  if (eventFree(p, d, e.from, e.to, ev.wake)) return e.from;
  if (!ev.afterShift) return null;
  const F = schedFrame(p, d), gp = shiftBlocks(p, d);
  const host = p.id === ev.host, need = host ? 5 : ev.min || 20, at = Math.max(e.from, F.workEnd + (host ? 15 : 2));   // a host comes even for the last few minutes (Calder works late some days), after the whole end of shift
  if (F.night || !F.works || gp && gp.blocks || F.workEnd <= e.from - 15 || at + need > e.to || e.to > F.bed - 20) return null;
  return at;
}
// spare (0.34.51, Gym club): the club leaves that many of its places free (for you), so at most places - spare go:
// the keenest by hash (the host first). -> the Set of ids going that day, made once a day
const EV_GOERS = new Map();
function evGoers(e, d) {
  const key = e.id + '@' + d; if (EV_GOERS.has(key)) return EV_GOERS.get(key);
  const S = schedData(), ev = e.ev, n = Math.max(0, ev.where.reduce((s, w) => s + (S.shared.get(w.deck + '|' + (w.room ? 'ev:' + ev.id + ':' + ev.where.indexOf(w) : w.pool)) || []).length, 0) - ev.spare);
  const l = schedPeople().filter(p => !p.player && (p.rank !== 'guest' || typeof aboard !== 'function' || aboard(p, d)) && evArrive(p, d, e) != null)
    .map(p => ({ p, x: p.id === ev.host || (ev.first && ev.first(p, d)) ? -1 : schedU(p.seed, d, ev.k) / Math.max(.01, ev.who(p, d, e)) })).sort((a, b) => a.x - b.x || (a.p.id < b.p.id ? -1 : 1));
  const s = new Set(l.slice(0, n).map(o => o.p.id));
  if (EV_GOERS.size > 40) EV_GOERS.clear();
  EV_GOERS.set(key, s); return s;
}
// a person's events on day d: who goes is a hash per person, day and event; a clash keeps the higher prio (then the earlier)
function eventPlan(p, d) {
  if (!EV_READY) return [];
  if (p.rank === 'guest') {                              // a guest goes only on the days they're aboard (section 14's aboard, else their event's days)
    if (typeof aboard === 'function') { if (!aboard(p, d)) return []; }
    else if (p.event && p.arrive == null) { const g = eventGuestDays(p); if (!g || d < g[0] || d > g[1]) return []; }
  }
  const out = [];
  for (const e of eventsOn(d)) {
    const ev = e.ev, ctx = e;
    const at = evArrive(p, d, e); if (at == null) continue;
    if (ev.spare != null && !evGoers(e, d).has(p.id)) continue;
    const opts = ev.whereFor ? ev.whereFor(p, d, eventOpts(ev, p)) : eventOpts(ev, p); if (!opts.length) continue;   // whereFor (0.83.2, RA): who sits where (the speaker on the stool, Maeve in the booth)
    const anim = ev.anim(p, d) || null;
    let from = at - (ev.early && e.honorees.includes(p) ? ev.early : 0), to = e.to - Math.round((ev.jitter || 0) * schedU(p.seed, d, ev.k + 100));   // 420-433
    if (ev.stay && ev.host !== p.id) [from, to] = evStay(p, d, e);   // 0.83 (RA): drifting in and out
    out.push({ id: ev.id, from, to, opts, anim, tag: 'ev-' + ev.id + (anim ? '-' + anim : ''), min: ev.host === p.id ? Math.min(ev.min || 20, to - from) : ev.min || 20, prio: ev.prio || 0, host: !!(ev.host && ev.host === p.id), own: e.honorees.includes(p), meal: ev.meal || null });   // host: section 14 seats them first; meal: going IS their dinner or breakfast (section 14)
  }
  out.sort((x, y) => y.own - x.own || y.host - x.host || y.prio - x.prio || x.from - y.from);   // their own birthday, then one they host (0.34.52: Tomas's quiz on a birthday night), then prio
  const keep = [];
  for (const x of out) if (!keep.some(k => x.from < k.to && k.from < x.to)) keep.push(x);
  return keep.sort((x, y) => x.from - y.from);
}
// section 10's poses: an event's tag says what they do there (TAG_ACT), registered once section 10 has run
let EV_TAGS = false;
function eventTags() {
  if (EV_TAGS) return;
  try { for (const ev of evTable()) for (const a of ['talk', 'drink', 'play', 'water', 'wash', 'read', 'cheer', 'clap']) TAG_ACT['ev-' + ev.id + '-' + a] = a; EV_TAGS = true; } catch (e) { /* section 10 not in yet */ }
}
// the event someone is at, or going to later today, from their plan: { e, seg, now }
function eventOf(p, t) {
  const d = Math.floor(t / 1440) + 1;
  for (const s of planDay(p, d)) if (s.tag && /^ev-/.test(s.tag) && s.to > t) {
    const e = eventsOn(d).find(x => s.tag === 'ev-' + x.id || s.tag.startsWith('ev-' + x.id + '-'));
    if (e) return { e, seg: s, now: s.from <= t };
  }
  return null;
}
function eventLine(p, t) {
  const o = eventOf(p, t); if (!o) return null;
  return evText(o.now ? o.e.ev.here : o.e.ev.ask, o.e, p);
}

// ---- on the deck: Mail the evening before, decor while it's on, the player joining ----
// SHIP.events = { sent: ['id@day', ...], joined: ['id@day', ...] } (saved as ship.events)
SHIP.events = (() => {
  const s = SAVED && SAVED.ship && SAVED.ship.events, ok = a => Array.isArray(a) && a.every(x => typeof x === 'string');
  const oo = s && Array.isArray(s.oneOffs) ? s.oneOffs.filter(r => r && typeof r.id === 'string' && Number.isInteger(r.day) && Array.isArray(r.at) && Array.isArray(r.where)) : [];
  return { sent: s && ok(s.sent) ? s.sent.slice(-60) : [], joined: s && ok(s.joined) ? s.joined.slice(-60) : [], oneOffs: oo, noted: s && ok(s.noted) ? s.noted.slice(-60) : [],
    votes: s && s.votes && typeof s.votes === 'object' ? Object.fromEntries(Object.entries(s.votes).filter(([k, v]) => typeof v === 'string').slice(-20)) : {} };
})();
SAVE_EXTRA.push(s => { s.ship.events = { sent: SHIP.events.sent.slice(-60), joined: SHIP.events.joined.slice(-60), oneOffs: SHIP.events.oneOffs.slice(-20).map(({ def, ...r }) => r), noted: SHIP.events.noted.slice(-60), votes: Object.fromEntries(Object.entries(SHIP.events.votes).slice(-20)) }; });
// a one-off gathering (section 20's story beats, e.g. Pell's music boxes): eventOneOff({ id, name, day, at: [from, to],
// where: [{ deck, pool } | { deck, room: 'regexp source' | RegExp, types, ids? }], host?, chance? (base, 0-1; friends of
// the host more), anim?, hostAnim?, venue?, from?, mail? (text: the evening-before Mail), ask?, here?, thanks? }).
// Only for a later day (today's plans are made); it's saved and planned like a tradition. Returns true when added
function eventOneOff(o) {
  if (!o || !o.id || !Number.isInteger(o.day) || o.day <= Math.floor(shipNow() / 1440) + 1 || SHIP.events.oneOffs.some(r => r.id === o.id && r.day === o.day)) return false;
  const r = { ...o, where: (o.where || []).map(w => w.room instanceof RegExp ? { ...w, room: w.room.source } : { ...w }) };
  delete r.who; SHIP.events.oneOffs.push(r);
  SCHED_DATA = null; EV_DAYS.clear(); for (const d of [...SHIP_DAYS.keys()]) if (d >= o.day) SHIP_DAYS.delete(d);   // its places join the pools; later plans are made again
  return true;
}
const EV_MAIL_AT = 1080;                                 // 18:00 the evening before
let EV_LAST = null;                                      // the last minute the Mail was checked to
// the announcements due in (from, to]: at most three days' worth after a long skip. EV_MAILBOX keeps the last 20
// (for the device's calendar later, and events_check); they go to the Mail tab when it's there (section 15)
const EV_MAILBOX = [];
function eventsMail(from, to, quiet) {   // quiet: no toast (after a sleep or skip; never before 06:30 on Day 1, under the welcome)
  from = Math.max(from, to - 3 * 1440);
  for (let d = Math.floor(from / 1440) + 1; d <= Math.floor(to / 1440) + 2; d++) for (const e of eventsOn(d)) {
    const at = (d - 2) * 1440 + EV_MAIL_AT, key = e.id + '@' + d;
    if (at <= from || at > to || SHIP.events.sent.includes(key) || !e.ev.mail) continue;   // ship-wide gatherings and one-offs: no tradition Mail
    if (e.ev.quiet === 'career' && recBigDay(d)) continue;   // 0.83 (RA): the weekly sport ones aren't pushed at you on the career's big days
    SHIP.events.sent.push(key);
    const m = { at, from: e.ev.from, subject: 'Ship tradition: ' + e.name + ', ' + WEEKDAYS[weekday(d)] + ' ' + hhmm(e.from), body: evText(e.ev.mail, e), event: key };   // the user's name for them: "ship traditions"
    EV_MAILBOX.push(m); if (EV_MAILBOX.length > 40) EV_MAILBOX.shift();
    (EV_BUNDLE[at] || (EV_BUNDLE[at] = [])).push(m);
  }
  for (const at of Object.keys(EV_BUNDLE)) {             // one Mail an evening (reviewer 2: Tuesdays brought three): several traditions tomorrow share one
    const l = EV_BUNDLE[at].sort((x, y) => x.subject.slice(-5) < y.subject.slice(-5) ? -1 : x.subject.slice(-5) > y.subject.slice(-5) ? 1 : 0); delete EV_BUNDLE[at];   // in time order (0.34.51)
    const m = l.length === 1 ? l[0] : { at: +at, from: 'The Wren', subject: 'Ship traditions tomorrow: ' + l.map(x => x.subject.replace(/^Ship tradition: /, '').replace(/, \w+day /, ' ')).join('; '), body: l.map(x => x.body).join('\n\n') };
    if (typeof mailSend === 'function') mailSend({ at: m.at, from: m.from, subject: m.subject, body: m.body, quiet: !!quiet || to < 390 });
  }
}
const EV_BUNDLE = {};
// after each one (Pillar 4): simNote('tradition', { id, day, at, came: [crew ids whose plan took them there], you (you
// joined), host, src: 'tradition' | 'shipwide' | 'oneoff' }) once its window has ended, in play or on a skip (at most
// two days back); section 20 makes memories and cues of it. Once each (SHIP.events.noted, saved)
const evTagId = tag => { const m = /^ev-(.+?)(?:-(?:talk|drink|play|water|wash|read|cheer|clap|disc))?$/.exec(tag || ''); return m && (REC_DECK && /^ev-rec-.*-talk$/.test(tag) && SHIP_TRADITIONS.some(e => e.id === tag.slice(3)) ? tag.slice(3) : m[1]); };   // rec-chiefs-talk (0.83.2): an id ending like an anim   // 'ev-quiz-drink' -> 'quiz'
function eventsNoted(from, to) {
  if (typeof simNote !== 'function') return;
  from = Math.max(from, to - 2 * 1440);
  for (let d = Math.floor(from / 1440) + 1; d <= Math.floor(to / 1440) + 1; d++) for (const e of eventsOn(d)) {
    const at = (d - 1) * 1440 + e.to, key = e.id + '@' + d;
    if (at <= from || at > to || SHIP.events.noted.includes(key)) continue;
    SHIP.events.noted.push(key); if (SHIP.events.noted.length > 60) SHIP.events.noted.shift();
    const came = schedPeople().filter(p => planDay(p, d).some(s => evTagId(s.tag) === e.id)).map(p => p.id);
    simNote('tradition', { id: e.id, day: d, at, came, you: SHIP.events.joined.includes(key), host: e.ev.host || null, src: SHIP_TRADITIONS.includes(e.ev) ? 'tradition' : e.ev.when.ship ? 'shipwide' : 'oneoff', tally: e.ev.ties && e.ev.ties.tally ? tallyOf(e.id, d) : null });
  }
}
// ---- the Sunday "This week aboard" Mail (Pillar 4; the monthly tradition designer's words and rules, in
// content/traditions/this-week-aboard.mail; events_check checks this copy against the file, so copy it again when the
// file changes). Sunday 18:00, from the first Sunday after you arrive: the week from Monday, the traditions that aren't
// weekly in full, birthdays, a weekly one the voice budget left out; the weekly ones in one line, except the first time
const WEEK_MAIL = {"from": "oduya", "subject": "This week aboard", "open": ["Here's the week ahead aboard the Wren.", "The week ahead, all in one place. Mark the ones you like on your Calendar.", "A new week aboard. Here's what's on."], "season": ["{season} starts this week. New season, new seedlings.", "A new season this week: {season}. The garden's been waiting."], "day": ["{weekday}"], "item": ["{trad}, {time}, {place}."], "birthday": ["{names}'s birthday: cake in the mess, 20:15."], "dropped": ["{trad}: not this {weekday}, as something rarer is on."], "weekly": ["And all the usual weekly ones: the Calendar has them.", "Plus the usual weekly ones. They're on your Calendar."], "quiet": ["A quiet week: just the usual weekly ones, on your Calendar.", "Nothing special this week. Sometimes that's the best kind."], "close": ["See you there. Matthias", "Come to one, if you can. Matthias", "That's the week. Rest well tonight. Matthias"]};
const WEEK_MAILS = [];                                   // what was sent (the checks)
const evWeekly = w => !w.after && !w.birthday && !w.ship && !w.date && (w.every === 'week' || (w.weekday != null && !w.every));
function evPlaceName(ev) {
  const w = ev.where[0], pool = { gym: 'the gym', garden: 'the garden', 'garden-tend': 'the garden', 'common-room': 'the junior common room', music: 'the music room', 'mess-seat': 'the mess', 'lounge-seat': 'the bow lounge', bench: 'the promenade' };
  const room = w.room ? 'the ' + w.room.source.replace(/^\^|\$$/g, '').replace(/\\/g, '').toLowerCase() : pool[w.pool] || deckIn(w.deck);
  return room + (w.room && w.deck <= 2 ? ', ' + deckIn(w.deck) : '');
}
function weekMail(d) {                                   // d: a Sunday; -> { at, from, subject, body } or null
  const arr = evArrival(); if (weekday(d) !== 6 || d < arr + 7) return null;
  const wk = Math.floor((d - 1) / 7), pick = k => { const l = WEEK_MAIL[k] || []; return l.length ? l[((wk % l.length) + l.length) % l.length] : null; };
  const fill = (t, o) => { let ok = true; const r = t.replace(/\{(\w+)\}/g, (_, k) => o[k] != null ? o[k] : (ok = false, '')); return ok ? r : null; };
  const first = d === arr + 7, out = [pick('open')], days = []; let listed = 0;
  if (evYearDay(d + 1) % 91 === 1) { const l = fill(pick('season'), { season: seasonOf(d + 1).name }); if (l) out.push(l); }
  for (let x = d + 1; x <= d + 7; x++) {
    const on = eventsOn(x), lines = [];
    for (const e of on) {
      if (!SHIP_TRADITIONS.includes(e.ev)) continue;
      if (e.ev.when.birthday) { const l = fill(pick('birthday'), { names: e.names }); if (l) lines.push([e.from, l]); continue; }
      if (evWeekly(e.ev.when) && !first) continue;
      const l = fill(pick('item'), { trad: e.name, time: hhmm(e.from), place: evPlaceName(e.ev), weekday: WEEKDAYS[weekday(x)] }); if (l) lines.push([e.from, l]);
    }
    for (const id of EV_DROPPED.get(x) || []) { const ev = SHIP_TRADITIONS.find(t => t.id === id); if (ev && evWeekly(ev.when)) { const l = fill(pick('dropped'), { trad: ev.name, weekday: WEEKDAYS[weekday(x)] }); if (l) lines.push([ev.at[0], l]); } }
    if (lines.length) { days.push(fill(pick('day'), { weekday: WEEKDAYS[weekday(x)] }), ...lines.sort((a, b) => a[0] - b[0]).map(l => l[1])); listed += lines.length; }   // in time order
  }
  out.push(...days); if (!first) out.push(listed ? pick('weekly') : pick('quiet')); out.push(pick('close'));
  const p = typeof schedPeople === 'function' && schedPeople().find(q => q.id === WEEK_MAIL.from);
  return { at: (d - 1) * 1440 + EV_MAIL_AT, from: p ? p.name : WEEK_MAIL.from, subject: WEEK_MAIL.subject, body: out.filter(Boolean).join('\n'), day: d };
}
function weekMailSend(from, to, quiet) {
  from = Math.max(from, to - 3 * 1440);
  for (let d = Math.floor(from / 1440) + 1; d <= Math.floor(to / 1440) + 1; d++) {
    const at = (d - 1) * 1440 + EV_MAIL_AT, key = 'week@' + d;
    if (weekday(d) !== 6 || at <= from || at > to || SHIP.events.sent.includes(key)) continue;
    const m = weekMail(d); if (!m) continue;
    SHIP.events.sent.push(key); WEEK_MAILS.push(m); if (WEEK_MAILS.length > 8) WEEK_MAILS.shift();
    if (typeof mailSend === 'function') mailSend({ at: m.at, from: m.from, subject: m.subject, body: m.body, quiet: !!quiet });
  }
}
SIM_ADVANCE.push((from, to) => { eventsMail(from, to, true); weekMailSend(from, to, true); eventsNoted(from, to); EV_LAST = to; });
// the player joins by being in one of the event's rooms for 5 ship minutes while it's on: a little social, a toast,
// and a thank-you in the Mail
let EV_IN = { key: null, since: 0 };
function eventRooms(ev) {
  const S = schedData(), rooms = new Set();
  for (const [k, l] of S.shared) { const [n, key] = [+k.split('|')[0], k.split('|')[1]]; if (key === 'ev:' + ev.id || key.startsWith('ev:' + ev.id + ':') || ev.where.some(w => w.pool === key && w.deck === n)) for (const pl of l) rooms.add(n + '|' + pl.room); }
  return rooms;
}
function eventsPlayer(now) {
  const d = Math.floor(now / 1440) + 1, m = now - (d - 1) * 1440, here = deckDef.num + '|' + roomAt(...player.here());
  const e = eventsOn(d).find(x => m >= x.from && m < x.to && (x.rooms || (x.rooms = eventRooms(x.ev))).has(here));
  const key = e ? e.id + '@' + d : null;
  if (key !== EV_IN.key) EV_IN = { key, since: now };
  if (key && e.id === 'quiz' && QUIZ_PLAYED !== d && SHIP.events.joined.includes(key) && !DIALOGUE) quizStart(d, now);   // joined while another card was open: the game when it's free
  if (!key || now - EV_IN.since < 5 || SHIP.events.joined.includes(key) || TJ_WALK) return;   // not on the way past, in a walk's line (0.70.0)
  if (tradJoinable(e) && !tradDoingIt(e)) return;        // 0.70.0: one with something to do together is joined by a tap (tradJoinTap), or by doing it at one of its places
  eventJoin(e, d, now);
}
// joined (by being there, or by a tap): a little social by the best bond there, leisure, the toast (or `notice`), a quiet
// thank-you Mail, and the goal arrow cleared when it pointed at this tradition (0.70.0, the user's "once you've joined,
// its tracking arrow goes away")
function eventJoin(e, d, now, notice) {
  const key = e.id + '@' + d; if (SHIP.events.joined.includes(key)) return false;
  if (!e.rooms) e.rooms = eventRooms(e.ev);
  SHIP.events.joined.push(key);
  if (typeof IX_GOAL !== 'undefined' && IX_GOAL && (IX_GOAL.tj || tradGoalHere(IX_GOAL, e)) && typeof clearGoal === 'function') clearGoal();
  if (e.ev.trace) traceAdd(e.ev.trace, d);              // e.g. Sowing morning plants your seedling (the deck architect's seedlingYours)
  const bb = typeof bondBest === 'function' && typeof DECK_CREW !== 'undefined' ? Math.max(1, bondBest(DECK_CREW.filter(c => c.settled && c.spot && e.rooms.has(deckDef.num + '|' + c.spot.room)).map(c => (c.p || c).id))) : 1;   // 0.28.43: by the best bond there
  const n = SHIP.player && SHIP.player.needs; if (n && typeof n.social === 'number') n.social = Math.min(100, n.social + Math.min(20, 12 * bb));   // at most +20 even among close friends (0.28.49, the lead)
  if (typeof leisureAdd === 'function') leisureAdd(15, 'tradition');   // 0.34.51: going to a tradition fills leisure (PE6's 7th need, +15 in the plan)
  toast(e.name, notice || evText(e.ev.thanks, e));
  if (typeof mailSend === 'function') mailSend({ at: now, from: e.ev.from, subject: 'Thanks for coming', body: 'Good to see you at ' + e.name.toLowerCase() + '. Same time next one?', quiet: true });   // the join toast says it already
  if (e.id === 'quiz') quizStart(d, now);
  if (/^rec-(wren|chiefs)-talk$/.test(e.id)) recTalkCard(e, d, now);   // a Wren talk: listen, or ask one question (0.83.2, RA)
  if (e.id === 'rec-talent-night') recActCard(e, d, now); // talent night: do an act, or watch (0.83.1, RA)
  return true;
}
// talent night's choice card (0.83.1): Lucia asks if you're on the sheet: play a tune, tell a ship joke, a Works trick, or
// just watch. No failing: the crowd cheers whichever, and the ship talks about it for days (newsAdd, about you). Words:
// Ferreira's lines (kinds talent.ask, talent.tune, talent.joke, talent.trick, talent.watch, the writer's), else stand-ins
function recActCard(e, d, now) {
  const q = schedPeople().find(p => p.id === 'ferreira'); if (!q || typeof dialogueShow !== 'function') return;
  const say = (k, x) => { const L = typeof lineFor === 'function' ? lineFor(q.id, k, { t: now }) : null; return L && L.text || x; };
  const did = k => { if (typeof leisureAdd === 'function') leisureAdd(10, 'talent');
    if (typeof newsAdd === 'function') newsAdd({ id: 'rec-talent-you@' + d, about: 'you', lines: [['Did you see the new hand at talent night?', 'The new hand got up at talent night! Brave.', 'Talent night: the new hand\'s act. People are still talking about it.'][k]], seed: ['ferreira', 'volkov-maeve'], weight: .7, life: 4 }); };
  const baked = MEETING_SCRIPTS['rec.talent.you'];          // the writer's act card (W3), when it's baked: its first three choices are acts
  if (baked) { baked.onPick = k => { if (k < 3) did(k); }; dialogueShow('rec.talent.you', { id: 'rec.talent@' + d, who: [q.id], at: now }); return; }
  MEETING_SCRIPTS['rec.talent'] = { title: 'Talent night', gist: 'Talent night in the auditorium.',
    onPick: k => { if (k < 3) did(k); },
    lines: [{ who: q.id, text: say('talent.ask', 'You\'re on the sheet if you want to be. One act. Nobody fails at talent night.') },
      { choice: [{ text: 'Play a tune', rel: { [q.id]: 2 }, reply: { who: q.id, text: say('talent.tune', 'Lovely. Give them a big hand!') } },
        { text: 'Tell a ship joke', rel: { [q.id]: 2 }, reply: { who: q.id, text: say('talent.joke', 'They laughed! Mostly at the right bit.') } },
        { text: 'A Works trick', rel: { [q.id]: 2 }, reply: { who: q.id, text: say('talent.trick', 'A spanner, a bolt and a lot of nerve. Brilliant.') } },
        { text: 'Just watch', reply: { who: q.id, text: say('talent.watch', 'Next time, then. Enjoy the show.') } }] }] };
  dialogueShow('rec.talent', { id: 'rec.talent@' + d, who: [q.id], at: now });
}
// the Wren talks' panel (0.83.2): the speaker's opening, then a choice: ask one question (a friendship step with the
// speaker; a chief remembers who asked) or just listen. Words: the speaker's own lines (kinds talk.open, talk.answer,
// talk.listen, the writer's), else stand-ins. SHIP.rec.talk keeps the talks heard and the speakers asked, by day
function recTalkCard(e, d, now) {
  const t = recTalk(d), q = t && schedPeople().find(p => p.id === t.by);
  if (t && t.by === 'you' && MEETING_SCRIPTS['talk.you'] && typeof dialogueShow === 'function') { dialogueShow('talk.you', { id: 'rec.talk@' + d, who: [], at: now }); return; }   // your own talk (W3's script)
  if (!q || typeof dialogueShow !== 'function') return;
  const say = (k, x) => { const L = typeof lineFor === 'function' ? lineFor(q.id, k, { t: now }) : null; return L && L.text || x; };
  const key = t.by + '@' + d, T = SHIP.rec.talk;
  if (!T.heard.includes(key)) { T.heard.push(key); if (T.heard.length > 40) T.heard.shift(); }
  const baked = MEETING_SCRIPTS['talk.' + t.by];          // the writer's longer script for this talk (W3's talk.<speaker>), when it's baked
  if (baked) { dialogueShow('talk.' + t.by, { id: 'rec.talk@' + d, who: [q.id], at: now }); return; }
  MEETING_SCRIPTS['rec.talk'] = { title: '"' + t.title + '"', gist: shortName(q) + ' gave a talk: "' + t.title + '".',
    onPick: k => { if (k === 0 && !T.asked.includes(key)) { T.asked.push(key); if (T.asked.length > 40) T.asked.shift(); if (t.size === 'chief' && typeof memAdd === 'function') memAdd(q.id, 'asked.talk'); } },
    lines: [{ who: q.id, text: say('talk.open', 'So. ' + t.title + '. Stop me if you\'ve heard this one.') },
      { choice: [{ text: 'Ask a question', rel: { [q.id]: 3 }, reply: { who: q.id, text: say('talk.answer', 'Good question. Nobody\'s asked me that before.') } },
        { text: 'Just listen', reply: { who: q.id, text: say('talk.listen', 'Right, where was I?') } }] }] };
  dialogueShow('rec.talk', { id: 'rec.talk@' + d, who: [q.id], at: now });
}
// ---- tap to join (playtest 1, the traditions engineer, 0.70.0; the user: "tap the leader or anyone taking part to
// join; you then do the activity with them automatically") ----
// TRAD_JOIN lists the traditions with something to do together; the rest are joined by turning up (eventsPlayer). Shared
// so the holidays can use it later: a spec per id, data only.
//   act:  'walk' (fall in behind the leader for a lap: tradWalk), 'gym' (a free machine, Gym club's member rule), an act
//         kind of section 15/15b ('ixGarden', 'ixStars'), or none: our own 'tj:<id>' act (TJ_ACT below) at a free spot
//   host: the leader when the tradition names none; lead(e, goers) picks one per day (the jam: a musician going)
//   pose: what you do at the spot ('sit:' ones become standing at a standing spot, and the reverse 'sit:talk')
//   need, gain, also: our act's gains over TJ_MINS ship minutes (it then goes on, gains done, until the tradition ends)
//   verb: the tip ("Tap Tomas to join the lap"); what: the join notice ("Lap of the Wren: walk the promenade...")
// The head writer's words win when present: LINES['join.<id>.tip'] ({name}) and LINES['join.<id>.notice'].
// While one is on and you haven't joined: a marker over the leader's head (DOM, no draw calls), the goal arrow at the
// leader once you're in one of its rooms (unless the arrow is on something else), and its tip once. A tap on the leader
// or anyone at it joins you (tradJoinTap, from section 10's tapCrew): eventJoin's payoff and the notice at once, then the
// activity. Nothing saved beyond SHIP.events.joined; nothing calls R()
const TJ_MINS = 30;
const TRAD_JOIN = {
  running: { act: 'gym', host: 'rina', verb: 'join Gym club', what: 'take a machine and work out with the club' },
  'department-cup': { act: 'gym', verb: 'join the cup', what: 'take a machine and work out for your department' },
  'lap-of-the-wren': { act: 'walk', host: 'tomas', verb: 'join the lap', what: 'walk the lap of the promenade together, in one line' },
  'lantern-walk': { act: 'walk', verb: 'join the lantern walk', what: 'walk the promenade under the lanterns together, in one line' },
  'sunrise-stretch': { host: 'rina', pose: 'stretch', need: 'fitness', gain: 10, also: { leisure: 8, social: 3 }, verb: 'stretch with them', what: 'stretch with the early risers' },
  'cook-along': { pose: 'cook', need: 'leisure', gain: 20, also: { social: 6 }, verb: 'cook along', what: 'cook along with the class' },
  'garden-hour': { act: 'ixGarden', verb: 'tend the beds with them', what: 'tend a bed with the gardeners' },
  'pick-your-own': { act: 'ixGarden', verb: 'pick with them', what: 'pick fresh fruit and greens with the gardeners' },
  sowing: { act: 'ixGarden', verb: 'sow with them', what: 'sow the new season\'s seeds with the gardeners' },
  harvest: { act: 'ixGarden', host: 'brennan', verb: 'help with the harvest', what: 'pick the harvest with the crew' },
  'tiles-night': { pose: 'sit:play', verb: 'play Tiles', what: 'sit in on a game of Tiles' },
  'tiles-ladder': { pose: 'sit:play', verb: 'play on the ladder', what: 'play a ladder game of Tiles' },
  quiz: { pose: 'sit:talk', verb: 'join a quiz team', what: 'squeeze onto a team; Tomas asks the questions' },
  jam: { pose: 'sit:play', verb: 'sit in on the jam', what: 'sit in and play along',
    lead: (e, goers) => (goers.filter(p => evHas(p, e.day, 'musician')).length ? goers.filter(p => evHas(p, e.day, 'musician')) : goers).slice().sort((a, b) => schedU(idHash(a.id), e.day, 701) - schedU(idHash(b.id), e.day, 701))[0] },
  'book-circle': { pose: 'sit:read', verb: 'join the book circle', what: 'read along with the circle' },
  'knit-and-natter': { pose: 'sit:read', verb: 'knit and natter', what: 'knit and chat with them' },
  'postcard-night': { pose: 'read', verb: 'write a postcard', what: 'write a postcard home with them' },
  'observatory-night': { act: 'ixStars', host: 'sato', verb: 'stargaze with them', what: 'take a scope and stargaze with them' },
  'open-lab': { pose: 'talk', need: 'leisure', gain: 15, also: { social: 6 }, verb: 'look round the lab', what: 'look round the lab with the Survey crew' },
  'name-on-the-beam': { act: 'beam', verb: 'paint your name', what: 'you paint your name on the beam, beside everyone who has served in Works' },
  'works-tea': { pose: 'wash', need: 'social', gain: 10, also: { leisure: 8, hunger: 4 }, host: 'calder', verb: 'wipe tools over tea', what: 'wipe down tools with the Works crew over tea' },
};
// our own act per tradition (TJ_ACT): in PLAYER_ACTS (section 15 runs it) and IX_ACTS (15b adds the side gains, with company)
const tjEnd = A => typeof shipNow === 'function' && A.o.end != null && shipNow() >= A.o.end;
for (const [id, s] of Object.entries(TRAD_JOIN)) if (!s.act || s.act === 'beam') {
  const def = { need: s.need || 'social', gain: s.gain || 12, mins: s.act === 'beam' ? 3 : TJ_MINS, also: s.also || { leisure: 10 }, with: 4, title: id, until: s.act === 'beam' ? A => A.done >= A.def.mins : tjEnd };   // the beam: a few minutes' painting
  PLAYER_ACTS['tj:' + id] = def; if (typeof IX_ACTS !== 'undefined') IX_ACTS['tj:' + id] = def;
}
const tradJoinable = e => !!(e && TRAD_JOIN[e.id] && SHIP_TRADITIONS.includes(e.ev));
const tradWords = (e, k, ctx) => { const t = quizText('join.' + e.id + '.' + k, e.day, ctx); return t; };
// the people going (their plan has them there today), and the leader: the tradition's host, else the spec's, when going;
// else the spec's pick or the first of the goers by a hash of the day. Cached per day
const TJ_LEAD = new Map();
function tradGoers(e) { return schedPeople().filter(p => planDay(p, e.day).some(s => evTagId(s.tag) === e.id)); }
function tradLeader(e) {
  const key = e.id + '@' + e.day; if (TJ_LEAD.has(key)) return TJ_LEAD.get(key);
  const s = TRAD_JOIN[e.id], goers = tradGoers(e), going = id => goers.find(p => p.id === id);
  const p = going(e.ev.host) || going(s.host) || (s.lead && goers.length ? s.lead(e, goers) : null)
    || goers.slice().sort((a, b) => schedU(idHash(a.id), e.day, 700) - schedU(idHash(b.id), e.day, 700))[0] || null;
  if (TJ_LEAD.size > 40) TJ_LEAD.clear(); TJ_LEAD.set(key, p ? p.id : null);
  return p ? p.id : null;
}
const tjFirst = id => { const p = schedPeople().find(q => q.id === id); return p ? shortName(p) : id; };   // section 14's: 'Dr. Sato', 'Chief Calder', 'Tomas' (reviewer R3, 0.70.3)
const tjAgent = id => typeof DECK_CREW !== 'undefined' ? DECK_CREW.find(c => c.p && c.p.id === id) || null : null;
// the tradition on now that you could join on this deck: { e, key, lead (id), agent } or null (once a ship minute)
let TJ_NOW = null;
function tradJoinMinute(now) {
  TJ_NOW = null;
  const d = Math.floor(now / 1440) + 1, m = now - (d - 1) * 1440;
  for (const e of eventsOn(d)) {
    if (m < e.from || m >= e.to || !tradJoinable(e) || SHIP.events.joined.includes(e.id + '@' + d)) continue;
    if (!e.rooms) e.rooms = eventRooms(e.ev);
    if (![...e.rooms].some(r => +r.split('|')[0] === deckDef.num)) continue;
    let lead = tradLeader(e), agent = lead && tjAgent(lead);
    const host = e.ev.host || TRAD_JOIN[e.id].host, ha = host && host !== lead && tjAgent(host);   // the host on duty nearby leads anyway (Cook-along's Lukas at the pass: reviewer R3)
    if (ha && [...tradSpotIds(e)].some(id => { const sp = PLACE_OF.has(id) && placeSpot(id); return sp && Math.hypot(sp.x - ha.x, sp.z - ha.z) < 6; })) { lead = host; agent = ha; }
    if (!agent) continue;
    TJ_NOW = { e, key: e.id + '@' + d, lead, agent }; break;
  }
  const g = typeof IX_GOAL !== 'undefined' ? IX_GOAL : null;
  if (g && g.tj && (!TJ_NOW || g.tj !== TJ_NOW.key)) clearGoal();   // it ended, or you joined: the arrow at the leader goes
  if (!TJ_NOW) return;
  const here = deckDef.num + '|' + roomAt(...player.here()), name = tjFirst(TJ_NOW.lead), s = TRAD_JOIN[TJ_NOW.e.id];
  if (!TJ_NOW.e.rooms.has(here)) return;
  const beam = s.act === 'beam', label = tradWords(TJ_NOW.e, 'tip', { name }) || (beam ? 'Tap the beam to paint your name' : 'Tap ' + name + ' to ' + s.verb);
  if (!g || g.tj === TJ_NOW.key || tradGoalHere(g, TJ_NOW.e)) { if (!g || g.tj !== TJ_NOW.key) setGoal(beam ? { deck: 5, item: /^The beam$/, label, tj: TJ_NOW.key } : { deck: deckDef.num, crew: TJ_NOW.lead, label, tj: TJ_NOW.key }); }
  ixTip('t:join:' + TJ_NOW.e.id, label + (beam ? '. The Works crew are waiting to see it go up.' : '. Anyone taking part will do: you join in with them.'));
}
// a goal arrow pointing at this tradition's room (the device's heads-up, the Tracked list): { deck, room (key or name) }
function tradGoalHere(g, e) {
  if (!g || !g.room || !e.rooms) return false;
  const key = typeof g.room === 'string' && ROOMS[g.room] ? g.room : Object.keys(ROOMS).find(k => g.room instanceof RegExp ? g.room.test(ROOMS[k].name || '') : ROOMS[k].name === g.room);
  return g.deck === deckDef.num && !!key && e.rooms.has(g.deck + '|' + key);
}
// you're doing it already: your activity is at one of its places (a machine in Gym club, a bed in the garden hour)
function tradDoingIt(e) {
  if (typeof ACT === 'undefined' || !ACT || !ACT.placeId || ACT.phase !== 'do' || TRAD_JOIN[e.id].act === 'beam') return false;   // the beam: only by painting
  return tradSpotIds(e).has(ACT.placeId);
}
function tradSpotIds(e) {
  const S = schedData(), ids = new Set();
  for (const [n, k] of eventOpts(e.ev, { rank: 'junior' })) if (n === deckDef.num) for (const pl of S.shared.get(n + '|' + k) || []) ids.add(pl.id);
  return ids;
}
// a free spot of the tradition's on this deck for you, nearest x, z: not anyone's (heading there or at it), not private
function tradSpot(e, x, z) {
  const s = TRAD_JOIN[e.id];
  const ok = pl => pl && !heldBy(pl.id) && !BUSY.has(pl.id) && pl.id !== PLAYER_PLACE && !(PRIVATE_TYPES.has(pl.type) && privatePlace(pl))
    && (s.act !== 'gym' || pl.type === 'gym' && pl.anim !== 'drink') && (s.act !== 'ixGarden' || pl.pose !== 'sit') && (s.act !== 'ixStars' || pl.type !== 'bench');
  const stand = s.pose && !/^sit/.test(s.pose), off = sp => stand && sp.pose === 'sit' ? 50 : 0;   // a standing one (stretch, cook) at a standing spot first
  const pick = l => l.filter(ok).map(pl => [pl, placeSpot(pl.id)]).filter(([, sp]) => sp)
    .sort((a, b) => off(a[1]) + Math.hypot(a[1].x - x, a[1].z - z) - off(b[1]) - Math.hypot(b[1].x - x, b[1].z - z) || (a[0].id < b[0].id ? -1 : 1))[0] || null;
  // every one taken (a full music room): any free seat or spot in its rooms, so there's always room for you (like Gym club's spare)
  return pick([...tradSpotIds(e)].map(id => PLACE_OF.get(id))) || (s.act === 'gym' ? null
    : pick([...PLACE_OF.values()].filter(pl => (SIT_TYPES.has(pl.type) || pl.type === 'event') && e.rooms && e.rooms.has(deckDef.num + '|' + pl.room))));
}
function tradPose(s, pl, sp) {
  const sit = sp.pose === 'sit';
  if (s.act === 'gym') return (typeof poseOf === 'function' ? poseOf(pl) : null) || pl.anim || (pl.pose === 'stand' ? 'lift' : pl.pose);
  if (s.act === 'ixGarden') return 'water';
  if (s.act === 'ixStars') return sit ? 'sit' : 'stand';
  const p = s.pose || 'talk';
  return sit ? (/^sit/.test(p) ? p : /^(read|play|drink|call)$/.test(p) ? 'sit:' + p : 'sit:talk') : p.replace(/^sit:/, '');
}
// the tap (section 10's tapCrew asks first): someone at a joinable tradition now (or its leader) joins you. True when it did
function tradJoinTap(a) {
  if (!a || !a.p || typeof deckDef === 'undefined') return false;
  const now = shipNow(), d = Math.floor(now / 1440) + 1, m = now - (d - 1) * 1440;
  const o = eventOf(a.p, now), e = o && o.now ? o.e : TJ_NOW && TJ_NOW.lead === a.p.id ? TJ_NOW.e : null;
  if (!e || !tradJoinable(e) || m < e.from || m >= e.to || SHIP.events.joined.includes(e.id + '@' + d)) return false;
  return tradJoin(e, a);
}
function tradJoin(e, a) {
  const s = TRAD_JOIN[e.id], now = shipNow(), d = e.day, lead = TJ_NOW && TJ_NOW.e === e ? TJ_NOW.lead : tradLeader(e), name = tjFirst(lead || a.p.id);
  const notice = tradWords(e, 'notice', { name }) || e.name + ': ' + s.what + '. Social and leisure up.';
  player.stop(); a.talking = 2; player.face = Math.atan2(a.x - player.obj.position.x, a.z - player.obj.position.z);
  if (s.act === 'beam') { toast(a.p.name, '"' + (tradWords(e, 'tell', { name }) || 'Go on, tap the beam. Your name goes up there, with ours.') + '"'); return true; }
  if (s.act === 'walk') { eventJoin(e, d, now, notice); tradWalkStart(e, lead); return true; }
  const near = tjAgent(lead) || a, sp = tradSpot(e, near.x, near.z);
  eventJoin(e, d, now, notice);
  const kind = s.act || 'tj:' + e.id, o = { title: e.name, member: s.act === 'gym', after: notice, end: (d - 1) * 1440 + e.to, tj: e.id + '@' + d };
  if (!sp) {                                             // every spot taken (a full music room): you stand beside the leader and join in there
    const w = nearestOpen(near.x + .9, near.z + .9, player), c = w && cellPos(...w);
    if (!c || s.act) { toast(e.name, notice + ' Every spot\'s taken just now, so you stand and chat with them.'); return true; }
    actStart('tj:' + e.id, null, { ...o, pose: tradPose(s, {}, { pose: 'stand' }), company: 1, spot: { id: null, walk: w, x: c.x, z: c.z, y: 0, face: Math.atan2(near.x - c.x, near.z - c.z), pose: 'stand' } });
    return true;
  }
  const [pl, spot] = sp, company = typeof ixBond === 'function' ? ixBond(spot) : 1;
  actStart(kind, pl.id, { ...o, pose: tradPose(s, pl, spot), company });
  return true;
}
// the marker over the leader's head (once a frame): a small badge, DOM only
let TJ_MARK = null; const tjV = new THREE.Vector3();
function tradJoinFrame() {
  const A = TJ_NOW && TJ_NOW.agent && DECK_CREW.includes(TJ_NOW.agent) ? TJ_NOW.agent : null;
  if (!A) { if (TJ_MARK) TJ_MARK.style.display = 'none'; return; }
  if (!TJ_MARK) {
    const st = document.createElement('style');
    st.textContent = '#tjMark{position:fixed;left:0;top:0;z-index:2;pointer-events:none;transform:translate(-50%,-100%);font:600 12px system-ui,sans-serif;color:#0b2a26;background:#5fd6c6;border-radius:999px;padding:2px 8px;box-shadow:0 1px 6px rgba(0,0,0,.4);white-space:nowrap}'
      + '#tjMark:after{content:"";position:absolute;left:50%;bottom:-5px;margin-left:-5px;border:5px solid transparent;border-bottom:0;border-top-color:#5fd6c6}';
    document.head.appendChild(st); TJ_MARK = document.createElement('div'); TJ_MARK.id = 'tjMark'; document.body.appendChild(TJ_MARK);
  }
  const txt = '★ ' + tjFirst(TJ_NOW.lead); if (TJ_MARK.textContent !== txt) TJ_MARK.textContent = txt;
  tjV.set(A.x, (A.y || 0) + (A.pose === 'sit' || /^sit/.test(A.pose || '') ? 1.55 : 2.1), A.z).project(camera);
  const vis = tjV.z < 1 && Math.abs(tjV.x) < 1.05 && Math.abs(tjV.y) < 1.05;
  TJ_MARK.style.display = vis ? 'block' : 'none';
  if (vis) TJ_MARK.style.transform = 'translate(' + Math.round((tjV.x + 1) * innerWidth / 2) + 'px,' + Math.round((1 - tjV.y) * innerHeight / 2 - 6) + 'px) translate(-50%,-100%)';
}
// Name on the beam (0.70.0, the user's): you're told to tap the beam; tapped while it's on, you walk under its west end
// (5-beam-1) and paint for a few minutes; then your name is up (trace nameYours, as before), you've joined, the crew there
// say well done (the head writer's 'beam.congrats' lines through lineFor, else ours) and, a couple of ship minutes later,
// the gathering breaks up: everyone at it goes on to the rest of their evening (TJ_FREE, read by tradWhere).
const TJ_CHEER = ['Well done! Welcome to Works.', 'There it is. Up with the rest of us.', 'Looks good up there.', 'Big letters. Good.'];
let TJ_FREE = null;                                      // { ids: Map(id -> the end of their tradition segment), at, until }
// painting your name (0.71.3, the user's playtest 2: "couldn't tap the Name Beam": the beam is a thin target high on the
// wall): a tap on the beam or on the floor within BEAM_REACH tiles of the beam's spot starts it (its leader still only says to)
const BEAM_REACH = 2.5;
const beamOn = () => !!TJ_NOW && TRAD_JOIN[TJ_NOW.e.id].act === 'beam' && PLACE_OF.has('5-beam-1') && !(typeof ACT !== 'undefined' && ACT && ACT.o && ACT.o.beam);
function beamPaint() {
  if (!beamOn()) return false;
  const e = TJ_NOW.e;
  actStart('tj:' + e.id, '5-beam-1', { pose: 'work', title: e.name, beam: e.id + '@' + e.day, company: 0,
    after: tradWords(e, 'paint', {}) || 'Zeke hands you the pen. You paint your name, big letters, at the end of the row.' });
  return true;
}
PLAYER_TAPS.push((it, at) => !!it && it.t === 'The beam' && beamPaint());
function beamFloorTap(point) {                           // section 15's playerFloorTap asks first
  if (!point || !beamOn() || deckDef.num !== 5) return false;
  const sp = placeSpot('5-beam-1'); return !!sp && Math.hypot(point.x - sp.x, point.z - sp.z) <= BEAM_REACH && beamPaint();
}
let BEAM_CHEERS = [];                                    // [{ c: agent, text, at: real ms }]: the welcomes, said in turn
function tradBeamFrame() {
  while (BEAM_CHEERS.length && simNow() >= BEAM_CHEERS[0].at) { const b = BEAM_CHEERS.shift(); if (b.c.h && DECK_CREW.includes(b.c) && typeof bubbleSay === 'function') bubbleSay(b.c.h, b.text, 4); }
  const A = typeof ACT !== 'undefined' ? ACT : null;
  if (!A || !A.o.beam || A.o.painted || !(A.phase === 'do' || A.phase === 'out') || A.done < A.def.mins) return;
  A.o.painted = true;
  const now = shipNow(), d = Math.floor(now / 1440) + 1, e = eventsOn(d).find(x => x.id + '@' + d === A.o.beam); if (!e) return;
  eventJoin(e, d, now, tradWords(e, 'notice', {}) || 'Name on the beam: your name is up, beside everyone who has served in Works. The crew cheer. Social and leisure up.');
  const there = DECK_CREW.filter(c => c.p && c.p.id && (o => o && o.now && o.e.id === e.id)(eventOf(c.p, now)));
  BEAM_CHEERS = there.slice().sort((x, y) => Math.hypot(x.x - A.x, x.z - A.z) - Math.hypot(y.x - A.x, y.z - A.z)).slice(0, 8).map((c, k) => {   // everyone there, one after another (playtest 2, 0.71.3; was the nearest four at once)
    let l = null; try { l = typeof lineFor === 'function' && lineFor(c.p.id, 'beam.congrats', {}); } catch (x) { l = null; }
    return { c, text: l && l.text || TJ_CHEER[k % TJ_CHEER.length], at: simNow() + k * 1600 };
  });
  const ids = new Map();
  for (const c of there) { const sg = planDay(c.p, d).find(x => evTagId(x.tag) === e.id && x.from <= now && now < x.to); if (sg) ids.set(c.p.id, sg.to); }
  TJ_FREE = { ids, at: now + 2, until: (d - 1) * 1440 + e.to + 30 };
}
// the beam's names (0.70.0, for the deck architect's WALL_KIT.nameBeam; all first names, the user's): -> [{ id, name, day }]
// of each new Works hand whose Name on the beam (name-on-the-beam-new: the Monday after their rotation) has begun by
// `now`, oldest first. Yours is DECK_DRESS.nameYours (the trace). Pure: the rotations and the calendar only
function beamNew(now = shipNow(), recent) {   // recent: only rotations in the last 8 days (once a ship minute)
  let rots; try { rots = ROSTER_ROTATIONS; } catch (e) { return []; }
  const out = [], today = Math.floor(now / 1440) + 1, m = now - (today - 1) * 1440;
  for (const r of rots || []) for (let d = r.day + 1; d <= r.day + 7 && d <= today && !(recent && r.day < today - 8); d++) {
    const e = eventsOn(d).find(x => x.id === 'name-on-the-beam-new'); if (!e) continue;
    if (d === today && m < e.from + 10) break;
    for (const p of e.honorees) out.push({ id: p.id, name: p.name.split(' ')[0], day: d });
    break;
  }
  return out;
}
// their names go up as theirs begins (in play and on skips): a trace { id: 'nameNew', day, name } each, which the deck
// architect's DECK_DRESS.nameNew draws on the beam beside yours (0.47.6: the newest three). Pushed directly: traceAdd
// keeps one per id
let BEAM_ALL = false;                                    // the first time, every rotation so far (an older save)
function beamTraces(now) {
  const recent = BEAM_ALL; BEAM_ALL = true;
  for (const x of beamNew(now, recent)) if (!SHIP.traces.some(t => t && t.id === 'nameNew' && t.day === x.day && t.name === x.name)) SHIP.traces.push({ id: 'nameNew', day: x.day, name: x.name });
}
SIM_ADVANCE.push((from, to) => { BEAM_ALL = false; beamTraces(to); });
// the HUD's Tracked list (seat U): its arrow for a tradition asks tradGoal(x) first (x: the device's day item, { kind:
// 'tradition', tkind: the tradition's id, deck, room, ... }). One you could tap to join, on now with its leader on this
// deck: the leader (the beam: the beam); else null (the room, as before)
function tradGoal(x) {
  if (!x || !TJ_NOW || TJ_NOW.e.id !== (x.tkind || String(x.id || '').split('@')[0])) return null;
  const s = TRAD_JOIN[TJ_NOW.e.id], name = tjFirst(TJ_NOW.lead), label = tradWords(TJ_NOW.e, 'tip', { name }) || (s.act === 'beam' ? 'Tap the beam to paint your name' : 'Tap ' + name + ' to ' + s.verb);
  return s.act === 'beam' ? { deck: 5, item: /^The beam$/, label, tj: TJ_NOW.key } : { deck: deckDef.num, crew: TJ_NOW.lead, label, tj: TJ_NOW.key };
}
// the walks (Lap of the Wren, the Lantern walk): joined, the leader sets off round the promenade loop (the deck
// architect's 3-lap-1..12, in walking order) and you fall in behind them, then up to TJ_LINE of the others at it, each
// behind the one ahead: one line. Section 14's whereIs asks tradWhere (in play only) and section 10's escortStep walks
// them ('lead' waits for you; 'follow' with `after` follows the person ahead). You walk on your own: tap anywhere or
// steer and you drop out. One lap, then everyone goes back to their spots. TJ_WALK: { e, lead, path, k, n, roles, cb }
const TJ_LINE = 24, TJ_OVER = 15,   // 0.70.6: everyone at it walks (the user's 'everyone walks the lap'); left standing on the loop they blocked your way (X)
      TJ_LOOP = Array.from({ length: 12 }, (_, k) => '3-lap-' + (k + 1));
let TJ_WALK = null, TJ_WALK_T = 0;
const TJ_DT = (() => { let t0 = performance.now(); return () => { const t = performance.now(), d = Math.min(.1, (t - t0) / 1000); t0 = t; return d; }; })();   // real seconds since the last frame
function tradWalkStart(e, lead) {
  const a = tjAgent(lead), path = TJ_LOOP.filter(id => PLACE_OF.has(id));
  if (!a || path.length < 4) return false;
  const cp = id => { const s = placeSpot(id); return cellPos(...s.walk); };
  const k0 = path.map((id, k) => [k, Math.hypot(cp(id).x - a.x, cp(id).z - a.z)]).sort((x, y) => x[1] - y[1])[0][0];
  const now = shipNow(), others = DECK_CREW.filter(c => c !== a && c.p && c.p.id && (o => o && o.now && o.e.id === e.id)(eventOf(c.p, now)))
    .sort((x, y) => Math.hypot(x.x - a.x, x.z - a.z) - Math.hypot(y.x - a.x, y.z - a.z)).slice(0, TJ_LINE);
  const roles = new Map([[lead, { mode: 'lead', to: path[(k0 + 1) % path.length] }]]);
  others.forEach((c, i) => roles.set(c.p.id, { mode: 'follow', after: i ? others[i - 1] : null }));
  TJ_WALK = { e, lead, path, k: k0 + 1, n: 0, roles, cb: () => {}, end: (e.day - 1) * 1440 + e.to + TJ_OVER };   // a lap begun late may finish a little after the end
  return true;
}
function tradWalkEnd(why) {
  const W = TJ_WALK; if (!W) return; TJ_WALK = null;
  if (why === 'done') { if (typeof leisureAdd === 'function') leisureAdd(5, 'tradition'); toast(W.e.name, tradWords(W.e, 'done', {}) || 'Round the whole promenade and back where you started. A good lap.'); }
  else if (why === 'left') toast(W.e.name, tradWords(W.e, 'left', {}) || 'You drop out of the line. They wave you off.');
}
function tradWalkFrame(dt) {
  const W = TJ_WALK; if (!W) return;
  const a = tjAgent(W.lead);
  if (!a || deckDef.num !== 3 || shipNow() >= W.end) { tradWalkEnd('over'); return; }
  if ((player.path.length && player.onArrive !== W.cb) || player.steer || (typeof ACT !== 'undefined' && ACT)) { tradWalkEnd('left'); return; }
  const lw = cellPos(...placeSpot(W.path[W.k % W.path.length]).walk);
  if (Math.hypot(lw.x - a.x, lw.z - a.z) < .6) {            // the leader is at the next turn: on to the one after
    W.k++; W.n++;
    if (W.n >= W.path.length) { tradWalkEnd('done'); return; }
    W.roles.get(W.lead).to = W.path[W.k % W.path.length];
  }
  TJ_WALK_T -= dt; if (TJ_WALK_T > 0) return; TJ_WALK_T = .3;
  const p = player.obj.position;
  if (Math.hypot(p.x - a.x, p.z - a.z) > 1.6) {             // keep up: a tile or so behind them
    const f = a.face || 0, g = nearestOpen(a.x - Math.sin(f) * 1.1, a.z - Math.cos(f) * 1.1, player);
    if (g && (!player.goal || K(player.goal) !== K(g))) player.goTo(g, W.cb);
  }
}
// section 14's whereIs, first after a visit: the walk's roles (escort-shaped, so section 10 walks them), else null
function tradWhere(p, t) {
  const ws = REC_DECK ? wsoWhere(p, t) : null; if (ws) return ws;   // Winner Stays On: the two on court (0.83.1, RA)
  if (TJ_FREE && t >= TJ_FREE.at) {                      // the beam's crowd breaks up: on to what comes after it
    if (t >= TJ_FREE.until) TJ_FREE = null;
    else { const end = TJ_FREE.ids.get(p.id); if (end != null && t < end) return planWhere(p, end); }
  }
  const r = TJ_WALK && TJ_WALK.roles.get(p.id);
  if (!r) return null;
  return { deck: deckDef.num, act: 'intro', type: null, placeId: null, moving: false, from: t - 1, until: t + 1, tag: 'escort', escort: r };
}
// Quiz night's mini-game (0.34.51, the user, 2026-10-18): when you join, Tomas asks you three questions about the ship
// on the choice card (dialogueShow), 3-4 answers each, one right; a remark either way, no fail, a little leisure for
// each right one. The head writer's pool (content/banks/quiz.lines): quiz.q<n>.text and quiz.q<n>.a1 (always the right
// one) to .a4, shown shuffled, n from 1 up; Tomas's quiz.open, quiz.right, quiz.wrong ({answer}), quiz.done ({n}),
// quiz.done.perfect and quiz.done.zero. Three a night,
// the same for a given day, no repeats until the pool is used: a fixed hash order of the pool, read three at a time
// by the week. No pool in the build: no game (the join toast as before). Nothing saved
const quizH = (a, b) => (Math.imul(a + 1, 2654435761) ^ Math.imul(b + 7, 40503)) >>> 0;   // a plain hash (never R())
const quizS = s => { let h = 0; for (let i = 0; i < s.length; i++) h = Math.imul(h ^ s.charCodeAt(i), 16777619) >>> 0; return h; };   // a string's hash
function quizPick(d) {
  const pool = [];
  for (let n = 1; n < 500 && quizText('quiz.q' + n + '.text', 0); n++) {
    const q = [quizText('quiz.q' + n + '.text', 0), ...[1, 2, 3, 4].map(k => quizText('quiz.q' + n + '.a' + k, 0)).filter(Boolean)];
    if (q.length >= 4) pool.push(q);
  }
  if (pool.length < 3) return null;
  const order = pool.map((q, i) => i).sort((a, b) => quizH(a, 991) - quizH(b, 991) || a - b), n = Math.floor((d - 1) / 7);
  return [0, 1, 2].map(i => {
    const q = pool[order[(n * 3 + i) % pool.length]], right = q[1];
    return { q: q[0], right, answers: q.slice(1).sort((a, b) => quizH(d, quizS(a)) - quizH(d, quizS(b)) || (a < b ? -1 : 1)) };
  });
}
function quizText(kind, k, ctx) {
  const L = typeof LINES !== 'undefined' && LINES[kind], e = Array.isArray(L) && L.length ? L[k % L.length] : null;
  return e && typeof e.text === 'string' ? e.text.replace(/\{(\w+)\}/g, (m, w) => ctx && ctx[w] != null ? ctx[w] : m) : null;
}
function quizStart(d, now) {
  const qs = quizPick(d); if (!qs || typeof dialogueShow !== 'function' || DIALOGUE) return false;
  QUIZ_PLAYED = d; let score = 0;
  const lines = [], open = quizText('quiz.open', d);
  if (open) lines.push({ who: 'tomas', text: open });
  qs.forEach((x, i) => {
    lines.push({ who: 'tomas', prompt: x.q, label: 'Quiz night · Question ' + (i + 1) + ' of ' + qs.length, choice: x.answers.map(a => {
      const ok = a === x.right, r = quizText(ok ? 'quiz.right' : 'quiz.wrong', d + i, { answer: x.right });
      return { text: a, ok, last: i === qs.length - 1, reply: r ? { who: 'tomas', text: r } : null };
    }) });
  });
  MEETING_SCRIPTS['moment:quiz'] = { title: 'Quiz night', noCount: true, lines,
    onPick: (k, c) => {
      if (c.ok) { score++; if (typeof leisureAdd === 'function') leisureAdd(2, 'quiz'); }
      if (c.last && DIALOGUE) { const t = (score === 3 && quizText('quiz.done.perfect', d, { n: score })) || (!score && quizText('quiz.done.zero', d, { n: score })) || quizText('quiz.done', d, { n: score }); if (t) DIALOGUE.queue.push({ who: 'tomas', text: t }); }
    },
    onEnd: () => { delete MEETING_SCRIPTS['moment:quiz']; QUIZ_LAST = { day: d, score }; } };
  return dialogueShow('moment:quiz', { id: 'moment:quiz', who: ['tomas'], at: now, where: { deck: 3, room: /^Bow lounge$/ } });   // 'moment:' never counts toward a commendation
}
let QUIZ_LAST = null, QUIZ_PLAYED = null;               // the last game's score (events_check reads it); the day a game last opened (once a night)
// decor: a few cheap props on the deck while an event is on (from 30 minutes before to 15 after), built on demand,
// added to the deck's root (so a deck change takes them away), colours through col(), no R(), no shadows
const EV_DECOR = { key: '', g: null, root: null };
const EV_MATS = {};
const evMat = c => EV_MATS[c] || (EV_MATS[c] = new THREE.MeshStandardMaterial({ color: col(c), roughness: .6 }));
const EV_KIT = {
  cake(g) {                                              // on the first long table in the mess hall, unless the galley's own is out
    if (deckDef.num !== 3 || !ROOM_BOX.M || evGalleyCake()) return;   // (section 16 bakes birthday cakes: one cake, theirs)
    const b = ROOM_BOX.M, x = X0(b.i0) + 2.6, z = Z0(b.j0) + 1.0, add = (geo, c, y) => { const m = new THREE.Mesh(geo, evMat(c)); m.position.set(x, y, z); g.add(m); return m; };
    add(new THREE.CylinderGeometry(.22, .22, .02, 20), '#e6e0d3', .783);                       // the plate
    add(new THREE.CylinderGeometry(.16, .16, .13, 20), '#f2d7a0', .858);                       // the cake
    add(new THREE.CylinderGeometry(.165, .165, .03, 20), '#f7f1e8', .917);                     // the icing
    const c = add(new THREE.CylinderGeometry(.008, .008, .07, 6), '#c45a3f', .962);            // a candle, and its flame
    const f = new THREE.Mesh(new THREE.SphereGeometry(.012, 8, 6), new THREE.MeshBasicMaterial({ color: col('#ffd27a') })); f.position.set(x, 1.005, z); g.add(f);
  },
  stalls(g) {                                            // two trestle stalls at the promenade's east end
    if (deckDef.num !== 3) return;
    for (const [i, j, s, c] of [[39, 9, 1, '#c45a3f'], [39, 12, -1, '#5fd6c6']]) {
      const x = X0(i) + 1, z = (s > 0 ? Z0(j) : Z0(j + 1)) + s * (T / 2 + .22), add = (w, h, d, cc, y, dz = 0) => { const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), evMat(cc)); m.position.set(x, y, z + dz); g.add(m); };
      add(1.5, .05, .4, '#a07a4f', .74);                 // the top
      add(1.5, .6, .02, c, .4, -s * .19);                // the cloth front, toward the promenade
      add(.5, .12, .25, '#d9a441', .83); add(.3, .2, .2, '#7a8fb0', .87);   // things to swap
    }
  },
};
// the galley's cake (section 16: SHIP.galley.cake, out on the servery from 19:30): when it's out, there's no second one
const evGalleyCake = () => !!(typeof SHIP !== 'undefined' && SHIP.galley && SHIP.galley.cake && SHIP.galley.cake.out);
function eventsDecor(now) {
  if (EV_DECOR.root !== deckRoot) { EV_DECOR.root = deckRoot; EV_DECOR.g = null; EV_DECOR.key = ''; }
  const d = Math.floor(now / 1440) + 1, m = now - (d - 1) * 1440;
  const galley = typeof galleyAdvance === 'function';   // section 16 bakes for `cake: true` events (0.29.15): their cake, not a prop
  const on = eventsOn(d).filter(e => e.ev.decor && !(galley && e.ev.cake && e.ev.decor === 'cake') && m >= e.from - 30 && m < e.to + 15).map(e => e.ev.decor), key = deckDef.num + ':' + [...new Set(on)].sort().join(',') + (evGalleyCake() ? ':galley-cake' : '');
  if (key === EV_DECOR.key) return;
  EV_DECOR.key = key;
  if (EV_DECOR.g) { deckRoot.remove(EV_DECOR.g); EV_DECOR.g.traverse(o => o.geometry && o.geometry.dispose()); EV_DECOR.g = null; }
  if (!on.length) return;
  const g = new THREE.Group(); for (const k of new Set(on)) EV_KIT[k](g);
  if (g.children.length) { deckRoot.add(g); EV_DECOR.g = g; }
}
let EV_MIN = -1;
function eventsTick() {
  eventFeelFrame();                                      // a ship-wide event's jolt and light dip (inert with none)
  tradJoinFrame(); tradWalkFrame(TJ_DT()); tradBeamFrame();               // 0.70.0: the leader's marker; a walk in one line
  if (DIALOGUE && !dialogueView().choices && performance.now() - DIALOGUE.at > DIALOGUE_AUTO) dialogueStep();
  const now = shipNow(), m = Math.floor(now);
  if (m === EV_MIN) return;
  const prev = EV_MIN;
  EV_MIN = m; eventTags();
  if (EV_LAST === null) EV_LAST = now; else if (now > EV_LAST) { eventsMail(EV_LAST, now); weekMailSend(EV_LAST, now); eventsNoted(EV_LAST, now); EV_LAST = now; } else EV_LAST = now;
  eventsDecor(now); eventsPlayer(now); tradJoinMinute(now); beamTraces(now);   // 0.70.0: the tradition you could tap to join (marker, arrow, tip)
  eventAdvance(now);                                     // a ship-wide event's phases (inert while none is due)
  eventMomentsTick(prev, m); meetingsTick(now);          // its felt moments and meetings, in play
  eventsDress(now);                                      // its dressing and the traces left by past events
  occasionsTick(now);                                    // C10: summons, invitations, progress talks
  if (REC_DECK) { recShowCue(now); recMyTalk(now); }    // the auditorium's show state for rec engineer B's recShow; your own talk's ask (0.83.1, RA)
}
// the auditorium's state for its dressing (the film screen down, the house lights, the stage pools: rec engineer B's
// recShow(state), which RA only calls): 'film' | 'talent' | 'allhands' | 'talk' (either Wren talk) | null, every ship minute
// (RB2: the same state again does nothing; null ends the show; looks only)
let REC_SHOW_CUE = { s: undefined, deck: null };            // (0.83.3: renamed from REC_SHOW / recShowTick, which are rec engineer B's in 8c)
function recShowCue(now) {
  const on = id => tradOn(id, now), st = on('rec-film-night') ? 'film' : on('rec-talent-night') ? 'talent' : on('rec-all-hands') ? 'allhands' : on('rec-chiefs-talk') || on('rec-wren-talk') ? 'talk' : null;
  const dk = typeof deckDef !== 'undefined' && deckDef ? deckDef.num : null;
  REC_SHOW_CUE = { s: st, deck: dk };                    // sent every ship minute (RB2's recShow does nothing for the same state)
  if (typeof recShow === 'function') try { recShow(st); } catch (e) { /* B's to mend */ }
}
// your own talk (the traditions plan: once you're an Engine Specialist, after the career arc, you're asked to give a small
// talk, "What I learned in my first month"): the first Monday or Thursday four or more days on with no talk and not a big
// day; the ask by Mail (the writer's words: simNote('recTalkAsked') for the bus); plans from then are made again
function recMyTalk(now) {
  const T = SHIP.rec.talk; if (T.mine != null || !SHIP.works || SHIP.works.rank !== 'specialist') return;
  const d0 = Math.floor(now / 1440) + 1; let d = d0 + 4;
  while (!([0, 3].includes(weekday(d)) && !recBigDay(d) && !recTalk(d))) d++;
  T.mine = d; EV_DAYS.clear(); for (const x of [...SHIP_DAYS.keys()]) if (x >= d) SHIP_DAYS.delete(x);
  recMail(now, 'Comms Chief Lucia Ferreira', 'mail.rec.talk.you', 'A Wren talk from you?', 'Would you give one of the small Wren talks? ' + WEEKDAYS[weekday(d)] + ' at 19:00, on the auditorium stage. Call it "What I learned in my first month". Twenty minutes, then questions. Tea provided.', { weekday: WEEKDAYS[weekday(d)] });
  if (typeof simNote === 'function') simNote('recTalkAsked', { day: d });
}
// the deck architect's dressShow (0.38.1): the running event's dressing for its phase, plus every saved trace. It does
// nothing when nothing changed and puts them back after a deck change
// a tradition's props (ties.decor: the deck architect's DECK_DRESS id, e.g. tilesNight) from 30 minutes before to 15 after
function tradDecor(now) {
  const d = Math.floor(now / 1440) + 1, m = now - (d - 1) * 1440;
  return eventsOn(d).filter(e => e.ev.ties && e.ev.ties.decor && m >= e.from - 30 && m < e.to + 15).map(e => {
    const r = e.ev.ties.tally && tallyOf(e.id, d); if (!r) return { id: e.ev.ties.decor };
    const f = Math.max(0, Math.min(1, (m - e.from) / (e.to - e.from)));   // the votes come in through the window (a chalkboard)
    return { id: e.ev.ties.decor, title: r.choices.map(tallyLabel).join(' or '), lines: r.choices.map(c => tallyLabel(c) + ': ' + Math.round(r.counts[c] * f)) };
  });
}
function eventsDress(now) {
  if (typeof dressShow !== 'function') return;
  const n = eventNow(now), e = SHIP.event, def = n && SHIP_EVENTS[n.id], c = e ? evCtx(e) : { band: 'smooth', mine: {}, you: 'Cadet' };
  const list = (def && def.dressing && def.dressing[n.phase] || []).map(x => ({ ...x, lines: x.lines ? evText(x.lines, c) : undefined }));
  dressShow(list.concat(tradDecor(now), SHIP.traces));
}
// ---- ship-wide events (Pillar 3, C6): the big ones, 2-4 days, a layer over normal life ----
// The format (plans/pillar3-plan.md, "How an event is put together" and "Shared formats"):
//   SHIP_EVENTS.<id> = { title, days, earliest, gap?, draft?,
//     phases: [{ id, at: [day, minute], clears? }],       // day 0 is the warning's day; phases in order. A phase marked
//                                                          // `clears` drops what earlier phases changed (resolution, afterglow)
//     systems:  { <phase>: { wear: { power: 2 }, effects: ['flicker'] } },   // read by section 17 through eventMod
//     routines: { <phase>: [{ who, where, rule }] },        // section 14
//     galley:   { <phase>: { menu, grab } },                // section 16
//     jobs:     { <phase>: [{ kind, where, tier }] },       // section 17
//     news:     [{ id, from, phase, seed, lines }],         // section 20 (social)
//     moments:  [{ id, phase, where, feel }],               // felt everywhere (5, 8b)
//     meetings: [{ id, phase, at: [day, min], where, script }],
//     address:  { <phase>: ['line', ...] },                 // the Captain's ship-wide address as that phase starts
//     mail:     { <phase>: { from, subject, body } },       // a notice as that phase starts
//     threads:  [{ id, label, good, bad }],                 // lower is better: <= good smoothly, >= bad roughly, else bumpily
//     traces:   { smooth: [...], bumpy: [...], rough: [...] } }
//   eventNow(t?)        -> { id, phase, day } | null          anyone may ask; null means no event
//   eventMod(kind, key) -> number | rule | true | null        null means "no change" (every reader treats it so)
//   eventScore(thread, n) / eventMine(what, n)                the simulation's and the player's part, added up
//   eventStart(id, day) / eventAdvance(t)                     start one; move it on (phases, the end, the log)
//   SHIP.event = { id, startDay, phase, threads: {}, mine: {} } | null; SHIP.eventLog; SHIP.traces   (saved)
//   captainAddress({ lines, at }), MEETING_SCRIPTS, meeting(), dialogueShow(), dialogueClose(), upcomingTraditions()
// Nothing here calls R(); when an event starts comes from schedU and the day, so a replay is identical.
const SHIP_EVENTS = {};
const EVENT_ORDER = ['ionStorm', 'diplomatic'];   // the main events with the short ones between (Part 2, "The full order")                        // the main and short events, in the plan's order (Part 2, "The full order")
const EVENT_BANDS = ['smooth', 'bumpy', 'rough'];
// ---- the ion storm (event 1; plans/pillar3-plan.md, "The main events"). The prose's Days 1-4 are days 0-3 here;
// the afterglow runs on to the end of day 5.
SHIP_EVENTS.ionStorm = {
  title: 'Ion storm', days: 6, earliest: 10, spread: 1, need: ['calder'],    // switched on (0.34.12): day 10 in a new game (a Wednesday), whoever's days off move   // need: on shift on the warning day (Calder's briefing)
  phases: [{ id: 'warning', at: [0, 360] }, { id: 'onset', at: [1, 840] }, { id: 'escalation', at: [2, 360] },
    { id: 'resolution', at: [3, 600], clears: true }, { id: 'afterglow', at: [3, 1320], clears: true }],
  scores: { resolution: { calls: e => stormCallBacklog(e) } },   // threads section 18 scores itself, as that phase begins
  // ship traditions don't happen in these phases (no observatory night or quiz in a storm), except those in `keep`
  pause: ['onset', 'escalation'], keep: ['birthday'],
  // section 17: wear by system or machine kind; effects: 'flicker' (lights flicker), 'blackouts' (a deck at a time goes to
  // emergency lighting for 15-60 minutes, scored as the 'blackout' thread), 'commsDown' (no calls home, no outside Mail)
  systems: {
    onset: { wear: { power: 1.5, comms: 2 }, effects: ['flicker', 'commsDown'] },
    escalation: { wear: { power: 2, comms: 3, chiller: 1.5 }, effects: ['flicker', 'blackouts', 'commsDown'] },
  },
  // section 14: who: 'dept:<d>' | 'all'; where: '<deck>|<room name>' | 'type:<place type>'. rules: doubleShift (on
  // shift twice as long), patrol (Watch walks the decks), closed (nobody goes there), stayIn (that share of leisure in
  // their own quarters; where '<deck>|<room key>'), rush (everyone with a call owed goes, in `at` minutes)
  routines: {
    onset: [{ who: 'dept:command', rule: 'doubleShift' }, { who: 'dept:helm', rule: 'doubleShift' }, { who: 'dept:watch', rule: 'patrol' },
      { where: '3|L', name: 'the bow lounge', rule: 'closed' }, { where: 'type:callhome', rule: 'closed' }, { who: 'all', rule: 'stayIn', share: .4 }],
    escalation: [{ who: 'dept:command', rule: 'doubleShift' }, { who: 'dept:helm', rule: 'doubleShift' }, { who: 'dept:watch', rule: 'patrol' },
      { where: '3|L', name: 'the bow lounge', rule: 'closed' }, { where: 'type:callhome', rule: 'closed' }, { who: 'all', rule: 'stayIn', share: .5 }],
    resolution: [{ where: 'type:callhome', rule: 'rush', at: [600, 1080] }],
  },
  needs: { escalation: { sleep: .8, social: 1.2 } },    // sections 14 and 15: energy refills slower, social drains faster
  // section 16 (the galley's keys, 0.29.18): menu, cook (time multiplier), grab (shelf multiplier), trays (to the bridge)
  galley: { escalation: { menu: 'stormStew', cook: .75, grab: 1.5, trays: 6 } },
  // section 17 posts them, tagged event: 'ionStorm'. at: the minute that phase's day they go up. stops: a place id,
  // or a room and place types, or a machine kind on a deck (the nearest of that kind)
  jobs: {
    warning: [
      { id: 'stormLounge', title: 'Storm prep: secure the lounge glassware and bar', tier: 1, at: 510,
        stops: [{ deck: 3, room: /^Bow lounge$/, types: ['lounge-seat'], mins: 30, tag: 'secure' }] },
      { id: 'stormBallasts', title: 'Storm prep: fit shielded lamp ballasts', tier: 1, at: 510, parts: ['lamp', 'lamp'],
        stops: [{ deck: 3, machine: 'lights', mins: 20, tag: 'lamp' }, { deck: 4, machine: 'lights', mins: 20, tag: 'lamp' }] },
      { id: 'stormBatteries', title: 'Storm prep: carry battery packs to the bridge', tier: 1, at: 510, bring: 'two battery packs',
        stops: [{ placeId: '5-parts-1', mins: 5, tag: 'pickup' }, { placeId: '1-works-1', mins: 10, tag: 'drop' }] },
      { id: 'stormJunctions', title: 'Storm prep: service the power junctions', tier: 3, at: 540,
        stops: [{ deck: 5, machine: 'junction', mins: 30, tag: 'service' }] },
    ],
    // (the bridge trays are the galley's own cart run at 18:00, from galley.trays: one run, the lead's call)
    afterglow: [
      { id: 'stormTidy', title: 'Put the bow lounge back together', tier: 1, at: 480,
        stops: [{ deck: 3, room: /^Bow lounge$/, types: ['lounge-seat'], mins: 25, tag: 'tidy' }] },
    ],
  },
  // section 20 spreads them: at [day, minute] the seed people know it (who would know first); lines may be a function of
  // the event's context (c.band, c.dark: a deck that went dark)
  news: [
    { id: 'storm-readings', from: 'sato', phase: 'warning', at: [0, 360], seed: ['dept:survey'], weight: 3,
      lines: ['Sato hasn\'t left the chart room since last night.', 'Survey says something big is coming our way.', 'They say the storm\'s the size of a moon.'] },
    { id: 'storm-prep', from: 'calder', phase: 'warning', at: [0, 540], seed: ['dept:works'], weight: 2,
      lines: ['Works is tying down everything that isn\'t bolted.', 'Calder says the lights will flicker for two days.', 'Top up your water bottle. Just in case.'] },
    { id: 'storm-bridge', from: 'vance', phase: 'onset', at: [1, 900], seed: ['dept:command', 'dept:helm'], weight: 2,
      lines: ['The bridge is on double shifts.', 'Vance hasn\'t slept. You can tell.'] },
    { id: 'storm-dark', phase: 'escalation', at: [2, 420], seed: ['dept:watch'], weight: 2,
      lines: c => [c.dark ? deckWord(c.dark) + ' went to emergency lights for a while.' : 'The lights held all morning. Fingers crossed.', 'I keep waiting for the next jolt.'] },
    { id: 'storm-stew', from: 'brennan', phase: 'escalation', at: [2, 660], seed: ['dept:galley'], weight: 1,
      lines: ['Storm stew again. One pot, no complaints.', 'Brennan\'s sending trays up to the bridge.'] },
    { id: 'storm-clear', from: 'marrow', phase: 'resolution', at: [3, 600], seed: ['all'], weight: 3,
      lines: ['It\'s over. Comms are back.', 'The queue at the booths goes round the plaza.', 'Party in the bow lounge tonight!'] },
    { id: 'storm-told', phase: 'afterglow', at: [3, 1320], seed: ['all'], weight: 2, lines: c => STORM_RETELL[c.band] },
  ],
  // felt everywhere (sections 5 and 8b: the performance engineer) and the gathering after; the addresses are below
  moments: [
    { id: 'front', phase: 'onset', at: [1, 840], where: 'shipwide', feel: ['jolt', 'lightsDip', 'flicker'], len: 6 },
    { id: 'surge', phase: 'escalation', at: [2, 680], where: 'shipwide', feel: ['jolt', 'lightsDip'], len: 4 },
    { id: 'party', phase: 'resolution', at: [3, 1140], len: 120, where: { venue: 'bow-lounge', deck: 3, room: /^Bow lounge$/ }, gathering: true, who: .7, anim: 'talk' },
  ],
  // meetings with dialogue: who: ROSTER ids, or 'works:2' (two Works crew on shift there, the script's tech1 and tech2)
  meetings: [
    { id: 'stormBriefing', phase: 'warning', at: [0, 555],   // 09:15 (0.70.1: the day shift starts at 09:00, playtest 1; was 08:15)
      len: 12, where: { venue: 'works-bay', deck: 5, room: /^Works bay$/ }, script: 'calderStorm', who: ['calder', 'works:2'],
      notify: 'Chief Calder\'s storm briefing, at the job board in the Works bay at 09:15.' },
    { id: 'allClear', phase: 'resolution', at: [3, 600], len: 12, where: { venue: 'observation', deck: 1, room: /^Observation room$/ }, script: 'captainAllClear', who: ['marrow', 'vance', 'sato', 'holt', 'calder'] },
  ],
  address: {
    onset: ['This is the Captain. We\'re in it.', 'Expect flickers, and no calls home for a while.', 'Look after each other. Marrow out.'],
    resolution: c => ['This is the Captain. The storm has passed.',
      { smooth: 'You kept this ship bright and fed through two hard days. Thank you, all of you.', bumpy: 'It wasn\'t smooth, but we came through it together. Thank you.',
        rough: 'It was a hard storm, and you got us through it. Rest when you can; we\'ll put the ship right together.' }[c.band],
      'Comms are back and the booths are open. And there\'s a party in the bow lounge at 19:00. Marrow out.'],
  },
  mail: {
    warning: { from: 'Chief Ines Calder', subject: 'Storm prep', body: 'Ion storm due tomorrow afternoon. Before then: secure loose fittings, top up the filters, check the battery packs. Storm jobs are on the board.' },
    onset: { from: 'Commander Teo Vance', subject: 'Storm stations', body: 'The bridge is on double shifts and the bow lounge is closed. The call-home booths are off line until it\'s over.' },
  },
  // lower is better. Who scores what (the lead, 2026-10-16): blackout minutes, section 17; meals spoiled and the bridge
  // crew's hours on double shift without a hot meal, section 16; the call-home backlog (hours of queue), section 18
  threads: [{ id: 'blackout', label: 'Keep the lights on', good: 60, bad: 200 }, { id: 'spoiled', label: 'Nothing spoiled', good: 10, bad: 60 },
    { id: 'bridgeHungry', label: 'A fed bridge', good: 6, bad: 14 }, { id: 'calls', label: 'Calls home', good: 3, bad: 6 }],
  // dressing while a phase is on (dressShow, the deck architect's DECK_DRESS ids): a sign-up sheet, the party's bunting
  dressing: {
    warning: [{ id: 'signupWorks', title: 'Storm prep: who\'s doing what', lines: c => ['I. Calder: the board', 'Bay crew: lounge, ballasts'].concat(c.mine['wants:stormBatteries'] ? [c.you + ': batteries to the bridge'] : c.mine['wants:stormLounge'] ? [c.you + ': the lounge'] : []) }],
    resolution: [{ id: 'partyLounge', title: 'All clear!' }], afterglow: [{ id: 'partyLounge', title: 'All clear!' }],
  },
  traces: { smooth: ['stormRosterTeaCorner'], bumpy: ['relayScorch'], rough: ['relayScorch', 'tapedPanel'] },
  debrief: { from: 'Chief Ines Calder',
    smooth: 'We came through the storm in good order: short blackouts, nothing lost from the cold store, and a bridge crew that ate on time.',
    bumpy: 'We came through. A relay burnt out on the bridge and a few decks spent time on emergency lights. I\'ll have it patched by the end of the week.',
    rough: 'That was a hard one. Long blackouts, a scorched relay room, food binned. We\'ll be putting the ship right for a while. Rest first.',
    mine: c => c.mine.jobs ? ' Thanks for the ' + (c.mine.jobs > 1 ? c.mine.jobs + ' storm jobs' : 'storm job') + ' you took on; it showed.' : '' },
};
const STORM_RETELL = {
  smooth: ['The lights only went once on our deck, thanks to Works.', 'Best storm I\'ve been through. Is that a thing you can say?', 'Somebody pinned the storm roster up in the tea corner.'],
  bumpy: ['We lost a relay on the bridge. Calder was not pleased.', 'An hour on emergency lights. I read by torch.', 'Could\'ve been worse. Could\'ve been a lot better.'],
  rough: ['The relay room got scorched. You can still smell it.', 'I didn\'t sleep for two nights.', 'Half the cold store went in the bin.'],
};
// the call-home backlog (section 18's thread): when comms return, everyone owed a call queues for the booths, about 40
// minutes each. Owed: the calls-home crew, and about a third of the rest by hash; slower with the comms system worn
// who's owed a call home when comms come back (section 14's 'rush' rule uses it too)
const callOwed = (p, startDay) => (habitsOn(p, startDay + 3) || []).includes('calls-home') || schedU(p.seed, startDay, 336) < .33;
function stormCallBacklog(e) {
  const ppl = schedPeople().filter(p => p.rank !== 'guest');
  const owed = ppl.filter(p => callOwed(p, e.startDay)).length;
  const booths = Math.max(1, placesOf(['callhome']).length), comms = typeof shipSystems === 'function' ? shipSystems().comms : 100;
  return Math.round(owed * 40 / booths / 60 * (1 + (100 - comms) / 100) * 10) / 10;
}
// ---- the diplomatic visit (event 2; plans/pillar3-plan.md, "The main events"): a Veyli delegation of four (GUESTS with
// event 'diplomatic', section 9) aboard for five days. Day 0 Vance's warning; day 2 10:00 the greeting in the shuttle
// bay; formal dinners on days 3 and 5 in the Captain's quarters; day 7 the gift exchange at 09:00 and the farewell at
// 10:00, when the guests leave (eventGuestDays: guestsArrive 2, their stay 5); the afterglow to the end of day 8
SHIP_EVENTS.diplomatic = {
  title: 'Diplomatic visit', days: 9, gap: 7, need: ['vance'], guestsArrive: 2, draft: true,   // on when the lead says (events_check runs it)
  phases: [{ id: 'warning', at: [0, 540] }, { id: 'onset', at: [2, 600] }, { id: 'escalation', at: [3, 360] },
    { id: 'resolution', at: [7, 540], clears: true }, { id: 'afterglow', at: [7, 720], clears: true }],
  pause: ['onset'], keep: ['birthday'],                  // the greeting day is all hands; traditions carry on after it
  systems: {
    warning: { wear: { washer: 1.5 } },                  // dress uniforms through the laundry
    onset: { effects: ['guests'] },                      // eventMod('effect', 'guests'): the delegation is aboard (section 17's coldCabins)
    escalation: { wear: { heat: 1.3, heater: 1.5 }, effects: ['guests'] },   // the guest cabins' heaters turned up: the Veyli like it warm
  },
  routines: {
    onset: [{ who: 'dept:watch', rule: 'patrol' }],
    escalation: [{ where: '2|C', name: 'the Captain\'s quarters', rule: 'closed' }],   // set for the formal dinners
  },
  // the galley: guests at the servery all visit long; the formal dinners on days 3 and 5 (a function of eventNow: { day })
  galley: {
    onset: { extra: 4 },
    escalation: { extra: 4, batch: n => n.day === 3 || n.day === 5 ? { meals: 10, label: 'the Veyli dinner in the Captain\'s quarters' } : null, herbs: true },
  },
  jobs: {
    warning: [
      { id: 'veyliSuite', title: 'Visit prep: make up the visitors\' cabin and turn its heater up', tier: 1, at: 600,
        stops: [{ placeId: '2-armchair-8', mins: 25, tag: 'tidy' }] },
      { id: 'veyliLamp', title: 'Visit prep: fix the lamp in the Captain\'s dining room', tier: 1, at: 600, parts: ['lamp'],
        stops: [{ placeId: '2-captable-1', mins: 15, tag: 'lamp' }] },
      { id: 'veyliGifts', title: 'Visit prep: bring the gift crates up from the hold', tier: 1, at: 660, bring: 'a crate of gifts',
        stops: [{ placeId: '5-hold-1', mins: 5, tag: 'pickup' }, { placeId: '1-conf-1', mins: 10, tag: 'drop' }] },
    ],
    escalation: [
      { id: 'veyliHerbs', title: 'Pick herbs in the garden for the Veyli dinner', tier: 1, at: 840,
        stops: [{ placeId: '3-tend-1', mins: 20, tag: 'pick' }, { placeId: '3-cold-1', mins: 5, tag: 'drop' }] },
    ],
  },
  news: [
    { id: 'veyli-coming', from: 'vance', phase: 'warning', at: [0, 540], seed: ['dept:command'], weight: 3,
      lines: ['A Veyli delegation is coming aboard. Four of them.', 'Dress uniforms. Everyone. Vance was very clear.'] },
    { id: 'veyli-holt', from: 'holt', phase: 'warning', at: [0, 780], seed: ['dept:watch'], weight: 2,
      lines: ['Holt says he\'ll be polite. Holt says a lot of things.', 'Watch is doubling up on the Deck 2 corridor.'] },
    { id: 'veyli-moleth', phase: 'escalation', at: [3, 600], seed: ['dept:works'], weight: 2,
      lines: ['One of the Veyli has forty questions for Calder. Forty.', 'Their scholar wants to see the engine room. Torres is thrilled.'] },
    { id: 'veyli-clash', from: 'holt', phase: 'escalation', at: [4, 1260], seed: ['dept:watch', 'dept:command'], weight: 3,
      lines: ['Holt and the Veyli pilot had words about the Watch rota.', 'Something about who stands where at the door. It got frosty.'] },
    { id: 'veyli-told', phase: 'afterglow', at: [7, 720], seed: ['all'], weight: 2, lines: c => VEYLI_RETELL[c.band] },
  ],
  moments: [
    { id: 'farewell', phase: 'resolution', at: [7, 600], len: 30, where: { venue: 'shuttle-bay', deck: 5, room: /^Shuttle bay$/ }, gathering: true, who: .8, anim: null,   // mid-morning: only those off shift can come
      name: 'The Veyli farewell', ask: 'The Veyli leave at ten. I want to see them off.', here: 'Safe travels.', thanks: 'You line the shuttle bay to see the delegation off.' },
  ],
  meetings: [
    { id: 'veyliGreeting', phase: 'onset', at: [2, 600], len: 20, where: { venue: 'shuttle-bay', deck: 5, room: /^Shuttle bay$/ }, script: 'veyliGreeting',
      who: ['marrow', 'vance', 'saruth', 'teshavi', 'kesrin'], notify: 'The Veyli delegation arrives in the shuttle bay (Deck 5) at 10:00.' },
    { id: 'veyliGifts', phase: 'resolution', at: [7, 540], len: 20, where: { venue: 'observation', deck: 1, room: /^Observation room$/ }, script: 'veyliGiftExchange',
      who: ['marrow', 'saruth', 'teshavi', 'moleth'] },
  ],
  address: {
    onset: ['This is the Captain. Our Veyli guests are aboard.', 'They are here as friends. Make them welcome, answer their questions, and mind your manners.', 'Marrow out.'],
    resolution: c => ['This is the Captain. The delegation leaves us this morning.',
      { smooth: 'Speaker Teshavi tells me she has rarely been made so welcome. Thank you.', bumpy: 'It was a busy five days, and you carried it well. Thank you.',
        rough: 'Not everything went to plan. They leave as friends all the same, and we\'ll do better next time.' }[c.band], 'Marrow out.'],
  },
  mail: {
    warning: { from: 'Commander Teo Vance', subject: 'A Veyli delegation', body: 'A Veyli delegation of four arrives in two days, 10:00 in the shuttle bay. Dress uniforms for the greeting. The visitors\' cabin and the guest cabins on Deck 4 need making up, and the Veyli like it warm: heaters up. Visit jobs are on the Works board.' },
  },
  // lower is better. Who scores what (to agree with the lead): late dinners (minutes, galley 16), cold guest cabins
  // (hours below comfort, systems 17), dinners without herbs (galley 16, from the garden), discourtesy (section 20 from
  // crew mood toward the guests, Holt above all; plus meeting choices here)
  threads: [{ id: 'dinnersLate', label: 'Dinners on time', good: 10, bad: 60 }, { id: 'coldCabins', label: 'Warm guest cabins', good: 4, bad: 16 },
    { id: 'noHerbs', label: 'Herbs from the garden', good: 0, bad: 2 }, { id: 'discourtesy', label: 'Courtesy', good: 2, bad: 6 }],
  dressing: { warning: [{ id: 'signupMess', title: 'The greeting line: volunteers', lines: c => ['T. Vance', 'B. Holt (under protest)'].concat(c.mine['wants:veyliSuite'] ? [c.you] : []) }] },
  traces: { smooth: ['veyliCordSculpture'], bumpy: [], rough: [] },
  debrief: { from: 'Commander Teo Vance',
    smooth: 'The delegation left delighted. Dinners on time, warm cabins, and not one incident at the door. The Speaker\'s gift hangs in the bow lounge.',
    bumpy: 'The delegation left on good terms. A cold cabin and a late dinner, but nothing that will make the Concord\'s reports.',
    rough: 'The delegation left politely, which is the most I can say. Cold cabins, a bare herb rack and Chief Holt\'s remarks. We will do better.',
    mine: c => c.mine.jobs ? ' Your work on the visit was noticed.' : '' },
};
const VEYLI_RETELL = {
  smooth: ['Did you see the cord sculpture? It moves when the vents come on.', 'The Speaker laughed at one of Brennan\'s jokes. Actually laughed.'],
  bumpy: ['The Veyli dinner was late. Brennan blamed the herbs.', 'Holt\'s still telling the door story. It gets longer every time.'],
  rough: ['Their cabin was freezing the first night. Nobody\'s owning up.', 'Holt and their pilot still won\'t look at each other.'],
};
// the ship-wide events' gathering moments, shaped like traditions (EV_SHIPWIDE, read by eventsOn); each its own
// hash key k (the storm's party 340, then 351 up)
for (const [id, def] of Object.entries(SHIP_EVENTS)) for (const m of def.moments || []) if (m.gathering) EV_SHIPWIDE.push({
  id: m.id, name: m.name || 'All-clear party', k: EV_SHIPWIDE.length ? 350 + EV_SHIPWIDE.length : 340, when: { ship: id, day: m.at[0] }, at: [m.at[1], m.at[1] + m.len], min: 25, hold: [], venue: m.where.venue,
  where: [{ deck: m.where.deck, room: m.where.room, types: ['lounge-seat'] }, { deck: m.where.deck, room: m.where.room, types: ['bench', 'common-room'] }],
  who: () => m.who, anim: () => m.anim || null, ask: m.ask || 'Party in the bow lounge at seven. We earned it.', here: m.here || 'To the Wren, and to clear skies!',
  thanks: m.thanks || 'You squeeze into the bow lounge for the all-clear party. Someone hands you a cup.', from: 'Commander Teo Vance' });
// the saved state (section 13's SAVE_EXTRA): ship.event, ship.eventLog, ship.traces
SHIP.event = null; SHIP.eventLog = []; SHIP.traces = [];
(() => {
  const s = SAVED && SAVED.ship, e = s && s.event;
  if (e && typeof e === 'object' && SHIP_EVENTS[e.id] && Number.isInteger(e.startDay)) SHIP.event = { id: e.id, startDay: e.startDay, phase: e.phase || null, threads: { ...(e.threads || {}) }, mine: { ...(e.mine || {}) } };
  if (s && Array.isArray(s.eventLog)) SHIP.eventLog = s.eventLog.filter(x => x && typeof x.id === 'string');
  if (s && Array.isArray(s.traces)) SHIP.traces = s.traces.filter(x => typeof x === 'string' || (x && typeof x.id === 'string' && Number.isInteger(x.day)));   // an id, or { id, day } (a trace that grows: your seedling)
})();
SAVE_EXTRA.push(s => { s.ship.event = SHIP.event; s.ship.eventLog = SHIP.eventLog; s.ship.traces = SHIP.traces; });
// where a running event is at minute t: its day (0 = the warning's) and the last phase begun
// Pure for any t: it reads the running event, the log of past ones and the next one due, so a replay of a past or
// future day (the galley's, the schedules') sees the same event as play did or will
function eventNow(t = shipNow()) {
  const e = typeof SHIP !== 'undefined' && SHIP.event, spans = [];
  if (e && SHIP_EVENTS[e.id]) spans.push({ id: e.id, startDay: e.startDay });
  if (typeof SHIP !== 'undefined' && SHIP.eventLog) for (const l of SHIP.eventLog) spans.push(l);
  if (!e) { const due = eventDueDay(); if (due) spans.push({ id: due.id, startDay: due.day }); }
  for (const sp of spans) {
    const def = SHIP_EVENTS[sp.id]; if (!def) continue;
    const rel = t - (sp.startDay - 1) * 1440; if (rel < 0 || rel >= def.days * 1440) continue;
    let ph = null; for (const p of def.phases) if (rel >= p.at[0] * 1440 + p.at[1]) ph = p.id;
    if (ph) return { id: sp.id, phase: ph, day: Math.floor(rel / 1440) };
  }
  return null;
}
// what the event changes now: a phase's value, else an earlier phase's (an onset's wear carries into the escalation),
// stopping at a phase that `clears`. kinds: 'wear' and 'effect' (systems), 'routine', 'galley', 'jobs', or any other
// table on the event (def[kind][phase][key]). null: no change.
function eventMod(kind, key, t) {
  const now = eventNow(t); if (!now) return SHIP.occasions && typeof occasionMod === 'function' ? occasionMod(kind, key, t === undefined ? shipNow() : t) : null;
  const def = SHIP_EVENTS[now.id], i = def.phases.findIndex(p => p.id === now.phase);
  for (let k = i; k >= 0; k--) {
    const ph = def.phases[k].id;
    let v = null;
    if (kind === 'wear') v = def.systems && def.systems[ph] && def.systems[ph].wear ? def.systems[ph].wear[key] : undefined;
    else if (kind === 'effect') v = def.systems && def.systems[ph] && def.systems[ph].effects ? (def.systems[ph].effects.includes(key) ? true : undefined) : undefined;
    else if (kind === 'routine') v = def.routines && def.routines[ph] ? def.routines[ph].find(r => r.rule === key || r.where === key || r.who === key) : undefined;
    else { const tb = def[kind === 'jobs' ? 'jobs' : kind]; v = tb && tb[ph] ? (key === undefined ? tb[ph] : tb[ph][key]) : undefined; }
    if (typeof v === 'function' && key !== undefined) v = v(now, t);   // a value by day (the diplomatic visit's dinners)
    if (v !== undefined && v !== null) return v;
    if (def.phases[k].clears) return null;
  }
  return null;
}
// for section 14's plans, made a day at a time and cached: the event on day d, and the minute of that day each of its
// phases begins (0 for one already running at midnight). Pure, from eventNow
function eventOn(d) {
  const t0 = (d - 1) * 1440, n0 = eventNow(t0), n1 = eventNow(t0 + 1439), n = n0 || n1; if (!n) return null;
  const def = SHIP_EVENTS[n.id], sd = n0 ? d - n0.day : d - n1.day, phases = [];
  if (n0) phases.push({ id: n0.phase, from: 0 });
  for (const p of def.phases) { const at = (sd - 1 + p.at[0]) * 1440 + p.at[1] - t0; if (at > 0 && at < 1440) phases.push({ id: p.id, from: at }); }
  return { id: n.id, day: d - sd, phases };
}
// the gatherings on day d (the meetings and gathering moments), for section 14's gathering(): { id, where: venue,
// at and len in minutes of that day, who: ROSTER ids and '<dept>:N' slots, or a chance (0-1) for everyone free }
function eventGatherings(d) {
  const o = eventOn(d); if (!o) return [];
  const def = SHIP_EVENTS[o.id], out = [];
  for (const m of (def.meetings || []).concat((def.moments || []).filter(x => x.gathering))) if (m.at[0] === o.day && m.where && m.where.venue)
    out.push({ id: m.id, event: o.id, where: m.where.venue, at: m.at[1], len: m.len || 15, who: m.who, anim: m.anim || null });
  return out;
}
// a ship tradition paused by a ship-wide event (no observatory night or quiz in a storm): its start or end falls in one
// of the event's `pause` phases, and it isn't in `keep`. From eventNow, so plans made on any day agree
function eventPauses(ev, d) {
  for (const m of [ev.at[0], ev.at[1] - 1]) {
    const n = eventNow((d - 1) * 1440 + m), def = n && SHIP_EVENTS[n.id];
    if (def && (def.pause || []).includes(n.phase) && !(def.keep || []).includes(ev.id)) return true;
  }
  return false;
}
// a news seed's tokens as crew ids: 'dept:<d>' (that department), 'all' (everyone aboard), ids as they are
const newsSeed = l => [...new Set(l.flatMap(x => x === 'all' ? schedPeople().map(p => p.id) : /^dept:/.test(x) ? schedPeople().filter(p => p.dept === x.slice(5)).map(p => p.id) : [x]))];
// the deck that last went to emergency lighting in the 12 hours before t (section 17's blackoutAt), or null
function lastDark(t) { if (typeof blackoutAt !== 'function') return null; for (let k = t; k > t - 720; k -= 15) { const b = blackoutAt(k); if (b) return b.deck; } return null; }
// the context an event's texts are written against: c.band (as things stand), c.mine, c.you, c.dark
const evCtx = (e, t) => ({ dark: t === undefined ? null : lastDark(t), band: e ? eventBand(e.id, e.threads || {}) : 'smooth', mine: (e && e.mine) || {}, threads: (e && e.threads) || {}, you: (SHIP.player && SHIP.player.name) || 'Cadet',
  jobsDone: typeof yourJobsDone === 'function' ? yourJobsDone() : 0, commended: !!(SHIP.commendations && SHIP.commendations.length) });
// section 14's schedule rules at ship minute t: the whole list in force (the phase's, else an earlier phase's back to
// one that `clears`), [] when nothing's on. Rules: { who: 'dept:<d>' | 'all', where: '<deck>|<room key>' |
// 'type:<place type>', rule, share?, at? }. Pure, like eventNow
function eventRoutines(t) {
  const now = eventNow(t); if (!now) return [];
  const def = SHIP_EVENTS[now.id], i = def.phases.findIndex(p => p.id === now.phase);
  for (let k = i; k >= 0; k--) { const l = def.routines && def.routines[def.phases[k].id]; if (l) return l; if (def.phases[k].clears) return []; }
  return [];
}
// an event guest's stay (section 14, C8): [arriveDay, leaveDay] in ship days, from the event's start day (running,
// logged or next due): they arrive arriveOffset days after it starts (default the event's `guestsArrive`, else its
// onset's day) and stay `stay` days. null when that event isn't running, logged or due. Pure
function eventGuestDays(g) {
  const def = g && SHIP_EVENTS[g.event]; if (!def) return null;
  const e = SHIP.event && SHIP.event.id === g.event ? SHIP.event : [...SHIP.eventLog].reverse().find(l => l.id === g.event) || (() => { const d = eventDueDay(); return d && d.id === g.event ? { startDay: d.day } : null; })();
  if (!e) return null;
  const on = def.phases.find(p => p.id === 'onset'), off = g.arriveOffset != null ? g.arriveOffset : def.guestsArrive != null ? def.guestsArrive : on ? on.at[0] : 0;
  return [e.startDay + off, e.startDay + off + (g.stay || 1)];
}
// the threads and the player's part: other sections add to them (inert while no event runs)
function eventScore(thread, n = 1) { const e = SHIP.event; if (e) e.threads[thread] = (e.threads[thread] || 0) + n; }
function eventMine(what, n = 1) { const e = SHIP.event; if (e) e.mine[what] = (e.mine[what] || 0) + n; }
const threadBand = (th, v) => v <= th.good ? 'smooth' : v >= th.bad ? 'rough' : 'bumpy';
// the overall result: the threads' bands blended (their average, rounded)
function eventBand(id, threads) {
  const def = SHIP_EVENTS[id]; if (!def || !def.threads.length) return 'smooth';
  const v = def.threads.reduce((a, th) => a + EVENT_BANDS.indexOf(threadBand(th, threads[th.id] || 0)), 0) / def.threads.length;
  return EVENT_BANDS[Math.round(v)];
}
function eventStart(id, day) {
  if (!SHIP_EVENTS[id]) return false;
  SHIP.event = { id, startDay: day, phase: null, threads: {}, mine: {} }; return true;
}
// when the next event starts, if none is running: the first in EVENT_ORDER not yet in the log, not a draft, from its
// `earliest` day plus 0-2 days by hash, at least `gap` days (default 7) after the last one ended, then on to the first
// day its `need` people are all on shift
function eventDueDay() {
  const id = EVENT_ORDER.find(x => SHIP_EVENTS[x] && !SHIP_EVENTS[x].draft && !SHIP.eventLog.some(l => l.id === x));
  if (!id) return null;
  const def = SHIP_EVENTS[id], last = SHIP.eventLog[SHIP.eventLog.length - 1];
  const from = Math.max(def.earliest || 1, last ? last.endDay + (def.gap || 7) : 1);
  let day = from + Math.floor((def.spread != null ? def.spread : 3) * schedU(4242, from, EVENT_ORDER.indexOf(id)));   // spread: how many days it may wander (default 3)
  const need = (def.need || []).map(n => ROSTER.find(p => p.id === n)).filter(Boolean);   // on shift on the warning day
  for (let k = 0; k < 7 && !need.every(p => isWorkDay(p, day)); k++) day++;
  return { id, day };
}
// move the event on to minute t: start one when due, run each phase's actions as it begins (the address, a notice),
// and at the end score it, lay down its traces, log it and send the debrief. Returns what happened, for the checks.
function eventAdvance(t = shipNow(), quiet) {
  const out = [];
  if (!SHIP.event) { const due = eventDueDay(); if (due && t >= (due.day - 1) * 1440) { eventStart(due.id, due.day); out.push('start ' + due.id); } }
  const e = SHIP.event, def = e && SHIP_EVENTS[e.id]; if (!def) return out;
  for (const m of def.meetings || []) meeting({ id: m.id, event: e.id, where: m.where, at: (e.startDay - 1 + m.at[0]) * 1440 + m.at[1], len: m.len, who: m.who, script: m.script, notify: m.notify });
  const now = eventNow(t), end = (e.startDay - 1 + def.days) * 1440;
  for (const n of def.news || []) {                      // section 20 (social) spreads it from its seed people
    const at = (e.startDay - 1 + n.at[0]) * 1440 + n.at[1];
    if (at > t || e.mine['news:' + n.id] || typeof newsAdd !== 'function') continue;
    e.mine['news:' + n.id] = 1;
    newsAdd({ id: n.id + '@' + e.startDay, about: def.title, lines: evText(n.lines, evCtx(e, at)), weight: n.weight || 1, seed: newsSeed((n.from ? [n.from] : []).concat(n.seed || [])), born: at, kind: 'event', event: e.id, life: 2 });
  }
  if (now && now.phase !== e.phase) {
    const from = e.phase ? def.phases.findIndex(p => p.id === e.phase) + 1 : 0, to = def.phases.findIndex(p => p.id === now.phase);
    for (let k = from; k <= to; k++) {                   // every phase begun since last time, in order (a sleep can pass several)
      const ph = def.phases[k].id; out.push('phase ' + ph);
      for (const [th, f] of Object.entries((def.scores && def.scores[ph]) || {})) eventScore(th, f(e));
      if (def.address && def.address[ph]) captainAddress({ lines: evText(def.address[ph], evCtx(e)), at: (e.startDay - 1) * 1440 + def.phases[k].at[0] * 1440 + def.phases[k].at[1], quiet: quiet || k < to });
      const m = def.mail && def.mail[ph]; if (m && typeof mailSend === 'function') mailSend({ at: t, from: m.from, subject: m.subject, body: evText(m.body, evCtx(e)), quiet: !!quiet });
    }
    e.phase = now.phase;
  }
  if (t >= end) {
    const band = eventBand(e.id, e.threads), traces = (def.traces && def.traces[band]) || [];
    for (const tr of traces) if (!SHIP.traces.includes(tr)) SHIP.traces.push(tr);
    SHIP.eventLog.push({ id: e.id, startDay: e.startDay, endDay: e.startDay + def.days, band, threads: { ...e.threads }, mine: { ...e.mine } });
    if (typeof mailSend === 'function' && def.debrief && def.debrief[band]) mailSend({ at: t, from: def.debrief.from || 'Commander Teo Vance', subject: def.title + ': how it went', body: def.debrief[band] + evText(def.debrief.mine || '', evCtx(e)), quiet: !!quiet });
    const mine = e.mine || {};
    if ((mine.jobs || 0) >= 2 || ((mine.jobs || 0) >= 1 && (mine.meetings || 0) >= 1)) {   // your part: commended (Part 2, "How outcomes are scored")
      SHIP.commendations.push({ event: e.id, day: Math.floor(t / 1440) + 1 }); out.push('commended');
      if (typeof mailSend === 'function') mailSend({ at: t, from: 'Captain Odile Marrow', subject: 'Commendation: ' + def.title, body: 'For your work during the ' + def.title.toLowerCase() + ', noted on your record with thanks. Chief Calder spoke well of you.', quiet: !!quiet });
    }
    SHIP.event = null; out.push('end ' + band);
  }
  return out;
}
const traceOn = id => SHIP.traces.some(x => (x.id || x) === id);   // for the architects' trace props: a scorch mark, a plaque, a pet
// a lasting trace from a tradition you joined (`trace` on it): { id, day } once, for dressShow (your seedling grows by day)
function traceAdd(id, day) { if (id && !traceOn(id)) SHIP.traces.push({ id, day }); }
SIM_ADVANCE.push((from, to) => { eventAdvance(to, true); });

// ---- the Captain's ship-wide address: a banner across the top on every deck for about 20 seconds, copied to Mail.
// The device engineer owns the look; this is the plain stand-in. Time never stops.
let ADDRESS_EL = null, ADDRESS_T = 0;
const ADDRESSES = [];                                    // every address so far (for the checks and the Ship app)
function captainAddress({ lines, at = shipNow(), from = 'Captain Odile Marrow', quiet = false }) {
  const text = (lines || []).join(' ');
  if (REC_DECK && SHIP.event && SHIP.rec && SHIP.rec.ah == null) recFirstAllHands(at);   // the first ship-wide event's address is the first all-hands (0.83.2, RA)
  ADDRESSES.push({ at, from, text });
  if (typeof mailSend === 'function') mailSend({ at, from, subject: 'All hands', body: text, quiet: true });
  if (quiet || typeof document === 'undefined') return;
  if (typeof deviceAddress === 'function') return deviceAddress({ from, text });   // section 19's CRT banner (0.35.7)
  if (!ADDRESS_EL) {
    ADDRESS_EL = document.createElement('div');
    ADDRESS_EL.style.cssText = 'position:fixed;left:50%;top:12px;transform:translateX(-50%);max-width:min(560px,92vw);padding:10px 14px;border-radius:10px;background:rgba(14,20,24,.92);color:#e8f4ef;font:14px/1.4 system-ui,sans-serif;z-index:30;pointer-events:none;box-shadow:0 4px 18px rgba(0,0,0,.4)';
    document.body.appendChild(ADDRESS_EL);
  }
  ADDRESS_EL.innerHTML = '<div style="font-weight:600;color:#9fe0cf;margin-bottom:2px">' + from + ', to all hands</div>';
  ADDRESS_EL.appendChild(document.createTextNode(text));
  ADDRESS_EL.hidden = false; simClear(ADDRESS_T); ADDRESS_T = simTimeout(() => { if (ADDRESS_EL) ADDRESS_EL.hidden = true; }, 20000);
}

// ---- meetings with dialogue (the fourth kind of moment): scripts are data; section 19 (the device engineer) draws
// the panel; until section 19 provides deviceDialogue(view, onTap), a plain strip at the bottom stands in.
// MEETING_SCRIPTS.<id> = { title, gist, lines: [{ who, text, pose? } | { choice: [{ text, rel?, job? }, ...] }] }
const MEETING_SCRIPTS = {};
if (typeof linesMeetings === 'function') linesMeetings(MEETING_SCRIPTS);   // section 22: the baked meetings in, {me} texts made functions
const MEETINGS = [];                                     // meetings registered by events: { id, where, at, who, script }
function meeting(m) { if (m && m.id && !MEETINGS.some(x => x.id === m.id && x.at === m.at)) MEETINGS.push(m); return m; }
// At run time (0.34.9): you're there when you're in the meeting's room on its deck while it's on; then its script plays,
// line by line, tap to go on (or it moves on by itself after a few seconds; a choice waits for you). Walking out of the
// room closes it and the gist comes by Mail; if you weren't there at all, the gist comes when it ends. The panel is
// section 19's: deviceDialogue(view) when it exists (view = { title, who: the speaker's name, role, text, choices,
// and id, to, pose, i, n }; null hides it), and its taps call dialogueNext(), dialogueChoose(k) and dialogueClose();
// else the plain strip below.
let DIALOGUE = null;                                     // { id, m, cast, ctx, queue, i, at }: the script being shown
let DIALOGUE_EL = null;
const DIALOGUE_AUTO = 7000;                              // real ms before a line moves on by itself
// the cast: ROSTER ids as they are; 'works:2' -> two Works juniors on shift that day (by hash), as tech1 and tech2
function meetingCast(m) {
  const d = Math.floor(m.at / 1440) + 1, ppl = schedPeople(), cast = {};
  for (const w of m.who || []) {
    const mm = /^(\w+):(\d+)$/.exec(w);
    if (!mm) { const p = evPerson(w); if (p) cast[w] = p; continue; }
    const pool = ppl.filter(p => p.dept === mm[1] && p.rank === 'junior' && p.shift !== 'night' && isWorkDay(p, d) && !(m.who || []).includes(p.id))
      .sort((a, b) => schedU(a.seed, d, 337) - schedU(b.seed, d, 337));
    pool.slice(0, +mm[2]).forEach((p, i) => { cast['tech' + (i + 1)] = p; });
  }
  return cast;
}
const evPerson = id => schedPeople().find(p => p.id === id) || (typeof GUESTS !== 'undefined' && GUESTS.find(g => g.id === id)) || null;   // crew, Saruth, event guests
const castName = (D, who) => who === 'you' ? D.ctx.you : D.cast[who] ? D.cast[who].name : (evPerson(who) || { name: who }).name;
function dialogueShow(scriptId, m) {
  const sc = MEETING_SCRIPTS[scriptId]; if (!sc) return false;
  m = m || MEETINGS.find(x => x.script === scriptId) || { id: scriptId, who: [], at: shipNow() };
  DIALOGUE = { id: scriptId, m, cast: meetingCast(m), ctx: evCtx(SHIP.event), queue: sc.lines.slice(), i: 0, at: 0 };
  if (!/^moment:/.test(scriptId)) eventMine('meetings', 1);   // a moment (20c) never counts toward a commendation
  dialogueDraw(); return true;
}
function dialogueView() {
  const D = DIALOGUE, sc = MEETING_SCRIPTS[D.id], l = D.queue[D.i]; if (!l) return null;
  if (l.choice) return l.prompt ? { title: l.label || sc.title, name: castName(D, l.who), who: castName(D, l.who), id: l.who, role: '', text: evText(l.prompt, D.ctx), choices: l.choice.map(c => c.text), i: D.i, n: sc.noCount ? 0 : D.queue.length }   // a question asked with its answers (the quiz, 0.34.51)
    : { title: sc.title, name: D.ctx.you, who: D.ctx.you, id: 'you', role: '', text: '', choices: l.choice.map(c => c.text), i: D.i, n: D.queue.length };
  const p = D.cast[l.who] || evPerson(l.who);
  return { title: sc.title, name: castName(D, l.who), who: castName(D, l.who), id: p ? p.id : l.who, role: p ? p.role || '' : '', text: evText(l.text, D.ctx), to: evText(l.to, D.ctx) || null, pose: l.pose || null, choices: null, i: D.i, n: sc.noCount ? 0 : D.queue.length };   // noCount: no "2/8" (the quiz says Question 2 of 3)
}
function dialogueDraw() {
  const v = DIALOGUE && dialogueView();
  if (!v) return dialogueEnd(true);
  DIALOGUE.at = performance.now();
  if (typeof deviceDialogue === 'function') return deviceDialogue(v);
  if (typeof document === 'undefined') return;
  if (!DIALOGUE_EL) {
    DIALOGUE_EL = document.createElement('div');
    DIALOGUE_EL.style.cssText = 'position:fixed;left:50%;bottom:14px;transform:translateX(-50%);width:min(560px,92vw);box-sizing:border-box;padding:10px 14px;border-radius:10px;background:rgba(14,20,24,.94);color:#e8f4ef;font:14px/1.4 system-ui,sans-serif;z-index:31;box-shadow:0 4px 18px rgba(0,0,0,.4)';
    DIALOGUE_EL.addEventListener('click', e => { if (DIALOGUE && !e.target.dataset.c && !dialogueView().choices) dialogueStep(); });
    document.body.appendChild(DIALOGUE_EL);
  }
  DIALOGUE_EL.innerHTML = '';
  const h = document.createElement('div'); h.style.cssText = 'font-weight:600;color:#9fe0cf;margin-bottom:2px';
  h.textContent = v.choices ? v.title + ': your reply' : v.name; DIALOGUE_EL.appendChild(h);
  if (!v.choices) DIALOGUE_EL.appendChild(document.createTextNode(v.text));
  else v.choices.forEach((c, k) => {
    const b = document.createElement('button'); b.textContent = c; b.dataset.c = '1';
    b.style.cssText = 'display:block;width:100%;margin-top:6px;padding:8px 10px;border-radius:8px;border:1px solid #3d5a52;background:#1d2b2a;color:#e8f4ef;font:inherit;text-align:left';
    b.addEventListener('click', () => dialogueStep(k)); DIALOGUE_EL.appendChild(b);
  });
  DIALOGUE_EL.hidden = false;
}
// on to the next line; on a choice line, k is the reply picked: its nudges, its job, and the reply said back
function dialogueStep(k) {
  const D = DIALOGUE; if (!D) return;
  const l = D.queue[D.i];
  if (l && l.choice) {
    const c = l.choice[k]; if (!c) return;
    { const sc = MEETING_SCRIPTS[D.id]; if (sc && typeof sc.onPick === 'function') try { sc.onPick(k, c); } catch (e) { /* the panel goes on */ } }   // a moment's reply (20c)
    if (!/^moment:/.test(D.id)) eventMine('choice:' + D.id, k + 1);   // social B's moments aren't the event's meetings
    for (const [who, pts] of Object.entries(c.rel || {})) { const p = D.cast[who] || schedPeople().find(q => q.id === who); if (p && typeof relAdd === 'function') relAdd(p.id, 'meeting:' + D.m.id, pts); }
    if (c.job) eventTakeJob(c.job);
    if (c.flag && typeof flagSet === 'function') flagSet(c.flag);   // a story beat (bridge.invited opens bridge hour)
    for (const [th, n] of Object.entries(c.thread || {})) eventScore(th, n);   // a small nudge to the event's thread
    if (c.reply) D.queue.splice(D.i + 1, 0, c.reply);
    if (typeof simNote === 'function') simNote('choice', { script: D.id, k, meeting: D.m && D.m.id || null, who: [...new Set(Object.values(D.cast || {}).filter(Boolean).map(p => p.id))],   // the bus (Pillar 4): social remembers your reply
      flavour: c.flavour || null, mem: c.mem || null, flag: c.flag || null });
  }
  D.i++; dialogueDraw();
}
const dialogueNext = () => dialogueStep(), dialogueChoose = k => dialogueStep(k);   // section 19's taps
// a job offered in a meeting: always remembered in SHIP.event.mine ('wants:<job>': the sign-up sheet reads it, and
// section 17 claims it for you when it posts it later), and claimed at once if section 17 has already posted it
// (tagged event and eventJob). The lead's 0.41.7 merge fix: the battery job is already up at the briefing (09:15 since 0.70.1)
function eventTakeJob(job) {
  const e = SHIP.event; if (!e) return false;
  e.mine['wants:' + job] = 1;
  const j = (SHIP.jobs || []).find(x => x.event === e.id && x.eventJob === job && x.status === 'open');
  if (j && typeof claimJob === 'function') return claimJob(j.id);
  return false;
}
function dialogueEnd(finished) {
  const D = DIALOGUE; if (!D) return;
  DIALOGUE = null;
  { const sc = MEETING_SCRIPTS[D.id]; if (sc && typeof sc.onEnd === 'function') try { sc.onEnd(finished); } catch (e) { /* closes anyway */ } }   // a moment ending (20c)
  if (typeof deviceDialogue === 'function') deviceDialogue(null); else if (DIALOGUE_EL) DIALOGUE_EL.hidden = true;
  if (!finished && D.m.event !== 'occasion') meetingGist(D.id);   // an occasion's gist is for missing it, not leaving early
}
const dialogueClose = () => dialogueEnd(false);          // walking away: the gist arrives in Mail
function meetingGist(scriptId) {
  const sc = MEETING_SCRIPTS[scriptId]; if (!sc || !sc.gist || typeof mailSend !== 'function') return;
  mailSend({ at: shipNow(), from: sc.from || 'Works', subject: sc.title + ' (notes)', body: evText(sc.gist, SHIP.event ? evCtx(SHIP.event) : { band: 'smooth', mine: {}, you: 'Cadet' }), quiet: true });
}
function inMeeting(m) {
  const w = m.where || {}; if (w.any) return true;      // anywhere (0.62.6, social: a recorded message on your device plays on through doorways and the lift)
  if (deckDef.num !== w.deck) return false;
  const r = roomAt(...player.here()), room = r && DECKS[w.deck].rooms && DECKS[w.deck].rooms[r];
  return !!room && (!w.room || w.room.test(room.name || ''));
}
// once a ship minute: the notice 15 minutes before (notify: true), the script when you're there, walking away, the gist after
function meetingFlags(m) {
  if (m.event === 'occasion') { const r = (SHIP.occasions || []).find(x => x.key === m.id); return r && r.status === 'asked' ? (r.f || (r.f = {})) : null; }
  return SHIP.event && SHIP.event.id === m.event ? SHIP.event.mine : null;
}
function meetingsTick(now, quiet) {                     // quiet: a sleep or skip (no notice, no panel; the gists still come)
  for (const m of MEETINGS) {
    const k = m.id, f = meetingFlags(m); if (!f) continue;
    if (quiet) { if (!f['met:' + k] && !f['gist:' + k] && now >= m.at + (m.len || 15)) { f['gist:' + k] = 1; meetingGist(m.script); } continue; }
    if (m.notify && !f['told:' + k] && now >= m.at - 15 && now < m.at) { f['told:' + k] = 1; toast(MEETING_SCRIPTS[m.script].title, m.notify); }
    if (!DIALOGUE && !f['met:' + k] && now >= m.at && now < m.at + (m.len || 15) && inMeeting(m)) { f['met:' + k] = 1; dialogueShow(m.script, m); }
    if (!f['met:' + k] && !f['gist:' + k] && now >= m.at + (m.len || 15)) { f['gist:' + k] = 1; meetingGist(m.script); }
    if (m.event === 'occasion' && f['met:' + k]) { const r = SHIP.occasions.find(x => x.key === k); if (r) r.met = true; }
  }
  if (DIALOGUE && !inMeeting(DIALOGUE.m)) dialogueClose();
}

// ---- felt everywhere (the first kind of moment): the front hits, every light dips, then flickers. The performance
// engineer owns the real effect, shipFeel(kinds, len) (sections 5, 8b), used when it exists; until then this plain
// stand-in: the camera shakes, the lights dip and come back, a rare flicker while the event's 'flicker' effect is on.
// Visual only (real time, never the simulation), on the current deck; nothing happens with no event.
const FEEL = { until: 0, t0: 0, kinds: [], flicker: false, log: [] };
function eventFeel(kinds, len = 4) {
  FEEL.log.push({ at: shipNow(), kinds: kinds.slice() }); if (FEEL.log.length > 20) FEEL.log.shift();
  if (typeof shipFeel === 'function') return shipFeel(kinds, len);
  FEEL.t0 = simNow(); FEEL.until = FEEL.t0 + len * 1000; FEEL.kinds = kinds.slice();
}
function eventFeelFrame() {                              // every frame, after the lights and camera are set, before the render
  if (typeof shipFeel === 'function') return;
  const now = simNow(); let k = 1;
  if (now < FEEL.until) {
    const s = (now - FEEL.t0) / 1000;
    if (FEEL.kinds.includes('jolt') && s < .7) { const a = .25 * (1 - s / .7); camera.position.x += a * Math.sin(s * 60); camera.position.y += a * .6 * Math.sin(s * 47 + 1); }
    if (FEEL.kinds.includes('lightsDip')) k = s < .3 ? 1 - s / .3 * .6 : s < 1.5 ? .4 : Math.min(1, .4 + (s - 1.5) * .4);
    if (FEEL.kinds.includes('flicker') && s > 1.5 && Math.floor(s * 9) % 5 === 0) k *= .6;
  } else if (FEEL.flicker && (Math.imul(Math.floor(now / 110), 2654435761) >>> 0) % 97 < 3) k = .7;
  if (k < 1) { hemi.intensity *= k; sun.intensity *= k; for (const L of LAMPS) L.l.intensity *= k; }
}
// the event's felt moments as their minute comes, in play only (a sleep or skip passes them quietly)
const FEEL_DONE = new Set();
function eventMomentsTick(from, to) {
  const e = SHIP.event, def = e && SHIP_EVENTS[e.id]; if (!def) { FEEL.flicker = false; return; }
  FEEL.flicker = !!eventMod('effect', 'flicker', to);
  for (const mo of def.moments || []) {
    if (!mo.feel) continue;
    const at = (e.startDay - 1 + mo.at[0]) * 1440 + mo.at[1], key = mo.id + '@' + e.startDay;
    if (at > from && at <= to && to - at < 3 && !FEEL_DONE.has(key)) { FEEL_DONE.add(key); eventFeel(mo.feel, mo.len); }
  }
}

// the ion storm's two meetings. who: a ROSTER id, or a cast slot the meeting fills from who's there ('tech1', 'tech2':
// its 'works:2'). text and to may be functions of the context: c.band, c.mine (the player's part), c.you (your name).
// A choice's reply is said back; rel nudges relationships (section 20's relAdd), job puts that event job on your list
MEETING_SCRIPTS.calderStorm = {
  title: 'Storm briefing', from: 'Chief Ines Calder',
  gist: 'Briefing notes: the ion storm is due tomorrow about 14:00, and Survey says it\'s a big one. In order: the lounge glassware and bar, shielded ballasts on the main lamps, battery packs up to the bridge. Storm jobs are on the board.',
  lines: [
    { who: 'calder', text: 'Gather round. Coffee can wait two minutes.', pose: 'gesture' },
    { who: 'calder', text: 'Survey\'s tracking an ion storm. Dr. Sato says it reaches us tomorrow afternoon, and it\'s a big one.' },
    { who: 'tech1', text: 'How big is big?', pose: 'nod' },
    { who: 'calder', text: 'Big enough that the lights flicker for two days and comms go dark. So we get ahead of it.' },
    { who: 'calder', text: 'Loose fittings secured. Shielded ballasts on the lamps that matter. Battery packs where they\'re needed.', pose: 'gesture' },
    { who: 'tech2', text: 'The lounge bar\'s the worst for loose glass. Last storm we were sweeping it up for a week.' },
    { who: 'calder', text: 'Then the lounge goes first. And somebody takes battery packs up to the bridge before the front hits.' },
    { who: 'calder', text: c => c.you + ', you\'re new to this. Anything you want to take on?', to: 'you' },
    { choice: [
      { text: 'I\'ll take the battery run to the bridge.', rel: { calder: 2 }, job: 'stormBatteries', reply: { who: 'calder', text: 'Good. The packs are in main storage. Mind the lift.', pose: 'nod' } },
      { text: 'I can do the lounge.', rel: { calder: 1, tech2: 1 }, job: 'stormLounge', reply: { who: 'tech2', text: 'I\'ll show you where the bar keeps the good glasses.', pose: 'nod' } },
      { text: '(Say nothing)', reply: { who: 'calder', text: 'Fine. The board\'s there when you want it.' } },
    ] },
    { who: 'calder', text: 'Right. Storm jobs are on the board. Off you go.', pose: 'gesture' },
  ],
};
MEETING_SCRIPTS.captainAllClear = {
  title: 'The all-clear', from: 'Commander Teo Vance',
  gist: c => 'Notes from the observation room: the storm passed at 09:40. ' + SHIP_EVENTS.ionStorm.debrief[c.band] + ' Comms are back; expect a queue at the booths. Party in the bow lounge at 19:00.',
  lines: [
    { who: 'marrow', text: 'Dr. Sato?' },
    { who: 'sato', text: 'The front passed us at 09:40. Readings are back to background. It\'s over.' },
    { who: 'marrow', text: c => ({ smooth: 'Then let\'s say so. That went about as well as a storm can.', bumpy: 'Then let\'s say so. Not our smoothest two days, but nobody got hurt.',
      rough: 'Then let\'s say so. That was a hard one, and the ship shows it.' })[c.band], pose: 'nod' },
    { who: 'calder', text: c => ({ smooth: 'The lights only went a few times. The prep paid off.', bumpy: 'We lost a relay on the bridge. I\'ll have it patched by the end of the week.',
      rough: 'The relay room\'s a mess. We\'ll be patching for a week.' })[c.band] },
    { who: 'holt', text: 'Watch reports no injuries. Some short tempers. Mine included.' },
    { who: 'marrow', text: c => c.mine.jobs ? 'And I\'m told our newest Works hand did their share. Thank you, ' + c.you + '.' : 'Comms are back. Expect a queue at the booths.', to: c => c.mine.jobs ? 'you' : null },
    { choice: [
      { text: 'It was good to be useful.', rel: { marrow: 1, calder: 1 }, reply: { who: 'marrow', text: 'It always is. Remember that on the dull days.', pose: 'nod' } },
      { text: 'Is there a party?', rel: { vance: 1 }, reply: { who: 'vance', text: 'Bow lounge, 19:00. The Captain insists.', pose: 'gesture' } },
      { text: '(Just nod)' },
    ] },
    { who: 'marrow', text: 'Right. I\'ll tell the ship.', pose: 'gesture' },
  ],
};

// ---- occasions (C10; plans/pillar3-plan.md Part 4, "Progression hooks"): moments of trust, each opened by something
// you earned and each an appointment (a time window that opens a door). Section 18 decides when they're due and plays
// them as meetings; section 20 knows who's friends (relTier), section 19 shows the appointment (apptAdd), section 14
// opens the door for its window (doorOpenFor reads occasionDoorOpen), the galley cooks for the Captain's table.
//   OCCASIONS.<id> = { title, kind: 'summons' | 'invite' | 'meeting', by, deck, room (key), at, len, script,
//                      due(d) -> bool (pure from saved state), ask? (you ask for it), galley?, trace?, mail }
//   SHIP.occasions: [{ id, key, at, len, deck, room, status: 'asked' | 'kept' | 'missed' }]   (saved; the device's Record
//   reads the kept ones). SHIP.commendations: [{ event, day }]   (saved; an event ends with your part counted)
// Commended: two or more of the event's jobs, or one and a meeting (`eventMine`). Nothing here calls R().
SHIP.occasions = []; SHIP.commendations = [];
(() => {
  const s = SAVED && SAVED.ship;
  if (s && Array.isArray(s.occasions)) SHIP.occasions = s.occasions.filter(o => o && OCC_OK(o)).slice(-40);
  if (s && Array.isArray(s.commendations)) SHIP.commendations = s.commendations.filter(c => c && typeof c.event === 'string' && Number.isInteger(c.day));
})();
function OCC_OK(o) { return typeof o.id === 'string' && typeof o.key === 'string' && Number.isFinite(o.at); }
SAVE_EXTRA.push(s => { s.ship.occasions = SHIP.occasions.slice(-40); s.ship.commendations = SHIP.commendations; });
// a New game (section 13's simNote('newGame')): everything section 18 keeps for a game starts again: occasions and
// commendations, the ship-wide event and its log, traces, the traditions' sent/joined/noted, one-offs and your votes,
// meetings, and the caches (reviewer 1b, via device engineer 3: a new game kept the last one's Captain's table)
if (typeof onSim === 'function') onSim('newGame', () => {
  if (DIALOGUE) dialogueEnd(true);
  SHIP.occasions.length = 0; SHIP.commendations.length = 0;
  SHIP.event = null; SHIP.eventLog.length = 0; SHIP.traces.length = 0;
  const oo = SHIP.events.oneOffs.length; for (const k of ['sent', 'joined', 'noted', 'oneOffs']) SHIP.events[k].length = 0; SHIP.events.votes = {};
  MEETINGS.length = 0; FEEL_DONE.clear(); EV_MAILBOX.length = 0; WEEK_MAILS.length = 0; for (const k in EV_BUNDLE) delete EV_BUNDLE[k];
  EV_LAST = null; EV_MIN = -1; EV_ARR = null; EV_DAYS.clear(); EV_DROPPED.clear(); TALLY_MEMO.clear();
  if (oo && typeof SHIP_DAYS !== 'undefined') { SCHED_DATA = null; SHIP_DAYS.clear(); }   // as eventOneOff: the one-offs leave the plans
});
const occRel = id => typeof relTier === 'function' ? relTier(id) || 0 : 0;
const occOnShift = (id, d) => { const p = schedPeople().find(q => q.id === id); return !!p && isWorkDay(p, d); };
const yourJobsDone = () => (SHIP.jobs || []).filter(j => j.status === 'done' && j.doneBy === 'you').length;
const OCCASIONS = {
  // summoned after your first commendation (the next day the Captain is on shift), or by Vance once you're friends
  readyRoom: { title: 'The Captain\'s ready room', kind: 'summons', by: 'marrow', deck: 1, room: 'R', at: 660, len: 25, script: 'readyRoomFirst', once: true,
    due: d => { const c = SHIP.commendations[0], from = c ? c.day + 1 : null;
      if (from === null && occRel('vance') < 3) return false;
      if (from !== null && d < from) return false;
      for (let k = from || d; k < d; k++) if (occOnShift('marrow', k)) return false;   // only the first such day
      return occOnShift('marrow', d); },
    mail: { from: 'Commander Teo Vance', subject: 'The Captain would like a word', body: 'The Captain would like to see you in her ready room on Deck 1 at 11:00 today. The door will be open. No need to change.' } },
  // the Captain's table: a dinner in her quarters every 28 days (days 20, 48...), one junior who stood out invited
  captainsTable: { title: 'The Captain\'s table', kind: 'invite', by: 'marrow', deck: 2, room: 'C', at: 1170, len: 90, script: 'captainsTable', notice: 1,
    due: d => d % 28 === 20 && (SHIP.commendations.some(c => c.day > d - 28 && c.day <= d)
      || (typeof SHIP.rel === 'object' && SHIP.rel ? Object.keys(SHIP.rel).filter(id => occRel(id) >= 3).length >= 3 : false)),
    galley: { batch: { meals: 8, label: 'the Captain\'s table' } }, trace: 'framedMenu',
    mail: { from: 'Captain Odile Marrow', subject: 'Dinner at my table', body: 'You\'re invited to dinner in my quarters on Deck 2 tomorrow at 19:30. Chef Brennan is cooking. Come as you are, but do come.' } },
  // a progress talk in the Chief's office: you ask for one (the device's Appointments app calls occasionAsk)
  progressTalk: { title: 'A progress talk', kind: 'meeting', by: 'calder', deck: 5, room: 'o', len: 20, script: 'calderProgress', ask: true,
    mail: { from: 'Chief Ines Calder', subject: 'Your progress talk', body: 'My office, at the time you asked for. Bring nothing; I have your record.' } },
  // the bridge invite (Pillar 4; the head writer's content/meetings/bridgeInvite.meet): Vance at breakfast in the mess the
  // day before your first bridge hour (day 22 in a new game). A chance meeting: no appointment, no notice, no Mail first.
  // Any reply, or missing him (the gist comes by Mail), sets flag bridge.invited, which opens bridge hour's gate
  // (and the bridge itself, SHIP.bridgeInvited). Step 3: only once the first ship-wide event has ended (bridgeInviteReady; was d >= 15)
  bridgeInvite: { title: 'An invitation', kind: 'meeting', by: 'vance', deck: 3, room: 'M', at: 390, len: 30, script: 'bridgeInvite', once: true, chance: true, flag: 'bridge.invited',
    due: d => bridgeInviteReady(d) && !flag('bridge.invited') && occBridgeEve(d), slot: d => occMealSlot('vance', d, '3-mess-', 300, 600) },
};
// the day before a bridge hour (its rhythm only, not its flag); and a person's first stay at places `pre` between two
// minutes of the day (Vance's breakfast in the mess: the sim's plan for that day), as { at, len }, or null
function occBridgeEve(d) { const b = SHIP_TRADITIONS.find(e => e.id === 'bridge-hour'); return !!b && evDue(b.when, d + 1); }
function occMealSlot(id, d, pre, lo, hi) {
  const p = schedPeople().find(q => q.id === id), B = (d - 1) * 1440;
  const s = p && planDay(p, d).find(x => x.placeId && x.placeId.startsWith(pre) && x.from - B >= lo && x.from - B < hi);
  return s ? { at: s.from - B, len: Math.max(10, s.to - s.from) } : null;
}
// a new occasion on the books: the appointment, the Mail, and the meeting that plays when you're in the room
function occasionAdd(id, at, quiet, len) {
  const o = OCCASIONS[id], key = id + '@' + (Math.floor(at / 1440) + 1);
  if (!o || SHIP.occasions.some(x => x.key === key)) return null;
  const r = { id, key, at, len: len || o.len, deck: o.deck, room: o.room, by: o.by, kind: o.kind, status: 'asked' };
  SHIP.occasions.push(r);
  if (!o.chance && typeof apptAdd === 'function') apptAdd({ id: key, with: [o.by, ...(o.with || [])], at, len: o.len, where: o.deck + '|' + o.room, kind: o.kind, status: 'yes', by: o.by, title: o.title });
  if (o.mail && typeof mailSend === 'function') mailSend({ at: Math.min(shipNow(), at), from: o.mail.from, subject: o.mail.subject, body: o.mail.body, quiet: !!quiet });
  return r;
}
// you ask for one (ask: true): at ship minute `at`, if its person is on shift that day; returns the record or null
function occasionAsk(id, at) { const o = OCCASIONS[id]; return o && o.ask && occOnShift(o.by, Math.floor(at / 1440) + 1) ? occasionAdd(id, at) : null; }
// the doors (section 14's doorOpenFor): the room is open to you from 10 minutes before an occasion to its end
function occasionDoorOpen(deck, room, t = shipNow()) { return SHIP.occasions.some(r => r.status === 'asked' && r.deck === deck && r.room === room && t >= r.at - 10 && t < r.at + r.len); }
// the galley's keys during an occasion's day (eventMod falls back to this when no event is on)
function occasionMod(kind, key, t) {
  const d = Math.floor(t / 1440);
  for (const r of SHIP.occasions) { const o = OCCASIONS[r.id]; if (o && o[kind] && Math.floor(r.at / 1440) === d && r.status !== 'missed' && o[kind][key] != null) return o[kind][key]; }
  return null;
}
// once a ship minute (and on skips): book what's due today and tomorrow, keep the meetings registered, close the past
function occasionsTick(now, quiet) {
  const d = Math.floor(now / 1440) + 1;
  for (const [id, o] of Object.entries(OCCASIONS)) {
    if (o.ask || (o.once && SHIP.occasions.some(r => r.id === id))) continue;
    for (const k of [d, d + (o.notice || 0)]) if (o.due(k)) {
      const sl = o.slot && o.slot(k) || { at: o.at, len: o.len }, at = (k - 1) * 1440 + sl.at;
      if (at > now || (o.chance && k === d)) occasionAdd(id, at, quiet, sl.len);   // a chance meeting slept through still counts as missed
    }
  }
  for (const r of SHIP.occasions) {
    const o = OCCASIONS[r.id]; if (!o) continue;
    if (r.status === 'asked' && now < r.at + r.len) meeting({ notify: o.chance || typeof deviceApp === 'function' || typeof apptAdd === 'function' ? null : o.title + ': ' + DECKS[r.deck].rooms[r.room].name + ', ' + deckIn(r.deck) + ', at ' + hhmm(r.at % 1440) + '.', id: r.key, event: 'occasion', where: { deck: r.deck, room: new RegExp('^' + DECKS[r.deck].rooms[r.room].name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '$') }, at: r.at, len: r.len, who: [r.by], script: o.script });
    if (r.status === 'asked' && now >= r.at + r.len) {
      r.status = r.met ? 'kept' : 'missed'; if (r.met && o.trace && !SHIP.traces.includes(o.trace)) SHIP.traces.push(o.trace);
      const f = r.f || (r.f = {}); if (!r.met && o.chance && !f['gist:' + r.key]) { f['gist:' + r.key] = 1; meetingGist(o.script); }   // missed before its meeting was ever registered
      if (o.flag && typeof flagSet === 'function') flagSet(o.flag);
    }
  }
}
SIM_ADVANCE.push((from, to) => { meetingsTick(to, true); occasionsTick(to, true); });   // after a skip: book what's due, and the gists of what you missed
MEETING_SCRIPTS.readyRoomFirst = {
  title: 'The ready room', from: 'Commander Teo Vance',
  gist: 'The Captain sent for you and you weren\'t there. She says it will keep, and she has a long memory.',
  lines: [
    { who: 'marrow', text: 'Come in. Mind the step; everyone trips on it.', pose: 'gesture' },
    { who: 'marrow', text: c => c.commended ? 'I read the debrief. Calder says you were where you were needed.' : 'Commander Vance tells me you\'re worth knowing. He doesn\'t say that often.', to: 'you' },
    { who: 'marrow', text: 'Tell me something. From where you stand, what does this ship need that the senior crew can\'t see?', to: 'you' },
    { choice: [
      { text: 'Better lights on the lower decks.', rel: { marrow: 1 }, mem: 'readyroom.lights', reply: { who: 'marrow', text: 'Noted. Calder will love that.', pose: 'nod' } },
      { text: 'More people who know where the spare filters are.', rel: { marrow: 1, calder: 1 }, mem: 'readyroom.filters', reply: { who: 'marrow', text: 'Ha. That\'s a Works answer.', pose: 'nod' } },
      { text: 'I\'m still learning. Ask me in a month.', rel: { marrow: 2 }, mem: 'readyroom.month', reply: { who: 'marrow', text: 'Honest. I will.' } },
    ] },
    { who: 'marrow', text: 'Before you go: meet the Admiral.', pose: 'gesture' },
    { who: 'marrow', text: 'He\'s been aboard longer than anyone. He doesn\'t say much, which is why he outranks us all.' },
    { who: 'marrow', text: c => 'Thank you, ' + c.you + '. Back to it.', to: 'you' },
  ],
};
MEETING_SCRIPTS.captainsTable = {
  title: 'The Captain\'s table', from: 'Captain Odile Marrow',
  gist: 'Your seat at the Captain\'s table stayed empty. Chef Brennan saved you a slice of the tart.',
  lines: [
    { who: 'marrow', text: 'Sit, sit. Brennan has outdone herself.', pose: 'gesture' },
    { who: 'vance', text: 'To the Wren.' },
    { who: 'sato', text: 'And to whoever fixed the observatory heater.' },
    { who: 'calder', text: 'That would be Works. As usual.', pose: 'nod' },
    { who: 'marrow', text: 'So. What do the juniors say about us when we\'re not listening?', to: 'you' },
    { choice: [
      { text: 'That the Commander never sleeps.', rel: { vance: 1 }, reply: { who: 'vance', text: 'Accurate.' } },
      { text: 'That the stew\'s improved.', rel: { marrow: 1 }, reply: { who: 'marrow', text: 'I\'ll tell Brennan. She\'ll pretend not to care.', pose: 'nod' } },
      { text: 'Only good things, Captain.', rel: { holt: 1 }, reply: { who: 'holt', text: 'A diplomat. We\'ll make an officer of you yet.' } },
    ] },
    { who: 'marrow', text: 'Same time next month, then. Perhaps.' },
  ],
};
MEETING_SCRIPTS.calderProgress = {
  title: 'A progress talk', from: 'Chief Ines Calder',
  gist: 'You missed your progress talk. Calder says ask again when you\'re ready.',
  lines: [
    { who: 'calder', text: 'Sit. Let\'s look at your record.', pose: 'gesture' },
    { who: 'calder', text: c => c.jobsDone + (c.jobsDone === 1 ? ' job' : ' jobs') + ' signed off since you came aboard.' },
    { who: 'calder', text: c => c.jobsDone >= 25 ? 'That\'s close to what Tier 2 asks. A seal check or two and I\'ll put your name forward.' : 'Tier 2 wants about twenty-five, and a seal check or two. Keep at it.', to: 'you' },
    { choice: [
      { text: 'What should I work on?', rel: { calder: 1 }, reply: { who: 'calder', text: 'Seals. Everyone avoids them.' } },
      { text: 'Thanks, Chief.', reply: { who: 'calder', text: 'Don\'t thank me. Thank the filters.', pose: 'nod' } },
    ] },
  ],
};

// the diplomatic visit's two meetings (its data is with the storm's, above)
MEETING_SCRIPTS.veyliGreeting = {
  title: 'The Veyli greeting', from: 'Commander Teo Vance',
  gist: 'The Veyli delegation came aboard at 10:00: Speaker Teshavi, her aide Kesrin, the scholar Moleth and their pilot Ithra. They\'re in the visitors\' cabin and the guest cabins on Deck 4 for five days.',
  lines: [
    { who: 'marrow', text: 'Speaker Teshavi. Welcome aboard the Wren.', pose: 'gesture' },
    { who: 'teshavi', text: 'Captain. Your ship is warmer than the reports said. That is a compliment.', pose: 'nod' },
    { who: 'saruth', text: 'Speaker. It has been too long.' },
    { who: 'teshavi', text: 'Saruth. You look well fed. The humans are treating you kindly, then.' },
    { who: 'kesrin', text: 'The Speaker would like to meet the crew who keep the ship running. Informally.', to: 'you' },
    { who: 'teshavi', text: 'You. The young one in Works grey. What do you do aboard?', to: 'you' },
    { choice: [
      { text: 'I keep the lights on, Speaker. Mostly.', rel: { marrow: 1 }, reply: { who: 'teshavi', text: 'Mostly. An honest answer. I like it.', pose: 'nod' } },
      { text: 'Welcome aboard. Ask me anything about the ship.', rel: { vance: 1 }, thread: { discourtesy: -1 }, reply: { who: 'kesrin', text: 'Careful. Moleth has forty questions.' } },
      { text: '(A respectful nod)', reply: { who: 'teshavi', text: 'Quiet. Good. Most of your crew talk too much.' } },
    ] },
    { who: 'marrow', text: 'Commander Vance will show you to your cabins. Dinner is tomorrow, in my quarters.' },
  ],
};
MEETING_SCRIPTS.veyliGiftExchange = {
  title: 'The gift exchange', from: 'Commander Teo Vance',
  gist: c => 'The gift exchange in the observation room this morning. ' + (c.band === 'smooth' ? 'The Speaker gave the Wren a cord sculpture; it hangs in the bow lounge.' : 'The Speaker thanked the Captain with a few formal words.') + ' The delegation left from the shuttle bay at 10:00.',
  lines: [
    { who: 'teshavi', text: 'Captain. It is our custom to leave something of ourselves behind.', pose: 'gesture' },
    { who: 'teshavi', text: c => c.band === 'smooth' ? 'Seven knots, tied by seven hands. Hang it where your crew gather.' : 'Please accept our thanks. They are sincere.' },
    { who: 'marrow', text: 'Thank you, Speaker. And from us: charts of every system we\'ve crossed. Dr. Sato insisted.', pose: 'nod' },
    { who: 'moleth', text: 'I have thirty-one questions left. I will write.', to: 'you' },
    { choice: [
      { text: 'Write to me. I\'ll ask Calder for the answers.', rel: { calder: 1 }, thread: { discourtesy: -1 }, reply: { who: 'moleth', text: 'I will hold you to that.', pose: 'nod' } },
      { text: 'Safe travels.', reply: { who: 'moleth', text: 'And to you. Keep the lights on. Mostly.' } },
    ] },
    { who: 'saruth', text: 'Speaker. Travel well.' },
  ],
};

// ---- the Calendar's list (section 19): the ship traditions between two ship minutes, in time order:
// [{ id, title, at, where (words), deck, room (key, or null when its places span several rooms) }]
function upcomingTraditions(fromMin, toMin) {
  const out = [], S = schedData();
  for (let d = Math.floor(fromMin / 1440) + 1; d <= Math.floor(toMin / 1440) + 1; d++) for (const e of eventsOn(d)) {
    const at = (d - 1) * 1440 + e.from; if (at < fromMin || at > toMin) continue;
    const w = e.ev.where[0], pool = S.shared.get(w.deck + '|' + (w.room ? 'ev:' + e.id + ':0' : w.pool)) || [], pl = pool[0];
    const room = pl && DECKS[pl.deck].rooms && DECKS[pl.deck].rooms[pl.room], one = !!pl && pool.every(q => q.room === pl.room);
    out.push({ id: e.id, title: e.name + (e.names ? ' (' + e.names + ')' : ''), at, to: (d - 1) * 1440 + e.to, where: (room ? room.name + ', ' : '') + deckWord(w.deck),
      deck: pl ? pl.deck : w.deck, room: one ? pl.room : null });   // for the device's Go there (deck, room key; null: a pool over several rooms)
  }
  return out.sort((a, b) => a.at - b.at);
}

var EV_READY = true;                                     // section 14's hooks wait for this (it's read before section 18 runs)
if (SCHED_DATA) { SCHED_DATA = null; SHIP_DAYS.clear(); EV_DAYS.clear(); }   // anything planned before now is planned again, with the events

