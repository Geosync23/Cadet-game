import sys, json
CC = sys.argv[1]; GAMEF = sys.argv[2]; sys.argv = [CC, GAMEF, 'none']
__file__ = CC; exec(open(CC).read().split('\nwith sync_playwright() as pw:')[0])
src = ON_SRC
TX = "[[...document.body.querySelectorAll('*')].filter(e => e.tagName !== 'SCRIPT' && e.tagName !== 'STYLE' && e.checkVisibility({visibilityProperty: true}) && e.getBoundingClientRect().width > 0).map(e => e.id || e.className || e.tagName).join(','), document.getElementById('tt').textContent, document.getElementById('tx').textContent, toastEl.classList.contains('show'), typeof PAD === 'object' ? PAD.used : null]"
with sync_playwright() as pw:
    for mode, presses in (('none', []), ('pad', ['B'])):
        r = Run(pw, src, 'probe_' + mode, mode=mode, plug={} if mode != 'none' else None, touch=True)
        r.ev("SHIP.device && SHIP.device.settings && (SHIP.device.settings.tips = false)"); r.step(10)
        for b in presses: r.press(b); r.step(4); print(mode, 'after', b, r.ev(TX))
        r.step(PRE - 10 - 7 * len(presses)); print(mode, 'before tap0', r.ev(TX))
        r.page.mouse.click(450, 380); r.step(90); print(mode, 'tap0', r.ev(TX))
        r.page.touchscreen.tap(700, 300); r.step(90); print(mode, 'tap1', r.ev(TX)); r.close()
