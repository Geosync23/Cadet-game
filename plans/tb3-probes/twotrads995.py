# TB3 probe for TR1's item 5 (0.99.5, TRAD995_ON): two joinable traditions on one deck at once. For each case (day, minute,
# deck): every one on now is in TJ_ALL with its leader; standing in each one's room, the arrow and the tip are that one's
# (TJ_NOW); every other one has its own star (.tjMark2); a tap on that one's leader joins that one. Off: as before (one).
#   python3 plans/tb3-probes/twotrads995.py starship-cadet.html
import sys, json, os, pathlib
sys.argv[0] = str(pathlib.Path(__file__).resolve().parents[2] / 'cadet_test.py')
exec(open(sys.argv[0]).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright

build = sys.argv[1]; src = pathlib.Path(build).read_text()
on = src.replace("const TRAD995_ON = false ||", "const TRAD995_ON = true ||", 1); assert on != src
won = WORK / 'test' / ('_two995_%d.html' % os.getpid()); won.write_text(on)
FAILS = []
def check(c, m):
    print(('ok   ' if c else 'FAIL ') + m)
    if not c: FAILS.append(m)
# Day 57 (Monday) 21:20 on Deck 4: Book circle and Playlist duel; Day 6 (Saturday) 15:40 on Deck 3: Cook-along, the Tiles ladder
CASES = [(57, 1280, 4), (6, 945, 3), (20, 945, 3)]
ONE = r"""((d, m, n) => {
  goToDeck(n, null); actEnd(true); clearGoal(); setShipNow((d - 1) * 1440 + m); deckCrewFill(); SHIP.device.settings.tips = false;
  for (const k of NEED_KEYS) SHIP.player.needs[k] = 90; SHIP.events.joined = [];
  EV_MIN = -1; eventsTick(); tradJoinMinute(shipNow());
  const all = TJ_ALL.map(c => [c.e.id, c.lead]), out = { all, rooms: {} };
  for (const c of TJ_ALL.slice()) {
    const rk = [...c.e.rooms].map(r => r.split('|')).filter(r => +r[0] === n).map(r => r[1]).find(r => ROOM_TILES[r] && ROOM_TILES[r].length);
    const tl = ROOM_TILES[rk], p = cellPos(...tl[Math.floor(tl.length / 2)]); player.obj.position.copy(p); player.stop(); clearGoal();
    tradJoinMinute(shipNow()); tradJoinFrame();
    const marks = [...document.querySelectorAll('.tjMark2')].filter(e => e.textContent).map(e => e.textContent), other = TJ_ALL.find(x => x !== TJ_NOW);
    out.rooms[c.e.id] = { now: TJ_NOW && TJ_NOW.e.id, goal: IX_GOAL && IX_GOAL.tj || null, marks, want: other ? '★ ' + tjFirst(other.lead) : null, n: TJ_ALL.length };
  }
  // a tap on the leader of the one you're NOT in the room of
  const second = TJ_ALL.find(c => c !== TJ_NOW);
  const ok = second ? tradJoinTap(second.agent) : false; { let k = 0; while (typeof DIALOGUE !== 'undefined' && DIALOGUE && k++ < 20) { const v = dialogueView(); dialogueStep(v && v.choices ? 0 : undefined); } }   // a host's card first (0.93.2's): through it
  out.tap = second ? [second.e.id, ok, SHIP.events.joined.slice()] : null;
  actEnd(true); return out;
})"""
with sync_playwright() as pw:
    g = Game(pw, str(won), 900, 760)
    for d, m, n in CASES:
        r = g.ev(f"({ONE})({d}, {m}, {n})")
        print('Day %d %s, Deck %d: %s' % (d, g.ev(f"hhmm({m})"), n, json.dumps(r)))
        if len(r['all']) < 2: print('  (only one on now: nothing to compare)'); continue
        for id, x in r['rooms'].items():
            check(x['now'] == id and (x['goal'] or '').startswith(id), 'Day %d: in %s\'s room, its arrow and tip (%s, %s)' % (d, id, x['now'], x['goal']))
            check(x['want'] in x['marks'], 'Day %d: in %s\'s room, the other one has its star (%s in %s)' % (d, id, x['want'], x['marks']))
        check(bool(r['tap']) and r['tap'][1] and any(k.startswith(r['tap'][0] + '@') for k in r['tap'][2]), 'Day %d: a tap on the other one\'s leader joins it (%s)' % (d, r['tap']))
    check(not g.errors, 'no errors %s' % g.errors[:3])
    g.close()
won.unlink(missing_ok=True)
print('TWO TRADS PROBE ' + ('OK' if not FAILS else 'FAILED (%d)' % len(FAILS)))
