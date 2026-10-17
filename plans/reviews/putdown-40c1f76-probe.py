# Reviewer 1g: Put down (0.28.60) beyond PE8's probe: a real save and reload with the crate down, the button during a
# lift ride, a New game, and a part your job makes. Run: python3 putdown-40c1f76-probe.py BUILD.html
import sys
exec(open(__file__.replace('putdown-40c1f76-probe.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
ok = True
def check(c, m):
    global ok
    print('ok  ' if c else 'FAIL', m); ok = ok and bool(c); return c
DELIV = """(() => { const c = choreWhere('delivery')[0]; const C = CHORES.delivery, t = shipNow();
  const j = { id: 'pd-del@1', machine: null, deck: c.deck, room: c.room, kind: 'chore', chore: 'delivery', target: c.key, title: c.title, bring: c.bring || null, tier: 1,
    stops: c.stops.map(x => ({ ...x })), urgency: 0, posted: t, found: t, claimedBy: null, parts: (C.parts || []).slice(), status: 'open' };
  SHIP.jobs.push(j); MACH_REV++; claimJob(j.id); const k = jobStops(j).findIndex(x => x.step === 'pickup'); jobStepDone(j.id, k); return k; })()"""
vis = "!document.getElementById('putDown').hidden"
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844)
    url = g.page.url.split('?')[0] + '?debug'
    g.page.evaluate("localStorage.clear()")
    g.page.goto(url); g.page.wait_for_function('window.__sc !== undefined', timeout=60000)
    g.ev("(() => { const rr = renderer.render.bind(renderer); renderer.render = (s, c) => { if (!window.__skip) rr(s, c); }; })()")
    g.ev("if (typeof introSkip === 'function' && SHIP.time.day === 0) newGameStart(false)"); g.step(10)
    g.ev("goToDeck(5)"); g.step(5)
    pick = g.ev(DELIV); g.step(3)
    check(g.ev(vis), 'crate in hand: button shown (saves on)')
    print('    on top of the button:', g.ev("(() => { const b = document.getElementById('putDown').getBoundingClientRect(), e = document.elementFromPoint(b.left + b.width / 2, b.top + b.height / 2); let x = e, path = []; while (x && x !== document.body) { path.push(x.tagName + (x.id ? '#' + x.id : '') + (x.className && typeof x.className === 'string' ? '.' + x.className.split(' ').join('.') : '')); x = x.parentElement; } return [path.join(' < '), getComputedStyle(e).zIndex, SHIP.time.day, SHIP.time.min]; })()"))
    g.ev("document.getElementById('putDown').click()"); g.step(3)
    c0 = g.ev("SHIP.player.crate"); check(c0, f'crate down {c0}')
    g.ev("saveGame()")
    sv = g.page.evaluate("JSON.parse(localStorage.getItem(Object.keys(localStorage).find(k => /cadet|wren/i.test(k)) || localStorage.key(0)))")
    check(sv and sv.get('player', {}).get('crate'), f"in the real save: {sv and sv.get('player', {}).get('crate')}")
    g.page.goto(url); g.page.wait_for_function('window.__sc !== undefined', timeout=60000)
    g.ev("(() => { const rr = renderer.render.bind(renderer); renderer.render = (s, c) => { if (!window.__skip) rr(s, c); }; })()")
    g.step(10)
    r = g.ev(f"[SHIP.player.crate, !!myJob() && myJob().id, myJob() && jobStops(myJob())[{pick}].done, player.holding, !!(PUT_CRATE && PUT_CRATE.visible), {vis}, deckDef.num]")
    print('    after reload', r)
    check(r[0] and r[0]['x'] == c0['x'] and r[1] == 'pd-del@1' and r[2] and r[3] != 'carry' and not r[5], 'reload: crate still down, job still yours, hands empty, no button')
    check(r[4] == (r[6] == c0['deck']), 'reload: crate drawn on its deck')
    # lift ride with a part in hand
    g.ev("SHIP.player.crate = null; SHIP.player.carry.push('filter')"); g.step(3)
    g.ev("(() => { const L = ITEMS.find(i => i.lift); if (L) { L.hit.getWorldPosition(_wp); const p = nearestOpen(_wp.x, _wp.z, player); player.obj.position.copy(cellPos(...p)); } })()"); g.step(3)
    inl = g.ev("inLift()")
    if inl:
        g.ev("startRide(deckDef.num === 5 ? 4 : 5)"); g.step(2)
        check(g.ev("!!ride") and not g.ev(vis), f'mid lift ride: button hidden (ride {g.ev("!!ride")}, shown {g.ev(vis)})')
        g.step(200)
    else: print('    (could not stand in the lift; lift-ride check skipped)')
    # New game
    g.ev("SHIP.player.carry.length = 0"); g.ev(DELIV); g.step(2); g.ev("document.getElementById('putDown').click()"); g.step(2)
    g.ev("newGameStart(false)"); g.step(5)
    check(not g.ev("SHIP.player.crate") and not g.ev("PUT_CRATE && PUT_CRATE.visible"), f'New game: no crate ({g.ev("SHIP.player.crate")})')
    check(not g.errors, f'no console errors {g.errors[:3]}')
    g.close()
print('1G PROBE OK' if ok else '1G PROBE FAILED')
