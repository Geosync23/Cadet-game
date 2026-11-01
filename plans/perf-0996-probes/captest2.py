exec(open('/tmp/pf/scripts/common.py').read())
from playwright.sync_api import sync_playwright
path=sys.argv[1]
with sync_playwright() as pw:
    for q in ['', '&pfcap', '&pfcap=30']:
        EXTRA_Q=q; g=GameQ(pw,path,390,844)
        r=g.ev("(() => { let n = 0; const rr = renderer.render.bind(renderer); renderer.render = (s, c) => { n++; }; const m0 = SHIP.time.min; window.__step(1200, 1000 / 120); renderer.render = rr; return [n, +(SHIP.time.min - m0).toFixed(2)]; })()")
        print(q or 'none', 'loop frames in 10 s of a 120 Hz screen:', r[0], ' ship minutes passed:', r[1]); g.close()
