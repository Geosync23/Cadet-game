# Does renderer.compile(scene, camera) right after a deck build take the cost out of the first frame?
import sys, os, re, time
src = open('/home/user/Cadet-game/cadet_test.py').read().split("import sys, json, hashlib")[0]
exec(src)
from playwright.sync_api import sync_playwright
J = """([n, warm]) => { const a = __realNow(); __sc('goToDeck(' + n + ')'); const b = __realNow(); const p0 = __sc('renderer.info.programs.length');
  if (warm) __sc('renderer.compile(scene, camera)'); const c = __realNow(); window.__skip = false; __step(1, 33); const d = __realNow();
  return [Math.round(b - a), Math.round(c - b), Math.round(d - c), p0, __sc('renderer.info.programs.length')]; }"""
with sync_playwright() as pw:
    for warm in (False, True, False, True):
        g = Game(pw, sys.argv[1], 390, 844)
        g.page.evaluate("window.__realNow = (() => { const f = Object.getPrototypeOf(performance).now.bind(performance); return () => f(); })()")
        rows = [g.page.evaluate(J, [n, warm]) for n in (3, 5, 2, 4)]
        print('compile' if warm else 'plain  ', ' | '.join(f'D{n}: build {r[0]} + compile {r[1]} + frame {r[2]} ms, programs {r[3]}->{r[4]}' for n, r in zip((3, 5, 2, 4), rows)), flush=True)
        g.close()
