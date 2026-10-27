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
    # Senior, everything before m19 trained (as mech_check's reset), (m20)
    ev("(() => { const W = SHIP.works; W.tier = 3; W.rank = 'senior'; for (const r of CAREER_LADDER.slice(0, CAREER_LADDER.indexOf(ladderRow('m20')))) { if (W.tr[r.id] === undefined) W.tr[r.id] = 16; W.use[r.id] = Math.max(W.use[r.id] || 0, 9); if (!Object.values(W.op).some(a => a.includes(r.id))) (W.op[16] = W.op[16] || []).push(r.id); } W.xp = 50; W.cur = null; return true; })()")
    ev(f"devmodeSkipTo({D(19, 5, 50)})"); ev("devmodeTopUp()"); step(10)
    ev(HOOK)
    who = "(() => ['mori','calder'].map(id => { const a = DECK_CREW.find(x => x.p && x.p.id === id); return id + ':' + (a ? (ROOMS[roomAt(...a.here())] || {}).name : 'not on deck ' + deckDef.num); }))()"
    print('  ', ev("(typeof ladderRow === 'function' && ladderRow('m20')) ? JSON.stringify({ day: ladderRow('m20').day, by: ladderRow('m20').by }) : 'no row'"), 'mori works Fri?', ev("(() => { try { return isWorkDay(ROSTER.find(p => p.id === 'mori'), 19); } catch (e) { return String(e); } })()"))
    ev(f"devmodeSkipTo({D(19, 9, 0)})"); ev("devmodeTopUp()"); step(10); ev("careerClock(shipNow(), true)"); step(5)
    until(D(19, 9, 50)); flush(); print('  09:50', info()); shot('m20_0950_arrow')
    ev("(() => { goToDeck(2); const t = ROOM_TILES['A']; player.obj.position.copy(cellPos(...t[Math.floor(t.length/2)])); player.stop(); })()"); step(20)
    until(D(19, 10, 2)); flush(); print('  10:02', info(), ev(who)); shot('m20_1002_room')
    until(D(19, 10, 30), "typeof DIALOGUE !== 'undefined' && !!DIALOGUE"); flush(); print('  card', info(), ev(who)); shot('m20_card')
    lines = []
    for i in range(30):
        v = ev("(() => { if (!DIALOGUE) return null; const v = dialogueView(); return v ? { n: v.name, t: v.text, c: v.choices ? v.choices.map(c => c.text || c) : null } : null; })()")
        if not v: break
        lines.append(v); ev("(() => { const v = dialogueView(); if (v && v.choices) dialogueChoose(0); else dialogueNext(); })()"); step(3)
    for l in lines: print('    ', l)
    flush(); print('  after', info(), 'trained', ev("SHIP.works.tr.m20"), 'cur', ev("SHIP.works.cur && SHIP.works.cur.id"))
    for t in (10, 25, 40, 60, 90):
        until(D(19, 10, t)); flush(); print(f"  10:{t:02d}" if t < 60 else f"  t+{t}", info(), "cur", ev("SHIP.works.cur && [SHIP.works.cur.id, SHIP.works.cur.st, SHIP.works.cur.j]"), "myJob", ev("(() => { try { const m = myJob(); return m && m.id; } catch (e) { return null; } })()"))
        if t == 25: shot("m20_1025_turn")
    print("errors", errs[:5]); b.close(); srv.terminate()
