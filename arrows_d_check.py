# Starship Cadet: the arrows plan's piece D (AC2), the shift chain S1-S9 (plans/arrows-pillar5-plan.html, "Step 1").
# In a copy of the build with POINT_ON true and GUIDE_ON set true while it runs, at 390 x 844, Day 9 (an ordinary
# workday), on paper (the clock set by hand, guideShift called by hand, except "tick"):
#   clock in (S2):  nothing before 08:00; from 08:00 a level-4 "Clock in" entry at the time clock; on the clock screen
#                   the pointer on Clock in; pressed: clocked in, the entry and the pointer gone
#   take a job (S3): clocked in with a job you can take: "Take a job at the board"; on the board the pointer on the
#                   first row's Take it (a held one first); taken: the job's own arrow, no pointer
#   turn it in (S5): the work done: the pointer on Turn it in; turned in: S8, the device pointer to the Works app's Work
#                   log, gone once the tab shows
#   empty (S6):     nothing to take: no arrow, "Board's empty for now" once an hour; tracking off: nothing said
#   clock out (S7): from 17:00 "Shift over: clock out" over a job still in hand and over T3 (your training turn), for an
#                   hour; the pointer on Clock out; pressed: gone. Section 15's direct clock-out arrow stays off
#   pass-over:      an entry with nothing to show (T3 while you hold another job) gives way to the next live one
#   reputation (S9): a new word: a toast once and the pointer to the Works app's Training tab; never again for that word
#   pointers:       each panel pointer three times at most, then not asked
#   tick:           guideTick asks the shift chain itself once a ship minute
# And in the build as it is (both off): no entries, no pointer, section 15's clock-out arrow as before.
# Setup as cadet_test.py (playwright, three r128 in $CADET_WORK/three).  Run:  python3 arrows_d_check.py BUILD.html
import sys, json, re, os, pathlib
from playwright.sync_api import sync_playwright

WORK = pathlib.Path(os.environ.get('CADET_WORK', '/tmp/cadet-work'))
(WORK / 'test').mkdir(parents=True, exist_ok=True)
THREE = (WORK / 'three/package/build/three.min.js').read_text()
INIT = """(() => { let vt = 1000; const cbs = []; performance.now = () => vt; Date.now = () => vt;
  window.requestAnimationFrame = cb => { cbs.push(cb); return cbs.length; };
  window.__step = (n, dtMs) => { for (let k = 0; k < n; k++) { vt += dtMs; const q = cbs.splice(0); for (const cb of q) cb(vt); } }; })();"""
ok = True
def check(cond, msg):
    global ok
    if not cond: ok = False; print('FAIL', msg)
    return cond

class Page:
    def __init__(self, ctx, path, tag):
        self.errors = []
        self.page = ctx.new_page()
        self.page.on('pageerror', lambda e: self.errors.append(f'pageerror: {e}'))
        self.page.on('console', lambda m: m.type == 'error' and self.errors.append(f'error: {m.text}'))
        self.page.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
        self.page.add_init_script(INIT)
        html = pathlib.Path(path).read_text(); i = html.rfind('})();')
        tmp = WORK / 'test' / ('_arrows_d_' + tag + '_' + pathlib.Path(path).name)
        tmp.write_text(html[:i] + "window.__sc = src => eval(src);\n" + html[i:])
        self.page.goto('file://' + str(tmp) + '#dev')
        self.page.wait_for_function('window.__sc !== undefined', timeout=90000)
        self.ev("(() => { const rr = renderer.render.bind(renderer); renderer.render = (s, c) => { if (window.__draw) rr(s, c); }; })()")
        self.step(20)
        if self.page.locator('text=Sign and go aboard').count():
            self.page.fill('form input', 'Ada'); self.page.click('text=Sign and go aboard'); self.step(30)
    def ev(self, src): return self.page.evaluate('s => window.__sc(s)', src)
    def step(self, n, dt=1000 / 30): self.page.evaluate(f'window.__step({n}, {dt})')
    def day9(self, guide):                            # the career to the end of Day 8, Day 9 07:50, as in a real game
        self.ev("devmodeRun('Set career', () => devmodeSetCareerTo(8))"); self.step(20)
        if guide: self.ev("GUIDE_ON = true; guideStart()")
        self.ev("devmodeSkipTo(8 * 1440 + 470); clearGoal(); SHIP.player.track = undefined; for (const k of NEED_KEYS) SHIP.player.needs[k] = Math.max(SHIP.player.needs[k], 85); while (typeof TIP_Q !== 'undefined' && TIP_Q.length) tipDone()")
        self.step(10)

B = 8 * 1440                                          # Day 9's start
LAB = "(() => { GUIDE.key = ''; const g = goalNow(); return g ? g.label || null : null; })()"
PTR = r"""(() => { const g = document.getElementById('ptr'); if (!g || g.hidden) return { up: false, now: pointNow() };
  const a = POINT.aim; return { up: true, now: pointNow(), label: g.children[2].textContent, text: a ? a.textContent.slice(0, 40) : null }; })()"""
# a machine job on the board you can take (the arrows check's way): open, unclaimed, tier 1
JOB = """((id, mine) => { const t = shipNow(), m = machineList().find(m => m.deck === 5 && !m.stub && !ENGINE_KINDS.has(m.kind)) || machineList().find(m => !m.stub);
  SHIP.jobs = SHIP.jobs.filter(x => x.id !== id);
  SHIP.jobs.push({ id, machine: m.id, deck: m.deck, room: m.room, kind: 'service', urgency: 1, posted: t, found: t, claimedBy: mine ? 'you' : null, status: mine ? 'claimed' : 'open', start: t, parts: [], title: 'Service' });
  MACH_REV++; ixGoalAt = -1; return id; })"""

def at(pg, m): pg.ev(f"setShipNow({B + m}); GUIDE.key = ''")
def shift(pg): pg.ev("guideShift(); GUIDE.key = ''")
def ptr(pg, n=3): pg.step(n); return pg.ev(PTR)

def part_on(pg):
    pg.ev("window.__toasts = []; { const t0 = toast; toast = (a, b, o) => { __toasts.push(String(b)); return t0(a, b, o); }; }")
    # S2: clock in
    at(pg, 470); shift(pg)
    early = pg.ev(LAB); ids = pg.ev("guideList().map(e => e.id)")
    check(not any(i.startswith('shift:') for i in ids) and not str(early or '').startswith('Clock in'), f'S2: nothing before 08:00 ({early}, {ids})')
    at(pg, 480); shift(pg)
    e = pg.ev("guideList().find(e => e.id === 'shift:in:9') || null"); lab = pg.ev(LAB)
    print('  S2:', lab, e and e['level'])
    check(e and e['level'] == 4 and lab == 'Clock in: shift at 09:00', f'S2: from 08:00 a level-4 "Clock in" entry ({lab}, {e})')
    g = pg.ev("(() => { GUIDE.key = ''; const g = goalNow(); return g ? [g.deck, g.place] : null; })()")
    check(g == [5, '5-timeclock-1'], f'S2: at the time clock ({g})')
    pg.ev("clockScreen()"); p = ptr(pg)
    print('  S2 pointer:', p)
    check(p['up'] and p['now'] == 'p:clock:in' and p['text'] == 'Clock in', f'S2: on the clock screen, the pointer on Clock in ({p})')
    pg.ev("POINT.aim.click()"); pg.step(2); pg.ev("document.getElementById('clockScreen').hidden = true"); shift(pg)
    r = pg.ev("({ inn: careerClockedIn(9), live: guideList().some(e => e.id === 'shift:in:9') })"); p = ptr(pg)
    check(r['inn'] and not r['live'] and not p['up'] and pg.ev("!POINT_Q.some(x => x.id === 'p:clock:in')"), f'S2: pressed: clocked in, the entry and the pointer gone ({r}, {p})')
    # S3: take a job (all other open jobs claimed by the crew, so the first row is ours)
    at(pg, 545)
    if not pg.ev("guideTakeable().length"): pg.ev(f"({JOB})('arrows-d1', false)")
    shift(pg); lab = pg.ev(LAB)
    e = pg.ev("guideList().find(e => e.id === 'shift:job:9') || null")
    print('  S3:', lab)
    check(e and e['level'] == 4 and lab == 'Take a job at the board', f'S3: clocked in, a job to take: "Take a job at the board" at level 4 ({lab}, {e})')
    pg.ev("ixBoard.open()"); shift(pg); p = ptr(pg)
    print('  S3 pointer:', p)
    check(p['up'] and p['now'] == 'p:board:take' and p['text'] == 'Take it', f'S3: on the board, the pointer on Take it ({p})')
    pg.ev("POINT.aim.click()"); pg.step(2); shift(pg); lab = pg.ev(LAB); p = ptr(pg)
    mine = pg.ev("myJob() && myJob().id")
    check(mine and lab and lab != 'Take a job at the board' and not p['up'], f'S3: taken: the job\'s own arrow, no pointer ({mine}, {lab}, {p})')
    # pass-over (RV6's T3 note): T3 empty while you hold another job; the next live entry shows
    r = pg.ev("""(() => { const W = SHIP.works, keep = W.cur, now = Math.floor(shipNow());
      SHIP.jobs.push({ id: 'arrows-tj', machine: myJob().machine, deck: 5, kind: 'repair', urgency: 1, posted: now, found: now, claimedBy: null, parts: [], status: 'open' });
      W.cur = { id: 'm4', st: 'do', d: 9, by: 'esposito-yara', j: 'arrows-tj' }; guideTrain();
      guideAsk({ id: 'arrows-q4', level: 4, goal: () => ({ deck: 5, room: 'w', label: 'arrows-q4' }), until: now + 30 });
      GUIDE.key = ''; const g = goalNow(), t3 = guideList().find(e => e.id === 'train:m4:do');
      guideDrop('arrows-q4'); window.__keep = keep; return { lab: g && g.label, t3: !!t3, pick: guidePick() && guidePick().id }; })()""")
    print('  pass-over:', r)
    check(r['t3'] and r['pick'] == 'train:m4:do' and r['lab'] == 'arrows-q4', f'pass-over: T3 (the pick) has nothing to show, the next live entry should ({r})')
    # S7: clock out over a held job and over T3
    at(pg, 1019); shift(pg); lab0 = pg.ev(LAB)
    at(pg, 1020); pg.ev("guideTrain()"); shift(pg); lab = pg.ev(LAB)
    e = pg.ev("guideList().find(e => e.id === 'shift:out:9') || null")
    print('  S7:', lab0, '->', lab, e and e['until'])
    check(lab0 != 'Shift over: clock out', f'S7: not before 17:00 ({lab0})')
    check(e and e['level'] == 4 and e['until'] == B + 1080 and lab == 'Shift over: clock out', f'S7: from 17:00 for an hour, over the held job and T3 ({lab}, {e})')
    pg.ev("{ const k = myJob(); SHIP.jobs = SHIP.jobs.filter(j => j !== k); } MACH_REV++; ixGoalAt = -1; SHIP.player.track = undefined"); lab2 = pg.ev(LAB)
    check(lab2 == 'Shift over: clock out', f'S7: over T3 with your hands free too ({lab2})')
    pg.ev("SHIP.works.cur = __keep; SHIP.jobs = SHIP.jobs.filter(j => j.id !== 'arrows-tj'); GUIDE.list = GUIDE.list.filter(e => !e.id.startsWith('train:')); GUIDE.rev++")
    pg.ev("clearGoal(); clockRmPoint('out')"); d = pg.ev("IX_GOAL && IX_GOAL.label")
    check(d is None, f'S7: section 15\'s direct clock-out arrow should stay off with the queue on ({d})')
    pg.ev("clockScreen()"); p = ptr(pg)
    print('  S7 pointer:', p)
    check(p['up'] and p['now'] == 'p:clock:out' and p['text'] == 'Clock out', f'S7: the pointer on Clock out ({p})')
    pg.ev("POINT.aim.click()"); pg.step(2); pg.ev("document.getElementById('clockScreen').hidden = true"); shift(pg)
    r = pg.ev("({ out: careerClockedOut(9), live: guideList().some(e => e.id === 'shift:out:9'), lab: (GUIDE.key = '', (goalNow() || {}).label || null) })")
    check(r['out'] and not r['live'] and r['lab'] != 'Shift over: clock out', f'S7: pressed: clocked out, gone ({r})')

def part_on2(pg):
    # S5 and S8: turn it in, then the Work log; S6: the empty board; S9: the reputation word; three times at most
    pg.ev("window.__toasts = []; { const t0 = toast; toast = (a, b, o) => { __toasts.push(String(b)); return t0(a, b, o); }; }")
    at(pg, 600); pg.ev("SHIP.career.ci = 8 * 1440 + 540; SHIP.career.co = 0")
    pg.ev("for (const j of SHIP.jobs) if (!j.claimedBy && j.status !== 'done') { j.claimedBy = 'arrows-crew'; } MACH_REV++")
    pg.ev(f"({JOB})('arrows-d2', true); SHIP.player.track = 'arrows-d2'; Object.assign(myJob(), {{ workDone: true }}); ixGoalAt = -1")
    shift(pg); pg.ev("ixBoard.open()"); shift(pg); p = ptr(pg)
    print('  S5 pointer:', p)
    check(p['up'] and p['now'] == 'p:board:turnin' and p['text'] == 'Turn it in', f'S5: the pointer on Turn it in ({p})')
    pg.ev("POINT.aim.click()"); pg.step(2); pg.ev("ixBoard.close()"); shift(pg); p = ptr(pg)
    print('  S8 pointer:', p)
    check(not pg.ev("!!myJob()") and p['up'] and p['now'] == 'p:works:log' and p['label'] == 'Open your device', f'S8: turned in: the pointer on the Device button for the Work log ({p})')
    pg.ev("deviceShow('works'); WORKS_TAB = 'training'; deviceRefresh()"); p = ptr(pg)
    check(p['up'] and p['now'] == 'p:works:log' and p['text'] and p['text'].startswith('Work log'), f'S8: in the Works app, the pointer on the Work log tab ({p})')
    pg.ev("POINT.aim.click()"); p = ptr(pg); pg.ev("deviceClose()")
    check(not p['up'] and pg.ev("!POINT_Q.some(x => x.id === 'p:works:log')"), f'S8: the tab shown: gone ({p})')
    # S6
    pg.ev("window.__oj = openJobs; openJobs = () => []; __toasts.length = 0"); at(pg, 605); shift(pg); pg.ev("ixGoalAt = -1"); pg.step(2); lab = pg.ev(LAB)
    at(pg, 630); shift(pg); n1 = pg.ev("__toasts.filter(t => /Board.s empty/.test(t)).length")
    at(pg, 661); shift(pg); n2 = pg.ev("__toasts.filter(t => /Board.s empty/.test(t)).length")
    pg.ev("SHIP.player.track = null"); at(pg, 721); shift(pg); n3 = pg.ev("__toasts.filter(t => /Board.s empty/.test(t)).length"); pg.ev("SHIP.player.track = undefined")
    pg.ev("openJobs = __oj")
    print('  S6:', lab, n1, n2, n3)
    check(not (lab or '').startswith('Take a job') and n1 == 1 and n2 == 2 and n3 == 2, f'S6: an empty board: no arrow, said once an hour, not with tracking off ({lab}; said {n1}, {n2}, {n3})')
    # S9
    r = pg.ev("""(() => { const W = SHIP.works, keep = W.xp; __toasts.length = 0; guideShift(); const B = WORK_BANDS[W.tier] || WORK_BANDS[1], b0 = worksBand();
      W.xp = 0; guideShift(); const nx = B[1]; W.xp = nx[0]; guideShift(); const t1 = __toasts.slice(); const q = POINT_Q.some(x => x.id === 'p:works:training');
      W.xp = keep; guideShift(); W.xp = nx[0]; guideShift(); const t2 = __toasts.length; W.xp = keep; guideShift(); return { b0, b1: nx[1], t1, q, t2 }; })()""")
    print('  S9:', r)
    if check(r is not None, 'S9: (no higher reputation word to reach)'):
        check(len(r['t1']) == 1 and r['t1'][0].startswith('Works reputation: ') and r['q'], f'S9: a new word: a toast and the Training tab pointer ({r})')
        check(r['t2'] == 1, f'S9: the same word again: said once only ({r})')
    # three times at most
    r = pg.ev("""(() => { SHIP.device.pointsSeen['p:clock:out'] = 3; pointDrop('p:clock:out'); const now = Math.floor(shipNow());
      setShipNow(8 * 1440 + 1030); SHIP.career.co = 0; guideShift(); const q = POINT_Q.some(x => x.id === 'p:clock:out'); setShipNow(now); return q; })()""")
    check(not r, f'pointers: a fourth time is not asked ({r})')

def part_tick(pg):
    at(pg, 478); pg.ev("GUIDE.list.length = 0; GUIDE.rev++; guideStart()")
    for _ in range(60):
        pg.step(15)
        if pg.ev('Math.floor(shipNow())') > B + 481: break
    has = pg.ev("guideList().some(e => e.id === 'shift:in:9')")
    check(has, 'tick: the minute tick did not ask the shift chain')

def part_off(pg):
    at(pg, 480); pg.step(30); r = pg.ev("({ list: GUIDE.list.length, q: POINT_Q.length, on: GUIDE_ON })")
    check(r['list'] == 0 and r['q'] == 0 and not r['on'], f'off: no entries, no pointer ({r})')
    at(pg, 1020); pg.ev("SHIP.career.ci = 8 * 1440 + 540; SHIP.career.co = 0; clearGoal(); clockRmPoint('out')"); d = pg.ev("IX_GOAL && IX_GOAL.label")
    check(d and 'lock out' in d, f'off: section 15\'s clock-out arrow as before ({d})')

with sync_playwright() as pw:
    path = sys.argv[1] if len(sys.argv) > 1 else 'starship-cadet.html'
    src = pathlib.Path(path).read_text()
    if check('const POINT_ON = false;' in src and 'function guideShift' in src, 'the build has piece D (guideShift) and the pointer switch'):
        on = WORK / 'test' / ('_d_on_' + pathlib.Path(path).name)
        on.write_text(src.replace('const POINT_ON = false;', 'const POINT_ON = true;', 1))
        b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
        ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
        for name, fn, p, guide in (('off', part_off, path, False), ('on: S2, S3, pass-over, S7', part_on, str(on), True), ('on: S5, S8, S6, S9', part_on2, str(on), True), ('tick', part_tick, str(on), True)):
            print('==', name)
            try:
                pg = Page(ctx, p, 'on' if guide else 'off'); pg.day9(guide); fn(pg)
                check(not pg.errors, f'{name}: page errors {pg.errors[:3]}')
                pg.page.close()
            except Exception as e: check(False, f'{name}: stopped: {str(e)[:300]}')
        b.close()

print('arrows_d_check: OK' if ok else 'arrows_d_check: FAILED')
sys.exit(0 if ok else 1)
