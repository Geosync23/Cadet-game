# Keep every compiled shader program alive across deck changes (three r128: a program is deleted when its last material is disposed)
import sys, os, re, time
src = open('/home/user/Cadet-game/cadet_test.py').read().split("import sys, json, hashlib")[0]
exec(src)
from playwright.sync_api import sync_playwright
KEEP = """(() => { const seen = new Set(); window.__keepTick = () => { for (const p of renderer.info.programs) if (!seen.has(p)) { seen.add(p); p.usedTimes++; } }; })()"""
J = """([n, keep]) => { const a = __realNow(); __sc('goToDeck(' + n + ')'); const b = __realNow(); window.__skip = false; __step(1, 33); if (keep) __sc('__keepTick()'); const d = __realNow();
  return [Math.round(b - a), Math.round(d - b), __sc('renderer.info.programs.length')]; }"""
with sync_playwright() as pw:
    for keep in (False, True):
        g = Game(pw, sys.argv[1], 390, 844)
        g.page.evaluate("window.__realNow = (() => { const f = Object.getPrototypeOf(performance).now.bind(performance); return () => f(); })()")
        if keep: g.ev(KEEP); g.ev('__keepTick()')
        for lap in (1, 2):
            rows = [g.page.evaluate(J, [n, keep]) for n in (3, 5, 2, 1, 6, 7, 4)]
            print('keep ' if keep else 'plain', f'lap {lap}:', ' | '.join(f'D{n} {r[0]}+{r[1]} ms p{r[2]}' for n, r in zip((3, 5, 2, 1, 6, 7, 4), rows)), '| frames total', sum(r[1] for r in rows), 'ms', flush=True)
        g.close()
