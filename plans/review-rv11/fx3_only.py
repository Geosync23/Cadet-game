# Starship Cadet: interactions check (keep in the repo, next to player_check.py)
# Checks section 15b (the interactions engineer): more places to use, the job board, the goal pointer.
#   parity: tapping the real things on the real decks starts the crew's activity there (the bar, lounges, reading
#   seats, benches, the garden, the music room, the laundry, basins, the kettle, the telescope, the observatory),
#   with a pose, and the main need rises; places crew hold are "In use"; private cabins, beds, notices and
#   section 15's own taps (treadmill, shower) are left alone; walking away stops it; draw calls stay under BUDGET
#   the job board: tapping it opens the list; Take it claims the job (section 17's claimJob); Drop it puts it back;
#   a round or a haul has a Take it; a side job (the drill) and the other registered kinds (an incident, a leak...) not
#   the goal pointer: hidden with no goal; your job's next step shows by itself; on another deck it says "Take the
#   lift to Deck N"; setGoal / clearGoal; an arrow at the screen edge when the place is off screen, a marker when on
# Setup and environment as for cadet_test.py.
# Run:  python3 interactions_check.py BUILD.html
import sys, json
exec(open('/home/user/w-fx3b/cadet_test.py').read().split("a, shots = run(")[0])
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


print('FX3 BLOCK', 'OK' if ok else 'FAILED')
