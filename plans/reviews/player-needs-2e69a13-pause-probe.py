# reviewer 1f: does a pause eat a real-time deadline (a crew visit's 25 s knock)? exec cadet_test.py's harness
import sys, json
src = open('cadet_test.py').read().split('import sys, json, hashlib')[0]
exec(src)
from playwright.sync_api import sync_playwright
SET = "(() => { socInit(); const p = SOC.crew.find(q => q.id !== 'you'); VISIT = { p, until: performance.now() + 25000, inside: false }; SEEK = { p, until: VISIT.until, visit: true }; return p.id; })()"
GET = "JSON.stringify([!!VISIT, document.getElementById('tt').textContent, document.getElementById('tx').textContent])"
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1]); g.step(30)
    g.ev(SET); g.step(90); print('no pause, 3 s later      :', g.ev(GET))
    g.ev("VISIT = null; SEEK = null"); g.ev(SET)
    g.ev("pauseSet(true)"); g.step(900); print('paused 30 s              :', g.ev(GET))
    g.ev("pauseSet(false)"); g.step(90); print('3 s after resuming       :', g.ev(GET))
    g.close()
