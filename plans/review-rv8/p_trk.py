# RV8 probe: Tracked panel at 390x844 with real taps. python3 p_trk.py GAME.html CADET_TEST_DIR OUTPREFIX
import sys
exec(open(sys.argv[2] + '/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
out = sys.argv[3]
def rows(g): return g.page.evaluate("[...document.querySelectorAll('#trkList button')].map(b => (b.classList.contains('goal') ? '[HI] ' : '') + b.textContent)")
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844); g.step(3)
    g.ev("skipTo(1440 + 18 * 60)"); g.step(3); g.ev("clearGoal()"); g.step(2)
    g.page.click('#trkBtn'); g.step(2)
    print('rows:'); [print('  ', r) for r in rows(g)]
    g.shot(out + '-1-open.png')
    tom = g.page.evaluate("[...document.querySelectorAll('#trkList button')].findIndex(b => /Tomorrow/.test(b.textContent) && !b.disabled)")
    print('tomorrow idx', tom)
    if tom >= 0:
        g.page.locator('#trkList button').nth(tom).click(); g.step(2)
        print('after tap: panel hidden', g.page.evaluate("document.getElementById('trkPanel').hidden"), 'IX_GOAL', g.ev("IX_GOAL && IX_GOAL.label"))
        print('   row now:', rows(g)[tom] if not g.page.evaluate("document.getElementById('trkPanel').hidden") else '-')
        g.shot(out + '-2-tomorrow.png')
        g.step(30 * 60 * 3)  # some ship time
        print('   later  :', g.ev("Math.floor(shipNow())"), rows(g)[tom] if rows(g) else '-')
    # a today row
    g.page.click('#trkClose'); g.step(1)
    g.ev("setGoal({ deck: 5, item: /job board/i, room: 'w', label: 'Take your first round at the job board' })"); g.step(2)
    g.page.click('#trkBtn'); g.step(2)
    print('with round goal:'); [print('  ', r) for r in rows(g) if r.startswith('[HI]')]
    g.shot(out + '-3-arrow.png')
    g.page.click('#trkClose'); g.step(1)
    # device app
    g.ev("deviceShow('tracked')"); g.step(2)
    print('device:', g.page.evaluate("document.getElementById('devBody').innerText")[:1200])
    g.shot(out + '-4-device.png')
    print('errors', g.errors[:5])
    g.close()
