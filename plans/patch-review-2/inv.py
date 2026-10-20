import pp
from pp import *
import os
g = start('?nosave&debug&firstlight&mug'); g.step(5)
g.page.add_style_tag(content='.bub{animation:none!important}')
g.ev("skipTo(18*60+20)"); g.ev("goToDeck(3)"); g.step(5)
z = g.ev("(() => { const a = DECK_CREW.find(a => a.p.id === 'torres-zeke'); return a ? [a.x, a.z] : null; })()")
g.ev(f"(() => {{ const c = nearestOpen({z[0]} + .8, {z[1]} + .8, player); player.obj.position.copy(cellPos(...c)); target.copy(player.obj.position).setY(.7); }})()")
g.secs(2)
print(g.ev("(() => { const z = DECK_CREW.find(a => a.p.id === 'torres-zeke'); return bubbles.list.map(b => { const r = b.el.getBoundingClientRect(); return [b.text.slice(0, 30), b.who === z ? 'ACTOR' : b.who === z.h ? 'HANDLE' : 'other', b.el.style.display, Math.round(r.left), Math.round(r.top), typeof z.h, z.h && z.h.pos ? 'h.pos' : 'no h.pos']; }); })()"))
g.ev("(() => { const z = DECK_CREW.find(a => a.p.id === 'torres-zeke'); bubbleSay(z.h, 'FIXED: Cocoa in the bow lounge at eight.'); })()"); g.step(5)
print(g.ev("bubbles.list.map(b => [b.text.slice(0, 20), b.el.style.display])"))
g.page.screenshot(path='/tmp/rv/shots/e26_invite.png'); g.close()
