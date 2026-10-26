# RV19: the promotion's beats played live at phone size (390 x 844), Dev mode on a real (Dev) save
# Run: python3 plans/rv19-storm-live.py GAME.html SERVE_DIR SHOT_DIR   (own CADET_WORK; 127.0.0.1:8793; Dev mode; Friday 18:00 to the storm stories)
import sys, os, re, json, pathlib, subprocess, time
GAME, SRV, OUT = sys.argv[1], pathlib.Path(sys.argv[2]), sys.argv[3]
STAGES = set(sys.argv[4:]) or None
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
(SRV / 'g.html').write_text(instrument(pathlib.Path(GAME).read_text()))
srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8793', '--bind', '127.0.0.1', '-d', str(SRV)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
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
    page.add_init_script(INIT); page.goto('http://127.0.0.1:8793/g.html#dev')
    page.wait_for_function('window.__sc !== undefined', timeout=90000)
    ev = lambda s: page.evaluate('s => window.__sc(s)', s)
    page.add_style_tag(content='*,*::before,*::after{transition:none!important;animation:none!important}')
    ev(SKIP_SWITCH)
    def step(n):
        if n > 1: page.evaluate(f'window.__skip = true; window.__step({n - 1}, {1000/30}); window.__skip = false')
        page.evaluate(f'window.__step(1, {1000/30})')
    step(20)
    if page.locator('text=Sign and go aboard').count(): page.fill('form input', 'Ada'); page.click('text=Sign and go aboard'); step(30)
    ev('introSkip()'); step(10); print('start', ev('clockText()'), 'storm sat', ev('stormSatDay()'))
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
    jc = "(() => { const r = 'j'; goToDeck(4); player.obj.position.copy(cellPos(...ROOM_TILES[r][Math.floor(ROOM_TILES[r].length / 2)])); player.stop(); })()"
    print('Day 12 Friday evening'); ev(f"devmodeSkipTo({D(12, 17, 55)})"); ev("devmodeTopUp()"); until(D(12, 18, 3)); flush()
    print('Day 13 morning'); ev(f"devmodeSkipTo({D(13, 8, 40)})"); ev("devmodeTopUp()"); ev(bay); step(5); flush()
    print('  ', info(), ev("devDay(13).map(x => hhmm(x.from) + ' ' + x.title).join(' | ')"))
    until(D(13, 9, 2)); ev("careerClock(shipNow(), true)"); step(5)
    ev("ixBoard.open()"); step(20); flush(); print('  board:', ev("[...document.querySelectorAll('#ixBoard .row b, .board .row b, #board b')].map(b => b.textContent).slice(0, 14)"))
    print('  jobsBoard:', ev("jobsBoard().filter(j => !stormBoardHide(j)).map(j => j.title + (j.claimedBy ? ' [' + j.claimedBy + ']' : '')).slice(0, 14)"))
    print('  hidden:', ev("jobsBoard().filter(j => stormBoardHide(j)).length"), 'works crew at work 10:00?')
    shot('S1_board_0902')
    ev("ixBoard.close && ixBoard.close()"); step(5)
    until(D(13, 10, 0)); print('  ', ev("schedPeople().filter(p => p.dept === 'works' && p.shift !== 'night' && p.rank !== 'guest').map(p => { const w = whereIs(p, shipNow()); return w && w.act; }).reduce((o, a) => (o[a] = (o[a] || 0) + 1, o), {})"))
    print('Day 13 supper'); ev(f"devmodeSkipTo({D(13, 17, 50)})"); ev("devmodeTopUp()"); flush()
    print('  ', info(), ev("devDay(13).filter(x => x.from >= 1020).map(x => hhmm(x.from) + ' ' + x.title).join(' | ')"))
    ev("(() => { goToDeck(3); player.obj.position.copy(cellPos(...ROOM_TILES['M'][5])); player.stop(); })()"); until(D(13, 18, 20)); flush(); shot('S2_supper_1820')
    print('Day 13 storm stories'); ev(f"devmodeSkipTo({D(13, 20, 58)})"); ev("devmodeTopUp()"); ev(jc); step(5); until(D(13, 21, 5)); flush()
    print('  ', info(), 'dress', ev("[...DRESS.on]"), 'oduya', ev("(() => { const a = DECK_CREW.find(x => x.p && x.p.id === 'oduya'); return a ? [roomAt(...cellAt(a.x, a.z)), a.spot && a.spot.id] : null; })()"), 'in j:', ev("DECK_CREW.filter(a => { try { return roomAt(...cellAt(a.x, a.z)) === 'j'; } catch (e) { return false; } }).length"))
    shot('S3_stories_2105')
    r = ev("(() => { try { return tradJoinTap(DECK_CREW.find(x => x.p && x.p.id === 'oduya')); } catch (e) { return 'ERR ' + e.message; } })()"); print('  tradJoin:', r); step(60); flush()
    print('  ', info(), 'act', ev("ACT ? [ACT.kind, ACT.placeId, ACT.phase] : null"), 'room', ev("roomAt(...player.here())"))
    until(D(13, 21, 15)); flush(); shot('S4_stories_2115')
    until(D(13, 21, 47)); flush(); print('  ', info()); shot('S5_after')
    print('errors', errs[:4])
    b.close()
srv.terminate()
