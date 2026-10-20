# PR2: batch C's end of training day (#18/#19) and Zeke's gap (#17) at 390x844
import pp
from b1_common import *
pp.SHOTS = '/tmp/rv/shots'
g = start(); to_day1(g, 8*60+40)
g.page.add_style_tag(content='.bub{animation:none!important}')
g.ev("""(() => { window.__said = []; const old = bubbleSay; bubbleSay = function (h, text, s) { const a = DECK_CREW.find(x=>x.h===h); window.__said.push([clockText(), a&&a.p?a.p.id:'?', text]); return old.apply(this, arguments); }; return true; })()""")
tele(g, 5, [20, 4])
for i in range(40):
    g.secs(2); g.ev(DLG)
    if g.ev("SHIP.time.min") >= 9*60+16: break
g.ev("careerClock()"); g.secs(1)
g.ev("skipTo((SHIP.time.day - 1) * 1440 + 16 * 60 + 40)"); tele(g, 5, [20, 8]); g.secs(1)
Z = "(() => { const a = DECK_CREW.find(x => x.p && x.p.id === 'torres-zeke'), p = player.obj.position; return a ? [deckDef.num, +Math.hypot(a.x-p.x, a.z-p.z).toFixed(2), a.esc || null, a.pose] : null; })()"
shots = set(); mind = 99
for k in range(400):
    g.step(15); g.ev(DLG)
    r = g.ev(GOAL); z = g.ev(Z)
    if z and z[0] == 5 and z[2]: mind = min(mind, z[1])
    said = [s for s in g.ev('window.__said') if s[1] == 'torres-zeke' and s[0] >= 'Day 1, Monday 16:4']
    if said and 'te' not in shots: shots.add('te'); g.snap('rvC_trainend'); print('TRAINEND', said[-1], z, flush=True)
    if r['want'] == 'clockout' and 'co' not in shots: g.secs(1); shots.add('co'); g.snap('rvC_clockout'); print('CLOCKOUT', g.ev(GOAL), flush=True); g.ev("careerClock()"); g.secs(2); print('after clock', g.ev(GOAL), g.ev("DIALOGUE && DIALOGUE.id"), flush=True)
    if r['want'] == 'beam' and 'bm' not in shots:
        g.secs(1); shots.add('bm'); g.snap('rvC_beam'); print('BEAM', g.ev(GOAL), flush=True)
    if k % 20 == 0: print(r, z, flush=True)
    if g.ev("SHIP.time.min") > 17*60+15: break
print('said:', [s for s in g.ev('window.__said') if s[1] == 'torres-zeke'][-5:])
print('min Zeke gap while escorting', mind, 'errors', g.errors[:3])
g.close()
