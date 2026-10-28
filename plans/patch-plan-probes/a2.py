from pp import *
import re, json
src = open(REPO+'/intro_check.py').read()
WALK = re.search(r'WALK_TICK = r"""(.*?)"""', src, re.S).group(1)
# same follower, but stop auto-advancing the meetings once at the table
WALK2 = WALK.replace("if (DIALOGUE) {", "if (DIALOGUE && !window.__manual) {")
g = start()
g.step(10)
g.ev("""(() => { window.__said = []; const old = bubbleSay; bubbleSay = function (h, text, s) { const a = DECK_CREW.find(x=>x.h===h); window.__said.push([clockText(), SHIP.intro.step, a&&a.p?a.p.id:'?', 'BUBBLE', text, bubbles.hidden]); return old.apply(this, arguments); };
 const ot = toast; toast = function (a, b) { window.__said.push([clockText(), SHIP.intro.step, '', 'TOAST', a + ' | ' + b]); return ot.apply(this, arguments); }; return true; })()""")
sign(g)
n=0
for k in range(600):
    g.step(20)
    st = g.ev("SHIP.intro.step")
    if st in ('table','chief','free') : g.ev("window.__manual = true")
    r = g.page.evaluate('([s, m]) => window.__sc(s)(m)', [WALK2, 'follow' if st not in ('table','chief','free','tomas') else 'stand'])
    d = g.ev("DIALOGUE ? [DIALOGUE.id, DIALOGUE.i, (DIALOGUE.queue[DIALOGUE.i]||{}).who, (DIALOGUE.queue[DIALOGUE.i]||{}).text, !!(DIALOGUE.queue[DIALOGUE.i]||{}).choice] : null")
    if d:
        n+=1
        if n in (1,) or (d[0]=='introChief' and d[1] in (0,)): g.snap('_a2_%s_%d'%(d[0],d[1]))
        print(r['t'], d)
        g.secs(2)
        if d[4]: g.ev("dialogueChoose(1)")
        else: g.ev("dialogueNext()")
        continue
    if g.ev("SHIP.intro.done['chief:end'] !== undefined"):
        break
print('after chief', g.ev(STATE))
for i in range(14):
    g.secs(1.5); g.snap('_a2_after_%02d'%i)
said = g.ev('window.__said')
for s in said[-25:]: print(s)
g.close()
