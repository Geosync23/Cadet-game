# Starship Cadet: tap-to-join check (playtest 1, the traditions engineer, 0.70.x; keep in the repo next to events_check.py)
# Checks section 18's tap to join (TRAD_JOIN) in a test game (?nosave&debug), each part on its deck:
#   every joinable tradition: being there doesn't join it; a tap on its leader joins you (eventJoin: social, the notice)
#   and starts its activity at one of its spots (or a walk); the leader's marker, the arrow at the leader and its tip while
#   it's on, the arrow gone once joined; a turn-up tradition (the birthday) still joins by being there;
#   Lap of the Wren: on Sundays (not Mondays), Tomas leads, the walk forms a line (leader, you, followers), goes round
#   and finishes; tapping elsewhere drops you out;
#   Name on the beam: tapping crew tells you to tap the beam; the beam's tap paints your name (trace nameYours, joined),
#   the crowd breaks up after; the newcomer's version only for new Works hands (beamNew), their nameNew traces through a
#   real save and reload; no page errors.
# Setup and environment as for cadet_test.py.   Run:  python3 join_check.py BUILD.html    (about 3 minutes)
import sys
exec(open(__file__.replace('join_check.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright

FAILS = []
def fail(m): FAILS.append(m); print('  FAIL', m)

EACH = r"""(id => {
  let d = 1, e = null; for (; d < 400; d++) { e = eventsOn(d).find(x => x.id === id); if (e) break; }
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
  const r = { id, d, lead, passive, now, goal, marked, ok, joined: SHIP.events.joined.includes(id + '@' + d), social: SHIP.player.needs.social - s0,
    act: ACT ? [ACT.kind, ACT.placeId, ACT.o.pose] : null, walk: !!TJ_WALK, goalAfter: !!(IX_GOAL && IX_GOAL.tj), toast: document.getElementById('tx').textContent };
  if (TJ_WALK) tradWalkEnd('over'); actEnd(true); return r;
})"""

with sync_playwright() as pw:
    g = Game(pw, sys.argv[1])
    ids = g.ev("Object.keys(TRAD_JOIN).filter(id => TRAD_JOIN[id].act !== 'beam')")
    print(f"{len(ids)} joinable traditions (plus the beam): {', '.join(ids)}")
    for i in ids:
        r = g.ev(f"({EACH})('{i}')")
        if r.get('err'): fail(f"{i}: {r['err']}"); continue
        print(f"  {i} day {r['d']}: leader {r['lead']}, arrow '{r['goal']}', marker {r['marked']}; tap -> joined {r['joined']} (+{r['social']:.0f} social), {('walk' if r['walk'] else r['act'])}")
        if r['passive']: fail(f"{i}: joined by being there (it's tap to join)")
        if not r['now'] or not r['goal'] or not r['marked']: fail(f"{i}: no arrow/marker at the leader: {r}")
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
      return { days, wd: [...new Set(days.map(d => weekday(d)))] }; })()""")
    print('Lap of the Wren on days', lap['days'], 'weekdays', lap['wd'])
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
    # Name on the beam
    g.ev("""(() => { goToDeck(5); actEnd(true); clearGoal(); const d = 1, e = eventsOn(d).find(x => x.id === 'name-on-the-beam');
      SHIP.traces.length = 0; SHIP.events.joined = []; setShipNow((d - 1) * 1440 + e.from + 6); deckCrewFill(); const sp = placeSpot('5-beam-4'); player.obj.position.set(sp.x, 0, sp.z); player.stop(); EV_MIN = -1; eventsTick();
      const it = ITEMS.find(i => i.t === 'The beam'), p = it.hit.getWorldPosition(new THREE.Vector3());
      window.__beam = { goal: IX_GOAL && IX_GOAL.label, tell: TJ_NOW && tradJoinTap(TJ_NOW.agent), joined0: SHIP.events.joined.length, tr0: SHIP.traces.length, tap: PLAYER_TAPS.some(f => f(it, p, p)) }; })()""")
    g.step(400)
    bm = g.ev("({ ...__beam, tr: SHIP.traces.map(x => x.id), joined: SHIP.events.joined, free: TJ_FREE ? TJ_FREE.ids.size : 0, goalAfter: IX_GOAL && IX_GOAL.label })")
    print('Name on the beam:', bm)
    if bm['goal'] != 'Tap the beam to paint your name' and not (bm['goal'] or '').lower().count('beam'): fail(f"the beam: no arrow to the beam: {bm}")
    if bm['joined0'] or bm['tr0'] or not bm['tap']: fail(f"the beam: tapping crew shouldn't paint; the beam's tap should: {bm}")
    if bm['tr'] != ['nameYours'] or bm['joined'] != ['name-on-the-beam@1'] or bm['free'] < 3 or bm['goalAfter']: fail(f"the beam: name up, joined, crowd breaks up: {bm}")
    nw = g.ev("""(() => ({ names: beamNew(200 * 1440).map(x => x.name + '@' + x.day), on: [...Array(200).keys()].map(x => x + 1).filter(d => eventsOn(d).some(e => e.id === 'name-on-the-beam-new')),
      depts: [...Array(200).keys()].map(x => x + 1).flatMap(d => (eventsOn(d).find(e => e.id === 'name-on-the-beam-new') || { honorees: [] }).honorees.map(p => p.dept)) }))()""")
    print('New Works hands on the beam:', nw)
    if not nw['names'] or set(nw['depts']) != {'works'} or len(nw['on']) != len(nw['names']): fail(f"newcomers' Name on the beam: {nw}")
    # the save (0.70.1): nameNew traces come back after a real reload (a page without ?nosave)
    url = g.page.url.split('?')[0]
    g.page.goto(url + '?debug'); g.page.wait_for_function('window.__sc !== undefined', timeout=60000)
    g.ev("(() => { SHIP.traces.length = 0; skipTo(100 * 1440); saveGame(); })()")
    g.page.reload(); g.page.wait_for_function('window.__sc !== undefined', timeout=60000)
    rt = g.ev("SHIP.traces.filter(t => t && t.id === 'nameNew').map(t => t.name + '@' + t.day)")
    g.ev("localStorage.clear()")
    print('nameNew traces after a reload at day 100:', rt)
    if rt != ['Basil@36', 'Rafe@78']: fail(f"nameNew traces through the save: {rt}")
    for e in g.errors: fail('page: ' + e)
    g.close()
print('JOIN CHECK ' + ('FAILED' if FAILS else 'OK'))
sys.exit(1 if FAILS else 0)
