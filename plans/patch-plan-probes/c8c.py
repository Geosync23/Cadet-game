from pp import *
g = start('?nosave&debug')
g.step(5)
g.ev("(() => { skipTo(533); goToDeck(3); player.obj.position.copy(cellPos(20, 19)); target.copy(player.obj.position).setY(.7); return 1; })()")
for i in range(40):
    g.secs(0.5)
    r = g.ev(r"""(() => { const a = DECK_CREW.find(a => a.p.id === 'tomas'); if (!a) return clockText() + ' -'; return [clockText(), SHIP.time.min.toFixed(2), cellAt(a.x, a.z), a.goalId, a.settled, a.path ? a.path.length : null, a.spot && a.spot.walk, a.pose]; })()""")
    if i % 2 == 0: print(r)
print(g.ev("CREW_SPEED"))
g.close()
