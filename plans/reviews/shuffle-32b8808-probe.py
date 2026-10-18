# Reviewer 1g: shuffle-aside (0.28.70) in busy play. The player keeps walking into crew on their feet (a tapped path to
# their tile, so head-on and from behind) on Deck 3 at dinner and Deck 4 in the evening; every frame, every crew member:
# on a free tile, not in a wall or furniture; counts the steps aside, a person stepped aside again and again (jitter or
# being herded along), how far each was moved in total, the player's stalls, and the polite words.
# Run: python3 shuffle_probe.py BUILD.html
import sys, json
exec(open(__file__.replace('shuffle-32b8808-probe.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
INST = """(() => { window.__sh = { steps: [], bad: [], said: 0, stall: 0, frames: 0 }; const T = window.__sh;
  const ot = toast; toast = (a, b) => { if (/steps aside/.test(b || '')) T.said++; return ot(a, b); };
  const os = SHUFFLE.set.bind(SHUFFLE); SHUFFLE.set = (a, s) => { const p = player.obj.position; T.steps.push([a.p && a.p.id, performance.now(), s.left, Math.round(a.x * 100) / 100, Math.round(a.z * 100) / 100, Math.round(s.x * 100) / 100, Math.round(s.z * 100) / 100, !!a.path.length, a.pose, Math.round(p.x * 100) / 100, Math.round(p.z * 100) / 100, (a.goalId || '') + '']); return os(a, s); };
  let last = null, still = 0;
  const ou = playerUpdate; playerUpdate = (dt, t) => { ou(dt, t); T.frames++;
    for (const a of SHUFFLE.keys()) { const c = cellAt(a.x, a.z); if (!free(...c)) T.bad.push([a.p && a.p.id, 'tile', c]);
      else { const q = { x: a.x, z: a.z }; collide(q, BODY_R, null); if (Math.hypot(q.x - a.x, q.z - a.z) > .05) T.bad.push([a.p && a.p.id, 'solid', [a.x, a.z]]); } }
    const p = player.obj.position; if (player.path.length && last && Math.hypot(p.x - last.x, p.z - last.z) < 1e-3) { if (++still === 45) T.stall++; } else still = 0; last = p.clone(); };
  return true; })()"""
CHASE = """(() => { if (player.path.length || ACT) return 0; const p = player.obj.position;
  const c = DECK_CREW.filter(a => shuffleable(a) && Math.hypot(a.x - p.x, a.z - p.z) > 2).sort((a, b) => Math.hypot(a.x - p.x, a.z - p.z) - Math.hypot(b.x - p.x, b.z - p.z))[%d %% 3];
  if (!c) return -1; const dx = c.x - p.x, dz = c.z - p.z, d = Math.hypot(dx, dz), t = nearestOpen(c.x + dx / d * 2, c.z + dz / d * 2, player); if (!t) return -1; playerGo(t, () => {}); return 1; })()"""
with sync_playwright() as pw:
    for deck, at in ((3, 18 * 60 + 5), (4, 21 * 60 + 30), (3, 7 * 60 + 10)):
        g = Game(pw, sys.argv[1], 390, 844)
        g.ev(f"setShipNow(Math.floor(shipNow() / 1440) * 1440 + 1440 * 2 + {at}); needsT = null"); g.ev(f"goToDeck({deck})"); g.step(60)
        g.ev(INST); goes = 0
        for k in range(300):                              # about 5 minutes of play at 30 fps
            r = g.ev(CHASE % k); goes += r == 1; g.step(30)
        T = g.ev("window.__sh"); st = T['steps']
        per = {}
        for s in st: per.setdefault(s[0], []).append(s[1])
        rapid = {k: len(v) for k, v in per.items() if any(v[i + 2] - v[i] < 3000 for i in range(len(v) - 2))}
        print(f"Deck {deck} at {at // 60:02d}:{at % 60:02d}: {goes} walks, {len(st)} steps aside by {len(per)} people, said {T['said']}, frames {T['frames']}, stalls {T['stall']}")
        print('   bad (in a wall / furniture / closed tile):', T['bad'][:6], len(T['bad']))
        print('   3+ steps within 3 s (jitter or herded):', rapid)
        for k in list(rapid)[:3]:
            print('   ', k, [(round(x[1] / 1000, 1), x[3], x[4], 'dir', x[5], x[6], x[2], 'walking' if x[7] else 'standing', x[8], 'you', x[9], x[10], x[11]) for x in st if x[0] == k])
        print('   step sizes:', sorted(set(round(s[2], 2) for s in st)))
        print('   errors:', g.errors[:3])
        g.close()
