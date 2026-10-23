# RV10 probe: FX7 Tiles partner sits at your board, real taps at phone sizes (Deck 4 junior common room table)
import sys, os, re, pathlib, json
GAME, CT, OUT = sys.argv[1], sys.argv[2], pathlib.Path(sys.argv[3]); OUT.mkdir(parents=True, exist_ok=True)
HOURS = [int(x) for x in (sys.argv[4] if len(sys.argv) > 4 else '19').split(',')]
exec(open(CT + '/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
TMP = WORK / 'test' / ('_rv10_' + pathlib.Path(GAME).name); TMP.write_text(instrument(pathlib.Path(GAME).read_text()))
def run(pw, W, H, hr):
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
    pg.add_style_tag(content='*,*::before,*::after{transition:none!important;animation:none!important}')
    step(20); ev("newGameStart(false); introSkip()"); step(20); ev(f"skipTo((SHIP.time.day - 1) * 1440 + {hr} * 60)"); step(30)
    if ev('deckDef.num') != 4: ev('goToDeck(4)'); step(20)
    # walk to the common room by tapping its floor through the game (a real walk), then tap the table on screen
    ev("(() => { const it = ITEMS.find(i => /^Tiles table$/.test(i.t)); const p = new THREE.Vector3(); it.hit.getWorldPosition(p); walkTo ? walkTo(p.x + 1.5, p.z + 1.5) : null; })()") if ev("typeof walkTo === 'function'") else None
    for _ in range(40):
        step(15)
    TXY = """(() => { const it = ITEMS.find(i => /^Tiles table$/.test(i.t)); const p = new THREE.Vector3(); it.hit.getWorldPosition(p); const v = p.clone().project(camera);
      return [(v.x + 1) * innerWidth / 2, (1 - v.y) * innerHeight / 2, Math.hypot(player.obj.position.x - p.x, player.obj.position.z - p.z)]; })()"""
    for k in range(8):   # walk towards it by tapping the floor at the screen's edge, as a player would
        xy = ev(TXY)
        if 20 <= xy[0] <= W - 20 and 150 <= xy[1] <= H - 130: break
        fx = min(max(xy[0], 30), W - 30); fy = min(max(xy[1], 170), H - 150)
        pg.touchscreen.tap(fx, fy)
        for _ in range(12): step(15)
    xy = ev(TXY)
    pg.touchscreen.tap(xy[0], xy[1]); how = 'screen tap'
    print(f'{W}x{H} {hr}:00 table at', [round(v) for v in xy], how)
    seen = None
    for k in range(80):
        step(15)
        r = ev("""(() => { const T = typeof TL_GAME !== 'undefined' && TL_GAME; const o = ACT && ACT.o || {};
          const a = o.opp && DECK_CREW.find(x => x.p && x.p.id === o.opp); const it = ITEMS.find(i => /^Tiles table$/.test(i.t));
          return { act: ACT && ACT.kind, st: o.st, mine: ACT && ACT.placeId, seat: o.seat, opp: o.opp, oppSeat: a && a.goalId, oppPose: a && a.pose, oppSettled: a && a.settled, oppDist: a && +ixDist(it, a).toFixed(2),
            inSeats: !!o.seat && DECKS[4].tiles.seats.includes(o.seat), game: !!T, tx: (document.getElementById('tx') || {}).textContent || '', clock: clockText() }; })()""")
        if r['game'] or (r['st'] is None and r['act'] is None and k > 10): seen = r; break
        seen = r
    pg.screenshot(path=str(OUT / f'{W}x{H}-{hr}.png'), timeout=120000)
    ev("typeof deviceClose === 'function' && deviceClose()"); step(3)
    pg.screenshot(path=str(OUT / f'{W}x{H}-{hr}-closed.png'), timeout=120000)
    print(f'{W}x{H} {hr}:00 result:', json.dumps(seen)); print('  errors:', errs[:3]); b.close()
with sync_playwright() as pw:
    for W, H in ((320, 640), (390, 844)):
        for hr in HOURS: run(pw, W, H, hr)
