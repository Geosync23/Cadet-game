from pp import *
g = start(); g.step(10); sign(g); g.secs(2)
g.ev("""(() => { for (let t = shipNow(); t <= 20*60+30; t++) { setShipNow(t); introAdvance(t, null); } })()""")
g.ev("skipTo(1440 + 8*60+20)")
for who in ['calder','silva-bea']:
  print(who, g.ev(f"JSON.stringify(planDay(ROSTER.find(p => p.id==='{who}'), 2).filter(s => s.to > 1440+7*60 && s.from < 1440+10*60).map(s => [hhmm(s.from-1440), hhmm(s.to-1440), s.deck, s.placeId, s.act, s.tag]))"))
print(g.ev("JSON.stringify(ROSTER.find(p => p.id==='silva-bea').looks)"))
print(g.ev("JSON.stringify(ROSTER.find(p => p.id==='calder').looks)"))
print(g.ev("JSON.stringify((DECKS[5].places||[]).filter(q => q.room==='o').map(q => [q.id, q.type, q.at]))"))
print(g.ev("(() => { const S = schedData(); return JSON.stringify((DECKS[5].places||[]).filter(q => q.room==='o').map(q => [q.id, S.owner.get(q.id)||null, !!S.deskOf(q.id), q.machine||null])); })()"))
