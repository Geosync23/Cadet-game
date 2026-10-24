import sys
exec(open('/home/user/w-ds1/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    for W, H in ((390, 844), (320, 640)):
        g = Game(pw, sys.argv[1], W, H); g.step(3)
        g.ev('localStorage.clear()'); g.ev('CLOTHES_ON = true'); g.ev('newGameStart(true)'); g.step(5)
        g.ev("(() => { if (DIALOGUE) dialogueEnd(true); const f = document.querySelector('form input[maxlength=\"24\"]'); f.value = 'Sam'; f.form.requestSubmit(); })()"); g.step(20)
        g.ev("skipTo(introAbs(0, 19 * 60 + 50))"); g.step(5)
        g.ev("""(() => { const I = SHIP.intro; I.done.goodnight = Math.floor(shipNow()); delete I.done.bed; INTRO_UI.bed = false; INTRO_UI.goal = false; if (IX_GOAL) clearGoal(); if (DIALOGUE) dialogueEnd(true);
          SHIP.device.settings.tips = true; delete SHIP.device.tipsSeen.bedtime; TIP_Q.length = 0; goToDeck(4); introBedTick(); })()""")
        g.step(30)
        r = g.ev("(() => { const t = [...document.querySelectorAll('[id*=ip], .tip, #devTip, #ixTip')].filter(e => e.offsetWidth && /20:00/.test(e.textContent)); return t.map(e => { const b = e.getBoundingClientRect(); return [e.id || e.className, Math.round(b.left), Math.round(b.top), Math.round(b.right), Math.round(b.bottom)]; }); })()")
        print(W, H, r, g.errors[:2])
        g.page.screenshot(path=f'shots/ds1-tip-{W}.png')
        g.close()
