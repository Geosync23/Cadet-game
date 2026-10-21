# PR4: EV2's storm S8 (5cb698a): the Captain's banner at the front (Day 12 14:00) on a phone starts below the device,
# pause and Tracked buttons. Switched-on copy, a real save Day 12 13:55, at 390x844 and 360x780; shots and the boxes.
import os, sys, json, re, pathlib
os.environ.setdefault('CADET_WORK', '/tmp/work-RV4')
exec(open('/home/user/cadet-game/plans/review-4/pp.py').read())
path = sys.argv[1]; OUT = pathlib.Path('/home/user/cadet-game/plans/review-4/shots'); OUT.mkdir(exist_ok=True)
save = {'v': 2, 'build': 'x', 'time': {'day': 12, 'min': 835}, 'player': {'deck': 3, 'tile': [20, 10], 'facing': 0}, 'ship': {'decks': {}, 'eventLog': []}, 'crew': {}}
pw = sync_playwright().start()
b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME'), args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
(WORK / 'test').mkdir(parents=True, exist_ok=True)
tmp = WORK / 'test' / '_s8_on.html'; tmp.write_text(instrument(pathlib.Path(path).read_text()))
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
    for k in range(400):
        step(10)
        if ev("(() => { const c = document.getElementById('devAddr') || ADDRESS_EL; return !!(c && !c.hidden && c.offsetWidth > 0 && c.textContent.length > 5); })()"): break
    box = ev("""(() => { const r = e => { const el = typeof e === 'string' ? document.getElementById(e) : e; if (!el || !el.offsetWidth) return null; const b = el.getBoundingClientRect(); return [Math.round(b.top), Math.round(b.bottom), Math.round(b.left), Math.round(b.right)]; };
      return { t: clockText(), addr: r(document.getElementById('devAddr') || ADDRESS_EL), dev: r('devBtn'), pause: r('pauseBtn'), trk: r('trkBtn') }; })()""")
    pg.screenshot(path=str(OUT / f's8_banner_{w}.png'))
    lows = [v[1] for k, v in box.items() if k in ('dev', 'pause', 'trk') and v]
    res[w] = (box, bool(box['addr']) and all(box['addr'][0] >= y for y in lows), errs[:2]); print(w, res[w], flush=True)
    ctx.close()
print('S8', 'OK' if all(v[1] and not v[2] for v in res.values()) else 'CHECK'); b.close(); pw.stop()
