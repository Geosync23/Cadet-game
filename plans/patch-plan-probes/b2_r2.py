from pp import *
g = start(); g.step(10); sign(g); g.secs(2)
g.ev("""(() => { for (let t = shipNow(); t <= 20*60+30; t++) { setShipNow(t); introAdvance(t, null); } })()""")
g.ev("skipTo(1440 + 8*60+40)"); g.ev("goToDeck(5)"); g.step(5)
W = r"""(() => { const a = DECK_CREW.find(x => x.p.id==='calder'); if (!a) return 'not on deck ' + JSON.stringify(whereIs ? whereIs(ROSTER.find(p=>p.id==='calder')) : null); const c = cellAt(a.x,a.z); return [c, (ROOMS[roomAt(...c)]||{}).name, a.mode||a.state||'', a.seg && a.seg.tag]; })()"""
for i in range(12):
    g.shipmins(2); print(g.ev('clockText()'), g.ev(W))
