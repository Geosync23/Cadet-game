# PR7: Dev mode D5 (Traditions) through the real buttons at phone size, with reloads; the real save untouched.
# python3 dm_trad_probe.py BUILD.html OUTDIR
import os, sys, json, re, pathlib
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("a, shots = run(")[0])
GAME = sys.argv[1]; OUT = pathlib.Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
TMP = WORK / 'test' / '_dm_trad_probe.html'; TMP.write_text(instrument(pathlib.Path(GAME).read_text()))
BAD = []
def check(c, m):
    print(('  ok  ' if c else '  BAD ') + m, flush=True)
    if not c: BAD.append(m)
class Page:
    def __init__(self, ctx, suffix):
        self.errors = []; self.page = ctx.new_page()
        self.page.on('pageerror', lambda e: self.errors.append(f'pageerror: {e}'))
        self.page.on('console', lambda m: m.type == 'error' and self.errors.append(f'error: {m.text}'))
        self.page.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
        self.page.add_init_script(INIT); self.page.goto('file://' + str(TMP) + suffix); self.ready()
    def ready(self):
        self.page.wait_for_function('window.__sc !== undefined', timeout=90000)
        self.ev("(() => { const rr = renderer.render.bind(renderer); window.__draw = false; renderer.render = (s, c) => { if (window.__draw) rr(s, c); }; })()")
        self.step(20)
    def ev(self, src): return self.page.evaluate('s => window.__sc(s)', src)
    def step(self, n, dt=1000 / 30): self.page.evaluate(f'window.__step({n}, {dt})')
    def shot(self, p): self.page.evaluate('window.__draw = true'); self.step(1); self.page.screenshot(path=str(p)); self.page.evaluate('window.__draw = false')
    def tap(self, text, exact=True):
        loc = self.page.locator('#dmSheet button', has_text=re.compile('^' + re.escape(text) + '$' if exact else re.escape(text)))
        n = loc.count()
        if not n: return False
        loc.first.click(); self.step(2); return True
    def fade(self):                      # devmodeDo: a 280 ms real-time fade, then the action
        self.page.wait_for_timeout(700); self.step(10)
    def sign(self):                      # the arrival's manifest, if it's up (as devmode_check does)
        if self.page.locator('text=Sign and go aboard').count():
            self.page.fill('form input', 'Ada'); self.page.click('text=Sign and go aboard'); self.step(30)
    def reload_ready(self):
        self.page.wait_for_function('window.__sc !== undefined', timeout=90000); self.ready()
def store(pg): return pg.page.evaluate('() => Object.fromEntries(Object.keys(localStorage).map(k => [k, localStorage.getItem(k)]))')
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    for w, h in ((390, 844), (360, 780)):
        ctx = b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=1)
        # a real game first, to protect
        pg = Page(ctx, '?debug'); pg.sign(); pg.ev('newGameStart(false); introSkip(); saveGame()'); real = {k: v for k, v in store(pg).items() if not k.endswith('-dev') and 'dev-' not in k}; pg.page.close()
        pg = Page(ctx, '#dev'); pg.sign()
        pg.ev('newGameStart(false); introSkip()'); pg.step(10)
        pg.ev("devmodeRun('Clock', () => devmodeSkipTo(2 * 1440 + 17 * 60))"); pg.step(5)
        base = pg.ev("JSON.stringify(eventsOn(3).map(e => [e.id, e.from, e.to]))")
        pg.ev('devmodeOpen(true); DM_UI.tab = "trad"; DM_UI.trad = null; devmodeDraw()'); pg.step(2)
        pg.page.fill('#dmSheet input.dmFind', 'quiz'); pg.step(2)
        check(pg.tap('Quiz night'), f'{w}: Quiz night in the list after a search')
        pg.shot(OUT / f'd5_{w}_card.png')
        check(pg.tap('In 20 minutes'), f'{w}: In 20 minutes button'); pg.fade()
        msg = pg.ev('DM_UI.msg'); print('  msg:', msg)
        e = pg.ev("(eventsOn(3).find(e => e.id === 'quiz' && e.dev) || null)")
        check(e is not None and e['from'] == 17 * 60 + 20, f'{w}: the quiz started today at 17:20 ({e and e["from"]})')
        check('going' in (msg or ''), f'{w}: the panel says how many are going: {msg}')
        pg.shot(OUT / f'd5_{w}_started.png')
        # reload: still started, listed on the tab
        pg.page.reload(); pg.reload_ready()
        pg.ev('devmodeOpen(true); DM_UI.tab = "trad"; DM_UI.trad = null; devmodeDraw()'); pg.step(2)
        txt = pg.ev("document.querySelector('#dmSheet').innerText")
        check('Started by Dev mode' in txt and 'Quiz night' in txt, f'{w}: after a reload the tab lists the started quiz')
        check(pg.tap('Take me there'), f'{w}: Take me there'); pg.fade(); pg.step(30)
        room = pg.ev("(r => r && ROOMS[r] ? ROOMS[r].name : null)(roomAt(...player.here()))"); print('  there:', room, 'deck', pg.ev('deckDef.num'))
        check(room is not None and re.search('lounge', room or '', re.I), f'{w}: Take me there put you in {room}')
        pg.ev("devmodeRun('Clock', () => devmodeSkipTo(2 * 1440 + 17 * 60 + 40))"); pg.step(60)
        there = pg.ev("schedPeople().filter(p => { const w = whereIs(p, shipNow()); return w && w.tag && evTagId(w.tag) === 'quiz'; }).length")
        onDeck = pg.ev("DECK_CREW.filter(a => { const w = whereIs(a.p, shipNow()); return w && w.tag && evTagId(w.tag) === 'quiz'; }).length")
        check(there >= 3 and onDeck >= 3, f'{w}: at 17:40 {there} at the quiz by plan, {onDeck} of them on the deck')
        pg.shot(OUT / f'd5_{w}_quiz1740.png')
        # Stop it through the button: back to the calendar (the clock moved, so compare the list for Day 3)
        pg.ev('devmodeOpen(true); DM_UI.tab = "trad"; DM_UI.trad = null; devmodeDraw()'); pg.step(2)
        check(pg.tap('Stop it'), f'{w}: Stop it'); pg.fade()
        check(pg.ev("JSON.stringify(eventsOn(3).map(e => [e.id, e.from, e.to]))") == base, f'{w}: Day 3 back to its calendar after Stop it')
        # Undo (Quick tab): the quiz back
        pg.ev('DM_UI.tab = "quick"; devmodeDraw()'); pg.step(2)
        with pg.page.expect_navigation(timeout=90000):
            pg.ev('devmodeUndo()')
        pg.reload_ready()
        check(pg.ev("devmodeState().tr.some(r => r.id === 'quiz' && r.day === 3)"), f'{w}: Undo of Stop it brings the quiz back')
        # a birthday: whose by taps
        pg.ev('devmodeOpen(true); DM_UI.tab = "trad"; DM_UI.trad = "birthday"; DM_UI.who = null; devmodeDraw()'); pg.step(2)
        pg.tap('Tomorrow'); pg.fade(); m = pg.ev('DM_UI.msg'); check('whose' in (m or '').lower(), f'{w}: a birthday without whose refused: {m}')
        names = pg.ev("schedPeople().filter(p => !p.player && aboard(p, 4)).sort((a, b) => a.name.localeCompare(b.name)).slice(0, 2).map(p => p.name)")
        for n in names: pg.tap(n)
        pg.shot(OUT / f'd5_{w}_whose.png')
        pg.tap('Tomorrow'); pg.fade(); m = pg.ev('DM_UI.msg'); print('  birthday:', m)
        hon = pg.ev("(e => e ? e.names : null)(eventsOn(4).find(e => e.id === 'birthday' && e.dev))")
        check(hon and all(n in hon for n in names), f'{w}: the birthday is for {names}: {hon}')
        # the real save untouched
        st = store(pg); now_real = {k: v for k, v in st.items() if k in real}
        check(now_real == real, f'{w}: the real game\'s keys untouched')
        check(not pg.errors, f'{w}: errors {pg.errors[:3]}')
        ctx.close()
    b.close()
print('DM TRAD PROBE ' + ('OK' if not BAD else 'FAILED: ' + '; '.join(BAD)))
