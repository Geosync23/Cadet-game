# PR9: what the panel helper costs a frame with a long list open: padTick's time (ms) in the Roster app, the pad in use
import sys, os, json
src = open('controller_check.py').read(); sys.argv = [sys.argv[0], 'starship-cadet.html', 'none']
exec(src.split('def part_off')[0].replace("__file__.replace('controller_check.py', 'cadet_test.py')", "'cadet_test.py'"))
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    p = Pad(pw, ON); p.plug(); p.press('x'); p.log()
    p.press('y'); p.step(3)
    for app in ('home', 'roster', 'calendar'):
        if app != 'home': p.ev(f"deviceShow('{app}')")
        p.step(5)
        r = p.ev("(() => { const it = padItems(padLayer()), n = it.length; padFocusTo(it[Math.min(10, n - 1)]); const inL = padLayer().contains(document.activeElement), t0 = performance.now(); for (let i = 0; i < 200; i++) padTick(1 / 60); return [n, (performance.now() - t0) / 200, inL, PAD.live, PAD.used]; })()")
        print(app, 'items', r[0], 'padTick ms', round(r[1], 3), 'focus in panel', r[2], 'live/used', r[3], r[4])
    p.close()
