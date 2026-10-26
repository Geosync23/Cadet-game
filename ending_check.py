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
#   week:    Friday: the friends come to you one at a time (seek asks), each with "About the transfer" and their own take;
#            Zeke after dinner (arrow level 1 "Talk to Zeke", he finds you, the scene); a call home plays your family's
#            scene once; the Schedule's rows (your answer by Saturday 20:00, Zeke); the Record's lines
# Setup and environment as for cadet_test.py (CADET_WORK, CADET_CHROME).
# Run:  python3 ending_check.py BUILD.html [part ...]   Good is ENDING CHECK OK (exit 0); a failure exits 1.
import sys, pathlib, json
exec(open(__file__.replace('ending_check.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright

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
  window.__lines = () => { const out = []; let n = 0; while (DIALOGUE && n++ < 40) { const v = dialogueView(); if (!v) break; if (v.choices) return { out, choices: v.choices }; out.push(v.name + ': ' + v.text); dialogueNext(); } return { out, choices: null }; };
  return true;
})()"""

def part_off(g):
    print('(off) the build as given:')
    r = g.ev("""(() => { __reset(32, 360); __tick(); setShipNow(31 * 1440 + 950); __tick();
      const p = __marrow(); const save = {}; try { SAVE_EXTRA.forEach(f => f({ ship: {}, player: {} })); } catch (e) { /* */ }
      return { on: EV_ENDING_ON, end: typeof SHIP.end, occ: typeof OCCASIONS.endingOffer, booked: SHIP.occasions.length, btn: typeof endChatButton === 'function' ? endChatButton(p) : 'none',
        guide: GUIDE.list.filter(e => /^end:/.test(e.id)).length, scripts: Object.keys(MEETING_SCRIPTS).filter(k => /ending/.test(k)) }; })()""")
    print('   ', r)
    check(r['on'] is False and r['end'] == 'undefined' and r['occ'] == 'undefined' and r['booked'] == 0, f"off: no SHIP.end, no ending occasion, nothing booked ({r})")
    check(r['btn'] is None and r['guide'] == 0 and not r['scripts'], f"off: no button, no arrows, no scripts ({r})")

def part_offer(g):
    print('(offer) the day, the booking, the room, Calder:')
    r = g.ev("""(() => { const out = {}; __reset(20, 600);
      out.plain = endOfferDay(); window.P5_STEP6 = true; SHIP.works = SHIP.works || worksInit();
      delete SHIP.works.end; out.none = endOfferDay(); SHIP.works.end = { answer: 'teach the new cadets', day: 26 }; out.steady = endOfferDay(); out.post = endPostKind();
      SHIP.works.end = { answer: 'engines', day: 33 }; out.slow = endOfferDay(); out.week = endWeek(); delete window.P5_STEP6; delete SHIP.works.end; out.back = endOfferDay(); return out; })()""")
    print('   ', r)
    check(r['plain'] == 32 and r['none'] is None and r['steady'] == 32 and r['slow'] == 39 and r['back'] == 32, f"offer: Day 32 (Step 6 off), none before Calder's question, Day 32 after Day 26, Day 39 after Day 33 ({r})")
    check(r['post'] == 'teaching' and r['week'] == {'offer': 39, 'due': 41, 'settle': 42, 'leave': 43}, f"offer: the post by your answer, the slower week ({r})")
    r = g.ev("""(() => { __reset(32, 359); __tick(); const before = !!(SHIP.end && SHIP.end.offer); setShipNow(31 * 1440 + 361); __tick();
      const o = SHIP.occasions.find(x => x.id === 'endingOffer'); setShipNow(31 * 1440 + 946); __tick();
      return { before, offer: SHIP.end.offer, occ: o && [hhmm(o.at % 1440), o.len, o.deck, o.room], notes: __notes.slice(), mail: __mail(), arrow: __guide('end:offer'),
        door: occasionDoorOpen(1, 'R', 31 * 1440 + 1070), shut: occasionDoorOpen(1, 'R', 31 * 1440 + 1090), appt: (SHIP.device.appts || []).filter(a => a.occ && /endingOffer/.test(a.occ)).map(a => hhmm(a.at % 1440) + ' ' + a.with.join('+')) }; })()""")
    print('   ', r)
    check(not r['before'] and r['offer'] and r['offer']['day'] == 32 and r['occ'] == ['16:00', 120, 1, 'R'], f"offer: booked at 06:00 on Day 32: 16:00 in the ready room, open till 18:00 ({r})")
    check(any('16:00' in n for n in r['notes']) and any('Vance' in m and '16:00' in m for m in r['mail']), f"offer: the morning notice and Vance's Mail name 16:00 ({r['notes']}, {r['mail']})")
    check(r['arrow'] and r['arrow']['level'] == 1 and r['arrow']['from'] == 31 * 1440 + 945, f"offer: the arrow, level 1 from 15:45 ({r['arrow']})")
    check(r['door'] and not r['shut'] and r['appt'] == ['16:00 marrow+calder'], f"offer: the door open till 18:00, the appointment with the Captain and Calder ({r})")
    r = g.ev("""(() => { setShipNow(31 * 1440 + 960); __to(1, 'R'); __tick(); occasionsTick(shipNow()); meetingsTick(shipNow()); const id = DIALOGUE && DIALOGUE.id; const L = __lines();
      if (L.choices) dialogueChoose(2); __run(0); return { id, lines: L.out, choices: L.choices, offer: SHIP.end.offer, said: __said.slice(), walk: (CREW_SCENE.get('calder') || {}).mode, later: SIM_TIMERS.length, open: endOpen(), arrow: __guide('end:offer') }; })()""")
    print('   ', r['id'], r['choices'], r['offer'], r['said'], r['walk'])
    for l in r['lines']: print('      ', l)
    check(r['id'] == 'moment:ending.offer' and len(r['lines']) >= 5 and r['choices'] and len(r['choices']) == 3, f"offer: in the room at 16:00 the scene plays, three replies ({r['id']}, {r['choices']})")
    check(any('Concord headquarters' in l for l in r['lines']), f"offer: the letter is from Concord headquarters, through the Captain ({r['lines']})")
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
      endChatDo(p, 'tell'); const L = __lines(); dialogueChoose(0); __run(0); const a = endSaid();
      setShipNow(32 * 1440 + 600); endChatDo(p, 'tell'); const L2 = __lines(); dialogueChoose(1); __run(0); const b = endSaid();
      setShipNow(33 * 1440 + 600); endChatDo(p, 'tell'); __lines(); dialogueChoose(2); __run(0); const c = endSaid(); __tick(); const lvlSat = __guide('end:tell');
      setShipNow(33 * 1440 + 1081); __tick(); const lvl18u = __guide('end:tell');
      endChatDo(p, 'tell'); __lines(); dialogueChoose(0); __run(0); __tick(); const lvlFirm = __guide('end:tell');
      return { btn, lvl, choices: L.choices, again: L2.out[0], a, b, c, lvlSat, lvl18u, lvlFirm, said: SHIP.end.said, settled: SHIP.end.settled, kept: endState().said.filter(x => x[1] === 'go').length }; })()""")
    print('   ', r)
    check(r['btn'] and r['btn']['label'] == 'About the transfer' and r['lvl'] and r['lvl']['level'] == 6, f"answers: \"About the transfer\" on the Captain; \"Tell the Captain\" at level 6 ({r['btn']}, {r['lvl']})")
    check(r['choices'] and len(r['choices']) == 3 and r['a'] == 'stay' and r['b'] == 'go' and r['c'] == 'unsure', f"answers: Stay, then Go, then Not sure ({r})")
    check('mind' in (r['again'] or ''), f"answers: she knows you're changing your mind ({r['again']})")
    check(r['lvlSat'] and r['lvlSat']['level'] == 6 and r['lvl18u'] and r['lvl18u']['level'] == 6, f"answers: Not sure keeps it open: no level 1 on Saturday ({r})")
    check(r['lvlFirm'] is None and r['settled'] is None, f"answers: told (Stay): the arrow goes; not settled before the address ({r})")
    r = g.ev("""(() => { setShipNow(34 * 1440 + 899); __tick(); const s1 = SHIP.end.settled; setShipNow(34 * 1440 + 900); __tick();
      return { s1, s2: SHIP.end.settled, flag: flag('end.stay'), btn: endChatButton(__marrow()), open: endOpen(), choice: endingChoice() }; })()""")
    print('    address:', r)
    check(r['s1'] is None and r['s2'] == {'day': 35, 'choice': 'stay'} and r['flag'] == 35 and r['btn'] is None and not r['open'] and r['choice'] == 'stay', f"answers: settled at the address, Sunday 15:00: end.stay, nothing open after ({r})")
    made(g)
    r = g.ev("""(() => { setShipNow(33 * 1440 + 1080); __tick(); const l18 = __guide('end:tell'); setShipNow(33 * 1440 + 1171); __tick(); const search = !!SHIP.end.f.search, mode = (CREW_SCENE.get('marrow') || {}).mode, notes = __notes.slice();
      return { l18, search, mode, notes }; })()""")
    print('    search:', r)
    check(r['l18'] and r['l18']['level'] == 1, f"answers: nothing said by Saturday 18:00: the arrow to her at level 1 ({r['l18']})")
    check(r['search'] and r['mode'] == 'follow' and any('find you' in n for n in r['notes']), f"answers: 19:30 with nothing said, she comes to find you ({r})")
    made(g)
    r = g.ev("""(() => { const p = __marrow(); setShipNow(32 * 1440 + 600); endChatDo(p, 'tell'); __lines(); dialogueChoose(2); __run(0);
      setShipNow(34 * 1440 + 900); __tick(); const s1 = SHIP.end.settled, l = __guide('end:tell');
      const ask = endingAsk(); const L = __lines(); dialogueChoose(1); __run(0);
      return { s1, l, ask, choices: L.choices, settled: SHIP.end.settled, flag: flag('end.go') }; })()""")
    print('    not sure at the address:', r)
    check(r['s1'] is None and r['l'] and r['l']['level'] == 1, f"answers: Not sure at the address: not settled, the arrow to her at level 1 ({r})")
    check(r['ask'] and r['choices'] and len(r['choices']) == 2 and r['settled'] == {'day': 35, 'choice': 'go'} and r['flag'] == 35, f"answers: she asks, Stay or Go only; Go settles it ({r})")
    r = g.ev("""(() => { const keep = JSON.parse(JSON.stringify(SHIP.end)); const s = { ship: {}, player: {} }; for (const f of SAVE_EXTRA) try { f(s); } catch (e) { /* others' parts */ }
      const back = endClean(JSON.parse(JSON.stringify(s.ship.end))); return { same: JSON.stringify(back) === JSON.stringify(keep), saved: s.ship.end }; })()""")
    check(r['same'], f"answers: SHIP.end saved and read back the same ({r})")

def part_week(g):
    print('(week) the friends, Zeke, the call home, the rows, the Record:')
    made(g)
    r = g.ev("""(() => { socInit(); setShipNow(32 * 1440 + 470); __tick(); const asks = (SHIP.social.seekAsks || []).filter(a => a.why === 'ending').map(a => a.id + ' ' + hhmm(a.from % 1440));
      const pell = SOC.crew[SOC.idx.get('pell')], btn = endFriendButton(pell); chatOpen(pell); chatDo('end:friend'); const said = CHAT && CHAT.line && CHAT.line.text; const after = endFriendButton(pell); chatClose();
      const cap = endChatButton(__marrow()), str = SOC.crew.find(p => !END_FRIENDS.includes(p.id) && p.id !== 'marrow' && relTier(p.id) < 3), none = endChatButton(str);
      return { asks, btn, said, after, cap, none, rows: devDay(33).filter(x => x.kind === 'beat').map(x => hhmm(x.from) + ' ' + x.title) }; })()""")
    print('   ', r)
    check(len(r['asks']) >= 5 and r['asks'][0].startswith('pell 08:00') and len(set(a.split()[1] for a in r['asks'])) == len(r['asks']), f"week: Friday, the friends come one at a time ({r['asks']})")
    check(r['btn'] and r['btn']['label'] == 'About the transfer' and r['said'] and "can't go" in r['said'] and r['after'] is None, f"week: Pell's \"About the transfer\", her own take, once ({r})")
    check(r['cap'] and r['none'] is None, f"week: the Captain's button stays; not on someone you barely know ({r['cap']}, {r['none']})")
    check(any('Zeke' in x for x in r['rows']) and any('by Saturday 20:00' in x for x in r['rows']), f"week: Friday's rows: your answer, Zeke ({r['rows']})")
    r = g.ev("""(() => { setShipNow(32 * 1440 + 1186); const p = schedPeople().find(x => x.id === 'torres-zeke'), w = whereIs(p, shipNow()); if (w && w.deck && deckDef.num !== w.deck) goToDeck(w.deck); deckCrewFill();
      __tick(); const arrow = __guide('end:zeke'); const a = DECK_CREW.find(x => x.p && x.p.id === 'torres-zeke'); if (a) player.obj.position.set(a.x + .5, player.obj.position.y, a.z);
      __said.length = 0; __tick(); const led = !!SHIP.end.f.zekeLed, said = __said.slice(); setShipNow(shipNow() + 21); if (a) player.obj.position.set(a.x + .5, player.obj.position.y, a.z); __tick();
      const id = DIALOGUE && DIALOGUE.id; __run(1); return { deck: w && w.deck, here: !!a, arrow, led, said, id, done: !!SHIP.end.f.zeke }; })()""")
    print('    Zeke:', r)
    check(r['arrow'] and r['arrow']['level'] == 1, f"week: after Friday's dinner, the arrow to Zeke, level 1 ({r['arrow']})")
    check(r['led'] and any(x.startswith('torres-zeke:') for x in r['said']) and r['id'] == 'moment:ending.zeke' and r['done'], f"week: Zeke finds you, walks you over, the talk ({r})")
    r = g.ev("""(() => { setShipNow(32 * 1440 + 1040); __tick(); const arrow = __guide('end:call'); const keep = ACT; ACT = { kind: 'call', phase: 'sit' }; __tick(); const id = DIALOGUE && DIALOGUE.id; __run(0); ACT = keep;
      const done = !!SHIP.end.f.call; ACT = { kind: 'call', phase: 'sit' }; __tick(); const again = DIALOGUE && DIALOGUE.id; ACT = keep; if (DIALOGUE) dialogueEnd(true);
      return { arrow, id, done, again, rec: endRecord().map(b => b.text || (b.rows || []).map(x => x.text).join(' / ')) }; })()""")
    print('    call:', r)
    check(r['arrow'] and r['arrow']['level'] == 2 and r['id'] == 'moment:ending.call' and r['done'] and not r['again'], f"week: the booths' arrow (level 2), your family's scene, once ({r})")
    check(any('offered you a transfer' in x for x in r['rec']), f"week: the Record has the offer ({r['rec']})")

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
    ev = lambda src: pg.evaluate('s => window.__sc(s)', src)
    pg.goto(ORIGIN + 'game.html', timeout=120000); ready()
    if pg.locator('text=Sign and go aboard').count():
        pg.fill('form input', 'Ada'); pg.click('text=Sign and go aboard'); pg.evaluate('window.__step(30, 33)')
    ev(SETUP)
    a = ev("""(() => { introSkip(); __reset(32, 361); __tick(); setShipNow(31 * 1440 + 960); __to(1, 'R'); occasionsTick(shipNow()); meetingsTick(shipNow()); __run(0);
      setShipNow(32 * 1440 + 600); endChatDo(__marrow(), 'tell'); __lines(); dialogueChoose(1); __run(0); updateClock(); saveGame(); return JSON.stringify(SHIP.end); })()""")
    pg.reload(timeout=120000); ready()
    r = ev("""(() => ({ end: JSON.stringify(SHIP.end), day: SHIP.time.day, script: !!MEETING_SCRIPTS['moment:ending.offer'], btn: endChatButton(schedPeople().find(p => p.id === 'marrow')), said: endSaid() }))()""")
    print('    before', a); print('    after ', r)
    A, R = json.loads(a), json.loads(r['end'])
    check(all(A[k] == R[k] for k in ('offer', 'said', 'settled')) and all(R['f'].get(k) == v for k, v in A['f'].items()) and r['day'] == 33 and r['said'] == 'go', f"reload: SHIP.end the same after a reload (the clock may add Friday's bookings) ({r})")
    check(r['script'] and r['btn'] and r['btn']['label'] == 'About the transfer', f"reload: the offer's scene and \"About the transfer\" still there ({r})")
    check(not errs, f'reload: page errors {errs[:3]}')
    ctx.close()

with sync_playwright() as pw:
    src = pathlib.Path(sys.argv[1]).read_text()
    if not ONLY or 'off' in ONLY:
        g = Game(pw, sys.argv[1])
        g.step(2)
        check(g.ev(SETUP), 'setup')
        try: part_off(g)
        except Exception as e: fail(f'off: {e}')
        if g.errors: fail('page errors (off): ' + ' | '.join(g.errors[:5]))
        g.close()
    if SWITCH not in src: fail('the switch line is not in the build'); src = None
    if src and (not ONLY or ONLY - {'off'}):
        g = None
        on = WORK / 'test' / ('ending_on_' + pathlib.Path(sys.argv[1]).name)
        on.write_text(src.replace(SWITCH, "const EV_ENDING_ON = true;"))
        g = Game(pw, str(on))
        g.step(2)
        check(g.ev(SETUP), 'setup (on)')
        for name, fn in [('offer', part_offer), ('answers', part_answers), ('week', part_week)]:
            if ONLY and name not in ONLY: continue
            try: fn(g)
            except Exception as e: fail(f'{name}: {e}')
        if g.errors: fail('page errors (on): ' + ' | '.join(g.errors[:5]))
        g.close()
        if not ONLY or 'reload' in ONLY:
            sv = WORK / 'test' / ('ending_save_' + pathlib.Path(sys.argv[1]).name); sv.write_text(instrument(src.replace(SWITCH, "const EV_ENDING_ON = true;")))
            b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
            try: part_reload(b, sv)
            except Exception as e: fail(f'reload: {e}')
            b.close(); sv.unlink()
        on.unlink()
print('ENDING CHECK OK' if ok else 'ENDING CHECK FAILED')
sys.exit(0 if ok else 1)
