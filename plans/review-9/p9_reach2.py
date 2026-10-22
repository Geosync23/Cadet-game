import sys, os, json
src = open('controller_check.py').read(); sys.argv = [sys.argv[0], 'starship-cadet.html', 'none']
exec(src.split('def part_off')[0].replace("__file__.replace('controller_check.py', 'cadet_test.py')", "'cadet_test.py'"))
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    p = Pad(pw, ON); p.plug(); p.press('x'); p.log()
    p.ev('openLiftPanel()'); p.step(3)
    print('lift here', p.ev("[...document.querySelectorAll('#lift .deckbtn')].filter(b => /You are here/.test(b.textContent)).map(b => [b.disabled, b.getAttribute('aria-disabled')])"))
    p.press('b'); p.step(2); p.ev('alarmOpen()'); p.step(3)
    print('alarmDn', p.ev("(() => { const b = document.getElementById('alarmDn'); return [b.disabled, b.getAttribute('aria-disabled'), b.className]; })()"))
    p.press('b'); p.step(2); p.press('y'); p.step(3)
    print('devBack on home', p.ev("(() => { const b = document.getElementById('devBack'); const cs = getComputedStyle(b); return [b.disabled, b.getAttribute('aria-hidden'), cs.visibility, cs.opacity, b.closest('[aria-hidden]') && b.closest('[aria-hidden]').id, b.getBoundingClientRect().width]; })()"))
    p.ev("deviceShow('maps')"); p.step(3)
    print('maps svg', p.ev("""(() => { const s = [...document.querySelectorAll('#device svg')].find(e => e.onclick); return s && [String(s.onclick).slice(0, 400), s.getBoundingClientRect().width, s.getBoundingClientRect().height, s.parentElement.id || s.parentElement.className]; })()"""))
    print('maps items', p.ev("padItems(padLayer()).slice(0, 25).map(e => e.tagName + ' ' + (e.textContent || e.getAttribute('aria-label') || '').trim().slice(0, 20))"))
    p.close()
