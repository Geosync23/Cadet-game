// =====================================================================
// 15r. THE REC DECK'S ACTIVITIES (the rec deck architect, 0.80.6-0.80.7; plans/recdeck-plan.html section 9 "For you: tap and do")
// One tap each, for the player only (phase 1): the pool (swim lengths), the kayak dock and the rivers (paddle the loop),
// the climbing wall (climb, ring the bell, be lowered), the float room (float), an auditorium seat (sit), the stands
// (watch). Each is a section 15 activity, so walking away stops it and the needs work as everywhere; the moving ones use
// section 8c's mover (RA1's actStart(kind, place, { move }): REC_MOVES, recMoveStep), its rec kit (playerKit) and its
// locker change (PLAYER_ACTS.recChange). The pool and the kayaks need rec kit: in uniform you go to a locker first, and
// when you're done you come back for a quick shower (a towel over your shoulder after) and change back; the first time a
// tip says so. Leaving the deck puts your uniform back on. Outside 06:00-midnight: "The rec deck's closed till six."
// Lightdisc's court, scoreboard and its Ask someone to play panel say it's coming soon. Nothing here calls R().
// =====================================================================
Object.assign(PLAYER_ACTS, {
  recSwim:   { need: 'leisure', gain: 25, mins: 15, cost: { energy: 8 }, also: { hygiene: 10, fitness: 15 }, pose: 'tread', title: 'Swimming', done: 'Your lengths done. You climb out tingling.' },
  recKayak:  { need: 'leisure', gain: 25, mins: 15, cost: { energy: 6 }, also: { fitness: 15 }, pose: 'kayak', title: 'Kayaking', done: 'You bring the kayak in to the dock, soaked and grinning.' },
  recClimb:  { need: 'leisure', gain: 20, mins: 8, cost: { energy: 6 }, also: { fitness: 8 }, pose: 'climb', title: 'Climbing', done: 'Back on the floor. Your arms are jelly. You rang the bell, though.' },
  recFloat:  { need: 'leisure', gain: 25, mins: 10, also: { fitness: 10 }, pose: 'float',   // 0.82.5: fitness as the gym (1 a minute)
    title: 'Float room', done: 'Back to full gravity. Your legs feel very heavy.' },
  recSeat:   { need: 'leisure', gain: 8, mins: 15, pose: 'sit', title: 'Auditorium', done: 'You get up and stretch.' },
  recWatch:  { need: 'leisure', gain: 8, mins: 15, pose: 'sit', title: 'Stands', done: 'You get up and stretch.' },
  recBean:   { need: 'leisure', gain: 8, mins: 15, pose: 'sit', title: 'Beanbag', done: 'You haul yourself out of the beanbag. It takes two goes.' },
  recShower: { need: 'hygiene', gain: 20, mins: 3, pose: 'stand', title: 'Shower' },
  recWait:   { need: 'leisure', gain: 4, mins: 40, pose: 'sit', title: 'Waiting your turn', done: 'You give up waiting.' },   // RA, 0.83.0: the queue (recQueue)
});
const REC = { chain: null, last: null, q: null, wso: null, cup: null };
const recKitOn = () => PLAYER_SPEC.kit === 'rec';
const recOpen = () => SHIP.time.min >= DECKS[7].open[0] * 60;   // 06:00 to midnight
// where things are: spots in world units (from deck tile coordinates), moves in deck coordinates (section 8c's)
const recSpot = (walk, x, z, face, pose) => ({ id: null, walk, x: x - OX, z: z - OZ, y: 0, face, pose });
const recLocker = () => recSpot([19, 1], 19.35, 1.25, Math.PI, 'browse');
const recShowerAt = () => recSpot([17, 2], 17.65, 3.35, Math.PI, 'stand');
const REC_LANES = [1.35, 2.25, 3.15, 4.05];             // the pool's four lanes (plan v4: ropes at 1.8, 2.7 and 3.6)
const REC_LOOP = [[11.4, 4.85], [4.8, 4.85], [4.8, 1.3], [13.8, 1.3, 1], [13.8, 4.85, 1]];   // the kayak loop: west along the slow channel, east down the white water
function recTap(it, at, point) {
  if (typeof deckDef === 'undefined' || !deckDef || deckDef.num !== 7) return false;
  const t = it.t;
  if ((t === 'Lightdisc court' || t === 'Ask someone to play') && recShut().court) { toast('Lightdisc', worksText('rec.shut.net', 'The net\'s down. No Lightdisc till Works fix the emitters.')); return true; }   // 0.84.4 (rec engineer B); 0.84.8 W3's key
  if ((t === 'Lightdisc court' || t === 'Ask someone to play') && (recCupTap() || recWsoTap())) return true;   // Winner Stays On: skip the line (0.83.1); Cup day: your match (0.83.2)
  if (t === 'Lightdisc court' || t === 'Ask someone to play') { if (!recQueue('disc', t, null)) discAsk(recCourtWaiting()); return true; }   // section 23b (0.82.0); two crew already on the court: wait your turn (RA, 0.83.0)
  if (t === 'Scoreboard') { toast(t, it.x); return true; }
  const kind = t === 'Pool' ? 'swim' : /^(Kayak dock|River|White water|Kayak rack|Wave gate)$/.test(t) ? 'kayak' : t === 'Climbing wall' ? 'climb'
    : t === 'Float room' ? 'float' : t === 'Seats' ? 'seat' : t === 'Stands' ? 'watch' : t === 'Beanbag' ? 'bean' : t === 'Lockers' && recKitOn() ? 'unchange' : null;
  if (!kind) return false;
  if (!recOpen() && kind !== 'unchange') { toast(t, 'The rec deck\'s closed till six.'); return true; }
  recGo(kind, point, t, it.x); return true;
}
PLAYER_TAPS.push(recTap);
// 0.82.5 (the user's): walking into the float room starts floating, no tap; walking out (or a tap elsewhere) ends it, as any activity
function recRoomIn(r) {
  if (r !== 'F' || !deckDef || deckDef.num !== 7 || ACT || !recOpen()) return;
  recGo('float', null, 'Float room', 'A fifth of a g. The padding is soft underfoot.');
}
function recGo(kind, point, title, flavour) {
  REC.chain = null;
  if (kind === 'seat' || kind === 'watch' || kind === 'bean') {   // the nearest free seat to your tap, in that room (a beanbag: the concourse's)
    const room = kind === 'seat' ? 'A' : kind === 'bean' ? '=' : 'T', type = kind === 'bean' ? 'lounge-seat' : 'rec:seat', pl = [...PLACE_OF.values()].filter(p => p.type === type && p.room === room && !p.ring && !heldBy(p.id))
      .map(p => [p, placeSpot(p.id)]).filter(([, s]) => s).sort((a, b) => Math.hypot(a[1].x - point.x, a[1].z - point.z) - Math.hypot(b[1].x - point.x, b[1].z - point.z))[0];
    if (!pl) { toast(title, 'Every seat\'s taken.'); return; }
    if (kind === 'bean') { actStart('recBean', pl[0].id, { pose: 'sit', title, flavour, after: 'You flop into the beanbag. It swallows you whole.' }); return; }
    actStart(kind === 'seat' ? 'recSeat' : 'recWatch', pl[0].id, { pose: 'sit', title, flavour, after: kind === 'seat' ? 'You sink into a violet seat and look at the stars behind the stage.' : 'You take a seat on the bench and watch the court.' });
    return;
  }
  if (kind === 'unchange') { actStart('recChange', null, { title: 'Changing rooms', spot: recLocker(), kit: null, after: 'You change back into your uniform.' }); return; }
  if ((kind === 'swim' || kind === 'kayak') && !recKitOn()) {   // the wet way: change first
    if (typeof ixTip === 'function') ixTip('recChange', 'Swimming and kayaking: change first. You\'ll stop at the changing rooms by the lift.');
    REC.chain = { then: kind, title, flavour, point: point ? [point.x + OX, point.z + OZ] : null };
    actStart('recChange', null, { title: 'Changing rooms', spot: recLocker(), kit: 'rec', after: 'You change into rec kit at a locker: teal, with a coral stripe.' });
    return;
  }
  recStart(kind, title, flavour, point ? [point.x + OX, point.z + OZ] : null);
}
// the crew are here too (RA, 0.83.0): a lane or a belay the crew are using (or walking to) isn't yours. When every one is
// taken you wait your turn at its waiting spot (the loungers, the pebble beach, the stands' gate bench), and when one comes
// free: "You're up." The kayaks (3 crew and you) and the float room (6 and you) always have room
const REC_BELAYS = [['7-climb-1', 1], ['7-climb-2', 2]];   // the two auto-belays, over routes 1 and 2 (0-based: yellow and blue; rec engineer B2's)
const recLanesFree = () => REC_LANES.filter((z, i) => !heldBy('7-lane-' + (i + 1)));
const recBelaysFree = () => { const sh = typeof recShut === 'function' ? recShut() : null; return REC_BELAYS.filter(([id, r], b) => !heldBy(id) && !(sh && ((sh.belayOff || [])[b] || sh.route === r))).map(([, r]) => r); };   // not one tagged out or roped off
const recBelaysUsable = () => { const sh = REC_DECK && typeof recShut === 'function' ? recShut() : null; return REC_BELAYS.filter(([, r], b) => !(sh && ((sh.belayOff || [])[b] || sh.route === r))).length; };   // free or busy, not tagged out or roped off: none means no turn will come (R7's note; RE20, 0.64.1)
const recCourtFree = () => !heldBy('7-disc-1');           // your baseline: crew there means a game of theirs is on (0.83.2)
const REC_QUEUE = { swim: ['rec:poolq', 'Every lane\'s taken. You wait on a lounger for one to come free.'], climb: ['rec:climbq', 'Both belays are in use. You wait on the pebble beach for your turn.'],
  disc: ['rec:seat', 'Two are playing. You wait on the bench by the gate: you\'re next.'] };
const recFreeFor = kind => kind === 'swim' ? recLanesFree().length > 0 : kind === 'climb' ? recBelaysFree().length > 0 : kind === 'disc' ? recCourtFree() : true;
// Winner Stays On (0.83.1): tap the court or its gate while it's on and you play the one who's on next ("Go on, you're
// up"); win three in a row and your name goes on the foyer's board with the rest (REC.wso counts your run that day)
// the Lightdisc Cup (0.83.2): you enter at the gate on Cup day and play your matches live, a round at a time against
// each round's first winner on the bracket (cupBracket); lose one and you're out, win them all and the Cup's yours
function recCupTap() {
  if (!REC_DECK || typeof tradOn !== 'function' || !tradOn('rec-cup') || typeof cupBracket !== 'function') return false;
  const d = SHIP.time.day, c = cupBracket(d); if (!c || !c.rounds.length) return false;
  if (!REC.cup || REC.cup.day !== d) REC.cup = { day: d, round: 0, won: false, out: false, wins: SHIP.disc.won, played: SHIP.disc.played };
  const C = REC.cup;
  if (C.out || C.won) { toast('Lightdisc Cup', C.won ? 'The Cup\'s yours this time. Pell has already engraved it, badly.' : 'You\'re out of the Cup this time. Cheer from the stands.'); return true; }
  const m = c.rounds[Math.min(C.round, c.rounds.length - 1)][0], opp = schedPeople().find(q => q.id === m[2]); if (!opp) return false;
  toast('Lightdisc Cup', (C.round === c.rounds.length - 1 ? 'The final! ' : 'Round ' + (C.round + 1) + '. ') + 'You play ' + shortName(opp) + '.');
  discAsk(opp); return true;
}
function recWsoTap() {
  if (!REC_DECK || typeof tradOn !== 'function' || !tradOn('rec-wso') || typeof wsoCourt !== 'function') return false;
  const d = SHIP.time.day, c = wsoCourt(d), m = SHIP.time.min, g = c && c.games.find(x => x.from <= m && m < x.to) || c && c.games.find(x => x.from > m);
  const champ = g && schedPeople().find(q => q.id === g.a); if (!champ) return false;
  if (!REC.wso || REC.wso.day !== d) REC.wso = { day: d, run: 0, won: SHIP.disc.won, played: SHIP.disc.played };
  toast('Winner Stays On', 'Pell waves you through the gate. "Go on, you\'re up." You play ' + shortName(champ) + '.');
  discAsk(champ); return true;
}
// someone waiting on the stern baseline for a game (a crew pick-up with nobody yet): they play you (R6's fix, 0.83.2)
const recCourtWaiting = () => { const a = heldBy('7-disc-2'); return a && a.p && !heldBy('7-disc-1') ? schedPeople().find(q => q.id === a.p.id) || null : null; };
function recQueue(kind, title, p) {                      // true when you're now waiting (REC.q), false when there's room
  if (!REC_QUEUE[kind] || recFreeFor(kind)) return false;
  const [type, line] = REC_QUEUE[kind], gate = kind === 'disc';
  const pl = [...PLACE_OF.values()].filter(q => q.type === type && !heldBy(q.id) && (!gate || q.room === 'T' && q.at[1] === 11 && q.at[0] >= 12))[0];
  REC.q = { kind, title, p };
  actStart('recWait', pl ? pl.id : null, { title: 'Waiting your turn', pose: pl ? pl.pose : 'stand', after: line, ...(pl ? {} : { spot: recSpot(kind === 'swim' ? [26, 5] : kind === 'climb' ? [3, 4] : [14, 12], kind === 'swim' ? 26.5 : kind === 'climb' ? 3.5 : 14.5, kind === 'swim' ? 5.5 : kind === 'climb' ? 4.5 : 12.5, 0, 'stand') }) });
  return true;
}
function recStart(kind, title, flavour, p) {             // p: the tap in deck coordinates (or null)
  if (kind === 'float' && recShut().float) { toast('Float room', worksText('rec.shut.float', 'The float room\'s shut: the gravity plates are down. Works are on it.')); return; }   // 0.84.4 (rec engineer B); 0.84.8 W3's key
  if (kind === 'climb' && !recShut().belays) { toast('Climbing wall', worksText('rec.shut.belays', 'Both auto-belays are tagged out. Works are on it.')); return; }   // 0.84.4 (rec engineer B); 0.84.8 W3's key
  if (kind === 'climb' && REC_DECK && !recBelaysUsable()) { toast('Climbing wall', worksText('rec.shut.wall', 'One auto-belay\'s tagged out and the other one\'s route is taped off. No climbing till Works are done.')); return; }   // one tagged out, the other's route taped: no waiting for a turn that won't come (R7's note; RE20, 0.64.1)
  const water = { pool: .35, river: .36 };
  if (recQueue(kind, title, p)) return;
  if (kind === 'swim') {
    const free = recLanesFree(), lane = free.reduce((m, z) => p && Math.abs(z - p[1]) < Math.abs(m - p[1]) ? z : m, free.includes(REC_LANES[1]) ? REC_LANES[1] : free[0]);
    actStart('recSwim', null, { title, flavour, spot: recSpot([23, Math.min(4, Math.floor(lane))], 23.55, lane, Math.PI / 2, 'stand'),
      move: { kind: 'swim', path: [[24.5, lane], [30.5, lane]], y: water.pool, lengths: 4 }, after: 'You slip in at the shallow end and start your lengths.' });
  } else if (kind === 'kayak') {
    actStart('recKayak', null, { title, flavour, spot: recSpot([11, 6], 11.4, 5.75, Math.PI, 'stand'),
      move: { kind: 'kayak', path: REC_LOOP, y: water.river, laps: 2 }, follow: true, after: 'You take a kayak from the dock and push off into the slow channel.' });
  } else if (kind === 'climb') {
    const len = REC_WALL.z1 - REC_WALL.z0, r0 = Math.max(0, Math.min(REC_ROUTES - 1, Math.floor(((p ? p[1] : 4.3) - REC_WALL.z0) / len * REC_ROUTES)));
    const r = REC_DECK ? recBelaysFree().reduce((m, x) => Math.abs(x - r0) < Math.abs(m - r0) ? x : m, recBelaysFree()[0]) : r0;   // a free belay's route nearest your tap (0.83.0: two belays)
    const z = REC_WALL.z0 + len * (r + .5) / REC_ROUTES, sh = recShut();   // 0.84.12 (R7): not up a taped route, nor under a tagged-out belay (belay n is over route n)
    if (sh.route === r) { toast('Climbing wall', worksText('rec.shut.route', 'That route\'s taped off: a loose hold. Try another one.')); return; }
    if ((r === 1 || r === 2) && sh.belayOff[r - 1]) { toast('Climbing wall', worksText('rec.shut.belay', 'That route\'s auto-belay is tagged out. Try the other one.')); return; }
    actStart('recClimb', null, { title, flavour, spot: recSpot([2, Math.max(2, Math.min(6, Math.floor(z)))], 2.5, z, -Math.PI / 2, 'stand'),
      move: { kind: 'climb', at: [1.95, z], face: 'w', top: Math.max(.8, H - 2.25), onRing: () => toast('The bell', 'Ding! You ring the brass bell at the top of the wall. The whole river hall hears it.') },
      after: 'You clip into an auto-belay on the ' + ['red', 'yellow', 'blue', 'green'][r] + ' route and start up.' });
  } else if (kind === 'float') {
    actStart('recFloat', null, { title, flavour, spot: recSpot([18, 12], 20.5, 14.5, 0, 'stand'),
      move: { kind: 'float', at: [21, 14.8], r: 1.2, top: Math.min(2.2, H - 1.4), bounces: 4 }, follow: true, after: 'You pull on grip socks from the shelf and step into a fifth of a g.' });
  }
}
// after each one ends: the next step of the wet way (change, the activity, a shower, change back)
function recAfter(A) {
  const done = A.phase === 'out' && (A.o.move ? !!(A.mv && A.mv.done) : A.done >= A.def.mins);
  if (!done) { REC.chain = null; return; }
  if (A.kind === 'recChange' && A.o.kit === 'rec' && REC.chain) { const c = REC.chain; REC.chain = null; recStart(c.then, c.title, c.flavour, c.point); return; }
  if (A.kind === 'recSwim' || A.kind === 'recKayak') { actStart('recShower', null, { title: 'Changing rooms', spot: recShowerAt(), after: 'Back through the changing rooms: a quick shower first.' }); return; }
  if (A.kind === 'recShower' && recKitOn()) { if (typeof recTowel === 'function') recTowel(20); actStart('recChange', null, { title: 'Changing rooms', spot: recLocker(), kit: null, after: 'You change back into your uniform.' }); }
}
// each frame (its own requestAnimationFrame, like 15b's): the chain, the side gains, and your uniform back off the deck
function recFrame() {
  requestAnimationFrame(recFrame);
  if (typeof deckDef === 'undefined' || !deckDef || typeof ACT === 'undefined') return;
  if (recKitOn() && deckDef.num !== 7 && !ACT && typeof playerKit === 'function') playerKit(null);   // off the deck: back in uniform
  const A = ACT;
  const W = REC.wso; if (W && W.day === SHIP.time.day && SHIP.disc.played !== W.played && !DISC.g) {   // a Winner Stays On game of yours just ended
    W.played = SHIP.disc.played; if (SHIP.disc.won === W.won) W.run = 0;
    else { W.run++; if (W.run === 3 && typeof recBoardAdd === 'function') { recBoardAdd('wso', 'you', W.day); toast('Winner Stays On', 'Three in a row! Pell chalks your name on the board in the foyer.'); } }
    W.won = SHIP.disc.won;
  }
  const Cc = REC.cup; if (Cc && Cc.day === SHIP.time.day && SHIP.disc.played !== Cc.played && !DISC.g) {   // a Cup match of yours just ended
    Cc.played = SHIP.disc.played; const c = cupBracket(Cc.day);
    if (SHIP.disc.won === Cc.wins) { Cc.out = true; toast('Lightdisc Cup', 'Out in round ' + (Cc.round + 1) + '. The stands give you a cheer anyway.'); }
    else { Cc.wins = SHIP.disc.won; Cc.round++; if (c && Cc.round >= c.rounds.length) { Cc.won = true; toast('Lightdisc Cup', 'You win the Lightdisc Cup! Your name goes on the foyer\'s Cup board.'); } else toast('Lightdisc Cup', 'Through to round ' + (Cc.round + 1) + '. Tap the gate when you\'re ready.'); }
  }
  if (A && A.kind === 'recWait' && REC.q && recFreeFor(REC.q.kind)) {   // your turn (RA, 0.83.0)
    const q = REC.q; REC.q = null; toast(q.title, 'You\'re up.');
    if (q.kind === 'disc') { actEnd(true); discAsk(recCourtWaiting()); } else recStart(q.kind, q.title, null, q.p);
  } else if (A && A.kind === 'recWait' && REC.q && REC.q.kind === 'climb' && REC_DECK && !recBelaysUsable()) {   // waiting, and now no belay can free up: stop waiting (RE20, 0.64.1)
    REC.q = null; actEnd(true); toast('Climbing wall', recShut().belays ? worksText('rec.shut.wall', 'One auto-belay\'s tagged out and the other one\'s route is taped off. No climbing till Works are done.') : worksText('rec.shut.belays', 'Both auto-belays are tagged out. Works are on it.'));
  } else if (REC.q && (!A || A.kind !== 'recWait')) REC.q = null;   // gave up waiting, or went off to do something else
  if (A !== REC.last) { const was = REC.last; REC.last = A; if (was && was.kind.startsWith('rec') && !A) recAfter(was); }
  if (A && A.kind.startsWith('rec') && A.phase === 'do' && A.def.also) {   // the second gains (a swim washes you, all of them keep you fit), as the minutes go by
    const d = Math.max(0, Math.min(A.done, A.def.mins) - (A.alsoDone || 0)), n = SHIP.player.needs; A.alsoDone = (A.alsoDone || 0) + d;
    for (const k in A.def.also) if (k in n) n[k] = needClamp(n[k] + A.def.also[k] * d / A.def.mins);
  }
}
requestAnimationFrame(recFrame);
let trkAt = 0;
(function trkFrame() {                                   // the button's dot while an arrow's up; its place (the Device button and Pause move); the panel kept current while open
  requestAnimationFrame(trkFrame);
  const now = performance.now(); if (now - trkAt < 400) return; trkAt = now;
  const on = typeof goalNow === 'function' && !!goalNow(); if (trkBtn.classList.contains('on') !== on) trkBtn.classList.toggle('on', on);
  trkPlace();
  if (!trkEl.hidden && trkSig !== trkKey()) trkDraw();
})();

