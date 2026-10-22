# RV8 probe: who takes the tracked Clock in arrow down on Day 1 (clearGoal / setGoal wrapped with a stack). p_clock2.py GAME CT_DIR
import sys, json
exec(open(sys.argv[2] + '/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
G = "[hhmm(SHIP.time.min), deckDef.num, IX_GOAL ? (IX_GOAL.trk || '') + '|' + IX_GOAL.label : null, typeof DIALOGUE !== 'undefined' && !!DIALOGUE, careerClockedIn(SHIP.time.day)]"
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844); g.step(3)
    g.ev('localStorage.clear()'); g.ev('newGameStart(true)'); g.step(5)
    g.page.fill('form input[maxlength="24"]', 'Sam'); g.page.click('form button'); g.step(5)
    g.ev("skipTo(introAbs(1, 8 * 60 + 30))"); g.ev("(() => { if (bagHeld()) bagStow(false); if (typeof DIALOGUE !== 'undefined' && DIALOGUE) dialogueEnd(); goToDeck(4); })()"); g.step(10)
    g.page.click('#trkBtn'); g.step(2)
    rows = g.page.evaluate("[...document.querySelectorAll('#trkList button')].map(b => b.textContent)")
    i = next((k for k, r in enumerate(rows) if 'Clock in' in r), -1)
    g.page.locator('#trkList button').nth(i).click(); g.step(3)
    g.ev("""(() => { window.__log = []; const c0 = clearGoal, s0 = setGoal;
      clearGoal = function () { if (IX_GOAL) __log.push(hhmm(SHIP.time.min) + ' clear ' + (IX_GOAL.trk || '') + '|' + IX_GOAL.label + ' <- ' + new Error().stack.split('\\n').slice(2, 5).map(x => x.trim().split(' ')[1]).join(' < ')); return c0.apply(this, arguments); };
      setGoal = function (g) { __log.push(hhmm(SHIP.time.min) + ' set ' + (g && ((g.trk || '') + '|' + g.label)) + ' <- ' + new Error().stack.split('\\n').slice(2, 5).map(x => x.trim().split(' ')[1]).join(' < ')); return s0.apply(this, arguments); }; })()""")
    last = None
    for k in range(30):
        if k == 6: g.ev("goToDeck(5)")
        if k == 8: print('   walk from', g.ev("[roomAt(...player.here()), Math.round(Math.hypot(placeSpot('5-timeclock-1').x - player.obj.position.x, placeSpot('5-timeclock-1').z - player.obj.position.z))]")); g.ev("(() => { const s = placeSpot('5-timeclock-1'); playerGo(nearestOpen(s.x, s.z + 1, player), null); })()")
        g.step(30); s = g.ev(G)
        if s[1:] != last: print('  ', s, 'room', g.ev("roomAt(...player.here())"), 'm to clock', g.ev("(() => { const s = placeSpot('5-timeclock-1'); return s ? Math.round(Math.hypot(s.x - player.obj.position.x, s.z - player.obj.position.z) * 10) / 10 : -1; })()")); last = s[1:]
    print('\n'.join(g.ev("__log")[:30]))
    print('errors', g.errors[:3]); g.close()
