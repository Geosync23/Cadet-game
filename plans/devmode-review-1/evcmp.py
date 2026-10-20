import sys, os, json, hashlib
os.environ.setdefault('CADET_CHROME','/opt/pw-browsers/chromium')
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
out = {}
with sync_playwright() as pw:
    for f in sys.argv[1:]:
        g = Game(pw, f, 390, 844); g.step(2)
        r = g.ev("JSON.stringify([...Array(30)].map((_, i) => eventsOn(i + 1).map(e => [e.id, e.from, e.to, e.honorees]))) + '|' + JSON.stringify(ROSTER.slice(0, 40).map(p => eventPlan(p, 4)))")
        out[f] = hashlib.sha256(r.encode()).hexdigest()[:12]; print(f, out[f], 'first-light listed:', 'first-light' in r); g.close()
print('IDENTICAL' if len(set(out.values())) == 1 else 'DIFFERENT')
