import sys
exec(open(sys.argv[2] + '/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844); g.step(3)
    g.ev("skipTo(1440 + 18 * 60)"); g.step(3); g.ev("clearGoal(); deviceShow('tracked')"); g.step(3)
    loc = g.page.locator('#devBody').get_by_text('Breakfast', exact=True).first
    loc.scroll_into_view_if_needed(); loc.click(); g.step(3)
    t = g.page.evaluate("document.getElementById('devBody').innerText")
    i = t.find('Breakfast'); print('device open', g.ev("!!document.getElementById('devBody').offsetWidth"), 'IX_GOAL', g.ev("IX_GOAL && IX_GOAL.label")); print(t[i:i+120])
    g.page.screenshot(path=sys.argv[3]); print('errors', g.errors[:3]); g.close()
