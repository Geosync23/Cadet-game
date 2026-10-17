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
#   8. the evening in the real game (once section 13 has the Day 0 start): New game arriving, the manifest, a player
#      who follows Torres across three decks; every step reached in order, nothing missed, the device and Calder,
#      draw calls under 450, no page errors
#   Later waves (shown as "not yet"): the reserved jobs, the week in play, Sowing's draw calls.
# Setup and environment as for cadet_test.py.
# Run:  python3 intro_check.py BUILD.html
import sys, json
exec(open(__file__.replace('intro_check.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright

# run the intro on paper, minute by minute from Day 0 17:40 to `to` (absolute ship minutes); `who`: 'happy' (always at
# the checkpoint), 'wander' (misses every other step of the evening), 'idle' (never anywhere). reload: save and load
# section 21's state at every step change. Returns the intro, the points, the flags, the Mail it sent and the order.
RUN = r"""(({ who, reload, to, skip, endAt, pace }) => {
  const FLAGS = INTRO_FLAGS;
  socInit(); socReset(0); SHIP.mail.length = 0;
  SHIP.intro = introBlank(); SHIP.notes = []; if (SHIP.device) SHIP.device.appts = [];   // each run books its own health check   // section 13's flags are NOT reset: introBegin must clear what the last run left
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
    if (who === 'pace' && st && st.checkpoint) {         // walking in: tiles away = minutes left until you arrive (one step slow, then a steady pace)
      const took = pace[st.id] !== undefined ? pace[st.id] : pace.rest, left = Math.max(introAbs(st.day, st.at), SHIP.intro.since === null ? -1e9 : SHIP.intro.since) + took - t;
      const c = st.checkpoint; here = left <= 0 ? { deck: c.deck, tile: c.tile } : { deck: c.deck, tile: [c.tile[0] + left, c.tile[1]] };
    }
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

# one look at the real game for part 8: the player follows Torres (or walks to a step that isn't his), rides the lift
# when he does, and taps through meetings, choosing the second reply
WALK_TICK = r"""((mode) => {
  const I = SHIP.intro, st = introStepById(I.step), pp = player.obj.position, here = cellAt(pp.x, pp.z);
  const a = DECK_CREW.find(x => x.p && x.p.id === INTRO_ESCORT);
  let act = '';
  if (DIALOGUE) { const l = DIALOGUE.queue[DIALOGUE.i]; if (l && l.choice) dialogueChoose(1); else dialogueNext(); act = 'talk'; }
  else if (mode === 'follow' && st && st.checkpoint) {
    const cp = st.checkpoint;
    if (cp.deck !== deckDef.num) {                      // ride the lift to the checkpoint's deck
      if (!a || Math.hypot(a.x - pp.x, a.z - pp.z) < 3 || !a) { goToDeck(cp.deck); act = 'lift ' + cp.deck; }
      else { const c = cellAt(a.x, a.z), n = nearestOpen(cellPos(...c).x, cellPos(...c).z, player); if (n) player.obj.position.copy(cellPos(...n)); act = 'to him'; }
    } else {
      // keep 2 tiles behind him; once he's near the checkpoint, step onto it
      const tgt = a && Math.max(Math.abs(cellAt(a.x, a.z)[0] - cp.tile[0]), Math.abs(cellAt(a.x, a.z)[1] - cp.tile[1])) > 2 ? cellAt(a.x, a.z) : cp.tile;
      const dx = Math.sign(tgt[0] - here[0]), dz = Math.sign(tgt[1] - here[1]);
      const nx = here[0] + dx, nz = here[1] + dz;
      if (free(nx, nz) && !(a && Math.max(Math.abs(nx - cellAt(a.x, a.z)[0]), Math.abs(nz - cellAt(a.x, a.z)[1])) < 1)) player.obj.position.copy(cellPos(nx, nz));
      else { const p = cellPos(...tgt), n = nearestOpen(p.x, p.z, player); if (n) player.obj.position.copy(cellPos(...n)); }
      act = 'walk';
    }
  }
  return { t: clockText(), step: I.step, deck: deckDef.num, me: cellAt(player.obj.position.x, player.obj.position.z),
           esc: a ? [cellAt(a.x, a.z), a.pose, a.tag] : null, seat: typeof introSeat === 'function' ? introSeat(INTRO_ESCORT) : null, calls: renderer.info.render.calls, act, goal: IX_GOAL && IX_GOAL.label, dlg: DIALOGUE && DIALOGUE.id };
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
  const v = GAME_BUILD.split('.').map(Number);
  return { bad, rota, combined: v[0] > 0 || v[1] >= 60, steps: INTRO_STEPS.length, week: INTRO_WEEK.length, settle: SETTLE.length };
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
        if has != want and d['combined']: fail(f'{who} has days off {has}; the first week needs {want} (combined builds 0.60+)')

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
    if 'd2-health:appt' not in a['I']['done']: fail('Tuesday\'s health check was never booked')
    if 'd5-mug:met' not in a['I']['done']: fail('the Friday mug moment never happened (or its Mail)')
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
    for pc in ({'haulway': 25, 'rest': 7}, {'lift': 25, 'rest': 6}, {'bunk': 35, 'rest': 7}):
        pr = run(who='pace', pace=pc, to=EVENING)
        slow = [k for k in pc if k != 'rest']
        print(f"  one slow step then steady {pc}: missed {pr['I']['missed']}")
        if [m for m in pr['I']['missed'] if m not in slow]: fail(f'one slow step costs others: {pr["I"]["missed"]}')
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
    # skip (0.42.6): the evening's points and steps, no scripted week, every gate open (all flags but mug and seedling)
    want = {f: f not in ('mug', 'seedling') for f in s['flags']}
    print(f"  points {s['rel']} (the evening's: {s['rel'] == e['rel']}); every gate open: {s['flags'] == want}; the week off: {s['I']['ended']}")
    if s['rel'] != e['rel']: fail(f"skip gives {s['rel']}, the evening {e['rel']}")
    if s['flags'] != want: fail(f"skip's flags: {[f for f in want if s['flags'][f] != want[f]]} wrong")
    if any(e['flags'][f] and not s['flags'][f] for f in e['flags']): fail('skip lacks a flag the evening sets')
    if sorted(s['I']['done']) != sorted(e['I']['done']): fail('skip marks different steps done')
    if not (s['I']['skipped'] and s['I']['ended']): fail('skip is not marked skipped and ended')
    sk = g.ev("(() => { introSkip(); const r = { on: introOn(), beats: introBeats('torres-zeke', 1).length + introBeats('calder', 2).length, esc: escortPlan(ROSTER.find(p => p.id === INTRO_ESCORT), 1440 + 600) }; SHIP.intro = introBlank(); return r; })()")
    if sk['on'] or sk['beats'] or sk['esc']: fail(f'skip still runs the week: {sk}')

    print('6. Determinism')
    b = run()
    print('  the same twice:', b['intro'] == a['intro'] and b['mail'] == a['mail'])
    if b['intro'] != a['intro'] or b['mail'] != a['mail']: fail('the happy path came out differently the second time')

    print('7. The Settling-in list, and the job notes')
    jn = g.ev("(() => { introBegin(); introJobNote({ step: 'take', reserved: 1 }); introJobNote({ step: 'turnin', reserved: 1 }); introJobNote({ step: 'turnin', reserved: 1 }); introJobNote({ step: 'turnin', reserved: 0 }); const r = Object.keys(SHIP.intro.done); SHIP.intro = introBlank(); return r; })()")
    print('  slot 1 turned in ->', jn)
    if jn != ['d1-shadow:job']: fail('the shadow shift\'s note: ' + str(jn))
    t = g.ev(SETTLE_NOTES)
    print('  every item ticks from its own note:', not t['bad'], '| all done sends the note:', t['all'])
    for x in t['bad']: fail(x)
    if not t['all']: fail('ticking everything did not finish the list')

    print('8. The evening in the real game (New game arriving, a player who follows Torres and taps through meetings)')
    if not g.ev("typeof newGameStart === 'function' && typeof escortPlanOf === 'function'"):
        fail('no newGameStart or escort walker (sections 13 and 10, the sim engineer): the arrival cannot start')
    else:
        g.ev('newGameStart(true)'); g.step(5)
        g.page.fill('form input[maxlength="24"]', 'Sam'); g.page.click('form button'); g.step(5)
        order, peak, led = [], {}, 0
        for k in range(420):
            g.step(20)
            r = g.page.evaluate('([s, m]) => window.__sc(s)(m)', [WALK_TICK, 'follow'])
            peak[r['deck']] = max(peak.get(r['deck'], 0), r['calls'])
            if r['esc'] and r['esc'][2] == 'escort': led += 1
            if not order or order[-1] != r['step']: order.append(r['step']); print(f"  {r['t']}  {r['step']}  (you: Deck {r['deck']} {r['me']}; Torres {r['esc'][0] if r['esc'] else 'not here'}{'; his seat ' + r['seat'] if r['seat'] else ''})")
            if r['step'] is None: break
        w = g.ev("({ missed: SHIP.intro.missed, done: Object.keys(SHIP.intro.done), device: introFlag('intro.device'), calder: introFlag('met.calder') })")
        print(f'  draw-call peaks by deck {peak}; Torres led you for {led} looks')
        if w['missed']: fail('the real walk missed ' + ', '.join(w['missed']))
        if [s for s in steps if s not in w['done']]: fail('the real walk never reached ' + ', '.join(s for s in steps if s not in w['done']))
        if order[-1] is not None: fail('the evening did not end in the real walk')
        if not (w['device'] and w['calder']): fail('no device or no Calder after the real walk')
        if max(peak.values()) >= 450: fail(f'draw calls {max(peak.values())} at the arrival (budget 450)')
        if led < 20: fail('Torres hardly led you')
    print('9. A first launch arrives (no save, never arrived, not a test URL), and its Day 0 save loads at the same step')
    if not g.ev("typeof newGameStart === 'function'"):
        fail('no newGameStart (section 13): a first launch cannot arrive')
    else:
        url = g.page.url.split('?')[0]
        g.page.evaluate('localStorage.clear()')
        g.page.goto(url + '?debug'); g.page.wait_for_function('window.__sc !== undefined || window.__err', timeout=60000)
        g.step(5)
        f = g.ev("({ t: clockText(), deck: deckDef.num, on: introOn(), step: SHIP.intro.step, form: !!document.querySelector('form input[maxlength=\"24\"]') })")
        print(f"  {f['t']}, Deck {f['deck']}, intro {'on' if f['on'] else 'off'} at {f['step']}, manifest {'up' if f['form'] else 'not up'}")
        if not (f['t'].startswith('Day 0, Sunday 17:40') and f['deck'] == 5 and f['on'] and f['form']): fail('a first launch did not arrive by shuttle')
        g.page.fill('form input[maxlength="24"]', 'Sam'); g.page.click('form button'); g.step(30)
        g.ev('saveGame()'); before = g.ev('({ step: SHIP.intro.step, day: SHIP.time.day })')
        g.page.goto(url + '?debug'); g.page.wait_for_function('window.__sc !== undefined || window.__err', timeout=60000); g.step(5)
        after = g.ev("({ step: SHIP.intro.step, day: SHIP.time.day, form: !!document.querySelector('form input[maxlength=\"24\"]'), name: SHIP.player.name })")
        print(f"  saved at {before}, loaded at step {after['step']} on Day {after['day']}, manifest {'up' if after['form'] else 'gone'}, name {after['name']}")
        if after['step'] != before['step'] or after['day'] != 0 or after['form']: fail('a Day 0 save did not load at its step')
        if after['name'] != 'Sam': print('  (the name comes back once section 15 saves SHIP.player.name: player engineer 3)')
        g.page.evaluate('localStorage.clear()')
    print('10. Monday in the real game: the three jobs held at 05:00, the briefing at 07:50, the shadow shift with Torres')
    if not g.ev("typeof jobReserve === 'function' && typeof newGameStart === 'function'"):
        print('  not yet: this build has no jobReserve (section 17, systems 0.33.36+)')
    else:
        g.ev('localStorage.clear()'); g.ev('newGameStart(true)'); g.step(5)
        g.page.fill('form input[maxlength="24"]', 'Sam'); g.page.click('form button'); g.step(5)
        g.ev('skipTo(introAbs(1, 7 * 60 + 40))'); g.ev('(() => { goToDeck(5); player.obj.position.copy(cellPos(15, 3)); })()'); g.step(5)   # the next frames run 05:00's beat, which holds the jobs
        res = g.ev("[1, 2, 3].map(k => SHIP.jobs.find(x => x.reserved === k)).map(j => j && j.machine)")
        print('  held for you:', res)
        if not all(res): fail('the week\'s three jobs are not all held')
        met = None
        for i in range(40):
            g.step(30); met = g.ev('DIALOGUE && DIALOGUE.id')
            if met: break
        print('  07:50 in the Works bay:', met)
        if met != 'introBriefing': fail('the Monday briefing did not play')
        g.ev('(() => { while (DIALOGUE) dialogueNext(); })()')
        for i in range(40):
            g.step(30)
            if g.ev('shipNow() >= introAbs(1, 486)'): break
        took = g.ev("claimJob(SHIP.jobs.find(x => x.reserved === 1).id)")
        g.step(60)
        esc = g.ev("(() => { const a = DECK_CREW.find(x => x.p.id === INTRO_ESCORT), e = escortPlan(ROSTER.find(p => p.id === INTRO_ESCORT), shipNow()), pp = player.obj.position; return { mode: e && e.mode, d: a ? Math.round(Math.hypot(a.x - pp.x, a.z - pp.z)) : null }; })()")
        fin = g.ev("(() => { const j = SHIP.jobs.find(x => x.reserved === 1); jobStops(j).forEach((s, k) => jobStepDone(j.id, k)); j.workDone = true; return { t: turnInJob(j.id), shadow: !!SHIP.intro.settle.shadow, mem: (SHIP.notes || []).some(n => n.kind === 'introStep' && n.step === 'd1-shadow') }; })()")
        print(f"  took it: {took}; Torres {esc['mode']}, {esc['d']} tiles from you; turned in: {fin['t']}; 'Shadow a job' ticked: {fin['shadow']}; d1-shadow note: {fin['mem']}")
        if not took: fail('could not take the shadow job at 08:06')
        if esc['mode'] != 'follow' or esc['d'] is None or esc['d'] > 4: fail(f'Torres is not with you on the shadow shift: {esc}')
        if not (fin['t'] and fin['shadow'] and fin['mem']): fail(f'the shadow job did not complete the intro\'s side: {fin}')
    print('Not yet: Tuesday and the rest of the week in play, reload mid-walk in the real game')
    if g.errors: fail('page errors: ' + ' | '.join(g.errors[:6]))
    g.close()

print('OK' if ok else 'FAILED')
sys.exit(0 if ok else 1)
