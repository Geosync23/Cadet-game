# RV20: M19's Day 17 lesson played live at phone size. python3 m19_live.py GAME.html SERVE_DIR SHOT_DIR PORT
import sys, os, re, json, pathlib, subprocess, time
GAME, SRV, OUT, PORT = sys.argv[1], pathlib.Path(sys.argv[2]), sys.argv[3], sys.argv[4]
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
SRV.mkdir(parents=True, exist_ok=True); (SRV / 'g.html').write_text(instrument(pathlib.Path(GAME).read_text()))
srv = subprocess.Popen([sys.executable, '-m', 'http.server', PORT, '--bind', '127.0.0.1', '-d', str(SRV)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
HOOK = r"""(() => { window.__log = []; const L = (k, a) => window.__log.push([clockText().replace(/^Day /, 'D'), k, ...a.map(x => typeof x === 'string' ? x : JSON.stringify(x)).map(s => (s||'').slice(0, 200))]);
  const w = (name, k, f) => { const o = eval(name); return (...a) => { L(k, f ? f(a) : a); return o(...a); }; };
  toast = w('toast', 'toast'); deviceNotify = w('deviceNotify', 'notice', a => [a[0] && a[0].text, a[0] && a[0].urgent ? 'urgent' : '']);
  worksSay = w('worksSay', 'says'); mailSend = w('mailSend', 'mail', a => [a[0].from, a[0].subject, a[0].body]);
  dialogueShow = w('dialogueShow', 'card', a => [a[0]]); return true; })()"""
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    page = b.new_context(viewport={'width': 390, 'height': 844}).new_page(); errs = []
    page.on('pageerror', lambda e: errs.append(str(e)))
    page.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
    page.add_init_script(INIT); page.goto(f'http://127.0.0.1:{PORT}/g.html?p5s5#dev')
    page.wait_for_function('window.__sc !== undefined', timeout=120000)
    ev = lambda s: page.evaluate('s => window.__sc(s)', s)
    page.add_style_tag(content='*,*::before,*::after{transition:none!important;animation:none!important}')
    ev(SKIP_SWITCH)
    def step(n):
        if n > 1: page.evaluate(f'window.__skip = true; window.__step({n - 1}, {1000/30}); window.__skip = false')
        page.evaluate(f'window.__step(1, {1000/30})')
    step(20)
    if page.locator('text=Sign and go aboard').count(): page.fill('form input', 'Ada'); page.click('text=Sign and go aboard'); step(30)
    ev('introSkip()'); step(10); print('start', ev('clockText()'), 'P5', ev('P5_STEP5'), ev('P5_M19'))
    seen = 0
    def flush():
        global seen
        L = ev('window.__log'); new = L[seen:]; seen = len(L)
        for x in new:
            if x[1] == 'toast' and 'New job' in ' '.join(x[2:]): continue
            print('   ', ' | '.join(x))
    def until(mins, cond=None, chunk=30):
        for _ in range(6000):
            if ev('shipNow()') >= mins or (cond and ev(cond)): return
            step(chunk)
    def shot(name):
        step(2); page.screenshot(path=f'{OUT}/{name}.png', timeout=180000); print('    shot', name, ev('clockText()'))
    def info():
        return ev("({ clock: clockText(), deck: deckDef.num, room: (ROOMS[roomAt(...player.here())] || {}).name, goal: typeof IX_GOAL !== 'undefined' && IX_GOAL ? IX_GOAL.label : null, guide: GUIDE.pick && GUIDE.pick.id, cur: SHIP.works.cur && [SHIP.works.cur.id, SHIP.works.cur.st], trk: trkItems().slice(0, 4).map(x => (x.tag || '') + ' ' + x.title), card: typeof DIALOGUE !== 'undefined' && DIALOGUE ? (DIALOGUE.m && DIALOGUE.m.id || 'card') : null, tier: SHIP.works.tier, rank: SHIP.works.rank })")

    D = lambda d, h, m=0: (d - 1) * 1440 + h * 60 + m
    print(ev("devmodeRun('Set', () => devmodeSetCareerTo(14))")); step(10)
    ev("(() => { const W = SHIP.works; W.tier = 3; W.rank = 'senior'; for (const r of CAREER_LADDER) { if (r.id === 'mys') continue; if (W.tr[r.id] === undefined) W.tr[r.id] = 18; if (!Object.values(W.op).some(a => a.includes(r.id))) (W.op[18] = W.op[18] || []).push(r.id); } W.cur = null; return true; })()")
    ev(f"devmodeSkipTo({D(21, 8, 50)})"); ev("devmodeTopUp()"); step(10); ev(HOOK)
    bay = "(() => { if (deckDef.num !== 5) goToDeck(5); player.obj.position.copy(cellPos(...ROOM_TILES['w'][2] || ROOM_TILES['w'][0])); player.stop(); })()"
    ev(bay); step(10)
    until(D(21, 9, 2)); flush(); print('  ', info(), 'torres', ev("(() => { const a = DECK_CREW.find(x => x.p && x.p.id === 'torres-zeke'); return a ? (ROOMS[roomAt(...a.here())]||{}).name : 'not on deck'; })()"))
    print('  guide', ev("GUIDE.list.map(e => e.id + ':' + e.level)"), ev("guideMode()"))
    shot('mys_0902')
    # tap the board for real
    ev("(() => { const it = ITEMS.find(i => /^old mysteries$/i.test(i.t)); it.hit.getWorldPosition(_wp); const T = ROOM_TILES['w'].slice().sort((a, b) => { const p = cellPos(...a), q = cellPos(...b); return Math.hypot(p.x - _wp.x, p.z - _wp.z) - Math.hypot(q.x - _wp.x, q.z - _wp.z); }); player.obj.position.copy(cellPos(...T[1])); player.stop(); })()"); step(30); shot('mys_near')
    xy = ev("(() => { const it = ITEMS.find(i => /^old mysteries$/i.test(i.t)); it.hit.getWorldPosition(_wp); const v = _wp.clone().project(camera); return [(v.x + 1) / 2 * innerWidth, (1 - v.y) / 2 * innerHeight]; })()")
    print('  board at', xy); page.mouse.click(xy[0], xy[1]); step(10)
    for t in range(40):
        if ev("!!DEV.open"): break
        step(15)
    flush(); shot('mys_board'); print('  board', ev("DEV.open ? document.getElementById('devBody').innerText.slice(0, 1200) : 'closed'"))
    take = page.locator('#devBody button:visible', has_text='Take')
    print('  takes', take.count())
    if take.count(): take.first.click(); step(10); flush(); shot('mys_taken'); print('  after take', ev("document.getElementById('devBody').innerText.slice(0, 800)"))
    ev("deviceClose()"); step(5)
    print('  sides', ev("ixSides().map(j => j.id)"), 'chore', ev("(ixChore() || {}).id"), 'myJob', ev("(myJob() || {}).id"), 'track', ev("SHIP.player.track"))
    for k in range(4):
        pid = ev("(() => { const j = SHIP.jobs.find(x => x.kind === 'mysc' && x.status !== 'done'); if (!j) return null; const st = jobStops(j); const n = st.findIndex(x => !x.done); return n < 0 ? null : st[n].places[0]; })()")
        if not pid: break
        ev(f"(() => {{ const P = placeById('{pid}'); if (deckDef.num !== P.deck) goToDeck(P.deck); const sp = placeSpot('{pid}'); player.obj.position.set(sp.x, player.obj.position.y, sp.z); player.stop(); }})()"); step(30)
        for y, label in ((0.0, 'floor'), (0.9, 'machine')):
            xy = ev(f"(() => {{ const sp = placeSpot('{pid}'); const v = new THREE.Vector3(sp.x, {y}, sp.z).project(camera); return [(v.x + 1) / 2 * innerWidth, (1 - v.y) / 2 * innerHeight]; }})()")
            page.mouse.click(xy[0], xy[1]); step(30)
            for t in range(40):
                if not ev("typeof ACT !== 'undefined' && !!ACT"): break
                step(30)
            flush(); print('  step', k, pid, label, ev("(() => { const j = SHIP.jobs.find(x => x.kind === 'mysc'); return j && [j.status, j.stepsDone]; })()"))
        shot(f'mys_card{k}')
        # the job board's call
    btns = page.locator('button:visible'); print('  buttons now', [btns.nth(i).inner_text() for i in range(btns.count())][:10])
    print('  state', ev("JSON.stringify(SHIP.works.side.mys)"))
    print('errors', errs[:4])
    page.context.browser.close()
srv.terminate()
