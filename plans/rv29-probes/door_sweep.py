# RV29: PL2 note 13: every locked ('closed') door on Decks 1, 2, 4, 5, 6 (7 if built): stand on the open side next to it,
# Doors setting all / private / none: can you walk through (findPath to the far side), does it slide open for you
# (crewNearDoor's player branch with no crew near), edgeBlocks. Day 3 10:00, a junior. Prints per deck the doors you get through.
import sys, json, types
from playwright.sync_api import sync_playwright
src = open(sys.argv[1] + '/cadet_test.py').read(); src = src[:src.index('import sys, json, hashlib')]
ct = types.ModuleType('ct'); exec(src, ct.__dict__)
JS = r"""((n, mode, at) => { setShipNow(at); if (deckDef.num !== n) goToDeck(n); SHIP.device.settings.doors = mode;
  const out = [], LB = typeof lockedBehind === 'function' ? lockedBehind : null, crew0 = DECK_CREW.slice(); DECK_CREW.length = 0;
  for (const [k, e] of EDGES) { if (!e || e.type !== 'closed' || e.service) continue;
    const cs = e.horiz ? [[e.i, e.j - 1], [e.i, e.j]] : [[e.i - 1, e.j], [e.i, e.j]], rs = cs.map(c => roomAt(...c)); if (!rs[0] || !rs[1]) continue;
    for (let s = 0; s < 2; s++) { const me = cs[s], far = cs[1 - s]; if (!free(...me) || !free(...far)) continue;
      const p = cellPos(...me); player.obj.position.set(p.x, 0, p.z); player.path = [];
      const path = findPath(me, far, null, player), d = DOOR_OBJS.find(o => o.e.key === k), slide = d ? crewNearDoor(d) : null;
      out.push([k, rs[s] + '>' + rs[1 - s], !!path, slide, !!edgeBlocks(e, player), LB ? LB(rs[1 - s]) : null, LB ? LB(rs[s]) : null]); } }
  DECK_CREW.push(...crew0); return out; })"""
with sync_playwright() as pw:
    g = ct.Game(pw, sys.argv[2])
    g.ev("(() => { SHIP.device.settings.tips = false; })()")
    for n in [1, 2, 4, 5, 6]:
        for mode in ['private', 'all', 'none']:
            r = g.ev(JS + f"({n}, '{mode}', (3 - 1) * 1440 + 600)")
            through = [x for x in r if x[2] or x[3]]
            print(f"deck {n} {mode}: {len(r)} door sides; you get through {len(through)}: " + json.dumps(through)[:1500])
    print('errors', g.errors[:3]); g.close()
