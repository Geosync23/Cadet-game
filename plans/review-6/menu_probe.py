# PR6: EV4's S9 framed menu (f32d901): a switched-on copy, a real save Day 21 09:00 on Deck 4 with the Captain's table's
# trace ({ id: 'framedMenu', day: 20 }); stand in the bunk room, shots at 390x844 and 360x780, the prop on, its tap
# card, a save and reload keeps it; and the same in an off copy: never shown (on() is the switch).
import os, sys, json, re, pathlib
os.environ.setdefault('CADET_WORK', '/tmp/cadet-work')
exec(open('/home/user/cadet-game/plans/review-6/pp.py').read())
path = sys.argv[1]; tag = sys.argv[2] if len(sys.argv) > 2 else 'on'
OUT = pathlib.Path('/home/user/cadet-game/plans/review-6/shots'); OUT.mkdir(exist_ok=True)
save = {'v': 2, 'build': 'x', 'time': {'day': 21, 'min': 540}, 'player': {'deck': 4, 'tile': [20, 10], 'facing': 0}, 'ship': {'decks': {}, 'eventLog': [], 'evFrom': 0}, 'crew': {}}
pw = sync_playwright().start()
b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME'), args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
(WORK / 'test').mkdir(parents=True, exist_ok=True)
tmp = WORK / 'test' / ('_menu_' + tag + '.html'); tmp.write_text(instrument(pathlib.Path(path).read_text()))
PUT = """(() => { const R = DECKS[4].rooms, o = DRESS_INFO && DRESS_INFO.find ? null : null; const key = 'a';
  const pl = DECKS[4].places.find(p => p.room === key) ; const c = pl ? pl.at : [20, 10], P = cellPos(...c), q = nearestOpen(P.x, P.z, player) || c;
  player.obj.position.copy(cellPos(...q)); player.path.length = 0; target.copy(player.obj.position).setY(.7); return [key, R[key] && R[key].name, c]; })()"""
res = {}
for w, h in [(390, 844), (360, 780)]:
    ctx = b.new_context(viewport={'width': w, 'height': h}, has_touch=True); pg = ctx.new_page(); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
    pg.add_init_script(INIT + "try { if (!sessionStorage.getItem('seeded')) { sessionStorage.setItem('seeded', '1'); localStorage.clear(); localStorage.setItem('starship-cadet-save', " + json.dumps(json.dumps(save)) + "); localStorage.setItem('starship-cadet-arrived', '1'); } } catch (e) {}")
    pg.goto('file://' + str(tmp) + '?debug'); pg.wait_for_function('window.__sc !== undefined || window.__err', timeout=90000)
    ev = lambda s: pg.evaluate('s => window.__sc(s)', s)
    step = lambda n: pg.evaluate(f'window.__step({n}, 1000/30)')
    step(20)
    ev("(() => { if (!SHIP.traces.some(t => (t.id || t) === 'framedMenu')) SHIP.traces.push({ id: 'framedMenu', day: 20 }); goToDeck(3); goToDeck(4); })()")
    step(10); print(w, 'put', ev(PUT), flush=True); step(30)
    r = ev("""(() => { window.__skip = false; window.__step(1, 16); return { t: clockText(), on: DRESS.on.has('framedMenu'), calls: renderer.info.render.calls, home: SHIP.works && SHIP.works.home }; })()""")
    pg.screenshot(path=str(OUT / f'menu_{tag}_{w}.png'), timeout=180000)
    ev("saveGame()"); pg.reload(); pg.wait_for_function('window.__sc !== undefined || window.__err', timeout=90000); step(20)
    r['afterReload'] = ev("[DRESS.on.has('framedMenu'), SHIP.traces.filter(t => (t.id || t) === 'framedMenu').length]")
    res[w] = (r, errs[:3]); print(w, res[w], flush=True); ctx.close()
print('RESULT', res)
want = tag == 'on'
print('MENU', 'OK' if all(v[0]['on'] == want and v[0]['afterReload'][0] == want and not v[1] and v[0]['calls'] < 450 for v in res.values()) else 'CHECK')
b.close(); pw.stop()
