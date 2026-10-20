# DR1: what a Dev clock jump's "excused" day does (D3), Dev on, a fresh Dev save started with Skip to Monday
import sys, os, re, json, pathlib
os.environ.setdefault('CADET_CHROME','/opt/pw-browsers/chromium')
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("class Game")[0])
from playwright.sync_api import sync_playwright
GAME = sys.argv[1]
tmp = WORK / 'test' / '_dr1_excuse.html'; tmp.write_text(instrument(pathlib.Path(GAME).read_text()))
PROBE = r"""(({ day, from, to }) => {
  const at = m => (day - 1) * 1440 + m;
  // reach `from` on `day` by plain skips (as sleeping would), no Dev action
  for (let t = shipNow() + 30; t < at(from); t += 30) skipTo(t); skipTo(at(from)); worksCareerTick(at(from));
  const W0 = SHIP.works, before = { shiftOn: playerShiftOn(day), op: W0 && W0.op[day] ? W0.op[day].slice() : [], cur: W0 && W0.cur ? W0.cur.id + ':' + W0.cur.st : null };
  const ok = devmodeRun('test jump', () => devmodeSkipTo(at(to)));
  worksCareerTick(at(to)); worksTick();
  const W = SHIP.works, c = SHIP.career;
  const r = { clock: clockText(), ran: ok, held: devmodeHold(), excused: devmodeState().ex.slice(), shiftOn: playerShiftOn(day), careerOff: careerOff(day),
    clock_in: careerClock(shipNow(), true), clockedIn: careerClockedIn(day), ms: c.ms, missed: c.md,
    before, opAfter: W && W.op[day] ? W.op[day].slice() : [], curAfter: W && W.cur ? W.cur.id + ':' + W.cur.st : null,
    heldForYou: SHIP.jobs.filter(j => j.status === 'open' && j.reserved).map(j => j.kind + '/' + j.reserved), note: devmodeState().note, msg: DM_UI.msg };
  // the rest of the day, as a player who now walks into the Works bay and works: can they?
  for (let t = at(to) + 30; t <= at(16 * 60); t += 30) { skipTo(t); worksCareerTick(t); }
  r.endOfDay = { opDay: W && W.op[day] ? W.op[day].slice() : [], cur: W && W.cur ? W.cur.id + ':' + W.cur.st : null, myJobs: openJobs('you').length };
  return r;
})"""
def page(pw):
    b = pw.chromium.launch(executable_path=os.environ['CADET_CHROME'], args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
    pg = b.new_page(viewport={'width':390,'height':844}); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)[:150]))
    pg.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
    pg.add_init_script(INIT); pg.goto('file://' + str(tmp) + '#dev')
    pg.wait_for_function('window.__sc !== undefined', timeout=90000)
    ev = lambda s: pg.evaluate('s => window.__sc(s)', s)
    ev("(() => { renderer.render = () => {}; })()"); pg.evaluate('window.__step(10, 33)')
    ev("(INTRO_BOOT = false, newGameStart(false), introSkip(), TIPS_OFF = true, 0)")
    return b, ev, errs
with sync_playwright() as pw:
    for (day, frm, to) in [(2, 8*60, 9*60+30), (2, 8*60, 8*60+55), (9, 8*60, 10*60), (9, 9*60+30, 9*60+40)]:
        b, ev, errs = page(pw)
        r = ev(f"({PROBE})({{ day: {day}, from: {frm}, to: {to} }})")
        print(f"Day {day} {frm//60:02d}:{frm%60:02d} -> {to//60:02d}:{to%60:02d}:", json.dumps(r)[:900], errs[:2]); b.close()
