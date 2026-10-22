# PR9: after the pad moves the highlight in the device and a touch hands back, is any outline left on the focused button?
import sys, os, json
src = open('controller_check.py').read(); sys.argv = [sys.argv[0], 'starship-cadet.html', 'none']
exec(src.split('def part_off')[0].replace("__file__.replace('controller_check.py', 'cadet_test.py')", "'cadet_test.py'"))
from playwright.sync_api import sync_playwright
O = "(() => { const a = document.activeElement, cs = a && getComputedStyle(a); return a && [a.id || a.tagName, a.textContent.trim().slice(0, 16), cs.outlineStyle, cs.outlineWidth, cs.boxShadow.slice(0, 40), a.matches(':focus-visible'), document.body.classList.contains('pad')]; })()"
with sync_playwright() as pw:
    p = Pad(pw, ON); p.plug(); p.press('x'); p.log()
    p.press('y'); p.step(3); p.press('down'); p.step(2)
    print('pad in use', p.ev(O))
    p.js("document.getElementById('devBody').dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))"); p.step(2)
    print('after a touch (synthetic pointerdown)', p.ev(O))
    p.g.page.mouse.move(5, 5); p.g.page.mouse.move(40, 60); p.step(2)
    print('after a real mouse move', p.ev(O))
    p.close()
