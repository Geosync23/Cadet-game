from pp import *
g = start(); g.step(10); sign(g); g.secs(2)
g.ev("""(() => { for (let t = shipNow(); t <= 20*60+30; t++) { setShipNow(t); introAdvance(t, null); } })()""")
g.ev("skipTo(1440 + 8*60+30)")
print(g.ev("(() => { const S = schedData(); return JSON.stringify(S.deskOf('5-office-1')); })()"))
for d in (1,2,3):
  print(d, g.ev(f"JSON.stringify(ROSTER.flatMap(p => planDay(p, {d}).filter(s => /^5-office/.test(s.placeId||'')).map(s => [p.id, (p.looks||{{}}).hairColor, hhmm(s.from-{(d-1)*1440}), hhmm(s.to-{(d-1)*1440}), s.placeId, s.act, s.tag||''])))"))
