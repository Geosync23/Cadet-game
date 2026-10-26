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
    who = "(id => { const a = DECK_CREW.find(x => x.p && x.p.id === id); return a ? (ROOMS[roomAt(...a.here())] || {}).name : '-'; })"
    def go(deck, room):
        ev(f"(() => {{ if (deckDef.num !== {deck}) goToDeck({deck}); const t = ROOM_TILES['{room}']; player.obj.position.copy(cellPos(...t[Math.floor(t.length/2)])); player.stop(); }})()"); step(20)
    def goPlace(pid):
        ev(f"(() => {{ const P = placeById('{pid}'); if (deckDef.num !== P.deck) goToDeck(P.deck); const sp = placeSpot('{pid}'); player.obj.position.set(sp.x, player.obj.position.y, sp.z); player.stop(); }})()"); step(20)
    def card(tag, maxn=60):
        n = 0
        for i in range(maxn):
            if not ev("typeof DIALOGUE !== 'undefined' && !!DIALOGUE"): break
            b = page.locator('button.act:visible')
            if b.count(): b.first.click()
            step(12); n += 1
            if i == 2: shot(tag + '_mid')
        flush(); return n
    def wait_card(until_m, tag):
        until(until_m, "typeof DIALOGUE !== 'undefined' && !!DIALOGUE"); flush(); print('  ', info()); shot(tag)
    # 1. the offer at the storm party, Day 14
    print(ev("devmodeRun('Set', () => devmodeSetCareerTo(13))")); step(10); ev(HOOK)
    ev(f"devmodeSkipTo({D(14, 18, 50)})"); ev("devmodeTopUp()"); go(3, 'L')
    print('  party', info(), 'calder', ev(who + "('calder')"))
    wait_card(D(14, 20, 30), 'pu_offer')
    print('  calder', ev(who + "('calder')"), 'halloran', ev(who + "('halloran-emeka')"))
    card('pu_offer'); step(20); flush(); print('  after offer', info(), ev("JSON.stringify(SHIP.works.pu)")); shot('pu_offer_after')
    # 2. the test morning, Day 15
    ev(f"devmodeSkipTo({D(15, 8, 40)})"); ev("devmodeTopUp()"); go(5, 'w'); ev("careerClock(shipNow(), true)")
    until(D(15, 8, 46)); flush(); print('  ', info(), 'calder', ev(who + "('calder')")); shot('pu_test_0846')
    until(D(15, 9, 2)); flush(); print('  ', info(), 'calder', ev(who + "('calder')")); shot('pu_test_0902')
    # 3. the result, Day 16 (career set to 15: the test passed)
    print(ev("devmodeRun('Set', () => devmodeSetCareerTo(15))")); step(10); ev(HOOK)
    ev(f"devmodeSkipTo({D(16, 7, 50)})"); ev("devmodeTopUp()"); go(5, 'w'); ev("careerClock(shipNow(), true)")
    until(D(16, 8, 2)); flush(); print('  ', info(), 'calder', ev(who + "('calder')")); shot('pu_res_0802')
    goPlace('5-office-visit-sit'); until(D(16, 8, 10)); print('  calder', ev(who + "('calder')"))
    wait_card(D(16, 8, 40), 'pu_result'); card('pu_result'); step(20); flush(); print('  after result', info(), ev("JSON.stringify(SHIP.works.pu)")); shot('pu_result_after')
    # 4. the bar, Day 16 16:30
    ev(f"devmodeSkipTo({D(16, 16, 5)})"); ev("devmodeTopUp()"); go(5, 'w')
    until(D(16, 16, 17)); flush(); print('  ', info()); shot('pu_bar_1617')
    go(1, 'O'); until(D(16, 16, 25)); print('  guests', [ (p, ev(who + f"('{p}')")) for p in ('marrow', 'vance', 'calder', 'torres-zeke')])
    wait_card(D(16, 17, 0), 'pu_bar'); card('pu_bar'); step(30); flush(); print('  after bar', info(), ev("JSON.stringify(SHIP.works.pu)"), 'rank', ev("PLAYER_SPEC.rank"), ev("PLAYER_SPEC.bar"))
    shot('pu_bar_after')
    until(ev('shipNow()') + 10); flush(); print('  cake', info()); shot('pu_cake')
    # 5. the toast, Day 17 19:00
    ev(f"devmodeSkipTo({D(17, 18, 40)})"); ev("devmodeTopUp()"); go(5, 'w')
    until(D(17, 18, 46)); flush(); print('  ', info()); shot('pu_toast_1846')
    go(2, 'C'); wait_card(D(17, 19, 30), 'pu_toast'); print('  guests', [(p, ev(who + f"('{p}')")) for p in ('marrow', 'vance', 'calder')])
    card('pu_toast'); step(20); flush(); print('  after toast', info(), ev("JSON.stringify(SHIP.works.pu)"))
    print('errors', errs[:4])
    page.context.browser.close()
srv.terminate()
