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
#   move:  Take me to every room on every deck lands you in that room (rooms nobody can walk into are listed, not
#          failed), the testing spots and your next appointment; the clock doesn't move; refused during the escort and
#          inside a meeting; Mark here then Back to mark reloads into the same save, byte for byte
#   slow:  the reload after Undo and Back to mark held back 6 s (a phone on a weak link; DR1's probe): the kept save stays
#          put while the old page waits, and the new page has it (the Undo happened, its record used up)
#   career: the Career tab (Stop 2): xp, the next band, the next training, a tool, the rank by hand, each undoable; the
#          promotion test opened on Day 8 with only the day missing (ladderOpen), passed, and Next step to the ceremony
#   set:   Set career (Stop 2): the table's days are CAREER_LADDER's; Days 2, 10, 12, 26 from new Dev games land at 06:00
#          with the table's career, in your bed's room, no miss, no first-week meeting notes, no sick day; Day 11 opens
#          no trained row again; two Set careers to Day 12 give the same save; starting friendships; the Day 9 test
#          and Day 10 promotion beats; the panel's way (a day at a time, the progress shown, one save); Undo; the tab
#   card:  in Dev mode the place-and-clock card has the DEV tag and opens the sheet "Dev mode: not your real game"
#   trad:  Traditions (Stop 1b): refused on Day 0; five kinds started (in 20 minutes, at the usual time, tomorrow) with
#          people going and at the room; whose for a birthday; a clash with a Dev start, too late, a usual time gone
#          refused; a calendar tradition in the same room gives way; its Mail now; the starts ride in the Dev save and
#          through Undo; Stop it puts the day back to its calendar; the list, the search, 44px buttons
#   jumps: Jump to's groundwork (plan v4.4, J0): the jump list sound; the week-slow offset; Set career to Day 36 twice (the
#          same save, timed) with your answers put in on the way (Calder's question Engines, the offer Stay), settled Stay,
#          the endgame, the Day 26 milestones kept (CA1's F1); a Go jump settles Go on Day 35; Senior Officer and Engine
#          Specialist by hand; the panel's Stop; the Jump to and Set career tabs at 390 px (DEVMODE_SHOTS=folder: a shot)
#   beats: J1's Career and Nights jumps: each lands at its time and room and the game books or starts its beat (played
#          where it needs you up: Power safety, the nights once clocked in); Undo; one jump twice in fresh browsers
#   ending1: J3's answers row and the ending's list at 390 px; the offer, still open, before the address; Calder's four answers give their posts
#   ending2: J3's goodbye, end page, staying on, the slower career's offer; the Traditions card's Its next showing
#   events1: J2's Ship events jumps: each lands at its day, time and room with the event running by the calendar; Undo; one twice
#   events2: J2's Running now card: threads − and +, Next phase, Its meeting, settled greys the threads, End and keep, Undo
# Setup and environment as for cadet_test.py (CADET_WORK, CADET_CHROME).
# Run:  python3 devmode_check.py BUILD.html [part ...]   (parts: only those)   Good is DEVMODE CHECK OK (exit 0); a failure exits 1.
import sys, os, re, json, pathlib
exec(open(__file__.replace('devmode_check.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
RUN_ID = f'p{os.getpid()}_'   # FX18-1: this run's copies carry the process id (two runs in one CADET_WORK never open each other's), gone at exit
__import__('atexit').register(lambda: [f.unlink(missing_ok=True) for f in (WORK / 'test').glob(f'*_{RUN_ID}*') if f.is_file()])
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
ONLY = set(sys.argv[2:])                          # optional: run only these parts (e.g. trad)
SHOTS = pathlib.Path(os.environ['DEVMODE_SHOTS']) if os.environ.get('DEVMODE_SHOTS') else None   # (J0) a folder for the new tabs' screenshots, if wanted
TMP = WORK / 'test' / ('_devmode_check_' + RUN_ID + '.html')
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
    check(pg.ev("DM_SPEED.sizes.length === 0 && DM_SPEED.fr.length === 0"), 'off: the Speed card measured without #dev (opt #8)')
    check(not pg.errors, f'off: errors {pg.errors[:3]}')
    pg.close()
    pg = Page(ctx, '?nosave#dev')
    check(pg.ev('DEVMODE') is False and pg.ev("!document.getElementById('dmTag')"), 'off: ?nosave with #dev turned Dev mode on')
    pg.close()
    print('  off: nothing of Dev mode without #dev; real keys only:', sorted(st))

def part_real(ctx):
    # the real game exists (part_off made it); play on a little so it's a real save, then keep its bytes
    for arrived, suffix in ((False, '#dev'), (True, '#dev.debug'), (True, '#dev')):   # DR1: with and without the real arrived key
      pg = Page(ctx, '')
      pg.page.evaluate('a => a ? localStorage.setItem("starship-cadet-arrived", "1") : localStorage.removeItem("starship-cadet-arrived")', arrived)
      pg.ev('saveGame()'); real = {k: v for k, v in store(pg).items() if k in REAL}; pg.close()
      check('starship-cadet-save' in real and ('starship-cadet-arrived' in real) == arrived, f'real: the real game to protect isn\'t there: {sorted(real)}')
      if True:
        pg = Page(ctx, suffix)
        check(pg.ev('DEVMODE') is True, f'real: {suffix} did not turn Dev mode on')
        check(pg.ev("SAVE_KEY === 'starship-cadet-save-dev' && INTRO_KEY === 'starship-cadet-arrived-dev'"), f'real: {suffix}: the save names are not the Dev ones')
        pg.sign(); pg.step(60); pg.ev('introSkip(); saveGame()'); pg.reload(); pg.step(30); pg.ev('saveGame()')
        st = store(pg); dev_keys_ok(st, suffix)
        check('starship-cadet-save-dev' in st and st.get('starship-cadet-arrived-dev') == '1', f'real: {suffix}: no Dev save or Dev arrived key written: {sorted(st)}')
        check({k: v for k, v in st.items() if k in REAL} == real, f'real: {suffix} (real arrived key {arrived}): the real game\'s keys or bytes changed in a Dev session')
        check(not pg.errors, f'real: {suffix}: errors {pg.errors[:3]}')
        pg.close()
    pg = Page(ctx, ''); pg.step(200); pg.ev('SHIP.time.min += 90; saveGame()')
    after = store(pg).get('starship-cadet-save')
    check(after and after != real['starship-cadet-save'] and json.loads(after)['time']['min'] != json.loads(real['starship-cadet-save'])['time']['min'], 'real: the real game no longer writes its save after a Dev session')
    check(pg.ev('!SAVED || !SAVED.dev'), 'real: the real save carries Dev state')
    pg.close()
    print('  real: the real keys (with and without the arrived key) byte-identical through #dev and #dev.debug, the Dev arrived key written, and the real game still writes after')

def part_card(ctx):
    pg = Page(ctx, '#dev'); pg.sign()
    check(pg.ev("document.getElementById('dmTag') && document.getElementById('dmTag').textContent") == 'DEV', 'card: no DEV tag on the card')
    check(pg.ev("getComputedStyle(document.querySelector('.hud')).pointerEvents") == 'auto', 'card: the card takes no taps')
    pg.page.click('.hud'); pg.step(2)
    check(pg.ev('DM_UI.open') and pg.ev("document.getElementById('dmT').textContent") == 'Dev mode: not your real game', 'card: tapping the card did not open the sheet')
    check(pg.ev("document.querySelectorAll('#dmSheet .dmTabs button').length") == 7, 'card: the sheet has not seven tabs (six, and Speed: opt #8)')
    small = pg.ev("[...document.querySelectorAll('#dmSheet button')].filter(b => b.offsetParent && b.getBoundingClientRect().height < 44).map(b => b.textContent)")
    check(not small, f'card: buttons under 44px: {small}')
    pg.page.click('#dmSheet .dmTabs button[data-tab="speed"]'); pg.step(40)   # the Speed card (opt #8, the render seat)
    sp = pg.ev("(document.getElementById('dmSpeed') || {}).textContent || ''")
    check(sp.startswith('Screen: ' + str(pg.ev('innerWidth')) + ' x ' + str(pg.ev('innerHeight')) + ' CSS px') and 'Draw calls:' in sp and 'shaders' in sp, f'card: the Speed card says {sp[:120]!r}')
    pg.page.click('.dmClose'); pg.step(2)
    check(not pg.ev('DM_UI.open'), 'card: the sheet did not close')
    check(not pg.errors, f'card: errors {pg.errors[:3]}')
    pg.close()
    print('  card: DEV tag, the sheet opens and closes, seven tabs, buttons 44px, the Speed card')

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
    # (each new game here gets the Dev seed, DM_SEED: no sick day before Day 46, so the excused days are the same every run;
    # a random seed gave a sick day about 1 run in 28, with nothing to excuse)
    # a Dev game the Skip to Monday way; DR1's case: Day 2 08:00 to 09:30 leaves the day open (clock in still works)
    pg.ev('newGameStart(false); introSkip(); careerInit(); SHIP.career.gs = DM_SEED; devmodeState().ex = []; devmodeState().note = ""'); pg.step(10)
    pg.ev("devmodeRun('Clock', () => devmodeSkipTo(1440 + 8 * 60)); devmodeRun('Clock', () => devmodeSkipTo(1440 + 9 * 60 + 30))")
    check(pg.ev('devmodeState().ex') == [] and pg.ev('playerShiftOn(2)') and pg.ev("careerClock() === 'in'"), f'clock: Day 2 08:00 to 09:30 closed the day: {pg.ev("devmodeState().ex")}')
    pg.ev('newGameStart(false); introSkip(); careerInit(); SHIP.career.gs = DM_SEED; devmodeState().ex = []; devmodeState().note = ""'); pg.step(10)
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
    check(C['ex'] == [8] and C['off8'] and not C['on8'], f'clock: the excused days (only past the first week, a jump past 12:30): {C}')
    check(C['crew'] > 0, 'clock: nobody on the deck after the jump')
    missed = pg.ev("SHIP.mail.filter(m => /missed|summons|warning/i.test(m.subject || '')).map(m => m.subject)")
    check(not missed, f'clock: Mail about missing work: {missed}')
    # a short hop past 09:00 isn't a miss, so it excuses nothing (DR1)
    pg.ev("devmodeRun('Clock: to 09:30', () => devmodeSkipTo(devmodeNext(9 * 60 + 30)))"); pg.ev("devmodeRun('Clock: +10 min', () => devmodeSkipTo(shipNow() + 10))")
    check(9 not in pg.ev('devmodeState().ex') and pg.ev('playerShiftOn(9)'), f'clock: a hop to 09:40 excused the day: {pg.ev("devmodeState().ex")}')
    # clocked in, you stay clocked in
    pg.ev("devmodeRun('Clock: to 08:55', () => devmodeSkipTo(devmodeNext(8 * 60 + 55)))"); pg.ev('careerClock()')
    pg.ev("devmodeRun('Clock: to 16:55', () => devmodeSkipTo(devmodeNext(16 * 60 + 55)))"); pg.step(60)
    C = pg.ev('({ in10: careerClockedIn(10), out10: careerClockedOut(10), ex: devmodeState().ex, ms: SHIP.career.ms, day: clockText() })')
    check(C['day'].startswith('Day 10') and C['in10'] and not C['out10'] and 10 not in C['ex'] and 9 in C['ex'] and C['ms'] == 0, f'clock: clocked in, the jump didn\'t keep you clocked in (or Day 9, passed at 12:30, wasn\'t excused): {C}')
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

TAKE = r'''(({ n, k }) => {
  const t0 = shipNow(), ok = devmodeRun('Take me to', () => { const c = devmodeMove(n, () => ixGoalWorld({ room: k }), r => r === k); return c ? null : 'none'; }, devmodeStory);
  const here = player.here();
  return { ok, msg: DM_UI.msg, deck: deckDef.num, room: roomAt(...here), clock: shipNow() === t0,
    walk: !!findPath(here, (() => { const c = nearestOpen(LIFT_AT[0], LIFT_AT[1], player); return c; })(), null, player) };
})'''

def part_move(b):
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
    pg = Page(ctx, '#dev'); pg.sign()
    # the escort: the manifest signed, Zeke walking you through the arrival
    check(pg.ev('!!SHIP.intro.step') and pg.ev("devmodeRun('Take me to', () => null, devmodeStory)") is False and 'arrival' in pg.ev('DM_UI.msg'), f'move: not refused during the escort: {pg.ev("DM_UI.msg")}')
    pg.ev('newGameStart(false); introSkip()'); pg.step(10)
    # inside a meeting
    pg.ev("dialogueShow(Object.keys(MEETING_SCRIPTS).find(k => !/^moment:/.test(k)))")
    check(pg.ev("devmodeRun('Take me to', () => null, devmodeStory)") is False and 'meeting' in pg.ev('DM_UI.msg'), f'move: not refused inside a meeting: {pg.ev("DM_UI.msg")}')
    pg.ev('dialogueEnd(true)')
    # every room on every deck
    rooms = pg.ev("DECK_ORDER.map(n => [n, Object.keys(DECKS[n].rooms || {}).filter(k => !devmodeSpine(n, k) && DECKS[n].rooms[k].name)])")
    n_all = 0; shut = []; bad = []
    for n, keys in rooms:
        for k in keys:
            r = pg.page.evaluate('a => window.__sc(' + json.dumps(TAKE) + ')(a)', {'n': n, 'k': k}); n_all += 1
            if not (r['ok'] and r['deck'] == n and r['clock']): bad.append((n, k, r['msg'])); continue
            if r['room'] != k: bad.append((n, k, 'landed in ' + str(r['room'])))
            elif not r['walk']: shut.append(f'{n}:{k}')
    check(not bad, f'move: Take me to a room failed: {bad[:6]}')
    check(sorted(shut) == sorted(pg.ev('DM_SHUT')), f'move: DM_SHUT ({pg.ev("DM_SHUT")}) isn\'t the rooms with no walking way to the lift: {shut}')
    pg.step(5); check(not pg.errors, f'move: errors after the rooms {pg.errors[:3]}')
    # the testing spots and the next appointment, through the panel's own functions
    def spot(src, deck):
        pg.ev(src); pg.page.wait_for_timeout(700); pg.step(3)
        check(pg.ev('deckDef.num') == deck and "You're at" in pg.ev('DM_UI.msg'), f'move: {src}: {pg.ev("DM_UI.msg")}, on deck {pg.ev("deckDef.num")}')
        return pg.ev('DM_UI.msg')
    pg.ev('goToDeck(4)')
    lad = spot('devmodeLadder()', 4)
    spot("devmodeGoal('the time clock', DM_SPOTS[0][1]())", 5)
    spot("devmodeGoal('the job board', DM_SPOTS[1][1]())", 5)
    pg.ev("devmodeRun('Clock: to 08:30', () => devmodeSkipTo(devmodeNext(8 * 60 + 30)))")
    appt = spot('devmodeAppt()', 5)
    # Mark here, Back to mark
    pg.ev('devmodeMark()'); mark = pg.ev('devmodeRead(DM_KEY.mark)')
    check(mark and mark['label'].startswith(pg.ev('clockText()')), f'move: Mark here: {pg.ev("DM_UI.msg")}')
    pg.ev("devmodeRun('Clock: +1 day', () => devmodeSkipTo(shipNow() + 1440))")
    got = pg.ev_reload('devmodeBack()')
    check(got == mark['save'], 'move: Back to mark did not reload the marked save byte for byte')
    check(pg.ev('devmodeRead(DM_KEY.undo).label') == 'Back to mark' and pg.ev('!!devmodeRead(DM_KEY.mark)'), 'move: Back to mark kept no Undo, or lost the mark')
    got2 = pg.ev_reload('devmodeBack()')
    check(got2 == mark['save'], 'move: a second Back to mark differs')
    check(not pg.errors, f'move: errors {pg.errors[:3]}')
    pg.close(); ctx.close()
    print(f'  move: {n_all} rooms on {len(rooms)} decks, clock unmoved' + (f' (no walking way from the lift: {", ".join(shut)})' if shut else '') + f'; refused in the escort and a meeting; {lad} | {appt}; Mark and Back to mark byte for byte, twice')

def part_slow(b):
    import threading, http.server, functools, time
    d = WORK / 'test'; name = '_devmode_slow.html'; (d / name).write_text(TMP.read_text())
    loads = {'slow': False}
    class Quiet(http.server.SimpleHTTPRequestHandler):  # the server holds the page back (its own thread, so the old page runs on)
        def log_message(self, *a): pass
        def do_GET(self):
            if loads['slow'] and name in self.path: time.sleep(6)
            return super().do_GET()
    srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(d)))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
    pg = ctx.new_page(); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
    pg.add_init_script(INIT)
    pg.goto(f'http://127.0.0.1:{srv.server_address[1]}/{name}#dev'); pg.wait_for_function('window.__sc !== undefined', timeout=90000)
    ev = lambda src: pg.evaluate('s => window.__sc(s)', src)
    ev('(() => { renderer.render = () => {}; })()'); pg.evaluate('window.__step(10, 33)')
    ev('(INTRO_BOOT = false, newGameStart(false), introSkip(), saveGame(), 0)')
    def held(src, want_save):
        loads['slow'] = True                               # the old page notes, at 4.6 s, its Dev save and message (sessionStorage outlives the reload)
        pg.evaluate('s => { setTimeout(() => sessionStorage.setItem("probe", JSON.stringify([localStorage.getItem("starship-cadet-save-dev"), window.__sc("DM_UI.msg")])), 4600); window.__sc(s); }', src)
        pg.wait_for_function('window.__sc !== undefined && performance.getEntriesByType("navigation")[0].type === "reload"', timeout=90000, polling=250)
        loads['slow'] = False
        first = pg.evaluate('() => localStorage.getItem("starship-cadet-save-dev")')
        mid, msg = json.loads(pg.evaluate('() => sessionStorage.getItem("probe") || "[null, \\"(no note: reloaded before 4.6 s)\\"]"'))
        pg.evaluate('() => sessionStorage.removeItem("probe")')
        ev('(() => { renderer.render = () => {}; })()'); pg.evaluate('window.__step(10, 33)')
        return mid, msg, first
    before = ev('clockText()'); s0 = pg.evaluate('() => localStorage.getItem("starship-cadet-save-dev")')
    ev("devmodeRun('Clock: +3 hours', () => devmodeSkipTo(shipNow() + 180))")
    mid, msg, _ = held('devmodeUndo()', s0)
    check(mid == s0 and 'still reloading' in msg, f'slow: during a slow reload the kept save didn\'t stay put ({msg})')
    check(ev('clockText()') == before and not ev('devmodeRead(DM_KEY.undo)'), f'slow: after a slow reload the Undo didn\'t happen ({ev("clockText()")}, not {before}) or its record is still there')
    ev('devmodeMark()'); mark = ev('devmodeRead(DM_KEY.mark)'); ev("devmodeRun('Clock: +1 day', () => devmodeSkipTo(shipNow() + 1440))")
    mid, msg, first = held('devmodeBack()', mark['save'])
    check(mid == mark['save'] and first == mark['save'], f'slow: Back to mark: the marked save didn\'t stay put through a slow reload ({msg})')
    check(not errs, f'slow: errors {errs[:3]}')
    ctx.close(); srv.shutdown()
    print(f'  slow: Undo and Back to mark with the reload held back 6 s: the kept save stayed put; the Undo happened and was used up')


TRAD = r"""(({ id, how, who, mail }) => {
  DM_UI.who = who || null; DM_UI.tmail = !!mail;
  const ev = SHIP_TRADITIONS.find(e => e.id === id), a = devmodeTradAt(ev, how);
  if (typeof a === 'string') return { refused: a };
  const ok = devmodeRun('Tradition', () => { const st = devmodeState(); st.tr = st.tr.filter(r => !(r.id === id && r.day === a.d)).concat([{ id, day: a.d, from: a.from, ...(who ? { who } : {}) }]);
    devmodeTradsAgain(a.d); if (mail) devmodeTradMail(ev, a.d); return null; });
  const e = eventsOn(a.d).find(x => x.id === id && x.dev);
  return { ok, d: a.d, from: a.from, on: !!e, to: e && e.to, len: ev.at[1] - ev.at[0], going: devmodeGoing(id, a.d), crew: DECK_CREW.length };
})"""

def part_trad(b):
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
    pg = Page(ctx, '#dev')
    start = lambda id, how, who=None, mail=False: pg.page.evaluate('([s, a]) => window.__sc(s)(a)', [TRAD, {'id': id, 'how': how, 'who': who, 'mail': mail}])
    r = start('quiz', 'soon')
    check('Day 0' in (r.get('refused') or ''), f'trad: not refused on Day 0: {r}')
    pg.ev('newGameStart(false); introSkip(); careerInit(); SHIP.career.gs = DM_SEED; devmodeState().ex = []; devmodeState().note = ""; devmodeState().tr = []'); pg.step(10)
    n = pg.ev('SHIP_TRADITIONS.length')
    check(n >= 40, f'trad: only {n} traditions to start')
    pg.ev("devmodeRun('Clock', () => devmodeSkipTo(2 * 1440 + 17 * 60))")    # Day 3, Wednesday 17:00
    base = pg.ev("JSON.stringify(eventsOn(3).map(e => [e.id, e.from, e.to]))")
    out = []
    # five kinds: weekly (quiz, a Thursday's, on a Wednesday), every 14 days (harvest), yearly (founding), a birthday (whose), the gym club with its spare machines
    cases = [('quiz', 'soon', None), ('harvest', 'tomorrow', None), ('founding', 'usual', None), ('running', 'tomorrow', None)]
    for id, how, who in cases:
        r = start(id, how, who); out.append((id, r))
        check(r.get('ok') and r.get('on') and r['to'] - r['from'] == r['len'], f'trad: {id} {how} not started: {r}')
        check(r.get('going', 0) >= (1 if id == 'running' else 3), f'trad: {id} {how}: only {r.get("going")} going')   # gym club: the gym's regulars (two machines kept free)
    q = out[0][1]
    check(q['d'] == 3 and q['from'] == 17 * 60 + 20, f'trad: quiz in 20 minutes at {q}')
    check(q['crew'] > 0, 'trad: nobody on the deck after the plans were made again')
    who = pg.ev("schedPeople().filter(p => !p.player && aboard(p, 4)).slice(0, 2).map(p => p.id)")
    r = start('birthday', 'tomorrow', None); check('whose' in (r.get('refused') or ''), f'trad: a birthday without whose: {r}')
    r = start('birthday', 'tomorrow', who); out.append(('birthday', r))
    check(r.get('ok') and r.get('on') and r.get('going', 0) >= 3, f'trad: birthday not started: {r}')
    hon = pg.ev("eventsOn(4).find(e => e.id === 'birthday' && e.dev).honorees.map(p => p.id)")
    check(hon == who, f'trad: the birthday is not for whose was picked: {hon} vs {who}')
    # the same room at the same time: hull lights in the bow lounge during the quiz
    r = start('hull-lights', 'soon'); check('same room' in (r.get('refused') or ''), f'trad: a clash with another Dev start not refused: {r}')
    gave = pg.ev("eventsOn(4).some(e => e.id === 'quiz')")
    check(not gave, 'trad: Thursday\'s quiz didn\'t give way to the Dev-started birthday (the mess, then the bow lounge)')
    # its Mail now
    m0 = pg.ev('SHIP.mail.length'); r = start('jam', 'tomorrow', None, True)
    check(r.get('ok') and pg.ev('SHIP.mail.length') == m0 + 1 and 'Music jam' in pg.ev('SHIP.mail[0].subject'), f'trad: its Mail now: {pg.ev("SHIP.mail[0].subject")}')
    # the crew really go: the quiz minute by minute, crew in the bow lounge
    pg.ev("devmodeRun('Clock', () => devmodeSkipTo(2 * 1440 + 17 * 60 + 40))"); pg.step(30)
    there = pg.ev("schedPeople().filter(p => { const w = whereIs(p, shipNow()); return w && w.tag && evTagId(w.tag) === 'quiz'; }).length")
    check(there >= 3, f'trad: only {there} at the Dev quiz at 17:40')
    # too late tonight; a usual time gone
    pg.ev("devmodeRun('Clock', () => devmodeSkipTo(2 * 1440 + 23 * 60))")
    r = start('quiz', 'soon'); check('Too late' in (r.get('refused') or ''), f'trad: 23:20 not refused: {r}')
    r = start('market', 'usual'); check('has gone' in (r.get('refused') or ''), f'trad: a usual time gone not refused: {r}')
    # the saved starts ride in the Dev save; Undo takes the last one away
    pg.ev('saveGame()'); saved = json.loads(pg.ev('localStorage.getItem(SAVE_KEY)'))['dev']['tr']
    check([x['id'] for x in saved] == ['quiz', 'harvest', 'founding', 'running', 'birthday', 'jam'], f'trad: the Dev save holds {saved}')
    pg.ev("devmodeRun('Tradition: stop', () => { devmodeTradsAgain(4); return null; })")
    pg.ev_reload('devmodeUndo()')
    check(len(pg.ev('devmodeState().tr')) == 6, 'trad: Undo lost the starts')
    # Stop it: back to the calendar (Day 3's own list again)
    pg.ev("devmodeState().tr.filter(r => r.day === 3).forEach(r => devmodeRun('stop', () => { devmodeState().tr = devmodeState().tr.filter(x => x !== r); devmodeTradsAgain(3); return null; }))")
    check(pg.ev("JSON.stringify(eventsOn(3).map(e => [e.id, e.from, e.to]))") == base, 'trad: Day 3 not back to its calendar after Stop it')
    # the tab draws: the list, a search, a tradition's card at phone size
    pg.ev('devmodeOpen(true); DM_UI.tab = "trad"; DM_UI.trad = null; devmodeDraw()')
    rows = pg.ev("document.querySelectorAll('#dmSheet .dmBody .dmRow button').length")
    pg.page.fill('#dmSheet input.dmFind', 'quiz'); pg.step(2)
    hits = pg.ev("[...document.querySelectorAll('#dmSheet .dmBody .dmRow button')].map(b => b.textContent)")
    check(rows >= n and any('Quiz' in h for h in hits) and len(hits) < rows, f'trad: the list ({rows}) or search ({hits})')
    small = pg.ev("[...document.querySelectorAll('#dmSheet button')].filter(b => b.offsetParent && b.getBoundingClientRect().height < 44).map(b => b.textContent)")
    check(not small, f'trad: buttons under 44px: {small}')
    check(not pg.errors, f'trad: errors {pg.errors[:3]}')
    pg.close(); ctx.close()
    print('  trad: Day 0 refused; ' + ', '.join(f'{i} {r.get("going")}' for i, r in out) + ' going; whose asked; room clash, too late, usual gone refused; Mail; crew at the quiz; saved; Undo; Stop it back to the calendar; list and search')


def part_set(b):
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
    pg = Page(ctx, '#dev'); pg.sign(); pg.step(20)
    # the table's days are the ladder's (a moved training fails here, not silently)
    bad = pg.ev("""(() => { const out = [], seen = new Set();
      for (const r of DM_CAREER) for (const id of r.defer || []) seen.add(id);   // (S5-2, RV20 S4) a row the Step 5 ladder puts off past its day (m17: Day 31)
      for (const r of DM_CAREER) for (const id of r.train || []) { seen.add(id); const row = ladderRow(id); if (!row || row.day !== r.day) out.push(id + ': table ' + r.day + ', ladder ' + (row ? row.day : 'none')); }
      for (const row of CAREER_LADDER) if (row.day <= devmodeTableEnd() && !seen.has(row.id)) out.push(row.id + ': on the ladder (Day ' + row.day + '), not in the table');   // (J0, F1) up to the table's last day: after it the career is the game's own
      return out; })()""")
    check(not bad, f'set: the table and CAREER_LADDER disagree: {bad}')
    setc = lambda n: pg.ev(f"devmodeRun('Set career to Day {n}', () => devmodeSetCareerTo({n}))")
    pg.ev("devmodeRun('Clock: +3 hours', () => devmodeSkipTo(shipNow() + 180))"); before = pg.ev('clockText()')
    got = {}
    for n in (2, 10, 12, 26):
        check(setc(n) is True, f'set: Day {n} refused: {pg.ev("DM_UI.msg")}')
        pg.step(20)
        S = pg.ev(f"""(() => {{ const W = SHIP.works, c = devmodeCareerFor({n}); return {{ clock: clockText(), rank: W && W.rank, tier: W && W.tier, xp: W && W.xp, tr: W && Object.keys(W.tr).sort().join(), want: Object.keys(c.tr).sort().join(),
          wrank: c.rank, cur: W && W.cur, room: ROOMS[roomAt(...player.here())].name, bed: roomAt(...player.here()) === roomAt(...(DECKS[deckOf(playerBed())].places.find(p => p.id === playerBed()) || {{ at: [0, 0] }}).at), deck: deckDef.num, bdeck: deckOf(playerBed()), pip: PLAYER_SPEC.rank || 0,
          ms: SHIP.career.ms, st: SHIP.career.st, missed: SHIP.mail.filter(m => /missed|summons|warning/i.test(m.subject || '') || Object.values(INTRO_MEETINGS).some(x => m.subject === x.title + ' (notes)')).map(m => m.subject), open: SHIP.occasions.filter(o => o.status === 'asked').map(o => o.id),
          met: INTRO_WEEK.filter(b => b.meeting && introAbs(b.day, b.at) < shipNow()).every(b => SHIP.intro.done[b.id + ':met'] >= 0), set: devmodeState().set, settle: !!SHIP.intro.settle.all }}; }})()""")
        got[n] = S
        check(S['clock'].startswith(f'Day {n},') and S['clock'].endswith('06:00'), f'set: Day {n} landed at {S["clock"]}')
        check(S['rank'] == S['wrank'] and S['tr'] == S['want'] and S['cur'] is None, f'set: Day {n}: the career isn\'t the table\'s: {S}')
        check(S['bed'] and S['deck'] == S['bdeck'] in (4, 2), f'set: Day {n}: not woken in your bed\'s room ({S["room"]})')
        check(S['ms'] == 0 and S['st'] == 0 and not S['missed'] and not S['open'], f'set: Day {n}: a miss, a first-week meeting\'s notes, a summons or something still asking: {S}')
        check(S['met'] and S['set']['day'] == n and (S['settle'] == (n > 7)), f'set: Day {n}: the first week or the Dev record: {S}')
    sick = pg.ev("Array.from({ length: DM_JUMPMAX }, (_, i) => i + 1).filter(d => sickDue(d))")   # (J0) to the latest jump's day: the Dev seed has none before Day 46
    check(not sick and not pg.ev('sickNow()'), f'set: the Dev seed brings sick days {sick}')
    check(got[10]['rank'] == 'officer' and got[10]['tier'] == 2 and got[10]['pip'] == 1 and got[2]['pip'] == 0, f'set: Day 10 isn\'t an officer with the pip: {got[10]}')
    check(got[10]['room'] != got[2]['room'], f'set: Day 10 not woken in cabin 4-23: {got[10]["room"]}')
    # play Day 11 hour by hour: the ladder never opens a trained row again
    setc(10); pg.step(10)
    again = pg.ev("""(() => { const tr = new Set(Object.keys(SHIP.works.tr)), out = [];
      for (let h = 10 * 24 + 6; h <= 10 * 24 + 16; h++) { devmodeSkipTo(h * 60); for (const id of ladderTick(h)) if (tr.has(id)) out.push(id); }
      if (SHIP.works.cur && tr.has(SHIP.works.cur.id)) out.push('cur ' + SHIP.works.cur.id); return out; })()""")
    check(not again, f'set: Day 11 opened trained rows again: {again}')
    # two Set careers to Day 12 give the same save, byte for byte (the Dev seed)
    saves = []
    for _ in range(2):
        setc(12); pg.ev('saveGame()'); saves.append(json.loads(pg.ev('localStorage.getItem(SAVE_KEY)')))
    diff = [k for k in set(saves[0]) | set(saves[1]) if saves[0].get(k) != saves[1].get(k)]
    deep = [k for k in set(saves[0].get('ship', {})) | set(saves[1].get('ship', {})) if saves[0]['ship'].get(k) != saves[1]['ship'].get(k)]
    check(not diff, f'set: two Set careers to Day 12 differ in {sorted(diff)} (ship: {sorted(deep)})')
    # starting friendships (Day 12): the people a steady player meets, through relAdd
    fr = pg.ev("(socInit(), { gone: DM_FRIENDS.filter(f => !SOC.idx.has(f[0])).map(f => f[0]), zeke: relTier('torres-zeke'), tomas: relTier('tomas'), calder: relTier('calder'), known: DM_FRIENDS.filter(f => relTier(f[0]) >= 1).length })")
    check(not fr['gone'] and fr['zeke'] >= 3 and fr['tomas'] >= 3 and fr['calder'] >= 2 and fr['known'] >= 10, f'set: Day 12 friendships: {fr}')
    # Undo brings the game before back
    pg.ev_reload('devmodeUndo()')
    check(pg.ev('devmodeState().set && devmodeState().set.day') == 12, f'set: Undo of the second Day 12 isn\'t the first: {pg.ev("devmodeState().set")}')
    # the beats: Day 9's test job (08:50, the bay, the test held for you) and Day 10's promotion (10:50, the summons at 11:00)
    beat = lambda id: pg.ev(f"devmodeRun('Set career: beat', () => devmodeSetCareerTo(DM_BEATS.find(b => b.id === '{id}').day, DM_BEATS.find(b => b.id === '{id}')))")
    beat('t2'); pg.step(20)
    T = pg.ev("({ clock: clockText(), room: ROOMS[roomAt(...player.here())].name, rank: SHIP.works.rank, test: SHIP.works.test, cur: SHIP.works.cur && SHIP.works.cur.id, tr: 't2' in SHIP.works.tr, m6: 'm6' in SHIP.works.tr })")
    check(T['clock'] == 'Day 9, Tuesday 08:50' and T['room'] == 'Works bay' and T['rank'] == 'junior' and T['test'] and not T['test']['passed'] and T['cur'] == 't2' and not T['tr'] and T['m6'], f'set: the Day 9 test beat: {T}')
    beat('promo'); pg.step(20)
    PB = pg.ev("typeof promoBeatsOn === 'function' && promoBeatsOn()")   # FX28 (PROMO_BEATS_ON): the result at 08:15, not 11:00
    pg.ev(f"devmodeRun('Clock', () => devmodeSkipTo(9 * 1440 + {8 * 60 + 7 if PB else 11 * 60 + 2}))")
    P = pg.ev("({ clock: clockText(), rank: SHIP.works.rank, passed: SHIP.works.test && SHIP.works.test.passed, summons: SHIP.occasions.some(o => o.id === 'promoSummons') })")
    check(P['rank'] == 'junior' and P['passed'] and P['summons'], f'set: the Day 10 promotion beat (at {"08:07" if PB else "11:02"} the summons is booked, still a junior): {P}')
    # the panel's way: a day at a time under the fade, the progress on the panel, then one save
    pg.ev('devmodeOpen(true); DM_UI.tab = "set"; DM_UI.day = 5; devmodeDraw()')
    pg.page.click('#dmSheet button:has-text("Set career to Day 5")'); pg.page.click('#dmSheet button:has-text("Tap again")')
    seen = set()
    for _ in range(100):
        pg.page.wait_for_timeout(80); seen.add(pg.ev('DM_UI.msg'))
        if not pg.ev('DM_HOLD') and 'Career set to Day 5' in pg.ev('DM_UI.msg'): break
    check(any(m.startswith('Setting career: Day') and m.endswith('of 5…') for m in seen) and pg.ev('clockText()') == 'Day 5, Friday 06:00' and not pg.ev('DM_HOLD'), f'set: the panel\'s Set career (progress {sorted(seen)[:4]}, {pg.ev("clockText()")})')
    check(pg.ev('devmodeState().last') == 'Set career to Day 5' and json.loads(pg.ev('localStorage.getItem(SAVE_KEY)'))['dev']['set']['day'] == 5, 'set: the panel\'s Set career wasn\'t saved')
    pg.ev_reload('devmodeUndo()')
    check(pg.ev("devmodeState().set && devmodeState().set.beat") == 'promo', f'set: Undo after the panel\'s Set career: {pg.ev("devmodeState().set")}')
    # the tab draws at phone size
    pg.ev('devmodeOpen(true); DM_UI.tab = "set"; devmodeDraw()')
    txt = pg.ev("document.querySelector('#dmSheet .dmBody').textContent")
    check('What\'s set: Day 10, Day 10: the promotion' in txt and 'approximate' in txt and 'Trained' in txt, f'set: the tab: {txt[:200]}')
    small = pg.ev("[...document.querySelectorAll('#dmSheet button')].filter(b => b.offsetParent && b.getBoundingClientRect().height < 44).map(b => b.textContent)")
    check(not small, f'set: buttons under 44px: {small}')
    check(not pg.errors, f'set: errors {pg.errors[:3]}')
    pg.close(); ctx.close()
    print(f'  set: table = ladder; Days 2, 10, 12, 26: ' + '; '.join(f'{n} {g["rank"]} T{g["tier"]} xp {g["xp"]}, {len(g["tr"].split(",")) if g["tr"] else 0} trained, {g["room"]}' for n, g in got.items()) + f'; no miss or notes Mail; Day 11 opens nothing trained; two Day 12s identical; friends (Zeke {fr["zeke"]}, {fr["known"]} known); test and promotion beats; the panel\'s progress; Undo; the tab')


def part_career(b):
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
    pg = Page(ctx, '#dev'); pg.sign(); pg.step(20)
    run = lambda src: pg.ev(f"devmodeRun('Career', () => {{ {src} }})")
    # by hand, from a fresh Day 1 evening (the record is made), each an undoable Dev action
    pg.ev("devmodeRun('Set', () => devmodeSetCareerTo(1)); devmodeRun('Clock', () => devmodeSkipTo(17 * 60 + 30))")
    W0 = pg.ev('JSON.stringify(SHIP.works)')
    pg.ev("devmodeRun('xp', () => { const W = devmodeW(); W.xp += DM_XP; return null; })")
    check(pg.ev('SHIP.works.xp') == 5, 'career: xp + 5')
    pg.ev("devmodeRun('band', () => { const W = devmodeW(); W.xp = devmodeBandNext(W)[0]; return null; })")
    check(pg.ev('worksBand()') == 'steady' and pg.ev('SHIP.works.xp') == 8, f'career: to the next band: {pg.ev("worksBand()")}')
    pg.ev("(() => { const W = SHIP.works, row = CAREER_LADDER.find(r => W.tr[r.id] === undefined && r.tier <= W.tier && r.id !== 't2'); devmodeRun('train', () => { if (!worksOpened(W).has(row.id)) (W.op[SHIP.time.day] = W.op[SHIP.time.day] || []).push(row.id); W.use[row.id] = 1; worksTrained(row.id); return null; }); })()")
    check(pg.ev("SHIP.works.tr.m1 === 1 && !!SHIP.works.tools.clipboard && worksIsOpen('m1')"), 'career: the next training (Rounds, with the clipboard)')
    pg.ev("devmodeRun('tool', () => (toolGive('tester'), null))"); check(pg.ev('!!SHIP.works.tools.tester'), 'career: give a tool')
    pg.ev_reload('devmodeUndo()')
    check(pg.ev('!SHIP.works.tools.tester && SHIP.works.tr.m1 === 1'), 'career: Undo of the tool')
    # the rank by hand: Officer (the pip, cabin 4-23's bed), then Junior again
    pg.ev("DM_HOLD = false; devmodeRank('officer')"); pg.page.wait_for_timeout(700); pg.step(5)
    R = pg.ev("({ rank: SHIP.works.rank, tier: SHIP.works.tier, pip: PLAYER_SPEC.rank || 0, bed: playerBed(), done: SHIP.works.done })")
    check(R['rank'] == 'officer' and R['tier'] == 2 and R['pip'] == 1 and R['bed'] == '4-23' and 'ceremony2' in R['done'], f'career: rank Officer by hand: {R}')
    pg.ev("devmodeRank('junior')"); pg.page.wait_for_timeout(700); pg.step(5)
    R = pg.ev("({ rank: SHIP.works.rank, tier: SHIP.works.tier, pip: PLAYER_SPEC.rank || 0, bed: playerBed() })")
    check(R['rank'] == 'junior' and R['tier'] == 1 and R['pip'] == 0 and R['bed'] != '4-23', f'career: rank Junior by hand: {R}')
    # the promotion opened from Day 8 (only the day missing) runs to the ceremony
    pg.ev("devmodeRun('Set', () => devmodeSetCareerTo(8))"); pg.step(10)
    pg.ev("devmodeRun('Clock', () => devmodeSkipTo(7 * 1440 + 9 * 60 + 30))")
    N = pg.ev("devmodeTestNeeds(SHIP.works).map(x => x[1])")
    check(N == [False, True, True, True, True], f'career: Day 8 09:30 test needs (only the day missing): {N}')
    pg.ev("DM_HOLD = false; devmodeTestOpen()"); pg.page.wait_for_timeout(700); pg.step(5)
    T = pg.ev("({ msg: DM_UI.msg, cur: SHIP.works.cur && SHIP.works.cur.id, j: SHIP.works.cur && SHIP.works.cur.j, test: SHIP.works.test })")
    check(T['cur'] == 't2' and T['j'] and T['test']['day'] == 8, f'career: Open the test now: {T}')
    pg.ev("devmodeRun('Turn in', () => { worksDone('t2', shipNow()); return null; })")
    check(pg.ev('SHIP.works.test.passed'), 'career: the test passed when turned in')
    seen = []
    for _ in range(7):
        pg.ev("DM_HOLD = false; devmodePromoNext()"); pg.page.wait_for_timeout(700); pg.step(10)
        seen.append(pg.ev('clockText()'))
        if pg.ev("promoDone('ceremony2')"): break
        pg.ev("devmodeRun('Clock', () => devmodeSkipTo(shipNow() + 40))"); pg.step(5)
    PB = pg.ev("typeof promoBeatsOn === 'function' && promoBeatsOn()")   # FX28: the walk after your dinner, or at 20:00; 4-23 yours by 22:00 whatever happens
    pg.ev(f"devmodeRun('Clock', () => devmodeSkipTo(devmodeNext({22 * 60 + 5 if PB else 20 * 60})))")
    E = pg.ev("({ rank: SHIP.works.rank, done: SHIP.works.done, home: SHIP.works.home, pip: PLAYER_SPEC.rank || 0 })")
    check(E['rank'] == 'officer' and all(k in E['done'] for k in ('summons2', 'move2', 'ceremony2')) and E['home'] == '4-23' and E['pip'] == 1, f'career: the promotion didn\'t run to the ceremony: {E} (steps at {seen})')
    # the tab draws at phone size
    pg.ev('devmodeOpen(true); DM_UI.tab = "career"; DM_UI.msg = ""; devmodeDraw()')
    txt = pg.ev("document.querySelector('#dmSheet .dmBody').textContent")
    check('Works Officer, Tier 2' in txt and 'Trainings' in txt and '(m6)' in txt and 'Tools' in txt, f'career: the tab: {txt[:160]}')
    small = pg.ev("[...document.querySelectorAll('#dmSheet button')].filter(b => b.offsetParent && b.getBoundingClientRect().height < 44).map(b => b.textContent)")
    check(not small, f'career: buttons under 44px: {small}')
    check(not pg.errors, f'career: errors {pg.errors[:3]}')
    pg.close(); ctx.close()
    print(f'  career: xp, next band, next training (Rounds + clipboard), a tool, Undo; rank Officer and Junior by hand; Day 8 test opened (only the day missing), passed, Next step through {seen} to the ceremony; the tab')

# ---- S6-3 (W7): the Engine Specialist's presets (Days 22, 22, 23, 25), on a build with P5_PROMO4 on (else skipped)
def part_t4beats(b):
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
    pg = Page(ctx, '#dev'); pg.sign(); pg.step(20)
    if not pg.ev("typeof P5_PROMO4 !== 'undefined' && P5_PROMO4"): print('  t4beats: P5_PROMO4 off: skipped'); pg.close(); ctx.close(); return
    beat = lambda id: pg.ev(f"devmodeRun('Set career: beat', () => devmodeSetCareerTo(DM_BEATS.find(b => b.id === '{id}').day, DM_BEATS.find(b => b.id === '{id}')))")
    look = "({ clock: clockText(), deck: deckDef.num, room: ROOMS[roomAt(...player.here())].name, rank: SHIP.works.rank, t4: puT4(), home: SHIP.works.home, badge: SHIP.occasions.filter(o => o.id === 'pu4Badge' && o.status === 'asked').length })"
    got = {}
    for id in ('t4', 't4res', 't4badge', 't4move'):
        beat(id); pg.step(20); got[id] = pg.ev(look)
    for k, v in got.items(): print('   ', k, v)
    t = got['t4']; check(t['clock'] == 'Day 22, Monday 09:20' and t['room'] == 'Works bay' and t['rank'] == 'senior' and t['t4'] and t['t4']['day'] == 22 and not t['t4']['passed'], f't4beats: Day 22 the test: {t}')
    t = got['t4res']; check(t['clock'].startswith('Day 22,') and t['clock'].endswith('22:30') and t['deck'] == 1 and t['rank'] == 'senior' and t['t4']['passed'] and not t['t4']['res'], f't4beats: Day 22 the result: {t}')
    t = got['t4badge']; check(t['clock'].endswith('16:00') and t['deck'] == 1 and t['rank'] == 'specialist' and t['t4']['res'] == 22 and not t['t4']['badge'] and t['badge'] == 1, f't4beats: Day 23 the badge booked: {t}')
    t = got['t4move']; check(t['clock'].endswith('18:30') and t['deck'] == 3 and t['t4']['move'] and t['t4']['move']['ready'] == 25 and not t['t4']['move']['walked'] and t['home'] == '4-23', f't4beats: Day 25 the move: {t}')
    if pg.ev("typeof P5_END !== 'undefined' && P5_END"):   # (S6-9, W8) Calder's question: Day 26 18:35 by the tea corner, the question settled
        beat('cq'); pg.step(20); q = pg.ev("({ clock: clockText(), room: ROOMS[roomAt(...player.here())].name, rank: SHIP.works.rank, end: SHIP.works.end })"); print('    cq', q)
        check(q['clock'] == 'Day 26, Friday 18:35' and q['room'] == 'Tea corner' and q['rank'] == 'specialist' and q['end'] and q['end']['day'] == 26 and not q['end']['answer'], f't4beats: Day 26 Calder\'s question: {q}')
    check(not pg.errors, f't4beats: errors {pg.errors[:3]}')
    pg.close(); ctx.close()

# ---- J0 (plan v4.4, DM1): Jump to's groundwork: the jump list, the runner's stops (your answers on the way, CA1's F2),
# the table keeping what the game wrote (F1, backlog DM1-1), plain Set career past Day 32 saying Stay (F3), the week-slow
# offset, rank by hand (Senior, Specialist), the Stop, the tabs at phone size, and how long a Day 36 run takes
def part_jumps(b):
    import time
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
    pg = Page(ctx, '#dev'); pg.sign(); pg.step(20)
    bad = pg.ev("""(() => { const out = [], seen = new Set(), G = DM_JUMP_GROUPS.map(g => g[0]);
      for (const j of DM_JUMPS) {
        if (seen.has(j.id)) out.push('twice: ' + j.id); seen.add(j.id);
        if (!G.includes(j.group)) out.push(j.id + ': group ' + j.group);
        if (!(Number.isInteger(j.day) && j.day >= 1 && j.day <= DM_JUMPMAX) || !(j.at >= 0 && j.at < 1440)) out.push(j.id + ': day ' + j.day + ', at ' + j.at);
        if (j.by != null && !(j.by >= 1 && j.by <= j.day)) out.push(j.id + ': by ' + j.by);
        if (j.where && !(DECKS[j.where.deck] && DECKS[j.where.deck].rooms && DECKS[j.where.deck].rooms[j.where.room])) out.push(j.id + ': no room ' + JSON.stringify(j.where));
        if (typeof j.label !== 'string' || !j.label) out.push(j.id + ': no label');
      }
      return out; })()""")
    check(not bad, f'jumps: the jump list: {bad}')
    n = pg.ev("DM_JUMPS.length"); onN = pg.ev("DM_JUMPS.filter(devmodeJumpOn).length")
    # the week-slow offset (pure): every row a week later
    S = pg.ev("({ a: devmodeCareerFor(16).rank, b: devmodeCareerFor(17, 7).rank, c: devmodeCareerFor(23, 7).rank, d: devmodeCareerFor(30, 7).rank, t: devmodeCareerFor(30, 7).tr.m1, t0: devmodeCareerFor(30).tr.m1, ms: devmodeCareerFor(30, 7).ms })")
    check(S['a'] == 'senior' and S['b'] == 'officer' and S['c'] == 'senior' and S['d'] == 'specialist' and S['t'] == S['t0'] + 7, f'jumps: the week-slow offset: {S}')
    # plain Set career to Day 36: timed; the answers put in on the way (Calder's question, then the offer, Stay); the
    # milestones the game wrote on Day 26 still there (F1); the endgame (F3); twice the same save
    # (each in a fresh browser, as two testers would: within one page, leftovers from the game before make the first run
    # differ from later ones, on the starting build too: backlog DM1-2 and DM1-3)
    times, saves = [], []
    for k in range(2):
        if k: pg.close(); ctx.close(); ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1); pg = Page(ctx, '#dev'); pg.sign(); pg.step(20)
        t0 = time.time(); r = pg.ev("devmodeRun('Set career to Day 36', () => devmodeSetCareerTo(36))"); times.append(time.time() - t0)
        check(r is True, f'jumps: Set career to Day 36 refused: {pg.ev("DM_UI.msg")}')
        pg.ev('saveGame()'); saves.append(pg.ev('localStorage.getItem(SAVE_KEY)'))
    pg.step(20)
    E = pg.ev("""({ clock: clockText(), rank: SHIP.works.rank, ms: SHIP.works.ms.map(x => x[0]), q: SHIP.works.end && SHIP.works.end.answer, offer: SHIP.end && SHIP.end.offer, settled: SHIP.end && SHIP.end.settled,
      stay: typeof endgameDay === 'function' ? endgameDay() : null, set: devmodeState().set, msg: DM_UI.msg, room: ROOMS[roomAt(...player.here())].name })""")
    print('    Day 36:', {k: E[k] for k in ('clock', 'rank', 'ms', 'q', 'settled', 'stay', 'set', 'room')})
    check(E['clock'].startswith('Day 36,') and E['clock'].endswith('06:00') and E['rank'] == 'specialist', f'jumps: Day 36 landed: {E["clock"]} {E["rank"]}')
    check(all(k in E['ms'] for k in ('nights', 'question', 'officer', 'senior', 'specialist')), f'jumps: Day 36 lost milestones (F1): {E["ms"]}')
    check(E['q'] == 'engines' and E['offer'] and E['offer'].get('met') and E['settled'] and E['settled']['choice'] == 'stay' and E['stay'], f'jumps: Day 36 answers on the way (F2, F3): question {E["q"]}, offer {E["offer"]}, settled {E["settled"]}, endgame {E["stay"]}')
    check(E['set'] and E['set'].get('ans') == {'cq': 'engines', 'offer': 'stay'} and 'Your answers on the way' in E['msg'], f'jumps: the answers used not recorded or said: {E["set"]} / {E["msg"][-160:]}')
    if saves[0] != saves[1]:
        a, c = json.loads(saves[0]), json.loads(saves[1]); fail(f'jumps: two Set careers to Day 36 (fresh browsers) give different saves: {sorted(k for k in set(a.get("ship", {})) | set(c.get("ship", {})) if a["ship"].get(k) != c["ship"].get(k))} {sorted(k for k in set(a) | set(c) if a.get(k) != c.get(k))}')
    # a jump with its own answer (Go): the address settles Go on Day 35
    pg.ev("devmodeRun('Jump: test go', () => devmodeSetCareerTo(35, { id: 'test-go', label: 'test', day: 35, by: 34, at: 16 * 60, where: null, ans: { offer: 'go' } }))")
    G = pg.ev("({ clock: clockText(), settled: SHIP.end && SHIP.end.settled, set: devmodeState().set })")
    check(G['clock'].endswith('16:00') and G['settled'] and G['settled']['choice'] == 'go' and G['settled']['day'] == 35, f'jumps: a Go jump: {G}')
    # rank by hand: Senior Officer, then Engine Specialist (approximate), from a Day 12 officer
    pg.ev("devmodeRun('Set career to Day 12', () => devmodeSetCareerTo(12))")
    pg.ev("DM_HOLD = false; devmodeRank('senior')"); pg.page.wait_for_timeout(700); pg.step(5)
    R1 = pg.ev("({ rank: SHIP.works.rank, tier: SHIP.works.tier, t3: SHIP.works.pu && SHIP.works.pu.t3 && SHIP.works.pu.t3.passed, ms: SHIP.works.ms.map(x => x[0]), tr: Object.keys(SHIP.works.tr).length })")
    pg.ev("devmodeRank('specialist')"); pg.page.wait_for_timeout(700); pg.step(5)
    R2 = pg.ev("({ rank: SHIP.works.rank, tier: SHIP.works.tier, t4: SHIP.works.pu && SHIP.works.pu.t4 && SHIP.works.pu.t4.passed, ms: SHIP.works.ms.map(x => x[0]), tr: Object.keys(SHIP.works.tr).length })")
    check(R1['rank'] == 'senior' and R1['tier'] == 3 and R1['t3'] and 'senior' in R1['ms'], f'jumps: Senior Officer by hand: {R1}')
    check(R2['rank'] == 'specialist' and R2['tier'] == 4 and R2['t4'] and R2['tr'] == R1['tr'], f'jumps: Engine Specialist by hand (trainings kept): {R2}')
    # the panel's Stop: a Set career to Day 20 stopped after a few days: saved where it got to, the hold let go
    pg.ev('devmodeOpen(true); DM_UI.tab = "set"; DM_UI.day = 20; DM_UI.msg = ""; devmodeDraw()')
    pg.page.click('#dmSheet button:has-text("Set career to Day 20")'); pg.page.click('#dmSheet button:has-text("Tap again")')
    for _ in range(100):
        pg.page.wait_for_timeout(50)
        if pg.ev("/Setting career: Day [3-9] /.test(DM_UI.msg)"): break
    stopped = pg.page.locator('#dmSheet button:has-text("Stop")').count()
    if stopped: pg.page.click('#dmSheet button:has-text("Stop")', timeout=5000)
    for _ in range(100):
        pg.page.wait_for_timeout(50)
        if not pg.ev('DM_HOLD'): break
    T = pg.ev("({ msg: DM_UI.msg, day: SHIP.time.day, hold: DM_HOLD, run: DM_UI.run, saved: JSON.parse(localStorage.getItem(SAVE_KEY)).dev.set })")
    check(stopped and T['msg'].startswith('Stopped:') and 1 < T['day'] < 20 and not T['hold'] and T['run'] is None and T['saved'] and T['saved']['day'] == T['day'], f'jumps: Stop: {T}')
    # the tabs at phone size: Jump to (its groups, the career beats with Go), Set career (By rank)
    pg.ev('DM_UI.tab = "jump"; DM_UI.jg = "career"; DM_UI.msg = ""; devmodeDraw()')
    J = pg.ev("""({ tabs: [...document.querySelectorAll('#dmSheet .dmTabs button')].map(b => b.textContent), groups: [...document.querySelectorAll('#dmSheet .dmGroups button')].map(b => b.textContent),
      rows: [...document.querySelectorAll('#dmSheet .dmJump')].map(r => r.firstChild.textContent), wide: document.querySelector('#dmSheet .dmBody').scrollWidth > document.querySelector('#dmSheet .dmBody').clientWidth,
      small: [...document.querySelectorAll('#dmSheet button')].filter(b => b.offsetParent && b.getBoundingClientRect().height < 44).map(b => b.textContent) })""")
    check(J['tabs'] == ['Quick', 'Clock', 'Traditions', 'Career', 'Set career', 'Jump to', 'Speed'] and J['groups'] == ['Career', 'Nights', 'Ship events', 'The ending'], f'jumps: the tabs and groups: {J["tabs"]} {J["groups"]}')
    check(len(J['rows']) >= 2 and not J['wide'] and not J['small'], f'jumps: the Jump to tab at 390 px: {J}')
    pg.shot(str(SHOTS / 'jump-career-390.png')) if SHOTS else None
    pg.ev('DM_UI.tab = "set"; DM_UI.day = null; devmodeDraw()')
    txt = pg.ev("document.querySelector('#dmSheet .dmBody').textContent")
    check('By rank (its first morning)' in txt and 'Engine Specialist' in txt, f'jumps: Set career\'s By rank: {txt[:200]}')
    check(not pg.errors, f'jumps: errors {pg.errors[:3]}')
    pg.close(); ctx.close()
    print(f'  jumps: {n} jumps ({onN} on), the list sound; week-slow offset; Day 36 in {times[0]:.1f} s and {times[1]:.1f} s, the same save twice, Engines and Stay put in on the way, settled Stay, the endgame, milestones kept; a Go jump settles Go on Day 35; Senior and Specialist by hand; Stop; the tabs at 390 px')

# ---- stubs (plan v4.4, J0): each later turn fills its own part here, so nobody edits the part list again
def part_beats(b):
    # J1 (plan v4.4): every Career and Nights jump J1 added lands at its time and room, and the game then books or starts
    # its beat: Power safety asked once you're up (played), the Tier 3 test held for you, its result, the bar and the
    # toast booked, each lesson's meeting and the briefing booked in their room, and each night's work once you clock in
    # at the time clock (played). One jump twice in fresh browsers gives the same save; Undo after a jump
    J1 = ['ps', 't3', 't3res', 't3bar', 't3toast', 'm19', 'm18', 'm20', 'm21', 'n1', 'n2', 'n3']
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
    pg = Page(ctx, '#dev'); pg.sign(); pg.step(20)
    on = pg.ev(f"{json.dumps(J1)}.filter(id => {{ const j = devmodeJumpOf(id); return j && devmodeJumpOn(j); }})")
    if not on: print('  beats: none on in this build'); pg.close(); ctx.close(); return
    play = lambda mins: pg.step(int(mins * 50) + 10)   # 0.6 ship minutes a real second: 50 frames a ship minute
    occ = lambda id: pg.ev(f"(SHIP.occasions || []).filter(o => o.id === '{id}' && o.status === 'asked').map(o => [hhmm(o.at % 1440), o.deck, o.room])")
    got = {}
    for id in on:
        r = pg.ev(f"devmodeRun('Jump', () => devmodeSetCareerTo(devmodeJumpOf('{id}').day, devmodeJumpOf('{id}')))")
        pg.step(10)
        L = pg.ev(f"""(() => {{ const j = devmodeJumpOf('{id}'), w = j.where, here = roomAt(...player.here());
          return {{ ok: {str(True).lower()}, clock: clockText(), want: 'Day ' + j.day + ',', at: hhmm(j.at), deck: deckDef.num, room: (ROOMS[here] || {{}}).name || '', wdeck: w ? w.deck : null, wroom: w ? DECKS[w.deck].rooms[w.room].name : null,
            rank: SHIP.works.rank, set: devmodeState().set }}; }})()""")
        check(r is True and L['clock'].startswith(L['want']) and L['clock'].endswith(L['at']) and (L['wdeck'] is None or (L['deck'] == L['wdeck'] and L['room'] == L['wroom'])) and L['set'] and L['set'].get('beat') == id,
              f'beats: {id} landed: {L} ({pg.ev("DM_UI.msg")[:120]})')
        if id == 'ps':
            play(20); o = occ('works.ps'); got[id] = o
            check(o and pg.ev("SHIP.works.tr.ps === undefined && worksOpened(SHIP.works).has('ps')"), f'beats: ps: Power safety not asked once up: {o}')
        elif id == 't3':
            T = pg.ev("({ cur: SHIP.works.cur && SHIP.works.cur.id + ':' + SHIP.works.cur.st, t3: puT3() })"); got[id] = T
            check(T['cur'] == 't3:do' and T['t3'] and T['t3']['day'] == 15 and not T['t3']['passed'], f'beats: t3: the test not held for you: {T}')
        elif id in ('t3res', 't3bar', 't3toast'):
            o = occ({'t3res': 'pu3Result', 't3bar': 'pu3Bar', 't3toast': 'pu3Toast'}[id]); got[id] = o
            check(len(o) == 1 and o[0][1] == L['wdeck'], f'beats: {id}: its occasion not booked here: {o}')
            if id != 't3res': check(L['rank'] == 'senior', f'beats: {id}: not a Senior Officer: {L["rank"]}')
        elif id in ('m19', 'm18', 'm20'):
            o = occ('works.' + id); c = pg.ev("SHIP.works.cur && SHIP.works.cur.id + ':' + SHIP.works.cur.st"); got[id] = (o, c)
            check(len(o) == 1 and o[0][1] == L['wdeck'] and c == id + ':meet', f'beats: {id}: its meeting not booked: {o} {c}')
        elif id == 'm21':
            o = occ('m21.brief'); got[id] = o
            check(len(o) == 1 and o[0][0] == '08:30' and o[0][1] == 1, f'beats: m21: the briefing not booked: {o}')
        else:   # the nights: on to the night's start, clock in at the time clock (p5nClock, as its tap does), then play
            n = {'n1': 22, 'n2': 23, 'n3': 24}[id]
            pg.ev(f"devmodeRun('Clock', () => devmodeSkipTo(p5NightOf({n}).from + 2))")
            ci = pg.ev("p5nClock(Math.floor(shipNow()), () => {})"); play(6)
            N = pg.ev(f"""({{ in: (SHIP.works.ns || {{}})[{n}] && SHIP.works.ns[{n}].in > 0, m23: m23State(), m24: m24State(), rows: [].concat(m23Items({n}), m24Items({n})).map(r => r.title), on23: m23On({n}), on24: m24On({n}),
              j1: (SHIP.jobs || []).some(j => j.type === 'm23night' && j.claimedBy === 'you') }})""")
            got[id] = {k: N[k] for k in ('in', 'rows', 'j1')}
            check(ci == 'in' and N['in'], f'beats: {id}: not clocked in for the night: {ci} {N["in"]}')
            if id == 'n1': check(N['on23'] and (N['j1'] or (N['m23'] and N['m23'].get('j1'))), f'beats: n1: night 1\'s work with Reyes not posted: {N["m23"]} {N["rows"]}')
            if id == 'n2': check(N['on23'] and N['rows'], f'beats: n2: night 2\'s reactor not on: {N["rows"]}')
            if id == 'n3': check(N['on24'] and N['rows'], f'beats: n3: night 3\'s coil swap not on: {N["rows"]}')
    for k, v in got.items(): print('   ', k, str(v)[:160])
    # Undo puts back the last Dev action: after the last night's clock-in skip, its landing (the jump itself before that)
    last = on[-1]; land = pg.ev(f"'Day ' + devmodeJumpOf('{last}').day + ','")
    pg.ev_reload('devmodeUndo()')
    U = pg.ev("({ beat: devmodeState().set && devmodeState().set.beat, clock: clockText() })")
    check(U['beat'] == last and U['clock'].startswith(land), f'beats: Undo after {last}\'s clock skip: {U}')
    check(not pg.errors, f'beats: errors {pg.errors[:3]}')
    pg.close(); ctx.close()
    # the same jump in two fresh browsers: the same save (within one page, see backlog DM1-3)
    saves = []
    for _ in range(2):
        c2 = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1); p2 = Page(c2, '#dev'); p2.sign(); p2.step(20)
        p2.ev("devmodeRun('Jump', () => devmodeSetCareerTo(16, devmodeJumpOf('t3res')))"); p2.ev('saveGame()'); saves.append(p2.ev('localStorage.getItem(SAVE_KEY)')); p2.close(); c2.close()
    check(saves[0] == saves[1], 'beats: the Tier 3 result jump twice (fresh browsers) gives different saves')
    print(f'  beats: {len(on)} jumps landed at their time and room, each beat booked or started (Power safety asked once up, the test held, result, bar, toast, the lessons, the briefing, the nights once clocked in); Undo; t3res twice the same save')
def j2_click(pg, text, wait=900):                 # a button on the open panel by its words (a Dev action: wait out its fade; wait 0: an ask, not redrawn)
    n = pg.ev(f"(() => {{ const b = [...document.querySelectorAll('#dmSheet button')].find(x => x.textContent === {json.dumps(text)}); if (!b || b.disabled) return b ? 'off' : 'none'; b.click(); return 'ok'; }})()")
    if n == 'ok' and wait: pg.page.wait_for_timeout(wait); pg.step(5)
    if wait: pg.ev('devmodeDraw()')
    return n

def j2_card(pg):                                  # the Running now card as drawn: its words and buttons
    return pg.ev("""(() => { const s = document.querySelector('#dmSheet .dmBody'), h = [...s.querySelectorAll('h3')].map(x => x.textContent);
      return { head: h.find(x => /^Running now/.test(x)) || null, text: s.textContent, buttons: Object.fromEntries([...s.querySelectorAll('button')].map(b => [b.textContent, !b.disabled])),
        wide: s.scrollWidth > s.clientWidth, small: [...document.querySelectorAll('#dmSheet button')].filter(b => b.offsetParent && b.getBoundingClientRect().height < 44).map(b => b.textContent) }; })()""")

J2_STATE = """(() => { const j = devmodeJumpOf(%s), w = j.where, n = eventNow(), t = (j.day - 1) * 1440 + j.at;
  return { clock: clockText(), want: 'Day ' + j.day + ',', at: hhmm(j.at), deck: deckDef.num, room: (ROOMS[roomAt(...player.here())] || {}).name || '', wdeck: w ? w.deck : null, wroom: w ? DECKS[w.deck].rooms[w.room].name : null,
    set: devmodeState().set, ev: SHIP.event && SHIP.event.id, ph: SHIP.event && SHIP.event.phase, now: n && n.id, nph: n && n.phase, want_ev: j.ev || null,
    meet: MEETINGS.filter(m => m.event === j.ev && m.at === t + 5).map(m => m.id), log: SHIP.eventLog.map(l => l.id),
    missed: SHIP.mail.filter(m => /missed/i.test(m.subject || '') || Object.values(INTRO_MEETINGS).some(x => m.subject === x.title + ' (notes)')).map(m => m.subject),
    sat: typeof stormSatDay === 'function' && stormSatDay() === j.day && playerCalledIn(j.day), fri: friShort(j.day), addr: eventsOn(j.day).some(e => e.id === 'captains-address' && e.from === j.at + 10),
    tern: typeof rotTernArrivals === 'function' ? rotTernArrivals(j.day).length : 0 }; })()"""

def part_events1(b):
    # J2 (plan v4.4): every Ship events jump lands at its day, time and room, a new Dev game run there with the event
    # started by the calendar's own rules (SHIP.event the jump's event, its phase caught up with eventNow; none yet before its first), the meetings
    # it lands before booked at their minute, no missed shift and no first-week notes; the Short Friday, the Friday address
    # and the rotation on their day; Undo after the last; one jump twice in fresh browsers gives the same save
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
    pg = Page(ctx, '#dev'); pg.sign(); pg.step(20)
    on = pg.ev("DM_JUMPS.filter(j => j.group === 'events' && devmodeJumpOn(j)).sort((a, b) => a.day - b.day || a.at - b.at).map(j => j.id)")
    if not on: print('  events1: none on in this build'); pg.close(); ctx.close(); return
    import time
    t0, got = time.time(), {}
    for id in on:
        r = pg.ev(f"devmodeRun('Jump', () => devmodeSetCareerTo(devmodeJumpOf('{id}').day, devmodeJumpOf('{id}')))"); pg.step(10)
        L = pg.ev(J2_STATE % json.dumps(id))
        got[id] = f"{L['clock']} {L['room'] or '-'} {L['ev'] or ''}:{L['ph'] or ''}{' meet ' + ','.join(L['meet']) if L['meet'] else ''}"
        check(r is True and L['clock'].startswith(L['want']) and L['clock'].endswith(L['at']) and (L['wdeck'] is None or (L['deck'] == L['wdeck'] and L['room'] == L['wroom'])) and L['set'] and L['set'].get('beat') == id,
              f'events1: {id} landed: {L} ({pg.ev("DM_UI.msg")[:120]})')
        check(not L['missed'], f'events1: {id}: a missed shift or first-week notes: {L["missed"]}')
        if L['want_ev']:
            check(L['ev'] == L['want_ev'] and L['now'] in (L['want_ev'], None) and L['ph'] == L['nph'] and L['want_ev'] not in L['log'], f'events1: {id}: the event not running as the calendar has it: {L}')
        if id in ('evStormBrief', 'evStormClear', 'evVisitAboard', 'evVisitGifts'): check(L['meet'], f'events1: {id}: its meeting not booked at its minute: {L["meet"]}')
        if id == 'evStormSat': check(L['sat'], f'events1: storm Saturday: not called in: {L}')
        if id == 'evShortFri': check(L['fri'], f'events1: the Short Friday: not a short Friday: {L}')
        if id == 'evFriAddress': check(L['addr'], f'events1: the Friday address not on its day at its time: {L}')
        if id == 'evRotation': check(L['tern'] > 0, f'events1: the rotation: nobody off the Tern: {L}')
    dt = time.time() - t0
    for k, v in got.items(): print('   ', k, v[:150])
    # Undo after the last jump: the one before it, back
    before = on[-2]; land = pg.ev(f"'Day ' + devmodeJumpOf('{before}').day + ','")
    pg.ev_reload('devmodeUndo()')
    U = pg.ev("({ beat: devmodeState().set && devmodeState().set.beat, clock: clockText() })")
    check(U['beat'] == before and U['clock'].startswith(land), f'events1: Undo after {on[-1]}: {U}')
    check(not pg.errors, f'events1: errors {pg.errors[:3]}')
    pg.close(); ctx.close()
    saves = []
    for _ in range(2):   # fresh browsers (within one page, see backlog DM1-3)
        c2 = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1); p2 = Page(c2, '#dev'); p2.sign(); p2.step(20)
        p2.ev("devmodeRun('Jump', () => devmodeSetCareerTo(devmodeJumpOf('evVisitAboard').day, devmodeJumpOf('evVisitAboard')))"); p2.ev('saveGame()'); saves.append(p2.ev('localStorage.getItem(SAVE_KEY)')); p2.close(); c2.close()
    check(saves[0] == saves[1], 'events1: the Veyli aboard jump twice (fresh browsers) gives different saves')
    print(f'  events1: {len(on)} jumps landed at their day, time and room in {dt:.0f} s, each event running by the calendar (its phase caught up), the meetings ahead booked, no miss or first-week notes; the Short Friday, the address, the rotation; Undo; the visit\'s jump twice the same save')

def part_events2(b):
    # J2: the Running now card. From the front (Day 12 13:55): the card at 390 px; a thread's + twice moves its band and
    # the event's, − puts it back; Next phase to the onset (14:00); Its meeting takes you to its room, the clock still. The
    # all-clear (Day 14): Next phase settles it, the threads greyed. The visit (Day 17): End and keep, one debrief, logged
    # once, SHIP.event cleared, today's plans made again; not started again, no second debrief by its last day; Undo
    # brings it back running. Nothing drawn without an event
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
    pg = Page(ctx, '#dev'); pg.sign(); pg.step(20)
    if not pg.ev("devmodeJumpOn(devmodeJumpOf('evStormFront')) && devmodeJumpOn(devmodeJumpOf('evVisitAboard'))"): print('  events2: the storm or the visit off in this build'); pg.close(); ctx.close(); return
    pg.ev('devmodeOpen(true); DM_UI.tab = "jump"; DM_UI.jg = "events"; DM_UI.msg = ""; devmodeDraw()')
    check(j2_card(pg)['head'] is None, 'events2: a Running now card with no event running')
    pg.ev("devmodeRun('Jump', () => devmodeSetCareerTo(12, devmodeJumpOf('evStormFront')))"); pg.step(10)
    pg.ev('DM_UI.tab = "jump"; DM_UI.jg = "events"; DM_UI.msg = ""; devmodeDraw()')
    C = j2_card(pg)
    check(C['head'] == 'Running now: Ion storm' and 'the warning' in C['text'] and C['buttons'].get('Next phase ›') and C['buttons'].get('Its meeting') and C['buttons'].get('End and keep') and not C['wide'] and not C['small'], f'events2: the card at 390 px: {C["head"]} {C["buttons"]} wide {C["wide"]} small {C["small"]}')
    pg.shot(str(SHOTS / 'jump-events-390.png')) if SHOTS else None
    th = pg.ev("(() => { const t = SHIP_EVENTS.ionStorm.threads[0]; return { id: t.id, label: t.label, k: dmEvStep(t) }; })()")
    B = lambda: pg.ev(f"({{ v: SHIP.event.threads['{th['id']}'] || 0, band: threadBand(SHIP_EVENTS.ionStorm.threads[0], SHIP.event.threads['{th['id']}'] || 0), all: eventBand('ionStorm', SHIP.event.threads) }})")
    b0 = B(); j2_click(pg, f"{th['label']} + {th['k']}"); j2_click(pg, f"{th['label']} + {th['k']}"); b2 = B(); j2_click(pg, f"{th['label']} − {th['k']}"); j2_click(pg, f"{th['label']} − {th['k']}"); b4 = B()
    check(b0['v'] == 0 and b2['v'] == 2 * th['k'] and b2['band'] != b0['band'] and b4 == b0, f'events2: the threads − and +: {b0} {b2} {b4}')
    j2_click(pg, 'Next phase ›'); P = pg.ev("({ clock: clockText(), ph: SHIP.event && SHIP.event.phase })")
    check(P['clock'].endswith('14:00') and P['ph'] == 'onset', f'events2: Next phase: {P}')
    G = pg.ev("(() => { const g = dmEvMeet(SHIP.event, SHIP_EVENTS[SHIP.event.id], shipNow()); return g && { deck: g.deck, room: DECKS[g.deck].rooms[g.room].name, label: g.label }; })()")
    clk = pg.ev('clockText()'); j2_click(pg, 'Its meeting')
    M = pg.ev("({ deck: deckDef.num, room: (ROOMS[roomAt(...player.here())] || {}).name, clock: clockText() })")
    check(G and M['deck'] == G['deck'] and M['room'] == G['room'] and M['clock'] == clk, f'events2: Its meeting: {G} -> {M}')
    # the all-clear settles the result: the threads greyed
    pg.ev("devmodeRun('Jump', () => devmodeSetCareerTo(14, devmodeJumpOf('evStormClear')))"); pg.step(10)
    pg.ev('DM_UI.msg = ""; devmodeDraw()'); j2_click(pg, 'Next phase ›'); C = j2_card(pg)
    tb = {k: v for k, v in C['buttons'].items() if re.search(r' [−+] \d+$', k)}
    check(pg.ev("!!(SHIP.event && SHIP.event.mine.settled)") and tb and not any(tb.values()) and 'settled' in C['text'], f'events2: settled at the all-clear, the threads greyed: {pg.ev("SHIP.event && SHIP.event.mine.settled")} {tb}')
    # End and keep on the visit (Day 17 09:55)
    pg.ev("devmodeRun('Jump', () => devmodeSetCareerTo(17, devmodeJumpOf('evVisitAboard')))"); pg.step(10)
    pg.ev('DM_UI.msg = ""; devmodeDraw()')
    deb = "SHIP.mail.filter(m => m.subject === SHIP_EVENTS.diplomatic.title + ': how it went').length"
    pg.ev("window.__j2day = SHIP_DAYS.get(SHIP.time.day)")
    j2_click(pg, 'End and keep', 0); j2_click(pg, 'Tap again: end it')
    E = pg.ev(f"({{ ev: SHIP.event && SHIP.event.id, log: SHIP.eventLog.filter(l => l.id === 'diplomatic').length, deb: {deb}, replan: SHIP_DAYS.get(SHIP.time.day) !== window.__j2day, msg: DM_UI.msg, card: !!document.querySelector('#dmSheet h3') && [...document.querySelectorAll('#dmSheet h3')].some(h => /^Running now/.test(h.textContent)) }})")
    check(E['ev'] is None and E['log'] == 1 and E['deb'] == 1 and E['replan'] and not E['card'] and 'ended now and kept' in E['msg'], f'events2: End and keep: {E}')
    pg.ev_reload('devmodeUndo()')   # Undo: the visit back, running
    U = pg.ev("({ ev: SHIP.event && SHIP.event.id, log: SHIP.eventLog.filter(l => l.id === 'diplomatic').length, clock: clockText() })")
    check(U['ev'] == 'diplomatic' and U['log'] == 0, f'events2: Undo after End and keep: {U}')
    pg.ev('devmodeOpen(true); DM_UI.tab = "jump"; DM_UI.jg = "events"; DM_UI.msg = ""; devmodeDraw()')
    j2_click(pg, 'End and keep', 0); j2_click(pg, 'Tap again: end it')
    pg.ev("devmodeRun('Clock', () => devmodeSkipTo(19 * 1440 - 30))"); pg.step(10)   # on to the end of its last day (Day 19)
    A = pg.ev(f"({{ ev: SHIP.event && SHIP.event.id, log: SHIP.eventLog.filter(l => l.id === 'diplomatic').length, deb: {deb}, clock: clockText() }})")
    check(A['ev'] != 'diplomatic' and A['log'] == 1 and A['deb'] == 1, f'events2: after End and keep, to its last day: started again or a second debrief: {A}')
    check(not pg.errors, f'events2: errors {pg.errors[:3]}')
    pg.close(); ctx.close()
    print(f'  events2: no card without an event; the card at 390 px; {th["label"]} + and − move its band and back; Next phase to the onset; Its meeting ({G["room"] if G else "-"}); settled at the all-clear, threads greyed; End and keep on the visit (one debrief, logged once, replanned, not again by Day 19); Undo back to running')
def j3_page(b):
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
    pg = Page(ctx, '#dev'); pg.sign(); pg.step(20); return ctx, pg

def j3_jump(pg, id, ans=None):                    # a jump from the list, with the answers row set to ans first
    if ans: pg.ev(f"Object.assign(DM_UI.ans, {json.dumps(ans)})")
    r = pg.ev(f"devmodeRun('Jump', () => devmodeSetCareerTo(devmodeJumpOf('{id}').day, devmodeJumpOf('{id}')))"); pg.step(10)
    L = pg.ev(f"""(() => {{ const j = devmodeJumpOf('{id}'), w = j.where, E = SHIP.end || {{}};
      return {{ clock: clockText(), want: 'Day ' + j.day + ',', at: hhmm(j.at), deck: deckDef.num, room: (ROOMS[roomAt(...player.here())] || {{}}).name || '', wdeck: w ? w.deck : null, wroom: w ? DECKS[w.deck].rooms[w.room].name : null,
        q: SHIP.works.end && SHIP.works.end.answer, qday: SHIP.works.end && SHIP.works.end.day, offer: E.offer || null, said: typeof endSaid === 'function' ? endSaid() : null, settled: E.settled || null, ended: E.ended || null,
        stay: typeof endgameDay === 'function' ? endgameDay() : null, oday: typeof endOfferDay === 'function' ? endOfferDay() : null, post: typeof endPostKind === 'function' ? endPostKind() : null,
        occ: (SHIP.occasions || []).filter(o => o.id === 'endingOffer' && o.status === 'asked').map(o => [hhmm(o.at % 1440), o.deck, o.room]), set: devmodeState().set }}; }})()""")
    check(r is True and L['clock'].startswith(L['want']) and L['clock'].endswith(L['at']) and (L['wdeck'] is None or (L['deck'] == L['wdeck'] and L['room'] == L['wroom'])) and L['set'] and L['set'].get('beat') == id,
          f'{id}: landed: {L} ({pg.ev("DM_UI.msg")[:120]})')
    return L

def part_ending1(b):
    # J3 (plan v4.4): the answers row draws; the offer (Day 32: Calder's question answered on the way, the offer booked at
    # 16:00 in the ready room, not yet heard); your answer still open (Day 34: heard, Unsure, not settled); the address
    # (Day 35: the row's answer, Stay, said and not yet settled); the four answers to Calder's question each give their post
    ctx, pg = j3_page(b)
    if not pg.ev("DM_J3()"): print('  ending1: the ending off in this build'); pg.close(); ctx.close(); return
    pg.ev('devmodeOpen(true); DM_UI.tab = "jump"; DM_UI.jg = "ending"; DM_UI.msg = ""; devmodeDraw()')
    J = pg.ev("""({ heads: [...document.querySelectorAll('#dmSheet h3')].map(h => h.textContent), rows: [...document.querySelectorAll('#dmSheet .dmJump')].length,
      on: [...document.querySelectorAll('#dmSheet .dmGroups button.dmAsk')].map(b => b.textContent), wide: document.querySelector('#dmSheet .dmBody').scrollWidth > document.querySelector('#dmSheet .dmBody').clientWidth,
      small: [...document.querySelectorAll('#dmSheet button')].filter(b => b.offsetParent && b.getBoundingClientRect().height < 44).map(b => b.textContent) })""")
    check('Your answers on the way' in J['heads'] and J['rows'] == 7 and 'Engines' in J['on'] and 'Stay' in J['on'] and not J['wide'] and not J['small'], f'ending1: the ending\'s list and answers row at 390 px: {J}')
    pg.shot(str(SHOTS / 'jump-ending-390.png')) if SHOTS else None
    L = j3_jump(pg, 'endOffer')
    check(L['q'] == 'engines' and L['oday'] == 32 and L['occ'] == [['16:00', 1, 'R']] and not (L['offer'] or {}).get('met'), f'ending1: the offer: {L}')
    L = j3_jump(pg, 'endOpen', {'offer': 'go'})   # its own answer (Unsure) wins over the row
    check(L['offer'] and L['offer'].get('met') and L['said'] == 'unsure' and not L['settled'], f'ending1: still open: {L}')
    L = j3_jump(pg, 'endAddress', {'offer': 'stay'})
    check(L['offer'] and L['offer'].get('met') and L['said'] == 'stay' and not L['settled'], f'ending1: before the address: {L}')
    posts = {}
    for k in ('engines', 'bridge', 'teach', 'unsure'):
        pg.ev(f"devmodeRun('Set career', () => devmodeSetCareerTo(27, null, {{ ans: {{ cq: '{k}' }} }}))")
        posts[k] = pg.ev("({ a: SHIP.works.end && SHIP.works.end.answer, post: endPostKind() })")
    check(all(posts[k]['a'] == k for k in posts) and [posts[k]['post'] for k in ('engines', 'bridge', 'teach', 'unsure')] == ['engines', 'bridge', 'teach', 'unsure'], f'ending1: Calder\'s four answers and their posts: {posts}')
    pg.ev("Object.assign(DM_UI.ans, { cq: 'engines', offer: 'stay' })")
    check(not pg.errors, f'ending1: errors {pg.errors[:3]}')
    pg.close(); ctx.close()
    print(f'  ending1: the list (7) and the answers row at 390 px; the offer booked 16:00 in the ready room (Engines put in on the way); still open (Unsure, its own); before the address (Stay); the four answers give their four posts')

def part_ending2(b):
    # J3: the goodbye (Day 36: settled Go, the shuttle bay, going); the end page (ended, the page up); staying on (the
    # endgame from Day 36, in bed); the slower career (Calder asks Day 33, the offer Day 39 in the ready room); and the
    # Traditions card's Its next showing (the clock to 10 minutes before its next calendar day, refused past 14 days)
    ctx, pg = j3_page(b)
    if not pg.ev("DM_J3()"): print('  ending2: the ending off in this build'); pg.close(); ctx.close(); return
    L = j3_jump(pg, 'endBye')
    check(L['settled'] and L['settled']['choice'] == 'go' and pg.ev("endGoing()"), f'ending2: the goodbye: {L}')
    L = j3_jump(pg, 'endPage')
    pg.step(5); page = pg.ev("!!document.querySelector('#endPage') && !document.querySelector('#endPage').hidden")
    check(L['ended'] and page, f'ending2: the end page: ended {L["ended"]}, page {page}')
    pg.reload()   # the page holds the screen: a fresh load (the Dev save keeps the ended game)
    L = j3_jump(pg, 'endStay')
    check(L['settled'] and L['settled']['choice'] == 'stay' and L['stay'] == 36 and not L['ended'], f'ending2: staying on: {L}')
    L = j3_jump(pg, 'endSlow')
    check(L['qday'] == 33 and L['q'] == 'engines' and L['oday'] == 39 and L['occ'] == [['16:00', 1, 'R']] and L['set'].get('slow') == 7, f'ending2: the slower career: {L}')
    # Its next showing (from a Day 3 game): quiz night's next Thursday, 10 minutes before; a tradition weeks off refused
    pg.ev("devmodeRun('Set career to Day 3', () => devmodeSetCareerTo(3))")
    q = pg.ev("SHIP_TRADITIONS.find(e => /quiz/i.test(e.name)).id")
    pg.ev(f"DM_HOLD = false; devmodeTradNextGo(SHIP_TRADITIONS.find(e => e.id === '{q}'))"); pg.page.wait_for_timeout(800); pg.step(5)
    N = pg.ev(f"(() => {{ const e = eventsOn(SHIP.time.day).find(x => x.id === '{q}'); return {{ clock: clockText(), from: e ? e.from : null, min: SHIP.time.min, msg: DM_UI.msg }}; }})()")
    check(N['from'] is not None and round(N['min']) == N['from'] - 10, f'ending2: Its next showing (quiz night): {N}')
    far = pg.ev("(() => { const d = SHIP.time.day; const e = SHIP_TRADITIONS.find(x => { const n = devmodeTradNext(x, d); return n != null && n - d > DM_NEXTMAX; }); return e ? e.id : null; })()")
    if far:
        before = pg.ev("clockText()"); pg.ev(f"devmodeTradNextGo(SHIP_TRADITIONS.find(e => e.id === '{far}'))")
        check(pg.ev("clockText()") == before and 'more than' in pg.ev("DM_UI.msg"), f'ending2: a showing weeks off not refused: {far} {pg.ev("DM_UI.msg")}')
    check(not pg.errors, f'ending2: errors {pg.errors[:3]}')
    pg.close(); ctx.close()
    print(f'  ending2: the goodbye (settled Go, the bay); the end page; staying on (the endgame from Day 36); the slower career (asked Day 33, the offer Day 39); Its next showing (quiz night, {N["clock"]}), and refused weeks off ({far})')

with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
    for name, part in (('off', part_off), ('real', part_real), ('card', part_card), ('store', part_store)):
        if ONLY and name not in ONLY: continue
        try: part(ctx)
        except Exception as e: fail(f'{name}: stopped: {str(e)[:300]}')
    for name, part in (('clock', part_clock), ('move', part_move), ('slow', part_slow), ('trad', part_trad), ('set', part_set), ('career', part_career), ('t4beats', part_t4beats),
                       ('jumps', part_jumps), ('beats', part_beats), ('events1', part_events1), ('events2', part_events2), ('ending1', part_ending1), ('ending2', part_ending2)):
        if ONLY and name not in ONLY: continue
        try: part(b)
        except Exception as e: fail(f'{name}: stopped: {str(e)[:300]}')
    b.close()

print('DEVMODE CHECK OK' if ok else 'DEVMODE CHECK FAILED')
sys.exit(0 if ok else 1)
