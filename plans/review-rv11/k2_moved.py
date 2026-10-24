import sys, json
exec(open('/home/user/w-k2/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844); g.step(3)
    r = g.ev("""(() => { skipTo(11 * 1440 + 958); goToDeck(7, null); SHIP.device.settings.tips = false;
      const pl = [...PLACE_OF.values()].filter(p => p.type === 'rec:seat' && p.room === 'A' && !p.ring && !heldBy(p.id)); const sp = placeSpot(pl[0].id);
      recGo('seat', { x: sp.x, z: sp.z }, 'Seats', ''); const mine = ACT && ACT.placeId;
      window.__a = DECK_CREW.find(x => x.p && !x.p.story && x.p.rank !== 'guest'); window.__mine = mine;
      let i = 0; window.__skip = true; for (; i < 900; i++) { window.__a.goalId = mine; window.__step(1, 1000 / 30); if (!ACT || ACT.o.moved || ACT.phase === 'do') break; } window.__skip = false;
      return [mine, i, ACT && ACT.placeId, ACT && ACT.o.moved, ACT && ACT.phase]; })()""")
    print('your seat, held by the stub:', r)
    mv = []
    for k in range(60):
        g.step(30); mv.append(g.ev("[SHIP.time.min, ACT ? ACT.kind + ':' + ACT.phase : null, !!(ACT && ACT.o && ACT.o.moved), ACT && ACT.placeId, !!(ACT && ACT.def && ACT.def.until)]"))
        if g.ev("SHIP.time.min") >= 1016: break
    on = [x for x in mv if x[1] == 'recSeat:do']
    print('seated rows', len(on), 'first', on[:1], 'last', on[-1:], 'errors', g.errors[:2])
    g.close()
