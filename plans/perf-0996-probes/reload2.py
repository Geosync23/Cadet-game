exec(open('/tmp/pf/scripts/common.py').read())
from playwright.sync_api import sync_playwright
path=sys.argv[1]; SAVE=open(sys.argv[2]).read()
G="(() => { const m = renderer.info.memory; return [deckDef.num, m.geometries, m.textures, SHIP.time.day, Math.round(SHIP.time.min)]; })()"
with sync_playwright() as pw:
    g=Game(pw,path,390,844)
    g.ev(f"localStorage.setItem('starship-cadet-save', {json.dumps(SAVE)}); localStorage.setItem('starship-cadet-save-slot','1')")
    g.page.goto('file://' + str(g.tmp) + '?debug'); g.page.wait_for_function('window.__sc !== undefined', timeout=90000); g.ev("localStorage.clear()")
    g.step(30); print('loaded', g.ev(G))
    for d in [4,3,4,3,5,3]:
        g.ev(f"goToDeck({d})"); g.step(30); print(d, g.ev(G))
    g.ev("skipTo(shipNow()+60)"); g.step(30); print('skip', g.ev(G))
    # fresh page, same moment
    g2=Game(pw,path,390,844); g2.ev(f"skipTo({39*1440+604})"); g2.step(30); print('fresh', g2.ev(G))
    for d in [4,3]: g2.ev(f"goToDeck({d})"); g2.step(30); print(d, g2.ev(G))
