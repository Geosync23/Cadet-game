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
    calder = "(() => { const a = DECK_CREW.find(x => x.p && x.p.id === 'calder'); return a ? [deckDef.num, (ROOMS[roomAt(...a.here())] || {}).name] : 'not on this deck'; })()"
    print(ev("devmodeRun('Set', () => devmodeSetCareerTo(14))")); step(10)
    ev("(() => { const W = SHIP.works; W.tier = 3; W.rank = 'senior'; for (const r of CAREER_LADDER) { if (r.id === 'm18' || r.day > 18 && r.id !== 'm19') continue; if (W.tr[r.id] === undefined) W.tr[r.id] = 17; if (!Object.values(W.op).some(a => a.includes(r.id))) (W.op[17] = W.op[17] || []).push(r.id); } W.cur = null; return true; })()")
    ev(f"devmodeSkipTo({D(18, 5, 55)})"); ev("devmodeTopUp()"); step(10); ev(HOOK)
    bay = "(() => { if (deckDef.num !== 5) goToDeck(5); player.obj.position.copy(cellPos(...ROOM_TILES['w'][2] || ROOM_TILES['w'][0])); player.stop(); })()"
    until(D(18, 6, 5)); flush(); print('  ', info())
    ev(f"devmodeSkipTo({D(18, 8, 25)})"); ev("devmodeTopUp()"); ev(bay); step(10); flush()
    until(D(18, 8, 31)); ev("careerClock(shipNow(), true)"); flush(); print('  ', info()); shot('sd_0831')
    until(D(18, 8, 46)); flush(); print('  ', info(), ev(calder)); shot('sd_0846_arrow')
    ev("(() => { goToDeck(6); const t = ROOM_TILES['j']; player.obj.position.copy(cellPos(...t[Math.floor(t.length/2)])); player.stop(); })()"); step(20)
    for k in range(5):
        until(ev('shipNow()') + 3); print('  ', ev('clockText()'), ev(calder))
    until(D(18, 9, 30), "typeof DIALOGUE !== 'undefined' && !!DIALOGUE"); flush(); print('  ', info(), ev(calder)); shot('sd_meeting')
    for i in range(80):
        if not ev("typeof DIALOGUE !== 'undefined' && !!DIALOGUE"): break
        btn = page.locator('button.act:visible')
        if btn.count(): btn.first.click()
        else: page.mouse.click(195, 760)
        step(12)
    step(30); flush(); print('  ', info(), ev(calder), 'dev open', ev("!!DEV.open")); shot('sd_screen')
    print('  screen', ev("document.getElementById('devBody') && document.getElementById('devBody').innerText.slice(0, 1500)"))
    def click(text):
        b = page.locator('#devBody button:visible', has_text=text)
        if not b.count(): print('   no button', text); return False
        b.first.click(); step(10); flush(); return True
    click('Quietest hour'); shot('sd_quiet'); print('  after quiet', ev("document.getElementById('devBody').innerText.slice(0, 1500)"))
    for i in range(8):
        if not click('Warn'): break
    click('Book for'); shot('sd_booked'); print('  after book', ev("document.getElementById('devBody').innerText.slice(0, 900)"), ev("JSON.stringify(SHIP.works.sd)"), 'tr', ev("SHIP.works.tr.m18"))
    print('  job', ev("(() => { const j = SHIP.jobs.find(x => x.shut); return j && [j.id, j.status, j.why, j.reserved]; })()"))
    ev("deviceClose()"); step(5)
    b = ev("(() => { const b = SHIP.works.sd && SHIP.works.sd.book[0]; return b && [b.day, b.at]; })()"); print('  booking', b)
    if b:
        ev(f"devmodeSkipTo({D(18, 21, 55)})"); step(10); until(D(18, 22, 2)); flush(); print('  settled', ev("JSON.stringify(SHIP.works.sd.set)"))
        at = b[1]
        ev(f"devmodeSkipTo({D(19, at // 60, at % 60) - 40})"); ev("devmodeTopUp()"); ev(bay); step(10); ev("careerClock(shipNow(), true)")
        until(D(19, at // 60, at % 60) - 28); flush(); print('  ', info()); shot('sd_day_notice')
        until(D(19, at // 60, at % 60) - 13); flush(); print('  ', info()); shot('sd_day_arrow')
        print('  job', ev("(() => { const j = SHIP.jobs.find(x => x.shut); return j && [j.id, j.status, j.claimedBy]; })()"))
        until(D(19, at // 60, at % 60) + 1)
        r = ev("(() => { const j = SHIP.jobs.find(x => x.shut); return claimJob(j.id); })()"); step(10); flush(); print('  claimed', r, info())
        ev("(() => { const j = SHIP.jobs.find(x => x.shut); const m = machineById(j.machine); if (deckDef.num !== m.deck) goToDeck(m.deck); player.obj.position.copy(cellPos(...m.panel)); player.stop(); })()"); step(30); flush(); shot('sd_day_junction'); print('  ', info())
        xy = ev("(() => { const j = SHIP.jobs.find(x => x.shut); const sp = placeSpot(panelPlace(j.machine)); const v = new THREE.Vector3(sp.x, 0.4, sp.z).project(camera); return [(v.x + 1) / 2 * innerWidth, (1 - v.y) / 2 * innerHeight]; })()")
        page.mouse.click(xy[0], xy[1]); step(30); flush()
        for t in range(80):
            if not ev("typeof ACT !== 'undefined' && !!ACT"): break
            step(30)
        flush(); print('  after work', info(), ev("JSON.stringify(SHIP.works.sd.set)"), ev("(() => { const j = SHIP.jobs.find(x => x.shut); return j && [j.status, j.workDone, j.claimedBy]; })()"))
        shot('sd_day_done')
    print('errors', errs[:4])
    page.context.browser.close()
srv.terminate()
