# Starship Cadet: controller check (section 26, controller support CT1; plans/controller-plan.html)
# Plays the game with a PRETEND controller: before the game loads, the browser's controller list
# (navigator.getGamepads) is replaced by scripted pads whose buttons and sticks the check sets frame by frame, and
# their hello and goodbye are announced the way a real pad's are (gamepadconnected / gamepaddisconnected).
# The game file's switch PAD_ON is flipped on in a copy (the "on" build); the file as given is the "off" build.
# Parts (turn 1, the base):
#   off:    with the switch off, a pad saying hello and pressing buttons changes nothing (no PAD.live, no body.pad)
#   quiet:  with the switch on and no pad: nothing new on the page (elements, styles, body classes), PAD.live false
#   base:   hello; a press fires once and marks the controller in use (body.pad); its release; the dead zones (sticks,
#           triggers); a held D-pad repeats (after 0.5 s, then every 0.25 s); a touch, the mouse or the wheel hands
#           back (body.pad goes); the pad families from their names; a non-standard pad; two pads (the last to press
#           is in charge); a disconnect lets go of everything and says whether the pad was in use; the last pad going
#           leaves PAD.live false
# Setup and environment as for cadet_test.py (CADET_WORK, CADET_CHROME).
# Run:  python3 controller_check.py BUILD.html [part ...]    Good is CONTROLLER CHECK OK (exit 0); a failure exits 1.
import sys, os, re, json, pathlib
exec(open(__file__.replace('controller_check.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright

ok = True
def fail(msg):
    global ok
    ok = False
    print('FAIL', msg)
def check(cond, msg):
    if not cond: fail(msg)
    return cond

# the pretend controller, installed before the game's script runs
FAKEPAD = r"""
(() => {
  const mk = (i, id, mapping) => ({ index: i, id, mapping, connected: true, timestamp: 0, axes: [0, 0, 0, 0],
    buttons: Array.from({ length: 17 }, () => ({ pressed: false, touched: false, value: 0 })) });
  window.__pads = [null, null, null, null];
  Object.defineProperty(navigator, 'getGamepads', { value: () => window.__pads.slice(), configurable: true });
  window.__padPlug = (i, id, mapping) => { window.__pads[i] = mk(i, id || 'Xbox Wireless Controller (STANDARD GAMEPAD Vendor: 045e Product: 0b13)', mapping === undefined ? 'standard' : mapping); return true; };
  window.__padHello = i => { const e = new Event('gamepadconnected'); e.gamepad = window.__pads[i]; dispatchEvent(e); return true; };
  window.__padUnplug = i => { const g = window.__pads[i]; if (!g) return false; g.connected = false; window.__pads[i] = null;
    const e = new Event('gamepaddisconnected'); e.gamepad = g; dispatchEvent(e); return true; };
  window.__padBtn = (i, k, v) => { const b = window.__pads[i].buttons[k]; b.value = +v; b.pressed = +v > .5; b.touched = +v > 0; return true; };
  window.__padAxes = (i, a) => { window.__pads[i].axes = a.slice(); return true; };
})();
"""
INIT = INIT + FAKEPAD                              # Game() installs INIT before the game loads
BTN = {n: k for k, n in enumerate(['a', 'b', 'x', 'y', 'lb', 'rb', 'lt', 'rt', 'view', 'menu', 'ls', 'rs', 'up', 'down', 'left', 'right'])}

GAME = sys.argv[1]
ONLY = set(sys.argv[2:])
SRC = pathlib.Path(GAME).read_text()
if not check('const PAD_ON = false;' in SRC, 'the game has no "const PAD_ON = false;" switch line'):
    print('CONTROLLER CHECK FAILED'); sys.exit(1)
ON = WORK / 'test' / ('_pad_on_' + pathlib.Path(GAME).name)
ON.write_text(SRC.replace('const PAD_ON = false;', 'const PAD_ON = true;', 1))

class Pad:
    """The game with a pretend controller: plug, hello, press, sticks, step."""
    def __init__(self, pw, path, w=390, h=844):
        self.g = Game(pw, str(path), w, h)
        self.g.ev("SHIP.device && SHIP.device.settings && (SHIP.device.settings.tips = false)")
        self.g.step(10)
    def js(self, src): return self.g.page.evaluate(src)
    def ev(self, src): return self.g.ev(src)
    def step(self, n=1): self.g.step(n)
    def plug(self, i=0, id=None, mapping='standard', hello=True):
        self.js(f'window.__padPlug({i}, {json.dumps(id)}, {json.dumps(mapping)})')
        if hello: self.js(f'window.__padHello({i})')
    def btn(self, name, v=1, i=0): self.js(f'window.__padBtn({i}, {BTN[name]}, {v})')
    def axes(self, a, i=0): self.js(f'window.__padAxes({i}, {json.dumps(a)})')
    def press(self, name, i=0, frames=2):
        self.btn(name, 1, i); self.step(frames); self.btn(name, 0, i); self.step(1)
    def log(self, clear=True):
        out = self.ev('(PAD.log || []).slice()')
        if clear: self.ev('PAD.log = []')
        return out
    def close(self):
        errs = [e for e in self.g.errors if 'error' in e]
        check(not errs, 'page errors: ' + ' | '.join(errs[:4]))
        self.g.close()

PAGE_SHAPE = "(() => ({ kids: [...document.body.children].map(e => e.tagName + '#' + e.id).join(' '), styles: document.querySelectorAll('style').length, cls: document.body.className, live: typeof PAD === 'object' ? PAD.live : null }))()"

def part_off(pw):
    p = Pad(pw, GAME)
    p.plug(); p.ev('PAD.log = []'); p.press('a'); p.axes([1, 0, 0, 0]); p.step(5)
    check(p.ev('PAD.live') is False, 'off: PAD.live went true with the switch off')
    check('pad' not in p.ev('document.body.className'), 'off: body.pad with the switch off')
    check(p.ev('PAD.log') == [], 'off: something fired with the switch off')
    p.close()

def part_quiet(pw):
    a = Pad(pw, GAME); sa = a.ev(PAGE_SHAPE); a.close()
    b = Pad(pw, ON); sb = b.ev(PAGE_SHAPE); b.close()
    check(sa == sb, f'quiet: the page differs with the switch on and no pad: {sa} vs {sb}')
    check(sb['live'] is False, 'quiet: PAD.live true with no pad')

def part_base(pw):
    p = Pad(pw, ON)
    p.plug(); p.ev('PAD.log = []')
    check(p.ev('PAD.live') is True, 'base: hello did not make PAD.live')
    p.step(3)
    check(p.ev('PAD.used') is False and p.log() == ['frame'] * 3, 'base: an idle pad counted as in use, or fired more than frame')
    p.btn('a'); p.step(1)
    l = p.log(); check(l[:2] == ['use', 'a'], f'base: a press should fire use then a: {l}')
    check(p.ev('PAD.used') and 'pad' in p.ev('document.body.className'), 'base: a press did not mark the pad in use')
    p.step(10); l = p.log(); check('a' not in l and 'a+' not in l, f'base: a held A fired again: {l}')
    p.btn('a', 0); p.step(1); check('a:up' in p.log(), 'base: no a:up on release')
    # dead zones
    p.axes([.15, .1, 0, 0]); p.step(1); check(p.ev('PAD.ls') == [0, 0], 'base: a stick inside the dead zone moved')
    p.axes([1, 0, 0, -1]); p.step(1); ls, rs = p.ev('PAD.ls'), p.ev('PAD.rs')
    check(abs(ls[0] - 1) < 1e-6 and abs(rs[1] + 1) < 1e-6, f'base: full sticks should read 1: {ls} {rs}')
    p.axes([.5, 0, 0, 0]); p.step(1); x = p.ev('PAD.ls[0]'); check(.3 < x < .4, f'base: half a stick should read about .36: {x}')
    p.axes([0, 0, 0, 0]); p.btn('rt', .3); p.step(1); l = p.log()
    rt = p.ev('PAD.rt'); check(.15 < rt < .25 and 'rt' not in l, f'base: a light trigger: rt {rt}, fired {l}')
    p.btn('rt', .8); p.step(1); check('rt' in p.log(), 'base: a trigger past half way did not fire')
    p.btn('rt', 0); p.step(1); p.log()
    # a held D-pad repeats: 1.2 s at 30 frames a second -> the press, then repeats at 0.5, 0.75, 1.0 s
    p.btn('down'); p.step(36); l = [x for x in p.log() if x.startswith('down')]
    check(l == ['down', 'down+', 'down+', 'down+'], f'base: a held D-pad should repeat three times in 1.2 s: {l}')
    p.btn('down', 0); p.step(1); p.log()
    # a touch hands back
    p.press('b'); p.log()
    p.js("document.body.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))")
    check(p.ev('PAD.used') is False and 'pad' not in p.ev('document.body.className') and 'unuse' in p.log(), 'base: a touch did not hand back')
    p.press('x'); p.js("document.body.dispatchEvent(new WheelEvent('wheel', { bubbles: true, deltaY: 1 }))")
    check(p.ev('PAD.used') is False, 'base: the wheel did not hand back')
    p.press('x'); p.js("document.body.dispatchEvent(new MouseEvent('mousemove', { bubbles: true, movementX: 0, movementY: 0 }))")
    check(p.ev('PAD.used') is True, 'base: a mousemove without movement handed back')
    # families and a non-standard pad
    for pid, fam in [('Wireless Controller (STANDARD GAMEPAD Vendor: 054c Product: 09cc)', 'ps'), ('DualSense Wireless Controller', 'ps'),
                     ('Pro Controller (STANDARD GAMEPAD Vendor: 057e Product: 2009)', 'nin'), ('Backbone One', 'xbox'), ('Razer Kishi V2', 'xbox'), ('Xbox Wireless Controller (STANDARD GAMEPAD Vendor: 045e Product: 0b13)', 'xbox')]:
        check(p.ev(f'padFamily({json.dumps(pid)})') == fam, f'base: padFamily({pid}) should be {fam}')
    p.plug(1, 'Pro Controller (Vendor: 057e Product: 2009)', ''); p.log()
    p.btn('b', 1, 1); p.step(1); l = p.log()
    check(p.ev('PAD.idx') == 1 and p.ev('PAD.std') is False and p.ev('PAD.fam') == 'nin' and 'b' in l, f'base: the second pad pressing B should take charge (non-standard, nin): {l}')
    p.btn('b', 0, 1); p.step(1)
    p.btn('a', 1, 0); p.step(1); check(p.ev('PAD.idx') == 0 and p.ev('PAD.fam') == 'xbox', 'base: the first pad pressing again should take charge back')
    # a disconnect while holding A, in use
    p.log(); p.js('window.__padUnplug(0)'); l = p.log()
    check('a:up' in l and 'release' in l and 'gone' in l and p.ev('PAD.goneUsed') is True, f'base: unplugging the pad in charge: {l}')
    check(p.ev('PAD.live') is True, 'base: one pad still plugged in, PAD.live should stay')
    p.step(2); check(p.ev('PAD.idx') == 1, 'base: the other pad should be in charge')
    p.js('window.__padUnplug(1)'); p.step(2)
    check(p.ev('PAD.live') is False, 'base: no pads left, PAD.live should be false')
    p.close()

SCREEN = "(() => { const v = player.obj.position.clone().project(camera); return [v.x * innerWidth / 2, -v.y * innerHeight / 2, player.obj.position.x, player.obj.position.z]; })()"
def settle(p, n=40):
    p.step(n)

def part_deck(pw):
    p = Pad(pw, ON)
    p.plug(); p.press('a'); p.log()
    # walking: in each of the four view directions, each stick direction that moves you moves you that way on screen.
    # From the most open floor on the deck (a free tile with the most free tiles within two), so furniture rarely slides you
    p.ev("""(() => { let best = null, bn = -1; for (let i = 2; i < W - 2; i++) for (let j = 2; j < D - 2; j++) { if (!free(i, j)) continue;
      let n = 0; for (let a = -2; a <= 2; a++) for (let b = -2; b <= 2; b++) if (free(i + a, j + b)) n++; if (n > bn) { bn = n; best = [i, j]; } }
      player.stop(); player.obj.position.copy(cellPos(best[0], best[1])); target.copy(player.obj.position).setY(.7); return best; })()""")
    for turn in range(4):
        p.ev(f'azT = az = Math.PI / 4 + {turn} * Math.PI / 2'); settle(p, 10)
        moved = 0
        for name, (sx, sy) in [('up', (0, -1)), ('right', (1, 0)), ('down', (0, 1)), ('left', (-1, 0))]:
            a = p.ev(SCREEN); p.axes([sx, sy, 0, 0]); p.step(2)
            # the way the stick asks you to walk, on screen: exactly the stick's way
            ex, ey = p.ev("(() => { const s = player.steer, A = new THREE.Vector3(0, 0, 0).project(camera), B = new THREE.Vector3(s.x, 0, s.z).project(camera); return [(B.x - A.x) * innerWidth / 2, -(B.y - A.y) * innerHeight / 2]; })()")
            en = (ex * ex + ey * ey) ** .5 or 1
            check((ex * sx + ey * sy) / en > .999, f'deck: view {turn}, stick {name}: asks to walk the wrong way on screen ({ex:.1f}, {ey:.1f})')
            p.step(18); b = p.ev(SCREEN); p.axes([0, 0, 0, 0]); p.step(2)
            dist = ((b[2] - a[2]) ** 2 + (b[3] - a[3]) ** 2) ** .5
            if dist < .3: continue
            moved += 1
            # both places through this frame's camera (the camera follows you, so screen positions taken at different
            # times would drift back toward the middle)
            dx, dy = p.ev(f"(() => {{ const A = new THREE.Vector3({a[2]}, 0, {a[3]}).project(camera), B = new THREE.Vector3({b[2]}, 0, {b[3]}).project(camera); return [(B.x - A.x) * innerWidth / 2, -(B.y - A.y) * innerHeight / 2]; }})()")
            n = (dx * dx + dy * dy) ** .5 or 1
            dot = (dx * sx + dy * sy) / n
            check(dot > .5, f'deck: view {turn}, stick {name}: walked the wrong way on screen ({dx:.1f}, {dy:.1f})')   # loose: furniture slides you along
            # walking back where we came from keeps the test in the same room
            p.axes([-sx, -sy, 0, 0]); p.step(20); p.axes([0, 0, 0, 0]); p.step(2)
        check(moved >= 2, f'deck: view {turn}: the stick moved you in only {moved} of 4 directions')
        check(p.ev('player.steer') is None, f'deck: view {turn}: letting go of the stick should stop you')
    # a gentle push walks slower than a full one
    p.ev('azT = az = Math.PI / 4'); settle(p, 10)
    p.axes([0, -.45, 0, 0]); p.step(2); k1 = p.ev('player.steer && player.steer.k'); p.axes([0, -1, 0, 0]); p.step(2); k2 = p.ev('player.steer && player.steer.k')
    p.axes([0, 0, 0, 0]); p.step(2)
    check(k1 is not None and k2 is not None and k1 < k2 and abs(k2 - 1) < 1e-6, f'deck: walking speed should follow the push: {k1} {k2}')
    # turning: LB and RB a quarter turn each way; the right stick, one quarter turn per push however long it's held
    az0 = p.ev('azT'); p.press('rb'); check(abs(p.ev('azT') - az0 - 3.14159265 / 2) < 1e-6, 'deck: RB should turn a quarter turn')
    p.press('lb'); check(abs(p.ev('azT') - az0) < 1e-6, 'deck: LB should turn back')
    p.axes([0, 0, 1, 0]); p.step(20); p.axes([0, 0, 0, 0]); p.step(2); p.axes([0, 0, 1, 0]); p.step(5); p.axes([0, 0, 0, 0]); p.step(2)
    check(abs(p.ev('azT') - az0 - 3.14159265) < 1e-6, 'deck: two pushes of the right stick should be two quarter turns')
    p.axes([0, 0, -1, 0]); p.step(3); p.axes([0, 0, 0, 0]); p.step(30)
    # zooming: the right trigger in, the left out, the same limits as pinch; the stick click back to the opening zoom
    z0 = p.ev('camera.zoom'); p.btn('rt', .4); p.step(10); p.btn('rt', 0); p.step(1); z1 = p.ev('camera.zoom')
    check(z1 > z0, f'deck: the right trigger should zoom in: {z0} -> {z1}')
    p.btn('rt', 1); p.step(200); p.btn('rt', 0); p.step(1); check(abs(p.ev('camera.zoom') - p.ev('ZOOM_MAX')) < 1e-6, 'deck: zoom in stops at ZOOM_MAX')
    p.btn('lt', 1); p.step(300); p.btn('lt', 0); p.step(1); check(abs(p.ev('camera.zoom') - p.ev('ZOOM_MIN')) < 1e-6, 'deck: zoom out stops at ZOOM_MIN')
    p.axes([0, 0, 0, -1]); p.step(10); p.axes([0, 0, 0, 0]); p.step(1); check(p.ev('camera.zoom') > p.ev('ZOOM_MIN'), 'deck: up on the right stick should zoom in')
    p.press('rs'); check(abs(p.ev('camera.zoom') - p.ev('padZoom0()')) < 1e-6, 'deck: the right stick click should go back to the opening zoom')
    # Menu, Y, View: the same as their buttons
    p.press('menu'); check(p.ev('PAUSE.on') is True, 'deck: Menu should pause'); p.press('menu'); check(p.ev('PAUSE.on') is False, 'deck: Menu again should resume')
    p.press('y'); check(p.ev('DEV.open') is True, 'deck: Y should open the device')
    # with a panel open the deck takes nothing: no walking, no turning
    a = p.ev(SCREEN); az1 = p.ev('azT'); p.axes([1, 0, 0, 0]); p.step(20); p.axes([0, 0, 0, 0]); p.press('rb'); b = p.ev(SCREEN)
    check(abs(a[2] - b[2]) + abs(a[3] - b[3]) < 1e-6 and p.ev('azT') == az1, 'deck: with the device open the stick walked or RB turned')
    check(p.ev('padLayer() && padLayer().id') == 'device', 'deck: padLayer should name the device')
    p.press('y'); check(p.ev('DEV.open') is False, 'deck: Y again should close the device')
    p.press('view'); check(p.ev('!trkEl.hidden') is True, 'deck: View should open Tracked'); p.press('view'); check(p.ev('trkEl.hidden') is True, 'deck: View again should close Tracked')
    p.ev("toast('Test', 'A toast')"); p.step(1); p.press('b'); check(not p.ev("toastEl.classList.contains('show')"), 'deck: B should put a toast away')
    check(p.ev('padLayer()') is None, 'deck: nothing should be open at the end')
    p.close()

PARTS = [('off', part_off), ('quiet', part_quiet), ('base', part_base), ('deck', part_deck)]
with sync_playwright() as pw:
    for name, fn in PARTS:
        if ONLY and name not in ONLY: continue
        print('part', name, flush=True)
        try: fn(pw)
        except Exception as e: fail(f'{name}: {type(e).__name__}: {e}')
print('CONTROLLER CHECK OK' if ok else 'CONTROLLER CHECK FAILED')
sys.exit(0 if ok else 1)
