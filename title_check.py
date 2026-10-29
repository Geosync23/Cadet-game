#!/usr/bin/env python3
"""title_check.py: the title screen (section 30, option B, the crew terminal; plans/title-screen-plan.md).

    CADET_CHROME=/opt/pw-browsers/chromium python3 title_check.py [GAME.html]     (about 2-3 minutes)

Makes a copy with the switch on (TITLE_ON and the page's TITLE_EARLY made true by text) and opens it with ?title at
phone size (390 x 844), in real time (the title's hand-over is on real timers). Checks:
  the switch as it is in the build;
  New game and Start over (0.99.2): the terminal stays up until the shuttle's manifest is drawn (or the deck, for Monday), so
  the old deck never shows in between (a per-frame record); for a player who has arrived before, the device's question
  shows on top of the terminal;
  the gate (0.99.1, the user's pick): asleep, only "> TAP TO WAKE THE TERMINAL"; a tap, a key or a pad press wakes it
  (and asks for the title's music) without choosing anything, before three.js too and in landscape;
  the page's first script paints the title while three.js is still on its way (10%), and a Continue chosen then waits
  ("BOARDING ...") and goes in once the game has loaded;
  the loading bar reaches 100 (READY); the ship is held while it's up (the clock and FREEZE), nothing is written to
  localStorage (a pagehide too), and the save is written as it hands over if one was asked for;
  no save: no Continue, NEW GAME first, New game goes to the arrival (the manifest);
  a save: the Continue line (day, weekday, time, deck), the phosphor from the save (amber), Continue goes in with the
  ship's day and minute unchanged and the welcome back; New game asks (Keep playing, Escape and B keep it; Start over
  starts a new game);
  Settings and Saves open the device on top and come back to the title; a device not yet issued says so; Start over
  inside Settings leaves the title;
  a pretend controller: the D-pad moves the highlight, A chooses, B keeps, Start is Continue (not Pause);
  reduced motion (the plain fade), landscape (two columns), the three phosphors' ink;
  hidden under ?debug, ?nosave and #dev without title, and with #dev even with it;
  draw calls with the title up the same as just after it.
Good is TITLE CHECK OK. Exits 1 on any FAIL.
"""
import os, re, sys, json, pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent
GAME = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ROOT / 'starship-cadet.html').resolve()
WORK = pathlib.Path(os.environ.get('CADET_WORK', '/tmp/cadet-work'))
THREE = (WORK / 'three/package/build/three.min.js').read_text()
TEST = WORK / 'test'; TEST.mkdir(parents=True, exist_ok=True)
HOOK = "window.__sc = src => eval(src);\n"
ARGS = ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist']
# a pretend controller (controller_check's way, cut down): one standard pad, window.__pad(button, value)
PAD = r"""(() => { const p = { id: 'Xbox Wireless Controller (STANDARD GAMEPAD Vendor: 045e Product: 0b13)', index: 0, connected: true, mapping: 'standard',
  timestamp: 0, axes: [0, 0, 0, 0], buttons: Array.from({ length: 17 }, () => ({ pressed: false, touched: false, value: 0 })) };
  const copy = () => ({ ...p, axes: p.axes.slice(), buttons: p.buttons.map(b => ({ ...b })) });
  Object.defineProperty(Navigator.prototype, 'getGamepads', { configurable: true, value: () => [window.__padOn ? copy() : null, null, null, null] });
  window.__pad = (k, v) => { if (!window.__padOn) { window.__padOn = true; const e = new Event('gamepadconnected'); Object.defineProperty(e, 'gamepad', { value: copy() }); dispatchEvent(e); }
    p.buttons[k] = { pressed: v > .5, touched: v > 0, value: v }; p.timestamp = performance.now(); return true; }; })();"""
BTN = dict(A=0, B=1, MENU=9, UP=12, DOWN=13)

ok = True
def check(cond, msg):
    global ok
    print(('ok   ' if cond else 'FAIL ') + msg)
    if not cond: ok = False
    return cond

src = GAME.read_text()
m_on, m_early = re.search(r'const TITLE_ON = (true|false);', src), re.search(r'const TITLE_EARLY = (true|false);', src)
if not (m_on and m_early): print('FAIL no title screen switches in this build (TITLE_ON, TITLE_EARLY)'); sys.exit(1)
def copy(text, tag):
    i = text.rfind('})();'); f = TEST / f'_title_{os.getpid()}_{tag}.html'; f.write_text(text[:i] + HOOK + text[i:]); return f
ON = copy(src.replace('const TITLE_ON = false;', 'const TITLE_ON = true;').replace('const TITLE_EARLY = false;', 'const TITLE_EARLY = true;'), 'on')
AS_IS = copy(src, 'asis')
SWITCH = m_on.group(1) == 'true'

with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=ARGS)
    ERR = []
    def page(w=390, h=844, motion='no-preference', pad=False, hold=None):
        ctx = br.new_context(viewport={'width': w, 'height': h}, reduced_motion=motion)
        pg = ctx.new_page()
        pg.on('pageerror', lambda e: ERR.append(str(e)))
        def three(r):
            if hold is not None and hold[0]: hold.append(r)
            else: r.fulfill(body=THREE, content_type='application/javascript')
        pg.route(re.compile(r'.*three\.min\.js'), three)
        if pad: pg.add_init_script(PAD)
        return pg
    def go(pg, f, q, wait=True):
        pg.goto('file://' + str(f) + q, wait_until='load' if wait else 'commit', timeout=90000)
        if wait: pg.wait_for_function('window.__sc !== undefined', timeout=90000)
    ev = lambda pg, s: pg.evaluate('s => window.__sc(s)', s)
    js = lambda pg, s: pg.evaluate(s)
    up = lambda pg: js(pg, "!document.getElementById('title').hidden")
    ready = lambda pg: pg.wait_for_function("document.getElementById('tiLine').textContent === 'READY'", timeout=20000)
    clock = lambda pg: ev(pg, '[SHIP.time.day, SHIP.time.min]')
    def until(pg, cond, ms=20000):                         # a busy machine draws slowly: wait for the state, not a fixed time
        try: pg.wait_for_function('s => window.__sc(s)', arg=cond, timeout=ms); return True
        except Exception: return False
    gone = "document.getElementById('title').hidden && !TITLE.on"
    asleep = lambda pg: js(pg, "document.getElementById('title').classList.contains('asleep')")
    shown = lambda pg, sel: js(pg, f"(e => !!(e && e.getClientRects().length))(document.querySelector('{sel}'))")
    # (0.99.2) every frame after New game: is the screen covered, by the terminal (T), the terminal switching off (O) over
    # the manifest, or the manifest (M)? A frame with neither (the terminal gone or going and no manifest) shows the old deck
    FLASH = """(() => { window.__fr = []; const f = () => { const t = document.getElementById('title'), m = typeof INTRO_UI !== 'undefined' && !!INTRO_UI.manifest;
      window.__fr.push((t && !t.hidden ? (t.classList.contains('off') ? 'O' : 'T') : '-') + (m ? 'M' : '-')); if (window.__fr.length < 300) requestAnimationFrame(f); }; requestAnimationFrame(f); })()"""
    def flash_start(pg): ev(pg, FLASH)
    def flash_count(pg):
        fr = ev(pg, 'window.__fr'); return sum(1 for x in fr if x[0] in '-O' and x[1] == '-'), ''.join(x[0] for x in fr[:40])
    def wake(pg):                                          # the gate (0.99.1): one tap on the wake line
        pg.click('#tiWake'); return not asleep(pg)

    # ---- the switch as the build has it ----
    pg = page(); go(pg, AS_IS, '?title'); pg.wait_for_timeout(800)
    if not SWITCH:
        check(not up(pg) and not ev(pg, 'FREEZE.frozen'), 'switch off (as built): no title and nothing held, even with ?title')
    else:
        check(up(pg), 'switch on (as built): the title shows with ?title')
    pg.context.close()

    # ---- the saves the parts use: a Monday (device yours) and the arrival (device not yet issued) ----
    pg = page(); go(pg, ON, ''); pg.wait_for_timeout(500)
    check(not up(pg), 'under webdriver without ?title: no title (every other check)')
    ARR = js(pg, "localStorage.getItem('starship-cadet-save')")   # the arrival, at the manifest: the device not yet yours
    ev(pg, 'newGameStart(false); introSkip(); SHIP.device.settings.phosphor = "amber"; SHIP.time.day = 12; SHIP.time.min = 460; saveGame()')
    MON = js(pg, "localStorage.getItem('starship-cadet-save')")
    for q in ['?debug', '?nosave', '#dev', '#dev.title']:
        go(pg, ON, q); pg.wait_for_timeout(300); check(not up(pg), f'{q}: no title')
    pg.context.close()
    def with_save(pg, save):
        go(pg, ON, '?nosave'); js(pg, "localStorage.clear()")
        if save: pg.evaluate("s => localStorage.setItem('starship-cadet-save', s)", save)

    # ---- no save ----
    pg = page(); with_save(pg, None); go(pg, ON, '?title')
    check(up(pg) and js(pg, "document.getElementById('tiGo').hidden"), 'no save: the title, and no Continue')
    check(asleep(pg) and shown(pg, '#tiWake') and not shown(pg, '#tiMenu') and not shown(pg, '.tiBig') and not shown(pg, '.tiLoad'), 'the gate: asleep, only the wake line shows')
    check(not ev(pg, 'SND.titleOn'), 'the gate: no title music before the wake')
    pg.keyboard.press('Enter')
    check(not asleep(pg) and shown(pg, '#tiMenu') and shown(pg, '.tiBig') and up(pg) and ev(pg, 'SND.titleOn'), 'the gate: a key wakes it (the music on), the menu shows, nothing chosen')
    check(js(pg, "document.querySelector('#title button.on').id") == 'tiNew', 'no save: NEW GAME highlighted first')
    ready(pg); c0 = clock(pg); pg.wait_for_timeout(1500)
    js(pg, "dispatchEvent(new Event('pagehide')); document.dispatchEvent(new Event('visibilitychange'))")
    check(clock(pg) == c0 and ev(pg, 'FREEZE.frozen && titleHold()'), f'no save: the ship held while it is up {c0}')
    check(js(pg, 'localStorage.length') == 0, 'no save: nothing written to localStorage while it is up (pagehide too)')
    flash_start(pg); pg.click('#tiNew'); until(pg, gone + " && !!document.querySelector('form input') && !FREEZE.frozen")
    fc = flash_count(pg); check(fc[0] == 0, f'no save, New game: the old deck never shows before the manifest ({fc[0]} frames; {fc[1]})')
    check(not up(pg) and not ev(pg, 'titleHold()'), 'no save: New game closes the title and lets the ship go')
    sv = (json.loads(js(pg, "localStorage.getItem('starship-cadet-save')") or 'null') or {}).get('time')
    check(js(pg, "document.body.textContent.includes('PASSENGER MANIFEST')") and sv == {'day': 0, 'min': 1035}, f'no save: New game is the arrival (the manifest), saved at Day 0 17:15 ({sv})')
    pg.context.close()

    # ---- a save: the Continue line, the phosphor, Continue unchanged ----
    pg = page(); with_save(pg, MON); go(pg, ON, '?title'); ready(pg); wake(pg)
    check(js(pg, "document.getElementById('tiWhere').textContent") == 'DAY 12 · FRI 07:40 · DECK 4', 'a save: the Continue line ' + js(pg, "document.getElementById('tiWhere').textContent"))
    check(js(pg, "document.querySelector('#title button.on').id") == 'tiGo', 'a save: CONTINUE highlighted first')
    check(js(pg, "getComputedStyle(document.getElementById('tiFound')).color") == 'rgb(255, 179, 71)', 'a save: the amber phosphor from the save')
    pg.wait_for_timeout(1200); js(pg, "dispatchEvent(new Event('pagehide'))")
    check(js(pg, "localStorage.getItem('starship-cadet-save')") == MON and clock(pg) == [12, 460], 'a save: held and nothing saved while up')
    calls_up = ev(pg, 'renderer.info.render.calls')   # the same frozen moment with the title out of the page's way
    js(pg, "document.getElementById('title').style.display = 'none'"); pg.wait_for_timeout(400); calls_off = ev(pg, 'renderer.info.render.calls')
    js(pg, "document.getElementById('title').style.display = ''")
    check(calls_up == calls_off, f'draw calls with the title up {calls_up}, the same moment without it {calls_off}')
    pg.keyboard.press('Enter'); until(pg, gone + ' && !FREEZE.frozen')
    t = clock(pg)
    check(not up(pg) and t[0] == 12 and 460 <= t[1] < 461, f'Continue (Enter): in, at the saved day and minute {t}')
    check('Welcome back' in js(pg, "document.getElementById('tx').textContent"), 'Continue: the welcome back')
    check(json.loads(js(pg, "localStorage.getItem('starship-cadet-save')"))['time']['day'] == 12, 'Continue: the save written as it handed over (a pagehide asked)')
    pg.context.close()

    # ---- New game with a save: the question ----
    pg = page(); with_save(pg, MON); go(pg, ON, '?title'); ready(pg); wake(pg)
    pg.keyboard.press('Tab'); pg.keyboard.press('Tab'); check(js(pg, "document.activeElement.id") == 'tiSaves', 'Tab moves along the title\'s lines only')
    pg.click('#tiNew'); check(js(pg, "!document.getElementById('tiAsk').hidden && document.getElementById('tiMenu').hidden"), 'New game asks: ' + js(pg, "document.querySelector('#tiAsk p').textContent"))
    check(js(pg, "document.querySelector('#title button.on').id") == 'tiKeep', 'the question: KEEP PLAYING highlighted first')
    pg.keyboard.press('Escape'); check(js(pg, "document.getElementById('tiAsk').hidden") and up(pg), 'Escape is Keep playing')
    pg.click('#tiNew'); pg.click('#tiKeep'); check(js(pg, "document.getElementById('tiAsk').hidden") and up(pg) and clock(pg) == [12, 460], 'Keep playing: back to the menu, nothing changed')
    pg.click('#tiNew'); flash_start(pg); pg.click('#tiOver'); until(pg, gone + " && (!document.getElementById('devDlg').hidden || SHIP.time.day !== 12)")
    fc = flash_count(pg); check(fc[0] == 0, f'Start over: the old deck never shows before the manifest ({fc[0]} frames; {fc[1]})')
    dlg = js(pg, "(d => d && !d.hidden ? d.textContent : '')(document.getElementById('devDlg'))")
    check(not up(pg) and ('How do you want to start' in dlg or clock(pg) != [12, 460]), 'Start over: the title closes and New game starts (' + (dlg[:40] or str(clock(pg))) + ')')
    pg.context.close()

    # ---- Start over for a player who has arrived before: the device asks how, on top of the terminal (0.99.2) ----
    for choice, want in [('Skip to Monday morning', 'monday'), ('Arrive by shuttle', 'arrive')]:
        pg = page(); with_save(pg, MON); js(pg, "localStorage.setItem('starship-cadet-arrived', '1')"); go(pg, ON, '?title'); ready(pg); wake(pg)
        pg.click('#tiNew'); flash_start(pg); pg.click('#tiOver'); until(pg, "!document.getElementById('devDlg').hidden")
        z = js(pg, "+getComputedStyle(document.getElementById('devDlg')).zIndex")
        check(up(pg) and z > 70, f'arrived before, Start over: "How do you want to start?" on top of the terminal (z {z}), the terminal still up')
        pg.click(f"#devDlg button:has-text('{choice}')")
        if want == 'monday':
            t = clock(pg) if until(pg, gone) else [0, 0]; check(t[0] == 1 and 360 <= t[1] < 362, f'{choice}: the terminal goes onto Monday 06:00 {t}')
        else:
            until(pg, gone + " && !!document.querySelector('form input')")
            fc = flash_count(pg); check(not up(pg) and fc[0] == 0, f'{choice}: the manifest, and the old deck never shows ({fc[0]} frames; {fc[1]})')
        pg.context.close()

    # ---- Settings and Saves on top, and back ----
    pg = page(); with_save(pg, MON); go(pg, ON, '?title'); ready(pg); wake(pg)
    for btn, app in [('#tiSet', 'settings'), ('#tiSaves', 'saves')]:
        pg.click(btn); pg.wait_for_timeout(300)
        z = js(pg, "+getComputedStyle(document.getElementById('device')).zIndex")
        check(ev(pg, 'DEV.open && DEV.app') == app and z > 70, f'{app}: the device opens on top of the title (z {z})')
        ev(pg, 'deviceClose()'); pg.wait_for_timeout(200)
        check(up(pg) and ev(pg, 'TITLE.on && !TITLE.away && FREEZE.frozen') and clock(pg) == [12, 460], f'{app}: closing the device comes back to the title')
    pg.click('#tiSet'); pg.wait_for_timeout(200); ev(pg, "devNewAct('newgame'); devNewAct('newgo')"); until(pg, gone)
    check(not up(pg), 'Settings > New game > Start over: the title goes')
    pg.context.close()
    pg = page(); with_save(pg, ARR); go(pg, ON, '?title'); ready(pg); wake(pg)
    pg.click('#tiSet'); pg.wait_for_timeout(200)
    st = ev(pg, "[DEV.open, document.getElementById('tiLine').textContent, TITLE.on, SHIP.intro && SHIP.intro.step]")
    check(not st[0] and 'ISSUED' in st[1] and st[2], f'the arrival (device not yet yours): Settings says so, the title stays {st}')
    pg.context.close()

    # ---- a pretend controller ----
    pg = page(pad=True); with_save(pg, MON); go(pg, ON, '?title'); ready(pg)
    def press(k):
        frames = 'new Promise(r => requestAnimationFrame(() => requestAnimationFrame(() => requestAnimationFrame(r))))'   # the pad is read once a frame
        js(pg, f'__pad({BTN[k]}, 1)'); pg.evaluate(frames); js(pg, f'__pad({BTN[k]}, 0)'); pg.evaluate(frames); pg.wait_for_timeout(100)
    press('DOWN'); press('DOWN')   # (the first press only says hello; the second wakes the terminal)
    check(not asleep(pg) and up(pg), 'pad: a press wakes the gate, nothing chosen')
    press('DOWN')
    check(js(pg, "document.activeElement && document.activeElement.id") in ('tiNew', 'tiSaves') and js(pg, "document.querySelector('#title button.on') === document.activeElement"), 'pad: the D-pad moves the highlight (' + str(js(pg, "document.activeElement.id")) + ')')
    for _ in range(4): press('UP')
    press('DOWN'); check(js(pg, "document.activeElement.id") == 'tiNew', 'pad: on NEW GAME')
    press('A'); check(js(pg, "!document.getElementById('tiAsk').hidden"), 'pad: A chooses (the question)')
    press('B'); check(js(pg, "document.getElementById('tiAsk').hidden") and up(pg), 'pad: B is Keep playing')
    press('MENU'); until(pg, gone)
    check(not up(pg) and not ev(pg, 'PAUSE.on') and clock(pg)[0] == 12, 'pad: Start is Continue, not Pause')
    pg.context.close()

    # ---- the early paint, while three.js is on its way; Continue chosen then ----
    held = [False]; pg = page(hold=held); with_save(pg, MON)
    held[0] = True; pg.on('dialog', lambda d: d.dismiss())
    go(pg, ON, '?title', wait=False); pg.wait_for_function("document.getElementById('tiLine') && !document.getElementById('title').hidden", timeout=20000)
    check(len(held) >= 2 and js(pg, "document.getElementById('tiLine').textContent").endswith('10%') and js(pg, "!document.getElementById('tiGo').hidden"), 'before three.js: the title painted (' + js(pg, "document.getElementById('tiLine').textContent") + '), Continue there')
    check(asleep(pg) and not shown(pg, '#tiGo'), 'before three.js: asleep, the wake line only')
    pg.click('#tiWake'); check(not asleep(pg) and shown(pg, '#tiGo') and js(pg, "document.getElementById('tiLine').textContent").endswith('10%'), 'before three.js: a tap wakes it, nothing chosen')
    pg.click('#tiGo'); check(js(pg, "document.getElementById('tiLine').textContent") == 'BOARDING ...', 'before three.js: Continue waits (BOARDING ...)')
    for r in held[1:]: r.fulfill(body=THREE, content_type='application/javascript')
    pg.wait_for_function('window.__sc !== undefined', timeout=90000)
    try: pg.wait_for_function("document.getElementById('title').hidden", timeout=15000)
    except Exception: pass
    check(not up(pg) and clock(pg)[0] == 12, 'before three.js: the Continue went in once loaded')
    check(not ev(pg, 'SND.titleOn'), 'before three.js: the music asked for at load, and off again after Continue')
    pg.context.close()

    # ---- reduced motion, landscape, the phosphors ----
    pg = page(motion='reduce'); with_save(pg, MON); go(pg, ON, '?title'); ready(pg); wake(pg)
    check(js(pg, "getComputedStyle(document.querySelector('#title .tiCrt'), '::before').animationName") == 'none', 'reduced motion: no roll or flicker')
    pg.click('#tiGo'); pg.wait_for_timeout(60)
    check(js(pg, "getComputedStyle(document.getElementById('title')).animationName") == 'tifade', 'reduced motion: the plain fade')
    pg.context.close()
    pg = page(844, 390); with_save(pg, MON); go(pg, ON, '?title'); ready(pg)
    check(asleep(pg) and shown(pg, '#tiWake') and not shown(pg, '#tiMenu'), 'landscape: the gate too'); wake(pg)
    lm, lt = js(pg, "document.getElementById('tiMenu').getBoundingClientRect().left"), js(pg, "document.querySelector('.tiBig').getBoundingClientRect().left")
    check(lm > lt + 200, f'landscape: two columns (title at {lt:.0f}, menu at {lm:.0f})')
    for ph, ink in [('cyan', 'rgb(111, 240, 220)'), ('green', 'rgb(93, 255, 138)'), ('amber', 'rgb(255, 179, 71)')]:
        js(pg, f"document.getElementById('title').dataset.ph = '{ph}'")
        check(js(pg, "getComputedStyle(document.getElementById('tiNew')).color") == ink, f'phosphor {ph}: the ink {ink}')
    pg.context.close()

    check(not ERR, 'no page errors' + ('' if not ERR else ': ' + ' | '.join(ERR[:4])))
    br.close()
for f in (ON, AS_IS): f.unlink(missing_ok=True)
print('TITLE CHECK OK' if ok else 'TITLE CHECK FAILED')
sys.exit(0 if ok else 1)
