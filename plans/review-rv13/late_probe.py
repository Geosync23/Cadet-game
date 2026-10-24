# RV13 probe: Name on the beam when you arrive late (item 13): does the beam still open before the event ends?
import sys, json
exec(open('/tmp/rv13/wt-dv1/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1])
    g.ev("if (typeof GUIDE_ON !== 'undefined' && GUIDE_ON) { GUIDE.tq.length = 0; guideToast = () => false; }")
    for late in [int(x) for x in sys.argv[2:]]:
        g.ev(f"""(() => {{ goToDeck(5); actEnd(true); clearGoal(); const d = 1, e = eventsOn(d).find(x => x.id === 'name-on-the-beam');
          SHIP.traces.length = 0; SHIP.events.joined = []; if (typeof BEAM_OPEN !== "undefined") BEAM_OPEN.key = null; setShipNow((d - 1) * 1440 + e.from + {late}); deckCrewFill(); const sp = placeSpot('5-beam-4'); player.obj.position.set(sp.x, 0, sp.z); player.stop(); EV_MIN = -1; eventsTick();
          window.__e = {{ from: e.from, to: e.to }}; }})()""")
        out = None
        for i in range(400):
            g.step(30)
            r = g.ev("({ now: Math.floor(shipNow() % 1440), tj: !!TJ_NOW, ready: typeof beamReady === 'function' ? beamReady() : true, e: window.__e })")
            if r['ready'] or not r['tj']: out = r; break
        print(f"arrive {late} min after the start:", out)
