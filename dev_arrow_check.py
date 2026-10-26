# Starship Cadet: the Dev career arrow check (section 25's slot, DV1; design-doc "Dev mode", the career arrow)
# Opens the game at phone size (390 x 844) and checks:
#   off:   without #dev there is no Dev arrow (no #dmArrow, dvCareerNext() gives nothing)
#   walk:  in Dev mode, the arrow names the right next career step at each of the first steps: the arrival evening
#          (Calder's Monday briefing, tomorrow 08:50); a Skip-to-Monday game before any job (clock in, for the shadow
#          shift Rounds needs); the shadow shift done (Rounds training: Torres asks you, tomorrow 06:00); Day 2 after the
#          ask (Torres's meeting, at the meeting's own time); watching him; your turn; trained (one more round, for
#          Hauling); the round done (Hauling training: Yara asks you, tomorrow 06:00); and it still points with the
#          Teaching arrows Off and tracking off, and on another deck it points at the lift with the deck named
#   s5:    Pillar 5 Step 5 with P5_STEP5 on (B1): Power safety's arrow, the Tier 3 rows, the Senior Officer presets
#   look:  the arrow is drawn (its own element, the DEV tag), holds still over frames, its pin never on the game's pin
#          when both point at the same thing; Hide it and Show it from the Quick tab, the choice kept over a reload
# Setup and environment as for cadet_test.py (CADET_WORK, CADET_CHROME).
# Run:  python3 dev_arrow_check.py BUILD.html [part ...]   Good is DEV ARROW CHECK OK (exit 0); a failure exits 1.
import sys, os, re, pathlib
exec(open(__file__.replace('dev_arrow_check.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
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

GAME = sys.argv[1]
ONLY = set(sys.argv[2:])
TMP = WORK / 'test' / ('_dev_arrow_check_' + RUN_ID + '.html')
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

# s5 (Pillar 5 Step 5, S5-1 turn 3, B1): with P5_STEP5 on, an Officer set to Day 11 (Tracing done) on Day 12: the arrow names
# Power safety (Calder asks you), then her appointment at the Deck 6 port junction once asked, and not once trained; the
# Day 14 preset's Training tab shows "Your promotion: the Tier 3 test" with Relied on and Power safety ticked; the Day 16
# and 21 presets are a Senior Officer (Tier 3, the test passed, the milestone; Trusted by Day 21). Off: "not yet".
def part_s5(b):
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
    pg = Page(ctx, '#dev'); pg.sign()
    if not pg.ev("typeof P5_STEP5 !== 'undefined' && P5_STEP5"):
        print('  s5: not yet (P5_STEP5 off)'); ctx.close(); return
    pg.ev('newGameStart(false); introSkip(); careerInit(); SHIP.career.gs = DM_SEED; devmodeState().ex = []; devmodeState().note = ""'); pg.step(10)
    pg.ev("(devmodeSkipTo(11 * 1440 + 300), devmodeCareerSet(11, shipNow()), SHIP.works.tr.m9 = 11, (SHIP.works.op[11] = SHIP.works.op[11] || []).push('m9'))"); pg.step(5)   # Tracing's ask is at 06:00 too: done here, so the next step is Power safety
    g = pg.next()
    check('Power safety' in (g.get('label') or '') and 'asks you' in (g.get('label') or ''), f"s5: Day 12 before the ask, the arrow names Power safety's ask: {g}")
    pg.ev("(() => { for (let m = 11 * 1440 + 360; m <= 11 * 1440 + 420; m += 5) { setShipNow(m); machinesNow(); worksCareerTick(m); } })()"); pg.step(5)
    asked = pg.ev("SHIP.occasions.filter(x => x.id === 'works.ps').map(x => [x.deck, x.room, hhmm(x.at % 1440)])")
    pg.ev("(() => { const r = SHIP.occasions.find(x => x.id === 'works.ps'); if (r) { setShipNow(r.at - 14); machinesNow(); } })()")   # 14 minutes before it (before then, clocking in comes first)
    g = pg.next()
    check(asked and asked[0][:2] == [6, 'j'], f"s5: Calder's appointment made at the Deck 6 port junction: {asked}")
    check('Power safety with' in (g.get('label') or '') and g.get('deck') == 6, f"s5: the arrow names her appointment on Deck 6: {g}")
    pg.ev("worksTrained('ps')"); g = pg.next()
    check('Power safety' not in (g.get('label') or ''), f"s5: trained, the arrow moves on: {g}")
    rows = pg.ev("(devmodeCareerSet(14, shipNow()), JSON.parse(JSON.stringify(puCheck())))")
    flat = ' | '.join((r.get('text') or '') + ' ' + ' '.join(x['text'] + ':' + x.get('sub', '') for x in r.get('rows', [])) for r in rows)
    check('Your promotion: the Tier 3 test' in flat and 'Relied on' in flat and 'Power safety:Done' in flat and "you're Relied on):Done" in flat, f"s5: the Day 14 preset's Training tab rows: {flat}")
    c = pg.ev("[16, 21].map(n => { const c = devmodeCareerFor(n); return [c.tier, c.rank, !!(c.pu && c.pu.t3 && c.pu.t3.passed), c.ms.some(m => m[0] === 'senior'), Object.keys(c.tr).filter(k => ['t3', 'm19', 'm18', 'm20', 'mys'].includes(k)).length, c.xp, (WORK_BANDS[c.tier].filter(b => c.xp >= b[0]).pop() || [])[1]]; })")
    check(c[0][:4] == [3, 'senior', True, True] and c[1][4] == 5 and c[1][6] == 'trusted', f"s5: the Day 16 and 21 presets, a Senior Officer (Trusted by Day 21): {c}")
    check(not pg.errors, f's5: errors {pg.errors[:3]}')
    ctx.close()
    print(f"  s5: Power safety's arrow (ask, appointment {asked}), the Tier 3 rows on Day 14, Senior Officer presets {c}")

with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    for name, part in (('off', part_off), ('walk', part_walk), ('look', part_look), ('s5', part_s5)):
        if ONLY and name not in ONLY: continue
        try: part(b)
        except Exception as e: fail(f'{name}: stopped: {str(e)[:300]}')
    b.close()

print('DEV ARROW CHECK OK' if ok else 'DEV ARROW CHECK FAILED')
sys.exit(0 if ok else 1)
