# PR2's batch B probe: the arrival evening at 390x844. #14 glow/pointer, #3 Chief at the next table, #4 goodnight bubbles + hush.
import pp
from pp import *
import re, json, sys
pp.SHOTS = '/tmp/rv/shots'
src = open(REPO+'/intro_check.py').read()
WALK = re.search(r'WALK_TICK = r"""(.*?)"""', src, re.S).group(1)
WALK2 = WALK.replace("if (DIALOGUE) {", "if (DIALOGUE && !window.__manual) {")
g = start()
g.step(10)
g.ev("""(() => { window.__said = []; const old = bubbleSay; bubbleSay = function (h, text, s) { const a = DECK_CREW.find(x=>x.h===h); window.__said.push([clockText(), SHIP.intro.step, a&&a.p?a.p.id:'?', text]); return old.apply(this, arguments); }; return true; })()""")
sign(g)
CAL = """(() => { const c = DECK_CREW.find(x => x.p && x.p.id === 'calder'); return c ? [cellAt(c.x,c.z), c.pose, c.spot && c.spot.id] : null; })()"""
PT = """(() => { const p = document.getElementById('devPoint'), b = document.getElementById('devBtn'); if (!p) return null; const r = p.getBoundingClientRect(); return { pt: [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)], glow: b.classList.contains('devglow'), dlg: typeof DIALOGUE !== 'undefined' && DIALOGUE ? DIALOGUE.id : null, vw: innerWidth }; })()"""
seen = set(); gnStart = None
for k in range(1400):
    g.step(20)
    st = g.ev("SHIP.intro.step")
    pt = g.ev(PT)
    if pt and 'pt' not in seen: seen.add('pt'); print(g.ev('clockText()'), st, 'POINTER first', pt, flush=True); g.snap('rvB_pointer_first')
    if pt and pt['dlg'] and 'ptd' not in seen: seen.add('ptd'); print('POINTER over a dialogue', pt, flush=True); g.snap('rvB_pointer_dialogue')
    if not pt and 'pt' in seen and 'ptgone' not in seen: seen.add('ptgone'); print(g.ev('clockText()'), 'POINTER gone; booted', g.ev('SHIP.device.booted'), flush=True)
    if st in ('table', 'chief', 'free'): g.ev("window.__manual = true")
    r = g.page.evaluate('([s, m]) => window.__sc(s)(m)', [WALK2, 'stand' if (st in ('chief', 'free') or g.ev('!!DIALOGUE')) else 'follow'])
    d = g.ev("DIALOGUE ? [DIALOGUE.id, DIALOGUE.i, (DIALOGUE.queue[DIALOGUE.i]||{}).who, (DIALOGUE.queue[DIALOGUE.i]||{}).text, !!(DIALOGUE.queue[DIALOGUE.i]||{}).choice] : null")
    if d and g.ev("!!window.__manual"):
        print(r['t'], d[0], d[1], (d[3] or '')[:50], 'calder', g.ev(CAL), flush=True)
        t = (d[3] or '')
        if d[0].startswith('introDinner') and 'din' not in seen: seen.add('din'); g.snap('rvB_dinner_chat')
        if "coming over" in t and 'co' not in seen: seen.add('co'); g.snap('rvB_coming_over')
        if d[0] == 'introChief' and 'ch' not in seen: seen.add('ch'); g.snap('rvB_chief_first')
        g.secs(1)
        if d[4]: g.ev("dialogueChoose(1)")
        else: g.ev("dialogueNext()")
        continue
    if not d and pt is None and 'pt' in seen and not g.ev('SHIP.device.booted') and st in ('table',):
        pass
    gn = g.ev("window.__said.filter(x => x[2] === 'torres-zeke' && /that's me|Off at five|evening's yours|Shift's at nine/.test(x[3])).length")
    if gn and ('gn%d' % gn) not in seen:
        if gnStart is None: gnStart = len(g.ev('window.__said')) - 1
        seen.add('gn%d' % gn); g.step(3); g.snap('rvB_goodnight_%d' % gn)
        print('GN', gn, g.ev(STATE)['t'], 'hush', g.ev('introHush()'), 'bubbles', g.ev("bubbles.list.map(b => [b.text.slice(0,30), b.el.style.display])"), flush=True)
    if gn >= 4:
        g.secs(6); print('goodnight done', g.ev('clockText()'), 'hush now', g.ev('introHush()'), flush=True); break
    if k % 50 == 0: print(r['t'], st, flush=True)
# before the open: open the device if not yet, to see the pointer go
if g.ev(PT): g.ev("document.getElementById('devBtn').click()"); g.step(5); print('after open', g.ev(PT), g.ev('SHIP.device.booted'))
said = g.ev('window.__said')
if gnStart is not None:
    print('bubbles said during the goodnight (others than Zeke = hush broken):')
    for s in said[gnStart:]: print('  ', s)
print('errors', g.errors[:3])
g.close()
