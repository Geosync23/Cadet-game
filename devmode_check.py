# Starship Cadet: Dev mode check (section 25, the Dev mode engineer; plans/devmode-plan.html v3.1 on claude/devmode-plan)
# Opens the game in a phone-sized browser (390 x 844) with real saving, the way the user's Dev link does, and checks:
#   off:   without #dev nothing of Dev mode exists (no tag, no sheet, no class, no "-dev" keys in storage); ?nosave with
#          #dev is not Dev mode either (Dev mode needs its own save)
#   real:  a real game saved first stays byte for byte the same through a Dev session (#dev, then #dev.debug), every
#          Dev key ends in "-dev" or is one of Dev mode's own, and the real game still writes its save afterwards
#   store: the space check refuses a Dev copy that would crowd the real save (nothing removed, the real game still
#          writes); Undo my last Dev action brings the save back exactly; Copy my real game copies it byte for byte
#          and leaves it alone; Clear Dev save takes every Dev key away and starts a new Dev game
#   clock: refused during the arrival evening; from a Skip-to-Monday Dev game, +7 days and +1 day pass with every
#          workday excused (no miss, no leave spent), needs kept, the crew on the deck; a jump frozen under its fade;
#          clocked in you stay clocked in; Top up needs; a jump past a first-week meeting leaves the notice
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
    def ev_reload(self, src):                         # a Dev action that reloads the page itself
        with self.page.expect_navigation(timeout=90000):
            self.page.evaluate('s => window.__sc(s)', src)
        self.page.wait_for_function('window.__sc !== undefined', timeout=90000)
        first = self.page.evaluate('() => localStorage.getItem("starship-cadet-save-dev")')   # before any frame
        self.ready(); return first
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

def part_store(ctx):
    pg = Page(ctx, '#dev'); pg.sign(); pg.step(30)
    real0 = store(pg).get('starship-cadet-save')
    # the space check: junk fills the site up to just short of what Dev mode leaves free; the Undo copy is refused
    used = pg.ev('devmodeUsed()'); room = pg.ev('DM_ROOM - Math.max(DM_KEEP, 2 * (localStorage.getItem(DM_REAL.save) || "").length)')
    pg.page.evaluate(f'n => localStorage.setItem("zz-junk", "x".repeat(n))', max(0, room - used - 5000))
    before = store(pg)
    check(pg.ev("devmodeRun('Test', () => null)") is False and 'space' in pg.ev('DM_UI.msg'), f'store: a Dev copy over the space limit was not refused: {pg.ev("DM_UI.msg")}')
    after = store(pg)
    check(set(after) == set(before) and 'starship-cadet-dev-undo' not in after, 'store: the space check changed what is stored')
    real_pg = Page(ctx, ''); real_pg.ev('SHIP.time.min = (SHIP.time.min + 37) % 1440; saveGame()')
    r1 = store(real_pg).get('starship-cadet-save'); real_pg.close()
    check(r1 and r1 != real0, 'store: with Dev mode\'s storage full, the real game could not write its save')
    pg.page.evaluate('() => localStorage.removeItem("zz-junk")')
    # the real save as it is now is the one Copy my real game must copy
    real0 = r1
    # Undo my last Dev action, round trip
    pg.ev('saveGame()'); s0 = store(pg)['starship-cadet-save-dev']
    check(pg.ev("devmodeRun('Test: an hour on', () => { SHIP.time.min = Math.min(1439, SHIP.time.min + 60); return null; })") is True, f'store: a Dev action was refused: {pg.ev("DM_UI.msg")}')
    s1 = store(pg)['starship-cadet-save-dev']
    check(s1 != s0, 'store: the Dev action changed nothing in the Dev save')
    check(pg.ev('devmodeRead(DM_KEY.undo).label') == 'Test: an hour on', 'store: no Undo kept')
    back = pg.ev_reload('devmodeUndo()')
    check(back == s0, 'store: Undo did not bring the Dev save back byte for byte')
    check(pg.ev('!devmodeRead(DM_KEY.undo)'), 'store: the Undo is still there after undoing')
    # Copy my real game
    got = pg.ev_reload('devmodeCopyReal()')
    check(got == real0, 'store: Copy my real game did not copy the real save byte for byte')
    check(store(pg).get('starship-cadet-save') == real0, 'store: Copy my real game changed the real save')
    check(pg.ev('!!devmodeRead(DM_KEY.undo)'), 'store: Copy my real game kept no Undo')
    # Clear Dev save
    pg.ev_reload('devmodeClear()')
    st = store(pg)
    check('starship-cadet-dev-undo' not in st and 'starship-cadet-dev-mark' not in st and st.get('starship-cadet-save') == real0, f'store: Clear left Dev keys or touched the real save: {sorted(st)}')
    check(pg.ev('SHIP.time.day') == 0, 'store: Clear did not start a new Dev game (by shuttle)')
    dev_keys_ok(st, 'store')
    check(not pg.errors, f'store: errors {pg.errors[:3]}')
    pg.close()
    print(f'  store: space check refused at {round(used / 1e3)}k + junk, real save still writes; Undo, Copy my real game, Clear')

def part_clock(b):
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
    pg = Page(ctx, '#dev')
    run = lambda label, to: pg.ev(f"devmodeRun('Clock: {label}', () => devmodeSkipTo({to}), devmodeArrival)")
    check(run('+1 hour', 'shipNow() + 60') is False and 'arrival' in pg.ev('DM_UI.msg'), f'clock: not refused during the arrival evening: {pg.ev("DM_UI.msg")}')
    # the first week's meeting notice, on paper: the arrival evening over, Day 1 05:00, a jump to Day 2 10:00
    pg.ev('SHIP.intro.step = null; setShipNow(5 * 60); updateClock()')
    miss = pg.ev('devmodeMissed(shipNow(), 1440 + 600)')
    check(miss == ['d1-briefing', 'd2-solo'], f'clock: the first week\'s meetings passed: {miss}')
    pg.ev("devmodeRun('Clock: to Day 2', () => devmodeSkipTo(1440 + 600))")
    check('Skipped: the Day 1 briefing counted as missed' in pg.ev('devmodeState().note') and 'solo job' in pg.ev('devmodeState().note'), f'clock: no skipped-meeting notice: {pg.ev("devmodeState().note")}')
    # a Dev game the Skip to Monday way: Day 1, 06:00
    pg.ev('newGameStart(false); introSkip(); devmodeState().ex = []; devmodeState().note = ""'); pg.step(10)
    check(pg.ev('clockText()') == 'Day 1, Monday 06:00', f'clock: the Skip-to-Monday game starts at {pg.ev("clockText()")}')
    t = pg.page.evaluate('() => { const t = performance.now(); return t; }')
    import time as _t; t0 = _t.time()
    check(run('+7 days', 'shipNow() + 7 * 1440') is True, f'clock: +7 days refused: {pg.ev("DM_UI.msg")}')
    secs = _t.time() - t0; pg.step(10)
    n0 = pg.ev('JSON.stringify(SHIP.player.needs)')
    check(pg.ev('clockText()') == 'Day 8, Monday 06:00', f'clock: +7 days landed at {pg.ev("clockText()")}')
    t0 = _t.time(); check(run('+1 day', 'shipNow() + 1440') is True, 'clock: +1 day refused'); secs1 = _t.time() - t0
    check(pg.ev('JSON.stringify(SHIP.player.needs)') == n0, 'clock: needs changed over a Dev jump')
    pg.step(30)
    C = pg.ev('({ ms: SHIP.career.ms, l: SHIP.career.l, st: SHIP.career.st, ca: SHIP.career.ca, ex: devmodeState().ex, off8: careerOff(8), on8: playerShiftOn(8), crew: DECK_CREW.length, day: clockText() })')
    check(C['day'].startswith('Day 9, Tuesday 06:0'), f'clock: +1 day landed at {C["day"]}')
    check(C['ms'] == 0 and C['st'] == 0 and not C['ca'], f'clock: a skipped workday counted as missed: {C}')
    check(C['l'] == 3, f'clock: leave was spent: {C}')
    check(C['ex'] == [1, 2, 3, 4, 5, 8] and C['off8'] and not C['on8'], f'clock: the excused days: {C}')
    check(C['crew'] > 0, 'clock: nobody on the deck after the jump')
    missed = pg.ev("SHIP.mail.filter(m => /missed|summons|warning/i.test(m.subject || '')).map(m => m.subject)")
    check(not missed, f'clock: Mail about missing work: {missed}')
    # clocked in, you stay clocked in
    pg.ev("devmodeRun('Clock: to 08:55', () => devmodeSkipTo(devmodeNext(8 * 60 + 55)))"); pg.ev('careerClock()')
    pg.ev("devmodeRun('Clock: to 16:55', () => devmodeSkipTo(devmodeNext(16 * 60 + 55)))"); pg.step(60)
    C = pg.ev('({ in9: careerClockedIn(9), out9: careerClockedOut(9), ex: devmodeState().ex, ms: SHIP.career.ms, day: clockText() })')
    check(C['in9'] and not C['out9'] and 9 not in C['ex'] and C['ms'] == 0, f'clock: clocked in, the jump didn\'t keep you clocked in: {C}')
    # Top up needs, through the panel's own way (the fade, frozen meanwhile)
    pg.ev('SHIP.player.needs.hunger = 20; devmodeOpen(true); DM_UI.tab = "quick"; devmodeDraw()')
    m0 = pg.ev('SHIP.time.min'); pg.page.evaluate("[...document.querySelectorAll('#dmSheet button')].find(b => b.textContent === 'Top up needs').click()"); pg.step(15)
    check(pg.ev('SHIP.time.min') == m0 and pg.ev('freezeSync()'), 'clock: the ship ran under a Dev action\'s fade')
    pg.page.wait_for_timeout(800); pg.step(5)
    check(all(v > 99.9 for v in pg.ev('Object.values(SHIP.player.needs)')), f'clock: Top up needs: {pg.ev("JSON.stringify(SHIP.player.needs)")}')
    check(pg.ev('!freezeSync()'), 'clock: still frozen after the action')
    check(not pg.errors, f'clock: errors {pg.errors[:3]}')
    pg.close(); ctx.close()
    print(f'  clock: arrival refused; meeting notice; +7 days in {secs:.1f} s, +1 day in {secs1:.1f} s; excused {C["ex"]}, no miss, leave kept, needs kept; clocked in kept; Top up frozen under the fade')

with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
    for name, part in (('off', part_off), ('real', part_real), ('card', part_card), ('store', part_store)):
        try: part(ctx)
        except Exception as e: fail(f'{name}: stopped: {str(e)[:300]}')
    try: part_clock(b)
    except Exception as e: fail(f'clock: stopped: {str(e)[:300]}')
    b.close()

print('DEVMODE CHECK OK' if ok else 'DEVMODE CHECK FAILED')
sys.exit(0 if ok else 1)
