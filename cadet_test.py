# Starship Cadet: regression test (keep in the Project)
# Compares two builds headlessly: game state, 300 paths, 3000 collision probes,
# crew positions, tap results, and screenshots across rotate / walls / night /
# shadows / crew / taps / steering. Deterministic: virtual clock, manual frames.
# Setup in a fresh container:
#   mkdir -p $CADET_WORK/three && cd $CADET_WORK/three && npm pack three@0.128.0 && tar xzf three-0.128.0.tgz
#   (CADET_WORK defaults to /tmp/cadet-work)
# Run:  python3 cadet_test.py OLD.html NEW.html     (screenshots land in the current folder)
# Builds must share a random seed for screenshots to match pixel for pixel.
# Deterministic headless runner for Starship Cadet builds.
# Virtual clock + manual frame stepping, three.js served locally, a direct-eval hook into the game's scope.
import json, sys, re, pathlib, hashlib, os
from playwright.sync_api import sync_playwright

WORK = pathlib.Path(os.environ.get('CADET_WORK', '/tmp/cadet-work'))
(WORK / 'test').mkdir(parents=True, exist_ok=True)
THREE = (WORK / 'three/package/build/three.min.js').read_text()
INIT = """
(() => {
  let vt = 1000; const cbs = [];
  performance.now = () => vt; Date.now = () => vt;
  window.requestAnimationFrame = cb => { cbs.push(cb); return cbs.length; };
  window.__step = (n, dtMs) => { for (let k = 0; k < n; k++) { vt += dtMs; const q = cbs.splice(0); for (const cb of q) cb(vt); } };
})();
"""
HOOK = "window.__sc = src => eval(src);\n"

def instrument(html):
    # expose the game's scope to tests: direct eval inside the IIFE, added just before the closing of it
    i = html.rfind('})();')
    return html[:i] + HOOK + html[i:]

class Game:
    def __init__(self, pw, path, w=900, h=760, errors=None):
        self.errors = [] if errors is None else errors
        b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
        self.b = b
        self.page = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=1)
        self.page.on('console', lambda m: m.type in ('error', 'warning') and self.errors.append(f'{m.type}: {m.text}'))
        self.page.on('pageerror', lambda e: self.errors.append(f'pageerror: {e}'))
        self.page.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
        self.page.add_init_script(INIT)
        html = instrument(pathlib.Path(path).read_text())
        tmp = WORK / 'test' / ('_run_' + pathlib.Path(path).name)
        tmp.write_text(html)
        # ?nosave: tests never read or write a save (0.15.1). ?debug: shows the Night/Day button the shots use.
        # Builds before 0.15.1 ignore both.
        self.page.goto('file://' + str(tmp) + '?nosave&debug')
        # toasts fade on real-time timers and CSS transitions, not the virtual clock: keep them out of screenshots
        # (their text is still read from the DOM) so shots don't depend on how fast the machine runs
        self.page.add_style_tag(content='#toast,.nf{opacity:0!important} *,*::before,*::after{transition:none!important;animation:none!important}')   # .nf: the needs' floating notes, gone on a real-time timer too
        try:
            self.page.wait_for_function('window.__sc !== undefined || window.__err', timeout=60000)
        except Exception:
            pass
        if self.page.evaluate('window.__sc === undefined'):
            raise RuntimeError('game failed to start: ' + ' | '.join(self.errors[:6]))
        # headless rendering is slow: simulate every frame, but only draw the last one of each step
        self.ev("(() => { const rr = renderer.render.bind(renderer); window.__skip = false; renderer.render = (s, c) => { if (!window.__skip) rr(s, c); }; })()")
    def ev(self, src):
        return self.page.evaluate('s => window.__sc(s)', src)
    def step(self, n, dt=1000/30):
        if n > 1: self.page.evaluate(f'window.__skip = true; window.__step({n - 1}, {dt}); window.__skip = false')
        self.page.evaluate(f'window.__step(1, {dt})')
    def shot(self, path):
        self.page.screenshot(path=path)
    def close(self):
        self.b.close()

import sys, json, hashlib
import numpy as np
from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright

STATE = r'''(() => {
  const r = v => Math.round(v * 1e4) / 1e4;
  return {
    size: [W, D],
    edges: [...EDGES.values()].map(e => [e.key, e.type, r(e.cx), r(e.cz), e.hull, e.out, e.wx === undefined ? null : [r(e.wx), r(e.wz), r(e.sx)], e.hrun ? e.hrun.room : null]),
    runs: RUNS.map(x => [x.edges.length, x.out, x.room || null, r(x.cx || 0), r(x.cz || 0)]),
    posts: POSTS.map(p => [r(p.cx), r(p.cz), p.full, p.touch.map(e => e.key)]),
    blocked: [...BLOCKED].sort(), stand: [...STAND].sort(),
    items: ITEMS.map(i => [i.t, i.x, r(i.front), r(i.depth), !!i.wall]),
    spots: SPOTS.map(s => [s.room, s.tag, r(s.x), r(s.z), r(s.front)]),
    roomBox: ROOM_BOX, roomTiles: ROOM_TILES, closed: CLOSED_DOORS,
    doors: DOOR_OBJS.map(d => [d.e.key, d.passable]),
    voids: VOID_BLOCKS.map(v => [r(v.cx), r(v.cz)]),
    tall: TALL.map(t => [t.pts.length, t.mats.length]), noFade: [...NO_FADE].sort(),
    lamps: LAMPS.length, steam: STEAM.length, dust: DUST.length, hullPts: HULL_PTS.length, hullRuns: HULL_RUNS.map(h => [h.room, h.edges.length]),
    wallDecor: WALL_DECOR.length, map: MAP,
    mem: renderer.info.memory, calls: renderer.info.render.calls, tris: renderer.info.render.triangles,
    seedNow: seed,
  };
})()'''
WALKERS = "walkers.map(w => [w.spec.name, Math.round(w.obj.position.x * 1e4), Math.round(w.obj.position.z * 1e4), Math.round(w.obj.rotation.y * 1e3), w.goal])"
PATHS = r'''(() => { const out = []; let s = 7; const rnd = () => (s = (s * 48271) % 2147483647) / 2147483647;
  for (let k = 0; k < 300; k++) { const a = [Math.floor(rnd() * W), Math.floor(rnd() * D)], b = [Math.floor(rnd() * W), Math.floor(rnd() * D)];
    const p = free(...a) && free(...b) ? findPath(a, b) : 'x'; out.push(p === null ? null : (p === 'x' ? 'x' : p.length + ':' + p.map(c => c.join(',')).join(' ')));
  } return out; })()'''
COLLIDE = r'''(() => { const out = []; let s = 3; const rnd = () => (s = (s * 48271) % 2147483647) / 2147483647;
  for (let k = 0; k < 3000; k++) { const p = new THREE.Vector3((rnd() - .5) * W * 1.1, 0, (rnd() - .5) * D * 1.1); collide(p, BODY_R); out.push([Math.round(p.x * 1e5), Math.round(p.z * 1e5)]); }
  return out; })()'''

def run(path, tag):
    res = {}
    shots = []
    with sync_playwright() as pw:
        g = Game(pw, path)
        res['state'] = g.ev(STATE)
        res['paths'] = g.ev(PATHS)
        res['collide'] = g.ev(COLLIDE)
        def snap(name):
            g.shot(f'{tag}_{name}.png'); shots.append(name)
            res['walk_' + name] = g.ev(WALKERS)
        g.step(40); snap('a_start')
        g.step(300); snap('b_wander10s')
        g.page.click('#rot'); g.step(40); snap('c_rotated')
        g.page.click('#walls'); g.step(40); snap('d_wallslow')
        # back to automatic walls (one click on builds before 0.5.8, two from 0.5.8: down, up, auto)
        while g.ev("typeof wallsMode === 'undefined' ? wallsLow : wallsMode !== 'auto'"): g.page.click('#walls')
        g.page.click('#light'); g.step(80); snap('e_night')
        g.page.click('#light'); g.page.click('#shad'); g.step(20); snap('f_noshadow')
        g.page.click('#shad'); g.page.click('#crew'); g.step(20); snap('g_nocrew')
        g.page.click('#crew'); g.step(20); snap('h_crewback')
        # taps: walk to things on screen, then read the toast
        for k, (x, y) in enumerate([(450, 380), (700, 300), (300, 520), (600, 600), (150, 250)]):
            g.page.mouse.move(x, y); g.page.mouse.down(); g.page.mouse.up(); g.step(150)
            res[f'tap{k}'] = [g.page.inner_text('#tt'), g.page.inner_text('#tx'), g.page.inner_text('#room')]
            snap(f'i_tap{k}')
        # press and hold: steer the player around for a while
        g.ev("player.steer = { x: .8, z: .6, k: 1 }"); g.step(120); snap('j_steer1')
        g.ev("player.steer = { x: -1, z: 0, k: 1 }"); g.step(200); snap('j_steer2')
        g.ev("player.steer = null")
        res['state_end'] = g.ev("[renderer.info.memory, renderer.info.render.calls, document.getElementById('room').textContent, document.querySelector('.hud .sub').textContent]")
        res['errors'] = g.errors
        g.close()
    return res, shots

a, shots = run(sys.argv[1], 'A')
b, _ = run(sys.argv[2], 'B')
ok = True; noise = False
for k in a:
    if k == 'errors': continue
    same = json.dumps(a[k], sort_keys=True) == json.dumps(b[k], sort_keys=True)
    if not same:
        ok = False
        if isinstance(a[k], dict):
            diff = [kk for kk in a[k] if json.dumps(a[k].get(kk), sort_keys=True) != json.dumps(b[k].get(kk), sort_keys=True)]
            print('DIFF', k, diff)
        else: print('DIFF', k, str(a[k])[:200], '|', str(b[k])[:200])
for s in shots:
    A = np.array(Image.open(f'A_{s}.png').convert('RGB')).astype(int); B = np.array(Image.open(f'B_{s}.png').convert('RGB')).astype(int)
    d = np.abs(A - B).max(axis=2); n = int((d > 0).sum())
    print(f'{s:14s} differing px {n:6d}  max {int(d.max())}')
    # the software renderer in cloud containers (SwiftShader) sometimes rounds a few dozen pixels one level
    # differently from run to run, even for the same build: a difference of at most 1 is that, not a change
    if d.max() > 1: ok = False
    elif n: noise = True
print('errors A', a['errors'][:3], 'errors B', b['errors'][:3])
print('taps', [a[f'tap{k}'][0] for k in range(5)])
print(('ALL IDENTICAL' + (' (apart from renderer noise: some pixels 1 level off)' if noise else '')) if ok else 'DIFFERENCES FOUND')
