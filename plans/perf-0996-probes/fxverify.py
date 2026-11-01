exec(open('/tmp/pf/scripts/common.py').read())
from playwright.sync_api import sync_playwright
path=sys.argv[1]
V=r"""(() => { const f = shipEffectsAt; window.__fx = { n: 0, bad: 0, ex: null };
  shipEffectsAt = function (deck, t) { const r = f(deck, t); if (window.__fx.n++ % 7 === 0) { const h = histHour(t), fresh = fxFrom(deck, MACH_HIST.get(h) || null); if (JSON.stringify(fresh) !== JSON.stringify(r)) { window.__fx.bad++; if (!window.__fx.ex) window.__fx.ex = [deck, t, JSON.stringify(fresh).slice(0, 200), JSON.stringify(r).slice(0, 200)]; } } return r; }; return true; })()"""
with sync_playwright() as pw:
    g=Game(pw,path,390,844); g.ev(V)
    for d in range(2,31):
        g.ev(f"skipTo({(d-1)*1440+7*60})"); g.ev(f"goToDeck({[3,4,5,1,2,6,7][d%7]})"); g.step(3000)
        if d % 5 == 0: print(d, g.ev("window.__fx"), flush=True)
    g.ev("goToDeck(3)")
    for b in range(24): g.step(3000)      # a day and more in real time
    print('real day', g.ev("window.__fx"), g.ev("clockText()"))
