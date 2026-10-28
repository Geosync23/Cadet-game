# patch #6 probe: the time clock's tap guard, buttons apart, early confirm, Undo window. GAME=..., Q=extra query
import sys, os; sys.path.insert(0, '/home/user/Cadet-game/plans/patch-plan-probes')
from pp import *
OUT = sys.argv[1] if len(sys.argv) > 1 else '/tmp'
g = start('?nosave&debug' + os.environ.get('Q', '')); g.step(5)
def at(t):
    g.ev(f"skipTo({t})"); g.ev("goToDeck(5)"); g.step(5); g.ev("SHIP.player.carry.length = 0")
    g.ev("(() => { const q = (DECKS[5].places||[]).find(p => p.id==='5-timeclock-1'); const n = nearestOpen(cellPos(...q.at).x, cellPos(...q.at).z, player); player.obj.position.copy(cellPos(...n)); target.copy(player.obj.position).setY(.7); })()")
    g.step(5)
def scr(): return g.ev("document.getElementById('clockScreen').hidden ? '(hidden)' : document.getElementById('clockScreen').innerText.replace(/\\n/g,' | ')")
def btns(): return g.ev("[...document.querySelectorAll('#clockScreen .btns button')].map(b => [b.innerText, b.style.visibility === 'hidden' ? 'gap' : 'btn', Math.round(b.getBoundingClientRect().x)])")
def st(): return g.ev("({ t: clockText(), in: careerClockedIn(), out: careerClockedOut(), on: SHIP.career.on, notes: simNotes('clock').length, undo: typeof CLOCK_UNDO !== 'undefined' && CLOCK_UNDO ? CLOCK_UNDO.what : null })")
def tap(i):   # tap the i-th button's centre (0 left, 1 right) as the screen is now; returns the point
    b = g.page.locator('#clockScreen .btns button').nth(i).bounding_box(); x, y = b['x'] + b['width']/2, b['y'] + b['height']/2
    g.page.mouse.click(x, y); return x, y
def dbl(i):   # a quick double tap at one spot (2 frames apart)
    x, y = tap(i); g.step(2); g.page.mouse.click(x, y); g.step(2)
D3 = 2*1440
print('== A. clock in at 08:50, double tap'); at(D3 + 8*60+50); g.ev("clockScreen()"); g.secs(1); print(btns())
dbl(0); print(st(), '|', scr()); print(btns()); g.page.screenshot(path=OUT + '/06-undo-in.png')
print('== B. Undo (after the guard)'); g.secs(1); tap(1); g.step(2); print(st(), '|', scr()); print(btns())
print('== C. clock in, let 5 s pass'); g.secs(1); tap(0); g.step(2); n0 = st(); g.secs(6); print(n0, '->', st(), '|', scr()); print(btns())
print('== D. at 15:00, clock out twice fast'); g.ev("clockScreen()"); g.secs(1); g.ev(f"setShipNow({D3} + 15*60)"); g.ev("clockScreen()"); g.secs(1); print(btns())
dbl(1); print(st(), '|', scr()); print(btns()); g.page.screenshot(path=OUT + '/06-early-ask.png')
print('== E. 17:05 clock out; Undo; walk away'); g.ev(f"setShipNow({D3} + 17*60+5)"); g.ev("clockScreen()"); g.secs(1); print(btns())
dbl(1); print(st(), '|', scr()); print(btns()); g.page.screenshot(path=OUT + '/06-undo-out.png')
g.secs(1); tap(0); g.step(2); print('undone', st(), '|', btns())
g.secs(1); tap(1); g.step(2); print('out again', st())
g.ev("player.obj.position.x += 3; target.copy(player.obj.position).setY(.7)"); g.step(3); print('walked away', st(), '|', scr())
print('== F. Day 4 08:55: in, then a save in the window'); at(D3 + 1440 + 8*60+55); g.ev("clockScreen()"); g.secs(1); tap(0); g.step(2); print(st())
g.ev("SAVE_EXTRA[0]({ player: {} })"); print('after save hooks', st())
print('== G. Day 5 09:10: in, then a Dev clock jump (+2 h)'); at(D3 + 2*1440 + 9*60+10); g.ev("clockScreen()"); g.secs(1); tap(0); g.step(2); print(st())
g.ev(f"skipTo({D3} + 2*1440 + 11*60+10)"); g.step(3); print('after jump', st(), '|', scr())
print('errors', g.errors[:5]); g.close()
