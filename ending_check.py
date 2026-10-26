# Starship Cadet: the ending (lead 39; plans/ending-spec.html on claude/p5-specs, section 7), on paper in one page (the
# game's own functions at the times they'd run, no walking). Parts so far (EN2, E-4; EN1 adds offer, answers, goodbye
# and endpage, EN2 crossing for E-1):
#   off:      the build as it is (EV_ENDING_ON false): no endgame whatever the flag says, the endgame lines never hold,
#             no first morning, no Schedule rows, "What's next" and the calendar as before; no crossing back
#   endgame:  a copy with the switch on: the endgame lines never before end.stay nor before its day; every hour of the
#             first 14 days, about 4 hours in 10 after; endgame:false the other way round; no calendar row after the
#             crossing back once you've stayed (one planted on Day 40); "What's next" and the Works app's last page;
#             the first morning (booked on Day 36 at the Captain's breakfast, its Schedule row, the notice once, the
#             level 1 arrow to the mess, cleared when met); a New game clears it all
#   crossing: (E-1) the crossing back on paper, for each answer before the address (none, Go, Stay): the calendar's row on
#             Day 31 after the vessel, its phases at their minutes, the oath's meeting, the guard's rows; Vance comes to
#             you; the notices; the ship's arrow (2) and the oath's (1); the Veyli ship's poses; the oath with you as host;
#             the address (asked first when not answered) and the answer settled at it, Stay starting the endgame; the
#             record; the certificate's second date; the Line supper; nothing on the calendar after it
# Setup and environment as for cadet_test.py (CADET_WORK, CADET_CHROME).
# Run:  python3 ending_check.py BUILD.html [part ...]   Good is ENDING CHECK OK (exit 0); a failure exits 1.
import sys, pathlib, os, re
exec(open(__file__.replace('ending_check.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright

ok = True
def fail(msg):
    global ok
    ok = False
    print('  FAIL', msg)
def check(cond, msg):
    if not cond: fail(msg)
    return cond

ONLY = set(sys.argv[2:])
SRC = pathlib.Path(sys.argv[1]).read_text()
RUN_ID = f'p{os.getpid()}_'
__import__('atexit').register(lambda: [f.unlink(missing_ok=True) for f in (WORK / 'test').glob(f'ending_{RUN_ID}*') if f.is_file()])
SW = re.compile(r"^const EV_ENDING_ON = [^;]+;", re.M)
def variant(tag, on):
    if not SW.search(SRC): return None
    p = WORK / 'test' / f'ending_{RUN_ID}{tag}.html'
    p.write_text(SW.sub('const EV_ENDING_ON = ' + ('true' if on else 'false') + ';', SRC, count=1)); return str(p)

SETUP = r"""(() => {
  window.__toasts = []; toast = (a, b) => { window.__toasts.push([String(a), String(b || '')]); };
  window.__notes = []; deviceNotify = o => { window.__notes.push(String(o && o.text)); };
  window.__tick = (skip = false) => { for (const f of WORK_TICKS) try { f(shipNow(), skip); } catch (e) { console.error(e); } };
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

def part_off(g):
    print('(off) the build as it is:')
    r = g.ev("""(() => { const out = {}; out.sw = typeof EV_ENDING_ON === 'undefined' ? null : EV_ENDING_ON; SHIP.flags = SHIP.flags || {};
      const plan0 = JSON.stringify(evCalPlan()); __at(36, 300); const next0 = worksNext();
      flagSet('end.stay', 36); out.day = endgameDay(); out.on = endgameOn(); out.set = endStaySet(36);
      out.plan = JSON.stringify(evCalPlan()) === plan0; out.next = worksNext() === next0; out.occ = typeof OCCASIONS.endFirstMorning;
      out.items = endingItems(36).length; out.rows = devDay(36).filter(x => /Captain/.test(x.title)).length;
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
      out.first = first; out.later = later; out.postFalse = __egHold(40 * 1440, 'false');
      // a line said: lineFor gives an endgame greet on Day 36 to a crew member with no own greet line under it
      __at(36, 600); const who = ROSTER.find(p => p.id === 'holt');   // (Holt's own greet lines have no endgame one)
      out.say = who ? (lineFor(who, 'greet', { peek: true }) || {}).id : null; out.egIds = lines.lines.filter(x => x[0] === 'greet' && !x[2]).map(x => x[1].id);
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
    print('   ', {k: r[k] for k in r if k not in ('egIds',)})
    check(r['n'] > 0, f"endgame: there are endgame lines in the build ({r['n']})")
    check(r['pre'] == 0 and r['preFalse'][0] == r['preFalse'][1], f"endgame: no endgame line holds before the flag, every endgame:false one does ({r['pre']}, {r['preFalse']})")
    check(r['set'] and r['day'] == 36 and not r['on35'] and r['d35'] == 0, f"endgame: endStaySet gives Day 36 at the earliest; not on Day 35 ({r})")
    check(r['first'][1] > 0 and r['first'][0] == r['first'][1], f"endgame: every hour of the first 14 days ({r['first']})")
    fr = r['later'][0] / max(1, r['later'][1])
    check(.25 <= fr <= .55, f"endgame: about 4 hours in 10 after the first 14 days ({r['later']}, {fr:.2f})")
    check(r['postFalse'][0] == 0, f"endgame: endgame:false lines never hold after ({r['postFalse']})")
    check(r['say'] in r['egIds'], f"endgame: lineFor picks an endgame greet on Day 36 ({r['say']} not in {r['egIds']})")
    check(r['planOff'] and not r['planOn'] and not r['cross'], f"endgame: a calendar row after Day 35 is planned before you stay, never after; the crossing back itself never closed ({r})")
    check('home' not in r['next35'].lower() and 'The Wren is home' in r['next36'] and not r['tab35'] and r['tab36'], f"endgame: What's next and the last page from Day 36 ({r['next35']} | {r['next36']}, tab {r['tab35']} {r['tab36']})")
    check('The Wren is home' in r['page'], f"endgame: the last page's words ({r['page']})")

    print('(endgame) the first morning:')
    r = g.ev("""(() => { const out = {}; __at(36, 240); __notes.length = 0; GUIDE.list.length = 0; SHIP.occasions = SHIP.occasions.filter(x => x.id !== 'endFirstMorning');
      occasionsTick(shipNow(), true); const rec = SHIP.occasions.find(x => x.id === 'endFirstMorning');
      out.booked = rec ? hhmm(rec.at % 1440) + ' ' + rec.len + ' ' + rec.deck + rec.room : null; out.script = !!MEETING_SCRIPTS.endFirstMorning;
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

CROSS = r"""((ans) => { const out = { notes: [], arrows: [] }; SHIP.flags = SHIP.flags || {}; for (const k of ['end.stay', 'end.cb.stay', 'end.cb.go']) flagSet(k, null);
  SHIP.end = ans ? { said: [[33, ans]] } : undefined; if (!ans) delete SHIP.end;
  // the calendar: the events before it logged as run, nothing running
  const plan = evCalPlan(); out.row = plan.find(r => r.id === 'crossingBack') || null;
  SHIP.event = null; SHIP.eventLog.length = 0; for (const r of plan) if (r.id !== 'crossingBack') SHIP.eventLog.push({ id: r.id, startDay: r.day, endDay: r.day + SHIP_EVENTS[r.id].days, band: 'smooth' });
  out.due = eventDueDay(); __at(31, 1); eventAdvance(shipNow(), true); out.started = SHIP.event ? SHIP.event.id + '@' + SHIP.event.startDay : null;
  const ph = []; for (const [d, m] of [[31, 479], [31, 480], [35, 869], [35, 870], [35, 914], [35, 915], [35, 1154], [35, 1155], [35, 1439]]) { const n = eventNow((d - 1) * 1440 + m); ph.push(d + ' ' + hhmm(m) + ' ' + (n ? n.id + '.' + n.phase : '-')); }
  out.phases = ph; const mt = MEETINGS.find(x => x.id === 'crossingBackOath'); out.meet = mt ? [Math.floor(mt.at / 1440) + 1, hhmm(mt.at % 1440), mt.len, mt.script] : null;
  out.beats = EV_BEATS.filter(b => b.id === 'crossingBack' || b.id === 'endingOffer').map(b => b.id + ' ' + b.kind + ' ' + b.day + ' ' + b.at.join('-'));
  out.status31 = eventStatus((30) * 1440 + 600);
  const M = SHIP.event.mine, T = m => { setShipNow(m); crossingBackTick(m); }, d = (day, m) => (day - 1) * 1440 + m;
  __notes.length = 0; GUIDE.list.length = 0; CREW_SCENE.clear();
  // Wednesday: Vance sets off to find you (a crewScene), the notice he's coming; his word ends with the record notice
  T(d(31, 509)); out.vanceEarly = CREW_SCENE.has('vance'); T(d(31, 510)); out.vance = CREW_SCENE.has('vance') ? CREW_SCENE.get('vance').mode : null;
  out.vanceFor = !!MEETING_SCRIPTS.crossingBackVance && crossingBackMoment('crossingBackVance', ['vance'], ['story:vance', 1]);
  while (DIALOGUE) { const v = dialogueView(); if (!v) break; dialogueStep(v.choices ? 0 : undefined); }
  T(d(31, 520)); out.vanceDone = [M['story:vance'], CREW_SCENE.has('vance')]; out.notes.push(...__notes.splice(0));
  // Saturday 10:00: the ship, its arrow (level 2); the sky ship's poses
  T(d(34, 599)); T(d(34, 600)); const sh = GUIDE.list.find(x => x.id === 'end:cb:ship'); out.shipArrow = sh ? [sh.level, sh.goal().room] : null; out.notes.push(...__notes.splice(0));
  out.sky = [[34, 599], [34, 600], [35, 869], [35, 870], [35, 893], [35, 899], [35, 900]].map(([dd, m]) => { const x = crossingBackShip(d(dd, m)); return x ? x.pose + (x.flash ? '*' : '') : '-'; });
  // Sunday: the morning notice, the oath's arrow from 14:00 (level 1), the horn
  T(d(35, 400)); T(d(35, 840)); const oa = GUIDE.list.find(x => x.id === 'end:cb:oath'); out.oathArrow = oa ? [oa.level, oa.goal().deck, oa.goal().room, hhmm(oa.until % 1440)] : null;
  T(d(35, 870)); out.notes.push(...__notes.splice(0)); out.cert0 = crossingBackDone();
  // the oath, met in the lounge; then the address by the answer (or the Captain asks), settled
  goToDeck(3); player.obj.position.copy(cellPos(...ROOM_TILES['L'][Math.floor(ROOM_TILES['L'].length / 2)]));
  setShipNow(d(35, 880)); meetingsTick(shipNow()); out.oathShown = DIALOGUE ? DIALOGUE.id : null; const lines = [];
  while (DIALOGUE) { const v = dialogueView(); if (!v) break; lines.push(v.who + ': ' + (v.text || v.choices.join(' / '))); dialogueStep(v.choices ? 0 : undefined); }
  out.oathLines = lines.length; out.oathYou = lines.filter(l => l.startsWith((SHIP.player && SHIP.player.name) || 'Cadet')).length;
  const addr = []; for (let i = 0; i < 3 && !M['story:address']; i++) { T(d(35, 900 + i)); const id = DIALOGUE ? DIALOGUE.id : null; if (id) addr.push(id);
    while (DIALOGUE) { const v = dialogueView(); if (!v) break; dialogueStep(v.choices ? 0 : undefined); } }
  out.address = addr; out.settled = M['settled'] || null; out.stay = endgameDay();
  T(d(35, 915)); out.record = ADDRESSES.length ? ADDRESSES[ADDRESSES.length - 1].text : null; out.cert = crossingBackDone();
  out.keep = (evWord('event.crossingBack.keepsake') || '').slice(0, 40);
  out.supper = (EV_DAY_DRESS.get('sunday-table@35') || {}).o ? EV_DAY_DRESS.get('sunday-table@35').o.name : null;
  // the event's end: logged, and nothing after it on the calendar
  __at(36, 1); eventAdvance(shipNow(), true); out.logged = SHIP.eventLog.some(l => l.id === 'crossingBack'); out.next = eventDueDay();
  goToDeck(4); return out; })"""

def part_crossing(g):
    for ans, want in [(None, 'stay'), ('go', 'go'), ('stay', 'stay')]:
        print(f'(crossing) the answer before the address: {ans}')
        r = g.ev(CROSS + f"({repr(ans) if ans else 'null'})".replace("'", "'"))
        print('   ', {k: r[k] for k in r if k not in ('notes',)})
        print('    notes:', r['notes'])
        check(r['row'] and r['row']['day'] == 31 and r['due'] and r['due']['id'] == 'crossingBack' and r['started'] == 'crossingBack@31', f"crossing: the calendar's row on Day 31, due and started ({r['row']}, {r['due']}, {r['started']})")
        check(r['phases'] == ['31 07:59 -', '31 08:00 crossingBack.warning', '35 14:29 crossingBack.warning', '35 14:30 crossingBack.onset', '35 15:14 crossingBack.onset', '35 15:15 crossingBack.resolution', '35 19:14 crossingBack.resolution', '35 19:15 crossingBack.afterglow', '35 23:59 crossingBack.afterglow'], f"crossing: the phases at their minutes ({r['phases']})")
        check(r['meet'] == [35, '14:40', 35, 'crossingBackOath'], f"crossing: the oath's meeting Sunday 14:40 ({r['meet']})")
        check(len(r['beats']) == 2 and r['status31'] and 'Sunday' in r['status31'], f"crossing: the guard's rows and the status line ({r['beats']}, {r['status31']})")
        check(not r['vanceEarly'] and r['vance'] == 'follow' and r['vanceFor'] and r['vanceDone'] == [1, False], f"crossing: Vance comes to you from 08:30 and his word ends it ({r['vance']}, {r['vanceDone']})")
        n = ' | '.join(r['notes'])
        check('coming to find you' in n and 'You lead the oath' in n and 'off the bow' in n and 'Today at 14:30' in n and 'horn' in n.lower(), f"crossing: the notices, Vance, the ship, the morning, the horn ({r['notes']})")
        check(r['shipArrow'] == [2, 'L'] and r['oathArrow'] and r['oathArrow'][:3] == [1, 3, 'L'], f"crossing: the ship's arrow level 2, the oath's level 1 to the bow lounge ({r['shipArrow']}, {r['oathArrow']})")
        check(r['sky'] == ['-', 'bow', 'bow', 'alongside', 'alongside*', 'alongside', '-'], f"crossing: the Veyli ship off the bow from Saturday 10:00, alongside from the horn, the flashes, gone at 15:00 ({r['sky']})")
        check(r['oathShown'] == 'crossingBackOath' and r['oathYou'] >= 4, f"crossing: the oath played with you as host ({r['oathShown']}, {r['oathYou']} of {r['oathLines']} lines yours)")
        exp = (['moment:crossingBackAddress.ask'] if not ans else []) + ['moment:crossingBackAddress.' + want]
        check(r['address'] == exp and r['settled'] == want, f"crossing: the address {exp} and settled {want} ({r['address']}, {r['settled']})")
        check((r['stay'] == 36) == (want == 'stay'), f"crossing: Stay starts the endgame on Day 36, Go doesn't ({r['stay']})")
        check(r['record'] and ('keeping them' in r['record'] if want == 'stay' else 'Concord' in r['record']), f"crossing: the address's record names your choice ({r['record']})")
        check(not r['cert0'] and r['cert'] and r['keep'], f"crossing: the certificate's second date from 15:15 ({r['cert0']}, {r['cert']})")
        check(r['supper'] == 'The Line supper' and r['logged'] and r['next'] is None, f"crossing: the Line supper, logged at its end, nothing after ({r['supper']}, {r['logged']}, {r['next']})")

with sync_playwright() as pw:
    parts = [('off', part_off, sys.argv[1]), ('endgame', part_endgame, None), ('crossing', part_crossing, None)]
    pages = {}
    for name, fn, build in parts:
        if ONLY and name not in ONLY: continue
        key = 'off' if build else 'on'
        if key not in pages:
            path = build if build else variant('on', True)
            if not path: fail('no EV_ENDING_ON line in the build'); continue
            g = Game(pw, path); g.step(2); check(g.ev(SETUP), 'setup'); pages[key] = g
        try: fn(pages[key])
        except Exception as e: fail(f'{name}: {e}')
    for g in pages.values():
        if g.errors: fail('page errors: ' + ' | '.join(g.errors[:5]))
        g.close()
print('ENDING CHECK OK' if ok else 'ENDING CHECK FAILED')
sys.exit(0 if ok else 1)
