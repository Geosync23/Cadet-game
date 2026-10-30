from pp import *
g = start('?nosave&debug')
g.step(5)
v = g.ev(r"""(() => { const out = []; for (const p of schedPeople()) for (const s of planDay(p, 1)) if (s.deck === 3 && s.tag === 'toilet' && s.from % 1440 > 420) out.push([s.from, s.to, p.id, s.placeId || s.place]); out.sort((a,b)=>a[0]-b[0]); return out.slice(0, 6); })()""")
print(v)
t0 = v[0][0]
g.ev(f"(() => {{ skipTo({t0} - 3); goToDeck(3); player.obj.position.copy(cellPos(20, 19)); target.copy(player.obj.position).setY(.7); return 1; }})()")
for i in range(16):
    g.secs(2)
    r = g.ev(r"""(() => { const out = []; for (const a of DECK_CREW) { const c = cellAt(a.x, a.z); if (c[1] >= 19 && c[0] >= 16 && c[0] <= 23) out.push([a.p.id, c, a.state || a.mode || '', a.placeId || (a.seg && a.seg.placeId) || '']); } return [clockText(), out]; })()""")
    print(r)
    if i in (3, 5): g.snap('08-washroom-light-deck3-%d' % i); print(g.ev("['3-toilet-1','3-toilet-2'].map(id => !!heldBy(id))"))
g.close()
