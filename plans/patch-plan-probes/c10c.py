# #10's pass mark (patch builder B): c10's scene (Deck 3 at dinner, Day 1 from 18:07, 120 real s, a sample every 0.5 s),
# counting for each pair of walkers the longest unbroken run of samples within 0.3 tiles: by their tile position
# (a.x, a.z) and by where the body is drawn (plus the lane, a.lx/a.lz, when the build has it).
# Pass: no pair over 3 real seconds (6 samples).
from pp import *
g = start('?nosave&debug')
g.step(5)
g.ev("(() => { skipTo(1080 + 7); goToDeck(3); player.obj.position.copy(cellPos(20, 13)); target.copy(player.obj.position).setY(.7); return 1; })()")
g.secs(2)
run = {'tile': {}, 'drawn': {}}; best = {'tile': {}, 'drawn': {}}; walkers = 0
for i in range(240):
    g.secs(0.5)
    r = g.ev(r"""(() => { const W = DECK_CREW.filter(a => a.pose === 'walk'); const out = { tile: [], drawn: [] };
      for (let i = 0; i < W.length; i++) for (let j = i + 1; j < W.length; j++) { const a = W[i], b = W[j], k = a.p.id + '/' + b.p.id;
        if (Math.hypot(a.x - b.x, a.z - b.z) < .3) out.tile.push(k);
        if (Math.hypot(a.x + (a.lx || 0) - b.x - (b.lx || 0), a.z + (a.lz || 0) - b.z - (b.lz || 0)) < .3) out.drawn.push(k); }
      out.n = W.length; return out; })()""")
    walkers = max(walkers, r['n'])
    for m in ('tile', 'drawn'):
        now = set(r[m])
        for k in list(run[m]):
            if k not in now: del run[m][k]
        for k in now:
            run[m][k] = run[m].get(k, 0) + 1; best[m][k] = max(best[m].get(k, 0), run[m][k])
for m in ('tile', 'drawn'):
    top = sorted(best[m].items(), key=lambda x: -x[1])
    over = [x for x in top if x[1] > 6]
    print(m + ':', len(top), 'pairs ever within 0.3 tiles; longest runs (samples of 0.5 s):', top[:8], '| over 3 s:', len(over))
print('most walking at once', walkers, g.ev('clockText()'), g.errors[:3])
g.close()
