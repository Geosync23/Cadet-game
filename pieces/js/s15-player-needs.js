// =====================================================================
// 15. PLAYER NEEDS & DEVICE
// Your needs (hunger, energy, hygiene, fitness, social, bathroom; 0-100,
// 100 = fully met) in SHIP.player.needs. They drain with ship time and come back by
// doing things: eat (the servery, a mess seat, the grab shelf), sleep (your
// bunk, section 13), shower, work out (treadmill, weights), call home (a
// booth), use a toilet (any public washroom, 0.28.19). Tap the thing to do it: you walk there, take the pose, time runs,
// the need rises; walk away to stop. Places crew hold are left alone.
// Needs give bonuses and penalties (needEffects, 0.28.9): over NEED_HIGH a
// bonus, under NEED_LOW a penalty (low fitness or energy: you walk slower).
// There is no fail state.
// The device's screens are section 19's apps (0.35.0); device.addSection(id,
// title, render) still works there as a shim.
// Sits after 14 like 13 and 14 do; it only touches the player, the deck and
// the HUD at run time (section 10 and on). Nothing here calls R().
// Mail (0.28.10): mailSend({ at, from, subject, body }) from any section puts a
// message in SHIP.mail, read on the device's Mail tab. Social also comes from
// chatting with crew (tap them) and eating with company; the store sells
// snacks and small comforts for credits (SHIP.player.credits).
// A tap on a machine asks section 17's machineUse (0.28.11); a restock job is
// a hover-cart run you push yourself; crawlway tiles (a deck's crawl list)
// slow you to a crouch. Tap a free seat to sit (0.28.12); you can squeeze
// past crew settled at their places when there's no other way round.
// Hooks elsewhere: the save (13: v 2, needs, New game), the item tap (11), the
// crew tap (10: playerChat), Walker.update's pose (10: holding, crouch),
// playerUpdate in the main loop (12), the device's HTML and CSS.
// =====================================================================
const NEED_KEYS = ['hunger', 'energy', 'hygiene', 'fitness', 'social', 'bathroom', 'leisure'];   // the plan's NEEDS (section 14 has it too, as NEEDS); bathroom: the user's, 0.28.19; leisure: 0.60.7's (0.28.61)
const NEED_LABEL = { hunger: 'Food', energy: 'Energy', hygiene: 'Hygiene', fitness: 'Fitness', social: 'Social', bathroom: 'Bathroom', leisure: 'Leisure' };
// drain per ship hour (so they hold whatever SHIP_RATE is): [awake, asleep]. A normal day (breakfast, dinner, a
// shower, a night's sleep) keeps food, hygiene and fitness above 40; the gym every two or three days keeps fitness
// up; a call home every two days keeps social up. Energy (0.28.9, the user's long days): 4.4 an hour takes a rested
// player from 100 to the tired line (25) in 17 ship hours at average fitness, about 18 when fit and 16 when not
// (needEffects' drain, below). Bathroom (0.28.19, the user's): 12 an hour awake, from a visit to the low line in
// about six hours, so it comes up three or four times a day (on waking, midday, dinner, bedtime); 3 asleep.
// Leisure (0.28.61, the 0.60.7 plan): 0.8 an hour awake, none asleep, so about 6 ship days from full to the low line;
// hobbies, traditions, Tiles, the bar, a full talk, calling home and a few places fill it (leisureAdd, below)
const NEED_DRAIN = { hunger: [4, 2], energy: [4.8, 0], hygiene: [2.5, 1], fitness: [.6, .3], social: [1, .25], bathroom: [6, 1.5], leisure: [.8, 0] };   // bathroom halved in 0.28.62 (the 0.60.7 plan: about two visits a day); energy 4.4 -> 4.8 in 0.73.0 (playtest 2, the lead's tuning: a normal 16-hour day ends near 20-25)
const SLEEP_GAIN = 12.5;                                 // energy per ship hour asleep: 8 hours fills it
const NEEDS_FRESH = { hunger: 60, energy: 100, hygiene: 60, fitness: 70, social: 70, bathroom: 60, leisure: 70 };   // a new game: just woken, before breakfast
const NEEDS_OLD = 80;                                    // a v 1 save had no needs: start them here
const SLOW_BELOW = 25, SLOW_SPEED = .8;                  // fitness or energy under this: walk at this speed (each one counts)
const needClamp = v => Math.max(0, Math.min(100, v));
// what your needs do (the user's rule, 0.28.9): at NEED_HIGH or over a need gives a bonus, under NEED_LOW a penalty,
// in between nothing; the effects multiply. walk: walking speed; task: how fast tasks go (repairs, making parts,
// activities: 1.15 = 15% faster); drain: how fast energy drains while awake; socialGain: social from chatting with
// crew and eating in company. Each comes with the device's one-line reason. The machines' walk is never in it.
const NEED_HIGH = 75, NEED_LOW = SLOW_BELOW;
const GO_SPEED = .7, GO_SAY = 'Bursting for the toilet: you walk slower, and tasks go 10% slower.';   // bathroom at 0 (0.28.41)
const NEED_FX = {   // need: { hi: [effects, reason], lo: [effects, reason] }
  energy:  { hi: [{ task: 1.15 }, 'Well rested: tasks go 15% faster.'], lo: [{ walk: SLOW_SPEED }, 'Tired: you walk slower.'] },
  fitness: { hi: [{ drain: .94, walk: 1.05 }, 'Fit: a spring in your step, and you tire more slowly.'], lo: [{ walk: SLOW_SPEED, drain: 1.06 }, 'Out of shape: you walk slower and tire sooner.'] },
  hunger:  { hi: [{ drain: .96 }, 'Well fed: you tire a little more slowly.'], lo: [{ task: .85 }, 'Hungry: tasks go 15% slower.'] },
  hygiene: { hi: [{ socialGain: 1.5 }, 'Fresh and clean: chatting does you more good.'], lo: [{ socialGain: .5 }, 'You could do with a wash: chatting does half the good.'] },
  social:  { hi: [{ task: 1.1 }, 'In good spirits: tasks go 10% faster.'], lo: [{ drain: 1.05 }, 'Lonely: you tire a little sooner.'] },
  bathroom: { hi: [{ task: 1.05 }, 'Comfortable: tasks go 5% faster.'], lo: [{ task: .9 }, 'You need the toilet: it\'s hard to concentrate, tasks go 10% slower.'] },
  leisure: { hi: [{ friendGain: 1.25 }, 'In good spirits: talking makes friends 25% faster.'], lo: [{ task: .9 }, 'Restless: tasks go 10% slower.'] },   // 0.28.61; friendGain: section 20's Talk a while
};
function needEffects(n = SHIP.player.needs) {             // -> { walk, task, drain, socialGain, notes: [reason], marks: { need: ['up' | 'down', reason] } }
  const e = { walk: 1, task: 1, drain: 1, socialGain: 1, friendGain: 1, notes: [], marks: {} };
  for (const k of NEED_KEYS) {
    const side = n[k] >= NEED_HIGH ? 'hi' : n[k] < NEED_LOW ? 'lo' : null, fx = side && NEED_FX[k][side]; if (!fx) continue;
    for (const f in fx[0]) e[f] *= fx[0][f];
    e.marks[k] = [side === 'hi' ? 'up' : 'down', fx[1]]; e.notes.push(fx[1]);
  }
  if (n.bathroom <= 0) {                                 // bursting (0.28.41, the user's): you hold yourself and walk slower ('+go')
    e.walk *= GO_SPEED; e.marks.bathroom = ['down', GO_SAY]; e.notes[e.notes.indexOf(NEED_FX.bathroom.lo[1])] = GO_SAY;
  }
  const sk = n === SHIP.player.needs && typeof sickFx === 'function' ? sickFx() : null;   // being sick (the career engineer, 0.61.5): slower, more tired
  if (sk) { e.walk = Math.max(SICK.floor, e.walk * sk.walk); e.drain *= sk.drain; e.notes.push(sk.note); }   // never slower than SICK.floor, 40% (reviewer 1d, the lead: phones)
  return e;
}
function needsLoad(s) {                                  // from the save (section 13): v 2 has needs; v 1, none
  const src = s && s.v >= 2 && s.player && s.player.needs, out = {};
  for (const k of NEED_KEYS) { const v = src && src[k]; out[k] = !s ? NEEDS_FRESH[k] : typeof v === 'number' && isFinite(v) ? needClamp(v) : k === 'leisure' ? NEEDS_FRESH.leisure : NEEDS_OLD; }   // a save from before leisure: 70, as a new game
  return out;
}
SHIP.player = { needs: needsLoad(SAVED), carry: [], work: null };   // carry and work come from the save below (the job loop)
// credits, your locker and who you've chatted with today (0.28.10): from the save, read defensively
const CREDITS_FRESH = 40, LOCKER_MAX = 40;
function walletLoad(s) {
  const p = s && s.player, c = p && p.credits, lk = p && p.locker, ch = p && p.chats, chats = {};
  if (ch && typeof ch === 'object') for (const k in ch) if (Number.isInteger(ch[k])) chats[k] = ch[k];
  return { credits: typeof c === 'number' && isFinite(c) && c >= 0 ? Math.floor(c) : CREDITS_FRESH,
    locker: Array.isArray(lk) ? lk.filter(x => typeof x === 'string').slice(0, LOCKER_MAX) : [], chats };
}
Object.assign(SHIP.player, walletLoad(SAVED));
// your name (0.28.22, Pillar 4): typed in the shuttle (section 21, the onboarding engineer, calls playerNameSet); saved
// here as save.player.name. null until then: lines say 'Cadet'. At most NAME_MAX characters, trimmed.
const NAME_MAX = 24;
const nameClean = v => typeof v === 'string' && v.trim() ? v.trim().replace(/\s+/g, ' ').slice(0, NAME_MAX) : null;
SHIP.player.name = nameClean(SAVED && SAVED.player && SAVED.player.name);
function playerNameSet(v) { SHIP.player.name = nameClean(v); return SHIP.player.name; }
SAVE_EXTRA.push(s => { (s.player || (s.player = {})).name = SHIP.player.name; });
// what you did, for the sim's note bus (Pillar 4: section 13's simNote, when it's there; section 21's Settling-in list
// and the dialogue engineer's reactions read it): wash, eat (with: crew at your table), laundry, buy, call
const simAct = (act, o) => { if (typeof simNote === 'function') try { simNote('act', { act, ...o }); } catch (e) { /* a listener's problem, not the player's */ } };
SAVE_EXTRA.push(s => { const p = s.player || (s.player = {}); p.credits = SHIP.player.credits; p.locker = SHIP.player.locker.slice(); p.chats = { ...SHIP.player.chats }; });
SAVE_EXTRA.push(s => { const p = s.player || (s.player = {}); p.needs = { ...SHIP.player.needs }; p.carry = SHIP.player.carry.slice(); p.work = SHIP.player.work && { ...SHIP.player.work, fitted: SHIP.player.work.fitted.slice(), make: SHIP.player.work.make && { ...SHIP.player.work.make } }; });   // into the save (section 13)
// the ship's state (section 17, the systems engineer): shipEffects(deck) gives { restore, drain, walk, notes, ... };
// restore and drain multiply ours (a failing recycler, weaker showers). walk is left out: the user's rule is that
// only low fitness and energy slow you. Read at most once a ship minute; all 1s until section 17 is there.
let FX_MIN = -1, FX_NOW = null;
function playerFx() {
  const m = Math.floor(shipNow()), d = typeof deckDef !== 'undefined' && deckDef ? deckDef.num : 0;
  if (m !== FX_MIN || !FX_NOW || FX_NOW.deck !== d) {
    FX_MIN = m; FX_NOW = null;
    try { if (typeof shipEffects === 'function' && d) FX_NOW = shipEffects(d); } catch (e) { FX_NOW = null; }
    if (!FX_NOW) FX_NOW = { deck: d, restore: {}, drain: {}, notes: [] };
    if (typeof clothesFx === 'function') FX_NOW = clothesFx(FX_NOW);   // section 21b: yesterday's clothes (0.42.40)
  }
  return FX_NOW;
}
const fxR = (fx, k) => fx && fx.restore && isFinite(fx.restore[k]) ? fx.restore[k] : 1;
const fxD = (fx, k) => fx && fx.drain && isFinite(fx.drain[k]) ? fx.drain[k] : 1;
function needsDrain(mins, asleep, fx, except) {          // except: the need an activity is restoring (it doesn't drain meanwhile)
  const n = SHIP.player.needs;
  for (let left = mins; left > 0;) {                     // in steps of up to half an hour, so a long skip feels the bonuses change
    const step = Math.min(left, 30), h = step / 60, ed = asleep ? 1 : needEffects(n).drain; left -= step;
    for (const k of NEED_KEYS) if (k !== except) n[k] = needClamp(n[k] - NEED_DRAIN[k][asleep ? 1 : 0] * fxD(fx, k) * (k === 'energy' ? ed : 1) * h);
    if (asleep) n.energy = needClamp(n.energy + SLEEP_GAIN * fxR(fx, 'energy') * h);
  }
}
// walking speed (needEffects): SLOW_SPEED for low fitness, times SLOW_SPEED again for low energy; 105% when fit
const playerSpeed = (n = SHIP.player.needs) => needEffects(n).walk;
const taskMins = mins => Math.max(1, Math.round(mins / needEffects().task));   // how long a task of so many minutes takes you now
// the line on the device: the lowest need under 50 says something, else all's well
const NEED_SAY = {
  energy: ['You feel sluggish: get some sleep. Your bunk is in Bunk 1 on Deck 4.', 'You\'re getting tired.'],
  fitness: ['You\'re out of shape and slow on your feet: work out at the gym on Deck 3.', 'You could do with some exercise.'],
  hunger: ['You\'re hungry. The mess serves breakfast 06:00-09:00 and dinner 17:00-20:30; the grab shelf is always open.', 'You\'re getting peckish.'],
  hygiene: ['You need a shower. The washrooms are at the ends of the junior wing on Deck 4.', 'A shower would be nice.'],
  social: ['You miss home. The call-home booths are on Deck 3.', 'You\'d like to hear from home.'],
  bathroom: ['You really need the toilet. The washrooms are at the ends of the junior wing on Deck 4.', 'You could do with a trip to the toilet.'],
  leisure: ['You\'re restless. Try a hobby (the Hobbies app on your device), a tradition, or a game of Tiles.', 'You could do with some time to yourself.'],
};
function needsLine() {
  const n = SHIP.player.needs, k = NEED_KEYS.slice().sort((a, b) => n[a] - n[b])[0];
  return bedText(n[k] < SLOW_BELOW ? NEED_SAY[k][0] : n[k] < 50 ? NEED_SAY[k][1] : 'You feel fine.');
}
// your bed's room by name for the texts that say "Bunk 1" (0.45.7, Step 4's loose end): after the move to your cabin
// (SHIP.works.home, which playerBed() follows) they name its room instead
function myBedRoom() {
  const id = typeof playerBed === 'function' ? playerBed() : null, pl = id && (DECKS[4].places || []).find(q => q.id === id), r = pl && DECKS[4].rooms[pl.room];
  return r && r.name ? r.name.replace(/^(Spare|Guest) cabin /, 'Cabin ') : 'Bunk 1';   // 'Cabin 4-23', as the move's Mail says
}
const bedText = s => typeof s === 'string' && s.includes('Bunk 1') ? s.replace(/Bunk 1/g, myBedRoom()) : s;
// quiet moments (0.28.41): what's on screen. popupBusy: a panel, a card, a dialogue, sleep, the lift or a fade is up,
// so nothing new should pop up (the panels are looked at four times a second, the rest every frame). POP.toast / POP.card:
// when an ordinary toast / a tip card or dialogue was last on screen, or a heads-up came up (performance.now(), so virtual in tests).
// The need warnings and the teaching tips (below) wait for a quiet moment; nothing here changes what's shown.
const POP = { at: -1e9, panels: false, busy: false, toast: -1e9, card: -1e9, warn: -1e9, tip: -1e9 };
let TOAST_AT = -1e9;                                     // when toast() last showed one (section 12 stamps it; performance.now(), so virtual in tests; 0.28.48)
const POP_PANELS = ['lift', 'sleepAsk', 'qAsk', 'ixBoard', 'ixHealth', 'chat', 'devAddr', 'seek'];
const popOn = id => { const e = document.getElementById(id); return !!(e && !e.hidden); };
function popupWatch(now) {
  if (now - POP.at >= 250) { POP.at = now; const fe = document.getElementById('fade'); POP.panels = POP_PANELS.some(popOn) || !!(fe && +fe.style.opacity > 0); }
  const dlg = document.body.classList.contains('dlgon') || (typeof DIALOGUE !== 'undefined' && !!DIALOGUE);
  if (now - TOAST_AT < 5600) POP.toast = now;            // a toast is up for 5.6 s: read from its stamp, not the page (whose timer is real time)
  if (dlg || TIP_Q.length || DEV.hu && DEV.hu !== POP.hu || DEV.choose) POP.card = now;   // a heads-up counts as it comes (it can stay up a while, at the side)
  POP.hu = DEV.hu;
  POP.busy = POP.panels || dlg || !!DEV.choose || TIP_Q.length > 0 || sleeping || !!ride;
}
// need warnings (0.28.41, the user's "as any need approaches the lower end a warning and an explanation needs to
// appear"): a gentle toast the first time a need drops under WARN_AT[0] (the low line, where its penalty starts), a firmer
// one under WARN_AT[1]; each need re-arms once it's back to WARN_REARM. One at a time, never over a panel, a card, a
// dialogue or sleep, nor with the device open, and WARN_GAP after anything else; the lowest need goes first. Not the
// Tips setting's (they're about you, not teaching). At 0 nothing more happens (no fail state) except bathroom's '+go'.
const WARN_AT = [NEED_LOW, 10], WARN_REARM = 40, WARN_GAP = 8000;
const NEED_WARN = {   // need: [[title, text] under 25, [title, text] under 10] (text: head writer 3)
  hunger: [['Hungry', 'Getting peckish. Mess on Deck 3: breakfast 06:00-09:00, dinner 17:00-20:30. The grab shelf never closes.'],
    ['Very hungry', 'Starving: tasks are 15% slower. Eat something. The grab shelf in the mess, Deck 3, is always open.']],
  energy: [['Tired', 'You\'re tired, so you\'re walking slower. Your bunk\'s in Bunk 1, Deck 4, from 20:00. By day, sit down a while.'],
    ['Exhausted', 'Exhausted. Get to your bunk, Bunk 1 on Deck 4, and sleep it off.']],
  hygiene: [['Could do with a wash', 'Time for a wash: people enjoy your company less. Showers are in the junior wing washrooms, Deck 4.'],
    ['Really need a shower', 'You really need a shower. Chats do half the good till you\'ve had one. Junior wing, Deck 4.']],
  fitness: [['Out of shape', 'Out of shape: you walk slower and tire sooner. A treadmill or weights session in the Deck 3 gym will help.'],
    ['Badly out of shape', 'Badly out of shape. Get to the gym on Deck 3. Even one workout makes a difference.']],
  social: [['A bit lonely', 'A bit lonely, and tiring sooner for it. Chat with someone, eat with company, or call home from the Deck 3 booths.'],
    ['Missing people', 'Really missing people. Find a friendly face, or call home from the booths on Deck 3.']],
  bathroom: [['Need the toilet', 'You need the toilet. Public washrooms are in the junior wing on Deck 4, and on Deck 3.'],
    ['Bursting', 'You really need the toilet, now! Deck 4 or Deck 3. Hold on, or you\'ll be hopping.']],
  leisure: [['Restless', 'All work lately. Try a hobby on your device, go to a tradition, or play a game of Tiles.'],
    ['Very restless', 'You really need some time to yourself: tasks are 10% slower. A hobby, a tradition or a game of Tiles will help.']],
};
// work wears leisure down (0.73.0, playtest 2 item 23, the user's "work needs to hit leisure a good bit harder"; the
// lead's tuning: a full shift takes 40-50 off; 5 an hour in all, 40 a shift): WORK_LEISURE an hour on top of NEED_DRAIN's while you're at work
// (workingNow: clocked in at the time clock and not out yet, or doing a job's activity), not while something is
// filling leisure. Shown like a gain, a "−5 Leisure" note each time WORK_LS_NOTE has gone (WORK_LS: what's gone since
// the last note; nothing saved). No R().
const WORK_LEISURE = 4.2, WORK_LS_NOTE = 5, WORK_ACTS = new Set(['job', 'fetch', 'make', 'workStep', 'ixStop', 'cartTake', 'cartLoad', 'cartUnload', 'cartBack']);
let WORK_LS = 0;
function workingNow() {
  const A = typeof ACT !== 'undefined' ? ACT : null;
  if (A && A.phase === 'do' && WORK_ACTS.has(A.kind)) return true;
  return typeof careerClockedIn === 'function' && careerClockedIn() && !careerClockedOut() && typeof DAY_SHIFT !== 'undefined' && SHIP.time.min < DAY_SHIFT[1] + 60;
}
function workLeisure(mins, fx, except) {                 // mins awake (playerUpdate); fx the ship's effects
  if (except === 'leisure' || !(mins > 0) || !workingNow()) return;
  const N = SHIP.player.needs, b = N.leisure; N.leisure = needClamp(N.leisure - WORK_LEISURE / 60 * mins * fxD(fx, 'leisure'));
  WORK_LS += b - N.leisure;
  if (WORK_LS >= WORK_LS_NOTE) { needFloat('\u2212' + Math.round(WORK_LS) + ' ' + NEED_LABEL.leisure, 'leisure', -WORK_LS); WORK_LS = 0; }
}
// leisureAdd(n, why) (0.28.61, for every section: section 18's traditions, 20's Talk a while, the bar, calling home):
// adds n leisure (times the ship's restore, like any gain) and returns what it added. why is a short word for the notes
function leisureAdd(n, why) {
  const N = SHIP.player && SHIP.player.needs; if (!N || !(n > 0)) return 0;
  const b = N.leisure; N.leisure = needClamp(N.leisure + n * fxR(playerFx(), 'leisure'));
  return N.leisure - b;
}
let WARN_SAID = {};                                      // need -> 0 armed, 1 the gentle one said, 2 the firm one said
function needWarnTick(now) {
  needGoalTick();                                        // a very low need's marker goes once it's back up (playtest 1)
  const n = SHIP.player.needs; let pick = null, lvl = 0;
  for (const k of NEED_KEYS) {
    if (n[k] >= WARN_REARM) { WARN_SAID[k] = 0; continue; }
    const l = n[k] < WARN_AT[1] ? 2 : n[k] < WARN_AT[0] ? 1 : 0;
    if (l > (WARN_SAID[k] || 0) && (!pick || n[k] < n[pick])) { pick = k; lvl = l; }
  }
  if (!pick || POP.busy || DEV.open || Math.max(POP.toast, POP.card, POP.warn) > now - WARN_GAP) return null;
  const w = NEED_WARN[pick][lvl - 1]; WARN_SAID[pick] = lvl; POP.warn = POP.toast = now;
  if (lvl === 1) needPop(pick); else toast(w[0], bedText(w[1]) + (needGoal(pick) ? ' Follow the marker.' : ''));  // the first one: a pop-up in plain words (0.28.62); the firm one stays a toast, with the way (playtest 1)
  return pick;
}
// the low-need pop-up (0.28.62, the user's "in plain words: 'You need to pee'"): one line beside the need's icon on the
// needs strip (or its folded heart), as the need first crosses the low line. needWarnTick's pacing keeps it one at a time,
// never over a panel, a card or a dialogue. Words: the head writer's need.low.<need> (variant 0), these until they're in.
const NEED_LOW_SAY = { bathroom: 'You need to pee.', hunger: 'You\'re hungry.', energy: 'You\'re tired.', hygiene: 'You could do with a wash.',
  fitness: 'You could do with some exercise.', social: 'You could do with some company.', leisure: 'You could do with some time to yourself.' };
const NEED_POP = { el: null, t: 0 };
function needPop(k) {
  let txt = null; try { txt = careerText('need.low.' + k); } catch (e) { txt = null; }
  txt = bedText(txt || NEED_LOW_SAY[k] || NEED_WARN[k][0][1]);
  let el = NEED_POP.el;
  if (!el) {
    el = NEED_POP.el = document.createElement('div'); el.id = 'needPop'; el.setAttribute('role', 'status'); el.setAttribute('aria-live', 'polite');
    el.style.cssText = 'position:fixed;z-index:3;max-width:min(260px,calc(100vw - 28px));padding:8px 12px;border-radius:12px;background:rgba(13,21,33,.92);border:1px solid var(--line);font-size:14px;line-height:1.3;color:var(--ink);box-shadow:0 6px 18px rgba(0,0,0,.4);pointer-events:auto;cursor:pointer';
    el.onclick = e => { e.stopPropagation(); el.hidden = true; };
    el.addEventListener('pointerdown', e => e.stopPropagation());
    document.body.appendChild(el);
  }
  const strip = needStrip(), icon = strip.querySelector('.ns[data-k="' + k + '"]'), fold = strip.classList.contains('fold'), r = (fold || !icon ? strip : icon).getBoundingClientRect(), sr = strip.getBoundingClientRect();
  el.textContent = txt; el.style.borderColor = NEED_COL[k]; el.hidden = false;
  el.style.left = Math.round(Math.max(14, Math.min(r.left - 6, innerWidth - 14 - el.offsetWidth))) + 'px'; el.style.top = Math.round(sr.bottom + 6) + 'px';
  simClear(NEED_POP.t); NEED_POP.t = simTimeout(() => { el.hidden = true; }, 6000);
  return txt;
}
// teaching tips (0.28.42, the user's "a lot more tips and tutorial bubbles appearing, teaching you. But not too many and
// not too often"): TEACH lists them in priority order, [id, test(c), text]. teachTick (from playerUpdate, once a second)
// shows the first one not seen whose test passes, through the device's tipShow (its card, its saved tipsSeen, its Tips
// setting). Pacing: one every TEACH_GAP at most; none within TEACH_QUIET of another tip card, need warning, heads-up or
// dialogue, nor TEACH_TOAST of a toast; none during the arrival (teachHeld) or while anything's up (POP.busy). App tips ('t:a-...')
// show only over that app on the device; the rest never over the device. A tip whose moment passes waits for the next.
// TEACH_ST: what teachWatch has seen happen (not saved: a reload starts it again, the tips themselves are saved).
const TEACH_GAP = 180000, TEACH_QUIET = 60000, TEACH_TOAST = 6000;
let TEACH_CK = -1e9, TEACH_ST = null;
const teachRecent = (at, c, ms = 120000) => at !== undefined && c.now - at < ms;
const teachMeal = m => m >= MEALS.breakfast[0] && m < MEALS.breakfast[1] || m >= MEALS.dinner[0] && m < MEALS.dinner[1];   // breakfast and dinner at the servery
const TEACH = [   // text: head writer 3. A 4th element { sure: true }: shown when due whatever the 3-minute and 60 s pacing says
  // playtest 2 (0.72.5, HUD U; texts: the head writer's tip.device and tip.laundry.day2, read when shown): item 9, once on your
  // training day while you're on shift; item 19, the laundry tip at the start of Day 2 (from 06:00, before 09:00's shift)
  ['t:devwork', c => c.d === 1 && c.work && c.min >= 9 * 60 + 30 && c.min < 17 * 60 && !c.app, () => careerText('tip.device') || 'Working is a good chance to check out your device. Schedule, Jobs and Tracked are a tap away.'],
  ['t:laund2', c => c.d === 2 && c.min >= 6 * 60 && c.min < 9 * 60, () => careerText('tip.laundry.day2') || 'New day: fresh clothes from your wardrobe. When they run out, take your hamper to the laundry on Deck 4.', { sure: true }],
  ['t:rep', c => c.d >= 1 && (c.S.turnin !== undefined && shipNow() - c.S.turnin >= 30 || c.min >= 1020 || c.d >= 2), 'Not just jobs: kindness and joining in count too. Each department has its own view of you, and so does the ship.', { sure: true }],   // the user's: on the 2nd day (Monday), after your first job's turned in or at the shift's end; half an hour after the turn-in, so Zeke says his part first (0.28.50)
  // free time (0.28.63, the 0.60.7 plan's "Tips for your first evenings"; the plan's approved words): off shift, then one an evening, Days 1-4
  ['t:offshift', c => c.d >= 1 && c.min >= 1020 && c.min < 1290, 'Off shift. Your evening is yours: call home from the booths on Deck 3, go to a ship tradition (Calendar), talk a while with someone, or try a hobby.', { sure: true }],
  ['t:eve-talk', c => c.d === 1 && c.min >= 1110 && c.min < 1320 && !!SHIP.device.tipsSeen['t:offshift'], 'Tap someone and choose Talk a while: a proper chat builds far more friendship than a quick hello.', { sure: true }],
  ['t:eve-hobby', c => c.d === 2 && c.min >= 1050 && c.min < 1320, 'Hobbies fill your Leisure. Open Hobbies on your device to read, write, play a game or watch a film, anywhere you sit or stand still.', { sure: true }],
  ['t:eve-trad', c => c.d === 3 && c.min >= 1050 && c.min < 1260, 'Several traditions on tonight, and you can\'t go to them all. Pick one in the Calendar.', { sure: true }],
  ['t:eve-call', c => c.d === 4 && c.min >= 1050 && c.min < 1320, 'Missing home? The call-home booths on Deck 3 put you through to your people. One call a day.', { sure: true }],
  ['t:garden', c => c.deck === 3 && /garden/i.test(((deckDef.rooms || {})[roomAt(...player.here())] || {}).name || '') && !(c.work && c.min >= 480 && c.min < 1020), 'The garden\'s yours off shift too. Tending a bed counts as a hobby: it fills your leisure.', { sure: true }],   // the user's (0.28.65), the head writer's tip.garden
  ['t:a-hobbies', c => c.app === 'hobbies', 'Hobbies fill your Leisure. Read, write, play games or watch a film on your device anywhere. Drawing, knitting and puzzles need supplies from the crew store on Deck 3; Zeke might teach you to knit.'],
  ['t:a-sched', c => c.app === 'schedule', 'Your day at a glance: meals, your shift, anything booked. Tap an entry and the marker shows the way.'],
  ['t:a-cal', c => c.app === 'calendar', 'The weeks ahead: days off, traditions, birthdays and appointments.'],
  ['t:a-maps', c => c.app === 'maps', 'Every deck, room by room. Tap a room to put the marker on it.'],
  ['t:a-jobs', c => c.app === 'jobs', 'Your job and its steps. The board in the Works bay has the rest.'],
  ['t:a-crew', c => c.app === 'crew', 'Everyone you\'ve met, and how well you know them.'],
  ['t:a-needs', c => c.app === 'needs', 'What each need is doing for you right now: ▲ helping, ▼ holding you back.'],
  ['t:queue', c => ACT && ACT.kind === 'queue', 'The line moves on its own. You\'ll get a tray at the front. Tap anywhere to leave the queue.'],
  ['t:tray', c => !!SHIP.player.tray && !(ACT && ACT.kind === 'eat'), 'Take your tray to any free seat and tap it to eat. Company at the table lifts your spirits too.'],
  ['t:lift', c => teachRecent(c.S.arrived, c), 'Seven decks, one lift. Maps on your device shows where you are and what\'s on every deck.'],
  ['t:deck3', c => c.deck === 3, 'Deck 3 is the Commons: the mess, the gym, the crew store, the call-home booths, the bow lounge and the promenade.'],
  ['t:deck5', c => c.deck === 5, 'Deck 5 is Operations: the Works bay and its job board, main storage and the machine shop. You work here.'],
  ['t:shift', c => c.work && c.min >= 510 && c.min < 540, 'Your shift is 09:00 to 17:00 in the Works bay, Deck 5. Clock in, then take a job from the board.'],
  ['t:dayoff', c => c.work === false && c.min >= 420 && c.min < 1200, 'Day off! No shift today. The garden, a game of Tiles, a long call home, or nothing at all. Your choice.'],
  ['t:fault', c => c.fault, 'A blinking light means a machine is struggling. Faults become jobs on the Works board. The News feed on your device shows how she\'s holding up.'],
  ['t:pay', c => c.S.paid, 'Credits! Spend them at the crew store on Deck 3: snacks and small comforts. Some make good gifts.'],
  ['t:gift', c => giftHeld(), 'You\'re carrying a gift. Tap a crewmate to give it. Everyone has their favourites.'],
  ['t:carry', c => SHIP.player.carry.length > 0 && !giftHeld() && !bagHeld(), 'Parts in hand. Fit them at the job\'s machine. Spares go back to main storage.'],
  ['t:chat', c => Object.keys(SHIP.player.chats).length > 0, 'Chatting lifts your Social. The first chat with someone each day counts most. It\'s how strangers become friends.'],
  ['t:tier', c => c.S.tierUp > 0, 'You\'re getting to know someone. Chats, meals and favours move you along: stranger, acquaintance, colleague, friend, close friend.'],
  ['t:friend', c => c.S.tierUp >= 3, 'A friend! Friends save you a seat, ask you along to things, and sometimes leave a note on your bunk.'],
  ['t:mail', c => mailUnread() > 0, 'New mail. Read it in Mail on your device. Ship traditions are announced the evening before.'],
  ['t:trad', c => c.trad, 'There\'s a ship tradition today. Turn up and join in. It\'s how the crew makes a long voyage feel like home.'],
  ['t:hu', c => c.S.hu, 'Heads-ups tell you what\'s coming. Set how early, or turn them off, in your device\'s Settings.'],
  ['t:sleep', c => c.S.woke, 'Slept well? Your bunk takes you from 20:00 through to 06:00. By day, lie on it to rest.'],
  ['t:late', c => c.min >= 1320, 'Getting late. Your bunk\'s in Bunk 1 on Deck 4. Stay up if you like. You\'ll feel it tomorrow.'],
  ['t:needs', c => NEED_KEYS.some(k => c.n[k] < 50), 'Your needs sit in the strip at the top. Keep them up and the day goes well. Let them drop and you slow down.'],
  ['t:loo', c => c.n.bathroom < 50, 'Public washrooms are in the junior wing on Deck 4, and on Deck 3. Cabin bathrooms are private.'],
  ['t:food', c => c.n.hunger < 50 && !teachMeal(c.min), 'Missed a meal? The grab shelf in the mess, Deck 3, is always open.'],
  ['t:sit', c => c.n.energy < 50, 'Tired? Sit down anywhere for a bit; it slows the tiredness. Lying on your bunk rests you properly.'],
  ['t:gym', c => c.n.fitness < 50, 'The gym on Deck 3 has treadmills and weights. A workout every few days keeps you fit and quick on your feet.'],
  ['t:call', c => c.n.social < 50, 'Missing home? The call-home booths on Deck 3 put you through to Mum, Gran, Jo or Sam.'],
  ['t:bonus', c => c.now - c.S.start > 600000 && Object.values(needEffects(c.n).marks).some(m => m[0] === 'up'), 'Needs kept high give bonuses: well rested, you work faster. The Needs app shows what\'s helping and what isn\'t.'],
  ['t:pause', c => c.now - c.S.start > 900000, 'Need a break? Pause, at the top, stops the ship\'s clock and everyone in it. Tap anywhere to carry on.'],
  ['t:view', c => c.now - c.S.start > 300000, 'Rotate turns the view. Walls lowers them so you can see into rooms. Pinch or scroll to zoom.'],
];
const teachTry = f => { try { return !!f(); } catch (e) { return false; } };
function teachWatch(now) {                               // what's happened, for the tests that need more than a look
  const S = TEACH_ST || (TEACH_ST = { start: now, deck: deckDef.num, cr: SHIP.player.credits, tierUp: 0, slept: false });
  if (deckDef.num !== S.deck && !ride) { S.deck = deckDef.num; S.arrived = now; }
  if (SHIP.player.credits > S.cr) S.paid = true; S.cr = SHIP.player.credits;
  if (sleeping) S.slept = true; else if (S.slept) S.woke = true;
  if (DEV.hu) S.huOn = true; else if (S.huOn) S.hu = true;
  return S;
}
if (typeof onSim === 'function') {
  onSim('tierUp', x => { if (TEACH_ST && x && x.tier > TEACH_ST.tierUp) TEACH_ST.tierUp = x.tier; });
  onSim('job', x => { if (TEACH_ST && x && x.step === 'turnin' && TEACH_ST.turnin === undefined) TEACH_ST.turnin = shipNow(); });   // when (0.28.50)
}
// the intro's arrival (day 0's scripted steps) teaches by itself: tips wait for it. Its first week runs on (introOn() till
// day 8) with tips, which is when they're most use.
const teachHeld = () => typeof introOn === 'function' && introOn() && (!!SHIP.intro.step || SHIP.time.day < 1);
function teachTick(now) {
  if (now - TEACH_CK < 1000) return null; TEACH_CK = now;
  const S = teachWatch(now), D = SHIP.device;
  if (!D || !D.settings.tips || teachHeld() || devLocked() || POP.busy || POP.toast > now - TEACH_TOAST) return null;
  const paced = now - POP.tip >= TEACH_GAP && Math.max(POP.card, POP.warn) <= now - TEACH_QUIET;
  const d = SHIP.time.day, min = SHIP.time.min, deck = deckDef.num;
  const c = { now, S, n: SHIP.player.needs, d, min, deck, app: DEV.open ? DEV.app : null,
    work: teachTry(() => typeof playerShiftOn === 'function') ? !!playerShiftOn(d) : null,
    fault: teachTry(() => typeof machineList === 'function' && machineList().some(m => m.deck === deck && machineLook(m.id).blink)),
    trad: teachTry(() => typeof eventsOn === 'function' && eventsOn(d).some(e => min >= e.from - 60 && min < e.to)) };
  for (const [id, test, text, o] of TEACH) {
    if (D.tipsSeen[id] || !paced && !(o && o.sure) || id.startsWith('t:a-') !== !!DEV.open || !teachTry(() => test(c))) continue;
    let tx = text; if (typeof text === 'function') { try { tx = text(); } catch (e) { tx = null; } }
    if (tipShow(id, bedText(tx))) { POP.tip = POP.card = now; return id; }   // a text may be read when shown (the head writer's, 0.72.5); Bunk 1 names your room (24 core)
  }
  return null;
}
// the news feed (0.28.44, the user's, through the lead: the device's Ship app becomes "News feed"): short posts, newest
// first, each with a time and a source. SHIP.news = [{ at, src, text, id }] (saved, the last FEED_MAX). Posts come from
// head writer 3's bank (content/banks/news.lines: kinds 'news.<src>', a crew member as the subject, conditions as
// triggers) through section 22's lineFor, so the feed fills in once that bank is in the build. Each ship day has 2-6
// slot times (newsSlots: a hash of the day, no R()) between 06:30 and 21:30; a slot picks a source (NEWS_W, at most
// NEWS_PER_SRC a day) and a subject, and posts what lineFor gives. On top: today's traditions at 06:00, tomorrow's at
// 18:00 (ctx.flags 'trad.tomorrow.<id>'), one just held (the 'tradition' note: ctx.trad and 'trad.done.<id>'), your own
// repair (the 'repair' note, who 'you'), and a ship system getting worse or better (section 17's shipHealthRows). A post
// id never comes back within NEWS_COOL ship days (SHIP.newsUsed, saved). newsTick runs once a ship minute; after a time
// skip it catches up on the slots of the last NEWS_CATCH minutes.
const NEWS_SRC = { bridge: 'Bridge', galley: 'Galley', works: 'Works', garden: 'Garden', infirmary: 'Infirmary', trad: 'Traditions',
  crew: 'Crew', gossip: 'Overheard', outside: 'Outside', notice: 'Noticeboard' };
const NEWS_W = { bridge: 2, galley: 2, works: 2, garden: 1, infirmary: 1, crew: 2, gossip: 2, outside: 1, notice: 1 };
const NEWS_DEPT = { bridge: ['command', 'helm', 'comms', 'watch'], galley: ['galley'], works: ['works'], garden: ['survey', 'galley'], infirmary: ['infirmary'] };
const FEED_MAX = 40, NEWS_COOL = 7, NEWS_PER_SRC = 2, NEWS_CATCH = 720;
const newsH = (d, k) => { let h = (d * 2654435761 + k * 40503) >>> 0; h ^= h >>> 15; h = Math.imul(h, 2246822507) >>> 0; h ^= h >>> 13; return (h >>> 0) / 4294967296; };
function newsLoad(s) {
  const n = s && Array.isArray(s.news) ? s.news : [], u = s && Array.isArray(s.newsUsed) ? s.newsUsed : [];
  return { news: n.filter(x => x && isFinite(x.at) && typeof x.text === 'string' && NEWS_SRC[x.src]).slice(0, FEED_MAX).map(x => ({ at: +x.at, src: x.src, text: x.text.slice(0, 200), id: typeof x.id === 'string' ? x.id : '' })),
    used: u.filter(x => Array.isArray(x) && typeof x[0] === 'string' && Number.isInteger(x[1])).slice(-120),
    at: s && isFinite(s.newsAt) ? +s.newsAt : null, rows: s && s.newsRows && typeof s.newsRows === 'object' ? { ...s.newsRows } : {} };
}
{ const L = newsLoad(SAVED); SHIP.news = L.news; SHIP.newsUsed = L.used; SHIP.newsAt = L.at; SHIP.newsRows = L.rows; }
SAVE_EXTRA.push(s => { s.news = SHIP.news.slice(0, FEED_MAX); s.newsUsed = SHIP.newsUsed.slice(-120); s.newsAt = SHIP.newsAt; s.newsRows = { ...SHIP.newsRows }; });
function newsSlots(d) {                                  // -> sorted ship minutes of the day's slots (2 to 6)
  const n = 2 + Math.floor(newsH(d, 1) * 5), out = [];
  for (let i = 0; i < n; i++) out.push(390 + Math.floor(newsH(d, 10 + i) * 900));
  return out.sort((a, b) => a - b);
}
function feedAdd(at, src, text, id) {
  if (!text || !NEWS_SRC[src]) return false;
  const d = Math.floor(at / 1440) + 1;
  SHIP.news.unshift({ at, src, text, id: id || '' }); SHIP.news.sort((a, b) => b.at - a.at); if (SHIP.news.length > FEED_MAX) SHIP.news.length = FEED_MAX;
  if (id) { SHIP.newsUsed.push([id, d]); if (SHIP.newsUsed.length > 120) SHIP.newsUsed.splice(0, SHIP.newsUsed.length - 120); }
  return true;
}
const newsCount = (d, src) => SHIP.news.filter(x => Math.floor(x.at / 1440) + 1 === d && (!src || x.src === src)).length;
// a post from the bank: tries a few subjects (the source's department first) until a line fits; null without one
function newsLine(src, at, ctx = {}) {
  if (typeof lineFor !== 'function' || typeof LINES === 'undefined' || !LINES['news.' + src] || typeof ROSTER === 'undefined') return null;
  const d = Math.floor(at / 1440) + 1, used = new Set(SHIP.newsUsed.filter(x => x[1] > d - NEWS_COOL).map(x => x[0]));
  const crew = ROSTER.filter(p => p && p.id && p.rank !== 'guest'), depts = NEWS_DEPT[src];
  const pool = depts ? crew.filter(p => depts.includes(p.dept)).concat(crew.filter(p => !depts.includes(p.dept))) : crew;
  if (!pool.length) return null;
  const k0 = Math.floor(newsH(d, at % 1440) * pool.length);
  for (let i = 0; i < 4; i++) {
    const p = pool[(depts && i < 2 ? Math.floor(newsH(d, at + i) * Math.max(1, crew.filter(q => depts.includes(q.dept)).length)) : k0 + i * 7) % pool.length];
    let r = null; try { r = lineFor(p.id, 'news.' + src, { ...ctx, t: at, peek: true, keep: e => !used.has(e.id) }); } catch (e) { r = null; }
    if (r && r.text) return { text: r.text, id: r.id || (r.e && r.e.id) || '' };
  }
  return null;
}
function newsPost(src, at, ctx, fallback) {
  const L = newsLine(src, at, ctx);
  if (L) return feedAdd(at, src, L.text.charAt(0).toUpperCase() + L.text.slice(1), L.id);   // a post never starts lower case ({trad} first, 0.28.60)
  return fallback ? feedAdd(at, src, fallback, '') : false;
}
function newsSlot(at) {                                  // a slot: the source by weight, at most NEWS_PER_SRC each a day
  const d = Math.floor(at / 1440) + 1, srcs = Object.keys(NEWS_W).filter(k => newsCount(d, k) < NEWS_PER_SRC);
  if (!srcs.length) return false;
  let r = newsH(d, 100 + at % 1440) * srcs.reduce((a, k) => a + NEWS_W[k], 0);
  const order = srcs.slice(); let first = order[order.length - 1];
  for (const k of order) { r -= NEWS_W[k]; if (r < 0) { first = k; break; } }
  for (const k of [first, ...order.filter(x => x !== first)]) if (newsPost(k, at, {})) return true;   // the first source with a line
  return false;
}
// a tradition's name mid-sentence (0.28.60, reviewer 1f's LOW on 0.28.49): "the quiet watch", "quiz night", but
// "Brennan's tasting table", "Founding Day", "Sunday swap meet" and "Works Friday tea" keep their capitals (a crew
// name, a weekday or a proper word first, possessive or not). Only the first letter ever changes. A post that starts
// with it gets its capital back (newsPost).
const TRAD_PROPER = new Set(['Works', 'Founding', 'Captain', 'Veyli', 'Wren', 'Envoy', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']);
function tradName(n) {
  n = String(n || ''); const w = n.split(/[\s-]/)[0];
  const k = w.replace(/'s$/, '');                        // "Brennan's" is a name; "Year's end" isn't
  if (!k || TRAD_PROPER.has(k) || typeof ROSTER !== 'undefined' && ROSTER.some(p => String(p.name || '').split(' ').includes(k))) return n;
  return n.charAt(0).toLowerCase() + n.slice(1);
}
function newsTrad(at, d, when) {                         // today's traditions (06:00) or tomorrow's (18:00)
  if (typeof eventsOn !== 'function') return;
  let es = []; try { es = eventsOn(d) || []; } catch (e) { es = []; }
  for (const e of es.slice(0, 2)) {
    const ctx = when === 'today' ? { trad: tradName(e.name || e.id), tradId: e.id } : { flags: { ['trad.tomorrow.' + e.id]: true } };   // {trad} fills with the name (0.28.49, reviewer 1e)
    newsPost('trad', at, ctx, when === 'today' ? 'Today aboard: ' + e.name + ' at ' + hhmm(e.from) + '.' : null);
  }
}
function newsRows(at) {                                  // a ship system getting worse or better (section 17), as a Works post
  if (typeof shipHealthRows !== 'function') return;
  let rows = []; try { rows = shipHealthRows(); } catch (e) { rows = []; }
  const R_ = SHIP.newsRows, rank = { fine: 0, worn: 1, poor: 2, failing: 3 };
  for (const r of rows) {
    const was = R_[r.key], now = rank[r.state] !== undefined ? rank[r.state] : 0; R_[r.key] = now;
    if (was === undefined || was === now) continue;
    if (now > was && now >= 2) feedAdd(at, 'works', (r.worst ? r.worst.charAt(0).toUpperCase() + r.worst.slice(1) : r.name) + ' running rough: ' + r.name.toLowerCase() + ' at ' + r.value + '%. A job\'s on the board.', '');
    else if (now < was && now <= 1 && was >= 2) feedAdd(at, 'works', r.name + ' back to normal. Thanks to whoever fixed it.', '');
  }
}
if (typeof onSim === 'function') {
  onSim('tradition', x => { if (!x || !x.id) return; const at = isFinite(x.at) ? x.at : shipNow(), d = Number.isInteger(x.day) ? x.day : Math.floor(at / 1440) + 1;
    let e = null; try { e = typeof eventsOn === 'function' ? (eventsOn(d) || []).find(q => q.id === x.id) : null; } catch (err) { e = null; }
    newsPost('trad', at, { trad: tradName(e && e.name || x.id.replace(/-/g, ' ')), tradId: x.id, flags: { ['trad.done.' + x.id]: true } }); });
  onSim('repair', x => { if (x && x.who === 'you') newsPost('works', isFinite(x.t) ? x.t : shipNow(), { machine: typeof machineLabel === 'function' && typeof machineById === 'function' && machineById(x.machine) ? machineLabel(machineById(x.machine)) : undefined }); });
}
function newsTick(now) {                                 // once a ship minute (playerUpdate)
  now = Math.floor(now); const from = SHIP.newsAt === null ? now : Math.max(SHIP.newsAt + 1, now - NEWS_CATCH);
  SHIP.newsAt = now; if (from > now) return;
  for (let d = Math.floor(from / 1440) + 1; d <= Math.floor(now / 1440) + 1; d++) {
    const base = (d - 1) * 1440, inside = m => base + m >= from && base + m <= now;
    if (inside(360)) newsTrad(base + 360, d, 'today');
    for (const m of newsSlots(d)) if (inside(m)) newsSlot(base + m);
    if (inside(1080)) newsTrad(base + 1080, d + 1, 'tomorrow');
  }
  newsRows(now);
}
// pause (0.28.48, the user's "Need a pause button"): PAUSE.on stops the ship. The main loop (section 12) skips ship time
// and every sim step while it's set (input, you, the crew, the galley, the Works, events, social, the intro) and only
// draws. pauseSet(on): a calm overlay with Resume (a tap anywhere resumes), saved on pausing; a hidden tab pauses too and
// stays paused. Resuming moves the real-time stamps that pace things (the warnings' and tips' gaps, a dialogue's
// auto-advance) on by the pause, so nothing jumps; toasts and the ghost-tap guard keep their own real time. Paused time
// simply doesn't pass: determinism is untouched.
const PAUSE = { on: false, since: 0, tiles: null, tilesTap: null };   // tiles / tilesTap: section 23's (0.28.50)
function pauseSet(on) {
  on = !!on; if (on === PAUSE.on) return PAUSE.on;
  const now = performance.now(), btn = document.getElementById('pauseBtn');
  let el = document.getElementById('pauseCard');
  if (!el) {
    el = document.createElement('div'); el.id = 'pauseCard'; el.hidden = true; el.setAttribute('role', 'dialog'); el.setAttribute('aria-label', 'Paused');
    el.style.cssText = 'position:fixed;inset:0;z-index:60;display:none;align-items:center;justify-content:center;background:rgba(6,14,18,.55)';
    el.innerHTML = '<div style="padding:20px 26px;border-radius:14px;background:rgba(8,20,26,.94);border:1px solid #6fa8b0;color:#e6f0f1;text-align:center;font:inherit">'
      + '<div style="font-size:20px;font-weight:600;margin-bottom:6px">Paused</div><div style="opacity:.8;margin-bottom:14px">The ship waits for you.</div>'
      + '<button type="button" style="font:inherit;min-height:44px;padding:8px 22px;border-radius:10px;border:1px solid #6fa8b0;background:#16323a;color:#e6f0f1">Resume</button></div>';
    el.addEventListener('pointerdown', e => { e.stopPropagation(); e.preventDefault(); pauseSet(false); });
    el.querySelector('button').onclick = e => { e.stopPropagation(); pauseSet(false); };   // Enter or Space on the focused Resume (0.28.54, reviewer 1f)
    document.body.appendChild(el);
  }
  if (on) {
    PAUSE.on = true; PAUSE.since = now; try { saveGame(); } catch (e) { /* the save's own problem */ }
  } else PAUSE.on = false;
  freezeSync();                                          // section 13's frozen clock (0.28.50): it calls pauseShift as the freeze ends
  el.hidden = !on; el.style.display = on ? 'flex' : 'none';   // the inline display would beat [hidden]
  if (on && !document.hidden) try { el.querySelector('button').focus(); } catch (e) { /* no focus */ }   // Resume has the keyboard (0.28.54)
  else if (!on && document.activeElement && el.contains(document.activeElement)) try { document.activeElement.blur(); } catch (e) { /* fine */ }
  if (btn) { btn.setAttribute('aria-pressed', String(on)); btn.setAttribute('aria-label', on ? 'Resume the game' : 'Pause the game'); const sp = btn.querySelector('span'); if (sp) sp.textContent = on ? 'Resume' : 'Pause'; }
  return PAUSE.on;
}
// leaving any freeze (Pause, a game of Tiles): the real-time stamps that pace things move on by it (section 13's freezeSync)
function pauseShift(d) {
  if (!(d > 0)) return;
  for (const k of ['at', 'toast', 'card', 'warn', 'tip']) POP[k] += d; TOAST_AT += d;
  TEACH_CK += d; if (typeof DIALOGUE !== 'undefined' && DIALOGUE && isFinite(DIALOGUE.at)) DIALOGUE.at += d;
}
// narrow phones (0.28.50): the 3 x 2 icon grid has no room for a 7th (a third row would sit under the tip card and the
// heads-up), so Pause sits beside the Device button at its height (CSS), lined up here; a 44px tap target
function pausePlace() {
  const b = document.getElementById('pauseBtn'), d = document.getElementById('devBtn'); if (!b || !d) return;
  if (!matchMedia('(max-width:720px),(max-height:500px)').matches) { b.style.left = b.style.top = b.style.height = ''; return; }
  const put = () => { const r = d.getBoundingClientRect(); b.style.left = Math.round(r.right + 8) + 'px'; b.style.top = Math.round(r.top) + 'px'; b.style.height = Math.round(r.height) + 'px'; };
  const hits = () => { const q = b.getBoundingClientRect(); return [...document.querySelectorAll('.controls button')].some(o => { if (o === b || !o.offsetWidth) return false; const r = o.getBoundingClientRect(); return r.left < q.right + 4 && q.left < r.right && r.top < q.bottom && q.top < r.bottom; }); };
  d.classList.remove('compact'); put();
  if (hits()) { d.classList.add('compact'); put(); }       // the narrowest phones (0.28.59; 320 px): the Device button drops its word so Pause clears the round buttons
}
addEventListener('resize', pausePlace); setTimeout(pausePlace, 0);
if (typeof ResizeObserver === 'function') new ResizeObserver(() => pausePlace()).observe(document.getElementById('devBtn'));   // the mail count widens it
{ const b = document.getElementById('pauseBtn'); if (b) b.onclick = e => { e.stopPropagation(); pauseSet(!PAUSE.on); }; }
document.addEventListener('visibilitychange', () => { if (document.hidden) pauseSet(true); });
// paused, the keyboard stays on the card (0.28.54, reviewer 1f): Tab keeps to Resume, never the HUD buttons under it; Escape resumes
addEventListener('keydown', e => {
  if (!PAUSE.on) return;
  const b = document.querySelector('#pauseCard button');
  if (e.key === 'Tab') { e.preventDefault(); if (b) b.focus(); }
  else if (e.key === 'Escape') { e.preventDefault(); pauseSet(false); }
}, true);

// ---- mail (0.28.10): any section sends with mailSend({ at, from, subject, body }) (at: absolute ship minutes, now if
// left out). SHIP.mail holds the newest MAIL_MAX, newest first: { id, at, from, subject, body, read }. Saved in
// save.mail (SAVE_EXTRA), read back defensively. New mail shows a count on the device button and a toast (one for a
// batch: several sections can send in the same moment, a sleep's catch-up most of all). ----
const MAIL_MAX = 60;
function mailLoad(s) {
  const m = s && Array.isArray(s.mail) ? s.mail : [];
  return m.filter(x => x && typeof x === 'object' && typeof x.subject === 'string').slice(0, MAIL_MAX).map((x, i) => ({
    id: Number.isInteger(x.id) ? x.id : -i, at: isFinite(x.at) ? +x.at : 0, from: typeof x.from === 'string' ? x.from : 'Ship',
    subject: x.subject, body: typeof x.body === 'string' ? x.body : '', read: !!x.read, ...(typeof x.play === 'string' ? { play: x.play.slice(0, 60) } : {}) }));
}
SHIP.mail = mailLoad(SAVED).concat(SHIP.mail || []);
SAVE_EXTRA.push(s => { s.mail = SHIP.mail.map(m => ({ ...m })); });
let mailNew = [], mailTimer = 0;
function mailSend({ at, from, subject, body, quiet, play } = {}) {   // quiet: no toast (the welcome, under the first toast); play: a recording (0.28.30, social B2's 'home:gran')
  if (!SHIP.mail) SHIP.mail = [];
  const id = SHIP.mail.reduce((a, m) => Math.max(a, m.id), 0) + 1;
  const m = { id, at: isFinite(at) ? +at : shipNow(), from: String(from || 'Ship'), subject: String(subject || '(no subject)'), body: String(body || ''), read: false };
  if (play) m.play = String(play).slice(0, 60);
  SHIP.mail.unshift(m); SHIP.mail.sort((a, b) => b.at - a.at || b.id - a.id); SHIP.mail.length = Math.min(SHIP.mail.length, MAIL_MAX);
  if (!quiet) mailNew.push(m);
  if (!mailTimer && mailNew.length) mailTimer = setTimeout(() => {         // one toast for a batch
    const n = mailNew.filter(x => !x.read); mailNew = []; mailTimer = 0;
    if (n.length && !(typeof sleeping !== 'undefined' && sleeping)) toast('Your device', n.length === 1 ? 'New mail from ' + n[0].from + ': ' + n[0].subject + '.' : n.length + ' new messages. Open your device to read them.');
  }, 0);
  try { device.refresh(); } catch (e) { /* sent before the device exists: it shows on the first refresh */ }
  return id;
}
const mailUnread = () => SHIP.mail.filter(m => !m.read).length;
function mailWelcome() {
  mailSend({ from: 'Works Office', subject: 'Welcome aboard the Wren', body: 'Welcome to the CSV Wren, Cadet. You\'re a Works technician on the day shift: '
    + 'take jobs from the job board in the Works bay on Deck 5 (your device keeps track of them), fetch parts from main storage, and keep the ship running. '
    + 'Look after yourself too: eat in the mess on Deck 3, shower in the junior wing\'s washrooms, keep fit at the gym, and get some sleep: your bunk is in Bunk 1. '
    + 'Your pay is credited for each job you finish; the store on Deck 3 sells snacks and small comforts. Welcome aboard.', quiet: true });
}

// ---- activities: tap the thing. ACT_TAP picks the activity by what you tapped, then the nearest free place of
// its types (on this deck, within ACT_NEAR m of the thing). Without a place nearby the tap does what it always did. ----
const PLAYER_ACTS = {   // need and gain over mins ship minutes; pose: the crowd's (anim names fall back to stand until 8b has them)
  gym:    { need: 'fitness', gain: 30, mins: 30, cost: { energy: 6 }, title: 'Working out', done: 'Workout done. You feel loose and warm.' },
  call:   { need: 'social', gain: 40, mins: 15, pose: 'call', title: 'Calling home', done: 'You say goodbye and send it off. It\'ll be days getting there.' },
  browse: { mins: 8, pose: 'browse', title: 'Browsing' },
  pay:    { mins: 2, pose: 'pay', title: 'Paying' },
  shower: { need: 'hygiene', gain: 80, mins: 10, pose: 'stand', title: 'Showering', done: 'Clean, and smelling of the ship\'s one soap.' },
  toilet: { need: 'bathroom', gain: 100, mins: 3, pose: 'sit', cost: { hygiene: 3 }, title: 'Toilet', done: 'Now wash your hands at the basins.' },   // any public toilet (0.28.19); a little hygiene, back at the basins (15b's ixBasin, playtest 1)
  tray:   { mins: 1, pose: 'stand', title: 'At the servery' },
  queue:  { mins: 1, pose: 'stand', title: 'In the queue', until: A => {   // the servery's queue (section 16): wait for your turn, then take a tray
    if (!galleyTurn('player')) return false;
    const f = foodFrom('servery'); A.o.dish = f.ok ? f.dish : null; A.o.why = f.why; return true;
  } },
  eat:    { need: 'hunger', gain: 55, mins: 20, title: 'Eating', done: 'You finish up and leave your tray for clearing.' },   // no tray return (the user, 0.60.7)
  grab:   { need: 'hunger', gain: 25, mins: 3, pose: 'browse', title: 'Grab and go', done: 'Something to eat on the way.' },
  fetch:  { mins: 4, pose: 'browse', title: 'Main storage' },   // the job loop (B2): parts off the shelf, the machine's panel, parts back
  job:    { mins: 3, pose: 'work', title: 'Your job' },
  stow:   { mins: 2, pose: 'browse', title: 'Main storage' },
  make:   { mins: 60, pose: 'work', title: 'Machine shop' },   // section 17's JOB_MAKE: an hour a part, like the crew
  craft:  { mins: 15, pose: 'work', title: 'Machine shop' },   // a small gift, no job (0.28.25: section 20's GIFT_MAKES sets the minutes)
  sit:    { mins: 1, pose: 'sit', title: 'Sitting', until: () => false },   // sit anywhere (0.28.12): until you get up
  hobby:  { need: 'leisure', gain: 25, mins: 30, pose: 'sit:read', title: 'Hobby', done: 'You put it away.', until: A => hobbyUntil(A) },   // a hobby (0.28.61): see HOBBIES
  lie:    { mins: 1, pose: 'lie', title: 'Your bunk', until: () => false },   // lying in your bunk (0.28.29): until you get up
  cartTake: { mins: 2, pose: 'stand', title: 'Cart bay' },     // the cart run (0.28.11): the crew's own times (section 17's jobRun)
  cartLoad: { mins: 10, pose: 'work+cart', title: 'Cargo hold' },
  cartUnload: { mins: 15, pose: 'work+cartfull', title: 'Unloading' },
  cartBack: { mins: 2, pose: 'stand+cart', title: 'Cart bay' },
};
// the store (0.28.10): browsing picks something from the shelf you tapped (a different one each visit), the counter
// sells it. Snacks are eaten on the way out (+hunger); comforts go in your locker (+social). Credits: CREDITS_FRESH
// to start, JOB_PAY for each job you finish.
const STORE = {
  snack: [['a bag of dried apple', 2, 6], ['a bar of ship-made chocolate', 3, 8, 'bar of chocolate'], ['a pot of spiced nuts', 3, 8], ['a honey flapjack', 2, 7], ['a packet of biscuits', 3, 6, 'biscuits']],
  drink: [['a cold fizzy lime', 2, 4], ['a bottle of cold tea', 2, 4], ['a carton of oat milk', 2, 5], ['a tin of tea', 4, 3, 'tin of tea']],
  comfort: [['a paperback novel', 8, 5, 'paper novel'], ['a pair of soft socks', 6, 4], ['a postcard of Earth', 3, 3, 'postcard'], ['a little potted succulent', 10, 6, 'little plant'], ['a deck of cards', 5, 4], ['a scented candle (unlit, ship rules)', 7, 4], ['a puzzle book', 6, 4, 'puzzle book'], ['a music chip of old songs', 4, 4, 'music chip'], ['a pocket puzzle', 4, 3, 'pocket puzzle'], ['a spare tiles set', 6, 4, 'spare tiles set']],
};
// gifts (0.28.25, Pillar 4: section 20's giftAdd): a store line with a 4th name is a gift (SOC_GIFTS' name). Bought, it
// goes into your hands to give to someone (giftAdd) instead of your locker or your mouth; hands full, as before.
const STORE_SHELF = it => /fridge/i.test(it.t) ? 'drink' : /display/i.test(it.t) ? 'comfort' : 'snack';
const JOB_PAY = 15;
function storePick(kind) {                               // the next thing on that shelf: deterministic, never R()
  if (kind === 'comfort' && typeof HOBBIES !== 'undefined') {   // hobby supplies first, one of each you don't have yet (0.28.63, the 0.60.7 plan)
    const id = ['draw', 'puzzle', 'knit'].find(h => !hobbyHas(h));
    if (id) { const h = HOBBIES[id]; let name = null; try { name = careerText('hobby.store.' + id); } catch (e) { name = null; } return { kind: 'hobby', name: name || h.prop, price: h.price, gain: 0, gift: null, hobby: id }; }
  }
  const list = STORE[kind], n = SHIP.player.locker.length + (SHIP.player.bought || 0) + SHIP.time.day;
  const [name, price, gain, gift] = list[n % list.length];
  return { kind, name, price, gain, gift: gift || null };
}
const ACT_TAP = [   // what you tapped (its title), the place types it leads to, the activity
  [/treadmill|rowing|weights|mats/i, ['gym'], 'gym'],
  [/^booth/i, ['callhome'], 'call'],
  [/^shelves$|drinks fridge|window display/i, ['shop'], 'browse'],
  [/^counter$/i, ['work:store'], 'pay'],
  [/^servery$/i, ['servery-queue'], 'tray'],
  [/^grab and go$/i, ['grab-shelf'], 'grab'],
  [/table/i, ['mess-seat'], 'eat'],
  [/^shower$/i, ['shower'], 'shower'],
  [/^toilet$/i, ['toilet'], 'toilet'],
];
const PRIVATE_TYPES = new Set(['shower', 'toilet']);     // someone's own (privatePlace) is never offered: wash pods, cabins' toilets
const ACT_NEAR = 2.4;
let ACT = null, basket = null, needsT = null, PLAYER_V0, slowWas = {}, devMin = -1;
const heldBy = id => DECK_CREW.find(a => a.goalId === id);       // crew at a place, or on their way to it
const playerHolds = () => ACT && ACT.placeId || null;             // the place you're using (for the schedules, later)
function privatePlace(pl) {                              // someone's own: named after a bed, or in a room with a bed
  const mine = playerBed();
  for (const q of PLACE_OF.values()) if (q.type === 'bed' && q.id !== mine && (q.room === pl.room || pl.id.startsWith(q.id + '-'))) return true;
  return false;
}
// food comes from the galley (section 16, the galley engineer): galleyServe(where, peek) with where 'servery' or
// 'grab' gives { ok, dish } or { ok: false, why }; peek only asks. Until it's there: the servery is open in the
// meal windows, the shelf always.
const dishName = d => typeof d === 'string' && d && !/\b(null|undefined)\b/.test(d) ? d : 'the hot meal';   // never "a tray: null" (reviewer 1c, 0.28.38)
function foodFrom(where, peek) {
  if (typeof galleyServe === 'function') return galleyServe(where, peek);
  if (typeof takePortion === 'function') {               // section 16 as built (0.29.0): takePortion gives a hot portion, else
    const sv = typeof galleyText === 'function' ? galleyText('servery') : '', gr = typeof galleyText === 'function' ? galleyText('grab') : '';
    const hot = /^(Serving|Ready): ([^.]+)\./.exec(sv);   // something from the grab shelf, else false; galleyText says what's on
    if (peek) {
      if (where === 'servery' && /^Closed/.test(sv)) return { ok: false, why: sv + ' The grab-and-go shelf usually has something.' };
      if (!hot && /empty/i.test(gr)) return { ok: false, why: 'Nothing to eat just now. ' + sv + ' ' + gr };
      return { ok: true };
    }
    if (!takePortion('player')) return { ok: false, why: 'Nothing to eat just now. ' + sv + ' ' + gr };
    return { ok: true, dish: hot ? (where === 'grab' ? 'a hot plate of ' : '') + hot[2] : 'something from the grab shelf' };
  }
  if (where === 'grab') return { ok: true, dish: 'a roll and an apple' };
  const m = SHIP.time.min;
  if (m >= MEALS.breakfast[0] && m < MEALS.breakfast[1]) return { ok: true, dish: 'breakfast' };
  if (m >= 1020 && m < 1230) return { ok: true, dish: 'dinner' };
  return { ok: false, why: 'The servery is closed. Breakfast is 06:00 to 09:00, dinner 17:00 to 20:30. The grab-and-go shelf is always open.' };
}
// a gift from the garden (0.28.25, the galley engineer's notes): on a harvest day (section 16's gardenHarvestDay), once
// your garden run (section 17's chore 'garden', id 'garden@<minute>') has its pickup ticked off, a sprig of herbs and/or
// a tomato from that lot (SHIP.galley.garden.crates, matched by id; GARDEN_CROPS) go into your hands as gifts (giftAdd),
// once a run. Checked each ship minute. Flowers aren't a crop, so none for now.
const GARDEN_GIFTS = { herbs: 'herbs', tomatoes: 'tomato' }, GARDEN_GIVEN = new Set();
function gardenGift() {
  if (typeof giftAdd !== 'function' || typeof myJob !== 'function' || typeof GARDEN_CROPS === 'undefined' || !SHIP.galley || !SHIP.galley.garden) return;
  const j = myJob(); if (!j || j.chore !== 'garden' || GARDEN_GIVEN.has(j.id) || !(j.stepsDone || []).length) return;
  GARDEN_GIVEN.add(j.id);
  if (typeof gardenHarvestDay === 'function' && !gardenHarvestDay(SHIP.time.day)) return;
  const lot = (SHIP.galley.garden.crates || []).find(c => c && c.id === j.id), got = [];
  for (const [ci] of (lot && lot.items) || []) { const g = GARDEN_GIFTS[(GARDEN_CROPS[ci] || {}).id]; if (g && !got.includes(g) && giftAdd(g)) got.push(g); }
  if (got.length) toast('The garden', 'You tuck ' + got.map(g => g === 'herbs' ? 'a sprig of herbs' : 'a ripe tomato').join(' and ') + ' aside to give to someone.');
}
// your bunk (0.28.25, Pillar 4): with section 20's bunkNote, a tap on your own bunk walks you there and shows a friend's
// note if one was left (the oldest unread; marked read), else does what a bunk tap always did (offerSleep, section 13)
function bunkTap(it, at) {
  if (typeof playerBed !== 'function' || typeof PLACE_OF === 'undefined') return false;   // section 20's bunkNote optional (0.28.29)
  const id = playerBed(), bed = PLACE_OF.get(id); if (!bed || at.distanceTo(cellPos(...bed.at)) > 1.2) return false;
  const p = at.clone();
  approach(p, it.front, it.depth, () => { let n = null; try { n = typeof bunkNote === 'function' ? bunkNote() : null; } catch (e) { n = null; }
    if (n) toast('A note on your bunk', 'From ' + n.from + ': "' + n.text + '"'); else bunkPick(id); });
  return true;
}
// lying down (0.28.29, the user's "I can't lay down in bed"): your bunk (only yours; the others' are private) lies you
// down in it, the crowd's 'lie' pose at its mattress, until you tap anywhere to get up. Lying rests you: no energy
// drain and LIE_GAIN a minute. From 20:00 (section 13's bedtime) you then sleep there (offerSleep: the fade, 06:00)
// and wake still lying in it. Before 0.28.29 a tap only slept you at night (standing) or said "Too early".
const LIE_GAIN = .05;                                    // energy a ship minute lying down: 3 an hour
function bunkLie(id) {
  const sick = typeof sickNow === 'function' && sickNow(), night = typeof bedtime === 'function' && bedtime() || sick;   // unwell: you sleep it off, by day too (0.61.5)
  actStart('lie', id, { title: 'Your bunk', sleep: night, after: sick ? 'You crawl into your bunk and close your eyes.' : night ? 'You climb into your bunk and pull the blanket up.' : 'You lie down for a rest. Tap anywhere to get up.' });
}
// the Thursday inspection's berth (Pillar 5, m3): on an inspection morning (Thursday 05:30-08:00, not unwell) a tap on
// your bunk asks: Make the bed (SHIP.player.bedMade = the day; saved; cleared when you next sleep in it), Tidy your locker
// (puts away what you bought since, SHIP.player.untidy; lockerTidy()) or Lie down. Each a 1-minute hold. Any other time: lie down
const bunkMorning = () => weekday(SHIP.time.day) === 3 && SHIP.time.min >= 330 && SHIP.time.min < 480 && !(typeof sickNow === 'function' && sickNow());
const lockerTidy = () => !SHIP.player.untidy || typeof cabinPutAway === 'function' && cabinPutAway();   // 24t: things placed in your cabin count as put away (E4, 0.53.11)
Object.assign(PLAYER_ACTS, { bedMake: { mins: 1, pose: 'work', title: 'Your bunk' }, tidy: { mins: 1, pose: 'work', title: 'Your locker' } });
function bunkPick(id) {
  const P = SHIP.player, made = P.bedMade === SHIP.time.day;
  if (!bunkMorning() || made && lockerTidy() || typeof deviceChoose !== 'function') { bunkLie(id); return; }
  const s = placeSpot(id), c = s && s.walk ? cellPos(...s.walk) : null, spot = c ? { ...s, x: c.x, z: c.z, y: 0, id: null, pose: 'stand' } : null;   // beside it, on your feet
  const opts = (made ? [] : [['Make the bed', () => actStart('bedMake', null, { title: 'Your bunk', spot, after: 'You pull the blanket straight and tuck the corners in.' })]])
    .concat(lockerTidy() ? [] : [['Tidy your locker', () => actStart('tidy', null, { title: 'Your locker', spot, after: 'You put your things away.' })]], [['Lie down', () => bunkLie(id)]]);
  if (!deviceChoose({ title: 'Your bunk', text: 'The inspection is at 06:30.', choices: opts.map(o => o[0]) }, i => { if (opts[i]) opts[i][1](); })) bunkLie(id);
}
function bunkSleep(A) {                                  // once you're lying in it at night: sleep (section 13's fade and skip)
  if (A.kind !== 'lie' || A.o.slept || A.phase !== 'do') return;
  if (!A.o.sleep && !bedtime()) return; A.o.sleep = true;   // lay down by day and stayed past 20:00: sleep now (reviewer 1, 0.28.37)
  A.o.slept = true; SHIP.player.bedMade = null; const bed = PLACE_OF.get(A.placeId);   // slept in: unmade (m3)
  if (bed && typeof offerSleep === 'function') offerSleep(cellPos(...bed.at));
}
const PLAYER_TAPS = [];                                  // other sections' taps (15b): f(item, itemPos, tapPoint) -> true if handled
// an item was tapped (section 11): start its activity, or return false to let the tap do what it always did
function playerTap(it, at, point) {
  if (queueHeld()) return true;                          // in the line: ask first (0.28.31)
  if (SHIP.player.tray && /^servery$/i.test(it.t)) { toast(it.t, 'You already have your tray. Find a seat and tap it to eat.'); return true; }
  if (bunkTap(it, at)) return true;                      // a friend's note on your bunk (0.28.25)
  if (cartTap(it, at)) return true;                      // a restock job: the hover cart (below)
  if (jobTap(it, at)) return true;                       // the job loop (below): main storage, or the machine you're working on
  if (PLAYER_TAPS.some(f => f(it, at, point))) return true;   // other sections' taps (15b)
  const chore = own => typeof ixChoreLast === 'function' && ixChoreLast(it, at, own);   // your chore's stop: only things with nothing of their own to do (0.28.55)
  const rule = ACT_TAP.find(r => r[0].test(it.t)); if (!rule) return sitTap(it, at, point) || chore(true) || machineTap(it, at) || chore(false);
  const [, types, kind] = rule;
  const near = [...PLACE_OF.values()].filter(pl => types.includes(pl.type) && !(PRIVATE_TYPES.has(pl.type) && privatePlace(pl)))
    .map(pl => [pl, placeSpot(pl.id)]).filter(([, s]) => s && Math.hypot(s.x - at.x, s.z - at.z) < ACT_NEAR)
    .sort((m, n) => Math.hypot(m[1].x - point.x, m[1].z - point.z) - Math.hypot(n[1].x - point.x, n[1].z - point.z));
  if (!near.length) return chore(false);
  if (kind === 'pay') {                                  // the counter: pay for what you've picked out, standing at it
    if (!basket) return false;
    if (SHIP.player.credits < basket.price) { toast(it.t, basket.name[0].toUpperCase() + basket.name.slice(1) + ' is ' + basket.price + ' credits, and you have ' + SHIP.player.credits + '. Finish a job or two first.'); basket = null; return true; }
    const clerk = heldBy(near[0][0].id);
    approach(at.clone(), it.front, it.depth, () => actStart('pay', null, { title: it.t, after: clerk ? clerk.p.name + ' rings it up.' : 'Nobody\'s on the till, so you scan your badge yourself.' }));
    return true;
  }
  if (kind === 'tray' && !foodFrom('servery', true).ok) { toast(it.t, foodFrom('servery', true).why); return true; }   // a table with no tray just sits you (0.28.45)
  if (kind === 'tray' && typeof galleyJoin === 'function' && typeof galleyTurn === 'function') {   // join the galley's queue at its back
    const j = galleyJoin('player'), ln = j.line && typeof lineSpot === 'function' ? lineAt(lineSpot('player')) : null;   // the back of section 10's line for now (the galley joins you to it), else the galley's spot
    if (j.line && typeof galleyLeave === 'function') galleyLeave('player');   // in the line only once you reach it (0.28.36; actBegin joins again): from across the room you'd hold it up
    actStart('queue', null, { title: it.t, ahead: j.ahead, turnAt: j.turnAt,
      spot: ln || { id: null, walk: j.at, x: j.xy[0] - OX, z: j.xy[1] - OZ, y: 0, face: typeof j.face === 'number' ? j.face * Math.PI / 180 : FACE_ANGLE[j.face] || 0, pose: 'stand' } });   // a number: degrees, as placeSpot (0 south, 90 east)
    return true;
  }
  if (kind === 'grab' && !foodFrom('grab', true).ok) { toast(it.t, foodFrom('grab', true).why); return true; }
  let free = near.find(([pl]) => !heldBy(pl.id)), member = false;
  if (!free && kind === 'gym' && gymClubOn()) {          // Gym club (0.28.62, the 0.60.7 plan): you're a member, so the machine is yours; whoever had it picks another (section 10: nobody keeps the place you're using)
    free = near[0]; const a = heldBy(free[0].id);
    if (a && a.h && typeof bubbleSay === 'function') { let l = null; try { l = typeof lineFor === 'function' && lineFor(a.p.id, 'gym.yield', {}); } catch (e) { l = null; } bubbleSay(a.h, l && l.text || 'All yours. I\'ll take another.'); }
    member = true;
    let mt = null; try { mt = careerText('gym.member'); } catch (e) { mt = null; }
    toast(it.t, mt || 'Gym club: you\'re a member, so this one\'s yours.');
  }
  if (!free && (kind === 'call' || kind === 'shower') && typeof queueJoin === 'function' && queueJoin(kind, near[0][0], it)) return true;   // every booth or shower in use: the line (section 10, 0.71.4)
  if (!free) {
    const a = heldBy(near[0][0].id);
    toast(it.t, (kind === 'tray' ? 'There\'s a queue at the servery. Try again in a minute.' : kind === 'toilet' ? 'Occupied: the little light is red. Try another, or wait a minute.' : 'In use: ' + a.p.name + ' is ' + (kind === 'eat' ? 'sitting there.' : 'on it.')) + ' ' + it.x);
    return true;
  }
  const [pl, spot] = free;
  const crowdPose = typeof poseOf === 'function' ? poseOf(pl) : null;   // section 8b's pose for a place (with A2), as the crew use
  const pose = kind === 'eat' ? spot.pose : kind === 'gym' && !pl.anim && /treadmill/i.test(it.t) ? 'run'
    : crowdPose || (kind === 'gym' ? pl.anim || (pl.pose === 'stand' ? 'lift' : pl.pose) : kind === 'call' ? pl.anim || 'call' : pl.anim || PLAYER_ACTS[kind].pose);
  actStart(kind, pl.id, { pose, title: it.t, flavour: it.x, shelf: kind === 'browse' ? STORE_SHELF(it) : null, member });
  return true;
}
// sit anywhere (0.28.12): a tap on a seat (or anything) with a free place you can sit at within SIT_NEAR m of the tap
// point walks you there and sits you down, in the crowd's sit pose at the seat's height; tap elsewhere or walk to get
// up. The toast still shows the thing's own description. Public seats only (SIT_TYPES: lounges, benches, the mess,
// common rooms, the garden, the music room, events), never anyone's workstation, bed or toilet, nor a place crew hold.
// Sitting rests you (energy drains at SIT_REST) and crew sitting near you are a little company (SIT_GAIN each).
const SIT_NEAR = 1.3, SIT_REST = .6, SIT_GAIN = .1;
const SIT_TYPES = new Set(['lounge-seat', 'mess-seat', 'bench', 'common-room', 'garden', 'music', 'event', 'observatory']);
function sitTap(it, at, point) {
  if (typeof PLACE_OF === 'undefined') return false;
  const near = [...PLACE_OF.values()].filter(pl => SIT_TYPES.has(pl.type) && pl.pose === 'sit' && !privatePlace(pl))
    .map(pl => [pl, placeSpot(pl.id)]).filter(([, sp]) => sp && sp.pose === 'sit' && Math.hypot(sp.x - point.x, sp.z - point.z) < SIT_NEAR)
    .sort((m, n) => Math.hypot(m[1].x - point.x, m[1].z - point.z) - Math.hypot(n[1].x - point.x, n[1].z - point.z));
  if (!near.length) return false;
  const free = near.find(([pl]) => !heldBy(pl.id));
  if (!free) { toast(it.t, it.x + ' ' + heldBy(near[0][0].id).p.name + ' is sitting there.'); return true; }
  actStart('sit', free[0].id, { pose: free[1].pose, title: it.t, after: [it.x, 'You sit down. Tap anywhere to get up.'].filter(Boolean).join(' ') });
  return true;
}
// a tap that reached the floor (0.28.17, the user's treadmills; section 11, one line): things with no description of
// their own aren't tappable (two of the three treadmills, the far mess tables' seats, two store shelves), so the tap
// went through to the floor and you only walked there. If the tap's line of sight passes within FLOOR_NEAR m of a
// usable place's spot at any height up to 1.2 m (the belt, the console, the seat), use that place as a tap on it
// would: the gym, a call-home booth, a store shelf, or a seat to sit on. Else the floor tap walks, as always.
const FLOOR_NEAR = .5;
const FLOOR_ACTS = { gym: pl => pl.anim === 'run' ? 'Treadmill' : pl.anim === 'row' ? 'Rowing machine' : pl.anim === 'cycle' ? 'Exercise bike' : pl.pose === 'lie' ? 'Mats' : 'Weights', callhome: () => 'Booth', shop: () => 'Shelves', toilet: () => 'Toilet' };
function playerFloorTap(point) {
  if (queueHeld()) return true;                          // in the line: ask first (0.28.31)
  if (bagLockerTap(point)) return true;                  // the kit bag into your locker (0.28.26)
  if (typeof beamFloorTap === 'function' && beamFloorTap(point)) return true;   // section 18: by the beam at Name on the beam, paint your name (0.71.3)
  if (typeof crateTap === 'function' && crateTap(point)) return true;   // the crate you set down (Put down, 0.28.60)
  if (typeof clothesFloorTap === 'function' && clothesFloorTap(point)) return true;   // section 21b: your wardrobe, or the hamper you set down (0.42.40)
  if (typeof PLACE_OF === 'undefined' || typeof ray === 'undefined') return false;
  const o = ray.ray.origin, d = ray.ray.direction, hits = [];
  for (const pl of PLACE_OF.values()) {
    const use = FLOOR_ACTS[pl.type] && !(PRIVATE_TYPES.has(pl.type) && privatePlace(pl)) ? 'act' : SIT_TYPES.has(pl.type) && pl.pose === 'sit' && !privatePlace(pl) ? 'sit' : null; if (!use) continue;
    const sp = placeSpot(pl.id); if (!sp) continue;
    let best = Infinity;
    for (let y = 0; y <= 1.2; y += .1) { const k = (y - o.y) / d.y; if (!(k > 0)) continue; best = Math.min(best, Math.hypot(o.x + d.x * k - sp.x, o.z + d.z * k - sp.z)); }
    if (best < FLOOR_NEAR) hits.push([best, pl, sp, use]);
  }
  const job = jobHere(point, true);                      // the floor at your job's stop (0.28.52, the user's lamp), unless a usable place is nearer the tap
  if (job && (!hits.length || job.by <= hits.reduce((m, h) => Math.min(m, h[0]), Infinity))) return !!job.go();
  if (!hits.length) return false;
  const [, pl, sp, use] = hits.sort((a, b) => a[0] - b[0])[0], at = new THREE.Vector3(sp.x, 0, sp.z);
  if (use === 'sit') return sitTap({ t: 'Seat', x: '' }, at, at);
  return playerTap({ t: FLOOR_ACTS[pl.type](pl), x: '', front: 0, depth: 0 }, at, at);
}
// crew near you (0.28.12, for sitting): settled at a place you'd sit at, within COMPANY_NEAR m
const sitCompany = A => !A || !A.spot || typeof DECK_CREW === 'undefined' ? 0   // 0.28.43: each by the bond (bondMult)
  : bondSum(DECK_CREW.filter(a => a.settled && a.spot && a.spot.pose === 'sit' && Math.hypot(a.x - A.spot.x, a.z - A.spot.z) < COMPANY_NEAR).map(crewId), COMPANY_CAP);
// a machine (0.28.11): the nearest of this deck's machines within MACHINE_NEAR m of the thing tapped. Section 17's
// machineUse(id, 'player') says what the tap does ({ text, ran }: a line about it, and whether it started it). You
// walk up to it first. Without machineUse, or no machine there, the tap does what it always did.
const MACHINE_NEAR = 1.2;
function machineTap(it, at) {
  if (typeof machineUse !== 'function' || typeof machineList !== 'function' || typeof deckDef === 'undefined') return false;
  const m = machineList().filter(m => m.deck === deckDef.num && !m.stub && m.at).map(m => [m, cellPos(...m.at)])
    .filter(([, c]) => Math.hypot(c.x - at.x, c.z - at.z) < MACHINE_NEAR).sort((a, b) => Math.hypot(a[1].x - at.x, a[1].z - at.z) - Math.hypot(b[1].x - at.x, b[1].z - at.z))[0]
    || stubTap(it, at);
  if (!m) return false;
  approach(at.clone(), it.front, it.depth, () => {
    let r = null; try { r = machineUse(m[0].id, 'player'); } catch (e) { r = null; }
    toast(it.t, r && r.text ? r.text : it.x);
    if (r && r.ran && /wash/i.test(m[0].kind)) simAct('laundry');   // the note bus (0.28.22)
  });
  return true;
}
// a stub machine (0.28.14): one section 17 knows only by its room (the washers), so no tile to be near. Matched by
// the thing you tapped instead: in the stub's room, titled with its kind's name, and with its number if the title
// has one ('Washer 3' -> 4-washer-3)
function stubTap(it, at) {
  const rm = roomAt(...cellAt(at.x, at.z)), num = (it.t.match(/\d+/) || [])[0];
  const m = machineList().find(m => m.stub && m.deck === deckDef.num && m.room && m.room === rm && MACHINE_KINDS[m.kind]
    && it.t.toLowerCase().startsWith(MACHINE_KINDS[m.kind].name.toLowerCase()) && (!num || m.id.endsWith('-' + num)));
  return m ? [m, null] : null;
}
// head for a place (or, with no place, do it where you stand) and do the activity there
function actStart(kind, placeId, o = {}) {
  if (SHIP.player.tray && (kind === 'eat' || kind === 'sit') && placeId && (PLACE_OF.get(placeId) || {}).type === 'mess-seat') {   // your tray: eat it at the seat you chose (0.28.31)
    kind = 'eat'; o = { ...o, title: 'Mess hall', fed: true, dish: SHIP.player.tray, pose: (placeSpot(placeId) || {}).pose || o.pose };
  }
  if (kind === 'eat' && !o.fed) {                        // no tray, no meal (0.28.45, the user's: "no auto tray: you must get it from the line"): you just sit
    kind = 'sit'; o = { ...o, after: [o.flavour, 'You sit down. To eat, queue at the servery for a tray, then bring it to a seat.'].filter(Boolean).join(' ') };
  }
  actEnd(true);
  const spot = placeId ? placeSpot(placeId) : o.spot || null, here = player.here();
  ACT = { kind, def: { ...PLAYER_ACTS[kind] }, placeId, spot, o, deck: deckDef, phase: 'walk', done: 0, cb: null };
  if (!spot) { actBegin(); return; }
  ACT.cb = () => actBegin();
  if (K(spot.walk) === K(here) && !player.path.length) { player.stop(); actBegin(); return; }
  if (!playerGo(spot.walk, ACT.cb)) {
    if (typeof crewMakeWay === 'function') { ACT.release = crewMakeWay(spot.walk); ACT.phase = 'wait'; ACT.waitT = 0; ACT.tried = 0; return; }   // someone on that tile (a cook at a range's panel): they step aside (sim 0.26.36; 0.28.40)
    ACT = null; toast(o.title || PLAYER_ACTS[kind].title, 'You can\'t get there just now: someone\'s in the way.');
  }
}
function actBegin() {
  const A = ACT; if (!A) return;
  const pl = A.placeId && PLACE_OF.get(A.placeId), who = pl && !A.o.member && heldBy(pl.id);   // a Gym club member's machine is theirs (0.28.62)
  if (who) {                                             // someone got there first: the next free one of its kind nearby, if any
    const alt = [...PLACE_OF.values()].filter(q => q.type === pl.type && q.id !== pl.id && !heldBy(q.id) && !(PRIVATE_TYPES.has(q.type) && privatePlace(q)))
      .map(q => [q, placeSpot(q.id)]).filter(([, s]) => s && Math.hypot(s.x - A.spot.x, s.z - A.spot.z) < ACT_NEAR)
      .sort((m, n) => Math.hypot(m[1].x - A.spot.x, m[1].z - A.spot.z) - Math.hypot(n[1].x - A.spot.x, n[1].z - A.spot.z))[0];
    if (alt && !A.o.moved) { actStart(A.kind, alt[0].id, { ...A.o, moved: true, pose: A.kind === 'eat' ? alt[1].pose : A.o.pose }); return; }
    ACT = null; toast(A.o.title, 'In use: ' + who.p.name + ' got there first.'); return;
  }
  if (A.kind === 'tray' || A.kind === 'grab') {          // take the food now (an 'eat' is always a served tray since 0.28.45)
    const f = foodFrom(A.kind === 'grab' ? 'grab' : 'servery');
    if (!f.ok) { ACT = null; toast(A.o.title, f.why); return; }
    A.o.dish = f.dish;
  }
  if (A.kind === 'queue') { const j = galleyJoin('player'); A.o.ahead = j.ahead; A.o.turnAt = j.turnAt;   // your place in line from when you reach it
    const ln = typeof lineSpot === 'function' && lineAt(lineSpot('player')); if (ln) A.spot = ln; }   // the back of the real line now (0.28.36; section 16 owns who's in it, 15 only reads the spot)
  if (A.kind === 'eat' && A.o.fed) SHIP.player.tray = null;   // sat down with your tray (0.28.31)
  if (A.kind === 'job' && !jobBegin(A)) return;          // at the machine: fit parts, then inspect or repair (the job loop, below)
  if ((A.kind === 'ixTea' || A.kind === 'ixLounge') && teaHere(A)) teaBegin(A);   // 13:00 in the Tea corner: tea and biscuits (playtest 1)
  if (A.def.need && NEED_GOAL && NEED_GOAL.need === A.def.need) needGoalClear();   // on your way to fixing it: the marker's done its job
  if (A.kind === 'sit' || A.kind === 'eat') sitBump(A);   // sitting down near people: a little social (playtest 1)
  const p = player.obj.position, s = A.spot || { x: p.x, z: p.z, y: 0, face: player.face };
  A.body = new FullPerson(PLAYER_SPEC, 'you'); A.x = p.x; A.z = p.z; A.y = 0; A.face = player.face;
  A.to = s; A.pose = A.o.pose || A.def.pose || 'stand'; A.phase = 'in';
  A.body.set({ x: A.x, y: 0, z: A.z }, A.face, 'stand'); player.obj.visible = false;
  const what = A.kind === 'queue' ? 'You join the queue.' :   // no count (0.28.30, the user's: you see the people ahead of you)
    A.kind === 'tray' ? 'You take a tray: ' + A.o.dish + '.' : A.kind === 'eat' ? (A.spot ? 'You sit down to ' : 'You eat ') + A.o.dish + '.'
    : A.kind === 'grab' ? 'You take ' + A.o.dish + '.' : A.o.after || '';
  toast(A.o.title || A.def.title, [A.o.flavour && A.kind !== 'eat' && A.kind !== 'tray' ? A.o.flavour : '', what, A.def.need ? 'About ' + taskMins(A.def.mins) + ' minutes; walk away to stop.' : ''].filter(Boolean).join(' '));
  if (A.kind === 'call' && typeof homeBooth === 'function') homeBooth();   // social B2's call picker at a booth (0.28.30)
}
// stop: abort (walked away, a time skip, a new deck) leaves at once; otherwise step back out first (actUpdate)
function actEnd(abort) {
  const A = ACT; if (!A) return; ACT = null; trayOnTable(null);
  if (A.release) try { A.release(); } catch (e) { /* theirs */ }   // whoever stepped aside for you goes back (crewMakeWay, 0.28.40)
  if (A.kind === 'queue' && !A.o.dish && typeof galleyLeave === 'function') try { galleyLeave('player'); } catch (e) { /* not ours to mend */ }   // out of the galley's queue and the real line (galley 0.29.32; the owner's ruling: only section 16 joins or leaves you)
  if (A.body) { A.body.dispose(); player.obj.visible = true; }
  if (A.o.cost) for (const k in A.o.cost) if (A.o.cost[k] >= .5) needFloat('\u2212' + Math.round(A.o.cost[k]) + ' ' + NEED_LABEL[k], k, -A.o.cost[k]);   // what it cost, like a gain's note: the toilet's "−3 Hygiene" (playtest 2, 0.73.0)
  if ((A.phase === 'do' || A.phase === 'out') && A.done > 0) {   // the note bus (0.28.22): done, or walked away part way
    const act = { shower: 'wash', eat: 'eat', grab: 'eat', call: 'call' }[A.kind];
    if (A.kind === 'call' && A.done >= A.def.mins) leisureAdd(5, 'call');   // a whole call home: +5 leisure (0.28.64)
    if (A.kind === 'ixGarden' && A.done >= A.def.mins && typeof hobbyCount === 'function') hobbyCount('garden');   // tending a bed is a hobby (0.28.65)
    if (act) simAct(act, act === 'eat' ? { with: A.o.company || 0 } : {});
  }
  if (A.kind === 'workStep') workStepEnd(A, abort);       // a work step (Pillar 5): a look's marks, or a pause
  if (abort) return;
  if (A.kind === 'bedMake' && A.done >= A.def.mins) { SHIP.player.bedMade = SHIP.time.day; toast('Your bunk', 'Bed made, corners and all.'); }   // the inspection's berth (m3)
  if (A.kind === 'tidy' && A.done >= A.def.mins) { SHIP.player.untidy = false; toast('Your locker', 'All put away. Tidy.'); }
  if (typeof A.def.onDone === 'function' && A.done >= A.def.mins) try { A.def.onDone(A); } catch (e) { console.error(e); }   // a sub-block's own timed hold (24m's bench, 0.45.11)
  player.face = player.obj.rotation.y = A.face;
  if (A.def.done) toast(A.def.title, A.def.done + (A.kind === 'eat' && A.o.company ? ' Good company, too.' : '') + (A.def.need ? ' ' + NEED_LABEL[A.def.need] + ' ' + Math.round(SHIP.player.needs[A.def.need]) + '.' : ''));
  if (A.kind === 'browse') {
    basket = storePick(A.o.shelf || 'snack');
    toast(A.def.title, 'You pick out ' + basket.name + ' (' + basket.price + ' credits; you have ' + SHIP.player.credits + '). Pay at the counter.');
  }
  if (A.kind === 'pay' && basket && SHIP.player.credits < basket.price) { toast('Counter', basket.name[0].toUpperCase() + basket.name.slice(1) + ' is ' + basket.price + ' credits, and you have ' + SHIP.player.credits + '.'); basket = null; return; }   // checked again at the till (0.28.39)
  if (A.kind === 'pay' && basket) {
    const b = basket, P = SHIP.player; P.credits -= b.price; P.bought = (P.bought || 0) + 1; P.untidy = true; simAct('buy', { item: b.name });   // untidy: out until you tidy your locker (m3)
    if (b.gift && typeof giftAdd === 'function' && giftAdd(b.gift)) {   // a gift: into your hands (0.28.25)
      toast('Paid', 'You pay ' + b.price + ' credits for ' + b.name + '. You keep it in your hands to give to someone. ' + P.credits + ' credits left.'); basket = null; return;
    }
    if (b.kind === 'hobby') {                          // a hobby's supplies (0.28.63): yours for good
      hobbyGive(b.hobby); toast('Paid', 'You pay ' + b.price + ' credits for ' + b.name + '. Sit down anywhere and tap Hobby for some ' + HOBBIES[b.hobby].name.toLowerCase() + '. ' + P.credits + ' credits left.'); basket = null; return;
    }
    if (b.kind === 'comfort') { P.locker.push(b.name); while (P.locker.length > LOCKER_MAX) P.locker.shift(); P.needs.social = needClamp(P.needs.social + b.gain); }   // a full locker: the oldest goes home, never the new one (0.28.39)
    else P.needs.hunger = needClamp(P.needs.hunger + b.gain);
    toast('Paid', 'You pay ' + b.price + ' credits for ' + b.name + (b.kind === 'comfort' ? '. It goes in your locker; it\'s nice to have something of your own.' : ' and have it on the way out.')
      + ' ' + P.credits + ' credits left.');
  }
  if (A.kind === 'fetch' || A.kind === 'job' || A.kind === 'stow' || A.kind === 'make') jobEnd(A);
  if (A.kind.startsWith('cart')) cartEnd(A);
  if (A.kind === 'craft') {                              // the gift you made (0.28.25)
    const P = SHIP.player; if (P.carry.length < CARRY_MAX && (!A.o.needs || typeof SHIP.stores[A.o.needs] !== 'number' || takePart(A.o.needs)) && giftAdd(A.o.gift)) { P.crafted = (P.crafted || 0) + 1; P.untidy = true; toast('Machine shop', 'You make ' + partList([A.o.gift]) + '. It\'s in your hands: give it to someone.'); }
  }
  if (A.kind === 'pay') basket = null;
  if (A.kind === 'queue' && !A.o.dish) { toast('Servery', A.o.why || 'Nothing to eat just now.'); return; }
  if (A.kind === 'queue') { SHIP.player.tray = dishName(A.o.dish); toast('Servery', 'Your turn. You take a tray: ' + SHIP.player.tray + '. Find a seat and tap it to eat.'); return; }   // 0.28.31: control back, tray in hand
  if (A.kind === 'tray') {                               // tray in hand: the nearest free mess seat
    const seat = [...PLACE_OF.values()].filter(pl => pl.type === 'mess-seat' && !heldBy(pl.id)).map(pl => [pl, placeSpot(pl.id)])
      .filter(([, s]) => s).sort((m, n) => Math.hypot(m[1].x - A.x, m[1].z - A.z) - Math.hypot(n[1].x - A.x, n[1].z - A.z))[0];
    const o = { title: 'Mess hall', fed: true, dish: A.o.dish };
    if (seat) actStart('eat', seat[0].id, { ...o, pose: seat[1].pose });
    else { actStart('eat', null, o); toast('Mess hall', 'Every seat\'s taken, so you eat standing up.'); }
  }
}
// the food line (0.28.31, the user's "you move with the line until it's your turn and get control back"): while you
// queue, a tap or a drag doesn't walk you off; it asks "Leave the queue?" (Leave / Stay). Served, you hold your tray
// (SHIP.player.tray, the dish; not saved) and choose a mess seat yourself: tap it and you sit and eat.
const queueHeld = () => !!(ACT && ACT.kind === 'queue' && ACT.phase !== 'walk' && ACT.phase !== 'out') && (queueAsk(), true);
SHIP.player.tray = null;
function queueAsk() {
  let el = document.getElementById('qAsk');
  if (!el) {
    const st = document.createElement('style');
    st.textContent = '#qAsk{position:fixed;left:50%;bottom:18px;transform:translateX(-50%);z-index:5;display:flex;align-items:center;gap:10px;padding:10px 12px 10px 16px;border-radius:14px;background:var(--glass);border:1px solid var(--line);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px)}#qAsk[hidden]{display:none}#qAsk span{flex:1;white-space:nowrap}';
    document.head.appendChild(st);
    el = document.createElement('div'); el.id = 'qAsk'; el.setAttribute('role', 'dialog');
    el.innerHTML = '<span>Leave the queue?</span><button id="qLeave">Leave</button><button id="qStay">Stay</button>';
    document.body.appendChild(el);
    document.getElementById('qLeave').onclick = () => { el.hidden = true; queueLeave(); };
    document.getElementById('qStay').onclick = () => { el.hidden = true; };
  }
  if (typeof toastEl !== 'undefined') toastEl.classList.remove('show');
  el.hidden = false;
}
const lineAt = sp => sp && isFinite(sp.x) && isFinite(sp.z) ? { id: null, walk: sp.at, x: sp.x, z: sp.z, y: 0, face: isFinite(sp.face) ? sp.face : 0, pose: 'stand' } : null;   // lineSpot -> a spot
function queueLeave() {
  if (!ACT || ACT.kind !== 'queue') return;
  actEnd(true); toast('Servery', 'You step out of the line.');   // actEnd calls galleyLeave
}
// social comes from people, scaled by the bond (0.28.43, the user's "that last part is always true"): bondMult(id) is
// how much one person's company or chat counts, by your tier with them (section 20's relTier: stranger, acquaintance,
// colleague, friend, close friend). A close friend is worth three strangers. Without section 20 everyone counts 1.
// bondSum(ids, cap): the people together, at most cap; bondBest(ids): the best of them (0 for nobody).
const BOND_MULT = [1, 1.2, 1.5, 2, 3];
function bondMult(id) {
  let t = 0; try { t = typeof relTier === 'function' && id ? relTier(id) || 0 : 0; } catch (e) { t = 0; }
  return BOND_MULT[Math.max(0, Math.min(BOND_MULT.length - 1, t | 0))];
}
const bondSum = (ids, cap = Infinity) => Math.min(cap, ids.reduce((a, id) => a + bondMult(id), 0));
const bondBest = ids => ids.reduce((a, id) => Math.max(a, bondMult(id)), 0);
const crewId = a => (a.p || a).id;
// tables (0.28.43): mess seats close together (TABLE_LINK m, seat to seat) make one table: the long tables seat eight, the
// round ones four. seatTable(placeId) -> the first seat id of its table, or null; made once a deck, from the places.
const TABLE_LINK = 1.3, TABLES = new Map();
function seatTable(id) {
  const pl = PLACE_OF.get(id); if (!pl || pl.type !== 'mess-seat') return null;
  const dk = id.split('-')[0]; if (!TABLES.has(dk)) {
    const seats = [...PLACE_OF.values()].filter(q => q.type === 'mess-seat' && q.id.split('-')[0] === dk && q.xy), m = new Map();
    for (const q of seats) if (!m.has(q.id)) {             // single linkage: everything within TABLE_LINK of the table so far
      const todo = [q]; m.set(q.id, q.id);
      while (todo.length) { const a = todo.pop(); for (const b of seats) if (!m.has(b.id) && Math.hypot(a.xy[0] - b.xy[0], a.xy[1] - b.xy[1]) < TABLE_LINK) { m.set(b.id, q.id); todo.push(b); } }
    }
    TABLES.set(dk, m);
  }
  return TABLES.get(dk).get(id) || null;
}
// company at a meal (0.28.10; your table only, 0.28.43, the user's "you should only get social at a meal if people are
// sitting next to you", then "anyone at YOUR table"): crew settled at the other seats of your table, nobody at other
// tables. COMPANY_GAIN social a minute for each, times their bondMult, the lot at most COMPANY_CAP (two close friends).
// A 20-minute meal with three strangers at your table: about +12 (times needEffects' socialGain); an empty table, nothing.
const COMPANY_CAP = 6, COMPANY_GAIN = .2, COMPANY_NEAR = 3;   // COMPANY_NEAR: sitting elsewhere (sitCompany), not meals
function tableCrew(A) {
  if (!A || !A.placeId || typeof DECK_CREW === 'undefined') return [];
  const tb = seatTable(A.placeId); if (!tb) return [];
  return DECK_CREW.filter(a => a.settled && a.goalId && a.goalId !== A.placeId && seatTable(a.goalId) === tb).map(crewId);
}
const company = A => bondSum(tableCrew(A), COMPANY_CAP);
// chatting (0.28.10): a tap on a crew member (section 10) calls playerChat(person). The first chat with someone each
// ship day gives CHAT_GAIN social, later ones CHAT_AGAIN; times needEffects' socialGain (clean: more, unwashed: half).
// It adds a line to the tap's toast.
const CHAT_GAIN = 6, CHAT_AGAIN = 1;
function playerChat(p) {
  if (!p) return 0;
  const P = SHIP.player, key = String(p.id || p.name), fx = needEffects(), first = P.chats[key] !== SHIP.time.day;
  const gain = (first ? CHAT_GAIN : CHAT_AGAIN) * fx.socialGain * bondMult(p.id);   // by the bond (0.28.43)
  P.chats[key] = SHIP.time.day;
  for (const k in P.chats) if (P.chats[k] < SHIP.time.day - 1) delete P.chats[k];   // only today's (and yesterday's) are kept
  P.needs.social = needClamp(P.needs.social + gain);
  const tx = document.getElementById('tx'), first1 = (p.name || '').split(' ')[0];
  if (tx) tx.textContent += first ? ' You chat for a minute.' + (P.needs.hygiene < NEED_LOW ? ' ' + first1 + ' wrinkles their nose a little.' : '') : ' You say hello again.';
  device.refresh();
  return gain;
}
// your tray (0.28.15, the user's note): like the crew, you carry a tray from the servery (or the queue) to your mess
// seat ('+tray', section 8b's prop: Walker.update, then the stand-in sliding in); seated, it sits on the table in
// front of you while you eat (one small mesh made at load in the mess's own tray colours, shown only then); when
// you're done it's cleared away (0.60.7: no tray return). The grab shelf has no tray.
const TRAY_ON = (() => {
  const g = new THREE.Group(); box(.42, .02, .3, MESS.trays[0], 0, 0, 0, g); cyl(.09, .09, .016, MESS.white, -.06, .018, .02, g, 16);
  cyl(.035, .03, .08, MESS.white, .13, .05, -.07, g, 10); g.visible = false; scene.add(g); return g;
})();
const TRAY_REACH = .42;                                  // from your seat's spot toward the table (the long tables' benches and the round tables' chairs)
function trayOnTable(A) {
  if (!A) { TRAY_ON.visible = false; return; }
  const f = A.to.face || 0; TRAY_ON.position.set(A.to.x + Math.sin(f) * TRAY_REACH, .78, A.to.z + Math.cos(f) * TRAY_REACH);
  TRAY_ON.rotation.y = f; TRAY_ON.visible = true;
}
// once a frame: the walk there, sliding into the place, the time it takes, and stepping back out
function actUpdate(dt, t) {
  const A = ACT;
  if (A.deck !== deckDef) { actEnd(true); return; }
  if (A.phase === 'wait') {                              // waiting for them to step aside: try the walk every half second, for 8 at most
    if (player.path.length || player.steer) { actEnd(true); return; }
    A.waitT += dt; if (A.waitT - A.tried < .5) return; A.tried = A.waitT;
    if (playerGo(A.spot.walk, A.cb)) A.phase = 'walk';
    else if (A.waitT > 8) { actEnd(true); toast(A.o.title || A.def.title, 'You can\'t get there just now: someone\'s in the way.'); }
    return;
  }
  if (A.phase === 'walk') { if (player.onArrive !== A.cb) { if (A.release) A.release(); ACT = null; } return; }   // you went somewhere else
  if ((player.path.length || player.steer) && A.kind === 'queue' && A.phase !== 'out') { player.stop(); if (typeof endSteer === 'function') endSteer(); queueAsk(); }   // the line holds you (0.28.31)
  else if (player.path.length || player.steer) { actEnd(true); return; }          // walked away: stop
  const go = (x, z) => {                                 // glide toward x, z; true when there
    const dx = x - A.x, dz = z - A.z, d = Math.hypot(dx, dz), st = CREW_SPEED * .8 * dt;
    if (d <= st) { A.x = x; A.z = z; return true; }
    A.x += dx / d * st; A.z += dz / d * st; A.face = Math.atan2(dx, dz); return false;
  };
  let pose = A.pose;
  if (A.phase === 'in') {
    if (A.kind === 'queue' && typeof lineSpot === 'function') { const ln = lineAt(lineSpot('player')); if (ln) A.to = ln; player.obj.position.set(A.x, 0, A.z); }   // to the line's back as it is now, the camera with you (0.28.36)
    if (go(A.to.x, A.to.z)) { A.phase = 'do'; A.face = A.to.face; A.y = A.to.y || 0; } else pose = A.kind === 'eat' && A.o.fed ? 'walk+tray' : 'walk';
  } else if (A.phase === 'do') {
    if (A.kind === 'queue' && typeof lineSpot === 'function') {   // the line moves: walk up with it, a tile at a time (0.28.34)
      const ln = lineAt(lineSpot('player'));
      if (ln && !go(ln.x, ln.z)) pose = 'walk'; else if (ln) A.face = ln.face;
      if (ln) player.obj.position.set(A.x, 0, A.z);       // you are where your stand-in is (the camera follows; no walk back after)
    }
    if (A.o.move && typeof recMoveStep === 'function') pose = recMoveStep(A, dt, t) || pose;   // a rec deck move (0.81.x, 8c): swim, paddle, climb, float
    if (A.o.move ? A.mv && A.mv.done : A.def.until ? A.def.until(A) : A.done >= A.def.mins) { A.phase = 'out'; A.y = 0; }
    bunkSleep(A);                                        // lying down at night: to sleep (0.28.29)
  }
  if (A.phase === 'out') {
    const p = player.obj.position;
    if (go(p.x, p.z)) { actEnd(false); return; }
    pose = 'walk';
  }
  trayOnTable(A.kind === 'eat' && A.phase === 'do' && A.spot && A.spot.pose === 'sit' ? A : null);
  A.body.set({ x: A.x, y: A.y, z: A.z }, A.face, pose);
  A.body.update(dt, t);
}
// ---- you can see it working (0.28.20, the user's): when a need rises, a small "+25 Food" note floats up from your
// character and the device button gives a soft pulse. Read off the needs themselves once a frame (needsSeen), so
// every gain shows, whichever section made it (meals, showers, the toilet, sleep, chats, company, the store, 15b's
// and 20's): rises add up per need and show once they stop for FLOAT_WAIT real seconds, or every FLOAT_EVERY
// seconds while they go on (a toilet visit or the grab shelf shows one note; a long meal a few).
// Drains never show. needPulse(k) is true for PULSE_SECS after need k showed a rise (for the device's Needs bars).
// DOM and CSS made here, so the HTML stays as it was; nothing calls R(). ----
const FLOAT_EVERY = 5, FLOAT_WAIT = .6, FLOAT_MIN = 1, FLOAT_SECS = 1.8, PULSE_SECS = 1.5;
let NEED_SEEN = null, FLOAT_LIVE = 0, PULSE_AT = -1e9;
const FLOATS = [];                                       // live notes [el, born]: faded by the frame clock (0.28.23), so tests see the same thing every run
const FLOAT_LOG = [];                                    // the last notes shown (player_check reads it: notes come and go on real-time timers)
const NEED_RISE = {}, NEED_PULSE = {}, floatV = new THREE.Vector3();
const needPulse = k => (NEED_PULSE[k] || 0) > performance.now();
function needFxLayer() {
  let el = document.getElementById('needFx'); if (el) return el;
  const st = document.createElement('style');
  st.textContent = '#needFx{position:fixed;left:0;top:0;width:0;height:0;z-index:2;pointer-events:none}'
    + '#needFx .nf{position:absolute;transform:translate(-50%,-100%);white-space:nowrap;font-size:12.5px;font-weight:600;color:#bdeee6;padding:2px 9px;border-radius:999px;background:var(--glass);border:1px solid var(--line);text-shadow:0 1px 6px rgba(0,0,0,.5);opacity:0}'
    ;
  document.head.appendChild(st);
  el = document.createElement('div'); el.id = 'needFx'; el.setAttribute('aria-live', 'polite'); document.body.appendChild(el);
  return el;
}
function needFloat(text, k, v) {                         // one note over your head (the stand-in's while you're at a place)
  if (k && NEED_COL[k]) { stripRise(k, v); FLOAT_LOG.push(text); if (FLOAT_LOG.length > 20) FLOAT_LOG.shift(); PULSE_AT = performance.now(); return; }   // 0.28.32: beside its icon in the strip
  if (typeof camera === 'undefined' || typeof player === 'undefined') return;
  const A = ACT && ACT.body && ACT.phase !== 'walk' ? ACT : null, p = player.obj.position;
  floatV.set(A ? A.x : p.x, (A ? A.y : 0) + 2, A ? A.z : p.z).project(camera);
  const x = Math.max(60, Math.min(innerWidth - 60, (floatV.x + 1) * innerWidth / 2)), y = Math.max(40, (1 - floatV.y) * innerHeight / 2 - FLOAT_LIVE * 24 - (actProgress() ? 40 : 0));   // above the progress bar (0.28.21)
  const n = document.createElement('div'); n.className = 'nf'; n.textContent = text; n.style.left = x.toFixed(1) + 'px'; n.style.top = y.toFixed(1) + 'px';
  needFxLayer().appendChild(n); FLOAT_LIVE++; FLOAT_LOG.push(text); if (FLOAT_LOG.length > 20) FLOAT_LOG.shift();
  FLOATS.push([n, performance.now()]); PULSE_AT = performance.now();
}
// each frame (0.28.23): notes rise and fade, and the device button's glow, by performance.now() (the frame clock; a
// virtual one in the tests) instead of CSS animations and real-time timers, which made screenshots differ run to run
const PULSE_SECS_BTN = .9;
function floatsTick() {
  const now = performance.now(), still = typeof matchMedia === 'function' && matchMedia('(prefers-reduced-motion: reduce)').matches;
  for (let i = FLOATS.length - 1; i >= 0; i--) {
    const [n, born] = FLOATS[i], f = (now - born) / (FLOAT_SECS * 1000);
    if (f >= 1) { n.remove(); FLOATS.splice(i, 1); FLOAT_LIVE = Math.max(0, FLOAT_LIVE - 1); continue; }
    n.style.opacity = (f < .15 ? f / .15 : f > .7 ? (1 - f) / .3 : 1).toFixed(3);
    n.style.marginTop = still ? '0px' : (6 - 40 * (1 - (1 - f) * (1 - f))).toFixed(1) + 'px';   // ease-out, 6 px down to 34 up
  }
  deviceLockLook(); stripTick(now, still);
  const b = document.getElementById('devBtn'), g = (now - PULSE_AT) / (PULSE_SECS_BTN * 1000);
  if (b && (g < 1 || b.style.boxShadow)) b.style.boxShadow = g < 1 && !still && !DEV_LOCK_SHOWN ? '0 0 0 ' + (12 * g).toFixed(1) + 'px rgba(76,195,181,' + (.7 * (1 - g)).toFixed(3) + ')' : '';
}
// the device lock (0.28.26, Pillar 4): until it's handed over in your bunk (section 21's flag 'intro.device'), the button
// reads "No device yet", is dimmed and doesn't open: a capture listener here stops section 19's onclick and says why.
// Section 19 may ask deviceLocked() too, for the other ways in (its screen is theirs).
const deviceLocked = () => typeof introOn === 'function' && introOn() && typeof introFlag === 'function' && !introFlag('intro.device');
const deviceLockedTap = () => toast('No device yet', 'Torres hands you your device at your bunk, Bunk 1 on Deck 4.');
let DEV_LOCK_SHOWN = false;
function deviceLockLook() {
  const b = document.getElementById('devBtn'), on = deviceLocked(); if (!b || on === DEV_LOCK_SHOWN) return;
  DEV_LOCK_SHOWN = on; const s = b.querySelector('span'); if (s) s.textContent = on ? 'No device yet' : 'Device';
  b.style.opacity = on ? '.6' : ''; b.setAttribute('aria-label', on ? 'No device yet' : 'Your device: the time and your needs');
}
{ const b = document.getElementById('devBtn'); if (b) b.addEventListener('click', e => { if (deviceLocked()) { e.stopImmediatePropagation(); deviceLockedTap(); } }, true); }
// the needs strip (0.28.32, the user's "needs should be cleanly displayed", approved design): under the Device button,
// six small icons, each with a short bar in its own colour (NEED_COL, through col()); a bar turns amber and pulses
// gently under NEED_LOW. A rise shows as "+N" beside its icon (rises close together merge) instead of a note over your
// head. Tap the strip for names and numbers. DOM only (no draw calls), a fixed size; pulses and fades run on the frame
// clock in floatsTick, like the notes (0.28.23).
const RISE_SECS = 2.2;                                   // NEED_LOW (25) is the needs' own line, above
const cssCol = h => '#' + col(h).convertLinearToSRGB().getHexString();
const NEED_COL = { hunger: cssCol('#f07f6e'), energy: cssCol('#e9d36b'), hygiene: cssCol('#6cc4e4'), fitness: cssCol('#79d08a'), social: cssCol('#c69be6'), bathroom: cssCol('#9bb7cc'), leisure: cssCol('#f2a6c8') };
const NEED_AMBER = cssCol('#ff9a3c');
const NEED_ICON = {                                       // 24-unit stroke icons: fork and knife, bolt, droplet, dumbbell, two people, door
  hunger: 'M7 3v7M5 3v4a2 2 0 0 0 4 0V3M7 10v11M17 3c-2 1-3 4-3 8h3v10', energy: 'M13 2 5 13h6l-1 9 8-12h-6z',
  hygiene: 'M12 3s6 7 6 11a6 6 0 0 1-12 0c0-4 6-11 6-11z', fitness: 'M3 10v4M6.5 7v10M17.5 7v10M21 10v4M6.5 12h11',
  social: 'M9 11a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM3 20c0-3 3-5 6-5s6 2 6 5M16 5.5a2.5 2.5 0 0 1 0 5M17 15c2.5.3 4 2.2 4 5', bathroom: 'M7 3h5v7H7zM5 10h12a5 5 0 0 1-5 5H9l-1 6h7',   // a toilet (0.28.62; a door before)
  leisure: 'M12 3l2.4 5.2 5.6.6-4.2 3.8 1.2 5.6L12 15.4 7 18.2l1.2-5.6L4 8.8l5.6-.6z' };   // leisure (0.28.61): a star
const RISES = {};                                         // need -> { v, at }: the "+N" showing beside its icon
// folding it away (0.28.33, the user's "you should be able to collapse the needs window"): the little chevron at its end
// folds the strip (and its names panel) to one heart icon, amber while any need is low; a tap on that opens it again.
// Saved as save.player.stripFold.
const STRIP_HEART = 'M12 20s-7-4.5-7-10a4 4 0 0 1 7-2.5A4 4 0 0 1 19 10c0 5.5-7 10-7 10z';
SHIP.player.stripFold = !!(SAVED && SAVED.player && SAVED.player.stripFold === true);
SAVE_EXTRA.push(s => { (s.player || (s.player = {})).stripFold = !!SHIP.player.stripFold; });
SHIP.player.alarm = SAVED && SAVED.player && alarmOk(SAVED.player.alarm) ? SAVED.player.alarm : WAKE_AT;   // section 13's alarm clock (0.73.0), kept here where SHIP.player is
SAVE_EXTRA.push(s => { (s.player || (s.player = {})).alarm = SHIP.player.alarm; });
function stripFold(on) { SHIP.player.stripFold = !!on; const el = needStrip(); el.classList.toggle('fold', !!on); if (on) el.classList.remove('open'); el.setAttribute('aria-label', on ? 'Your needs (folded): tap to show' : 'Your needs: tap for names and numbers'); STRIP_SIG = ''; }
let STRIP_SIG = '', STRIP_G = '';
function needStrip() {
  let el = document.getElementById('needStrip'); if (el) return el;
  const st = document.createElement('style');
  st.textContent = '#needStrip{position:fixed;left:14px;top:124px;z-index:2;display:flex;gap:7px;padding:6px 9px;border-radius:12px;background:var(--glass);border:1px solid var(--line);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);cursor:pointer;touch-action:manipulation}'
    + '#needStrip .ns{position:relative;display:flex;flex-direction:column;align-items:center;width:22px}'
    + '#needStrip svg{width:15px;height:15px;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}'
    + '#needStrip i{display:block;width:20px;height:3px;margin-top:4px;border-radius:2px;background:rgba(255,255,255,.14);overflow:hidden}'
    + '#needStrip i b{display:block;height:100%;width:100%;background:currentColor;transform-origin:left center}'
    + '#needStrip em{position:absolute;left:15px;top:-9px;font-style:normal;font-size:10.5px;font-weight:700;line-height:14px;padding:0 4px;border-radius:7px;background:rgba(12,20,30,.85);opacity:0;pointer-events:none;white-space:nowrap}'
    + '#needStrip span,#needStrip u{display:none;text-decoration:none}'
    + '#needStrip.open{flex-direction:column;gap:5px}#needStrip.open .ns{flex-direction:row;width:auto;gap:7px}'
    + '#needStrip.open i{width:70px;margin:0}#needStrip.open span{display:block;width:62px;font-size:12px;color:var(--ink)}'
    + '#needStrip.open u{display:block;width:22px;text-align:right;font-size:12px;color:var(--muted);font-variant-numeric:tabular-nums}#needStrip.open em{left:100%;margin-left:6px;top:0}'
    + '#needStrip .nsFold,#needStrip .nsMini{display:flex;align-items:center;justify-content:center;width:18px;color:var(--muted)}#needStrip .nsMini{display:none;width:22px}'
    + '#needStrip .nsFold{appearance:none;border:0;background:none;padding:0;min-height:0;font-size:15px;line-height:1;cursor:pointer;-webkit-backdrop-filter:none;backdrop-filter:none}'
    + '#needStrip .nsT{display:flex;align-items:center;font-size:12px;font-weight:600;color:var(--muted);letter-spacing:.03em;padding-right:1px}#needStrip.open .nsT{align-self:flex-start}'   // 0.28.57: the strip says what it is (the user's)
    + '#needStrip.open .nsFold{align-self:flex-end}#needStrip.fold{padding:6px 8px}#needStrip.fold .ns,#needStrip.fold .nsFold{display:none}#needStrip.fold .nsMini{display:flex}';
  document.head.appendChild(st);
  el = document.createElement('div'); el.id = 'needStrip'; el.setAttribute('role', 'button'); el.setAttribute('aria-label', 'Your needs: tap for names and numbers');
  el.innerHTML = '<b class="nsT" aria-hidden="true">Needs</b>' + NEED_KEYS.map(k => '<div class="ns" data-k="' + k + '" style="color:' + NEED_COL[k] + '"><svg viewBox="0 0 24 24"><path d="' + NEED_ICON[k] + '"/></svg><span>' + NEED_LABEL[k] + '</span><i><b></b></i><u></u><em></em></div>').join('')
    + '<button class="nsFold" aria-label="Fold your needs away">‹</button><div class="nsMini"><svg viewBox="0 0 24 24"><path d="' + STRIP_HEART + '"/></svg></div>';
  el.onclick = e => { e.stopPropagation(); if (SHIP.player.stripFold) stripFold(false); else { el.classList.toggle('open'); STRIP_SIG = ''; } };
  el.querySelector('.nsFold').onclick = e => { e.stopPropagation(); stripFold(true); };
  document.body.appendChild(el);
  if (SHIP.player.stripFold) el.classList.add('fold');
  try { hudBelow(); } catch (e) { /* section 11 not run yet: its next clock tick lines it up */ }   // under a tall HUD (0.28.59)
  return el;
}
function stripRise(k, v) {                               // a rise beside its icon; a new one while it shows adds to it
  const now = performance.now(), r = RISES[k], keep = r && now - r.at < RISE_SECS * 1000 && (r.v < 0) === (v < 0);   // a drop (v < 0, 0.73.0) never merges with a rise
  RISES[k] = { v: (keep ? r.v : 0) + v, at: now, txt: '' };
}
function stripTick(now, still) {
  const el = needStrip(), n = SHIP.player.needs, low = NEED_KEYS.filter(k => n[k] < NEED_LOW);
  const g = low.length && !still ? .55 + .45 * Math.abs(Math.sin(now / 520)) : 1;   // the gentle pulse, on the frame clock
  const sig = NEED_KEYS.map(k => Math.round(n[k])).join(',') + '|' + low.length, gq = low.length ? (Math.round(g * 10) / 10).toFixed(1) : '';   // the pulse in tenths (0.28.38, reviewer 1c): a few style changes a second, not a rebuild every frame
  if (sig === STRIP_SIG && gq !== STRIP_G) {
    STRIP_G = gq; el.querySelector('.nsMini').style.opacity = gq;
    for (const d of el.children) if (d.dataset.k && n[d.dataset.k] < NEED_LOW) d.style.opacity = gq;
  }
  if (sig !== STRIP_SIG) {
    STRIP_SIG = sig; STRIP_G = gq;
    const mini = el.querySelector('.nsMini'); mini.style.color = low.length ? NEED_AMBER : 'var(--teal)'; mini.style.opacity = gq;
    for (const d of el.children) {
      if (!d.dataset.k) continue;
      const k = d.dataset.k, v = Math.max(0, Math.min(100, n[k])), lo = v < NEED_LOW;
      d.style.color = lo ? NEED_AMBER : NEED_COL[k]; d.style.opacity = lo ? gq : '';
      d.children[2].children[0].style.transform = 'scaleX(' + (v / 100).toFixed(3) + ')'; d.children[3].textContent = Math.round(v);
      d.title = NEED_LABEL[k] + ' ' + Math.round(v);
    }
  }
  for (const d of el.children) {
    if (!d.dataset.k) continue;
    const k = d.dataset.k, r = RISES[k], em = d.children[4];
    if (!r) { if (em.style.opacity !== '0' && em.style.opacity) em.style.opacity = '0'; continue; }
    const f = (now - r.at) / (RISE_SECS * 1000);
    if (f >= 1) { delete RISES[k]; em.style.opacity = '0'; continue; }
    const txt = (r.v < 0 ? '\u2212' : '+') + Math.round(Math.abs(r.v)); if (r.txt !== txt) { r.txt = txt; em.textContent = txt; }
    em.style.opacity = (f < .1 ? f / .1 : f > .7 ? (1 - f) / .3 : 1).toFixed(3);
  }
}
function needsSeen() {                                   // once a frame: what rose since the last frame
  const n = SHIP.player.needs, now = performance.now();
  if (!NEED_SEEN) { NEED_SEEN = { ...n }; return; }
  for (const k of NEED_KEYS) {
    const d = n[k] - NEED_SEEN[k]; NEED_SEEN[k] = n[k];
    const r = NEED_RISE[k] || (NEED_RISE[k] = { v: 0, t: 0 });
    if (d > 0) { if (!(r.v > 0)) r.t0 = now; r.v += d; r.t = now; }
    const stopped = now - r.t > FLOAT_WAIT * 1000;      // a slow trickle under FLOAT_MIN keeps adding up until it stops
    if (r.v > 0 && (stopped || r.v >= FLOAT_MIN && now - r.t0 > FLOAT_EVERY * 1000)) {
      if (r.v >= FLOAT_MIN) { needFloat('+' + Math.round(r.v) + ' ' + NEED_LABEL[k], k, r.v); NEED_PULSE[k] = now + PULSE_SECS * 1000; }
      r.v = 0;
    }
  }
}
// ---- progress for things that take time (0.28.21, the user's): a small bar over your character while an activity
// runs, with what you're doing and how long is left. Any activity of a set length shows it (eating, the grab shelf,
// a shower, the toilet, a workout, a call home, browsing, paying, the job loop's steps, the cart run, and 15b's
// activities, which are ACTs too); the servery queue shows the wait to your turn; sitting (until you get up) shows
// none. actProgress(A) -> { title, frac, left } or null; the bar is placed once a frame. DOM only. ----
const BAR_Y = 1.95;                                      // over the stand-in's head, m
let BAR_TXT = '';
function actProgress(A = ACT) {
  if (!A || A.phase !== 'do' || !A.body) return null;
  const title = A.def.title || A.o.title || '';
  if (A.kind === 'queue') return null;                    // no countdown in the queue (0.28.30): its turn is only an estimate
  if (A.def.until || !(A.def.mins > 0)) return null;
  const tk = A.kind === 'eat' && typeof CHAT !== 'undefined' && CHAT && CHAT.talk && !CHAT.talk.end ? CHAT : null;   // talking while you eat: one bar for both (playtest 1)
  return { title: tk ? 'Eating, talking with ' + shortName(tk.p) : title, frac: Math.max(0, Math.min(1, A.done / A.def.mins)), left: Math.max(0, (A.def.mins - A.done) / needEffects().task) };
}
function actBar() {
  let el = document.getElementById('actBar');
  const pr = actProgress();
  if (!pr) { if (el && !el.hidden) el.hidden = true; return; }
  if (!el) {
    needFxLayer();
    const st = document.createElement('style');
    st.textContent = '#actBar{position:fixed;left:14px;top:0;z-index:2;pointer-events:none;width:180px;margin:0;padding:4px 9px 6px;border-radius:10px;background:var(--glass);border:1px solid var(--line);font-size:11.5px;line-height:1.3;color:#cfd9dc;text-align:center;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}'
      + '#actBar[hidden]{display:none}#actBar i{display:block;height:4px;margin-top:3px;border-radius:2px;background:rgba(150,200,196,.22);overflow:hidden}'
      + '#actBar b{display:block;height:100%;background:var(--teal);transform-origin:left center}';
    document.head.appendChild(st);
    el = document.createElement('div'); el.id = 'actBar'; el.setAttribute('role', 'progressbar'); el.setAttribute('aria-valuemin', 0); el.setAttribute('aria-valuemax', 100);
    el.innerHTML = '<span></span><i><b></b></i>'; document.body.appendChild(el); BAR_TXT = '';
  }
  const A = ACT, txt = pr.title + ' · ' + (pr.left < 1 ? 'nearly done' : Math.ceil(pr.left) + ' min');
  if (txt !== BAR_TXT) { BAR_TXT = txt; el.children[0].textContent = txt; el.setAttribute('aria-label', txt); }
  el.children[1].children[0].style.transform = 'scaleX(' + pr.frac.toFixed(3) + ')'; el.setAttribute('aria-valuenow', Math.round(pr.frac * 100));
  floatV.set(A.x, A.y + BAR_Y, A.z).project(camera);
  const sb = document.getElementById('needStrip'), tb = document.getElementById('trkBtn');   // under the needs strip (0.28.32); on a phone under the Tracked button there (item D, the user's, 0.64.2: the bar always last)
  const under = sb && sb.offsetWidth && tb && !tb.hidden && tb.offsetWidth && matchMedia('(max-width:720px),(max-height:500px)').matches ? tb.getBoundingClientRect().bottom : null;
  const y = under !== null ? Math.round(under + 6) : sb ? sb.offsetTop + sb.offsetHeight + 6 : 124;
  el.style.transform = 'translateY(' + y + 'px)'; el.style.width = sb ? sb.offsetWidth + 'px' : '';
  el.hidden = typeof DEV !== 'undefined' && !!DEV.open;  // never over the device
}
// once a frame from the main loop (section 12): needs over ship time, walking speed, the activity, the device
function playerUpdate(dt, t) {
  const now = shipNow(), n = SHIP.player.needs;
  if (SHIP.player.tray && typeof deckDef !== 'undefined' && deckDef.num !== 3) SHIP.player.tray = null;   // trays stay in the mess (0.28.38, reviewer 1c): off Deck 3 it's left behind for clearing
  if (needsT === null || now < needsT) needsT = now;
  const dm = now - needsT;
  if (dm > 0) {
    const A = ACT, doing = A && A.phase === 'do' && A.done < A.def.mins && A.def.need;
    let fx = playerFx();
    const sat = A && A.kind === 'sit' && A.phase === 'do';
    if (sat) fx = { ...fx, drain: { ...fx.drain, energy: fxD(fx, 'energy') * SIT_REST } };   // sitting rests you (0.28.12)
    const lay = A && A.kind === 'lie' && A.phase === 'do';
    if (lay) fx = { ...fx, drain: { ...fx.drain, energy: 0 } };   // lying in your bunk: no tiring, a little rest (0.28.29)
    needsT = now; needsDrain(dm, false, fx, doing || null); workLeisure(dm, fx, doing);
    if (lay) n.energy = needClamp(n.energy + LIE_GAIN * dm);
    if (sat) n.social = needClamp(n.social + SIT_GAIN * sitCompany(A) * needEffects(n).socialGain * dm);
    if (A && A.phase === 'do') {
      const dw = A.def.until || A.def.real ? dm : dm * needEffects(n).task;   // tasks go faster or slower with your needs (needEffects)
      const m = Math.max(0, Math.min(dw, A.def.mins - A.done)); A.done += dw;
      if (A.kind === 'job' && A.o.repair && SHIP.player.work) SHIP.player.work.done += m;   // repair time is kept if you walk away
      if (A.kind === 'make' && SHIP.player.work && SHIP.player.work.make) SHIP.player.work.make.done += m;   // and making a part
      const bm = A.def.need === 'social' && A.o.opp ? bondMult(A.o.opp) : 1;   // a game of Tiles: by your bond with them (0.28.43)
      if (A.def.need) n[A.def.need] = needClamp(n[A.def.need] + A.def.gain / A.def.mins * fxR(fx, A.def.need) * bm * m);
      if (A.def.cost) for (const k in A.def.cost) { const was = n[k]; n[k] = needClamp(n[k] - A.def.cost[k] / A.def.mins * m); (A.o.cost || (A.o.cost = {}))[k] = (A.o.cost[k] || 0) + was - n[k]; }   // a workout tires you (0.28.17); A.o.cost: what it took, shown at the end (0.73.0)
      if (A.kind === 'eat' && m > 0) {                   // company at your table (0.28.10, 0.28.43): by the bond, up to COMPANY_CAP
        const c = company(A); A.o.company = Math.max(A.o.company || 0, c);   // bond-weighted, capped (0.28.43)
        n.social = needClamp(n.social + COMPANY_GAIN * c * needEffects(n).socialGain * m);
      }
    }
  }
  if (PLAYER_V0 === undefined) PLAYER_V0 = player.maxV;
  bagTick();                                             // the kit bag into your locker after the bunk step (0.28.26)
  handTick();                                            // the Repair button (0.28.52)
  dinnerTick();                                          // sit down at your table for the arrival dinner (0.28.28)
  const P = SHIP.player, hold = P.cart ? (P.cart.stage === 'full' ? 'cartfull' : 'cart') : P.carry.length > 0 || typeof hamperHeld === 'function' && hamperHeld() ? true
    : ACT && ACT.kind === 'eat' && ACT.o.fed && ACT.phase === 'walk' || !ACT && P.tray ? 'tray' : typeof ixHold === 'function' && ixHold() || false;   // a tray from the servery to your seat (0.28.15); 15b's ixHold: a job's toolbox or crate
  if (hold || player.holding) player.holding = hold;   // in hand (Walker.update): parts (true, the crate) or a hover cart ('cart', 'cartfull')
  player.maxV = PLAYER_V0 * playerSpeed();
  const crouch = crawlTiles().has(K(player.here()));   // a crawlway (0.28.11): crouch-walk, slower
  if (crouch) player.maxV *= CRAWL_SPEED;
  if (squeezeStep()) player.maxV *= SQUEEZE_SPEED;      // squeezing past someone (0.28.12)
  shuffleTick(dt);                                       // walking into someone on their feet: they step aside (0.28.70)
  if (crouch && !player.crouch) toast('Crawlway', 'You duck down and crouch-walk through.');
  const bent = typeof sickBent === 'function' && sickBent();   // doubled over when you're very unwell (0.61.5)
  if (crouch || bent || player.crouch) player.crouch = crouch || bent;
  const go = n.bathroom <= 0;                            // bursting (0.28.41): the '+go' pose while it's at 0 (hands full keep their hold)
  if (go || player.needGo) player.needGo = go;
  const pn = performance.now(); popupWatch(pn); needWarnTick(pn); teachTick(pn);   // a need getting low says so (0.28.41; it replaced the two slow-walk toasts), and the teaching tips (0.28.42)
  if (ACT) actUpdate(dt, t);
  needsSeen(); floatsTick();                             // a need that rose shows it (0.28.20; faded by frames, 0.28.23)
  actBar();                                              // and how long the activity has left (0.28.21)
  const m = Math.floor(now);
  if (m !== devMin) { devMin = m; jobNotice(); jobTouch(); cartAuto(); gardenGift(); newsTick(now); device.refresh(); }
}
// squeezing past (0.28.12): crew settled at their places hold their tile (section 10's occupiedBy), which can close
// the only way through (Chef Brennan at the galley's middle station, the plant panel behind her). When the player's
// goTo (section 10, one line) finds no path, squeezePath tries again through settled crew's tiles (never walking
// crew, never ending on one). Passing them slows you to SQUEEZE_SPEED, with a polite word the first time.
const SQUEEZE_SPEED = .5; let SQUEEZE = new Map(), squeezeSaid = null;
function squeezePath(w, goal, avoid) {
  if (typeof DECK_CREW === 'undefined') return null;
  const held = new Map(); for (const a of DECK_CREW) if (a.settled && a.spot && a.spot.onTile) held.set(K(a.spot.walk), a);
  if (!held.size || held.has(K(goal))) return null;
  const p = findPath(w.here(), goal, new Set([...avoid].filter(k => !held.has(k))), w); if (!p) return null;
  SQUEEZE = new Map(p.filter(c => held.has(K(c))).map(c => [K(c), held.get(K(c))]));
  return SQUEEZE.size ? p : null;
}
function squeezeStep() {                                 // each frame: slow down passing someone, and say excuse me once
  if (!SQUEEZE.size) return false;
  if (!player.path.length) { SQUEEZE = new Map(); squeezeSaid = null; return false; }
  const at = k => { const a = SQUEEZE.get(k); return a && a.settled && a.spot && K(a.spot.walk) === k ? a : null; };   // still there
  const a = at(K(player.here())) || at(K(player.path[0]));
  if (!a) return false;
  if (squeezeSaid !== a) {
    squeezeSaid = a; const first = (a.p.name || '').split(' ')[0];
    toast(a.p.name, '"Excuse me, ' + (/chef/i.test(a.p.role || '') ? 'Chef' : first) + '." ' + first + ' shifts aside to let you by.');
  }
  return true;
}
// shuffling aside (0.28.70, the user's note on 0.60.5): walk into a crew member who's standing or walking (not seated,
// not settled at a place: squeeze past covers those) and they take a small step aside, SHUFFLE_STEP tiles to the
// nearer open side of your way (the other side if that one's a wall or furniture; in a one-tile corridor a shorter
// step, SHUFFLE_SHORT, to the wall; else a step back), then carry on with what they were doing. You're never held up
// by them (section 10's press-and-hold push skips them: shuffleable). No room on any side: you pass them anyway.
// Stepped once, a person isn't stepped again for SHUFFLE_COOL ms (no wobbling while you follow close behind). A polite
// word in a speech bubble over them (8b's bubbleSay; never a toast, so the need warnings never wait on it), at most once
// a person a minute (SHUFFLE_SAID, real ms), and never over something they're already saying.
const SHUFFLE_STEP = .5, SHUFFLE_SHORT = .25, SHUFFLE_V = 2, SHUFFLE_NEAR = .45, SHUFFLE_SAY = 60000, SHUFFLE_COOL = 1500;
const SHUFFLE_WORDS = ['Oh, sorry.', 'After you.', 'Excuse me.', 'Oops, mind out.', 'Sorry, go ahead.'];
const SHUFFLE = new Map(), SHUFFLE_SAID = new Map(), SHUFFLE_DONE = new Map();   // crew agent -> { x, z, left } (the step still to take); person id -> when they last said it; crew agent -> when their step ended
const shuffleable = a => !!a && !a.settled && !(a.esc && !/^follow\|/.test(a.esc)) && !(a.talking > 0) && !(a.p && a.p.player) && a.pose !== 'sit' && a.pose !== 'lie';
const shuffleStep = (b, c) => {                           // from tile b to the next tile c: no wall between (a diagonal: open round one corner)
  const di = c[0] - b[0], dj = c[1] - b[1]; if (Math.abs(di) > 1 || Math.abs(dj) > 1) return false;
  if (!di || !dj) return edgeOpen(b[0], b[1], c[0], c[1], null);
  return [[c[0], b[1]], [b[0], c[1]]].some(m => free(...m) && edgeOpen(b[0], b[1], m[0], m[1], null) && edgeOpen(m[0], m[1], c[0], c[1], null));
};
function shuffleClear(x0, z0, x1, z1) {                  // a body can go from (x0, z0) to (x1, z1): open tiles, no wall between, nothing solid
  const n = Math.max(2, Math.ceil(Math.hypot(x1 - x0, z1 - z0) / .2));
  for (let k = 1; k <= n; k++) {
    const x = x0 + (x1 - x0) * k / n, z = z0 + (z1 - z0) * k / n, c = cellAt(x, z), b = cellAt(x0 + (x1 - x0) * (k - 1) / n, z0 + (z1 - z0) * (k - 1) / n);
    if (!free(...c)) return false;
    if (K(c) !== K(b) && !shuffleStep(b, c)) return false;
    const q = { x, z }; collide(q, BODY_R, null); if (Math.hypot(q.x - x, q.z - z) > .02) return false;
  }
  return true;
}
function shuffleTick(dt) {
  if (typeof DECK_CREW === 'undefined') return;
  for (const [a, s] of SHUFFLE) {                        // the step aside, a little each frame
    if (!DECK_CREW.includes(a) || !shuffleable(a)) { SHUFFLE.delete(a); continue; }
    const st = Math.min(s.left, SHUFFLE_V * dt); a.x += s.x * st; a.z += s.z * st; s.left -= st;
    if (s.left <= 1e-4) { SHUFFLE.delete(a); SHUFFLE_DONE.set(a, performance.now()); }
  }
  for (const [a, t] of SHUFFLE_DONE) if (performance.now() - t >= SHUFFLE_COOL || !DECK_CREW.includes(a)) SHUFFLE_DONE.delete(a);
  const pos = player.obj.position, s = player.steer;
  let mx = s ? s.x : 0, mz = s ? s.z : 0;               // which way you're walking: the finger, or the next tile of your path
  if (!s && player.path.length) { const c = cellPos(...player.path[0]); mx = c.x - pos.x; mz = c.z - pos.z; }
  const ml = Math.hypot(mx, mz); if (ml < 1e-3 || player.vel < .15) return;
  mx /= ml; mz /= ml;
  for (const a of DECK_CREW) {
    if (SHUFFLE.has(a) || SHUFFLE_DONE.has(a) || !shuffleable(a)) continue;
    const ox = a.x - pos.x, oz = a.z - pos.z, od = Math.hypot(ox, oz);
    if (od >= SHUFFLE_NEAR || od > 1e-4 && (ox * mx + oz * mz) / od < .3) continue;   // touching, and ahead of you
    const side = ox * mz - oz * mx >= 0 ? 1 : -1;       // the side of your way they're already on (a tie: your right)
    const L = SHUFFLE_STEP, S = SHUFFLE_SHORT, ways = [[mz * side, -mx * side, L], [-mz * side, mx * side, L], [mz * side, -mx * side, S], [-mz * side, mx * side, S], [mx, mz, L]];
    const w = ways.find(([ux, uz, l]) => shuffleClear(a.x, a.z, a.x + ux * l, a.z + uz * l) && (!a.path.length || (() => { const c = cellPos(...a.path[0]); return shuffleClear(a.x + ux * l, a.z + uz * l, c.x, c.z); })()));
    if (!w) continue;                                    // nowhere to step: you just get by
    SHUFFLE.set(a, { x: w[0], z: w[1], left: w[2] });
    const id = a.p && a.p.id, at = performance.now();
    if (id && a.h && typeof bubbleSay === 'function' && !(at - SHUFFLE_SAID.get(id) < SHUFFLE_SAY) && !bubbles.list.some(b => b.who === a.h)) {   // never over something they're already saying
      SHUFFLE_SAID.set(id, at); bubbleSay(a.h, SHUFFLE_WORDS[(idHash(id) + SHUFFLE_SAID.size) % SHUFFLE_WORDS.length], 2.5);
    }
  }
}
// crawlway tiles: the deck's crawl list (['i,j', ...], from the architects); CRAWL_SPEED of your walking speed there
const CRAWL_SPEED = .5; let CRAWL = { def: null, set: new Set() };
function crawlTiles() {
  if (typeof deckDef === 'undefined' || !deckDef) return CRAWL.set;
  if (CRAWL.def !== deckDef) CRAWL = { def: deckDef, set: new Set((Array.isArray(deckDef.crawl) ? deckDef.crawl : []).map(String)) };
  return CRAWL.set;
}
// a time skip: asleep if you chose Sleep (section 13), or for the debug Day button (a skip from the night);
// otherwise awake. Any activity stops.
SIM_ADVANCE.push((from, to) => {
  if (!(ACT && ACT.kind === 'lie')) actEnd(true); JOB_SEEN = null; SHIP.player.tray = null;   // a tray doesn't last the night (0.28.38)   // asleep in your bunk you wake there, still lying (0.28.29)                        // jobs posted while you slept aren't announced one by one
  const d = typeof deckDef !== 'undefined' && deckDef ? deckDef.num : 0;   // a replay: section 17's pure record, never the live machines
  let fx = null; try { fx = typeof shipEffectsAt === 'function' && d ? shipEffectsAt(d, from) : null; } catch (e) { fx = null; }
  needsDrain(to - from, sleeping || nightAt(from % 1440) > .5, fx);
  needsT = to;
});
// New game (section 13): fresh needs, nothing in hand
function playerNew() {
  actEnd(true); basket = null; SHIP.player.needs = needsLoad(null); NEED_SEEN = null; SHIP.player.carry = []; SHIP.player.work = null; SHIP.player.wsteps = []; SHIP.player.bedMade = null; SHIP.player.untidy = false; SHIP.player.teaDay = null; NEED_GOAL = null; PUSH = null; SHIP.player.tray = null; SHIP.player.crate = null; needsT = null; slowWas = {}; WARN_SAID = {}; TEACH_ST = null; POP.tip = -1e9; Object.assign(SHIP, { news: [], newsUsed: [], newsAt: null, newsRows: {} });
  Object.assign(SHIP.player, walletLoad(null)); SHIP.player.bought = 0; SHIP.player.cart = null; SHIP.player.name = null; SHIP.mail = []; mailWelcome(); device.refresh();
  DINNER_SAT = false; DINNER_TRY = -1;                   // a new arrival dinner seats you again (reviewer 1, 0.28.37)
  SHIP.player.alarm = WAKE_AT;                           // the alarm clock back at 06:00 (0.73.0)
}

// ---- your job (Pillar 2, B2): the player's side of section 17's job list. Take a job on the device (17's jobs
// section), fetch its parts from main storage on Deck 5 (tap a shelf or the counter there; you carry CARRY_MAX at a
// time), then tap the machine: you walk to its panel place, fit what you carry, look it over (INSPECT_MINS, the first
// time) and repair it for the job's minutes. Walking away keeps what's fitted and the repair time done. Finished:
// finishJob (17) puts the machine right. A job with more parts than you can carry takes two trips. Parts you hold
// with no job to use them go back on a shelf (17's returnPart, when it's there). Without section 17, none of this. ----
const CARRY_MAX = 2, INSPECT_MINS = 3;
// a free place of a type in a room of this deck, nearest a point: the storage places by the shelves and the lathe
function jobPlaceNear(type, room, at) {
  return [...PLACE_OF.values()].filter(q => q.type === type && q.room === room && !heldBy(q.id)).map(q => [q, placeSpot(q.id)]).filter(([, s]) => s)
    .sort((m, n) => Math.hypot(m[1].x - at.x, m[1].z - at.z) - Math.hypot(n[1].x - at.x, n[1].z - at.z)).map(m => m[0])[0] || null;
}
// the wrist comm: a job you could take is posted (checked each ship minute; not for jobs posted while you slept)
// progress on your job keeps it yours (section 17's touchJob: the 12-hour lapse counts from the last progress):
// parts fitted, and each ship minute of repairing or making a part for it
function jobTouch(now) {
  if (typeof touchJob !== 'function' || !SHIP.player.work) return;
  if (now || ACT && ACT.phase === 'do' && (ACT.kind === 'job' && ACT.o.repair || ACT.kind === 'make')) touchJob(SHIP.player.work.job);
}
let JOB_SEEN = null;
function jobNotice() {
  if (!jobsOn() || typeof jobsBoard !== 'function') return;
  const tier = typeof playerTier === 'function' ? playerTier() : 1;
  const open = jobsBoard().filter(j => !j.claimedBy && j.machine && (typeof jobTier !== 'function' || jobTier(j) <= tier)
    && !(typeof ENGINE_KINDS !== 'undefined' && ENGINE_KINDS.has((machineById(j.machine) || {}).kind)));
  if (!JOB_SEEN) { JOB_SEEN = new Set(open.map(j => j.id)); return; }
  const fresh = open.filter(j => !JOB_SEEN.has(j.id)); for (const j of open) JOB_SEEN.add(j.id);
  if (!fresh.length || myJob() || ACT) return;           // not while you hold a job or are busy
  const c = typeof jobCard === 'function' ? jobCard(fresh[0]) : [fresh[0].kind, deckWord(fresh[0].deck)];
  toast('Your device', 'New job: ' + c[0] + ', ' + c[1] + (fresh.length > 1 ? ', and ' + (fresh.length - 1) + ' more' : '') + '. Take it at the job board in the Works bay, Deck 5.');
}
function carryLoad(s) { const c = s && s.player && s.player.carry; return Array.isArray(c) ? c.filter(x => typeof x === 'string').slice(0, CARRY_MAX) : []; }
function workLoad(s) {
  const w = s && s.player && s.player.work; if (!w || !(typeof w.job === 'string' || typeof w.job === 'number')) return null;
  const mk = w.make && typeof w.make.part === 'string' ? { part: w.make.part, done: isFinite(w.make.done) && w.make.done > 0 ? +w.make.done : 0 } : null;
  return { job: w.job, fitted: Array.isArray(w.fitted) ? w.fitted.filter(x => typeof x === 'string') : [], done: isFinite(w.done) && w.done > 0 ? +w.done : 0, seen: !!w.seen, make: mk };
}
SHIP.player.carry = carryLoad(SAVED); SHIP.player.work = workLoad(SAVED);
if (!SAVED) setTimeout(() => { if (!SHIP.mail.length) mailWelcome(); }, 0);   // a fresh start (after the device exists, below)
const jobsOn = () => typeof myJob === 'function' && typeof finishJob === 'function' && typeof takePart === 'function' && typeof machineById === 'function';
// getting quicker (Pillar 5, foundation 15.2): your repair minutes on a machine kind shrink with the jobs on that kind
// you've turned in (SHIP.works.sk[kind], counted by section 24 core): 1 for 0-4, .8 from 5, .65 from 15. Words only
// on screen (24 core's skillWord). No SHIP.works: always 1
function careerSpeed(kind) {
  const n = typeof SHIP !== 'undefined' && SHIP.works && SHIP.works.sk && +SHIP.works.sk[kind] || 0;
  return n >= 15 ? .65 : n >= 5 ? .8 : 1;
}
const jobKindOfMachine = j => j && j.machine && typeof machineById === 'function' ? (machineById(j.machine) || {}).kind || null : null;
const jobMins = j => JOB_TYPES[j.kind].work * (1 + .25 * ((typeof jobTier === 'function' ? jobTier(j) : 1) - 1)) * careerSpeed(jobKindOfMachine(j)) * (j.logged ? .9 : 1);   // j.logged: written up in the Works log (24n), 10% quicker
function myWork() {                                      // the job you hold, and how far you've got with it (null: none)
  const j = jobsOn() ? myJob() : null, P = SHIP.player;
  if (!j || !j.machine) { P.work = null; return null; }
  if (!P.work || P.work.job !== j.id) P.work = { job: j.id, fitted: [], done: 0, seen: false, make: null };
  return { j, w: P.work };
}
function jobNeeds(j, w, less = []) {                     // the parts still to fit, less any listed (what you carry)
  const need = j.parts.slice();
  for (const p of w.fitted.concat(less)) { const i = need.indexOf(p); if (i >= 0) need.splice(i, 1); }
  return need;
}
// a part the job says you make yourself (0.28.24, Pillar 4: section 17's reserved jobs carry j.make, e.g. 'bracket'):
// never taken off the shelf, always made in the machine shop (j.makeMins, else PLAYER_ACTS.make's hour). shelfNeeds:
// what's left to fetch from main storage. whereFrom: where the parts still needed come from, for the toasts.
const madeHere = j => typeof j.make === 'string' && j.make ? j.make : null;
function shelfNeeds(j, w, less) { const n = jobNeeds(j, w, less), i = madeHere(j) ? n.indexOf(j.make) : -1; if (i >= 0) n.splice(i, 1); return n; }
const makeMins = j => Number.isFinite(j && j.makeMins) && j.makeMins > 0 ? j.makeMins : PLAYER_ACTS.make.mins;
const whereFrom = (j, need) => need.includes(madeHere(j)) ? 'Make the ' + j.make + ' in the machine shop on Deck 5' + (need.length > 1 ? '; the rest is in main storage next door.' : '.') : 'Main storage is on Deck 5.';
function jobStopMark(j, step) {                          // tell section 17 a stop is done (its stepsDone, simNote('job', 'stop'))
  if (typeof jobStepDone !== 'function' || typeof jobStops !== 'function') return;
  const k = jobStops(j).findIndex(x => x.step === step); if (k >= 0) try { jobStepDone(j.id, k); } catch (e) { /* not ours to mend */ }
}
const giftHeld = () => typeof giftInHands === 'function' && !!giftInHands();   // a gift among the things in your hands (section 20, 0.28.25)
// the kit bag (0.28.26, Pillar 4, agreed with section 21): from the top of the Tern's ramp (introOn(), step 'ramp') you
// hold your kit bag in one of your two hands (P.carry, saved with it). It goes in your locker when you tap anywhere in
// Bunk 1 (bagLockerTap, from playerFloorTap), or by itself once the bunk step is done; a missed bunk step leaves it in
// your hands until you do. Never with the intro off: then it goes in quietly. bagGive() / bagStow(quiet) for section 21.
// Never a part: main storage doesn't take it back. handsFix(what): what to do about full hands, for the toasts.
const KIT_BAG = 'kitbag';
const bagHeld = () => SHIP.player.carry.includes(KIT_BAG);
function bagGive() { const P = SHIP.player; if (bagHeld() || P.carry.length >= CARRY_MAX) return false; P.carry.unshift(KIT_BAG); return true; }
function bagStow(quiet) {
  const P = SHIP.player, i = P.carry.indexOf(KIT_BAG); if (i < 0) return false;
  P.carry.splice(i, 1); if (!P.locker.includes(KIT_BAG) && P.locker.length < LOCKER_MAX) P.locker.push(KIT_BAG);
  if (!quiet) toast('Bunk 1', 'You put your kit bag in your locker. Your hands are free.');
  return true;
}
function bagTick() {
  const on = typeof introOn === 'function' && introOn(), I = SHIP.intro || {};
  if (!bagHeld()) { if (on && I.step === 'ramp') bagGive(); return; }
  if (!on) bagStow(true);
  else if ((I.done || {}).bunk !== undefined && !(I.missed || []).includes('bunk')) bagStow(false);
}
function bagLockerTap(point) {                           // a tap in Bunk 1 with the bag in your hands: walk there, stow it
  if (!bagHeld() || typeof deckDef === 'undefined' || deckDef.num !== 4) return false;
  const ch = roomAt(...cellAt(point.x, point.z)), rm = ch && deckDef.rooms && deckDef.rooms[ch];
  if (!rm || rm.name !== 'Bunk 1') return false;
  approach(new THREE.Vector3(point.x, 0, point.z), 0, 0, () => bagStow(false));
  return true;
}
// the arrival dinner (0.28.28, the lead's polish row): you sit at the table instead of standing. playerSitNear(deck,
// tile, title) sits you at the free public seat nearest that tile (within DINNER_NEAR m; false if none or you're
// elsewhere); section 21 may call it. dinnerTick() does it once by itself: section 21's 'chief' step (your table in the
// mess, and the 'table' step before it, the dinner chat with Torres at the same table: onboarding 5, 0.42.63, the user's "I used to sit down")
// while it's yours, or in its first DINNER_MINS after you reached it, when you stand idle within DINNER_NEAR of
// its checkpoint: at section 21's introSeat('you') (3-mess-10, by Torres) when it names a free one, else the nearest.
// Tap anywhere to get up, as with any seat.
const DINNER_NEAR = 3, DINNER_MINS = 30;
let DINNER_SAT = false, DINNER_TRY = -1;                 // seated once (also the saved flag 'intro.dinnerSat' when section 13's flags are here: a reload doesn't seat you again); the last ship minute it looked for a seat
const dinnerSat = v => { if (v) { DINNER_SAT = true; if (typeof flagSet === 'function') flagSet('intro.dinnerSat'); } return DINNER_SAT || typeof flag === 'function' && !!flag('intro.dinnerSat'); };
function playerSitNear(deck, tile, title = 'Mess table') {
  if (typeof PLACE_OF === 'undefined' || typeof deckDef === 'undefined' || deckDef.num !== deck) return false;
  const c = cellPos(...tile), seat = [...PLACE_OF.values()].filter(pl => SIT_TYPES.has(pl.type) && pl.pose === 'sit' && !privatePlace(pl) && !heldBy(pl.id))
    .map(pl => [pl, placeSpot(pl.id)]).filter(([, sp]) => sp && sp.pose === 'sit' && Math.hypot(sp.x - c.x, sp.z - c.z) < DINNER_NEAR)
    .sort((m, n) => Math.hypot(m[1].x - c.x, m[1].z - c.z) - Math.hypot(n[1].x - c.x, n[1].z - c.z))[0];
  if (!seat) return false;
  actStart('sit', seat[0].id, { pose: seat[1].pose, title, after: 'You sit down at the table. Tap anywhere to get up.' });
  return true;
}
function dinnerTick() {
  if (ACT || player.path.length || typeof introOn !== 'function' || !introOn() || dinnerSat()) return;
  const m = Math.floor(shipNow()); if (m === DINNER_TRY) return; DINNER_TRY = m;   // once a ship minute: no searching every frame while no seat is free (reviewer 1)
  const I = SHIP.intro, st = typeof introStepById === 'function' ? introStepById('chief') : null, cp = st && st.checkpoint;
  if (!cp || deckDef.num !== cp.deck) return;
  const done = (I.done || {}).chief, yours = I.step === 'table' || I.step === 'chief' || done !== undefined && !(I.missed || []).includes('chief') && shipNow() - done < DINNER_MINS;
  if (!yours) return;
  const c = cellPos(...cp.tile), p = player.obj.position; if (Math.hypot(p.x - c.x, p.z - c.z) > DINNER_NEAR) return;
  const mine = typeof introSeat === 'function' ? introSeat('you') : null, sp = mine && PLACE_OF.has(mine) && !heldBy(mine) ? placeSpot(mine) : null;
  if (sp) { actStart('sit', mine, { pose: sp.pose, title: 'Mess table', after: 'You sit down at the table. Tap anywhere to get up.' }); dinnerSat(true); return; }
  dinnerSat(playerSitNear(cp.deck, cp.tile));
}
const handsFix = what => bagHeld() ? 'Put your bag in your locker first' : giftHeld() ? 'Give the gift away first' : what;
const partList = a => { const n = {}; for (const k of a) n[k] = (n[k] || 0) + 1; return Object.entries(n).map(([k, c]) => (c > 1 ? c + ' × ' : /^[aeiou]/i.test(k) ? 'an ' : 'a ') + k).join(' and '); };
const machineName = m => (typeof MACHINE_KINDS !== 'undefined' && MACHINE_KINDS[m.kind] ? MACHINE_KINDS[m.kind].name : m.kind).toLowerCase();
// a tap (section 11, through playerTap): main storage, or the machine of the job you hold. False: not the job's business
function jobTap(it, at) {
  if (!jobsOn() || typeof deckDef === 'undefined') return false;
  if (typeof traceHidden === 'function' && traceTap(it, at)) return true;   // 24i: a traced job not yet found: the pipe kit's reading (Pillar 5, M3)
  const P = SHIP.player, mw = myWork(), c = cellAt(at.x, at.z);
  if (typeof shopTap === 'function' && shopTap(it, at, mw)) return true;   // 24j: the order board, your order's stops, tinkering (Pillar 5, M10)
  if (deckDef.num === 5 && roomAt(...c) === 'r' && !/tarp/i.test(it.t)) {      // main storage, Deck 5: a shelf or the counter
    if (!mw) {
      const sh = typeof shelfTapped === 'function' ? shelfTapped(it) : null;   // no job at all: a shelf says what's on it (0.33.41)
      if (sh && !myJob() && !P.carry.some(p => p !== KIT_BAG)) { toast(it.t + ' shelf', shelfLine(sh)); return true; }   // not with a chore: its stop may be here (a delivery's pickup)
      if (!P.carry.some(p => p !== KIT_BAG) || typeof returnPart !== 'function') return false;
      approach(at.clone(), it.front, it.depth, () => actStart('stow', null, { title: it.t }));
      return true;
    }
    const need = shelfNeeds(mw.j, mw.w, P.carry);
    if (!need.length && jobNeeds(mw.j, mw.w, P.carry).length) { toast(it.t, 'The ' + mw.j.make + ' isn\'t kept on the shelves: you make it yourself in the machine shop next door.'); return true; }   // 0.28.24
    if (!need.length) { toast(it.t, 'You have what the job needs: ' + partList(P.carry) + '. It\'s at the ' + machineName(machineById(mw.j.machine)) + ' on ' + deckIn(mw.j.deck) + '.'); return true; }
    if (P.carry.length >= CARRY_MAX) { toast(it.t, 'Your hands are full (' + partList(P.carry) + '). ' + handsFix('Fit those first') + ', then come back for ' + partList(need) + '.'); return true; }
    if (typeof shelfWrong === 'function' && shelfWrong(it)) return true;   // the right part from the right shelf (0.33.41): another shelf costs nothing
    const o = { title: it.t, flavour: it.x, after: 'You look for ' + partList(need) + '.' }, pl = jobPlaceNear('storage', 'r', at);
    if (pl) actStart('fetch', pl.id, { ...o, pose: 'browse' }); else approach(at.clone(), it.front, it.depth, () => actStart('fetch', null, o));
    return true;
  }
  if (!mw && deckDef.num === 5 && roomAt(...c) === 'f' && typeof GIFT_MAKES !== 'undefined' && typeof giftAdd === 'function') {   // no job: make a small gift (0.28.25)
    const g = GIFT_MAKES[(P.crafted || 0) % GIFT_MAKES.length], pl = jobPlaceNear('storage', 'f', at);
    if (!g || !pl) return false;
    if (P.carry.length >= CARRY_MAX) { toast(it.t, 'Your hands are full (' + partList(P.carry) + ').'); return true; }
    if (g.needs && typeof SHIP.stores[g.needs] === 'number' && !(SHIP.stores[g.needs] > 0)) { toast(it.t, 'No ' + g.needs + ' left to make ' + partList([g.item]) + ' from.'); return true; }
    actStart('craft', pl.id, { title: it.t, flavour: it.x, gift: g.item, needs: g.needs || null, after: 'You make ' + partList([g.item]) + ' from offcuts, to give to someone: about ' + taskMins(g.mins) + ' minutes.' });
    if (ACT && ACT.kind === 'craft') ACT.def.mins = g.mins;
    return true;
  }
  if (!mw) return false;
  if (deckDef.num === 5 && roomAt(...c) === 'f') {         // the machine shop: make a part storage has run out of
    const want = jobNeeds(mw.j, mw.w, P.carry);           // the job's own made part first (0.28.24), else one storage has run out of
    const make = (P.work.make && P.work.make.part) || (want.includes(madeHere(mw.j)) ? mw.j.make : want.find(p => !(SHIP.stores[p] > 0) && !(typeof NO_MAKE !== 'undefined' && NO_MAKE.has(p))));
    const pl = make && jobPlaceNear('storage', 'f', at);
    if (make && pl) {
      if (P.carry.length >= CARRY_MAX) { toast(it.t, 'Your hands are full (' + partList(P.carry) + '). ' + handsFix('Fit those first') + '.'); return true; }
      if (!P.work.make || P.work.make.part !== make) P.work.make = { part: make, done: 0 };
      const left = Math.max(1, makeMins(mw.j) - P.work.make.done);
      actStart('make', pl.id, { title: it.t, flavour: it.x, part: make, after: (P.work.make.done ? 'Back to the ' : 'You start on a new ') + make + ': about ' + taskMins(left) + ' minutes. Walk away to pause.' });
      if (ACT && ACT.kind === 'make') ACT.def.mins = left;
      return true;
    }
  }
  const m = machineById(mw.j.machine), pid = m && m.deck === deckDef.num && typeof panelPlace === 'function' ? panelPlace(m.id) : null;
  const spot = pid && PLACE_OF.has(pid) ? placeSpot(pid) : null; if (!spot) return false;
  const mc = cellPos(...(m.at || PLACE_OF.get(pid).at));
  // the machine itself (0.28.55, reviewer 1f and the lead: anything within 3 m of its panel took over a washer next to it,
  // the welding bench, the Works station): the thing tapped is in its room, within MACHINE_NEAR of it or .8 m of its panel
  // (Deck 4's light relays), and no other machine in the room is nearer. The floor at its panel and glass-backed things
  // past it still start the work (jobSpotTap), as does Repair
  const dm = Math.hypot(mc.x - at.x, mc.z - at.z), dp = Math.hypot(spot.x - at.x, spot.z - at.z), mine = Math.min(dm, dp);
  if (!(dm <= MACHINE_NEAR || dp <= .8) || roomAt(...c) !== m.room
    || machineList().some(o => o.id !== m.id && !o.stub && o.deck === m.deck && o.room === m.room && o.at && (q => Math.hypot(q.x - at.x, q.z - at.z))(cellPos(...o.at)) < mine)) return false;
  actStart('job', pid, { title: it.t, pose: (typeof poseOf === 'function' ? poseOf(PLACE_OF.get(pid)) : null) || 'work' });
  return true;
}
// your job's work from where you are (0.28.52, the user's lamp report: a lamp's stop is a spot in a lobby with nothing of
// its own to tap, so a tap at the marker only walked you there): the next stop of your chore (15b's ixChoreTap) or the
// panel of the machine you're repairing (jobTap), within JOB_REACH m of point p on this deck, or (a tap: viaRay) under
// the tap's line of sight as it passes over the spot (a thing in front, like Deck 1's trunk head, catches the tap first).
// Null: no work here. parts: what it fits is in hand (or fitted), so the work itself starts (the Repair button's test)
const JOB_REACH = 1.5, JOB_RAY = .6;
function jobRayDist(s) {                                 // the tap's ray from the floor to 1.2 m up: how close it passes to spot s
  const o = ray.ray.origin, d = ray.ray.direction; let best = Infinity;
  for (let y = 0; y <= 1.2; y += .1) { const k = (y - o.y) / d.y; if (k > 0) best = Math.min(best, Math.hypot(o.x + d.x * k - s.x, o.z + d.z * k - s.z)); }
  return best;
}
function jobHere(p, viaRay) {
  if (!jobsOn() || typeof deckDef === 'undefined' || !p) return null;
  let by = Infinity;                                     // how near the tap passes the spot (the floor tap's tie-break, 0.28.55)
  const near = pid => { const s = pid && PLACE_OF.has(pid) ? placeSpot(pid) : null; if (!s) return null; const d = Math.hypot(s.x - p.x, s.z - p.z), r = viaRay ? jobRayDist(s) : Infinity; by = Math.min(d, r);
    return d < JOB_REACH || r < JOB_RAY ? s : null; };
  const P = SHIP.player, j = typeof ixChore === 'function' ? ixChore() : null;
  if (j && !j.workDone) {
    const nx = ixNextStop(j), s = nx && nx.s.step !== 'fetch' && nx.s.deck === deckDef.num ? near(nx.s.places[0]) : null;
    if (s) return { by, parts: !!j.parts.length && !jobNeeds(j, { fitted: [] }, P.carry).length, go: () => ixChoreTap({ t: j.title, x: '' }, new THREE.Vector3(s.x, 0, s.z)) };
  }
  const mj = myJob(), m = mj && mj.machine && !mj.workDone ? machineById(mj.machine) : null, s = m && m.deck === deckDef.num ? near(panelPlace(m.id)) : null;
  const w = P.work && P.work.job === (mj && mj.id) ? P.work : { fitted: [] };   // not myWork(): it makes P.work, and this runs every few frames
  if (s) return { by, parts: !jobNeeds(mj, w, P.carry).length, go: () => jobTap({ t: machineName(m)[0].toUpperCase() + machineName(m).slice(1), x: '', front: 0, depth: 0 }, new THREE.Vector3(s.x, 0, s.z)) };
  return null;
}
// a locked room any stop of your job is in opens for you until you turn the job in (0.28.52: section 18's veyliLamp is a
// lamp in the Captain's quarters, which you could never get into; section 14's doorOpenFor asks). Chores only. And a locked
// room you're standing in always lets you out (0.28.55: it used to shut behind you once the lamp was in)
function jobDoorOpen(deck, room) {
  if (typeof deckDef !== 'undefined' && deckDef.num === deck && roomAt(...player.here()) === room) return true;   // never shut on you inside (0.28.55, reviewer 1f's softlock)
  const j = typeof myJob === 'function' ? myJob() : null; if (!j || !Array.isArray(j.stops) || typeof placeById !== 'function') return false;
  return j.stops.some(x => { const pl = x.placeId && placeById(x.placeId); return !!pl && pl.deck === deck && pl.room === room; });   // any stop of the job you hold, until it's turned in
}
const jobSpotTap = p => { const h = jobHere(p, typeof ray !== 'undefined'); return !!(h && h.go()); };   // a tap on the floor or on anything near your job's stop
// the Repair button (0.28.52, the user's design, "Repair" step): small and thumb-sized at the bottom right, in the slot
// above Put down's (player engineer 8's #putDown), shown only when it applies: you stand at your job's stop (jobHere at
// your feet) with what it fits in hand, and aren't already at work. It starts the same work as a tap there. handTick (playerUpdate) checks four times a
// second of real time; nothing it does touches the ship, so tests and replays are unchanged
const HAND = { at: -1e9, repair: null };
function handEl() {
  let el = document.getElementById('handBtns'); if (el) return el;
  const st = document.createElement('style');
  st.textContent = '#handBtns{position:fixed;right:max(12px,env(safe-area-inset-right));bottom:calc(76px + env(safe-area-inset-bottom));z-index:2;display:flex;flex-direction:column;align-items:flex-end;gap:8px;pointer-events:none}'
    + '#handBtns button{pointer-events:auto;min-width:44px;min-height:44px;padding:8px 14px;border-radius:22px;font-size:14px;display:flex;align-items:center;gap:6px;touch-action:manipulation}'
    + '#handBtns button[hidden]{display:none}#handBtns svg{width:18px;height:18px;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}'
    + '#repairBtn{border-color:#e8c06a;color:#f2e3bf}body.dlgon #handBtns{display:none}';
  document.head.appendChild(st);
  el = document.createElement('div'); el.id = 'handBtns';
  el.innerHTML = '<button type="button" id="hobbyBtn" hidden aria-label="Hobby: something to do while you sit"><svg viewBox="0 0 24 24"><path d="' + NEED_ICON.leisure + '"/></svg><span>Hobby</span></button>'   // 0.28.61
    + '<button type="button" id="repairBtn" hidden aria-label="Repair: start the work here"><svg viewBox="0 0 24 24"><path d="M14.7 6.3a4 4 0 0 0-5.4 5.1L4 16.7 7.3 20l5.3-5.3a4 4 0 0 0 5.1-5.4l-2.6 2.6-2.4-.6-.6-2.4z"/></svg><span>Repair</span></button>';
  document.body.appendChild(el);
  for (const b of el.querySelectorAll('button')) b.addEventListener('pointerdown', e => e.stopPropagation());   // never a tap on the deck behind
  document.getElementById('repairBtn').onclick = e => { e.stopPropagation(); const h = handRepair(); if (h) h.go(); handTick(true); };
  document.getElementById('hobbyBtn').onclick = e => { e.stopPropagation(); hobbyPick(); handTick(true); };
  return el;
}
// ---- hobbies (0.28.61, the 0.60.7 plan's "Hobbies"): seven, each 30 ship minutes for +25 leisure, a meter like a
// meal's. On your device (dev): read, write, play games, anywhere you sit, lie or stand still (the Hobbies app). With a
// prop (prop): drawing (a sketchpad), knitting (needles and wool), puzzles (a puzzle book), from the crew store or (knitting)
// Zeke; stargazing needs only a big window (win). Sitting with a prop hobby or at a window, a Hobby button comes up
// beside Repair. Supplies last for good. SHIP.player.hobbies = { has: [prop ids], done: { id: count }, last: { id: day } },
// saved. Section 20 (social) and the store call hobbyGive(id); hobbyHas(id) and hobbyDone() are for the Record and lines.
const HOBBIES = {
  read:   { dev: true, name: 'Reading', doing: 'Reading', pose: 'sit:read', stand: 'stand+device' },
  write:  { dev: true, name: 'Writing', doing: 'Writing', pose: 'sit:read', stand: 'stand+device' },
  games:  { dev: true, name: 'Playing games', doing: 'Playing a game', pose: 'sit:read', stand: 'stand+device' },
  film:   { dev: true, name: 'Watching films', doing: 'Watching a film', pose: 'sit:read', stand: 'stand+device', label: 'Watch a film' },   // the user's (0.72.1, HUD U): reading's pose and rules; label: the button until the head writer's hobby.name.film
  draw:   { prop: 'a sketchpad', name: 'Drawing', doing: 'Drawing', pose: 'sit:read', price: 15 },
  knit:   { prop: 'needles and wool', name: 'Knitting', doing: 'Knitting', pose: 'sit:read', price: 12 },
  puzzle: { prop: 'a puzzle book', name: 'Puzzles', doing: 'Doing a puzzle', pose: 'sit:read', price: 10 },
  stars:  { win: true, name: 'Stargazing', doing: 'Stargazing', pose: 'sit' },
  garden: { garden: true, name: 'Tend a bed', doing: 'Tending a bed', pose: 'water' },   // the user's (0.28.65): a garden bed off shift, through 15b's ixGarden (30 minutes, +25 leisure)
};
const hobbyText = (key, fb, ctx) => { let t = null; try { t = careerText(key); } catch (e) { t = null; } t = t || fb; if (ctx) for (const k in ctx) t = t.split('{' + k + '}').join(ctx[k]); return t; };   // the head writer's hobby.* texts, else the stand-in
function hobbiesLoad(s) {
  const h = s && s.player && s.player.hobbies, out = { has: [], done: {}, last: {} };
  if (h && typeof h === 'object') {
    if (Array.isArray(h.has)) out.has = [...new Set(h.has.filter(id => HOBBIES[id] && HOBBIES[id].prop))];
    for (const k of ['done', 'last']) if (h[k] && typeof h[k] === 'object') for (const id in h[k]) if (HOBBIES[id] && Number.isFinite(h[k][id])) out[k][id] = Math.max(0, Math.floor(h[k][id]));
  }
  return out;
}
SHIP.player.hobbies = hobbiesLoad(SAVED);
SAVE_EXTRA.push(s => { (s.player || (s.player = {})).hobbies = JSON.parse(JSON.stringify(SHIP.player.hobbies)); });
const hobbyHas = id => !!HOBBIES[id] && (!HOBBIES[id].prop || SHIP.player.hobbies.has.includes(id));
function hobbyGive(id) { const H = SHIP.player.hobbies; if (!HOBBIES[id] || !HOBBIES[id].prop || H.has.includes(id)) return false; H.has.push(id); return true; }
// what you can do where you are: the device hobbies anywhere you're still; prop hobbies and stargazing only sitting (a
// window seat, the observatory or a lounge window for the stars)
// ---- the bar (0.28.62, the 0.60.7 plan's "A bartender and a drink"): tap the bow lounge's bar from 17:30 to 23:00
// with someone behind it (the deck architect's 3-bar-1/2, the systems engineer's rota; a deck without those places
// serves anyway): "What'll it be?" Tea, juice, fizz or cocoa, BAR_PRICE credits. You carry it to a stool and drink it
// there (15b's ixDrink: a little food, social and leisure). The same drink three times running and they offer "The
// usual". Out of hours: "Back at 17:30". SHIP.player.bar = { last, run } is saved; the drink in hand is not.
const BAR_OPEN = [1050, 1380], BAR_PRICE = 2;
const BAR_DRINKS = { tea: { name: 'Tea', short: 'tea' }, juice: { name: 'Juice', short: 'juice' }, fizz: { name: 'Fizz', short: 'fizz' }, cocoa: { name: 'Cocoa', short: 'cocoa' } };
SHIP.player.bar = (() => { const b = SAVED && SAVED.player && SAVED.player.bar; return { last: b && BAR_DRINKS[b.last] ? b.last : null, run: b && Number.isInteger(b.run) && b.run > 0 ? Math.min(b.run, 99) : 0 }; })();
SHIP.player.drink = null;
SAVE_EXTRA.push(s => { (s.player || (s.player = {})).bar = { ...SHIP.player.bar }; });
const barSays = (who, kind, fb, ctx) => { let l = null; try { l = who && typeof lineFor === 'function' && lineFor(who, kind, ctx || {}); } catch (e) { l = null; } let t = l && l.text; if (!t) { try { t = careerText(kind); } catch (e) { t = null; } } t = t || fb; for (const k in ctx || {}) t = t.split('{' + k + '}').join(ctx[k]); return t; };
function barTap(it, at) {
  if (!it || !(it.bar || /^the bar$/i.test(it.t || ''))) return false;
  if (SHIP.player.drink) return false;                   // drink in hand: a tap on the bar is a tap on its stools (15b's ixDrink), open or not
  const m = SHIP.time.min, staff = ['3-bar-1', '3-bar-2'].filter(id => PLACE_OF.has(id)), keeper = staff.map(id => heldBy(id)).find(a => a && a.settled);
  if (m < BAR_OPEN[0] || m >= BAR_OPEN[1] || staff.length && !keeper) { toast(it.t, barSays(null, 'bar.closed', 'Back at 17:30.')); return true; }
  const who = keeper ? keeper.p.id : null, name = keeper ? shortName(keeper.p) : 'The bar';
  const order = () => {
    const B = SHIP.player.bar, ids = Object.keys(BAR_DRINKS), usual = B.run >= 3 && B.last;
    const choices = (usual ? [barSays(who, 'bar.usual', 'The usual? ' + BAR_DRINKS[usual].name + '.', { drink: BAR_DRINKS[usual].short })] : []).concat(ids.map(id => barSays(null, 'bar.drink.' + id, BAR_DRINKS[id].name) + ' (' + BAR_PRICE + ' credits)'));
    const pick = i => {
      const id = usual ? (i === 0 ? usual : ids[i - 1]) : ids[i]; if (!id) return;
      if (SHIP.player.credits < BAR_PRICE) { toast(name, barSays(who, 'bar.broke', 'That\'s ' + BAR_PRICE + ' credits, and you\'re a bit short. Next time.')); return; }
      SHIP.player.credits -= BAR_PRICE; SHIP.player.drink = id; B.run = B.last === id ? B.run + 1 : 1; B.last = id;
      toast(name, barSays(who, 'bar.serve', 'One ' + BAR_DRINKS[id].short + '. Enjoy.', { drink: BAR_DRINKS[id].short }) + ' Take it to a stool.');
    };
    if (typeof deviceChoose === 'function') deviceChoose({ title: name, text: barSays(who, 'bar.ask', 'What\'ll it be?'), choices }, pick); else pick(usual ? 0 : 0);
  };
  if (typeof approach === 'function' && it.front !== undefined) approach(at.clone(), it.front, it.depth, order); else order();
  return true;
}
PLAYER_TAPS.unshift(barTap);
// Gym club (the traditions engineer's renamed Running club, id 'running'): on now, on this ship day
function gymClubOn() {
  if (typeof eventsOn !== 'function') return false;
  const m = SHIP.time.min; try { return eventsOn(SHIP.time.day).some(e => e.id === 'running' && m >= e.from - 10 && m < e.to); } catch (e) { return false; }
}
function hobbyHere() {
  const A = ACT, sat = A && A.kind === 'sit' && A.phase === 'do', pl = sat && A.placeId && PLACE_OF.get(A.placeId);
  const still = !A ? !player.path.length && !player.steer : sat;
  if (!still) return [];
  return Object.keys(HOBBIES).filter(id => { const h = HOBBIES[id]; return h.garden ? false : h.dev ? true : !sat ? false : h.win ? !!(pl && (pl.window || pl.type === 'observatory')) : hobbyHas(id); });
}
// start one: sitting, it takes over the seat (and you sit on after); standing, a device hobby is done where you stand
function hobbyStart(id) {
  const h = HOBBIES[id]; if (!h || !hobbyHere().includes(id)) return false;
  const A = ACT, title = hobbyText('hobby.name.' + id, h.label || h.name), start = hobbyText('hobby.start.' + id, h.doing + '...');
  if (A && A.kind === 'sit' && A.phase === 'do') {
    A.kind = 'hobby'; A.def = { ...PLAYER_ACTS.hobby, title }; A.done = 0; A.pose = h.pose; A.o.hobby = id; A.o.sat = true; A.o.shared = hobbyShare(id);
    toast(title, start + ' About ' + taskMins(A.def.mins) + ' minutes; walk away to stop.');
  } else { actStart('hobby', null, { hobby: id, title, pose: h.stand || h.pose, flavour: start }); if (ACT && ACT.kind === 'hobby') ACT.o.shared = hobbyShare(id); }
  return true;
}
// sharing a hobby (0.28.64, the plan: "sitting near someone who shares the hobby gives a little social and a line"):
// crew settled within HOBBY_NEAR m whose habits (or the systems engineer's p.hobby) match. Once a hobby, as it starts
const HOBBY_HABITS = { garden: ['gardener', 'garden-lover'], read: ['quiet-corner', 'reader'], games: ['common-room', 'gamer'], stars: ['stargazer', 'window-seat'], knit: ['knitter'], draw: ['sketcher'], puzzle: ['puzzler'], write: ['writer'] };
const HOBBY_NEAR = 3.5, HOBBY_SHARE = 3;
const hobbyOf = (p, id) => !!p && (p.hobby === id || (Array.isArray(p.hobbies) && p.hobbies.includes(id)) || (p.habits || []).some(h => (HOBBY_HABITS[id] || []).includes(h)) || id === 'knit' && p.id === INTRO_ESCORT);
function hobbyShare(id) {
  const me = player.obj.position, a = DECK_CREW.find(c => c.settled && c.p && c.p.id && hobbyOf(c.p, id) && Math.hypot(c.x - me.x, c.z - me.z) < HOBBY_NEAR);
  if (!a) return null;
  SHIP.player.needs.social = needClamp(SHIP.player.needs.social + HOBBY_SHARE * needEffects().socialGain * (typeof bondMult === 'function' ? bondMult(a.p.id) : 1));
  let l = null; try { l = typeof lineFor === 'function' && lineFor(a.p.id, 'hobby.share.' + id, {}); } catch (e) { l = null; }
  if (a.h && typeof bubbleSay === 'function') bubbleSay(a.h, l && l.text || 'You too? Nice. Mind if I join you?');
  return a.p.id;
}
function hobbyCount(id) { const H = SHIP.player.hobbies; H.done[id] = (H.done[id] || 0) + 1; H.last[id] = SHIP.time.day; simAct('hobby', { hobby: id }); }   // the Record, and the note bus: the Settling-in list's 'Try a hobby' (0.28.63)
function hobbyUntil(A) {   // the meter's full: counted for the Record; sitting, you sit on
  if (A.done < A.def.mins) return false;
  const id = A.o.hobby, H = SHIP.player.hobbies;
  if (id && !A.o.counted) {
    A.o.counted = true; hobbyCount(id);
    let t = hobbyText('hobby.done.' + id, 'That was nice.');
    const pl = A.placeId && PLACE_OF.get(A.placeId);
    if (id === 'draw' && pl && pl.window) t += ' ' + hobbyText('hobby.drew', 'You sketched the view from the {room}.', { room: ((deckDef.rooms || {})[pl.room] || {}).name || 'window' });   // a nice view (0.28.64)
    if (A.o.sat) toast(A.def.title, t + ' Leisure ' + Math.round(SHIP.player.needs.leisure) + '.'); else A.def.done = t;   // standing, actEnd says it as you put the device away
  }
  if (A.o.sat) { A.kind = 'sit'; A.def = { ...PLAYER_ACTS.sit }; A.pose = 'sit'; A.done = 0; return false; }
  return true;
}
// your job's work at your feet with its parts in hand, while you're free to start it (null: no Repair button)
function handRepair() {
  if (PAUSE.on || (typeof ride !== 'undefined' && ride) || ACT && (ACT.kind === 'ixStop' || ACT.kind === 'job' || ACT.phase === 'do')) return null;
  const h = jobHere(player.obj.position); return h && h.parts ? h : null;
}
function handTick(now) {
  const t = performance.now(); if (!now && t - HAND.at < 250) return; HAND.at = t;
  const el = handEl(), r = document.getElementById('repairBtn'), h = handRepair(), hb = document.getElementById('hobbyBtn');
  const hob = !h && !PAUSE.on && ACT && ACT.kind === 'sit' && ACT.phase === 'do' && hobbyHere().some(id => !HOBBIES[id].dev);   // the Hobby button (0.28.61): sitting, with a prop hobby or a window
  if (hb.hidden !== !hob) hb.hidden = !hob;
  HAND.repair = !!h; if (r.hidden !== !h) r.hidden = !h;
  if (!h && !hob) return;
  // never over Put down (player engineer 8's #putDown, below us, lifts above a toast on phones) or a toast (0.28.55)
  const tops = [innerHeight - 76], pd = document.getElementById('putDown'), tt = document.getElementById('toast');
  if (pd && !pd.hidden) tops.push(pd.getBoundingClientRect().top - 10);
  if (tt && tt.classList.contains('show') && innerWidth <= 720) tops.push(tt.getBoundingClientRect().top - 10 - (pd && !pd.hidden ? 58 : 0));
  const b = Math.round(innerHeight - Math.min(...tops)), key = b + 'px';
  if (HAND.bottom !== key) { HAND.bottom = key; el.style.bottom = b > 76 ? b + 'px' : ''; }   // measured: the safe area is already in it
}
// the Record's words for your hobbies (0.28.63): the head writer's hobby.record.<h>, else by how often and how lately
function hobbyWords() {
  const H = SHIP.player.hobbies, d = SHIP.time.day;
  return Object.keys(HOBBIES).filter(id => (H.done[id] || 0) > 0).sort((a, b) => H.done[b] - H.done[a]).slice(0, 4).map(id => {
    const n = H.done[id], ago = d - (H.last[id] || d), noun = HOBBIES[id].name.toLowerCase();
    let t = null; try { t = careerText('hobby.record.' + id); } catch (e) { t = null; }
    return t && n >= 3 ? t : n >= 6 && ago <= 3 ? 'You make time for ' + noun + ' most days.' : n >= 3 ? 'You enjoy ' + noun + ' now and then.' : 'You\'ve tried ' + noun + '.';
  });
}
// "Ideas for tonight" (0.28.63, the 0.60.7 plan's first evenings): on the device's home screen from 17:00 to 23:00 for
// your first two weeks: the next tradition, someone you know on this deck, a hobby to try, a free booth. Texts: ideas.*
function ideasTonight() {
  const d = SHIP.time.day, m = SHIP.time.min; if (d < 1 || d > 14 || m < 1020 || m >= 1380) return null;
  const T = (k, fb, ctx) => hobbyText(k, fb, ctx), out = [T('ideas.title', 'Ideas for tonight')];
  let tr = null; try { tr = devTraditions(shipNow(), d * 1440 - 1).find(x => x.at >= shipNow() - 15); } catch (e) { tr = null; }
  if (tr) out.push(T('ideas.trad', '{trad} at {time}.', { trad: tr.title, time: devWhen(tr.at) }));
  let fr = null; try { fr = DECK_CREW.filter(a => a.p && a.p.id && ROSTER.some(x => x.id === a.p.id) && typeof relTier === 'function' && relTier(a.p.id) >= 1).sort((a, b) => relTier(b.p.id) - relTier(a.p.id) || (a.p.id < b.p.id ? -1 : 1))[0]; } catch (e) { fr = null; }
  if (fr) out.push(T('ideas.friend', '{name} is about, in the {room}. Talk a while?', { name: shortName(fr.p), room: ((deckDef.rooms || {})[roomAt(...fr.here())] || {}).name || 'deck' }));
  const H = SHIP.player.hobbies, hb = Object.keys(HOBBIES).filter(hobbyHas).sort((a, b) => (H.done[a] || 0) - (H.done[b] || 0) || (a < b ? -1 : 1))[0];
  if (hb) out.push(T('ideas.hobby', 'Try {hobby}: open Hobbies on your device.', { hobby: HOBBIES[hb].name.toLowerCase() }));
  out.push(T('ideas.booth', 'Call home from the booths on Deck 3.'));
  return out.length > 1 ? out : [out[0], T('ideas.none', 'A quiet evening. Sit somewhere nice and try a hobby.')];
}
// the Hobbies app (0.28.63): Read, Write, Play games and (0.72.1) Watch a film on your device, anywhere you're still; the prop hobbies you have
// and how to get the rest. A first-time tooltip (tip.hobby) explains it
deviceApp({ id: 'hobbies', title: 'Hobbies', icon: 'hobby', order: 46,
  view: () => {
    const here = hobbyHere(), dev = ['read', 'write', 'games', 'film'], B = [];
    B.push({ kind: 'text', text: 'Hobbies fill your Leisure: about 30 minutes for a good boost. Walk away to stop; you keep what you got.' });
    B.push({ kind: 'buttons', items: dev.map(id => ({ label: hobbyText('hobby.name.' + id, HOBBIES[id].label || HOBBIES[id].name), action: { app: 'hobbies', do: 'start', arg: id } })) });
    if (!here.length) B.push({ kind: 'text', text: 'Stand still or sit down to start one.', mark: 'down' });
    const props = ['draw', 'knit', 'puzzle', 'stars', 'garden'].map(id => ({ text: hobbyText('hobby.name.' + id, HOBBIES[id].name), sub: id === 'garden' ? 'Tap a bed in the garden on Deck 3, off shift.' : id === 'stars' ? 'Sit at a big window, or in the observatory, and tap Hobby.' : hobbyHas(id) ? 'Yours. Sit anywhere and tap Hobby.' : id === 'knit' ? 'Needles and wool at the crew store, Deck 3. Zeke might teach you.' : HOBBIES[id].prop[0].toUpperCase() + HOBBIES[id].prop.slice(1) + ' at the crew store, Deck 3 (' + HOBBIES[id].price + ' credits).' }));
    B.push({ kind: 'text', text: 'With your own things', mark: 'head' }); B.push({ kind: 'list', rows: props });
    return { title: 'Hobbies', blocks: B };
  },
  act: (verb, arg) => { if (verb === 'start' && HOBBIES[arg]) { if (hobbyStart(arg)) deviceClose(); else toast('Hobbies', 'Stand still or sit down first.'); } } });
// the Hobby button: the one hobby here, or a choice of them (the device's chooser, in its style)
function hobbyPick() {
  const ids = hobbyHere().filter(id => !HOBBIES[id].dev);
  if (ids.length === 1 || typeof deviceChoose !== 'function') { if (ids[0]) hobbyStart(ids[0]); return; }
  deviceChoose({ title: hobbyText('hobby.button', 'Hobby'), text: 'What would you like to do?', choices: ids.map(id => hobbyText('hobby.name.' + id, HOBBIES[id].name)) }, i => { if (ids[i]) hobbyStart(ids[i]); });
}
// at the panel (actBegin): fit the parts you carry, then repair if they're all in, else look it over the first time
function jobBegin(A) {
  const mw = myWork(); if (!mw || A.placeId !== panelPlace(mw.j.machine)) { ACT = null; toast(A.o.title, 'You don\'t have a job here any more.'); return false; }
  const P = SHIP.player, { j, w } = mw, fit = [];
  for (const p of P.carry.slice()) if (jobNeeds(j, w).includes(p)) { w.fitted.push(p); fit.push(p); P.carry.splice(P.carry.indexOf(p), 1); }
  if (fit.length) jobTouch(true);
  const need = jobNeeds(j, w), name = machineName(machineById(j.machine)), fitted = fit.length ? 'You fit ' + partList(fit) + '. ' : '';
  if (!need.length) {
    const ks = typeof jobStops === 'function' ? jobStops(j).findIndex(x => x.step === 'job') : -1, ss = ks >= 0 ? jobStops(j)[ks] : null;
    if (ss && wsHow(ss) !== 'hold') { ACT = null; if (fit.length) toast(A.o.title, fitted); workStep(j, ss, ks, A.spot); return false; }   // the panel's own work step (Pillar 5)
    const left = Math.max(1, jobMins(j) - w.done);
    A.def = { mins: left, pose: 'work', title: 'Repairing' }; A.o.repair = true; w.seen = true;
    A.o.after = fitted + (w.done ? 'Back to the ' + name + ': about ' + taskMins(left) + ' minutes to go.' : 'You set to work on the ' + name + ': about ' + taskMins(left) + ' minutes.') + ' Walk away to pause.';
    return true;
  }
  if (!w.seen) {
    w.seen = true; A.def = { mins: INSPECT_MINS * (j.cause && typeof scanHave === 'function' && scanHave() && typeof toolSlow === 'function' ? toolSlow('scanner') : 1), pose: 'work', title: 'Inspecting' };   // a due scanner: a quarter longer (M11)
    A.o.after = fitted + 'You open the panel on the ' + name + ' and look it over.'; A.o.need = need;
    return true;
  }
  ACT = null; toast(A.o.title, fitted + 'The ' + name + ' still needs ' + partList(need) + '. ' + whereFrom(j, need)); device.refresh();
  return false;
}
// done (actEnd, not walked away): what each step leaves you with
function jobEnd(A) {
  const P = SHIP.player, mw = myWork();
  if (A.kind === 'stow') {
    const back = []; for (const p of P.carry.slice()) if (p !== KIT_BAG && returnPart(p)) { back.push(p); P.carry.splice(P.carry.indexOf(p), 1); }
    toast('Main storage', back.length ? 'You put back ' + partList(back) + '.' : 'Nothing to put back.');
  } else if (A.kind === 'make' && mw && P.work.make) {
    const part = P.work.make.part; P.work.make = null;
    if (P.carry.length < CARRY_MAX) { P.carry.push(part); toast('Machine shop', 'You make ' + partList([part]) + '. ' + (shelfNeeds(mw.j, mw.w, P.carry).length ? 'Now ' + partList(shelfNeeds(mw.j, mw.w, P.carry)) + ' from main storage next door.' : 'Now to the ' + machineName(machineById(mw.j.machine)) + ' on ' + deckIn(mw.j.deck) + '.')); }
    if (part === madeHere(mw.j)) jobStopMark(mw.j, 'make');   // the job's make stop (0.28.24)
  } else if (A.kind === 'fetch' && mw) {
    const need = shelfNeeds(mw.j, mw.w, P.carry), got = [], none = [];
    for (const p of need) {
      if (P.carry.length >= CARRY_MAX) break;
      if (takePart(p)) { P.carry.push(p); got.push(p); } else if (!none.includes(p)) none.push(p);
    }
    const rest = shelfNeeds(mw.j, mw.w, P.carry), toMake = jobNeeds(mw.j, mw.w, P.carry).includes(madeHere(mw.j));
    if (madeHere(mw.j) && got.length && !rest.length) jobStopMark(mw.j, 'fetch');   // the job's fetch stop (0.28.24)
    toast('Main storage', (got.length ? 'You take ' + partList(got) + '.' : 'Nothing you need is on the shelves.')
      + (none.length ? ' None left: ' + none.join(', ') + '. ' + (none.some(p => typeof NO_MAKE !== 'undefined' && !NO_MAKE.has(p)) ? 'The machine shop next door can make one (about an hour at the lathe).' : 'It can\'t be made aboard; the next delivery is on Wednesday.') : '')
      + (rest.length && !none.length ? ' Your hands are full; you\'ll need another trip for ' + partList(rest) + '.' : '')
      + (got.length ? toMake && !rest.length ? ' Now make the ' + mw.j.make + ' in the machine shop next door.' : ' Now to the ' + machineName(machineById(mw.j.machine)) + ' on ' + deckIn(mw.j.deck) + '.' : ''));
  } else if (A.kind === 'job' && mw) {
    const name = machineName(machineById(mw.j.machine));
    if (A.o.repair) {
      if (finishJob(mw.j.id)) { P.work = null; P.credits += JOB_PAY; toast('Job done', 'The ' + name + ' is running sweetly again. That\'s one off the board. +' + JOB_PAY + ' credits.'); }
      else toast('Your job', 'The job isn\'t yours any more.');
    } else if (!(typeof scanOpen === 'function' && scanOpen(mw.j.id))) toast('Inspecting', 'The ' + name + ' needs ' + partList(A.o.need) + '. ' + (P.carry.length && !A.o.need.includes(madeHere(mw.j)) ? '' : whereFrom(mw.j, A.o.need)));
  }
  device.refresh();
}

// ---- the work steps (Pillar 5, foundation 15.1; DEV_NOTES "The work steps"): one runner for a stop whose `how` isn't
// 'hold' (look, choose, turn, wait; 'carry' is the cart and your hands, as before). Started where a stop starts today
// (15b's ixChoreTap, 15's jobBegin); each ends with section 17's jobStepDone(job.id, k, res). A step under way is
// SHIP.player.wsteps = [{ job, k, how, v, at, done }] (saved; one per stop under way, so a wait runs on while you do
// the next stop): walking away pauses a step, coming back carries on ----
const WS_HOW = new Set(['look', 'choose', 'turn', 'wait']);
const WS_POSE = (want, fb) => typeof ACTS !== 'undefined' && ACTS[want] || typeof BASES !== 'undefined' && BASES.has(want) ? want : fb;   // the page's poses, until 8b has them
Object.assign(PLAYER_ACTS, { workStep: { mins: 1, pose: 'work', title: 'Your job' } });
const wsHow = st => st && WS_HOW.has(st.how) ? st.how : 'hold';
const wsFind = (id, k) => SHIP.player.wsteps.find(w => w.job === id && w.k === k) || null;
function wsOf(j, k, how) {                               // the step under way on this stop, or a fresh one (other jobs' go)
  const P = SHIP.player, w = wsFind(j.id, k); if (w && w.how === how) return w;
  P.wsteps = P.wsteps.filter(x => x.job === j.id && x.k !== k).slice(-7);
  const n = { job: j.id, k, how, v: null, at: null, done: 0 }; P.wsteps.push(n); return n;
}
const wsUntil = (w, o) => Number.isFinite(o.until) ? o.until : w.at + (Number.isFinite(o.mins) && o.mins > 0 ? o.mins : 30);
function workWaitAt(id) {                               // the job card's "ready at": the soonest wait of this job under way, or null
  const j = SHIP.jobs.find(x => x.id === id), at = j && typeof jobStops === 'function' ? SHIP.player.wsteps.filter(w => w.job === id && w.how === 'wait' && w.at !== null).map(w => { const st = jobStops(j)[w.k]; return st ? wsUntil(w, st.opts || {}) : null; }).filter(Number.isFinite) : [];
  return at.length ? Math.min(...at) : null;
}
// workStep(job, stop, k, spot?) -> true when it took the tap (false: a 'hold' or 'carry' stop, today's path)
function workStep(j, st, k, spot) {
  const how = wsHow(st); if (how === 'hold' || !j || typeof jobStepDone !== 'function') return false;
  const o = st.opts || {}, w = wsOf(j, k, how), title = o.title || j.title || 'Your job';
  if (!spot) { const pid = st.places && st.places[0]; spot = pid && PLACE_OF.has(pid) ? placeSpot(pid) : null; }
  if (how === 'wait') {                                  // start it, leave, come back
    if (w.at === null) { w.at = shipNow(); toast(title, (o.text || 'Started.') + ' Ready at ' + hhmm(wsUntil(w, o)) + '; come back then.'); device.refresh(); return true; }
    const at = wsUntil(w, o); if (shipNow() < at) { toast(title, 'Not ready yet: ready at ' + hhmm(at) + '.'); return true; }
    wsFinish(j, k, {}, title); return true;
  }
  const secs = (Number.isFinite(o.secs) && o.secs > 0 ? o.secs : 4) * (o.tool && typeof toolSlow === 'function' ? toolSlow(o.tool) : 1), mins = how === 'look' ? secs * SHIP_RATE : 1;   // o.tool: a due tool, a quarter longer (M11)
  actStart('workStep', null, { title, job: j.id, ws: k, how, pose: how === 'look' ? WS_POSE('look', 'stand') : how === 'turn' ? WS_POSE('tune', 'work') : 'work',
    spot: spot ? { ...spot, id: null, pose: 'stand' } : null, after: o.text || (how === 'look' ? 'You stand and look it over.' : '') });
  if (ACT && ACT.kind === 'workStep') {
    ACT.def.title = how === 'look' ? 'Looking' : title;
    if (how === 'look') { ACT.def.mins = Math.max(.05, mins - Math.min(w.done, mins * .95)); ACT.def.real = true; }   // real seconds: needs don't speed a look
    else ACT.def.until = A => wsCard(A);                 // choose / turn: you stay at it until the card is answered
  }
  return true;
}
// choose / turn: the card in the device's style (deviceChoose: 44 px+ buttons), opened once you're there
function wsCard(A) {
  if (A.o.fin) return true; if (A.o.open || ACT !== A) return false;
  const j = myJobAny(A.o.job), st = j && jobStops(j)[A.o.ws]; if (!st) { A.o.fin = true; return true; }
  const o = st.opts || {}, w = wsOf(j, A.o.ws, A.o.how), opts = Array.isArray(o.options) ? o.options.slice(0, 6) : [];
  const close = () => { A.o.open = false; A.o.fin = true; };
  if (A.o.how === 'choose') {
    A.o.open = deviceChoose({ title: o.title || A.o.title, text: o.text || 'Which one?', choices: opts.map(x => x.label) }, i => { close(); if (opts[i]) wsFinish(j, A.o.ws, { pick: opts[i].id }, A.o.title); });
  } else {
    if (w.v === null) w.v = Number.isFinite(o.v) ? o.v : 0;
    const by = Number.isFinite(o.by) && o.by > 0 ? o.by : 1, lo = Number.isFinite(o.min) ? o.min : -Infinity, hi = Number.isFinite(o.max) ? o.max : Infinity;
    const ask = said => {
      const g = typeof o.gauge === 'function' ? o.gauge(w.v) : null;
      A.o.open = deviceChoose({ title: o.label || 'The setting', text: [said, g].filter(Boolean).join(' ') || 'A step at a time; watch the machine.', choices: ['−', '+'], cancel: 'Step back' }, i => {
        A.o.open = false; if (i < 0 || ACT !== A) { close(); return; }
        w.v = Math.max(lo, Math.min(hi, w.v + (i ? by : -by)));
        const t = typeof o.onTurn === 'function' ? o.onTurn(w.v) : null;
        if (typeof o.ok === 'function' && o.ok(w.v)) { close(); wsFinish(j, A.o.ws, { value: w.v }, A.o.title, t); } else ask(t);
      });
    };
    ask(null);
  }
  if (!A.o.open) { close(); toast(A.o.title, 'Your device is busy; try again in a moment.'); }
  return A.o.fin;
}
const myJobAny = id => SHIP.jobs.find(x => x.id === id && x.claimedBy === 'you' && x.status === 'claimed') || null;
// a step's activity is over (actEnd): a look that ran its seconds gives its marks card, or is done; anything else is a pause
function workStepEnd(A, abort) {
  const j = myJobAny(A.o.job), w = j && wsFind(j.id, A.o.ws);
  if (A.o.how !== 'look') { if (A.o.open && typeof devChosen === 'function' && DEV.choose) devChosen(-1); return; }   // walked away from a card: it goes
  if (!w) return;
  w.done += Math.min(A.done, A.def.mins);
  if (abort && A.done < A.def.mins) return;              // walked away: the look so far is kept
  if (A.o.read && typeof traceRead === 'function') { SHIP.player.wsteps = SHIP.player.wsteps.filter(x => x !== w); traceRead(j, A.o.read); device.refresh(); return; }   // 24i's pipe kit (the act's o.read: a machine id): its reading, never jobStepDone
  const st = jobStops(j)[A.o.ws], marks = st && st.opts && Array.isArray(st.opts.marks) ? st.opts.marks.slice(0, 6) : null;
  if (!marks || !marks.length) { wsFinish(j, A.o.ws, {}, A.o.title); return; }
  if (!deviceChoose({ title: st.opts.title || A.o.title, text: [st.opts.text, st.opts.ask || 'How does it look?'].filter(Boolean).join(' '), choices: marks.map(x => x.label) }, i => { if (marks[i]) wsFinish(j, A.o.ws, { pick: marks[i].id }, A.o.title); })) toast(A.o.title, 'Your device is busy; tap it again to mark it.');
}
// the stop is done: section 17 marks it (with the result), and you hear what's next, as for a chore's stop
function wsFinish(j, k, res, title, said) {
  const P = SHIP.player; P.wsteps = P.wsteps.filter(w => !(w.job === j.id && w.k === k));
  const r = jobStepDone(j.id, k, res); if (typeof ixGoalAt !== 'undefined') ixGoalAt = -1;
  if (!r || !r.ok) { toast('Your job', 'The job isn\'t yours any more.'); return; }
  if (r.wrong) { device.refresh(); return; }               // a wrong part: 24k's caseFitted has said so
  if (r.retry) { toast(title, typeof r.say === 'string' && r.say ? r.say : 'Not quite. Try again.'); device.refresh(); return; }   // the kind said no (17's def.veto): the stop stays to do
  toast(r.done ? 'Work done' : title, [said, typeof r.say === 'string' ? r.say : '', r.done ? j.title + ': done. Turn it in at the job board in the Works bay, Deck 5.' : 'Done here. ' + r.left + (r.left === 1 ? ' stop' : ' stops') + ' to go: follow the marker.'].filter(Boolean).join(' '));
  device.refresh();
}
function wstepsLoad(s) {                                // junk, or a step of no job, is dropped; at most 8
  const a = s && s.player && s.player.wsteps; if (!Array.isArray(a)) return [];
  return a.filter(w => w && (typeof w.job === 'string' || typeof w.job === 'number') && WS_HOW.has(w.how) && Number.isInteger(w.k) && w.k >= 0 && w.k < 64).slice(-8)
    .map(w => ({ job: w.job, k: w.k, how: w.how, v: Number.isFinite(w.v) ? +w.v : null, at: Number.isFinite(w.at) ? +w.at : null, done: Number.isFinite(w.done) && w.done > 0 ? Math.min(+w.done, 600) : 0 }));
}
SHIP.player.wsteps = wstepsLoad(SAVED);
SHIP.player.bedMade = Number.isInteger(SAVED && SAVED.player && SAVED.player.bedMade) ? SAVED.player.bedMade : null; SHIP.player.untidy = !!(SAVED && SAVED.player && SAVED.player.untidy === true);
SAVE_EXTRA.push(s => { const p = s.player || (s.player = {}); p.bedMade = SHIP.player.bedMade; p.untidy = !!SHIP.player.untidy; });
SAVE_EXTRA.push(s => { const p = s.player || (s.player = {}); p.wsteps = SHIP.player.wsteps.filter(w => myJobAny(w.job)).map(w => ({ ...w })); });

// ---- playtest 1 (0.28.74, plans/brief-playtest1.md, package P) ----
// a very low need (needWarnTick's firm warning): the marker to the nearest place that fixes it, on this deck if there's
// one, else the nearest deck's. Cleared when you start fixing it, or the need is back up (WARN_REARM)
const NEED_FIX = { hunger: ['servery-queue', 'grab-shelf'], energy: ['bed'], hygiene: ['shower'], bathroom: ['toilet'], fitness: ['gym'], social: ['callhome'], leisure: ['lounge-seat'] };
const NEED_FIX_SAY = { hunger: 'Food', energy: 'Your bunk', hygiene: 'A shower', bathroom: 'A toilet', fitness: 'The gym', social: 'The call booths', leisure: 'Somewhere to sit and unwind' };
let NEED_GOAL = null;                                     // { need, label } while the marker is ours
function needGoal(k) {
  if (!NEED_FIX[k] || typeof setGoal !== 'function' || typeof IX_GOAL === 'undefined' || IX_GOAL && !(NEED_GOAL && IX_GOAL.label === NEED_GOAL.label)) return false;   // never over someone else's arrow
  const bed = typeof playerBed === 'function' ? playerBed() : null, here = typeof deckDef !== 'undefined' && deckDef ? deckDef.num : 4, pos = player.obj.position;
  const ok = pl => k === 'energy' ? pl.id === bed : NEED_FIX[k].includes(pl.type) && !(PRIVATE_TYPES.has(pl.type) && privatePlace(pl));
  const near = pl => pl.deck === here ? Math.hypot(cellPos(...pl.at).x - pos.x, cellPos(...pl.at).z - pos.z) : 1000 * (1 + Math.abs(pl.deck - here));
  const all = Object.keys(DECKS).flatMap(n => (DECKS[n].places || []).map(pl => ({ ...pl, deck: +n }))).filter(ok);
  const pl = all.sort((a, b) => near(a) - near(b) || (a.id < b.id ? -1 : 1))[0]; if (!pl) return false;
  NEED_GOAL = { need: k, label: NEED_FIX_SAY[k] + (pl.deck !== here ? ', ' + deckIn(pl.deck) : '') };
  setGoal({ deck: pl.deck, place: pl.id, label: NEED_GOAL.label }); return true;
}
function needGoalClear() { if (NEED_GOAL && typeof IX_GOAL !== 'undefined' && IX_GOAL && IX_GOAL.label === NEED_GOAL.label) clearGoal(); NEED_GOAL = null; }
function needGoalTick() { if (NEED_GOAL && SHIP.player.needs[NEED_GOAL.need] >= WARN_REARM) needGoalClear(); }
// pushing into someone who can't step aside (settled, leading you, talking: section 10's press-and-hold stops you):
// after PUSH_MS of pushing their way, you get by them for PASS_MS (the user's "push through", playtest 1)
const PUSH_MS = 2000, PASS_MS = 1500; let PUSH = null;   // { who, t0, last, until }
function pushThrough(who, x, z, pos) {
  const s = player.steer, now = performance.now();
  if (PUSH && PUSH.who === who && now < PUSH.until) return true;
  const dx = x - pos.x, dz = z - pos.z, d = Math.hypot(dx, dz);
  if (!s || s.k < .2 || d > .5 || d > 1e-4 && (dx * s.x + dz * s.z) / d < .3) return false;   // not pushing their way
  if (!PUSH || PUSH.who !== who || now - PUSH.last > 300) PUSH = { who, t0: now, last: now, until: 0 };
  PUSH.last = now;
  if (now - PUSH.t0 < PUSH_MS) return false;
  PUSH.until = now + PASS_MS; return true;
}
// sitting down near people (a seat or a meal, with company at hand: sitCompany): a little social, once a ship hour
const SIT_BUMP = 2; let SIT_BUMP_AT = -1e9;
function sitBump(A) {
  const c = sitCompany(A), t = shipNow(); if (!(c > 0) || t - SIT_BUMP_AT < 60) return;
  SIT_BUMP_AT = t; SHIP.player.needs.social = needClamp(SHIP.player.needs.social + SIT_BUMP);
}
// tea and biscuits at 13:00 (the user's: it replaces the Works' 10:30 tea): in the Tea corner on Deck 5 on your shift
// days, 13:00-13:45 (the crew's own tea is section 14's; worksTeaOn(t) when it's there). The tea table's cup of tea is
// then tea and biscuits (a little more food). When you turn a job in while it's out and you haven't had yours, the
// marker points to the Tea corner, with a card to say Keep working (it goes). SHIP.player.teaDay: the day you had it (saved)
const TEA_FROM = 780, TEA_TO = 825, TEA_GOAL = 'Tea and biscuits, in the Tea corner';
function teaOut(t = shipNow()) {
  const d = Math.floor(t / 1440) + 1, m = t - (d - 1) * 1440, shift = typeof playerShiftOn === 'function' ? !!playerShiftOn(d) : weekday(d) < 5;
  if (typeof worksTeaOn === 'function') return shift && !!worksTeaOn(t);   // section 14's crew tea (X, 0.71.1): its times; your shift days
  const W = typeof WORKS_TEA !== 'undefined' && WORKS_TEA && Number.isFinite(WORKS_TEA.at) ? WORKS_TEA : { at: TEA_FROM, until: TEA_TO };   // section 14's crew tea (X, 0.71.1)
  return shift && m >= W.at && m < W.until;
}
function teaHere(A) {                                    // in the Tea corner (Deck 5, room 't'), while tea's out: its tea table, or a seat there
  if (typeof deckDef === 'undefined' || !deckDef || deckDef.num !== 5 || !teaOut()) return false;
  const pl = A && A.placeId && PLACE_OF.get(A.placeId), s = A && A.spot;
  return (pl ? pl.room : s ? roomAt(...cellAt(s.x, s.z)) : null) === 't';
}
function teaBegin(A) {
  A.def = { ...A.def, need: 'hunger', gain: 4, mins: Math.max(6, A.def.mins || 0), title: 'Tea and biscuits',   /* 0.72.5 (playtest 2, item 10): only a little food (was 10) */ done: 'Tea and a biscuit or two. Just the thing.' }; A.o.biscuits = true;
  if (A.kind === 'ixLounge') A.o.pose = 'sit:drink';     // in a seat there: a cup in your hand
  SHIP.player.teaDay = SHIP.time.day; teaDismiss(); if (typeof simNote === 'function') simNote('tea', { day: SHIP.time.day, who: 'you' });
}
const teaHad = (d = SHIP.time.day) => SHIP.player.teaDay === d;   // for section 21's Day 1 tea walk (O5)
const teaGoal = () => teaOut() ? { deck: 5, room: 't', label: TEA_GOAL } : null;
function teaOffer() {
  const P = SHIP.player; if (!teaOut() || teaHad() || typeof setGoal !== 'function' || typeof IX_GOAL === 'undefined' || IX_GOAL) return false;
  if (typeof introTeaLead === 'function' && introTeaLead()) return false;   // Day 1: Zeke leads you there himself (section 21)
  setGoal(teaGoal());
  const say = 'Tea\'s out in the Tea corner on Deck 5, and biscuits. Follow the marker, or keep working.';
  if (!(typeof deviceChoose === 'function' && deviceChoose({ title: 'Tea and biscuits', text: say, choices: ['Off to tea'], cancel: 'Keep working' }, i => { if (i < 0) teaDismiss(); }))) toast('Tea and biscuits', say);
  return true;
}
function teaDismiss() { if (typeof IX_GOAL !== 'undefined' && IX_GOAL && IX_GOAL.label === TEA_GOAL) clearGoal(); }
if (typeof onSim === 'function') onSim('job', n => { if (n && n.step === 'turnin') teaOffer(); });
SHIP.player.teaDay = Number.isInteger(SAVED && SAVED.player && SAVED.player.teaDay) ? SAVED.player.teaDay : null;
SAVE_EXTRA.push(s => { const p = s.player || (s.player = {}); p.teaDay = SHIP.player.teaDay; });

// ---- the cart run (0.28.11, answer 8): a restock job (section 17's kind 'restock', taken on the device) is a hover
// cart you push yourself, the same steps as the crew's jobRun: take a cart from its dock in the Cart bay (Deck 5),
// load it in the cargo hold, unload it in main storage ('stores') or Deck 3's cold store ('meals'), and dock it
// again; then finishJob. Tap anything in each room to do that step. SHIP.player.cart = { job, stage, dock } with
// stage 'empty' (going to the hold), 'full' (loaded), 'done' (unloaded, going back); saved. The cargo hold has nothing
// to tap, so loading and unloading also start on their own when you stop in that room with the cart (cartAuto). ----
const CART_STEP = { empty: 'Load it in the cargo hold on Deck 5.', full: null, done: 'Take it back to its dock in the Cart bay.' };
const placeRoom = id => { const pl = (DECKS[deckOf(id)].places || []).find(q => q.id === id); return pl ? pl.room : null; };
// the places for a step: section 17's jobStops(j) (0.33.16) when it's there, else the same lists here
function cartStops(j, step, ids) { const st = typeof jobStops === 'function' ? (jobStops(j).find(x => x.step === step) || {}).places : null; return st && st.length ? st : ids; }
function cartDest(j) { return j.cargo === 'meals' ? { deck: 3, room: placeRoom('3-cold-1'), ids: ['3-cold-1', '3-cold-2'], name: 'the cold store on Deck 3' } : { deck: 5, room: 'r', ids: ['5-parts-1', '5-parts-2', '5-parts-3', '5-parts-4'], name: 'main storage on Deck 5' }; }
function cartFree(ids) { const q = ids.filter(id => PLACE_OF.has(id) && !heldBy(id)); return q[0] || null; }
function cartTap(it, at) {
  if (!jobsOn() || typeof deckDef === 'undefined') return false;
  const P = SHIP.player, j = myJob(), d = deckDef.num, rm = roomAt(...cellAt(at.x, at.z)), c = P.cart;
  const dockTap = d === 5 && /^cart dock/i.test(it.t), dockId = dockTap ? '5-cart-' + (it.t.match(/\d+/) || [1])[0] : null;
  if (c && (!j || j.id !== c.job)) {                     // the job's gone (dropped, or back on the board): the cart goes back
    if (!dockTap) return false;
    actStart('cartBack', PLACE_OF.has(dockId) ? dockId : null, { title: it.t, after: 'You dock the cart and plug it in to charge.' });
    return true;
  }
  if (!j || j.kind !== 'restock') return false;
  if (!c) {
    if (!dockTap) return false;
    if (P.carry.length) { toast(it.t, 'Your hands are full (' + partList(P.carry) + '). ' + handsFix('Put them back in main storage first') + '.'); return true; }
    const out = typeof cartsOut === 'function' ? cartsOut(shipNow()) : new Set();
    if (out.has(+dockId.split('-').pop())) { toast(it.t, 'That cart\'s out on a run. Try the other dock.'); return true; }
    actStart('cartTake', PLACE_OF.has(dockId) ? dockId : null, { title: it.t, dock: dockId, after: 'You unplug the cart and float it out of the dock.' });
    return true;
  }
  if (cartStep(j, c, d, rm, it.t)) return true;
  const dest = cartDest(j);
  if (dockTap && c.stage === 'done') { actStart('cartBack', PLACE_OF.has(dockId) ? dockId : null, { title: it.t, after: 'You dock the cart and plug it in to charge.' }); return true; }
  if (dockTap) { toast(it.t, 'You\'ve got a cart already. ' + (CART_STEP[c.stage] || 'Take the load to ' + dest.name + '.')); return true; }
  return false;
}
// load in the hold, unload where it's going: from a tap there, or on its own when you stop in that room with the cart
function cartStep(j, c, d, rm, title) {
  if (c.stage === 'empty' && d === 5 && rm === placeRoom('5-hold-1')) {
    actStart('cartLoad', cartFree(cartStops(j, 'load', ['5-hold-1', '5-hold-2'])), { title: title || 'Cargo hold', after: 'You load the cart: ' + (j.cargo === 'meals' ? 'crates of meals for the cold store.' : 'the delivery for the shelves.') });
    return true;
  }
  const dest = cartDest(j);
  if (c.stage === 'full' && d === dest.deck && rm === dest.room) {
    actStart('cartUnload', cartFree(cartStops(j, 'unload', dest.ids)), { title: title || 'Unloading', after: 'You unload the cart and shelve it all.' });
    if (ACT && ACT.kind === 'cartUnload' && j.cargo !== 'meals') ACT.def.mins = 10;   // it unloads itself (0.33.42; 20 before)
    return true;
  }
  return false;
}
function cartAuto() {                                    // each ship minute (playerUpdate): standing still in the right room
  const P = SHIP.player, c = P.cart; if (!c || ACT || player.path.length || player.steer || !jobsOn() || typeof deckDef === 'undefined') return;
  const j = myJob(); if (!j || j.id !== c.job) return;
  cartStep(j, c, deckDef.num, roomAt(...player.here()), null);
}
function cartEnd(A) {
  const P = SHIP.player, j = jobsOn() ? myJob() : null;
  if (A.kind === 'cartTake' && j) { P.cart = { job: j.id, stage: 'empty', dock: A.o.dock || '5-cart-1' }; touchJob(j.id); toast('Cart bay', 'The cart hums along at hip height. ' + CART_STEP.empty); }
  else if (A.kind === 'cartLoad' && P.cart && j && j.cargo === 'stores' && typeof cartLoadHold === 'function') {   // the delivery's crates (section 17, 0.33.42)
    const n = cartLoadHold(j.id); P.cart.stage = 'full'; touchJob(j.id);
    toast('Cargo hold', (n ? 'The cart pulls in ' + n + (n === 1 ? ' crate' : ' crates') + ' by itself.' : 'Loaded.') + ' Now to main storage on Deck 5: tap any shelf.');
  }
  else if (A.kind === 'cartLoad' && P.cart && j) { P.cart.stage = 'full'; touchJob(j.id); toast('Cargo hold', 'Loaded. Now to ' + cartDest(j).name + '.'); }
  else if (A.kind === 'cartUnload' && P.cart && j && j.cargo === 'stores' && typeof cartUnloadShelves === 'function') {   // every part onto its own shelf
    const r = cartUnloadShelves(j.id); P.cart.stage = r.left ? 'empty' : 'done';
    toast('Unloaded', 'The cart unloads itself: ' + r.parts + ' parts, each onto its own shelf. ' + (r.left ? r.left + (r.left === 1 ? ' crate is' : ' crates are') + ' still in the cargo hold: one more trip.' : CART_STEP.done));
  }
  else if (A.kind === 'cartUnload' && P.cart && j) {
    P.cart.stage = 'done'; touchJob(j.id);
    const h = +String(j.id).split('@')[1];               // a meals run's food lands in the cold store now (section 16; safe to call twice)
    const n = j.cargo === 'meals' && typeof galleyCartLand === 'function' && isFinite(h) ? galleyCartLand(h) : 0;
    toast('Unloaded', (n ? n + ' meals into the cold store. ' : 'All shelved. ') + CART_STEP.done);
  }
  else if (A.kind === 'cartBack') {
    const done = P.cart && j && P.cart.job === j.id && P.cart.stage === 'done'; P.cart = null;
    if (done && finishJob(j.id)) { P.credits += JOB_PAY; toast('Job done', 'Cart docked, run done. That\'s one off the board. +' + JOB_PAY + ' credits.'); }
    else toast('Cart bay', 'Cart docked.');
  }
  device.refresh();
}
function cartLoad(s) {
  const c = s && s.player && s.player.cart;
  return c && (typeof c.job === 'string') && ['empty', 'full', 'done'].includes(c.stage) ? { job: c.job, stage: c.stage, dock: typeof c.dock === 'string' ? c.dock : '5-cart-1' } : null;
}
SHIP.player.cart = cartLoad(SAVED);
SAVE_EXTRA.push(s => { const p = s.player || (s.player = {}); p.cart = SHIP.player.cart && { ...SHIP.player.cart }; });

// ---- the device: its screens (Home, Needs, Mail, Wallet and the rest) are section 19's apps (0.35.0) ----

