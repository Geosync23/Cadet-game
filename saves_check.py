# Starship Cadet: save slots check (0.93.2, FX27; section 13's slots and section 19's Saves app)
# Opens the game in a phone-sized browser (390 x 844) with real saving and checks:
#   off:     the build with SAVE_SLOTS_ON false: one save under its old name, no Saves app, no slot keys, no save.at
#   migrate: a save written by the build with slots off is Slot 1, byte for byte, until the game saves it again
#   switch:  New game in empty Slot 2 (Skip to Monday) reloads into a Monday game there, Slot 1 untouched; Play Slot 1
#            goes back to it (the day it was saved on); New game in Slot 3 by shuttle starts the arrival there
#   delete:  the slot being played can't be deleted; another asks first (Keep it changes nothing), then goes
#   download: outside claude.ai a file named starship-cadet-dayN-HHMM.json whose text is the save; on a claude.ai page the
#            downloads capability gets the same name and text; with no capability, Copy save as text is offered
#   load:    a bad file (not JSON, a JSON that isn't a save, v 3) says so and changes nothing; a good one through the file
#            picker into an empty slot plays it; over a used slot it asks, Keep it changes nothing, Replace it plays it
#   nosave:  ?nosave never shows the app or reads the slot; Dev (#dev) slots carry "-dev"; Dev mode's Copy my real game
#            copies the Playtest slot being played and changes no Playtest slot
#   shot:    the Saves page at phone size (saves_check_page.png)
#   shut:    (S5-4) a shutdown booking saved before 22:00 reads back unsettled; after 22:00, settled (P5_STEP5 on in a copy)
# Setup and environment as for cadet_test.py (CADET_WORK, CADET_CHROME).
# Run:  python3 saves_check.py BUILD.html [part ...]   Good is SAVES CHECK OK (exit 0); a failure exits 1.
import sys, os, re, json, pathlib
exec(open(__file__.replace('saves_check.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
RUN_ID = f'p{os.getpid()}_'
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
SRC = pathlib.Path(GAME).read_text()
ON_LINE = 'const SAVE_SLOTS_ON = true,'
if ON_LINE not in SRC: sys.exit('saves_check: no SAVE_SLOTS_ON line in the build')
TMP = WORK / 'test' / ('_saves_check_' + RUN_ID + '.html'); TMP.write_text(instrument(SRC))
TMP_OFF = WORK / 'test' / ('_saves_check_off_' + RUN_ID + '.html'); TMP_OFF.write_text(instrument(SRC.replace(ON_LINE, 'const SAVE_SLOTS_ON = false,')))
K1, K2, K3, KS = 'starship-cadet-save', 'starship-cadet-save-2', 'starship-cadet-save-3', 'starship-cadet-save-slot'

class Page:
    def __init__(self, ctx, suffix='', path=TMP):
        self.errors = []; self.path = path
        self.page = ctx.new_page()
        self.page.on('pageerror', lambda e: self.errors.append(f'pageerror: {e}'))
        self.page.on('console', lambda m: m.type == 'error' and self.errors.append(f'error: {m.text}'))
        self.page.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
        self.page.add_init_script(INIT)
        self.go(suffix, path)
    # another build or link in this same tab (as a player opening the new link): never a closed tab and a new one, so
    # the save is never handed between two browser processes (CR4's one-off "old save null" in migrate, 0.93.2 round)
    def go(self, suffix='', path=TMP):
        self.path = path
        self.page.goto(ORIGIN + path.name + suffix, timeout=120000); self.ready()   # a busy machine (straight after check_fast) can take over the default 30 s to load the game
    def ready(self):
        self.page.wait_for_function('window.__sc !== undefined', timeout=90000)
        self.page.add_style_tag(content='*,*::before,*::after{transition:none!important;animation:none!important}')
        self.ev("(() => { const rr = renderer.render.bind(renderer); window.__draw = false; renderer.render = (s, c) => { if (window.__draw) rr(s, c); }; })()")
        self.step(20)
    def ev(self, src):
        return self.page.evaluate('s => window.__sc(s)', src)
    def ev_reload(self, src):                         # an action that reloads the page itself
        with self.page.expect_navigation(timeout=90000):
            self.page.evaluate('s => window.__sc(s)', src)
        self.ready()
    def step(self, n, dt=1000 / 30):
        self.page.evaluate(f'window.__step({n}, {dt})')
    def sign(self):
        if self.page.locator('text=Sign and go aboard').count():
            self.page.fill('form input', 'Ada'); self.page.click('text=Sign and go aboard'); self.step(30)
    def store(self):
        return self.page.evaluate('() => Object.fromEntries(Object.keys(localStorage).map(k => [k, localStorage.getItem(k)]))')
    def close(self):
        check(not self.errors, f'page errors: {self.errors[:3]}')
        self.page.close()

# the game is served from a made-up web address (ORIGIN), as players get it from a web page, never opened as a file: a
# page opened from a file:// address was now and then given a fresh, empty storage of its own after a change of page
# (the old save still there, seen from another page; CR4's one-off migrate FAIL in the 0.93.2 round, reproduced here
# 2 in 30, and the same with the slots-off build on both sides). Pages of one web address always share their storage.
ORIGIN = 'http://saves-check.test/'
def new_ctx(b, **kw):
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, **kw)
    ctx.route(re.compile(r'^http://saves-check\.test/[^?#]*'), lambda r: r.fulfill(path=str(WORK / 'test' / r.request.url.split('?')[0].split('#')[0][len(ORIGIN):]), content_type='text/html')
              if r.request.url[len(ORIGIN):].split('?')[0].split('#')[0].endswith('.html') else r.continue_())
    return ctx

def day_of(text):
    return json.loads(text)['time']['day'] if text else None

def monday_game(pg, day):                             # a game on Monday-week `day` at 09:30, saved
    pg.sign(); pg.ev(f'introSkip(); setShipNow(({day} - 1) * 1440 + 570); updateClock(); saveGame()'); pg.step(5)

def part_off(b):
    ctx = new_ctx(b)
    pg = Page(ctx, '', TMP_OFF); monday_game(pg, 3)
    st = pg.store()
    check(pg.ev('SAVE_SLOTS_ON') is False and pg.ev('SAVE_KEY') == K1, 'off: the save name moved with slots off')
    check(pg.ev("!DEVICE_APPS.has('saves')"), 'off: the Saves app is there with slots off')
    check(set(st) <= {K1, 'starship-cadet-arrived'}, f'off: storage holds more than the one save: {sorted(st)}')
    check(K1 in st and 'at' not in json.loads(st[K1]), 'off: no save, or the save carries save.at with slots off')
    print('  off: one save, no app, keys', sorted(st))
    return ctx, pg

def part_migrate(b):
    ctx, pg = part_off(b)
    check(not pg.errors, f'off: page errors: {pg.errors[:3]}')
    pg.page.add_init_script('window.__first = localStorage.getItem("starship-cadet-save"); window.__keys = Object.keys(localStorage)')   # before the game's script
    pg.go('', TMP); old = pg.page.evaluate('window.__first')   # the build with slots on, in the same tab
    if not check(old and 'at' not in json.loads(old), 'migrate: the save left by the build with slots off is not there'):
        print('   storage before the game ran:', pg.page.evaluate('window.__keys'), '| the game loaded:', pg.ev('SAVED ? clockText() : null'), '| storage now:', sorted(pg.store()))
        pg.close(); return ctx
    o = json.loads(old)['time']
    check(pg.ev('SHIP.time.day') == o['day'] and abs(pg.ev('SHIP.time.min') - o['min']) < 5, f'migrate: the old save\'s time did not load ({pg.ev("clockText()")} vs {o})')
    check(pg.ev('SAVE_SLOT') == 1 and pg.ev('SAVE_KEY') == K1, 'migrate: an old save is not Slot 1')
    pg.ev('saveGame()'); st = pg.store()
    check(day_of(st.get(K1)) == day_of(old) and 'at' in json.loads(st[K1]), 'migrate: Slot 1 not saved again with save.at')
    check(KS not in st and K2 not in st and K3 not in st, f'migrate: slot keys written without a slot change: {sorted(st)}')
    pg.close()
    print('  migrate: the old save is Slot 1, day', day_of(old))
    return ctx

def part_switch(b):
    ctx = new_ctx(b)
    pg = Page(ctx); monday_game(pg, 5)
    s1 = pg.store()[K1]
    check(pg.ev('slotNew(2)') is True and pg.ev('!!DEV.choose'), 'switch: New game in Slot 2 did not ask arrive or skip')
    pg.ev_reload('devChosen(1)')
    check(pg.ev('SAVE_SLOT') == 2 and pg.ev('SAVE_KEY') == K2, 'switch: not playing Slot 2 after New game there')
    check(pg.ev('SHIP.time.day') == 1 and abs(pg.ev('SHIP.time.min') - 360) < 5 and pg.ev('!introOn()'), f'switch: Slot 2 is not a Monday 06:00 game: {pg.ev("clockText()")}')
    pg.step(10); pg.ev('saveGame()'); st = pg.store()
    check(day_of(st.get(K1)) == 5, 'switch: Slot 1 changed when Slot 2 began')
    check(day_of(st.get(K2)) == 1 and st.get(KS) == '2' and 'starship-cadet-save-new' not in st, f'switch: Slot 2 not saved, or the slot keys wrong: {sorted(st)}')
    check(pg.ev("slotDelete(2) === false && localStorage.getItem('starship-cadet-save-2') !== null"), 'delete: the slot being played was deleted')
    pg.ev_reload('slotPlay(1)')
    check(pg.ev('SAVE_SLOT') == 1 and pg.ev('SHIP.time.day') == 5 and pg.ev('hhmm(SHIP.time.min)') == '09:30', f'switch: Play Slot 1 did not go back to Day 5 09:30: {pg.ev("clockText()")}')
    # delete: asks first, Keep it, then Delete it
    pg.ev("deviceShow('saves')"); pg.step(2)
    pg.ev("deviceDo({ app: 'saves', do: 'del', arg: 2 })")
    check(pg.page.locator('#devBody >> text=Delete Slot 2?').count() == 1, 'delete: Delete did not ask first')
    pg.ev("deviceDo({ app: 'saves', do: 'keep' })")
    check(pg.page.evaluate('k => localStorage.getItem(k)', K2) is not None, 'delete: Keep it deleted the slot')
    pg.ev("deviceDo({ app: 'saves', do: 'del', arg: 2 })"); pg.ev("deviceDo({ app: 'saves', do: 'delgo', arg: 2 })")
    check(pg.page.evaluate('k => localStorage.getItem(k)', K2) is None and pg.page.evaluate('k => localStorage.getItem(k)', K1) is not None, 'delete: Delete it did not remove Slot 2 alone')
    check(pg.page.locator('#devBody >> text=Empty').count() == 2, 'delete: Slots 2 and 3 do not say Empty')
    pg.ev('deviceClose()')
    # arrive by shuttle in Slot 3
    pg.ev('slotNew(3)'); pg.ev_reload('devChosen(0)')
    check(pg.ev('SAVE_SLOT') == 3 and pg.ev('SHIP.time.day') == 0 and pg.ev('introOn()'), f'switch: New game by shuttle in Slot 3 is not the arrival: {pg.ev("clockText()")}')
    pg.sign(); pg.ev('saveGame()'); st = pg.store()
    check(day_of(st.get(K3)) == 0 and day_of(st.get(K1)) == 5 and K2 not in st, 'switch: the slots are not Day 5, deleted and Day 0')
    pg.close()
    print('  switch and delete: slots 1-3 played, switched, deleted')
    return ctx

def part_download(b):
    ctx = new_ctx(b, accept_downloads=True)
    pg = Page(ctx); monday_game(pg, 12)
    with pg.page.expect_download(timeout=60000) as d:
        pg.ev('slotDownload()')
    dl = d.value; path = dl.path(); text = pathlib.Path(path).read_text()
    check(dl.suggested_filename == 'starship-cadet-day12-0930.json', f'download: the file name is {dl.suggested_filename}')
    check(text == pg.page.evaluate('k => localStorage.getItem(k)', K1), 'download: the file is not the save')
    check(pg.ev('saveOk(JSON.parse(' + json.dumps(text) + '))'), 'download: the file is not a save this build loads')
    # a claude.ai page: the downloads capability
    pg.ev("window.claude = { use: async n => n === 'downloads' ? { save: async r => { window.__dl = r; return { status: 'saved' }; } } : null }")
    pg.page.evaluate('() => window.__sc("slotDownload()")'); pg.page.wait_for_function('window.__dl !== undefined', timeout=60000, polling=100)
    r = pg.page.evaluate('window.__dl')
    check(r['filename'] == 'starship-cadet-day12-0930.json' and r['data'] == pg.page.evaluate('k => localStorage.getItem(k)', K1), 'download: the capability got the wrong name or text')
    pg.ev("window.claude = { use: async () => null }; SLOT_UI.copy = false")
    pg.page.evaluate('() => window.__sc("slotDownload()")'); pg.page.wait_for_function('window.__sc("SLOT_UI.copy")', timeout=60000, polling=100)
    check('Copy save as text' in pg.ev('SLOT_UI.msg'), f'download: no capability, and no copy offered: {pg.ev("SLOT_UI.msg")}')
    pg.ev('delete window.claude')
    pg.close()
    print('  download: file and capability carry the save,', r['filename'])

def part_load(b):
    ctx = new_ctx(b)
    pg = Page(ctx); monday_game(pg, 4)
    good = pg.page.evaluate('k => localStorage.getItem(k)', K1)
    g9 = json.loads(good); g9['time']['day'] = 9; g9 = json.dumps(g9)
    before = pg.store()
    for name, bad in (('not JSON', 'hello'), ('not a save', '{"a":1}'), ('v 3', good.replace('"v":2', '"v":3', 1)), ('no tile', good.replace('"tile":', '"tilex":', 1))):
        pg.ev('slotLoadText(' + json.dumps(bad) + ')')
        check('isn\'t a Starship Cadet save' in pg.ev('SLOT_UI.msg') and not pg.ev('!!DEV.choose'), f'load: a bad file ({name}) was not refused')
    after = pg.store(); after.pop(K1, None); b2 = dict(before); b2.pop(K1, None)
    check(after == b2, 'load: a bad file changed the storage')
    # a good file through the picker, into empty Slot 3
    p9 = WORK / 'test' / f'_saves_day9_{RUN_ID}.json'; p9.write_text(g9)
    pg.ev("deviceShow('saves')"); pg.step(2)
    with pg.page.expect_file_chooser(timeout=60000) as fc:
        pg.page.click('#devBody button:has-text("Load a save file")')
    fc.value.set_files(str(p9))
    pg.page.wait_for_function('window.__sc("!!DEV.choose")', timeout=60000, polling=100)
    pg.ev_reload('devChosen(2)')
    check(pg.ev('SAVE_SLOT') == 3 and pg.ev('SHIP.time.day') == 9, f'load: the file did not play in Slot 3: slot {pg.ev("SAVE_SLOT")}, {pg.ev("clockText()")}')
    check(day_of(pg.page.evaluate('k => localStorage.getItem(k)', K1)) == 4, 'load: Slot 1 changed')
    # over used Slot 1: asks; Keep it changes nothing; Replace it plays it
    g7 = json.loads(good); g7['time']['day'] = 7; g7 = json.dumps(g7)
    pg.ev('slotLoadText(' + json.dumps(g7) + ')'); pg.ev('devChosen(0)')
    check(pg.ev("!!DEV.choose && document.querySelector('#devDlg').textContent.toLowerCase().includes('replace slot 1')"), 'load: over a used slot it did not ask')
    pg.ev('devChosen(1)')
    check(day_of(pg.page.evaluate('k => localStorage.getItem(k)', K1)) == 4 and pg.ev('SAVE_SLOT') == 3, 'load: Keep it changed something')
    pg.ev('slotLoadText(' + json.dumps(g7) + ')'); pg.ev('devChosen(0)')
    pg.ev_reload('devChosen(0)')
    check(pg.ev('SAVE_SLOT') == 1 and pg.ev('SHIP.time.day') == 7, f'load: Replace it did not play the file in Slot 1: {pg.ev("clockText()")}')
    check(day_of(pg.page.evaluate('k => localStorage.getItem(k)', K3)) == 9, 'load: Slot 3 lost its game when Slot 1 was replaced')
    # over the slot being played: replaced, and the old page's last save never wrote over it
    g8 = json.loads(good); g8['time']['day'] = 8; g8 = json.dumps(g8)
    pg.ev('slotLoadText(' + json.dumps(g8) + ')'); pg.ev('devChosen(0)'); pg.ev_reload('devChosen(0)')
    check(pg.ev('SAVE_SLOT') == 1 and pg.ev('SHIP.time.day') == 8, f'load: the file did not replace the game being played: {pg.ev("clockText()")}')
    pg.close()
    print('  load: bad files refused, good ones played in Slots 3 and 1')

def part_nosave(b):
    ctx = new_ctx(b)
    pg = Page(ctx); monday_game(pg, 2); pg.page.evaluate('k => localStorage.setItem(k, "2")', KS)
    pg.go('?nosave')
    check(pg.ev("SAVE_SLOT === 1 && !DEVICE_APPS.has('saves') && SLOT_NEW === null"), 'nosave: the slots or the app are on with ?nosave')
    pg.go('#dev')
    check(pg.ev("SAVE_BASE === 'starship-cadet-save-dev' && slotKey(2) === 'starship-cadet-save-dev-2' && SAVE_KEY === 'starship-cadet-save-dev'"), 'nosave: the Dev slots don\'t carry -dev')
    # Dev mode's Copy my real game copies the Playtest slot being played (Slot 2 here, Day 11), not Slot 1 (Day 2)
    pg.page.evaluate('() => { const s = JSON.parse(localStorage.getItem("starship-cadet-save")); s.time.day = 11; localStorage.setItem("starship-cadet-save-2", JSON.stringify(s)); }')
    real2 = pg.page.evaluate('k => localStorage.getItem(k)', K2)
    pg.ev_reload('devmodeCopyReal()')
    check(pg.ev('DEVMODE && SHIP.time.day') == 11, f'nosave: Copy my real game did not copy Playtest Slot 2: {pg.ev("clockText()")}')
    check(pg.page.evaluate('k => localStorage.getItem(k)', K2) == real2 and day_of(pg.page.evaluate('k => localStorage.getItem(k)', K1)) == 2, 'nosave: Copy my real game changed a Playtest slot')
    pg.close()
    print('  nosave: no slots with ?nosave; Dev slots are -dev')

# promo3 (S5-2, B5): the Senior Officer promotion in a save, with P5_STEP5 on in a copy: saved between the test and the
# result (the record read back, the result still to come the next morning at 08:15), and between the result and the bar
# (a Senior Officer, the bar's occasion still booked for 16:30, given at the ceremony)
P5_SW = "const P5_STEP5 = URL_FLAGS.has('p5s5');"
def part_promo3(b):
    if (P5_SW not in SRC and not re.search(r'^const P5_STEP5 = true;', SRC, re.M)) or 'function puPromote' not in SRC: print('  promo3: not yet (no P5_STEP5 switch line or no Senior Officer promotion in this build)'); return   # (BM19) or already on (0.94.0)
    tmp = WORK / 'test' / ('_saves_check_pu3_' + RUN_ID + '.html'); tmp.write_text(instrument(SRC.replace(P5_SW, 'const P5_STEP5 = true;')))
    ctx = new_ctx(b); pg = Page(ctx, '', tmp); pg.sign()
    pg.ev("""(() => { introSkip(); setShipNow(14 * 1440 + 700); machinesNow(); const W = worksInit(); W.tier = 2; W.rank = 'officer'; W.xp = 60; W.tr.ps = 12; W.tr.t2 = 9;
      const T = puSet(15); T.tries = 1; puPassed(shipNow()); updateClock(); saveGame(); })()""")
    pg.go('', tmp)
    a = pg.ev("(() => ({ day: SHIP.time.day, t3: puT3(), tier: SHIP.works.tier, rd: puResultDay(), next: worksNext() }))()")
    print('  promo3: saved after the test:', a)
    check(a['t3'] and a['t3']['passed'] and a['t3']['day'] == 15 and a['t3']['tries'] == 1 and a['tier'] == 2 and a['rd'] == 16 and 'result' in a['next'].lower(), f'promo3: the passed test did not read back, the result still to come ({a})')
    pg.ev("(() => { for (let t = shipNow(); t <= 15 * 1440 + 520; t += 5) { setShipNow(t); machinesNow(); worksCareerTick(t); } const r = SHIP.occasions.find(x => x.id === 'pu3Result'); if (r && SHIP.works.tier === 2) puPromote(shipNow(), 'met'); updateClock(); saveGame(); })()")
    pg.go('', tmp)
    c = pg.ev("(() => { const r = SHIP.occasions.find(x => x.id === 'pu3Bar'); return { t3: puT3(), tier: SHIP.works.tier, rank: SHIP.works.rank, bar: r ? [hhmm(r.at % 1440), r.status] : null, hooked: !!(MEETING_SCRIPTS['pu3.bar'] && MEETING_SCRIPTS['pu3.bar'].puHooked) }; })()")
    print('  promo3: saved after the result:', c)
    check(c['tier'] == 3 and c['rank'] == 'senior' and c['t3'] and c['t3']['res'] == 16 and not c['t3']['bar'] and c['bar'] == ['16:30', 'asked'] and c['hooked'], f'promo3: a Senior Officer with the bar still booked did not read back ({c})')
    e = pg.ev("(() => { MEETING_SCRIPTS['pu3.bar'].onEnd(true); return [puT3().bar, PLAYER_SPEC.rank]; })()")
    check(e == [16, 2], f'promo3: after the reload the bar is given at its end, a third pip ({e})')
    check(not pg.errors, f'promo3: page errors {pg.errors[:3]}')
    pg.close(); tmp.unlink(missing_ok=True)
LATER = [('promo3', part_promo3)]

def part_shot(b):
    ctx = new_ctx(b)
    pg = Page(ctx); monday_game(pg, 6)
    pg.page.evaluate('k => localStorage.setItem(k, localStorage.getItem("starship-cadet-save").replace(\'"day":6\', \'"day":3\'))', K2)
    pg.ev("deviceShow('saves')"); pg.step(3)
    n = pg.page.locator('#devBody button').count()
    check(n >= 4, f'shot: the Saves page has {n} buttons')
    small = pg.page.evaluate("() => [...document.querySelectorAll('#devBody button')].filter(b => b.getBoundingClientRect().height < 40).length")
    check(small == 0, f'shot: {small} buttons under 40px tall')
    pg.page.evaluate('window.__draw = true'); pg.step(1); pg.page.screenshot(path='saves_check_page.png'); pg.page.evaluate('window.__draw = false')
    pg.close()
    print('  shot: saves_check_page.png')

# (S5-4, B3) shutdowns (24w, P5_M18) in the save: a booking made on Day 18 and saved before 22:00 reads back unsettled
# (the job still waits for its shutdown); played on to 22:00 it settles, and a save after reads back settled, the job
# held, Day 19's plan with the booked rooms closed. Runs on a copy with P5_STEP5 switched on; without the switch line,
# "not yet" (never a pass)
P5_LINE = "const P5_STEP5 = URL_FLAGS.has('p5s5');"
def part_shut(b):
    if (P5_LINE not in SRC and not re.search(r'^const P5_STEP5 = true;', SRC, re.M)) or 'function sdBook' not in SRC: print('  shut: not yet (no P5_STEP5 switch line or no shutdowns in this build)'); return   # (BM19) or already on (0.94.0)
    tmp = WORK / 'test' / ('_saves_check_p5_' + RUN_ID + '.html'); tmp.write_text(instrument(SRC.replace(P5_LINE, 'const P5_STEP5 = true;')))
    ctx = new_ctx(b); pg = Page(ctx, '', tmp); pg.sign()
    j = pg.ev("""(() => { introSkip(); setShipNow(17 * 1440 + 600); machinesNow(); const W = worksInit(); W.tier = 3; W.rank = 'senior'; W.tr.m18 = 18;
      const id = jobReserve('6-junction-1', 18, 600, 43, { tier: 3 }); sdMark(shipNow()); const b = sdBook(id, 840, 'galley', ['3|K'], { warned: ['brennan'], inPerson: ['brennan'] });
      updateClock(); saveGame(); return [id, !!b]; })()""")
    check(j[1], f'shut: the booking was not made ({j})')
    pg.go('', tmp)
    a = pg.ev(f"""(() => {{ const S = SHIP.works && SHIP.works.sd, j = SHIP.jobs.find(x => x.id === {json.dumps(j[0])}); return {{ day: SHIP.time.day, book: S ? S.book.map(b => [b.day, b.at, b.branch, b.keep.join(), b.inPerson.join()]) : null, set: S ? Object.keys(S.set) : null, job: j ? [j.status, !!j.shut, !!j.reserved] : null }}; }})()""")
    print('  shut: saved before 22:00:', a)
    check(a['book'] == [[19, 840, 'galley', '3|K', 'brennan']] and a['set'] == [] and a['job'] == ['waiting', True, True], f'shut: an unsettled booking did not read back as it was ({a})')
    pg.ev("(() => { for (let t = shipNow(); t <= 17 * 1440 + 1325; t += 5) { setShipNow(t); machinesNow(); worksCareerTick(t); } updateClock(); saveGame(); })()")
    pg.go('', tmp)
    c = pg.ev(f"""(() => {{ const S = SHIP.works && SHIP.works.sd, j = SHIP.jobs.find(x => x.id === {json.dumps(j[0])}), L = sdShutList(19); return {{ book: S ? S.book.length : null, set: S && S.set[19] ? S.set[19].map(b => [b.at, b.branch, b.keep.join()]) : null, job: j ? [j.status, !!j.reserved] : null, rooms: L ? [...L[0].rooms] : null }}; }})()""")
    print('  shut: saved after 22:00:', c)
    check(c['book'] == 0 and c['set'] == [[840, 'galley', '3|K']] and c['job'] == ['waiting', True] and c['rooms'] == ['3|M'], f'shut: the settled booking did not read back ({c})')
    pg.close(); tmp.unlink(missing_ok=True)

PARTS = [('migrate', part_migrate), ('switch', part_switch), ('download', part_download), ('load', part_load), ('nosave', part_nosave), ('shot', part_shot), ('shut', part_shut)]
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    for name, f in PARTS + LATER:   # LATER: Step 5's parts (S5-2's promo3)
        if ONLY and name not in ONLY: continue
        try: f(b)
        except Exception as e: fail(f'{name}: stopped: {type(e).__name__}: {e}'); __import__('traceback').print_exc()   # the whole story, for a runner who keeps only the end
    b.close()
print('SAVES CHECK OK' if ok else 'SAVES CHECK FAILED')
sys.exit(0 if ok else 1)
