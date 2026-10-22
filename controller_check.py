# Starship Cadet: controller check (keep in the repo; CTT, the controller test builder; plans/controller-plan.html section 10)
# Plays the game with a pretend controller: before the game loads, navigator.getGamepads is replaced by scripted pads
# (buttons and sticks the check sets frame by frame) that are announced the way a real one is (gamepadconnected).
# The check is built part by part as the controller work (section 26, CONTROLLER) lands. A part whose package isn't
# built yet says "not yet": never a pass. The packages built are read from the game itself (PAD_BUILT in section 26,
# e.g. ['base', 'deck']); a game with no section 26 has none, and every controller part is "not yet".
#
# Parts (run them all, or name some):
#   idle      the game is the same, pixel for pixel, with no pad, with the pad API and no pad, with a pad plugged in but
#             never pressed, and with a drifting pad (sticks wobbling inside any sane dead zone); with PAD_ON off and,
#             in a copy, on. Same pictures, same crew, same DOM, same styles, same random numbers, same storage.
#   save      the save with an idle or drifting pad is byte-identical to the one with no pad (settings: "not yet" until
#             the settings package: change a button, save, reload, the change holds)
#   calls     draw calls and triangles with an idle pad are the no-pad ones (with the ring, at phone size: "not yet")
#   touch     touch after pad: press, then tap: the picture is the no-pad one and no focus outline is left (base)
#   walk      walking in all four view directions, letting go stops; turning and zooming (deck)
#   pick      the ringed thing and A, against cadet_test's taps (pick)
#   reach     the non-circular sweep: the clickables are read from the page itself (every element that is a button,
#             link or input, or has a click/pointer/touch listener, or shows a hand cursor), first by mouse through every
#             panel and menu; then every one must be reached and pressed by pad (panels)
#   day       a whole ship day played by pad (all packages)
#   games     Tiles to the end, and Lightdisc (games)
#   unplug    disconnect: stop walking at once, pause if used lately; reconnect resumes (deck, marks)
#   odd       a pad that doesn't report the standard layout, and two pads (deck)
# --inventory: with reach, runs its touch half even before the panels package (the list of what there is to reach).
# --selftest: runs the parts on a copy with this check's own small stand-in driver (to prove the parts before section 26).
# --mutants: plants faults in copies of the game (each part's own list) and checks the part FAILS on every one.
# CTL_BUILT=pkg,pkg: count those packages as built (a builder's branch before PAD_BUILT names them).
# Setup and environment as for cadet_test.py (CADET_WORK, CADET_CHROME=/opt/pw-browsers/chromium).
# Run:  python3 controller_check.py BUILD.html [part ...] [--mutants]
import sys, json, re, os, pathlib
exec(open(__file__.replace('controller_check.py', 'cadet_test.py')).read().split("a, shots = run(")[0])

ARGS = [a for a in sys.argv[1:] if not a.startswith('--')]
FLAGS = {a for a in sys.argv[1:] if a.startswith('--')}
GAME = pathlib.Path(ARGS[0])
ALL_PARTS = ['idle', 'save', 'calls', 'touch', 'walk', 'pick', 'reach', 'day', 'games', 'unplug', 'odd',
             'off', 'quiet', 'base', 'deck', 'pick1', 'panels', 'api', 'lists', 'tiles', 'disc', 'screens', 'marks', 'touch3', 'drop', 'settings', 'a11y', 'firstuse']
PARTS = ARGS[1:] or ALL_PARTS
SHOTS = WORK / 'test' / 'ctl_shots'; SHOTS.mkdir(parents=True, exist_ok=True)
ARGS_GL = ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist']

# ---- the pretend controller --------------------------------------------------------------------------------------
# mode 'none': the browser's own navigator.getGamepads, untouched (the game as everyone plays it today).
# Otherwise getGamepads is replaced: four slots, a fresh copy of each pad on every call (as Chrome does), and
# window.__pads to plug, unplug and set pads. A pad: { id, mapping, nb (buttons), na (axes), drift }. drift: every read
# gives the sticks a wobble of up to +-0.05 and the triggers 0.02 (an LCG, so the same every run), never a press.
FAKEPAD = r"""
(() => {
  const CFG = __CFG__;
  { let r = 99991; Math.random = () => (r = (r * 48271) % 2147483647) / 2147483647; }   // the same every run (the career's seed gs reads it)
  if (CFG.mode === 'none') return;
  const slots = [null, null, null, null];
  let s = 12345; const rnd = () => (s = (s * 48271) % 2147483647) / 2147483647;
  const mk = (i, o) => ({ id: o.id || 'Xbox Wireless Controller (STANDARD GAMEPAD Vendor: 045e Product: 0b13)', index: i, connected: true,
    mapping: o.mapping === undefined ? 'standard' : o.mapping, timestamp: performance.now(), drift: !!o.drift,
    axes: new Array(o.na || 4).fill(0), buttons: Array.from({ length: o.nb || 17 }, () => ({ pressed: false, touched: false, value: 0 })) });
  const copy = p => {
    const axes = p.axes.slice(), buttons = p.buttons.map(b => ({ pressed: b.pressed, touched: b.touched, value: b.value }));
    if (p.drift) { for (let k = 0; k < axes.length; k++) if (axes[k] === 0) axes[k] = (rnd() - .5) * .1; for (const k of [6, 7]) if (buttons[k] && !buttons[k].pressed) buttons[k].value = .02; }
    return Object.freeze({ id: p.id, index: p.index, connected: p.connected, mapping: p.mapping, timestamp: p.timestamp, axes: Object.freeze(axes), buttons: Object.freeze(buttons.map(Object.freeze)), vibrationActuator: null });
  };
  const fire = (type, p) => { const e = new Event(type); Object.defineProperty(e, 'gamepad', { value: copy(p) }); window.dispatchEvent(e); };
  window.__pads = {
    reads: 0,
    // o.hidden: the browser keeps the pad to itself (getGamepads gives null, no event) until a button is first pressed,
    // then shows it and says hello in that same moment, as Chrome does (mode a); otherwise it's there at once (mode b)
    plug(i, o) { slots[i] = mk(i, o || {}); slots[i].hidden = !!(o && o.hidden); if (!slots[i].hidden) fire('gamepadconnected', slots[i]); },
    unplug(i) { const p = slots[i]; if (!p) return; p.connected = false; slots[i] = null; fire('gamepaddisconnected', p); },
    // b: { index: value 0..1 } (pressed above .5 for the face buttons, any value for the triggers), a: { index: value }
    set(i, b, a) { const p = slots[i]; if (!p) return; for (const k in (b || {})) { const v = +b[k]; p.buttons[k] = { pressed: v > .1, touched: v > 0, value: v }; }
      if (p.hidden && p.buttons.some(x => x.value > 0)) { p.hidden = false; fire('gamepadconnected', p); }
      for (const k in (a || {})) p.axes[k] = +a[k]; p.timestamp = performance.now(); },
    clear(i) { const p = slots[i]; if (!p) return; p.axes.fill(0); p.buttons.forEach((b, k) => p.buttons[k] = { pressed: false, touched: false, value: 0 }); p.timestamp = performance.now(); },
  };
  Object.defineProperty(Navigator.prototype, 'getGamepads', { configurable: true, value: function () { window.__pads.reads++; return slots.map(p => p && !p.hidden ? copy(p) : null); } });
  window.__padPlug = (i, id, mapping) => { slots[i] = mk(i, { id, mapping }); return true; };
  window.__padHello = i => { fire('gamepadconnected', slots[i]); return true; };
  window.__padUnplug = i => { window.__pads.unplug(i); return true; };
  window.__padBtn = (i, k, v) => { window.__pads.set(i, { [k]: v }); return true; };
  window.__padAxes = (i, a) => { window.__pads.set(i, null, Object.fromEntries(a.map((v, k) => [k, v]))); return true; };
  if (CFG.plug) { const go = () => window.__pads.plug(0, CFG.plug); document.readyState === 'loading' ? addEventListener('DOMContentLoaded', go) : go(); }
})();
"""
# the standard mapping's buttons (W3C "standard gamepad"), by position
BTN = dict(A=0, B=1, X=2, Y=3, LB=4, RB=5, LT=6, RT=7, VIEW=8, MENU=9, LS=10, RS=11, UP=12, DOWN=13, LEFT=14, RIGHT=15, HOME=16)

# ---- the game, its switches and its packages ---------------------------------------------------------------------
SRC = GAME.read_text()
def pad_switch(src):
    m = re.search(r'\bconst PAD_ON\s*=\s*(true|false)\b', src)
    return None if not m else m.group(1) == 'true'
def with_switch(src, on):
    return re.sub(r'(\bconst PAD_ON\s*=\s*)(true|false)\b', r'\g<1>' + ('true' if on else 'false'), src, count=1)
# the packages, from section 26's PAD_BUILT line; until it has one, found from section 26's own tables (and said so)
FOUND_BY = [('base', r'\bconst PAD_ON\s*='), ('deck', r'\bconst PAD_DECK\s*='), ('pick', r'\bconst PAD_PICK\s*=')]
def pad_built(src):
    m = re.search(r'\bconst PAD_BUILT\s*=\s*\[([^\]]*)\]', src)
    if m: return set(re.findall(r"['\"](\w+)['\"]", m.group(1))), 'PAD_BUILT'
    return {k for k, rx in FOUND_BY if re.search(rx, src)}, 'found from the code (no PAD_BUILT line)'

ok = True
RESULTS = []   # (part, 'OK' | 'FAIL' | 'not yet', note)
def check(cond, msg):
    global ok
    if not cond: ok = False; print('FAIL', msg)
    return cond

QUIET = '#toast,.nf{opacity:0!important} #needFx{display:none!important} #devHu{display:none!important} #needStrip{display:none!important} #devBtn{box-shadow:none!important} *,*::before,*::after{transition:none!important;animation:none!important} .bubw{opacity:0!important}'
# .bubw (speech bubbles) out of the pictures: mid-fade, one in three runs drew a bubble's layer a shade differently with
# the same DOM and styles (a compositor quirk). Their text, place and fade are still compared through the page state.
class Run:
    """One page of the game with the pretend controller in a given mode. extra: JS put into the game's scope at load."""
    def __init__(self, br, src, tag, mode='none', plug=None, w=900, h=760, query='?nosave&debug', storage=None, touch=False):
        self.errors = []
        # a browser of its own for every run, as cadet_test does: a second page in one browser sometimes drew a speech
        # bubble's layer differently (the same styles and DOM, different pixels), a browser quirk, not the game
        self.br = br.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=ARGS_GL)
        self.ctx = self.br.new_context(viewport={'width': w, 'height': h}, device_scale_factor=1, has_touch=touch)
        self.page = self.ctx.new_page()
        self.page.on('console', lambda m: m.type in ('error', 'warning') and self.errors.append(f'{m.type}: {m.text}'))
        self.page.on('pageerror', lambda e: self.errors.append(f'pageerror: {e}'))
        self.page.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
        if storage: self.page.add_init_script('(() => { const s = ' + json.dumps(storage) + '; for (const k in s) localStorage.setItem(k, s[k]); })();')
        self.page.add_init_script(INIT)
        self.page.add_init_script(FAKEPAD.replace('__CFG__', json.dumps({'mode': mode, 'plug': plug})))
        self.page.add_init_script(CENSUS)
        f = WORK / 'test' / f'_ctl_{tag}.html'
        # the same quiet style as cadet_test's, but in the page from the start: added after loading, a speech bubble made
        # on the first frames could be caught mid pop-in, a different picture depending on how fast the machine ran
        f.write_text(instrument(src).replace('</head>', '<style>' + QUIET + '</style></head>', 1))
        self.page.goto('file://' + str(f) + query)
        try: self.page.wait_for_function('window.__sc !== undefined || window.__err', timeout=90000)
        except Exception: pass
        if self.page.evaluate('window.__sc === undefined'): raise RuntimeError('game failed to start: ' + ' | '.join(self.errors[:6]))
        self.ev(SKIP_SWITCH)
        # let the game's own real-time timers at load run first (section 19's DEV.live at 0 ms, section 17's machine
        # averages from 300 ms), so every run starts from the same place however fast the machine is
        try: self.page.wait_for_function("window.__sc('typeof MACH_NORM === \\'undefined\\' || MACH_NORM !== null')", timeout=30000)
        except Exception: pass
        self.page.wait_for_timeout(300)
        # (RV5) the welcome message hides itself on a real-time timer (5.6 s), so whether it still shows at the first
        # snapshot depended on the machine's speed: put it away now, the same in every run (its text stays in the page)
        self.ev("typeof toastTimer !== 'undefined' && clearTimeout(toastTimer); typeof toastEl !== 'undefined' && toastEl.classList.remove('show')")
    def reload(self):
        self.page.reload(timeout=90000)
        self.page.wait_for_function('window.__sc !== undefined || window.__err', timeout=90000)
        self.ev(SKIP_SWITCH); self.page.wait_for_timeout(300)
    def ev(self, s): return self.page.evaluate('s => window.__sc(s)', s)
    def js(self, s): return self.page.evaluate(s)
    def step(self, n, dt=1000/30):
        if n > 1: self.page.evaluate(f'window.__skip = true; window.__step({n - 1}, {dt}); window.__skip = false')
        self.page.evaluate(f'window.__step(1, {dt})')
    # the pad, frame by frame: hold buttons / sticks for n frames, then let go (and one frame for the release)
    def pad(self, n=2, b=None, a=None, i=0, release=True):
        self.js(f'window.__pads.set({i}, {json.dumps({str(BTN.get(k, k)): v for k, v in (b or {}).items()})}, {json.dumps({str(k): v for k, v in (a or {}).items()})})')
        self.step(n)
        if release: self.js(f'window.__pads.clear({i})'); self.step(1)
    def press(self, name, i=0): self.pad(2, {name: 1}, i=i)
    def shot(self, name):
        p = str(SHOTS / f'{name}.png'); self.page.screenshot(path=p); return p
    def close(self): self.br.close()

# Everything the page shows that a controller must not change while unused: the DOM (elements, their classes, inline
# styles and text), the style sheets, storage, the random seed, listeners asked for. Read at each snapshot.
# CENSUS also records every element that gets a click-like listener (for the reachability sweep): non-circular, it
# is the page's own wiring, not a list kept by the controller team.
CENSUS = r"""
(() => {
  const TYPES = new Set(['click', 'pointerdown', 'pointerup', 'mousedown', 'mouseup', 'touchstart', 'touchend', 'dblclick', 'keydown']);
  const tagged = new WeakMap(); const counts = {};
  const add = EventTarget.prototype.addEventListener;
  EventTarget.prototype.addEventListener = function (type, fn, opt) {
    counts[type] = (counts[type] || 0) + 1;
    if (TYPES.has(type) && this instanceof Element) { if (!tagged.has(this)) tagged.set(this, new Set()); tagged.get(this).add(type); }
    return add.call(this, type, fn, opt);
  };
  window.__census = { tagged, counts, lastClick: null };
  add.call(document, 'click', e => { window.__census.lastClick = e.target; }, true);   // which element the last click reached
})();
"""
# listeners: every kind asked for, less the two waiting ones (gamepadconnected, gamepaddisconnected) allowed at load
PAGE_STATE = r"""(() => {
  let h = 0; const mix = s => { for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) | 0; };
  let n = 0; for (const e of document.querySelectorAll('*')) { n++; mix(e.tagName + '|' + e.id + '|' + e.className + '|' + (e.getAttribute('style') || '') + '|' + (e.hidden ? 'h' : '') + (e === document.activeElement ? 'F' : '')); if (e.tagName !== 'SCRIPT' && e.tagName !== 'STYLE') for (const c of e.childNodes) if (c.nodeType === 3) mix(c.textContent); }
  let rules = 0; for (const s of document.styleSheets) { try { rules += s.cssRules.length; } catch (e) {} }
  const ls = []; try { for (let i = 0; i < localStorage.length; i++) { const k = localStorage.key(i); ls.push(k + '=' + localStorage.getItem(k).length); } } catch (e) {}
  return { elements: n, domHash: h, sheets: document.styleSheets.length, rules, storage: ls.sort(), listeners: Object.fromEntries(Object.entries(window.__census.counts).filter(([k]) => k !== 'gamepadconnected' && k !== 'gamepaddisconnected')), focus: document.activeElement && (document.activeElement.id || document.activeElement.tagName) };
})()"""
GAME_STATE = r"""(() => ({ seed, walkers: walkers.map(w => [w.spec.name, Math.round(w.obj.position.x * 1e4), Math.round(w.obj.position.z * 1e4), Math.round(w.obj.rotation.y * 1e3), w.goal]),
  player: [Math.round(player.obj.position.x * 1e4), Math.round(player.obj.position.z * 1e4), player.deck], time: [SHIP.time.day, SHIP.time.min],
  cam: [Math.round(camera.zoom * 1e4), Math.round(az * 1e4), Math.round(target.x * 1e4), Math.round(target.z * 1e4)],
  calls: renderer.info.render.calls, tris: renderer.info.render.triangles, mem: renderer.info.memory, scene: scene.children.length }))()"""

# ---- parts ---------------------------------------------------------------------------------------------------------
def scenario(r, tag):
    """The same short play for every mode: frames, a quarter turn, taps on the deck, a held finger, the device."""
    out = {}; shots = []
    r.ev("SHIP.device && SHIP.device.settings && (SHIP.device.settings.tips = false)")
    def snap(name):
        shots.append((name, r.shot(f'{tag}_{name}')))
        out[name] = {'game': r.ev(GAME_STATE), 'page': r.js(PAGE_STATE), 'toast': [r.page.inner_text('#tt'), r.page.inner_text('#tx'), r.page.inner_text('#room')]}
    r.step(40); snap('a_start')
    r.step(240); snap('b_wander')
    r.page.click('#rot'); r.step(40); snap('c_rotated')
    for k, (x, y) in enumerate([(450, 380), (700, 300), (300, 520)]):
        r.page.mouse.move(x, y); r.page.mouse.down(); r.page.mouse.up(); r.step(120); snap(f'd_tap{k}')
    r.ev("player.steer = { x: .8, z: .6, k: 1 }"); r.step(90); r.ev("player.steer = null"); r.step(10); snap('e_steer')
    r.page.click('#devBtn'); r.step(30); snap('f_device')
    r.page.click('#devClose'); r.step(30); snap('g_closed')
    out['errors'] = r.errors[:5]
    return out, shots

def same_pics(sa, sb):
    """max pixel difference and count over two lists of (name, path); the renderer's 1-level noise allowed (cadet_test)"""
    from PIL import Image
    import numpy as np
    bad = []
    for (n, pa), (_, pb) in zip(sa, sb):
        A = np.array(Image.open(pa).convert('RGB')).astype(int); B = np.array(Image.open(pb).convert('RGB')).astype(int)
        d = np.abs(A - B).max(axis=2)
        if d.max() > 1: bad.append(f'{n}: {int((d > 1).sum())} px differ (max {int(d.max())})')
    return bad

def diff_state(a, b, path=''):
    if json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True): return []
    if isinstance(a, dict) and isinstance(b, dict):
        out = []
        for k in sorted(set(a) | set(b)): out += diff_state(a.get(k), b.get(k), path + '.' + str(k))
        return out
    return [f'{path}: {str(a)[:90]} -> {str(b)[:90]}']

IDLE_MODES = [('none', 'no pad again (the check is steady)', None), ('api', 'the pad API with no pad', None), ('hidden', 'a drifting pad the browser keeps hidden until a press (mode a), never pressed', {'hidden': True, 'drift': True}), ('idle', 'a pad there at load (mode b), never pressed', {}), ('drift', 'a drifting pad there at load (mode b), never pressed', {'drift': True})]
def part_idle(br, src, tag):
    """FAIL lines for: every idle mode (and PAD_ON on, if there is a switch) against the game with no pad."""
    fails = []
    builds = both_builds(src); sw = pad_switch(src)
    print(f'  PAD_ON: {"no switch in this build" if sw is None else ("on" if sw else "off")}')
    r = Run(br, builds[0][1], f'{tag}_base'); base, bshots = scenario(r, f'{tag}_base'); r.close()
    for bname, bsrc in builds:
        for mode, what, plug in IDLE_MODES if bname == 'off' else [('none', 'no pad', None)] + IDLE_MODES[1:]:
            r = Run(br, bsrc, f'{tag}_{bname}_{mode}', mode=mode, plug=plug)
            got, gshots = scenario(r, f'{tag}_{bname}_{mode}')
            reads = r.js('window.__pads ? window.__pads.reads : 0'); r.close()
            d = diff_state(base, got) + same_pics(bshots, gshots)
            label = f'PAD_ON {bname}, {what}'
            print(f'  {label}: {"identical" if not d else str(len(d)) + " differences"} (the game read the pads {reads} times)')
            fails += [f'{label}: {x}' for x in d[:6]]
    return fails

def save_text(br, src, tag, mode, plug, frames=200):
    # a real save (no ?nosave), the arrival marked done so the intro doesn't start
    r = Run(br, src, tag, mode=mode, plug=plug, query='?debug', storage={'starship-cadet-arrived': '1'})
    # the whole of storage, not only the save: a controller's own key would be a change to what's kept too
    r.step(frames); txt = r.ev("saveGame(), JSON.stringify(Object.fromEntries(Object.keys(localStorage).sort().map(k => [k, k === SAVE_KEY ? JSON.parse(localStorage.getItem(k)) : localStorage.getItem(k)])))"); r.close()
    return txt
def both_builds(src):
    # the file as given with its switch off, and a copy with it on; a build with no switch is tested as it is
    if pad_switch(src) is None: return [('as given', src)]
    return [('off', with_switch(src, False)), ('on', with_switch(src, True))]
def part_save(br, src, tag):
    fails = []
    builds = both_builds(src)
    base = save_text(br, builds[0][1], f'{tag}_save_none', 'none', None)
    print(f'  storage with no pad (the save and everything else kept): {len(base or "")} bytes')
    if not base: return ['no save was written with no pad']
    for bname, bsrc in builds:
        for mode, what, plug in ([] if bname != 'on' else [('none', 'no pad', None)]) + IDLE_MODES[1:]:
            t = save_text(br, bsrc, f'{tag}_save_{bname}_{mode}', mode, plug)
            same = t == base
            print(f'  PAD_ON {bname}, {what}: {"byte-identical" if same else "DIFFERENT"} ({len(t or "")} bytes)')
            if not same:
                a, b = json.loads(base), json.loads(t or '{}')
                fails.append(f'PAD_ON {bname}, {what}: storage differs: ' + '; '.join(diff_state(a, b)[:4]))
    return fails

def part_calls(br, src, tag):
    fails = []
    for (name, w, h) in [('phone', 390, 844), ('wide', 1280, 800)]:
        got = {}
        on = both_builds(src)[-1][1]   # the switch on (the off build is idle's)
        for mode, plug in [('none', None), ('hidden', {'hidden': True, 'drift': True}), ('idle', {}), ('drift', {'drift': True})]:
            r = Run(br, on, f'{tag}_calls_{name}_{mode}', mode=mode, plug=plug, w=w, h=h)
            r.step(60); g = r.ev(GAME_STATE); r.close()
            got[mode] = [g['calls'], g['tris'], g['mem']['geometries'], g['mem']['textures'], g['scene']]
        print(f'  {name} {w}x{h}: draw calls, triangles, geometries, textures, scene objects: ' + ', '.join(f'{m} {v}' for m, v in got.items()))
        for m in ('hidden', 'idle', 'drift'):
            if got[m] != got['none']: fails.append(f'{name}: {m} pad {got[m]} vs no pad {got["none"]}')
        if got['none'][0] >= 450: fails.append(f'{name}: {got["none"][0]} draw calls, the budget is 450')
    return fails

# ---- the reachability sweep: what the page itself says can be pressed -----------------------------------------------
# A clickable: a button, link, input, select, textarea or summary; anything with a pressable role or its own tabindex; an
# element with onclick or a click listener; or a leaf (nothing pressable inside) with pointer/touch/mouse listeners and a
# hand cursor; or the top of a hand-cursor area. It must be visible, on screen, not disabled, and really under a finger
# at its middle (or a corner), so a card covered by a dialog doesn't count. The canvas (the deck) is the pick part's.
SCAN = r"""(() => {
  const T = window.__census.tagged, out = [], seen = new Map();
  const ROLES = /^(button|link|tab|menuitem|menuitemradio|menuitemcheckbox|option|checkbox|switch|radio|slider|spinbutton|combobox)$/;
  const kind = e => {
    const t = e.tagName; if (t === 'CANVAS') return 0;
    if (t === 'BUTTON' || t === 'SELECT' || t === 'TEXTAREA' || t === 'SUMMARY' || (t === 'A' && e.hasAttribute('href')) || (t === 'INPUT' && e.type !== 'hidden')) return 1;
    const r = e.getAttribute('role'); if (r && ROLES.test(r)) return 1;
    if (e.hasAttribute('tabindex') && e.tabIndex >= 0) return 1;
    const ty = T.get(e);
    if (e.onclick || (ty && (ty.has('click') || ty.has('dblclick')))) return 2;
    if ((ty && [...ty].some(x => x !== 'keydown')) || e.onpointerdown || e.onpointerup || e.ontouchstart || e.onmousedown) return 3;
    const cs = getComputedStyle(e); if (cs.cursor === 'pointer' && (!e.parentElement || getComputedStyle(e.parentElement).cursor !== 'pointer')) return 4;
    return 0;
  };
  const vis = e => {
    if (e.closest('[hidden]') || (e.disabled === true) || e.getAttribute('aria-disabled') === 'true') return null;
    if (e.checkVisibility && !e.checkVisibility({ opacityProperty: true, visibilityProperty: true })) return null;
    const b = e.getBoundingClientRect(); if (b.width < 2 || b.height < 2) return null;
    const x0 = Math.max(0, b.left), x1 = Math.min(innerWidth, b.right), y0 = Math.max(0, b.top), y1 = Math.min(innerHeight, b.bottom);
    if (x1 - x0 < 2 || y1 - y0 < 2) return null;
    for (const [fx, fy] of [[.5, .5], [.2, .3], [.8, .3], [.2, .7], [.8, .7]]) {
      const x = x0 + (x1 - x0) * fx, y = y0 + (y1 - y0) * fy, h = document.elementFromPoint(x, y);
      if (h && (h === e || e.contains(h) || (h.control && h.control === e))) return [Math.round(x), Math.round(y)];
    }
    return null;
  };
  const all = [...document.body.querySelectorAll('*')], cand = new Map();
  for (const e of all) { const k = kind(e); if (k) cand.set(e, k); }
  for (const [e, k] of cand) {
    // a listener-only or hand-cursor element with pressable things inside is a container (taps on its buttons), not one
    if (k >= 3 && [...cand.keys()].some(o => o !== e && e.contains(o))) continue;
    if (k === 4 && [...cand.keys()].some(o => o !== e && o.contains(e))) continue;
    const at = vis(e); if (!at) continue;
    let a = e, path = ''; while (a && a !== document.body && !a.id) { a = a.parentElement; }
    const own = (e.getAttribute('aria-label') || e.textContent || e.value || e.title || '').replace(/\s+/g, ' ').trim().slice(0, 40), lab = own.replace(/\d+/g, 'N');   // no digits in keys: a clock or a count isn't a new thing
    let key = e.id ? '#' + e.id : (a && a.id ? '#' + a.id + ' ' : '') + e.tagName.toLowerCase() + (e.className && typeof e.className === 'string' ? '.' + e.className.trim().split(/\s+/)[0] : '') + '[' + lab + ']';
    const n = (seen.get(key) || 0) + 1; seen.set(key, n); if (n > 1) key += '#' + n;
    const d = e.closest('[role=dialog],[aria-modal=true],.lift,.device,dialog');
    const f = document.activeElement, lc = window.__census.lastClick;
    out.push({ k: key, x: at[0], y: at[1], why: ['', 'tag', 'click', 'listener', 'cursor'][k], dlg: d ? (d.id || d.className) : null, label: own,
      foc: !!f && f !== document.body && (f === e || e.contains(f)), clicked: !!lc && (lc === e || e.contains(lc)) });
  }
  const dlg = [...document.querySelectorAll('[role=dialog],[aria-modal=true],.lift,.device,dialog')].filter(e => !e.closest('[hidden]') && e.getBoundingClientRect().width > 0 && (!e.checkVisibility || e.checkVisibility({ opacityProperty: true, visibilityProperty: true }))).map(e => e.id || e.className);
  return { items: out, dialogs: dlg, url: location.href, deck: typeof player !== 'undefined' ? player.deck : null };
})()"""

# The deck's own tappable things, read from what section 11's tap() reads: the items (ITEMS, each with its hit mesh), the
# crew (DECK_CREW, tapCrew), the lift doors and the closed doors. One of each name (the same kind of thing opens the same
# kind of panel). Then a tap on one: stand beside it, tap where it is on screen, and let the game run until it settles.
# Panel candidates in the page as loaded: hidden children of body (hidden, or display none) that are dialogs or hold
# something pressable or a heading. Each must be seen open in the sweep, or be on NOT_FROM_NEW_GAME with a reason.
CANDS = r"""(() => [...document.body.children].filter(e => (e.hidden || getComputedStyle(e).display === 'none') && e.id &&
  (e.matches('[role=dialog],[aria-modal=true],dialog') || e.querySelector('button,input,select,textarea,a[href],[role=button],h1,h2,h3'))).map(e => e.id))()"""
OPEN_NOW = r"""((ids) => ids.filter(id => { const e = document.getElementById(id); if (!e || e.hidden) return false; const b = e.getBoundingClientRect();
  return b.width > 0 && b.height > 0 && getComputedStyle(e).display !== 'none' && getComputedStyle(e).visibility !== 'hidden'; }))"""
NOT_FROM_NEW_GAME = {}   # id: the reason it can't open in a new game at a test URL (filled as the sweep finds them, each with a reason)
DECK_TARGETS = r"""(() => { const out = [], seen = new Set(), v = new THREE.Vector3();
  const add = (name, x, y, z) => { if (seen.has(name)) return; seen.add(name); out.push({ name, x, y, z }); };
  for (const it of ITEMS) { if (!it.hit) continue; it.hit.getWorldPosition(v); add('item:' + it.t, v.x, v.y, v.z); }
  if (typeof DECK_CREW !== 'undefined') for (const a of DECK_CREW) { if (a.x !== undefined) { add('crew', a.x, 1.1, a.z); break; } }
  for (const d of DOOR_OBJS) if (d.e.type === 'lift') { add('lift door', d.e.cx, 1, d.e.cz); break; }
  for (const k in (typeof CLOSED_DOORS !== 'undefined' ? CLOSED_DOORS : {})) { const e = EDGES.get(k); if (e) add('closed door:' + (CLOSED_DOORS[k].t || k), e.cx, 1, e.cz); }
  return out; })()"""
TAP_TARGET = r"""((t) => { const c = nearestOpen(t.x, t.z, player); if (!c) return null; player.stop(); player.steer = null;
  player.obj.position.copy(cellPos(...c)); target.copy(player.obj.position).setY(.7); return true; })"""
WHERE = r"""((t) => { let x = t.x, z = t.z; if (t.name === 'crew' && typeof DECK_CREW !== 'undefined') { const a = DECK_CREW.find(a => a.x !== undefined); if (a) { x = a.x; z = a.z; } }
  const v = new THREE.Vector3(x, t.y, z).project(camera); return [(v.x + 1) / 2 * innerWidth, (1 - v.y) / 2 * innerHeight, Math.abs(v.x) < .95 && Math.abs(v.y) < .95]; })"""

class Sweep:
    """The touch half of the reachability sweep: from the deck and from every panel it can open, press every clickable
    by mouse (a real click at its middle, as a finger would) and record each screen state reached: the pressable things
    in it, read from the page. Back to the state before with Escape, else by reloading and replaying the presses."""
    MAX_DEPTH, MAX_PRESSES = 6, int(os.environ.get('CTL_PRESSES', 700))
    SKIP = {'#newgame'}   # pressed once at the top only (twice starts a new game; nothing new to find behind it)
    def __init__(self, pw, src, tag):
        self.pw, self.src, self.tag = pw, src, tag
        self.states = {}          # signature -> {'path': [...], 'items': [...], 'dialogs': [...]}
        self.pressed = set(); self.presses = 0; self.reloads = 0; self.lost = []; self.capped = set(); self.tapped = set()
        self.cands = None; self.opened = set(); self.seen_keys = set(); self.groups = {}
        self.r = None
    def load(self):
        try:
            if self.r: self.r.reload()
            else: self.r = Run(self.pw, self.src, f'{self.tag}_sweep')
        except Exception:   # a reload that hangs on a busy machine: a fresh browser instead
            try: self.r.close()
            except Exception: pass
            self.r = Run(self.pw, self.src, f'{self.tag}_sweep')
        self.r.ev("SHIP.device && SHIP.device.settings && (SHIP.device.settings.tips = false)"); self.r.step(20); self.reloads += 1
    def scan(self):
        sc = self.r.ev(SCAN)
        if self.cands is None: self.cands = self.r.ev(CANDS)
        self.opened |= set(self.r.ev(f"({OPEN_NOW})({json.dumps(self.cands)})"))
        return sc
    BACK = re.compile(r'^(back|close|stay here|not yet|cancel|done|leave|no|×|✕|x)$', re.I)
    @staticmethod
    def inner(sc):
        # with a panel open, its own things; the screen's edge buttons are pressed from the deck only
        return [i for i in sc['items'] if i['dlg']] if sc['dialogs'] else sc['items']
    # a panel's own fixed keys (the device's Back, Home and Close) are pressed like the rest but don't make a screen new:
    # Back comes and goes with the app, so home after an app would look like another screen
    FIXED = {'#devBack', '#devHome', '#devClose'}
    @classmethod
    def sig(cls, sc): return (sc.get('deck'), tuple(sorted(sc['dialogs'])), tuple(sorted(i['k'] for i in cls.inner(sc) if i['k'] not in cls.FIXED)))
    def deck_tap(self, key):
        name = key[len('@tap:'):]
        t = next((t for t in self.r.ev(DECK_TARGETS) if t['name'] == name), None)
        if not t or not self.r.ev(f"({TAP_TARGET})({json.dumps(t)})"): return False
        self.r.step(6); x, y, on = self.r.ev(f"({WHERE})({json.dumps(t)})")
        if not on: return False
        self.r.page.mouse.click(x, y); self.presses += 1
        for _ in range(15):   # up to 5 s of game: a walk to it, then whatever it opens
            self.r.step(10)
            if self.r.ev(SCAN)['dialogs']: break
        return True
    def press(self, sc, key):
        if key.startswith('@deck:'): self.r.ev(f"goToDeck({int(key[6:])})"); self.r.step(40); return True
        if key.startswith('@tap:'): return self.deck_tap(key)
        it = next((i for i in sc['items'] if i['k'] == key), None)
        if not it: return False
        self.r.page.mouse.click(it['x'], it['y']); self.r.step(8); self.presses += 1
        return True
    def replay(self, path):
        self.load()
        for k in path:
            if not self.press(self.scan(), k): return False
        return True
    def back_to(self, path, sig, need=()):
        # Escape, else load again and replay the presses; a screen that comes back a little different (the device
        # reopens on the app last used) is taken as it is, and the presses left are made from there
        here = lambda sc: self.sig(sc) == sig or (need and tuple(sorted(sc['dialogs'])) == sig[1] and sc.get('deck') == sig[0] and set(need) <= {i['k'] for i in self.inner(sc)})
        # the panel's own Back first (Escape closes the whole device), then Escape
        for _ in range(4):
            sc = self.scan()
            if here(sc): return True
            b = next((i for i in self.inner(sc) if self.BACK.match(i['label'])), None)
            if b and b['k'] != '#devClose': self.press(sc, b['k'])
            else: self.r.page.keyboard.press('Escape'); self.r.step(4)
        if here(self.scan()): return True
        if self.replay(path) and here(self.scan()): return True
        self.lost.append(' > '.join(path) or '(the deck)'); return True
    def crawl(self, path=(), depth=0):
        # coverage, not screens: a screen is explored only if it shows something pressable not seen before, and each
        # pressable thing is pressed once in the whole sweep (a game's screens change with what you did, endlessly)
        sc = self.scan(); sg = self.sig(sc)
        fresh = [i['k'] for i in self.inner(sc) if i['k'] not in self.seen_keys]
        if sg in self.states or (path and not fresh and not path[-1].startswith('@deck:')): return
        self.seen_keys.update(i['k'] for i in self.inner(sc))
        self.states[sg] = {'path': list(path), 'items': self.inner(sc), 'dialogs': sc['dialogs']}
        print(f'    state {len(self.states)}: {" > ".join(path) or "(the deck)"}: {len(self.inner(sc))} things, {self.presses} presses, {self.reloads} loads', flush=True)
        if depth >= self.MAX_DEPTH:
            if self.inner(sc): self.capped.add(f'depth {self.MAX_DEPTH} reached at {" > ".join(path)}')
            return
        todo = list(self.inner(sc))
        if not sc['dialogs'] and all(not k.startswith('@tap:') for k in path):
            # on a deck: its tappable things too (each name once in the whole sweep), then the other decks
            for t in self.r.ev(DECK_TARGETS):
                if t['name'] not in self.tapped: self.tapped.add(t['name']); todo.append({'k': '@tap:' + t['name']})
            if not path:
                for n in self.r.ev("(typeof DECK_ORDER !== \"undefined\" ? DECK_ORDER : Object.keys(DECKS).map(Number)).filter(n => n !== player.deck)"):
                    todo.append({'k': f'@deck:{n}'})
        for it in todo:
            if self.presses >= self.MAX_PRESSES: self.capped.add(f'{self.MAX_PRESSES} presses reached'); return
            if it['k'] in self.pressed or (it['k'] in self.SKIP and path): continue
            # of a big set of alike things (20 or more on one screen with the same container and class: Tiles' 36
            # squares) two are pressed; every one of them is still listed, and the pad half must reach every one
            grp = re.sub(r'\[.*\](#\d+)?$', '', it['k'])
            big = sum(1 for i in todo if re.sub(r'\[.*\](#\d+)?$', '', i['k']) == grp) >= 20   # a board or a long list, not the device's apps
            if not it['k'].startswith('@') and grp != it['k'] and big and self.groups.get(grp, 0) >= 2: continue
            # alike things with the same label (the key's #2, #3...: a map's pins, each "N" once digits are hidden): two
            # pressed in the whole sweep; each one pressed went a level deeper into the same screens (0.90.5's run)
            same = re.sub(r'#\d+$', '', it['k'])
            if not it['k'].startswith('@') and self.groups.get('=' + same, 0) >= 2: continue
            self.groups[grp] = self.groups.get(grp, 0) + 1; self.groups['=' + same] = self.groups.get('=' + same, 0) + 1
            self.pressed.add(it['k'])
            cur = self.scan(); need = [it['k']] if not it['k'].startswith('@') else []
            if need and it['k'] not in {i['k'] for i in self.inner(cur)}: self.back_to(list(path), sg, need)
            elif not need and (cur['dialogs'] or cur.get('deck') != sg[0]): self.back_to(list(path), sg)   # deck taps from the bare deck
            if not self.press(self.scan(), it['k']): continue
            after = self.scan()
            if after['url'] != sc['url']: self.lost.append('left the page: ' + it['k']); self.replay(list(path)); continue
            if self.sig(after) != sg or it['k'].startswith('@deck:'):
                self.crawl(tuple(path) + (it['k'],), depth + 1)
                left = [i['k'] for i in todo if i['k'] not in self.pressed and not i['k'].startswith('@')]
                self.back_to(list(path), sg, left[:1])
    def run(self):
        self.load(); self.crawl()
        if self.r: self.r.close()
        return self

def part_reach(pw, src, tag):
    sw = Sweep(pw, src, tag).run()
    keys = sorted({i['k'] for st in sw.states.values() for i in st['items']})
    dl = sorted({d for st in sw.states.values() for d in st['dialogs']})
    print(f'  by touch: {len(sw.states)} screen states, {len(keys)} different pressable things, {sw.presses} presses, {sw.reloads} loads; panels seen: {", ".join(dl)}')
    if sw.capped: print(f'  INCOMPLETE: {"; ".join(sorted(sw.capped))}')
    if sw.lost: print(f'  could not get back from: {"; ".join(sw.lost[:6])}')
    for st in list(sw.states.values())[:200]:
        print(f'    {" > ".join(st["path"]) or "(the deck)"}: {len(st["items"])} things' + (f' in {", ".join(st["dialogs"])}' if st['dialogs'] else ''))
    REACH_INVENTORY.update(states=sw.states, keys=keys)
    fails = []
    never = [c for c in (sw.cands or []) if c not in sw.opened and c not in NOT_FROM_NEW_GAME]
    print(f'  panels in the page as loaded: {len(sw.cands or [])}; seen open: {", ".join(sorted(sw.opened)) or "none"}')
    for c in sorted(NOT_FROM_NEW_GAME): print(f'  not from a new game: #{c} ({NOT_FROM_NEW_GAME[c]})')
    fails += [f'the panel #{c} (hidden at load) was never seen open in the sweep' for c in never]
    fails += [f'the sweep stopped early: {c}' for c in sorted(sw.capped)]
    if 'panels' in built and '--inventory' not in FLAGS: fails += part_reach_pad(pw, src, tag, sw.states)
    return fails
REACH_INVENTORY = {}

# ---- the pad half (panels): every thing on every screen the touch half found, reached and pressed by pad --------------
# For each screen with a panel open: get there by the touch half's own presses, then move the highlight (the page's real
# focus, plan section 3) with the D-pad only: back and forth along rows, down and up, and a seeded wander, until nothing
# new is reached. Every thing the page lists on that screen must have had the highlight. Then A on the highlighted thing
# must click that very thing, and B must leave the panel (or go back a step).
def pad_moves(r, n):
    seen, order = set(), []
    def look():
        sc = r.ev(SCAN); it = next((i for i in Sweep.inner(sc) if i['foc']), None); f = it and it['k']
        if f and f not in seen:
            seen.add(f); order.append(f)
            # CP5's rule: what the highlight lands on has a name a screen reader reads (text, aria-label or title)
            if not r.js("(() => { const e = document.activeElement; return !!((e.getAttribute('aria-label') || e.textContent || e.title || (e.labels && e.labels[0] && e.labels[0].textContent) || '').trim()); })()"): pad_moves.nameless.add(f)
        return f
    r.press('DOWN'); r.step(1); look()
    for d1, d2 in (('RIGHT', 'LEFT'), ('LEFT', 'RIGHT')):
        for row in range(n):
            for d in (d1, d2):
                last = None
                for k in range(n):
                    r.press(d); r.step(1); f = look()
                    if f == last: break
                    last = f
            r.press('DOWN' if d1 == 'RIGHT' else 'UP'); r.step(1); look()
    x = 7
    for k in range(4 * n):
        x = (x * 48271) % 2147483647; r.press(['UP', 'DOWN', 'LEFT', 'RIGHT'][x % 4]); r.step(1); look()
    return seen, order
pad_moves.nameless = set()
def part_reach_pad(pw, src, tag, states):
    fails = []; pad_moves.nameless = set()
    for st in states.values():
        if not st['dialogs'] or any(k.startswith('@deck:') for k in st['path']): continue
        sw = Sweep(pw, src, f'{tag}_pad'); sw.r = Run(pw, src, f'{tag}_padsweep', mode='pad', plug={}); sw.r.ev("SHIP.device && SHIP.device.settings && (SHIP.device.settings.tips = false)"); sw.r.step(20)
        okp = all(sw.press(sw.scan(), k) for k in st['path'])
        where = ' > '.join(st['path'])
        if not okp: print(f'  {where}: could not get there again'); sw.r.close(); continue
        want = {i['k'] for i in st['items']}
        seen, order = pad_moves(sw.r, min(12, len(want) + 2))
        now = {i['k'] for i in Sweep.inner(sw.scan())}
        missing = sorted((want & now) - seen)
        print(f'  {where}: {len(seen & want & now)} of {len(want & now)} things highlighted by the D-pad' + (f'; never: {missing[:5]}' if missing else ''))
        if missing: fails.append(f'{where}: the D-pad never reaches {len(missing)}: {missing[:5]}')
        if pad_moves.nameless: fails.append(f'{where}: highlighted with no readable name: {sorted(pad_moves.nameless)[:5]}'); pad_moves.nameless = set()
        # A clicks the highlighted thing
        sc = sw.scan(); f = next((i for i in Sweep.inner(sc) if i['foc']), None)
        if f and not Sweep.BACK.match(f['label']):
            sw.r.js("window.__census.lastClick = null; window.__f = document.activeElement")
            sw.r.press('A'); sw.r.step(4)
            hit = sw.r.js("(() => { const c = window.__census.lastClick, f = window.__f; return !c ? 'nothing' : (c === f || f.contains(c)) ? 'it' : (c.id || c.tagName); })()")
            if hit != 'it': fails.append(f'{where}: A on the highlighted {f["k"]} clicked {hit}, not it')
        # B leaves the panel or goes back
        sig0 = Sweep.sig(sw.scan())
        sw.r.press('B'); sw.r.step(6); sc3 = sw.scan()
        if Sweep.sig(sc3) == sig0: fails.append(f'{where}: B changed nothing (the panel stays as it was)')
        sw.r.close()
    return fails

# ---- on the deck: walking, turning, zooming, Pause, Device, Tracked (the deck package) --------------------------------
OPEN_CELL = r"""(() => { let best = null;
  for (let j = 2; j < D - 2; j++) for (let i = 2; i < W - 2; i++) { if (!free(i, j)) continue; const room = roomAt(i, j); let n = 0;
    for (let dj = -2; dj <= 2; dj++) for (let di = -2; di <= 2; di++) if (free(i + di, j + dj) && roomAt(i + di, j + dj) === room) n++;
    if (!best || n > best[2]) best = [i, j, n]; }
  return best; })()"""
PUT = "(([i, j]) => { player.obj.position.copy(cellPos(i, j)); player.stop(); player.steer = null; })"
SCREEN = r"""(() => { const v = player.obj.position.clone().project(camera); return [v.x * innerWidth / 2, -v.y * innerHeight / 2, player.obj.position.x, player.obj.position.z]; })"""
def screen_delta(r, w0, w1):
    # both world points through today's camera: the screen move, whatever the camera did meanwhile
    return r.ev(f"(() => {{ const a = new THREE.Vector3({w0[0]}, 0, {w0[1]}).project(camera), b = new THREE.Vector3({w1[0]}, 0, {w1[1]}).project(camera); return [(b.x - a.x) * innerWidth / 2, -(b.y - a.y) * innerHeight / 2]; }})()")
def in_use(r, i=0):
    # the pad in use before a walk is measured: since CP4's first use (0.90.8), a stick push on a pad not in use (none
    # yet, or touch took over: the check's own click on the turn button) counts only after 0.15 s held, by design; a
    # press of B counts at once (on the deck it only puts a message away)
    if not r.ev("typeof PAD === 'object' && PAD.used && PAD.idx === " + str(i)): r.press('B', i=i); r.step(2)
def part_walk(pw, src, tag):
    import math
    fails = []
    r = Run(pw, src, f'{tag}_walk', mode='pad', plug={})
    r.step(10)
    cell = r.ev(OPEN_CELL); print(f'  an open spot: tile {cell[:2]} ({cell[2]} of 25 tiles around it open)')
    for rot in range(4):
        az0 = r.ev("azT")
        for name, (sx, sy) in [('up', (0, -1)), ('right', (1, 0)), ('down', (0, 1)), ('left', (-1, 0))]:
            r.ev(f"({PUT})({json.dumps(cell[:2])})"); r.step(3); in_use(r)
            p0 = r.ev(f"({SCREEN})()")
            r.pad(12, a={0: sx, 1: sy}, release=False)
            p1 = r.ev(f"({SCREEN})()")
            r.js('window.__pads.clear(0)'); r.step(2); p2 = r.ev(f"({SCREEN})()"); r.step(6); p3 = r.ev(f"({SCREEN})()")
            dx, dy = screen_delta(r, p0[2:], p1[2:]); moved = math.hypot(dx, dy)
            err = abs((math.degrees(math.atan2(dy, dx) - math.atan2(sy, sx)) + 180) % 360 - 180) if moved > 0 else 180
            drift = math.hypot(p3[2] - p2[2], p3[3] - p2[3])
            if moved < 15 or err > 30: fails.append(f'view {rot}: stick {name}: walked {moved:.0f} px at {err:.0f} degrees off (want 15+ px within 30)')
            if drift > .01: fails.append(f'view {rot}: stick {name}: still moving {drift:.3f} m after letting go')
        print(f'  view {rot} (az {az0:.2f}): four directions walked')
        r.page.click('#rot'); r.step(30)
    # faster the further you push
    sp = []
    for k in (.5, 1):
        r.ev(f"({PUT})({json.dumps(cell[:2])})"); r.step(3); in_use(r); p0 = r.ev(f"({SCREEN})()")
        r.pad(10, a={0: k}); p1 = r.ev(f"({SCREEN})()"); sp.append(math.hypot(p1[2] - p0[2], p1[3] - p0[3]))
    print(f'  half a push walks {sp[0]:.2f} m, a full push {sp[1]:.2f} m')
    if not (sp[1] > sp[0] * 1.2 and sp[0] > 0): fails.append(f'a full push should walk faster than half a push ({sp[0]:.2f} vs {sp[1]:.2f} m)')
    # turning: LB and RB a quarter turn each way; the right stick, one quarter turn a push however long it's held
    q = math.pi / 2
    for b in ('LB', 'RB'):
        a0 = r.ev("azT"); r.press(b); r.step(20); a1 = r.ev("azT")
        if abs(abs(a1 - a0) - q) > 1e-6: fails.append(f'{b} turned the view {a1 - a0:.3f}, want a quarter turn ({q:.3f})')
        turn = a1 - a0
        if b == 'LB': lb = turn
        else:
            if lb * turn >= 0: fails.append(f'LB and RB turned the same way ({lb:.3f}, {turn:.3f})')
    for sx in (1, -1):
        a0 = r.ev("azT"); r.pad(30, a={2: sx}); r.step(20); a1 = r.ev("azT")
        if abs(abs(a1 - a0) - q) > 1e-6: fails.append(f'right stick {"right" if sx > 0 else "left"} held: turned {a1 - a0:.3f}, want one quarter turn')
    # zooming: the triggers and the right stick, within pinch's limits; a light squeeze slower; the right stick click back to normal
    zmin, zmax, z0 = r.ev("[ZOOM_MIN, ZOOM_MAX, camera.zoom]")
    r.pad(120, {'RT': 1}); zin = r.ev("camera.zoom"); r.pad(160, {'LT': 1}); zout = r.ev("camera.zoom")
    print(f'  zoom: normal {z0:.2f}, RT held {zin:.3f} (limit {zmax}), LT held {zout:.3f} (limit {zmin})')
    if abs(zin - zmax) > 1e-6: fails.append(f'RT held should zoom in to the limit {zmax}: {zin}')
    if abs(zout - zmin) > 1e-6: fails.append(f'LT held should zoom out to the limit {zmin}: {zout}')
    r.press('RS'); r.step(10); zb = r.ev("camera.zoom")
    if abs(zb - z0) > 1e-3: fails.append(f'the right stick click should go back to the usual zoom {z0:.3f}: {zb:.3f}')
    d = []
    for v in (.3, 1):
        r.press('RS'); r.step(5); a = r.ev("camera.zoom"); r.pad(8, {'RT': v}); d.append(r.ev("camera.zoom") - a)
    if not (0 < d[0] < d[1]): fails.append(f'a light squeeze should zoom in more slowly than a full one ({d[0]:.3f}, {d[1]:.3f})')
    r.press('RS'); r.step(5); a = r.ev("camera.zoom"); r.pad(15, a={3: -1}); up = r.ev("camera.zoom") - a
    r.press('RS'); r.step(5); a = r.ev("camera.zoom"); r.pad(15, a={3: 1}); dn = r.ev("camera.zoom") - a
    if not (up * dn < 0): fails.append(f'the right stick up and down should zoom opposite ways ({up:.3f}, {dn:.3f})')
    r.press('RS'); r.step(5)
    # Pause (Menu), your device (Y), Tracked (View): each opens and the same button closes it
    for b, what, js in [('MENU', 'Pause', 'PAUSE.on'), ('Y', 'your device', 'DEV.open'), ('VIEW', 'Tracked', '!document.getElementById("trkPanel").hidden')]:
        r.press(b); r.step(10); on = r.ev(js)
        if on and b != 'MENU':
            # with a panel open the deck takes nothing: the stick doesn't walk you, RB doesn't turn the view
            a = r.ev(f"({SCREEN})()"); a0 = r.ev("azT"); r.pad(20, a={0: 1}); r.press('RB'); r.step(5); c = r.ev(f"({SCREEN})()")
            if abs(a[2] - c[2]) + abs(a[3] - c[3]) > 1e-3 or r.ev("azT") != a0: fails.append(f'with {what} open, the stick walked or RB turned the view')
        t0 = r.ev("SHIP.time.min"); r.step(60); t1 = r.ev("SHIP.time.min")
        r.press(b); r.step(10); off = r.ev(js)
        if not on or off: fails.append(f'{b} should open {what} and close it again (open {on}, after the second press {off})')
        if b == 'MENU' and on and t1 != t0: fails.append(f'the ship clock ran while paused ({t0} -> {t1})')
    if r.errors: fails.append('page errors: ' + ' | '.join(r.errors[:3]))
    r.close()
    return fails

# planted faults in the input itself (the same for every build: navigator.getGamepads wrapped inside the game's copy),
# so they need nothing from section 26's insides
def WRAP(body):
    return ("(() => { const real = Navigator.prototype.getGamepads; let mem = null, n = 0;\n"
            "  Object.defineProperty(Navigator.prototype, 'getGamepads', { configurable: true, value: function () { return [...real.call(this)].map(p => { if (!p) return p;\n"
            "    const axes = [...p.axes], buttons = p.buttons.map(b => ({ pressed: b.pressed, touched: b.touched, value: b.value })); " + body + "\n"
            "    return { ...p, id: p.id, index: p.index, mapping: p.mapping, connected: p.connected, timestamp: p.timestamp, axes, buttons }; }); } }); })();\n")
# ---- touch after pad (base): press, then tap: the no-pad picture, no focus outline left -----------------------------
OUTLINES = r"""(() => { const out = []; for (const e of document.querySelectorAll('*')) { const cs = getComputedStyle(e);
  if (cs.outlineStyle !== 'none' && parseFloat(cs.outlineWidth) > 0 && e.getBoundingClientRect().width > 0) out.push((e.id || e.tagName) + ' ' + cs.outlineWidth); }
  const a = document.activeElement; return { outlines: out.slice(0, 5), focus: a && a !== document.body ? (a.id || a.tagName) : null }; })()"""
# what you can see: the rendered elements (hash of tag, id, classes, inline style, text), the body's classes, the 3D
# objects drawn. Things made on the pad's first use and hidden again after a touch (the ring, the bottom line) are listed
# apart, as information: the rule is that touch looks and behaves as without a pad, not that nothing is ever made.
SEEN_STATE = r"""(() => { let h = 0, n = 0; const mix = s => { for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) | 0; };
  // (the message box shows and hides on real-time timers, and P3's one-time "Controller connected" after the first pad
  // press is by design: the box and its lines are counted, but their text and classes are not compared)
  const box = document.getElementById('toast');
  for (const e of document.body.querySelectorAll('*')) { if (e.tagName === 'SCRIPT' || e.tagName === 'STYLE') continue;
    if (box && (e === box || box.contains(e))) { n++; mix('toast-box'); continue; }
    if (e.checkVisibility && !e.checkVisibility({ visibilityProperty: true })) continue;   // not opacity: the bubbles are hidden from pictures that way
    const b = e.getBoundingClientRect(); if (b.width <= 0 || b.height <= 0) continue;
    n++; mix(e.tagName + '|' + e.id + '|' + e.className + '|' + (e.getAttribute('style') || '')); for (const c of e.childNodes) if (c.nodeType === 3) mix(c.textContent); }
  let drawn = 0; scene.traverseVisible(o => { if (o.isMesh || o.isLine || o.isPoints || o.isSprite) drawn++; });
  return { seen: n, seenHash: h, body: document.body.className, drawn, all: document.querySelectorAll('*').length, scene: scene.children.length }; })()"""
PRE = 40   # frames before the first tap, the same in every run (each press is 3 frames and 4 after it)
def touch_play(pw, src, tag, mode, presses):
    r = Run(pw, src, tag, mode=mode, plug={} if mode != 'none' else None, touch=True)
    r.ev("SHIP.device && SHIP.device.settings && (SHIP.device.settings.tips = false)")
    r.step(10)
    for b in presses: r.press(b); r.step(4)
    r.step(PRE - 10 - 7 * len(presses))
    shots, st = [], []
    # the first tap by the mouse, the second a real touch (the phone's way)
    for k, (x, y) in enumerate([(450, 380), (700, 300)]):
        if k == 0: r.page.mouse.click(x, y)
        else: r.page.touchscreen.tap(x, y)
        r.step(90)
        shots.append((f'tap{k}', r.shot(f'{tag}_tap{k}'))); g = r.ev(GAME_STATE)
        for x in ('calls', 'tris', 'mem', 'scene'): g.pop(x, None)   # made on first use and kept: not what you see
        st.append([g, r.js(OUTLINES), r.ev(SEEN_STATE)])
    r.close(); return shots, st
def part_touch(pw, src, tag):
    fails = []
    a, sa0 = touch_play(pw, src, f'{tag}_touch_none', 'none', [])
    # B (put away a message: none on screen) and D-pad up then down (to the screen's edge buttons and back); not LB/RB,
    # which really turn the view (a different picture by design)
    for presses in ([], ['B'], ['UP', 'DOWN'], ['UP']):   # [] first: no pad again, the check's own steadiness
        b, sb = touch_play(pw, src, f'{tag}_touch_{"".join(presses) or "again"}', 'pad' if presses else 'none', presses)
        sa = json.loads(json.dumps(sa0))
        kept = {x: (sa[1][2][x], sb[1][2][x]) for x in ('all', 'scene') if sa[1][2][x] != sb[1][2][x]}
        if kept: print(f'    kept hidden after the touch (information): ' + ', '.join(f'{x} {u} -> {v}' for x, (u, v) in kept.items()))
        for k in range(2):
            for x in ('all', 'scene'): sa[k][2].pop(x, None); sb[k][2].pop(x, None)
        d = same_pics(a, b) + [x for k in range(2) for x in diff_state(sa[k][0], sb[k][0], f'tap{k}') + diff_state(sa[k][2], sb[k][2], f'tap{k}.seen')]
        for k in range(2):
            if sb[k][1]['outlines']: d.append(f'tap{k}: a focus outline is left: {sb[k][1]["outlines"]}')
            if sb[k][1]['focus'] != sa[k][1]['focus']: d.append(f'tap{k}: focus on {sb[k][1]["focus"]}, without a pad {sa[k][1]["focus"]}')
        print(f'  {"pressed " + " then ".join(presses) if presses else "no pad again"}, then a click and a touch: {"the no-pad game" if not d else str(len(d)) + " differences"}')
        fails += [f'after {"+".join(presses)}: {x}' for x in d[:5]]
    return fails

# ---- disconnecting (deck: stop at once; marks: the pause and its line) -------------------------------------------------
def part_unplug(pw, src, tag):
    fails = []
    r = Run(pw, src, f'{tag}_unplug', mode='pad', plug={}); r.step(10)
    cell = r.ev(OPEN_CELL); r.ev(f"({PUT})({json.dumps(cell[:2])})"); r.step(3)
    r.pad(10, a={0: 1}, release=False)
    r.js('window.__pads.unplug(0)'); r.step(1); p0 = r.ev(f"({SCREEN})()"); r.step(10); p1 = r.ev(f"({SCREEN})()")
    moved = ((p1[2] - p0[2]) ** 2 + (p1[3] - p0[3]) ** 2) ** .5
    st = r.ev("[PAUSE.on, (document.getElementById('pauseCard') || {}).textContent || '']")
    print(f'  unplugged mid-walk: moved {moved:.3f} m after; paused {st[0]}, the card: "{st[1][:80]}"')
    if moved > .01: fails.append(f'still walking after the pad was unplugged ({moved:.3f} m)')
    if r.ev("!!player.steer && player.steer.k > 0"): fails.append('unplugged: the walk the stick asked for is still there (player.steer), it walks on when the game goes on')
    if not st[0]: fails.append('unplugged within half a minute of using it: the game should pause')
    elif 'Controller disconnected' not in st[1]: fails.append(f'the Pause card should say "Controller disconnected": "{st[1][:80]}"')
    t0 = r.ev("SHIP.time.min"); r.step(60); t1 = r.ev("SHIP.time.min")
    if t1 != t0: fails.append(f'the ship clock ran while paused after the unplug ({t0} -> {t1})')
    r.js('window.__pads.plug(0, {})'); r.step(5); r.press('MENU'); r.step(10)
    if r.ev("PAUSE.on"): fails.append('reconnected and pressed Start: the game should go on')
    else:
        print('  plugged back in, Start: playing again')
        a = r.ev(f"({SCREEN})()"); r.step(15); b = r.ev(f"({SCREEN})()"); mv = ((b[2] - a[2]) ** 2 + (b[3] - a[3]) ** 2) ** .5
        if mv > .01 and not r.ev("(player.path || []).length"): fails.append(f'after the reconnect you walk by yourself ({mv:.2f} m with the stick untouched)')
    # not used for over half a minute: unplugging only stops (no pause)
    r.step(31 * 30); r.js('window.__pads.unplug(0)'); r.step(10)
    if r.ev("PAUSE.on"): fails.append('unplugged a pad not used for half a minute: the game should not pause')
    else: print('  unplugged after half a minute unused: no pause')
    # touch keeps working all the while
    t = r.ev(f"({SCREEN})()"); r.page.mouse.click(450, 380); r.step(90); u = r.ev(f"({SCREEN})()")
    if abs(t[2] - u[2]) + abs(t[3] - u[3]) < .01 and not r.ev("!!player.path || !!player.act"): print('  (the tap after the unplug did not walk; the tap spot may be where you stand)')
    if r.errors: fails.append('page errors: ' + ' | '.join(r.errors[:3]))
    r.close(); return fails

# ---- odd pads (deck): one that doesn't report the standard layout, and two at once ----------------------------------
def walk_with(r, cell, i):
    r.ev(f"({PUT})({json.dumps(cell[:2])})"); r.step(3); in_use(r, i); p0 = r.ev(f"({SCREEN})()")
    r.pad(10, a={0: 1}, i=i); p1 = r.ev(f"({SCREEN})()")
    return ((p1[2] - p0[2]) ** 2 + (p1[3] - p0[3]) ** 2) ** .5
def part_odd(pw, src, tag):
    fails = []
    r = Run(pw, src, f'{tag}_odd1', mode='pad', plug={'id': 'USB Gamepad (Vendor: 0079 Product: 0006)', 'mapping': '', 'nb': 12, 'na': 6}); r.step(10)
    cell = r.ev(OPEN_CELL); m = walk_with(r, cell, 0)
    print(f'  a pad without the standard layout (12 buttons, 6 axes): the left stick walked {m:.2f} m')
    if m < .2: fails.append(f'a non-standard pad: its left stick should still walk (best-guess layout): {m:.2f} m')
    r.close()
    r = Run(pw, src, f'{tag}_odd2', mode='pad', plug={}); r.step(5)
    r.js("window.__pads.plug(1, { id: 'DualSense Wireless Controller (STANDARD GAMEPAD Vendor: 054c Product: 0ce6)' })"); r.step(5)
    cell = r.ev(OPEN_CELL)
    m0 = walk_with(r, cell, 0); r.press('LB', i=1); r.step(20); m1 = walk_with(r, cell, 1); r.press('RB', i=0); r.step(20); m2 = walk_with(r, cell, 0)
    print(f'  two pads: the first walked {m0:.2f} m; after a press on the second it walked {m1:.2f} m; the first again {m2:.2f} m')
    if min(m0, m1, m2) < .2: fails.append(f'two pads: whichever pressed last should walk ({m0:.2f}, {m1:.2f}, {m2:.2f} m)')
    # the pad not in charge unplugged while the other walks: no stop, no pause
    r.press('LB', i=1); r.step(20); r.ev(f"({PUT})({json.dumps(cell[:2])})"); r.step(3)
    r.pad(4, a={0: 1}, i=1, release=False); r.js('window.__pads.unplug(0)'); p0 = r.ev(f"({SCREEN})()"); r.step(6); p1 = r.ev(f"({SCREEN})()")
    r.js('window.__pads.clear(1)'); r.step(2)
    mv = ((p1[2] - p0[2]) ** 2 + (p1[3] - p0[3]) ** 2) ** .5; pz = r.ev("PAUSE.on")
    print(f'  the other pad unplugged while this one walks: walked on {mv:.2f} m, paused {pz}')
    if mv < .05 or pz: fails.append(f'unplugging the pad not in charge should neither stop nor pause the one walking ({mv:.2f} m, paused {pz})')
    if r.errors: fails.append('page errors: ' + ' | '.join(r.errors[:3]))
    r.close(); return fails

# ---- picking (pick): the ringed thing and A, against a tap on the same thing --------------------------------------------
# Five kinds of thing, found from the deck itself: a crew member (DECK_CREW, awake if any), a seat (a place of a sitting
# kind), an item (ITEMS), a sealed door (CLOSED_DOORS) and the lift door. Stand beside it facing it; step the D-pad right
# until the bottom line (#padHint) names it; press A. A second run, frame for frame the same, taps the thing where it is
# on screen instead. A must lead to what the tap led to.
CROWDED_SEAT = r"""(() => { const held = id => typeof heldBy === 'function' ? !!heldBy(id) : false;
  for (const pl of PLACE_OF.values()) { if (pl.type !== 'mess-seat' || held(pl.id)) continue; const sp = placeSpot(pl.id); if (!sp) continue;
    const a = DECK_CREW.find(a => a.x !== undefined && a.settled && Math.hypot(a.x - sp.x, a.z - sp.z) < 1.3);
    if (a) return { kind: 'crowded seat', name: pl.id + ' beside ' + a.p.name, words: ['sit'], x: sp.x, y: 0, z: sp.z, seat: 1 }; }
  return null; })()"""
PICK_TARGETS = r"""(() => { const out = [], v = new THREE.Vector3();
  const a = DECK_CREW.find(a => a.x !== undefined && a.pose !== 'lie') || DECK_CREW.find(a => a.x !== undefined);
  if (a) out.push({ kind: 'crew', name: a.p.name, words: [a.p.name.toLowerCase()], x: a.x, y: (a.y || 0) + 1, z: a.z, crew: DECK_CREW.indexOf(a) });
  // a seat with no other seat within reach, so "Sit" on the bottom line can only mean that one
  const seats = [...PLACE_OF.values()].filter(pl => ['lounge-seat', 'mess-seat', 'bench', 'common-room'].includes(pl.type) && placeSpot(pl.id)).map(pl => [pl, placeSpot(pl.id)]);
  const lone = seats.find(([pl, sp]) => seats.every(([q, sq]) => q === pl || Math.hypot(sq.x - sp.x, sq.z - sp.z) > 3.6));
  const seat = lone ? lone[0] : null;
  if (seat) { const sp = placeSpot(seat.id); out.push({ kind: 'seat', name: seat.id, words: ['sit'], x: sp.x, y: 0, z: sp.z, seat: 1 }); }
  const it = ITEMS.find(i => i.hit && !i.wall && !i.see && !i.lift && /\w/.test(i.t) && (i.machine || i.mach || /panel|valve|pump|console|unit|rack|station/i.test(i.t))) || ITEMS.find(i => i.hit && !i.wall && !i.see && !i.lift);
  if (it) { it.hit.getWorldPosition(v); out.push({ kind: 'item', name: it.t, words: [it.t.toLowerCase()], x: v.x, y: v.y, z: v.z, item: ITEMS.indexOf(it) }); }
  const dk = Object.keys(typeof CLOSED_DOORS !== 'undefined' ? CLOSED_DOORS : {})[0];
  if (dk) { const e = EDGES.get(dk), c = CLOSED_DOORS[dk]; out.push({ kind: 'sealed door', name: c.t, words: [(c.t || 'door').toLowerCase()], x: e.cx, y: 1, z: e.cz, door: dk }); }
  const ld = DOOR_OBJS.find(d => d.e.type === 'lift'); if (ld) out.push({ kind: 'lift', name: 'the lift', words: ['lift'], x: ld.e.cx, y: 1, z: ld.e.cz, lift: 1 });
  return out; })()"""
STAND_BY = r"""((t) => { const c = nearestOpen(t.x, t.z, player); if (!c) return false; player.stop(); player.steer = null;
  player.obj.position.copy(cellPos(...c)); target.copy(player.obj.position).setY(.7);
  player.face = Math.atan2(t.x - player.obj.position.x, t.z - player.obj.position.z); return true; })"""
TARGET_AT = r"""((t) => { let x = t.x, y = t.y, z = t.z; if (t.crew !== undefined) { const a = DECK_CREW[t.crew]; if (a) { x = a.x; z = a.z; y = (a.y || 0) + (a.pose === 'lie' ? .15 : a.pose === 'sit' ? .7 : 1); } }
  const v = new THREE.Vector3(x, y, z).project(camera); return [(v.x + 1) / 2 * innerWidth, (1 - v.y) / 2 * innerHeight]; })"""
# a point a finger can tap to reach it, by the game's own hit tests (section 11's pick and crewAtScreen): the middle of
# the thing on screen, else the nearest point around it (a spiral out to 60 px) that reaches it
TAP_POINT = r"""((t) => { const [x0, y0] = (TARGET_AT_)(t), a = t.crew !== undefined ? DECK_CREW[t.crew] : null;
  const ok = (x, y) => { const c = crewAtScreen(x, y); if (t.crew !== undefined) return c === a; if (c) return false;
    const h = pick(x, y), u = h ? h.object.userData : null;
    if (t.item !== undefined) return !!(u && u.item === ITEMS[t.item]);
    if (t.door !== undefined) return !!(u && u.closedDoor === t.door);
    if (t.lift) return !!(u && (u.liftDoor || (u.item && u.item.lift)));
    if (t.seat) return !!h && !(u && (u.item || u.walker || u.closedDoor || u.liftDoor || u.youLock));
    return false; };
  for (let r = 0; r <= 60; r += 4) for (let k = 0; k < (r ? 16 : 1); k++) { const x = x0 + r * Math.cos(k * Math.PI / 8), y = y0 + r * Math.sin(k * Math.PI / 8); if (ok(x, y)) return [x, y]; }
  return null; })"""
OUTCOME = r"""(() => ({ at: [Math.round(player.obj.position.x * 100), Math.round(player.obj.position.z * 100)], path: (player.path || []).length,
  act: typeof ACT !== 'undefined' && ACT ? String(ACT.kind) : null, toast: document.getElementById('tt').textContent + '|' + document.getElementById('tx').textContent,
  dev: DEV.open, lift: !document.getElementById('lift').hidden, paused: PAUSE.on, deck: player.deck,
  chat: (() => { const c = document.getElementById('chat'); return c && !c.hidden && c.getBoundingClientRect().width > 0 ? c.textContent.replace(/\s+/g, ' ').slice(0, 60) : null; })(),
  talking: DECK_CREW.filter(a => a.talking > 0).map(a => a.p.id).sort(),
  open: [...document.querySelectorAll('[role=dialog],.lift,.device')].filter(e => !e.hidden && e.getBoundingClientRect().width > 0).map(e => e.id || e.className).sort() }))()"""
HINT = "(() => { const h = document.getElementById('padHint'); return h && !h.hidden && h.getBoundingClientRect().width > 0 ? h.textContent : null; })()"
# a seat with no other seat within reach, on the deck you're on (so "Sit" can only mean that one)
LONE_SEAT = r"""(() => { const seats = [...PLACE_OF.values()].filter(pl => ['lounge-seat', 'mess-seat', 'bench', 'common-room'].includes(pl.type) && placeSpot(pl.id)).map(pl => [pl, placeSpot(pl.id)]);
  const lone = seats.find(([pl, sp]) => seats.every(([q, sq]) => q === pl || Math.hypot(sq.x - sp.x, sq.z - sp.z) > 3.6));
  return lone ? { kind: 'seat', name: deckDef.num + ':' + lone[0].id, words: ['sit'], x: lone[1].x, y: 0, z: lone[1].z, seat: 1 } : null; })()"""
DECKS_JS = "(typeof DECK_ORDER !== 'undefined' ? DECK_ORDER : Object.keys(DECKS).map(Number))"
def hint_now(r):
    """the bottom line; a message showing hides it, so B first puts the message away, as a player would"""
    h = r.ev(HINT)
    if h is None and r.ev("toastEl.classList.contains('show')"): r.press('B'); r.step(2); h = r.ev(HINT)
    return h
def pick_one(pw, src, tag, by_pad, n, presses=0, seat_search=False):
    # target n of PICK_TARGETS, from a fresh load (a panel the last one opened can't get in the way), frame for frame
    # the same in the pad run and the tap run: the pad run goes first, and the tap run waits 7 frames for each D-pad
    # press the pad run made (presses) before it taps
    r = Run(pw, src, f'{tag}_{n}', mode='pad' if by_pad else 'none', plug={} if by_pad else None, w=390, h=844)
    r.ev("SHIP.device && SHIP.device.settings && (SHIP.device.settings.tips = false)")
    r.step(10)
    if by_pad: r.press('B'); r.step(2)
    else: r.step(5)
    ts = r.ev(PICK_TARGETS)
    if seat_search:   # (RV5) no lone seat on Deck 4: the first deck that has one
        t = None
        for d in r.ev(DECKS_JS):
            r.ev(f"goToDeck({d}, null)"); r.step(60); t = r.ev(LONE_SEAT)
            if t: break
        if not t: r.close(); return ['seat (none on any deck)', 'nowhere to stand', None, None, 0], len(ts)
    elif n >= len(ts): r.close(); return None, len(ts)
    else: t = ts[n]
    name = t['kind'] + ' (' + str(t.get('name')) + ')'
    r.ev("toastEl.classList.remove('show'); document.getElementById('tt').textContent = ''; document.getElementById('tx').textContent = ''")
    if not r.ev(f"({STAND_BY})({json.dumps(t)})"): r.close(); return [name, 'nowhere to stand', None, None], len(ts)
    r.step(72); hints = []; found = not by_pad   # (the ring's search needs about 2 s after the check moves you)
    if not by_pad and presses: r.step(7 * presses)
    for k in range(9 if by_pad else 0):
        h = r.ev(HINT); hints.append(h)
        if h and any(w in h.lower() for w in t['words']): found = True; break
        r.press('RIGHT'); r.step(4); presses += 1   # (a press is 3 frames)
    if by_pad: r.press('A')
    else:
        pt = r.ev(f"({TAP_POINT.replace('TARGET_AT_', TARGET_AT)})({json.dumps(t)})")
        if pt: r.page.mouse.click(*pt)
        else: print(f'  ({name}: no point on screen reaches it by a tap)')
        r.step(3)
    r.step(90); out = [name, hints[-1] if found and hints else hints, r.ev(OUTCOME), found, presses]
    r.close(); return out, len(ts)
def pick_play(pw, src, tag, by_pad, pad=None):
    # pad: the pad run's results, for the tap run to wait as long as each pad run read the line
    out, n = [], 0
    while True:
        o, total = pick_one(pw, src, tag + ('_pad' if by_pad else '_tap'), by_pad, n, pad[n][4] if pad and n < len(pad) else 0)
        if o is None: break
        out.append(o); n += 1
    if not any(x[0].startswith('seat') for x in out):
        o, _ = pick_one(pw, src, tag + ('_pad' if by_pad else '_tap'), by_pad, n, pad[n][4] if pad and n < len(pad) else 0, seat_search=True)
        out.append(o)
    return out
# facing (RV2's fix): a spot with two things in reach on opposite sides; face one, and the ring starts on it (before any
# D-pad); turn round, and it starts on the other
FACING_SPOT = r"""(() => { const v = new THREE.Vector3(), its = ITEMS.filter(i => i.hit && !i.wall && !i.see && /\w/.test(i.t)).map(i => { i.hit.getWorldPosition(v); return [i, v.x, v.z]; });
  for (let j = 1; j < D - 1; j++) for (let i = 1; i < W - 1; i++) { if (!free(i, j)) continue; const c = cellPos(i, j);
    if (DECK_CREW.some(a => a.x !== undefined && Math.hypot(a.x - c.x, a.z - c.z) < 3.5)) continue;
    const near = its.filter(([it, x, z]) => { const d = Math.hypot(x - c.x, z - c.z); return d > .8 && d < 2.2; });
    for (const A of near) for (const B of near) { if (A[0].t === B[0].t) continue;
      const a = Math.atan2(A[1] - c.x, A[2] - c.z), b = Math.atan2(B[1] - c.x, B[2] - c.z), d = Math.abs(((a - b + 3 * Math.PI) % (2 * Math.PI)) - Math.PI);
      if (d > 2.6 && near.every(([it, x, z]) => it === A[0] || it === B[0] || Math.abs(((Math.atan2(x - c.x, z - c.z) - a + 3 * Math.PI) % (2 * Math.PI)) - Math.PI) > .9 && Math.abs(((Math.atan2(x - c.x, z - c.z) - b + 3 * Math.PI) % (2 * Math.PI)) - Math.PI) > .9))
        return { cell: [i, j], a: [A[0].t, a], b: [B[0].t, b] }; } }
  return null; })()"""
def part_facing(pw, src, tag):
    fails = []
    r = Run(pw, src, f'{tag}_facing', mode='pad', plug={}, w=390, h=844); r.step(10); r.press('B'); r.step(2)
    sp = r.ev(FACING_SPOT)
    if not sp: r.close(); return ['facing: not proven (no spot on Deck 4 with two things on opposite sides and nothing else beside them)']
    for name, ang in (sp['a'], sp['b']):
        r.ev(f"player.stop(); player.obj.position.copy(cellPos({sp['cell'][0]}, {sp['cell'][1]})); target.copy(player.obj.position).setY(.7); player.face = {ang}")
        r.step(72); h = hint_now(r)
        print(f'  facing {name}: the ring starts on "{h}"')
        if not h or name.lower() not in h.lower(): fails.append(f'facing {name} (another thing behind you): the ring should start on it, the line says "{h}"')
    r.close(); return fails
# the crowded mess at breakfast (the plan's risk: "picking the wrong thing in a crowded mess hall"): stand among the
# tables beside a free seat with someone seated next to it, let the ring settle (its search runs a little each frame and
# a D-pad press starts it again, so after the check moves you it waits about 2 s), then step through what's offered. A
# "Sit" whose point on screen has a person on it at the moment A is pressed is the hard case (PR9's c7): A must not talk
# to them (the game finds another point, or does nothing). Without such a one the case is not proven: a failure, so a
# change to the deck can't quietly switch it off. (It is made the ring's choice as the D-pad does it, one frame before A,
# so the crowd can't move away in between.)
RING_SEL = r"""(() => { const s = typeof PAD_PICK !== 'undefined' ? PAD_PICK.sel : null; if (!s || !s.s) return null;
  const a = crewAtScreen(s.s[0], s.s[1]); return { key: s.key, on: a ? a.p.name : null }; })()"""
RING_PICK_CROWDED = r"""(() => { const P = PAD_PICK; for (const t of P.list) { if (!t.key.startsWith('place:') || !t.s) continue; const a = crewAtScreen(t.s[0], t.s[1]);
  if (a) { P.sel = t; P.chosen = true; P.n = P.every; P.job = null; return [t.key, a.p.name]; } } return null; })()"""
RING_PICK_NAMED = r"""(() => { const P = PAD_PICK; for (const t of P.list) { if (!t.key.startsWith('crew:') || !t.s) continue; const a = crewAtScreen(t.s[0], t.s[1]);
  if (a && 'crew:' + a.p.id !== t.key) { P.sel = t; P.chosen = true; P.n = P.every; P.job = null; return [t.key, a.p.name]; } } return null; })()"""
CREW_NAME = "(k => { const a = DECK_CREW.find(a => 'crew:' + a.p.id === k); return a ? a.p.name : null; })"
def crowded_setup(pw, src, tag):
    r = Run(pw, src, tag, mode='pad', plug={}, w=390, h=844)
    r.ev("SHIP.device && SHIP.device.settings && (SHIP.device.settings.tips = false)"); r.step(10); r.press('B'); r.step(2)
    # breakfast's busiest minutes moved with the playtests (07:00 from 0.64.17): the first of these with a free seat beside
    # someone seated
    t = None; r.ev("goToDeck(3, null)")
    for hm in (7 * 60 + 20, 7 * 60 + 40, 8 * 60, 8 * 60 + 20):
        r.ev(f"SHIP.time.min < {hm} && skipTo((SHIP.time.day - 1) * 1440 + {hm})"); r.step(240); t = r.ev(CROWDED_SEAT)
        if t: break
    if not t or not r.ev(f"({STAND_BY})({json.dumps(t)})"): r.close(); return None, None
    r.ev("toastEl.classList.remove('show')"); r.step(72); return r, t
# (RV5's C7) in the same crowd: "Talk to X" whose point on screen is on someone else, Y, at the moment A is pressed. A must
# talk to X (the game finds X again), never Y. Without such a one: said, not a failure (the seat case above is the proof
# that the crowd is there).
def part_crowded_named(pw, src, tag):
    r, t = crowded_setup(pw, src, f'{tag}_crowd2')
    if not r: return []
    want = other = None
    for k in range(30):
        got = r.ev(RING_PICK_NAMED)
        if got:
            r.step(1); sel = r.ev(RING_SEL)
            if sel and sel['key'] == got[0] and sel['on'] and sel['on'] == got[1]: want, other = got; break
        r.step(4)
    if not want: print('  crowded talk: no "Talk to" in the ring with someone else on its point came up (not tried)'); r.close(); return []
    name = r.ev(f"({CREW_NAME})({json.dumps(want)})"); h = r.ev(HINT)
    r.press('A'); r.step(90); o = r.ev(OUTCOME)
    print(f'  crowded talk: A on "{h}" with {other} on its point: chat {o["chat"]}')
    fails = []
    if not o['chat'] or name not in o['chat']: fails.append(f'crowded talk: A on "{h}" ({other} on its point) should talk to {name}: chat {o["chat"]}')
    if r.errors: fails.append('crowded talk: page errors: ' + ' | '.join(r.errors[:3]))
    r.close(); return fails
def part_crowded(pw, src, tag):
    fails = []
    r, t = crowded_setup(pw, src, f'{tag}_crowd')
    if not r: return ['crowded seat: not proven (no free seat beside someone seated in the Deck 3 mess at 07:40)']
    seen = []
    for k in range(10):
        h, sel = r.ev(HINT), r.ev(RING_SEL)
        if sel and sel['key'] in [x[1]['key'] for x in seen]: break
        if sel: seen.append((h, sel))
        r.press('RIGHT'); r.step(4)
    sits = [(h, sel) for h, sel in seen if h and 'sit' in h.lower()]
    print(f'  crowded seat (beside {t["name"]}): the ring offers ' + '; '.join(f'"{h}"' + (f' (its point on {sel["on"]})' if sel['on'] else '') for h, sel in seen))
    if not sits: r.close(); return fails + ['crowded seat: the ring never offered a seat in the crowded mess']
    # the hard case at the moment of pressing: a seat in the ring with a person on its point now (the crowd moves, so
    # look for one for up to about 4 s); it becomes the ring's choice, as the D-pad makes it, and A is pressed at once
    # (one frame after choosing, so the line has been redrawn for the choice; then the person must still be on its point)
    on = None
    for k in range(30):
        got = r.ev(RING_PICK_CROWDED)
        if got:
            r.step(1); sel = r.ev(RING_SEL)
            if sel and sel['key'] == got[0] and sel['on']: want, on = got[0], sel['on']; break
        r.step(4)
    if not on: r.close(); return fails + ['crowded seat: not proven (no seat in the ring with a person on its point came up in about 4 s)']
    h = r.ev(HINT)
    r.press('A'); r.step(90); o = r.ev(OUTCOME)
    print(f'  crowded seat: A on "{h}" ({want}, a person on its point: {on}): chat {o["chat"]}, act {o["act"]}')
    if o['chat']: fails.append(f'crowded seat: A on "{h}" ({want}) talked to someone instead ({o["chat"]})')
    if r.errors: fails.append('crowded seat: page errors: ' + ' | '.join(r.errors[:3]))
    r.close(); return fails
def part_pick(pw, src, tag):
    fails = part_facing(pw, src, tag)
    fails += part_crowded(pw, src, tag)
    fails += part_crowded_named(pw, src, tag)
    P = pick_play(pw, src, f'{tag}_pick', True)
    T = pick_play(pw, src, f'{tag}_pick', False, P)
    for (kind, hint, op, found, _), (_, _, ot, _, _) in zip(P, T):
        if kind.startswith('seat (none'): fails.append('seat: not proven (no seat without another seat in reach on any deck)'); continue
        if hint == 'nowhere to stand': print(f'  {kind}: nowhere to stand beside it'); continue
        if not found: fails.append(f'{kind}: the bottom line never named it ({[h for h in hint if h][:4]})'); print(f'  {kind}: not reached by the D-pad'); continue
        if 'seat' in kind:
            ot = {k: ot[k] for k in ('act', 'open', 'dev', 'lift', 'deck', 'chat')} | {'toast': ot['toast'].split('|')[0]}
            op = {k: op[k] for k in ('act', 'open', 'dev', 'lift', 'deck', 'chat')} | {'toast': op['toast'].split('|')[0]}
        d = diff_state(ot, op)
        print(f'  {kind}: the line says "{hint}"; A {"did what the tap did" if not d else "differs from the tap: " + "; ".join(d[:3])}')
        if d: fails.append(f'{kind} ("{hint}"): A and a tap differ: ' + '; '.join(d[:3]))
    kinds = {x[0].split(' (')[0] for x in P}
    for k in ('crew', 'seat', 'item', 'sealed door', 'lift'):
        if k not in kinds: print(f'  {k}: none on this deck to try' + (' (no seat without another seat in reach, so "Sit" would be ambiguous)' if k == 'seat' else ''))
    if len(P) < 4: fails.append(f'only {len(P)} kinds of thing found on the deck to pick')
    return fails

# ---- the games (games): Tiles to the end, and Lightdisc, by pad ---------------------------------------------------------
# Tiles: opened as tiles_check does (tilesPlay), then played only by pad: each move is the game's own choice (tilesAI,
# medium), and each square or hold button it needs is reached with the D-pad (the highlight is the page's focus) and
# pressed with A. The crew's answer is made at once (its real-time timer cleared, as tiles_check does). At the end the
# D-pad and A reach Done and the board closes.
FOCUS_ON = r"""((sel) => { const t = document.querySelector(sel), f = document.activeElement; if (!t) return { gone: true };
  if (f === t || t.contains(f)) return { on: true };
  const a = t.getBoundingClientRect(), b = f && f !== document.body ? f.getBoundingClientRect() : null;
  if (!b) return { none: true };
  const dx = (a.left + a.width / 2) - (b.left + b.width / 2), dy = (a.top + a.height / 2) - (b.top + b.height / 2);
  return { dx, dy }; })"""
def pad_to(r, sel, tries=40):
    """move the highlight onto sel with the D-pad (the bigger gap first); True once it's there"""
    for k in range(tries):
        f = r.ev(f"({FOCUS_ON})({json.dumps(sel)})")
        if f.get('on'): return True
        if f.get('gone'): return False
        if f.get('none'): r.press('DOWN'); r.step(1); continue
        dx, dy = f['dx'], f['dy']
        r.press(('RIGHT' if dx > 0 else 'LEFT') if abs(dx) >= abs(dy) else ('DOWN' if dy > 0 else 'UP')); r.step(1)
    return r.ev(f"({FOCUS_ON})({json.dumps(sel)})").get('on', False)
def part_games(pw, src, tag):
    fails = []
    r = Run(pw, src, f'{tag}_tiles', mode='pad', plug={}, w=390, h=844)
    r.ev("SHIP.device && SHIP.device.settings && (SHIP.device.settings.tips = false); SHIP.device.tipsSeen && (SHIP.device.tipsSeen.device = true)"); r.step(10)
    r.press('B'); r.step(2)
    r.ev("tilesPlay('tomas', null, 'quick')"); r.step(4)
    played0 = r.ev("SHIP.tiles.played"); moves = 0; stuck = None
    for n in range(120):
        st = r.ev("(() => { const G = TL_GAME; if (!G) return null; if (G.timer) { clearTimeout(G.timer); G.timer = 0; } if (!G.s.over && G.s.p === 1) tilesCrewMove(); return { over: G.s.over, p: G.s.p }; })()")
        if not st or st['over']: break
        mv = r.ev(f"(() => {{ const m = tilesAI(TL_GAME.s, 'medium', tilesRng({n})); return m; }})()")
        first = f'#devBody .tl-hd button[data-h="{mv["m"]}"]' if mv.get('k') == 'l' else f'#devBody .tl-c[data-c="{mv["from"]}"]'
        for sel in (first, f'#devBody .tl-c[data-c="{mv["to"]}"]'):
            if not pad_to(r, sel): stuck = sel; break
            r.press('A'); r.step(2)
        if stuck: break
        moves += 1
    over = r.ev("!!TL_GAME && TL_GAME.s.over")
    print(f'  Tiles: {moves} moves made by pad; game over {over}' + (f'; the highlight never reached {stuck}' if stuck else ''))
    if stuck: fails.append(f'Tiles: the D-pad never reached {stuck}')
    elif not over: fails.append(f'Tiles: not over after {moves} moves by pad')
    else:
        done = pad_to(r, '#devBody .tl-end button[data-end="done"]')
        if done: r.press('A'); r.step(6)
        closed = r.ev("!TL_GAME || !DEV.open || DEV.app !== 'tiles'"); played = r.ev("SHIP.tiles.played")
        print(f'  Tiles: Done reached and pressed by pad: {done}; the board closed: {closed}; games played {played0} -> {played}')
        if not (done and closed): fails.append(f'Tiles: Done by pad should end it (reached {done}, closed {closed})')
        if played != played0 + 1: fails.append(f'Tiles: a game played to the end should count once ({played0} -> {played})')
    if r.errors: fails.append('Tiles: page errors: ' + ' | '.join(r.errors[:3]))
    r.close()
    # Lightdisc: on the rec deck in the evening (as disc_check), asked for, then by pad only: A through the how-to-play,
    # the stick moves you, B leaves
    r = Run(pw, src, f'{tag}_disc', mode='pad', plug={}, w=390, h=844)
    r.ev("SHIP.device && SHIP.device.settings && (SHIP.device.settings.tips = false)"); r.step(5)
    r.ev("(() => { skipTo((SHIP.time.day - 1) * 1440 + 19 * 60); goToDeck(7, null); })()"); r.step(30)
    r.press('B'); r.step(2); r.ev("discAsk()")
    for k in range(90):
        r.step(30)
        if r.ev("!!(DISC.g && DISC.view)"): break
    if not r.ev("!!(DISC.g && DISC.view)"): fails.append('Lightdisc: no game started (nobody came?)'); r.close(); return fails
    for k in range(6):
        if r.ev("DISC.how") < 0: break
        x0 = r.ev("DISC.g.p[0].x"); r.pad(20, a={0: 1}); r.pad(20, a={0: -1}); r.press('A'); r.step(4)
    x0 = r.ev("DISC.g.p[0].x"); r.pad(15, a={0: 1}); x1 = r.ev("DISC.g.p[0].x"); r.pad(15, a={0: -1}); x2 = r.ev("DISC.g.p[0].x")
    print(f'  Lightdisc: the how-to-play passed ({r.ev("DISC.how")}); the stick moved you {x1 - x0:+.2f} then {x2 - x1:+.2f}')
    if not (x1 > x0 and x2 < x1): fails.append(f'Lightdisc: the stick should move you right then left ({x0:.2f} -> {x1:.2f} -> {x2:.2f})')
    r.press('B'); r.step(10)
    for k in range(3):   # Leave may ask once more: the highlight lands on its button, A confirms
        if not r.ev("!!DISC.g"): break
        r.press('A'); r.step(10)
    left = not r.ev("!!(DISC.g && DISC.view)")
    print(f'  Lightdisc: B left the game: {left}')
    if not left: fails.append('Lightdisc: B should leave the game')
    if r.errors: fails.append('Lightdisc: page errors: ' + ' | '.join(r.errors[:3]))
    r.close(); return fails

# ---- a whole day by pad (all packages) ---------------------------------------------------------------------------------
# You move only by the pretend controller: the stick steers along the game's own path (findPath) to where you're going,
# the D-pad steps the ring until the bottom line names the thing, A uses it, and in panels the D-pad and A press the
# button wanted. The check only fast-forwards the clock between scenes and marks the button it wants (data-ctt) so the
# D-pad can be steered to it. Scenes: the lift down to breakfast, eat, talk to someone, take a job at the board, the
# lift home, set the alarm and sleep.
STEER = r"""((gx, gz) => { const s = player.here(), g = nearestOpen(gx, gz, player); if (!s || !g) return null;
  const pp = player.obj.position, gp = cellPos(...g); if (Math.hypot(gp.x - pp.x, gp.z - pp.z) < .45 || (s[0] === g[0] && s[1] === g[1])) return { there: true };   // (on its cell: there, though people may keep you off its middle)
  // (around people if it can; else through them: the game lets you push past someone after 2 s)
  let path = findPath(s, g, null, player); if (!path || !path.length) path = findPath(s, g); if (!path || !path.length) return { nopath: true };
  // the stick for that way, by the view's own axes (up on the stick is away from the camera: right (cos az, -sin az),
  // forward (-sin az, -cos az)); the way it looks on screen is squashed by the camera's tilt, so it isn't used
  // the next cell of the way (the one after it once you're on it): aiming further cuts corners and sticks on them
  let w = cellPos(...path[0]); if (path.length > 1 && Math.hypot(w.x - pp.x, w.z - pp.z) < .3) w = cellPos(...path[1]);
  const dx = w.x - pp.x, dz = w.z - pp.z, d = Math.hypot(dx, dz) || 1;
  const x = (dx * Math.cos(az) - dz * Math.sin(az)) / d, y = (dx * Math.sin(az) + dz * Math.cos(az)) / d; return { x, y }; })"""
def walk_to(r, x, z, frames=900):
    shut = 0
    for k in range(frames // 6):
        # a panel that opened on the way (a ladder hatch underfoot, 0.64.17): B puts it away, as a player would, then on
        if shut < 4 and r.ev("!!padLayer()"): r.js('window.__pads.clear(0)'); r.press('B'); r.step(3); shut += 1; continue
        st = r.ev(f"({STEER})({x}, {z})")
        if not st or st.get('there'): r.js('window.__pads.clear(0)'); r.step(2); return bool(st)
        if st.get('nopath'): r.js('window.__pads.clear(0)'); return False
        r.pad(6, a={0: st['x'], 1: st['y']}, release=False)
    r.js('window.__pads.clear(0)'); r.step(2); return False
def ring_and_A(r, words, tries=10):
    for k in range(tries):
        h = hint_now(r)
        if h and any(w in h.lower() for w in words): r.press('A'); r.step(4); return h
        r.press('RIGHT'); r.step(4)
    return None
# which deck has a thing, from its deck definition (without going there)
DECK_HAS = "Object.values(DECKS[D_]).some(v => (typeof v === 'function' ? v.toString() : (() => { try { return JSON.stringify(v) || ''; } catch (e) { return ''; } })()).includes('RX'))"
MARK = r"""((js) => { for (const e of document.querySelectorAll('[data-ctt]')) e.removeAttribute('data-ctt'); const e = (new Function('return ' + js))(); if (!e) return false; e.setAttribute('data-ctt', '1'); return true; })"""
def press_in_panel(r, js):
    if not r.ev(f"({MARK})({json.dumps(js)})"): return 'not there'
    if not pad_to(r, '[data-ctt]'): return 'never highlighted'
    r.press('A'); r.step(6); return 'ok'
WHERE_IS = r"""((re) => { const rx = new RegExp(re, 'i'), v = new THREE.Vector3(); const it = ITEMS.find(i => i.hit && rx.test(i.t)); if (!it) return null; it.hit.getWorldPosition(v); return [v.x, v.z, it.t]; })"""
def ride(r, deck, fails, scene):
    lp = r.ev("(() => { const d = DOOR_OBJS.find(d => d.e.type === 'lift'); return d ? [d.e.cx, d.e.cz] : null; })()")
    if not lp or not walk_to(r, *lp): fails.append(f'{scene}: could not walk to the lift by the stick'); return False
    if not ring_and_A(r, ['lift']): fails.append(f'{scene}: the ring never named the lift'); return False
    for k in range(20):
        if r.ev("!document.getElementById('lift').hidden"): break
        r.step(10)
    # the deck's button by its place in the game's own deck order (its words changed in 0.64.17: deckLabel)
    res = press_in_panel(r, f"document.querySelectorAll('#liftList button')[DECK_ORDER.indexOf({deck})]")
    if res != 'ok': fails.append(f'{scene}: the lift\'s Deck {deck} button: {res}'); return False
    for k in range(60):
        r.step(10)
        if r.ev("player.deck") == deck and not r.ev("!!ride"): return True
    fails.append(f'{scene}: the lift never reached Deck {deck}'); return False
MY_BUNK = r"""(() => { const id = playerBed(), bed = (DECKS[deckOf(id)].places || []).find(p => p.id === id); if (!bed) return null;
  const c = cellPos(...bed.at), v = new THREE.Vector3(); let best = null, bd = 1.2;
  ITEMS.forEach((it, i) => { if (!it.hit) return; it.hit.getWorldPosition(v); const d = Math.hypot(v.x - c.x, v.z - c.z); if (d <= bd) { bd = d; best = 'item:' + i; } });
  return best; })()"""
FREE_SEAT = r"""(() => { const held = id => typeof heldBy === 'function' ? !!heldBy(id) : false, pp = player.obj.position; let best = null, bd = 1e9;
  for (const [pl, sp] of padPlaces()) { if (pl.pose !== 'sit' || held(pl.id)) continue; const w = sp.walk ? cellPos(...sp.walk) : sp, d = Math.hypot(w.x - pp.x, w.z - pp.z); if (d < bd) { bd = d; best = [w.x, w.z, pl.id]; } }
  return best; })()"""
def part_day(pw, src, tag):
    fails = []
    r = Run(pw, src, f'{tag}_day', mode='pad', plug={}, w=390, h=844)
    r.ev("SHIP.device && SHIP.device.settings && (SHIP.device.settings.tips = false)"); r.step(10); r.press('B'); r.step(2)
    # breakfast: the servery is on another deck
    sv = None; deck = None
    for d in r.ev("(typeof DECK_ORDER !== 'undefined' ? DECK_ORDER : Object.keys(DECKS).map(Number))"):
        if r.ev(DECK_HAS.replace('RX', 'Servery').replace('D_', str(d))): deck = d; break
    h0 = r.ev("SHIP.player.needs.hunger")
    if deck and ride(r, deck, fails, 'breakfast'):
        sv = r.ev(f"({WHERE_IS})('servery')")
        if sv and walk_to(r, sv[0], sv[1]):
            got = ring_and_A(r, ['servery', 'eat', 'breakfast', 'food'])
            for k in range(60):   # the queue, then a tray
                r.step(15)
                if r.ev("!!SHIP.player.tray"): break
            tray = r.ev("SHIP.player.tray || null")
            if tray:   # carry it to the nearest free seat (by the stick), then "Sit" by the ring
                seat = r.ev(FREE_SEAT); sat = None
                if seat and walk_to(r, seat[0], seat[1]): sat = ring_and_A(r, ['sit', 'eat'])
                print(f'  a tray ({tray}); the nearest free seat {seat}; then "{sat}"')
            for k in range(60): r.step(15)
            h1 = r.ev("SHIP.player.needs.hunger")
            print(f'  breakfast on Deck {deck}: the line said "{got}"; hunger {h0:.0f} -> {h1:.0f}')
            if not got or h1 <= h0: fails.append(f'breakfast: by pad at the servery hunger should rise ({got}, {h0:.0f} -> {h1:.0f})')
        else: fails.append(f'breakfast: could not walk to the servery ({sv})')
    elif not deck: fails.append('breakfast: no servery found on any deck')
    # talk: the nearest crew member the ring offers; a conversation opens; B puts it away
    r.ev("actEnd && ACT && actEnd(true)"); r.step(10)
    a = r.ev("(() => { const a = DECK_CREW.find(a => a.x !== undefined && a.pose !== 'lie'); return a ? [a.x, a.z, a.p.name] : null; })()")
    if a and walk_to(r, a[0], a[1]):
        got = ring_and_A(r, ['talk']); r.step(30)
        opened = r.ev("[...document.querySelectorAll('[role=dialog],#chat')].some(e => !e.hidden && e.getBoundingClientRect().width > 0)") or r.ev("document.getElementById('tt').textContent.length > 0")
        r.press('B'); r.step(10)
        print(f'  talk: "{got}", something opened {opened}')
        if not got or not opened: fails.append(f'talk: by pad ({got}, opened {opened})')
    else: fails.append('talk: no crew member to walk to')
    # a job: the board (the job board item), Take it by pad
    jb = None
    for d in r.ev("(typeof DECK_ORDER !== 'undefined' ? DECK_ORDER : Object.keys(DECKS).map(Number))"):
        if r.ev(DECK_HAS.replace('RX', 'Job board').replace('D_', str(d))): jb = d; break
    if jb and (r.ev("player.deck") == jb or ride(r, jb, fails, 'the job board')):
        b = r.ev(f"({WHERE_IS})('job board')")
        if b and walk_to(r, b[0], b[1]) and ring_and_A(r, ['job board', 'board']):
            r.step(30); res = press_in_panel(r, "[...document.querySelectorAll('#ixBoardL button')].find(b => /take it/i.test(b.textContent))")
            mine = r.ev("typeof myJob === 'function' && !!myJob()")
            print(f'  the job board: Take it by pad: {res}; a job of yours: {mine}')
            if res != 'ok' or not mine: fails.append(f'the job board: Take it by pad ({res}, a job: {mine})')
            r.press('B'); r.step(10)
        else: fails.append('the job board: could not reach it by pad')
    # bed: the evening, the lift home, your bunk, Set alarm
    r.ev("skipTo((SHIP.time.day - 1) * 1440 + 22 * 60)"); r.step(20)
    if r.ev("player.deck") == 4 or ride(r, 4, fails, 'bedtime'):
        bp = r.ev("(() => { const s = placeSpot(playerBed()); if (!s) return null; const w = s.walk ? cellPos(...s.walk) : s; return [w.x, w.z]; })()")   # (its walk-to tile)
        if bp and walk_to(r, bp[0], bp[1]):
            # your own bunk, not a neighbour's (the game offers sleep only within 1.2 m of your bed): its ring key
            mine = r.ev(MY_BUNK); got = None
            for k in range(12):
                sel = r.ev(RING_SEL)
                if sel and mine and sel['key'] == mine: got = r.ev(HINT); break
                r.press('RIGHT'); r.step(4)
            if got: r.press('A')
            else: fails.append(f'bedtime: the ring never offered your own bunk ({mine})')
            for k in range(40):   # you walk over and lie down; at night, lying in it brings the alarm card (bunkSleep)
                r.step(15)
                if r.ev("!document.getElementById('sleepAsk').hidden"): break
            asked = r.ev("!document.getElementById('sleepAsk').hidden")
            res = press_in_panel(r, "document.getElementById('sleepYes')") if asked else 'no alarm card'
            r.step(60); t = r.ev("[SHIP.time.day, SHIP.time.min]")
            print(f'  bedtime: "{got}", the alarm card {asked}, Set alarm by pad: {res}; now day {t[0]} {int(t[1]) // 60:02d}:{int(t[1]) % 60:02d}')
            if res != 'ok': fails.append(f'bedtime: Set alarm by pad ({got}, {res})')
        else: fails.append(f'bedtime: could not walk to your bunk by the stick (bed {bp}; you at ' + str(r.ev("[player.deck, Math.round(player.obj.position.x * 10) / 10, Math.round(player.obj.position.z * 10) / 10, String(ACT && ACT.kind), !!ride, String(padLayer() && (padLayer().id || padLayer().className))]")) + '; the way: ' + str(r.ev(f"({STEER})({bp[0]}, {bp[1]})") if bp else None) + ')')
    if r.errors: fails.append('page errors: ' + ' | '.join(r.errors[:3]))
    r.close(); return fails

# ---- the builders' old-shape parts, brought in unchanged ---------------------------------------------------------------
# CT1's file gave each part (def part_X(pw)) the paths GAME (switch off) and ON (switch on), a Pad class over
# cadet_test's Game with CT1's pretend pad (window.__pads an array, __padPlug/__padHello/__padBtn/__padAxes), and check()
# and fail() globals. legacy_parts() gives them the same, per call: the parts below are the builders' own code, copied
# as it is (indented one step; CP3's part_touch is part_touch3; Pad makes its Game through old_game, which adds CT1's
# pad), and their failures are collected in a list, so a planted fault fails only that run.
# To update one: copy the builder's new version of the function in over the old one, and the tip in its heading.
OLD_FAKEPAD = r"""
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
def old_game(pw, path, w, h):
    global INIT
    keep = INIT; INIT = keep + OLD_FAKEPAD   # cadet_test's Game installs INIT before the game loads
    try: return Game(pw, path, w, h)
    finally: INIT = keep
def legacy_parts(GAME, ON, fails):
    BTN = {n: k for k, n in enumerate(['a', 'b', 'x', 'y', 'lb', 'rb', 'lt', 'rt', 'view', 'menu', 'ls', 'rs', 'up', 'down', 'left', 'right'])}
    def fail(msg): fails.append(msg); print('  (' + msg + ')')
    def check(cond, msg):
        if not cond: fail(msg)
        return cond
    # ---- CT1 and CP1 (claude/controller-p1 cff5bab, + CP1's claude/controller c11ed33c and 3dfe6579 in pick): off, quiet, base, deck, pick, panels, api, lists ----
    class Pad:
        """The game with a pretend controller: plug, hello, press, sticks, step."""
        def __init__(self, pw, path, w=390, h=844):
            self.g = old_game(pw, str(path), w, h)
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
        for q in (a, b): q.ev("typeof PAD_MARK === 'object' && (PAD_MARK.say = false, PAD_MARK.said = true)")   # (P3's one-time "Controller connected" comes at its own moment in each copy)
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
    # ---- CP2 (claude/controller-p2 7b11451): tiles, disc, screens ----
    # ---- P2: the mini-games (controller package 2) ----
    TL_FOCUS = "(() => { const a = document.activeElement, R = TL_UI.root; if (!a || !R || !R.contains(a)) return null; const d = a.dataset; return d.c !== undefined ? 'c' + d.c : d.h !== undefined ? 'h' + d.h : d.end ? 'e' + d.end : '?'; })()"
    def tl_settled(p, limit=10.0):                      # the board's own real-time redraw (it clears TL_GAME.fx) has happened; up to limit s
        for _ in range(int(limit * 10)):
            if p.ev('!TL_GAME || !TL_GAME.fx'): return True
            p.g.page.wait_for_timeout(100)
        return check(False, 'tiles: the board never redrew after its move (TL_GAME.fx still set after %g s)' % limit)
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
        tl_settled(p); p.step(3)   # (the move's animations end and the board redraws on its own real-time timer, which clears fx: wait for it, so it can't land mid-check)
        # the hold: A picks a tile in your hold, and the highlight keeps its place when the board redraws
        p.ev("TL_GAME.s.p = 0; TL_GAME.sel = null; TL_GAME.s.hold[0] = [1]; tilesDraw(); padFocusTo(TL_UI.root.querySelector('[data-h=\"1\"]'))"); p.step(2)
        p.press('a'); p.step(2)
        check(p.ev('TL_GAME.sel && TL_GAME.sel.h') == 1 and p.ev(TL_FOCUS) == 'h1', f'tiles: A on your hold should pick its tile and keep the highlight there ({p.ev(TL_FOCUS)})')
        p.press('up'); f = p.ev(TL_FOCUS); check(f and f[0] in 'ce', f'tiles: D-pad up from your hold should go back toward the board, not {f}')
        # the end: Again highlighted; along to Done, A
        p.ev("""(() => { const G = TL_GAME; G.sel = null; G.s.sc = [6, 0]; G.s.p = 0; let n = 0; while (!G.s.over && n++ < 80) { if (G.timer) { clearTimeout(G.timer); G.timer = 0; } if (G.s.p === 0) tilesDo(tilesAI(G.s, 'hard', G.rng)); else { const mv = tilesMoves(G.s, 1).find(m => !tilesApply(G.s, m).pts) || tilesMoves(G.s, 1)[0]; tilesDo(mv); } } if (G.timer) clearTimeout(G.timer); })()"""); p.step(3)
        tl_settled(p); p.step(3)   # (the board redraws on its own timer once its moves' animations end, clearing fx; the highlight follows a frame later)
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
        for ax in ([1, 0, 0, 0], [0, 1, 0, 0], [0, -1, 0, 0], [-1, 0, 0, 0]):   # a full push every way: Skip is to the right of Next, Leave below
            p.ev('DISC.g.p[0].x = 0'); p.axes(ax); p.step(12); p.axes([0, 0, 0, 0]); p.step(2)
            check(p.ev(LD_FOCUS) == 'next', f'disc: the stick pushed {ax[:2]} moved the highlight ({p.ev(LD_FOCUS)})')
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
    # ---- CP3 (claude/controller-p3 18e9032, + CP1's claude/controller 0251af41 in marks): marks, touch (here touch3), drop ----
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
        p4 = p.ev("typeof PAD_SET === 'object' && typeof padSetBind === 'function'")   # (with P4 built, its own settings; else stand-ins)
        p.ev("PAD_SET.marks = 'off'" if p4 else "window.padMarkFamily = () => null"); p.step(12)
        check(not any(a != 'padHint' for a, _ in marks(p)), f'marks: marks on the buttons with Off: {marks(p)}')
        p.ev("PAD_SET.marks = 'auto'; padSetBind('y', 'lb'); PAD.fam = 'xbox'" if p4 else "window.padMarkFamily = () => PAD.fam; window.padButtonFor = a => a === 'y' ? 'lb' : a; PAD.fam = 'xbox'"); p.step(2)
        check(marks(p).get(('devBtn', 'y')) == ('xbox:lb', True) and p.ev("document.querySelector('#devBtn > .padk').textContent") == 'LB', f'marks: Device should show LB after rebinding: {marks(p)}')
        p.ev("padSetBind('y', 'y')" if p4 else "delete window.padMarkFamily; delete window.padButtonFor"); p.step(12)
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
    def part_touch3(pw):
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
    # ---- CP4 (part_settings as merged in claude/controller fda82c1a, 0.90.8): settings ----
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
        if p.ev("typeof PAD_LAYOUTS === 'undefined'"): p.ev("window.PAD_LAYOUTS = { left: Object.fromEntries(PAD_BTN.map((n, i) => [n, PAD_BTN[(i + 1) % 16]])), right: Object.fromEntries(PAD_BTN.map(n => [n, n === 'a' ? 'rs' : n === 'rs' ? 'a' : n])) }")
        labels = p.ev("padSetView().blocks.flatMap(b => (b.items || []).map(i => i.label))")
        check('One hand: left' in labels and 'One hand: right' in labels, 'settings: the one-hand buttons should show with PAD_LAYOUTS')
        p.ev("deviceDo({ app: 'padsettings', do: 'hand', arg: 'right' })")
        check(p.ev("padButtonFor('a')") == p.ev("PAD_LAYOUTS.right.a") and p.ev('PAD_SET.sticks') is True and p.ev('PAD_SET.swap') is False, 'settings: One hand: right should set its map and swap the sticks')
        p.ev("deviceDo({ app: 'padsettings', do: 'hand', arg: 'left' })")
        check(p.ev("padButtonFor('a')") == p.ev("PAD_LAYOUTS.left.a") and p.ev('PAD_SET.sticks') is False, 'settings: One hand: left should set its map, sticks normal')
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

    # ---- CP5 (claude/controller-p5 4892a0b): a11y ----
    # P5 (accessibility, CP5): every button the highlight lands on has a name a screen reader can say: [] or the nameless
    # The names are the browser's own accessible names (CDP Accessibility.getPartialAXTree), not padSaid's guess; a name
    # with no letters in it (a mark alone: "✕", "+") counts as none.
    AX_ITEMS = """(() => {
      const L = padLayer(); if (!L) return null;
      window.__ax = padItems(L); window.__ax.forEach(e => padNameIt(e));
      return window.__ax.map(e => (e.id ? '#' + e.id : e.className ? '.' + String(e.className).split(' ')[0] : e.tagName) + ' ' + e.outerHTML.slice(0, 70));
    })()"""
    def nameless(p):
        """the buttons of the layer on top with no accessible name a screen reader can say, or None with no layer"""
        descr = p.ev(AX_ITEMS)
        if descr is None: return None
        if not hasattr(p, 'cdp'): p.cdp = p.g.page.context.new_cdp_session(p.g.page); p.cdp.send('Accessibility.enable')
        out = []
        for i, d in enumerate(descr):
            oid = p.cdp.send('Runtime.evaluate', {'expression': f'window.__ax[{i}]'})['result'].get('objectId')
            nodes = p.cdp.send('Accessibility.getPartialAXTree', {'objectId': oid, 'fetchRelatives': False})['nodes'] if oid else []
            name = str(((nodes[0].get('name') or {}).get('value')) if nodes else '' or '')
            if not re.search(r'[^\W\d_]', name or ''): out.append(f'{d} (heard: {name!r})')
        return out
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
        # the one-handed presets: each a whole shuffle of the buttons (every action on its own button), as P4's PAD_SET.map takes
        for side, m in p.ev('PAD_LAYOUTS').items():
            check(sorted(m) == sorted(BTN) and sorted(m.values()) == sorted(BTN), f'a11y: the one-handed {side} layout should give every action its own button: {m}')
        left = p.ev('PAD_LAYOUTS.left'); hand = {'up', 'down', 'left', 'right', 'lb', 'lt', 'view', 'ls'}
        check(all(left[k] in hand for k in ('a', 'b', 'x', 'y', 'menu', 'up', 'left', 'right')), f'a11y: the left-hand layout should put use, back, device, action, Pause and the D-pad on the left side: {left}')
        right = p.ev('PAD_LAYOUTS.right'); hand = {'a', 'b', 'x', 'y', 'rb', 'rt', 'menu', 'rs'}
        check(all(right[k] in hand for k in ('a', 'b', 'x', 'y', 'menu', 'up', 'left', 'right')), f'a11y: the right-hand layout should put use, back, device, action, Pause and the screen edge on the right side: {right}')
        # toasts are read out once the controller is in use
        check(p.ev("toastEl.getAttribute('role') === 'status' && toastEl.getAttribute('aria-live') === 'polite'"), 'a11y: the toast should be a polite live region once the pad is used')
        p.js("document.body.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))"); p.step(2)
        check(p.ev("!toastEl.hasAttribute('role') && !toastEl.hasAttribute('aria-live')"), 'a11y: a touch taking back should leave the toast as it was')
        p.press('x'); p.step(2)
        # the highlight: thick, teal, with a dark edge
        p.press('up'); p.step(2)
        st = p.ev("(() => { const c = getComputedStyle(document.activeElement); return [c.outlineWidth, c.outlineColor, c.outlineStyle, c.boxShadow]; })()")
        check(st[0] == '4px' and st[1] == 'rgb(76, 195, 181)' and st[2] == 'solid' and st[3].count('rgb(13, 21, 33)') == 2, f'a11y: the highlight should be a 4px teal outline with a dark edge on both sides (two dark shadows): {st}')
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
            p.step(3); r = nameless(p)
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
    # ---- CP4 (claude/controller-firstuse 3f6bb66, as merged in claude/controller fda82c1a): firstuse ----
    # the first use (lead 27, PR9's note): a stick that drifts at connect is not a use; a firm push held a moment is, a press at once
    def part_firstuse(pw):
        p = Pad(pw, ON)
        shape = "[PAD.used, PAD.lastUse > -1e9, document.body.classList.contains('pad'), document.querySelectorAll('style').length, document.body.children.length]"
        p.plug(); p.step(2); s0 = p.ev(shape)
        check(p.ev('PAD.listening') is False, 'firstuse: the touch hand-back listeners were added at hello, before any use')
        pos0 = p.ev('[player.obj.position.x, player.obj.position.z]')
        p.axes([.35, .12, -.3, .2]); p.step(45)                # past the dead zone, a gentle drift on both sticks for 1.5 s
        pos1 = p.ev('[player.obj.position.x, player.obj.position.z]')
        check(pos0 == pos1 and p.ev('player.steer') is None, f'firstuse: a drifting stick at connect walked the player: {pos0} -> {pos1}')
        check(p.ev(shape) == s0 and s0[0] is False and s0[1] is False, f'firstuse: a drifting stick at connect counted as a use: {s0} -> {p.ev(shape)}')
        view = "[camera.zoom, azT]"
        p.ev('setZoom(padZoom0())'); v0 = p.ev(view)
        p.btn('lt', .4); p.step(45); p.btn('lt', 0); p.step(1)  # a light, steady trigger for 1.5 s
        check(p.ev('PAD.used') is False, 'firstuse: a light trigger counted as a use')
        check(p.ev(view) == v0, f'firstuse: a light trigger before the first use moved the view: {v0} -> {p.ev(view)}')
        p.axes([0, 0, 0, .37]); p.step(45); p.axes([0, 0, 0, 0]); p.step(1)   # the right stick drifting down for 1.5 s
        check(p.ev(view) == v0, f'firstuse: a right-stick drift before the first use zoomed: {v0} -> {p.ev(view)}')
        p.axes([0, 0, 1, 0]); p.step(3); p.axes([0, 0, 0, 0]); p.step(1)    # a 0.1 s push sideways: not a use, so no turn
        check(p.ev(view) == v0 and p.ev('PAD.used') is False, f'firstuse: a short push before the first use turned the view: {v0} -> {p.ev(view)}')
        p.axes([1, 0, 0, 0]); p.step(3); u = p.ev('PAD.used')   # a firm push, 0.1 s: not yet
        p.step(3); v = p.ev('PAD.used'); p.axes([0, 0, 0, 0]); p.step(1)   # 0.2 s: a use
        check(u is False and v is True and 'pad' in p.ev('document.body.className'), f'firstuse: a firm push should count after about 0.15 s: {u} {v}')
        check(p.ev('PAD.listening') is True, 'firstuse: the first use should add the touch hand-back listeners')
        # handed back to touch: the drift doesn't take it back; a press does, at once
        p.js("document.body.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))")
        p.axes([.35, .12, 0, 0]); p.step(30); check(p.ev('PAD.used') is False, 'firstuse: a drifting stick took the screen back from touch')
        p.axes([0, 0, 0, 0]); p.btn('b'); p.step(1); check(p.ev('PAD.used') is True, 'firstuse: a press should count at once'); p.btn('b', 0); p.step(1)
        # in use: a gentle stick keeps it in use (lastUse moves on)
        t0 = p.ev('PAD.lastUse'); p.axes([.35, 0, 0, 0]); p.step(5); p.axes([0, 0, 0, 0]); p.step(1)
        check(p.ev('PAD.lastUse') > t0, 'firstuse: in use, a gentle stick should still count')
        p.close()
    return locals()
def legacy(name):
    """an old-shape part as a part of this check: GAME and ON are written from the build given (the switch-on copy, or
    a planted fault's copy), the part runs, and its failures (and any exception) are the list returned"""
    def run(pw, src, tag):
        fails = []
        off, on = WORK / 'test' / f'_old_{tag}_{name}_off.html', WORK / 'test' / f'_old_{tag}_{name}_on.html'
        off.write_text(with_switch(src, False)); on.write_text(with_switch(src, True))
        try: legacy_parts(str(off), on, fails)['part_' + name](pw)
        except Exception as e: fails.append(f'{type(e).__name__}: {e}')
        return fails
    return run
OLD_NEEDS = {'off': ['base'], 'quiet': ['base'], 'base': ['base'], 'deck': ['deck'], 'pick': ['pick'], 'panels': ['panels'], 'api': ['panels'],
             'lists': ['panels'], 'tiles': ['games'], 'disc': ['games'], 'screens': ['panels'], 'marks': ['marks'], 'touch3': ['marks'],
             'drop': ['marks'], 'settings': ['settings'], 'a11y': ['panels', 'pick'], 'firstuse': ['base']}
OLD_NAME = {'pick': 'pick1'}   # CT1's pick beside this check's own

# parts that need a package: 'not yet' until PAD_BUILT names it
NEEDS = {'touch': ['base'], 'walk': ['deck'], 'pick': ['pick'], 'reach': ['panels'], 'day': ['base', 'deck', 'pick', 'panels', 'games'],
         'games': ['games'], 'unplug': ['deck', 'marks'], 'odd': ['deck']}
PART_FN = {'idle': part_idle, 'save': part_save, 'calls': part_calls, 'walk': part_walk, 'touch': part_touch, 'unplug': part_unplug, 'odd': part_odd, 'pick': part_pick, 'reach': part_reach, 'games': part_games, 'day': part_day}   # 'reach' joins when the pad half is written
for k, v in OLD_NEEDS.items(): NEEDS[OLD_NAME.get(k, k)] = v; PART_FN[OLD_NAME.get(k, k)] = legacy(k)

# ---- planted faults --------------------------------------------------------------------------------------------------
# Each is put into a copy of the game just before the test hook (inside the game's scope). A part must FAIL on each of
# its own. Per-frame faults use the game's own requestAnimationFrame (the check's virtual clock drives it).
EACH_FRAME = "(() => { const f = () => { try { __BODY__ } catch (e) {} requestAnimationFrame(f); }; requestAnimationFrame(f); })();\n"
MUTANTS = {
    'idle': {
        'an invisible element on connect': "addEventListener('gamepadconnected', () => { const d = document.createElement('div'); d.style.display = 'none'; document.body.appendChild(d); });\n",
        'a style on connect': "addEventListener('gamepadconnected', () => { const s = document.createElement('style'); s.textContent = '.padX{}'; document.head.appendChild(s); });\n",
        'one random number on connect': "addEventListener('gamepadconnected', () => { R(); });\n",
        'walking on stick drift (no dead zone)': EACH_FRAME.replace('__BODY__', "const p = navigator.getGamepads()[0]; if (p && Math.abs(p.axes[0]) > .001) player.steer = { x: p.axes[0], z: p.axes[1], k: 1 };"),
        'the camera turned a hair on connect': "addEventListener('gamepadconnected', () => { az += 1e-3; });\n",
        'focus moved on connect': "addEventListener('gamepadconnected', () => { document.getElementById('rot').focus(); });\n",
    },
    'save': {
        'a pad record in every save': "SAVE_EXTRA.push(s => { if (navigator.getGamepads().some(p => p)) s.pad = {}; });\n",
        'a separate storage key on connect': "addEventListener('gamepadconnected', () => { try { localStorage.setItem('starship-cadet-pad', '{}'); } catch (e) {} });\n",
    },
    'calls': {
        'a hidden-in-plain-sight ring mesh on connect': "addEventListener('gamepadconnected', () => { const m = new THREE.Mesh(new THREE.RingGeometry(.3, .4, 16), new THREE.MeshBasicMaterial({ color: 0x00ffff })); m.rotation.x = -Math.PI / 2; m.position.y = .02; scene.add(m); });\n",
    },
}
def plant(src, code):
    # a fault is JS added beside the game, or ('src', old, new): a change inside section 26 itself (a reviewer's fault), or
    # a list of those, all planted together
    if isinstance(code, list):
        for c in code: src = plant(src, c)
        return src
    if isinstance(code, tuple):
        if src.count(code[1]) != 1: raise ValueError('cannot be planted in this build (its line is not there once)')
        return src.replace(code[1], code[2])
    i = src.rfind('})();')
    return src[:i] + '\n// planted by controller_check --mutants\n' + code + src[i:]

MUTANTS['walk'] = {
    'the stick upside down': WRAP("axes[1] = -axes[1];"),
    'the view turn forgotten (the stick in the first view\'s directions)': WRAP("const t = az - Math.PI / 4, c = Math.cos(t), s = Math.sin(t), x = axes[0], y = axes[1]; axes[0] = x * c - y * s; axes[1] = x * s + y * c;"),
    'the stick sticks after letting go': WRAP("if (Math.abs(axes[0]) + Math.abs(axes[1]) > .2) { mem = [axes[0], axes[1]]; n = 20; } else if (n > 0) { n--; axes[0] = mem[0]; axes[1] = mem[1]; }"),
    'LB turns the same way as RB': WRAP("if (buttons[4].pressed) { buttons[5] = buttons[4]; buttons[4] = { pressed: false, touched: false, value: 0 }; }"),
    'Menu does nothing': WRAP("buttons[9] = { pressed: false, touched: false, value: 0 };"),
    'zoom goes past the limit': EACH_FRAME.replace('__BODY__', "if (camera.zoom >= ZOOM_MAX - 1e-9 && navigator.getGamepads()[0] && navigator.getGamepads()[0].buttons[7].value > .5) { camera.zoom = ZOOM_MAX * 1.1; camera.updateProjectionMatrix(); }"),
}

MUTANTS['touch'] = {
    'a focus outline left on Rotate': EACH_FRAME.replace('__BODY__', "const p = navigator.getGamepads()[0]; if (p && p.buttons.some(b => b.pressed)) { const e = document.getElementById('rot'); e.focus(); e.style.outline = '3px solid #4cc3b5'; }"),
    'a button picture that stays after touch': "addEventListener('gamepadconnected', () => {}); (() => { const f = () => { requestAnimationFrame(f); const p = navigator.getGamepads()[0]; if (p && p.buttons.some(b => b.pressed) && !document.getElementById('padMk')) { const d = document.createElement('b'); d.id = 'padMk'; d.textContent = 'Y'; d.style.cssText = 'position:fixed;left:10px;bottom:90px;color:#fff;font-size:20px;z-index:9'; document.body.appendChild(d); } }; requestAnimationFrame(f); })();\n",
}
MUTANTS['unplug'] = {
    'walking goes on after the unplug': "addEventListener('gamepaddisconnected', () => { player.steer = { x: 1, z: 0, k: 1 }; });\n",
    'no pause on the unplug': "addEventListener('gamepaddisconnected', () => { setTimeout(() => {}, 0); requestAnimationFrame(() => pauseSet(false)); });\n",
    'the pause card without its line': EACH_FRAME.replace('__BODY__', "const c = document.getElementById('pauseCard'); if (c) for (const e of c.querySelectorAll('*')) if (e.children.length === 0 && /Controller disconnected/.test(e.textContent)) e.textContent = '';"),
}
MUTANTS['odd'] = {
    'a non-standard pad ignored': WRAP("if (p.mapping !== 'standard') return null;").replace("if (!p) return p;", "if (!p || p.mapping !== 'standard') return null;"),
    'only the first pad listened to': WRAP("").replace("if (!p) return p;", "if (!p || p.index > 0) return null;"),
}

# PR9's faults in section 26 itself (plans/review-9/ct_mutants.py on claude/review-8), for builds that have those lines
MUTANTS['idle']['PR9 c6: a hidden ring mesh made at load'] = ('src', "if (PAD_ON) { addEventListener('gamepadconnected', padHello);", "if (PAD_ON) { const _pr = new THREE.Mesh(new THREE.RingGeometry(.4, .5, 40), new THREE.MeshBasicMaterial({ color: col('#4cc3b5') })); _pr.visible = false; scene.add(_pr); addEventListener('gamepadconnected', padHello);")
MUTANTS['walk']['PR9 c1: the stick walks the wrong way'] = ('src', "const wx = rx * x - fx * y, wz = rz * x - fz * y", "const wx = rx * x + fx * y, wz = rz * x + fz * y")
MUTANTS['walk']['PR9 c2: letting go keeps walking'] = ('src', "function padWalkEnd() { if (PAD_DECK.walking) { PAD_DECK.walking = false; if (!steering) player.steer = null; } }", "function padWalkEnd() { if (PAD_DECK.walking) { PAD_DECK.walking = false; } }")
MUTANTS['walk']['PR9 c3: the device missing from the panel list'] = ('src', "['dmSheet', () => DM_UI.open], ['device', () => DEV.open], ", "['dmSheet', () => DM_UI.open], ")
MUTANTS['touch']['PR9 c4: a touch does not hand back'] = ('src', "addEventListener('pointerdown', back, true); ", "")
MUTANTS['pick'] = {
    'PR9 c7: a seat ringed where the tap reaches a person': ('src', "if (a) return 'crew:' + a.p.id;", "if (a && !(want && want.startsWith('place:'))) return 'crew:' + a.p.id;"),
    'RV2 t3_noop_crew: A ignores crew': ('src', "  if (!s) return true;\n  P.chosen = false; tap(s[0], s[1]);", "  if (!s || t.key.startsWith('crew:')) return true;\n  P.chosen = false; tap(s[0], s[1]);"),
    'RV2 t3_noface: facing ignored': ('src', "const fx = Math.sin(player.face || 0), fz = Math.cos(player.face || 0);", "const fx = 0, fz = 0;"),
    'PR9 c5: A does nothing': ('src', "P.chosen = false; tap(s[0], s[1]); P.n = 0;", "P.chosen = false; P.n = 0;"),
    'A and B swapped': WRAP("const t = buttons[0]; buttons[0] = buttons[1]; buttons[1] = t;"),
    'the bottom line names the wrong thing': EACH_FRAME.replace('__BODY__', "const h = document.getElementById('padHint'); if (h && !h.hidden && h.textContent !== 'A Something') h.textContent = 'A Something';"),
    'A steps the player a tile before tapping': WRAP("if (buttons[0].pressed) { player.obj.position.x += .5; }"),
}

MUTANTS['reach'] = {
    'the D-pad skips the device\'s Home key': EACH_FRAME.replace('__BODY__', "if (document.activeElement && document.activeElement.id === 'devHome') document.getElementById('devBack').focus();"),
    'A clicks the panel, not the highlighted thing': WRAP("if (buttons[0].pressed && document.activeElement && document.activeElement !== document.body) { buttons[0] = { pressed: false, touched: false, value: 0 }; const d = document.activeElement.closest('[role=dialog],.lift,.device'); if (d) d.click(); }"),
}

MUTANTS['games'] = {
    'A does nothing on the Tiles board': WRAP("if (document.activeElement && document.activeElement.closest && document.activeElement.closest('.tl-bd')) buttons[0] = { pressed: false, touched: false, value: 0 };"),
    # (the pad's left stick reads still while Lightdisc is open: a fault in the input, whoever reads it; zeroing DISC.inp
    # once a frame missed a driver that sets it later in the same frame)
    'the stick does not move you in Lightdisc': WRAP("if (typeof DISC !== 'undefined' && DISC.view) { axes[0] = 0; axes[1] = 0; }"),
    'B does not leave Lightdisc': WRAP("if (typeof DISC !== 'undefined' && DISC.view) buttons[1] = { pressed: false, touched: false, value: 0 };"),
}
# the builders' own planted faults for their old-shape parts (each line once in the builder's game at its tip)
MUTANTS['marks'] = {   # CP3, claude/controller-p3 18e9032
  'marks shown without the pad in use': ('src', "'body.pad .padk{display:inline-flex}", "'.padk{display:inline-flex}body.pad .padk{display:inline-flex}"),
  'Nintendo marks in Xbox places': ('src', "nin: { a: ['B', '#e6f0f1', 'B'], b: ['A', '#e6f0f1', 'A'],", "nin: { a: ['A', '#e6f0f1', 'A'], b: ['B', '#e6f0f1', 'B'],"),
  'Controller connected over another message': ('src', "if (PAD_MARK.say && PAD.used && !toastEl.classList.contains('show')) {", "if (PAD_MARK.say && PAD.used) {"),
}
MUTANTS['touch3'] = {
  'the ring left up after a touch': [('src', "  if (!free) { if (P.ring) padPickShow(false); P.n = 0;", "  if (!free) { P.n = 0;"), ('src', "padOn('unuse', () => { if (PAD_PICK.ring) padPickShow(false); });", "")],
}
MUTANTS['drop'] = {
  'no pause after a drop-out': ('src', "if (PAD.goneUsed && !PAUSE.on) {", "if (false) {"),
  'the card keeps saying disconnected': ('src', "else if (!on && PAD_MARK.line) {", "else if (false) {"),
}
# CT1's old parts (off quiet base deck pick1), RV5's C3: faults written by CTT2 from section 26's own lines
MUTANTS['off'] = {
  'the switch ignored: a hello with PAD_ON off': ('src', "if (PAD_ON) { addEventListener('gamepadconnected', padHello);", "if (true) { addEventListener('gamepadconnected', padHello);"),
}
MUTANTS['quiet'] = {
  'an element made at load with the switch on': "if (PAD_ON) document.body.appendChild(document.createElement('i'));\n",
}
MUTANTS['base'] = {
  'the D-pad repeats too soon': ('src', "const PAD_REP = { first: .5, every: .25 };", "const PAD_REP = { first: .25, every: .25 };"),
  'a touch does not hand back': ('src', "addEventListener('pointerdown', back, true); ", ""),
  'two pads: the last to press is not in charge': ('src', "  for (const g of pads) if (g.index !== PAD.idx && g.buttons.some(b => b && b.pressed)) { padRelease(); PAD.idx = g.index; }", ""),
}
MUTANTS['deck'] = {k: MUTANTS['walk'][k] for k in ('PR9 c1: the stick walks the wrong way', 'PR9 c2: letting go keeps walking')}
MUTANTS['pick1'] = {k: MUTANTS['pick'][k] for k in ('PR9 c5: A does nothing', 'RV2 t3_noop_crew: A ignores crew')}
# CP1, claude/controller-p1 cff5bab (and claude/controller 5ae76569, 0.90.3)
MUTANTS['api'] = {
  'panel order lost': ('src', "  if (at < 0) PAD_PANELS.push(row); else PAD_PANELS.splice(at, 0, row);", "  PAD_PANELS.push(row);"),
  'a touch after the pad keeps the focus': ('src', "  const F = PAD_FOCUS, a = document.activeElement; if (F.el && a === F.el && a.blur) a.blur();", "  const F = PAD_FOCUS, a = document.activeElement;"),
  'same row not first': ('src', "  return row || best;", "  return best;"),
}
MUTANTS['panels'] = {
  'B in the device does nothing': ('src', "  device: () => { if (DEV.app && DEV.app !== 'home') deviceShow('home'); else deviceClose(); },", "  device: () => {},"),
  'the address card unreachable': ('src', "#ixBoard, #seek, #devHu, #devHu button, #devAddr, #devTip';", "#ixBoard, #seek, #devHu, #devHu button, #devTip';"),
}
MUTANTS['lists'] = {
  'B in a text box leaves the panel too': ('src', "if (a && /^(INPUT|TEXTAREA|SELECT)$/.test(a.tagName) && L.contains && L.contains(a)) { PAD_FOCUS.last = null; a.blur(); return; }", "if (false) { }"),
  'RT does not page': ('src', "padOn('rt', e => { const L = padLayer(); if (!L) return; if (!padOwnDo('rt', L, e)) padScroll(innerHeight * .6); return true; });", "padOn('rt', e => { const L = padLayer(); if (!L) return; return true; });"),
}
MUTANTS['settings'] = {   # CP4, claude/controller-p4 7631ab6
  'an unchanged save writes s.pad': ('src', "SAVE_EXTRA.push(s => { const d = padSetDiff(); if (d) s.pad = d; });   // nothing changed: nothing written", "SAVE_EXTRA.push(s => { s.pad = padSetDiff() || {}; });"),
  'the stick swap not loading': ('src', "    if (d.sticks === true) S.sticks = true;", "    if (d.sticks === true) S.sticks = false;"),
  'the button map not saving': ('src', "  if (Object.keys(S.map).length) d.map = Object.assign({}, S.map);", "  if (false) d.map = Object.assign({}, S.map);"),
  'gentle walking lost': ('src', "    if (PAD_SET.walk === 'gentle' && PAD_DECK.walking && player.steer && !steering) player.steer.k = Math.min(player.steer.k, .6);", "    // gentle walking lost (planted)"),
  'an odd save loading as it is': ('src', "    const all = PAD_BTN.map(n => S.map[n] || n); if (new Set(all).size !== all.length) S.map = {};   // not one button each: back to normal", "    // odd maps kept (planted)"),
  'a clash not swapping': ('src', "  const phy = Object.assign({}, PAD_PHY), k = PAD_BTN.indexOf(b), other = PAD_MAPK[k]; if (k < 0 || other === n) return;", "  const phy = Object.assign({}, PAD_PHY), k = PAD_BTN.indexOf(b), other = PAD_MAPK[k]; if (k < 0 || other === n || true) return;"),
  'padTick ignoring the map': ('src', "    const n = PAD_MAPK[k], b = bt[k], trig = k === 6 || k === 7,", "    const n = PAD_BTN[k], b = bt[k], trig = k === 6 || k === 7,"),   # (the line as in 0.90.8)
}
# CP2, claude/controller-p2 7b11451 (the game as 5b4d9f0)
MUTANTS['disc'] = {
  'no full range: a light push is a full one': ('src', "    if (play) { const [x, y] = PAD.ls; if (x || y || PAD_LD.stick) { inp.kx = x; inp.kz = y; PAD_LD.stick = !!(x || y); } }   // a let-go stops you, once", "    if (play) { const [x, y] = PAD.ls; if (x || y || PAD_LD.stick) { inp.kx = Math.sign(x); inp.kz = Math.sign(y); PAD_LD.stick = !!(x || y); } }   // a let-go stops you, once"),
  'the stick also moves the highlight': ('src', "    return play;                                           // (while you play the stick is yours, not the highlight's)", "    return false;                                          // (while you play the stick is yours, not the highlight's)"),
  'A presses Leave by itself': ('src', "    if (a && V.root.contains(a) && padShown(a) && (a !== V.leave || PAD_LD.chose)) { a.click(); return true; }", "    if (a && V.root.contains(a) && padShown(a)) { a.click(); return true; }"),
}
MUTANTS['tiles'] = {
  'the highlight never lands': ('src', "  if (to && to !== a) padFocusTo(to);", "  if (to && to !== a && !to) padFocusTo(to);"),
  'a redraw loses your place': ('src', "  const to = !T.shown || over && !T.over ? padTlLand() : lost ? padTlFind(T.key) || padTlLand() : null;   // arriving, the game ending, a redraw", "  const to = !T.shown || over && !T.over ? padTlLand() : lost ? padTlLand() : null;   // arriving, the game ending, a redraw"),
}
MUTANTS['screens'] = {
  'a question card lands on the x': ('src', "PAD_FIRST.devDlg = '#devDlg .act';", "PAD_FIRST.devDlg = '#devDlg';"),
  'B on a question does nothing': ('src', "  b: () => { const x = document.querySelector('#devDlg button.x'); if (x) x.click(); return true; },", "  b: () => true,"),
  'a turn card asking again loses the place': ('src', "  const was = PAD_FOCUS.last;", "  const was = null;"),   # (replaces P2's dead-code fault; the line is P1's)
  'the alarm lands on minus': ('src', "PAD_FIRST.sleepAsk = '#sleepYes';                         // the alarm: Set alarm first (− and + a press away), as the lift lands on your goal deck", "PAD_FIRST.sleepAsk = '#alarmDn';"),
  'no suggested name': ('src', "  box.value = PAD_NAME; return true;                       // shown in the box first; A again signs", "  return;"),
  'the manifest is never a panel': ('src', "padOn('frame', () => { const m = PAD.used && INTRO_UI.manifest; if (m && !m.id) m.id = 'introManifest'; });", "padOn('frame', () => {});"),
}
MUTANTS['a11y'] = {   # CP5, claude/controller-p5 4892a0b
  'outline 3px': ('src', "outline:4px solid #4cc3b5!important;outline-offset:3px", "outline:3px solid #4cc3b5!important;outline-offset:3px"),
  'one dark shadow, not two': ('src', "box-shadow:0 0 0 3px #0d1521,0 0 0 9px #0d1521!important", "box-shadow:0 0 0 3px #0d1521!important"),
  'padStill false': ('src', "  return !!(A.rmq && A.rmq.matches);", "  return false;"),
  'no toast role': ('src', "  if (!toastEl.hasAttribute('role')) { toastEl.setAttribute('role', 'status'); PAD_A11Y.toast.push('role'); }", "  if (0) { }"),
  'the toast role kept after a touch': ('src', "toastEl.removeAttribute(a);", "void a;"),
  "Maps' deck buttons nameless": ('src', "'Deck ' + el.textContent.trim() : ''", "''"),
  'one-handed layout broken': ('src', "lb: 'x', lt: 'y', down: 'b', view: 'menu', ls: 'a' },", "lb: 'x', lt: 'y', down: 'b', view: 'menu', ls: 'lt' },"),
}

# ---- the stand-in (--selftest) ----------------------------------------------------------------------------------------
# A tiny controller driver written for this check alone, planted in a copy of the game, so each part can be shown to
# PASS on something that works and FAIL on its planted faults before section 26 exists. It is not the design: section 26
# is CT1's. It covers what's built in the parts here so far (the deck package).
STANDIN = r"""
const PAD_ON = true;
const PAD_BUILT = ['base', 'deck', 'marks', 'panels', 'games'];
(() => {
  if (!PAD_ON) return;
  const prev = {}; let steering = false, flick = 0, charge = null, used = -1e9;
  const usual = () => innerWidth / innerHeight < .8 ? 1.62 : 1.22;
  const stop = () => { if (steering) { player.steer = null; steering = false; } };
  addEventListener('gamepaddisconnected', e => {
    const i = e.gamepad.index; delete prev[i];
    if (charge !== null && charge !== i) return;
    charge = null; stop();
    if (performance.now() - used < 30000) { pauseSet(true); const c = document.getElementById('pauseCard');
      if (c && !document.getElementById('padLine')) { const l = document.createElement('p'); l.id = 'padLine'; l.textContent = 'Controller disconnected'; l.style.cssText = 'position:absolute;bottom:20%;color:#fff'; c.appendChild(l); } }
  });
  const f = () => {
    requestAnimationFrame(f);
    const pads = [...navigator.getGamepads()].filter(x => x && x.connected); if (!pads.length) return;
    for (const q of pads) if (q.buttons.some((b, k) => b.pressed && !(prev[q.index] || [])[k])) charge = q.index;
    const p = pads.find(q => q.index === charge) || pads.find(q => Math.hypot(q.axes[0] || 0, q.axes[1] || 0) > .2) || pads[0];
    const pv = prev[p.index] || [];
    // panels (a simple stand-in): the top open panel's buttons; the D-pad to the nearest one that way, A clicks, B backs
    const top = [...document.querySelectorAll('#pauseCard,[role=dialog],.lift,.device')].filter(e => !e.hidden && e.getBoundingClientRect().width > 0 && getComputedStyle(e).display !== 'none').pop();
    const hitp = k => !!(p.buttons[k] && p.buttons[k].pressed) && !pv[k];
    if (typeof DISC !== 'undefined' && DISC.view && DISC.g) {   // Lightdisc (a stand-in): the stick moves you, A is Next, B leaves
      const sx = p.axes[0] || 0; DISC.inp.kx = Math.abs(sx) > .2 ? sx : 0;
      if (hitp(0)) { const n = DISC.view.howNext; if (n && n.offsetParent) n.click(); }
      if (hitp(1) && DISC.view.leave) DISC.view.leave.click();
      for (const q of pads) prev[q.index] = q.buttons.map(b => b.pressed);
      return;
    }
    if (top && !hitp(3) && !hitp(8) && !hitp(9)) {   // Y, View and Menu keep their own jobs
      const btns = [...top.querySelectorAll('button,[role=button],a[href],input,select,textarea,[tabindex]')].filter(e => !e.disabled && e.getBoundingClientRect().width > 0 && (!e.checkVisibility || e.checkVisibility()));
      const cur = top.contains(document.activeElement) ? document.activeElement : null;
      const go = (dx, dy) => { const c = cur ? cur.getBoundingClientRect() : { left: 0, top: 0, width: 0, height: 0 }, cx = c.left + c.width / 2, cy = c.top + c.height / 2;
        let best = null, bd = 1e9; for (const e of btns) { if (e === cur) continue; const b = e.getBoundingClientRect(), x = b.left + b.width / 2 - cx, y = b.top + b.height / 2 - cy;
          const along = x * dx + y * dy, side = Math.abs(x * dy - y * dx); if (cur && along <= 1) continue; const d = along + 2 * side; if (d < bd) { bd = d; best = e; } }
        if (best) best.focus(); };
      if (!cur && btns[0] && [12, 13, 14, 15].some(hitp)) btns[0].focus();
      else { if (hitp(12)) go(0, -1); if (hitp(13)) go(0, 1); if (hitp(14)) go(-1, 0); if (hitp(15)) go(1, 0); }
      if (hitp(0) && cur) cur.click();
      if (hitp(1)) { const bk = document.getElementById('devBack'); if (top.id === 'device' && bk && bk.getBoundingClientRect().width > 0 && DEV.app !== 'home') bk.click(); else document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true })); }
      for (const q of pads) prev[q.index] = q.buttons.map(b => b.pressed);
      return;
    }
    const B = k => !!(p.buttons[k] && p.buttons[k].pressed), V = k => p.buttons[k] ? p.buttons[k].value : 0, hit = k => B(k) && !pv[k];
    const sx = p.axes[0] || 0, sy = p.axes[1] || 0, m = Math.hypot(sx, sy);
    if (m > .2 || p.buttons.some(b => b.pressed)) used = performance.now();
    if (m > .2) { const k = Math.min(1, (m - .2) / .8), fx = -Math.sin(az), fz = -Math.cos(az), rx = Math.cos(az), rz = -Math.sin(az);
      const wx = rx * sx - fx * sy, wz = rz * sx - fz * sy, wl = Math.hypot(wx, wz); player.steer = { x: wx / wl, z: wz / wl, k }; steering = true; }
    else stop();
    if (hit(4)) azT -= Math.PI / 2; if (hit(5)) azT += Math.PI / 2;
    const rx = p.axes[2] || 0; if (Math.abs(rx) > .6 && !flick) { azT += Math.sign(rx) * Math.PI / 2; flick = 1; } else if (Math.abs(rx) < .3) flick = 0;
    const z = V(7) - V(6) - ((Math.abs(p.axes[3] || 0) > .2) ? p.axes[3] : 0); if (Math.abs(z) > .05) setZoom(camera.zoom * (1 + .03 * z));
    if (hit(11)) setZoom(usual());
    if (hit(9)) { pauseSet(!PAUSE.on); if (!PAUSE.on) { const l = document.getElementById('padLine'); if (l) l.remove(); } }
    if (hit(3)) { if (DEV.open) deviceClose(); else document.getElementById('devBtn').click(); }
    if (hit(8)) trkOpen();
    for (const q of pads) prev[q.index] = q.buttons.map(b => b.pressed);
  };
  requestAnimationFrame(f);
})();
"""

# ---- run ----------------------------------------------------------------------------------------------------------
if '--selftest' in FLAGS:
    if pad_switch(SRC) is not None: print('--selftest is for a build without section 26 (it plants its own PAD_ON)'); sys.exit(1)
    SRC = plant(SRC, STANDIN); print('--selftest: the parts run on a copy with the check\'s own stand-in driver (not section 26)')
built, built_how = pad_built(SRC)
if os.environ.get('CTL_BUILT'):   # a builder's branch before its package is on the PAD_BUILT line: CTL_BUILT=marks,settings
    built |= set(os.environ['CTL_BUILT'].split(',')); built_how += ', plus ' + os.environ['CTL_BUILT'] + ' from CTL_BUILT'
print(f'controller_check on {GAME}: PAD_ON {pad_switch(SRC)}, packages built: {sorted(built) or "none"} ({built_how})')
# the parts that play with the pad run on the switch-on copy (idle, save and calls test both themselves)
ON_SRC = both_builds(SRC)[-1][1]
SELF_BOTH = {'idle', 'save', 'calls'}
with sync_playwright() as pw:
    br = pw   # each Run launches its own browser
    for part in PARTS:
        print(f'[{part}]')
        if part not in PART_FN and NEEDS.get(part) and all(p in built for p in NEEDS[part]):
            # the package is there, the part isn't: never a pass
            check(False, f'{part}: its package is built ({", ".join(NEEDS[part])}) but this check has no part for it yet')
            RESULTS.append((part, 'FAIL', 'package built, part not written yet')); continue
        if part not in PART_FN or any(p not in built for p in NEEDS.get(part, [])):
            missing = [p for p in NEEDS.get(part, []) if p not in built]
            if part == 'reach' and '--inventory' in FLAGS:   # the touch half alone: what there is to reach, read from the page
                for f in part_reach(br, ON_SRC, 'g'): check(False, f'reach (touch half): {f}')
            note = f'waits for package{"s" if len(missing) > 1 else ""} {", ".join(missing)}' if missing else 'built in this check later'
            print(f'  not yet ({note})'); RESULTS.append((part, 'not yet', note)); continue
        psrc = SRC if part in SELF_BOTH else ON_SRC
        fails = PART_FN[part](br, psrc, 'g')
        for f in fails: check(False, f'{part}: {f}')
        RESULTS.append((part, 'FAIL' if fails else 'OK', f'{len(fails)} problems' if fails else ''))
        if '--mutants' in FLAGS:
            for name, code in MUTANTS.get(part, {}).items():
                if os.environ.get('CTL_MUT') and not re.search(os.environ['CTL_MUT'], name): continue   # only the planted faults named (a regex)
                # caught only by a failure the clean run didn't have (a part already failing proves nothing)
                norm = lambda f: re.sub(r'-?[\d.]+', 'N', f)   # the same failure with other numbers is the same failure
                try: msrc = plant(psrc if part not in SELF_BOTH else SRC, code)
                except ValueError as e: print(f'  planted fault "{name}": {e}'); RESULTS.append((part + ' mutant', 'n/a', name)); continue
                mf = [f for f in PART_FN[part](br, msrc, 'm') if norm(f) not in {norm(x) for x in fails}]
                caught = bool(mf)
                print(f'  planted fault "{name}": {"caught (" + mf[0][:110] + ")" if caught else "NOT CAUGHT"}')
                check(caught, f'{part}: the planted fault "{name}" was not caught')
                RESULTS.append((part + ' mutant', 'OK' if caught else 'FAIL', name))

print('Summary:')
for p, res, note in RESULTS: print(f'  {p:16s} {res:8s} {note}')
ny = [p for p, res, _ in RESULTS if res == 'not yet']
print(('CONTROLLER CHECK OK' + (f' (not yet: {", ".join(ny)})' if ny else '')) if ok else 'CONTROLLER CHECK FAILED')
sys.exit(0 if ok else 1)
