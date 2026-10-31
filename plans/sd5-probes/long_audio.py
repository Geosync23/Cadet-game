# SD5 probe (note 17): a long real-time session with sound on, counting what the audio graph holds over time.
# Real rAF and clock (no virtual clock); a counter wrapped round the Web Audio calls before the game loads.
# Usage: python3 long_audio.py BUILD.html MINUTES [OUT.json]
import sys, os, re, json, time, pathlib
from playwright.sync_api import sync_playwright
path, mins = sys.argv[1], float(sys.argv[2]); out = sys.argv[3] if len(sys.argv) > 3 else None
WORK = pathlib.Path(os.environ.get('CADET_WORK', '/tmp/cadet-work'))
THREE = (WORK / 'three/package/build/three.min.js').read_text()
html = pathlib.Path(path).read_text(); i = html.rfind('})();'); html = html[:i] + "window.__sc = src => eval(src);\n" + html[i:]
tmp = WORK / 'test' / f'_long_{os.getpid()}.html'; tmp.parent.mkdir(parents=True, exist_ok=True); tmp.write_text(html)
INIT = r"""(() => {
  const C = window.__ac = { made: {}, started: 0, ended: 0, live: 0, peakLive: 0, autom: 0, cancels: 0, conn: 0, disc: 0, params: new Set(), comp: null };
  const B = (window.BaseAudioContext || window.AudioContext).prototype;
  for (const k of Object.getOwnPropertyNames(B)) if (/^create/.test(k) && typeof B[k] === 'function') { const f = B[k]; B[k] = function (...a) { C.made[k] = (C.made[k] || 0) + 1; const n = f.apply(this, a); if (k === 'createDynamicsCompressor' && !C.comp) C.comp = n; return n; }; }
  const S = window.AudioScheduledSourceNode.prototype, st = S.start;
  S.start = function (...a) { C.started++; C.live++; C.peakLive = Math.max(C.peakLive, C.live); this.addEventListener('ended', () => { C.ended++; C.live--; }); return st.apply(this, a); };
  const P = AudioParam.prototype;
  for (const k of ['setValueAtTime', 'linearRampToValueAtTime', 'exponentialRampToValueAtTime', 'setTargetAtTime', 'setValueCurveAtTime']) { const f = P[k]; P[k] = function (...a) { C.autom++; if (!this.__n) { this.__n = 0; } this.__n++; C.params.add(this); return f.apply(this, a); }; }
  { const f = P.cancelScheduledValues; P.cancelScheduledValues = function (...a) { C.cancels++; this.__n = 0; return f.apply(this, a); }; }
  const N = AudioNode.prototype, cn = N.connect, dc = N.disconnect;
  N.connect = function (...a) { C.conn++; return cn.apply(this, a); }; N.disconnect = function (...a) { C.disc++; return dc.apply(this, a); };
})();"""
ROOMS = [(3, 'Mess hall'), (3, 'Gym'), (3, 'Galley'), (4, 'Laundry'), (2, None), (5, None), (6, None), (3, 'Mess hall'), (1, None)]
GO = r"""(([deck, room]) => { goToDeck(deck); const R = DECKS[deck].rooms; let k = room ? Object.keys(R).find(x => R[x].name === room) : null;
  if (!k) { const ks = Object.keys(ROOM_TILES).filter(x => ROOM_TILES[x] && ROOM_TILES[x].length > 6); k = ks[(Math.random() * ks.length) | 0]; }
  const tl = ROOM_TILES[k]; if (!tl || !tl.length) return 'none'; player.obj.position.copy(cellPos(...tl[(tl.length / 2) | 0])); return k + ':' + (R[k] ? R[k].name : ''); })"""
SAMPLE = r"""(() => { const C = window.__ac; let big = 0, bigLab = 0; C.params.forEach(p => { if (p.__n > big) big = p.__n; });
  const a = window.__an; let pk = 0, pkc = 0;
  if (a) { const b = new Float32Array(a.m.fftSize); a.m.getFloatTimeDomainData(b); for (const v of b) pk = Math.max(pk, Math.abs(v)); a.c.getFloatTimeDomainData(b); for (const v of b) pkc = Math.max(pkc, Math.abs(v)); }
  return { t: Math.round(SND.ctx.currentTime), wall: Math.round(performance.now() / 1000), state: SND.ctx.state, made: Object.values(C.made).reduce((x, y) => x + y, 0), started: C.started, live: C.live, peakLive: C.peakLive,
    autom: C.autom, maxEventsOneParam: big, params: C.params.size, conn: C.conn, disc: C.disc, loops: SND._.LOOPS.size, loopLabels: [...SND._.LOOPS].map(l => l.label || '?').join(','),
    music: SND.music ? SND.music.state().name : null, deck: deckDef.num, ship: Math.floor(shipNow()), red: C.comp ? Math.round(C.comp.reduction * 10) / 10 : null, peakMaster: Math.round(pk * 1000) / 1000, peakOut: Math.round(pkc * 1000) / 1000,
    lat: SND.ctx.baseLatency, under: SND.ctx.playbackStats ? SND.ctx.playbackStats.underrunEvents : null, underMs: SND.ctx.playbackStats ? Math.round(SND.ctx.playbackStats.underrunDuration * 1000) : null, heap: performance.memory ? Math.round(performance.memory.usedJSHeapSize / 1e6) : null }; })()"""
rows = []
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--autoplay-policy=no-user-gesture-required'])
    pg = b.new_page(viewport={'width': 900, 'height': 760})
    errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
    pg.add_init_script(INIT)
    pg.goto('file://' + str(tmp) + '?nosave&debug&sound'); pg.wait_for_function('window.__sc !== undefined', timeout=90000)
    ev = lambda s: pg.evaluate('s => window.__sc(s)', s)
    pg.wait_for_timeout(3000); pg.mouse.click(450, 380); pg.wait_for_timeout(1500)
    print('state', ev("SND._.state()"))
    ev("skipTo(2 * 1440 + 7 * 60)")
    ev("(() => { const C = window.__ac; const m = SND.ctx.createAnalyser(); m.fftSize = 2048; SND.bus.master.connect(m); const c = SND.ctx.createAnalyser(); c.fftSize = 2048; if (C.comp) C.comp.connect(c); window.__an = { m, c }; })()")
    t0 = time.time(); k = 0; last_move = -1e9; peakmax = 0
    while time.time() - t0 < mins * 60:
        el = time.time() - t0
        if el - last_move > 45:
            if k % 4 == 3: ev('pauseSet(true)'); pg.wait_for_timeout(3000); ev('pauseSet(false)')
            last_move = el; where = ev(f"({GO})({json.dumps(ROOMS[k % len(ROOMS)])})"); k += 1
        # sample the peaks often, record a row every 15 s
        for _ in range(15):
            pg.wait_for_timeout(1000)
            try: r = ev(SAMPLE); peakmax = max(peakmax, r['peakOut'])
            except Exception as e: print('sample error', e); break
        r['where'] = where; r['peakOutMax15s'] = peakmax; peakmax = 0
        rows.append(r); print(json.dumps({k2: r[k2] for k2 in ['wall', 't', 'state', 'live', 'peakLive', 'made', 'autom', 'maxEventsOneParam', 'loops', 'music', 'red', 'peakOutMax15s', 'under', 'underMs', 'heap', 'where']}), flush=True)
    print('loops at end:', rows[-1]['loopLabels']); print('errors', errs[:5])
    b.close()
if out: json.dump(rows, open(out, 'w'))
