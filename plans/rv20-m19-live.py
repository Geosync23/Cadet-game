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
    # Senior, everything before m19 trained (as mech_check's reset), on Day 16 evening
    ev("(() => { const W = SHIP.works; W.tier = 3; W.rank = 'senior'; for (const r of CAREER_LADDER.slice(0, CAREER_LADDER.indexOf(ladderRow('m19')))) { if (r.id === 'm15' || r.id === 'm17') continue; if (W.tr[r.id] === undefined) W.tr[r.id] = 16; W.use[r.id] = Math.max(W.use[r.id] || 0, 9); if (!Object.values(W.op).some(a => a.includes(r.id))) (W.op[16] = W.op[16] || []).push(r.id); } W.xp = 50; W.cur = null; return true; })()")
    ev(f"devmodeSkipTo({D(17, 5, 50)})"); ev("devmodeTopUp()"); step(10)
    ev(HOOK)
    bay = "(() => { if (deckDef.num !== 5) goToDeck(5); player.obj.position.copy(cellPos(...ROOM_TILES['w'][2] || ROOM_TILES['w'][0])); player.stop(); })()"

    calder = "(() => { const a = DECK_CREW.find(x => x.p && x.p.id === 'calder'); const pl = (typeof crewWhere === 'function') ? crewWhere('calder') : null; return a ? ['here', deckDef.num, (ROOMS[roomAt(...a.here())] || {}).name] : ['not on this deck', JSON.stringify(pl)]; })()"
    ev(f"devmodeSkipTo({D(17, 8, 55)})"); ev("devmodeTopUp()"); ev(bay); step(10); flush()
    until(D(17, 9, 1)); ev("careerClock(shipNow(), true)"); step(5); flush(); print('  ', info())
    until(D(17, 10, 46)); flush(); print('  ', info(), ev(calder))
    ev("(() => { goToDeck(1); const t = ROOM_TILES['u']; player.obj.position.copy(cellPos(...t[Math.floor(t.length/2)])); player.stop(); })()"); step(20)
    for k in range(4):
        until(ev('shipNow()') + 3); print('  ', ev('clockText()'), ev(calder))
    until(D(17, 11, 20), "typeof DIALOGUE !== 'undefined' && !!DIALOGUE"); flush(); print('  ', info(), ev(calder)); shot('m19b_card')
    for i in range(30):
        if not ev("typeof DIALOGUE !== 'undefined' && !!DIALOGUE"): break
        btn = page.locator('button.act:visible')
        if btn.count(): btn.first.click()
        else: page.mouse.click(195, 760)
        step(45)
    flush(); print('  ', info(), ev(calder))
    for k in range(5):
        until(ev('shipNow()') + 4); flush(); print('  ', info(), ev(calder))
        if k == 1: shot('m19b_watch')
        if ev("SHIP.works.cur && SHIP.works.cur.st") == 'do': break
    shot('m19b_yourturn')
    clickAt = """(id => { const sp = placeSpot(panelPlace(id)); const v = new THREE.Vector3(sp.x, 0.3, sp.z).project(camera); return [(v.x + 1) / 2 * innerWidth, (1 - v.y) / 2 * innerHeight]; })"""
    def play(mid, tag, pick_wrong):
        for k in range(12):
            j = ev(f"(() => {{ const j = SHIP.jobs.find(x => x.machine === '{mid}' && /relayswap|battcell/.test(x.kind) && x.status !== 'done'); return j && [j.id, j.status, j.claimedBy, j.stepsDone, j.bad, j.wrongs, j.workDone]; }})()")
            print('   job', j)
            if not j or j[6]: break
            ev(f"(() => {{ const m = machineById('{mid}'); if (deckDef.num !== m.deck) goToDeck(m.deck); player.obj.position.copy(cellPos(...m.panel)); player.stop(); }})()"); step(10)
            xy = ev(clickAt + f"('{mid}')"); page.mouse.click(xy[0], xy[1]); step(20)
            for t in range(60):
                if not ev("typeof ACT !== 'undefined' && !!ACT"): break
                step(30)
            flush()
            labs = [page.locator('button:visible').nth(i).inner_text() for i in range(page.locator('button:visible').count())]
            opts = [l for l in labs if (l.startswith('R') and len(l) <= 3) or l.startswith('Cells')]
            if opts:
                shot(f'{tag}_pick')
                if pick_wrong:
                    page.locator(f'button:visible:text-is("{opts[(j[4] + 1) % len(opts)]}")').first.click(); step(20); flush(); pick_wrong = False
                    print('   wrong picked', ev(f"(() => {{ const j = SHIP.jobs.find(x => x.id === '{j[0]}'); return [j.stepsDone, j.wrongs]; }})()"))
                    continue
                page.locator(f'button:visible:text-is("{opts[j[4]]}")').first.click(); step(20); flush()
            if k == 0: shot(f'{tag}_tap0')
    for k in range(5):
        if ev("SHIP.works.cur && SHIP.works.cur.st") == 'do': break
        until(ev('shipNow()') + 4)
    ev("(() => { const j = SHIP.jobs.find(x => x.machine === '1-relay-2' && x.status !== 'done'); if (j && j.claimedBy !== 'you') claimJob(j.id); })()"); step(5)
    play('1-relay-2', 'train', False)
    flush(); print('  trained', ev("SHIP.works.tr.m19"), ev("SHIP.works.tr.m15"), info())
    ev("(() => { const j = pwrJob('relayswap', '1-relay-1', shipNow(), { key: 99 }); SHIP.jobs.push(j); claimJob(j.id); MACH_REV++; return j.id; })()"); step(10)
    play('1-relay-1', 'board', True)
    print('  uses', ev("SHIP.works.use.m19"), ev("JSON.stringify(SHIP.works.side.pwr)"))
    print('errors', errs[:4])
    b.close()
srv.terminate()
