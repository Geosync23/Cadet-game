from pp import *
import re, json
src = open(REPO+'/intro_check.py').read()
WALK = re.search(r'WALK_TICK = r"""(.*?)"""', src, re.S).group(1)
g = start()
g.step(10)
g.ev("""(() => { window.__said = []; const old = bubbleSay; bubbleSay = function (h, text, s) { const a = DECK_CREW.find(x=>x.h===h); window.__said.push([clockText(), SHIP.intro.step, a&&a.p?a.p.id:'?', 'BUBBLE', text]); return old.apply(this, arguments); };
 const ot = toast; toast = function (a, b) { window.__said.push([clockText(), SHIP.intro.step, '', 'TOAST', a + ' | ' + b]); return ot.apply(this, arguments); }; return true; })()""")
sign(g)
log=[]; shots=set(); last=None
for k in range(520):
    g.step(20)
    r = g.page.evaluate('([s, m]) => window.__sc(s)(m)', [WALK, 'follow'])
    ex = g.ev("""(() => { const a = DECK_CREW.find(x => x.p && x.p.id === 'torres-zeke'), c = DECK_CREW.find(x => x.p && x.p.id === 'calder'), p = player.obj.position;
      return { dz: a ? +Math.hypot(a.x-p.x, a.z-p.z).toFixed(2) : null, cal: c ? [cellAt(c.x,c.z), c.pose, c.tag, +Math.hypot(c.x-p.x,c.z-p.z).toFixed(1)] : null,
        dev: typeof introFlag==='function' && introFlag('intro.device'), goal: IX_GOAL && IX_GOAL.label, devBtn: (()=>{const b=document.getElementById('devBtn'); return b? getComputedStyle(b).display+'/'+b.className : null})() } })()""")
    r.update(ex)
    log.append(r)
    st = r['step']
    if st != last:
        print(r['t'], st, 'deck', r['deck'], 'me', r['me'], 'esc', r['esc'], 'dz', r['dz'], 'cal', r['cal'], 'dev', r['dev'], 'goal', r['goal'])
        last = st
    if st == 'chief' and 'chief' not in shots: shots.add('chief'); g.snap('_a_chief_start')
    if r['dz'] is not None and r['dz'] < 0.45 and r['deck'] in (4,5,3) and ('clip'+str(r['deck'])) not in shots and not r['dlg']:
        shots.add('clip'+str(r['deck'])); g.snap('_a_clip_d%d'%r['deck']); print('  CLIP', r['t'], r['me'], r['esc'], r['dz'])
    if r['dev'] and 'dev' not in shots and not r['dlg']: shots.add('dev'); g.snap('_a_device_first'); print('  DEVICE', r['t'], r['devBtn'])
    if g.ev("SHIP.intro.done.goodnight !== undefined") and 'gn' not in shots: shots.add('gn'); print('  goodnight done', r['t'])
    if st in ('tomas','night') and k > 0 and 'end' not in shots:
        shots.add('end'); g.snap('_a_after_free')
    if r['t'].endswith('19:45'): break
said = g.ev('window.__said')
json.dump({'log':log,'said':said}, open('a1.json','w'))
for s in said: print(s)
print(g.errors[:5])
g.close()
