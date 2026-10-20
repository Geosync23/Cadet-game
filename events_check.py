# Starship Cadet: events check (keep in the repo, next to day_check.py)
# Steps a few weeks of ship days with ?nosave and checks the ship's small traditions (section 18, SHIP_TRADITIONS):
#   each event happens when it's due (its weekday, every N days, its day of the year, a birthday) and on no other day;
#   people go to it (an occasional day with nobody, the room full of others, is noted; never anyone fails), only at its time (honorees a little early; staying on up to 25 minutes after) and only to its places;
#   the schedules stay sound on event days (dayReport: sleep, meals, shifts, no double-booking, no gaps);
#   the same day planned twice gives the same events;
#   on the deck, minute by minute through each event (the CrewAgents, no drawing): attendees reach their places,
#   nobody is stuck for more than 10 ship minutes, nobody shares a place; draw calls at the event under BUDGET;
#   the Mail the evening before (18:00), once each; the ship note after each tradition (simNote, once, who came);
#   the voice budget (at most two traditions at once, never two at once in a room; 2+ every weekday) every day of a year; decor on the deck while it's on, and gone after;
#   the player joining by being in the room (a little social, once); the tap line before it;
#   a whole ship year on paper (Pillar 4): the new rhythms (every 2 or 4 weeks, by quarter, by year, from your arrival)
#   due exactly when they should be, the four seasons, the baked traditions (content/traditions) loaded and filled;
#   a ship-wide event on paper: the ion storm's skeleton from day 10, its phases in order, eventMod in each, the same twice.
# Setup and environment as for cadet_test.py.
# Run:  python3 events_check.py BUILD.html [DAYS]     (DAYS defaults to 28, from Day 1, plus days 100 and 300)
import sys
exec(open(__file__.replace('events_check.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright

DAYS = int(sys.argv[2]) if len(sys.argv) > 2 else 28
BUDGET = 450
MORNING_WAIT = set()                                      # was the two early ones (0.34.51), until social 0607's morning() (d3d5b4d) slots them
STEP = 0.05                    # real seconds a step, as day_check

# Pillar 4's rhythms, worked out forwards from each rhythm's first day (not with the game's evDue), for days lo..hi
DUE_NEW = r"""((w, lo, hi) => {
  const s = new Set(), wdOf = d => ((d - 1) % 7 + 7) % 7, seas = d => ['sowing', 'greening', 'harvest', 'lanterns'][Math.floor((((d - 1) % 364) + 364) % 364 / 91)];
  const add = d => { if (d >= lo && d <= hi && (!w.season || [].concat(w.season).includes(seas(d))) && (w.from == null || d >= w.from) && (w.until == null || d <= w.until)) s.add(d); };
  const n = { week: 1, '2weeks': 2, '4weeks': 4 }[w.every || (w.weekday != null ? 'week' : '')];
  if (Array.isArray(w.weekday)) { for (const x of w.weekday) dueNew({ ...w, weekday: x }, lo, hi).forEach(d => s.add(d)); return s; }
  if (w.after === 'arrival') { const a = typeof introArrival === 'function' ? introArrival() : 0;
    if (w.days != null) add(a + w.days); else add(a + 1 + (w.weekday - wdOf(a + 1) + 7) % 7 + 7 * ((w.nth || 1) - 1)); }
  else if (n) { const first = 1 + 7 * ((w.week || 1) - 1) + w.weekday; for (let d = first; d <= hi; d += 7 * n) add(d); for (let d = first - 7 * n; d >= lo; d -= 7 * n) add(d); }
  else if (w.every === 'quarter') for (let q = 0; 91 * q + 1 <= hi; q++) add(91 * q + (w.quarterDay != null ? w.quarterDay : 1 + 7 * ((w.week || 1) - 1) + w.weekday));
  else if (w.every === 'year') for (let y = 0; 364 * y + 1 <= hi; y++) add(364 * y + (w.dayOfYear != null ? w.dayOfYear : 1 + 7 * ((w.week || 1) - 1) + w.weekday));
  return s;
})"""
IS_NEW = "(w => typeof w.every === 'string' || !!w.after || w.season != null || w.from != null || w.until != null || Array.isArray(w.weekday))"

PLANS = r"""(days => {
  const out = { days: [], bad: [], empty: [], ids: SHIP_TRADITIONS.filter(e => !e.flag || (typeof flag === 'function' && flag(e.flag))).map(e => e.id) }, LINGER = 25;   // staying on a little after the end is fine
  const isNew = """ + IS_NEW + r""", dueNew = """ + DUE_NEW + r""", lo = Math.min(...days), hi = Math.max(...days);
  const DUE = new Map(SHIP_TRADITIONS.filter(ev => isNew(ev.when)).map(ev => [ev.id, dueNew(ev.when, lo, hi)]));
  const tagId = tag => { if (SHIP_TRADITIONS.some(e => e.id === tag.slice(3))) return tag.slice(3); const m = /^ev-(.+?)(-(talk|drink|play|water|wash|read|cheer|clap|disc|cocoa))?$/.exec(tag); return m && m[1]; };   // an id first (rec-chiefs-talk ends like an anim)   // cheer, clap, disc: the rec deck's (0.83, RA)
  for (const d of days) {
    const on = eventsOn(d), wd = weekday(d), yd = shipYearDay(d), row = { d, wd: WEEKDAYS[wd].slice(0, 3), ev: [] };
    // due exactly when the table says
    for (const ev of SHIP_TRADITIONS) {
      const w = ev.when, due = !(ev.flag && !(typeof flag === 'function' && flag(ev.flag))) && !(ev.unflag && typeof flag === 'function' && flag(ev.unflag)) && (w.rota ? TRAD_ROTA[w.rota](d) : w.birthday ? schedPeople().some(p => birthdayOf(p) === yd && (typeof aboard !== 'function' || (aboard(p, d) && (typeof guestStay !== 'function' || guestStay(p, d) !== 'leave')))) : w.rotation != null ? ROSTER_ROTATIONS.some(r => (w.rotation === 'after' ? d > r.day && d <= r.day + 7 && weekday(d) === w.weekday : d === r.day + w.rotation) && (w.rotation !== 'after' && w.rotation < 0 ? r.out : r.in).some(id => { const p = schedPeople().find(q => q.id === id); return p && (!w.dept || p.dept === w.dept) && (typeof aboard !== 'function' || aboard(p, d)); })) : DUE.has(ev.id) ? DUE.get(ev.id).has(d) : (w.weekday === wd || (w.every && d % w.every === w.on) || w.yearDay === yd)) && !eventPauses(ev, d) && !(EV_DROPPED.get(d) || []).includes(ev.id) && !(ev.skip && ev.skip(d));   // a ship-wide event's quiet days; the voice budget
      if (due !== on.some(e => e.id === ev.id)) out.bad.push(d + ' ' + ev.id + (due ? ' due but not on' : ' on but not due'));
    }
    const S = schedData(), went = {}, places = {};
    for (const p of schedPeople()) for (const s of planDay(p, d)) {
      if (!s.tag || !/^ev-/.test(s.tag)) continue;
      const id = tagId(s.tag), e = on.find(x => x.id === id), B = (d - 1) * 1440;
      if (!e) { out.bad.push(d + ' ' + p.id + ' at ' + id + ', which is not on'); continue; }
      if (s.from < B + e.from - Math.max(e.ev.early || 0, p.id === e.ev.host ? 5 : 0, e.ev.meal && typeof TRAD_LINE !== 'undefined' ? TRAD_LINE[1] : 0) ||   // the sim plans a host 5 minutes early; a meal tradition's diners sit as the line serves them, up to TRAD_LINE[1] early (sim 0.26.41)
         s.to > B + e.to + LINGER) out.bad.push(d + ' ' + p.id + ' at ' + id + ' ' + hhmm(s.from - B) + '-' + hhmm(s.to - B) + ' outside ' + hhmm(e.from) + '-' + hhmm(e.to));
      const pools = eventOpts(e.ev, p).map(([n, k]) => S.shared.get(n + '|' + k) || []).flat().map(pl => pl.id);
      if (!pools.includes(s.placeId)) out.bad.push(d + ' ' + p.id + ' at ' + id + ' in ' + s.placeId + ', not one of its places');
      (went[id] = went[id] || new Set()).add(p.id); (places[id] = places[id] || new Set()).add(s.placeId);
    }
    for (const e of on) {
      const want = schedPeople().filter(p => eventPlan(p, d).some(x => x.id === e.id)).length, n = went[e.id] ? went[e.id].size : 0;
      const cap = new Set(e.ev.where.flatMap((w, i) => S.shared.get(w.deck + '|' + (w.room ? 'ev:' + e.id + ':' + i : w.pool)) || []).map(pl => pl.id)).size;
      if (!n) out.empty.push(d + ' ' + e.id + ': nobody went (' + want + ' meant to; the room was full)');
      row.ev.push({ id: e.id, names: e.names, at: hhmm(e.from) + '-' + hhmm(e.to), want, went: n, places: places[e.id] ? places[e.id].size : 0, cap });
    }
    // a tradition's held places (eventPlaces) are only for those going while it's on: nobody else (a meal, the gym, the
    // bar) sits in one then (0.34.51, the user: no tradition shares a room or place with a meal or other use)
    for (const e of on) {
      const held = new Set(eventPlaces(e)), B = (d - 1) * 1440;
      for (const p of schedPeople()) for (const s of planDay(p, d)) if (s.placeId && held.has(s.placeId) && s.from < B + e.to && B + e.from < s.to && tagId(s.tag || '') !== e.id)
        out.bad.push(d + ' ' + p.id + ' in ' + s.placeId + ' (' + (s.tag || s.act) + ') ' + hhmm(s.from - B) + '-' + hhmm(s.to - B) + ', held for ' + e.id);
    }
    const r = dayReport(d);
    for (const k of ['short', 'meals', 'work', 'double', 'gaps']) if (r[k].length) out.bad.push(d + ' dayReport ' + k + ': ' + r[k].slice(0, 4).join(', '));
    out.days.push(row);
  }
  return out;
})"""

# the same day twice: every event segment, after clearing the caches and planning other days in between
SAME = r"""(d => {
  const sig = () => schedPeople().map(p => planDay(p, d).filter(s => s.tag && /^ev-/.test(s.tag)).map(s => p.id + s.from + s.placeId + s.tag).join()).join('|');
  const a = sig(); SHIP_DAYS.clear(); EV_DAYS.clear(); for (const x of [d + 3, d - 2, d + 1]) shipDay(x); SHIP_DAYS.delete(d);
  return a === sig() && a.length > 0;
})"""

# one event on its deck, minute by minute, from 30 minutes before to its end
SIM = r"""(async ({ d, id, step }) => {
  const e = eventsOn(d).find(x => x.id === id), B = (d - 1) * 1440;
  const att = new Map();                                 // person -> their event segment
  for (const p of schedPeople()) for (const s of planDay(p, d)) if (s.tag && s.tag.startsWith('ev-' + id) && s.placeId) att.set(p.id, s);
  const decks = [...new Set([...att.values()].map(s => s.deck))];
  const out = { id, d, decks: [] };
  for (const n of decks) {
    const r = { n, att: 0, reached: 0, notReached: [], stuck: 0, stuckWho: '', shared: 0, sharedWho: [], noPath: [], calls: 0, crew: 0, decor: 0 };
    const mine = [...att.entries()].filter(([, s]) => s.deck === n); r.att = mine.length;
    const got = new Set();
    SHIP.galley = null;                                  // the galley starts fresh that morning (a jump of weeks has no hover carts)
    setShipNow(B + e.from - 30); goToDeck(n);
    for (let k = 0; B + e.from - 30 + k * step * SHIP_RATE < B + e.to; k++) {
      const now = B + e.from - 30 + k * step * SHIP_RATE; setShipNow(now); updateDeckCrew(step);
      const held = new Map();
      for (const a of DECK_CREW) {
        if (a.stuckMax > r.stuck) { r.stuck = a.stuckMax; r.stuckWho = a.p.id + ' ' + hhmm(now - B); }
        if (a.noPath && !r.noPath.includes(a.p.id)) r.noPath.push(a.p.id);
        if (a.settled && a.spot) {
          if (held.has(a.spot.id)) { r.shared++; if (r.sharedWho.length < 4) r.sharedWho.push(a.spot.id + ' ' + held.get(a.spot.id) + '/' + a.p.id + ' ' + hhmm(now - B)); }
          held.set(a.spot.id, a.p.id);
          const s = att.get(a.p.id); if (s && s.deck === n && now >= s.from && now < s.to && a.spot.id === s.placeId) got.add(a.p.id);
        }
      }
      if (Math.abs(now - (B + e.from + Math.min(30, (e.to - e.from) / 2))) < step * SHIP_RATE / 2 + 1e-9) {   // a frame over the crowd, at the event
        const c = DECK_CREW.length ? new THREE.Vector3(...[...att.keys()].map(i => DECK_CREW.find(a => a.p.id === i)).filter(Boolean).reduce((s, a, _, l) => [s[0] + a.x / l.length, 0, s[2] + a.z / l.length], [0, 0, 0])) : cellPos(...LIFT_AT);
        player.obj.position.copy(c); target.copy(c).setY(.7);
        eventsTick(); window.__skip = false; window.__step(1, 1); window.__step(2, 16); setShipNow(now);   // settled: the cutaway's fades done
        r.calls = renderer.info.render.calls; r.crew = DECK_CREW.length; r.decor = EV_DECOR.g ? EV_DECOR.g.children.length : 0;
      }
    }
    r.reached = mine.filter(([i]) => got.has(i)).length;
    r.notReached = mine.filter(([i]) => !got.has(i)).map(([i, s]) => i + '>' + s.placeId + ' ' + hhmm(s.from - B)).slice(0, 6);
    out.decks.push(r);
  }
  return out;
})"""


# a ship-wide event on paper (Pillar 3): the ion storm's skeleton from day 10, stepped every 10 ship minutes to day 15,
# twice from a clean slate. Phases in order, eventMod right in each phase, the end logged with a band and traces.
STORM = r"""(() => {
  const run = () => {
    const keep = { e: SHIP.event, log: SHIP.eventLog.slice(), tr: SHIP.traces.slice() };
    SHIP.event = null; SHIP.eventLog.length = 0; SHIP.traces.length = 0; const m0 = MEETINGS.splice(0);
    const recKeep = typeof recClean === 'function' ? { rec: JSON.stringify(SHIP.rec), f: ['rec.allHands', 'rec.filmMoved'].map(k => [k, SHIP.flags && SHIP.flags[k]]) } : null;   // the rec deck's first all-hands comes with the storm's first address (0.83): from a clean slate each run
    if (recKeep) { SHIP.rec = recClean(null); for (const [k] of recKeep.f) if (SHIP.flags) delete SHIP.flags[k]; }
    const due = eventDueDay();                           // as in a new game
    eventStart('ionStorm', 10); EV_DAYS.clear();
    const a0 = ADDRESSES.length, mails = [], ms = MEETINGS.length, send = typeof mailSend === 'function' ? mailSend : null;
    if (send) mailSend = m => { mails.push(Math.floor(m.at / 1440) + 1 + ' ' + hhmm(m.at % 1440) + ' ' + m.subject); };
    const news = [], fmt = x => Math.floor(x.born / 1440) + 1 + ' ' + hhmm(x.born % 1440) + ' ' + x.id + ' (' + x.seed.length + ' know): ' + x.lines[0];
    const real = typeof NEWS !== 'undefined' && typeof newsAdd === 'function', n0 = real ? (socInit(), NEWS.length) : 0;   // section 20's own, or a stand-in
    if (!real) window.newsAdd = x => { news.push(fmt(x)); return x; };
    const on = [10, 11, 13, 16].map(d => { const o = eventOn(d); return d + ':' + (o ? o.day + ' ' + o.phases.map(p => p.id + '@' + p.from).join(' ') : '-'); });
    const gath = [10, 13].map(d => eventGatherings(d).map(g => d + ' ' + g.id + ' ' + g.where + ' ' + hhmm(g.at) + ' ' + g.len).join('; '));
    const steps = [], sig = [], mods = {};
    const paused = [9, 10, 11, 12, 13, 14].map(d => d + ':' + eventsOn(d).map(e => e.id).join('+'));
    for (let t = 9 * 1440; t <= 17 * 1440; t += 10) {
      const n = eventNow(t);
      const o = eventAdvance(t, true); if (o.length) steps.push('day ' + (Math.floor(t / 1440) + 1) + ' ' + hhmm(t % 1440) + ' ' + o.join(', '));
      const k = n ? n.phase : '-', m = [eventMod('wear', 'power', t), eventMod('wear', 'comms', t), eventMod('effect', 'flicker', t)];
      sig.push(k + ':' + m.join(',')); mods[k] = m;
      if (n && n.phase === 'escalation') eventScore('blackout', 1);   // a stand-in: a minute of blackout per step of the escalation
      const g = eventMod('galley', 'menu', t); if (g) mods.menu = g;
    }
    if (send) mailSend = send;
    if (real) { for (const x of NEWS.splice(n0)) { news.push(fmt(x)); delete SHIP.knows[x.id]; } } else delete window.newsAdd;
    const addr = ADDRESSES.slice(a0).map(x => Math.floor(x.at / 1440) + 1 + ' ' + hhmm(x.at % 1440) + ' ' + x.text);
    const meets = MEETINGS.slice(ms).map(m => m.id + ' day ' + (Math.floor(m.at / 1440) + 1) + ' ' + hhmm(m.at % 1440) + ' ' + m.script);
    ADDRESSES.length = a0; MEETINGS.length = 0; MEETINGS.push(...m0); EV_DAYS.clear();
    const res = { steps, sig: sig.join('|'), mods, log: JSON.parse(JSON.stringify(SHIP.eventLog)), traces: SHIP.traces.slice(), left: SHIP.event, addr, mails, meets, paused, news, on, gath, due,
      scripts: Object.keys(MEETING_SCRIPTS), lines: Object.values(MEETING_SCRIPTS).map(sc => sc.lines.length), modAfter: eventMod('wear', 'power', 12 * 1440) };
    SHIP.event = keep.e; SHIP.eventLog.length = 0; SHIP.eventLog.push(...keep.log); SHIP.traces.length = 0; SHIP.traces.push(...keep.tr);
    if (recKeep) { SHIP.rec = recClean(JSON.parse(recKeep.rec)); for (const [k, v] of recKeep.f) if (SHIP.flags) { if (v === undefined) delete SHIP.flags[k]; else SHIP.flags[k] = v; } EV_DAYS.clear(); }
    return res;
  };
  const a = run(), b = run();
  return { a, same: a.sig === b.sig && JSON.stringify(a.log) === JSON.stringify(b.log) && a.addr.join() === b.addr.join() && a.mails.join() === b.mails.join(), due: a.due, cal: upcomingTraditions(0, 7 * 1440).slice(0, 3) };
})()"""

# a live ion storm (0.34.9): started on day 10 and played through on the deck at the moments that matter: Calder's
# briefing in the Works bay (the panel, the cast, a choice), the front at 14:00 on day 11 (the jolt, the address), the
# all-clear in the observation room (walking out mails the gist), then on to the end (the log, the traces, the debrief)
LIVE = r"""(() => {
  const dress = [], hadDress = typeof dressShow === 'function', ds = hadDress ? dressShow : null;
  const spy = l => { const k = l.map(x => typeof x === 'string' ? x : x.id + (x.lines ? '[' + x.lines.length + ']' : '')).join('+'); if (dress[dress.length - 1] !== k) dress.push(k); };
  // with the deck architect's dressShow in the game's own scope, a window stand-in is never seen: wrap the real one there
  if (hadDress) dressShow = l => { spy(l); return ds(l); }; else window.dressShow = spy;
  const D = {}, mails = [], send = mailSend; mailSend = m => { mails.push(Math.floor(m.at / 1440) + 1 + ' ' + hhmm(m.at % 1440) + ' ' + m.subject); };
  const keep = { e: SHIP.event, log: SHIP.eventLog.slice(), tr: SHIP.traces.slice() };
  SHIP.event = null; SHIP.eventLog.length = 0; SHIP.traces.length = 0; MEETINGS.length = 0; FEEL.log.length = 0; FEEL_DONE.clear();
  const put = (n, id) => { if (deckDef.num !== n) goToDeck(n); const at = DECKS[n].places.find(p => p.id === id).at;
    player.obj.position.copy(cellPos(...nearestOpen(...cellPos(...at).toArray().filter((_, i) => i !== 1), player))); target.copy(player.obj.position).setY(.7); };
  const tick = (a, b) => { for (let t = a; t <= b; t++) { setShipNow(t); eventsTick(); } };
  const frames = () => { window.__skip = false; window.__step(1, 1); window.__step(2, 16); return renderer.info.render.calls; };
  skipTo(9 * 1440 + 7 * 60); eventStart('ionStorm', 10); EV_DAYS.clear(); eventAdvance(shipNow(), true);
  // the briefing: day 10, 09:15, the Works bay (0.70.1: the 09:00 shift)
  put(5, '5-jobboard-1'); tick(9 * 1440 + 8 * 60 + 50, 9 * 1440 + 9 * 60 + 16);
  D.briefing = DIALOGUE ? { open: true, cast: Object.fromEntries(Object.entries(DIALOGUE.cast).map(([k, p]) => [k, p.name])), first: dialogueView() } : { open: false };
  const devDlg = document.getElementById('devDlg');   // section 19's panel (deviceDialogue) when the device is merged, else the plain strip
  D.panel = !!(DIALOGUE_EL && !DIALOGUE_EL.hidden && DIALOGUE_EL.textContent.length > 5) || !!(devDlg && !devDlg.hidden && devDlg.textContent.length > 5);
  D.calls1 = frames();
  const seen = []; let n = 0;
  while (DIALOGUE && n++ < 30) { const v = dialogueView(); seen.push((v.choices ? '[choice] ' + v.choices.join(' / ') : v.name + ': ' + v.text)); dialogueStep(v.choices ? 0 : undefined); }
  D.lines = seen; D.mine = { ...SHIP.event.mine }; D.closed = !DIALOGUE;
  D.choiceNotes = (window.__notes || []).filter(x => x.kind === 'choice').map(x => x.script + ':' + x.k + ':' + x.who.length);   // the ship note for your reply
  // the front: day 11, 14:00, on Deck 3
  skipTo(10 * 1440 + 13 * 60 + 50); put(3, '3-grab-1'); tick(10 * 1440 + 13 * 60 + 51, 10 * 1440 + 14 * 60 + 1);
  D.feel = FEEL.log.map(f => f.kinds.join('+')); D.banner = !!(ADDRESS_EL && !ADDRESS_EL.hidden) || !!(document.getElementById('devAddr') && !document.getElementById('devAddr').hidden); D.flicker = FEEL.flicker; D.calls2 = frames();   // the banner: the plain one, or section 19's
  // the all-clear: day 13, 10:00, the observation room; then walk out to the bridge
  skipTo(12 * 1440 + 9 * 60 + 50); put(1, '1-tea-1'); tick(12 * 1440 + 9 * 60 + 51, 12 * 1440 + 10 * 60 + 1);
  D.allClear = DIALOGUE ? dialogueView() : null; D.calls3 = frames();
  put(1, '1-works-1'); tick(12 * 1440 + 10 * 60 + 2, 12 * 1440 + 10 * 60 + 2); D.walked = !DIALOGUE;
  skipTo(15 * 1440 + 10);
  D.log = JSON.parse(JSON.stringify(SHIP.eventLog)); D.traces = SHIP.traces.slice(); D.left = SHIP.event; D.mails = mails;
  D.dress = dress; if (hadDress) dressShow = ds; else delete window.dressShow;
  mailSend = send; SHIP.event = keep.e; SHIP.eventLog.length = 0; SHIP.eventLog.push(...keep.log); SHIP.traces.length = 0; SHIP.traces.push(...keep.tr);
  MEETINGS.length = 0; EV_DAYS.clear(); if (DIALOGUE) dialogueEnd(true); if (ADDRESS_EL) ADDRESS_EL.hidden = true; if (typeof deviceAddress === 'function') deviceAddress(null);
  return D;
})()"""

# occasions (C10, 0.34.11): a commendation on day 16 -> the ready-room summons on day 17 at 11:00 (the door open, the
# meeting played in the room, kept), the Captain's table on day 20 (booked the day before, the galley's batch, missed),
# a progress talk asked for on day 18, and nothing booked without a commendation
OCC = r"""(() => {
  const R = {}, mails = [], send = mailSend; mailSend = m => { mails.push(Math.floor(m.at / 1440) + 1 + ' ' + hhmm(m.at % 1440) + ' ' + m.subject); };
  const keep = { o: SHIP.occasions.slice(), c: SHIP.commendations.slice(), e: SHIP.event, tr: SHIP.traces.slice() };
  SHIP.occasions.length = 0; SHIP.commendations.length = 0; SHIP.event = null; MEETINGS.length = 0;
  const tick = (a, b) => { for (let t = a; t <= b; t++) { setShipNow(t); eventsTick(); } };
  skipTo(16 * 1440 + 360); R.none = SHIP.occasions.length;
  SHIP.commendations.push({ event: 'ionStorm', day: 16 });
  skipTo(16 * 1440 + 400); R.booked = SHIP.occasions.map(r => r.key + ' ' + hhmm(r.at % 1440) + ' ' + r.status);
  R.doorBefore = occasionDoorOpen(1, 'R', 16 * 1440 + 600); R.doorAt = occasionDoorOpen(1, 'R', 16 * 1440 + 655);
  skipTo(16 * 1440 + 640); goToDeck(1); const b = ROOM_BOX.R;   // inside the ready room (its door is section 14's doorOpenFor, not in yet)
  player.obj.position.copy(cellPos(Math.floor((b.i0 + b.i1) / 2), Math.floor((b.j0 + b.j1) / 2))); target.copy(player.obj.position).setY(.7);
  R.room = roomAt(...player.here());
  tick(16 * 1440 + 641, 16 * 1440 + 661);
  R.open = DIALOGUE ? DIALOGUE.id : null; const seen = []; let n = 0;
  while (DIALOGUE && n++ < 20) { const v = dialogueView(); seen.push(v.choices ? '[choice]' : v.who + ': ' + v.text); dialogueStep(v.choices ? 2 : undefined); }
  R.lines = seen; tick(16 * 1440 + 662, 16 * 1440 + 690);
  R.after = SHIP.occasions.map(r => r.key + ' ' + r.status);
  R.ask = !!occasionAsk('progressTalk', 17 * 1440 + 840); const cOff = [19, 20, 21, 22, 23, 24, 25].find(d => !isWorkDay(schedPeople().find(p => p.id === 'calder'), d)); R.askOff = !!occasionAsk('progressTalk', (cOff - 1) * 1440 + 840);   // on a day Calder's off (the roster's days off)
  skipTo(18 * 1440 + 900); R.table = SHIP.occasions.map(r => r.key + ' ' + hhmm(r.at % 1440) + ' ' + r.status);
  R.batch = eventMod('galley', 'batch', 19 * 1440 + 900); R.noBatch = eventMod('galley', 'batch', 18 * 1440 + 900);
  skipTo(20 * 1440 + 60); R.end = SHIP.occasions.map(r => r.key + ' ' + r.status); R.mails = mails; R.traces = SHIP.traces.slice();
  mailSend = send; SHIP.occasions.length = 0; SHIP.occasions.push(...keep.o); SHIP.commendations.length = 0; SHIP.commendations.push(...keep.c);
  SHIP.event = keep.e; SHIP.traces.length = 0; SHIP.traces.push(...keep.tr); MEETINGS.length = 0; if (DIALOGUE) dialogueEnd(true);
  return R;
})()"""

# the bridge invite (0.34.35): Vance at breakfast in the mess on day 22, the day before the first bridge hour; a reply
# sets flag bridge.invited and bridge hour is then on day 23; slept through (day 50), it's missed, the gist comes and the flag too
INVITE = r"""(() => {
  const R = {}, mails = [], send = mailSend; mailSend = m => { mails.push(Math.floor(m.at / 1440) + 1 + ' ' + hhmm(m.at % 1440) + ' ' + m.subject); };
  const keep = SHIP.occasions.slice(); SHIP.occasions.length = 0; MEETINGS.length = 0; flagSet('bridge.invited', null);
  const tick = (a, b) => { for (let t = a; t <= b; t++) { setShipNow(t); eventsTick(); } };
  R.eves = [...Array(120).keys()].filter(d => d >= 15 && occBridgeEve(d)); R.before = eventsOn(23).some(e => e.id === 'bridge-hour');
  tick(21 * 1440 + 300, 21 * 1440 + 300); R.booked = SHIP.occasions.map(r => r.key + ' ' + hhmm(r.at % 1440) + ' ' + r.status);   // set, not skipped: earlier parts leave the clock past day 22
  const r = SHIP.occasions.find(x => x.id === 'bridgeInvite'), v = schedPeople().find(p => p.id === 'vance');
  R.vanceThere = !!r && planDay(v, 22).some(s => s.placeId && s.placeId.startsWith('3-mess-') && s.from <= r.at && s.to >= r.at);
  R.appt = typeof APPTS !== 'undefined' ? APPTS.some(a => /^bridgeInvite/.test(a.id)) : false;
  if (r) {
    goToDeck(3); const b = ROOM_BOX.M; player.obj.position.copy(cellPos(Math.floor((b.i0 + b.i1) / 2), Math.floor((b.j0 + b.j1) / 2))); target.copy(player.obj.position).setY(.7);
    tick(21 * 1440 + 301, r.at + 1);
    R.open = DIALOGUE ? DIALOGUE.id : null; const seen = []; let n = 0;
    while (DIALOGUE && n++ < 20) { const v = dialogueView(); seen.push(v.choices ? '[choice]' : v.who + ': ' + v.text); if (v.choices) R.flagBefore = !!flag('bridge.invited'); dialogueStep(v.choices ? 1 : undefined); }
    R.lines = seen; R.flagAfter = !!flag('bridge.invited'); tick(r.at + 2, r.at + r.len + 2);
  }
  R.after = SHIP.occasions.map(r => r.key + ' ' + r.status); R.on23 = eventsOn(23).some(e => e.id === 'bridge-hour');
  R.going = schedPeople().filter(p => planDay(p, 23).some(s => s.tag && s.tag.startsWith('ev-bridge-hour'))).length;
  skipTo(21 * 1440 + 18 * 60 + 5); R.mails1 = mails.slice();
  // slept through: the next eve (day 50) with no flag, skipped straight to 09:00, past Vance's breakfast
  SHIP.occasions.length = 0; MEETINGS.length = 0; flagSet('bridge.invited', null); mails.length = 0;
  skipTo(48 * 1440 + 22 * 60); skipTo(49 * 1440 + 540);
  R.slept = SHIP.occasions.map(r => r.key + ' ' + r.status); R.sleptFlag = !!flag('bridge.invited'); R.mails2 = mails.slice();
  mailSend = send; SHIP.occasions.length = 0; SHIP.occasions.push(...keep); MEETINGS.length = 0; flagSet('bridge.invited', null); if (DIALOGUE) dialogueEnd(true);
  return R;
})()"""

# the hooks for others (0.34.13): the party through eventPlan (in play, day 13), eventRoutines, eventGuestDays,
# a one-off (Pell's show) added for a later day and planned like a tradition
HOOKS = r"""(() => {
  const R = {};
  R.partyDay = eventsOn(13).map(e => e.id); R.party11 = eventsOn(11).some(e => e.id === 'party');
  R.partyGoing = schedPeople().filter(p => planDay(p, 13).some(s => s.tag && s.tag.startsWith('ev-party'))).length;
  R.partyPlaces = [...new Set(schedPeople().flatMap(p => planDay(p, 13).filter(s => s.tag && s.tag.startsWith('ev-party')).map(s => s.placeId)))].slice(0, 4);
  R.routines = [11 * 1440 + 900, 12 * 1440 + 400, 12 * 1440 + 700, 13 * 1440 + 100].map(t => eventRoutines(t).map(r => r.rule).join(','));
  R.guest = eventGuestDays({ event: 'ionStorm', stay: 3 }); R.noGuest = eventGuestDays({ event: 'nope', stay: 3 });
  R.owed = schedPeople().filter(p => callOwed(p, 10)).length;
  const d = Math.floor(shipNow() / 1440) + 3;
  R.added = eventOneOff({ id: 'pell-show', name: 'Pell\'s music boxes', day: d, at: [1230, 1290], where: [{ deck: 4, pool: 'music' }], host: 'pell', chance: .3, anim: null, here: 'Shh, the next one plays a waltz.' });
  R.again = eventOneOff({ id: 'pell-show', name: 'x', day: d, at: [1230, 1290], where: [{ deck: 4, pool: 'music' }] });
  R.today = eventOneOff({ id: 'y', name: 'y', day: d - 2, at: [1230, 1290], where: [{ deck: 4, pool: 'music' }] });
  R.oneOffOn = eventsOn(d).map(e => e.id);
  R.hostFlag = eventPlan(schedPeople().find(p => p.id === 'pell'), d).some(x => x.id === 'pell-show' && x.host);
  R.hostFree = eventFree(schedPeople().find(p => p.id === 'pell'), d, 1230, 1290);
  R.oneOffGoing = schedPeople().filter(p => planDay(p, d).some(s => s.tag && s.tag.startsWith('ev-pell-show'))).map(p => p.id);
  SHIP.events.oneOffs.length = 0; SCHED_DATA = null; EV_DAYS.clear(); SHIP_DAYS.clear();
  return R;
})()"""

# the diplomatic visit (event 2, 0.34.16) on paper, twice: after the storm (logged, ending day 16) it's due from day 23;
# run from day 23 to its end; phases, addresses, Mail, meetings, the farewell as a gathering, the guests' days, the
# formal dinners' galley batch on days 3 and 5 only, and the greeting's cast with the Veyli names
DIPLO = r"""(() => {
  const keep = { e: SHIP.event, log: SHIP.eventLog.slice(), tr: SHIP.traces.slice(), m: MEETINGS.splice(0), draft: SHIP_EVENTS.diplomatic.draft };
  SHIP_EVENTS.diplomatic.draft = false;                  // as it will be when it's switched on
  const run = () => {
    SHIP.event = null; SHIP.eventLog.length = 0; SHIP.traces.length = 0; MEETINGS.length = 0; EV_DAYS.clear();
    SHIP.eventLog.push({ id: 'ionStorm', startDay: 10, endDay: 16, band: 'smooth', threads: {}, mine: {} });
    const due = eventDueDay(), sd = due.day, a0 = ADDRESSES.length, mails = [], send = mailSend;
    mailSend = m => { mails.push(Math.floor(m.at / 1440) + 1 - sd + ' ' + hhmm(m.at % 1440) + ' ' + m.subject); };
    eventStart('diplomatic', sd); EV_DAYS.clear();
    const steps = [], batch = [], guestsOn = [];
    for (let t = (sd - 1) * 1440; t <= (sd + 9) * 1440; t += 15) {
      const o = eventAdvance(t, true); if (o.length) steps.push((Math.floor(t / 1440) + 1 - sd) + ' ' + hhmm(t % 1440) + ' ' + o.join(', '));
      if (t % 1440 === 900) { const b = eventMod('galley', 'batch', t); batch.push((Math.floor(t / 1440) + 1 - sd) + ':' + (b ? b.meals : '-')); }
      if (t % 1440 === 900 && eventMod('effect', 'guests', t)) guestsOn.push(Math.floor(t / 1440) + 1 - sd);
    }
    mailSend = send;
    const R = { due, steps, batch, guestsOn, mails, addr: ADDRESSES.slice(a0).map(x => x.text.slice(0, 60)), meets: MEETINGS.map(m => m.id + ' ' + (Math.floor(m.at / 1440) + 1 - sd) + ' ' + hhmm(m.at % 1440)),
      farewell: eventsOn(sd + 7).filter(e => e.id === 'farewell').map(e => e.from + '-' + e.to), going: schedPeople().filter(p => planDay(p, sd + 7).some(s => s.tag && s.tag.startsWith('ev-farewell'))).length,
      guests: ['teshavi', 'kesrin'].map(id => { const g = typeof GUESTS !== 'undefined' && GUESTS.find(x => x.id === id); return g ? id + ':' + (eventGuestDays(g) || []).map(d => d - sd).join('-') : id + ':-'; }),
      log: SHIP.eventLog.slice(1).map(l => l.band + ' ' + JSON.stringify(l.threads)), traces: SHIP.traces.slice() };
    ADDRESSES.length = a0; return R;
  };
  const a = run(), b = run();
  const sc = MEETING_SCRIPTS.veyliGreeting; dialogueShow('veyliGreeting', { id: 'veyliGreeting', who: ['marrow', 'vance', 'saruth', 'teshavi', 'kesrin'], at: shipNow() });
  const names = []; let n = 0; while (DIALOGUE && n++ < 20) { const v = dialogueView(); names.push(v.choices ? '[choice]' : v.who); dialogueStep(v.choices ? 1 : undefined); }
  // live: the greeting plays when you're in the shuttle bay at 10:00 on the visit's day 2
  SHIP.event = null; SHIP.eventLog.length = 0; SHIP.eventLog.push({ id: 'ionStorm', startDay: 10, endDay: 16, band: 'smooth', threads: {}, mine: {} }); MEETINGS.length = 0; EV_DAYS.clear();
  const sd = a.due.day; eventStart('diplomatic', sd); EV_DAYS.clear();
  skipTo((sd + 1) * 1440 + 580); goToDeck(5); const bx = ROOM_BOX.S;
  player.obj.position.copy(cellPos(Math.floor((bx.i0 + bx.i1) / 2), Math.floor((bx.j0 + bx.j1) / 2))); target.copy(player.obj.position).setY(.7);
  for (let t = (sd + 1) * 1440 + 581; t <= (sd + 1) * 1440 + 602; t++) { setShipNow(t); eventsTick(); }
  const live = { room: roomAt(...player.here()), open: DIALOGUE ? DIALOGUE.id : null, first: DIALOGUE ? dialogueView().who : null };
  if (DIALOGUE) dialogueEnd(true); if (typeof deviceAddress === 'function') deviceAddress(null); if (ADDRESS_EL) ADDRESS_EL.hidden = true;
  SHIP_EVENTS.diplomatic.draft = keep.draft;
  SHIP.event = keep.e; SHIP.eventLog.length = 0; SHIP.eventLog.push(...keep.log); SHIP.traces.length = 0; SHIP.traces.push(...keep.tr); MEETINGS.length = 0; MEETINGS.push(...keep.m); EV_DAYS.clear();
  return { a, same: JSON.stringify(a) === JSON.stringify(b), names, live };
})()"""

ok = True
def fail(msg):
    global ok
    ok = False
    print('  FAIL', msg)

with sync_playwright() as pw:
    g = Game(pw, sys.argv[1])
    g.ev("window.__realTick = tickShip; tickShip = () => {}")
    g.ev("player.steer = null; player.stop()")
    print(f"{g.ev('SHIP_TRADITIONS.length')} events: " + ', '.join(g.ev("SHIP_TRADITIONS.map(e => e.id)")))
    days = list(range(1, DAYS + 1)) + [100, 300]
    # and each tradition's first day in the year, when it isn't among those (seasonal, yearly, life moments: Pillar 4)
    first = g.ev("Object.fromEntries(SHIP_TRADITIONS.filter(e => !e.when.birthday).map(e => [e.id, [...Array(364).keys()].map(x => x + 1).find(x => eventsOn(x).some(o => o.id === e.id)) || null]))")
    days += sorted({d for i, d in first.items() if d and not any(d == x for x in days) and not g.ev(f"{days}.some(x => eventsOn(x).some(o => o.id === '{i}'))")})

    # 1. on paper: due days, who goes, where, and the schedules
    r = g.ev(f"({PLANS})({days})")
    for row in r['days']:
        if row['ev']:
            print(f"Day {row['d']} {row['wd']}: " + '; '.join(f"{e['id']}{' (' + e['names'] + ')' if e['names'] else ''} {e['at']} went {e['went']}/{e['want']} (places {e['cap']})" for e in row['ev']))
    seen = {e['id'] for row in r['days'] for e in row['ev'] if e['went']}
    for x in r['empty']: print('  note:', x)
    for i in r['ids']:
        if i not in seen and i in MORNING_WAIT: print(f"  WAITING: {i}: nobody goes until section 14's morning() slots a gathering before breakfast (asked of the sim engineer at 0.34.51); then drop it from MORNING_WAIT")
        elif i not in seen: fail(f"{i} never happened (or nobody ever went) in the days checked")
    for b in r['bad'][:20]: fail(b)
    if len(r['bad']) > 20: print(f"  ... and {len(r['bad']) - 20} more")
    same = g.ev(f"({SAME})(4)")
    print('Plans the same twice (day 4):', same)
    if not same: fail('day 4 planned differently the second time')

    # 1b. a whole ship year on paper (Pillar 4): the new rhythms due exactly when they should be, from day 0 (your
    # arrival) to day 364; the four seasons; the baked traditions (content/traditions, the TRADITIONS block) loaded
    yr = g.ev("""(() => {
      const isNew = """ + IS_NEW + """, dueNew = """ + DUE_NEW + """, out = { bad: [], count: {}, seasons: [], errors: TRAD_ERRORS.slice(), baked: [] };
      for (const ev of SHIP_TRADITIONS.filter(e => isNew(e.when))) {
        const due = dueNew(ev.when, 0, 364), on = new Set();
        for (let d = 0; d <= 364; d++) if (eventsOn(d).some(e => e.id === ev.id)) on.add(d);
        if (ev.flag && !(typeof flag === 'function' && flag(ev.flag))) { if (on.size) out.bad.push(ev.id + ' on without its flag ' + ev.flag); out.count[ev.id] = []; continue; }
        for (const d of due) if (!on.has(d) && !eventPauses(ev, d) && !(EV_DROPPED.get(d) || []).includes(ev.id) && !(ev.skip && ev.skip(d))) out.bad.push(ev.id + ' due on day ' + d + ' but not on');
        for (const d of on) if (!due.has(d)) out.bad.push(ev.id + ' on day ' + d + ' but not due');
        out.count[ev.id] = [...on].sort((a, b) => a - b);
      }
      // the voice budget, every day of the year (0.34.51, 0.60.7): at most two traditions at once, never two at once in
      // one room (birthdays aside), and what it left out; and every weekday (Monday to Friday) has 2 or more
      out.dropped = [];
      for (let d = 0; d <= 364; d++) {
        const all = eventsOn(d).filter(e => SHIP_TRADITIONS.includes(e.ev) && !e.ev.when.birthday), recOnly = e => e.ev.where.every(w => w.deck === 7);
        const t = all.filter(e => !recOnly(e));   // the rec deck's own are budgeted among themselves (0.83, RA): one at a time in a room, checked below with the rest
        for (const x of t) if (t.filter(k => k.from <= x.from && x.from < k.to).length > 2) out.bad.push('day ' + d + ': more than two traditions at once at ' + x.from);
        for (const a of all) for (const b of all) if (a !== b && recOnly(a) && recOnly(b) && a.from < b.to && b.from < a.to && evRooms(a.ev).some(r => evRooms(b.ev).includes(r))) out.bad.push('day ' + d + ': ' + a.id + ' and ' + b.id + ' at once in one room');
        for (const a of t) for (const b of t) if (a !== b && a.from < b.to && b.from < a.to && evRooms(a.ev).some(r => evRooms(b.ev).includes(r))) out.bad.push('day ' + d + ': ' + a.id + ' and ' + b.id + ' at once in one room');
        if (d >= 1 && weekday(d) < 5 && t.length < 2 && !eventOn(d)) out.bad.push('day ' + d + ' (a weekday) has ' + t.length + ' tradition(s), not 2-3');
        if (EV_DROPPED.get(d)) out.dropped.push(d + ':' + EV_DROPPED.get(d).join('+'));
      }
      for (const d of [0, 1, 91, 92, 182, 183, 273, 274, 364, 365]) out.seasons.push(d + ':' + season(d) + ':' + seasonOf(d).week);
      const ks = SHIP_TRADITIONS.map(e => e.k); if (new Set(ks).size !== ks.length) out.bad.push('two traditions share a hash key k');
      out.invites = SHIP_TRADITIONS.filter(e => e.invite).map(e => e.id + ':' + e.invite.host);   // for section 20's invitations
      for (const e of SHIP_TRADITIONS.filter(e => e.invite)) { const v = e.invite;
        if (!schedPeople().some(p => p.id === v.host) || !(v.odds > 0 && v.odds <= 1) || typeof v.line !== 'string' || !v.line || v.line.length > 140) out.bad.push(e.id + ': invite ' + JSON.stringify(v)); }
      for (const t of TRAD_LIST) {
        const ev = SHIP_TRADITIONS.find(e => e.id === t.id); if (!ev || !ev.baked) { out.bad.push('baked ' + t.id + ' not loaded'); continue; }
        let n = 0; for (let d = 0; d <= 364; d++) if (eventsOn(d).some(e => e.id === t.id)) n++;
        if (!n && !t.when.birthday && !t.flag) out.bad.push('baked ' + t.id + ' never happens in a whole year');   // a flagged one waits for its story beat (tested above)
        const d = [...(out.count[t.id] || [])].find(x => x >= 1) || [...Array(365).keys()].find(x => x >= 1 && eventsOn(x).some(e => e.id === t.id)) || 1, e = eventsOn(d).find(x => x.id === t.id) || { ev, day: d, names: '', first: '', from: ev.at[0], honorees: [] };
        for (const k of ['mail', 'ask', 'here']) if ((t.text || {})[k] && !evText(ev[k], e, schedPeople()[0])) out.bad.push(t.id + ': no ' + k + ' line could be filled');
        for (const [c] of t.who.concat(Array.isArray(t.anim) ? t.anim : [])) for (const p of schedPeople()) tradIs(c, p, d, e, t.host);   // every word resolves (TRAD_ERRORS)
        out.baked.push({ id: t.id, from: ev.from, mail: evText(ev.mail, e), ties: t.ties || null });
      }
      // a tradition that waits for a story flag (bridge hour: 'bridge.invited') comes on once it's set, and goes again
      for (const ev of SHIP_TRADITIONS.filter(e => e.flag && typeof flagSet === 'function')) {
        const was = flag(ev.flag), on = () => [...Array(56).keys()].map(x => x + 1).concat([92, 99]).filter(x => eventsOn(x).some(e => e.id === ev.id)).length;   // + 92, 99: a season's first Monday (the rec deck's all-hands, 0.83)
        flagSet(ev.flag, null); const off = on(); flagSet(ev.flag, true); const yes = on(); flagSet(ev.flag, was === undefined ? null : was); eventsOn(1);
        out.flags = (out.flags || []).concat(ev.id + ': ' + off + ' without, ' + yes + ' with ' + ev.flag);
        if (off || !yes) out.bad.push(ev.id + ' and its flag ' + ev.flag + ': ' + off + ' days without, ' + yes + ' with');
      }
      // and each rhythm on its own, as a tradition designer might write it
      for (const w of [{ every: 'week', weekday: 6 }, { every: '2weeks', weekday: 1 }, { every: '2weeks', weekday: 1, week: 2 }, { every: '4weeks', weekday: 5, week: 3 },
          { every: 'quarter', quarterDay: 1 }, { every: 'quarter', week: 13, weekday: 6 }, { every: 'year', dayOfYear: 182 }, { every: 'year', week: 52, weekday: 6 },
          { after: 'arrival', days: 7 }, { after: 'arrival', days: 28 }, { after: 'arrival', weekday: 4 }, { after: 'arrival', weekday: 4, nth: 4 },
          { every: 'week', weekday: 2, season: 'greening' }, { every: 'week', weekday: 0, season: ['harvest', 'lanterns'], from: 200 }]) {
        const due = dueNew(w, 0, 400);
        for (let d = 0; d <= 400; d++) if (evDue(w, d) !== due.has(d)) { out.bad.push('rhythm ' + JSON.stringify(w) + ' wrong on day ' + d); break; }
        if (!due.size) out.bad.push('rhythm ' + JSON.stringify(w) + ' never due');
      }
      out.errors = TRAD_ERRORS.slice();
      return out;
    })()""")
    print('A year on paper:', '; '.join(f"{k} {len(v)}x (days {', '.join(map(str, v[:6]))}{'...' if len(v) > 6 else ''})" for k, v in yr['count'].items()))
    print('Seasons (day:season:week):', ' '.join(yr['seasons']))
    print('The voice budget left out (day:ids):', ' '.join(yr['dropped']) or 'nothing')
    print('Invitations (tradition:host):', ' '.join(yr['invites']) or 'none')
    print('Flagged traditions:', yr.get('flags') or 'none')
    exp = ['0:lanterns:13', '1:sowing:1', '91:sowing:13', '92:greening:1', '182:greening:13', '183:harvest:1', '273:harvest:13', '274:lanterns:1', '364:lanterns:13', '365:sowing:1']
    if yr['seasons'] != exp: fail(f"seasons {yr['seasons']}")
    for b in yr['baked']: print(f"  baked {b['id']}: from {b['from']}; ties {b['ties']}; Mail: {b['mail']}")
    import os, re as _re                                  # every .trad file in the repo is in the game (an empty baked block must not hide one)
    tdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'content', 'traditions')
    files = sorted(f for f in os.listdir(tdir) if f.endswith('.trad')) if os.path.isdir(tdir) else []
    want_ids = [m.group(1) for f in files for m in [_re.search(r'^@tradition\s+(\S+)', open(os.path.join(tdir, f), encoding='utf-8').read(), _re.M)] if m]
    loaded = g.ev("SHIP_TRADITIONS.filter(e => e.baked).map(e => e.id)")
    print(f"Tradition files: {len(files)} ({', '.join(want_ids)}); loaded from the baked block or stand-in: {', '.join(loaded) or 'none'}")
    rec_on = g.ev("typeof REC_DECK !== 'undefined' && REC_DECK")
    for i in want_ids:
        if i.startswith('rec-') and not rec_on: continue    # the rec deck's own load only with the deck switched on (0.83)
        if i not in loaded: fail(f"content/traditions has {i}, but the game didn't load it (bake the TRADITIONS block again)")
    # every decor and trace id a tradition names is one the deck architect built (DECK_DRESS) or has announced, or one
    # a designer has asked for (it shows nothing until built); anything else is a typo
    ANNOUNCED = {'tilesNight', 'seedlingYours', 'tastingTable', 'lanternWalk', 'mugYours', 'longTables', 'harvestTables', 'cupBoard', 'talentStage', 'yearsEnd', 'openLab'}   # the deck architect, 0.38.10-0.38.14 and their list
    ASKED = {'nameYours', 'spiceJars'}                    # named by deck architect 4 (claude/deck-0607, "Places for 0.60.7"), not in this branch yet
    ids = g.ev("SHIP_TRADITIONS.flatMap(e => [e.ties && e.ties.decor, e.trace].filter(Boolean).map(x => [e.id, x]))")
    built = set(g.ev("typeof DECK_DRESS === 'undefined' ? [] : Object.keys(DECK_DRESS)"))
    waiting = sorted({x for _, x in ids if x not in built})
    print(f"Props and traces: {len(ids)} named; not in this build yet: {', '.join(waiting) or 'none'}")
    for t, x in ids:
        if x not in built and x not in ANNOUNCED and x not in ASKED: fail(f"{t}: decor or trace '{x}' isn't in DECK_DRESS, announced or asked for (a typo?)")
    for x in yr['errors']: fail('TRAD_ERRORS: ' + x)
    for b in yr['bad'][:20]: fail(b)

    # 1c. the rec deck's traditions (RA, 0.83; plans/rec-traditions-plan.html FINAL), when the deck is switched on: each
    # due on exactly the plan's days (weeks 1-6, worked out here from the plan, not from the game), the speaker at their
    # talk and the hosts at theirs when free, film night's move after the first all-hands (and the junior common room's
    # film no more), the season's all-hands once it's held, the boards filling, and the numbers at each
    if g.ev("typeof REC_TRADS !== 'undefined' && REC_DECK && REC_TRAD_ON"):
        PLAN = {'rec-wso': [7, 14, 21, 35, 42], 'rec-cup': [28], 'rec-dawn-swim': [d for d in range(2, 43) if (d - 1) % 7 in (1, 3)],
                'rec-paddle-club': list(range(3, 43, 7)), 'rec-wall-night': list(range(2, 43, 7)), 'rec-float-hour': list(range(3, 43, 7)),
                'rec-slow-stretch': list(range(7, 43, 7)), 'rec-regatta': [21], 'rec-talent-night': [14, 42], 'rec-chiefs-talk': [8, 18], 'rec-wren-talk': [25, 29],
                'rec-film-night': [], 'rec-all-hands': []}
        rc = g.ev("""(() => { const out = { on: {}, n: {}, hosts: [], talks: [] };
          for (let d = 1; d <= 42; d++) for (const e of eventsOn(d)) if (/^rec-/.test(e.id)) {
            (out.on[e.id] = out.on[e.id] || []).push(d);
            const went = schedPeople().filter(p => planDay(p, d).some(s => evTagId(s.tag) === e.id)).map(p => p.id);
            (out.n[e.id] = out.n[e.id] || []).push(went.length);
            if (e.ev.host && !went.includes(e.ev.host)) { const h = schedPeople().find(p => p.id === e.ev.host); if (h && eventFree(h, d, e.from, e.to, e.ev.wake)) out.hosts.push(d + ' ' + e.id + ' without its host ' + e.ev.host); }
            const t = /^rec-(wren|chiefs)-talk$/.test(e.id) && recTalk(d); if (t) out.talks.push([d, t.size, t.by, went.includes(t.by)]);
          }
          return out; })()""")
        for k, want in PLAN.items():
            got = rc['on'].get(k, [])
            if k == 'rec-wso': want = [d for d in want if d != 28]
            if got != want: fail(f"{k} on days {got}, the plan says {want}")
        print('Rec deck traditions, days 1-42 (people at each):', '; '.join(f"{k} {v}" for k, v in sorted(rc['n'].items())))
        for x in rc['hosts']: fail(x)
        for d, size, by, ok_ in rc['talks']:
            if not ok_: fail(f"day {d}: the {size} talk without its speaker {by}")
        print('  the talks:', rc['talks'])
        mv = g.ev("""(() => { const sat = d => eventsOn(d).map(e => e.id).filter(i => i === 'film' || i === 'rec-film-night');
          const before = [6, 13].map(sat); recFirstAllHands(9 * 1440 + 600); const after = [13, 20].map(sat);
          const ah = eventsOn(92).filter(e => e.id === 'rec-all-hands').length, g92 = schedPeople().filter(p => planDay(p, 92).some(s => evTagId(s.tag) === 'rec-all-hands'));
          const lect = schedPeople().filter(p => planDay(p, 92).some(s => s.placeId === '7-lectern-1')).map(p => p.id);
          return { before, after, ah, n: g92.length, lect, flagA: flag('rec.allHands'), day: SHIP.rec.ah }; })()""")
        print('  film night and the all-hands:', mv)
        if mv['before'] != [['film'], ['film']] or mv['after'] != [['rec-film-night'], ['rec-film-night']]: fail(f"film night's move: {mv}")
        if mv['ah'] != 1 or mv['n'] < 30 or mv['lect'] != ['marrow'] or mv['day'] != 10: fail(f"the season's all-hands: {mv}")
        bd = g.ev("""(() => { SHIP.rec.wso.length = 0; SHIP.rec.bell.length = 0; for (const [id, d] of [['rec-wso', 7], ['rec-wall-night', 9], ['rec-regatta', 21], ['rec-cup', 28]]) simNote('tradition', { id, day: d, at: 0, came: [], you: false });
          return { wso: recBoard('wso', 7), bell: recBoard('bell', 9), reg: recBoard('reg', 21), cup: recBoard('cup', 28), three: (wsoCourt(7) || {}).three }; })()""")
        print('  the boards:', bd)
        if bd['wso'] != bd['three'] or not bd['bell'] or not bd['cup']: fail(f"the boards: {bd}")
        g.ev("(() => { for (const k of ['rec.allHands', 'rec.filmMoved']) delete SHIP.flags[k]; SHIP.rec = recClean(null); EV_DAYS.clear(); SHIP_DAYS.clear(); })()")   # back as it was for the walks below

    # 2. on the deck: one of each kind, walked through minute by minute
    bd = g.ev(f"[...Array({DAYS}).keys()].map(i => i + 1).find(d => eventsOn(d).some(e => e.id === 'birthday'))")
    sims = [(1, 'running'), (6, 'observatory-night'), (4, 'quiz'), (5, 'works-tea'), (5, 'jam'), (bd, 'birthday'), (6, 'film'), (6, 'harvest'), (7, 'market'), (24, 'hull-lights'), (100, 'founding'), (300, 'quiet-watch')]
    sims += [(next(x for x in yr['count'][b['id']] if x >= 1), b['id']) for b in yr['baked'] if any(x >= 1 for x in yr['count'].get(b['id'], []))]   # the baked ones too
    for d, i in sims:
        if not g.ev(f"eventsOn({d}).some(e => e.id === '{i}')"):   # another tradition may take its day (the voice budget): its next one
            d2 = g.ev(f"[...Array({max(DAYS, 28)}).keys()].map(x => x + 1).find(x => eventsOn(x).some(e => e.id === '{i}'))")
            if not d2: fail(f"{i} not on day {d} nor any day to {max(DAYS, 28)}"); continue
            print(f"  ({i} isn't on day {d} (the voice budget: {g.ev(f'(EV_DROPPED.get({d}) || []).join()') or '-'}); walking day {d2})"); d = d2
        s = g.ev(f"({SIM})({{ d: {d}, id: '{i}', step: {STEP} }})")
        for x in s['decks']:
            print(f"  {i} day {d}, Deck {x['n']}: {x['reached']}/{x['att']} reached their places, worst stuck {x['stuck']:.1f} min {x['stuckWho']}, draw calls {x['calls']} ({x['crew']} crew{', decor ' + str(x['decor']) + ' meshes' if x['decor'] else ''})")
            if x['att'] and x['reached'] < x['att']: (fail if x['reached'] < x['att'] * .8 else print)(f"  not reached: {x['notReached']}")
            if x['stuck'] >= 10: fail(f"stuck {x['stuck']:.1f} min: {x['stuckWho']}")
            if x['shared']: fail(f"places shared: {x['sharedWho']}")
            if x['noPath']: fail(f"no path: {x['noPath']}")
            if x['calls'] >= BUDGET: fail(f"draw calls {x['calls']} >= {BUDGET}")
    for d, i, k in [(7, 'market', 'stalls'), (bd, 'birthday', 'cake')]:
        g.ev(f"SHIP.galley = null; goToDeck(3); setShipNow(({d} - 1) * 1440 + eventsOn({d}).find(e => e.id === '{i}').from + 10); if (typeof galleyTick === 'function') galleyTick(); EV_MIN = -1; eventsTick()")
        on = g.ev("EV_DECOR.g ? EV_DECOR.g.children.length : 0")
        if k == 'cake':                                   # one cake: the galley's on the servery (section 16) when it's out, else ours
            gc = g.ev("typeof evGalleyCake === 'function' && evGalleyCake()")
            print(f"  the galley's cake out: {gc}; ours: {on} meshes")
            if gc and on: fail('two cakes: the galley\'s and ours')
            if gc or g.ev("typeof galleyAdvance === 'function'"): on = 1   # the galley bakes it (0.29.15)
        g.ev(f"setShipNow(({d} - 1) * 1440 + eventsOn({d}).find(e => e.id === '{i}').to + 30); EV_MIN = -1; eventsTick()")
        off = g.ev("EV_DECOR.g ? EV_DECOR.g.children.length : 0")
        print(f"Decor ({k}): {on} meshes during {i}, {off} after")
        if not on or off: fail(f"{k} decor: {on} during, {off} after")

    # 3. the Mail the evening before: a week of skips from Day 1 (and the ship note after each tradition, Pillar 4:
    # the sim engineer's bus when it's in, else a stand-in simNote that only records)
    g.ev("setShipNow(360); EV_LAST = null; EV_MIN = -1; eventsTick(); SHIP.events.sent.length = 0; EV_MAILBOX.length = 0; WEEK_MAILS.length = 0")
    g.ev("window.__notes = []; SHIP.events.noted.length = 0; if (typeof onSim === 'function') { onSim('tradition', n => __notes.push(n)); onSim('choice', n => __notes.push(n)); } else window.simNote = (kind, data) => __notes.push({ ...data, kind })")
    g.ev("for (let t = 360 + 600; t <= 7 * 1440; t += 600) skipTo(t)")
    nt = g.ev("""(() => {
      const want = [1, 2, 3, 4, 5, 6].flatMap(d => eventsOn(d).filter(e => (d - 1) * 1440 + e.to > 360).map(e => ({ key: e.id + '@' + d, n: schedPeople().filter(p => planDay(p, d).some(s => s.tag && /^ev-/.test(s.tag) && evTagId(s.tag) === e.id)).length })));
      return { want, got: __notes.map(n => ({ key: n.id + '@' + n.day, n: n.came.length, kind: n.kind, src: n.src, at: n.at })) };
    })()""")
    gk = [x['key'] for x in nt['got']]
    print(f"Ship notes after each tradition (days 1-6): {len(gk)}, e.g. {nt['got'][:3]}")
    for w in nt['want']:
        x = [n for n in nt['got'] if n['key'] == w['key']]
        if len(x) != 1: fail(f"tradition note for {w['key']}: {len(x)} sent")
        elif x[0]['n'] != w['n'] or x[0]['kind'] != 'tradition': fail(f"tradition note for {w['key']}: came {x[0]['n']}, planned {w['n']}")
    m = g.ev("EV_MAILBOX.map(x => [x.event, x.at, x.subject])")
    due = g.ev("[2, 3, 4, 5, 6, 7, 8].flatMap(d => eventsOn(d).filter(e => !(e.ev.quiet === 'career' && typeof recBigDay === 'function' && recBigDay(d))).map(e => e.id + '@' + d))")   # the rec deck's weekly sport ones send none on the career's big days (0.83)
    got = [x[0] for x in m]
    print(f"Mail: {len(m)} announcements for days 2-8 ({len(due)} events due); e.g. {m[0][2] if m else '-'}")
    for k in due:
        if k not in got: fail(f"no Mail for {k}")
    # the Sunday "This week aboard" Mail (Pillar 4): sent on day 7 at 18:00 (the first Sunday after you arrive), once,
    # in time order within a day; section 18's WEEK_MAIL is a copy of content/traditions/this-week-aboard.mail
    wm = g.ev("WEEK_MAILS.map(m => [m.day, m.at, m.body])")
    print(f"This week aboard: {[(x[0], x[1]) for x in wm]}; day 7 reads: " + (wm[0][2].replace(chr(10), ' / ')[:300] if wm else '-'))
    if [x[0] for x in wm] != [7] or wm[0][1] != 6 * 1440 + 1080: fail(f"the Sunday Mail: {[(x[0], x[1]) for x in wm]}")
    import json as _json, re as _re2
    tw = os.path.join(tdir, 'this-week-aboard.mail')
    if os.path.exists(tw):
        want, sec = {}, None
        for l in open(tw, encoding='utf-8').read().splitlines():
            st = l.strip()
            if not st or st.startswith('//') or st.startswith('@'): continue
            if st.startswith('=='): sec = st[2:].strip(); want[sec] = []; continue
            if sec is None: k, v = st.split(':', 1); want[k.strip()] = v.strip(); continue
            t = st[2:].strip(); mt = _re2.search(r'\s#(\w+)\s*$', t); want[sec].append(t[:mt.start()].rstrip() if mt else t)
        if g.ev("WEEK_MAIL") != want: fail('WEEK_MAIL in section 18 differs from content/traditions/this-week-aboard.mail: copy it again')
    if len(got) != len(set(got)): fail('a Mail sent twice')
    for k, at, _ in m:
        d = int(k.split('@')[1])
        if at != (d - 2) * 1440 + 1080: fail(f"{k} announced at {at}, not 18:00 the evening before")

    # 4. the player joins the quiz by being in the bow lounge (Day 4), and a tap line before it
    line = g.ev("(() => { const p = schedPeople().find(p => planDay(p, 4).some(s => s.tag && s.tag.startsWith('ev-quiz'))); return p ? eventLine(p, 3 * 1440 + 1100) : null; })()")
    print('Tap line before the quiz:', line)
    if not line: fail('no tap line before the quiz')
    j = g.ev("""(() => {
      goToDeck(3); const c = PLACE_OF.get('3-lounge-30'); const at = (DECKS[3].places.find(p => p.id === '3-lounge-30') || {}).at;
      player.obj.position.copy(cellPos(...nearestOpen(...cellPos(...at).toArray().filter((_, i) => i !== 1), player)));
      const n0 = SHIP.player.needs.social = 50; SHIP.events.joined.length = 0;
      for (const m of [1210, 1213, 1217, 1220]) { setShipNow(3 * 1440 + m); EV_MIN = -1; eventsTick(); }
      const passive = SHIP.events.joined.slice();          // 0.70.0: the quiz is tap to join: being there isn't joining
      deckCrewFill(); EV_MIN = -1; eventsTick(); const a = TJ_NOW && TJ_NOW.agent, tapped = !!a && tradJoinTap(a);
      return { room: roomAt(...player.here()), passive, lead: TJ_NOW ? TJ_NOW.lead : (a && a.p.id), tapped, joined: SHIP.events.joined.slice(), social: SHIP.player.needs.social, n0 };
    })()""")
    print(f"Player in room {j['room']} during the quiz: joined by being there {j['passive']}; tapped {j['lead']}: {j['tapped']}, joined {j['joined']}, social {j['n0']} -> {j['social']}")
    if j['passive'] or not j['tapped'] or j['joined'] != ['quiz@4'] or j['social'] <= j['n0']: fail('the player should join the quiz by tapping Tomas (and not by being there)')

    # 4b. Pillar 4: joining Sowing morning (day 6) leaves your seedling (trace seedlingYours with its day); a tradition's
    # ties.decor goes to dressShow only in its window
    sw = g.ev("""(() => {
      goToDeck(3); const at = (DECKS[3].places.find(p => p.id === '3-garden-5') || {}).at; if (!at) return { err: 'no 3-garden-5' };
      player.obj.position.copy(cellPos(...nearestOpen(...cellPos(...at).toArray().filter((_, i) => i !== 1), player)));
      const t0 = SHIP.traces.slice(); SHIP.events.joined.length = 0;
      const e = eventsOn(6).find(x => x.id === 'sowing'); if (!e) return { err: 'sowing not on day 6' };
      for (const m of [e.from + 1, e.from + 4, e.from + 7, e.from + 10]) { setShipNow(5 * 1440 + m); EV_MIN = -1; eventsTick(); }
      deckCrewFill(); EV_MIN = -1; eventsTick(); if (TJ_NOW && TJ_NOW.e.id === 'sowing') tradJoinTap(TJ_NOW.agent);   // 0.70.0: tap to join
      const tr = SHIP.traces.filter(x => x.id === 'seedlingYours'); SHIP.traces.length = 0; SHIP.traces.push(...t0);
      const ties = e.ev.ties; e.ev.ties = { ...ties, decor: 'testDecor' };
      const dec = [e.from - 40, e.from - 20, e.to + 10, e.to + 20].map(m => tradDecor(5 * 1440 + m).map(x => x.id).join());
      e.ev.ties = ties;
      return { room: roomAt(...player.here()), joined: SHIP.events.joined.slice(), tr, dec };
    })()""")
    print('Sowing morning joined:', sw)
    if sw.get('err') or sw['joined'] != ['sowing@6'] or len(sw['tr']) != 1 or sw['tr'][0].get('day') != 6: fail(f"joining Sowing morning should plant your seedling once: {sw}")
    if sw.get('dec') != ['', 'testDecor', 'testDecor', '']: fail(f"a tradition's decor window: {sw.get('dec')}")

    # 4c. tallies (Pillar 4): the tasting vote (two dishes a week, in turn), the department cup by teams, the same twice,
    # your vote counts once and only on the day, the galley's tallyLast, a decor with a tally shows the votes
    ty = g.ev("""(() => {
      const d1 = [...Array(28).keys()].map(x => x + 1).find(x => eventsOn(x).some(e => e.id === 'tasting-table'));
      const d2 = d1 + 7, cup = [...Array(56).keys()].map(x => x + 1).find(x => eventsOn(x).some(e => e.id === 'department-cup'));
      if (!d1) return { err: 'no tasting table' };
      const a = tallyOf('tasting-table', d1); TALLY_MEMO.clear(); const a2 = tallyOf('tasting-table', d1), b = tallyOf('tasting-table', d2);
      const votes0 = { ...SHIP.events.votes }, t0 = shipNow();
      setShipNow((d1 - 1) * 1440 + 1100); const ok = tallyVote('tasting-table', a.choices[1]); const late = (setShipNow((d1 - 1) * 1440 + 1200), tallyVote('tasting-table', a.choices[0]));
      const v = tallyOf('tasting-table', d1), last = tallyLast('tasting-table', d1 + 4);
      const e = eventsOn(d1).find(x => x.id === 'tasting-table'), ties = e.ev.ties; e.ev.ties = { ...ties, decor: 'testDecor' };
      const dec = tradDecor((d1 - 1) * 1440 + Math.round((e.from + e.to) / 2)).find(x => x.id === 'testDecor'); e.ev.ties = ties;
      SHIP.events.votes = votes0; TALLY_MEMO.clear();
      return { d1, a, same: JSON.stringify(a) === JSON.stringify(a2), b: b && b.choices, ok, late, you: v.you, plus: v.counts[a.choices[1]] - a.counts[a.choices[1]], last: last && last.day, dec, cup: cup && tallyOf('department-cup', cup) };
    })()""")
    print('Tallies:', ty)
    if ty.get('err') or not ty['same'] or len(ty['a']['choices']) != 2 or ty['b'] == ty['a']['choices'] or not ty['ok'] or ty['late'] or ty['plus'] != 1 or ty['last'] != ty['d1']: fail(f"the tasting tally: {ty}")
    if not ty.get('dec') or ' or ' not in ty['dec'].get('title', '') or len(ty['dec'].get('lines', [])) != 2: fail(f"a decor with a tally: {ty.get('dec')}")
    if not ty.get('cup') or sum(ty['cup']['counts'].values()) == 0: fail(f"the department cup's teams: {ty.get('cup')}")


    # 5. a ship-wide event on paper: the ion storm's skeleton, twice
    st = g.ev(STORM); a = st['a']
    print('Ion storm on paper (days 10-16):'); [print('  ' + x) for x in a['steps']]
    print(f"  wear and flicker by phase: {a['mods']}; result {a['log'][0]['band'] if a['log'] else '-'}, threads {a['log'][0]['threads'] if a['log'] else '-'}, traces {a['traces']}")
    print('  addresses:'); [print('    ' + x) for x in a['addr']]
    print('  Mail:', a['mails'])
    print('  meetings:', a['meets'], '| scripts', a['scripts'], a['lines'])
    print('  traditions by day (storm from day 10):', a['paused'], '| menu', a['mods'].get('menu'))
    print('  news:'); [print('    ' + x) for x in a['news']]
    print('  eventOn:', a['on'], '| gatherings:', a['gath'])
    print('  the same twice:', st['same'], '| due in play:', st['due'], '(day 10 in a new game)')
    print('  upcoming traditions:', [(c['title'], c['at'], c['where']) for c in st['cal']])
    want = ['start', 'warning', 'onset', 'escalation', 'resolution', 'afterglow', 'end']
    got = [w for x in a['steps'] for w in want if (' ' + w) in (' ' + x.split(' ', 3)[3]).replace('phase ', ' ').replace('end ', ' end ')]
    if [w for w in want if w != 'start'] != [w for w in got if w != 'start']: fail(f"storm phases out of order: {a['steps']}")
    m = a['mods']
    if m.get('-') != [None, None, None] or m.get('onset') != [1.5, 2, True] or m.get('escalation') != [2, 3, True] or m.get('resolution') != [None, None, None]: fail(f"eventMod by phase: {m}")
    if not st['same']: fail('the storm ran differently the second time')
    if not st['due'] or st['due'].get('day') != 10: fail(f"the storm isn't due on day 10 in play: {st['due']}")
    if len(a['addr']) != 2 or 'in it' not in a['addr'][0] or 'passed' not in a['addr'][1]: fail(f"the Captain's addresses: {a['addr']}")
    if not any('Storm prep' in x for x in a['mails']) or not any('how it went' in x for x in a['mails']): fail(f"the storm's Mail: {a['mails']}")
    if len(a['news']) != 7 or not all('@10 ' in x for x in a['news']): fail(f"the storm's news: {a['news']}")
    if a['on'] != ['10:0 warning@360', '11:1 warning@0 onset@840', '13:3 escalation@0 resolution@600 afterglow@1320', '16:-'] or 'stormBriefing works-bay 09:15' not in a['gath'][0] or 'party bow-lounge 19:00' not in a['gath'][1]: fail(f"eventOn / eventGatherings: {a['on']} {a['gath']}")
    if len(a['meets']) != 2: fail(f"the storm's meetings: {a['meets']}")
    if m.get('menu') != 'stormStew': fail('eventMod at t: no storm stew in the escalation')
    if a['log'] and 'calls' not in a['log'][0]['threads']: fail('the call-home backlog was not scored')
    pd = dict(x.split(':') for x in a['paused'])
    if 'quiz' in pd['11'] or 'works-tea' in pd['12']: fail(f"traditions in the storm: {a['paused']}")
    if len(a['log']) != 1 or a['log'][0]['band'] not in ('smooth', 'bumpy', 'rough') or a['left'] is not None: fail(f"the storm didn't end cleanly: {a['log']} {a['left']}")
    if not st['cal']: fail('upcomingTraditions found nothing in the first week')

    # 6. a live ion storm on the deck
    L = g.ev(LIVE)
    print('Live ion storm:')
    print('  briefing:', L['briefing'], '| panel shown:', L['panel'], '| draw calls', L['calls1'])
    [print('    ' + x) for x in L['lines']]
    print('  after it:', {k: v for k, v in L['mine'].items()}, '| closed:', L['closed'])
    print('  the front:', L['feel'], '| address banner:', L['banner'], '| flicker on:', L['flicker'], '| draw calls', L['calls2'])
    print('  all-clear:', L['allClear'], '| draw calls', L['calls3'], '| walked out, closed:', L['walked'])
    print('  Mail:', L['mails'])
    print('  log:', L['log'], '| traces', L['traces'])
    print('  dressing shown:', L['dress'])
    if not any('signupWorks[3]' in x for x in L['dress']) or not any('partyLounge' in x for x in L['dress']): fail(f"the storm's dressing: {L['dress']}")
    b = L['briefing']
    if not b['open'] or set(b.get('cast', {})) != {'calder', 'tech1', 'tech2'} or not L['panel']: fail(f"the briefing didn't open with its cast: {b}")
    if not any(x.startswith('[choice]') for x in L['lines']) or not any('Mind the lift' in x for x in L['lines']) or not L['closed']: fail('the briefing script did not play through with the reply')
    print('  ship notes for your replies:', L.get('choiceNotes'))
    mo = g.ev("""(() => {   // social B's moments play on this panel: onPick and onEnd on the script (20c)
      const got = []; MEETING_SCRIPTS['moment:test'] = { title: 'Test', lines: [{ who: 'tomas', text: 'Hi.' }, { choice: [{ text: 'A' }, { text: 'B' }] }, { who: 'tomas', text: 'Bye.' }],
        onPick: (k, c) => { got.push('pick:' + k + ':' + c.text); throw new Error('a bad listener'); }, onEnd: f => got.push('end:' + f) };
      const ev0 = SHIP.event; SHIP.event = { id: 'x', startDay: 1, phase: null, threads: {}, mine: {} };   // a moment never counts as the event's meeting
      dialogueShow('moment:test'); dialogueStep(); dialogueStep(1); dialogueStep(); dialogueEnd(true);
      if (Object.keys(SHIP.event.mine).length) got.push('counted:' + Object.keys(SHIP.event.mine).join()); SHIP.event = ev0;
      delete MEETING_SCRIPTS['moment:test']; return got;
    })()""")
    print('  a moment on the panel:', mo)
    if mo != ['pick:1:B', 'end:true']: fail(f"a moment's onPick / onEnd: {mo}")
    if not any(x.startswith('stormBriefing:0:') or x.startswith('calderStorm:0:') for x in L.get('choiceNotes') or []): fail(f"no simNote('choice') for the briefing reply: {L.get('choiceNotes')}")
    if L['mine'].get('choice:calderStorm') != 1 or not (L['mine'].get('wants:stormBatteries') or L['mine'].get('jobs')): fail(f"the briefing choice was not recorded: {L['mine']}")
    if any('Storm briefing (notes)' in x for x in L['mails']): fail('a gist was mailed for a briefing played to the end')
    if not L['feel'] or 'jolt' not in L['feel'][0] or not L['banner'] or not L['flicker']: fail('the front was not felt (jolt, banner, flicker)')
    if not L['allClear'] or L['allClear']['name'] != 'Captain Odile Marrow' or not L['walked'] or not any('The all-clear (notes)' in x for x in L['mails']): fail('the all-clear did not open, or walking out sent no gist')
    if max(L['calls1'], L['calls2'], L['calls3']) >= 450: fail('draw calls over 450 in the storm')
    if len(L['log']) != 1 or L['left'] is not None or not L['traces'] or not any('how it went' in x for x in L['mails']): fail(f"the live storm didn't end cleanly: {L['log']}")

    # 7. occasions (C10)
    O = g.ev(OCC)
    print('Occasions: before a commendation', O['none'], '| booked', O['booked'], '| door', O['doorBefore'], O['doorAt'], '| in room', O['room'])
    print('  ready room:', O['open'], O['lines'])
    print('  after:', O['after'], '| progress talk asked:', O['ask'], 'on a day off:', O['askOff'])
    print('  the table:', O['table'], '| batch', O['batch'], O['noBatch'], '| end', O['end'], '| traces', O['traces'])
    print('  Mail:', O['mails'])
    if O['none'] or not O['booked'] or 'readyRoom@17 11:00 asked' not in O['booked'][0] or O['doorBefore'] or not O['doorAt']: fail(f"the ready-room summons: {O['booked']}")
    if O['open'] != 'readyRoomFirst' or not any('Admiral' in x for x in O['lines']) or 'readyRoom@17 kept' not in O['after']: fail(f"the ready room didn't play or wasn't kept: {O['open']} {O['after']}")
    if not O['ask'] or O['askOff']: fail('occasionAsk: the progress talk')
    if not any('captainsTable@20 19:30' in x for x in O['table']) or not O['batch'] or O['noBatch']: fail(f"the Captain's table: {O['table']} {O['batch']}")
    if not any('captainsTable@20 missed' in x for x in O['end']) or 'framedMenu' in O['traces'] or not any('Captain\'s table (notes)' in x for x in O['mails']): fail(f"a missed table: {O['end']} {O['mails']}")

    # 8. the hooks for others
    H = g.ev(HOOKS)
    print('Hooks: party on day 13', H['partyDay'], '(day 11:', H['party11'], ') going', H['partyGoing'], H['partyPlaces'])
    print('  routines (day 12 15:00, 13 06:40, 13 11:40, 14 01:40):', H['routines'], '| guest days', H['guest'], H['noGuest'], '| owed a call', H['owed'])
    print('  one-off:', H['added'], H['again'], H['today'], H['oneOffOn'], 'going', H['oneOffGoing'], '| Pell free:', H['hostFree'], '| host flagged:', H['hostFlag'])
    if 'party' not in H['partyDay'] or H['party11'] or H['partyGoing'] < 10: fail('the all-clear party is not planned on day 13')
    if not H['routines'][0].startswith('doubleShift') or not H['routines'][1].startswith('doubleShift') or H['routines'][2] != 'rush' or H['routines'][3] != '': fail(f"eventRoutines: {H['routines']}")
    if H['guest'] != [11, 14] or H['noGuest'] is not None: fail(f"eventGuestDays: {H['guest']}")
    if not H['added'] or H['again'] or H['today'] or 'pell-show' not in H['oneOffOn'] or not H['oneOffGoing'] or (H['hostFree'] and not H['hostFlag']): fail('eventOneOff')

    # 9. the diplomatic visit on paper
    V = g.ev(DIPLO); a = V['a']
    print('Diplomatic visit on paper: due', a['due'], '| the same twice:', V['same'])
    [print('  day ' + x) for x in a['steps']]
    print('  galley batch at 15:00 by day:', a['batch'], '| guests (days from the start):', a['guests'])
    print('  addresses:', a['addr']); print('  Mail:', a['mails']); print('  meetings:', a['meets'])
    print('  farewell:', a['farewell'], 'going', a['going'], '| result', a['log'], a['traces'])
    print('  greeting speakers:', V['names'], '| guests flag on days', a['guestsOn'])
    print('  live greeting (in the shuttle bay at 10:00):', V['live'])
    if V['live']['open'] != 'veyliGreeting' or V['live']['first'] != 'Captain Odile Marrow': fail(f"the live greeting: {V['live']}")
    if a['guestsOn'] != [2, 3, 4, 5, 6]: fail(f"the 'guests' effect: {a['guestsOn']}")
    if not a['due'] or a['due']['id'] != 'diplomatic' or a['due']['day'] < 23 or not V['same']: fail(f"the diplomatic visit's start or repeatability: {a['due']} {V['same']}")
    want = ['warning', 'onset', 'escalation', 'resolution', 'afterglow', 'end']
    if [w for x in a['steps'] for w in want if (' ' + w) in x.replace('phase ', ' ')] != want: fail(f"diplomatic phases: {a['steps']}")
    bd = dict(x.split(':') for x in a['batch'])
    if bd.get('3') != '10' or bd.get('5') != '10' or bd.get('4') != '-' or bd.get('1') != '-': fail(f"the formal dinners' batch: {a['batch']}")
    if len(a['addr']) != 2 or len(a['meets']) != 2 or not a['farewell'] or a['going'] < 3: fail('the visit\'s addresses, meetings or farewell')
    if a['guests'][0] != 'teshavi:2-7' and a['guests'][0] != 'teshavi:-': fail(f"the guests' days: {a['guests']}")
    if 'Speaker Teshavi' not in V['names'] or 'Envoy Saruth' not in V['names']: fail(f"the greeting's cast: {V['names']}")

    # 9b. tradOn (0.34.37, social B's calls home): the Sunday long table's window (Letters evening, its first user, went in 0.62.0) in absolute ship minutes, null outside it
    T = g.ev("""(() => { const d = [...Array(28).keys()].map(x => x + 1).find(x => eventsOn(x).some(e => e.id === 'sunday-table')); if (!d) return null;
      const e = eventsOn(d).find(x => x.id === 'sunday-table'), B = (d - 1) * 1440;
      return { d, at: [B + e.from - 1, B + e.from, B + e.to - 1, B + e.to].map(t => tradOn('sunday-table', t)), other: tradOn('sunday-table', B + 600), none: tradOn('nope', B + e.from) }; })()""")
    print('tradOn sunday-table:', T and T['d'], T and [x and (x['from'], x['to']) for x in T['at']])
    if not T or T['at'][0] or not T['at'][1] or not T['at'][2] or T['at'][3] or T['other'] or T['none'] or T['at'][1]['day'] != T['d']: fail(f"tradOn('sunday-table'): {T}")

    # 9c. upcomingTraditions' deck and room (0.34.42, the device's Go there): a deck number, and a room key on that deck or null
    U = g.ev("upcomingTraditions(0, 8 * 1440).map(x => [x.id, x.deck, x.room, Number.isInteger(x.deck) && (x.room === null || !!(DECKS[x.deck].rooms || {})[x.room])])")
    print('upcomingTraditions, days 1-8:', len(U), 'with a room key:', sum(1 for u in U if u[2]))
    if not U or not all(u[3] for u in U) or not any(u[2] for u in U): fail(f"upcomingTraditions' deck/room: {[u for u in U if not u[3]][:5]}")

    # 9d. crew rotation traditions (0.34.43): the farewell supper the day before each rotation day (its leavers), the
    # crew welcome tea the first Friday after (its arrivals); {names} filled; the honorees' friends, department, cabin
    RT = g.ev("""(() => ROSTER_ROTATIONS.map(r => { const row = { day: r.day };
      for (const [id, d, ids] of [['farewell-supper', r.day - 1, r.out], ['crew-welcome-tea', r.day + 1 + (4 - weekday(r.day + 1) + 7) % 7, r.in]]) {
        const e = eventsOn(d).find(x => x.id === id), go = e ? schedPeople().filter(p => planDay(p, d).some(s => s.tag && s.tag.startsWith('ev-' + id))) : [];
        row[id] = e ? { d, hon: e.honorees.map(p => p.id).sort().join(',') === ids.slice().sort().join(','), names: e.names, mail: !!(e.ev.mail && e.ev.mail(e)), went: go.length,
          honWent: go.filter(p => e.honorees.includes(p)).map(p => p.id + (p.shift === 'night' ? '(night)' : '')), others: go.filter(p => !e.honorees.includes(p)).length } : { d, missing: true, dropped: (EV_DROPPED.get(d) || []).includes(id) };
      }
      return row; }))()""")
    for r in RT:
        print(f"  rotation day {r['day']}: " + '; '.join(f"{k} day {v['d']}: " + ('MISSING' if v.get('missing') else f"{v['names']} ({'honorees ok' if v['hon'] else 'WRONG honorees'}), went {v['went']}, honorees {v['honWent']}") for k, v in r.items() if k != 'day'))
        for k, v in r.items():
            if k == 'day': continue
            if v.get('missing') or not v['hon'] or not v['mail'] or v['others'] < 2: fail(f"{k} for the rotation on day {r['day']}: {v}")

    # 9e. Quiz night's mini-game (0.34.51): three questions from the pool (a stand-in pool here, unless the build has the
    # head writer's), the same three for a day, different the next week; joining the quiz in the bow lounge opens it;
    # a right and a wrong answer each get Tomas's remark, the score at the end
    Q = g.ev("""(() => { const keep = {}, real = !!LINES['quiz.q3.text'];
      if (!real) { const set = (k, v) => { keep[k] = LINES[k]; LINES[k] = [{ text: v }]; };
        for (let i = 1; i <= 7; i++) { set('quiz.q' + i + '.text', 'Q' + i + '?'); set('quiz.q' + i + '.a1', 'R' + i); for (const k of [2, 3, 4]) set('quiz.q' + i + '.a' + k, 'W' + i + k); }
        set('quiz.right', 'Right.'); set('quiz.wrong', 'It was {answer}.'); set('quiz.done', '{n} of 3.'); }
      const d = 4, a = quizPick(d), out = { real, three: a.length === 3 && new Set(a.map(x => x.q)).size === 3, same: JSON.stringify(a) === JSON.stringify(quizPick(d)),
        next: quizPick(d + 7).map(x => x.q).join() !== a.map(x => x.q).join(), oneRight: a.every(x => x.answers.includes(x.right) && x.answers.length >= 3 && x.answers.length <= 4) };
      const was = DIALOGUE; if (was) dialogueClose();
      out.start = quizStart(d, shipNow()); const seen = [];
      for (let s = 0; s < 14 && DIALOGUE && DIALOGUE.id === 'moment:quiz'; s++) { const v = dialogueView(); if (!v) break;
        if (v.choices) { const x = a[Math.floor(s / 3)], k = s < 3 ? v.choices.indexOf(x.right) : v.choices.findIndex(c => c !== x.right); seen.push('pick ' + v.choices[k]); dialogueChoose(k); }
        else { seen.push(v.text); dialogueNext(); } }
      out.seen = seen; out.score = QUIZ_LAST && QUIZ_LAST.score; out.closed = !DIALOGUE;
      for (const k in keep) { if (keep[k] === undefined) delete LINES[k]; else LINES[k] = keep[k]; }
      return out; })()""")
    print('Quiz night game:', Q)
    if not (Q['three'] and Q['same'] and Q['next'] and Q['oneRight'] and Q['start'] and Q['closed'] and Q['score'] is not None and 1 <= Q['score'] <= 3 and len(Q['seen']) >= 7): fail(f"the quiz game: {Q}")

    # 10. the bridge invite (0.34.35), last: it skips on to day 50
    I = g.ev(INVITE)
    print('Bridge invite: eves', I['eves'][:4], '| booked', I['booked'], '| Vance there', I['vanceThere'], '| open', I.get('open'), '| flag', I.get('flagBefore'), '->', I.get('flagAfter'), '| after', I['after'], '| bridge hour day 23', I['before'], '->', I['on23'], f"({I['going']} going)")
    print('  slept through:', I['slept'], 'flag', I['sleptFlag'], '| Mail', [x for x in I['mails1'] + I['mails2'] if 'invitation' in x or 'Bridge hour' in x])
    if I['eves'][:2] != [22, 50] or I['before']: fail(f"the bridge invite's days: {I['eves']} (bridge hour on day 23 before the invite: {I['before']})")
    if len(I['booked']) != 1 or not I['booked'][0].startswith('bridgeInvite@22 ') or not I['booked'][0].endswith(' asked'): fail(f"the bridge invite wasn't booked for day 22: {I['booked']}")
    if not I['vanceThere'] or I['appt']: fail(f"the bridge invite: Vance not at breakfast in the mess, or an appointment made: {I['vanceThere']} {I['appt']}")
    if I.get('open') != 'bridgeInvite' or I.get('flagBefore') or not I.get('flagAfter') or not any('best view' in x for x in I.get('lines', [])): fail(f"the bridge invite didn't play, or its reply didn't set the flag: {I.get('open')} {I.get('lines')}")
    if I['after'] != ['bridgeInvite@22 kept'] or not I['on23'] or not I['going']: fail(f"after the invite: {I['after']}, bridge hour on day 23 {I['on23']} ({I['going']} going)")
    if any('An invitation (notes)' in x for x in I['mails1']) or not any(x.startswith('22 18:00') and 'Bridge hour' in x for x in I['mails1']): fail(f"the Mail around a played invite: {I['mails1']}")
    if I['slept'] != ['bridgeInvite@50 missed'] or not I['sleptFlag'] or not any('An invitation (notes)' in x for x in I['mails2']): fail(f"a slept-through invite: {I['slept']} flag {I['sleptFlag']} {I['mails2']}")

    # 11. a New game (0.34.50; reviewer 1b): section 18's per-game state starts again (last: it restarts the game)
    NG = g.ev("""(() => {
      SHIP.commendations.push({ event: 'ionStorm', day: 16 }); skipTo(18 * 1440 + 900);   // books the Captain's table (day 20)
      SHIP.traces.push('framedMenu'); SHIP.events.sent.push('quiz@4'); SHIP.events.votes['tasting-table@3'] = 'x'; flagSet('bridge.invited');
      const before = { occ: SHIP.occasions.length, com: SHIP.commendations.length, tr: SHIP.traces.length };
      newGameStart(false); skipTo(3 * 1440 + 600);
      return { before, occ: SHIP.occasions.map(o => o.key), com: SHIP.commendations.length, ev: SHIP.event, log: SHIP.eventLog.length, tr: SHIP.traces.slice(),
        sent: SHIP.events.sent.filter(k => !/@[1-5]$/.test(k)), votes: Object.keys(SHIP.events.votes), meet: MEETINGS.filter(m => m.event === 'occasion').map(m => m.id), flag: !!flag('bridge.invited'), day: Math.floor(shipNow() / 1440) + 1 };
    })()""")
    print('New game: before', NG['before'], '| after: occasions', NG['occ'], 'commendations', NG['com'], 'traces', NG['tr'], 'old Mail keys', NG['sent'], 'votes', NG['votes'], 'occasion meetings', NG['meet'], 'flag', NG['flag'], 'day', NG['day'])
    if not NG['before']['occ'] or NG['occ'] or NG['com'] or NG['ev'] or NG['log'] or NG['tr'] or NG['sent'] or NG['votes'] or NG['meet'] or NG['flag']: fail(f"a New game kept section 18's state: {NG}")

    if g.errors: fail(f"console: {g.errors[:4]}")
    g.b.close()

print('EVENTS CHECK OK' if ok else 'EVENTS CHECK FAILED')
sys.exit(0 if ok else 1)
