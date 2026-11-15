# Starship Cadet: the safety nets check (FR1, the Fable code review; plans/review-fable-code.md section A)
# Each part makes a copy of the build with one review switch on (flip(), which fails unless exactly one line changed; a
# switch already on in the build is used as it is) and proves the fix with a planted fault. Where it can, the same fault
# is planted in a copy with the switch off first, to show the fault bites without the fix.
#   loop    A1 LOOP_GUARD_ON   one bad frame: the game carries on; every frame bad: the card comes up, once
#   keep    A2 SAVE_KEEP_ON    a save cut short, and one from an unknown version: kept under -bad, the player told, the
#                              Saves app offers it and can throw it away; a good save is left alone
#   tell    A3 SAVE_TELL_ON    storage refuses: the player is told once, the Saves app says so, Download hands over the
#                              game as it is now; storage back: told again; one failing save handler: the rest is saved
#   lib     A4 LIB_SAY_ON      three.js can't be fetched: the title says so
#   sleep   A5 SLEEP_SAFE_ON   an error in the night's catch-up: the fade lifts, you wake
#   load    A6 LOAD_SAFE_ON    four damaged saves load and play an hour
#   memo    A7 EVON_MEMO_ON    eventsOn gives the same answers, switch off and on, flags changed and all
#   walls   A8 WALLS_STILL_ON  standing still nothing is sent again; a wall that moves is sent
#   tab     A12 SAVE_TAB_ON    another tab further on: this one stops saving and says so; one that is behind: saved over
#   hint    A9 TEX_READ_ON     the game loads with it (its pictures are cadet_test's to judge, with the switch on)
#   quiet   R2_QUIET_ON        (review update 2, piece F) errors that come and go: no card, each kind logged once and
#                              kept in a list; every frame bad for 10 real seconds: the card, once; it goes when frames
#                              come good; a hidden tab's gap is not a freeze; R2_FREEZE_CARD false: never a card
# Setup and environment as for cadet_test.py (CADET_WORK, CADET_CHROME).
# Run:  python3 robust_check.py BUILD.html [part ...]   Good is ROBUST CHECK OK (exit 0); a failure exits 1. About 4 minutes.
import sys, os, re, json, pathlib, time
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright

ok = True
def check(cond, msg):
    global ok
    print(('ok   ' if cond else 'FAIL ') + msg)
    if not cond: ok = False
    return cond

GAME = sys.argv[1]; ONLY = set(sys.argv[2:]); SRC = pathlib.Path(GAME).read_text(); RUN = f'_robust_{os.getpid()}_'
__import__('atexit').register(lambda: [f.unlink(missing_ok=True) for f in (WORK / 'test').glob(RUN + '*')])
LIB = 'const LIB_SAY_ON = '
def build(tag, on=(), off=()):                           # a copy with these switches on (and these off), hooked for the check
    s = SRC
    for n in on:
        if re.search(r'\bconst ' + n + r' = true;', s): continue
        s = flip(s, n, True)
    for n in off:
        if re.search(r'\bconst ' + n + r' = false;', s): continue
        s = flip(s, n, False)
    p = WORK / 'test' / (RUN + tag + '.html'); p.write_text(instrument(s)); return p
ARGS = ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist']

class Tab:                                               # one fresh browser (its own storage), saving on unless q says otherwise
    def __init__(self, pw, path, q='?debug', plant=None, before=None, wait=True):
        self.errors = []
        self.b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=ARGS)
        self.page = self.b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
        self.page.on('pageerror', lambda e: self.errors.append(str(e)[:200]))
        self.page.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
        self.page.add_init_script(INIT); self.page.add_init_script('window.cadetPopupsNow = true')   # the game's own test hook: a pop-up shows at once instead of waiting its turn
        if plant: self.page.add_init_script("if (!sessionStorage.getItem('rc')) { sessionStorage.setItem('rc', '1'); const P = %s; for (const k in P) localStorage.setItem(k, P[k]); }" % json.dumps(plant))
        if before: self.page.add_init_script(before)
        self.url = 'file://' + str(path) + q
        self.page.goto(self.url, timeout=180000)
        if wait:
            try: self.page.wait_for_function('window.__sc !== undefined', timeout=120000)
            except Exception: pass
        self.up = self.page.evaluate('window.__sc !== undefined')
        if self.up: self.ev(SKIP_SWITCH); self.ev("(() => { const o = toast; window.__said = [document.getElementById('tt').textContent + ' | ' + document.getElementById('tx').textContent]; toast = (a, b, c) => { window.__said.push(a + ' | ' + b); return o(a, b, c); }; })()")   # every pop-up is noted, so a check never depends on which one is on screen (the game says other things too)
    def ev(self, src): return self.page.evaluate('s => window.__sc(s)', src)
    def step(self, n, safe=False):
        try: self.page.evaluate(f'window.__skip = true; window.__step({n}, {1000 / 30}); window.__skip = false')
        except Exception as e:
            if not safe: raise
    def toast(self): return self.page.evaluate("window.__said.join(' || ')")   # every pop-up since the page loaded, or since clear()
    def clear(self): self.page.evaluate('window.__said = []')
    def store(self, k): return self.page.evaluate('k => localStorage.getItem(k)', k)
    def close(self): self.b.close()

def good_save(pw, path):                                 # a real Day 10 save from this build, and its key
    t = Tab(pw, path); t.ev("if (typeof introOn === 'function' && introOn()) introSkip()"); t.step(30); t.ev('skipTo(9 * 1440 + 600)'); t.step(30); t.ev('saveGame()')
    key = t.ev('SAVE_KEY'); s = t.store(key); t.close(); return key, s
ARRIVED = {'starship-cadet-arrived': '1'}

QUIET_OFF = ['R2_QUIET_ON'] if 'const R2_QUIET_ON = ' in SRC else []   # piece F changes when the card comes: the loop part is A1 without it
def part_loop(pw):
    PLANT_ONE = "(() => { const u = crowd.update.bind(crowd); let n = 0; crowd.update = (a, b) => { if (n++ === 0) throw new Error('robust_check: one bad frame'); return u(a, b); }; })()"
    PLANT_ALL = "crowd.update = () => { throw new Error('robust_check: every frame bad'); }"
    off = Tab(pw, build('loop_off', off=['LOOP_GUARD_ON']), '?nosave&debug'); off.step(30); off.ev(PLANT_ONE); m0 = off.ev('shipNow()'); off.step(1, safe=True); off.step(60, safe=True)
    check(off.ev('shipNow()') == m0, 'loop, switch off: one bad frame stops the game (the fault bites)'); off.close()
    t = Tab(pw, build('loop_on', on=['LOOP_GUARD_ON'], off=QUIET_OFF), '?nosave&debug'); t.step(30); t.ev(PLANT_ONE); m0 = t.ev('shipNow()'); t.step(61)
    check(t.ev('shipNow()') > m0 + .5, f"loop, on: after one bad frame the game carries on (ship minute {m0:.2f} -> {t.ev('shipNow()'):.2f})")
    check(t.page.evaluate("!document.getElementById('loopCard')"), 'loop, on: no card for one bad frame')
    t.ev(PLANT_ALL); t.step(18); check(t.page.evaluate("!document.getElementById('loopCard')"), 'loop, on: 19 bad frames among the last 120 (the one, then 18 in a row): no card yet')
    t.step(30); card = t.page.evaluate("(() => { const c = document.querySelectorAll('#loopCard'); return c.length + ' | ' + (c[0] ? c[0].textContent : ''); })()")
    check(card.startswith('1 | ') and 'Something went wrong' in card and 'Reload' in card and 'saved' not in card, f'loop, on: every frame bad: one card, in plain words, and with saving off it does not say "saved" ({card!r})')
    t.close()
    t = Tab(pw, build('loop_on', on=['LOOP_GUARD_ON'], off=QUIET_OFF), '?nosave&debug'); t.step(30)
    t.ev("(() => { const u = crowd.update.bind(crowd); let n = 0; crowd.update = (a, b) => { if (n++ % 2 === 0) throw new Error('robust_check: every other frame bad'); return u(a, b); }; })()")
    t.step(30); none = t.page.evaluate("!document.getElementById('loopCard')"); t.step(40)
    check(none and t.page.evaluate("!!document.getElementById('loopCard')"), 'loop, on: every other frame bad: no card after 15 bad frames, the card once 20 of the last 120 were bad'); t.close()
    key, good = good_save(pw, build('loop_on', on=['LOOP_GUARD_ON'], off=QUIET_OFF))
    t = Tab(pw, build('loop_on', on=['LOOP_GUARD_ON'], off=QUIET_OFF), plant={key: good, **ARRIVED}); t.step(30); t.ev(PLANT_ALL); t.step(30)
    check(t.page.evaluate("document.activeElement && document.activeElement.textContent") == 'Reload', 'loop, on: the card\'s Reload button has the focus')
    card = t.page.evaluate("(document.getElementById('loopCard') || {}).textContent || ''"); check('saved up to Day 10, 10:00' in card, f'loop, on, a game with a save: the card names the save that is really in storage ({card!r})')
    t.page.evaluate("k => localStorage.removeItem(k)", key); check('no save yet' in t.ev('loopCardLine()'), 'loop, on, nothing in storage: the card says there is no save'); t.close()

def part_keep(pw):
    p = build('keep_on', on=['SAVE_KEEP_ON']); key, good = good_save(pw, p); bad_key = key + '-bad'
    for name, bad in (('cut short', good[:len(good) // 2]), ('from an unknown version', good.replace('"v":2', '"v":3', 1))):
        t = Tab(pw, p, plant={key: bad, **ARRIVED}); t.step(60)
        check(t.up and not t.errors, f'keep, {name}: the game starts (errors {t.errors[:1]})')
        check(t.store(bad_key) == bad, f'keep, {name}: the old save is kept under {bad_key}, text for text')
        check("couldn't be opened" in t.toast(), f'keep, {name}: the player is told ({t.toast()[:70]!r})')
        t.ev("if (typeof introOn === 'function' && introOn()) introSkip()"); t.ev('skipTo(shipNow() + 61)'); t.step(5)
        check(t.store(bad_key) == bad, f'keep, {name}: still kept after an hour of play (the new game has saved itself)')
        view = json.dumps(t.ev('slotsView()'))
        check('Download the old save' in view and "couldn't be opened" in view, f'keep, {name}: the Saves app offers the old save')
        if name == 'cut short':
            t.ev("slotsAct('baddel')"); check(t.store(bad_key) == bad and "can't be brought back" in json.dumps(t.ev('slotsView()')), 'keep: Throw it away asks first, and nothing is gone yet')
            t.ev("slotsAct('keep')"); check(t.store(bad_key) == bad and "can't be brought back" not in json.dumps(t.ev('slotsView()')), 'keep: Keep it changes nothing')
            t.ev("slotsAct('baddel')"); t.ev("slotsAct('baddelgo')"); check(t.store(bad_key) is None and 'Download the old save' not in json.dumps(t.ev('slotsView()')), 'keep: asked and answered, Throw it away removes the copy and the offer')
        t.close()
    t = Tab(pw, p, plant={key: good, **ARRIVED}); t.step(30)
    check(t.ev('SHIP.time.day') == 10 and t.store(bad_key) is None and 'Welcome back' in t.toast(), 'keep: a good save loads as always, nothing kept aside'); t.close()
    # a second unreadable save while an earlier copy is kept (RV37): the first stays, the later one is kept beside it
    first, second = good[:len(good) // 2], good[:len(good) // 3]
    t = Tab(pw, p, plant={key: second, bad_key: first, **ARRIVED}); t.step(60); view = json.dumps(t.ev('slotsView()'))
    check(t.store(bad_key) == first and t.store(bad_key + '-2') == second, 'keep, a second unreadable save: the first copy stays and the later one is kept beside it (-bad-2)')
    check("couldn't be opened" in t.toast() and 'Download the later one' in view and 'Download the old save' in view, 'keep, a second one: the player is told, and the Saves app offers both')
    t.ev("slotsAct('baddel')"); t.ev("slotsAct('baddelgo')"); check(t.store(bad_key) is None and t.store(bad_key + '-2') is None, 'keep: Throw it away (asked and answered) removes both'); t.close()
    t = Tab(pw, p, plant={key: first, **ARRIVED}, before=REFUSE + ' window.__refuse = true;'); t.step(60)
    check(t.store(bad_key) is None and 'no room' in t.toast() and 'is kept' not in t.toast(), f'keep, no room in storage for the copy: the player is not told it was kept ({t.toast()[:90]!r})'); t.close()
    t = Tab(pw, build('keep_off', off=['SAVE_KEEP_ON']), plant={key: good[:len(good) // 2], **ARRIVED}); t.step(30)
    check(t.store(bad_key) is None, 'keep, switch off: nothing is kept (the game as before)'); t.close()

REFUSE = "window.__refuse = false; (() => { const s = Storage.prototype.setItem; Storage.prototype.setItem = function (k, v) { if (window.__refuse && this === localStorage) { const e = new Error('robust_check: storage refuses'); e.name = 'QuotaExceededError'; throw e; } return s.call(this, k, v); }; })();"
def part_tell(pw):
    p = build('tell_on', on=['SAVE_TELL_ON']); key, good = good_save(pw, p)
    t = Tab(pw, p, plant={key: good, **ARRIVED}, before=REFUSE); t.step(30)
    check(t.ev('saveGame()') is True and t.ev('SAVE_ST.fail') == 0, 'tell: a save that works answers true')
    t.page.evaluate('window.__refuse = true'); t.ev('skipTo(shipNow() + 125)'); t.step(5)
    check(t.ev('saveGame()') is False and t.ev('SAVE_ST.fail') >= 1, 'tell: storage refuses: saveGame answers false and counts it')
    check('Not saving' in t.toast(), f'tell: the player is told ({t.toast()[:60]!r})')
    t.clear(); t.ev('saveGame()'); t.step(5); check('Not saving' not in t.toast(), 'tell: told once, not at every failed save')
    check("isn't being saved" in json.dumps(t.ev('slotsView()')), 'tell: the Saves app says the game isn\'t being saved')
    live = t.ev('slotText()'); now = t.ev('SHIP.time.min')
    check(isinstance(live, str) and abs(json.loads(live)['time']['min'] - now) < 1 and json.loads(t.store(key))['time']['min'] != json.loads(live)['time']['min'], 'tell: Download my save hands over the game as it is now, not the old one in storage')
    t.page.evaluate('window.__refuse = false'); check(t.ev('saveGame()') is True, 'tell: storage back: the save is written'); t.step(5)
    check('Saving again' in t.toast() and "isn't being saved" not in json.dumps(t.ev('slotsView()')), 'tell: and the player is told it is saving again')
    # a save handler fails (RV37, lead 52): a failed save. Nothing is written over the last whole save, the player is told
    before = t.store(key); t.clear(); t.ev("window.__h = SAVE_EXTRA[6]; SAVE_EXTRA[6] = s => { s.player.halfMade = 1; s.alsoHalf = 2; throw new Error('robust_check: a save handler fails after writing inside the save'); }")
    t.ev('skipTo(shipNow() + 61)'); t.step(5); r = t.ev('saveGame()')
    check(r is False and t.store(key) == before, 'tell: a save handler fails: saveGame answers false and the last whole save stays in storage, untouched')
    check('Not saving' in t.toast() and "isn't being saved" in json.dumps(t.ev('slotsView()')), 'tell: and the player is told, on screen and in the Saves app')
    t.clear(); t.ev('SAVE_EXTRA[6] = window.__h'); r = t.ev('saveGame()'); t.step(5); s2 = json.loads(t.store(key))
    check(r is True and 'halfMade' not in s2['player'] and 'alsoHalf' not in s2 and 'Saving again' in t.toast(), 'tell: the handler works again: a whole save is written (nothing half made in it) and the player is told')
    t.close()
    # the same at the first save of a sitting (RV37's probe: a Day 10 save loaded, a handler fails at once)
    t = Tab(pw, p, plant={key: good, **ARRIVED}); t.step(30); t.ev("SAVE_EXTRA[0] = () => { throw new Error('robust_check: fails at the first save'); }"); t.ev('skipTo(shipNow() + 61)'); t.step(5)
    check(t.ev('saveGame()') is False and t.store(key) == good and 'Not saving' in t.toast(), 'tell: a handler failing at the first save after a load: the loaded save stays whole in storage, the player is told'); t.close()
    t = Tab(pw, build('tell_off', off=['SAVE_TELL_ON', 'SAVE_TAB_ON']), plant={key: good, **ARRIVED}, before=REFUSE); t.step(30); t.page.evaluate('window.__refuse = true'); t.ev('skipTo(shipNow() + 61)'); t.step(5)
    check(t.ev('saveGame()') is None and 'Not saving' not in t.toast(), 'tell, switch off: nothing is said (the game as before)'); t.close()

def part_lib(pw):
    for tag, on in (('lib_off', False), ('lib_on', True)):
        s = SRC; i = s.index(LIB); cur = s[i + len(LIB):].startswith('true')
        if cur != on:
            n = s.count(LIB + ('true' if cur else 'false') + ';'); assert n == 1, f'{n} LIB_SAY_ON lines'
            s = s.replace(LIB + ('true' if cur else 'false') + ';', LIB + ('true' if on else 'false') + ';')
        p = WORK / 'test' / (RUN + tag + '.html'); p.write_text(s)
        b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=ARGS); page = b.new_page(viewport={'width': 390, 'height': 844})
        page.route(re.compile(r'.*three\.min\.js'), lambda r: r.abort()); page.goto('file://' + str(p) + '?title', timeout=120000); page.wait_for_timeout(1500)
        line = page.evaluate("(() => { const t = document.getElementById('title'); return (t && !t.hidden ? 'shown' : 'hidden') + ' | ' + document.getElementById('tiLine').textContent + ' | menu ' + (document.getElementById('tiMenu').hidden ? 'hidden' : 'shown'); })()")
        if on:
            check(line.startswith('shown') and "COULDN'T LOAD" in line and 'menu hidden' in line, f'lib, on: three.js blocked: the title says so ({line!r})')
            page.screenshot(path='robust_check_lib.png')
        else: check("COULDN'T LOAD" not in line, f'lib, switch off: the title as before ({line!r})')
        b.close()

def part_sleep(pw):
    PLANT = "SIM_ADVANCE.push(() => { throw new Error('robust_check: the night fails'); })"
    for tag, on in (('sleep_off', False), ('sleep_on', True)):
        t = Tab(pw, build(tag, on=['SLEEP_SAFE_ON'] if on else [], off=[] if on else ['SLEEP_SAFE_ON']), '?nosave&debug'); t.step(30); t.ev('skipTo(1440 + 21.5 * 60)'); t.step(10); t.ev(PLANT)
        t.ev('sleepGo(360)'); t.page.wait_for_timeout(2600); t.step(5, safe=True)
        st = t.ev("({ fade: fadeEl.style.opacity, sleeping, min: Math.floor(SHIP.time.min), day: SHIP.time.day })")
        if on: check(str(st['fade']) == '0' and st['sleeping'] is False and st['day'] == 3 and st['min'] >= 360, f'sleep, on: the night\'s catch-up fails: the fade lifts and you wake at the alarm ({st})')
        else: check(str(st['fade']) == '1' and st['sleeping'] is True, f'sleep, switch off: the screen stays black (the fault bites) ({st})')
        t.close()

def part_load(pw):
    on = build('load_on', on=['LOAD_SAFE_ON']); off = build('load_off', off=['LOAD_SAFE_ON']); key, good = good_save(pw, on)
    def dmg(f):
        s = json.loads(good); f(s); return json.dumps(s)
    def no_book(s): s['social']['stories']['cs'].pop('book', None)
    def garden(s): s['galley']['garden']['beds'].append([99, 1, 1]); s['galley']['cold']['produce'] = [[99, 2, 3], 'junk']; s['galley']['garden']['crates'].append({'at': 5, 'items': [[77, 1]], 'id': None})
    def noteq(s): s['social'].setdefault('noteq', []).insert(0, [s['time']['day'] * 1440 - 1440 + s['time']['min'] - 10, 'tradition', None])   # [when, kind, data]: its data gone
    def ahead(s): s['time']['day'] = 36
    base = json.loads(good)
    cases = [('the day ahead of the machines\' clock', ahead)]
    if isinstance(base.get('social', {}).get('stories', {}).get('cs'), dict): cases.append(('the stories without their book', no_book))
    else: print('note load: this save has no social.stories.cs: that case is skipped')
    if isinstance(base.get('galley', {}).get('garden'), dict): cases.append(('junk in the garden and the cold store', garden))
    else: print('note load: this save has no galley.garden: that case is skipped')
    cases.append(('a waiting note with no data', noteq))
    check(len(cases) == 4, 'load: all four damaged saves could be made from this build\'s save')
    for name, f in cases:
        bad = dmg(f)
        o = Tab(pw, off, plant={key: bad, **ARRIVED}); bit = not o.up
        if o.up:
            try: o.step(30); m = o.ev('shipNow()'); o.ev('skipTo(shipNow() + 125)'); o.step(30); bit = bool(o.errors) or o.ev('shipNow()') <= m + 125
            except Exception: bit = True
        o.close(); print(f"note load, switch off, {name}: {'the game fails (the fault bites)' if bit else 'no failure seen with the switch off'}")
        t = Tab(pw, on, plant={key: bad, **ARRIVED}); good_run = t.up
        if t.up:
            try: t.step(30); m = t.ev('shipNow()'); t.ev('skipTo(shipNow() + 125)'); t.step(60); good_run = not t.errors and t.ev('shipNow()') > m + 125
            except Exception as e: good_run = False; t.errors.append(str(e)[:160])
        check(good_run, f'load, on, {name}: the game starts and plays two hours on (errors {t.errors[:1]})'); t.close()
    t = Tab(pw, on, plant={key: good, **ARRIVED}); t.step(30); t.ev('saveGame()'); a = json.loads(t.store(key)); b = json.loads(good)
    check(a.get('galley', {}).get('garden') == b.get('galley', {}).get('garden') and a['galley']['cold'].get('produce') == b['galley']['cold'].get('produce'), 'load, on: a sound save keeps its garden and cold store as they were'); t.close()

def part_memo(pw):
    JS = "(() => { const out = []; const ids = d => eventsOn(d).map(e => e.id + '@' + e.from + '-' + e.to).join(','); for (let d = 1; d <= 45; d++) out.push(ids(d)); const fl = [...new Set(SHIP_TRADITIONS.flatMap(e => [e.flag, e.unflag]).filter(Boolean))]; for (const f of fl) { flagSet(f); out.push(f + ':' + EV_ARR); for (let d = 1; d <= 20; d++) out.push(ids(d)); } for (const f of fl) { flagSet(f, null); out.push(EV_ARR); out.push(ids(9)); } return { n: out.length, flags: fl.length, text: JSON.stringify(out) }; })()"
    res = []
    for tag, on in (('memo_off', False), ('memo_on', True)):
        t = Tab(pw, build(tag, on=['EVON_MEMO_ON'] if on else [], off=[] if on else ['EVON_MEMO_ON']), '?nosave&debug'); t.step(30); t.ev('skipTo(1440 + 600)'); t.step(10)
        try: res.append(t.ev(JS))
        except Exception as e: res.append({'n': 0, 'flags': 0, 'text': 'error ' + str(e)[:200]})
        if on: check(t.ev('EVON_L !== null && EVON_L.length') == res[-1]['flags'] or res[-1]['flags'] == 0 or t.ev('EVON_L.length') > 0, 'memo, on: the kept list is in use')
        t.close()
    check(res[0]['n'] > 45 and res[0]['text'] == res[1]['text'], f"memo: eventsOn's answers over 45 days, and through {res[0]['flags']} flags set and cleared, are the same with the switch off and on ({res[0]['n']} answers)")

def part_walls(pw):
    HOOK = "(() => { const gl = renderer.getContext(); window.__up = 0; const o = gl.bufferSubData.bind(gl); gl.bufferSubData = (...a) => { window.__up += (a[2] && a[2].byteLength) || 0; return o(...a); }; })()"
    got = {}
    for tag, on in (('walls_off', False), ('walls_on', True)):
        t = Tab(pw, build(tag, on=['WALLS_STILL_ON'] if on else [], off=[] if on else ['WALLS_STILL_ON']), '?nosave&debug&crew'); t.ev('skipTo(1440 + 3 * 60)'); t.step(200)
        t.page.evaluate('window.__skip = false; window.__step(40, 33.3)'); t.ev(HOOK); t.page.evaluate('window.__up = 0; window.__step(20, 33.3)'); still = t.page.evaluate('window.__up') / 20
        t.ev("document.getElementById('walls').click()"); t.page.evaluate('window.__up = 0; window.__step(5, 33.3)'); moving = t.page.evaluate('window.__up') / 5
        got[on] = (still, moving); t.close()
    check(got[True][0] < got[False][0] * .6, f'walls: standing still, bytes of positions sent a frame: {got[False][0]:.0f} with the switch off, {got[True][0]:.0f} on')
    check(got[True][1] > got[True][0], f'walls, on: walls coming down are sent ({got[True][1]:.0f} bytes a frame while they move)')

def part_tab(pw):
    p = build('tab_on', on=['SAVE_TAB_ON']); key, good = good_save(pw, p)
    def at(day): s = json.loads(good); s['time']['day'] = day; return json.dumps(s)
    t = Tab(pw, p, plant={key: good, **ARRIVED}); t.step(30)
    check(t.ev('saveGame()') is True, 'tab: alone, the game saves as always')
    t.page.evaluate('([k, v]) => localStorage.setItem(k, v)', [key, at(8)]); r = t.ev('saveGame()')
    check(r is True and json.loads(t.store(key))['time']['day'] == 10, 'tab: another tab that is behind (Day 8): this one saves over it')
    later = at(12); t.page.evaluate('([k, v]) => localStorage.setItem(k, v)', [key, later]); r = t.ev('saveGame()'); t.step(5)
    check(r is False and t.store(key) == later, 'tab: another tab further on (Day 12): this one does not save over it')
    check('another tab' in t.toast(), f'tab: and says so ({t.toast()[:60]!r})')
    t.ev('skipTo(shipNow() + 3 * 1440)'); t.step(5); check(t.ev('saveGame()') is False and t.store(key) == later and 'another tab' in json.dumps(t.ev('slotsView()')), 'tab: it stays stopped (even once past that day), and the Saves app says why')
    live = json.loads(t.ev('slotText()')); check(live['time']['day'] == t.ev('SHIP.time.day') == 13 and abs(live['time']['min'] - t.ev('SHIP.time.min')) < 1, 'tab: Download my save in the stopped tab hands over this tab\'s game as it is now (Day 13), and storage is left alone') ; check(t.store(key) == later, 'tab: (storage still the other tab\'s)')
    t.close()
    t = Tab(pw, build('tab_off', off=['SAVE_TAB_ON', 'SAVE_TELL_ON']), plant={key: good, **ARRIVED}); t.step(30); t.page.evaluate('([k, v]) => localStorage.setItem(k, v)', [key, at(12)]); t.ev('saveGame()')
    check(json.loads(t.store(key))['time']['day'] == 10, 'tab, switch off: the newer save is written over (the game as before)'); t.close()

def part_hint(pw):
    t = Tab(pw, build('hint_on', on=['TEX_READ_ON']), '?nosave&debug'); t.step(30)
    check(t.up and not t.errors and t.ev('renderer.info.memory.textures') > 0, f'hint, on: the game loads and draws (errors {t.errors[:1]})'); t.close()

def part_quiet(pw):
    if 'const R2_QUIET_ON = ' not in SRC: print('skipped: R2_QUIET_ON is not in this build'); return
    ODD = "(() => { const u = crowd.update.bind(crowd); let n = 0; crowd.update = (a, b) => { if (n++ % 2 === 0) throw new Error('robust_check: every other frame bad'); return u(a, b); }; })()"
    ALL = "(() => { window.__u = crowd.update; crowd.update = () => { throw new Error('robust_check: every frame bad'); }; })()"
    BACK = "crowd.update = window.__u"
    card = lambda t: t.page.evaluate("document.querySelectorAll('#loopCard').length")
    def tab(path):                                       # Tab.step's frame is 1/30 of a (virtual) real second: 300 frames are ten seconds
        t = Tab(pw, path, '?nosave&debug'); t.cons = []
        t.page.on('console', lambda m: m.type == 'error' and t.cons.append(m.text[:200])); t.step(30); return t
    on = build('quiet_on', on=['LOOP_GUARD_ON', 'R2_QUIET_ON'])
    # 1. an error that comes and goes (every other frame, for 20 real seconds: A1's rule would show its card after 40 frames)
    t = tab(on); t.ev(ODD); m0 = t.ev('shipNow()'); t.step(600); log = t.ev('r2Errors()')
    check(card(t) == 0, 'quiet: every other frame bad for 20 real seconds: no card')
    check(t.ev('shipNow()') > m0 + 2, f"quiet: the game carries on meanwhile (ship minute {m0:.2f} -> {t.ev('shipNow()'):.2f})")
    check(len(log) == 1 and log[0]['n'] == 300 and 'every other frame bad' in log[0]['kind'] and log[0]['day'] is not None, f'quiet: the list holds the one kind, counted 300 times, with its ship day ({log})')
    check(len([c for c in t.cons if 'every other frame bad' in c]) == 1, f'quiet: that kind is written to the console once, not 300 times ({len(t.cons)} console errors)')
    # 2. a second kind is its own row and its own one console line; many kinds: R2_KINDS rows and one row for the rest
    t.ev("(() => { const u = crowd.update; let n = 0; crowd.update = (a, b) => { if (n++ < 4) throw new TypeError('robust_check: a second kind'); return u(a, b); }; })()"); t.step(10); log = t.ev('r2Errors()')
    check(len(log) == 2 and log[1]['n'] == 4 and log[1]['kind'].startswith('TypeError') and len([c for c in t.cons if 'a second kind' in c]) == 1, f'quiet: a second kind has its own row and one console line ({[(r["kind"][:40], r["n"]) for r in log]})')
    t.ev("(() => { const u = crowd.update; let n = 0; crowd.update = (a, b) => { if (n < 20) throw new Error('robust_check: kind number ' + n++); return u(a, b); }; })()"); t.step(30); log = t.ev('r2Errors()'); kinds = t.ev('R2_KINDS')
    check(len(log) == kinds + 1 and log[-1]['kind'] == 'Other errors' and sum(r['n'] for r in log if 'kind number' in r['kind'] or r['kind'] == 'Other errors') == 20, f'quiet: 20 more kinds: the list stops at {kinds} kinds and one row for the rest ({len(log)} rows)')
    check(card(t) == 0 and not t.errors, f'quiet: still no card, and nothing reached the page as an uncaught error ({t.errors[:1]})'); t.close()
    # 3. a true freeze: every frame bad. No card at 9 real seconds, one card after 10; it names no save with saving off
    t = tab(on); t.ev(ALL); t.step(270); check(card(t) == 0, 'quiet: every frame bad for 9 real seconds: no card yet')
    t.step(40); txt = t.page.evaluate("(document.getElementById('loopCard') || {}).textContent || ''")
    check(card(t) == 1 and 'Something went wrong' in txt and 'Reload' in txt and 'saved' not in txt, f'quiet: every frame bad for 10 real seconds: the card, in plain words ({txt!r})')
    t.step(300); check(card(t) == 1 and len(t.ev('r2Errors()')) == 1 and len(t.cons) == 1, 'quiet: ten seconds more of it: still one card, one row, one console line')
    # the frames come good again: the card goes and the game carries on; a second freeze brings it back
    t.ev(BACK); m0 = t.ev('shipNow()'); t.step(30); still = card(t); t.step(60)
    check(still == 1 and card(t) == 0 and t.ev('shipNow()') > m0 + .5, 'quiet: frames good again: the card stays a second, then goes, and the game carries on')
    t.ev(ALL); t.step(320); check(card(t) == 1, 'quiet: a second freeze brings the card again'); t.close()
    # 4. bad frames with good ones between never add up to a freeze; nor does the gap of a hidden tab
    t = tab(on); t.ev("(() => { const u = crowd.update.bind(crowd); let n = 0; crowd.update = (a, b) => { if (n++ % 100 !== 99) throw new Error('robust_check: 99 bad, one good'); return u(a, b); }; })()"); t.step(900)
    check(card(t) == 0, 'quiet: 99 bad frames then one good, for 30 real seconds: no card (not every frame)'); t.close()
    t = tab(on); t.ev(ALL); t.step(150); t.page.evaluate('window.__step(1, 60000)'); t.step(30)
    check(card(t) == 0, 'quiet: five seconds of bad frames, a minute hidden, a second more: no card (the gap is not a freeze)')
    t.step(150); check(card(t) == 1, 'quiet: and the card once the bad frames themselves reach ten seconds'); t.close()
    # 5. the freeze card switched off (R2_FREEZE_CARD): never a card, the log only
    src = SRC.replace('const R2_FREEZE_CARD = true,', 'const R2_FREEZE_CARD = false,')
    if check(src != SRC and src.count('const R2_FREEZE_CARD = false,') == 1, 'quiet: R2_FREEZE_CARD is one constant in the build'):
        for n in ('LOOP_GUARD_ON', 'R2_QUIET_ON'):
            if not re.search(r'\bconst ' + n + r' = true;', src): src = flip(src, n, True)
        p = WORK / 'test' / (RUN + 'quiet_nocard.html'); p.write_text(instrument(src))
        t = tab(p); t.ev(ALL); t.step(600); log = t.ev('r2Errors()')
        check(card(t) == 0 and len(log) == 1 and log[0]['n'] == 600, f'quiet, R2_FREEZE_CARD false: every frame bad for 20 real seconds: no card, the list has it ({log[0]["n"] if log else None} times)')
        t.ev(BACK); m0 = t.ev('shipNow()'); t.step(60); check(t.ev('shipNow()') > m0 + .5, 'quiet, R2_FREEZE_CARD false: and the game carries on when the frames come good'); t.close()
    # 6. with no fault nothing is logged (piece F off, LOOP_GUARD_ON alone, is A1 as before: the loop part)
    t = tab(on); t.step(120); check(t.ev('r2Errors()') == [] and card(t) == 0 and not t.cons, f'quiet: a healthy game: nothing logged, no card ({t.cons[:1]})'); t.close()

PARTS = [('loop', part_loop), ('keep', part_keep), ('tell', part_tell), ('lib', part_lib), ('sleep', part_sleep), ('load', part_load), ('memo', part_memo), ('walls', part_walls), ('tab', part_tab), ('hint', part_hint), ('quiet', part_quiet)]
if __name__ == '__main__':
    t0 = time.time()
    with sync_playwright() as pw:
        for name, f in PARTS:
            if ONLY and name not in ONLY: continue
            print(f'-- {name}')
            try: f(pw)
            except SystemExit: raise
            except Exception as e: check(False, f'{name}: the part itself failed: {str(e)[:300]}')
    print(('ROBUST CHECK OK' if ok else 'ROBUST CHECK FAILED') + f' ({time.time() - t0:.0f} s)')
    sys.exit(0 if ok else 1)
