# Starship Cadet: the ship-wide events check (the events base, F7; keep in the repo, next to events_check.py)
# Driven by the game's own data (section 18's SHIP_EVENTS, EV_CALENDAR, EV_BEATS), so a new event is checked as soon as
# it's in the calendar. F7a, on paper (no deck drawn), with the events base switched on (EVENTS_ON flipped in a copy):
#   each built event is due on its calendar day; its phases begin at their minutes, in order, on their days;
#   nothing of an event begins in a held hour (the Friday address, 15:30-17:00 from Day 5): no phase, meeting or
#   gathering (EV_SHIPWIDE), and a beat moved by the hold lands at its end;
#   one event at a time: no two built events' days overlap; eventDay(d) only on the onset, escalation and all-clear days;
#   the career-beat guard: every meeting and gathering keeps clear of the beats' hours (its own beat aside), at most one
#   Captain's scene a day, none on a test day or across a night shift;
#   the meetings' casts are on shift that day, or (once F0b is in) marked called in; the same run twice is identical.
# And with the switch off (the build as it is): no calendar, no hold, no guard (eventDay false, guardFree true).
# Setup and environment as for cadet_test.py (three.js in $CADET_WORK/three, CADET_CHROME a Chromium).
# Run:  python3 bigevents_check.py BUILD.html
import sys, pathlib, json
exec(open(__file__.replace('bigevents_check.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright

ON_LINE = 'const EVENTS_ON = false;'
src = pathlib.Path(sys.argv[1]).read_text()
if ON_LINE not in src:
    print('no events base in this build (no "' + ON_LINE + '")'); print('BIGEVENTS CHECK FAILED'); sys.exit(1)
on_path = WORK / 'test' / ('_bigev_on_' + pathlib.Path(sys.argv[1]).name)
on_path.write_text(src.replace(ON_LINE, 'const EVENTS_ON = true;', 1))

# everything on paper, in the game's scope: one plain record of what the events would do in a new game, Days 0-40
PAPER = r"""(() => {
  const H = t => { const d = Math.floor(t / 1440) + 1; return 'Day ' + d + ' ' + hhmm(t - (d - 1) * 1440); };
  const out = { events: [], held: [], guard: [], cast: [], overlap: [], eventDays: [], notes: [] };
  const rows = EV_CALENDAR.filter(r => SHIP_EVENTS[r.id] && !SHIP_EVENTS[r.id].draft && !EV_SKIPPED.has(r.id));
  out.due = eventDueDay();
  for (const r of rows) {
    const def = SHIP_EVENTS[r.id], ev = { id: r.id, day: r.day, days: def.days, phases: [], scan: [] };
    for (const p of def.phases) {
      const raw = (r.day - 1 + p.at[0]) * 1440 + p.at[1], at = evBeatAt(r.day, p.at);
      ev.phases.push({ id: p.id, at, when: H(at), moved: at !== raw });
      if (evHeld(raw) && at !== evHeldEnd(raw)) out.held.push(r.id + ' phase ' + p.id + ' at ' + H(raw) + ' moved to ' + H(at));
    }
    // eventNow minute by minute through the event (as a new game sees it: nothing running, nothing logged)
    let last = null;
    for (let t = (r.day - 1) * 1440; t < (r.day - 1 + def.days) * 1440; t++) {
      const n = eventNow(t), k = n ? n.id + ':' + n.phase : '-';
      if (k !== last) { ev.scan.push([k, t]); last = k; }
    }
    for (const m of def.meetings || []) {
      const at = evBeatAt(r.day, m.at), d = Math.floor(at / 1440) + 1, from = at - (d - 1) * 1440, len = m.len || 15;
      if (evHeld(at)) out.held.push(r.id + ' meeting ' + m.id + ' begins in a held hour, ' + H(at));
      const own = EV_BEATS.filter(b => b.day === d && from < b.at[1] && from + len > b.at[0] && b.id !== m.beat);
      const ok = guardFree(d, from, from + len, 'beat') || own.every(b => b.kind === 'captain' && b.day === d && Math.abs(b.at[0] - from) <= 15);
      out.guard.push({ what: r.id + ' meeting ' + m.id, when: H(at), ok, beats: own.map(b => b.id) });
      for (const w of [].concat(m.who || [])) {
        if (typeof w !== 'string' || /:/.test(w)) continue;
        const p = schedPeople().find(q => q.id === w); if (!p) { out.cast.push({ what: m.id, who: w, day: d, state: 'not aboard' }); continue; }
        const on = isWorkDay(p, d), called = typeof eventCalledIn === 'function' ? !!eventCalledIn(p, d) : null;
        out.cast.push({ what: m.id, who: w, day: d, state: on ? 'on shift' : called ? 'called in' : called === null ? 'off (called in comes with F0b)' : 'off, not marked' });
      }
    }
    out.events.push(ev);
  }
  for (const g of EV_SHIPWIDE) {
    const r = rows.find(x => x.id === g.when.ship); if (!r) continue;
    const at = (r.day - 1 + g.when.day) * 1440 + g.at[0], d = Math.floor(at / 1440) + 1;
    if (evHeld(at)) out.held.push('gathering ' + g.id + ' begins in a held hour, ' + H(at));
    out.guard.push({ what: 'gathering ' + g.id, when: H(at), ok: guardFree(d, g.at[0], g.at[1], 'beat'), beats: evBeatsOn(d).filter(b => g.at[0] < b.to && g.at[1] > b.from).map(b => b.id) });
    out.notes.push('gathering ' + g.id + ' k ' + g.k + ' ' + H(at));
  }
  for (let i = 0; i < rows.length; i++) for (let j = i + 1; j < rows.length; j++) {
    const a = rows[i], b = rows[j], ae = a.day + SHIP_EVENTS[a.id].days, be = b.day + SHIP_EVENTS[b.id].days;
    if (a.day < be && b.day < ae) out.overlap.push(a.id + ' (Days ' + a.day + '-' + (ae - 1) + ') and ' + b.id + ' (Days ' + b.day + '-' + (be - 1) + ')');
  }
  for (let d = 0; d <= 40; d++) if (eventDay(d)) out.eventDays.push(d);
  out.bigDays = rows.flatMap(r => SHIP_EVENTS[r.id].phases.filter(p => EV_BIG_PHASES.includes(p.id)).map(p => r.day + p.at[0])).filter((d, i, a) => a.indexOf(d) === i).sort((x, y) => x - y);
  // the guard's own rules, read from EV_BEATS: a Captain's scene never on a test day, never two in a day
  out.captainDays = {}; for (const b of EV_BEATS) if (b.kind === 'captain') out.captainDays[b.day] = (out.captainDays[b.day] || 0) + 1;
  out.testDays = EV_BEATS.filter(b => b.kind === 'test').map(b => b.day);
  out.holdSamples = [[11 * 1440 + 960, evHeldEnd(11 * 1440 + 960)], [4 * 1440 + 930, evHeldEnd(4 * 1440 + 930)], [3 * 1440 + 960, evHeldEnd(3 * 1440 + 960)], [11 * 1440 + 840, evHeldEnd(11 * 1440 + 840)]];
  out.guardSamples = [guardFree(15, 600, 625, 'captain'), guardFree(18, 960, 985, 'captain'), guardFree(20, 1170, 1260, 'captain'), guardFree(20, 1140, 1215, 'captain'), guardFree(21, 300, 330, 'beat')];
  return out;
})()"""

OFF = r"""(() => ({ on: EVENTS_ON, eventDay: [...Array(41).keys()].filter(d => eventDay(d)), guard: [guardFree(15, 600, 625, 'captain'), guardFree(12, 960, 990, 'beat'), guardFree(21, 300, 330, 'beat')],
  hold: evBeatAt(12, [0, 960]) === 11 * 1440 + 960, at: evBeatAt(11, [1, 840]) === 11 * 1440 + 840 }))()"""

ok = True
def fail(msg):
    global ok
    ok = False
    print('FAIL', msg)

with sync_playwright() as pw:
    runs = []
    for k in range(2):
        g = Game(pw, str(on_path), 390, 844)
        runs.append(g.ev(PAPER)); errs = g.errors[:5]; g.b.close()
        if errs: fail('page errors (on): ' + ' | '.join(errs))
    g = Game(pw, sys.argv[1], 390, 844); off = g.ev(OFF); errs = g.errors[:5]; g.b.close()
    if errs: fail('page errors (off): ' + ' | '.join(errs))

P = runs[0]
print('switched on: due', P['due'])
for ev in P['events']:
    print(' ', ev['id'], 'from Day', ev['day'], 'for', ev['days'], 'days:', ', '.join(p['id'] + ' ' + p['when'] + (' (held, moved)' if p['moved'] else '') for p in ev['phases']))
    seen = [k for k, t in ev['scan'] if k != '-']
    want = [ev['id'] + ':' + p['id'] for p in ev['phases']]
    if seen != want: fail(ev['id'] + ': eventNow went ' + str(seen) + ', the data says ' + str(want))
    for (k, t), p in zip([x for x in ev['scan'] if x[0] != '-'], ev['phases']):
        if t != p['at']: fail(ev['id'] + ' ' + p['id'] + ': eventNow began it at minute ' + str(t) + ', evBeatAt says ' + str(p['at']))
if P['due'] and P['events'] and (P['due']['id'], P['due']['day']) != (P['events'][0]['id'], P['events'][0]['day']):
    fail('due ' + str(P['due']) + ', the calendar says ' + P['events'][0]['id'] + ' on Day ' + str(P['events'][0]['day']))
for h in P['held']: fail('held hour: ' + h)
for o in P['overlap']: fail('two events at once: ' + o)
if P['eventDays'] != P['bigDays']: fail('eventDay names Days ' + str(P['eventDays']) + ', the big phases fall on ' + str(P['bigDays']))
print('  eventDay:', P['eventDays'])
for x in P['guard']:
    print('  guard:', x['what'], x['when'], 'clear' if x['ok'] else 'CLASH ' + str(x['beats']))
    if not x['ok']: fail('guard: ' + x['what'] + ' at ' + x['when'] + ' meets ' + str(x['beats']))
for d, n in P['captainDays'].items():
    if n > 1: fail("two Captain's scenes on Day " + str(d))
    if int(d) in P['testDays']: fail("a Captain's scene on test Day " + str(d))
for c in P['cast']:
    print('  cast:', c['what'], c['who'], 'Day', c['day'], c['state'])
    if c['state'] in ('not aboard', 'off, not marked'): fail('cast: ' + c['who'] + ' for ' + c['what'] + ' on Day ' + str(c['day']) + ': ' + c['state'])
want_hold = [[11 * 1440 + 960, 11 * 1440 + 1020], [4 * 1440 + 930, 4 * 1440 + 1020], [3 * 1440 + 960, 3 * 1440 + 960], [11 * 1440 + 840, 11 * 1440 + 840]]
if P['holdSamples'] != want_hold: fail('the Friday hold: ' + str(P['holdSamples']) + ', wanted ' + str(want_hold))
if P['guardSamples'] != [False, True, False, True, False]: fail('the guard samples: ' + str(P['guardSamples']) + ' (test day, Day 18 16:00, table 19:30, table 19:00, the night shift)')
for n in P['notes']: print(' ', n)
if json.dumps(runs[0], sort_keys=True) != json.dumps(runs[1], sort_keys=True): fail('two runs on paper differ')
print('switched off:', off)
if off != {'on': False, 'eventDay': [], 'guard': [True, True, True], 'hold': True, 'at': True}: fail('switched off, the base still acts: ' + str(off))

print('BIGEVENTS CHECK OK' if ok else 'BIGEVENTS CHECK FAILED')
sys.exit(0 if ok else 1)
