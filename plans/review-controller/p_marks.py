# RV2 probe (P3): the button marks after a pad press: where each sits against its button, at phone and wide sizes,
# for each pad family; shots; then a touch: marks hidden, page as before. Run: python3 p_marks.py GAME_ON.html OUTDIR
import sys, os, json
GAMEF, OUT = sys.argv[1], sys.argv[2]; sys.argv = [sys.argv[0]]
exec(open(os.path.join(os.path.dirname(os.path.abspath(GAMEF)), 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
FAKEPAD = r"""
(() => {
  const mk = (i, id) => ({ index: i, id, mapping: 'standard', connected: true, timestamp: 0, axes: [0, 0, 0, 0],
    buttons: Array.from({ length: 17 }, () => ({ pressed: false, touched: false, value: 0 })) });
  window.__pads = [null, null, null, null];
  Object.defineProperty(navigator, 'getGamepads', { value: () => window.__pads.slice(), configurable: true });
  window.__plug = (i, id) => { window.__pads[i] = mk(i, id); const e = new Event('gamepadconnected'); e.gamepad = window.__pads[i]; dispatchEvent(e); };
  window.__unplug = i => { const g = window.__pads[i]; g.connected = false; window.__pads[i] = null; const e = new Event('gamepaddisconnected'); e.gamepad = g; dispatchEvent(e); };
  window.__btn = (i, k, v) => { const b = window.__pads[i].buttons[k]; b.value = v; b.pressed = v > .5; b.touched = v > 0; };
})();
"""
INIT = INIT + FAKEPAD
RECTS = r"""(() => [...document.querySelectorAll('.padk')].map(m => { const r = m.getBoundingClientRect(), p = m.parentElement.getBoundingClientRect(), cs = getComputedStyle(m);
  const h = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
  return { on: (m.parentElement.id || m.parentElement.className), k: m.dataset.k, shown: cs.display !== 'none', mark: [Math.round(r.left), Math.round(r.top), Math.round(r.width), Math.round(r.height)],
    btn: [Math.round(p.left), Math.round(p.top), Math.round(p.width), Math.round(p.height)], offscreen: r.left < 0 || r.top < 0 || r.right > innerWidth || r.bottom > innerHeight,
    covered: !!h && h !== m && !m.contains(h) }; }))()"""
IDS = {'xbox': 'Xbox Wireless Controller (STANDARD GAMEPAD Vendor: 045e Product: 0b13)', 'ps': 'DualSense Wireless Controller (STANDARD GAMEPAD Vendor: 054c Product: 0ce6)', 'nin': 'Pro Controller (STANDARD GAMEPAD Vendor: 057e Product: 2009)'}
with sync_playwright() as pw:
    for (w, h) in [(390, 844), (320, 640), (1280, 800)]:
        for fam, pid in IDS.items():
            g = Game(pw, GAMEF, w, h); g.ev("SHIP.device && SHIP.device.settings && (SHIP.device.settings.tips = false)"); g.step(10)
            g.page.evaluate(f"window.__plug(0, {json.dumps(pid)})"); g.step(2)
            g.page.evaluate("window.__btn(0, 1, 1)"); g.step(2); g.page.evaluate("window.__btn(0, 1, 0)"); g.step(12)
            rs = g.ev(RECTS); fam_game = g.ev("[PAD.fam, padFam()]"); toast = g.ev("[toastEl.classList.contains('show'), document.getElementById('tt').textContent, document.getElementById('tx').textContent]")
            g.page.screenshot(path=f'{OUT}/marks_{w}x{h}_{fam}.png')
            print(f'{w}x{h} {fam} (game says {fam_game}) toast {toast}')
            for r in rs: print('   ', r)
            if fam == 'xbox':
                g.page.mouse.click(w // 2, h // 2); g.step(4)
                print('   after a click: shown', [r['k'] for r in g.ev(RECTS) if r['shown']], 'body.pad', 'pad' in g.ev('document.body.className'))
                # unplug while in use: pause, its line
                g.page.evaluate("window.__btn(0, 1, 1)"); g.step(2); g.page.evaluate("window.__btn(0, 1, 0)"); g.step(2)
                g.page.evaluate("window.__unplug(0)"); g.step(3)
                card = g.ev("(() => { const c = document.getElementById('pauseCard'); return c ? [PAUSE.on, c.textContent] : null; })()")
                print('   unplugged in use: pause card', card, 'marks shown', [r['k'] for r in g.ev(RECTS) if r['shown']], 'body.pad', 'pad' in g.ev('document.body.className'))
                g.page.screenshot(path=f'{OUT}/unplug_{w}x{h}.png')
                g.page.mouse.click(w // 2, h // 2); g.step(3)
                card = g.ev("(() => { const c = document.getElementById('pauseCard'); return c ? [PAUSE.on, c.textContent] : null; })()")
                print('   tapped the card: ', card)
            print('    errors', [e for e in g.errors if 'error' in e][:3])
            g.close()
