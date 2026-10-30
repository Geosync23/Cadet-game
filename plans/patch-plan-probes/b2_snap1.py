from pp import *
g = start(); g.step(10); sign(g); g.secs(2)
g.ev("""(() => { for (let t = shipNow(); t <= 20*60+30; t++) { setShipNow(t); introAdvance(t, null); } })()""")
g.ev("skipTo(1440 + 7*60+40)")
g.ev("goToDeck(5)"); g.step(5)
g.ev("(() => { player.obj.position.copy(cellPos(12,2)); target.copy(player.obj.position).setY(.7); })()")
for i in range(40):
    g.shipmins(2)
    s = g.ev(r"""(() => { const off = DECK_CREW.filter(x => roomAt(...cellAt(x.x,x.z))==='o').map(x => x.p.id); const c = DECK_CREW.find(x=>x.p.id==='calder'); return [clockText(), off, c ? (ROOMS[roomAt(...cellAt(c.x,c.z))]||{}).name : null, DIALOGUE && DIALOGUE.id]; })()""")
    print(s)
    if s[0].endswith('08:46') or s[0].endswith('08:47'): g.snap('01-day2-office-no-calder')
    if s[3]: g.snap('01-day2-meeting-without-calder'); break
