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
# Setup and environment as for cadet_test.py (CADET_WORK, CADET_CHROME=/opt/pw-browsers/chromium).
# Run:  python3 controller_check.py BUILD.html [part ...] [--mutants]
import sys, json, re, os, pathlib
exec(open(__file__.replace('controller_check.py', 'cadet_test.py')).read().split("a, shots = run(")[0])

ARGS = [a for a in sys.argv[1:] if not a.startswith('--')]
FLAGS = {a for a in sys.argv[1:] if a.startswith('--')}
GAME = pathlib.Path(ARGS[0])
ALL_PARTS = ['idle', 'save', 'calls', 'touch', 'walk', 'pick', 'reach', 'day', 'games', 'unplug', 'odd']
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
    plug(i, o) { slots[i] = mk(i, o || {}); fire('gamepadconnected', slots[i]); },
    unplug(i) { const p = slots[i]; if (!p) return; p.connected = false; slots[i] = null; fire('gamepaddisconnected', p); },
    // b: { index: value 0..1 } (pressed above .5 for the face buttons, any value for the triggers), a: { index: value }
    set(i, b, a) { const p = slots[i]; if (!p) return; for (const k in (b || {})) { const v = +b[k]; p.buttons[k] = { pressed: v > .1, touched: v > 0, value: v }; }
      for (const k in (a || {})) p.axes[k] = +a[k]; p.timestamp = performance.now(); },
    clear(i) { const p = slots[i]; if (!p) return; p.axes.fill(0); p.buttons.forEach((b, k) => p.buttons[k] = { pressed: false, touched: false, value: 0 }); p.timestamp = performance.now(); },
  };
  Object.defineProperty(Navigator.prototype, 'getGamepads', { configurable: true, value: function () { window.__pads.reads++; return slots.map(p => p && copy(p)); } });
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
def pad_built(src):
    m = re.search(r'\bconst PAD_BUILT\s*=\s*\[([^\]]*)\]', src)
    return set() if not m else set(re.findall(r"['\"](\w+)['\"]", m.group(1)))

ok = True
RESULTS = []   # (part, 'OK' | 'FAIL' | 'not yet', note)
def check(cond, msg):
    global ok
    if not cond: ok = False; print('FAIL', msg)
    return cond

QUIET = '#toast,.nf{opacity:0!important} #needFx{display:none!important} #devHu{display:none!important} #needStrip{display:none!important} #devBtn{box-shadow:none!important} *,*::before,*::after{transition:none!important;animation:none!important}'
class Run:
    """One page of the game with the pretend controller in a given mode. extra: JS put into the game's scope at load."""
    def __init__(self, br, src, tag, mode='none', plug=None, w=900, h=760, query='?nosave&debug', storage=None):
        self.errors = []
        # a browser of its own for every run, as cadet_test does: a second page in one browser sometimes drew a speech
        # bubble's layer differently (the same styles and DOM, different pixels), a browser quirk, not the game
        self.br = br.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=ARGS_GL)
        self.ctx = self.br.new_context(viewport={'width': w, 'height': h}, device_scale_factor=1)
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
    def reload(self):
        self.page.reload()
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
  window.__census = { tagged, counts };
})();
"""
PAGE_STATE = r"""(() => {
  let h = 0; const mix = s => { for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) | 0; };
  let n = 0; for (const e of document.querySelectorAll('*')) { n++; mix(e.tagName + '|' + e.id + '|' + e.className + '|' + (e.getAttribute('style') || '') + '|' + (e.hidden ? 'h' : '') + (e === document.activeElement ? 'F' : '')); for (const c of e.childNodes) if (c.nodeType === 3) mix(c.textContent); }
  let rules = 0; for (const s of document.styleSheets) { try { rules += s.cssRules.length; } catch (e) {} }
  const ls = []; try { for (let i = 0; i < localStorage.length; i++) { const k = localStorage.key(i); ls.push(k + '=' + localStorage.getItem(k).length); } } catch (e) {}
  return { elements: n, domHash: h, sheets: document.styleSheets.length, rules, storage: ls.sort(), listeners: window.__census.counts, focus: document.activeElement && (document.activeElement.id || document.activeElement.tagName) };
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

IDLE_MODES = [('none', 'no pad again (the check is steady)', None), ('api', 'the pad API with no pad', None), ('idle', 'a pad plugged in, never pressed', {}), ('drift', 'a drifting pad, never pressed', {'drift': True})]
def part_idle(br, src, tag):
    """FAIL lines for: every idle mode (and PAD_ON on, if there is a switch) against the game with no pad."""
    fails = []
    builds = [('off', src)]
    sw = pad_switch(src)
    if sw is not None: builds = [('off', with_switch(src, False)), ('on', with_switch(src, True))]
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
def part_save(br, src, tag):
    fails = []
    base = save_text(br, src, f'{tag}_save_none', 'none', None)
    print(f'  storage with no pad (the save and everything else kept): {len(base or "")} bytes')
    if not base: return ['no save was written with no pad']
    for mode, what, plug in IDLE_MODES[1:]:
        t = save_text(br, src, f'{tag}_save_{mode}', mode, plug)
        same = t == base
        print(f'  {what}: {"byte-identical" if same else "DIFFERENT"} ({len(t or "")} bytes)')
        if not same:
            a, b = json.loads(base), json.loads(t or '{}')
            fails.append(f'save with {what} differs: ' + '; '.join(diff_state(a, b)[:4]))
    return fails

def part_calls(br, src, tag):
    fails = []
    for (name, w, h) in [('phone', 390, 844), ('wide', 1280, 800)]:
        got = {}
        for mode, plug in [('none', None), ('idle', {}), ('drift', {'drift': True})]:
            r = Run(br, src, f'{tag}_calls_{name}_{mode}', mode=mode, plug=plug, w=w, h=h)
            r.step(60); g = r.ev(GAME_STATE); r.close()
            got[mode] = [g['calls'], g['tris'], g['mem']['geometries'], g['mem']['textures'], g['scene']]
        print(f'  {name} {w}x{h}: draw calls, triangles, geometries, textures, scene objects: ' + ', '.join(f'{m} {v}' for m, v in got.items()))
        for m in ('idle', 'drift'):
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
    const own = (e.getAttribute('aria-label') || e.textContent || e.value || e.title || '').replace(/\s+/g, ' ').trim().slice(0, 40);
    let key = e.id ? '#' + e.id : (a && a.id ? '#' + a.id + ' ' : '') + e.tagName.toLowerCase() + (e.className && typeof e.className === 'string' ? '.' + e.className.trim().split(/\s+/)[0] : '') + '[' + own + ']';
    const n = (seen.get(key) || 0) + 1; seen.set(key, n); if (n > 1) key += '#' + n;
    const d = e.closest('[role=dialog],[aria-modal=true],.lift,.device,dialog');
    out.push({ k: key, x: at[0], y: at[1], why: ['', 'tag', 'click', 'listener', 'cursor'][k], dlg: d ? (d.id || d.className) : null, label: own });
  }
  const dlg = [...document.querySelectorAll('[role=dialog],[aria-modal=true],.lift,.device,dialog')].filter(e => !e.closest('[hidden]') && e.getBoundingClientRect().width > 0 && (!e.checkVisibility || e.checkVisibility({ opacityProperty: true, visibilityProperty: true }))).map(e => e.id || e.className);
  return { items: out, dialogs: dlg, url: location.href };
})()"""

class Sweep:
    """The touch half of the reachability sweep: from the deck and from every panel it can open, press every clickable
    by mouse (a real click at its middle, as a finger would) and record each screen state reached: the pressable things
    in it, read from the page. Back to the state before with Escape, else by reloading and replaying the presses."""
    MAX_DEPTH, MAX_PRESSES = 4, int(os.environ.get('CTL_PRESSES', 700))
    SKIP = {'#newgame'}   # pressed once at the top only (twice starts a new game; nothing new to find behind it)
    def __init__(self, pw, src, tag):
        self.pw, self.src, self.tag = pw, src, tag
        self.states = {}          # signature -> {'path': [...], 'items': [...], 'dialogs': [...]}
        self.pressed = set(); self.presses = 0; self.reloads = 0; self.lost = []
        self.r = None
    def load(self):
        if self.r: self.r.reload()
        else: self.r = Run(self.pw, self.src, f'{self.tag}_sweep')
        self.r.ev("SHIP.device && SHIP.device.settings && (SHIP.device.settings.tips = false)"); self.r.step(20); self.reloads += 1
    def scan(self): return self.r.ev(SCAN)
    BACK = re.compile(r'^(back|close|stay here|not yet|cancel|done|leave|no|×|✕|x)$', re.I)
    @staticmethod
    def inner(sc):
        # with a panel open, its own things; the screen's edge buttons are pressed from the deck only
        return [i for i in sc['items'] if i['dlg']] if sc['dialogs'] else sc['items']
    @classmethod
    def sig(cls, sc): return (tuple(sorted(sc['dialogs'])), tuple(sorted(i['k'] for i in cls.inner(sc))))
    def press(self, sc, key):
        it = next((i for i in sc['items'] if i['k'] == key), None)
        if not it: return False
        self.r.page.mouse.click(it['x'], it['y']); self.r.step(8); self.presses += 1
        return True
    def replay(self, path):
        self.load()
        for k in path:
            if not self.press(self.scan(), k): return False
        return True
    def back_to(self, path, sig):
        # Escape, else load again and replay the presses; a screen that comes back a little different (the device
        # reopens on the app last used) is taken as it is, and the presses left are made from there
        self.r.page.keyboard.press('Escape'); self.r.step(4)
        for _ in range(3):
            sc = self.scan()
            if self.sig(sc) == sig: return True
            b = next((i for i in self.inner(sc) if self.BACK.match(i['label'])), None)
            if not b: break
            self.press(sc, b['k'])
        if self.sig(self.scan()) == sig: return True
        if self.replay(path) and self.sig(self.scan()) == sig: return True
        self.lost.append(' > '.join(path) or '(the deck)'); return True
    def crawl(self, path=(), depth=0):
        sc = self.scan(); sg = self.sig(sc)
        if sg in self.states: return
        self.states[sg] = {'path': list(path), 'items': self.inner(sc), 'dialogs': sc['dialogs']}
        print(f'    state {len(self.states)}: {" > ".join(path) or "(the deck)"}: {len(self.inner(sc))} things, {self.presses} presses, {self.reloads} loads', flush=True)
        if depth >= self.MAX_DEPTH: return
        for it in self.inner(sc):
            if self.presses >= self.MAX_PRESSES: return
            if (sg, it['k']) in self.pressed or (it['k'] in self.SKIP and path): continue
            self.pressed.add((sg, it['k']))
            cur = self.scan()
            if self.sig(cur) != sg: self.back_to(list(path), sg)
            if not self.press(self.scan(), it['k']): continue
            after = self.scan()
            if after['url'] != sc['url']: self.lost.append('left the page: ' + it['k']); self.replay(list(path)); continue
            if self.sig(after) != sg:
                self.crawl(tuple(path) + (it['k'],), depth + 1)
                self.back_to(list(path), sg)
    def run(self):
        self.load(); self.crawl()
        if self.r: self.r.close()
        return self

def part_reach(pw, src, tag):
    sw = Sweep(pw, src, tag).run()
    keys = sorted({i['k'] for st in sw.states.values() for i in st['items']})
    dl = sorted({d for st in sw.states.values() for d in st['dialogs']})
    print(f'  by touch: {len(sw.states)} screen states, {len(keys)} different pressable things, {sw.presses} presses, {sw.reloads} loads; panels seen: {", ".join(dl)}')
    if sw.lost: print(f'  could not get back from: {"; ".join(sw.lost[:6])}')
    for st in list(sw.states.values())[:200]:
        print(f'    {" > ".join(st["path"]) or "(the deck)"}: {len(st["items"])} things' + (f' in {", ".join(st["dialogs"])}' if st['dialogs'] else ''))
    REACH_INVENTORY.update(states=sw.states, keys=keys)
    return []
REACH_INVENTORY = {}

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
def part_walk(pw, src, tag):
    import math
    fails = []
    r = Run(pw, src, f'{tag}_walk', mode='pad', plug={})
    r.step(10)
    cell = r.ev(OPEN_CELL); print(f'  an open spot: tile {cell[:2]} ({cell[2]} of 25 tiles around it open)')
    for rot in range(4):
        az0 = r.ev("azT")
        for name, (sx, sy) in [('up', (0, -1)), ('right', (1, 0)), ('down', (0, 1)), ('left', (-1, 0))]:
            r.ev(f"({PUT})({json.dumps(cell[:2])})"); r.step(3)
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
        r.ev(f"({PUT})({json.dumps(cell[:2])})"); r.step(3); p0 = r.ev(f"({SCREEN})()")
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
def touch_play(pw, src, tag, mode, presses):
    r = Run(pw, src, tag, mode=mode, plug={} if mode != 'none' else None)
    r.ev("SHIP.device && SHIP.device.settings && (SHIP.device.settings.tips = false)")
    r.step(20)
    for b in presses: r.press(b); r.step(4)
    r.step(20 - 6 * len(presses) if len(presses) < 3 else 1)
    shots, st = [], []
    for k, (x, y) in enumerate([(450, 380), (700, 300)]):
        r.page.mouse.click(x, y); r.step(90)
        shots.append((f'tap{k}', r.shot(f'{tag}_tap{k}'))); g = r.ev(GAME_STATE); g.pop('calls', None); st.append([g, r.js(OUTLINES)])
    r.close(); return shots, st
def part_touch(pw, src, tag):
    fails = []
    a, sa = touch_play(pw, src, f'{tag}_touch_none', 'none', [])
    for presses in (['B'], ['LB', 'RB'], ['UP', 'DOWN']):
        b, sb = touch_play(pw, src, f'{tag}_touch_{"".join(presses)}', 'pad', presses)
        d = same_pics(a, b) + [x for k in range(2) for x in diff_state(sa[k][0], sb[k][0], f'tap{k}')]
        for k in range(2):
            if sb[k][1]['outlines']: d.append(f'tap{k}: a focus outline is left: {sb[k][1]["outlines"]}')
            if sb[k][1]['focus'] != sa[k][1]['focus']: d.append(f'tap{k}: focus on {sb[k][1]["focus"]}, without a pad {sa[k][1]["focus"]}')
        print(f'  pressed {" then ".join(presses)}, then tapped twice: {"the no-pad game" if not d else str(len(d)) + " differences"}')
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
    if not st[0]: fails.append('unplugged within half a minute of using it: the game should pause')
    elif 'Controller disconnected' not in st[1]: fails.append(f'the Pause card should say "Controller disconnected": "{st[1][:80]}"')
    t0 = r.ev("SHIP.time.min"); r.step(60); t1 = r.ev("SHIP.time.min")
    if t1 != t0: fails.append(f'the ship clock ran while paused after the unplug ({t0} -> {t1})')
    r.js('window.__pads.plug(0, {})'); r.step(5); r.press('MENU'); r.step(10)
    if r.ev("PAUSE.on"): fails.append('reconnected and pressed Start: the game should go on')
    else: print('  plugged back in, Start: playing again')
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
    r.ev(f"({PUT})({json.dumps(cell[:2])})"); r.step(3); p0 = r.ev(f"({SCREEN})()")
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

# parts that need a package: 'not yet' until PAD_BUILT names it
NEEDS = {'touch': ['base'], 'walk': ['deck'], 'pick': ['pick'], 'reach': ['panels'], 'day': ['base', 'deck', 'pick', 'panels', 'games'],
         'games': ['games'], 'unplug': ['deck', 'marks'], 'odd': ['deck']}
PART_FN = {'idle': part_idle, 'save': part_save, 'calls': part_calls, 'walk': part_walk, 'touch': part_touch, 'unplug': part_unplug, 'odd': part_odd}   # 'reach' joins when the pad half is written

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

# ---- the stand-in (--selftest) ----------------------------------------------------------------------------------------
# A tiny controller driver written for this check alone, planted in a copy of the game, so each part can be shown to
# PASS on something that works and FAIL on its planted faults before section 26 exists. It is not the design: section 26
# is CT1's. It covers what's built in the parts here so far (the deck package).
STANDIN = r"""
const PAD_ON = true, PAD_BUILT = ['base', 'deck', 'marks'];
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
    SRC = plant(SRC, STANDIN); print('--selftest: the parts run on a copy with the check\'s own stand-in driver (not section 26)')
built = pad_built(SRC)
print(f'controller_check on {GAME}: PAD_ON {pad_switch(SRC)}, packages built: {sorted(built) or "none"}')
with sync_playwright() as pw:
    br = pw   # each Run launches its own browser
    for part in PARTS:
        print(f'[{part}]')
        if part not in PART_FN or any(p not in built for p in NEEDS.get(part, [])):
            missing = [p for p in NEEDS.get(part, []) if p not in built]
            if part == 'reach' and '--inventory' in FLAGS:   # the touch half alone: what there is to reach, read from the page
                part_reach(br, SRC, 'g')
            note = f'waits for package{"s" if len(missing) > 1 else ""} {", ".join(missing)}' if missing else 'built in this check later'
            print(f'  not yet ({note})'); RESULTS.append((part, 'not yet', note)); continue
        fails = PART_FN[part](br, SRC, 'g')
        for f in fails: check(False, f'{part}: {f}')
        RESULTS.append((part, 'FAIL' if fails else 'OK', f'{len(fails)} problems' if fails else ''))
        if '--mutants' in FLAGS:
            for name, code in MUTANTS.get(part, {}).items():
                mf = PART_FN[part](br, plant(SRC, code), 'm')
                caught = bool(mf)
                print(f'  planted fault "{name}": {"caught (" + mf[0][:110] + ")" if caught else "NOT CAUGHT"}')
                check(caught, f'{part}: the planted fault "{name}" was not caught')
                RESULTS.append((part + ' mutant', 'OK' if caught else 'FAIL', name))

print('Summary:')
for p, res, note in RESULTS: print(f'  {p:16s} {res:8s} {note}')
ny = [p for p, res, _ in RESULTS if res == 'not yet']
print(('CONTROLLER CHECK OK' + (f' (not yet: {", ".join(ny)})' if ny else '')) if ok else 'CONTROLLER CHECK FAILED')
sys.exit(0 if ok else 1)
