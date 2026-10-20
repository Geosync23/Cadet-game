# PR2: #31 a real screen tap on Zeke on the ramp at 390x844: no panel, no chat card
import pp
from pp import *
pp.SHOTS = '/tmp/rv/shots'
g = start(); g.step(10)
g.page.add_style_tag(content='.bub{animation:none!important}')
sign(g); g.secs(6)
g.ev("(() => { window.__taps = []; const o = introTap; introTap = function (p) { const r = o.apply(this, arguments); window.__taps.push([p && p.id, r]); return r; }; return 1; })()")
PROJ = "(() => { const a = DECK_CREW.find(x => x.p && x.p.id === 'torres-zeke'); if (!a) return null; const v = new THREE.Vector3(a.x, 1.0, a.z).project(camera); return [Math.round((v.x + 1) * innerWidth / 2), Math.round((1 - v.y) * innerHeight / 2), SHIP.intro.step, clockText()]; })()"
for i in range(3):
    r = g.ev(PROJ); print('zeke at', r)
    g.page.touchscreen.tap(r[0], r[1]); g.step(3); g.secs(1)
    st = g.ev("({ taps: window.__taps.slice(), dlg: typeof DIALOGUE !== 'undefined' && DIALOGUE ? DIALOGUE.id : null, chat: typeof CHAT !== 'undefined' && CHAT ? (CHAT.id || CHAT.who || true) : null, panels: [...document.querySelectorAll('.dlg, #dlg, #chat, .chat')].filter(e => e.offsetParent).length, said: bubbles.list.map(b => b.text.slice(0, 40)), step: SHIP.intro.step })")
    print('after tap', i, st)
    g.snap('rv31_tap%d' % i)
print('errors', g.errors[:3]); g.close()
