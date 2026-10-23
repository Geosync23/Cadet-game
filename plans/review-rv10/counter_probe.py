# RV10 probe: FX7's counter taps in a real crowd (LEAD31-9 (4)): at several dinner minutes and four camera turns, points
# on the servery counter with someone near on screen; just before each tap, record whether the point is on a person then;
# tap (touch, 390x844); the result: queue, a crew card, or other
import sys, os, re, pathlib, json
GAME, CT = sys.argv[1], sys.argv[2]
exec(open(CT + '/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
TMP = WORK / 'test' / ('_rv10_' + pathlib.Path(GAME).name); TMP.write_text(instrument(pathlib.Path(GAME).read_text()))
ONTHEM = "((x, y) => { const near = crewAtScreen(x, y); if (!near) return null; const on = [.5, 1, 1.4].some(hy => { _cp.set(near.x, near.y + hy, near.z).project(camera); return Math.hypot((_cp.x + 1) / 2 * innerWidth - x, (1 - _cp.y) / 2 * innerHeight - y) < CREW_ON_PX; }); return on ? 'on' : 'near'; })"
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1, has_touch=True, is_mobile=True)
    pg = ctx.new_page(); pg.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript')); pg.add_init_script(INIT)
    ev = lambda s: pg.evaluate('s => window.__sc(s)', s)
    def step(n):
        pg.evaluate('s => { if (window.__skip === undefined && window.__sc) window.__sc(s); }', SKIP_SWITCH)
        if n > 1: pg.evaluate(f'window.__skip = true; window.__step({n - 1}, 33); window.__skip = false')
        pg.evaluate('window.__step(1, 33)')
    pg.goto('file://' + str(TMP) + '?nosave'); pg.wait_for_function('window.__sc !== undefined', timeout=120000)
    step(10); ev("newGameStart(false); introSkip()"); step(10)
    res = {'queue': 0, 'card_on': 0, 'card_near': 0, 'other_on': 0, 'other': 0}; ex = []
    for mins in (18 * 60 + 5, 18 * 60 + 25, 18 * 60 + 45, 19 * 60 + 5):
        ev(f"(() => {{ goToDeck(3); setShipNow((SHIP.time.day - 1) * 1440 + {mins}); deckCrewFill(); if (typeof GUIDE_ON !== 'undefined' && GUIDE_ON) {{ GUIDE.tq.length = 0; guideToast = () => false; }} window.__sv = ITEMS.find(i => /^servery$/i.test(i.t)); }})()"); step(60)
        for turn in range(4):
            ev("(() => { actEnd(true); SHIP.player.tray = null; const b = new THREE.Box3().setFromObject(__sv.hit), c = nearestOpen(b.min.x - 3, (b.min.z + b.max.z) / 2 + 2, player); player.obj.position.copy(cellPos(...c)); player.stop(); })()"); step(40)
            pts = ev("""(() => { const b = new THREE.Box3().setFromObject(__sv.hit), out = [];
              for (const fz of [.1, .3, .5, .7, .9]) for (const fy of [.6, 1]) for (const fx of [0, .5]) { const v = new THREE.Vector3(b.min.x + (b.max.x - b.min.x) * fx, b.max.y * fy, b.min.z + (b.max.z - b.min.z) * fz).project(camera), q = [(v.x + 1) / 2 * innerWidth, (1 - v.y) / 2 * innerHeight];
                if (!(q[0] > 10 && q[0] < 380 && q[1] > 140 && q[1] < 780)) continue; const h = pick(q[0], q[1]); if (!h || h.object.userData.item !== __sv || !crewAtScreen(q[0], q[1])) continue; out.push(q); }
              return out.slice(0, 4); })()""")
            for x, y in pts:
                ev("actEnd(true); player.stop(); SHIP.player.tray = null"); step(2)
                st = ev(f"({ONTHEM})({x}, {y})"); pg.touchscreen.tap(x, y); step(6)
                a = ev("ACT && ACT.kind"); card = ev("(() => { const d = document.getElementById('devDlg'); return !!(d && !d.hidden); })()")
                if card: ev("devDialogueDo && devDialogueDo('close')")
                k = 'queue' if a == 'queue' else ('card_' + ('on' if st == 'on' else 'near')) if card else ('other_on' if st == 'on' else 'other')
                res[k] += 1
                if k not in ('queue', 'card_on'): ex.append([mins, turn, round(x), round(y), st, a, card])
            ev("actEnd(true)"); pg.locator('#rot').tap(); step(80)
    print(json.dumps(res), ex[:8]); b.close()
