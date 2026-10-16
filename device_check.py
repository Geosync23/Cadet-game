# Starship Cadet: device check (keep in the repo, next to player_check.py)
# Checks section 19 (the device engineer): the device's two layers, the apps and the skin.
#   every app registered with deviceApp opens, draws something, and leaves no errors (DEV.errors, the page's errors)
#   the home screen shows the time and a tile for every app, with badges (unread mail on the Mail tile and the button)
#   tapping a tile opens the app; Back goes home; Close and the button close it; deviceOn('open' / 'close') fire once each
#   deviceDo runs an app's action (Mail: reading marks it read); deviceNotify badges an app until it's opened
#   the shim: device.addSection(id, title, render) still draws, and never replaces a native app
#   the look (0.35.1): nothing under 15px, buttons 44px high, no blur or backdrop filter, the screen's text 7:1
#   phone and wide sizes: the panel fits on screen; opening it adds nothing to the 3D scene, draw calls stay under 450
# Setup and environment as for cadet_test.py.
# Run:  python3 device_check.py BUILD.html
import sys, json
exec(open(__file__.replace('device_check.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright

ok = True
def check(cond, msg):
    global ok
    if not cond: ok = False; print('FAIL', msg)
    return cond

SIZES = [('phone', 390, 844), ('wide', 1280, 800)]
# the look rules: nothing under 15px, every button 44px high, no blur or backdrop filter, text 7:1 on the screen
LOOK = r"""(() => {
  const dev = document.getElementById('device'), lum = c => { const v = c.match(/[\d.]+/g).slice(0, 3).map(x => +x / 255).map(x => x <= .04045 ? x / 12.92 : ((x + .055) / 1.055) ** 2.4); return .2126 * v[0] + .7152 * v[1] + .0722 * v[2]; };
  const small = [], tiny = [], blur = [];
  for (const e of dev.querySelectorAll('*')) {
    const cs = getComputedStyle(e); if (e.offsetParent === null) continue;
    if (e.childNodes.length && [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()) && parseFloat(cs.fontSize) < 15) small.push(e.tagName + ':' + e.textContent.slice(0, 20));
    if (e.tagName === 'BUTTON' && e.getBoundingClientRect().height < 44) tiny.push(e.textContent.slice(0, 20));
    if ((cs.backdropFilter && cs.backdropFilter !== 'none') || (cs.webkitBackdropFilter && cs.webkitBackdropFilter !== 'none') || (cs.filter && cs.filter !== 'none')) blur.push(e.tagName);
  }
  const st = getComputedStyle(dev), ink = lum(st.getPropertyValue('--crt-ink').trim().replace(/^#(..)(..)(..)$/, (m, r, g, b) => `rgb(${parseInt(r, 16)},${parseInt(g, 16)},${parseInt(b, 16)})`)),
    bgc = getComputedStyle(dev.querySelector('.crt')).backgroundColor, bg = lum(bgc);
  return { small: small.slice(0, 4), tiny: tiny.slice(0, 4), blur: blur.slice(0, 4), contrast: Math.round((Math.max(ink, bg) + .05) / (Math.min(ink, bg) + .05) * 10) / 10 };
})()"""

def run(path):
    with sync_playwright() as pw:
        for name, w, h in SIZES:
            print(f'{name} ({w} x {h}):')
            g = Game(pw, path, w, h)
            g.step(3)
            apps = g.ev("deviceApps().map(a => a.id)")
            print('  apps:', apps)
            check(len(apps) >= 4 and all(a in apps for a in ['needs', 'jobs', 'mail', 'wallet']), f'the first apps are there: {apps}')
            MEM = "[scene.children.length, renderer.info.memory.geometries, renderer.info.memory.textures]"
            mem0 = g.ev(MEM)
            g.ev("window.__ev = []; deviceOn('open', () => __ev.push('open')); deviceOn('close', () => __ev.push('close'))")
            # the home screen
            g.page.click('#devBtn'); g.step(2)
            home = g.ev("""(() => { const b = document.getElementById('devBody'); return { open: !document.getElementById('device').hidden, app: DEV.app,
              tiles: [...b.querySelectorAll('.apps .app')].map(t => t.dataset.app), text: b.textContent, back: !document.getElementById('devBack').disabled }; })()""")
            check(home['open'] and home['app'] == 'home' and not home['back'], f'the button opens the home screen: {home["app"]}')
            check(home['tiles'] == apps, f'a tile for every app, in order: {home["tiles"]}')
            check('Day ' in home['text'], 'the home screen shows the day and time')
            mem1, calls1 = g.ev(MEM), g.ev("renderer.info.render.calls")
            check(mem1 == mem0 and calls1 < 450, f'no 3D objects added while open, draw calls under 450: {mem0} -> {mem1}, {calls1} calls')
            # every app opens and draws
            for a in apps:
                g.page.click(f'#devBody .apps .app[data-app="{a}"]'); g.step(1)
                r = g.ev("""(() => { const b = document.getElementById('devBody'); return { app: DEV.app, kids: b.children.length, text: b.textContent.slice(0, 80),
                  head: document.getElementById('devT').textContent, back: !document.getElementById('devBack').disabled, failed: b.textContent.includes('failed to draw') }; })()""")
                print(f'  {a}: {r["head"]!r} {r["text"]!r}')
                check(r['app'] == a and r['kids'] > 0 and r['back'] and not r['failed'], f'{a} opens and draws: {r}')
                lk = g.ev(LOOK)
                check(not lk['small'] and not lk['tiny'] and not lk['blur'] and lk['contrast'] >= 7, f'{a}: the look rules (15px+, 44px targets, no blur, 7:1): {lk}')
                g.page.click('#devBack'); g.step(1)
                check(g.ev("DEV.app") == 'home', f'Back from {a} goes home')
            # mail: badge, read through deviceDo, tile badge clears
            ml = g.ev("""(() => { SHIP.mail = []; mailSend({ from: 'Stores', subject: 'Filters low', body: 'Two left.' }); deviceRefresh();
              const out = { btn: document.getElementById('devMail').textContent, tile: (document.querySelector('#devBody .app[data-app="mail"] b') || {}).textContent };
              deviceShow('mail'); document.querySelector('#devBody button.row').click();
              out.read = mailUnread(); out.body = document.getElementById('devBody').textContent.includes('Two left.'); deviceShow('home'); return out; })()""")
            check(ml == {'btn': '1', 'tile': '1', 'read': 0, 'body': True}, f'mail: badges, tap to read: {ml}')
            # notify: a badge until the app is opened; urgent ones toast
            nt = g.ev("""(() => { deviceNotify({ app: 'wallet', text: 'Paid', urgent: true }); const t = (document.querySelector('#devBody .app[data-app="wallet"] b') || {}).textContent;
              const toast = document.getElementById('tx').textContent; deviceShow('wallet'); deviceShow('home');
              return [t, toast, !!document.querySelector('#devBody .app[data-app="wallet"] b')]; })()""")
            check(nt == ['1', 'Paid', False], f'deviceNotify: badge, toast, cleared on opening: {nt}')
            # the shim
            sh = g.ev("""(() => { device.addSection('test', 'Test', el => { el.textContent = 'shim works'; }); device.addSection('mail', 'Old inbox', el => { el.textContent = 'old'; });
              device.show('test'); const a = document.getElementById('devBody').textContent; device.show('mail'); const b = document.getElementById('devT').textContent;
              DEVICE_APPS.delete('test'); device.show('status'); return [a, b, DEV.app]; })()""")
            check(sh == ['shim works', 'Mail', 'home'], f'addSection shim: {sh}')
            # it fits on screen
            box = g.ev("(() => { const r = document.getElementById('device').getBoundingClientRect(); return [r.left, r.top, r.right, r.bottom]; })()")
            check(box[0] >= 0 and box[1] >= 0 and box[2] <= w and box[3] <= h, f'the panel fits on screen: {box}')
            g.page.click('#devClose'); g.step(1)
            check(g.ev("document.getElementById('device').hidden && !DEV.open"), 'Close closes it')
            g.page.click('#devBtn'); g.step(1); g.page.click('#devClose'); g.step(1)   # wide: the side panel covers the button; Close is the way out
            ev = g.ev("__ev")
            check(ev == ['open', 'close', 'open', 'close'], f'deviceOn fires once per open and close: {ev}')
            errs = g.ev("DEV.errors")
            check(not errs, f'no app errors: {errs}')
            check(not g.errors, f'no page errors: {g.errors[:5]}')
            g.close()
    print('device_check:', 'OK' if ok else 'FAILED')
    return ok

if __name__ == '__main__':
    sys.exit(0 if run(sys.argv[1]) else 1)
