# #9 on the deck (patch builder B): play a stretch of a deck in real frames and count each planned toilet visit
# (whereIs act wash, tag toilet) of the crew on it: did they get onto the stall (settled at its spot) before the
# visit was over? Args: deck, start ship minute (day 1), real seconds. Prints visits, reached, and the misses.
from pp import *
dk, t0, secs = (int(x) for x in (sys.argv[1:4] if len(sys.argv) > 3 else (4, 400, 200)))
g = start('?nosave&debug')
g.step(5)
g.ev(f"(() => {{ skipTo({t0}); goToDeck({dk}); return 1; }})()")
g.ev("window.__skip = true"); g.secs(1)   # no drawing: the crew logic still runs every frame
seen = {}
for i in range(int(secs * 2)):
    g.secs(0.5)
    r = g.ev(r"""(() => { const now = shipNow(), out = []; for (const a of DECK_CREW) { const w = whereIs(a.p, now); if (!w || w.tag !== 'toilet' || w.deck !== deckDef.num) continue;
      out.push([a.p.id + '@' + hhmm(w.from % 1440), !!(a.settled && a.spot && a.spot.id === w.placeId), w.placeId]); } return out; })()""")
    for k, ok, pid in r:
        seen[k] = seen.get(k, False) or ok
n = len(seen); ok = sum(1 for v in seen.values() if v)
print('deck', dk, 'from', t0, 'for', secs, 's:', 'toilet visits seen', n, 'reached the stall', ok, 'missed', [k for k, v in seen.items() if not v][:20])
print(g.ev('clockText()'), g.errors[:3])
g.close()
