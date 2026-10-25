# RV16: watch a crew story's big moment in the browser at phone size (390 x 844). Plays days 1..D-1 on paper
# (stories_check's "play" loop), then runs the real game to the booking, goes to the person's deck, stands you next to
# them, opens the beat (as their card would), and steps the frames through the scene: screenshots, bubble anchors
# against the speaker's head, and anyone jumping (more than 0.6 tiles in one frame).
import sys, os, json, types, re
os.environ.setdefault('CADET_CHROME', '/opt/pw-browsers/chromium')
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'cadet_test.py')).read(); src = src[:src.index('import sys, json, hashlib')]
ct = types.ModuleType('ct'); exec(src, ct.__dict__)
sc = open(os.path.join(HERE, 'stories_check.py')).read()
RUN = re.search(r'RUN = r"""(.*?)"""', sc, re.S).group(1).replace('([DAYS, MODE]) =>', '([D0, DAYS, MODE]) =>').replace('for (let d = 1; d <= DAYS; d++)', 'for (let d = D0; d <= DAYS; d++)')
BUILD, WHO, DAY = sys.argv[1], sys.argv[2], int(sys.argv[3])
MEAS = r"""(() => { const v = new THREE.Vector3(); const bs = (typeof bubbles !== 'undefined' ? bubbles.list : []).filter(b => b.el.style.display !== 'none').map(b => { const w = b.who, p = w.pos || (w.obj && w.obj.position) || w, h = w.h || 1;
  const seat = w.pos && w.pos.y >= .3 ? w.pos.y : 0; v.set(p.x, seat ? seat + 1.15 * h : (w.pos ? w.pos.y : w.obj ? w.obj.position.y : p.y || 0) + 2.0 * h, p.z).project(camera);
  return { t: b.text.slice(0, 20), dx: Math.round(b.ax - (v.x + 1) / 2 * innerWidth) }; });
  const cr = DECK_CREW.map(a => [a.p.id, +a.x.toFixed(2), +a.z.toFixed(2)]);
  const V = DIALOGUE ? dialogueView() : null;
  return JSON.stringify({ bs, cr, dlg: !!DIALOGUE, v: V && { text: (V.text || '').slice(0, 50), who: V.who, ch: V.choices ? V.choices.length : 0 } }); })()"""
with sync_playwright() as pw:
    g = ct.Game(pw, BUILD, 390, 844); g.step(3)
    g.page.evaluate('([s, a]) => window.__sc("(" + s + ")(" + JSON.stringify(a) + ")")', [RUN, [1, DAY - 1, 'play']])
    b = json.loads(g.ev(f"JSON.stringify(storyPeekCS().book['{WHO}'] || null)")); print('booking:', b)
    if not b: print('LOOK: no booking'); sys.exit(1)
    t0 = b['from'] + (12 if WHO == 'kovac-zainab' else 5)
    g.ev(f"skipTo({t0})"); g.step(10)
    w = json.loads(g.ev(f"JSON.stringify(whereIs(socP('{WHO}'), shipNow()))")); print('where:', w)
    g.ev(f"goToDeck({w['deck']})"); g.step(90)
    a = json.loads(g.ev(f"(() => {{ const a = DECK_CREW.find(a => a.p.id === '{WHO}'); return JSON.stringify(a ? [a.x, a.z, a.settled || false] : null); }})()")); print('on deck at:', a)
    if a: g.ev(f"(() => {{ const a = DECK_CREW.find(a => a.p.id === '{WHO}'); const t = nearestOpen(a.x + 1, a.z, player); const c = cellPos(t[0], t[1]); player.obj.position.set(c.x, 0, c.z); }})()"); g.step(20)
    rd = g.ev(f"momentReady(socP('{WHO}'), shipNow())"); print('ready:', rd)
    g.shot(f'shots/{WHO}_0_before.png')
    ok = g.ev(f"momentShow(momentReady(socP('{WHO}'), shipNow()) || momentNextId(socP('{WHO}')))"); print('shown:', ok)
    prev, jumps, worst, n = None, [], 0, 0
    for k in range(400):
        g.step(3, 1000 / 30)
        m = json.loads(g.ev(MEAS))
        for x in m['bs']: worst = max(worst, abs(x['dx']))
        if prev:
            P = {c[0]: c for c in prev['cr']}
            for c in m['cr']:
                q = P.get(c[0])
                if q and ((c[1] - q[1]) ** 2 + (c[2] - q[2]) ** 2) ** .5 > 0.6: jumps.append((k, c[0], q[1:], c[1:]))
        if k % 8 == 0 and m['dlg'] and n < 12: g.shot(f'shots/{WHO}_{n + 1:02d}.png'); n += 1; print('  ', k, m['v'], [x['t'] + ':' + str(x['dx']) for x in m['bs']])
        if not m['dlg']: break
        if k % 4 == 3: g.ev("(() => { const v = dialogueView(); if (!v) return; if (v.choices) dialogueStep(0); else dialogueStep(); })()")
        prev = m
    g.shot(f'shots/{WHO}_z_after.png')
    told = json.loads(g.ev(f"JSON.stringify([storyPeekCS().told['{WHO}'] || [], storyPeekCS().book['{WHO}'] || null])"))
    print('told after:', told, '| bubble anchor worst px off speaker:', worst, '| crew jumps:', jumps[:8], '| errors:', g.errors[:5])
    g.close()
