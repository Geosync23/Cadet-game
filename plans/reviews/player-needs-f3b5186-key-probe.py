import sys
src = open('cadet_test.py').read().split('import sys, json, hashlib')[0]; exec(src)
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1]); g.step(30)
    g.page.click('#pauseBtn'); g.step(3)
    r = [g.ev("PAUSE.on"), g.ev("document.activeElement && document.activeElement.closest('#pauseCard') ? 'resume' : (document.activeElement || {}).id")]
    for k in range(3): g.page.keyboard.press('Tab'); g.step(1)
    r.append(g.ev("document.activeElement && document.activeElement.closest('#pauseCard') ? 'resume' : (document.activeElement || {}).id"))
    t0 = g.ev("shipNow()"); g.step(60); r.append(g.ev("shipNow()") == t0)
    g.page.keyboard.press('Enter'); g.step(3); r.append(g.ev("PAUSE.on"))
    g.page.click('#pauseBtn'); g.step(3); g.page.keyboard.press('Escape'); g.step(3); r.append(g.ev("PAUSE.on"))
    print('paused, focus, focus after 3 Tabs, time still, after Enter paused?, after Escape paused?:', r, g.errors[:2])
    g.close()
