# RV19: the promotion's beats played live at phone size (390 x 844), Dev mode on a real (Dev) save
# Run: python3 plans/rv19-promo-live.py GAME.html SERVE_DIR SHOT_DIR   (own CADET_WORK; serves on 127.0.0.1:8792; Dev mode on a real Dev save)
import sys, os, re, json, pathlib, subprocess, time
GAME, SRV, OUT = sys.argv[1], pathlib.Path(sys.argv[2]), sys.argv[3]
STAGES = set(sys.argv[4:]) or None
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
(SRV / 'g.html').write_text(instrument(pathlib.Path(GAME).read_text()))
srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8792', '--bind', '127.0.0.1', '-d', str(SRV)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
HOOK = r"""(() => { window.__log = []; const L = (k, a) => window.__log.push([clockText().replace(/^Day /, 'D'), k, ...a.map(x => typeof x === 'string' ? x : JSON.stringify(x)).map(s => s.slice(0, 160))]);
  const w = (name, k, f) => { const o = eval(name); return (...a) => { L(k, f ? f(a) : a); return o(...a); }; };
  toast = w('toast', 'toast'); deviceNotify = w('deviceNotify', 'notice', a => [a[0] && a[0].text, a[0] && a[0].urgent ? 'urgent' : '']);
  worksSay = w('worksSay', 'says'); bubbleSay = w('bubbleSay', 'bubble', a => [a[0] && a[0].userData && a[0].userData.name || '?', a[1]]);
  mailSend = w('mailSend', 'mail', a => [a[0].from, a[0].subject, a[0].body]);
  dialogueShow = w('dialogueShow', 'card', a => [a[0]]); return true; })()"""
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    page = b.new_context(viewport={'width': 390, 'height': 844}).new_page(); errs = []
    page.on('pageerror', lambda e: errs.append(str(e)))
    page.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
    page.add_init_script(INIT); page.goto('http://127.0.0.1:8792/g.html#dev')
    page.wait_for_function('window.__sc !== undefined', timeout=90000)
    ev = lambda s: page.evaluate('s => window.__sc(s)', s)
    page.add_style_tag(content='*,*::before,*::after{transition:none!important;animation:none!important}')
    ev(SKIP_SWITCH)
    def step(n):
        if n > 1: page.evaluate(f'window.__skip = true; window.__step({n - 1}, {1000/30}); window.__skip = false')
        page.evaluate(f'window.__step(1, {1000/30})')
    step(20)
    if page.locator('text=Sign and go aboard').count(): page.fill('form input', 'Ada'); page.click('text=Sign and go aboard'); step(30)
    ev('introSkip()'); step(10); print('start', ev('clockText()'), 'beats on', ev('promoBeatsOn()'))
    ev(HOOK)
    seen = 0
    def flush(tag=''):
        global seen
        L = ev('window.__log'); new = L[seen:]; seen = len(L)
        for x in new:
            if x[1] == 'toast' and 'New job' in x[2] + (x[3] if len(x) > 3 else ''): continue
            print('   ', ' | '.join(x))
    def until(mins, cond=None, chunk=30):     # step real frames till the ship clock passes mins (absolute), or cond is true
        for _ in range(4000):
            if ev('shipNow()') >= mins or (cond and ev(cond)): return
            step(chunk)
    def shot(name):
        step(2); page.screenshot(path=f'{OUT}/{name}.png', timeout=180000); print('    shot', name, ev('clockText()'))
    def info():
        return ev("({ clock: clockText(), deck: deckDef.num, room: (ROOMS[roomAt(...player.here())] || {}).name, goal: typeof IX_GOAL !== 'undefined' && IX_GOAL ? IX_GOAL.label : null, trk: trkItems().slice(0, 4).map(x => (x.tag || '') + ' ' + x.title), card: typeof DIALOGUE !== 'undefined' && DIALOGUE ? DIALOGUE.m && DIALOGUE.m.id || 'card' : null, tier: SHIP.works && SHIP.works.tier })")
    D = lambda d, h, m=0: (d - 1) * 1440 + h * 60 + m
    bay = "(() => { if (deckDef.num !== 5) goToDeck(5); player.obj.position.copy(cellPos(...ROOM_TILES['w'][2] || ROOM_TILES['w'][0])); player.stop(); })()"
    print(ev("devmodeRun('Set', () => devmodeSetCareerTo(8))")); step(10)
    ev(f"devmodeSkipTo({D(9, 9, 5)})"); ev(bay); step(5)
    ev("(() => { const c = SHIP.works.cur, j = c && SHIP.jobs.find(x => x.id === c.j); if (j) j.claimedBy = 'you'; })()")
    ev("devmodeRun('Turn in', () => { worksDone('t2', shipNow()); return null; })"); step(30)
    ev(f"devmodeSkipTo({D(10, 7, 45)})"); ev("devmodeTopUp()"); ev(bay); step(5); flush()
    until(D(10, 7, 52)); print('  ', info()); shot('G1_0752_toppedup')
    office = "(() => { player.obj.position.copy(cellPos(...ROOM_TILES['o'][1])); player.stop(); })()"
    until(D(10, 8, 10)); ev(office); flush()
    until(D(10, 8, 30), "typeof DIALOGUE !== 'undefined' && !!DIALOGUE"); flush(); print('  ', info()); shot('G2_result_card')
    def through(tag):
        for i in range(40):
            if not ev("typeof DIALOGUE !== 'undefined' && !!DIALOGUE"): break
            btn = page.locator('#dlgBox button:visible, .dlg button:visible, #dlg button:visible')
            if btn.count(): btn.first.click()
            else: page.mouse.click(195, 760)
            step(45)
            if i == 3: shot(tag)
        flush()
    through('G3_result_mid'); print('  ', info(), ev('SHIP.works.tier'))
    ev("careerClock(shipNow(), true)"); step(5)
    ev(f"devmodeSkipTo({D(10, 15, 55)})"); ev("devmodeTopUp()"); ev(bay); step(5); flush()
    until(D(10, 16, 1)); flush(); print('  ', info()); shot('H1_1601')
    until(D(10, 16, 12)); flush(); print('  ', info()); shot('H2_1612_arrow')
    until(D(10, 16, 58), "typeof DIALOGUE !== 'undefined' && !!DIALOGUE"); flush(); print('  ', info(), ev("deckDef.num"), ev("(ROOMS[roomAt(...player.here())]||{}).name")); shot('H3_ceremony')
    through('H4_ceremony_mid'); print('  ', info(), 'pip', ev('PLAYER_SPEC.rank || 0'), ev('SHIP.works.done'))
    ev(f"devmodeSkipTo({D(10, 19, 55)})"); ev(bay); step(5); flush()
    until(D(10, 20, 4)); flush(); print('  ', info()); shot('J1_2004_walk')
    until(D(10, 20, 30), "SHIP.works.done.includes('move2')"); flush(); print('  ', info(), ev('SHIP.works.done'), ev('playerBed()'))
    print('errors', errs[:4])
    b.close()
srv.terminate()
