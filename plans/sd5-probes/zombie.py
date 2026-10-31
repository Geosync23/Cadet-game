# SD5 probe (note 17, the mechanism): does a finished one-shot's chain (gain, filter, panner) left connected cost render time
# until garbage collection? Offline render of 20 s with K finished chains still connected (held, as before GC), vs disconnected.
from playwright.sync_api import sync_playwright
JS = r"""(async (K, disc) => {
  const c = new OfflineAudioContext(2, 48000 * 20, 48000), keep = [];
  const bus = c.createGain(); bus.connect(c.destination);
  for (let i = 0; i < K; i++) {
    const o = c.createOscillator(), f = c.createBiquadFilter(), g = c.createGain(), p = c.createStereoPanner();
    o.connect(f); f.connect(g); g.connect(p); p.connect(bus); o.start(0); o.stop(0.01 + (i % 50) * 0.002);
    if (disc) o.onended = () => { o.disconnect(); f.disconnect(); g.disconnect(); p.disconnect(); };
    keep.push([o, f, g, p]);
  }
  const t = performance.now(); await c.startRendering(); return Math.round(performance.now() - t);
})"""
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome')
    p = b.new_page(); p.goto('about:blank')
    for K in [0, 500, 2000, 5000]:
        print(K, 'connected ms', p.evaluate(f"({JS})({K}, false)"), ' disconnected-on-end ms', p.evaluate(f"({JS})({K}, true)"))
    b.close()
