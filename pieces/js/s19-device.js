// =====================================================================
// 19. DEVICE
// Your personal device (Pillar 3, the device engineer, 0.35.x): the game's one
// menu. Two layers. The APPS describe: deviceApp({ id, title, icon, order,
// badge, view, act }) registers one; view(ctx) returns plain content (a VIEW,
// below) and act(verb, arg) handles its buttons. The SKIN draws: DEVICE_SKIN is
// the only code here that touches the DOM, so the look can change without
// touching an app. deviceDo(action) runs a tapped action; deviceNotify({ app,
// text, urgent }) puts a badge on an app (and a toast if urgent); deviceOn('open'
// | 'close', fn) for the pose and the camera. device.addSection(id, title,
// render) stays as a shim: render(el) draws into a box, as before.
// VIEW: { title, blocks: [ { kind: 'text', text, mark }, { kind: 'list', rows:
//   [{ text, sub, mark, action, button }] }, { kind: 'bars', items: [{ label,
//   value, mark, note, level }] }, { kind: 'buttons', items: [{ label, action }] },
//   { kind: 'chips', items: [{ label, on, action }] } ] } (chips: big toggles, crossed out while on is false;
//   build one with devChips(items), which falls back to buttons marked "✕ " on a skin without them),
//   { kind: 'strip', rows: [{ label, hours: [24 × 0-1], pins: [hour] }] } (a day strip: a bar per hour, 12 px wide,
//   scrolling sideways on a phone; build one with devStrip(rows, fallback), a list on a skin without it)
// action: { app, do, arg }. mark: 'up' | 'down' | 'new' | 'urgent' | 'hot' | 'big'.
// Sits before 15 (after 14), so 15 and 17 can register at load; apps only read
// other sections when drawn. Nothing here calls R() or makes 3D objects.
// =====================================================================
const DEVICE_APPS = new Map();                 // id -> { id, title, icon, order, badge, view, act }
const DEV = { open: false, app: 'home', notes: {}, on: { open: [], close: [], phosphor: [] }, errors: [] };
// what the device keeps (saved, SAVE_EXTRA): settings now; memos, appointments, pins and tips as their apps arrive
const PHOSPHORS = { amber: 'Amber', green: 'Green', cyan: 'Wren cyan' };
function deviceLoad(s) {
  const d = s && s.device && typeof s.device === 'object' ? s.device : {}, st = d.settings && typeof d.settings === 'object' ? d.settings : {};
  const r = d.calendarRemind && typeof d.calendarRemind === 'object' ? d.calendarRemind : {}, per = {};
  if (r.per && typeof r.per === 'object') for (const k in r.per) if (typeof r.per[k] === 'boolean' && k.length < 40) per[k] = r.per[k];
  const memos = (Array.isArray(d.memos) ? d.memos : []).filter(m => m && typeof m === 'object' && typeof m.title === 'string').slice(0, 50)
    .map((m, i) => ({ id: Number.isInteger(m.id) ? m.id : 1000 + i, title: m.title.slice(0, 80), text: typeof m.text === 'string' ? m.text.slice(0, 2000) : '', at: isFinite(m.at) ? +m.at : 0, pinned: !!m.pinned }));
  const tipsSeen = {}; if (d.tipsSeen && typeof d.tipsSeen === 'object') for (const k in d.tipsSeen) if (d.tipsSeen[k] === true && k.length < 40) tipsSeen[k] = true;
  const appts = (Array.isArray(d.appts) ? d.appts : []).filter(a => a && typeof a === 'object' && Number.isInteger(a.id) && isFinite(a.at) && Array.isArray(a.with) && typeof a.where === 'string')
    .slice(-60).map(a => ({ ...a, id: a.id, with: a.with.filter(x => typeof x === 'string').slice(0, 8), at: +a.at, len: isFinite(a.len) ? +a.len : 30, where: a.where,
      kind: typeof a.kind === 'string' ? a.kind : 'social', status: ['asked', 'yes', 'no', 'kept', 'missed'].includes(a.status) ? a.status : 'no', by: typeof a.by === 'string' ? a.by : null,
      ...(Number.isInteger(a.grp) ? { grp: a.grp } : {}), ...(a.places && typeof a.places === 'object' ? { places: Object.fromEntries(Object.entries(a.places).filter(([k, v]) => typeof v === 'string').slice(0, 8)) } : { places: undefined }) }));   // places: each person's seat (0.71.2)
  return { memos, tipsSeen, appts, booted: d.booted === true, settings: { phosphor: PHOSPHORS[st.phosphor] ? st.phosphor : 'cyan', fx: st.fx !== false, tips: st.tips !== false, quiet: st.quiet === true },
    calendarRemind: { on: r.on !== false, ahead: [15, 30, 60].includes(r.ahead) ? r.ahead : 15, morning: r.morning !== false, per, everyday: r.everyday !== false,
      heard: (Array.isArray(r.heard) ? r.heard : []).filter(k => typeof k === 'string' && k.length < 120).slice(-80) } };   // 0.35.29: heads-ups
}
SHIP.device = deviceLoad(SAVED);
// the page knows the phosphor (html data-ph) for screens drawn by other sections, like section 20's #seek chip
function devPhosphorPage() { document.documentElement.dataset.ph = SHIP.device.settings.phosphor; }
devPhosphorPage();
SAVE_EXTRA.push(s => { s.device = JSON.parse(JSON.stringify(SHIP.device)); });
setTimeout(() => {
  DEV.live = true;
  try { if (typeof CHAT_SKIN !== 'undefined' && CHAT_SKIN && !CHAT_SKIN.draw) CHAT_SKIN.draw = DEVICE_SKIN.chat; } catch (e) { /* no section 20 */ }
}, 0);
// ---- your day (0.35.2): the shift, the meals, the week's shape and the ship traditions, for Schedule, Calendar
// and Home. The player works the day shift, with Saturday and Sunday off (section 14's playerShiftOn). ----
const DEV_SHIFT = { from: 540, to: 1020, where: 'the Works bay, Deck 5' };   // 09:00-17:00 (0.44.14; section 17's DAY_SHIFT, which comes later in the file)
// 0.35.17: the player's days off come from section 14's playerShiftOn(d) (the sim engineer; the user chose Saturday and
// Sunday off). Section 19 no longer defines it, as a later declaration here would override section 14's
const devShiftOn = d => { if (typeof playerShiftOn !== 'function') return true; try { return playerShiftOn(d) !== false; } catch (e) { return true; } };
// the weekday shapes (section 14's WEEK_SHAPE) that really put people somewhere. 0.35.18 (the user: "the schedule says
// there is a Works meeting but nothing happened"): Monday's "All-hands briefing in the Works bay" is gone, as section 14's
// Monday only starts the day shift 10 minutes early and nobody gathers; the Captain's piano stand-in is gone too (only
// section 18's traditions are listed). Wednesday's drill (off-duty crew muster by each deck's lift, tag 'drill') and
// Thursday's bunk tidy for inspection (juniors in the Deck 4 bunk rooms, tag 'inspection') do happen
const DEV_WEEK = [
  [], [],
  [{ at: 900, title: 'Drill: off-duty crew muster by the lift', where: 'the lift lobby on each deck', len: 15 }],
  [{ at: 400, title: 'Bunk inspection: tidy your bunk', where: 'your bunk, Deck 4', len: 20 }],
  [], [], []];
const devDeckOf = ev => { const w = ev && ev.where && ev.where[0]; return w ? deckWord(w.deck) : 'aboard'; };
// the ship traditions between two absolute ship minutes: section 18's upcomingTraditions when it's there, else eventsOn
function devTraditions(a, b) {
  if (typeof upcomingTraditions === 'function') {
    try { return upcomingTraditions(a, b).map(x => ({ id: x.id + '@' + x.at, kind: x.kind || String(x.id).replace(/@.*$/, ''), title: x.title, at: x.at, to: x.to || x.at + 60, where: x.where || 'aboard',
      ...(Number.isInteger(x.deck) ? { deck: x.deck, room: typeof x.room === 'string' ? x.room : null } : {}) })); }
    catch (e) { DEV.errors.push('upcomingTraditions: ' + (e && e.message || e)); }
  }
  if (typeof eventsOn !== 'function') return [];
  const out = [];
  for (let d = Math.floor(a / 1440) + 1; d <= Math.floor(b / 1440) + 1; d++) {
    for (const e of eventsOn(d)) {
      const at = (d - 1) * 1440 + e.from; if (at < a || at > b) continue;
      out.push({ id: e.id + '@' + d, kind: e.id, at, to: (d - 1) * 1440 + e.to, title: e.id === 'birthday' && e.names ? 'Birthday: ' + e.names : e.name, where: devDeckOf(e.ev) });
    }
    for (const x of DEV_WEEK[weekday(d)]) if (x.tradition) { const at = (d - 1) * 1440 + x.at; if (at >= a && at <= b) out.push({ id: x.tradition + '@' + d, kind: x.tradition, at, title: x.title, where: x.where }); }
  }
  return out.sort((x, y) => x.at - y.at);
}
// section 18's booked occasions (0.35.30: the ready room, the Captain's table, a progress talk), read only: SHIP.occasions
// still 'asked', not a chance one (a surprise), between two ship minutes. Section 18 calls apptAdd for them, which no
// section has, so until then the Schedule lists them from here
function devOccasions(a, b) {
  try {
    if (!Array.isArray(SHIP.occasions) || typeof OCCASIONS === 'undefined') return [];
    const booked = new Set(SHIP.device.appts.map(x => x.occ).filter(Boolean));   // 0.35.32: those apptAdd booked are listed as appointments
    return SHIP.occasions.filter(r => r && r.status === 'asked' && r.at >= a && r.at <= b && OCCASIONS[r.id] && !OCCASIONS[r.id].chance && !booked.has(r.key)).map(r => {
      const rm = DECKS[r.deck] && DECKS[r.deck].rooms && DECKS[r.deck].rooms[r.room];
      return { at: r.at, len: r.len || 30, title: OCCASIONS[r.id].title, deck: r.deck, room: rm ? r.room : null, where: (rm ? rm.name + ', ' : '') + deckWord(r.deck) };
    });
  } catch (e) { return []; }
}
// one day's items, in time order: [{ from, to, title, where, kind }] in minutes of that day
function devDay(d) {
  const B = (d - 1) * 1440, out = [
    { from: MEALS.breakfast[0], to: MEALS.breakfast[1], title: 'Breakfast', where: 'the mess, Deck 3', kind: 'meal' },
    { from: DEV_SHIFT.from, to: DEV_SHIFT.to, title: 'On shift', where: DEV_SHIFT.where, kind: 'shift' },
    { from: MEALS.dinner[0], to: MEALS.dinner[1], title: 'Dinner', where: 'the mess, Deck 3', kind: 'meal' }];
  if (!devShiftOn(d)) out.splice(1, 1, { from: DEV_SHIFT.from, to: DEV_SHIFT.to, title: 'Day off', where: 'no shift today, your time is your own', kind: 'off' });
  for (const g of apptGroups(SHIP.device.appts.filter(a => (a.status === 'yes' || a.status === 'kept') && a.at >= B && a.at < B + 1440)))
    out.push({ from: g.a.at - B, to: g.a.at - B + (g.a.len || 30), title: g.a.title || 'With ' + g.names, where: apptWhereName(g.a.where), kind: 'appt', place: g.a.where, aid: g.a.grp || g.a.id });
  for (const x of DEV_WEEK[weekday(d)]) if (!x.tradition) out.push({ from: x.at, to: x.at + x.len, title: x.title, where: x.where, kind: 'ship' });
  for (const x of devTraditions(B, B + 1439)) out.push({ from: x.at - B, to: x.at - B + 60, title: x.title, where: x.where, kind: 'tradition', id: x.id, tkind: x.kind, deck: x.deck, room: x.room });
  for (const o of devOccasions(B, B + 1439)) out.push({ from: o.at - B, to: o.at - B + o.len, title: o.title, where: o.where, kind: 'occasion', deck: o.deck, room: o.room });
  // playtest 2 (0.72.5, items 10-11): tea and biscuits on your shift days (section 14's crew tea times, else section 15's), and
  // the week's supply delivery to the cargo hold (section 17's DELIVERY, a day or two late some weeks: deliveryLate)
  try { const T = typeof WORKS_TEA !== 'undefined' && WORKS_TEA && Number.isFinite(WORKS_TEA.at) ? WORKS_TEA : typeof TEA_FROM !== 'undefined' ? { at: TEA_FROM, until: TEA_TO } : null;
    if (T && devShiftOn(d)) out.push({ from: T.at, to: T.until, title: 'Tea and biscuits', where: 'the Tea corner, Deck 5', kind: 'tea' }); } catch (e) { /* not yet */ }
  try { if (typeof DELIVERY !== 'undefined' && typeof deliveryLate === 'function') { const due = DELIVERY.day + deliveryLate(d);
    if (weekday(d) === due) out.push({ from: DELIVERY.hour * 60, to: DELIVERY.hour * 60 + 60, title: 'Supply delivery', where: 'the cargo hold, Deck 5', kind: 'delivery' }); } } catch (e) { /* not yet */ }
  // playtest 2 item 12 (a) (0.73.2, U2; the lead's call): the arrival week's timed beats you go to that aren't booked as
  // appointments (section 21's INTRO_WEEK: Monday's briefing, Calder's first job, the Day 2 booths, the crew store), while
  // the intro runs, so the heads-ups, the Schedule and the Tracked list have them. Beats that come to you (Zeke walking
  // up, a wash call at your bunk), the shift's own, meals, tea and traditions are listed already or need no heads-up.
  try { if (typeof introOn === 'function' && introOn() && typeof INTRO_WEEK !== 'undefined') for (const b of INTRO_WEEK)
    if (b.day === d && DEV_BEATS[b.id] && b.where && Number.isInteger(b.where.deck))
      out.push({ from: b.at, to: b.until || b.at + 30, title: DEV_BEATS[b.id], where: b.where.room + ', ' + deckIn(b.where.deck), kind: 'beat', deck: b.where.deck, room: b.where.room }); } catch (e) { /* not yet */ }
  return out.sort((x, y) => x.from - y.from);
}
const DEV_BEATS = { 'd1-briefing': 'Morning briefing with the Chief', 'd2-solo': 'The Chief\'s office: your first job', 'd2-booths': 'Calling home', 'd3-store': 'The crew store' };   // titles (stand-ins; the beats' own words are section 21's)
const devWhen = t => hhmm(((t % 1440) + 1440) % 1440);
const devDayName = d => d === SHIP.time.day ? 'Today' : d === SHIP.time.day + 1 ? 'Tomorrow' : WEEKDAYS[weekday(d)] + ', Day ' + d;
function devNow() {                                      // the strip: where you're expected right now, and what's next
  const d = SHIP.time.day, m = SHIP.time.min, items = devDay(d);
  const now = items.filter(x => x.from <= m && m < x.to && x.kind !== 'tradition').pop(), next = items.find(x => x.from > m);
  return { now: now ? now.title + ': ' + now.where : 'Free time', next: next ? 'Next: ' + next.title + ' at ' + hhmm(next.from) : null };
}

// ---- reminders (the user's addition): about 30 ship minutes before each tradition, a chirp (a toast) or, during your
// shift, a quiet badge unless you marked it "Remind me". Each morning the Calendar gets a badge and Home a "Today
// aboard" line. SHIP.device.calendarRemind = { on, ahead, morning, per: { <kind>: true | false } }, saved. ----
let devTickMin = -1, devMorning = SHIP.time.day;
function deviceTick() {
  if (!DEV.live return;                                 // not while the script is still loading (section 18 comes later)
  if (devLocked()) { SHIP.device.booted = false; if (DEV.open) deviceClose(); }
  const t = shipNow(); if (t === devTickMin) return; devTickMin = t;
  if (typeof sleeping !== 'undefined' && sleeping) return;
  const R = SHIP.device.calendarRemind;
  if (SHIP.time.day !== devMorning && SHIP.time.min >= 360) {   // a new morning
    devMorning = SHIP.time.day;
    if (R.on && R.morning && devTraditions(t, (SHIP.time.day) * 1440 - 1).length) DEV.notes.calendar = (DEV.notes.calendar || 0) + 1;
  }
  if (Array.isArray(SHIP.occasions)) for (const a of SHIP.device.appts) if (a.occ && a.status === 'yes') {   // 0.35.32: an occasion you met is kept, wherever in the
    const r = SHIP.occasions.find(x => x.key === a.occ); if (r && (r.met || r.status === 'kept')) { a.status = 'kept'; a.keptAt = t; }   // room you stood; 0.35.38 (the lead):
  }                                                       // once section 14 has marked it missed (15 minutes in), missed is final
  for (const a of SHIP.device.appts) if (a.grp && a.status === 'kept')   // a group meeting: meeting one of them (section 14's apptTick) keeps them all
    for (const o of SHIP.device.appts) if (o.grp === a.grp && (o.status === 'yes' && t >= o.at - 2 || o.status === 'missed')) { o.status = 'kept'; o.keptAt = t; }
  devHeadsTick(t);
}

// ---- heads-ups (0.35.29, the user's): before anything in your Schedule starts (traditions, ship items, appointments and
// the meetings section 18 books as appointments, meals and your shift), a short strip at the screen's edge, R.ahead ship
// minutes before ("Tiles night starts in 15 min · Bow lounge, Deck 3") and a gentler one as it starts. Only the Schedule's
// own items (devDay), never two at once, never over a meeting, a question, a tip, the Captain's address, a chat card or
// sleep (they wait; stale ones drop), never while the device is locked, each once (R.heard, saved). Tap: the Schedule;
// Go there: the goal arrow. Traditions keep their rules: Don't (R.per) skips them, and on shift they're a quiet Calendar
// badge unless you chose Remind me. Meals and your shift can be switched off (R.everyday); all but your appointments with R.on (0.35.33). ----
const HU_Q = [];                                         // waiting heads-ups, oldest first; HU_Q[0] is on screen when DEV.hu
const devHeard = k => SHIP.device.calendarRemind.heard.includes(k);
function devHear(k) { const h = SHIP.device.calendarRemind.heard; h.push(k); if (h.length > 80) h.splice(0, h.length - 80); }
function devPlaceGoal(id) {                              // a place id (an appointment's) -> setGoal's { deck, place, label }
  for (const n of Object.keys(DECKS)) if ((DECKS[n].places || []).some(x => x.id === id)) return { deck: +n, place: id, label: apptWhereName(id) };
  return null;
}
function devItemGoal(x) {
  if (x.kind === 'appt' && x.place) return devPlaceGoal(x.place);
  if (x.kind === 'meal') return { deck: 3, room: 'M', label: 'The mess hall, Deck 3' };
  if (x.kind === 'shift') return { deck: 5, room: 'w', label: 'The Works bay, Deck 5' };
  if (x.kind === 'tea') return { deck: 5, room: 't', label: 'The Tea corner, Deck 5' };   // 0.72.5
  if (x.kind === 'delivery') return { deck: 5, room: 'c', label: 'The cargo hold, Deck 5' };
  if ((x.kind === 'tradition' || x.kind === 'occasion' || x.kind === 'beat') && Number.isInteger(x.deck) && x.room) return { deck: x.deck, room: x.room, label: x.where };
  return null;
}
const devHuName = x => x.kind === 'shift' ? 'Your shift' : x.title;
function devHuBusy() {
  if (typeof sleeping !== 'undefined' && sleeping) return true;
  if (document.body.classList.contains('dlgon') || TIP_Q.length || DEV.choose) return true;
  const a = document.getElementById('devAddr'), c = document.getElementById('chat');
  return !!(a && !a.hidden) || !!(c && !c.hidden && c.classList.contains('devchat'));
}
function devHeadsTick(t) {
  const R = SHIP.device.calendarRemind;
  if (devLocked()) { HU_Q.length = 0; if (DEV.hu) { DEV.hu = null; DEVICE_SKIN.heads(null); } return; }
  if (DEV.hu && devHuBusy()) devHeadsBack();             // 0.35.33: something that takes the screen (a chat card...) sends a showing strip back to wait
  for (let d = SHIP.time.day; d <= SHIP.time.day + 1; d++) for (const x of devDay(d)) {
    const at = (d - 1) * 1440 + x.from, key = x.kind + '|' + at + '|' + (x.kind === 'appt' ? x.aid : x.title);   // an appointment by its id: a group that grows isn't new
    if (x.kind === 'off' || at - R.ahead > t || at + 3 <= t) continue;
    if (!R.on && x.kind !== 'appt' && x.kind !== 'beat') continue;   // the arrival week's beats like appointments (0.73.2); 0.35.33 (the lead): what you're booked for still comes with heads-ups off
    if ((x.kind === 'meal' || x.kind === 'shift' || x.kind === 'tea') && !R.everyday) continue;   // tea like the meals (0.72.5)
    if (x.kind === 'tradition' && R.per[x.tkind] === false) continue;
    const stage = t < at ? 'soon' : 'start', k = key + '|' + stage;
    if (devHeard(k) || (stage === 'soon' && at - t < 3)) continue;   // a 'soon' with under 3 minutes left waits for the start
    devHear(k);
    if (x.kind === 'tradition' && devOnShift() && R.per[x.tkind] !== true) { DEV.notes.calendar = (DEV.notes.calendar || 0) + 1; continue; }   // on shift: a quiet badge
    for (let i = HU_Q.length - 1; i >= 0; i--) if (HU_Q[i].key === key) HU_Q.splice(i, 1);   // the start replaces a waiting 'soon'
    HU_Q.push({ key, stage, at, title: devHuName(x), where: x.where, goal: devItemGoal(x) });
  }
  for (const a of SHIP.device.appts) if (a && a.kind === 'invite' && a.status === 'asked' && a.by && Number.isFinite(a.at)) {   // 0.72.6 (playtest 2, item 12): an invitation still waiting for your answer reminds you too, like an appointment
    const at = a.at, key = 'invite|' + a.id; if (at - R.ahead > t || at + 3 <= t) continue;
    const stage = t < at ? 'soon' : 'start', k = key + '|' + stage;
    if (devHeard(k) || (stage === 'soon' && at - t < 3)) continue;
    devHear(k);
    for (let i = HU_Q.length - 1; i >= 0; i--) if (HU_Q[i].key === key) HU_Q.splice(i, 1);
    let who = a.by; try { who = apptName(a.by); } catch (e) { /* the id */ }
    let where = ''; try { where = apptWhereName(a.where); } catch (e) { where = ''; }
    HU_Q.push({ key, stage, at, title: 'Invitation from ' + who, where, goal: devPlaceGoal(a.where) });
  }
  for (let i = HU_Q.length - 1; i >= 0; i--) { const h = HU_Q[i]; if (h.stage === 'soon' ? t >= h.at : t >= h.at + 10) { if (i === 0 && DEV.hu) { DEV.hu = null; DEVICE_SKIN.heads(null); } HU_Q.splice(i, 1); } }
  if (HU_Q.length > 4) HU_Q.splice(DEV.hu ? 1 : 0, HU_Q.length - 4);   // never a backlog: the newest four
  devHeadsShow(t);
}
function devHeadsShow(t = shipNow()) {
  if (DEV.hu || !HU_Q.length) return;
  if (devHuBusy()) return;
  const h = HU_Q[0], left = Math.max(1, Math.round(h.at - t));
  DEV.hu = h; DEVICE_SKIN.heads({ text: h.stage === 'soon' ? h.title + ' starts in ' + left + ' min' : h.title + (h.title === 'Your shift' ? ' starts now' : ' is starting'),
    where: h.where, soft: h.stage === 'start', go: !!h.goal });
}
function devHeadsReset() { SHIP.device.calendarRemind.heard = []; HU_Q.length = 0; DEV.hu = null; DEVICE_SKIN.heads(null); }   // a new game, and the checks
if (typeof onSim === 'function') onSim('newGame', () => {   // the clock starts again: nothing is heard yet; 0.35.37 (reviewer 1b): no appointments
  devHeadsReset(); SHIP.device.appts = []; DEV.notes = {};  // carry over from the last game (they'd list, remind and walk people to old times)
  try { apptDraft = null; apptSay = null; } catch (e) { /* not made yet */ }
});
function devHeadsBack() { if (DEV.hu) { DEV.hu = null; DEVICE_SKIN.heads(null); } }   // a tip or the address takes the top: the strip waits (still HU_Q[0])
function devHeadsDo(verb) {                              // the strip's taps: 'open' (the Schedule), 'go' (the goal arrow), 'done'
  const h = DEV.hu; if (!h) return; DEV.hu = null; HU_Q.shift(); DEVICE_SKIN.heads(null);
  if (verb === 'open') deviceShow('schedule');
  else if (verb === 'go' && h && h.goal && typeof setGoal === 'function') { SHIP.player.track = null; setGoal(h.goal); }
  if (verb === 'done') devHeadsShow();
}

function deviceApp(def) {
  if (!def || typeof def.id !== 'string') return;
  DEVICE_APPS.set(def.id, Object.assign({ title: def.id, icon: 'dot', order: 50 }, def));
  deviceRefresh();
}
function deviceDo(action) {
  if (!action) return;
  const a = DEVICE_APPS.get(action.app);
  if (action.do === 'open' || action.do === undefined) {   // open an app; one with no verb (e.g. { app, with }) hands the app the action
    let to = action.do === 'open' ? action.arg || action.app : action.app;   // an app's act may name another app to show (Maps → Roster)
    if (action.do === undefined && a && a.act) try { const r = a.act('open', action); if (typeof r === 'string' && DEVICE_APPS.has(r)) to = r; } catch (e) { DEV.errors.push(String(e && e.message || e)); }
    deviceShow(to); return;
  }
  try { if (a && a.act) a.act(action.do, action.arg); } catch (e) { DEV.errors.push(String(e && e.message || e)); }
  deviceRefresh();
}
// Quiet off shift (0.35.11, a setting): work notifications (DEV_WORK_APPS) are quiet badges, not toasts, when you're off shift
const DEV_WORK_APPS = new Set(['jobs', 'ship', 'record']);
const devOnShift = () => devShiftOn(SHIP.time.day) && SHIP.time.min >= DEV_SHIFT.from && SHIP.time.min < DEV_SHIFT.to;
function deviceNotify({ app, text, urgent } = {}) {
  if (urgent && SHIP.device.settings.quiet && DEV_WORK_APPS.has(app) && !devOnShift()) urgent = false;
  if (app) DEV.notes[app] = (DEV.notes[app] || 0) + 1;
  DEVICE_SKIN.notify({ app, text, urgent });
  deviceRefresh();
}
function deviceOn(ev, fn) { if (DEV.on[ev] && typeof fn === 'function') DEV.on[ev].push(fn); }
function deviceFire(ev) { for (const fn of DEV.on[ev] || []) try { fn(DEV.app); } catch (e) { DEV.errors.push(String(e && e.message || e)); } }
function deviceBadge(a) {
  let n = null; try { n = a.badge ? a.badge() : null; } catch (e) { n = null; }
  return (n || 0) + (DEV.notes[a.id] || 0) || null;
}
function deviceView(id) {                      // the app's VIEW, or a stand-in if it fails
  const a = DEVICE_APPS.get(id);
  if (!a) return { title: 'Your device', blocks: [{ kind: 'text', text: 'No such app.' }] };
  try { const v = a.view({ t: shipNow(), wide: DEVICE_SKIN.wide() }) || {}; return { title: v.title || a.title, blocks: v.blocks || [] }; }
  catch (e) { DEV.errors.push(id + ': ' + String(e && e.message || e)); return { title: a.title, blocks: [{ kind: 'text', text: '(this app failed to draw)' }] }; }
}
function deviceApps() { return [...DEVICE_APPS.values()].filter(a => a.id !== 'home' && !(a.hidden && devTry(a.hidden))).sort((a, b) => a.order - b.order || (a.id < b.id ? -1 : 1)); }
// the device before it's yours (0.35.21, Pillar 4): section 15's deviceLocked() (true on the arrival evening until Torres
// hands it over, section 21's flag 'intro.device'); while locked nothing opens it, and deviceLockedTap() says why.
// The first open after that is the first switch-on (the 'boot' screen, once; SHIP.device.booted, saved)
const devTry = f => { try { return !!f(); } catch (e) { return false; } };
// the ship's season (0.35.22, Pillar 4): section 18's seasonOf(d) -> { id, name, day, week }; null without it
const devSeason = d => { try { return typeof seasonOf === 'function' ? seasonOf(d) : null; } catch (e) { return null; } };
const devSeasonLine = d => { const s = devSeason(d); return s && s.name ? s.name + ', week ' + s.week + ' of 13' : null; };
const devLocked = () => { try { return typeof deviceLocked === 'function' && !!deviceLocked(); } catch (e) { return false; } };
function deviceShow(id) {
  if (!DEV.open && devLocked()) { try { if (typeof deviceLockedTap === 'function') deviceLockedTap(); } catch (e) { /* section 15's */ } return; }
  if (!DEV.open && !SHIP.device.booted && devTry(() => SHIP.intro && SHIP.intro.on && !SHIP.intro.skipped)) { SHIP.device.booted = true; id = 'boot'; }
  if (!DEVICE_APPS.has(id)) id = 'home';
  if (id !== 'settle') settleSure = false;               // 0.35.24 (reviewer 2): the end-the-welcome confirm never outlives the screen
  DEV.app = id; delete DEV.notes[id];
  if (!DEV.open) { DEV.open = true; DEVICE_SKIN.open(); deviceFrame(!DEVICE_SKIN.wide()); deviceFire('open');
    tipShow('device', 'Your device: Schedule and Calendar for your day, Maps to find your way, Jobs to track your work, Mail and Memos, Needs for how you feel.'); }
  deviceRefresh();
}
function deviceClose() { if (!DEV.open) return; DEV.open = false; DEVICE_SKIN.close(); deviceFrame(false); deviceFire('close'); }
// first tips (C13): tipShow(id, text) shows a tip once ever (SHIP.device.tipsSeen, saved), unless tips are off in
// Settings. The card never pauses anything; a tap or about 9 seconds closes it. One at a time; others wait their turn.
const TIP_Q = [];
function tipShow(id, text) {
  const D = SHIP.device; if (!id || !text || D.tipsSeen[id] || !D.settings.tips || TIP_Q.some(x => x.id === id)) return false;
  D.tipsSeen[id] = true; TIP_Q.push({ id, text }); if (TIP_Q.length === 1) DEVICE_SKIN.tip(TIP_Q[0]);
  return true;
}
// tipSeen(id) (0.35.26, for section 21): marks a tip as seen without showing it, so the intro can skip tips a person
// has already taught. A tip waiting its turn is dropped; one on screen stays. True if it wasn't seen before.
function tipSeen(id) {
  const D = SHIP.device; if (!id || typeof id !== 'string' || id.length >= 40) return false;
  const i = TIP_Q.findIndex(x => x.id === id); if (i > 0) TIP_Q.splice(i, 1);
  if (D.tipsSeen[id]) return false; D.tipsSeen[id] = true; return true;
}
function tipDone() { TIP_Q.shift(); if (TIP_Q.length) DEVICE_SKIN.tip(TIP_Q[0]); else DEVICE_SKIN.tip(null); }
// the camera's framing on a phone (C11): while the sheet covers the bottom two thirds, the view eases down so you
// stay in the visible top part, and eases back on close. deviceFrame(on); the eased amount (0 to 1) is DEV.fr.
// It only shifts the camera's projection (top and bottom), by whole pixels, and leaves it alone at 0.
DEV.fr = 0; DEV.frOn = false;
function deviceFrame(on) { DEV.frOn = !!on; }
let devFrameT = 0;
function deviceFrameStep(now) {
  requestAnimationFrame(deviceFrameStep);
  devPulseStep();
  const dt = Math.min(.1, Math.max(0, (now - (devFrameT || now)) / 1000)); devFrameT = now;
  const want = DEV.frOn ? 1 : 0; if (DEV.fr === want && !DEV.frApplied) return;
  DEV.fr += (want - DEV.fr) * Math.min(1, dt * 6); if (Math.abs(want - DEV.fr) < .002) DEV.fr = want;
  if (typeof camera === 'undefined' || typeof renderer === 'undefined') return;
  const vh = camera.top - camera.bottom, px = vh / Math.max(1, renderer.domElement.height), off = Math.round(.33 * vh * DEV.fr / px) * px;
  camera.top = vh / 2 - off; camera.bottom = -vh / 2 - off; camera.updateProjectionMatrix();
  DEV.frApplied = off !== 0;
}
requestAnimationFrame(deviceFrameStep);
// ---- the meeting dialogue panel (Part 2, "meetings with dialogue"): section 18 owns the scripts and their flow
// (advancing, replies, walking away); this only draws and reports taps. deviceDialogue(view, onTap): view = { title,
// name or who (a name), text, to, pose, choices: null | [text], i, n }; onTap() goes on, onTap(k) picks reply k; with
// no onTap the taps call section 18's dialogueNext() and dialogueChoose(k). null closes it.
// the Captain's ship-wide address (section 18's captainAddress calls this first): a banner across the top in the
// screen's style, about 20 real seconds, a tap dismisses it. deviceAddress(null) hides it.
function deviceAddress(a) { DEVICE_SKIN.address(a && a.text ? a : null); return true; }
let devDlgTap = null;
function deviceDialogue(v, onTap) {
  if (DEV.choose) { const f = DEV.choose; DEV.choose = null; try { f(-1); } catch (e) { /* the asker's */ } }   // 0.35.25: a meeting takes the panel; a pending question is Not now
  devDlgTap = v && typeof onTap === 'function' ? onTap : null;
  if (v && !v.name && v.who) { const p = typeof ROSTER !== 'undefined' ? ROSTER.find(x => x.id === v.who) : null; v = { ...v, name: p ? p.name : String(v.who) }; }
  DEVICE_SKIN.dialogue(v || null);
  return true;
}
// deviceChoose(view, onPick) (0.35.23, Pillar 4): a question with buttons in the meeting panel's style, e.g. section 13's
// New game: { title, text, choices: [label, ...], cancel } (cancel: the last button's label, 'Not now' by default, false
// for none). onPick(k) gets the index of the choice, or -1 for Not now or the ×. One question at a time.
// 0.35.25 (reviewer 2): it shares the panel with section 18's meetings, so it refuses (returns false) while the panel or
// a meeting is up, and a meeting drawn over a question cancels the question first (deviceDialogue)
function deviceChoose(v, onPick) {
  if (!v || !Array.isArray(v.choices) || !v.choices.length || DEV.choose) return false;
  const panel = document.getElementById('devDlg'); if (panel && !panel.hidden) return false;
  try { if (typeof DIALOGUE !== 'undefined' && DIALOGUE) return false; } catch (e) { /* section 18 not loaded */ }
  const n = v.choices.length, choices = v.choices.map(String).concat(v.cancel === false ? [] : [v.cancel || 'Not now']);
  deviceDialogue({ title: v.title || 'Choose', name: '', text: v.text || '', choices }, k => devChosen(k < n ? k : -1));
  DEV.choose = typeof onPick === 'function' ? onPick : () => {};
  return true;
}
function devChosen(k) {
  const f = DEV.choose; DEV.choose = null; devDlgTap = null; DEVICE_SKIN.dialogue(null);
  if (f) try { f(k); } catch (e) { DEV.errors.push('deviceChoose: ' + (e && e.message || e)); }
}
function devDialogueDo(what, k) {
  try {
    if (what === 'close' && DEV.choose) { devChosen(-1); return; }   // the × on a question: Not now
    if (what === 'close') { DEVICE_SKIN.dialogue(null); devDlgTap = null; if (typeof dialogueClose === 'function') dialogueClose(); return; }
    if (devDlgTap) devDlgTap(what === 'choose' ? k : undefined);
    else if (what === 'choose' && typeof dialogueChoose === 'function') dialogueChoose(k);   // section 18's own flow (0.34.10)
    else if (what === 'next' && typeof dialogueNext === 'function') dialogueNext();
    else DEVICE_SKIN.dialogue(null);
  } catch (e) { DEV.errors.push('dialogue: ' + (e && e.message || e)); DEVICE_SKIN.dialogue(null); }
}
function deviceRefresh() {
  deviceTick();
  DEVICE_SKIN.button();
  if (DEV.open) DEVICE_SKIN.draw(DEV.app, deviceView(DEV.app));
}

// ---- the skin: the only DOM code. It draws a VIEW into #devBody, the home grid, the button's badge. ----
const DEVICE_SKIN = (() => {
  const $ = id => document.getElementById(id);
  const el = $('device'), body = $('devBody'), btn = $('devBtn'), badge = $('devMail'), head = $('devT'), backB = $('devBack'), led = $('devLed');
  const GLYPH = { hobby: '✿', home: '⌂', needs: '♥', wrench: '⚒', mail: '✉', wallet: '¤', schedule: '◷', calendar: '▦', memo: '✎', map: '⌖', ship: '◈', news: '☰', record: '★', crew: '☺', people: '♡', gear: '✲', dot: '•', track: '◎' };
  const mk = (tag, cls, txt) => { const e = document.createElement(tag); if (cls) e.className = cls; if (txt != null) e.textContent = txt; return e; };
  const act = (b, action) => { b.type = 'button'; b.onclick = e => { e.stopPropagation(); deviceDo(action); }; return b; };
  let back = null, drawn = null, drawnKey = null, mapCache = null;
  const layout = () => {                       // phone: a sheet over the bottom two thirds; wide (an unfolded TriFold, a desktop): a side panel
    const st = SHIP.device.settings, w = skin.wide();
    el.classList.toggle('wide', w); el.dataset.ph = st.phosphor; el.classList.toggle('fx', !!st.fx);
    document.body.classList.toggle('devsheet', DEV.open && !w);
  };
  const blocks = {
    text(b) { return mk('p', b.mark ? (b.mark === 'up' || b.mark === 'down' ? 'fx ' + b.mark : b.mark) : '', b.text); },
    list(b) {
      const box = mk('div', 'list');
      for (const r of b.rows || []) {
        const whole = r.action && !r.button, row = mk(whole ? 'button' : 'div', 'row' + (r.mark ? ' ' + r.mark : ''));
        row.appendChild(mk('span', 'rt', r.text));
        if (r.sub) row.appendChild(mk('small', '', r.sub));
        if (whole) act(row, r.action);
        if (r.button) row.appendChild(act(mk('button', 'act', r.button), r.action));
        box.appendChild(row);
      }
      return box;
    },
    bars(b) {
      const box = mk('div', 'bars');
      for (const it of b.items || []) {
        const row = mk('div', 'need' + (it.level ? ' ' + it.level : '') + (it.pulse ? ' pulse' : '') + (it.icon ? ' ic' : '') + (it.color ? ' tint' : '')), lab = mk('span', '', it.label), bar = mk('i'), fill = mk('b'), v = Math.max(0, Math.min(100, +it.value || 0));
        fill.style.width = v.toFixed(1) + '%';
        if (it.color) row.style.setProperty('--nc', it.color);   // 0.35.28: a need's own colour (section 15's NEED_COL), as on the strip
        if (it.icon) { const NS = 'http://www.w3.org/2000/svg', svg = document.createElementNS(NS, 'svg'), path = document.createElementNS(NS, 'path');
          svg.setAttribute('viewBox', '0 0 24 24'); svg.setAttribute('aria-hidden', 'true'); path.setAttribute('d', it.icon); svg.appendChild(path); row.appendChild(svg); }
        if (it.mark) { const em = mk('em', it.mark, it.mark === 'up' ? '▲' : '▼'); if (it.note) em.title = it.note; em.setAttribute('aria-label', it.mark === 'up' ? 'bonus' : 'penalty'); lab.appendChild(em); }
        row.setAttribute('role', 'meter'); row.setAttribute('aria-label', it.label); row.setAttribute('aria-valuenow', Math.round(v));
        row.setAttribute('aria-valuemin', 0); row.setAttribute('aria-valuemax', 100);
        bar.appendChild(fill); row.append(lab, bar, mk('span', '', Math.round(v))); box.appendChild(row);
      }
      return box;
    },
    timeline(b) {                              // 0.34.51 (the Calendar): rows of blocks on a day's time bar, from..to minutes
      const box = mk('div', 'tl'), span = Math.max(1, b.to - b.from), pc = m => (Math.max(0, Math.min(span, m - b.from)) / span * 100).toFixed(2) + '%';
      for (const lane of b.rows || []) {                 // each block a bar, its name above it, running on to the next block in the row
        const row = mk('div', 'tl-row'), l = lane.slice().sort((x, y) => x.a - y.a);
        l.forEach((x, i) => {
          const s = mk('span', 'tl-blk' + (x.past ? ' past' : '')), n = mk('span', 'tl-lab' + (x.past ? ' past' : ''), x.label), next = l[i + 1] ? l[i + 1].a : b.to;
          s.style.left = n.style.left = pc(x.a); s.style.width = 'calc(' + pc(x.b) + ' - ' + pc(x.a) + ')'; n.style.maxWidth = 'calc(' + pc(next) + ' - ' + pc(x.a) + ' - 2px)'; n.title = x.label;
          row.append(s, n);
          const fit = k => setTimeout(() => {   // too tight for the name: its first word, else none (the list below has it)
            if (!n.isConnected) { if (k < 5) fit(k + 1); return; }   // drawn before the page is on screen: wait for it
            if (n.scrollWidth > n.clientWidth + 1) n.textContent = x.label.split(/[\s-]/)[0];
            if (n.scrollWidth > n.clientWidth + 1) n.textContent = '';
          }, 0);
          fit(0);
        });
        box.appendChild(row);
      }
      if (b.ticks) { const tk = mk('div', 'tl-ticks'); for (const s of b.ticks) tk.appendChild(mk('span', '', s)); box.appendChild(tk); }
      return box;
    },
    strip(b) {                                 // 0.55.14 (P1's day strip): a row per machine, a bar per hour of how it ran, the pinned hours outlined
      const box = mk('div', 'strip');
      for (const r of b.rows || []) {
        const row = mk('div', 'st-row'), bars = mk('div', 'st-bars'), pins = new Set(r.pins || []);
        (r.hours || []).slice(0, 24).forEach((v, h) => { const x = Math.max(0, Math.min(1, +v || 0)), c = mk('span', 'st-h' + (x < .8 ? ' low' : '') + (pins.has(h) ? ' pin' : ''));
          c.style.height = Math.round(4 + 28 * x) + 'px'; c.title = String(h).padStart(2, '0') + ':00'; bars.appendChild(c); });
        row.append(mk('div', 'st-lab', r.label || ''), bars); box.appendChild(row);
      }
      const tk = mk('div', 'st-ticks'); for (const t of ['00', '06', '12', '18', '24']) tk.appendChild(mk('span', '', t)); box.appendChild(tk);
      return box;
    },
    chips(b) {                                 // 0.55.0 (the case engine's suspects): big toggles, crossed out while on is false
      const box = mk('div', 'chips');
      for (const it of b.items || []) { const x = act(mk('button', 'chip' + (it.on === false ? ' off' : ''), it.label), it.action); x.setAttribute('aria-pressed', it.on !== false); box.appendChild(x); }
      return box;
    },
    buttons(b) { const box = mk('div', 'btns'); for (const it of b.items || []) { const x = act(mk('button', 'act' + (it.on ? ' on' : ''), it.label), it.action); if (it.on != null) x.setAttribute('aria-pressed', !!it.on); box.appendChild(x); } return box; },
    map(b) {                                   // a deck plan as SVG (DOM, not a canvas): room runs, walls, you, the pick and the goal
      // 0.35.14 (the performance engineer's advice): the plan is kept while its deck, rooms, pick and goal stay the same,
      // and only the dots (people, you) are drawn again, so a ship minute with Maps open costs a few circles
      const NS = 'http://www.w3.org/2000/svg', g = b.grid || [], H = g.length, W = Math.max(0, ...g.map(r => r.length)), at = (i, j) => (g[j] || '')[i] || '.';
      const sv = (tag, a) => { const e = document.createElementNS(NS, tag); for (const k in a) e.setAttribute(k, a[k]); return e; };
      const dots = svg => {
        const old = svg.querySelector('g.m-dots'); if (old) old.remove();
        const dg = sv('g', { class: 'm-dots' });
        for (const q of b.people || []) { const c = sv('circle', { cx: q.x + .5, cy: q.y + .5, r: .62, class: 'm-per' + (q.pick ? ' pick' : '') }); c.dataset.who = q.id; dg.appendChild(c); }
        if (b.you) dg.appendChild(sv('circle', { cx: b.you[0] + .5, cy: b.you[1] + .5, r: .9, class: 'm-you' }));
        svg.appendChild(dg);
        svg.onclick = e => { const ds = e.target && e.target.dataset || {}, k = ds.room;
          if (ds.who && b.whoAction) { e.stopPropagation(); deviceDo({ ...b.whoAction, arg: ds.who }); } else if (k && b.action) { e.stopPropagation(); deviceDo({ ...b.action, arg: k }); } };
        return svg;
      };
      const pk = JSON.stringify([b.rooms, b.pick, b.goal, b.marks || null]);
      if (mapCache && mapCache.grid === g && mapCache.key === pk) return dots(mapCache.svg);
      const svg = sv('svg', { viewBox: '-0.5 -0.5 ' + (W + 1) + ' ' + (H + 1), class: 'devmap', role: 'img', 'aria-label': 'Deck plan' });
      const pat = sv('pattern', { id: 'devhatch', patternUnits: 'userSpaceOnUse', width: .8, height: .8, patternTransform: 'rotate(45)' });
      pat.appendChild(sv('rect', { width: .8, height: .8, class: 'm-hbg' })); pat.appendChild(sv('line', { x1: 0, y1: 0, x2: 0, y2: .8, class: 'm-hl' }));
      const defs = sv('defs', {}); defs.appendChild(pat); svg.appendChild(defs);
      for (let j = 0; j < H; j++) for (let i = 0; i < W;) {
        const k = at(i, j); let e = i; while (e < W && at(e, j) === k) e++;
        const r = b.rooms[k];
        if (k !== '.' && r) { const x = sv('rect', { x: i, y: j, width: e - i, height: 1, class: 'm-' + r.kind + (k === b.pick ? ' pick' : '') + (k === b.goal ? ' goal' : '') }); x.dataset.room = k; svg.appendChild(x); }
        i = e;
      }
      let d = '';
      for (let j = -1; j < H; j++) for (let i = -1; i < W; i++) {
        const k = at(i, j);
        if (k !== at(i + 1, j) && (k !== '.' || at(i + 1, j) !== '.')) d += 'M' + (i + 1) + ' ' + j + 'v1';
        if (k !== at(i, j + 1) && (k !== '.' || at(i, j + 1) !== '.')) d += 'M' + i + ' ' + (j + 1) + 'h1';
      }
      svg.appendChild(sv('path', { d, class: 'm-wall' }));
      for (const t of Array.isArray(b.marks) ? b.marks : []) if (Array.isArray(t)) svg.appendChild(sv('rect', { x: t[0] - .45, y: t[1] - .45, width: 1.9, height: 1.9, class: 'm-mark' }));   // marks: [[i, j], ...] (24i's line)
      mapCache = { grid: g, key: pk, svg };
      return dots(svg);
    },
    form(b) {                                  // text fields; the submit action gets { field id: value }
      const box = mk('form', 'devform'), ins = {};
      for (const f of b.fields || []) {
        const lab = mk('label', '', f.label), x = mk(f.multiline ? 'textarea' : 'input');
        if (!f.multiline) x.type = 'text'; x.value = f.value || ''; x.maxLength = f.multiline ? 2000 : 80; if (f.multiline) x.rows = 5;
        ins[f.id] = x; lab.appendChild(x); box.appendChild(lab);
      }
      const row = mk('div', 'btns'), ok = mk('button', 'act', b.submit ? b.submit.label : 'OK'); ok.type = 'submit'; row.appendChild(ok);
      if (b.cancel) row.appendChild(act(mk('button', 'act', b.cancel.label), b.cancel.action));
      box.appendChild(row);
      box.onsubmit = e => { e.preventDefault(); const v = {}; for (const k in ins) v[k] = ins[k].value; if (b.submit) deviceDo({ ...b.submit.action, arg: v }); };
      return box;
    },
    dom(b) { const box = mk('div'); try { b.render(box); } catch (e) { box.textContent = '(this section failed to draw)'; } return box; },   // the addSection shim
  };
  const INK = { amber: '#ffb347', green: '#5dff8a', cyan: '#6ff0dc' };   // --crt-ink per phosphor, for the 3D prop (section 8b)
  const skin = {
    get ink() { return INK[SHIP.device.settings.phosphor] || INK.cyan; },
    wide: () => innerWidth > innerHeight * 1.15 && innerWidth >= 720,
    has: kind => !!blocks[kind],               // 0.55.0: which VIEW blocks this skin draws (devChips asks)
    open() { back = document.activeElement; el.hidden = false; layout(); $('devClose').focus(); },
    close() { el.hidden = true; drawn = null; drawnKey = null; layout(); if (back && back.focus) back.focus(); },
    button() {
      let low = false; try { low = NEED_KEYS.some(k => SHIP.player.needs[k] < SLOW_BELOW); } catch (e) { /* before section 15 */ }
      btn.classList.toggle('low', low);
      let un = 0; try { un = mailUnread(); } catch (e) { /* before section 15 */ }
      if (devLocked()) un = 0;                          // no mail badge on a device you haven't got yet
      if (badge && (badge.hidden !== !un || badge.textContent !== String(un))) { badge.hidden = !un; badge.textContent = un; if (typeof pausePlace === 'function') pausePlace(); }   // Pause sits beside the button (0.28.59)
      led.classList.toggle('on', un > 0); led.classList.toggle('blink', un > 0);   // the power light blinks for new mail
    },
    draw(id, v) {
      if (drawn === id && body.contains(document.activeElement) && /^(INPUT|TEXTAREA)$/.test(document.activeElement.tagName)) return;   // typing: leave it be
      // nothing changed since the last draw (most ship minutes): leave the screen be, as rebuilding the glowing text costs
      // phones the most (0.35.12). Views holding a dom block (the shim) always redraw; home adds its badges
      let key = null;
      try { key = v.blocks.some(b => b && b.kind === 'dom') ? null : id + JSON.stringify(v) + (id === 'home' ? deviceApps().map(a => a.id + ':' + deviceBadge(a)).join() : ''); } catch (e) { key = null; }
      if (key && key === drawnKey && drawn === id) { layout(); return; }
      drawnKey = key;
      const keep = drawn === id ? body.scrollTop : 0;
      layout(); head.textContent = id === 'home' ? 'Your device' : v.title; backB.disabled = id === 'home';
      body.textContent = ''; body.dataset.app = id;
      for (const b of v.blocks) { const f = blocks[b && b.kind]; if (f) body.appendChild(f(b)); }
      if (id === 'home') {                     // the app grid, with badges
        const grid = mk('div', 'apps');
        for (const a of deviceApps()) {
          const t = act(mk('button', 'app'), { app: a.id, do: 'open' }), n = deviceBadge(a);
          t.dataset.app = a.id; t.append(mk('i', '', (GLYPH[a.icon] || GLYPH.dot) + '︎'), mk('span', '', a.short || a.title));
          if (n) t.appendChild(mk('b', '', n));
          t.setAttribute('aria-label', a.title + (n ? ', ' + n + ' new' : ''));
          grid.appendChild(t);
        }
        body.appendChild(grid);
      }
      body.scrollTop = keep; drawn = id;
    },
    tip(t) {                                   // the tip card, in the screen's style; null hides it
      let c = $('devTip');
      if (!c) { c = mk('div', 'devtip'); c.id = 'devTip'; c.setAttribute('role', 'status'); c.hidden = true; document.body.appendChild(c); c.onclick = () => tipDone(); }
      simClear(c._t); c.hidden = !t; if (!t || document.body.classList.contains('dlgon')) return;   // no tips over a meeting
      devHeadsBack(); c.dataset.ph = SHIP.device.settings.phosphor; c.textContent = ''; c.append(mk('b', '', 'TIP'), mk('span', '', t.text));
      c._t = simTimeout(() => tipDone(), 9000);   // section 13's frozen clock (0.28.50): a pause holds it
    },
    dialogue(v) {                              // the meeting panel: a strip across the bottom, in the screen's style
      let c = $('devDlg');
      if (!c) {
        c = mk('div', 'devdlg'); c.id = 'devDlg'; c.setAttribute('role', 'dialog'); c.setAttribute('aria-live', 'polite'); c.hidden = true; document.body.appendChild(c);
        c.addEventListener('pointerdown', e => e.stopPropagation());   // taps on the panel never reach the deck
      }
      c.hidden = !v; document.body.classList.toggle('dlgon', !!v);
      if (!v) { if (TIP_Q.length) skin.tip(TIP_Q[0]); return; }   // a tip waiting behind the meeting comes back
      c.dataset.ph = SHIP.device.settings.phosphor; c.textContent = '';
      const x = mk('button', 'x', '×'); x.type = 'button'; x.setAttribute('aria-label', 'Walk away'); x.onclick = e => { e.stopPropagation(); devDialogueDo('close'); };
      c.append(x, mk('small', '', (v.title ? v.title.toUpperCase() + (v.name ? ' · ' : '') : '') + (v.name || '') + (v.n ? ' · ' + ((v.i || 0) + 1) + '/' + v.n : '')));
      if (v.text) { const t = mk('p', '', v.text); c.appendChild(t); }
      if (v.choices && v.choices.length) {
        const box = mk('div', 'btns');
        v.choices.forEach((ch, k) => { const b = mk('button', 'act', ch); b.type = 'button'; b.onclick = e => { e.stopPropagation(); devDialogueDo('choose', k); }; box.appendChild(b); });
        c.appendChild(box);
      } else { const n = mk('button', 'act next', 'Go on ▸'); n.type = 'button'; n.onclick = e => { e.stopPropagation(); devDialogueDo('next'); }; c.appendChild(n); }
    },
    address(a) {
      let c = $('devAddr');
      if (!c) { c = mk('div', 'devaddr'); c.id = 'devAddr'; c.setAttribute('role', 'status'); c.setAttribute('aria-live', 'polite'); c.hidden = true; document.body.appendChild(c);
        c.addEventListener('pointerdown', e => e.stopPropagation()); c.onclick = () => skin.address(null); }
      simClear(c._t); c.hidden = !a; if (!a) return;
      devHeadsBack(); c.dataset.ph = SHIP.device.settings.phosphor; c.textContent = '';
      c.append(mk('small', '', ((a.from || 'The Captain') + ', to all hands').toUpperCase()), mk('p', '', a.text));
      c._t = simTimeout(() => skin.address(null), 20000);
    },
    chat(el, v) {                              // section 20's chat card (CHAT_SKIN.draw), in the screen's style
      el.className = 'devchat'; el.dataset.ph = SHIP.device.settings.phosphor; el.textContent = '';
      const x = mk('button', 'x', '×'); x.type = 'button'; x.setAttribute('aria-label', 'Close'); x.onclick = () => chatClose();
      el.append(x, mk('b', '', v.who), mk('small', '', [v.role, v.tier].filter(Boolean).join(' · ')), mk('p', v.say ? '' : 'feel', v.say ? '"' + v.line + '"' : v.line));
      const row = mk('div', 'btns');
      for (const b of v.buttons || []) { const e = mk('button', 'act', b.label); e.type = 'button'; e.disabled = !!b.off; e.onclick = () => chatDo(b.id); row.appendChild(e); }
      el.appendChild(row);
    },
    heads(h) {                                 // 0.35.29: the heads-up strip at the screen's right edge; null hides it
      let c = $('devHu');
      if (!c) { c = mk('div', 'devhu'); c.id = 'devHu'; c.setAttribute('role', 'status'); c.setAttribute('aria-live', 'polite'); c.hidden = true; document.body.appendChild(c);
        c.addEventListener('pointerdown', e => e.stopPropagation()); c.onclick = () => devHeadsDo('open'); }
      simClear(c._t); c.hidden = !h; if (!h) return;
      c.dataset.ph = SHIP.device.settings.phosphor; c.classList.toggle('soft', !!h.soft); c.textContent = '';
      const tx = mk('span', '', ''); tx.append(mk('b', '', h.text), mk('small', '', h.where || '')); c.appendChild(tx);
      if (h.go) { const g = mk('button', 'act', 'Go there'); g.type = 'button'; g.onclick = e => { e.stopPropagation(); devHeadsDo('go'); }; c.appendChild(g); }
      c.style.top = ''; const me = c.getBoundingClientRect(); let top = me.top;   // 0.35.31: below section 15's needs strip and activity bar when they'd overlap (a phone)
      for (const id of ['needStrip', 'actBar', 'trkBtn']) { const e = document.getElementById(id); if (!e || e.hidden || !e.offsetWidth) continue;   // 0.72.0: and the Tracked button
        const r = e.getBoundingClientRect(); if (r.right > me.left && r.left < me.right && r.bottom + 8 > top) top = r.bottom + 8; }
      if (top !== me.top) c.style.top = Math.round(top) + 'px';
      c._t = simTimeout(() => devHeadsDo('done'), h.soft ? 6000 : 9000);
    },
    notify(n) { if (n && n.urgent && n.text) toast(n.app && DEVICE_APPS.has(n.app) ? DEVICE_APPS.get(n.app).title : 'Your device', n.text); },
  };
  btn.onclick = () => (DEV.open ? deviceClose() : deviceShow('home'));
  $('devClose').onclick = deviceClose;
  backB.onclick = () => deviceShow('home'); $('devHome').onclick = () => deviceShow('home');
  addEventListener('keydown', e => { if (e.key === 'Escape' && DEV.open) deviceClose(); });
  addEventListener('resize', () => { if (DEV.open) layout(); });
  // 0.35.15 (the user: "sometimes it just pops up"): only the Device button opens it. The swipe up from the bottom edge
  // is gone, as a drag that began low on the screen (steering) opened it. On a phone a swipe down on the bezel or a
  // tap on the ship closes it.
  // 0.35.12 (the phone review): the ship closes it on a tap (lifted within 12px and 0.4 s), not at the first touch, so a
  // drag or a pinch over the ship doesn't close it (it doesn't steer or zoom either while the sheet is up); a cancelled
  // touch (the phone took the gesture) forgets the swipe
  let swipe = null;
  addEventListener('pointerdown', e => {
    const cv = e.target && e.target.tagName === 'CANVAS';
    if (DEV.open && !skin.wide() && e.target.closest && e.target.closest('#devBez')) swipe = { y: e.clientY, open: false };
    else if (DEV.open && !skin.wide() && cv) { e.stopPropagation(); swipe = { x: e.clientX, y: e.clientY, tap: performance.now() }; }
  }, true);
  addEventListener('pointerup', e => {
    if (!swipe) return; const dy = e.clientY - swipe.y;
    if (swipe.tap) { if (Math.hypot(e.clientX - swipe.x, dy) < 12 && performance.now() - swipe.tap < 400) { e.stopPropagation(); deviceClose(); } }
    else if (dy > 40) deviceClose();
    swipe = null;
  }, true);
  addEventListener('pointercancel', () => { swipe = null; }, true);
  return skin;
})();

// a chips block for an app's view (0.55.0); a skin without chips gets the same toggles as buttons, "✕ " on the crossed ones
function devChips(items) {
  if (DEVICE_SKIN.has && DEVICE_SKIN.has('chips')) return { kind: 'chips', items };
  return { kind: 'buttons', items: items.map(it => ({ label: (it.on === false ? '✕ ' : '') + it.label, action: it.action })) };
}

// a day strip for an app's view (0.55.14); a skin without strips gets a list: each row's label and its words (fallback(row))
function devStrip(rows, fallback) {
  if (DEVICE_SKIN.has && DEVICE_SKIN.has('strip')) return { kind: 'strip', rows };
  return { kind: 'list', rows: rows.map(r => ({ text: r.label + (fallback ? ': ' + fallback(r) : '') })) };
}

// ---- the shim: the old device object. addSection(id, title, render) becomes an app drawn by render(el); an app
// already registered with deviceApp keeps its id (the native one wins). show('status') is the home screen. ----
const device = {
  addSection(id, title, render) {
    const a = DEVICE_APPS.get(id); if (a && !a.legacy) return;
    deviceApp({ id, title, order: 70, legacy: true, view: () => ({ title, blocks: [{ kind: 'dom', render }] }) });
  },
  open(id) { deviceShow(id || 'home'); },
  close() { deviceClose(); },
  show(id) { deviceShow(id === 'status' ? 'home' : id); },
  refresh() { deviceRefresh(); },
  get isOpen() { return DEV.open; },
  get tab() { return DEV.app; },
};

// ---- the apps. Home: the time and what you're doing (the old Now section), then the grid. ----
// the first switch-on (0.35.21): shown once, the first time it opens after Torres hands it over; not on the home grid
deviceApp({ id: 'boot', title: 'Crew device', order: -1, hidden: () => true, view: () => {
  const name = (SHIP.player && SHIP.player.name) || 'Cadet';
  return { title: 'Crew device', blocks: [{ kind: 'text', text: 'CSV WREN CREW DEVICE', mark: 'big' }, { kind: 'text', text: 'Assigned to: ' + name + '.', mark: 'hot' },
    { kind: 'text', text: 'Works department, Bunk 1, Deck 4.' }, { kind: 'text', text: 'Your day, your mail, the ship and its people, in one place. Settling in lists what to learn this week.' },
    { kind: 'buttons', items: [{ label: 'Start', action: { app: 'home', do: 'open' } }] }] };
} });
// Settling in (0.35.21, Pillar 4): section 21's SETTLE list, each item ticked when you've done it (SHIP.intro.settle[id],
// a ship minute), naming who can teach it; Go there points the arrow at its place, or at the teacher (where the Roster
// says they are). "I know my way around" ends the welcome (introEnd, after a second tap). Hidden without section 21,
// before any intro and once the list is all done (SHIP.intro.settle.all)
let settleSure = false;
const settleList = () => { try { return typeof SETTLE !== 'undefined' && Array.isArray(SETTLE) ? SETTLE : null; } catch (e) { return null; } };
const settleDone = id => !!(SHIP.intro && SHIP.intro.settle && SHIP.intro.settle[id] !== undefined);
function settleGoal(it) {                                // { deck, room, label } for an item, or null
  if (it.place && it.place.deck && it.place.room) return { deck: it.place.deck, room: it.place.room, label: it.title + ': ' + it.place.room };
  const p = it.teacher && apptPerson(it.teacher), w = p && rosterWhere(p);
  return w && w.room ? { deck: w.deck, room: w.room, label: it.title + ': ' + p.name.split(' ')[0] } : null;
}
deviceApp({ id: 'settle', title: 'Settling in', short: 'Settling', icon: 'record', order: 5,
  hidden: () => !settleList() || !SHIP.intro || !(SHIP.intro.on || SHIP.intro.skipped) || !!(SHIP.intro.settle && SHIP.intro.settle.all),
  badge: () => null,
  act(verb, arg) {
    if (verb === 'go' && typeof setGoal === 'function') {
      const it = (settleList() || []).find(x => x.id === arg), g = it && settleGoal(it); if (!g) return;
      SHIP.player.track = null; setGoal(g); deviceNotify({ app: 'settle', text: 'Follow the marker: ' + g.label + '.', urgent: true }); delete DEV.notes.settle;
    }
    else if (verb === 'end') { if (!settleSure) settleSure = true; else { settleSure = false; if (typeof introEnd === 'function') introEnd(false); } }
  },
  view: () => {
    const L = settleList() || [], done = L.filter(x => settleDone(x.id)).length, B = [];
    B.push({ kind: 'text', text: done + ' of ' + L.length + ' done. Nothing here is required: people will show you as the week goes on.', mark: 'hot' });
    const rows = L.map(it => { const d = settleDone(it.id), p = it.teacher && apptPerson(it.teacher), g = !d && settleGoal(it);
      return { text: (d ? '✓ ' : '') + it.title, sub: d ? 'Done' : (p ? 'Ask ' + p.name : '') + (it.place ? (p ? ' · ' : '') + it.place.room + ', ' + deckIn(it.place.deck) : ''),
        mark: d ? 'past' : null, button: g ? 'Go there' : null, action: g ? { app: 'settle', do: 'go', arg: it.id } : null }; });
    B.push({ kind: 'list', rows });
    if (devTry(() => typeof introOn === 'function' && introOn()))
      B.push({ kind: 'buttons', items: [{ label: settleSure ? 'Tap again to end the welcome' : 'I know my way around', action: { app: 'settle', do: 'end' } }] });
    return { title: 'Settling in', blocks: B };
  } });

deviceApp({ id: 'home', title: 'Home', icon: 'home', order: 0, view: () => {
  const B = [{ kind: 'text', text: clockText(), mark: 'big' }], sn = devSeasonLine(SHIP.time.day);
  if (sn) B.push({ kind: 'text', text: 'Season: ' + sn + '.' });
  const say = text => B.push({ kind: 'text', text }), dn = devNow(), t = shipNow(), today = devTraditions(t, SHIP.time.day * 1440 - 1);
  B.push({ kind: 'text', text: dn.now + (dn.next ? '. ' + dn.next + '.' : '.'), mark: 'hot' });
  if (today.length) say('Today aboard' + (today.length > 1 ? ', ' + today.length + ' traditions' : '') + ': ' + today.map(x => x.title + ' at ' + devWhen(x.at)).join(', ') + '.');   // 0.34.51: how many, then each
  say(ACT && ACT.phase !== 'walk' ? ACT.kind === 'queue' ? 'In the queue for the servery.'   // 0.35.27: no guessed wait (the user: no invented numbers)
    : (ACT.o.title || ACT.def.title) + (ACT.def.need ? ': ' + Math.max(0, Math.ceil((ACT.def.mins - ACT.done) / needEffects().task)) + ' min to go.' : '.') : needsLine());
  const P = SHIP.player, w = P.work, mj = jobsOn() ? myJob() : null;
  if (P.carry.length) say('Carrying: ' + P.carry.join(', ') + '.');
  if (P.cart) say('Pushing a hover cart (' + (P.cart.stage === 'full' ? 'loaded' : 'empty') + '). ' + (CART_STEP[P.cart.stage] || (mj ? 'Take the load to ' + cartDest(mj).name + '.' : '')));
  if (mj && w && w.job === mj.id && (w.fitted.length || w.done)) say('Your job: ' + w.fitted.length + ' of ' + mj.parts.length + ' parts fitted' + (w.done ? ', ' + Math.floor(w.done) + ' of ' + Math.round(jobMins(mj)) + ' min of repair done' : '') + '.');
  for (const nt of (playerFx().notes || []).slice(0, 2)) if (nt && nt.text) say(nt.text + '.');
  const sl = settleList(), sa = DEVICE_APPS.get('settle');
  if (sl && sa && !devTry(sa.hidden)) say('Settling in: ' + sl.filter(x => settleDone(x.id)).length + ' of ' + sl.length + ' done.');
  const pin = SHIP.device.memos.find(x => x.pinned);
  if (pin) say('▪ ' + pin.title + (pin.text ? ': ' + pin.text.slice(0, 120) : ''));
  const idea = typeof ideasTonight === 'function' ? devTry(ideasTonight) : null;   // "Ideas for tonight" (0.28.63, section 15)
  if (idea && idea.length) { B.push({ kind: 'text', text: idea[0], mark: 'head' }); for (const x of idea.slice(1)) say('▪ ' + x); }
  return { title: 'Home', blocks: B };
} });

// Schedule: today as a timeline, with where you're expected right now; tomorrow below. A day picked in the Calendar
// (0.35.10: { app: 'schedule', day }) shows instead of tomorrow until the device closes.
let schedDay = null;
deviceOn('close', () => { schedDay = null; if (typeof mapFor !== 'undefined') mapFor = null; if (typeof settleSure !== 'undefined') settleSure = false; });
deviceApp({ id: 'schedule', title: 'Schedule', icon: 'schedule', order: 10,
  act(verb, arg) { if (verb === 'open' && arg && Number.isInteger(arg.day)) schedDay = arg.day > SHIP.time.day ? arg.day : null; else if (verb === 'today') schedDay = null;
    else if (verb === 'leave' && Number.isInteger(arg) && typeof careerBook === 'function') careerBook(arg); },   // book or cancel a leave day (the career engineer, 0.61.0)
  view: () => {
  const d = SHIP.time.day, m = SHIP.time.min, n = devNow(), B = [{ kind: 'text', text: n.now, mark: 'hot' }];
  if (n.next) B.push({ kind: 'text', text: n.next });
  if (schedDay) B.push({ kind: 'buttons', items: [{ label: 'Back to today', action: { app: 'schedule', do: 'today' } }] });
  for (const day of schedDay ? [schedDay] : [d, d + 1]) {
    B.push({ kind: 'text', text: devDayName(day) + ' · ' + WEEKDAYS[weekday(day)] + (typeof careerOn === 'function' && careerOn(day) ? ' · Leave' : typeof sickToday === 'function' && sickToday(day) ? ' · Sick' + (SHIP.career.sh === 1 ? ', seen by Rina' : SHIP.career.sh === 2 ? ', seen in the infirmary' : '') : devShiftOn(day) ? '' : ' · Day off'), mark: 'head' });
    B.push({ kind: 'list', rows: devDay(day).map(x => ({ text: hhmm(x.from) + (x.kind === 'tradition' ? '' : '–' + hhmm(x.to)) + '  ' + x.title, sub: x.where,
      mark: day === d && x.from <= m && m < x.to ? 'hot' : day === d && x.to <= m ? 'past' : null })) });
    if (day === d && typeof careerClockedIn === 'function' && careerClockedIn(d)) B.push({ kind: 'text', text: 'Clocked in ' + hhmm(SHIP.career.ci % 1440) + (careerClockedOut(d) ? ' · out ' + hhmm(SHIP.career.co % 1440) : '') });   // your hours (0.61.13)
    const lv = typeof careerCanBook === 'function' ? careerCanBook(day) : null;   // leave (0.61.0): a workday you can still book, or cancel, until 07:30 that day
    if (lv) { B.push({ kind: 'buttons', items: [{ label: lv === 'book' ? 'Take this day as leave (' + SHIP.career.l + ' left)' : 'Cancel this leave', action: { app: 'schedule', do: 'leave', arg: day } }] }); tipShow('career.leave', careerText('career.tip.leave')); }
  }
  return { title: 'Schedule', blocks: B };
} });

// Calendar: the week ahead, today and the next six days (0.34.51, the user's 0.60.7 ask; it was two weeks), each day
// with a time bar from 06:00 to midnight (a block a tradition, overlapping ones on a second row: kind 'timeline') and
// its list (the week's shape and the ship traditions, each with Remind me / Don't, and "same time as ..." on a clash).
// Tap a day (0.35.10) for See the day (Schedule shows it) or Make an appointment (Appointments, on that day).
const calShort = s => { s = String(s).replace(/^(The|Birthday:|Brennan's)\s+/, '').replace(/\s*\(.*$/, ''); if (s.length > 11) s = s.split(' ')[0]; return s.charAt(0).toUpperCase() + s.slice(1); };   // "Spice", "Tiles night", "Knit"
const calClash = (x, l) => l.filter(y => y !== x && y.at < x.to && x.at < y.to);
let calDay = null;
deviceApp({ id: 'calendar', title: 'Calendar', icon: 'calendar', order: 15,
  act(verb, arg) {
    const R = SHIP.device.calendarRemind;
    if (verb === 'remind') R.per[arg] = R.per[arg] === false ? true : R.per[arg] === true ? false : false;   // default (on) -> Don't -> Remind me -> Don't
    else if (verb === 'on') R.on = !!arg;
    else if (verb === 'ahead' && [15, 30, 60].includes(arg)) R.ahead = arg;
    else if (verb === 'day') calDay = calDay === arg ? null : arg;
  },
  view: () => {
    const R = SHIP.device.calendarRemind, d0 = SHIP.time.day, B = [], sn = devSeasonLine(d0);
    if (sn) B.push({ kind: 'text', text: 'Season: ' + sn + '.', mark: 'hot' });
    for (let d = d0; d < d0 + 7; d++) {
      const B0 = (d - 1) * 1440, all = devTraditions(B0, B0 + 1439), trad = d === d0 ? all.filter(x => x.at >= shipNow()) : all, ship = DEV_WEEK[weekday(d)].filter(x => !x.tradition);
      const sd = devSeason(d), turn = d > d0 && sd && sd.day === 1;   // a new season starts that day
      B.push({ kind: 'list', rows: [{ text: devDayName(d) + (d < d0 + 2 ? ' · ' + WEEKDAYS[weekday(d)] : '') + (all.length ? ' · ' + all.length + (all.length === 1 ? ' tradition' : ' traditions') : '') + (turn ? ' · ' + sd.name + ' begins' : ''), sub: (devShiftOn(d) ? '' : 'Day off') + (calDay === d ? '' : (devShiftOn(d) ? '' : ' · ') + 'Tap to plan this day') || null, mark: calDay === d ? 'head hot' : 'head', action: { app: 'calendar', do: 'day', arg: d } }] });
      if (calDay === d) B.push({ kind: 'buttons', items: [{ label: 'See the day', action: { app: 'schedule', day: d } }, { label: 'Make an appointment', action: { app: 'appointments', day: d } }] });
      if (all.length) {                                   // the day's time bar: each tradition in the first row it fits
        const lanes = [];
        for (const x of all) { const a = x.at - B0, b = x.to - B0; let i = lanes.findIndex(l => l.every(y => y.b <= a || b <= y.a)); if (i < 0) i = lanes.push([]) - 1; lanes[i].push({ a, b, label: calShort(x.title), past: x.to <= shipNow() }); }
        B.push({ kind: 'timeline', from: 360, to: 1440, rows: lanes, ticks: ['06:00', '15:00', '24:00'] });
      }
      const rows = ship.map(x => ({ m: x.at, text: hhmm(x.at) + '  ' + x.title, sub: x.where }));
      for (const x of trad) {
        const p = R.per[x.kind], same = calClash(x, all);
        rows.push({ m: x.at - B0, text: devWhen(x.at) + '  ' + x.title, sub: x.where + (same.length ? ' · same time as ' + same.map(y => y.title).join(' and ') : '') + (R.on ? p === false ? ' · no reminder' : p === true ? ' · remind me, even on shift' : ' · reminder' : ''),
          button: R.on ? p === false ? 'Remind me' : 'Don\'t' : null, action: R.on ? { app: 'calendar', do: 'remind', arg: x.kind } : null });
      }
      if (rows.length) B.push({ kind: 'list', rows: rows.sort((a, b) => a.m - b.m).map(({ m, ...r }) => r) });   // in time order, the ship's items among them
    }
    B.push({ kind: 'text', text: 'Heads-ups before things start (also in Settings)', mark: 'head' }, { kind: 'buttons', items: [
      { label: 'On', on: R.on, action: { app: 'calendar', do: 'on', arg: true } }, { label: 'Off', on: !R.on, action: { app: 'calendar', do: 'on', arg: false } }] });
    if (R.on) B.push({ kind: 'text', text: 'How long before:' }, { kind: 'buttons', items: [15, 30, 60].map(a => ({ label: a + ' min', on: R.ahead === a, action: { app: 'calendar', do: 'ahead', arg: a } })) });
    return { title: 'Calendar', blocks: B };
  } });

// Jobs (0.35.2, tracks only): you take jobs and turn them in at the job board. Here: yours, its steps and parts, and
// Track (SHIP.player.track: the tracked one drives the goal arrow, section 15b); what's on the board, to read
deviceApp({ id: 'jobs', title: 'Jobs', icon: 'wrench', order: 30,
  act(verb, id) {
    if (verb === 'track') { SHIP.player.track = SHIP.player.track === null ? id : null; if (SHIP.player.track && typeof clearGoal === 'function') clearGoal(); }
    else if (verb === 'board' && typeof setGoal === 'function') { SHIP.player.track = null; setGoal({ deck: 5, room: 'w', label: 'The job board, in the Works bay' }); }
  },
  view: () => {
    const B = [], say = (text, mark) => B.push({ kind: 'text', text, mark });
    if (!jobsOn() || typeof jobsBoard !== 'function') { say('No jobs today.'); return { title: 'Jobs', blocks: B }; }
    const board = jobsBoard(), mine = myJob();
    if (mine) {
      const [title, where] = jobCard(mine), m = mine.machine && machineById(mine.machine), tracked = SHIP.player.track !== null;   // a taken job is tracked until you switch it off (null)
      say('Yours: ' + title + ', ' + where + '.', 'hot');
      if (mine.kind === 'chore') {
        const stops = mine.stops.map(st => { const p = placeById(st.placeId); return (st.tag === 'pickup' ? 'pick up ' + (mine.bring || 'the load') + ' in the ' : st.tag === 'drop' ? 'drop it in the ' : '') + (p ? roomName(p.deck, p.room) || 'room' : 'room') + ' on ' + deckIn(st.deck); });
        say(mine.title + '. ' + (mine.parts.length ? 'Bring ' + mine.parts.map(k => 'a ' + k).join(', ') + ' from main storage on Deck 5. ' : '') + 'Go to: ' + stops.join(', then ') + '.');
      } else if (typeof traceHidden === 'function' && traceHidden(mine)) {   // 24i: a traced job not yet found (the machine stays hidden)
        say(worksText('trace.how', 'Find where it starts: tap the machines on {line} with the pipe kit to read the flow. The Maps app marks them.', { line: traceLineName(mine.symptom.line) }));
      } else if (m) {
        const need = {}; for (const k of mine.parts) need[k] = (need[k] || 0) + 1;
        say('Needs ' + Object.entries(need).map(([k, n]) => n + ' × ' + k + ' (' + (SHIP.stores[k] || 0) + ' in storage)').join(', ') + '. Parts are in main storage on Deck 5; the job is in the ' + ((DECKS[m.deck].rooms[m.room] || {}).name || 'room').toLowerCase() + ' on ' + deckIn(m.deck) + '.');
      } else say(mine.cargo === 'meals' ? 'Take a hover cart from the Cart bay on Deck 5, load ' + (mine.meals || 'the') + ' meals in the cargo hold, and take them up to the cold store on Deck 3. Then bring the cart back.'
        : 'Take a hover cart from the Cart bay on Deck 5, load the delivery in the cargo hold, and take it to main storage. Then bring the cart back.');
      const step = typeof ixJobStep === 'function' ? ixJobStep() : null;
      if (step && step.label) say('Next step: ' + step.label + (step.deck ? ' (' + deckIn(step.deck) + ')' : '') + '.');
      B.push({ kind: 'buttons', items: [{ label: tracked ? 'Tracking' : 'Track', on: tracked, action: { app: 'jobs', do: 'track', arg: mine.id } }] });
      say('Turn it in at the job board when it\'s done.');
    } else say('You take jobs at the job board in the Works bay (Deck 5), and turn them in there when they\'re done.');
    const open = board.filter(j => !j.claimedBy);
    if (open.length) {
      say('On the board', 'head');
      B.push({ kind: 'list', rows: open.slice(0, 5).map(j => { const [title, where, state, pri] = jobCard(j);
        return { text: (pri === 'urgent' ? '! ' : '') + title, sub: where + ' · ' + state + (jobTier(j) > playerTier() ? ' · tier ' + jobTier(j) : ''), mark: pri === 'urgent' ? 'urgent' : null }; }) });
      if (open.length > 5) say('And ' + (open.length - 5) + ' more on the board.');
    } else if (!mine) say('Nothing on the board. Enjoy it while it lasts.');
    if (!mine) B.push({ kind: 'buttons', items: [{ label: 'Show me the board', action: { app: 'jobs', do: 'board' } }] });
    return { title: 'Jobs', blocks: B };
  } });

// Maps (0.35.3): each deck as a plan drawn from its deck data (DECKS[n].map and rooms): halls, rooms, locked rooms
// hatched, the lift, you as a dot on your deck, the goal as a pin. Tap a room on the plan or in the list to pick it;
// "Go there" points the goal arrow at it (setGoal, section 15b); on another deck the arrow leads to the lift first.
let mapDeck = null, mapPick = null;
const mapLocked = (n, k) => typeof schedRoomLocked === 'function' ? schedRoomLocked(n, k) : false;
// Maps shows no people (0.35.16, the user's answer): where someone is lives in the Roster app below.
let mapFor = null;                                       // 'appointments' while picking a place to meet (0.35.10)
deviceApp({ id: 'maps', title: 'Maps', icon: 'map', order: 25,
  act(verb, arg) {
    // someone's whereabouts (section 20's Crew app: { app: 'maps', do: 'person', arg } or { app: 'maps', who }) go to the Roster
    if (verb === 'open' && arg && arg.who) { rosterPick = arg.who; return 'roster'; }
    if (verb === 'person' || verb === 'who') { rosterPick = arg; deviceShow('roster'); return; }
    if (verb === 'deck' && DECKS[arg]) { mapDeck = arg; mapPick = null; }
    else if (verb === 'pick') mapPick = mapPick === arg ? null : arg;
    else if (verb === 'go' && mapPick && typeof setGoal === 'function') {
      const n = mapDeck || deckDef.num, r = DECKS[n].rooms[mapPick];
      SHIP.player.track = null; setGoal({ deck: n, room: mapPick, label: r.name + (n !== deckDef.num ? ', ' + deckIn(n) : '') });
      deviceNotify({ app: 'maps', text: 'Follow the marker to the ' + r.name.toLowerCase() + '.', urgent: true }); delete DEV.notes.maps;
    }
    else if (verb === 'clear' && typeof clearGoal === 'function') clearGoal();
    else if (verb === 'meet' && mapFor === 'appointments') {
      const id = mapPick && apptRoomPlace(mapDeck || deckDef.num, mapPick); mapFor = null;
      if (id && apptDraft) apptDraft.where = id;
      deviceShow('appointments');
    }
    else if (verb === 'unmeet') { mapFor = null; deviceShow('appointments'); }
  },
  view: () => {
    const n = mapDeck && DECKS[mapDeck] ? mapDeck : deckDef.num, def = DECKS[n], rooms = {};
    for (const [k, r] of Object.entries(def.rooms || {})) {
      const kind = r.void ? 'void' : r.floor === 'lift' ? 'lift' : r.hall ? 'hall' : mapLocked(n, k) ? 'locked' : r.still || r.spine ? 'service' : 'room';
      rooms[k] = { name: r.name || k, kind };
    }
    const you = n === deckDef.num && typeof player !== 'undefined' ? player.here() : null;
    const g = typeof IX_GOAL !== 'undefined' && IX_GOAL && IX_GOAL.deck === n ? IX_GOAL : null;
    let mk = null; try { mk = typeof traceMarks === 'function' ? traceMarks(n) : null; } catch (e) { mk = null; }   // 24i: your traced job's line
    const B = [{ kind: 'text', text: 'Deck' }, { kind: 'buttons', items: DECK_ORDER.filter(d => DECKS[d]).map(d => ({ label: deckLabel(d), on: d === n, action: { app: 'maps', do: 'deck', arg: d } })) },
      { kind: 'text', text: deckWord(n) + ': ' + def.name + (n === deckDef.num ? ' (you are here)' : ''), mark: 'head' },
      { kind: 'map', grid: def.map, rooms, you, pick: mapPick, goal: g ? (g.room && typeof g.room === 'string' ? g.room : null) : null, marks: mk && mk.tiles.length ? mk.tiles : null, action: { app: 'maps', do: 'pick' } }];
    if (mk) B.push({ kind: 'text', text: mk.text, mark: 'hot' });
    if (mapFor === 'appointments') {
      if (!apptDraft) mapFor = null;
      else {
        const id = mapPick && apptRoomPlace(n, mapPick);
        B.splice(0, 0, { kind: 'text', text: mapPick ? id ? 'Meet in the ' + rooms[mapPick].name.toLowerCase() + '?' : 'Nowhere to sit and meet in there. Try a lounge, the mess or a garden.' : 'Tap a room to meet in.', mark: 'hot' },
          { kind: 'buttons', items: (id ? [{ label: 'Meet here', action: { app: 'maps', do: 'meet' } }] : []).concat([{ label: 'Cancel', action: { app: 'maps', do: 'unmeet' } }]) });
      }
    }
    if (mapPick && rooms[mapPick]) {
      const r = rooms[mapPick];
      B.push({ kind: 'text', text: r.name + (r.kind === 'locked' ? ': locked' : r.kind === 'service' ? ': a service room' : ''), mark: 'hot' });
      if (r.kind !== 'locked' && r.kind !== 'void' && !mapFor) B.push({ kind: 'buttons', items: [{ label: 'Go there', action: { app: 'maps', do: 'go' } }] });
    }
    B.push({ kind: 'text', text: 'Rooms', mark: 'head' });
    const list = Object.entries(rooms).filter(([, r]) => r.kind === 'room' || r.kind === 'hall' && /lobby|lounge|promenade|bridge/i.test(r.name))
      .sort((a, b) => a[1].name < b[1].name ? -1 : 1);
    B.push({ kind: 'list', rows: list.map(([k, r]) => ({ text: r.name, mark: k === mapPick ? 'hot' : null, action: { app: 'maps', do: 'pick', arg: k } })) });
    return { title: 'Maps', blocks: B };
  } });

// Roster (0.35.16, the user's answer): everyone aboard by department, people you know first (section 20's relTier;
// section 20's Crew app is the people you know and what you know about them). Tap a name for one line on where they
// are now, from section 14's whereIs; asleep or washing reads "In their quarters" (privacy). Go there points the goal
// arrow at that room. { app: 'roster', who: crewId } opens it on someone. Guests show only while aboard.
const ROSTER_DEPTS = [['command', 'Command'], ['helm', 'Helm'], ['comms', 'Comms'], ['survey', 'Survey'], ['works', 'Works'], ['watch', 'Watch'],
  ['infirmary', 'Infirmary'], ['galley', 'Galley'], ['store', 'Ship\'s store'], ['civilian', 'Civilians'], ['guest', 'Guests']];
const ROSTER_ACT = { work: 'On duty', breakfast: 'At breakfast', lunch: 'At lunch', dinner: 'At dinner', gym: 'At the gym', appt: 'At an appointment' };
let rosterPick = null, rosterTab = 'all';             // rosterTab: 'all' (everyone, the main view) or 'known' (People I know: Friends, Acquaintances, Met; 0.36.82)
const rosterTier = id => { if (typeof relTier !== 'function') return 0; try { return relTier(id) || 0; } catch (e) { return 0; } };
const rosterRoomName = n => /\d/.test(n) ? n : 'the ' + n.charAt(0).toLowerCase() + n.slice(1);
function rosterWhere(p, t = shipNow()) {                 // { line, deck, room }: room only when Go there makes sense
  let w = null; try { w = typeof whereIs === 'function' ? whereIs(p, t) : null; } catch (e) { w = null; }
  if (!w) return { line: 'Not aboard right now.' };
  if (w.act === 'sleep' || w.act === 'wash') return { line: 'In their quarters.' };
  if (w.moving) return { line: 'On the move' + (w.deck ? ', heading for ' + deckIn(w.deck) : '') + '.' };
  const S = typeof schedData === 'function' ? schedData() : null, pl = w.placeId && S ? S.byId.get(w.placeId) : null;
  const room = pl && pl.deck === w.deck ? pl.room : null, r = room && DECKS[w.deck] && (DECKS[w.deck].rooms || {})[room], rn = r && r.name;
  if (rn && mapLocked(w.deck, room) && w.act !== 'work') return { line: 'In their quarters.' };   // a private cabin
  const at = deckWord(w.deck) + (rn ? ', ' + rosterRoomName(rn) : '');
  return { line: (ROSTER_ACT[w.act] ? ROSTER_ACT[w.act] + ': ' : '') + at + '.', deck: w.deck, room: rn ? room : null, roomName: rn };
}
function rosterPeople() {                                // everyone aboard: [{ p, tier }]; guests only while aboard
  const all = typeof schedPeople === 'function' ? schedPeople() : [], t = shipNow();
  const gone = id => { try { return typeof movedOff === 'function' && movedOff(id); } catch (e) { return false; } };
  return all.filter(p => !p.player && !gone(p.id) && (p.rank !== 'guest' && p.dept !== 'guest' || (() => { try { return !!whereIs(p, t); } catch (e) { return false; } })()))
    .map(p => ({ p, tier: rosterTier(p.id) }));
}
deviceApp({ id: 'roster', title: 'Roster', icon: 'crew', order: 52,
  act(verb, arg) {
    if (verb === 'open' && arg && arg.who) rosterPick = arg.who;
    else if (verb === 'pick') rosterPick = rosterPick === arg ? null : arg;
    else if (verb === 'tab') { rosterTab = arg === 'known' ? 'known' : 'all'; rosterPick = null; }
    else if (verb === 'go' && rosterPick && typeof setGoal === 'function') {
      const p = apptPerson(rosterPick), w = p && rosterWhere(p); if (!w || !w.room) return;
      SHIP.player.track = null; setGoal({ deck: w.deck, room: w.room, label: p.name.split(' ')[0] + ', ' + rosterRoomName(w.roomName) + (w.deck !== deckDef.num ? ', ' + deckIn(w.deck) : '') });
      deviceNotify({ app: 'roster', text: 'Follow the marker to ' + rosterRoomName(w.roomName) + '.', urgent: true }); delete DEV.notes.roster;
    }
  },
  view: () => {
    const B = [], ps = rosterPeople(), byName = (a, b) => a.p.name < b.p.name ? -1 : 1;
    const group = (title, list) => {
      if (!list.length) return;
      if (title) B.push({ kind: 'text', text: title, mark: 'head' });
      let rows = [];
      for (const x of list) {
        rows.push({ text: x.p.name, sub: (x.p.role || '') + (x.tier >= 1 && typeof REL_NAMES !== 'undefined' ? ' · ' + REL_NAMES[x.tier] : ''), mark: x.p.id === rosterPick ? 'hot' : null, action: { app: 'roster', do: 'pick', arg: x.p.id } });
        if (x.p.id !== rosterPick) continue;
        const w = rosterWhere(x.p); B.push({ kind: 'list', rows }); rows = [];
        B.push({ kind: 'text', text: w.line, mark: 'hot' });
        if (w.room) B.push({ kind: 'buttons', items: [{ label: 'Go there', action: { app: 'roster', do: 'go' } }] });
      }
      if (rows.length) B.push({ kind: 'list', rows });
    };
    const tx = (k, d, n) => (typeof talkText === 'function' ? talkText(k, d) : d).replace(/\{n\}/g, n);
    B.push({ kind: 'buttons', items: [{ label: tx('roster.tab.all', 'Everyone'), on: rosterTab !== 'known', action: { app: 'roster', do: 'tab', arg: 'all' } },
      { label: tx('roster.tab.known', 'People I know'), on: rosterTab === 'known', action: { app: 'roster', do: 'tab', arg: 'known' } }] });
    if (rosterTab === 'known') {                         // People I know (0.36.82): Friends (friend, close friend), Acquaintances (acquaintance, colleague), Met (section 20's rel.met: you opened their card, were introduced, ate or worked together)
      const met = x => { try { return typeof metDays === 'function' && metDays(x.p.id) >= 0; } catch (e) { return false; } };
      const sets = [['roster.friends', 'Friends', ps.filter(x => x.tier >= 3)], ['roster.acq', 'Acquaintances', ps.filter(x => x.tier === 1 || x.tier === 2)], ['roster.met', 'Met', ps.filter(x => x.tier < 1 && met(x))]];
      if (!sets.some(x => x[2].length)) B.push({ kind: 'text', text: tx('roster.none', 'Nobody yet. Say hello to someone!', 0) });
      else for (const [k, d, list] of sets) { const h = tx(k, d + ' ({n})', list.length); B.push({ kind: 'text', text: /\d/.test(h) ? h : h + ' (' + list.length + ')', mark: 'head' }); if (list.length) { group(null, list.sort((a, b) => b.tier - a.tier || byName(a, b))); } }
      return { title: 'Roster', blocks: B };
    }
    group('People you know', ps.filter(x => x.tier >= 1).sort((a, b) => b.tier - a.tier || byName(a, b)));
    const rest = ps.filter(x => x.tier < 1), known = new Set(ROSTER_DEPTS.map(d => d[0]));
    for (const [d, title] of ROSTER_DEPTS) group(title, rest.filter(x => x.p.dept === d).sort(byName));
    group('Others aboard', rest.filter(x => !known.has(x.p.dept)).sort(byName));
    let gone = []; try { gone = typeof movedOn === 'function' ? movedOn() || [] : []; } catch (e) { gone = []; }   // 0.35.22: section 20's movedOn
    gone = gone.filter(x => x && typeof x === 'object');
    if (gone.length) B.push({ kind: 'text', text: 'Left the Wren', mark: 'head' }, { kind: 'list', rows: gone.map(x => ({ text: String(x.name || x.id || 'Someone'),
      sub: [x.role, Number.isFinite(x.day) ? 'left on Day ' + x.day : 'left the ship'].filter(Boolean).join(' · ') + (x.to ? ', for ' + x.to : ''), mark: 'past' })) });
    if (!ps.length) B.push({ kind: 'text', text: 'No crew list yet.' });
    return { title: 'Roster', blocks: B };
  } });

// Memos (0.35.4): notes you write (a title and plain text, dated), saved in SHIP.device.memos. Pin one to Home.
// "Remember this" on a Mail copies it into a new memo (memoAdd, for other apps too).
let memoOpen = null, memoNew = false;
function memoAdd(title, text) {
  const M = SHIP.device.memos, id = M.reduce((a, m) => Math.max(a, m.id), 0) + 1;
  M.unshift({ id, title: String(title || 'Memo').slice(0, 80), text: String(text || '').slice(0, 2000), at: shipNow(), pinned: false });
  M.length = Math.min(M.length, 50);
  return id;
}
deviceApp({ id: 'memos', title: 'Memos', icon: 'memo', order: 45,
  act(verb, arg) {
    const M = SHIP.device.memos, m = M.find(x => x.id === (arg && arg.id || arg));
    if (verb === 'new') { memoNew = true; memoOpen = null; }
    else if (verb === 'save' && arg) { if (String(arg.title || '').trim() || String(arg.text || '').trim()) memoOpen = memoAdd(String(arg.title || '').trim() || 'Memo', arg.text); memoNew = false; }
    else if (verb === 'cancel') memoNew = false;
    else if (verb === 'open') memoOpen = memoOpen === arg ? null : arg;
    else if (verb === 'pin' && m) { const was = m.pinned; for (const x of M) x.pinned = false; m.pinned = !was; }
    else if (verb === 'delete' && m) { M.splice(M.indexOf(m), 1); memoOpen = null; }
  },
  view: () => {
    const M = SHIP.device.memos, B = [];
    if (memoNew) {
      B.push({ kind: 'form', fields: [{ id: 'title', label: 'Title', value: '' }, { id: 'text', label: 'Note', value: '', multiline: true }],
        submit: { label: 'Save', action: { app: 'memos', do: 'save' } }, cancel: { label: 'Cancel', action: { app: 'memos', do: 'cancel' } } });
      return { title: 'New memo', blocks: B };
    }
    B.push({ kind: 'buttons', items: [{ label: 'New memo', action: { app: 'memos', do: 'new' } }] });
    if (!M.length) B.push({ kind: 'text', text: 'No memos yet. Write one, or tap "Remember this" on a message.' });
    for (const m of M) {
      B.push({ kind: 'list', rows: [{ text: (m.pinned ? '▪ ' : '') + m.title, sub: 'Day ' + (Math.floor(m.at / 1440) + 1) + ' ' + devWhen(m.at), action: { app: 'memos', do: 'open', arg: m.id }, mark: m.id === memoOpen ? 'hot' : null }] });
      if (m.id === memoOpen) {
        if (m.text) B.push({ kind: 'text', text: m.text });
        B.push({ kind: 'buttons', items: [{ label: m.pinned ? 'Unpin' : 'Pin to Home', action: { app: 'memos', do: 'pin', arg: m.id } }, { label: 'Delete', action: { app: 'memos', do: 'delete', arg: m.id } }] });
      }
    }
    return { title: 'Memos', blocks: B };
  } });

// Ship (0.35.4): ship health and each system, as on the Works bay board (shipHealthRows, section 17), and what's on
// today. Ship news (0.35.8): what you've heard aboard, newest first (section 20's shipNews: { text, from, at }).
const SHIP_NEWS_N = 8;
function devNews() {
  if (typeof shipNews !== 'function') return [];
  try { return (shipNews(SHIP_NEWS_N) || []).filter(x => x && typeof x.text === 'string'); } catch (e) { DEV.errors.push('shipNews: ' + (e && e.message || e)); return []; }
}
deviceApp({ id: 'ship', title: 'News feed', icon: 'news', order: 60, view: () => {   // 0.28.44: the Ship app became the News feed (section 15's SHIP.news)
  const B = [], posts = (Array.isArray(SHIP.news) ? SHIP.news : []).map(x => ({ at: x.at, text: x.text, from: typeof NEWS_SRC !== 'undefined' && NEWS_SRC[x.src] || x.src }));
  for (const x of devNews()) posts.push({ at: x.at, text: x.text, from: 'Overheard' + (x.from ? ', ' + x.from : '') });   // what you've heard aboard (section 20's shipNews)
  posts.sort((a, b) => (isFinite(b.at) ? b.at : 0) - (isFinite(a.at) ? a.at : 0));
  if (posts.length) B.push({ kind: 'list', rows: posts.slice(0, 40).map(x => ({ text: x.text, sub: x.from + (isFinite(x.at) ? ' · ' + devDayName(Math.floor(x.at / 1440) + 1) + ' ' + devWhen(x.at) : '') })) });
  else B.push({ kind: 'text', text: 'No news yet. Posts from around the ship turn up here through the day.' });
  const notes = (playerFx().notes || []).filter(n => n && n.text);
  if (notes.length) { B.push({ kind: 'text', text: 'Around you', mark: 'head' }); for (const n of notes.slice(0, 4)) B.push({ kind: 'text', text: n.text + '.' }); }
  B.push({ kind: 'text', text: 'Systems', mark: 'head' });   // the bars stay, small, at the bottom: the health board is only in the Works bay
  if (typeof shipHealthRows === 'function') {
    const rows = shipHealthRows();
    B.push({ kind: 'bars', items: rows.map(r => ({ label: r.name, value: r.value, level: r.state === 'failing' ? 'low' : r.state === 'poor' ? 'mid' : '' })) });
  } else B.push({ kind: 'text', text: 'No ship systems report yet.' });
  return { title: 'News feed', blocks: B };
} });

// Record (0.35.4): your Works record, where progression shows. Certification and the Chief's comments come later.
deviceApp({ id: 'record', title: 'Record', icon: 'record', order: 70, view: () => {
  const mine = (SHIP.jobs || []).filter(j => j.doneBy === 'you'), B = [];
  B.push((typeof worksRecordHead === 'function' && worksRecordHead()) || { kind: 'text', text: 'Works technician, tier ' + (typeof playerTier === 'function' ? playerTier() : 1) + '.', mark: 'hot' });
  B.push({ kind: 'text', text: mine.length ? 'Jobs on the recent record: ' + mine.length + '.' : 'No jobs on your record yet. Take one at the job board in the Works bay.' });
  if (mine.length) B.push({ kind: 'list', rows: mine.slice(-6).reverse().map(j => { const [title, where] = jobCard(j); return { text: title, sub: where + ', Day ' + (Math.floor(j.doneAt / 1440) + 1) }; }) });
  // reputation (0.35.22, Pillar 4): section 20's repView(), words only, never numbers
  let rv = null; try { rv = typeof repView === 'function' ? repView() : null; } catch (e) { rv = null; }
  if (rv) {
    B.push({ kind: 'text', text: 'Reputation', mark: 'head' });
    if (rv.ship) B.push({ kind: 'text', text: [rv.ship.work, rv.ship.kindness, rv.ship.spirit].filter(Boolean).join('. ') + '.' });
    if (rv.knownFor && rv.knownFor.length) B.push({ kind: 'text', text: 'Known for: ' + rv.knownFor.join(', ') + '.', mark: 'hot' });
    const DN = Object.fromEntries(ROSTER_DEPTS); DN.garden = 'Garden';
    if (rv.depts && rv.depts.length) B.push({ kind: 'list', rows: rv.depts.filter(x => x.band !== 'new').map(x => ({ text: DN[x.dept] || x.dept, sub: x.name }))
      .concat(rv.depts.some(x => x.band === 'new') ? [{ text: 'Elsewhere', sub: 'A new face: ' + rv.depts.filter(x => x.band === 'new').map(x => DN[x.dept] || x.dept).join(', '), mark: 'past' }] : []) });
    if (rv.notes && rv.notes.length) { B.push({ kind: 'text', text: 'What people said', mark: 'head' }); B.push({ kind: 'list', rows: rv.notes.slice(0, 4).map(n => ({ text: n.text, sub: (n.from ? n.from + ', ' : '') + 'Day ' + n.day })) }); }
  } else B.push({ kind: 'text', text: 'The Chief\'s view and your road to certification will show here.' });
  const hw = typeof hobbyWords === 'function' ? hobbyWords() : [];   // your hobbies in words (0.28.63, the plan: no levels or points)
  if (hw.length) { B.push({ kind: 'text', text: 'Free time', mark: 'head' }); for (const t of hw) B.push({ kind: 'text', text: t }); }
  return { title: 'Record', blocks: B };
} });

// Crew and Appointments (0.35.4): shells. The social engineer's section 20 registers its own 'crew' and 'appointments' apps
// with deviceApp, which replace these.
deviceApp({ id: 'crew', title: 'Relationships', short: 'People', icon: 'people', order: 50, view: () => ({ title: 'Relationships', blocks: [{ kind: 'text', text: 'Your contacts fill in as you get to know people aboard.' }] }) });

// Appointments (0.35.6, C3): make one (who, when, where), and crew answer from their real day (section 14's
// apptReply: yes, "how about 18:30?", or no). Accepted ones go into SHIP.device.appts (saved) and section 14 walks
// them there (apptWhere) and marks them 'kept' or 'missed' (apptTick). Invitations from crew (by set, status 'asked')
// arrive here to accept or decline. A reminder comes about 10 ship minutes before. Missing one is never punished.
const APPT_PLACE_ROOMS = /mess|lounge|gym|garden|common room|tea corner|music|observ|infirmary|chief's office|promenade/i;
const APPT_SEATS = ['lounge-seat', 'mess-seat', 'bench', 'common-room', 'garden', 'gym', 'music'];
let apptPlacesCache = null, apptDraft = null, apptSay = null;
function apptPlaces() {                                  // [{ id, name, deck }]: one good spot in each meeting room
  if (apptPlacesCache) return apptPlacesCache;
  const out = [];
  for (const n of Object.keys(DECKS).map(Number).sort((a, b) => a - b)) {
    const def = DECKS[n], rooms = def.rooms || {}, seen = new Set(); if (def.playerOnly) continue;
    for (const pl of def.places || []) {
      const r = rooms[pl.room]; if (!r || seen.has(pl.room) || !APPT_PLACE_ROOMS.test(r.name || '') || mapLocked(n, pl.room)) continue;
      if (!APPT_SEATS.includes(pl.type) && !/office|infirmary/i.test(r.name)) continue;
      seen.add(pl.room); out.push({ id: pl.id, name: r.name, deck: n, room: pl.room });
    }
  }
  return (apptPlacesCache = out);
}
// a free spot in that room at that time (the sim engineer's advice): a seat nobody's plan holds then (shipDay's occ),
// and no other appointment; a room behind a locked door takes any place in it
const apptSpot = (where, at, len) => apptSpots(where, at, len, 1)[0];
function apptSpots(where, at, len, k = 1) {               // k free spots (0.35.10: a group gets a seat each), repeating the last if short
  const n = apptDeckOf(where); if (n === null) return Array(k).fill(where);
  const def = DECKS[n], room = def.places.find(q => q.id === where).room, office = /office|infirmary/i.test((def.rooms[room] || {}).name || '');
  const d = Math.floor(at / 1440) + 1, occ = typeof shipDay === 'function' ? shipDay(d).occ : null, over = (a, b) => a < at + len && at - 10 < b;
  const used = new Set(SHIP.device.appts.filter(a => (a.status === 'yes' || a.status === 'kept') && over(a.at, a.at + (a.len || 30))).map(a => a.where));
  const free = def.places.filter(q => q.room === room && (office || APPT_SEATS.includes(q.type)) && !used.has(q.id)
    && !(occ && (occ.get(q.id) || []).some(([a, b]) => over(a, b))));
  const ids = free.slice(0, k).map(q => q.id); if (!ids.length) ids.push(where);
  while (ids.length < k) ids.push(ids[ids.length - 1]);
  return ids;
}
const apptDeckOf = id => { for (const n of Object.keys(DECKS)) if ((DECKS[n].places || []).some(q => q.id === id)) return +n; return null; };
// a place to meet in room key of deck n, for a room picked on Maps (0.35.10): its listed meeting spot, else any seat
// in it; null for a locked room or one with nowhere to sit
function apptRoomPlace(n, key) {
  const ref = apptPlaces().find(x => x.deck === n && x.room === key); if (ref) return ref.id;
  const r = (DECKS[n].rooms || {})[key]; if (!r || r.void || r.floor === 'lift' || mapLocked(n, key)) return null;
  const q = (DECKS[n].places || []).find(x => x.room === key && APPT_SEATS.includes(x.type) && !x.machine);
  return q ? q.id : null;
}
const apptPerson = id => typeof schedPeople === 'function' ? schedPeople().find(p => p.id === id) : (typeof ROSTER !== 'undefined' ? ROSTER.find(p => p.id === id) : null);
const apptName = id => { const p = apptPerson(id); return p ? p.name : String(id); };
const apptWhereName = id => {                          // the room's name, for any place in it
  for (const n of Object.keys(DECKS)) { const q = (DECKS[n].places || []).find(x => x.id === id); if (q) { const r = (DECKS[n].rooms || {})[q.room]; return (r ? r.name : 'there') + ', ' + deckIn(n); } }
  return 'there';
};
function apptPeople() {                                  // who you can ask: people you've met when section 20 says, else story and Works crew
  const all = typeof schedPeople === 'function' ? schedPeople().filter(p => !p.player && p.rank !== 'guest') : [];
  const met = typeof relTier === 'function' ? all.filter(p => { try { return relTier(p.id) >= 1; } catch (e) { return false; } }) : [];
  return (met.length ? met : all.filter(p => p.story || p.dept === 'works')).slice().sort((a, b) => a.name < b.name ? -1 : 1);
}
// appointments as the player sees them: a group meeting (0.35.10) is one appointment per person (each with their own
// seat, so section 14 walks each to a spot of their own) sharing a grp id; apptGroups gathers them: [{ a, all, names }]
const APPT_MAX = 6;
function apptGroups(list) {
  const out = [], by = new Map();
  for (const a of list) {
    const g = a.grp ? by.get(a.grp) : null;
    if (g) g.all.push(a); else { const n = { a, all: [a] }; out.push(n); if (a.grp) by.set(a.grp, n); }
  }
  for (const g of out) g.names = g.all.flatMap(x => x.with).map(apptName).join(', ');
  return out;
}
const apptNames = ids => ids.length < 3 ? ids.map(id => apptName(id).split(' ')[0]).join(' and ') : ids.slice(0, -1).map(id => apptName(id).split(' ')[0]).join(', ') + ' and ' + apptName(ids[ids.length - 1]).split(' ')[0];
function apptKind(where, withId) {
  const r = apptPlaces().find(x => x.id === where), p = apptPerson(withId);
  return r && /infirmary/i.test(r.name) ? 'checkup' : r && /office/i.test(r.name) || p && /chief/i.test(p.role || '') && r && /office/i.test(r.name) ? 'work' : 'social';
}
// apptAdd (0.35.32, the lead): section 18's occasions (the ready room summons, the Captain's table, a progress talk) become
// real appointments, as the Pillar 3 plan had it: occasionAdd calls apptAdd({ id: key, with: [by], at, len,
// where: 'deck|room', kind, status: 'yes', by, title }). The room becomes a spot in it (a seat if there is one), so
// section 14 walks the host there and keeps or misses it, and section 20 counts it like any other. Once per occasion
// (a.occ = its key); the record keeps title and occ (deviceLoad keeps extra fields). Returns the appointment or null.
function apptOccSpot(n, key) {                           // a spot in a room, locked ones too (the ready room, the Captain's quarters)
  const P = (DECKS[n] && DECKS[n].places || []).filter(x => x.room === key && !x.machine);
  const q = P.find(x => APPT_SEATS.includes(x.type)) || P.find(x => /seat|chair|bench|stand|desk/.test(x.type || '')) || P[0];
  return q ? q.id : null;
}
function apptAdd(o) {
  if (!o || typeof o !== 'object' || !Array.isArray(o.with) || !Number.isFinite(o.at)) return null;
  const D = SHIP.device, occ = typeof o.id === 'string' ? o.id : null;
  if (occ) { const had = D.appts.find(a => a.occ === occ); if (had) return had; }
  let where = typeof o.where === 'string' ? o.where : null; const m = where && /^(\d+)\|(.+)$/.exec(where);
  if (m) { where = apptOccSpot(+m[1], m[2]); if (where) where = apptSpot(where, +o.at, Number.isFinite(o.len) ? +o.len : 30); }   // 0.35.35 (sim engineer 4): a seat nobody's plan holds then
  if (!where || !(typeof apptPlace === 'function' ? apptPlace({ where }) : null)) return null;
  const a = { id: D.appts.reduce((x, y) => Math.max(x, y.id), 0) + 1, with: o.with.filter(x => typeof x === 'string').slice(0, 8), at: +o.at, len: Number.isFinite(o.len) ? +o.len : 30,
    where, kind: typeof o.kind === 'string' ? o.kind : 'meeting', status: o.status === 'asked' ? 'asked' : 'yes', by: typeof o.by === 'string' ? o.by : null,
    ...(typeof o.title === 'string' ? { title: o.title.slice(0, 80) } : {}), ...(occ ? { occ } : {}) };
  D.appts.push(a); if (D.appts.length > 60) D.appts.splice(0, D.appts.length - 60);
  deviceRefresh(); return a;
}
function apptBook(ids, at, len, kind) {                  // accepted: one appointment each, a seat each, one grp for a group
  const D = SHIP.device, spots = apptSpots(apptDraft.where, at, len, ids.length), id0 = D.appts.reduce((m, x) => Math.max(m, x.id), 0) + 1;
  ids.forEach((pid, i) => D.appts.push({ id: id0 + i, with: [pid], at, len, where: spots[i], kind, status: 'yes', by: null, ...(ids.length > 1 ? { grp: id0 } : {}) }));
}
deviceApp({ id: 'appointments', title: 'Appointments', short: 'Appts', icon: 'calendar', order: 12,
  badge: () => SHIP.device.appts.filter(a => a.by && a.status === 'asked').length || null,
  act(verb, arg) {
    const D = SHIP.device, now = shipNow();
    if (verb === 'open' && arg && arg.with) { apptDraft = { with: [].concat(arg.with).filter(x => typeof x === 'string').slice(0, APPT_MAX), day: SHIP.time.day, min: Math.max(360, Math.ceil((SHIP.time.min + 60) / 15) * 15) % 1440, where: null }; apptSay = null; }
    else if (verb === 'open' && arg && Number.isInteger(arg.day) && arg.day >= SHIP.time.day) {   // from the Calendar: that day, after shift unless it's today
      apptDraft = { with: [], day: arg.day, min: arg.day === SHIP.time.day ? Math.ceil((SHIP.time.min + 60) / 15) * 15 % 1440 : 1080, where: null }; apptSay = null; }
    else if (verb === 'map' && apptDraft) { mapFor = 'appointments'; const w = apptDraft.where && apptDeckOf(apptDraft.where); mapDeck = w || null; mapPick = null; deviceShow('maps'); }
    else if (verb === 'new') { apptDraft = { with: [], day: SHIP.time.day, min: Math.ceil((SHIP.time.min + 60) / 15) * 15 % 1440, where: null }; apptSay = null; }
    else if (verb === 'cancel') { apptDraft = null; apptSay = null; }
    else if (verb === 'who' && apptDraft && arg) {               // add or remove someone (a group meeting: up to APPT_MAX)
      const W = apptDraft.with, i = W.indexOf(arg);
      if (i >= 0) W.splice(i, 1); else if (W.length < APPT_MAX) W.push(arg);
      apptDraft.adding = false; delete apptDraft.later; delete apptDraft.some;
    }
    else if (verb === 'adding' && apptDraft) apptDraft.adding = !apptDraft.adding;
    else if (verb === 'day' && apptDraft) apptDraft.day = arg;
    else if (verb === 'time' && apptDraft) apptDraft.min = Math.max(360, Math.min(22 * 60, apptDraft.min + arg));
    else if (verb === 'where' && apptDraft) apptDraft.where = arg;
    else if (verb === 'ask' && apptDraft && apptDraft.with.length && apptDraft.where) {
      const d = apptDraft, ids = d.with.slice(), at = (d.day - 1) * 1440 + d.min, len = 30, kind = apptKind(d.where, ids[0]);
      if (at <= now + 10) { apptSay = 'That\'s too soon. Pick a later time.'; return; }
      delete d.later; delete d.some;
      const nextId = () => D.appts.reduce((m, x) => Math.max(m, x.id), 0) + 1;
      const ask = (pid, t, where) => { const a = { id: nextId(), with: [pid], at: t, len, where: where || apptSpot(d.where, t, len), kind, status: 'asked', by: null };
        return { a, r: typeof apptReply === 'function' ? apptReply(apptPerson(pid), a) : { answer: 'yes', at: t, text: apptName(pid) + ': "See you then."' } }; };
      if (ids.length === 1) {
        const { a, r } = ask(ids[0], at);
        apptSay = r.text;
        if (r.answer === 'yes') { a.status = 'yes'; D.appts.push(a); apptDraft = null; }
        else if (r.answer === 'later') d.later = r.at;
        return;
      }
      const rs = ids.map(pid => ask(pid, at).r), yes = ids.filter((x, i) => rs[i].answer === 'yes');
      if (yes.length === ids.length) { apptBook(ids, at, len, kind); apptSay = 'Everyone can come: ' + apptNames(ids) + ', ' + devWhen(at) + '.'; apptDraft = null; return; }
      apptSay = rs.filter(x => x.answer !== 'yes').map(x => x.text).join(' ') + (yes.length ? ' (' + apptNames(yes) + (yes.length > 1 ? ' can.)' : ' can.)') : '');
      const dayEnd = Math.floor(at / 1440) * 1440 + 22 * 60;   // a time later that day everyone can do
      for (let t = Math.ceil((at + 30) / 30) * 30; t + len <= dayEnd; t += 30) if (ids.every(pid => ask(pid, t).r.answer === 'yes')) { d.later = t; break; }
      if (yes.length) d.some = yes;
      if (!d.later && !d.some) apptSay += ' Try another time or day.';
    }
    else if (verb === 'some' && apptDraft && apptDraft.some) {   // go ahead with those who can
      const d = apptDraft, at = (d.day - 1) * 1440 + d.min, ids = d.some;
      apptBook(ids, at, 30, apptKind(d.where, ids[0])); apptSay = 'Booked with ' + apptNames(ids) + ', ' + devWhen(at) + '.'; apptDraft = null;
    }
    else if (verb === 'later' && apptDraft && apptDraft.later) { apptDraft.min = apptDraft.later % 1440; apptDraft.day = Math.floor(apptDraft.later / 1440) + 1; delete apptDraft.later; DEVICE_APPS.get('appointments').act('ask'); }
    else if (verb === 'accept' || verb === 'decline') { const a = D.appts.find(x => x.id === arg); if (a) a.status = verb === 'accept' ? 'yes' : 'no'; }
    else if (verb === 'drop') { const a = D.appts.find(x => x.id === arg); if (a) for (const o of D.appts) if ((o === a || a.grp && o.grp === a.grp) && o.status === 'yes') o.status = 'no'; }
  },
  view: () => {
    const D = SHIP.device, now = shipNow(), B = [], d = apptDraft;
    if (d) {
      if (apptSay) B.push({ kind: 'text', text: apptSay, mark: 'hot' });
      if (d.later || d.some) B.push({ kind: 'buttons', items: (d.later ? [{ label: 'OK, ' + devWhen(d.later) + (d.with.length > 1 ? ' for all' : ''), action: { app: 'appointments', do: 'later' } }] : [])
        .concat(d.some ? [{ label: 'Just ' + apptNames(d.some), action: { app: 'appointments', do: 'some' } }] : [], [{ label: 'Never mind', action: { app: 'appointments', do: 'cancel' } }]) });
      B.push({ kind: 'text', text: 'Who', mark: 'head' });
      if (d.with.length) B.push({ kind: 'list', rows: d.with.map(id => ({ text: apptName(id), sub: (apptPerson(id) || {}).role || '', mark: 'hot', button: 'Remove', action: { app: 'appointments', do: 'who', arg: id } })) });
      if (!d.with.length || d.adding) B.push({ kind: 'list', rows: apptPeople().filter(p => !d.with.includes(p.id)).map(p => ({ text: p.name, sub: p.role || '', action: { app: 'appointments', do: 'who', arg: p.id } })) });
      else if (d.with.length < APPT_MAX) B.push({ kind: 'buttons', items: [{ label: 'Add someone', action: { app: 'appointments', do: 'adding' } }] });
      if (d.with.length) {
        B.push({ kind: 'text', text: 'When', mark: 'head' },
          { kind: 'buttons', items: [0, 1, 2].map(k => ({ label: k ? k === 1 ? 'Tomorrow' : WEEKDAYS[weekday(SHIP.time.day + 2)].slice(0, 3) : 'Today', on: d.day === SHIP.time.day + k, action: { app: 'appointments', do: 'day', arg: SHIP.time.day + k } }))
            .concat(d.day > SHIP.time.day + 2 ? [{ label: WEEKDAYS[weekday(d.day)].slice(0, 3) + ' ' + d.day, on: true, action: { app: 'appointments', do: 'day', arg: d.day } }] : []) },
          { kind: 'text', text: hhmm(d.min), mark: 'big' },
          { kind: 'buttons', items: [[-60, '−1h'], [-15, '−15'], [15, '+15'], [60, '+1h']].map(([v, l]) => ({ label: l, action: { app: 'appointments', do: 'time', arg: v } })) },
          { kind: 'text', text: 'Where', mark: 'head' },
          { kind: 'buttons', items: [{ label: 'Pick on the map', action: { app: 'appointments', do: 'map' } }] },
          { kind: 'list', rows: (d.where && !apptPlaces().some(x => x.id === d.where) ? [{ text: apptWhereName(d.where), mark: 'hot', action: { app: 'appointments', do: 'where', arg: d.where } }] : [])
            .concat(apptPlaces().map(x => ({ text: x.name + ', ' + deckIn(x.deck), mark: x.id === d.where ? 'hot' : null, action: { app: 'appointments', do: 'where', arg: x.id } }))) });
        if (d.where) B.push({ kind: 'buttons', items: [{ label: d.with.length > 1 ? 'Ask all ' + d.with.length : 'Ask ' + apptName(d.with[0]).split(' ').slice(-1)[0], action: { app: 'appointments', do: 'ask' } }] });
      }
      B.push({ kind: 'buttons', items: [{ label: 'Cancel', action: { app: 'appointments', do: 'cancel' } }] });
      return { title: 'New appointment', blocks: B };
    }
    if (apptSay) B.push({ kind: 'text', text: apptSay, mark: 'hot' });
    B.push({ kind: 'buttons', items: [{ label: 'New appointment', action: { app: 'appointments', do: 'new' } }] });
    const inv = D.appts.filter(a => a.by && a.status === 'asked');
    if (inv.length) {
      B.push({ kind: 'text', text: 'Invitations', mark: 'head' });
      for (const a of inv) B.push({ kind: 'list', rows: [{ text: apptName(a.by) + ': ' + apptWhereName(a.where), sub: devDayName(Math.floor(a.at / 1440) + 1) + ' ' + devWhen(a.at), mark: 'new' }] },
        { kind: 'buttons', items: [{ label: 'Accept', action: { app: 'appointments', do: 'accept', arg: a.id } }, { label: 'Decline', action: { app: 'appointments', do: 'decline', arg: a.id } }] });
    }
    const up = D.appts.filter(a => a.status === 'yes' && a.at + 15 >= now).sort((a, b) => a.at - b.at);
    B.push({ kind: 'text', text: 'Coming up', mark: 'head' });
    if (!up.length) B.push({ kind: 'text', text: 'Nothing booked.' });
    for (const { a, names } of apptGroups(up)) B.push({ kind: 'list', rows: [{ text: devWhen(a.at) + '  ' + names, sub: devDayName(Math.floor(a.at / 1440) + 1) + ' · ' + apptWhereName(a.where), button: a.occ ? null : 'Cancel it', action: a.occ ? null : { app: 'appointments', do: 'drop', arg: a.id } }] });
    const past = apptGroups(D.appts.filter(a => a.status === 'kept' || a.status === 'missed')).slice(-4).reverse();
    if (past.length) B.push({ kind: 'text', text: 'Earlier', mark: 'head' }, { kind: 'list', rows: past.map(({ a, names }) => ({ text: names + (a.status === 'kept' ? ': met' : ': missed'), sub: devDayName(Math.floor(a.at / 1440) + 1) + ' ' + devWhen(a.at) + ' · ' + apptWhereName(a.where), mark: 'past' })) });
    return { title: 'Appointments', blocks: B };
  } });

// a need's bar lights up for a moment when it rises (0.35.19): section 15's needPulse(k), true for about 1.5 s after
// a "+N" note; while Needs is open the frame loop redraws it when that changes (it blinks with Screen effects on)
const devPulse = k => { if (typeof needPulse !== 'function') return false; try { return !!needPulse(k); } catch (e) { return false; } };
let devPulseKey = '';
function devPulseStep() {
  if (!DEV.open || DEV.app !== 'needs' || typeof needPulse !== 'function' || typeof NEED_KEYS === 'undefined') { devPulseKey = ''; return; }
  const k = NEED_KEYS.map(devPulse).join(); if (k !== devPulseKey) { devPulseKey = k; deviceRefresh(); }
}
// Needs (0.35.28, the user's needs-display redesign): the six needs with section 15's icons and colours (NEED_ICON,
// NEED_COL; amber, NEED_AMBER, under NEED_LOW, as on the HUD strip), then short effect lines ("Hungry: tasks −15%")
// built from section 15's NEED_FX numbers, and your walking speed. Without the icons and colours: the plain bars.
const DEV_FX_WORD = { energy: ['Well rested', 'Tired'], fitness: ['Fit', 'Out of shape'], hunger: ['Well fed', 'Hungry'], hygiene: ['Fresh', 'Unwashed'],
  social: ['Good spirits', 'Lonely'], bathroom: ['Comfortable', 'Need the toilet'] };
const DEV_FX_WHAT = { task: 'tasks', walk: 'walking', drain: 'tiring', socialGain: 'chats' };
const devPct = m => { const p = Math.round((m - 1) * 100); return (p > 0 ? '+' : '−') + Math.abs(p) + '%'; };
function devFxLine(k, side) {                            // 'Hungry: tasks −15%'; null when section 15 has no such effect
  let fx = null; try { fx = typeof NEED_FX !== 'undefined' && NEED_FX[k] && NEED_FX[k][side === 'up' ? 'hi' : 'lo']; } catch (e) { fx = null; }
  if (!fx || !fx[0]) return null;
  const parts = Object.keys(DEV_FX_WHAT).filter(f => typeof fx[0][f] === 'number' && fx[0][f] !== 1).map(f => DEV_FX_WHAT[f] + ' ' + devPct(fx[0][f]));
  const w = DEV_FX_WORD[k] ? DEV_FX_WORD[k][side === 'up' ? 0 : 1] : String(fx[1] || '').split(':')[0];
  return parts.length ? w + ': ' + parts.join(', ') : null;
}
function devNeedLook(k, v) {                             // { icon, color } from section 15, or {} without them
  try {
    const low = v < (typeof NEED_LOW !== 'undefined' ? NEED_LOW : SLOW_BELOW);
    return { icon: typeof NEED_ICON !== 'undefined' && NEED_ICON[k] || null,
      color: typeof NEED_COL !== 'undefined' && NEED_COL[k] ? (low && typeof NEED_AMBER !== 'undefined' ? NEED_AMBER : NEED_COL[k]) : null };
  } catch (e) { return {}; }
}
deviceApp({ id: 'needs', title: 'Needs', icon: 'needs', order: 20, view: () => {
  const n = SHIP.player.needs, fx = needEffects(n), B = [];
  B.push({ kind: 'bars', items: NEED_KEYS.map(k => ({ label: NEED_LABEL[k], value: n[k], level: n[k] < SLOW_BELOW ? 'low' : n[k] < 50 ? 'mid' : '', pulse: devPulse(k),
    mark: fx.marks[k] ? fx.marks[k][0] : null, note: fx.marks[k] ? fx.marks[k][1] : null, ...devNeedLook(k, n[k]) })) });
  const up = [], down = [];
  for (const k of NEED_KEYS) if (fx.marks[k]) { const side = fx.marks[k][0], t = devFxLine(k, side) || fx.marks[k][1]; (side === 'up' ? up : down).push({ kind: 'text', text: (side === 'up' ? '▲ ' : '▼ ') + t, mark: side }); }
  B.push(...down, ...up);                                // what's holding you back first
  const sp = playerSpeed();
  if (sp !== 1) B.push({ kind: 'text', text: 'Walking at ' + Math.round(sp * 100) + '% speed.' });
  return { title: 'Needs', blocks: B };
} });

// Mail: newest first; tap one to read it (and mark it read)
let mailOpen = null;                                     // the message shown in full
// calls home (0.35.27, social B2): Mail from section 20's homeFolks() (Mum, Gran, Jo, Sam) comes first under "From home";
// an open one that section 20's mailPlayable(m) says can be played gets a Play button. Both guarded.
const devHomeFolks = () => { try { const h = typeof homeFolks === 'function' ? homeFolks() : null; return Array.isArray(h) ? h : []; } catch (e) { return []; } };
const devPlayable = m => { try { return typeof mailPlay === 'function' && typeof mailPlayable === 'function' && !!mailPlayable(m); } catch (e) { return false; } };
deviceApp({ id: 'mail', title: 'Mail', icon: 'mail', order: 40, badge: () => mailUnread() || null,
  act(verb, id) {
    const m = SHIP.mail.find(x => x.id === id);
    if (verb === 'read') { mailOpen = mailOpen === id ? null : id; if (m) m.read = true; }
    // 0.35.27 (social B2's calls home): Play hands a recorded message to section 20's mailPlay(m) (synchronous: true when
    // its dialogue opened, false when there's nothing to play or a dialogue is up); on true the device closes for the panel
    else if (verb === 'play' && m && typeof mailPlay === 'function') { let r = false; try { r = mailPlay(m); } catch (e) { DEV.errors.push('mailPlay: ' + (e && e.message || e)); } if (r === true) deviceClose(); }
    else if (verb === 'remember' && m) { memoAdd(m.subject, m.from + ': ' + m.body); deviceNotify({ app: 'memos', text: 'Saved to your memos.', urgent: true }); delete DEV.notes.memos; }
  },
  view: () => {
    if (!SHIP.mail.length) return { title: 'Mail', blocks: [{ kind: 'text', text: 'No mail.' }] };
    const B = [], home = devHomeFolks(), fromHome = SHIP.mail.filter(m => home.includes(m.from)), rest = SHIP.mail.filter(m => !home.includes(m.from));
    for (const m of fromHome.concat(rest)) {
      if (fromHome.length && (m === fromHome[0] || m === rest[0])) B.push({ kind: 'text', text: m === fromHome[0] ? 'From home' : 'Ship mail', mark: 'head' });
      B.push({ kind: 'list', rows: [{ text: (m.read ? '' : '● ') + m.subject, sub: m.from + ', Day ' + (Math.floor(m.at / 1440) + 1) + ' ' + hhmm(((m.at % 1440) + 1440) % 1440),
        mark: m.read ? null : 'new', action: { app: 'mail', do: 'read', arg: m.id } }] });
      if (mailOpen === m.id) B.push({ kind: 'text', text: m.body }, { kind: 'buttons', items: [
        ...(devPlayable(m) ? [{ label: 'Play', action: { app: 'mail', do: 'play', arg: m.id } }] : []),
        { label: 'Remember this', action: { app: 'mail', do: 'remember', arg: m.id } }] });
    }
    return { title: 'Mail', blocks: B };
  } });

// Settings: the screen's colour (the three phosphors), screen effects (the flicker and roll; always off when the
// phone asks for reduced motion), tips on or off
deviceApp({ id: 'settings', title: 'Settings', icon: 'gear', order: 99,
  act(verb, arg) { const st = SHIP.device.settings; if (verb === 'phosphor' && PHOSPHORS[arg]) { st.phosphor = arg; devPhosphorPage(); deviceFire('phosphor'); } else if (verb === 'fx') st.fx = !!arg; else if (verb === 'tips') st.tips = !!arg; else if (verb === 'quiet') st.quiet = !!arg;
    else if (verb === 'heads') SHIP.device.calendarRemind.on = !!arg; else if (verb === 'everyday') SHIP.device.calendarRemind.everyday = !!arg;
    else if (verb === 'ahead' && [15, 30, 60].includes(arg)) SHIP.device.calendarRemind.ahead = arg; },
  view: () => {
    const st = SHIP.device.settings, R = SHIP.device.calendarRemind, on = (v, verb) => [{ label: 'On', action: { app: 'settings', do: verb, arg: true }, on: !!v }, { label: 'Off', action: { app: 'settings', do: verb, arg: false }, on: !v }];
    return { title: 'Settings', blocks: [
      { kind: 'text', text: 'Screen colour' },
      { kind: 'buttons', items: Object.entries(PHOSPHORS).map(([k, label]) => ({ label, action: { app: 'settings', do: 'phosphor', arg: k }, on: st.phosphor === k })) },
      { kind: 'text', text: 'Screen effects (flicker and roll)' }, { kind: 'buttons', items: on(st.fx, 'fx') },
      { kind: 'text', text: 'Tips' }, { kind: 'buttons', items: on(st.tips, 'tips') },
      { kind: 'text', text: 'Quiet off shift (work news as badges, no pop-ups, outside your shift)' }, { kind: 'buttons', items: on(st.quiet, 'quiet') },
      { kind: 'text', text: 'Heads-ups before things on your Schedule start (your appointments always remind you)' }, { kind: 'buttons', items: on(R.on, 'heads') },
      { kind: 'text', text: 'How early' }, { kind: 'buttons', items: [15, 30, 60].map(m => ({ label: m + ' min', action: { app: 'settings', do: 'ahead', arg: m }, on: R.ahead === m })) },
      { kind: 'text', text: 'Meals and your shift too' }, { kind: 'buttons', items: on(R.everyday, 'everyday') }] };
  } });

// Wallet: credits and your locker (0.28.10)
deviceApp({ id: 'wallet', title: 'Wallet', icon: 'wallet', order: 90, view: () => {
  const P = SHIP.player;
  const B = [{ kind: 'text', text: P.credits + ' credits.' + (P.locker.length ? ' In your locker: ' + P.locker.join(', ') + '.' : ' Your locker is empty.') }];
  let ks = []; try { ks = typeof keepsakes === 'function' ? keepsakes() || [] : []; } catch (e) { ks = []; }   // gifts from friends (0.35.22, section 20)
  ks = ks.filter(k => k && typeof k === 'object');      // 0.35.24 (reviewer 2): a row with a missing field never breaks the page
  if (ks.length) B.push({ kind: 'text', text: 'Keepsakes', mark: 'head' }, { kind: 'list', rows: ks.map(k => { const w = String(k.what || 'a keepsake');
    return { text: w.charAt(0).toUpperCase() + w.slice(1), sub: 'From ' + (k.name || k.from || 'a friend') + (Number.isFinite(k.day) ? ', Day ' + k.day : '') }; }) });
  return { title: 'Wallet', blocks: B };
} });

