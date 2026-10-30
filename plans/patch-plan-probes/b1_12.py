from b1_common import *
g = start(); to_day1(g, 8*60+40)
tele(g, 5, [20, 4])
for i in range(40):
    g.secs(2); g.ev(DLG)
    if g.ev("SHIP.time.min") >= 9*60+16: break
g.ev("careerClock()"); g.secs(1)
Z = "(() => { const a = DECK_CREW.find(x => x.p && x.p.id === INTRO_ESCORT); return a ? { x: +a.x.toFixed(2), z: +a.z.toFixed(2), esc: a.esc || null, settled: !!a.settled, pose: a.pose, talking: a.talking || 0, shuf: shuffleable(a), moving: !!(a.path && a.path.length) } : null; })()"
for i in range(8):
    print(g.ev("clockText()"), g.ev(Z), g.ev("player.here()"))
    g.secs(3)
# head-on and off-axis pushes when he's standing still
res = []
for ang in [0, 8, 20]:
    for tries in range(10):
        z = g.ev(Z)
        if z and not z['moving']: break
        g.secs(2)
    r = g.ev(f"""(() => {{ const a = DECK_CREW.find(x => x.p && x.p.id === INTRO_ESCORT); const th = {ang} * Math.PI / 180;
      // stand 0.9 m east of him, push west (rotated by th)
      const dx = -Math.cos(th), dz = Math.sin(th);
      player.obj.position.set(a.x - dx * .9, 0, a.z - dz * .9); player.path.length = 0; player.goal = null;
      if (!free(...player.here())) return 'blocked start ' + player.here();
      player.steer = {{ x: dx, z: dz, k: 1 }}; window.__p0 = {{ x: a.x, z: a.z, dx, dz }}; return 'ok ' + player.here(); }})()""")
    t = None
    for f in range(150):  # 5 s
        g.ev(f"player.steer = {{ x: window.__p0.dx, z: window.__p0.dz, k: 1 }}")
        g.step(1)
        past = g.ev("(() => { const p = player.obj.position, q = window.__p0; return (p.x - q.x) * q.dx + (p.z - q.z) * q.dz; })()")
        if past > 0.45: t = f / 30; break
    if f == 20 and ang == 0: g.snap('12-pushing-into-zeke')
    res.append((ang, r, t, g.ev(Z)))
    g.ev("endSteer()"); g.secs(1)
for x in res: print(x)
g.close()
