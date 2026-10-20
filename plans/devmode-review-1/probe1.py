import sys, os, time, json
os.environ.setdefault('CADET_CHROME','/opt/pw-browsers/chromium')
os.environ['CADET_WORK']='/tmp/cadet-work'
sys.path.insert(0,'/home/user/Cadet-game')
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844)
    g.step(5)
    print(g.ev("clockText()"))
    out = {}
    for target in [3, 8, 12, 20, 27]:
        t0 = time.time()
        r = g.ev(f"(() => {{ const a = performance.now(); skipTo(({target}-1)*1440 + 480); const b = performance.now(); const c = SHIP.career; return {{ ms: Math.round(b-a), clock: clockText(), career: c && {{ ms: c.ms, st: c.st, go: c.go, n: c.n, end: c.end }}, works: SHIP.works && {{ rank: SHIP.works.rank, tier: SHIP.works.tier, xp: SHIP.works.xp, tr: SHIP.works.tr }}, work: careerWork(), needs: SHIP.player.needs, event: SHIP.event, log: SHIP.eventLog.map(l=>l.id+':'+l.band) }} }})()")
        print(target, round(time.time()-t0,1), json.dumps(r)[:900])
    g.step(30); g.shot('probe1_day27.png')
    print('errors', g.errors[:5])
    g.close()
