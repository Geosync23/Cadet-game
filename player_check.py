# Starship Cadet: player check (keep in the repo, next to cadet_test.py, deck_check.py and day_check.py)
# Checks the player's needs and activities (section 15), deterministically:
#   on paper: a week of normal days (shower, two meals, the gym and a call home every other day, 8 hours' sleep)
#   keeps every need at 30 or more and the walking speed at 100%; a week of neglect never goes below 0 or above 100
#   the speed rule: fitness or energy under 25 walks at 80%, both at 64%, and you really do cover less ground
#   sleep: the bunk's Sleep refills energy; a time skip awake drains it; a night without sleep slows you
#   long days (0.28.9): a rested player stays up 16 to 18 ship hours before energy hits the tired line (17 at average
#   fitness); your bunk from 20:00 fades out and wakes you at 06:00 with no dialog, and earlier says it's too early
#   bonuses and penalties (needEffects, 0.28.9): the table, stacking, the device's marks, and tasks really going faster
#   mail (0.28.10): mailSend, the unread count on the button and the Mail tab, reading marks it read, the welcome on a
#   fresh start, saved and loaded; social from chatting (first chat a day, then a little, times socialGain) and from
#   company at the mess table; the store sells what you picked out for credits (snacks: food; comforts: the locker)
#   machines, carts, crawlways (0.28.11): a tap on a machine walks you up and shows machineUse's text; a restock job is a
#   hover-cart run you push (dock, hold, storage, dock: the hold lands on the shelves, you're paid, the cart in your
#   hands on the way); a crawl tile slows you to half speed in a crouch
#   sit anywhere (0.28.12): a tap on a public seat sits you there (the sit pose, at its height), rests you, and you get
#   up by walking; squeeze past (0.28.12): crew settled at their station no longer wall off the way to the galley plant
#   the treadmills (0.28.17, the user's report): a real click on each of the three (belt or console) walks you there,
#   you run on it (pose 'run'), its belt scrolls, and over a few ship minutes fitness rises and energy falls
#   in the game, one player day on the real decks, by tapping the real things: shower (Deck 4), servery tray then a
#   mess seat, grab shelf, treadmill (run), weights (lift), call-home booth (call), shelves then the counter
#   (browse, pay); each need rises by its gain, the pose is right, you're back on your feet and visible after
#   places held by crew are left alone ("In use"); the servery is closed between meals; walking away stops an
#   activity (keeping what you'd gained); someone's private wash pod isn't offered; draw calls stay under BUDGET
#   the bathroom need (0.28.19): toilets in the public washrooms (Decks 4 and 3) sit you down and fill it; cabins' are private
#   seeing it work (0.28.20, 0.28.21): each tapped activity shows the progress bar and a +N note for its need
#   the kit bag and the device lock (0.28.26): held from the ramp, into the locker in Bunk 1
#   lying down in your bunk (0.28.29): by day to rest, at night to sleep, and getting up
#   gifts (0.28.25): store gifts and machine-shop gifts into your hands (giftAdd); a friend's note on your bunk
#   a reserved training job (0.28.24): the shelf part, the bracket made in the machine shop with the bar, the stops marked, the repair
#   the note bus (0.28.22): simNote('act', ...) for wash, eat (with), call, buy; your name saved and cleaned
#   saving: a v 2 save keeps needs; a v 1 save loads with needs at 80; ?nosave neither reads nor writes
#   --long (0.28.41, the lead's save budget): only this: the whole save from the real arrival (newGameStart(true)) to
#   day 280 (or --long N), skipTo ten hours at a time, measured after each day's 06:00; prints the size and the biggest
#   parts every 10 days and fails if it ever passes SAVE_BUDGET (250 KB). About two minutes on a combined build.
# Setup and environment as for cadet_test.py.
# Run:  python3 player_check.py BUILD.html  [--long [DAYS]]
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
    if (d.need) n[d.need] = needClamp(n[d.need] + d.gain / d.mins + NEED_DRAIN[d.need][0] / 60);
    if (d.cost) for (const k in d.cost) n[k] = needClamp(n[k] - d.cost[k] / d.mins); look(); } };
  const sleep = mins => { needsDrain(mins, true); look(); };
  for (let day = 1; day <= 7; day++) {                    // 06:00 to 06:00
    if (normal) {
      act('toilet'); awake(57); act('shower'); awake(5); act('eat'); awake(25);   // 06:00-08:00 (the toilet: 0.28.19)
      awake(4 * 60); act('toilet'); awake(5 * 60 - 3);                            // the shift, 08:00-17:00, with a break at noon
      awake(30); act('eat'); act('toilet'); awake(37);                            // dinner about 17:30
      if (day % 2) act('gym'); else act('call');
      awake(22 * 60 - (18 * 60 + 30) - (day % 2 ? 30 : 15) - 3); act('toilet');   // to 22:00, and before bed
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
STATE = r"""JSON.stringify({ act: ACT && [ACT.kind, ACT.placeId, ACT.phase, ACT.pose, Math.round(ACT.done * 10) / 10, player.holding === undefined ? null : player.holding, typeof TRAY_ON !== 'undefined' && TRAY_ON.visible],
  needs: Object.fromEntries(NEED_KEYS.map(k => [k, Math.round(SHIP.player.needs[k] * 10) / 10])), basket,
  visible: player.obj.visible, toast: document.getElementById('tt').textContent + ': ' + document.getElementById('tx').textContent,
  time: hhmm(SHIP.time.min), calls: renderer.info.render.calls, deck: deckDef.num,
  bar: (b => b && !b.hidden ? b.textContent : null)(document.getElementById('actBar')), nf: typeof FLOAT_LOG === 'undefined' ? [] : FLOAT_LOG.splice(0) })"""

def state(g): return json.loads(g.ev(STATE))
UI = {}                                                   # per activity: progress-bar texts and floating notes seen (0.28.20, 0.28.21)

def servery_seat(g, label):
    """the servery's line (0.28.31): served, you hold your tray and get control back; then you tap a mess table yourself"""
    tp, b, seen, e, pk = run_activity(g, 'Servery', label=label)
    tray = g.ev("[SHIP.player.tray, player.holding, !!ACT]")
    print('  served, tray in hand, control back:', tray)
    if g.ev("typeof galleyJoin === 'function'") and any(a[0] == 'queue' for a in seen):
        check(isinstance(tray[0], str) and tray[1] == 'tray' and tray[2] is False, f'served: your tray in hand and control back ({tray})')
        # mess tables have no description of their own: you tap a seat, and playerFloorTap's line of sight finds it
        tp2 = g.ev("""(() => { const p = player.obj.position;
          const sp = [...PLACE_OF.values()].filter(q => q.type === 'mess-seat' && !heldBy(q.id)).map(q => placeSpot(q.id)).filter(Boolean)
            .sort((m, n) => Math.hypot(m.x - p.x, m.z - p.z) - Math.hypot(n.x - p.x, n.z - p.z))[0];
          const v = new THREE.Vector3(sp.x, .45, sp.z).project(camera); ray.setFromCamera(new THREE.Vector2(v.x, v.y), camera);
          return playerFloorTap(new THREE.Vector3(sp.x, 0, sp.z)); })()""")
        seen2, pk2 = [], 0
        for k in range(4000 // 30):
            g.step(30); st = state(g); pk2 = max(pk2, st['calls'])
            if st['act']: seen2.append(st['act'])
            if not st['act'] and k > 0: break
        g.step(30); e = state(g)
        print(f"  {label + ' (the seat)':22s} tapped={tp2!s:5s} {e['time']} needs {e['needs']}")
        check(tp2 is True and g.ev("SHIP.player.tray") is None and any(a[0] == 'eat' for a in seen2), f'a tap on a mess seat with your tray: sit and eat ({tp2})')
        seen, pk = seen + seen2, max(pk, pk2)
    return tp, b, seen, e, pk

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
        u = UI.setdefault(label or title, {'bar': [], 'nf': set()})
        if s['bar'] and s['bar'] not in u['bar']: u['bar'].append(s['bar'])
        u['nf'].update(s['nf'])
        if not s['act'] and k > 0: break
    g.step(30)                                            # the last +N note shows just after (once the rise has stopped)
    end = state(g); UI.setdefault(label or title, {'bar': [], 'nf': set()})['nf'].update(end['nf'])
    if not any(x[2] == 'do' for x in seen) and re.match(r"In use|There's a queue", end['toast'].split(': ', 1)[1]) and limit > 0:
        print('   ', title, 'taken on arrival:', end['toast'][:80]); g.step(190)
        return run_activity(g, title, near, limit - 1000, label)
    if os.environ.get('PC_DEBUG'): print(seen[:3], seen[-3:], end)
    print(f"  {label or title:22s} tapped={tapped!s:5s} poses={sorted(set(a[3] for a in seen if a[2] == 'do'))} "
          f"{end['time']} needs {end['needs']} calls<={peak}")
    return tapped, before, seen, end, peak

def body_check(name, need, gain, before, end, seen, pose):
    if pose: check(any(a[2] == 'do' and a[3] in ((pose,) if isinstance(pose, str) else pose) for a in seen), f'{name}: pose {pose} not taken ({sorted(set(str(a[3]) for a in seen))})')
    if need: check(end['needs'][need] >= min(99.5, before['needs'][need] + gain - 3) - .1, f"{name}: {need} {before['needs'][need]} -> {end['needs'][need]} (gain {gain})")
    check(end['visible'] and not end['act'], f'{name}: not back on your feet ({end})')

SAVE_BUDGET = 250 * 1024                                  # the whole save at any point to day 280 (the lead, 0.28.41)
SAVE_SIZE = r"""(() => { saveGame(); const raw = localStorage.getItem(SAVE_KEY) || '', s = JSON.parse(raw || '{}'), out = { total: raw.length };
  for (const k in s) { if ((k === 'ship' || k === 'player') && s[k] && typeof s[k] === 'object') { for (const j in s[k]) out[k + '.' + j] = JSON.stringify(s[k][j]).length; } else out[k] = JSON.stringify(s[k]).length; }
  return JSON.stringify(out); })()"""
def save_budget(pw, path, days):
    """the whole save from the real arrival to day `days`: the largest size seen, and its parts"""
    tmp = WORK / 'test' / '_save_budget.html'; tmp.write_text(instrument(pathlib.Path(path).read_text()))
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    page = b.new_page(viewport={'width': 600, 'height': 500}); errs = []
    page.on('pageerror', lambda e: errs.append(f'pageerror: {e}'))
    page.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
    page.add_init_script(INIT)
    def load():
        page.goto('file://' + str(tmp)); page.wait_for_function('window.__sc !== undefined', timeout=60000)
    ev = lambda s: page.evaluate('s => window.__sc(s)', s)
    load(); ev("localStorage.clear()"); load()                # saving on (no ?nosave), from an empty store
    if not ev("typeof newGameStart === 'function' && typeof skipTo === 'function'"):   # this branch alone: no arrival (section 13) to start from
        print('  this build has no newGameStart / skipTo (section 13): skipped'); b.close(); return (0, 0, {}), errs
    print('  arrival:', ev("(() => { newGameStart(true); return JSON.stringify([SHIP.time.day, hhmm(SHIP.time.min), typeof introOn === 'function' && introOn()]); })()"))
    worst = (0, 0, {})
    for d in range(1, days + 1):
        ev(f"(() => {{ const end = {d} * 1440 + 360; while (shipNow() < end) skipTo(Math.min(end, shipNow() + 600)); }})()")
        sz = json.loads(ev(SAVE_SIZE))
        if sz['total'] > worst[0]: worst = (sz['total'], d, sz)
        if d % 10 == 0 or d == days:
            top = sorted(((v, k) for k, v in sz.items() if k != 'total'), reverse=True)[:6]
            print(f"  day {d:3d} {sz['total'] / 1024:6.1f} KB  biggest: " + ', '.join(f'{k} {v / 1024:.1f}' for v, k in top), flush=True)
    ev("localStorage.clear()"); b.close()
    return worst, errs

if '--long' in sys.argv:
    k = sys.argv.index('--long'); days = int(sys.argv[k + 1]) if len(sys.argv) > k + 1 and sys.argv[k + 1].isdigit() else 280
    print(f'The whole save, from the real arrival to day {days} (budget {SAVE_BUDGET // 1024} KB):')
    with sync_playwright() as pw:
        (big, day, parts), errs = save_budget(pw, sys.argv[1], days)
    print(f'  largest: {big / 1024:.1f} KB on day {day}:', ', '.join(f'{k} {v / 1024:.1f}' for k, v in sorted(parts.items(), key=lambda x: -x[1]) if k != 'total' and v >= 512))
    check(big <= SAVE_BUDGET, f'the whole save passed {SAVE_BUDGET // 1024} KB: {big / 1024:.1f} KB on day {day}')
    if errs: fail('page errors: ' + '; '.join(errs[:3]))
    print('SAVE BUDGET OK' if ok else 'SAVE BUDGET FAILED')
    sys.exit(0 if ok else 1)

with sync_playwright() as pw:
    g = Game(pw, sys.argv[1])
    errors = g.errors

    print('On paper, a week of normal days:')
    p = g.ev(f"({PAPER})({{ normal: true }})"); print('  lowest', p['lo'], 'slow minutes', p['slowMins'])
    for k, v in p['lo'].items(): check(v >= (25 if k in ('energy', 'bathroom') else 30), f'normal week: {k} fell to {v}')
    check(p['slowMins'] == 0, f"normal week: slowed for {p['slowMins']} minutes")
    print('On paper, a week of neglect:')
    p = g.ev(f"({PAPER})({{ normal: false }})"); print('  end', p['end'], 'lowest', p['lo'], 'highest', p['hi'])
    check(all(0 <= p['lo'][k] and p['hi'][k] <= 100 for k in p['lo']), 'neglect: a need left 0-100')
    check(p['end']['fitness'] < 25 and p['end']['hunger'] == 0, 'neglect: fitness and hunger should be low')

    print('The speed rule:')
    sp = g.ev(r"""(() => { const n = SHIP.player.needs, out = {};
      const walk = () => { Object.assign(player.obj.position, cellPos(...nearestOpen(LIFT_AT[0], LIFT_AT[1], player))); player.steer = { x: 0, z: 1, k: 1 }; player.vel = 0;
        for (let k = 0; k < 20; k++) { playerUpdate(.05, 0); player.update(.05, 0); } player.steer = null; return player.vel; };
      for (const [f, e] of [[80, 80], [20, 80], [80, 20], [20, 20], [25, 25]]) { Object.assign(n, { fitness: f, energy: e, bathroom: 50 }); playerUpdate(0, 0);
        out[f + '/' + e] = [Math.round(playerSpeed() * 1000) / 1000, Math.round(player.maxV / PLAYER_V0 * 1000) / 1000, Math.round(walk() / PLAYER_V0 * 1000) / 1000]; }
      Object.assign(n, NEEDS_FRESH); playerUpdate(0, 0); return out; })()""")
    print('  fitness/energy: [speed, top speed ratio, walking speed reached after 1 s, as a ratio]', sp)
    for key, want in [('80/80', 1.05), ('20/80', .8), ('80/20', .84), ('20/20', .64), ('25/25', 1)]:   # fit (75+): 105% (0.28.9)
        check(abs(sp[key][0] - want) < 1e-9 and abs(sp[key][1] - want) < 1e-3, f'speed {key}: {sp[key]} want {want}')
    for key in sp: check(abs(sp[key][2] - sp[key][0]) < .01, f'speed {key}: walking at {sp[key][2]}, want {sp[key][0]}')
    # bursting for the toilet (0.28.41, the user's): at bathroom 0 the '+go' pose (no prop: no new meshes) and 70% walking; above 0, gone
    bg = g.ev(r"""(() => { const n = SHIP.player.needs, out = [];
      const walk = () => { Object.assign(player.obj.position, cellPos(...nearestOpen(LIFT_AT[0], LIFT_AT[1], player))); player.steer = { x: 0, z: 1, k: 1 }; player.vel = 0;
        for (let k = 0; k < 20; k++) { playerUpdate(.05, 0); player.update(.05, 0); } player.steer = null; return player.vel; };
      for (const b of [0, .5]) { Object.assign(n, { fitness: 50, energy: 50, hunger: 50, bathroom: b }); const v = walk() / PLAYER_V0;
        out.push([Math.round(playerSpeed() * 1000) / 1000, Math.round(v * 100) / 100, !!player.needGo, Math.round((player.k && player.k['+go'] || 0) * 100) / 100, (player.propMeshes || []).length, needEffects().marks.bathroom[1].slice(0, 8)]); }
      Object.assign(n, NEEDS_FRESH); playerUpdate(0, 0); return JSON.stringify(out); })()""")
    bg = json.loads(bg); print('  bathroom 0, then 0.5: [speed, walked, needGo, the pose blend, prop meshes, the device note]', bg)
    check(bg[0][:3] == [.7, .7, True] and bg[0][3] > .9 and bg[0][4] == 0 and bg[0][5] == 'Bursting', f"bathroom 0: hold yourself ('+go', no prop) and walk at 70%: {bg[0]}")
    check(bg[1][:3] == [1, 1, False] and bg[1][3] < .1 and bg[1][5] != 'Bursting', f'bathroom above 0: the pose and the slow walk end: {bg[1]}')

    print('Pause (0.28.48, the user\'s "Need a pause button"):')
    S1 = "JSON.stringify([SHIP.time.day, Math.round(SHIP.time.min * 1000) / 1000, Math.round(SHIP.player.needs.hunger * 1000) / 1000, player.obj.position.x.toFixed(3), player.obj.position.z.toFixed(3)])"
    g.ev("(() => { actEnd(true); const c = cellPos(...player.here()), n = nearestOpen(c.x + 1.2, c.z, player); if (n) playerGo(n, null); })()"); g.step(3)
    pz = json.loads(g.ev("(() => { POP.tip = performance.now() - 1000; const t0 = POP.tip; pauseSet(true); return JSON.stringify([t0, PAUSE.on, getComputedStyle(document.getElementById('pauseCard')).display !== 'none', document.querySelector('#pauseBtn span').textContent]); })()"))
    a0 = g.ev(S1); g.step(90); a1 = g.ev(S1)
    rs = json.loads(g.ev("(() => { const t = performance.now(), d = t - PAUSE.since; pauseSet(false); return JSON.stringify([PAUSE.on, getComputedStyle(document.getElementById('pauseCard')).display === 'none', Math.round(POP.tip - " + str(pz[0]) + " - d)]); })()"))
    g.step(60); a2 = g.ev(S1)
    print('  paused [on, overlay, button]:', pz[1:], '| before, after 3 s paused, 2 s after resuming:', a0, a1, a2, '| resumed [on, overlay hidden, tips gap moved by the pause]:', rs)
    check(pz[1:] == [True, True, 'Resume'] and a0 == a1, f'paused: the overlay shows, ship time, needs and you stand still: {a0} {a1}')
    check(rs == [False, True, 0] and json.loads(a2)[1] != json.loads(a1)[1], f'resumed: the overlay goes, time runs again, the pacing stamps moved on by the pause: {rs} {a2}')
    g.ev("player.stop(); actEnd(true)"); g.step(30)

    print('Walking speed on arrival (0.28.47, the user\'s "walking very slowly at the start"):')
    ar = g.ev(r"""(() => { if (typeof sickNow !== 'function' || typeof careerInit !== 'function') return null;
      const t0 = shipNow(), c = careerInit(), keep = { sd: c.sd, sh: c.sh }, n = SHIP.player.needs, n0 = { ...n }; Object.assign(n, NEEDS_FRESH);
      setShipNow(-1440 + 17 * 60 + 30); c.sd = 0; c.sh = 0; const a = [SHIP.time.day, sickNow(), playerSpeed(), needEffects().notes.some(x => /unwell/.test(x))];
      setShipNow(5 * 1440 + 12 * 60); c.sd = SHIP.time.day; c.sh = 0; const b = [sickNow(), playerSpeed() < 1];   // a real sick day still counts
      Object.assign(c, keep); setShipNow(t0); Object.assign(n, n0); return JSON.stringify([a, b]); })()""")
    if ar is None: print('  (no career section in this build)')
    else:
        ar = json.loads(ar); print('  day 0 at 17:30 [day, unwell, speed, an unwell note]; a real sick day [unwell, slower]:', ar)
        check(ar[0] == [0, False, 1, False] and ar[1] == [True, True], f'a new arrival is not "unwell" (a sick day 0 meant never): full speed at 17:30 on day 0: {ar}')

    print('No tray, no meal (0.28.45, the user\'s):')
    def table_go(tray):
        g.ev(f"""(() => {{ actEnd(true); if (deckDef.num !== 3) goToDeck(3); setShipNow(Math.floor(shipNow() / 1440) * 1440 + 18 * 60 + 5); needsT = null;
          SHIP.player.tray = {json.dumps(tray)}; Object.assign(SHIP.player.needs, {{ hunger: 40, energy: 60, hygiene: 60, fitness: 60, social: 60, bathroom: 60 }});
          const it = ITEMS.find(i => /^Long table$/.test(i.t)), q = new THREE.Vector3(); it.hit.getWorldPosition(q); return playerTap(it, q, q); }})()""")
        for k in range(200):
            g.step(10)
            if g.ev("!ACT || ACT.phase === 'do'"): break
        h0 = g.ev("SHIP.player.needs.hunger"); r0 = g.ev("JSON.stringify([ACT && ACT.kind, ACT && !!ACT.o.fed, TRAY_ON.visible, SHIP.player.tray])")
        g.step(150)
        h1 = g.ev("SHIP.player.needs.hunger"); r = json.loads(r0) + [round(h1 - h0, 1), g.ev("TRAY_ON.visible")]
        g.ev("actEnd(true); SHIP.player.tray = null"); return r
    nt = table_go(None); wt = table_go('Test soup')
    print('  a table, no tray: [activity, fed, tray on the table, tray in hand, food change, tray later]', nt)
    print('  a table with a served tray:', wt)
    check(nt[0] == 'sit' and nt[1] is False and nt[2] is False and nt[4] <= 0 and nt[5] is False, f'sitting at a mess table without a meal: just sitting, no tray, no food: {nt}')
    check(wt[0] == 'eat' and wt[1] is True and wt[2] is True and wt[3] is None and wt[4] > 1, f'with a tray from the servery: it goes on the table and food rises as you eat: {wt}')

    print('Need warnings (0.28.41):')
    wn = json.loads(g.ev(r"""(() => { const n = SHIP.player.needs, out = [], te = document.getElementById('toast');
      let t = performance.now() + 1e6;
      const quiet = () => { POP.toast = POP.card = POP.warn = -1e9; POP.busy = false; te.classList.remove('show'); TOAST_AT = -1e9; };
      const tick = (gap = true) => { if (gap) quiet(); t += 1000; const k = needWarnTick(t); return k ? [k, document.getElementById('tt').textContent] : null; };
      deviceClose(); TIP_Q.length = 0; DEVICE_SKIN.tip(null); WARN_SAID = {}; Object.assign(n, { hunger: 60, energy: 60, hygiene: 60, fitness: 60, social: 60, bathroom: 60 });
      out.push(tick());                                      // 0 nothing low
      n.hunger = 24; out.push(tick(), tick(false), tick());  // 1 the gentle one, 2 not again at once, 3 nor later
      n.hunger = 9; out.push(tick());                        // 4 the firm one
      n.hunger = 30; tick(); n.hunger = 20; out.push(tick()); // 5 not re-armed at 30
      n.hunger = 45; tick(); n.hunger = 20; out.push(tick()); // 6 re-armed at 40+
      n.hunger = 20; n.bathroom = 5; n.social = 22; out.push(tick(), tick(false), tick(), tick());   // 7-10 lowest first, one at a time (food already said)
      n.energy = 20; DEV.open = true; out.push(tick()); DEV.open = false;   // 11 not with the device open
      quiet(); POP.busy = true; t += 1000; out.push(needWarnTick(t)); // 12 not while busy
      sleeping = true; POP.at = -1e9; popupWatch(t); out.push(POP.busy); sleeping = false; POP.at = -1e9; popupWatch(t + 1); out.push(POP.busy);   // 13, 14
      out.push(JSON.stringify([POP_PANELS.filter(popOn), !!ride, !!DEV.choose, TIP_Q.length, document.body.classList.contains('dlgon')]));   // 15: what's busy, if anything
      out.push(tick());                                      // 16 energy now
      WARN_SAID = {}; Object.assign(n, NEEDS_FRESH); return JSON.stringify(out); })()"""))
    for i, x in enumerate(wn): print('   ', i, x)
    check(wn[0] is None and wn[1] == ['hunger', 'Hungry'] and wn[2] is None and wn[3] is None, f'a gentle warning once when food drops under 25: {wn[:4]}')
    check(wn[4] == ['hunger', 'Very hungry'] and wn[5] is None and wn[6] == ['hunger', 'Hungry'], f'a firmer one under 10; re-armed only at 40+: {wn[4:7]}')
    check(wn[7] == ['bathroom', 'Bursting'] and wn[8] is None and wn[9] == ['social', 'A bit lonely'] and wn[10] is None, f'the lowest need first, one at a time, after a gap: {wn[7:11]}')
    check(wn[11] is None and wn[12] is None and wn[13] is True and wn[14] is False and wn[16] == ['energy', 'Tired'], f'never with the device open, while busy or asleep: {wn[11:]}')
    # and in the running game: food under 25 says so within a few seconds once the screen is quiet
    g.ev("WARN_SAID = {}; POP.toast = POP.card = POP.warn = -1e9; document.getElementById('toast').classList.remove('show'); TOAST_AT = -1e9; deviceClose(); TIP_Q.length = 0; DEVICE_SKIN.tip(null); Object.assign(SHIP.player.needs, { hunger: 20, energy: 60, hygiene: 60, fitness: 60, social: 60, bathroom: 60 })")
    g.step(30)
    wl = json.loads(g.ev("JSON.stringify([WARN_SAID.hunger || 0, document.getElementById('tt').textContent])")); print('  in the game:', wl)
    check(wl == [1, 'Hungry'], f'the warning shows in the running game: {wl}')
    g.ev("WARN_SAID = {}; Object.assign(SHIP.player.needs, NEEDS_FRESH)")

    print('Teaching tips (0.28.42):')
    tt = json.loads(g.ev(r"""(() => { const D = SHIP.device, keep = { ...D.tipsSeen }, tipsOn = D.settings.tips, intro = SHIP.intro && { ...SHIP.intro }, out = {};
      const ids = TEACH.map(x => x[0]); out.list = [ids.length, new Set(ids).size, Math.max(...ids.map(x => x.length)), Math.max(...TEACH.map(x => x[2].length))];
      let t = performance.now() + 5e6;
      const clear = () => { TIP_Q.length = 0; DEVICE_SKIN.tip(null); };
      const quiet = () => { clear(); Object.assign(POP, { toast: -1e9, card: -1e9, warn: -1e9, tip: -1e9, busy: false, panels: false }); document.getElementById('toast').classList.remove('show'); TOAST_AT = -1e9; };
      const tick = () => { t += 1000; POP.busy = false; return teachTick(t); };
      if (SHIP.intro) SHIP.intro.ended = true; deviceClose(); D.settings.tips = true;
      for (const id of ids) delete D.tipsSeen[id];
      Object.assign(SHIP.player.needs, { hunger: 40, energy: 60, hygiene: 60, fitness: 60, social: 60, bathroom: 60 });
      quiet(); const a = tick(); out.first = [a, !!D.tipsSeen[a], TIP_Q.length && TIP_Q[0].id, document.getElementById('devTip') && !document.getElementById('devTip').hidden];
      quiet(); POP.tip = t; out.gap = [tick()];                              // 3 minutes between tips
      clear(); POP.card = POP.tip = t - 181000; POP.card = t - 30000; out.gap.push(tick());   // a card 30 s ago: not yet
      POP.card = t - 61000; const b = tick(); out.gap.push(b, b && b !== a);  // 61 s: the next one
      quiet(); POP.toast = t - 3000; out.gap.push(tick());                   // a toast 3 s ago
      const seen0 = ids.filter(k => D.tipsSeen[k]).length; quiet(); D.settings.tips = false; out.off = [tick(), ids.filter(k => D.tipsSeen[k]).length - seen0]; D.settings.tips = true;
      if (SHIP.intro) { SHIP.intro.on = true; SHIP.intro.ended = false; SHIP.intro.step = 'chief'; quiet(); out.intro = tick(); SHIP.intro.step = null; SHIP.intro.ended = true; }
      for (const id of ids) D.tipsSeen[id] = true; delete D.tipsSeen['t:rep']; quiet(); POP.tip = t; TEACH_ST.turnin = undefined; const m0 = SHIP.time.min, d0 = SHIP.time.day; SHIP.time.day = 1; SHIP.time.min = 600;
      out.rep = [SHIP.time.day, tick()]; TEACH_ST.turnin = shipNow() - 10; out.rep.push(tick() || 'not yet'); TEACH_ST.turnin = shipNow() - 40; out.rep.push(tick()); delete D.tipsSeen['t:rep']; TEACH_ST.turnin = undefined; SHIP.time.min = 1030; quiet(); POP.tip = t; out.rep.push(tick()); SHIP.time.min = m0; SHIP.time.day = d0;
      for (const id of ids) delete D.tipsSeen[id];
      quiet(); DEV.open = true; DEV.app = 'home'; out.dev = [tick()]; DEV.app = 'needs'; quiet(); out.dev.push(tick()); DEV.open = false; DEV.app = 'home';
      for (const id of ids) D.tipsSeen[id] = true; delete D.tipsSeen['t:queue']; delete D.tipsSeen['t:needs'];
      const was = ACT; ACT = { kind: 'queue', o: {}, def: {} }; quiet(); out.prio = [tick()]; ACT = was; quiet(); out.prio.push(tick());
      out.size = JSON.stringify(D.tipsSeen).length;
      for (const id of ids) delete D.tipsSeen[id]; Object.assign(D.tipsSeen, keep); D.settings.tips = tipsOn; if (intro) Object.assign(SHIP.intro, intro);
      clear(); Object.assign(SHIP.player.needs, NEEDS_FRESH); return JSON.stringify(out); })()"""))
    for k in tt: print('   ', k, tt[k])
    check(tt['list'][0] >= 25 and tt['list'][0] == tt['list'][1] and tt['list'][2] < 12 and tt['list'][3] <= 200, f'25+ tips, unique short ids, short texts: {tt["list"]}')
    check(str(tt['first'][0]).startswith('t:') and tt['first'][1] is True and tt['first'][2] == tt['first'][0] and tt['first'][3] is True, f'a due tip shows on the card and is marked seen: {tt["first"]}')
    check(tt['gap'][0] is None and tt['gap'][1] is None and tt['gap'][3] is True and tt['gap'][4] is None, f'pacing: 3 minutes apart, 60 s after a card, not just after a toast: {tt["gap"]}')
    check(tt['off'] == [None, 0], f'Tips off: none shown, none marked seen: {tt["off"]}')
    check(tt.get('intro') is None, f'none during the arrival: {tt.get("intro")}')
    check(tt['rep'] == [1, None, 'not yet', 't:rep', 't:rep'], f'the reputation tip on Monday: after your first job is turned in, or at 17:00, whatever the pacing: {tt["rep"]}')
    check(tt['dev'] == [None, 't:a-needs'], f'over the device only the open app\'s tip: {tt["dev"]}')
    check(tt['prio'] == ['t:queue', 't:needs'], f'the first due tip in priority order: {tt["prio"]}')
    check(tt['size'] < 800, f'all the tips seen fit in a small save: {tt["size"]} bytes')

    print('The News feed (0.28.44):')
    nf = json.loads(g.ev(r"""(() => { const out = {}, added = [], keep = { news: SHIP.news, used: SHIP.newsUsed, at: SHIP.newsAt, rows: SHIP.newsRows };
      for (const k of Object.keys(NEWS_SRC)) if (!LINES['news.' + k]) { added.push(k);   // stand-ins until head writer 3's bank is in the build
        LINES['news.' + k] = Array.from({ length: 12 }, (_, i) => ({ text: NEWS_SRC[k] + ' post ' + i + ' about {first}.', id: 'tn' + k + i }));
        if (k === 'trad') LINES['news.trad'].push({ text: 'On today: {trad}. Come along.', id: 'tntoday', trad: 'today' }); }
      SHIP.news = []; SHIP.newsUsed = []; SHIP.newsAt = null; SHIP.newsRows = {};
      const d0 = SHIP.time.day + 1, days = 14, per = {}; let t = (d0 - 1) * 1440;
      newsTick(t); for (let h = 1; h <= days * 24; h++) { t += 60; newsTick(t);
        for (const x of SHIP.news) { const d = Math.floor(x.at / 1440) + 1; ((per[d] = per[d] || {})[x.at + '|' + x.text] = x); } }
      const counts = [], srcMax = [], ids = {};
      for (let d = d0; d < d0 + days; d++) { const xs = Object.values(per[d] || {}); counts.push(xs.length);
        const c = {}; for (const x of xs) if (x.src !== 'trad' && x.src !== 'works') c[x.src] = (c[x.src] || 0) + 1; srcMax.push(Math.max(0, ...Object.values(c)));
        for (const x of xs) if (x.id) (ids[x.id] = ids[x.id] || []).push(d); }
      out.counts = counts; out.srcMax = Math.max(...srcMax);
      out.repeat = Object.values(ids).some(ds => ds.some((d, i) => i > 0 && d - ds[i - 1] < NEWS_COOL));
      out.kept = SHIP.news.length; out.sources = [...new Set(SHIP.news.map(x => x.src))].length;
      out.sorted = SHIP.news.every((x, i) => !i || SHIP.news[i - 1].at >= x.at);
      const sv = {}; for (const f of SAVE_EXTRA) try { f(sv); } catch (e) { /* not ours */ } out.bytes = JSON.stringify([sv.news, sv.newsUsed, sv.newsAt, sv.newsRows]).length;
      deviceShow('ship'); const body = document.getElementById('devBody').textContent; out.app = [DEVICE_APPS.get('ship').title, !!SHIP.news[0] && body.includes(SHIP.news[0].text), body.includes('Systems')];
      deviceShow('crew'); out.rel = DEVICE_APPS.get('crew').title; deviceClose();
      const tp = SHIP.news.filter(x => x.id === 'tntoday'); out.trad = tp.length ? tp.every(x => !/-/.test(x.text) && /On today: [a-z]/.test(x.text)) : SHIP.news.some(x => /^Today aboard/.test(x.text)) || null; out.tradText = tp.length ? tp[0].text : null;
      for (const k of added) delete LINES['news.' + k]; Object.assign(SHIP, { news: keep.news, newsUsed: keep.used, newsAt: keep.at, newsRows: keep.rows });
      return JSON.stringify(out); })()"""))
    print('  ', nf)
    c = nf['counts']
    check(min(c) >= 2 and max(c) <= 10 and 3 <= sum(c) / len(c) <= 8, f'about 3 to 8 posts a ship day: {c}')
    check(nf['srcMax'] <= 2 and not nf['repeat'] and nf['sources'] >= 5, f'at most 2 a source a day, no post again within 7 days, a mix of sources: {nf}')
    check(nf['kept'] == 40 and nf['sorted'] and nf['bytes'] < 9000, f'the last 40 kept, newest first, small in the save: {nf["kept"]}, {nf["bytes"]} bytes')
    check(nf['trad'] is True, f"tradition posts name it, not its id (reviewer 1e): {nf.get('tradText')}")
    check(nf['app'] == ['News feed', True, True] and nf['rel'] == 'Relationships', f'the apps renamed; the feed and the system bars show: {nf["app"]}, {nf["rel"]}')
    # in the running game: with the screen quiet (heads-ups paused), a due tip comes up on its own
    g.ev("for (const x of TEACH) delete SHIP.device.tipsSeen[x[0]]; SHIP.device.calendarRemind.on = false; SHIP.device.settings.tips = true; TEACH_CK = -1e9; WARN_SAID = {}; Object.assign(SHIP.player.needs, { hunger: 45, energy: 60, hygiene: 60, fitness: 60, social: 60, bathroom: 60 }); Object.assign(POP, { toast: -1e9, card: -1e9, warn: -1e9, tip: -1e9 }); document.getElementById('toast').classList.remove('show'); TOAST_AT = -1e9; TIP_Q.length = 0; DEVICE_SKIN.tip(null); deviceClose()")
    g.step(90)
    tg = json.loads(g.ev("JSON.stringify([TIP_Q.map(x => x.id), !document.getElementById('devTip').hidden])")); print('  in the game:', tg)
    check(len(tg[0]) == 1 and tg[0][0].startswith('t:') and tg[1], f'a due tip shows by itself in the running game: {tg}')
    g.ev("TIP_Q.length = 0; DEVICE_SKIN.tip(null); SHIP.device.calendarRemind.on = true; for (const x of TEACH) delete SHIP.device.tipsSeen[x[0]]")

    print('Sleep and time skips:')
    sl = g.ev(r"""(() => { const n = SHIP.player.needs; Object.assign(n, NEEDS_FRESH); setShipNow(22 * 60); needsT = null; playerUpdate(0, 0);
      n.energy = 40; sleeping = true; sleepUntil(WAKE_AT); sleeping = false; const slept = n.energy;
      skipTo(shipNow() + 21 * 60); const awake = n.energy; n.bathroom = 50; playerUpdate(0, 0);   // bursting would slow you too (0.28.41)
      return { slept: Math.round(slept), awake21h: Math.round(awake), speed: playerSpeed(), at: clockText() }; })()""")
    print(' ', sl)
    check(sl['slept'] == 100, 'sleep should refill energy')
    check(sl['awake21h'] < 25 and abs(sl['speed'] - .8) < 1e-9, 'twenty-one hours awake should slow you')

    print('Long days (energy from 100 to the tired line, awake):')
    ld = g.ev(r"""(() => { const n = SHIP.player.needs, out = {};
      for (const f of [20, 50, 80]) { Object.assign(n, { hunger: 50, energy: 100, hygiene: 50, fitness: f, social: 50 }); let m = 0;
        while (n.energy >= 25 && m < 2000) { const keep = { hunger: 50, hygiene: 50, fitness: f, social: 50 }; needsDrain(1, false); Object.assign(n, keep); m++; }
        out[f] = Math.round(m / 6) / 10; }
      Object.assign(n, NEEDS_FRESH); return out; })()""")
    print('  hours awake by fitness (food, hygiene, social held at 50):', ld)
    check(abs(ld['50'] - 17) <= .3, f"average fitness should last about 17 hours, not {ld['50']}")
    check(15.8 <= ld['20'] <= 18.2 and 15.8 <= ld['80'] <= 18.2 and ld['20'] < ld['50'] < ld['80'], f'16 to 18 hours whatever your fitness: {ld}')

    print('Needs give bonuses and penalties (needEffects):')
    ne = g.ev(r"""(() => { const r = x => Math.round(x * 1000) / 1000, f = n => { const e = needEffects(n); return [r(e.walk), r(e.task), r(e.drain), r(e.socialGain), Object.keys(e.marks).sort().join(',')]; };
      return { mid: f({ hunger: 50, energy: 50, hygiene: 50, fitness: 50, social: 50 }), high: f({ hunger: 80, energy: 80, hygiene: 80, fitness: 80, social: 80 }),
        low: f({ hunger: 10, energy: 10, hygiene: 10, fitness: 10, social: 10 }), edge: f({ hunger: 75, energy: 25, hygiene: 74.9, fitness: 24.9, social: 50 }) }; })()""")
    print('  [walk, task, drain, socialGain, marks]', ne)
    check(ne['mid'] == [1, 1, 1, 1, ''], f"in between, nothing: {ne['mid']}")
    check(ne['high'][:4] == [1.05, 1.265, .902, 1.5] and ne['high'][4] == 'energy,fitness,hunger,hygiene,social', f"all high: {ne['high']}")
    check(ne['low'][:4] == [.64, .85, 1.113, .5] and ne['low'][4] == 'energy,fitness,hunger,hygiene,social', f"all low: {ne['low']}")
    check(ne['edge'] == [.8, 1, 1.018, 1, 'fitness,hunger'], f"75 counts as high, 25 isn't low: {ne['edge']}")
    dv = g.ev(r"""(() => { Object.assign(SHIP.player.needs, { hunger: 80, energy: 50, hygiene: 10, fitness: 50, social: 50 }); device.open('needs');
      const b = document.getElementById('devBody'), out = [[...b.querySelectorAll('.need em')].map(e => e.className + ':' + e.textContent), [...b.querySelectorAll('p.fx')].map(p => p.textContent)];
      device.close(); Object.assign(SHIP.player.needs, NEEDS_FRESH); return out; })()""")
    print('  the device:', dv)
    check(dv[0] == ['up:▲', 'down:▼'] and len(dv[1]) == 2 and sorted(['fed' if 'fed' in x else 'wash' if 'wash' in x.lower() else x for x in dv[1]]) == ['fed', 'wash'], f'device marks (either order; device 0.35.28 lists penalties first): {dv}')

    tk = g.ev(r"""(() => { const n = SHIP.player.needs, out = [];
      for (const st of [{ energy: 100, social: 50, hunger: 50 }, { energy: 50, social: 50, hunger: 10 }, { energy: 50, social: 50, hunger: 50 }]) {
        Object.assign(n, st); ACT = { kind: 'gym', def: PLAYER_ACTS.gym, phase: 'do', done: 0, o: {}, deck: deckDef, x: 0, z: 0, y: 0, face: player.face, to: {}, body: { set() {}, update() {}, dispose() {} } };
        needsT = shipNow() - 10; playerUpdate(0, 0); out.push(Math.round(ACT.done * 100) / 100); }
      ACT = null; Object.assign(n, NEEDS_FRESH); return out; })()""")
    print('  ten ship minutes of a workout count as (rested, hungry, neither):', tk)
    check(tk == [11.5, 8.5, 10], f'tasks should go 15% faster rested and 15% slower hungry: {tk}')

    print('Going to bed (your bunk, no dialog):')
    BED = "(() => { const id = playerBed(), b = DECKS[4].places.find(p => p.id === id); return offerSleep(cellPos(...b.at)); })()"
    g.ev("goToDeck(4); setShipNow(Math.floor(shipNow() / 1440) * 1440 + 1440 + 14 * 60); needsT = null"); g.step(3)
    early = [g.ev(BED), g.ev("document.getElementById('tx').textContent"), g.ev("clockText()")]; print('  at 14:00:', early)
    check(early[0] is True and 'Too early' in early[1] and early[2].endswith('14:00'), f'the bunk before 20:00 should say it is too early: {early}')
    # a friend's note on your bunk (0.28.25, section 20's bunkNote; a stand-in when it's missing): the first tap reads it, the next is the bunk as before
    BTAP = "(() => { const id = playerBed(), b = cellPos(...DECKS[4].places.find(p => p.id === id).at); const it = ITEMS.map(i => { i.hit.getWorldPosition(_wp); return [i, _wp.clone()]; }).sort((m, n) => m[1].distanceTo(b) - n[1].distanceTo(b))[0]; return playerTap(it[0], it[1].clone(), it[1].clone()); })()"
    stubn = g.ev("(() => { if (typeof bunkNote === 'function') return false; let left = 1; window.bunkNote = () => left-- > 0 ? { from: 'Tomas Reyes', text: 'Left you the good pillow.' } : null; return true; })()")
    notes = []
    for k in range(2):
        tp = g.ev(BTAP)
        for j in range(60):
            g.step(10)
            if not g.ev("player.path.length > 0"): break
        g.step(5); notes.append([tp, g.ev("document.getElementById('tt').textContent + ': ' + document.getElementById('tx').textContent")])
    if stubn: g.ev("delete window.bunkNote")
    print('  your bunk with a note, then again:', notes)
    if stubn: check(notes[0][0] is True and notes[0][1].startswith('A note on your bunk') and 'lie down' in notes[1][1], f"the bunk: a friend's note first, then the bunk as before ({notes})")
    # lying down (0.28.29, the user's "I can't lay down in bed"): a tap on your bunk by day lies you down in it to rest;
    # walking off gets you up; at night you lie down, sleep to 06:00 and wake still lying there
    for j in range(40):
        g.step(10)
        if g.ev("!!ACT && ACT.phase === 'do'"): break
    ly = g.ev("[ACT && ACT.kind, ACT && ACT.phase, ACT && ACT.pose, ACT && ACT.placeId === playerBed(), ACT && +ACT.y.toFixed(2), player.obj.visible]")
    g.ev("SHIP.player.needs.energy = 50"); e0 = g.ev("SHIP.player.needs.energy"); g.ev("setShipNow(shipNow() + 60)"); g.step(3); e1 = g.ev("SHIP.player.needs.energy")
    print('  lying down by day:', ly, 'energy over an hour:', round(e0, 2), '->', round(e1, 2))
    check(ly[:4] == ['lie', 'do', 'lie', True] and ly[4] > .2 and ly[5] is False, f'a tap on your bunk should lie you down in it: {ly}')
    check(e1 >= e0 + 2.5, f'lying down should rest you, not tire you: {e0} -> {e1}')
    g.ev("(() => { const p = player.obj.position, c = nearestOpen(p.x + 1.2, p.z + 1.2, player); playerGo(c, null); })()")
    for j in range(40):
        g.step(10)
        if g.ev("!ACT && player.obj.visible"): break
    up = g.ev("[!!ACT, player.obj.visible]"); print('  walking off:', up)
    check(up == [False, True], f'walking off should get you up: {up}')
    g.ev("setShipNow(Math.floor(shipNow() / 1440) * 1440 + 21 * 60); needsT = null; SHIP.player.needs.energy = 30"); g.step(3)
    day0 = g.ev("SHIP.time.day"); tp = g.ev(BTAP); asked = g.ev("!sleepEl.hidden")
    for j in range(60):
        g.step(10)
        if g.ev("sleeping || !!ACT && ACT.o.slept"): break
    g.page.wait_for_function("window.__sc('!sleeping')", timeout=10000, polling=200); g.step(3)
    bed = g.ev("[SHIP.time.day, hhmm(SHIP.time.min), Math.round(SHIP.player.needs.energy), document.getElementById('tt').textContent, ACT && ACT.kind, ACT && ACT.phase]"); print('  at 21:00:', tp, bed, 'dialog shown:', asked)
    check(tp is True and not asked and bed[0] == day0 + 1 and bed[1] == '06:00' and bed[2] == 100 and bed[3] == 'Good morning' and bed[4:] == ['lie', 'do'], f'the bunk at 21:00 should lie you down and sleep you to 06:00, still in it: {bed}')
    g.ev("actEnd(true)")
    # lay down by day (19:40, a few minutes' walk from the bunk) and still there at 20:00 (reviewer 1, 0.28.37): you fall asleep, as if you'd lain down at night
    g.ev("setShipNow(Math.floor(shipNow() / 1440) * 1440 + 19 * 60 + 40); needsT = null"); g.step(3); day0 = g.ev("SHIP.time.day"); tp = g.ev(BTAP)
    for j in range(60):
        g.step(10)
        if g.ev("!!ACT && ACT.kind === 'lie' && ACT.phase === 'do'"): break
    by = g.ev("[ACT && ACT.kind, !!(ACT && ACT.o.sleep), hhmm(SHIP.time.min)]"); g.ev("setShipNow(Math.floor(shipNow() / 1440) * 1440 + 20 * 60 + 1)")
    for j in range(60):
        g.step(10)
        if g.ev("sleeping || !!ACT && ACT.o.slept"): break
    g.page.wait_for_function("window.__sc('!sleeping')", timeout=10000, polling=200); g.step(3)
    lz = g.ev("[SHIP.time.day, hhmm(SHIP.time.min), ACT && ACT.kind]"); print('  lay down at', by, '-> past 20:00:', lz)
    check(by[:2] == ['lie', False] and lz == [day0 + 1, '06:00', 'lie'], f'lying down by day and still there at 20:00 should sleep you to 06:00: {by} {lz}')
    g.ev("actEnd(true)")

    print('One player day, tapping the real things:')
    g.ev("Object.assign(SHIP.player.needs, { hunger: 20, energy: 100, hygiene: 10, fitness: 30, social: 20, bathroom: 20 }); basket = false")
    g.ev("setShipNow(10 * 60 + 30 + 1440 * 7); needsT = null; goToDeck(4); Object.assign(player.obj.position, cellPos(7, 3)); player.stop()"); g.step(5)
    # someone's own wash pod is not offered
    t = g.ev(f"({TAP})({json.dumps({'title': 'Wash pod'})})"); g.step(5)
    check(t is False and not state(g)['act'], 'a private wash pod should not be offered')
    peak = 0
    tp, b, seen, e, pk = run_activity(g, 'Shower', near=[3, 1]); peak = max(peak, pk)
    check(tp is True and seen and seen[0][1].startswith('4-shower'), f'shower: {seen[:1]}'); body_check('shower', 'hygiene', 80, b, e, seen, 'stand')
    # the toilet (0.28.19, the user's bathroom need): the junior wing's, sitting, and bathroom fills
    tp, b, seen, e, pk = run_activity(g, 'Toilet', near=[5, 1]); peak = max(peak, pk)
    check(tp is True and seen and seen[0][1].startswith('4-toilet'), f'toilet: {seen[:1]}'); body_check('toilet', 'bathroom', 100, b, e, seen, None)
    check(any(a[2] == 'do' and str(a[3]).startswith('sit') for a in seen), f"toilet: should sit ({sorted(set(str(a[3]) for a in seen))})")
    g.ev("setShipNow(shipNow() + 1); goToDeck(3)"); g.step(5)   # mid-morning on Deck 3: the crew are at work
    tp, b, seen, e, pk = run_activity(g, 'Grab and go'); peak = max(peak, pk); body_check('grab', 'hunger', 25, b, e, seen, None)
    tp, b, seen, e, pk = run_activity(g, 'Treadmills'); peak = max(peak, pk); body_check('treadmill', 'fitness', 30, b, e, seen, 'run')
    tp, b, seen, e, pk = run_activity(g, 'Weights'); peak = max(peak, pk); body_check('weights', 'fitness', 30, b, e, seen, 'lift')
    hb = g.ev("(() => { if (typeof homeBooth === 'function') return false; window.__hb = 0; window.homeBooth = () => { window.__hb++; return true; }; return true; })()")   # social B2's call picker (0.28.30)
    tp, b, seen, e, pk = run_activity(g, 'Booth 1'); peak = max(peak, pk); body_check('booth', 'social', 40, b, e, seen, ('call', 'sit:call'))
    if hb:
        hbn = g.ev("window.__hb"); g.ev("delete window.homeBooth"); print('  homeBooth calls at the booth:', hbn)
        check(hbn == 1, f'sitting at a booth should open the call picker once: {hbn}')
    check(seen and seen[0][1].startswith('3-callhome'), 'booth: should use a callhome place')
    g.ev("SHIP.player.needs.bathroom = 30")              # a public toilet on Deck 3 (0.28.19)
    tp, b, seen, e, pk = run_activity(g, 'Toilet', near=[20, 20]); peak = max(peak, pk)
    check(tp is True and seen and seen[0][1].startswith('3-toilet'), f'deck 3 toilet: {seen[:1]}'); body_check('deck 3 toilet', 'bathroom', 70, b, e, seen, None)
    print('Seeing it work (0.28.20, 0.28.21): progress bars and +N notes')
    for name, need in [('Shower', 'Hygiene'), ('Toilet', 'Bathroom'), ('Grab and go', 'Food'), ('Treadmills', 'Fitness'), ('Booth 1', 'Social')]:
        u = UI.get(name, {'bar': [], 'nf': set()}); print(f"  {name:12s} bar {u['bar'][:2]}{'...' if len(u['bar']) > 2 else ''} notes {sorted(u['nf'])[:4]}")
        check(u['bar'] and any('min' in x or 'nearly' in x for x in u['bar']), f'{name}: no progress bar seen')
        check(any(x.startswith('+') and x.endswith(need) for x in u['nf']), f'{name}: no +N {need} note seen')
    pv = g.ev("(() => { goToDeck(2); const r = [...PLACE_OF.values()].filter(q => q.type === 'toilet').map(q => [q.id, privatePlace(q)]); goToDeck(3); return r; })()"); g.step(5)
    print('  Deck 2 toilets private:', sum(1 for x in pv if x[1]), 'of', len(pv), [x[0] for x in pv if not x[1]])
    check(all(x[1] == ('wctoilet' not in x[0]) for x in pv), f'cabin toilets are private, the washroom ones public: {pv}')
    t = g.ev(f"({TAP})({json.dumps({'title': 'Counter'})})"); g.step(60)
    check(t is False and not state(g)['act'], 'the counter with nothing picked out should just show its text')
    tp, b, seen, e, pk = run_activity(g, 'Shelves'); peak = max(peak, pk); body_check('browse', None, 0, b, e, seen, 'browse')
    check(isinstance(e['basket'], dict) and e['basket'].get('price', 0) > 0, f"browsing should leave something to pay for ({e['basket']})")
    cr0, hu0 = g.ev("SHIP.player.credits"), e['needs']['hunger']
    tp, b, seen, e, pk = run_activity(g, 'Counter'); peak = max(peak, pk); body_check('pay', None, 0, b, e, seen, 'pay')
    check(e['basket'] is None, 'paying should empty the basket')
    cr1 = g.ev("SHIP.player.credits"); print('  credits', cr0, '->', cr1, '|', e['toast'][:100])
    check(cr1 == cr0 - b['basket']['price'] and e['toast'].startswith('Paid'), f"paying should cost {b['basket']['price']} credits: {cr0} -> {cr1}")
    if b['basket']['kind'] == 'comfort': check(g.ev("SHIP.player.locker.includes(%s)" % json.dumps(b['basket']['name'])), 'a comfort goes in your locker')
    else: check(e['needs']['hunger'] > hu0, 'a snack should feed you a little')
    g.ev("setShipNow(Math.floor(shipNow() / 1440) * 1440 + 17 * 60 + 40); needsT = null"); g.step(5)   # dinner
    tp, b, seen, e, pk = servery_seat(g, 'Servery, then a seat'); peak = max(peak, pk)
    kinds = [a[0] for a in seen]
    joins = g.ev("typeof galleyJoin === 'function'")    # with the galley's queue (0.29.6) the servery is the queue; without it, a tray at a queue spot
    check(tp is True and ('queue' if joins else 'tray') in kinds and 'eat' in kinds, f'servery: {sorted(set(kinds))}')
    check(any(a[0] == 'eat' and a[1] and a[1].startswith('3-mess') and a[3] == 'sit' for a in seen), 'servery: should sit at a mess seat to eat')
    body_check('eat', 'hunger', 55, b, e, seen, None)
    if g.ev("typeof TRAY_ON !== 'undefined'"):              # your tray (0.28.15): carried to the seat, on the table while you eat, gone after
        carried = any(a[0] == 'eat' and a[2] == 'walk' and a[5] == 'tray' for a in seen)
        on_table = any(a[0] == 'eat' and a[2] == 'do' and a[6] for a in seen)
        after = g.ev("[TRAY_ON.visible, player.holding]")
        print('  the tray: carried to the seat', carried, '| on the table while eating', on_table, '| after: on the table, in hand', after)
        check(carried and on_table and after == [False, False], f'the tray: carried {carried}, on the table {on_table}, after {after}')
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
    tp, b, seen, e, pk = servery_seat(g, 'The queue, then a seat')
    kinds = [a[0] for a in seen]
    check(tp is True and 'queue' in kinds and 'eat' in kinds and 'tray' not in kinds, f'queue: {sorted(set(kinds))}')
    waited = sum(1 for a in seen if a[0] == 'queue' and a[1] is None and a[2] == 'do')
    check(waited >= (1 if real[1] else 3), f'queue: should wait at the back of the line for the turn ({waited} checks)')
    check(any(a[0] == 'eat' and a[1] and a[1].startswith('3-mess') and a[3] == 'sit' for a in seen), 'queue: then sit at a mess seat to eat')
    body_check('queue and eat', 'hunger', 55, b, e, seen, None)
    # in the line a tap doesn't walk you off: it asks "Leave the queue?" (0.28.31)
    g.ev("SHIP.player.needs.hunger = 30"); g.ev(f"({TAP})({json.dumps({'title': 'Servery', 'near': None})})")
    for j in range(60):
        g.step(10)
        if g.ev("!!ACT && ACT.kind === 'queue' && ACT.phase === 'do'"): break
    lq = g.ev("(() => { const inq = !!ACT && ACT.kind === 'queue' && ACT.phase === 'do'; const p = player.obj.position; const r = playerFloorTap(new THREE.Vector3(p.x + 2, 0, p.z + 2)); return [inq, r, !document.getElementById('qAsk').hidden, !!ACT && ACT.kind]; })()")
    g.step(5); still = g.ev("!!ACT && ACT.kind")
    g.ev("document.getElementById('qLeave').click()"); g.step(5); left = g.ev("[!!ACT, document.getElementById('qAsk').hidden]")
    print('  the line holds you (in it, tap held, asked, still queueing):', lq, still, '| after Leave:', left)
    if lq[0]: check(lq[1:] == [True, True, 'queue'] and still == 'queue' and left == [False, True], f'a tap in the line asks first; Leave takes you out: {lq} {still} {left}')
    # moving with the real line (0.28.34, section 10's lineSpot, section 16's galleyLeave; stand-ins when they're missing): your
    # stand-in walks up a tile when the line moves, and you are where it is; leaving takes you out of the line
    stub = g.ev("""(() => { if (typeof lineSpot === 'function') return false; const j = galleyJoin('player');
      window.__ls = { x: j.xy[0] - OX, z: j.xy[1] - OZ, face: Math.PI, at: j.at.slice() }; window.__left = 0;
      window.lineJoin = () => window.__ls; window.lineSpot = () => window.__ls; window.lineLeave = () => {}; if (typeof galleyLeave !== 'function') window.galleyLeave = () => { window.__left++; };   // section 15 leaves only through the galley (the owner's ruling)
      window.__gt = galleyTurn; galleyTurn = () => false; return true; })()""")   # your turn held back while the line moves (the game's own binding: __sc evals inside its scope, where window.galleyTurn isn't seen)
    if stub:
        g.ev("SHIP.player.needs.hunger = 30"); g.ev(f"({TAP})({json.dumps({'title': 'Servery', 'near': None})})")
        for j in range(60):
            g.step(10)
            if g.ev("!!ACT && ACT.kind === 'queue' && ACT.phase === 'do'"): break
        z0 = g.ev("ACT && ACT.z"); g.ev("window.__left = 0"); g.ev("window.__ls = { ...window.__ls, z: window.__ls.z + 1, at: [window.__ls.at[0], window.__ls.at[1] + 1] }")
        for j in range(20): g.step(5)
        mv = g.ev("ACT ? [ACT.kind, +(ACT.z - window.__ls.z).toFixed(2), +(player.obj.position.z - window.__ls.z).toFixed(2)] : [null]")
        g.ev("queueAsk(); document.getElementById('qLeave').click()"); g.step(3)
        lv = g.ev("[!!ACT, window.__left, typeof galleyLeave === 'function' && !GALLEY_JOINED.has('player')]"); g.ev("delete window.lineJoin; delete window.lineSpot; delete window.lineLeave; delete window.galleyLeave; galleyTurn = window.__gt; actEnd(true); SHIP.player.tray = null; if (typeof GALLEY_JOINED !== 'undefined') GALLEY_JOINED.delete('player')")   # nothing left in hand for the later checks
        print('  moving with the line (stand-in): from z', z0, '->', mv, '| left:', lv)
        check(z0 is not None and mv == ['queue', 0, 0] and lv[0] is False and (lv[1] == 1 or lv[2]), f'the line moves you up a tile, and Leave takes you out of it: {z0} {mv} {lv}')
    elif g.ev("typeof servLine === 'function' && typeof galleyLeave === 'function'"):   # a combined build: the real line (0.28.36, reviewer 1c)
        far = g.ev("""(() => { actEnd(true); SHIP.player.tray = null; SHIP.player.needs.hunger = 30; const w = cellPos(19, 10), c = nearestOpen(w.x, w.z, player);
          player.obj.position.copy(cellPos(...c)); player.path.length = 0; const it = ITEMS.find(i => i.t === 'Servery'); it.hit.getWorldPosition(_wp);
          return [c, +Math.hypot(_wp.x - player.obj.position.x, _wp.z - player.obj.position.z).toFixed(1)]; })()""")
        g.ev(f"({TAP})({json.dumps({'title': 'Servery', 'near': None})})"); walk_in, do_in, phases = set(), set(), []
        for j in range(400):
            g.step(10); r = g.ev("[ACT && ACT.kind, ACT && ACT.phase, servLine().includes('player'), SHIP.player.tray]")
            if r[0] == 'queue': (walk_in if r[1] == 'walk' else do_in).add(r[2]); phases.append(r[1]) if not phases or phases[-1] != r[1] else None
            if not r[0] and j > 0: break
        print('  the real line from', far, 'tiles/m away: in the line while walking', walk_in, '| while queueing', do_in, '| phases', phases, '| tray', r[3])
        check(far[1] >= 10 and walk_in == {False} and True in do_in and isinstance(r[3], str), f'from across the room you join the real line only on reaching it, then are served: {far} {walk_in} {do_in} {phases} {r}')
        g.ev("SHIP.player.tray = null")
    # someone on the tile you need (sim 0.26.36's crewMakeWay; a stand-in when it's missing): they step aside, you go, and they go back when you're done (0.28.40)
    mw0 = g.ev("""(() => { actEnd(true); window.__pg = playerGo; let n = 0; playerGo = (c, cb) => n++ ? window.__pg(c, cb) : false;   // the first try refused, as with a cook on the tile
      window.__rel = 0; window.__mwStub = typeof crewMakeWay !== 'function'; if (window.__mwStub) window.crewMakeWay = () => () => { window.__rel++; };
      const q = [...PLACE_OF.values()].find(q => q.type === 'mess-seat' && !heldBy(q.id)); actStart('sit', q.id, { title: 'Mess table' }); return [q.id, ACT && ACT.phase]; })()""")
    mws = []
    for j in range(80):
        g.step(5); ph = g.ev("ACT && ACT.phase")
        if not mws or mws[-1] != ph: mws.append(ph)
        if ph == 'do': break
    mw = g.ev("(() => { const r0 = window.__rel; actEnd(true); playerGo = window.__pg; const r = [window.__mwStub, r0, window.__rel]; if (window.__mwStub) delete window.crewMakeWay; return r; })()")
    print('  someone in the way:', mw0, '->', mws, '| stand-in, released before/after getting up:', mw)
    check(mw0[1] == 'wait' and 'walk' in mws and mws[-1] == 'do' and (not mw[0] or mw[1:] == [0, 1]), f'someone in the way steps aside, you get there, and they go back after: {mw0} {mws} {mw}')
    qn = g.ev("[actProgress({ kind: 'queue', phase: 'do', body: {}, def: { title: 'In the queue' }, o: { turnAt: shipNow() + 5 } })]")
    check(qn[0] is None, f'the queue shows no countdown over your head (0.28.30): {qn}')
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

    print('The store (credits, snacks, comforts):')
    sh = g.ev(r"""(() => { const P = SHIP.player, n = P.needs; P.credits = 20; P.locker = []; n.social = 50; n.hunger = 50;
      basket = { ...storePick('comfort'), gift: null }; ACT = { kind: 'pay', def: PLAYER_ACTS.pay, o: {}, face: 0 }; actEnd(false); const a = [P.credits, P.locker.slice(), Math.round(n.social), basket];   // not a gift (0.28.25)
      basket = { ...storePick('snack'), gift: null }; ACT = { kind: 'pay', def: PLAYER_ACTS.pay, o: {}, face: 0 }; actEnd(false); const b = [P.credits, P.locker.length, Math.round(n.hunger)];
      P.credits = 1; basket = storePick('comfort'); const it = ITEMS.find(i => i.t === 'Counter'); it.hit.getWorldPosition(_wp); const r = playerTap(it, _wp.clone(), _wp.clone());
      const c = [r, !!ACT, basket, document.getElementById('tx').textContent];
      actEnd(true); P.credits = 1; P.locker = []; basket = { ...storePick('comfort'), gift: null }; ACT = { kind: 'pay', def: PLAYER_ACTS.pay, o: {}, face: 0 }; actEnd(false);   // too little at the till (0.28.39)
      const d = [P.credits, P.locker.length, basket];
      P.credits = 20; P.locker = Array.from({ length: LOCKER_MAX }, (_, i) => 'old ' + i); basket = { ...storePick('comfort'), gift: null }; const nm = basket.name; ACT = { kind: 'pay', def: PLAYER_ACTS.pay, o: {}, face: 0 }; actEnd(false);
      d.push(P.locker.length === LOCKER_MAX, P.locker[P.locker.length - 1] === nm, P.locker[0]); P.locker = []; P.credits = 40; return [a, b, c, d]; })()""")
    print(' ', sh)
    check(sh[0][1] and sh[0][0] < 20 and sh[0][2] > 50 and sh[0][3] is None, f'a comfort: credits down, in the locker, social up: {sh[0]}')
    check(sh[1][0] < sh[0][0] and sh[1][1] == len(sh[0][1]) and sh[1][2] > 50, f'a snack: credits down, eaten (food up), not in the locker: {sh[1]}')
    check(sh[2][0] is True and not sh[2][1] and sh[2][2] is None and 'credits' in sh[2][3], f'not enough credits: a toast, no sale: {sh[2]}')
    check(sh[3] == [1, 0, None, True, True, 'old 1'], f'too little at the till: no sale; a full locker keeps the new comfort (the oldest goes): {sh[3]}')
    print('Gifts and your bunk (0.28.25: section 20\'s giftAdd, GIFT_MAKES, bunkNote; stand-ins when they\'re missing):')
    gf = g.ev(r'''(() => { const P = SHIP.player, stub = typeof giftAdd !== 'function', out = {};
      if (stub) { window.giftAdd = x => P.carry.length < CARRY_MAX ? (P.carry.push(x), true) : false; window.GIFT_MAKES = [{ item: 'keyring', mins: 10, needs: 'scrap' }]; }
      P.carry = []; P.credits = 40; P.locker = []; basket = { kind: 'comfort', name: 'a postcard of Earth', price: 3, gain: 3, gift: 'postcard' };
      ACT = { kind: 'pay', def: PLAYER_ACTS.pay, o: {}, face: 0 }; actEnd(false); out.bought = [P.carry.slice(), P.locker.length, P.credits];
      out.gifts = Object.values(STORE).flat().filter(x => x[3]).map(x => x[3]);
      P.carry = []; ACT = { kind: 'craft', def: { ...PLAYER_ACTS.craft }, o: { gift: 'keyring', needs: 'scrap' }, face: 0 }; actEnd(false); out.made = P.carry.slice(); P.carry = [];
      if (typeof gardenCarry === 'function' && SHIP.galley && SHIP.galley.garden) {   // a garden run with herbs and tomatoes: both into your hands once picked up
        const id = gardenCarry({ at: Math.floor(shipNow()) - 1, crates: 2 }), j = SHIP.jobs.find(x => x.id === id), hi = GARDEN_CROPS.findIndex(c => c.id === 'herbs'), ti = GARDEN_CROPS.findIndex(c => c.id === 'tomatoes');
        SHIP.galley.garden.crates.push({ at: shipNow(), items: [[hi, 5], [ti, 20]], id });
        for (const x of SHIP.jobs) if (x.claimedBy === 'you' && x !== j) { x.claimedBy = null; x.status = 'open'; } j.claimedBy = 'you'; j.status = 'claimed'; j.stepsDone = [0]; out.mine = myJob() && myJob().id; const t0 = shipNow(); let hd = SHIP.time.day; if (typeof gardenHarvestDay === 'function') { while (!gardenHarvestDay(hd) && hd < SHIP.time.day + 60) hd++; out.notToday = SHIP.time.day === hd ? null : (gardenGift(), P.carry.slice()); GARDEN_GIVEN.delete(id); setShipNow((hd - 1) * 1440 + SHIP.time.min); } gardenGift(); out.garden = P.carry.slice(); P.carry = []; gardenGift(); out.again = P.carry.slice(); setShipNow(t0);
        SHIP.galley.garden.crates = SHIP.galley.garden.crates.filter(c => c.id !== id); SHIP.jobs = SHIP.jobs.filter(x => x !== j); P.carry = [];
      }
      if (stub) { delete window.giftAdd; delete window.GIFT_MAKES; }
      out.stub = stub; return out; })()''')
    print(' ', gf)
    check(gf['bought'] == [['postcard'], 0, 37], f"a gift from the store goes into your hands, not the locker ({gf['bought']})")
    check(set(gf['gifts']) <= {'tin of tea', 'biscuits', 'postcard', 'little plant', 'puzzle book', 'bar of chocolate', 'paper novel', 'music chip', 'pocket puzzle', 'spare tiles set'} and len(gf['gifts']) == 10, f"the store's gifts are section 20's names ({gf['gifts']})")
    check(gf['made'] == ['keyring'], f"a gift made in the machine shop goes into your hands ({gf['made']})")
    if 'garden' in gf: check(gf['garden'] == ['herbs', 'tomato'] and gf['again'] == [], f"a garden run's herbs and tomato into your hands, once ({gf.get('garden')}, {gf.get('again')})")
    if gf.get('notToday') is not None: check(gf['notToday'] == [], f"no garden gift on a day that isn't a harvest day ({gf['notToday']})")

    print('Social from chatting and company:')
    ch = g.ev(r"""(() => { const n = SHIP.player.needs, out = []; SHIP.player.chats = {};
      const chat = (who, hy) => { n.social = 50; n.hygiene = hy; playerChat({ id: who, name: 'Test ' + who }); return Math.round((n.social - 50) * 10) / 10; };
      out.push(chat('a', 50), chat('a', 50), chat('b', 80), chat('c', 10), document.getElementById('tx').textContent.includes('nose'));
      setShipNow(shipNow() + 1440); out.push(chat('a', 50)); setShipNow(shipNow() - 1440); n.hygiene = 50; return out; })()""")
    print('  first chat, again, clean, unwashed (and the remark), next day:', ch)
    check(ch[:4] == [6, 1, 9, 3] and ch[4] is True and ch[5] == 6, f'chatting: {ch}')
    cf = g.ev("(() => { if (!SHIP.rel) return null; const n = SHIP.player.needs, k = SHIP.rel['tst-f']; SHIP.rel['tst-f'] = { pts: 0, tier: 3, met: 1, known: true }; n.social = 50; delete SHIP.player.chats['tst-f']; playerChat({ id: 'tst-f', name: 'Test F' }); const g = Math.round((n.social - 50) * 10) / 10; if (k === undefined) delete SHIP.rel['tst-f']; else SHIP.rel['tst-f'] = k; delete SHIP.player.chats['tst-f']; return g; })()")
    print('  first chat with a friend (0.28.43):', cf)
    check(cf is None or cf == 12, f'a chat with a friend counts twice: {cf}')
    # company at a meal (0.28.43, the user's): only your own table counts, each person by your bond (bondMult); capped
    cp = json.loads(g.ev(r"""(() => { const n = SHIP.player.needs, seats = [...PLACE_OF.values()].filter(q => q.type === 'mess-seat' && /^3-/.test(q.id));
      const me = seats[0], tb = seatTable(me.id), mates = seats.filter(q => q.id !== me.id && seatTable(q.id) === tb), others = seats.filter(q => seatTable(q.id) !== tb).slice(0, 2);
      const sizes = {}; for (const q of seats) { const t = seatTable(q.id); sizes[t] = (sizes[t] || 0) + 1; }
      const s0 = placeSpot(me.id), rel = SHIP.rel || {}, keep = {}, out = [];
      const fake = (q, id) => { const s = placeSpot(q.id); return { settled: true, goalId: q.id, x: s.x, z: s.z, spot: { pose: 'sit', room: 'M' }, p: { id, name: 'Test' } }; };
      const ids = ['tst-a', 'tst-b', 'tst-c', 'tst-d', 'tst-e', 'tst-f']; for (const id of ids) keep[id] = rel[id];
      const was = DECK_CREW.filter(a => a.settled && a.goalId && seatTable(a.goalId) === tb); DECK_CREW.splice(0, DECK_CREW.length, ...DECK_CREW.filter(a => !was.includes(a)));   // the table to ourselves
      const meal = (crew, tiers = {}) => {
        for (const id in tiers) if (SHIP.rel) SHIP.rel[id] = { pts: 0, tier: tiers[id], met: 1, known: true };
        DECK_CREW.push(...crew); Object.assign(n, { hunger: 50, social: 50, hygiene: 50, energy: 50, fitness: 50, bathroom: 50 });
        FX_MIN = Math.floor(shipNow()); FX_NOW = { deck: deckDef.num, restore: {}, drain: {}, notes: [] };
        ACT = { kind: 'eat', def: PLAYER_ACTS.eat, phase: 'do', done: 0, o: {}, placeId: me.id, spot: s0, deck: deckDef, x: 0, z: 0, y: 0, face: player.face, to: {}, body: { set() {}, update() {}, dispose() {} } };
        needsT = shipNow() - 10; playerUpdate(0, 0); const r = [Math.round(company(ACT) * 10) / 10, Math.round((n.social - 50 + NEED_DRAIN.social[0] / 6) * 10) / 10];
        DECK_CREW.splice(DECK_CREW.length - crew.length, crew.length); ACT = null; for (const id in tiers) if (SHIP.rel) delete SHIP.rel[id]; return r; };
      out.push(meal([]), meal([fake(mates[0], 'tst-a'), fake(mates[1], 'tst-b')]), meal(mates.slice(0, 4).map((q, i) => fake(q, ids[i]))),
        meal(others.map((q, i) => fake(q, ids[i]))), meal([fake(mates[0], 'tst-e'), fake(mates[1], 'tst-f')], { 'tst-e': 4, 'tst-f': 4 }),
        meal(mates.slice(0, 4).map((q, i) => fake(q, ids[i])), { 'tst-a': 4, 'tst-b': 4, 'tst-c': 4, 'tst-d': 4 }));
      for (const id of ids) { if (keep[id] === undefined) { if (SHIP.rel) delete SHIP.rel[id]; } else SHIP.rel[id] = keep[id]; }
      DECK_CREW.push(...was); FX_MIN = -1; return JSON.stringify({ tables: Object.values(sizes).sort(), mates: mates.length, out, mult: BOND_MULT, rel: !!SHIP.rel }); })()"""))
    print('  mess tables (seats each), your table-mates; ten minutes eating with [company, social]: nobody, 2 and 4 strangers at your table, 2 at another table, 2 and 4 close friends:', cp)
    o = cp['out']
    check(cp['tables'] == [4, 4, 4, 8, 8, 8, 8] and cp['mates'] == 7, f"the mess's tables: four long ones of eight, three round ones of four ({cp['tables']}, mates {cp['mates']})")
    check(o[0] == [0, 0] and o[1] == [2, 4] and o[2] == [4, 8] and o[3] == [0, 0], f'only your own table counts, +0.2 a minute a stranger, an empty table nothing: {o[:4]}')
    if cp['rel']: check(o[4] == [6, 12] and o[5] == [6, 12], f"close friends count three times, at most six strangers' worth: {o[4:]}")
    print('The note bus (0.28.22: simNote acts, inert until section 13 has simNote):')
    sn = g.ev(r'''(() => { const log = [], real = typeof simNote === 'function';
      if (!real) window.simNote = (k, o) => log.push([k, o]); else return 'real';
      const fake = (kind, o = {}, phase = 'do', done = 5) => { ACT = { kind, def: { ...PLAYER_ACTS[kind] }, phase, done, o, face: player.face, deck: deckDef }; actEnd(true); };
      fake('shower'); fake('eat', { company: 2 }); fake('grab'); fake('call'); fake('toilet'); fake('shower', {}, 'walk', 0);
      const P = SHIP.player, c0 = P.credits; P.credits = 50; basket = storePick('snack'); ACT = { kind: 'pay', def: PLAYER_ACTS.pay, o: {}, face: 0 }; actEnd(false); P.credits = c0;
      delete window.simNote; return log; })()''')
    print(' ', sn)
    if sn != 'real':
        check([x[1]['act'] for x in sn] == ['wash', 'eat', 'eat', 'call', 'buy'] and sn[1][1]['with'] == 2 and sn[2][1]['with'] == 0 and all(x[0] == 'act' for x in sn),
              f'simNote acts: wash, eat (with 2), eat (with 0), call, buy; nothing for the toilet or an activity never started: {sn}')
    print('Mail:')
    ml = g.ev(r"""(() => { SHIP.mail = []; device.refresh(); const b = document.getElementById('devMail'), out = [b.hidden];
      mailSend({ from: 'Stores', subject: 'Filters low', body: 'Two left.' }); mailSend({ at: shipNow() - 5, from: 'Galley', subject: 'Cake tonight', body: 'Tomas turns 24.' });
      out.push(b.hidden, b.textContent, mailUnread(), SHIP.mail.map(m => m.subject));
      device.open(); const tile = document.querySelector('#devBody .app[data-app="mail"]'); device.show('mail'); const body = document.getElementById('devBody');
      out.push([tile.querySelector('span').textContent, tile.querySelector('b').textContent], body.querySelectorAll('button.row').length);
      body.querySelector('button.row').click(); out.push(mailUnread(), document.getElementById('devBody').textContent.includes('Two left.'));
      device.show('status'); device.close(); return out; })()""")
    print(' ', ml)
    check(ml[0] is True and ml[1] is False and ml[2] == '2' and ml[3] == 2, f'mail: the unread count on the button: {ml[:4]}')
    check(ml[4] == ['Filters low', 'Cake tonight'] and ml[5] == ['Mail', '2'] and ml[6] == 2, f'mail: the Mail app (its tile shows 2), newest first: {ml[4:7]}')
    check(ml[7] == 1 and ml[8] is True, f'mail: opening one shows it and marks it read: {ml[7:]}')

    print('A machine tap (machineUse):')
    real_use = g.ev("typeof machineUse === 'function'")
    if not real_use: g.ev("window.machineUse = (id, who) => (window.__used = [id, who], { text: 'Stand-in: ' + id + ' looked at.', ran: false })")
    g.ev("goToDeck(4); Object.assign(player.obj.position, cellPos(7, 3)); player.stop()"); g.step(5)
    mt = g.ev(r"""(() => { const here = player.here();   // a machine in a room you can walk into, and the thing nearest it
      for (const m of machineList().filter(m => m.deck === 4 && !m.stub)) {
        const c = cellPos(...m.at), it = ITEMS.filter(i => !i.see && !i.lift).map(i => { i.hit.getWorldPosition(_wp); return [i, _wp.clone()]; }).sort((a, b) => Math.hypot(a[1].x - c.x, a[1].z - c.z) - Math.hypot(b[1].x - c.x, b[1].z - c.z))[0];
        if (!it || Math.hypot(it[1].x - c.x, it[1].z - c.z) > .8 || ACT_TAP.some(r => r[0].test(it[0].t))) continue;
        const fx = Math.sin(it[0].front), fz = Math.cos(it[0].front), goal = nearestOpen(it[1].x + fx * (it[0].depth / 2 + .55), it[1].z + fz * (it[0].depth / 2 + .55), player);
        if (!goal || !findPath(here, goal, null, player)) continue;
        return [it[0].t, playerTap(it[0], it[1].clone(), it[1].clone()), m.id];
      }
      return ['none', false, null]; })()""")
    for k in range(60):
        g.step(30)
        if not g.ev("player.path.length > 0"): break
    mt.append(g.ev("document.getElementById('tt').textContent + ': ' + document.getElementById('tx').textContent"))
    if not real_use: mt.append(g.ev("window.__used")); g.ev("delete window.machineUse; delete window.__used")
    print(' ', mt)
    check(mt[1] is True and mt[2] and len(mt[3]) > len(mt[0]) + 2 and ('Stand-in' in mt[3] if not real_use else True) and (real_use or mt[4] == [mt[2], 'player']), f'a machine tap should ask machineUse: {mt}')
    wt = g.ev(r"""(() => { const it = ITEMS.find(i => /^washer \d/i.test(i.t)); if (!it) return null; it.hit.getWorldPosition(_wp);   // a stub machine (0.28.14): by room and name
      const near = machineList().filter(m => m.deck === deckDef.num && !m.stub && m.at && m.kind === 'washer').map(m => [m, cellPos(...m.at)]).filter(([, c]) => Math.hypot(c.x - _wp.x, c.z - _wp.z) < MACHINE_NEAR)[0];   // a real washer now (section 17), else a stub
      const m = near || stubTap(it, _wp.clone()); return [it.t, m && m[0].id, !!near]; })()""")
    print('  a washer (its machine: the real one by the tap, else a stub by name and number):', wt)
    check(wt is None or (wt[1] and 'washer' in wt[1] and (wt[2] or wt[1].endswith('-' + wt[0].split()[-1]))), f'a washer tap should find its machine: {wt}')
    no = g.ev("(() => { const it = ITEMS.find(i => /^bunk/i.test(i.t)); it.hit.getWorldPosition(_wp); return machineTap(it, _wp.clone()); })()")
    check(no is False, 'a bunk is no machine: the tap does what it always did')

    print('Crawlways (crouch-walk):')
    cw = g.ev(r"""(() => { const t = nearestOpen(LIFT_AT[0], LIFT_AT[1], player), was = deckDef.crawl; deckDef.crawl = [K(t)]; CRAWL.def = null;
      Object.assign(player.obj.position, cellPos(...t)); Object.assign(SHIP.player.needs, { fitness: 50, energy: 50 }); playerUpdate(0, 0);
      const out = [player.maxV / PLAYER_V0, player.crouch, document.getElementById('tx').textContent];
      deckDef.crawl = was; CRAWL.def = null; playerUpdate(0, 0); out.push(player.maxV / PLAYER_V0, player.crouch); return out; })()""")
    print('  on a crawl tile [speed, crouching, toast], then off it [speed, crouching]:', cw)
    check(cw[0] == .5 and cw[1] is True and 'crouch' in cw[2] and cw[3] == 1 and cw[4] is False, f'crawlway: {cw}')
    g.ev("goToDeck(3)"); g.step(5)                      # back where the next checks expect you

    print('Sit anywhere:')
    st = g.ev(r"""(() => { const seat = [...PLACE_OF.values()].filter(pl => SIT_TYPES.has(pl.type) && pl.pose === 'sit' && !heldBy(pl.id) && pl.type !== 'mess-seat')
        .map(pl => [pl, placeSpot(pl.id)]).filter(([, s]) => s && s.pose === 'sit' && findPath(player.here(), s.walk, null, player))[0];
      if (!seat) return null; const p = new THREE.Vector3(seat[1].x, .4, seat[1].z);
      const it = ITEMS.map(i => { i.hit.getWorldPosition(_wp); return [i, _wp.clone()]; }).sort((a, b) => a[1].distanceTo(p) - b[1].distanceTo(p))[0];
      return [seat[0].id, seat[0].type, it[0].t, playerTap(it[0], it[1].clone(), p)]; })()""")
    print('  tapped:', st)
    if check(st and st[3] is True, f'sit anywhere: a tap on a free seat should sit you ({st})'):
        for k in range(80):
            g.step(30)
            if g.ev("!!ACT && ACT.phase === 'do'"): break
        sat = json.loads(g.ev("JSON.stringify([ACT && ACT.kind, ACT && ACT.placeId, ACT && ACT.pose, ACT && ACT.y, player.obj.visible, document.getElementById('tx').textContent])"))
        print('  sitting:', sat[:5], '|', sat[5][:80])
        check(sat[0] == 'sit' and sat[1] == st[0] and sat[2] == 'sit' and not sat[4] and 'sit down' in sat[5], f'sit anywhere: sitting at the seat ({sat})')
        rest = g.ev(r"""(() => { const n = SHIP.player.needs; Object.assign(n, { energy: 60, fitness: 50, hunger: 50, social: 50 }); FX_MIN = Math.floor(shipNow()); FX_NOW = { deck: deckDef.num, restore: {}, drain: {}, notes: [] };
          needsT = shipNow() - 60; playerUpdate(0, 0); FX_MIN = -1; return [Math.round((60 - n.energy) * 100) / 100, !!ACT]; })()""")
        print('  an hour sitting: energy drained', rest[0], '(awake, standing: 4.4)')
        check(abs(rest[0] - 4.4 * .6) < .01 and rest[1], f'sitting should rest you: energy -{rest[0]} in an hour, want {4.4 * .6:.2f}')
        g.ev("playerGo(nearestOpen(LIFT_AT[0], LIFT_AT[1], player))"); g.step(5)
        up = g.ev("[!!ACT, player.obj.visible]"); print('  walked off:', up)
        check(up == [False, True], f'walking away should get you up ({up})')

    print('The treadmills, by real clicks (Deck 3 gym):')
    BELT = "(id => { const s = placeSpot(id), v = []; scene.traverse(m => { if (m.isMesh && m.material && m.material.map && m.userData.noMerge) { m.getWorldPosition(_wp); if (Math.hypot(_wp.x - s.x, _wp.z - s.z) < 1.2) v.push(m.material.map.offset.y); } }); return JSON.stringify(v); })"
    W, H = g.page.viewport_size['width'], g.page.viewport_size['height']
    ran = 0
    TREADS = ['3-gym-1', '3-gym-2', '3-gym-3']
    if all(g.ev(f"!!heldBy('{p}')") for p in TREADS):    # all three taken: a weekday mid-morning, when the crew are at work
        g.ev("setShipNow(Math.floor(shipNow() / 1440) * 1440 + 1440 + 10 * 60 + 30); needsT = null"); g.step(10)
    for pid, ht in [('3-gym-1', .3), ('3-gym-2', 1.1), ('3-gym-3', .6)]:
        g.ev("actEnd(true); player.stop(); Object.assign(player.obj.position, cellPos(26, 17)); Object.assign(SHIP.player.needs, { fitness: 40, energy: 70, hunger: 50, social: 50 })"); g.step(30)
        xy = g.ev(f"(() => {{ const s = placeSpot('{pid}'); const v = new THREE.Vector3(s.x, {ht}, s.z).project(camera); return [(v.x + 1) / 2 * innerWidth, (1 - v.y) / 2 * innerHeight]; }})()")
        if not check(0 < xy[0] < W and 0 < xy[1] < H, f'treadmill {pid} should be on screen ({xy})'): continue
        who = g.ev(f"(a => a ? a.p.name : null)(heldBy('{pid}'))")
        if who: print(' ', pid, 'in use by', who, '(a click there taps them, which is right)'); continue   # a crew member on it: the click is a tap on them (0.41.6)
        g.page.mouse.click(xy[0], xy[1]); g.step(2)
        for k in range(60):
            g.step(30)
            if g.ev("!!ACT && ACT.phase === 'do'"): break
        a = json.loads(g.ev("JSON.stringify([ACT && ACT.placeId, ACT && ACT.phase, ACT && ACT.pose, SHIP.player.needs.fitness, SHIP.player.needs.energy, shipNow()])")); b0 = g.ev(f"({BELT})('{pid}')")
        g.step(250)
        b = json.loads(g.ev("JSON.stringify([ACT && ACT.placeId, ACT && ACT.phase, ACT && ACT.pose, SHIP.player.needs.fitness, SHIP.player.needs.energy, shipNow()])")); b1 = g.ev(f"({BELT})('{pid}')")
        print(f'  {pid} (clicked at {ht} m): {a[:3]} | {b[5] - a[5]:.1f} ship min: fitness {a[3]:.1f} -> {b[3]:.1f}, energy {a[4]:.1f} -> {b[4]:.1f} | belt moving {b0 != b1}')
        if check(a[0] == pid and a[1] == 'do' and a[2] == 'run', f'treadmill {pid}: should be running on it ({a[:3]})'):
            ran += 1
            check(b[0] == pid and b0 != b1 and b[3] > a[3] + 2 and b[4] < a[4] - .5, f'treadmill {pid}: belt moving, fitness up, energy down ({a} -> {b}, belt {b0 != b1})')
    check(ran >= 1, 'treadmills: at least one free to run on')
    g.ev("actEnd(true); player.stop()")

    print('Squeezing past settled crew (the galley plant, Deck 3):')   # the chef on [39,3]: [39,4] is shared by two places, where sim 0.26.36's crew step aside instead (0.28.40)
    sq = g.ev(r"""(() => { const blocker = { settled: true, spot: { onTile: true, walk: [39, 3], pose: 'work', x: cellPos(39, 3).x, z: cellPos(39, 3).z }, x: cellPos(39, 3).x, z: cellPos(39, 3).z,
        goalId: 'test', p: { name: 'Test Brennan', role: 'Chef', id: 'test' }, update() { return true; }, remove() {}, h: { set() {} } };
      window.__blocker = blocker; DECK_CREW.push(blocker);
      const goal = [39, 1], here = player.here(), avoid = occupiedBy(player);
      const walled = !findPath(here, goal, avoid, player), went = playerGo(goal);
      return [walled, went, player.path.some(c => c[0] === 39 && c[1] === 3)]; })()""")
    print('  walled off without squeezing, path found, through the chef\'s tile:', sq)
    slow = 1
    for k in range(400):
        g.step(3); slow = min(slow, g.ev("player.maxV / PLAYER_V0 / needEffects().walk"))
        if not g.ev("player.path.length > 0"): break
    sqe = g.ev("[K(player.here()), document.getElementById('tt').textContent + ': ' + document.getElementById('tx').textContent]")
    g.ev("DECK_CREW.splice(DECK_CREW.indexOf(window.__blocker), 1); delete window.__blocker")
    print('  arrived at', sqe[0], '| slowest', round(slow, 2), '|', sqe[1][:80])
    check(sq[1] is True and sq[2] is True and sqe[0] == '39,1', f'squeeze past: should reach the galley plant panel through the chef ({sq}, {sqe})')
    check(abs(slow - .5) < .01 and 'Excuse me, Chef' in sqe[1], f'squeeze past: slowed to half, with a polite word ({slow}, {sqe[1]})')

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
      playerUpdate(0, 0); out.speed = playerSpeed() / needEffects().walk; out.maxV = player.maxV / PLAYER_V0 / needEffects().walk;   // the needs' own walk only
      device.open(); out.note = document.getElementById('devBody').textContent.includes('showers are running weak'); device.close();
      n.hygiene = 10; n.bathroom = 50; ACT = { kind: 'shower', def: PLAYER_ACTS.shower, phase: 'do', done: 0, o: {}, deck: deckDef, x: 0, z: 0, y: 0, face: player.face, to: {}, body: { set() {}, update() {}, dispose() {} } };
      needsT = shipNow() - PLAYER_ACTS.shower.mins; """ + FX + r""" playerUpdate(0, 0); out.shower = Math.round(n.hygiene); ACT = null; FX_MIN = -1;
      return out; })()""")
    print(' ', st)
    check(st['drainHungerX2'] == 8 and st['hygieneDrain'] == 2.5, 'drain multipliers from shipEffects')
    check(st['speed'] == 1 and abs(st['maxV'] - 1) < 1e-9, "shipEffects' walk must not slow the player (the user's rule)")
    check(st['note'], 'the ship notes should show on the device')
    check(st['shower'] == 50, f"a weak shower (restore x0.5) should give half: 10 -> {st['shower']}")
    if real[2]:
        live = g.ev("(() => { FX_MIN = -1; const f = playerFx(), r = shipEffects(deckDef.num); return f === r && NEED_KEYS.every(k => k === 'bathroom' ? !(k in f.restore) || isFinite(f.restore[k]) && isFinite(f.drain[k]) : isFinite(f.restore[k]) && isFinite(f.drain[k])); })()   // section 17 knows the first five needs (bathroom, 0.28.19: 1 when left out)")
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

    # the job loop (B2), when the build has section 17's jobs (myJob, finishJob, takePart): take a job, look the machine
    # over, fetch its part from main storage on Deck 5, fit it and repair it; walking away pauses the repair
    if g.ev("jobsOn()"):
        print('The job loop (section 17\'s jobs):')
        JST = "JSON.stringify([ACT && [ACT.kind, ACT.placeId, ACT.phase], SHIP.player.carry, SHIP.player.work, document.getElementById('tt').textContent + ': ' + document.getElementById('tx').textContent])"
        def jrun(n=80):
            for k in range(n):
                g.step(30)
                if k > 1 and not g.ev("!!ACT || player.path.length > 0"): break
            return json.loads(g.ev(JST))
        TAPI = "(() => { const s = placeSpot(panelPlace(myJob().machine)), it = ITEMS.map(i => { i.hit.getWorldPosition(_wp); return [i, _wp.clone()]; }).sort((a, b) => Math.hypot(a[1].x - s.x, a[1].z - s.z) - Math.hypot(b[1].x - s.x, b[1].z - s.z))[0]; return playerTap(it[0], it[1].clone(), it[1].clone()); })()"
        TAPS = "(() => { const it = ITEMS.find(i => i.t === %s); it.hit.getWorldPosition(_wp); return playerTap(it, _wp.clone(), _wp.clone()); })()"
        g.ev("setShipNow(Math.floor(shipNow() / 1440) * 1440 + 1440 * 2 + 9 * 60); needsT = null; SHIP.player.carry = []; SHIP.player.work = null"); g.step(3)
        # a tier-1 service job on a machine with a panel place, handed to you (the crew may have claimed it: test only)
        jid = g.ev(r"""(() => { machinesNow(); const j = SHIP.jobs.find(j => j.machine && j.kind === 'service' && j.status !== 'done' && jobTier(j) <= PLAYER_TIER && panelPlace(j.machine) && !ENGINE_KINDS.has(machineById(j.machine).kind));
          if (!j) return null; j.claimedBy = null; j.status = 'open'; delete j.start; j.found = Math.min(j.found, shipNow()); MACH_REV++; return claimJob(j.id) ? j.id : null; })()""")
        check(jid is not None, 'job loop: a tier-1 service job to take')
        if jid:
            mj = json.loads(g.ev("JSON.stringify([myJob().parts, machineById(myJob().machine).deck, myJob().machine, SHIP.stores[myJob().parts[0]]])"))
            print('  your job:', jid, mj)
            g.ev(f"goToDeck({mj[1]})"); g.step(5)
            check(g.ev(TAPI) is True, 'job loop: a tap on the machine should be the job'); s1 = jrun()
            print('  inspected:', s1[3][:110]); check(s1[2]['seen'] and 'needs' in s1[3], f'job loop: inspecting should say what it needs ({s1[3]})')
            g.ev("goToDeck(5)"); g.step(5)
            shelf = g.ev("JSON.stringify(ITEMS.filter(i => roomAt(...cellAt(i.hit.getWorldPosition(_wp).x, _wp.z)) === 'r' && !/tarp/i.test(i.t)).map(i => i.t)[0])")
            check(g.ev(TAPS % shelf) is True, 'job loop: a tap on a storage shelf should fetch'); s2 = jrun()
            print('  fetched:', s2[1], s2[3][:100]); check(s2[1] == mj[0][:2], f'job loop: should carry {mj[0]}, carries {s2[1]}')
            check(g.ev(f"SHIP.stores[{json.dumps(mj[0][0])}]") == mj[3] - 1, 'job loop: one off the storage shelf')
            check(g.ev("player.holding") is True, 'job loop: carrying parts should show the crate (player.holding)')
            g.ev(f"goToDeck({mj[1]})"); g.step(5)
            check(g.ev(TAPI) is True, 'job loop: back at the machine')
            for k in range(60):                                # repair a few minutes, then walk away
                g.step(30)
                if g.ev("!!ACT && ACT.phase === 'do' && SHIP.player.work.done >= 4"): break
            g.ev("playerGo(nearestOpen(LIFT_AT[0], LIFT_AT[1], player))"); g.step(3)
            paused = json.loads(g.ev(JST)); print('  walked away mid-repair:', paused[0], paused[2])
            check(not paused[0] and paused[2]['fitted'] == mj[0] and paused[2]['done'] >= 4, 'job loop: walking away should keep the part fitted and the repair time done')
            check(g.ev("player.holding") is not True, 'job loop: with the parts fitted, the crate goes')   # True is the crate; 15b's toolbox may stay (0.37.5)
            if g.ev("typeof touchJob === 'function'"):
                tc = g.ev(f"(() => {{ const j = SHIP.jobs.find(j => j.id === {json.dumps(jid)}); return [j.touched || 0, j.start, shipNow()]; }})()")
                print('  touched (section 17\'s touchJob):', tc)
                check(tc[0] > tc[1] and tc[2] - tc[0] < 3, 'job loop: repairing should touch the job (keeps it yours)')
            sv = json.loads(g.ev("(() => { const s = { player: {} }; for (const f of SAVE_EXTRA) try { f(s); } catch (e) {} return JSON.stringify(s.player); })()"))
            check(sv.get('work', {}).get('done', 0) >= 4 and sv.get('carry') == [], f"job loop: the save should hold the work ({sv.get('work')})")
            g.step(60); check(g.ev(TAPI) is True, 'job loop: resume'); s3 = jrun(160)
            g.ev("(() => { const j = typeof turnInJob === 'function' && myJob(); if (j && j.workDone) turnInJob(j.id); })()")   # TURN_IN (0.37.3): finished jobs are turned in at the board
            done = json.loads(g.ev(f"JSON.stringify([myJob(), SHIP.jobs.find(j => j.id === {json.dumps(jid)}).status, SHIP.machines[{json.dumps(mj[2])}].cond])"))
            print('  repaired:', s3[3][:80], '| job', done[1], '| condition', round(done[2]))
            check(done[0] is None and done[1] == 'done' and done[2] >= 99 and s3[2] is None, f'job loop: the job should be done and the machine as new ({done})')
        # making a part: storage has none, so the machine shop (an hour at the lathe; resumed here near the end)
        mk = g.ev(r"""(() => { machinesNow(); const j = SHIP.jobs.find(j => j.machine && j.status !== 'done' && jobTier(j) <= PLAYER_TIER && !ENGINE_KINDS.has(machineById(j.machine).kind));
          if (!j) return null; j.claimedBy = null; j.status = 'open'; delete j.start; j.found = Math.min(j.found, shipNow()); j.parts = ['element']; MACH_REV++;
          if (!claimJob(j.id)) return null; window.__stock = SHIP.stores.element; SHIP.stores.element = 0; SHIP.player.carry = []; myWork(); return j.id; })()""")
        if mk:
            g.ev("goToDeck(5)"); g.step(5)
            f = g.ev(TAPS % '"Galley parts"'); s5 = jrun(); print('  storage out of elements:', s5[3][:120])
            check(s5[1] == [] and 'machine shop' in s5[3], 'job loop: no elements in storage should point to the machine shop')
            g.ev("SHIP.player.work.make = { part: 'element', done: 57 }")
            lathe = g.ev("JSON.stringify(ITEMS.filter(i => roomAt(...cellAt(i.hit.getWorldPosition(_wp).x, _wp.z)) === 'f').map(i => i.t)[0])")
            check(g.ev(TAPS % lathe) is True, f'job loop: a tap in the machine shop ({lathe}) should make the part'); s6 = jrun()
            print('  made:', s6[1], '|', s6[3][:100])
            check(s6[1] == ['element'] and s6[2]['make'] is None, 'job loop: making should leave the part in your hands')
            g.ev(f"SHIP.stores.element = window.__stock; dropJob({json.dumps(mk)}); SHIP.player.carry = []")
        # a reserved training job (0.28.24, section 17's jobReserve): a shelf part, then a bracket you make, then the repair
        if g.ev("typeof jobReserve === 'function'"):
            rj = g.ev(r"""(() => { SHIP.player.carry = []; SHIP.player.work = null; const id = jobReserve('lights', SHIP.time.day, Math.max(0, SHIP.time.min - 1), 3);
              if (!id || !claimJob(id)) return null; myWork(); const j = myJob(); return [id, j.parts, j.make, machineById(j.machine).deck, jobStops(j).map(x => x.step)]; })()""")
            print('  a reserved job:', rj)
            if check(rj and rj[2] and rj[2] in rj[1] and 'make' in rj[4], f'reserved job: should need a part you make ({rj})'):
                g.ev("goToDeck(5)"); g.step(5)
                shelf = g.ev("JSON.stringify(ITEMS.filter(i => roomAt(...cellAt(i.hit.getWorldPosition(_wp).x, _wp.z)) === 'r' && !/tarp/i.test(i.t)).map(i => i.t)[0])")
                g.ev(TAPS % shelf); r1 = jrun(); print('  fetched:', r1[1], '|', r1[3][:120])
                check(r1[1] == [x for x in rj[1] if x != rj[2]] and 'machine shop' in r1[3], f'reserved job: fetch takes the shelf part only and points to the machine shop ({r1[1]}, {r1[3]})')
                g.ev(TAPS % shelf); g.step(3); t2 = g.ev("document.getElementById('tx').textContent")
                check("isn't kept on the shelves" in t2, f'reserved job: storage says the {rj[2]} is made, not kept ({t2})')
                g.ev(f"SHIP.player.work.make = {{ part: {json.dumps(rj[2])}, done: makeMins(myJob()) - 3 }}")
                lathe = g.ev("JSON.stringify(ITEMS.filter(i => roomAt(...cellAt(i.hit.getWorldPosition(_wp).x, _wp.z)) === 'f').map(i => i.t)[0])")
                g.ev(TAPS % lathe); bar = None
                for k in range(80):
                    g.step(10); bar = bar or g.ev("(p => p && p.title + ' ' + Math.round(p.frac * 100))(actProgress())")
                    if bar: break
                r2 = jrun(); sd = g.ev("(() => { const j = myJob(); return [j.stepsDone || [], jobStops(j).map(x => x.step)]; })()")
                print('  made:', r2[1], '| bar', bar, '| stops done', sd, '|', r2[3][:100])
                check(sorted(r2[1]) == sorted(rj[1]) and bar and bar.startswith('Machine shop'), f'reserved job: the {rj[2]} made, in your hands, with the progress bar ({r2[1]}, {bar})')
                check(sd[1].index('fetch') in sd[0] and sd[1].index('make') in sd[0], f'reserved job: the fetch and make stops marked done ({sd})')
                g.ev(f"goToDeck({rj[3]})"); g.step(5)
                check(g.ev(TAPI) is True, 'reserved job: a tap on the machine'); r3 = jrun(200)
                g.ev("(() => { const j = typeof turnInJob === 'function' && myJob(); if (j && j.workDone) turnInJob(j.id); })()")
                rd = g.ev(f"(() => {{ const j = SHIP.jobs.find(j => j.id === {json.dumps(rj[0])}); return [j.status, !!myJob()]; }})()")
                print('  repaired:', rd, '|', r3[3][:80])
                check(rd == ['done', False], f'reserved job: done after fitting both parts and the repair ({rd})')
        # the wrist comm: a job you could take, posted while you're free
        nt = g.ev(r"""(() => { const t0 = document.getElementById('tx').textContent; JOB_SEEN = new Set(); machinesNow();
          const j = SHIP.jobs.find(j => j.machine && j.status !== 'done' && jobTier(j) <= PLAYER_TIER && !ENGINE_KINDS.has(machineById(j.machine).kind));
          if (!j) return null; j.claimedBy = null; j.status = 'open'; delete j.start; j.found = Math.min(j.found, shipNow()); MACH_REV++; jobNotice();
          return [document.getElementById('tt').textContent, document.getElementById('tx').textContent]; })()""")
        print('  notice:', nt)
        check(nt is None or (nt[0] == 'Your device' and nt[1].startswith('New job')), f'job loop: a new job you could take should be announced ({nt})')
        # carrying two at most: a job needing three filters takes two trips
        two = g.ev(r"""(() => { machinesNow(); const j = SHIP.jobs.find(j => j.machine && j.status !== 'done' && !j.claimedBy && jobTier(j) <= PLAYER_TIER && !ENGINE_KINDS.has(machineById(j.machine).kind))
          || SHIP.jobs.find(j => j.machine && j.status !== 'done' && jobTier(j) <= PLAYER_TIER && !ENGINE_KINDS.has(machineById(j.machine).kind));
          if (!j) return null; j.claimedBy = null; j.status = 'open'; delete j.start; j.found = Math.min(j.found, shipNow()); j.parts = ['filter', 'filter', 'filter']; MACH_REV++; return claimJob(j.id) ? j.id : null; })()""")
        if two:
            g.ev("goToDeck(5); SHIP.player.carry = []"); g.step(5)
            g.ev(TAPS % '"Filters"'); s4 = jrun()
            print('  three filters needed, carrying:', s4[1], '|', s4[3][:110])
            check(s4[1] == ['filter', 'filter'] and 'another trip' in s4[3], 'job loop: two at most, and say another trip is needed')
            g.ev(f"dropJob({json.dumps(two)})")
            if g.ev("typeof returnPart === 'function'"):          # no job now: a tap in storage puts the filters back
                f0 = g.ev("SHIP.stores.filter"); g.ev(TAPS % '"Filters"'); s7 = jrun()
                print('  put back:', s7[1], '|', s7[3][:60], '| filters on the shelf', f0, '->', g.ev("SHIP.stores.filter"))
                check(s7[1] == [] and g.ev("SHIP.stores.filter") == f0 + 2, 'job loop: with no job, parts go back on the shelf')
        else: print('  (no job left to try carrying with)')
        # the cart run: a restock job (stores) is a hover cart you push: dock, cargo hold, main storage, dock
        print('  the cart run:')
        g.ev("goToDeck(5); SHIP.player.carry = []; SHIP.player.cart = null"); g.step(5)
        cj = g.ev(r"""(() => { machinesNow(); for (const j of SHIP.jobs) if (j.claimedBy === 'you' && j.status === 'claimed') dropJob(j.id);
          SHIP.hold = { filter: 3 }; const id = 'restock-stores@test'; SHIP.jobs.push({ id, machine: null, deck: 5, kind: 'restock', cargo: 'stores', urgency: 1, posted: shipNow(), found: shipNow(), claimedBy: null, parts: [], status: 'open' });
          MACH_REV++; return claimJob(id) ? [id, SHIP.stores.filter] : null; })()""")
        check(cj is not None, 'cart run: a restock job to take')
        if cj:
            IN_ROOM = "(r => { const it = ITEMS.find(i => roomAt(...cellAt(i.hit.getWorldPosition(_wp).x, _wp.z)) === r && !/tarp/i.test(i.t)); it.hit.getWorldPosition(_wp); return [it.t, playerTap(it, _wp.clone(), _wp.clone())]; })"
            CST = "JSON.stringify([SHIP.player.cart, player.holding, document.getElementById('tt').textContent + ': ' + document.getElementById('tx').textContent])"
            steps = []
            dock = g.ev("[1, 2].find(n => !(typeof cartsOut === 'function' ? cartsOut(shipNow()) : new Set()).has(n)) || 1")   # a crew run may have the other cart out
            print('    taking the cart at dock', dock)
            g.ev(TAPS % json.dumps('Cart dock %d' % dock)); c1 = jrun(); c1 = json.loads(g.ev(CST)); steps.append(c1)
            hold_room = g.ev("placeRoom('5-hold-1')")
            g.ev("playerGo(placeSpot('5-hold-2').walk)"); jrun(); g.step(90); jrun(); c2 = json.loads(g.ev(CST)); steps.append(c2)   # nothing to tap in the hold: stop there
            g.ev(f"({IN_ROOM})('r')"); jrun(); c3 = json.loads(g.ev(CST)); steps.append(c3)
            pre = g.ev("[SHIP.stores.filter || 0, SHIP.hold.filter || 0]")   # the hourly job list may have moved stock meanwhile: compare across the docking
            g.ev(TAPS % json.dumps('Cart dock %d' % dock)); jrun(); c4 = json.loads(g.ev(CST)); steps.append(c4)
            g.ev("(() => { const j = typeof turnInJob === 'function' && myJob(); if (j && j.workDone) turnInJob(j.id); })()")   # TURN_IN (0.37.3): finished jobs are turned in at the board
            fin = g.ev(f"[SHIP.jobs.find(j => j.id === {json.dumps(cj[0])}).status, SHIP.stores.filter, myJob()]")
            for st in steps: print('   ', st[0], st[1], '|', st[2][:90])
            print('    job', fin[0], '| filters on the shelf, in the hold before docking:', pre, '| on the shelf after:', fin[1])
            check(c1[0] and c1[0]['stage'] == 'empty' and c1[1] == 'cart', f'cart run: taking the cart ({c1})')
            check(c2[0] and c2[0]['stage'] == 'full' and c2[1] == 'cartfull', f'cart run: loading in the hold ({c2})')
            check(c3[0] and c3[0]['stage'] == 'done' and c3[1] == 'cart', f'cart run: unloading in storage ({c3})')
            check(c4[0] is None and not c4[1] and 'Job done' in c4[2], f'cart run: docking the cart finishes the job ({c4})')
            check(fin[0] == 'done' and pre[1] > 0 and fin[1] == pre[0] + pre[1] and fin[2] is None, f'cart run: the delivery is on the shelves ({pre} -> {fin})')
    else:
        print('The job loop: this build has no section 17 jobs (myJob, finishJob): skipped')

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
    ev("Object.assign(SHIP.player.needs, { hunger: 11, energy: 22, hygiene: 33, fitness: 44, social: 55, bathroom: 66 }); saveGame()")
    raw = json.loads(ev("localStorage.getItem(SAVE_KEY)")); print('  saved:', raw['v'], raw['player'].get('needs'))
    check(raw['v'] == 2 and raw['player']['needs'] == {'hunger': 11, 'energy': 22, 'hygiene': 33, 'fitness': 44, 'social': 55, 'bathroom': 66}, 'v 2 save should hold the needs')
    ev = load()
    v2 = json.loads(ev("JSON.stringify(SHIP.player.needs)")); print('  v 2 save:', v2)
    ev("mailSend({ from: 'Test', subject: 'Kept', body: 'b', play: 'home:gran' }); SHIP.player.credits = 77; SHIP.player.locker = ['a deck of cards']; SHIP.player.chats = { x: SHIP.time.day }; playerNameSet('Ada'); stripFold(true); saveGame()")
    ev = load()
    kept = json.loads(ev("JSON.stringify([SHIP.mail.map(m => m.subject + (m.play ? '|' + m.play : '')), SHIP.player.credits, SHIP.player.locker, Object.keys(SHIP.player.chats), SHIP.player.name])")); print('  mail, credits, locker, chats, name kept:', kept)
    fold = json.loads(ev("(() => { const el = needStrip(), r = [SHIP.player.stripFold, el.classList.contains('fold')]; el.click(); r.push(SHIP.player.stripFold, el.classList.contains('fold')); el.querySelector('.nsFold').click(); r.push(SHIP.player.stripFold); stripFold(false); return JSON.stringify(r); })()"))
    print('  the needs strip folded, kept, tapped open, folded again (0.28.33):', fold)
    check(fold == [True, True, False, False, True], f'the needs strip folds away, stays folded after a reload and a tap opens it: {fold}')
    check(kept == [['Kept|home:gran'], 77, ['a deck of cards'], ['x'], 'Ada'], f'the save should keep mail, credits, locker, chats and your name: {kept}')
    check(v2 == {'hunger': 11, 'energy': 22, 'hygiene': 33, 'fitness': 44, 'social': 55, 'bathroom': 66}, 'a v 2 save should load its needs')
    ev("localStorage.setItem(SAVE_KEY, JSON.stringify({ v: 2, build: 'x', time: { day: 2, min: 600 }, player: { deck: 4, tile: [7, 3], facing: 0, needs: { hunger: 'x', energy: 500 }, name: { x: 1 } }, ship: { decks: {} }, crew: {} })); Storage.prototype.setItem = () => {}")
    ev = load()
    bad = json.loads(ev("Storage.prototype.setItem = () => {}; JSON.stringify(SHIP.player.needs)")); print('  junk needs:', bad)
    check(ev("SHIP.player.name") is None, 'a junk name in the save should load as no name')
    check(bad == {'hunger': 80, 'energy': 100, 'hygiene': 80, 'fitness': 80, 'social': 80, 'bathroom': 80}, 'junk needs should be clamped or filled at 80')
    raw0 = ev("localStorage.getItem(SAVE_KEY)")
    ev = load('?nosave')
    ns = json.loads(ev("const n0 = NEED_KEYS.map(k => SHIP.player.needs[k]); SHIP.player.needs.hunger = 1; saveGame(); JSON.stringify([n0, localStorage.getItem(SAVE_KEY)])"))
    print('  ?nosave:', ns[0])
    check(ns[0] == [60, 100, 60, 70, 70, 60], f'?nosave should start fresh: {ns[0]}')
    wl = json.loads(ev("JSON.stringify([SHIP.mail.map(m => [m.from, m.subject, m.read]), SHIP.player.credits])")); print('  a fresh start: mail', wl[0], 'credits', wl[1])
    check(len(wl[0]) == 1 and wl[0][0][1].startswith('Welcome') and wl[0][0][2] is False and wl[1] == 40, f'a fresh start should have the welcome mail and 40 credits: {wl}')
    check(ns[1] == raw0, '?nosave should not write the save')
    nm = json.loads(ev("JSON.stringify([SHIP.player.name, playerNameSet('  Ada   Okafor '), playerNameSet(''), playerNameSet(42), playerNameSet('x'.repeat(40)).length])"))
    print('  your name (0.28.22): fresh, set, empty, junk, long:', nm)
    check(nm == [None, 'Ada Okafor', None, None, 24], f'playerNameSet cleans names: {nm}')
    # the kit bag and the device lock (0.28.26, Pillar 4): section 21's intro when it's there, else stand-ins
    kb = json.loads(ev("""(() => {
      const real = typeof introBegin === 'function', P = SHIP.player, b = document.getElementById('devBtn'), out = [];
      if (real) { introBegin(); SHIP.intro.step = 'ramp'; } else { SHIP.intro = { on: true, ended: false, step: 'ramp', done: {}, missed: [], flags: {} }; window.introOn = () => SHIP.intro.on && !SHIP.intro.ended; window.introFlag = k => !!SHIP.intro.flags[k]; }
      window.__devSet = () => real ? introFlagSet('intro.device') : (SHIP.intro.flags['intro.device'] = true);
      P.carry = []; P.locker = [];
      bagTick(); bagTick(); out.push(P.carry.slice());
      SHIP.intro.step = 'wing'; bagTick(); floatsTick(); b.click();
      out.push([bagHeld(), deviceLocked(), b.querySelector('span').textContent, typeof DEV !== 'undefined' && !!DEV.open, handsFix('Fit those first')]);
      if (typeof returnPart === 'function' && typeof jobEnd === 'function') { P.carry.push('valve'); jobEnd({ kind: 'stow' }); out.push(P.carry.slice()); } else out.push(['kitbag']);
      SHIP.intro.done.bunk = SHIP.time.min; SHIP.intro.missed.push('bunk'); SHIP.intro.step = 'toMess'; bagTick();
      out.push([bagHeld(), P.locker.slice()]);              // a missed bunk: still in your hands
      const d4 = DECKS[4], bunk = d4 && Object.keys(d4.rooms).find(k => d4.rooms[k].name === 'Bunk 1'); let cell = null;
      if (deckDef.num === 4 && bunk) for (let j = 0; j < d4.map.length && !cell; j++) for (let i = 0; i < d4.map[j].length; i++) if (d4.map[j][i] === bunk) { cell = [i, j]; break; }
      const pt = cell ? cellPos(...cell) : null;
      out.push([!!pt, pt ? bagLockerTap(new THREE.Vector3(pt.x, 0, pt.z)) : null, bagLockerTap(new THREE.Vector3(999, 0, 999))]);
      return JSON.stringify(out);
    })()"""))
    for _ in range(60):                                  # frames are stepped by hand here (window.__step)
        page.evaluate('window.__step(30, 1000 / 30)')
        if ev('!bagHeld()'): break
    walked = ev('!bagHeld()')
    kb2 = json.loads(ev("""(() => {
      const P = SHIP.player, b = document.getElementById('devBtn'), out = [P.locker.slice()];
      P.carry = ['kitbag']; P.locker = []; SHIP.intro.missed = []; bagTick();   // the bunk step done: it goes in by itself
      __devSet(); floatsTick(); b.click();
      out.push([bagHeld(), P.locker.slice(), deviceLocked(), b.querySelector('span').textContent, typeof DEV === 'undefined' || !!DEV.open]);
      if (typeof deviceClose === 'function') deviceClose();
      P.carry = ['kitbag']; SHIP.intro.ended = true; bagTick();      // the intro off with the bag in hand: quietly to the locker
      out.push([bagHeld(), P.locker.length, handsFix('Fit those first')]);
      return JSON.stringify(out);
    })()"""))
    print('  kit bag and device lock (0.28.26):', kb, walked, kb2)
    # the arrival dinner (0.28.28): at your table for the Chief's step, idle, you sit down by yourself, once
    dn0 = json.loads(ev("""(() => {
      const real = typeof introBegin === 'function';
      if (real) { introBegin(); setShipNow(introAbs(0, 1111)); for (const st of INTRO_STEPS) { if (st.id === 'chief') break; SHIP.intro.done[st.id] = introAbs(0, st.at); } }
      else { SHIP.intro = { on: true, ended: false, done: {}, missed: [], flags: {} }; window.introStepById = id => id === 'chief' ? { id, checkpoint: { deck: 3, tile: [28, 2] } } : null; }
      SHIP.intro.step = 'chief'; SHIP.player.carry = []; actEnd(true); goToDeck(3);
      const w = cellPos(28, 2), c = nearestOpen(w.x, w.z, player); player.obj.position.copy(cellPos(...c)); player.path.length = 0;
      const mine = typeof introSeat === 'function' ? introSeat('you') : null, h = mine && heldBy(mine);   // crew already heading for your seat?
      return JSON.stringify([real, c, h ? h.p.id : null]); })()"""))
    for _ in range(10): page.evaluate('window.__step(15, 1000 / 30)')
    dn = json.loads(ev("JSON.stringify([ACT && ACT.kind, ACT && ACT.phase, ACT && ACT.placeId, DINNER_SAT, typeof introSeat === 'function' ? introSeat('you') : null])"))
    print('  the arrival dinner (0.28.28):', dn0, dn)
    check(dn[0] == 'sit' and dn[1] == 'do' and str(dn[2]).startswith('3-mess') and dn[3] is True and (dn[4] is None or dn[2] == dn[4] or dn0[2]), f'at your table for the dinner you sit down (in your own seat when section 21 names one and nobody is heading for it): {dn}')
    ev("actEnd(true); SHIP.intro.ended = true; goToDeck(4)")
    nd = json.loads(ev("JSON.stringify([DINNER_SAT, (playerNew(), DINNER_SAT)])")); print('  seated at the dinner, then after a new game:', nd)
    check(nd == [True, False], f'a new game lets the next arrival dinner seat you again (reviewer 1): {nd}')
    check(kb[0] == ['kitbag'], f'at the ramp you hold one kit bag: {kb[0]}')
    check(kb[1] == [True, True, 'No device yet', False, 'Put your bag in your locker first'], f'before the bunk: the bag held, the device locked and shut: {kb[1]}')
    check(kb[2] == ['kitbag'], f'main storage takes back parts, never the kit bag: {kb[2]}')
    check(kb[3] == [True, []], f'a missed bunk step leaves the bag in your hands: {kb[3]}')
    check(kb[4] == [True, True, False] and walked and kb2[0] == ['kitbag'], f'a tap in Bunk 1 walks you there and stows the bag: {kb[4]} {walked} {kb2[0]}')
    check(kb2[1] == [False, ['kitbag'], False, 'Device', True], f'the bunk step done: the bag in your locker, the device opens: {kb2[1]}')
    check(kb2[2] == [False, 1, 'Fit those first'], f'the intro off: the bag goes to the locker once: {kb2[2]}')
    ev("localStorage.removeItem(SAVE_KEY)")
    b.close()

print('errors', errors[:5])
if errors: fail('page errors')
print('PLAYER CHECK OK' if ok else 'PLAYER CHECK FAILED')
sys.exit(0 if ok else 1)
