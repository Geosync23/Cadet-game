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
    (3, 'Water', 'ixWater', 'hunger'), (3, 'Telescope', 'ixStars', 'energy'),
    (4, 'Folding table', 'ixFold', 'hygiene'), (4, 'Grand piano', 'ixMusic', 'social'), (4, 'Kettle', 'ixTea', 'hunger'),
    (4, 'Basins', 'ixBasin', 'hygiene'), (4, 'Tiles table', 'ixLounge', 'social'),
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
    r = g.ev("(() => { const it = ITEMS.find(i => i.t === 'Bench'); it.hit.getWorldPosition(_wp); return ixTap(it, _wp.clone(), _wp.clone()); })()")
    check(r is False, 'a plain bench is section 15\'s sit-anywhere, not ours')
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
    if g.ev("typeof actProgress === 'function'"):          # 0.37.8: the goal marker steps aside while section 15's progress bar shows
        g.ev(f"({TAP})({{title: 'Folding table'}})"); g.ev("(() => { setGoal({ deck: 4, at: player.here(), label: 'Laundry' }); })()"); g.step(60); s = st()
        check(s['act'] and not s['goal'] and g.ev("!!actProgress()"), f'the goal marker hides while the progress bar shows ({s["act"]}, {s["goal"]})')
        g.ev("player.steer = { x: 1, z: 0, k: 1 }"); g.step(10); g.ev("player.steer = null"); g.step(5); s = st()
        check(not s['act'] and s['goal'] == 'Laundry', f'and comes back when it ends ({s["goal"]})')
        g.ev("clearGoal()")

    print('== the job board and the goal pointer')
    # the first tips (C13): a stand-in tipShow records which fire, when the build has none of its own (the device's, 19)
    g.ev("if (typeof tipShow === 'undefined') window.tipShow = (id, text) => { (window.__tips = window.__tips || []).push(id); return true; }")
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
    g.step(2); check(g.ev("player.holding") == 'toolbox', f'a repair job: a toolbox in hand ({g.ev("player.holding")!r})')
    print('   goal:', s['goal'])
    check(s['goal'] and 'storage' in s['goal'], f'the pointer: fetch from main storage ({s["goal"]})')
    check(g.ev("SHIP.player.track") == 'ixtest@1', f'taking a job tracks it ({g.ev("SHIP.player.track")})')
    g.ev("SHIP.player.track = null"); g.step(3); s = st()
    check(s['goal'] is None, f'tracking switched off (the device): no job arrow ({s["goal"]})')
    sv = g.ev("(() => { const s = { player: {} }; for (const f of SAVE_EXTRA) try { f(s); } catch (e) {} return s.player.track; })()")
    check(sv is None and g.ev("(() => { const s = { player: {} }; for (const f of SAVE_EXTRA) try { f(s); } catch (e) {} return 'track' in s.player; })()"), 'the save keeps tracking off')
    g.ev("SHIP.player.track = myJob().id"); g.step(3); s = st()
    g.ev("goToDeck(4)"); g.step(3); s = st()
    check(s['goal'] and s['goal'].startswith('Take the lift to Deck 5'), f'another deck: take the lift ({s["goal"]})')
    g.ev("SHIP.player.carry = [" + json.dumps(job[1]) + "]"); g.step(40); s = st()
    check(s['goal'] and s['goal'].startswith('Take the lift to Deck 3') and 'epair' in s['goal'], f'parts in hand: to the machine ({s["goal"]})')
    g.ev("goToDeck(3)"); g.step(3); s = st()
    check(s['goal'] and s['goal'].startswith('Repair the'), f'on its deck: repair it ({s["goal"]})')
    g.ev("(() => { const m = machineById(myJob().machine), sp = placeSpot(panelPlace(m.id)); player.obj.position.copy(cellPos(...sp.walk)); player.stop(); })()"); g.step(45)
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
    check(not g.ev("myJob()") and s['goal'] is None, f'Drop it: no job and the pointer hides ({g.ev("JSON.stringify(myJob())")}, {s["goal"]}, board {s["board"]}, {s["toast"][:80]})')
    g.ev("ixBoard.close(); SHIP.player.carry = []")
    # a cart run (section 15's cartTap): the pointer starts at the Cart bay's docks
    if g.ev("typeof jobStops === 'function'"):
        g.ev("(() => { const t = shipNow(); SHIP.jobs.push({ id: 'ixcart@1', machine: null, deck: 5, kind: 'restock', cargo: 'meals', urgency: 1, posted: t, found: t, claimedBy: null, parts: [], status: 'open' }); MACH_REV++; })()")
        took = g.ev("claimJob('ixcart@1')"); g.step(3); s = st()
        check(took and s['goal'] and 'Cart bay' in s['goal'], f'a cart run: take a cart from the Cart bay ({took}, {s["goal"]})')
        g.ev("dropJob('ixcart@1')"); g.step(3)
    # chores without a machine (0.37.3): fetch, each stop, work done, turn it in at the board
    if g.ev("typeof jobStepDone === 'function' && typeof CHORES !== 'undefined'"):
        print('== chores')
        g.ev("TURN_IN = true")   # on in the build from 0.37.3; set anyway, so the check also works on older builds
        # stand by the thing nearest a place and tap it, the way a player would
        TAPAT = r"""(({ place }) => { const s = placeSpot(place); if (!s) return 'no spot';
          const it = ITEMS.filter(i => !i.lift && !i.see).map(i => [i, ixDist(i, s)]).sort((a, b) => a[1] - b[1])[0][0];
          it.hit.getWorldPosition(_wp); const g = nearestOpen(_wp.x, _wp.z, player); player.obj.position.copy(cellPos(...g)); player.stop();
          return [it.t, playerTap(it, _wp.clone(), _wp.clone())]; })"""
        def walk_stop(label):
            for k in range(200):
                g.step(30); s = st()
                if not s['act']: break
            return s
        for kind in ['lamp', 'delivery']:
            job = g.ev(f"""(() => {{ const c = choreWhere('{kind}')[0]; if (!c) return null; const C = CHORES['{kind}'], t = shipNow();
              (C.parts || []).forEach(p => SHIP.stores[p] = Math.max(SHIP.stores[p] || 0, 3));
              const j = {{ id: 'ixchore-{kind}@1', machine: null, deck: c.deck, room: c.room, kind: 'chore', chore: '{kind}', target: c.key, title: c.title, bring: c.bring || null, tier: 1,
                stops: c.stops.map(x => ({{ ...x }})), urgency: 0, posted: t, found: t, claimedBy: null, parts: C.parts.slice(), status: 'open' }};
              SHIP.jobs.push(j); MACH_REV++; return [j.id, j.title, jobStops(j).map(x => x.step + '@' + x.deck + ':' + (x.places[0] || '-'))]; }})()""")
            if not check(job, f'a {kind} chore to test'): continue
            print('  ', job)
            g.ev("goToDeck(5)"); g.step(3)
            took = g.ev(f"claimJob('{job[0]}')"); g.step(3)
            check(took, f'{kind}: taken')
            stops = g.ev(f"jobStops(myJob()).map(x => [x.step, x.deck, x.places[0] || null])")
            for i, (step, deck, place) in enumerate(stops):
                s = st(); print('    goal before', step, ':', s['goal'])
                check(s['goal'] and ('storage' in s['goal'] if step == 'fetch' else (f'Deck {deck}' in s['goal'] if g.ev('deckDef.num') != deck else True)), f'{kind} {step}: the pointer leads there ({s["goal"]})')
                if g.ev('deckDef.num') != deck: g.ev(f"goToDeck({deck})"); g.step(3)
                if step == 'fetch':
                    r = g.ev(f"({TAP})({{title: ITEMS.find(i => roomAt(...cellAt(i.hit.getWorldPosition(_wp).x, _wp.z)) === 'r' && !/tarp/i.test(i.t)).t}})")
                else:
                    r = g.ev(f"({TAPAT})({json.dumps({'place': place})})")
                g.step(2); s0 = st()
                for tries in range(5):                       # a crew member on the walk-to tile: try again in a little while
                    if s0['act'] or 'in the way' not in s0['toast']: break
                    g.step(120); r = g.ev(f"({TAPAT})({json.dumps({'place': place})})") if step != 'fetch' else r; g.step(2); s0 = st()
                check(s0['act'] and s0['act'][0] == 'ixStop', f'{kind} {step}: the stop starts ({r}, {s0["act"]}, {s0["toast"][:80]})')
                s = walk_stop(step); g.step(3); s = st()
                done = g.ev(f"jobStops(myJob() || {{}}).map(x => !!x.done)") if g.ev("!!myJob()") else []
                check(len(done) > i and done[i], f'{kind} {step}: marked done ({done}, {s["toast"][:80]})')
                hold = g.ev("player.holding")
                want = ('carry' if kind == 'delivery' and step == 'pickup' else None if kind == 'delivery' else True if g.ev("SHIP.player.carry.length") else 'toolbox') if i < len(stops) - 1 else False
                if want is not None: check(hold == want, f'{kind} after {step}: in hand {hold!r}, want {want!r}')
            s = st()
            check(g.ev("!!(myJob() && myJob().workDone)") and s['goal'] and 'turn it in' in s['goal'].lower(), f'{kind}: work done, the pointer says turn it in ({s["goal"]})')
            check(not g.ev("SHIP.player.carry.length"), f'{kind}: the parts were used')
            g.ev("goToDeck(5)"); g.step(3)
            cr = g.ev("SHIP.player.credits || 0")
            r = tap('Job board'); g.step(150)
            btn = g.ev("(document.querySelector('#ixBoardL .ixjob button') || {}).textContent")
            check(btn == 'Turn it in', f'{kind}: the board offers Turn it in ({btn})')
            g.ev("document.querySelector('#ixBoardL .ixjob button').click()"); g.step(3); s = st()
            check(not g.ev("myJob()") and g.ev(f"SHIP.jobs.find(j => j.id === '{job[0]}').status") == 'done' and s['goal'] is None, f'{kind}: turned in, complete, no pointer ({s["toast"][:80]})')
            check(g.ev("SHIP.player.credits || 0") > cr or not g.ev("typeof JOB_PAY !== 'undefined'"), f'{kind}: paid at turn-in')
            g.ev("ixBoard.close()")
    # the ship health board (0.37.6): tapping it opens a panel with every system, the ship's health, faults and jobs
    if g.ev("typeof shipHealthRows === 'function'"):
        print('== ship health')
        g.ev("goToDeck(5)"); g.step(3)
        r = tap('Ship health'); g.step(150)
        hp = g.ev("""(() => { const el = document.getElementById('ixHealth'), b = el.getBoundingClientRect();
          return { open: !el.hidden, names: [...el.querySelectorAll('.ixbar span')].map(x => x.textContent), want: shipHealthRows().map(r => r.name),
            inside: b.left >= 0 && b.top >= 0 && b.right <= innerWidth && b.bottom <= innerHeight }; })()""")
        print('   rows:', hp['names'])
        check(r is True and hp['open'], 'tapping the ship health board opens its panel')
        check(hp['names'] == hp['want'] and len(hp['names']) >= 11, f'every system listed, the ship first ({len(hp["names"])})')
        check(hp['inside'], 'the panel is fully on screen')
        g.page.mouse.click(5, g.page.viewport_size['height'] - 5); g.step(3)
        check(g.ev("document.getElementById('ixHealth').hidden"), 'a tap outside closes it')
        g.step(200); check(g.ev("document.getElementById('ixHealth').hidden"), 'it never opens by itself')
    # real machines: their taps are section 15's machineTap (machineUse), never one of ours
    over = []
    for n in g.ev("Object.keys(DECKS).map(Number)"):
        g.ev(f"goToDeck({n})"); g.step(3)
        over += g.ev(r"""(() => { const out = []; if (typeof machineList !== 'function') return out; const near = typeof MACHINE_NEAR !== 'undefined' ? MACHINE_NEAR : 1;
          for (const it of ITEMS) { if (/job board/i.test(it.t) || it.lift || it.see) continue; it.hit.getWorldPosition(_wp); const at = _wp.clone();
            if (!machineList().some(m => m.deck === deckDef.num && !m.stub && m.at && cellPos(...m.at).distanceTo(new THREE.Vector3(at.x, 0, at.z)) < near)) continue;
            const r = ixTap(it, at.clone(), at.clone()); actEnd(true); if (r) out.push(deckDef.num + ' ' + it.t); }
          return out; })()""")
    check(not over, f'no tap near a real machine is ours ({over[:5]})')
    tips = g.ev("window.__tips || null")
    if tips is not None:
        print('   tips fired:', tips)
        check(all(t in tips for t in ['board', 'taken', 'machine', 'turnin']), f'the four job-loop tips fire (board, taken, machine, turn in): {tips}')
    print('   draw-call peak while doing things:', peak)
    check(peak < BUDGET, f'draw calls under {BUDGET} ({peak})')
    check(not g.errors, f'no console errors ({g.errors[:3]})')
    g.close()

# a fresh game (0.37.6; strict from 0.37.7, with section 17's 0.33.32; the user's "the job board never has any jobs"): every hour of Day 1's day shift has a job you
# could take on the board (section 17's openJobs), the way a new player finds it
if '--quick' not in sys.argv:
    with sync_playwright() as pw:
        g = Game(pw, sys.argv[1])
        print('== a fresh game: jobs for you on the board, Day 1')
        hours = []
        for h in range(6, 17):                             # from the moment a new game starts (06:00) to the end of the day shift
            g.ev(f"skipTo({h * 60})"); g.step(3)
            hours.append((h, g.ev("typeof openJobs === 'function' ? openJobs('you').length : jobsBoard().filter(j => !j.claimedBy).length")))
        print('   open to you by hour:', ' '.join(f'{h:02d}:00 {n}' for h, n in hours))
        empty = [h for h, n in hours if n < 1]
        check(not empty, f'a fresh game has a job for you on the board every hour of the day shift (empty at {empty})')   # strict from 0.37.7 (section 17's 0.33.32)
        check(not g.errors, f'no console errors ({g.errors[:3]})')
        g.close()

print('INTERACTIONS CHECK OK' if ok else 'INTERACTIONS CHECK FAILED')
sys.exit(0 if ok else 1)
