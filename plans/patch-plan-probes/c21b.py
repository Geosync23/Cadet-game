from pp import *
g = start('?nosave&debug')
g.step(5)
print(g.ev(r"""(() => { const P = schedPeople(), r = {}; for (const p of P) { const k = p.rank; (r[k] = r[k] || []).push(p.role); }
 const out = {}; for (const k in r) out[k] = [r[k].length, [...new Set(r[k])].slice(0, 6)]; return out; })()"""))
print(g.ev(r"""(() => { const till = []; for (const p of schedPeople()) for (const s of planDay(p, 1)) if (s.place === '3-shop-7' || s.placeId === '3-shop-7') till.push([hhmm(s.from%1440), hhmm(s.to%1440), p.id, s.act]); return till.filter(x => x[3] === 'work'); })()"""))
print(g.ev("Object.keys(ROSTER.find(p=>p.id==='esposito-yara')||{}).join(',')"))
g.close()
