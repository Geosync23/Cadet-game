# RV30 probe (note 9): the real game loop (real requestAnimationFrame, no test clock), a real hidden tab: a second tab
# brought to the front, then back; and a real freeze (CDP Page.setWebLifecycleState). Prints the sound's state and
# whether frames were drawn while hidden. Usage: CADET_WORK=... python3 hide_real.py BUILD
import sys, os, re, pathlib, time
from playwright.sync_api import sync_playwright
WORK = pathlib.Path(os.environ.get('CADET_WORK', '/tmp/cadet-work'))
THREE = (WORK / 'three/package/build/three.min.js').read_text()
src = pathlib.Path(sys.argv[1]).read_text(); i = src.rfind('})();'); src = src[:i] + "window.__sc = s => eval(s);\n" + src[i:]
tmp = WORK / 'test' / f'_rv30_hide_{os.getpid()}.html'; tmp.write_text(src)
FR = "(() => { window.__fr = 0; const f = () => { window.__fr++; requestAnimationFrame(f); }; requestAnimationFrame(f); })()"
with sync_playwright() as pw:
    b = pw.chromium.launch(headless=os.environ.get('HEADED') != '1', executable_path=os.environ.get('CADET_CHROME'), args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--autoplay-policy=no-user-gesture-required'])
    ctx = b.new_context(viewport={'width': 900, 'height': 700}); p = ctx.new_page()
    errs = []; p.on('pageerror', lambda e: errs.append(str(e)))
    p.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
    p.goto('file://' + str(tmp) + '?nosave&debug&sound'); p.wait_for_function('window.__sc !== undefined', timeout=90000)
    p.wait_for_timeout(4000); p.mouse.click(450, 380); p.wait_for_timeout(3000)
    st = lambda: p.evaluate("() => [document.visibilityState, window.__sc('SND._.state()'), window.__sc('PAUSE.on'), window.__fr]")
    p.evaluate(FR); p.wait_for_timeout(500)
    print('start      ', st())
    # 1. a real hidden tab: another tab to the front
    cdp = ctx.new_cdp_session(p); wid = cdp.send('Browser.getWindowForTarget')['windowId']
    p.evaluate("() => { window.__vis = []; document.addEventListener('visibilitychange', () => setTimeout(() => window.__vis.push([document.visibilityState, window.__sc('SND._.state()')]), 300)); }")
    cdp.send('Browser.setWindowBounds', {'windowId': wid, 'bounds': {'windowState': 'minimized'}})
    f0 = p.evaluate('window.__fr'); time.sleep(2.5); s = st(); print('minimised 2.5 s', s, 'frames while hidden', s[3] - f0)
    cdp.send('Browser.setWindowBounds', {'windowId': wid, 'bounds': {'windowState': 'normal'}}); p.wait_for_timeout(1500)
    print('back       ', st(), 'states 0.3 s after each change', p.evaluate('window.__vis'))
    p.evaluate("window.__sc('pauseSet(false)')"); p.wait_for_timeout(1500); print('resumed    ', st())
    # 2. a real freeze (what Android does to a background tab), then thaw
    p.evaluate("() => { window.__th = null; document.addEventListener('resume', () => { window.__th = window.__sc('SND._.state()'); }); }")
    try:
        cdp.send('Page.enable'); cdp.send('Page.setWebLifecycleState', {'state': 'frozen'}); time.sleep(1.5)
        cdp.send('Page.setWebLifecycleState', {'state': 'active'}); p.wait_for_timeout(300); print('after freeze', st(), 'sound at thaw (before any frame)', p.evaluate('window.__th'))
    except Exception as e: print('freeze: CDP refused', e)
    print('page errors', errs[:3]); b.close()
tmp.unlink(missing_ok=True)
