# the game at its own speed (no virtual clock): MIN real minutes, sampled each minute: the main loop's own time per frame
# (mean, p99, max), frames per second, heap, DOM, audio nodes made and still playing. ARGS: build minutes out.json [sound|mute]
import sys, os, json, time, re, pathlib
from playwright.sync_api import sync_playwright
path, MIN, OUT, MODE = sys.argv[1], float(sys.argv[2]), sys.argv[3], sys.argv[4]
W = pathlib.Path('/tmp/cadet-work'); THREE = (W / 'three/package/build/three.min.js').read_text()
HOOK = r"""
(() => { const A = window.__A = { made: {}, live: 0, ended: 0, conn: 0, disc: 0 };
  const P = (window.BaseAudioContext || window.AudioContext).prototype;
  for (const k of Object.getOwnPropertyNames(P)) if (/^create/.test(k) && typeof P[k] === 'function' && k !== 'createBuffer' && k !== 'createPeriodicWave') { const f = P[k];
    P[k] = function (...a) { const n = f.apply(this, a); A.made[k] = (A.made[k] || 0) + 1; if (n && n.addEventListener && 'onended' in n) { A.live++; n.addEventListener('ended', () => { A.live--; A.ended++; }); } return n; }; }
  const C = AudioNode.prototype.connect, D = AudioNode.prototype.disconnect;
  AudioNode.prototype.connect = function (...a) { A.conn++; return C.apply(this, a); };
  AudioNode.prototype.disconnect = function (...a) { A.disc++; return D.apply(this, a); };
  // the main loop's own time: every requestAnimationFrame callback timed
  const raf = window.requestAnimationFrame.bind(window), T = window.__T = [];
  window.requestAnimationFrame = cb => raf(ts => { const a = performance.now(); cb(ts); T.push(performance.now() - a); });
})();
"""
html = pathlib.Path(path).read_text(); i = html.rfind('})();'); html = html[:i] + "window.__sc = src => eval(src);\n" + html[i:]
tmp = W / 'test' / f'_real_{os.getpid()}.html'; tmp.write_text(html)
q = '?nosave&debug' + ('&sound' if MODE == 'sound' else '&mute')
rows = []
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path='/opt/pw-browsers/chromium', args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--autoplay-policy=no-user-gesture-required'])
    pg = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
    errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
    pg.add_init_script(HOOK)
    pg.goto('file://' + str(tmp) + q); pg.wait_for_function('window.__sc !== undefined', timeout=120000)
    pg.keyboard.press('Shift'); pg.mouse.click(5, 420)            # the first tap starts the sound
    ev = lambda s: pg.evaluate('s => window.__sc(s)', s)
    ev("(() => { if (deckDef.num !== 3) goToDeck(3); const k = Object.keys(ROOM_BOX).find(k => ROOMS[k] && /^Mess/i.test(ROOMS[k].name)), b = ROOM_BOX[k], mid = cellPos(Math.floor((b.i0 + b.i1) / 2), Math.floor((b.j0 + b.j1) / 2)); const at = nearestOpen(mid.x, mid.z, player); player.obj.position.copy(cellPos(...at)); target.copy(player.obj.position).setY(.7); })()")
    cdp = pg.context.new_cdp_session(pg)
    t0 = time.time(); k = 0
    while time.time() - t0 < MIN * 60:
        time.sleep(60 - (time.time() - t0) % 60); k += 1
        r = pg.evaluate("""() => { const T = window.__T.splice(0), s = [...T].sort((a, b) => a - b), q = p => s.length ? +s[Math.min(s.length - 1, Math.floor(p * s.length))].toFixed(1) : null;
          return { frames: T.length, mean: T.length ? +(T.reduce((a, b) => a + b, 0) / T.length).toFixed(2) : null, p50: q(.5), p99: q(.99), max: q(1), over33: T.filter(v => v > 33).length, A: JSON.parse(JSON.stringify(window.__A)), dom: document.getElementsByTagName('*').length }; }""")
        r.update(ev("({ day: SHIP.time.day, min: Math.round(SHIP.time.min), crew: crowd.stats().people, snd: !!(SND && SND.ctx), sstate: SND && SND.ctx ? SND.ctx.state : null, geo: renderer.info.memory.geometries })"))
        cdp.send('HeapProfiler.collectGarbage'); r['heap'] = round(cdp.send('Runtime.getHeapUsage')['usedSize'] / 1048576, 1)
        r['min_real'] = k; r['fps'] = round(r['frames'] / 60, 1); r['made'] = sum(r['A']['made'].values())
        rows.append(r); json.dump({'rows': rows, 'errs': errs[:20]}, open(OUT, 'w'))
        print(k, {x: r[x] for x in ('fps', 'mean', 'p50', 'p99', 'max', 'over33', 'heap', 'dom', 'crew', 'day', 'min', 'snd', 'sstate', 'made')}, 'live', r['A']['live'], 'conn', r['A']['conn'], 'disc', r['A']['disc'], flush=True)
    b.close()
tmp.unlink()
