# Starship Cadet: interactions check (keep in the repo, next to player_check.py)
# Checks section 15b (the interactions engineer): more places to use, the job board, the goal pointer.
#   parity: tapping the real things on the real decks starts the crew's activity there (the bar, lounges, reading
#   seats, benches, the garden, the music room, the laundry, basins, the kettle, the telescope, the observatory),
#   with a pose, and the main need rises; places crew hold are "In use"; private cabins, beds, notices and
#   section 15's own taps (treadmill, shower) are left alone; walking away stops it; draw calls stay under BUDGET
#   the job board: tapping it opens the list; Take it claims the job (section 17's claimJob); Drop it puts it back
#   the goal pointer: hidden with no goal; your job's next step shows by itself; on another deck it says "Take the
#   lift to Deck N"; setGoal / clearGoal; an arrow at the screen edge when the place is off screen, a marker when on
# Setup and environment as for cadet_test.py.
# Run:  python3 interactions_check.py BUILD.html
import sys, json
exec(open(__file__.replace('interactions_check.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright

BUDGET = 450
ok = True
def check(cond, msg):
    global ok
    if not cond: ok = False; print('FAIL', msg)
    return cond

# stand by a thing (by title, nearest a tile if given) and tap it, as section 11 would
TAP = r"""(({ title, near, place }) => {
  const its = ITEMS.filter(i => i.t === title); if (!its.length) return 'no item';
  const c = near ? cellPos(...near) : null;
  const it = its.map(i => { i.hit.getWorldPosition(_wp); return [i, _wp.clone()]; }).sort((a, b) => c ? a[1].distanceTo(c) - b[1].distanceTo(c) : 0)[0];
  if (place !== false) { const g = nearestOpen(it[1].x, it[1].z, player); player.obj.position.copy(cellPos(...g)); player.stop(); }
  return playerTap(it[0], it[1].clone(), it[1].clone());
})"""
STATE = r"""JSON.stringify({ act: ACT && [ACT.kind, ACT.placeId, ACT.phase, ACT.pose, Math.round(ACT.done * 10) / 10],
  needs: Object.fromEntries(NEED_KEYS.map(k => [k, Math.round(SHIP.player.needs[k] * 10) / 10])), visible: player.obj.visible,
  toast: document.getElementById('tt').textContent + ': ' + document.getElementById('tx').textContent, calls: renderer.info.render.calls,
  goal: document.getElementById('ixGoal').hidden ? null : document.querySelector('#ixGoal .ixlab').textContent,
  arrow: document.querySelector('#ixGoal .ixarr').style.display !== 'none', board: !document.getElementById('ixBoard').hidden })"""

# deck, title, the kind expected, the need that must rise (None: just that it starts and ends)
PARITY = [
    (3, 'The bar', 'ixDrink', 'hunger'), (3, 'Sofa', None, 'social'), (3, 'Herb bed', 'ixGarden', 'social'),
    (3, 'Water', 'ixWater', 'hunger'), (3, 'Telescope', 'ixStars', 'energy'), (3, 'Pond', 'ixRest', 'energy'),
    (4, 'Folding table', 'ixFold', 'hygiene'), (4, 'Grand piano', 'ixMusic', 'social'), (4, 'Kettle', 'ixTea', 'hunger'),
    (4, 'Basins', 'ixBasin', 'hygiene'), (4, 'Tiles table', 'ixLounge', 'social'), (4, 'Beanbags', None, None),
    (5, 'Armchair', None, None), (5, 'Hot water', 'ixTea', 'hunger'), (1, 'Window seat', None, None),
]

with sync_playwright() as pw:
    g = Game(pw, sys.argv[1])
    st = lambda: json.loads(g.ev(STATE))
    tap = lambda title, near=None, place=True: g.ev(f"({TAP})({json.dumps({'title': title, 'near': near, 'place': place})})")
    check(g.ev("typeof PLAYER_TAPS !== 'undefined' && PLAYER_TAPS.includes(ixTap)"), 'section 15 has the PLAYER_TAPS hook with ixTap in it')
    check(st()['goal'] is None, 'no goal at the start: the pointer is hidden')
    peak = 0

    print('== parity')
    for deck, title, kind, need in PARITY:
        g.ev(f"goToDeck({deck})"); g.step(3)
        g.ev("for (const k of NEED_KEYS) SHIP.player.needs[k] = 50")
        r = tap(title); g.step(2); s0 = st()
        if not check(r is True and s0['act'], f'Deck {deck} {title}: an activity starts ({r}, {s0["toast"][:80]})'): continue
        if kind: check(s0['act'][0] == kind, f'Deck {deck} {title}: {kind}, got {s0["act"][0]}')
        check(s0['act'][0] in ('gym',) or s0['act'][0].startswith('ix'), f'{title}: one of ours')
        n0, seen = s0['needs'], []
        for k in range(200):
            g.step(30); s = st(); peak = max(peak, s['calls'])
            if s['act']: seen.append(s['act'])
            else: break
        poses = sorted({a[3] for a in seen if a[2] == 'do' and a[3]})
        d = {k: round(s['needs'][k] - n0[k], 1) for k in n0}
        print(f'   Deck {deck} {title}: {s0["act"][0]} {poses} {d} | {s["toast"][:70]}')
        check(not s['act'] and s['visible'], f'{title}: done, back on your feet and visible')
        check(poses, f'{title}: a pose while doing it')
        if need: check(d[need] > 0, f'{title}: {need} rose ({d[need]})')

    print('== held, private and other taps')
    g.ev("goToDeck(3)"); g.step(3)
    g.ev("window.__busy = [...PLACE_OF.keys()]; for (const id of __busy) BUSY.add(id)")
    tap('The bar'); s = st()
    g.ev("for (const id of __busy) BUSY.delete(id)")
    check(not s['act'] and s['toast'].split(': ', 1)[1].startswith('In use'), f'every bar stool held: "In use" ({s["toast"][:70]})')
    tap('Treadmills'); g.step(2); s = st()
    check(s['act'] and s['act'][0] == 'gym', f'the treadmill is still section 15\'s workout ({s["act"]})')
    g.ev("actEnd(true)")
    check(g.ev("ixTap(ITEMS.find(i => i.t === 'Health notices') || ITEMS.find(i => /notice/i.test(i.t)), new THREE.Vector3(), new THREE.Vector3())") is False, 'a notice board reads as before')
    g.ev("goToDeck(2)"); g.step(3)
    priv = g.ev("[...PLACE_OF.values()].filter(pl => pl.type === 'lounge-seat' && privatePlace(pl)).length")
    r = g.ev("(() => { const pl = [...PLACE_OF.values()].find(q => q.type === 'lounge-seat' && privatePlace(q)); const s = placeSpot(pl.id); const it = ITEMS.map(i => { i.hit.getWorldPosition(_wp); return [i, _wp.distanceTo(new THREE.Vector3(s.x, _wp.y, s.z))]; }).sort((a, b) => a[1] - b[1])[0][0]; it.hit.getWorldPosition(_wp); return [it.t, ixTap(it, _wp.clone(), _wp.clone())]; })()")
    check(priv > 0 and r[1] is False, f'a seat in someone\'s cabin is left alone ({r})')
    g.ev("goToDeck(4)"); g.step(3)
    r = g.ev("(() => { const it = ITEMS.find(i => /^Washer/.test(i.t)); it.hit.getWorldPosition(_wp); return [it.t, ixMachine(_wp.clone()), ixTap(it, _wp.clone(), _wp.clone())]; })()")
    print('   washer:', r)
    if r[1]: check(r[2] is False, 'a washer (a machine) is the machine\'s tap, not ours')
    g.ev("actEnd(true)"); tap('Folding table'); g.step(40); check(st()['act'], f'at the folding table ({st()["toast"][:80]})')
    g.ev("player.steer = { x: 1, z: 0, k: 1 }"); g.step(10); g.ev("player.steer = null"); g.step(5); s = st()
    check(not s['act'] and s['visible'], 'walking away stops it')

    print('== the job board and the goal pointer')
    g.ev("goToDeck(5)"); g.step(3)
    r = tap('Job board'); g.step(150); s = st()
    check(r is True and s['board'], 'tapping the job board opens the list')
    # a job you can take, on Deck 3 (a tier 1 machine there), in case the crew have left none
    job = g.ev(r"""(() => { const t = shipNow(); const m = machineList().find(m => m.deck === 3 && !m.stub && jobTier({ machine: m.id }) <= PLAYER_TIER && !ENGINE_KINDS.has(m.kind) && PLACE_OF && panelPlace(m.id));
      if (!m) return null; const part = MACHINE_KINDS[m.kind].part || 'gasket'; SHIP.stores[part] = Math.max(SHIP.stores[part] || 0, 2);
      SHIP.jobs.push({ id: 'ixtest@1', machine: m.id, deck: 3, kind: 'repair', urgency: 1, posted: t, found: t, claimedBy: null, parts: [part], status: 'open' }); MACH_REV++;
      return [m.id, part]; })()""")
    check(job, f'a test job posted ({job})')
    g.ev("ixBoard.draw()")
    rows = g.ev("document.querySelectorAll('#ixBoardL .ixjob').length")
    check(rows >= 1, f'the board lists jobs ({rows})')
    took = g.ev("ixBoard.take('ixtest@1')"); g.step(3); s = st()
    check(took and g.ev("(myJob() || {}).id") == 'ixtest@1' and not s['board'], 'Take it: the job is yours and the board closes')
    print('   goal:', s['goal'])
    check(s['goal'] and 'storage' in s['goal'], f'the pointer: fetch from main storage ({s["goal"]})')
    g.ev("goToDeck(4)"); g.step(3); s = st()
    check(s['goal'] and s['goal'].startswith('Take the lift to Deck 5'), f'another deck: take the lift ({s["goal"]})')
    g.ev("SHIP.player.carry = [" + json.dumps(job[1]) + "]"); g.step(40); s = st()
    check(s['goal'] and s['goal'].startswith('Take the lift to Deck 3') and 'epair' in s['goal'], f'parts in hand: to the machine ({s["goal"]})')
    g.ev("goToDeck(3)"); g.step(3); s = st()
    check(s['goal'] and s['goal'].startswith('Repair the'), f'on its deck: repair it ({s["goal"]})')
    # off screen: an arrow; on screen: the marker
    g.ev("setGoal({ deck: 3, at: [0, 0], label: 'Far corner' })"); g.step(2); s = st()
    check(s['goal'] == 'Far corner', 'setGoal overrides the job\'s goal')
    far = s['arrow']
    g.ev("(() => { const h = player.here(); setGoal({ deck: 3, at: h, label: 'Right here' }); })()"); g.step(2); s = st()
    check(s['goal'] == 'Right here' and not s['arrow'], 'a goal on screen: the marker, no arrow')
    check(far, 'a goal off screen: an arrow at the edge')
    g.ev("clearGoal()"); g.step(2); s = st()
    check(s['goal'] and s['goal'].startswith('Repair the'), 'clearGoal: back to the job')
    g.ev("goToDeck(5)"); g.step(3); tap('Job board'); g.step(150)
    g.ev("document.querySelector('#ixBoardL .ixjob button').click()"); g.step(3); s = st()
    check(not g.ev("myJob()") and s['goal'] is None, 'Drop it: no job and the pointer hides')
    g.ev("ixBoard.close(); SHIP.player.carry = []")
    print('   draw-call peak while doing things:', peak)
    check(peak < BUDGET, f'draw calls under {BUDGET} ({peak})')
    check(not g.errors, f'no console errors ({g.errors[:3]})')
    g.close()

print('INTERACTIONS CHECK OK' if ok else 'INTERACTIONS CHECK FAILED')
sys.exit(0 if ok else 1)
