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
# Parts (P2, the mini-games):
#   tiles:  How to play's Next highlighted and pressed with A; the D-pad square by square; a move by the pad alone (A picks
#           up, A puts down); A on your hold keeps the highlight when the board redraws; Again at the end, Done by D-pad and A
#   disc:   Lightdisc: Next highlighted, A is Next; the left stick's full range (a light push slower), never the highlight;
#           letting go stops; A never presses Leave by itself, B leaves; the result card's Again, Quick game by D-pad and A
#   screens: the lift (your goal deck highlighted, A rides, B stays); the alarm (Set alarm first, − and + in reach, B
#           closes); a work step's turn card (its first answer, not the ×; the place kept as it asks again; B is the ×);
#           the arrival's manifest (the name box first, B stays, A on Sign fills a suggested name, A again signs)

#   settings (P4, plan section 7): with no pad, Settings and the save are unchanged (switch off vs on); once a pad is seen
#           Settings ends with the Controller page's button; change a button by pad (the A that began it is not taken,
#           the chosen button does nothing, the two swap), B back to Settings, the swap of confirm and back, an action's
#           own button keeps it; every setting takes effect; the changes are small in the save and hold through a real
#           reload; turning by holding, flipped zoom, gentle walking; an odd save loads as normal; Everything back to
#           normal leaves nothing saved
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
            for q in (a, b): q.ev("document.getElementById('tt').textContent = ''; document.getElementById('tx').textContent = ''")   # (an old message: the controller's own may differ in time)
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
# (P1, PR9's cross-check) the same panel read from the page, not from padItems: every visible thing a finger could press
# (a button or form box, role=button, an onclick, a pointer cursor) that the highlight can't land on (not in padItems, not
# inside one). Allowed: disabled buttons; the Maps app's drawing (its room taps are the Rooms list's buttons).
CLICKY = """(() => { const L = padLayer(); if (!L || L === PAD_HUD) return []; const items = padItems(L);
  const vis = e => e.getClientRects().length && getComputedStyle(e).visibility !== 'hidden' && !e.closest('[hidden]') && e.getAttribute('aria-hidden') !== 'true';
  const out = [];
  for (const e of L.querySelectorAll('*')) {
    if (!vis(e) || e.disabled || e.closest('button:disabled') || items.includes(e) || items.some(i => i.contains(e) || e.contains(i))) continue;
    if (DEV.app === 'maps' && e.closest('svg')) continue;
    const cs = getComputedStyle(e), clicky = e.onclick || cs.cursor === 'pointer' || e.getAttribute('role') === 'button' || /^(BUTTON|INPUT|SELECT|TEXTAREA|A)$/.test(e.tagName);
    if (!clicky || cs.pointerEvents === 'none' || e.parentElement && out.some(o => o.el === e.parentElement)) continue;
    out.push({ el: e, d: e.tagName.toLowerCase() + (e.id ? '#' + e.id : '') + ' ' + (e.textContent || '').trim().slice(0, 24) + (e.onclick ? ' [onclick]' : '') });
  }
  return out.map(o => o.d); })()"""
def sweep(p, what, back=True, must=False):
    p.step(3)
    miss = p.ev(CLICKY)
    check(not miss, f'panels: {what}: things a finger can press that the highlight cannot reach: {miss[:6]}')
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

# ---- P3 (plan sections 5 and 6): button pictures, connecting and disconnecting ----
# marks:   nothing before a press; after one, a mark on Device (Y), Pause (Menu), Tracked (View), inside its button, shown;
#          the bottom line's mark in the pad's style; Xbox / PlayStation / Nintendo from the pad's name and from
#          P4's padMarkFamily (Off too) and padButtonFor (a rebound button); X's mark moves to the action button showing; Lightdisc's Leave gets B; a touch hides them all;
#          "Controller connected" once a session; the marks follow the text size (em); a speech bubble is drawn above them
# touch:   press, then touch: the screenshot is the no-pad one, pixel for pixel
# drop:    a disconnect mid-walk stops you and pauses ("Controller disconnected" on the card); A on the card resumes once
#          the pad is back; the card's usual line comes back; a pad not used for 30 s stops you but doesn't pause;
#          two pads: the last to press decides the marks' style
SHOTS = os.environ.get('PAD_SHOTS')
MARKS = "(() => [...document.querySelectorAll('.padk')].map(m => [m.parentElement.id || m.parentElement.className, m.dataset.k, m.dataset.f, getComputedStyle(m).display !== 'none']))()"
def marks(p): return {(a, k): (f, shown) for a, k, f, shown in p.ev(MARKS)}

def part_marks(pw):
    p = Pad(pw, ON)
    p.plug(); p.step(3)
    check(p.ev("document.querySelectorAll('.padk').length") == 0, 'marks: marks on the page before any press')
    # "Controller connected" waits for the message showing (the opening one) to go, then shows
    p.ev("toast('Deck 4, CSV Wren', 'opening')"); p.press('x'); p.step(12)
    check(p.ev("document.getElementById('tt').textContent") == 'Deck 4, CSV Wren', 'marks: "Controller connected" replaced the message showing')
    p.ev("toastEl.classList.remove('show')"); p.step(2)
    m = marks(p)
    for b, k in [('devBtn', 'y'), ('pauseBtn', 'menu'), ('trkBtn', 'view')]:
        check(m.get((b, k)) == ('xbox:' + k, True), f'marks: no shown Xbox {k} mark on {b}: {m}')
    check(p.ev("document.getElementById('tt').textContent") == 'Controller connected', 'marks: no "Controller connected" at the first press')
    check(p.ev("document.querySelector('#devBtn > .padk').textContent") == 'Y', 'marks: the Device mark should read Y')
    hint = p.ev("(() => { const h = document.getElementById('padHint'); const k = h && h.querySelector('.padk'); return h && !h.hidden && k ? [k.dataset.k, k.dataset.f, k.textContent] : null; })()")
    check(hint is None or hint == ['a', 'xbox:a', 'A'], f'marks: the bottom line\'s mark: {hint}')
    # text size: the phone's text size scales the HUD's px text; the mark's shape is in em, so it grows with its letter
    w0 = p.ev("document.querySelector('#pauseBtn > .padk').getBoundingClientRect().height")
    p.ev("document.querySelector('#pauseBtn > .padk').style.fontSize = '22px'"); w1 = p.ev("document.querySelector('#pauseBtn > .padk').getBoundingClientRect().height")
    p.ev("document.querySelector('#pauseBtn > .padk').style.fontSize = ''")
    check(w0 > 14, f'marks: the Pause mark is too small to see: {w0}px')
    check(w1 > w0 * 1.6, f'marks: the mark did not grow with the text size: {w0} -> {w1}')
    # speech bubbles are drawn above the buttons (and so above their marks)
    zb = p.ev("(() => { const d = document.createElement('div'); d.style.cssText = 'position:fixed;inset:0;z-index:2'; document.body.appendChild(d); const r = document.querySelector('#devBtn > .padk').getBoundingClientRect(); const top = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2); d.remove(); return top === d; })()")
    check(zb, 'marks: a layer like the speech bubbles\' (z-index 2, later on the page) does not cover the marks')
    if SHOTS: p.g.shot(SHOTS + '/marks-xbox.png')
    # X: the action button showing
    # (section 15's handTick hides the Hobby button again on its own timer: shown and marked at once, without a step)
    m = p.ev("(() => { handEl(); const b = document.getElementById('hobbyBtn'); b.hidden = false; padMarksSync(); const m = b.querySelector(':scope > .padk'); return m ? [m.dataset.k, getComputedStyle(m).display !== 'none'] : null; })()")
    check(m == ['x', True], f'marks: no X mark on the Hobby button showing: {m}')
    if SHOTS: p.g.shot(SHOTS + '/marks-x.png')
    p.ev("document.getElementById('hobbyBtn').hidden = true; padMarksSync()")
    check(not any(k == 'x' for _, k in marks(p)), 'marks: the X mark stayed with no action button showing')
    # the families (PAD.fam, from the pad's name; P4's padMarkFamily() when it's there)
    for fam, y in [('ps', None), ('nin', 'X')]:
        p.ev(f"PAD.fam = {json.dumps(fam)}"); p.step(2)
        m = marks(p); check(m.get(('devBtn', 'y')) == (fam + ':y', True), f'marks: the family {fam} did not restyle the marks: {m}')
        if y: check(p.ev("document.querySelector('#devBtn > .padk').textContent") == y, f'marks: Nintendo\'s top button should read {y}')
        if SHOTS: p.g.shot(SHOTS + f'/marks-{fam}.png')
    check(p.ev("padWord('a')") == 'B', 'marks: on a Nintendo pad the bottom button is B')
    # P4's Settings: Off (no marks on the buttons, a plain one on the bottom line), and Y's action moved to LB
    p.ev("window.padMarkFamily = () => null"); p.step(12)
    check(not any(a != 'padHint' for a, _ in marks(p)), f'marks: marks on the buttons with Off: {marks(p)}')
    p.ev("window.padMarkFamily = () => PAD.fam; window.padButtonFor = a => a === 'y' ? 'lb' : a; PAD.fam = 'xbox'"); p.step(2)
    check(marks(p).get(('devBtn', 'y')) == ('xbox:lb', True) and p.ev("document.querySelector('#devBtn > .padk').textContent") == 'LB', f'marks: Device should show LB after rebinding: {marks(p)}')
    p.ev("delete window.padMarkFamily; delete window.padButtonFor"); p.step(12)
    # Lightdisc's Leave: B
    if p.ev("(() => { const a = DECK_CREW[0]; if (!a) return false; discBegin(a); return !!(DISC.view && DISC.view.leave); })()"):
        p.press('x'); p.step(12)
        check(p.ev("(() => { const m = DISC.view.leave.querySelector('.padk'); return m && m.dataset.k === 'b' && getComputedStyle(m).display !== 'none'; })()"), 'marks: no B mark on Lightdisc\'s Leave')
        if SHOTS: p.g.shot(SHOTS + '/marks-lightdisc.png')
        p.press('b'); p.step(10)
        check(not p.ev('DISC.view'), 'marks: B did not leave Lightdisc')
    # a touch hides them all; the connected message only once a session
    p.ev("document.getElementById('tt').textContent = ''")
    p.js("document.body.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))"); p.step(2)
    check(not any(s for _, s in marks(p).values()), f'marks: a mark still shows after a touch: {marks(p)}')
    p.press('x'); p.step(3)
    check(p.ev("document.getElementById('tt').textContent") == '', 'marks: "Controller connected" said twice in a session')
    p.close()

def part_touch(pw):
    # speech bubbles are kept out of the pictures (the browser sometimes draws their layer a shade differently with the
    # same page, CTT's find) and compared as text and place instead
    BUBS = "bubbles.list.map(b => [b.text, b.el.style.display, b.el.style.transform])"
    a = Pad(pw, ON); a.plug(); a.step(31); a.g.page.add_style_tag(content='.bubw{opacity:0!important}')
    a.g.shot(str(WORK / 'test' / '_pad_nopad.png')); ba = a.ev(BUBS); a.close()
    b = Pad(pw, ON); b.plug(); b.press('x'); b.step(27)   # (a press is 3 frames)
    b.js("document.body.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))"); b.step(1)   # (the deck drawn once after the touch)
    b.g.page.add_style_tag(content='.bubw{opacity:0!important}')
    b.g.shot(str(WORK / 'test' / '_pad_touch.png')); bb = b.ev(BUBS); b.close()
    check(ba == bb, f'touch: the speech bubbles differ after a press then a touch: {ba} vs {bb}')
    x, y = (WORK / 'test' / '_pad_nopad.png').read_bytes(), (WORK / 'test' / '_pad_touch.png').read_bytes()
    check(x == y, 'touch: the screenshot after a press then a touch differs from the no-pad one (' + str(WORK / 'test') + '/_pad_*.png)')

def part_drop(pw):
    p = Pad(pw, ON)
    p.plug(); p.ev("toastEl.classList.remove('show')"); p.press('b'); p.step(2)   # the first press is B, which puts messages away
    check(p.ev("document.getElementById('tt').textContent") == 'Controller connected' and p.ev("toastEl.classList.contains('show')"), 'drop: a first press of B lost "Controller connected"')
    p.axes([0, -1, 0, 0]); p.step(6)
    check(p.ev('!!player.steer'), 'drop: the stick did not walk')
    p.js('window.__padUnplug(0)'); p.step(1)
    check(p.ev('player.steer') is None, 'drop: still walking after the pad went')
    check(p.ev('PAUSE.on') is True, 'drop: a pad in use going away did not pause')
    line = p.ev("document.getElementById('pauseLine').textContent")
    check(line == 'Controller disconnected', f'drop: the Pause card reads {line!r}')
    check('pad' not in p.ev('document.body.className'), 'drop: the marks stayed with no pad')
    if SHOTS: p.g.shot(SHOTS + '/drop-pause.png')
    p.plug(); p.step(2); p.press('a'); p.step(2)
    check(p.ev('PAUSE.on') is False, 'drop: A on the Pause card did not resume once the pad was back')
    p.press('menu'); p.step(2)
    line = p.ev("document.getElementById('pauseLine').textContent")
    check(p.ev('PAUSE.on') is True and line == 'The ship waits for you.', f'drop: an ordinary pause afterwards reads {line!r}')
    p.press('menu'); p.step(2)
    # not used for half a minute: stop, no pause
    p.ev('PAD.lastUse -= 31000'); p.js('window.__padUnplug(0)'); p.step(1)
    check(p.ev('PAUSE.on') is False, 'drop: a pad unused for 30 s going away paused the game')
    # two pads: the last to press decides the style
    p.plug(0); p.press('x'); p.plug(1, 'DualSense Wireless Controller'); p.press('x', 1); p.step(3)
    check(marks(p).get(('devBtn', 'y'), ('',))[0] == 'ps:y', f'drop: the PlayStation pad pressed last, marks still {marks(p)}')
    p.press('x', 0); p.step(3)
    check(marks(p).get(('devBtn', 'y'), ('',))[0] == 'xbox:y', 'drop: the Xbox pad pressed last, marks not back to Xbox')
    p.close()

# P4, the Controller page in Settings (plan section 7)
SV = "(() => { const s = {}; for (const f of SAVE_EXTRA) try { f(s); } catch (e) { } return s; })()"
SAVE_NOW = """(() => { const decks = {}; for (const n in SHIP.decks) if (SHIP.decks[n].open.size) decks[n] = { open: [...SHIP.decks[n].open] };
  const save = { v: SAVE_V, build: GAME_BUILD, time: { day: SHIP.time.day, min: SHIP.time.min }, player: { deck: player.deck, tile: player.here(), facing: player.face }, ship: { decks }, crew: {}, flags: SHIP.flags || {}, notes: SHIP.notes || [] };
  if (typeof crewState === 'function') save.crew = crewState(SHIP.time.day); for (const f of SAVE_EXTRA) f(save); localStorage.setItem(SAVE_KEY, JSON.stringify(save)); return true; })()"""
def part_settings(pw):
    # with no pad: Settings unchanged, nothing saved; the save's extras byte-identical with the switch off and on
    a = Pad(pw, GAME); va = a.ev("JSON.stringify(deviceView('settings'))"); sa = a.ev(f'JSON.stringify({SV})'); a.close()
    p = Pad(pw, ON)
    check(p.ev("JSON.stringify(deviceView('settings'))") == va, 'settings: the Settings app differs with the switch on and no pad')
    check(p.ev(f'JSON.stringify({SV})') == sa, 'settings: the save differs with the switch on and no pad')
    p.plug(); p.step(3)
    check(p.ev("JSON.stringify(deviceView('settings'))") == va, 'settings: a pad connected but never pressed changed Settings')
    p.press('x'); p.log()
    v = p.ev("deviceView('settings').blocks.map(b => b.text || (b.items || []).map(i => i.label).join('|'))")
    check(v[-1] == 'Controller settings', f'settings: with a pad seen, Settings should end with the Controller button: {v[-2:]}')
    check('pad' not in p.ev(SV), 'settings: a pad used but nothing changed wrote s.pad')
    p.ev("deviceShow('settings')"); p.step(3)
    p.ev("padFocusTo([...document.querySelectorAll('#devBody button')].find(b => b.textContent === 'Controller settings'))"); p.press('a'); p.step(3)
    check(p.ev('DEV.app') == 'padsettings', f'settings: A on Controller settings should open the page, not {p.ev("DEV.app")}')
    sweep(p, 'Controller page', back=False)
    # change a button by pad: highlight "Your device", A, then LB. The A that began it is not taken; Y and LB swap
    p.ev("padFocusTo([...document.querySelectorAll('#devBody button')].find(b => b.textContent.startsWith('Your device')))"); p.log()
    p.btn('a'); p.step(2)
    check(p.ev('PAD_SET_UI.listen') == 'y', 'settings: A on an action should wait for a button')
    p.step(3); p.btn('a', 0); p.step(2); check(p.ev('PAD_SET_UI.listen') == 'y', 'settings: letting go of A stopped the wait')
    p.btn('lb'); p.step(2)
    check(p.ev("padButtonFor('y')") == 'lb' and p.ev("padButtonFor('lb')") == 'y', f'settings: Y and LB should swap: y on {p.ev("padButtonFor(\'y\')")}, lb on {p.ev("padButtonFor(\'lb\')")}')
    check(p.ev('DEV.open && DEV.app') == 'padsettings', 'settings: the chosen button did something (the device moved on)')
    p.step(5); p.btn('lb', 0); p.step(2)
    check(p.ev('DEV.open && DEV.app') == 'padsettings' and p.ev('azT === az && !PAD_SET_UI.eat'), 'settings: the chosen button did something when let go')
    # B on the page goes back to Settings; Y (now on LB) closes the device
    p.press('b'); p.step(2); check(p.ev('DEV.open && DEV.app') == 'settings', f'settings: B on the Controller page should go back to Settings, not {p.ev("DEV.app")}')
    p.press('lb'); p.step(2); check(p.ev('DEV.open') is False, 'settings: the device action, moved to LB, should close the device')
    p.log(); p.press('y'); p.step(2); l = p.log(); check('lb' in l and 'y' not in l, f'settings: the Y button should now turn left (lb): {l}')
    # by deviceDo: Pause onto X, then the swap of confirm and back
    p.ev("deviceShow('padsettings'); deviceDo({ app: 'padsettings', do: 'bind', arg: 'menu' })"); p.step(2); p.press('x'); p.step(2)
    check(p.ev("padButtonFor('menu')") == 'x' and p.ev("padButtonFor('x')") == 'menu', 'settings: Pause onto X should swap them')
    p.ev("deviceDo({ app: 'padsettings', do: 'swap', arg: true })")
    check(p.ev("padButtonFor('a')") == 'b' and p.ev("padButtonFor('b')") == 'a', 'settings: the swap should put confirm on B')
    p.ev("deviceDo({ app: 'padsettings', do: 'bind', arg: 'a' })"); p.step(2); p.press('rs'); p.step(2)
    check(p.ev("padButtonFor('a')") == 'rs' and p.ev("padButtonFor('rs')") == 'b' and p.ev('PAD_SET.swap') is True, f'settings: confirm onto RS with the swap on: a {p.ev("padButtonFor(\'a\')")}, rs {p.ev("padButtonFor(\'rs\')")}')
    # a light squeeze of a trigger is not a press, whatever action it's on (confirm onto LT for this)
    p.ev("deviceDo({ app: 'padsettings', do: 'bind', arg: 'a' })"); p.step(2); p.press('lt'); p.step(2)
    check(p.ev("padButtonFor('a')") == 'lt', 'settings: confirm onto LT'); p.log()
    p.js("Object.assign(window.__pads[0].buttons[6], { pressed: true, value: .3, touched: true })"); p.step(3); l = p.log()
    p.js("Object.assign(window.__pads[0].buttons[6], { pressed: false, value: 0, touched: false })"); p.step(2)
    check('a' not in l, f'settings: a light squeeze of LT (bound to confirm) pressed it: {l}')
    p.btn('lt', .9); p.step(2); l = p.log(); p.btn('lt', 0); p.step(2)
    check('a' in l, f'settings: LT squeezed past half way should confirm: {l}')
    p.ev("deviceShow('padsettings'); deviceDo({ app: 'padsettings', do: 'bind', arg: 'a' })"); p.step(2); p.press('rs'); p.step(2)
    p.ev("deviceDo({ app: 'padsettings', do: 'bind', arg: 'view' })"); p.step(2); p.press('view'); p.step(2)
    check(p.ev("padButtonFor('view')") == 'view', 'settings: pressing an action\'s own button should keep it')
    for verb, val in [('dead', .32), ('walk', 'gentle'), ('zoom', 1.6), ('flip', True), ('turn', 'hold'), ('marks', 'off'), ('first', .8), ('every', 0), ('buzz', True), ('sticks', True)]:
        p.ev(f"deviceDo({{ app: 'padsettings', do: {json.dumps(verb)}, arg: {json.dumps(val)} }})")
    check(p.ev('PAD_DEAD.stick') == .32 and p.ev('PAD_REP.first === Infinity') and p.ev('PAD_REP.every') == .25, 'settings: the dead zone and the menu repeat (no repeat) should take effect')
    p.axes([0, 0, 1, 0]); p.step(1); check(p.ev('PAD.ls[0]') == 1 and p.ev('PAD.rs[0]') == 0, 'settings: with the sticks swapped the right stick should walk'); p.axes([0, 0, 0, 0]); p.step(1)
    check(p.ev('padMarkFamily()') is None, 'settings: button pictures off should give no family')
    sv = p.ev(SV)['pad']; n = len(json.dumps(sv, separators=(',', ':')))
    check(n < 250, f'settings: the saved changes should be small: {n} bytes {sv}')
    want = p.ev('JSON.stringify(PAD_SET)'); mk = p.ev('PAD_MAPK.join()')
    # reload: the save written, the page opened again with saving on; it all holds
    p.ev(SAVE_NOW); url = p.g.page.url.replace('?nosave&debug', '?debug')
    p.g.page.goto(url); p.g.page.wait_for_function('window.__sc !== undefined || window.__err', timeout=60000); p.step(5)
    check(p.ev('JSON.stringify(PAD_SET)') == want and p.ev('PAD_MAPK.join()') == mk and p.ev('PAD_DEAD.stick') == .32, 'settings: the changes did not hold through a reload')
    check(p.ev("deviceView('settings').blocks.slice(-1)[0].items[0].label") == 'Controller settings', 'settings: changed settings should keep the page shown after a reload with no pad')
    p.plug(); p.press('a'); p.log()
    # turning by holding: 1.3 s of the right stick turns three times (flick: once); the right stick flipped zooms out
    p.ev('azT = az = Math.PI / 4'); p.axes([1, 0, 0, 0]); p.step(39); p.axes([0, 0, 0, 0]); p.step(2)
    turns = round(p.ev('(azT - Math.PI / 4) / (Math.PI / 2)')); check(turns == 3, f'settings: holding to turn for 1.3 s should give 3 quarter turns: {turns}')
    p.ev('setZoom(padZoom0())'); z0 = p.ev('camera.zoom'); p.axes([0, -1, 0, 0]); p.step(6); p.axes([0, 0, 0, 0]); p.step(1)
    check(p.ev('camera.zoom') < z0, 'settings: flipped, up on the right stick should zoom out')
    p.axes([0, 0, 1, 0]); p.step(2); k = p.ev('player.steer && player.steer.k'); p.axes([0, 0, 0, 0]); p.step(2)
    check(k is not None and k <= .6, f'settings: gentle walking at full push: {k}')
    # vibration: on (it held), a buzz of a known kind reaches the pad; an unknown kind, or vibration off, doesn't
    p.js("window.__bz = 0; window.__pads[0].vibrationActuator = { playEffect: () => { window.__bz++; return Promise.resolve(); } }")
    r = [p.ev("padBuzz('done')"), p.ev("padBuzz('nope')")]; p.ev("PAD_SET.buzz = false"); r.append(p.ev("padBuzz('pick')")); p.ev("PAD_SET.buzz = true")
    check(r == [True, False, False] and p.js('window.__bz') == 1, f'settings: vibration: {r}, {p.js("window.__bz")} buzzes')
    # P5's one-hand layouts (a stand-in PAD_LAYOUTS): the buttons show, right turns the sticks over, back to normal clears both
    p.ev("window.PAD_LAYOUTS = { left: Object.fromEntries(PAD_BTN.map((n, i) => [n, PAD_BTN[(i + 1) % 16]])), right: Object.fromEntries(PAD_BTN.map(n => [n, n === 'a' ? 'rs' : n === 'rs' ? 'a' : n])) }")
    labels = p.ev("padSetView().blocks.flatMap(b => (b.items || []).map(i => i.label))")
    check('One hand: left' in labels and 'One hand: right' in labels, 'settings: the one-hand buttons should show with PAD_LAYOUTS')
    p.ev("deviceDo({ app: 'padsettings', do: 'hand', arg: 'right' })")
    check(p.ev("padButtonFor('a')") == 'rs' and p.ev('PAD_SET.sticks') is True and p.ev('PAD_SET.swap') is False, 'settings: One hand: right should set its map and swap the sticks')
    p.ev("deviceDo({ app: 'padsettings', do: 'hand', arg: 'left' })")
    check(p.ev("padButtonFor('a')") == 'b' and p.ev('PAD_SET.sticks') is False, 'settings: One hand: left should set its map, sticks normal')
    p.ev("deviceDo({ app: 'padsettings', do: 'normalbtn' })")
    check(p.ev('Object.keys(PAD_SET.map).length') == 0 and p.ev('PAD_SET.sticks') is False, 'settings: Buttons back to normal should clear the map and the sticks')
    # an odd save stays normal: two actions on one button, a value not offered
    p.ev("padSetLoad({ map: { a: 'b' }, dead: .5, marks: 'sega', swap: 'yes' })")
    check(p.ev('padSetDiff()') is None and p.ev('PAD_MAPK.join()') == p.ev('PAD_BTN.join()'), 'settings: an odd save should load as normal')
    p.ev(f"padSetLoad({json.dumps(sv)})"); check(p.ev('padSetDiff() !== null'), 'settings: loading the changes back')
    # everything back to normal (two presses): nothing saved, the save's extras as before any change
    p.ev("deviceShow('padsettings'); deviceDo({ app: 'padsettings', do: 'normal' })"); check(p.ev('padSetDiff() !== null'), 'settings: one press of Everything back to normal should only ask')
    p.ev("deviceDo({ app: 'padsettings', do: 'normal' })")
    check(p.ev('padSetDiff()') is None and 'pad' not in p.ev(SV) and p.ev('PAD_MAPK.join()') == p.ev('PAD_BTN.join()') and p.ev('PAD_DEAD.stick') == .22 and p.ev('PAD_REP.first') == .5 and p.ev('PAD_SET.sticks') is False and p.ev('PAD_REP.every') == .25,
          f'settings: Everything back to normal should leave nothing changed and nothing saved: {p.ev("[padSetDiff(), PAD_MAPK.join(), PAD_DEAD.stick, PAD_REP.first, PAD_REP.every]")} {list(p.ev(SV).keys())[:3]}')
    p.ev('localStorage.clear()'); p.close()

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
    p.ev("(() => { const c = document.createElement('div'); c.id = 'tClk'; c.textContent = 'tap me'; c.onclick = () => {}; document.getElementById('tstPanel').appendChild(c); })()")
    check(any('tClk' in m for m in p.ev(CLICKY)), 'api: the page cross-check should find a box with an onclick the highlight cannot reach')
    p.ev("document.getElementById('tClk').remove()")
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
    # (PR9) a touch after the pad: the button the pad highlighted loses its focus (no outline for a touch player)
    p.ev("padFocusTo(document.getElementById('t1'))"); p.step(1)
    p.ev("document.querySelector('canvas').dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))"); p.step(2)   # a touch that moves no focus itself
    check(p.ev("document.activeElement && document.activeElement.id") != 't1', 'api: a touch should take the focus off the pad\'s highlighted button')
    check(p.ev("getComputedStyle(document.getElementById('t1')).outlineStyle") == 'none', 'api: no outline left on it after a touch')
    p.press('x'); p.step(2); p.ev("padFocusTo(document.getElementById('t3'))")
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

# ---- P2: the mini-games (controller package 2) ----
TL_FOCUS = "(() => { const a = document.activeElement, R = TL_UI.root; if (!a || !R || !R.contains(a)) return null; const d = a.dataset; return d.c !== undefined ? 'c' + d.c : d.h !== undefined ? 'h' + d.h : d.end ? 'e' + d.end : '?'; })()"
def tl_nav(p, cell):                                   # D-pad to a square, one square a press
    for _ in range(14):
        f = p.ev(TL_FOCUS)
        if not f or f[0] != 'c': return False
        c = int(f[1:])
        if c == cell: return True
        dx, dy = cell % 6 - c % 6, cell // 6 - c // 6
        p.press('right' if dx > 0 else 'left' if dx < 0 else 'up' if dy > 0 else 'down'); p.step(1)
        n = p.ev(TL_FOCUS)
        want = c + (1 if dx > 0 else -1 if dx < 0 else 6 if dy > 0 else -6)
        if not check(n == 'c%d' % want, f'tiles: a D-pad press from square {c} should land on square {want}, not {n}'): return False
    return False

def part_tiles(pw):
    p = Pad(pw, ON)
    p.plug(); p.press('x'); p.log()
    p.ev("SHIP.device.tipsSeen.device = true; tilesPlay('tomas', null, 'full'); if (TL_GAME.timer) { clearTimeout(TL_GAME.timer); TL_GAME.timer = 0; }"); p.step(3)
    check(p.ev(TL_FOCUS) == 'etnext', f'tiles: your first game should land on How to play\'s Next, not {p.ev(TL_FOCUS)}')
    for _ in range(12):
        if p.ev('TL_GAME.tut') < 0: break
        p.press('a'); p.step(1)
    check(p.ev('TL_GAME.tut') < 0, 'tiles: A on Next should go through How to play')
    f = p.ev(TL_FOCUS); check(f and f[0] == 'c', f'tiles: after How to play the highlight should be on a square, not {f}')
    # one move by the pad alone: to the tile, A, to the square, A
    mv = p.ev("(() => { const m = tilesMoves(TL_GAME.s, 0).find(m => m.k === 's') || tilesMoves(TL_GAME.s, 0).find(m => m.from !== undefined); return m ? [m.from, m.to] : null; })()")
    plies = p.ev('TL_GAME.s.plies')
    if check(mv, 'tiles: no move to make') and tl_nav(p, mv[0]):
        p.press('a'); check(p.ev('TL_GAME.sel && TL_GAME.sel.c') == mv[0], f'tiles: A on square {mv[0]} should pick up its tile')
        check(p.ev(TL_FOCUS) == 'c%d' % mv[0], 'tiles: the highlight should stay on the square after A')
        if tl_nav(p, mv[1]):
            p.press('a'); check(p.ev('TL_GAME.s.plies') == plies + 1, f'tiles: A on square {mv[1]} should put the tile down (a move made)')
    p.ev("if (TL_GAME.timer) { clearTimeout(TL_GAME.timer); TL_GAME.timer = 0; }")
    # the hold: A picks a tile in your hold, and the highlight keeps its place when the board redraws
    p.ev("TL_GAME.s.p = 0; TL_GAME.sel = null; TL_GAME.s.hold[0] = [1]; tilesDraw(); padFocusTo(TL_UI.root.querySelector('[data-h=\"1\"]'))"); p.step(2)
    p.press('a'); p.step(2)
    check(p.ev('TL_GAME.sel && TL_GAME.sel.h') == 1 and p.ev(TL_FOCUS) == 'h1', f'tiles: A on your hold should pick its tile and keep the highlight there ({p.ev(TL_FOCUS)})')
    p.press('up'); f = p.ev(TL_FOCUS); check(f and f[0] in 'ce', f'tiles: D-pad up from your hold should go back toward the board, not {f}')
    # the end: Again highlighted; along to Done, A
    p.ev("""(() => { const G = TL_GAME; G.sel = null; G.s.sc = [6, 0]; G.s.p = 0; let n = 0; while (!G.s.over && n++ < 80) { if (G.timer) { clearTimeout(G.timer); G.timer = 0; } if (G.s.p === 0) tilesDo(tilesAI(G.s, 'hard', G.rng)); else { const mv = tilesMoves(G.s, 1).find(m => !tilesApply(G.s, m).pts) || tilesMoves(G.s, 1)[0]; tilesDo(mv); } } if (G.timer) clearTimeout(G.timer); })()"""); p.step(3)
    p.g.page.wait_for_timeout(1500); p.step(3)              # (the board redraws on its own timer once its moves' animations end; the highlight follows a frame later)
    if check(p.ev('TL_GAME.s.over'), 'tiles: the game did not end'):
        check(p.ev(TL_FOCUS) == 'efull', f'tiles: at the end the highlight should be on Again, not {p.ev(TL_FOCUS)}')
        p.press('right'); check(p.ev(TL_FOCUS) == 'equick', f'tiles: D-pad right from Again should reach Quick game ({p.ev(TL_FOCUS)})')
        p.press('left'); p.press('down')                     # (on a phone Done wraps to a row of its own, under Again)
        check(p.ev(TL_FOCUS) == 'edone', f'tiles: the D-pad should reach Done ({p.ev(TL_FOCUS)})')
        p.press('a'); p.step(2); check(p.ev('TL_GAME') is None, 'tiles: A on Done should end the game')
    p.close()

LD_FOCUS = "(() => { const a = document.activeElement, V = DISC.view; if (!V || !a || !V.root.contains(a)) return null; return a === V.leave ? 'leave' : a === V.howNext ? 'next' : a.textContent; })()"
def part_disc(pw):
    p = Pad(pw, ON)
    p.plug(); p.press('x'); p.log()
    begin = "discBegin(DECK_CREW.find(a => !a.asleep) || DECK_CREW[0], %s)"   # (Again needs your opponent on the deck)
    p.ev(begin % 'false'); p.step(3)
    check(p.ev("(padLayer() || {}).id") == 'ld', 'disc: Lightdisc\'s view should be the panel on top')
    check(p.ev(LD_FOCUS) == 'next', f'disc: How to play\'s Next should have the highlight, not {p.ev(LD_FOCUS)}')
    p.press('a'); check(p.ev('DISC.how') == 1, 'disc: A should be Next in How to play')
    # the stick: a light push is a slow step, a full one the arrow keys' speed; it never moves the highlight; let go stops
    def run(x, n=10):
        x0 = p.ev('DISC.g.p[0].x'); p.axes([x, 0, 0, 0]); p.step(n); k = p.ev('DISC.inp.kx'); x1 = p.ev('DISC.g.p[0].x'); return k, x1 - x0
    p.ev('DISC.g.p[0].x = 0'); kl, dl = run(-.45)
    p.ev('DISC.g.p[0].x = 0'); kf, df = run(-1)
    check(-1 < kl < 0 and kf == -1, f'disc: the stick should set the move by how far it is pushed ({kl}, {kf})')
    check(dl < 0 and df < 0 and abs(df) > abs(dl) * 1.5, f'disc: a full push should go further than a light one ({dl:.2f}, {df:.2f})')
    check(p.ev(LD_FOCUS) == 'next', f'disc: the stick moved the highlight ({p.ev(LD_FOCUS)})')
    p.axes([0, 0, 0, 0]); p.step(2); check(p.ev('DISC.inp.kx') == 0 and p.ev('DISC.inp.kz') == 0, 'disc: letting go of the stick should stop you')
    for _ in range(4):
        if p.ev('DISC.how') < 0: break
        p.press('a')
    check(p.ev('DISC.how') == -1, 'disc: A should go through How to play')
    p.step(2); check(p.ev(LD_FOCUS) == 'leave', f'disc: with How to play done the highlight goes to Leave ({p.ev(LD_FOCUS)})')
    p.press('a'); p.step(2); check(p.ev('!!DISC.g && !!DISC.view'), 'disc: A should never press Leave by itself')
    p.press('b'); p.step(3); check(p.ev('!DISC.g && !document.getElementById("ld")'), 'disc: B should be Leave')
    # the result card: Again highlighted, the D-pad along it, A presses
    p.ev(begin % 'false'); p.step(3)
    p.ev("(() => { const G = DISC.g; G.over = true; G.winner = 0; G.score = [7, 3]; G.phase = 'over'; discOver(); discResult(); })()"); p.step(3)
    check(p.ev(LD_FOCUS) == 'Again', f'disc: the result card should land on Again ({p.ev(LD_FOCUS)})')
    p.press('right'); check(p.ev(LD_FOCUS) == 'Quick game', f'disc: D-pad right on the result card should reach Quick game ({p.ev(LD_FOCUS)})')
    p.press('a'); p.step(3); check(p.ev('!!DISC.g && DISC.g.target') == 5, 'disc: A on Quick game should start a game to 5')
    p.press('b'); p.step(3); check(p.ev('!DISC.g'), 'disc: B should leave the quick game')
    p.close()

FOCUS_ID = "(() => { const a = document.activeElement; return a ? (a.id || a.textContent.trim().slice(0, 24)) : null; })()"
def part_screens(pw):
    p = Pad(pw, ON)
    p.plug(); p.press('x'); p.log()
    # the lift: your goal's deck highlighted; A rides; B stays
    goal = p.ev("(() => { const n = [4, 5, 6, 7, 3, 2, 1].find(n => DECKS[n] && n !== deckDef.num); setGoal({ deck: n, x: 0, z: 0, label: 'test' }); return n; })()")
    p.ev('openLiftPanel()'); p.step(3)
    check(p.ev("document.activeElement && document.activeElement.classList.contains('goal')"), f'screens: the lift should highlight your goal deck ({goal}), not {p.ev(FOCUS_ID)}')
    p.press('b'); p.step(2); check(p.ev("document.getElementById('lift').hidden") and not p.ev('ride'), 'screens: B on the lift should stay')
    p.ev('window.__pp = []; window.__ppWas = pressPanel; pressPanel = n => __pp.push(n); openLiftPanel()'); p.step(3); p.press('a'); p.step(2)   # (the ride itself needs you in the car)
    check(p.ev('__pp.join()') == str(goal), f'screens: A on the goal deck should ride to it ({p.ev("__pp.join()")})')
    p.ev('pressPanel = __ppWas; setGoal(null)')
    # the alarm: Set alarm highlighted; − and + in reach; B is Not yet
    p.ev('alarmOpen()'); p.step(3)
    check(p.ev(FOCUS_ID) == 'sleepYes', f'screens: the alarm should land on Set alarm, not {p.ev(FOCUS_ID)}')
    t0 = p.ev("document.getElementById('alarmT').textContent"); p.press('up'); f = p.ev(FOCUS_ID)
    if check(f in ('alarmDn', 'alarmUp'), f'screens: D-pad up from Set alarm should reach − or +, not {f}'):
        p.press('a'); check(p.ev("document.getElementById('alarmT').textContent") != t0, 'screens: A on − or + should move the alarm')
        p.press('left' if f == 'alarmUp' else 'right'); check(p.ev(FOCUS_ID) in ('alarmDn', 'alarmUp') and p.ev(FOCUS_ID) != f, 'screens: the D-pad should reach the other of − and +')
    p.press('b'); p.step(2); check(p.ev("document.getElementById('sleepAsk').hidden"), 'screens: B on the alarm should close it')
    # a work step's turn card (deviceChoose): the first answer highlighted, not the ×; the place kept when it asks again; B is the ×
    p.ev("window.__ws = { picks: [], v: 0 }; window.__ask = () => deviceChoose({ title: 'The setting', text: 'v ' + __ws.v, choices: ['−', '+'], cancel: 'Step back' }, i => { __ws.picks.push(i); if (i >= 0) { __ws.v += i ? 1 : -1; if (__ws.v < 3) __ask(); } }); __ask()"); p.step(3)
    check(p.ev(FOCUS_ID) == '−', f'screens: a turn card should land on its first answer, not {p.ev(FOCUS_ID)}')
    p.press('right'); check(p.ev(FOCUS_ID) == '+', f'screens: D-pad right should reach + ({p.ev(FOCUS_ID)})')
    for _ in range(3): p.press('a'); p.step(2)
    check(p.ev('__ws.v') == 3 and p.ev('__ws.picks.join()') == '1,1,1', f'screens: A three times on + should keep the place as the card asks again ({p.ev("__ws.picks.join()")})')
    p.ev('__ws.v = 0; __ask()'); p.step(3); p.press('b'); p.step(2)
    check(p.ev('__ws.picks.slice(-1)[0]') == -1 and p.ev('!DEV.choose'), 'screens: B on a question should be the × (Not now, Step back)')
    # the arrival's manifest: the name box first; A on Sign with it empty fills a suggested name; A again signs
    p.ev("if (typeof introManifest === 'function') introManifest()"); p.step(4)
    if check(p.ev("(padLayer() || {}).id") == 'introManifest', f'screens: the manifest should be the panel on top ({p.ev("(padLayer() || {}).id")})'):
        check(p.ev("document.activeElement && document.activeElement.tagName") == 'INPUT', 'screens: the manifest should land in the name box')
        p.press('b'); p.step(2); check(p.ev("(padLayer() || {}).id") == 'introManifest', 'screens: B should not leave the manifest')
        p.press('down'); check(p.ev("document.activeElement && document.activeElement.tagName") == 'BUTTON', 'screens: D-pad down should reach Sign and go aboard')
        p.press('a'); check(p.ev("INTRO_UI.manifest && INTRO_UI.manifest.querySelector('input').value") == p.ev('PAD_NAME'), 'screens: A on Sign with no name should fill in the suggested one')
        p.ev("INTRO_UI.manifest.querySelector('button').focus()"); p.press('a'); p.step(3)
        check(p.ev('!INTRO_UI.manifest') and p.ev('SHIP.player.name') == p.ev('PAD_NAME'), f'screens: A on Sign again should sign ({p.ev("SHIP.player.name")})')
    p.close()

PARTS = [('off', part_off), ('quiet', part_quiet), ('base', part_base), ('deck', part_deck), ('pick', part_pick), ('panels', part_panels), ('api', part_api), ('lists', part_lists), ('tiles', part_tiles), ('disc', part_disc), ('screens', part_screens), ('marks', part_marks), ('touch', part_touch), ('drop', part_drop), ('settings', part_settings)]
with sync_playwright() as pw:
    for name, fn in PARTS:
        if ONLY and name not in ONLY: continue
        print('part', name, flush=True)
        try: fn(pw)
        except Exception as e: fail(f'{name}: {type(e).__name__}: {e}')
print('CONTROLLER CHECK OK' if ok else 'CONTROLLER CHECK FAILED')
sys.exit(0 if ok else 1)
