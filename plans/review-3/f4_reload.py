# PR3: EV1's F4 (EV_REPLAY_ON). With EVENTS_ON on in a copy, a real save at Day 11 09:00: walk into Calder's storm briefing
# (09:15, the Works bay), save mid-way, reload: it plays again once (meetings counted once); end it: 'open' cleared. Then a
# second save mid-meeting reloaded after its window: no replay, the gist instead. Run: python3 f4_reload.py ON.html
import os, sys, json, re, pathlib
os.environ.setdefault('CADET_WORK', '/tmp/work-RV3')
exec(open('/tmp/rv/pp.py').read())
path = sys.argv[1]
save = {'v': 2, 'build': 'x', 'time': {'day': 11, 'min': 540}, 'player': {'deck': 5, 'tile': [20, 4], 'facing': 0}, 'ship': {'decks': {}, 'eventLog': []}, 'crew': {}}
pw = sync_playwright().start()
b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME'), args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
ctx = b.new_context(viewport={'width': 390, 'height': 844}, has_touch=True); pg = ctx.new_page(); errs = []
pg.on('pageerror', lambda e: errs.append(str(e)))
pg.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
pg.add_init_script(INIT + "try { if (!sessionStorage.getItem('seeded')) { sessionStorage.setItem('seeded', '1'); localStorage.clear(); localStorage.setItem('starship-cadet-save', " + json.dumps(json.dumps(save)) + "); localStorage.setItem('starship-cadet-arrived', '1'); } } catch (e) {}")
tmp = WORK / 'test' / '_f4_on.html'; tmp.write_text(instrument(pathlib.Path(path).read_text()))
def load():
    pg.goto('file://' + str(tmp) + '?debug'); pg.wait_for_function('window.__sc !== undefined || window.__err', timeout=90000)
ev = lambda s: pg.evaluate('s => window.__sc(s)', s)
step = lambda n: pg.evaluate(f'window.__step({n}, 1000/30)')
GO = """(() => { const m = MEETINGS.find(x => x.id === 'stormBriefing'); if (!m) return 'no meeting'; const d = m.where.deck; if (deckDef.num !== d) goToDeck(d);
  const key = evRoomKey(d, m.where.room), pl = DECKS[d].places.find(p => p.room === key) || DECKS[d].places.find(p => p.type === 'jobboard');
  const c = pl.at, P = cellPos(...c), o = nearestOpen(P.x, P.z, player) || c; player.obj.position.copy(cellPos(...o)); player.path.length = 0; target.copy(player.obj.position).setY(.7); return [d, key, m.at % 1440]; })()"""
ST = "(() => ({ t: clockText(), dlg: DIALOGUE && DIALOGUE.id, i: DIALOGUE && DIALOGUE.i, ev: SHIP.event && SHIP.event.id, mine: SHIP.event && SHIP.event.mine }))()"
load(); step(20); print('loaded', ev(ST), flush=True)
ev("skipTo(10 * 1440 + 9 * 60 + 13)"); step(5); print('go', ev(GO), flush=True)
for k in range(300):
    step(15)
    if ev("!!DIALOGUE"): break
print('in meeting', ev(ST), flush=True)
ev("DIALOGUE && dialogueNext()"); step(3); ev("saveGame()"); print('saved mid', ev(ST), flush=True)
load(); step(30); ev(GO); 
for k in range(60):
    step(15)
    if ev("!!DIALOGUE"): break
r1 = ev(ST); print('after reload', r1, flush=True)
for k in range(80):
    if not ev("!!DIALOGUE"): break
    ev("(() => { const l = DIALOGUE.queue[DIALOGUE.i]; if (l && l.choice) dialogueChoose(0); else dialogueNext(); })()"); step(2)
r2 = ev(ST); print('ended', r2, flush=True)
ok = r1['dlg'] == 'calderStorm' and r1['i'] == 0 and r2['mine'].get('meetings') == 1 and 'open:stormBriefing' not in r2['mine']
print('REPLAY', 'OK' if ok else 'FAILED')
# case 2: saved mid-meeting, the save's clock moved past the meeting's window: no replay, its gist instead
ev("skipTo(10 * 1440 + 9 * 60 + 13)"); step(3)
ev("(() => { const f = SHIP.event.mine; delete f['met:stormBriefing']; delete f['gist:stormBriefing']; delete f['choice:calderStorm']; f.meetings = 0; })()")
ev(GO)
for k in range(300):
    step(15)
    if ev("!!DIALOGUE"): break
ev("DIALOGUE && dialogueNext()"); step(3); ev("saveGame()"); m0 = ev(ST)
pg.evaluate("(() => { const s = JSON.parse(localStorage.getItem('starship-cadet-save')); s.time.min = 9 * 60 + 45; localStorage.setItem('starship-cadet-save', JSON.stringify(s)); Storage.prototype.setItem = () => {}; })()")
load(); step(40); r3 = ev(ST); print('reloaded past the window', r3, flush=True)
ok2 = not r3['dlg'] and 'open:stormBriefing' not in r3['mine'] and r3['mine'].get('gist:stormBriefing') == 1
print('GIST', 'OK' if ok2 else 'FAILED', '| errors', errs[:3])
b.close(); pw.stop()
