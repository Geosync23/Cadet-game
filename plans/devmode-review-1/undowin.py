# DR1: patch #6's Undo window with Dev mode merged (scratch merge pe_dev.html): a Dev jump, a save, and an Undo across 09:00
import sys, os, re, json, pathlib
os.environ.setdefault('CADET_CHROME','/opt/pw-browsers/chromium')
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("class Game")[0])
from playwright.sync_api import sync_playwright
tmp = WORK / 'test' / '_dr1_undowin.html'; tmp.write_text(instrument(pathlib.Path(sys.argv[1]).read_text()))
SETUP = r"""(() => { INTRO_BOOT = false; newGameStart(false); introSkip(); TIPS_OFF = true;
  for (let t = shipNow() + 30; t < 8 * 1440 + 8 * 60 + 56; t += 30) skipTo(t); skipTo(8 * 1440 + 8 * 60 + 56);   // Day 9, Tuesday 08:56
  goToDeck(5); clockScreen(); return clockText(); })()"""
STATE = "(() => { const c = SHIP.career, d = SHIP.time.day; return { clock: clockText(), ci: c.ci ? hhmm(c.ci % 1440) : 0, on: c.on === d, sent: flag('shiftSent') === d, undo: !!CLOCK_UNDO, ex: DEVMODE ? devmodeState().ex.slice() : null, clockNotes: simNotes('clock').map(n => n.what + '@' + hhmm(n.t % 1440)), ms: c.ms }; })()"
def page(pw):
    b = pw.chromium.launch(executable_path=os.environ['CADET_CHROME'], args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
    pg = b.new_page(viewport={'width':390,'height':844}); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)[:150]))
    pg.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
    pg.add_init_script(INIT); pg.goto('file://' + str(tmp) + '#dev.clockundo')
    pg.wait_for_function('window.__sc !== undefined', timeout=90000)
    ev = lambda s: pg.evaluate('s => window.__sc(s)', s)
    ev("(() => { renderer.render = () => {}; })()"); pg.evaluate('window.__step(10, 33)')
    print('  start', ev(SETUP)); return b, pg, ev, errs
with sync_playwright() as pw:
    print('A: clock in, then a Dev jump (+3 h) inside the window')
    b, pg, ev, errs = page(pw)
    print('  punch', ev("clockPunch(false)"), ev(STATE))
    ev("(devmodeRun('jump', () => devmodeSkipTo(shipNow() + 180)), 0)"); pg.evaluate('window.__step(3, 33)')
    print('  after jump', ev(STATE), errs[:2]); b.close()
    print('B: clock in, then a save inside the window')
    b, pg, ev, errs = page(pw)
    ev("clockPunch(false)"); ev("saveGame()"); print('  after save', ev(STATE), errs[:2]); b.close()
    print('C: clock in at 08:56, play frames to past 09:00 inside the 5 s window, then Undo; then to the day\'s end')
    b, pg, ev, errs = page(pw)
    ev("(SHIP.time.min = 8 * 60 + 58.5, 0)"); ev("clockPunch(false)")
    for i in range(12):
        pg.evaluate('window.__step(10, 33)')   # 10 frames of 1/30 s virtual time each
        st = ev(STATE)
        if st['sent'] or not st['undo']: break
    print('  in the window', st)
    print('  Undo ->', ev("clockUndo()"), ev(STATE))
    ev("(() => { for (let t = shipNow() + 30; t <= 9 * 1440 + 60; t += 30) skipTo(t); })()")
    print('  next morning', ev(STATE), 'careerFullDay(9):', ev("careerFullDay(9)"), errs[:2]); b.close()
