# SD5 (note 17): does a long-lived AudioParam fed setTargetAtTime calls forever (as the mess murmur's voices are)
# cost more and more render time? 12 voices, each param moved ~20 times a second, 0.35 s ahead, as voice2 does.
# mode 'plain' as the game; mode 'hold' calls cancelAndHoldAtTime(now) first each time (drops what's past)
import sys, os, time, subprocess
from playwright.sync_api import sync_playwright
mode = sys.argv[1]; mins = float(sys.argv[2])
def ticks(pid_set):
    tot = 0
    for p in subprocess.run(['pgrep', '-f', 'chrome.*type=renderer'], capture_output=True, text=True).stdout.split():
        if p not in pid_set: continue
        for t in os.listdir(f'/proc/{p}/task'):
            try:
                if open(f'/proc/{p}/task/{t}/comm').read().strip() == 'AudioOutputDevi':
                    f = open(f'/proc/{p}/task/{t}/stat').read().rsplit(')', 1)[1].split(); tot += int(f[11]) + int(f[12])
            except Exception: pass
    return tot
with sync_playwright() as pw:
    before = set(subprocess.run(['pgrep', '-f', 'chrome.*type=renderer'], capture_output=True, text=True).stdout.split())
    b = pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome', args=['--autoplay-policy=no-user-gesture-required'])
    p = b.new_page(); p.goto('about:blank')
    mine = set(subprocess.run(['pgrep', '-f', 'chrome.*type=renderer'], capture_output=True, text=True).stdout.split()) - before
    p.evaluate("""(mode) => { const c = new AudioContext(); window.c = c; const out = c.createGain(); out.gain.value = 0.01; out.connect(c.destination);
      const V = []; for (let i = 0; i < 12; i++) { const o = c.createOscillator(), f1 = c.createBiquadFilter(), g = c.createGain(); o.type = 'sawtooth'; f1.type = 'bandpass'; g.gain.value = 0;
        o.connect(f1); f1.connect(g); g.connect(out); o.start(); V.push({ o, f1, g, next: c.currentTime }); }
      const mv = (pr, v, t, k) => { if (mode === 'hold' && pr.cancelAndHoldAtTime) pr.cancelAndHoldAtTime(c.currentTime); pr.setTargetAtTime(v, t, k); };
      setInterval(() => { const u = c.currentTime + 0.35; for (const x of V) while (x.next < u) { const t = x.next; mv(x.f1.frequency, 300 + Math.random() * 600, t, 0.025); mv(x.o.frequency, 100 + Math.random() * 100, t, 0.04); mv(x.g.gain, Math.random(), t, 0.018); x.next += 0.05 + Math.random() * 0.1; } }, 16); }""", mode)
    t0 = time.time(); a = ticks(mine)
    while time.time() - t0 < mins * 60:
        time.sleep(30); z = ticks(mine); print(f'{mode} {round((time.time() - t0) / 60, 1)} min: audio thread {round((z - a) / 30, 1)}% of a core', flush=True); a = z
    b.close()
