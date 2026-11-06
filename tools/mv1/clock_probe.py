# MV1-2: Day 1, the briefing read quickly, then taps on the time clock: does the clock (not the Chief) answer?
import sys, json, os
os.chdir('/home/user/Cadet-game')
exec(open('cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
CAL = "(() => { const a = DECK_CREW.find(x => x.p.id === 'calder'); const w = whereIs(ROSTER.find(p => p.id === 'calder'), shipNow()); return hhmm(shipNow() % 1440) + ' calder ' + (a ? a.here() + (a.settled ? ' sat ' : ' ') : 'off deck ') + (w.placeId || w.act); })()"
TAP = r"""(() => { const it = ITEMS.find(i => i.t === 'Time clock'), v = new THREE.Vector3(); it.hit.getWorldPosition(v); v.project(camera);
  const x = (v.x + 1) / 2 * innerWidth, y = (1 - v.y) / 2 * innerHeight; tap(x, y);
  const shown = id => { const e = document.getElementById(id); return !!e && !e.hidden && e.getClientRects().length > 0; };
  return { clock: shown('clockScreen'), chat: shown('chat'), dlg: !!DIALOGUE }; })()"""
CLOSE = "(() => { for (const id of ['clockScreen', 'chat']) { const e = document.getElementById(id); if (e && !e.hidden) { const b = e.querySelector('button.close, .close, button[data-close]'); if (b) b.click(); else e.hidden = true; } } if (typeof chatClose === 'function') try { chatClose(); } catch (e) {} })()"
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844)
    url = g.page.url.split('?')[0]
    g.page.goto(url + '?debug'); g.page.wait_for_function('window.__sc !== undefined || window.__err', timeout=60000); g.ev(SKIP_SWITCH); g.step(5)
    g.ev('localStorage.clear()'); g.ev('if (typeof DEV !== "undefined" && DEV.open) deviceClose(); newGameStart(true)'); g.step(5)
    g.ev("(() => { const f = document.querySelector('form input[maxlength=\"24\"]'); f.value = 'Sam'; f.form.requestSubmit(); })()"); g.step(5)
    g.ev('skipTo(introAbs(1, 8 * 60 + 40))'); g.ev('(() => { goToDeck(5); player.obj.position.copy(cellPos(19, 2)); player.stop(); })()'); g.step(5)
    for i in range(80):
        g.step(30)
        if g.ev('!!DIALOGUE'): break
    print('briefing', g.ev('DIALOGUE && DIALOGUE.id'), g.ev(CAL))
    if len(sys.argv) > 2:
        for k in range(4):
            g.step(60); r = g.ev(TAP); g.step(60); print(' during', g.ev(CAL), r, 'clocked in', g.ev('careerClockedIn(SHIP.time.day)'), 'dialogue still', g.ev('!!DIALOGUE')); g.ev(CLOSE)
    n = 0
    while g.ev('!!DIALOGUE') and n < 60:
        g.ev('(() => { const l = DIALOGUE.queue[DIALOGUE.i]; if (l && l.choice) dialogueChoose(0); else dialogueNext(); })()'); n += 1; g.step(10)
    print('read quickly, ended', g.ev(CAL))
    for k in range(8):
        r = g.ev(TAP); g.step(40); r2 = g.ev("(() => { const shown = id => { const e = document.getElementById(id); return !!e && !e.hidden && e.getClientRects().length > 0; }; return { clock: shown('clockScreen'), chat: shown('chat'), in: careerClockedIn(SHIP.time.day) }; })()")
        print(' tap', g.ev(CAL), r, '->', r2)
        if r2['clock'] or r2['in']: break
        g.ev(CLOSE); g.step(60)
    print('errors', g.errors[:3])
