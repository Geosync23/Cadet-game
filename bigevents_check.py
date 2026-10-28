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
#   shift or called in (eventCalledIn), and planned in the meeting's room; gatherings fit their places (unseated crowds
#   at most 60, never more there at once than its places; a seated one (no standing, the user's) never more at once than its seats, any number meaning to go: lead 24); no tradition in a gathering's or meeting's room while it's on, and the
#   plan's clashes (talent night and Lap of the Wren off the party night, the lap on Day 15 at 20:30); the run twice
#   is identical;
#   4. a self-test: clashes planted in a copy (a meeting in the Friday hold, one over the officer's ceremony, a
#   gathering in the hold, a dressed copy of a tradition in the party's room) must each be caught;
#   5. late saves (F0c): evSkippedFor for any day, evCalPlan; real saves: SHIP.evFrom (the day events first came on,
#   saved) decides what's passed over (evFrom 0 on Day 20: the storm it missed is run at load and logged), kept through a save and a reload, null and unsaved while off;
#   and in parts 1-3, the phase notes (F2): the clock run through the storm's warning and front, each phase's note once at
#   its minute, its cue, a crew reaction line for the front; none while EV_NOTES_ON is off; and the device (F3a): the
#   Schedule's event items at the meetings' minutes (each EV_SHIPWIDE gathering once as a tradition, nothing twice), a
#   meeting's own toast only while the device's heads-ups are off, Tracked's booths only while open, eventClosed
#   (the auditorium opened just for the Friday address); nothing while EV_DEVICE_ON is off; called in (F0b): skipping
#   through the all-clear, one calledIn note and one cue each for the four off that day; none while off.
# Each part skips (SKIP, or WAITING with what it waits for) while its switch or code isn't there yet, so it runs on
# today's integration and grows as the events base is built. Exits 1 on a FAIL. About 2 minutes.
# Setup and environment as for cadet_test.py (three.js in $CADET_WORK/three, CADET_CHROME a Chromium).
# Run:  python3 bigevents_check.py BUILD.html
import sys, re, json, pathlib, os
exec(open(__file__.replace('bigevents_check.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
RUN_ID = f'p{os.getpid()}_'   # FX18-1: this run's copies carry the process id (two runs in one CADET_WORK never open each other's), gone at exit
__import__('atexit').register(lambda: [f.unlink(missing_ok=True) for f in (WORK / 'test').glob(f'*_{RUN_ID}*') if f.is_file()])
from playwright.sync_api import sync_playwright

SRC = pathlib.Path(sys.argv[1]).read_text()
SWAP = bool(re.search(r"^const EV_SWAP_ON = true", SRC, flags=re.M))   # the event swap (0.93.2): the visit (Day 16) is the one a Day 20 load passes over; the comet (Day 22, FX25) is still due, and past by Day 23 with the visit
COMET_ON = bool(re.search(r"^const EV_COMET_ON = true", SRC, flags=re.M))   # the comet (FX25, 0.93.2): on Monday Day 22, after a Day 20 load (so not passed over); a Day 23 load passes it over
PASSED = 'diplomatic' if SWAP else None if COMET_ON else 'comet'
PAST = [PASSED] if PASSED else []
VESSEL_ON = bool(re.search(r"^const EV_VESSEL_ON = true", SRC, flags=re.M))   # A Veyli vessel needs help (VB1, Days 27-30): due on Day 27 after a Day 23 load; a save first loaded with it on from Day 28 passes it over (SHIP.vesselFrom)
OFF_BUILD = sys.argv[1]          # the build switched off, for part 1
ON_ALREADY = 'const EVENTS_ON = true;' in SRC
if ON_ALREADY:                   # events on in the build (storm S10): parts 1-2 need the switched-off game, so make that copy
    SRC = SRC.replace('const EVENTS_ON = true;', 'const EVENTS_ON = false;', 1)
    (WORK / 'test').mkdir(parents=True, exist_ok=True)
    OFF_BUILD = str(WORK / 'test' / f'bigev_{RUN_ID}off.html'); pathlib.Path(OFF_BUILD).write_text(SRC)
CROWD = 80                     # a standing crowd's limit on meaning to go, set by performance tests, not a fixed 60 (the user, 2026-10-21: "60 was just a guess
                               # on performance. We can go higher. Just need to test for performance."; was the events plan v3.2 answer 4's 60; lead 24: unseated only).
                               # LB3's measure (perf_check's Line ceremony scene with 0-90 extra people stood in the bow lounge, the phone and trifold sizes): draw
                               # calls barely move (the crowd packs 12 to a call: 391 -> 397 at the widest view from 59 to 149 on Deck 3, budget 450); triangles grow
                               # about 4k a person (516k -> 598k at 79, 794k at 149); game code 1.5-3.5 ms a frame throughout. About 3 in 4 of those meaning to go
                               # get there (the ceremony: 61 -> 45), so 80 is about 60 in the room and 75-80 on the deck: about 600k triangles, the busiest scene
                               # already shipped (Sunday dinner, 69 on Deck 3, 565k) plus a little. Raise it only after measuring again (plans/build-table.md, line L5j)
MESS_SEATS = 44                # the mess hall's seats (kept for reference; the standing-places rule it served is dropped)
LINE_SUPPER_MIN = 40           # the Line supper: at least about 40 should come (ER3's review)

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
    p = WORK / 'test' / f'bigev_{RUN_ID}{tag}.html'; p.write_text(src); return str(p)

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
    const off = !!p.work && !isWorkDay(p, b.day), c = has('eventCalledIn') ? !!eventCalledIn(p, b.day) : null;   // no rota (Saruth, a guest): never off duty, so never called in (EV1, the visit on)
    const seg = planDay(p, b.day).find(s => s.from <= b.t && b.t < s.to);
    const pl = seg && seg.placeId && S.byId.get(seg.placeId), rm = pl && DECKS[pl.deck] && DECKS[pl.deck].rooms && DECKS[pl.deck].rooms[pl.room];
    const arriving = !!seg && !!p.guest && seg.tag === 'arrive' && seg.deck === b.deck;   // a guest stepping off the shuttle into the bay that minute (the Veyli at their greeting, GUEST_AT 10:00)
    const there = arriving || !!seg && seg.deck === b.deck && !!rm && (!b.room || (rm.name || '').toLowerCase() === b.room);
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
    const cap = new Set(pls.map(pl => pl.id)).size, seats = new Set(pls.filter(pl => pl.pose === 'sit' || /seat|chair|bench|stool|sofa/.test(pl.type)).map(pl => pl.id)).size, crowd = new Set(pls.filter(pl => pl.gather).map(pl => pl.id)).size;   // a seat: any place sat at (the long tables' chairs are type 'event'); a crowd spot: a gather place
    // the most crew there at once (lead 23: never over its places at any one time), minute by minute through the gathering
    const B = (g.day - 1) * 1440, segs = people.flatMap(p => planDay(p, g.day).filter(s => s.tag && (s.tag === 'ev-' + g.id || s.tag.startsWith('ev-' + g.id + '-'))));
    let peak = 0, peakAt = null; for (let m = B + e.from - 30; m < B + e.to + 30; m++) { const n = segs.filter(s => s.from <= m && m < s.to).length; if (n > peak) { peak = n; peakAt = m - B; } }
    // a seated one (the user: nobody eats standing): each who means to go, a meal with no place (not the servery queue) in its window = eaten standing (PR10's gap)
    const standing = e.ev.seated ? people.filter(p => eventPlan(p, g.day).some(x => x.id === g.id) && planDay(p, g.day).some(s => (s.act === 'dinner' || s.act === 'breakfast') && !s.placeId && s.tag !== 'queue' && s.from < B + e.to + 30 && B + e.from - 30 < s.to)).map(p => p.id) : [];
    out.caps.push({ id: g.id, day: g.day, at: hhmm(e.from) + '-' + hhmm(e.to), want, went, cap, seats, peak, standing, peakAt: peakAt == null ? null : hhmm(peakAt), stay: e.ev.stay || null, seated: !!e.ev.seated, crowd, rooms: g.rooms, mess: g.rooms.some(r => /mess/.test(r)) });
  }
  // traditions in a gathering's or meeting's room while it's on; and the traditions on the events' days, for the plan's list
  const isTrad = e => SHIP_TRADITIONS.some(t => t.id === e.ev.id);   // by id: a ship-wide event's day dress (S6, EV_DAY_DRESS) lists a dressed copy, a new object (PR4)
  const span = []; for (const r of CAL.filter(built)) for (let d = r.day; d <= r.day + SHIP_EVENTS[r.id].days; d++) span.push(d);
  for (const d of [...new Set(span)]) out.named[d] = eventsOn(d).filter(isTrad).map(e => [e.id, e.from, e.to]);
  const things = out.gath.filter(g => !g.draft && g.day).map(g => ({ id: g.id, day: g.day, from: g.at[0], to: g.at[1], rooms: g.rooms }))
    .concat(out.beats.filter(b => b.what === 'meeting' && !b.draft && b.room).map(b => ({ id: b.id, day: b.day, from: b.t - ab(b.day, 0), to: b.t - ab(b.day, 0) + b.len, rooms: [b.deck + '|' + b.room] })));
  for (const x of things) for (const e of eventsOn(x.day).filter(isTrad)) {
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
    for (const g of out.gath.filter(g => !g.draft && g.day)) {   // its own beat aside, as a meeting's: one with its id, or a Captain's beat that day within 15 minutes (EV5: the Line's ceremony)
      const own = evBeatsOn(g.day).filter(x => g.at[0] < x.to && g.at[1] > x.from && x.id !== g.id);
      G.items.push({ what: 'gathering ' + g.id, when: dm(ab(g.day, g.at[0])), ok: guardFree(g.day, g.at[0], g.at[1], 'beat') || own.every(x => x.kind === 'captain' && Math.abs(x.from - g.at[0]) <= 15), beats: own.map(x => x.id) });
    }
    for (const b of EV_BEATS) if (b.kind === 'captain') G.captainDays[b.day] = (G.captainDays[b.day] || 0) + 1;
    // test day; Day 18 16:00 free; the table at 19:30 on Day 20 crosses the night shift, at 19:00 it doesn't; Day 21 05:00 is the night shift; Friday 16:00
    G.samples = [guardFree(15, 600, 625, 'captain'), guardFree(18, 960, 985, 'captain'), guardFree(20, 1170, 1260, 'captain'), guardFree(20, 1140, 1215, 'captain'), guardFree(21, 300, 330, 'beat'), guardFree(12, 960, 990, 'beat')];
    G.p5 = typeof P5_STEP5 !== 'undefined' && !!P5_STEP5; G.samples5 = [guardFree(23, 300, 330, 'beat'), guardFree(16, 495, 510, 'beat'), guardFree(22, 1380, 1400, 'beat'), guardFree(24, 1300, 1330, 'beat')];   // Pillar 5 Step 5's held hours (S5-1): nights from Day 22, the result at 08:15 on Day 16
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
  // a dressed tradition (a copy, as S6's EV_DAY_DRESS makes) put in the party's room during the party
  const t = SHIP_TRADITIONS.find(e => e.id === 'book-circle') || SHIP_TRADITIONS[0], pd = EV_CALENDAR.find(r => r.id === 'ionStorm').day + p.when.day;
  const copy = { ...t, where: p.where.map(w => ({ ...w })) }, on0 = eventsOn;
  eventsOn = d => { const l = on0(d); return d === pd ? l.concat([{ id: t.id, name: t.name, ev: copy, day: d, from: p.at[0] + 10, to: p.at[0] + 50, honorees: [], names: '', first: '' }]) : l; };
  return t.id;
})()"""
PLANTED = ['plantHold', 'plantGuard', 'plantGath']
# the comet (FX25, A8): a dressed copy of quiz night put in the bow lounge at 21:45 on the comet's day, during its gathering
PLANT_COMET = r"""(() => {
  if (!SHIP_EVENTS.comet) return null;
  const p = EV_SHIPWIDE.find(g => g.id === 'cometLounge'), t = SHIP_TRADITIONS.find(e => e.id === 'quiz') || SHIP_TRADITIONS[1], pd = EV_CALENDAR.find(r => r.id === 'comet').day;
  const copy = { ...t, where: p.where.map(w => ({ ...w })) }, on0 = eventsOn;
  eventsOn = d => { const l = on0(d); return d === pd ? l.concat([{ id: t.id, name: t.name, ev: copy, day: d, from: 1305, to: 1335, honorees: [], names: '', first: '' }]) : l; };
  return t.id;
})()"""

# F2, the phase notes, live on paper (EV1's part, made from the data): the clock run every 5 ship minutes from 05:00 on
# the first built event's calendar day to 15:00 the next (the storm's warning and front) through eventAdvance(t, quiet)
# and section 20's socialTick; each phase's note once, at its own minute (evBeatAt); the cue event.<id>.<phase> made
# (cues last a ship day: read at 12:00 on the first day and at the end); someone's reaction line for the last phase
# (section 22's lineFor, kind 'cue'). Switched off (EV_NOTES_ON): no note at all
NOTES = r"""((a, b) => {
  const out = { notes: [], cues: [], lines: 0, want: [], err: null, on: typeof EV_NOTES_ON !== 'undefined' ? EV_NOTES_ON : null };
  try {
    const r = typeof EV_CALENDAR !== 'undefined' && EV_CAL_ON ? (EV_CALENDAR.find(x => x.id === 'ionStorm' && SHIP_EVENTS[x.id] && !SHIP_EVENTS[x.id].draft) || EV_CALENDAR.find(x => SHIP_EVENTS[x.id] && !SHIP_EVENTS[x.id].draft)) : null;   // the storm's own row (EV5: the Line comes first)
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
    const r = typeof EV_CALENDAR !== 'undefined' && EV_CAL_ON ? (EV_CALENDAR.find(x => x.id === 'ionStorm' && SHIP_EVENTS[x.id] && !SHIP_EVENTS[x.id].draft) || EV_CALENDAR.find(x => SHIP_EVENTS[x.id] && !SHIP_EVENTS[x.id].draft)) : null;   // the storm's own row (EV5: the Line comes first)
    const sd = r ? r.day : (eventDueDay() || {}).day;
    out.off = { items: [sd, sd + 1, sd + 2, sd + 3].map(d => eventItems(ab(d, 0), ab(d, 1439)).length), lounge: eventClosed({ deck: 3, room: 'L' }, ab(sd + 1, 900)) };
    if (!out.on) return out;
    const meets = new Set((SHIP_EVENTS[r.id].meetings || []).map(m => m.id)), shipwide = new Set(EV_SHIPWIDE.map(g => g.id));
    for (let d = sd; d < sd + SHIP_EVENTS[r.id].days; d++) {
      const G = eventGatherings(d), all = devDay(d), items = all.filter(x => x.kind === 'event'), trads = all.filter(x => x.kind === 'tradition');
      const want = G.filter(g => meets.has(g.id) || !shipwide.has(g.id)).map(g => g.at).sort((x, y) => x - y);   // a meeting (or a gathering not in EV_SHIPWIDE) once as 'event'
      const asTrad = G.filter(g => shipwide.has(g.id)).map(g => [g.id, g.at, trads.filter(x => String(x.id).split('@')[0] === g.id && x.from === g.at).length]);   // an EV_SHIPWIDE gathering once as 'tradition'
      const seen = {}, twice = []; for (const x of all) { const k = x.title + '@' + x.from; if (seen[k]) twice.push(k); seen[k] = 1; }
      out.days.push({ d, want, got: items.map(x => x.from).sort((x, y) => x - y), asTrad, twice, goals: items.filter(x => { const g = devItemGoal(x); return !(g && Number.isInteger(g.deck) && g.room); }).map(x => x.title + ' ' + hhmm(x.from)) });
    }
    // a meeting's own toast (m.notify): none while the device's heads-ups are on (the Schedule gives it), kept when they're off
    const R0 = SHIP.device && SHIP.device.calendarRemind, ev0 = SHIP.event, toast = on => { MEETINGS.length = 0; SHIP.event = null; if (R0) R0.on = on; eventAdvance(ab(sd, 0) + 1, true);
      return (SHIP_EVENTS[r.id].meetings || []).map(m => { const x = MEETINGS.find(y => y.id === m.id); return [m.id, x ? x.notify || null : 'missing', m.notify || null]; }); };
    if (R0) { const was = R0.on; out.toast = { on: toast(true), off: toast(false) }; R0.on = was; MEETINGS.length = 0; SHIP.event = ev0; }
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
        if x['got'] != x['want']: fail(f"{tag}: the Schedule on Day {x['d']} has event items at {[hhmm_py(m) for m in x['got']]}, the event's meetings are at {[hhmm_py(m) for m in x['want']]}")
        for i, at, n in x['asTrad']:
            say(f"  Schedule D{x['d']}: {i} {hhmm_py(at)} as a tradition x{n}")
            if n != 1: fail(f"{tag}: the gathering {i} on Day {x['d']} {hhmm_py(at)} is listed {n} times as a tradition, not once")
        for k in x['twice']: fail(f"{tag}: the Schedule on Day {x['d']} lists {k} twice")
        for t in x['goals']: fail(f"{tag}: Schedule item {t} on Day {x['d']} has no goal to walk to")
    for x in D['trk']:
        say(f"  Tracked D{x['d']} {hhmm_py(x['m'])}: call booths {'closed' if x['shut'] else 'open'}, offered {x['offered']}")
        if x['offered'] == x['shut'] or x['closed'] != x['shut']: fail(f"{tag}: Tracked on Day {x['d']} {hhmm_py(x['m'])}: the booths are {'closed' if x['shut'] else 'open'} but offered = {x['offered']}, eventClosed = {x['closed']}")
    if [c[2] for c in D['closed']] != [True, False, False]: fail(f"{tag}: eventClosed for the bow lounge (front day 15:00, warning day 15:00, all-clear day 20:00): {D['closed']}")
    if D['open7'] is not None and [c[2] for c in D['open7']] != [True, False, True, True]: fail(f"{tag}: with Deck 7 closed, the auditorium should open just for the Friday address (15:00 shut, 16:10 open, 17:10 shut; the common room shut): {D['open7']}")
    say(f"  eventClosed: bow lounge {D['closed']}; Deck 7 closed in the onset: {D['open7']}")
    T = D.get('toast')
    if T is None: waiting(f"{tag}: the meetings' toasts (no SHIP.device.calendarRemind)")
    else:
        say(f"  meeting toasts: heads-ups on {T['on']}; off {T['off']}")
        for i, got, want in T['on']:
            if got is not None: fail(f"{tag}: meeting {i} keeps its own toast while the device's heads-ups are on: {got}")
        for i, got, want in T['off']:
            if got != want: fail(f"{tag}: meeting {i} with heads-ups off should keep its toast {want!r}: {got!r}")

# F0b, called in (EV2, ca2f9d6; PR3's ask): in its own page, skipTo 10 minutes before the first event meeting that
# calls someone in (the storm's all-clear, Day 14 10:00), then 5 minutes after it and an hour after it: one
# simNote('calledIn') for each named person off that day (eventCalledIn), at a minute in; one 'calledIn' cue each in
# section 20's cues (read at the hour after: notes are applied when their social hour runs); nobody else. Off (EV_CALLIN_ON): no calledIn note at all
CALLIN = r"""(() => {
  const out = { on: typeof EV_CALLIN_ON !== 'undefined' ? EV_CALLIN_ON : null, meets: [], notes: [], err: null };
  try {
    const ab = (d, m) => (d - 1) * 1440 + m, list = [];
    if (out.on && typeof evMeetsOn === 'function') for (let d = 1; d <= 40; d++) for (const m of evMeetsOn(d)) {
      const want = m.who.filter(w => { const p = schedPeople().find(x => x.id === w); return p && eventCalledIn(p, d); }).sort();
      if (want.length) list.push({ id: m.id, day: d, at: m.at, t: ab(d, m.at), want });
    }
    if (!list.length) skipTo(ab(14, 590)), skipTo(ab(14, 665));   // off: the all-clear's hour, where it would be
    for (const m of list.sort((a, b) => a.t - b.t)) {   // each meeting that calls someone in, in turn: 10 minutes before, 5 after, an hour after (its cues: the hour after)
      for (const t of [m.t - 10, m.t + 5, m.t + 65]) if (t > shipNow()) skipTo(t);
      const cues = ((SHIP.social && SHIP.social.cues) || []).filter(c => c.key === 'calledIn' && c.at >= m.t - 1).map(c => c.who).sort();
      const notes = simNotes('calledIn').filter(n => n.meeting === m.id && n.day === m.day).map(n => [n.who, n.t]).sort();
      out.meets.push({ meet: m.id + ' D' + m.day + ' ' + hhmm(m.at), id: m.id, want: m.want, at: m.t, notes, cues });
    }
    out.notes = simNotes('calledIn').map(n => [n.who, n.meeting, n.day, n.t]).sort();
  } catch (e) { out.err = String(e && e.stack || e).slice(0, 300); }
  return out;
})()"""

def check_callin(pw, path, tag, want_on):
    if 'EV_CALLIN_ON' not in SRC: waiting('called in (F0b, EV_CALLIN_ON)'); return
    g = Game(pw, path); C = g.ev(CALLIN); errs = g.errors[:3]; g.close()
    if C['err']: fail(f"{tag}: called in: {C['err']}"); return
    for e in errs: fail(f"{tag}: called in: page error: {e}")
    if not want_on:
        say(f"  called in (off): notes {C['notes']}")
        if C['notes']: fail(f"{tag}: calledIn notes while EV_CALLIN_ON is off: {C['notes']}")
        return
    if not C['meets']: fail(f"{tag}: no event meeting calls anyone in"); return
    for M in C['meets']:
        say(f"  called in: {M['meet']}: notes {M['notes']}; cues {M['cues']}")
        got = sorted(n[0] for n in M['notes'])
        if got != M['want']: fail(f"{tag}: {M['meet']}: calledIn notes for {got}, want one each for {M['want']}")
        for w, t in M['notes']:
            if t != M['at'] + 1: fail(f"{tag}: {M['meet']}: {w}'s calledIn note at minute {t}, want {M['at'] + 1} (a minute into the meeting)")
        if M['cues'] != M['want']: fail(f"{tag}: {M['meet']}: calledIn cues for {M['cues']}, want one each for {M['want']}")
        if M['id'] == 'allClear' and M['want'] != ['calder', 'holt', 'marrow', 'sato']: fail(f"{tag}: the all-clear's called in are {M['want']}, the plan says Marrow, Sato, Holt and Calder")
    stray = [n for n in C['notes'] if not any(n[1] == M['id'] and n[0] in M['want'] for M in C['meets'])]
    if stray: fail(f"{tag}: calledIn notes for nobody's meeting: {stray}")

# Crossing the Line (EV5, claude/line-update; plans/event-line-plan.md), in a copy with EV_LINE_ON switched on too:
# the oath ceremony's cast at the glass (Marrow and Brennan on the lead spots, Brennan on her galley stint), the front
# spots for first-timers only (lineFirst), Saruth never at the ceremony (a Veyli does not watch another people's rite),
# Tomas at his post through the day and on the Lap at 20:30 with Torres-Zeke and Pell, the Line supper (the Sunday table
# dressed) at most 60 and never more there at once than its places, and no commendation (commend: false)
LINE = r"""(() => {
  const out = { err: null }, ab = (d, m) => (d - 1) * 1440 + m, P = id => schedPeople().find(p => p.id === id), S = schedData();
  try {
    const r = EV_CALENDAR.find(x => x.id === 'crossingLine'), def = SHIP_EVENTS.crossingLine, d = r.day + 1;   // the crossing: its day 1 (Sunday Day 7)
    out.day = d; out.commend = def.commend;
    const at = (p, m) => { const q = P(p); const s = q && planDay(q, d).find(s => s.from <= ab(d, m) && ab(d, m) < s.to); return s ? { place: s.placeId || null, tag: s.tag || null, act: s.act, from: s.from - ab(d, 0), to: s.to - ab(d, 0) } : null; };
    const cer = def.meetings.find(m => m.id === 'crossingCeremony'), cm = cer.at[1];
    out.cast = ['marrow', 'brennan'].map(id => [id, at(id, cm + 5)]);
    const g = EV_SHIPWIDE.find(x => x.id === 'lineCeremony'), gFrom = g.at[0], gTo = g.at[1];
    out.saruth = (P('saruth') ? planDay(P('saruth'), d) : []).filter(s => s.from < ab(d, gTo) && ab(d, gFrom) < s.to && /^ev-(lineCeremony|crossingLine)/.test(s.tag || '')).map(s => s.tag + '@' + (s.placeId || ''));
    const front = new Set((S.shared.get('3|@bow-lounge-line-front') || []).map(q => q.id)), first = typeof lineFirst === 'function' ? lineFirst() : new Set();
    out.front = { spots: front.size, inFront: [], notFirst: [] };
    for (const p of schedPeople()) for (const s of planDay(p, d)) if (s.placeId && front.has(s.placeId) && s.from < ab(d, gTo) && ab(d, gFrom) < s.to) { out.front.inFront.push(p.id); if (!first.has(p.id)) out.front.notFirst.push(p.id); }
    out.tomas = { post: at('tomas', 600), lap: at('tomas', 1240) };
    out.lapWith = ['torres-zeke', 'pell'].map(id => [id, at(id, 1240)]);
    out.watch = ['tomas', 'ueda-vera'].map(id => { const l = []; for (let m = 870; m <= 915; m += 5) l.push([hhmm(m), at(id, m)]); return [id, l]; });   // 14:30-15:15: the crossing's afternoon
    const sup = eventsOn(d).find(e => e.id === 'sunday-table'), people = schedPeople();
    if (sup) {
      const want = people.filter(p => eventPlan(p, d).some(x => x.id === 'sunday-table')).length, B = ab(d, 0);
      const isSup = s => s.tag && (s.tag === 'ev-sunday-table' || s.tag.startsWith('ev-sunday-table-')), segs = people.flatMap(p => planDay(p, d).filter(isSup));
      const came = people.filter(p => planDay(p, d).some(isSup)).length;
      let peak = 0; for (let m = B + sup.from; m < B + sup.to; m++) peak = Math.max(peak, segs.filter(s => s.from <= m && m < s.to).length);
      const pls = sup.ev.where.flatMap((w, i) => S.shared.get(w.deck + '|' + (w.room ? 'ev:' + sup.id + ':' + i : w.pool)) || []), cap = new Set(pls.map(q => q.id)).size;
      const seats = new Set(pls.filter(q => q.pose === 'sit' || /seat|chair|bench|stool|sofa/.test(q.type)).map(q => q.id)).size, crowd = new Set(pls.filter(q => q.gather).map(q => q.id)).size;
      const standing = people.filter(p => eventPlan(p, d).some(x => x.id === 'sunday-table') && planDay(p, d).some(s => s.act === 'dinner' && !s.placeId && s.tag !== 'queue' && s.from < B + sup.to + 30 && B + sup.from - 30 < s.to)).map(p => p.id);   // eaten standing (PR10's gap)
      out.supper = { at: hhmm(sup.from) + '-' + hhmm(sup.to), want, came, peak, cap, seats, crowd, seated: !!sup.ev.seated, standing };
    }
  } catch (e) { out.err = String(e && e.stack || e).slice(0, 300); }
  return out;
})()"""

def check_line(g, tag):
    L = g.ev(LINE)
    if L['err']: fail(f"{tag}: the Line: {L['err']}"); return
    say(f"  the Line D{L['day']}: cast {L['cast']}; front spots {L['front']['spots']}, in them {len(L['front']['inFront'])}; Tomas {L['tomas']}; at the Lap {L['lapWith']}; supper {L.get('supper')}")
    if L['commend'] is not False: fail(f"{tag}: the Line should never commend (commend: false): {L['commend']}")
    for i, a in L['cast']:
        if not a or not str(a['place'] or '').startswith('3-bow-lounge-line-lead'): fail(f"{tag}: {i} isn't on a lead spot at the oath: {a}")
    b = dict(L['cast']).get('brennan')
    if b and b['place'] != '3-bow-lounge-line-lead-2': fail(f"{tag}: Brennan should be at 3-bow-lounge-line-lead-2 for the oath: {b}")
    if L['saruth']: fail(f"{tag}: Saruth is at the Line's ceremony: {L['saruth']}")
    if not L['front']['spots']: fail(f"{tag}: no front spots ('@bow-lounge-line-front')")
    if L['front']['notFirst']: fail(f"{tag}: not first-timers in the front spots: {L['front']['notFirst']}")
    t = L['tomas']
    if not t['post'] or t['post']['place'] != '2-watch-6': fail(f"{tag}: Tomas isn't at his post (2-watch-6) at 10:00 on the Line's day: {t['post']}")
    if not t['lap'] or not str(t['lap']['tag'] or '').startswith('ev-lap-of-the-wren'): fail(f"{tag}: Tomas isn't on the Lap at 20:40: {t['lap']}")
    for i, a in L['lapWith']:
        if not a or not str(a['tag'] or '').startswith('ev-lap-of-the-wren'): fail(f"{tag}: {i} isn't on the Lap at 20:40: {a}")
    sp = L.get('supper')
    if not sp: fail(f"{tag}: no Line supper (the Sunday table) on Day {L['day']}")
    else:
        if sp['want'] > CROWD and not sp['seated']: fail(f"{tag}: the Line supper: a crowd of {sp['want']}, over {CROWD}")   # seated: no cap on meaning to go (lead 24), only at once <= seats
        if sp['peak'] > sp['cap']: fail(f"{tag}: the Line supper: {sp['peak']} at once for {sp['cap']} places")
        say(f"  the Line supper {sp['at']}: {sp['want']} mean to go, {sp['came']} came, at most {sp['peak']} at once, {sp['seats']} seats")
        if sp['came'] < LINE_SUPPER_MIN: fail(f"{tag}: the Line supper: only {sp['came']} came (want {sp['want']}), fewer than {LINE_SUPPER_MIN}: the ship's supper of the year is empty")
        if not sp['seated']: fail(f"{tag}: the Line supper isn't seated (the user's call: no standing at meals): {sp['seats']} seats, {sp['crowd']} standing spots, {sp['peak']} at once")
        else:   # seated, as the lantern supper: never more at once than its seats, no standing spot
            if sp['peak'] > sp['seats']: fail(f"{tag}: the Line supper (seated): {sp['peak']} at once for {sp['seats']} seats")
            if sp['standing']: fail(f"{tag}: the Line supper (seated): {len(sp['standing'])} eat standing, no seat for their sitting: {sp['standing'][:8]}")
            if sp['crowd']: fail(f"{tag}: the Line supper (seated) has {sp['crowd']} standing crowd spots")
    # the watch keeps the ship through the crossing's afternoon: Tomas and Ueda at their posts every 5 minutes from 14:30
    # to 15:15 (a short toilet or hand-wash on Deck 2 is fine), never at an event
    for i, l in L['watch']:
        off = [f"{m} {a['place'] if a else None}/{a['tag'] if a else None}" for m, a in l if not a or str(a['tag'] or '').startswith('ev-') or not (str(a['place'] or '').startswith('2-watch-') or str(a['place'] or '').startswith('2-wc'))]
        if off: fail(f"{tag}: {i} is off watch in the crossing's afternoon (14:30-15:15): {off}")

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
        if 'ionStorm' in days and not {12, 13, 14} <= set(a['eventDay']): fail(f"{tag}: the storm's eventDays {sorted({12, 13, 14} - set(a['eventDay']))} are missing from {a['eventDay']}")
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
        if G.get('p5'):   # Pillar 5 Step 5's held hours (S5-1, plan v3.1): the nights move to Days 22-24, so Day 20's table is back at 19:30 and Day 21 05:00 is free
            if G['samples'] != [False, True, True, True, True, False]: fail(f"{tag}: the guard's samples with P5_STEP5 {G['samples']} (want: test Day 15 no; Day 18 16:00 yes; Day 20 19:30-21:00 yes; 19:00-20:15 yes; Day 21 05:00 yes; Friday 16:00 no)")
            if G['samples5'] != [False, False, False, False]: fail(f"{tag}: Step 5's holds {G['samples5']} (want all no: Day 23 05:00 in night 1, Day 16 08:15 the result, Day 22 23:00 night 1, Day 24 21:40 night 3)")
        elif G['samples'] != [False, True, False, True, False, False]: fail(f"{tag}: the guard's samples {G['samples']} (want: test Day 15 no; Day 18 16:00 yes; Day 20 19:30-21:00 no; 19:00-20:15 yes; the night shift Day 21 05:00 no; Friday 16:00 no)")
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
        say(f"  gathering {c['id']} D{c['day']} {c['at']}: {c['want']} mean to go, {c['went']} planned there, at most {c['peak']} at once ({c['peakAt']}){', dropping in for ' + str(c['stay'][0]) + '-' + str(c['stay'][1]) + ' min' if c['stay'] else ''}, {c['cap']} places ({c['seats']} seats{', seated only' if c['seated'] else ''}) in {c['rooms']}")
        if c['peak'] > c['cap']: fail(f"{tag}: {c['id']}: {c['peak']} there at once ({c['peakAt']}) for {c['cap']} places")
        if c['want'] > c['cap'] and not c['stay']: fail(f"{tag}: {c['id']}: {c['want']} mean to go for {c['cap']} places")   # one that drops in and out (stay) is judged by the most there at once
        if c['want'] > CROWD and not c['seated']: fail(f"{tag}: {c['id']}: a crowd of {c['want']}, over {CROWD}")   # seated sittings (staggered): no cap on meaning to go (lead 24); at once <= seats below
        if c['id'] == 'lanternSupper' and not c['seated']: fail(f"{tag}: the lantern supper isn't seated (the user's call: no standing at meals)")
        if c['seated']:   # seated sittings only (the user, the storm's lantern supper): never more at once than its seats, and no crowd spot
            if c['peak'] > c['seats']: fail(f"{tag}: {c['id']} (seated): {c['peak']} at once for {c['seats']} seats")
            if c.get('standing'): fail(f"{tag}: {c['id']} (seated): {len(c['standing'])} eat standing, no seat for their sitting: {c['standing'][:8]}")
            if c['crowd']: fail(f"{tag}: {c['id']} (seated) has {c['crowd']} standing crowd spots among its places")
        # (the old rule, a mess gathering over 44 needing standing places, is dropped: the user removed standing at meals)
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
    print('Switches:', 'EVENTS_ON (on in the build; a switched-off copy for parts 1-2)' if ON_ALREADY else 'EVENTS_ON (off)' if base else 'EVENTS_ON on already' if 'const EVENTS_ON = true;' in SRC else 'no EVENTS_ON', '|', ', '.join(s for s in ['EV_CAL_ON', 'EV_GUARD_ON', 'EV_NOTES_ON', 'EV_DEVICE_ON', 'EV_REPLAY_ON', 'EV_RANK_ON', 'EV_COMMS_ON'] if re.search(r'const ' + s + r' = ', SRC)) or 'no pieces')
    if not base and 'const EVENTS_ON = true;' not in SRC:
        print('  SKIP: no events base in this build (EVENTS_ON): nothing to check')
        print('BIGEVENTS CHECK OK (nothing built yet)'); sys.exit(0)

    # 1. off: today's game
    print('\n1. Switched off (the build as it is):')
    if ON_ALREADY: note('EVENTS_ON is on in this build: parts 1-2 run on a switched-off copy of it (EVENTS_ON = false), part 3 on the build as switched on')
    g = Game(pw, OFF_BUILD); a = paper(g, 'off'); show(a)
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
    if not a['sw']['EVENTS_ON'] and 'EV_LINE_ON' in SRC:   # the Line off: no Line in the menu, no ceremony, no venue
        lo = g.ev(r"""(() => { const S = schedData(), d = (EV_CALENDAR.find(x => x.id === 'crossingLine') || { day: 6 }).day + 1;
          return { d, menu: /Line/.test(JSON.stringify(galleyMenu(d))), cer: eventsOn(d).some(e => e.id === 'lineCeremony'),
            keys: [...S.shared.keys()].filter(k => /bow-lounge-line/.test(k)), places: [...S.byId.keys()].filter(k => /bow-lounge-line/.test(k)).length }; })()""")
        if lo['menu']: fail(f"off: the galley's menu for Day {lo['d']} mentions the Line")
        # the menu around the Line's day as it is, then with the Line's menu hook (linePudding) taken out, as a build with no
        # Line code: off, the two must match, pudding and note too (ER3's plant P4: a pudding set on Day 7 before the switch's test)
        mn = g.ev(r"""(() => { const d = (EV_CALENDAR.find(x => x.id === 'crossingLine') || { day: 6 }).day + 1, ds = [d - 1, d, d + 1];
          const read = () => { GALLEY_MENU.clear(); return ds.map(x => JSON.stringify(galleyMenu(x))); };
          const was = read(), keep = typeof linePudding === 'function' ? linePudding : null;
          if (keep) window.__sc('linePudding = () => {}'); const bare = read(); if (keep) { window.__keepLP = keep; window.__sc('linePudding = window.__keepLP'); } GALLEY_MENU.clear();
          return ds.map((x, i) => { if (was[i] === bare[i]) return null; const A = JSON.parse(was[i]), Z = JSON.parse(bare[i]);
            return 'Day ' + x + ': ' + [...new Set(Object.keys(A).concat(Object.keys(Z)))].filter(k => JSON.stringify(A[k]) !== JSON.stringify(Z[k])).map(k => k + ' ' + JSON.stringify(A[k]) + ', without the Line ' + JSON.stringify(Z[k])).join('; '); }).filter(Boolean); })()""")
        for m in mn: fail(f"off: the galley's menu differs from a build without the Line: {m[:300]}")
        if lo['cer']: fail(f"off: the Line's ceremony (lineCeremony) is on Day {lo['d']}")
        if lo['keys'] or lo['places']: fail(f"off: the Line's venue ('bow-lounge-line') is there: {lo['keys'][:4]}, {lo['places']} places")
    for e in g.errors[:3]: fail(f'off: page error: {e}')
    g.close()
    if not a['sw']['EVENTS_ON']: check_callin(pw, OFF_BUILD, 'off', False)
    if not a['sw']['EVENTS_ON']: check_notes(pw, OFF_BUILD, 'off', False)

    # 2. the calendar alone (EV_CAL_ON), then 3. everything on (EVENTS_ON)
    for n, tag, on, title in ([(2, 'calendar', ['EV_CAL_ON'], 'The calendar alone (EV_CAL_ON)')] if cal_alone else []) + [(3, 'on', 'all', 'Everything on (EVENTS_ON)')]:
        print(f'\n{n}. {title}:')
        g = Game(pw, variant(tag, on)); a = paper(g, tag); show(a); judge(a, tag); check_device(g, tag, on == 'all')
        if on == 'all' and g.ev("typeof SHIP_EVENTS.crossingLine !== 'undefined' && !SHIP_EVENTS.crossingLine.draft"): check_line(g, tag)
        for e in g.errors[:3]: fail(f'{tag}: page error: {e}')
        g.close()
        check_notes(pw, variant(tag, on), tag, on == 'all')
        if on == 'all': check_callin(pw, variant(tag, on), tag, True)

    # 3b. with Crossing the Line on (EV_LINE_ON; it follows EVENTS_ON from L6): everything again, and the Line's own cases
    if 'const EV_LINE_ON = false;' in SRC:
        print('\n3b. With Crossing the Line (EV_LINE_ON):')
        lsrc = SRC.replace('const EVENTS_ON = false;', 'const EVENTS_ON = true;', 1).replace('const EV_LINE_ON = false;', 'const EV_LINE_ON = EVENTS_ON;', 1)
        lp = WORK / 'test' / f'bigev_{RUN_ID}line.html'; lp.write_text(lsrc)
        g = Game(pw, str(lp)); a = paper(g, 'line'); show(a); judge(a, 'line'); check_device(g, 'line', True); check_line(g, 'line')
        for e in g.errors[:3]: fail(f'line: page error: {e}')
        g.close()
        check_callin(pw, str(lp), 'line', True)
    elif "SHIP_EVENTS.crossingLine" in SRC and 'EV_LINE_ON' in SRC:
        note('EV_LINE_ON already follows EVENTS_ON: the Line is checked in part 3')

    # 4. the self-test: each planted clash is caught
    print('\n4. Self-test (clashes planted in a copy):')
    g = Game(pw, variant('on', 'all')); dressed = g.ev(PLANT); dressedC = g.ev(PLANT_COMET); a = g.ev(PAPER); g.close()
    SINK = []; judge(a, 'planted'); caught, SINK = SINK, None
    for p in PLANTED + [dressed + ' ']:
        hit = [c for c in caught if p in c and (p != dressed + ' ' or 'during party' in c)]
        print(f"  {p}: " + ('caught: ' + hit[0] if hit else 'NOT caught'))
        if not hit: fail(f'the self-test: the planted {p} was not caught')
    if dressedC:
        hit = [c for c in caught if dressedC + ' ' in c and 'during cometLounge' in c]
        print(f"  {dressedC} in the comet's bow lounge: " + ('caught: ' + hit[0] if hit else 'NOT caught'))
        if not hit: fail(f'the self-test: the planted {dressedC} in the comet\'s bow lounge was not caught')

    # 5. late saves (F0c, OR1): the skip comes from SHIP.evFrom, the day the calendar was first on in this game, set
    # once and saved (ship.evFrom), never from the day a page loads. On paper, evSkippedFor for any day; then real saves
    # in the browser: evFrom 20 passes over the storm for good, evFrom 0 on Day 20 passes over nothing, a save with no
    # evFrom key loaded with the calendar on takes the day it loads and keeps it through a save and a reload; with the
    # calendar off, SHIP.evFrom is null and the save has no key
    print('\n5. Late saves:')
    if 'function evSkippedFor' not in SRC:
        waiting('evSkippedFor and SHIP.evFrom (F0c)')
    else:
        g = Game(pw, variant('on', 'all'))
        P5 = g.ev("""(() => {
          const want = (from, log, cur) => from == null || EV_LATE !== 'skip' ? [] : EV_CALENDAR.filter(r => r.day < from && !log.some(l => l.id === r.id) && !(cur && cur.id === r.id)).map(r => r.id);
          const cases = [[20, [], null], [9, [], null], [20, [{ id: 'ionStorm' }], null], [20, [], { id: 'ionStorm' }], [0, [], null], [1, [], null], [null, [], null], [40, [], null]];
          const plan = evCalPlan();
          return { evFrom: SHIP.evFrom, late: EV_LATE, cases: cases.map(([f, l, c]) => ({ f, l: l.map(x => x.id), c: c && c.id, got: evSkippedFor(f, l, c), want: want(f, l, c) })),
            plan, due: evCalDue(), days: plan.map(r => SHIP_EVENTS[r.id].days), bigs: plan.map(r => SHIP_EVENTS[r.id].phases.filter(p => ['onset', 'escalation', 'resolution'].includes(p.id)).map(p => r.day + p.at[0])),
            cal: EV_CALENDAR.filter(r => SHIP_EVENTS[r.id] && !SHIP_EVENTS[r.id].draft && !EV_SKIPPED.has(r.id)).map(r => r.id) };
        })()""")
        g.close()
        print(f"  a new page: SHIP.evFrom {P5['evFrom']}, EV_LATE {P5['late']}; the plan {P5['plan']}; due {P5['due']}")
        if P5['evFrom'] not in (0, 1): fail(f"a new game's SHIP.evFrom is {P5['evFrom']}, not 0 or 1 (its first day)")
        for c in P5['cases']:
            print(f"  evSkippedFor({c['f']}, log {c['l']}, running {c['c']}) = {c['got']}")
            if c['got'] != c['want']: fail(f"evSkippedFor({c['f']}, {c['l']}, {c['c']}) = {c['got']}, want {c['want']}")
        if P5['late'] == 'skip':
            named = {(20, ()): ['crossingLine', 'ionStorm'] + PAST, (9, ()): ['crossingLine'], (20, ('ionStorm',)): ['crossingLine'] + PAST, (0, ()): [], (1, ()): []}
            for c in P5['cases']:
                k = (c['f'], tuple(c['l']))
                if k in named and not c['c'] and c['got'] != named[k]: fail(f"evSkippedFor({c['f']}, {c['l']}): {c['got']}, the brief says {named[k]}")
        # the plan: built rows not passed over, in the calendar's order, each on or after its day, one at a time; due = its first
        if [r['id'] for r in P5['plan']] != P5['cal']: fail(f"evCalPlan lists {[r['id'] for r in P5['plan']]}, the calendar's built rows are {P5['cal']}")
        for x, y, n in zip(P5['plan'], P5['plan'][1:], P5['days']):
            if y['day'] < x['day'] + n: fail(f"evCalPlan: {y['id']} on Day {y['day']} before {x['id']} ends (Day {x['day'] + n - 1})")
        if P5['plan'] and P5['due'] != {'id': P5['plan'][0]['id'], 'day': P5['plan'][0]['day']}: fail(f"evCalDue {P5['due']} isn't the plan's first {P5['plan'][0]}")

        def load(b, path, save, reload=False, errs=None):
            pg = b.new_page(viewport={'width': 900, 'height': 760})
            pg.on('pageerror', lambda e: errs.append(str(e)))
            pg.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
            seed = "if (!sessionStorage.getItem('__bev')) { sessionStorage.setItem('__bev', '1'); localStorage.clear(); localStorage.setItem('starship-cadet-save', " + json.dumps(json.dumps(save)) + "); localStorage.setItem('starship-cadet-arrived', '1'); }"
            pg.add_init_script(INIT + "try { " + seed + " } catch (e) {}")
            pg.goto('file://' + str(path)); pg.wait_for_function('window.__sc !== undefined || window.__err', timeout=60000)
            return pg
        def state(pg):
            return pg.evaluate('s => window.__sc(s)', """(() => { const sk = [...EV_SKIPPED].sort(), ed = [...Array(61).keys()].filter(d => eventDay(d)), d0 = SHIP.time.day, due = evCalDue();
              SHIP.time.day = 3; const same = JSON.stringify([[...EV_SKIPPED].sort(), [...Array(61).keys()].filter(d => eventDay(d))]) === JSON.stringify([sk, ed]); SHIP.time.day = d0;
              return { day: d0, evFrom: SHIP.evFrom, sk, ed, due, same, log: SHIP.eventLog.map(l => l.id + ':' + l.startDay + '-' + l.endDay), ev: SHIP.event && SHIP.event.id + ':' + SHIP.event.startDay + ':' + SHIP.event.phase }; })()""")
        def saved_from(pg):
            return pg.evaluate('s => window.__sc(s)', "(() => { saveGame(); const s = JSON.parse(localStorage.getItem(SAVE_KEY) || '{}'); return s.ship && 'evFrom' in s.ship ? s.ship.evFrom : 'no key'; })()")
        def mk(day, log=None, frm='none'):
            ship = {'decks': {}, 'eventLog': log or []}
            if frm != 'none': ship['evFrom'] = frm
            return {'v': 2, 'build': 'x', 'time': {'day': day, 'min': 600}, 'player': {'deck': 4, 'tile': [7, 3], 'facing': 0}, 'ship': ship, 'crew': {}}
        on_html = WORK / 'test' / f'_run_bigev_{RUN_ID}late.html'; on_html.write_text(instrument(pathlib.Path(variant('late', 'all')).read_text()))
        off_html = WORK / 'test' / f'_run_bigev_{RUN_ID}lateoff.html'; off_html.write_text(instrument(SRC))
        errs = []
        b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
        storm = ['ionStorm'] if 'ionStorm' in P5['cal'] else []
        # from the game's own data, every planned event (EV5: the Line comes before the storm): its big days, and its span
        # in the log once a late load has caught it up (each one ended by Day 20)
        bigs = {r['id']: b for r, b in zip(P5['plan'], P5['bigs'])}
        big_but = lambda *skip: sorted({d for i, b in bigs.items() if i not in skip for d in b})
        later = next(({'id': r['id'], 'day': r['day']} for r in P5['plan'] if r['day'] > 22), None)   # a row after the comet (the ending's crossing back, Day 31, EN2): due once the comet's passed
        slog = [f"{r['id']}:{r['day']}-{r['day'] + n}" for r, n in zip(P5['plan'], P5['days']) if r['day'] + n <= 20]
        for title, save, want in [
            ('a Day 20 save, events first on at Day 20', mk(20, frm=20), {'evFrom': 20, 'sk': sorted(PAST + ['crossingLine', 'ionStorm']), 'ed': big_but('crossingLine', 'ionStorm', *PAST), 'due': {'id': 'comet', 'day': 22} if COMET_ON else None, 'log': []}),
            ('a Day 20 save, events on from the start (evFrom 0)', mk(20, frm=0), {'evFrom': 0, 'sk': [], 'ed': big_but(), 'due': {'id': 'comet', 'day': 22} if COMET_ON else None, 'log': slog}),   # every event it missed is run on load, as an unbroken game ran them
            ('a Day 9 save, events first on at Day 9', mk(9, frm=9), {'evFrom': 9, 'sk': ['crossingLine'], 'ed': big_but('crossingLine'), 'due': {'id': 'ionStorm', 'day': 11} if storm else None, 'log': []}),
            ('a Day 20 save, evFrom 20, the storm logged', mk(20, [{'id': 'ionStorm', 'startDay': 11, 'endDay': 17}], 20), {'evFrom': 20, 'sk': sorted(PAST + ['crossingLine']), 'ed': big_but('crossingLine', *PAST), 'due': {'id': 'comet', 'day': 22} if COMET_ON else None})] + ([('a Day 23 save, events first on at Day 23 (the comet passed over)', mk(23, frm=23), {'evFrom': 23, 'sk': sorted(['comet', 'crossingLine', 'ionStorm'] + (['diplomatic'] if SWAP else [])), 'due': later})] if COMET_ON else []) + ([
            ('a Day 27 save, events on from the start, the vessel first on at Day 27', mk(27, frm=0), {'evFrom': 0, 'sk': [], 'due': {'id': 'veyliVessel', 'day': 27}}),
            ('a Day 28 save, events on from the start, the vessel first on at Day 28 (passed over)', mk(28, frm=0), {'evFrom': 0, 'sk': ['veyliVessel'], 'due': next(({'id': r['id'], 'day': r['day']} for r in P5['plan'] if r['day'] > 28), None)})] if VESSEL_ON else []):   # the next row after the vessel (the ending's crossing back, Day 31, with EV_ENDING_ON)
            pg = load(b, on_html, save, errs=errs); r = state(pg); pg.close()
            print(f"  {title}: evFrom {r['evFrom']}, passes over {r['sk']}, eventDay {r['ed']}, due {r['due']}, log {r['log']}, running {r['ev']}")
            for k in ('evFrom', 'sk', 'ed', 'due', 'log'):
                if k in want and r[k] != want[k]: fail(f"{title}: {k} {r[k]}, want {want[k]}")
            if not r['same']: fail(f"{title}: what's passed over changed with the clock")
        # no evFrom key: takes the day it loads, kept through a save and a reload
        pg = load(b, on_html, mk(20), errs=errs); r1 = state(pg); k1 = saved_from(pg)
        pg.reload(); pg.wait_for_function('window.__sc !== undefined || window.__err', timeout=60000); r2 = state(pg); pg.close()
        print(f"  a Day 20 save with no evFrom: evFrom {r1['evFrom']} (saved {k1}), passes over {r1['sk']}; after a reload evFrom {r2['evFrom']}, passes over {r2['sk']}")
        if r1['evFrom'] != 20 or k1 != 20: fail(f"a save with no evFrom loaded on Day 20 should take evFrom 20 and save it: {r1['evFrom']}, saved {k1}")
        if (r2['evFrom'], r2['sk'], r2['ed']) != (r1['evFrom'], r1['sk'], r1['ed']): fail(f"after a save and a reload: evFrom {r2['evFrom']}, {r2['sk']}, eventDay {r2['ed']} (was {r1['evFrom']}, {r1['sk']}, {r1['ed']})")
        # the calendar off (the build as it is): no evFrom, and the save gains no key
        if 'const EVENTS_ON = false;' in SRC:
            pg = load(b, off_html, mk(20), errs=errs); ro = pg.evaluate('s => window.__sc(s)', 'SHIP.evFrom'); ko = saved_from(pg); pg.close()
            print(f"  switched off: SHIP.evFrom {ro}, saved {ko}")
            if ro is not None or ko != 'no key': fail(f"switched off, SHIP.evFrom should be null and the save have no evFrom key: {ro}, {ko}")
        b.close()
        for e in errs[:3]: fail(f'late saves: page error: {e}')

    # 6. live (F7b) and crowds (F7c): with F2-F4 and the storm update
    print('\n6. Live phases and crowds:')
    waiting('F7b (jumps, reloads mid-phase and mid-meeting) comes with F4 (the phase notes and the device are in parts 1-3); F7c (draw calls at about 60, phone size) with the storm update')

print('\nBIGEVENTS CHECK OK' if ok else '\nBIGEVENTS CHECK FAILED')
sys.exit(0 if ok else 1)
