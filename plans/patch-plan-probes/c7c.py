from pp import *
g = start('?nosave&debug')
g.step(5)
M = r"""(() => { const p = ROSTER.find(x => x.id === 'marrow'); let m = 0, v = 0, lastTo = -99, play=0; for (let d = 1; d <= 28; d++) for (const s of planDay(p, d)) if (s.deck === 4 && s.act !== 'commute' && s.act !== 'sleep') { m += s.to - s.from; if (s.from - lastTo > 5) v++; lastTo = s.to; if (s.tag==='play'||/piano/.test(s.tag||'')) play+=s.to-s.from; } return [Math.round(m / 4 / 6) / 10, v / 4, Math.round(play/4/6)/10]; })()"""
print('now (4 weeks avg: h/week, visits/week, playing h/week)', g.ev(M))
print('no music habit', g.ev("(() => { const p = ROSTER.find(x => x.id === 'marrow'); p.habits = p.habits.filter(h => h !== 'music'); SHIP_DAYS.clear(); return 1; })()"), g.ev(M))
g.close()
