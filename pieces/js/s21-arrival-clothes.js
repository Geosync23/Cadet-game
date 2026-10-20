// =====================================================================
// 21. ARRIVAL
// The arrival and the first week (plans/pillar4-plan.md, Part 1; the social side is plans/social-deep-plan.md,
// Part 7). A new game opens on Day 0, Sunday 17:30 (the user, after 0.60.3; was 17:40), on the Tern's ramp in the Deck 5 shuttle bay: Zeke Torres (Works,
// one rank above you) walks you to your bunk and to dinner, Chief Calder stops by the table, and the week after is
// taught by people (the shadow shift on Monday, your first solo job on Tuesday, Sowing morning on Saturday).
// On paper so far (0.42.0): the steps, the week's beats, the Settling-in list, the flags and the save. Nothing calls
// in here yet, nothing here draws anything or calls R(), and test URLs (?nosave) never start the intro.
//   SHIP.intro = { on, step, since, near: [tiles, minute], day, done: { stepId: shipMin }, missed: [stepId], settle: { itemId: shipMin }, skipped, ended, escort, flags }
//   (the name you type on the manifest is section 15's SHIP.player.name, set with playerNameSet)
//   INTRO_STEPS  the arrival evening, A0-A13: { id, day, at, until, who, where, mode, meeting, checkpoint, fallback, rel }
//   INTRO_WEEK   Days 1-7: one beat per person who teaches you something, in their real day (section 14 plans them)
//   SETTLE       the Settling-in list (the device's app reads it); each item ticks itself from the ship notes
//   introOn() introStep() introDone(id) introEnd() introSkip() introArrival() introWanted() introNewGame(arriving) introSig()   escortPlan(p, t)   introBeats(id, d)   settleNote(kind, data)
//   introAdvance(t, here)   moves the steps on at minute t; here = { deck, tile } of the player, or null (walked off)
// SHIP.intro.since: the minute the current step became yours (its fallback's wait counts from then).
// Times: day 0 is the arrival Sunday, so a step's minute is (day - 1) * 1440 + at, below 0 on Day 0.
// Hash keys 700-749 (the plan's map): 700 your table at dinner. Hooks into other sections are one-line and typeof-guarded
// (DEV_NOTES "Hook register"). Until section 13 has the ship notes bus and the flag store (simNote, onSim, flag,
// flagSet), the stand-ins below keep the flags in SHIP.intro.flags and hand this section's own notes to settleNote.
// =====================================================================
const INTRO_ESCORT = 'torres-zeke';                      // the user: a future friend, one notch above you in Works
const INTRO_KEY = 'starship-cadet-arrived';              // set once you've finished or ended an intro: New game offers the skip (outside the save)
const INTRO_START = { day: 0, min: 17 * 60 + 30, deck: 5, tile: [5, 7], face: 0 };   // inside the Tern, in its aisle facing the door (south; the deck architect's DECKS[5].tern.start, 0.38.18)
const introAbs = (day, min) => (day - 1) * 1440 + min;
const INTRO_REACH = 2;                                   // a step is done when you're in its checkpoint's room, this many tiles from it at most
const introRoomAt = (deck, tile) => { const D = DECKS[deck], ch = D && D.map[tile[1]] && D.map[tile[1]][tile[0]], r = D && D.rooms[ch]; return r ? r.name : null; };
const introNote = (kind, data) => {                      // the ship notes bus (section 13) when it's there; this list hears its own either way
  if (typeof simNote === 'function') simNote(kind, data);
  if (!INTRO_HEARD) settleNote(kind, data);
};
const introFlag = k => typeof flag === 'function' ? !!flag(k) : !!(SHIP.intro.flags && SHIP.intro.flags[k]);
const introFlagSet = (k, v = true) => { if (typeof flagSet === 'function') flagSet(k, v); else { const f = SHIP.intro.flags || (SHIP.intro.flags = {}); if (v === null) delete f[k]; else f[k] = v; } };
// every flag this section sets: a new arrival clears them all (section 13's store outlives SHIP.intro), and the end of
// the intro, however it comes, leaves all but 'mug' and 'seedling' set (the device, Calder met, every week's gate open)
// the week's three jobs (section 17's jobReserve(kind, day, at, slot), agreed with the systems engineer): Monday's shadow
// shift and the one you lead in the afternoon, and Tuesday's first solo job from Calder. Reserved at Monday 05:00
// (INTRO_WEEK 'd1-jobs'); not on skip.
const INTRO_JOBS = [['lights', 1, 9 * 60, 1], ['washer', 1, 13 * 60, 2], ['lights', 2, 8 * 60 + 45, 3]];   // the 09:00 shift (0.44.14): an hour on from 08:00 and 07:45
const INTRO_FLAGS = ['escort.' + INTRO_ESCORT, 'week1', 'intro.device', 'met.calder', 'week1.d2', 'week1.d3', 'week1.d4', 'week1.d5', 'week1.d6', 'week1.d7', 'week1.done', 'mug', 'seedling'];
const introRel = (id, step, pts) => { if (pts && typeof relAdd === 'function') relAdd(id, 'intro:' + step, pts); };
const introMail = (m, at) => { if (m && typeof mailSend === 'function') mailSend({ at, from: m.from, subject: m.subject, body: m.body }); };

// ---- Day 0, the arrival evening (the plan's table A0-A13) ----
// mode: 'lead' (the escort walks ahead to the checkpoint, waits when you're more than 4 tiles behind), 'wait' (stands
// at the checkpoint), 'meet' (a meeting with dialogue there), 'free' (the escort goes back to his own Sunday).
// checkpoint: where a reload resumes and where the escort waits ({ deck, tile, room }: the room the tile must be in).
// fallback: wait so many ship minutes for you at the checkpoint (or until a minute of the day), then send the Mail (if
// any), set its own flags (not the step's: a missed bunk is no device yet) and move on to `later`.
// rel: points to people when the step is done (the social plan's end state: Torres 10, Tomas 10, Pell 5, Calder 3, Brennan 3).
// Checkpoint tiles are provisional until wave 2 walks them (intro_check: in the room, on the deck's map).
const INTRO_STEPS = [
  { id: 'manifest', day: 0, at: 17 * 60 + 30, who: null, mode: 'free', where: 'the shuttle manifest',
    teaches: 'your name' },
  { id: 'ramp', day: 0, at: 17 * 60 + 30, who: INTRO_ESCORT, mode: 'wait', where: 'the Tern\'s ramp',
    checkpoint: { deck: 5, tile: [5, 11], room: 'Shuttle bay' }, tip: 'walk', fallback: { wait: 20, later: 'hello' } },
  { id: 'hello', day: 0, at: 17 * 60 + 32, who: INTRO_ESCORT, mode: 'wait', where: 'the ramp foot',
    checkpoint: { deck: 5, tile: [5, 11], room: 'Shuttle bay' }, rel: { [INTRO_ESCORT]: 4 }, fallback: { wait: 20, later: 'haulway' } },
  { id: 'haulway', day: 0, at: 17 * 60 + 34, who: INTRO_ESCORT, mode: 'lead', where: 'the haulway',
    checkpoint: { deck: 5, tile: [12, 8], room: 'Haulway' }, fallback: { wait: 20, later: 'works' } },
  { id: 'works', day: 0, at: 17 * 60 + 36, who: INTRO_ESCORT, mode: 'lead', where: 'the Works bay door',
    checkpoint: { deck: 5, tile: [16, 6], room: 'Lift lobby' }, fallback: { wait: 20, later: 'lift' } },
  { id: 'lift', day: 0, at: 17 * 60 + 38, who: INTRO_ESCORT, mode: 'lead', where: 'the lift, Deck 5',
    checkpoint: { deck: 5, tile: [15, 9], room: 'Lift lobby' }, fallback: { wait: 20, later: 'wing' } },
  { id: 'wing', day: 0, at: 17 * 60 + 40, who: INTRO_ESCORT, mode: 'lead', where: 'the junior wing, Deck 4',
    checkpoint: { deck: 4, tile: [12, 4], room: 'Junior corridor' }, fallback: { wait: 20, later: 'bunk' } },
  { id: 'bunk', day: 0, at: 17 * 60 + 43, who: INTRO_ESCORT, mode: 'meet', where: 'Bunk 1', meeting: 'introBunk',
    checkpoint: { deck: 4, tile: [8, 3], room: 'Bunk 1' }, rel: { [INTRO_ESCORT]: 3, tomas: 10 }, flags: ['intro.device'],
    fallback: { wait: 30, later: 'toMess', mail: { from: 'Zeke Torres', subject: 'Your bunk', body: 'Couldn\'t find you. Your bunk\'s in Bunk 1, Deck 4: drop your bag in your locker when you can. Your device I\'ll hand you myself. Dinner\'s on Three. — Z.' } } },
  { id: 'toMess', day: 0, at: 17 * 60 + 55, who: INTRO_ESCORT, mode: 'lead', where: 'to the mess, Deck 3',
    checkpoint: { deck: 3, tile: [22, 7], room: 'Lift plaza' }, fallback: { wait: 20, later: 'servery' } },
  { id: 'servery', day: 0, at: 18 * 60 + 2, who: INTRO_ESCORT, mode: 'lead', where: 'the mess servery',
    checkpoint: { deck: 3, tile: [33, 3], room: 'Mess hall' }, rel: { pell: 5, brennan: 3 }, fallback: { wait: 25, later: 'table' } },
  { id: 'table', day: 0, at: 18 * 60 + 4, who: INTRO_ESCORT, mode: 'meet', where: 'your table in the mess', meeting: 'introDinner',   // 0.42.20: Torres about himself, before the Chief
    checkpoint: { deck: 3, tile: [28, 1], room: 'Mess hall' }, fallback: { wait: 15, later: 'chief' } },
  { id: 'chief', day: 0, at: 18 * 60 + 20, who: 'calder', mode: 'meet', where: 'your table in the mess', meeting: 'introChief',
    checkpoint: { deck: 3, tile: [28, 1], room: 'Mess hall' }, rel: { calder: 3 }, flags: ['met.calder'],
    seats: { you: '3-mess-10', [INTRO_ESCORT]: '3-mess-12', calder: '3-mess-9' },   // you, Torres beside you, the Chief across
    // (0.71.3, the user's playtest 2: "the Chief isn't at the dinner with Zeke") she sits across from you from the start of the dinner, not at the far table (0.42.64's away)
    fallback: { until: 19 * 60 + 30, later: 'free', mail: { from: 'I. Calder', subject: 'Tomorrow', body: 'Missed you at dinner. Torres has you tomorrow; ten to nine, the Works bay.' } } },
  { id: 'free', day: 0, at: 19 * 60 + 30, who: INTRO_ESCORT, mode: 'free', where: 'the mess', rel: { [INTRO_ESCORT]: 3 } },   // he lets you go after his goodnight (introNightTick), 19:30 at the latest (reviewer 1c: no fixed 19:00)
  { id: 'tomas', day: 0, at: 19 * 60 + 30, who: 'tomas', mode: 'free', where: 'the junior common room or Bunk 1', teaches: 'Chat and Ask about', seek: 22 * 60 },
  { id: 'night', day: 0, at: 20 * 60, who: null, mode: 'free', where: 'your bunk', teaches: 'sleep' },
];
// the meetings the writers fill (content/meetings, merged into MEETING_SCRIPTS): their gist is what Mail says if you miss them
const INTRO_MEETINGS = {
  introBunk: { title: 'Your bunk', cast: [INTRO_ESCORT, 'tomas'], gist: 'Torres showed you Bunk 1 and your locker, and handed you your device.' },
  introDinner: { title: 'Dinner with Torres', cast: [INTRO_ESCORT], choice: true, gist: 'Dinner with Zeke Torres: engines, coil three, and how the ship runs.' },
  introChief: { title: 'The Chief stops by', cast: ['calder', INTRO_ESCORT], choice: true, gist: 'Chief Calder: Torres has you on Monday; your first job on Tuesday is hers.' },
  introBriefing: { title: 'Monday briefing', cast: ['calder', INTRO_ESCORT, 'works:2'], gist: 'The Monday briefing: you shadow Torres today.' },
  introSoloJob: { title: 'Your first solo job', cast: ['calder'], gist: 'Your first solo job is on your device. Book a progress talk any time.' },
};

// ---- Days 1-7: who teaches you what, in their real day (the plan's table). introBeats(id, d) hands section 14 the
// beats of one person on one day (introPlan), so they are in the schedules, seeded and testable; nobody is teleported.
// action: what this section does at `at` (flags, the invitation); settle: the Settling-in item it teaches.
const INTRO_WEEK = [
  { id: 'd1-jobs', day: 1, at: 5 * 60, who: null, reserve: true },   // section 17: the week's three jobs, held for you (not at
  // the arrival itself: a new game's clock jumps back to Day 0 and the machines start afresh after it)
  { id: 'd1-wash', day: 1, at: 6 * 60, until: 6 * 60 + 30, who: 'tomas', where: { deck: 4, room: 'Bunk 1' }, settle: 'washed' },
  { id: 'd1-briefing', day: 1, at: 8 * 60 + 50, until: 9 * 60 + 5, who: 'calder', also: [INTRO_ESCORT], where: { deck: 5, room: 'Works bay' }, meeting: 'introBriefing', settle: 'team',
    flags: ['intro.device', 'met.calder'] },   // if you missed them on Sunday, Torres hands you the device here
  { id: 'd1-shadow', day: 1, at: 9 * 60 + 5, until: 13 * 60, who: INTRO_ESCORT, where: { deck: 5, room: 'Works bay' }, escort: 'follow', job: 'reserved:1', settle: 'shadow' },   // he stays at your side and talks you through it (introJobLines); the arrow shows the way
  { id: 'd1-lead', day: 1, at: 13 * 60, until: 16 * 60 + 30, who: INTRO_ESCORT, where: { deck: 5, room: 'Works bay' }, escort: 'follow', job: 'reserved:2', settle: 'lead' },
  { id: 'd1-dinner', day: 1, at: 18 * 60, until: 19 * 60, who: 'brennan', where: { deck: 3, room: 'Mess hall' }, settle: 'eat' },
  { id: 'd1-zeke-dinner', day: 1, at: 18 * 60, until: 19 * 60, who: INTRO_ESCORT, where: { deck: 3, room: 'Mess hall' } },   // 0.42.41: he eats in the mess (section 21b's evening and laundry lines, CLOTHES_BEATS)
  { id: 'd2-solo', day: 2, at: 8 * 60 + 45, until: 9 * 60, who: 'calder', where: { deck: 5, room: 'Works Chief\'s office' }, meeting: 'introSoloJob', settle: 'solo' },
  { id: 'd2-tea', day: 2, at: 13 * 60, until: 13 * 60 + 45, who: INTRO_ESCORT, where: { deck: 5, room: 'Tea corner' }, says: 'walk.job3.tea' },   // his one check-in on your solo day
  { id: 'd2-health', day: 2, at: 14 * 60, until: 14 * 60 + 30, who: 'rina', where: { deck: 3, room: 'Infirmary' }, appt: 'intro-health', settle: 'health' },
  { id: 'd2-booths', day: 2, at: 18 * 60, until: 19 * 60, who: 'eklund-leila', where: { deck: 3, room: 'Call-home booths' }, settle: 'call' },
  { id: 'd3-pick', day: 3, at: 9 * 60, until: 9 * 60 + 15, who: INTRO_ESCORT, where: { deck: 5, room: 'Works bay' }, settle: 'take' },
  { id: 'd3-store', day: 3, at: 16 * 60 + 30, until: 17 * 60 + 30, who: 'ishikawa-orla', where: { deck: 3, room: 'Crew store' }, settle: 'buy' },
  { id: 'd3-pell', day: 3, at: 18 * 60 + 30, until: 20 * 60, who: 'pell', where: 'seek', seek: true, settle: 'friend' },
  { id: 'd4-mail', day: 4, at: 7 * 60, who: null, mail: { from: 'Zeke Torres', subject: 'On your own', body: 'Day off for me. Don\'t break anything big. — Z.' } },
  { id: 'd4-favour', day: 4, at: 16 * 60, until: 19 * 60 + 30, who: 'kovac-zainab', where: 'seek', seek: true, settle: 'favour' },
  { id: 'd4-quiz', day: 4, at: 20 * 60, until: 21 * 60 + 30, who: 'pell', where: { deck: 3, room: 'Bow lounge' }, settle: 'tradition' },
  { id: 'd5-mug', day: 5, at: 13 * 60, until: 13 * 60 + 45, who: 'halloran-emeka', where: { deck: 5, room: 'Tea corner' }, flags: ['mug'],
    moment: { title: 'Friday tea', here: 'Halloran hands you a mug with your name on it. "New hand\'s mug. It lives on the rack now. So do you."',
      mail: { from: 'Emeka Halloran', subject: 'Your mug', body: 'Missed you at tea. Your mug\'s on the rack in the tea corner, name and all. — E.H.' } } },
  { id: 'd5-invite', day: 5, at: 18 * 60, who: 'tomas', invite: { trad: 'sowing', day: 6, from: 'tomas' } },
  { id: 'd6-sowing', day: 6, at: 11 * 60 + 45, until: 12 * 60 + 40, who: 'tomas', where: { deck: 3, room: 'Hydroponics garden' }, settle: 'dayoff', flags: ['seedling'] },
  { id: 'd7-calder', day: 7, at: 18 * 60, who: null, mail: { from: 'I. Calder', subject: 'One week', body: 'One week. You\'ll do. — I. Calder' } },
  { id: 'd8-done', day: 8, at: 0, who: null, flags: ['week1.done'], end: true },
];
// the week's flags open social features one by one (the social plan, Part 7): favours from week1.d2, friends waving you
// over from week1.d3, invitations from week1.d5, moments and bunk visits after week1.done. Each at 06:00 on its day.
for (let d = 2; d <= 7; d++) INTRO_WEEK.push({ id: 'd' + d + '-flag', day: d, at: 6 * 60, who: null, flags: ['week1.d' + d] });
INTRO_WEEK.sort((a, b) => introAbs(a.day, a.at) - introAbs(b.day, b.at));

// ---- the Settling-in list: each item ticks itself when a ship note says you did the thing (any time, from anyone) ----
// The notes are section 13's bus: introStep { step, who } is this section's; act { act } (the player engineer's: wash,
// eat, laundry, buy, call), job { id, step, reserved }, apptKept { id }, favour, tradition { id, you }, tierUp { id, tier }
// are other sections' (DEV_NOTES "Hook register" lists who sends what).
const introStepIs = (...ids) => (k, d) => k === 'introStep' && ids.includes(d.step);
const SETTLE_KINDS = ['introStep', 'act', 'job', 'apptKept', 'favour', 'tradition', 'tierUp'];
const SETTLE = [
  { id: 'washed', title: 'Washed and fed', teacher: 'tomas', place: { deck: 4, room: 'Port washroom' }, done: (k, d) => k === 'act' && d.act === 'wash' },
  { id: 'team', title: 'Meet the team', teacher: 'calder', place: { deck: 5, room: 'Works bay' }, done: introStepIs('d1-briefing') },
  { id: 'shadow', title: 'Shadow a job', teacher: INTRO_ESCORT, place: { deck: 5, room: 'Works bay' }, done: (k, d) => k === 'job' && d.step === 'turnin' && d.reserved === 1 },
  { id: 'lead', title: 'Lead a job', teacher: INTRO_ESCORT, place: { deck: 5, room: 'Works bay' }, done: (k, d) => k === 'job' && d.step === 'turnin' && d.reserved === 2 },
  { id: 'eat', title: 'Eat with the crew', teacher: 'brennan', place: { deck: 3, room: 'Mess hall' }, done: (k, d) => k === 'act' && d.act === 'eat' && d.with > 0 },
  { id: 'solo', title: 'Your first solo job', teacher: 'calder', place: { deck: 5, room: 'Works Chief\'s office' }, done: (k, d) => k === 'job' && d.step === 'turnin' && (d.reserved === 3 || !d.reserved) },
  { id: 'health', title: 'Health check', teacher: 'rina', place: { deck: 3, room: 'Infirmary' }, done: (k, d) => k === 'apptKept' && (d.id === 'intro-health' || (SHIP.intro && d.id === SHIP.intro.done['d2-health:appt']) || (Array.isArray(d.with) && d.with.includes('rina'))) },   // any check-up with Rina (a skipped arrival books none)
  { id: 'call', title: 'Call home', teacher: 'eklund-leila', place: { deck: 3, room: 'Call-home booths' }, done: (k, d) => k === 'act' && d.act === 'call' },
  { id: 'take', title: 'Take a job yourself', teacher: INTRO_ESCORT, place: { deck: 5, room: 'Works bay' }, done: (k, d) => k === 'job' && d.step === 'take' && !d.reserved },
  { id: 'buy', title: 'Buy something', teacher: 'ishikawa-orla', place: { deck: 3, room: 'Crew store' }, done: (k, d) => k === 'act' && d.act === 'buy' },
  { id: 'friend', title: 'Make a friend', teacher: 'pell', place: null, done: (k, d) => k === 'tierUp' && d.tier >= 1 && d.id !== INTRO_ESCORT && d.id !== 'tomas' },
  { id: 'favour', title: 'Do a favour', teacher: 'kovac-zainab', place: null, done: k => k === 'favour' },
  { id: 'clothes', title: 'Change your clothes', teacher: INTRO_ESCORT, place: { deck: 4, room: 'Bunk 1' }, done: (k, d) => k === 'act' && d.act === 'clothes' },   // section 21b (0.42.40)
  { id: 'laundry', title: 'Laundry day', teacher: 'tomas', place: { deck: 4, room: 'Laundry' }, done: (k, d) => k === 'act' && d.act === 'laundry' },
  { id: 'tradition', title: 'Join a tradition', teacher: 'pell', place: { deck: 3, room: 'Bow lounge' }, done: (k, d) => k === 'tradition' && d.you },
  { id: 'dayoff', title: 'A day off', teacher: 'tomas', place: { deck: 3, room: 'Hydroponics garden' }, done: introStepIs('d6-sowing') },
];
SETTLE.push({ id: 'hobby', title: 'Try a hobby', teacher: INTRO_ESCORT, place: null, done: (k, d) => k === 'act' && d.act === 'hobby' });   // 0.60.7 (the player engineer, 0.28.63): section 15's hobbies send act 'hobby'
// the list listens on section 13's bus once it's there (onSim(kind, fn), fn called with the note's data)
let INTRO_HEARD = false;
if (typeof onSim === 'function') { INTRO_HEARD = true; for (const k of SETTLE_KINDS) onSim(k, d => settleNote(k, d)); onSim('job', introJobNote); onSim('apptMissed', introHealthMissed); }
// what Torres says as you work (stand-ins until the writers' lines): slot 1, the shadow shift, step by step; slot 2,
// the one you lead, only at the end
const INTRO_JOB_LINES = {
  1: { take: ['That one\'s ours. Lamp junction on Four. Your device has it under Jobs.', 'Arrow\'s yours to follow. I\'m right behind you.'],
    'stop.fetch': ['Storage. Relay off the shelf, top left. She\'s fussy about the left.'],
    'stop.make': ['The bracket we make. Lathe, slow and steady. Thirty minutes, mind your fingers.'],
    'stop.job': ['Panel open, old relay out, new one in. Hold it till it clicks.'],
    done: ['Listen to that. Nothing. That\'s the sound of it working.', 'Not done till it\'s turned in, though. Board.'],
    turnin: ['Your first one in the Record. Right: lunch, then you lead.'] },
  2: { take: ['Your lead. I\'m just the tall shadow.'], turnin: ['That one was all you. Good.'] },
  3: { turnin: ['Heard you did the Chief\'s job. Clean. Told you.'] },
};
// the shadow shift and the job you lead on Monday end when you turn in reserved slots 1 and 2 (section 17's job notes):
// their introStep notes are the core memories social keeps (intro.shadowShift)
// one of Torres's lines from the writers by its flag (content/lines/torres-zeke.lines, kind week1), or null
// (0.42.21) exactly the line gated by that flag: past a place's last line, and even before it once the week is under
// way, lineFor hands back one of his general week-1 lines (week1 is set all week)
function introWriterLine(flagKey, id = SHIP.intro.escort) {   // id: whose line (the escort's by default; 'raman' for the pilot)
  try {
    if (typeof lineFor !== 'function' || typeof VOICE === 'undefined') return null;
    const v = VOICE[id], e = ((v && v.lines && v.lines.week1) || []).find(x => x.flag === flagKey); if (!e) return null;
    // that exact line, filled as lineFor fills one ({me}, voice tokens); lineFor itself may prefer another week-1 line
    const who = typeof linesWho === 'function' ? linesWho(id) : null;
    const text = who && typeof linesFill === 'function' ? linesFill(e.text, who, { t: shipNow(), flags: { [flagKey]: true } }) : e.text;
    return text ? [text] : null;
  } catch (e) { return null; }
}
// every line under one flag key, in the file's order (a job step's talk-through: head writer 5, 0.48.78's turn-in), or null
function introWriterLines(flagKey, id = SHIP.intro.escort) {
  try {
    if (typeof VOICE === 'undefined' || typeof linesFill !== 'function') { const l = introWriterLine(flagKey, id); return l; }
    const v = VOICE[id], who = typeof linesWho === 'function' ? linesWho(id) : null;
    const out = ((v && v.lines && v.lines.week1) || []).filter(x => x.flag === flagKey).map(e => who ? linesFill(e.text, who, { t: shipNow(), flags: { [flagKey]: true } }) : e.text).filter(Boolean);
    return out.length ? out : null;
  } catch (e) { return null; }
}
// Zeke the trainer (0.42.31-0.42.32, the lead; head writer 0607's lines on these keys, a76e232): while he follows you
// (Day 1), each step of any job adds walk.train.<job>.<step> (job: the board's chore or kind through INTRO_TRAIN_JOB, so
// Day 1's held repairs are 'fault'; step: take, fetch, make, at (the panel), done, turnin); and walking together, between
// steps and between jobs, walk.follow.<n> in order, one every INTRO_FOLLOW_GAP, never repeated (the count is saved)
const INTRO_TRAIN_JOB = { repair: 'fault', restock: 'cart', inspect: 'round' }, INTRO_TRAIN_STEP = { take: 'take', 'stop.fetch': 'fetch', 'stop.make': 'make', 'stop.job': 'at', done: 'done', turnin: 'turnin' };
const INTRO_FOLLOW_GAP = 8000;                            // real ms between them
function introFollowing() {
  if (!introOn() || typeof ROSTER === 'undefined') return false;
  const p = ROSTER.find(x => x.id === SHIP.intro.escort), e = p && escortPlan(p, shipNow()); return !!e && e.mode === 'follow';
}
function introTrainLines(n, key) {
  const step = INTRO_TRAIN_STEP[key]; if (!step || !n.job || !introFollowing()) return null;
  return introWriterLines('walk.train.' + (INTRO_TRAIN_JOB[n.job] || n.job) + '.' + step);
}
function introFollowTick() {
  if (!introFollowing() || DIALOGUE || simNow() < (INTRO_UI.sayEnd || 0) || simNow() < INTRO_UI.next) return;   // simNow: the pause-aware clock, like the tour's (reviewer 0607's LOW)
  const a = introWalker(), now = simNow(); if (!a || a.pose !== 'walk' || Math.hypot(a.x - player.obj.position.x, a.z - player.obj.position.z) > 4) return;   // walking together
  if (now - (INTRO_UI.followAt || 0) < INTRO_FOLLOW_GAP) return;
  INTRO_UI.followAt = now; const k = (SHIP.intro.done['follow:n'] || 0) + 1, l = introWriterLine('walk.follow.' + k);
  if (l && typeof bubbleSay === 'function') { SHIP.intro.done['follow:n'] = k; bubbleSay(a.h, l[0], 4.5); INTRO_UI.next = now + INTRO_TOUR_GAP; }
}
function introJobNote(n) {
  if (!introOn() || !n) return;
  const key = n.step === 'stop' ? 'stop.' + n.tag : n.step;
  // the writers' first (kind week1, flag walk.job.<step> for slot 1, walk.job2.<step> and walk.job3.<step> for the
  // others; step: take, fetch, make, panel, done, turnin), else the stand-ins, else nothing
  let say = null;
  const fk = 'walk.job' + (n.reserved === 1 ? '' : n.reserved) + '.' + ({ 'stop.job': 'panel' }[key] || key.replace('stop.', ''));   // walk.job<slot>.<step>
  if (n.reserved >= 1 && n.reserved <= 3) say = introWriterLines(fk);
  if (!say) say = INTRO_JOB_LINES[n.reserved] && INTRO_JOB_LINES[n.reserved][key];
  const tr = introTrainLines(n, key); if (tr) say = (say || []).concat(tr);   // (0.42.31) Zeke the trainer: on any job while he's with you
  if (say && typeof introSay === 'function') introSay(say);
  if (n.reserved === 1 && n.step === 'take' && SHIP.device && SHIP.device.tipsSeen) for (const k of ['board', 'machine', 'turnin']) { if (typeof tipSeen === 'function') tipSeen(k); else SHIP.device.tipsSeen[k] = true; }   // Torres teaches these (section 19's tipSeen when it's there)
  if (n.step !== 'turnin' || !(n.reserved === 1 || n.reserved === 2)) return;
  const id = n.reserved === 1 ? 'd1-shadow' : 'd1-lead';
  if (SHIP.intro.done[id + ':job'] === undefined) { SHIP.intro.done[id + ':job'] = Math.floor(shipNow()); introNote('introStep', { step: id, who: SHIP.intro.escort }); }
}
function settleNote(kind, data) {
  const I = SHIP.intro; if (!I || !I.on && !I.skipped) return;
  for (const s of SETTLE) if (!I.settle[s.id] && s.done(kind, data || {})) I.settle[s.id] = Math.floor(shipNow());
  if (!I.settle.all && SETTLE.every(s => I.settle[s.id])) {
    I.settle.all = Math.floor(shipNow());
    introMail({ from: 'I. Calder', subject: 'Settled in', body: 'Everything on your list, done. Noted on your Record. — I. Calder' });
  }
}

// ---- the state and the save (save.intro, read defensively) ----
const introBlank = () => ({ on: false, step: null, since: null, near: null, day: 0, done: {}, missed: [], settle: {}, skipped: false, ended: false, escort: INTRO_ESCORT, flags: {} });
function introLoad(s) {
  const I = introBlank(), x = s && s.intro;
  if (!x || typeof x !== 'object') return I;
  I.on = !!x.on; I.skipped = !!x.skipped; I.ended = !!x.ended;
  I.step = INTRO_STEPS.some(t => t.id === x.step) || INTRO_WEEK.some(t => t.id === x.step) ? x.step : null;
  I.day = Number.isInteger(x.day) ? x.day : 0;
  I.since = x.since !== null && isFinite(x.since) ? +x.since : null;
  I.near = Array.isArray(x.near) && x.near.length === 2 && x.near.every(isFinite) ? x.near.map(Number) : null;
  for (const k of ['done', 'settle', 'flags']) if (x[k] && typeof x[k] === 'object') for (const i in x[k]) if (isFinite(x[k][i]) || x[k][i] === true) I[k][i] = x[k][i];
  if (Array.isArray(x.missed)) I.missed = x.missed.filter(id => INTRO_STEPS.some(t => t.id === id));
  if (typeof x.escort === 'string') I.escort = x.escort;
  return I;
}
SHIP.intro = introLoad(SAVED);
// a first launch arriving by shuttle (the lead's one design, with sim 0.26.25): section 13 starts every game as before
// and this section decides; its first frame (introTick, once every section has run) calls section 13's
// newGameStart(true) when there's no save, it isn't a test URL and this device has never arrived
let INTRO_BOOT = typeof SAVED !== 'undefined' && !SAVED && !NOSAVE && introWanted();
const introSave = () => JSON.parse(JSON.stringify(SHIP.intro));
SAVE_EXTRA.push(s => { s.intro = introSave(); });
const introOn = () => !!(SHIP.intro && SHIP.intro.on && !SHIP.intro.ended);
// the day you came aboard (section 18's "after arrival" rhythms count from it): always the arrival Sunday, Day 0, for
// you, whether you walked the evening, skipped it or started before there was an arrival
const introArrival = () => INTRO_START.day;
const introStepById = id => INTRO_STEPS.find(t => t.id === id) || INTRO_WEEK.find(t => t.id === id) || null;
const introStep = () => introOn() ? introStepById(SHIP.intro.step) : null;
const introArrived = () => { try { return !!localStorage.getItem(INTRO_KEY); } catch (e) { return false; } };
const introMarkArrived = () => { try { if (!NOSAVE) localStorage.setItem(INTRO_KEY, '1'); } catch (e) {} };
// a new arriving game (section 13's New game calls it in wave 2; never on a test URL): the state only, not the player
function introBegin(name) {
  for (const k of INTRO_FLAGS) introFlagSet(k, null);
  SHIP.intro = introBlank(); SHIP.intro.on = true; SHIP.intro.step = INTRO_STEPS[0].id;
  if (name !== undefined) { if (typeof playerNameSet === 'function') playerNameSet(name); else SHIP.player.name = String(name).trim().slice(0, 24) || null; }
  introFlagSet('escort.' + INTRO_ESCORT); introFlagSet('week1');
}

// for section 13's New game (newGameStart): whether a new game should arrive by shuttle (never on a test URL; once
// you've arrived before, wave 2's choice will ask; until then a returning player starts on Monday as before), and the
// intro's side of the fresh start, called after section 13 has cleared the flags and set the clock
// (a function declaration reading the key directly: section 13 asks this at load, before this section has run)
function introWanted() { try { return !NOSAVE && !localStorage.getItem('starship-cadet-arrived'); } catch (e) { return false; } }
function introNewGame(arriving) { try { introUiReset(); } catch (e) {} if (arriving) introBegin(); else SHIP.intro = introBlank(); }
// what the evening in play keeps between frames, back to a fresh start on New game (reviewer 1: on a second arrival
// the Chief never came to your table); an arrow of its own (Torres's, your bunk's) goes too
const INTRO_BED_GOAL = 'Head to your bunk when you\'re done looking around';   // a suggestion, not an order (the user, 0.60.5a)
function introUiReset() {
  const U = INTRO_UI; (U.said || []).forEach(simClear); U.night = null; U.chiefD = null;
  const own = typeof IX_GOAL !== 'undefined' && IX_GOAL && (IX_GOAL.label === INTRO_BED_GOAL || IX_GOAL.label === 'Zeke Torres' || INTRO_ARROW_LABELS.has(IX_GOAL.label));
  if (own && typeof clearGoal === 'function') clearGoal();
  Object.assign(U, { tableD: null, arrow: null, arrowAt: 0, min: null, step: undefined, said: [], callAt: 0, goal: false, goalKey: '', meet: [], next: 0, still: 0, stillAt: null, more: 0, bed: false, tour: [], pause: null, calder: false, calls: 0, beat: null, sow: false });
  if ('pilotAt' in U) Object.assign(U, { pilotAt: 0, ternOpened: false, ternShut: false });
}
// section 14 plans the crew again when this changes (introBeats depends on nothing else)
const introSig = () => (introOn() ? 'on' : 'off') + (SHIP.intro.skipped ? '|skipped' : '');

// one step done: its points, its flags, its note; then the next step (the evening) or none (the week runs by the clock)
function introDone(id, at = Math.floor(shipNow())) {
  const I = SHIP.intro, st = introStepById(id);
  if (!st || I.done[id] !== undefined) return;
  I.done[id] = at;
  for (const who in st.rel || {}) introRel(who, id, st.rel[who]);
  for (const f of st.flags || []) introFlagSet(f);
  introNote('introStep', { step: id, who: st.who });
  if (st.seek && typeof socialSeekAsk === 'function') socialSeekAsk(st.who, { from: at, until: introAbs(st.day, st.seek), why: 'intro:' + id });   // section 20: Tomas finds you
  const i = INTRO_STEPS.indexOf(st);
  if (i >= 0) { I.step = i + 1 < INTRO_STEPS.length ? INTRO_STEPS[i + 1].id : null; I.since = at; I.near = null; }
}
// the steps move on at minute t: here = { deck, tile } (the player), or null when the player isn't anywhere useful.
// On paper the tests pass `here` themselves; wave 2's frame tick passes the player's.
const INTRO_WITH = 10;                                   // tiles: he's with you
function introWithEscort(here) {                         // the real game only: the escort on your deck, near you
  const a = typeof introWalker === 'function' ? introWalker() : null;
  return !!(a && here && typeof deckDef !== 'undefined' && here.deck === deckDef.num && Math.max(Math.abs(cellAt(a.x, a.z)[0] - here.tile[0]), Math.abs(cellAt(a.x, a.z)[1] - here.tile[1])) <= INTRO_WITH);
}
function introAdvance(t, here) {
  const I = SHIP.intro; if (!introOn()) return;
  for (let guard = 0; guard < 40 && I.step; guard++) {    // the evening, one step at a time
    const st = introStepById(I.step), at = introAbs(st.day, st.at);
    if (t < at) break;
    const cp = st.checkpoint, f = st.fallback || {};
    const nx = INTRO_STEPS[INTRO_STEPS.indexOf(st) + 1];   // (0.42.31) a lead step on a deck you've ridden on from, to the next step's deck: done (the lift's, passed between two of its minutes)
    const there = !cp || here && here.deck === cp.deck && introRoomAt(here.deck, here.tile) === cp.room
      && Math.max(Math.abs(here.tile[0] - cp.tile[0]), Math.abs(here.tile[1] - cp.tile[1])) <= INTRO_REACH
      || !!(cp && here && st.mode === 'lead' && here.deck !== cp.deck && nx && nx.checkpoint && nx.checkpoint.deck === here.deck);
    if (there) { introDone(st.id, Math.max(at, Math.floor(t))); continue; }
    // (0.42.31, the user on 0.60.6: Zeke already in the mess, not with you off the lift) his own steps never time out while
    // he's with you (on your deck, within INTRO_WITH tiles): you're lingering together; until 19:00, then as before
    if (st.who === I.escort && f.until === undefined && t < introAbs(0, 19 * 60) && introWithEscort(here)) { I.near = [I.near ? I.near[0] : 99, Math.floor(t)]; break; }
    // the wait counts from when the step became yours, or from the last minute you got nearer to it than the minute
    // before, on its deck (so nobody on their way loses a step); once you've missed one, he waits only 5 minutes at
    // each until you catch up (so the evening still ends by 20:00 if you never come)
    if (cp && here && here.deck === cp.deck) {
      const dist = Math.max(Math.abs(here.tile[0] - cp.tile[0]), Math.abs(here.tile[1] - cp.tile[1]));
      I.near = [dist, I.near && dist < I.near[0] ? Math.floor(t) : I.near ? I.near[1] : at];   // [tiles away now, the last minute you got nearer]
    }
    const prev = INTRO_STEPS[INTRO_STEPS.indexOf(st) - 1], wait = prev && I.missed.includes(prev.id) ? Math.min(5, f.wait || 20) : (f.wait || 20);
    const late = f.until !== undefined ? introAbs(st.day, f.until) : Math.max(at, I.since === null ? at : I.since, I.near ? I.near[1] : at) + wait;
    if (t < late) break;
    introMail(f.mail, late);                              // you weren't there: the gist by Mail, and on to the next one
    I.done[st.id] = late; I.missed.push(st.id); introNote('introStep', { step: st.id, who: st.who, missed: true });
    for (const fl of f.flags || []) introFlagSet(fl);
    const j = INTRO_STEPS.findIndex(x => x.id === f.later);
    I.step = j >= 0 ? f.later : null; I.since = late; I.near = null;
    for (const s of INTRO_STEPS.slice(INTRO_STEPS.indexOf(st) + 1, j)) if (I.done[s.id] === undefined) { I.done[s.id] = late; I.missed.push(s.id); }   // skipped over
  }
  for (const b of INTRO_WEEK) {                           // the week, by the clock
    const at = introAbs(b.day, b.at);
    if (t < at || I.done[b.id] !== undefined) continue;
    I.done[b.id] = at; I.day = b.day;
    for (const f of b.flags || []) introFlagSet(f);
    if (b.mail) introMail(b.mail, at);
    if (b.reserve && typeof jobReserve === 'function') for (const r of INTRO_JOBS) jobReserve(...r);
    if (b.reserve) introBookHealth();
    if (b.seek && typeof socialSeekAsk === 'function') socialSeekAsk(b.who, { from: at, until: introAbs(b.day, b.until), why: 'intro:' + b.id });   // section 20: they come and find you
    if (b.invite && typeof socialInvite === 'function') socialInvite(b.invite);   // section 20: Tomas asks you to Sowing morning
    if (b.id === 'd1-briefing' || b.id === 'd6-sowing') introNote('introStep', { step: b.id, who: b.who });
    if (b.end) introEnd(true);
  }
}
// "I know my way around" (the device), the week's end, or skip: the scripted beats stop, the list stays as a checklist
function introEnd(finished) {
  const I = SHIP.intro; if (!I.on || I.ended) return;
  I.ended = true; I.step = null; if (typeof introArrowClear === 'function') introArrowClear();
  for (const k of INTRO_FLAGS) if (k !== 'mug' && k !== 'seedling') introFlagSet(k);
  if (typeof jobRelease === 'function') jobRelease();   // section 17: any of the week's jobs you haven't taken go to the crew
  introMarkArrived();
  introNote('introStep', { step: finished ? 'done' : 'ended', who: null });
}
// skip to Monday morning (0.42.6, for a player who knows the ship): the same points as after the arrival evening, no
// scripted week (no beats, no reserved jobs, the tips teach instead), every social gate open at once (all of
// INTRO_FLAGS but 'mug' and 'seedling', as when an intro ends); the Settling-in list stays as a checklist
function introSkip() {
  introBegin();
  const I = SHIP.intro;
  for (const st of INTRO_STEPS) {
    I.done[st.id] = introAbs(INTRO_START.day, INTRO_START.min);
    for (const who in st.rel || {}) introRel(who, st.id, st.rel[who]);
    for (const f of st.flags || []) introFlagSet(f);
  }
  for (const k of INTRO_FLAGS) if (k !== 'mug' && k !== 'seedling') introFlagSet(k);
  I.step = null; I.skipped = true; I.ended = true; I.day = 1; introMarkArrived();
  if (typeof ternRamp === 'function') ternRamp(true, 0);   // never left shut behind a skip
}
// the escort's walker mode at minute t (section 10 drives him with it): lead to the checkpoint, wait there, follow
// you (Monday afternoon), or null (his own plan)
// the dinner table (0.42.15, the lead: Calder comes visibly to your table and you all sit): who sits where from the
// Chief's step until Torres lets you go (after his goodnight, 19:30 at the latest). Section 10 seats Torres and Calder, section 15 the player.
function introSeat(who) {
  if (!introOn()) return null;
  const I = SHIP.intro; if (I.step !== 'table' && I.step !== 'chief' && I.step !== 'free') return null;
  const st = introStepById('chief'); return (st.seats && st.seats[who === SHIP.intro.escort ? INTRO_ESCORT : who]) || null;
}
const introEscorting = st => !!(st && st.checkpoint && INTRO_STEPS.indexOf(st) >= 0 && INTRO_STEPS.indexOf(st) < INTRO_STEPS.findIndex(x => x.id === 'free'));
function escortPlan(p, t) {
  const I = SHIP.intro; if (!introOn() || !p || p.id !== I.escort) return null;
  const st = introStepById(I.step);
  // he's yours until he lets you go (the 'free' step): he waits where he's to meet you or show you something, and leads
  // you everywhere else, including to the table where the Chief stops by (her step, not his)
  if (introEscorting(st) && introSeat(p.id)) return { mode: 'wait', to: introSeat(p.id) };   // at dinner: he walks to his seat and sits (section 10, sim 0.26.26)
  if (introEscorting(st) && st.mode === 'lead' && INTRO_UI.pause) return { mode: 'wait', to: INTRO_UI.pause };   // pausing for the tour's core lines (introTourTick)
  if (introEscorting(st)) return { mode: st.who === p.id && st.mode !== 'lead' ? 'wait' : 'lead', to: { deck: st.checkpoint.deck, tile: st.checkpoint.tile },
    pace: st.mode === 'lead' && st.checkpoint.deck === 5 && I.done['tour:lift'] === undefined ? INTRO_STROLL : 1 };   // strolling to the lift (section 10 reads pace)
  if (st && st.id === 'free' && introSeat(p.id)) return { mode: 'wait', to: introSeat(p.id) };   // at the table until his goodnight
  const scene = typeof DIALOGUE !== 'undefined' && DIALOGUE && DIALOGUE.m && /^intro-/.test(DIALOGUE.m.id || '');   // (the lead, 0.42.30: Calder's briefing plays in full first)
  const tea = typeof introTeaPlan === 'function' && !scene ? introTeaPlan(t) : null; if (tea) return tea;   // Zeke's Day 1 tea (0.42.61)
  for (const b of INTRO_WEEK) if (b.escort && b.who === p.id && t >= introAbs(b.day, b.at) && t < introAbs(b.day, b.until) && !scene) return { mode: b.escort, to: b.where };
  return null;
}
// what section 14's introPlan needs: one person's intro beats on day d ({ id, at, until, where, also }), or []
function introBeats(id, d) {
  if (!introOn()) return [];
  const out = [];
  for (const st of INTRO_STEPS) if (st.day === d && st.who === id && st.checkpoint) { const f = st.fallback || {}, seat = (st.away && st.away[id]) || st.seats && st.seats[id], tb = st.id === 'chief' && st.seats && introStepById('table'); out.push({ id: st.id, at: tb && tb.at != null ? Math.min(st.at, tb.at) : st.at, until: f.until !== undefined ? f.until : st.at + (f.wait || 20), where: seat ? { ...st.checkpoint, placeId: seat } : st.checkpoint }); }
  for (const b of INTRO_WEEK) if (b.day === d && (b.who === id || (b.also || []).includes(id)) && b.until) out.push({ id: b.id, at: b.at, until: b.until, where: b.where });
  return out;
}

// ---- the arrival evening in play (wave 2, 0.42.5): introTick() once a frame from the main loop (section 12). With the
// intro off (every test URL, every game before Pillar 4) it returns at once. Everything below only shows things: the
// steps themselves move on in introAdvance, once a ship minute, from where you are.
// The escort's lines as he walks (stand-ins from the plan, until the writers' content replaces them): said in his
// speech bubble (section 8b's bubbleSay) as each step becomes yours, a few seconds apart.
const INTRO_LINES = {
  hello: ['You must be the new hand. Zeke Torres, Works. Welcome to the Wren.', 'Right, onward. Stay close.'],
  haulway: ['Cargo hold on the left, Cart bay on the right.', 'Mind the carts. They don\'t mind you.'],
  works: ['That\'s us. The board, the tea corner, the Chief\'s glass office.', 'Tomorrow, ten to nine. Right here.'],
  lift: ['Four, please. Panel\'s all yours.'],
  wing: ['Washrooms. Hot water till ten, then it\'s character-building.', 'Laundry, common room. Nearly there.'],
  toMess: ['Dinner. Mess is on Three.'],
  servery: ['Grab a tray. Brennan doesn\'t bite. Much.'],
  free: ['You\'re free. Bunk\'s yours any time from eight.', 'I\'m on Four if you need me. Fourteen, the one with the music.'],
};
const INTRO_CALL = ['This way!', 'Over here, new hand.', 'Keep up. The ship\'s bigger than it looks.'];
// stand-in meeting scripts, used only while the writers' MEETING_SCRIPTS of the same id aren't there
const INTRO_STUB_SCRIPTS = {
  introBunk: { title: 'Your bunk', from: 'Zeke Torres', lines: [
    { who: INTRO_ESCORT, text: 'Bunk 1. Bottom one\'s yours. Bag in the locker, there.' },
    { who: INTRO_ESCORT, text: 'And this is yours too: your device. Schedule, maps, Mail, the lot. Don\'t lose it.' },
    { who: INTRO_ESCORT, text: 'Right. Dinner. Come on.' }] },
  introChief: { title: 'The Chief stops by', from: 'I. Calder', lines: [
    { who: 'calder', text: 'I\'m not here. Day off. Welcome aboard.' },
    { who: 'calder', text: 'Torres has you tomorrow. Ten to eight, the Works bay. Tuesday, your first job is mine.' },
    { choice: [
      { text: 'Looking forward to it.', rel: { calder: 1 }, reply: { who: 'calder', text: 'Good.' } },
      { text: 'What should I read up on?', rel: { calder: 2 }, reply: { who: 'calder', text: 'The scrubber manual. Chapter three. Nobody reads chapter three.' } },
      { text: '(Say nothing.)', reply: { who: 'calder', text: 'Quiet. Good. The ship\'s loud enough.' } }] },
    { who: 'calder', text: 'Eat something. That\'s an order, and I\'m not even here.' }] },
};
for (const id in INTRO_STUB_SCRIPTS) if (!MEETING_SCRIPTS[id]) MEETING_SCRIPTS[id] = { ...INTRO_STUB_SCRIPTS[id], gist: INTRO_MEETINGS[id].gist };
INTRO_STUB_SCRIPTS.introBriefing = { title: 'Monday briefing', from: 'I. Calder', lines: [
  { who: 'calder', text: 'Morning. Board\'s light, ship\'s quiet. Keep it that way.' },
  { who: 'calder', text: 'New hand shadows Torres today. Torres: one job, start to finish, properly.' },
  { who: INTRO_ESCORT, text: 'Properly. Always.' },
  { who: 'calder', text: 'Good. Go.' }] };
INTRO_STUB_SCRIPTS.introSoloJob = { title: 'Your first solo job', from: 'I. Calder', lines: [
  { who: 'calder', text: 'Sit. This one\'s yours: the other lamp junction on Four. It\'s on your device.' },
  { who: 'calder', text: 'Every job goes in your Record. I read the Record, not the talk.' },
  { who: 'calder', text: 'Progress talks: any time. Book it. Now go and fix my lamp.' }] };
for (const id of ['introBriefing', 'introSoloJob']) if (!MEETING_SCRIPTS[id]) MEETING_SCRIPTS[id] = { ...INTRO_STUB_SCRIPTS[id], gist: INTRO_MEETINGS[id].gist };
const INTRO_UI = { min: null, step: undefined, said: [], callAt: 0, goal: false, goalKey: '', manifest: null, meet: [], next: 0, still: 0, stillAt: null, more: 0, bed: false, tour: [], pause: null, pilotAt: 0, ternOpened: false, ternShut: false };
INTRO_STUB_SCRIPTS.introDinner = { title: 'Dinner with Torres', from: 'Zeke Torres', lines: [
  { who: INTRO_ESCORT, text: 'Engines, me. Deck 6. The drive coils, mostly. Coil three\'s my favourite. Don\'t tell the others.' },
  { who: INTRO_ESCORT, text: 'Two years aboard. Day shift, tea and biscuits at one. Works never misses tea.' },
  { choice: [
    { text: 'Why coil three?', rel: { [INTRO_ESCORT]: 1 }, reply: { who: INTRO_ESCORT, text: 'She hums a half-step flat. Like she\'s thinking about something.' } },
    { text: 'What\'s a normal day?', reply: { who: INTRO_ESCORT, text: 'Board at nine, jobs, tea, jobs, dinner. Then the ship\'s yours till ten.' } }] },
  { who: INTRO_ESCORT, text: 'Ah. Here\'s the Chief. Sit up straight.' }] };
if (!MEETING_SCRIPTS.introDinner) MEETING_SCRIPTS.introDinner = { ...INTRO_STUB_SCRIPTS.introDinner, gist: INTRO_MEETINGS.introDinner.gist };
// Torres's tour (0.42.20, the user: "a proper introduction to the ship and to himself, the whole way"; paced in 0.42.21b,
// the user's pacing A after reviewer 1c found a follower heard 19 of 61 lines): places along the walk, reached strictly
// in order (within r tiles, on its deck; one a tick; a place you never reach is passed once the walk is two steps
// beyond its `step`). Each place's lines go into one queue, one bubble at a time 3.6 s apart, never over a meeting,
// and a place starts only when the last one's core lines are done: its `core` first lines (or the writers' entries
// marked core) always play, and Torres pauses where he is while they do (escortPlan; you within 5 tiles, at most as long
// as they take); the rest are extras, heard while you linger at the place (or tap him there), dropped once you've
// moved on or the next place is waiting. The tour ends at the table: anything left is dropped. The writers' lines are
// walk.<id>.1, .2 ... (content/lines/torres-zeke.lines, kind week1); else the stand-ins. Standing still near him on
// a walking step with the tour quiet gives the next walk.more.<n> line.
const INTRO_STROLL = 0.5;                                 // his pace on the walk to the lift (x CREW_SPEED): time for the welcome talk
const INTRO_TOUR_GAP = 3600;                              // real ms between his tour lines (a 60-character bubble reads in about 3 s)
// his first lines wait until you've reached him (the user on 0.63.1, 0.42.47): the greeting at the ramp starts only within
// INTRO_CLOSE m of you, so it doesn't fly by as you walk up; the tour's pacing is otherwise as it was (the user: "perfect")
const INTRO_CLOSE = 3.5;
const introClose = a => !!a && typeof player !== 'undefined' && Math.hypot(a.x - player.obj.position.x, a.z - player.obj.position.z) <= INTRO_CLOSE;
const INTRO_TOUR = [
  // before the lift (the user on 0.60.5): one stop at the ramp to welcome you, then walk-and-talk (`walk`: he never
  // pauses, strolling at INTRO_STROLL): walk.up in order from 3 tiles off the ramp (`leave`), walk.works as you pass the
  // Works bay (`must`: next, and heard even if that's at the lift); walk.up lines unsaid at the lift are skipped (head writer 4)
  { id: 'shuttle', deck: 5, at: [5, 10], r: 2, stub: 'hello', step: 'hello', core: 3 }, { id: 'up', deck: 5, at: [5, 10], leave: 3, stub: 'haulway', step: 'haulway', core: 12, walk: true },
  { id: 'works', deck: 5, at: [16, 6], r: 2, stub: 'works', step: 'works', core: 2, walk: true, must: true },
  { id: 'lift', deck: 5, at: [15, 9], r: 2, stub: 'lift', step: 'lift', core: 3 },
  { id: 'officers', deck: 4, at: [21, 5], r: 3, step: 'wing', core: 3 }, { id: 'wing', deck: 4, at: [12, 4], r: 3, stub: 'wing', step: 'wing', core: 2 },
  { id: 'deck3', deck: 3, at: [22, 7], r: 3, stub: 'toMess', step: 'toMess', core: 2 }, { id: 'servery', deck: 3, at: [33, 3], r: 2, stub: 'servery', step: 'servery', core: 3 },
];
// a place's lines split into { core, extra }: the writers' entries marked core if any are, else its first `core` lines
// (head writer 3, content 0.48.49: walk.<place>.1..N are core, N as below)
function introTourSplit(t) {
  const all = introTourLines(t.id, t.stub), L = (typeof VOICE !== 'undefined' && VOICE[SHIP.intro.escort] && VOICE[SHIP.intro.escort].lines && VOICE[SHIP.intro.escort].lines.week1) || [];
  const marked = all.map((x, i) => { const e = L.find(y => y.flag === 'walk.' + t.id + '.' + (i + 1)); return !!(e && e.core); });
  if (marked.some(Boolean)) return { core: all.filter((x, i) => marked[i]), extra: all.filter((x, i) => !marked[i]) };
  return { core: all.slice(0, t.core || 2), extra: all.slice(t.core || 2) };
}
const introAtTour = (t, here) => deckDef.num === t.deck && Math.max(Math.abs(here[0] - t.at[0]), Math.abs(here[1] - t.at[1])) <= t.r + 1;
function introTourLines(id, stub) {
  const out = []; for (let n = 1; n <= 12; n++) { const l = introWriterLine('walk.' + id + '.' + n); if (!l) break; out.push(l[0]); }
  return out.length ? out : (stub && INTRO_LINES[stub]) || [];
}
function introTourTick() {
  const I = SHIP.intro, st = introStep(), fin = st && st.id === 'free' && INTRO_UI.tour.length;   // (the last core lines may run on past dinner's steps)
  if ((!introEscorting(st) && !fin) || typeof player === 'undefined') return;
  const here = player.here(), now = simNow(), a = introWalker(), Q = INTRO_UI.tour;
  const t = INTRO_TOUR.find(x => I.done['tour:' + x.id] === undefined);   // only the next place can be reached
  const td = t && Math.max(Math.abs(here[0] - t.at[0]), Math.abs(here[1] - t.at[1]));
  if (t && deckDef.num === t.deck && (t.leave ? td > t.leave : td <= t.r)) {   // (before the dinner hand-over: its step may move on in the very frame you arrive)
    I.done['tour:' + t.id] = Math.floor(shipNow());
    { const L = introTourSplit(t), q = { t, ...L, at: 0, held: 0, cap: (L.core.length + 1) * INTRO_TOUR_GAP }, k = Q.findIndex(x => x.t.walk && !x.t.must); if (t.must && k >= 0) Q.splice(k, 0, q); else Q.push(q); }   // (a must place goes before the walk's lines)
    if (!t.walk) for (let i = Q.length - 1; i >= 0; i--) if (Q[i].t.walk && !Q[i].t.must) Q.splice(i, 1);   // at the lift, the walk's lines left unsaid are skipped
  } else if (t && INTRO_STEPS.indexOf(st) >= INTRO_STEPS.findIndex(x => x.id === t.step) + 2) I.done['tour:' + t.id] = -1;   // passed it without coming near
  if (st.id === 'table' || st.id === 'chief' || st.id === 'free') {   // the tour hands over to dinner: extras and places not yet reached are dropped; the core
    Q.forEach(q => { q.extra.length = 0; }); INTRO_UI.pause = null;   // lines left finish first (the dinner chat waits for them, introTick)
    for (const x of INTRO_TOUR) if (I.done['tour:' + x.id] === undefined) I.done['tour:' + x.id] = -1;
    while (Q.length && !Q[0].core.length) Q.shift();
    if (Q.length && !DIALOGUE && a && typeof bubbleSay === 'function' && now >= INTRO_UI.next) { bubbleSay(a.h, Q[0].core.shift(), 4.5); INTRO_UI.next = now + INTRO_TOUR_GAP; }
    return;
  }
  // a place whose core lines are done goes once the next is waiting or you've left it (its extras dropped); one on a
  // deck you've left goes whole (you went on without him: Deck 5's lines never play on Deck 4)
  while (Q.length && (Q[0].t.deck !== deckDef.num || (!Q[0].core.length && (Q.length > 1 || !Q[0].extra.length || !introAtTour(Q[0].t, here))))) Q.shift();
  const head = Q[0], near = a && Math.hypot(a.x - player.obj.position.x, a.z - player.obj.position.z) <= 5;
  // he pauses where he is while core lines are waiting and you're with him (at the ramp and from the lift on: never on the walk between, the `walk` places), never longer in all than a place's lines take
  // (only the time he's actually held counts: not meetings, not the lift)
  const hold = head && head.core.length && Q.some(q => !q.t.walk) && near && !DIALOGUE && head.held < head.cap;
  if (hold) head.held += Math.min(250, now - (INTRO_UI.tickAt || now));
  INTRO_UI.tickAt = now;
  if (hold && !INTRO_UI.pause) INTRO_UI.pause = cellAt(a.x, a.z); else if (!hold) INTRO_UI.pause = null;   // his tile on this deck (the queue holds only this deck's places)
  if (DIALOGUE || !a || typeof bubbleSay !== 'function') return;
  if (head) {
    if (now >= INTRO_UI.next && (head.t.id !== 'shuttle' || introClose(a))) {   // his first lines wait until you've reached him (the user on 0.63.1, 0.42.47)
      const text = head.core.length ? head.core.shift() : head.extra.shift();
      if (!head.at) head.at = now; bubbleSay(a.h, text, 4.5); INTRO_UI.next = now + INTRO_TOUR_GAP; INTRO_UI.still = now;
    }
    return;
  }
  // standing still near him with nothing else to say: a line about himself
  const key = here.join(','); if (key !== INTRO_UI.stillAt) { INTRO_UI.stillAt = key; INTRO_UI.still = now; return; }
  if (now - INTRO_UI.still > 8000 && now >= INTRO_UI.next && st.mode !== 'meet' && Math.hypot(a.x - player.obj.position.x, a.z - player.obj.position.z) <= 3) {
    const l = introWriterLine('walk.more.' + (INTRO_UI.more + 1)); INTRO_UI.still = now;
    if (l) { INTRO_UI.more++; bubbleSay(a.h, l[0], 4.5); INTRO_UI.next = now + INTRO_TOUR_GAP; }
  }
}
// the first night (the user): after Torres lets you go on Sunday, and on Monday evening if you never found it, the
// goal arrow points to your own bunk until you reach it (or sleep)
// the goodnight (the user, after 0.60.3): once the Chief's welcome is over and his last tour lines are said, Torres says
// goodnight (the writers' walk.goodnight.<n> in order, else the stand-in), and that lets you go: the 'free' step (else
// at 19:30, reviewer 1c: the evening isn't held to a fixed 19:00). The first night's bunk arrow waits for it
// (introBedTick). Not with you then (another deck, or more than 6 tiles off), or gone before he's finished: no line, the
// arrow anyway. SHIP.intro.done.goodnight: when (null: not said; day 0's minutes are negative)
const INTRO_GOODNIGHT = ['Explore as long as you like tonight. Early start, mind: get some sleep.'];
function introNightTick() {
  const I = SHIP.intro; if (!introOn() || I.done.goodnight !== undefined || typeof player === 'undefined') return;
  // after the Chief's welcome (her step done and her meeting over, or missed), or once 'free' came by the clock (19:30)
  const said = I.done['chief:end'] !== undefined || I.missed.includes('chief');
  if (I.done.free === undefined && (I.done.chief === undefined || !said || DIALOGUE || INTRO_UI.meet.length)) return;
  const p = player.obj.position, U = INTRO_UI, now = simNow(), a = introWalker(), near = !!a && Math.hypot(a.x - p.x, a.z - p.z) <= 6;
  if (!U.night) {
    if (U.tour.some(q => q.core.length)) return;          // his last tour lines first
    if (!near) { I.done.goodnight = null; introDone('free'); return; }
    U.night = []; for (let n = 1; n <= 4; n++) { const l = introWriterLine('walk.goodnight.' + n); if (!l) break; U.night.push(l[0]); }
    if (!U.night.length) U.night = INTRO_GOODNIGHT.slice();
  }
  if (!a || Math.hypot(a.x - p.x, a.z - p.z) > 10) { I.done.goodnight = Math.floor(shipNow()); U.night = null; introDone('free'); return; }   // you went: the arrow anyway
  if (DIALOGUE || now < U.next || typeof bubbleSay !== 'function') return;
  bubbleSay(a.h, U.night.shift(), 4.5); U.next = now + INTRO_TOUR_GAP;
  if (!U.night.length) { I.done.goodnight = Math.floor(shipNow()); U.night = null; introDone('free'); }   // and he lets you go
}
function introBedTick() {
  const I = SHIP.intro; if (I.done.bed !== undefined || typeof setGoal !== 'function') return;
  const now = Math.floor(shipNow()), on = (now < introAbs(1, 0) && I.done.goodnight !== undefined) || (now >= introAbs(1, 19 * 60) && now < introAbs(2, 0));
  const bed = typeof playerBed === 'function' ? playerBed() : '4-B1-4', pl = (DECKS[4].places || []).find(q => q.id === bed), me = player.here();
  // (reviewer 1: only when you have no arrow of your own, and it never clears one it didn't set)
  const mine = typeof IX_GOAL !== 'undefined' && IX_GOAL && IX_GOAL.label === INTRO_BED_GOAL;
  if ((typeof sleeping !== 'undefined' && sleeping) || (pl && deckDef.num === 4 && Math.hypot(me[0] - pl.at[0], me[1] - pl.at[1]) <= 1.5)) {
    I.done.bed = now; if (INTRO_UI.bed) { INTRO_UI.bed = false; if (mine) clearGoal(); } return;
  }
  if (on && !INTRO_UI.goal && !INTRO_UI.bed && !(typeof IX_GOAL !== 'undefined' && IX_GOAL)) { setGoal({ deck: 4, place: bed, label: INTRO_BED_GOAL }); INTRO_UI.bed = true; }
  else if (!on && INTRO_UI.bed) { INTRO_UI.bed = false; if (mine) clearGoal(); }
}
const introWalker = () => typeof DECK_CREW !== 'undefined' ? DECK_CREW.find(a => a.p && a.p.id === SHIP.intro.escort) || null : null;
// his walking lines: the writers' (content/lines/torres-zeke.lines, kind week1, gated flag:walk.<step>, through the
// dialogue engineer's lineFor), else the stand-ins above
function introLines(step) {
  if (step === 'call') { INTRO_UI.calls = (INTRO_UI.calls || 0) + 1; const c = introWriterLine('walk.call.' + ((INTRO_UI.calls - 1) % 5 + 1)) || introWriterLine('walk.call.1'); if (c) return c; }   // the writers' walk.call.1-5, in turn
  const w = introWriterLine('walk.' + step); if (w) return w;
  return step === 'call' ? [INTRO_CALL[((Math.floor(shipNow()) >> 1) % INTRO_CALL.length + INTRO_CALL.length) % INTRO_CALL.length]] : INTRO_LINES[step];
}
function introSay(lines) {                                // his lines, one now and the rest a few seconds apart
  INTRO_UI.said.forEach(simClear); INTRO_UI.said = [];
  INTRO_UI.sayEnd = simNow() + (lines || []).length * 4800 + 3000;   // (introFollowTick waits for them)
  (lines || []).forEach((text, i) => INTRO_UI.said.push(simTimeout(() => { const a = introWalker(); if (a && typeof bubbleSay === 'function') bubbleSay(a.h, text, 4.5); }, i * 4800)));
}
// A0: the shuttle's manifest, before the fade-in. The ship's clock holds at 17:30 (INTRO_START) until you've typed your name.
function introManifest() {
  if (INTRO_UI.manifest) return;
  const el = INTRO_UI.manifest = document.createElement('div');
  el.style.cssText = 'position:fixed;inset:0;z-index:40;display:flex;align-items:center;justify-content:center;background:#05080a;color:#d8efe6;font:16px/1.45 system-ui,sans-serif;padding:16px';
  el.innerHTML = '<form style="max-width:340px;width:100%;border:1px solid #2f4a44;border-radius:12px;padding:18px 18px 16px;background:#0c1416">'
    + '<div style="font-size:12px;letter-spacing:.12em;color:#7fb8a8">SHUTTLE TERN · PASSENGER MANIFEST</div>'
    + '<div style="margin:10px 0 4px">Destination: CSV Wren, Works department.<br>Arriving Sunday, ' + String(Math.floor(INTRO_START.min / 60)).padStart(2, '0') + ':' + String(INTRO_START.min % 60).padStart(2, '0') + '.</div>'
    + '<label style="display:block;margin-top:12px;font-size:13px;color:#9fc9bc">Your name</label>'
    + '<input maxlength="24" autocomplete="off" style="width:100%;box-sizing:border-box;margin-top:4px;padding:10px;border-radius:8px;border:1px solid #3d5a52;background:#132022;color:#e8f4ef;font:inherit">'
    + '<button style="width:100%;margin-top:12px;padding:10px;border-radius:8px;border:0;background:#2f6f5f;color:#fff;font:inherit">Sign and go aboard</button></form>';
  const input = el.querySelector('input');
  el.querySelector('form').onsubmit = e => {
    e.preventDefault();
    const name = input.value.trim(); if (!name) { input.focus(); return; }
    if (typeof playerNameSet === 'function') playerNameSet(name); else SHIP.player.name = name.slice(0, 24);
    el.remove(); INTRO_UI.manifest = null;
    introDone('manifest', introAbs(INTRO_START.day, INTRO_START.min));
    if (typeof eventFeel === 'function') eventFeel(['jolt'], 1);   // the Tern settles
    if (typeof tipShow === 'function') tipShow('walk', 'Tap where you want to go, or press and hold to walk.');
    INTRO_UI.pilotAt = simNow() + 2000;   // introTernTick, on the frame clock (reviewer 1c: not a timer)
    saveGame();
  };
  document.body.appendChild(el); setTimeout(() => input.focus(), 50);
}
// the Tern's ramp (0.42.22; the deck architect's ternRamp, 0.38.18): shut while you sign the manifest; about 2 s after,
// the pilot's line (on the frame clock, and once: done.pilot; Dev Raman over the speaker: the writers' raman week1 'pilot.ramp', else a stand-in) and it opens.
// Once you're off it and nobody's in its well or on the ramp (ternClear), it closes behind you; it opens again once
// Torres lets you go (on another deck it just snaps). After a reload the ramp is simply open, as the Tern always was.
const INTRO_PILOT = 'Down gently. Ramp\'s opening. Welcome to the Wren.';
function introPilot() {
  INTRO_UI.pilotAt = 0; if (!introOn() || typeof ternRamp !== 'function') return;
  SHIP.intro.done.pilot = Math.floor(shipNow());
  const text = (introWriterLine('pilot.ramp', 'raman') || [INTRO_PILOT])[0];
  toast('Dev Raman, the pilot', text); ternRamp(true, 2.5); INTRO_UI.ternOpened = true;
}
function introTernTick() {
  if (typeof ternRamp !== 'function' || !DECKS[5].tern) return;
  const I = SHIP.intro, k = INTRO_STEPS.findIndex(x => x.id === I.step), free = INTRO_STEPS.findIndex(x => x.id === 'free');
  if (I.step === 'ramp' && I.done.pilot === undefined) {   // the pilot's line is due (after a reload too: shut it again, then he speaks)
    if (!INTRO_UI.pilotAt) { INTRO_UI.pilotAt = simNow() + 2000; ternRamp(false, 0); }
    else if (simNow() >= INTRO_UI.pilotAt) introPilot();
    return;
  }
  if (INTRO_UI.ternShut) { if (k < 0 || k >= free) { INTRO_UI.ternShut = false; ternRamp(true); } return; }
  if (!INTRO_UI.ternOpened || deckDef.num !== 5 || ternRampOpen() < 1 || k < 0 || k >= free) return;
  const t = DECKS[5].tern, at = player.here();
  if (!t.aisle.concat([t.well], t.ramp).some(([i, j]) => i === at[0] && j === at[1]) && ternClear()) { INTRO_UI.ternShut = true; ternRamp(false, 3); }
}
// tap-to-ask (0.42.24; section 10's tapCrew calls it first, sim 0.26.31): while Torres is still showing you round (the
// evening up to 'free'), tapping him at a tour place with extras left has him say the next at once; else it opens the writers' introAsk (three questions) instead of the chat card; three asks
// at most (each counts as a meeting), then he's a plain tap again. Returns true when it opened.
function introTap(p) {
  if (!introOn() || !p || p.id !== SHIP.intro.escort || !introEscorting(introStep())) return false;
  if (typeof dialogueShow !== 'function' || typeof MEETING_SCRIPTS === 'undefined' || !MEETING_SCRIPTS.introAsk || (typeof DIALOGUE !== 'undefined' && DIALOGUE)) return false;
  const h = INTRO_UI.tour[0];   // at a tour place with extras left: the next one, now
  if (h && !h.core.length && h.extra.length && typeof player !== 'undefined' && introAtTour(h.t, player.here())) { INTRO_UI.next = 0; return true; }
  const I = SHIP.intro, n = [1, 2, 3].find(k => I.done['ask:' + k] === undefined); if (!n) return false;
  I.done['ask:' + n] = Math.floor(shipNow());
  if (typeof player !== 'undefined' && player.stop) player.stop();
  return dialogueShow('introAsk', { id: 'intro-ask', who: [p.id], where: { deck: deckDef.num, room: /./ }, at: shipNow() });
}
// the week's meetings (Monday's briefing, Tuesday's first solo job): while one is on, being in its room plays it; if
// you never came, its gist comes by Mail when it ends. Tuesday's job is yours either way: Calder hands it over in
// person, or it's simply in your Jobs (section 17's reserved slot 3, claimed for you).
// a meeting's script as it can be played here: the lines of anyone cast who isn't in the room are left out (Tomas may
// be elsewhere on Sunday evening); a choice and its replies stay. The trimmed copy is MEETING_SCRIPTS['<id>~here'].
function introScriptHere(id, m, keep) {   // keep: the step's own speaker, never left out
  const sc = MEETING_SCRIPTS[id]; if (!sc || typeof DECK_CREW === 'undefined') return id;
  const here = new Set(DECK_CREW.filter(a => { const r = roomAt(...cellAt(a.x, a.z)); return r && ROOMS[r] && m.where.room.test(ROOMS[r].name || ''); }).map(a => a.p.id));
  const away = (m.who || []).filter(w => w !== keep && !here.has(w)); if (!away.length) return id;
  MEETING_SCRIPTS[id + '~here'] = { ...sc, lines: sc.lines.filter(l => !l.who || !away.includes(l.who)) };
  return id + '~here';
}
// Tuesday's new-crew health check with Rina, already in your Appointments from Monday (the device's appointments,
// section 19; kept or missed by section 14's apptTick, which sends apptKept { id }: "Health check" ticks on it)
function introBookHealth() {
  const D = SHIP.device; if (!D || !Array.isArray(D.appts) || SHIP.intro.done['d2-health:appt'] !== undefined) return;
  introHealthAppt(introAbs(2, 14 * 60));
}
// the booking itself (kind 'checkup', the infirmary's, section 14's apptKind): any earlier game's one still to come is
// dropped first (reviewer 1: two New games in a page booked it twice); a missed one is booked again once, a day later
const INTRO_HEALTH_TITLE = 'New-crew health check';
function introHealthAppt(at) {
  const D = SHIP.device, pl = typeof apptPlaces === 'function' && apptPlaces().find(x => x.deck === 3 && /infirmary/i.test(x.name)); if (!pl) return null;
  D.appts = D.appts.filter(x => !(x.by === 'rina' && x.title === INTRO_HEALTH_TITLE && x.status === 'yes' && x.at > shipNow()));
  const id = D.appts.reduce((m, x) => Math.max(m, x.id), 0) + 1;
  D.appts.push({ id, with: ['rina'], at, len: 30, where: pl.id, kind: 'checkup', status: 'yes', by: 'rina', title: INTRO_HEALTH_TITLE });
  SHIP.intro.done['d2-health:appt'] = id; return id;
}
function introHealthMissed(n) {
  const I = SHIP.intro; if (!introOn() || !n || n.id !== I.done['d2-health:appt'] || I.done['d2-health:again'] !== undefined) return;
  const at = (Math.floor(shipNow() / 1440) + 1) * 1440 + 14 * 60;   // tomorrow, 14:00
  if (introHealthAppt(at)) { I.done['d2-health:again'] = Math.floor(shipNow()); introMail({ from: 'Rina Deshi', subject: 'Health check, again', body: 'Missed you today. No harm done: same time tomorrow, the infirmary. Ten minutes, I promise.' }, shipNow()); }
}
// the Works team's mug at Friday tea (a moment, no meeting): in the tea corner during it, they hand it over; else it's
// on the rack when you look, and a note says so
// the week's beats said in play (0.42.26; the writers' week-1 lines beat.<id>.<n>, kind week1 on the beat's teacher):
// in the beat's room during its window with them there too, their lines one bubble at a time (INTRO_TOUR_GAP), once;
// they stop while they talk; leave and the rest is dropped. A beat with no room of its own (Friday's invite) plays when they're within
// INTRO_BEAT_NEAR tiles of you in the four hours after it.
const INTRO_BEAT_NEAR = 6;
function introBeatLines(b) { const out = []; for (let n = 1; n <= 12; n++) { const l = introWriterLine('beat.' + b.id + '.' + n, b.who); if (!l) break; out.push(l[0]); } return out; }
function introBeatHere(b, a) {
  if (!a || typeof player === 'undefined') return false;
  const P = player.obj.position, room = c => (ROOMS[roomAt(...c)] || {}).name;
  if (!b.where || b.where === 'seek') return Math.hypot(a.x - P.x, a.z - P.z) <= INTRO_BEAT_NEAR;
  return deckDef.num === b.where.deck && room(player.here()) === b.where.room && room(cellAt(a.x, a.z)) === b.where.room;
}
function introBeatTick() {
  if (typeof DECK_CREW === 'undefined' || typeof bubbleSay !== 'function') return;
  const I = SHIP.intro, U = INTRO_UI, now = shipNow(), t = simNow(), crew = id => DECK_CREW.find(x => x.p && x.p.id === id);
  if (U.beat) {
    const a = crew(U.beat.b.who);
    if (!introBeatHere(U.beat.b, a)) U.beat = null;   // you (or they) left: the rest is dropped
    else if ((a.talking = Math.max(a.talking || 0, 1)) && !DIALOGUE && t >= U.next) { bubbleSay(a.h, U.beat.lines.shift(), 4.5); U.next = t + INTRO_TOUR_GAP; if (!U.beat.lines.length) U.beat = null; }   // they stop for it, facing you (section 10's tap pause)
    return;
  }
  if (DIALOGUE) return;
  for (const b of INTRO_WEEK) {
    if (!b.who || I.done[b.id + ':said'] !== undefined) continue;
    const from = introAbs(b.day, b.at), until = b.until !== undefined ? introAbs(b.day, b.until) : from + 240;
    if (now < from || now >= until || !introBeatHere(b, crew(b.who))) continue;
    I.done[b.id + ':said'] = Math.floor(now); const lines = introBeatLines(b); if (lines.length) { U.beat = { b, lines }; return; }
  }
}
// Saturday's Sowing (d6-sowing, 11:45): Tomas is on watch then (the crew have no lunch in the sim), so while you're on
// Deck 3 in its window he's walked to the garden for about ten minutes ("Holt said ten minutes"; section 10's
// crewComeTo) and then goes back to his watch; his rota is unchanged
const INTRO_SOW_MIN = 10, INTRO_SOW_SPOTS = ['3-tend-3', '3-tend-2', '3-tend-4', '3-tend-1'];
function introSowTick(now) {
  const b = INTRO_WEEK.find(x => x.id === 'd6-sowing'); if (!b || INTRO_UI.sow || typeof crewComeTo !== 'function' || deckDef.num !== b.where.deck) return;
  const from = introAbs(b.day, b.at), until = introAbs(b.day, b.until); if (now < from || now >= until - 5) return;
  const spot = INTRO_SOW_SPOTS.find(id => (typeof PLACE_OF === 'undefined' || PLACE_OF.has(id)) && !(typeof heldBy === 'function' && heldBy(id))); if (!spot) return;
  INTRO_UI.sow = true; crewComeTo(b.who, spot, null, { until: Math.min(until, now + INTRO_SOW_MIN + 5) });   // (+5: the walk up from Deck 2)
}
// someone who was to come and find you this week (section 20's socialSeekAsk) and never did: when the window ends, a
// Mail from them instead (reviewer 1): the writers' mail.<beatId> ("Subject | body", kind week1), else a stand-in
const INTRO_SEEK_MAIL = {
  'd3-pell': { subject: 'Quiz tomorrow', body: 'Looked for you tonight! Quiz night tomorrow, the bow lounge at eight. You\'re on my team.' },
  'd4-favour': { subject: 'A small favour', body: 'Could you look at the tea-corner kettle on Five when you pass? It clicks and sulks. Thank you!' },
};
function introSeekMail(now) {
  const I = SHIP.intro;
  for (const b of INTRO_WEEK) {
    if (!b.seek || I.done[b.id + ':seek'] !== undefined || now < introAbs(b.day, b.until)) continue;
    const ask = ((SHIP.social && SHIP.social.seekAsks) || []).find(a => a.id === b.who && a.from === introAbs(b.day, b.at));
    I.done[b.id + ':seek'] = ask && ask.done ? 1 : -1; if (ask && ask.done) continue;
    const w = introWriterLine('mail.' + b.id, b.who), k = w && w[0].indexOf(' | '), p = typeof ROSTER !== 'undefined' && ROSTER.find(x => x.id === b.who);
    const m = w && k > 0 ? { subject: w[0].slice(0, k), body: w[0].slice(k + 3) } : INTRO_SEEK_MAIL[b.id];
    if (m) introMail({ from: (p && p.name) || b.who, ...m }, now);
  }
}
function introMoments(now) {
  const I = SHIP.intro;
  for (const b of INTRO_WEEK) {
    if (!(b.moment || b.says) || I.done[b.id + ':met'] !== undefined) continue;
    const at = introAbs(b.day, b.at), until = introAbs(b.day, b.until); if (now < at) continue;
    const here = deckDef.num === b.where.deck && (ROOMS[roomAt(...player.here())] || {}).name === b.where.room;
    if (now < until && here) { I.done[b.id + ':met'] = now; if (b.moment) toast(b.moment.title, b.moment.here); if (b.says) introSay(introWriterLine(b.says) || []); }
    else if (now >= until) { I.done[b.id + ':met'] = -1; if (b.moment) introMail(b.moment.mail, until); }
  }
}
function introWeekMeetings(now) {
  const I = SHIP.intro;
  for (const b of INTRO_WEEK) {
    if (!b.meeting || I.done[b.id + ':met'] !== undefined) continue;
    const at = introAbs(b.day, b.at), until = introAbs(b.day, b.until); if (now < at) continue;
    const room = new RegExp('^' + b.where.room.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '$');
    const m = { id: 'intro-' + b.id, who: INTRO_MEETINGS[b.meeting].cast.filter(w => !/:/.test(w)), where: { deck: b.where.deck, room }, at };
    // it starts once its speaker is there too (or 10 minutes on, so a late speaker never holds it up for good)
    const speakerIn = typeof DECK_CREW !== 'undefined' && DECK_CREW.some(a => a.p.id === b.who && room.test((ROOMS[roomAt(...cellAt(a.x, a.z))] || {}).name || ''));
    if (now < until && (speakerIn || now >= at + 10) && !(typeof DIALOGUE !== 'undefined' && DIALOGUE) && typeof inMeeting === 'function' && inMeeting(m)) { I.done[b.id + ':met'] = now; dialogueShow(introScriptHere(b.meeting, m, b.who), m); }
    else if (now >= until) { I.done[b.id + ':met'] = -1; if (typeof meetingGist === 'function') meetingGist(b.meeting); }
    else continue;
    if (b.id === 'd2-solo' && typeof jobReserved === 'function' && typeof claimJob === 'function') { const id = jobReserved(3); if (id) claimJob(id); }
  }
}
// ---- the first-time arrows (onboarding 5, 0.42.60, the user's playtest notes for 0.63.2): the goal arrow (15b's setGoal)
// shows the way the first time you're told to do something. Day 1: the time clock once you're in the Works bay and have
// been told to clock in (the briefing over, or introArrowTold('clock') from whoever says it), then the job board the
// moment you've clocked in, until you take a job (your job's own arrow then). The servery the first time the Chief tells
// you to eat (Calder's "Eat something" at the arrival dinner; Brennan's Day 1 dinner beat if you missed her), unless
// you've a tray or have eaten. Each is shown again after a reload until it's done (I.done 'arrow:<id>', saved), never
// over someone else's arrow, and cleared once done or past its time.
const INTRO_ARROWS = {
  clock: { deck: 5, place: '5-timeclock-1', label: 'Clock in at the time clock' },
  board: { deck: 5, item: /job board/i, room: 'w', label: 'Take a job at the job board' },
  eat: { deck: 3, item: /^servery$/i, label: 'Get your dinner at the servery' },
  tea: { deck: 5, room: 't', label: 'Tea and biscuits with Zeke' },   // Zeke's Day 1 tea (introTeaTick, below)
  call: { deck: 3, room: 'B', label: 'Call home from the booths' },   // Day 0's call-home card, when you tap Track it (introCallTick)
};
INTRO_ARROWS.call.label = (typeof LINES !== 'undefined' && Array.isArray(LINES['tip.callhome.goal']) && LINES['tip.callhome.goal'][0] && LINES['tip.callhome.goal'][0].text) || INTRO_ARROWS.call.label;
const INTRO_CLOCK_AUTO = 8 * 60 + 50;                     // 0.72.5 (playtest 2, item 6): on your first shift, the time clock's arrow from 08:50 if you're in the Works bay (then the job board's, item 7)
const INTRO_EAT_MINS = 30;                                 // the servery arrow stays up this long after you're told to eat, at most (R3: never over the whole evening's bunk arrow and call card)
const INTRO_ARROW_LABELS = new Set(Object.values(INTRO_ARROWS).map(a => a.label));
function introArrowTold(id) { if (introOn() && INTRO_ARROWS[id] && SHIP.intro.done['told:' + id] === undefined) SHIP.intro.done['told:' + id] = Math.floor(shipNow()); }
function introArrowClear() {
  INTRO_UI.arrow = null;
  if (typeof IX_GOAL !== 'undefined' && IX_GOAL && INTRO_ARROW_LABELS.has(IX_GOAL.label) && typeof clearGoal === 'function') clearGoal();
}
// which arrow is wanted now, or null; marks the ones that are done or past
function introArrowWant(now) {
  const I = SHIP.intro, d = Math.floor(now / 1440) + 1, m = now - (d - 1) * 1440, fin = id => { if (I.done['arrow:' + id] === undefined) I.done['arrow:' + id] = Math.floor(now); };
  const P = SHIP.player, late = m >= 20 * 60 + 30;        // dinner's till half eight
  if (introTeaPhase(now) === 'go') return 'tea';
  if (I.done['call:track'] !== undefined && I.done['call:end'] === undefined) return 'call';
  if (P.tray || ACT && (ACT.kind === 'queue' || ACT.kind === 'eat')) I.done['ate:last'] = Math.floor(now);   // the last minute you had food in hand (or were queueing, eating)
  if (I.done['arrow:eat'] === undefined) {
    const at = typeof I.done['chief:end'] === 'number' ? I.done['chief:end'] : I.done['d1-dinner:said'];   // told to eat (null: walked away from the Chief)
    if (typeof at === 'number') { if (late || d > 1 || now >= at + INTRO_EAT_MINS || I.done['ate:last'] !== undefined && I.done['ate:last'] >= at - 60) fin('eat'); else return 'eat'; }
    else if (d > 1 || d === 1 && late) fin('eat');
  }
  if (d > 1 || typeof careerClockedIn !== 'function') { fin('clock'); fin('board'); return null; }
  if (d < 1) return null;
  const out = m >= (typeof CAREER !== 'undefined' ? CAREER.clockOut : 1020);
  if (I.done['arrow:clock'] === undefined) {
    let inBay = false; try { inBay = deckDef.num === 5 && roomAt(...player.here()) === 'w'; } catch (e) { inBay = false; }
    if (careerClockedIn(1) || out) fin('clock');
    else {
      const brief = INTRO_WEEK.find(b => b.id === 'd1-briefing'), opened = I.done['d1-opener'] !== undefined || I.done['d1-briefing:met'] !== undefined && now >= introAbs(1, brief.until) + 5;   // Zeke's training-day opener done (onboarding 4's 'd1-opener'), or the briefing's window five minutes gone
      if (I.done['told:clock'] === undefined && inBay && !DIALOGUE && (opened || m >= INTRO_CLOCK_AUTO)) I.done['told:clock'] = Math.floor(now);   // 0.72.5 (playtest 2, item 6): from 08:50 in the Works bay it comes up by itself
      if (I.done['told:clock'] !== undefined) return 'clock';
    }
  }
  if (I.done['arrow:board'] === undefined && careerClockedIn(1)) {
    if (out || typeof myJob === 'function' && myJob()) fin('board');
    else return 'board';
  }
  return null;
}
function introArrowTick() {
  const t = simNow(); if (t < (INTRO_UI.arrowAt || 0)) return; INTRO_UI.arrowAt = t + 250;   // four times a second
  introTeaTick(Math.floor(shipNow())); introCallTick(Math.floor(shipNow()));
  const id = introArrowWant(Math.floor(shipNow())), g = id && INTRO_ARROWS[id];
  const cur = typeof IX_GOAL !== 'undefined' ? IX_GOAL : null, ours = cur && (INTRO_ARROW_LABELS.has(cur.label) || cur.label === INTRO_BED_GOAL && id === 'call');   // 0.72.5 (playtest 2, item 3): the call-home arrow takes over from the first night's bunk arrow (up since the goodnight), which comes back once you're at the booths
  if (!g) { if (INTRO_UI.arrow) introArrowClear(); return; }
  if (cur && !ours) return;                               // someone else's arrow is up: ours waits for it
  if (!cur || cur.label !== g.label) setGoal(g);
  INTRO_UI.arrow = id;
}
// ---- call home on the first night (onboarding 5, 0.42.62; the user via lead 13): once the Chief's table visit is over
// (and you've food, if she told you to eat), a card says to call home, with Track it (the head writer's tip.callhome,
// .button, .goal; section 19's deviceChoose). Tracked, the arrow points to the Call-home booths on Deck 3 until you're
// in there (or 22:00); then the default arrow, your bunk, comes back. Saved in SHIP.intro.done: 'call:tip', 'call:track', 'call:end'.
const introText = (k, or) => { const L = typeof LINES !== 'undefined' && LINES[k], e = Array.isArray(L) && L[0]; return e && typeof e.text === 'string' ? e.text : or; };
function introCallTick(now) {
  const I = SHIP.intro, D = I.done; if (D['call:end'] !== undefined) return;
  if (now >= introAbs(0, 22 * 60)) { D['call:end'] = -1; return; }   // past quiet hours (and every later day)
  if (D['call:tip'] === undefined) {
    if (D['chief:met'] === undefined || INTRO_UI.chiefD || DIALOGUE || INTRO_UI.arrow === 'eat' || D['arrow:eat'] === undefined && typeof D['chief:end'] === 'number') return;
    const text = introText('tip.callhome', 'Call home tonight. The call booths are on Deck 3. Tell them you arrived safely.');
    const shown = typeof deviceChoose === 'function' && deviceChoose({ title: 'Call home', text, choices: [introText('tip.callhome.button', 'Track it')], cancel: 'Not now' }, k => {
      if (k === 0 && SHIP.intro.done['call:end'] === undefined) { SHIP.intro.done['call:track'] = Math.floor(shipNow()); INTRO_UI.arrowAt = 0; } else if (SHIP.intro.done['call:track'] === undefined) SHIP.intro.done['call:end'] = Math.floor(shipNow()); });
    if (shown) D['call:tip'] = now; else if (typeof deviceChoose !== 'function') D['call:end'] = -1;
    return;
  }
  if (D['call:track'] === undefined) return;
  let there = false; try { there = deckDef.num === 3 && roomAt(...player.here()) === 'B'; } catch (e) { there = false; }
  if (there) { D['call:end'] = now; INTRO_UI.bed = false; }   // reached: the bunk arrow (introBedTick) may come back
}
// ---- Zeke's Day 1 tea (onboarding 5, 0.42.61; the user: "Zeke explains it; once your job is finished he leads you there
// (tracked, with an arrow), then work carries on with Zeke following and chatting"). The 13:00 tea and biscuits in the
// Tea corner is the player engineer's (teaOut(t), teaHad(day), the 'tea' note) and the crew sim's (the Works crew,
// staggered). On Day 1, once you've taken your first job, Zeke explains it at the first quiet moment (walk.tea.explain.<n>);
// once that job's turned in and tea is out (and you've not had it), he says walk.tea.go.<n> and leads you to the Tea
// corner (escortPlan 'lead', the arrow INTRO_ARROWS.tea; the player engineer's own after-job arrow stays down while
// introTeaLead() is true); there he waits with you (walk.tea.at.<n>) until you've had tea, 20 minutes, or you leave,
// then says walk.tea.back.<n> and follows you again (the week's d1-lead). Saved in SHIP.intro.done: 'tea:told', 'tea:go',
// 'tea:at', 'tea:end' (-1: tea came and went without the walk). Tea that's over before your job is done: no walk.
const INTRO_TEA_AT = [23, 2], INTRO_TEA_STAY = 20;      // where he stands in the Tea corner (a free tile by the tea table, clear of the crew's three seats); minutes he stays at most
const INTRO_TEA_LINES = {                                 // stand-ins (the head writer's d47b63d), used only while the writers' lines are missing
  explain: ['One o\'clock\'s tea and biscuits, in the tea corner.', 'Most of Works goes, a few at a time. Fills a gap, too.', 'Finish this job, then I\'ll take you. Biscuits await.'],
  go: ['Job done. Tea\'s out. Come on.'], at: ['Mug off the hook. Biscuits in the tin.'], back: ['Right. Back to it. I\'m right behind you.'],
};
const introTeaSay = k => introWriterLines('walk.tea.' + k) || (() => { const out = []; for (let n = 1; n <= 6; n++) { const l = introWriterLine('walk.tea.' + k + '.' + n); if (!l) break; out.push(l[0]); } return out.length ? out : INTRO_TEA_LINES[k]; })();
function introTeaPhase(now) {                             // 'go' (he's leading you there), 'at' (tea together), or null
  const I = SHIP.intro; if (!introOn() || I.done['tea:go'] === undefined || I.done['tea:end'] !== undefined || Math.floor(now / 1440) + 1 !== 1) return null;
  return I.done['tea:at'] === undefined ? 'go' : 'at';
}
const introTeaLead = () => introOn() && SHIP.intro.done['tea:end'] === undefined && Math.floor(shipNow() / 1440) + 1 === 1;   // read by the player engineer's teaOffer: on Day 1 the tea is Zeke's (no after-job card or arrow) until his walk is over or off
function introTeaPlan(t) {                                // escortPlan's: where he is for the tea walk
  const ph = introTeaPhase(t); return !ph ? null : { mode: ph === 'go' ? 'lead' : 'wait', to: { deck: 5, tile: INTRO_TEA_AT } };
}
function introTeaTick(now) {
  const I = SHIP.intro, d = Math.floor(now / 1440) + 1, m = now - (d - 1) * 1440, D = I.done, end = v => { D['tea:end'] = v; };
  if (D['tea:end'] !== undefined || typeof teaOut !== 'function') return;
  if (d > 1) { end(-1); return; }
  if (d < 1 || DIALOGUE) return;
  const a = introWalker(), near = a && Math.hypot(a.x - player.obj.position.x, a.z - player.obj.position.z) <= 4, quiet = simNow() >= (INTRO_UI.sayEnd || 0) && simNow() >= INTRO_UI.next && simNow() - (INTRO_UI.followAt || 0) >= INTRO_TOUR_GAP;   // (not over one of his walk.follow lines)
  const room = () => { try { return deckDef.num === 5 && roomAt(...player.here()) === 't'; } catch (e) { return false; } };
  const had = typeof teaHad === 'function' ? teaHad(1) : SHIP.player.teaDay === 1;
  if (D['tea:go'] === undefined) {
    if (D['tea:told'] === undefined && near && quiet && introFollowing() && typeof myJob === 'function' && myJob()) { D['tea:told'] = now; introSay(introTeaSay('explain')); return; }
    if (m >= 13 * 60 && !teaOut(now) || had) { end(-1); return; }   // tea's over (or you've had it) before your job was done
    if (D['d1-shadow:job'] !== undefined && teaOut(now) && (quiet || m >= 13 * 60 + 10)) { const first = D['tea:told'] === undefined ? introTeaSay('explain') : []; D['tea:told'] = D['tea:told'] !== undefined ? D['tea:told'] : now; D['tea:go'] = now; introSay(first.concat(introTeaSay('go'))); }   // not explained yet (a quick job): both now
    return;
  }
  if (D['tea:at'] === undefined) {
    if (room()) { D['tea:at'] = now; introSay(introTeaSay('at')); }
    else if (!teaOut(now)) { end(now); introArrowClear(); }   // tea's over before you got there
    return;
  }
  if (had || now >= D['tea:at'] + INTRO_TEA_STAY || !room() && now >= D['tea:at'] + 2 || !teaOut(now)) { end(now); if (quiet || had) introSay(introTeaSay('back')); }
}
// the Chief at your table: her agent within a tile of her seat (section 10's crewComeTo brings her)
function introCalderIn() {
  const id = introSeat('calder'), a = typeof DECK_CREW !== 'undefined' && DECK_CREW.find(x => x.p && x.p.id === 'calder'), sp = id && typeof placeSpot === 'function' ? placeSpot(id) : null;
  return !!(a && sp && Math.hypot(a.x - sp.x, a.z - sp.z) <= 1.2);
}
function introTick() {
  if (INTRO_BOOT) { INTRO_BOOT = false; if (typeof newGameStart === 'function') newGameStart(true); }
  if (!introOn() || typeof player === 'undefined') return;
  const I = SHIP.intro;
  if (I.step === 'manifest') { SHIP.time.day = INTRO_START.day; SHIP.time.min = INTRO_START.min; if (typeof ternRamp === 'function') ternRamp(false, 0); introManifest(); return; }
  const now = Math.floor(shipNow());
  if (now !== INTRO_UI.min) {
    INTRO_UI.min = now;
    const done = Object.keys(I.done).length;
    introAdvance(now, { deck: deckDef.num, tile: player.here() });
    // a meeting step you've just reached plays its script (walking out of the room closes it; its gist comes by Mail)
    for (const id of Object.keys(I.done).slice(done)) { const st = introStepById(id); if (st && st.meeting && st.checkpoint && !I.missed.includes(id)) INTRO_UI.meet.push(st); }   // the evening's (the week's are introWeekMeetings')
    // waiting while another dialogue is open; if you've left its room by then, the gist comes by Mail instead
    for (const st of INTRO_UI.meet.slice()) {
      if (typeof dialogueShow !== 'function') { INTRO_UI.meet.length = 0; break; }
      const cp = st.checkpoint, room = new RegExp('^' + cp.room.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '$'), m = { id: 'intro-' + st.id, who: INTRO_MEETINGS[st.meeting].cast.filter(w => !/:/.test(w)), where: { deck: cp.deck, room }, at: now };
      if (!inMeeting(m)) { INTRO_UI.meet.splice(INTRO_UI.meet.indexOf(st), 1); if (typeof meetingGist === 'function') meetingGist(st.meeting); if (st.id === 'chief') I.done['chief:end'] = null; if (st.id === 'table' && I.done['table:end'] === undefined) I.done['table:end'] = now; continue; }
      if (DIALOGUE || INTRO_UI.tour.some(q => q.core.length)) break;   // after the tour's last core lines
      if (st.id === 'chief' && !introCalderIn() && now < (I.done.chief !== undefined ? I.done.chief : now) + 10) break;   // she's still on her way over
      INTRO_UI.meet.splice(INTRO_UI.meet.indexOf(st), 1); dialogueShow(introScriptHere(st.meeting, m, st.who), m);
      if (st.id === 'table') INTRO_UI.tableD = DIALOGUE;   // its last line sends the Chief over
      if (st.id === 'chief') { I.done['chief:met'] = now; INTRO_UI.chiefD = DIALOGUE; }   // the Chief's welcome: the goodnight waits for it (0.42.27)
    }
  }
  if (INTRO_UI.chiefD && DIALOGUE !== INTRO_UI.chiefD) { const D = INTRO_UI.chiefD; INTRO_UI.chiefD = null; I.done['chief:end'] = D.i >= D.queue.length ? Math.floor(shipNow()) : null; }   // all her lines, or walked away (null: day 0's minutes are negative)
  if (now === INTRO_UI.min) { introWeekMeetings(now); introMoments(now); introSeekMail(now); introSowTick(now); }
  // the Chief comes over to your table for her step (section 10's crewComeTo, live only, so again after a reload)
  // (0.42.64, the user: "the Chief used to walk up after you were sat"): she has her dinner at the far table (the step's
  // `away`) and comes over once the dinner chat with Torres is on its last line ("Look who's coming over") or over,
  // or the chat never happened; her own welcome waits until she's sat at your table (introCalderIn), ten minutes at most
  if (INTRO_UI.tableD && DIALOGUE !== INTRO_UI.tableD) { INTRO_UI.tableD = null; if (I.done['table:end'] === undefined) I.done['table:end'] = now; }
  const chat = INTRO_UI.tableD && DIALOGUE === INTRO_UI.tableD && DIALOGUE.i >= DIALOGUE.queue.length - 1;
  const calderGo = I.done['table:end'] !== undefined || chat || I.missed.includes('table') || I.step === 'free' && I.done['chief:met'] !== undefined || I.done.chief !== undefined && now >= I.done.chief + 10;   // (the last: a reload mid-chat, or a chat that never came)
  if ((I.step === 'chief' || I.step === 'free') && calderGo && !INTRO_UI.calder && introSeat('calder') && typeof crewComeTo === 'function' && deckDef.num === 3) {
    INTRO_UI.calder = true; crewComeTo('calder', introSeat('calder'), null, { until: introAbs(0, 19 * 60) });
  }
  // his lines for a step once its time has come and no meeting is on ("I'm on Four if you need me" waits for 19:00)
  const cur = introStepById(I.step);
  if (I.step !== INTRO_UI.step && !DIALOGUE && (!cur || Math.floor(shipNow()) >= introAbs(cur.day, cur.at))) { INTRO_UI.step = I.step; }   // ('free' said walk.free here until 0.42.27: his goodnight, introNightTick, says it now)
  introTourTick(); introNightTick(); introBedTick(); introTernTick(); introBeatTick(); introFollowTick(); introArrowTick();
  // the goal arrow points at him while he's leading you (section 15b's setGoal), and is cleared when he lets you go
  const st = introStep(), lead = !DIALOGUE && introEscorting(st) && !INTRO_UI.arrow;   // while he's yours, not over a meeting (nor over a first-time arrow: the servery after the Chief's "Eat something")
  if (lead) {
    const a = introWalker(), d = st.checkpoint.deck;
    const g = a && deckDef.num === d ? { deck: d, at: cellAt(a.x, a.z), label: 'Zeke Torres' } : { deck: d, at: st.checkpoint.tile, label: 'Zeke Torres' };
    const key = g.deck + ':' + g.at, mine = typeof IX_GOAL !== 'undefined' && IX_GOAL && IX_GOAL.label === g.label;   // only when he moves, or someone else's arrow took over
    if ((key !== INTRO_UI.goalKey || !mine) && typeof setGoal === 'function') { setGoal(g); INTRO_UI.goalKey = key; } INTRO_UI.goal = true;
    if (a && Math.hypot(a.x - player.obj.position.x, a.z - player.obj.position.z) > 6 && simNow() - INTRO_UI.callAt > 15000 && simNow() >= INTRO_UI.next && typeof bubbleSay === 'function') {
      INTRO_UI.callAt = simNow(); bubbleSay(a.h, (introLines('call') || [])[0], 3.5); INTRO_UI.next = simNow() + INTRO_TOUR_GAP;   // never over a tour line
    }
  } else if (INTRO_UI.goal) { INTRO_UI.goal = false; INTRO_UI.goalKey = ''; if (typeof clearGoal === 'function' && !INTRO_UI.arrow) clearGoal(); }
}

// =====================================================================
// 21b. CLOTHES (onboarding engineer 4, 0.42.40+; plans/plan-0607.html "Clothes and laundry", the user's ask)
// Change every morning at your wardrobe (the locker by your bunk in Bunk 1): one minute. Not changed by 10:00 and you're
// "in yesterday's clothes" until 22:00: hygiene drains faster (CLOTHES_DRAIN, through section 15's playerFx) and the
// device's status says so. Nothing worse. Out of clean clothes, the wardrobe gives you your laundry hamper: carry it to a
// free washer in the Deck 4 laundry (WASH_MINS, you can leave; a toast says when it's done), take it out, and put it
// away at the wardrobe: CLOTHES_FULL clean outfits again. No laundry duty.
// A new arrival comes with one spare outfit (changed into on Day 1); Zeke warns you at dinner on Day 1, so the first
// laundry is Day 2, and after it your full kit has come up from stores. A game started on Monday (or an older save)
// has the full kit. The hamper is not in SHIP.player.carry (parts, the kit bag, gifts): it's SHIP.clothes.hamper, and
// section 15/15b's hooks ask hamperHeld() (the holding pose, Put down) and clothesFloorTap(point) (the wardrobe and the
// set-down hamper). Off at test URLs (?nosave) unless ?clothes is in the URL, so the regressions stay identical.
//   SHIP.clothes = { clean, changed (the day you last changed; -1 never), kit, hamper, said: { beatId: shipMin }, told }
//   hamper: null | { state: 'dirty' | 'washing' | 'clean', at: 'hands' | 'floor' | 'washer', deck, x, z, washer, until, done }
// Nothing here calls R(); the set-down hamper's look is made the first time it's needed (existing materials only).
// =====================================================================
const CLOTHES_FULL = 5, CLOTHES_SPARE = 1, CLOTHES_LATE = 10 * 60, CLOTHES_NIGHT = 22 * 60, CLOTHES_DRAIN = 1.6, WASH_MINS = 30;
const HAMPER_NEAR = .6, WARDROBE_NEAR = .6;
let CLOTHES_ON = !NOSAVE || URL_FLAGS.has('clothes');
const clothesBlank = full => ({ clean: full ? CLOTHES_FULL : CLOTHES_SPARE, changed: full ? -1 : 0, kit: !!full, hamper: null, said: {}, told: -1, grime: 0 });
const grimeRound = g => Math.round(Math.max(0, Math.min(1, +g || 0)) * 100) / 100;   // 0-1, two decimals (0.42.46)
function clothesLoad(s) {
  const x = s && s.clothes, C = clothesBlank(true);
  if (!x || typeof x !== 'object') { C.changed = SHIP.time.day; return C; }   // an older save: the full kit, and already changed today
  if (Number.isInteger(x.clean) && x.clean >= 0) C.clean = Math.min(CLOTHES_FULL, x.clean);
  if (Number.isInteger(x.changed)) C.changed = x.changed;
  if (Number.isInteger(x.told)) C.told = x.told;
  C.kit = x.kit !== false;
  C.grime = isFinite(x.grime) ? grimeRound(x.grime) : 0;   // an older save: clean (0.42.46)
  if (x.said && typeof x.said === 'object') for (const k in x.said) if (isFinite(x.said[k])) C.said[k] = +x.said[k];
  const h = x.hamper;
  if (h && ['dirty', 'washing', 'clean'].includes(h.state) && ['hands', 'floor', 'washer'].includes(h.at)) {
    const ok = h.at === 'hands' || h.at === 'floor' && DECKS[h.deck] && isFinite(h.x) && isFinite(h.z) || h.at === 'washer' && typeof h.washer === 'string' && isFinite(h.until);
    if (ok) C.hamper = { state: h.state, at: h.at, deck: +h.deck || 0, x: +h.x || 0, z: +h.z || 0, washer: h.washer || null, until: +h.until || 0, done: !!h.done };
  }
  return C;
}
SHIP.clothes = clothesLoad(SAVED);
SAVE_EXTRA.push(s => { s.clothes = JSON.parse(JSON.stringify(SHIP.clothes)); s.clothes.grime = grimeRound(SHIP.clothes.grime); });
onSim('newGame', n => { SHIP.clothes = clothesBlank(!n.arrival); });   // by shuttle: one spare outfit; on Monday: the full kit
onSim('job', n => { if (n.step === 'turnin' && SHIP.time.day === 1 && SHIP.clothes.said['d1:turnin'] === undefined) SHIP.clothes.said['d1:turnin'] = Math.floor(shipNow()); });   // Day 1's first turn-in (d1-better)   // by shuttle: one spare outfit; on Monday: the full kit
const hamperHeld = () => CLOTHES_ON && !!SHIP.clothes.hamper && SHIP.clothes.hamper.at === 'hands';
const clothesYesterday = () => CLOTHES_ON && SHIP.clothes.changed < SHIP.time.day && SHIP.time.min >= CLOTHES_LATE && SHIP.time.min < CLOTHES_NIGHT;
// your uniform's grime (0.42.46, Pillar 5's m2 "uniform" page, for the mechanic seat's 24b): SHIP.clothes.grime 0-1 (saved, two
// decimals). Oily jobs add to it through clothesGrime(add); a change at your wardrobe while grubby always takes a clean
// outfit (even if you've changed today) and sets it to 0; a shower leaves it. uniformState(): 'grubby' (grime >= GRIME_GRUBBY),
// else 'yesterday' (clothesYesterday), else 'clean'. Grubby drains hygiene as yesterday's clothes do (one CLOTHES_DRAIN,
// never both). simNote('uniform', { state }) on each change (uniformWatch). Off at test URLs: 'clean', and clothesGrime is null.
const GRIME_GRUBBY = .6;
const uniformState = () => !CLOTHES_ON ? 'clean' : SHIP.clothes.grime >= GRIME_GRUBBY ? 'grubby' : clothesYesterday() ? 'yesterday' : 'clean';
function clothesGrime(add) {
  if (!CLOTHES_ON || !isFinite(add)) return null;
  SHIP.clothes.grime = grimeRound(SHIP.clothes.grime + add); uniformWatch();
  return SHIP.clothes.grime;
}
let UNIFORM_SEEN = null;
function uniformWatch() { const u = uniformState(); if (u !== UNIFORM_SEEN) { const was = UNIFORM_SEEN; UNIFORM_SEEN = u; if (was !== null) simNote('uniform', { state: u }); } }
function clothesFx(fx) {                                 // section 15's playerFx: hygiene drains faster in yesterday's clothes, or a grubby uniform
  const u = uniformState(); if (u === 'clean') return fx;
  return { ...fx, drain: { ...(fx.drain || {}), hygiene: fxD(fx, 'hygiene') * CLOTHES_DRAIN }, notes: [{ text: u === 'grubby' ? 'Your uniform is grubby' : 'In yesterday\'s clothes' }, ...(fx.notes || [])] };
}
Object.assign(PLAYER_ACTS, { clothes: { mins: 1, pose: 'browse', title: 'Changing' } });
const clothesHandsFull = () => { const P = SHIP.player; return P.carry.length > 0 || !!P.tray || !!P.cart || hamperHeld(); };
// the head writer's texts (content/banks/clothes.lines: LINES[kind], variant k, {n} and {time} filled), else the stand-in
function clothesText(kind, fill = {}, or = '', k = SHIP.time.day) {
  const L = typeof LINES !== 'undefined' && LINES[kind], e = Array.isArray(L) && L.length ? L[((k % L.length) + L.length) % L.length] : null;
  return e && typeof e.text === 'string' ? e.text.replace(/\{(n|time)\}/g, (m, x) => fill[x] !== undefined ? fill[x] : m) : or;
}
const clothesLeft = n => n === 0 ? 'no clean outfits left' : n === 1 ? 'one clean outfit left' : n + ' clean outfits left';
// your wardrobe: the deck architect's (DECKS[4].wardrobes[bed]: Bunk 1's west locker, its place 4-B1-4-wardrobe in
// front of it, 0.38.24): the bunk-room locker ('cleanUniforms' spot) nearest that place; before that, the room's west one
function clothesWardrobe() {
  if (typeof deckDef === 'undefined' || typeof PLACE_OF === 'undefined') return null;
  const bed = PLACE_OF.get(playerBed()); if (!bed || deckDef.num !== deckOf(bed.id)) return null;
  const W = DECKS[deckDef.num].wardrobes && DECKS[deckDef.num].wardrobes[bed.id], sp = W && PLACE_OF.has(W.place) ? placeSpot(W.place) : null;
  const lk = SPOTS.filter(s => s.tag === 'cleanUniforms' && s.room === bed.room);
  if (sp) lk.sort((m, n) => Math.hypot(m.x - sp.x, m.z - sp.z) - Math.hypot(n.x - sp.x, n.z - sp.z)); else lk.sort((m, n) => m.x - n.x);
  return lk[0] ? { ...lk[0], tile: W && PLACE_OF.has(W.place) ? PLACE_OF.get(W.place).at : null } : null;
}
let CLOTHES_TILE = null;                                 // your wardrobe's tile, from the last time Deck 4 was built (else your bunk's)
const clothesWardrobeTile = () => { const w = clothesWardrobe(); if (w) CLOTHES_TILE = w.tile || cellAt(w.x, w.z); const bed = (DECKS[4].places || []).find(p => p.id === playerBed()); return CLOTHES_TILE || (bed ? bed.at : [8, 1]); };
function clothesRayNear(x, z, top) {                     // how near the tap's line of sight passes to (x, z), from the floor to top
  if (typeof ray === 'undefined') return Infinity;
  const o = ray.ray.origin, d = ray.ray.direction; let best = Infinity;
  for (let y = 0; y <= top; y += .1) { const k = (y - o.y) / d.y; if (k > 0) best = Math.min(best, Math.hypot(o.x + d.x * k - x, o.z + d.z * k - z)); }
  return best;
}
// a tap that reached the floor (section 15's playerFloorTap; the bunk lockers have no words of their own): the wardrobe or the set-down hamper
function clothesFloorTap(point) {
  if (!CLOTHES_ON) return false;
  const h = SHIP.clothes.hamper;
  if (h && h.at === 'floor' && h.deck === deckDef.num && Math.min(Math.hypot(point.x - h.x, point.z - h.z), clothesRayNear(h.x, h.z, .5)) <= HAMPER_NEAR) {
    approach(new THREE.Vector3(h.x, 0, h.z), 0, 0, () => hamperUp(false));
    return true;
  }
  const w = clothesWardrobe(); if (!w) return false;
  if (Math.min(Math.hypot(point.x - w.x, point.z - w.z), clothesRayNear(w.x, w.z, 2)) > WARDROBE_NEAR) return false;
  approach(new THREE.Vector3(w.x, 0, w.z), w.front, .6, wardrobeUse);
  return true;
}
// a tap on a thing with words (section 15's PLAYER_TAPS): a wardrobe (the deck architect's, when it has a title), or a washer with your laundry in play
PLAYER_TAPS.push((it, at) => {
  if (!CLOTHES_ON || typeof deckDef === 'undefined') return false;
  if (it.wardrobe === playerBed() || !it.wardrobe && /wardrobe/i.test(it.t)) {   // yours (the deck architect's tag), or a titled wardrobe right at it (reviewer's LOW: not any locker)
    const w = clothesWardrobe(); if (!w || it.wardrobe !== playerBed() && Math.hypot(at.x - w.x, at.z - w.z) > .6) return false;
    approach(at.clone(), it.front, it.depth, wardrobeUse); return true;
  }
  if (!/^washer\b/i.test(it.t) || deckDef.num !== 4) return false;
  const h = SHIP.clothes.hamper; if (!h || !(h.at === 'hands' && h.state === 'dirty' || h.at === 'washer')) return false;
  const m = washerNear(at); if (!m) return false;
  approach(at.clone(), it.front, it.depth, () => washerUse(m, it.t));
  return true;
});
function wardrobeUse() {
  const C = SHIP.clothes, h = C.hamper, today = SHIP.time.day;
  if (h && h.at === 'hands' && h.state === 'clean') {   // put the clean washing away (and change, if you haven't today)
    const first = !C.kit; C.kit = true; C.clean = CLOTHES_FULL; C.hamper = null; clothesGoal(null);
    let say = first ? clothesText('laundry.kit', {}, 'Your full kit has come up from stores while you were out: you put it away with your clean washing. Five outfits.') : clothesText('laundry.away', {}, 'You put your clean washing away. Five outfits.');
    if (C.changed < today || C.grime >= GRIME_GRUBBY) { C.clean--; C.changed = today; C.grime = 0; uniformWatch(); simAct('clothes'); say += ' You change into a fresh set. ' + clothesText('clothes.left', { n: C.clean }, clothesLeft(C.clean)[0].toUpperCase() + clothesLeft(C.clean).slice(1) + '.'); }
    actStart('clothes', null, { title: 'Wardrobe', after: say });
    return;
  }
  if (h && h.at === 'hands') { toast('Wardrobe', 'Your hamper\'s full of dirty washing. Take it to a free washer in the laundry, past the washrooms in the junior wing.'); clothesGoal('washer'); return; }
  if (h && h.at === 'washer') { toast('Wardrobe', 'Your washing is in ' + washerName(h.washer) + ' in the laundry' + (h.done || shipNow() >= h.until ? ': it\'s done, take it out.' : ', done at ' + hhmm(h.until) + '.')); return; }
  if (h && h.at === 'floor') { toast('Wardrobe', 'Your laundry hamper is where you set it down' + (h.deck !== deckDef.num ? ', on ' + deckIn(h.deck) : '') + '. Pick it up again when you\'re ready.'); return; }
  if (C.clean > 0 && C.changed >= today && C.grime < GRIME_GRUBBY) { toast('Wardrobe', 'You\'re in clean clothes today. ' + clothesLeft(C.clean)[0].toUpperCase() + clothesLeft(C.clean).slice(1) + ' in here.'); return; }
  if (C.clean > 0) {                                     // (grubby: always, even if you changed today)
    C.clean--; C.changed = today; C.grime = 0; uniformWatch(); simAct('clothes');
    const fresh = clothesText('clothes.changed', {}, 'You change into clean clothes.'), spare = !C.kit && !C.clean;
    actStart('clothes', null, { title: 'Wardrobe', after: fresh + ' ' + (spare ? clothesText('clothes.spare', {}, 'Your one spare outfit. The rest of your kit comes up from stores.')
      : C.clean ? clothesText('clothes.left', { n: C.clean }, clothesLeft(C.clean)[0].toUpperCase() + clothesLeft(C.clean).slice(1) + '.') : 'That was your last clean set.') + (C.clean ? '' : ' Do your laundry before tomorrow: tap the wardrobe again for your hamper.') });
    return;
  }
  if (clothesHandsFull()) { toast('Wardrobe', 'No clean clothes left. Your hamper\'s in here, but your hands are full: put things down first.'); return; }
  C.hamper = { state: 'dirty', at: 'hands', deck: 0, x: 0, z: 0, washer: null, until: 0, done: false };
  toast('Wardrobe', clothesText('clothes.empty', {}, 'No clean clothes left. Take the hamper to the laundry on Deck 4.') + ' You take your laundry hamper.');
  if (typeof ixTip === 'function') ixTip('laundry', clothesText('tip.laundry', {}, 'Laundry: carry your hamper to a free washer in the Deck 4 laundry and tap it. It runs half an hour, and you can leave. Take the clean washing out and put it away at your wardrobe.'));
  clothesGoal('washer');
}
// the washers (section 17's machines, kind 'washer', in the Deck 4 laundry): free, busy (anyone's run, MACH_RUN) or broken
const washerList = () => typeof machineList === 'function' ? machineList().filter(m => m.kind === 'washer' && m.deck === 4 && m.at) : [];
const washerName = id => 'Washer ' + ((String(id).match(/(\d+)$/) || [])[1] || '');
const washerBusyUntil = id => { const mine = SHIP.clothes.hamper, r = typeof MACH_RUN !== 'undefined' && MACH_RUN[id] || 0; return Math.max(r, mine && mine.at === 'washer' && mine.washer === id ? mine.until : 0); };
const washerBroken = id => { try { const st = machinesNow()[id]; return !!st && st.state === 'broken'; } catch (e) { return false; } };
function washerNear(at) {
  return washerList().map(m => [m, cellPos(...m.at)]).filter(([, c]) => Math.hypot(c.x - at.x, c.z - at.z) < 1.6)
    .sort((a, b) => Math.hypot(a[1].x - at.x, a[1].z - at.z) - Math.hypot(b[1].x - at.x, b[1].z - at.z)).map(x => x[0])[0] || null;
}
function washerUse(m, title) {
  const C = SHIP.clothes, h = C.hamper, now = shipNow(); if (!h) return;
  if (h.at === 'washer') {                               // your washing: take it out when it's done
    if (h.washer !== m.id) { toast(title, 'Your washing is in ' + washerName(h.washer) + '.'); return; }
    if (now < h.until) { toast(title, 'Your washing is still going: done at ' + hhmm(h.until) + '.'); return; }
    if (clothesHandsFull()) { toast(title, 'Your washing\'s done, but your hands are full: put things down first.'); return; }
    C.hamper = { state: 'clean', at: 'hands', deck: 0, x: 0, z: 0, washer: null, until: 0, done: false };
    toast(title, 'You take your clean washing out. ' + clothesText('laundry.fold', {}, 'Fold it at the folding table if you like.') + ' Then put it away at your wardrobe in Bunk 1.');
    clothesGoal('wardrobe');
    return;
  }
  const free = id => washerBusyUntil(id) <= now && !washerBroken(id);
  if (!free(m.id)) {
    const others = washerList().filter(o => free(o.id));
    if (others.length) { toast(title, (washerBroken(m.id) ? 'This one\'s broken.' : 'This one\'s going.') + ' ' + washerName(others[0].id) + ' is free.'); return; }
    const first = washerList().filter(o => !washerBroken(o.id)).sort((a, b) => washerBusyUntil(a.id) - washerBusyUntil(b.id))[0];
    toast(title, first ? clothesText('laundry.busy', { n: washerName(first.id).replace('Washer ', ''), time: hhmm(washerBusyUntil(first.id)) }, 'All the washers are going. ' + washerName(first.id) + ' finishes first, at ' + hhmm(washerBusyUntil(first.id)) + '.') : 'Every washer is broken. Works will be on it: try later.');
    return;
  }
  let r = null; try { r = machineUse(m.id, 'player'); } catch (e) { r = null; }
  if (r && !r.ran) { toast(title, r.text || 'It won\'t start.'); return; }
  C.hamper = { state: 'washing', at: 'washer', deck: 4, x: 0, z: 0, washer: m.id, until: now + WASH_MINS, done: false };
  simAct('laundry'); clothesGoal(null);
  toast(title, 'You load your washing. ' + clothesText('laundry.running', { time: hhmm(now + WASH_MINS) }, 'Done at ' + hhmm(now + WASH_MINS) + '. You don\'t have to wait; your device will tell you.'));
}
function hamperUp(quiet) {                               // pick the set-down hamper up again
  const h = SHIP.clothes.hamper; if (!h || h.at !== 'floor') return false;
  if (clothesHandsFull()) { toast('Laundry hamper', 'Your hands are full: put things down first.'); return false; }
  h.at = 'hands'; h.deck = 0;
  if (!quiet) toast('Laundry hamper', 'You pick your hamper up again.');
  return true;
}
function hamperPut() {                                   // section 15b's Put down: set the hamper down where you stand
  if (!hamperHeld()) return '';
  const h = SHIP.clothes.hamper, p = player.obj.position, f = player.face || 0;
  h.at = 'floor'; h.deck = deckDef.num; h.x = p.x + Math.sin(f) * .45; h.z = p.z + Math.cos(f) * .45;
  return 'You set your laundry hamper down. Tap it to pick it up again.';
}
// the arrow: to a free washer (or the laundry) with the dirty washing, back to your wardrobe with the clean
let CLOTHES_GOAL = null;
function clothesGoal(to) {
  if (typeof setGoal !== 'function') return;
  if (!to) { if (CLOTHES_GOAL && typeof IX_GOAL !== 'undefined' && IX_GOAL && IX_GOAL.label === CLOTHES_GOAL) clearGoal(); CLOTHES_GOAL = null; return; }
  const w = washerList().find(m => washerBusyUntil(m.id) <= shipNow() && !washerBroken(m.id)) || washerList()[0];
  const g = to === 'washer' ? { deck: 4, at: w ? (w.panel || w.at) : [13, 18], label: 'Laundry' } : { deck: 4, at: clothesWardrobeTile(), label: 'Your wardrobe' };
  setGoal(g); CLOTHES_GOAL = g.label;
}
// Zeke's Day 1 and Day 2 (plan-0607 "Clothes" and "Team and time"; onboarding 3's handover): said like section 21's
// beats, once, in the window, when you're in the room with him (or within INTRO_BEAT_NEAR for where: 'seek'). Lines:
// the head writer's week-1 keys on torres-zeke (content/keys-0607.md), each `keys` entry a numbered flag prefix
// (walk.dinner.eve.1, .2, ...) or an exact flag, in order; the plan's words as stand-ins while content is missing.
// when(C): still wanted; seek: section 20's socialSeekAsk brings him to you in the window; then: after the last line.
const CLOTHES_BEATS = [
  // the cabin (the user on 0.63.1, 0.42.48): after the bunk meeting Zeke shows you your wardrobe ("this is where you get clean
  // clothes"), and the rest of his bunk talk comes as Mail from him (the meeting tells you to open it; clothesCabinMail)
  { id: 'd0-wardrobe', day: 0, at: 17 * 60 + 40, till: 19 * 60, who: INTRO_ESCORT, where: { deck: 4, room: 'Bunk 1' }, when: () => SHIP.intro.done.bunk !== undefined,
    keys: () => ['walk.cabin.wardrobe'], lines: () => ['That\'s your wardrobe, by the door. It\'s where you get clean clothes.'], first: () => clothesCabinMail() },
  { id: 'd1-dinner-zeke', day: 1, at: 18 * 60, till: 20 * 60, who: INTRO_ESCORT, where: { deck: 3, room: 'Mess hall' }, when: () => true, settle: 'clothes',   // settle: the Settling-in item it teaches (as INTRO_WEEK's; intro_check reads both)
    keys: C => ['walk.dinner.eve', 'walk.eve.choose', ...(C.kit ? [] : [['beat.d1-clothes', 'walk.dinner.laundry']])],   // walk.eve.choose (0.42.48): you can't do every tradition, you choose
    lines: C => ['Evenings are yours. Most of us have a thing. I knit, don\'t laugh. Pell reads. Find yours.',
      ...(C.kit ? [] : ['One change of clothes? The laundry\'s past the washrooms in the junior wing.', 'Do it tomorrow after shift, or you\'ll be wearing that on Wednesday.'])] },
  // Day 1's training (the user on 0.63.1, 0.42.48): when the Monday briefing is over, Zeke's opener (walk.train.open: "training
  // day, I'm with you all day"; sets SHIP.intro.done['d1-opener'] for O5's clock arrow); after your first job's turn-in, "jobs
  // get better as you go" (walk.train.better)
  { id: 'd1-opener', day: 1, at: (INTRO_WEEK.find(b => b.id === 'd1-briefing') || { until: 9 * 60 }).until, till: 12 * 60, who: INTRO_ESCORT, where: 'seek', when: () => true,
    keys: () => ['walk.train.open'], lines: () => ['Training day today. I\'m with you all day to help.'], then: () => { SHIP.intro.done['d1-opener'] = Math.floor(shipNow()); } },
  { id: 'd1-better', day: 1, at: 8 * 60, till: 17 * 60, who: INTRO_ESCORT, where: 'seek', when: C => C.said['d1:turnin'] !== undefined,
    keys: () => ['walk.train.better'], lines: () => ['Don\'t worry. The jobs get better as you go.'] },
  { id: 'd2-laundry', day: 2, at: 16 * 60 + 45, till: 18 * 60, who: INTRO_ESCORT, where: 'seek', when: C => !C.kit && !(C.hamper && C.hamper.state !== 'dirty'),
    keys: () => [['beat.d2-laundry', 'walk.laundry']], lines: () => ['Laundry today, remember? After shift\'s quietest.'] },
  { id: 'd2-knit', day: 2, at: 18 * 60 + 30, till: 21 * 60, who: INTRO_ESCORT, where: 'seek', seek: true, settle: 'hobby', when: () => typeof hobbyHas !== 'function' || !hobbyHas('knit'),
    keys: () => ['walk.knit'], lines: () => ['Want to learn to knit? I\'ve got spare needles.'],
    then: () => { if (typeof hobbyGive === 'function' && hobbyGive('knit')) toast('Knitting', 'Zeke gives you a pair of spare needles and some wool. Knitting is one of your hobbies now: sit down and tap Hobby.'); } },
  // your first delivery (plan-0607 "Stores and the lift": Day 3, your first Wednesday, Yara Esposito mentions it; offered,
  // never forced): while section 17's Wednesday delivery is on the board and nobody has it (held for you till 14:00),
  // she comes and finds you and says the writers' stores.delivery card lines (gate flag delivery.first)
  { id: 'd3-delivery', day: 3, at: 10 * 60, till: 13 * 60 + 30, who: 'esposito-yara', where: 'seek', seek: true, when: () => !!clothesDelivery(),
    own: () => clothesVoice('esposito-yara', 'stores.delivery', 'delivery.first'),
    lines: () => ['Wednesday. Delivery day. There\'s a stack of crates in the hold.', 'Fancy unloading it? Cart, crates, shelves. It\'s on the board.', 'No pressure. If it\'s still there at two, someone else gets it.'],
    first: () => introFlagSet('delivery.first'),
    then: () => { if (clothesDelivery()) toast('The Wednesday delivery', 'It\'s on the job board in the Works bay, Deck 5, until 14:00: take it there if you\'d like to. A hover cart from the Cart bay, the crates in the cargo hold, then tap any shelf in main storage.'); } },
];
// Zeke's Mail after the bunk meeting (once, saved in SHIP.clothes.said): the writers' text mail.zeke.cabin ("Subject | body"),
// else the stand-in; sent when his wardrobe line starts, or by the frame loop once the bunk step is done and you've left Bunk 1
function clothesCabinMail() {
  const C = SHIP.clothes; if (C.said.cabinMail !== undefined || typeof mailSend !== 'function') return;
  C.said.cabinMail = Math.floor(shipNow());
  const t = clothesText('mail.zeke.cabin', {}, 'Settling in | The rest of what I meant to say in the bunk room. Your bed\'s the upper one, middle of the three. Your wardrobe\'s by the door: clean clothes there every morning, and do your laundry when they run out. Washrooms at both ends of the wing. Dinner\'s on Three. Tomorrow\'s briefing is in the Works bay on Deck 5: the time\'s on your device. Sleep well. Z.'), i = t.indexOf(' | ');
  mailSend({ at: shipNow(), from: 'Zeke Torres', subject: i < 0 ? 'Settling in' : t.slice(0, i), body: i < 0 ? t : t.slice(i + 3) });
}
// this week's delivery job while it's still open and nobody has it (section 17: a stores restock found today), or null
const clothesDelivery = () => (SHIP.jobs || []).find(j => j.kind === 'restock' && j.cargo === 'stores' && j.status !== 'done' && !j.claimedBy && Math.floor(j.found / 1440) + 1 === SHIP.time.day && j.found <= shipNow()) || null;
// one person's lines of one kind under a flag (the voice cards: VOICE[id].lines[kind], entries with that flag), filled, or null
function clothesVoice(id, kind, flagKey) {
  try {
    const v = typeof VOICE !== 'undefined' && VOICE[id], L = (v && v.lines && v.lines[kind] || []).filter(e => e.flag === flagKey); if (!L.length) return null;
    const who = typeof linesWho === 'function' ? linesWho(id) : null;
    return L.map(e => who && typeof linesFill === 'function' ? linesFill(e.text, who, { t: shipNow(), flags: { [flagKey]: true } }) : e.text).filter(Boolean);
  } catch (e) { return null; }
}
function clothesBeatLines(b, C) {                        // the writers' lines for a beat, in order, or the stand-ins
  const out = [];
  const said = k => {                                    // one key: its exact lines, else k.1, k.2, ... in order
    const W = f => typeof introWriterLines === 'function' ? introWriterLines(f, b.who) : null, got = W(k) || [];
    for (let n = 1; !got.length || n <= 12; n++) { const l = W(k + '.' + n); if (!l) break; got.push(...l); }
    return got;
  };
  for (const k of (b.keys ? b.keys(C) : [])) { for (const alt of [].concat(k)) { const l = said(alt); if (l.length) { out.push(...l); break; } } }   // an array: the first name that has lines
  const own = b.own && b.own(C); if (own && own.length) return own.slice();
  return out.length ? out : b.lines(C).slice();
}
let CLOTHES_BEAT = null;
function clothesBeatTick() {
  if (typeof introOn !== 'function' || !introOn() || typeof DECK_CREW === 'undefined' || typeof bubbleSay !== 'function') return;
  const C = SHIP.clothes, U = INTRO_UI, now = shipNow(), t = simNow(), crew = id => DECK_CREW.find(x => x.p && x.p.id === id);
  if (CLOTHES_BEAT) {
    const B = CLOTHES_BEAT, a = crew(B.b.who);
    if (!introBeatHere(B.b, a)) CLOTHES_BEAT = null;
    else if ((a.talking = Math.max(a.talking || 0, 1)) && !DIALOGUE && t >= U.next) {
      bubbleSay(a.h, B.lines.shift(), 4.5); U.next = t + INTRO_TOUR_GAP;
      if (!B.lines.length) { CLOTHES_BEAT = null; if (B.b.then) B.b.then(C); }
    }
    return;
  }
  if (DIALOGUE || U.beat) return;
  for (const b of CLOTHES_BEATS) {
    if (C.said[b.id] !== undefined || !b.when(C)) continue;
    const from = introAbs(b.day, b.at), until = introAbs(b.day, b.till);
    if (b.seek && now >= from && now < until && typeof socialSeekAsk === 'function') socialSeekAsk(b.who, { from, until, why: 'intro:' + b.id });
    if (now < from || now >= until || !introBeatHere(b, crew(b.who))) continue;
    C.said[b.id] = Math.floor(now); if (b.first) b.first(C); CLOTHES_BEAT = { b, lines: clothesBeatLines(b, C) }; return;
  }
  clothesCrewTick(C, now, crew);
}
// the crew at work (Days 1 and 2, the systems engineer's showJob(day): Bea on a vent on Day 1, tools carried on Day 2):
// while Zeke is with you and the one doing it is in view (on your deck, within CREW_SEE m), he points them out once
// (walk.crew.vent / walk.crew.delivery)
const CREW_SEE = 9, CREW_SAY = { vent: 'walk.crew.vent', tools: 'walk.crew.delivery', delivery: 'walk.crew.delivery' };
function clothesCrewTick(C, now, crew) {
  if (typeof showJob !== 'function' || SHIP.time.day < 1 || SHIP.time.day > 2) return;
  let j = null; try { j = showJob(SHIP.time.day); } catch (e) { j = null; }
  const key = j && CREW_SAY[j.key]; if (!key || C.said['crew:' + j.key] !== undefined) return;
  const z = crew(INTRO_ESCORT), a = crew(j.who), p = player.obj.position;
  if (!z || !a || Math.hypot(z.x - p.x, z.z - p.z) > INTRO_BEAT_NEAR || Math.hypot(a.x - p.x, a.z - p.z) > CREW_SEE) return;
  const lines = typeof introWriterLines === 'function' && introWriterLines(key) || [j.key === 'vent' ? 'That\'s ' + a.p.name.split(' ')[0] + ' on the vent. You\'ll do those by Wednesday.' : 'Delivery coming through. We share the small jobs out.'];
  C.said['crew:' + j.key] = Math.floor(now);
  CLOTHES_BEAT = { b: { who: INTRO_ESCORT, where: 'seek' }, lines: lines.slice() };
}
// once a frame: the washing done, yesterday's clothes at 10:00, the set-down hamper's look, the beats
let HAMPER_LOOK = null, CLOTHES_STALE = null, CLOTHES_SCAN = 0;
function hamperLook() {                                  // a small laundry hamper on the floor, made once (no R())
  const g = new THREE.Group();
  box(.46, .4, .34, KM.hamper, 0, .21, 0, g);            // just off the floor: no coplanar faces
  box(.5, .04, .38, M.slateDark, 0, .42, 0, g);
  soft(KM.teal, -.08, .45, 0, .13, .05, .1, g); soft(KM.gold, .1, .45, .03, .12, .05, .09, g);
  g.visible = false; scene.add(g); return g;
}
function clothesFrame() {
  requestAnimationFrame(clothesFrame);
  if (!CLOTHES_ON || typeof deckDef === 'undefined' || !deckDef || typeof player === 'undefined') return;
  const C = SHIP.clothes, h = C.hamper, now = shipNow();
  if (SHIP.clothes.said.cabinMail === undefined && typeof introOn === 'function' && introOn() && SHIP.intro.done.bunk !== undefined && !(SHIP.intro.missed || []).includes('bunk') && deckDef.num !== 4) clothesCabinMail();   // left the wing without his wardrobe line: the Mail anyway
  uniformWatch();                                        // simNote('uniform') when it turns grubby, yesterday's or clean (10:00, 22:00, a change)
  if (h && h.at === 'washer' && !h.done && now >= h.until) { h.done = true; toast('Laundry', clothesText('laundry.done', {}, 'Your washing\'s done. Collect it from the laundry on Deck 4.') + ' It\'s in ' + washerName(h.washer) + '.'); }
  if (C.changed < SHIP.time.day && C.clean > 0 && SHIP.time.min >= 6 * 60 && SHIP.time.min < CLOTHES_LATE && deckDef.num === 4 && typeof ixTip === 'function' && !ACT)
    ixTip('clothes', clothesText('tip.clothes', {}, 'Fresh clothes every morning from your wardrobe, by the door in Bunk 1 (by 10:00 you\'re in yesterday\'s clothes). When they run out, do your laundry when you can.'));   // once (the device's tips)
  if (C.told !== SHIP.time.day && clothesYesterday()) {
    C.told = SHIP.time.day;
    toast('Yesterday\'s clothes', clothesText('clothes.stale', {}, 'You\'re in yesterday\'s clothes.') + (C.clean > 0 || h && h.state === 'clean' ? ' Change at your wardrobe in Bunk 1; till then you\'ll feel grubby sooner.' : ' And there are no clean ones left: your hamper\'s in your wardrobe. Do your laundry.'));
  }
  const stale = clothesYesterday();                     // the writers' clothes.remark lines are gated on this flag (crew notice)
  if (stale !== CLOTHES_STALE && typeof flagSet === 'function') { CLOTHES_STALE = stale; flagSet('clothes.stale', stale ? true : null); }
  const here = !!h && h.at === 'floor' && h.deck === deckDef.num;
  if (here && !HAMPER_LOOK) HAMPER_LOOK = hamperLook();
  if (HAMPER_LOOK) { HAMPER_LOOK.visible = here; if (here) HAMPER_LOOK.position.set(h.x, 0, h.z); }
  if (simNow() < CLOTHES_SCAN) return; CLOTHES_SCAN = simNow() + 250;   // the beats, the crew-at-work look-up and the remark scan: four times a second, not every frame (reviewer's LOW)
  clothesBeatTick();
  if (stale && C.said.remark !== SHIP.time.day) clothesRemark(C);
}
requestAnimationFrame(clothesFrame);
// someone notices (the plan: "people may remark on it"): once a day at most, the first crew member who passes within
// REMARK_NEAR m while you're in yesterday's clothes says one of the writers' clothes.remark lines (none: nobody does)
const REMARK_NEAR = 2.2;
function clothesRemark(C) {
  if (typeof DECK_CREW === 'undefined' || typeof bubbleSay !== 'function' || typeof DIALOGUE !== 'undefined' && DIALOGUE || CLOTHES_BEAT) return;
  const L = typeof LINES !== 'undefined' && LINES['clothes.remark']; if (!Array.isArray(L) || !L.length) return;
  const p = player.obj.position, a = DECK_CREW.find(x => x.p && x.p.id && x.h && x.p.id !== INTRO_ESCORT && Math.hypot(x.x - p.x, x.z - p.z) < REMARK_NEAR);
  if (!a) return;
  C.said.remark = SHIP.time.day;                         // the day of the last remark (one key, so the save stays small)
  const e = L[SHIP.time.day % L.length], who = typeof linesWho === 'function' ? linesWho(a.p.id) : null;
  const text = who && typeof linesFill === 'function' ? linesFill(e.text, who, { t: shipNow(), flags: { 'clothes.stale': true } }) : e.text;
  if (text) bubbleSay(a.h, text, 4);
}

