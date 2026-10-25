import sys, json
__file__ = '/tmp/rv14/wk/cadet_test.py'
exec(open('/tmp/rv14/wk/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 900, 760)
    d = json.loads(g.ev("JSON.stringify([...Array(30).keys()].map(i => i + 1).filter(d => eventsOn(d).some(e => e.id === 'spice-shelf-supper'))[0])"))
    g.ev("(() => { skipTo(%d * 1440 + 1120); goToDeck(3, null); SHIP.device.settings.tips = false; })()" % (d - 1)); g.step(10)
    print('spice day', d, g.ev("(() => { spiceCard(%d, spiceWeek(%d), shipNow()); return JSON.stringify([SHIP.time.min, DIALOGUE && DIALOGUE.id]); })()" % (d, d)))
    s = []
    for k in range(10): g.step(20); s.append(g.ev("JSON.stringify([+SHIP.time.min.toFixed(1), DIALOGUE ? DIALOGUE.id : null])"))
    print('spice', ' '.join(s)); g.close()
    g = Game(pw, sys.argv[1], 900, 760)
    g.ev("(() => { skipTo(7 * 1440 + 1170); goToDeck(7, null); SHIP.device.settings.tips = false; })()"); g.step(10)
    print('talk', g.ev("(() => { const e = eventsOn(8).find(x => /^rec-(wren|chiefs)-talk$/.test(x.id)); recTalkCard(e, 8, shipNow(), true); return JSON.stringify([e && e.id, SHIP.time.min, DIALOGUE && DIALOGUE.id]); })()"))
    s = []
    for k in range(10): g.step(20); s.append(g.ev("JSON.stringify([+SHIP.time.min.toFixed(1), DIALOGUE ? DIALOGUE.id : null])"))
    print('talk', ' '.join(s)); print(g.errors[:3]); g.close()
