// =====================================================================
// 13. SHIP TIME & SAVE
// Sits here, after lighting and before the first deck is built (section 10):
// the clock drives the light, and the save decides where you wake.
// 18 ship hours take 30 real minutes (a whole day 40). SHIP.time is the ship's clock: day 1 is
// a Monday, min counts ship minutes since midnight. It only runs while the
// game is on screen; the ship doesn't run while the game is closed.
// The game saves itself in the browser (localStorage, one save per device):
// every ship hour, on every deck change, and when the page is hidden or
// closed. Every read and write is in try/catch: no storage means a fresh
// start each time. URL flags: ?nosave turns saving and loading off (the tests
// use it); ?debug shows the Night/Day button (skip to 21:40, sleep to 07:40).
// Nothing here calls R().
// =====================================================================
const GAME_BUILD = '0.64.2';                           // keep in step with the header's build line
// ---- the ship notes bus and the flag store (Pillar 4): how every section tells the others what happened ----
// simNote(kind, data) -> the note { kind, t (ship minute), ...data }: handed to every onSim(kind, fn) listener (and
//   onSim('*', fn) ones), each in try/catch, so one bad listener never stops the rest. Each note is also kept for two
//   ship days as a cue (simNotes(kind, since) -> those notes, newest last), saved with the game (save.notes).
//   data.t, when given, is when it happened (section 17 runs hours late, in a time jump); otherwise now.
//   A payload never has its own `kind` or a non-number `t` (the note's kind wins; a number t is when it happened).
//   Kinds (pillar4-plan, appendix): repair {who, machine, job (service | repair | overhaul), deck}, favour {who, from}, tradition {id, day, came, you},
//   gift {to, item}, apptKept / apptMissed {id, with}, introStep {step, who}, eventPhase {id, phase}, choice {script, k,
//   who}, jobAbandoned {machine, dept}, harvest, lateMeal, job {id, step, job}, need {key, low}; social: tierUp, moment, bond, invite.
// flag(key) -> its value (undefined when unset); flagSet(key, value = true) sets it; flagSet(key, null) clears it.
//   Flags are saved with the game (save.flags): 'met.calder', 'escort.torres', 'week1.d2' ... Values are plain JSON.
// Function declarations and lazily made state, so a section anywhere in the file may call these while it loads.
// Nothing here calls R(); a note never changes a plan (plans are pure), only what listeners do with it.
var SIM_ON = null, SIM_DEPTH = 0;
var SIM_CUE = 2880, SIM_RING = 200;                      // cues last two ship days; at most 200 kept (var: usable from sections 1-5 too)
function onSim(kind, fn) {
  if (typeof fn !== 'function') return () => {};
  const m = SIM_ON || (SIM_ON = new Map()); if (!m.has(kind)) m.set(kind, []); m.get(kind).push(fn);
  return () => { const l = m.get(kind), i = l ? l.indexOf(fn) : -1; if (i >= 0) l.splice(i, 1); };   // to stop listening
}
function simNote(kind, data) {
  const now = typeof SHIP !== 'undefined' && SHIP.time ? (SHIP.time.day - 1) * 1440 + SHIP.time.min : 0;
  const t = data && typeof data === 'object' && Number.isFinite(data.t) ? data.t : now;   // a sender may say when it happened (section 17's hours, run late)
  let note;                                              // a plain copy, so it always saves: an object that won't (a walker, a cycle) drops the note
  try { note = Object.assign(JSON.parse(JSON.stringify(data && typeof data === 'object' ? data : {})), { kind, t }); }
  catch (e) { if (typeof DEBUG !== 'undefined' && DEBUG) console.warn('simNote ' + kind + ': data is not plain JSON; note dropped'); return null; }
  if (typeof SHIP !== 'undefined') {
    const ring = SHIP.notes || (SHIP.notes = []);
    let i = ring.length; while (i > 0 && ring[i - 1].t > t) i--;   // kept in time order (an earlier hour's note goes before later ones)
    ring.splice(i, 0, note);
    while (ring.length > SIM_RING || (ring.length && ring[0].t < Math.max(now, t) - SIM_CUE)) ring.shift();
  }
  if (SIM_ON && SIM_DEPTH < 8) {                          // a listener may send notes of its own, a few deep at most
    SIM_DEPTH++;
    try { for (const fn of (SIM_ON.get(kind) || []).concat(SIM_ON.get('*') || [])) { try { fn(note); } catch (e) { /* that listener's problem */ } } }
    finally { SIM_DEPTH--; }
  }
  return note;
}
function simNotes(kind, since = -Infinity) {
  const ring = (typeof SHIP !== 'undefined' && SHIP.notes) || [];
  return ring.filter(n => (!kind || kind === '*' || n.kind === kind) && n.t >= since);
}
function flag(key) { return typeof SHIP !== 'undefined' && SHIP.flags && Object.prototype.hasOwnProperty.call(SHIP.flags, key) ? SHIP.flags[key] : undefined; }
function flagSet(key, value = true) {
  if (typeof SHIP === 'undefined' || typeof key !== 'string') return;
  const f = SHIP.flags || (SHIP.flags = {});
  if (value === null || value === undefined) delete f[key]; else f[key] = value;
}
const SHIP_RATE = 1080 / 1800;                           // ship minutes per real second: 18 ship hours in 30 real minutes (0.6)
const SHIP_START = { day: 1, min: 6 * 60, deck: 4 };     // Monday 06:00, in Bunk 1 (the tile is PLAYER_SPEC.start)
// a new game that arrives by shuttle (Pillar 4): day 0, a real ship Sunday, 17:30 (17:40 until 0.42.27), on the Tern's ramp on Deck 5 (day 1
// stays Monday, so the calendar never moves). Section 21 starts it: newGameStart(true), from New game or, on a first
// launch with no save, from its own load (this section can't see section 21 while it loads). Never with ?nosave
const SHIP_START_ARRIVAL = { day: 0, min: 17 * 60 + 30, deck: 5, tile: [5, 7], face: 0 };   // in the Tern's aisle (5-tern-aisle-1, the deck architect's walkable Tern), facing south to the door (section 21's INTRO_START; 0.26.35)
SHIP.time = { day: SHIP_START.day, min: SHIP_START.min };
const WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
const shipNow = () => (SHIP.time.day - 1) * 1440 + SHIP.time.min;    // absolute ship minutes
const weekday = day => ((day - 1) % 7 + 7) % 7;                         // 0 = Monday ... 6 = Sunday
const hhmm = min => { const m = Math.floor(min); return String(Math.floor(m / 60) % 24).padStart(2, '0') + ':' + String(m % 60).padStart(2, '0'); };
const clockText = () => 'Day ' + SHIP.time.day + ', ' + WEEKDAYS[weekday(SHIP.time.day)] + ' ' + hhmm(SHIP.time.min);
function setShipNow(abs) { SHIP.time.day = Math.floor(abs / 1440) + 1; SHIP.time.min = abs - (SHIP.time.day - 1) * 1440; }
// how dark the ship is at a time of day, 0 (day) to 1 (night): night from 21:00 to 06:00, with an hour of
// dusk (20:30-21:30) and of dawn (05:30-06:30) centred on them. The light eases toward this (main loop).
function nightAt(min = SHIP.time.min) {
  const s = x => x <= 0 ? 0 : x >= 1 ? 1 : x * x * (3 - 2 * x);
  return Math.max(1 - s((min - 330) / 60), s((min - 1230) / 60));
}

// Time jumps. Anything that simulates the ship registers a function here, SIM_ADVANCE.push((from, to) => ...),
// called with absolute ship minutes whenever time skips forward (sleep, the debug skip). It must be fast and draw
// nothing. Nothing is registered yet: the schedules (section 14) will advance everyone's state through it.
const SIM_ADVANCE = [];
function skipTo(abs) {
  const from = shipNow(); if (!(abs > from)) return;
  setShipNow(abs);
  if (typeof machinesNow === 'function') machinesNow();  // the machines' hours first, so their notes (stamped with their hour) are out before anyone catches up
  for (const f of SIM_ADVANCE) f(from, abs);
  updateClock(); saveGame();
}
// the player sleeps: time skips to `min` (ship minutes since midnight) the next time it comes round
function sleepUntil(min) {
  const now = shipNow(), today = (SHIP.time.day - 1) * 1440 + min;
  skipTo(today > now ? today : today + 1440);
}
// ---- the frozen clock (0.28.50, under section 15's Pause, 0.28.48): while the ship is frozen (PAUSE.on, or a game of
// Tiles being played: section 23's PAUSE.tiles) the main loop skips the sim. freezeSync() (once a frame, and from
// pauseSet) starts and stops the freeze; simNow() is performance.now() less the time spent frozen, for the sim's own
// real-time pacing (cool-downs, timeouts, auto-advances) so nothing jumps afterwards; simTimeout(fn, ms) / simClear(id)
// are setTimeout on that clock, run by the main loop (the tip card, the heads-up, the Captain's address, the intro's
// spoken lines). Leaving a freeze also calls section 15's pauseShift(ms) for the stamps that stay on real time.
// Toasts, input and the ghost-tap guard keep real time. Frozen time simply doesn't pass. Nothing here calls R().
const FREEZE = { frozen: false, at: 0, ms: 0 };
function simNow() { return (FREEZE.frozen ? FREEZE.at : performance.now()) - FREEZE.ms; }
function freezeSync() {
  let f = false; try { f = !!(PAUSE.on || PAUSE.tiles && PAUSE.tiles() || PAUSE.disc && PAUSE.disc()); } catch (e) { f = false; }   // PAUSE.disc: a game of Lightdisc (section 23b, 0.82.0)
  if (f === FREEZE.frozen) return f;
  const n = performance.now();
  if (f) FREEZE.at = n; else { const d = n - FREEZE.at; FREEZE.ms += d; if (typeof pauseShift === 'function') pauseShift(d); }
  FREEZE.frozen = f; return f;
}
const SIM_TIMERS = []; let SIM_TID = 0;
function simTimeout(fn, ms) { const id = ++SIM_TID; SIM_TIMERS.push({ id, at: simNow() + (ms || 0), fn }); return id; }
function simClear(id) { const i = SIM_TIMERS.findIndex(x => x.id === id); if (i >= 0) SIM_TIMERS.splice(i, 1); }
function simTimers() {                                   // main loop, when not frozen
  if (!SIM_TIMERS.length) return;
  const n = simNow();
  for (let k = 0; k < SIM_TIMERS.length; k++) { const x = SIM_TIMERS[k]; if (x.at > n) continue; SIM_TIMERS.splice(k--, 1); try { x.fn(); } catch (e) { console.error(e); } }
}
// the clock's frame step (main loop): the HUD clock each ship minute, a save each ship hour
function tickShip(dt) {
  if (document.hidden) return;                           // time never runs while the tab is hidden
  const m = Math.floor(SHIP.time.min), h = Math.floor(shipNow() / 60);
  SHIP.time.min += dt * SHIP_RATE;
  if (SHIP.time.min >= 1440) { SHIP.time.min -= 1440; SHIP.time.day++; }
  if (Math.floor(SHIP.time.min) !== m) { updateClock(); if (typeof pausePlace === 'function') pausePlace(); if (typeof apptTick === 'function') apptTick(); if (typeof shiftTick === 'function') shiftTick(); if (typeof careerTick === 'function') careerTick(); }   // section 14: appointments kept or missed; your shift's start
  if (Math.floor(shipNow() / 60) !== h) saveGame();
}

// ---- saving: { v, build, time, player: { deck, tile, facing, needs }, ship: { decks: { n: { open } } }, crew: {} } ----
// v 2 (0.28.1) adds player.needs (section 15, through SAVE_EXTRA); a v 1 save still loads, with needs at 80
const SAVE_KEY = 'starship-cadet-save', SAVE_V = 2;
const SAVE_EXTRA = [];                                   // other sections add their part: f(save) just before it's written (17: machines)
const URL_FLAGS = new URLSearchParams(location.search);
// 0.27.12: a claude.ai artifact page never gets the ?query, only a #hash of letters, digits and . _ ~ -, so the switches
// also read it: tokens joined by '.', a value after the first '-' (#crowd-120.seats is ?crowd=120&seats). The ?query wins.
for (const tok of location.hash.slice(1).split('.')) { const i = tok.indexOf('-'), k = i < 0 ? tok : tok.slice(0, i); if (k && !URL_FLAGS.has(k)) URL_FLAGS.set(k, i < 0 ? '' : tok.slice(i + 1)); }
const urlFlag = name => URL_FLAGS.has(name) ? URL_FLAGS.get(name) : null;   // a switch's value ('' when it has none), or null
const NOSAVE = URL_FLAGS.has('nosave') || URL_FLAGS.has('crowd') || URL_FLAGS.has('poses') || URL_FLAGS.has('seats'),   // the crowd, pose and seat demos (section 8b) never touch the save
      DEBUG = URL_FLAGS.has('debug');
function saveGame() {
  if (NOSAVE) return;
  try {
    const decks = {};
    for (const n in SHIP.decks) if (SHIP.decks[n].open.size) decks[n] = { open: [...SHIP.decks[n].open] };
    const save = {
      v: SAVE_V, build: GAME_BUILD, time: { day: SHIP.time.day, min: SHIP.time.min },
      player: { deck: player.deck, tile: player.here(), facing: player.face }, ship: { decks }, crew: {},
      flags: SHIP.flags || {}, notes: SHIP.notes || [],
    };
    if (typeof crewState === 'function') save.crew = crewState(SHIP.time.day);   // who's aboard, who left, who arrived (rebuilt from the roster on load)
    for (const f of SAVE_EXTRA) f(save);
    localStorage.setItem(SAVE_KEY, JSON.stringify(save));
  } catch (e) { /* no storage, or full: the game carries on unsaved */ }
}
function loadGame() {
  if (NOSAVE) return null;
  try {
    const s = JSON.parse(localStorage.getItem(SAVE_KEY));
    if (!s || !(s.v === 1 || s.v === SAVE_V)) return null;   // no save, or one this build doesn't know: start fresh
    const t = s.time, p = s.player, tile = p && p.tile;
    if (!t || !(t.day >= 0 && t.day % 1 === 0) || !(t.min >= 0 && t.min < 1440) || !DECKS[p.deck]) return null;
    if (!Array.isArray(tile) || tile.length !== 2 || !tile.every(Number.isInteger) || !isFinite(p.facing)) return null;
    return s;
  } catch (e) { return null; }
}
const SAVED = loadGame();
// where you start: the save's deck, tile and facing, or Deck 4 at PLAYER_SPEC.start (section 10 reads this)
const START = SAVED && (REC_DECK || SAVED.player.deck !== 7) ? { deck: SAVED.player.deck, tile: SAVED.player.tile, face: SAVED.player.facing } : { deck: SHIP_START.deck };   // REC_DECK off: a save on the rec deck starts at the usual place
if (SAVED) {
  SHIP.time.day = SAVED.time.day; SHIP.time.min = SAVED.time.min;
  const decks = (SAVED.ship && SAVED.ship.decks) || {};
  for (const n in decks) if (DECKS[n] && Array.isArray(decks[n].open)) shipDeck(+n).open = new Set(decks[n].open);
  // the flag store and the recent notes (Pillar 4), read defensively: plain objects only, a note needs a kind and a time
  const fl = SAVED.flags; if (fl && typeof fl === 'object' && !Array.isArray(fl)) SHIP.flags = Object.assign(SHIP.flags || {}, fl);
  if (Array.isArray(SAVED.notes)) SHIP.notes = SAVED.notes.filter(n => n && typeof n.kind === 'string' && isFinite(n.t)).slice(-SIM_RING);
}
nightT = nightAt();                                      // wake to the right light, not a fade into it
document.addEventListener('visibilitychange', () => { if (document.hidden) saveGame(); });
addEventListener('pagehide', saveGame);
const welcomeBack = () => 'Welcome back. ' + clockText() + '.';

// New game: the first tap asks, a second within 4 seconds clears the save and starts again in Bunk 1 at 06:00
const newBtn = document.getElementById('newgame'); let newAsk = 0;
newBtn.onclick = () => {
  const span = newBtn.querySelector('span');
  if (!newAsk) { span.textContent = 'Tap again'; newBtn.classList.add('ask'); newAsk = setTimeout(() => { newAsk = 0; span.textContent = 'New game'; newBtn.classList.remove('ask'); }, 4000);
    if (matchMedia('(max-width:720px),(max-height:500px)').matches) toast('New game', 'Tap again to start over.');   // 0.35.34: the label is hidden on narrow phones
    return; }
  clearTimeout(newAsk); newAsk = 0; span.textContent = 'New game'; newBtn.classList.remove('ask');
  if (ride) return;                                      // not mid-ride
  // how to start (agreed with section 21 and the device): the tests and anyone without section 21 wake on Monday; a
  // device that has never arrived arrives by shuttle; one that has gets the choice (arrive, or skip to Monday)
  if (NOSAVE || typeof introArrived !== 'function') return newGameStart(false);
  if (!introArrived() || typeof deviceChoose !== 'function') return newGameStart(true);
  deviceChoose({ title: 'New game', text: 'How do you want to start?', choices: ['Arrive by shuttle (Sunday evening)', 'Skip to Monday morning'] },
    i => { if (i === 0) newGameStart(true); else { newGameStart(false); if (typeof introSkip === 'function') introSkip(); } });
};
// a new game (Pillar 4): by shuttle on day 0 at 17:30 (arrival true: section 21 then calls introBegin), or in Bunk 1
// on Monday at 06:00 (false; section 21 calls introSkip when you skipped the arrival). Clears the save, the decks'
// state, the habit changes, the flag store and the notes, then sections 15, 20 start again
function newGameStart(arrival) {
  const arr = !!arrival;
  try { if (!NOSAVE) localStorage.removeItem(SAVE_KEY); } catch (e) {}
  for (const n in SHIP.decks) delete SHIP.decks[n];
  HABIT_SAVED = null; HABIT_WEEKS.length = 1;           // section 14: the habit changes start again
  try { queueOut(false); } catch (e) { /* at load, before section 10's lines exist: nobody's in one */ }   // section 10: out of a booth or shower line (0.71.6)
  SHIP.flags = {}; SHIP.notes = [];                      // the flag store and the notes start again too
  const S0 = arr ? SHIP_START_ARRIVAL : SHIP_START;
  SHIP.time.day = S0.day; SHIP.time.min = S0.min; nightT = nightAt();
  if (!liftEl.hidden) closeLiftPanel();
  goToDeck(S0.deck);
  let c = arr ? SHIP_START_ARRIVAL.tile : PLAYER_SPEC.start;
  if (!free(...c)) { const p = cellPos(...c); c = nearestOpen(p.x, p.z, player) || c; }
  player.obj.position.copy(cellPos(...c)); player.face = player.obj.rotation.y = arr ? SHIP_START_ARRIVAL.face : Math.PI;
  target.copy(player.obj.position).setY(.7); lastRoom = null;
  playerNew();                                           // section 15: fresh needs
  if (typeof machinesNew === 'function') machinesNew();  // section 17: the machines and jobs afresh, before section 21 reserves its jobs
  if (typeof socialNew === 'function') socialNew();      // section 20: strangers again
  if (typeof introNewGame === 'function') introNewGame(arr);   // section 21: the arrival begins, or a blank intro (Monday)
  simNote('newGame', { arrival: arr });                  // anyone else with state of their own starts again
  updateClock(); saveGame();
  if (!arr) toast('Deck 4, CSV Wren', 'A new game. You wake in Bunk 1, in the junior wing, at 06:00 on a Monday.');
}
// Going to sleep: tap your own bunk (playerBed(), ROSTER_PLAYER's bed, by its place on Deck 4) from 20:00 to 05:30.
// The alarm clock opens (0.73.0; no dialog from 0.28.9 to then); Set alarm fades the view out, skips to the wake time
// (sleepUntil) and fades back in. Unwell by day (the nap) you sleep at once, as before.
const playerBed = () => { const h = typeof SHIP !== 'undefined' && SHIP.works && SHIP.works.home; return typeof h === 'string' && (DECKS[4].places || []).some(q => q.id === h && q.type === 'bed') ? h : ROSTER_PLAYER.bed; }, WAKE_AT = 6 * 60, CLOCK_EARLY = 7;   // CLOCK_EARLY: minutes the Works crew arrive early to clock in (the clock's queue wait, 6, and the clocking, 1)   // read when used: ROSTER_PLAYER comes later in the file
const sleepEl = document.getElementById('sleepAsk'); let sleeping = false;
const bedtime = () => SHIP.time.min >= 20 * 60 || SHIP.time.min < 5 * 60 + 30;
function offerSleep(at) {                                // at: where the tapped item is. True if it was your bunk
  const id = playerBed(), bed = (DECKS[deckOf(id)].places || []).find(p => p.id === id);
  if (!bed || deckDef.num !== deckOf(id) || at.distanceTo(cellPos(...bed.at)) > 1.2) return false;
  if (!bedtime() && !(typeof sickNow === 'function' && sickNow())) { toast('Your bunk', 'Too early to turn in. You can sleep here from 20:00.'); return true; }
  toastEl.classList.remove('show');
  if (!bedtime()) sleepGo(null); else alarmOpen();       // the nap (unwell by day) at once; at night the alarm clock (0.73.0)
  return true;
}
// the alarm clock (0.73.0, playtest 2, the user's): pick the wake time with − / + (ALARM_STEP minutes, ALARM_FROM to
// ALARM_TO and at least ALARM_SOON ahead), see the energy you'll wake with (alarmEnergy: the overnight skip's own
// needsDrain on a copy of your needs, so later gives more) and a warning when it's at or after your shift's start that
// morning (alarmLate). Set alarm sleeps until then; Not yet closes it (lying in your bunk you stay lying). The time is
// kept for next night as SHIP.player.alarm (minute of the day; save.player.alarm; old saves and New game: WAKE_AT,
// 06:00, what bedtime always did). Texts: the head writer's alarm.* (stand-ins until baked). No R().
const ALARM_STEP = 30, ALARM_FROM = 4 * 60, ALARM_TO = 12 * 60, ALARM_SOON = 30;
const alarmOk = m => Number.isInteger(m) && m >= ALARM_FROM && m <= ALARM_TO && m % ALARM_STEP === 0;
let ALARM_PICK = WAKE_AT;
const alarmText = (k, fb, v = {}) => ((typeof careerText === 'function' && careerText(k)) || fb).replace(/\{(\w+)\}/g, (x, n) => v[n] !== undefined ? v[n] : x);
function alarmAt(m) { const now = shipNow(), t = (SHIP.time.day - 1) * 1440 + m; return t > now ? t : t + 1440; }   // as sleepUntil
function alarmChoices() {                                // the wake times on offer now, soonest first
  const out = [], now = shipNow();
  for (let m = ALARM_FROM; m <= ALARM_TO; m += ALARM_STEP) { const d = alarmAt(m) - now; if (d >= ALARM_SOON && d <= 18 * 60) out.push(m); }
  return out.sort((a, b) => alarmAt(a) - alarmAt(b));
}
function alarmEnergy(m) {                                // the energy you'd wake with, rounded
  const n = SHIP.player.needs, keep = { ...n }, d = typeof deckDef !== 'undefined' && deckDef ? deckDef.num : 0;
  let fx = null; try { fx = typeof shipEffectsAt === 'function' && d ? shipEffectsAt(d, shipNow()) : null; } catch (e) { fx = null; }
  try { needsDrain(alarmAt(m) - shipNow(), true, fx); return Math.round(n.energy); } finally { Object.assign(n, keep); }
}
function alarmLate(m) {                                  // your shift's start that morning if the alarm is at or after it, else 0
  const d = Math.floor(alarmAt(m) / 1440) + 1;
  return typeof DAY_SHIFT !== 'undefined' && typeof playerShiftOn === 'function' && playerShiftOn(d) && m >= DAY_SHIFT[0] ? DAY_SHIFT[0] : 0;
}
function alarmDraw() {
  const ch = alarmChoices(), k = ch.indexOf(ALARM_PICK), $ = id => document.getElementById(id), late = alarmLate(ALARM_PICK);
  $('sleepT').textContent = alarmText('alarm.title', 'Alarm');
  $('alarmT').textContent = alarmText('alarm.wake', 'Wake at {time}', { time: hhmm(ALARM_PICK) });
  $('alarmDn').disabled = k <= 0; $('alarmUp').disabled = k < 0 || k >= ch.length - 1;
  $('alarmE').textContent = alarmText('alarm.energy', 'You\'ll wake with about {n}% energy.', { n: alarmEnergy(ALARM_PICK) }) + ' ' + alarmText('alarm.more', 'Sleep longer, wake fresher.');
  $('alarmW').hidden = !late; $('alarmW').textContent = late ? alarmText('alarm.late', 'That\'s after your shift starts at {start}. Set it earlier?', { start: hhmm(late) }) : '';
  $('sleepYes').textContent = alarmText('alarm.set', 'Set alarm');
}
function alarmOpen() {                                   // the saved time, or the nearest one on offer
  const ch = alarmChoices(), a = SHIP.player.alarm, gap = m => Math.min(Math.abs(m - a), 1440 - Math.abs(m - a));
  ALARM_PICK = ch.includes(a) ? a : ch.slice().sort((x, y) => gap(x) - gap(y))[0];
  if (ALARM_PICK === undefined) { sleepGo(WAKE_AT); return; }   // nothing on offer (can't happen in bedtime's hours): as before
  alarmDraw(); sleepEl.hidden = false;
}
function alarmStep(by) { const ch = alarmChoices(), k = ch.indexOf(ALARM_PICK) + by; if (k >= 0 && k < ch.length) { ALARM_PICK = ch[k]; alarmDraw(); } }
document.getElementById('alarmDn').onclick = () => alarmStep(-1);
document.getElementById('alarmUp').onclick = () => alarmStep(1);
document.getElementById('sleepNo').onclick = () => { sleepEl.hidden = true; };
document.getElementById('sleepYes').onclick = () => sleepGo(ALARM_PICK);
function sleepGo(wake) {                                 // wake: the alarm (minute of the day), or null for the nap
  sleepEl.hidden = true; if (sleeping || ride) return;
  sleeping = true; fadeEl.style.transition = 'opacity .8s'; fadeEl.style.opacity = 1;
  const nap = !bedtime() && typeof sickNow === 'function' && sickNow();   // unwell by day: sleep it off for a few hours (0.61.5)
  if (!nap) { if (!alarmOk(wake)) wake = WAKE_AT; SHIP.player.alarm = wake; toast(alarmText('alarm.title', 'Alarm'), alarmText('alarm.toast', 'Alarm set for {time}.', { time: hhmm(wake) })); }
  setTimeout(() => {
    if (nap) { skipTo(shipNow() + SICK.nap); sickCure(3); } else sleepUntil(wake); nightT = nightAt();
    fadeEl.style.opacity = 0;
    setTimeout(() => { fadeEl.style.transition = ''; sleeping = false; if (!nap) toast('Good morning', alarmText('alarm.ring', 'Morning. Your alarm\'s going.') + ' ' + clockText() + '.'); }, 850);
  }, 900);
}
addEventListener('keydown', e => { if (e.key === 'Escape' && !sleepEl.hidden) sleepEl.hidden = true; });
// the Night/Day button is a debug control now: Night skips to 21:40, Day sleeps until 07:40
function debugSkip() {
  if (nightAt() > .5) sleepUntil(7 * 60 + 40);
  else skipTo((SHIP.time.day - 1) * 1440 + 21 * 60 + 40);
}
if (!DEBUG) document.getElementById('light').style.display = 'none';

