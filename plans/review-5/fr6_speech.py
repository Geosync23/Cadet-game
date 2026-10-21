# PR5: turn 6 + the arrival fix on a real save (localStorage), phone 390x844.
#  A. Day 5 from 15:40 in the auditorium (a seat row): the room fills, the speech over Marrow/Vance, the bubble's
#     place on screen (inside the viewport? its card's top >= 0?), shots at 16:06 and 16:20
#  B. a real reload at ~16:24 (saveGame, page reload): same speech (FRI.today), the line of the moment, not line 0
#  C. missed: Day 12 (stays on Deck 4) -> the banner + Mail at 16:50 once; and Day 19 skipped across midnight from 15:00
#  D. off-screen pin: the bubble's anchor steady over still frames
import os, sys, json, re, pathlib
S = '/tmp/claude-0/-home-user/a4344e06-66ec-50a3-8125-a9cc15d32fe0/scratchpad'
exec(open(S + '/probe/pp.py').read())
path = sys.argv[1]; OUT = pathlib.Path(S + '/probe/shots'); tag = sys.argv[2] if len(sys.argv) > 2 else 'p'
save = {'v': 2, 'build': 'x', 'time': {'day': 5, 'min': 16 * 60 + 18}, 'player': {'deck': 7, 'tile': [20, 4], 'facing': 0}, 'ship': {'decks': {}, 'eventLog': []}, 'crew': {}}
pw = sync_playwright().start()
b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME'), args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
ctx = b.new_context(viewport={'width': 390, 'height': 844}, has_touch=True); pg = ctx.new_page(); errs = []
pg.on('pageerror', lambda e: errs.append(str(e)))
pg.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
pg.add_init_script(INIT + "try { if (!sessionStorage.getItem('seeded')) { sessionStorage.setItem('seeded', '1'); localStorage.clear(); localStorage.setItem('starship-cadet-save', " + json.dumps(json.dumps(save)) + "); localStorage.setItem('starship-cadet-arrived', '1'); } } catch (e) {}")
(WORK / 'test').mkdir(parents=True, exist_ok=True)
tmp = WORK / 'test' / ('_r5_' + tag + '.html'); tmp.write_text(instrument(pathlib.Path(path).read_text()))
def load():
    pg.goto('file://' + str(tmp) + '?debug', timeout=240000); pg.wait_for_function('window.__sc !== undefined || window.__err', timeout=240000)
    pg.add_style_tag(content='.bub{animation:none!important}')
ev = lambda s: pg.evaluate('s => window.__sc(s)', s)
step = lambda n: pg.evaluate(f'window.__step({n}, 1000/30)')
SEAT = """(() => { if (deckDef.num !== 7) goToDeck(7); const M = DECKS[7].map, c = []; for (let j = 0; j < M.length; j++) for (let i = 0; i < M[j].length; i++) if (M[j][i] === 'A') c.push([i, j]);
  const t = cellPos(...c[Math.floor(c.length / 2)]); player.obj.position.set(t.x, 0, t.z); player.path.length = 0; target.copy(player.obj.position).setY(.7); return c[Math.floor(c.length / 2)]; })()"""
BUB = """(() => bubbles.list.map(b => { const r = b.card.getBoundingClientRect(), w = b.who; return { who: (bubblePerson(w) || {}).id, stand: !!(w.H), shown: b.el.style.display !== 'none',
  top: Math.round(r.top), bot: Math.round(r.bottom), left: Math.round(r.left), right: Math.round(r.right), x: +b.x.toFixed(1), y: +b.y.toFixed(1), t: b.text.slice(0, 40) }; }))()"""
CNT = "(() => { const l = DECKS[7].places.find(p => p.type === 'rec:lectern'), L = cellPos(...l.at); let s = 0, lec = []; for (const a of DECK_CREW) { const dd = Math.hypot(a.x - L.x, a.z - L.z); if (dd < 12 && /sit/.test(a.pose || '')) s++; if (dd < 2.5 && a.p) lec.push(a.p.id); } return [clockText(), s, lec.sort(), FRI_SAID && FRI_SAID[1]]; })()"
res = {}
load(); step(20); print('loaded', ev("clockText()"), ev("SHORT_FRIDAY"), flush=True)
print('seat', ev(SEAT)); step(10)
# A
shot = {}; log = []
for k in range(900):
    step(20); c = ev(CNT); m = ev("Math.floor(shipNow() % 1440)")
    if k % 10 == 0: log.append(c); print(c, flush=True)
    if m >= 966 and 'a' not in shot: shot['a'] = 1; pg.screenshot(path=str(OUT / (tag + '_d5_1606.png'))); res['A_1606'] = [c, ev(BUB)]
    if m >= 980 and 'b' not in shot: shot['b'] = 1; pg.screenshot(path=str(OUT / (tag + '_d5_1620.png'))); res['A_1620'] = [c, ev(BUB)]
    if m >= 984 or (m >= 966 and m < 975 and 'a' in shot and False): break
print('fill log', log, flush=True)
print('A 16:06', json.dumps(res.get('A_1606')), flush=True); print('A 16:20', json.dumps(res.get('A_1620')), flush=True)
# D: still frames, anchor steady
xs = []
for k in range(30): step(1); xs.append([(b['x'], b['y'], b['who']) for b in ev(BUB)])
res['D_still'] = xs[::6]; print('D still', xs[::6], flush=True)
# B: real reload
before = ev("[JSON.stringify(FRI.today), FRI_SAID, clockText()]")
ev("saveGame()"); sv = ev("JSON.parse(localStorage.getItem(SAVE_KEY)).fri")
print('B before', before, 'saved fri', json.dumps(sv)[:200], flush=True)
ev("window.onbeforeunload = null"); load(); step(3)
after = ev("[JSON.stringify(FRI.today), FRI_SAID, clockText(), Math.floor((shipNow() % 1440 - FRI_TALK[0]) * friSpeech(5).length / (FRI_TALK[1] - FRI_TALK[0]))]")
print('B after reload', after, flush=True)
print('B seat after reload', ev("[deckDef.num, roomAt(...player.here())]"), ev(BUB), flush=True)
res['B'] = [before, after]
# C1: missed Day 12 on Deck 4
ev("goToDeck(4)"); ev("skipTo(11 * 1440 + 15 * 60)"); step(5)
ev("window.__toasts = []; { const t0 = toast; toast = (t, x) => { window.__toasts.push([t, x, clockText()]); t0(t, x); }; }")
ev("skipTo(11 * 1440 + 16 * 60 + 45)")
for k in range(80): step(20)
res['C1'] = ev("[FRI.heard, FRI.mailed, window.__toasts.filter(x => /missed|Mail/.test(x[1] || '')), SHIP.mail.filter(m => m.at > 11 * 1440 + 900).map(m => [m.at % 1440, m.from, m.subject])]")
print('C1 Day 12 missed', json.dumps(res['C1']), flush=True)
# C2: Day 19 slept/skipped from 15:00 Friday to Saturday 07:00
ev("skipTo(18 * 1440 + 15 * 60)"); step(5); ev("skipTo(19 * 1440 + 7 * 60)")
for k in range(20): step(10)
res['C2'] = ev("[clockText(), FRI.heard, FRI.mailed, SHIP.mail.filter(m => m.at > 18 * 1440 + 900).map(m => [m.at % 1440, m.from, m.subject])]")
print('C2 Day 19 skipped over', json.dumps(res['C2']), flush=True)
print('errors', errs[:5])
json.dump(res, open(OUT / (tag + '_res.json'), 'w'), indent=1)
