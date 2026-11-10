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
exec(open(__file__.replace('cr2_check.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
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

STATE = """(() => { const W = SHIP.works, o = SHIP.occasions.filter(x => x.id === 'promoSummons').pop();
  return { clock: clockText(), tier: W.tier, rank: W.rank, sd: promoSummonsDay(), occ: o ? { key: o.key, status: o.status, met: !!o.met } : null,
    room: (ROOMS[roomAt(...player.here())] || {}).name, dlg: DIALOGUE ? (DIALOGUE.m && DIALOGUE.m.script) || DIALOGUE.sc || 1 : null }; })()"""
def jump(pg, id): pg.ev(f"devmodeRun('cr2', () => devmodeSetCareerTo(DM_BEATS.find(b => b.id === '{id}').day, DM_BEATS.find(b => b.id === '{id}')))"); pg.step(10)
def clock(pg, abs_expr): pg.ev(f"devmodeRun('Clock', () => devmodeSkipTo({abs_expr}))"); pg.step(10)
def office(pg):                                        # into her office before 08:15, then a few ship minutes in play
    pg.ev("devmodeMove(5, () => ixGoalWorld({ room: 'o' }), r => r === 'o')")
    seen = None
    for _ in range(12):
        pg.step(30)
        s = pg.ev(STATE)
        if s['dlg']: seen = s; break
    if not seen: return pg.ev(STATE), False
    for _ in range(80):                                # play the scene through
        if not pg.ev('!!DIALOGUE'): break
        pg.ev('(() => { const l = DIALOGUE.queue[DIALOGUE.i]; if (l && l.choice) dialogueChoose(0); else dialogueNext(); })()'); pg.step(3)
    pg.step(30)
    return seen, pg.ev(STATE)['tier'] == 2

def run(ctx, on, way):
    pg = Page(ctx); pg.ev(f'CR9991_RESULTS_ON = {"true" if on else "false"}')
    if way in ('jump', 'stuck'):
        jump(pg, 'promo')
        if way == 'stuck': pg.ev("SHIP.occasions.filter(o => o.id === 'promoSummons').forEach(o => o.status = 'done')"); pg.step(10)
        clock(pg, "(SHIP.time.day - 1) * 1440 + 8 * 60 + 10")
    else:
        jump(pg, 't2'); pg.ev('promoPassed(shipNow())'); pg.step(10)
        if way == 'clock': clock(pg, "SHIP.time.day * 1440 + 8 * 60 + 10")
        elif way == 'sleep': pg.ev("skipTo(SHIP.time.day * 1440 + 8 * 60 + 10)"); pg.step(10)
        elif way == 'next':
            pg.ev("devmodeRun('Next', () => { const s = devmodePromoSteps().find(x => !x.done && x.at - 5 > shipNow()); devmodeSkipTo(s.at - 5); })"); pg.step(10)
        elif way == 'late':
            clock(pg, "SHIP.time.day * 1440 + 13 * 60"); clock(pg, "(SHIP.time.day) * 1440 + 8 * 60 + 10")
    before = pg.ev(STATE); seen, promoted = office(pg)
    errs = pg.errors[:3]; pg.page.close()
    return before, seen, promoted, errs

with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    has = None
    cases = [('jump', 'jump', [True, False]), ('stuck', 'stuck', [True]), ('test', 'clock', [True, False]), ('test', 'sleep', [True]), ('test', 'next', [True]), ('late', 'late', [True, False])]
    for part, way, ons in cases:
        if ONLY and part not in ONLY: continue
        for on in ons:
            ctx = b.new_context(viewport={'width': 800, 'height': 600})
            if has is None:
                pg = Page(ctx); has = pg.ev("typeof CR9991_RESULTS_ON !== 'undefined'"); pg.page.close()
                if not check(has, 'no CR9991_RESULTS_ON in this build'): break
            before, seen, promoted, errs = run(ctx, on, way); ctx.close()
            tag = f'{part}/{way} {"on" if on else "off"}'
            print(f'  {tag}: at {before["clock"]} summons {before["occ"]}; office {seen["clock"] if isinstance(seen, dict) else seen}: scene {seen["dlg"] if isinstance(seen, dict) else None}; promoted {promoted}')
            check(not errs, f'{tag}: errors {errs}')
            day = 10 if way == 'late' else 9
            if way == 'jump' and not on:
                check(before['occ'] and before['occ']['status'] == 'done' and not promoted, f'{tag}: the 0.99.9 bug (summons closed, no scene) is gone with the switch off, so the off proof proves nothing: {before}, {seen}')
            else:
                check(before['occ'] and before['occ']['key'] == f'promoSummons@{day}' and before['occ']['status'] == 'asked', f'{tag}: the summons isn\'t open for Day {day}: {before}')
                check(isinstance(seen, dict) and seen['dlg'] and seen['room'] == "Works Chief's office" and seen['clock'].startswith(f'Day {day},'), f'{tag}: no results scene in Calder\'s office on Day {day}: {seen}')
                check(promoted, f'{tag}: the scene played through didn\'t make you an officer')
    b.close()
print('CR2 CHECK OK' if ok else 'CR2 CHECK FAILED')
sys.exit(0 if ok else 1)
