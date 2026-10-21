# Starship Cadet: big events check (keep in the repo, next to events_check.py). Not in check_fast (lead 21's call).
# The ship-wide events (section 18, SHIP_EVENTS) by the events base (plans/events-base-brief.md, F7), driven by the data:
#   the switches: EVENTS_ON and each piece's line (EV_CAL_ON, EV_GUARD_ON, ...); the check builds copies of the game with
#   them switched on by text (the way day_check flips REC_TRAD_ON) and runs each part on the copy it needs;
#   off = today's game: eventDay never true, no beat moved by the hold, the party's hash key 340;
#   on paper (one page each, no frames stepped): the calendar's days (storm Day 11, its big days 12-14 = eventDay);
#   one main event at a time; every beat (phase, meeting, news, felt moment, job, gathering) at its time, none starting
#   in a Friday hold (15:30-17:00 from Day 5; a beat put there waits to 17:00); called-in crew on their day off
#   (eventCalledIn); gatherings fit their places (crowds about 60, the mess's 44 seats plus standing); no tradition in a
#   gathering's room while it's on, and the plan's clashes (talent night and Lap of the Wren off the party night, the
#   lap on Day 15 at 20:30); the career-beat guard (guardFree); the Captain's table on Day 20 19:00-20:15 on a night-
#   shift week; the same run twice is identical, and none of it reads the saved or live state;
#   late saves (in the browser): a Day 20 save passes over the storm for good, decided once at load.
# Each part skips (SKIP, or WAITING with what it waits for) while its switch or code isn't there yet, so it runs on
# today's integration and grows as the events base is built. Exits 1 on a FAIL.
# Setup and environment as for cadet_test.py.
# Run:  python3 bigevents_check.py BUILD.html
import sys, re, json, pathlib, os
exec(open(__file__.replace('bigevents_check.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright

SRC = pathlib.Path(sys.argv[1]).read_text()
SWITCHES = ['EV_CAL_ON', 'EV_GUARD_ON', 'EV_NOTES_ON', 'EV_DEVICE_ON', 'EV_REPLAY_ON', 'EV_RANK_ON', 'EV_COMMS_ON']
CROWD = 66                     # crowds up to about 60 (the user, events plan v3.2 answer 4): a tenth over is a FAIL
MESS_SEATS = 44

ok = True
def fail(msg):
    global ok
    ok = False
    print('  FAIL', msg)
def hhmm_py(m): m = int(m); return f'{m // 60 % 24:02d}:{m % 60:02d}'
def note(msg): print('  note:', msg)
def waiting(msg): print('  WAITING:', msg)

def variant(tag, on):
    # a copy of the game with these switches on: EVENTS_ON (on = None: as it is), or single pieces' lines alone
    src = SRC
    if on == 'all':
        src = src.replace('const EVENTS_ON = false;', 'const EVENTS_ON = true;', 1)
    else:
        for s in on: src = re.sub(r'const ' + s + r' = EVENTS_ON;', 'const ' + s + ' = true;', src, count=1)
    p = WORK / 'test' / f'bigev_{tag}.html'; p.write_text(src); return str(p)

# the events on paper: everything from the data and pure functions, nothing stepped. The saved and live state
# (SHIP.event, SHIP.eventLog, the clock) is set aside first and put back after
PAPER = r"""(() => {
  const keep = { e: SHIP.event, log: SHIP.eventLog.slice(), time: { ...SHIP.time } }; SHIP.event = null; SHIP.eventLog.length = 0;
  const has = n => { try { return typeof eval(n) !== 'undefined'; } catch (e) { return false; } };
  const ab = (d, m) => (d - 1) * 1440 + m, dm = t => { const d = Math.floor(t / 1440) + 1; return 'D' + d + ' ' + WEEKDAYS[weekday(d)].slice(0, 3) + ' ' + hhmm(t - (d - 1) * 1440); };
  const out = { sw: {}, cal: [], beats: [], gath: [], held: [], synth: null, due: null, chain: [], eventDay: [], called: [], calledStray: [], caps: [], clash: [], named: {}, captains: [], guard: null, table: null, late: null, notes: [] };
  for (const s of ['EVENTS_ON', 'EV_CAL_ON', 'EV_GUARD_ON', 'EV_NOTES_ON', 'EV_DEVICE_ON', 'EV_REPLAY_ON', 'EV_RANK_ON', 'EV_COMMS_ON']) out.sw[s] = has(s) ? eval(s) : null;
  const CAL = has('EV_CALENDAR') ? EV_CALENDAR : [], built = r => !!SHIP_EVENTS[r.id] && !SHIP_EVENTS[r.id].draft;
  const beatAt = has('evBeatAt') ? evBeatAt : (sd, at) => ab(sd + at[0], at[1]), heldAt = has('evHeld') ? evHeld : () => false;
  out.cal = CAL.map(r => ({ id: r.id, day: r.day, kind: r.kind, built: !!SHIP_EVENTS[r.id], draft: !!(SHIP_EVENTS[r.id] && SHIP_EVENTS[r.id].draft), skipped: has('EV_SKIPPED') && EV_SKIPPED.has(r.id) }));
  out.skipped = has('EV_SKIPPED') ? [...EV_SKIPPED] : null; out.late = has('EV_LATE') ? EV_LATE : null;
  // the Friday hold, minute by minute over five weeks (afternoons), and a beat put in it
  for (let d = 1; d <= 35; d++) for (let m = 840; m < 1140; m += 5) if (heldAt(ab(d, m))) out.held.push([d, m]);
  if (has('evBeatAt')) out.synth = [[5, 945], [12, 930], [12, 1019], [12, 1020], [12, 925], [11, 945]].map(([d, m]) => [d, m, evBeatAt(d, [0, m]) - ab(d, 0)]);
  // the beats of each event on the calendar, built ones (drafts too, marked: they're switched on later)
  for (const r of CAL) {
    const def = SHIP_EVENTS[r.id]; if (!def) continue;
    const sd = r.day, list = [];
    for (const p of def.phases) list.push(['phase', p.id, p.at]);
    for (const m of def.meetings || []) list.push(['meeting', m.id, m.at, m.len || 15, m.who, m.where]);
    for (const n of def.news || []) list.push(['news', n.id, n.at]);
    for (const mo of def.moments || []) if (!mo.gathering) list.push(['moment', mo.id, mo.at, mo.len]);
    for (const [ph, js] of Object.entries(def.jobs || {})) { const p = def.phases.find(x => x.id === ph); if (p) for (const j of js) list.push(['job', j.id, [p.at[0], j.at]]); }
    for (const b of list) {
      const raw = ab(sd + b[2][0], b[2][1]), t = beatAt(sd, b[2]);
      out.beats.push({ ev: r.id, draft: !built(r), what: b[0], id: b[1], raw, t, at: dm(t), rawHeld: heldAt(raw), held: heldAt(t), len: b[3] || 0, who: b[4] || null,
        deck: b[5] ? b[5].deck : null, room: b[5] && b[5].room ? b[5].room.source.replace(/^\^|\$$/g, '').replace(/\\/g, '').toLowerCase() : null, day: Math.floor(t / 1440) + 1 });
    }
  }
  // the gatherings made at load (EV_SHIPWIDE): their day and hours; not moved by the hold
  for (const g of (typeof EV_SHIPWIDE !== 'undefined' ? EV_SHIPWIDE : [])) {
    const r = CAL.find(x => x.id === g.when.ship), sd = r ? r.day : null;
    out.gath.push({ id: g.id, ev: g.when.ship, k: g.k, day: sd != null ? sd + g.when.day : null, at: g.at, held: sd != null && (heldAt(ab(sd + g.when.day, g.at[0])) || heldAt(ab(sd + g.when.day, g.at[1] - 1))), rooms: evRooms(g), draft: !r || !built(r) });
  }
  // the due day, and the calendar played forward on paper (each event logged as run; one at a time)
  const dueOf = () => { const x = eventDueDay(); return x ? { id: x.id, day: x.day } : null; };
  out.due = dueOf();
  for (let k = 0, x = out.due; x && k < 8; k++, x = dueOf()) { const def = SHIP_EVENTS[x.id]; out.chain.push({ id: x.id, day: x.day, end: x.day + def.days }); SHIP.eventLog.push({ id: x.id, startDay: x.day, endDay: x.day + def.days, band: 'bumpy', threads: {}, mine: {} }); }
  SHIP.eventLog.length = 0;
  // eventDay: the big days, and the same whatever the saved or live state says
  const eday = () => has('eventDay') ? [...Array(61).keys()].filter(d => eventDay(d)) : null;
  out.eventDay = eday();
  SHIP.event = { id: 'ionStorm', startDay: 3, phase: 'onset', threads: {}, mine: {} }; SHIP.eventLog.push({ id: 'ionStorm', startDay: 2, endDay: 8, band: 'rough', threads: {}, mine: {} }); SHIP.time.day = 25;
  out.eventDayLive = eday(); out.skippedLive = has('EV_SKIPPED') ? [...EV_SKIPPED] : null;
  out.beatsLive = out.beats.map(b => beatAt(CAL.find(r => r.id === b.ev).day, [Math.floor((b.raw) / 1440) + 1 - CAL.find(r => r.id === b.ev).day, b.raw % 1440]));
  SHIP.event = null; SHIP.eventLog.length = 0; SHIP.time.day = keep.time.day; SHIP.time.min = keep.time.min;
  // called in on a day off (F0b): each meeting's named crew; and nobody else called in on those days
  const people = schedPeople(), pById = id => people.find(p => p.id === id);
  for (const b of out.beats.filter(b => b.what === 'meeting' && !b.draft && Array.isArray(b.who))) for (const id of b.who) {
    const p = pById(id); if (!p) continue;
    const off = !isWorkDay(p, b.day), c = has('eventCalledIn') ? !!eventCalledIn(p, b.day) : null;
    const seg = planDay(p, b.day).find(s => s.from <= b.t && b.t < s.to);
    const pl = seg && seg.placeId && schedData().byId.get(seg.placeId), rm = pl && DECKS[pl.deck] && DECKS[pl.deck].rooms && DECKS[pl.deck].rooms[pl.room];
    const there = !!seg && seg.deck === b.deck && !!rm && (!b.room || (rm.name || '').toLowerCase() === b.room);
    out.called.push({ meet: b.id, day: b.day, at: b.at, id, off, called: c, deck: seg ? seg.deck : null, act: seg ? seg.act : null, place: seg ? seg.placeId || null : null, roomName: rm ? rm.name : null, want: b.deck, wantRoom: b.room, there });
  }
  if (has('eventCalledIn')) for (const d of [...new Set(out.beats.filter(b => !b.draft).map(b => b.day))])
    for (const p of people) if (eventCalledIn(p, d) && !out.called.some(c => c.day === d && c.id === p.id)) out.calledStray.push(d + ' ' + p.id);
  // the gatherings on their day: who means to go, who's planned there, and how many places
  const S = schedData();
  for (const g of out.gath.filter(g => !g.draft && g.day)) {
    const e = eventsOn(g.day).find(x => x.id === g.id); if (!e) { out.caps.push({ id: g.id, day: g.day, missing: true }); continue; }
    const want = people.filter(p => eventPlan(p, g.day).some(x => x.id === g.id)).length;
    const went = people.filter(p => planDay(p, g.day).some(s => s.tag && (s.tag === 'ev-' + g.id || s.tag.startsWith('ev-' + g.id + '-')))).length;
    const pls = e.ev.where.flatMap((w, i) => S.shared.get(w.deck + '|' + (w.room ? 'ev:' + e.id + ':' + i : w.pool)) || []);
    const cap = new Set(pls.map(pl => pl.id)).size, seats = new Set(pls.filter(pl => /seat|chair|bench|stool|sofa/.test(pl.type)).map(pl => pl.id)).size;
    out.caps.push({ id: g.id, day: g.day, at: hhmm(e.from) + '-' + hhmm(e.to), want, went, cap, seats, rooms: g.rooms, mess: g.rooms.some(r => /mess/.test(r)) });
  }
  // traditions in a gathering's or meeting's room while it's on; and every tradition on the events' days, for the plan's list
  const evDays = [...new Set(out.beats.filter(b => !b.draft).map(b => b.day).concat(out.gath.filter(g => !g.draft && g.day).map(g => g.day)))].sort((a, b) => a - b);
  const span = []; for (const r of CAL.filter(built)) for (let d = r.day; d < r.day + SHIP_EVENTS[r.id].days + 1; d++) span.push(d);
  for (const d of [...new Set(span.concat(evDays))]) out.named[d] = eventsOn(d).filter(e => SHIP_TRADITIONS.includes(e.ev)).map(e => [e.id, e.from, e.to]);
  const things = out.gath.filter(g => !g.draft && g.day).map(g => ({ id: g.id, day: g.day, from: g.at[0], to: g.at[1], rooms: g.rooms }))
    .concat(out.beats.filter(b => b.what === 'meeting' && !b.draft && b.room).map(b => ({ id: b.id, day: b.day, from: b.t - ab(b.day, 0), to: b.t - ab(b.day, 0) + b.len, rooms: [b.deck + '|' + b.room] })));
  for (const x of things) for (const e of eventsOn(x.day).filter(e => SHIP_TRADITIONS.includes(e.ev))) {
    const rooms = evRooms(e.ev); if (e.from < x.to && x.from < e.to && rooms.some(r => x.rooms.includes(r))) out.clash.push('D' + x.day + ' ' + e.id + ' ' + hhmm(e.from) + '-' + hhmm(e.to) + ' in ' + rooms.join(',') + ' during ' + x.id + ' ' + hhmm(x.from) + '-' + hhmm(x.to));
  }
  // the Captain's scenes: meetings she's named in, a day at a time
  const cap = {}; for (const b of out.beats.filter(b => b.what === 'meeting' && !b.draft && Array.isArray(b.who) && b.who.includes('marrow'))) (cap[b.day] = cap[b.day] || []).push(b.id + ' ' + b.at);
  out.captains = cap;
  // the career-beat guard (F1b)
  if (has('guardFree')) {
    const G = { rows: EV_BEATS.map(b => ({ ...b })), probes: [] };
    for (const b of EV_BEATS) {
      const days = b.days ? [...Array(b.days[1] - b.days[0] + 1).keys()].map(k => b.days[0] + k) : b.day != null ? [b.day] : [...Array(35).keys()].map(k => k + 1).filter(d => (b.weekday == null || weekday(d) === b.weekday) && (b.fromDay == null || d >= b.fromDay));
      for (const d of days.slice(0, 6)) if (b.at) G.probes.push({ id: b.id, kind: b.kind, d, from: b.at[0], to: b.at[1], free: guardFree(d, b.at[0], b.at[1], 'captain') });
    }
    G.free = [[8, 600, 630], [9, 1200, 1230]].map(([d, a, z]) => ({ d, a, z, free: guardFree(d, a, z, 'event') }));
    out.guard = G;
  }
  // the Captain's table (F1c)
  if (has('occasionSlot')) out.table = { slot: occasionSlot('captainsTable', 20), night: has('EV_BEATS') && EV_BEATS.some(b => b.kind === 'night' && (b.day === 20 || (b.days && b.days[0] <= 20 && 20 <= b.days[1]))) };
  else if (typeof OCCASIONS !== 'undefined' && OCCASIONS.captainsTable) out.table = { today: [OCCASIONS.captainsTable.at, OCCASIONS.captainsTable.len] };
  out.stormNew = !!(SHIP_EVENTS.ionStorm && (SHIP_EVENTS.ionStorm.meetings || []).some(m => m.id === 'stormBriefing' && m.at[1] === 840));
  SHIP.event = keep.e; SHIP.eventLog.length = 0; SHIP.eventLog.push(...keep.log); Object.assign(SHIP.time, keep.time);
  return out;
})()"""

def paper(g, tag):
    a = g.ev(PAPER); b = g.ev(PAPER)
    if json.dumps(a, sort_keys=True) != json.dumps(b, sort_keys=True): fail(f'{tag}: the events on paper came out differently the second time')
    return a

def show(a):
    print('  calendar:', ', '.join(f"{r['id']} D{r['day']} {r['kind']}{'' if r['built'] else ' (not built)'}{' (draft)' if r['draft'] else ''}{' (skipped)' if r['skipped'] else ''}" for r in a['cal']))
    print('  due:', a['due'], '| played forward:', ', '.join(f"{c['id']} D{c['day']}-{c['end'] - 1}" for c in a['chain']))
    print('  eventDay:', a['eventDay'])
    for b in a['beats']:
        if b['what'] in ('phase', 'meeting', 'moment'): print(f"    {b['ev']}{' (draft)' if b['draft'] else ''} {b['what']} {b['id']} {b['at']}{' (moved from ' + str(b['raw']) + ')' if b['raw'] != b['t'] else ''}")

def check_hold(a, tag, on):
    # the Friday hold: Fridays from Day 5, 15:30-17:00, nothing else
    want = [[d, m] for d in range(1, 36) for m in range(840, 1140, 5) if (d - 1) % 7 == 4 and d >= 5 and 930 <= m < 1020]
    if a['sw']['EV_CAL_ON'] is None: return
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
        if x['held']: (note if x['draft'] else fail)(f"{tag}: gathering {x['id']} (D{x['day']} {x['at']}) is in the Friday hold (gatherings aren't moved)")

with sync_playwright() as pw:
    # 0. the switches
    have = {s: bool(re.search(r'const ' + s + r' = EVENTS_ON;', SRC)) for s in SWITCHES}
    base = 'const EVENTS_ON = false;' in SRC
    print('Switches:', 'EVENTS_ON' if base else 'no EVENTS_ON line (or already on)', '|', ', '.join(s for s, v in have.items() if v) or 'no pieces')
    if not base and 'const EVENTS_ON = true;' not in SRC:
        print('  SKIP: no events base in this build (EVENTS_ON): nothing to check')
        print('BIGEVENTS CHECK OK (nothing built yet)'); sys.exit(0)

    # 1. off: today's game
    print('\n1. Switched off (the build as it is):')
    g = Game(pw, sys.argv[1]); a = paper(g, 'off'); show(a)
    if a['sw']['EVENTS_ON']: note('EVENTS_ON is already on in this build: part 1 checks the build as it is')
    else:
        if a['eventDay'] is not None and a['eventDay']: fail(f"off: eventDay is true on {a['eventDay']}")
        moved = [b for b in a['beats'] if b['raw'] != b['t']]
        if moved: fail(f"off: beats moved by the hold: {[(b['id'], b['at']) for b in moved][:5]}")
        if a['skipped']: fail(f"off: a new game passes over {a['skipped']}")
    party = [x for x in a['gath'] if x['id'] == 'party']
    if party and party[0]['k'] != 340: fail(f"the party's hash key is {party[0]['k']}, not 340")
    ks = [x['k'] for x in a['gath']]
    if len(ks) != len(set(ks)): fail(f'two ship-wide gatherings share a hash key: {ks}')
    trk = g.ev("SHIP_TRADITIONS.map(e => e.k)")
    if set(ks) & set(trk): fail(f'a ship-wide gathering shares a hash key with a tradition: {sorted(set(ks) & set(trk))}')
    check_hold(a, 'off', False)
    g.close()

    # 2. the calendar alone (EV_CAL_ON), then 3. everything on (EVENTS_ON)
    runs = []
    if have['EV_CAL_ON']: runs.append(('calendar', ['EV_CAL_ON']))
    runs.append(('on', 'all'))
    for tag, on in runs:
        print(f"\n{2 if tag == 'calendar' else 3}. {'The calendar alone (EV_CAL_ON)' if tag == 'calendar' else 'Everything on (EVENTS_ON)'}:")
        g = Game(pw, variant(tag, on)); a = paper(g, tag); show(a)
        cal_on = bool(a['sw']['EV_CAL_ON']); guard_on = bool(a['sw']['EV_GUARD_ON'])
        if not cal_on: print('  SKIP: the calendar is off in this copy'); g.close(); continue
        built = [r for r in a['cal'] if r['built'] and not r['draft']]
        # the calendar's days and the due day
        days = {r['id']: r['day'] for r in a['cal']}
        if days.get('ionStorm') != 11: fail(f"{tag}: the storm's calendar day is {days.get('ionStorm')}, not 11")
        first = next((r for r in a['cal'] if r['built'] and not r['draft'] and not r['skipped']), None)
        if first and (not a['due'] or a['due'] != {'id': first['id'], 'day': first['day']}): fail(f"{tag}: due {a['due']}, not {first['id']} on Day {first['day']}")
        if [c['id'] for c in a['chain']] != [r['id'] for r in built if not r['skipped']]: fail(f"{tag}: the calendar played forward: {a['chain']} (want {[r['id'] for r in built]})")
        for x, y in zip(a['chain'], a['chain'][1:]):
            if y['day'] < x['end']: fail(f"{tag}: {y['id']} starts Day {y['day']} before {x['id']} ends (Day {x['end'] - 1})")
        mains = sorted([(r['day'], r['day'] + g.ev(f"SHIP_EVENTS['{r['id']}'].days"), r['id'], r['draft']) for r in a['cal'] if r['built'] and r['kind'] == 'main'])
        for x, y in zip(mains, mains[1:]):
            if y[0] < x[1]: (note if x[3] or y[3] else fail)(f"{tag}: main events overlap on the calendar: {x[2]} D{x[0]}-{x[1] - 1} and {y[2]} from D{y[0]}")
        # the storm's skeleton: the warning Day 11, the front Friday Day 12 14:00, the big days 12-14
        ph = {b['id']: b for b in a['beats'] if b['ev'] == 'ionStorm' and b['what'] == 'phase'}
        if ph:
            if ph['warning']['day'] != 11: fail(f"{tag}: the storm's warning is {ph['warning']['at']}, not Day 11")
            if ph.get('onset') and ph['onset']['at'] != 'D12 Fri 14:00': fail(f"{tag}: the front is {ph['onset']['at']}, not D12 Fri 14:00")
            if ph.get('resolution') and ph['resolution']['day'] != 14: fail(f"{tag}: the all-clear is {ph['resolution']['at']}, not Day 14")
        if guard_on and a['eventDay'] is not None:
            want = sorted({b['day'] for b in a['beats'] if b['what'] == 'phase' and not b['draft'] and b['id'] in ('onset', 'escalation', 'resolution')})
            if a['eventDay'] != want: fail(f"{tag}: eventDay is true on {a['eventDay']}, want {want} (the front, the escalation and the all-clear)")
            if 'ionStorm' in days and a['eventDay'][:3] != [12, 13, 14]: fail(f"{tag}: the storm's eventDays are {a['eventDay']}, not 12-14")
        elif a['eventDay'] is None: waiting('eventDay (F1a)')
        if a['eventDayLive'] != a['eventDay']: fail(f"{tag}: eventDay changed with the saved/live state: {a['eventDay']} -> {a['eventDayLive']}")
        if a['skippedLive'] != a['skipped']: fail(f"{tag}: the passed-over events changed after load: {a['skipped']} -> {a['skippedLive']}")
        if [b['t'] for b in a['beats']] != a['beatsLive']: fail(f"{tag}: a beat's time changed with the saved/live state")
        if a['skipped']: fail(f"{tag}: a new game passes over {a['skipped']}")
        check_hold(a, tag, True)
        # Day 11 with today's storm hours (OR1: expected until the storm update; noted, not failed)
        if not a['stormNew']:
            d11 = [b for b in a['beats'] if b['ev'] == 'ionStorm' and b['day'] == 11]
            note(f"{tag}: Day 11 has today's storm hours (the storm update gives the new ones): " + ', '.join(f"{b['what']} {b['id']} {b['at'][-5:]}" for b in d11))
        # called in on a day off (F0b)
        if a['sw'].get('EVENTS_ON') or tag == 'on':
            for c in a['called']:
                if c['called'] is not None and c['called'] != c['off']: fail(f"{tag}: {c['id']} at {c['meet']} D{c['day']}: {'off' if c['off'] else 'on shift'} but called in = {c['called']}")
                if not c['there']: (fail if c['called'] is not None else waiting)(f"{tag}: {c['id']} ({'off' if c['off'] else 'on shift'}) isn't planned at {c['meet']} ({c['at']}, Deck {c['want']} {c['wantRoom']}): {c['act']} at {c['place']} ({c['roomName']}, Deck {c['deck']}){'' if c['called'] is not None else ' (F0b brings them)'}")
            print('  called in:', ', '.join(f"{c['id']}@{c['meet']} D{c['day']}" for c in a['called'] if c['off']) or 'nobody', '' if any(c['called'] is not None for c in a['called']) else '(eventCalledIn not built: marks not checked)')
            if not any(c['called'] is not None for c in a['called']): waiting('eventCalledIn (F0b)')
            for x in a['calledStray']: fail(f"{tag}: called in but named in no meeting: {x}")
        # the gatherings fit their places
        for c in a['caps']:
            if c.get('missing'): fail(f"{tag}: gathering {c['id']} isn't on Day {c['day']}"); continue
            print(f"  gathering {c['id']} D{c['day']} {c['at']}: {c['want']} mean to go, {c['went']} planned there, {c['cap']} places ({c['seats']} seats) in {c['rooms']}")
            if c['want'] > c['cap'] or c['went'] > c['cap']: fail(f"{tag}: {c['id']}: {max(c['want'], c['went'])} people for {c['cap']} places")
            if c['want'] > CROWD: fail(f"{tag}: {c['id']}: a crowd of {c['want']}, over about 60")
            if c['mess'] and c['want'] > MESS_SEATS and c['cap'] - c['seats'] < c['want'] - MESS_SEATS: fail(f"{tag}: {c['id']} in the mess: {c['want']} people, {c['seats']} seats and too few standing places")
            if c['went'] < c['want']: note(f"{c['id']}: {c['want'] - c['went']} meant to go but aren't planned there")
        # no tradition in a gathering's or meeting's room while it's on; the Captain's scenes one a day
        for x in a['clash']: fail(f"{tag}: {x}")
        for d, l in a['captains'].items():
            if len(l) > 1: fail(f"{tag}: two of the Captain's scenes on Day {d}: {l}")
        # the plan's clashes (events plan v3.2): with the storm's new hours
        sd = days.get('ionStorm'); party = next((x for x in a['gath'] if x['id'] == 'party'), None)
        if sd and party and party['day']:
            pd = str(party['day']); on_pd = {e[0]: e for e in a['named'].get(pd, [])}; l15 = {e[0]: e for e in a['named'].get(str(party['day'] + 1), [])}
            probs = [f"{i} on the party night (D{pd} {hhmm_py(on_pd[i][1])})" for i in ('rec-talent-night', 'lap-of-the-wren') if i in on_pd and on_pd[i][1] < party['at'][1] and party['at'][0] < on_pd[i][2]]
            if 'lap-of-the-wren' not in l15 or l15['lap-of-the-wren'][1] != 1230: probs.append(f"Lap of the Wren not on D{party['day'] + 1} at 20:30 ({l15.get('lap-of-the-wren')})")
            if probs: (fail if a['stormNew'] else waiting)(f"{tag}: the plan's clashes{'' if a['stormNew'] else ' (the storm update moves them)'}: " + '; '.join(probs))
        print('  traditions by day:', '; '.join(f"D{d}: " + ', '.join(f"{e[0]} {hhmm_py(e[1])}" for e in l) for d, l in sorted(a['named'].items(), key=lambda x: int(x[0]))))
        # the career-beat guard (F1b) and the Captain's table (F1c)
        if a['guard']:
            for p in a['guard']['probes']:
                if p['free']: fail(f"{tag}: guardFree says a Captain's scene may go in {p['id']} ({p['kind']}) D{p['d']} {hhmm_py(p['from'])}-{hhmm_py(p['to'])}")
            for p in a['guard']['free']:
                if not p['free']: note(f"guardFree: D{p['d']} {hhmm_py(p['a'])} isn't free (a beat there?)")
            for b in [b for b in a['beats'] if not b['draft'] and b['what'] in ('phase', 'meeting', 'moment')]:
                if g.ev(f"guardFree({b['day']}, {b['t'] % 1440}, {b['t'] % 1440 + max(1, b['len'])}, 'event')") is False: fail(f"{tag}: {b['ev']} {b['what']} {b['id']} {b['at']} is in a guarded hour")
        elif guard_on: waiting('guardFree and the career beats in EV_BEATS (F1b)')
        t = a['table']
        if t and 'slot' in t:
            s = t['slot']; print('  the Captain\'s table Day 20:', s, '(a night-shift week)' if t['night'] else '')
            if t['night'] and (not s or s['at'] != 1140 or s['at'] + s['len'] > 1215): fail(f"{tag}: the Captain's table on Day 20 on a night-shift week is {s}, not 19:00 ending by 20:15")
        elif t: waiting(f"the Captain's table's hours by the guard (F1c occasionSlot); today {hhmm_py(t['today'][0])} for {t['today'][1]} min")
        g.close()

    # 4. late saves (in the browser): a save made on Day 20 before events were on passes over the storm for good;
    # a Day 9 save keeps it; one that already ran it doesn't pass it over; decided once, at load
    print('\n4. Late saves:')
    path = variant('late', 'all')
    if 'EV_SKIPPED' not in SRC: waiting('EV_SKIPPED (F0a)')
    else:
        html = instrument(pathlib.Path(path).read_text()); tmp = WORK / 'test' / '_run_bigev_late.html'; tmp.write_text(html)
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
            ev = lambda s: pg.evaluate('s => window.__sc(s)', s)
            r = ev("""(() => { const sk = [...EV_SKIPPED], due = evCalDue(), ed = [...Array(31).keys()].filter(d => eventDay(d)), d0 = SHIP.time.day;
              SHIP.time.day = 3; const sk2 = [...EV_SKIPPED], ed2 = [...Array(31).keys()].filter(d => eventDay(d)); SHIP.time.day = d0;
              return { day: d0, loadDay: EV_LOAD_DAY, log: SHIP.eventLog.map(l => l.id), sk, due, ed, same: JSON.stringify([sk, ed]) === JSON.stringify([sk2, ed2]) }; })()""")
            pg.close()
            print(f"  a Day {day} save{' (storm logged)' if log else ''}: loaded on Day {r['day']}, passes over {r['sk']}, due {r['due']}, eventDay {r['ed']}")
            if r['day'] != day: fail(f"the Day {day} save loaded on Day {r['day']}"); continue
            if sorted(r['sk']) != sorted(want['skip']): fail(f"a Day {day} save should pass over {sorted(want['skip'])}: {r['sk']}")
            if r['due'] != want['due']: fail(f"a Day {day} save: due {r['due']}, want {want['due']} (the visit is still a draft)")
            if not r['same']: fail(f"a Day {day} save: what's passed over changed after load")
            if day == 20 and not log and r['ed']: fail(f"a Day 20 save (storm passed over) still has eventDays {r['ed']}")
        b.close()
        for e in errs[:3]: fail(f'page error: {e}')

    # 5. live (F7b) and crowds (F7c): with F2-F4 and the storm update
    print('\n5. Live phases and crowds:')
    waiting('F7b (jumps, reloads mid-phase, phase notes to a reaction line, the device) comes with F2-F4; F7c (draw calls at 60) with the storm update')

print('\nBIGEVENTS CHECK OK' if ok else '\nBIGEVENTS CHECK FAILED')
sys.exit(0 if ok else 1)
