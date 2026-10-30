from pp import *
g = start(); g.step(10); sign(g); g.secs(2)
g.ev("""(() => { for (let t = shipNow(); t <= 20*60+30; t++) { setShipNow(t); introAdvance(t, null); } })()""")
g.ev("skipTo(1440 + 8*60+30)")
print(g.ev("(() => { const S = schedData(); const q = S.byId.get('5-aisle-1'); return JSON.stringify([q && q.room, q && q.at, q && q.type, S.deskOf('5-office-1')]); })()"))
print(g.ev("JSON.stringify(ROSTER.filter(p => (p.looks||{}).hairColor && /red|ginger|auburn|copper/.test(p.looks.hairColor)).map(p => [p.id, p.looks.hairColor, p.dept, p.role]))"))
g.ev("goToDeck(5)"); g.step(5)
for i in range(18):
    g.shipmins(2)
    print(g.ev(r"""(() => { const a = DECK_CREW.find(x => x.p.id==='calder'); const off = DECK_CREW.filter(x => { const r = roomAt(...cellAt(x.x,x.z)); return r==='o'; }).map(x => [x.p.id, x.p.looks.hairColor]); return clockText() + ' calder ' + (a ? JSON.stringify([cellAt(a.x,a.z), (ROOMS[roomAt(...cellAt(a.x,a.z))]||{}).name, a.mode||a.state||'']) : 'not on deck') + ' office: ' + JSON.stringify(off); })()"""))
