# Starship Cadet: interactions check (keep in the repo, next to player_check.py)
# Checks section 15b (the interactions engineer): more places to use, the job board, the goal pointer.
#   parity: tapping the real things on the real decks starts the crew's activity there (the bar, lounges, reading
#   seats, benches, the garden, the music room, the laundry, basins, the kettle, the telescope, the observatory),
#   with a pose, and the main need rises; places crew hold are "In use"; private cabins, beds, notices and
#   section 15's own taps (treadmill, shower) are left alone; walking away stops it; draw calls stay under BUDGET
#   the job board: tapping it opens the list; Take it claims the job (section 17's claimJob); Drop it puts it back;
#   a round or a haul has a Take it; a side job (the drill) and the other registered kinds (an incident, a leak...) not
#   your lesson's job (FX10, patch 0.92.3 item 29) first and marked on the board; a small repair's stop (FX10) starts with a tap, one in each room
#   a job you take that runs past your next lesson's start says so in the "Job taken" message (FX10, patch 0.92.4 item D)
#   the goal pointer: hidden with no goal; your job's next step shows by itself; on another deck it says "Take the
#   lift to Deck N"; setGoal / clearGoal; an arrow at the screen edge when the place is off screen, a marker when on
# Setup and environment as for cadet_test.py.
# Run:  python3 interactions_check.py BUILD.html
import sys, json
exec(open(__file__.replace('interactions_check.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
# The teaching arrows are on from 0.92.0. Here, as on a shift, you are clocked in when you take a test job (else the
# arrow rightly points at the time clock first), and every pop-up shows at once (the pop-up queue is arrows_check's).
ARROWS_ON = """if (typeof GUIDE_ON !== 'undefined' && GUIDE_ON) { const cj = claimJob; GUIDE.tq.length = 0; guideToast = () => false;
  claimJob = function (...a) { if (typeof careerClockedIn === 'function' && !careerClockedIn()) { if (!SHIP.career && typeof careerInit === 'function') careerInit(); if (SHIP.career) SHIP.career.ci = Math.max(1, Math.floor(shipNow())), SHIP.career.co = 0; } return cj.apply(this, a); }; }"""
_Game = Game
def Game(*a, **k):
    g = _Game(*a, **k); g.ev(ARROWS_ON); return g

BUDGET = 450
ok = True
# with no job on a shift, the arrow shows the time clock till you've clocked in, then the job board (playtest 1, note 9)
NO_JOB_GOALS = (None, 'Clock in at the time clock', 'Take a job at the job board', 'Take a job at the board')   # the last: the shift chain's (teaching arrows, 0.92.0)

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
    (4, 'Basins', 'ixBasin', 'hygiene'),   # the junior common room's Tiles table plays any time since 0.28.62 (tiles_check)
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
        if kind == 'ixBasin': g.ev("if (typeof washLoad === 'function') SHIP.player.wash = { shower: null, owed: 3, pre: 53 }")   # a hand-wash puts back only a toilet's take (FX6): as after a visit
        if title == 'The bar':                         # a stool is a drink only with one from the bar (section 15's barTap, 0.28.62); by day the bar is shut
            g.ev("SHIP.player.drink = null"); shut = tap(title); g.step(1)
            check(shut is True and 'Back at 17:30' in st()['toast'] and not g.ev("SHIP.player.drink"), f'the bar by day: "Back at 17:30" ({st()["toast"][:60]})')
            g.ev("SHIP.player.drink = 'tea'")
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
    g.ev("SHIP.player.drink = 'tea'"); tap('The bar'); s = st(); g.ev("SHIP.player.drink = null")   # with a drink, a tap on the bar is a tap on its stools (0.28.62)
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
    # a round and a haul (registered job kinds, run by their stops) have a Take it on the board; a side kind (the drill)
    # does not (AC2, FX2's find: they said "not yet: coming soon", so Rounds and Hauling could never be taken)
    rk = g.ev(r"""(() => { if (typeof ixBoard === 'undefined' || typeof ixBoard.doable !== 'function') return 'no ixBoard.doable in this build'; let j = null; try { j = roundJob(SHIP.time.day, Math.floor(SHIP.time.min), { train: 'm1', yours: true }); } catch (e) { return 'roundJob: ' + e.message; }
      if (!j) return 'no round'; if (!SHIP.jobs.includes(j)) SHIP.jobs.push(j); j.claimedBy = null; j.status = 'open'; MACH_REV++; ixBoard.draw();
      const row = [...document.querySelectorAll('#ixBoardL [data-job]')].find(r => r.dataset.job === j.id), b = row && row.querySelector('button');
      const out = { offered: openJobs('you').some(o => o.id === j.id), row: !!row, btn: b ? b.textContent : null, haul: !JOB_KINDS.haul || ixBoard.doable({ kind: 'haul' }), drill: ixBoard.doable({ kind: 'drill' }), others: ['incident', 'leak', 'nozzle', 'tracedemo', 'rewire', 'tune'].filter(k => ixBoard.doable({ kind: k })) };
      SHIP.jobs = SHIP.jobs.filter(x => x !== j); MACH_REV++; ixBoard.draw(); return out; })()""")
    print('   a round on the board:', rk)
    check(isinstance(rk, dict) and rk['row'] and rk['btn'] == 'Take it' and rk['haul'] and not rk['drill'] and not rk['others'], f'a round (and a haul) can be taken at the board; a drill, an incident, a leak, nozzles, a rewire, the trace demo or a machine-less tune not (lead 29) ({rk})')
    # your lesson's job (FX10, patch 0.92.3 item 29): a lesson at "your turn" (24 core's trainDo: SHIP.works.cur at 'do')
    # puts its job first on the board, outlined, "Your lesson: take this one"; nothing marked once it isn't your turn
    ls = g.ev(r"""(() => { if (typeof boardLesson !== 'function') return 'no boardLesson in this build'; let j = null; try { j = roundJob(SHIP.time.day, Math.floor(SHIP.time.min), { train: 'm1', yours: true }); } catch (e) { return 'roundJob: ' + e.message; }
      if (!j) return 'no round'; if (!SHIP.jobs.includes(j)) SHIP.jobs.push(j); j.claimedBy = null; j.status = 'open'; j.found = Math.min(j.found, shipNow() - 1); MACH_REV++;
      const had = SHIP.works, W = (typeof worksInit === 'function' && worksInit()) || SHIP.works || (SHIP.works = {}), keep = W.cur, rowOf = () => document.querySelector('#ixBoardL [data-job]');
      W.cur = { id: 'm1', st: 'do', d: SHIP.time.day, by: ['torres-zeke'], occ: null, j: j.id, w: 0 }; ixBoard.draw();
      const r = rowOf(), out = { first: !!r && r.dataset.job === j.id, lesson: !!r && r.classList.contains('lesson'), text: r ? r.textContent : null, sub: document.getElementById('ixBoardX').textContent };
      W.cur = keep; if (!had) SHIP.works = had; ixBoard.draw(); out.after = [...document.querySelectorAll('#ixBoardL .lesson')].length;
      SHIP.jobs = SHIP.jobs.filter(x => x !== j); MACH_REV++; ixBoard.draw(); return out; })()""")
    print('   your lesson on the board:', ls)
    check(isinstance(ls, dict) and ls['first'] and ls['lesson'] and re.search(r'Your [a-z ]*lesson: take this one', ls['text'] or '') and not ls['after'],   # (DS1, patch 0.92.5 #12: the lesson named)
          f'your lesson\'s job is first on the board and marked, and only while it\'s your turn (FX10, item 29) ({ls})')
    # a job that runs past your next lesson (FX10, patch 0.92.4 item D): with a lesson meeting 30 minutes off, taking a repair
    # whose part has to be made says so in the "Job taken" message; with the meeting 10 hours off, nothing is said
    LC = r"""((ahead) => { const t = shipNow(), m = machineList().find(m => m.deck === 3 && !m.stub && jobTier({ machine: m.id }) <= PLAYER_TIER && !ENGINE_KINDS.has(m.kind) && panelPlace(m.id)); if (!m) return 'no machine';
      const part = MACHINE_KINDS[m.kind].part, keepS = SHIP.stores[part], keepW = SHIP.works, keepO = SHIP.occasions; SHIP.stores[part] = 0;
      for (const j of SHIP.jobs) if (j.claimedBy === 'you' && j.status === 'claimed') { j.claimedBy = null; j.status = 'open'; }
      SHIP.occasions = (keepO || []).concat([{ key: 'ixlc@1', at: t + ahead, len: 15, deck: 5, room: 'o', status: 'asked', met: false }]);
      SHIP.works = { ...(keepW || {}), tr: (keepW && keepW.tr) || {}, use: (keepW && keepW.use) || {}, op: (keepW && keepW.op) || {}, cur: { id: 'm6', st: 'meet', d: SHIP.time.day, by: 'calder', occ: 'ixlc@1', j: null, w: 0 } };
      SHIP.jobs.push({ id: 'ixlc@1', machine: m.id, deck: 3, kind: 'repair', urgency: 1, posted: t, found: t, claimedBy: null, parts: [part], status: 'open' }); MACH_REV++;
      let took = false; try { took = ixBoard.take('ixlc@1'); } catch (e) { return 'take: ' + e.message; }
      const msg = document.getElementById('tt').textContent + ': ' + document.getElementById('tx').textContent;
      SHIP.jobs = SHIP.jobs.filter(j => j.id !== 'ixlc@1'); SHIP.stores[part] = keepS; SHIP.works = keepW; SHIP.occasions = keepO; MACH_REV++;
      return { took, msg }; })"""
    near, far = g.ev(f"({LC})(30)"), g.ev(f"({LC})(600)")
    print('   a job past your lesson:', near, '| 10 hours off:', far)
    check(isinstance(near, dict) and near['took'] and 'Heads up' in near['msg'] and 'machine shop' in near['msg'] and 'starts at' in near['msg']
          and isinstance(far, dict) and far['took'] and 'Heads up' not in far['msg'], f'a job that runs past your lesson says so when you take it, and only then (FX10, patch 0.92.4 item D) ({near} | {far})')
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
    check(s['goal'] and ('storage' in s['goal'] or 'shelf' in s['goal']), f'the pointer: fetch from main storage ({s["goal"]})')   # or the part's own shelf (0.33.41)
    check(g.ev("SHIP.player.track") == 'ixtest@1', f'taking a job tracks it ({g.ev("SHIP.player.track")})')
    g.ev("SHIP.player.track = null"); g.step(3); s = st()
    check(s['goal'] is None, f'tracking switched off (the device): no job arrow ({s["goal"]})')
    sv = g.ev("(() => { const s = { player: {} }; for (const f of SAVE_EXTRA) try { f(s); } catch (e) {} return s.player.track; })()")
    check(sv is None and g.ev("(() => { const s = { player: {} }; for (const f of SAVE_EXTRA) try { f(s); } catch (e) {} return 'track' in s.player; })()"), 'the save keeps tracking off')
    g.ev("SHIP.player.track = myJob().id"); g.step(3); s = st()
    g.ev("goToDeck(4)"); g.step(3); s = st()
    check(s['goal'] and s['goal'].startswith('Tap the lift: Deck 5'), f'another deck: the lift panel ({s["goal"]})')   # (FX3: was "Take the lift to Deck 5")
    g.ev("SHIP.player.carry = [" + json.dumps(job[1]) + "]"); g.step(40); s = st()
    check(s['goal'] and s['goal'].startswith('Tap the lift: Deck 3') and 'epair' in s['goal'], f'parts in hand: to the machine ({s["goal"]})')
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
    check(not g.ev("myJob()") and (s['goal'] in NO_JOB_GOALS or (s['goal'] or '').endswith('back: main storage')), f'Drop it: no job and the pointer hides (or shows the clock or the board, or, with its part still in your hands, where to put it back: FX3) ({g.ev("JSON.stringify(myJob())")}, {s["goal"]}, board {s["board"]}, {s["toast"][:80]})')
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
        # stand by the stop and tap the floor at it, the way a player would (0.28.55: a thing you can use there does its own
        # thing now, like the laundry's washers at a delivery's drop; before, this tapped the nearest thing)
        STANDAT = r"""(({ place }) => { const s = placeSpot(place); if (!s) return null; const gl = nearestOpen(s.x, s.z, player); player.obj.position.copy(cellPos(...gl)); player.stop(); return true; })"""
        SCRAT = r"""(({ place }) => { const s = placeSpot(place), v = new THREE.Vector3(s.x, .02, s.z).project(camera); return [(v.x + 1) / 2 * innerWidth, (1 - v.y) / 2 * innerHeight]; })"""
        def TAPAT_click(place):
            if not g.ev(f"({STANDAT})({json.dumps({'place': place})})"): return 'no spot'
            g.step(15); x, y = g.ev(f"({SCRAT})({json.dumps({'place': place})})"); g.page.mouse.click(x, y); return ['floor', x, y]
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
                check(s['goal'] and (('storage' in s['goal'] or 'shelf' in s['goal']) if step == 'fetch' else (f'Deck {deck}' in s['goal'] if g.ev('deckDef.num') != deck else True)), f'{kind} {step}: the pointer leads there ({s["goal"]})')
                if g.ev('deckDef.num') != deck: g.ev(f"goToDeck({deck})"); g.step(3)
                if step == 'fetch':
                    r = g.ev(f"({TAP})({{title: typeof shelfWant === 'function' && shelfWant() ? shelfName(shelfWant()) : ITEMS.find(i => roomAt(...cellAt(i.hit.getWorldPosition(_wp).x, _wp.z)) === 'r' && !/tarp/i.test(i.t)).t}})")   # the part's own shelf (section 17's shelves, 0.33.41)
                else:
                    r = TAPAT_click(place)
                g.step(2); s0 = st()
                for tries in range(5):                       # a crew member on the walk-to tile: try again in a little while
                    if s0['act'] or 'in the way' not in s0['toast']: break
                    g.step(120); r = TAPAT_click(place) if step != 'fetch' else r; g.step(2); s0 = st()
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
            check(not g.ev("myJob()") and g.ev(f"SHIP.jobs.find(j => j.id === '{job[0]}').status") == 'done' and s['goal'] in NO_JOB_GOALS, f'{kind}: turned in, complete, no pointer (or the clock or the board) ({s["toast"][:80]})')
            check(g.ev("SHIP.player.credits || 0") > cr or not g.ev("typeof JOB_PAY !== 'undefined'"), f'{kind}: paid at turn-in')
            g.ev("ixBoard.close()")
    # a tap at your job's stop starts the work (0.28.52, the user's lamp report from 0.60.5b): a real screen tap at the spot the
    # marker shows, on the floor or on whatever is in front of it (Deck 1's trunk head, seen through glass), for every lamp
    # chore, section 18's two lamp jobs (stormBallasts, veyliLamp, in the Captain's locked quarters) and a machine repair
    if g.ev("typeof jobHere === 'function' && typeof CHORES !== 'undefined'"):
        print('== a tap at the stop')
        MKJ = r"""((kind) => { const t = shipNow(), out = []; SHIP.stores.lamp = Math.max(SHIP.stores.lamp || 0, 9);
          const add = j => { if (j) { SHIP.jobs.push(j); out.push(j.id); } };
          if (kind === 'lamp') choreWhere('lamp').forEach(c => add({ id: 'ixtap-' + c.key, machine: null, deck: c.deck, room: c.room, kind: 'chore', chore: 'lamp', target: c.key, title: c.title, tier: 1,
            stops: c.stops.map(x => ({ ...x })), urgency: 0, posted: t, found: t, claimedBy: null, parts: ['lamp'], status: 'open' }));
          if (kind === 'event' && typeof SHIP_EVENTS !== 'undefined') for (const id of ['stormBallasts', 'veyliLamp']) {
            const E = (Array.isArray(SHIP_EVENTS) ? SHIP_EVENTS : Object.values(SHIP_EVENTS)).find(e => e.jobs && Object.values(e.jobs).some(l => Array.isArray(l) && l.some(x => x.id === id)));
            if (E) add(eventJob(Object.values(E.jobs).flat().find(x => x && x.id === id), E.id, t, 'ixtap-' + id)); }
          if (kind === 'machine') { const m = machineList().find(m => m.id === '3-oven-1');
            if (m) add({ id: 'ixtap-oven', machine: m.id, deck: m.deck, room: m.room, kind: Object.keys(JOB_TYPES)[0], urgency: 1, posted: t, found: t, claimedBy: null, parts: ['seal'], status: 'open', title: 'Repair the oven' }); }
          if (kind === 'fix' && typeof fixTable === 'function') { const T = fixTable(), one = new Set();   // FX10's small repairs: one in each room they're in
            for (const r of T.s.concat(T.p)) { const pl = placeById(r.place); if (!pl || (pl.deck === 7 && !REC_DECK) || one.has(pl.deck + pl.room)) continue; one.add(pl.deck + pl.room);
              if (r.part) SHIP.stores[r.part] = Math.max(SHIP.stores[r.part] || 0, 9);
              add({ id: 'ixtap-fix-' + r.id, machine: null, deck: pl.deck, room: pl.room, kind: 'chore', chore: 'fix', target: r.id, title: r.title, tier: 1, stops: [{ deck: pl.deck, placeId: r.place, mins: r.mins, tag: 'fix' }],
                urgency: 0, posted: t, found: t, claimedBy: null, parts: r.part ? [r.part] : [], status: 'open', fix: r.id, fixS: pl.deck === 2 ? 's' : 'p', tool: r.tool }); } }
          if (kind.startsWith('odd') && typeof fixTable === 'function' && fixTable().o) { const one = new Set();   // FX20's odd jobs (ODD_ON): one in each room ('odd'), or every row ('oddall', a probe)
            const only = kind.startsWith('odd:') ? kind.slice(4).split(',') : null;   // odd:<id>,<id>: just those rows
            for (const r of fixTable().o) { const pl = placeById(r.place); if (!pl || (pl.deck === 7 && !REC_DECK) || (kind === 'odd' && one.has(pl.deck + pl.room)) || (only && !only.includes(r.id))) continue; one.add(pl.deck + pl.room);
              if (r.part) SHIP.stores[r.part] = Math.max(SHIP.stores[r.part] || 0, 9);
              add({ id: 'ixtap-odd-' + r.id, machine: null, deck: pl.deck, room: pl.room, kind: 'chore', chore: 'fix', target: r.id, title: r.title, tier: 1, stops: [{ deck: pl.deck, placeId: r.place, mins: r.mins, tag: 'fix' }],
                urgency: 0, posted: t, found: t, claimedBy: null, parts: r.part ? [r.part] : [], status: 'open', fix: r.id, fixS: 'o', tool: r.tool }); } }
          MACH_REV++; return out; })"""
        HOLD = r"""((id) => { for (const j of SHIP.jobs) if (j.claimedBy === 'you' && j.status === 'claimed') { j.claimedBy = null; j.status = 'open'; }
          actEnd(true); SHIP.player.work = null; const j = SHIP.jobs.find(x => x.id === id); j.claimedBy = 'you'; j.status = 'claimed'; j.start = shipNow(); MACH_REV++;   // claimed by hand: the tier doesn't matter here
          SHIP.player.carry = j.parts.slice(0, 2); jobStops(j).forEach((x, k) => { if (x.step === 'fetch' && j.kind === 'chore') jobStepDone(j.id, k); });
          const nx = jobStops(j).find(x => !x.done && x.step !== 'fetch'); return nx ? [nx.step, nx.deck, nx.places[0]] : null; })"""
        # the floor at the spot, or near it (inside JOB_REACH) where no crew member is in front: a tap on a person talks to them
        # (section 10's tapCrew comes first), and someone waiting to get past you can stand there (X3: Sol at Deck 3's lift, 0.71.5)
        SCR = r"""((pid) => { const s = placeSpot(pid), scr = (dx, dz) => { const v = new THREE.Vector3(s.x + dx, .02, s.z + dz).project(camera); return [(v.x + 1) / 2 * innerWidth, (1 - v.y) / 2 * innerHeight]; };
          for (const [dx, dz] of [[0, 0], [.4, 0], [-.4, 0], [0, .4], [0, -.4], [.4, .4], [-.4, .4], [.4, -.4], [-.4, -.4], [.8, 0], [-.8, 0], [0, .8], [0, -.8]]) { const p = scr(dx, dz); if (!crewAtScreen(...p)) return p; }
          return scr(0, 0); })"""
        PUT = r"""((pid) => { const s = placeSpot(pid), gl = nearestOpen(s.x, s.z, player); player.obj.position.copy(cellPos(...gl)); player.stop(); })"""
        for kind in ['lamp', 'event', 'machine', 'fix', os.environ.get('IX_ODD', 'odd')]:   # IX_ODD=oddall: every odd job's stop (FX20's probe)
            for jid in g.ev(f"({MKJ})('{kind}')"):
                nx = g.ev(f"({HOLD})('{jid}')")
                if not check(nx, f'{jid}: a stop to go to'): continue
                step, deck, pid = nx
                if g.ev('deckDef.num') != deck: g.ev(f"goToDeck({deck})"); g.step(3)
                if jid == 'ixtap-veyliLamp':                 # the Captain's quarters are locked: your job's stop opens the door for you
                    path = g.ev(f"(() => {{ const pl = PLACE_OF.get('{pid}'), lw = [...PLACE_OF.values()].find(p => p.type === 'lift-wait'); return !!findPath(lw.walk || lw.at, pl.walk || pl.at, null, player); }})()")
                    check(path, f'{jid}: the way into the Captain\'s quarters is open while the job is yours')
                g.ev(f"({PUT})('{pid}')"); g.step(60 if kind == 'fix' or kind.startswith('odd') else 15)   # fix: one stop after another on a deck, far apart: the camera catches up first (FX10)
                x, y = g.ev(f"({SCR})('{pid}')")
                g.page.mouse.click(x, y); g.step(90); s = st()
                check(s['act'] and s['act'][0] in ('ixStop', 'job'), f'{jid}: a tap at the stop ({step}, Deck {deck}) starts the work ({s["act"]}, {s["toast"][:70]})')
                print('  ', jid, step, 'Deck', deck, '->', s['act'])
                g.ev("actEnd(true)")
        g.ev("for (const j of SHIP.jobs) if (j.claimedBy === 'you' && j.status === 'claimed') { j.claimedBy = null; j.status = 'open'; } SHIP.jobs = SHIP.jobs.filter(j => !String(j.id).startsWith('ixtap-')); SHIP.player.carry = []; SHIP.player.work = null; MACH_REV++")
        lw = g.ev("(() => { goToDeck(2); const pl = PLACE_OF.get('2-captable-1'), lw = [...PLACE_OF.values()].find(p => p.type === 'lift-wait'); return pl ? !!findPath(lw.walk || lw.at, pl.walk || pl.at, null, player) : null; })()")
        check(lw is not True, f'with no job the Captain\'s quarters stay shut ({lw})')
    # 0.28.55 (reviewer 1f's BLOCK on 0.28.52): (1) holding a repair, a real click on another usable thing near its machine
    # does that thing (Washer 2 starts a load; the welding bench and the Works station aren't the repair), and the machine
    # itself still starts it; (2) the Captain's quarters let you out once the lamp is in, and after turn-in; shut from outside
    if g.ev("typeof jobDoorOpen === 'function' && typeof machineById === 'function'"):
        print('== near your job, but not it')
        HOLD = r"""((mid) => { for (const j of SHIP.jobs) if (j.claimedBy === 'you' && j.status === 'claimed') { j.claimedBy = null; j.status = 'open'; }
          actEnd(true); SHIP.player.work = null; const m = machineById(mid), t = shipNow(); if (!m) return null;
          SHIP.jobs.push({ id: 'ixhj-' + mid, machine: m.id, deck: m.deck, room: m.room, kind: Object.keys(JOB_TYPES)[0], urgency: 1, posted: t, found: t, claimedBy: 'you', status: 'claimed', start: t, parts: ['seal'], title: 'Repair ' + mid });
          MACH_REV++; SHIP.player.carry = ['seal']; return panelPlace(m.id); })"""
        CLICK = r"""((title, near) => { const c = placeSpot(near);
          const its = ITEMS.filter(i => i.t === title).map(i => { i.hit.getWorldPosition(_wp); return [i, _wp.clone()]; }).sort((a, b) => Math.hypot(a[1].x - c.x, a[1].z - c.z) - Math.hypot(b[1].x - c.x, b[1].z - c.z));
          if (!its.length) return null; const p = its[0][1], gl = nearestOpen(p.x, p.z, player); player.obj.position.copy(cellPos(...gl)); player.stop(); return [p.x, p.y, p.z]; })"""
        SCRP = r"""((x, y, z) => { const v = new THREE.Vector3(x, y, z).project(camera); return [(v.x + 1) / 2 * innerWidth, (1 - v.y) / 2 * innerHeight]; })"""
        for mid, deck, title, mine in [('4-washer-1', 4, 'Washer 2', False), ('5-battery-1', 5, 'Welding bench', False), ('1-databus-1', 1, 'Works station', False), ('4-washer-1', 4, 'Washer 1', True)]:
            if g.ev('deckDef.num') != deck: g.ev(f"goToDeck({deck})"); g.step(3)
            pid = g.ev(f"({HOLD})('{mid}')"); p = g.ev(f"({CLICK})('{title}', '{pid}')") if pid else None
            if not check(p, f'{mid} and a {title} to test'): continue
            g.step(10); x, y = g.ev(f"({SCRP})({p[0]}, {p[1]}, {p[2]})"); g.page.mouse.click(x, y); g.step(90); s = st()
            rep = bool(s['act'] and s['act'][0] == 'job')
            print('  ', mid, 'held, clicked', title, '->', s['act'], '|', s['toast'][:70])
            check(rep == mine, f'{mid} held: a click on {title} ' + ('starts the repair' if mine else 'does its own thing, not the repair') + f' ({s["act"]}, {s["toast"][:70]})')
            g.ev("actEnd(true)")
        # a chore's stop (0.28.55): the laundry's lamp; Washer 1 there starts a load, and the floor at the stop the lamp
        CH = r"""(() => { for (const j of SHIP.jobs) if (j.claimedBy === 'you' && j.status === 'claimed') { j.claimedBy = null; j.status = 'open'; }
          actEnd(true); SHIP.player.work = null; const c = choreWhere('lamp').find(c => c.key === '4-laundry-1'), t = shipNow(); if (!c) return null;
          const j = { id: 'ixhj-lamp', machine: null, deck: 4, room: c.room, kind: 'chore', chore: 'lamp', target: c.key, title: c.title, tier: 1, stops: c.stops.map(x => ({ ...x })), urgency: 0, posted: t, found: t, claimedBy: 'you', status: 'claimed', start: t, parts: ['lamp'] };
          SHIP.jobs.push(j); MACH_REV++; jobStepDone(j.id, 0); SHIP.player.carry = ['lamp']; return c.key; })()"""
        if g.ev('deckDef.num') != 4: g.ev("goToDeck(4)"); g.step(3)
        pid = g.ev(CH)
        if check(pid, 'a laundry lamp chore to test'):
            p = g.ev(f"({CLICK})('Washer 1', '{pid}')"); g.step(10); x, y = g.ev(f"({SCRP})({p[0]}, {p[1]}, {p[2]})"); g.page.mouse.click(x, y); g.step(90); s = st()
            print('   lamp chore in the laundry, clicked Washer 1 ->', s['act'], '|', s['toast'][:70])
            check(not (s['act'] and s['act'][0] == 'ixStop'), f'a lamp chore in the laundry: Washer 1 does its own thing ({s["act"]}, {s["toast"][:70]})')
            g.ev("actEnd(true)")
        g.ev("goToDeck(2)"); g.step(3)
        lk = g.ev(r"""(() => { for (const j of SHIP.jobs) if (j.claimedBy === 'you' && j.status === 'claimed') { j.claimedBy = null; j.status = 'open'; }
          SHIP.player.carry = []; SHIP.player.work = null; if (typeof SHIP_EVENTS === 'undefined') return null;
          const E = (Array.isArray(SHIP_EVENTS) ? SHIP_EVENTS : Object.values(SHIP_EVENTS)).find(e => e.jobs && Object.values(e.jobs).some(l => Array.isArray(l) && l.some(x => x.id === 'veyliLamp')));
          const j = E && eventJob(Object.values(E.jobs).flat().find(x => x && x.id === 'veyliLamp'), E.id, shipNow(), 'ixhj-veyli'); if (!j) return null;
          SHIP.jobs.push(j); j.claimedBy = 'you'; j.status = 'claimed'; MACH_REV++;
          const pl = PLACE_OF.get('2-captable-1'), lw = [...PLACE_OF.values()].find(p => p.type === 'lift-wait'), w = pl.walk || pl.at, lwt = lw.walk || lw.at;
          const out = { in: !!findPath(lwt, w, null, player) }; player.obj.position.copy(cellPos(...w)); player.stop();
          jobStops(j).forEach((x, k) => jobStepDone(j.id, k)); out.done = !!j.workDone; out.outAfterDone = !!findPath(w, lwt, null, player);
          if (typeof turnInJob === 'function') turnInJob(j.id); out.outAfterTurnIn = !!findPath(w, lwt, null, player);
          player.obj.position.copy(cellPos(...lwt)); player.stop(); out.shutFromOutside = !findPath(lwt, w, null, player); return out; })()""")
        print('   the Captain\'s quarters:', lk)
        if check(lk, 'veyliLamp to test the Captain\'s quarters'):
            check(lk['in'] and lk['done'] and lk['outAfterDone'] and lk['outAfterTurnIn'] and lk['shutFromOutside'], f'the Captain\'s quarters: in for the lamp, out after it and after turn-in, shut from outside ({lk})')
        g.ev("for (const j of SHIP.jobs) if (j.claimedBy === 'you' && j.status === 'claimed') { j.claimedBy = null; j.status = 'open'; } SHIP.jobs = SHIP.jobs.filter(j => !String(j.id).startsWith('ixhj-')); SHIP.player.carry = []; SHIP.player.work = null; MACH_REV++")
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
    for n in g.ev("typeof DECK_ORDER !== 'undefined' ? DECK_ORDER.slice().sort((a, b) => a - b) : Object.keys(DECKS).map(Number)"):
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

# FX3 (lead 28, from AR1's play of 0.64.15): (1) a calibrate chore on the galley plant: its arrow says "Calibrate", and a real
# tap at the arrow's pin starts it (the cold store's chiller in front used to take the tap: "in good order"); (2) a dropped
# job's part left in your hands: the arrow says to put it back (a cart won't take full hands), a shelf tap does, then the cart
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1]); g.step(5)
    if g.ev("typeof jobsOn === 'function' && jobsOn() && !!machineById('3-galleyplant-1') && !!panelPlace('3-galleyplant-1')"):
        print('== FX3: calibrating the galley plant, a part left in your hands')
        lab = g.ev(r"""(() => { setShipNow(1440 * 2 + 9 * 60); machinesNow(); const t = shipNow(); for (const j of SHIP.jobs) if (j.claimedBy === 'you') { j.claimedBy = null; j.status = 'open'; }
          const m = machineById('3-galleyplant-1');
          SHIP.jobs.push({ id: 'fx3-cal', machine: m.id, deck: 3, room: m.room, kind: 'chore', chore: 'calibrate', title: 'Calibrate the galley plant', tier: 1, urgency: 1, posted: t, found: t, claimedBy: null, parts: [], status: 'open', stops: [panelStop(m, 15, 'calibrate')] }); MACH_REV++;
          claimJob('fx3-cal'); goToDeck(3); const s = placeSpot(panelPlace(m.id)); player.obj.position.set(s.x - .5, 0, s.z + 1.2); player.stop(); return (ixJobStep() || {}).label; })()""")
        g.step(120)
        xy = g.ev("(() => { const s = placeSpot(panelPlace('3-galleyplant-1')), v = new THREE.Vector3(s.x, 0.05, s.z).project(camera); return [(v.x + 1) / 2 * innerWidth, (1 - v.y) / 2 * innerHeight]; })()")
        g.page.mouse.move(*xy); g.page.mouse.down(); g.page.mouse.up(); g.step(150)
        cal = g.ev("JSON.stringify([ACT && ACT.kind, ACT && ACT.placeId, document.getElementById('tx').textContent])")
        print('   calibrate:', lab, cal[:160])
        check(lab == 'Calibrate the galley plant', f'the calibrate chore\'s arrow says Calibrate ({lab})')
        check('"job","3-galleyplant-1-panel"' in cal, f'a tap at the arrow\'s pin starts the calibration, not the chiller in front ({cal})')
        pb = g.ev(r"""(() => { actEnd(true); SHIP.jobs = SHIP.jobs.filter(j => j.id !== 'fx3-cal'); SHIP.player.work = null; SHIP.player.carry = ['relay']; const a = ixJobStep() || {};
          const t = shipNow(); SHIP.jobs.push({ id: 'fx3-cart', machine: null, deck: 3, kind: 'restock', cargo: 'stores', urgency: 1, posted: t, found: t, claimedBy: null, parts: [], status: 'open' }); MACH_REV++;
          const ok = claimJob('fx3-cart'), b = ixJobStep() || {}; goToDeck(5); return [a.label, a.place, ok, b.label]; })()""")
        g.step(5)
        g.ev(TAP + "({ title: 'Lights' })")
        for k in range(80):
            g.step(30)
            if k > 1 and not g.ev("!!ACT || player.path.length > 0"): break
        after = g.ev("[SHIP.player.carry.slice(), (ixJobStep() || {}).label]")
        print('   a part in your hands:', pb, after)
        check(pb[0] == 'Put the relay back: main storage' and pb[1] == '5-parts-1', f'no job and a relay in hand: put it back ({pb})')
        check(pb[2] and pb[3] == 'Put the relay back: main storage', f'a cart run taken with the relay in hand: put it back first ({pb})')
        check(after[0] == [] and after[1] and 'back: main storage' not in after[1], f'a shelf tap puts it back, then the cart run\'s own arrow ({after})')
        g.ev("SHIP.jobs = SHIP.jobs.filter(j => j.id !== 'fx3-cart'); SHIP.player.carry = []")
        check(not g.errors, f'no console errors ({g.errors[:3]})')
    g.close()

# FX3 (the user's, lead 28): a goal on another deck points at the lift's control panel (the thing you tap to choose a deck),
# not the middle of the landing; following it and tapping there opens the deck picker, and the goal's deck takes you there
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1]); g.step(5)
    print('== FX3: the arrow to the lift panel')
    LP = r"""(() => { const el = document.getElementById('ixGoal'), m = (el.style.transform.match(/translate\(([-\d.]+)px, ?([-\d.]+)px\)/) || []).slice(1).map(Number);
      const its = ITEMS.filter(i => i.lift && isShown(i.hit)).map(i => { i.hit.getWorldPosition(_wp); const v = _wp.clone().project(camera); return [(v.x + 1) / 2 * innerWidth, (1 - v.y) / 2 * innerHeight]; });
      return { hidden: el.hidden, label: el.children[2].textContent, at: m, panels: its }; })()"""
    # on Decks 5, 3 and 4, inside the car and at the landing: the arrow on a lift panel you can see, and a real tap there opens the deck picker (FE1, lead 28)
    for deck, goal in ((5, 4), (3, 5), (4, 5)):
        for spot in ('inside', 'landing'):
            g.ev(f"goToDeck({deck})"); g.step(3)
            g.ev("(w => { const t = w === 'inside' ? ROOM_TILES['@'][Math.floor(ROOM_TILES['@'].length / 2)] : null; if (t) player.obj.position.copy(cellPos(...t)); else player.obj.position.set(LIFT_AT[0] + 3, 0, LIFT_AT[1]); player.stop(); SHIP.player.track = null; })('" + spot + "')")
            g.ev(f"setGoal({{ deck: {goal}, item: /job board/i, room: 'w', label: 'The job board' }})"); g.step(90)
            lp = g.ev(LP)
            near = min((((p[0] - lp['at'][0]) ** 2 + (p[1] - lp['at'][1]) ** 2) ** .5 for p in lp['panels']), default=999) if lp['at'] else 999
            tip = g.ev("(() => { const c = document.getElementById('devTip'); if (!c || c.hidden) return null; const r = c.getBoundingClientRect(); return [r.left, r.top, r.right, r.bottom, c.style.pointerEvents === 'none']; })()")
            if tip and lp['at']: check(tip[4] or not (tip[0] <= lp['at'][0] <= tip[2] and tip[1] <= lp['at'][1] <= tip[3]), f"Deck {deck} {spot}: the tip card isn't over the arrow's target, or lets the tap through (tip {[round(v) for v in tip[:4]]}, target {lp['at']}) (FX5)")
            opened = False
            if lp['at'] and near < 3:
                g.ev("while (TIP_Q.length) tipDone()"); g.step(2)   # a device tip card can sit over the panel (t:lift on Deck 3 at 06:07 with breakfast from 07:00): this part tests the arrow, so close tips first (the card's own fix: FX5)
                g.page.mouse.move(*lp['at']); g.page.mouse.down(); g.page.mouse.up()
                for k in range(120):
                    g.step(10)
                    if g.ev("!document.getElementById('lift').hidden"): opened = True; break
            print(f"   Deck {deck}, {spot}: {lp['label']} | {round(near, 1)} px from a panel you can see | picker {opened}")
            check(not lp['hidden'] and lp['label'].startswith(f'Tap the lift: Deck {goal}') and 'job board' in lp['label'], f"Deck {deck} {spot}: the label names the lift, the deck and the goal ({lp['label']})")
            check(near < 3, f"Deck {deck} {spot}: the arrow points at a lift panel you can see, not the landing ({near:.1f} px)")
            check(opened, f'Deck {deck} {spot}: tapping where the arrow points opens the deck picker')
            if opened and (deck, spot) == (4, 'landing'):
                g.ev("document.querySelector('#liftList button.goal').click()")
                for k in range(200):
                    g.step(10)
                    if g.ev("deckDef.num") == 5 and not g.ev("ride"): break
                check(g.ev("deckDef.num") == 5, f'the goal\'s deck button takes you there (Deck {g.ev("deckDef.num")})')
            elif opened: g.ev("closeLiftPanel()"); g.step(2)
    g.ev("clearGoal()")
    check(not g.errors, f'no console errors ({g.errors[:3]})')
    g.close()

# FX3 (RV6, lead 29): the climbing holds' job (rec deck, 7-wall-holds): its arrow's pin stands over the Climbing wall, and a tap
# there started a climb instead of the job's look-over (the same as the galley plant's chiller: jobTap now takes a tap over its spot)
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1]); g.step(5)
    if g.ev("typeof REC_DECK !== 'undefined' && REC_DECK && !!machineById('7-wall-holds') && !!panelPlace('7-wall-holds')"):
        print('== FX3: the climbing holds\' pin')
        g.ev(r"""(() => { setShipNow(1440 * 2 + 10 * 60); machinesNow(); const t = shipNow(); for (const j of SHIP.jobs) if (j.claimedBy === 'you') { j.claimedBy = null; j.status = 'open'; }
          const m = machineById('7-wall-holds'); SHIP.jobs = SHIP.jobs.filter(j => j.machine !== m.id);
          SHIP.jobs.push({ id: 'fx3-holds', machine: m.id, deck: 7, kind: 'service', urgency: 1, posted: t, found: t, claimedBy: null, parts: ['seal'], status: 'open' }); MACH_REV++;
          claimJob('fx3-holds'); goToDeck(7); const s = placeSpot(panelPlace(m.id)); player.obj.position.set(s.x + 1.2, 0, s.z + 1.2); player.stop(); })()""")
        g.page.click('#rot'); g.step(80)
        xy = g.ev("(() => { const s = placeSpot(panelPlace('7-wall-holds')), v = new THREE.Vector3(s.x, 1.2, s.z).project(camera); return [(v.x + 1) / 2 * innerWidth, (1 - v.y) / 2 * innerHeight]; })()")
        under = g.ev(f"(() => {{ const h = pick({xy[0]}, {xy[1]}); return h && h.object.userData.item ? h.object.userData.item.t : 'floor'; }})()")
        g.page.mouse.move(*xy); g.page.mouse.down(); g.page.mouse.up(); g.step(150)
        r = g.ev("JSON.stringify([ACT && ACT.kind, ACT && ACT.placeId, document.getElementById('tt').textContent])")
        print('   under the pin:', under, '| tapped:', r)
        check('"job","7-wall-holds-svc"' in r, f'a tap at the holds job\'s pin (over the {under}) starts the job, not a climb ({r})')
        # anywhere on the wall, away from the pin (the week guide's Day 5, lead 29): the wall is the holds (JOB_THING), not a climb
        g.ev("actEnd(false); { const t = shipNow(), m = machineById('7-wall-holds'); SHIP.jobs = SHIP.jobs.filter(j => j.machine !== m.id); SHIP.player.work = null; SHIP.jobs.push({ id: 'fx3-holds', machine: m.id, deck: 7, kind: 'service', urgency: 1, posted: t, found: t, claimedBy: null, parts: ['seal'], status: 'open' }); MACH_REV++; claimJob('fx3-holds'); }"); g.step(5)   # a fresh job: the first tap's look-over is done
        r2 = g.ev(r"""(() => { const it = ITEMS.find(i => i.t === 'Climbing wall'); if (!it) return 'no wall'; it.hit.getWorldPosition(_wp); const s = placeSpot(panelPlace('7-wall-holds'));
          const far = new THREE.Vector3(_wp.x + (_wp.x - s.x), 1.5, _wp.z + (_wp.z - s.z)).project(camera); ray.setFromCamera(new THREE.Vector2(far.x, far.y), camera);
          const r = playerTap(it, _wp.clone(), _wp.clone()); return JSON.stringify([r, ACT && ACT.kind, ACT && ACT.placeId, +jobRayDist(s).toFixed(2)]); })()""")
        print('   a tap on the wall away from the pin:', r2)
        check('"job","7-wall-holds-svc"' in r2, f'a tap on the Climbing wall away from the pin, with the holds job yours, starts the job, not a climb ({r2})')
        g.ev("actEnd(true); SHIP.jobs = SHIP.jobs.filter(j => j.id !== 'fx3-holds')"); g.step(5)
        r3 = g.ev(r"""(() => { const it = ITEMS.find(i => i.t === 'Climbing wall'); it.hit.getWorldPosition(_wp); const r = jobTap(it, _wp.clone()); return JSON.stringify([r, ACT && ACT.kind]); })()""")
        check(r3.startswith('[false'), f'with no job on the holds, the wall is not taken by the job loop ({r3})')
        g.ev("actEnd(true)")
        check(not g.errors, f'no console errors ({g.errors[:3]})')
    g.close()

# FX3 (AC2's arrows_check shift guide, AR2; lead 29): the linen delivery's drop (4-laundry-1) and the laundry's vent stop stand by
# Washer 1; a tap at the arrow's pin hit the washer and did the washer's thing (your own load), never the stop. Now a tap on
# the line to your chore's next stop does the stop; a washer tapped elsewhere still does its own (0.28.55, tested above)
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1]); g.step(5)
    if g.ev("typeof DELIVERIES !== 'undefined' && !!placeById('4-laundry-1')"):
        print('== FX3: the laundry stops by Washer 1')
        SET = r"""(kind => { actEnd(true); setShipNow(1440 * 2 + 13 * 60 + 40); machinesNow(); const t = shipNow(); SHIP.jobs = SHIP.jobs.filter(j => !/^fx3-/.test(j.id)); for (const j of SHIP.jobs) if (j.claimedBy === 'you') { j.claimedBy = null; j.status = 'open'; }
          const d = DELIVERIES.find(x => x.key === 'linen'), to = placeById(d.to);
          SHIP.jobs.push(kind === 'linen' ? { id: 'fx3-linen', machine: null, deck: 4, room: to.room, kind: 'chore', chore: 'delivery', title: d.title, bring: d.bring, tier: 1, urgency: 1, posted: t, found: t, claimedBy: null, parts: [], status: 'open',
              stops: [{ deck: 5, placeId: d.from, mins: 3, tag: 'pickup' }, { deck: 4, placeId: d.to, mins: 3, tag: 'drop' }], stepsDone: [0] }
            : { id: 'fx3-vent', machine: null, deck: 4, room: to.room, kind: 'chore', chore: 'vent', title: 'Clean a vent: laundry', tier: 1, urgency: 1, posted: t, found: t, claimedBy: null, parts: [], status: 'open', stops: [{ deck: 4, placeId: d.to, mins: 20, tag: 'vent' }] });
          MACH_REV++; claimJob(kind === 'linen' ? 'fx3-linen' : 'fx3-vent'); if (deckDef.num !== 4) goToDeck(4); const s = placeSpot(d.to); player.obj.position.set(s.x + 1.2, 0, s.z + 1.2); player.stop(); })"""
        res = []
        for kind in ('linen', 'vent'):
            for rot in range(4):
                g.ev(f"({SET})('{kind}')"); g.step(80)
                xy = g.ev("(() => { const s = placeSpot('4-laundry-1'), v = new THREE.Vector3(s.x, 1.2, s.z).project(camera); return [(v.x + 1) / 2 * innerWidth, (1 - v.y) / 2 * innerHeight]; })()")
                under = g.ev(f"(() => {{ const h = pick({xy[0]}, {xy[1]}); return h && h.object.userData.item ? h.object.userData.item.t : 'floor'; }})()")
                g.page.mouse.move(*xy); g.page.mouse.down(); g.page.mouse.up(); g.step(150)
                res.append([kind, rot, under, g.ev("ACT && ACT.kind")])
                g.page.click('#rot'); g.step(30)
        print('   at the pin [chore, camera turn, under the pin, what started]:', res)
        washer = [r for r in res if r[2].startswith('Washer')]
        check(washer, f'(the pin stands over a washer in some camera turn: {res})')
        check(all(r[3] == 'ixStop' for r in res), f'a tap at the laundry stop\'s pin does the chore\'s stop, over a washer too ({res})')
        g.ev("actEnd(true); SHIP.jobs = SHIP.jobs.filter(j => !/^fx3-/.test(j.id))")
        check(not g.errors, f'no console errors ({g.errors[:3]})')
    g.close()

# FX3 (fresh-eyes 2, item 64; lead 31): the shelf glow in main storage. A job needing a relay lights up the Lights shelf; a
# real tap on the glow's lower part (where a thumb lands) met the floor in front, or at some camera turns the Filters shelf
# in front ("No relays on the Filters shelf"), and the Day 1 job's relay couldn't be had. Now a tap on the glow is the shelf
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844); g.step(5)
    if g.ev("typeof shelfWant === 'function' && typeof SHELF_NAME !== 'undefined' && machineList().some(m => m.kind === 'lights' && m.deck === 4)"):
        print('== FX3: a tap on the glowing shelf takes the part')
        g.ev("(() => { if (SHIP.device && SHIP.device.settings) SHIP.device.settings.tips = false; const t = document.getElementById('devTip'); if (t) t.hidden = true; })()")
        g.page.click('#crew'); g.step(5)   # nobody in the way (a tap on a person is theirs)
        SET = r"""(() => { actEnd(true); for (const k of NEED_KEYS) SHIP.player.needs[k] = 100; needsT = null; NEED_GOAL = null; clearGoal(); setShipNow(10 * 60 + 40); machinesNow();
          for (const j of SHIP.jobs) if (j.claimedBy === 'you') { j.claimedBy = null; j.status = 'open'; }
          const t = shipNow(), m = machineList().find(m => m.kind === 'lights' && m.deck === 4); SHIP.jobs = SHIP.jobs.filter(j => j.id !== 'fx3-relay');
          SHIP.jobs.push({ id: 'fx3-relay', machine: m.id, deck: 4, kind: 'repair', urgency: 1, posted: t, found: t, claimedBy: null, parts: ['relay'], status: 'open' }); MACH_REV++;
          claimJob('fx3-relay'); SHIP.player.track = 'fx3-relay'; SHIP.player.work = null; myWork(); SHIP.player.carry = [];
          if (deckDef.num !== 5) goToDeck(5); const it = ITEMS.filter(i => i.t === 'Lights')[1]; it.hit.getWorldPosition(_wp); const c = cellAt(_wp.x, _wp.z);
          player.obj.position.copy(cellPos(c[0] + 1, c[1])); player.stop(); return shelfWant(); })()"""
        PTS = r"""(deg => { az = azT = deg * Math.PI / 180; placeCam(); if (!SHELF_GLOW || !SHELF_GLOW.mesh.visible) return null; const b = new THREE.Box3().setFromObject(SHELF_GLOW.mesh), out = [];
          for (const fx of [.1, .5, .9]) for (const fz of [.1, .5, .9]) for (const fy of [.05, .2]) { const v = new THREE.Vector3(b.min.x + fx * (b.max.x - b.min.x), b.min.y + fy * (b.max.y - b.min.y), b.min.z + fz * (b.max.z - b.min.z)).project(camera);
            const x = (v.x + 1) / 2 * innerWidth, y = (1 - v.y) / 2 * innerHeight; ndc.set(x / innerWidth * 2 - 1, -(y / innerHeight) * 2 + 1); ray.setFromCamera(ndc, camera);
            if (x > 0 && y > 120 && x < innerWidth && y < innerHeight - 100 && ray.ray.intersectsBox(b)) { const h = pick(x, y); let o = h && h.object; while (o && !(o.userData && o.userData.item)) o = o.parent; out.push([x, y, h ? (o ? o.userData.item.t : 'floor') : 'none']); } }
          return out; })"""
        res, under = [], {}
        for deg in range(0, 360, 30):
            if g.ev(SET) != '5-parts-1': res.append([deg, 'no glow']); continue
            g.step(60); pts = g.ev(PTS + f"({deg})") or []
            for x, y, u in pts:
                g.ev(SET); g.ev(f"az = azT = {deg} * Math.PI / 180; placeCam()"); g.step(2)
                g.page.mouse.move(x, y); g.page.mouse.down(); g.page.mouse.up(); g.step(3)
                a = g.ev("ACT && ACT.kind"); res.append([deg, round(x), round(y), u, a]); under[u] = under.get(u, 0) + 1
                g.ev("actEnd(true)")
        bad = [r for r in res if len(r) < 5 or r[4] != 'fetch']
        print(f'   taps on the glow\'s lower part: {len(res)} over 12 camera angles (the bottom and corners of the glow, where a thumb lands); under them first {under}; not a fetch: {bad[:6]}')
        check(len(res) >= 100 and not bad, f'a tap on the glowing shelf takes the part, whatever is under the tap ({len(bad)} of {len(res)}: {bad[:6]})')
        # someone standing in front of the glow (RV11): a tap on them, where the line also crosses the glow, is still theirs
        g.page.click('#crew'); g.step(5)   # the crew shown again
        ON = r"""(deg => { az = azT = deg * Math.PI / 180; placeCam(); const a = DECK_CREW.find(x => x && x.p); if (!a || !SHELF_GLOW || !SHELF_GLOW.mesh.visible) return null;
          const b = new THREE.Box3().setFromObject(SHELF_GLOW.mesh), c = b.getCenter(new THREE.Vector3()), p = player.obj.position;
          for (const f of [.5, .4, .6, .3, .7]) { a.x = p.x + (c.x - p.x) * f; a.z = p.z + (c.z - p.z) * f; a.y = 0; a.path = []; a.settled = false; a.spot = null; a.talking = 0;
            const v = new THREE.Vector3(a.x, 1, a.z).project(camera), x = (v.x + 1) / 2 * innerWidth, y = (1 - v.y) / 2 * innerHeight;
            ndc.set(x / innerWidth * 2 - 1, -(y / innerHeight) * 2 + 1); ray.setFromCamera(ndc, camera);
            if (crewAtScreen(x, y) === a && ray.ray.intersectsBox(b) && y > 120 && y < innerHeight - 100) return [a.p.name, x, y]; }
          return null; })"""
        talk = []
        for deg in range(0, 360, 45):
            g.ev(SET); g.step(30); q = g.ev(ON + f"({deg})")
            if not q: continue
            g.page.mouse.move(q[1], q[2]); g.page.mouse.down(); g.page.mouse.up(); g.step(3)
            talk.append([deg, q[0], g.ev("ACT && ACT.kind"), g.ev(f"(DECK_CREW.find(x => x && x.p && x.p.name === {json.dumps(q[0])}) || {{}}).talking > 0")])
            g.ev("actEnd(true)")
        print('   a tap on someone in front of the glow [angle, who, started, talking]:', talk)
        check(len(talk) >= 3 and all(t[2] != 'fetch' and t[3] for t in talk), f'a tap on someone standing in front of the glow talks to them, not the shelf ({talk})')
        g.ev("actEnd(true); SHIP.jobs = SHIP.jobs.filter(j => j.id !== 'fx3-relay')")
        check(not g.errors, f'no console errors ({g.errors[:3]})')
    g.close()

# FX3 (lead 30, from AC2's arrows_check week on arrows-c): the burst pipe's second puddle (4-wet-2) with someone standing on
# it or beside it (Calder escorting you, a crewmate on the way to the lift): a real tap at the arrow's pin went to section 11's
# tapCrew (it takes taps within 26 px of a person) as a chat, so "Mop up (2 of 2)" never started. Now the pin is your job's;
# a tap on the person away from the pin still talks to them
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844); g.step(5)
    if g.ev("typeof incJob === 'function' && !!placeById('4-wet-2') && typeof crewAtScreen === 'function'"):
        print('== FX3: the burst pipe\'s puddle with someone on it')
        g.ev("(() => { if (SHIP.device && SHIP.device.settings) SHIP.device.settings.tips = false; const t = document.getElementById('devTip'); if (t) t.hidden = true; })()")
        PIN = r"""(() => { const el = document.getElementById('ixGoal'), m = (el.style.transform.match(/translate\(([-\d.]+)px, ?([-\d.]+)px\)/) || []).slice(1).map(Number);
          return el.hidden || !m.length ? null : [m[0], m[1], el.children[2].textContent]; })()"""
        SET = r"""(() => { actEnd(true); for (const q of NEED_KEYS) SHIP.player.needs[q] = 100; needsT = null; NEED_GOAL = null; clearGoal();
          setShipNow(1440 * 7 + 10 * 60 + 40); machinesNow(); const t = shipNow(); SHIP.jobs = SHIP.jobs.filter(j => j.kind !== 'incident'); for (const j of SHIP.jobs) if (j.claimedBy === 'you') { j.claimedBy = null; j.status = 'open'; }
          careerInit(); SHIP.career.ci = t - 90; SHIP.career.co = null; const j = incJob('burst', 4, t); SHIP.jobs.push(j); MACH_REV++; claimJob(j.id); SHIP.player.track = j.id; j.stepsDone = [0, 1]; SHIP.player.carry = [];
          if (deckDef.num !== 4) goToDeck(4); player.obj.position.copy(cellPos(10, 5)); player.stop(); })()"""
        ON = r"""(dx => { const a = DECK_CREW.find(x => x && x.p); if (!a) return null; const w = placeSpot('4-wet-2'); a.x = w.x + dx; a.z = w.z; a.y = 0; a.path = []; a.settled = false; a.spot = null; return a.p.name; })"""
        res, chat = [], []
        for rot in range(4):
            g.ev(SET); g.step(60); p = g.ev(PIN); who = g.ev(ON + '(0)')   # (placed just before the tap: the crew move on in the next frame)
            if p:
                caught = g.ev(f"(() => {{ const a = crewAtScreen({p[0]}, {p[1]}); return a && a.p.id; }})()")
                g.page.mouse.move(p[0], p[1]); g.page.mouse.down(); g.page.mouse.up(); g.step(5)
                res.append([rot, who, caught, g.ev("ACT && ACT.kind")])
            g.ev("actEnd(true)"); g.page.click('#rot'); g.step(30)
        # a person away from the pin: a tap on them is a chat (their name on the toast), not the job
        # the same, with the tap on their legs, away from the pin: a chat with them, not the job
        chat = [None, None, 'nobody under the pin']
        for rot in range(4):
            g.ev(SET); g.step(60); p = g.ev(PIN); g.ev(ON + '(0)')
            tgt = p and g.ev(f"""(() => {{ const a = DECK_CREW.find(x => x && x.p); if (!a) return null; const v = new THREE.Vector3(a.x, a.y + .4, a.z).project(camera), x = (v.x + 1) / 2 * innerWidth, y = (1 - v.y) / 2 * innerHeight;
              return Math.hypot(x - {p[0]}, y - {p[1]}) > 26 && crewAtScreen(x, y) === a ? [a.p.name, x, y] : null; }})()""")
            if tgt:
                g.page.mouse.move(tgt[1], tgt[2]); g.page.mouse.down(); g.page.mouse.up(); g.step(5)
                chat = [tgt[0], g.ev("ACT && ACT.kind"), g.ev(f"(DECK_CREW.find(x => x && x.p && x.p.name === {json.dumps(tgt[0])}) || {{}}).talking > 0")]
                g.ev("actEnd(true)"); break
            g.page.click('#rot'); g.step(30)
        # beside them, not on them (RV7's optional line): someone half a metre from the puddle, a tap on the floor at the
        # puddle 12-26 px from their body and away from the pin: the job (a wider "on the person" would make it a chat)
        side = None
        for rot in range(4):
            g.ev(SET); g.step(60); p = g.ev(PIN)
            for dx in (.35, .45, .55, .65, -.35, -.45, -.55, -.65):
                q = p and g.ev(f"""(() => {{ const a = DECK_CREW.find(x => x && x.p); if (!a) return null; const w = placeSpot('4-wet-2'); a.x = w.x + {dx}; a.z = w.z; a.y = 0; a.path = []; a.settled = false; a.spot = null;
                  const v = new THREE.Vector3(w.x, .02, w.z).project(camera), x = (v.x + 1) / 2 * innerWidth, y = (1 - v.y) / 2 * innerHeight;
                  const body = Math.min(...[.5, 1, 1.4].map(hy => {{ _cp.set(a.x, hy, a.z).project(camera); return Math.hypot((_cp.x + 1) / 2 * innerWidth - x, (1 - _cp.y) / 2 * innerHeight - y); }}));
                  return crewAtScreen(x, y) === a && body > 12 && body < 26 && Math.hypot(x - {p[0]}, y - {p[1]}) > 26 ? [a.p.name, x, y, Math.round(body)] : null; }})()""")
                if q:
                    g.page.mouse.move(q[1], q[2]); g.page.mouse.down(); g.page.mouse.up(); g.step(5)
                    side = [rot, dx, q[0], q[3], g.ev("ACT && ACT.kind")]; g.ev("actEnd(true)"); break
            if side: break
            g.page.click('#rot'); g.step(30)
        print('   beside someone [turn, offset, who, px from them, started]:', side)
        check(side and side[4] == 'ixStop', f'a tap on the floor at the puddle just beside someone (not on them) mops it ({side})')
        print('   at the pin [turn, standing on it, under the tap, started]:', res, '| a tap on someone away from it:', chat)
        check(any(r[2] for r in res), f'(someone under the pin in some camera turn: {res})')
        check(len(res) == 4 and all(r[3] == 'ixStop' for r in res), f'a tap at the pin mops the puddle, with someone standing on it ({res})')
        check(bool(chat[0]) and chat[1] != 'ixStop' and chat[2] is True, f'a tap on someone away from the pin still talks to them ({chat})')
        g.ev("actEnd(true); SHIP.jobs = SHIP.jobs.filter(j => j.kind !== 'incident')")
        check(not g.errors, f'no console errors ({g.errors[:3]})')
    g.close()

# FX3 (fresh-eyes batch 2, items 33 and 38; lead 29): the arrow's pin on the thing you need, and a tap at the pin is that thing:
# a part you make points at the lathe (it pointed at the machine shop's middle), and "Turn it in at the job board" opens the
# board from its pin (the pin sat on empty floor when the board's wall was cut away). Four camera turns, real taps at the pin
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1]); g.step(5)
    if g.ev("typeof jobReserve === 'function' && typeof MAKE_AT !== 'undefined' && !!placeById('5-make-1')"):
        print('== FX3: the pin on the lathe and on the job board')
        g.ev("(() => { if (SHIP.device && SHIP.device.settings) SHIP.device.settings.tips = false; const t = document.getElementById('devTip'); if (t) t.hidden = true; })()")   # a first-time tip card can sit over the pin
        g.page.click('#crew'); g.step(5)   # the crew hidden: someone standing at the pin takes the tap (her card), as they should
        PIN = r"""(() => { const el = document.getElementById('ixGoal'), m = (el.style.transform.match(/translate\(([-\d.]+)px, ?([-\d.]+)px\)/) || []).slice(1).map(Number);
          return el.hidden || !m.length ? null : [m[0], m[1], el.children[2].textContent]; })()"""
        MAKE = r"""(() => { actEnd(true); for (const k of NEED_KEYS) SHIP.player.needs[k] = 100; needsT = null; NEED_GOAL = null; clearGoal(); closeLiftPanel && 0; if (typeof ixBoard !== 'undefined' && ixBoard.close) ixBoard.close(); setShipNow(1440 * 2 + 10 * 60); machinesNow(); for (const j of SHIP.jobs) if (j.claimedBy === 'you') { j.claimedBy = null; j.status = 'open'; }
          SHIP.player.carry = []; SHIP.player.work = null; const id = jobReserve('lights', SHIP.time.day, Math.max(0, SHIP.time.min - 1), 3); claimJob(id); SHIP.player.track = id; myWork(); const j = myJob();
          for (const p of j.parts) if (p !== j.make) SHIP.player.carry.push(p); if (deckDef.num !== 5) goToDeck(5); const s = placeSpot('5-make-1'); player.obj.position.set(s.x + 1.5, 0, s.z + 1); player.stop(); return id; })()"""
        TURN = r"""(() => { actEnd(true); for (const k of NEED_KEYS) SHIP.player.needs[k] = 100; needsT = null; NEED_GOAL = null; clearGoal(); const j = myJob(); if (j) { j.workDone = true; MACH_REV++; } SHIP.player.carry = []; const c = cellPos(...placeById('5-jobboard-1').at); player.obj.position.set(c.x + 1, 0, c.z + 2.5); player.stop(); })()"""
        res = {'lathe': [], 'board': []}
        for rot in range(4):
            jid = g.ev(MAKE); g.step(80); p = g.ev(PIN)
            if p:
                g.page.mouse.move(p[0], p[1]); g.page.mouse.down(); g.page.mouse.up(); g.step(400)
                res['lathe'].append([rot, p[2], g.ev("ACT && ACT.kind"), g.ev(f"(e => e && (e.id || e.tagName))(document.elementFromPoint({p[0]}, {p[1]}))")])
            g.ev(TURN); g.step(80); p = g.ev(PIN)
            if p:
                g.page.mouse.move(p[0], p[1]); g.page.mouse.down(); g.page.mouse.up(); g.step(400)
                res['board'].append([rot, p[2], g.ev("!!document.getElementById('ixBoard') && !document.getElementById('ixBoard').hidden"), g.ev(f"(e => e && (e.id || e.tagName))(document.elementFromPoint({p[0]}, {p[1]}))")])
            g.ev("(() => { const b = document.getElementById('ixBoard'); if (b) b.hidden = true; const j = myJob(); if (j) dropJob(j.id); })()"); g.page.click('#rot'); g.step(30)
        print('   the lathe [turn, label, started]:', res['lathe'])
        print('   the job board [turn, label, opened]:', res['board'])
        check(len(res['lathe']) == 4 and all(x[1].endswith('at the lathe') and x[2] == 'make' for x in res['lathe']), f'a part you make: the pin on the lathe, and a tap there makes it ({res["lathe"]})')
        check(len(res['board']) == 4 and all(x[1].startswith('Turn it in') and x[2] for x in res['board']), f'turn it in: a tap at the pin opens the job board ({res["board"]})')
        # a manifest run's first stop, the cart at Cart dock 1 (lead 29): the pin stands over the docks; a tap at the pin, or on
        # Cart dock 1 itself, takes the cart (on 2b4a05db the pin over a dock did nothing)
        HAUL = r"""(() => { actEnd(true); const b = document.getElementById('ixBoard'); if (b) b.hidden = true; for (const k of NEED_KEYS) SHIP.player.needs[k] = 100; needsT = null; NEED_GOAL = null; clearGoal();
          setShipNow(1440 * 3 + 13 * 60); machinesNow(); for (const j of SHIP.jobs) if (j.claimedBy === 'you') { j.claimedBy = null; j.status = 'open'; } SHIP.jobs = SHIP.jobs.filter(j => j.id !== 'fx3-haul');
          SHIP.manifest = manifestFor(4); const j = haulJob(shipNow(), haulCrates(), { crew: false }); j.id = 'fx3-haul'; SHIP.jobs.push(j); MACH_REV++; claimJob('fx3-haul'); SHIP.player.track = 'fx3-haul'; SHIP.player.carry = [];
          if (deckDef.num !== 5) goToDeck(5); const s = placeSpot(haulDock()); player.obj.position.set(s.x + 1.5, 0, s.z + 1); player.stop(); })()"""
        hl = []
        if g.ev("typeof haulJob === 'function' && typeof haulDock === 'function' && !!haulDock()"):
            for rot in range(4):
                g.ev(HAUL); g.step(80); p = g.ev(PIN)
                if p:
                    g.page.mouse.move(p[0], p[1]); g.page.mouse.down(); g.page.mouse.up(); g.step(300)
                    hl.append([rot, p[2], g.ev("ACT && ACT.kind")])
                g.page.click('#rot'); g.step(30)
            print('   the cart stop [turn, label, started]:', hl)   # (a tap on Cart dock 1 itself: FB1's choreThingTap on claude/fe-cartdock, its own check)
            check(len(hl) == 4 and all(x[1].startswith('Take a hover cart') and x[2] == 'ixStop' for x in hl), f'a run\'s cart stop: a tap at the pin takes the cart ({hl})')
            g.ev("actEnd(true); SHIP.jobs = SHIP.jobs.filter(j => j.id !== 'fx3-haul')")
        check(not g.errors, f'no console errors ({g.errors[:3]})')
    g.close()

# FB1 (lead 29, from the arrows_check week guide): Hauling's first stop "Take a hover cart from the Cart bay" and its last
# "Cart back to its dock" have their pin by Cart dock 1, a machine; a tap on the dock said "Cart dock 1: in good order" and
# nothing started. Now a machine within reach of a haul's next stop (JOB_REACH from its edge) does the stop: real taps on
# the dock itself, four camera turns, for both stops. The machines further off (the Lathe, the Breaker cabinet, the washers
# by the laundry drop, the Electrolyser by a shelf) are out of reach and keep their own; plain chores keep 0.28.55's rule
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1]); g.step(5)
    if g.ev("typeof manifestRun === 'function' && !!JOB_KINDS.haul && !!placeById('5-cart-1')"):
        print('== FB1: the hover cart at Cart dock 1')
        g.ev("goToDeck(5)"); g.step(5)
        TIPOFF = "(() => { if (SHIP.device && SHIP.device.settings) SHIP.device.settings.tips = false; const t = document.getElementById('devTip'); if (t) t.hidden = true; })()"   # a first-time tip card can sit over the thing
        SET = r"""(tag => { actEnd(true); setShipNow(1440 * 2 + 10 * 60); machinesNow(); for (const j of SHIP.jobs) if (j.claimedBy === 'you') { j.claimedBy = null; j.status = 'open'; }
          SHIP.jobs = SHIP.jobs.filter(j => !/^parts-fb1/.test(j.id)); SHIP.player.carry = []; SHIP.player.cart = null; SHIP.stores.relay = Math.max(SHIP.stores.relay || 0, 5);
          for (const k of NEED_KEYS) SHIP.player.needs[k] = 80;
          const id = manifestRun(['relay'], '3-store-drop', { for: 'fb1' }); if (!id) return null; claimJob(id);
          const st = jobStops(myJob()), k = st.findIndex(x => x.step === tag); for (let i = 0; i < k; i++) jobStepDone(id, i);
          const s = placeSpot('5-cart-1'); player.obj.position.set(s.x + 1.2, 0, s.z + 1.2); player.stop(); return [k, st[k].places[0]]; })"""
        # a point on the screen where the dock itself is under the finger (pick says so), as a player taps it
        ON = r"""(() => { const i = ITEMS.find(i => i.t === 'Cart dock 1'), b = new THREE.Box3().setFromObject(i.hit);
          for (let fy = .5; fy <= .9; fy += .2) for (let fx = .5, n = 0; n < 5; n++, fx = .5 + (n % 2 ? 1 : -1) * Math.ceil(n / 2) * .15) for (const fz of [.5, .3, .7]) {
            const v = new THREE.Vector3(b.min.x + (b.max.x - b.min.x) * fx, b.min.y + (b.max.y - b.min.y) * fy, b.min.z + (b.max.z - b.min.z) * fz).project(camera), x = (v.x + 1) / 2 * innerWidth, y = (1 - v.y) / 2 * innerHeight, h = pick(x, y);
            if (h && h.object.userData.item === i) return [x, y]; }
          return null; })()"""
        res = []
        for tag in ('cart', 'return'):
            for rot in range(4):
                kp = g.ev(f"({SET})('{tag}')"); g.step(60)
                for _ in range(rot): g.page.click('#rot'); g.step(30)
                g.ev(TIPOFF); xy = g.ev(ON)
                if not xy: res.append([tag, rot, 'no point on the dock', None, '']); continue
                g.page.mouse.move(*xy); g.page.mouse.down(); g.page.mouse.up(); g.step(60)
                a = g.ev("JSON.stringify(ACT && [ACT.kind, ACT.o && ACT.o.ixStep])")
                res.append([tag, rot, kp, a, g.ev("document.getElementById('tt').textContent + ': ' + document.getElementById('tx').textContent")[:50]])
        print('   [stop, camera turn, (stop, its place), what started, the toast]:', res)
        for tag in ('cart', 'return'):
            check(sum(1 for r in res if r[0] == tag and r[3]) >= 2, f'the dock under the finger in at least two camera turns for the "{tag}" stop ({res})')
        for r in res:
            if r[3]: check(json.loads(r[3]) == ['ixStop', r[2][0]], f'a real tap on Cart dock 1 does the haul\'s "{r[0]}" stop (camera turn {r[1]}: {r[3]}, {r[4]})')
        # out of reach: the machines further from a haul stop keep their own (JOB_REACH 1.5 from the thing's edge)
        far = g.ev(r"""(() => { const s = placeSpot('5-cart-1'); return ITEMS.filter(i => /^(Lathe|Breaker cabinet)$/.test(i.t) && isShown(i.hit)).map(i => [i.t, Math.round(ixDist(i, s) * 100) / 100]); })()""")
        print('   by the dock, out of reach:', far)
        check(far and all(d >= 1.5 for _, d in far), f'the Lathe and the Breaker cabinet are out of the dock stop\'s reach ({far})')
        g.ev("actEnd(true); SHIP.jobs = SHIP.jobs.filter(j => !/^parts-fb1/.test(j.id))")
        # pushing a haul's cart to its drop, anything in reach does the stop (lead 29): the linen's drop in the laundry, where
        # the Folding table nearest the pin started your own laundry (0.28.55's rule) and the arrows_check follower looped there
        if g.ev("!!placeById('4-laundry-drop')"):
            g.ev("goToDeck(4)"); g.step(5)
            HSET = r'''(() => { actEnd(true); setShipNow(1440 * 2 + 10 * 60);   // 10:00, clear of Yara's 12:00 hauling lesson (its own run and steps took the job, now and then, on a busy runner)
              machinesNow(); for (const j of SHIP.jobs) if (j.claimedBy === 'you') { j.claimedBy = null; j.status = 'open'; }
              SHIP.jobs = SHIP.jobs.filter(j => !/^haul.*fb1|^haul@.*y$/.test(j.id)); SHIP.player.carry = []; for (const k of NEED_KEYS) SHIP.player.needs[k] = 80;
              const j = haulJob(shipNow(), [{ id: 'linen', dest: '4-laundry-drop' }], { yours: true }); SHIP.jobs.push(j); MACH_REV++; const cl = claimJob(j.id); window.__cl = [cl, (myJob() || {}).id, SHIP.jobs.filter(x => x.claimedBy).map(x => x.id + ':' + x.claimedBy + ':' + x.status)];
              const st = jobStops(myJob()), k = st.findIndex(x => x.step === 'deliver'); for (let i = 0; i < k; i++) jobStepDone(j.id, i);
              const s = placeSpot('4-laundry-drop'); player.obj.position.set(s.x + 1, 0, s.z + 1); player.stop(); return [k, j.id]; })()'''
            ONT = ON.replace("i.t === 'Cart dock 1'", "i.t === 'Folding table' && isShown(i.hit) && ixDist(i, placeSpot('4-laundry-drop')) < 1.5")
            fres = []
            for rot in range(4):
                kp = g.ev(HSET); g.step(60)
                check(g.ev("window.__cl[0] && (myJob() || {}).id === window.__cl[1]"), f'(the test holds its haul: {g.ev("JSON.stringify(window.__cl)")})')
                for _ in range(rot): g.page.click('#rot'); g.step(30)
                g.ev(TIPOFF); xy = g.ev(ONT)
                if not xy: fres.append([rot, 'no point on the table', None]); continue
                FT = f"(k => {{ const j = SHIP.jobs.find(x => x.id === {json.dumps(kp[1])}); return j && jobStops(j)[k].done ? JSON.stringify(['ixStop', k]) : JSON.stringify(ACT && [ACT.kind, ACT.o && ACT.o.ixStep]); }})({kp[0]})"   # done already counts
                g.page.mouse.move(*xy); g.page.mouse.down(); g.page.mouse.up(); g.step(60); a = g.ev(FT)
                if a == 'null':
                    print('      (claim)', g.ev('JSON.stringify(window.__cl)'), g.ev('JSON.stringify([(myJob() || {}).id, SHIP.jobs.filter(x => /haul/.test(x.id)).map(x => x.id + ":" + x.claimedBy + ":" + x.status)])'))
                    print('      (diag)', g.ev(f"JSON.stringify([(e => e && (e.id || e.className || e.tagName))(document.elementFromPoint({xy[0]}, {xy[1]})), typeof ride !== 'undefined' && !!ride, typeof FREEZE !== 'undefined' && FREEZE.frozen, !document.getElementById('lift').hidden, typeof PAUSE !== 'undefined' && PAUSE.on, clockText(), deckDef.num, player.here().join(','), player.path.length, (goalNow() || {{}}).label, document.getElementById('tt').textContent])"))
                    g.page.mouse.down(); g.page.mouse.up(); g.step(60); a = g.ev(FT) + ' (tapped twice)'   # a tap lost on a busy runner: a player taps again
                fres.append([rot, kp, a])
            print('   the linen\'s drop, a tap on the Folding table [camera turn, (stop, job), what started]:', fres)
            check(sum(1 for r in fres if r[2]) >= 2, f'the Folding table under the finger in at least two camera turns ({fres})')
            for r in fres:
                if r[2]: check(json.loads(r[2].replace(' (tapped twice)', '')) == ['ixStop', r[1][0]], f'pushing the linen to the laundry, a tap on the Folding table by the drop delivers it (camera turn {r[0]}: {r[2]})')
            # with no haul the table is your laundry again (0.28.55; parity above taps it too)
            g.ev("actEnd(true); for (const j of SHIP.jobs) if (j.claimedBy === 'you') { j.claimedBy = null; j.status = 'open'; } SHIP.jobs = SHIP.jobs.filter(j => !/^haul@.*y$/.test(j.id)); MACH_REV++")
            g.step(5); g.ev(f"(() => {{ const s = placeSpot('4-laundry-drop'); player.obj.position.set(s.x + 1, 0, s.z + 1); player.stop(); }})()"); g.step(30)
            g.ev(TIPOFF); xy = g.ev(ONT)
            if xy:
                g.page.mouse.move(*xy); g.page.mouse.down(); g.page.mouse.up(); g.step(60); a = g.ev("ACT && ACT.kind")
                if a is None: g.page.mouse.down(); g.page.mouse.up(); g.step(60); a = g.ev("ACT && ACT.kind"); print('   (tapped twice: the first tap was lost)')
                print('   no haul, the Folding table:', a)
                check(a == 'ixFold', f'with no haul, the Folding table by the drop is your laundry ({a})')
            g.ev("actEnd(true)")
        check(not g.errors, f'no console errors ({g.errors[:3]})')
    g.close()

# FB1 (lead 29, RV7): every pick-up and drop of a haul and of a delivery, with real screen taps: at the arrow's pin, and on the
# thing nearest the stop when it's in reach, four camera turns each. RV7 found "Crew store stock to the crew store", "Linen to
# the laundry", "Pick up a crate of linen" and the infirmary's medical supplies stuck: the thing under the finger did its own
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1]); g.step(5)
    if g.ev("typeof haulJob === 'function' && typeof DELIVERIES !== 'undefined' && !!haulDock() && !!haulLoadAt()"):
        print('== FB1: every pick-up and drop of a haul and a delivery, real taps')
        g.ev("(() => { if (SHIP.device && SHIP.device.settings) SHIP.device.settings.tips = false; const t = document.getElementById('devTip'); if (t) t.hidden = true; if (typeof bridgeInvite === 'function') bridgeInvite(); else SHIP.bridgeInvited = true; })()")
        g.page.click('#crew'); g.step(5)   # the crew hidden: someone standing at a pin takes the tap (their card), as they should
        PIN = r"""(() => { const el = document.getElementById('ixGoal'), m = (el.style.transform.match(/translate\(([-\d.]+)px, ?([-\d.]+)px\)/) || []).slice(1).map(Number);
          return el.hidden || !m.length ? null : [m[0], m[1], el.children[2].textContent]; })()"""
        # (kind, key, the stop's step): a haul of one crate per drop (its cart, load, deliver and return), a delivery's pickup and drop
        STOPS = g.ev(r"""(() => { const out = [['haul', 'linen', 'cart'], ['haul', 'linen', 'load'], ['haul', 'linen', 'return']];
          for (const k of Object.keys(MANIFEST_DROP)) if (placeById(MANIFEST_DROP[k])) out.push(['haul', k, 'deliver']);
          for (const d of DELIVERIES) if (placeById(d.from) && placeById(d.to)) { out.push(['delivery', d.key, 'pickup']); out.push(['delivery', d.key, 'drop']); }
          return out; })()""")
        SET = r"""(([kind, key, step]) => { actEnd(true); const b = document.getElementById('ixBoard'); if (b) b.hidden = true; for (const k of NEED_KEYS) SHIP.player.needs[k] = 100; needsT = null; NEED_GOAL = null; clearGoal();
          setShipNow(1440 * 2 + 10 * 60); machinesNow(); for (const j of SHIP.jobs) if (j.claimedBy === 'you') { j.claimedBy = null; j.status = 'open'; } SHIP.jobs = SHIP.jobs.filter(j => !/^fb1-/.test(j.id));
          SHIP.player.carry = []; SHIP.player.work = null; if (SHIP.player.crate) SHIP.player.crate = null; const t = shipNow(); let j;
          if (kind === 'haul') { j = haulJob(t, [{ id: key, dest: MANIFEST_DROP[key] }], { crew: false }); j.id = 'fb1-haul'; }
          else { const d = DELIVERIES.find(x => x.key === key), to = placeById(d.to), fr = placeById(d.from);
            j = { id: 'fb1-del', machine: null, deck: to.deck, room: to.room, kind: 'chore', chore: 'delivery', title: d.title, bring: d.bring, tier: 1, urgency: 1, posted: t, found: t, claimedBy: null, parts: [], status: 'open',
              stops: [{ deck: fr.deck, placeId: d.from, mins: 3, tag: 'pickup' }, { deck: to.deck, placeId: d.to, mins: 3, tag: 'drop' }] }; }
          SHIP.jobs.push(j); MACH_REV++; claimJob(j.id); SHIP.player.track = j.id;
          const st = jobStops(myJob()), k = st.findIndex(x => x.step === step); for (let i = 0; i < k; i++) jobStepDone(j.id, i);
          const pid = st[k].places[0], pl = placeById(pid); if (deckDef.num !== pl.deck) goToDeck(pl.deck);
          const s = placeSpot(pid); player.obj.position.copy(cellPos(...nearestOpen(s.x + 1.3, s.z + 1.3, player))); player.stop(); return [k, pid]; })"""
        # a screen point on the thing nearest the stop (in reach, shown), where pick() says that thing is under the finger
        ON = r"""(pid => { const s = placeSpot(pid), its = ITEMS.filter(i => i.hit && isShown(i.hit) && ixDist(i, s) < JOB_REACH).sort((a, b) => ixDist(a, s) - ixDist(b, s));
          for (const i of its) { const b = new THREE.Box3().setFromObject(i.hit);
            for (const fy of [.5, .7, .3, .9]) for (const fx of [.5, .35, .65, .2, .8]) for (const fz of [.5, .35, .65, .2, .8]) {
              const v = new THREE.Vector3(b.min.x + (b.max.x - b.min.x) * fx, b.min.y + (b.max.y - b.min.y) * fy, b.min.z + (b.max.z - b.min.z) * fz).project(camera), x = (v.x + 1) / 2 * innerWidth, y = (1 - v.y) / 2 * innerHeight, h = pick(x, y);
              if (x > 0 && y > 0 && x < innerWidth && y < innerHeight && h && h.object.userData.item === i) return [x, y, i.t]; } }
          return null; })"""
        bad, n = [], {'pin': 0, 'thing': 0}
        for stop in STOPS:
            row = []
            for rot in range(4):
                for how in ('pin', 'thing'):
                    kp = g.ev(f"({SET})({json.dumps(stop)})"); g.step(60)
                    for _ in range(rot): g.page.click('#rot'); g.step(30)
                    g.ev("(() => { const t = document.getElementById('devTip'); if (t) t.hidden = true; })()")   # a first-time tip card can sit over the pin
                    p = g.ev(PIN) if how == 'pin' else g.ev(f"({ON})({json.dumps(kp[1])})")
                    if not p: row.append(f'{rot}{how[0]}:-'); continue
                    g.page.mouse.move(p[0], p[1]); g.page.mouse.down(); g.page.mouse.up(); g.step(400)
                    a = g.ev(f"(k => {{ const j = SHIP.jobs.find(x => /^fb1-/.test(x.id)); return j && jobStops(j)[k].done ? 'done' : JSON.stringify(ACT && [ACT.kind, ACT.o && ACT.o.ixStep]); }})({kp[0]})")
                    good = a == 'done' or a == json.dumps(['ixStop', kp[0]]).replace(' ', '')   # the stop done, or under way (a short stop is over by now)
                    n[how] += 1; row.append(f'{rot}{how[0]}:{"ok" if good else a}' + ('' if how == 'pin' else '(' + p[2] + ')'))
                    if not good: bad.append([stop, rot, how, p[2], a, g.ev("document.getElementById('tt').textContent + ': ' + document.getElementById('tx').textContent")[:60]])
                g.page.click('#rot'); g.step(30)
            print(f'   {stop[0]} {stop[1]} {stop[2]} ({kp[1]}):', ' '.join(row))
        print(f'   taps: {n["pin"]} at the pin, {n["thing"]} on the thing')
        check(n['pin'] >= 3 * len(STOPS) and n['thing'] >= len(STOPS), f'the pin and a thing in reach under the finger for every stop ({n}, {len(STOPS)} stops)')
        for b in bad: check(False, f'a real tap does the stop: {b}')
        g.ev("actEnd(true); SHIP.jobs = SHIP.jobs.filter(j => !/^fb1-/.test(j.id))")
        check(not g.errors, f'no console errors ({g.errors[:3]})')
    g.close()

# FB1 (lead 29, arrows_check week Day 6): "Put the seal back: main storage" (FX3's fix 9) stuck over 3 hours: a tap on the shelf
# nearest the arrow's pin walked you round to the shelf's front, 7 tiles away, and the follower's next step pulled you back.
# Now a part goes back from the shelf's spot nearest the tap, as a fetch does (a step or two from the pin, under 2.2 m): real taps
# on the shelf nearest the pin, four camera turns
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1]); g.step(5)
    if g.ev("typeof ixLoose === 'function' && typeof shelfOf === 'function' && !!shelfOf('seal')"):
        print('== FB1: put a part back from the arrow\'s pin')
        g.ev("goToDeck(5)"); g.step(5); g.page.click('#crew'); g.step(5)
        PB = r"""(() => { actEnd(true); for (const k of NEED_KEYS) SHIP.player.needs[k] = 100; needsT = null; NEED_GOAL = null; clearGoal(); if (SHIP.device && SHIP.device.settings) SHIP.device.settings.tips = false; const t = document.getElementById('devTip'); if (t) t.hidden = true;
          setShipNow(1440 * 5 + 7 * 60 + 30); machinesNow(); for (const j of SHIP.jobs) if (j.claimedBy === 'you') { j.claimedBy = null; j.status = 'open'; } MACH_REV++; SHIP.player.carry = ['seal']; SHIP.player.work = null; SHIP.player.track = undefined;
          const w = placeSpot(shelfOf('seal')); player.obj.position.copy(cellPos(...nearestOpen(w.x, w.z, player))); player.stop(); return [w.x, w.z]; })()"""
        ONS = r"""(w => { const its = ITEMS.filter(i => i.hit && isShown(i.hit) && /^(Lights|Filters|Plumbing|Galley parts)$/.test(i.t)).map(i => { i.hit.getWorldPosition(_wp); return [i, Math.hypot(_wp.x - w[0], _wp.z - w[1])]; }).sort((a, b) => a[1] - b[1]);
          for (const [i] of its.slice(0, 2)) { const b = new THREE.Box3().setFromObject(i.hit);
            for (const fy of [.5, .7, .3]) for (const fx of [.5, .35, .65, .2, .8]) for (const fz of [.5, .35, .65, .2, .8]) {
              const v = new THREE.Vector3(b.min.x + (b.max.x - b.min.x) * fx, b.min.y + (b.max.y - b.min.y) * fy, b.min.z + (b.max.z - b.min.z) * fz).project(camera), x = (v.x + 1) / 2 * innerWidth, y = (1 - v.y) / 2 * innerHeight, h = pick(x, y);
              if (x > 0 && y > 0 && x < innerWidth && y < innerHeight && h && h.object.userData.item === i) return [x, y, i.t]; } }
          return null; })"""
        res = []
        for rot in range(4):
            w = g.ev(PB); g.step(30)
            for _ in range(rot): g.page.click('#rot'); g.step(30)
            lab = g.ev("(goalNow() || {}).label"); p = g.ev(f"({ONS})({json.dumps(w)})")
            if not p: res.append([rot, lab, 'no shelf under the finger']); continue
            g.page.mouse.move(p[0], p[1]); g.page.mouse.down(); g.page.mouse.up(); g.step(3)
            a = g.ev(f"(w => ACT && ACT.kind === 'stow' && ACT.spot ? ['stow', Math.round(Math.hypot(ACT.spot.x - w[0], ACT.spot.z - w[1]) * 10) / 10] : [ACT && ACT.kind, null])({json.dumps(w)})")
            g.step(600); res.append([rot, lab, p[2], a, g.ev("JSON.stringify(SHIP.player.carry)")])
        print('   [camera turn, the arrow, shelf tapped, (started, its spot from the pin in m), in hand after]:', res)
        check(len([r for r in res if len(r) > 3]) >= 3, f'a shelf by the pin under the finger in at least three camera turns ({res})')
        for r in res:
            if len(r) > 3: check(r[1] == 'Put the seal back: main storage' and r[3][0] == 'stow' and r[3][1] is not None and r[3][1] < 2.2 and r[4] == '[]',
                                 f'a tap on the shelf by the put-back pin puts the seal back from the spot by the pin (camera turn {r[0]}: {r})')
        check(not g.errors, f'no console errors ({g.errors[:3]})')
    g.close()

# FB1 (lead 29, arrows_check week Day 4): "Clean a vent: hydroponics garden" stuck over 3 hours from 13:12: its stop is the
# garden's tending spot (3-tend-1) by the Orange tree, and from two camera turns of four the arrow's pin stands over the tree
# (or the Salad bed), which took the tap as "Tend a bed". Now any chore: a tap on the line to its next stop does the stop,
# whatever caught it (FX3's fix 14, past machines). Every vent and lamp chore stop, real taps at the pin, four camera turns;
# and the Orange tree tapped off the pin is still the garden (0.28.55)
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1]); g.step(5)
    if g.ev("typeof choreWhere === 'function' && choreWhere('vent').some(c => c.key === '3-tend-1')"):
        print('== FB1: a tap at a chore\'s pin does the stop, whatever is under it (vents and lamps)')
        g.page.click('#crew'); g.step(5)
        PIN = r"""(() => { const el = document.getElementById('ixGoal'), m = (el.style.transform.match(/translate\(([-\d.]+)px, ?([-\d.]+)px\)/) || []).slice(1).map(Number);
          return el.hidden || !m.length ? null : [m[0], m[1], el.children[2].textContent]; })()"""
        SET = r"""(([kind, key]) => { actEnd(true); for (const k of NEED_KEYS) SHIP.player.needs[k] = 100; needsT = null; NEED_GOAL = null; clearGoal(); if (SHIP.device && SHIP.device.settings) SHIP.device.settings.tips = false; const tp = document.getElementById('devTip'); if (tp) tp.hidden = true;
          setShipNow(1440 * 3 + 13 * 60 + 10); machinesNow(); for (const j of SHIP.jobs) if (j.claimedBy === 'you') { j.claimedBy = null; j.status = 'open'; } SHIP.jobs = SHIP.jobs.filter(j => !/^fb1-/.test(j.id));
          const c = choreWhere(kind).find(c => c.key === key), t = shipNow(), st = c.stops[0];
          SHIP.jobs.push({ id: 'fb1-chore', machine: null, deck: st.deck, room: c.room, kind: 'chore', chore: kind, target: c.key, title: c.title, tier: 1, stops: c.stops.map(x => ({ ...x })), urgency: 0, posted: t, found: t, claimedBy: null, status: 'open', parts: kind === 'lamp' ? ['lamp'] : [] });
          MACH_REV++; claimJob('fb1-chore'); SHIP.player.track = 'fb1-chore'; SHIP.player.carry = kind === 'lamp' ? ['lamp'] : []; SHIP.player.work = null; if (deckDef.num !== st.deck) goToDeck(st.deck);
          jobStops(myJob()).forEach((x, i) => { if (x.step === 'fetch') jobStepDone('fb1-chore', i); });   // the lamp in hand (as 0.28.55's test)
          const s = placeSpot(st.placeId); player.obj.position.copy(cellPos(...(nearestOpen(s.x + 1.3, s.z + 1.3, player) || nearestOpen(s.x, s.z, player)))); player.stop(); return ixNextStop(myJob()).k; })"""
        UNDER = "(p => { const h = pick(p[0], p[1]); return h && h.object.userData.item ? h.object.userData.item.t : 'floor'; })"
        stops = g.ev("['vent', 'lamp'].flatMap(k => choreWhere(k).map(c => [k, c.key]))")
        bad, things, n = [], set(), 0
        for cs in stops:
            row = []
            for rot in range(4):
                k = g.ev(f"({SET})({json.dumps(cs)})"); g.step(40); want = json.dumps(['ixStop', k]).replace(' ', '')
                for _ in range(rot): g.page.click('#rot'); g.step(30)
                g.ev("(() => { const t = document.getElementById('devTip'); if (t) t.hidden = true; })()"); p = g.ev(PIN)
                if not p: row.append('-'); continue
                u = g.ev(f"({UNDER})({json.dumps(p)})"); g.page.mouse.move(p[0], p[1]); g.page.mouse.down(); g.page.mouse.up(); g.step(20)
                a = g.ev("JSON.stringify(ACT && [ACT.kind, ACT.o && ACT.o.ixStep])"); n += 1
                if u != 'floor': things.add(u)
                row.append(('ok' if a == want else a) + '(' + u + ')')
                if a != want: bad.append([cs, rot, u, a])
                g.page.click('#rot'); g.step(30)
            print(f'   {cs[0]} {cs[1]}:', ' '.join(row))
        print(f'   {n} taps at the pin; things under it: {sorted(things)}')
        check(n >= 3 * len(stops), f'the pin under the finger in most turns ({n} taps, {sorted(things)})')
        for b in bad: check(False, f'a real tap at a chore\'s pin does the stop: {b}')
        # the garden over the hydroponics vent's pin, whatever the camera does (whether a pin lands on the tree depends on the
        # turn and the pin's drawing): a real tap on the Orange tree or the Salad bed whose line passes over the stop
        GARDEN = r"""(() => { const s = placeSpot('3-tend-1');
          for (const i of ITEMS.filter(i => i.hit && isShown(i.hit) && /^(Orange tree|Salad bed)$/.test(i.t))) { const b = new THREE.Box3().setFromObject(i.hit);
            for (let fy = .1; fy <= .95; fy += .1) for (let fx = .1; fx <= .95; fx += .2) for (let fz = .1; fz <= .95; fz += .2) {
              const v = new THREE.Vector3(b.min.x + (b.max.x - b.min.x) * fx, b.min.y + (b.max.y - b.min.y) * fy, b.min.z + (b.max.z - b.min.z) * fz).project(camera), x = (v.x + 1) / 2 * innerWidth, y = (1 - v.y) / 2 * innerHeight;
              if (!(x > 0 && y > 0 && x < innerWidth && y < innerHeight)) continue; const h = pick(x, y); if (!h || h.object.userData.item !== i) continue;
              ndc.set(v.x, v.y); ray.setFromCamera(ndc, camera); if (jobRayDist(s) < JOB_RAY) return [x, y, i.t]; } }
          return null; })()"""
        gres = []
        for rot in range(4):
            k = g.ev(f"({SET})({json.dumps(['vent', '3-tend-1'])})"); g.step(40)
            for _ in range(rot): g.page.click('#rot'); g.step(30)
            g.ev("(() => { const t = document.getElementById('devTip'); if (t) t.hidden = true; })()"); q = g.ev(GARDEN)
            if q:
                g.page.mouse.move(q[0], q[1]); g.page.mouse.down(); g.page.mouse.up(); g.step(20)
                gres.append([rot, q[2], g.ev("JSON.stringify(ACT && [ACT.kind, ACT.o && ACT.o.ixStep])"), k])
            g.page.click('#rot'); g.step(30)
        print('   the garden on the line over the hydroponics vent [camera turn, thing, what started]:', gres)
        check(gres, 'a point on the Orange tree or the Salad bed whose tap line passes over the vent stop, in some camera turn')
        for r in gres: check(r[2] == json.dumps(['ixStop', r[3]]).replace(' ', ''), f'a tap on the garden, on the line over the vent\'s stop, cleans the vent ({r})')
        # off the pin, the Orange tree is the garden still (0.28.55: a thing you can use does its own thing)
        g.ev(f"({SET})({json.dumps(['vent', '3-tend-1'])})"); g.step(40)
        off = g.ev(r"""(() => { const s = placeSpot('3-tend-1'), i = ITEMS.filter(i => i.t === 'Orange tree' && isShown(i.hit)).sort((a, b) => ixDist(a, s) - ixDist(b, s))[0]; if (!i) return null; const b = new THREE.Box3().setFromObject(i.hit);
          for (const fy of [.6, .8, .4]) for (const fx of [.5, .3, .7]) for (const fz of [.5, .3, .7]) { const v = new THREE.Vector3(b.min.x + (b.max.x - b.min.x) * fx, b.min.y + (b.max.y - b.min.y) * fy, b.min.z + (b.max.z - b.min.z) * fz).project(camera), x = (v.x + 1) / 2 * innerWidth, y = (1 - v.y) / 2 * innerHeight, h = pick(x, y);
            if (h && h.object.userData.item === i && (ray.setFromCamera(new THREE.Vector2(v.x, v.y), camera), jobRayDist(s) >= JOB_RAY)) return [x, y]; }
          return null; })()""")
        if off:
            g.page.mouse.move(*off); g.page.mouse.down(); g.page.mouse.up(); g.step(20); a = g.ev("ACT && ACT.kind")
            print('   the Orange tree off the pin:', a); check(a == 'ixGarden', f'the Orange tree tapped off the pin is the garden, not the vent ({a})')
        # RV8: playerTap called some other way (a check, another section) after a real tap at the pin: the pin's line is that old
        # tap's, not this one's, so a garden thing far from it is the garden, not the vent
        g.ev(f"({SET})({json.dumps(['vent', '3-tend-1'])})"); g.step(40)
        for _ in range(4):
            g.ev("(() => { const t = document.getElementById('devTip'); if (t) t.hidden = true; })()"); p = g.ev(PIN)
            if p and g.ev(f"({UNDER})({json.dumps(p)})") == 'floor': break
            g.page.click('#rot'); g.step(30)
        if p:
            g.page.mouse.move(p[0], p[1]); g.page.mouse.down(); g.page.mouse.up(); g.step(5)
            stale = g.ev(r"""(() => { actEnd(true); const s = placeSpot('3-tend-1'), o = ray.ray.origin, d = ray.ray.direction, f = -o.y / d.y, fx = o.x + d.x * f, fz = o.z + d.z * f;
              const it = ITEMS.filter(i => i.hit && /bed|tree|planter|herb/i.test(i.t) && roomAt(...cellAt(i.hit.getWorldPosition(_wp).x, _wp.z)) === 'G').map(i => { i.hit.getWorldPosition(_wp); return [i, _wp.clone()]; })
                .filter(([i, q]) => jobRayDist({ x: q.x, z: q.z }) > 2.5 && ixDist(i, s) > 2.5)[0];   // far from the old line's 0-1.7 m band (FX4)
              if (!it) return null; playerTap(it[0], it[1].clone(), it[1].clone()); return [it[0].t, ACT && ACT.kind]; })()""")
            print('   a garden thing tapped some other way after a pin tap:', stale)
            if check(stale, 'a garden thing far from the pin to tap'): check(stale[1] != 'ixStop', f'a playerTap made some other way after a pin tap does its own thing, not the vent (the old line is not this tap\'s: {stale})')
        g.ev("actEnd(true); SHIP.jobs = SHIP.jobs.filter(j => !/^fb1-/.test(j.id))")
        check(not g.errors, f'no console errors ({g.errors[:3]})')
    g.close()

# FB1 (lead 30, AC2's Day 2 run): "Take dry goods to the galley" stuck all day. The arrow's dot is drawn above its 1.2 m anchor
# and bobs; a tap on it crosses the stop's line at about 1.6 m, and the tap's line was only looked at from the floor to 1.2 m
# (jobRayDist), where it read 0.57-0.6 m off against 0.6: the same tap did the stop or only walked, as the dot bobbed. Now it
# looks to 2 m. Real taps on the top edge of the drawn dot at the top of its bob (any of its 22 px is the pin to a player), four
# camera turns: every delivery's pick-up and
# drop, every haul drop, and every vent
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1]); g.step(5)
    if g.ev("typeof DELIVERIES !== 'undefined' && typeof haulJob === 'function' && typeof choreWhere === 'function'"):
        print('== FB1: a tap on the top of the drawn dot, at the top of its bob, does the stop')
        g.page.click('#crew'); g.step(5)
        g.ev("(() => { const st = document.createElement('style'); st.textContent = '#ixGoal .ixpin{animation:none !important}'; document.head.appendChild(st); if (typeof bridgeInvite === 'function') bridgeInvite(); else SHIP.bridgeInvited = true; })()")   # the dot held still, then 5 px up: the top of its bob
        DOT = r"""(() => { const pe = document.getElementById('ixGoal'), pd = pe && !pe.hidden && pe.children[1]; if (!pd || getComputedStyle(pd).display === 'none') return null; const r = pd.getBoundingClientRect(); return [r.left + r.width / 2, r.top + 2 - 5, pe.children[2].textContent]; })()"""
        STOPS = g.ev(r"""(() => { const out = [];
          for (const k of Object.keys(MANIFEST_DROP)) if (placeById(MANIFEST_DROP[k])) out.push(['haul', k, 'deliver']);
          for (const d of DELIVERIES) if (placeById(d.from) && placeById(d.to)) { out.push(['delivery', d.key, 'pickup']); out.push(['delivery', d.key, 'drop']); }
          for (const c of choreWhere('vent')) out.push(['vent', c.key, 'vent']);
          return out; })()""")
        SET = r"""(([kind, key, step]) => { actEnd(true); const b = document.getElementById('ixBoard'); if (b) b.hidden = true; for (const k of NEED_KEYS) SHIP.player.needs[k] = 100; needsT = null; NEED_GOAL = null; clearGoal();
          if (SHIP.device && SHIP.device.settings) SHIP.device.settings.tips = false; const tp = document.getElementById('devTip'); if (tp) tp.hidden = true;
          setShipNow(1440 * 2 + 10 * 60); machinesNow(); for (const j of SHIP.jobs) if (j.claimedBy === 'you') { j.claimedBy = null; j.status = 'open'; } SHIP.jobs = SHIP.jobs.filter(j => !/^fb1-/.test(j.id));
          SHIP.player.carry = []; SHIP.player.work = null; if (SHIP.player.crate) SHIP.player.crate = null; const t = shipNow(); let j;
          if (kind === 'haul') { j = haulJob(t, [{ id: key, dest: MANIFEST_DROP[key] }], { crew: false }); j.id = 'fb1-dot'; }
          else if (kind === 'vent') { const c = choreWhere('vent').find(c => c.key === key); j = { id: 'fb1-dot', machine: null, deck: c.stops[0].deck, room: c.room, kind: 'chore', chore: 'vent', target: c.key, title: c.title, tier: 1, stops: c.stops.map(x => ({ ...x })), urgency: 0, posted: t, found: t, claimedBy: null, status: 'open', parts: [] }; }
          else { const d = DELIVERIES.find(x => x.key === key), to = placeById(d.to), fr = placeById(d.from);
            j = { id: 'fb1-dot', machine: null, deck: to.deck, room: to.room, kind: 'chore', chore: 'delivery', title: d.title, bring: d.bring, tier: 1, urgency: 1, posted: t, found: t, claimedBy: null, parts: [], status: 'open',
              stops: [{ deck: fr.deck, placeId: d.from, mins: 3, tag: 'pickup' }, { deck: to.deck, placeId: d.to, mins: 3, tag: 'drop' }] }; }
          SHIP.jobs.push(j); MACH_REV++; claimJob(j.id); SHIP.player.track = j.id;
          const st = jobStops(myJob()), k = st.findIndex(x => x.step === step); for (let i = 0; i < k; i++) jobStepDone(j.id, i);
          const pid = st[k].places[0], pl = placeById(pid); if (deckDef.num !== pl.deck) goToDeck(pl.deck);
          const s = placeSpot(pid); player.obj.position.copy(cellPos(...s.walk)); player.stop(); return [k, pid]; })"""
        bad, n = [], 0
        for stop in STOPS:
            row = []
            for rot in range(4):
                kp = g.ev(f"({SET})({json.dumps(stop)})"); g.step(40)
                for _ in range(rot): g.page.click('#rot'); g.step(30)
                g.ev("(() => { const t = document.getElementById('devTip'); if (t) t.hidden = true; })()"); p = g.ev(DOT)
                if not p: row.append('-'); g.page.click('#rot'); g.step(30); continue
                g.page.mouse.move(p[0], p[1]); g.page.mouse.down(); g.page.mouse.up(); g.step(20); n += 1
                a = g.ev(f"(k => {{ const j = SHIP.jobs.find(x => x.id === 'fb1-dot'); return j && jobStops(j)[k].done ? 'done' : JSON.stringify(ACT && [ACT.kind, ACT.o && ACT.o.ixStep]); }})({kp[0]})")
                good = a == 'done' or a == json.dumps(['ixStop', kp[0]]).replace(' ', ''); row.append('ok' if good else a)
                if not good: bad.append([stop, rot, kp[1], a])
                g.page.click('#rot'); g.step(30)
            print(f'   {stop[0]} {stop[1]} {stop[2]}:', ' '.join(row))
        print(f'   {n} taps on the dot')
        check(n >= 3 * len(STOPS), f'the dot on screen in most camera turns ({n} taps, {len(STOPS)} stops)')
        for b in bad: check(False, f'a real tap on the drawn dot does the stop: {b}')
        # lead 30: the pin doesn't catch taps meant for something else. Off the pin, a thing by a vent stop does its own thing;
        # with the job gone, the same tap on the lift door at a lift lobby calls the lift; a person standing at the stop is a person
        OFF = r"""(pid => { const s = placeSpot(pid);
          for (const i of ITEMS.filter(i => i.hit && isShown(i.hit) && !i.lift && ixDist(i, s) < 2.5).sort((a, b) => ixDist(a, s) - ixDist(b, s))) { const b = new THREE.Box3().setFromObject(i.hit);
            for (const fy of [.5, .3, .7]) for (const fx of [.5, .3, .7]) for (const fz of [.5, .3, .7]) {
              const v = new THREE.Vector3(b.min.x + (b.max.x - b.min.x) * fx, b.min.y + (b.max.y - b.min.y) * fy, b.min.z + (b.max.z - b.min.z) * fz).project(camera), x = (v.x + 1) / 2 * innerWidth, y = (1 - v.y) / 2 * innerHeight, h = pick(x, y);
              if (!(x > 0 && y > 0 && x < innerWidth && y < innerHeight && h && h.object.userData.item === i)) continue;
              ndc.set(v.x, v.y); ray.setFromCamera(ndc, camera); if (jobRayDist(s) >= JOB_RAY) return [x, y, i.t]; } }
          return null; })"""
        offs = []
        for vk in [st[1] for st in STOPS if st[0] == 'vent']:
            g.ev(f"({SET})({json.dumps(['vent', vk, 'vent'])})"); g.step(40); g.ev("(() => { const t = document.getElementById('devTip'); if (t) t.hidden = true; })()")
            q = g.ev(f"({OFF})({json.dumps(vk)})")
            if not q: continue
            g.page.mouse.move(q[0], q[1]); g.page.mouse.down(); g.page.mouse.up(); g.step(20); withJob = g.ev("ACT && ACT.kind")
            g.ev("(() => { actEnd(true); const j = myJob(); if (j) dropJob(j.id); SHIP.player.track = undefined; clearGoal(); })()"); g.step(5)
            g.page.mouse.move(q[0], q[1]); g.page.mouse.down(); g.page.mouse.up(); g.step(20); own = g.ev("ACT && ACT.kind")
            offs.append([vk, q[2], withJob, own])
        print('   a thing by a vent stop, tapped off the pin [stop, thing, with the vent job, with no job]:', offs)
        check(len([o for o in offs if o[3]]) >= 2, f'things with a use of their own by two vent stops or more, to tap off the pin ({offs})')
        for o in offs:
            if o[3]: check(o[2] == o[3], f'a thing by a vent stop tapped off the pin does its own thing with the job too, not the vent ({o})')   # scenery with no use of its own may do the stop (0.28.55)
        lifts = []
        for vk in [st[1] for st in STOPS if st[0] == 'vent' and '-lift' in st[1]]:
            for rot in range(4):
                g.ev(f"({SET})({json.dumps(['vent', vk, 'vent'])})"); g.step(40)
                for _ in range(rot): g.page.click('#rot'); g.step(30)
                g.ev("(() => { const t = document.getElementById('devTip'); if (t) t.hidden = true; })()"); p = g.ev(DOT)
                lift = p and g.ev(f"(() => {{ const h = pick({p[0]}, {p[1]}), u = h && h.object.userData; return !!(u && (u.liftDoor || u.item && u.item.lift)); }})()")
                if lift:
                    g.page.mouse.move(p[0], p[1]); g.page.mouse.down(); g.page.mouse.up(); g.step(20); withJob = g.ev("ACT && ACT.kind")
                    g.ev("(() => { actEnd(true); const j = myJob(); if (j) dropJob(j.id); SHIP.player.track = undefined; clearGoal(); })()"); g.step(5)
                    g.page.mouse.move(p[0], p[1]); g.page.mouse.down(); g.page.mouse.up(); called = False
                    for _ in range(40):
                        g.step(10)
                        if g.ev("!document.getElementById('lift').hidden || (typeof ride !== 'undefined' && !!ride)"): called = True; break
                    lifts.append([vk, rot, withJob, called]); g.ev("(() => { if (typeof closeLiftPanel === 'function') closeLiftPanel(); })()"); g.step(5)
                g.page.click('#rot'); g.step(30)
                if lifts and lifts[-1][0] == vk: break
        print('   the dot over a lift door [stop, camera turn, with the job, without it the lift came]:', lifts)
        check(len(lifts) >= 2, f'the dot over the lift door at two lift lobbies or more ({lifts})')
        for l in lifts: check(l[2] == 'ixStop' and l[3], f'over the lift door: with the vent job the tap cleans the vent, without it the lift comes ({l})')
        # a person standing at the stop: the crew shown again, one of them moved to the galley drop; a tap on their head is them
        g.page.click('#crew'); g.step(5); g.ev(f"({SET})({json.dumps(['delivery', 'galley', 'drop'])})"); g.step(20)
        PER = r"""(() => { const s = placeSpot('3-cold-1'), a = DECK_CREW.find(c => c.p && c.p.name); if (!a) return null; a.x = s.x + .4; a.z = s.z + .2; a.settled = false; a.pose = 'stand'; if (a.path) a.path.length = 0;   // standing there
          const v = new THREE.Vector3(a.x, (a.y || 0) + 1.4, a.z).project(camera); return [(v.x + 1) / 2 * innerWidth, (1 - v.y) / 2 * innerHeight, a.p.name]; })()"""
        hd = g.ev(PER)
        if hd:
            g.page.mouse.move(hd[0], hd[1]); g.page.mouse.down(); g.page.mouse.up(); g.step(3)
            res = g.ev("[ACT && ACT.kind, document.getElementById('tt').textContent, !!document.querySelector('#chat:not([hidden]), .chat:not([hidden])')]")
            print('   a person at the galley drop, tapped on the head:', hd[2], res)
            check(res[0] != 'ixStop' and (res[1] == hd[2] or res[2]), f'a person standing at the stop, tapped, is that person, not the drop ({hd[2]}: {res})')
        g.ev("actEnd(true); SHIP.jobs = SHIP.jobs.filter(j => !/^fb1-/.test(j.id))")
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

# Tracked (0.72.0, HUD U; the user's playtest notes; since 0.72.4 also a device app, first in its list, the HUD button kept): what's on
# and coming up, your job and the fixed places, each tracked with the goal arrow on a tap and stopped on a second; the
# device's app labels on one line on a 320 px phone
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 320, 640)
    if g.ev("typeof DEVICE_APPS !== 'undefined' && DEVICE_APPS.has('tracked')"):
        print('== tracked')
        g.ev("typeof introSkip === 'function' && introSkip()"); g.step(3)
        g.ev("skipTo(17 * 60 + 40)"); g.step(3)
        job = g.ev("(() => { const o = openJobs('you'); return o.length && claimJob(o[0].id) ? myJob().id : null })()")
        g.ev("clearGoal(); if (myJob()) SHIP.player.track = myJob().id"); g.step(3)   # as Take it at the board does (no other arrow up)
        g.page.click('#devBtn'); g.step(3); g.ev("deviceShow('home')"); g.step(1)
        first = g.ev("(document.querySelector('.device .app span') || {}).textContent || ''")
        check(first.lower() == 'schedule tracker', f'the Schedule tracker (was Tracked; the user, 0.92.3 #14) is the first app on the device ({first})')
        ROWS = "JSON.stringify([...document.querySelectorAll('#devBody .list .row')].map(r => [r.querySelector('.rt').textContent, r.classList.contains('hot'), r.tagName === 'BUTTON']))"
        OPEN = "deviceShow('tracked')"
        def tap(text):
            return g.ev(f"(() => {{ const r = [...document.querySelectorAll('#devBody .list button.row')].find(b => b.querySelector('.rt').textContent.includes({json.dumps(text)})); if (r) r.click(); return !!r; }})()")
        g.ev(OPEN); g.step(2)
        rows = json.loads(g.ev(ROWS)); titles = [r[0] for r in rows]
        check(g.ev("DEV.open && DEV.app === 'tracked'"), 'the Tracked app opens')
        check(all(any(t in x for x in titles) for t in ['The job board', 'Your bunk', 'The call booths']), f'the fixed places are listed ({titles})')
        check(job is None or g.ev("myJob().title") in titles[0], f'your job comes first ({titles[:1]})')
        check(any(any(t in x for x in titles) for t in ['Dinner', 'Gym club', 'Lap of the Wren']), f"the evening's items are listed ({titles})")
        check(job is None or rows[0][1], 'your job, taken at the board, shows as Tracking')
        tap('Your bunk'); g.step(3)
        s = st()
        check(not g.ev("DEV.open") and g.ev("IX_GOAL && IX_GOAL.trk") == 'place:bed' and s['goal'] == 'Your bunk', f'a tap tracks your bunk and closes the device ({s["goal"]})')
        g.page.click('#devBtn'); g.step(2); g.ev(OPEN); g.step(2)
        rows = json.loads(g.ev(ROWS)); on = [r[0] for r in rows if r[1]]
        check(len(on) == 1 and 'Your bunk' in on[0], f'only your bunk shows as Tracking now ({on})')
        tap('Your bunk'); g.step(3)
        check(g.ev("IX_GOAL") is None and g.ev("SHIP.player.track") == job and g.ev("DEV.open"), 'a second tap stops it (no arrow of its own; your job, still tracked, has the arrow back), the device stays open')   # FX1: tracking a place no longer switches job tracking off
        if job:
            tap(g.ev("myJob().title")); g.step(3); off = g.ev("SHIP.player.track")
            tap(g.ev("myJob().title")); g.step(3)   # (a stop leaves the device open)
            check(off is None and g.ev("SHIP.player.track") == job and g.ev("IX_GOAL") is None, 'a tap on your job switches its arrow off, another tracks it again')
        g.page.click('#devBtn'); g.step(2); g.ev(OPEN); g.step(2)
        hadDinner = tap('Dinner'); g.step(3)
        check(not hadDinner or (g.ev("IX_GOAL && IX_GOAL.deck") == 3 and 'Deck 3' in (st()['goal'] or '')), f'a meal tracks the mess ({st()["goal"]})')
        g.ev("deviceClose(); clearGoal()"); g.step(2)
        # FX5 (the user, 2026-10-23): the call booths' row points at a free booth and stays up in the room till the call begins (it went on walking in)
        keep = g.ev("JSON.stringify({ deck: deckDef.num, pos: [player.obj.position.x, player.obj.position.z] })")
        g.page.click('#devBtn'); g.step(2); g.ev(OPEN); g.step(2); tap('The call booths'); g.step(3)
        g.ev("(() => { goToDeck(3); player.obj.position.copy(cellPos(37, 12)); player.stop(); })()"); g.step(20)
        g.ev("(() => { player.obj.position.copy(cellPos(37, 15)); player.stop(); })()"); g.step(30)
        inroom = g.ev("({ trk: IX_GOAL && IX_GOAL.trk, place: IX_GOAL && IX_GOAL.place, room: roomAt(...player.here()) })")
        moved = g.ev("(() => { if (!IX_GOAL) return null; const was = IX_GOAL.place, x = { goalId: was }; DECK_CREW.push(x); trkDoneCheck(); const now = IX_GOAL.place; DECK_CREW.splice(DECK_CREW.indexOf(x), 1); IX_GOAL.place = was; return [was, now]; })()")
        # (RV10, 320 wide: someone at the booth under the pin took the tap as a chat) someone stands on the booth: a real tap at the pin is the booth
        g.ev("(() => { for (let k = 0; k < 9 && TIP_Q.length; k++) tipDone(); })()"); g.step(2)
        g.ev("(() => { player.obj.position.copy(cellPos(38, 19)); player.stop(); })()"); g.step(20)
        for rot in range(4):                               # a camera turn with them under the pin
            who = g.ev("(() => { const a = DECK_CREW.find(x => x && x.p), s = placeSpot(IX_GOAL.place); a.x = s.x; a.z = s.z; a.y = 0; a.path = []; a.settled = false; a.spot = null; return a.p.id; })()"); g.step(2)
            pin = g.ev("(() => { const el = document.getElementById('ixGoal'), m = el.style.transform.match(/translate\\(([-\\d.]+)px, ?([-\\d.]+)px\\)/); return !el.hidden && m && el.children[1].style.display !== 'none' ? [+m[1], +m[2]] : null; })()")
            over = pin and g.ev(f"(a => a && a.p && a.p.id)(crewAtScreen({pin[0]}, {pin[1]}))")
            if pin and over == who: break
            g.page.click('#rot'); g.step(30)
        if pin: g.page.mouse.click(*pin)
        for i in range(40):
            g.step(10)
            if g.ev("!!ACT && ACT.kind === 'call' && ACT.phase !== 'walk'"): break
        chat = g.ev("!!document.getElementById('chat') && !document.getElementById('chat').hidden"); g.ev("typeof chatClose === 'function' && chatClose()")
        check(pin and over == who and not chat and g.ev("!!ACT && ACT.kind === 'call'"), f"the call booths' row: with {who} on the booth under the pin, a real tap at the pin starts the call, not a chat (FX5) (pin {pin}, under it {over}, chat {chat}, act {g.ev('ACT && ACT.kind')})")
        g.step(5); after = g.ev("({ act: ACT && ACT.kind, trk: IX_GOAL && IX_GOAL.trk })")
        print('   the call booths\' row: in the room', inroom, '| booth taken, moved', moved, '| the call begun', after)
        check(inroom['trk'] == 'place:calls' and (inroom['place'] or '').startswith('3-callhome-') and inroom['room'] == 'B', f"the call booths' row: in the room its arrow stays up, on a booth (FX5) ({inroom})")
        check(moved and moved[0] != moved[1], f"the call booths' row: someone takes its booth, the arrow moves to a free one (FX5) ({moved})")
        check(after['act'] == 'call' and after['trk'] != 'place:calls', f"the call booths' row: once the call begins the arrow goes (FX5) ({after})")
        for k in range((4 - rot - (0 if pin and over == who else 1)) % 4): g.page.click('#rot'); g.step(5)   # the camera as it was
        g.ev("(() => { if (typeof DIALOGUE !== 'undefined' && DIALOGUE && typeof dialogueEnd === 'function') dialogueEnd(true); if (DEV.choose) devChosen(-1); })()"); g.step(2)   # the first call's own talk
        g.ev(f"(() => {{ actEnd(true); clearGoal(); const k = {keep}; if (deckDef.num !== k.deck) goToDeck(k.deck); player.obj.position.x = k.pos[0]; player.obj.position.z = k.pos[1]; player.stop(); }})()"); g.step(3)
        if g.ev("!!document.getElementById('trkBtn')"):   # the main-screen button and panel, kept beside the app (the user, ~04:00)
            g.page.add_style_tag(content='#needStrip{display:flex!important} #devTip{display:none!important}')   # a tip card over it would take the tap
            g.page.click('#trkBtn'); g.step(2)
            prow = g.ev("[...document.querySelectorAll('#trkList button b')].map(b => b.textContent)")
            check(g.ev("!document.getElementById('trkPanel').hidden") and 'Your bunk' in prow, f'the Tracked button opens its panel with the same list ({prow[-3:]})')
            g.page.click('#trkList button:has-text("Your bunk")'); g.step(3)
            check(g.ev("document.getElementById('trkPanel').hidden") and g.ev("IX_GOAL && IX_GOAL.trk") == 'place:bed', 'a tap in the panel tracks it and closes the panel')
            g.page.click('#trkBtn'); g.step(2); g.page.click('#trkList button:has-text("Your bunk")'); g.step(3)
            check(g.ev("IX_GOAL") is None and not g.ev("document.getElementById('trkPanel').hidden"), 'a second tap stops it, the panel stays')
            # a tap outside: (160, 620) unless the panel reaches it (a longer Tracked list with the rec traditions on, lead 19), else
            # the first point near it that lands on the scene itself, clear of the panel
            ox, oy = g.ev("""(() => { const r = document.getElementById('trkPanel').getBoundingClientRect(), H = innerHeight;
              const c = [[160, 620], [160, r.top - 30], [160, r.bottom + 30], [20, r.top - 30], [160, 200], [r.left / 2, H / 2], [(r.right + innerWidth) / 2, H / 2], [160, (r.bottom + H) / 2]].filter(([x, y]) => y > 0 && y < H);   // the last three: the margins round a panel that fills the screen
              const ok = ([x, y]) => { const e = document.elementFromPoint(x, y); return e && e.tagName === 'CANVAS' && !(x >= r.left && x <= r.right && y >= r.top && y <= r.bottom); };
              return c.find(ok) || [160, 620]; })()""")
            g.page.mouse.click(ox, oy); g.step(2)
            b = json.loads(g.ev("JSON.stringify(document.getElementById('trkBtn').getBoundingClientRect())"))
            hit = g.ev(f"[...document.querySelectorAll('.controls button,#devBtn,#needStrip')].filter(o => o.offsetWidth).map(o => o.getBoundingClientRect()).some(r => r.left < {b['right']} && {b['left']} < r.right && r.top < {b['bottom']} && {b['top']} < r.bottom)")
            check(g.ev("document.getElementById('trkPanel').hidden") and not hit and b['right'] <= 320, f'a tap outside closes it; the button clears the other HUD buttons on a 320 px phone ({b})')
        g.page.click('#devBtn'); g.step(3); g.ev("deviceShow('home')"); g.step(1)
        # the Schedule tracker's two words (the user's name for it, 0.92.3 #14) may take two lines, inside its tile; no other label wraps
        wrap = g.ev("[...document.querySelectorAll('.device .app span')].filter(e => (e.getClientRects().length > 1 || e.getBoundingClientRect().height > 24) && !(/^schedule tracker$/i.test(e.textContent.trim()) && e.getBoundingClientRect().height <= 40 && e.getBoundingClientRect().bottom <= e.closest('.app').getBoundingClientRect().bottom)).map(e => e.textContent)")
        check(g.ev("document.querySelectorAll('.device .app span').length") > 4 and not wrap, f'no device app label wraps at 320 px ({wrap})')
        if g.ev("typeof HOBBIES !== 'undefined' && !!HOBBIES.film"):   # Watch a film (0.72.1, the user's): a device hobby exactly like reading
            g.ev("deviceShow('hobbies')"); g.step(2)
            btns = g.ev("[...document.querySelectorAll('#devBody button')].map(b => b.textContent)")
            check('Watch a film' in btns, f'the Hobbies app has a Watch a film button ({btns})')
            g.ev("deviceClose(); actEnd && ACT && actEnd(true); player.stop()"); g.step(2)
            f = g.ev("(() => { SHIP.player.needs.leisure = 20; const ok = hobbyStart('film'); return { ok, kind: ACT && ACT.kind, hobby: ACT && ACT.o.hobby, pose: ACT && ACT.pose, readPose: HOBBIES.read.stand } })()")
            check(f['ok'] and f['kind'] == 'hobby' and f['hobby'] == 'film' and f['pose'] == f['readPose'], f'Watch a film starts standing, with reading\'s pose ({f})')
            g.step(30 * 60)                               # half an hour of play: plenty of ship minutes
            r = g.ev("({ leisure: Math.round(SHIP.player.needs.leisure), done: SHIP.player.hobbies.done.film || 0, act: ACT && ACT.kind })")
            check(r['done'] >= 1 and r['leisure'] > 20, f'it finishes, counts and fills Leisure ({r})')
            rt = g.ev("JSON.stringify(hobbiesLoad({ player: { hobbies: JSON.parse(JSON.stringify(SHIP.player.hobbies)) } }).done.film) + '|' + JSON.stringify(hobbiesLoad({ player: { hobbies: { has: [], done: { read: 2 }, last: {} } } }))")
            check(rt.split('|')[0] == str(r['done']) and '"done":{"read":2}' in rt, f'film counts save and load; an old save loads unchanged ({rt})')
        if g.ev("typeof turnInShow === 'function'"):   # the turn-in's gains (0.72.3, Step 3): chips for rep and each ship meter
            g.ev("deviceClose()"); g.step(1)
            r = g.ev("""(() => { if (myJob()) dropJob && dropJob(myJob().id); const o = openJobs('you'); if (!o.length || !claimJob(o[0].id)) return null; const j = myJob(); j.workDone = true;
              j.gains = { rep: [{ dept: 'works', add: 3 }], meters: [{ sys: 'power', add: 4 }, { sys: 'air', add: 2.4 }, { sys: 'heat', add: 0 }] };
              const ok = ixBoard.turnIn(j.id); return [ok, [...document.querySelectorAll('#tx .tgain b')].map(b => [b.textContent, b.className])]; })()""")
            nrep = 0 if r is None else len([1 for t, c in r[1] if c == 'rep'])   # FX3: your own reputation's chip may come first, then the Works team's standing
            check(r is None or (r[0] and len(r[1]) == 2 + nrep and nrep in (1, 2) and all(c == 'rep' for t, c in r[1][:nrep]) and ('reputation up' in r[1][0][0] or 'standing up' in r[1][0][0]) and not any(ch.isdigit() for t, c in r[1][:nrep] for ch in t) and any('4' in t and t.startswith('+') for t, c in r[1][nrep:]) and not any('Heat' in t for t, c in r[1])), f'the turn-in shows rep first (words only, the user\'s 0.61.15 rule), then +N for each meter the job raised (none for 0) ({r})')
            r = g.ev("""(() => { const o = openJobs('you'); if (!o.length || !claimJob(o[0].id)) return null; const j = myJob(); j.workDone = true;
              const a = turnInSnap(); a.sys.power -= 3; a.rep.works -= 2; return turnInGains(j, a).map(c => c.text); })()""")
            r2 = g.ev("""(() => turnInGains({ meters: [{ key: 'water', name: 'Water', gain: 3.4 }, { key: 'heat', name: 'Heat', gain: .2 }] }, null).map(c => c.text))()""")
            check(len(r2) == 1 and r2[0].startswith('+3') and 'Water' in r2[0], f"S2's j.meters (0.33.57) show as +N, under half a point left out ({r2})")
            d = g.ev("""(() => turnInGains({ gains: { rep: [{ dept: 'works' }, { dept: 'works', name: 'Works' }], meters: [{ sys: 'power', add: 4 }, { sys: 'power', add: 4 }] } }, null).map(c => c.text))()""")
            check(len(d) == 2, f'the same gain recorded twice (C2 and another section) shows once ({d})')
            check(r is None or (any('standing up' in t or 'reputation up' in t for t in r) and any('3' in t and t.startswith('+') for t in r)), f'with no j.gains, a before/after look fills it in ({r})')
        check(not g.errors, f'no console errors ({g.errors[:3]})')
    g.close()

# playtest 2 (HUD U, 0.72.5+): the first night's call-home arrow over the bunk arrow (item 3); Day 1's time clock arrow
# from 08:50 in the Works bay, then the job board's (6, 7); the training-day device tip and Day 2's laundry tip (9, 19);
# career warnings once a save like every other tip (17)
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844); g.step(3)
    if g.ev("typeof INTRO_CLOCK_AUTO !== 'undefined'"):
        print('== playtest 2')
        r = g.ev("""(() => { const I = SHIP.intro; I.on = true; I.ended = false; setShipNow(introAbs(0, 19 * 60));
          I.done['call:track'] = I.done['call:tip'] = Math.floor(shipNow()); delete I.done['call:end'];
          setGoal({ deck: 4, place: playerBed(), label: INTRO_BED_GOAL }); INTRO_UI.bed = true; INTRO_UI.arrowAt = 0;
          introArrowTick(); const out = [IX_GOAL && IX_GOAL.label]; I.done['call:end'] = Math.floor(shipNow()); clearGoal(); return out; })()""")
        check(r[0] == g.ev("INTRO_ARROWS.call.label"), f'"Track it" on the first night: the call-home arrow takes over from the bunk arrow ({r})')
        g.ev("goToDeck(5)"); g.step(5)
        r = g.ev("""(() => { const I = SHIP.intro; for (const k of ['told:clock','arrow:clock','arrow:board','d1-opener','d1-briefing:met']) delete I.done[k];
          const c = cellPos(...(() => { for (let j = 0; j < D; j++) for (let i = 0; i < W; i++) if (MAP[j][i] === 'w') return [i, j]; })()); player.obj.position.copy(c); player.stop();
          const tick = m => { setShipNow(introAbs(1, m)); INTRO_UI.arrowAt = 0; introArrowTick(); return IX_GOAL && IX_GOAL.label; };
          clearGoal(); const a = [tick(8 * 60 + 40), tick(8 * 60 + 51)]; careerClock(Math.floor(shipNow())); a.push(tick(8 * 60 + 52)); return a; })()""")
        check(r[0] is None and r[1] == 'Clock in at the time clock' and r[2] == 'Take a job at the job board', f'Day 1 in the Works bay: no arrow at 08:40, the time clock at 08:51, the job board once clocked in ({r})')
        r = g.ev("""(() => { const out = {}, D = SHIP.device; D.settings.tips = true; SHIP.intro.on = false; clearGoal();
          const run = (day, min) => { setShipNow((day - 1) * 1440 + min); POP.busy = false; POP.toast = POP.tip = POP.card = POP.warn = -1e9; TEACH_CK = -1e9; TIP_Q.length = 0; if (DEV.open) deviceClose(); return teachTick(performance.now() + 1e7); };
          for (const [id] of TEACH) D.tipsSeen[id] = true; delete D.tipsSeen['t:devwork']; delete D.tipsSeen['t:laund2'];
          // the patch (#13): the device tip waits for a long work step under way (a stand-in 40-minute job here)
          const longJob = f => { const old = ACT; ACT = { kind: 'job', def: { mins: 40 }, done: 5, phase: 'do', o: {} }; try { return f(); } finally { ACT = old; } };
          out.idle = run(1, 10 * 60); out.d1 = longJob(() => run(1, 10 * 60)); out.d2 = run(2, 6 * 60 + 30); out.again = [longJob(() => run(1, 11 * 60)), run(2, 7 * 60)];
          delete D.tipsSeen['career.late']; TIP_Q.length = 0; out.ct = [careerTip('late'), (TIP_Q.length = 0, careerTip('late')), !!D.tipsSeen['career.late']];
          return out; })()""")
        check(r['idle'] is None and r['d1'] == 't:devwork' and r['d2'] == 't:laund2' and r['again'] == [None, None], f'the device tip (only with a long job under way) and the Day 2 laundry tip, each once ({r})')
        check(r['ct'][0] is not False and r['ct'][1] is False and r['ct'][2], f'a career warning shows once a save, saved like the other tips ({r["ct"]})')
        if g.ev("typeof devDay === 'function' && typeof DECK_NAMES !== 'undefined'"):   # batch B (0.72.6): tea and the delivery on the Schedule, tea a little food, Deck 2's lift label
            r = g.ev("""(() => { const k = d => devDay(d).filter(x => x.kind === 'tea' || x.kind === 'delivery').map(x => x.title + ' ' + hhmm(x.from) + (devItemGoal(x) ? '' : ' (no goal)'));
              const wed = [1, 2, 3, 4, 5, 6, 7].find(d => weekday(d) === DELIVERY.day + deliveryLate(d)), sat = [1, 2, 3, 4, 5, 6, 7].find(d => !devShiftOn(d));
              const A = { def: { mins: 6 }, o: {}, kind: 'ixTea' }; teaBegin(A);
              return { wed: k(wed), sat: sat ? k(sat) : [], gain: A.def.gain, lift: DECK_NAMES[2] }; })()""")
            check(any(t.startswith('Supply delivery') for t in r['wed']) and any(t.startswith('Tea and biscuits') for t in r['wed']) and not any('no goal' in t for t in r['wed']) and r['sat'] == [], f'the Schedule lists tea on shift days and the week\'s delivery, each with an arrow; none on a day off ({r})')
            r2 = g.ev("""(() => { const t0 = (SHIP.time.day - 1) * 1440 + 19 * 60, P = DECKS[3].places.find(x => x.type === 'lounge-seat') || DECKS[3].places[0]; SHIP.device.calendarRemind.heard = []; HU_Q.length = 0;
              SHIP.device.appts.push({ id: 9999, with: ['tomas'], at: t0 + 30, len: 30, where: P.id, kind: 'invite', status: 'asked', by: 'tomas' });
              const at = m => { setShipNow(t0 + m); devTickMin = -1; deviceTick(); return HU_Q.filter(h => h.key === 'invite|9999').map(h => h.stage + (h.goal ? '+goal' : '')); };
              const out = [at(16), at(31)]; SHIP.device.appts = SHIP.device.appts.filter(a => a.id !== 9999); return out; })()""")
            check(r2 == [['soon+goal'], ['start+goal']], f'an invitation still waiting for your answer reminds you 15 minutes before and at its start (item 12) ({r2})')
            check(r['gain'] <= 5 and r['lift'] == "Officer's Quarters - Science", f'tea and biscuits is only a little food; the lift says Officer\'s Quarters - Science ({r["gain"]}, {r["lift"]})')
        if g.ev("typeof DEV_BEATS !== 'undefined'"):   # 0.73.2 (U2, item 12 a): the arrival week's beats on the Schedule, with heads-ups and an arrow
            r = g.ev("""(() => { const I = SHIP.intro, was = [I.on, I.ended]; I.on = true; I.ended = false; const out = [];
              for (const d of [1, 2, 3]) for (const x of devDay(d)) if (x.kind === 'beat') { const g = devItemGoal(x), rooms = Object.values((DECKS[x.deck] || {}).rooms || {}).map(r => r.name);
                out.push([d, hhmm(x.from), x.title, x.where, !!g && rooms.includes(x.room)]); }
              const R = SHIP.device.calendarRemind, on = R.on; R.on = false; R.heard = R.heard.filter(k => !/^beat\|/.test(k)); HU_Q.length = 0;
              const fl = SHIP.flags && SHIP.flags['intro.device']; flagSet('intro.device'); const b = INTRO_WEEK.find(x => x.id === 'd2-booths'); setShipNow(introAbs(2, b.at - 15)); devTickMin = -1; deviceTick(); if (!fl) delete SHIP.flags['intro.device'];
              const hu = HU_Q.filter(h => /^beat\|/.test(h.key)).map(h => h.title + ' ' + h.stage + (h.goal ? '+goal' : '')); HU_Q.length = 0; R.on = on;
              I.on = false; const off = devDay(2).filter(x => x.kind === 'beat').length; [I.on, I.ended] = was; return { out, hu, off }; })()""")
            print('  the arrival week\'s beats [day, time, title, where, goal found]:', r['out'], '| heads-up:', r['hu'], '| intro over:', r['off'])
            check(len(r['out']) == 4 and all(x[4] for x in r['out']) and r['off'] == 0, f'the briefing, the Chief\'s office, the booths and the store on the Schedule with a goal, only during the intro ({r})')
            check(r['hu'] == ['Calling home soon+goal'], f'a beat gets its 15-minute heads-up with the arrow, even with heads-ups off ({r["hu"]})')
        if g.ev("typeof roundGuide === 'function'"):   # 0.73.0 (U2, item 1): the first round's arrow and tips, on E1's roundTrainStep (a stand-in when it's missing)
            r = g.ev("""(() => { const D = SHIP.device, real = typeof roundTrainStep === 'function' ? roundTrainStep : null; D.settings.tips = true; careerInit(); const ci0 = SHIP.career.ci; SHIP.career.ci = Math.max(1, Math.floor(shipNow()));   /* clocked in (FX1: a round's arrow waits for that) */ TIP_Q.length = 0; DEVICE_SKIN.tip(null); clearGoal(); RG_LAST = ''; RG_N = 0;
              for (const k in D.tipsSeen) if (/^rg:/.test(k)) delete D.tipsSeen[k];
              const seq = [{ step: 'take' }, { step: 'take' }, { step: 'go', machine: 'Washer 2' }, { step: 'look', machine: 'Washer 2' }, { step: 'mark', machine: 'Washer 2' }, { step: 'next', machine: 'Light relays 1' }, { step: 'look', machine: 'Light relays 1' }, { step: 'done' }, null];
              const out = []; let k = 0; roundTrainStep = () => seq[k];   // the binding itself: with 24a's own function in the build, a window property doesn't replace it
              for (; k < seq.length; k++) { roundGuide(); out.push([IX_GOAL && IX_GOAL.label, TIP_Q.map(t => t.id).join(','), (TIP_Q[0] || {}).text || '']); }
              setGoal({ deck: 3, room: 'M', label: 'Someone else' }); RG_LAST = 'take|'; k = 0; roundGuide(); roundGuide(); const other = IX_GOAL && IX_GOAL.label; clearGoal();
              k = 2; RG_LAST = ''; RG_N = 0; roundGuide(); const again = TIP_Q.length; TIP_Q.length = 0; DEVICE_SKIN.tip(null);
              SHIP.career.ci = ci0; if (real) roundTrainStep = real; else delete window.roundTrainStep; return { out, other, again }; })()""")
            o = r['out']; print('  the first round, step by step [arrow, tips queued, tip]:'); [print('   ', x) for x in o]
            check(o[0][0] == 'Take your first round at the job board' and o[0][1] == 'rg:take:0' and o[1][1] == 'rg:take:0', f'take: the arrow to the job board and its tip, once ({o[:2]})')
            check(o[2][0] is None and o[2][1] == 'rg:go:0' and 'Washer 2' in o[2][2], f'go: the board arrow gives way to the job\'s, the tip names the machine and replaces the last ({o[2]})')
            check([x[1] for x in o[3:8]] == ['rg:look:0', 'rg:mark:0', 'rg:next:1', 'rg:look:1', 'rg:done:0'] and o[8][1] == '', f'look, mark, next, look, done: one tip at a time, gone once it is turned in ({[x[1] for x in o]})')
            check(r['other'] == 'Someone else', f'the board arrow is never put over another section\'s once the walk-through is under way ({r["other"]})')
            check(r['again'] == 0, f'each round tip shows once a save ({r["again"]})')
        check(not g.errors, f'no console errors ({g.errors[:3]})')
    g.close()

# the climbing wall with two faults at once (R7's note; RE20, 0.64.1): one auto-belay tagged out and the other belay's route
# taped means no turn can ever come, so a tap is refused (not queued), and a player already waiting when the second fault
# lands stops waiting with the same refusal. recShut is stood in for; the rec deck switched on only
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1])
    if g.ev("typeof REC_DECK !== 'undefined' && REC_DECK && typeof recQueue === 'function'"):
        print('== the climbing wall, both belays out of use')
        tap = lambda title, near=None, place=True: g.ev(f"({TAP})({json.dumps({'title': title, 'near': near, 'place': place})})")
        g.ev("skipTo(600)"); g.step(3); g.ev("goToDeck(7)"); g.step(3)
        g.ev("window.__recShut = recShut; recShut = () => ({ ...REC_OK, belays: 1, belayOff: [true, false], route: 2 })")   # belay 1 tagged out, belay 2's route (blue) taped
        g.ev("actEnd(true); REC.q = null"); tap('Climbing wall'); g.step(3)
        s = json.loads(g.ev(STATE)); q = g.ev("REC.q && REC.q.kind")
        print('   tap:', s['act'], q, s['toast'][:110])
        check(q is None and not (s['act'] and s['act'][0] in ('recWait', 'recClimb')), f"two faults: a wall tap is refused, not queued ({s['act']}, {q})")
        check('tagged out' in s['toast'] and 'taped off' in s['toast'], f"two faults: the refusal says why ({s['toast'][:110]})")
        # already waiting (belay 2 busy, belay 1 tagged out), then belay 2's route is taped
        g.ev("recShut = () => ({ ...REC_OK, belays: 1, belayOff: [true, false], route: null })")
        w = g.ev("(() => { const fake = { goalId: '7-climb-2' }; DECK_CREW.push(fake); const r = recQueue('climb', 'Climbing wall', null); DECK_CREW.splice(DECK_CREW.indexOf(fake), 1); return [r, ACT && ACT.kind, REC.q && REC.q.kind]; })()")
        check(w == [True, 'recWait', 'climb'], f'one belay busy, the other tagged out: you wait your turn ({w})')
        g.ev("recShut = () => ({ ...REC_OK, belays: 1, belayOff: [true, false], route: 2 })"); g.step(5)
        s = json.loads(g.ev(STATE)); q = g.ev("REC.q && REC.q.kind")
        print('   mid-wait:', s['act'], q, s['toast'][:110])
        check(q is None and not (s['act'] and s['act'][0] == 'recWait'), f"the second fault mid-wait: the wait ends ({s['act']}, {q})")
        check('tagged out' in s['toast'] and 'taped off' in s['toast'], f"the second fault mid-wait: the refusal says why ({s['toast'][:110]})")
        g.ev("recShut = window.__recShut")
        check(not g.errors, f'no console errors ({g.errors[:3]})')
    else:
        print('== the climbing wall: the rec deck is off in this build, skipped')
    # the sim bay (FX14, rec-simbay S3; behind SIM_BAY, so only on a build or copy with it on): a pod tap walks you in and
    # sits you down for a 15-minute run with its screen playing, leisure up about 20 and no score; both pods taken, you
    # wait on the bench and get in when one frees up
    if g.ev("typeof SIM_BAY !== 'undefined' && SIM_BAY"):
        print('== the sim bay: a run in a pod, and waiting for one')
        tap = lambda title, near=None, place=True: g.ev(f"({TAP})({json.dumps({'title': title, 'near': near, 'place': place})})")
        g.ev("skipTo(19 * 60)"); g.step(3); g.ev("goToDeck(7); actEnd(true); REC.q = null"); g.step(3)
        l0 = g.ev("SHIP.player.needs.leisure"); tap('Sim pod'); g.step(240)
        s = json.loads(g.ev(STATE)); run = g.ev("Math.max(simRunAt(0), simRunAt(1))")
        print('   in the pod:', s['act'], round(run, 2))
        check(s['act'] and s['act'][0] == 'recSim' and s['act'][1] in ('7-sim-1', '7-sim-2') and s['act'][2] == 'do' and s['act'][3] == 'sit', f"a pod tap: you sit in a pod ({s['act']})")
        check(0 < run < 1, f'its screen plays the run ({run})')
        for _ in range(12):
            if not g.ev("ACT && ACT.kind === 'recSim'"): break
            g.step(150)
        l1 = g.ev("SHIP.player.needs.leisure"); s = json.loads(g.ev(STATE))
        print('   after:', s['act'], round(l0, 1), '->', round(l1, 1), s['toast'][:90])
        check(not (s['act'] and s['act'][0] == 'recSim'), f"the run ends by itself ({s['act']})")
        check(14 <= l1 - l0 <= 24 or l1 >= 99, f'leisure up about 20 ({l0:.1f} -> {l1:.1f})')
        check(g.ev("SIM_POD_IDS.every((id, k) => simRunAt(k) === -1 || !!heldBy(id))"), 'the screens go back to drifting stars (unless one of the crew is flying)')   # the crew's sim pilots (S5) fly too
        w = g.ev("(() => { const fakes = SIM_POD_IDS.map(id => ({ goalId: id, x: -999, z: -999, path: [] })); DECK_CREW.push(...fakes); actEnd(true); REC.q = null; const r = recQueue('sim', 'Sim pod', null); const a = [r, ACT && ACT.kind, ACT && ACT.placeId, REC.q && REC.q.kind]; for (const f of fakes) DECK_CREW.splice(DECK_CREW.indexOf(f), 1); return a; })()")
        check(w[0] is True and w[1] == 'recWait' and (w[2] or '').startswith('7-simq-') and w[3] == 'sim', f'both pods taken: you wait on the bench ({w})')
        g.step(60); s = json.loads(g.ev(STATE))   # (the stand-ins leave in the same breath: they aren't real crew to step)
        print('   the pods free up:', s['act'])
        check(s['act'] and s['act'][0] == 'recSim', f"a pod frees up: you're up, in it ({s['act']})")
        g.ev("actEnd(true); REC.q = null")
        # the pods are machines (S4): one tagged out, a tap takes the other; both, a tap is refused and says why
        g.ev("window.__simShut = simPodsShut; simPodsShut = () => [true, false]"); tap('Sim pod', [29, 13]); g.step(30)
        s = json.loads(g.ev(STATE)); busy = g.ev("!!heldBy('7-sim-2')"); print('   pod 1 tagged out:', s['act'], 'pod 2 in use by the crew' if busy else '')
        check(s['act'] and (s['act'][0] == 'recSim' and s['act'][1] == '7-sim-2' or busy and s['act'][0] == 'recWait'), f"one pod tagged out: you get the other, or wait for it while one of the crew flies it ({s['act']}, {busy})")
        g.ev("actEnd(true); REC.q = null; simPodsShut = () => [true, true]"); tap('Sim pod'); g.step(5)
        s = json.loads(g.ev(STATE)); print('   both tagged out:', s['act'], s['toast'][:90])
        check(not (s['act'] and s['act'][0] in ('recSim', 'recWait')) and 'tagged out' in s['toast'], f"both tagged out: refused, and says why ({s['act']}, {s['toast'][:90]})")
        g.ev("simPodsShut = window.__simShut")
        m = g.ev("JSON.stringify(machineList().filter(m => m.kind === 'simpod').map(m => [m.id, m.at, m.panel, !!panelPlace(m.id)]))")
        print('   the pods as machines:', m)
        check(len(json.loads(m)) == 2 and all(x[3] for x in json.loads(m)), f'two pod machines, each with its panel place ({m})')
        # the crew's sim pilots (S5; RV13's ask), on paper: over days 1-6 Dev Raman and at least one other pilot have turns in
        # the pods; with pod 1 tagged out the evening before (simPlanShut stood in for, every day planned again) no plan puts
        # anyone in pod 1, and pod 2 is still flown
        PILOTS = "JSON.stringify((() => { const out = {}; for (let d = 1; d <= 6; d++) for (const p of schedPeople()) for (const s of planDay(p, d)) if (/^7-sim-[12]$/.test(s.placeId || '')) (out[s.placeId] = out[s.placeId] || []).push(p.id); return out; })())"
        REPLAN = "SCHED_DATA = null; SHIP_DAYS.clear(); EV_DAYS.clear()"
        u = json.loads(g.ev(PILOTS)); who = sorted(set(sum(u.values(), [])))
        print('   pilots in the pods, days 1-6:', {k: len(v) for k, v in u.items()}, who)
        check('raman' in who and len(who) >= 2, f'the crew fly the pods: Dev Raman and at least one other pilot ({who})')
        g.ev("window.__simPS = simPlanShut; simPlanShut = d => [true, false]; " + REPLAN)
        u2 = json.loads(g.ev(PILOTS)); print('   pod 1 tagged out each evening before:', {k: len(v) for k, v in u2.items()})
        check('7-sim-1' not in u2 and len(u2.get('7-sim-2', [])) > 0, f'a pod tagged out the evening before is never planned; the other still is ({ {k: len(v) for k, v in u2.items()} })')
        g.ev("simPlanShut = window.__simPS; " + REPLAN)
        g.ev("actEnd(true); REC.q = null")
        check(not g.errors, f'no console errors ({g.errors[:3]})')
    # playtest 1, notes 9-11, on paper: no job on a shift day, the arrow shows the time clock, then (clocked in) the job
    # board, and nothing after the shift; a tracked tea points at the tea table, not the room's middle; tracking
    # something else over your job, then done with it, tracking goes back to your job
    if g.ev("typeof ixWorkStep === 'function'"):
        print('== the arrow with no job, tea, back to the job (playtest 1, notes 9-11)')
        g.ev("goToDeck(5)"); g.step(3)
        r = g.ev("""(() => { const o = {}, P = SHIP.player; careerInit(); const C = SHIP.career, ci0 = C.ci;
          for (const j of SHIP.jobs) if (j.claimedBy === 'you' && j.status === 'claimed') { j.claimedBy = null; j.status = 'open'; }
          let d = 2; while (!playerShiftOn(d)) d++; setShipNow((d - 1) * 1440 + 600); P.track = undefined; clearGoal();
          C.ci = 0; o.clock = (ixWorkStep() || {}).label;
          C.ci = (d - 1) * 1440 + 560; o.open = openJobs('you').length; o.board = (ixWorkStep() || {}).label;
          setShipNow((d - 1) * 1440 + dayShiftEnd(d) + 30); o.after = ixWorkStep(); C.ci = ci0;
          const tg = devItemGoal({ kind: 'tea' }), w = ixGoalWorld(tg), mid = ixGoalWorld({ deck: 5, room: 't' }), it = ITEMS.find(i => i.t === 'Tea table');
          const ip = it && it.hit.getWorldPosition(new THREE.Vector3());
          o.table = !!(w && ip && Math.hypot(w.x - ip.x, w.z - ip.z) < .05); o.notMid = !!(w && mid && Math.hypot(w.x - mid.x, w.z - mid.z) > .3);
          const x = trkItems().find(q => !q.job && q.goal); P.track = undefined;
          if (x) { trkTap(x.key); o.tapped = [P.track === undefined, !!IX_GOAL];   /* FX1: tracking stays on under it */ trkDone(IX_GOAL); o.back = [P.track === undefined, IX_GOAL === null]; }
          P.track = null; setGoal({ ...tg, trk: 'tea' }); trkDone(IX_GOAL); o.off = P.track === null;   // tracking was off before: it stays off
          P.track = undefined; clearGoal();
          return o; })()""")
        print('  ', r)
        check(r['clock'] == 'Clock in at the time clock' and r['board'] == ('Take a job at the job board' if r['open'] else None) and r['after'] is None, f'no job: the clock, then the board (while it has a job for you), nothing once the shift is over ({r})')
        check(r['table'] and r['notMid'], f'a tracked tea points at the tea table ({r})')
        check(r.get('tapped') == [True, True] and r.get('back') == [True, True] and r['off'], f'tracking goes back to your job when the other thing is done ({r})')
    g.close()

# the toilets (TQ1, the user's playtest note 19): you can use a toilet unless its red light is on (someone's in it), never
# blocked by crew only heading for it; with every light on you join the washroom's line and go in when one comes free.
# The crew: a wait for a toilet is spent in the washroom's line (tag 'toiletq'), they go in in turn, nobody shares a
# place or gets stuck; and when you take the toilet someone is about to use, they take another or wait, never in yours
TQ_SIM = r"""(({ day, deck, m0, m1, who, you }) => {
  const B = (day - 1) * 1440, step = .05, out = { line: false, went: false, inYours: false, shared: 0, stuck: 0, alt: null, left: 0 };
  setShipNow(B + m0); goToDeck(deck); if (typeof ACT !== 'undefined' && ACT) actEnd(true);
  for (let k = 0; B + m0 + k * step * SHIP_RATE < B + m1; k++) {
    const now = B + m0 + k * step * SHIP_RATE; setShipNow(now);
    if (you && !you.on && now >= B + you.at) { you.on = true; actStart('toilet', you.id, { pose: 'sit', title: 'Toilet' }); }
    if (you && you.on && !you.off && now >= B + you.end) { you.off = true; actEnd(true); }
    updateDeckCrew(step);
    const held = new Map();
    for (const a of DECK_CREW) { if (a.settled && a.spot) { if (held.has(a.spot.id)) out.shared++; held.set(a.spot.id, a.p.id); } out.stuck = Math.max(out.stuck, a.stuckMax); }
    const a = DECK_CREW.find(x => x.p.id === who.id); if (!a) continue;
    if (QUEUE_SPOT.get(who.id)) out.line = true;
    if (a.settled && a.spot && PLACE_OF.get(a.spot.id) && PLACE_OF.get(a.spot.id).type === 'toilet') { out.went = true; if (a.spot.id !== who.toilet) out.alt = a.spot.id; }
    if (a.settled && a.spot && you && you.on && !you.off && a.spot.id === you.id) out.inYours = true;
  }
  out.left = [...QUEUE_NOW.values()].reduce((n, L) => n + L.length, 0); return out; })"""
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1]); g.step(3)
    if g.ev("typeof QUEUE_TAGS !== 'undefined' && !!QUEUE_TAGS.toiletq"):
        print('== the toilets: the red light and the line (note 19)')
        tap = lambda title, near=None, place=True: g.ev(f"({TAP})({json.dumps({'title': title, 'near': near, 'place': place})})")
        g.ev("skipTo(600)"); g.step(3); g.ev("goToDeck(3)"); g.step(3); g.ev("actEnd(true)")
        r = g.ev("""(() => { const T = [...PLACE_OF.values()].filter(q => q.type === 'toilet' && !privatePlace(q)), far = T.map(q => ({ goalId: q.id, p: { id: 'far-' + q.id, name: 'Someone' } }));
          DECK_CREW.push(...far); let r; try { r = (%s)({ title: 'Toilet' }); } finally { for (const f of far) DECK_CREW.splice(DECK_CREW.indexOf(f), 1); }
          return [r, ACT && ACT.kind, ACT && ACT.placeId, T.length, document.getElementById('tx').textContent]; })()""" % TAP)
        print('   every toilet only heading-for by crew far off, tap:', r)
        check(r[0] is True and r[1] == 'toilet' and r[2] and r[2].startswith('3-toilet'), f'a toilet crew are only heading for (light off) is yours: no "Occupied" ({r})')
        g.ev("actEnd(true)"); g.step(2)
        r = g.ev("""(() => { const T = [...PLACE_OF.values()].filter(q => q.type === 'toilet' && !privatePlace(q)); for (const q of T) BUSY.add(q.id);
          const r = (%s)({ title: 'Toilet' }); const lit = (stallCapsTick(), STALL_CAP.list.filter(c => c.id && placeBusy(c.id)).length);
          return [r, ACT && ACT.kind, QUEUE_YOU && QUEUE_YOU.type, document.getElementById('tx').textContent, lit]; })()""" % TAP)
        print('   every red light on, tap:', r)
        check(r[0] is True and r[1] != 'toilet' and r[2] == 'toilet' and 'line' in r[3], f'every red light on: no toilet, you join the washroom\'s line ({r})')
        check(r[4] > 0, f'the stalls of the toilets in use have their red light on ({r[4]})')
        for k in range(40):
            g.step(5)
            if g.ev("!!ACT && ACT.kind === 'toilet'"): break
        r = g.ev("[ACT && ACT.kind, ACT && ACT.placeId, QUEUE_YOU && QUEUE_YOU.type]")
        print('   the lights off again:', r)
        check(r[0] == 'toilet' and r[2] is None, f'a light goes off: out of the line and into that toilet ({r})')
        g.ev("actEnd(true)"); g.step(2)
        # the crew's line, from the plans: the first planned wait for a toilet on Deck 3 or 4 in the first week, not straight off the lift (a walk from the lift can take longer than the visit)
        q = g.ev("""(() => { for (let d = 1; d <= 7; d++) for (const p of schedPeople()) { const S = planDay(p, d);
            for (let i = 1; i + 1 < S.length; i++) if (S[i].tag === 'toiletq' && [3, 4].includes(S[i].deck) && S[i + 1].placeId && S[i - 1].act !== 'commute' && S[i - 1].deck === S[i].deck) return { day: d, deck: S[i].deck, id: p.id, from: S[i].from - (d - 1) * 1440, at: S[i + 1].from - (d - 1) * 1440, to: S[i + 1].to - (d - 1) * 1440, toilet: S[i + 1].placeId }; }
          return null; })()""")
        n = g.ev("(() => { let n = 0; for (let d = 1; d <= 7; d++) for (const p of schedPeople()) n += planDay(p, d).filter(s => s.tag === 'toiletq').length; return n; })()")
        print('   planned waits for a toilet in week 1:', n, '| first on Deck 3 or 4:', q)
        check(n > 0 and q, f'the crew plan waits for a toilet in the washroom\'s line ({n}, {q})')
        if q:
            w = {'id': q['id'], 'toilet': q['toilet']}
            r = g.ev(f"({TQ_SIM})({json.dumps({'day': q['day'], 'deck': q['deck'], 'm0': q['from'] - 15, 'm1': q['to'] + 3, 'who': w})})")
            print(f"   {q['id']}, the line from {q['from'] // 60:02d}:{q['from'] % 60:02d}:", r)
            check(r['line'] and r['went'] and r['shared'] == 0 and r['stuck'] < 1 and r['left'] == 0, f'the line forms, they go in in turn, nobody shares a place or gets stuck, and it clears ({r})')
            r = g.ev(f"({TQ_SIM})({json.dumps({'day': q['day'], 'deck': q['deck'], 'm0': q['from'] - 15, 'm1': q['to'] + 3, 'who': w, 'you': {'id': q['toilet'], 'at': q['at'] - 1, 'end': q['at'] + 3}})})")
            print(f"   you take {q['toilet']} first:", r)
            check(not r['inYours'] and r['shared'] == 0 and r['stuck'] < 1 and (r['alt'] or r['line']), f'you took theirs first: they take another or wait in the line, never in yours ({r})')
        g.ev("actEnd(true)")
        check(not g.errors, f'no console errors ({g.errors[:3]})')
    else:
        print('== the toilets: no toilet line in this build, skipped')
    g.close()

# Tracked (fresh-eyes batch 2, 2026-10-22): (24) a row for tomorrow morning can't be followed yet: its tap sets no arrow
# and the row says "That's tomorrow" (the panel and the device app); a row for today still sets its arrow; (41) the row
# the arrow follows is highlighted, also for an arrow set without a Tracked tap; (38) the pin on the job board takes a tap
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844); g.step(3)
    print('== Tracked: a row for tomorrow (fresh-eyes 24)')
    g.ev("skipTo(1440 + 18 * 60)"); g.step(3)
    r = g.ev("""(() => { clearGoal(); const o = {}, its = trkItems(), t = its.find(x => x.sec === 'on' && /^Tomorrow/.test(x.sub) && x.goal), n = its.find(x => x.sec === 'on' && !/^Tomorrow/.test(x.sub) && x.goal);
      o.has = [!!t, !!n]; if (!t) return o;
      o.tap = trkTap(t.key); o.goal = !!IX_GOAL; o.panelSub = (trkOpen(), [...trkList.querySelectorAll('button')].find(b => b.textContent.includes(t.title)).textContent);
      trkClose(); deviceShow('tracked'); o.appSub = document.getElementById('devBody').textContent.includes("That's tomorrow"); deviceClose();
      if (n) { o.todayTap = trkTap(n.key); o.todayGoal = !!(IX_GOAL && IX_GOAL.trk === n.key); clearGoal(); }
      return o; })()""")
    print('  ', r)
    if check(r['has'][0], f'Tracked: a row for tomorrow to test ({r})'):
        check(r['tap'] is False and r['goal'] is False, f'Tracked: a tomorrow row sets no arrow ({r})')
        check("That's tomorrow" in r['panelSub'] and r['appSub'], f'Tracked: the row says That\'s tomorrow, in the panel and the app ({r})')
        if r['has'][1]: check(r['todayTap'] is True and r['todayGoal'] is True, f'Tracked: a row for today still sets its arrow ({r})')
    # (41) the row the arrow is following is highlighted, also when the arrow was set without a Tracked tap
    print('== Tracked: the row the arrow follows (fresh-eyes 41)')
    r = g.ev("""(() => { const o = {}, P = SHIP.player, t0 = P.track; P.track = null; clearGoal();
      const lit = () => { trkOpen(); const b = [...trkList.querySelectorAll('button.goal')].map(x => x.textContent); trkClose(); return b; };
      o.none = lit();
      setGoal({ deck: 5, item: /job board/i, room: 'w', label: 'Take your first round at the job board' });   // as the round guide sets it
      o.lit = lit(); deviceShow('tracked'); o.app = document.getElementById('devBody').textContent.includes('The Works bay, Deck 5 · The arrow points here'); deviceClose();
      clearGoal(); const k = trkItems().find(x => x.key === 'place:board'); trkTap(k.key); o.tracked = lit(); clearGoal(); P.track = t0;
      return o; })()""")
    print('  ', r)
    check(r['none'] == [], f'Tracked: no arrow, no row highlighted ({r})')
    check(len(r['lit']) == 1 and 'The job board' in r['lit'][0] and r['lit'][0].endswith('Arrow') and r['app'], f'Tracked: the job board row is highlighted for an arrow set elsewhere ({r})')
    check(len(r['tracked']) == 1 and r['tracked'][0].endswith('Tracking'), f'Tracked: a tracked row still says Tracking ({r})')
    # (38) "Turn it in at the job board": the pin sits on the board (its middle, not 1.2 m up, on the floor when the board's
    # wall is cut away) and a real tap on it walks you up and opens the board, 10 taps in every camera turn where it shows;
    # a goal on a place gives no tappable pin
    print('== the pin on the job board (fresh-eyes 38)')
    g.ev("goToDeck(5)"); g.step(3)
    g.ev("(() => { const it = ITEMS.find(i => /job board/i.test(i.t)), p = it.hit.getWorldPosition(new THREE.Vector3()); player.stop(); player.obj.position.set(p.x + 1.5, 0, p.z + 4); target.copy(player.obj.position).setY(.7); clearGoal(); setGoal({ deck: 5, item: /job board/i, room: 'w', label: 'Turn it in at the job board' }); azT = az = Math.PI / 4 + Math.PI; })()")
    g.step(20)
    pin = g.ev("""(() => { const el = document.getElementById('ixGoal'), p = el.children[1], r = p.getBoundingClientRect(), it = ITEMS.find(i => /job board/i.test(i.t)), b = new THREE.Box3().setFromObject(it.hit), v = b.getCenter(new THREE.Vector3()).project(camera);
      return { shown: !el.hidden && p.style.display !== 'none', tap: el.classList.contains('tap'), x: r.left + r.width / 2, y: r.top + r.height / 2, bx: (v.x + 1) / 2 * innerWidth, by: (1 - v.y) / 2 * innerHeight }; })()""")
    print('  ', pin)
    if check(pin['shown'], f'the pin shows over the job board ({pin})'):
        check(abs(pin['x'] - pin['bx']) < 3 and abs(pin['by'] - pin['y'] - 19) < 4, f'the pin points at the board\'s middle ({pin})')
    # every camera turn where the pin is on screen, 10 taps each: pressed, a few frames of the pin bobbing, released (RV8:
    # a tap acting on 'click' was lost 1 in 9 when the pin moved between press and release); each opens the board
    PUT = "(() => { const it = ITEMS.find(i => /job board/i.test(i.t)), p = it.hit.getWorldPosition(new THREE.Vector3()); document.getElementById('ixBoard').hidden = true; player.stop(); player.obj.position.set(p.x + .5, 0, p.z + 1.6); target.copy(player.obj.position).setY(.7); })()"
    PIN = "(() => { const el = document.getElementById('ixGoal'), p = el.children[1], r = p.getBoundingClientRect(); return { tap: !el.hidden && el.classList.contains('tap') && p.style.display !== 'none', x: r.left + r.width / 2, y: r.top + r.height / 2 }; })()"
    turns, taps, missed = 0, 0, []
    for t in range(4):
        g.ev(f"azT = az = Math.PI / 4 + {t} * Math.PI / 2"); g.ev(PUT); g.step(20)
        if not g.ev(PIN)['tap']: continue
        turns += 1
        for n in range(10):
            g.ev(PUT); g.step(4); q = g.ev(PIN)
            if not q['tap']: missed.append((t, n, 'no pin')); continue
            g.page.mouse.move(q['x'], q['y']); g.page.mouse.down(); g.step(3); g.page.mouse.up(); taps += 1; opened = False
            for _ in range(30):
                g.step(6)
                if g.ev("!document.getElementById('ixBoard').hidden"): opened = True; break
            if not opened: missed.append((t, n))
    print(f'   the pin: {turns} camera turns with it on screen, {taps} taps, missed {missed}')
    check(turns >= 1 and taps >= 10 and not missed, f'every tap on the pin opens the job board ({turns} turns, {taps} taps, missed {missed})')
    g.ev("document.getElementById('ixBoard').hidden = true"); g.step(2)
    g.ev("clearGoal(); setGoal({ deck: 5, place: playerBed(), room: 'w', label: 'Somewhere' })"); g.step(3)
    check(not g.ev("document.getElementById('ixGoal').classList.contains('tap')"), 'a goal on a place gives no tappable pin')
    g.ev("clearGoal()")
    check(not g.errors, f'no console errors ({g.errors[:3]})')
# a tap on the floor by a place (section 15's playerFloorTap: gym kit, booths, shelves, toilets) hands the taps a stand-in
# with no hit box; ixTap measured from that box and threw at the Deck 3 exercise bikes ("reading 'updateWorldMatrix'",
# 0.92.0's trial, FX7): on every deck no floor tap throws, and the one by a bike starts the gym on that bike
FLOOR_TAPS = r"""(() => { const out = { n: 0, bad: [], bike: null };
  for (const pl of PLACE_OF.values()) { if (!FLOOR_ACTS[pl.type]) continue; const sp = placeSpot(pl.id); if (!sp) continue;
    const it = { t: FLOOR_ACTS[pl.type](pl), x: '', front: 0, depth: 0 }, at = new THREE.Vector3(sp.x, 0, sp.z); out.n++;
    try { actEnd(true); playerTap(it, at, at); if (/bike/i.test(it.t) && !out.bike) out.bike = [pl.id, ACT && ACT.kind, ACT && ACT.placeId]; } catch (e) { out.bad.push(pl.id + ': ' + e.message); }
    actEnd(true); }
  return out; })()"""
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1]); g.step(3)
    print('== a floor tap by every place, every deck')
    if g.ev("typeof FLOOR_ACTS !== 'undefined' && typeof playerTap === 'function'"):
        bikes = None
        for d in (1, 2, 3, 4, 5, 7):
            g.ev(f"goToDeck({d})"); g.step(3)
            r = g.ev(FLOOR_TAPS)
            check(not r['bad'], f'Deck {d}: no floor tap by a place throws ({r["n"]} places: {r["bad"][:3]})')
            if r['bike']: bikes = r['bike']
        check(bikes and bikes[1] == 'gym' and bikes[2] == bikes[0], f'a floor tap by an exercise bike starts the gym on that bike ({bikes})')
        check(not g.errors, f'no console errors ({g.errors[:3]})')
    g.close()

# LEAD31-1 (0.92.1): real taps at phone size by the Deck 3 gym's two exercise bikes, in all four camera turns: on the floor at
# each bike and 0.3 m out on the three sides away from the other bike, each starts that bike (before: a floor tap took the
# place the tap's line passed nearest at any height, and only bike 16 had a tap box, so taps by bike 17 started bike 16 or
# nothing). At 03:00, with nobody in the gym (a tap by someone is a word with them, as designed)
BIKE_AT = r"""((pid, dx, dz) => { const s = placeSpot(pid), v = new THREE.Vector3(s.x + dx, .02, s.z + dz).project(camera); return [(v.x + 1) / 2 * innerWidth, (1 - v.y) / 2 * innerHeight]; })"""
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844); g.step(3)
    print('== real taps by the exercise bikes, four camera turns')
    home = g.ev("""(() => { goToDeck(3); setShipNow((SHIP.time.day - 1) * 1440 + 3 * 60); if (typeof GUIDE_ON !== 'undefined' && GUIDE_ON) { GUIDE.tq.length = 0; guideToast = () => false; }
      const s = placeSpot('3-gym-17'); if (!s || !placeSpot('3-gym-16')) return null; const c = nearestOpen(s.x + 1.5, s.z + 1.5, player); window.__home = cellPos(...c); player.obj.position.copy(__home); player.stop();
      return Math.sign(placeSpot('3-gym-17').x - placeSpot('3-gym-16').x) || 1; })()""")
    if home is None: print('   no exercise bikes in this build, skipped')
    else:
        g.step(60); res, bad = [], []
        for turn in range(4):
            for pid, away in (('3-gym-16', -home), ('3-gym-17', home)):
                for dx, dz in ((0, 0), (.3 * away, 0), (0, .3), (0, -.3)):
                    g.ev("actEnd(true); player.obj.position.copy(__home); player.stop()"); g.step(30)
                    x, y = g.ev(f"({BIKE_AT})('{pid}', {dx}, {dz})")
                    if 0 <= x <= 390 and 0 <= y <= 844: g.page.mouse.click(x, y); g.step(90)
                    a = g.ev("ACT && [ACT.kind, ACT.placeId]")
                    res.append(bool(a and a[1] == pid))
                    if not (a and a[1] == pid): bad.append([turn, pid, (round(dx, 1), dz), a])
            g.ev("actEnd(true)"); g.page.click('#rot'); g.step(80)
        print(f'   {sum(res)} of {len(res)} taps started the bike tapped')
        check(not bad, f'a real tap by an exercise bike, any camera turn, starts that bike ({bad[:4]})')
        check(not g.errors, f'no console errors ({g.errors[:3]})')
    g.close()

# LEAD31-9 (0.92.2, FE2's items 35 and 38): real taps in the mess at Day 1's dinner. (1) A tray, a seat, then one more tap
# on the same seat mid-meal: the meal goes on (it ended it, the tray already eaten into, and sat you down with nothing);
# with the needs list open, a tap on the deck only closes it; walking away mid-meal leaves the tray, and you're told
# (the user, 0.92.4: "the tray goes away when you get up from the table"; 0.92.2 kept the rest on it). (2) A tap on the servery counter beside the galley staff or the line, not on them, joins the queue
# (it opened their card), in any camera turn; a tap on a person still talks to them
MESS_SCR = r"""((x, y, z) => { const v = new THREE.Vector3(x, y, z).project(camera); return [(v.x + 1) / 2 * innerWidth, (1 - v.y) / 2 * innerHeight]; })"""
MESS_ST = "[ACT && ACT.kind, ACT && ACT.placeId, ACT && ACT.phase, SHIP.player.tray, SHIP.player.needs.hunger, document.getElementById('tx').textContent]"
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844); g.step(3)
    print('== the mess at dinner: a second tap mid-meal, the counter beside the staff (real taps)')
    if g.ev("typeof GUIDE_ON !== 'undefined' && GUIDE_ON"): g.ev("GUIDE.tq.length = 0; guideToast = () => false")
    g.ev("goToDeck(3); setShipNow(18 * 60 + 50); SHIP.player.needs.hunger = 5; for (const t of ITEMS) if (t.t === 'Servery') { window.__sv = t; break; }"); g.step(60)
    sv = g.ev("(() => { __sv.hit.getWorldPosition(_wp); const c = nearestOpen(_wp.x - 3, _wp.z, player); player.obj.position.copy(cellPos(...c)); player.stop(); return [_wp.x, _wp.y + .3, _wp.z]; })()"); g.step(30)
    x, y = g.ev(f"({MESS_SCR})({sv[0]}, {sv[1]}, {sv[2]})"); g.page.mouse.click(x, y)
    tray = False
    for k in range(80):
        g.step(30)
        if g.ev("!!SHIP.player.tray"): tray = True; break
    seat = g.ev(f"""(() => {{ const pp = player.obj.position, scr = {MESS_SCR};
      const c = [...PLACE_OF.values()].filter(p => p.room === 'M' && p.pose === 'sit' && SIT_TYPES.has(p.type) && !heldBy(p.id)).map(p => [p, placeSpot(p.id)]).filter(x => x[1])
        .sort((a, b) => Math.hypot(a[1].x - pp.x, a[1].z - pp.z) - Math.hypot(b[1].x - pp.x, b[1].z - pp.z))
        .find(([p, s]) => {{ const q = scr(s.x, s.y, s.z); const el = document.elementFromPoint(q[0], q[1]); return q[0] > 20 && q[0] < 370 && q[1] > 200 && q[1] < 800 && !crewAtScreen(q[0], q[1]) && el && el.tagName === 'CANVAS'; }});
      return c && [c[0].id, c[1].x, c[1].y, c[1].z]; }})()""")
    check(tray and seat, f'the servery hands you a tray and there is a free seat to tap ({tray}, {seat})')
    if tray and seat:
        x, y = g.ev(f"({MESS_SCR})({seat[1]}, {seat[2]}, {seat[3]})"); g.page.mouse.click(x, y)
        for k in range(40):
            g.step(30)
            if g.ev("!!(ACT && ACT.kind === 'eat' && ACT.phase === 'do')"): break
        g.step(60); f0 = g.ev("SHIP.player.needs.hunger")
        x, y = g.ev(f"({MESS_SCR})({seat[1]}, {seat[2]}, {seat[3]})"); g.page.mouse.click(x, y); g.step(4)
        s1 = g.ev(MESS_ST)
        check(s1[0] == 'eat' and s1[1] == seat[0] and 'still eating' in s1[5], f'one more tap on your seat mid-meal: you keep eating ({s1[:3]}, {s1[5][:70]})')
        # the needs list open (tap the strip for names and numbers): a tap on the deck closes it and nothing else
        g.ev("document.getElementById('needStrip').classList.add('open')"); g.page.mouse.click(x, y); g.step(4)
        sb = g.ev("[document.getElementById('needStrip').classList.contains('open'), ACT && ACT.kind, ACT && ACT.placeId]")
        check(not sb[0] and sb[1] == 'eat' and sb[2] == seat[0], f'with the needs list open, a tap on the deck only closes it: the meal goes on ({sb})')
        # walking away mid-meal: the tray goes, and you're told (the user's rule, 0.92.4); your seat then only sits you
        g.step(150)
        w = g.ev("(() => { const s = placeSpot(ACT.placeId), c = nearestOpen(s.x + 3, s.z + 2, player); playerGo(c); return c; })()"); g.step(20)
        sw = g.ev(MESS_ST)
        check(sw[0] != 'eat' and not sw[3] and 'leave your tray' in sw[5], f'walking away mid-meal: the tray goes, and you\'re told ({sw[0]}, {sw[3]}, {sw[5][:70]})')
        x, y = g.ev(f"({MESS_SCR})({seat[1]}, {seat[2]}, {seat[3]})"); g.page.mouse.click(x, y)
        for k in range(40):
            g.step(30)
            if g.ev("!!(ACT && ACT.phase === 'do')"): break
        s2 = g.ev(MESS_ST)
        check(s2[0] == 'sit' and not s2[3], f'back at your seat with no tray, you only sit ({s2[:4]})')
    # (2) the counter, from 3 m, four camera turns: points on its tap box with someone near on screen but the tap not on them
    g.ev("actEnd(true); SHIP.player.tray = null; setShipNow(18 * 60 + 40)"); g.step(30)
    tried, bad = 0, []
    for turn in range(4):
        g.ev("(() => { actEnd(true); const b = new THREE.Box3().setFromObject(__sv.hit), c = nearestOpen(b.min.x - 3, (b.min.z + b.max.z) / 2 + 2, player); player.obj.position.copy(cellPos(...c)); player.stop(); })()"); g.step(40)
        pts = g.ev(f"""(() => {{ const b = new THREE.Box3().setFromObject(__sv.hit), scr = {MESS_SCR}, out = [];
          for (const fz of [.1, .3, .5, .7, .9]) for (const fy of [.6, 1]) for (const fx of [0, .5]) {{
            const q = scr(b.min.x + (b.max.x - b.min.x) * fx, b.max.y * fy, b.min.z + (b.max.z - b.min.z) * fz); if (!(q[0] > 10 && q[0] < 380 && q[1] > 10 && q[1] < 834)) continue;
            const h = pick(q[0], q[1]), near = crewAtScreen(q[0], q[1]), el = document.elementFromPoint(q[0], q[1]);
            if (!h || h.object.userData.item !== __sv || !near || !el || el.tagName !== 'CANVAS') continue;
            const on = [.5, 1, 1.4].some(hy => {{ _cp.set(near.x, near.y + hy, near.z).project(camera); return Math.hypot((_cp.x + 1) / 2 * innerWidth - q[0], (1 - _cp.y) / 2 * innerHeight - q[1]) < CREW_ON_PX; }});
            if (!on) out.push([Math.round(q[0]), Math.round(q[1]), near.p ? near.p.id : '?']); }}
          return out.slice(0, 3); }})()""")
        for px, py, who in pts:
            g.ev("actEnd(true); player.stop()"); g.step(2)
            # the line moves between picking the point and the tap (RV10): only a point still on the counter, beside someone and not on them
            still = g.ev(f"""(() => {{ const h = pick({px}, {py}), near = crewAtScreen({px}, {py}); if (!h || h.object.userData.item !== __sv || !near) return false;
              return ![.5, 1, 1.4].some(hy => {{ _cp.set(near.x, near.y + hy, near.z).project(camera); return Math.hypot((_cp.x + 1) / 2 * innerWidth - {px}, (1 - _cp.y) / 2 * innerHeight - {py}) < CREW_ON_PX; }}); }})()""")
            if not still: continue
            g.page.mouse.click(px, py); g.step(6); tried += 1
            a = g.ev("ACT && ACT.kind")
            if a != 'queue': bad.append([turn, px, py, who, a])
        g.ev("actEnd(true)"); g.page.click('#rot'); g.step(80)
    print(f'   counter taps beside someone: {tried} tried, {tried - len(bad)} joined the queue')
    check(tried > 0 and not bad, f'a tap on the servery counter beside the staff or the line, not on them, joins the queue ({tried} tried: {bad[:3]})')
    # (3) LEAD31-14 (FX6), after the counter's part (before it, it moved the crowd the counter's taps meet): very hungry, the arrow says Food; a tray from the servery (a real tap) turns it to a seat for your
    # tray (it stayed on the servery: "You already have your tray" till Food 0); a real tap on that seat eats it
    g.ev("actEnd(true); SHIP.player.tray = null; clearGoal(); NEED_GOAL = null; SHIP.player.needs.hunger = 5; needGoal('hunger')"); g.step(4)
    a0 = g.ev("(goalNow() || {}).label")
    g.ev("(() => { __sv.hit.getWorldPosition(_wp); const c = nearestOpen(_wp.x - 3, _wp.z, player); player.obj.position.copy(cellPos(...c)); player.stop(); })()"); g.step(30)
    x, y = g.ev(f"({MESS_SCR})({sv[0]}, {sv[1]}, {sv[2]})"); g.page.mouse.click(x, y)
    for k in range(80):
        g.step(30)
        if g.ev("!!SHIP.player.tray"): break
    g.step(30)
    ts = g.ev(f"""(() => {{ const g = goalNow(), pl = g && g.place && PLACE_OF.get(g.place), s = pl && placeSpot(pl.id), q = s && {MESS_SCR}(s.x, s.y, s.z);
      return [!!SHIP.player.tray, g && g.label, pl && pl.type, pl && pl.id, q]; }})()""")
    check(a0 == 'Food' and ts[0] and ts[1] == 'A seat for your tray' and ts[2] == 'mess-seat', f'very hungry with a tray in hand, the arrow points at a seat for it, not the servery (LEAD31-14: before {a0!r}, then {ts[:4]})')
    if ts[4]:
        for k in range(20):   # as (1)'s seat: tap it only while it's on screen, nobody stands on the point and nothing covers it
            q = g.ev(f"""(() => {{ const s = placeSpot('{ts[3]}'), q = {MESS_SCR}(s.x, s.y, s.z), el = document.elementFromPoint(q[0], q[1]);
              return q[0] > 20 && q[0] < 370 && q[1] > 200 && q[1] < 800 && !crewAtScreen(q[0], q[1]) && el && el.tagName === 'CANVAS' ? q : null; }})()""")
            if q: break
            g.step(15)
        if q: g.page.mouse.click(*q)
        for k in range(40):
            g.step(30)
            if g.ev("!!(ACT && ACT.kind === 'eat' && ACT.phase === 'do')"): break
        te = g.ev("[ACT && ACT.kind, ACT && ACT.placeId, !!SHIP.player.tray, (goalNow() || {}).label || null, document.getElementById('tx').textContent.slice(0, 80)]")
        check(te[0] == 'eat' and not te[2] and te[3] != 'A seat for your tray', f'a tap on the seat the arrow shows eats your tray, and the arrow goes ({te})')
    # (4) FX12, the user's tray rules (0.92.4, item A; 0.92.3 let it travel): never sat down, your tray stays while you walk
    # in the mess hall and goes, with a word, once you leave it (here, for the gym); and off Deck 3 it's gone
    g.ev("actEnd(true); clearGoal(); NEED_GOAL = null; SHIP.player.tray = 'stew'; SHIP.player.trayLeft = 0; SHIP.player.needs.hunger = 60"); g.step(4)
    tm = g.ev("""(() => { const pp = player.obj.position, m = [...PLACE_OF.values()].filter(p => p.type === 'mess-seat' && p.room === 'M').map(p => placeSpot(p.id)).filter(Boolean)
      .sort((a, b) => Math.hypot(b.x - pp.x, b.z - pp.z) - Math.hypot(a.x - pp.x, a.z - pp.z))[0]; playerGo(m.walk); return K(m.walk); })()""")
    for k in range(60):
        g.step(10)
        if not g.ev("player.path.length"): break
    hm = g.ev("[roomAt(...player.here()), SHIP.player.tray, player.holding]")
    check(hm == ['M', 'stew', 'tray'], f'never sat down, walking about the mess hall your tray stays in your hands ({tm}, {hm})')
    tw = g.ev("""(() => { const b = [...PLACE_OF.values()].filter(p => p.type === 'gym' && p.room !== 'M').map(p => placeSpot(p.id)).filter(Boolean)[0]; if (!b) return null; playerGo(b.walk); return K(b.walk); })()""")
    for k in range(80):
        g.step(10)
        if not g.ev("player.path.length"): break
    hw = g.ev("[roomAt(...player.here()), SHIP.player.tray, document.getElementById('tx').textContent]")
    check(tw and hw[0] != 'M' and not hw[1] and 'leave your tray' in hw[2], f'out of the mess hall, the tray stays behind, and you\'re told ({tw}, {hw})')
    g.ev("goToDeck(3); SHIP.player.tray = 'stew'; goToDeck(4)"); g.step(30)
    d4 = g.ev("[deckDef.num, SHIP.player.tray, player.holding]")
    check(d4[0] == 4 and not d4[1] and d4[2] != 'tray', f'off Deck 3 your tray is gone ({d4})')
    check(not g.errors, f'no console errors ({g.errors[:3]})')
    g.close()

# patch 0.92.3 #22 (FX8): a real tap on the person you're due to meet keeps the appointment (Rina's health check: you
# walked up to her and tapped her, but only standing by the infirmary's bench counted, 2.2 tiles from where she stands)
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844); g.step(3)
    print('== an appointment kept by tapping the person (Rina in the infirmary, a real tap)')
    if g.ev("typeof GUIDE_ON !== 'undefined' && GUIDE_ON"): g.ev("GUIDE.tq.length = 0; guideToast = () => false")
    g.ev("setShipNow(1440 + 15 * 60 + 30); goToDeck(3)"); g.step(60)   # Day 2, 15:30: Rina at her infirmary station
    r = g.ev("""(() => { const a = DECK_CREW.find(x => x.p.id === 'rina'); if (!a || !a.settled) return null;
      const b = placeSpot('3-visit-1'), c = nearestOpen(a.x + 1.5, a.z + 1.5, player), q = cellPos(...c);
      player.obj.position.copy(q); player.stop();
      if (!Array.isArray(SHIP.device.appts)) SHIP.device.appts = [];
      SHIP.device.appts.push({ id: 9998, with: ['rina'], at: shipNow() + 1, len: 30, where: '3-visit-1', kind: 'checkup', status: 'yes', by: 'rina', title: 'Health check (test)' });
      return { rina: [a.x, a.z], bench: Math.hypot(q.x - b.x, q.z - b.z), her: Math.hypot(q.x - a.x, q.z - a.z) }; })()""")
    check(r and r['bench'] > 2.2 and r['her'] < 4, f'standing by Rina, not by the bench, with a health check due ({r})')
    if r:
        g.step(4); pt = None
        for k in range(20):
            pt = g.ev("""(() => { const a = DECK_CREW.find(x => x.p.id === 'rina'), scr = """ + MESS_SCR + """;
              for (const hy of [1.0, .5, 1.4]) { const q = scr(a.x, a.y + hy, a.z), el = document.elementFromPoint(q[0], q[1]);
                if (q[0] > 20 && q[0] < 370 && q[1] > 120 && q[1] < 760 && crewAtScreen(q[0], q[1]) === a && el && el.tagName === 'CANVAS') return q; } return null; })()""")
            if pt: break
            g.step(10)
        st0 = g.ev("SHIP.device.appts.find(a => a.id === 9998).status")
        if pt: g.page.mouse.click(*pt)
        g.step(4)
        st = g.ev("[SHIP.device.appts.find(a => a.id === 9998).status, document.getElementById('tt').textContent, document.getElementById('tx').textContent]")
        check(pt and st0 == 'yes' and st[0] == 'kept' and 'Kept' in st[2], f'a real tap on Rina keeps the health check, and says so ({pt}, {st0} -> {st})')
        g.ev("SHIP.device.appts = SHIP.device.appts.filter(a => a.id !== 9998)")
        # with nothing due, a tap on her is a word with her as ever (no appointment touched)
        g.step(200)
        if pt: g.page.mouse.click(*pt)
        g.step(4)
        n = g.ev("document.getElementById('tx').textContent")
        check('Kept' not in n, f'with nothing due, a tap on her is the usual card ({n[:60]})')
        # RV11: she must be there for it: a tap on her outside the infirmary, away from her spot (still on her way), keeps nothing
        w = g.ev("""(() => { if (typeof apptTapKeep !== 'function') return null; const b = placeSpot('3-visit-1'), rp = schedData().people.find(q => q.id === 'rina'); let best = null;
          for (let i = 0; i < W; i++) for (let j = 0; j < D; j++) { if (!free(i, j) || roomAt(i, j) === 'I' || !roomAt(i, j)) continue; const c = cellPos(i, j), d = Math.hypot(c.x - b.x, c.z - b.z); if (d > 3 && d < 7 && (!best || d < best[0])) best = [d, i, j]; }
          if (!best) return null; const c = cellPos(best[1], best[2]); player.obj.position.copy(c); player.stop();
          SHIP.device.appts.push({ id: 9997, with: ['rina'], at: shipNow() + 1, len: 30, where: '3-visit-1', kind: 'checkup', status: 'yes', by: 'rina', title: 'Health check (test)' });
          const k = apptTapKeep(rp, c.x, c.z), st = SHIP.device.appts.find(a => a.id === 9997).status; SHIP.device.appts = SHIP.device.appts.filter(a => a.id !== 9997);
          return [roomAt(best[1], best[2]), +best[0].toFixed(1), !!k, st]; })()""")
        check(w and not w[2] and w[3] == 'yes', f'a tap on Rina outside the infirmary, 3+ tiles from her spot, keeps nothing ([room, tiles from the bench, kept, status]: {w})')
    # RV11: an occasion (Calder's progress talk) is met only in its room: a tap on its host near you but outside it leaves it 'yes'
    oc = g.ev("""(() => { if (typeof apptTapKeep !== 'function') return 'no apptTapKeep (an older build)'; if (typeof occasionAdd !== 'function' || typeof OCCASIONS === 'undefined' || !OCCASIONS.progressTalk) return null;
      setShipNow(1440 + 15 * 60 + 30); goToDeck(5); const a = DECK_CREW.find(x => x.p.id === 'calder'); if (!a) return 'no calder';
      const rm = roomAt(...cellAt(a.x, a.z)); let best = null;
      for (let i = 0; i < W; i++) for (let j = 0; j < D; j++) { if (!free(i, j) || roomAt(i, j) === rm || !roomAt(i, j)) continue; const c = cellPos(i, j), d = Math.hypot(c.x - a.x, c.z - a.z); if (d < 4 && (!best || d < best[0])) best = [d, i, j]; }
      if (!best) return 'no spot'; player.obj.position.copy(cellPos(best[1], best[2])); player.stop();
      occasionAdd('progressTalk', shipNow() + 1); const ap = SHIP.device.appts.find(x => x.occ && x.status === 'yes' && (x.with || []).includes('calder')); if (!ap) return 'no appt';
      const k = apptTapKeep(a.p, a.x, a.z); return [rm, roomAt(best[1], best[2]), +best[0].toFixed(1), !!k, ap.status]; })()""")
    check(isinstance(oc, list) and not oc[3] and oc[4] == 'yes', f"a tap on Calder near you but outside her office leaves her progress talk's appointment 'yes' ([her room, yours, tiles, kept, status]: {oc})")
    check(not g.errors, f'no console errors ({g.errors[:3]})')
    g.close()

    # 0.92.6 #16 (the user's): a small Lift button, like Put down, when you stand very close to a lift panel (and in the car,
    # lead 35); hidden a few metres off and with the panel open; a tap opens the panel. Off at test URLs unless switched on
    g = Game(pw, sys.argv[1]); g.step(5)
    if g.ev("typeof liftBtnShow === 'function'"):
        lift = g.ev("""(() => { const out = {}, vis = () => { handTick(true); const b = document.getElementById('liftBtn'); return !!b && !b.hidden; };
          LIFT_BTN_ON = false; goToDeck(4); player.stop(); out.off = vis(); LIFT_BTN_ON = true;
          const q = ixLiftPanel(), here = player.here(); out.room = roomAt(...here); out.car = vis();
          let near = null, far = null;
          for (let i = 0; i < W; i++) for (let j = 0; j < D; j++) { if (!free(i, j) || !roomAt(i, j) || !ROOMS[roomAt(i, j)].hall) continue; const c = cellPos(i, j), d = Math.hypot(c.x - q.x, c.z - q.z);
            if (d < LIFT_BTN_NEAR && (!near || d < near[0])) near = [d, i, j]; if (d > 3 && d < 5 && !far) far = [d, i, j]; }
          if (near) { player.obj.position.copy(cellPos(near[1], near[2])); player.stop(); out.near = [+near[0].toFixed(2), roomAt(near[1], near[2]), vis()]; }
          if (far) { player.obj.position.copy(cellPos(far[1], far[2])); player.stop(); out.far = [+far[0].toFixed(2), vis()]; }
          out.decks = {}; out.walled = [];                // every built deck: a landing tile by a panel shows it; no non-hall tile that near does (walls, the trunks' glass)
          for (const n of DECK_ORDER) { if (!DECKS[n]) continue; goToDeck(n); player.stop(); const p0 = ixLiftPanel(); if (!p0) { out.decks[n] = 'no panel'; continue; } let hit = 0;
            for (let i = 0; i < W; i++) for (let j = 0; j < D; j++) { const r = roomAt(i, j); if (!free(i, j) || !r || ROOMS[r].floor === 'lift') continue; const c = cellPos(i, j);
              player.obj.position.copy(c); player.stop(); const q2 = ixLiftPanel(); if (!q2 || Math.hypot(c.x - q2.x, c.z - q2.z) >= LIFT_BTN_NEAR) continue;
              if (vis()) { if (ROOMS[r].hall) hit++; else out.walled.push([n, r, i, j]); } }
            out.decks[n] = hit; }
          goToDeck(4); player.stop();
          if (near) { player.obj.position.copy(cellPos(near[1], near[2])); player.stop(); vis(); }
          return out; })()""")
        print('  the Lift button:', lift)
        check(lift['off'] is False and lift['car'] is True and lift.get('near') and lift['near'][2] is True and lift.get('far') and lift['far'][1] is False,
              f'the Lift button: off at test URLs till switched on, shown in the car and by the landing panel, hidden 3+ m away (0.92.6 #16): {lift}')
        check(all(isinstance(v, int) and v > 0 for v in lift['decks'].values()) and not lift['walled'], f'on every deck the Lift button shows on the landing by a panel, and never from a room beyond a wall or the glass (0.92.6 #16): {lift["decks"]} {lift["walled"][:4]}')
        bb = g.ev("(() => { const b = document.getElementById('liftBtn').getBoundingClientRect(); return [Math.round(b.left + b.width / 2), Math.round(b.top + b.height / 2)]; })()")
        g.page.mouse.click(*bb); g.step(40)
        op = g.ev("[!document.getElementById('lift').hidden, (handTick(true), document.getElementById('liftBtn').hidden)]")
        check(op[0] and op[1], f'a tap on the Lift button opens the lift panel, and the button hides while it is open (0.92.6 #16): {op}')
        g.ev("closeLiftPanel(); LIFT_BTN_ON = false")
    else: check(False, 'no liftBtnShow (0.92.6 #16)')
    # Auto doors (0.93.2, the user's): with the setting off, for you only, a door stays shut to your own steering; a tap on
    # the door opens it; a tap in the room beyond walks you through (it opens as you reach it); on, as always; the crew
    # never asked; the setting saved only when off, and loaded back
    if g.ev("typeof adoorShut === 'function' && AUTO_DOORS_ON"):
        AD = r"""(() => { goToDeck(3); actEnd(true); player.stop(); adoorSet(false); const ds = DOOR_OBJS.filter(o => o.e.type === 'door').map(o => [o, doorSides(o.e)]).filter(([o, s]) => s.length === 2 && s.every(([i, j]) => free(i, j)));
          const [o, s] = ds[0]; window.__door = { key: o.e.key, a: s[0], b: s[1] }; player.obj.position.copy(cellPos(...s[0])); player.stop(); return o.e.key; })()"""
        STEER = r"""(() => { const { a, b } = window.__door, A = cellPos(...a), B = cellPos(...b), dx = B.x - A.x, dz = B.z - A.z, d = Math.hypot(dx, dz); player.steer = { x: dx / d, z: dz / d, k: 1 }; return true; })()"""
        AT = r"""(() => { const { a, b, key } = window.__door, h = player.here(), o = DOOR_OBJS.find(x => x.e.key === key); return [h[0] === a[0] && h[1] === a[1], h[0] === b[0] && h[1] === b[1] || Math.hypot(player.obj.position.x - cellPos(...a).x, player.obj.position.z - cellPos(...a).z) > 1.5, +o.open.toFixed(2)]; })()"""
        BACK = "(() => { endSteer(); ADOOR.tap = null; player.obj.position.copy(cellPos(...window.__door.a)); player.stop(); return true; })()"
        ad = {'door': g.ev(AD)}
        g.ev(STEER); g.step(60); ad['steerOff'] = g.ev(AT); g.ev(BACK); g.step(20)
        g.ev("adoorTap(window.__door.key)"); g.step(40); g.ev(STEER); g.step(60); ad['afterTap'] = g.ev(AT); g.ev(BACK); g.step(20)
        ad['self'] = g.ev("(() => { const ok = adoorTapSelf(); return [ok, ADOOR.tap === window.__door.key]; })()"); g.ev(BACK); g.step(20)   # a tap on yourself by the shut door is the door's (RV18)
        g.ev("playerGo(window.__door.b)"); mx = 0
        for i in range(12): g.step(10); mx = max(mx, g.ev(AT)[2])
        ad['walkIn'] = g.ev(AT); ad['walkOpen'] = mx; g.ev(BACK); g.step(20)
        ad['crew'] = g.ev("(() => { const e = EDGES.get(window.__door.key), a = DECK_CREW.find(c => c.p); return [!!a && adoorShut(e, a), !!a && edgeBlocks(e, a.p)]; })()")
        ad['saved'] = g.ev("(() => { const d = deviceLoad({ device: JSON.parse(JSON.stringify(SHIP.device)) }); return [SHIP.device.settings.doors, d.settings.doors]; })()")
        # 0.93.3: the three choices; an old save's autoDoors: false is 'none', nothing is the default 'private' (not saved);
        # in 'private' a public door opens by itself to your own steering and a bunk room's stays shut
        ad['old'] = g.ev("(() => { const L = s => deviceLoad({ device: { settings: s } }).settings; return [L({ autoDoors: false }).doors, L({}).doors === undefined, L({ doors: 'all' }).doors, L({ doors: 'private' }).doors === undefined]; })()")
        PRIV = r"""(priv => { adoorSet('private'); goToDeck(priv ? 4 : 3); actEnd(true); player.stop(); const ds = DOOR_OBJS.filter(o => o.e.type === 'door' && adoorPrivate(o.e.key) === priv).map(o => [o, doorSides(o.e)]).filter(([o, s]) => s.length === 2 && s.every(([i, j]) => free(i, j)));
          const [o, s] = ds[0]; window.__door = { key: o.e.key, a: s[0], b: s[1] }; player.obj.position.copy(cellPos(...s[0])); player.stop(); return [o.e.key, doorsMode(), 'doors' in SHIP.device.settings]; })(%s)"""
        ad['pubSet'] = g.ev(PRIV % 'false'); g.ev(STEER); g.step(60); ad['pub'] = g.ev(AT); g.ev(BACK)
        ad['privSet'] = g.ev(PRIV % 'true'); g.ev("ADOOR.hints = 0; ADOOR.hintAt = -1e9; document.getElementById('tx').textContent = ''"); g.ev(STEER); g.step(60); ad['priv'] = g.ev(AT)
        ad['hint'] = g.ev("[ADOOR.hints, document.getElementById('tx').textContent]"); g.ev(BACK)
        # FX29 (RV18's should): a real tap on your own body, standing by the bunk room's shut door, opens it (pick() never returns you)
        if g.ev("typeof adoorOnMe === 'function'"):
            g.ev(PRIV % 'true'); g.ev("(() => { ADOOR.here = null; const p = player.obj.position; target.copy(p).setY(.7); placeCam(); })()"); g.step(5)   # (adoorSet in the doorway the last part left you in keeps that door open till you're clear: not this test's case)
            xy = g.ev("(() => { const p = player.obj.position, v = new THREE.Vector3(p.x, .9, p.z).project(camera); return [(v.x + 1) / 2 * innerWidth, (1 - v.y) / 2 * innerHeight, adoorSelfKey()]; })()")
            g.page.mouse.click(xy[0], xy[1]); g.step(3)
            ad['tapMe'] = g.ev("[ADOOR.tap === window.__door.key, ADOOR.tap]") + [xy[2]]; g.ev(BACK); g.ev("ADOOR.tap = null")
            check(ad['tapMe'][0], f"Doors 'private': a real tap on yourself by the bunk room's shut door opens it (FX29, RV18): {ad['tapMe']} {xy}")
            check(ad['hint'][0] == 1 and 'Tap the door' in ad['hint'][1], f"Doors 'private': stopped at the shut door by your own steering, the hint says how it opens, once (FX29): {ad['hint']}")
        else: check(False, 'no adoorOnMe (FX29)')
        # FX29 (lead 39, CR1's week guide): an arrow's way opens its doors, however you walk; with the arrow gone, the rule again
        if g.ev("typeof adoorWay === 'function'"):
            g.ev(PRIV % 'true'); g.ev("(() => { window.__trk = SHIP.player.track; SHIP.player.track = null; setGoal({ deck: 4, at: window.__door.b, label: 'FX29 test' }); adoorWay(goalNow()); })()")
            ad['wayDoors'] = g.ev("!!ADOOR.way && ADOOR.way.doors.has(window.__door.key)")
            g.ev(STEER); g.step(60); ad['way'] = g.ev(AT); g.ev(BACK); g.step(5)
            g.ev("(() => { clearGoal(); adoorWay(goalNow()); })()"); g.ev(STEER); g.step(60); ad['wayGone'] = g.ev(AT); g.ev(BACK)
            g.ev("(() => { SHIP.player.track = window.__trk; })()")
            check(ad['wayDoors'] and ad['way'][1], f"Doors 'private': the arrow's way opens its bunk-room door to your own steering (FX29): {ad['wayDoors']} {ad['way']}")
            check(ad['wayGone'][0] and ad['wayGone'][2] < .05, f"Doors 'private': the arrow gone, the bunk room's door is shut to your steering again (FX29): {ad['wayGone']}")
        else: check(False, 'no adoorWay (FX29)')
        g.ev(AD)   # back to the Deck 3 door, all doors on a tap
        g.ev("adoorSet(true)"); g.ev(STEER); g.step(60); ad['steerOn'] = g.ev(AT); g.ev(BACK)
        ad['savedOn'] = g.ev("'autoDoors' in deviceLoad({ device: JSON.parse(JSON.stringify(SHIP.device)) }).settings")
        print('  Auto doors:', ad)
        check(ad['steerOff'][0] and ad['steerOff'][2] < .05, f"Auto doors off: walking into a shut door yourself, you stop at it and it stays shut (0.93.2): {ad['steerOff']}")
        check(ad['afterTap'][1], f"Auto doors off: a tap on the door opens it and you can walk through (0.93.2): {ad['afterTap']}")
        check(ad['walkIn'][1] and ad['walkOpen'] > .5, f"Auto doors off: a tap in the room beyond walks you through, the door opening as you reach it (0.93.2): {ad['walkIn']} {ad['walkOpen']}")
        check(ad.get('self') == [True, True], f"Auto doors off: a tap on yourself right by a shut door opens it (0.93.2, RV18): {ad.get('self')}")
        check(ad['steerOn'][1], f"Auto doors on: you walk straight through, as always (0.93.2): {ad['steerOn']}")
        check(ad['crew'] == [False, False], f"Auto doors: the crew are never stopped (0.93.2): {ad['crew']}")
        check(ad['saved'] == ['none', 'none'] and ad['savedOn'] is False, f"Doors: 'none' saved and loaded back (0.93.3): {ad['saved']} {ad['savedOn']}")
        check(ad['old'] == ['none', True, 'all', True], f"Doors: an old save's autoDoors off is 'none'; nothing, or 'private', is the default and not saved (0.93.3): {ad['old']}")
        check(ad['pubSet'][1] == 'private' and ad['pubSet'][2] is False and ad['pub'][1], f"Doors 'private' (the default): a public door opens as you walk into it (0.93.3): {ad['pubSet']} {ad['pub']}")
        check(ad['priv'][0] and ad['priv'][2] < .05, f"Doors 'private': a bunk room's door stays shut to your own steering (0.93.3): {ad['privSet']} {ad['priv']}")
    else: check(False, 'no Auto doors (0.93.2)')
    # Take a seat (0.93.2, the user's): with a tray in the mess hall, next to a free mess seat, a button the size of Put down
    # just above it; a tap sits you at the nearest free seat and you eat (the tray's sit-and-eat); none without a tray, none
    # outside the mess hall, none with no free seat near
    if g.ev("typeof seatBtnSeat === 'function'"):
        g.ev("(() => { goToDeck(3); actEnd(true); setShipNow(18 * 60 + 30); deckCrewFill(); SHIP.player.tray = null; })()")
        tb = g.ev(r"""(() => { const out = {}, vis = () => (handTick(true), !document.getElementById('seatBtn').hidden), rect = id => { const b = document.getElementById(id).getBoundingClientRect(); return [b.top, b.bottom, b.right, b.height]; };
          const pl = [...PLACE_OF.values()].find(q => q.type === 'mess-seat' && !heldBy(q.id)), sp = placeSpot(pl.id);
          player.obj.position.set(sp.x + 1.0, 0, sp.z + .6); player.stop(); out.noTray = vis();
          SHIP.player.tray = 'stew'; SHIP.player.trayLeft = 0; out.tray = vis(); out.near = (seatBtnSeat() || [{}])[0].id; return out; })()""")
        g.step(10)   # Put down shows on its own tick: give it a few frames before measuring the two
        tb.update(g.ev(r"""(() => { const out = {}, vis = () => (handTick(true), !document.getElementById('seatBtn').hidden), rect = id => { const b = document.getElementById(id).getBoundingClientRect(); return [b.top, b.bottom, b.right, b.height]; };
          out.near = (seatBtnSeat() || [{}])[0].id;   // again: the crew move in those frames
          if (vis()) { const s = rect('seatBtn'), p = rect('putDown'); out.above = s[1] <= p[0] && s[1] > p[0] - 30; out.same = Math.abs(s[3] - p[3]) <= 1; out.right = Math.abs(s[2] - p[2]) <= 1; }
          const p0 = player.obj.position.clone(), lp = [...PLACE_OF.values()].find(q => q.type === 'lounge-seat' && placeSpot(q.id)), ls = placeSpot(lp.id); player.obj.position.set(ls.x + .8, 0, ls.z); player.stop(); out.lounge = vis();
          player.obj.position.copy(p0); player.stop(); vis(); return out; })()"""))
        bb = g.ev("(() => { const b = document.getElementById('seatBtn').getBoundingClientRect(); return [Math.round(b.left + b.width / 2), Math.round(b.top + b.height / 2)]; })()")
        g.page.mouse.click(*bb); g.step(5)
        tb['tap'] = g.ev("[ACT && ACT.kind, ACT && !!ACT.o.fed, ACT && ACT.placeId, (handTick(true), document.getElementById('seatBtn').hidden)]")
        g.ev("(() => { actEnd(true); SHIP.player.tray = null; handTick(true); })()")
        print('  Take a seat:', tb)
        check(tb['noTray'] is False and tb['tray'] is True and tb.get('above') and tb.get('same') and tb.get('right') and tb['lounge'] is False,
              f'Take a seat: only with a tray in the mess hall by a free seat, Put down\'s size, straight above it (0.93.2): {tb}')
        check(tb['tap'][0] == 'eat' and tb['tap'][1] is True and tb['tap'][2] == tb['near'] and tb['tap'][3] is True,
              f'a tap on Take a seat sits you at the nearest free seat to eat your tray, and the button goes (0.93.2): {tb["tap"]}')
    else: check(False, 'no seatBtnSeat (0.93.2, Take a seat)')
    check(not g.errors, f'no console errors ({g.errors[:3]})')
    g.close()

# the comet (FX25, 0.93.2; plans/events-plan-2.html A8), with the build's EV_COMET_ON: on Day 22 the two jobs on the board at
# 09:05 (the blankets for anyone, the scope's filter for Officers and up), kept for you; from 21:30 the marker over Sato and
# the arrow at her; a tap on Sato joins you at the bow glass (her words, a spot by her); at 21:50 her naming card (your
# pick kept); at 22:00 the arrow at Saruth and a tap ties your knot (its trace); a tap on Mori, Tomas and the Captain each
# joins theirs (the Captain as an Officer); a Cadet tapping the Captain is sent to the bow lounge, kindly, the arrow with them
COMET_LIVE = r"""(() => { const R = {}, d = 22, B = (d - 1) * 1440;
  const tick = (a, b) => { for (let t = a; t <= b; t++) { setShipNow(t); EV_MIN = -1; eventsTick(); } };
  const into = (n, rk) => { actEnd(true); clearGoal(); goToDeck(n); deckCrewFill(); const tl = ROOM_TILES[rk], c = cellPos(...tl[Math.floor(tl.length / 2)]); player.obj.position.copy(cellPos(...nearestOpen(c.x, c.z, player))); player.stop(); };
  const tap = id => { const a = tjAgent(id); if (!a) return { id, err: 'not on the deck' }; const ok = tradJoinTap(a); return { id, ok, joined: SHIP.events.joined.filter(k => /^comet/.test(k)), act: ACT && ACT.kind, toast: document.getElementById('tx').textContent }; };
  skipTo(B + 545); R.jobs = (SHIP.jobs || []).filter(j => j.event === 'comet').map(j => [j.eventJob, j.reserved || null, j.only || null, j.status]);
  skipTo(B + 1260); into(3, 'L'); tick(B + 1261, B + 1296); deckCrewFill(); tick(B + 1297, B + 1300);
  R.lead = TJ_NOW && [TJ_NOW.key, TJ_NOW.lead]; R.goal = IX_GOAL && IX_GOAL.crew; R.mark = (document.getElementById('tjMark') || {}).textContent || '';
  R.sato = tap('sato'); tick(B + 1301, B + 1312); R.card = DIALOGUE && DIALOGUE.id;
  let n = 0; while (DIALOGUE && n++ < 10) { const v = dialogueView(); if (v.choices) dialogueStep(2); else dialogueStep(); }
  R.named = SHIP.event && [SHIP.event.mine.named, SHIP.event.mine.namedBy];
  tick(B + 1313, B + 1321); R.goal2 = IX_GOAL && IX_GOAL.crew; R.knot = tap('saruth'); R.knotCard = DIALOGUE && DIALOGUE.id; if (DIALOGUE) dialogueEnd(true);
  R.trace = SHIP.traces.some(t => (t.id || t) === 'cometKnotYours');
  into(2, 'J'); tick(B + 1322, B + 1323); R.mori = tap('mori');
  into(4, 'j'); tick(B + 1324, B + 1325); R.tomas = tap('tomas');
  into(1, 'O'); tick(B + 1326, B + 1327); R.cadetMark = !!TJ_NOW; R.cadet = tap('marrow'); R.cadetGoal = IX_GOAL && [IX_GOAL.deck, IX_GOAL.room];
  const wk = SHIP.works; SHIP.works = { ...(wk || {}), rank: 'officer' }; clearGoal(); tick(B + 1328, B + 1329); R.officerMark = !!TJ_NOW; R.officer = tap('marrow'); SHIP.works = wk;
  R.skyUp = !!COMET_SKY.m; tick(B + 1330, B + 1366); R.skyGone = !COMET_SKY.m;   // c.3: the sky shape up while it passes, gone by 22:46
  if (DIALOGUE) dialogueEnd(true); actEnd(true); return R; })()"""
if True:
    print('\nThe comet (Day 22):')
    with sync_playwright() as pw:
        g = Game(pw, sys.argv[1])
        if not g.ev("typeof EV_COMET_ON !== 'undefined' && EV_COMET_ON && !!SHIP_EVENTS.comet"): print('  SKIP: the comet is switched off')
        else:
            C = g.ev(COMET_LIVE)
            for k, v in C.items(): print(f'  {k}: {v}')
            check(sorted(C['jobs']) == [['cometBlankets', 'event', None, 'open'], ['cometFilter', 'event', 'officer', 'open']], f"the comet's two jobs on the board at 09:05, kept for you, the filter Officers and up: {C['jobs']}")
            check(C['lead'] == ['cometLounge@22', 'sato'] and C['goal'] == 'sato' and 'Sato' in C['mark'], f"the marker and the arrow at Sato from 21:30: {C['lead']} {C['goal']} {C['mark']}")
            check(C['sato'].get('ok') and 'cometLounge@22' in C['sato']['joined'] and C['sato']['act'] == 'tj:cometLounge' and 'Sato' in C['sato']['toast'], f"a tap on Sato joins you at the bow glass: {C['sato']}")
            check(C['card'] and 'comet.name' in C['card'] and C['named'] == [3, 'you'], f"Sato's naming card at 21:50, your pick kept: {C['card']} {C['named']}")
            check(C['goal2'] == 'saruth' and C['knot'].get('ok') and C['knotCard'] and 'knot' in C['knotCard'] and C['trace'], f"Saruth's knot at 22:00: {C['goal2']} {C['knot']} {C['knotCard']} {C['trace']}")
            for k, want in (('mori', 'ixStars'), ('tomas', 'tj:cometStern'), ('officer', 'tj:cometCaptain')):
                check(C[k].get('ok') and C[k]['act'] == want, f"a tap on the host joins ({k}): {C[k]}")
            check(not C['cadetMark'] and C['cadet'].get('ok') and 'downstairs' in C['cadet']['toast'] and 'cometCaptain@22' not in C['cadet']['joined'] and C['cadetGoal'] == [3, 'L'] and C['officerMark'],
                  f"a Cadet at the Captain's tea is sent to the bow lounge, kindly; an Officer has the marker: {C['cadetMark']} {C['cadet']} {C['cadetGoal']} {C['officerMark']}")
            check(C.get('skyUp') and C.get('skyGone'), f"the comet's sky shape up while it passes and gone by 22:46: {C.get('skyUp')} {C.get('skyGone')}")
        check(not g.errors, f'no console errors in the comet part ({g.errors[:3]})')
        g.close()

# MA6-1 (PZ6 for lead 41): an ordinary team job (24h, M8) as a real player at phone size. An Officer in the Day 17
# scrubber job (the rota's own, posted the day before), at your spot: the job is one of your chores at your turn; a real
# tap on your spot's floor starts your turn (Holding) and, done, the job moves on to the next step; a tap during
# someone else's step is refused (24h's veto: "Not yet"), nothing done
TEAM_SET = r"""(() => { const reset = t => { machinesNew(); SHIP.jobs = []; MACH_HOUR = null; MACH_SEEN = -1; setShipNow(t); machinesNow(); SHIP.works = null; worksInit(t); SHIP.works.team = { plan: {} }; SHIP.works.inc = { plan: {}, open: null }; };
  reset(15 * 1440 + 900); SHIP.works.rank = 'officer'; SHIP.works.tier = 2; let j = null;
  for (let t = 15 * 1440 + 900; t <= 16 * 1440 + 900; t += 5) { setShipNow(t); machinesNow(); for (const f of WORK_TICKS) f(t, false); j = SHIP.jobs.find(x => x.kind === 'team' && x.claimedBy === 'you'); if (j && t >= j.start - 5) break; }
  if (!j) return null;
  for (const k of NEED_KEYS) SHIP.player.needs[k] = 90;
  goToDeck(j.deck); const s = placeSpot(j.spots.you); player.obj.position.set(s.x, player.obj.position.y, s.z); target.copy(player.obj.position).setY(.7); player.stop();
  window.__tj = j.id; return { id: j.id, spot: j.spots.you, seq: j.seq.map(x => x.who) }; })()"""
TEAM_TO = r"""((mine) => { const j = SHIP.jobs.find(x => x.id === window.__tj);   // the clock to the next step that is (mine) or isn't yours
  for (let t = shipNow(); t < j.start + 120; t++) { setShipNow(t); for (const f of WORK_TICKS) f(t, false); if (j.cur >= 0 && j.cur < j.seq.length && (j.seq[j.cur].who === 'you') === mine) break; }
  return { cur: j.cur, who: j.seq[j.cur] && j.seq[j.cur].who, chores: ixChores().map(x => x.id) }; })"""
TEAM_XY = r"""(() => { const j = SHIP.jobs.find(x => x.id === window.__tj), s = placeSpot(j.spots.you), v = new THREE.Vector3(s.x, .05, s.z).project(camera), r = renderer.domElement.getBoundingClientRect();
  return [r.left + (v.x + 1) / 2 * r.width, r.top + (1 - v.y) / 2 * r.height]; })()"""
TEAM_ST = r"""(() => { const j = SHIP.jobs.find(x => x.id === window.__tj); return { cur: j.cur, done: (j.stepsDone || []).slice(), act: ACT && ACT.kind, job: ACT && ACT.o && ACT.o.job, toast: (document.getElementById('toast') || {}).textContent || '' }; })()"""
if True:
    print('\nA team job\'s turn by a real tap (MA6-1):')
    with sync_playwright() as pw:
        g = Game(pw, sys.argv[1], 390, 844); g.step(5)
        g.ev("SHIP.device && SHIP.device.settings && (SHIP.device.settings.tips = false)")
        T = g.ev(TEAM_SET); print('  ', T)
        check(T and 'you' in T['seq'], f"a team job with you in it, at your spot: {T}")
        if T:
            g.step(20); a = g.ev(f"({TEAM_TO})(false)"); g.step(6)
            x, y = g.ev(TEAM_XY); g.page.mouse.click(x, y); g.step(240); early = g.ev(TEAM_ST); print('   out of turn:', a, early)
            check(not early['done'] and early['cur'] <= 1, f"a tap during someone else's step does none of yours (the lead's step runs on by itself): {early}")
            b = g.ev(f"({TEAM_TO})(true)"); g.step(6); print('   your turn:', b)
            check(T['id'] in b['chores'], f"at your turn the team job is one of your chores (15b's ixChores): {b['chores']}")
            g.ev("actEnd(true)"); g.step(4); x, y = g.ev(TEAM_XY); g.page.mouse.click(x, y); g.step(30); c = g.ev(TEAM_ST)
            check(c['act'] == 'ixStop' and c['job'] == T['id'], f"a real tap on your spot starts your turn: {c}")
            g.step(300); d = g.ev(TEAM_ST); print('   after:', d)
            check(0 in d['done'] and d['cur'] > b['cur'], f"your turn done, the job on to the next step: {d}")
        check(not [e for e in g.errors if e.startswith('pageerror')], f'no page errors in the team part ({g.errors[:2]})')
        g.close()

print('INTERACTIONS CHECK OK' if ok else 'INTERACTIONS CHECK FAILED')
sys.exit(0 if ok else 1)
