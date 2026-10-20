# patch #6 with Dev mode: a Dev clock jump during the Undo window (the real Dev action, devmodeRun + devmodeSkipTo)
import sys, os; sys.path.insert(0, '/home/user/Cadet-game/plans/patch-plan-probes')
from pp import *
g = start('?debug&clockundo#dev'); g.step(10)
if g.ev(SIGN): sign(g)
g.secs(2); print('Dev mode on:', g.ev("DEVMODE"))
D3 = 2*1440
g.ev(f"skipTo({D3} + 8*60+50)"); g.ev("goToDeck(5)"); g.step(5); g.ev("SHIP.player.carry.length = 0")
g.ev("(() => { const q = (DECKS[5].places||[]).find(p => p.id==='5-timeclock-1'); const n = nearestOpen(cellPos(...q.at).x, cellPos(...q.at).z, player); player.obj.position.copy(cellPos(...n)); target.copy(player.obj.position).setY(.7); })()"); g.step(5)
g.ev("clockScreen()"); g.secs(1)
b = g.page.locator('#clockScreen .btns button').nth(0).bounding_box(); g.page.mouse.click(b['x'] + 5, b['y'] + 5); g.step(2)
st = "({ t: clockText(), in: careerClockedIn(), ci: SHIP.career.ci, undo: CLOCK_UNDO ? CLOCK_UNDO.what : null, notes: SHIP.notes.filter(n => n.kind === 'clock').length })"
print('in the window:', g.ev(st))
print('Dev jump:', g.ev(f"devmodeRun('Clock: test', () => devmodeSkipTo({D3} + 11*60))"), g.ev("DM_UI.msg"))
g.step(5); print('after:', g.ev(st), '| screen:', g.ev("document.getElementById('clockScreen').hidden ? '(hidden)' : document.getElementById('clockScreen').innerText.replace(/\\n+/g, ' | ')"))
print('errors', g.errors[:5]); g.close()
