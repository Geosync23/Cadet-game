# reviewer 1f: do the dust motes drift away during a pause? (0.28.50 freezes the frame clock t, and the dust adds sin(t ...) each frame)
import sys, json
src = open('cadet_test.py').read().split('import sys, json, hashlib')[0]
exec(src)
from playwright.sync_api import sync_playwright
D = "JSON.stringify(DUST.length ? (() => { const a = DUST[0].geo.attributes.position.array; let s = 0; for (let i = 0; i < Math.min(30, DUST[0].n); i++) s += Math.hypot(a[i*3] - (window.__d0 || a)[i*3], a[i*3+1] - (window.__d0 || a)[i*3+1]); return Math.round(s / Math.min(30, DUST[0].n) * 1000) / 1000; })() : null)"
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1]); g.step(30)
    for n in (1, 2, 3, 5, 6):
        g.ev(f"goToDeck({n})"); g.step(3)
        if g.ev("DUST.length"): print("dust on deck", n); break
    g.ev("window.__d0 = DUST.length ? Array.from(DUST[0].geo.attributes.position.array) : null")
    g.step(1800); print('mean mote move after 60 s running:', g.ev(D))
    g.ev("window.__d0 = DUST.length ? Array.from(DUST[0].geo.attributes.position.array) : null; pauseSet(true)")
    g.step(1800); print('mean mote move after 60 s paused :', g.ev(D))
    g.ev("pauseSet(false)"); g.close()
