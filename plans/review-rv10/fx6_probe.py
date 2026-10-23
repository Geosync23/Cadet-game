# RV10 probe: FX6 showers/basin with real taps at phone sizes, and a changing-room rinse before a real shower
import sys, os, re, pathlib, json
GAME, CT, OUT = sys.argv[1], sys.argv[2], pathlib.Path(sys.argv[3]); OUT.mkdir(parents=True, exist_ok=True)
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
    pg.add_style_tag if False else None
    ev = lambda s: pg.evaluate('s => window.__sc(s)', s)
    def step(n):
        pg.evaluate('s => { if (window.__skip === undefined && window.__sc) window.__sc(s); }', SKIP_SWITCH)
        if n > 1: pg.evaluate(f'window.__skip = true; window.__step({n - 1}, 33); window.__skip = false')
        pg.evaluate('window.__step(1, 33)')
    pg.goto('file://' + str(TMP) + '?nosave'); pg.wait_for_function('window.__sc !== undefined', timeout=120000)
    pg.add_style_tag(content='*,*::before,*::after{transition:none!important;animation:none!important}')
    step(20)
    ev("newGameStart(false); introSkip()"); step(20); ev("skipTo(14 * 60)"); step(30)
    if ev('deckDef.num') != 4: ev('goToDeck(4)'); step(20)
    def go_near(pid):
        step(10)
    def tap_item(pid):   # the shower/basin item nearest the place, tapped on screen
        xy = ev(f"""(() => {{ const s = placeSpot('{pid}'); let best = null, bd = 9;
          for (const it of ITEMS) {{ if (!/^shower$/i.test(it.t) || !it.hit) continue; const p = new THREE.Vector3(); it.hit.getWorldPosition(p); const d = Math.hypot(p.x - s.x, p.z - s.z); if (d < bd) {{ bd = d; best = [it, p]; }} }}
          if (!best) return null; const v = best[1].clone(); v.y = Math.max(.5, v.y); v.project(camera); return [ (v.x + 1) * innerWidth / 2, (1 - v.y) * innerHeight / 2, best[0].t ]; }})()""")
        if not xy: return None
        pg.touchscreen.tap(xy[0], xy[1]); return xy
    def finish():
        for _ in range(120):
            step(15)
            if ev("!ACT"): break
        step(5)
    def read(tag):
        r = ev("(() => ({ hyg: Math.round(SHIP.player.needs.hygiene * 10) / 10, wash: SHIP.player.wash, tx: (document.getElementById('tx') || {}).textContent || '', clock: clockText(), act: ACT ? ACT.kind : null }))()")
        pg.screenshot(path=str(OUT / f'{W}x{H}-{tag}.png'), timeout=120000); print(f'{W}x{H} {tag}:', json.dumps(r)[:400]); return r
    sp = ev("(() => { const L = [...PLACE_OF.values()].filter(pl => pl.type === 'shower' && !(PRIVATE_TYPES.has(pl.type) && privatePlace(pl)) && (deckDef.places || []).includes(pl)); return L.map(pl => pl.id); })()")
    print('public showers on deck 4:', sp); SP = sp[0]
    go_near(SP)
    ev("SHIP.player.needs.hygiene = 30; SHIP.player.wash = washLoad(null)")
    print('playerTap', ev(f"(() => {{ const s = placeSpot('{SP}'); const it = ITEMS.filter(i => /^shower$/i.test(i.t) && i.hit).map(i => {{ const p = new THREE.Vector3(); i.hit.getWorldPosition(p); return [i, p]; }}).sort((a, b) => Math.hypot(a[1].x - s.x, a[1].z - s.z) - Math.hypot(b[1].x - s.x, b[1].z - s.z))[0]; return playerTap(it[0], it[1].clone(), it[1].clone()); }})()")); step(5); ev_act = ev("ACT && ACT.kind"); print('  act after tap:', ev_act)
    finish(); read('shower1')
    ev("SHIP.player.needs.hygiene = 40"); go_near(SP)
    print('tap', tap_item(SP)); step(5); print('  act after tap:', ev("ACT && ACT.kind")); finish(); read('shower2-cooling')
    # a changing-room rinse (the rec deck's automatic recShower after a swim) first, then the Deck 4 shower
    ev("SHIP.player.wash = washLoad(null); SHIP.player.needs.hygiene = 30; actStart('recShower', null, { title: 'Changing rooms', spot: placeSpot('" + SP + "') })")
    finish(); read("after-rinse")
    go_near(SP); print('tap', tap_item(SP)); step(5); print('  act after tap:', ev("ACT && ACT.kind")); finish(); read('shower-after-rinse')
    print(f'{W}x{H} errors:', errs[:5]); b.close()
with sync_playwright() as pw:
    for W, H in ((320, 640), (390, 844)): run(pw, W, H)
