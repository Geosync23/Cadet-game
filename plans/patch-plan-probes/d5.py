from pp import *
g = start('?nosave&debug')
g.step(10)
print(g.ev(STATE))
# list hatch/closed edges per deck that the player can't pass, with room names either side
for n in [1,2,3,4,5,6,7]:
    g.ev(f"goToDeck({n})"); g.step(5)
    r = g.ev(r"""(() => { const out=[]; for (const [k,e] of EDGES) { if (e.type==='hatch'||e.type==='closed') { const [h,a,b]=k.split(','), i=+a,j=+b; const rs=(h==='h'?[roomAt(i,j-1),roomAt(i,j)]:[roomAt(i-1,j),roomAt(i,j)]).map(x=>x&&ROOMS[x]?ROOMS[x].name:x); out.push([k,e.type,e.service?'svc'+(e.tier||0):'', edgeBlocks(e,'player')?'BLOCK':'pass', rs.join(' | ')]); } } return out; })()""")
    print('Deck', n)
    for x in r: print('  ', x)
g.close()
