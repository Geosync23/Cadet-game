# Starship Cadet: a tap on the thing at your small job's stop (FX30 for lead 49, backlog JB2-2, 0.99.6; a one-off
# targeted check, kept next to the others). "Unstick a gym locker" (oj-d3gym-locker) stops at 3-gym-1, a treadmill.
# With the job yours, a real screen click on that treadmill:
#   on the build as it is (FIXTAP_ON off): starts a run (gym), not the repair, as backlog JB2-2 says;
#   on a copy with FIXTAP_ON on: starts the job's step (ixStop). The only tappable treadmill, "Treadmills", stands on
#   3-gym-2, next to the stop: a click on it is the job; a click on another thing in the gym (the punch bag, 3-gym-13)
#   is still that thing; with no job "Treadmills" is a run as before; with another
#   gym job (the vent, not in FIXTAP_ROWS) a tap on it does just what it does off.
# Run:  python3 fixtap_probe.py BUILD.html
import sys, json, os, pathlib
exec(open(__file__.replace('fixtap_probe.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
ok = True
def check(cond, msg):
    global ok
    print('ok  ' if cond else 'FAIL', msg)
    if not cond: ok = False
    return cond

MK = r"""((rid) => { actEnd(true); for (const k of NEED_KEYS) SHIP.player.needs[k] = 80;   // fresh for each tap (a fourth workout in a row is refused) for (const j of SHIP.jobs) if (j.claimedBy === 'you' && j.status === 'claimed') { j.claimedBy = null; j.status = 'open'; }
  SHIP.jobs = SHIP.jobs.filter(j => !String(j.id).startsWith('fxtap-')); SHIP.player.work = null; SHIP.player.carry = [];
  if (!rid) { MACH_REV++; return null; }
  const r = fixRow(rid), pl = placeById(r.place), t = shipNow();
  const j = { id: 'fxtap-' + r.id, machine: null, deck: pl.deck, room: pl.room, kind: 'chore', chore: 'fix', target: r.id, title: r.title, tier: 1, stops: [{ deck: pl.deck, placeId: r.place, mins: r.mins, tag: 'fix' }],
    urgency: 0, posted: t, found: t, claimedBy: 'you', status: 'claimed', start: t, parts: [], fix: r.id, fixS: 'o', tool: r.tool };
  SHIP.jobs.push(j); MACH_REV++; return r.place; })"""
PUT = r"""((pid) => { const s = placeSpot(pid), gl = nearestOpen(s.x, s.z + 1.2, player); player.obj.position.copy(cellPos(...gl)); player.stop(); })"""
# the screen point of the item nearest a place's spot (its hit box centre), and the item's title
AIM = r"""((pid) => { const s = placeSpot(pid), b = new THREE.Box3(), c = new THREE.Vector3();
  const its = ITEMS.filter(i => i.hit).map(i => { b.setFromObject(i.hit); b.getCenter(c); return [i, c.clone(), b.distanceToPoint(new THREE.Vector3(s.x, c.y, s.z))]; }).sort((m, n) => m[2] - n[2]);
  const [it, p] = its[0], v = p.clone().project(camera); return { t: it.t, d: Math.round(its[0][2] * 100) / 100, xy: [(v.x + 1) / 2 * innerWidth, (1 - v.y) / 2 * innerHeight] }; })"""
ACTS = "ACT ? [ACT.kind, ACT.placeId] : null"

def run(path):
    out = {}
    with sync_playwright() as pw:
        g = Game(pw, path, 390, 844); g.step(3)
        g.ev("setShipNow(1440 * 6 + 10 * 60); machinesNow(); goToDeck(3)"); g.step(5)
        for name, rid, target in [('job', 'oj-d3gym-locker', '3-gym-1'), ('other', 'oj-d3gym-locker', '3-gym-13'), ('nojob', None, '3-gym-1'), ('vent', 'oj-d3gym-vent', '3-gym-2')]:
            g.ev(f"({MK})({json.dumps(rid)})"); g.ev(f"({PUT})('{target}')"); g.step(60)
            a = g.ev(f"({AIM})('{target}')"); g.page.mouse.click(*a['xy']); g.step(90)
            out[name] = (a["t"], a["d"], g.ev(ACTS)); out[name + "Toast"] = g.ev("document.getElementById('tt').textContent + ': ' + document.getElementById('tx').textContent")[:90]; g.ev("actEnd(true)")
        pe = [e for e in g.errors if e.startswith('pageerror')]; out['errors'] = pe
        g.close()
    return out

src = pathlib.Path(sys.argv[1]).read_text(); OFF = 'var FIXTAP_ON = false;'
if OFF not in src: print('FAIL no FIXTAP_ON switch line in this build'); sys.exit(1)
on = WORK / 'test' / f'_fixtap_on_{os.getpid()}.html'; on.parent.mkdir(parents=True, exist_ok=True); on.write_text(src.replace(OFF, 'var FIXTAP_ON = true;', 1))
try:
    A = run(sys.argv[1]); print('off:', A)
    check(A['job'][2] and A['job'][0] == 'Treadmills' and A['job'][2][0] == 'gym', f"switch off: the treadmill by the locker job's stop starts a run, not the job, as before: {A['job']}")
    B = run(str(on)); print('on: ', B)
    check(B['job'][2] and B['job'][2][0] in ('ixStop', 'job'), f"switch on: the treadmill by the stop starts the job: {B['job']}")
    check(B['other'][0] == 'Punch bag' and B['other'][2] and B['other'][2][0] == 'gym' and B['other'][2][1] == '3-gym-13' and B['other'] == A['other'], f"switch on: another thing in the gym (the punch bag) is still itself, as off: {B['other']} {A['other']}")
    check(B['vent'] == A['vent'] and B['ventToast'] == A['ventToast'], f"switch on: another job (the gym vent, its stop also a treadmill; not in FIXTAP_ROWS): a tap on Treadmills does just what it does off: {B['vent']} {B['ventToast']!r}")
    check(B['nojob'][2] and B['nojob'][2][0] == 'gym' and B['nojob'][2] == A['nojob'][2], f"switch on: with no job the treadmill is a run, as off: {B['nojob']} {A['nojob']}")
    check(not A['errors'] and not B['errors'], f"no page errors: {A['errors']} {B['errors']}")
finally:
    on.unlink(missing_ok=True)
print('FIX TAP PROBE OK' if ok else 'FIX TAP PROBE FAILED')
sys.exit(0 if ok else 1)
