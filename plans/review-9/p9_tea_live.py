# PR9: the tea corner live, Day 5 13:20 of a new game (intro on), 390x844: where Halloran, Soto and the tea seats' crew are; a shot
import sys, json, os
exec(open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[1])), 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
tag = sys.argv[2]
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1])
    g.page.set_viewport_size({'width': 390, 'height': 844})
    g.ev('localStorage.clear()'); g.ev('newGameStart(true)'); g.step(5)
    g.page.fill('form input[maxlength="24"]', 'Sam'); g.page.click('form button'); g.step(5)
    out = []
    for m in (782, 800, 815, 832):
        g.ev(f"(() => {{ skipTo(4 * 1440 + {m}); if (deckDef.num !== 5) goToDeck(5); return 1; }})()"); g.step(240)
        r = g.ev("""(() => { const P = schedData().byId, out = [];
          for (const a of DECK_CREW) { const w = whereIs(a.p, shipNow()); if (w && /^5-tea/.test(w.placeId || '') || ['halloran-emeka', 'soto-marta', 'calder'].includes(a.p.id))
            out.push([a.p.id, w && w.placeId, w && w.tag, a.x.toFixed(2), a.z.toFixed(2), a.goalId || null]); }
          return { t: clockText(), crew: out }; })()""")
        out.append(r); print(json.dumps(r))
        if m == 815:
            g.ev("(() => { const q = schedData().byId.get('5-tea-1'); player.obj.position.copy(cellPos(q.at[0] - 2, q.at[1] + 1)); return 1; })()"); g.step(30)
            g.page.screenshot(path=f'{tag}_tea_1335.png')
    print('page errors', g.errors[:4]); g.close()
