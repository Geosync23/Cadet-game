# PR4: EV3's storm S3/S5/S7 (d3bf237), live, switched on, at 390x844:
#  a. S7 Friday Day 12 17:05 in the mess near Lukas: his moment opens ("Sixty"), reply 0 holds the lantern job; no
#     Lukas Mail at 20:50; the lantern job yours when it posts Saturday 14:00;
#  b. S5 the lantern supper, Saturday Day 13: from 17:40 frames played in the mess to 18:40: crew in the mess hall,
#     Brennan there and Lukas not, staying in off, draw calls (phones: under 450), a shot;
#  c. S3 Day 12 15:00 on Deck 7: a rec tap refused with the storm words.
import os, sys, json, re, pathlib
os.environ.setdefault('CADET_WORK', '/tmp/work-RV4')
exec(open('/home/user/cadet-game/plans/review-4/pp.py').read())
path = sys.argv[1]; OUT = pathlib.Path('/home/user/cadet-game/plans/review-4/shots'); OUT.mkdir(exist_ok=True)
save = {'v': 2, 'build': 'x', 'time': {'day': 12, 'min': 840}, 'player': {'deck': 3, 'tile': [20, 10], 'facing': 0}, 'ship': {'decks': {}, 'eventLog': [], 'evFrom': 0}, 'crew': {}}
pw = sync_playwright().start()
b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME'), args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
ctx = b.new_context(viewport={'width': 390, 'height': 844}, has_touch=True); pg = ctx.new_page(); errs = []
pg.on('pageerror', lambda e: errs.append(str(e)))
pg.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
pg.add_init_script(INIT + "try { if (!sessionStorage.getItem('seeded')) { sessionStorage.setItem('seeded', '1'); localStorage.clear(); localStorage.setItem('starship-cadet-save', " + json.dumps(json.dumps(save)) + "); localStorage.setItem('starship-cadet-arrived', '1'); } } catch (e) {}")
(WORK / 'test').mkdir(parents=True, exist_ok=True)
tmp = WORK / 'test' / '_s37_on.html'; tmp.write_text(instrument(pathlib.Path(path).read_text()))
pg.goto('file://' + str(tmp) + '?debug'); pg.wait_for_function('window.__sc !== undefined || window.__err', timeout=90000)
pg.add_style_tag(content='.bub{animation:none!important}')
ev = lambda s: pg.evaluate('s => window.__sc(s)', s)
step = lambda n: pg.evaluate(f'window.__step({n}, 1000/30)')
step(20); res = {}
PUT = """((deck, rx) => { if (deckDef.num !== deck) goToDeck(deck); const R = DECKS[deck].rooms, key = Object.keys(R).find(k => rx.test(R[k].name || ''));
  const pl = DECKS[deck].places.find(p => p.room === key && p.type !== 'callhome') || DECKS[deck].places.find(p => p.room === key); const c = pl.at, P = cellPos(...c), o = nearestOpen(P.x, P.z, player) || c;
  player.obj.position.copy(cellPos(...o)); player.path.length = 0; target.copy(player.obj.position).setY(.7); return [key, R[key].name]; })"""
# c. the rec deck closed
ev("skipTo(11 * 1440 + 15 * 60)"); step(5); print('deck 7', ev(PUT + "(7, /Common room|Lounge|Auditorium|Float/)"), flush=True); step(30)
res['c_shut'] = ev("recEventShut()"); res['c_rec_crew'] = ev("DECK_CREW.filter(a => a.p && a.h).length")
print('rec shut at 15:00', res['c_shut'], 'crew drawn on Deck 7', res['c_rec_crew'], flush=True)
# a. Friday, Lukas
ev("skipTo(11 * 1440 + 17 * 60 + 5)"); step(5); print('mess', ev(PUT + "(3, /^Galley$/)"), flush=True)
got = None
for k in range(200):
    step(10)
    if ev("!!DIALOGUE"): got = ev("[clockText(), DIALOGUE.id, dialogueView()]"); break
    if k % 40 == 39:   # walk to Lukas if he's drawn
        ev("(() => { const a = DECK_CREW.find(a => a.p && a.p.id === 'dlamini-lukas' && a.h); if (a) { const o = nearestOpen(a.x, a.z, player); if (o) { player.obj.position.copy(cellPos(...o)); target.copy(player.obj.position).setY(.7); } } })()")
print('friday moment', got and [got[0], got[1], got[2].get('text')], flush=True); res['a_moment'] = got and got[1]
if got:
    pg.screenshot(path=str(OUT / 's7_lukas_fri.png'))
    for k in range(30):
        if not ev("!!DIALOGUE"): break
        v = ev("dialogueView()")
        if v.get('choices'): print('   choices', v['choices']); ev("dialogueChoose(0)")
        else: print('   ', v.get('name'), '|', v.get('text')); ev("dialogueNext()")
        step(2)
res['a_wants'] = ev("SHIP.event.mine['wants:stormLanterns'] || 0")
ev("skipTo(11 * 1440 + 21 * 60)"); step(3)
res['a_mail'] = ev("SHIP.mail.filter(m => m.from === 'Lukas Dlamini').map(m => [m.at % 1440, m.subject])")
ev("skipTo(12 * 1440 + 14 * 60 + 5)"); step(3)
res['a_job'] = ev("SHIP.jobs.filter(j => j.eventJob === 'stormLanterns').map(j => [j.posted % 1440, j.status, j.claimedBy || null])")
print('wants', res['a_wants'], 'lukas mail', res['a_mail'], 'lantern job', res['a_job'], flush=True)
# b. the supper
ev("skipTo(12 * 1440 + 17 * 60 + 40)"); step(5); print('mess', ev(PUT + "(3, /^Mess hall$/)"), flush=True)
dc = []
for k in range(36):   # play frames, about a ship minute each 30 steps; read every so often
    step(60)
    if k % 6 == 5:
        r = ev("""(() => { const R = DECKS[3].rooms, inMess = DECK_CREW.filter(a => a.p && a.h && (() => { const c = [Math.round(a.x + OX), Math.round(a.z + OZ)]; const k = roomAt(...c); return k && R[k] && /^Mess hall$/.test(R[k].name || ''); })());
          window.__skip = false; window.__step(1, 16); return [clockText(), inMess.length, inMess.some(a => a.p.id === 'brennan'), inMess.some(a => a.p.id === 'dlamini-lukas'), renderer.info.render.calls, eventRoutines(shipNow()).map(r => r.rule).join(',')]; })()""")
        dc.append(r); print('  ', r, flush=True)
pg.screenshot(path=str(OUT / 's5_supper.png'))
res['b'] = dc[-1] if dc else None; res['b_maxcalls'] = max(x[4] for x in dc) if dc else None
ok = res['c_shut'] and res['a_moment'] and res['a_wants'] and not res['a_mail'] and any(j[2] == 'you' for j in res['a_job']) and res['b'] and res['b'][1] >= 40 and res['b'][2] and res['b_maxcalls'] < 450
print('RESULT', res); print('errors', errs[:5]); print('S37', 'OK' if ok and not errs else 'CHECK')
b.close(); pw.stop()
