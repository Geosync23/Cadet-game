# Starship Cadet: intro check (keep in the repo, next to day_check.py)
# The arrival and the first week (section 21, plans/pillar4-plan.md Part 1). Wave 1a: everything on paper.
#   0. test URLs (?nosave&debug) start with the intro off: Day 1 06:00, no escort, no beats (so every other check is unchanged)
#   1. the data: steps and beats in time order, everyone named is on the roster, every checkpoint tile is in its room on
#      its deck's map, every fallback leads to a real step, every meeting and Settling-in item is known
#   2. the happy path on paper: a player always at the checkpoint, Day 0 16:30 (INTRO_START) to Day 8; every step in order, the
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
#   14. Tuesday's first solo job (the playtest patch 1, #7): after the Chief's meeting the arrow leads to it, Take it at the board
#   18. (item 81) Tuesday 08:51: the solo job's Tracked arrow at your spot in her office; a real tap on the Chief walks you in and it
#      starts; at 10:05 a tap on her doesn't (--solotap: this part alone)
#   Later waves (shown as "not yet"): the reserved jobs, the week in play, Sowing's draw calls.
# Setup and environment as for cadet_test.py.
# Run:  python3 intro_check.py BUILD.html
import sys, json
exec(open('/home/user/w-dv1/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright

# run the intro on paper, minute by minute from Day 0 16:30 (INTRO_START) to `to` (absolute ship minutes); `who`: 'happy' (always at
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
CALDER_D = """(() => { const a = DECK_CREW.find(x => x.p && x.p.id === 'calder'), sp = placeSpot(introSeat('calder') || '3-mess-9'); return a && sp ? Math.round(Math.hypot(a.x - sp.x, a.z - sp.z) * 10) / 10 : null; })()"""
# the patch (#3): during the dinner chat she eats at the next table (the chief step's `away` seat), then walks over
CALDER_AWAY = """(() => { const a = DECK_CREW.find(x => x.p && x.p.id === 'calder'), st = introStepById('chief'), sp = st.away && placeSpot(st.away.calder); return a && sp ? Math.round(Math.hypot(a.x - sp.x, a.z - sp.z) * 10) / 10 : null; })()"""
# playtest patch 1, #6: someone `after` (5) ship minutes past `key` (a SHIP.intro.done minute): how far from their seat at your table
LINGER = r"""(([who, key]) => {
  const I = SHIP.intro, at = I.done[key], seat = (introStepById('chief').seats || {})[who];
  if (typeof at !== 'number' || !seat || shipNow() < at + 5) return null;
  const a = DECK_CREW.find(x => x.p && x.p.id === who), sp = placeSpot(seat);
  return { t: clockText(), after: Math.floor(shipNow()) - at, d: a && sp && deckDef.num === 3 ? Math.round(Math.hypot(a.x - sp.x, a.z - sp.z) * 10) / 10 : null };
})"""
WALK_TICK = r"""((mode) => {
  const I = SHIP.intro, st = introStepById(I.step), pp = player.obj.position, here = cellAt(pp.x, pp.z);
  const a = DECK_CREW.find(x => x.p && x.p.id === INTRO_ESCORT);
  let act = '';
  if (DIALOGUE) { const l = DIALOGUE.queue[DIALOGUE.i]; if (l && l.choice) dialogueChoose(1); else dialogueNext(); act = 'talk'; }
  else if (typeof DEV !== 'undefined' && DEV.open && I.done['hand:start'] !== undefined && I.done['hand:end'] === undefined) {   // DS1: his Mail on your device, read, then closed
    window.__handMail = window.__handMail || { t: clockText(), app: DEV.app, mail: typeof mailOpen !== 'undefined' ? mailOpen : null, subject: ((SHIP.mail || []).find(m => m.id === mailOpen) || {}).subject || null };
    if ((window.__handRead = (window.__handRead || 0) + 1) > 3) deviceClose(); act = 'read mail';
  }
  else if (I.step === 'stow' && typeof bagHeld === 'function' && bagHeld() && typeof wardrobeUse === 'function') {   // playtest patch 1: your bag into your wardrobe (a tap on it)
    const w = clothesWardrobe(); if (w && w.tile) player.obj.position.copy(cellPos(...w.tile));
    window.__stow = { t: clockText(), goal: typeof IX_GOAL !== 'undefined' && IX_GOAL ? IX_GOAL.label : null }; wardrobeUse(); act = 'stow';
  }
  else if (mode === 'follow' && typeof introHandDue === 'function' && introHandDue() && a) {   // DS1 (lead 31): his device hand-over: stay with him (the arrow says "Zeke Torres"), beside him
    const c = cellAt(a.x, a.z); if (Math.max(Math.abs(c[0] - here[0]), Math.abs(c[1] - here[1])) > 1) { const n = nearestOpen(a.x, a.z, player); if (n) player.obj.position.copy(cellPos(...n)); }
    act = 'hand-over';
  }
  else if (mode === 'follow' && st && st.checkpoint && typeof INTRO_UI !== 'undefined' && INTRO_UI.pause && a) act = 'listen';   // he's stopped to tell you about a place: stay with him
  else if (mode === 'beside' && st && st.checkpoint && a && cellAt(a.x, a.z) && st.checkpoint.deck === deckDef.num) {   // DS1 (FE2 on 0.92.0): a player who walks beside him,
    // 2 tiles off, never onto a step's own spot (it's where he stands): toward him a tile at a time when further, else stays put
    const c = cellAt(a.x, a.z), cp = st.checkpoint.tile;
    if (Math.max(Math.abs(c[0] - here[0]), Math.abs(c[1] - here[1])) > 2) {
      const nx = here[0] + Math.sign(c[0] - here[0]), nz = here[1] + Math.sign(c[1] - here[1]);
      if (free(nx, nz) && !(nx === cp[0] && nz === cp[1])) player.obj.position.copy(cellPos(nx, nz));
      else { const n = nearestOpen(cellPos(...c).x, cellPos(...c).z, player); if (n && !(n[0] === cp[0] && n[1] === cp[1])) player.obj.position.copy(cellPos(...n)); }
      act = 'walk';
    } else act = 'beside';
  }
  else if ((mode === 'follow' || mode === 'beside') && st && st.checkpoint) {
    const cp = st.checkpoint;
    if (cp.deck !== deckDef.num) {                      // ride the lift to the checkpoint's deck
      if (typeof ride !== 'undefined' && ride) act = 'riding';   // 0.42.29: the real ride (doors, fade, the new deck built), as a player takes it
      else if (!a || Math.hypot(a.x - pp.x, a.z - pp.z) < 3 || !a) {
        if (typeof startRide === 'function') {
          if (!inLift()) { const c = liftTiles().sort((x, y) => Math.hypot(x[0] - here[0], x[1] - here[1]) - Math.hypot(y[0] - here[0], y[1] - here[1]))[0]; if (c) player.obj.position.copy(cellPos(...c)); }   // step into the car
          startRide(cp.deck);
        } else goToDeck(cp.deck);
        act = 'lift ' + cp.deck;
      }
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
           esc: a ? [cellAt(a.x, a.z), a.pose, a.tag] : null, seat: typeof introSeat === 'function' ? introSeat(INTRO_ESCORT) : null, calls: renderer.info.render.calls, act, goal: IX_GOAL && IX_GOAL.label, shown: (el => el && !el.hidden ? el.children[2].textContent : null)(document.getElementById('ixGoal')), dlg: DIALOGUE && DIALOGUE.id,
           ex: a ? [+a.x.toFixed(2), +a.z.toFixed(2)] : null, pause: !!(typeof INTRO_UI !== 'undefined' && INTRO_UI.pause), pre: I.done['tour:up'] !== undefined && I.done['tour:lift'] === undefined, sm: shipNow() };
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
    const taught = INTRO_WEEK.some(b => b.settle === s.id) || typeof CLOTHES_BEATS !== 'undefined' && CLOTHES_BEATS.some(b => b.settle === s.id);   // 0.42.45: section 21b's beats teach clothes (Zeke at dinner) and hobby (his knitting offer)
    if (!taught && s.id !== 'laundry') bad.push('Settling in, ' + s.id + ': nobody teaches it in the week');
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
    tradition: ['tradition', { id: 'quiz', you: true }], dayoff: ['introStep', { step: 'd6-sowing' }],
    clothes: ['act', { act: 'clothes' }], hobby: ['act', { act: 'hobby' }], talk: ['talk', { id: 'pell', mins: 10 }] };   // 0.60.7: section 21b's wardrobe, section 15's hobbies, social's Talk a while
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

# part 12, also on its own: python3 intro_check.py BUILD.html --week (a fast-forwarded week is slow; the lead's quick checks)
def week(g):
    print('12. The week in the real game: on paper, no intro beat\'s place shared with someone else\'s plan (Days 0-8); each beat\'s teacher says their lines in its room in its window (the writers\' beat.<id>.<n>); Tomas comes to Sowing')
    if not g.ev("typeof introBeatTick === 'function' && typeof skipTo === 'function'"):
        print('  not yet: no introBeatTick')
    else:
        g.ev('localStorage.clear()'); g.ev('newGameStart(true)'); g.step(5)
        g.page.fill('form input[maxlength="24"]', 'Sam'); g.page.click('form button'); g.step(5)
        # on paper first (backlogs #20 and #25, PR9's rule): Days 0-8, nobody planned in a place someone on an intro beat
        # has at the same minutes (seated places, not an event's standing spots): a teacher's seat stays theirs
        cl = g.ev("""(() => { const out = [], byId = schedData().byId;
          for (let d = 0; d <= 8; d++) { const segs = []; for (const [id, plan] of shipDay(d).plans) for (const s of plan) if (s.placeId) segs.push([id, s]);
            for (let i = 0; i < segs.length; i++) for (let j = i + 1; j < segs.length; j++) { const [a, s] = segs[i], [b, u] = segs[j];
              if (a !== b && s.placeId === u.placeId && s.from < u.to && u.from < s.to && (byId.get(s.placeId) || {}).type !== 'event' && (/^intro/.test(s.tag || '') || /^intro/.test(u.tag || '')))
                out.push(`Day ${d} ${s.placeId} ${hhmm(Math.max(s.from, u.from) % 1440)}: ${a} (${s.tag || s.act}) and ${b} (${u.tag || u.act})`); } }
          return out; })()""")
        print(f"  intro beats' places, Days 0-8: {len(cl)} shared with someone else's plan")
        for c in cl[:8]: fail('a place shared with an intro beat: ' + c)
        g.ev("(() => { window.__said = []; const old = bubbleSay; bubbleSay = function (h, text, s) { window.__said.push([clockText(), text]); return old.apply(this, arguments); }; return true; })()")
        beats = g.ev("INTRO_WEEK.filter(b => b.who && introBeatLines(b).length).map(b => b.id)")
        only = [x.split('=', 1)[1].split(',') for x in sys.argv if x.startswith('--beats=')]   # e.g. --week --beats=d4-quiz,d5-invite
        if only: beats = [b for b in beats if b in only[0]]
        if not beats: print('  no beats walked: none match --beats' if only else '  not yet: the writers\' beat lines are not in this build')
        for bid in beats:
            go = g.ev("""((id) => { const b = INTRO_WEEK.find(x => x.id === id), from = introAbs(b.day, b.at);
              if (shipNow() < from + 1) skipTo(from + 1);
              const p = ROSTER.find(q => q.id === b.who), w = whereIs(p, shipNow());
              const deck = b.where && b.where !== 'seek' ? b.where.deck : w && w.deck;
              if (deck && deck !== deckDef.num) goToDeck(deck);
              return { t: clockText(), deck, plan: w && [w.deck, w.act, w.placeId] }; })""" + f"('{bid}')")
            g.step(30)
            place = """((id) => { const b = INTRO_WEEK.find(x => x.id === id), a = DECK_CREW.find(x => x.p && x.p.id === b.who);
              let tgt = null;
              if (b.where && b.where !== 'seek') {
                const L = Object.keys(ROOMS).find(k => ROOMS[k].name === b.where.room), T = [];
                deckDef.map.forEach((row, r) => [...row].forEach((ch, c) => { if (ch === L) T.push([c, r]); }));
                const ref = a ? cellAt(a.x, a.z) : T[T.length >> 1]; T.sort((u, v) => Math.hypot(u[0] - ref[0], u[1] - ref[1]) - Math.hypot(v[0] - ref[0], v[1] - ref[1]));
                tgt = T.find(c => free(...c) && !(a && c[0] === cellAt(a.x, a.z)[0] && c[1] === cellAt(a.x, a.z)[1]));
              } else if (a) { const n = nearestOpen(a.x + 1, a.z + 1, player); tgt = n; }
              if (tgt) player.obj.position.copy(cellPos(...tgt));
              return { here: player.here(), them: a ? cellAt(a.x, a.z) : null }; })"""
            g.page.evaluate('([s, id]) => window.__sc(s)(id)', [place, bid])
            n0 = len(g.ev('window.__said'))
            seen = False
            for k in range(160):   # a teacher can reach the room late; then up to 12 lines at 3.6 s
                g.step(20); g.page.evaluate('([s, m]) => window.__sc(s)(m)', [WALK_TICK, 'stand'])
                st = g.ev(f"(() => {{ const b = INTRO_WEEK.find(x => x.id === '{bid}'); return {{ said: SHIP.intro.done['{bid}:said'] !== undefined, playing: !!INTRO_UI.beat, here: introBeatHere(b, DECK_CREW.find(x => x.p && x.p.id === b.who)) }}; }})()")
                seen = seen or st['here']
                if st['said'] and not st['playing']: break
                if k % 10 == 9 and not st['here']: g.page.evaluate('([s, id]) => window.__sc(s)(id)', [place, bid])   # they moved: go to them again
            lines = g.ev(f"introBeatLines(INTRO_WEEK.find(x => x.id === '{bid}'))")
            said = [x[1] for x in g.ev('window.__said')[n0:]]
            heard = sum(1 for l in lines if l in said)
            print(f"  {bid} ({go['t']}, plan {go['plan']}): heard {heard}/{len(lines)}{'' if seen else ' -- the teacher was never there with you'}")
            if heard < len(lines): fail(f'{bid}: you stayed, but heard {heard} of {len(lines)} of the teacher\'s lines; missing {[l for l in lines if l not in said]}; dialogue {g.ev("DIALOGUE && DIALOGUE.id")}; said meanwhile {said[:8]}')
        if 'd6-sowing' in beats:
            sow = g.ev("({ sow: !!INTRO_UI.sow, at: (DECK_CREW.find(x => x.p.id === 'tomas') || {}).goalId || null })")
            print(f'  Sowing: Tomas brought to the garden {sow}')
            if not sow['sow']: fail('Tomas was never brought to the garden for Sowing')

# part 13, also on its own: python3 intro_check.py BUILD.html --firsts (onboarding 5, 0.42.60-0.42.62, the 0.63.2 playtest):
# the first-time arrows (the servery after the Chief's "Eat something", the time clock after Day 1's opener, the job
# board once clocked in, gone once a job's taken), the first night's call-home card and its Track it arrow, and Zeke's
# the playtest patch 1, #7 (the user: "the Chief's first solo job: the cut scene starts, then nothing happens"): Tuesday
# 08:45 in the real game, you walk into her office and read her meeting through. Once it closes the solo job must be yours
# AND tracked like a job taken at the board, its own marker on screen and a toast naming it, and nothing else may take the
# arrow while you're on it (sampled to 10:40: Zeke's Rounds ask, told at 06:00 before, took it); the Rounds ask (his
# Mail) not before her meeting is over; her words say how (the board, turn it in) and never put Torres on Deck 6. Then
# each step moves the arrow like a board job: the shelf, the shop, the machine, back to the board; turned in, it's done
def solo(g):
    print('14. Tuesday\'s first solo job in the real game: after the Chief\'s meeting it\'s yours and tracked, and keeps the arrow')
    if not g.ev("typeof jobReserved === 'function' && typeof myJob === 'function'"):
        print('  not yet: no jobReserved'); return
    SEEN = "(() => { const el = document.getElementById('ixGoal'), id = SHIP.jobs.find(x => x.reserved === 3 && x.status !== 'done'); return { t: clockText().slice(-5), dlg: DIALOGUE ? DIALOGUE.id : null, shown: !!el && !el.hidden, label: el && !el.hidden ? el.children[2].textContent : '', goal: IX_GOAL ? IX_GOAL.label : null, track: SHIP.player.track === undefined ? 'unset' : SHIP.player.track, job: id ? id.id : null, mine: myJob() ? myJob().id : null }; })()"
    g.ev('localStorage.clear()'); g.ev('newGameStart(true)'); g.step(5)
    g.page.fill('form input[maxlength="24"]', 'Sam'); g.page.click('form button'); g.step(5)
    g.ev("window.__solo = []; { const t0 = toast; toast = (a, b) => { window.__solo.push([Math.floor(shipNow()), String(a), String(b)]); return t0(a, b); }; }")
    g.ev('skipTo(introAbs(1, 8 * 60 + 40))'); g.ev('(() => { goToDeck(5); player.obj.position.copy(cellPos(15, 3)); })()'); g.step(60)   # Monday in the bay
    g.ev("SHIP.intro.done['d1-shadow:job'] = introAbs(1, 11 * 60)")   # and Monday's shadow job done, as in play: Tuesday's Rounds ask then comes at 06:00
    g.ev('skipTo(introAbs(2, 8 * 60 + 35))'); g.ev('(() => { goToDeck(5); player.obj.position.copy(cellPos(15, 3)); })()'); g.step(5)
    g.ev("SHIP.player.track = null")                    # as after Day 1's Tracked items (a real Tuesday has it off)
    g.ev("for (const k of NEED_KEYS) SHIP.player.needs[k] = 95")   # had breakfast and a wash (the skip from Sunday leaves you starving: the need marker would rightly lead)
    g.ev("playerGo(DECKS[5].places.find(q => q.id === '5-office-visit-1').at)")
    met = None
    for i in range(80):
        g.step(30); met = g.ev('DIALOGUE && DIALOGUE.id')
        if met: break
    if not met or not met.startswith('introSoloJob'): fail(f'Tuesday\'s solo job meeting did not play: {met}'); return
    said = g.ev("DIALOGUE.queue.filter(l => l.who === 'calder').map(l => l.text).join(' ')")
    n = 0
    while g.ev('!!DIALOGUE') and n < 40:
        g.ev("(() => { const l = DIALOGUE.queue[DIALOGUE.i]; if (l && l.choice) dialogueChoose(2); else dialogueNext(); })()"); g.step(60); n += 1
    end = g.ev("typeof SHIP.intro.done['d2-solo:end'] === 'number' ? SHIP.intro.done['d2-solo:end'] : Math.floor(shipNow())")   # when her panel closed
    g.step(30); after = g.ev(SEEN)
    print(f'  after her meeting: {after}')
    toasts = g.ev('window.__solo')
    named = [x for x in toasts if x[0] >= end - 6 and after['job'] and g.ev(f"(j => !!j && {json.dumps(' '.join(x[1:]))}.includes(j.title || jobCard(j)[0]))(SHIP.jobs.find(x => x.id === {json.dumps(after['job'])}))")]
    print(f'  toasts from her meeting\'s end: {[x[1] + ": " + x[2][:60] for x in toasts if x[0] >= end - 6][:3]}')
    if 'board' not in said.lower() or 'turn it in' not in said.lower(): fail('her words don\'t say how to do it (turn it in at the board)')
    if 'deck 6' in said.lower(): fail('her words still put Torres on Deck 6 (he shows you rounds this morning)')
    if not (after['job'] and after['mine'] == after['job'] and after['track'] == after['job']): fail(f'after her meeting the solo job is not yours and tracked: {after}')
    if not after['shown'] or after['goal'] is not None: fail(f'after her meeting the solo job\'s own marker is not up: {after}')
    if not named: fail('no toast naming the solo job when her meeting ended')
    bad = []
    while g.ev('shipNow() < introAbs(2, 10 * 60 + 40)'):
        g.step(150); w = g.ev(SEEN)
        if not (w['mine'] == after['job'] and w['track'] == after['job'] and w['goal'] is None and w['shown']): bad.append(w)
    print('  the arrow to 10:40:', 'the solo job\'s throughout' if not bad else bad[:2])
    if bad: fail(f'something else took the arrow from the solo job before 10:40: {bad[:2]}')
    ask = g.ev("(() => { const c = SHIP.works && SHIP.works.cur, m = c && c.mail && SHIP.mail.find(x => x.subject === c.mail); return { cur: c ? c.id : null, at: m ? m.at : null }; })()")
    print(f'  the Rounds ask: {ask} (her meeting ended {end})')
    if ask['cur'] == 'm1' and ask['at'] is not None and ask['at'] < end: fail(f'the Rounds ask came before her meeting was over: {ask}, end {end}')
    # step by step, as a board job: each part in hand moves the arrow on; the work done sends you back to the board
    jid = json.dumps(after['job'])
    # with the teaching arrows on (0.92.0) a training meeting takes the arrow from 15 minutes before (the arrows plan): Zeke's
    # 10:45 Rounds meeting has it from 10:30, so then the job's own step (ixJobStep, the arrow it gives back) is read
    meet = "(() => { const n = typeof guideNow === 'function' ? guideNow() : null; return n && /^train:.*:meet:/.test(n.id) ? ((ixJobStep() || {}).label || null) : undefined; })()"
    lab = lambda: (lambda m: g.ev(SEEN)['label'] if m is None else m)(g.ev(meet))
    shelf = g.ev(f"(j => SHIP.stores[j.parts[0]] || 0)(SHIP.jobs.find(x => x.id === {jid}))")   # the crew may have used the shelf's last one by now (then you make it in the shop, as for any job)
    steps = [lab()]
    g.ev(f"(j => {{ takePart(j.parts[0]); SHIP.player.carry.push(j.parts[0]); }})(SHIP.jobs.find(x => x.id === {jid}))"); g.step(30); steps.append(lab())
    g.ev(f"(j => {{ SHIP.player.carry.push(j.parts[1]); if (SHIP.player.work && SHIP.player.work.make) SHIP.player.work.make = null; }})(SHIP.jobs.find(x => x.id === {jid}))"); g.step(30); steps.append(lab())
    g.ev(f"(j => {{ jobStops(j).forEach((s, k) => jobStepDone(j.id, k)); SHIP.player.carry.length = 0; if (!j.workDone) finishJob(j.id); }})(SHIP.jobs.find(x => x.id === {jid}))"); g.step(30); steps.append(lab())
    app = g.ev(f"(() => {{ const j = SHIP.jobs.find(x => x.id === {jid}); return typeof jobCard === 'function' && !!j && myJob() === j; }})()")
    t_in = g.ev(f"turnInJob({jid})"); g.step(30); fin = g.ev(SEEN)
    print('  the arrow, step by step (' + str(shelf) + ' on the shelf):', ' > '.join(steps), '| turned in:', t_in, '| after:', fin['mine'], fin['track'])
    want = [r'fetch ' if shelf > 0 else r'make ', r'(make |look over )', r'repair ', r'turn it in at the job board']   # (off its deck: 'Take the lift to Deck 4: ...'; the machine shows what else it needs, as for any job)
    import re as _re
    if len(steps) != 4 or not all(_re.search(w, (x or '').lower()) for w, x in zip(want, steps)): fail(f'the solo job\'s arrow does not walk its steps like a board job: {steps}')
    if not app: fail('the solo job is not your job (myJob) through its steps')
    if not t_in or fin['mine']: fail(f'the solo job could not be turned in at the board: {t_in}, {fin}')

# item 81 (FE2 on 0.92.0, LEAD31-13): Tuesday 08:51, in the Works bay. The Tracked arrow for the solo job points at the spot
# you stand at in the Chief's office, not her seat; a real tap on her (as FE2 tapped the pin over her desk) walks you in and
# her meeting starts; once it has been (or outside its time), a tap on her is her card as before, no walk

with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844)
    g.ev('localStorage.clear()'); g.ev('newGameStart(true)'); g.step(5)
    g.page.fill('form input[maxlength="24"]', 'Sam'); g.page.click('form button'); g.step(5)
    g.ev('skipTo(introAbs(1, 8 * 60 + 52))'); g.ev("for (const k of NEED_KEYS) SHIP.player.needs[k] = 95")
    print('done flags', g.ev("JSON.stringify(Object.keys(SHIP.intro.done).filter(k => k.startsWith('d1-b')))"))
    g.ev("(() => { goToDeck(5); })()"); g.step(10)
    # a cell outside the Works bay, on Deck 5, reachable
    info = g.ev("""(() => { const key = Object.keys(ROOMS).find(k => /^Works bay$/.test(ROOMS[k].name || '')); let first = null;
      for (let j = 0; j < D && !first; j++) for (let i = 0; i < W && !first; i++) if (MAP[j][i] === key) first = [i, j];
      const a = DECK_CREW.find(c => c.p.id === 'calder'); return { key, first, calder: a ? [a.x.toFixed(1), a.z.toFixed(1), ROOMS[roomAt(...cellAt(a.x, a.z))].name] : null, here: player.here(), room: ROOMS[roomAt(...player.here())].name }; })()""")
    print(info)
    # move outside: the first cell of another room (cargo hold 'c')
    g.ev("(() => { let to=null; for (let j = 0; j < D && !to; j++) for (let i = 0; i < W && !to; i++) if (MAP[j][i] === 'c') to = [i, j]; player.obj.position.copy(cellPos(...to)); player.path.length = 0; })()"); g.step(5)
    r = g.ev("(() => { const a = DECK_CREW.find(c => c.p.id === 'calder'); if (!a) return 'no calder'; const ok = introMeetGo(a.p); return [ok, player.path.length, player.path.length ? player.path[player.path.length-1] : null]; })()")
    print('introMeetGo calder Day1 08:5x from the cargo hold:', r)
    met = None
    for i in range(60):
        g.step(30); met = g.ev("DIALOGUE && DIALOGUE.m ? DIALOGUE.m.id : null")
        if met: break
    print('then', met, g.ev('clockText()'), g.ev('ROOMS[roomAt(...player.here())].name'), g.ev('player.here()'))
    g.close()
