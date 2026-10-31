# TB3 probe for TR1's item 2 (0.99.5, TRAD995_ON): your milestones and Open door, tap to join. For each, on its first day,
# 10 minutes in, in its room: the star and the arrow at its host, a tap joins you (one notice), and the host's card for the
# new hand's tea, six weeks and twelve weeks (its lines, a reply, the close); Four weeks and Open door: joined, no card of ours.
#   python3 plans/tb3-probes/milestones995.py starship-cadet.html
import sys, json, os, pathlib
sys.argv[0] = str(pathlib.Path(__file__).resolve().parents[2] / 'cadet_test.py')
exec(open(sys.argv[0]).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
build = sys.argv[1]; src = pathlib.Path(build).read_text()
on = src.replace("const TRAD995_ON = false ||", "const TRAD995_ON = true ||", 1); assert on != src
won = WORK / 'test' / ('_ms995_%d.html' % os.getpid()); won.write_text(on)
FAILS = []
def check(c, m):
    print(('ok   ' if c else 'FAIL ') + m)
    if not c: FAILS.append(m)
ONE = r"""(id => {
  let d = 1, e = null; for (; d < 120; d++) { e = eventsOn(d).find(x => x.id === id); if (e) break; }
  if (!e) return { id, err: 'not on' };
  goToDeck(e.ev.where[0].deck); actEnd(true); clearGoal(); setShipNow((d - 1) * 1440 + e.from + 10); deckCrewFill(); SHIP.events.joined = []; SHIP.device.settings.tips = false;
  for (const k of NEED_KEYS) SHIP.player.needs[k] = 90;
  if (!window.__th) { window.__th = 1; const t0 = toast; toast = function (a, b) { (window.__ts = window.__ts || []).push([a, b]); return t0.apply(this, arguments); }; }
  if (typeof GUIDE_ON !== 'undefined' && GUIDE_ON) { GUIDE.tq.length = 0; guideToast = () => false; }
  const rk = [...(e.rooms || (e.rooms = eventRooms(e.ev)))].map(r => r.split('|')).find(r => +r[0] === deckDef.num)[1], tl = ROOM_TILES[rk], c = cellPos(...tl[Math.floor(tl.length / 2)]);
  player.obj.position.copy(cellPos(...nearestOpen(c.x, c.z, player))); player.stop(); EV_MIN = -1; eventsTick(); tradJoinMinute(shipNow());
  const now = TJ_NOW && TJ_NOW.e.id === id ? TJ_NOW : TJ_ALL.find(x => x.e.id === id), goal = IX_GOAL && IX_GOAL.tj || null;
  window.__ts = []; const ok = now ? tradJoinTap(now.agent) : false, card = typeof DIALOGUE !== 'undefined' && DIALOGUE ? DIALOGUE.id : null, lines = [];
  { let k = 0; while (DIALOGUE && k++ < 20) { const v = dialogueView(); if (v) lines.push(v.text || (v.choices || []).join(' / ')); dialogueStep(v && v.choices ? 0 : undefined); } }
  const r = { id, d, at: hhmm(e.from), lead: now ? now.lead : null, goal, ok, joined: SHIP.events.joined.includes(id + '@' + d), card, lines, toasts: window.__ts.filter(t => t[0] === e.name).length, act: ACT ? ACT.kind : null };
  actEnd(true); return r;
})"""
with sync_playwright() as pw:
    g = Game(pw, str(won), 900, 760)
    for id, want in (('new-hands-tea', 'ms995.new-hands-tea'), ('four-weeks-aboard', None), ('six-weeks-aboard', 'ms995.six-weeks-aboard'), ('twelve-weeks-aboard', 'ms995.twelve-weeks-aboard'), ('open-door', None)):
        r = g.ev(f"({ONE})('{id}')"); print(json.dumps(r)[:600])
        if r.get('err'): check(False, '%s: %s' % (id, r['err'])); continue
        check(bool(r['lead']) and bool(r['goal']), '%s day %d: the star and the arrow (%s, %s)' % (id, r['d'], r['lead'], r['goal']))
        check(r['ok'] and r['joined'] and r['toasts'] == 1, '%s: a tap joins, one notice (%s, %s, %d)' % (id, r['ok'], r['joined'], r['toasts']))
        check(r['card'] == want and (want is None or len(r['lines']) >= 4), '%s: its card %s (%s, %d lines)' % (id, want, r['card'], len(r['lines'])))
    check(not g.errors, 'no errors %s' % g.errors[:3])
    g.close()
won.unlink(missing_ok=True)
print('MILESTONES PROBE ' + ('OK' if not FAILS else 'FAILED (%d)' % len(FAILS)))
