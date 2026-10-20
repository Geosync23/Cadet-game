# Starship Cadet: Dev mode check (section 25, the Dev mode engineer; plans/devmode-plan.html v3.1 on claude/devmode-plan)
# Opens the game in a phone-sized browser (390 x 844) with real saving, the way the user's Dev link does, and checks:
#   off:   without #dev nothing of Dev mode exists (no tag, no sheet, no class, no "-dev" keys in storage); ?nosave with
#          #dev is not Dev mode either (Dev mode needs its own save)
#   real:  a real game saved first stays byte for byte the same through a Dev session (#dev, then #dev.debug), every
#          Dev key ends in "-dev" or is one of Dev mode's own, and the real game still writes its save afterwards
#   card:  in Dev mode the place-and-clock card has the DEV tag and opens the sheet "Dev mode: not your real game"
# Setup and environment as for cadet_test.py (CADET_WORK, CADET_CHROME).
# Run:  python3 devmode_check.py BUILD.html          Good is DEVMODE CHECK OK (exit 0); a failure exits 1.
import sys, os, re, json, pathlib
exec(open(__file__.replace('devmode_check.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright

ok = True
def fail(msg):
    global ok
    ok = False
    print('FAIL', msg)
def check(cond, msg):
    if not cond: fail(msg)
    return cond

REAL = ('starship-cadet-save', 'starship-cadet-arrived')
DEV_OWN = ('starship-cadet-dev-mark', 'starship-cadet-dev-undo')   # Dev mode's Mark and Undo (D2, D4)
GAME = sys.argv[1]
TMP = WORK / 'test' / '_devmode_check.html'
TMP.write_text(instrument(pathlib.Path(GAME).read_text()))

class Page:
    """One tab in a browser context: the context keeps localStorage (file:// is one origin) across tabs and reloads."""
    def __init__(self, ctx, suffix):
        self.errors = []
        self.page = ctx.new_page()
        self.page.on('pageerror', lambda e: self.errors.append(f'pageerror: {e}'))
        self.page.on('console', lambda m: m.type == 'error' and self.errors.append(f'error: {m.text}'))
        self.page.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
        self.page.add_init_script(INIT)
        self.go(suffix)
    def go(self, suffix):
        self.page.goto('file://' + str(TMP) + suffix)
        self.ready()
    def ready(self):
        self.page.wait_for_function('window.__sc !== undefined', timeout=90000)
        self.page.add_style_tag(content='*,*::before,*::after{transition:none!important;animation:none!important}')
        self.ev("(() => { const rr = renderer.render.bind(renderer); window.__draw = false; renderer.render = (s, c) => { if (window.__draw) rr(s, c); }; })()")   # no drawing (slow headless), but for shots
        self.step(20)
    def reload(self):
        self.page.reload(); self.ready()
    def ev(self, src):
        return self.page.evaluate('s => window.__sc(s)', src)
    def step(self, n, dt=1000 / 30):
        self.page.evaluate(f'window.__step({n}, {dt})')
    def sign(self):                                   # the arrival's manifest, if it's up
        if self.page.locator('text=Sign and go aboard').count():
            self.page.fill('form input', 'Ada'); self.page.click('text=Sign and go aboard'); self.step(30)
    def shot(self, path):
        self.page.evaluate('window.__draw = true'); self.step(1); self.page.screenshot(path=path); self.page.evaluate('window.__draw = false')
    def close(self):
        self.page.close()

def store(pg):
    return pg.page.evaluate('() => Object.fromEntries(Object.keys(localStorage).map(k => [k, localStorage.getItem(k)]))')

def dev_keys_ok(keys, where):
    for k in keys:
        check(k in REAL or k.endswith('-dev') or k in DEV_OWN, f'{where}: a storage key that is neither the real game\'s nor Dev mode\'s: {k}')

def part_off(ctx):
    pg = Page(ctx, ''); pg.sign(); pg.step(30)
    st = store(pg)
    check(pg.ev('DEVMODE') is False, 'off: DEVMODE is on without #dev')
    check(all(k in REAL for k in st), f'off: storage holds more than the real game\'s keys: {sorted(st)}')
    check('starship-cadet-save' in st, 'off: the real game wrote no save')
    check(pg.ev("!document.getElementById('dmTag') && !document.getElementById('dmSheet') && !document.body.classList.contains('devmode')"), 'off: Dev mode\'s tag, sheet or class exists without #dev')
    check(pg.ev("getComputedStyle(document.querySelector('.hud')).pointerEvents") == 'none', 'off: the card takes taps without #dev')
    check(not pg.errors, f'off: errors {pg.errors[:3]}')
    pg.close()
    pg = Page(ctx, '?nosave#dev')
    check(pg.ev('DEVMODE') is False and pg.ev("!document.getElementById('dmTag')"), 'off: ?nosave with #dev turned Dev mode on')
    pg.close()
    print('  off: nothing of Dev mode without #dev; real keys only:', sorted(st))

def part_real(ctx):
    # the real game exists (part_off made it); play on a little so it's a real save, then keep its bytes
    pg = Page(ctx, ''); pg.ev('saveGame()'); real = {k: v for k, v in store(pg).items() if k in REAL}; pg.close()
    check('starship-cadet-save' in real, 'real: no real save to protect')
    for suffix in ('#dev', '#dev.debug'):
        pg = Page(ctx, suffix)
        check(pg.ev('DEVMODE') is True, f'real: {suffix} did not turn Dev mode on')
        check(pg.ev("SAVE_KEY === 'starship-cadet-save-dev' && INTRO_KEY === 'starship-cadet-arrived-dev'"), f'real: {suffix}: the save names are not the Dev ones')
        pg.sign(); pg.step(60); pg.ev('saveGame()'); pg.reload(); pg.step(30); pg.ev('saveGame()')
        st = store(pg); dev_keys_ok(st, suffix)
        check('starship-cadet-save-dev' in st, f'real: {suffix}: no Dev save written')
        for k, v in real.items():
            check(st.get(k) == v, f'real: {suffix}: the real game\'s {k} changed in a Dev session')
        check(not pg.errors, f'real: {suffix}: errors {pg.errors[:3]}')
        pg.close()
    pg = Page(ctx, ''); pg.step(200); pg.ev('SHIP.time.min += 90; saveGame()')
    after = store(pg).get('starship-cadet-save')
    check(after and after != real['starship-cadet-save'] and json.loads(after)['time']['min'] != json.loads(real['starship-cadet-save'])['time']['min'], 'real: the real game no longer writes its save after a Dev session')
    check(pg.ev('!SAVED || !SAVED.dev'), 'real: the real save carries Dev state')
    pg.close()
    print('  real: the real save byte-identical through #dev and #dev.debug, and still writes after')

def part_card(ctx):
    pg = Page(ctx, '#dev'); pg.sign()
    check(pg.ev("document.getElementById('dmTag') && document.getElementById('dmTag').textContent") == 'DEV', 'card: no DEV tag on the card')
    check(pg.ev("getComputedStyle(document.querySelector('.hud')).pointerEvents") == 'auto', 'card: the card takes no taps')
    pg.page.click('.hud'); pg.step(2)
    check(pg.ev('DM_UI.open') and pg.ev("document.getElementById('dmT').textContent") == 'Dev mode: not your real game', 'card: tapping the card did not open the sheet')
    check(pg.ev("document.querySelectorAll('#dmSheet .dmTabs button').length") == 6, 'card: the sheet has not six tabs')
    small = pg.ev("[...document.querySelectorAll('#dmSheet button')].filter(b => b.offsetParent && b.getBoundingClientRect().height < 44).map(b => b.textContent)")
    check(not small, f'card: buttons under 44px: {small}')
    pg.page.click('.dmClose'); pg.step(2)
    check(not pg.ev('DM_UI.open'), 'card: the sheet did not close')
    check(not pg.errors, f'card: errors {pg.errors[:3]}')
    pg.close()
    print('  card: DEV tag, the sheet opens and closes, six tabs, buttons 44px')

with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
    for name, part in (('off', part_off), ('real', part_real), ('card', part_card)):
        try: part(ctx)
        except Exception as e: fail(f'{name}: stopped: {str(e)[:300]}')
    b.close()

print('DEVMODE CHECK OK' if ok else 'DEVMODE CHECK FAILED')
sys.exit(0 if ok else 1)
