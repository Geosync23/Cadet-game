from pp import *
g = start('?nosave&debug')
g.step(5)
r = g.ev(r"""(() => { const out = { days: [] };
 for (let d = 1; d <= 7; d++) { const P = schedPeople(); let n = 0, ppl = 0, none = 0, byDeck = {}, byHour = {}, place = {}, dur = [];
   for (const p of P) { const t = planDay(p, d).filter(s => s.act === 'wash' && s.tag === 'toilet'); n += t.length; if (!t.length) none++; else ppl++;
     for (const s of t) { byDeck[s.deck] = (byDeck[s.deck] || 0) + 1; const h = Math.floor((s.from % 1440) / 60); byHour[h] = (byHour[h] || 0) + 1; dur.push(s.to - s.from); place[s.place || s.placeId || '?'] = (place[s.place||s.placeId||'?']||0)+1; } }
   out.days.push({ d, crew: P.length, visits: n, none, byDeck, dur: [Math.min(...dur), Math.max(...dur)] });
   if (d === 1) { out.byHour = byHour; out.place = place; }
 }
 const sample = planDay(schedPeople()[3], 1).find(s => s.tag === 'toilet'); out.sample = sample;
 return out; })()""")
for d in r['days']: print(d)
print(r['byHour']); print(r['place']); print(r['sample'])
g.close()
