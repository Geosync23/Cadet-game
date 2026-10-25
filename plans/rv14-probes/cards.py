import sys, json
__file__ = '/tmp/rv14/wk/cadet_test.py'
exec(open('/tmp/rv14/wk/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    for name, start, end, deck, host, card in [('week1', 6*1440+1028, 1045, 3, 'torres-zeke', 'week1.zeke'), ('swap', 13*1440+655, 665, 3, 'ishikawa-orla', 'swap.meet')]:
        g = Game(pw, sys.argv[1], 900, 760)
        g.ev("(() => { skipTo(%d); goToDeck(%d, null); SHIP.device.settings.tips = false; })()" % (start, deck)); g.step(10)
        for _ in range(80):
            g.step(30)
            if g.ev('SHIP.time.min') >= end: break
        r = g.ev("(() => { const z = DECK_CREW.find(x => x.p.id === '%s'); if (!z) return 'no host on deck'; tradJoinTap(z); return JSON.stringify([SHIP.time.min, DIALOGUE && DIALOGUE.id]); })()" % host)
        print(name, 'tap ->', r)
        seen = []
        for k in range(16):
            g.step(20)
            seen.append(g.ev("JSON.stringify([+SHIP.time.min.toFixed(1), DIALOGUE ? DIALOGUE.id : null, DIALOGUE && DIALOGUE.i != null ? DIALOGUE.i : null])"))
        print(name, ' '.join(seen)); print(name, 'errors', g.errors[:3]); g.close()
