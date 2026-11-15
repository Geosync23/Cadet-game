# shared probe harness: cadet_test's virtual clock and scope hook, plus CDP profiling
import json, sys, re, pathlib, os, itertools, time
from playwright.sync_api import sync_playwright
WORK = pathlib.Path(os.environ.get('CADET_WORK', '/tmp/cadet-work')); (WORK / 'test').mkdir(parents=True, exist_ok=True)
THREE = (WORK / 'three/package/build/three.min.js').read_text()
INIT = """(() => { let vt = 1000; const cbs = []; window.__realNow = (() => { const f = performance.now.bind(performance); return () => f(); })();
  performance.now = () => vt; Date.now = () => vt;
  window.requestAnimationFrame = cb => { cbs.push(cb); return cbs.length; };
  window.__step = (n, dtMs) => { for (let k = 0; k < n; k++) { vt += dtMs; const q = cbs.splice(0); for (const cb of q) cb(vt); } };
})();"""
SKIP = "(() => { const rr = renderer.render.bind(renderer); window.__skip = false; renderer.render = (s, c) => { if (!window.__skip) rr(s, c); }; })()"
N = itertools.count(1)
class Game:
    def __init__(self, pw, path, w=390, h=844, q='?nosave&debug', virtual=True, storage=None):
        self.errors = []
        self.b = pw.chromium.launch(executable_path='/opt/pw-browsers/chromium', args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--enable-precise-memory-info', '--js-flags=--expose-gc'])
        self.ctx = self.b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=1)
        self.page = self.ctx.new_page()
        self.page.on('console', lambda m: m.type in ('error', 'warning') and self.errors.append(f'{m.type}: {m.text}'))
        self.page.on('pageerror', lambda e: self.errors.append(f'pageerror: {e}'))
        self.page.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
        if virtual: self.page.add_init_script(INIT)
        html = pathlib.Path(path).read_text(); i = html.rfind('})();'); html = html[:i] + "window.__sc = src => eval(src);\n" + html[i:]
        self.tmp = WORK / 'test' / f'_fr1_{os.getpid()}_{next(N)}.html'; self.tmp.write_text(html)
        self.url = 'file://' + str(self.tmp) + q
        self.page.goto(self.url, timeout=180000)
        self.page.wait_for_function('window.__sc !== undefined', timeout=180000)
        self.cdp = self.ctx.new_cdp_session(self.page)
        if virtual: self.ev(SKIP)
    def ev(self, src): return self.page.evaluate('s => window.__sc(s)', src)
    def step(self, n, dt=1000/30, draw=False):
        if draw: self.page.evaluate(f'window.__skip = false; window.__step({n}, {dt})')
        else: self.page.evaluate(f'window.__skip = true; window.__step({n}, {dt}); window.__skip = false')
    def gc(self): self.cdp.send('HeapProfiler.collectGarbage')
    def heap(self): self.gc(); return self.page.evaluate('performance.memory.usedJSHeapSize')
    def profile(self, fn, interval=200):
        self.cdp.send('Profiler.enable'); self.cdp.send('Profiler.setSamplingInterval', {'interval': interval}); self.cdp.send('Profiler.start')
        fn(); p = self.cdp.send('Profiler.stop')['profile']
        byid = {n['id']: n for n in p['nodes']}; agg = {}; tot = 0
        for s, d in zip(p['samples'], p['timeDeltas']):
            f = byid[s]['callFrame']; k = (f['functionName'] or '(anon)') + (':' + str(f['lineNumber'] + 1) if f['url'].startswith('file') else ' [three]' if 'three' in f['url'] else '')
            agg[k] = agg.get(k, 0) + d; tot += d
        # inclusive time by function name (a node's own time counts for every distinct function on its stack)
        par = {}
        for n in p['nodes']:
            for c in n.get('children', []): par[c] = n['id']
        selfus = {}
        for s, d in zip(p['samples'], p['timeDeltas']): selfus[s] = selfus.get(s, 0) + d
        inc = {}
        for nid, us in selfus.items():
            seen = set(); x = nid
            while x is not None:
                nm = byid[x]['callFrame']['functionName'] or '(anon)'
                if nm not in seen: seen.add(nm); inc[nm] = inc.get(nm, 0) + us
                x = par.get(x)
        self.inc = {k: v / 1000 for k, v in inc.items()}
        return tot / 1000, sorted(((v / 1000, k) for k, v in agg.items()), reverse=True)
    def alloc(self, fn, interval=4096):
        self.cdp.send('HeapProfiler.enable'); self.cdp.send('HeapProfiler.startSampling', {'samplingInterval': interval, 'includeObjectsCollectedByMajorGC': True, 'includeObjectsCollectedByMinorGC': True})
        fn(); p = self.cdp.send('HeapProfiler.stopSampling')['profile']; agg = {}
        def walk(n):
            f = n['callFrame']; k = (f['functionName'] or '(anon)') + (':' + str(f['lineNumber'] + 1) if f['url'].startswith('file') else ' [three]' if 'three' in f['url'] else '')
            agg[k] = agg.get(k, 0) + n['selfSize']
            for c in n.get('children', []): walk(c)
        walk(p['head']); return sum(agg.values()), sorted(((v, k) for k, v in agg.items()), reverse=True)
    def close(self): self.b.close(); self.tmp.unlink(missing_ok=True)
