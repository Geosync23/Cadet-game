# Starship Cadet: bench press probe (0.92.6 #6, the user's: "weight not parallel with the ground, doesn't line up with
# the hands"; a one-off targeted check, kept next to the other checks)
# Poses you (a FullPerson, as your activities are drawn) and one crew member (the crowd) in the bench press ('lie:bench') through a whole lift, 24 moments, and measures the held
# bar from its holder: both ends at the same height (level) and each grip on the bar (its distance from the bar's line).
# Run:  python3 bench_probe.py BUILD.html
import sys, json
exec(open(__file__.replace('bench_probe.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
ok = True
def check(cond, msg):
    global ok
    print('ok  ' if cond else 'FAIL', msg)
    if not cond: ok = False
    return cond
PROBE = """(who) => {
  const o = who === 'you' ? new FullPerson(PLAYER_SPEC, 'you') : crowd.people.find(p => p.rig && p.propBones); if (!o) return null;   // your activities are drawn by a FullPerson (actStart's A.body)
  const pos = (o.pos && o.pos.y) || .5, out = [];
  o.fresh = true; animateActivity(o, 'lie:bench', 1 / 30, 0, 0, pos);
  for (let f = 0; f < 120; f++) animateActivity(o, 'lie:bench', 1 / 30, f / 30, 0, pos);   // settle into the pose
  const arms = o.rig.arms, aR = arms[0].side < 0 ? arms[0] : arms[1], aL = aR === arms[0] ? arms[1] : arms[0];
  for (let k = 0; k < 24; k++) {
    const t = 4 + k * (2 * Math.PI / 1.5) / 24;           // one press: ACTS.bench runs at t * 1.5
    animateActivity(o, 'lie:bench', 1 / 30, t, 0, pos);
    o.rig.root.rotation.set(-Math.PI / 2, .7, 0);         // lying, turned some way, as the crowd and the player do
    o.rig.root.updateMatrixWorld(true);
    const hold = o.propBones ? o.propBones[0] : (o.propMeshes || []).find(m => m.parent === aR.hand);
    if (!hold) { out.push(null); continue; }
    const a = hold.localToWorld(new THREE.Vector3(-.75, 0, 0)), b = hold.localToWorld(new THREE.Vector3(.75, 0, 0));
    const gr = aR.hand.localToWorld(new THREE.Vector3(0, -.055, .01)), gl = aL.hand.localToWorld(new THREE.Vector3(0, -.055, .01));
    const line = new THREE.Line3(a, b), off = p => { const c = new THREE.Vector3(); line.closestPointToPoint(p, true, c); return c.distanceTo(p); };
    out.push({ tilt: Math.abs(a.y - b.y), gr: off(gr), gl: off(gl), y: (a.y + b.y) / 2 });
  }
  if (who === 'you' && o.dispose) o.dispose();
  return out; }"""
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 900, 760)
    g.ev("goToDeck(3)"); g.step(5)
    for who in ['you', 'crew']:
        r = g.ev("(" + PROBE + ")(" + json.dumps(who) + ")")
        if not check(r and all(r), f'{who}: a held bar through the lift ({"none" if not r else sum(1 for x in r if x)} of 24 moments)'): continue
        tilt, grip, ys = max(x['tilt'] for x in r), max(max(x['gr'], x['gl']) for x in r), [x['y'] for x in r]
        print(f'    {who}: worst tilt {tilt * 100:.2f} cm end to end, worst grip off the bar {grip * 100:.2f} cm, the bar travels {(max(ys) - min(ys)) * 100:.1f} cm')
        check(tilt < .01, f'{who}: the bar stays level (ends within 1 cm of the same height)')
        check(grip < .03, f'{who}: both hands stay on the bar (each grip within 3 cm of it)')
        check(max(ys) - min(ys) > .05, f'{who}: the bar goes down and up with the press')
    check(not g.errors, f'no console errors ({g.errors[:3]})')
    g.close()
print('BENCH PROBE OK' if ok else 'BENCH PROBE FAILED')
sys.exit(0 if ok else 1)
