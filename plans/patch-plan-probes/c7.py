from pp import *
g = start('?nosave&debug')
g.step(5)
r = g.ev(r"""(() => { const p = ROSTER.find(x => x.id === 'marrow'); const out = [];
 for (let d = 1; d <= 14; d++) { const segs = planDay(p, d); const d4 = segs.filter(s => s.deck === 4);
   out.push([d, WEEKDAYS[weekday(d)], d4.reduce((a, s) => a + (s.to - s.from), 0), d4.map(s => [hhmm(s.from % 1440), hhmm(s.to % 1440), s.act, s.place || s.tag || ''].join(' '))]); }
 return out; })()""")
for x in r: print(x)
print(g.ev("JSON.stringify(planDay(ROSTER.find(x => x.id === 'marrow'), 1).map(s => [hhmm(s.from%1440), hhmm(s.to%1440), s.deck, s.act, s.place, s.tag]))"))
g.close()
