# Starship Cadet: CR2's check (lead 51, the user's 0.99.9 bug "the meeting with Calder for your results doesn't work ...
# I walk into Calder's office on time and nothing happens"; switch CR9991_RESULTS_ON, 24p's slot; a hook in section 25).
# In a real page with #dev, each Dev way to the Tier 2 result, then into Calder's office (Deck 5, room 'o') at 08:15
# and on a few ship minutes in play: her results scene must open there and, played through, make you a Works Officer.
#   jump   Dev's "Day 9: the promotion" jump (08:05 in the bay). Off: the summons is closed by the career setter
#          ('done') and the office stays empty, the 0.99.9 bug, proved still there; on: the scene
#   stuck  the same with the summons closed by hand after the jump (a Dev save already stuck that way): on, opened again
#   test   Dev's "Day 8: the test job", the test passed, then to Day 9 08:14 by the Dev clock, by sleeping (skipTo) and
#          by Dev's Next step: the scene, on and off (normal play's way, unchanged)
#   late   the test passed, then the Dev clock past Day 9's 12:30 (Day 9 excused): the scene on Day 10 08:15, on and off
# The switch is a var, flipped at run time on the page. Setup as cadet_test.py (CADET_WORK, CADET_CHROME).
# Run:  python3 cr2_check.py BUILD.html [part ...]   (about 4 minutes)   Good is CR2 CHECK OK (exit 0).
import sys, os, re, json, pathlib
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright

ok = True
def fail(msg):
    global ok
    ok = False
    print('FAIL', msg)
def check(cond, msg):
    if not cond: fail(msg)
    return cond

GAME = sys.argv[1]
ONLY = set(sys.argv[2:])
TMP = WORK / 'test' / f'_cr2_check_p{os.getpid()}.html'
TMP.write_text(instrument(pathlib.Path(GAME).read_text()))
__import__('atexit').register(lambda: TMP.unlink(missing_ok=True))

class Page:
    def __init__(self, ctx):
        self.errors = []; self.page = ctx.new_page()
        self.page.on('pageerror', lambda e: self.errors.append(f'pageerror: {e}'))
        self.page.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
        self.page.add_init_script(INIT)
        self.page.goto('file://' + str(TMP) + '#dev'); self.page.wait_for_function('window.__sc !== undefined', timeout=90000)
        self.ev("(() => { renderer.render = () => {}; })()"); self.step(20)
        if self.page.locator('text=Sign and go aboard').count():
            self.page.fill('form input', 'Ada'); self.page.click('text=Sign and go aboard'); self.step(30)
    def ev(self, s): return self.page.evaluate('s => window.__sc(s)', s)
    def step(self, n, dt=1000 / 30): self.page.evaluate(f'window.__step({n}, {dt})')


SNAP = """(() => { const W = JSON.parse(JSON.stringify(SHIP.works || null));
  return { clock: clockText(), works: W, occ: SHIP.occasions.map(o => [o.key, o.status, !!o.met]), appts: (typeof apptList === 'function' ? apptList() : []).map(a => [a.id, a.at, a.status]),
    flags: JSON.stringify(SHIP.flags || null).length, mail: SHIP.mail.map(m => m.subject) }; })()"""
targets = [('beat', b) for b in ['t2', 'promo']] + [('day', n) for n in [8, 9, 10, 12, 22]]
def go(on, kind, x):
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
        ctx = b.new_context(viewport={'width': 800, 'height': 600}); pg = Page(ctx); pg.ev(f'CR9991_RESULTS_ON = {"true" if on else "false"}')
        if kind == 'beat': pg.ev(f"devmodeRun('rv', () => devmodeSetCareerTo(DM_BEATS.find(b => b.id === '{x}').day, DM_BEATS.find(b => b.id === '{x}')))")
        else: pg.ev(f"devmodeRun('rv', () => devmodeSetCareerTo({x}))")
        pg.step(10); s = pg.ev(SNAP); s['errors'] = pg.errors[:3]; b.close(); return s
import json
for kind, x in targets:
    off, on = go(False, kind, x), go(True, kind, x)
    diffs = [k for k in off if off[k] != on[k]]
    detail = {k: (off[k], on[k]) for k in diffs if k != 'works'}
    if 'works' in diffs: detail['works'] = [k for k in set(off['works']) | set(on['works']) if off['works'].get(k) != on['works'].get(k)]
    if 'occ' in diffs: detail['occ'] = [(a, b) for a, b in zip(off['occ'], on['occ']) if a != b] + ([('len', len(off['occ']), len(on['occ']))] if len(off['occ']) != len(on['occ']) else [])
    print(kind, x, off['clock'], '| tier', off['works'] and off['works'].get('tier'), '| same' if not diffs else '| DIFF ' + json.dumps(detail)[:900], off['errors'], on['errors'])
