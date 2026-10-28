from b1_common import *
g = start(); to_day1(g, 8*60+40)
tele(g, 5, [20, 4])
for i in range(40):
    g.secs(2); g.ev(DLG)
    if g.ev("SHIP.time.min") >= 9*60+16: break
g.ev("careerClock()"); g.secs(1)
g.ev("skipTo((SHIP.time.day - 1) * 1440 + 16 * 60 + 58)"); tele(g, 5, [12, 4]); g.secs(1)
print(g.ev("eventsOn(1).map(e => e.id + ' ' + e.from + '-' + e.to)"))
P = r"""(() => { const gl = goalNow(); let w = gl && deckDef.num === gl.deck ? ixGoalWorld(gl) : null;
  const v = new THREE.Vector3(); const pr = (x, y, z) => { v.set(x, y, z).project(camera); return [Math.round((v.x + 1) * innerWidth / 2), Math.round((1 - v.y) * innerHeight / 2)]; };
  const it = ITEMS.find(i => i.t === 'Your name') || null; let yn = null; if (it) { const q = new THREE.Vector3(); it.hit.getWorldPosition(q); yn = [q.x.toFixed(2), q.y.toFixed(2), q.z.toFixed(2), pr(q.x, q.y, q.z)]; }
  const beam = ITEMS.find(i => i.t === 'The beam'); let bm = null; if (beam) { const q = new THREE.Vector3(); beam.hit.getWorldPosition(q); bm = [q.x.toFixed(2), q.y.toFixed(2), q.z.toFixed(2), pr(q.x, q.y, q.z)]; }
  const sp = placeSpot('5-beam-1');
  return { t: clockText(), tj: TJ_NOW ? TJ_NOW.e.id : null, goal: gl && gl.label, goalWorld: w && [w.x.toFixed(2), w.z.toFixed(2)], arrowAt: w && pr(w.x, 1.2, w.z), beamCentre: bm, beamSpot: sp && [sp.x.toFixed(2), sp.z.toFixed(2)], nameSlot0: (() => { const s = BEAM.slots[0]; return s; })(), yourName: yn, el: document.getElementById('ixGoal').style.transform }; })()"""
shot = 0
for k in range(60):
    g.secs(2); g.ev(DLG)
    r = g.ev(P)
    if k % 3 == 0 or (r['tj'] and shot == 0): print(r)
    if r['tj'] and shot == 0 and r['goal'] and 'beam' in r['goal'].lower(): g.secs(1); g.snap('19-beam-arrow'); shot = 1; print('SHOT', g.ev(P))
    if g.ev("SHIP.time.min") > 17*60+20: break
g.close()
