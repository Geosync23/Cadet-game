# DR1: the same scripted session in two builds, three ways (no switch, #debug, ?nosave), starting from the same real save:
# the storage each build leaves must be byte-identical (the career's random gs zeroed: Date.now ^ Math.random)
import sys, os, re, json, pathlib
os.environ.setdefault('CADET_CHROME','/opt/pw-browsers/chromium')
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("class Game")[0])
from playwright.sync_api import sync_playwright
A, B = sys.argv[1], sys.argv[2]
def run(pw, game, suffix, seed):
    tmp = WORK / 'test' / ('_dr1_cmp_' + pathlib.Path(game).name); tmp.write_text(instrument(pathlib.Path(game).read_text()))
    b = pw.chromium.launch(executable_path=os.environ['CADET_CHROME'], args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width':390,'height':844})
    if seed is not None: ctx.add_init_script("if (!sessionStorage.getItem('seeded')) { sessionStorage.setItem('seeded','1'); localStorage.clear(); const s = " + json.dumps(seed) + "; for (const k in s) localStorage.setItem(k, s[k]); }")
    pg = ctx.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)[:150]))
    pg.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
    pg.add_init_script(INIT); pg.goto('file://' + str(tmp) + suffix)
    pg.wait_for_function('window.__sc !== undefined', timeout=90000)
    ev = lambda s: pg.evaluate('s => window.__sc(s)', s)
    ev("(() => { renderer.render = () => {}; })()")
    pg.evaluate('window.__step(120, 33)'); ev("(skipTo(shipNow() + 200), saveGame(), 0)"); pg.evaluate('window.__step(60, 33)'); ev("saveGame()")
    st = pg.evaluate('() => Object.fromEntries(Object.keys(localStorage).map(k => [k, localStorage.getItem(k)]))')
    info = ev("({ NOSAVE, DEBUG, key: typeof SAVE_KEY !== 'undefined' ? SAVE_KEY : null, ik: INTRO_KEY, dm: typeof DEVMODE !== 'undefined' ? DEVMODE : 'n/a', clock: clockText() })")
    b.close()
    def norm(v):
        try: j = json.loads(v)
        except Exception: return v
        if isinstance(j, dict) and isinstance(j.get('ship'), dict) and isinstance(j['ship'].get('career'), dict): j['ship']['career']['gs'] = 0
        return json.dumps(j, sort_keys=True)
    return {k: norm(v) for k, v in st.items()}, info, errs
with sync_playwright() as pw:
    # a real save to start from: made by build A with no switch
    seed, _, _ = run(pw, A, '', None)
    raw = {k: v for k, v in seed.items()}; raw['starship-cadet-arrived'] = '1'
    print('seed keys', sorted(raw), 'save bytes', len(raw.get('starship-cadet-save', '')))
    rd, idd, ed = run(pw, B, '#dev', raw); print('#dev on B: real keys unchanged =', all(rd.get(k) == raw[k] or (k == 'starship-cadet-save' and rd.get(k) == json.dumps(json.loads(raw[k]), sort_keys=True)) for k in raw), 'keys', sorted(rd), idd, ed[:1])
    for suffix in ('', '#debug'):
        ra, ia, ea = run(pw, A, suffix, raw); rb, ib, eb = run(pw, B, suffix, raw)
        same = ra == rb
        diff = [k for k in set(ra) | set(rb) if ra.get(k) != rb.get(k)]
        print(f"{suffix or '(none)':14} identical={same} keys A={sorted(ra)} B={sorted(rb)} diff={diff} infoA={ia} infoB={ib} errs={ea[:1]}{eb[:1]}")
        if diff:
            for k in diff[:2]:
                a, b2 = ra.get(k) or '', rb.get(k) or ''
                i = next((n for n in range(min(len(a), len(b2))) if a[n] != b2[n]), None); print('   first diff at', i, a[max(0,(i or 0)-80):(i or 0)+80], '|', b2[max(0,(i or 0)-80):(i or 0)+80])
