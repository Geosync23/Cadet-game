# RV28: player_check's Saving start alone: a v 1 save planted, the page loaded, the needs read; console errors kept.
import sys, os, re, json, pathlib
WT, BUILD = sys.argv[1], sys.argv[2]
exec(open(WT + '/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    tmp = WORK / 'test' / ('_rv28_save_' + str(os.getpid()) + '.html'); tmp.write_text(instrument(pathlib.Path(BUILD).read_text()))
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    page = b.new_page(viewport={'width': 600, 'height': 500}); errs = []
    page.on('console', lambda m: m.type in ('error', 'warning') and errs.append(m.type + ': ' + m.text[:300]))
    page.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)[:400]))
    page.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
    page.add_init_script(INIT)
    url = 'file://' + str(tmp)
    def load():
        page.goto(url); page.wait_for_function('window.__sc !== undefined', timeout=60000)
        return lambda s: page.evaluate('s => window.__sc(s)', s)
    ev = load()
    ev("localStorage.setItem(SAVE_KEY, JSON.stringify({ v: 1, build: '0.25.2', time: { day: 2, min: 600 }, player: { deck: 4, tile: [7, 3], facing: 0 }, ship: { decks: {} }, crew: {} })); Storage.prototype.setItem = () => {}")
    ev = load()
    print('v1 load:', ev("JSON.stringify([SHIP.time.day, SHIP.player.needs, typeof SAVED !== 'undefined' ? !!SAVED : 'n/a', typeof STORIES2_ON !== 'undefined' ? STORIES2_ON : 'n/a'])"))
    print('errors:', errs[:6])
    # where does loading fail? try the load step by step if there's a loader
    print('loader:', ev("(() => { const f = ['loadGame', 'loadSave', 'restoreSave'].filter(n => { try { return typeof eval(n) === 'function'; } catch (e) { return false; } }); return f.join(','); })()"))
    b.close()
