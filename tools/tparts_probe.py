import sys, json
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1]); a = g.ev(open('tools/tparts_probe.js').read())
    for k in ('not0','bring','not'): print(k, a[k].get('mach'), a[k].get('first'), a[k].get('run'), a[k].get('teams'))
    g.close()
