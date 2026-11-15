# interactive driver: a phone-size page with a virtual clock; commands come in over a local socket
import sys, os, json, re, pathlib, socket, traceback
from playwright.sync_api import sync_playwright
BUILD = sys.argv[1]; PORT = int(sys.argv[2]); HASH = sys.argv[3] if len(sys.argv) > 3 else ''
HERE = os.path.dirname(os.path.abspath(__file__))
THREE = open('/tmp/cadet-work/three/package/build/three.min.js').read()
INIT = """(() => { let vt = 1000; const cbs = []; performance.now = () => vt; Date.now = () => vt;
  window.requestAnimationFrame = cb => { cbs.push(cb); return cbs.length; };
  window.__step = (n, dtMs) => { for (let k = 0; k < n; k++) { vt += dtMs; const q = cbs.splice(0); for (const cb of q) cb(vt); } }; })();"""
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome', args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1, has_touch=True, is_mobile=True)
    page = ctx.new_page(); errors = []
    page.on('pageerror', lambda e: errors.append(f'pageerror: {e}'))
    page.on('console', lambda m: m.type == 'error' and errors.append(f'error: {m.text}'))
    page.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
    page.add_init_script(INIT)
    html = pathlib.Path(BUILD).read_text(); i = html.rfind('})();')
    tmp = pathlib.Path(HERE) / f'_game_{PORT}.html'; tmp.write_text(html[:i] + "window.__sc = src => eval(src);\n" + html[i:])
    def ready():
        page.wait_for_function('window.__sc !== undefined', timeout=90000)
        page.evaluate("s => window.__sc(s)", "(() => { const rr = renderer.render.bind(renderer); window.__draw = false; renderer.render = (s, c) => { if (window.__draw) rr(s, c); }; })()")
    page.goto('file://' + str(tmp) + HASH); ready()
    def step(n, dt=33.3):
        if n > 1: page.evaluate(f'window.__step({n - 1}, {dt})')
        page.evaluate(f'window.__draw = true; window.__step(1, {dt}); window.__draw = false')
    srv = socket.socket(); srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1); srv.bind(('127.0.0.1', PORT)); srv.listen(1)
    print('ready', flush=True)
    while True:
        c, _ = srv.accept(); data = b''
        while True:
            d = c.recv(65536)
            if not d: break
            data += d
            if data.endswith(b'\n\n'): break
        out = []
        try:
            for cmd in json.loads(data.decode()):
                k = cmd[0]
                if k == 'tap': page.touchscreen.tap(cmd[1], cmd[2]); step(cmd[3] if len(cmd) > 3 else 3); out.append('ok')
                elif k == 'click': page.mouse.click(cmd[1], cmd[2]); step(3); out.append('ok')
                elif k == 'tapsel': page.locator(cmd[1]).first.tap(timeout=3000); step(3); out.append('ok')
                elif k == 'fill': page.fill(cmd[1], cmd[2]); out.append('ok')
                elif k == 'step': step(cmd[1], cmd[2] if len(cmd) > 2 else 33.3); out.append('ok')
                elif k == 'shot': step(1, 1); page.screenshot(path=f'{HERE}/shots/{cmd[1]}.png'); out.append(cmd[1])
                elif k == 'ev': out.append(page.evaluate('s => window.__sc(s)', cmd[1]))
                elif k == 'js': out.append(page.evaluate(cmd[1]))
                elif k == 'wait': page.wait_for_timeout(cmd[1]); out.append('ok')
                elif k == 'reload': page.reload(); ready(); out.append('ok')
                elif k == 'drag':
                    cdp = ctx.new_cdp_session(page); x0, y0, x1, y1 = cmd[1:5]; n = 8
                    cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x0, 'y': y0}]}); step(1)
                    for q in range(1, n + 1):
                        cdp.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': [{'x': x0 + (x1 - x0) * q / n, 'y': y0 + (y1 - y0) * q / n}]}); step(cmd[5] if len(cmd) > 5 else 2)
                    cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []}); step(2); out.append('ok')
                elif k == 'errors': out.append(errors[-10:])
                elif k == 'quit': c.sendall(b'"bye"'); c.close(); b.close(); sys.exit(0)
        except Exception as e:
            out.append('ERR ' + traceback.format_exc()[-600:])
        c.sendall(json.dumps(out).encode()); c.close()
