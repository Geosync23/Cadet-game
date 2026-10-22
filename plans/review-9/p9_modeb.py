import sys, os, json
src = open('controller_check.py').read(); sys.argv = [sys.argv[0], 'starship-cadet.html', 'none']
exec(src.split('def part_off')[0].replace("__file__.replace('controller_check.py', 'cadet_test.py')", "'cadet_test.py'"))
from playwright.sync_api import sync_playwright
SETS = "(() => { deviceShow('settings'); return [...document.querySelectorAll('#devBody button')].some(b => /Controller settings/.test(b.textContent)); })()"
with sync_playwright() as pw:
    p = Pad(pw, ON)
    p.js("window.__padPlug(0); window.__padHello(0)"); p.step(5)
    print('connected, never pressed: live', p.ev('PAD.live'), 'used', p.ev('PAD.used'), '| Settings shows Controller settings?', p.ev(SETS))
    p.close()
