# RV10 probe: DV1's Dev career arrow at phone sizes, with real taps on the Dev panel; later career steps via Set career
import sys, os, re, pathlib, json, time
GAME, CT, OUT = sys.argv[1], sys.argv[2], pathlib.Path(sys.argv[3]); OUT.mkdir(parents=True, exist_ok=True)
exec(open(CT + '/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
TMP = WORK / 'test' / '_rv10_dv.html'; TMP.write_text(instrument(pathlib.Path(GAME).read_text()))
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
    def ready():
        pg.wait_for_function('window.__sc !== undefined', timeout=120000)
        pg.add_style_tag(content='*,*::before,*::after{transition:none!important;animation:none!important}')
        step(20)
    pg.goto('file://' + str(TMP) + '#dev'); ready()
    if pg.locator('text=Sign and go aboard').count():
        pg.fill('form input', 'Ada'); pg.locator('text=Sign and go aboard').tap(); step(30)
    def arrow(tag):
        step(10)
        r = ev("(() => { const e = document.getElementById('dmArrow'); const l = e && e.querySelector('.dvlab'); const W = SHIP.works; return { hidden: e ? e.hidden : 'none', label: l ? l.textContent : null, box: l && !e.hidden ? l.getBoundingClientRect().toJSON() : null, clock: clockText(), deck: deckDef.num, cur: W && W.cur ? W.cur.id + ':' + W.cur.st : null, tr: W ? Object.keys(W.tr).join(',') : null, tier: W ? W.tier : null, test: W ? W.test : null, game: (() => { const g = document.getElementById('ixGoal'); return g && !g.hidden ? g.textContent : null; })() }; })()")
        pg.screenshot(path=str(OUT / f'{W}x{H}-{tag}.png'), timeout=120000)
        print(f'{W}x{H} {tag}:', json.dumps(r)); return r
    arrow('arrival')
    def setday(label_btn, beat=False):
        pg.locator('.hud').first.tap(); step(3)
        pg.locator('#dmSheet .dmTabs button[data-tab="set"]').tap(); step(3)
        if not beat:
            pg.locator(f'#dmSheet button:text-is("{label_btn}")').first.tap(); step(3)
            btn = pg.locator('#dmSheet button', has_text=re.compile(r'^Set career to Day'))
        else:
            btn = pg.locator(f'#dmSheet button:text-is("{label_btn}")')
        btn.first.tap(); step(3)
        try:
            with pg.expect_navigation(timeout=15000): pg.locator('#dmSheet button', has_text='Tap again').first.tap()
            ready()
        except Exception as e:
            print('  (no reload)', str(e)[:80]); step(10)
        if ev('DM_UI.open'): pg.locator('#dmSheet .dmClose').tap(); step(3)
    for d in ('Day 2', 'Day 5', 'Day 8'):
        setday(d); arrow(d.replace(' ', ''))
        ev("devmodeSkipTo(Math.floor(shipNow()) + 150)"); arrow(d.replace(' ', '') + '+2h30')
    setday('Day 9: the test job', beat=True); arrow('beat-t2')
    # the arrow takes no taps: element at the label's centre is not the dev arrow
    hit = ev("(() => { const l = document.querySelector('#dmArrow .dvlab'); if (!l || document.getElementById('dmArrow').hidden) return 'hidden'; const r = l.getBoundingClientRect(); const e = document.elementFromPoint(r.x + r.width / 2, r.y + r.height / 2); return e ? (e.closest('#dmArrow') ? 'DEV ARROW TAKES TAPS' : e.tagName + '#' + e.id) : 'none'; })()")
    print(f'{W}x{H} tap-through:', hit)
    print(f'{W}x{H} errors:', errs[:5])
    b.close()
with sync_playwright() as pw:
    for W, H in ((320, 640), (390, 844)): run(pw, W, H)
