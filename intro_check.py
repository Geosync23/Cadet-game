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
#      starts; at 08:35 (before it) and 10:05 a tap on her doesn't (--solotap: this part alone)
#   20. (CH1) a save and reload on the third card of Zeke's dinner chat: the Chief sat till then, then over and her welcome (--dinner: this part alone)
#   Later waves (shown as "not yet"): the reserved jobs, the week in play, Sowing's draw calls.
# Setup and environment as for cadet_test.py.
# Run:  python3 intro_check.py BUILD.html
import sys, json
exec(open(__file__.replace('intro_check.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
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
def solo_tap(g):
    print('18. Tuesday 08:51: the solo job\'s arrow at your spot in her office, a tap on the Chief walks you in and it starts; later her card')
    g.ev('localStorage.clear()'); g.ev('newGameStart(true)'); g.step(5)
    g.page.fill('form input[maxlength="24"]', 'Sam'); g.page.click('form button'); g.step(5)
    g.ev('skipTo(introAbs(1, 8 * 60 + 40))'); g.ev("SHIP.intro.done['d1-shadow:job'] = introAbs(1, 11 * 60)")
    g.ev('skipTo(introAbs(2, 8 * 60 + 35))'); g.ev("for (const k of NEED_KEYS) SHIP.player.needs[k] = 95")
    HERE = "(() => { goToDeck(5); player.obj.position.copy(cellPos(12, 5)); player.path.length = 0; if (SHIP.device && SHIP.device.settings) SHIP.device.settings.tips = false; const t = document.getElementById('devTip'); if (t) t.hidden = true; })()"   # a first-time tip card can sit over her (as interactions_check)
    g.ev(HERE); g.step(60)
    row = g.ev("(trkItems().find(x => x.title === DEV_BEATS['d2-solo']) || {})")
    goal = row.get('goal') or {}
    print(f"  Tracked: {row.get('title')} -> {goal}")
    if goal.get('place') != '5-office-visit-1': fail(f'the solo job\'s Tracked arrow is not at your spot in her office: {goal}')
    # a point on her the canvas takes (a speech bubble or a toast can cover part of her, as for a player, who'd tap the rest)
    TAP = """(() => { const a = DECK_CREW.find(c => c.p.id === 'calder'); if (!a) return null; const room = ROOMS[roomAt(...cellAt(a.x, a.z))].name; let first = null;
      for (const h of [.9, .5, 1.2, .7, 1.4]) for (const dx of [0, -8, 8]) { const v = new THREE.Vector3(a.x, (a.y || 0) + h, a.z).project(camera), x = (v.x + 1) * innerWidth / 2 + dx, y = (1 - v.y) * innerHeight / 2;
        const e = document.elementFromPoint(x, y), c = crewAtScreen(x, y); if (!first) first = (e && e.closest('[id]') ? e.closest('[id]').id : e && e.tagName) || '?';
        if (e && e.tagName === 'CANVAS' && c && c.p.id === 'calder') return [x, y, room, 'canvas']; }
      return [0, 0, room, 'covered by ' + first]; })()"""
    # 08:35 (RV11): she's at her desk from 08:25 (early: 20), but her meeting isn't on yet: a tap on her is her card, no walk
    pt = g.ev(TAP)
    if pt and pt[3] == 'canvas':
        g.page.mouse.click(pt[0], pt[1]); g.step(5)
        early = g.ev("({ path: player.path.length, dlg: !!DIALOGUE, room: ROOMS[roomAt(...player.here())].name })")
        print(f'  08:35, before her meeting: a tap on her: {early}')
        if early['path'] or early['dlg']: fail(f'at 08:35, before her meeting, a tap on the Chief walked you in or started it: {early}')
    else: fail(f'08:35: no point on the Chief in her office to tap: {pt}')
    g.ev('(() => { if (typeof chatClose === "function") chatClose(); })()'); g.ev('skipTo(introAbs(2, 8 * 60 + 51))'); g.ev(HERE); g.step(60)
    pt = g.ev(TAP)
    if not pt or pt[2] != "Works Chief's office": fail(f'the Chief is not in her office at 08:51: {pt}'); return
    print(f'  the tap on her: {pt}')
    if pt[3] != 'canvas': fail(f'no point on the Chief to tap: {pt}'); return
    g.page.mouse.click(pt[0], pt[1]); g.step(5)
    walking = g.ev('player.path.length')
    met = None
    for i in range(40):
        g.step(30); met = g.ev("DIALOGUE && DIALOGUE.m ? DIALOGUE.m.id : null")
        if met: break
    print(f"  a tap on her from the bay at 08:51: walking {walking > 0}, then {met} at {g.ev('clockText()')[-5:]} in {g.ev('ROOMS[roomAt(...player.here())].name')}")
    if not walking: fail('a tap on the Chief from the bay during her meeting\'s time did not walk you in')
    if met != 'intro-d2-solo': fail(f'her solo job meeting did not start after the tap: {met}')
    n = 0
    while g.ev('!!DIALOGUE') and n < 40:
        g.ev("(() => { const l = DIALOGUE.queue[DIALOGUE.i]; if (l && l.choice) dialogueChoose(2); else dialogueNext(); })()"); g.step(60); n += 1
    g.ev('skipTo(introAbs(2, 10 * 60 + 5))'); g.ev(HERE); g.step(60)
    pt = g.ev(TAP)
    if pt and pt[3] == 'canvas':
        g.page.mouse.click(pt[0], pt[1]); g.step(5)
        late = g.ev("({ path: player.path.length, dlg: !!DIALOGUE, card: !!(document.querySelector('.chat:not([hidden]), #chat:not([hidden])') || (document.getElementById('tt') || {}).textContent) })")
        print(f'  10:05, the meeting over: a tap on her: {late}')
        if late['path'] or late['dlg']: fail(f'at 10:05 a tap on the Chief still walked you in or started a meeting: {late}')
    else: print('  10:05: the Chief is not on Deck 5 (her card not tapped)')

# Day 1 tea (he explains it, leads you to the Tea corner once your first job's turned in, waits for your tea, follows again)
def clock_tracked(g):
    # fresh-eyes (FE1 item 36): on Day 1 you tap Tracked's "Clock in" on Deck 4, Zeke walks you down, you step out on Deck 5:
    # the arrow stays the clock's until you've clocked in (it was replaced by Zeke's and cleared when he let you go)
    print('13b. Tracked "Clock in" stays up on the training day until you punch')
    if not g.ev("typeof clockTrkItem === 'function'"):
        print('  not yet: no clockTrkItem'); return
    g.ev('localStorage.clear()'); g.ev('newGameStart(true)'); g.step(5)
    g.page.fill('form input[maxlength="24"]', 'Sam'); g.page.click('form button'); g.step(5)
    g.ev("skipTo(introAbs(1, 8 * 60 + 30))"); g.ev("(() => { if (typeof DIALOGUE !== 'undefined' && DIALOGUE) dialogueEnd(); goToDeck(4); })()"); g.step(10)
    G = "(IX_GOAL ? IX_GOAL.trk || IX_GOAL.label : null)"
    tap = g.ev("(() => { const it = clockTrkItem(); if (!it) return null; setGoal(it.goal); return it.goal.trk; })()")
    seen = []
    for k in range(4): g.step(30); seen.append(g.ev(G))
    g.ev("goToDeck(5)"); g.step(5)
    for k in range(4): g.step(30); seen.append(g.ev(G))
    walk = g.ev("""(() => { const s = placeSpot('5-timeclock-1'), t = (ROOM_TILES.w || []).filter(c => free(...c)).map(c => [c, cellPos(...c)]).filter(([, w]) => Math.hypot(w.x - s.x, w.z - s.z) > 4).sort((a, b) => Math.hypot(a[1].x - s.x, a[1].z - s.z) - Math.hypot(b[1].x - s.x, b[1].z - s.z))[0];
      if (!t) return null; player.obj.position.copy(t[1]); player.stop(); return [roomAt(...player.here()), Math.round(Math.hypot(t[1].x - s.x, t[1].z - s.z) * 10) / 10]; })()""")   # into the Works bay, a few metres from the clock (RV8: arriving in the bay took it down)
    for k in range(8): g.step(30); seen.append(g.ev(G))
    print('  in the Works bay, away from the clock:', walk)
    print('  tracked', tap, '| the arrow after, on Deck 4 then Deck 5:', sorted(set(map(str, seen))))
    if tap != 'clock:in' or any(x != 'clock:in' for x in seen): fail(f'Tracked "Clock in" did not stay up till you punched: {seen}')
    punched = g.ev("(() => { careerClock(shipNow()); for (let i = 0; i < 3; i++) clockRemindTick(shipNow()); return [careerClockedIn(SHIP.time.day), IX_GOAL && IX_GOAL.trk || null]; })()")
    print('  punched in:', punched)
    if not punched[0] or punched[1] == 'clock:in': fail(f'after clocking in the clock arrow should go: {punched}')

# 14. Leaving the bunk room early (0.64.15's playtest: "after the bag, Zeke just stands in the bunk room"): a player who
# walks out into the corridor right after putting the bag away (or without putting it away) must still get the device from
# Zeke and be led on to the mess; on 0.64.15 he waited in Bunk 1 for good (the 'device' step wanted you in there)
def bunk_leave(g):
    print('14. Leaving Bunk 1 early: the device and the walk on still come')
    if not g.ev("typeof INTRO_STEPS !== 'undefined' && INTRO_STEPS.some(s => s.id === 'device')"):
        print('  not yet: no device step'); return
    url = g.page.url.split('?')[0]
    # how: 'stay' never puts the bag away and stays in Bunk 1, 'out' the corridor after the bag, 'nobag' the corridor without it, 'deck' the lift to Deck 3 after the bag,
    # 'reload' a save and reload in the device step, then the corridor (the lead 27's cases)
    for how in ('stay', 'out', 'nobag', 'deck', 'reload'):
        if how == 'reload':
            g.page.evaluate('localStorage.clear()')
            g.page.goto(url + '?debug', timeout=RELOAD_MS); g.page.wait_for_function('window.__sc !== undefined || window.__err', timeout=60000); g.step(5)
            if not g.ev("!!document.querySelector('form input[maxlength=\"24\"]')"): g.ev('localStorage.clear(); newGameStart(true)'); g.step(5)   # (an earlier part's save on this page: arrive anew)
        else:
            g.ev('localStorage.clear()'); g.ev('CLOTHES_ON = true'); g.ev('newGameStart(true)'); g.step(5)
        g.ev("(() => { if (DIALOGUE) dialogueEnd(true); const f = document.querySelector('form input[maxlength=\"24\"]'); f.value = 'Sam'; f.form.requestSubmit(); })()"); g.step(20)   # (a panel left from the last run may cover the button)
        for k in range(500):
            g.step(20)
            if g.ev("SHIP.intro.step === 'stow' && !DIALOGUE"): break
            g.page.evaluate('([s, m]) => window.__sc(s)(m)', [WALK_TICK, 'follow'])
        t0 = g.ev('Math.floor(shipNow())')
        if how not in ('nobag', 'stay'): g.ev("(() => { const w = clothesWardrobe(); if (w && w.tile) player.obj.position.copy(cellPos(...w.tile)); wardrobeUse(); })()"); g.step(10)
        if how == 'reload':
            for k in range(60):
                g.step(10)
                if g.ev("SHIP.intro.step === 'device'"): break
            g.ev('saveGame()')
            g.page.goto(url + '?debug', timeout=RELOAD_MS); g.page.wait_for_function('window.__sc !== undefined || window.__err', timeout=60000); g.step(10)
        if how == 'deck': g.ev('goToDeck(3)'); g.step(10)
        elif how != 'stay': g.ev("(() => { player.path.length = 0; playerGo([11, 4]); })()")   # out into the junior corridor
        r = None
        if how in ('stay', 'nobag'):   # DS1 (the user, 2026-10-23): with the bag still in your hands he waits, as long as it takes, the arrow on your wardrobe; nobody stows it for you
            for k in range(60):
                g.step(30)
                if g.ev('!!DIALOGUE'): g.ev('(() => { const l = DIALOGUE.queue[DIALOGUE.i]; if (l && l.choice) dialogueChoose(1); else dialogueNext(); })()')
            w = g.ev("({ m: Math.floor(shipNow()), step: SHIP.intro.step, bag: bagHeld(), goal: IX_GOAL && IX_GOAL.label, zr: (a => a && (DECKS[4].rooms[roomAt(...cellAt(a.x, a.z))] || {}).name)(introWalker()), missed: SHIP.intro.missed.slice() })")
            print(f"  {how}: {w['m'] - t0} ship minutes on with the bag: step {w['step']}, bag {w['bag']}, arrow {w['goal']!r}, Zeke in {w['zr']}")
            if w['step'] != 'stow' or not w['bag'] or w['goal'] != 'Put your bag in your wardrobe' or w['missed']: fail(f"{how}: with the bag in your hands he should wait at the bag step, the arrow on your wardrobe: {w}")
            g.ev("(() => { const w = clothesWardrobe(); if (w && w.tile) player.obj.position.copy(cellPos(...w.tile)); wardrobeUse(); })()"); g.step(10)   # now you put it in
            t0 = g.ev('Math.floor(shipNow())')
        for k in range(200):
            g.step(30)
            if g.ev('!!DIALOGUE'): g.ev('(() => { const l = DIALOGUE.queue[DIALOGUE.i]; if (l && l.choice) dialogueChoose(1); else dialogueNext(); })()')
            if g.ev("typeof DEV !== 'undefined' && DEV.open"): g.ev('deviceClose()')   # DS1: his Mail on your device after the hand-over, read and closed
            r = g.ev("({ t: clockText(), m: Math.floor(shipNow()), step: SHIP.intro.step, dev: introFlag('intro.device'), given: SHIP.intro.done['device:given'], bag: bagHeld(), deck: deckDef.num, z: (a => a && cellAt(a.x, a.z))(introWalker()), zr: (a => a && deckDef.num === 4 ? introRoomAt(4, cellAt(a.x, a.z)) : null)(introWalker()) })")
            if r['step'] not in ('stow', 'device') and r['zr'] != 'Bunk 1' and (r['dev'] or how == 'deck'): break
        took = r['m'] - t0
        print(f"  {how}: {took} ship minutes later step {r['step']}, device {r['dev']} (in person: {r['given'] is not None}), bag in hands {r['bag']}, you on Deck {r['deck']}, Zeke at {r['z']} ({r['zr']})")
        if r['step'] in ('stow', 'device') or r['zr'] == 'Bunk 1' or not r['dev'] and how != 'deck' or r['bag'] or took > (20 if how == 'deck' else 12):   # (deck: you left him: the device waits for Monday's briefing, as for a missed bunk)
            fail(f"leaving Bunk 1 ({how}): the evening never moved on, or no device ({r})")
        if how in ('stay', 'out', 'nobag', 'reload') and r['given'] is None: fail(f'the device was not handed over in person when you left the room ({how}): {r}')
    g.page.evaluate('localStorage.clear()')

# 15. The talk steps with you near but not there (OR2, after 0.64.15): during 'bunk' you stand in the corridor just
# outside Bunk 1, during 'table' in the mess away from your table, both within his 10 tiles. On 2b4a05db he waited until
# 18:00; now the step moves on (missed, its gist by Mail) INTRO_HOLD_MAX + 5 minutes after it became yours
# part 16 (DS1, FE2 on 0.92.0: "Zeke stands by the Deck 5 lift, silent, for 35 minutes"): a player who walks beside him,
# 2 tiles off and never onto a step's own spot (he stands on it himself), from the ramp to the servery. Every step comes
# (none missed), the Works bay door is passed within 10 ship minutes of his reaching it, the bunk talk plays, and dinner's
# table by 18:45. Also on its own: python3 intro_check.py BUILD.html --beside
def beside_walk(g):
    print('16. Beside him, not on the spot: a player who stops 2 tiles off him (never on a step\'s spot) gets the whole evening')
    g.ev('localStorage.clear()'); g.ev('CLOTHES_ON = true'); g.ev('newGameStart(true)'); g.step(5)
    g.ev("(() => { if (DIALOGUE) dialogueEnd(true); const f = document.querySelector('form input[maxlength=\"24\"]'); f.value = 'Sam'; f.form.requestSubmit(); })()"); g.step(160)
    at, dlgs, still = {}, set(), {}
    hm = lambda x: int(x[-5:-3]) * 60 + int(x[-2:])   # 'HH:MM' -> minutes
    for k in range(2000):
        g.step(20)
        st = g.ev('SHIP.intro.step')
        r = g.page.evaluate('([s, m]) => window.__sc(s)(m)', [WALK_TICK, 'follow' if st in ('servery', 'table', 'chief', 'free', 'tomas', 'night', None) else 'beside'])
        m = hm(r['t']); at.setdefault(r['step'], m)
        if r['dlg']: dlgs.add(r['dlg'])
        if r['step'] == 'works' and r['esc'] and r['esc'][0] == [16, 6] and r['deck'] == 5:   # he's at the Works bay door
            if 'works' not in still:   # (lead 31) a tap on him: his usual card, no chat, and the tour goes on
                tap = g.ev("(() => { const a = DECK_CREW.find(x => x.p && x.p.id === INTRO_ESCORT), seen = []; const t0 = toast; toast = function (t, x, o) { seen.push(t + ': ' + x); return t0.apply(this, arguments); }; const r = introTap(a.p); toast = t0; return { r, seen, dlg: !!DIALOGUE, chat: typeof CHAT !== 'undefined' && !!CHAT }; })()")
                print(f'  a tap on him at the Works door: {tap}')
                if not (tap['r'] and any(x.startswith('Zeke Torres: ') for x in tap['seen']) and not tap['dlg'] and not tap['chat']): fail(f'a tap on him during the tour should show his card (no chat): {tap}')
            still.setdefault('works', m)
        if r['step'] in ('table', 'chief', 'free', None): break
    missed = g.ev('SHIP.intro.missed.slice()'); done = g.ev("(() => { const D = SHIP.intro.done, out = {}; for (const k of ['works', 'lift', 'wing', 'bunk', 'beside:works', 'beside:bunk']) out[k] = D[k] === undefined ? null : hhmm(((D[k] % 1440) + 1440) % 1440); return out; })()")
    print(f"  steps began: {sorted(((v, k) for k, v in at.items()))}; done: {done}; missed: {missed}; talks: {sorted(dlgs)}")
    if missed: fail(f'walking beside him (not on the spot), steps were missed: {missed}')
    w0, w1 = still.get('works'), done.get('works') and hm(done['works'])
    if w0 is None or w1 is None or w1 - w0 > 10: fail(f'at the Works bay door he waited {None if w0 is None or w1 is None else w1 - w0} ship minutes with you beside him (at most 10)')
    if not any(str(d).startswith('introBunk') for d in dlgs): fail(f'walking beside him, the bunk talk never played: {sorted(dlgs)}')
    if 'table' not in at or at['table'] > 18 * 60 + 45: fail(f"walking beside him, dinner's table only at {at.get('table')}")

# part 17 (DS1, FE2 on 0.92.0: Calder's "Missed you at dinner" came while Zeke was still taking them to dinner): late on the
# way (the clock on to 19:32 at the servery step), with him all the way past her step's 19:45: no Mail from her (on 685af944 it
# came at 19:45, the table and her steps missed)
def late_dinner(g):
    print('17. Late to dinner, with him: Calder\'s "Missed you at dinner" Mail never comes while he\'s still taking you')
    g.ev('localStorage.clear()'); g.ev('CLOTHES_ON = true'); g.ev('newGameStart(true)'); g.step(5)
    g.ev("(() => { if (DIALOGUE) dialogueEnd(true); const f = document.querySelector('form input[maxlength=\"24\"]'); f.value = 'Sam'; f.form.requestSubmit(); })()"); g.step(160)
    for k in range(2000):
        g.step(20)
        r = g.page.evaluate('([s, m]) => window.__sc(s)(m)', [WALK_TICK, 'follow'])
        if r['step'] == 'servery' and r['deck'] == 3: break
    if g.ev("SHIP.intro.step !== 'servery'"): fail('part 17: never reached the servery step'); return
    g.ev('skipTo(introAbs(0, 19 * 60 + 32))'); g.step(10)
    near = []
    for k in range(400):
        g.step(20)
        r = g.page.evaluate('([s, m]) => window.__sc(s)(m)', [WALK_TICK, 'beside'])
        near.append(g.ev("introWithEscort({ deck: deckDef.num, tile: player.here() })"))
        if g.ev('shipNow() >= introAbs(0, 19 * 60 + 58)'): break
    m = g.ev("(SHIP.mail || []).filter(x => x.from === 'I. Calder' && /Missed you at dinner/.test(x.body || '')).map(x => hhmm(((x.at % 1440) + 1440) % 1440))")
    st = g.ev("({ t: clockText(), step: SHIP.intro.step, chief: SHIP.intro.done.chief, missed: SHIP.intro.missed.slice() })")
    print(f"  with him {sum(near)}/{len(near)} frames to {st['t']}; step {st['step']}; missed {st['missed']}; Calder's Mail: {m}")
    if not all(near): fail('part 17: the walker lost him (the check needs you with him all the way)')
    if m: fail(f'Calder\'s "Missed you at dinner" Mail came while he was still with you: {m}')

# part 20 (CH1, the user on 0.99.1): a save and reload in the middle of Zeke's dinner chat. The chat is not replayed; the Chief,
# still at the next table, gets up then (there's no chat left to wait for), walks over, sits, and gives her welcome
def dinner_reload(g):
    print('20. A reload mid-dinner: the Chief sat through the chat\'s first cards, then over to your table and her welcome after the reload')
    url = g.page.url.split('?')[0]
    g.page.evaluate('localStorage.clear()')
    g.page.goto(url + '?debug', timeout=RELOAD_MS); g.page.wait_for_function('window.__sc !== undefined || window.__err', timeout=60000); g.step(5)
    if not g.ev("!!document.querySelector('form input[maxlength=\"24\"]')"): g.ev('localStorage.clear(); newGameStart(true)'); g.step(5)
    g.ev('CLOTHES_ON = true')
    g.ev("(() => { if (DIALOGUE) dialogueEnd(true); const f = document.querySelector('form input[maxlength=\"24\"]'); f.value = 'Sam'; f.form.requestSubmit(); })()"); g.step(160)
    for k in range(3000):
        g.step(20)
        if g.ev("!!DIALOGUE && /^introDinner/.test(DIALOGUE.id || '')"): break
        g.page.evaluate('([s, m]) => window.__sc(s)(m)', [WALK_TICK, 'follow'])
    if not g.ev("!!DIALOGUE && /^introDinner/.test(DIALOGUE.id || '')"): fail('part 20: the dinner chat never began'); return
    g.step(80); before = []
    for _ in range(3):   # three cards at a player's pace (5 s a card), then save
        g.step(150); before.append([g.ev('DIALOGUE ? DIALOGUE.i : null'), g.ev('!!INTRO_UI.calder'), g.ev(CALDER_AWAY)])
        g.ev('(() => { const l = DIALOGUE.queue[DIALOGUE.i]; if (l && l.choice) dialogueChoose(1); else dialogueNext(); })()')
    saved = g.ev("(() => { saveGame(); return clockText(); })()")
    g.page.goto(url + '?debug', timeout=RELOAD_MS); g.page.wait_for_function('window.__sc !== undefined || window.__err', timeout=60000); g.step(10)
    up, welcome, end = None, None, None
    for k in range(400):
        g.step(30)
        if up is None and g.ev('!!INTRO_UI.calder'): up = g.ev('clockText()')
        if welcome is None and g.ev("!!DIALOGUE && /^introChief/.test(DIALOGUE.id || '')"): welcome = { 't': g.ev('clockText()'), 'in': g.ev('introCalderIn()') }
        if g.ev('!!DIALOGUE'): g.ev('(() => { const l = DIALOGUE.queue[DIALOGUE.i]; if (l && l.choice) dialogueChoose(1); else dialogueNext(); })()')
        end = g.ev("SHIP.intro.done['chief:end']")
        if end is not None or g.ev('shipNow() >= introAbs(0, 20 * 60)'): break
    print(f"  before the save at {saved} (card, the Chief up, m from her seat at the next table): {before}; after the reload she got up at {up}, her welcome {welcome}, ended {end}")
    if any(b[1] or b[2] is None or b[2] >= 1 for b in before): fail(f'part 20: the Chief left the next table during the first cards of the chat: {before}')
    if not up: fail('part 20: after a reload mid-dinner the Chief never got up to come over')
    if not welcome or not welcome['in']: fail(f"part 20: after a reload mid-dinner her welcome never played, or began before she'd sat at your table: {welcome}")
    elif end is None: fail('part 20: after a reload mid-dinner her welcome never ended')

# part 19 (DS1, the user's patch 0.92.3 items 1, 7-10), in one new game: the bedtime tip with the bunk's arrow on Day 0; Day 1's
# wardrobe arrow till you've changed; Tomas's wake-up lines without the towel one (its key retired, the next still said);
# Zeke's opener says clock in right after his hello; his "quiet days / the ship gets lively" pair comes early on the
# training day (else before his end-of-day words), his other follow lines still in order
def patch923(g):
    print('19. Patch 0.92.3: the bedtime tip, Day 1\'s change-clothes arrow, Tomas without the towel, Zeke\'s clock-in first, the "lively" pair on training day')
    g.ev('localStorage.clear()'); g.ev('CLOTHES_ON = true'); g.ev('newGameStart(true)'); g.step(5)
    g.ev("(() => { if (DIALOGUE) dialogueEnd(true); const f = document.querySelector('form input[maxlength=\"24\"]'); f.value = 'Sam'; f.form.requestSubmit(); })()"); g.step(20)
    # 1: the bunk's arrow after his goodnight brings the bedtime tip, once
    g.ev("skipTo(introAbs(0, 19 * 60 + 50))"); g.step(5)
    bt = g.ev("""(() => { const I = SHIP.intro; I.done.goodnight = Math.floor(shipNow()); delete I.done.bed; INTRO_UI.bed = false; INTRO_UI.goal = false; if (typeof clearGoal === 'function' && IX_GOAL) clearGoal();
      SHIP.device.settings.tips = true; delete SHIP.device.tipsSeen.bedtime; TIP_Q.length = 0; introBedTick();
      return { goal: IX_GOAL && IX_GOAL.label, seen: !!SHIP.device.tipsSeen.bedtime, text: (TIP_Q.find(x => x.id === 'bedtime') || {}).text || '' }; })()""")
    print(f"  #1 the bunk's arrow '{bt['goal']}', the bedtime tip: {bt['seen']} {bt['text'][:90]!r}")
    if not (bt['seen'] and '20:00' in bt['text']): fail(f'#1: no bedtime tip with the bunk\'s arrow (sleep from 20:00): {bt}')
    # 10: Tomas's wake-up lines
    tw = g.ev("introBeatLines(INTRO_WEEK.find(b => b.id === 'd1-wash'))")
    print(f'  #10 Tomas at 06:00: {tw}')
    if any('owel' in x for x in tw) or not any(x.startswith('Out the door') for x in tw) or len(tw) != 3: fail(f'#10: Tomas\'s wake-up lines should be three, no towel, "Out the door" still said: {tw}')
    # 7: Zeke's opener, clock in right after his hello, none removed
    op = g.ev("[1, 2, 3].map(n => (introWriterLine('walk.train.open.' + n) || [''])[0])")
    print(f'  #7 his opener: {op}')
    if not (op[0].startswith('Morning') and 'clock in' in op[1] and op[2].startswith('Anything')): fail(f'#7: his opener should be hello, clock in, then the rest: {op}')
    # 9: Day 1, up at 07:00 in yesterday's clothes: the wardrobe's arrow; changed: gone
    g.ev("skipTo(introAbs(1, 7 * 60))"); g.step(5)
    ch = g.ev("""(() => { const C = SHIP.clothes, I = SHIP.intro; delete I.done['arrow:change']; C.changed = 0; C.clean = Math.max(C.clean, 1);
      const a = introArrowWant(Math.floor(shipNow())); C.changed = SHIP.time.day; const b = introArrowWant(Math.floor(shipNow()));
      return { before: a, after: b, label: INTRO_ARROWS.change && INTRO_ARROWS.change.label }; })()""")
    print(f"  #9 Day 1 07:00: the arrow {ch['before']!r} ('{ch['label']}'), changed: {ch['after']!r}")
    if ch['before'] != 'change' or ch['after'] == 'change': fail(f'#9: Day 1\'s change-clothes arrow: {ch}')
    # 8: the pair after his first three follow lines, then the rest in order past them; else before his end-of-day words
    FT = """((n) => { const I = SHIP.intro, D = I.done, a = introWalker(); if (!a) return null; const said = [], ob = bubbleSay, of = introFollowing;
      D['follow:n'] = n; for (const k of [15, 16]) delete D['follow:' + k]; bubbleSay = (h, t) => { said.push(t); }; introFollowing = () => true;
      try { for (let i = 0; i < 4; i++) { INTRO_UI.followAt = -1e9; INTRO_UI.next = 0; INTRO_UI.sayEnd = 0;   /* (8 s since his last: the sim clock may be young) */ a.pose = 'walk'; player.obj.position.set(a.x + .5, player.obj.position.y, a.z); introFollowTick(); } }
      finally { bubbleSay = ob; introFollowing = of; } return { said, n: D['follow:n'], d15: D['follow:15'] !== undefined, d16: D['follow:16'] !== undefined, why: said.length ? null : { dlg: DIALOGUE && (DIALOGUE.id || 'dlg'), pose: a.pose, d: +Math.hypot(a.x - player.obj.position.x, a.z - player.obj.position.z).toFixed(2), sim: simNow() < (INTRO_UI.sayEnd || 0) || simNow() < INTRO_UI.next } }; })"""
    g.ev("skipTo(introAbs(1, 9 * 60 + 30))"); g.ev("goToDeck(5)"); g.step(30)
    for _ in range(60):
        if g.ev("!!introWalker()"): break
        g.step(10)
    want = g.ev("[3, 4, 5, 6, 14, 15, 16, 17].map(k => (introWriterLine('walk.follow.' + k) || [''])[0])")
    f1 = g.page.evaluate('([s, n]) => window.__sc(s)(n)', [FT, 3])
    print(f'  #8 after three follow lines: {f1}')
    if not f1 or f1['said'] != [want[5], want[6], want[1], want[2]]: fail(f'#8: after his third follow line, the "quiet / lively" pair, then lines 4 and 5: {f1}; wanted {want[5:7] + want[1:3]}')
    g.ev("for (const k of [15, 16]) SHIP.intro.done['follow:' + k] = 1")
    f2 = g.page.evaluate('([s, n]) => window.__sc(s)(n)', [FT.replace("for (const k of [15, 16]) delete D['follow:' + k];", ''), 14])
    print(f'  #8 at line 14, the pair already said: {f2}')
    if not f2 or not f2['said'] or f2['said'][0] != want[7]: fail(f'#8: past line 14 with the pair said, he goes on with line 17: {f2}')
    de = g.ev("""(() => { const I = SHIP.intro, D = I.done, a = introWalker(); if (!a) return null; D['follow:n'] = 5; for (const k of [15, 16, 'd1-end:told', 'd1-end:start']) delete D['follow:' + k], delete D[k];
      INTRO_UI.endQ = null; const said = [], ob = bubbleSay; bubbleSay = (h, t) => { said.push(t); };
      try { skipTo(introAbs(1, INTRO_DAYEND.at + 1)); player.obj.position.set(a.x + .5, player.obj.position.y, a.z); INTRO_UI.next = 0; if (DIALOGUE) dialogueEnd(true); introDayEndTick(); }
      finally { bubbleSay = ob; } return { said, q: (INTRO_UI.endQ || []).slice() }; })()""")
    print(f'  #8 never walked far enough: his end-of-day words {de}')
    if not de or not (de['said'] + de['q'])[1:3] == want[5:7]: fail(f'#8: the "quiet / lively" pair before his end-of-day words: {de}')

def talk_away(g):
    print('15. Near him but not at the spot: the bunk talk and the dinner chat still move on')
    for step, deck, spot in (('bunk', 4, [12, 4]), ('table', 3, [33, 3])):
        g.ev('localStorage.clear()'); g.ev('CLOTHES_ON = true'); g.ev('newGameStart(true)'); g.step(5)
        g.ev("(() => { if (DIALOGUE) dialogueEnd(true); const f = document.querySelector('form input[maxlength=\"24\"]'); f.value = 'Sam'; f.form.requestSubmit(); })()"); g.step(20)   # (a panel left from the last run may cover the button)
        for k in range(600):
            g.step(20)
            if g.ev(f"SHIP.intro.step === '{step}' && deckDef.num === {deck} && !DIALOGUE"): break
            g.page.evaluate('([s, m]) => window.__sc(s)(m)', [WALK_TICK, 'follow'])
        if g.ev(f"SHIP.intro.step !== '{step}'"): fail(f'never reached {step}'); continue
        t0 = g.ev('Math.floor(shipNow())'); g.ev(f"(() => {{ actEnd(true); player.path.length = 0; player.obj.position.copy(cellPos({spot[0]}, {spot[1]})); }})()")
        r = None
        for k in range(200):
            g.step(30)
            if g.ev('!!DIALOGUE'): g.ev('(() => { const l = DIALOGUE.queue[DIALOGUE.i]; if (l && l.choice) dialogueChoose(1); else dialogueNext(); })()')
            g.ev(f"(() => {{ if (deckDef.num === {deck} && (K(player.here()) !== K([{spot[0]}, {spot[1]}]) || ACT)) {{ actEnd(true); player.path.length = 0; player.obj.position.copy(cellPos({spot[0]}, {spot[1]})); }} }})()")   # stay put
            r = g.ev("({ t: clockText(), m: Math.floor(shipNow()), step: SHIP.intro.step, missed: SHIP.intro.missed.slice(), given: SHIP.intro.done['device:given'], z: (a => a && cellAt(a.x, a.z))(introWalker()), me: player.here() })")
            if g.ev("typeof DEV !== 'undefined' && DEV.open"): g.ev('deviceClose()')   # DS1: his Mail after the hand-over, read and closed
            if step == 'bunk' and g.ev("SHIP.intro.step === 'stow' && bagHeld()"): g.ev("(() => { const w = clothesWardrobe(); if (w && w.tile) player.obj.position.copy(cellPos(...w.tile)); wardrobeUse(); })()")   # DS1 (the user): nobody stows it for you, so you do, then back to your spot
            if r['step'] not in ((step, 'stow', 'device') if step == 'bunk' else (step,)) and (step != 'bunk' or g.ev("SHIP.intro.done['hand:end'] !== undefined || !introHandDue()")): break   # (bunk: on through the bag, the device and his hand-over)
        took = r['m'] - t0
        print(f"  {step}, you at {spot}: {took} ship minutes later step {r['step']}, missed {r['missed']}, device in person {r['given'] is not None}, Zeke at {r['z']}")
        if step == 'bunk' and r['given'] is None: fail(f'standing outside Bunk 1 through his bunk talk, the device never came from him in person ({r})')   # (OR2)
        if r['step'] == step or took > (25 if step == 'bunk' else 20): fail(f"standing near him but not at the spot during '{step}', the evening never moved on ({r})")
    g.page.evaluate('localStorage.clear()')

def firsts(g):
    print('13. First-time arrows, calling home, Zeke\'s Day 1 tea')
    if not g.ev("typeof introArrowTick === 'function'"):
        print('  not yet: no introArrowTick'); return
    G = "(typeof IX_GOAL !== 'undefined' && IX_GOAL ? IX_GOAL.label : null)"
    g.ev('localStorage.clear()'); g.ev('newGameStart(true)'); g.step(5)
    g.page.fill('form input[maxlength="24"]', 'Sam'); g.page.click('form button'); g.step(5)
    g.ev("skipTo(introAbs(0, INTRO_START.min + 70))"); g.ev("(() => { goToDeck(3); player.obj.position.copy(cellPos(28, 2)); })()"); g.step(5)
    g.ev("if (typeof bagHeld === 'function' && bagHeld()) bagStow(true)"); g.step(2)   # (DS1: nobody stows your bag for you; a player who skipped here would have; after a frame, past the ramp step that hands it over)
    g.ev("(() => { if (DIALOGUE) dialogueEnd(); INTRO_UI.chiefD = null; SHIP.intro.done['chief:met'] = SHIP.intro.done['chief:end'] = Math.floor(shipNow()); SHIP.player.tray = null; delete SHIP.intro.done['ate:last']; clearGoal(); })()"); g.step(20)
    eat = g.ev(G); card0 = g.ev("SHIP.intro.done['call:tip'] !== undefined")
    g.ev("SHIP.player.tray = 'Stew'"); g.step(10); eat2 = g.ev(G); card = ''
    for i in range(10):
        g.step(15); card = g.ev("(() => { const c = document.getElementById('devDlg'); return c && !c.hidden ? c.textContent : ''; })()")
        if 'Call home' in card: break
    if 'Call home' not in card: print('  (no card:', g.ev("({ dlg: DIALOGUE && DIALOGUE.id, choose: !!DEV.choose, panel: (document.getElementById('devDlg') || {}).hidden, keys: Object.keys(SHIP.intro.done).filter(k => /call|arrow|ate|chief/.test(k)).map(k => k + '=' + SHIP.intro.done[k]), arrow: INTRO_UI.arrow, chiefD: !!INTRO_UI.chiefD })"), ')')
    print(f"  the Chief says eat, no tray: arrow '{eat}', call card held back {not card0}; with a tray: arrow '{eat2}', call card {'up' if 'Call home' in card else 'not up'}")
    if eat != 'Get your dinner at the servery': fail(f'no servery arrow after the Chief told you to eat: {eat}')
    if eat2 == 'Get your dinner at the servery' or card0: fail(f'the servery arrow stayed with a tray in hand ({eat2}) or the call card came first ({card0})')
    if 'Call home' not in card: fail('no call-home card after the Chief\'s visit')
    else:
        g.ev("devChosen(0)"); g.step(20); tr = g.ev(G)
        g.ev("(() => { player.obj.position.copy(cellPos(37, 19)); })()"); g.step(20)
        mid = g.ev("({ g: " + G + ", place: IX_GOAL && IX_GOAL.place, end: SHIP.intro.done['call:end'] !== undefined })")
        # (0.92.0's evening: the crew may hold the other three booths; one is freed for the test, so a free one exists)
        moved = g.ev("""(() => { const was = INTRO_ARROWS.call.place, B = ['3-callhome-1', '3-callhome-2', '3-callhome-3', '3-callhome-4'], other = B.find(id => id !== was), h = DECK_CREW.filter(a => a.goalId === other), x = { goalId: was };
          h.forEach(a => a.goalId = null); DECK_CREW.push(x); introCallTick(Math.floor(shipNow())); const now = INTRO_ARROWS.call.place;
          DECK_CREW.splice(DECK_CREW.indexOf(x), 1); h.forEach(a => a.goalId = other); INTRO_ARROWS.call.place = was; return [was, now, other]; })()""")
        if moved[1] != moved[2]: fail(f"someone took the booth the call arrow was on, and it didn't move to the free one (FX5): {moved}")
        # FX5 (the user, 2026-10-23): in the room it still points at a booth, a free one, until the call begins (it went on walking
        # in); once the call's begun the call arrow is gone (the bunk arrow may come back)
        g.ev("(() => { const it = ITEMS.find(i => i.t === 'Booth ' + ((IX_GOAL && IX_GOAL.place) || '1').slice(-1)); it.hit.getWorldPosition(_wp); playerTap(it, _wp.clone(), _wp.clone()); })()")
        for i in range(40):
            g.step(10)
            if g.ev("!!ACT && ACT.kind === 'call' && ACT.phase !== 'walk'"): break
        g.step(20)
        end = g.ev("({ g: " + G + ", end: SHIP.intro.done['call:end'] !== undefined, act: ACT && ACT.kind })")
        g.ev("actEnd(true)")
        print(f"  Track it: arrow '{tr}'; in the booths: arrow {mid['g']} on {mid['place']}, done {mid['end']}; the call begun ({end['act']}): arrow {end['g']}, done {end['end']}")
        if not tr or 'booth' not in tr.lower() or end['g'] == tr or not end['end'] or end['act'] != 'call': fail(f'the call-home arrow went wrong: {tr}, {end}')
        if mid['g'] != tr or not (mid['place'] or '').startswith('3-callhome-') or mid['end'] or g.ev(f"!!heldBy('{mid['place']}')"): fail(f"in the booths' room the arrow went before the call began, or isn't on a free booth (FX5): {mid}")
    g.ev("(() => { const b = INTRO_WEEK.find(x => x.id === 'd1-briefing'); SHIP.intro.done['d1-briefing:met'] = introAbs(1, b.at); skipTo(introAbs(1, b.until + 6)); goToDeck(5); player.obj.position.copy(cellPos(15, 3)); clearGoal(); })()"); g.step(20)
    c1 = g.ev(G); g.ev('careerClock()'); g.step(20); c2 = g.ev(G)
    took = g.ev("(() => { const j = SHIP.jobs.find(x => x.reserved === 1) || SHIP.jobs.find(x => !x.by); return !!j && claimJob(j.id); })()"); g.step(20); c3 = g.ev(G)
    print(f"  Day 1 after the briefing: '{c1}'; clocked in: '{c2}'; job taken {took}: {c3}")
    # (FX15, patch 0.92.5 #22) clocked in, the board's arrow names the job: 'Your shadow job: take it at the board'
    if c1 != 'Clock in at the time clock' or c2 not in ('Take a job at the job board', 'Your shadow job: take it at the board') or c3 in ('Clock in at the time clock', 'Take a job at the job board', 'Your shadow job: take it at the board'): fail(f'the Day 1 arrows went wrong: {c1}, {c2}, {c3}')
    if not g.ev("typeof teaOut === 'function'"):
        print('  tea: not yet (no teaOut, the player engineer\'s 0.28.74)'); return
    g.ev("(() => { const j = SHIP.jobs.find(x => x.reserved === 1); if (j) { jobStops(j).forEach((s, k) => jobStepDone(j.id, k)); j.workDone = true; turnInJob(j.id); } SHIP.intro.done['d1-shadow:job'] = SHIP.intro.done['d1-shadow:job'] || Math.floor(shipNow()); })()")
    g.ev("skipTo(introAbs(1, 13 * 60 + 1))"); g.ev("(() => { SHIP.player.needs = { hunger: 80, energy: 80, hygiene: 80, fitness: 80, social: 80 }; clearGoal(); const a = DECK_CREW.find(x => x.p.id === INTRO_ESCORT); if (a) { const n = nearestOpen(a.x + 1, a.z, player); if (n) player.obj.position.copy(cellPos(...n)); } })()")
    for i in range(40):   # he starts once his turn-in talk is over, by 13:10 at the latest
        g.step(30)
        if g.ev("SHIP.intro.done['tea:go'] !== undefined || SHIP.intro.done['tea:end'] !== undefined"): break
    g.step(30)
    Z = "(e => e && e.mode)(escortPlan(ROSTER.find(p => p.id === INTRO_ESCORT), shipNow()))"
    go = g.ev("({ go: SHIP.intro.done['tea:go'] !== undefined, told: SHIP.intro.done['tea:told'] !== undefined, g: " + G + ", mode: " + Z + ", lead: introTeaLead() })")
    g.ev('(() => { goToDeck(5); player.obj.position.copy(cellPos(22, 1)); })()'); g.step(30)
    at = g.ev("({ at: SHIP.intro.done['tea:at'] !== undefined, g: " + G + ", mode: " + Z + " })")
    g.ev("SHIP.player.teaDay = 1"); g.step(60)
    after = g.ev("({ end: SHIP.intro.done['tea:end'], mode: " + Z + " })")
    print(f"  13:01, first job done: {go}; in the Tea corner: {at}; after your tea: {after}")
    if not (go['go'] and go['told'] and go['mode'] == 'lead' and go['g'] == 'Tea and biscuits with Zeke' and go['lead']): fail(f'Zeke did not lead you to tea: {go}')
    if not (at['at'] and at['mode'] == 'wait' and not at['g']): fail(f'tea at the Tea corner went wrong: {at}')
    if after['end'] is None or after['end'] < 0 or after['mode'] == 'lead' or after['mode'] == 'wait': fail(f'the tea walk did not end after your tea: {after}')

RELOAD_MS = 120000   # parts 9 and 11 reload the page right after part 8's long evening: in a cloud container that load took 31-32 s, past Playwright's 30 s default (BM11, 0.64.7)
FIRSTS_ONLY = '--firsts' in sys.argv
LEAVE_ONLY = '--leave' in sys.argv   # part 14 alone (0.64.15's "Zeke stands in the bunk room")
WEEK_ONLY = '--week' in sys.argv
BESIDE_ONLY = '--beside' in sys.argv   # part 16 alone (FE2 on 0.92.0)
P923_ONLY = '--p923' in sys.argv   # part 19 alone (patch 0.92.3)
EVENING_ONLY = '--evening' in sys.argv or '--dawdle' in sys.argv
DAWDLE = '--dawdle' in sys.argv   # 0.42.31 (the user on 0.60.6): part 8 lingers ~40 s by the Deck 5 lift and again after the bunk; Torres must still ride with you   # part 8 alone: the evening walked in the real game (the tour's quick check)
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1])
    if not g.ev("typeof INTRO_STEPS !== 'undefined'"):
        print('No section 21 in this build.'); sys.exit(1)
    if LEAVE_ONLY:
        talk_away(g)
        bunk_leave(g)
        if g.errors: fail('page errors: ' + ' | '.join(g.errors[:6]))
        g.close(); print('OK' if ok else 'FAILED'); sys.exit(0 if ok else 1)
    if '--solotap' in sys.argv:   # part 18 alone (item 81)
        solo_tap(g)
        if g.errors: fail('page errors: ' + ' | '.join(g.errors[:6]))
        g.close(); print('OK' if ok else 'FAILED'); sys.exit(0 if ok else 1)
    if BESIDE_ONLY:
        beside_walk(g); late_dinner(g)
        if g.errors: fail('page errors: ' + ' | '.join(g.errors[:6]))
        g.close(); print('OK' if ok else 'FAILED'); sys.exit(0 if ok else 1)
    if '--dinner' in sys.argv:   # part 20 alone (CH1)
        dinner_reload(g)
        if g.errors: fail('page errors: ' + ' | '.join(g.errors[:6]))
        g.close(); print('OK' if ok else 'FAILED'); sys.exit(0 if ok else 1)
    if P923_ONLY:
        patch923(g)
        if g.errors: fail('page errors: ' + ' | '.join(g.errors[:6]))
        g.close(); print('OK' if ok else 'FAILED'); sys.exit(0 if ok else 1)
    if FIRSTS_ONLY:
        firsts(g); clock_tracked(g)
        if g.errors: fail('page errors: ' + ' | '.join(g.errors[:6]))
        g.close(); print('OK' if ok else 'FAILED'); sys.exit(0 if ok else 1)
    if WEEK_ONLY:
        week(g)
        if g.errors: fail('page errors: ' + ' | '.join(g.errors[:6]))
        g.close(); print('OK' if ok else 'FAILED'); sys.exit(0 if ok else 1)

    steps = g.ev("INTRO_STEPS.map(s => s.id)")   # (part 8 needs it with --evening too)
    START_MIN = g.ev('INTRO_START.min'); START_HM = f'{START_MIN // 60:02d}:{START_MIN % 60:02d}'   # 16:30 since playtest patch 1 (was 17:30)
    if not EVENING_ONLY:   # --evening: part 8 alone (the tour's quick check)
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
        EVENING = -1440 + g.ev("introStepById('night').at") + 31          # Day 0 20:01 with the night step at 19:30 (DS1: it moves with the arrival)
        WANT = {'torres-zeke': 10, 'tomas': 10, 'pell': 5, 'calder': 3, 'brennan': 3}

        print('2. The happy path, on paper (Day 0 from INTRO_START to Day 8 00:00)')
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
        print('  mail:', '; '.join(f"{mins(int(m[0]))} {m[1]}: {m[2]}" for m in a['mail']))
        if any(m[2] in ('Your bunk', 'Tomorrow') for m in a['mail']): fail('a fallback Mail went out with the player there')

        print('3. The wanderer and the idler')
        for who in ('wander', 'idle'):
            e = run(who=who, to=EVENING)
            late = [s for s in steps if s not in e['I']['done']]
            miss = e['I']['missed']
            print(f"  {who}: by Day 0 {EVENING + 1440} min step {e['I']['step']}, missed {len(miss)} ({', '.join(miss)}); mail: {', '.join(m[2] for m in e['mail'])}")
            if e['I']['step'] is not None or late: fail(f"{who}: the evening hasn't ended by {EVENING + 1440} min (left: {', '.join(late)})")
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

        tl = g.ev("typeof introTourLines === 'function' ? INTRO_TOUR.map(x => [x.id, introTourLines(x.id, x.stub).length, introWriterLine('walk.' + x.id + '.1') ? 'writers' : 'stand-ins']) : null")
        if tl: print('  Torres\'s tour (lines per place):', ', '.join(f'{i} {n} ({w})' for i, n, w in tl))
        if tl and g.ev("typeof LINES !== 'undefined' && !!LINES.crew && !!LINES.crew['torres-zeke']") and any(w != 'writers' and c for (i, n, w), c in zip(tl, g.ev('INTRO_TOUR.map(x => x.core)'))): fail('the writers\' tour lines are in this build but a talking place has none: ' + str([i for (i, n, w), c in zip(tl, g.ev('INTRO_TOUR.map(x => x.core)')) if w != 'writers' and c]))   # 0.42.27: the quiet places (core 0) have none
    print('8. The evening in the real game (New game arriving, a player who follows Torres and taps through meetings)')
    if not g.ev("typeof newGameStart === 'function' && typeof escortPlanOf === 'function'"):
        fail('no newGameStart or escort walker (sections 13 and 10, the sim engineer): the arrival cannot start')
    else:
        g.ev("(() => { window.__said = []; const old = bubbleSay; bubbleSay = function (h, text, s) { window.__said.push([clockText(), SHIP.intro.step, text]); return old.apply(this, arguments); }; return true; })()")   # reviewer 1c's probe: what's actually said
        g.ev('CLOTHES_ON = true'); g.ev('newGameStart(true)'); g.step(5)   # playtest patch 1: clothes on, as in a real game (the wardrobe, his wardrobe lines before the device)
        tern = g.ev("typeof ternRamp === 'function' && !!DECKS[5].tern")
        if tern:   # the walk-in Tern (deck architect 0.38.18): you start in its aisle with the ramp shut
            t0 = g.ev("({ me: player.here(), start: SHIP_START_ARRIVAL.tile, open: ternRampOpen() })")
            print(f"  the Tern: you start at {t0['me']} (start {t0['start']}, INTRO_START {g.ev('INTRO_START.tile')}), ramp {t0['open']}")
            if t0['me'] != g.ev('INTRO_START.tile'): fail(f"a new arriving game starts you at {t0['me']}, not INTRO_START's tile (section 13's SHIP_START_ARRIVAL is {t0['start']})")
            if t0['open'] != 0: fail('the Tern\'s ramp is open while you sign the manifest')
        g.page.fill('form input[maxlength="24"]', 'Sam'); g.page.click('form button'); g.step(5)
        if tern:   # about 2 s after signing, the pilot's line and the ramp opens (2.5 s)
            g.ev("window.__shown = []; { const el = document.getElementById('toast'); if (el) new MutationObserver(() => window.__shown.push(el.textContent)).observe(el, { subtree: true, childList: true, characterData: true }); }")   # every pop-up shown (with the teaching arrows on, 0.92.0, a later one waits its turn and then follows it)
            r0 = g.ev('ternRampOpen()'); g.step(150)   # 2 s to the pilot, 2.5 s of ramp (the frame clock)
            for _ in range(10):                         # a pop-up ahead of it in the queue: the pilot's line follows in its turn
                if g.ev("window.__shown.some(t => t.includes('Raman'))"): break
                g.step(30)
            r1 = g.ev("({ open: ternRampOpen(), toast: window.__shown.find(t => t.includes('Raman')) || (document.getElementById('toast') || {}).textContent || '', pilot: !!introWriterLine('pilot.ramp', 'raman') })")
            src = "the writers' line" if r1['pilot'] else 'the stand-in'
            print(f"  the ramp right after signing {r0}, 5 s later {r1['open']}; the pilot ({src}): {r1['toast'][:90]}")
            if r0 != 0: fail('the ramp opened before the pilot spoke')
            if r1['open'] != 1: fail('the ramp did not open after the pilot\'s line')
            if 'Raman' not in r1['toast']: fail('no pilot\'s line when the ramp opened')
        shut, reopened = None, None
        tap = g.ev("typeof introTap === 'function' && typeof MEETING_SCRIPTS !== 'undefined' && !!MEETING_SCRIPTS.introAsk && typeof tapCrew === 'function' && /introTap/.test(tapCrew.toString())")
        if tap:   # "Ask Zeke" parked (the patch's #31): tapping Torres while he shows you round plays his next tour line or does nothing; never the introAsk panel, never the chat card
            t1 = g.ev("(() => { const ok = introTap(ROSTER.find(p => p.id === INTRO_ESCORT)); return { ok, dlg: DIALOGUE && DIALOGUE.id, parked: typeof INTRO_ASK_ON !== 'undefined' && !INTRO_ASK_ON, other: introTap(ROSTER.find(p => p.id === 'calder')) }; })()")
            print(f"  tapping Torres on the ramp: taken {t1['ok']}, panel {t1['dlg']} (tapping someone else: {t1['other']})")
            if t1['parked']:
                if not t1['ok'] or t1['dlg']: fail('tapping Torres during the evening should do nothing (no panel, no chat card): "Ask Zeke" is parked')
            elif not t1['ok'] or t1['dlg'] != 'introAsk': fail('tapping Torres during the evening did not open introAsk')
            if t1['other']: fail('introTap answered for someone who is not the escort')
        else: print('  not yet: tap-to-ask (needs introTap, the writers\' introAsk and sim 0.26.31\'s hook in tapCrew)')
        tl2 = g.ev("(() => { const L = (typeof VOICE !== 'undefined' && VOICE['torres-zeke'] && VOICE['torres-zeke'].lines && VOICE['torres-zeke'].lines.week1) || []; return INTRO_TOUR.map(x => [x.id, introTourLines(x.id, x.stub).length, L.filter(e => (e.flag || '').startsWith('walk.' + x.id + '.')).length]); })()")
        wrong = [i for i, n, w in tl2 if w and n != w]
        print('  tour lines with the week under way (place, played, written):', tl2)
        if wrong: fail('a tour place plays other lines than its own: ' + ', '.join(wrong))
        order, peak, led = [], {}, 0
        rides, rideFrom, liftArrow = [], None, []   # (the lead, the user on 0.60.5a): after each lift ride Torres steps out with you, not at the room he's heading for
        lingered = []
        pre = { 'n': 0, 'pause': 0, 'still': 0, 'run': 0, 'last': None, 'sm': [] }   # 0.42.29 (the user on 0.60.5): from the ramp's welcome to the lift, walk-and-talk, no pauses
        dinner, bunkAt, seats, chat, chiefAt = None, None, None, None, None
        linger = {}
        INTRO_ESC_ID = g.ev('INTRO_ESCORT')
        BED_GOAL = g.ev("typeof INTRO_BED_GOAL !== 'undefined' ? INTRO_BED_GOAL : 'Your bunk'")
        for k in range(600):   # (playtest patch 1: the evening's last step is 19:30)
            g.step(20)
            r = g.page.evaluate('([s, m]) => window.__sc(s)(m)', [WALK_TICK, 'follow'])
            peak[r['deck']] = max(peak.get(r['deck'], 0), r['calls'])
            if r['esc'] and r['esc'][2] == 'escort': led += 1
            if r['step'] == 'wing' and r['deck'] == 5 and r.get('shown'): liftArrow.append(r['shown'])   # FX3: at the Deck 5 lift with Deck 4 to go, the arrow at the lift panel
            spot = ('lift' if r['step'] in ('lift', 'wing') and r['deck'] == 5 and r['me'][0] >= 14 else 'bunk' if r['step'] == 'toMess' and r['deck'] == 4 and not r['dlg'] else None)
            if DAWDLE and spot and spot not in lingered:   # stand still for ~40 real s (more than the steps' old 20 ship minutes)
                lingered.append(spot)
                for _ in range(70): g.step(20); g.page.evaluate('([s, m]) => window.__sc(s)(m)', [WALK_TICK, 'stand'])
                print(f"  lingered by {spot} till {g.ev('clockText()')}: step {g.ev('SHIP.intro.step')}, missed {g.ev('SHIP.intro.missed')}")
                continue
            if r['act'] == 'riding' or (r['act'] or '').startswith('lift'): rideFrom = rideFrom or r['deck']
            elif rideFrom is not None and r['deck'] != rideFrom:
                d = max(abs(r['me'][0] - r['esc'][0][0]), abs(r['me'][1] - r['esc'][0][1])) if r['esc'] else None
                rides.append([rideFrom, r['deck'], r['t'], r['me'], r['esc'][0] if r['esc'] else None, d]); rideFrom = None
            if r.get('pre') and r['deck'] == 5 and not r['dlg']:
                pre['n'] += 1; pre['pause'] += r['pause']; pre['sm'].append(r['sm']); mv = r['ex'] != pre['last']; pre['last'] = r['ex']
                pre['run'] = 0 if mv else pre['run'] + 1; pre['still'] = max(pre['still'], pre['run'])
            if tern and shut is None and g.ev('INTRO_UI.ternShut'): shut = (r['t'], r['step'], r['me']); print(f"  {r['t']}  the ramp closes behind you (you at {r['me']}, ramp {g.ev('ternRampOpen().toFixed(2)')})")
            if tern and shut and reopened is None and not g.ev('INTRO_UI.ternShut'): reopened = (r['t'], r['step'])
            if not order or order[-1] != r['step']: order.append(r['step']); print(f"  {r['t']}  {r['step']}  (you: Deck {r['deck']} {r['me']}; Torres {r['esc'][0] if r['esc'] else 'not here'}{'; his seat ' + r['seat'] if r['seat'] else ''})")
            if r['step'] == 'table' and dinner is None:   # the lead's condition for the longer tour: dinner still hot, seats and crew there
                dinner = g.ev("(() => { const G = SHIP.galley || {}, sv = G.servery || {}, mess = DECK_CREW.filter(a => deckDef.num === 3 && /Mess hall/.test((ROOMS[roomAt(...cellAt(a.x, a.z))] || {}).name || '')).length; return { t: clockText(), portions: sv.portions, dish: sv.dish, meal: sv.meal, mess, you: introSeat('you'), him: introSeat(INTRO_ESCORT) }; })()")
                print(f"  at the table {dinner['t']}: servery {dinner['portions']} portions of {dinner['dish']} ({dinner['meal']}), {dinner['mess']} crew in the mess, seats you {dinner['you']}, Torres {dinner['him']}")
                hm = dinner['t'].split()[-1]; tmin = int(hm[:2]) * 60 + int(hm[3:])
                if tmin > START_MIN + 90 and not DAWDLE: fail(f'the walk is too long: you reach the table at {hm}, more than 90 minutes after the arrival (reviewer 1c; the scenes wait till the Chief\'s step ends)')   # 0.42.27; playtest patch 1: from INTRO_START
            if chat is None and g.ev("!!DIALOGUE && /^introDinner/.test(DIALOGUE.id || '')"):   # the dinner chat at your table (0.42.63, the user: the game sits you down for it)
                for _ in range(4): g.step(20)   # stop steering: let the game sit you (CH1: no taps, so every card of the chat is read below)
                chat = { 't': g.ev('clockText()'), 'seat': g.ev("introSeat('you')"), 'sat': g.ev("typeof ACT !== 'undefined' && ACT ? ACT.placeId || null : null"), 'calder': g.ev(CALDER_D), 'away': g.ev(CALDER_AWAY) }
                print(f"  the dinner chat at {chat['t']}: sat down by the game in {chat['sat']} (your seat {chat['seat']}); the Chief {chat['calder']} m from her seat at your table, {chat['away']} m from hers at the next table")
                if chat['seat'] and chat['sat'] != chat['seat'] and not DAWDLE: fail(f"you weren't sat down at your table for the dinner chat: {chat}")
                if chat['away'] is None or chat['away'] >= 2: fail(f"the Chief wasn't at the next table when the dinner chat began (the patch #3: she eats there, in view, and walks over on \"Look who's coming over\"): {chat}")
                # (CH1, the user on 0.99.1: she got up mid-chat, ten ship minutes after you sat) read the chat at a player's pace, 5 s a card
                # (3 ship minutes): she stays sat at the next table through his lines and the question, gets up on the card before his last
                # ("Look who's coming over", the reply to your answer), and is on her way or sat across from you by that last card
                cards = []
                for _ in range(20):
                    if not g.ev("!!DIALOGUE && /^introDinner/.test(DIALOGUE.id || '')"): break
                    g.step(150)
                    c = g.ev("(() => { const D = DIALOGUE; if (!D || !/^introDinner/.test(D.id || '')) return null; const l = D.queue[D.i]; return { i: D.i, n: D.queue.length, choice: !!(l && l.choice), up: !!INTRO_UI.calder, t: clockText().slice(-5) }; })()")
                    if not c: break
                    c['away'] = g.ev(CALDER_AWAY); cards.append(c)
                    g.ev('(() => { const l = DIALOGUE.queue[DIALOGUE.i]; if (l && l.choice) dialogueChoose(1); else dialogueNext(); })()')
                print('  the dinner chat card by card (card/of, the Chief up, m from her seat at the next table):', ' '.join(f"{c['t']} {c['i'] + 1}/{c['n']}{'?' if c['choice'] else ''} {'up' if c['up'] else 'sat'} {c['away']}" for c in cards))
                early = [c for c in cards if c['up'] and (c['i'] < c['n'] - 2 or c['choice'])]
                last = cards[-1] if cards else None
                if early: fail(f"the Chief got up before the card ahead of \"Look who's coming over\" (CH1, the user on 0.99.1): {early[0]}")
                if not last or last['i'] != last['n'] - 1 or not last['up']: fail(f"the Chief had not got up by \"Look who's coming over\": {last}")
                elif len(cards) >= 2 and not cards[-2]['up']: fail(f"the Chief got up on \"Look who's coming over\" itself, not the card before it: {cards[-2:]}")
                if any(not c['up'] and (c['away'] is None or c['away'] >= 1) for c in cards): fail(f"the Chief left her seat at the next table before getting up: {cards}")
            if chiefAt is None and g.ev("!!DIALOGUE && /^introChief/.test(DIALOGUE.id || '')"):   # her welcome: she's walked over and sat first, after you and the chat
                chiefAt = { 't': g.ev('clockText()'), 'calder': g.ev(CALDER_D), 'in': g.ev('introCalderIn()'), 'chat': chat is not None, 'you': g.ev("typeof ACT !== 'undefined' && ACT ? ACT.placeId || null : null") }
                print(f"  the Chief's welcome at {chiefAt['t']}: she's {chiefAt['calder']} m from her seat (at it: {chiefAt['in']}), after the chat {chiefAt['chat']}, you in {chiefAt['you']}")
                if not chiefAt['in']: fail(f"the Chief's welcome began before she'd walked over to your table: {chiefAt}")   # (playtest patch 1, #5: --dawdle too, the user's late arrival)
                if not chiefAt['chat'] and not DAWDLE: fail(f"the Chief's welcome came before the dinner chat with Torres: {chiefAt}")
            if r['step'] == 'free' and seats is None:   # reviewer 1: who sits in the three dinner seats once the Chief has come over
                for _ in range(4): g.step(20); g.page.evaluate('([s, m]) => window.__sc(s)(m)', [WALK_TICK, 'stand'])   # stop steering: let the game sit you
                seats = g.ev("(() => { const S = introStepById('chief').seats || {}, h = id => { const a = id && heldBy(id); return a ? a.p.id : null; }; return { you: [S.you, h(S.you), typeof ACT !== 'undefined' && ACT ? ACT.placeId || null : null], torres: [S[INTRO_ESCORT], h(S[INTRO_ESCORT])], calder: [S.calder, h(S.calder)], t: clockText() }; })()")
                print(f"  the dinner seats at {seats['t']}: yours {seats['you']}, Torres {seats['torres']}, Calder {seats['calder']}")
            if r['goal'] in ('Your bunk', BED_GOAL) and bunkAt is None: bunkAt = r['t']; print(f"  {r['t']}  the arrow points to your bunk")
            for who, key in (('torres-zeke', 'free'), ('calder', 'chief:end')):   # playtest patch 1, #6: they stay sat a little after their last word, then go
                if who in linger: continue
                lg = g.page.evaluate('([s, m]) => window.__sc(s)(m)', [LINGER, [who, key]])
                if lg: linger[who] = lg; print(f"  {lg['t']}: {who} {lg['after']} ship minutes after {key}: {lg['d']} m from the seat at your table")
            if r['step'] is None and (bunkAt or g.ev('shipNow() >= introAbs(0, 20 * 60)')): break   # (playtest patch 1: the evening's last step can end before the bunk arrow, which waits for his goodnight and the servery arrow)
        simnow = g.ev("typeof tapCrew === 'function' && /introTap/.test(tapCrew.toString())")   # the sim's dinner seating and evening cooking (0.26.26-0.26.31)
        if not simnow: print('  not yet: the dinner and seat checks (they need the sim engineer\'s current build, 0.26.31+)')
        elif dinner is None or not dinner['portions'] or dinner['portions'] < 2 or dinner['mess'] < 3 or not dinner['you'] or not dinner['him']: fail(f'no proper dinner when you reach the table: {dinner}')
        if not bunkAt: fail('the first-night arrow never pointed to your bunk before 20:00')
        gn = g.ev("[SHIP.intro.done.goodnight, (window.__said || []).slice(-3).map(x => x[0] + ' ' + x[2])]") if g.ev("typeof INTRO_GOODNIGHT !== 'undefined'") else None
        ch = g.ev("[SHIP.intro.done['chief:met'], SHIP.intro.done['chief:end'], SHIP.intro.done.goodnight, SHIP.intro.missed.includes('chief')]")
        print(f'  the Chief\'s welcome (introChief): shown {ch[0]}, ended {ch[1]} (None: cut short), goodnight {ch[2]}')
        if ch[3] or ch[0] is None: fail('the Chief\'s welcome never played (the user on 0.60.4: "the Chief didn\'t give their speech")')
        elif ch[1] is None: fail(f'the Chief\'s welcome was cut short or never ended: {ch}')
        elif ch[2] is not None and ch[2] < ch[1]: fail(f'his goodnight came before the Chief had finished: {ch}')
        if gn is not None:   # 0.42.27 (the user): Torres's goodnight after dinner, and only then the bunk arrow
            print(f'  his goodnight at {gn[0]} (ship minute; None: not with you), last lines said: {gn[1]}')
            if g.ev('SHIP.intro.done.goodnight === undefined'): fail('Torres never said goodnight (or the fallback never ran)')
            elif bunkAt and gn[0] is not None and int(bunkAt.split()[-1][:2]) * 60 + int(bunkAt.split()[-1][3:]) - 1440 < gn[0]: fail(f'the bunk arrow came before his goodnight ({bunkAt})')
        if simnow and (not seats or seats['you'][1] or seats['you'][2] != seats['you'][0] or seats['torres'][1] != INTRO_ESC_ID or (seats['calder'][1] not in ('calder', None) or seats['calder'][1] is None and not chiefAt)): fail(f'the dinner seats are wrong (place, held by): {seats}')   # (0.42.64: the Chief may still be on her way over then; the welcome check below has her sat)
        w = g.ev("({ missed: SHIP.intro.missed, done: Object.keys(SHIP.intro.done), device: introFlag('intro.device'), calder: introFlag('met.calder') })")
        print(f'  draw-call peaks by deck {peak}; Torres led you for {led} looks')
        if w['missed']: fail('the real walk missed ' + ', '.join(w['missed']))
        if [s for s in steps if s not in w['done']]: fail('the real walk never reached ' + ', '.join(s for s in steps if s not in w['done']))
        if order[-1] is not None: fail('the evening did not end in the real walk')
        if not (w['device'] and w['calder']): fail('no device or no Calder after the real walk')
        # playtest patch 1 (#2-#4, #6): the bag into the wardrobe by you, the device from Zeke in person, no cabin Mail, the linger
        hand = g.ev("({ cabin: SHIP.clothes.said['d0-wardrobe'], stow: window.__stow || null, given: SHIP.intro.done['device:given'], stowAt: SHIP.intro.done.stow, devMet: SHIP.intro.done.device, bag: typeof bagHeld === 'function' && bagHeld(), mail: SHIP.mail.filter(m => m.from === 'Zeke Torres').map(m => m.subject) })")
        print(f"  the bag and the device: stowed by you {hand['stow']}, device handed over at {hand['given']} (stow step {hand['stowAt']}, device step {hand['devMet']}); Zeke's Mail {hand['mail']}")
        hv = g.ev("({ s: SHIP.intro.done['hand:start'], e: SHIP.intro.done['hand:end'], mail: window.__handMail || null, lines: introHandLines(false), after: introHandLines(true), toast: (document.getElementById('tx') || {}).textContent })")
        if hv['s'] is None: fail('the device hand-over in his bubbles never played (lead 31: part 8 must play it)')
        heard = [x for x in g.ev('window.__said') if x[2] in hv['lines'] + hv['after']]
        order = [x[2] for x in heard]
        print(f"  the hand-over's lines heard {len(order)}/{len(hv['lines']) + len(hv['after'])}, at {sorted(set(x[0] for x in heard))}")
        if order != hv['lines'] + hv['after']: fail(f"the hand-over's lines out of order or missing: {order}")
        if len(set(x[0] for x in heard)) > 1: fail(f"the ship clock moved during the hand-over: {sorted(set(x[0] for x in heard))}")
        if hv['s'] is not None:   # DS1 (lead 30's (e)): his hand-over in bubbles, his Mail opened on your device, the clock held through it
            print(f"  the hand-over: from ship minute {hv['s']} to {hv['e']}; the device opened on {hv['mail']}")
            if hv['e'] is None or hv['e'] - hv['s'] > 1: fail(f"the ship clock should hold through Zeke's hand-over: {hv}")
            if not hv['mail'] or hv['mail'].get('app') != 'mail' or not hv['mail'].get('subject'): fail(f"the device should open on his Mail at the hand-over: {hv}")
        if 'stow' in steps:
            if not hand['stow'] or hand['stow']['goal'] != 'Put your bag in your wardrobe' or hand['bag']: fail(f"the bag did not go into the wardrobe by your tap, with its arrow: {hand}")
            if hand['given'] is None or hand['stowAt'] is None or hand['given'] < hand['stowAt']: fail(f"the device was not handed over in person after the bag: {hand}")
            if hand['cabin'] is None or hand['given'] < hand['cabin']: fail(f"his wardrobe lines did not come between the bag and the device: {hand}")
            if any(x in ('Everything I didn\'t say', 'Settling in') for x in hand['mail']): fail('Zeke\'s cabin Mail is back (parked, playtest patch 1 #4)')
        if True:   # (playtest patch 1, #6: on any build, so an old one fails it)
            for who in ('torres-zeke', 'calder'):
                if who not in linger: fail(f'{who}: never sampled after their last word (the linger check)')
                elif linger[who]['d'] is None or linger[who]['d'] > 1.2: fail(f'{who} left the table straight after speaking: {linger[who]}')
        if max(peak.values()) >= 450: fail(f'draw calls {max(peak.values())} at the arrival (budget 450)')
        if led < 20: fail('Torres hardly led you')
        # the tour as heard by a follower (pacing A): every place's core lines, in place order; extras only if you linger
        said = [x[2] for x in g.ev('window.__said')]
        sp = g.ev("INTRO_TOUR.map(t => [t.id, introTourSplit(t)])")
        walkp = set(g.ev("INTRO_TOUR.filter(t => t.walk && !t.must && t.deck === 5).map(t => t.id)"))   # (DS1: Deck 4's officers' corridor walks too, after the lift; its core lines must still be heard) before the lift: heard as you walk, the rest skipped at the lift (a must place is always heard)
        ps = (pre['sm'][-1] - pre['sm'][0]) / g.ev('SHIP_RATE') / max(1, pre['n'] - 1) if pre['n'] > 1 else 0   # real seconds a look
        print('  after each ride (from, to, time, you, Torres, tiles apart):', rides)
        for x in rides[:2]:
            if x[5] is None or x[5] > 3: fail(f'after the lift ride Deck {x[0]} -> {x[1]} Torres is not beside you: {x}')
        if len(rides) < 2: fail(f'expected two lift rides on the evening (Deck 5 -> 4 -> 3): {rides}')
        print('  the arrow at the Deck 5 lift, Deck 4 to go:', sorted(set(liftArrow))[:3])
        if not any(x.startswith('Tap the lift: Deck 4') for x in liftArrow): fail(f'at the Deck 5 lift with Torres, the arrow should point at the lift panel for Deck 4 (the user\'s: "an arrow pointing to the control panel"): {sorted(set(liftArrow))[:3]}')
        print(f"  the walk to the lift: {pre['n'] * ps:.0f} s with him on Deck 5 ({pre['n']} looks), paused {pre['pause'] * ps:.1f} s, longest standing still {pre['still'] * ps:.1f} s")
        if pre['pause']: fail('Torres paused for his lines before the lift (the user on 0.60.5: walk-and-talk until the lift)')
        wl = [i for i, x in enumerate(said) if any(x in L['core'] + L['extra'] for p, L in sp if p in walkp)]
        later = [p for p, L in sp][[p for p, L in sp].index('lift'):] if any(p == 'lift' for p, L in sp) else []
        ll = [i for i, x in enumerate(said) if any(x in L['core'] + L['extra'] for p, L in sp if p in later)]
        print('  said up to the lift:', [x[0].split()[-1] + ' ' + x[2][:28] for x in g.ev('window.__said')[:(min(ll) if ll else 0) + 1]])
        if wl and ll and max(wl) > min(ll): fail('a line from the walk to the lift was said after the lift\'s')
        pos = {}
        for i, x in enumerate(said): pos.setdefault(x, i)
        heard_core = sum(1 for i, L in sp for l in L['core'] if l in pos and i not in walkp); all_core = sum(len(L['core']) for i, L in sp if i not in walkp)
        heard_all = sum(1 for i, L in sp for l in L['core'] + L['extra'] if l in pos); all_lines = sum(len(L['core']) + len(L['extra']) for i, L in sp)
        print(f'  the tour, following: core lines heard {heard_core}/{all_core}, all lines {heard_all}/{all_lines}; per place ' + ', '.join(f"{i} {sum(1 for l in L['core'] if l in pos)}/{len(L['core'])}+{sum(1 for l in L['extra'] if l in pos)}" for i, L in sp))
        if heard_core < all_core: fail('following Torres, some core tour lines are never heard: ' + ', '.join(i for i, L in sp if i not in walkp and any(l not in pos for l in L['core'])))
        seq = [pos[l] for i, L in sp for l in L['core'] if l in pos]
        if seq != sorted(seq): fail('the tour\'s core lines are heard out of place order')
        # the last place's core lines may finish at the table (the dinner chat waits for them); extras there, or anything at the Chief's, may not
        late = [x for x in g.ev('window.__said') if (x[1] == 'chief' and any(x[2] in L['core'] + L['extra'] for i, L in sp)) or (x[1] == 'table' and any(x[2] in L['extra'] for i, L in sp))]
        if late: fail(f'tour lines play over dinner: {late[:3]}')
        if tern:
            print(f'  the ramp: closed behind you at {shut}, open again at {reopened} (target {g.ev("TERN.target")})')
            if not shut: fail('the Tern\'s ramp never closed behind you')
            elif shut[1] not in ('ramp', 'hello', 'haulway', 'works'): fail(f'the ramp closed late, at step {shut[1]}')
            if not reopened or g.ev('TERN.target') != 1: fail('the Tern\'s ramp was left shut after Torres let you go')
    if EVENING_ONLY:
        if g.errors: fail('page errors: ' + ' | '.join(g.errors[:6]))
        g.close(); print('OK' if ok else 'FAILED'); sys.exit(0 if ok else 1)
    print('9. A first launch arrives (no save, never arrived, not a test URL), and its Day 0 save loads at the same step')
    if not g.ev("typeof newGameStart === 'function'"):
        fail('no newGameStart (section 13): a first launch cannot arrive')
    else:
        url = g.page.url.split('?')[0]
        g.page.evaluate('localStorage.clear()')
        g.page.goto(url + '?debug', timeout=RELOAD_MS); g.page.wait_for_function('window.__sc !== undefined || window.__err', timeout=60000)
        g.step(5)
        f = g.ev("({ t: clockText(), deck: deckDef.num, on: introOn(), step: SHIP.intro.step, form: !!document.querySelector('form input[maxlength=\"24\"]') })")
        print(f"  {f['t']}, Deck {f['deck']}, intro {'on' if f['on'] else 'off'} at {f['step']}, manifest {'up' if f['form'] else 'not up'}")
        if not (f['t'].startswith('Day 0, Sunday ' + START_HM) and f['deck'] == 5 and f['on'] and f['form']): fail('a first launch did not arrive by shuttle')
        g.page.fill('form input[maxlength="24"]', 'Sam'); g.page.click('form button'); g.step(30)
        g.ev('saveGame()'); before = g.ev('({ step: SHIP.intro.step, day: SHIP.time.day })')
        g.page.goto(url + '?debug', timeout=RELOAD_MS); g.page.wait_for_function('window.__sc !== undefined || window.__err', timeout=60000); g.step(5)
        after = g.ev("({ step: SHIP.intro.step, day: SHIP.time.day, form: !!document.querySelector('form input[maxlength=\"24\"]'), name: SHIP.player.name })")
        print(f"  saved at {before}, loaded at step {after['step']} on Day {after['day']}, manifest {'up' if after['form'] else 'gone'}, name {after['name']}")
        if after['step'] != before['step'] or after['day'] != 0 or after['form']: fail('a Day 0 save did not load at its step')
        if after['name'] != 'Sam': print('  (the name comes back once section 15 saves SHIP.player.name: player engineer 3)')
        print('11. Reload mid-walk: follow Torres to the lift (or the wing), save and reload short of it, then on to your bunk')
        mid = None
        for k in range(120):
            g.step(20); r = g.page.evaluate('([s, m]) => window.__sc(s)(m)', [WALK_TICK, 'follow'])
            # save on the lift or wing step while you're still short of its checkpoint (within reach, the step is done
            # on the next minute either way, so a reload there would rightly move on)
            far = r['step'] in ('lift', 'wing') and g.ev(f"(() => {{ const c = introStepById('{r['step']}').checkpoint, h = player.here(); return c.deck !== deckDef.num || Math.max(Math.abs(h[0] - c.tile[0]), Math.abs(h[1] - c.tile[1])) > INTRO_REACH; }})()")
            if far: mid = r; break
        g.ev('saveGame()')
        g.page.goto(url + '?debug', timeout=RELOAD_MS); g.page.wait_for_function('window.__sc !== undefined || window.__err', timeout=60000); g.step(10)
        back = g.ev("(() => { const a = DECK_CREW.find(x => x.p.id === INTRO_ESCORT), pp = player.obj.position; return { step: SHIP.intro.step, deck: deckDef.num, esc: a ? Math.round(Math.hypot(a.x - pp.x, a.z - pp.z)) : null, plan: (escortPlan(ROSTER.find(p => p.id === INTRO_ESCORT), shipNow()) || {}).mode }; })()")
        print(f"  saved at step {mid and mid['step']} ({mid and mid['t']}); after the reload: step {back['step']}, Deck {back['deck']}, Torres {back['esc']} tiles away ({back['plan']})")
        if not mid or back['step'] != mid['step'] or back['esc'] is None: fail(f'reloading mid-walk lost the step or Torres: {back}')
        for k in range(400):
            g.step(20); r = g.page.evaluate('([s, m]) => window.__sc(s)(m)', [WALK_TICK, 'follow'])
            if r['step'] == 'toMess' and g.ev("SHIP.intro.done['hand:end'] !== undefined || !introHandDue()"): break   # (DS1: after his hand-over)
        bunk = g.ev("({ done: SHIP.intro.done.bunk !== undefined, missed: SHIP.intro.missed.slice(), device: introFlag('intro.device') })")
        print(f"  on to the bunk after the reload: reached {bunk['done']}, missed {bunk['missed']}, device {bunk['device']}")
        if not bunk['done'] or bunk['missed'] or not bunk['device']: fail(f'after reloading mid-walk the evening went wrong: {bunk}')
        g.page.evaluate('localStorage.clear()')
    print('10. Monday in the real game: the three jobs held at 05:00, the briefing at 08:50, the shadow shift with Torres')
    if not g.ev("typeof jobReserve === 'function' && typeof newGameStart === 'function'"):
        print('  not yet: this build has no jobReserve (section 17, systems 0.33.36+)')
    else:
        stale = g.ev("({ calder: INTRO_UI.calder, tour: INTRO_UI.tour.length })")   # after part 8's evening
        for i in range(120):   # (DS1) a lift ride left from part 11's follower (on its way to the mess) lands first
            if not g.ev("typeof ride !== 'undefined' && !!ride"): break
            g.step(10)
        g.ev('localStorage.clear()'); g.ev('if (typeof DEV !== "undefined" && DEV.open) deviceClose(); newGameStart(true)'); g.step(5)
        fresh = g.ev("({ calder: !!INTRO_UI.calder, tour: INTRO_UI.tour.length, step: INTRO_UI.step === undefined, meet: INTRO_UI.meet.length })")
        print(f'  New game again: the evening\'s state before {stale}, after {fresh}')
        if fresh['calder'] or fresh['tour'] or not fresh['step'] or fresh['meet']: fail(f'New game kept the last evening\'s state: {fresh}')
        g.ev("(() => { const f = document.querySelector('form input[maxlength=\"24\"]'); f.value = 'Sam'; f.form.requestSubmit(); })()"); g.step(5)   # (the click timed out once under load; nothing covered the button)
        g.ev('skipTo(introAbs(1, 8 * 60 + 40))'); g.ev('(() => { goToDeck(5); player.obj.position.copy(cellPos(15, 3)); })()'); g.step(5)   # the next frames run 05:00's beat, which holds the jobs
        res = g.ev("[1, 2, 3].map(k => SHIP.jobs.find(x => x.reserved === k)).map(j => j && j.machine)")
        print('  held for you:', res)
        if not all(res): fail('the week\'s three jobs are not all held')
        met = None
        for i in range(40):
            g.step(30); met = g.ev('DIALOGUE && DIALOGUE.id')
            if met: break
        print('  08:50 in the Works bay:', met)
        who = g.ev("DIALOGUE ? { lines: DIALOGUE.queue.filter(l => l.who).map(l => l.who), cal: (() => { const a = DECK_CREW.find(x => x.p.id === 'calder'); return a ? (ROOMS[roomAt(...cellAt(a.x, a.z))] || {}).name : null; })() } : null")
        print('  its speakers:', who)
        if not met or not met.startswith('introBriefing'): fail('the Monday briefing did not play: ' + str(g.ev("({ t: clockText(), dlg: DIALOGUE && DIALOGUE.id, dev: typeof DEV !== 'undefined' && DEV.open, step: SHIP.intro.step, missed: SHIP.intro.missed, bag: bagHeld(), brief: SHIP.intro.done['d1-briefing'], met: SHIP.intro.done['d1-briefing:met'], hand: [SHIP.intro.done['hand:start'], SHIP.intro.done['hand:end']], deck: deckDef.num, room: (ROOMS[roomAt(...player.here())] || {}).name, cal: (a => a && (ROOMS[roomAt(...cellAt(a.x, a.z))] || {}).name)(DECK_CREW.find(x => x.p.id === 'calder')), meet: INTRO_UI.meet.map(x => x.id) })")))
        elif who and 'calder' in who['lines'] and who['cal'] != 'Works bay' and g.ev('shipNow() < introAbs(1, 540)'): fail('Calder speaks the briefing from ' + str(who['cal']))
        # the lead (0.42.30): the briefing plays in full at a reader's pace (a tap every ~3 s) before the shadow shift starts
        bf = { 'start': g.ev('clockText()'), 'n': g.ev('DIALOGUE ? DIALOGUE.queue.length : 0'), 'taps': 0, 'cut': None, 'follow': None }
        while g.ev('!!DIALOGUE') and bf['taps'] < 60:
            if bf['follow'] is None and g.ev("(e => !!e && e.mode === 'follow')(escortPlan(ROSTER.find(p => p.id === INTRO_ESCORT), shipNow()))"): bf['follow'] = g.ev('clockText()')
            g.ev('(() => { const l = DIALOGUE.queue[DIALOGUE.i]; if (l && l.choice) dialogueChoose(0); else dialogueNext(); })()'); bf['taps'] += 1
            if not g.ev('!!DIALOGUE'): break                # our tap on its last line ended it
            g.step(100)                                     # (about 3 s: reading the next line)
            if not g.ev('!!DIALOGUE'): bf['cut'] = g.ev('clockText()')   # it went away by itself
        bf['end'] = g.ev('clockText()'); bf['met'] = g.ev("SHIP.intro.done['d1-briefing:met']")
        print(f"  the briefing at a reader's pace: {bf['n']} lines, {bf['taps']} taps, {bf['start'].split()[-1]} to {bf['end'].split()[-1]}; Torres on the shadow shift from {bf['follow'] or 'after it'}")
        if bf['cut']: fail(f"the briefing closed before its last line: {bf}")
        if bf['follow']: fail(f"the shadow shift began during the briefing ({bf['follow']}): {bf}")
        for i in range(40):
            g.step(30)
            if g.ev("shipNow() >= introAbs(1, INTRO_WEEK.find(b => b.id === 'd1-shadow').at + 1)"): break
        took = g.ev("claimJob(SHIP.jobs.find(x => x.reserved === 1).id)")
        # the first week's work day is the ship's day shift (TS3, a planted fault: DAY_SHIFT an hour late went unnoticed):
        # the shadow beat starts within 15 minutes of the shift's start, and you're on your shift when you take its job
        sh = g.ev("({ t: clockText(), m: SHIP.time.min, beat: INTRO_WEEK.find(b => b.id === 'd1-shadow').at, from: DAY_SHIFT[0], to: dayShiftEnd(SHIP.time.day), on: playerShiftOn(SHIP.time.day) })")
        if not (sh['on'] and sh['from'] <= sh['m'] < sh['to'] and 0 <= sh['beat'] - sh['from'] <= 15): fail(f"the shadow shift is not the day shift's start: the beat at {sh['beat'] // 60:02d}:{sh['beat'] % 60:02d}, the job taken {sh['t']}, the shift {sh['from'] // 60:02d}:{sh['from'] % 60:02d}-{sh['to'] // 60:02d}:{sh['to'] % 60:02d}: {sh}")
        g.step(60)
        esc = g.ev("(() => { const a = DECK_CREW.find(x => x.p.id === INTRO_ESCORT), e = escortPlan(ROSTER.find(p => p.id === INTRO_ESCORT), shipNow()), pp = player.obj.position; return { mode: e && e.mode, d: a ? Math.round(Math.hypot(a.x - pp.x, a.z - pp.z)) : null }; })()")
        fin = g.ev("(() => { const j = SHIP.jobs.find(x => x.reserved === 1); jobStops(j).forEach((s, k) => jobStepDone(j.id, k)); j.workDone = true; return { t: turnInJob(j.id), shadow: !!SHIP.intro.settle.shadow, mem: (SHIP.notes || []).some(n => n.kind === 'introStep' && n.step === 'd1-shadow') }; })()")
        print(f"  took it: {took}; Torres {esc['mode']}, {esc['d']} tiles from you; turned in: {fin['t']}; 'Shadow a job' ticked: {fin['shadow']}; d1-shadow note: {fin['mem']}")
        if not took: fail('could not take the shadow job at 09:06')
        if esc['mode'] != 'follow' or esc['d'] is None or esc['d'] > 4: fail(f'Torres is not with you on the shadow shift: {esc}')
        if not (fin['t'] and fin['shadow'] and fin['mem']): fail(f'the shadow job did not complete the intro\'s side: {fin}')
        # reviewer 1's lows (0.42.25): the health check booked once as a 'checkup', rebooked once when missed; a Mail
        # from Pell when she never found you on Wednesday evening
        if g.ev("typeof introHealthAppt === 'function' && typeof apptPlaces === 'function' && !!SHIP.device && Array.isArray(SHIP.device.appts)"):
            g.ev('(() => { goToDeck(5); player.obj.position.copy(cellPos(15, 3)); })()'); g.step(5)
            g.ev('skipTo(introAbs(2, 15 * 60))'); g.step(60)
            h = g.ev("(() => { const A = SHIP.device.appts.filter(a => a.title === INTRO_HEALTH_TITLE); return { appts: A.map(a => [hhmm(a.at % 1440), Math.floor(a.at / 1440), a.status, a.kind]), again: SHIP.intro.done['d2-health:again'] !== undefined, mail: SHIP.mail.some(m => /Health check, again/.test(m.subject)) }; })()")
            print(f"  the health check missed on Tuesday: {h}")
            if not h['again'] or len([x for x in h['appts'] if x[2] == 'yes']) != 1 or any(x[3] != 'checkup' for x in h['appts']) or not h['mail']: fail(f'a missed health check is not booked again once: {h}')
            g.ev('skipTo(introAbs(3, 20 * 60 + 5))'); g.step(60)
            pm = g.ev("(() => { const ask = ((SHIP.social && SHIP.social.seekAsks) || []).find(a => a.id === 'pell'); return { asked: !!ask, done: ask ? ask.done : null, mail: (SHIP.mail.find(m => m.from === 'Mira Pell' || /Pell/.test(m.from)) || {}).subject || null, seek: SHIP.intro.done['d3-pell:seek'] }; })()")
            print(f"  Pell's Wednesday ask (you were away): {pm}")
            if pm['seek'] is None or (not pm['done'] and not pm['mail']): fail(f'no Mail when Pell never found you: {pm}')
            if not pm['asked']: fail(f'Pell was never asked to come and find you on Wednesday (socialSeekAsk): {pm}')   # TS3, a planted fault
    firsts(g)
    week(g)
    talk_away(g)
    beside_walk(g)
    late_dinner(g)
    patch923(g)
    dinner_reload(g)
    bunk_leave(g)   # last: its reload leaves the page on a saving URL
    solo(g)
    solo_tap(g)
    if g.errors: fail('page errors: ' + ' | '.join(g.errors[:6]))
    g.close()

print('OK' if ok else 'FAILED')
sys.exit(0 if ok else 1)
