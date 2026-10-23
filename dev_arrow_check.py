# Starship Cadet: the Dev career arrow check (section 25's slot, DV1; design-doc "Dev mode", the career arrow)
# Opens the game at phone size (390 x 844) and checks:
#   off:   without #dev there is no Dev arrow (no #dmArrow, dvCareerNext() gives nothing)
#   walk:  in Dev mode, the arrow names the right next career step at each of the first steps: the arrival evening
#          (Calder's Monday briefing, tomorrow 08:50); a Skip-to-Monday game before any job (clock in, for the shadow
#          shift Rounds needs); the shadow shift done (Rounds training: Torres asks you, tomorrow 06:00); Day 2 after the
#          ask (Torres's meeting, at the meeting's own time); watching him; your turn; trained (one more round, for
#          Hauling); the round done (Hauling training: Yara asks you, tomorrow 06:00); and it still points with the
#          Teaching arrows Off and tracking off, and on another deck it points at the lift with the deck named
#   look:  the arrow is drawn (its own element, the DEV tag), holds still over frames, its pin never on the game's pin
#          when both point at the same thing; Hide it and Show it from the Quick tab, the choice kept over a reload
# Setup and environment as for cadet_test.py (CADET_WORK, CADET_CHROME).
# Run:  python3 dev_arrow_check.py BUILD.html [part ...]   Good is DEV ARROW CHECK OK (exit 0); a failure exits 1.
import sys, os, re, pathlib
exec(open(__file__.replace('dev_arrow_check.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright

ok = True
def fail(msg):
    global ok
    ok = False
    print('FAIL', msg)
def check(cond, msg):
    if not cond: fail(msg)
    return cond

GAME = sys.argv[1]
ONLY = set(sys.argv[2:])
TMP = WORK / 'test' / '_dev_arrow_check.html'
TMP.write_text(instrument(pathlib.Path(GAME).read_text()))

class Page:
    def __init__(self, ctx, suffix):
        self.errors = []
        self.page = ctx.new_page()
        self.page.on('pageerror', lambda e: self.errors.append(f'pageerror: {e}'))
        self.page.on('console', lambda m: m.type == 'error' and self.errors.append(f'error: {m.text}'))
        self.page.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
        self.page.add_init_script(INIT)
        self.page.goto('file://' + str(TMP) + suffix)
        self.ready()
    def ready(self):
        self.page.wait_for_function('window.__sc !== undefined', timeout=90000)
        self.page.add_style_tag(content='*,*::before,*::after{transition:none!important;animation:none!important}')
        self.ev("(() => { const rr = renderer.render.bind(renderer); renderer.render = (s, c) => {}; })()")   # no drawing (slow headless)
        self.step(20)
    def ev(self, src):
        return self.page.evaluate('s => window.__sc(s)', src)
    def step(self, n, dt=1000 / 30):
        self.page.evaluate(f'window.__step({n}, {dt})')
    def sign(self):
        if self.page.locator('text=Sign and go aboard').count():
            self.page.fill('form input', 'Ada'); self.page.click('text=Sign and go aboard'); self.step(30)
    def next(self):
        self.step(3)
        return self.ev("(() => { const g = dvCareerNext(); return g ? { label: g.label, deck: g.deck, key: g.key, crew: g.crew || null } : null; })()") or {}

def part_off(b):
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
    pg = Page(ctx, '')
    check(pg.ev("document.getElementById('dmArrow') === null && dvCareerNext() === null"), 'off: a Dev arrow without the Dev link')
    check(not pg.errors, f'off: errors {pg.errors[:3]}')
    ctx.close()
    print('  off: no Dev arrow without #dev')

def part_walk(b):
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
    pg = Page(ctx, '#dev'); pg.sign()
    seen = []
    def want(n, *parts):
        g = pg.next(); seen.append(g.get('label'))
        check(all(p in (g.get('label') or '') for p in parts), f'walk {n}: wanted {parts}, the arrow says {g}')
        return g
    want(1, 'Monday briefing', 'tomorrow 08:50')                     # the arrival evening
    pg.ev('newGameStart(false); introSkip(); careerInit(); SHIP.career.gs = DM_SEED; devmodeState().ex = []; devmodeState().note = ""'); pg.step(10)
    check(pg.ev('clockText()') == 'Day 1, Monday 06:00', f'walk: the Skip-to-Monday game starts at {pg.ev("clockText()")}')
    want(2, 'Clock in', 'shadow shift', 'Rounds', '08:00')
    pg.ev("(devmodeW(), SHIP.works.log.push(['dv-check', 1, 0, 'lights', null]))")   # a job turned in: the shadow shift's stand-in
    want(3, 'Rounds training', 'Zeke asks you', 'tomorrow 06:00')
    pg.ev("devmodeRun('Clock', () => devmodeSkipTo(1440 + 10 * 60))"); pg.step(10)
    c = pg.ev("SHIP.works.cur && { id: SHIP.works.cur.id, st: SHIP.works.cur.st }")
    if not (c and c.get('id') == 'm1'):
        pg.ev('ladderTick(Math.floor(shipNow() / 60))'); c = pg.ev("SHIP.works.cur && { id: SHIP.works.cur.id, st: SHIP.works.cur.st }")
    check(c and c.get('id') == 'm1' and c.get('st') == 'meet', f'walk: Day 2 10:00, Rounds not asked: {c}')
    at = pg.ev("(() => { const c = SHIP.works.cur, r = SHIP.occasions.find(x => x.key === c.occ); return r ? hhmm(r.at % 1440) : '?'; })()")
    now = pg.ev('hhmm(shipNow() % 1440)')
    want(4, 'Zeke\'s meeting: rounds', at if at > now else '')
    pg.ev("(() => { const c = SHIP.works.cur; trainWatch(ladderRow('m1'), c, Math.floor(shipNow()), false); })()")   # Rounds has no watch step (WORK_MECH.m1.self: the talk, then yours)
    if check(pg.ev('SHIP.works.cur.st') == 'do', f'walk: Rounds after the meeting is not your turn: {pg.ev("SHIP.works.cur.st")}'):
        want(5, 'Your turn: rounds')
    # a watch step, on paper (Hauling's: Yara leads, you watch): the arrow at her
    pg.ev("SHIP.works._dv = SHIP.works.cur; SHIP.works.cur = { id: 'm4', st: 'watch', d: 2, by: 'esposito-yara', occ: null, j: null, w: 0 }")
    g = want(6, 'Watch Yara: hauling'); check(g.get('crew') == 'esposito-yara', f'walk 6: not at Yara: {g}')
    pg.ev("SHIP.works.cur = SHIP.works._dv; delete SHIP.works._dv")
    pg.ev("worksTrained('m1')")
    want(7, 'Rounds: 1 more', 'Hauling')
    pg.ev('SHIP.works.use.m1 = 1')
    want(8, 'Hauling and stores training', 'Yara asks you', 'tomorrow 06:00')
    # whatever the Teaching arrows say, tracking off, and a goal tracked by hand
    pg.ev("GUIDE.mode = 'off'; SHIP.player.track = null; setGoal({ deck: 3, room: 'K', label: 'A goal of my own' })")
    want(9, 'Hauling and stores training')
    pg.ev("GUIDE.mode = null; SHIP.player.track = undefined; clearGoal()")
    # another deck: the lift's panel, the deck named
    pg.ev('goToDeck(3)'); pg.step(20)
    lab = pg.ev("document.querySelector('#dmArrow .dvlab').textContent")
    check(lab.startswith('DEVDeck 5 · Hauling'), f'walk 10: on Deck 3 the arrow says {lab!r}')
    check(not pg.errors, f'walk: errors {pg.errors[:3]}')
    ctx.close()
    print('  walk: ' + ' | '.join(str(s) for s in seen))

def part_look(b):
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
    pg = Page(ctx, '#dev'); pg.sign()
    pg.ev('newGameStart(false); introSkip(); careerInit(); SHIP.career.gs = DM_SEED; devmodeState().ex = []'); pg.step(10)
    pg.ev("devmodeRun('Clock', () => devmodeSkipTo(8 * 60 + 5))"); pg.step(10)
    if pg.ev('deckDef.num') != 5: pg.ev('goToDeck(5)'); pg.step(20)
    pos = lambda sel: pg.ev(f"(() => {{ const e = document.querySelector('{sel}'); if (!e || e.offsetParent === null && getComputedStyle(e).position !== 'fixed') return null; const r = e.getBoundingClientRect(); return r.width ? [Math.round(r.left), Math.round(r.top), Math.round(r.width)] : null; }})()")
    shown = pg.ev("!document.getElementById('dmArrow').hidden && document.querySelector('#dmArrow .dvlab b').textContent === 'DEV'")
    check(shown, 'look: the Dev arrow is not shown with its DEV tag')
    a = [pg.ev("document.getElementById('dmArrow').style.transform")]
    for _ in range(8): pg.step(1); a.append(pg.ev("document.getElementById('dmArrow').style.transform"))
    check(len(set(a)) == 1, f'look: the Dev arrow moves with nothing moving: {sorted(set(a))[:3]}')
    # both arrows at the same thing (clock in: the game's arrow and ours both at the time clock): pins apart
    pg.ev("setGoal({ deck: 5, place: '5-timeclock-1', label: 'Clock in' })"); pg.step(4)
    same = pg.ev("(() => { const g = dvCareerNext(); return g && g.place === '5-timeclock-1'; })()")
    boxes = lambda sel: pg.ev(f"[...document.querySelectorAll('{sel} > div')].filter(e => getComputedStyle(e).display !== 'none' && !e.closest('[hidden]')).map(e => e.getBoundingClientRect().toJSON())")
    def apart(where):
        G, D = boxes('#ixGoal'), boxes('#dmArrow')
        hit = [(a, c) for a in G for c in D if not (a['right'] <= c['left'] or c['right'] <= a['left'] or a['bottom'] <= c['top'] or c['bottom'] <= a['top'])]
        check(G and D and not hit, f'look: {where}: the two arrows cover each other (game {len(G)} parts, dev {len(D)}): {hit[:1]}')
    if check(same, 'look: both arrows should be at the time clock'):
        apart('the time clock off screen')
        pg.ev("(() => { const s = placeSpot('5-timeclock-1'); player.obj.position.set(s.x + 1.5, 0, s.z + 2.5); })()"); pg.step(90)
        on = pg.ev("getComputedStyle(document.querySelector('#ixGoal .ixpin')).display !== 'none'")
        apart('the time clock ' + ('on screen' if on else 'off screen, close by'))
    b1 = [pg.ev("document.getElementById('dmArrow').style.transform")]
    for _ in range(6): pg.step(1); b1.append(pg.ev("document.getElementById('dmArrow').style.transform"))
    check(len(set(b1)) == 1, f'look: with both arrows up, the Dev arrow flickers: {sorted(set(b1))[:3]}')
    pg.ev('clearGoal()')
    # Hide it / Show it (the Quick tab), kept over a reload
    pg.ev("devmodeOpen(true); DM_UI.tab = 'quick'; devmodeDraw()")
    pg.page.click('#dmSheet button:text-is("Hide it")'); pg.step(3)
    check(pg.ev("document.getElementById('dmArrow').hidden"), 'look: Hide it left the arrow up')
    pg.page.reload(); pg.ready(); pg.step(10)
    check(pg.ev("document.getElementById('dmArrow').hidden && DV.on === false"), 'look: hidden, then a reload: back up')
    pg.ev("devmodeOpen(true); DM_UI.tab = 'quick'; devmodeDraw()")
    pg.page.click('#dmSheet button:text-is("Show it")'); pg.step(3)
    check(pg.ev("DV.on === true && (!document.getElementById('dmArrow').hidden || dvCareerNext() === null)"), 'look: Show it did not bring it back')
    txt = pg.ev("document.querySelector('#dmSheet .dmBody').textContent")
    check('Career arrow (Dev only)' in txt and 'The magenta DEV arrow:' in txt, f'look: the Quick tab row: {txt[-200:]}')
    check(not pg.errors, f'look: errors {pg.errors[:3]}')
    ctx.close()
    print('  look: drawn with its tag, still over frames, apart from the game\'s pin, Hide/Show kept over a reload')

with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    for name, part in (('off', part_off), ('walk', part_walk), ('look', part_look)):
        if ONLY and name not in ONLY: continue
        try: part(b)
        except Exception as e: fail(f'{name}: stopped: {str(e)[:300]}')
    b.close()

print('DEV ARROW CHECK OK' if ok else 'DEV ARROW CHECK FAILED')
sys.exit(0 if ok else 1)
