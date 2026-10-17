#!/usr/bin/env python3
"""newgame_check.py BUILD.html — a fresh new game (no save, no ?nosave) starts on Day 0 at 17:30 (0.42.27+; 17:40 before) on Deck 5 by the
Tern's ramp with the intro on; a test URL (?nosave&debug) stays at Day 1 06:00 on Deck 4 with the intro off."""
import sys, os
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cadet_test.py')).read().split("a, shots = run(")[0]
exec(src.replace("'?nosave&debug'", "QUERY"))

STATE = "({ day: SHIP.time.day, min: SHIP.time.min, deck: typeof deckDef !== 'undefined' && deckDef ? deckDef.num : null, clock: clockText(), intro: typeof introOn === 'function' ? introOn() : null, step: SHIP.intro && SHIP.intro.step })"
ok = True
with sync_playwright() as pw:
    for name, q, want, tap in [('first-ever load (no save, never arrived)', '?debug', (0, 17 * 60 + 30, True), False),
                               ('New game tapped twice', '?debug', (0, 17 * 60 + 30, True), True),
                               ('test URL', '?nosave&debug', (1, 6 * 60, False), False)]:
        QUERY = q
        g = Game(pw, sys.argv[1])
        if tap:
            g.page.click('#newgame', force=True); g.page.click('#newgame', force=True); g.page.wait_for_timeout(3000)
        s = g.ev(STATE)
        errs = [e for e in g.errors if 'favicon' not in e]
        print(f"  {name} ({q}): {s['clock']}, deck {s['deck']}, intro on {s['intro']}, step {s['step']}, errors {len(errs)}")
        if want and (s['day'], round(s['min']), bool(s['intro'])) != want:
            ok = False; print(f"  FAIL {name}: wanted day {want[0]} {want[1] // 60:02d}:{want[1] % 60:02d}, intro {want[2]}")
        if errs: ok = False; print('  FAIL errors:', errs[:3])
        g.b.close()
print('NEWGAME OK' if ok else 'NEWGAME FAILED')
sys.exit(0 if ok else 1)
