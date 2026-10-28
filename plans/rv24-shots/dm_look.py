# RV24: DM1's Dev mode J0 at 390x844 with #dev, by taps: the panel, the Jump to tab, Set career to Day 36 (progress, Stop, landing),
# By rank. Usage: python3 dm_look.py BUILD.html OUTDIR
import sys, os, re, json, time
G = sys.argv[1]; OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
exec(open(os.path.join(os.path.dirname(os.path.abspath(G)), 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
src = open(G).read(); i = src.rfind('})();'); vp = WORK / 'test' / '_rv24_dm.html'; vp.write_text(src[:i] + "window.__sc = src => eval(src);\n" + src[i:])
with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    pg = br.new_page(viewport={'width': 390, 'height': 844}); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
    pg.goto('file://' + str(vp) + '#dev'); pg.wait_for_function('window.__sc !== undefined', timeout=120000)
    ev = lambda s: pg.evaluate('s => window.__sc(s)', s)
    pg.wait_for_timeout(1500)
    if pg.locator('text=Sign and go aboard').count(): pg.fill('form input', 'Ada'); pg.click('text=Sign and go aboard'); pg.wait_for_timeout(1500)
    print('dev', ev("DEVMODE"))
    pg.click('.hud'); pg.wait_for_timeout(500); print('panel open', ev("DM_UI.open"))
    def tab(name): pg.click(f'#dmSheet .dmTabs button:has-text("{name}")'); pg.wait_for_timeout(400)
    tab('Jump to'); pg.screenshot(path=f'{OUT}/dm_jump.png'); print('jump tab', ev("document.getElementById('dmSheet').innerText.slice(0, 400)"))
    tab('Set career'); pg.screenshot(path=f'{OUT}/dm_set.png'); print('set tab', ev("document.getElementById('dmSheet').innerText.slice(0, 600)"))
    print('buttons', ev("[...document.querySelectorAll('#dmSheet button')].map(b => b.textContent.trim()).filter(Boolean).slice(0, 60)"))
    # Set career to Day 36: pick 36 then Set (the panel's own way, whatever its control is)
    ok = ev("""(() => { const bs = [...document.querySelectorAll('#dmSheet button')]; const b = bs.find(x => /^(Day )?36$/.test(x.textContent.trim())); if (b) { b.click(); return 'day button'; } return 'no day 36 button'; })()""")
    print('pick 36', ok); pg.wait_for_timeout(300); print('after pick', ev("document.getElementById('dmSheet').innerText.slice(0, 300)"))
    t0 = time.time()
    for k in range(2):
        b = ev("""(() => { const bs = [...document.querySelectorAll('#dmSheet button')]; const b = bs.find(x => /^(Set career|Set|Again)/.test(x.textContent.trim())); if (b) { b.click(); return b.textContent.trim(); } return null; })()"""); print('press', b); pg.wait_for_timeout(300)
    pg.wait_for_timeout(1500); pg.screenshot(path=f'{OUT}/dm_running.png'); print('running', ev("[!!DM_UI.run, document.getElementById('dmSheet').innerText.slice(0, 300)]"))
    for k in range(240):
        pg.wait_for_timeout(1000)
        if not ev("!!DM_UI.run"): break
    print('run took', round(time.time() - t0), 's')
    pg.screenshot(path=f'{OUT}/dm_landed.png'); print('landed', ev("[clockText(), SHIP.works && SHIP.works.rank, SHIP.works && JSON.stringify(SHIP.works.ms), document.getElementById('dmSheet').innerText.slice(0, 500)]"))
    print('errors', errs[:5]); br.close()
