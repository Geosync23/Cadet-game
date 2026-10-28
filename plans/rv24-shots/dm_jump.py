# RV24: Dev mode jumps by taps at 390x844 with #dev: Jump to tab, a group, Go twice on a jump, the landing.
# Usage: python3 dm_jump.py BUILD.html OUTDIR 'Group:label part' ...
import sys, os, re, json, time
G = sys.argv[1]; OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
exec(open(os.path.join(os.path.dirname(os.path.abspath(G)), 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
src = open(G).read(); i = src.rfind('})();'); vp = WORK / 'test' / '_rv24_dmj.html'; vp.write_text(src[:i] + "window.__sc = src => eval(src);\n" + src[i:])
with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    pg = br.new_page(viewport={'width': 390, 'height': 844}); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
    pg.goto('file://' + str(vp) + '#dev'); pg.wait_for_function('window.__sc !== undefined', timeout=120000)
    ev = lambda s: pg.evaluate('s => window.__sc(s)', s)
    pg.wait_for_timeout(1500)
    if pg.locator('text=Sign and go aboard').count(): pg.fill('form input', 'Ada'); pg.click('text=Sign and go aboard'); pg.wait_for_timeout(1500)
    pg.click('.hud'); pg.wait_for_timeout(500)
    for arg in sys.argv[3:]:
        grp, lab = arg.split(':', 1)
        if not ev("DM_UI.open"): pg.click('.hud'); pg.wait_for_timeout(500)
        pg.click('#dmSheet .dmTabs button:has-text("Jump to")'); pg.wait_for_timeout(300)
        pg.click(f'#dmSheet .dmGroups button:has-text("{grp}")'); pg.wait_for_timeout(300)
        b = pg.locator(f'#dmSheet .dmJump:has-text("{lab}") button'); print(arg, 'found', b.count())
        if not b.count(): continue
        t0 = time.time(); b.first.click(); pg.wait_for_timeout(300); b = pg.locator(f'#dmSheet .dmJump:has-text("{lab}") button'); b.first.click(); pg.wait_for_timeout(1500)
        for k in range(240):
            if not ev("!!DM_UI.run"): break
            pg.wait_for_timeout(1000)
        print('  took', round(time.time() - t0), 's; landed', ev("[clockText(), deckDef.num, (ROOMS[roomAt(...player.here())] || {}).name, SHIP.works && SHIP.works.rank, typeof goalNow === 'function' && (goalNow() || {}).label]"))
        print('  says', ev("(document.getElementById('dmSheet').innerText.match(/(career set to[^\\n]*|[^\\n]*career set to[^\\n]*)/i) || [''])[0].slice(0, 300)"))
        if ev("DM_UI.open"): pg.click('#dmSheet .dmTabs button:has-text("Quick")'); pg.wait_for_timeout(200)
        pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
        for k in range(20): pg.evaluate('window.__step && window.__step(10, 33)') if False else pg.wait_for_timeout(100)
        pg.screenshot(path=f'{OUT}/dmj_{re.sub("[^a-z0-9]+", "_", lab.lower())[:30]}.png')
    print('errors', errs[:5]); br.close()
