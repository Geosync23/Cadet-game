from pp import *
g = start('?nosave&debug')
g.step(5)
g.ev("(() => { skipTo(533); goToDeck(3); player.obj.position.copy(cellPos(20, 19)); target.copy(player.obj.position).setY(.7); return 1; })()")
for i in range(8):
    g.secs(3)
    print(g.ev(r"""(() => [clockText(), DECK_CREW.filter(a => /toilet/.test(a.goalId || '')).map(a => [a.p.id, a.goalId, !!a.settled, Object.keys(a).join(',')])])()"""))
g.close()
