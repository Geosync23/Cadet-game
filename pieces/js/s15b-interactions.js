// =====================================================================
// 15b. PLAYER INTERACTIONS
// More things to use, the job board and a pointer to where you're going (the interactions engineer).
// Parity: wherever the crew meet a need or pass the time, you can too, with their pose: the bar, lounges and
// common rooms, reading seats, benches, the garden, the music room, the laundry, basins, the gym's water, the
// observatory. Tap the thing; section 15's activity loop does the rest (walk there, the pose, the minutes,
// the gain; walk away to stop), so its rules (needEffects, the ship's effects) apply here too. A second need
// (the bar: food and a little company) comes in from 15b's own frame loop (ixSide). Places crew hold are left alone,
// and so is anything private (a room with someone's bed in it).
// The job board: tap it for the open jobs; take one (section 17's claimJob, as the device's Jobs section does).
// The goal pointer: setGoal({ deck, at: [i, j] | place: id | room: key or name, label }) and clearGoal(). While
// you hold a job the pointer follows it by itself (storage, the machine shop, the machine). On screen: a marker
// over the place; off screen: an arrow at the edge; on another deck: "Take the lift to Deck N". DOM only, so
// no draw calls. Hidden with no goal.
// Hooks: one line in section 15's playerTap (PLAYER_TAPS). Nothing here calls R() or makes geometry.
// =====================================================================
// ---- parity: what a place is for. ixKind(place, item) -> an activity kind below, or null (not ours) ----
// need: the main need, gain over mins; also: { need: gain } on the side, and `with`: extra social with company
const IX_ACTS = {
  ixWater:  { need: 'hunger', gain: 3, mins: 2, pose: 'drink', title: 'Water', done: 'Cold, and it tastes faintly of the recycler. You feel better for it.' },
  ixDrink:  { need: 'hunger', gain: 10, mins: 20, also: { social: 4, leisure: 5 }, with: 6, title: 'A drink', done: 'You finish your drink and push the glass back across.' },   // only with a drink from the bar (0.28.62)
  ixTea:    { need: 'hunger', gain: 5, mins: 6, also: { social: 1 }, with: 3, pose: 'drink', title: 'A cup of tea', done: 'Tea, the ship\'s real fuel.' },
  ixRead:   { need: 'energy', gain: 5, mins: 20, also: { social: 2, leisure: 6 }, with: 3, title: 'Reading', done: 'You put the book down feeling rested.' },
  ixLounge: { need: 'social', gain: 4, mins: 20, also: { energy: 4 }, with: 8, title: 'Taking it easy', done: 'You get up, unhurried.' },
  ixStars:  { need: 'energy', gain: 6, mins: 15, also: { social: 2, leisure: 6 }, with: 4, title: 'Stargazing', done: 'The stars don\'t move much, but you feel calmer for watching them.' },
  ixGarden: { need: 'leisure', gain: 25, mins: 30, also: { social: 4, fitness: 2 }, with: 4, pose: 'water', title: 'Tend a bed', done: 'The beds are watered. Your hands smell of tomato leaves.' },   // a hobby (the user's, 0.28.65): section 15's 'garden', 30 minutes for +25 leisure
  ixMusic:  { need: 'social', gain: 8, mins: 20, also: { energy: 2, leisure: 6 }, with: 4, pose: 'play', title: 'Playing music', done: 'You stop playing. Someone, somewhere, claps.' },   // leisure +6 on these four (0.28.64, the plan's table)
  ixFold:   { need: 'hygiene', gain: 12, mins: 15, pose: 'fold', title: 'Doing your laundry', done: 'Clean clothes, folded, ready for the locker.' },
  ixBasin:  { need: 'hygiene', gain: 6, mins: 2, pose: 'stand', title: 'Washing up', done: 'Hands and face washed.' },
};
const IX_SKIP = /\bbed\b|bunk|berth|notice|rota|board|sign|journal|plaque|chart|screen|messages|model of|survey|^washer\b/i;   // taps that stay what they were
const IX_BEDS = /(herb|flower|salad|seed|grow|raised) bed/i;   // garden beds aren't for sleeping
const IX_NEAR = 2.4, IX_COMPANY = 3.5;                    // IX_NEAR: from the edge of the thing you tapped
// how far a place's spot is from the thing tapped, measured to its outline (a long table, a big garden bed)
const ixBox = new THREE.Box3(), ixP = new THREE.Vector3();
function ixDist(it, s) { ixBox.setFromObject(it.hit); ixP.set(s.x, (ixBox.min.y + ixBox.max.y) / 2, s.z); return ixBox.distanceToPoint(ixP); }
const ixRoomName = pl => ((typeof deckDef !== 'undefined' && deckDef && deckDef.rooms && deckDef.rooms[pl.room]) || {}).name || '';
function ixKind(pl, it) {
  const t = pl.type, a = pl.anim || '', sit = pl.pose === 'sit', title = it ? it.t : '';
  if (t === 'gym') return a === 'drink' ? 'ixWater' : 'gym';                 // the gym's kit is section 15's; its water cooler is ours
  if (t === 'lounge-seat' || t === 'common-room') {
    if (/observ/i.test(ixRoomName(pl))) return 'ixStars';
    if (a === 'drink') return sit ? (SHIP.player.drink ? 'ixDrink' : null) : 'ixTea';   // a bar stool: your drink from the bar (barTap, 0.28.62), else just a seat
    if (!sit) return /telescope|window/i.test(title) ? 'ixStars' : 'ixTea';  // the kettle, the hot water, the telescope
    return a === 'read' ? 'ixRead' : 'ixLounge';
  }
  if (t === 'bench') return null;                        // plain seats (benches, garden seats, beanbags) are section 15's sit-anywhere (sitTap)
  if (t === 'garden') return sit ? null : 'ixGarden';
  if (t === 'music') return a === 'play' || !sit || /guitar|piano|keys|drum/i.test(title) ? 'ixMusic' : null;
  if (t === 'laundry') return 'ixFold';
  if (t === 'basin') return 'ixBasin';
  return null;
}
Object.assign(PLAYER_ACTS, IX_ACTS);
// company: crew settled near the spot (or anyone sitting in the same room)
const ixCompany = s => DECK_CREW.filter(c => c.settled && c.spot && (Math.hypot(c.x - s.x, c.z - s.z) < IX_COMPANY || c.spot.room === s.room && s.room)).length;
const ixBond = s => typeof bondBest === 'function' ? bondBest(DECK_CREW.filter(c => c.settled && c.spot && (Math.hypot(c.x - s.x, c.z - s.z) < IX_COMPANY || c.spot.room === s.room && s.room)).map(c => (c.p || c).id)) : ixCompany(s) > 0 ? 1 : 0;   // 0.28.43: the best bond there
// the side gains as the minutes pass (ixFrame, below, each frame while one of ours runs): also{}, plus `with` more
// social for company (scaled by needEffects' socialGain). They follow A.done, so needEffects' task speed applies
function ixSide(A) {
  if (A.kind === 'ixDrink' && !A.o.drink && SHIP.player.drink) { A.o.drink = SHIP.player.drink; SHIP.player.drink = null; A.def.done = 'You finish your ' + BAR_DRINKS[A.o.drink].short + '.'; }   // the drink from the bar goes as you drink it (0.28.62)
  const d = A.def, f = Math.max(0, Math.min(1, A.done / d.mins));
  if (!A.o.ixSide) {
    let mult = 1; try { const e = typeof needEffects === 'function' ? needEffects(SHIP.player.needs) : null; if (e && isFinite(e.socialGain)) mult = e.socialGain; } catch (e) { mult = 1; }
    const side = { ...(d.also || {}) };
    if (A.o.company && d.with) side.social = (side.social || 0) + d.with * mult * (A.o.company === true ? 1 : A.o.company);   // by the best bond there (0.28.43)
    if (side[d.need]) { d.gain += side[d.need]; delete side[d.need]; }   // more of the main need: section 15 spreads d.gain over the minutes
    A.o.ixSide = side; A.o.ixGiven = {};
    if (A.o.company && d.with) d.done = (d.done || '') + ' The company helped.';
  }
  const fx = typeof playerFx === 'function' ? playerFx() : null, n = SHIP.player.needs;
  for (const k in A.o.ixSide) {
    const want = A.o.ixSide[k] * f, give = want - (A.o.ixGiven[k] || 0);
    if (give > 0) { n[k] = needClamp(n[k] + give * fxR(fx, k)); A.o.ixGiven[k] = want; }
  }
}
// the pose: the crew's own (poseOf, section 8b) for the place; seats with nothing particular read alone, talk in company
function ixPose(kind, pl, spot, company) {
  const base = spot.pose || pl.pose || 'stand', own = typeof poseOf === 'function' ? poseOf(pl) : base;
  if (kind === 'ixMusic') return base === 'sit' ? 'sit:play' : 'play';
  if (kind === 'ixGarden' || kind === 'ixFold' || kind === 'ixWater') return IX_ACTS[kind].pose;
  if (kind === 'ixTea') return 'drink';
  if (kind === 'ixDrink') return base === 'sit' ? 'sit:drink' : 'drink';
  if (base === 'sit' && own === 'sit') return company ? 'sit:talk' : kind === 'ixStars' ? 'sit' : 'sit:read';
  return own;
}
// a machine you tapped (section 17's list; stand-ins don't count): its tap is the machine's own (repairs, using it)
// (section 15's machineTap rule exactly: a real machine within MACHINE_NEAR); washers too, which machineUse runs
const ixMachine = at => typeof machineList === 'function' && machineList().some(m => !m.stub && m.deck === deckDef.num && m.at && (() => { const c = cellPos(...m.at); return Math.hypot(c.x - at.x, c.z - at.z) < (typeof MACHINE_NEAR !== 'undefined' ? MACHINE_NEAR : 1); })());
// would section 15's own ACT_TAP take this tap? Then leave it to them
function ixTheirs(it, at) {
  const rule = ACT_TAP.find(r => r[0].test(it.t)); if (!rule) return false;
  return [...PLACE_OF.values()].some(pl => rule[1].includes(pl.type) && (() => { const s = placeSpot(pl.id); return s && Math.hypot(s.x - at.x, s.z - at.z) < ACT_NEAR; })());
}
// ---- chores without a machine (section 17's CHORES: a lamp, a vent, a delivery, an inspection round): tap something at
// the next stop and do its minutes; jobStepDone (17) marks the stop. Parts first, from main storage, when it needs any.
// After the last stop the work is done (17 sets workDone) and the job waits to be turned in at the job board (Pillar 3:
// "take and turn in at the board"). Chores on a machine (calibrate, faults, filters) go through section 15's repair. ----
const IX_STOP = { lamp: ['Replacing the lamp', 'work'], vent: ['Cleaning the vent', 'work'], pickup: ['Picking it up', 'browse'], drop: ['Dropping it off', 'browse'],
  inspect: ['Inspecting', 'work'], fault: ['Clearing the fault', 'work'], fetch: ['Main storage', 'browse'] };
Object.assign(PLAYER_ACTS, { ixStop: { mins: 10, pose: 'work', title: 'Your job' } });
const ixChore = () => { const j = typeof myJob === 'function' && typeof jobStepDone === 'function' && typeof jobStops === 'function' ? myJob() : null; return j && (j.kind === 'chore' || typeof JOB_KINDS === 'object' && JOB_KINDS && JOB_KINDS[j.kind]) && !j.machine ? j : null; };   // a registered kind (17's jobKindAdd) walks like a chore (Pillar 5)
function ixNextStop(j) { const st = jobStops(j), k = st.findIndex(x => !x.done); return k < 0 ? null : { k, s: st[k] }; }
// first tips (Pillar 3, C13: 15b says when, the device draws them): tipShow(id, text) shows each once, when it's there
function ixTip(id, text) { if (typeof tipShow === 'function') { try { tipShow(id, text); } catch (e) { /* the tips aren't ours */ } } }
// 0.28.55 (the lead): at a chore's stop a thing you can use does its own thing. Section 15's playerTap asks ixChoreLast
// last of all (scenery with nothing of its own to do), and with own = true just before machineTap, for a stop that is that
// machine's own panel (section 18's stormBallasts at the lights). The floor at the stop and the Repair button: jobHere
function ixChoreLast(it, at, own) {
  const j = ixChore(), nx = j && !j.workDone ? ixNextStop(j) : null, pl = nx && nx.s.places[0] && PLACE_OF.get(nx.s.places[0]);
  return own && !(pl && pl.machine) ? false : ixChoreTap(it, at);
}
function ixChoreTap(it, at) {
  const j = ixChore(); if (!j || j.workDone) return false;
  const nx = ixNextStop(j); if (!nx) return false;
  const { k, s: st } = nx, room = roomAt(...cellAt(at.x, at.z)), P = SHIP.player, o = { title: it.t, flavour: it.x, job: j.id, ixStep: k };
  if (st.step === 'fetch') {                             // parts off the shelves in main storage, Deck 5
    if (deckDef.num !== 5 || room !== 'r') return false;
    const need = jobNeeds(j, { fitted: [] }, P.carry);
    if (!need.length) { jobStepDone(j.id, k); ixGoalAt = -1; toast(it.t, 'You have what the job needs: ' + partList(P.carry) + '.'); return true; }
    if (P.carry.length >= CARRY_MAX) { toast(it.t, 'Your hands are full (' + partList(P.carry) + '). Put something back first.'); return true; }
    if (typeof shelfWrong === 'function' && shelfWrong(it)) return true;   // the right shelf (0.33.41)
    const pl = jobPlaceNear('storage', 'r', at);
    actStart('ixStop', pl ? pl.id : null, { ...o, ixFetch: true, pose: 'browse', after: 'You look for ' + partList(need) + '.' });
    if (ACT && ACT.kind === 'ixStop') { ACT.def.mins = PLAYER_ACTS.fetch ? PLAYER_ACTS.fetch.mins : 4; ACT.def.title = 'Main storage'; }
    return true;
  }
  if (st.deck !== deckDef.num) return false;
  const pid = st.places[0], spot = pid && PLACE_OF.has(pid) ? placeSpot(pid) : null;
  if (!spot || !(it.hit ? ixDist(it, spot) < IX_NEAR + .6 : Math.hypot(spot.x - at.x, spot.z - at.z) < JOB_REACH) && PLACE_OF.get(pid).room !== room) return false;   // no thing (jobHere, 0.28.52): from the point
  if (st.step === 'drop' && crateDown(j)) { toast(it.t, 'The crate is where you set it down, on ' + deckIn(SHIP.player.crate.deck) + '. Pick it up first: follow the marker.'); return true; }   // Put down (0.28.60)
  if (typeof workStep === 'function' && workStep(j, st, k, spot)) return true;   // look, choose, turn, wait (section 15, Pillar 5)
  const [title, pose] = IX_STOP[st.step] || ['Your job', 'work'];
  // the stop's spot, not the place: a lamp over the lift queue is yours to change even with someone waiting there
  actStart('ixStop', null, { ...o, pose, spot: { ...spot, id: null, pose: 'stand' }, after: j.title + ': about ' + Math.ceil(st.mins || 10) + ' minutes. Walk away to pause.' });
  if (ACT && ACT.kind === 'ixStop') { ACT.def.mins = st.mins || 10; ACT.def.title = title; }
  return true;
}
// what you carry for your job between stops (section 15 asks, for the held prop: 8b's '+toolbox', '+carry'), after its own
// cases (a cart, parts in hand, a tray): a delivery's crate from the pickup to the drop; a toolbox for any other job you're
// on until its work is done (repairs, lamps, vents, rounds). Nothing for cart runs (the cart) or with no job.
function ixHold() {
  const j = typeof myJob === 'function' ? myJob() : null;
  if (!j || j.workDone || j.kind === 'restock') return null;
  if (j.kind === 'chore' && j.chore === 'delivery' && typeof jobStops === 'function') {
    const st = jobStops(j), pick = st.findIndex(x => x.step === 'pickup'), drop = st.findIndex(x => x.step === 'drop');
    return pick >= 0 && st[pick].done && !(drop >= 0 && st[drop].done) && !crateDown(j) ? 'carry' : null;   // not while it's set down (Put down, 0.28.60)
  }
  const kd = typeof JOB_KINDS === 'object' && JOB_KINDS && JOB_KINDS[j.kind];   // a registered kind's own (17's jobKindAdd def.hold: 'datapad' for a round, Pillar 5)
  let h = null; try { h = kd ? typeof kd.hold === 'function' ? kd.hold(j) : kd.hold : null; } catch (e) { h = null; }   // or of the job (a haul: 'cart', then 'cartfull')
  return typeof h === 'string' && typeof HOLDS !== 'undefined' && HOLDS[h] ? h : h === null && kd && 'hold' in kd ? null : 'toolbox';
}
// a stop's minutes are done (ixFrame sees the activity step out): mark it with section 17, and say what's next
function ixStopDone(A) {
  const j = ixChore(), P = SHIP.player; if (!j || j.id !== A.o.job) return;
  if (A.o.ixFetch) {
    const got = [], none = [];
    for (const p of jobNeeds(j, { fitted: [] }, P.carry)) { if (P.carry.length >= CARRY_MAX) break; if (takePart(p)) { P.carry.push(p); got.push(p); } else none.push(p); }
    if (!got.length) { toast('Main storage', 'None on the shelves: ' + none.join(', ') + '. The next delivery is on Wednesday.'); return; }
    jobStepDone(j.id, A.o.ixStep); ixGoalAt = -1;
    toast('Main storage', 'You take ' + partList(got) + '. Now ' + j.title.charAt(0).toLowerCase() + j.title.slice(1) + '.'); return;
  }
  const r = jobStepDone(j.id, A.o.ixStep); ixGoalAt = -1;
  if (!r.ok) { toast('Your job', 'The job isn\'t yours any more.'); return; }
  if (r.wrong) { device.refresh(); return; }               // a wrong part: 24k's caseFitted has said so
  if (r.retry) { toast(A.def.title, typeof r.say === 'string' && r.say ? r.say : 'Not quite. Try again.'); device.refresh(); return; }   // the kind said no (17's def.veto)
  const say = typeof r.say === 'string' && r.say ? r.say + ' ' : '';   // the kind's own words (its stepDone, through 17)
  if (r.done) {
    for (const p of j.parts) { const i = P.carry.indexOf(p); if (i >= 0) P.carry.splice(i, 1); }   // the lamp went in: it's used
    toast('Work done', say + j.title + ': done. Turn it in at the job board in the Works bay, Deck 5.');
    ixTip('turnin', 'Head back to the board to turn it in.');
  } else toast(A.def.title, say + 'Done here. ' + r.left + (r.left === 1 ? ' stop' : ' stops') + ' to go: follow the marker.');
  device.refresh();
}
// the tap (section 15's playerTap, through PLAYER_TAPS): the job board, or a place to use
function ixTap(it, at, point) {
  if (/job board/i.test(it.t) && typeof jobsBoard === 'function') { approach(at.clone(), it.front, it.depth, () => ixBoard.open(it)); return true; }
  if (/^ship health$/i.test(it.t) && typeof shipHealthRows === 'function') { approach(at.clone(), it.front, it.depth, () => ixHealth.open()); return true; }
  if (IX_SKIP.test(it.t) && !IX_BEDS.test(it.t) || it.lift || ixTheirs(it, at) || ixMachine(at)) return false;
  const room = roomAt(...cellAt(at.x, at.z));             // the thing's own room: never a place through a wall
  const near = [...PLACE_OF.values()].map(pl => [pl, placeSpot(pl.id), ixKind(pl, it)])
    .filter(([pl, s, k]) => k && s && (!room || pl.room === room) && !privatePlace(pl) && ixDist(it, s) < IX_NEAR)
    .sort((m, n) => Math.hypot(m[1].x - point.x, m[1].z - point.z) - Math.hypot(n[1].x - point.x, n[1].z - point.z));
  if (!near.length) return false;
  const busy = id => heldBy(id) || (typeof placeBusy === 'function' && placeBusy(id) && playerHolds() !== id);
  const free = near.find(([pl]) => !busy(pl.id));
  if (!free) { const a = heldBy(near[0][0].id); toast(it.t, 'In use' + (a ? ': ' + a.p.name + ' is there.' : '.') + ' ' + it.x); return true; }
  const [pl, spot, kind] = free, company = ixBond(spot);   // 0 or the best bond (0.28.43; truthy as before)
  const pose = kind === 'gym' ? (typeof poseOf === 'function' ? poseOf(pl) : pl.anim || 'lift') : ixPose(kind, pl, spot, company);
  actStart(kind, pl.id, { pose, title: it.t, flavour: it.x, company });
  return true;
}
PLAYER_TAPS.push(ixTap);

// ---- Put down (0.28.60, the design doc's Repair step: "whenever your hands hold anything, a small 'Put down' button
// lets you set it down; nothing is lost and the job stays yours"). A thumb-sized button, bottom right (#putDown), shown
// while your hands hold a part, a tray or a delivery's crate. One tap puts all of them down: parts go back on the main
// storage shelf (returnPart; a part your job makes waits finished at the machine shop's lathe instead, P.work.make), and
// a chore's fetch stop opens again so you fetch them later; a tray is just set down (0.60.7: no tray return); the crate is set down where
// you stand (SHIP.player.crate: { job, deck, x, z, at }, saved) and a tap on it picks it up again. Left till 05:00, or
// once the job isn't yours, the crew take it back to the pickup (its pickup stop opens again). A gift and the kit bag
// aren't put down: they have their own ways (give it to someone; your locker in Bunk 1). Hidden while you're busy. ----
const PUT_NEAR = .6;                                     // a tap this close to the set-down crate picks it up (m)
let PUT_CRATE = null;                                    // the crate's look, made the first time one is set down
{ const c = SAVED && SAVED.player && SAVED.player.crate; SHIP.player.crate = c && (typeof c.job === 'string' || typeof c.job === 'number') && DECKS[c.deck] && isFinite(c.x) && isFinite(c.z) ? { job: c.job, deck: +c.deck, x: +c.x, z: +c.z, at: isFinite(c.at) ? +c.at : 0 } : null; }
SAVE_EXTRA.push(s => { const p = s.player || (s.player = {}); if (SHIP.player.crate) p.crate = { ...SHIP.player.crate }; });
const putGift = x => typeof giftOf === 'function' && !!giftOf(x);
const putParts = () => SHIP.player.carry.filter(x => x !== KIT_BAG && !putGift(x));
function crateDown(j) { const c = SHIP.player.crate; return !!(c && j && c.job === j.id); }
function putDelivery() {                                 // your delivery job, with its pickup and drop stop indexes
  const j = typeof myJob === 'function' ? myJob() : null;
  if (!j || j.workDone || j.kind !== 'chore' || j.chore !== 'delivery' || typeof jobStops !== 'function') return null;
  const st = jobStops(j), pick = st.findIndex(x => x.step === 'pickup'), drop = st.findIndex(x => x.step === 'drop');
  return pick < 0 ? null : { j, st, pick, drop };
}
const crateHeld = () => { const d = putDelivery(); return !!d && d.st[d.pick].done && !(d.drop >= 0 && d.st[d.drop].done) && !crateDown(d.j); };
const trayHeld = () => !!SHIP.player.tray;
const putWhat = () => putParts().length > 0 || trayHeld() || crateHeld() || typeof hamperHeld === 'function' && hamperHeld();   // section 21b's laundry hamper (0.42.40)
function stepUndo(j, step) {                             // open a stop of your job again (section 17's stepsDone)
  const k = jobStops(j).findIndex(x => x.step === step); if (k < 0 || !Array.isArray(j.stepsDone)) return;
  j.stepsDone = j.stepsDone.filter(x => x !== k); if (typeof MACH_REV !== 'undefined') MACH_REV++;
}
function putDown() {
  if (typeof ride !== 'undefined' && ride || !putWhat()) return false;   // never mid lift ride (reviewer 1g)
  const P = SHIP.player, said = [];
  if (ACT) { actEnd(true); player.stop(); }              // whatever you were walking to, with it in your hands, is off
  const parts = putParts();
  if (parts.length) {
    const mw = typeof myWork === 'function' && jobsOn() ? myWork() : null, made = mw && madeHere(mw.j), back = [];
    let kept = null;
    for (const p of parts) {
      if (p === made && !kept && !(P.work.make && P.work.make.part)) { kept = p; P.work.make = { part: p, done: makeMins(mw.j) }; }   // made, not stocked: it waits at the lathe
      else if (typeof returnPart === 'function' && returnPart(p)) back.push(p); else continue;
      P.carry.splice(P.carry.indexOf(p), 1);
    }
    const ch = typeof ixChore === 'function' ? ixChore() : null;
    if (ch && !ch.workDone && jobNeeds(ch, { fitted: [] }, P.carry).length) stepUndo(ch, 'fetch');   // fetch them again before the stop
    if (back.length) said.push('You put ' + partList(back) + ' back on the shelf in main storage, Deck 5. Fetch ' + (back.length > 1 ? 'them' : 'it') + ' again when you need ' + (back.length > 1 ? 'them' : 'it') + '.');
    if (kept) said.push('The ' + kept + ' waits for you at the lathe in the machine shop, Deck 5.');
  }
  if (trayHeld()) { P.tray = null; said.push('You set your tray down. Someone will clear it.'); }   // no tray return (the user, 0.60.7): a tray just goes
  if (crateHeld()) {
    const d = putDelivery(), p = player.obj.position, f = player.face || 0;
    P.crate = { job: d.j.id, deck: deckDef.num, x: p.x + Math.sin(f) * .45, z: p.z + Math.cos(f) * .45, at: shipNow() };
    said.push('You set the crate down here. Tap it to pick it up again; your job stays yours.');
  }
  if (typeof hamperPut === 'function') { const h = hamperPut(); if (h) said.push(h); }   // section 21b (0.42.40)
  if (typeof ixGoalAt !== 'undefined') ixGoalAt = -1;
  if (typeof device !== 'undefined' && device.refresh) device.refresh();
  toast('Put down', said.join(' ') + (P.carry.length ? ' Still in your hands: ' + partList(P.carry) + '.' : ''));
  return true;
}
function crateUp(quiet) {                                // pick the set-down crate up again
  const d = putDelivery(); if (!d || !crateDown(d.j)) return false;
  SHIP.player.crate = null; if (typeof ixGoalAt !== 'undefined') ixGoalAt = -1;
  if (!quiet) toast('Your job', 'You pick the crate up again. ' + d.j.title + '.');
  return true;
}
function crateTap(point) {                               // a tap on (or right by) the set-down crate: walk there, pick it up
  const c = SHIP.player.crate; if (!c || typeof deckDef === 'undefined' || c.deck !== deckDef.num || typeof ray === 'undefined') return false;
  const o = ray.ray.origin, dr = ray.ray.direction; let best = Math.hypot(point.x - c.x, point.z - c.z);
  for (let y = 0; y <= .5; y += .1) { const k = (y - o.y) / dr.y; if (k > 0) best = Math.min(best, Math.hypot(o.x + dr.x * k - c.x, o.z + dr.z * k - c.z)); }
  if (best > PUT_NEAR) return false;
  if (!crateDown(putDelivery() && putDelivery().j)) return false;
  approach(new THREE.Vector3(c.x, 0, c.z), 0, 0, () => crateUp(false));
  return true;
}
function putCrateLook() {                                // a small crate on the floor, made once (no R())
  const g = new THREE.Group();
  box(.5, .36, .4, KM.crate, 0, .185, 0, g);                 // just off the floor: no coplanar faces
  for (const y of [.09, .27]) box(.52, .04, .42, M.slateDark, 0, y, 0, g);
  box(.22, .06, .02, KM.label, 0, .18, .205, g);
  g.visible = false; scene.add(g); return g;
}
// the night tidy (the lead's call): a crate set down goes back at the first 05:00 after it was set down
const PUT_TIDY = 5 * 60, putTidyAt = at => (Math.floor((at - PUT_TIDY) / 1440) + 1) * 1440 + PUT_TIDY;
let putShown = null, putLast = '';
function putFrame() {
  requestAnimationFrame(putFrame);
  if (typeof deckDef === 'undefined' || !deckDef || typeof player === 'undefined') return;
  const P = SHIP.player, c = P.crate;
  if (c) {                                               // the crew take it back: the job isn't yours any more, or overnight
    const d = putDelivery(), gone = !d || !crateDown(d.j), night = shipNow() >= putTidyAt(c.at);
    if (gone || night) {
      P.crate = null; if (typeof ixGoalAt !== 'undefined') ixGoalAt = -1;
      if (!gone) { stepUndo(d.j, 'pickup'); toast('Your job', 'The crew took the crate you left back to the pickup in the night tidy. Pick it up there again: ' + d.j.title.charAt(0).toLowerCase() + d.j.title.slice(1) + '.'); }
    }
  }
  const here = !!(P.crate && P.crate.deck === deckDef.num);
  if (here && !PUT_CRATE) PUT_CRATE = putCrateLook();
  if (PUT_CRATE) { PUT_CRATE.visible = here; if (here) PUT_CRATE.position.set(P.crate.x, 0, P.crate.z); }
  const b = document.getElementById('putDown'); if (!b) return;
  const busy = ACT && ACT.phase !== 'walk' || P.cart || (typeof ride !== 'undefined' && ride) || (typeof PAUSE !== 'undefined' && PAUSE.on) || (typeof DEV !== 'undefined' && DEV.open)
    || document.body.classList.contains('dlgon') || !document.getElementById('lift').hidden;
  const show = !busy && putWhat();
  if (show !== putShown) { putShown = show; b.hidden = !show; }
  if (!show) return;
  const t = document.getElementById('toast'), up = t && t.classList.contains('show') && innerWidth <= 720 ? t.offsetHeight + 10 : 0;   // phones: above a toast
  const key = up + '';
  if (key !== putLast) { putLast = key; b.style.bottom = up ? 'calc(' + (18 + up) + 'px + env(safe-area-inset-bottom))' : ''; }
}
(() => {
  const st = document.createElement('style');
  st.textContent = '#putDown{position:fixed;right:calc(12px + env(safe-area-inset-right));bottom:calc(18px + env(safe-area-inset-bottom));z-index:2;min-height:48px;min-width:48px;padding:0 16px;font-size:14px;font-weight:600;gap:8px;touch-action:manipulation;transition:bottom .35s}'
    + '#putDown[hidden]{display:none}#putDown svg{width:19px;height:19px}@media (prefers-reduced-motion:reduce){#putDown{transition:none}}';
  document.head.appendChild(st);
  const b = document.createElement('button'); b.id = 'putDown'; b.type = 'button'; b.hidden = true;
  b.setAttribute('aria-label', 'Put down what you\'re holding');
  b.innerHTML = '<svg viewBox="0 0 24 24"><path d="M12 4v10"/><path d="M8 10l4 4 4-4"/><path d="M5 19h14"/></svg><span>Put down</span>';
  b.addEventListener('pointerdown', e => e.stopPropagation());
  b.onclick = e => { e.stopPropagation(); putDown(); };
  document.body.appendChild(b);
  requestAnimationFrame(putFrame);
})();

// ---- the look: the board panel and the goal pointer, made here (DOM and CSS), so the HTML stays as it was ----
(() => {
  const st = document.createElement('style');
  st.textContent = '.ixboard .ixjob{display:flex;align-items:center;gap:8px;margin:0 0 6px;padding:8px 10px;border:1px solid var(--line);border-radius:12px;background:rgba(38,52,58,.55)}'
    + '.ixboard .ixjob i{flex:none;width:6px;align-self:stretch;border-radius:3px;background:#5fd6c6}.ixboard .ixjob.soon i{background:#e8c06a}.ixboard .ixjob.urgent i{background:#e0503f}'
    + '.ixboard .ixjob.taken{opacity:.55}.ixboard .ixjob div{flex:1;min-width:0}.ixboard .ixjob b{display:block;font-size:13.5px;font-weight:600}.ixboard .ixjob small{display:block;font-size:12px;color:var(--muted);margin-top:1px}'
    + '.ixboard .ixjob button{flex:none;padding:6px 11px;font-size:12.5px}.ixboard .ixlist{flex:1 1 auto;min-height:0;overflow-y:auto;touch-action:pan-y;-webkit-overflow-scrolling:touch}'
    // the panel's own box (0.37.6): centred, always inside the screen and its safe areas, scrolling inside when tall
    + '.ixpanel{left:50%;top:50%;transform:translate(-50%,-50%);display:flex;flex-direction:column;width:min(380px,calc(100vw - 24px - env(safe-area-inset-left) - env(safe-area-inset-right)));'
    + 'max-height:calc(100vh - 24px - env(safe-area-inset-top) - env(safe-area-inset-bottom));max-height:calc(100dvh - 24px - env(safe-area-inset-top) - env(safe-area-inset-bottom))}.ixpanel[hidden]{display:none}'
    + '.ixpanel h2,.ixpanel>p,.ixpanel .stay{flex:none}'
    // the ship health panel's rows (0.37.6): a label, its bar and number, the condition word; colours by state
    + '.ixbar{display:grid;grid-template-columns:minmax(0,1fr) 34px 58px;grid-template-areas:"n v w" "b b b";gap:3px 8px;align-items:center;margin:0 0 9px;font-size:13.5px}'
    + '.ixbar span{grid-area:n}.ixbar b{grid-area:v;text-align:right;font-variant-numeric:tabular-nums;font-weight:600}.ixbar em{grid-area:w;font-style:normal;font-size:12px;color:var(--muted);text-align:right}'
    + '.ixbar i{grid-area:b;height:7px;border-radius:4px;background:#26343a;overflow:hidden}.ixbar i u{display:block;height:100%;background:#4cc3b5}'
    + '.ixbar.worn i u{background:#d9b25a}.ixbar.poor i u{background:#e0904f}.ixbar.failing i u{background:#e0503f}.ixbar.whole{font-size:15px;padding-bottom:8px;border-bottom:1px solid var(--line)}'
    + '.ixnote{margin:0 2px 6px;font-size:12.5px;color:#cfd9dc;line-height:1.4}.ixnote.head{margin-top:8px;color:var(--muted);text-transform:uppercase;letter-spacing:.04em;font-size:11.5px}'
    + '#ixGoal{position:fixed;left:0;top:0;z-index:2;pointer-events:none;width:0;height:0}#ixGoal[hidden]{display:none}'
    + '#ixGoal .ixarr{position:absolute;left:-19px;top:-19px;width:38px;height:38px;border-radius:50%;background:rgba(13,21,33,.82);border:2px solid #e8c06a;box-shadow:0 2px 10px rgba(0,0,0,.45)}'
    + '#ixGoal .ixarr::after{content:"";position:absolute;left:13px;top:10px;border-style:solid;border-width:8px 0 8px 14px;border-color:transparent transparent transparent #e8c06a}'
    + '#ixGoal .ixpin{position:absolute;left:-11px;top:-30px;width:22px;height:22px;animation:ixbob 1.4s ease-in-out infinite}'
    + '#ixGoal .ixpin::after{content:"";position:absolute;left:1px;top:2px;border-style:solid;border-width:14px 10px 0 10px;border-color:#e8c06a transparent transparent transparent;filter:drop-shadow(0 1px 3px rgba(0,0,0,.6))}'
    + '#ixGoal .ixlab{position:absolute;left:0;top:14px;transform:translateX(-50%);white-space:nowrap;max-width:min(260px,70vw);overflow:hidden;text-overflow:ellipsis;font-size:12.5px;padding:3px 9px;border-radius:999px;background:rgba(13,21,33,.82);border:1px solid rgba(232,192,106,.5);color:#f2e3bf}'
    + '@keyframes ixbob{50%{transform:translateY(-5px)}}@media (prefers-reduced-motion:reduce){#ixGoal .ixpin{animation:none}}';
  document.head.appendChild(st);
  const g = document.createElement('div'); g.id = 'ixGoal'; g.hidden = true; g.setAttribute('aria-live', 'polite');
  g.innerHTML = '<div class="ixarr"></div><div class="ixpin"></div><div class="ixlab"></div>';
  document.body.appendChild(g);
  const b = document.createElement('div'); b.className = 'lift ixboard ixpanel';   // not .device: that's the device's own sheet (section 19)
  b.id = 'ixBoard'; b.hidden = true;
  b.setAttribute('role', 'dialog'); b.setAttribute('aria-labelledby', 'ixBoardT');
  b.innerHTML = '<h2 id="ixBoardT">Job board</h2><p id="ixBoardX">Pick a job and take it.</p><div class="ixlist" id="ixBoardL"></div><button class="stay" id="ixBoardC">Close</button>';
  document.body.appendChild(b);
  const hp = document.createElement('div'); hp.className = 'lift ixboard ixpanel'; hp.id = 'ixHealth'; hp.hidden = true;   // the ship health panel, the same family
  hp.setAttribute('role', 'dialog'); hp.setAttribute('aria-labelledby', 'ixHealthT');
  hp.innerHTML = '<h2 id="ixHealthT">Ship health</h2><p id="ixHealthX">Every system aboard, how well it\'s running right now.</p><div class="ixlist" id="ixHealthL"></div><button class="stay" id="ixHealthC">Close</button>';
  document.body.appendChild(hp);
  // a tap outside an open panel closes it, and goes no further (no walk), like the lift's panel
  addEventListener('pointerdown', e => {
    for (const id of ['ixBoard', 'ixHealth']) { const el = document.getElementById(id);
      if (!el.hidden && !el.contains(e.target)) { e.stopPropagation(); e.preventDefault(); (id === 'ixBoard' ? ixBoard : ixHealth).close(); } }
  }, true);
})();
// ---- the ship health board (Deck 1's vestibule, the Works bay): tap it for every system's condition (section 17's
// shipHealthRows, read only), the ship's overall health, what's worst in each, and the jobs on the board ----
const IX_STATE = { fine: 'Good', worn: 'Worn', poor: 'Poor', failing: 'Failing' };
const ixHealth = (() => {
  const el = document.getElementById('ixHealth'), list = document.getElementById('ixHealthL'); let back = null, drawnAt = -1;
  const bar = (r, whole) => { const d = document.createElement('div'), n = document.createElement('span'), v = document.createElement('b'), w = document.createElement('em'), i = document.createElement('i'), u = document.createElement('u');
    d.className = 'ixbar ' + r.state + (whole ? ' whole' : ''); n.textContent = r.name; v.textContent = r.value; w.textContent = IX_STATE[r.state] || r.state; u.style.width = Math.max(0, Math.min(100, r.value)) + '%';
    i.appendChild(u); d.append(n, v, w, i); d.setAttribute('role', 'meter'); d.setAttribute('aria-label', r.name + ', ' + (IX_STATE[r.state] || r.state)); d.setAttribute('aria-valuenow', r.value); d.setAttribute('aria-valuemin', 0); d.setAttribute('aria-valuemax', 100); list.appendChild(d); };
  const note = (t, head) => { const p = document.createElement('p'); p.className = 'ixnote' + (head ? ' head' : ''); p.textContent = t; list.appendChild(p); };
  const api = {
    open() { back = document.activeElement; el.hidden = false; api.draw(); document.getElementById('ixHealthC').focus(); },
    close() { el.hidden = true; if (back && back.focus) back.focus(); },
    get isOpen() { return !el.hidden; },
    draw() {
      if (el.hidden) return; drawnAt = Math.floor(shipNow()); list.textContent = '';
      const rows = shipHealthRows(), [ship, ...sys] = rows;
      bar(ship, true); for (const r of sys) bar(r);
      const faults = sys.filter(r => r.worst && r.state !== 'fine');
      note('Faults', true);
      if (faults.length) for (const r of faults) note(r.name + ': ' + (IX_STATE[r.state] || r.state).toLowerCase() + '. Worst is the ' + r.worst + '.');
      else note('Nothing out of order. Everything is running as it should.');
      if (typeof jobsBoard === 'function') {
        const b = jobsBoard(), open = b.filter(j => !j.claimedBy).length, mine = typeof myJob === 'function' && myJob();
        note('Jobs', true);
        note(b.length ? b.length + (b.length === 1 ? ' job' : ' jobs') + ' on the board: ' + open + ' open, ' + (b.length - open) + ' being done.' + (mine ? ' One of them is yours.' : '') + ' The job board is in the Works bay, Deck 5.' : 'No jobs on the board.');
      }
    },
    tick() { if (!el.hidden && Math.floor(shipNow()) !== drawnAt) api.draw(); },   // kept live while open (ixFrame)
  };
  document.getElementById('ixHealthC').onclick = api.close;
  addEventListener('keydown', e => { if (e.key === 'Escape' && !el.hidden) api.close(); });
  return api;
})();

// ---- the job board: the open jobs, most urgent first, with Take it (claimJob: the same rule as the device's Jobs) ----
const ixBoard = (() => {
  const el = document.getElementById('ixBoard'), list = document.getElementById('ixBoardL'), sub = document.getElementById('ixBoardX');
  let back = null;
  const canTake = (j, mine) => !mine && !j.claimedBy && (typeof jobTier !== 'function' || jobTier(j) <= playerTier())
    && !(j.machine && typeof ENGINE_KINDS !== 'undefined' && ENGINE_KINDS.has((machineById(j.machine) || {}).kind));
  function row(title, line, pri, btn) {
    const r = document.createElement('div'), d = document.createElement('div'), h = document.createElement('b'), s = document.createElement('small');
    r.className = 'ixjob ' + (pri || ''); h.textContent = title; s.textContent = line; d.append(h, s); r.append(document.createElement('i'), d);
    if (btn) r.appendChild(btn); list.appendChild(r);
  }
  const PRI = ['routine', 'soon', 'urgent', 'urgent'];
  // what section 15 can walk you through today: machine jobs (and chores on a machine), and cart runs (cartTap)
  const doable = j => !!(j && (j.machine || j.kind === 'restock' || j.kind === 'chore' && typeof jobStepDone === 'function'));
  const button = (txt, fn) => { const x = document.createElement('button'); x.type = 'button'; x.textContent = txt; x.onclick = fn; return x; };
  const api = {
    open() { back = document.activeElement; el.hidden = false; api.draw(); document.getElementById('ixBoardC').focus(); },
    close() { el.hidden = true; if (back && back.focus) back.focus(); },
    get isOpen() { return !el.hidden; },
    draw() {
      if (el.hidden) return;
      list.textContent = '';
      const jobs = jobsBoard(), mine = myJob(), open = jobs.filter(j => !j.claimedBy);
      // yours to take: section 17's openJobs('you') when it's there (its titles and wording), else the device's rule
      const yours = typeof openJobs === 'function' ? openJobs('you') : open.filter(j => canTake(j, null)).map(j => { const [title, where, state] = jobCard(j); return { id: j.id, title, where, state, urgency: j.urgency }; });
      const ids = new Set(yours.map(o => o.id));
      const crew = jobs.filter(j => j.claimedBy && j.claimedBy !== 'you');   // the crew's, as the board on the wall shows them (0.37.6)
      sub.textContent = mine ? 'You have a job. Finish it or drop it to take another.' : yours.length ? 'Pick a job and take it. Tier ' + playerTier() + ' work is yours to take.'
        : 'Nothing open for you just now. New jobs come in through the day shift, and the crew take the urgent ones first: check back in an hour or two.';
      if (mine) {                                        // yours: Turn it in once the work's done (section 17's turnInJob), else Drop it
        const [title, where, state, pri] = jobCard(mine), done = mine.workDone && typeof turnInJob === 'function';
        row(mine.title || title, where + ' · ' + (done ? 'done: turn it in' : state), pri, done ? button('Turn it in', () => api.turnIn(mine.id))
          : button('Drop it', () => { dropJob(mine.id); api.draw(); device.refresh(); toast('Job board', 'You put the job back on the board.'); }));
      }
      for (const o of yours) {
        const raw = SHIP.jobs.find(j => j.id === o.id), ok = !mine && doable(raw);
        row(o.title, o.where + ' · ' + o.state + (doable(raw) ? '' : ' · not yet: coming soon'), PRI[o.urgency], ok ? button('Take it', () => api.take(o.id)) : null);
      }
      for (const j of open.filter(j => !ids.has(j.id))) {   // on the board, but not yours to take: say why
        const [title, where, state, pri] = jobCard(j), why = jobTier(j) > playerTier() ? 'tier ' + jobTier(j) : j.status === 'waiting' ? '' : 'crew only';
        row(j.title || title, where + ' · ' + state + (why ? ' · ' + why : ''), pri, null);
      }
      for (const j of crew) { const [title, where, state, pri] = jobCard(j); row(j.title || title, where + ' · ' + state, pri + ' taken', null); }
    },
    take(id) {
      if (!claimJob(id)) { toast('Job board', 'Someone got there first.'); api.draw(); return false; }
      const j = myJob(), [title, where] = jobCard(j);
      SHIP.player.track = j.id; clearGoal();             // a job taken is tracked (the device's Track switch: null = off), over any older arrow (playtest 1)
      api.close(); device.refresh(); ixGoalAt = -1;
      toast('Job taken', (j.title || title) + ', ' + where + '. Follow the marker' + (j.parts && j.parts.length ? ': parts first, from main storage on Deck 5.' : '.'));
      ixTip('taken', 'Track it on your device; the marker shows the way.');
      return true;
    },
    turnIn(id) {
      const g0 = typeof turnInSnap === 'function' ? turnInSnap() : null;   // 0.72.3: before, for the gains' fallback
      const j = myJob(); if (!j || j.id !== id || !turnInJob(id)) { toast('Job board', 'Nothing to turn in.'); api.draw(); return false; }
      // pay: section 15 pays machine jobs and cart runs when it finishes them; chores are paid here
      const pay = j.kind === 'chore' && !j.machine && typeof JOB_PAY !== 'undefined' ? JOB_PAY : 0;
      if (pay) SHIP.player.credits = (SHIP.player.credits || 0) + pay;
      api.draw(); device.refresh(); ixGoalAt = -1;
      toast('Job complete', (j.title || jobCard(j)[0]) + ': signed off on the board.' + (pay ? ' +' + pay + ' credits.' : '') + ' That\'s one more on your record.');
      if (typeof turnInShow === 'function') turnInShow(j, g0);   // what it did for your name and the ship (0.72.3)
      return true;
    },
  };
  document.getElementById('ixBoardC').onclick = api.close;
  addEventListener('keydown', e => { if (e.key === 'Escape' && !el.hidden) api.close(); });
  return api;
})();

// ---- the goal pointer: setGoal / clearGoal for any section; with no goal set, your job's next step ----
let IX_GOAL = null, ixJobGoal = null, ixGoalAt = -1;
// SHIP.player.track (Pillar 3, the device's Jobs app): null = tracking switched off (no job arrow); a job id or
// undefined = on. Taking a job at the board turns it on. Saved here (15b's field), read back defensively.
{ const t = SAVED && SAVED.player && SAVED.player.track; SHIP.player.track = t === null ? null : typeof t === 'string' || typeof t === 'number' ? t : undefined; }
SAVE_EXTRA.push(s => { const p = s.player || (s.player = {}); if (SHIP.player.track !== undefined) p.track = SHIP.player.track; });
function setGoal(g) { IX_GOAL = g && g.deck ? { ...g } : null; }
function clearGoal() { IX_GOAL = null; }
// the goal the arrow is showing, the same rule as ixFrame (0.28.58: the lift panel marks its deck); null with none
function goalNow() { return IX_GOAL || (SHIP.player.track === null ? null : ixJobGoal); }
// the shelf a part's on (section 17's shelfOf, 0.33.41): the arrow points at it and the label names it ("Fetch a relay:
// the Lights shelf"); without section 17's shelves, main storage as before
const ixShelf = need => { const id = typeof shelfOf === 'function' && need.length ? shelfOf(need[0]) : null; return id ? { place: id, say: ': the ' + shelfName(id) + ' shelf' } : { place: null, say: ' from main storage' }; };
// your job's next step: parts from main storage, a part from the machine shop, or the machine's panel
function ixJobStep() {
  if (typeof myJob !== 'function') return null;
  const j = myJob(); if (!j) return null;
  if (j.workDone) return { deck: 5, item: /job board/i, room: 'w', label: 'Turn it in at the job board' };   // Pillar 3: back to the board
  if (j.kind === 'restock') {                            // a cart run (section 15's cartTap): the dock, the hold, where it's going, the dock
    const c = SHIP.player.cart && SHIP.player.cart.job === j.id ? SHIP.player.cart : null, step = !c ? 'cart' : c.stage === 'empty' ? 'load' : c.stage === 'full' ? 'unload' : 'return';
    const st = typeof jobStops === 'function' ? jobStops(j).find(x => x.step === step) : null, meals = j.cargo === 'meals';
    const lab = { cart: 'Take a hover cart from the Cart bay', load: 'Load the cart in the cargo hold', unload: 'Unload at ' + (meals ? 'the cold store' : 'main storage'), return: 'Dock the cart in the Cart bay' }[step];
    return st ? { deck: st.deck, place: st.places[0] || null, room: !st.places.length && step === 'load' ? /cargo/i : null, label: lab } : { deck: 5, room: /cargo/i, label: lab };
  }
  if (crateDown(j)) { const c = SHIP.player.crate; return { deck: c.deck, xz: { x: c.x, z: c.z }, label: 'Pick up the crate you set down' }; }   // Put down (0.28.60)
  if (!j.machine) {                                      // a chore (section 17): parts first if it needs any, then its stops
    const P = SHIP.player, need = jobNeeds(j, { fitted: [] }, P.carry), nx = typeof jobStops === 'function' ? ixNextStop(j) : null;
    if (nx && nx.s.step === 'fetch' && need.length) return { deck: 5, room: 'r', place: ixShelf(need).place, label: 'Fetch ' + partList(need) + ixShelf(need).say };
    const st = nx && nx.s.step === 'fetch' ? jobStops(j)[nx.k + 1] : nx && nx.s;
    const rm = j.kind === 'rounds' && nx && nx.s === st && typeof machineById === 'function' ? machineById((j.route || [])[nx.k]) : null;   // a round: the machine by name (0.73.0)
    if (st && rm) return { deck: st.deck, place: st.places[0] || null, label: 'Look at ' + (typeof machineLabel === 'function' ? machineLabel(rm).split(',')[0] : machineName(rm)) };
    return st ? { deck: st.deck, place: st.places[0] || null, label: st.step === 'pickup' ? 'Pick up ' + (j.bring || 'the delivery') : st.step === 'inspect' ? j.title + ': the next stop' : j.title } : null;
  }
  if (typeof traceHidden === 'function' && traceHidden(j)) return typeof traceGoal === 'function' ? traceGoal(j) : null;   // a traced fault not yet found: the line, never the machine (24i)
  const m = machineById(j.machine); if (!m) return null;
  const P = SHIP.player, w = P.work && P.work.job === j.id ? P.work : { fitted: [], make: null };
  const need = jobNeeds(j, w, P.carry), name = machineName(m);
  if (need.length && P.carry.length < CARRY_MAX) {
    if (w.make && w.make.part) return { deck: 5, room: 'f', label: 'Make ' + partList([w.make.part]) + ' in the machine shop' };
    if (need.some(p => SHIP.stores[p] > 0)) { const on = need.filter(p => SHIP.stores[p] > 0), sh = ixShelf(on); return { deck: 5, room: 'r', place: sh.place, label: 'Fetch ' + partList(on) + sh.say }; }
    if (need.some(p => !(typeof NO_MAKE !== 'undefined' && NO_MAKE.has(p)))) return { deck: 5, room: 'f', label: 'Make ' + partList([need.find(p => !NO_MAKE.has(p))]) + ' in the machine shop' };
  }
  const pid = typeof panelPlace === 'function' ? panelPlace(m.id) : null;
  return { deck: m.deck, place: pid, at: m.at, room: m.room, label: (need.length ? 'Look over the ' : 'Repair the ') + name };
}
// where a goal is on this deck, in the world: a place, a tile, or the middle of a room (by key or name)
function ixGoalWorld(g) {
  if (g.crew && typeof DECK_CREW !== 'undefined') { const a = DECK_CREW.find(c => c.p && c.p.id === g.crew); if (a) return { x: a.x, z: a.z }; }   // someone on the deck (section 18's tradition leader, 0.70.0)
  if (g.xz) return g.xz;                                  // a spot on the floor (the set-down crate, 0.28.60)
  if (g.item) { const it = ITEMS.find(i => g.item instanceof RegExp ? g.item.test(i.t) : i.t === g.item); if (it) { it.hit.getWorldPosition(ixP); return { x: ixP.x, z: ixP.z }; } }
  if (g.place && PLACE_OF.has(g.place)) { const s = placeSpot(g.place); if (s) return { x: s.x, z: s.z }; }
  if (g.at) { const p = cellPos(...g.at); return { x: p.x, z: p.z }; }
  if (g.room) {
    const key = typeof g.room === 'string' && ROOMS[g.room] ? g.room : Object.keys(ROOMS).find(k => g.room instanceof RegExp ? g.room.test(ROOMS[k].name || '') : ROOMS[k].name === g.room);
    if (!key) return null;
    let sx = 0, sz = 0, n = 0, tiles = [];
    for (let j = 0; j < D; j++) for (let i = 0; i < W; i++) if (MAP[j][i] === key) { sx += i; sz += j; n++; tiles.push([i, j]); }
    if (!n) return null;
    const c = tiles.sort((a, b) => Math.hypot(a[0] - sx / n, a[1] - sz / n) - Math.hypot(b[0] - sx / n, b[1] - sz / n))[0], p = cellPos(...c);
    return { x: p.x, z: p.z };
  }
  return null;
}
// the first tips that depend on where you are (once a second at most): near the job board; at your job's machine
let ixTipAt = 0, ixStopLast = null;
function ixTips() {
  if (typeof tipShow !== 'function' || typeof deckDef === 'undefined' || !deckDef) return;
  const now = performance.now(); if (now - ixTipAt < 1000) return; ixTipAt = now;
  const p = player.obj.position, j = typeof myJob === 'function' ? myJob() : null;
  if (deckDef.num === 5) { const b = ITEMS.find(i => /job board/i.test(i.t)); if (b) { b.hit.getWorldPosition(ixP); if (Math.hypot(ixP.x - p.x, ixP.z - p.z) < 3.5) ixTip('board', 'Take jobs here, and turn them in here when they\'re done.'); } }
  if (j && j.machine && !j.workDone && typeof machineById === 'function') {
    const m = machineById(j.machine), pid = m && m.deck === deckDef.num && typeof panelPlace === 'function' ? panelPlace(m.id) : null, s = pid && PLACE_OF.has(pid) ? placeSpot(pid) : null;
    if (s && Math.hypot(s.x - p.x, s.z - p.z) < 2.5) ixTip('machine', 'Tap the machine to inspect. You may need parts from storage or the machine shop.');
  }
  if (j && j.workDone) ixTip('turnin', 'Head back to the board to turn it in.');
  roundGuide();
}
// the first round's walk-through (0.73.0, playtest 2 item 1, with E1's 24a): after Torres explains rounds, the round is a
// job on the board, and the goal arrow and green tips take you through it. E1's roundTrainStep() (once a second, no side
// effects) -> null or { step: 'take' | 'go' | 'look' | 'mark' | 'next' | 'done', job, machine, deck, place }. 'take': the
// arrow to the job board (our own goal, RG_GOAL; never over another section's arrow); once it's yours the job's own arrow
// (ixJobStep) walks each stop, naming the machine. Each new step shows its tip (the head writer's tip.round.<step>,
// {machine} filled; stand-ins until baked), replacing a round tip still showing, once a save (tipsSeen 'rg:<step>:<n>',
// n counting the machines). Nothing else saved; without roundTrainStep, nothing.
const RG_TIPS = { take: 'Your first round is on the job board. Take it, and follow the arrow.', go: 'Walk to {machine}. Follow the arrow.',
  look: 'Look at {machine}. Listen to it. Then mark what you see.', mark: 'Mark it: fine, worn, or something\'s off. Trust your eyes.',
  next: 'Next one. Follow the arrow.', done: 'Round done. Turn it in at the job board.' };
const RG_GOAL = 'Take your first round at the job board';
let RG_LAST = '', RG_N = 0;
function roundGuide() {
  let r = null; try { r = typeof roundTrainStep === 'function' ? roundTrainStep() : null; } catch (e) { r = null; }
  const ours = IX_GOAL && IX_GOAL.label === RG_GOAL, rgTips = () => { if (TIP_Q.length && /^rg:/.test(TIP_Q[0].id)) tipDone(); for (let i = TIP_Q.length - 1; i > 0; i--) if (/^rg:/.test(TIP_Q[i].id)) TIP_Q.splice(i, 1); };
  if (!r || r.step !== 'take') { if (ours) clearGoal(); }
  else if (!IX_GOAL || !RG_LAST) setGoal({ deck: 5, item: /job board/i, room: 'w', label: RG_GOAL });   // straight after Torres's talk it takes over (his meeting's arrow is done); later, never over another
  if (!r) { if (RG_LAST) rgTips(); RG_LAST = ''; return; }   // turned in: the last tip goes too
  const key = r.step + '|' + (r.machine || ''); if (key === RG_LAST) return;
  if (r.step === 'next' || r.step === 'look' && !/^(go|next)\|/.test(RG_LAST)) RG_N++;   // a new machine: next, or a look we walked up to without a go
  RG_LAST = key;
  const id = 'rg:' + r.step + ':' + (r.step === 'take' || r.step === 'done' ? 0 : RG_N);
  if (SHIP.device.tipsSeen[id]) return;
  rgTips();                                              // the last step's tip gives way
  const t = ((typeof careerText === 'function' && careerText('tip.round.' + r.step)) || RG_TIPS[r.step] || '').replace(/\{machine\}/g, r.machine || 'the machine');
  ixTip(id, t);
}
const ixV = new THREE.Vector3();
let ixLast = '';
function ixFrame() {
  requestAnimationFrame(ixFrame);
  if (ACT && IX_ACTS[ACT.kind] && ACT.phase !== 'walk' && ACT.body) ixSide(ACT);   // one of ours under way: its side gains
  // a chore's stop is done once its minutes are in: seen as it steps out, or (if it ended between our frames) once it's gone
  const L = ixStopLast; ixStopLast = ACT && ACT.kind === 'ixStop' ? ACT : null;
  for (const A of [ACT, L]) if (A && A.kind === 'ixStop' && !A.o.ixDone && (A.phase === 'out' || A !== ACT && A.done >= A.def.mins)) { A.o.ixDone = true; ixStopDone(A); }
  ixTips(); ixHealth.tick();
  const el = document.getElementById('ixGoal');
  if (typeof deckDef === 'undefined' || !deckDef || typeof player === 'undefined') { el.hidden = true; return; }
  const mj = typeof myJob === 'function' ? myJob() : null, m = Math.floor(shipNow()), key = m + '|' + (mj ? mj.id + (mj.workDone ? '+' : '') + (mj.stepsDone || []).length : '') + '|' + SHIP.player.carry.length + '|' + (SHIP.player.work ? SHIP.player.work.fitted.length + '|' + !!SHIP.player.work.make : '');
  if (ixGoalAt !== key) { ixGoalAt = key; try { ixJobGoal = ixJobStep(); } catch (e) { ixJobGoal = null; } }
  const g = IX_GOAL || (SHIP.player.track === null ? null : ixJobGoal);   // the job's step only while it's tracked
  if (!g) { if (!el.hidden) el.hidden = true; return; }
  if (typeof actProgress === 'function' && actProgress(ACT)) { if (!el.hidden) el.hidden = true; return; }   // section 15's progress bar is up over you: it says it all
  const here = deckDef.num === g.deck, w = here ? ixGoalWorld(g) : { x: LIFT_AT[0], z: LIFT_AT[1] };
  if (!w) { el.hidden = true; return; }
  const label = here ? g.label : 'Take the lift to ' + (g.deck === 7 ? 'the rec deck' : 'Deck ' + g.deck) + (g.label ? ': ' + g.label.charAt(0).toLowerCase() + g.label.slice(1) : '');
  ixV.set(w.x, 1.2, w.z).project(camera);
  // the arrow keeps inside a frame clear of the HUD at the top and the toast at the bottom
  const W2 = innerWidth / 2, H2 = innerHeight / 2, sx = (ixV.x + 1) * W2, sy = (1 - ixV.y) * H2, L0 = 30, R0 = innerWidth - 30, T0 = 130, B0 = innerHeight - 110;
  const dx = sx - W2, dy = sy - H2, k = Math.min(dx > 0 ? (R0 - W2) / dx : dx < 0 ? (L0 - W2) / dx : Infinity, dy > 0 ? (B0 - H2) / dy : dy < 0 ? (T0 - H2) / dy : Infinity);
  const on = sx >= L0 && sx <= R0 && sy >= T0 && sy <= B0, arr = el.children[0], pin = el.children[1], lab = el.children[2];
  const x = on ? sx : W2 + dx * k, y = on ? sy : H2 + dy * k;
  el.hidden = false; el.style.transform = 'translate(' + x.toFixed(1) + 'px,' + y.toFixed(1) + 'px)';
  arr.style.display = on ? 'none' : ''; pin.style.display = on ? '' : 'none';
  if (!on) arr.style.transform = 'rotate(' + Math.atan2(dy, dx).toFixed(3) + 'rad)';
  lab.style.top = on ? '6px' : y > H2 ? '-50px' : '24px';
  lab.style.transform = 'translateX(' + (x > innerWidth - 140 ? '-100%' : x < 140 ? '0' : '-50%') + ')';
  lab.style.left = x > innerWidth - 140 ? '18px' : x < 140 ? '-18px' : '0';
  if (label !== ixLast) { lab.textContent = ixLast = label; }
}
requestAnimationFrame(ixFrame);
// ---- Tracked (0.72.0, HUD U; the user's playtest note; also a device app since 0.72.4, first in its list): everything on or coming up (the rest of
// today and tomorrow morning from the Schedule's devDay: traditions, appointments, meals, your shift, ship items), your
// job, and a few fixed places (the job board, your bunk, the call booths). A tap tracks one with the goal arrow
// (setGoal, the goal carrying trk, its key, so the panel knows it's on; your job with SHIP.player.track, as the Jobs app
// does); a tap on the one being tracked stops it. A tradition asks tradGoal(x) first when there is one (the traditions
// seat: the arrow to the leader for tap-to-join), else the Schedule's devItemGoal (its room). Nothing here is saved. ----
const TRK_PLACES = [
  { key: 'place:board', title: 'The job board', sub: 'The Works bay, Deck 5', goal: () => ({ deck: 5, item: /job board/i, room: 'w', label: 'The job board' }) },
  { key: 'place:bed', title: 'Your bunk', sub: 'Your bed, Deck 4', goal: () => ({ deck: 4, place: playerBed(), label: 'Your bunk' }) },
  { key: 'place:calls', title: 'The call booths', sub: 'Call home, Deck 3', goal: () => ({ deck: 3, place: '3-callhome-1', room: 'B', label: 'The call booths' }) },
];
function trkGoalOf(x) {
  if (x.kind === 'tradition' && typeof tradGoal === 'function') { try { const g = tradGoal(x); if (g && g.deck) return g; } catch (e) { /* the room instead */ } }
  try { return devItemGoal(x); } catch (e) { return null; }
}
function trkItems() {
  const d = SHIP.time.day, m = SHIP.time.min, out = [], j = typeof myJob === 'function' ? myJob() : null;
  if (j) { let st = null; try { st = ixJobStep(); } catch (e) { /* no step */ }
    out.push({ sec: 'job', key: 'job:' + j.id, job: j.id, title: j.title || 'Your job', sub: st ? st.label : 'Your job', tag: 'Job' }); }
  for (const [day, upto] of [[d, 1440], [d + 1, 720]]) {   // the rest of today, and tomorrow until noon
    let list = []; try { list = devDay(day); } catch (e) { /* none */ }
    for (const x of list) {
      if (x.kind === 'off' || x.from >= upto || (day === d && x.to <= m)) continue;
      out.push({ sec: 'on', key: x.kind + ':' + day + ':' + x.from + ':' + x.title, title: x.title, sub: (day === d ? '' : 'Tomorrow · ') + x.where,
        tag: day === d && x.from <= m ? 'Now' : hhmm(x.from), goal: trkGoalOf(x) });
    }
  }
  for (const q of TRK_PLACES) out.push({ sec: 'place', key: q.key, title: q.title, sub: q.sub, tag: '', goal: q.goal() });
  return out;
}
const trkOn = it => { if (!it.job) return !!(IX_GOAL && IX_GOAL.trk === it.key); const j = typeof myJob === 'function' ? myJob() : null; return !IX_GOAL && SHIP.player.track !== null && !!j && j.id === it.job; };
function trkTap(key) {                                  // the app's tap: track it, or stop if it's the one tracked
  const it = trkItems().find(x => x.key === key); if (!it) return false;
  if (trkOn(it)) { if (it.job) SHIP.player.track = null; else clearGoal(); return false; }
  if (it.job) { SHIP.player.track = it.job; clearGoal(); }
  else if (it.goal) { SHIP.player.track = null; setGoal({ ...it.goal, trk: it.key }); }
  else return false;
  return true;
}
// the main-screen Tracked button and its panel (0.72.0; kept beside the app, the user's ~04:00 "for now keep it in the main UI")
const trkEl = document.getElementById('trkPanel'), trkList = document.getElementById('trkList'), trkBtn = document.getElementById('trkBtn');
const trkKey = () => Math.floor(shipNow()) + '|' + (IX_GOAL ? IX_GOAL.trk || IX_GOAL.label : '') + '|' + SHIP.player.track;
let trkSig = '';
function trkDraw() {
  const items = trkItems(); trkList.textContent = ''; trkSig = trkKey();
  for (const [sec, head] of [['job', 'Your job'], ['on', 'On and coming up'], ['place', 'Places']]) {
    const rows = items.filter(x => x.sec === sec); if (!rows.length) continue;
    const h = document.createElement('h3'), box = document.createElement('div'); h.textContent = head; box.className = 'decks'; trkList.append(h, box);
    for (const it of rows) {
      const on = trkOn(it), b = document.createElement('button'), sp = document.createElement('span'), t = document.createElement('b'), sm = document.createElement('small');
      b.type = 'button'; b.className = 'deckbtn' + (on ? ' goal' : ''); b.disabled = !on && !it.job && !it.goal; b.setAttribute('aria-pressed', String(on));
      if (it.tag) { const i = document.createElement('i'); i.textContent = it.tag; b.appendChild(i); }
      t.textContent = it.title; sm.textContent = it.sub + (b.disabled ? ' · no arrow for this one' : ''); sp.append(t, sm); b.appendChild(sp);
      if (on) { const e = document.createElement('em'); e.textContent = 'Tracking'; b.appendChild(e); }
      b.onclick = e => { e.stopPropagation(); if (trkTap(it.key)) trkClose(); else trkDraw(); };   // on its way: the arrow shows; a stop stays open
      box.appendChild(b);
    }
  }
}
function trkOpen() { if (!trkEl.hidden) return trkClose(); trkDraw(); trkEl.hidden = false; trkBtn.setAttribute('aria-expanded', 'true');
  try { (trkList.querySelector('button.goal') || trkList.querySelector('button:not(:disabled)') || document.getElementById('trkClose')).focus({ preventScroll: true }); } catch (e) { /* no focus */ } }
function trkClose() { trkEl.hidden = true; trkBtn.setAttribute('aria-expanded', 'false'); }
trkBtn.addEventListener('pointerdown', e => e.stopPropagation());
trkBtn.onclick = e => { e.stopPropagation(); trkOpen(); };
document.getElementById('trkClose').onclick = trkClose;
addEventListener('keydown', e => { if (e.key === 'Escape' && !trkEl.hidden) trkClose(); });
addEventListener('pointerdown', e => { if (!trkEl.hidden && !trkEl.contains(e.target) && !trkBtn.contains(e.target)) { e.stopPropagation(); e.preventDefault(); trkClose(); } }, true);   // a tap outside closes it, and goes no further
// where it sits: on phones (narrow or short, section 15's pausePlace's test) under the needs strip's left end, lined up
// with it, so the left column reads as one stack (card, Device and Pause, needs, Tracked, and section 15's activity bar
// last, under Tracked; item D, the user's, 0.64.2); it never moves when an activity starts or ends;
// elsewhere, or with no needs strip, in the Device button's row after Device (or Pause beside it), without its word
// when it would touch the round buttons
function trkPlace() {
  const d = document.getElementById('devBtn'), pb = document.getElementById('pauseBtn'), ns = document.getElementById('needStrip'); if (!d) return;
  const dr = d.getBoundingClientRect();
  trkBtn.classList.remove('compact'); trkBtn.style.height = Math.round(dr.height) + 'px';
  if (matchMedia('(max-width:720px),(max-height:500px)').matches && ns && !ns.hidden && ns.offsetWidth) {
    const r = ns.getBoundingClientRect(); trkBtn.style.left = Math.round(r.left) + 'px'; trkBtn.style.top = Math.round(r.bottom + 8) + 'px'; return;
  }
  const pr = pb && pb.style.left ? pb.getBoundingClientRect() : null, anchor = pr && Math.abs(pr.top - dr.top) < 4 ? pr : dr;
  const put = () => { trkBtn.style.left = Math.round(anchor.right + 8) + 'px'; trkBtn.style.top = Math.round(dr.top) + 'px'; };
  const hits = () => { const q = trkBtn.getBoundingClientRect(); return q.right > innerWidth - 8 || [...document.querySelectorAll('.controls button')].some(o => { if (o === pb || !o.offsetWidth) return false; const r = o.getBoundingClientRect(); return r.left < q.right + 4 && q.left < r.right && r.top < q.bottom && q.top < r.bottom; }); };
  put(); if (hits()) { trkBtn.classList.add('compact'); put(); }
}
addEventListener('resize', trkPlace); setTimeout(trkPlace, 0);
// the device app (0.72.4, the user's: "move it into the personal device as its own app, first in the list"); its glyph
// is the skin's 'track'
deviceApp({ id: 'tracked', title: 'Tracked', icon: 'track', order: 1,
  act(verb, key) { if (verb === 'track' && trkTap(key)) deviceClose(); },   // on its way: the device closes so the arrow shows
  view: () => {
    const items = trkItems(), B = [{ kind: 'text', text: 'Tap one to follow the arrow there. Tap it again to stop.' }];
    for (const [sec, head] of [['job', 'Your job'], ['on', 'On and coming up'], ['place', 'Places']]) {
      const rows = items.filter(x => x.sec === sec); if (!rows.length) continue;
      B.push({ kind: 'text', text: head, mark: 'head' });
      B.push({ kind: 'list', rows: rows.map(it => { const on = trkOn(it), can = on || it.job || it.goal;
        return { text: it.title, sub: (sec === 'on' && it.tag ? it.tag + ' · ' : '') + it.sub + (on ? ' · Tracking' : can ? '' : ' · no arrow for this one'), mark: on ? 'hot' : null,
          action: can ? { app: 'tracked', do: 'track', arg: it.key } : null }; }) });
    }
    return { title: 'Tracked', blocks: B };
  } });
// ---- the turn-in's gains (0.72.3, HUD U; Pillar 5 Step 3, the user's: "the job turn-in shows rep going up AND the points
// added to each ship meter the job helped"). The board's turnIn calls turnInShow(job, before) after its toast, which gets
// a row of chips: reputation first (gold), then each ship meter ("+4 Power"). What it shows comes from the job:
// j.gains = { rep: [{ dept, name?, add }], meters: [{ sys, name?, add, now? }] }, filled by whoever applies a gain (C2 the
// rep, as words: C2's careerJobIn, 0.44.22); the meters come from S2's j.meters = [{ key, name, gain }] (0.33.57, set when the work is done) when j.gains has none. Missing either list, a before/after look round turnInJob
// (turnInSnap: SHIP.rep's departments, shipHealthRows' systems) fills it in. Reputation is words only, never a number
// (the user's 0.61.15 rule). Words: the head writer's works.turnin.rep, works.turnin.meter ({n} {system}), meter.<sys>. Nothing saved; the job keeps j.gains.
function turnInSnap() {
  const out = { rep: {}, sys: {} };
  try { const R = typeof repInit === 'function' ? repInit() : null; if (R) out.rep = { ...R.dept }; } catch (e) { /* none */ }
  try { for (const r of shipHealthRows()) if (r.key !== 'ship') out.sys[r.key] = r.value; } catch (e) { /* none */ }
  return out;
}
const tgDept = d => (typeof DEPT_NAME !== 'undefined' && DEPT_NAME[d]) || String(d || 'works').charAt(0).toUpperCase() + String(d || 'works').slice(1);
function turnInGains(j, a) {
  const g = j && j.gains, T = (k, fb, ctx) => { let t = null; try { t = careerText(k); } catch (e) { t = null; } t = t || fb; for (const c in ctx || {}) t = t.split('{' + c + '}').join(ctx[c]); return t; };
  let reps = g && Array.isArray(g.rep) ? g.rep : null, mets = g && Array.isArray(g.meters) ? g.meters : null;
  if (!mets && j && Array.isArray(j.meters)) mets = j.meters.map(m => m && ({ sys: m.key, fb: m.name, add: m.gain }));   // S2's (0.33.57): set when the work is done
  if (a && (!reps || !mets)) {
    const b = turnInSnap();
    if (!reps) reps = Object.keys(b.rep).filter(d => isFinite(a.rep[d]) && b.rep[d] - a.rep[d] >= .5).map(d => ({ dept: d, add: Math.round(b.rep[d] - a.rep[d]) }));
    if (!mets) mets = Object.keys(b.sys).filter(k => isFinite(a.sys[k]) && b.sys[k] - a.sys[k] >= 1).map(k => ({ sys: k, add: b.sys[k] - a.sys[k] }));
  }
  const seen = new Set(), dup = k => seen.has(k) || !seen.add(k);   // one chip each: two sections may record the same gain (C2 and a test, BM6's find)
  if (mets) { const best = {}; for (const m of mets) if (m && (!best[m.sys] || m.add > best[m.sys].add)) best[m.sys] = m; mets = mets.filter(m => m && best[m.sys] === m); }
  const out = [];
  for (const r of reps || []) { if (r && dup('rep:' + (r.dept || 'works'))) continue; if (!r || !(r.add > 0) && r.add !== undefined) continue; const dn = r.name || tgDept(r.dept);   // words only, never a number (the user's 0.61.15 rule)
    out.push({ rep: true, text: (r.dept || 'works') === 'works' ? T('works.turnin.rep', 'Works reputation up') : dn + ' reputation up' }); }
  for (const m of mets || []) { if (!m || !(m.add >= .5)) continue; const nm = T('meter.' + m.sys, m.name || m.fb || (typeof SYSTEM_NAME !== 'undefined' && SYSTEM_NAME[m.sys]) || String(m.sys));   // the head writer's short name first
    out.push({ rep: false, text: T('works.turnin.meter', '+{n} {system}', { n: Math.round(m.add), system: nm }) }); }
  return out;
}
function turnInShow(j, a) {
  let list = []; try { list = turnInGains(j, a); } catch (e) { list = []; }
  if (!list.length) return list;
  const x = document.getElementById('tx'), row = document.createElement('span'); row.className = 'tgain';
  for (const c of list) { const b = document.createElement('b'); b.textContent = c.text; if (c.rep) b.className = 'rep'; row.appendChild(b); }
  x.appendChild(row); return list;
}

