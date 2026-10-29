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
#   meal traditions thin out: at most 6 diners get up in any one minute (Days 0-21), Day 0's table full till Zeke's goodnight;
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
  const n = { week: 1, '2weeks': 2, '3weeks': 3, '4weeks': 4, '6weeks': 6, '8weeks': 8 }[w.every || (w.weekday != null ? 'week' : '')];   // 3 and 6: 0.93.2 (FX24)
  if (w.any) { for (const x of w.any) dueNew(x, lo, hi).forEach(d => add(d)); return s; }   // either rhythm (0.93.2, TRAD_0932_WHEN)
  if (Array.isArray(w.weekday)) { for (const x of w.weekday) dueNew({ ...w, weekday: x }, lo, hi).forEach(d => s.add(d)); return s; }
  if (w.after === 'arrival') { const a = typeof introArrival === 'function' ? introArrival() : 0;
    if (w.days != null) add(a + w.days); else add(a + 1 + (w.weekday - wdOf(a + 1) + 7) % 7 + 7 * ((w.nth || 1) - 1)); }
  else if (n) { const first = 1 + 7 * ((w.week || 1) - 1) + w.weekday; for (let d = first; d <= hi; d += 7 * n) add(d); for (let d = first - 7 * n; d >= lo; d -= 7 * n) add(d); }
  else if (w.every === 'quarter') for (let q = 0; 91 * q + 1 <= hi; q++) add(91 * q + (w.quarterDay != null ? w.quarterDay : 1 + 7 * ((w.week || 1) - 1) + w.weekday));
  else if (w.every === 'year') for (let y = 0; 364 * y + 1 <= hi; y++) add(364 * y + (w.dayOfYear != null ? w.dayOfYear : 1 + 7 * ((w.week || 1) - 1) + w.weekday));
  return s;
})"""
IS_NEW = "(w => !!w.any || typeof w.every === 'string' || !!w.after || w.season != null || w.from != null || w.until != null || Array.isArray(w.weekday))"

PLANS = r"""(days => {
  const out = { days: [], bad: [], empty: [], ids: SHIP_TRADITIONS.filter(e => !e.flag || (typeof flag === 'function' && flag(e.flag))).map(e => e.id) }, LINGER = 25;   // staying on a little after the end is fine
  const isNew = """ + IS_NEW + r""", dueNew = """ + DUE_NEW + r""", lo = Math.min(...days), hi = Math.max(...days);
  const DUE = new Map(SHIP_TRADITIONS.filter(ev => isNew(ev.when)).map(ev => [ev.id, dueNew(ev.when, lo, hi)]));
  const tagId = tag => { if (SHIP_TRADITIONS.some(e => e.id === tag.slice(3))) return tag.slice(3); const m = /^ev-(.+?)(-(talk|drink|play|water|wash|read|cheer|clap|disc|cocoa|cook|fold))?$/.exec(tag); return m && m[1]; };   // an id first (rec-chiefs-talk ends like an anim)   // cheer, clap, disc: the rec deck's (0.83, RA)
  for (const d of days) {
    const on = eventsOn(d), wd = weekday(d), yd = shipYearDay(d), row = { d, wd: WEEKDAYS[wd].slice(0, 3), ev: [] };
    // due exactly when the table says
    for (const ev of SHIP_TRADITIONS) {
      const w = ev.when, due = !(ev.flag && !(typeof flag === 'function' && flag(ev.flag))) && !(ev.unflag && typeof flag === 'function' && flag(ev.unflag)) && (w.rota ? TRAD_ROTA[w.rota](d) : w.birthday ? schedPeople().some(p => birthdayOf(p) === yd && (typeof aboard !== 'function' || (aboard(p, d) && (typeof guestStay !== 'function' || guestStay(p, d) !== 'leave')))) : w.rotation != null ? ROSTER_ROTATIONS.some(r => (w.rotation === 'after' ? d > r.day && d <= r.day + 7 && weekday(d) === w.weekday : d === r.day + w.rotation) && (w.rotation !== 'after' && w.rotation < 0 ? r.out : r.in).some(id => { const p = schedPeople().find(q => q.id === id); return p && (!w.dept || p.dept === w.dept) && (typeof aboard !== 'function' || aboard(p, d)); })) : DUE.has(ev.id) ? DUE.get(ev.id).has(d) : (w.weekday === wd || (w.every && d % w.every === w.on) || w.yearDay === yd)) && !eventPauses(ev, d) && !(EV_DROPPED.get(d) || []).includes(ev.id) && !(ev.skip && ev.skip(d));   // a ship-wide event's quiet days; the voice budget
      const dd = typeof EV_DAY_DRESS !== 'undefined' ? EV_DAY_DRESS.get(ev.id + '@' + d) : null;   // a ship-wide event's day dress (the storm update): dropped that day, or added on a day it doesn't fall
      const want = dd ? !dd.drop && !eventPauses(ev, d) && !(EV_DROPPED.get(d) || []).includes(ev.id) : due;
      if (want !== on.some(e => e.id === ev.id)) out.bad.push(d + ' ' + ev.id + (want ? ' due but not on' : ' on but not due'));
    }
    const S = schedData(), went = {}, places = {};
    for (const p of schedPeople()) for (const s of planDay(p, d)) {
      if (!s.tag || !/^ev-/.test(s.tag) || (typeof eventMeetTag === 'function' && eventMeetTag(s.tag))) continue;   // a ship-wide event's meeting (F0b), not a tradition
      { const m = /^ev-(\w+)-/.exec(s.tag); if (m && SHIP_EVENTS[m[1]] && !SHIP_TRADITIONS.some(e => e.id === s.tag.slice(3))) continue; }   // an event guest's own steps (Taavek's ev-veyliVessel-ramp...), not a tradition (EV1: the guests' days are on paper from Day 1 now)
      const id = tagId(s.tag), e = on.find(x => x.id === id), B = (d - 1) * 1440;
      if (!e) { out.bad.push(d + ' ' + p.id + ' at ' + id + ', which is not on'); continue; }
      if (s.from + (s.walk || 0) < B + e.from - Math.max(e.ev.early || 0, p.id === e.ev.host || typeof P926_TRADS !== 'undefined' && P926_TRADS && /^rec-(wren|chiefs)-talk$/.test(e.id) && recSpeaker(p, d) ? 5 : 0, e.ev.meal && typeof TRAD_LINE !== 'undefined' ? TRAD_LINE[1] : 0, e.ev.lead ? 35 : 0) ||   // the sim plans a host 5 minutes early; a meal tradition's diners sit as the line serves them, up to TRAD_LINE[1] early (sim 0.26.41); the Captain's address seats them up to 30 minutes early (18f's friLead), its host 5 more
         s.to > B + e.to + LINGER) out.bad.push(d + ' ' + p.id + ' at ' + id + ' ' + hhmm(s.from - B) + '-' + hhmm(s.to - B) + ' outside ' + hhmm(e.from) + '-' + hhmm(e.to));
      const pools = (e.ev.whereFor ? e.ev.whereFor(p, d, eventOpts(e.ev, p)) : eventOpts(e.ev, p)).map(([n, k]) => S.shared.get(n + '|' + k) || []).flat().map(pl => pl.id);   // a place by person too (whereFor: the comet's hosts at their own spots, FX25)
      if (!pools.includes(s.placeId) && !(s.act === 'commute' && !s.placeId)) out.bad.push(d + ' ' + p.id + ' at ' + id + ' in ' + s.placeId + ', not one of its places');
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
  if (typeof DIALOGUE !== 'undefined' && DIALOGUE) dialogueEnd(true); if (typeof CREW_SCENE !== 'undefined') CREW_SCENE.clear();   // EN2: a scene left open, or someone sent walking, by a later day's play (the ending's) doesn't follow the clock back
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
          const s = att.get(a.p.id), w = s && planWhere(a.p, now);   // the seat their plan gives now: the deck running makes the day's plans again with the week's friendships (backlog #24)
          if (s && w && w.deck === n && w.tag && w.tag.startsWith('ev-' + id) && a.spot.id === w.placeId) got.add(a.p.id);
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
    SHIP.event = null; SHIP.eventLog.length = 0; SHIP.eventLog.push(...EV_BEFORE('ionStorm')); SHIP.traces.length = 0; const m0 = MEETINGS.splice(0);
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
      if (SHIP.eventLog.some(l => l.id === 'ionStorm')) break;   // the storm's own run: the visit starts on Day 16 now it's on (EV1)
    }
    if (send) mailSend = send;
    if (real) { for (const x of NEWS.splice(n0)) { news.push(fmt(x)); delete SHIP.knows[x.id]; } } else delete window.newsAdd;
    const addr = ADDRESSES.slice(a0).map(x => Math.floor(x.at / 1440) + 1 + ' ' + hhmm(x.at % 1440) + ' ' + x.text);
    const meets = MEETINGS.slice(ms).map(m => m.id + ' day ' + (Math.floor(m.at / 1440) + 1) + ' ' + hhmm(m.at % 1440) + ' ' + m.script);
    ADDRESSES.length = a0; MEETINGS.length = 0; MEETINGS.push(...m0); EV_DAYS.clear();
    const res = { steps, sig: sig.join('|'), mods, log: JSON.parse(JSON.stringify(SHIP.eventLog.filter(l => l.id === 'ionStorm'))), traces: SHIP.traces.slice(), left: SHIP.event, addr, mails, meets, paused, news, on, gath, due,
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
  if (typeof DIALOGUE !== 'undefined' && DIALOGUE) dialogueEnd(true); if (typeof CREW_SCENE !== 'undefined') CREW_SCENE.clear();   // EN2: a scene left open, or someone sent walking, by a later day's play (the ending's) doesn't follow the clock back
  const dress = [], hadDress = typeof dressShow === 'function', ds = hadDress ? dressShow : null;
  const spy = l => { const k = l.map(x => typeof x === 'string' ? x : x.id + (x.lines ? '[' + x.lines.length + ']' : '')).join('+'); if (dress[dress.length - 1] !== k) dress.push(k); };
  // with the deck architect's dressShow in the game's own scope, a window stand-in is never seen: wrap the real one there
  if (hadDress) dressShow = l => { spy(l); return ds(l); }; else window.dressShow = spy;
  const D = {}, mails = [], send = mailSend; mailSend = m => { mails.push(Math.floor(m.at / 1440) + 1 + ' ' + hhmm(m.at % 1440) + ' ' + m.subject); };
  const keep = { e: SHIP.event, log: SHIP.eventLog.slice(), tr: SHIP.traces.slice() };
  SHIP.event = null; SHIP.eventLog.length = 0; SHIP.eventLog.push(...EV_BEFORE('ionStorm')); SHIP.traces.length = 0; MEETINGS.length = 0; FEEL.log.length = 0; FEEL_DONE.clear();
  const put = (n, id) => { if (deckDef.num !== n) goToDeck(n); const at = DECKS[n].places.find(p => p.id === id).at;
    player.obj.position.copy(cellPos(...nearestOpen(...cellPos(...at).toArray().filter((_, i) => i !== 1), player))); target.copy(player.obj.position).setY(.7); };
  const tick = (a, b) => { for (let t = a; t <= b; t++) { setShipNow(t); eventsTick(); } };
  const frames = () => { window.__skip = false; window.__step(1, 1); window.__step(2, 16); return renderer.info.render.calls; };
  skipTo(9 * 1440 + 7 * 60); eventStart('ionStorm', 10); EV_DAYS.clear(); eventAdvance(shipNow(), true);
  // the briefing: day 10 at its data's minute, the Works bay (09:15 since 0.70.1; 14:00 with the storm update, EV_STORM_ON)
  const bm = SHIP_EVENTS.ionStorm.meetings.find(m => m.id === 'stormBriefing').at[1];
  put(5, '5-jobboard-1'); tick(9 * 1440 + bm - 25, 9 * 1440 + bm + 1);
  D.briefing = DIALOGUE ? { open: true, cast: Object.fromEntries(Object.entries(DIALOGUE.cast).map(([k, p]) => [k, p.name])), first: dialogueView() } : { open: false };
  const devDlg = document.getElementById('devDlg');   // section 19's panel (deviceDialogue) when the device is merged, else the plain strip
  D.panel = !!(devDlg && !devDlg.hidden && devDlg.textContent.length > 5);   // section 19's panel (the plain strip went in the storm's clean-up, S9)
  D.calls1 = frames();
  const seen = []; let n = 0;
  while (DIALOGUE && n++ < 30) { const v = dialogueView(); seen.push((v.choices ? '[choice] ' + v.choices.join(' / ') : v.name + ': ' + v.text)); dialogueStep(v.choices ? 0 : undefined); }
  D.lines = seen; D.mine = { ...SHIP.event.mine }; D.closed = !DIALOGUE;
  tick(9 * 1440 + bm + 2, 9 * 1440 + bm + 14); machinesNow();   // PR4: the job you picked is yours once it's up (not only wanted)
  D.claimed = ((SHIP.jobs || []).find(x => x.event === 'ionStorm' && x.eventJob === 'stormBatteries') || {}).claimedBy || null;
  D.other = (SHIP.jobs || []).filter(x => x.claimedBy === 'you' && x.status === 'claimed' && x.kind !== 'favour' && x.eventJob !== 'stormBatteries').map(x => x.id);   // already on another board job (day 10: the Works drill): section 17 leaves the pick open then (EV4)
  D.onShift = typeof playerShiftOn === 'function' ? !!playerShiftOn(10) : true;   // this part runs the storm from day 10; held only on a day you work (the calendar's briefing is Day 11, a workday)
  D.choiceNotes = (window.__notes || []).filter(x => x.kind === 'choice').map(x => x.script + ':' + x.k + ':' + x.who.length);   // the ship note for your reply
  // the front: day 11, 14:00, on Deck 3
  skipTo(10 * 1440 + 13 * 60 + 50); put(3, '3-grab-1'); tick(10 * 1440 + 13 * 60 + 51, 10 * 1440 + 14 * 60 + 1);
  D.feel = FEEL.log.map(f => f.kinds.join('+')); D.banner = !!(document.getElementById('devAddr') && !document.getElementById('devAddr').hidden); D.flicker = !!eventMod('effect', 'flicker'); D.calls2 = frames();   // section 19's banner; the flicker 8b's shipFeelFrame reads (the plain stand-ins went in the storm's clean-up, S9)
  // the all-clear: day 13, 10:00, the observation room; then walk out to the bridge
  skipTo(12 * 1440 + 9 * 60 + 50); put(1, '1-tea-1'); tick(12 * 1440 + 9 * 60 + 51, 12 * 1440 + 10 * 60 + 1);
  D.allClear = DIALOGUE ? dialogueView() : null; D.calls3 = frames();
  put(1, '1-works-1'); tick(12 * 1440 + 10 * 60 + 2, 12 * 1440 + 10 * 60 + 2); D.walked = !DIALOGUE;
  skipTo(15 * 1440 + 10);
  D.log = JSON.parse(JSON.stringify(SHIP.eventLog.filter(l => l.id === 'ionStorm'))); D.traces = SHIP.traces.slice(); D.left = SHIP.event; D.mails = mails;
  D.dress = dress; if (hadDress) dressShow = ds; else delete window.dressShow;
  mailSend = send; SHIP.event = keep.e; SHIP.eventLog.length = 0; SHIP.eventLog.push(...keep.log); SHIP.traces.length = 0; SHIP.traces.push(...keep.tr);
  MEETINGS.length = 0; EV_DAYS.clear(); if (DIALOGUE) dialogueEnd(true); if (typeof deviceAddress === 'function') deviceAddress(null);
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
  // the summons: the first day from 17 the guard leaves a Captain's hour free (F1c; day 17 at 11:00 while it's off)
  let rd = 17; while (rd < 30 && !occReadyDay(rd)) rd++; const ra = occReadyAt(rd), B = (rd - 1) * 1440, ts = occTableSlot(20);
  R.want = { booked: 'readyRoom@' + rd + ' ' + hhmm(ra) + ' asked', kept: 'readyRoom@' + rd + ' kept', table: 'captainsTable@20 ' + hhmm(ts ? ts.at : 1170), missed: 'captainsTable@20 missed' };
  skipTo(16 * 1440 + 360); R.none = SHIP.occasions.length;
  SHIP.commendations.push({ event: 'ionStorm', day: 16 });
  skipTo(B + 400); R.booked = SHIP.occasions.map(r => r.key + ' ' + hhmm(r.at % 1440) + ' ' + r.status);
  R.doorBefore = occasionDoorOpen(1, 'R', B + ra - 60); R.doorAt = occasionDoorOpen(1, 'R', B + ra - 5);
  skipTo(B + ra - 20); goToDeck(1); const b = ROOM_BOX.R;   // inside the ready room (its door is section 14's doorOpenFor, not in yet)
  player.obj.position.copy(cellPos(Math.floor((b.i0 + b.i1) / 2), Math.floor((b.j0 + b.j1) / 2))); target.copy(player.obj.position).setY(.7);
  R.room = roomAt(...player.here());
  tick(B + ra - 19, B + ra + 1);
  R.open = DIALOGUE ? DIALOGUE.id : null; const seen = []; let n = 0;
  while (DIALOGUE && n++ < 20) { const v = dialogueView(); seen.push(v.choices ? '[choice]' : v.who + ': ' + v.text); dialogueStep(v.choices ? 2 : undefined); }
  R.lines = seen; tick(B + ra + 2, B + ra + 30);
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
  R.slept = SHIP.occasions.filter(r => /^bridgeInvite/.test(r.key)).map(r => r.key + ' ' + r.status);   /* (BM19, N6's find) only the invite: with Step 6 on, the missed nights bring the Chief's summons onto Day 50 too */ R.sleptFlag = !!flag('bridge.invited'); R.mails2 = mails.slice();
  mailSend = send; SHIP.occasions.length = 0; SHIP.occasions.push(...keep); MEETINGS.length = 0; flagSet('bridge.invited', null); if (DIALOGUE) dialogueEnd(true);
  return R;
})()"""

# the hooks for others (0.34.13): the party through eventPlan (in play, day 13), eventRoutines, eventGuestDays,
# a one-off (Pell's show) added for a later day and planned like a tradition
HOOKS = r"""(() => {
  const R = {}, s0 = typeof EV_CAL_ON !== 'undefined' && EV_CAL_ON ? EV_CALENDAR.find(r => r.id === 'ionStorm').day : 10, o = (s0 - 10) * 1440;   // the storm's start: day 10, or the calendar's day 11 (F0)
  EV_DAYS.clear(); SHIP_DAYS.clear();   // plans made while earlier parts ran the storm from day 10 (LIVE) are made again
  R.s0 = s0; R.partyDay = eventsOn(s0 + 3).map(e => e.id); R.party11 = eventsOn(s0 + 1).some(e => e.id === 'party');
  R.partyGoing = schedPeople().filter(p => planDay(p, s0 + 3).some(s => s.tag && s.tag.startsWith('ev-party'))).length;
  R.partyPlaces = [...new Set(schedPeople().flatMap(p => planDay(p, s0 + 3).filter(s => s.tag && s.tag.startsWith('ev-party')).map(s => s.placeId)))].slice(0, 4);
  R.routines = [11 * 1440 + 900, 12 * 1440 + 400, 12 * 1440 + 700, 13 * 1440 + 100].map(t => eventRoutines(t + o).map(r => r.rule).join(','));
  R.guest = eventGuestDays({ event: 'ionStorm', stay: 3 }); R.noGuest = eventGuestDays({ event: 'nope', stay: 3 });
  R.owed = schedPeople().filter(p => callOwed(p, s0)).length;
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

# the diplomatic visit (event 2, 0.34.16) on paper, twice, as the build has it (EV1, 2026-10-28: on in a real game with
# the event swap; no longer forced on here: a build where it's still a draft is skipped, and failed if the swap is on):
# after the storm (logged, ending day 16) it's due from day 23;
# run from day 23 to its end; phases, addresses, Mail, meetings, the farewell as a gathering, the guests' days, the
# formal dinners' galley batch on days 3 and 5 only, and the greeting's cast with the Veyli names
DIPLO = r"""(() => {
  if (SHIP_EVENTS.diplomatic.draft) return { draft: true };   // off in this build: nothing to run
  const keep = { e: SHIP.event, log: SHIP.eventLog.slice(), tr: SHIP.traces.slice(), m: MEETINGS.splice(0) };
  const D = SHIP_EVENTS.diplomatic, on = D.phases.find(p => p.id === 'onset').at[0], fw = D.moments.find(m => m.id === 'farewell').at[0];   // the greeting's and the farewell's days (2 and 7; 1 and 3 with the event swap, 0.93.2)
  const run = () => {
    SHIP.event = null; SHIP.eventLog.length = 0; SHIP.traces.length = 0; MEETINGS.length = 0; EV_DAYS.clear();
    SHIP.eventLog.push(...EV_BEFORE('ionStorm'), { id: 'ionStorm', startDay: 10, endDay: 16, band: 'smooth', threads: {}, mine: {} }); SHIP.eventLog.push(...EV_BEFORE('diplomatic').filter(l => !SHIP.eventLog.some(x => x.id === l.id)));   // and any calendar event before it (the comet on Day 22 without the swap, FX25)
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
      farewell: eventsOn(sd + fw).filter(e => e.id === 'farewell').map(e => e.from + '-' + e.to), going: schedPeople().filter(p => planDay(p, sd + fw).some(s => s.tag && s.tag.startsWith('ev-farewell'))).length,
      guests: ['teshavi', 'kesrin'].map(id => { const g = typeof GUESTS !== 'undefined' && GUESTS.find(x => x.id === id); return g ? id + ':' + (eventGuestDays(g) || []).map(d => d - sd).join('-') : id + ':-'; }),
      log: SHIP.eventLog.filter(l => l.id === 'diplomatic').map(l => l.band + ' ' + JSON.stringify(l.threads)), traces: SHIP.traces.slice() };
    ADDRESSES.length = a0; return R;
  };
  const a = run(), b = run();
  const sc = MEETING_SCRIPTS.veyliGreeting; dialogueShow('veyliGreeting', { id: 'veyliGreeting', who: ['marrow', 'vance', 'saruth', 'teshavi', 'kesrin'], at: shipNow() });
  const names = []; let n = 0; while (DIALOGUE && n++ < 20) { const v = dialogueView(); names.push(v.choices ? '[choice]' : v.who); dialogueStep(v.choices ? 1 : undefined); }
  // live: the greeting plays when you're in the shuttle bay at 10:00 on the visit's day 2
  SHIP.event = null; SHIP.eventLog.length = 0; SHIP.eventLog.push(...EV_BEFORE('ionStorm'), { id: 'ionStorm', startDay: 10, endDay: 16, band: 'smooth', threads: {}, mine: {} }); SHIP.eventLog.push(...EV_BEFORE('diplomatic').filter(l => !SHIP.eventLog.some(x => x.id === l.id)));   // and any calendar event before it (the comet on Day 22 without the swap, FX25) MEETINGS.length = 0; EV_DAYS.clear();
  const sd = a.due.day; eventStart('diplomatic', sd); EV_DAYS.clear();
  skipTo((sd - 1 + on) * 1440 + 580); goToDeck(5); const bx = ROOM_BOX.S;
  player.obj.position.copy(cellPos(Math.floor((bx.i0 + bx.i1) / 2), Math.floor((bx.j0 + bx.j1) / 2))); target.copy(player.obj.position).setY(.7);
  for (let t = (sd - 1 + on) * 1440 + 581; t <= (sd - 1 + on) * 1440 + 602; t++) { setShipNow(t); eventsTick(); }
  const live = { room: roomAt(...player.here()), open: DIALOGUE ? DIALOGUE.id : null, first: DIALOGUE ? dialogueView().who : null };
  if (DIALOGUE) dialogueEnd(true); if (typeof deviceAddress === 'function') deviceAddress(null);
  SHIP.event = keep.e; SHIP.eventLog.length = 0; SHIP.eventLog.push(...keep.log); SHIP.traces.length = 0; SHIP.traces.push(...keep.tr); MEETINGS.length = 0; MEETINGS.push(...keep.m); EV_DAYS.clear();
  return { a, same: JSON.stringify(a) === JSON.stringify(b), names, live };
})()"""

# the comet (FX25, 0.93.2; plans/events-plan-2.html Part A, A8), on paper with the events base on, twice from a clean
# slate (the calendar's earlier events logged): due Monday Day 22; the four gatherings 21:30-22:40 and who goes (the
# hosts, the counts, Officers and up only at the Captain's tea); nobody else in the four rooms 21:15-22:45; Gym club and
# the cup over by 21:15; a birthday that day an hour clear; then run Day 22 to Day 24: the phases at their minutes, Sato's
# Mail at 08:00 and the log on Day 23 at 08:00, the two jobs from 09:00, smooth with no threads and no commendation
COMET = r"""(() => {
  if (typeof EV_COMET_ON === 'undefined' || !EV_COMET_ON || !SHIP_EVENTS.comet) return { off: true, has: !!SHIP_EVENTS.comet, cal: (EV_CALENDAR.find(r => r.id === 'comet') || {}).day || null };
  const run = () => {
    const keep = { e: SHIP.event, log: SHIP.eventLog.slice(), tr: SHIP.traces.slice(), m: MEETINGS.splice(0), com: JSON.stringify(SHIP.commendations || null) };
    SHIP.event = null; SHIP.eventLog.length = 0; SHIP.eventLog.push(...EV_BEFORE('comet')); EV_DAYS.clear(); SHIP_DAYS.clear();
    const due = eventDueDay(), d = due ? due.day : 22, B = (d - 1) * 1440, ids = ['cometLounge', 'cometScope', 'cometStern', 'cometCaptain'];
    const on = eventsOn(d).map(e => e.id + ' ' + hhmm(e.from) + '-' + hhmm(e.to)), rooms = new Set(COMET.rooms.map(r => r[0]));
    const going = {}, junior = [], hosts = {}, intruders = [];
    for (const id of ids) going[id] = 0;
    for (const p of schedPeople()) for (const s of planDay(p, d)) {
      const m = s.tag && /^ev-(comet[A-Za-z]+)/.exec(s.tag), pl = s.placeId && placeById(s.placeId);
      if (m && ids.includes(m[1]) && s.from <= B + 1290 + 10 && s.to > B + 1290) { going[m[1]]++; if (m[1] === 'cometCaptain' && (p.rank === 'junior' || p.rank === 'guest')) junior.push(p.id); }
      if (m && SHIP_EVENTS.comet.moments.some(x => x.id === m[1] && x.host === p.id)) hosts[p.id] = hhmm(s.from % 1440) + '-' + hhmm(s.to % 1440);
      if (!m && pl && rooms.has(pl.deck + '|' + pl.room) && s.from < B + 1365 && s.to > B + 1275 && s.act !== 'sleep' && s.act !== 'work') intruders.push(p.id + ' ' + s.act + ' ' + (s.tag || '') + ' ' + hhmm(s.from % 1440) + '-' + hhmm(s.to % 1440) + ' ' + s.placeId);
    }
    const ev = eventsOn(d), gym = ev.filter(e => /^(running|department-cup)$/.test(e.id)).map(e => e.id + ' ' + hhmm(e.to)), bday = ev.filter(e => e.id === 'birthday').map(e => hhmm(e.from) + '-' + hhmm(e.to));
    const late = ev.filter(e => e.ev.when && !e.ev.when.ship && e.to > 1230 && e.from < 1425).map(e => e.id + ' ' + hhmm(e.from) + '-' + hhmm(e.to));
    // run it: Day 21 to Day 24 every 10 minutes, the Mail captured
    eventStart('comet', d); EV_DAYS.clear();
    const mails = [], send = typeof mailSend === 'function' ? mailSend : null, steps = [], phase = {}, jobs = [];
    if (send) mailSend = m => { mails.push(Math.floor(m.at / 1440) + 1 - d + ' ' + hhmm(m.at % 1440) + ' ' + m.subject); };
    for (let t = B - 60; t <= B + 2 * 1440 + 60; t += 10) {
      const o = eventAdvance(t, true); if (o.length) steps.push(Math.floor(t / 1440) + 1 - d + ' ' + hhmm(t % 1440) + ' ' + o.join(', '));
      const n = eventNow(t); if (n && n.id === 'comet' && !phase[n.phase]) phase[n.phase] = Math.floor(t / 1440) + 1 - d + ' ' + hhmm(t % 1440);
      if (t === B + 540) { const l = eventMod('jobs', undefined, t); if (Array.isArray(l)) for (const j of l) jobs.push(j.id + (j.rank ? ':' + j.rank : '') + ' ' + hhmm(j.at) + '-' + hhmm(j.hold)); }
    }
    if (send) mailSend = send;
    const log = SHIP.eventLog.filter(l => l.id === 'comet').map(l => l.band + ' ' + JSON.stringify(l.threads)), com = JSON.stringify(SHIP.commendations || null) !== keep.com;
    const R = { due, on, going, junior, hosts, intruders: intruders.slice(0, 8), nIn: intruders.length, gym, bday, late, steps, phase, mails, jobs, log, com, left: SHIP.event && SHIP.event.id };
    SHIP.event = keep.e; SHIP.eventLog.length = 0; SHIP.eventLog.push(...keep.log); SHIP.traces.length = 0; SHIP.traces.push(...keep.tr); MEETINGS.length = 0; MEETINGS.push(...keep.m); EV_DAYS.clear(); SHIP_DAYS.clear();
    return R;
  };
  const a = run(), b = run();
  return { a, same: JSON.stringify(a) === JSON.stringify(b) };
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

    # 1a. meal traditions thin out (the user, 2026-10-23: "the room must not all empty at once"; SC1's dinner-spread, RV8's
    # condition): on paper, Days 0-21, at most 6 diners get up from a meal tradition in any one minute (a diner's leaving is
    # the end of their seat, kept on past the tradition's end in the same seat: Day 0's linger), and Day 0's Sunday table is
    # still full 5 minutes before Zeke's goodnight to you (section 21's INTRO_STEPS 'free')
    SP = g.ev(r"""(() => { const worst = [];
      for (let d = 0; d <= 21; d++) { const day = shipDay(d), by = new Map();
        for (const [id, segs] of day.plans) segs.forEach((s, i) => {
          if (!(s.tag && /^ev-/.test(s.tag) && s.placeId && /dinner|breakfast|supper|lunch|meal|eat|sit/i.test(String(s.act)))) return;
          let k = i; while (segs[k + 1] && segs[k + 1].placeId === s.placeId && Math.abs(segs[k + 1].from - segs[k].to) < .5) k++;
          if (!by.has(s.tag)) by.set(s.tag, new Map()); const L = by.get(s.tag); if (!L.has(id)) L.set(id, Math.round(segs[k].to)); });
        for (const [tag, L] of by) { const c = new Map(); for (const m of L.values()) c.set(m, (c.get(m) || 0) + 1);
          let w = 0, wm = 0; for (const [m, n] of c) if (n > w) { w = n; wm = m; } worst.push([d, tag, L.size, w, ((wm % 1440) + 1440) % 1440]); } }
      const f = typeof introStepById === 'function' && introStepById('free'), day = shipDay(0), B = -1440, pl = new Set();
      for (const [, segs] of day.plans) for (const s of segs) if (s.tag && /^ev-sunday-table/.test(s.tag) && s.placeId) pl.add(s.placeId);
      const at = m => { let n = 0; for (const [, segs] of day.plans) if (segs.some(s => pl.has(s.placeId) && s.from <= m && s.to > m)) n++; return n; };
      let most = 0; if (f) for (let m = B + 17 * 60; m < B + f.at; m += 5) most = Math.max(most, at(m));
      return { worst: worst.sort((a, b) => b[3] - a[3]), day0: f ? { seats: pl.size, free: f.at, most, before: at(B + f.at - 5) } : null }; })()""")
    print('Meal traditions, most getting up in one minute (day, tag, diners, most, at):', SP['worst'][:3], '| Day 0 table:', SP['day0'])
    for w in SP['worst']:
        if w[3] > 6: fail(f"Day {w[0]} {w[1]}: {w[3]} of {w[2]} diners get up in the same minute ({w[4] // 60:02d}:{w[4] % 60:02d}); at most 6 (the room must not empty at once)")
    D0 = SP['day0']
    if not D0 or not D0['most'] or D0['before'] < D0['most']: fail(f"Day 0's Sunday table not full 5 minutes before Zeke's goodnight: {D0}")
    # the user, 2026-10-23 (FX5): once Zeke's goodnight has really happened (the Chief's talk and his explanation over;
    # SHIP.intro.done.free, live), the table trickles out from that minute: full till then, nobody up before it, a few
    # at a time after (at most 4 in a minute), nearly empty an hour later, and nobody else's plan changes (RV10: no one
    # off the table moves at that minute). On paper with the arrival on, at 18:20 and 19:10
    LV = g.ev(r"""(() => { const I = SHIP.intro, keep = [I.on, I.ended, I.done.free], out = [], B = -1440;
      I.on = true; I.ended = false;
      delete I.done.free; const base = new Map([...shipDay(0).plans].map(([id, x]) => [id, JSON.stringify(x)]));   // without a live goodnight
      for (const fr of [18 * 60 + 20, 19 * 60 + 10]) {
        I.done.free = B + fr; const day = shipDay(0), pl = new Set();
        const diners = new Set([...day.plans].filter(([, x]) => x.some(q => q.tag && /^ev-sunday-table/.test(q.tag))).map(([id]) => id));
        const others = [...day.plans].filter(([id, x]) => !diners.has(id) && base.get(id) !== JSON.stringify(x)).map(([id]) => id);   // RV10: nobody off the table may change
        for (const [, segs] of day.plans) for (const s of segs) if (s.tag && /^ev-sunday-table/.test(s.tag) && s.placeId) pl.add(s.placeId);
        const at = m => { let n = 0; for (const [, segs] of day.plans) if (segs.some(s => pl.has(s.placeId) && s.from <= m && s.to > m)) n++; return n; };
        const ups = new Map(), filler = [], pre = []; let early = 0;
        for (const [, segs] of day.plans) { const i = segs.findIndex(s => s.tag && /^ev-sunday-table/.test(s.tag) && s.placeId); if (i < 0) continue;   // the tradition's diners: when they get up from its seat (kept on in the same seat)
          let k = i; while (segs[k + 1] && segs[k + 1].placeId === segs[i].placeId && Math.abs(segs[k + 1].from - segs[k].to) < .5) k++;
          const m = Math.round(segs[k].to - B); if (m < fr) early++; ups.set(m, (ups.get(m) || 0) + 1);
          // FX8 (the user, 2026-10-23: "let them do what they will do"): once up, their own planned evening, no made-up wait
          // (0.92.1's bunk trip or standing about until their old time: the first step after the lift is 'off' at their bed
          // or nowhere); and nothing of theirs changes before the goodnight
          let n = k + 1; while (segs[n] && (segs[n].act === 'commute' || segs[n].type === 'lift-wait')) n++;
          const nx = segs[n], me = [...day.plans].find(([, x]) => x === segs)[0], bed = (schedData().people.find(q => q.id === me) || {}).bed;
          if (nx && m > fr && nx.act === 'off' && (!nx.placeId || nx.placeId === bed)) filler.push(me + ' ' + nx.type + ' ' + Math.round(nx.from - B));
          const cut = x => JSON.stringify(x.filter(q => q.from < B + fr).map(q => ({ ...q, to: Math.min(q.to, B + fr) })));
          if (cut(segs) !== cut(JSON.parse(base.get(me)))) pre.push(me); }
        out.push({ free: fr, seats: pl.size, before: at(B + fr - 5), most: Math.max(...[0, 10, 20, 30, 40].map(k => at(B + fr - 5 - k))), early, top: Math.max(0, ...ups.values()), others, after10: at(B + fr + 10), after60: at(B + fr + 60), filler, pre, span: [Math.min(...ups.keys()) - fr, Math.max(...ups.keys()) - fr] });
      }
      I.on = keep[0]; I.ended = keep[1]; if (keep[2] === undefined) delete I.done.free; else I.done.free = keep[2]; return out; })()""")
    print('Day 0 table from the live goodnight (free, seats, before, most, up before it, most up in a minute, others changed, 10 and 60 min after):', LV)
    for r in LV:
        if r['before'] < r['most'] or r['early'] or r['top'] > 4 or not (r['after10'] < r['before']) or r['after60'] > r['before'] // 5:
            fail(f"Day 0's table after the live goodnight at {r['free'] // 60:02d}:{r['free'] % 60:02d} doesn't trickle out from it (full till then, nobody up before, at most 4 a minute, nearly empty an hour later): {r}")
        if r['others']: fail(f"the live goodnight at {r['free'] // 60:02d}:{r['free'] % 60:02d} changed the plans of people not at the table (they'd move mid-activity): {r['others'][:6]}")
        if r['filler']: fail(f"after the live goodnight at {r['free'] // 60:02d}:{r['free'] % 60:02d}, diners up from the table wait about instead of their own evening (bunk or standing till their old time): {r['filler'][:6]}")
        if r['pre']: fail(f"the live goodnight at {r['free'] // 60:02d}:{r['free'] % 60:02d} changed diners' plans before it: {r['pre'][:6]}")

    # 1b. a whole ship year on paper (Pillar 4): the new rhythms due exactly when they should be, from day 0 (your
    # arrival) to day 364; the four seasons; the baked traditions (content/traditions, the TRADITIONS block) loaded
    yr = g.ev("""(() => {
      const isNew = """ + IS_NEW + """, dueNew = """ + DUE_NEW + """, out = { bad: [], count: {}, seasons: [], errors: TRAD_ERRORS.slice(), baked: [] };
      for (const ev of SHIP_TRADITIONS.filter(e => isNew(e.when))) {
        const due = dueNew(ev.when, 0, 364), on = new Set();
        for (let d = 0; d <= 364; d++) if (eventsOn(d).some(e => e.id === ev.id)) on.add(d);
        if (ev.flag && !(typeof flag === 'function' && flag(ev.flag))) { if (on.size) out.bad.push(ev.id + ' on without its flag ' + ev.flag); out.count[ev.id] = []; continue; }
        const dd = d => typeof EV_DAY_DRESS !== 'undefined' ? EV_DAY_DRESS.get(ev.id + '@' + d) : null;   // a ship-wide event's day dress (the storm update): dropped, or added on a day it doesn't fall
        for (const d of due) if (!on.has(d) && !eventPauses(ev, d) && !(EV_DROPPED.get(d) || []).includes(ev.id) && !(ev.skip && ev.skip(d)) && !(dd(d) && dd(d).drop)) out.bad.push(ev.id + ' due on day ' + d + ' but not on');
        for (const d of on) if (!due.has(d) && !(dd(d) && dd(d).add)) out.bad.push(ev.id + ' on day ' + d + ' but not due');
        out.count[ev.id] = [...on].sort((a, b) => a - b);
      }
      // the voice budget, every day of the year (0.34.51, 0.60.7): at most two traditions at once, never two at once in
      // one room (birthdays aside), and what it left out; and every weekday (Monday to Friday) has 2 or more
      out.dropped = [];
      for (let d = 0; d <= 364; d++) {
        const all = eventsOn(d).filter(e => SHIP_TRADITIONS.some(t => t === e.ev || t.id === e.ev.id) && !e.ev.when.birthday), recOnly = e => e.ev.where.every(w => w.deck === 7);
        const t = all.filter(e => !recOnly(e));   // the rec deck's own are budgeted among themselves (0.83, RA): one at a time in a room, checked below with the rest
        for (const x of t) if (t.filter(k => k.from <= x.from && x.from < k.to).length > 2) out.bad.push('day ' + d + ': more than two traditions at once at ' + x.from);
        for (const a of all) for (const b of all) if (a !== b && recOnly(a) && recOnly(b) && a.from < b.to && b.from < a.to && evRooms(a.ev).some(r => evRooms(b.ev).includes(r))) out.bad.push('day ' + d + ': ' + a.id + ' and ' + b.id + ' at once in one room');
        for (const a of t) for (const b of t) if (a !== b && a.from < b.to && b.from < a.to && evRooms(a.ev).some(r => evRooms(b.ev).includes(r))) out.bad.push('day ' + d + ': ' + a.id + ' and ' + b.id + ' at once in one room');
        const bday = eventsOn(d).some(e => e.ev.when.birthday) ? 1 : 0;   // 0.92.5 (FX12): a birthday counts, as the weekly ones within an hour of it give way to it
        if (d >= 1 && weekday(d) < 5 && t.length + bday < 2 && !eventOn(d)) out.bad.push('day ' + d + ' (a weekday) has ' + (t.length + bday) + ' tradition(s), not 2-3');
        if (EV_DROPPED.get(d)) out.dropped.push(d + ':' + EV_DROPPED.get(d).join('+'));
      }
      for (const d of [0, 1, 91, 92, 182, 183, 273, 274, 364, 365]) out.seasons.push(d + ':' + season(d) + ':' + seasonOf(d).week);
      const ks = SHIP_TRADITIONS.map(e => e.k); if (new Set(ks).size !== ks.length) out.bad.push('two traditions share a hash key k');
      out.invites = SHIP_TRADITIONS.filter(e => e.invite).map(e => e.id + ':' + e.invite.host);   // for section 20's invitations
      for (const e of SHIP_TRADITIONS.filter(e => e.invite)) { const v = e.invite;
        if (!schedPeople().some(p => p.id === v.host) || !(v.odds > 0 && v.odds <= 1) || typeof v.line !== 'string' || !v.line || v.line.length > 140) out.bad.push(e.id + ': invite ' + JSON.stringify(v)); }
      for (const t of TRAD_LIST) {
        if (t.id === 'first-light' && !(typeof FLC_ON !== 'undefined' && FLC_ON)) continue;   // patch #26: loaded only with its switch on (section 15's FLC_ON)
        if (t.id === 'captains-address' && !(typeof SHORT_FRIDAY !== 'undefined' && SHORT_FRIDAY && REC_TRAD_ON)) continue;
        if (typeof P926_NEW !== 'undefined' && P926_NEW.has(t.id) && !P926_TRADS) continue;   // 0.92.6's new traditions (FX17): loaded only with P926_TRADS
        if (t.id === 'crew-welcome-tea' && typeof EV_SWAP_ON !== 'undefined' && EV_SWAP_ON) continue;   // gone with the event swap (0.93.2)
        if (typeof TRAD_0932_NEW !== 'undefined' && TRAD_0932_NEW.has(t.id) && !TRAD_0932_ON) continue;
        if (typeof TRAD_0932_ON !== 'undefined' && TRAD_0932_ON && t.id === 'crew-welcome-tea') { if (SHIP_TRADITIONS.some(e => e.id === t.id)) out.bad.push('crew-welcome-tea loaded with TRAD_0932_ON (retired)'); continue; }   // 0.93.2: retired   // 0.93.2's new traditions (FX24): loaded only with TRAD_0932_ON
        if (typeof TRAD_0932_ON !== 'undefined' && TRAD_0932_ON && (t.id === 'tasting-table' || t.id === 'tasting-table-late')) { if (!SHIP_TRADITIONS.some(e => e.id === 'tasting-table' && e.k === 1314)) out.bad.push('tasting-table-late not loaded as tasting-table'); continue; }   // 0.93.2: the reworked one in the old one's place
        if (typeof WEEKEND_TRADS !== 'undefined' && WEEKEND_TRADS.has(t.id) && !WEEKEND_ON) continue;   // the weekend traditions (0.92.5 item 16): loaded only with WEEKEND_ON   // Short Fridays: loaded only with its switch on (section 13's SHORT_FRIDAY; 18f) and the rec deck's traditions
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
        const was = flag(ev.flag), on = () => [...Array(56).keys()].map(x => x + 1).concat([92, 99, 97, 105]).filter(x => eventsOn(x).some(e => e.id === ev.id)).length;   // + 92, 99: a season's first Monday (the rec deck's all-hands, 0.83); 97, 105: 0.93.2's Lamplight paddle and Ring the bell (FX24)
        flagSet(ev.flag, null); const off = on(); flagSet(ev.flag, true); const yes = on(); flagSet(ev.flag, was === undefined ? null : was); eventsOn(1);
        out.flags = (out.flags || []).concat(ev.id + ': ' + off + ' without, ' + yes + ' with ' + ev.flag);
        if (off || !yes) out.bad.push(ev.id + ' and its flag ' + ev.flag + ': ' + off + ' days without, ' + yes + ' with');
      }
      // and each rhythm on its own, as a tradition designer might write it
      for (const w of [{ every: 'week', weekday: 6 }, { every: '2weeks', weekday: 1 }, { every: '2weeks', weekday: 1, week: 2 }, { every: '4weeks', weekday: 5, week: 3 }, { every: '8weeks', weekday: 0, week: 5, from: 29 },
          { every: '3weeks', weekday: 5, week: 2 }, { every: '6weeks', weekday: 6, week: 4, from: 64 }, { any: [{ weekday: 5, until: 7 }, { every: '2weeks', weekday: 5, week: 2 }] }, { any: [{ weekday: 3 }, { every: '2weeks', weekday: 1 }] },   // 0.93.2 (FX24)
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
    flc_on = g.ev("typeof FLC_ON !== 'undefined' && FLC_ON")
    fri_on = g.ev("typeof SHORT_FRIDAY !== 'undefined' && SHORT_FRIDAY && REC_TRAD_ON")
    wk_off = g.ev("typeof WEEKEND_TRADS !== 'undefined' && !WEEKEND_ON ? [...WEEKEND_TRADS] : []")
    wk_off += g.ev("typeof P926_NEW !== 'undefined' && !P926_TRADS ? [...P926_NEW] : []")   # 0.92.6's (FX17): only with P926_TRADS
    wk_off += g.ev("typeof EV_SWAP_ON !== 'undefined' && EV_SWAP_ON ? ['crew-welcome-tea'] : []")   # the new hand's tea after a rotation, gone with the event swap (0.93.2)
    wk_off += g.ev("typeof TRAD_0932_NEW !== 'undefined' ? (TRAD_0932_ON ? ['tasting-table-late', 'crew-welcome-tea'] : [...TRAD_0932_NEW]) : []")   # 0.93.2's (FX24): only with TRAD_0932_ON; the reworked tasting table loads as tasting-table
    for i in want_ids:
        if i.startswith('rec-') and not rec_on: continue    # the rec deck's own load only with the deck switched on (0.83)
        if i == 'first-light' and not flc_on: continue      # First Light Cocoa (patch #26) loads only with FLC_ON
        if i == 'captains-address' and not fri_on: continue  # the Captain's Friday address (Short Fridays, 18f) loads only with SHORT_FRIDAY
        if i in wk_off: continue                             # the weekend traditions (0.92.5 item 16) load only with WEEKEND_ON
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
        storm_cal = g.ev("typeof EV_CAL_ON !== 'undefined' && EV_CAL_ON")
        if g.ev("typeof P926_TRADS !== 'undefined' && P926_TRADS"): PLAN['rec-chiefs-talk'] = PLAN['rec-chiefs-talk'] + [32]; PLAN['rec-wren-talk'] = PLAN['rec-wren-talk'] + [36, 39]   # 0.92.6 (FX17): the full talk rota
        dress = g.ev("(() => { const o = {}; if (typeof EV_DAY_DRESS !== 'undefined') for (const [k, v] of EV_DAY_DRESS) { const [id, d] = k.split('@'); ((o[id] = o[id] || { drop: [], add: [] })[v.drop ? 'drop' : 'add']).push(+d); } return o; })()")
        rc = g.ev("""(() => { const out = { on: {}, n: {}, hosts: [], talks: [], paused: {} };
          for (const ev of SHIP_TRADITIONS) if (/^rec-/.test(ev.id)) for (let d = 1; d <= 42; d++) if (eventPauses(ev, d)) (out.paused[ev.id] = out.paused[ev.id] || []).push(d);   // a ship-wide event's quiet hours (the visit's greeting day, Day 17: EV1)
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
            if k == 'rec-slow-stretch' and storm_cal: want = [d for d in want if d != 14]   # Sunday Day 14 08:00: the calendar's storm (escalation) pauses it
            want = sorted((set(want) - set(dress.get(k, {}).get('drop', []))) | set(d for d in dress.get(k, {}).get('add', []) if d <= 42))   # a ship-wide event's day dress (the storm update: talent night a week on)
            want = [d for d in want if d not in rc['paused'].get(k, [])]
            if got != want: fail(f"{k} on days {got}, the plan says {want}")
        print('Rec deck traditions, days 1-42 (people at each):', '; '.join(f"{k} {v}" for k, v in sorted(rc['n'].items())))
        for x in rc['hosts']: fail(x)
        for d, size, by, ok_ in rc['talks']:
            if not ok_: fail(f"day {d}: the {size} talk without its speaker {by}")
        print('  the talks:', rc['talks'])
        mv = g.ev("""(() => { const sat = d => eventsOn(d).map(e => e.id).filter(i => i === 'film' || i === 'rec-film-night');
          const before = [6, 20].map(sat); recFirstAllHands(9 * 1440 + 600); const after = [27, 34].map(sat);   // Saturdays clear of the storm (the calendar's pauses Day 13)
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
        if i == 'film' and g.ev("typeof flag === 'function' && !!flag('rec.filmMoved')"): i = 'rec-film-night'   # moved by the first all-hands (the storm update: the Day 5 address, so before the walk)
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
    due = g.ev("[2, 3, 4, 5, 6, 7, 8].flatMap(d => eventsOn(d).filter(e => !(e.ev.quiet === 'career' && typeof recBigDay === 'function' && recBigDay(d)) && !e.ev.when.ship && e.ev.mail !== null).map(e => e.id + '@' + d))")   # the rec deck's weekly sport ones send none on the career's big days (0.83); a ship-wide event's gatherings (its own Mail and banner announce them) and a day it dresses with no Mail (Crossing the Line's supper: Vance's Mail covers it) send none
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
      const e0 = eventsOn(d1).find(x => x.id === 'tasting-table');   // its own window (0.93.2: after dinner with TRAD_0932_ON; off: 1100 in and 1200 after, as before)
      setShipNow((d1 - 1) * 1440 + e0.from + 5); const ok = tallyVote('tasting-table', a.choices[1]); const late = (setShipNow((d1 - 1) * 1440 + e0.to + 45), tallyVote('tasting-table', a.choices[0]));
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
    # the calendar's events before one (with Crossing the Line on: the Line, Days 6-8, before the storm), as already
    # run: the storm's and the visit's runs below log them first, as a game that got there would have
    g.ev("window.EV_BEFORE = id => { if (typeof EV_CAL_ON === 'undefined' || !EV_CAL_ON) return []; const r0 = EV_CALENDAR.find(r => r.id === id); return evCalPlan().filter(r => r.id !== id && r0 && r.day < r0.day).map(r => ({ id: r.id, startDay: r.day, endDay: r.day + SHIP_EVENTS[r.id].days, band: 'smooth', threads: {}, mine: {} })); }")
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
    due_day = g.ev("typeof EV_CAL_ON !== 'undefined' && EV_CAL_ON ? (EV_CALENDAR.find(r => r.id === 'ionStorm') || {}).day : 10")   # the calendar's day 11 (F0), else day 10
    if not st['due'] or st['due'].get('day') != due_day: fail(f"the storm isn't due on day {due_day} in play: {st['due']}")
    if len(a['addr']) != 2 or 'in it' not in a['addr'][0] or 'passed' not in a['addr'][1]: fail(f"the Captain's addresses: {a['addr']}")
    if not any('Storm prep' in x for x in a['mails']) or not any('how it went' in x for x in a['mails']): fail(f"the storm's Mail: {a['mails']}")
    if len(a['news']) != 7 or not all('@10 ' in x for x in a['news']): fail(f"the storm's news: {a['news']}")
    bt = g.ev("hhmm(SHIP_EVENTS.ionStorm.meetings.find(m => m.id === 'stormBriefing').at[1])")   # 09:15, or 14:00 with the storm update
    von = g.ev("!!SHIP_EVENTS.diplomatic && !SHIP_EVENTS.diplomatic.draft")   # the visit on (EV1): its warning is Day 16 09:00, the day after the storm
    if a['on'] != ['10:0 warning@360', '11:1 warning@0 onset@840', '13:3 escalation@0 resolution@600 afterglow@1320', '16:0 warning@540' if von else '16:-'] or f'stormBriefing works-bay {bt}' not in a['gath'][0] or 'party bow-lounge 19:00' not in a['gath'][1]: fail(f"eventOn / eventGatherings: {a['on']} {a['gath']}")
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
    # the pick is held unless you're already on another board job as it posts (section 17's rule): then it stays open for you
    # (this part runs the storm from day 10, a Works drill day: drill-<kind>@10 is yours; on the calendar's Day 11 it's held)
    if L.get('other'):
        print(f"  the battery job you picked stays open: you're already on {L['other']} (claimedBy {L.get('claimed')})")
        if L.get('claimed') is not None: fail(f"the battery job picked at the briefing went to {L.get('claimed')} while you were on {L['other']}")
    elif L.get('claimed') != 'you' and (L.get('onShift') or L.get('claimed') is not None): fail(f"the battery job picked at the briefing isn't yours once it's up: claimedBy {L.get('claimed')}")
    if not L['feel'] or 'jolt' not in L['feel'][0] or not L['banner'] or not L['flicker']: fail('the front was not felt (jolt, banner, flicker)')
    if not L['allClear'] or L['allClear']['name'] not in ('Captain Odile Marrow', 'Commander Teo Vance') or not L['walked'] or not any('The all-clear (notes)' in x for x in L['mails']): fail('the all-clear did not open, or walking out sent no gist')   # the writers' all-clear (the storm update) opens with Vance
    if max(L['calls1'], L['calls2'], L['calls3']) >= 450: fail('draw calls over 450 in the storm')
    if len(L['log']) != 1 or (L['left'] or {}).get('id', L['left']) not in (None, 'diplomatic') or not L['traces'] or not any('how it went' in x for x in L['mails']): fail(f"the live storm didn't end cleanly: {L['log']}")

    # 7. occasions (C10)
    O = g.ev(OCC)
    print('Occasions: before a commendation', O['none'], '| booked', O['booked'], '| door', O['doorBefore'], O['doorAt'], '| in room', O['room'])
    print('  ready room:', O['open'], O['lines'])
    print('  after:', O['after'], '| progress talk asked:', O['ask'], 'on a day off:', O['askOff'])
    print('  the table:', O['table'], '| batch', O['batch'], O['noBatch'], '| end', O['end'], '| traces', O['traces'])
    print('  Mail:', O['mails'])
    W = O['want']   # day 17 11:00 and the table at 19:30 while the guard is off; what the guard leaves when it's on (F1c)
    if O['none'] or not O['booked'] or W['booked'] not in O['booked'][0] or O['doorBefore'] or not O['doorAt']: fail(f"the ready-room summons: {O['booked']}, want {W['booked']}")
    if O['open'] != 'readyRoomFirst' or not any('Admiral' in x for x in O['lines']) or W['kept'] not in O['after']: fail(f"the ready room didn't play or wasn't kept: {O['open']} {O['after']}")
    if not O['ask'] or O['askOff']: fail('occasionAsk: the progress talk')
    if not any(W['table'] in x for x in O['table']) or not O['batch'] or O['noBatch']: fail(f"the Captain's table: {O['table']} {O['batch']}")
    if not any('captainsTable@20 missed' in x for x in O['end']) or 'framedMenu' in O['traces'] or not any('Captain\'s table (notes)' in x for x in O['mails']): fail(f"a missed table: {O['end']} {O['mails']}")

    # 8. the hooks for others
    H = g.ev(HOOKS)
    print(f"Hooks: party on day {H['s0'] + 3}", H['partyDay'], f"(day {H['s0'] + 1}:", H['party11'], ') going', H['partyGoing'], H['partyPlaces'])
    print('  routines (day 12 15:00, 13 06:40, 13 11:40, 14 01:40):', H['routines'], '| guest days', H['guest'], H['noGuest'], '| owed a call', H['owed'])
    print('  one-off:', H['added'], H['again'], H['today'], H['oneOffOn'], 'going', H['oneOffGoing'], '| Pell free:', H['hostFree'], '| host flagged:', H['hostFlag'])
    if 'party' not in H['partyDay'] or H['party11'] or H['partyGoing'] < 10: fail(f"the all-clear party is not planned on day {H['s0'] + 3}")
    if not H['routines'][0].startswith('doubleShift') or not H['routines'][1].startswith('doubleShift') or H['routines'][2] != 'rush' or H['routines'][3] != '': fail(f"eventRoutines: {H['routines']}")
    if H['guest'] != [H['s0'] + 1, H['s0'] + 4] or H['noGuest'] is not None: fail(f"eventGuestDays: {H['guest']}")
    if not H['added'] or H['again'] or H['today'] or 'pell-show' not in H['oneOffOn'] or not H['oneOffGoing'] or (H['hostFree'] and not H['hostFlag']): fail('eventOneOff')

    # 9. the diplomatic visit on paper
    V = g.ev(DIPLO)
    SW = g.ev("typeof EV_SWAP_ON !== 'undefined' && EV_SWAP_ON")   # the event swap (0.93.2): the short visit, Days 16-19, before the comet
    if V.get('draft'):
        (fail if SW else print)("the diplomatic visit is still a draft in this build" + (": with the event swap on it should run in a real game (the user, 2026-10-28)" if SW else " (no event swap): not run"))
    else:
        a = V['a']
        print('Diplomatic visit on paper: due', a['due'], '| the same twice:', V['same'])
        [print('  day ' + x) for x in a['steps']]
        print('  galley batch at 15:00 by day:', a['batch'], '| guests (days from the start):', a['guests'])
        print('  addresses:', a['addr']); print('  Mail:', a['mails']); print('  meetings:', a['meets'])
        print('  farewell:', a['farewell'], 'going', a['going'], '| result', a['log'], a['traces'])
        print('  greeting speakers:', V['names'], '| guests flag on days', a['guestsOn'])
        print('  live greeting (in the shuttle bay at 10:00):', V['live'])
        if V['live']['open'] != 'veyliGreeting' or V['live']['first'] != 'Captain Odile Marrow': fail(f"the live greeting: {V['live']}")
        if SW: print('  (the event swap is on: the short visit, Tuesday to Friday)')
        if a['guestsOn'] != ([1, 2] if SW else [2, 3, 4, 5, 6]): fail(f"the 'guests' effect: {a['guestsOn']}")
        if not a['due'] or a['due']['id'] != 'diplomatic' or (a['due']['day'] != 16 if SW else a['due']['day'] < 23) or not V['same']: fail(f"the diplomatic visit's start or repeatability: {a['due']} {V['same']}")
        want = ['warning', 'onset', 'escalation', 'resolution', 'afterglow', 'end']
        vs = a['steps']; e = next((i for i, x in enumerate(vs) if x.split(' ')[2:3] == ['end']), len(vs) - 1); vs = vs[:e + 1]   # the visit's own run: with the swap on, the comet starts inside the window
        if [w for x in vs for w in want if (' ' + w) in x.replace('phase ', ' ')] != want: fail(f"diplomatic phases: {a['steps']}")
        bd = dict(x.split(':') for x in a['batch'])
        if (bd.get('2') != '10' or any(v != '-' for k, v in bd.items() if k != '2')) if SW else (bd.get('3') != '10' or bd.get('5') != '10' or bd.get('4') != '-' or bd.get('1') != '-'): fail(f"the formal dinners' batch: {a['batch']}")
        if len(a['addr']) != 2 or len(a['meets']) != 2 or not a['farewell'] or a['going'] < 3: fail('the visit\'s addresses, meetings or farewell')
        if a['guests'][0] != ('teshavi:1-3' if SW else 'teshavi:2-7') and a['guests'][0] != 'teshavi:-': fail(f"the guests' days: {a['guests']}")
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
    # crew welcome tea the first Thursday after (its arrivals; the first Friday until PT1: the user's decision of 2026-10-21,
    # pinned here, so the tea's data moving off Thursday fails), and Off the Tern on the day itself (its arrivals, with ROT_TERN on; PT1); {names} filled; the
    # honorees' friends, department, cabin
    RT = g.ev("""(() => ROSTER_ROTATIONS.map(r => { const row = { day: r.day, teaWeekday: (SHIP_TRADITIONS.find(t => t.id === 'crew-welcome-tea') || { when: {} }).when.weekday }, tw = 3;
      for (const [id, d, ids] of [['farewell-supper', r.day - 1, r.out]].concat(typeof TRAD_0932_ON !== 'undefined' && TRAD_0932_ON ? [] : [['crew-welcome-tea', r.day + 1 + (tw - weekday(r.day + 1) + 7) % 7, r.in]]).concat(typeof ROT_TERN !== 'undefined' && ROT_TERN ? [['off-the-tern', r.day, r.in]] : [])) {
        const e = eventsOn(d).find(x => x.id === id), go = e ? schedPeople().filter(p => planDay(p, d).some(s => s.tag && s.tag.startsWith('ev-' + id))) : [];
        row[id] = e ? { d, hon: e.honorees.map(p => p.id).sort().join(',') === ids.slice().sort().join(','), names: e.names, mail: !!(e.ev.mail && e.ev.mail(e)), went: go.length,
          honWent: go.filter(p => e.honorees.includes(p)).map(p => p.id + (p.shift === 'night' ? '(night)' : '')), others: go.filter(p => !e.honorees.includes(p)).length } : { d, missing: true, dropped: (EV_DROPPED.get(d) || []).includes(id) };
      }
      return row; }))()""")
    SWT = g.ev("typeof EV_SWAP_ON !== 'undefined' && EV_SWAP_ON")   # the event swap (0.93.2): the rotations' new hand's tea is gone
    if SWT:
        if g.ev("SHIP_TRADITIONS.some(t => t.id === 'crew-welcome-tea')"): fail("the event swap: the rotations' new hand's tea should be gone")
        for r in RT: r.pop('crew-welcome-tea', None); r['teaWeekday'] = 3
    for r in RT:
        print(f"  rotation day {r['day']}: " + '; '.join(f"{k} day {v['d']}: " + ('MISSING' if v.get('missing') else f"{v['names']} ({'honorees ok' if v['hon'] else 'WRONG honorees'}), went {v['went']}, honorees {v['honWent']}") for k, v in r.items() if k not in ('day', 'teaWeekday')))
        if r['teaWeekday'] != 3 and not g.ev("typeof TRAD_0932_ON !== 'undefined' && TRAD_0932_ON"): fail(f"crew-welcome-tea's weekday is {r['teaWeekday']}, not Thursday (3), the user's decision")
        for k, v in r.items():
            if k in ('day', 'teaWeekday'): continue
            if v.get('missing') or not v['hon'] or not v['mail'] or v['others'] < 2: fail(f"{k} for the rotation on day {r['day']}: {v}")

    # 9d2. off the Tern on paper (PT1, PR7's ask): with ROT_TERN on, on each rotation day each arrival (id order, up to 3)
    # has 'arrive' at 5-tern-aisle-1 from 17:40 + 3k, then Off the Tern's tag at a crowd spot until 17:55; each leaver has
    # 'board' at 5-tern-aisle-1 ending at 15:00 - 3(n-1-k), then away; the greeter has 'greet' at 5-tern-ramp-foot.
    # Expected times worked out here from the roster, not from section 14's helpers
    TT = g.ev("""(() => { if (typeof ROT_TERN === 'undefined' || !ROT_TERN) return { off: true };
      const bad = [], P = schedPeople(), by = id => P.find(p => p.id === id), hm = m => hhmm(m % 1440);
      for (const r of ROSTER_ROTATIONS) { const B = (r.day - 1) * 1440, arr = r.in.slice().sort().slice(0, 3), lv = r.out.slice().sort().slice(0, 3);
        arr.forEach((id, k) => { const pl = planDay(by(id), r.day), i = pl.findIndex(s => s.placeId === '5-tern-aisle-1' && s.tag === 'arrive' && s.from === B + 1060 + 3 * k), nx = i >= 0 && pl[i + 1];
          if (i < 0 || !nx || !/^ev-off-the-tern/.test(nx.tag || '') || nx.to !== B + 1075 || !/shuttle-bay-crowd/.test(nx.placeId || '')) bad.push(r.day + ' arrival ' + id + ': ' + JSON.stringify(pl.filter(s => s.from >= B + 1050 && s.from < B + 1090).map(s => [hm(s.from), hm(s.to), s.act, s.placeId, s.tag]))); });
        lv.forEach((id, k) => { const pl = planDay(by(id), r.day), i = pl.findIndex(s => s.placeId === '5-tern-aisle-1' && s.tag === 'board' && s.to === B + 900 - 3 * (lv.length - 1 - k)), nx = i >= 0 && pl[i + 1];
          if (i < 0 || !nx || nx.act !== 'away') bad.push(r.day + ' leaver ' + id + ': ' + JSON.stringify(pl.filter(s => s.from >= B + 860 && s.from < B + 910).map(s => [hm(s.from), hm(s.to), s.act, s.placeId, s.tag]))); });
        const gr = P.filter(p => planDay(p, r.day).some(s => s.tag === 'greet' && s.placeId === '5-tern-ramp-foot' && s.from < B + 1060 && s.to > B + 1060)).map(p => p.id);
        if (gr.length !== 1) bad.push(r.day + ' greeter at the ramp foot: ' + JSON.stringify(gr)); }
      if (deckDef.num !== 5) goToDeck(5);                 // the ramp itself (rotTernTick): left alone on an ordinary day, shut on a rotation day before 17:40
      const keep = player.obj.position.clone(); player.obj.position.copy(cellPos(...nearestOpen(...cellPos(12, 12).toArray().filter((_, i) => i !== 1), null)));
      const R = ROSTER_ROTATIONS[0].day; ternRamp(true, 0); rotTernTick((R - 2) * 1440 + 1057, 5); const ord = TERN.target;
      ternRamp(true, 0); rotTernTick((R - 1) * 1440 + 1057, 5); const rot = TERN.target; ternRamp(true, 0); player.obj.position.copy(keep); ROT_TERN_UI.shut = -1;
      if (ord !== 1) bad.push('the ramp shut on an ordinary day (' + (R - 1) + ' 17:37)'); if (rot !== 0) bad.push('the ramp not shut on rotation day ' + R + ' at 17:37');
      return { off: false, bad }; })()""")
    print('Off the Tern on paper:', 'switched off' if TT['off'] else ('ok on every rotation' if not TT['bad'] else TT['bad'][:4]))
    if not TT['off'] and TT['bad']: fail(f"off the Tern on paper: {TT['bad'][:4]}")

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

    # 9f. the comet (FX25, 0.93.2), on paper (see COMET above); with the switch off (a copy, at the end): nothing at all
    CM = g.ev(COMET)
    if CM.get('off'):
        print('The comet: switched off (no entry:', not CM['has'], ')')
    else:
        a = CM['a']
        print('The comet on paper: due', a['due'], '| the same twice:', CM['same'])
        print('  that day:', a['on'])
        print('  going at 21:30 (bow glass, scope, blankets, Captain\'s tea):', a['going'], '| hosts', a['hosts'], '| juniors at the tea', a['junior'])
        print('  others in the four rooms 21:15-22:45:', a['nIn'], a['intruders'], '| gym:', a['gym'], '| birthday:', a['bday'], '| other evening traditions:', a['late'])
        print('  phases:', a['phase']); [print('    ' + x) for x in a['steps']]
        print('  Mail:', a['mails'], '| jobs at 09:05:', a['jobs'], '| result', a['log'], '| a commendation:', a['com'])
        G = a['going']
        if not a['due'] or a['due'].get('id') != 'comet' or a['due'].get('day') != 22: fail(f"the comet isn't due on Monday Day 22: {a['due']}")
        if sum(1 for x in a['on'] if x.endswith('21:30-22:40') and x.startswith('comet')) != 4: fail(f"the comet's four gatherings at 21:30-22:40: {a['on']}")
        if G['cometLounge'] < 30 or G['cometScope'] < 6 or G['cometStern'] < 6 or G['cometCaptain'] < 4 or a['junior']: fail(f"who goes to the comet: {G} (juniors at the Captain's tea: {a['junior']})")
        if set(a['hosts']) != {'sato', 'mori', 'tomas', 'marrow'}: fail(f"the comet's hosts: {a['hosts']}")
        if a['nIn']: fail(f"others in the comet's rooms 21:15-22:45: {a['intruders']}")
        if any(x.split(' ')[1] > '21:15' for x in a['gym']): fail(f"Gym club or the cup past 21:15: {a['gym']}")
        if any(x.split('-')[1] > '20:30' for x in a['bday']): fail(f"the birthday not an hour clear of the comet: {a['bday']}")
        if a['phase'] != {'warning': '0 07:00', 'onset': '0 21:30', 'resolution': '0 22:40', 'afterglow': '1 00:00'}: fail(f"the comet's phases: {a['phase']}")
        if a['mails'][:1] != ['0 08:00 A comet tonight'] or not any(x.startswith('1 08:00 ') and 'comet log' in x for x in a['mails']): fail(f"the comet's Mail: {a['mails']}")
        if a['jobs'] != ['cometBlankets 09:00-17:00', 'cometFilter:officer 09:00-17:00']: fail(f"the comet's jobs: {a['jobs']}")
        if a['log'] != ['smooth {}'] or a['com'] or a['left']: fail(f"the comet's end: {a['log']} commendation {a['com']} left {a['left']}")
        if not CM['same']: fail('the comet ran differently the second time')

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

# 12. Pick-your-own breakfast (FX12, 0.92.3 item 27, the user's): joined and finished at a garden bed, what you picked is
# your tray (the servery's own), with a toast and an arrow to a mess seat; a seat eats it and the arrow goes. Walked
# away part way: no tray. Once a day. A page of its own (the ship clock runs here)
PYO_ST = "[ACT && ACT.kind, ACT && ACT.phase, SHIP.player.tray, IX_GOAL && IX_GOAL.label, IX_GOAL && IX_GOAL.place, player.holding, document.getElementById('tx').textContent]"
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844); g.step(3)
    print('== Pick-your-own: a tray of what you picked')
    if g.ev("typeof GUIDE_ON !== 'undefined' && GUIDE_ON"): g.ev("GUIDE.tq.length = 0; guideToast = () => false")
    d = g.ev("(() => { for (let d = 2; d < 30; d++) if (eventsOn(d).some(e => e.id === 'pick-your-own')) return d; return null; })()")
    JOIN = f"""(() => {{ const e = eventsOn({d}).find(e => e.id === 'pick-your-own'); tradJoinMinute(shipNow()); const lead = tradLeader(e), a = DECK_CREW.find(c => c.p && c.p.id === lead) || DECK_CREW.find(c => c.p); return !!a && tradJoin(e, a); }})()"""
    def picking():
        for k in range(80):
            g.step(10)
            if g.ev("!!(ACT && ACT.kind === 'ixGarden' && ACT.phase === 'do')"): break
        g.step(70)
    # walked away part way: no tray (and still none after the minute ticks)
    g.ev(f"goToDeck(3); setShipNow(({d} - 1) * 1440 + 6 * 60 + 20)"); g.step(60)
    j = g.ev(JOIN); picking()
    s0 = g.ev("[ACT && ACT.kind, !!(ACT && ACT.def.onDone)]")
    g.ev("player.steer = { x: 1, z: 0, k: 1 }"); g.step(10); g.ev("player.steer = null"); g.step(60)
    s1 = g.ev(PYO_ST)
    print('  joined', j, d, '| picking', s0, '| walked away', s1[:5])
    if not (j and s0 == ['ixGarden', True]): fail(f"Pick-your-own: joining didn't start picking with a tray to come ({j}, {s0})")
    if s1[2] or s1[3] == 'Your breakfast: the mess hall': fail(f"Pick-your-own: walking away part way gave a tray ({s1[:5]})")
    # back at a bed, finished: the tray, the toast, the arrow at a mess seat, drawn in your hands
    g.ev("SHIP.events.joined = SHIP.events.joined.filter(k => !k.startsWith('pick-your-own@'))"); j = g.ev(JOIN); picking()
    g.ev("ACT.done = ACT.def.mins - .05")
    for k in range(40):
        g.step(10)
        if not g.ev("!!ACT"): break
    g.step(5); s2 = g.ev(PYO_ST); seat = s2[4]
    # it travels (the user, 0.92.4: the only tray that leaves the mess hall): still yours a while later, out in the garden
    g.step(90); s2b = g.ev("[roomAt(...player.here()), SHIP.player.tray, player.holding]")
    print('  a while later, out of the mess hall:', s2b)
    if not (s2b[0] != 'M' and s2b[1] == 'the fruit and greens you picked' and s2b[2] == 'tray'): fail(f"Pick-your-own: the tray didn't travel outside the mess hall ({s2b})")
    print('  finished:', s2[2:6], '|', s2[6][:90])
    if not (s2[2] == 'the fruit and greens you picked' and s2[3] == 'Your breakfast: the mess hall' and seat and seat.startswith('3-mess') and s2[5] == 'tray' and 'mess hall' in s2[6]):
        fail(f"Pick-your-own: finished, no tray of what you picked, toast or arrow at a mess seat ({s2})")
    # the tray is the servery's: a seat eats it (what you picked), and the arrow goes; picking again today: no second tray
    if seat:
        g.ev(f"actStart('sit', '{seat}', {{}})")
        for k in range(80):
            g.step(10)
            if g.ev("!!(ACT && ACT.kind === 'eat' && ACT.phase === 'do')"): break
        g.step(70); s3 = g.ev(PYO_ST)
        print('  at the seat:', s3[:5], '|', s3[6][:70])
        if not (s3[0] == 'eat' and not s3[2] and not s3[3] and 'you picked' in s3[6]): fail(f"Pick-your-own: a seat didn't eat the tray, or the arrow stayed ({s3})")
        # sat down with it, the usual rule: get up mid-meal and the tray goes (0.92.4)
        g.ev("player.steer = { x: 1, z: 0, k: 1 }"); g.step(10); g.ev("player.steer = null"); g.step(5); s3b = g.ev(PYO_ST)
        print('  got up mid-meal:', s3b[:3], '|', s3b[6][:60])
        if s3b[0] == 'eat' or s3b[2] or 'leave your tray' not in s3b[6]: fail(f"Pick-your-own: getting up from what you picked kept the tray ({s3b})")
        g.ev("actEnd(true); SHIP.player.tray = null; SHIP.events.joined = SHIP.events.joined.filter(k => !k.startsWith('pick-your-own@'))"); g.ev(f"setShipNow(({d} - 1) * 1440 + 6 * 60 + 25)"); g.step(30)
        j = g.ev(JOIN); picking(); s4a = g.ev(f"[ACT && ACT.kind, !!(ACT && ACT.def.onDone), (() => {{ const m = shipNow() - ({d} - 1) * 1440, e = eventsOn({d}).find(e => e.id === 'pick-your-own'); return m >= e.from && m < e.to; }})()]")
        g.ev("if (ACT) ACT.done = ACT.def.mins - .05"); g.step(60)
        s4 = g.ev(PYO_ST)
        print('  picking again the same day, inside the window:', j, s4a, '| tray', s4[2])
        if not (j and s4a[0] == 'ixGarden' and s4a[2]): fail(f"Pick-your-own: the second pick wasn't inside the tradition ({j}, {s4a})")
        if s4[2]: fail(f"Pick-your-own: a second tray the same day ({s4[:5]})")
        # off Deck 3 with what you picked, the hunger arrow still points at a mess seat (it travels "to the mess"; RV12, 0.92.4)
        g.ev("actEnd(true); clearGoal(); NEED_GOAL = null; SHIP.player.tray = PYO_DISH; SHIP.player.trayGo = true; goToDeck(4)"); g.step(20)
        g.ev("SHIP.player.needs.hunger = 5; needGoal('hunger')"); g.step(4)
        s5 = g.ev("[deckDef.num, SHIP.player.tray, IX_GOAL && IX_GOAL.label, IX_GOAL && IX_GOAL.deck, IX_GOAL && IX_GOAL.place]")
        print('  on Deck 4 with what you picked:', s5)
        if not (s5[0] == 4 and s5[1] and s5[2] == 'A seat for your tray' and s5[3] == 3 and str(s5[4]).startswith('3-mess')): fail(f"Pick-your-own: off Deck 3 the arrow isn't at a mess seat ({s5})")
    if g.errors: fail(f"console: {g.errors[:4]}")
    g.b.close()

# 13. Cook-along in the galley (0.92.5 item 19, the user's: "Cook along tradition should be in the kitchen"): on a Saturday
# while it's on, everyone at it is at a 3-cookalong place in the galley (room K), cooking; none in the mess hall
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1]); g.step(3)
    print('== Cook-along: in the galley')
    ca = g.ev(r"""(() => { goToDeck(3); let d = 2; while (d < 30 && !eventsOn(d).some(e => e.id === 'cook-along')) d++;
      const e = eventsOn(d).find(e => e.id === 'cook-along'); setShipNow((d - 1) * 1440 + e.from + 20); deckCrewFill(); for (let k = 0; k < 120; k++) updateDeckCrew(1 / 30);
      const at = DECK_CREW.filter(a => a.spot && a.spot.id.startsWith('3-cookalong-'));
      // nobody at a galley event spot inside a cook (RV14: Sato at 3-cookalong-3 .18 m from Madsen at 3-galley-6, 15:46): over
      // .45 m from anyone settled at a 3-galley-* place, every 2 ship minutes through Cook-along (and Bread day with the switch on)
      const close = [], gap = (a, b) => Math.hypot(a.x - b.x, a.z - b.z);
      const sweep = (dd, id) => { const x = eventsOn(dd).find(e => e.id === id); if (!x) return; setShipNow((dd - 1) * 1440 + x.from); deckCrewFill();
        const B0 = (dd - 1) * 1440 + x.from, st = .2; for (let k = 0; B0 + k * st * SHIP_RATE < (dd - 1) * 1440 + x.to; k++) { setShipNow(B0 + k * st * SHIP_RATE); updateDeckCrew(st); if (k % Math.max(1, Math.round(2 / (st * SHIP_RATE)))) continue;   // every 2 ship minutes
          const ev = DECK_CREW.filter(a => a.settled && a.spot && a.spot.id.startsWith('3-cookalong-')), ck = DECK_CREW.filter(a => a.settled && a.spot && a.spot.id.startsWith('3-galley-'));
          for (const a of ev) for (const b of ck) if (gap(a, b) < .45 && close.length < 6) close.push(id + ' day ' + dd + ' ' + hhmm(shipNow() % 1440) + ' ' + a.p.id + '@' + a.spot.id + ' / ' + b.p.id + '@' + b.spot.id + ' ' + gap(a, b).toFixed(2)); } };
      sweep(d, 'cook-along'); for (let dd = 7; dd < 30; dd++) if (eventsOn(dd).some(e => e.id === 'bread-day')) { sweep(dd, 'bread-day'); break; }
      return { day: d, at: at.map(a => [a.p.id, a.spot.id, roomAt(...a.here()), a.settled, a.pose]), places: deckDef.places.filter(p => p.id.startsWith('3-cookalong-')).map(p => p.room + ' ' + p.anim), close }; })()""")
    print('  Day', ca['day'], '| at it:', ca['at'], '| its places:', sorted(set(ca['places'])))
    if not ca['at'] or any(x[2] != 'K' for x in ca['at']) or set(ca['places']) != {'K cook'}: fail(f"Cook-along: not in the galley (room K, cooking): {ca}")
    print('  at a galley event spot within .45 m of a cook:', ca['close'] or 'nobody')
    if ca['close']: fail(f"a galley event spot inside a cook's place: {ca['close']}")
    if g.errors: fail(f"console: {g.errors[:4]}")
    g.b.close()

# 14. 0.92.5 (FX12, the user's playtest notes): (4) late piano: never two nights running, the Captain and a few others
# really there; (9) a birthday an hour apart from the day's other traditions; (10) the birthday redone: the birthday
# person at the head of the long table, the cake on it, a ring round them with bubbles (names, not ids; no line twice),
# a tap on the cake: a slice in your hand, eaten as you go, once a party. A page of its own (the ship clock runs here)
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844); g.step(3)
    print('== 0.92.5: late piano, birthdays')
    if g.ev("typeof GUIDE_ON !== 'undefined' && GUIDE_ON"): g.ev("GUIDE.tq.length = 0; guideToast = () => false")
    LP = g.ev("""(() => { const out = []; for (let d = 1; d <= 28; d++) { const e = eventsOn(d).find(e => e.id === 'late-piano'); if (!e) continue;
      const goers = schedPeople().filter(p => planDay(p, d).some(s => evTagId(s.tag) === e.id)).map(p => p.id); out.push([d, weekday(d), goers.length, goers.includes('marrow')]); } return out; })()""")
    print('  late piano (day, weekday, going, the Captain):', LP)
    days = [x[0] for x in LP]
    if not LP or any(b - a == 1 for a, b in zip(days, days[1:])): fail(f"late piano two nights running ({days})")
    if any(x[2] < 4 for x in LP) or sum(1 for x in LP if x[3]) < len(LP) - 1: fail(f"late piano: fewer than 4 going, or the Captain missing more than once ({LP})")
    BD = g.ev("""(() => { const out = []; for (let d = 1; d <= 120; d++) { const l = eventsOn(d), b = l.find(e => e.id === 'birthday'); if (!b) continue;
      out.push([d, b.from, b.to, l.filter(e => e !== b && evIsTrad(e.ev) && !evRare(e.ev.when) && (e.ev.prio || 0) < 2 && !e.ev.meal && e.from < b.to + 60 && b.from - 60 < e.to).map(e => e.id)]); } return out; })()""")   # a weekly one (the rest never give way: their time is taken last)
    print('  birthdays (day, from, to, a weekly tradition within the hour):', BD[:6], '...', len(BD))
    if not BD or any(x[3] for x in BD): fail(f"a birthday within an hour of a weekly tradition: {[x for x in BD if x[3]]}")
    d, fr = BD[0][0], BD[0][1]
    P0 = g.ev(f"""(() => {{ const e = eventsOn({d}).find(e => e.id === 'birthday'), at = id => schedPeople().filter(p => planDay(p, {d}).some(s => evTagId(s.tag) === 'birthday' && s.placeId && s.placeId.startsWith(id)));
      return [e.honorees.map(p => p.id), at('3-bday-head').map(p => p.id), at('3-bday-').length]; }})()""")
    print(f'  Day {d}: birthday for', P0[0], '| at the head', P0[1], '| planned in the ring and the head', P0[2])
    if not (P0[1] and P0[1][0] == P0[0][0] and P0[2] >= 6): fail(f"the birthday: its person not planned at the head, or the ring nearly empty ({P0})")
    g.ev(f"skipTo(({d} - 1) * 1440 + {fr} - 25); goToDeck(3)")
    g.ev("window.__bub = []; const _bs = bubbleSay; bubbleSay = (w, t, s) => { __bub.push(t); return _bs(w, t, s); }")
    for k in range(200):
        g.step(30)
        if g.ev("shipNow() % 1440") > fr + 15: break
    L = g.ev("""[dressingOn(), !!ITEMS.find(i => i.bdayCake), DECK_CREW.filter(a => a.p && a.settled && a.spot && a.spot.id === '3-bday-head').map(a => a.p.id),
      DECK_CREW.filter(a => a.p && a.settled && a.spot && /^3-bday-\\d/.test(a.spot.id)).length, __bub.filter(t => /birthday|Thank|returns|Hip|wish|cake/i.test(t))]""")
    print('  live:', L[:4], '| bubbles', L[4][:6])
    if 'birthdayTable' not in L[0] or not L[1]: fail(f"the birthday: no cake on the table ({L[:2]})")
    if L[2] != P0[0][:1] or L[3] < 4: fail(f"the birthday: its person not in the birthday chair, or fewer than 4 in the ring ({L[2]}, {L[3]})")
    bl = L[4]
    if len(bl) < 3 or len(set(bl)) < len(bl) or any('{' in t or '-' in t.split(',')[-1].strip(' .!').split(' ')[-1] for t in bl): fail(f"the birthday's bubbles: fewer than 3, a line twice, or an id for a name ({bl})")
    g.ev("(() => { const s = placeSpot('3-bday-head') || placeSpot('3-longtable-4'), c = nearestOpen(s.x + 1.5, s.z + 2.5, player); player.obj.position.copy(cellPos(...c)); player.stop(); })()"); g.step(30)
    TAP = "(() => { const it = ITEMS.find(i => i.bdayCake); if (!it) return false; it.hit.getWorldPosition(_wp); return playerTap(it, _wp.clone(), _wp.clone()); })()"
    g.ev(TAP)
    for k in range(60):
        g.step(10)
        if g.ev("!!SLICE"): break
    g.step(10); S1 = g.ev("[!!SLICE, player.holding, document.getElementById('tx').textContent]")
    g.ev("window.__tst = []; const _ts = toast; toast = (t, x, o) => { __tst.push(String(x)); return _ts(t, x, o); }")   # every pop-up after the second tap (FX20b: the birthday's own thanks can land in the same frames and cover it)
    g.ev(TAP); g.step(4)
    S2 = ' | '.join(g.ev("__tst")) or g.ev("document.getElementById('tx').textContent")
    for k in range(200):
        g.step(30)
        if not g.ev("!!SLICE"): break
    S3 = g.ev("[!!SLICE, document.getElementById('tx').textContent]")
    print('  the cake:', S1, '| again:', S2[:50], '| after:', S3)
    if not (S1[0] and S1[1] == 'slice' and 'slice' in S1[2].lower()): fail(f"a tap on the cake: no slice in your hand ({S1})")
    if 'had your slice' not in S2: fail(f"the cake: a second slice the same party ({S2})")
    if S3[0] or 'finish your slice' not in S3[1]: fail(f"the slice wasn't eaten as you go ({S3})")
    if days:
        d = next((x for x in days if x >= BD[0][0]), days[-1])   # on or after the birthday's day: the ship clock only runs forward
        g.ev(f"skipTo(({d} - 1) * 1440 + 21 * 60 + 20); goToDeck(4)")
        for k in range(40):
            g.step(60)
            if g.ev("shipNow() % 1440") >= 1325: break
        live = g.ev("DECK_CREW.filter(a => a.p && a.settled && roomAt(...cellAt(a.x, a.z)) === 'n').map(a => a.p.id)")
        print(f"  Day {d} at 22:05, settled in the music room:", live)
        if len(live) < 3 or 'marrow' not in live: fail(f"late piano, Day {d}: the Captain and at least 2 others not there by 22:05 ({live})")
    if g.errors: fail(f"console: {g.errors[:4]}")
    g.b.close()

# the comet switched off (FX25, 0.93.2): a copy with `const EV_COMET_ON = false;` has no comet at all (no entry, no
# gatherings on Day 22, the calendar's row passed over)
_src = pathlib.Path(sys.argv[1]).read_text()
if re.search(r'^const EV_COMET_ON = true;', _src, re.M):
    _off = WORK / 'test' / f'_comet_off_{os.getpid()}.html'
    _off.write_text(re.sub(r'^const EV_COMET_ON = true;', 'const EV_COMET_ON = false;', _src, count=1, flags=re.M)); _RUN_FILES.append(_off)
    with sync_playwright() as pw:
        g = Game(pw, str(_off))
        X = g.ev("({ has: !!SHIP_EVENTS.comet, day22: eventsOn(22).map(e => e.id).filter(id => /comet/i.test(id)), sw: EV_SHIPWIDE.filter(e => /comet/i.test(e.id)).length, due: evCalPlan().map(r => r.id) })")
        print('The comet switched off:', X)
        if X['has'] or X['day22'] or X['sw'] or 'comet' in X['due']: fail(f"the comet switched off still shows: {X}")
        if g.errors: fail(f"console (comet off): {g.errors[:4]}")
        g.close()

# A Veyli vessel needs help (VB1, V-1; plans/veyli-vessel-spec.html section 6), on paper with the events base on, in a
# copy with EV_VESSEL_ON switched on when the build has it off (its URL-flag line), twice from a clean slate (the
# calendar's earlier events logged): due Saturday Day 27; the phases at their minutes (warning 06:10, onset Sunday 08:00,
# escalation Monday 09:20, resolution Tuesday 09:15, afterglow 09:20, the end at midnight Tuesday); the Captain's two
# addresses (Saturday 08:00, Tuesday 09:15), Vance's Mail Saturday 18:00 and Taavek's letter Tuesday 12:00; Taavek aboard
# only Sunday 09:30 to Monday 15:30 at the latest (the Tern waits for you); the Captain, Calder and Lindqvist called in on their days off (Saturday, Sunday,
# Monday); the commendation rule (C1): none with nothing done, one at Tuesday 09:30 with two of its jobs; no score; and
# with the switch off nothing at all
VESSEL_JS = r"""(() => {
  if (typeof EV_VESSEL_ON === 'undefined' || !EV_VESSEL_ON || !SHIP_EVENTS.veyliVessel) return { off: true, has: !!SHIP_EVENTS.veyliVessel, plan: evCalPlan().map(r => r.id), sw: EV_SHIPWIDE.filter(e => /^vessel/.test(e.id)).length, day28: eventsOn(28).map(e => e.id).filter(id => /^vessel/.test(id)) };
  const run = jobs => {
    const keep = { e: SHIP.event, log: SHIP.eventLog.slice(), tr: SHIP.traces.slice(), m: MEETINGS.splice(0), com: (SHIP.commendations || []).slice(), t: shipNow() };
    SHIP.event = null; SHIP.eventLog.length = 0; SHIP.eventLog.push(...EV_BEFORE('veyliVessel')); EV_DAYS.clear(); SHIP_DAYS.clear();
    const due = eventDueDay(), d = due ? due.day : 27, B = (d - 1) * 1440, tv = schedPeople().find(p => p.id === 'taavek');
    const away = (p, t) => { const w = whereIs(p, t); return w.act === 'away' || !w.deck; };
    const aboardAt = tv ? [[1, 560], [1, 575], [2, 890], [2, 935], [0, 720], [3, 600]].map(([k, m]) => k + ' ' + hhmm(m) + ' ' + (away(tv, B + k * 1440 + m) ? 'away' : 'aboard')) : ['no Taavek'];
    const called = ['marrow', 'calder', 'lindqvist-isak'].map(id => { const q = schedPeople().find(x => x.id === id); return id + ' ' + [0, 1, 2, 3].filter(k => eventCalledIn(q, d + k)).join(','); });
    eventStart('veyliVessel', d); EV_DAYS.clear(); if (jobs) SHIP.event.mine.jobs = jobs;
    const mails = [], send = typeof mailSend === 'function' ? mailSend : null, steps = [], phase = {}, a0 = ADDRESSES.length, status = {};
    if (send) mailSend = m => { if (m.at >= B - 60) mails.push(Math.floor(m.at / 1440) + 1 - d + ' ' + hhmm(m.at % 1440) + ' ' + m.from + ': ' + m.subject); };   // (not a tradition's old Mail sent as the clock jumps)
    for (let t = B - 60; t <= B + 4 * 1440 + 60; t += 5) {
      setShipNow(t); const o = eventAdvance(t, true); vesselTick(t, true); if (o.length) steps.push(Math.floor(t / 1440) + 1 - d + ' ' + hhmm(t % 1440) + ' ' + o.join(', '));
      const n = eventNow(t); if (n && n.id === 'veyliVessel' && !phase[n.phase]) { phase[n.phase] = Math.floor(t / 1440) + 1 - d + ' ' + hhmm(t % 1440); status[n.phase] = eventStatus(t); }
    }
    if (send) mailSend = send;
    const log = SHIP.eventLog.filter(l => l.id === 'veyliVessel').map(l => l.band + ' ' + JSON.stringify(l.threads)), com = (SHIP.commendations || []).filter(c => c.event === 'veyliVessel').map(c => c.day - d);
    const R = { due, aboardAt, called, steps, phase, status, mails, addr: ADDRESSES.slice(a0).map(x => Math.floor(x.at / 1440) + 1 - d + ' ' + hhmm(x.at % 1440)),
      meets: MEETINGS.filter(m => m.event === 'veyliVessel').map(m => m.id + ' ' + (Math.floor(m.at / 1440) + 1 - d) + ' ' + hhmm(m.at % 1440)), log, com, left: SHIP.event && SHIP.event.id,
      late: [vesselLate(27, [], null), vesselLate(28, [], null), vesselLate(28, [{ id: 'veyliVessel' }], null), vesselLate(28, [], { id: 'veyliVessel' })] };
    ADDRESSES.length = a0;
    SHIP.event = keep.e; SHIP.eventLog.length = 0; SHIP.eventLog.push(...keep.log); SHIP.traces.length = 0; SHIP.traces.push(...keep.tr); MEETINGS.length = 0; MEETINGS.push(...keep.m); SHIP.commendations.length = 0; SHIP.commendations.push(...keep.com); EV_DAYS.clear(); SHIP_DAYS.clear(); setShipNow(keep.t);   // the clock back (the live part goes forward from here)
    return R;
  };
  const a = run(0), b = run(0), c = run(2);
  return { a, same: JSON.stringify(a) === JSON.stringify(b), c };
})()"""
_src = pathlib.Path(sys.argv[1]).read_text()
_von = re.search(r"^const EV_VESSEL_ON = true;", _src, re.M)
_vline = re.search(r"^const EV_VESSEL_ON = URL_FLAGS\.has\('evvessel'\);", _src, re.M)
if _von or _vline:
    _vp = sys.argv[1]
    if not _von:
        _vp = str(WORK / 'test' / f'_vessel_on_{os.getpid()}.html'); pathlib.Path(_vp).write_text(_src.replace(_vline.group(0), 'const EV_VESSEL_ON = true;', 1)); _RUN_FILES.append(pathlib.Path(_vp))
    with sync_playwright() as pw:
        g = Game(pw, _vp)
        if True:   # switched off: nothing at all (the build itself, or from 0.94.0, which ships it on, a copy switched off; W6)
            _voff = sys.argv[1]
            if _von: _voff = str(WORK / 'test' / f'_vessel_off_{os.getpid()}.html'); pathlib.Path(_voff).write_text(_src.replace(_von.group(0), 'const EV_VESSEL_ON = false;', 1)); _RUN_FILES.append(pathlib.Path(_voff))
            g2 = Game(pw, _voff); X = g2.ev(VESSEL_JS); g2.close()
            print('The Veyli vessel switched off:', X)
            if not X.get('off') or X['has'] or 'veyliVessel' in X['plan'] or X['sw'] or X['day28']: fail(f"the Veyli vessel switched off still shows: {X}")
        g.ev("window.EV_BEFORE = id => { if (typeof EV_CAL_ON === 'undefined' || !EV_CAL_ON) return []; const r0 = EV_CALENDAR.find(r => r.id === id); return evCalPlan().filter(r => r.id !== id && r0 && r.day < r0.day).map(r => ({ id: r.id, startDay: r.day, endDay: r.day + SHIP_EVENTS[r.id].days, band: 'smooth', threads: {}, mine: {} })); }")
        VS = g.ev(VESSEL_JS); a = VS['a']; c = VS['c']
        print('The Veyli vessel on paper' + (' (a copy switched on)' if not _von else '') + ': due', a['due'], '| the same twice:', VS['same'])
        print('  phases:', a['phase']); print('  status:', a['status']); [print('    ' + x) for x in a['steps']]
        print('  addresses:', a['addr'], '| Mail:', a['mails']); print('  meetings:', a['meets'])
        print('  Taavek:', a['aboardAt'], '| called in (event days):', a['called'])
        print('  result', a['log'], '| commendation (days from the start): none done', a['com'], '| two jobs', c['com'], '| late saves (27, 28, 28 logged, 28 running):', a['late'])
        if not a['due'] or a['due'].get('id') != 'veyliVessel' or a['due'].get('day') != 27: fail(f"the Veyli vessel isn't due on Saturday Day 27: {a['due']}")
        if a['phase'] != {'warning': '0 06:10', 'onset': '1 08:00', 'escalation': '2 09:20', 'resolution': '3 09:15', 'afterglow': '3 09:20'}: fail(f"the Veyli vessel's phases: {a['phase']}")
        if not any(x.startswith('4 00:00') and 'end smooth' in x for x in a['steps']) or (a['left'] and a['left'] != 'crossingBack'): fail(f"the Veyli vessel's end (midnight Tuesday): {a['steps'][-2:]} left {a['left']}")   # (BM19: with the ending on, the crossing back starts as the vessel ends, Day 31 00:00)
        if a['addr'] != ['0 08:00', '3 09:15']: fail(f"the Captain's addresses: {a['addr']}")
        if not any(x.startswith('0 18:00 Commander Teo Vance') for x in a['mails']) or not any(x.startswith('3 12:00 Taavek') for x in a['mails']): fail(f"the Veyli vessel's Mail: {a['mails']}")
        if a['aboardAt'] != ['1 09:20 away', '1 09:35 aboard', '2 14:50 aboard', '2 15:35 away', '0 12:00 away', '3 10:00 away']: fail(f"Taavek aboard only Sunday 09:30 to Monday 15:30 (the Tern waits for you to 15:30; RV21): {a['aboardAt']}")
        if a['called'] != ['marrow 0', 'calder 0,1', 'lindqvist-isak 2']: fail(f"called in: {a['called']}")
        if a['meets'] != ['vesselCall 0 09:00', 'vesselSheet 0 10:00', 'vesselRamp 1 09:30', 'vesselJob 2 09:20', 'vesselHome 2 14:30']: fail(f"the Veyli vessel's meetings: {a['meets']}")
        if a['log'] != ['smooth {}'] or a['com']: fail(f"the Veyli vessel's end with nothing done: {a['log']} commendation {a['com']}")
        if c['com'] != [3] or not any('3 09:30' in x and 'Commendation' in x for x in c['mails']): fail(f"the commendation rule (C1): two jobs, a commendation Tuesday 09:30: {c['com']} {c['mails']}")
        if a['late'] != [False, True, False, False]: fail(f"the late-save rule: {a['late']}")
        if not VS['same']: fail('the Veyli vessel ran differently the second time')
        # V-2 live: Saturday 10:00 Calder's sheet in the Works bay (the arrow at Calder, the scene, the arrow at the sheet,
        # signing, the parts list by Mail); Sunday the ramp three ways: at its foot at 09:30 (vesselRamp), late at 09:50 with
        # Taavek and Calder waiting (vesselRamp.late), and after 10:30 at the Works bay bench, Zeke having met them
        # (vesselRamp.bench); each time Taavek's at the bench afterwards and the Record says you met them
        g.ev("""window.__vmins = n => { for (let k = 0; k < n * 50; k++) window.__step(1, 1000 / 30); };
          window.__vfresh = t => { SHIP.event = null; SHIP.eventLog.length = 0; const v0 = evCalPlan().find(r => r.id === 'veyliVessel'); /* BM19: only the rows before the vessel (the crossing back logged as done made the calendar pass over it) */ for (const r of evCalPlan()) if (r.id !== 'veyliVessel' && (!v0 || r.day < v0.day)) SHIP.eventLog.push({ id: r.id, startDay: r.day, endDay: r.day + SHIP_EVENTS[r.id].days, band: 'smooth', threads: {}, mine: {} });
            MEETINGS.length = 0; EV_DAYS.clear(); SHIP_DAYS.clear(); if (DIALOGUE) dialogueEnd(true); guideList().filter(x => /^vessel:/.test(x.id)).forEach(x => guideDrop(x.id)); skipTo(t); };   // a fresh run: no arrows left from the last
          window.__vplay = () => { const seen = []; for (let k = 0; k < 30 && DIALOGUE; k++) { const v = dialogueView(); if (!v) break; seen.push(v.choices ? '[choice]' : v.id); dialogueStep(v.choices ? 0 : undefined); } return seen; };
          window.__vat = (c, r) => { goToDeck(5); player.obj.position.copy(cellPos(c, r)); target.copy(player.obj.position).setY(.7); }; 'ok'""")
        def vmins(n):
            for _ in range(n): g.step(50)
        g.ev("__vfresh(26 * 1440 + 590); __vat(15, 3)"); vmins(14)
        L = g.ev("({ t: hhmm(shipNow() % 1440), dlg: DIALOGUE && DIALOGUE.id, arrow: guideList().filter(x => x.id === 'vessel:sheet').map(x => x.level + (x.shown ? ' shown' : '')), row: vesselItems(27).map(x => x.title) })")
        L['lines'] = g.ev("__vplay()")
        g.ev("const it = ITEMS.find(i => i.vesselSheet); const p = new THREE.Vector3(); it.hit.getWorldPosition(p); window.__vmail = []; const ms = mailSend; window.__vms = ms; mailSend = m => { __vmail.push(m.from + ': ' + m.subject); ms(m); }; vesselSign(it, p)")
        for _ in range(12):
            vmins(1)
            if g.ev("!!SHIP.event.mine['vessel:signed']"): break
        L.update(g.ev("({ told: SHIP.event.mine['vessel:told'], signed: SHIP.event.mine['vessel:signed'], mail: __vmail.slice(), arrows: guideList().filter(x => /^vessel:/.test(x.id)).map(x => x.id) })")); g.ev("mailSend = __vms")
        print('  V-2 live, the sheet:', L)
        if L['dlg'] != 'vesselSheet' or '[choice]' not in L['lines'] or not L['told'] or not L['signed'] or not any('Calder' in x for x in L['mail']) or L['arrow'] != ['1 shown'] or not L['row']: fail(f"the sheet (Calder's scene, the arrow, signing, the parts list): {L}")
        def vfetch(t0, setup, who, want, mins):   # someone comes to find you in the bow lounge (Deck 3, the seats): their words, then the scene where they stop (RV22: a place 4-5 m off said nothing)
            g.ev(f"__vfresh({t0}); {setup} goToDeck(3); player.obj.position.copy(cellPos(...nearestOpen(cellPos(24, 3).x, cellPos(24, 3).z, player))); target.copy(player.obj.position).setY(.7); window.__vbub = []; window.__vbs = window.__vbs || bubbleSay; bubbleSay = (w, t, sc) => {{ __vbub.push((w && w.p ? w.p.id : '?') + ': ' + t); return __vbs(w, t, sc); }}")
            for _ in range(mins):
                vmins(1)
                if g.ev("!!DIALOGUE"): break
            F = g.ev(f"({{ t: hhmm(shipNow() % 1440), dlg: DIALOGUE && DIALOGUE.id, said: __vbub.filter(x => x.startsWith('{who}:')), ring: IX_GOAL && IX_GOAL.label, far: (() => {{ const a = DECK_CREW.find(a => a.p.id === '{who}'); return a ? +Math.hypot(a.x - player.obj.position.x, a.z - player.obj.position.z).toFixed(1) : null; }})() }})"); F['lines'] = g.ev("__vplay(); bubbleSay = __vbs; 'ok'")
            print(f'  V-2 live, {who} comes to find you in the bow lounge:', F)
            if F['dlg'] != want or not F['said']: fail(f"{who} came to find you but no words or no scene ({want}): {F}")
            return F
        vfetch(26 * 1440 + 686, '', 'calder', 'vesselSheet', 25)   # Saturday 11:30, Calder's second look for you
        for how, t0, at, want in [('on time', 27 * 1440 + 560, (5, 11), 'vesselRamp'), ('find', 27 * 1440 + 584, None, None), ('late', 27 * 1440 + 597, (5, 11), 'vesselRamp.late'), ('Zeke stood in', 27 * 1440 + 640, (16, 3), 'vesselRamp.bench')]:
            if how == 'find':   # C3: at 09:45, not at the ramp (in the mess on Deck 3), Calder comes to find you, in person (the clock only runs forward: between the others)
                g.ev(f"__vfresh({t0}); goToDeck(3); player.obj.position.copy(cellPos(30, 6)); target.copy(player.obj.position).setY(.7)"); vmins(4)
                F = g.ev("({ t: hhmm(shipNow() % 1440), found: SHIP.event.mine['vessel:found'], coming: COME_TO.has('calder'), where: whereIs(schedPeople().find(p => p.id === 'calder'), shipNow()).deck })")
                print('  V-2 live, Calder comes to find you at 09:45:', F)
                if not F['found'] or not F['coming'] or F['where'] != 3: fail(f"Calder didn't come to find you at 09:45: {F}")
                continue
            g.ev(f"__vfresh({t0}); __vat({at[0]}, {at[1]})"); r = None
            arrow = g.ev("(vmin => { __vmins(vmin); return guideList().filter(x => /^vessel:ramp/.test(x.id)).map(x => x.id + (x.shown ? '*' : '')); })(1)")
            for _ in range(16):
                vmins(1)
                arrow += g.ev("guideList().filter(x => /^vessel:ramp/.test(x.id)).map(x => x.id + (x.shown ? '*' : ''))")   # shown at some minute before the scene
                if g.ev("!!DIALOGUE"): break
            r = g.ev("({ t: hhmm(shipNow() % 1440), dlg: DIALOGUE && DIALOGUE.id, ix: IX_GOAL && IX_GOAL.label, covered: GUIDE.covered })"); r['arrow'] = arrow; r['lines'] = g.ev("__vplay()"); vmins(5)
            r.update(g.ev("({ met: SHIP.event.mine['vessel:met'], by: SHIP.event.mine['vessel:metBy'], taavek: (() => { const a = DECK_CREW.find(a => a.p.id === 'taavek'); return a && a.goalId; })(), rec: vesselRecord({ mine: SHIP.event.mine, startDay: 27 }) })"))
            print(f'  V-2 live, the ramp ({how}):', r)
            if r['dlg'] != want or not r['met'] or 'Taavek' not in (r['rec'] or '') or not r['arrow'] or not any(x.endswith('*') for x in r['arrow']): fail(f"the ramp ({how}): {r}")
            if how != 'Zeke stood in' and not str(r['taavek'] or '').startswith(('5-works-bay', '5-vbench')): fail(f"the ramp ({how}): Taavek not on the way to the bench: {r['taavek']}")
        # V-2b live: the round one at the bench after the Zeke run (met at 10:42, at the bench: the scene), Monday's goodbye at
        # the ramp 14:45, the engine lights at the bow glass (17:15 notice, the arrow at Saruth, tapping Saruth joins), and
        # Tuesday the sketch on your shelf; who's planned at the lights
        for _ in range(8):
            vmins(1)
            if g.ev("!!DIALOGUE"): break
        B1 = g.ev("({ t: hhmm(shipNow() % 1440), dlg: DIALOGUE && DIALOGUE.id, arrow: guideList().filter(x => x.id === 'vessel:bench').map(x => x.level + (x.shown ? '*' : '')) })"); B1['lines'] = g.ev("__vplay()")
        B1['done'] = g.ev("SHIP.event.mine['vessel:roundOne']"); print('  V-2b live, the round one:', B1)
        if B1['dlg'] != 'vesselRoundOne' or not B1['done']: fail(f"the round one at the bench: {B1}")
        RF = vfetch(27 * 1440 + 745, "SHIP.event.mine['vessel:met'] = 1; SHIP.event.mine['vessel:metBy'] = 'ramp';", 'taavek', 'vesselRoundOne', 30)   # Sunday 12:30: the round one unseen, Taavek brings it
        if RF['ring'] and 'chain sheet' in RF['ring']: fail(f"the sheet's arrow over the round one's (RV22): {RF}")
        # V-3 live: the parts chain, Sunday 13:00 (the arrow at Zeke from 12:45, tapping Zeke takes a gap, crates through your
        # hands counted, three of them your part toward C1); turnout planned (the spec: 25 or more)
        CH = g.ev("(() => { const d = 28; return { on: eventsOn(d).filter(x => x.id === 'vesselChain').map(x => hhmm(x.from) + '-' + hhmm(x.to)), going: schedPeople().filter(p => planDay(p, d).some(s => s.tag && s.tag.startsWith('ev-vesselChain'))).length, arrival: schedPeople().filter(p => planDay(p, d).some(s => s.tag && s.tag.startsWith('ev-vesselArrival'))).length }; })()")
        g.ev("skipTo(27 * 1440 + 766); __vat(16, 3)"); vmins(15)
        CH.update(g.ev("({ arrow: guideList().filter(x => x.id === 'vessel:chain').map(x => x.level + (x.shown ? '*' : '')) })"))
        CH['tap'] = g.ev("(() => { const a = DECK_CREW.find(a => a.p.id === 'torres-zeke'); return a ? tradJoinTap(a) : 'no zeke'; })()"); vmins(18)
        CH.update(g.ev("({ t: hhmm(shipNow() % 1440), joined: SHIP.events.joined.includes('vesselChain@28'), passed: SHIP.event.mine['vessel:chainN'], part: SHIP.event.mine['vessel:chain'], ring: guideList().filter(x => x.id === 'vessel:crate').map(x => x.level + (x.shown ? '*' : '')) })"))
        print('  V-3 live, the parts chain:', CH)
        if not 12 <= CH['arrival'] <= 30: fail(f"about twenty watching Taavek arrive (RV21): {CH['arrival']}")
        if CH['on'] != ['13:00-14:00'] or CH['going'] < 25 or not CH['arrow'] or CH['tap'] is not True or not CH['joined'] or (CH['passed'] or 0) < 3 or not CH['part'] or not CH['ring']: fail(f"the parts chain: {CH}")
        # V-4 live: Monday 09:15 in the Works bay: the arrow at Calder, Calder's word (vesselJob), the helper card twice (Kovac,
        # then Zeke), then the five steps in the machine shop (the stock card: a wrong pick first, ten minutes lost), the
        # lathe's wait, the part yours; the test fit at 13:30 with the helpers' reactions
        g.ev("skipTo(28 * 1440 + 555); __vat(16, 3)")
        for _ in range(10):
            vmins(1)
            if g.ev("!!DIALOGUE"): break
        MK = g.ev("({ t: hhmm(shipNow() % 1440), dlg: DIALOGUE && DIALOGUE.id, arrow: guideList().filter(x => x.id === 'vessel:job').map(x => x.level + (x.shown ? '*' : '')), row: vesselItems(29).map(x => x.title) })"); MK['lines'] = g.ev("__vplay()")
        g.step(30)   # the card comes once the scene's panel has closed (a moment: simTimeout)
        MK['card1'] = g.ev("DEV.choose ? (devChosen(0), SHIP.event.mine['vessel:helpers']) : 'no card'"); g.step(30)
        MK['card2'] = g.ev("DEV.choose ? (devChosen(vesselHelperIds(29).filter(id => id !== 'kovac-zainab').indexOf('torres-zeke')), SHIP.event.mine['vessel:helpers']) : 'no card'")
        g.ev("goToDeck(5); player.obj.position.copy(cellPos(24, 10)); target.copy(player.obj.position).setY(.7)")
        seen = []
        for _ in range(90):
            vmins(1)
            st = g.ev("({ s: SHIP.event.mine['vessel:step'] | 0, part: SHIP.event.mine['vessel:part'] || null, act: ACT && ACT.kind, card: !!DEV.choose, t: hhmm(shipNow() % 1440) })")
            if st['card']:   # the stock card: a wrong pick first (if it's not the right one already), then the right one
                k = g.ev("(() => { const L = Array.from(document.querySelectorAll('#devDlg button')).map(b => b.textContent).filter(x => x !== '×'); const right = vesselW('stock.1', 'The bronze bar, the one that sings'); const i = L.indexOf(right); window.__vright = i; return L; })()")
                ri = g.ev("window.__vright")
                if 'wrong' not in seen: g.ev(f"devChosen({(ri + 1) % 3})"); seen.append('wrong')
                else: g.ev(f"devChosen({ri})"); seen.append('right')
            if not seen or seen[-1] != f"step {st['s']}": seen.append(f"step {st['s']}")
            if st['part']: break
            # walk to the step's place when it isn't where you are
            g.ev("(() => { const x = VESSEL_STEPS[SHIP.event.mine['vessel:step'] | 0]; if (!x || (ACT && ACT.kind === 'vesselStep')) return; const sp = placeSpot(x.at); if (Math.hypot(sp.x - player.obj.position.x, sp.z - player.obj.position.z) > 1.5) playerGo(sp.walk); })()")
        MK.update(g.ev("({ t: hhmm(shipNow() % 1440), part: SHIP.event.mine['vessel:part'], helpers: SHIP.event.mine['vessel:helpers'], jobs: SHIP.event.mine.jobs })")); MK['seen'] = seen
        print('  V-4 live, making the round one:', MK)
        if MK['dlg'] != 'vesselJob' or not MK['arrow'] or MK['card2'] != ['kovac-zainab', 'torres-zeke'] or MK['part'] != 'you' or 'wrong' not in seen or 'step 5' not in seen: fail(f"making the round one: {MK}")
        g.ev("skipTo(28 * 1440 + 812); goToDeck(5); player.obj.position.copy(cellPos(23, 10)); target.copy(player.obj.position).setY(.7)")
        for _ in range(12):
            vmins(1)
            if g.ev("!!DIALOGUE"): break
        TF = g.ev("({ t: hhmm(shipNow() % 1440), dlg: DIALOGUE && DIALOGUE.id, arrow: guideList().filter(x => x.id === 'vessel:testfit').map(x => x.level + (x.shown ? '*' : '')) })"); TF['lines'] = g.ev("__vplay()"); TF['done'] = g.ev("SHIP.event.mine['vessel:testfit']")
        print('  V-4 live, the test fit:', TF)
        if TF['dlg'] != 'vesselTestFit' or not TF['done']: fail(f"the test fit: {TF}")
        g.ev("skipTo(28 * 1440 + 875); __vat(5, 11)")
        for _ in range(12):
            vmins(1)
            if g.ev("!!DIALOGUE"): break
        H = g.ev("({ t: hhmm(shipNow() % 1440), dlg: DIALOGUE && DIALOGUE.id, arrow: guideList().filter(x => x.id === 'vessel:home').map(x => x.level + (x.shown ? '*' : '')), row: vesselItems(29).map(x => x.title) })"); H['lines'] = g.ev("__vplay()")
        H.update(g.ev("({ home: SHIP.event.mine['vessel:home'], sketch: SHIP.event.mine['vessel:sketch'] })")); print('  V-2b live, Taavek goes home:', H)
        if H['dlg'] != 'vesselHome' or H['home'] != 1 or H['sketch'] != 'you': fail(f"seeing Taavek off: {H}")
        LG = g.ev("(() => { const d = 29, e = eventsOn(d).find(x => x.id === 'vesselLights'); return { on: e ? hhmm(e.from) + '-' + hhmm(e.to) : null, going: schedPeople().filter(p => planDay(p, d).some(s => s.tag && s.tag.startsWith('ev-vesselLights'))).length, saruth: planDay(schedPeople().find(p => p.id === 'saruth'), d).some(s => s.tag && s.tag.startsWith('ev-vesselLights')) }; })()")
        g.ev("skipTo(28 * 1440 + 1032); goToDeck(3); player.obj.position.copy(cellPos(44, 10)); target.copy(player.obj.position).setY(.7)"); vmins(12)
        LG.update(g.ev("({ t: hhmm(shipNow() % 1440), arrow: guideList().filter(x => x.id === 'vessel:lights').map(x => x.level + (x.shown ? '*' : '')), sar: !!DECK_CREW.find(a => a.p.id === 'saruth') })"))
        vmins(9); LG['tap'] = g.ev("(() => { const a = DECK_CREW.find(a => a.p.id === 'saruth'); return a ? tradJoinTap(a) : 'no saruth'; })()"); vmins(12)
        LG.update(g.ev("({ glass: SHIP.event.mine['vessel:glass'], you: SHIP.event.mine['vessel:lightsYou'], joined: SHIP.events.joined.includes('vesselLights@29') })")); print('  V-2b live, the engine lights:', LG)
        if LG['on'] != '17:30-18:00' or LG['going'] < 25 or not LG['saruth'] or not LG['arrow'] or not LG['joined'] or not LG['glass']: fail(f"the engine lights: {LG}")
        g.ev("skipTo(29 * 1440 + 725); goToDeck(4); const b = placeSpot(playerBed()); player.obj.position.set(b.x + .3, 0, b.z + .3); target.copy(player.obj.position).setY(.7)"); vmins(3)
        S = g.ev("({ shelved: SHIP.event && SHIP.event.mine['vessel:shelved'], trace: traceOn('vesselSketchShelf'), rec: vesselRecord({ mine: SHIP.event ? SHIP.event.mine : {}, startDay: 27 }) })"); print('  V-2b live, the sketch on your shelf:', S)
        if not S['shelved'] or not S['trace']: fail(f"the sketch on your shelf: {S}")
        if g.errors: fail(f"console (vessel): {g.errors[:4]}")
        g.close()

print('EVENTS CHECK OK' if ok else 'EVENTS CHECK FAILED')
sys.exit(0 if ok else 1)
