# Reviewer 1g: Put down with a reserved job's made part (the bracket waits at the lathe) and the toolbox
import sys, json
exec(open(__file__.replace('putdown-40c1f76-made-probe.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
ok = True
def check(c, m):
    global ok
    print('ok  ' if c else 'FAIL', m); ok = ok and bool(c); return c
TAPS = "(() => { const it = ITEMS.find(i => i.t === %s); it.hit.getWorldPosition(_wp); return playerTap(it, _wp.clone(), _wp.clone()); })()"
vis = "!document.getElementById('putDown').hidden"
def run_until_idle(g, n=120):
    for k in range(n):
        g.step(30)
        if k > 1 and not g.ev("!!ACT || player.path.length > 0"): break
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844)
    g.ev("setShipNow(Math.floor(shipNow() / 1440) * 1440 + 1440 * 2 + 9 * 60); needsT = null; SHIP.player.carry = []; SHIP.player.work = null"); g.step(3)
    rj = g.ev("(() => { const id = jobReserve('lights', SHIP.time.day, Math.max(0, SHIP.time.min - 1), 3); if (!id || !claimJob(id)) return null; myWork(); const j = myJob(); return [id, j.parts, j.make, jobStops(j).map(x => x.step)]; })()")
    print('    reserved job', rj)
    g.ev("goToDeck(5)"); g.step(5)
    check(g.ev("player.holding") == 'toolbox' and not g.ev(vis), f'job toolbox only: no button (holding {g.ev("player.holding")})')
    shelf = g.ev("JSON.stringify(ITEMS.filter(i => roomAt(...cellAt(i.hit.getWorldPosition(_wp).x, _wp.z)) === 'r' && !/tarp/i.test(i.t)).map(i => i.t)[0])")
    g.ev(TAPS % shelf); run_until_idle(g)
    g.ev(f"SHIP.player.work.make = {{ part: {json.dumps(rj[2])}, done: makeMins(myJob()) - 3 }}")
    lathe = g.ev("JSON.stringify(ITEMS.filter(i => roomAt(...cellAt(i.hit.getWorldPosition(_wp).x, _wp.z)) === 'f').map(i => i.t)[0])")
    g.ev(TAPS % lathe); run_until_idle(g)
    have = g.ev("SHIP.player.carry.slice()"); print('    in hand', have, 'stops done', g.ev("myJob().stepsDone"))
    check(sorted(have) == sorted(rj[1]), 'both parts in hand')
    stock = g.ev("Object.assign({}, SHIP.stores)")
    g.ev("document.getElementById('putDown').click()"); g.step(3)
    t = g.ev("document.getElementById('tx').textContent"); print('   ', t)
    r = g.ev(f"[SHIP.player.carry.slice(), SHIP.player.work.make, SHIP.stores[{json.dumps(rj[2])}] || 0, myJob().stepsDone, !!myJob()]")
    print('    after', r)
    shelfpart = [p for p in rj[1] if p != rj[2]][0]
    check(r[0] == [] and r[1] and r[1]['part'] == rj[2] and r[2] == (stock.get(rj[2]) or 0), f'the {rj[2]} waits at the lathe, not stocked')
    check(g.ev(f"SHIP.stores[{json.dumps(shelfpart)}]") == stock.get(shelfpart, 0) + 1, f'the {shelfpart} back on the shelf')
    g.step(40); lab = g.ev("document.getElementById('ixGoal').hidden ? null : document.querySelector('#ixGoal .ixlab').textContent"); print('    pointer', lab)
    g.ev(TAPS % lathe); run_until_idle(g)
    print('    lathe again', g.ev("SHIP.player.carry.slice()"), g.ev("document.getElementById('tx').textContent")[:110])
    check(rj[2] in g.ev("SHIP.player.carry"), f'a tap at the lathe hands the {rj[2]} back')
    g.ev(TAPS % shelf); run_until_idle(g)
    check(sorted(g.ev("SHIP.player.carry")) == sorted(rj[1]), f'and the shelf part again ({g.ev("SHIP.player.carry")})')
    check(not g.errors, f'no console errors {g.errors[:3]}')
    g.close()
print('MADE PROBE OK' if ok else 'MADE PROBE FAILED')
