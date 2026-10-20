# patch #24 probe: the storekeeper's Buy something menu. GAME=..., Q='&shopmenu'
import sys, os; sys.path.insert(0, '/home/user/Cadet-game/plans/patch-plan-probes')
from pp import *
OUT = sys.argv[1] if len(sys.argv) > 1 else '/tmp'
g = start('?nosave&debug' + os.environ.get('Q', '')); g.step(5)
g.ev("(() => { skipTo(15*60); goToDeck(3); player.obj.position.copy(cellPos(33, 15)); target.copy(player.obj.position).setY(.7); return 1; })()")
g.secs(4)
clerk = g.ev("(() => { const a = DECK_CREW.find(a => a.goalId === '3-store-1'); return a ? [a.p.id, a.settled] : null; })()"); print('at the counter:', clerk)
g.ev("SHIP.player.credits = 5")
print(g.ev(f"(() => {{ const a = DECK_CREW.find(a => a.p.id === '{clerk[0]}'); a.talking = 6; return chatOpen(a.p); }})()")); g.secs(1)
print(repr(g.ev("document.getElementById('chat').innerText")))
has = g.ev("[...document.querySelectorAll('#chat button')].some(b => /buy something/i.test(b.innerText))"); print('Buy something button:', has)
if has:
    g.page.locator('#chat button', has_text=re.compile('buy something', re.I)).click(); g.step(3)
    print(g.ev("document.getElementById('shopMenu').innerText.replace(/\\n+/g, ' | ')"))
    print('greyed:', g.ev("[...document.querySelectorAll('#shopMenu button.act')].filter(b => b.disabled).length"), 'of', g.ev("document.querySelectorAll('#shopMenu button.act').length"))
    g.page.screenshot(path=OUT + '/24-menu.png')
    before = g.ev("({ c: SHIP.player.credits, h: Math.round(SHIP.player.needs.hunger) })")
    g.page.locator('#shopMenu button.act', has_text=re.compile('dried apple', re.I)).click(); g.step(3)
    for k in range(12):
        g.secs(2); a = g.ev("ACT ? ACT.kind + ':' + ACT.phase : null")
        if not a: break
    print('before', before, 'after', g.ev("({ c: SHIP.player.credits, h: Math.round(SHIP.player.needs.hunger), bought: SHIP.player.bought, basket })"), 'toast', g.ev("(document.getElementById('toast')||{}).textContent"))
# someone not at the counter: no button
other = g.ev("(() => { const a = DECK_CREW.find(a => a.goalId !== '3-store-1' && a.p.dept !== 'guest'); a.talking = 6; chatOpen(a.p); return a.p.id; })()"); g.secs(1)
print('not a clerk', other, g.ev("[...document.querySelectorAll('#chat button')].some(b => /buy something/i.test(b.innerText))"))
print('errors', g.errors[:5]); g.close()
