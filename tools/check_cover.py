#!/usr/bin/env python3
"""check_cover.py: run one check as usual, with the browser recording which of the game's functions it used.

    CADET_CHROME=/opt/pw-browsers/chromium python3 tools/check_cover.py OUT.json CHECK.py [the check's arguments]

The check runs exactly as it would on its own (same file, same arguments, same pages; its output is printed as
usual and its exit code is kept). Every page it opens gets Chrome's precise coverage (Profiler.startPreciseCoverage,
call counts, function level), switched on before the game's script runs. Two sets are kept, by game line:
  load  functions that ran while a page was opening (until the game is ready: window.__sc defined)
  run   functions that ran after that, i.e. the ones the check itself made the game run
Coverage is read when a page is ready, every 200 page.evaluate calls, before a reload or goto, and when the page
closes; each read resets the counts. Functions are named by the line they start on in the game file (the test copy
adds its hook after the game's last line, so lines are the same) and by their name. Writes OUT.json:
  {"check": ..., "args": [...], "exit": N, "seconds": S, "game_sha1": ..., "load": [[line, end, name], ...], "run": [...]}
tools/affected.py reads these (tools/check_map.json is all of them in one file: tools/affected.py --merge).
Used to make the map, never to judge a check: its results count only from a normal run (the map run is separate).
"""
import builtins, hashlib, json, os, sys, time

if len(sys.argv) < 3:
    print(__doc__); sys.exit(2)
OUT, CHECK = sys.argv[1], os.path.abspath(sys.argv[2])
sys.argv = [CHECK] + sys.argv[3:]
sys.path.insert(0, os.path.dirname(CHECK))
from playwright.sync_api import Browser, BrowserContext, Page

LOAD, RUN = {}, {}                                   # (line, end) -> name
LINES = {}                                           # url -> (html text, offset of the main script's source, newline offsets)


def html_of(url):
    """the test copy behind a page's url: its text and where the game's script starts in it"""
    if url not in LINES:
        LINES[url] = None
        p = url.split('?')[0].split('#')[0]
        if p.startswith('file://'):
            try:
                html = open(p[7:], encoding='utf-8').read()
                a = html.find('<script>\n')
                if a >= 0:
                    nl = [i for i, ch in enumerate(html) if ch == '\n']
                    LINES[url] = (html, a + len('<script>'), nl)
            except OSError:
                pass
    return LINES[url]


def line_at(nl, i):
    import bisect
    return bisect.bisect_left(nl, i) + 1


def take(page, into):
    s = getattr(page, '_cov', None)
    if not s:
        return
    try:
        res = s.send('Profiler.takePreciseCoverage')['result']
    except Exception:
        return
    for sc in res:
        h = html_of(sc.get('url') or '')
        if not h:
            continue
        html, base, nl = h
        for f in sc['functions']:
            r = f['ranges'][0]
            if r['count'] <= 0 or (r['startOffset'] == 0 and not f['functionName']):
                continue                             # never ran, or the script's own top level
            a, b = line_at(nl, base + r['startOffset']), line_at(nl, base + r['endOffset'] - 1)
            into.setdefault((a, b), f['functionName'])


def arm(page):
    try:
        s = page.context.new_cdp_session(page)
        s.send('Profiler.enable'); s.send('Profiler.startPreciseCoverage', {'callCount': True, 'detailed': False})
        page._cov = s; page._ready = False; page._n = 0
    except Exception as e:
        print('check_cover: no coverage for a page:', e)
    return page


_new_page_b, _new_page_c = Browser.new_page, BrowserContext.new_page
Browser.new_page = lambda self, *a, **k: arm(_new_page_b(self, *a, **k))
BrowserContext.new_page = lambda self, *a, **k: arm(_new_page_c(self, *a, **k))


def ready(page):                                     # the first look after the game is up: what ran so far was the load
    if getattr(page, '_cov', None) and not page._ready:
        try:
            up = page.evaluate('window.__sc !== undefined')
        except Exception:
            return
        if up:
            take(page, LOAD); page._ready = True


_eval = Page.evaluate
def evaluate(self, *a, **k):
    if getattr(self, '_cov', None):
        if not self._ready:
            ready(self)
        self._n += 1
        if self._n % 200 == 0:
            take(self, RUN)
    return _eval(self, *a, **k)
Page.evaluate = evaluate


def navigating(name):
    orig = getattr(Page, name)
    def w(self, *a, **k):
        if getattr(self, '_cov', None):
            if self._ready:
                take(self, RUN)
            self._ready = False                       # the next page load counts as load again
        r = orig(self, *a, **k)
        return r
    setattr(Page, name, w)
for n in ('goto', 'reload'):
    navigating(n)

_wff = Page.wait_for_function
def wait_for_function(self, *a, **k):
    r = _wff(self, *a, **k)
    if getattr(self, '_cov', None) and not self._ready:
        ready(self)
    return r
Page.wait_for_function = wait_for_function

_close_p, _close_b = Page.close, Browser.close
def close_page(self, *a, **k):
    take(self, RUN if getattr(self, '_ready', False) else LOAD); return _close_p(self, *a, **k)
def close_browser(self, *a, **k):
    for c in self.contexts:
        for p in c.pages:
            take(p, RUN if getattr(p, '_ready', False) else LOAD)
    return _close_b(self, *a, **k)
Page.close, Browser.close = close_page, close_browser

T0, code = time.time(), 0
try:
    exec(compile(open(CHECK).read(), CHECK, 'exec'), {'__name__': '__main__', '__file__': CHECK})
except SystemExit as e:
    code = e.code if isinstance(e.code, int) else (0 if e.code is None else 1)
game = next((a for a in sys.argv[1:] if a.endswith('.html')), None)
json.dump({'check': os.path.basename(CHECK).replace('.py', ''), 'args': sys.argv[1:], 'exit': code, 'seconds': round(time.time() - T0),
           'game_sha1': hashlib.sha1(open(game, 'rb').read()).hexdigest() if game and os.path.exists(game) else None,
           'load': sorted([a, b, n] for (a, b), n in LOAD.items()), 'run': sorted([a, b, n] for (a, b), n in RUN.items())},
          open(OUT, 'w'))
print(f'check_cover: {len(LOAD)} functions at load, {len(RUN)} while the check ran -> {OUT}')
sys.exit(code)
