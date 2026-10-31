# RV30 probe (note 17, SND_LONG): the music looks 2 s ahead instead of 0.5 s. Does a hand-over sound different? The music
# is faded out (Music app: pick a track, a 2 s fade; a time-of-day change: a 6 s cross-fade); notes the old track had already
# scheduled still play under the fade. Counts the notes that start after the fade began (before the new track starts), with
# the switch as built and switched on. Real game loop. Usage: python3 music_x.py BUILD [on]
import sys, os, re, pathlib
from playwright.sync_api import sync_playwright
WORK = pathlib.Path(os.environ.get('CADET_WORK', '/tmp/cadet-work'))
THREE = (WORK / 'three/package/build/three.min.js').read_text()
src = pathlib.Path(sys.argv[1]).read_text()
if len(sys.argv) > 2: src = src.replace('const SND_LONG = false;', 'const SND_LONG = true;', 1)
i = src.rfind('})();'); src = src[:i] + "window.__sc = s => eval(s);\n" + src[i:]
tmp = WORK / 'test' / f'_rv30_mx_{os.getpid()}.html'; tmp.write_text(src)
REC = """() => { const S = AudioScheduledSourceNode.prototype, f = S.start; window.__st = [];
  S.start = function (...a) { if (window.__rec) window.__st.push(a[0] || this.context.currentTime); return f.apply(this, a); }; }"""
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME'), args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--autoplay-policy=no-user-gesture-required'])
    p = b.new_page(viewport={'width': 900, 'height': 700}); errs = []; p.on('pageerror', lambda e: errs.append(str(e)))
    p.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
    p.goto('file://' + str(tmp) + '?nosave&debug&sound'); p.wait_for_function('window.__sc !== undefined', timeout=90000)
    p.wait_for_timeout(4000); p.mouse.click(450, 380); p.wait_for_timeout(2000)
    print('SND_LONG', p.evaluate("window.__sc('SND_LONG')"))
    p.evaluate("window.__sc('skipTo(1440 + 600)')"); p.wait_for_timeout(1500)
    p.evaluate("window.__sc('SND.music.setEnabled(true); SND.music.next()')"); p.wait_for_timeout(8000)
    p.evaluate(REC); res = []
    for k in range(4):
        stt = p.evaluate("window.__sc('SND.music.state()')"); key = stt['track']
        # notes are scheduled ahead, so record from 3 s before; a plain 0.8 s of the track first (the room's own sounds), then the hand-over: fade 2 s, the new one starts 1 s later
        p.evaluate("() => { window.__st = []; window.__rec = true; window.__t0 = window.__sc('SND.ctx.currentTime'); }"); p.wait_for_timeout(3000)
        base = p.evaluate("() => window.__st.filter(t => t > window.__t0 + 2.05 && t < window.__t0 + 2.85).length")
        p.evaluate(f"() => {{ window.__t0 = window.__sc('SND.ctx.currentTime'); window.__sc(\"SND.music.setMode('{key}')\"); }}"); p.wait_for_timeout(900)
        after = p.evaluate("() => { const t0 = window.__t0; return [window.__st.filter(t => t > t0 + 0.05 && t < t0 + 0.85).length, Math.max(0, ...window.__st.map(t => t - t0))]; }")
        p.evaluate("() => { window.__rec = false; }")
        print(f'  {key}: notes in a plain 0.8 s: {base}; notes starting 0.05-0.85 s into the fade: {after[0]} (latest scheduled +{after[1]:.2f} s)')
        res.append(f'{after[0]}/{base}')
        p.evaluate("window.__sc(\"SND.music.setMode('schedule'); SND.music.next()\")"); p.wait_for_timeout(9000)
    print('old-track notes in the fade (each: in the fade / plain):', res, 'page errors', errs[:2]); b.close()
tmp.unlink(missing_ok=True)
