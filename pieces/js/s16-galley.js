// =====================================================================
// 16. GALLEY & FOOD
// The galley really cooks (Pillar 2, workstream A4). Three parts, all worked out from ship time alone:
//  - The rota. galleyDay(person, day) gives a galley worker's day: when they rise, how late they may go to bed
//    before an early start, their work blocks at the galley's stations, and when they eat. Chef Brennan rises
//    about 04:30 and cooks breakfast before 06:00, and dinner from 14:30; her deputy cooks on her days off. The
//    hands work an early shift (05:30-13:30) or a late one (13:00-21:15). The schedules (section 14) ask for it;
//    it never asks them, so there's no loop.
//  - The food. SHIP.galley, stepped a ship minute at a time (galleyAdvance) whatever deck you're on: meals in the
//    cold store, pots cooking, portions in the servery, the grab-and-go shelf, plates dirty and in use, anyone
//    waiting. The cooks cook to the numbers the crew's plans (planDay) say will eat; the crew take a portion when
//    they reach the front of the queue and bring the plate back when they've eaten; the hands wash up.
//  - What you see on Deck 3: food in the servery's pans, the grab shelf, dirty plates at the dish pit.
// For other sections: takePortion(who) (the player eats), galleyJoin(who) / galleyTurn(who) (the player queues), galleyHold(person, t) (someone waiting at the servery),
// galleySave() / galleyLoad(obj) (the save), galleyText(what) (tap text), galleyReport(day, days) (food_check.py).
// Nothing here calls R().
// =====================================================================
// ---- the rota ----
// a galley worker's team: ROSTER's galley field ('chef'; 'cook' for the chef's deputy; 'hand', who take early and late
// shifts by turns), or rota.team ('chef', 'early', 'late', with rota.cover: { for } on the deputy); without either,
// the chef by role
const galleyStaff = () => ROSTER.filter(p => p.dept === 'galley' && p.work && p.work.deck === 3);
const galleyTeam = p => (p.rota && p.rota.team) || (p.galley === 'chef' || /^chef\b/i.test(p.role || '') ? 'chef' : null);
const galleyDeputy = (p, head) => p.galley === 'cook' || !!(p.rota && p.rota.cover && (!head || p.rota.cover.for === head.id));
// the stations, by job: work:galley places on Deck 3, in the order they're tried
const GALLEY_AT = {
  cook: ['3-galley-1', '3-galley-4', '3-galley-2', '3-galley-5', '3-galley-3'],   // ranges, ovens, ranges, prep island, ranges
  bake: ['3-galley-4', '3-galley-6'],                                              // the ovens, the prep island's far side
  prep: ['3-galley-5', '3-galley-6'],                                              // the prep island
  serve: ['3-galley-pass'],                                                        // the pass, behind the servery
  wash: ['3-galley-7'],                                                            // the dish pit
  clean: ['3-galley-6', '3-galley-2', '3-galley-5', '3-galley-3'],
  tea: ['3-galley-8'],                                                             // Brennan's stool
  bar: ['3-bar-1', '3-bar-2'],                                                     // behind the bow lounge bar (0.36.88; DECKS[3].bar)
};
const GALLEY_NEXT = { cook: 'prep', bake: 'prep', serve: 'wash', wash: 'clean', prep: 'clean', tea: 'clean' };   // when every station for a job is taken
// each role's day, in minutes of the day: [from, to, task]. 'line' is serving and washing up by turns;
// 'breakfast' and 'dinner' are the staff's own meals
const GALLEY_SHIFTS = {
  chef: { wake: 270, plan: [[290, 540, 'cook'], [540, 560, 'breakfast'], [560, 630, 'clean'], [870, 990, 'cook'], [990, 1010, 'dinner'], [1010, 1230, 'cook'], [1230, 1245, 'tea']] },
  early: { wake: 305, plan: [[330, 360, 'bake'], [360, 540, 'line'], [540, 560, 'breakfast'], [560, 630, 'wash'], [630, 690, 'bake'], [690, 780, 'prep'], [780, 810, 'clean']] },   // breakfast served to 09:00 (0.71.1)
  late: { wake: null, plan: [[780, 870, 'prep'], [870, 990, 'cook'], [990, 1010, 'dinner'], [1010, 1230, 'line'], [1230, 1275, 'wash']] },
  bar: { wake: null, plan: [[900, 1020, 'prep'], [1020, 1045, 'dinner'], [1050, 1380, 'bar']] },   // bar duty 17:30-23:00 (plan-0607), ended in time for an early start
};
// who does what on a day: the chef (Brennan, else her deputy, else the first hand on duty), then the hands on
// duty by turns, late first, so there's always one on each shift
function galleyRoles(d) {
  const on = galleyStaff().filter(p => isWorkDay(p, d)).sort((a, b) => a.id < b.id ? -1 : 1), roles = new Map();
  const head = galleyStaff().find(p => galleyTeam(p) === 'chef');
  const chef = on.find(p => p === head) || on.find(p => galleyDeputy(p, head)) || on[0];
  if (chef) roles.set(chef.id, 'chef');
  const hands = on.filter(p => p !== chef), fixed = hands.filter(p => ['early', 'late', 'bar'].includes(galleyTeam(p)));
  for (const p of fixed) roles.set(p.id, galleyTeam(p));
  const rest = hands.filter(p => !fixed.includes(p)), r = rest.length ? ((d % rest.length) + rest.length) % rest.length : 0;
  rest.slice(r).concat(rest.slice(0, r)).forEach((p, k) => roles.set(p.id, k % 2 ? 'early' : 'late'));
  // the bar (0.36.91, the user's: one named bartender): rota.team 'bar' (Ivo Madsen) works it every evening he's on;
  // on his days off the relief (rota.relief 'bar', Tamsin Haddad) does her own shift and the bar after it
  // (roles.relief). Whoever's left keeps the galley going: with no late hand, the last early hand turns late
  const of = r => [...roles].filter(([, x]) => x === r).map(([id]) => id);
  if (!of('bar').length) { const rl = hands.find(p => p.rota && p.rota.relief === 'bar'); if (rl) roles.relief = rl.id; }
  if (!of('late').length) { const er = of('early').filter(id => id !== roles.relief); if (er.length > 1) roles.set(er[er.length - 1], 'late'); }
  return roles;
}
const BARTENDER = () => ROSTER.find(p => p.rota && p.rota.team === 'bar') || null, BAR_RELIEF = () => ROSTER.find(p => p.rota && p.rota.relief === 'bar') || null;   // who's on the bar (0.36.91; for section 15's bar)
const galleyWake = (p, d, role) => { const s = GALLEY_SHIFTS[role]; return s && s.wake !== null ? s.wake - 5 + Math.round(10 * schedU(p.seed, d, 301)) : null; };
// the whole galley's day: everyone's blocks, cut into 15-30 minute stints that move between stations, with no
// station held by two people at once
const GALLEY_ROTA = new Map();
function galleyRota(d) {
  if (GALLEY_ROTA.has(d)) return GALLEY_ROTA.get(d);
  const roles = galleyRoles(d), next = galleyRoles(d + 1), out = new Map(), busy = new Map();
  const have = new Set((DECKS[3].places || []).map(p => p.id));
  const isFree = (id, a, b) => !(busy.get(id) || []).some(([x, y]) => x < b && a < y);
  const take = (task, a, b, k) => {                      // the first free station for the job (or the next job), from the k-th
    for (let t = task; t; t = GALLEY_NEXT[t]) {
      const l = GALLEY_AT[t].filter(id => have.has(id));
      for (let i = 0; i < l.length; i++) { const id = l[(k + i) % l.length]; if (isFree(id, a, b)) { if (!busy.has(id)) busy.set(id, []); busy.get(id).push([a, b]); return [id, t]; } }
    }
    return [null, task];
  };
  const order = galleyStaff().slice().sort((a, b) => ['chef', 'early', 'late', 'bar'].indexOf(roles.get(a.id)) - ['chef', 'early', 'late', 'bar'].indexOf(roles.get(b.id)) || (a.id < b.id ? -1 : 1));
  let n = 0;
  for (const p of order) {
    const role = roles.get(p.id) || null, nr = next.get(p.id), nw = nr ? galleyWake(p, d + 1, nr) : null;
    const day = { role, wake: role ? galleyWake(p, d, role) : null, bedBy: nw !== null ? nw + 1440 - 415 : null, blocks: [], meals: {} };
    if (role) {
      const me = n++;
      const cap = day.bedBy !== null ? day.bedBy - 25 : 1440, plan = galleyPlan(role, d).slice();   // (a copy: the relief adds to it) bar duty ends in time for bed before an early start
      if (roles.relief === p.id) { const end = Math.max(...plan.map(x => x[1])); plan.push([Math.max(1050, end + 30), 1380, 'bar']); day.relief = true; }   // the relief: the bar after their own shift
      for (const [a, B, task] of plan) {
        const b = task === 'bar' ? Math.min(B, cap) : B; if (b <= a) continue;
        if (task === 'breakfast' || task === 'dinner') { day.meals[task] = [a, b]; continue; }
        for (let s = a, k = 0; s < b; k++) {             // stints of 15-30 minutes; the line swaps every half hour
          let e = task === 'line' ? s + 30 : s + 15 + Math.round(15 * schedU(p.seed, d, 310 + s));
          if (b - e < 10) e = b;
          const job = task === 'line' ? ((me + k) % 2 ? 'wash' : 'serve') : task;
          const [placeId, did] = take(job, s, e, me + k);
          const l = day.blocks[day.blocks.length - 1];
          if (l && l.placeId === placeId && l.task === did && l.to === s) l.to = e; else day.blocks.push({ from: s, to: e, placeId, task: did });
          s = e;
        }
      }
    }
    out.set(p.id, day);
  }
  GALLEY_ROTA.set(d, out);
  for (const k of GALLEY_ROTA.keys()) if (k < d - 3 || k > d + 3) GALLEY_ROTA.delete(k);
  return out;
}
// the hook for the schedules: a galley worker's day (null for anyone else), in minutes of the day
function galleyDay(person, d) { return person.dept === 'galley' ? galleyRota(d).get(person.id) || null : null; }

// ---- the food ----
// SHIP.galley = { at, cold: { meals }, servery: { portions, dish }, grab: { items }, dirty, inUse, pots, wait, back }
//   at: the next ship minute to work out; cold.meals: meal units in the cold store (one makes a portion or a grab item);
//   pots: [[minutes left, portions, 'hot' | 'grab'], ...] cooking; wait: [[id, since, kind, meal, place, eat], ...]
//   people waiting for food; back: [[minute, plates], ...] plates coming back to the dish pit
const FOOD = {
  batch: 10, cookT: 20,                   // a pot: 10 portions, 20 minutes of a cook's time
  bake: 8, bakeT: 15,                     // a tray for the grab shelf: 8 items, 15 minutes
  serveryCap: 50, grabCap: 16,            // what the hot line (5 pans of 10) and the shelf hold
  tastes: 4,                              // tastes from one meal unit (the tasting table)
  feastCap: 40,                           // more held warm for a meal tradition, whose diners all sit down at once (the Sunday long table)
  coldCap: 300, deliverAt: 630,           // the cold store holds under two days' food; topped up daily at 10:30...
  restock: 'carts',                       // ...while this is 'rule'. 'carts': section 17's hover carts bring it (B3; the
                                          // top-up stays on until cartClaim exists, so a build without section 17 still eats)
  plates: 110, washRate: 3,               // plates aboard; plates a minute through the dish machine
  open: { breakfast: 360, dinner: 1020 }, // the serving windows open (section 14's MEALS)...
  serveTo: { breakfast: 540, dinner: 1230 }, // ...and end (a tradition's `until` can keep breakfast going: galleyServeEnd)
  lead: 70,                               // ...and hot pots start at most this long before
  close: { breakfast: 570, dinner: 1245 },// leftovers go to the grab shelf (the rest is wasted); later by as much as serving runs on
  slack: 3, grabSlack: 4,                 // a few more than the plans need (you, for one)
  giveUp: 30,                             // minutes after the close that anyone still waiting gives up
  spoilDay: .25,                          // the share of the cold store that goes off in a day with its chiller broken (without chillerAt)
  binAt: [540, 1260], binOut: 630,        // spoiled food is binned at the 09:00 and 21:00 checks; the bin goes at 10:30
  trayAt: 1080,                           // an event's trays for the bridge go up at 18:00
  rushRate: 1, slowOven: 1.75,             // in a rush the line serves this many a minute; a slow oven's pots take this much longer
};
// the menu (answer 10): a week's cycle. Breakfasts by weekday. Dinners on Monday, Tuesday, Thursday and Saturday from
// `cycle`, moving on four dishes a week; Wednesday is a crew member's favourite (someone different each week);
// Friday is the treat, with a pudding; Sunday is the dish the crew voted for (galleyMenu). No dish name has a full stop
// in it (the player's section reads "Serving: <dish>.").
const MENU = {
  breakfast: ['porridge and eggs', 'Brennan\'s spiced beans', 'eggs and garden greens', 'oat bake and yoghurt', 'eggs on toast', 'pancakes and fruit', 'the big Sunday fry'],   // pancakes on Saturday, for the long breakfast
  cycle: ['Brennan\'s spiced lentils', 'fish pie', 'noodle soup', 'roast roots and grains', 'curry and rice', 'dumplings and greens', 'chilli and cornbread', 'mushroom risotto', 'shepherd\'s pie'],
  treat: ['pizza night', 'fish and chips', 'burger night', 'tacos'],
  pudding: ['sticky toffee pudding', 'apple crumble', 'chocolate cake', 'ice cream sundaes'],
  // what the crew like best (a ROSTER `favourite` wins; otherwise one of these, from the person's seed)
  fav: ['curry and rice', 'fish pie', 'Sunday roast', 'noodle soup', 'pizza night', 'dumplings and greens', 'chilli and cornbread', 'mushroom risotto', 'Brennan\'s spiced lentils', 'shepherd\'s pie', 'fish and chips', 'tacos'],
};
const galleyFirst = p => { const w = p.name.split(' '); return /^(Dr\.|Chef)$/.test(w[0]) ? w[0] + ' ' + w[w.length - 1] : w[0]; };
const galleyFav = (p, k = 0) => k === 0 && p.favourite ? p.favourite : MENU.fav[Math.floor(schedU(p.seed, 0, 920 + k) * MENU.fav.length)];
// ---- the traditions (Pillar 4): what a tradition asks of the galley, from section 18's tradTies('galley', d) (pure:
// [{ id, name, from, to, tie }]), folded by meal: galleyTies(d) -> { breakfast?, dinner? }, each { ids, dish, until,
// side, extra, batch, honorees }. dish: one of GALLEY_TRAD_DISH, or a dish's name (dashes for spaces); until: 'hh:mm',
// serving runs on to then (the long breakfast); side and extra: the tasting table's. {} on most days, and without section 18
const GALLEY_TRAD_DISH = { pancakes: 'pancakes, fruit and syrup', 'harvest-supper': 'the harvest supper, all from the garden' };
const GALLEY_TIES = new Map();
// the day caches that read section 18 (ties, menus, tastings, the rota and its events) start again when its events
// change (section 14's evSig, as shipDay does: a one-off booked for a day already worked out); menus also when a vote is cast
let GALLEY_SIG = null, GALLEY_VSIG = null;
function galleyFresh() {
  const s = typeof evSig === 'function' ? evSig() : '', v = SHIP.events && SHIP.events.votes ? JSON.stringify(SHIP.events.votes) : '';
  if (s !== GALLEY_SIG) { GALLEY_SIG = s; GALLEY_TIES.clear(); GALLEY_MENU.clear(); GALLEY_TASTE.clear(); GALLEY_ROTA.clear(); GALLEY_EV.clear(); }
  if (v !== GALLEY_VSIG) { GALLEY_VSIG = v; GALLEY_MENU.clear(); }
}
function galleyTies(d) {
  galleyFresh();
  // section 18 makes a day's events again when they change (a one-off booked, the arrival day set: its eventsOn(d) is
  // another list); then this day's ties, tasting, rota and day events, and the menus, are worked out again (reviewer 1)
  const src = !GALLEY_TEST.tradTies && typeof eventsOn === 'function' ? eventsOn(d).map(e => e.id + '@' + e.from + '-' + e.to).join() : null, had = GALLEY_TIES.get(d);   // by content: a list made again the same changes nothing
  if (had && had.src !== src) { GALLEY_TIES.delete(d); GALLEY_TASTE.delete(d); GALLEY_ROTA.delete(d); GALLEY_EV.delete(d); GALLEY_MENU.clear(); }
  else if (had) return had.out;
  const f = GALLEY_TEST.tradTies || (typeof tradTies === 'function' ? tradTies : null), out = {};
  for (const x of (f && f('galley', d)) || []) {
    const t = x.tie && typeof x.tie === 'object' ? x.tie : {}, o = out[t.meal === 'breakfast' ? 'breakfast' : 'dinner'] || (out[t.meal === 'breakfast' ? 'breakfast' : 'dinner'] = { ids: [] });
    o.ids.push(x.id);
    if (t.extra === 'tasting' && !o.taste) {             // the tasting table: when, and its tally's choices (section 18's tally tie)
      const tl = ((f && f('tally', d)) || []).find(y => y.id === x.id);
      o.taste = { id: x.id, from: x.from, to: x.to, choices: tl && tl.tie && Array.isArray(tl.tie.choices) ? tl.tie.choices : [] };
    }
    for (const k of ['dish', 'until', 'side', 'extra', 'batch']) if (t[k] != null && o[k] == null) o[k] = t[k];
    if (t.dish === 'favourite' && !o.honorees) { const e = x.honorees ? x : typeof eventsOn === 'function' ? eventsOn(d).find(e => e.id === x.id) : null; o.honorees = e && e.honorees || []; }
  }
  GALLEY_TIES.set(d, { out, src }); for (const k of GALLEY_TIES.keys()) if (k < d - 8 || k > d + 8) GALLEY_TIES.delete(k);
  return out;
}
// when a meal's serving ends on day d (minutes of the day): FOOD.serveTo, or later for a tradition's `until`; and when
// its line closes (leftovers to the grab shelf), as much later
function galleyServeEnd(d, meal) {
  const u = (galleyTies(d)[meal] || {}).until, h = typeof u === 'string' && /^(\d\d?):(\d\d)$/.exec(u), v = h ? +h[1] * 60 + +h[2] : typeof u === 'number' ? u : 0;
  return Math.max(FOOD.serveTo[meal], Math.min(v, meal === 'breakfast' ? 690 : 1380));
}
const galleyClose = (d, meal) => FOOD.close[meal] + galleyServeEnd(d, meal) - FOOD.serveTo[meal];
// a long breakfast's morning (the chef cooks on to half an hour before the end, the early hand serves to the end, then
// both eat and clean up); the rest of the day as usual
function galleyPlan(role, d) {
  const P = GALLEY_SHIFTS[role].plan, x = galleyServeEnd(d, 'breakfast') - FOOD.serveTo.breakfast;
  if (!x || (role !== 'chef' && role !== 'early')) return P;
  const head = role === 'chef' ? [[290, 510 + x, 'cook'], [510 + x, 530 + x, 'breakfast'], [530 + x, 600 + x, 'clean']] : [[330, 360, 'bake'], [360, 540 + x, 'line'], [540 + x, 560 + x, 'breakfast'], [560 + x, 630 + x, 'wash']];
  const end = head[head.length - 1][1];
  return head.concat(P.filter(b => b[1] > end && b[0] >= (role === 'chef' ? 660 : 0)).map(b => [Math.max(b[0], end), b[1], b[2]]));
}
// Brennan's tasting table (a dinner tie with extra: 'tasting', Wednesdays 18:15): two tastes for each taster coming (at least the tie's `batch`, 20) of two small
// dishes, cooked from an hour before (the garden's produce first) and set out at the servery's end while it runs. The
// vote is section 18's tally (one vote engine): tallyOf(id, d) says which two dishes and how the votes stand, and your
// token is its tallyVote. Without it, the next two of the tie's tally choices (two a week) and no vote.
// galleyTasting(d) -> null | { id, from, to, tastes, keys, choices, voters: [{ id, at }], votes, you, win, winner }:
// voters are who comes to taste (everyone whose plan has a segment tagged ev-<id>), and when; winner null without a tally
const GALLEY_TASTE = new Map();
function galleyTasting(d) {
  const T = galleyTies(d).dinner, tt = T && T.taste; if (!tt) return null;
  let o = GALLEY_TASTE.get(d);
  if (!o) {
    const voters = [], tag = 'ev-' + tt.id;
    for (const p of schedPeople().slice().sort((a, b) => a.id < b.id ? -1 : 1)) {
      const s = planDay(p, d).find(s => s.tag && (s.tag === tag || s.tag.startsWith(tag + '-')));
      if (s) voters.push({ id: p.id, at: Math.floor(s.from) });
    }
    o = { id: tt.id, from: tt.from, to: tt.to, tastes: Math.max(Math.round(galleyEvNum(T.batch, 20)), 2 * voters.length), voters };   // two each for everyone coming (the lead's call), at least the tie's batch
    GALLEY_TASTE.set(d, o); for (const k of GALLEY_TASTE.keys()) if (k < d - 10 || k > d + 10) GALLEY_TASTE.delete(k);
  }
  const r = typeof tallyOf === 'function' ? tallyOf(o.id, d) : null, label = c => String(c).replace(/-/g, ' ');
  let keys;
  if (r && r.choices.length) keys = r.choices.slice(0, 2);
  else { const L = tt.choices.length >= 2 ? tt.choices : ['herb-flatbread', 'pickled-beans'], w = Math.floor((d - 1) / 7); keys = [L[(2 * w) % L.length], L[(2 * w + 1) % L.length]]; }
  const votes = keys.map(k => r && r.counts ? r.counts[k] || 0 : 0), win = r && r.winner != null ? Math.max(0, keys.indexOf(r.winner)) : null;
  return { ...o, keys, choices: keys.map(label), votes, you: r && r.you != null && keys.includes(r.you) ? keys.indexOf(r.you) : null, win, winner: win === null ? null : label(keys[win]) };
}
// your token at the tasting table: section 18's tallyVote (choice 0 or 1, a key or a name); true when counted. You try
// both (two tastes, if there are any left). The tap or device button that offers it is someone else's
function galleyVote(choice) {
  const d = SHIP.time.day, o = galleyTasting(d); if (!o || typeof tallyVote !== 'function') return false;
  const k = choice === 0 || choice === 1 ? choice : o.keys.indexOf(choice) >= 0 ? o.keys.indexOf(choice) : o.choices.indexOf(choice);
  if (k < 0 || o.you !== null || !tallyVote(o.id, o.keys[k])) return false;
  const S = galleyAdvance(shipNow());
  if (S.tasting && S.tasting.d === d && S.tasting.out) S.tasting.left = Math.max(0, S.tasting.left - 2);
  GALLEY_MENU.clear(); return true;
}
// a day's menu: { breakfast, dinner, note, pudding, fav: person, votes: [[dish, n], ...] }. Sunday's vote: everyone
// aboard votes for their favourite, or their second choice if the favourite was on this week's menu; about one in
// four doesn't bother. The most votes wins (ties: the earlier in MENU.fav).
const GALLEY_MENU = new Map();
function galleyMenu(d) {
  galleyTies(d);                                         // (fresh: drops this day's menu when its events changed)
  if (GALLEY_MENU.has(d)) return GALLEY_MENU.get(d);
  const wd = weekday(d), w = Math.floor((d - 1) / 7), C = MENU.cycle, out = { breakfast: MENU.breakfast[wd], dinner: '', note: '' };
  const ppl = schedPeople().slice().sort((a, b) => a.id < b.id ? -1 : 1), regular = k => C[(w * 4 + k) % C.length];
  if (wd === 2 && ppl.length) {                          // a favourite that isn't on the menu already this week
    const p = ppl[(w * 5) % ppl.length], on = [0, 1, 2, 3].map(regular).concat(MENU.treat[w % MENU.treat.length]);
    const pick = [galleyFav(p), galleyFav(p, 1), ...MENU.fav].find(x => !on.includes(x)) || galleyFav(p);
    out.fav = p.id; out.dinner = pick; out.note = `${galleyFirst(p)}'s ${pick === galleyFav(p) ? 'favourite' : 'pick'}`;
  } else if (wd === 4) {
    out.dinner = MENU.treat[w % MENU.treat.length]; out.pudding = MENU.pudding[w % MENU.pudding.length]; out.note = `Friday treat, with ${out.pudding}`;
  } else if (wd === 6) {
    const week = [0, 1, 2, 3].map(regular).concat(MENU.treat[w % MENU.treat.length]), n = new Map();
    for (const p of ppl) {
      if (schedU(p.seed, w, 930) < .25) continue;
      const a = galleyFav(p), b = galleyFav(p, 1), v = week.includes(a) && !week.includes(b) ? b : a;
      n.set(v, (n.get(v) || 0) + 1);
    }
    out.votes = [...n].sort((x, y) => y[1] - x[1] || MENU.fav.indexOf(x[0]) - MENU.fav.indexOf(y[0]));
    out.dinner = out.votes.length ? out.votes[0][0] : 'Sunday roast';
    out.note = out.votes.length ? `voted for by the crew, ${out.votes[0][1]} votes` : '';
  } else out.dinner = regular([0, 1, , 2, , 3][wd]);
  // a harvest morning in the garden (section 18's eventsOn, id 'harvest'): fresh salad with dinner
  if (typeof eventsOn === 'function' && eventsOn(d).some(e => e.id === 'harvest')) { out.salad = true; out.note = (out.note ? out.note + ', ' : '') + 'with fresh garden salad'; }
  // the traditions' dishes (galleyTies): a long breakfast's pancakes; the suppers' dinners; a leaver's favourite
  const T = galleyTies(d), dish = v => GALLEY_TRAD_DISH[v] || String(v).replace(/-/g, ' '), add = n => { out.note = out.note ? out.note + ', ' + n : n; };
  if (T.breakfast && T.breakfast.dish) out.breakfast = dish(T.breakfast.dish);
  if (T.breakfast && galleyServeEnd(d, 'breakfast') > FOOD.serveTo.breakfast) out.bnote = 'long breakfast, to ' + hhmm(galleyServeEnd(d, 'breakfast'));
  const dt = T.dinner && T.dinner.dish;
  if (/^crossover/.test(dt || '')) add('and pancakes for the night shift, whose breakfast it is');   // the crossover supper: both meals at once
  else if (dt === 'first-fruits') add('and the first fruits of the new beds on every table');
  else if (dt === 'harvest-supper') { out.dinner = dish(dt); out.note = 'long tables, and a harvest pie after'; }
  else if (dt === 'favourite') {
    const h = (T.dinner.honorees || []).filter(p => p && p.seed !== undefined);
    if (h.length) { out.dinner = galleyFav(h[0]); out.note = `${galleyNames(h)}'s favourite, for the farewell`; }
    else { out.dinner = MENU.treat[w % MENU.treat.length]; out.note = 'a farewell supper'; }
  } else if (dt) out.dinner = dish(dt);
  if (dt === 'first-fruits' || dt === 'harvest-supper') out.supper = true;
  const tz = galleyTasting(d); if (tz) add(`tasting table at ${hhmm(tz.from)}: ${tz.choices.join(' and ')}`);
  if (T.dinner && T.dinner.side === 'tasting') {         // Sunday's side: the last tasting table's winner (within the week)
    for (let k = 1; k <= 7; k++) { const z = galleyTasting(d - k); if (z) { if (z.winner) { out.side = z.winner; add(`with Wednesday's winner: ${z.winner}`); } break; } }
  }
  GALLEY_MENU.set(d, out);
  for (const k of GALLEY_MENU.keys()) if (k < d - 8 || k > d + 8) GALLEY_MENU.delete(k);
  return out;
}
// busy windows (answer 11): some days the galley is visibly busy, picked from the day number, so a day is always the
// same. A rush after the day shift's 17:00 change (about half of weekday dinners, 17:00-17:45): the line moves one at a
// time. The odd slow oven (about one day in five, breakfast or dinner): hot pots take 75% longer from half an hour
// before the window opens to an hour after.
const GALLEY_BUSY_TEXT = { rush: 'the shift change is all here at once', slow: 'one of the ovens is playing up' };
const galleyU = (d, k) => schedU(schedU(4111, d, k) * 4294967296 | 0, d, k);   // hashed twice: once is streaky from day to day
function galleyBusy(d) {
  const out = [];
  if (weekday(d) < 5 && galleyU(d, 940) < .5) out.push({ kind: 'rush', meal: 'dinner', from: FOOD.open.dinner, to: FOOD.open.dinner + 45 });
  if (galleyU(d, 941) < .2) { const meal = galleyU(d, 942) < .5 ? 'breakfast' : 'dinner'; out.push({ kind: 'slow', meal, from: FOOD.open[meal] - 30, to: FOOD.open[meal] + 60 }); }
  return out;
}
// birthdays (answer 17): ROSTER `birthday` is a ship day of the year, 1-364 (the crew designer's; none yet means no
// cakes). On the day the galley bakes a cake at 15:00 (4 meals from the cold store), puts it out on the servery's tray
// slide after dinner (19:30) and it's gone by 21:30; Mail says so at 12:00
const CAKE = { mail: 720, bake: 900, out: 1170, gone: 1290, meals: 4 };
// ---- the garden (the user's ask, 0.29.23+): food grows in Deck 3's hydroponic garden, is picked, carried to the cold
// store and cooked. All on paper, a ship day at a time, the same in replays and live (no R()). Each crop has `beds`
// beds; a bed grows by the day's condition (0-1) and is ripe when it has grown `days`; its yield (meal units) is scaled
// by how well it grew (grown / days taken), so a poor garden gives less, later. Salad and herbs are picked every
// morning (GARDEN.pick); beans, tomatoes and roots on harvest mornings (section 18's 'harvest', else every 14th day).
// Picked produce goes to the cold store as its own stock (S.cold.produce: [[crop, meals, day picked], ...]), keeps
// `keep` days, and the cooks use it first (up to GARDEN.potShare of a pot).
const GARDEN_CROPS = [
  { id: 'greens', name: 'salad greens', beds: 4, days: 6, yield: 12, keep: 3, daily: true },
  { id: 'herbs', name: 'herbs', beds: 2, days: 4, yield: 5, keep: 3, daily: true },
  { id: 'beans', name: 'beans', beds: 3, days: 14, yield: 36, keep: 5 },
  { id: 'tomatoes', name: 'tomatoes', beds: 3, days: 21, yield: 54, keep: 7 },
  { id: 'roots', name: 'root vegetables', beds: 3, days: 28, yield: 72, keep: 14 },
];
const GARDEN = {
  pick: 645, harvest: 690, carry: 30,     // the daily pick (10:00-10:45) and the harvest morning's (to 11:30) are taken at their end; the
                                          // crates reach the cold store by section 17's gardenCarry job, else 30 minutes later
  tendHours: 8, untended: .4,             // gardener hours a day for a fully tended garden; growth with nobody tending
  potShare: .5,                           // at most half of a pot is fresh produce
};
// the garden's condition on day d (0-1): water, feed and light from section 17's gardenAt(t) (pure; 1s without it), and
// tending: gardener hours that day from gardenDay(p, d) (section 14's hook), or a fully tended garden while there's none
const GARDEN_COND = new Map();
function gardenCond(d) {
  if (GARDEN_COND.has(d)) return GARDEN_COND.get(d);
  const t = (d - 1) * 1440 + 720, g = (GALLEY_TEST.gardenAt || (typeof gardenAt === 'function' ? gardenAt : null));
  const e = g ? g(t) || {} : {}, f = v => typeof v === 'number' && isFinite(v) ? Math.max(0, Math.min(1, v)) : 1;
  let tend = 1;
  const gd = GALLEY_TEST.gardenDay || (typeof gardenDay === 'function' ? gardenDay : null);
  if (gd) {
    let h = 0; for (const p of ROSTER) { const x = gd(p, d); if (x && x.blocks) for (const b of x.blocks) h += Math.max(0, b.to - b.from) / 60; }
    tend = GARDEN.untended + (1 - GARDEN.untended) * Math.min(1, h / GARDEN.tendHours);
  }
  const out = { water: f(e.water), feed: f(e.feed), light: f(e.light), tend };
  out.grow = out.water * out.feed * out.light * out.tend;
  GARDEN_COND.set(d, out); for (const k of GARDEN_COND.keys()) if (k < d - 30 || k > d + 30) GARDEN_COND.delete(k);
  return out;
}
const gardenHarvestDay = d => typeof eventsOn === 'function' ? eventsOn(d).some(e => e.id === 'harvest' || (e.ev && e.ev.ties && e.ev.ties.garden === 'harvest')) : d % 14 === 6;   // a tradition's garden: 'harvest' too (the first-fruit supper)
// a fresh garden on day d: every bed part-grown, staggered so something is always coming ripe. Beds: [crop, grown, days]
const GARDEN_START = d => ({ beds: GARDEN_CROPS.flatMap((c, ci) => [...Array(c.beds)].map((_, b) => { const g = Math.floor(c.days * ((b + .5) / c.beds + (d % c.days) / c.days) % c.days); return [ci, g, g]; })), crates: [] });
const GARDEN_HARVEST = GARDEN_CROPS.reduce((a, c) => a + (c.daily ? 0 : c.beds * c.yield * 14 / c.days), 0);   // a usual harvest morning's slow crops
const GARDEN_WHY = { water: 'The irrigation is struggling.', feed: 'The nutrient dosing is off.', light: 'The grow lights are failing.', tend: 'There haven\'t been enough hands in the garden.' };
const gardenNames = items => { const n = items.map(x => GARDEN_CROPS[x[0]].name); return n.length > 1 ? n.slice(0, -1).join(', ') + ' and ' + n[n.length - 1] : n[0] || 'produce'; };
// the player unloads the garden's crates at the cold store: section 17 calls this with the carry job's id; they land now
function galleyCarryLand(id) {
  const S = galleyAdvance(shipNow()), G = S.garden; if (!G || !id) return 0;
  const d = Math.floor(shipNow() / 1440) + 1; let n = 0;
  G.crates = G.crates.filter(c => { if (c.id !== id) return true; for (const [ci, k] of c.items) { S.cold.produce.push([ci, k, d]); n += k; } return false; });
  return n;
}
// what's fresh in the cold store, by crop (most first)
const produceByCrop = S => { const m = new Map(); for (const b of S.cold.produce || []) m.set(b[0], (m.get(b[0]) || 0) + b[1]); return [...m].sort((a, b) => b[1] - a[1]); };
const produceMeals = S => (S.cold.produce || []).reduce((n, b) => n + b[1], 0);
// take up to n meal units of produce, oldest first; returns how many
function produceTake(S, n) {
  let got = 0; const P = S.cold.produce || [];
  while (got < n && P.length) { const b = P[0], k = Math.min(b[1], n - got); b[1] -= k; got += k; if (!b[1]) P.shift(); }
  return got;
}
// (yours too: ROSTER_PLAYER's birthday, when it's there)
// crew aboard that evening, as section 18's birthday honorees (schedPeople, aboard(p, d) and not leaving that day;
// birthdayOf(p) when it's there, so the galley bakes for the same people)
const galleyBirthdays = d => {
  const yd = typeof shipYearDay === 'function' ? shipYearDay(d) : ((d - 1) % 364 + 364) % 364 + 1, bday = p => typeof birthdayOf === 'function' ? birthdayOf(p) : p.birthday;
  const here = p => typeof aboard !== 'function' || (aboard(p, d) && (typeof guestStay !== 'function' || guestStay(p, d) !== 'leave'));
  return schedPeople().filter(p => p.rank !== 'guest' && bday(p) === yd && here(p)).concat(typeof ROSTER_PLAYER !== 'undefined' && ROSTER_PLAYER && ROSTER_PLAYER.birthday === yd ? [ROSTER_PLAYER] : []);
};
const galleyNames = ps => ps.map(p => p.player ? 'you' : galleyFirst(p)).join(' and ');
// the day's cake, if any: { who: [people], name, gather }. A birthday (ours, above), or any of section 18's events
// with `cake: true` (eventsOn(d), e.g. Founding Day); gather is when the event's gathering starts, if there is one
function galleyCake(d) {
  const all = typeof eventsOn === 'function' ? eventsOn(d) : [], who = galleyBirthdays(d);
  // (a cake for a tradition held off Deck 3, or with its own decor 'cake', isn't on the servery: four weeks aboard's at Works tea)
  const away = e => !!(e.ev && ((e.ev.ties && e.ev.ties.decor === 'cake') || (Array.isArray(e.ev.where) && e.ev.where.length && e.ev.where.every(w => w.deck !== 3))));
  const bev = all.find(e => e.id === 'birthday'), other = all.find(e => e.id !== 'birthday' && (e.cake || (e.ev && e.ev.cake)) && !away(e));
  if (who.length) return { who, name: '', gather: bev ? bev.from : null, out: CAKE.out };
  if (other) {                                           // a gathering in the mess before 19:30 (the welcome tea at 18:40) has it out from its start
    const g = other.ev && other.ev.ties && other.ev.ties.galley, mess = Array.isArray(other.ev && other.ev.where) && other.ev.where.some(w => w.deck === 3 && /Mess/.test(w.room || ''));
    const early = mess && other.from >= FOOD.open.dinner && other.from < CAKE.out;
    return { who: [], name: other.name, gather: other.from > CAKE.out || early ? other.from : null, out: early ? other.from : CAKE.out, pie: !!(g && /harvest/.test(g.dish || '')) };
  }
  return null;
}
// what the cake's for, in words: "Rosa's birthday", "your birthday", "Founding Day"
const galleyCakeFor = c => c.who.length ? galleyWhose(c.who) + ' birthday' : c.pie ? 'the ' + c.name.toLowerCase() : c.name;
const galleyCakeWord = c => c && c.pie ? 'pie' : 'cake';   // the harvest supper's is a pie
const galleyWhose = ps => ps.length === 1 && ps[0].player ? 'your' : galleyNames(ps) + '\'s';
const galleyMeal = (md, d) => md >= FOOD.open.breakfast - FOOD.lead && md < (d ? galleyClose(d, 'breakfast') : FOOD.close.breakfast) ? 'breakfast' : md >= FOOD.open.dinner - FOOD.lead && md < (d ? galleyClose(d, 'dinner') : FOOD.close.dinner) ? 'dinner' : null;
const GALLEY_START = () => ({ cold: { meals: FOOD.coldCap, produce: [] }, servery: { portions: 0, dish: '' }, grab: { items: 8 }, dirty: 0, inUse: 0, pots: [], wait: [], back: [], carts: [] });
// ship-wide events (Pillar 3, C7): section 18's eventMod('galley', key) changes the galley while an event runs;
// null (no event, or no section 18) means no change. Read on the hour into S.ev (galleyStep):
//   menu:  a dish (an id in GALLEY_EV_DISH, or the dish's own name) instead of the menu's, at both meals
//   cook:  hot pots take this many times as long (storm stew: one pot, quicker)
//   grab:  the grab shelf is stocked for this many times the usual
//   extra: this many more portions at each meal (guests at the servery)
//   batch: meals for a dinner away from the mess (a formal dinner in the Captain's quarters, a feast): a number, or
//          { meals, label }; cooked from the cold store from 15:00
//   trays: trays for the bridge at dinner: cooked with the dinner, plated at 18:00 and sent up by hover cart (section
//          17's cartTrays({ trays, at, to: 'bridge' }) posts the run, when it's there)
// Section 18's eventModAt(t, kind, key) (0.34.8), or its eventMod(kind, key, t) (0.34.7), answers for ship minute t, so
// replays agree with the live galley; an eventMod without the third argument is read live only (eventNow / eventMod:
// now), and replays run as if there were none.
const GALLEY_EV_DISH = { stormStew: 'storm stew', veyli: 'Veyli spiced grains with garden herbs', feast: 'the Founding Day feast', bland: 'plain rice and beans' };
const GALLEY_EV_KEYS = ['menu', 'cook', 'grab', 'extra', 'batch', 'trays', 'herbs'];
// a batch's dinner (the diplomatic visit's formal dinners): it starts at the batch's `at` (minutes of the day), else
// 19:00; cooking takes GALLEY_BATCH_T from 15:00, longer with worn ovens (galleyCookT); `herbs: true` wants
// GALLEY_HERBS meal units of the garden's herbs from the cold store. Late minutes and a dinner without herbs are the
// event's threads 'dinnersLate' and 'noHerbs' (live only)
const GALLEY_BATCH_T = 150, GALLEY_HERBS = 4;
const produceOf = (S, id) => (S.cold.produce || []).reduce((n, b) => n + (GARDEN_CROPS[b[0]].id === id ? b[1] : 0), 0);
function produceTakeOf(S, id, n) {
  let got = 0; for (const b of S.cold.produce || []) if (GARDEN_CROPS[b[0]].id === id && got < n) { const k = Math.min(b[1], n - got); b[1] -= k; got += k; }
  S.cold.produce = (S.cold.produce || []).filter(b => b[1] > 0); return got;
}
// GALLEY_TEST: stand-ins a test copy can set (food_check), since section 17's and 18's functions may be consts it
// can't replace: eventMod(kind, key, t), cartTrays(o) and traysArrivedAt(day, to). null in the game
const GALLEY_TEST = { tradTies: null, eventMod: null, cartTrays: null, traysArrivedAt: null, gardenAt: null, gardenDay: null, gardenCrew: null, gardenCarry: null, carryWaiting: null };
function galleyEvRead(m, replay) {
  let get = null;
  if (GALLEY_TEST.eventMod) get = k => GALLEY_TEST.eventMod('galley', k, m);
  else if (typeof eventModAt === 'function') get = k => eventModAt(m, 'galley', k);
  else if (typeof eventMod === 'function' && eventMod.length >= 3) get = k => eventMod('galley', k, m);
  else if (!replay && typeof eventMod === 'function' && typeof eventNow === 'function' && eventNow()) get = k => eventMod('galley', k);
  if (!get) return null;
  const o = {}; let any = false;
  for (const k of GALLEY_EV_KEYS) { const v = get(k); if (v !== null && v !== undefined) { o[k] = v; any = true; } }
  return any ? o : null;
}
const galleyEvDish = v => typeof v === 'string' && v ? GALLEY_EV_DISH[v] || v : null;
const galleyEvNum = (v, dflt) => typeof v === 'number' && isFinite(v) && v >= 0 ? v : dflt;
// a day's events, from the plans and the rota: who takes food when, and how many cook, bake and wash each minute
const GALLEY_EV = new Map();
function galleyEvents(d) {
  if (GALLEY_EV.has(d)) return GALLEY_EV.get(d);
  const B = (d - 1) * 1440, ev = [], rota = galleyRota(d);
  const cook = new Int8Array(1440), bake = new Int8Array(1440), wash = new Int8Array(1440);
  for (const day of rota.values()) for (const b of day.blocks) {
    const arr = b.task === 'cook' ? cook : b.task === 'bake' ? bake : b.task === 'wash' ? wash : null;
    if (arr) for (let m = b.from; m < Math.min(b.to, 1440); m++) arr[m]++;
  }
  const ppl = schedPeople().slice().sort((a, b) => a.id < b.id ? -1 : 1);
  for (const p of ppl) {
    const segs = planDay(p, d);
    for (let i = 0; i < segs.length; i++) {
      const s = segs[i]; if (s.act !== 'breakfast' && s.act !== 'dinner') continue;
      if (i && segs[i - 1].act === s.act) continue;      // the first segment of a meal is where they get their food
      let j = i; while (j + 1 < segs.length && segs[j + 1].act === s.act) j++;
      const len = s.to - s.from, t = Math.floor(s.from + (s.tag === 'queue' ? Math.min(2, Math.max(0, len - 1)) : 0));
      const kind = s.tag === 'grab' && s.type === 'grab-shelf' ? 'grab' : 'servery';
      const eat = s.tag === 'grab' ? 0 : Math.max(1, Math.floor(segs[j].to) - t);   // a sit-down meal brings a plate back when it's over
      ev.push({ t, id: p.id, meal: s.act, kind, place: s.tag === 'queue' || s.tag === 'grab' ? s.placeId : null, eat });
    }
  }
  ev.sort((a, b) => a.t - b.t || (a.id < b.id ? -1 : 1));
  const left = { breakfast: [], dinner: [] };           // when each meal's servery portions are taken, for "how many still to come"
  for (const e of ev) if (e.kind === 'servery') left[e.meal].push(e.t);
  const grabs = ev.filter(e => e.kind === 'grab').map(e => e.t);
  const out = { d, B, ev, cook, bake, wash, left, grabs, k: 0, busy: galleyBusy(d) };
  GALLEY_EV.set(d, out);
  for (const k of GALLEY_EV.keys()) if (k < d - 2 || k > d + 2) GALLEY_EV.delete(k);
  return out;
}
// worn ovens and ranges cook slower: section 17's shipEffectsAt(3, m).cook scales the time (1 when it isn't there).
// It's the pure, recorded version, safe inside a replay. The rota and galleyCooks never read it (wear reads them).
const galleyCookT = (t, m) => { const e = typeof shipEffectsAt === 'function' && shipEffectsAt(3, m); return Math.max(1, Math.round(t * (e && e.cook > 0 ? e.cook : 1))); };
// how many are at the stoves (cooking or baking) at absolute minute t, for oven wear (section 17)
function galleyCooks(t) { const d = Math.floor(t / 1440) + 1, md = Math.floor(t) - (d - 1) * 1440, E = galleyEvents(d); return E.cook[md] + E.bake[md]; }
const countFrom = (arr, t) => { let a = 0, b = arr.length; while (a < b) { const m = (a + b) >> 1; if (arr[m] < t) a = m + 1; else b = m; } return arr.length - a; };
// one ship minute m (absolute) of the galley, on state S; st collects the day's figures (galleyReport), or null
function galleyStep(S, m, st) {
  const d = Math.floor(m / 1440) + 1, E = galleyEvents(d), md = m - E.B, meal = galleyMeal(md, d);
  const carts = FOOD.restock === 'carts' && typeof cartClaim === 'function';
  if (md === FOOD.deliverAt && !carts) { const n = Math.max(0, FOOD.coldCap - S.cold.meals); S.cold.meals += n; if (st) st.delivered += n; }
  // B3, with FOOD.restock 'carts': on the hour, section 17's cartClaim(t, cold) (a pure rule) says whether a hover
  // cart sets off from the Deck 5 hold, and when it arrives; the meals land here, in replays and live alike
  if (carts) {
    if (!S.carts) S.carts = [];
    // meals already on their way (a run held for you, or not landed yet) count as in the cold store, so a run waiting
    // on the board doesn't set off another every hour. In replays the carts land within the hour, so it's 0 there
    if (md % 60 === 0) {
      const coming = S.carts.reduce((n, c) => n + c[1], 0), c = cartClaim(m, Math.min(FOOD.coldCap, S.cold.meals + coming + produceMeals(S)), { replay: !!st });
      if (c && c.meals > 0) S.carts.push([Math.max(m, Math.floor(c.arriveAt)), c.meals, Math.floor(m / 60)]);
    }
    // a run that's yours (section 17's cartWaiting(hour): on the board for you, or yours and not unloaded yet) waits
    // past its arriveAt: its meals land when you unload at the cold store (galleyCartLand). Live only; replays never wait
    const held = c => !st && c[2] !== undefined && typeof cartWaiting === 'function' && cartWaiting(c[2]);
    if (S.carts.length) { const keep = []; for (const c of S.carts) if (c[0] <= m && !held(c)) { const n = Math.min(c[1], FOOD.coldCap - S.cold.meals); S.cold.meals += n; if (st) { st.delivered += n; st.waste += c[1] - n; } } else keep.push(c); S.carts = keep; }
  }
  // spoilage (answer 7): S.spoil, the share of the cold store lost an hour, read on the hour from section 17's
  // chillerAt(m).spoil (0 while the chiller works well, up to CHILL_SPOIL broken), else from shipEffectsAt(3, m).spoil
  // (1 fine, 2 broken: FOOD.spoilDay a day). Both pure, so replays agree. A warm store's food goes off bit by bit (S.rot);
  // the 09:00 and 21:00 checks bin what's gone off (S.bin, by the dish pit) and tell you by Mail; the bin goes at 10:30
  if (md % 60 === 0) {
    const c = typeof chillerAt === 'function' && chillerAt(m), e = !c && typeof shipEffectsAt === 'function' && shipEffectsAt(3, m);
    S.spoil = c ? Math.max(0, c.spoil || 0) : e && e.spoil > 1 ? (e.spoil - 1) * FOOD.spoilDay / 24 : 0;
  }
  if (S.spoil) S.rot = (S.rot || 0) + S.cold.meals * S.spoil / 60;
  if (S.rot >= 1 && FOOD.binAt.includes(md)) {
    const n = Math.min(S.cold.meals, Math.floor(S.rot));
    S.rot -= Math.floor(S.rot); S.cold.meals -= n; S.bin = (S.bin || 0) + n;
    if (st) st.spoiled += n;
    else if (n && typeof eventNow === 'function' && eventNow(m)) galleyScore(m, 'spoiled', n);   // an event's "Nothing spoiled" thread
    if (!st && n) galleyMail(m, 'Spoiled food binned', `The cold store's chiller is running warm, and ${n} meal${n > 1 ? 's' : ''} had to go in the bin at the ${hhmm(md)} check. Works has been told.`);
  }
  if (md === FOOD.binOut) S.bin = 0;
  // the garden: a day's growth at midnight; the morning pick (salad, herbs) and the harvest morning (the rest); the
  // crates reach the cold store GARDEN.carry minutes later; produce past its keeping days is binned at the bin checks
  if (!S.garden) S.garden = GARDEN_START(d);
  if (S.garden.crates.length && Array.isArray(S.garden.crates[0])) S.garden.crates = S.garden.crates.map(c => ({ at: c[0] - GARDEN.carry, items: [[c[1], c[2]]], id: null }));   // a 0.29.23 save
  if (!S.cold.produce) S.cold.produce = [];
  const G = S.garden;
  if (md === 0) { const c = gardenCond(d).grow; for (const b of G.beds) if (b[1] < GARDEN_CROPS[b[0]].days) { b[2]++; b[1] = Math.min(GARDEN_CROPS[b[0]].days, b[1] + c); } }   // a ripe bed waits for its pick
  // the daily pick needs a gardener on duty (section 14's gardenCrew(d), when it's there); the harvest morning has
  // volunteers. One carry for each pick: G.crates = [{ at, items: [[crop, meals]], id }]
  let pickNow = md === GARDEN.pick ? 'daily' : md === GARDEN.harvest && gardenHarvestDay(d) ? 'harvest' : null;
  const crew = GALLEY_TEST.gardenCrew || (typeof gardenCrew === 'function' ? gardenCrew : null);
  if (pickNow === 'daily' && (gardenHarvestDay(d) || (crew && !(crew(d) || []).length))) pickNow = null;
  if (pickNow) {
    const items = [];
    for (const b of G.beds) {
      const c = GARDEN_CROPS[b[0]]; if (b[1] < c.days || (pickNow === 'daily' && !c.daily)) continue;   // the harvest morning picks everything ripe
      const n = Math.round(c.yield * Math.min(1, c.days / Math.max(c.days, b[2])) * (pickNow === 'harvest' && typeof irrigationBonus === 'function' ? 1 + irrigationBonus(d) : 1));   // 24r (E2): cleared nozzles, a little more
      if (n > 0) { const it = items.find(x => x[0] === b[0]); if (it) it[1] += n; else items.push([b[0], n]); if (st) st.picked += n; }
      b[1] = 0; b[2] = 0;
    }
    const got = items.reduce((a, x) => a + x[1], 0);
    if (got) {
      const cr = { at: m, items, id: null };
      if (!st) {                                         // live: section 17's carry job (the player first, then the crew)
        const gc = GALLEY_TEST.gardenCarry || (typeof gardenCarry === 'function' ? gardenCarry : null);
        if (gc) cr.id = gc({ at: m, crates: Math.ceil(got / 10), title: `Carry ${Math.ceil(got / 10)} crate${got > 10 ? 's' : ''} of ${gardenNames(items)} from the garden to the cold store` }) || null;
      }
      G.crates.push(cr);
    }
    if (pickNow === 'harvest' && !st && got < GARDEN_HARVEST / 2) {   // half a usual harvest morning or less: Brennan writes
      const c = gardenCond(d), worst = ['water', 'feed', 'light', 'tend'].sort((a, b) => c[a] - c[b])[0];
      galleyMail(m, 'A thin harvest', `Only ${got} meals' worth came in from the garden this morning (a good harvest is about ${Math.round(GARDEN_HARVEST / 10) * 10}). ${GARDEN_WHY[worst]} We'll lean on the stores until it picks up.`);
    }
  }
  if (G.crates.length) {
    const keep = [], cw = GALLEY_TEST.carryWaiting || (typeof carryWaiting === 'function' ? carryWaiting : null);
    for (const c of G.crates) {
      const waiting = !st && c.id && cw ? cw(c.id, m) : m < c.at + GARDEN.carry;
      if (waiting) keep.push(c); else for (const [ci, n] of c.items) S.cold.produce.push([ci, n, d]);
    }
    G.crates = keep;
  }
  if (FOOD.binAt.includes(md) && S.cold.produce.length) {
    const keep = []; let n = 0;
    for (const b of S.cold.produce) if (d - b[2] > GARDEN_CROPS[b[0]].keep) n += b[1]; else keep.push(b);
    if (n) { S.cold.produce = keep; S.bin = (S.bin || 0) + n; if (st) st.produceBinned += n; }
  }
  // an event (C7): its galley settings, on the hour; a batch for a dinner away from the mess at 15:00
  if (md % 60 === 0) S.ev = galleyEvRead(m, !!st);
  if (md === 900 && S.ev && S.ev.batch) {
    const b = S.ev.batch, want = Math.round(galleyEvNum(typeof b === 'object' ? b.meals : b, 0)), n = Math.min(want, S.cold.meals);
    if (n > 0) {
      S.cold.meals -= n; S.batch = { d, meals: n, label: (typeof b === 'object' && b.label) || 'a formal dinner' }; if (st) st.batch += n;
      const start = typeof b === 'object' && b.at > 900 ? b.at : 1140, ready = 900 + galleyCookT(GALLEY_BATCH_T, m);
      S.batch.late = Math.max(0, ready - start);
      if (S.ev.herbs) S.batch.herbs = produceTakeOf(S, 'herbs', GALLEY_HERBS) >= GALLEY_HERBS;
      if (!st && S.batch.late) galleyScore(m, 'dinnersLate', S.batch.late);
      if (!st && S.ev.herbs && !S.batch.herbs) galleyScore(m, 'noHerbs', 1);
    }
  }
  if (md === FOOD.open.breakfast) S.batch = null;
  // a cake: a birthday, or one of section 18's events with cake: true (Founding Day)
  if (md === CAKE.mail || md === CAKE.bake || (md >= FOOD.open.dinner && md <= CAKE.out) || md === CAKE.gone) {
    const c = galleyCake(d);
    if (md === CAKE.gone) S.cake = null;
    else if (c) {
      if (md === CAKE.mail && !st) galleyMail(m, `${c.pie ? 'Pie' : 'Cake'} tonight`, `It's ${galleyCakeFor(c)}. The ${galleyCakeWord(c)}'s out on the servery from ${hhmm(c.out)}` + (c.gather ? `, and everyone's in the mess at ${hhmm(c.gather)}.` : '. Everyone welcome.'));
      if (md === CAKE.bake) { const n = Math.min(CAKE.meals, S.cold.meals); S.cold.meals -= n; S.cake = n ? { d, who: c.who.map(p => p.id), out: false, pie: !!c.pie } : null; if (st && n) st.cakes++; }
      if (md === c.out && S.cake) S.cake.out = true;
    }
  }
  // the tasting table: its tastes cooked an hour before (produce first), out from the start, one for each taster as
  // they arrive (one of each dish: those already there when it opens, then at their minute); what's left goes 15 minutes
// after the end
  const tt = galleyTies(d).dinner && galleyTies(d).dinner.taste;
  if (tt) {
    if (md === tt.from - 60) {                           // a taste is a few bites: FOOD.tastes of them from a meal unit
      const n = galleyTasting(d).tastes, u = Math.ceil(n / FOOD.tastes), f = produceTake(S, u), k = Math.min(u - f, S.cold.meals), got = Math.min(n, (f + k) * FOOD.tastes);
      S.cold.meals -= k; S.tasting = { d, left: got, out: false, n: got }; if (st) { st.tastes += got; st.fresh += f; }
    }
    if (S.tasting && S.tasting.d === d) {
      if (md === tt.from) S.tasting.out = true;
      if (S.tasting.out && md < tt.to + 15) for (const v of galleyTasting(d).voters) if ((v.at === m || (md === tt.from && v.at < m)) && S.tasting.left > 0) { const k = Math.min(2, S.tasting.left); S.tasting.left -= k; if (st) st.tasted += k; }   // one of each
      if (md === tt.to + 15) { if (st) st.waste += S.tasting.left; S.tasting = null; }
    }
  }
  // plates come back, and the dish pit washes what it can
  if (S.back.length) { const keep = []; for (const b of S.back) if (b[0] <= m) { S.inUse -= b[1]; S.dirty += b[1]; } else keep.push(b); S.back = keep; }
  const w = Math.min(S.dirty, E.wash[md] * FOOD.washRate); S.dirty -= w; if (st) st.washed += w;
  // cooking: idle cooks start a pot when the coming meal needs more than the servery and the pots hold; bakers
  // (and idle cooks) fill the grab shelf; then everyone at the stoves works a pot
  const inPots = kind => S.pots.reduce((n, p) => n + (p[2] === kind ? p[1] : 0), 0);
  let cooks = E.cook[md], bakers = E.bake[md];
  const busy = k => E.busy.some(b => b.kind === k && md >= b.from && md < b.to);
  const potsOf = kind => S.pots.filter(p => p[2] === kind).length;
  if (meal && md >= FOOD.open[meal] - FOOD.lead) {
    const ev = S.ev || {}, evDish = galleyEvDish(ev.menu);
    if (!S.servery.dish || S.servery.meal !== meal || (evDish && S.servery.dish !== evDish && !S.servery.portions)) { S.servery.dish = evDish || galleyMenu(d)[meal]; S.servery.meal = meal; }
    const more = Math.round(galleyEvNum(ev.extra, 0)) + (meal === 'dinner' && md < FOOD.trayAt ? Math.round(galleyEvNum(ev.trays, 0)) : 0);
    let need = Math.min(FOOD.serveryCap + (galleyTies(d)[meal] ? FOOD.feastCap : 0), countFrom(E.left[meal], m) + S.wait.length + FOOD.slack + more) - S.servery.portions - inPots('hot');
    for (let idle = cooks - potsOf('hot'); idle > 0 && need > 0; idle--) {
      const fresh = produceTake(S, Math.floor(FOOD.batch * (galleyMenu(d).supper ? (meal === 'dinner' ? 1 : 0) : GARDEN.potShare))), n = fresh + Math.min(FOOD.batch - fresh, S.cold.meals); if (n <= 0) { if (st) st.coldOut++; break; }
      S.cold.meals -= n - fresh; if (st) st.fresh += fresh; S.pots.push([galleyCookT(FOOD.cookT * (busy('slow') ? FOOD.slowOven : 1) * galleyEvNum(ev.cook, 1), m), n, 'hot']); need -= n; if (st) st.cooked += n;
    }
  }
  {
    const g = galleyEvNum(S.ev && S.ev.grab, 1);
    let need = Math.min(FOOD.grabCap, Math.round((countFrom(E.grabs, m) + FOOD.grabSlack) * g)) - S.grab.items - inPots('grab');
    for (let idle = bakers + Math.max(0, cooks - potsOf('hot')) - potsOf('grab'); idle > 0 && need > 0; idle--) {
      const n = Math.min(FOOD.bake, S.cold.meals); if (n <= 0) break;
      S.cold.meals -= n; S.pots.push([galleyCookT(FOOD.bakeT, m), n, 'grab']); need -= n; if (st) st.baked += n;
    }
  }
  const done = [];
  for (const p of S.pots) {
    if (p[2] === 'hot' ? cooks > 0 : bakers + cooks > 0) {
      if (p[2] === 'hot') cooks--; else if (bakers > 0) bakers--; else cooks--;
      if (--p[0] <= 0) done.push(p);
    }
  }
  for (const p of done) {
    S.pots.splice(S.pots.indexOf(p), 1);
    if (p[2] === 'hot') S.servery.portions += p[1];
    else { const n = Math.min(p[1], FOOD.grabCap - S.grab.items); S.grab.items += n; if (st) st.waste += p[1] - n; }
  }
  // trays for the bridge (an event): plated from the servery at 18:00 and sent up by hover cart
  if (md === FOOD.trayAt && S.ev && S.ev.trays) {
    const n = Math.min(Math.round(galleyEvNum(S.ev.trays, 0)), S.servery.portions);
    if (n > 0) { S.trays = { d, n, job: null }; S.servery.portions -= n; if (st) st.trays += n; else S.trays.job = (GALLEY_TEST.cartTrays || (typeof cartTrays === 'function' ? cartTrays : () => null))({ trays: n, at: m, to: 'bridge' }) || null; }
  }
  // an event's "A fed bridge" thread: on a day it wants trays for the bridge, each hour from noon until they reach the
  // bridge: section 17's traysArrivedAt(day) is when the cart's drop-off ends (null: not yet, or nobody on it), so a
  // late or missed cart run shows. Without it (or when cartTrays made no run) the count stops when the trays go up at
  // 18:00, 6 hours a day, the thread's "good". Live only: replays never score
  if (!st && md % 60 === 0 && md >= 720 && S.ev && S.ev.trays) {
    const sent = S.trays && S.trays.d === d, ta = GALLEY_TEST.traysArrivedAt || (typeof traysArrivedAt === 'function' ? traysArrivedAt : null);
    const arr = sent && S.trays.job && ta ? ta(d, 'bridge') : undefined;
    const hungry = arr === undefined ? md < FOOD.trayAt && !sent : arr === null || m < arr;
    if (hungry) galleyScore(m, 'bridgeHungry', 1);
  }
  // serving: those already waiting first, then whoever reaches the front this minute (in a rush, only so many a minute)
  let line = busy('rush') ? FOOD.rushRate : Infinity;
  const serve = (kind, plate) => {
    if (kind === 'grab' && S.grab.items > 0) { S.grab.items--; return 'grab'; }
    if (line > 0 && S.servery.portions > 0 && (!plate || FOOD.plates - S.dirty - S.inUse > 0)) { S.servery.portions--; line--; return 'servery'; }
    return null;
  };
  const got = (x, how, eat) => {
    if (eat && how === 'servery') { S.inUse++; S.back.push([m + eat, 1]); }
    const lt = galleyLateBy(d, md, x.meal, m - x.since, how, LATE_WAIT.crew);
    if (lt) { if (st) st.late++; else galleyLate(m, x.id, x.meal, lt, how, how === 'servery' ? S.servery.dish : null); }
    if (st) {
      st[how === 'grab' ? 'grabbed' : 'eaten']++; const wt = m - x.since; st.waits.push(wt);
      if (wt > st.maxWait) { st.maxWait = wt; st.maxWho = x.id + ' ' + hhmm(md); }
      if (x.meal && wt > st.mealMax[x.meal]) st.mealMax[x.meal] = wt;
    }
  };
  if (S.wait.length) {
    const keep = [];
    for (const x of S.wait) {
      const [id, since, kind, wm, place, eat] = x, how = serve(kind, eat > 0);
      if (how) got({ id, since, meal: wm }, how, eat);
      else if (md === galleyClose(d, wm) + FOOD.giveUp) { if (st) st.missed.push(id + ' ' + wm); else galleyLate(m, id, wm, m - since, 'missed', null); }
      else keep.push(x);
    }
    S.wait = keep;
  }
  if (E.k > E.ev.length || (E.k && E.ev[E.k - 1].t >= md + E.B)) E.k = 0;   // a fresh pass over the day (a report, a new game)
  while (E.k < E.ev.length && E.ev[E.k].t < m) E.k++;
  for (; E.k < E.ev.length && E.ev[E.k].t === m; E.k++) {
    const e = E.ev[E.k], how = serve(e.kind, e.eat > 0);
    if (st) st.ate++;
    if (how) got({ id: e.id, since: m, meal: e.meal }, how, e.eat);
    else S.wait.push([e.id, m, e.kind, e.meal, e.place, e.eat]);
  }
  // the line closes: what's left goes to the grab shelf, wrapped, and the rest is wasted
  if (meal === null && S.servery.portions > 0 && (md === galleyClose(d, 'breakfast') || md === galleyClose(d, 'dinner'))) {
    const n = Math.min(S.servery.portions, FOOD.grabCap - S.grab.items);
    S.grab.items += n; if (st) st.waste += S.servery.portions - n; S.servery.portions = 0;
  }
  if (st) {
    st.coldMin = Math.min(st.coldMin, S.cold.meals);
    if (md === FOOD.open.breakfast || md === FOOD.open.dinner) st.ready[md === FOOD.open.breakfast ? 'breakfast' : 'dinner'] = { portions: S.servery.portions, grab: S.grab.items };
    if (md % 60 === 0) st.hours.push([hhmm(md), S.cold.meals, S.servery.portions, S.grab.items, S.dirty, S.inUse, S.pots.length, S.wait.length]);
  }
}
// someone eats late: section 13's simNote('lateMeal', { who: roster id | 'you', meal: 'breakfast' | 'dinner', late:
// minutes, how: 'servery' | 'grab' | 'missed', dish: the hot dish's name or null (the shelf, or missed), deck: 3 }), heard by section 20 (the cue 'lateMeal', 'lateMeal.you')
// and the reactions bank. Late is a wait of LATE_WAIT minutes or more (late: the wait), or a meal from the grab shelf
// 10 minutes to 4 hours after its serving has ended (late: the minutes since), or giving up on a wait. Live only, once per
// person and meal a day
const LATE_WAIT = { crew: 15, you: 10 }, GALLEY_LATE = new Set();
let GALLEY_QUIET = -Infinity;                            // galleyAdvance: a fresh start's catch-up from midnight to now posts no late meals
function galleyLateBy(d, md, meal, waited, how, wait) {
  if (!meal) return 0;
  if (waited >= wait) return waited;
  const end = galleyServeEnd(d, meal), after = md - end;
  return how === 'grab' && after >= 10 && after <= 240 ? after : 0;   // a few minutes after is just the grab-and-go
}
function galleyLate(m, who, meal, late, how, dish) {
  const d = Math.floor(m / 1440) + 1, k = d + '|' + who + '|' + meal;
  if (typeof simNote !== 'function' || GALLEY_LATE.has(k) || m < GALLEY_QUIET) return;   // a fresh galley worked out from midnight: those minutes didn't happen
  GALLEY_LATE.add(k); for (const x of GALLEY_LATE) if (+x.split('|')[0] < d - 2) GALLEY_LATE.delete(x);
  simNote('lateMeal', { who, meal, late: Math.round(late), how, dish: dish || null, deck: 3, t: m });   // t: when it happened (a time jump steps many minutes at once)
}
// step SHIP.galley up to ship minute `to` (absolute); a fresh start when there's no state or time went backwards
// you unload a cart at the cold store (3-cold-1/2): section 17 calls this with the run's hour (the hour in its job id,
// restock-meals@<hour>), and its meals land now. Returns the meals landed (0: nothing of that run is waiting)
function galleyCartLand(h) {
  const S = galleyAdvance(shipNow()); if (!S.carts) return 0;
  let n = 0; const keep = [];
  for (const c of S.carts) if (c[2] === h) { const k = Math.min(c[1], FOOD.coldCap - S.cold.meals); S.cold.meals += k; n += k; } else keep.push(c);
  S.carts = keep; return n;
}
// an event's thread (section 18's eventScore), once for each minute and thread: the live galley can step the same
// minutes again after a fresh start
const GALLEY_SCORED = new Set();
function galleyScore(m, thread, n) {
  const k = m + '|' + thread; if (typeof eventScore !== 'function' || GALLEY_SCORED.has(k)) return;
  GALLEY_SCORED.add(k); eventScore(thread, n);
}
// a note to the device's Mail tab (section 15's mailSend, when it's there), once: never twice for the same minute and subject
const GALLEY_MAILED = new Set();
function galleyMail(at, subject, body) {
  if (typeof mailSend !== 'function') return;
  const key = at + '|' + subject, box = SHIP.mail && (Array.isArray(SHIP.mail) ? SHIP.mail : SHIP.mail.inbox);
  if (GALLEY_MAILED.has(key) || (Array.isArray(box) && box.some(x => x && x.at === at && x.subject === subject))) return;
  GALLEY_MAILED.add(key); mailSend({ at, from: galleyChef() || 'The galley', subject, body });
}
const galleyChef = () => { const c = galleyStaff().find(p => galleyTeam(p) === 'chef'); return c ? galleyFirst(c) : ''; };
function galleyAdvance(to) {
  to = Math.floor(to);
  let S = SHIP.galley;
  if (!S || !(S.at <= to + 1)) { S = SHIP.galley = { at: (Math.floor(to / 1440)) * 1440, ...GALLEY_START() }; GALLEY_QUIET = to; }
  while (S.at <= to) galleyStep(S, S.at++, null);
  return S;
}
// the player (or anyone) eats: a hot portion and a plate if the servery has one, else something from the grab shelf
function takePortion(who = 'player') {
  const S = galleyAdvance(shipNow()), m = Math.floor(shipNow()), j = GALLEY_JOINED.get(who);
  GALLEY_JOINED.delete(who); if (j && j.line && typeof lineLeave === 'function') lineLeave(who);   // out of section 10's line
  let how = null;
  if (S.servery.portions > 0 && FOOD.plates - S.dirty - S.inUse > 0) { S.servery.portions--; S.inUse++; S.back.push([m + 20, 1]); how = 'servery'; }
  else if (S.grab.items > 0) { S.grab.items--; how = 'grab'; }
  if (how && who === 'player') {                         // your late meal (lateMeal): the meal whose serving ended last, the night's dinner after midnight
    let d = Math.floor(m / 1440) + 1, md = m - (d - 1) * 1440;
    if (md < FOOD.open.breakfast - FOOD.lead) { d--; md += 1440; }
    const meal = md >= FOOD.open.dinner - FOOD.lead ? 'dinner' : 'breakfast', lt = galleyLateBy(d, md, meal, j && j.since !== undefined ? m - j.since : 0, how, LATE_WAIT.you);
    if (lt) galleyLate(m, 'you', meal, lt, how, how === 'servery' ? S.servery.dish : null);
  }
  return !!how;
}
// the player joins the servery queue: where to stand (the back of the line, by the tray return: a tile that's no
// one's place) and when it's their turn. Ahead of you is who's really in the line now (galleyAhead); the line serves
// GALLEY_SERVE.each ship minutes a person (a minute in a rush, the galley's own rush rate), and you take yours
// GALLEY_SERVE.you after the last of them. galleyTurn(who) is true from then on while there's food (empty pans: you
// wait for the next pot); takePortion(who) serves them and ends it
const GALLEY_JOIN = { at: [33, 2], xy: [33.55, 2.5], face: 's' }, GALLEY_JOINED = new Map();   // face: a letter, or degrees (0 south, 90 east)
const GALLEY_SERVE = { each: .6, you: 1, near: .8 };   // ship minutes a serve (yours: taking a tray and being served, under 2 real seconds) (a line of 6 clears in about 3.6; the user's ask: 5-8 at peaks, cleared in a few minutes); how close to a queue spot counts as standing in it (m)
// the crew really in the line: section 10's live line (servLine) when it's there; else on Deck 3, those standing at
// (or right by) the queue spots (section 10's DECK_CREW, the bodies you see); elsewhere (a test, another deck) each person in a queue stop or waiting for food, once
function galleyAhead(now, who = 'player') {
  if (typeof servLine === 'function' && typeof deckDef !== 'undefined' && deckDef && deckDef.num === 3) return servLine().filter(id => id !== who).length;   // section 10's live line: who's in it
  const Q = new Set(GALLEY_QUEUE);
  if (typeof deckDef !== 'undefined' && deckDef && deckDef.num === 3 && typeof DECK_CREW !== 'undefined')
    return DECK_CREW.filter(a => a.spot && Q.has(a.spot.id) && Math.hypot(a.x - a.spot.x, a.z - a.spot.z) < GALLEY_SERVE.near).length;
  const ids = new Set(schedPeople().filter(p => { const w = whereIs(p, now); return w.deck === 3 && w.tag === 'queue'; }).map(p => p.id));
  for (const w of (SHIP.galley && SHIP.galley.wait) || []) ids.add(w[0]);
  return ids.size;
}
// serving at the counter (for section 10's live line, below): how long the person at the front takes, in ship minutes
// (GALLEY_SERVE.each; a minute in a rush), and whether there's anything to hand over now (a hot portion and a clean
// plate, or something on the grab shelf)
function galleyServeMins(t = shipNow()) {
  const d = Math.floor(t / 1440) + 1, md = Math.floor(t) - (d - 1) * 1440;
  return galleyEvents(d).busy.some(b => b.kind === 'rush' && md >= b.from && md < b.to) ? 1 / FOOD.rushRate : GALLEY_SERVE.each;
}
function galleyCanServe(t = shipNow()) {
  const S = galleyAdvance(t); return (S.servery.portions > 0 && FOOD.plates - S.dirty - S.inUse > 0) || S.grab.items > 0;
}
// section 10's live line on Deck 3 (sim engineer 3: lineJoin, lineSpot, lineFront, lineLeave, servLine), when it's
// there: you stand in it behind the real crew and step up; your turn is GALLEY_SERVE.you after you reach the counter.
// Without it, a spot at the back and a turn from who's standing in the line (galleyAhead)
const galleyLine = () => typeof lineJoin === 'function' && typeof lineSpot === 'function' && typeof lineFront === 'function' && typeof servLine === 'function';
// galleyJoin(who, { peek: true }): the spot at the back of the line now, without taking a place in it (section 15 walks
// you there, then joins on arrival, so you don't hold the counter while crossing the mess)
function galleyJoin(who = 'player', o = {}) {
  const now = shipNow(); galleyAdvance(now);
  const ahead = galleyAhead(now, who), j = { at: GALLEY_JOIN.at.slice(), xy: GALLEY_JOIN.xy.slice(), face: GALLEY_JOIN.face, ahead, since: now, turnAt: now + GALLEY_SERVE.you + ahead * galleyServeMins(now) };
  if (galleyLine()) {                                   // lineSpot: world x, z and face in radians; ours: the deck's x, y and degrees
    const had = servLine().includes(who); lineJoin(who); const sp = lineSpot(who);
    if (sp && sp.at) { j.at = sp.at.slice(); if (isFinite(sp.x)) j.xy = [sp.x + OX, sp.z + OZ]; if (isFinite(sp.face)) j.face = sp.face * 180 / Math.PI; }
    if (o.peek && !had) { lineLeave(who); j.peek = true; return j; }
    j.line = true; j.front = null; if (typeof servLine === 'function') j.ahead = Math.max(0, servLine().indexOf(who));
  }
  GALLEY_JOINED.set(who, j); return j;
}
// out of the line without being served (you walked away): section 15 may call it; galleyTick does it anyway once you
// aren't queueing (section 15's ACT), so nobody behind you is stuck at the counter
function galleyLeave(who = 'player') { const j = GALLEY_JOINED.get(who); GALLEY_JOINED.delete(who); if (typeof lineLeave === 'function' && (!j || j.line)) lineLeave(who); }
function galleyTurn(who = 'player') {
  const j = GALLEY_JOINED.get(who); if (!j) return false;
  const now = shipNow();
  if (j.line && galleyLine()) {                          // the live line: at the counter, then served
    if (!lineFront(who)) { j.front = null; return false; }
    if (j.front === null) { j.front = now; j.turnAt = now + GALLEY_SERVE.you; }
    return now >= j.turnAt && galleyCanServe(now);
  }
  return now >= j.turnAt && galleyCanServe(now);
}
// someone waiting for food at the servery: the queue place they wait at (null: stand where you are), else undefined
// Each waiter gets their own spot: the queue places in line order (the first to wait at the front), then null.
// The galley is brought up to t first, so a stepped test sees the same waits as the game.
const GALLEY_QUEUE = ['3-queue-4', '3-queue-3', '3-queue-2', '3-queue-1'];   // front first: 3-queue-4 is at the counter (the line runs from the trays south to the food)
function galleyHold(person, t) {
  let S = SHIP.galley; if (!S) return undefined;
  if (t !== undefined && S.at <= Math.floor(t)) S = galleyAdvance(t);
  if (!S.wait.length) return undefined;
  const k = S.wait.findIndex(w => w[0] === person.id); return k < 0 ? undefined : GALLEY_QUEUE[k] || null;
}
// the save: SHIP.galley as plain data, and back (anything malformed means a fresh start from the plans)
function galleySave() { return SHIP.galley ? JSON.parse(JSON.stringify(SHIP.galley)) : null; }
function galleyLoad(o) {
  const ok = o && typeof o === 'object' && Number.isInteger(o.at) && o.cold && isFinite(o.cold.meals) && o.servery && isFinite(o.servery.portions)
    && o.grab && isFinite(o.grab.items) && isFinite(o.dirty) && isFinite(o.inUse) && ['pots', 'wait', 'back'].every(k => Array.isArray(o[k]));
  SHIP.galley = ok ? JSON.parse(JSON.stringify(o)) : null;
  return !!ok;
}
// a line about the galley for tap texts: what's on, and how much is left
function galleyText(what = 'servery') {
  const S = galleyAdvance(shipNow()), md = SHIP.time.min, day = SHIP.time.day, meal = md >= galleyClose(day, 'breakfast') && md < galleyClose(day, 'dinner') ? 'dinner' : 'breakfast';
  if (what === 'grab') return S.grab.items ? `${S.grab.items} on the shelf.` : 'The shelf is empty.';
  if (what === 'dish') return S.dirty ? `${S.dirty} plates waiting to be washed.` : 'All washed up.';
  if (what === 'cold') return `About ${S.cold.meals} meals in the cold store` + (produceMeals(S) ? `, and ${produceMeals(S)} of fresh produce from the garden.` : '.') + (S.spoil ? ' It\'s running warm.' : '') + (S.bin ? ` ${S.bin} spoiled meals binned by the dish pit.` : '');
  if (what === 'menu') return galleyBoard();
  if (what === 'garden') {
    const G = S.garden || { beds: [], crates: [] }, ripe = new Map(), c = gardenCond(SHIP.time.day);
    for (const b of G.beds) if (b[1] >= GARDEN_CROPS[b[0]].days) ripe.set(b[0], (ripe.get(b[0]) || 0) + 1);
    const r = [...ripe].map(([ci, k]) => `${GARDEN_CROPS[ci].name} (${k} bed${k > 1 ? 's' : ''})`);
    let next = SHIP.time.day; while (!gardenHarvestDay(next) && next < SHIP.time.day + 15) next++;
    return (r.length ? `Ripe: ${r.join(', ')}.` : 'Nothing ripe just now.') + (c.grow < .7 ? ' ' + GARDEN_WHY[['water', 'feed', 'light', 'tend'].sort((a, b) => c[a] - c[b])[0]] : ' Growing well.')
      + ` Next harvest morning: ${next === SHIP.time.day ? 'today' : WEEKDAYS[weekday(next)]}.` + (G.crates.length ? ' Crates waiting to go to the cold store.' : '');
  }
  if (what === 'tasting') {                              // the tasting table: what's on, then (from its start) the vote so far
    const z = galleyTasting(SHIP.time.day); if (!z) return '';
    const left = S.tasting && S.tasting.d === SHIP.time.day ? S.tasting.left : 0, mine = z.you !== null ? ` You voted for ${z.choices[z.you]}.` : '';
    if (md < z.from) return `Brennan's tasting table at ${hhmm(z.from)}: ${z.choices.join(' and ')}.`;
    return `Brennan's tasting table: ${z.choices.join(' and ')}` + (left ? `, ${left} taste${left > 1 ? 's' : ''} left.` : '.') + (md >= z.to && z.winner ? ` ${z.winner[0].toUpperCase() + z.winner.slice(1)} won, ${z.votes[z.win]} vote${z.votes[z.win] === 1 ? '' : 's'} to ${z.votes[1 - z.win]}.` : '') + mine;
  }
  if (what === 'event') return S.batch && S.batch.d === SHIP.time.day ? `Brennan is cooking for ${S.batch.label} (${S.batch.meals} meals).` : '';
  const open = md >= FOOD.open[meal] && md < galleyServeEnd(day, meal);
  const evd = galleyEvDish(S.ev && S.ev.menu), M = evd ? { dinner: evd, note: '' } : galleyMenu(SHIP.time.day), ck = galleyCake(SHIP.time.day), now = galleyEvents(SHIP.time.day).busy.find(b => md >= b.from && md < b.to);
  let extra = meal === 'dinner' && M.note ? ` Tonight: ${M.dinner}, ${M.note}.` : '';
  if (S.wait.length) extra = ` ${S.wait.length} waiting` + (now ? `: ${GALLEY_BUSY_TEXT[now.kind]}.` : '.') + extra;
  if (S.cake && S.cake.out && ck) extra += ck.who.length ? ` Birthday cake for ${galleyNames(ck.who)} on the end of the counter.` : ck.pie ? ' A harvest pie on the end of the counter.' : ` A ${ck.name} cake on the end of the counter.`;
  else if (ck && md < ck.out) extra += ` ${ck.pie ? 'Pie' : 'Cake'} ${ck.out < CAKE.out ? 'at ' + hhmm(ck.out) : 'after dinner'}: it's ${galleyCakeFor(ck)}.`;
  if (meal === 'breakfast' && open && M.bnote) extra += ` It's the ${M.bnote}.`;
  if (S.tasting && S.tasting.d === day && S.tasting.out) extra += ' ' + galleyText('tasting');
  const fresh = produceByCrop(S).slice(0, 2).map(x => GARDEN_CROPS[x[0]].name);
  if (fresh.length && (S.servery.portions || open)) extra += ` Fresh from the garden: ${fresh.join(' and ')}.`;
  if (S.batch && S.batch.d === SHIP.time.day && md < 1260) extra += ` Brennan is also cooking for ${S.batch.label}` + (S.batch.late ? ', running late' : '') + (S.batch.herbs === false ? ', without the garden\'s herbs' : '') + '.';
  if (S.trays && S.trays.d === SHIP.time.day && md >= FOOD.trayAt && md < FOOD.trayAt + 60) extra += ` ${S.trays.n} trays have gone up to the bridge.`;
  if (S.servery.portions) return `${open ? 'Serving' : 'Ready'}: ${S.servery.dish}. ${S.servery.portions} portions in the pans.` + extra;
  return (open ? 'The pans are empty. The next pot is on its way.' : `Closed. ${meal === 'breakfast' ? 'Breakfast from 06:00' : 'Dinner from 17:00'}.`) + extra;
}
// the menu board: today's meals and the week's dinners
function galleyBoard(d = SHIP.time.day) {
  const M = galleyMenu(d);
  const week = [...Array(7)].map((_, k) => d - weekday(d) + k).map(x => WEEKDAYS[weekday(x)].slice(0, 3) + ' ' + galleyMenu(x).dinner);
  const ck = galleyCake(d), hb = ck && (ck.who.length ? `happy birthday, ${galleyNames(ck.who)}!` : `happy ${ck.name}!`);
  return `Today: ${M.breakfast} for breakfast${M.bnote ? ' (' + M.bnote + ')' : ''}, ${M.dinner} for dinner${M.note ? ' (' + M.note + ')' : ''}.` + (ck ? ck.pie ? ' A harvest pie after dinner.' : ` Cake after dinner: ${hb}` : '') + ` This week's dinners: ${week.join(', ')}.`;
}
// food_check.py: `days` ship days from a fresh galley at the start of `day`, with the figures for each day
function galleyReport(day, days = 1) {
  const S = { at: (day - 1) * 1440, ...GALLEY_START() }, out = [];
  for (const E of GALLEY_EV.values()) E.k = 0;
  for (let d = day; d < day + days; d++) {
    const st = { day: d, late: 0, tastes: 0, tasted: 0, picked: 0, fresh: 0, produceBinned: 0, spoiled: 0, cakes: 0, batch: 0, trays: 0, mealMax: { breakfast: 0, dinner: 0 }, busy: galleyBusy(d), ate: 0, eaten: 0, grabbed: 0, waits: [], maxWait: 0, maxWho: '', missed: [], cooked: 0, baked: 0, washed: 0, waste: 0, delivered: 0, coldOut: 0, coldMin: Infinity, ready: {}, hours: [] };
    for (let m = (d - 1) * 1440; m < d * 1440; m++) galleyStep(S, m, st);
    const rota = galleyRota(d), staff = [];
    for (const [id, g] of rota) if (g.role) staff.push({ id, role: g.role, wake: g.wake, bedBy: g.bedBy, first: g.blocks.length ? g.blocks[0].from : null, blocks: g.blocks.length });
    st.staff = staff;
    st.waited = st.waits.filter(w => w > 0).length;
    st.produceEnd = produceMeals(S); st.grow = gardenCond(d).grow;
    st.end = { cold: S.cold.meals, servery: S.servery.portions, grab: S.grab.items, dirty: S.dirty, inUse: S.inUse, pots: S.pots.length, wait: S.wait.length };
    delete st.waits; out.push(st);
  }
  for (const E of GALLEY_EV.values()) E.k = 0;
  return out;
}
// time skips (sleep, the debug button): bring the galley up to date before the save
SIM_ADVANCE.push((from, to) => { galleyAdvance(to); });
// the save (section 13's SAVE_EXTRA, when it's there): SHIP.galley goes in as `galley`, and comes back from it
if (typeof SAVE_EXTRA !== 'undefined') SAVE_EXTRA.push(s => { s.galley = galleySave(); });
if (typeof SAVED !== 'undefined' && SAVED && SAVED.galley) galleyLoad(SAVED.galley);

// ---- what you see on Deck 3 ----
// Made when you arrive (after the deck is built, so the deck's unload frees it) and redrawn only when the
// numbers change: food in the servery's five pans, rising with the portions and covered over when they're gone;
// the grab shelf's rolls and wraps (when the shelf leaves them to us: galleyShelfRows);
// dirty plates stacking in the dish pit's sink. Four instanced meshes, no shadows, never tapped.
let GV = null;
// the grab shelf's kit (section 4b, with `live` set) calls this instead of drawing its rolls and wraps: we draw
// them from the stock. A function declaration, so it's there when the first deck is built at load.
function galleyShelfRows(g, ys) { g.userData.live = ys; }
function galleyVisuals() {
  const it = t => ITEMS.find(x => x.t === t), V = { root: deckRoot, key: '' }, nope = () => {};
  const im = (geo, mat, n, parent, cols) => {             // colours first: r128 sizes the colour buffer by the count
    const m = new THREE.InstancedMesh(geo, mat, n); m.castShadow = false; m.receiveShadow = true; m.raycast = nope;
    if (cols) cols.forEach((c, k) => m.setColorAt(k, c));
    m.count = 0; m.frustumCulled = false; parent.add(m); return m;
  };
  const sv = it('Servery'), gs = it('Grab and go'), dp = it('Dish pit');
  const put0 = (m, i, x, y, z, sx, sy, sz) => { _gm.compose(_gpo.set(x, y, z), _gq, _gsc.set(sx, sy, sz)); m.setMatrixAt(i, _gm); };
  if (sv) {                                              // food in the pans (the pan colours), and steel covers over empty ones
    V.food = im(new THREE.BoxGeometry(.42, 1, .28), std('#ffffff', .55), 5, sv.g, MESS.pans.map(m => m.color));
    V.covers = im(new THREE.BoxGeometry(.47, .016, .33), std('#8e989f', .35, .5), 5, sv.g);   // over the whole pan, inside its rim
    // a birthday cake on the tray slide's far end (top .84), with five candles and their flames (one instanced mesh)
    V.cake = new THREE.Mesh(new THREE.CylinderGeometry(.1, .1, .09, 20), std('#f3e4d4', .6));
    V.cake.position.set(1.15, .887, .46); V.cake.visible = false; V.cake.castShadow = false; V.cake.raycast = nope; sv.g.add(V.cake);
    V.candles = im(new THREE.CylinderGeometry(.006, .006, 1, 6), std('#ffffff', .5), 10, sv.g, [...Array(10)].map((_, k) => col(k < 5 ? ['#e86a8a', '#6ab0e8', '#f0c050', '#7ad08a', '#c08ae8'][k] : '#ffcf5a')));
    // the tasting table's two small plates beside it (x .8 and .95, plates' top .852) and what's left on each
    V.taste = im(new THREE.CylinderGeometry(1, 1, 1, 14), std('#ffffff', .5), 4, sv.g, ['#e9e4da', '#e9e4da', '#b5c46a', '#c9884a'].map(c => col(c)));
    for (let k = 0; k < 10; k++) { const a = (k % 5) * 1.2566, r = .055; put0(V.candles, k, 1.15 + r * Math.cos(a), k < 5 ? .955 : .993, .46 + r * Math.sin(a), k < 5 ? 1 : 1.6, k < 5 ? .05 : .012, k < 5 ? 1 : 1.6); }
  }
  if (gs && gs.g.userData.live) {                        // rolls on the top shelf, wraps below: 8 places, one for every 2 items
    V.grab = im(new THREE.SphereGeometry(1, 12, 8), std('#ffffff', .7), 8, gs.g, [...Array(8)].map((_, k) => (k < 4 ? MESS.food.bread : MESS.food.wrap).color));
    const t = TALL.find(t => t.g === gs.g.parent);       // fade with the shelf when it would hide you
    if (t) { V.grab.material.userData.base = { op: 1, tr: false }; t.mats.push(V.grab.material); }
  }
  if (dp) V.plates = im(new THREE.CylinderGeometry(.1, .1, .012, 16), std('#d9d3c4', .45, .05), 24, dp.g);
  if (dp) V.bin = im(new THREE.SphereGeometry(1, 10, 7), std('#2c3a30', .8), 3, dp.g);   // spoiled food, bagged, beside the dish pit
  const mb = it('Menu board');                           // the board's canvas, redrawn with the day's menu; its tap text, live
  if (mb) {
    mb.g.traverse(o => { if (o.material && o.material.map && o.material.map.image && o.material.map.image.getContext) V.board = o.material.map; });
    Object.defineProperty(mb, 'x', { get: () => galleyBoard(), configurable: true });
  }
  return V;
}
const _gm = new THREE.Matrix4(), _gq = new THREE.Quaternion(), _gsc = new THREE.Vector3(), _gpo = new THREE.Vector3();
function galleyShow() {
  if (!deckDef || deckDef.num !== 3) { GV = null; return; }
  if (!GV || GV.root !== deckRoot) GV = galleyVisuals();
  const S = SHIP.galley, p = S.servery.portions, g = Math.ceil(S.grab.items / 2), dirty = Math.min(24, Math.ceil(S.dirty / 3));
  const bk = SHIP.time.day + '|' + (galleyEvDish(S.ev && S.ev.menu) || '');   // redrawn each day, and when an event changes the menu
  if (GV.board && GV.boardDay !== bk) { GV.boardDay = bk; galleyBoardDraw(GV.board, SHIP.time.day); }
  const bags = Math.min(3, Math.ceil((S.bin || 0) / 10)), cake = !!(S.cake && S.cake.out), pie = cake && !!S.cake.pie;
  const T = S.tasting && S.tasting.d === SHIP.time.day && S.tasting.out ? S.tasting : null, tl = T ? Math.ceil(4 * T.left / Math.max(1, T.n || 20)) : 0;
  const key = p + '|' + g + '|' + dirty + '|' + bags + '|' + cake + pie + '|' + tl; if (key === GV.key) return; GV.key = key;
  const put = (m, i, x, y, z, sx, sy, sz) => { _gm.compose(_gpo.set(x, y, z), _gq, _gsc.set(sx, sy, sz)); m.setMatrixAt(i, _gm); };
  if (GV.food) {
    const h = .008 + .05 * Math.min(1, p / FOOD.serveryCap);   // from just over the pans' own food (top at .98) up
    GV.food.count = p > 0 ? 5 : 0; GV.covers.count = p > 0 ? 0 : 5;
    for (let k = 0; k < 5; k++) { put(GV.food, k, -1.2 + k * .6, .978 + h / 2, -.05, 1, h, 1); put(GV.covers, k, -1.2 + k * .6, .98, -.05, 1, 1, 1); }
    GV.food.instanceMatrix.needsUpdate = GV.covers.instanceMatrix.needsUpdate = true;
  }
  if (GV.grab) {
    GV.grab.count = Math.min(8, g);
    const ys = GV.grab.parent.userData.live;          // the shelves' heights: wraps, then rolls
    for (let k = 0; k < 8; k++) put(GV.grab, k, -.3 + (k % 4) * .2, (k < 4 ? ys[1] : ys[0]) + .05, .04, .08, .04, .05);
    GV.grab.instanceMatrix.needsUpdate = true;
  }
  if (GV.plates) {
    GV.plates.count = dirty;
    for (let k = 0; k < 24; k++) put(GV.plates, k, k < 12 ? -.62 : -.28, .914 + (k % 12) * .014, .1, 1, 1, 1);
    GV.plates.instanceMatrix.needsUpdate = true;
  }
  if (GV.cake) { GV.cake.visible = cake; GV.cake.material.color.copy(col(pie ? '#c98a4b' : '#f3e4d4')); GV.candles.count = cake && !pie ? 10 : 0;   // a pie: golden crust, no candles
    GV.candles.instanceMatrix.needsUpdate = true; }
  if (GV.taste) {                                       // the tastes go down in quarters; the plates stay till they're cleared
    GV.taste.count = T ? (tl ? 4 : 2) : 0;
    for (let k = 0; k < 2; k++) {
      const h = .004 + .016 * tl / 4;
      put(GV.taste, k, .8 + k * .15, .847, .46, .06, .01, .06); put(GV.taste, k + 2, .8 + k * .15, .851 + h / 2, .46, .04, h, .04);
    }
    GV.taste.instanceMatrix.needsUpdate = true;
  }
  if (GV.bin) {                                         // up to three bags, one for every 10 meals binned, against the wall by the pit's end
    GV.bin.count = bags;
    [[-1.06, .15, -.19, .14, .15, .13], [-1.06, .15, .09, .14, .15, .13], [-1.06, .39, -.05, .12, .11, .11]].forEach((b, k) => put(GV.bin, k, ...b));
    GV.bin.instanceMatrix.needsUpdate = true;
  }
}
// the menu board (section 4b's menuBoard canvas, 320 x 200), in its own style: the day's breakfast and dinner, and the
// dinner's note (a favourite, the Friday treat, the Sunday vote)
function galleyBoardDraw(t, d) {
  const c = t.image.getContext('2d'), w = t.image.width, h = t.image.height, cap = x => x[0].toUpperCase() + x.slice(1);
  const evd = d === SHIP.time.day && SHIP.galley ? galleyEvDish(SHIP.galley.ev && SHIP.galley.ev.menu) : null;   // an event's menu
  const M = evd ? { breakfast: evd, dinner: evd, note: '' } : galleyMenu(d);
  const line = (txt, y, font, colour) => { let px = parseInt(font.split(' ')[1]); c.fillStyle = colour; do c.font = font.replace(/\d+px/, px + 'px'); while (c.measureText(txt).width > w - 30 && --px > 9); c.fillText(txt, 18, y); };
  c.fillStyle = '#1d2a2a'; c.fillRect(0, 0, w, h);
  line('MESS', 34, '700 24px system-ui,sans-serif', '#e8c06a');
  c.fillStyle = '#9fd9cf'; c.font = '600 15px system-ui,sans-serif'; c.fillText(WEEKDAYS[weekday(d)], w - 18 - c.measureText(WEEKDAYS[weekday(d)]).width, 34);
  line('Breakfast 06:00' + (M.bnote ? '-' + hhmm(galleyServeEnd(d, 'breakfast')) : '') + '  ' + cap(M.breakfast), 66, '600 15px system-ui,sans-serif', '#9fd9cf');
  line('Dinner 17:00  ' + cap(M.dinner), 92, '600 15px system-ui,sans-serif', '#9fd9cf');
  if (M.note) line(cap(M.note), 118, '500 14px system-ui,sans-serif', '#e8eef0');
  const ck = galleyCake(d);
  if (ck && ck.pie) line('Harvest pie after dinner', 148, '600 15px system-ui,sans-serif', '#e8c06a');
  else if (ck) line('Cake after dinner: ' + (ck.who.length ? 'happy birthday, ' + galleyNames(ck.who) + '!' : 'happy ' + ck.name + '!'), 148, '600 15px system-ui,sans-serif', '#e8c06a');
  else {
    const fr = d === SHIP.time.day && SHIP.galley ? produceByCrop(SHIP.galley).slice(0, 2).map(x => GARDEN_CROPS[x[0]].name) : [];
    line(fr.length ? 'Fresh from the garden: ' + fr.join(' and ') : 'Fresh rolls from the galley', 148, '500 15px system-ui,sans-serif', '#e8eef0');
  }
  line('Grab & go by the line', 172, '500 15px system-ui,sans-serif', '#e8eef0');
  c.fillStyle = '#c86b4a'; c.fillRect(18, 186, 60, 3);
  t.needsUpdate = true;
}
// once a frame from the main loop: the galley up to the minute, and on Deck 3, what it looks like
function galleyTick() {
  galleyAdvance(shipNow()); galleyShow();
  if (GALLEY_JOINED.has('player') && typeof ACT !== 'undefined' && !(ACT && ACT.kind === 'queue')) galleyLeave('player');   // walked away from the line
}

