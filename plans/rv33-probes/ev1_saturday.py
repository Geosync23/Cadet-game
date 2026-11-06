import sys
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1])
    print(g.ev("""JSON.stringify(eventsOn(6).map(e => [e.id, Math.floor(e.from/60)+':'+String(e.from%60).padStart(2,'0'), schedPeople().filter(p => planDay(p, 6).some(s => evTagId(s.tag) === e.id)).length]))"""))
