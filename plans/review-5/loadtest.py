import os, sys, json, re, pathlib, time
S = '/tmp/claude-0/-home-user/a4344e06-66ec-50a3-8125-a9cc15d32fe0/scratchpad'
exec(open(S + '/probe/pp.py').read())
path, mins, deck = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
save = {'v': 2, 'build': 'x', 'time': {'day': 5, 'min': mins}, 'player': {'deck': deck, 'tile': [20, 4], 'facing': 0}, 'ship': {'decks': {}, 'eventLog': []}, 'crew': {}}
pw = sync_playwright().start()
b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME'), args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
pg = b.new_context(viewport={'width': 390, 'height': 844}).new_page(); errs = []
pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: errs.append('console ' + m.text[:200]) if m.type == 'error' else None)
pg.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
pg.add_init_script(INIT + "try { localStorage.clear(); localStorage.setItem('starship-cadet-save', " + json.dumps(json.dumps(save)) + "); localStorage.setItem('starship-cadet-arrived', '1'); } catch (e) {}")
tmp = WORK / 'test' / '_r5_lt.html'; tmp.write_text(instrument(pathlib.Path(path).read_text()))
t0 = time.time(); pg.goto('file://' + str(tmp) + '?debug', timeout=300000)
print('goto', round(time.time() - t0), flush=True)
try:
    pg.wait_for_function('window.__sc !== undefined || window.__err', timeout=300000); print('ready', round(time.time() - t0), pg.evaluate("window.__err || window.__sc('clockText()')"))
except Exception as e: print('NOT READY', e)
print(errs[:5])
