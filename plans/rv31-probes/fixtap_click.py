# RV31: real screen clicks on things near a small job's stop, with the job yours and without, OFF.html then ON.html.
# Run from the repo root: python3 plans/rv31-probes/fixtap_click.py OFF.html ON.html
# Starship Cadet: a tap on the thing at your small job's stop (FX30 for lead 49, backlog JB2-2, 0.99.6; a one-off
# targeted check, kept next to the others). "Unstick a gym locker" (oj-d3gym-locker) stops at 3-gym-1, a treadmill.
# With the job yours, a real screen click on that treadmill:
#   on the build as it is (FIXTAP_ON off): starts a run (gym), not the repair, as backlog JB2-2 says;
#   on a copy with FIXTAP_ON on: starts the job's step (ixStop). The only tappable treadmill, "Treadmills", stands on
#   3-gym-2, next to the stop: a click on it is the job; a click on another thing in the gym (the punch bag, 3-gym-13)
#   is still that thing; with no job, "Treadmills" is a run as before.
# Run:  python3 fixtap_probe.py BUILD.html
import sys, json, os, pathlib
exec(open('cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
ok = True
def check(cond, msg):
    global ok
    print('ok  ' if cond else 'FAIL', msg)
    if not cond: ok = False
    return cond

MK = r"""((rid) => { actEnd(true); for (const j of SHIP.jobs) if (j.claimedBy === 'you' && j.status === 'claimed') { j.claimedBy = null; j.status = 'open'; }
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


AIMT = r"""((pid, title) => { const s = placeSpot(pid), b = new THREE.Box3(), c = new THREE.Vector3();
  const its = ITEMS.filter(i => i.hit && i.t === title).map(i => { b.setFromObject(i.hit); b.getCenter(c); return [i, c.clone(), b.distanceToPoint(new THREE.Vector3(s.x, c.y, s.z))]; }).sort((m, n) => m[2] - n[2]);
  if (!its.length) return null; const [it, p] = its[0], v = p.clone().project(camera); return { t: it.t, d: Math.round(its[0][2] * 100) / 100, xy: [(v.x + 1) / 2 * innerWidth, (1 - v.y) / 2 * innerHeight] }; })"""
CASES = [(5, 'w5-tap', '5-basin-1', 'Toilet'), (4, 'la-lint', '4-laundry-3', 'Washer 3'), (4, 'jc-kettle', '4-common-kettle', 'Kettle'), (3, 'gy-bench', '3-gym-5', 'Punch bag'), (4, 'jc-lamp', '4-common-5', 'Chore rota')]
def run(path):
    out = {}
    with sync_playwright() as pw:
        g = Game(pw, path, 390, 844); g.step(3); g.ev("setShipNow(1440 * 6 + 10 * 60); machinesNow()")
        for deck, rid, pid, title in CASES:
            g.ev(f"goToDeck({deck})"); g.step(5)
            for withjob in (True, False):
                g.ev(f"({MK})({json.dumps(rid if withjob else None)})"); g.ev(f"({PUT})('{pid}')"); g.step(60)
                a = g.ev(f"({AIMT})('{pid}', {json.dumps(title)})")
                if not a: out[(rid, withjob)] = None; continue
                g.page.mouse.click(*a['xy']); g.step(90)
                out[(rid, withjob)] = (a['t'], a['d'], g.ev(ACTS), g.ev("SHIP.player.toast || (document.querySelector('#toast') || {}).textContent || ''")[:80]); g.ev("actEnd(true)")
        out['errors'] = [e for e in g.errors if e.startswith('pageerror')]; g.close()
    return out
import sys
for name, b in (('off', sys.argv[1]), ('on', sys.argv[2])):
    o = run(b)
    for k, v in o.items(): print(name, k, v)
