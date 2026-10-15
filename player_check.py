# Starship Cadet: player check (keep in the repo, next to cadet_test.py, deck_check.py and day_check.py)
# Checks the player's needs and activities (section 15), deterministically:
#   on paper: a week of normal days (shower, two meals, the gym and a call home every other day, 8 hours' sleep)
#   keeps every need at 30 or more and the walking speed at 100%; a week of neglect never goes below 0 or above 100
#   the speed rule: fitness or energy under 25 walks at 80%, both at 64%, and you really do cover less ground
#   sleep: the bunk's Sleep refills energy; a time skip awake drains it; a night without sleep slows you
#   in the game, one player day on the real decks, by tapping the real things: shower (Deck 4), servery tray then a
#   mess seat, grab shelf, treadmill (run), weights (lift), call-home booth (call), shelves then the counter
#   (browse, pay); each need rises by its gain, the pose is right, you're back on your feet and visible after
#   places held by crew are left alone ("In use"); the servery is closed between meals; walking away stops an
#   activity (keeping what you'd gained); someone's private wash pod isn't offered; draw calls stay under BUDGET
#   saving: a v 2 save keeps needs; a v 1 save loads with needs at 80; ?nosave neither reads nor writes
# Setup and environment as for cadet_test.py.
# Run:  python3 player_check.py BUILD.html
import sys, json, pathlib
exec(open(__file__.replace('player_check.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright

BUDGET = 450
ok = True
def fail(msg):
    global ok
    ok = False
    print('FAIL', msg)
def check(cond, msg):
    if not cond: fail(msg)
    return cond

# a week of days on paper, with the game's own rates (needsDrain) and each activity's gain spread over its minutes
PAPER = r"""(({ normal }) => {
  const n = SHIP.player.needs; Object.assign(n, NEEDS_FRESH);
  let lo = {}, hi = {}, slowMins = 0; for (const k of NEED_KEYS) { lo[k] = 100; hi[k] = 0; }
  const look = () => { for (const k of NEED_KEYS) { lo[k] = Math.min(lo[k], n[k]); hi[k] = Math.max(hi[k], n[k]); } };
  const awake = mins => { for (let m = 0; m < mins; m++) { needsDrain(1, false); if (playerSpeed() < 1) slowMins++; look(); } };
  const act = kind => { const d = PLAYER_ACTS[kind]; for (let m = 0; m < d.mins; m++) { needsDrain(1, false);
    if (d.need) n[d.need] = needClamp(n[d.need] + d.gain / d.mins + NEED_DRAIN[d.need][0] / 60); look(); } };
  const sleep = mins => { needsDrain(mins, true); look(); };
  for (let day = 1; day <= 7; day++) {                    // 06:00 to 06:00
    if (normal) {
      awake(60); act('shower'); awake(5); act('eat'); awake(25);                  // 06:00-08:00
      awake(9 * 60);                                                              // the shift, 08:00-17:00
      awake(30); act('eat'); awake(40);                                           // dinner about 17:30
      if (day % 2) act('gym'); else act('call');
      awake(22 * 60 - (18 * 60 + 30) - (day % 2 ? 30 : 15));                      // to 22:00
      sleep(8 * 60);
    } else { awake(16 * 60); sleep(8 * 60); }                                     // no meals, no shower, no gym, no calls
  }
  const r = x => Math.round(x * 10) / 10;
  for (const k of NEED_KEYS) { lo[k] = r(lo[k]); hi[k] = r(hi[k]); }
  return { lo, hi, slowMins, end: Object.fromEntries(NEED_KEYS.map(k => [k, r(n[k])])) };
})"""

# tap a thing on the current deck by its title (and, if several, the one nearest a tile), as section 11 would
TAP = r"""(({ title, near }) => {
  const its = ITEMS.filter(i => i.t === title); if (!its.length) return 'no item ' + title;
  const c = near ? cellPos(...near) : null;
  const it = its.map(i => { i.hit.getWorldPosition(_wp); return [i, _wp.clone()]; }).sort((a, b) => c ? a[1].distanceTo(c) - b[1].distanceTo(c) : 0)[0];
  const done = playerTap(it[0], it[1].clone(), it[1].clone());
  if (!done) { it[0].hit.getWorldPosition(_wp); approach(_wp.clone(), it[0].front, it[0].depth, () => toast(it[0].t, it[0].x)); }
  return done;
})"""
STATE = r"""JSON.stringify({ act: ACT && [ACT.kind, ACT.placeId, ACT.phase, ACT.pose, Math.round(ACT.done * 10) / 10],
  needs: Object.fromEntries(NEED_KEYS.map(k => [k, Math.round(SHIP.player.needs[k] * 10) / 10])), basket,
  visible: player.obj.visible, toast: document.getElementById('tt').textContent + ': ' + document.getElementById('tx').textContent,
  time: hhmm(SHIP.time.min), calls: renderer.info.render.calls, deck: deckDef.num })"""

def state(g): return json.loads(g.ev(STATE))

def run_activity(g, title, near=None, limit=4000, label=None):
    """tap, then step until the activity is over (or the limit); returns (tapped, states seen, end state)"""
    before = state(g)
    for tries in range(6):                                # busy (crew on it, a queue): wait five ship minutes and try again
        tapped = g.ev(f"({TAP})({json.dumps({'title': title, 'near': near})})"); g.step(2)
        if state(g)['act'] or not re.match(r"In use|There's a queue", state(g)['toast'].split(': ', 1)[1]): break
        print('   ', title, 'busy:', state(g)['toast'][:80]); g.step(190)
    seen, peak = [], 0
    for k in range(limit // 30):
        g.step(30); s = state(g); peak = max(peak, s['calls'])
        if s['act']: seen.append(s['act'])
        if not s['act'] and k > 0: break
    end = state(g)
    if not any(x[2] == 'do' for x in seen) and re.match(r"In use|There's a queue", end['toast'].split(': ', 1)[1]) and limit > 0:
        print('   ', title, 'taken on arrival:', end['toast'][:80]); g.step(190)
        return run_activity(g, title, near, limit - 1000, label)
    if os.environ.get('PC_DEBUG'): print(seen[:3], seen[-3:], end)
    print(f"  {label or title:22s} tapped={tapped!s:5s} poses={sorted(set(a[3] for a in seen if a[2] == 'do'))} "
          f"{end['time']} needs {end['needs']} calls<={peak}")
    return tapped, before, seen, end, peak

def body_check(name, need, gain, before, end, seen, pose):
    if pose: check(any(a[2] == 'do' and a[3] in ((pose,) if isinstance(pose, str) else pose) for a in seen), f'{name}: pose {pose} not taken ({sorted(set(str(a[3]) for a in seen))})')
    if need: check(end['needs'][need] >= min(100, before['needs'][need] + gain - 3) - .1, f"{name}: {need} {before['needs'][need]} -> {end['needs'][need]} (gain {gain})")
    check(end['visible'] and not end['act'], f'{name}: not back on your feet ({end})')

with sync_playwright() as pw:
    g = Game(pw, sys.argv[1])
    errors = g.errors

    print('On paper, a week of normal days:')
    p = g.ev(f"({PAPER})({{ normal: true }})"); print('  lowest', p['lo'], 'slow minutes', p['slowMins'])
    for k, v in p['lo'].items(): check(v >= 30, f'normal week: {k} fell to {v}')
    check(p['slowMins'] == 0, f"normal week: slowed for {p['slowMins']} minutes")
    print('On paper, a week of neglect:')
    p = g.ev(f"({PAPER})({{ normal: false }})"); print('  end', p['end'], 'lowest', p['lo'], 'highest', p['hi'])
    check(all(0 <= p['lo'][k] and p['hi'][k] <= 100 for k in p['lo']), 'neglect: a need left 0-100')
    check(p['end']['fitness'] < 25 and p['end']['hunger'] == 0, 'neglect: fitness and hunger should be low')

    print('The speed rule:')
    sp = g.ev(r"""(() => { const n = SHIP.player.needs, out = {};
      const walk = () => { Object.assign(player.obj.position, cellPos(...nearestOpen(LIFT_AT[0], LIFT_AT[1], player))); player.steer = { x: 0, z: 1, k: 1 }; player.vel = 0;
        for (let k = 0; k < 20; k++) { playerUpdate(.05, 0); player.update(.05, 0); } player.steer = null; return player.vel; };
      for (const [f, e] of [[80, 80], [20, 80], [80, 20], [20, 20], [25, 25]]) { Object.assign(n, { fitness: f, energy: e }); playerUpdate(0, 0);
        out[f + '/' + e] = [Math.round(playerSpeed() * 1000) / 1000, Math.round(player.maxV / PLAYER_V0 * 1000) / 1000, Math.round(walk() / PLAYER_V0 * 1000) / 1000]; }
      Object.assign(n, NEEDS_FRESH); playerUpdate(0, 0); return out; })()""")
    print('  fitness/energy: [speed, top speed ratio, walking speed reached after 1 s, as a ratio]', sp)
    for key, want in [('80/80', 1), ('20/80', .8), ('80/20', .8), ('20/20', .64), ('25/25', 1)]:
        check(abs(sp[key][0] - want) < 1e-9 and abs(sp[key][1] - want) < 1e-3, f'speed {key}: {sp[key]} want {want}')
    for key in sp: check(abs(sp[key][2] - sp[key][0]) < .01, f'speed {key}: walking at {sp[key][2]}, want {sp[key][0]}')

    print('Sleep and time skips:')
    sl = g.ev(r"""(() => { const n = SHIP.player.needs; Object.assign(n, NEEDS_FRESH); setShipNow(22 * 60); needsT = null; playerUpdate(0, 0);
      n.energy = 40; sleeping = true; sleepUntil(WAKE_AT); sleeping = false; const slept = n.energy;
      skipTo(shipNow() + 21 * 60); const awake = n.energy; playerUpdate(0, 0);
      return { slept: Math.round(slept), awake21h: Math.round(awake), speed: playerSpeed(), at: clockText() }; })()""")
    print(' ', sl)
    check(sl['slept'] == 100, 'sleep should refill energy')
    check(sl['awake21h'] < 25 and abs(sl['speed'] - .8) < 1e-9, 'twenty-one hours awake should slow you')

    print('One player day, tapping the real things:')
    g.ev("Object.assign(SHIP.player.needs, { hunger: 20, energy: 100, hygiene: 10, fitness: 30, social: 20 }); basket = false")
    g.ev("setShipNow(10 * 60 + 30 + 1440 * 7); needsT = null; goToDeck(4); Object.assign(player.obj.position, cellPos(7, 3)); player.stop()"); g.step(5)
    # someone's own wash pod is not offered
    t = g.ev(f"({TAP})({json.dumps({'title': 'Wash pod'})})"); g.step(5)
    check(t is False and not state(g)['act'], 'a private wash pod should not be offered')
    peak = 0
    tp, b, seen, e, pk = run_activity(g, 'Shower', near=[3, 1]); peak = max(peak, pk)
    check(tp is True and seen and seen[0][1].startswith('4-shower'), f'shower: {seen[:1]}'); body_check('shower', 'hygiene', 80, b, e, seen, 'stand')
    g.ev("setShipNow(shipNow() + 1); goToDeck(3)"); g.step(5)   # mid-morning on Deck 3: the crew are at work
    tp, b, seen, e, pk = run_activity(g, 'Grab and go'); peak = max(peak, pk); body_check('grab', 'hunger', 25, b, e, seen, None)
    tp, b, seen, e, pk = run_activity(g, 'Treadmills'); peak = max(peak, pk); body_check('treadmill', 'fitness', 30, b, e, seen, 'run')
    tp, b, seen, e, pk = run_activity(g, 'Weights'); peak = max(peak, pk); body_check('weights', 'fitness', 30, b, e, seen, 'lift')
    tp, b, seen, e, pk = run_activity(g, 'Booth 1'); peak = max(peak, pk); body_check('booth', 'social', 40, b, e, seen, ('call', 'sit:call'))
    check(seen and seen[0][1].startswith('3-callhome'), 'booth: should use a callhome place')
    t = g.ev(f"({TAP})({json.dumps({'title': 'Counter'})})"); g.step(60)
    check(t is False and not state(g)['act'], 'the counter with nothing picked out should just show its text')
    tp, b, seen, e, pk = run_activity(g, 'Shelves'); peak = max(peak, pk); body_check('browse', None, 0, b, e, seen, 'browse')
    check(e['basket'] is True, 'browsing should leave something to pay for')
    tp, b, seen, e, pk = run_activity(g, 'Counter'); peak = max(peak, pk); body_check('pay', None, 0, b, e, seen, 'pay')
    check(e['basket'] is False, 'paying should empty the basket')
    g.ev("setShipNow(Math.floor(shipNow() / 1440) * 1440 + 17 * 60 + 40); needsT = null"); g.step(5)   # dinner
    tp, b, seen, e, pk = run_activity(g, 'Servery', label='Servery, then a seat'); peak = max(peak, pk)
    kinds = [a[0] for a in seen]
    check(tp is True and ('tray' in kinds or 'queue' in kinds) and 'eat' in kinds, f'servery: {sorted(set(kinds))}')
    check(any(a[0] == 'eat' and a[1] and a[1].startswith('3-mess') and a[3] == 'sit' for a in seen), 'servery: should sit at a mess seat to eat')
    body_check('eat', 'hunger', 55, b, e, seen, None)
    check(peak < BUDGET, f'draw calls {peak} over {BUDGET}')
    # the galley's queue (section 16, 0.29.6): galleyJoin gives the back of the line and your turn. The real galley when the
    # build has it (a combined build), else stand-ins shaped like it
    real = g.ev("[typeof takePortion === 'function', typeof galleyJoin === 'function', typeof shipEffects === 'function']")
    print('  the real galley and machines in this build:', dict(zip(['takePortion', 'galleyJoin', 'shipEffects'], real)))
    if not real[1]:
        g.ev(r"""(() => { window.portions = 30;
          window.takePortion = () => { delete window.joined; if (window.portions > 0) { window.portions--; return true; } return false; };
          window.galleyText = w => w === 'grab' ? '5 on the shelf.' : 'Serving: Fish pie. ' + window.portions + ' portions in the pans.';
          window.galleyJoin = () => (window.joined = { at: [33, 2], xy: [33.55, 2.5], face: 's', ahead: 3, turnAt: shipNow() + 3.25 });
          window.galleyTurn = () => !!window.joined && shipNow() >= window.joined.turnAt && window.portions > 0; })()""")
    g.ev("SHIP.player.needs.hunger = 20")
    tp, b, seen, e, pk = run_activity(g, 'Servery', label='The queue, then a seat')
    kinds = [a[0] for a in seen]
    check(tp is True and 'queue' in kinds and 'eat' in kinds and 'tray' not in kinds, f'queue: {sorted(set(kinds))}')
    waited = sum(1 for a in seen if a[0] == 'queue' and a[1] is None and a[2] == 'do')
    check(waited >= (1 if real[1] else 3), f'queue: should wait at the back of the line for the turn ({waited} checks)')
    check(any(a[0] == 'eat' and a[1] and a[1].startswith('3-mess') and a[3] == 'sit' for a in seen), 'queue: then sit at a mess seat to eat')
    body_check('queue and eat', 'hunger', 55, b, e, seen, None)
    if real[1]:
        joined = g.ev("GALLEY_JOINED.has('player')"); print('  still in the galley\'s line after eating:', joined)
        check(joined is False, 'queue: takePortion should clear the join')
    elif real[0]:                                     # the real galley's food but not yet its queue (before 0.29.6): the stand-in queue fed you from the real pans
        print('  (stand-in queue, real food: served from the real galley)')
        g.ev("delete window.takePortion; delete window.galleyText; delete window.galleyJoin; delete window.galleyTurn; delete window.joined; delete window.portions")
    else:
        left = g.ev("[window.portions, !!window.joined]"); print('  portions left, still joined:', left)
        check(left == [29, False], 'queue: one portion taken, and the join cleared')
        g.ev("delete window.takePortion; delete window.galleyText; delete window.galleyJoin; delete window.galleyTurn; delete window.joined; delete window.portions")

    print('Places held by crew, closed servery, walking away:')
    held = g.ev(r"""(() => { const ids = ['3-callhome-1', '3-callhome-2', '3-callhome-3', '3-callhome-4'];
      const fake = ids.map(id => ({ goalId: id, p: { name: 'Test ' + id } })); DECK_CREW.push(...fake);
      const it = ITEMS.find(i => i.t === 'Booth 2'); it.hit.getWorldPosition(_wp); const r = playerTap(it, _wp.clone(), _wp.clone());
      DECK_CREW.splice(DECK_CREW.length - 4, 4); return [r, !!ACT, document.getElementById('tx').textContent]; })()""")
    print(' ', held)
    check(held[0] is True and held[1] is False and held[2].startswith('In use'), f'held booths: {held}')
    g.ev("setShipNow(Math.floor(shipNow() / 1440) * 1440 + 1440 + 12 * 60); needsT = null"); g.step(2)
    t = g.ev(f"({TAP})({json.dumps({'title': 'Servery'})})"); g.step(2); s = state(g)
    print('  servery at 12:00 the next day:', s['toast'][:70])
    check(t is True and not s['act'] and 'closed' in s['toast'].lower(), 'the servery should be closed at 12:00')
    g.ev(f"({TAP})({json.dumps({'title': 'Treadmills'})})")
    for k in range(40):
        g.step(30)
        if state(g)['act'] and state(g)['act'][2] == 'do' and state(g)['act'][4] >= 5: break
    f0 = state(g)['needs']['fitness']
    g.ev("playerGo(nearestOpen(LIFT_AT[0], LIFT_AT[1], player))"); g.step(3); s = state(g)
    print('  walked away after 5 min:', s['act'], 'visible', s['visible'], 'fitness', f0, '->', s['needs']['fitness'])
    check(not s['act'] and s['visible'] and s['needs']['fitness'] >= f0 - .5, 'walking away should stop the workout and keep the gain')

    # the ship's effects (section 17): a known shipEffects result put in playerFx's once-a-minute cache, so the wiring is
    # tested the same with or without section 17
    print('The ship\'s effects on needs (a set shipEffects reading):')
    FX = "FX_MIN = Math.floor(shipNow()); FX_NOW = { deck: deckDef.num, restore: { hunger: 1, energy: 1, hygiene: .5, fitness: 1, social: 1 }, drain: { hunger: 2, energy: 1, hygiene: 1, fitness: 1, social: 1 }, walk: .5, notes: [{ text: 'The showers are running weak' }] };"
    st = g.ev(r"""(() => { """ + FX + r"""
      const n = SHIP.player.needs; Object.assign(n, { hunger: 50, hygiene: 50 });
      needsDrain(60, false, playerFx()); const out = { drainHungerX2: Math.round((50 - n.hunger) * 10) / 10, hygieneDrain: Math.round((50 - n.hygiene) * 10) / 10 };
      playerUpdate(0, 0); out.speed = playerSpeed(); out.maxV = player.maxV / PLAYER_V0;
      device.open(); out.note = document.getElementById('devBody').textContent.includes('showers are running weak'); device.close();
      n.hygiene = 10; ACT = { kind: 'shower', def: PLAYER_ACTS.shower, phase: 'do', done: 0, o: {}, deck: deckDef, x: 0, z: 0, y: 0, face: player.face, to: {}, body: { set() {}, update() {}, dispose() {} } };
      needsT = shipNow() - PLAYER_ACTS.shower.mins; """ + FX + r""" playerUpdate(0, 0); out.shower = Math.round(n.hygiene); ACT = null; FX_MIN = -1;
      return out; })()""")
    print(' ', st)
    check(st['drainHungerX2'] == 8 and st['hygieneDrain'] == 2.5, 'drain multipliers from shipEffects')
    check(st['speed'] == 1 and abs(st['maxV'] - 1) < 1e-9, "shipEffects' walk must not slow the player (the user's rule)")
    check(st['note'], 'the ship notes should show on the device')
    check(st['shower'] == 50, f"a weak shower (restore x0.5) should give half: 10 -> {st['shower']}")
    if real[2]:
        live = g.ev("(() => { FX_MIN = -1; const f = playerFx(), r = shipEffects(deckDef.num); return f === r && NEED_KEYS.every(k => isFinite(f.restore[k]) && isFinite(f.drain[k])); })()")
        print('  playerFx is the real shipEffects for this deck:', live)
        check(live, 'playerFx should read the real shipEffects')
    if not real[0]:                                   # the galley's food on its own, with stand-ins (a combined build tests the real one above)
        fd = g.ev(r"""(() => { window.portions = 1; window.grab = 0;
          window.takePortion = () => { if (portions > 0) { portions--; return true; } if (grab > 0) { grab--; return true; } return false; };
          window.galleyText = w => w === 'grab' ? (grab ? grab + ' on the shelf.' : 'The shelf is empty.') : portions ? 'Serving: Fish pie. ' + portions + ' portions in the pans.' : 'The pans are empty. The next pot is on its way.';
          const out = { peek: foodFrom('servery', true).ok, take: foodFrom('servery'), peekEmpty: foodFrom('grab', true), takeEmpty: foodFrom('grab').ok };
          delete window.takePortion; delete window.galleyText; delete window.portions; delete window.grab; return out; })()""")
        print('  galley stand-in:', fd)
        check(fd['peek'] is True and fd['take'].get('dish') == 'Fish pie' and fd['peekEmpty']['ok'] is False and fd['takeEmpty'] is False, f'galley stand-in: {fd}')
    errors = g.errors
    g.close()

    print('Saving:')
    tmp = WORK / 'test' / '_save_check.html'
    tmp.write_text(instrument(pathlib.Path(sys.argv[1]).read_text()))
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    page = b.new_page(viewport={'width': 600, 'height': 500})
    page.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
    page.add_init_script(INIT)
    url = 'file://' + str(tmp)
    def load(q=''):
        page.goto(url + q); page.wait_for_function('window.__sc !== undefined', timeout=60000)
        return lambda s: page.evaluate('s => window.__sc(s)', s)
    ev = load()
    ev("localStorage.setItem(SAVE_KEY, JSON.stringify({ v: 1, build: '0.25.2', time: { day: 2, min: 600 }, player: { deck: 4, tile: [7, 3], facing: 0 }, ship: { decks: {} }, crew: {} })); Storage.prototype.setItem = () => {}")
    ev = load()
    v1 = json.loads(ev("JSON.stringify([SHIP.time.day, SHIP.player.needs])")); print('  v 1 save:', v1)
    check(v1[0] == 2 and all(v == 80 for v in v1[1].values()), 'a v 1 save should load with needs at 80')
    ev("Object.assign(SHIP.player.needs, { hunger: 11, energy: 22, hygiene: 33, fitness: 44, social: 55 }); saveGame()")
    raw = json.loads(ev("localStorage.getItem(SAVE_KEY)")); print('  saved:', raw['v'], raw['player'].get('needs'))
    check(raw['v'] == 2 and raw['player']['needs'] == {'hunger': 11, 'energy': 22, 'hygiene': 33, 'fitness': 44, 'social': 55}, 'v 2 save should hold the needs')
    ev = load()
    v2 = json.loads(ev("JSON.stringify(SHIP.player.needs)")); print('  v 2 save:', v2)
    check(v2 == {'hunger': 11, 'energy': 22, 'hygiene': 33, 'fitness': 44, 'social': 55}, 'a v 2 save should load its needs')
    ev("localStorage.setItem(SAVE_KEY, JSON.stringify({ v: 2, build: 'x', time: { day: 2, min: 600 }, player: { deck: 4, tile: [7, 3], facing: 0, needs: { hunger: 'x', energy: 500 } }, ship: { decks: {} }, crew: {} })); Storage.prototype.setItem = () => {}")
    ev = load()
    bad = json.loads(ev("Storage.prototype.setItem = () => {}; JSON.stringify(SHIP.player.needs)")); print('  junk needs:', bad)
    check(bad == {'hunger': 80, 'energy': 100, 'hygiene': 80, 'fitness': 80, 'social': 80}, 'junk needs should be clamped or filled at 80')
    raw0 = ev("localStorage.getItem(SAVE_KEY)")
    ev = load('?nosave')
    ns = json.loads(ev("const n0 = NEED_KEYS.map(k => SHIP.player.needs[k]); SHIP.player.needs.hunger = 1; saveGame(); JSON.stringify([n0, localStorage.getItem(SAVE_KEY)])"))
    print('  ?nosave:', ns[0])
    check(ns[0] == [60, 100, 60, 70, 70], f'?nosave should start fresh: {ns[0]}')
    check(ns[1] == raw0, '?nosave should not write the save')
    ev("localStorage.removeItem(SAVE_KEY)")
    b.close()

print('errors', errors[:5])
if errors: fail('page errors')
print('PLAYER CHECK OK' if ok else 'PLAYER CHECK FAILED')
sys.exit(0 if ok else 1)
