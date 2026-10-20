from b1_common import *
g = start(); to_day1(g, 8*60+40)
tele(g, 5, [20, 4])
for i in range(40):
    g.secs(2); g.ev(DLG)
    if g.ev("SHIP.time.min") >= 9*60+16: break
g.ev("careerClock()"); g.secs(1)
print(g.ev("(() => { const id = jobReserved(1); const j = SHIP.jobs.find(x => x.id === id); return id ? [id, j.kind, j.title, j.machine, claimJob(id), (SHIP.player.track = id)] : 'none'; })()"))
D = "(() => { const a = DECK_CREW.find(x => x.p && x.p.id === INTRO_ESCORT); if (!a || deckDef.num !== a.deck && a.deckNum !== undefined) return null; const b = (ACT && ACT.body && ACT.body.obj) ? ACT.body.obj.position : player.obj.position; return a ? [Math.hypot(a.x - b.x, a.z - b.z), a.esc, a.pose, !!ACT && ACT.kind + ':' + ACT.phase] : null; })()"
# walk the job with tap-to-walk: each tick go to the goal's tile; when there, tap-equivalents
STEP = r"""(() => {
  const gl = goalNow(); if (!gl) return 'nogoal';
  if (ACT) return 'act ' + ACT.kind + ' ' + ACT.phase + ' ' + (ACT.done||0).toFixed(1);
  if (gl.deck !== deckDef.num) { goToDeck(gl.deck); return 'deck ' + gl.deck; }
  const w = ixGoalWorld(gl); if (!w) return 'noworld ' + gl.label;
  const c = cellAt(w.x, w.z), pp = player.obj.position, d = Math.hypot(w.x - pp.x, w.z - pp.z);
  if (d < 1.3 && !player.path.length) {
    if (gl.place && PLACE_OF.has(gl.place)) { const it = ITEMS.slice().sort((p, q) => { const a = new THREE.Vector3(), b = new THREE.Vector3(); p.hit.getWorldPosition(a); q.hit.getWorldPosition(b); return Math.hypot(a.x - w.x, a.z - w.z) - Math.hypot(b.x - w.x, b.z - w.z); })[0];
      const at = new THREE.Vector3(); it.hit.getWorldPosition(at); for (const f of PLAYER_TAPS) { try { if (f(it, at)) return 'tapped ' + it.t; } catch (e) { return 'err ' + e; } } return 'notap ' + it.t; }
    const it = ITEMS.find(i => gl.item && gl.item.test(i.t)); if (it) { const at = new THREE.Vector3(); it.hit.getWorldPosition(at); for (const f of PLAYER_TAPS) { try { if (f(it, at)) return 'tapped ' + it.t; } catch (e) {} } return 'notap item'; }
    return 'there ' + gl.label;
  }
  if (!player.path.length) { let t = c; if (!free(...t)) t = nearestOpen(w.x, w.z, player) || t; return player.goTo(t) ? 'walk ' + gl.label : 'nopath ' + gl.label; }
  return 'walking ' + gl.label;
})()"""
close = []; last = None; shots = 0; had = False
for k in range(600):
    g.step(10); g.ev(DLG)
    s = g.ev(STEP); d = g.ev(D)
    if s != last: print(g.ev("clockText()"), s, d and [round(d[0],2)] + d[1:]); last = s
    if d and d[0] < 0.4:
        close.append((g.ev("clockText()"), round(d[0], 2), d[3], s))
        if shots < 2 and d[0] < 0.25: g.snap('17-zeke-overlap-%d' % shots); shots += 1
    if s == 'nogoal' and k > 50 and had: break
    had = had or s != 'nogoal'
print('frames-ish under 0.4 m:', len(close))
for c in close[:40]: print(c)
g.close()
