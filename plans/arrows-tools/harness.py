# AR1's play harness: boot the game in Dev mode, set the career to a day, run the real loop and log what the player is told.
import sys, json, re, os, pathlib, time
sys.path.insert(0, '/home/user/Cadet-game')
GAME = os.environ.get('GAME', '/home/user/Cadet-game/starship-cadet.html')
from playwright.sync_api import sync_playwright
WORK = pathlib.Path('/tmp/cadet-work'); (WORK / 'test').mkdir(parents=True, exist_ok=True)
THREE = (WORK / 'three/package/build/three.min.js').read_text()
INIT = """(() => { let vt = 1000; const cbs = []; performance.now = () => vt; Date.now = () => vt;
  window.requestAnimationFrame = cb => { cbs.push(cb); return cbs.length; };
  window.__step = (n, dtMs) => { for (let k = 0; k < n; k++) { vt += dtMs; const q = cbs.splice(0); for (const cb of q) cb(vt); } }; })();"""
def instrument(html):
    i = html.rfind('})();'); return html[:i] + "window.__sc = src => eval(src);\n" + html[i:]
# the logger: everything the player is told, with the ship time
LOGGER = r"""(() => {
  window.__log = [];
  const T = () => clockText();
  const push = (k, s) => { const last = __log[__log.length - 1]; if (last && last[1] === k && last[2] === s) return; __log.push([T(), k, s]); };
  const _toast = toast; toast = function(a, b) { push('toast', a + ' :: ' + (b || '')); return _toast.apply(this, arguments); };
  const _mail = mailSend; mailSend = function(m) { push('mail', (m.from || '') + ' :: ' + (m.subject || '') + ' :: ' + String(m.body || '').slice(0, 160) + (m.at > shipNow() + 1 ? ' [at ' + hhmm(m.at % 1440) + ' Day ' + (Math.floor(m.at / 1440) + 1) + ']' : '')); return _mail.apply(this, arguments); };
  const _tip = tipShow; tipShow = function(id, t) { const r = _tip.apply(this, arguments); if (r) push('tip', id + ' :: ' + t); return r; };
  const _say = typeof bubbleSay === 'function' ? bubbleSay : null;
  window.__watch = () => {
    const g = goalNow(); const gl = g ? (g.label || '?') + ' @D' + g.deck + (g.room ? ' ' + g.room : '') + (g.place ? ' ' + g.place : '') : null;
    if (gl !== window.__gl) { window.__gl = gl; push('arrow', gl || '(none)'); }
    const W = SHIP.works, c = W && W.cur, cs = c ? c.id + ':' + c.st + (c.j ? ' job ' + c.j : '') : null;
    if (cs !== window.__cs) { window.__cs = cs; push('training', cs || '(none)'); }
    const dl = typeof DIALOGUE !== 'undefined' && DIALOGUE ? 'on' : null; if (dl !== window.__dl) { window.__dl = dl; if (dl) push('dialogue', (DIALOGUE.key || DIALOGUE.id || '') + ''); }
    const tr = W ? Object.keys(W.tr).join(',') : ''; if (tr !== window.__tr) { window.__tr = tr; push('trained', tr); }
    const mine = typeof openJobs === 'function' ? openJobs('you').map(j => j.title + (j.reserved ? '[R' + j.reserved + ']' : '')).join(' | ') : '';
    if (mine !== window.__bd) { window.__bd = mine; push('board', mine.slice(0, 300)); }
    const mj = typeof myJob === 'function' && myJob(); const ms = mj ? mj.id + ' ' + mj.title : null; if (ms !== window.__mj) { window.__mj = ms; push('myjob', ms || '(none)'); }
    const oc = (SHIP.occasions || []).filter(o => o.status === 'asked' || o.status === 'on').map(o => o.id + '@' + hhmm(o.at % 1440) + ' ' + (o.deck + o.room)).join(', ');
    if (oc !== window.__oc) { window.__oc = oc; push('occasions', oc); }
  };
})()"""
class G:
    def __init__(self, pw, w=390, h=844, suffix='#dev'):
        self.errors = []
        self.b = pw.chromium.launch(executable_path='/opt/pw-browsers/chromium', args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
        self.ctx = self.b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=1)
        self.page = self.ctx.new_page()
        self.page.on('pageerror', lambda e: self.errors.append(f'pageerror: {e}'))
        self.page.on('console', lambda m: m.type == 'error' and self.errors.append(f'error: {m.text}'))
        self.page.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
        self.page.add_init_script(INIT)
        tmp = WORK / 'test' / ('_ar1_' + pathlib.Path(GAME).name); tmp.write_text(instrument(pathlib.Path(GAME).read_text())); self.tmp = tmp
        self.page.goto('file://' + str(tmp) + suffix); self.ready()
    def ready(self):
        self.page.wait_for_function('window.__sc !== undefined', timeout=90000)
        self.page.add_style_tag(content='*,*::before,*::after{transition:none!important;animation:none!important}')
        self.ev("(() => { const rr = renderer.render.bind(renderer); window.__draw = false; renderer.render = (s, c) => { if (window.__draw) rr(s, c); }; })()")
        self.step(20)
        if self.page.locator('text=Sign and go aboard').count():
            self.page.fill('form input', 'Ada'); self.page.click('text=Sign and go aboard'); self.step(30)
        self.ev(LOGGER)
    def ev(self, src): return self.page.evaluate('s => window.__sc(s)', src)
    def step(self, n, dt=1000/30): self.page.evaluate(f'window.__step({n}, {dt})')
    def reload_ev(self, src):
        with self.page.expect_navigation(timeout=90000): self.page.evaluate('s => window.__sc(s)', src)
        self.ready()
    def run_min(self, mins, dt=50, watch_every=10, hook=None):
        # real loop until the ship clock has moved `mins` ship minutes (the game caps a frame's dt, so count by the clock)
        end = self.ev('shipNow()') + mins; guard = 0
        while self.ev('shipNow()') < end and guard < int(mins * 40) + 200:
            self.step(watch_every, dt); self.ev('__watch()'); guard += 1
            if hook: hook(self)
    def log(self, since=0): return self.ev('__log').__getitem__(slice(since, None))
    def shot(self, path):
        self.page.evaluate('window.__draw = true'); self.step(1); self.page.screenshot(path=path); self.page.evaluate('window.__draw = false')
    def close(self): self.b.close()
