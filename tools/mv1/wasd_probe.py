import sys, json, os
os.chdir('/home/user/Cadet-game')
exec(open('cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
SCR = "JSON.stringify((() => { const p = player.obj.position, v = p.clone().project(camera); return [Math.round((v.x + 1) / 2 * innerWidth), Math.round((1 - v.y) / 2 * innerHeight), +(p.x).toFixed(2), +(p.z).toFixed(2)]; })())"
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844)
    g.ev("setShipNow(1440 + 700); goToDeck(3)"); g.step(20)
    def hold(key, n=30):
        a = json.loads(g.ev(SCR)); g.page.keyboard.down(key); g.step(n); b = json.loads(g.ev(SCR)); g.page.keyboard.up(key); g.step(5); c = json.loads(g.ev(SCR))
        return a, b, c
    for k in ['w', 'd', 's', 'a', 'ArrowUp', 'ArrowLeft', 'W']:
        a, b, c = hold(k)
        az = g.ev('az'); import math
        dx, dz = b[2] - a[2], b[3] - a[3]; L = math.hypot(dx, dz) or 1
        right = (math.cos(az), -math.sin(az)); up = (-math.sin(az), -math.cos(az))
        print(k, 'walked', round(L, 2), 'tiles; along screen-right', round((dx*right[0]+dz*right[1])/L, 2), 'screen-up', round((dx*up[0]+dz*up[1])/L, 2), '| after release moved', round(abs(c[2] - b[2]) + abs(c[3] - b[3]), 2))
    # the view turned a quarter: up is still up the screen
    g.ev("azT += Math.PI / 2"); g.step(60)
    a, b, c = hold('w'); print('turned view, w: screen dx', b[0] - a[0], 'dy', b[1] - a[1])
    # a panel open: the device
    g.ev("document.getElementById('devBtn').click()"); g.step(10)
    print('device open', g.ev("DEV.open"))
    a, b, c = hold('w'); print('device open, w moved', round(abs(b[2] - a[2]) + abs(b[3] - a[3]), 2))
    g.ev("deviceClose()"); g.step(10)
    # typing in a text field
    g.ev("const i = document.createElement('input'); i.id = 'tf'; i.style.cssText = 'position:fixed;left:0;top:300px;z-index:99'; document.body.appendChild(i); i.focus()")
    a, b, c = hold('w'); print('text field, w moved', round(abs(b[2] - a[2]) + abs(b[3] - a[3]), 2), 'field has', repr(g.ev("document.getElementById('tf').value")))
    g.ev("document.getElementById('tf').blur()")
    # ctrl held
    g.page.keyboard.down('Control'); a, b, c = hold('d'); g.page.keyboard.up('Control'); print('ctrl+d moved', round(abs(b[2] - a[2]) + abs(b[3] - a[3]), 2))
    # paused
    g.ev("pauseSet(true)"); a, b, c = hold('w'); print('paused, w moved', round(abs(b[2] - a[2]) + abs(b[3] - a[3]), 2)); g.ev("pauseSet(false)")
    # a tap while a key walks: the tap still works afterwards
    a, b, c = hold('s', 10)
    print('errors', g.errors[:5])
    g.close()
