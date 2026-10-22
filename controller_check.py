# Starship Cadet: controller check (section 26, controller support CT1; plans/controller-plan.html)
# Plays the game with a PRETEND controller: before the game loads, the browser's controller list
# (navigator.getGamepads) is replaced by scripted pads whose buttons and sticks the check sets frame by frame, and
# their hello and goodbye are announced the way a real pad's are (gamepadconnected / gamepaddisconnected).
# The game file's switch PAD_ON is flipped on in a copy (the "on" build); the file as given is the "off" build.
# Parts (turn 1, the base):
#   off:    with the switch off, a pad saying hello and pressing buttons changes nothing (no PAD.live, no body.pad)
#   quiet:  with the switch on and no pad: nothing new on the page (elements, styles, body classes), PAD.live false
#   api:    (P1) the panel helper's API: padPanelAdd's order, first button and B; padOwn taking the D-pad, A and frames
#   lists:  (P1) the right stick scrolls a long list, the triggers page; the D-pad follows into it; a text box: A keeps
#           it, B leaves it first; LB and RB are the device's Back and Home
#   base:   hello; a press fires once and marks the controller in use (body.pad); its release; the dead zones (sticks,
#           triggers); a held D-pad repeats (after 0.5 s, then every 0.25 s); a touch, the mouse or the wheel hands
#           back (body.pad goes); the pad families from their names; a non-standard pad; two pads (the last to press
#           is in charge); a disconnect lets go of everything and says whether the pad was in use; the last pad going
#           leaves PAD.live false
#   a11y:   (CP5) walking stops the frame the stick is let go; the menu repeat's pace and "no repeat"; toasts read out;
#           the highlight's look; the ring pulses, and stays still with reduced motion; every button the highlight can
#           land on, panel by panel, has a name a screen reader can say
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

# what a tap (or A) led to, a second of game later: where you are and are going, what you're doing, what's open
OUTCOME = """(() => ({ at: [Math.round(player.obj.position.x * 100), Math.round(player.obj.position.z * 100)], goal: player.goal || null,
  path: player.path.length, act: typeof ACT !== 'undefined' && ACT ? ACT.kind + ':' + (ACT.phase || '') : null,
  toast: document.getElementById('tt').textContent + '|' + document.getElementById('tx').textContent,   // its text (it fades on a real-time timer)
  chat: (document.getElementById('chat') || { hidden: true }).hidden ? null : document.getElementById('chat').textContent.slice(0, 80),
  lift: !liftEl.hidden, dev: DEV.open, layer: (padLayer() || { id: null }).id }))()"""
SPOTS = """(() => {   // places to stand: by the lift, by people, by items, by seats, the most open floor (free tiles, sorted, at most 10)
  const out = [], seen = new Set(), put = (x, z) => { const c = nearestOpen(x, z, player); if (c && !seen.has(c.join())) { seen.add(c.join()); out.push(c); } };
  for (const d of DOOR_OBJS) if (d.e.type === 'lift') { put(d.cx + 1, d.cz); break; }
  for (const a of DECK_CREW.slice(0, 3)) put(a.x + 1, a.z);
  for (const it of ITEMS.filter(i => i.hit && !i.wall).slice(0, 40).filter((_, k) => k % 10 === 0)) { const p = new THREE.Vector3(); it.hit.getWorldPosition(p); put(p.x, p.z); }
  for (const pl of [...PLACE_OF.values()].filter(pl => SIT_TYPES.has(pl.type)).slice(0, 2)) { const sp = placeSpot(pl.id); if (sp) put(sp.x + .8, sp.z); }
  return out.slice(0, 10); })()"""
def go_to(p, cell):
    p.ev(f'player.stop(); if (typeof ACT !== "undefined" && ACT) actEnd(true); player.obj.position.copy(cellPos({cell[0]}, {cell[1]})); target.copy(player.obj.position).setY(.7); player.face = 0')
    p.step(8)

def part_pick(pw):
    a = Pad(pw, ON); b = Pad(pw, ON)                 # a presses A; b taps the same spot by hand: the same game, in lockstep
    kids0 = a.ev('scene.children.length')
    for q in (a, b): q.plug(); q.press('x'); q.log()
    check(a.ev('PAD_PICK.ring !== null') and a.ev('scene.children.length') == kids0 + 1, 'pick: the ring should be made at the first use, one object')
    spots = a.ev(SPOTS); check(len(spots) >= 5, f'pick: too few places to stand: {spots}')
    kinds, tried = set(), 0
    for cell in spots:
        for q in (a, b): go_to(q, cell)
        for q in (a, b): q.ev('PAD_PICK.n = 0; PAD_PICK.job = null; PAD_PICK.list = []; PAD_PICK.sel = null'); q.step(2)
        la, lb = a.ev('PAD_PICK.list.map(t => t.key)'), b.ev('PAD_PICK.list.map(t => t.key)')
        check(la == lb, f'pick: the two games see different things at {cell}: {la} vs {lb}')
        if not la: continue
        check(a.ev('PAD_PICK.ring.visible') is True, f'pick: no ring at {cell}')
        hint = a.ev('document.getElementById("padHint").textContent')
        check(a.ev('padLabel(PAD_PICK.sel.key)') in hint and hint.startswith('A'), f'pick: the line should name the ringed thing: {hint!r}')
        for k in range(min(3, len(la))):
            key = la[k]
            for q in (a, b): go_to(q, cell); q.ev('PAD_PICK.n = 0; PAD_PICK.job = null; PAD_PICK.list = []; PAD_PICK.sel = null'); q.step(2)
            for _ in range(k):                            # D-pad right k times (b steps along: the same game): each the next in the list
                want = a.ev('(() => { const L = PAD_PICK.list, i = L.indexOf(PAD_PICK.sel); return L[(i + 1) % L.length].key; })()')
                a.btn('right'); a.step(1); got = a.ev('PAD_PICK.sel && PAD_PICK.sel.key'); b.step(1); a.btn('right', 0); a.step(1); b.step(1)
                check(got == want, f'pick: D-pad right should ring the next thing, {want}, not {got}')
            key = a.ev('PAD_PICK.sel && PAD_PICK.sel.key')
            s = a.ev('PAD_PICK.sel.s')
            b.ev(f'tap({s[0]}, {s[1]})')                 # b: a finger, at the same moment
            a.btn('a'); a.step(1); b.step(1); a.btn('a', 0)
            a.step(40); b.step(40)
            oa, ob = a.ev(OUTCOME), b.ev(OUTCOME)
            check(oa == ob, f'pick: A on {key} at {cell} differs from a tap there:\n   A  {oa}\n   tap {ob}')
            kinds.add(key.split(':')[0]); tried += 1
            for q in (a, b):                              # put away whatever opened
                q.ev("chatClose && chatClose(); if (!liftEl.hidden) closeLiftPanel(); if (DEV.open) deviceClose(); toastEl.classList.remove('show'); trkClose()"); q.step(2)
    print(f'  pick: {tried} things pressed, kinds {sorted(kinds)}')
    check(tried >= 8 and {'lift', 'crew'} & kinds and 'item' in kinds, f'pick: too few kinds tried: {tried} {sorted(kinds)}')
    # the ring and the line go with a touch, and while a panel is open
    a.press('y'); a.step(2); check(a.ev('PAD_PICK.ring.visible') is False and a.ev('document.getElementById("padHint").hidden') is True, 'pick: the ring or line showed with the device open')
    a.press('y'); a.step(8)
    a.js("document.body.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))"); a.step(2)
    check(a.ev('PAD_PICK.ring.visible') is False and a.ev('document.getElementById("padHint").hidden') is True, 'pick: the ring or line stayed after a touch')
    a.close(); b.close()

# every button of the panel on top, reached from its first by D-pad moves alone: { layer, items, reached, missing }
REACH = """(() => {
  const L = padLayer(); if (!L) return null;
  const items = padItems(L), seen = new Set([items[0]]), todo = [items[0]];
  while (todo.length) { const e = todo.pop(); for (const d of ['up', 'down', 'left', 'right']) { padFocusTo(e); padMove(d); const n = document.activeElement; if (items.includes(n) && !seen.has(n)) { seen.add(n); todo.push(n); } } }
  padFocusTo(items[0]);
  const name = e => (e.id ? '#' + e.id : '') + ' ' + (e.getAttribute('aria-label') || e.textContent || '').trim().slice(0, 30);
  return { layer: L.id || L.className, items: items.length, reached: seen.size, missing: items.filter(e => !seen.has(e)).map(name) };
})()"""
def sweep(p, what, back=True, must=False):
    p.step(3)
    r = p.ev(REACH)
    if not check(r is not None, f'panels: {what}: no panel on top'): return None
    check(r['items'] > 0 and not r['missing'], f'panels: {what} ({r["layer"]}): {r["reached"]} of {r["items"]} buttons reached by the D-pad; missing {r["missing"][:6]}')
    check(p.ev('document.activeElement && padItems(padLayer()).includes(document.activeElement)'), f'panels: {what}: the highlight is not on one of its buttons')
    if back:
        L0 = p.ev('(padLayer() || {}).id || null'); p.press('b'); p.step(3); L1 = p.ev('(padLayer() || {}).id || null')
        if must: check(L1 == L0, f'panels: {what}: B closed a card you must answer')
        else: check(L1 != L0, f'panels: {what}: B did not close it (still {L1})')
    return r

def part_panels(pw):
    p = Pad(pw, ON)
    p.plug(); p.press('x'); p.log()
    n = 0
    # the screen's edge, from the deck
    p.press('up'); check(p.ev('padLayer() === PAD_HUD'), 'panels: D-pad up on the deck should reach the screen-edge buttons'); sweep(p, 'screen edge'); n += 1
    check(p.ev('padLayer()') is None, 'panels: B from the screen edge should go back to walking')
    p.press('up'); p.ev("padFocusTo(document.getElementById('pauseBtn'))"); p.press('a'); p.step(2)
    check(p.ev('PAUSE.on') is True and p.ev("(padLayer() || {}).id") == 'pauseCard', 'panels: A on the Pause button should pause, with the card on top')
    sweep(p, 'pause card'); n += 1; check(p.ev('PAUSE.on') is False, 'panels: B on the Pause card should resume')
    p.press('menu'); sweep(p, 'pause card by Menu', back=False); p.press('a'); check(p.ev('PAUSE.on') is False, 'panels: A on Resume should resume'); n += 1
    # the lift's deck list: its goal deck (or first deck) highlighted; B is Stay here
    p.ev('openLiftPanel()'); sweep(p, 'lift'); n += 1
    p.ev('alarmOpen()'); sweep(p, 'alarm'); n += 1
    p.press('view'); sweep(p, 'Tracked'); n += 1
    p.ev('ixBoard.open()'); sweep(p, 'job board'); n += 1
    # a conversation: the first person on the deck whose card opens (someone asleep only gets a toast)
    if check(p.ev("DECK_CREW.some(a => { chatOpen(a.p); const c = document.getElementById('chat'); return c && !c.hidden; })"), 'panels: no conversation card would open'):
        sweep(p, 'chat'); n += 1
    # (P1) more panels: the ladder (B = Escape), the queue's question (B = Stay), the waking card and a clock screen
    p.ev('ladderPanel()'); sweep(p, 'ladder'); n += 1
    p.ev('queueAsk()'); r = p.ev("(padLayer() || {}).id")
    if check(r == 'qAsk', f'panels: the queue question is not on top ({r})'): sweep(p, 'queue question'); n += 1
    p.ev("sickNote('Test', 'A card you must answer.', [['One', () => {}], ['Two', () => {}]])"); sweep(p, 'waking card', must=True); p.press('a'); p.step(2)
    check(p.ev("(padLayer() || {}).id") != 'sickCard', 'panels: A on the waking card should answer it'); n += 1
    p.ev("clockScreen('Test')"); r = p.ev("(padLayer() || {}).id")
    if r == 'clockScreen':
        sweep(p, 'clock screen'); n += 1
    else: p.ev("(() => { const e = document.getElementById('clockScreen'); if (e) e.hidden = true; })()")
    # a tip card on the deck: B puts it away; the heads-up cards are among the screen-edge buttons (D-pad up, A)
    p.ev("SHIP.device.settings.tips = true; tipShow('padTest', 'A test tip.')"); p.step(2)
    if check(p.ev("!document.getElementById('devTip').hidden"), 'panels: the test tip did not show'):
        p.press('b'); p.step(2); check(p.ev("document.getElementById('devTip').hidden"), 'panels: B on the deck should put a tip card away')
    p.ev("SHIP.device.settings.tips = false; tipShow('padTest2', 'Another.')")
    p.ev("DEVICE_SKIN.address({ text: 'Test address.' })"); p.step(2)
    p.press('up'); p.step(2)
    check(p.ev("padItems(PAD_HUD).includes(document.getElementById('devAddr'))"), 'panels: the address card should be among the screen-edge buttons')
    p.ev("padFocusTo(document.getElementById('devAddr'))"); check(p.ev("document.activeElement.id") == 'devAddr', 'panels: the highlight should land on the address card')
    p.press('a'); p.step(2); check(p.ev("document.getElementById('devAddr').hidden"), 'panels: A on the address card should put it away')
    p.press('b'); p.step(2)
    # the device: home, then every app on it, each by A from its tile; B back home, B again closes
    p.press('y'); sweep(p, 'device home', back=False); n += 1
    apps = p.ev("[...DEVICE_APPS.values()].filter(a => !(a.hidden && a.hidden()) && a.id !== 'home' && a.id !== 'boot').map(a => a.id)")
    for app in apps:
        p.ev(f'deviceShow({json.dumps(app)})'); p.step(3)
        r = sweep(p, 'device app ' + app, back=False)
        p.press('b'); p.step(2)
        check(p.ev('DEV.open && DEV.app') == 'home', f'panels: B in the {app} app should go back home, not {p.ev("DEV.open && DEV.app")}')
        n += 1
    p.press('b'); p.step(2); check(p.ev('DEV.open') is False, 'panels: B on the home screen should close the device')
    # A on a home tile opens that app
    p.press('y'); p.step(3); first = p.ev('document.activeElement && document.activeElement.textContent.trim().slice(0, 20)')
    p.press('a'); p.step(3); check(p.ev('DEV.open && DEV.app') != 'home', f'panels: A on the home tile {first!r} should open its app')
    p.press('y'); p.step(2)
    # X presses the action button that shows (none now: nothing happens, nothing opens)
    lay = p.ev("(() => { const L = padLayer(); return L ? L.id || L.className : null; })()")
    check(lay is None, f'panels: something still open before X: {lay}')
    p.press('x'); lay = p.ev("(() => { const L = padLayer(); return L ? L.id || L.className : null; })()")
    check(lay is None, f'panels: X with no action button opened {lay}')
    print(f'  panels: {n} panels swept, device apps {len(apps)}')
    p.close()

def part_api(pw):
    # the panel helper's API (P1) for the other packages: padPanelAdd (order, first, back), padOwn (move, a, b, frame)
    p = Pad(pw, ON)
    p.plug(); p.press('x'); p.log()
    p.ev("""(() => { const d = document.createElement('div'); d.id = 'tstPanel'; d.style.cssText = 'position:fixed;left:20px;top:200px;z-index:99;display:grid;grid-template-columns:90px 90px;gap:8px';
      d.innerHTML = '<button id="t1">one</button><button id="t2">two</button><button id="t3">three</button>'; document.body.appendChild(d);
      window.__tst = { back: 0, a: 0, moves: [], frames: 0 };
      padPanelAdd('tstPanel', { before: 'lift', first: '#t2', back: () => { __tst.back++; d.hidden = true; } }); })()""")
    p.step(3)
    check(p.ev("(padLayer() || {}).id") == 'tstPanel', 'api: an added panel should be on top')
    check(p.ev("PAD_PANELS.findIndex(r => r[0] === 'tstPanel') + 1 === PAD_PANELS.findIndex(r => r[0] === 'lift')"), 'api: before: should put it just above the lift')
    check(p.ev("document.activeElement && document.activeElement.id") == 't2', 'api: first: should land the highlight on #t2')
    p.press('left'); check(p.ev("document.activeElement.id") == 't1', 'api: D-pad left should move to #t1')
    p.press('down'); check(p.ev("document.activeElement.id") == 't3', 'api: D-pad down should move to #t3')
    # a screen of its own takes the D-pad and A, not B
    p.ev("padOwn(L => L && L.id === 'tstPanel', { move: d => { __tst.moves.push(d); return true; }, a: () => { __tst.a++; return true; }, frame: () => { __tst.frames++; } })")
    p.press('right'); p.press('a'); p.step(2)
    check(p.ev("__tst.moves.join()") == 'right' and p.ev("__tst.a") == 1 and p.ev("document.activeElement.id") == 't3', f'api: padOwn should take the D-pad and A: {p.ev("JSON.stringify(__tst)")}')
    check(p.ev("__tst.frames") > 0, 'api: padOwn frame should run while its panel is on top')
    # (P1, CP2's alarm case) a far button in the same row beats a wide one just below; (CP4's) a redraw keeps the place
    p.ev("""(() => { const d = document.createElement('div'); d.id = 'tstRow'; d.style.cssText = 'position:fixed;left:20px;top:420px;width:340px;z-index:99';
      const draw = () => { d.innerHTML = '<div style="display:flex;justify-content:space-between"><button id="rm" style="width:40px">-</button><button id="rp" style="width:40px">+</button></div><button id="rw" style="width:100%;margin-top:6px">Set</button><button id="rx">Again</button>';
        d.querySelector('#rx').onclick = draw; d.querySelector('#rw').onclick = draw; };
      draw(); document.body.appendChild(d); padPanelAdd('tstRow', { before: 'pauseCard', first: '#rp', back: () => { d.hidden = true; } }); })()""")
    p.step(3); check(p.ev("document.activeElement.id") == 'rp', 'api: the row panel should start on +')
    p.press('left'); check(p.ev("document.activeElement.id") == 'rm', f'api: D-pad left from + should go across to -, not {p.ev("document.activeElement.id")}')
    p.press('down'); p.press('down'); check(p.ev("document.activeElement.id") == 'rx', f'api: two downs should reach Again ({p.ev("document.activeElement.id")})')
    p.press('a'); p.step(3); check(p.ev("document.activeElement.id") == 'rx', f'api: after a redraw the highlight should stay on Again, not {p.ev("document.activeElement.id")}')
    p.press('b'); p.step(2)
    p.press('b'); p.step(2)
    check(p.ev("__tst.back") == 1 and p.ev("padLayer()") is None, 'api: B should run the panel\'s back and close it')
    p.close()

def part_lists(pw):
    # (P1) long lists and text boxes: the right stick scrolls, the triggers page, the D-pad follows into the scrolled-away
    # part; A in a text box keeps it (the system keyboard), B leaves the box first, then closes; LB and RB in the device
    p = Pad(pw, ON)
    p.plug(); p.press('x'); p.log()
    p.ev("""(() => { const d = document.createElement('div'); d.id = 'tstList'; d.style.cssText = 'position:fixed;left:20px;top:100px;width:200px;height:300px;z-index:99;display:flex;flex-direction:column';
      d.innerHTML = '<input id="tIn" aria-label="Name"><div id="tSc" style="overflow-y:auto;flex:1">' + Array.from({ length: 30 }, (_, i) => '<button style="display:block;width:180px;height:40px" id="b' + i + '">' + i + '</button>').join('') + '</div>';
      document.body.appendChild(d); padPanelAdd('tstList', { first: '#b0', back: () => { d.hidden = true; } }); })()""")
    p.step(3)
    check(p.ev("document.activeElement.id") == 'b0', 'lists: the highlight should start on #b0')
    p.axes([0, 0, 0, 1]); p.step(10); p.axes([0, 0, 0, 0]); p.step(1)
    s1 = p.ev("document.getElementById('tSc').scrollTop"); check(s1 > 50, f'lists: the right stick should scroll the list ({s1})')
    p.press('rt'); s2 = p.ev("document.getElementById('tSc').scrollTop"); check(s2 > s1, f'lists: RT should page down ({s1} -> {s2})')
    p.press('lt'); s3 = p.ev("document.getElementById('tSc').scrollTop"); check(s3 < s2, f'lists: LT should page up ({s2} -> {s3})')
    for _ in range(12): p.press('down')
    check(p.ev("document.activeElement.id") == 'b12', f'lists: twelve D-pad downs should reach #b12, not {p.ev("document.activeElement.id")}')
    r = p.ev("(() => { const a = document.activeElement.getBoundingClientRect(), b = document.getElementById('tSc').getBoundingClientRect(); return a.top >= b.top - 1 && a.bottom <= b.bottom + 1; })()")
    check(r, 'lists: the highlighted button should be scrolled into sight')
    p.ev("padFocusTo(document.getElementById('b0'))"); p.press('up'); check(p.ev("document.activeElement.id") == 'tIn', 'lists: D-pad up from the first button should reach the text box')
    p.press('a'); check(p.ev("document.activeElement.id") == 'tIn', 'lists: A in a text box should keep it')
    p.press('b'); check(p.ev("document.activeElement.id") != 'tIn' and p.ev("(padLayer() || {}).id") == 'tstList', 'lists: B in a text box should leave the box, not the panel')
    p.press('b'); check(p.ev("padLayer()") is None, 'lists: B again should close the panel')
    # the device: LB is its Back, RB its Home
    p.press('y'); p.step(3); p.ev("deviceShow('mail')"); p.step(3); check(p.ev("DEV.app") == 'mail', 'lists: the Mail app did not open'); p.press('lb'); p.step(2)
    check(p.ev("DEV.open && DEV.app") == 'home', f'lists: LB in an app should go back ({p.ev("DEV.app")})')
    p.ev("deviceShow('mail')"); p.step(3); p.press('rb'); p.step(2)
    check(p.ev("DEV.open && DEV.app") == 'home', f'lists: RB in an app should go home ({p.ev("DEV.app")})')
    p.close()

# P5 (accessibility, CP5): every button the highlight lands on has a name a screen reader can say: [] or the nameless
NAMELESS = """(() => {
  const L = padLayer(); if (!L) return null;
  return padItems(L).filter(e => { padNameIt(e); return !padName(e); }).map(e => (e.id ? '#' + e.id : e.className ? '.' + String(e.className).split(' ')[0] : e.tagName) + ' ' + e.outerHTML.slice(0, 70));
})()"""

def part_a11y(pw):
    p = Pad(pw, ON)
    p.plug(); p.press('x'); p.log(); p.step(3)
    # no holds: the stick walks only while pushed, and stops the frame it's let go
    p.axes([0, -1, 0, 0]); p.step(6); walking = p.ev('!!player.steer')
    p.axes([0, 0, 0, 0]); p.step(1)
    check(walking and p.ev('!player.steer && !PAD_DECK.walking'), f'a11y: walking should stop the frame the stick is let go (was walking: {walking})')
    # the menu repeat is calm (0.5 s, then 4 a second) and follows PAD_REP when Settings changes it: "no repeat" is one step
    check(p.ev('PAD_REP.first') == .5 and p.ev('PAD_REP.every') == .25, 'a11y: the menu repeat should start at 0.5 s, then 4 steps a second')
    p.ev('PAD_REP.first = Infinity'); p.log(); p.btn('down'); p.step(90); p.btn('down', 0); p.step(1)
    fired = [x for x in p.log() if x.startswith('down')]
    check(fired == ['down', 'down:up'], f'a11y: with no repeat, holding down three seconds should be one step: {fired}')
    p.ev('PAD_REP.first = .5')
    # toasts are read out once the controller is in use
    check(p.ev("toastEl.getAttribute('role') === 'status' && toastEl.getAttribute('aria-live') === 'polite'"), 'a11y: the toast should be a polite live region once the pad is used')
    # the highlight: thick, teal, with a dark edge
    p.press('up'); p.step(2)
    st = p.ev("(() => { const c = getComputedStyle(document.activeElement); return [c.outlineWidth, c.outlineColor, c.outlineStyle, c.boxShadow]; })()")
    check(st[0] == '4px' and st[1] == 'rgb(76, 195, 181)' and st[2] == 'solid' and 'rgb(13, 21, 33)' in st[3], f'a11y: the highlight should be a 4px teal outline with a dark edge: {st}')
    p.press('b'); p.step(2)
    # the deck ring: pulses, and stays still when the phone asks for reduced motion (asked live)
    ring = p.ev('!!(PAD_PICK.ring && PAD_PICK.ring.visible)')
    if check(ring, 'a11y: no ring on the deck where the game starts (needed for the pulse test)'):
        sc = []
        for _ in range(8): p.step(2); sc.append(p.ev('PAD_PICK.ring.scale.x'))
        check(len(set(sc)) > 1, f'a11y: the ring should pulse gently: {sc}')
        p.g.page.emulate_media(reduced_motion='reduce'); sc = []
        for _ in range(8): p.step(2); sc.append(p.ev('PAD_PICK.ring.scale.x'))
        check(set(sc) == {1}, f'a11y: with reduced motion the ring should stay still: {sc}')
        p.g.page.emulate_media(reduced_motion='no-preference')
    # every button the highlight can land on has a name, panel by panel
    gaps, n = {}, 0
    def look(what):
        nonlocal n
        p.step(3); r = p.ev(NAMELESS)
        if check(r is not None, f'a11y: {what}: no panel on top'): n += 1
        if r: gaps[what] = r
    p.press('up'); look('screen edge'); p.press('b')
    p.press('menu'); look('pause card'); p.press('b')
    p.ev('openLiftPanel()'); look('lift'); p.press('b')
    p.ev('alarmOpen()'); look('alarm'); p.press('b')
    p.press('view'); look('Tracked'); p.press('b')
    p.ev('ixBoard.open()'); look('job board'); p.press('b')
    if p.ev("DECK_CREW.some(a => { chatOpen(a.p); const c = document.getElementById('chat'); return c && !c.hidden; })"): look('chat'); p.press('b')
    p.press('y'); look('device home')
    for app in p.ev("[...DEVICE_APPS.values()].filter(a => !(a.hidden && a.hidden()) && a.id !== 'home' && a.id !== 'boot').map(a => a.id)"):
        p.ev(f'deviceShow({json.dumps(app)})'); look('device app ' + app); p.press('b'); p.step(2)
    p.press('b'); p.step(2)
    for what, r in gaps.items(): fail(f'a11y: {what}: buttons with no name a screen reader can say: {r[:4]}')
    print(f'  a11y: {n} panels looked at for names, {sum(len(r) for r in gaps.values())} nameless')
    p.close()

PARTS = [('off', part_off), ('quiet', part_quiet), ('base', part_base), ('deck', part_deck), ('pick', part_pick), ('panels', part_panels), ('api', part_api), ('lists', part_lists), ('a11y', part_a11y)]
with sync_playwright() as pw:
    for name, fn in PARTS:
        if ONLY and name not in ONLY: continue
        print('part', name, flush=True)
        try: fn(pw)
        except Exception as e: fail(f'{name}: {type(e).__name__}: {e}')
print('CONTROLLER CHECK OK' if ok else 'CONTROLLER CHECK FAILED')
sys.exit(0 if ok else 1)
