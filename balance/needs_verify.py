# BAL1: checks needs_sim.py's arithmetic against the game's own needsDrain (same starts, same minutes)
import sys, json, pathlib, os
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parent
exec(open(str(ROOT / 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
sys.path.insert(0, str(HERE)); import needs_sim as N
cases = [('awake 16h', dict(N.FRESH), 960, False), ('asleep 8h', dict(hunger=50, energy=20, hygiene=50, fitness=50, social=50, bathroom=50, leisure=50), 480, True),
         ('awake 10h low', dict(hunger=30, energy=30, hygiene=20, fitness=20, social=20, bathroom=20, leisure=20), 600, False)]
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1])
    for name, start, mins, asleep in cases:
        game = g.ev(f"(() => {{ Object.assign(SHIP.player.needs, {json.dumps(start)}); needsDrain({mins}, {str(asleep).lower()}, {{}}); return {{ ...SHIP.player.needs }}; }})()")
        p = N.P(); p.n = dict(start); p.drain(mins, asleep=asleep)
        diff = max(abs(game[k] - p.n[k]) for k in N.K)
        print(name, 'max difference', round(diff, 4), {k: round(game[k], 1) for k in N.K})
