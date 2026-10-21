# OR2: one person's plan on day D between minutes A and B
import sys, json
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("import sys, json, hashlib")[0])
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844)
    for s in g.ev(f"planDay(schedData().people.find(p => p.id === '{sys.argv[2]}'), {sys.argv[3]}).filter(s => s.to > {sys.argv[4]} && s.from < {sys.argv[5]}).map(s => JSON.stringify(s))"): print(s)
    g.close()
