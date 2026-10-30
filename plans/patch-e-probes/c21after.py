import sys; sys.path.insert(0, '/home/user/Cadet-game/plans/patch-plan-probes')
from pp import *
g = start('?nosave&debug&rankcard'); g.step(5)
g.ev("(() => { skipTo(600); goToDeck(3); player.obj.position.copy(cellPos(33, 15)); target.copy(player.obj.position).setY(.7); return 1; })()")
g.secs(3)
print(g.ev("(() => { const a = DECK_CREW.find(a => a.p.id === 'esposito-yara'); a.talking = 6; return chatOpen(a.p); })()")); g.secs(1)
print(repr(g.ev("document.getElementById('chat').innerText")))
g.page.screenshot(path=sys.argv[1] + '/21-after.png')
for id in ['marrow','vance','sato','holt']:
    print(id, g.ev(f"rankCardRole(SOC.crew[SOC.idx.get('{id}')])"))
print(g.ev("[...new Set(SOC.crew.map(p => rankCardRole(p)))].slice(0, 12)"))
g.ev("chatClose()")
print(g.errors[:3]); g.close()
