# RV10 probe: AC3's kept join notice, a real tap on a tradition's leader during a burst of pop-ups, at phone sizes
import sys, os, re, pathlib, json, time
GAME, CT, OUT = sys.argv[1], sys.argv[2], pathlib.Path(sys.argv[3]); OUT.mkdir(parents=True, exist_ok=True)
exec(open(CT + '/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
TMP = WORK / 'test' / ('_rv10_' + pathlib.Path(GAME).name); TMP.write_text(instrument(pathlib.Path(GAME).read_text()))
SET = r"""(name => {
  let d = 1, e = null; for (; d < 60; d++) { e = eventsOn(d).find(x => x.name === name); if (e) break; }
  if (!e) return { err: 'not on' };
  goToDeck(e.ev.where[0].deck); actEnd(true); clearGoal(); setShipNow((d - 1) * 1440 + e.from + 10); deckCrewFill();
  SHIP.events.joined = SHIP.events.joined.filter(k => k !== e.id + '@' + d); EV_MIN = -1; eventsTick();
  const lead = tradLeader(e), a = tjAgent(lead); if (!a) return { err: 'no leader' };
  const n = nearestOpen(a.x + 1.2, a.z + 1.2, player); player.obj.position.copy(cellPos(...n)); player.stop();
  window.__ev = e.id + '@' + d; return { id: e.id, d, lead };
})"""
def run(pw, W, H, name):
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
    pg.goto('file://' + str(TMP) + '?nosave'); pg.wait_for_function('window.__sc !== undefined', timeout=120000)
    step(10); ev("newGameStart(false); introSkip()"); step(10)
    s = ev(f"({SET})('{name}')"); step(40); print(f'{W}x{H} {name}:', s)
    # a burst of four ordinary pop-ups, then a real tap on the leader
    ev("['B1','B2','B3','B4'].forEach(k => toast('Burst', k))")
    xy = ev("(() => { const a = TJ_NOW && TJ_NOW.agent; if (!a) return null; const v = new THREE.Vector3(a.x, 1.1, a.z).project(camera); return [(v.x + 1) * innerWidth / 2, (1 - v.y) * innerHeight / 2]; })()")
    if xy: pg.touchscreen.tap(xy[0], xy[1])
    step(3); ev("['A1','A2','A3','A4'].forEach(k => toast('After', k))")   # more pop-ups straight after the join
    seen, t0 = [], time.time()
    for _k in range(60):
        step(6); txt = ev("document.getElementById('tt').textContent + ' | ' + document.getElementById('tx').textContent.slice(0, 50)")
        if not seen or seen[-1] != txt: seen.append(txt)
        if name in txt.split(' | ')[0] and not any('shot' in x for x in seen): pg.screenshot(path=str(OUT / f'{W}x{H}-join.png'), timeout=120000); seen.append('shot')
    joined = ev("SHIP.events.joined.includes(window.__ev)"); print('  queue now:', ev('JSON.stringify(GUIDE.tq)'), 'TOAST_AT age ms', ev('Math.round(performance.now() - TOAST_AT)'), 'GUIDE_ON', ev('GUIDE_ON'), 'loop', ev('GUIDE.loop'))
    print(f'  tap at {xy and [round(v) for v in xy]}; joined {joined}; pop-ups in order:'); [print('   ', x) for x in seen]
    print('  errors:', errs[:3]); b.close()
with sync_playwright() as pw:
    for W, H in ((320, 640), (390, 844)): run(pw, W, H, 'Gym club')
