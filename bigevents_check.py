# Starship Cadet: the big events check (keep in the repo, next to events_check.py). Not in check_fast (lead 21's call).
# The ship-wide events (section 18, SHIP_EVENTS) by the events base (plans/events-base-brief.md, F7), driven by the
# game's own data (SHIP_EVENTS, EV_CALENDAR, EV_BEATS, EV_SHIPWIDE), so a new event is checked as soon as it's in the
# calendar. One file from EC1's and EV1's two (lead 21, 2026-10-21); EC1 owns it.
#   the switches: the check builds copies of the game with EVENTS_ON (and EV_CAL_ON alone) switched on by text, the way
#   day_check flips REC_TRAD_ON, and runs each part on the copy it needs;
#   1. off = today's game: eventDay never true, guardFree always true, no beat moved by the hold, the party's k 340,
#   no hash key shared;
#   2-3. on paper (one page each, no frames stepped): the calendar's days (storm Day 11, due, played forward one at a
#   time; main events never overlap); each phase begins at its minute, in order (eventNow minute by minute); every beat
#   (phase, meeting, news, felt moment, job, gathering) at its time, none starting in a Friday hold (Fridays from Day 5,
#   15:30-17:00; a beat put there waits to 17:00); eventDay on the front, escalation and all-clear days only, unchanged
#   by the saved or live state; the career-beat guard (EV_BEATS, guardFree): every meeting and gathering clear of the
#   beats' hours (its own beat aside), one Captain's scene a day, none on a test day or across a night shift; the
#   summons on Day 18 at 16:00 and the Captain's table on Day 20 19:00-20:15 (a night-shift week); the meetings' casts on
#   shift or called in (eventCalledIn), and planned in the meeting's room; gatherings fit their places (crowds about
#   60, the mess's 44 seats plus standing); no tradition in a gathering's or meeting's room while it's on, and the
#   plan's clashes (talent night and Lap of the Wren off the party night, the lap on Day 15 at 20:30); the run twice
#   is identical;
#   4. a self-test: clashes planted in a copy (a meeting in the Friday hold, one over the officer's ceremony, a
#   gathering in the hold) must each be caught;
#   5. late saves (in the browser, real saves): a Day 20 save passes over the storm for good, decided once at load;
#   and in parts 1-3, the phase notes (F2): the clock run through the storm's warning and front, each phase's note once at
#   its minute, its cue, a crew reaction line for the front; none while EV_NOTES_ON is off; and the device (F3a): the
#   Schedule's event items at the meetings' and gatherings' minutes, Tracked's booths only while open, eventClosed
#   (the auditorium opened just for the Friday address); nothing while EV_DEVICE_ON is off.
# Each part skips (SKIP, or WAITING with what it waits for) while its switch or code isn't there yet, so it runs on
# today's integration and grows as the events base is built. Exits 1 on a FAIL. About 2 minutes.
# Setup and environment as for cadet_test.py (three.js in $CADET_WORK/three, CADET_CHROME a Chromium).
# Run:  python3 bigevents_check.py BUILD.html
import sys, re, json, pathlib, os
exec(open(__file__.replace('bigevents_check.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright

SRC = pathlib.Path(sys.argv[1]).read_text()
CROWD = 66                     # crowds up to about 60 (the user, events plan v3.2 answer 4): a tenth over is a FAIL
MESS_SEATS = 44

ok = True
SINK = None                    # the self-test collects the FAILs here instead of printing them
def fail(msg):
    global ok
    if SINK is not None: SINK.append(msg); return
    ok = False
    print('  FAIL', msg)
def note(msg):
    if SINK is None: print('  note:', msg)
def waiting(msg):
    if SINK is None: print('  WAITING:', msg)
def say(msg):
    if SINK is None: print(msg)
def hhmm_py(m): m = int(m); return f'{m // 60 % 24:02d}:{m % 60:02d}'

def variant(tag, on):
    # a copy of the game with these switches on: 'all' flips EVENTS_ON; else each piece's line alone
    src = SRC
    if on == 'all': src = src.replace('const EVENTS_ON = false;', 'const EVENTS_ON = true;', 1)
    else:
        for s in on: src = re.sub(r'const ' + s + r' = EVENTS_ON;', 'const ' + s + ' = true;', src, count=1)
    p = WORK / 'test' / f'bigev_{tag}.html'; p.write_text(src); return str(p)

# the events on paper: everything from the data and pure functions, nothing stepped. The saved and live state
# (SHIP.event, SHIP.eventLog, the clock) is set aside first (a new game: nothing running, nothing logged) and put back
PAPER = r"""(() => {
  const keep = { e: SHIP.event, log: SHIP.eventLog.slice(), time: { ...SHIP.time } }; SHIP.event = null; SHIP.eventLog.length = 0;
  const has = n => { try { return typeof eval(n) !== 'undefined'; } catch (e) { return false; } };
  const ab = (d, m) => (d - 1) * 1440 + m, dm = t => { const d = Math.floor(t / 1440) + 1; return 'D' + d + ' ' + WEEKDAYS[weekday(d)].slice(0, 3) + ' ' + hhmm(t - (d - 1) * 1440); };
  const out = { sw: {}, cal: [], beats: [], gath: [], held: [], synth: null, due: null, chain: [], scan: {}, eventDay: [], called: [], calledStray: [], caps: [], clash: [], named: {}, captains: {}, guard: null, occ: null };
  for (const s of ['EVENTS_ON', 'EV_CAL_ON', 'EV_GUARD_ON', 'EV_NOTES_ON', 'EV_DEVICE_ON', 'EV_REPLAY_ON', 'EV_RANK_ON', 'EV_COMMS_ON']) out.sw[s] = has(s) ? eval(s) : null;
  const CAL = has('EV_CALENDAR') ? EV_CALENDAR : [], built = r => !!SHIP_EVENTS[r.id] && !SHIP_EVENTS[r.id].draft;
  const beatAt = has('evBeatAt') ? evBeatAt : (sd, at) => ab(sd + at[0], at[1]), heldAt = has('evHeld') ? evHeld : () => false;
  out.cal = CAL.map(r => ({ id: r.id, day: r.day, kind: r.kind, days: SHIP_EVENTS[r.id] ? SHIP_EVENTS[r.id].days : null, built: !!SHIP_EVENTS[r.id], draft: !!(SHIP_EVENTS[r.id] && SHIP_EVENTS[r.id].draft), skipped: has('EV_SKIPPED') && EV_SKIPPED.has(r.id) }));
  out.skipped = has('EV_SKIPPED') ? [...EV_SKIPPED] : null;
  // the Friday hold, every 5 minutes of five weeks' afternoons, and test beats put in it
  for (let d = 1; d <= 35; d++) for (let m = 840; m < 1140; m += 5) if (heldAt(ab(d, m))) out.held.push([d, m]);
  if (has('evBeatAt')) out.synth = [[5, 945], [12, 930], [12, 1019], [12, 1020], [12, 925], [11, 945], [4, 960]].map(([d, m]) => [d, m, evBeatAt(d, [0, m]) - ab(d, 0)]);
  // the beats of each event on the calendar (drafts too, marked: they're switched on later)
  for (const r of CAL) {
    const def = SHIP_EVENTS[r.id]; if (!def) continue;
    const sd = r.day, list = [];
    for (const p of def.phases) list.push(['phase', p.id, p.at]);
    for (const m of def.meetings || []) list.push(['meeting', m.id, m.at, m.len || 15, m.who, m.where, m.beat]);
    for (const n of def.news || []) list.push(['news', n.id, n.at]);
    for (const mo of def.moments || []) if (!mo.gathering) list.push(['moment', mo.id, mo.at, mo.len]);
    for (const [ph, js] of Object.entries(def.jobs || {})) { const p = def.phases.find(x => x.id === ph); if (p) for (const j of js) list.push(['job', j.id, [p.at[0], j.at]]); }
    for (const b of list) {
      const raw = ab(sd + b[2][0], b[2][1]), t = beatAt(sd, b[2]);
      out.beats.push({ ev: r.id, draft: !built(r), what: b[0], id: b[1], raw, t, at: dm(t), rawHeld: heldAt(raw), held: heldAt(t), len: b[3] || 0, who: b[4] || null, beat: b[6] || null,
        deck: b[5] ? b[5].deck : null, room: b[5] && b[5].room ? b[5].room.source.replace(/^\^|\$$/g, '').replace(/\\/g, '').toLowerCase() : null, day: Math.floor(t / 1440) + 1 });
    }
    // eventNow minute by minute through the event, as a new game sees it (built, not passed over)
    if (built(r) && !(has('EV_SKIPPED') && EV_SKIPPED.has(r.id))) {
      const sc = []; let last = null;
      for (let t = ab(r.day, 0); t < ab(r.day + def.days, 0); t++) { const n = eventNow(t), k = n ? n.id + ':' + n.phase : '-'; if (k !== last) { sc.push([k, t]); last = k; } }
      out.scan[r.id] = { seen: sc, want: def.phases.map(p => [r.id + ':' + p.id, beatAt(sd, p.at)]) };
    }
  }
  // the gatherings made at load (EV_SHIPWIDE): their day and hours (not moved by the hold)
  for (const g of (typeof EV_SHIPWIDE !== 'undefined' ? EV_SHIPWIDE : [])) {
    const r = CAL.find(x => x.id === g.when.ship), sd = r ? r.day : null, d = sd != null ? sd + g.when.day : null;
    out.gath.push({ id: g.id, ev: g.when.ship, k: g.k, day: d, at: g.at, held: d != null && (heldAt(ab(d, g.at[0])) || heldAt(ab(d, g.at[1] - 1))), rooms: [...new Set(evRooms(g))], draft: !r || !built(r) });
  }
  // the due day, and the calendar played forward on paper (each event logged as run)
  const dueOf = () => { const x = eventDueDay(); return x ? { id: x.id, day: x.day } : null; };
  out.due = dueOf();
  for (let k = 0, x = out.due; x && k < 8; k++, x = dueOf()) { const def = SHIP_EVENTS[x.id]; out.chain.push({ id: x.id, day: x.day, end: x.day + def.days }); SHIP.eventLog.push({ id: x.id, startDay: x.day, endDay: x.day + def.days, band: 'bumpy', threads: {}, mine: {} }); }
  SHIP.eventLog.length = 0;
  // eventDay: the big days, and the same whatever the saved or live state says
  const eday = () => has('eventDay') ? [...Array(61).keys()].filter(d => eventDay(d)) : null;
  out.eventDay = eday();
  out.bigDays = CAL.filter(r => built(r) && !(has('EV_SKIPPED') && EV_SKIPPED.has(r.id))).flatMap(r => SHIP_EVENTS[r.id].phases.filter(p => ['onset', 'escalation', 'resolution'].includes(p.id)).map(p => r.day + p.at[0])).filter((d, i, a) => a.indexOf(d) === i).sort((x, y) => x - y);
  SHIP.event = { id: 'ionStorm', startDay: 3, phase: 'onset', threads: {}, mine: {} }; SHIP.eventLog.push({ id: 'ionStorm', startDay: 2, endDay: 8, band: 'rough', threads: {}, mine: {} }); SHIP.time.day = 25;
  out.eventDayLive = eday(); out.skippedLive = has('EV_SKIPPED') ? [...EV_SKIPPED] : null;
  out.beatsLive = out.beats.map(b => { const sd = CAL.find(r => r.id === b.ev).day; return beatAt(sd, [Math.floor(b.raw / 1440) + 1 - sd, b.raw % 1440]); });
  out.guardLive = has('guardFree') ? [guardFree(15, 600, 625, 'captain'), guardFree(20, 1170, 1260, 'captain')] : null;
  SHIP.event = null; SHIP.eventLog.length = 0; SHIP.time.day = keep.time.day; SHIP.time.min = keep.time.min;
  out.guardNew = has('guardFree') ? [guardFree(15, 600, 625, 'captain'), guardFree(20, 1170, 1260, 'captain')] : null;
  // the meetings' casts (F0b): on shift, or called in on a day off; planned in the meeting's room at its start
  const people = schedPeople(), pById = id => people.find(p => p.id === id), S = schedData();
  for (const b of out.beats.filter(b => b.what === 'meeting' && !b.draft && Array.isArray(b.who))) for (const id of b.who) {
    if (typeof id !== 'string' || /:/.test(id)) { out.called.push({ meet: b.id, day: b.day, at: b.at, id: String(id), slot: true }); continue; }   // a cast slot ('works:2') is filled from who's there (F7b checks it live)
    const p = pById(id); if (!p) { out.called.push({ meet: b.id, day: b.day, at: b.at, id, aboard: false }); continue; }
    const off = !isWorkDay(p, b.day), c = has('eventCalledIn') ? !!eventCalledIn(p, b.day) : null;
    const seg = planDay(p, b.day).find(s => s.from <= b.t && b.t < s.to);
    const pl = seg && seg.placeId && S.byId.get(seg.placeId), rm = pl && DECKS[pl.deck] && DECKS[pl.deck].rooms && DECKS[pl.deck].rooms[pl.room];
    const there = !!seg && seg.deck === b.deck && !!rm && (!b.room || (rm.name || '').toLowerCase() === b.room);
    out.called.push({ meet: b.id, day: b.day, at: b.at, id, aboard: true, off, called: c, deck: seg ? seg.deck : null, act: seg ? seg.act : null, place: seg ? seg.placeId || null : null, roomName: rm ? rm.name : null, want: b.deck, wantRoom: b.room, there });
  }
  if (has('eventCalledIn')) for (const d of [...new Set(out.beats.filter(b => !b.draft).map(b => b.day))])
    for (const p of people) if (eventCalledIn(p, d) && !out.called.some(c => c.day === d && c.id === p.id)) out.calledStray.push(d + ' ' + p.id);
  // the gatherings on their day: who means to go, who's planned there, and how many places
  for (const g of out.gath.filter(g => !g.draft && g.day)) {
    const e = eventsOn(g.day).find(x => x.id === g.id); if (!e) { out.caps.push({ id: g.id, day: g.day, missing: true }); continue; }
    const want = people.filter(p => eventPlan(p, g.day).some(x => x.id === g.id)).length;
    const went = people.filter(p => planDay(p, g.day).some(s => s.tag && (s.tag === 'ev-' + g.id || s.tag.startsWith('ev-' + g.id + '-')))).length;
    const pls = e.ev.where.flatMap((w, i) => S.shared.get(w.deck + '|' + (w.room ? 'ev:' + e.id + ':' + i : w.pool)) || []);
    const cap = new Set(pls.map(pl => pl.id)).size, seats = new Set(pls.filter(pl => /seat|chair|bench|stool|sofa/.test(pl.type)).map(pl => pl.id)).size;
    out.caps.push({ id: g.id, day: g.day, at: hhmm(e.from) + '-' + hhmm(e.to), want, went, cap, seats, rooms: g.rooms, mess: g.rooms.some(r => /mess/.test(r)) });
  }
  // traditions in a gathering's or meeting's room while it's on; and the traditions on the events' days, for the plan's list
  const span = []; for (const r of CAL.filter(built)) for (let d = r.day; d <= r.day + SHIP_EVENTS[r.id].days; d++) span.push(d);
  for (const d of [...new Set(span)]) out.named[d] = eventsOn(d).filter(e => SHIP_TRADITIONS.includes(e.ev)).map(e => [e.id, e.from, e.to]);
  const things = out.gath.filter(g => !g.draft && g.day).map(g => ({ id: g.id, day: g.day, from: g.at[0], to: g.at[1], rooms: g.rooms }))
    .concat(out.beats.filter(b => b.what === 'meeting' && !b.draft && b.room).map(b => ({ id: b.id, day: b.day, from: b.t - ab(b.day, 0), to: b.t - ab(b.day, 0) + b.len, rooms: [b.deck + '|' + b.room] })));
  for (const x of things) for (const e of eventsOn(x.day).filter(e => SHIP_TRADITIONS.includes(e.ev))) {
    const rooms = evRooms(e.ev); if (e.from < x.to && x.from < e.to && rooms.some(r => x.rooms.includes(r))) out.clash.push('D' + x.day + ' ' + e.id + ' ' + hhmm(e.from) + '-' + hhmm(e.to) + ' in ' + rooms.join(',') + ' during ' + x.id + ' ' + hhmm(x.from) + '-' + hhmm(x.to));
  }
  // the Captain's scenes in the events' meetings, a day at a time
  for (const b of out.beats.filter(b => b.what === 'meeting' && !b.draft && Array.isArray(b.who) && b.who.includes('marrow'))) (out.captains[b.day] = out.captains[b.day] || []).push(b.id + ' ' + b.at);
  // the career-beat guard (F1b): every meeting and gathering against the beats (its own beat aside: one named in
  // m.beat, or a Captain's beat that day starting within 15 minutes of it); its rows' rules; probes at the plan's hours
  if (has('guardFree') && has('evBeatsOn')) {
    const G = { items: [], captainDays: {}, testDays: EV_BEATS.filter(b => b.kind === 'test').map(b => b.day) };
    for (const b of out.beats.filter(b => b.what === 'meeting' && !b.draft)) {
      const from = b.t - ab(b.day, 0), own = evBeatsOn(b.day).filter(x => from < x.to && from + b.len > x.from && x.id !== b.beat);
      G.items.push({ what: b.ev + ' meeting ' + b.id, when: b.at, ok: guardFree(b.day, from, from + b.len, 'beat') || own.every(x => x.kind === 'captain' && Math.abs(x.from - from) <= 15), beats: own.map(x => x.id) });
    }
    for (const g of out.gath.filter(g => !g.draft && g.day)) G.items.push({ what: 'gathering ' + g.id, when: dm(ab(g.day, g.at[0])), ok: guardFree(g.day, g.at[0], g.at[1], 'beat'), beats: evBeatsOn(g.day).filter(x => g.at[0] < x.to && g.at[1] > x.from).map(x => x.id) });
    for (const b of EV_BEATS) if (b.kind === 'captain') G.captainDays[b.day] = (G.captainDays[b.day] || 0) + 1;
    // test day; Day 18 16:00 free; the table at 19:30 on Day 20 crosses the night shift, at 19:00 it doesn't; Day 21 05:00 is the night shift; Friday 16:00
    G.samples = [guardFree(15, 600, 625, 'captain'), guardFree(18, 960, 985, 'captain'), guardFree(20, 1170, 1260, 'captain'), guardFree(20, 1140, 1215, 'captain'), guardFree(21, 300, 330, 'beat'), guardFree(12, 960, 990, 'beat')];
    out.guard = G;
  }
  // the occasions the guard places (F1c): the summons' hour on Day 18, the Captain's table on Day 20
  if (typeof OCCASIONS !== 'undefined') {
    const R = OCCASIONS.readyRoom, T = OCCASIONS.captainsTable;
    out.occ = { ready18: R && R.slot ? R.slot(18) : null, table20: T && T.slot ? T.slot(20) : null, table48: T && T.slot ? T.slot(48) : null, today: T ? [T.at, T.len] : null,
      early: has('EV_TABLE_EARLY') ? EV_TABLE_EARLY : null, night20: has('EV_BEATS') && EV_BEATS.some(b => b.kind === 'night' && b.day === 20) };
  }
  out.stormNew = !!(SHIP_EVENTS.ionStorm && (SHIP_EVENTS.ionStorm.meetings || []).some(m => m.id === 'stormBriefing' && m.at[1] === 840));
  SHIP.event = keep.e; SHIP.eventLog.length = 0; SHIP.eventLog.push(...keep.log); Object.assign(SHIP.time, keep.time);
  return out;
})()"""

# the self-test's clashes, planted in a copy: a storm meeting in the Friday hold (Day 12 15:45), one over the
# officer's ceremony (Day 11 17:20), and a gathering in the hold (Day 12 16:00)
PLANT = r"""(() => {
  const M = SHIP_EVENTS.ionStorm.meetings;
  M.push({ id: 'plantHold', at: [1, 945], len: 10, where: { venue: 'bow-lounge', deck: 3, room: /^Bow lounge$/ }, who: [] });
  M.push({ id: 'plantGuard', at: [0, 1040], len: 20, where: { venue: 'works-bay', deck: 5, room: /^Works bay$/ }, who: [] });
  const p = EV_SHIPWIDE.find(g => g.id === 'party'); EV_SHIPWIDE.push({ ...p, id: 'plantGath', k: 9999, when: { ship: 'ionStorm', day: 1 }, at: [960, 1000] });
  return true;
})()"""
PLANTED = ['plantHold', 'plantGuard', 'plantGath']

# F2, the phase notes, live on paper (EV1's part, made from the data): the clock run every 5 ship minutes from 05:00 on
# the first built event's calendar day to 15:00 the next (the storm's warning and front) through eventAdvance(t, quiet)
# and section 20's socialTick; each phase's note once, at its own minute (evBeatAt); the cue event.<id>.<phase> made
# (cues last a ship day: read at 12:00 on the first day and at the end); someone's reaction line for the last phase
# (section 22's lineFor, kind 'cue'). Switched off (EV_NOTES_ON): no note at all
NOTES = r"""((a, b) => {
  const out = { notes: [], cues: [], lines: 0, want: [], err: null, on: typeof EV_NOTES_ON !== 'undefined' ? EV_NOTES_ON : null };
  try {
    const r = typeof EV_CALENDAR !== 'undefined' && EV_CAL_ON ? EV_CALENDAR.find(x => SHIP_EVENTS[x.id] && !SHIP_EVENTS[x.id].draft) : null;
    if (r) out.want = SHIP_EVENTS[r.id].phases.map(p => [r.id, p.id, evBeatAt(r.day, p.at)]).filter(x => x[2] >= a && x[2] <= b).map(x => x[0] + ':' + x[1] + '@' + x[2]);
    for (let t = a; t <= b; t += 5) { setShipNow(t); eventAdvance(t, true); if (typeof socialTick === 'function') socialTick();
      if (t === a + 420 || t === b) out.cues.push(...((SHIP.social && SHIP.social.cues) || []).map(c => c.key).filter(k => /^event\./.test(k))); }
    out.notes = simNotes('eventPhase').map(n => n.id + ':' + n.phase + '@' + n.t);
    const last = out.want[out.want.length - 1], cue = last && 'event.' + last.split('@')[0].replace(':', '.');
    out.cue = cue || null;
    if (cue && typeof lineFor === 'function') for (const p of schedPeople()) { const l = lineFor(p, 'cue', { t: shipNow(), keep: () => true }); if (l && [].concat(l.cue || []).some(c => c.startsWith(cue))) out.lines++; }
  } catch (e) { out.err = String(e && e.stack || e).slice(0, 300); }
  out.cues = [...new Set(out.cues)].sort();
  return out;
})"""

# F3a, on your device (in the same page, after the paper part; the clock put back after): for each day of the first
# built event, the Schedule (devDay) holds an 'event' item at each of eventGatherings' minutes, with a goal
# (devItemGoal) to walk to; Tracked (trkItems) offers the call booths exactly while the event hasn't closed them
# ('closed' routines at that minute: Day 12 10:00 yes, 15:00 no, Day 14 12:00 yes); eventClosed: the bow lounge on Day 12
# 15:00 and not Day 11; with a test rule closing Deck 7 in the onset, the auditorium is shut at 15:00, open 16:10 (the
# Friday address, EV_OPEN_FOR) and shut at 17:10, the common room shut at 16:10. Off (EV_DEVICE_ON): no items, nothing closed
DEVICE = r"""(() => {
  const keep = { ...SHIP.time }, out = { on: typeof EV_DEVICE_ON !== 'undefined' ? EV_DEVICE_ON : null, days: [], trk: [], closed: [], open7: null, off: null, err: null };
  const ab = (d, m) => (d - 1) * 1440 + m;
  try {
    const r = typeof EV_CALENDAR !== 'undefined' && EV_CAL_ON ? EV_CALENDAR.find(x => SHIP_EVENTS[x.id] && !SHIP_EVENTS[x.id].draft) : null;
    const sd = r ? r.day : (eventDueDay() || {}).day;
    out.off = { items: [sd, sd + 1, sd + 2, sd + 3].map(d => eventItems(ab(d, 0), ab(d, 1439)).length), lounge: eventClosed({ deck: 3, room: 'L' }, ab(sd + 1, 900)) };
    if (!out.on) return out;
    for (let d = sd; d < sd + SHIP_EVENTS[r.id].days; d++) {
      const want = eventGatherings(d).map(g => g.at).sort((x, y) => x - y), items = devDay(d).filter(x => x.kind === 'event');
      out.days.push({ d, want, got: items.map(x => x.from).sort((x, y) => x - y), goals: items.filter(x => { const g = devItemGoal(x); return !(g && Number.isInteger(g.deck) && g.room); }).map(x => x.title + ' ' + hhmm(x.from)) });
    }
    const calls = TRK_PLACES.find(q => q.key === 'place:calls');
    for (const [d, m] of [[sd + 1, 600], [sd + 1, 900], [sd + 2, 720], [sd + 3, 720], [sd + 4, 720]]) {
      setShipNow(ab(d, m)); const shut = eventRoutines(ab(d, m)).some(x => x.rule === 'closed' && (x.where === 'type:callhome' || x.where === '3|B'));
      out.trk.push({ d, m, shut, offered: trkItems().some(x => x.key === 'place:calls'), closed: calls ? eventClosed(calls.goal(), ab(d, m)) : null });
    }
    out.closed = [[sd + 1, 900], [sd, 900], [sd + 3, 1200]].map(([d, m]) => [d, m, eventClosed({ deck: 3, room: 'L' }, ab(d, m))]);
    const R = SHIP_EVENTS[r.id].routines, ph = R && R.onset; if (ph) { ph.push({ where: 'deck:7', rule: 'closed' });
      out.open7 = [[7, 'A', 900], [7, 'A', 970], [7, 'A', 1030], [7, 'C', 970]].map(([dk, rm, m]) => [dk + rm, m, eventClosed({ deck: dk, room: rm }, ab(sd + 1, m))]); ph.pop(); }
  } catch (e) { out.err = String(e && e.stack || e).slice(0, 300); }
  Object.assign(SHIP.time, keep);
  return out;
})()"""

def check_device(g, tag, want_on):
    if 'EV_DEVICE_ON' not in SRC: waiting('the device (F3a, EV_DEVICE_ON)'); return
    D = g.ev(DEVICE)
    if D['err']: fail(f"{tag}: device: {D['err']}"); return
    if not want_on:
        if any(D['off']['items']) or D['off']['lounge']: fail(f"{tag}: the device part acts while EV_DEVICE_ON is off: {D['off']}")
        return
    if not D['on']: fail(f"{tag}: EV_DEVICE_ON is off in this copy"); return
    for x in D['days']:
        say(f"  Schedule D{x['d']}: event items at {[hhmm_py(m) for m in x['got']]}")
        if x['got'] != x['want']: fail(f"{tag}: the Schedule on Day {x['d']} has event items at {[hhmm_py(m) for m in x['got']]}, the event's meetings and gatherings are at {[hhmm_py(m) for m in x['want']]}")
        for t in x['goals']: fail(f"{tag}: Schedule item {t} on Day {x['d']} has no goal to walk to")
    for x in D['trk']:
        say(f"  Tracked D{x['d']} {hhmm_py(x['m'])}: call booths {'closed' if x['shut'] else 'open'}, offered {x['offered']}")
        if x['offered'] == x['shut'] or x['closed'] != x['shut']: fail(f"{tag}: Tracked on Day {x['d']} {hhmm_py(x['m'])}: the booths are {'closed' if x['shut'] else 'open'} but offered = {x['offered']}, eventClosed = {x['closed']}")
    if [c[2] for c in D['closed']] != [True, False, False]: fail(f"{tag}: eventClosed for the bow lounge (front day 15:00, warning day 15:00, all-clear day 20:00): {D['closed']}")
    if D['open7'] is not None and [c[2] for c in D['open7']] != [True, False, True, True]: fail(f"{tag}: with Deck 7 closed, the auditorium should open just for the Friday address (15:00 shut, 16:10 open, 17:10 shut; the common room shut): {D['open7']}")
    say(f"  eventClosed: bow lounge {D['closed']}; Deck 7 closed in the onset: {D['open7']}")

def paper(g, tag):
    a = g.ev(PAPER); b = g.ev(PAPER)
    if json.dumps(a, sort_keys=True) != json.dumps(b, sort_keys=True): fail(f'{tag}: the events on paper came out differently the second time')
    return a

def show(a):
    say('  calendar: ' + ', '.join(f"{r['id']} D{r['day']} {r['kind']}{'' if r['built'] else ' (not built)'}{' (draft)' if r['draft'] else ''}{' (skipped)' if r['skipped'] else ''}" for r in a['cal']))
    say(f"  due: {a['due']} | played forward: " + ', '.join(f"{c['id']} D{c['day']}-{c['end'] - 1}" for c in a['chain']))
    say(f"  eventDay: {a['eventDay']}")
    for b in a['beats']:
        if b['what'] in ('phase', 'meeting', 'moment'): say(f"    {b['ev']}{' (draft)' if b['draft'] else ''} {b['what']} {b['id']} {b['at']}{' (moved from ' + hhmm_py(b['raw'] % 1440) + ')' if b['raw'] != b['t'] else ''}")

def check_hold(a, tag, on):
    # the Friday hold: Fridays from Day 5, 15:30-17:00, nothing else; a beat put there waits to 17:00 (only when on)
    if a['sw']['EV_CAL_ON'] is None: return
    want = [[d, m] for d in range(1, 36) for m in range(840, 1140, 5) if (d - 1) % 7 == 4 and d >= 5 and 930 <= m < 1020]
    if a['held'] != want: fail(f"{tag}: the Friday hold isn't Fridays from Day 5, 15:30-17:00: {a['held'][:6]}...")
    if a['synth'] is not None:
        exp = [[d, m, (1020 if on and (d - 1) % 7 == 4 and d >= 5 and 930 <= m < 1020 else m)] for d, m, _ in a['synth']]
        if a['synth'] != exp: fail(f"{tag}: a beat put in the hold should wait to 17:00 (calendar {'on' if on else 'off'}): {a['synth']} (want {exp})")
    for b in a['beats']:
        if b['held']: (note if b['draft'] else fail)(f"{tag}: {b['ev']} {b['what']} {b['id']} starts in the Friday hold: {b['at']}")
        elif b['rawHeld'] and on: (note if b['draft'] else fail)(f"{tag}: {b['ev']} {b['what']} {b['id']} falls in the Friday hold and waits to 17:00 ({b['at']}); none should be planned there")
        if b['what'] == 'meeting' and not b['held'] and (b['t'] % 1440) < 930 and (b['t'] % 1440) + b['len'] > 930 and (b['day'] - 1) % 7 == 4 and b['day'] >= 5:
            note(f"{tag}: {b['ev']} meeting {b['id']} runs into the Friday hold ({b['at']}, {b['len']} min)")
    for x in a['gath']:
        if x['held']: (note if x['draft'] else fail)(f"{tag}: gathering {x['id']} (D{x['day']} {hhmm_py(x['at'][0])}) is in the Friday hold (gatherings aren't moved)")

def check_notes(pw, path, tag, want_on):
    # the phase notes (F2) in their own page (the clock is run): the storm's calendar day 05:00 to 15:00 the next day
    if 'EV_NOTES_ON' not in SRC: waiting('the phase notes (F2, EV_NOTES_ON)'); return
    g = Game(pw, path); day = g.ev("typeof EV_CALENDAR !== 'undefined' ? (EV_CALENDAR.find(r => r.id === 'ionStorm') || {}).day || 11 : 11")
    a0, b0 = (day - 1) * 1440 + 300, day * 1440 + 900
    N = g.ev(f"({NOTES})({a0}, {b0})"); errs = g.errors[:3]; g.close()
    say(f"  phase notes D{day} 05:00 to D{day + 1} 15:00: {N['notes']} | cues: {N['cues']} | crew with a reaction line for {N['cue']}: {N['lines']}")
    if N['err']: fail(f"{tag}: phase notes: {N['err']}")
    for e in errs: fail(f"{tag}: phase notes: page error: {e}")
    if not want_on:
        if N['notes']: fail(f"{tag}: phase notes while EV_NOTES_ON is off: {N['notes']}")
        return
    if not N['on']: fail(f"{tag}: EV_NOTES_ON is off in this copy"); return
    if N['notes'] != N['want']: fail(f"{tag}: phase notes {N['notes']}, wanted {N['want']} (each once, at its own minute)")
    for w in N['want']:
        c = 'event.' + w.split('@')[0].replace(':', '.')
        if c not in N['cues']: fail(f"{tag}: no cue {c}")
    if N['cue'] and N['lines'] < 1: fail(f"{tag}: nobody has a reaction line for {N['cue']}")

def judge(a, tag):
    # everything on paper with the calendar on (parts 2-3, and the self-test)
    cal_on, guard_on = bool(a['sw']['EV_CAL_ON']), bool(a['sw']['EV_GUARD_ON'])
    if not cal_on: say('  SKIP: the calendar is off in this copy'); return
    built = [r for r in a['cal'] if r['built'] and not r['draft']]
    days = {r['id']: r['day'] for r in a['cal']}
    # the calendar's days, the due day, one at a time
    if days.get('ionStorm') != 11: fail(f"{tag}: the storm's calendar day is {days.get('ionStorm')}, not 11")
    first = next((r for r in built if not r['skipped']), None)
    if first and a['due'] != {'id': first['id'], 'day': first['day']}: fail(f"{tag}: due {a['due']}, not {first['id']} on Day {first['day']}")
    if [c['id'] for c in a['chain']] != [r['id'] for r in built if not r['skipped']]: fail(f"{tag}: the calendar played forward: {a['chain']} (want {[r['id'] for r in built]})")
    for x, y in zip(a['chain'], a['chain'][1:]):
        if y['day'] < x['end']: fail(f"{tag}: {y['id']} starts Day {y['day']} before {x['id']} ends (Day {x['end'] - 1})")
    rows = sorted((r['day'], r['day'] + r['days'], r['id'], r['draft'], r['kind']) for r in a['cal'] if r['built'])
    for i, x in enumerate(rows):
        for y in rows[i + 1:]:
            if y[0] < x[1] and x[0] < y[1]: (note if x[3] or y[3] else fail)(f"{tag}: two events at once on the calendar: {x[2]} D{x[0]}-{x[1] - 1} and {y[2]} D{y[0]}-{y[1] - 1}")
    # each phase begins at its minute, in order (eventNow minute by minute)
    for i, s in a['scan'].items():
        seen = [x for x in s['seen'] if x[0] != '-']
        if [k for k, _ in seen] != [k for k, _ in s['want']]: fail(f"{tag}: {i}: eventNow went {[k for k, _ in seen]}, the data says {[k for k, _ in s['want']]}")
        else:
            for (k, t), (_, w) in zip(seen, s['want']):
                if t != w: fail(f"{tag}: {k} began at minute {t}, evBeatAt says {w}")
    # the storm's skeleton: the warning Day 11, the front Friday Day 12 14:00, the all-clear Day 14
    ph = {b['id']: b for b in a['beats'] if b['ev'] == 'ionStorm' and b['what'] == 'phase'}
    if ph:
        if ph['warning']['day'] != 11: fail(f"{tag}: the storm's warning is {ph['warning']['at']}, not Day 11")
        if ph.get('onset') and ph['onset']['at'] != 'D12 Fri 14:00': fail(f"{tag}: the front is {ph['onset']['at']}, not D12 Fri 14:00")
        if ph.get('resolution') and ph['resolution']['day'] != 14: fail(f"{tag}: the all-clear is {ph['resolution']['at']}, not Day 14")
    # eventDay, and nothing reads the saved or live state
    if guard_on and a['eventDay'] is not None:
        if a['eventDay'] != a['bigDays']: fail(f"{tag}: eventDay is true on {a['eventDay']}, the big phases fall on {a['bigDays']}")
        if 'ionStorm' in days and a['eventDay'][:3] != [12, 13, 14]: fail(f"{tag}: the storm's eventDays are {a['eventDay']}, not 12-14")
    elif a['eventDay'] is None: waiting('eventDay (F1a)')
    if a['eventDayLive'] != a['eventDay']: fail(f"{tag}: eventDay changed with the saved/live state: {a['eventDay']} -> {a['eventDayLive']}")
    if a['skippedLive'] != a['skipped']: fail(f"{tag}: the passed-over events changed after load: {a['skipped']} -> {a['skippedLive']}")
    if [b['t'] for b in a['beats']] != a['beatsLive']: fail(f"{tag}: a beat's time changed with the saved/live state")
    if a['guardLive'] != a['guardNew']: fail(f"{tag}: guardFree changed with the saved/live state: {a['guardNew']} -> {a['guardLive']}")
    if a['skipped']: fail(f"{tag}: a new game passes over {a['skipped']}")
    check_hold(a, tag, True)
    if not a['stormNew']:   # OR1: Day 11 keeps today's storm hours until the storm update; noted, not failed
        d11 = [b for b in a['beats'] if b['ev'] == 'ionStorm' and b['day'] == 11]
        note(f"{tag}: Day 11 has today's storm hours (the storm update gives the new ones): " + ', '.join(f"{b['what']} {b['id']} {b['at'][-5:]}" for b in d11))
    # the career-beat guard (F1b)
    G = a['guard'] if guard_on else None                  # the guard off (the calendar alone): guardFree is always true
    if G:
        for x in G['items']:
            say(f"  guard: {x['what']} {x['when']} " + ('clear' if x['ok'] else f"CLASH {x['beats']}"))
            if not x['ok']: fail(f"{tag}: guard: {x['what']} at {x['when']} meets {x['beats']}")
        for d, n in G['captainDays'].items():
            if n > 1: fail(f"{tag}: two of the Captain's scenes on Day {d} (EV_BEATS)")
            if int(d) in G['testDays']: fail(f"{tag}: a Captain's scene on test Day {d}")
        if G['samples'] != [False, True, False, True, False, False]: fail(f"{tag}: the guard's samples {G['samples']} (want: test Day 15 no; Day 18 16:00 yes; Day 20 19:30-21:00 no; 19:00-20:15 yes; the night shift Day 21 05:00 no; Friday 16:00 no)")
    elif guard_on: waiting('guardFree and the career beats in EV_BEATS (F1b)')
    for d, l in a['captains'].items():
        if len(l) > 1: fail(f"{tag}: two of the Captain's scenes in the events' meetings on Day {d}: {l}")
    # the occasions the guard places (F1c)
    o = a['occ']
    if o and (o['table20'] is not None or o['ready18'] is not None):
        say(f"  occasions: the summons on Day 18 {o['ready18']}; the Captain's table Day 20 {o['table20']}{' (a night-shift week)' if o['night20'] else ''}, Day 48 {o['table48']}")
        if guard_on:
            if not o['ready18'] or o['ready18']['at'] != 960: fail(f"{tag}: the summons on Day 18 should be at 16:00, clear of the training: {o['ready18']}")
            if o['night20']:
                want = {'at': 1140, 'len': 75} if o['early'] else None
                if o['table20'] != want: fail(f"{tag}: the Captain's table on Day 20 (a night-shift week): {o['table20']}, want {want} (19:00, ending by 20:15)")
            if o['table48'] != {'at': 1170, 'len': 90}: fail(f"{tag}: the Captain's table on Day 48 (no night shift): {o['table48']}, want 19:30 for 90 minutes")
    elif o: waiting(f"the occasions' hours by the guard (F1c); the table today {hhmm_py(o['today'][0])} for {o['today'][1]} min")
    # the meetings' casts (F0b)
    called_built = any(c.get('called') is not None for c in a['called'])
    for c in a['called']:
        if c.get('slot'): say(f"  SKIP: {c['meet']}'s cast slot {c['id']} (filled from who's there; checked live in F7b)"); continue
        if not c['aboard']: fail(f"{tag}: {c['id']} for {c['meet']} on Day {c['day']}: not aboard"); continue
        if c['called'] is not None and c['called'] != c['off']: fail(f"{tag}: {c['id']} at {c['meet']} D{c['day']}: {'off' if c['off'] else 'on shift'} but called in = {c['called']}")
        if not c['there']: (fail if called_built else waiting)(f"{tag}: {c['id']} ({'off' if c['off'] else 'on shift'}) isn't planned at {c['meet']} ({c['at']}, Deck {c['want']} {c['wantRoom']}): {c['act']} at {c['place']} ({c['roomName']}, Deck {c['deck']}){'' if called_built else ' (F0b brings them)'}")
    say('  called in: ' + (', '.join(f"{c['id']}@{c['meet']} D{c['day']}" for c in a['called'] if c.get('off')) or 'nobody') + ('' if called_built else ' (eventCalledIn not built: marks not checked)'))
    if not called_built: waiting('eventCalledIn (F0b)')
    for x in a['calledStray']: fail(f"{tag}: called in but named in no meeting: {x}")
    # the gatherings fit their places
    for c in a['caps']:
        if c.get('missing'): fail(f"{tag}: gathering {c['id']} isn't on Day {c['day']}"); continue
        say(f"  gathering {c['id']} D{c['day']} {c['at']}: {c['want']} mean to go, {c['went']} planned there, {c['cap']} places ({c['seats']} seats) in {c['rooms']}")
        if c['want'] > c['cap'] or c['went'] > c['cap']: fail(f"{tag}: {c['id']}: {max(c['want'], c['went'])} people for {c['cap']} places")
        if c['want'] > CROWD: fail(f"{tag}: {c['id']}: a crowd of {c['want']}, over about 60")
        if c['mess'] and c['want'] > MESS_SEATS and c['cap'] - c['seats'] < c['want'] - MESS_SEATS: fail(f"{tag}: {c['id']} in the mess: {c['want']} people, {c['seats']} seats and too few standing places")
        if c['went'] < c['want']: note(f"{c['id']}: {c['want'] - c['went']} meant to go but aren't planned there")
    # no tradition in a gathering's or meeting's room while it's on; the plan's clashes (with the storm's new hours)
    for x in a['clash']: fail(f"{tag}: {x}")
    party = next((x for x in a['gath'] if x['id'] == 'party'), None)
    if days.get('ionStorm') and party and party['day']:
        pd, nd = str(party['day']), str(party['day'] + 1)
        on_pd = {e[0]: e for e in a['named'].get(pd, [])}; l15 = {e[0]: e for e in a['named'].get(nd, [])}
        probs = [f"{i} on the party night (D{pd} {hhmm_py(on_pd[i][1])})" for i in ('rec-talent-night', 'lap-of-the-wren') if i in on_pd and on_pd[i][1] < party['at'][1] and party['at'][0] < on_pd[i][2]]
        if 'lap-of-the-wren' not in l15 or l15['lap-of-the-wren'][1] != 1230: probs.append(f"Lap of the Wren not on D{nd} at 20:30")
        if probs: (fail if a['stormNew'] else waiting)(f"{tag}: the plan's clashes{'' if a['stormNew'] else ' (the storm update moves them)'}: " + '; '.join(probs))
    say('  traditions by day: ' + '; '.join(f"D{d}: " + ', '.join(f"{e[0]} {hhmm_py(e[1])}" for e in l) for d, l in sorted(a['named'].items(), key=lambda x: int(x[0]))))

with sync_playwright() as pw:
    # 0. the switches
    base = 'const EVENTS_ON = false;' in SRC
    cal_alone = bool(re.search(r'const EV_CAL_ON = EVENTS_ON;', SRC))
    print('Switches:', 'EVENTS_ON (off)' if base else 'EVENTS_ON on already' if 'const EVENTS_ON = true;' in SRC else 'no EVENTS_ON', '|', ', '.join(s for s in ['EV_CAL_ON', 'EV_GUARD_ON', 'EV_NOTES_ON', 'EV_DEVICE_ON', 'EV_REPLAY_ON', 'EV_RANK_ON', 'EV_COMMS_ON'] if re.search(r'const ' + s + r' = ', SRC)) or 'no pieces')
    if not base and 'const EVENTS_ON = true;' not in SRC:
        print('  SKIP: no events base in this build (EVENTS_ON): nothing to check')
        print('BIGEVENTS CHECK OK (nothing built yet)'); sys.exit(0)

    # 1. off: today's game
    print('\n1. Switched off (the build as it is):')
    g = Game(pw, sys.argv[1]); a = paper(g, 'off'); show(a)
    if a['sw']['EVENTS_ON']: note('EVENTS_ON is already on in this build: part 1 checks the build as it is')
    else:
        if a['eventDay']: fail(f"off: eventDay is true on {a['eventDay']}")
        moved = [b for b in a['beats'] if b['raw'] != b['t']]
        if moved: fail(f"off: beats moved by the hold: {[(b['id'], b['at']) for b in moved][:5]}")
        if a['skipped']: fail(f"off: a new game passes over {a['skipped']}")
        gf = g.ev("typeof guardFree === 'function' ? [guardFree(15, 600, 625, 'captain'), guardFree(12, 960, 990, 'beat'), guardFree(21, 300, 330, 'beat'), guardFree(20, 1170, 1260, 'captain')] : null")
        if gf is not None and gf != [True] * 4: fail(f'off: the guard still acts: {gf}')
        if a['occ'] and a['occ']['ready18'] and a['occ']['ready18']['at'] != 660: fail(f"off: the summons isn't at 11:00: {a['occ']['ready18']}")
        if a['occ'] and a['occ']['table20'] and a['occ']['table20'] != {'at': 1170, 'len': 90}: fail(f"off: the Captain's table isn't 19:30 for 90 minutes: {a['occ']['table20']}")
    party = [x for x in a['gath'] if x['id'] == 'party']
    if party and party[0]['k'] != 340: fail(f"the party's hash key is {party[0]['k']}, not 340")
    ks = [x['k'] for x in a['gath']]
    if len(ks) != len(set(ks)): fail(f'two ship-wide gatherings share a hash key: {ks}')
    trk = g.ev("SHIP_TRADITIONS.map(e => e.k)")
    if set(ks) & set(trk): fail(f'a ship-wide gathering shares a hash key with a tradition: {sorted(set(ks) & set(trk))}')
    check_hold(a, 'off', False)
    if not a['sw']['EVENTS_ON']: check_device(g, 'off', False)
    for e in g.errors[:3]: fail(f'off: page error: {e}')
    g.close()
    if not a['sw']['EVENTS_ON']: check_notes(pw, sys.argv[1], 'off', False)

    # 2. the calendar alone (EV_CAL_ON), then 3. everything on (EVENTS_ON)
    for n, tag, on, title in ([(2, 'calendar', ['EV_CAL_ON'], 'The calendar alone (EV_CAL_ON)')] if cal_alone else []) + [(3, 'on', 'all', 'Everything on (EVENTS_ON)')]:
        print(f'\n{n}. {title}:')
        g = Game(pw, variant(tag, on)); a = paper(g, tag); show(a); judge(a, tag); check_device(g, tag, on == 'all')
        for e in g.errors[:3]: fail(f'{tag}: page error: {e}')
        g.close()
        check_notes(pw, variant(tag, on), tag, on == 'all')

    # 4. the self-test: each planted clash is caught
    print('\n4. Self-test (clashes planted in a copy):')
    g = Game(pw, variant('on', 'all')); g.ev(PLANT); a = g.ev(PAPER); g.close()
    SINK = []; judge(a, 'planted'); caught, SINK = SINK, None
    for p in PLANTED:
        hit = [c for c in caught if p in c]
        print(f"  {p}: " + ('caught: ' + hit[0] if hit else 'NOT caught'))
        if not hit: fail(f'the self-test: the planted {p} was not caught')

    # 5. late saves (in the browser): a save made on Day 20 before events were on passes over the storm for good;
    # a Day 9 save keeps it; one that already ran it doesn't pass it over; decided once, at load
    print('\n5. Late saves:')
    if 'EV_SKIPPED' not in SRC: waiting('EV_SKIPPED (F0a)')
    else:
        tmp = WORK / 'test' / '_run_bigev_late.html'; tmp.write_text(instrument(pathlib.Path(variant('late', 'all')).read_text()))
        b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
        errs = []
        for day, log, want in [(20, [], {'skip': ['crossingLine', 'ionStorm', 'comet'], 'due': None}),
                               (9, [], {'skip': ['crossingLine'], 'due': {'id': 'ionStorm', 'day': 11}}),
                               (20, [{'id': 'ionStorm', 'startDay': 11, 'endDay': 17}], {'skip': ['crossingLine', 'comet'], 'due': None})]:
            save = {'v': 2, 'build': 'x', 'time': {'day': day, 'min': 600}, 'player': {'deck': 4, 'tile': [7, 3], 'facing': 0}, 'ship': {'decks': {}, 'eventLog': log}, 'crew': {}}
            pg = b.new_page(viewport={'width': 900, 'height': 760})
            pg.on('pageerror', lambda e: errs.append(str(e)))
            pg.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
            pg.add_init_script(INIT + "try { localStorage.clear(); localStorage.setItem('starship-cadet-save', " + json.dumps(json.dumps(save)) + "); localStorage.setItem('starship-cadet-arrived', '1'); Storage.prototype.setItem = () => {}; } catch (e) {}")
            pg.goto('file://' + str(tmp))
            pg.wait_for_function('window.__sc !== undefined || window.__err', timeout=60000)
            r = pg.evaluate('s => window.__sc(s)', """(() => { const sk = [...EV_SKIPPED], due = evCalDue(), ed = [...Array(31).keys()].filter(d => eventDay(d)), d0 = SHIP.time.day;
              SHIP.time.day = 3; const sk2 = [...EV_SKIPPED], ed2 = [...Array(31).keys()].filter(d => eventDay(d)); SHIP.time.day = d0;
              return { day: d0, sk, due, ed, same: JSON.stringify([sk, ed]) === JSON.stringify([sk2, ed2]) }; })()""")
            pg.close()
            print(f"  a Day {day} save{' (storm logged)' if log else ''}: loaded on Day {r['day']}, passes over {r['sk']}, due {r['due']}, eventDay {r['ed']}")
            if r['day'] != day: fail(f"the Day {day} save loaded on Day {r['day']}"); continue
            if sorted(r['sk']) != sorted(want['skip']): fail(f"a Day {day} save should pass over {sorted(want['skip'])}: {r['sk']}")
            if r['due'] != want['due']: fail(f"a Day {day} save: due {r['due']}, want {want['due']} (the visit is still a draft)")
            if not r['same']: fail(f"a Day {day} save: what's passed over changed after load")
            if day == 20 and not log and r['ed']: fail(f"a Day 20 save (storm passed over) still has eventDays {r['ed']}")
        b.close()
        for e in errs[:3]: fail(f'late saves: page error: {e}')

    # 6. live (F7b) and crowds (F7c): with F2-F4 and the storm update
    print('\n6. Live phases and crowds:')
    waiting('F7b (jumps, reloads mid-phase and mid-meeting) comes with F4 (the phase notes and the device are in parts 1-3); F7c (draw calls at about 60, phone size) with the storm update')

print('\nBIGEVENTS CHECK OK' if ok else '\nBIGEVENTS CHECK FAILED')
sys.exit(0 if ok else 1)
