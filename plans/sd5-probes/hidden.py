# SD5 probe (note 9): the page goes hidden (Android: another app or window) and the browser stops drawing frames.
# Does the sound stop? The test clock draws no frame after the hide, as a hidden page gets none.
import sys, os
exec(open('/home/user/cadet-game/cadet_test.py').read().split('a, shots = run(')[0])
path = sys.argv[1]
with sync_playwright() as pw:
    g = Game(pw, path)
    g.page.goto('file://' + str(g.tmp) + '?nosave&debug&sound&soundlog'); g.page.wait_for_function('window.__sc !== undefined', timeout=60000)
    g.step(30); g.page.mouse.click(450, 380); g.step(3)
    g.page.wait_for_function("window.__sc('SND._.state()') === 'running'", timeout=10000)
    for how in ['visibilitychange', 'pagehide', 'freeze']:
        g.ev("pauseSet(false)"); g.step(5); g.page.wait_for_function("window.__sc('SND._.state()') === 'running'", timeout=10000)
        g.ev(f"""(() => {{ Object.defineProperty(document, 'hidden', {{ configurable: true, get: () => true }}); Object.defineProperty(document, 'visibilityState', {{ configurable: true, get: () => 'hidden' }});
           {'document' if how != 'pagehide' else 'window'}.dispatchEvent(new Event('{how}')); }})()""")
        g.page.wait_for_timeout(1500)   # no frames drawn: hidden
        st = g.ev("[SND._.state(), PAUSE.on]")
        print(f'{how}: hidden, no frames for 1.5 s: sound {st[0]}, game paused {st[1]}')
        g.ev("delete document.hidden; delete document.visibilityState; document.dispatchEvent(new Event('visibilitychange'))"); g.step(5)
        print(f'  back: sound {g.ev("SND._.state()")} (paused {g.ev("PAUSE.on")})')
    g.close()
