# SD5 (note 17): the audio thread's CPU (% of one core) for each part of the sound, at 03:00 in the mess (nobody about),
# then the same spot held for HOLD minutes (does it grow?). The head count forced as in mess_rec.py.
# Usage: python3 cost.py BUILD.html HOLD_MINUTES [latency]
import sys, os, re, time, pathlib, subprocess
from playwright.sync_api import sync_playwright
path, hold = sys.argv[1], float(sys.argv[2]); lat = sys.argv[3] if len(sys.argv) > 3 else None
WORK = pathlib.Path(os.environ.get('CADET_WORK', '/tmp/cadet-work'))
THREE = (WORK / 'three/package/build/three.min.js').read_text()
src = pathlib.Path(path).read_text()
A = "    function count() {   // people in the mess hall (the crew there, plus you), or -1 when you're not in it\n"
src = src.replace(A, A + "      if (window.__messN !== undefined && deckDef && deckDef.num === 3) { M.full = 50; return window.__messN; }   // probe only\n")
if lat: src = src.replace("latencyHint: 'interactive'", f"latencyHint: '{lat}'")
i = src.rfind('})();'); src = src[:i] + "window.__sc = src => eval(src);\n" + src[i:]
tmp = WORK / 'test' / f'_cost_{os.getpid()}.html'; tmp.write_text(src)
def audio_ticks():
    tot = 0
    for p in subprocess.run(['pgrep', '-f', 'chrome.*type=renderer'], capture_output=True, text=True).stdout.split():
        try:
            for t in os.listdir(f'/proc/{p}/task'):
                try:
                    if open(f'/proc/{p}/task/{t}/comm').read().strip() == 'AudioOutputDevi':
                        f = open(f'/proc/{p}/task/{t}/stat').read().rsplit(')', 1)[1].split(); tot += int(f[11]) + int(f[12])
                except Exception: pass
        except Exception: pass
    return tot
def meas(secs=20):
    a = audio_ticks(); t = time.time(); time.sleep(secs); return round((audio_ticks() - a) / (time.time() - t), 1)   # ticks/s = % of a core
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    pg = b.new_page(viewport={'width': 900, 'height': 760})
    pg.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
    pg.goto('file://' + str(tmp) + '?nosave&debug&sound'); pg.wait_for_function('window.__sc !== undefined', timeout=90000)
    ev = lambda s: pg.evaluate('s => window.__sc(s)', s)
    pg.wait_for_timeout(3000); pg.mouse.click(450, 380); pg.wait_for_timeout(1500)
    print('latency', ev("[SND.ctx.baseLatency, SND.ctx.outputLatency]"))
    ev("""(() => { skipTo(2 * 1440 + 180); goToDeck(3); const R = DECKS[3].rooms, k = Object.keys(R).find(x => R[x].name === 'Mess hall');
      const tl = ROOM_TILES[k]; player.obj.position.copy(cellPos(...tl[(tl.length / 2) | 0])); SND.music.setEnabled(false); window.__messN = 0; })()""")
    pg.wait_for_timeout(4000)
    print('hum only (mess empty, music off):', meas(), '% of a core', flush=True)
    ev("SND.music.setEnabled(true); SND.music.setMode('dawn' in SND.music.TRACKS ? 'dawn' : Object.keys(SND.music.TRACKS)[0])"); pg.wait_for_timeout(4000)
    print('hum + music:', meas(), flush=True)
    ev("window.__messN = 40"); pg.wait_for_timeout(4000)
    print('hum + music + mess at the rush:', meas(), flush=True)
    ev("SND.music.setEnabled(false)"); pg.wait_for_timeout(4000)
    print('hum + mess at the rush:', meas(), flush=True)
    ev("SND.music.setEnabled(true)"); pg.wait_for_timeout(4000)
    t0 = time.time()
    while time.time() - t0 < hold * 60:
        print(f'held {round((time.time() - t0) / 60, 1)} min: hum + music + mess', meas(30), 'under', ev("SND.ctx.playbackStats.underrunEvents"), 'music', ev("SND.music.state().name"), flush=True)
    b.close()
tmp.unlink(missing_ok=True)
