# PR4's probe loader: cadet_test.py's top (WORK, THREE, INIT, instrument, Game) without its run. exec(open('pp.py').read())
exec(open('/home/user/cadet-game/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
