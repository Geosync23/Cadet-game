# #8 (patch builder B): Deck 4 from 07:30 on Day 1 (Dev mode's suggestion), sampling every 2 real s for 60 s: the
# toilets in use (placeBusy) against the red caps showing, and the draw calls; a shot when one shows.
from pp import *
g = start('?nosave&debug')
g.step(5)
g.ev("(() => { skipTo(450); goToDeck(4); const sp = placeSpot('4-toilet-p1'); player.obj.position.copy(cellPos(...sp.walk)); player.obj.position.x += 1.5; target.copy(player.obj.position).setY(.7); return 1; })()")
g.secs(1)
shot = False; agree = 0; n = 0; seen = 0
for i in range(30):
    g.secs(2)
    r = g.ev(r"""(() => { const L = typeof STALL_CAP === 'undefined' ? [] : STALL_CAP.list; return [clockText(), L.length, L.filter(c => c.id).map(c => [c.id, placeBusy(c.id), c.m.visible]), renderer.info.render.calls]; })()""")
    n += 1; ok = all(b == v or (b and not v) for _, b, v in r[2]); agree += ok
    if any(v for _, _, v in r[2]): seen += 1
    if i % 5 == 0 or (not shot and any(v for _, _, v in r[2])): print(r)
    if not shot and any(v for _, _, v in r[2]): g.snap('08-red-light-deck4'); shot = True
print('samples', n, 'never shown while free', agree, 'samples with a red light', seen, g.errors[:3])
g.close()
