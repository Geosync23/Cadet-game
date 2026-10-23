# RV10 probe: FX7's bike tap (LEAD31-1). Touch taps at phone sizes by both bikes (floor and on the bike) in four camera turns,
# plus floor taps at a sample of other Deck 3 places (gym, mess) at 03:00: which place starts
import sys, os, re, pathlib, json
GAME, CT = sys.argv[1], sys.argv[2]
exec(open(CT + '/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
TMP = WORK / 'test' / ('_rv10_' + pathlib.Path(GAME).name); TMP.write_text(instrument(pathlib.Path(GAME).read_text()))
AT = r"""((pid, dx, dz, y) => { const s = placeSpot(pid), v = new THREE.Vector3(s.x + dx, y, s.z + dz).project(camera); return [(v.x + 1) / 2 * innerWidth, (1 - v.y) / 2 * innerHeight]; })"""
def run(pw, W, H):
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': W, 'height': H}, device_scale_factor=1, has_touch=True, is_mobile=True)
    pg = ctx.new_page(); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
    pg.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
    pg.add_init_script(INIT)
    ev = lambda s: pg.evaluate('s => window.__sc(s)', s)
    def step(n):
        pg.evaluate('s => { if (window.__skip === undefined && window.__sc) window.__sc(s); }', SKIP_SWITCH)
        if n > 1: pg.evaluate(f'window.__skip = true; window.__step({n - 1}, 33); window.__skip = false')
        pg.evaluate('window.__step(1, 33)')
    pg.goto('file://' + str(TMP) + '?nosave&debug'); pg.wait_for_function('window.__sc !== undefined', timeout=120000)
    pg.add_style_tag(content='*,*::before,*::after{transition:none!important;animation:none!important}')
    step(10); ev("newGameStart(false); introSkip()"); step(10)
    ev("""(() => { goToDeck(3); setShipNow((SHIP.time.day - 1) * 1440 + 3 * 60); if (typeof GUIDE_ON !== 'undefined' && GUIDE_ON) { GUIDE.tq.length = 0; guideToast = () => false; }
      const s = placeSpot('3-gym-17'); const c = nearestOpen(s.x + 1.5, s.z + 1.5, player); window.__home = cellPos(...c); player.obj.position.copy(__home); player.stop(); })()""")
    step(60)
    def tap(pid, dx, dz, y):
        ev("actEnd(true); player.obj.position.copy(__home); player.stop()"); step(30)
        x, yy = ev(f"({AT})('{pid}', {dx}, {dz}, {y})")
        if not (0 <= x <= W and 130 <= yy <= H - 60): return 'off screen'
        pg.touchscreen.tap(x, yy); step(90)
        a = ev("ACT && ACT.placeId"); c = ev("(() => { const d = document.getElementById('devDlg'); return d && !d.hidden ? 'card' : null; })()")
        if c: ev("devDialogueDo && devDialogueDo('close')")
        return a or c or ev("ACT ? ACT.kind : 'nothing'")
    bike = {'ok': 0, 'n': 0, 'bad': []}
    for turn in range(4):
        for pid, sx in (('3-gym-16', -1), ('3-gym-17', 1)):
            for dx, dz, y, what in ((0, 0, .02, 'floor'), (.3 * sx, 0, .02, 'floor out'), (0, .3, .02, 'floor front'), (0, -.3, .02, 'floor back'), (0, 0, .45, 'saddle'), (0, 0, .85, 'bars')):
                r = tap(pid, dx, dz, y)
                if r == 'off screen': continue
                bike['n'] += 1
                if r == pid: bike['ok'] += 1
                else: bike['bad'].append([turn, pid, what, r])
        ev("actEnd(true)"); pg.locator('#rot').tap(); step(80)
    print(f'{W}x{H} bikes: {bike["ok"]} of {bike["n"]} taps started the bike tapped; others: {bike["bad"]}')
    # other places on Deck 3 (turn back to 0): a floor tap at each place's spot, from beside it
    others = ev("(() => (deckDef.places || []).filter(p => /^(3-gym-|3-mess-)/.test(p.id) && placeSpot(p.id)).map(p => p.id).filter((_, i) => i % 3 === 0).slice(0, 30))()")
    res = {}
    for pid in others:
        ev(f"(() => {{ const s = placeSpot('{pid}'); const c = nearestOpen(s.x + 1.2, s.z + 1.2, player); window.__home = cellPos(...c); }})()")
        res[pid] = tap(pid, 0, 0, .02)
    good = sum(1 for k, v in res.items() if v == k)
    print(f'{W}x{H} other places: {good} of {len([v for v in res.values() if v != "off screen"])} on screen started the place tapped')
    print('   ', json.dumps({k: v for k, v in res.items() if v != k}))
    print('  errors:', errs[:3]); b.close()
with sync_playwright() as pw:
    for W, H in ((320, 640), (390, 844)): run(pw, W, H)
