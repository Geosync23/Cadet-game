exec(open('/tmp/pf/scripts/common.py').read())
from playwright.sync_api import sync_playwright
path=sys.argv[1]
M="(() => { const m = renderer.info.memory, st = crowd.stats(); return { geo: m.geometries, tex: m.textures, chunks: st.chunks, people: st.people, props: Object.keys(_propPacks).length, pgeo: Object.keys(_propGeos).length, cgeo: Object.keys(_crowdGeos).length, gc: typeof _geoCache === 'object' ? (_geoCache.size ?? Object.keys(_geoCache).length) : null, t: hhmm(SHIP.time.min) }; })()"
with sync_playwright() as pw:
    g=Game(pw,path,390,844)
    for lap in range(4):
        for n in g.ev("Object.keys(DECKS).map(Number)") + [4]:
            g.ev(f"goToDeck({n})"); g.step(3)
        g.step(10); gc(g); print(lap, g.ev(M))
