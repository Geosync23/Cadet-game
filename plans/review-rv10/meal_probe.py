# RV10 probe: FX7's mess taps (LEAD31-9) with touch taps at phone sizes, Day 1 dinner on Deck 3:
# a second tap on your seat mid-meal; walking away mid-meal then another seat; the needs strip open then a deck tap
import sys, os, re, pathlib, json
GAME, CT = sys.argv[1], sys.argv[2]
exec(open(CT + '/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
TMP = WORK / 'test' / ('_rv10_' + pathlib.Path(GAME).name); TMP.write_text(instrument(pathlib.Path(GAME).read_text()))
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
    pg.goto('file://' + str(TMP) + '?nosave'); pg.wait_for_function('window.__sc !== undefined', timeout=120000)
    pg.add_style_tag(content='*,*::before,*::after{transition:none!important;animation:none!important}')
    step(10); ev("newGameStart(false); introSkip()"); step(10)
    ev("(() => { goToDeck(3); setShipNow((SHIP.time.day - 1) * 1440 + 19 * 60 + 20); deckCrewFill(); if (typeof GUIDE_ON !== 'undefined' && GUIDE_ON) { GUIDE.tq.length = 0; } })()"); step(30)
    # a free mess seat near the middle of the screen, the player 2 m from it
    seat = ev("""(() => { const L = [...PLACE_OF.values()].filter(pl => pl.type === 'mess-seat' && !heldBy(pl.id) && (deckDef.places || []).includes(pl)); const pl = L[Math.floor(L.length / 2)]; const s = placeSpot(pl.id);
      const c = nearestOpen(s.x + 1.5, s.z + 1.5, player); player.obj.position.copy(cellPos(...c)); player.stop(); SHIP.player.tray = 'Stew'; SHIP.player.trayLeft = 0; SHIP.player.needs.hunger = 30; return pl.id; })()""")
    step(60)
    def scr(pid, y=.5):
        return ev(f"(() => {{ const s = placeSpot('{pid}'), v = new THREE.Vector3(s.x, {y}, s.z).project(camera); return [(v.x + 1) * innerWidth / 2, (1 - v.y) * innerHeight / 2]; }})()")
    st = lambda: ev("({ act: ACT && ACT.kind, ph: ACT && ACT.phase, place: ACT && ACT.placeId, done: ACT && Math.round(ACT.done), mins: ACT && Math.round(ACT.def.mins), tray: SHIP.player.tray, left: Math.round(SHIP.player.trayLeft || 0), food: Math.round(SHIP.player.needs.hunger), tx: document.getElementById('tx').textContent.slice(0, 90) })")
    x, y = scr(seat); pg.touchscreen.tap(x, y)
    for _ in range(20): step(30)
    r1 = st(); print(f'{W}x{H} seat {seat} tapped:', r1)
    # (1) the same seat again mid-meal
    x, y = scr(seat); pg.touchscreen.tap(x, y); step(20); r2 = st(); print('  second tap on it:', r2)
    # (2) walk away (a floor tap 3 m off), then another free seat
    away = ev("(() => { const p = player.obj.position, c = nearestOpen(p.x + 3, p.z + 2, player), w = cellPos(...c), v = new THREE.Vector3(w.x, 0, w.z).project(camera); return [(v.x + 1) * innerWidth / 2, (1 - v.y) * innerHeight / 2]; })()")
    pg.touchscreen.tap(away[0], away[1]); step(30); r3 = st(); print('  walked away:', r3)
    seat2 = ev(f"(() => {{ const L = [...PLACE_OF.values()].filter(pl => pl.type === 'mess-seat' && pl.id !== '{seat}' && !heldBy(pl.id) && (deckDef.places || []).includes(pl)); const p = player.obj.position; L.sort((a, b) => {{ const s = placeSpot(a.id), t = placeSpot(b.id); return Math.hypot(s.x - p.x, s.z - p.z) - Math.hypot(t.x - p.x, t.z - p.z); }}); return L[0].id; }})()")
    x, y = scr(seat2); pg.touchscreen.tap(x, y); step(5)
    if ev("!ACT || ACT.placeId !== '" + seat2 + "'"): print('   (seat tap missed; starting it as a seat tap does)'); ev(f"actStart('sit', '{seat2}')")
    log = []
    for _ in range(80):
        step(30); c = st(); held = ev(f"(() => {{ const a = heldBy('{seat2}'); return a ? a.p.id : null; }})()"); log.append([c['act'], c['ph'], c['place'], c['done'], c['mins'], c['tray'], c['left'], held, c['tx'][:60]])
        if ev("!ACT"): break
    dd = []; [dd.append(x) for x in log if not dd or dd[-1] != x]; print('   trace:', dd[:12])
    r4 = st(); print('  finished at', seat2, ':', r4)
    # (3) the needs strip open, then a deck tap
    ns = ev("(() => { const el = document.getElementById('needStrip'); if (!el) return null; if (SHIP.player.stripFold) stripFold(false); const r = el.getBoundingClientRect(); return [r.x + r.width / 2, r.y + r.height / 2]; })()")
    if ns:
        pg.touchscreen.tap(ns[0], ns[1]); step(5); op = ev("document.getElementById('needStrip').classList.contains('open')")
        pg.touchscreen.tap(W / 2, H * .6); step(10)
        print('  needs strip opened', op, '-> after a deck tap open', ev("document.getElementById('needStrip').classList.contains('open')"), '| walking', ev("player.path.length > 0 || !!ACT"))
    print('  errors:', errs[:3]); b.close()
with sync_playwright() as pw:
    for W, H in ((320, 640), (390, 844)): run(pw, W, H)
