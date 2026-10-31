# SD5 (note 4): record the mess hall's murmur alone at set head counts, before (MESS_SCALE off) and after (on).
# A probe copy only: count() is told the head count (window.__messN); 03:00 so nobody else is about; music and hum muted.
# Usage: python3 mess_rec.py BUILD.html OUTDIR
import sys, os, re, json, time, pathlib, base64, struct
import numpy as np
from playwright.sync_api import sync_playwright
path, outd = sys.argv[1], pathlib.Path(sys.argv[2]); outd.mkdir(parents=True, exist_ok=True)
WORK = pathlib.Path(os.environ.get('CADET_WORK', '/tmp/cadet-work'))
THREE = (WORK / 'three/package/build/three.min.js').read_text()
src = pathlib.Path(path).read_text()
A = "    function count() {   // people in the mess hall (the crew there, plus you), or -1 when you're not in it\n"
assert src.count(A) == 1
src = src.replace(A, A + "      if (window.__messN !== undefined && deckDef && deckDef.num === 3) { M.full = 50; return window.__messN; }   // probe only (50: the 49 seats and you, as count() finds)\n")
CASES = [('empty', 0), ('one crew walking through', 2), ('three crew', 4), ('half full', 25), ('the rush', 40)]
SR = 22050
def wav(x):
    x = np.clip(x, -1, 1); d = (x * 32767).astype('<i2').tobytes()
    return b'RIFF' + struct.pack('<I', 36 + len(d)) + b'WAVEfmt ' + struct.pack('<IHHIIHH', 16, 1, 1, SR, SR * 2, 2, 16) + b'data' + struct.pack('<I', len(d)) + d
res = {}
for label, sw in [('before', 'false'), ('after', 'true')]:
    s2 = src.replace('const MESS_SCALE = false;', f'const MESS_SCALE = {sw};', 1)
    i = s2.rfind('})();'); s2 = s2[:i] + "window.__sc = src => eval(src);\n" + s2[i:]
    tmp = WORK / 'test' / f'_rec_{label}_{os.getpid()}.html'; tmp.write_text(s2)
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
        pg = b.new_page(viewport={'width': 900, 'height': 760})
        pg.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
        pg.goto('file://' + str(tmp) + '?nosave&debug&sound'); pg.wait_for_function('window.__sc !== undefined', timeout=90000)
        ev = lambda s: pg.evaluate('s => window.__sc(s)', s)
        pg.wait_for_timeout(3000); pg.mouse.click(450, 380); pg.wait_for_timeout(1500)
        ev("""(() => { skipTo(2 * 1440 + 180); goToDeck(3); const R = DECKS[3].rooms, k = Object.keys(R).find(x => R[x].name === 'Mess hall');
          const tl = ROOM_TILES[k]; player.obj.position.copy(cellPos(...tl[(tl.length / 2) | 0])); SND.music.setEnabled(false); window.__messN = 0; })()""")
        pg.wait_for_timeout(3000)
        ev("""(() => { SND.bus.hum.gain.cancelScheduledValues(0); SND.bus.hum.gain.value = 0;
          const c = SND.ctx, sp = c.createScriptProcessor(4096, 2, 1), z = c.createGain(); z.gain.value = 0; window.__rec = null;
          sp.onaudioprocess = e => { if (!window.__rec) return; const a = e.inputBuffer.getChannelData(0), b2 = e.inputBuffer.getChannelData(1); const o = new Float32Array(a.length); for (let i = 0; i < a.length; i++) o[i] = (a[i] + b2[i]) / 2; window.__rec.push(o); };
          SND.bus.master.connect(sp); sp.connect(z); z.connect(c.destination); window.__sr = c.sampleRate; })()""")
        for name, n in CASES:
            ev(f"window.__messN = {n}"); pg.wait_for_timeout(5000)
            ev("window.__rec = []"); pg.wait_for_timeout(10000)
            data = ev("(() => { const r = window.__rec; window.__rec = null; let n = 0; r.forEach(x => n += x.length); const o = new Float32Array(n); let k = 0; r.forEach(x => { o.set(x, k); k += x.length; }); const u = new Uint8Array(o.buffer); let s = ''; for (let i = 0; i < u.length; i += 32768) s += String.fromCharCode.apply(null, u.subarray(i, i + 32768)); return [btoa(s), window.__sr, SND.r3Mess.n, !!SND.r3Mess.scene]; })()")
            x = np.frombuffer(base64.b64decode(data[0]), dtype='<f4'); sr = data[1]
            idx = (np.arange(int(len(x) * SR / sr)) * sr / SR).astype(int); y = x[idx]
            rms = float(np.sqrt(np.mean(y ** 2))) if len(y) else 0
            db = 20 * np.log10(rms) if rms > 1e-7 else None
            fn = f"{label}-{name.replace(' ', '-')}.wav"; (outd / fn).write_bytes(wav(y * 4))   # recorded +12 dB (the same for every clip) so it can be heard on a phone
            res[f'{label}|{name}'] = {'n': data[2], 'scene': data[3], 'rms_db': None if db is None else round(db, 1), 'secs': round(len(y) / SR, 1), 'file': fn}
            print(label, name, res[f'{label}|{name}'], flush=True)
        b.close()
    tmp.unlink(missing_ok=True)
json.dump(res, open(outd / 'levels.json', 'w'), indent=1)
