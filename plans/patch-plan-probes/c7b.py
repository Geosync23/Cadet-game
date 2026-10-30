from pp import *
g = start('?nosave&debug')
g.step(5)
r = g.ev(r"""(() => { const out = {};
 const music = []; for (const n in DECKS) for (const q of DECKS[n].places || []) if (q.type === 'music') music.push(q.id);
 out.music = music;
 const P = schedPeople().filter(p => String(p.bed).startsWith('2-'));
 const rows = P.map(p => { let m = 0, v = 0, lastTo = -99, play = 0; for (let d = 1; d <= 14; d++) for (const s of planDay(p, d)) if (s.deck === 4 && s.act !== 'commute' && s.act !== 'sleep') { m += s.to - s.from; if (s.from - lastTo > 5) v++; lastTo = s.to; if (s.tag === 'play' || /piano/.test(s.tag||'')) play += s.to - s.from; } return [p.id, p.rank, p.cabin || p.bed, Math.round(m / 2 / 6) / 10, v / 2, Math.round(play/2/6)/10, (p.habits||[]).join(',')]; });
 rows.sort((a, b) => b[3] - a[3]); out.rows = rows.slice(0, 12); out.n = rows.length;
 out.avg = Math.round(rows.reduce((a, r) => a + r[3], 0) / rows.length * 10) / 10;
 return out; })()""")
print(r['music'], r['n'], 'avg h/week', r['avg'])
for x in r['rows']: print(x)
g.close()
