# PR9: P1's panels, checked from the page, not from padItems: for each panel the check opens, every visible clickable
# (cursor:pointer, an onclick property, role=button, a button or input) that the highlight can't land on (not in
# padItems and not inside one of them). Run from the build's folder: python3 p9_reach.py BUILD.html
import sys, os, json
src = open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[1])), 'controller_check.py')).read()
sys.argv = [sys.argv[0], sys.argv[1], 'none']
exec(src.split('def part_off')[0].replace("__file__.replace('controller_check.py', 'cadet_test.py')", repr(os.path.join(os.path.dirname(os.path.abspath(sys.argv[1])), 'cadet_test.py'))))
CLICK = """(() => { const L = padLayer(); if (!L) return null; const root = L === PAD_HUD ? document.body : L, items = padItems(L);
  const vis = e => e.getClientRects().length && getComputedStyle(e).visibility !== 'hidden' && !e.closest('[hidden]') && e.getAttribute('aria-hidden') !== 'true';
  const out = [];
  for (const e of root.querySelectorAll('*')) {
    if (!vis(e) || items.includes(e) || items.some(i => i.contains(e) || e.contains(i))) continue;
    const cs = getComputedStyle(e), clicky = e.onclick || cs.cursor === 'pointer' || e.getAttribute('role') === 'button' || /^(BUTTON|INPUT|SELECT|TEXTAREA|A)$/.test(e.tagName);
    if (!clicky || cs.pointerEvents === 'none') continue;
    if (e.parentElement && out.some(o => o.el === e.parentElement)) continue;
    out.push({ el: e, d: e.tagName.toLowerCase() + (e.id ? '#' + e.id : '') + (e.className && typeof e.className === 'string' ? '.' + e.className.split(' ')[0] : '') + ' ' + (e.textContent || '').trim().slice(0, 24) + (e.onclick ? ' [onclick]' : '') + ' ' + cs.cursor });
  }
  return { layer: L.id || L.className || 'hud', items: items.length, unreach: out.map(o => o.d) }; })()"""
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    p = Pad(pw, ON); p.plug(); p.press('x'); p.log()
    def look(what):
        p.step(3); r = p.ev(CLICK); print(what, json.dumps(r)); return r
    p.press('up'); look('screen edge'); p.press('b'); p.step(2)
    p.press('menu'); look('pause'); p.press('menu'); p.step(2)
    for js, what in [('openLiftPanel()', 'lift'), ('alarmOpen()', 'alarm'), ("trkOpen ? trkOpen() : null", 'tracked'), ('ixBoard.open()', 'job board'),
                     ("DECK_CREW.some(a => { chatOpen(a.p); const c = document.getElementById('chat'); return c && !c.hidden; })", 'chat'),
                     ('ladderPanel()', 'ladder'), ('queueAsk()', 'queue')]:
        try: p.ev(js)
        except Exception as e: print(what, 'open failed', str(e)[:80]); continue
        look(what); p.press('b'); p.step(3)
    p.press('y'); look('device home')
    apps = p.ev("[...DEVICE_APPS.values()].filter(a => !(a.hidden && a.hidden()) && a.id !== 'home' && a.id !== 'boot').map(a => a.id)")
    for app in apps:
        p.ev(f'deviceShow({json.dumps(app)})'); look('app ' + app); p.press('b'); p.step(2)
    p.close()
