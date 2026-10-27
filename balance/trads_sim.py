# BAL1: the traditions and gatherings calendar from the game's own eventsOn(d), Days 1..N: count a day, evening ones,
# overlaps (you can't be at both), evening minutes covered, by weekday. Run: python3 balance/trads_sim.py BUILD.html 56
import sys, json, pathlib
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parent
exec(open(str(ROOT / 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
days = int(sys.argv[2]) if len(sys.argv) > 2 else 56
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1])
    r = g.ev(f"""(() => {{ const out = []; for (let d = 1; d <= {days}; d++) {{ let L = []; try {{ L = eventsOn(d); }} catch (e) {{ L = [{{ err: String(e) }}]; }}
      out.push({{ d, wd: weekday(d), work: playerShiftOn(d), list: L.map(e => ({{ id: e.id, name: e.name || e.id, from: e.from, to: e.to, meal: !!e.meal, every: e.when && (e.when.every || e.when.weekly || null), kind: e.kind || null }})) }}); }}
      return out; }})()""")
    (HERE / 'data' / 'trads.json').write_text(json.dumps(r, indent=0))
    for x in r[:14]: print(x['d'], x['wd'], x['work'], [(e['name'], e['from'], e['to']) for e in x['list']])
