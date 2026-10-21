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
# Setup and environment as for cadet_test.py (CADET_WORK, CADET_CHROME).
# Run:  python3 devmode_check.py BUILD.html [part ...]   (parts: only those)   Good is DEVMODE CHECK OK (exit 0); a failure exits 1.
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
ONLY = set(sys.argv[2:])                          # optional: run only these parts (e.g. trad)
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
      for (const r of DM_CAREER) for (const id of r.train || []) { seen.add(id); const row = ladderRow(id); if (!row || row.day !== r.day) out.push(id + ': table ' + r.day + ', ladder ' + (row ? row.day : 'none')); }
      for (const row of CAREER_LADDER) if (row.day <= DM_MAXDAY && !seen.has(row.id)) out.push(row.id + ': on the ladder (Day ' + row.day + '), not in the table');
      return out; })()""")
    check(not bad, f'set: the table and CAREER_LADDER disagree: {bad}')
    setc = lambda n: pg.ev(f"devmodeRun('Set career to Day {n}', () => devmodeSetCareerTo({n}))")
    pg.ev("devmodeRun('Clock: +3 hours', () => devmodeSkipTo(shipNow() + 180))"); before = pg.ev('clockText()')
    got = {}
    for n in (2, 10, 12, 26):
        check(setc(n) is True, f'set: Day {n} refused: {pg.ev("DM_UI.msg")}')
        pg.step(20)
        S = pg.ev(f"""(() => {{ const W = SHIP.works, c = devmodeCareerFor({n}); return {{ clock: clockText(), rank: W && W.rank, tier: W && W.tier, xp: W && W.xp, tr: W && Object.keys(W.tr).sort().join(), want: Object.keys(c.tr).sort().join(),
          wrank: c.rank, cur: W && W.cur, room: ROOMS[roomAt(...player.here())].name, bed: roomAt(...player.here()) === roomAt(...(DECKS[deckOf(playerBed())].places.find(p => p.id === playerBed()) || {{ at: [0, 0] }}).at), deck: deckDef.num, pip: PLAYER_SPEC.rank || 0,
          ms: SHIP.career.ms, st: SHIP.career.st, missed: SHIP.mail.filter(m => /missed|summons|warning/i.test(m.subject || '') || Object.values(INTRO_MEETINGS).some(x => m.subject === x.title + ' (notes)')).map(m => m.subject), open: SHIP.occasions.filter(o => o.status === 'asked').map(o => o.id),
          met: INTRO_WEEK.filter(b => b.meeting && introAbs(b.day, b.at) < shipNow()).every(b => SHIP.intro.done[b.id + ':met'] >= 0), set: devmodeState().set, settle: !!SHIP.intro.settle.all }}; }})()""")
        got[n] = S
        check(S['clock'].startswith(f'Day {n},') and S['clock'].endswith('06:00'), f'set: Day {n} landed at {S["clock"]}')
        check(S['rank'] == S['wrank'] and S['tr'] == S['want'] and S['cur'] is None, f'set: Day {n}: the career isn\'t the table\'s: {S}')
        check(S['bed'] and S['deck'] == 4, f'set: Day {n}: not woken in your bed\'s room ({S["room"]})')
        check(S['ms'] == 0 and S['st'] == 0 and not S['missed'] and not S['open'], f'set: Day {n}: a miss, a first-week meeting\'s notes, a summons or something still asking: {S}')
        check(S['met'] and S['set']['day'] == n and (S['settle'] == (n > 7)), f'set: Day {n}: the first week or the Dev record: {S}')
    sick = pg.ev("Array.from({ length: DM_MAXDAY + 15 }, (_, i) => i + 1).filter(d => sickDue(d))")
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
    pg.ev("devmodeRun('Clock', () => devmodeSkipTo(9 * 1440 + 11 * 60 + 2))")
    P = pg.ev("({ clock: clockText(), rank: SHIP.works.rank, passed: SHIP.works.test && SHIP.works.test.passed, summons: SHIP.occasions.some(o => o.id === 'promoSummons') })")
    check(P['rank'] == 'junior' and P['passed'] and P['summons'], f'set: the Day 10 promotion beat (at 11:02 the summons is booked, still a junior): {P}')
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
    pg.ev("devmodeRun('Clock', () => devmodeSkipTo(devmodeNext(20 * 60)))")
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

with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
    for name, part in (('off', part_off), ('real', part_real), ('card', part_card), ('store', part_store)):
        if ONLY and name not in ONLY: continue
        try: part(ctx)
        except Exception as e: fail(f'{name}: stopped: {str(e)[:300]}')
    for name, part in (('clock', part_clock), ('move', part_move), ('slow', part_slow), ('trad', part_trad), ('set', part_set), ('career', part_career)):
        if ONLY and name not in ONLY: continue
        try: part(b)
        except Exception as e: fail(f'{name}: stopped: {str(e)[:300]}')
    b.close()

print('DEVMODE CHECK OK' if ok else 'DEVMODE CHECK FAILED')
sys.exit(0 if ok else 1)
