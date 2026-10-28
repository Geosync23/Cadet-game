#!/usr/bin/env python3
# path_check.py (the performance engineer, 0.27.29): checks that findPath (section 7, the heap search) finds exactly the
# same paths as findPathScan (the scan it replaced), tile for tile, and fails exactly where it failed.
#
#   CADET_CHROME=/opt/pw-browsers/chromium python3 path_check.py GAME.html [PAIRS_PER_DECK]
#
# 1. Every deck: PAIRS_PER_DECK (default 3000) searches between random tiles (open, blocked and off the grid), a third
#    with a random avoid set, for nobody, the player or a crew member; a fixed random stream, never the game's R().
# 2. A played ship day (day 1, a Monday: 06:00 to 23:00, moving between Decks 3, 4, 5 and 2): every real call, compared as it
#    happens (crewPath's doors opened for the moment, the same avoid sets).
# Also prints both searches' time on part 1. Ends "PATH CHECK OK" or "PATH CHECK: N problem(s)".
import sys, os, json
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
PAIRS = int(sys.argv[2]) if len(sys.argv) > 2 else 3000

RANDOM_JS = r"""(n => {
  let sd = 12345 + deckDef.num; const rnd = () => (sd = (sd * 16807) % 2147483647) / 2147483647, pick = a => a[Math.floor(rnd() * a.length)];
  const open = []; for (let i = 0; i < W; i++) for (let j = 0; j < D; j++) if (free(i, j)) open.push([i, j]);
  const whos = [null, player, ...DECK_CREW.slice(0, 6)], cases = [];
  for (let k = 0; k < n; k++) {
    const r = rnd(), tile = () => r < .8 ? pick(open).slice() : r < .95 ? [Math.floor(rnd() * W), Math.floor(rnd() * D)] : [Math.floor(rnd() * (W + 4)) - 2, Math.floor(rnd() * (D + 4)) - 2];
    let avoid = null; if (rnd() < .33) { avoid = new Set(); const m = 1 + Math.floor(rnd() * 12); for (let q = 0; q < m; q++) { const t = pick(open); avoid.add(t[0] + ',' + t[1]); } }
    cases.push([tile(), tile(), avoid, pick(whos)]);
  }
  const now = window.__realNow || (() => performance.now()), out = { n, open: open.length, same: 0, bad: [], found: 0, failed: 0 };
  let a = now(); const A = cases.map(([s, g, av, w]) => findPath(s, g, av, w)); out.newMs = +(now() - a).toFixed(1);
  a = now(); const B = cases.map(([s, g, av, w]) => findPathScan(s, g, av, w)); out.oldMs = +(now() - a).toFixed(1);
  cases.forEach((c, k) => { const x = JSON.stringify(A[k]), y = JSON.stringify(B[k]); if (x === y) out.same++; else if (out.bad.length < 5) out.bad.push({ s: c[0], g: c[1], avoid: c[2] && [...c[2]], new: x.slice(0, 200), old: y.slice(0, 200) }); if (B[k]) out.found++; else out.failed++; });
  return out;
})"""
LIVE_ON = r"""(() => { const F = findPath; window.__fpLive = { n: 0, same: 0, found: 0, bad: [] };
  findPath = (s, g, av, w) => { const r = F(s, g, av, w), o = findPathScan(s, g, av, w), L = window.__fpLive; L.n++; if (o) L.found++;
    if (JSON.stringify(r) === JSON.stringify(o)) L.same++; else if (L.bad.length < 5) L.bad.push({ s, g, avoid: av && [...av], new: JSON.stringify(r).slice(0, 200), old: JSON.stringify(o).slice(0, 200) }); return r; }; })()"""

bad = []
with sync_playwright() as pw:
    errs = []
    g = Game(pw, sys.argv[1], 390, 844, errs)
    g.page.evaluate("window.__realNow = (() => { const f = Object.getPrototypeOf(performance).now.bind(performance); return () => f(); })()")
    tn = to = 0
    for d in g.ev("Object.keys(DECKS).map(Number)"):
        g.ev(f"skipTo(1440 + 300); goToDeck({d})"); g.step(5)
        r = g.page.evaluate(f"s => window.__sc(s)({PAIRS})", RANDOM_JS)
        tn += r['newMs']; to += r['oldMs']
        print(f"Deck {d}: {r['same']}/{r['n']} the same ({r['found']} found, {r['failed']} no path; {r['open']} open tiles); new {r['newMs']} ms, old {r['oldMs']} ms")
        if r['same'] != r['n']: bad.append(f"Deck {d}: {r['n'] - r['same']} differ, e.g. {r['bad'][:2]}")
    print(f"All decks: new {tn:.0f} ms, old {to:.0f} ms ({to / max(tn, 1e-9):.1f}x faster)")
    g.ev(LIVE_ON)
    g.ev("skipTo(1440 + 360); goToDeck(3)"); g.step(5)
    for k, n in enumerate((3, 4, 5, 2, 3, 4)):            # 06:00 to 23:00, a deck change every ~3 hours, every frame stepped (drawing skipped)
        g.ev(f"goToDeck({n})")
        g.ev("window.__skip = true; window.__step(%d, 1000/30); window.__skip = false" % (170 * 50))
    L = g.ev("JSON.stringify(window.__fpLive)"); L = json.loads(L)
    print(f"A played day: {L['same']}/{L['n']} real calls the same ({L['found']} found a path)")
    if L['same'] != L['n']: bad.append(f"played day: {L['n'] - L['same']} differ, e.g. {L['bad'][:2]}")
    if L['n'] < 100: bad.append(f"played day: only {L['n']} calls seen")
    if errs: bad.append(f"errors: {errs[:4]}")
    g.close()
for b in bad: print('PROBLEM', b)
print('PATH CHECK OK' if not bad else f'PATH CHECK: {len(bad)} problem(s)')
sys.exit(1 if bad else 0)   # so a failing check fails for the computer too (check_fast.sh, GitHub)
