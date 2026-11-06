import sys
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
path, tag = sys.argv[1], sys.argv[2]
with sync_playwright() as pw:
    g = Game(pw, path, w=390, h=844)
    g.ev('localStorage.clear()'); g.ev("newGameStart(true)"); g.step(5)
    g.page.fill('form input[maxlength="24"]', 'Sam'); g.page.locator('form button').first.click(); g.step(10)
    g.ev("introSkip()"); g.step(3)
    g.ev("socInit(); for (const id of ['tomas','pell','torres-zeke','saad-amira','kovac-zainab','brennan','rina','halloran-emeka']) if (SOC.idx.has(id)) { relAdd(id, 'talk', 60); SHIP.rel[id].met = 0; }")
    def live(t, pid):
        return g.ev(f"(() => {{ setShipNow({t}); storyArrows({t}); return guideLive({t}).some(e => e.id === 'story:word:{pid}'); }})()")
    # walk through Days 9-12 every 10 ship minutes, before and after opening the card each day
    res = []
    for d in range(9, 13):
        seen = []; opened = None; pid = None
        for m in range(7 * 60, 23 * 60, 10):
            t = (d - 1) * 1440 + m
            if pid is None:
                pid = g.ev(f"(() => {{ const p = SOC.crew.find(p => storyIdx().beats.has(p.id) && momentReady(p, {t})); return p ? p.id : null; }})()")
                if pid is None: continue
            on = live(t, pid); seen.append(on)
            if on and opened is None and len(seen) >= 3:   # the player notices it after half an hour and opens their card
                g.ev(f"setShipNow({t})"); g.ev(f"chatOpen(socP('{pid}'))"); g.ev("chatClose()"); opened = len(seen)
        before = sum(seen[:opened]) if opened else sum(seen); after = sum(seen[opened:]) if opened else 0
        res.append(f'Day {d} {pid}: arrow samples before opening {before}, after opening {after}, opened at sample {opened}')
    for r in res: print(tag, r)
    print(tag, 'errors', g.errors[:4])
