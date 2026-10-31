# TB3 probe for TR1's item 8 (0.99.5, TRAD995_ON): joining a tradition part-way gives one notice, and it says until when
# (not "About 46 minutes" for a 30-minute one, and not the same words again a minute later). Sunrise stretch, Knit and
# natter, Book circle: joined 13 minutes in; every pop-up for 4 ship minutes after the tap.
#   python3 plans/tb3-probes/toast995.py starship-cadet.html
import sys, json, os, pathlib
sys.argv[0] = str(pathlib.Path(__file__).resolve().parents[2] / 'cadet_test.py')
exec(open(sys.argv[0]).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
build = sys.argv[1]; src = pathlib.Path(build).read_text()
on = src.replace("const TRAD995_ON = false ||", "const TRAD995_ON = true ||", 1); assert on != src
won = WORK / 'test' / ('_toast995_%d.html' % os.getpid()); won.write_text(on)
FAILS = []
def check(c, m):
    print(('ok   ' if c else 'FAIL ') + m)
    if not c: FAILS.append(m)
ONE = r"""(id => {
  let d = 1, e = null; for (; d < 60; d++) { e = eventsOn(d).find(x => x.id === id); if (e) break; }
  goToDeck(e.ev.where[0].deck); actEnd(true); clearGoal(); setShipNow((d - 1) * 1440 + e.from + 13); deckCrewFill(); SHIP.events.joined = [];
  for (const k of NEED_KEYS) SHIP.player.needs[k] = 90;
  if (!window.__th) { window.__th = 1; const t0 = toast; toast = function (a, b) { (window.__ts = window.__ts || []).push([a, b]); return t0.apply(this, arguments); }; }
  if (typeof GUIDE_ON !== 'undefined' && GUIDE_ON) { GUIDE.tq.length = 0; guideToast = () => false; }
  const rk = [...(e.rooms || (e.rooms = eventRooms(e.ev)))].map(r => r.split('|')).find(r => +r[0] === deckDef.num)[1], tl = ROOM_TILES[rk], c = cellPos(...tl[Math.floor(tl.length / 2)]);
  player.obj.position.copy(cellPos(...nearestOpen(c.x, c.z, player))); player.stop(); EV_MIN = -1; eventsTick(); tradJoinMinute(shipNow());
  window.__ts = []; const a = TJ_NOW && TJ_NOW.e === e ? TJ_NOW.agent : tjAgent(tradLeader(e)); const ok = tradJoinTap(a);
  return { id, d, ok, end: hhmm(e.to) };
})"""
with sync_playwright() as pw:
    g = Game(pw, str(won), 900, 760)
    for id in ('sunrise-stretch', 'knit-and-natter', 'book-circle'):
        r = g.ev(f"({ONE})('{id}')"); g.step(240)
        ts = g.ev("window.__ts"); mine = [t for t in ts if t[0] == g.ev(f"eventsOn({r['d']}).find(x => x.id === '{id}').name")]
        print(id, r, mine)
        check(r['ok'] and len(mine) == 1, '%s: one notice (%d)' % (id, len(mine)))
        check(bool(mine) and ('till' in mine[0][1] or 'taken' in mine[0][1]) and 'About' not in mine[0][1], '%s: it says until when (%s)' % (id, mine[0][1] if mine else None))
        g.ev("actEnd(true)")
    check(not g.errors, 'no errors %s' % g.errors[:3])
    g.close()
won.unlink(missing_ok=True)
print('TOAST PROBE ' + ('OK' if not FAILS else 'FAILED (%d)' % len(FAILS)))
