# #17: a tap-to-walk player through the welcome tour: taps the step's checkpoint tile (as the arrow invites), rides the
# lift like intro_check's walker, taps through meetings. Measures Zeke-to-you distance; snaps the first long overlap per deck.
from pp import *
import re
src = open(REPO+'/intro_check.py').read()
WALK = re.search(r'WALK_TICK = r"""(.*?)"""', src, re.S).group(1)
TAPWALK = r"""(() => {
  const I = SHIP.intro, st = introStepById(I.step), here = player.here();
  if (DIALOGUE) { const l = DIALOGUE.queue[DIALOGUE.i]; if (l && l.choice) dialogueChoose(1); else dialogueNext(); return 'talk'; }
  if (!st || !st.checkpoint || st.checkpoint.deck !== deckDef.num) return null;
  const c = st.checkpoint.tile;
  if (Math.max(Math.abs(here[0] - c[0]), Math.abs(here[1] - c[1])) >= 1 && !player.path.length) { player.goTo(c); return 'tap'; }
  return 'there';
})()"""
D = """(() => { const a = DECK_CREW.find(x => x.p && x.p.id === 'torres-zeke'), p = player.obj.position; return a ? [+Math.hypot(a.x-p.x,a.z-p.z).toFixed(2), a.pose, cellAt(a.x,a.z)] : null; })()"""
g = start(); g.step(10); sign(g)
run, worst, shots, stats = 0, {}, set(), {}
for k in range(700):
    g.step(15)
    st = g.ev("SHIP.intro.step")
    if st in ('table', 'chief', 'free', 'tomas', 'night'): break
    a = g.ev(TAPWALK)
    if a is None:     # another deck: use intro_check's walker to ride the lift
        g.page.evaluate('([s, m]) => window.__sc(s)(m)', [WALK, 'follow'])
    d = g.ev(D); dk = g.ev('deckDef.num')
    if not d: continue
    s = stats.setdefault((dk, st), [0, 0]); s[0] += 1
    if d[0] < .42: s[1] += 1; run += 1
    else: run = 0
    if run == 8 and (dk, st) not in shots:
        shots.add((dk, st)); g.snap('_a17_%d_%s' % (dk, st)); print('overlap', g.ev('clockText()'), dk, st, d, a, flush=True)
print('ticks (0.5 s each) per deck/step: [all, overlapping < .42 m]')
for k2, v in stats.items(): print(' ', k2, v)
g.close()
