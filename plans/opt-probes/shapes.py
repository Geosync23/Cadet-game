# shape cache proposal: per deck build, how many Box/Cylinder/Sphere/Plane geometries are made, how many distinct
# parameter sets, and the real time spent constructing them
import sys, os, re, json
src = open('/home/user/Cadet-game/cadet_test.py').read().split("import sys, json, hashlib")[0]
exec(src)
from playwright.sync_api import sync_playwright
WRAP = r"""(() => { window.__sh = {}; const T = () => new Event('x').timeStamp;
  for (const k of ['BoxGeometry', 'CylinderGeometry', 'SphereGeometry', 'PlaneGeometry', 'TorusGeometry', 'ConeGeometry', 'CircleGeometry', 'RingGeometry', 'ExtrudeGeometry', 'LatheGeometry', 'CapsuleGeometry']) {
    const O = THREE[k]; if (!O) continue;
    THREE[k] = class extends O { constructor(...a) { const t = T(); super(...a); const s = window.__sh[k] || (window.__sh[k] = { n: 0, ms: 0, keys: new Set() }); s.n++; s.ms += T() - t; s.keys.add(JSON.stringify(a.map(v => typeof v === 'number' ? +v.toFixed(5) : typeof v))); } };
  } })()"""
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844); g.ev("window.__realTick = tickShip; tickShip = () => {}")
    g.ev(WRAP)
    for n in (1, 2, 3, 4, 5, 6, 7):
        g.ev("for (const k in window.__sh) window.__sh[k] = { n: 0, ms: 0, keys: new Set() }")
        ms = g.page.evaluate("n => { const a = new Event('x').timeStamp; __sc('goToDeck(' + n + ')'); return Math.round(new Event('x').timeStamp - a); }", n)
        r = g.page.evaluate("Object.fromEntries(Object.entries(window.__sh).filter(([k, s]) => s.n).map(([k, s]) => [k, [s.n, s.keys.size, Math.round(s.ms)]]))")
        tot = sum(v[2] for v in r.values())
        print(f'D{n} build {ms} ms; shapes made [count, distinct, ms]: {r}; {tot} ms in shape constructors ({100 * tot / max(ms, 1):.0f}%)', flush=True)
    g.close()
