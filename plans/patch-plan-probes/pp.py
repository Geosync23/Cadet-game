# Patch-plan harness: the real game (claude/integration) at phone size, with saving on (a fresh profile each launch),
# so the arrival starts as it does for a player. Reuses cadet_test.py's Game (virtual clock, manual frames, __sc eval).
#   from pp import *; g = start(); g.ev('clockText()'); g.step(30); g.shot('x.png'); g.close()
# GAME env var: the build to load (default the repo's starship-cadet.html). CADET_WORK: a work dir of your own.
import os, sys, re, json, pathlib
REPO = '/home/user/Cadet-game'
os.environ.setdefault('CADET_CHROME', '/opt/pw-browsers/chromium')
_src = open(REPO + '/cadet_test.py').read().split("a, shots = run(")[0]
exec(_src)
from playwright.sync_api import sync_playwright

SHOTS = REPO + '/plans/patch-plan-shots'
os.makedirs(SHOTS, exist_ok=True)

class PGame(Game):
    """Game with a chosen query (default '?debug': saving on, so a first launch arrives on Day 0)."""
    def __init__(self, pw, path, query='?debug', w=390, h=844, errors=None):
        self.errors = [] if errors is None else errors
        b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
        self.b = b
        ctx = b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=1, has_touch=True)
        self.page = ctx.new_page()
        self.page.on('console', lambda m: m.type in ('error',) and self.errors.append(f'{m.type}: {m.text}'))
        self.page.on('pageerror', lambda e: self.errors.append(f'pageerror: {e}'))
        self.page.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
        self.page.add_init_script(INIT)
        html = instrument(pathlib.Path(path).read_text())
        tmp = WORK / 'test' / ('_pp_' + pathlib.Path(path).name)
        tmp.write_text(html)
        self.page.set_default_navigation_timeout(120000); self.page.goto('file://' + str(tmp) + query)
        self.page.wait_for_function('window.__sc !== undefined || window.__err', timeout=90000)
        self.ev("(() => { const rr = renderer.render.bind(renderer); window.__skip = false; renderer.render = (s, c) => { if (!window.__skip) rr(s, c); }; })()")
    def secs(self, s):            # real seconds of play at 30 fps (ship time runs at 0.6 ship min / real s)
        self.step(int(s * 30))
    def shipmins(self, m):        # play m ship minutes in real frames
        self.secs(m / 0.6)
    def snap(self, name):
        p = SHOTS + '/' + name + '.png'; self.page.screenshot(path=p); return p

def start(query='?debug', w=390, h=844):
    pw = sync_playwright().start()
    return PGame(pw, os.environ.get('GAME', REPO + '/starship-cadet.html'), query, w, h)

# common moves (strings for g.ev)
SIGN = "(() => { const i = document.querySelector('form input[maxlength=\"24\"]'); return !!i; })()"
def sign(g, name='Sam'):
    g.page.fill('form input[maxlength="24"]', name); g.page.click('form button'); g.step(5)

STATE = r"""(() => ({ t: clockText(), deck: deckDef.num, me: player.here(), step: SHIP.intro && SHIP.intro.step,
  dlg: typeof DIALOGUE !== 'undefined' && DIALOGUE ? DIALOGUE.id : null, act: typeof ACT !== 'undefined' && ACT ? (ACT.id || ACT.kind || true) : null,
  toast: (document.getElementById('toast') || {}).textContent || '' }))()"""
