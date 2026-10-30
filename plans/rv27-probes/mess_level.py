# RV27: the mess hall's real output at the dinner rush (Day 1 18:30), by frequency band, averaged over 6 s, and the clinks.
# Usage: CADET_WORK=... CADET_CHROME=... python3 mess_level.py WORKTREE
import sys, json, pathlib
WT = pathlib.Path(sys.argv[1]).resolve()
exec(open(WT / 'cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
src = (WT / 'sound_check.py').read_text(); R3_AT = src.split('R3_AT = r"""')[1].split('"""')[0]
BANDS = [(0, 250), (250, 2000), (2000, 6000), (6000, 22050)]
with sync_playwright() as pw:
    g = Game(pw, str(WT / 'starship-cadet.html'))
    g.page.goto('file://' + str(g.tmp) + '?nosave&debug&sound'); g.page.wait_for_function('window.__sc !== undefined', timeout=60000)
    g.step(30); g.page.mouse.click(450, 380); g.step(3)
    g.page.wait_for_function("window.__sc('SND._.state()') === 'running'", timeout=10000); g.step(5)
    for name, t in (('dinner rush 18:30', 1440 + 1110), ('lunch 12:15', 1440 + 735)):
        k = g.ev(f"({R3_AT})({json.dumps([t, 3, 'Mess hall'])})"); g.step(40)
        g.ev("(() => { if (window.__an) return; const a = SND.ctx.createAnalyser(); a.fftSize = 4096; a.smoothingTimeConstant = 0; SND.bus.master.connect(a); window.__an = a; })()")
        c0 = g.ev('SND.r3Mess.clinks'); acc = [0.0] * len(BANDS); n = 0
        for _ in range(24):
            g.page.wait_for_timeout(250); g.step(1)
            sp = g.ev("(() => { const a = __an, f = new Float32Array(a.frequencyBinCount); a.getFloatFrequencyData(f); return [Array.from(f), SND.ctx.sampleRate]; })()")
            f, sr = sp; hz = sr / 2 / len(f)
            for j, (lo, hi) in enumerate(BANDS): acc[j] += sum(10 ** (v / 10) for i, v in enumerate(f) if lo <= i * hz < hi and v > -200)
            n += 1
        import math
        db = [round(10 * math.log10(x / n + 1e-20), 1) for x in acc]
        r = g.ev("(M => ({ n: M.n, on: !!M.scene, clinks: M.clinks, bg: M.bg, voices: M.at(M.n).voices }))(SND.r3Mess)")
        print(name, k, r, 'clinks in 6 s', r['clinks'] - c0, 'bands', dict(zip([f'{a}-{b}' for a, b in BANDS], db)))
    print('errors', [e for e in g.errors if e.startswith('pageerror')][:3]); g.close()
