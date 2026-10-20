import pp
from pp import *
g = start('?nosave&debug'); g.step(5)
g.ev("skipTo(18*60+40)"); g.ev("goToDeck(3)"); g.step(30)
r = g.ev("""(() => { const P = player.obj.position; const a = DECK_CREW.filter(a => a.h).sort((x, y) => Math.hypot(x.x-P.x,x.z-P.z) - Math.hypot(y.x-P.x,y.z-P.z))[0]; window.__b = bubbleSay(a.h, 'TEST BUBBLE near person here', 4.5); return [a.p.id, a.pose]; })()""")
g.step(20)
print(r, g.ev("(() => { const b = window.__b, q = b.el.getBoundingClientRect(); const e = document.elementFromPoint(q.left + q.width/2, q.top + q.height/2); return [b.el.style.opacity, b.el.style.display, Math.round(q.left), Math.round(q.top), e && (e.id || e.className || e.tagName)]; })()"))
print(g.ev("(() => { const b = window.__b, cs = getComputedStyle(b.el), cc = getComputedStyle(b.card), cv = document.querySelector('canvas'); return [cs.opacity, cs.visibility, cs.transform, cc.opacity, cc.display, b.el.isConnected, bubbles.el.isConnected, getComputedStyle(cv).zIndex, getComputedStyle(cv).position, b.el.parentNode === bubbles.el, document.body.contains(bubbles.el)]; })()"))
g.page.screenshot(path='/tmp/rv/shots/bubq.png'); g.close()
