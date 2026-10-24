import sys
exec(open('/home/user/w-fx4c/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
tag = sys.argv[2]
with sync_playwright() as pw:
    for (W, H) in ((390, 844), (320, 640), (1280, 800)):
        g = Game(pw, sys.argv[1], W, H); g.step(5)
        g.ev("(() => { if (SHIP.device && SHIP.device.settings) SHIP.device.settings.tips = false; const t = document.getElementById('devTip'); if (t) t.hidden = true; })()")
        # a work meter (as device_check fakes it), then the device opened by a real tap on its button
        FAKE = "(() => { window._kp = window._kp || actProgress; window._ka = ACT; ACT = { kind: 'x', x: player.obj.position.x, y: 0, z: player.obj.position.z }; actProgress = () => ({ title: 'Repairing', frac: .3, left: 20 }); actBar(); ACT = window._ka; })()"
        g.ev(FAKE); g.page.screenshot(path=f'shots/{tag}-{W}-meter.png')
        g.page.click('#devBtn'); g.ev(FAKE)
        r = g.ev("(() => { const b = document.getElementById('actBar').getBoundingClientRect(), d = document.getElementById('device').getBoundingClientRect(); return { bar: [b.left, b.top, b.right, b.bottom].map(Math.round), dev: [d.left, d.top, d.right, d.bottom].map(Math.round), hidden: document.getElementById('actBar').hidden }; })()")
        print(W, H, 'meter with the device open', r)
        g.page.screenshot(path=f'shots/{tag}-{W}-device.png')
        g.ev("deviceClose(); actProgress = window._kp; actBar()"); g.step(2)
        # the lift panel with the goal on another deck
        g.ev("setGoal({ deck: 3, room: 'M', label: 'The mess hall, Deck 3' }); openLiftPanel()"); g.step(3)
        em = g.ev("(() => { const e = [...document.querySelectorAll('#lift em, .lift em')].find(x => x.offsetWidth); if (!e) return null; const r = e.getBoundingClientRect(), b = e.closest('button').getBoundingClientRect(); return { text: e.textContent, em: [r.left, r.right].map(Math.round), btn: [b.left, b.right].map(Math.round), lines: e.getClientRects().length }; })()")
        print(W, H, 'lift row', em)
        g.page.screenshot(path=f'shots/{tag}-{W}-lift.png')
        g.ev("closeLiftPanel()"); g.step(2)
        tb = g.ev("(() => { const b = document.getElementById('trkBtn').getBoundingClientRect(); return [b.left, b.top, b.right, b.bottom].map(Math.round).concat([document.querySelector('#trkBtn span').textContent]); })()")
        print(W, H, 'HUD button', tb)
        ov = g.ev("(() => { const t = document.getElementById('trkBtn').getBoundingClientRect(); return [...document.querySelectorAll('button, #needStrip, .hud, #hud > *')].filter(e => e.id !== 'trkBtn' && e.offsetWidth && !e.closest('#trkPanel') && !e.closest('#device') && !e.closest('.lift')).map(e => [e.id || e.className, e.getBoundingClientRect()]).filter(([n, r]) => r.left < t.right && t.left < r.right && r.top < t.bottom && t.top < r.bottom).map(([n, r]) => [n, Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]); })()")
        print(W, H, 'overlaps', ov)
        g.page.screenshot(path=f'shots/{tag}-{W}-hud.png')
        print(W, H, 'errors', g.errors[:3])
        g.close()
