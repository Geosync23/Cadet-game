# RV30 probe (note 17, SND_LONG): the real game loop in the mess hall at the dinner rush with music on; 6 stalls of 1.2 s
# (the page held busy); counts sound starts and gain moves scheduled in the past (a late start is a pop). As built / on.
# Usage: stall_real.py BUILD [on]
import sys, os, re, pathlib
from playwright.sync_api import sync_playwright
WORK = pathlib.Path(os.environ.get('CADET_WORK', '/tmp/cadet-work'))
THREE = (WORK / 'three/package/build/three.min.js').read_text()
src = pathlib.Path(sys.argv[1]).read_text()
if len(sys.argv) > 2: src = src.replace('const SND_LONG = false;', 'const SND_LONG = true;', 1)
i = src.rfind('})();'); src = src[:i] + "window.__sc = s => eval(s);\n" + src[i:]
tmp = WORK / 'test' / f'_rv30_st_{os.getpid()}.html'; tmp.write_text(src)
LATE = """() => { const L = window.__late = { s: 0, p: 0, worst: 0 }, S = AudioScheduledSourceNode.prototype, f = S.start;
  S.start = function (...a) { const c = this.context, d = c.currentTime - (a[0] || 0); if (c.state === 'running' && a[0] > 0 && d > 0.005) { L.s++; L.worst = Math.max(L.worst, d); } return f.apply(this, a); };
  for (const m of ['setValueAtTime', 'linearRampToValueAtTime', 'exponentialRampToValueAtTime', 'setTargetAtTime']) { const g = AudioParam.prototype[m];
    AudioParam.prototype[m] = function (v, t, ...r) { if (window.__ctx && window.__ctx.state === 'running' && t < window.__ctx.currentTime - 0.005) L.p++; return g.call(this, v, t, ...r); }; } }"""
R3_AT = r"""(([t, deck, room]) => { skipTo(t); goToDeck(deck); const R = DECKS[deck].rooms, k = R[room] ? room : Object.keys(R).find(x => R[x].name === room);
  const tl = ROOM_TILES[k]; if (!tl || !tl.length) return 'no tiles for ' + room; player.obj.position.copy(cellPos(...tl[(tl.length / 2) | 0])); return k; })"""
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME'), args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--autoplay-policy=no-user-gesture-required'])
    p = b.new_page(viewport={'width': 900, 'height': 700}); errs = []; p.on('pageerror', lambda e: errs.append(str(e)))
    p.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
    p.goto('file://' + str(tmp) + '?nosave&debug&sound'); p.wait_for_function('window.__sc !== undefined', timeout=90000)
    p.wait_for_timeout(4000); p.mouse.click(450, 380); p.wait_for_timeout(2000)
    p.evaluate("s => window.__sc(s)", f"({R3_AT})([{1440 + 1110}, 3, 'Mess hall'])"); p.wait_for_timeout(3000)
    p.evaluate("window.__sc('SND.music.setEnabled(true); SND.music.next()')"); p.wait_for_timeout(6000)
    p.evaluate("() => { window.__ctx = window.__sc('SND.ctx'); }"); p.evaluate(LATE); p.wait_for_timeout(3000)
    calm = p.evaluate("() => ({ ...window.__late })"); p.evaluate("() => { Object.assign(window.__late, { s: 0, p: 0, worst: 0 }); }")
    for k in range(6):
        p.evaluate("() => { const c = window.__ctx, t = c.currentTime; while (c.currentTime - t < 1.2); }"); p.wait_for_timeout(1500)
    r = p.evaluate("() => ({ ...window.__late })"); st = p.evaluate("window.__sc('[SND_LONG, SND.music.state().name, !!SND.r3Mess.scene, SND.r3Mess.n]')")
    print(f'SND_LONG {st[0]}: 3 s calm: {calm}; after 6 stalls of 1.2 s: late starts {r["s"]} (worst {r["worst"]:.2f} s), gain moves in the past {r["p"]}; playing {st[1:]}; errors {errs[:2]}')
    b.close()
tmp.unlink(missing_ok=True)
