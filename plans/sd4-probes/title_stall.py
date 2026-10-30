# SD4: freeze the page's main thread for 2.5 s at ~10 s after the wake tap; an AudioWorklet (audio thread) logs the level
# of the master bus every ~0.1 s, so a gap in the scheduled music shows even while the page is frozen.
import os, sys, pathlib, time, re
from playwright.sync_api import sync_playwright
GAME = pathlib.Path(sys.argv[1]); WORK = pathlib.Path(os.environ.get('CADET_WORK', '/tmp/cadet-work'))
THREE = (WORK / 'three/package/build/three.min.js').read_text()
src = GAME.read_text(); i = src.rfind('})();'); src = src[:i] + "window.__sc = s => eval(s);\n" + src[i:]
(WORK / 'test').mkdir(exist_ok=True); f = WORK / 'test' / f'_stall_{os.getpid()}.html'; f.write_text(src)
WK = "class M extends AudioWorkletProcessor{constructor(){super();this.s=0;this.n=0}process(i){const c=i[0]&&i[0][0];if(c){for(const v of c)this.s+=v*v;this.n+=c.length}if(this.n>=4410){this.port.postMessage([currentTime,10*Math.log10(this.s/this.n+1e-12)]);this.s=0;this.n=0}return true}}registerProcessor('m',M);"
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get('CADET_CHROME'), args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    pg = b.new_page(viewport={'width': 390, 'height': 844}); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
    pg.goto('file://' + str(f) + '?title&nosave&sound')
    pg.wait_for_function('window.__sc !== undefined', timeout=120000); time.sleep(2)
    pg.mouse.click(195, 420); pg.wait_for_function('window.__sc("!!SND.ctx")', timeout=20000)
    pg.evaluate('s => window.__sc(s)', "(async () => { const u = 'data:text/javascript,' + encodeURIComponent(" + repr(WK) + "); await SND.ctx.audioWorklet.addModule(u); const n = new AudioWorkletNode(SND.ctx, 'm'); window.__lv = []; n.port.onmessage = e => __lv.push(e.data); SND.bus.master.connect(n); n.connect(SND.ctx.destination); window.__wn = n; })()")
    time.sleep(8)
    t = pg.evaluate('s => window.__sc(s)', "(() => { const T = SND.titleSnd.list[0], ph = () => (SND.ctx.currentTime - T.startAt) % T.len; while (Math.abs(ph() - (T.len - 1.3)) > 0.03); const t = SND.ctx.currentTime, e = performance.now() + 2500; while (performance.now() < e); return t; })()")
    time.sleep(4)
    lv = pg.evaluate('s => window.__sc(s)', '__lv')
    rows = [(round(a - t, 1), round(d, 1)) for a, d in lv if -1 <= a - t <= 4]
    print('stall at', round(t, 1), 's; level (s after the stall start, dB):'); print(' '.join(f'{a}:{d}' for a, d in rows))
    print('bar starts at +1.3 s; level 1.3-2.4 s', round(sum(d for a, d in rows if 1.3 <= a <= 2.4) / max(1, sum(1 for a, d in rows if 1.3 <= a <= 2.4)), 1), 'dB; lowest during the stall window', min(d for a, d in rows if 0.5 <= a <= 3), 'errors', errs[:3]); b.close()
f.unlink(missing_ok=True)
