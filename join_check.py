# Starship Cadet: tap-to-join check (playtest 1, the traditions engineer, 0.70.x; keep in the repo next to events_check.py)
# Checks section 18's tap to join (TRAD_JOIN) in a test game (?nosave&debug), each part on its deck:
#   every joinable tradition: being there doesn't join it; a tap on its leader joins you (eventJoin: social, the notice)
#   and starts its activity at one of its spots (or a walk); the leader's marker, the arrow at the leader and its tip while
#   it's on, the arrow gone once joined; a turn-up tradition (the birthday) still joins by being there;
#   Lap of the Wren: on Sundays (not Mondays), Tomas leads, the walk forms a line (leader, you, followers), goes round
#   and finishes; tapping elsewhere drops you out;
#   Name on the beam: locked at its start until the crew gather and the leader says its lines (0.92.3 item 13); then tapping
#   crew tells you to tap the beam; the beam's tap paints your name (trace nameYours, joined), right beside the painted row (item 23),
#   the crowd breaks up after; the newcomer's version only for new Works hands (beamNew), their nameNew traces through a
#   real save and reload; the Tiles ladder (0.92.5 item 20, the user: "the group should stand around the tiles table
#   watching two people play and the player always has the choice to join in or watch"): on Day 6 its host is at the Tiles table
#   by 15:02 and at 15:15 two crew sit at the Tiles station playing and at least three stand in the ring round it facing the board; a tap on Olu asks "Play the
#   next game" or "Watch"; playing, you sit at the board when the game ends and play the winner; after it the ladder goes
#   on; an appointment (with P926_APPT): booked, a tap on its host joins it, its scene to its end, kept; no page errors.
# Setup and environment as for cadet_test.py.   Run:  python3 join_check.py BUILD.html    (about 3 minutes)
import sys
exec(open(__file__.replace('join_check.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright

FAILS = []
def fail(m): FAILS.append(m); print('  FAIL', m)

EACH = r"""(id => {
  let d = 1, e = null; for (; d < 400; d++) { e = eventsOn(d).find(x => x.id === id); if (e) break; }
  const recWas = typeof flag === 'function' ? flag('rec.on') : null; if (/^rec-/.test(id) && TRAD_JOIN[id] && TRAD_JOIN[id].rec && !recWas) { flagSet('rec.on', true); EV_DAYS.clear(); }   // 0.93.2's rec deck two wait for the deck's opening flag, as Paddle club (put back below)
  for (d = 1; d < 400; d++) { e = eventsOn(d).find(x => x.id === id); if (e) break; }
  if (!e) return { id, err: 'not on in 400 days' };
  goToDeck(e.ev.where[0].deck); actEnd(true); clearGoal(); setShipNow((d - 1) * 1440 + e.from + 10); deckCrewFill();
  SHIP.events.joined = SHIP.events.joined.filter(k => k !== id + '@' + d); EV_MIN = -1; eventsTick();
  const lead = tradLeader(e), a = tjAgent(lead);
  if (!a) return { id, d, err: 'leader ' + lead + ' not on the deck' };
  const rk = [...(e.rooms || (e.rooms = eventRooms(e.ev)))].map(r => r.split('|')).find(r => +r[0] === deckDef.num)[1], tl = ROOM_TILES[rk], c = cellPos(...tl[Math.floor(tl.length / 2)]);   // you arrive in its room
  player.obj.position.copy(cellPos(...nearestOpen(c.x, c.z, player))); player.stop();
  const t0 = shipNow(); for (const k of [1, 4, 7]) { setShipNow(t0 + k); EV_MIN = -1; eventsTick(); }
  const passive = SHIP.events.joined.includes(id + '@' + d), now = TJ_NOW && TJ_NOW.key === id + '@' + d;
  const goal = IX_GOAL && IX_GOAL.tj === id + '@' + d ? IX_GOAL.label : null; tradJoinFrame();
  const mark = document.getElementById('tjMark'), marked = !!mark && /★/.test(mark.textContent);
  const s0 = SHIP.player.needs.social = 40, ok = tradJoinTap(TJ_NOW ? TJ_NOW.agent : a);
  if (typeof DIALOGUE !== 'undefined' && DIALOGUE && DIALOGUE.id === 'tiles.ladder') { dialogueNext(); dialogueChoose(1); dialogueEnd(true); }   // the ladder asks play or watch (0.92.5 item 20): watch
  if (typeof DIALOGUE !== 'undefined' && DIALOGUE && /^(t932\.join|tasting\.table)$/.test(DIALOGUE.id)) { let n = 0; while (DIALOGUE && n++ < 20) { const v = dialogueView(); dialogueStep(v && v.choices ? 0 : undefined); } }   // 0.93.2 (FX24): the host's join line (the tasting table: its dishes and the jar), then the activity
  // (DS1, RV14's (a) on Bread day) the leader shown is TJ_NOW's (the host on duty near the spots leads: Brennan), not only
  // the planner's pick (tradLeader): the marker's name, the arrow's person and the tap must all be that one
  const shown = TJ_NOW ? TJ_NOW.lead : null, markName = mark ? mark.textContent : '', goalCrew = IX_GOAL && IX_GOAL.tj === id + '@' + d ? IX_GOAL.crew || null : null;
  const r = { id, d, lead: shown || lead, plan: lead, passive, now, goal, marked, ok, same: !!shown && markName.includes(tjFirst(shown)) && (goalCrew === null || goalCrew === shown) && (!goal || goal.includes(tjFirst(shown)) || /beam/i.test(goal)), joined: SHIP.events.joined.includes(id + '@' + d), social: SHIP.player.needs.social - s0,
    act: ACT ? [ACT.kind, ACT.placeId, ACT.o.pose] : null, walk: !!TJ_WALK, goalAfter: !!(IX_GOAL && IX_GOAL.tj), toast: document.getElementById('tx').textContent };
  if (TJ_WALK) tradWalkEnd('over'); actEnd(true); if (/^rec-/.test(id) && !recWas && typeof flagSet === 'function') { flagSet('rec.on', null); EV_DAYS.clear(); } return r;
})"""

with sync_playwright() as pw:
    g = Game(pw, sys.argv[1])
    # the teaching arrows are on from 0.92.0, and their pop-up queue makes a toast wait its turn (2.5 s of real time)
    # behind one just shown; each part here runs in one frozen moment of the test's clock, so the join notice would
    # still be waiting. Every pop-up shows at once, as in interactions_check (AC3's line; the queue is arrows_check's)
    g.ev("if (typeof GUIDE_ON !== 'undefined' && GUIDE_ON) { GUIDE.tq.length = 0; guideToast = () => false; }")
    ids = g.ev("Object.keys(TRAD_JOIN).filter(id => TRAD_JOIN[id].act !== 'beam' && !/^appt-/.test(id))")   # appointments (appt-*): only on the calendar once booked (below)
    print(f"{len(ids)} joinable traditions (plus the beam): {', '.join(ids)}")
    for i in ids:
        officer = i == 'cometCaptain'   # the comet's tea with the Captain is for Officers and up (FX25): joined as an Officer here; a Cadet's turn-away is interactions_check's
        if officer: g.ev("window.__wk = SHIP.works; SHIP.works = { ...(SHIP.works || {}), rank: 'officer' }")
        r = g.ev(f"({EACH})('{i}')")
        if officer: g.ev("SHIP.works = window.__wk")
        if r.get('err'): fail(f"{i}: {r['err']}"); continue
        print(f"  {i} day {r['d']}: leader {r['lead']}, arrow '{r['goal']}', marker {r['marked']}; tap -> joined {r['joined']} (+{r['social']:.0f} social), {('walk' if r['walk'] else r['act'])}")
        if r['passive']: fail(f"{i}: joined by being there (it's tap to join)")
        if not r['now'] or not r['goal'] or not r['marked']: fail(f"{i}: no arrow/marker at the leader: {r}")
        elif not r['same']: fail(f"{i}: the marker, the arrow and its words don't name the same person: {r}")
        if not r['ok'] or not r['joined'] or r['social'] <= 0: fail(f"{i}: the tap didn't join: {r}")
        if not r['walk'] and not r['act']: fail(f"{i}: joined but no activity: {r}")
        if r['goalAfter']: fail(f"{i}: the arrow at the leader stayed after joining")
        if ': ' not in r['toast']: fail(f"{i}: no join notice: {r['toast']}")
    # a turn-up tradition still joins by being there (the birthday)
    b = g.ev("""(() => { const d = [...Array(40).keys()].map(x => x + 1).find(x => eventsOn(x).some(e => e.id === 'birthday')), e = eventsOn(d).find(x => x.id === 'birthday');
      goToDeck(3); clearGoal(); setShipNow((d - 1) * 1440 + e.from + 5); deckCrewFill(); const sp = placeSpot('3-mess-3'); player.obj.position.set(sp.x, 0, sp.z + .8); player.stop();
      for (const k of [0, 3, 6, 9]) { setShipNow((d - 1) * 1440 + e.from + 5 + k); EV_MIN = -1; eventsTick(); }
      return { d, joined: SHIP.events.joined.includes('birthday@' + d), tj: tradJoinable(e) }; })()""")
    print('Birthday (turn up):', b)
    if not b['joined'] or b['tj']: fail(f"the birthday should join by being there: {b}")
    # Lap of the Wren: Sundays, Tomas, a line that goes round and finishes
    lap = g.ev("""(() => { const days = [...Array(29).keys()].filter(x => eventsOn(x).some(e => e.id === 'lap-of-the-wren'));   // from day 0: not the Sunday you arrive
      const moved = d => typeof EV_DAY_DRESS !== 'undefined' && EV_DAY_DRESS.has('lap-of-the-wren@' + d);   // the storm update moves it (S6: EV_DAY_DRESS, Monday Day 15 with Tomas): not a Sunday by design
      return { days, wd: [...new Set(days.filter(d => !moved(d)).map(d => weekday(d)))], moved: days.filter(moved) }; })()""")
    print('Lap of the Wren on days', lap['days'], 'weekdays', lap['wd'], 'moved by an event', lap['moved'])
    if lap['wd'] != [6] or lap['days'][:1] != [7]: fail(f"Lap of the Wren should be on Sundays only: {lap}")
    g.ev("""(() => { const d = 7, e = eventsOn(d).find(x => x.id === 'lap-of-the-wren'); goToDeck(3); actEnd(true); clearGoal();
      setShipNow((d - 1) * 1440 + e.from + 8); deckCrewFill(); const sp = placeSpot('3-lap-3'); player.obj.position.set(sp.x, 0, sp.z + 1); player.stop();
      SHIP.events.joined = []; EV_MIN = -1; eventsTick(); window.__lap = { lead: TJ_NOW && TJ_NOW.lead, ok: TJ_NOW && tradJoinTap(TJ_NOW.agent), n: TJ_WALK ? TJ_WALK.roles.size : 0, max: 0 }; })()""")
    for _ in range(150):
        g.step(30)
        st = g.ev("(() => { if (TJ_WALK) __lap.max = Math.max(__lap.max, TJ_WALK.n); return { on: !!TJ_WALK, n: TJ_WALK ? TJ_WALK.n : __lap.max }; })()")
        if not st['on']: break
    lp = g.ev("({ ...__lap, on: !!TJ_WALK, toast: document.getElementById('tx').textContent, t: hhmm(shipNow() % 1440) })")
    print('The lap:', lp)
    if lp['lead'] != 'tomas' or not lp['ok'] or lp['n'] < 3: fail(f"the lap: Tomas leads a line of 3 or more: {lp}")
    if lp['on'] or lp['max'] < 11: fail(f"the lap didn't go all the way round: {lp}")
    dr = g.ev("""(() => { const d = 7, e = eventsOn(d).find(x => x.id === 'lap-of-the-wren'); setShipNow((d - 1) * 1440 + e.from + 8); deckCrewFill(); SHIP.events.joined = []; EV_MIN = -1; eventsTick();
      tradJoinTap(TJ_NOW.agent); const was = !!TJ_WALK; playerGo(nearestOpen(player.obj.position.x - 3, player.obj.position.z, player)); tradWalkFrame(.1); return { was, now: !!TJ_WALK }; })()""")
    print('Dropping out of the lap:', dr)
    if not dr['was'] or dr['now']: fail(f"walking off should drop you out of the lap: {dr}")
    # Name on the beam (0.92.3 item 13: locked till the crew have gathered and the leader has said the event's lines)
    g.ev("""(() => { goToDeck(5); actEnd(true); clearGoal(); const d = 1, e = eventsOn(d).find(x => x.id === 'name-on-the-beam');
      SHIP.traces.length = 0; SHIP.events.joined = []; setShipNow((d - 1) * 1440 + e.from + 1); deckCrewFill(); const sp = placeSpot('5-beam-4'); player.obj.position.set(sp.x, 0, sp.z); player.stop(); EV_MIN = -1; eventsTick();
      const it = ITEMS.find(i => i.t === 'The beam'), p = it.hit.getWorldPosition(new THREE.Vector3());
      window.__said = []; { const b0 = bubbleSay; bubbleSay = (h, t, s) => { if (TJ_NOW && TJ_NOW.agent && h === TJ_NOW.agent.h) window.__said.push(t); return b0(h, t, s); }; }
      window.__beam = { early: { goal: IX_GOAL && IX_GOAL.label, ready: beamReady(), tap: PLAYER_TAPS.some(f => f(it, p, p)), tr: SHIP.traces.length, toast: document.getElementById('tx').textContent } }; })()""")
    for _ in range(120):
        g.step(30)
        if g.ev('beamReady()'): break
    g.ev("""(() => { const it = ITEMS.find(i => i.t === 'The beam'), p = it.hit.getWorldPosition(new THREE.Vector3()); tradJoinMinute(Math.floor(shipNow()));
      Object.assign(window.__beam, { opened: hhmm(shipNow() % 1440), said: window.__said.slice(), goal: IX_GOAL && IX_GOAL.label, tell: TJ_NOW && tradJoinTap(TJ_NOW.agent), joined0: SHIP.events.joined.length, tr0: SHIP.traces.length, tap: PLAYER_TAPS.some(f => f(it, p, p)) }); })()""")
    g.step(400)
    bm = g.ev("({ ...__beam, tr: SHIP.traces.map(x => x.id), joined: SHIP.events.joined, free: TJ_FREE ? TJ_FREE.ids.size : 0, goalAfter: IX_GOAL && IX_GOAL.label })")
    print('Name on the beam:', bm)
    if bm['early']['ready'] or bm['early']['tr'] or not bm['early']['tap'] or 'gathering' not in (bm['early']['toast'] or '') or 'paint' in (bm['early']['goal'] or '').lower(): fail(f"the beam: at the start (17:06) it should wait for the crew: no arrow to paint, a tap says they're gathering: {bm['early']}")
    if len(bm['said']) < 3: fail(f"the beam: the leader should say the event's lines before it opens: {bm['said']}")
    if bm['goal'] != 'Tap the beam to paint your name' and not (bm['goal'] or '').lower().count('beam'): fail(f"the beam: no arrow to the beam once open: {bm}")
    if bm['joined0'] or bm['tr0'] or not bm['tap']: fail(f"the beam: tapping crew shouldn't paint; the beam's tap should: {bm}")
    if bm['tr'] != ['nameYours'] or bm['joined'] != ['name-on-the-beam@1'] or bm['free'] < 3 or bm['goalAfter']: fail(f"the beam: name up, joined, crowd breaks up: {bm}")
    # RV13: a late arrival (in the bay at 17:32, 8 minutes before it ends) can still sign: fewer lines (the hand-over at least), then it opens in time
    g.ev("""(() => { actEnd(true); clearGoal(); const d = 1, e = eventsOn(d).find(x => x.id === 'name-on-the-beam'); window.__le = e;
      SHIP.traces.length = 0; SHIP.events.joined = []; BEAM_OPEN.key = null; setShipNow((d - 1) * 1440 + e.to - 8); deckCrewFill(); const sp = placeSpot('5-beam-4'); player.obj.position.set(sp.x, 0, sp.z); player.stop(); EV_MIN = -1; eventsTick(); window.__said = []; })()""")
    for _ in range(80):
        g.step(15)
        if g.ev('beamReady() || shipNow() >= (__le.day - 1) * 1440 + __le.to'): break
    late = g.ev("""(() => { const it = ITEMS.find(i => i.t === 'The beam'), p = it.hit.getWorldPosition(new THREE.Vector3()), ready = beamReady(), at = hhmm(shipNow() % 1440);
      return { at, ready, inTime: ready && shipNow() <= (__le.day - 1) * 1440 + __le.to - 3, said: window.__said.length, tap: ready && PLAYER_TAPS.some(f => f(it, p, p)) }; })()""")   # inTime: 3 minutes to paint before it ends
    g.step(400)
    late['tr'] = g.ev("SHIP.traces.map(x => x.id)")
    print('A late arrival at 17:32:', late)
    if not late['ready'] or not late['inTime'] or not late['tap'] or late['tr'] != ['nameYours'] or late['said'] < 1: fail(f"the beam: arriving 8 minutes before the end you should still sign: {late}")
    # 0.92.3 item 23: your name right beside the painted row (it was the west slot, 1.3 m short of the first name)
    sl = g.ev("""(() => { const [sa, sy] = BEAM.slots[0], first = BEAM.along - BEAM.len / 2 + BEAM.clear / 2048 * BEAM.len, edge = sa + .6 - BEAM.gap * 1.2 / 256;
      const r = ROOM_BOX[BEAM.room], w = beamSlotWorld();
      return { east: BEAM.slots.every(x => x[0] <= sa), top: sy > 0, gap: +(first - edge).toFixed(3), arrow: w ? +Math.abs(w.x - X0(r.i0) - edge).toFixed(3) : null }; })()""")
    print('Your name on the beam:', sl)
    if not (sl['east'] and sl['top'] and abs(sl['gap']) <= .25 and sl['arrow'] is not None and sl['arrow'] <= .7): fail(f"the beam: your name should be the top row's east slot, its right edge within 0.25 m of the first painted name, the arrow at it: {sl}")
    nw = g.ev("""(() => ({ names: beamNew(200 * 1440).map(x => x.name + '@' + x.day), on: [...Array(200).keys()].map(x => x + 1).filter(d => eventsOn(d).some(e => e.id === 'name-on-the-beam-new')),
      depts: [...Array(200).keys()].map(x => x + 1).flatMap(d => (eventsOn(d).find(e => e.id === 'name-on-the-beam-new') || { honorees: [] }).honorees.map(p => p.dept)) }))()""")
    print('New Works hands on the beam:', nw)
    if not nw['names'] or set(nw['depts']) != {'works'} or len(nw['on']) != len(nw['names']): fail(f"newcomers' Name on the beam: {nw}")
    # Sunday table's extra chairs (the playtest note): up from 30 minutes before, gone 15 after it ends, by the ship minute,
    # after a sleep through it and after a deck change (reviewer R3's arm)
    st = g.ev("""(() => { const d = 7, e = eventsOn(d).find(x => x.id === 'sunday-table'); if (!e) return { err: 'no sunday-table on day 7' };
      const at = m => { setShipNow((d - 1) * 1440 + m); EV_MIN = -1; eventsTick(); return dressingOn().includes('longTables'); };
      goToDeck(3); const r = { before: at(e.from - 40), on: at(e.from + 30), end: at(e.to + 10), after: at(e.to + 20) };
      at(e.from + 30); skipTo((d - 1) * 1440 + e.to + 60); EV_MIN = -1; eventsTick(); r.slept = dressingOn().includes('longTables');
      at(e.from + 30); goToDeck(4); setShipNow((d - 1) * 1440 + e.to + 30); EV_MIN = -1; eventsTick(); goToDeck(3); EV_MIN = -1; eventsTick(); r.deck = dressingOn().includes('longTables');
      return r; })()""")
    print("Sunday table's long tables:", st)
    if st != {'before': False, 'on': True, 'end': True, 'after': False, 'slept': False, 'deck': False}: fail(f"the Sunday table's dressing should go 15 minutes after it ends: {st}")
    # the save (0.70.1): nameNew traces come back after a real reload (a page without ?nosave)
    url = g.page.url.split('?')[0]
    g.page.goto(url + '?debug', timeout=120000); g.page.wait_for_function('window.__sc !== undefined', timeout=120000)   # a real load takes ~28.5 s on a busy box: 30 s (the default) flaked on any build (RV25)
    g.ev("(() => { SHIP.traces.length = 0; skipTo(100 * 1440); saveGame(); })()")
    g.page.reload(timeout=120000); g.page.wait_for_function('window.__sc !== undefined', timeout=120000)
    rt = g.ev("SHIP.traces.filter(t => t && t.id === 'nameNew').map(t => t.name + '@' + t.day)")
    g.ev("localStorage.clear()")
    print('nameNew traces after a reload at day 100:', rt)
    if rt != ['Basil@22', 'Rafe@78']: fail(f"nameNew traces through the save: {rt}")   # Basil joins on day 21 since PT1 (was 35: Basil@36)
    for e in g.errors: fail('page: ' + e)
    g.close()
    # the Tiles ladder round the Tiles table (0.92.5 item 20), in a fresh game
    g = Game(pw, sys.argv[1])
    g.ev("if (typeof GUIDE_ON !== 'undefined' && GUIDE_ON) { GUIDE.tq.length = 0; guideToast = () => false; }")
    g.ev("""(() => { const d = 6, e = eventsOn(d).find(x => x.id === 'tiles-ladder'); window.__le = e; goToDeck(3); actEnd(true); clearGoal(); SHIP.events.joined = [];
      skipTo((d - 1) * 1440 + e.from - 25); deckCrewFill(); const sp = placeSpot('3-ladder-2') || placeSpot('3-tiles-1'); player.obj.position.set(sp.x, 0, sp.z - 1.6); player.stop(); EV_MIN = -1; eventsTick(); })()""")
    LAD = r"""(() => { const st = ['3-tiles-1', '3-tiles-2'], ring = DECKS[3].places.filter(p => p.event === 'tiles-ladder').map(p => p.id), b = [placeSpot(st[0]), placeSpot(st[1])].filter(Boolean);
      const bx = b.length ? (b[0].x + b[1].x) / 2 : 0, bz = b.length ? (b[0].z + b[1].z) / 2 : 0, ang = d => Math.abs(Math.atan2(Math.sin(d), Math.cos(d)));
      const at = DECK_CREW.filter(a => a.p && a.settled && a.spot);
      const seated = at.filter(a => st.includes(a.spot.id)).map(a => [a.p.id, a.spot.id, a.pose]);
      const ring2 = at.filter(a => ring.includes(a.spot.id)).map(a => [a.p.id, a.spot.id, +(ang(Math.atan2(bx - a.spot.x, bz - a.spot.z) - a.spot.face) * 180 / Math.PI).toFixed(0)]);
      const lounge = at.filter(a => /^3-lounge/.test(a.spot.id) && /tiles-ladder/.test((whereIs(a.p, shipNow()) || {}).tag || '')).map(a => a.p.id);
      return { t: hhmm(shipNow() % 1440), seated, ring: ring2, lounge, boards: dressingOn().includes('tilesNight') }; })()"""
    host = g.ev("__le.ev.host")                       # from 14:35: the crew walk in as they would (their plans set off from 14:40)
    for _ in range(80):
        g.step(30)
        if g.ev("shipNow() >= (__le.day - 1) * 1440 + __le.from + 2"): break
    lr = g.ev(LAD)
    print('The Tiles ladder at', lr['t'], ':', lr)
    if not any(x[0] == host for x in lr['seated'] + lr['ring']): fail(f"the ladder: its host {host} should be at the Tiles table by the start (they set off ahead: tladLead): {lr}")
    for _ in range(80):                                  # the others set off 15 minutes ahead when they're free (tladLead): the ring by 15:15, mid-game (a new pair sits down at 15:10)
        g.step(30)
        if g.ev("shipNow() >= (__le.day - 1) * 1440 + __le.from + 15"): break
    lr = g.ev(LAD)
    if len(lr['seated']) != 2 or any(not x[2].startswith('sit') for x in lr['seated']): fail(f"the ladder: two crew should sit playing at the Tiles station at 15:15: {lr['seated']}")
    print('            at', lr['t'], ':', lr)
    facing = [x for x in lr['ring'] if x[2] <= 70]
    if len(facing) < 3: fail(f"the ladder: at least three should stand in the ring round the Tiles table facing the board: {lr['ring']}")
    if lr['lounge'] or lr['boards']: fail(f"the ladder: nobody at it in the lounge seats, no boards on every table: {lr}")
    card = g.ev("""(() => { const a = tjAgent(__le.ev.host) || DECK_CREW.find(c => c.p && c.settled && c.spot && /^3-ladder/.test(c.spot.id)); if (!a) return { err: 'nobody at the ladder to tap' };
      const ok = tradJoinTap(a), id = DIALOGUE && DIALOGUE.id; if (DIALOGUE) dialogueNext(); const v = DIALOGUE ? dialogueView() : null;
      return { ok, id, choices: v && v.choices, joined: SHIP.events.joined.includes('tiles-ladder@' + __le.day) }; })()""")
    print('A tap on the ladder:', card)
    if not card.get('choices') or 'Play the next game' not in card['choices'] or 'Watch' not in card['choices'] or not card.get('joined'): fail(f"the ladder: a tap should join and offer 'Play the next game' or 'Watch': {card}")
    if card.get('choices'):
        g.ev("(() => { dialogueChoose(card = 0); dialogueNext(); dialogueEnd(true); })()".replace('card = 0', '0'))
        play = None
        for _ in range(40):
            g.step(30)
            play = g.ev("({ t: hhmm(shipNow() % 1440), act: ACT && ACT.kind, place: ACT && ACT.placeId, opp: TL_GAME && TL_GAME.opp, across: (DECK_CREW.find(a => a.settled && a.spot && ['3-tiles-1', '3-tiles-2'].includes(a.spot.id) && (!ACT || a.spot.id !== ACT.placeId)) || { p: {} }).p.id })")
            if play['opp']: break
        print('Playing the next game:', play)
        if not play or play['act'] != 'tiles' or play['place'] not in ('3-tiles-1', '3-tiles-2') or not play['opp'] or play['opp'] != play['across']: fail(f"the ladder: 'Play the next game' should sit you at the board against the one across from you: {play}")
        if play and play['opp']:
            g.ev("(() => { tilesEnd('leave'); actEnd(true); })()")
            for _ in range(20):
                g.step(30)
                if len(g.ev(LAD)['seated']) == 2: break
            after = g.ev(LAD)
            print('After your game:', after['t'], after['seated'])
            if len(after['seated']) != 2: fail(f"the ladder: after your game two crew should be playing again: {after}")
    for e in g.errors: fail('page: ' + e)
    g.close()
    # an appointment (0.92.6 item 9, P926_APPT): a one-off that's only on the calendar once booked, so not in the sweep
    # above; here one is booked (the big scope with Sato, asked for) and joined by a tap on her, its scene read to its end
    g = Game(pw, sys.argv[1])
    if g.ev("typeof TRAD_JOIN['appt-scope'] !== 'undefined'"):
        g.ev("if (typeof GUIDE_ON !== 'undefined' && GUIDE_ON) { GUIDE.tq.length = 0; guideToast = () => false; }")
        b = g.ev("""(() => { skipTo(2 * 1440 + 600); SHIP.device.settings.tips = false; socInit(); const r = relGet('sato'); r.pts = 65; r.tier = 3;
          apptAsk('scope', 'sato'); const b = SHIP.apptx.book.slice(-1)[0]; if (!b) return null; skipTo((b.day - 1) * 1440 + b.from - 20);
          const e = eventsOn(b.day).find(x => x.id === 'appt-scope'), rk = [...eventRooms(e.ev)][0].split('|'); goToDeck(+rk[0]); deckCrewFill();
          const tl = ROOM_TILES[rk[1]], c = cellPos(...tl[Math.floor(tl.length / 2)]); player.obj.position.set(c.x, 0, c.z); player.stop(); return { id: b.id, day: b.day, from: b.from }; })()""")
        r = None
        if b:
            for _ in range(40):
                g.step(45)
                if g.ev("!!TJ_NOW && TJ_NOW.e.id === 'appt-scope' && !!TJ_NOW.agent && TJ_NOW.agent.settled"): break
            r = g.ev("""(() => { const a = TJ_NOW && TJ_NOW.e.id === 'appt-scope' ? TJ_NOW.agent : null; if (!a) return { err: 'no join offered' };
              const ok = tradJoinTap(a), open = !!DIALOGUE && DIALOGUE.id.startsWith('appt:scope'); let n = 0;
              while (DIALOGUE && n++ < 40) { const v = dialogueView(); if (v && v.choices) dialogueStep(0); else dialogueStep(0); }
              return { ok, lead: a.p.id, open, done: !!SHIP.apptx.book.find(x => x.id === %d).done, joined: SHIP.events.joined.includes('appt-scope@%d') }; })()""" % (b['id'], b['day']))
        print('An appointment (the big scope, booked):', b, r)
        if not b or not r or r.get('err') or not (r['ok'] and r['open'] and r['joined'] and r['done'] and r['lead'] == 'sato'): fail(f"an appointment: booked, a tap on Sato joins it and its scene runs to the end, kept: {b} {r}")
    else: print('An appointment: P926_APPT off, none to join')
    for e in g.errors: fail('page: ' + e)
    g.close()
print('JOIN CHECK ' + ('FAILED' if FAILS else 'OK'))
sys.exit(1 if FAILS else 0)
