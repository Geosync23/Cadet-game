# Reviewer 1c's tour probe (arrival 0ea5048): follows Torres as intro_check part 8 does and logs which tour lines are said.
# Run from a checkout of the build's branch: CADET_CHROME=/opt/pw-browsers/chromium python3 -u tour_probe.py BUILD.html [frames per tile]
import sys
src = open('intro_check.py').read()
exec(open('cadet_test.py').read().split("a, shots = run(")[0].replace('timeout=60000', 'timeout=240000'))
WALK_TICK = src.split('WALK_TICK = r"""')[1].split('"""')[0]
from playwright.sync_api import sync_playwright
SAYHOOK = r"""(() => { window.__said = []; const old = bubbleSay; bubbleSay = function (h, text, s) { window.__said.push([Math.round(performance.now()), clockText(), SHIP.intro.step, cellAt(player.obj.position.x, player.obj.position.z).join(','), text]); return old.apply(this, arguments); }; return true; })()"""
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1]); every = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    g.ev('newGameStart(true)'); g.step(5)
    g.page.fill('form input[maxlength="24"]', 'Sam'); g.page.click('form button'); g.step(5)
    print('hook', g.page.evaluate('(s) => window.__sc(s)', SAYHOOK))
    print('start', g.ev("({ me: player.here(), deck: deckDef.num, step: SHIP.intro.step })"))
    trig = {}
    for k in range(300):
        g.step(every)
        r = g.page.evaluate('([s, m]) => window.__sc(s)(m)', [WALK_TICK, 'follow'])
        d = g.ev("Object.keys(SHIP.intro.done).filter(k => k.startsWith('tour:'))")
        for x in d:
            if x not in trig: trig[x] = (k, r['t'], r['deck'], r['me']); print('  TRIGGER', x, trig[x])
        if r['step'] in ('free', None): break
    for k in range(200):
        g.step(30); r = g.page.evaluate('([s, m]) => window.__sc(s)(m)', [WALK_TICK, 'none'])
        if g.ev('shipNow() >= introAbs(0, 19 * 60 + 5)'): break
    print('19:05 goal', g.ev("({ t: clockText(), goal: IX_GOAL && IX_GOAL.label, bed: SHIP.intro.done.bed, ui: INTRO_UI.bed, step: SHIP.intro.step, on: introOn() })"))
    said = g.ev('window.__said')
    for s in said: print('  ', s)
    tl = g.ev("INTRO_TOUR.map(x => [x.id, introTourLines(x.id, x.stub)])")
    heard = set(s[4] for s in said)
    for i, L in tl: print(f'{i}: heard {sum(1 for l in L if l in heard)}/{len(L)}')
