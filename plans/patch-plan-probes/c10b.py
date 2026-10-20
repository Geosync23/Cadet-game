from pp import *
g = start('?nosave&debug')
g.step(5)
g.ev("(() => { skipTo(1080 + 7); goToDeck(3); player.obj.position.copy(cellPos(20, 13)); target.copy(player.obj.position).setY(.7); return 1; })()")
g.secs(2)
pairs = {}
best = None
for i in range(70):
    g.secs(1.5)
    r = g.ev(r"""(() => { const W = DECK_CREW.filter(a => a.pose === 'walk'); const out = [];
      for (let i = 0; i < W.length; i++) for (let j = i + 1; j < W.length; j++) { const d = Math.hypot(W[i].x - W[j].x, W[i].z - W[j].z); if (d < .3) out.push([W[i].p.id + '/' + W[j].p.id, +d.toFixed(2), cellAt(W[i].x, W[i].z)]); }
      return [clockText(), W.length, out]; })()""")
    for k, d, c in r[2]:
        pairs.setdefault(k, []).append(i)
    if r[2] and best is None and i > 10:
        pass
long = sorted(((k, len(v), v[0], v[-1]) for k, v in pairs.items()), key=lambda x: -x[1])
print('pairs within 0.3 tiles while walking (count of 0.5 s samples):', long[:10], 'of', len(pairs))
print(g.ev('clockText()'))
g.close()
