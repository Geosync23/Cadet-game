# Starship Cadet: the ending (EN1 for lead 39; plans/ending-spec.html on claude/p5-specs, EP2). On paper, in one page
# (the game's own functions at the times they'd run, no walking), like promo_beats_check:
#   off:     the build as given (EV_ENDING_ON off): no SHIP.end, no ending occasion, no "About the transfer", no arrows
#            on Day 32, nothing in the save
#   offer:   (a copy with EV_ENDING_ON on) the offer's day: Day 32 with Step 6 off; with Step 6 on, Day 32 after Calder's
#            question on Day 26, the Thursday after a later answer, none before one. Booked at 06:00 on the day (the
#            ready room at 16:00, the notice, Vance's Mail, the level 1 arrow from 15:45); in the room it plays, your
#            reply, Calder's walk after; late, Calder comes to find you and it plays where you are after 18:00
#   answers: "About the transfer" on the Captain's chat card only while it's open; Stay, Go, Not sure; changing your
#            mind; "Tell the Captain" at level 6, level 1 on Saturday from 18:00; her search at 19:30 with nothing said;
#            settled at her address on Sunday (end.stay / end.go); Not sure at the address: she asks, Stay or Go only;
#            nothing open after; a save and a reload keep it all
#   reload:  a real save between the offer and the answer (served from a web address, as saves_check does), reloaded:
#            SHIP.end the same, the offer's scene and "About the transfer" still there
#   keep:    (the same web page) no way back (the user, 2026-10-26): no copy of the save is ever written, nothing in the
#            Saves app; the end page marks the save ended and a reload shows it again with Keep this ending and Start a new game
#   endpage: the end page on paper: its rows (name and rank, days, ranks, friends, Zeke), its buttons, the page's focus
#   goodbye: (its own page at phone size, 390 x 844) Monday, gone: the notice at 06:00; from 09:15 the shuttle bay holds
#            about 60 with the aisle clear; draw calls under 450; the arrow names each farewell in turn (friends, the Chief,
#            Commander Vance, the Captain), each says goodbye as you reach them; Zeke's scene at the ramp; inside the Tern the
#            ramp closes, the save is marked ended and the end page opens
#   pad:     (a copy with the controller on too, PAD_ON, and a pretend pad) the end page by pad: the highlight on its first
#            button, the D-pad moves it to the second, A presses it, B does nothing (it must be answered)
#   limits:  (RV21's review) Monday (Go) is no shift: careerOff, no missed shift counted; the last breakfast's arrow is level 1
#            and Pell comes for you from 08:30; Zeke comes for you at 10:15 if you're not in the bay; from noon (you away) only
#            the farewells and Zeke wait; nothing at night; the end page's keepsakes are named, the ship's decor left out
#   week:    Friday: the friends come to you one at a time (seek asks), each with "About the transfer" and their own take;
#            Zeke after dinner (arrow level 1 "Talk to Zeke", he finds you, the scene); a call home plays your family's
#            scene once; the Schedule's rows (your answer by Saturday 20:00, Zeke); the Record's lines
#   endgame: (EN2, E-4) the endgame lines never before end.stay nor before its day; `endgame` every hour of the first
#            14 days, about 4 hours in 10 after; `endgame:early` only in the first 14; `endgame:false` the other way; no
#            calendar row after the crossing back once you've stayed; "What's next" and the Works app's last page; the
#            first morning (the Captain's breakfast, its row, the notice once, the level 1 arrow); a New game clears it
#   crossing: (EN2, E-1) the crossing back on paper, for each answer before the address (none, Go, Stay, Not sure, and no
#            offer yet): the calendar's row Day 31, the phases, the oath's meeting, the guard's rows, the status line by
#            day; Vance comes to you; the notices; the ship's arrow and Saruth at the glass; the oath's arrow; the sky
#            ship's poses; the oath with your lines; Saruth's signal, then the address (asked first when not firm; plain
#            with no offer) and settled at it; the record; the certificate and the plaque; the supper
# Setup and environment as for cadet_test.py (CADET_WORK, CADET_CHROME).
# Run:  python3 ending_check.py BUILD.html [part ...]   Good is ENDING CHECK OK (exit 0); a failure exits 1.
import sys, pathlib, json
exec(open(__file__.replace('ending_check.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
# (BM19, lead 42, 0.95.0) the parts here set the clock straight to the offer's day (Day 32): with Step 6 on, the offer
# waits for Calder's question (the career's end), so the check runs on a copy with P5_STEP6 off; Step 6's way into the
# ending is promo_beats_check's cq parts and arrows_check step6's. The copy's line assigns the global window.P5_STEP6 (R3's find;
# the game's script is wrapped in a function, so a const or var there would hide it) so part_offer's = true reaches endStep6
_s6 = re.compile(r"^const P5_STEP6 = P5_STEP5 && true;.*$", re.M); _src0 = pathlib.Path(sys.argv[1]).read_text()
if _s6.search(_src0):
    _off6 = WORK / 'test' / ('ending_s6off_' + pathlib.Path(sys.argv[1]).name); _off6.write_text(_s6.sub(lambda m: "window.P5_STEP6 = P5_STEP5 && URL_FLAGS.has('p5s6');", _src0, count=1))
    print(f'(on a copy with P5_STEP6 off: {_off6.name})'); sys.argv[1] = str(_off6)

ok = True
def fail(msg):
    global ok
    ok = False
    print('FAIL', msg)
def check(cond, msg):
    if not cond: fail(msg)
    return cond

ONLY = set(sys.argv[2:])
SWITCH = "const EV_ENDING_ON = URL_FLAGS.has('ending');"
SETUP = r"""(() => {
  window.__toasts = []; toast = (a, b) => { window.__toasts.push([String(a), String(b || '')]); };
  window.__notes = []; deviceNotify = o => { window.__notes.push(String(o && o.text)); };
  window.__said = []; worksSay = (id, t) => { window.__said.push(id + ': ' + t); };
  window.__tick = (skip = false) => { for (const f of WORK_TICKS) try { f(shipNow(), skip); } catch (e) { console.error(e); } };
  window.__mail = () => SHIP.mail.map(m => m.from + ': ' + m.subject + ' | ' + m.body);
  window.__guide = id => { const e = GUIDE.list.find(x => x.id === id); return e ? { level: e.level, from: e.from, until: e.until } : null; };
  window.__reset = (day, min) => { if (DIALOGUE) dialogueEnd(true); if (typeof SHIP.end !== 'undefined') SHIP.end = null; SHIP.occasions.length = 0; MEETINGS.length = 0; SHIP.mail = []; SHIP.flags = {};
    GUIDE.list.length = 0; CREW_SCENE.clear(); setShipNow((day - 1) * 1440 + min); __toasts.length = 0; __notes.length = 0; __said.length = 0; };
  window.__to = (deck, room) => { if (deckDef.num !== deck) goToDeck(deck); player.obj.position.copy(cellPos(...ROOM_TILES[room][0])); };
  window.__marrow = () => schedPeople().find(p => p.id === 'marrow');
  window.__run = (k) => { let n = 0; while (DIALOGUE && n++ < 40) { const v = dialogueView(); if (v && v.choices) dialogueChoose(k); else dialogueNext(); } return n; };
  window.endStaySet = d => flagSet('end.stay', d);   // EN2's (29c), as it will be
  window.__tell = (k) => { const p = __marrow(); endChatDo(p, 'tell'); if (!DEV.choose) return null; devChosen(k); const id = DIALOGUE && DIALOGUE.id; __run(0); return id; };
  window.__lines = () => { const out = []; let n = 0; while (DIALOGUE && n++ < 40) { const v = dialogueView(); if (!v) break; if (v.choices) return { out, choices: v.choices }; out.push(v.name + ': ' + v.text); dialogueNext(); } return { out, choices: null }; };
  return true;
})()"""

SETUP2 = r"""(() => {
      window.__at = (d, m) => { setShipNow((d - 1) * 1440 + m); };
  // every baked line with an endgame condition: [kind, entry, speaker] (the shared bank, the templates, the voice cards)
  window.__eg = () => { const out = [], who = ROSTER.filter(p => !p.guest).slice(0, 12);
    for (const k in LINES) if (Array.isArray(LINES[k])) for (const e of LINES[k]) if (e && e.endgame != null) out.push([k, e]);
    for (const id in VOICE) for (const k in (VOICE[id].lines || {})) for (const e of VOICE[id].lines[k]) if (e && e.endgame != null) out.push([k, e, id]);
    return { lines: out, who }; };
  // how many of the endgame lines hold for these speakers at minute t (each line, each speaker)
  window.__egHold = (t, want) => { const { lines, who } = __eg(); let n = 0, all = 0;
    for (const [k, e, id] of lines) for (const p of id ? [ROSTER.find(q => q.id === id)].filter(Boolean) : who) {
      if (String(e.endgame) !== want) continue; all++; if (lineCond('endgame', e.endgame, p, { t })) n++; }
    return [n, all]; };
  return true;
})()"""

def part_off_end(g):
    print('(off) EN2: no endgame, no crossing back:')
    r = g.ev("""(() => { const out = {}; out.sw = typeof EV_ENDING_ON === 'undefined' ? null : EV_ENDING_ON; SHIP.flags = SHIP.flags || {};
      const plan0 = JSON.stringify(evCalPlan()); __at(36, 300); const next0 = worksNext();
      flagSet('end.stay', 36); out.day = endgameDay(); out.on = endgameOn(); out.set = false;
      out.plan = JSON.stringify(evCalPlan()) === plan0; out.next = worksNext() === next0; out.occ = typeof OCCASIONS.endFirstMorning;
      out.items = END_ITEMS.reduce((n, f) => n + (f(36) || []).length, 0); out.rows = devDay(36).filter(x => /Captain/.test(x.title)).length;
      const p = ROSTER[3]; out.cond = [lineCond('endgame', 'true', p, { t: shipNow() }), lineCond('endgame', 'false', p, { t: shipNow() })];
      __tick(); out.tab = (WORKS_TABS || []).some(x => x.id === 'home'); out.notes = __notes.length;
      out.cb = [!!SHIP_EVENTS.crossingBack, EV_CALENDAR.some(x => x.id === 'crossingBack'), crossingBackShip(34 * 1440), crossingBackDone()];
      flagSet('end.stay', null); return out; })()""")
    print('   ', r)
    check(r['cb'] == [False, False, None, False], f"off: no crossing back ({r['cb']})")
    check(r['sw'] is False, f"off: EV_ENDING_ON is false in the build ({r['sw']})")
    check(r['day'] is None and not r['on'] and not r['set'], f"off: no endgame whatever the flag says ({r})")
    check(r['plan'] and r['next'] and r['occ'] == 'undefined' and r['items'] == 0 and r['rows'] == 0, f"off: the calendar, What's next, no first morning, no rows ({r})")
    check(r['cond'] == [False, True] and not r['tab'] and r['notes'] == 0, f"off: endgame lines never hold, no tab, no notice ({r})")

def part_endgame(g):
    g.ev('SHIP.end = null')
    print('(endgame) the switch on:')
    r = g.ev("""(() => { const out = {}; SHIP.flags = SHIP.flags || {}; flagSet('end.stay', null); SHIP.occasions.length = 0;
      const lines = __eg(); out.n = lines.lines.length;
      // before the flag: Days 30-36 every hour
      let pre = 0; for (let d = 30; d <= 36; d++) for (let m = 0; m < 1440; m += 60) pre += __egHold((d - 1) * 1440 + m, 'true')[0];
      out.pre = pre; out.preFalse = __egHold(36 * 1440 - 600, 'false');
      // the address settles Stay on Day 35: the endgame from Day 36
      __at(35, 905); out.set = endStaySet(30); out.day = endgameDay(); out.on35 = endgameOn(); out.d35 = __egHold(shipNow() + 60, 'true')[0];
      let first = [0, 0]; for (let d = 36; d < 50; d++) for (let m = 0; m < 1440; m += 60) { const [n, a] = __egHold((d - 1) * 1440 + m, 'true'); first[0] += n; first[1] += a; }
      let later = [0, 0]; for (let d = 50; d < 64; d++) for (let m = 0; m < 1440; m += 60) { const [n, a] = __egHold((d - 1) * 1440 + m, 'true'); later[0] += n; later[1] += a; }
      let early = [0, 0]; for (let d = 50; d < 64; d++) for (let m = 0; m < 1440; m += 60) { const [n, a] = __egHold((d - 1) * 1440 + m, 'early'); early[0] += n; early[1] += a; } out.early = early;
      out.first = first; out.later = later; out.postFalse = __egHold(40 * 1440, 'false');
      // a line said: lineFor gives an endgame greet on Day 36 to a crew member with no own greet line under it
      __at(36, 600); const who = ROSTER.find(p => p.id === 'holt'); { const r = relGet('holt'); r.pts = 999; r.tier = relTierOf(999); }   // a friend: the pool's greets are by tier
      out.say = who ? (lineFor(who, 'greet', { peek: true }) || {}).id : null; { const all = []; for (const src of [LINES, ...Object.values(VOICE).map(v => v.lines || {}), ...Object.values(VOICE_TEMPLATES).map(v => v.lines || {})]) for (const e of (src.greet || [])) if (e.endgame != null) all.push(e.id); out.egAll = all; } out.egIds = lines.lines.filter(x => x[0] === 'greet' && (!x[2] || x[2] === 'holt')).map(x => x[1].id);
      // the calendar closed for good: a row planted on Day 40 is planned without the flag, never with it
      SHIP_EVENTS.endTestLate = { title: 'test', days: 2, phases: [{ id: 'warning', at: [0, 360] }] }; EV_CALENDAR.push({ id: 'endTestLate', day: 40, kind: 'short' });
      const keep = SHIP.flags['end.stay']; flagSet('end.stay', null); out.planOff = evCalPlan().some(x => x.id === 'endTestLate');
      flagSet('end.stay', keep); out.planOn = evCalPlan().some(x => x.id === 'endTestLate'); out.cross = endCalClosed({ id: 'crossingBack', day: 35 });
      EV_CALENDAR.pop(); delete SHIP_EVENTS.endTestLate;
      // What's next and the Works app's last page
      __at(35, 1200); out.next35 = worksNext(); __tick(); out.tab35 = (WORKS_TABS || []).some(x => x.id === 'home');
      __at(36, 300); out.next36 = worksNext(); __tick(); out.tab36 = (WORKS_TABS || []).some(x => x.id === 'home');
      try { WORKS_TAB = 'home'; const v = worksView(); out.page = v.blocks.filter(b => b.kind === 'text').map(b => b.text).join(' / '); } catch (e) { out.page = 'error ' + e; }
      WORKS_TAB = 'training';
      return out; })()""")
    print('   ', {k: r[k] for k in r if k not in ('egIds', 'egAll')})
    check(r['n'] > 0, f"endgame: there are endgame lines in the build ({r['n']})")
    check(r['pre'] == 0 and r['preFalse'][0] == r['preFalse'][1], f"endgame: no endgame line holds before the flag, every endgame:false one does ({r['pre']}, {r['preFalse']})")
    check(r['set'] and r['day'] == 36 and not r['on35'] and r['d35'] == 0, f"endgame: endStaySet gives Day 36 at the earliest; not on Day 35 ({r})")
    check(r['first'][1] > 0 and r['first'][0] == r['first'][1], f"endgame: every hour of the first 14 days ({r['first']})")
    check(r['early'][1] > 0 and r['early'][0] == 0, f"endgame: endgame:early lines only in the first 14 days ({r['early']})")
    fr = r['later'][0] / max(1, r['later'][1])
    check(.25 <= fr <= .55, f"endgame: about 4 hours in 10 after the first 14 days ({r['later']}, {fr:.2f})")
    check(r['postFalse'][0] == 0, f"endgame: endgame:false lines never hold after ({r['postFalse']})")
    check(r['say'] in r['egAll'], f"endgame: lineFor picks an endgame greet on Day 36 ({r['say']} not in {len(r['egAll'])} endgame greets)")
    check(r['planOff'] and not r['planOn'] and not r['cross'], f"endgame: a calendar row after Day 35 is planned before you stay, never after; the crossing back itself never closed ({r})")
    check('home' not in r['next35'].lower() and 'The Wren is home' in r['next36'] and not r['tab35'] and r['tab36'], f"endgame: What's next and the last page from Day 36 ({r['next35']} | {r['next36']}, tab {r['tab35']} {r['tab36']})")
    check('The Wren is home' in r['page'], f"endgame: the last page's words ({r['page']})")

    print('(endgame) the first morning:')
    r = g.ev("""(() => { const out = {}; __at(36, 240); __notes.length = 0; GUIDE.list.length = 0; SHIP.occasions = SHIP.occasions.filter(x => x.id !== 'endFirstMorning');
      occasionsTick(shipNow(), true); const rec = SHIP.occasions.find(x => x.id === 'endFirstMorning');
      out.booked = rec ? hhmm(rec.at % 1440) + ' ' + rec.len + ' ' + rec.deck + rec.room : null; out.script = !!MEETING_SCRIPTS.endingFirstMorning;
      out.rows = devDay(36).filter(x => x.kind === 'beat').map(x => hhmm(x.from) + ' ' + x.title);
      out.rows35 = devDay(35).filter(x => /Captain/.test(x.title)).length + devDay(37).filter(x => /Captain/.test(x.title)).length;
      __at(36, (rec ? rec.at % 1440 : 450) - 40); __tick(); out.notes = __notes.slice(); const e0 = GUIDE.list.find(x => x.id === 'end:fm');
      out.arrow = e0 ? [e0.level, hhmm(e0.from % 1440), hhmm(e0.until % 1440), e0.goal().deck, e0.goal().room, e0.goal().label] : null;
      __tick(); __at(36, (rec ? rec.at % 1440 : 450) - 39); __tick(); out.notes2 = __notes.length;
      if (rec) rec.met = true; out.done = e0 ? !!e0.done() : null;
      // a New game: the flag, the tab
      SHIP.flags = {}; simNote('newGame', { arrival: 0 }); out.after = [endgameDay(), (WORKS_TABS || []).some(x => x.id === 'home')];
      return out; })()""")
    print('   ', r)
    check(r['booked'] and r['booked'].endswith('3M') and r['script'], f"first morning: booked on Day 36 in the mess, its script baked ({r['booked']}, {r['script']})")
    check(any('Breakfast with the Captain' in x for x in r['rows']) and r['rows35'] == 0, f"first morning: the Schedule row on Day 36 only ({r['rows']}, {r['rows35']})")
    check(len(r['notes']) == 1 and 'back on her course' in r['notes'][0] and r['notes2'] == 1, f"first morning: the notice once ({r['notes']}, {r['notes2']})")
    check(r['arrow'] and r['arrow'][0] == 1 and r['arrow'][3] == 3 and r['arrow'][4] == 'M', f"first morning: a level 1 arrow to the mess ({r['arrow']})")
    check(r['done'] is True, f"first morning: the arrow clears when met ({r['done']})")
    check(r['after'] == [None, False], f"first morning: a New game clears the endgame ({r['after']})")

CROSS = r"""((ans) => { const out = { notes: [] }; if (DIALOGUE) dialogueEnd(true); SHIP.flags = SHIP.flags || {}; for (const k of ['end.stay', 'end.go', 'end.cb.stay', 'end.cb.go']) flagSet(k, null);
  SHIP.end = ans === 'plain' ? null : endClean({ offer: { day: 32, met: true, how: 'room' }, said: ans ? [[33, ans]] : [] });
  const plan = evCalPlan(); out.row = plan.find(r => r.id === 'crossingBack') || null;
  SHIP.event = null; SHIP.eventLog.length = 0; for (const r of plan) if (r.id !== 'crossingBack') SHIP.eventLog.push({ id: r.id, startDay: r.day, endDay: r.day + SHIP_EVENTS[r.id].days, band: 'smooth' });
  out.due = eventDueDay(); __at(31, 1); eventAdvance(shipNow(), true); out.started = SHIP.event ? SHIP.event.id + '@' + SHIP.event.startDay : null;
  const ph = []; for (const [d, m] of [[31, 479], [31, 480], [35, 869], [35, 870], [35, 914], [35, 915], [35, 1154], [35, 1155], [35, 1439]]) { const n = eventNow((d - 1) * 1440 + m); ph.push(d + ' ' + hhmm(m) + ' ' + (n ? n.id + '.' + n.phase : '-')); }
  out.phases = ph; const mt = MEETINGS.find(x => x.id === 'crossingBackOath'); out.meet = mt ? [Math.floor(mt.at / 1440) + 1, hhmm(mt.at % 1440), mt.len, mt.script] : null;
  out.beats = EV_BEATS.filter(b => b.id === 'crossingBack' || b.id === 'endingOffer').map(b => b.id + ' ' + b.kind + ' ' + b.day + ' ' + b.at.join('-'));
  out.status = [31, 34, 35].map(d => { setShipNow((d - 1) * 1440 + 600); return eventStatus(shipNow()); });
  out.scripts = ['crossingBackWord', 'crossingBackOath', 'crossingBackSignal', 'crossingBackAddress.stay', 'crossingBackAddress.go', 'crossingBackAddress.ask', 'crossingBackAddress.plain', 'endingZekeSunday.stay', 'endingZekeSunday.go', 'endingFirstMorning'].filter(k => !MEETING_SCRIPTS[k]);
  const M = SHIP.event.mine, T = m => { setShipNow(m); crossingBackTick(m); }, d = (day, m) => (day - 1) * 1440 + m, run = (k = 0) => { const L = []; let n = 0; while (DIALOGUE && n++ < 60) { const v = dialogueView(); if (!v) break; L.push(v.choices ? '?' : v.who); dialogueStep(v.choices ? k : undefined); } return L; };
  __notes.length = 0; GUIDE.list.length = 0; CREW_SCENE.clear();
  T(d(31, 509)); out.vanceEarly = CREW_SCENE.has('vance'); T(d(31, 510)); out.vance = CREW_SCENE.has('vance') ? CREW_SCENE.get('vance').mode : null;
  out.vanceFor = crossingBackMoment('crossingBackWord', ['vance'], ['story:vance', 1]); run();
  T(d(31, 520)); out.vanceDone = [M['story:vance'], CREW_SCENE.has('vance')]; out.notes.push(...__notes.splice(0));
  T(d(34, 599)); T(d(34, 600)); const sh = GUIDE.list.find(x => x.id === 'end:cb:ship'); out.shipArrow = sh ? [sh.level, sh.goal().room] : null; out.shipDone0 = sh ? sh.done() : null; out.saruth = CREW_SCENE.has('saruth') ? CREW_SCENE.get('saruth').to : null; out.notes.push(...__notes.splice(0));
  out.sky = [[34, 599], [34, 600], [35, 869], [35, 870], [35, 893], [35, 899], [35, 900]].map(([dd, m]) => { const x = crossingBackShip(d(dd, m)); return x ? x.pose + (x.flash ? '*' : '') : '-'; });
  T(d(35, 400)); T(d(35, 840)); const oa = GUIDE.list.find(x => x.id === 'end:cb:oath'); out.oathArrow = oa ? [oa.level, oa.goal().deck, oa.goal().room, oa.goal().label] : null;
  T(d(35, 870)); goToDeck(4); CREW_SCENE.clear(); T(d(35, 875)); out.fetch = CREW_SCENE.has('vance') ? CREW_SCENE.get('vance').mode : null; CREW_SCENE.clear(); out.notes.push(...__notes.splice(0)); out.cert0 = crossingBackDone();
  goToDeck(3); player.obj.position.copy(cellPos(...ROOM_TILES['L'][Math.floor(ROOM_TILES['L'].length / 2)]));
  out.shipDone1 = sh ? sh.done() : null;
  setShipNow(d(35, 880)); meetingsTick(shipNow()); out.oathShown = DIALOGUE ? DIALOGUE.id : null; out.oath = run();
  const seen = []; for (let i = 0; i < 4 && !M['story:address']; i++) { T(d(35, 900 + i)); if (DIALOGUE) { seen.push(DIALOGUE.id); out['run' + i] = run(0).join(','); } }
  out.address = seen; out.settled = cbEnd(() => endingChoice()); out.endStay = flag('end.stay'); out.day = endgameDay();
  T(d(35, 915)); out.record = ADDRESSES.length ? ADDRESSES[ADDRESSES.length - 1].text : null; out.cert = crossingBackDone();
  out.plaque = (() => { try { return DECK_DRESS.linePlaque.make(new THREE.Group()).x; } catch (e) { return 'error ' + e.message; } })();
  out.supper = (EV_DAY_DRESS.get('sunday-table@35') || {}).o ? EV_DAY_DRESS.get('sunday-table@35').o.name : null;
  out.here = (LINES['event.crossingBack.gather.lineSupper.here'] || []).length + ' > ' + evLinesOf('event.crossingBack.gather.lineSupper.here').length;
  __at(36, 1); eventAdvance(shipNow(), true); out.logged = SHIP.eventLog.some(l => l.id === 'crossingBack'); out.next = eventDueDay();
  goToDeck(4); SHIP.end = null; return out; })"""

def part_crossing(g):
    for ans, want in [(None, 'stay'), ('go', 'go'), ('stay', 'stay'), ('unsure', 'stay'), ('plain', None)]:
        print(f'(crossing) your answer before the address: {ans}')
        r = g.ev(CROSS + '(' + ('null' if ans is None else repr(ans)) + ')')
        print('   ', {k: r[k] for k in r if k not in ('notes', 'phases')})
        print('    notes:', r['notes'])
        check(not r['scripts'], f"crossing: the scenes are baked ({r['scripts']})")
        check(r['row'] and r['row']['day'] == 31 and r['due'] and r['due']['id'] == 'crossingBack' and r['started'] == 'crossingBack@31', f"crossing: the calendar's row on Day 31, due and started ({r['row']}, {r['due']}, {r['started']})")
        check(r['phases'] == ['31 07:59 -', '31 08:00 crossingBack.warning', '35 14:29 crossingBack.warning', '35 14:30 crossingBack.onset', '35 15:14 crossingBack.onset', '35 15:15 crossingBack.resolution', '35 19:14 crossingBack.resolution', '35 19:15 crossingBack.afterglow', '35 23:59 crossingBack.afterglow'], f"crossing: the phases at their minutes ({r['phases']})")
        check(r['meet'] == [35, '14:40', 35, 'crossingBackOath'] and len(r['beats']) == 2, f"crossing: the oath's meeting Sunday 14:40, the guard's rows ({r['meet']}, {r['beats']})")
        check(all(r['status']) and len(set(r['status'])) == 3, f"crossing: the status line by day (the word, the vessel, the morning) ({r['status']})")
        check(not r['vanceEarly'] and r['vance'] == 'follow' and r['vanceFor'] and r['vanceDone'] == [1, False], f"crossing: Vance comes to you from 08:30 and his word ends it ({r['vance']}, {r['vanceDone']})")
        n = ' | '.join(r['notes'])
        check('coming to find you' in n and 'leading the oath' in n and 'off the bow' in n and 'Today at 14:30' in n and 'horn' in n.lower(), f"crossing: the notices, Vance, the ship, the morning, the horn ({r['notes']})")
        check(r['shipArrow'] == [2, 'L'] and r['saruth'] == '3-bow-lounge-line-lead-4' and r['oathArrow'] and r['oathArrow'][:3] == [1, 3, 'L'] and 'Lead the oath' in r['oathArrow'][3], f"crossing: the ship's arrow (2), Saruth at the glass, the oath's arrow (1) ({r['shipArrow']}, {r['saruth']}, {r['oathArrow']})")
        check(r['shipDone0'] is False and r['shipDone1'] is True, f"crossing: the ship's arrow clears once you're in the bow lounge ({r['shipDone0']}, {r['shipDone1']})")
        check(r['fetch'] == 'follow' and 'oath is waiting' in n, f"crossing: not in the lounge at 14:35, Vance comes to find you ({r['fetch']})")
        check(r['sky'] == ['-', 'bow', 'bow', 'alongside', 'alongside*', 'alongside', '-'], f"crossing: the Veyli ship's poses ({r['sky']})")
        check(r['oathShown'] == 'crossingBackOath' and r['oath'].count('?') >= 3, f"crossing: the oath played with your lines as one-reply choices ({r['oathShown']}, {r['oath']})")
        exp = ['moment:crossingBackSignal', 'moment:crossingBackAddress.' + ({None: 'ask', 'unsure': 'ask', 'plain': 'plain'}.get(ans) or want)]
        check(r['address'] == exp and r['settled'] == want, f"crossing: the signal, then the address {exp[1]}, settled {want} ({r['address']}, {r['settled']})")
        check((r['day'] == 36 and r['endStay'] == 36) == (want == 'stay'), f"crossing: Stay settled at the address starts the endgame on Day 36 ({r['endStay']}, {r['day']})")
        if ans in (None, 'unsure'): check(r.get('run1', '').count('Marrow') >= 5 and r.get('run1', '').count('?') == 2, f"crossing: after the ask, the rest of the Stay address plays ({r.get('run1')})")
        rec = {'stay': 'staying', 'go': 'Concord', None: 'reach'}[want]
        check(r['record'] and rec in r['record'], f"crossing: the address's record ({r['record']})")
        check(not r['cert0'] and r['cert'] and 'crossed back' in r['plaque'], f"crossing: the certificate's second date and the plaque's line from 15:15 ({r['cert0']}, {r['cert']}, {r['plaque'][-90:]})")
        check(r['supper'] and r['logged'] and r['next'] is None, f"crossing: the Line supper, logged at its end, nothing after ({r['supper']}, {r['logged']}, {r['next']})")

def part_off(g):
    print('(off) the build as given:')
    r = g.ev("""(() => { __reset(32, 360); __tick(); setShipNow(31 * 1440 + 950); __tick();
      const p = __marrow(); const save = {}; try { SAVE_EXTRA.forEach(f => f({ ship: {}, player: {} })); } catch (e) { /* */ }
      return { on: EV_ENDING_ON, end: typeof SHIP.end, occ: typeof OCCASIONS.endingOffer, booked: SHIP.occasions.length, btn: typeof endChatButton === 'function' ? endChatButton(p) : 'none',
        guide: GUIDE.list.filter(e => /^end:/.test(e.id)).length, scripts: Object.keys(MEETING_SCRIPTS).filter(k => /^moment:ending/.test(k)) }; })()""")
    print('   ', r)
    check(r['on'] is False and r['end'] == 'undefined' and r['occ'] == 'undefined' and r['booked'] == 0, f"off: no SHIP.end, no ending occasion, nothing booked ({r})")
    check(r['btn'] is None and r['guide'] == 0 and not r['scripts'], f"off: no button, no arrows, no scripts ({r})")

def part_offer(g):
    print('(offer) the day, the booking, the room, Calder:')
    r = g.ev("""(() => { const out = {}; __reset(20, 600);
      out.plain = endOfferDay(); window.P5_STEP6 = true; SHIP.works = SHIP.works || worksInit();
      delete SHIP.works.end; out.none = endOfferDay(); SHIP.works.end = { answer: 'teach the new cadets', day: 26 }; out.steady = endOfferDay(); out.post = endPostKind();
      SHIP.works.end = { answer: 'engines', day: 33 }; out.slow = endOfferDay(); out.week = endWeek(); window.P5_STEP6 = false; delete SHIP.works.end; out.back = endOfferDay(); return out; })()""")
    print('   ', r)
    check(r['plain'] == 32 and r['none'] is None and r['steady'] == 32 and r['slow'] == 39 and r['back'] == 32, f"offer: Day 32 (Step 6 off), none before Calder's question, Day 32 after Day 26, Day 39 after Day 33 ({r})")
    check(r['post'] == 'teach' and r['week'] == {'offer': 39, 'due': 41, 'settle': 42, 'leave': 43}, f"offer: the post by your answer, the slower week ({r})")
    r = g.ev("""(() => { __reset(32, 359); __tick(); const before = !!(SHIP.end && SHIP.end.offer); setShipNow(31 * 1440 + 361); __tick();
      const o = SHIP.occasions.find(x => x.id === 'endingOffer'); setShipNow(31 * 1440 + 946); __tick();
      return { before, offer: SHIP.end.offer, occ: o && [hhmm(o.at % 1440), o.len, o.deck, o.room], notes: __notes.slice(), mail: __mail(), arrow: __guide('end:offer'),
        door: occasionDoorOpen(1, 'R', 31 * 1440 + 1070), shut: occasionDoorOpen(1, 'R', 31 * 1440 + 1090), appt: (SHIP.device.appts || []).filter(a => a.occ && /endingOffer/.test(a.occ)).map(a => hhmm(a.at % 1440) + ' ' + a.with.join('+')) }; })()""")
    print('   ', r)
    check(not r['before'] and r['offer'] and r['offer']['day'] == 32 and r['occ'] == ['16:00', 120, 1, 'R'], f"offer: booked at 06:00 on Day 32: 16:00 in the ready room, open till 18:00 ({r})")
    check(any('16:00' in n for n in r['notes']), f"offer: the morning notice names 16:00 ({r['notes']})")
    check(r['arrow'] and r['arrow']['level'] == 1 and r['arrow']['from'] == 31 * 1440 + 945, f"offer: the arrow, level 1 from 15:45 ({r['arrow']})")
    check(r['door'] and not r['shut'] and r['appt'] == ['16:00 marrow+calder'], f"offer: the door open till 18:00, the appointment with the Captain and Calder ({r})")
    r = g.ev("""(() => { setShipNow(31 * 1440 + 960); __to(1, 'R'); __tick(); occasionsTick(shipNow()); meetingsTick(shipNow()); const id = DIALOGUE && DIALOGUE.id; const L = __lines();
      if (L.choices) dialogueChoose(2); __run(0); return { id, lines: L.out, choices: L.choices, offer: SHIP.end.offer, said: __said.slice(), mail: __mail().filter(m => /^Captain/.test(m)), flags: { offer: flag('end.offer') }, walk: (CREW_SCENE.get('calder') || {}).mode, later: SIM_TIMERS.length, open: endOpen(), arrow: __guide('end:offer') }; })()""")
    print('   ', r['id'], r['choices'], r['offer'], r['said'], r['walk'])
    for l in r['lines']: print('      ', l)
    check(r['id'] == 'moment:ending.offer' and len(r['lines']) >= 5 and r['choices'] and len(r['choices']) == 3, f"offer: in the room at 16:00 the scene plays, three replies ({r['id']}, {r['choices']})")
    check(any('Concord headquarters' in l for l in r['lines']), f"offer: the letter is from Concord headquarters, through the Captain ({r['lines']})")
    check(any('headquarters' in m.lower() for m in r['mail']) and r['flags']['offer'] == 32, f"offer: the Captain's Mail as the record after it, flag end.offer ({r['mail']}, {r['flags']})")
    check(r['offer']['met'] and r['offer']['how'] == 'room' and r['open'] and r['arrow'] is None, f"offer: made in the room; the choice open; the arrow gone ({r['offer']}, {r['arrow']})")
    check(len([x for x in r['said'] if x.startswith('calder:')]) == 1 and r['later'] >= 2 and r['walk'] == 'follow', f"offer: Calder walks out with you, talking (her first line now, two more after) ({r['said']}, {r['walk']}, {r['later']})")
    r = g.ev("""(() => { __reset(32, 361); __tick(); __to(5, 'w'); setShipNow(31 * 1440 + 971); __tick(); const seek = !!SHIP.end.f.seek, mode1 = (CREW_SCENE.get('calder') || {}).mode, toasts = __toasts.slice();
      setShipNow(31 * 1440 + 1081); SHIP.end.f.led = shipNow(); __tick(); const id = DIALOGUE && DIALOGUE.id; __run(0);
      return { seek, mode1, toasts, id, offer: SHIP.end.offer }; })()""")
    print('    late:', r)
    check(r['seek'] and r['mode1'] == 'follow' and any('find you' in t[1] for t in r['toasts']), f"offer: not there at 16:10, Calder comes to find you ({r})")
    check(r['id'] == 'moment:ending.offer' and r['offer']['met'] and r['offer']['how'] == 'late', f"offer: after 18:00 it plays where you are when she reaches you ({r})")
    r = g.ev("""(() => { __reset(31, 1300); __tick(true); setShipNow(32 * 1440 + 300); __tick(true); return { offer: SHIP.end.offer, seek: !!SHIP.end.f.seek, booked: SHIP.occasions.filter(x => x.id === 'endingOffer').length }; })()""")
    print('    slept through:', r)
    check(r['offer'] and not r['offer']['met'] and r['seek'], f"offer: slept through, still owed: Calder comes to find you ({r})")

def made(g, day=32):
    g.ev(f"""(() => {{ __reset({day}, 361); __tick(); setShipNow(({day} - 1) * 1440 + 960); __to(1, 'R'); occasionsTick(shipNow()); meetingsTick(shipNow()); __run(0); __said.length = 0; __toasts.length = 0; __notes.length = 0; return SHIP.end.offer.met; }})()""")

def part_answers(g):
    print('(answers) Stay, Go, Not sure, changing your mind, the search, the address:')
    r = g.ev("""(() => { __reset(31, 600); __tick(); const p = __marrow(), pell = schedPeople().find(x => x.id === 'pell'); return { before: endChatButton(p), friend: endChatButton(pell) }; })()""")
    check(r['before'] is None, f"answers: no button before the offer ({r})")
    made(g)
    r = g.ev("""(() => { const p = __marrow(); setShipNow(31 * 1440 + 1000); __tick(); const btn = endChatButton(p), lvl = __guide('end:tell');
      endChatDo(p, 'tell'); const L = { choices: DEV.choose ? ['stay', 'go', 'unsure'] : null }; devChosen(0); const s1 = DIALOGUE && DIALOGUE.id; __run(0); const a = endSaid();
      setShipNow(32 * 1440 + 600); const s2 = __tell(1); const L2 = { out: [s2 || ''] }; const b = endSaid();
      setShipNow(33 * 1440 + 600); __tell(2); const c = endSaid(); __tick(); const lvlSat = __guide('end:tell');
      setShipNow(33 * 1440 + 1081); __tick(); const lvl18u = __guide('end:tell');
      __tell(0); __tick(); const lvlFirm = __guide('end:tell');
      return { btn, lvl, choices: L.choices, again: L2.out[0], a, b, c, lvlSat, lvl18u, lvlFirm, said: SHIP.end.said, settled: SHIP.end.settled, kept: endState().said.filter(x => x[1] === 'go').length }; })()""")
    print('   ', r)
    check(r['btn'] and r['btn']['label'] == 'About the transfer' and r['lvl'] and r['lvl']['level'] == 6, f"answers: \"About the transfer\" on the Captain; \"Tell the Captain\" at level 6 ({r['btn']}, {r['lvl']})")
    check(r['choices'] and len(r['choices']) == 3 and r['a'] == 'stay' and r['b'] == 'go' and r['c'] == 'unsure', f"answers: Stay, then Go, then Not sure ({r})")
    check(r['again'] == 'moment:endingTell.change.go', f"answers: changing your mind plays her endingTell.change scene ({r['again']})")
    check(r['lvlSat'] and r['lvlSat']['level'] == 6 and r['lvl18u'] and r['lvl18u']['level'] == 6, f"answers: Not sure keeps it open: no level 1 on Saturday ({r})")
    check(r['lvlFirm'] is None and r['settled'] is None, f"answers: told (Stay): the arrow goes; not settled before the address ({r})")
    r = g.ev("""(() => { setShipNow(34 * 1440 + 899); __tick(); const s1 = SHIP.end.settled; setShipNow(34 * 1440 + 900); __tick();
      return { s1, s2: SHIP.end.settled, flag: flag('end.stay'), btn: endChatButton(__marrow()), open: endOpen(), choice: endingChoice() }; })()""")
    print('    address:', r)
    check(r['s1'] is None and r['s2'] == {'day': 35, 'choice': 'stay'} and r['flag'] == 36 and r['btn'] is None and not r['open'] and r['choice'] == 'stay', f"answers: settled at the address, Sunday 15:00: end.stay, nothing open after ({r})")
    made(g)
    r = g.ev("""(() => { setShipNow(33 * 1440 + 1080); __tick(); const l18 = __guide('end:tell'); setShipNow(33 * 1440 + 1171); __tick(); const search = !!SHIP.end.f.search, mode = (CREW_SCENE.get('marrow') || {}).mode, notes = __notes.slice();
      return { l18, search, mode, notes }; })()""")
    print('    search:', r)
    check(r['l18'] and r['l18']['level'] == 1, f"answers: nothing said by Saturday 18:00: the arrow to her at level 1 ({r['l18']})")
    check(r['search'] and r['mode'] == 'follow' and any('find you' in n for n in r['notes']), f"answers: 19:30 with nothing said, she comes to find you ({r})")
    r = g.ev("""(() => { endSearchShow(); const id = DIALOGUE && DIALOGUE.id; const L = __lines(); dialogueChoose(1); const after = __lines().out; __run(0); return { id, choices: L.choices, after, said: endSaid() }; })()""")
    print('    search scene:', r['id'], r['said'], r['after'][:3])
    check(r['id'] == 'moment:endingSearch' and r['said'] == 'go' and len(r['after']) >= 3 and any('send-off' in x for x in r['after']), f"answers: her search, your answer, then her endingTell scene from its second line ({r})")
    made(g)
    r = g.ev("""(() => { const p = __marrow(); setShipNow(32 * 1440 + 600); __tell(2);
      setShipNow(34 * 1440 + 900); __tick(); const s1 = SHIP.end.settled, l = __guide('end:tell');
      const ask = endingAsk(); const L = { choices: DEV.choose ? ['stay', 'go'] : null }; devChosen(1); __run(0);
      return { s1, l, ask, choices: L.choices, settled: SHIP.end.settled, flag: flag('end.go') }; })()""")
    print('    not sure at the address:', r)
    check(r['s1'] is None and r['l'] and r['l']['level'] == 1, f"answers: Not sure at the address: not settled, the arrow to her at level 1 ({r})")
    check(r['ask'] and r['choices'] and len(r['choices']) == 2 and r['settled'] == {'day': 35, 'choice': 'go'} and r['flag'] == 35, f"answers: she asks, Stay or Go only; Go settles it ({r})")
    r = g.ev("""(() => { const keep = JSON.parse(JSON.stringify(SHIP.end)); const s = { ship: {}, player: {} }; for (const f of SAVE_EXTRA) try { f(s); } catch (e) { /* others' parts */ }
      const back = endClean(JSON.parse(JSON.stringify(s.ship.end))); return { same: JSON.stringify(back) === JSON.stringify(keep), saved: s.ship.end }; })()""")
    check(r['same'], f"answers: SHIP.end saved and read back the same ({r})")

def part_endpage(g):
    print('(endpage) the end page on paper; no kept copy with ?nosave:')
    made(g)
    r = g.ev("""(() => { const p = __marrow(); setShipNow(32 * 1440 + 600); __notes.length = 0; endChatDo(p, 'tell'); devChosen(1); const after = __lines().out.concat(__notes); __run(0);
      const keys = Object.keys(localStorage).filter(k => /before-end/.test(k)); SHIP.player.name = 'Ada'; SHIP.rel = SHIP.rel || {}; endPage(true);
      const el = document.getElementById('endPage'); const r = { keys, made: endKeepCopy(), shown: !el.hidden, text: el.innerText, btns: [...el.querySelectorAll('button')].map(b => b.dataset.end), role: el.getAttribute('role'), focus: document.activeElement && document.activeElement.dataset.end };
      r.after = after; endPage(false); return r; })()""")
    print('   ', {k: r[k] for k in ('keys', 'made', 'btns', 'role', 'focus', 'after')})
    check(any('ends this save' in x for x in r['after']), f"endpage: telling her Go says plainly it ends this save ({r['after']})"); print('   ', r['text'][:300].replace('\n', ' | '))
    check(r['keys'] == [] and r['made'] is False, f"endpage: no kept copy with ?nosave ({r['keys']})")
    check(r['shown'] and 'Ada' in r['text'] and 'Days aboard' in r['text'] and 'Zeke' in r['text'] and r['role'] == 'dialog', f"endpage: the rows ({r['text'][:200]})")
    check(r['btns'] == ['keep', 'new'] and r['focus'] == 'keep', f"endpage: with no kept copy, Keep this ending and Start a new game, the first focused ({r})")

def part_goodbye(pw, on):
    print('(goodbye) Monday, at phone size:')
    g = Game(pw, str(on), w=390, h=844); g.step(2); g.ev(SETUP)
    tick = "__tick()"
    r = g.ev("""(() => { SHIP.player.name = 'Ada'; SHIP.end = endClean({ offer: { day: 32, met: true }, said: [[33, 'go']], settled: { day: 35, choice: 'go' }, f: { asks: 1 } });
      setShipNow(35 * 1440 + 361); __tick(); const notes = __notes.slice(); setShipNow(35 * 1440 + 556); goToDeck(5); player.obj.position.copy(cellPos(9, 10)); __tick(); return notes; })()""")
    check(any('10:00' in n for n in r), f"goodbye: the 06:00 notice names 10:00 ({r})")
    g.step(120); g.ev(tick); g.step(30)
    r = g.ev("""(() => { const bay = DECK_CREW.filter(a => a.p && roomAt(...cellAt(a.x, a.z)) === 'S'), aisle = new Set(END_BAY.aisle.map(t => t.join(',')));
      const inAisle = bay.filter(a => { const c = cellAt(a.x, a.z); return aisle.has(c.join(',')) && !['torres-zeke'].includes(a.p.id); }).map(a => a.p.id);
      renderer.render(scene, camera); return { bay: bay.length, inAisle, calls: renderer.info.render.calls, goal: (goalNow() || {}).label, level: __guide('end:bye') && __guide('end:bye').level }; })()""")
    print('   ', r)
    check(r['bay'] >= 45 and r['level'] == 1 and r['goal'] == 'Say goodbye to Pell', f"goodbye: the bay full (about 60), the arrow at level 1 on the first farewell ({r})")
    check(r['calls'] < 450, f"goodbye: draw calls under 450 at phone size ({r['calls']})")
    check(len(r['inAisle']) <= 3, f"goodbye: the aisle stays clear (people passing through aside) ({r['inAisle']})")
    seen = []
    for k in range(12):
        who = g.ev("""(() => { const n = endByes().find(id => !SHIP.end.f['bye:' + id]); const who = n || (!SHIP.end.f.ramp ? 'torres-zeke' : null); if (!who) return null;
          const a = DECK_CREW.find(x => x.p && x.p.id === who); if (a) player.obj.position.set(a.x + .4, player.obj.position.y, a.z + .4); return who + '|' + ((goalNow() || {}).label || ''); })()""")
        if not who: break
        g.ev(tick); g.step(2)
        if g.ev("!!DIALOGUE"): seen.append('scene:' + g.ev("DIALOGUE.id")); g.ev("__run(0)")
        seen.append(who)
    print('   ', seen)
    said = g.ev("__said.slice()")
    check([x.split('|')[0] for x in seen if '|' in x][-4:] == ['calder', 'vance', 'marrow', 'torres-zeke'] and 'scene:moment:endingRamp' in seen, f"goodbye: friends, then the Chief, Vance, the Captain; Zeke's scene last ({seen})")
    check(any('the Captain' in x for x in seen) and len([x for x in said if x.split(':')[0] in ('calder', 'vance', 'marrow', 'pell')]) >= 4, f"goodbye: each says goodbye ({said})")
    g.ev("player.obj.position.copy(cellPos(5, 7))"); g.ev(tick); g.step(200)
    r = g.ev("""(() => { const el = document.getElementById('endPage'); return { aboard: !!SHIP.end.f.aboard, ended: !!SHIP.end.ended, page: !!el && !el.hidden, ramp: TERN.target }; })()""")
    print('   ', r)
    check(r['aboard'] and r['ended'] and r['page'] and r['ramp'] == 0, f"goodbye: aboard, the ramp closes, ended, the end page ({r})")
    if g.errors: fail('page errors (goodbye): ' + ' | '.join(g.errors[:5]))
    g.close()

PAD_INIT = r"""(() => { const B = Array(17).fill(0); window.__padB = B;
  Object.defineProperty(Navigator.prototype, 'getGamepads', { configurable: true, value: () => [{ id: 'Pretend pad (STANDARD GAMEPAD)', index: 0, connected: true, mapping: 'standard', timestamp: performance.now(),
    buttons: B.map(v => ({ pressed: !!v, touched: !!v, value: v })), axes: [0, 0, 0, 0] }, null, null, null] }); })()"""
def part_pad(pw, src):
    print('(pad) the end page by controller:')
    pc = WORK / 'test' / ('ending_pad_' + pathlib.Path(sys.argv[1]).name)
    pc.write_text(src.replace(SWITCH, "const EV_ENDING_ON = true;").replace("const PAD_ON = false;", "const PAD_ON = true;"))   # (0.96.0) PAD_ON is on in the game itself now: the PAD_ON replace finds nothing and the part runs on the build as shipped
    g = Game(pw, str(pc)); g.page.evaluate(PAD_INIT); g.step(2); g.ev(SETUP)
    press = lambda b: (g.page.evaluate(f'__padB[{b}] = 1'), g.step(3), g.page.evaluate(f'__padB[{b}] = 0'), g.step(3))
    g.ev("(() => { dispatchEvent(Object.assign(new Event('gamepadconnected'), { gamepad: navigator.getGamepads()[0] })); })()"); g.step(5)
    press(12); press(13)   # a first press: the pad's in use
    g.ev("(() => { SHIP.end = endClean({ offer: { day: 32, met: true }, said: [[33, 'go']], settled: { day: 35, choice: 'go' } }); endTheEnd(); })()"); g.step(5)
    f = lambda: g.ev("(() => { const e = document.activeElement; return e && e.dataset ? e.dataset.end || e.id || e.tagName : null; })()")
    a = f(); press(13); b = f(); press(1); c = f(); vis = g.ev("!document.getElementById('endPage').hidden")
    press(12); press(0); d = g.ev("(() => ({ hidden: document.getElementById('endPage').hidden, note: document.querySelector('#endPage .note') && document.querySelector('#endPage .note').textContent }))()")
    print('   ', a, b, c, vis, d)
    check(a == 'keep' and b == 'new' and c == 'new' and vis, f"pad: the highlight on Keep this ending, the D-pad to Start a new game, B does nothing ({a}, {b}, {c}, {vis})")
    check(not d['hidden'] and 'stays ended' in (d['note'] or ''), f"pad: A presses Keep this ending ({d})")
    if g.errors: fail('page errors (pad): ' + ' | '.join(g.errors[:5]))
    g.close(); pc.unlink()

def part_limits(g):
    print('(limits) the goodbye day is no shift; the fetches; the crowd limit; keepsakes:')
    r = g.ev("""(() => { __reset(36, 300); SHIP.end = endClean({ offer: { day: 32, met: true }, said: [[33, 'go']], settled: { day: 35, choice: 'go' }, f: { asks: 1 } });
      const c = careerInit(); const ms0 = c.ms; for (const t of [480, 600, 760, 900, 1100]) { setShipNow(35 * 1440 + t); careerTick(shipNow()); }
      const out = { off36: careerOff(36), off37: careerOff(37), shift: playerShiftOn(36), missed: c.ms - ms0, md: c.md };
      __to(4, Object.keys(ROOM_TILES)[0]); setShipNow(35 * 1440 + 511); __tick(); out.bf = __guide('end:bf'); out.bfSeek = !!SHIP.end.f.bfSeek; out.pell = (CREW_SCENE.get('pell') || {}).mode;
      setShipNow(35 * 1440 + 616); __tick(); out.byeSeek = !!SHIP.end.f.byeSeek; out.zeke = (CREW_SCENE.get('torres-zeke') || {}).mode;
      CREW_SCENE.clear(); END_PAGE.crowd = null; setShipNow(35 * 1440 + 721); __tick(); out.noon = CREW_SCENE.size; out.byes = endByes().length;
      CREW_SCENE.clear(); setShipNow(35 * 1440 + 1330); __tick(); out.night = CREW_SCENE.size;
      SHIP.traces = ['linePlaque', 'longTables', 'tilesTrophy', 'partyLounge']; out.kept = endKeepsakes(); return out; })()""")
    print('   ', r)
    check(r['off36'] and not r['off37'] and not r['shift'] and r['missed'] == 0, f"limits: Monday (Go) is no shift, nothing missed ({r})")
    check(r['bf'] and r['bf']['level'] == 1 and r['bfSeek'] and r['pell'] == 'follow', f"limits: breakfast's arrow level 1, Pell comes for you at 08:30 ({r})")
    check(r['byeSeek'] and r['zeke'] == 'follow', f"limits: 10:15 and not in the bay, Zeke comes for you ({r})")
    check(r['noon'] <= r['byes'] + 1 and r['night'] == 0, f"limits: from noon only the farewells and Zeke wait; nobody at night ({r})")
    check(r['kept'] == ['Your name on the Line plaque', 'Your Tiles trophy'], f"limits: keepsakes named, decor left out ({r['kept']})")

def part_week(g):
    print('(week) the friends, Zeke, the call home, the rows, the Record:')
    made(g)
    r = g.ev("""(() => { socInit(); setShipNow(32 * 1440 + 470); __tick(); const asks = (SHIP.social.seekAsks || []).filter(a => a.why === 'ending').map(a => a.id + ' ' + hhmm(a.from % 1440));
      const pell = SOC.crew[SOC.idx.get('pell')], btn = endFriendButton(pell); chatOpen(pell); chatDo('end:friend'); const said = DIALOGUE && DIALOGUE.id; __run(0); const after = endFriendButton(pell); if (CHAT) chatClose();
      const cap = endChatButton(__marrow()), str = SOC.crew.find(p => !END_FRIENDS.includes(p.id) && p.id !== 'marrow' && relTier(p.id) < 3), none = endChatButton(str);
      return { asks, btn, said, after, cap, none, rows: devDay(33).filter(x => x.kind === 'beat').map(x => hhmm(x.from) + ' ' + x.title) }; })()""")
    print('   ', r)
    check(len(r['asks']) >= 5 and r['asks'][0].startswith('pell 08:00') and len(set(a.split()[1] for a in r['asks'])) == len(r['asks']), f"week: Friday, the friends come one at a time ({r['asks']})")
    check(r['btn'] and r['btn']['label'] == 'About the transfer' and r['said'] == 'moment:endingFriend.pell' and r['after'] is None, f"week: Pell's \"About the transfer\", her own take, once ({r})")
    check(r['cap'] and r['none'] is None, f"week: the Captain's button stays; not on someone you barely know ({r['cap']}, {r['none']})")
    check(any('Zeke' in x for x in r['rows']) and any('by Saturday 20:00' in x for x in r['rows']), f"week: Friday's rows: your answer, Zeke ({r['rows']})")
    r = g.ev("""(() => { setShipNow(32 * 1440 + 1186); const p = schedPeople().find(x => x.id === 'torres-zeke'), w = whereIs(p, shipNow()); if (w && w.deck && deckDef.num !== w.deck) goToDeck(w.deck); deckCrewFill();
      __tick(); const arrow = __guide('end:zeke'); const a = DECK_CREW.find(x => x.p && x.p.id === 'torres-zeke'); if (a) player.obj.position.set(a.x + .5, player.obj.position.y, a.z);
      __said.length = 0; __tick(); const led = !!SHIP.end.f.zekeLed, said = __said.slice(); setShipNow(shipNow() + 21); if (a) player.obj.position.set(a.x + .5, player.obj.position.y, a.z); __tick();
      const id = DIALOGUE && DIALOGUE.id; __run(1); return { deck: w && w.deck, here: !!a, arrow, led, said, id, done: !!SHIP.end.f.zeke }; })()""")
    print('    Zeke:', r)
    check(r['arrow'] and r['arrow']['level'] == 1, f"week: after Friday's dinner, the arrow to Zeke, level 1 ({r['arrow']})")
    check(r['led'] and any(x.startswith('torres-zeke:') for x in r['said']) and r['id'] == 'moment:endingZekeFriday' and r['done'], f"week: Zeke finds you, walks you over, the talk ({r})")
    r = g.ev("""(() => { setShipNow(32 * 1440 + 1040); __tick(); const arrow = __guide('end:call'); const keep = ACT; ACT = { kind: 'call', phase: 'sit' }; __tick(); const id = DIALOGUE && DIALOGUE.id; __run(0); ACT = keep;
      const done = !!SHIP.end.f.call; ACT = { kind: 'call', phase: 'sit' }; __tick(); const again = DIALOGUE && DIALOGUE.id; ACT = keep; if (DIALOGUE) dialogueEnd(true);
      return { arrow, id, done, again, rec: endRecord().map(b => b.text || (b.rows || []).map(x => x.text).join(' / ')) }; })()""")
    print('    call:', r)
    check(r['arrow'] and r['arrow']['level'] == 2 and r['id'] == 'moment:ending.call' and r['done'] and not r['again'], f"week: the booths' arrow (level 2), your family's scene, once ({r})")
    check(any('offered you a transfer' in x for x in r['rec']), f"week: the Record has the offer ({r['rec']})")
    r = g.ev("""(() => { SHIP.end.settled = { day: 35, choice: 'go' }; setShipNow(34 * 1440 + 1250); __to(5, 'S'); __tick(); deckCrewFill(); const arrow = __guide('end:zekesun'), rows = devDay(35).filter(x => x.kind === 'beat').map(x => hhmm(x.from) + ' ' + x.title);
      const a = DECK_CREW.find(x => x.p && x.p.id === 'torres-zeke'); if (a) player.obj.position.set(a.x + .5, player.obj.position.y, a.z); __tick(); const id = DIALOGUE && DIALOGUE.id; __run(0);
      return { arrow, here: !!a, id, done: !!SHIP.end.f.zekeSun, rows }; })()""")
    print('    Zeke Sunday:', r)
    check(r['arrow'] and r['arrow']['level'] == 1 and r['id'] == 'moment:endingZekeSunday.go' and r['done'] and any('Zeke' in x for x in r['rows']), f"week: Sunday 21:00, Zeke in the shuttle bay, his scene for your choice ({r})")

ORIGIN = 'http://ending-check.test/'
def part_reload(b, on):
    print('(reload) a save between the offer and the answer:')
    ctx = b.new_context(viewport={'width': 390, 'height': 844})
    ctx.route(re.compile(r'^http://ending-check\.test/[^?#]*'), lambda r: r.fulfill(path=str(on), content_type='text/html'))
    pg = ctx.new_page(); errs = []
    pg.on('pageerror', lambda e: errs.append(f'pageerror: {e}'))
    pg.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
    pg.add_init_script(INIT)
    def ready():
        pg.wait_for_function('window.__sc !== undefined', timeout=90000)
        pg.evaluate("s => window.__sc(s)", "(() => { const rr = renderer.render.bind(renderer); renderer.render = () => {}; })()")
        pg.evaluate('window.__step(20, 33)')
        pg.evaluate('s => window.__sc(s)', SETUP)
    ev = lambda src: pg.evaluate('s => window.__sc(s)', src)
    pg.goto(ORIGIN + 'game.html', timeout=120000); ready()
    if pg.locator('text=Sign and go aboard').count():
        pg.fill('form input', 'Ada'); pg.click('text=Sign and go aboard'); pg.evaluate('window.__step(30, 33)')
    ev(SETUP)
    a = ev("""(() => { introSkip(); __reset(32, 361); __tick(); setShipNow(31 * 1440 + 960); __to(1, 'R'); occasionsTick(shipNow()); meetingsTick(shipNow()); __run(0);
      setShipNow(32 * 1440 + 600); __tell(1); updateClock(); saveGame(); return JSON.stringify(SHIP.end); })()""")
    pg.reload(timeout=120000); ready()
    r = ev("""(() => ({ end: JSON.stringify(SHIP.end), day: SHIP.time.day, script: !!MEETING_SCRIPTS['moment:ending.offer'], btn: endChatButton(schedPeople().find(p => p.id === 'marrow')), said: endSaid() }))()""")
    print('    before', a); print('    after ', r)
    A, R = json.loads(a), json.loads(r['end'])
    check(all(A[k] == R[k] for k in ('offer', 'said', 'settled')) and all(R['f'].get(k) == v for k, v in A['f'].items()) and r['day'] == 33 and r['said'] == 'go', f"reload: SHIP.end the same after a reload (the clock may add Friday's bookings) ({r})")
    check(r['script'] and r['btn'] and r['btn']['label'] == 'About the transfer', f"reload: the offer's scene and \"About the transfer\" still there ({r})")
    print('(keep) no way back (the user, 2026-10-26): no copy is ever written; the ended save:')
    st = lambda: pg.evaluate('() => Object.fromEntries(Object.keys(localStorage).map(k => [k, localStorage.getItem(k)]))')
    ev("""(() => { for (const k of [0, 1]) __tell(k); saveGame(); })()""")
    keys = [k for k in st() if 'before-end' in k]
    check(keys == [] and ev("endKeepCopy()") is False and ev("JSON.stringify(endKeptRows(1))") == '[]', f"keep: after Go, Stay, Go: no copy written, none in the Saves app ({keys})")
    ev("endTheEnd()")
    pg.reload(timeout=120000); ready()
    r = ev("""(() => { const el = document.getElementById('endPage'); return { shown: !!el && !el.hidden, btns: el ? [...el.querySelectorAll('button')].map(b => b.dataset.end) : [], focus: document.activeElement && document.activeElement.dataset.end, ended: !!SHIP.end.ended, keys: Object.keys(localStorage).filter(k => /before-end/.test(k)) }; })()""")
    print('    ended, reloaded:', r)
    check(r['shown'] and r['btns'] == ['keep', 'new'] and r['focus'] == 'keep' and r['ended'] and r['keys'] == [], f"keep: an ended save shows the end page again: Keep this ending, Start a new game ({r})")
    check(not errs, f'reload: page errors {errs[:3]}')
    ctx.close()

with sync_playwright() as pw:
    src = pathlib.Path(sys.argv[1]).read_text(); offpath = sys.argv[1]
    _on = re.compile(r"^const EV_ENDING_ON = true;.*$", re.M)
    if _on.search(src):   # (BM19) switched on in 0.94.0: the off parts on a copy with the off line put back; the on parts as before
        src = _on.sub(lambda m: SWITCH, src, count=1); offp = WORK / 'test' / ('ending_off_' + pathlib.Path(sys.argv[1]).name); offp.write_text(src); offpath = str(offp)
    if not ONLY or 'off' in ONLY:
        g = Game(pw, offpath)
        g.step(2)
        check(g.ev(SETUP), 'setup')
        try: part_off(g)
        except Exception as e: fail(f'off: {e}')
        check(g.ev(SETUP2), 'setup (EN2)')
        try: part_off_end(g)
        except Exception as e: fail(f'off (EN2): {e}')
        if g.errors: fail('page errors (off): ' + ' | '.join(g.errors[:5]))
        g.close()
    if SWITCH not in src: fail('the switch line is not in the build'); src = None
    if src and (not ONLY or ONLY - {'off'}):
        g = None
        on = WORK / 'test' / ('ending_on_' + pathlib.Path(sys.argv[1]).name)
        on.write_text(src.replace(SWITCH, "const EV_ENDING_ON = true;"))
        g = Game(pw, str(on))
        g.step(2)
        check(g.ev(SETUP), 'setup (on)'); check(g.ev(SETUP2), 'setup (on, EN2)')
        for name, fn in [('offer', part_offer), ('answers', part_answers), ('week', part_week), ('endpage', part_endpage), ('limits', part_limits), ('endgame', part_endgame), ('crossing', part_crossing)]:
            if ONLY and name not in ONLY: continue
            try: fn(g)
            except Exception as e: fail(f'{name}: {e}')
        if g.errors: fail('page errors (on): ' + ' | '.join(g.errors[:5]))
        g.close()
        if not ONLY or 'pad' in ONLY:
            try: part_pad(pw, src)
            except Exception as e: fail(f'pad: {e}')
        if not ONLY or 'goodbye' in ONLY:
            try: part_goodbye(pw, on)
            except Exception as e: fail(f'goodbye: {e}')
        if not ONLY or 'reload' in ONLY or 'keep' in ONLY:
            sv = WORK / 'test' / ('ending_save_' + pathlib.Path(sys.argv[1]).name); sv.write_text(instrument(src.replace(SWITCH, "const EV_ENDING_ON = true;")))
            b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
            try: part_reload(b, sv)
            except Exception as e: fail(f'reload: {e}')
            b.close(); sv.unlink()
        on.unlink()
print('ENDING CHECK OK' if ok else 'ENDING CHECK FAILED')
sys.exit(0 if ok else 1)
