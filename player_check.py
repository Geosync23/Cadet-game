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
STATE = r"""JSON.stringify({ act: ACT && [ACT.kind, ACT.placeId, ACT.phase, ACT.pose, Math.round(ACT.done * 10) / 10, player.holding === undefined ? null : player.holding, typeof TRAY_ON !== 'undefined' && TRAY_ON.visible],
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
    for k, v in p['lo'].items(): check(v >= (25 if k == 'energy' else 30), f'normal week: {k} fell to {v}')
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
    for key, want in [('80/80', 1.05), ('20/80', .8), ('80/20', .84), ('20/20', .64), ('25/25', 1)]:   # fit (75+): 105% (0.28.9)
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
    dv = g.ev(r"""(() => { Object.assign(SHIP.player.needs, { hunger: 80, energy: 50, hygiene: 10, fitness: 50, social: 50 }); device.open();
      const b = document.getElementById('devBody'), out = [[...b.querySelectorAll('.need em')].map(e => e.className + ':' + e.textContent), [...b.querySelectorAll('p.fx')].map(p => p.textContent)];
      device.close(); Object.assign(SHIP.player.needs, NEEDS_FRESH); return out; })()""")
    print('  the device:', dv)
    check(dv[0] == ['up:▲', 'down:▼'] and len(dv[1]) == 2 and 'fed' in dv[1][0] and 'wash' in dv[1][1], f'device marks: {dv}')

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
    g.ev("setShipNow(Math.floor(shipNow() / 1440) * 1440 + 21 * 60); needsT = null; SHIP.player.needs.energy = 30"); g.step(3)
    day0 = g.ev("SHIP.time.day"); g.ev(BED); asked = g.ev("!sleepEl.hidden")
    g.page.wait_for_function("window.__sc('!sleeping')", timeout=10000, polling=200); g.step(3)
    bed = g.ev("[SHIP.time.day, hhmm(SHIP.time.min), Math.round(SHIP.player.needs.energy), document.getElementById('tt').textContent]"); print('  at 21:00:', bed, 'dialog shown:', asked)
    check(not asked and bed[0] == day0 + 1 and bed[1] == '06:00' and bed[2] == 100 and bed[3] == 'Good morning', f'the bunk at 21:00 should sleep you to 06:00: {bed}')

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
    check(isinstance(e['basket'], dict) and e['basket'].get('price', 0) > 0, f"browsing should leave something to pay for ({e['basket']})")
    cr0, hu0 = g.ev("SHIP.player.credits"), e['needs']['hunger']
    tp, b, seen, e, pk = run_activity(g, 'Counter'); peak = max(peak, pk); body_check('pay', None, 0, b, e, seen, 'pay')
    check(e['basket'] is None, 'paying should empty the basket')
    cr1 = g.ev("SHIP.player.credits"); print('  credits', cr0, '->', cr1, '|', e['toast'][:100])
    check(cr1 == cr0 - b['basket']['price'] and e['toast'].startswith('Paid'), f"paying should cost {b['basket']['price']} credits: {cr0} -> {cr1}")
    if b['basket']['kind'] == 'comfort': check(g.ev("SHIP.player.locker.includes(%s)" % json.dumps(b['basket']['name'])), 'a comfort goes in your locker')
    else: check(e['needs']['hunger'] > hu0, 'a snack should feed you a little')
    g.ev("setShipNow(Math.floor(shipNow() / 1440) * 1440 + 17 * 60 + 40); needsT = null"); g.step(5)   # dinner
    tp, b, seen, e, pk = run_activity(g, 'Servery', label='Servery, then a seat'); peak = max(peak, pk)
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

    print('The store (credits, snacks, comforts):')
    sh = g.ev(r"""(() => { const P = SHIP.player, n = P.needs; P.credits = 20; P.locker = []; n.social = 50; n.hunger = 50;
      basket = storePick('comfort'); ACT = { kind: 'pay', def: PLAYER_ACTS.pay, o: {}, face: 0 }; actEnd(false); const a = [P.credits, P.locker.slice(), Math.round(n.social), basket];
      basket = storePick('snack'); ACT = { kind: 'pay', def: PLAYER_ACTS.pay, o: {}, face: 0 }; actEnd(false); const b = [P.credits, P.locker.length, Math.round(n.hunger)];
      P.credits = 1; basket = storePick('comfort'); const it = ITEMS.find(i => i.t === 'Counter'); it.hit.getWorldPosition(_wp); const r = playerTap(it, _wp.clone(), _wp.clone());
      const c = [r, !!ACT, basket, document.getElementById('tx').textContent]; P.credits = 40; return [a, b, c]; })()""")
    print(' ', sh)
    check(sh[0][1] and sh[0][0] < 20 and sh[0][2] > 50 and sh[0][3] is None, f'a comfort: credits down, in the locker, social up: {sh[0]}')
    check(sh[1][0] < sh[0][0] and sh[1][1] == len(sh[0][1]) and sh[1][2] > 50, f'a snack: credits down, eaten (food up), not in the locker: {sh[1]}')
    check(sh[2][0] is True and not sh[2][1] and sh[2][2] is None and 'credits' in sh[2][3], f'not enough credits: a toast, no sale: {sh[2]}')

    print('Social from chatting and company:')
    ch = g.ev(r"""(() => { const n = SHIP.player.needs, out = []; SHIP.player.chats = {};
      const chat = (who, hy) => { n.social = 50; n.hygiene = hy; playerChat({ id: who, name: 'Test ' + who }); return Math.round((n.social - 50) * 10) / 10; };
      out.push(chat('a', 50), chat('a', 50), chat('b', 80), chat('c', 10), document.getElementById('tx').textContent.includes('nose'));
      setShipNow(shipNow() + 1440); out.push(chat('a', 50)); setShipNow(shipNow() - 1440); n.hygiene = 50; return out; })()""")
    print('  first chat, again, clean, unwashed (and the remark), next day:', ch)
    check(ch[:4] == [6, 1, 9, 3] and ch[4] is True and ch[5] == 6, f'chatting: {ch}')
    cp = g.ev(r"""(() => { const n = SHIP.player.needs, seats = [...PLACE_OF.values()].filter(q => q.type === 'mess-seat'), s0 = placeSpot(seats[0].id);
      const near = seats.slice(1).map(q => [q, placeSpot(q.id)]).filter(([, s]) => s && Math.hypot(s.x - s0.x, s.z - s0.z) < COMPANY_NEAR).slice(0, 4);
      const fake = near.map(([q, s]) => ({ settled: true, goalId: q.id, x: s.x, z: s.z, p: { name: 'Test' } })); const out = [];
      for (const k of [0, 2, 4]) {
        DECK_CREW.push(...fake.slice(0, k)); Object.assign(n, { hunger: 50, social: 50, hygiene: 50, energy: 50, fitness: 50 });
        FX_MIN = Math.floor(shipNow()); FX_NOW = { deck: deckDef.num, restore: {}, drain: {}, notes: [] };
        ACT = { kind: 'eat', def: PLAYER_ACTS.eat, phase: 'do', done: 0, o: {}, spot: s0, deck: deckDef, x: 0, z: 0, y: 0, face: player.face, to: {}, body: { set() {}, update() {}, dispose() {} } };
        needsT = shipNow() - 10; playerUpdate(0, 0); out.push([company(ACT), Math.round((n.social - 50 + NEED_DRAIN.social[0] / 6) * 10) / 10]);
        DECK_CREW.splice(DECK_CREW.length - k, k); ACT = null; }
      FX_MIN = -1; return [near.length, out]; })()""")
    print('  ten minutes eating with 0, 2, 4 (counts as 3) at the table: [company, social gained]', cp)
    if check(cp[0] >= 3, f'company: need three mess seats near each other ({cp[0]})'):
        check(all(abs(gn - 2 * min(c, 3)) < .15 for c, gn in cp[1]) and cp[1][1][0] - cp[1][0][0] == 2 and cp[1][2][0] - cp[1][0][0] == 4,
              f'company at the table: +0.2 a minute for each of up to three ({cp[1]}; the first is whoever was already eating)')

    print('Mail:')
    ml = g.ev(r"""(() => { SHIP.mail = []; device.refresh(); const b = document.getElementById('devMail'), out = [b.hidden];
      mailSend({ from: 'Stores', subject: 'Filters low', body: 'Two left.' }); mailSend({ at: shipNow() - 5, from: 'Galley', subject: 'Cake tonight', body: 'Tomas turns 24.' });
      out.push(b.hidden, b.textContent, mailUnread(), SHIP.mail.map(m => m.subject));
      device.open(); device.show('mail'); const body = document.getElementById('devBody');
      out.push([...body.querySelectorAll('.tabs button')].map(x => x.textContent), body.querySelectorAll('button.mail').length);
      body.querySelector('button.mail').click(); out.push(mailUnread(), document.getElementById('devBody').textContent.includes('Two left.'));
      device.show('status'); device.close(); return out; })()""")
    print(' ', ml)
    check(ml[0] is True and ml[1] is False and ml[2] == '2' and ml[3] == 2, f'mail: the unread count on the button: {ml[:4]}')
    check(ml[4] == ['Filters low', 'Cake tonight'] and ml[5] == ['Status', 'Mail (2)'] and ml[6] == 2, f'mail: the Mail tab, newest first: {ml[4:7]}')
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
      const m = stubTap(it, _wp.clone()); return [it.t, m && m[0].id]; })()""")
    print('  a washer (a stub machine, matched by name and number):', wt)
    check(wt is None or (wt[1] and wt[1].endswith('-' + wt[0].split()[-1]) and 'washer' in wt[1]), f'a washer tap should find its stub machine: {wt}')
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

    print('Squeezing past settled crew (the galley plant, Deck 3):')
    sq = g.ev(r"""(() => { const blocker = { settled: true, spot: { onTile: true, walk: [39, 4], pose: 'work', x: cellPos(39, 4).x, z: cellPos(39, 4).z }, x: cellPos(39, 4).x, z: cellPos(39, 4).z,
        goalId: 'test', p: { name: 'Test Brennan', role: 'Chef', id: 'test' }, update() { return true; }, remove() {}, h: { set() {} } };
      window.__blocker = blocker; DECK_CREW.push(blocker);
      const goal = [39, 1], here = player.here(), avoid = occupiedBy(player);
      const walled = !findPath(here, goal, avoid, player), went = playerGo(goal);
      return [walled, went, player.path.some(c => c[0] === 39 && c[1] === 4)]; })()""")
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
            check(g.ev("player.holding") is False, 'job loop: with the parts fitted, the crate goes')
            if g.ev("typeof touchJob === 'function'"):
                tc = g.ev(f"(() => {{ const j = SHIP.jobs.find(j => j.id === {json.dumps(jid)}); return [j.touched || 0, j.start, shipNow()]; }})()")
                print('  touched (section 17\'s touchJob):', tc)
                check(tc[0] > tc[1] and tc[2] - tc[0] < 3, 'job loop: repairing should touch the job (keeps it yours)')
            sv = json.loads(g.ev("(() => { const s = { player: {} }; for (const f of SAVE_EXTRA) try { f(s); } catch (e) {} return JSON.stringify(s.player); })()"))
            check(sv.get('work', {}).get('done', 0) >= 4 and sv.get('carry') == [], f"job loop: the save should hold the work ({sv.get('work')})")
            g.step(60); check(g.ev(TAPI) is True, 'job loop: resume'); s3 = jrun(160)
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
    ev("Object.assign(SHIP.player.needs, { hunger: 11, energy: 22, hygiene: 33, fitness: 44, social: 55 }); saveGame()")
    raw = json.loads(ev("localStorage.getItem(SAVE_KEY)")); print('  saved:', raw['v'], raw['player'].get('needs'))
    check(raw['v'] == 2 and raw['player']['needs'] == {'hunger': 11, 'energy': 22, 'hygiene': 33, 'fitness': 44, 'social': 55}, 'v 2 save should hold the needs')
    ev = load()
    v2 = json.loads(ev("JSON.stringify(SHIP.player.needs)")); print('  v 2 save:', v2)
    ev("mailSend({ from: 'Test', subject: 'Kept', body: 'b' }); SHIP.player.credits = 77; SHIP.player.locker = ['a deck of cards']; SHIP.player.chats = { x: SHIP.time.day }; saveGame()")
    ev = load()
    kept = json.loads(ev("JSON.stringify([SHIP.mail.map(m => m.subject), SHIP.player.credits, SHIP.player.locker, Object.keys(SHIP.player.chats)])")); print('  mail, credits, locker, chats kept:', kept)
    check(kept == [['Kept'], 77, ['a deck of cards'], ['x']], f'the save should keep mail, credits, locker and chats: {kept}')
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
    wl = json.loads(ev("JSON.stringify([SHIP.mail.map(m => [m.from, m.subject, m.read]), SHIP.player.credits])")); print('  a fresh start: mail', wl[0], 'credits', wl[1])
    check(len(wl[0]) == 1 and wl[0][0][1].startswith('Welcome') and wl[0][0][2] is False and wl[1] == 40, f'a fresh start should have the welcome mail and 40 credits: {wl}')
    check(ns[1] == raw0, '?nosave should not write the save')
    ev("localStorage.removeItem(SAVE_KEY)")
    b.close()

print('errors', errors[:5])
if errors: fail('page errors')
print('PLAYER CHECK OK' if ok else 'PLAYER CHECK FAILED')
sys.exit(0 if ok else 1)
