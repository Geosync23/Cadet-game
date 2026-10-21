# PR7: opt #4 (keepShaders): program counts over laps of every deck by day, by night, after a week, and with the
# lights changing; every live program kept; programs bounded. python3 keep_probe7.py BUILD.html [mut]
import sys, os, json
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("a, shots = run(")[0])
DECKS = (3, 5, 2, 1, 6, 7, 4)
out = {}
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844); g.step(5)
    has = g.ev("typeof KEPT_PROGRAMS !== 'undefined'")
    for cond, js in (('day 12:00', 'setShipNow(11 * 1440 + 720)'), ('night 23:30', 'setShipNow(11 * 1440 + 1410)'), ('a week on, 18:00', 'skipTo(18 * 1440 + 1080)'), ('day again', 'setShipNow(18 * 1440 + 1440 + 600)')):
        g.ev(js); g.step(40)
        for lap in (1, 2):
            rows = []
            for n in DECKS:
                g.ev(f"goToDeck({n})"); g.step(4)
                rows.append(g.ev('renderer.info.programs.length'))
            out[(cond, lap)] = rows
            unkept = g.ev("renderer.info.programs.filter(p => typeof KEPT_PROGRAMS === 'undefined' || !KEPT_PROGRAMS.has(p)).length")
            print(f'{cond} lap {lap}: programs {rows}  not kept {unkept}', flush=True)
    print('errors', g.errors[:3]); g.close()
allv = [v for r in out.values() for v in r]
grow = [k for k in out if k[1] == 2 and out[k] != out[(k[0], 1)]]
print(f'max programs {max(allv)}; KEPT_PROGRAMS in build: {has}; lap 2 differs from lap 1 in: {grow}')
