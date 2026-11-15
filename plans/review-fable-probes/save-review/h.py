import json, re, pathlib, os, time, http.server, threading, functools, socketserver
from playwright.sync_api import sync_playwright
S = pathlib.Path(__file__).parent
THREE = pathlib.Path('/tmp/cadet-work-save/three/package/build/three.min.js').read_text()
INIT = """
(() => {
  let vt = 1000; const cbs = [];
  performance.now = () => vt; Date.now = () => vt;
  window.__errs = [];
  window.addEventListener('error', e => window.__errs.push('E: ' + (e.message||e) + ' @' + e.lineno));
  window.requestAnimationFrame = cb => { cbs.push(cb); return cbs.length; };
  window.__pending = () => cbs.length;
  window.__step = (n, dtMs) => { for (let k = 0; k < n; k++) { vt += dtMs; const q = cbs.splice(0); for (const cb of q) { try { cb(vt); } catch (e) { window.__errs.push('FRAME: ' + (e && e.stack || e).toString().slice(0, 400)); } } } };
  { const set0 = Storage.prototype.setItem; window.__ro = false; Storage.prototype.setItem = function (k, v) { if (window.__ro) return; return set0.call(this, k, v); }; }
  __PRE__
})();
"""
def build():
    html = pathlib.Path('/home/user/Cadet-game/starship-cadet.html').read_text()
    i = html.rfind('})();')
    (S / 'www' / 'g.html').write_text(html[:i] + "window.__sc = src => eval(src);\n" + html[i:])
def serve(port):
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(S / 'www'))
    class Q(socketserver.ThreadingTCPServer): allow_reuse_address = True
    h.log_message = lambda *a: None
    srv = Q(('127.0.0.1', port), h); threading.Thread(target=srv.serve_forever, daemon=True).start(); return srv
class G:
    def __init__(self, pw, port, pre=''):
        self.b = pw.chromium.launch(executable_path='/opt/pw-browsers/chromium', args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
        self.ctx = self.b.new_context(viewport={'width': 600, 'height': 500})
        self.page = self.ctx.new_page(); self.errors = []
        self.page.on('pageerror', lambda e: self.errors.append('pageerror: ' + str(e)[:400]))
        self.page.on('console', lambda m: m.type == 'error' and self.errors.append('console: ' + m.text[:300]))
        self.page.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
        self.page.route(re.compile(r'.*fonts.*'), lambda r: r.abort())
        self.page.add_init_script(INIT.replace('__PRE__', pre))
        self.url = f'http://127.0.0.1:{port}/g.html'
    def load(self, q=''):
        self.errors.clear()
        try: self.page.evaluate('window.__ro = true')
        except Exception: pass
        self.page.goto(self.url + q, timeout=120000)
        try: self.page.wait_for_function('window.__sc !== undefined', timeout=60000); return True
        except Exception: return False
    def ev(self, s): return self.page.evaluate('s => window.__sc(s)', s)
    def step(self, n, dt=33):
        self.page.evaluate("if (window.__skip === undefined && window.__sc) window.__sc(\"(() => { const rr = renderer.render.bind(renderer); window.__skip = true; renderer.render = (s, c) => { if (!window.__skip) rr(s, c); }; })()\")")
        self.page.evaluate(f'window.__step({n}, {dt})')
    def errs(self): return self.errors + self.page.evaluate('window.__errs')
