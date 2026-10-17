# phone-like: CPU slowed 4x (set before load), one ship hour in the mess (3000 frames, drawing skipped), game code per frame
# usage (from a scratch folder, CADET_CHROME set): python3 plans/tools/phone.py BUILD.html SCENE(dinner|breakfast|sunline)
#   -> load seconds and frame stats as JSON. Alternate the builds and run each twice; report frames over 16.7/33 ms, p99, worst.
# Note: the player stands at nearestOpen of the mess hall's middle, which is in the bow lounge; the time covers the whole deck's crew either way.
import sys, time, json
src = open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..', '..', 'cadet_test.py')).read().split("a, shots = run(")[0]
sv = sys.argv; sys.argv = ['x']; exec(src); sys.argv = sv
from playwright.sync_api import sync_playwright
from playwright.sync_api._generated import Page
_goto = Page.goto
def goto(self, *a, **k):
    self._cdp = self.context.new_cdp_session(self); self._cdp.send('Emulation.setCPUThrottlingRate', {'rate': 4})
    return _goto(self, *a, **k)
Page.goto = goto
SCENES = {'dinner': 6*1440+18*60+25, 'breakfast': 1440+7*60+5, 'sunline': 6*1440+17*60+35}
path, scene = sys.argv[1], sys.argv[2]
with sync_playwright() as pw:
    t0 = time.time(); g = Game(pw, path); load = time.time() - t0
    g.ev(f"""(() => {{ skipTo({SCENES[scene]}); goToDeck(3); const b = ROOM_BOX['M'];
      const c = nearestOpen(Math.round((b.i0 + b.i1) / 2), Math.round((b.j0 + b.j1) / 2), player); player.obj.position.copy(cellPos(c[0], c[1])); }})()""")
    g.step(150)
    fs = []
    for k in range(10):
        fs += g.page.evaluate("""() => { window.__skip = true; const now = () => Performance.prototype.now.call(performance), out = [];
          for (let k = 0; k < 300; k++) { const t0 = now(); window.__step(1, 1000 / 30); out.push(now() - t0); } window.__skip = false; return out; }""")
    crew = g.ev("typeof DECK_CREW !== 'undefined' ? DECK_CREW.length : -1"); errs = g.errors[:3]
    g.close()
s = sorted(fs); n = len(s)
print(json.dumps({'build': path.split('/')[-1], 'scene': scene, 'load_s': round(load, 1), 'crew': crew, 'avg_ms': round(sum(s) / n, 2),
  'over16': sum(1 for x in s if x > 1000/60), 'over33': sum(1 for x in s if x > 1000/30), 'p99': round(s[int(n * .99)], 1), 'worst': round(s[-1], 1), 'errors': errs}))
