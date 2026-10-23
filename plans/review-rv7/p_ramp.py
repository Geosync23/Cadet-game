# RV7: Day 1 arrival: every pop-up shown from signing the manifest, with real time on screen
import sys, os, time
BUILD = sys.argv[1]; sys.argv = [sys.argv[0], BUILD]
exec(open('arrows_check.py').read().split("GUIDE = 'guide' in")[0])
class P(Page):
    def ready(self):
        self.page.wait_for_function('window.__sc !== undefined', timeout=90000)
        self.ev("(() => { const rr = renderer.render.bind(renderer); renderer.render = (s, c) => { if (window.__draw) rr(s, c); }; })()")
        self.step(20)
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
    pg = P(ctx, BUILD)
    pg.ev("window.__shown = []; { const el = document.getElementById('toast'); new MutationObserver(() => { const t = el.textContent; const L = window.__shown; if (!L.length || L[L.length - 1][1] !== t) L.push([Math.round(performance.now()), t]); }).observe(el, { subtree: true, childList: true, characterData: true }); }")
    if pg.page.locator('text=Sign and go aboard').count():
        pg.page.fill('form input', 'Ada'); pg.page.click('text=Sign and go aboard')
    t0 = pg.ev('performance.now()')
    for i in range(140): pg.step(8); time.sleep(0.25)
    L = pg.ev('window.__shown')
    for i, (t, x) in enumerate(L):
        nxt = L[i + 1][0] if i + 1 < len(L) else None
        print(f"{(t - t0) / 1000:6.1f}s  shown {((nxt - t) / 1000 if nxt else 0):4.1f}s  {x[:90]}")
