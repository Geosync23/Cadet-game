# DR1: Undo when the reload is slow (6 s for the page to come back, as a phone on a weak link might): does the Undo happen?
import sys, os, re, json, pathlib, time, threading, http.server, functools
os.environ.setdefault('CADET_CHROME','/opt/pw-browsers/chromium')
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("class Game")[0])
from playwright.sync_api import sync_playwright
DELAY = float(sys.argv[2])
d = WORK / 'test'; (d / '_dr1_slow.html').write_text(instrument(pathlib.Path(sys.argv[1]).read_text()))
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(d)))
threading.Thread(target=srv.serve_forever, daemon=True).start()
url = f'http://127.0.0.1:{srv.server_address[1]}/_dr1_slow.html#dev'
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ['CADET_CHROME'], args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width':390,'height':844}); pg = ctx.new_page()
    pg.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
    loads = {'n': 0}
    def slow(route):
        loads['n'] += 1
        if loads['n'] > 1: time.sleep(DELAY)          # the reload comes back slowly
        route.continue_()
    pg.route(re.compile(r'.*_dr1_slow\.html.*'), slow)
    pg.add_init_script(INIT); pg.goto(url); pg.wait_for_function('window.__sc !== undefined', timeout=90000)
    ev = lambda s: pg.evaluate('s => window.__sc(s)', s)
    ev("(() => { renderer.render = () => {}; })()"); pg.evaluate('window.__step(10, 33)')
    ev("(INTRO_BOOT = false, newGameStart(false), introSkip(), saveGame(), 0)")
    before = ev("clockText()")
    ev("(devmodeRun('test +3 h', () => devmodeSkipTo(shipNow() + 180)), 0)")
    after = ev("clockText()"); print('before', before, '| after the Dev action', after, '| undo kept:', ev("!!devmodeRead(DM_KEY.undo)"))
    # Undo: the page asks to reload; the main loop keeps running (real frames) while the reload is slow
    pg.evaluate("window.__sc('devmodeUndo()')")
    t0 = time.time()
    while time.time() - t0 < DELAY + 20:
        try:
            if pg.evaluate("typeof window.__sc === 'function' && window.__loaded2 === undefined") : pass
        except Exception: pass
        time.sleep(0.5)
        try:
            n = pg.evaluate("performance.getEntriesByType('navigation')[0].type")
            if n == 'reload' and pg.evaluate("window.__sc !== undefined"): break
        except Exception: pass
    pg.wait_for_function('window.__sc !== undefined', timeout=90000)
    ev = lambda s: pg.evaluate('s => window.__sc(s)', s)
    print(f'reload took ~{DELAY}s: after the reload the clock is', ev("clockText()"), '| undo record left:', ev("!!devmodeRead(DM_KEY.undo)"), '| Undo happened:', ev("clockText()") == before)
    b.close(); srv.shutdown()
