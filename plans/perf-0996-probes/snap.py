exec(open('/tmp/pf/scripts/common.py').read())
from playwright.sync_api import sync_playwright
path=sys.argv[1]; days=[int(x) for x in sys.argv[2].split(',')]; PLAY=3000
with sync_playwright() as pw:
    g=Game(pw,path,390,844); g.page.evaluate(REALNOW); decks=[3,4,5,1,2,6,7]
    for d in range(1,max(days)+1):
        if d>1: g.ev(f"skipTo({(d-1)*1440+7*60+30})")
        for k in range(2):
            dk=decks[(d*2+k)%len(decks)]; g.ev(f"if (DECKS[{dk}]) goToDeck({dk})"); g.step(PLAY)
        if d in days:
            g.ev("goToDeck(3)"); g.step(30)
            a=heapsnap(g,f'/tmp/pf/snap_d{d}.json'); print(d, sum(v[1] for v in a.values())/1048576, flush=True)
