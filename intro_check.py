# Starship Cadet: intro check (keep in the repo, next to day_check.py)
# The arrival and the first week (section 21, plans/pillar4-plan.md Part 1). Wave 1a: everything on paper.
#   0. test URLs (?nosave&debug) start with the intro off: Day 1 06:00, no escort, no beats (so every other check is unchanged)
#   1. the data: steps and beats in time order, everyone named is on the roster, every checkpoint tile is in its room on
#      its deck's map, every fallback leads to a real step, every meeting and Settling-in item is known
#   2. the happy path on paper: a player always at the checkpoint, Day 0 17:40 to Day 8; every step in order, the
#      week's flags at their times, the arrival evening's points (Torres 10, Tomas 10, Pell 5, Calder 3, Brennan 3)
#   3. the wanderer (misses every other step) and the idler (never there): the fallbacks' Mail, the evening still ends
#      by 20:00, the week still ends on Day 8
#   4. save and reload at every step of the evening: the run comes out the same as without reloads
#   5. skip-intro: the same points, flags and steps as after the arrival evening
#   6. determinism: the happy path twice, the same
#   7. the Settling-in list: one note of each kind ticks every item, and nothing else ticks any
#   Later waves (shown as "not yet"): walking it in the real game, the escort never stuck, crossing decks by lift,
#   meetings with their cast, the reserved jobs, draw calls under 450 at the bay, the Works door, dinner and Sowing.
# Setup and environment as for cadet_test.py.
# Run:  python3 intro_check.py BUILD.html
import sys, json
exec(open(__file__.replace('intro_check.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright

# run the intro on paper, minute by minute from Day 0 17:40 to `to` (absolute ship minutes); `who`: 'happy' (always at
# the checkpoint), 'wander' (misses every other step of the evening), 'idle' (never anywhere). reload: save and load
# section 21's state at every step change. Returns the intro, the points, the flags, the Mail it sent and the order.
RUN = r"""(({ who, reload, to, skip, endAt }) => {
  const FLAGS = INTRO_FLAGS;
  socInit(); socReset(0); SHIP.mail.length = 0;
  SHIP.intro = introBlank(); SHIP.notes = [];   // section 13's flags are NOT reset: introBegin must clear what the last run left
  const t0 = introAbs(INTRO_START.day, INTRO_START.min), order = [], flagAt = {};
  if (skip) { setShipNow(t0); introSkip(); }
  else introBegin('Sam');
  let k = 0, last = SHIP.intro.step;
  for (let t = t0; t <= to && !skip; t++) {
    setShipNow(t);
    const st = SHIP.intro.step && introStepById(SHIP.intro.step);
    let here = st && st.checkpoint ? { deck: st.checkpoint.deck, tile: st.checkpoint.tile } : { deck: 4, tile: [8, 3] };
    if (who === 'idle' || (who === 'wander' && st && INTRO_STEPS.indexOf(st) % 2)) here = null;
    if (who === 'slow' && st && t < Math.max(introAbs(st.day, st.at), SHIP.intro.since === null ? -1e9 : SHIP.intro.since) + 10) here = null;   // 10 ship minutes behind
    if (endAt !== undefined && t === endAt) introEnd(false);
    introAdvance(t, here);
    for (const f of FLAGS) if (flagAt[f] === undefined && introFlag(f)) flagAt[f] = t;
    if (SHIP.intro.step !== last) {
      order.push(last); last = SHIP.intro.step; k++;
      if (reload) { SHIP.intro = introLoad({ intro: JSON.parse(JSON.stringify(introSave())) }); }
    }
  }
  const rel = {}; for (const id of [INTRO_ESCORT, 'tomas', 'pell', 'calder', 'brennan']) rel[id] = SHIP.rel[id] ? SHIP.rel[id].pts : 0;
  const flags = {}; for (const f of FLAGS) flags[f] = introFlag(f);
  return { intro: JSON.stringify(SHIP.intro), I: SHIP.intro, rel, flags, flagAt, order,
           mail: SHIP.mail.map(m => [m.at, m.from, m.subject]).reverse(), steps: k };
})"""

DATA = r"""(() => {
  const bad = [], ids = new Set(ROSTER.map(p => p.id)), room = (d, name) => Object.values(DECKS[d].rooms).some(r => r.name === name);
  const seen = new Set();
  for (const s of INTRO_STEPS.concat(INTRO_WEEK)) { if (seen.has(s.id)) bad.push('two steps called ' + s.id); seen.add(s.id); }
  let prev = -1e9;
  for (const s of INTRO_STEPS) {
    const at = introAbs(s.day, s.at);
    if (at < prev) bad.push(s.id + ' is earlier than the step before it'); prev = at;
    if (s.who && !ids.has(s.who)) bad.push(s.id + ': nobody called ' + s.who);
    for (const w in s.rel || {}) if (!ids.has(w)) bad.push(s.id + ': points for nobody called ' + w);
    if (s.meeting && !INTRO_MEETINGS[s.meeting]) bad.push(s.id + ': no meeting ' + s.meeting);
    const f = s.fallback; if (f && !INTRO_STEPS.some(x => x.id === f.later)) bad.push(s.id + ': falls back to a step that isn\'t there, ' + f.later);
    if (f && f.later && INTRO_STEPS.findIndex(x => x.id === f.later) <= INTRO_STEPS.indexOf(s)) bad.push(s.id + ': falls back to an earlier step');
    const c = s.checkpoint; if (!c) continue;
    const D = DECKS[c.deck], ch = D && D.map[c.tile[1]] && D.map[c.tile[1]][c.tile[0]], r = D && D.rooms[ch];
    if (!r) bad.push(s.id + ': checkpoint ' + c.tile + ' is off Deck ' + c.deck + '\'s map');
    else if (r.name !== c.room) bad.push(s.id + ': checkpoint ' + c.tile + ' is in ' + r.name + ', not ' + c.room);
    else if (r.void) bad.push(s.id + ': checkpoint in a void');
  }
  for (let i = 1; i < INTRO_STEPS.length; i++) {      // a step must not count from the one before's checkpoint
    const p = INTRO_STEPS[i - 1].checkpoint, c = INTRO_STEPS[i].checkpoint; if (!p || !c || p.deck !== c.deck || p.room !== c.room) continue;
    const d = Math.max(Math.abs(p.tile[0] - c.tile[0]), Math.abs(p.tile[1] - c.tile[1]));
    if (d > 0 && d <= INTRO_REACH) bad.push(INTRO_STEPS[i].id + '\'s checkpoint is within reach of ' + INTRO_STEPS[i - 1].id + '\'s');
  }
  prev = -1e9;
  for (const b of INTRO_WEEK) {
    const at = introAbs(b.day, b.at); if (at < prev) bad.push(b.id + ' is earlier than the beat before it'); prev = at;
    for (const w of [b.who].concat(b.also || [])) if (w && !ids.has(w)) bad.push(b.id + ': nobody called ' + w);
    if (b.where && typeof b.where === 'object' && !room(b.where.deck, b.where.room)) bad.push(b.id + ': no ' + b.where.room + ' on Deck ' + b.where.deck);
    if (b.settle && !SETTLE.some(s => s.id === b.settle)) bad.push(b.id + ': teaches ' + b.settle + ', not on the list');
    if (b.meeting && !INTRO_MEETINGS[b.meeting]) bad.push(b.id + ': no meeting ' + b.meeting);
    if (b.until !== undefined && b.until <= b.at) bad.push(b.id + ': ends before it starts');
  }
  for (const s of SETTLE) {
    if (!ids.has(s.teacher)) bad.push('Settling in, ' + s.id + ': nobody called ' + s.teacher);
    if (s.place && !room(s.place.deck, s.place.room)) bad.push('Settling in, ' + s.id + ': no ' + s.place.room + ' on Deck ' + s.place.deck);
    if (!INTRO_WEEK.some(b => b.settle === s.id) && s.id !== 'laundry') bad.push('Settling in, ' + s.id + ': nobody teaches it in the week');
  }
  for (const m in INTRO_MEETINGS) for (const w of INTRO_MEETINGS[m].cast) if (!/^works:/.test(w) && !ids.has(w)) bad.push(m + ': nobody called ' + w);
  const off = id => { const p = ROSTER.find(x => x.id === id); return p && p.rota ? (p.rota.offDays || []).slice().sort().join(',') : '?'; };
  const rota = { 'torres-zeke': [off('torres-zeke'), '3,4'], calder: [off('calder'), '5,6'], 'halloran-emeka': [off('halloran-emeka'), '5,6'] };
  return { bad, rota, steps: INTRO_STEPS.length, week: INTRO_WEEK.length, settle: SETTLE.length };
})()"""

# one note that should tick each item (the kinds other sections will send; DEV_NOTES "Hook register")
SETTLE_NOTES = r"""(() => {
  const N = { washed: ['act', { act: 'wash' }], team: ['introStep', { step: 'd1-briefing' }], shadow: ['job', { step: 'turnin', reserved: 1 }],
    lead: ['job', { step: 'turnin', reserved: 2 }], eat: ['act', { act: 'eat', with: 2 }], solo: ['job', { step: 'turnin' }],
    health: ['apptKept', { id: 'intro-health' }], call: ['act', { act: 'call' }], take: ['job', { step: 'take' }], buy: ['act', { act: 'buy' }],
    friend: ['tierUp', { id: 'pell', tier: 1 }], favour: ['favour', { who: 'kovac-zainab' }], laundry: ['act', { act: 'laundry' }],
    tradition: ['tradition', { id: 'quiz', you: true }], dayoff: ['introStep', { step: 'd6-sowing' }] };
  const NOISE = [['act', { act: 'eat', with: 0 }], ['tierUp', { id: INTRO_ESCORT, tier: 1 }], ['tierUp', { id: 'tomas', tier: 1 }], ['tradition', { id: 'quiz', you: false }],
    ['job', { step: 'take', reserved: 1 }], ['introStep', { step: 'hello' }], ['apptKept', { id: 'other' }]];
  const bad = [];
  SHIP.intro = introBlank(); SHIP.intro.on = true;
  for (const [k, d] of NOISE) settleNote(k, d);
  const early = Object.keys(SHIP.intro.settle); if (early.length) bad.push('ticked by the wrong notes: ' + early.join(', '));
  for (const s of SETTLE) {
    if (!N[s.id]) { bad.push('no test note for ' + s.id); continue; }
    const before = Object.keys(SHIP.intro.settle).length; settleNote(...N[s.id]);
    if (!SHIP.intro.settle[s.id]) bad.push(s.id + ' did not tick');
    else if (Object.keys(SHIP.intro.settle).filter(k => k !== 'all').length !== before + 1) bad.push(s.id + '\'s note ticked others too');
  }
  const all = !!SHIP.intro.settle.all; SHIP.intro = introBlank();
  return { bad, all };
})()"""

ok = True
def fail(msg):
    global ok
    ok = False
    print('  FAIL', msg)

def mins(t):
    d = t // 1440 + 1
    return f"Day {d} {t % 1440 // 60:02d}:{t % 60:02d}"

with sync_playwright() as pw:
    g = Game(pw, sys.argv[1])
    if not g.ev("typeof INTRO_STEPS !== 'undefined'"):
        print('No section 21 in this build.'); sys.exit(1)

    print('0. Test URLs start with the intro off')
    st = g.ev("({ on: introOn(), s: SHIP.intro.on, day: SHIP.time.day, min: Math.floor(SHIP.time.min), esc: escortPlan(ROSTER.find(p => p.id === INTRO_ESCORT), shipNow()), beats: introBeats(INTRO_ESCORT, 1).length })")
    print(f"  intro {'on' if st['on'] else 'off'}, Day {st['day']} {st['min'] // 60:02d}:{st['min'] % 60:02d}, escort plan {st['esc']}, beats {st['beats']}")
    if st['on'] or st['s']: fail('the intro is on at a test URL')
    if (st['day'], st['min']) != (1, 360): fail('a test URL should start at Day 1 06:00')
    if st['esc'] is not None or st['beats']: fail('the escort or the beats are live with the intro off')

    print('1. The data')
    d = g.ev(DATA)
    print(f"  {d['steps']} steps on the arrival evening, {d['week']} beats in the week, {d['settle']} Settling-in items")
    for b in d['bad']: fail(b)
    for who, (has, want) in d['rota'].items():
        print(f"  {who} off days {has}{'' if has == want else ', WAITING for the crew designer: the week needs ' + want}")

    run = lambda **k: g.page.evaluate("([s, a]) => window.__sc(s)(a)", [RUN, {'who': 'happy', 'reload': False, 'to': 7 * 1440, 'skip': False, **k}])
    EVENING = -1440 + 20 * 60 + 1          # Day 0 20:01
    WANT = {'torres-zeke': 10, 'tomas': 10, 'pell': 5, 'calder': 3, 'brennan': 3}

    print('2. The happy path, on paper (Day 0 17:40 to Day 8 00:00)')
    a = run()
    steps = g.ev("INTRO_STEPS.map(s => s.id)")
    order = [k for k in a['I']['done'] if k in steps]
    print('  order:', ' > '.join(order))
    if order != steps: fail('the steps did not run in order: ' + ', '.join(order))
    missed = a['I']['missed']
    if missed: fail('missed with the player there: ' + ', '.join(missed))
    if a['rel'] != WANT: fail(f"points after the week: {a['rel']}, wanted {WANT}")
    print('  points:', a['rel'])
    when = {f'week1.d{d}': (d - 1) * 1440 + 360 for d in range(2, 8)}
    when['week1.done'] = 7 * 1440
    print('  flags:', ', '.join(f"{f} {mins(a['flagAt'][f])}" for f in when if f in a['flagAt']))
    for f, t in when.items():
        if a['flagAt'].get(f) != t: fail(f"{f} at {mins(a['flagAt'][f]) if f in a['flagAt'] else 'never'}, wanted {mins(t)}")
    if not a['I']['ended']: fail('the intro did not end on Day 8')
    print('  mail:', '; '.join(f"{mins(int(m[0]))} {m[1]}: {m[2]}" for m in a['mail']))
    if any(m[2] in ('Your bunk', 'Tomorrow') for m in a['mail']): fail('a fallback Mail went out with the player there')

    print('3. The wanderer and the idler')
    for who in ('wander', 'idle'):
        e = run(who=who, to=EVENING)
        late = [s for s in steps if s not in e['I']['done']]
        miss = e['I']['missed']
        print(f"  {who}: by Day 0 20:01 step {e['I']['step']}, missed {len(miss)} ({', '.join(miss)}); mail: {', '.join(m[2] for m in e['mail'])}")
        if e['I']['step'] is not None or late: fail(f"{who}: the evening hasn't ended by 20:01 (left: {', '.join(late)})")
        if who == 'idle' and not {'Your bunk', 'Tomorrow'} <= {m[2] for m in e['mail']}: fail('idle: the fallback Mail did not all arrive')
        if who == 'wander' and len(miss) < 5: fail(f'wander: only {len(miss)} steps missed; a step should not count from a nearby checkpoint')
        w = run(who=who)
        if not (w['flags']['intro.device'] and w['flags']['met.calder']): fail(who + ': no device or no Calder by the end of the week')
        if who == 'idle' and e['flags']['intro.device']: fail('idle: the device counts as handed over though you never came')
        if not w['I']['ended'] or not w['flags']['week1.done']: fail(who + ': the week did not end on Day 8')

    sl = run(who='slow', to=EVENING)
    print(f"  slow (10 ship minutes behind at every step): missed {len(sl['I']['missed'])} {sl['I']['missed']}")
    if sl['I']['missed']: fail('a player 10 minutes behind missed steps: ' + ', '.join(sl['I']['missed']))
    en = run(who='idle', endAt=1440 + 7 * 60)
    print('  idle, then "I know my way around" on Monday 07:00:', ', '.join(f for f, v in en['flags'].items() if not v) or 'every flag set', 'unset')
    for f in ['intro.device', 'met.calder', 'week1.done'] + [f'week1.d{d}' for d in range(2, 8)]:
        if not en['flags'][f]: fail('ending early leaves ' + f + ' unset')
    a2 = run(who='idle', to=EVENING)
    if a2['flags']['intro.device'] or a2['flags']['week1.done']: fail('a second arrival kept the last game\'s flags')
    print('4. Save and reload at every step')
    r = run(reload=True)
    print(f"  {r['steps']} reloads; the same as without: {r['intro'] == a['intro'] and r['rel'] == a['rel']}")
    if r['intro'] != a['intro'] or r['rel'] != a['rel'] or r['flags'] != a['flags']: fail('reloading changed the run')

    print('5. Skip-intro')
    s = run(skip=True)
    e = run(to=EVENING)
    same = s['rel'] == e['rel'] and s['flags'] == e['flags'] and sorted(s['I']['done']) == sorted(e['I']['done'])
    print(f"  points {s['rel']}; the same as after the evening: {same}")
    if s['rel'] != e['rel']: fail(f"skip gives {s['rel']}, the evening {e['rel']}")
    if s['flags'] != e['flags']: fail(f"skip's flags differ: {[f for f in s['flags'] if s['flags'][f] != e['flags'][f]]}")
    if sorted(s['I']['done']) != sorted(e['I']['done']): fail('skip marks different steps done')
    if not s['I']['skipped']: fail('skip is not marked skipped')

    print('6. Determinism')
    b = run()
    print('  the same twice:', b['intro'] == a['intro'] and b['mail'] == a['mail'])
    if b['intro'] != a['intro'] or b['mail'] != a['mail']: fail('the happy path came out differently the second time')

    print('7. The Settling-in list')
    t = g.ev(SETTLE_NOTES)
    print('  every item ticks from its own note:', not t['bad'], '| all done sends the note:', t['all'])
    for x in t['bad']: fail(x)
    if not t['all']: fail('ticking everything did not finish the list')

    print('Not yet (wave 2 and later): the real walk, the escort never stuck, the lift, meetings with their cast, the reserved jobs, draw calls')
    if g.errors: fail('page errors: ' + ' | '.join(g.errors[:6]))
    g.close()

print('OK' if ok else 'FAILED')
sys.exit(0 if ok else 1)
