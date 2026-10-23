import sys, os, json
BUILD = sys.argv[1]; sys.argv = [sys.argv[0], BUILD]
exec(open('arrows_check.py').read().split("GUIDE = 'guide' in")[0]); GUIDE = False
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
    for mode in ['first', 'off']:
        pg = Page(ctx, BUILD); real_game(pg, 2); pg.ev(f"SHIP.device.settings.teach = '{mode}'")
        pg.ev("devmodeSkipTo(1440 + 8 * 60 + 1); goToDeck(5)"); pg.step(30)
        r = pg.ev("""(() => { const out = []; for (let i = 0; i < 5; i++) { guideShift(); out.push([POINT_Q.map(p => p.id), typeof pointNow === 'function' ? pointNow() : null, !!(POINT.el && !POINT.el.hidden && POINT.el.isConnected)]); } return out; })()""")
        pg.step(30)
        r2 = pg.ev("[POINT_Q.map(p => p.id), pointNow(), !!(POINT.el && !POINT.el.hidden && POINT.el.isConnected), (goalNow() || {}).label]")
        print(mode, r[-1], r2)
        pg.page.close()
