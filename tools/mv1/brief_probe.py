# note 2: Day 1's briefing in the real game (intro on): where the Chief is while it plays at a reader's pace, and after
import sys, json, os
os.chdir('/home/user/Cadet-game')
exec(open('cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
MODE = sys.argv[2] if len(sys.argv) > 2 else 'attend'
CAL = "(() => { const a = DECK_CREW.find(x => x.p.id === 'calder'); const w = whereIs(ROSTER.find(p => p.id === 'calder'), shipNow()); return clockText().split(' ').pop() + ' ' + (a ? (ROOMS[roomAt(...cellAt(a.x, a.z))] || {}).name || '?' : 'not on deck') + ' plan:' + (w.deck + ':' + (w.placeId || w.act) + ' until ' + hhmm(w.until % 1440)); })()"
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1])
    url = g.page.url.split('?')[0]
    g.page.goto(url + '?debug'); g.page.wait_for_function('window.__sc !== undefined || window.__err', timeout=60000); g.ev(SKIP_SWITCH); g.step(5)
    g.ev('localStorage.clear()'); g.ev('if (typeof DEV !== "undefined" && DEV.open) deviceClose(); newGameStart(true)'); g.step(5)
    g.ev("(() => { const f = document.querySelector('form input[maxlength=\"24\"]'); f.value = 'Sam'; f.form.requestSubmit(); })()"); g.step(5)
    g.ev('skipTo(introAbs(1, 8 * 60 + (%d)))' % (40 if MODE != 'late' else 58))
    if MODE == 'miss': g.ev('goToDeck(3)')
    else: g.ev('(() => { goToDeck(5); player.obj.position.copy(cellPos(15, 3)); })()')
    g.step(5)
    if MODE == 'miss':
        g.ev('goToDeck(5); player.obj.position.copy(cellPos(2, 2))')   # away from the bay, on its deck, to watch her
        for i in range(60):
            g.step(60); print(g.ev(CAL), g.ev("SHIP.intro.done['d1-briefing:met']")) if i % 6 == 0 else None
        sys.exit()
    met = None
    for i in range(80):
        g.step(30); met = g.ev('DIALOGUE && DIALOGUE.id')
        if met: break
    print('dialogue', met, g.ev(CAL))
    rooms = []; n = 0
    while g.ev('!!DIALOGUE') and n < 60:
        g.ev('(() => { const l = DIALOGUE.queue[DIALOGUE.i]; if (l && l.choice) dialogueChoose(0); else dialogueNext(); })()'); n += 1
        if not g.ev('!!DIALOGUE'): break
        g.step(100); c = g.ev(CAL); rooms.append(c)
    for r in rooms[::3]: print('  ', r)
    print('last', rooms[-1] if rooms else None, 'taps', n)
    print('end recorded', g.ev("SHIP.intro.done['d1-briefing:end']"), 'met', g.ev("SHIP.intro.done['d1-briefing:met']"))
    for i in range(8):
        g.step(150); print(' after', g.ev(CAL))
    print('errors', g.errors[:4])
