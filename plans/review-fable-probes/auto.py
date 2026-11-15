# auto.py UNTIL_HHMM: follow arrows by jumps + tapping the pin; stop at dialogue or at the time
import sys, json, subprocess, os
until = sys.argv[1]
def c(cmds):
    r = subprocess.run(['python3', 'c.py', os.environ.get('PORT','7001'), '100000'], input=json.dumps(cmds), capture_output=True, text=True).stdout.strip().split('\n')
    return [json.loads(x) for x in r if x]
TP = """(() => { const t = clockText().slice(-5); if (DIALOGUE) return ['dialogue', t]; const g = goalNow(); if (!g) return ['none', t]; if (DEV.open) deviceClose(); if (ACT && ACT.phase !== 'walk') return ['busy:' + ACT.kind, t, g.label];
  if (deckDef.num !== g.deck) { goToDeck(g.deck); return ['lift', t, g.label]; }
  const w = ixGoalWorld(g); if (!w) return ['nospot', t, g.label]; const p = player.obj.position;
  if (Math.hypot(w.x - p.x, w.z - p.z) > 2.2) { const gl = nearestOpen(w.x, w.z, player); player.obj.position.copy(cellPos(...gl)); player.stop(); return ['tp', t, g.label]; }
  const e = document.getElementById('ixGoal'); const pd = e.children[1]; const r = pd.getBoundingClientRect(); const v = new THREE.Vector3(w.x, w.y || .05, w.z).project(camera);
  return ['tap', t, g.label, e.classList.contains('tap') ? r.left + r.width / 2 : (v.x + 1) / 2 * innerWidth, e.classList.contains('tap') ? r.top + r.height / 2 : (1 - v.y) / 2 * innerHeight]; })()"""
last = None
for k in range(400):
    r = c([['ev', TP]])[0]
    if r[1] >= until and r[1] < '23:59': print('time', r); break
    if r[0] == 'dialogue': print(r); break
    if r[0] == 'tap': c([['tap', r[3], r[4]], ['step', 40]])
    else: c([['step', 40]])
    key = (r[0], r[2] if len(r) > 2 else None)
    if key != last: print(r[:3], flush=True); last = key
