# RV34: lead 51's extra asks. (a) which moments carry `notice` (only lastLightBlink); (b) a deck change mid-blink: the
# light on the new deck after the blink equals the off build's at the same frame; (c) jumps past 14:08 (skipTo from 14:00
# to 14:30, and Dev mode's clock path if it has one) don't fire it; a jump landing at 14:09 does (the 3-minute window, as
# the horn). usage: blink_more.py BUILD.html
import sys, json
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("a, shots = run(")[0])
build = sys.argv[1]
L = "JSON.stringify([+SHIP.time.min.toFixed(2), deckDef.num, FEEL_S.kinds.join(), +(simNow()/1000 - FEEL_S.t0).toFixed(2), hemi.color.getHexString(), +hemi.intensity.toFixed(5), sun.color.getHexString(), +sun.intensity.toFixed(5), LAMPS.reduce((a, x) => a + x.l.intensity, 0).toFixed(5), SHIP.event && SHIP.event.mine && SHIP.event.mine['felt:lastLightBlink'] || 0])"
with sync_playwright() as pw:
    g = Game(pw, build, 390, 844); g.step(3)
    print('moments with notice:', g.ev("JSON.stringify(Object.entries(SHIP_EVENTS).flatMap(([id, d]) => (d.moments || []).filter(m => 'notice' in m).map(m => id + '.' + m.id)))"))
    g.ev("skipTo(3 * 1440 + 14 * 60 + 7); goToDeck(3, null)"); g.step(30)
    while 'beacon' not in g.ev("FEEL_S.kinds.join()"): g.step(1)
    g.step(10); print('b mid-blink deck 3', g.ev(L))
    g.ev("goToDeck(5, null)"); g.step(1); print('b just after the deck change', g.ev(L))
    g.step(150); print('b 5 s on, deck 5', g.ev(L))
    g.close()
    g = Game(pw, build, 390, 844); g.step(3)                 # the same frames with no blink felt: block it by marking it felt
    g.ev("skipTo(3 * 1440 + 14 * 60 + 7); goToDeck(3, null)"); g.step(30)
    g.ev("FEEL_DONE.add('lastLightBlink@' + SHIP.event.startDay); if (SHIP.event.mine) SHIP.event.mine['felt:lastLightBlink'] = 1")
    g.ev("goToDeck(5, null)"); g.step(1); g.step(150); print('b reference (no blink), deck 5', g.ev(L))
    g.close()
    for frm, to, tag in [(14 * 60, 14 * 60 + 30, 'skip 14:00 -> 14:30'), (14 * 60 + 7, 14 * 60 + 9, 'skip 14:07 -> 14:09'), (14 * 60 + 7, 14 * 60 + 12, 'skip 14:07 -> 14:12')]:
        g = Game(pw, build, 390, 844); g.step(3)
        g.ev(f"skipTo(3 * 1440 + {frm})"); g.step(5); g.ev(f"skipTo(3 * 1440 + {to})")
        seen = 0
        for i in range(60): g.step(1); seen += 'beacon' in g.ev("FEEL_S.kinds.join()")
        print('c', tag, 'beacon frames', seen, g.ev(L))
        g.close()
    g = Game(pw, build, 390, 844); g.step(3)                 # Dev mode's +3 hours from 12:08: 30-minute skipTo steps, one landing on 14:08
    g.ev("skipTo(3 * 1440 + 12 * 60 + 8)"); g.step(5); g.ev("window.__toasts = []; { const ts = toast; toast = function (a, b) { window.__toasts.push([+SHIP.time.min.toFixed(2), a, String(b||'')]); return ts.apply(this, arguments); }; }")
    g.ev("(() => { const from = shipNow(), to = from + 180; for (let t = from; t < to;) { t = Math.min(to, t + 30); skipTo(t); } })()")
    seen = 0
    for i in range(60): g.step(1); seen += 'beacon' in g.ev("FEEL_S.kinds.join()")
    print('c dev-style +3 h from 12:08', 'beacon frames', seen, g.ev(L), g.ev("JSON.stringify(window.__toasts.filter(t => /pale/.test(t[2])))"))
    g.close()
    g = Game(pw, build, 390, 844); g.step(3)
    print('c dev clock functions:', g.ev("JSON.stringify(['devClockSet', 'devSkip', 'devTime', 'devGo', 'devClock'].filter(n => { try { return typeof eval(n) === 'function'; } catch (e) { return false; } }))"))
    g.close()
