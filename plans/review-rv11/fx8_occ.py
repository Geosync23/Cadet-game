import sys
exec(open('/home/user/w-fx8/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844); g.step(3)
    g.ev("setShipNow(1440 + 15 * 60 + 30)"); g.step(5)
    out = None
    for dk in (5, 3, 4, 2, 1, 6):
      g.ev(f"goToDeck({dk})"); g.step(40)
      out = g.ev("""(() => { const res = [];
      for (const id of Object.keys(OCCASIONS)) { const o = OCCASIONS[id]; if (o.chance || +o.deck !== deckDef.num) continue;
        const a = DECK_CREW.find(x => x.p.id === o.by); if (!a) continue;
        const r = occasionAdd(id, shipNow() + 1); if (!r) continue;
        const ap = SHIP.device.appts.find(x => x.occ === r.key); if (!ap) { res.push([id, 'no appt']); continue; }
        // you, within 4 tiles of them, on their deck (wherever they are now)
        const c = nearestOpen(a.x + 1.5, a.z + 1.5, player), q = cellPos(...c); player.obj.position.copy(q); player.stop();
        const inRoom = (ROOMS[roomAt(...player.here())] || {}).name, room = o.room;
        const k = apptTapKeep(a.p, a.x, a.z);
        res.push({ occ: id, by: o.by, title: o.title, room, youIn: inRoom, them: (ROOMS[roomAt(...cellAt(a.x, a.z))] || {}).name, appt: ap.status, kept: !!k, occMet: !!r.met, occStatus: r.status });
        break; }
      return res; })()""")
      print(dk, out)
      if out: break
    g.close()
