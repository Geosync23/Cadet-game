# TR1 follow-ups in the game: Winner Stays On / the Lightdisc Cup mid-afternoon (Day 7 13:30, Day 28 13:30) and the quiet watch (Day 300 21:50)
import sys, json
sys.argv, ARGS = sys.argv[:1], sys.argv[1:]
exec(open("/home/user/cadet-game/cadet_test.py").read().split("a, shots = run(")[0].replace("timeout=60000", "timeout=240000"))
LOOK = """JSON.stringify((() => { const d = %d, e = eventsOn(d).find(x => x.id === '%s'); if (!e) return 'not on'; if (!e.rooms) e.rooms = eventRooms(e.ev); const ids = tradSpotIds(e);
  const tag = DECK_CREW.filter(a => a.p && evTagId(a.tag || '') === e.id);
  return { m: hhmm(SHIP.time.min %% 1440), planned: tradGoers(e).length, onDeck: tag.length, settled: tag.filter(a => a.settled).length, atIts: tag.filter(a => a.settled && a.spot && ids.has(a.spot.id)).length,
    spots: [...new Set(tag.filter(a => a.spot).map(a => a.spot.id.replace(/-\\d+$/, '')))].slice(0, 8), its: [...ids].slice(0, 6), rooms: [...e.rooms] }; })())"""
with sync_playwright() as pw:
    for d, t, deck, tid in [(7, 13 * 60 + 30, 7, 'rec-wso'), (28, 13 * 60 + 30, 7, 'rec-cup'), (300, 21 * 60 + 45, 1, 'quiet-watch')]:
        g = Game(pw, ARGS[0], 600, 500); g.ev("skipTo(%d); goToDeck(%d, null)" % ((d - 1) * 1440 + t, deck)); g.step(40)
        for k in range(3): g.step(60)
        print(tid, d, g.ev(LOOK % (d, tid))); g.close()
