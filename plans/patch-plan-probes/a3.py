from pp import *
import re, json, sys
src = open(REPO+'/intro_check.py').read()
WALK = re.search(r'WALK_TICK = r"""(.*?)"""', src, re.S).group(1)
WALK2 = WALK.replace("if (DIALOGUE) {", "if (DIALOGUE && !window.__manual) {")
g = start()
g.step(10)
g.ev("""(() => { window.__said = []; const old = bubbleSay; bubbleSay = function (h, text, s) { const a = DECK_CREW.find(x=>x.h===h); window.__said.push([clockText(), SHIP.intro.step, a&&a.p?a.p.id:'?', 'BUBBLE', text]); return old.apply(this, arguments); }; return true; })()""")
sign(g)
CAL = """(() => { const c = DECK_CREW.find(x => x.p && x.p.id === 'calder'); return c ? [cellAt(c.x,c.z), c.pose, c.tag, c.spot && c.spot.id] : null; })()"""
seen = set()
for k in range(900):
    g.step(20)
    st = g.ev("SHIP.intro.step")
    if st in ('table', 'chief', 'free'): g.ev("window.__manual = true")
    r = g.page.evaluate('([s, m]) => window.__sc(s)(m)', [WALK2, 'stand' if (st in ('chief', 'free') or g.ev('!!DIALOGUE')) else 'follow'])
    if st == 'table' and 'table' not in seen: seen.add('table'); print(r['t'], 'TABLE step; calder', g.ev(CAL), flush=True)
    d = g.ev("DIALOGUE ? [DIALOGUE.id, DIALOGUE.i, (DIALOGUE.queue[DIALOGUE.i]||{}).who, (DIALOGUE.queue[DIALOGUE.i]||{}).text, !!(DIALOGUE.queue[DIALOGUE.i]||{}).choice] : null")
    if d and g.ev("!!window.__manual"):
        print(r['t'], d, 'calder', g.ev(CAL), flush=True)
        t = (d[3] or '')
        if "evening's yours" in t and 'ev' not in seen: seen.add('ev'); g.snap('_a3_evening_yours')
        if "coming over" in t and 'co' not in seen: seen.add('co'); g.snap('_a3_coming_over')
        if d[0] == 'introChief' and 'ch' not in seen: seen.add('ch'); g.snap('_a3_chief_first')
        g.secs(1)
        if d[4]: g.ev("dialogueChoose(1)")
        else: g.ev("dialogueNext()")
        continue
    gn = g.ev("window.__said.filter(x => /that's me|Shift's at nine/.test(x[4])).length")
    if gn and ('gn%d' % gn) not in seen:
        seen.add('gn%d' % gn); g.step(3); g.snap('_a3_goodnight_%d' % gn); print('BUBBLES', g.ev("bubbles.list.map(b => [b.text.slice(0,30), b.el.style.display, Math.round(b.x), Math.round(b.y), b.t.toFixed(1)])"), 'GN shot', gn, g.ev(STATE), g.ev("(() => { const a = DECK_CREW.find(x => x.p && x.p.id === 'torres-zeke'), p = player.obj.position; return a ? [cellAt(a.x,a.z), a.pose, +Math.hypot(a.x-p.x,a.z-p.z).toFixed(2), ACT && ACT.placeId] : null; })()"), flush=True)
    if gn >= 2:
        print('goodnight done', r['t'], flush=True); break
    if k % 50 == 0: print(r['t'], st, flush=True)
g.secs(1); g.snap('_a3_after_goodnight')
for s in g.ev('window.__said')[-8:]: print(s)
print(g.errors[:3])
g.close()
