import sys
exec(open(__file__.replace('putdown-40c1f76-ride-probe.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
DELIV = open(__file__.replace('putdown-40c1f76-ride-probe.py', 'putdown-40c1f76-probe.py')).read().split('DELIV = """')[1].split('"""')[0]
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844)
    g.ev("goToDeck(5)"); g.step(5)
    print('z40 divs:', g.ev("[...document.querySelectorAll('body > div')].filter(e => getComputedStyle(e).zIndex === '40').map(e => [e.id, e.className, e.hidden, getComputedStyle(e).display, getComputedStyle(e).pointerEvents, getComputedStyle(e).opacity, e.textContent.slice(0, 60)])"))
    g.ev(DELIV); g.step(3)
    g.ev("(() => { const L = ITEMS.find(i => i.lift); L.hit.getWorldPosition(_wp); const p = nearestOpen(_wp.x, _wp.z, player); player.obj.position.copy(cellPos(...p)); })()"); g.step(3)
    print('inLift', g.ev("inLift()"), 'holding', g.ev("player.holding"))
    g.ev("startRide(4)"); g.step(12)
    print('ride', g.ev("!!ride && ride.t"), 'deck', g.ev("deckDef.num"), 'shown', g.ev("!document.getElementById('putDown').hidden"))
    g.ev("document.getElementById('putDown').click()"); g.step(3)
    print('crate', g.ev("SHIP.player.crate"), 'toast', g.ev("document.getElementById('tx').textContent")[:100])
    g.step(300)
    print('after ride: deck', g.ev("deckDef.num"), 'player at', g.ev("[player.obj.position.x, player.obj.position.z, inLift()]"), 'crate', g.ev("SHIP.player.crate"), 'visible', g.ev("PUT_CRATE && PUT_CRATE.visible"))
    print('crate tile free / reachable:', g.ev("(() => { const c = SHIP.player.crate; if (!c) return null; const t = nearestOpen(c.x + 0, c.z + .55, player); return [t, !!findPath(player.here(), t, null, player), Math.hypot(cellPos(...t).x - c.x, cellPos(...t).z - c.z)]; })()"))
    print('errors', g.errors[:3])
    g.close()
