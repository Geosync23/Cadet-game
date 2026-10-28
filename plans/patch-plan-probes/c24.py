from pp import *
g = start('?nosave&debug')
g.step(5)
print(g.ev(r"""(() => { const out = []; for (const p of schedPeople()) if (/store/i.test(p.role)) out.push([p.id, p.rank, p.role, p.shift, planDay(p, 1).filter(s => s.act === 'work').map(s => [hhmm(s.from%1440), hhmm(s.to%1440), s.placeId || s.place, s.tag]).slice(0,4)]); return out; })()"""))
g.close()
