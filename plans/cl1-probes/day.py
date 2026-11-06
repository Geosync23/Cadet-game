import sys, os
os.chdir('/home/user/Cadet-game')
exec(open('cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    g=Game(pw,sys.argv[1])
    print(g.ev(sys.argv[2]))
    print(g.errors[:5]); g.close()
