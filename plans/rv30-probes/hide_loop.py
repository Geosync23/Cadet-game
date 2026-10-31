# RV30 probe (note 9), the real game loop (real requestAnimationFrame and clock, not the test clock). This container's
# browsers never really hide a tab (tried: another tab, minimised window, CDP freeze), so the hide is played: document.hidden
# true, the event, and from then on no frame is drawn (the game's frame callbacks are held, as a hidden page gets none).
# Cases: visibilitychange, pagehide, freeze; and the race: the page hides in the same frame the sound was asked to resume.
import sys, os, re, pathlib, time
from playwright.sync_api import sync_playwright
WORK = pathlib.Path(os.environ.get('CADET_WORK', '/tmp/cadet-work'))
THREE = (WORK / 'three/package/build/three.min.js').read_text()
src = pathlib.Path(sys.argv[1]).read_text(); i = src.rfind('})();'); src = src[:i] + "window.__sc = s => eval(s);\n" + src[i:]
tmp = WORK / 'test' / f'_rv30_loop_{os.getpid()}.html'; tmp.write_text(src)
INIT = """(() => { const raf = window.requestAnimationFrame.bind(window); const held = []; window.__hold = false; window.__fr = 0;
  const go = cb => raf(t => { if (window.__hold) { held.push(cb); return; } window.__fr++; cb(t); }); window.requestAnimationFrame = cb => window.__hold ? (held.push(cb), 0) : go(cb);
  window.__release = () => { window.__hold = false; held.splice(0).forEach(cb => go(cb)); }; })()"""
HIDE = """how => { Object.defineProperty(document, 'hidden', { configurable: true, get: () => true }); Object.defineProperty(document, 'visibilityState', { configurable: true, get: () => 'hidden' });
  window.__hold = true; (how === 'pagehide' ? window : document).dispatchEvent(new Event(how)); }"""
UNHIDE = "() => { delete document.hidden; delete document.visibilityState; document.dispatchEvent(new Event('visibilitychange')); window.__release(); }"
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME'), args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--autoplay-policy=no-user-gesture-required'])
    p = b.new_page(viewport={'width': 900, 'height': 700}); errs = []; p.on('pageerror', lambda e: errs.append(str(e)))
    p.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
    p.add_init_script(INIT)
    p.goto('file://' + str(tmp) + '?nosave&debug&sound'); p.wait_for_function('window.__sc !== undefined', timeout=90000)
    p.wait_for_timeout(4000); p.mouse.click(450, 380); p.wait_for_timeout(3000)
    st = lambda: p.evaluate("() => [window.__sc('SND._.state()'), window.__sc('PAUSE.on'), window.__fr]")
    def play():
        p.evaluate("window.__sc('pauseSet(false)')")
        for _ in range(40):
            if st()[0] == 'running': return True
            p.wait_for_timeout(250)
        return False
    for how in ['visibilitychange', 'pagehide', 'freeze']:
        print(how, 'playing before:', play(), st())
        p.evaluate(f"({HIDE})('{how}')"); f0 = st()[2]; p.wait_for_timeout(1500); s = st()
        print(f'  hidden 1.5 s, no frames ({s[2] - f0} drawn): sound {s[0]}, paused {s[1]}')
        p.evaluate(UNHIDE); p.wait_for_timeout(2000); print('  back:', st())
    # the race: the game is resumed, and the page hides in the very frame the sound's resume was asked for
    p.evaluate("window.__sc('pauseSet(true)')"); p.wait_for_timeout(1500); print('race: paused first', st())
    p.evaluate(f"""() => {{ window.__sc('pauseSet(false)'); requestAnimationFrame(() => requestAnimationFrame(() => {{ window.__r = window.__sc('SND._.state()'); ({HIDE})('visibilitychange'); }})); }}""")
    p.wait_for_timeout(2500); s = st(); print(f'  hidden right after the resume was asked (state then {p.evaluate("window.__r")}): sound {s[0]}, paused {s[1]}')
    p.evaluate(UNHIDE); p.wait_for_timeout(1500)
    # the race, in flight: the page hides straight after ctx.resume() was called, before it has finished
    p.evaluate("window.__sc('pauseSet(true)')"); p.wait_for_timeout(1500); print('race 2: paused first', st())
    p.evaluate(f"""() => {{ const c = window.__sc('SND.ctx'), r = c.resume.bind(c); c.resume = () => {{ const pr = r(); window.__r = c.state; ({HIDE})('visibilitychange'); c.resume = r; return pr; }}; window.__sc('pauseSet(false)'); }}""")
    p.wait_for_timeout(2500); s = st(); print(f'  hidden while the resume was in flight (state then {p.evaluate("window.__r")}): sound {s[0]}, paused {s[1]}')
    p.evaluate(UNHIDE); p.wait_for_timeout(1500)
    print('page errors', errs[:3]); b.close()
tmp.unlink(missing_ok=True)
