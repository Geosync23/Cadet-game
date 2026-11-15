import sys; sys.path.insert(0, '' + __import__('os').path.dirname(__import__('os').path.abspath(__file__)) + ''); from g import *
GAME = sys.argv[1]; OUT = '/tmp/fr1/'
with sync_playwright() as pw:
    # 1. one exception in one frame
    g = Game(pw, GAME); g.step(60)
    m0 = g.ev('shipNow()'); g.ev("(() => { const u = crowd.update.bind(crowd); let n = 0; crowd.update = (a, b) => { if (n++ === 0) throw new Error('FR1 planted: one bad frame'); return u(a, b); }; })()")
    try: g.step(1)
    except Exception as e: print('1. step raised:', str(e)[:80])
    m1 = g.ev('shipNow()'); g.step(120); m2 = g.ev('shipNow()')
    print(f'1. one throw in crowd.update: ship minute before {m0:.2f}, after the bad frame {m1:.2f}, after 120 more frames {m2:.2f} ->', 'GAME STOPPED FOR GOOD' if m2 == m1 else 'carried on'); print('   errors:', g.errors[:2]); g.close()
    # 2. WebGL context lost and restored
    g = Game(pw, GAME); g.step(60); g.step(1, draw=True); g.page.screenshot(path=OUT + 'ctx_before.png')
    g.ev("window.__lc = renderer.getContext().getExtension('WEBGL_lose_context'); window.__lc.loseContext()"); g.page.wait_for_timeout(300); g.step(5, draw=True)
    g.ev("window.__lc.restoreContext()"); g.page.wait_for_timeout(500); g.step(5, draw=True); g.page.wait_for_timeout(300); g.page.screenshot(path=OUT + 'ctx_after.png')
    print('2. context lost and restored: errors', g.errors[:4], 'calls', g.ev('renderer.info.render.calls'), 'lost?', g.ev('renderer.getContext().isContextLost()'))
    g.ev("goToDeck(3)"); g.step(30); g.step(2, draw=True); g.page.screenshot(path=OUT + 'ctx_deck3.png'); print('   after a deck change: errors', g.errors[:4]); g.close()
    # 3. three.js can't be fetched (real clock, no route fulfil)
    b = pw.chromium.launch(executable_path='/opt/pw-browsers/chromium'); p = b.new_page(viewport={'width': 390, 'height': 844}); errs = []
    p.on('pageerror', lambda e: errs.append(str(e)[:120])); p.route(re.compile(r'.*three\.min\.js'), lambda r: r.abort())
    p.goto('file://' + GAME + '?title', timeout=120000); p.wait_for_timeout(4000); p.screenshot(path=OUT + 'nothree.png')
    print('3. three.js blocked: errors', errs[:3], '| title shown:', p.evaluate("(() => { const t = document.getElementById('title'); return t && !t.hidden ? document.getElementById('tiLine').textContent : 'no title'; })()"), '| canvas:', p.evaluate("document.querySelectorAll('canvas').length")); b.close()
