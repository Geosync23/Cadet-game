# Starship Cadet: the arrows plan's piece D (AC2), the shift chain S1-S9 (plans/arrows-pillar5-plan.html, "Step 1").
# In a copy of the build with POINT_ON true and GUIDE_ON set true while it runs, at 390 x 844, Day 9 (an ordinary
# workday), on paper (the clock set by hand, guideShift called by hand, except "tick"):
#   clock in (S2):  nothing before 08:00; from 08:00 a level-4 "Clock in" entry at the time clock; on the clock screen
#                   the pointer on Clock in; pressed: clocked in, the entry and the pointer gone
#   take a job (S3): clocked in with a job you can take: "Take a job at the board"; on the board the pointer on the
#                   first row's Take it (a held one first); taken: the job's own arrow, no pointer
#   turn it in (S5): the work done: the pointer on Turn it in; turned in: S8, the device pointer to the Works app's Work
#                   log, gone once the tab shows
#   empty (S6):     nothing to take (a row without a Take it counts as nothing): no arrow; FX1's "Nothing on the board" said, but not in a meeting (held till it ends)
#   S1 (FX1's row): tracking today's On shift row leaves no direct arrow, so the queue's Clock in leads
#   the meeting (RV6's E item 5): FX1's trainArrow puts no arrow up while the queue is on; T1 leads
#   clock out (S7): from 17:00 (15:30 on a short Friday, until 16:00) "Shift over: clock out" over a job still in hand and over T3 (your training turn), for an
#                   hour; the pointer on Clock out; pressed: gone. Section 15's direct clock-out arrow stays off
#   after clock-out: a job you hold has no arrow (nor Turn it in), and stays in Tracked
#   pass-over:      an entry with nothing to show (T3 while you hold another job) gives way to the next live one
#   reputation (S9): a new word reached: a toast once; never again for that word (a word first met on a drop still is, when reached going up); a drop: the toast "Works reputation down: <word>" only
#   pointers:       each panel pointer three times at most, then not asked
#   inspection:     on an inspection morning, 06:00-06:30, FX3's inspectGoal through the queue at level 2
#   pop-ups:        six at once: a training's word ("Trained: ...") still waits its turn, another is dropped
#   tick:           guideTick asks the shift chain itself once a ship minute
#   the drill:      (the build as it is) the 14:50 drill arrow has no trk tag and stays up once you reach the Works bay
# And in the build as it is (both off): no entries, no pointer, section 15's clock-out arrow as before.
# Setup as cadet_test.py (playwright, three r128 in $CADET_WORK/three).  Run:  python3 arrows_d_check.py BUILD.html
import sys, json, re, os, pathlib
from playwright.sync_api import sync_playwright

WORK = pathlib.Path(os.environ.get('CADET_WORK', '/tmp/cadet-work'))
RUN_ID = f'p{os.getpid()}_'   # FX18-1: this run's copies carry the process id (two runs in one CADET_WORK never open each other's), gone at exit
__import__('atexit').register(lambda: [f.unlink(missing_ok=True) for f in (WORK / 'test').glob(f'*_{RUN_ID}*') if f.is_file()])
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
        tmp = WORK / 'test' / ('_arrows_d_' + RUN_ID + tag + '_' + pathlib.Path(path).name)
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
    r = pg.ev("""(() => { setGoal({ deck: 3, room: 'w', label: 'old arrow' }); const it = trkItems().find(x => x.work); if (!it) return null; const t = trkTap(it.key); return { t, sub: it.sub, direct: IX_GOAL && IX_GOAL.label, track: SHIP.player.track === null ? 'off' : 'on' }; })()""")
    print('  S1:', r)
    check(r and r['t'] and r['direct'] is None and r['track'] == 'on' and '08:00' in r['sub'], f'S1: tracking On shift: no direct arrow, tracking on, "the clock opens at 08:00" ({r})')
    at(pg, 480); shift(pg)
    e = pg.ev("guideList().find(e => e.id === 'shift:in:9') || null"); lab = pg.ev(LAB)
    print('  S2:', lab, e and e['level'])
    check(e and e['level'] == 4 and lab == 'Clock in: shift at 09:00', f'S2: from 08:00 a level-4 "Clock in" entry ({lab}, {e})')
    g = pg.ev("(() => { GUIDE.key = ''; const g = goalNow(); return g ? [g.deck, g.place] : null; })()")
    check(g == [5, '5-timeclock-1'], f'S2: at the time clock ({g})')
    pg.ev("clockScreen()"); p = ptr(pg)
    print('  S2 pointer:', p)
    check(p['up'] and p['now'] == 'p:clock:in' and p['text'] == 'Clock in', f'S2: on the clock screen, the pointer on Clock in ({p})')
    pg.step(30); pg.ev("POINT.aim.click()"); pg.step(2); pg.ev("document.getElementById('clockScreen').hidden = true"); shift(pg)   # (R3, 0.95.0) step past patch #6's 500 ms tap guard first: the check's clock only moves with step
    r = pg.ev("({ inn: careerClockedIn(9), live: guideList().some(e => e.id === 'shift:in:9') })"); p = ptr(pg)
    check(r['inn'] and not r['live'] and not p['up'] and pg.ev("!POINT_Q.some(x => x.id === 'p:clock:in')"), f'S2: pressed: clocked in, the entry and the pointer gone ({r}, {p})')
    # S3: take a job (all other open jobs claimed by the crew, so the first row is ours)
    at(pg, 545)
    if not pg.ev("guideTakeable().length"): pg.ev(f"({JOB})('arrows-d1', false)")
    shift(pg); lab = pg.ev(LAB)
    e = pg.ev("guideList().find(e => e.id === 'shift:job:9') || null")
    # (RV16, 0.93.1) Day 9 is the Tier 2 test day: with the test on the board the arrow names it ("Your Tier 2 test job") and
    # the pointer marks its Take it (FX10/FX15's lesson rule). Before 0.93.1 this check's own clock step back (07:50.2 -> 07:50)
    # let the board drop the not-yet-posted test job, so S3 saw a plain board; it no longer does
    les = pg.ev("(() => { const l = boardLesson(); return l ? 'Your ' + boardLessonName(l) : null; })()")
    print('  S3:', lab, '(a lesson on the board: ' + les + ')' if les else '')
    want = les or 'Take a job at the board'
    check(e and e['level'] == 4 and lab == want, f'S3: clocked in, a job to take: "{want}" at level 4 ({lab}, {e})')
    pg.ev("ixBoard.open()"); shift(pg); p = ptr(pg)
    print('  S3 pointer:', p)
    check(p['up'] and p['text'] == 'Take it' and (p['now'].startswith('p:board:lesson:') if les else p['now'] == 'p:board:take'), f'S3: on the board, the pointer on Take it ({"the lesson" if les else "the first row"}) ({p})')
    pg.ev("POINT.aim.click()"); pg.step(2); shift(pg); lab = pg.ev(LAB); p = ptr(pg)
    mine = pg.ev("myJob() && myJob().id")
    check(mine and lab and lab != 'Take a job at the board' and not p['up'], f'S3: taken: the job\'s own arrow, no pointer ({mine}, {lab}, {p})')
    # only a round on the board (a registered kind, not a machine job): S3 still says take a job (RV7)
    r = pg.ev("""(() => { const keep = openJobs, t = shipNow(); const mj = myJob(); if (mj) mj.claimedBy = 'arrows-away';
      SHIP.jobs.push({ id: 'arrows-round', kind: 'rounds', deck: 4, room: 'l', route: [], marks: {}, title: 'Your first round', urgency: 1, posted: t, found: t, claimedBy: null, parts: [], status: 'open' });
      openJobs = () => [{ id: 'arrows-round', asked: true }]; guideShift(); GUIDE.key = ''; const g = goalNow(), L = guideTakeable().map(o => o.id);
      openJobs = keep; SHIP.jobs = SHIP.jobs.filter(j => j.id !== 'arrows-round'); if (mj) mj.claimedBy = 'you'; return { lab: g && g.label, L }; })()""")
    print('  S3, only a round:', r)
    check(r['L'] == ['arrows-round'] and r['lab'] == 'Take a job at the board', f'S3: a round on the board counts as a job to take (the board\'s own rule) ({r})')
    # a job held for you comes first on the pointer's list (RV6's note)
    r = pg.ev("""(() => { const keep = openJobs; openJobs = () => [{ id: 'arrows-a', asked: false }, { id: 'arrows-h', asked: true }];
      const t = shipNow(), m = machineList().find(m => !m.stub); for (const id of ['arrows-a', 'arrows-h']) SHIP.jobs.push({ id, machine: m.id, deck: m.deck, kind: 'service', urgency: 1, posted: t, found: t, claimedBy: null, parts: [], status: 'open' });
      const L = guideTakeable().map(o => o.id); openJobs = keep; SHIP.jobs = SHIP.jobs.filter(j => !j.id.startsWith('arrows-a') && j.id !== 'arrows-h'); return L; })()""")
    check(r == ['arrows-h', 'arrows-a'], f'S3: a job held for you first ({r})')
    # pass-over (RV6's T3 note): T3 empty while you hold another job; the next live entry shows
    r = pg.ev("""(() => { const W = SHIP.works, keep = W.cur, now = Math.floor(shipNow());
      SHIP.jobs.push({ id: 'arrows-tj', machine: myJob().machine, deck: 5, kind: 'repair', urgency: 1, posted: now, found: now, claimedBy: null, parts: [], status: 'open' });
      W.cur = { id: 'm4', st: 'do', d: 9, by: 'esposito-yara', j: 'arrows-tj' }; guideTrain();
      guideAsk({ id: 'arrows-q4', level: 4, goal: () => ({ deck: 5, room: 'w', label: 'arrows-q4' }), until: now + 30 });
      GUIDE.key = ''; const g = goalNow(), t3 = guideList().find(e => e.id === 'train:m4:do:9');   /* (DS1, patch 0.92.5 #12: T3 is per day) */
      guideDrop('arrows-q4'); window.__keep = keep; return { lab: g && g.label, t3: !!t3, pick: guidePick() && guidePick().id }; })()""")
    print('  pass-over:', r)
    check(r['t3'] and r['pick'] == 'train:m4:do:9' and r['lab'] == 'arrows-q4', f'pass-over: T3 (the pick) has nothing to show, the next live entry should ({r})')
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
    pg.step(30); pg.ev("POINT.aim.click()"); pg.step(2); pg.ev("document.getElementById('clockScreen').hidden = true"); shift(pg)
    r = pg.ev("({ out: careerClockedOut(9), live: guideList().some(e => e.id === 'shift:out:9'), lab: (GUIDE.key = '', (goalNow() || {}).label || null) })")
    check(r['out'] and not r['live'] and r['lab'] != 'Shift over: clock out', f'S7: pressed: clocked out, gone ({r})')
    # clocked out: the job arrow rests (lead 29: off shift you're free); a job you hold stays in Tracked
    pg.ev(f"({JOB})('arrows-late', true); SHIP.player.track = 'arrows-late'; ixGoalAt = -1"); pg.step(3)
    r = pg.ev("(() => { GUIDE.key = ''; const g = goalNow(); return { lab: g && g.label, step: (ixJobStep() || {}).label || null, row: trkItems().some(x => x.job === 'arrows-late') }; })()")
    Object_done = pg.ev("Object.assign(myJob(), { workDone: true }); ixGoalAt = -1; (ixJobStep() || {}).label || null")
    pg.ev("SHIP.jobs = SHIP.jobs.filter(j => j.id !== 'arrows-late'); MACH_REV++; ixGoalAt = -1")
    print('  after clock-out, a held job:', r, Object_done)
    check(r['lab'] is None and r['step'] is None and Object_done is None and r['row'], f'after clock-out: no job arrow (its steps or Turn it in), the job still in Tracked (lead 29) ({r}, {Object_done})')

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
    # S6: nothing with a Take it (a row without one counts as nothing): no arrow; FX1's word said (boardEmptySay)
    # (FX19, 0.92.6: with PROMO_SIGHT_ON the Day 8 career's test is offered at once and runs on Day 9, its stage 'do' all day,
    # and boardEmptySay rightly holds its word in a training or test; the empty board is tried with nothing under way, then put back)
    pg.ev("window.__kc = SHIP.works ? SHIP.works.cur : null; if (SHIP.works) SHIP.works.cur = null")
    pg.ev("window.__oj = openJobs; openJobs = () => [{ id: 'arrows-none', asked: false }]; __toasts.length = 0; if (boardEmptySay.s) boardEmptySay.s.dry = false, boardEmptySay.s.at = -1e9")
    at(pg, 605); shift(pg); pg.ev("ixGoalAt = -1"); pg.step(2); lab = pg.ev(LAB); n1 = pg.ev("__toasts.filter(t => /Nothing on the board/.test(t)).length")
    hold = pg.ev("""(() => { boardEmptySay.s.dry = false; boardEmptySay.s.at = -1e9; __toasts.length = 0; const now = Math.floor(shipNow()), occ = { key: 'arrows-occ4', deck: 5, room: 'r', at: now - 2, len: 15, status: 'asked' };
      SHIP.occasions.push(occ); boardEmptySay(true, now); const inMeet = __toasts.length; SHIP.occasions.splice(SHIP.occasions.indexOf(occ), 1); boardEmptySay(true, now + 1); return [inMeet, __toasts.length]; })()""")
    hold2 = pg.ev("""(() => { const say = () => { boardEmptySay.s.dry = false; boardEmptySay.s.at = -1e9; __toasts.length = 0; boardEmptySay(true, Math.floor(shipNow())); return __toasts.length; };
      const W = SHIP.works, keep = W.cur, dk = DIALOGUE, out = {};
      DIALOGUE = { arrows: true }; out.dialogue = say(); DIALOGUE = dk;
      W.cur = { id: 'm4', st: 'watch', d: 9, by: 'esposito-yara' }; out.watch = say(); W.cur.st = 'do'; out.doo = say(); W.cur = keep; out.free = say(); return out; })()""")
    pg.ev("openJobs = __oj; if (SHIP.works) SHIP.works.cur = __kc")
    print('  S6:', lab, n1, 'in a meeting, then after:', hold, '| in a dialogue, a watch, a turn, then free:', hold2)
    check(hold2 == {'dialogue': 0, 'watch': 0, 'doo': 0, 'free': 1}, f'S6: the board\'s word waits through a dialogue and a training\'s watch and turn (RV7) ({hold2})')
    check(hold == [0, 1], f'S6: the board\'s word waits through a meeting, then is said (lead 29) ({hold})')
    check(not (lab or '').startswith('Take a job') and n1 == 1, f'S6: an empty board: no arrow, and the board\'s word said ({lab}; said {n1})')
    # S9: up to a new word: said with the pointer; up to it again: not said; a drop: "Works reputation down: <word>"
    r = pg.ev("""(() => { const W = SHIP.works, keep = W.xp, B = WORK_BANDS[W.tier] || WORK_BANDS[1], b0 = worksBand(); guideShift();
      W.xp = 0; guideShift(); __toasts.length = 0; W.xp = B[1][0]; guideShift(); const t1 = __toasts.slice(), q = POINT_Q.some(x => x.id === 'p:works:training');
      __toasts.length = 0; W.xp = 0; guideShift(); const down = __toasts.slice(); __toasts.length = 0; W.xp = B[1][0]; guideShift(); const t2 = __toasts.slice();
      W.xp = keep; guideShift(); __toasts.length = 0; W.xp = B[3][0]; guideShift(); const down2 = __toasts.slice(); W.xp = keep; guideShift();
      __toasts.length = 0; W.xp = B[2][0]; guideShift(); W.xp = B[1][0]; guideShift(); W.xp = B[2][0]; guideShift(); const back = __toasts.slice(); W.xp = keep; guideShift(); return { b0, t1, q, down, t2, down2, back }; })()""")
    print('  S9:', r)
    check(r['t1'] == ['Works reputation: Steady'] and r['q'], f'S9: a new word: a toast and the Training tab pointer ({r})')
    check(r['t2'] == [], f'S9: the same word reached again: not said again ({r})')
    check(r['back'][-1:] == ['Works reputation: Reliable'], f'S9: a word first met by a drop is said when later reached going up (RV7) ({r})')
    check(r['down'] == ['Works reputation down: New'] and r['down2'] == ['Works reputation down: Trusted'], f'S9: a drop says it went down, even to a word not yet reached (lead 29, RV6) ({r})')
    # a short Friday: clock out from 15:30, until the clock signs you out at 16:00
    r = pg.ev("""(() => { const now = Math.floor(shipNow()), ci = SHIP.career.ci, co = SHIP.career.co; let d = 9; while (!friShort(d) && d < 16) d++; if (!friShort(d)) return null;
      const b = (d - 1) * 1440; setShipNow(b + 935); SHIP.career.ci = b + 540; SHIP.career.co = 0; guideShift(); const e = guideList().find(x => x.id === 'shift:out:' + d) || null;
      guideDrop('shift:out:' + d); guideDrop('shift:job:' + d); SHIP.career.ci = ci; SHIP.career.co = co; setShipNow(now); return { d, from: e && e.from - b, until: e && e.until - b }; })()""")
    print('  short Friday:', r)
    if check(r is not None, 'Friday: (no short Friday found)'): check(r['from'] == 930 and r['until'] == 960, f'S7: on a short Friday from 15:30 until 16:00 ({r})')
    # the meeting: trainArrow puts nothing up while the queue is on; T1 leads (RV6's E item 5)
    r = pg.ev("""(() => { const W = SHIP.works, keep = W.cur, now = Math.floor(shipNow()), occ = { key: 'arrows-occ3', id: 'works.m4', deck: 5, room: 'r', at: now + 10, len: 15, status: 'asked' };
      SHIP.occasions.push(occ); W.cur = { id: 'm4', st: 'meet', d: 9, by: 'esposito-yara', occ: 'arrows-occ3', told: true }; clearGoal();
      trainArrow(W.cur, now); const direct = IX_GOAL && IX_GOAL.label; guideTrain(); GUIDE.key = ''; const g = goalNow();
      W.cur = keep; SHIP.occasions.splice(SHIP.occasions.indexOf(occ), 1); GUIDE.list = GUIDE.list.filter(e => !e.id.startsWith('train:')); GUIDE.rev++; clearGoal();
      return { direct, lab: g && g.label }; })()""")
    print('  meeting:', r)
    check(r['direct'] is None and 'meet Yara' in str(r['lab']), f'meeting: no direct arrow from trainArrow with the queue on; T1 leads ({r})')
    # the pop-up queue never drops a training's word (lead 29, RV7: "Trained: rounds" was lost when six came at once)
    r = pg.ev("""(() => { GUIDE.tq.length = 0; toast('A', 'first, on screen'); TOAST_AT = performance.now();
      toast('Zeke Torres', 'Trained: rounds, with Zeke Torres.'); for (const k of [2, 3, 4, 5]) toast('B', 'pop-up ' + k);
      const q = GUIDE.tq.map(x => x[1]); GUIDE.tq.length = 0; return q; })()""")
    print('  pop-ups waiting after six at once:', r)
    check('Trained: rounds, with Zeke Torres.' in r and len(r) <= 3, f'pop-ups: a training\'s word is kept when the queue is full, something else goes ({r})')
    # the inspection morning (F2): FX3's arrows through the queue, level 2, 06:00-06:30
    r = pg.ev("""(() => { if (typeof inspectGoal !== 'function') return null; const keep = inspectDue, now = Math.floor(shipNow()); inspectDue = () => true; clearGoal();
      setShipNow(8 * 1440 + 361); GUIDE.key = ''; guideShift(); const e = guideList().find(x => x.id === 'inspect:9') || null; GUIDE.key = ''; const g = goalNow(), want = inspectGoal(9);
      setShipNow(8 * 1440 + 391); GUIDE.key = ''; const after = (goalNow() || {}).label || null, live = guideList().some(x => x.id === 'inspect:9');
      inspectDue = keep; setShipNow(now); GUIDE.key = ''; return { level: e && e.level, lab: g && g.label, want: want && want.label, after, live }; })()""")
    print('  inspection morning:', r)
    if check(r is not None, 'inspection: (no inspectGoal in this build)'):
        check(r['level'] == 2 and r['want'] and r['lab'] == r['want'] and not r['live'] and r['after'] != r['want'], f'inspection: from 06:00 the queue shows FX3\'s arrow at level 2, gone at 06:30 ({r})')
    # three times at most
    r = pg.ev("""(() => { SHIP.device.pointsSeen['p:clock:out'] = 3; pointDrop('p:clock:out'); const now = Math.floor(shipNow());
      setShipNow(8 * 1440 + 1030); SHIP.career.co = 0; guideShift(); const q = POINT_Q.some(x => x.id === 'p:clock:out'); setShipNow(now); return q; })()""")
    check(not r, f'pointers: a fourth time is not asked ({r})')

def part_drill(pg):                                  # the 14:50 drill arrow stays up once you're in the Works bay (FX2's own line; RV7)
    pg.ev("devmodeRun('Set career', () => devmodeSetCareerTo(2))"); pg.step(20); d = 3   # Day 3, a Wednesday: your first drill (a junior's)
    pg.ev(f"devmodeSkipTo({(d - 1) * 1440 + 14 * 60 + 40}); clearGoal(); SHIP.player.track = undefined; while (typeof TIP_Q !== 'undefined' && TIP_Q.length) tipDone()"); pg.step(10)
    for _ in range(200):
        pg.step(10, 50)
        if pg.ev(f"shipNow() >= {(d - 1) * 1440 + 14 * 60 + 51}"): break
    r = pg.ev("(() => { const g = IX_GOAL; return g && { label: g.label, drill: !!g.drill, trk: g.trk || null }; })()")
    if not check(r and r['drill'], f'drill: the 14:50 arrow is up ({r}; {pg.ev("[clockText(), !!drillJobOf(SHIP.time.day), (drillJobOf(SHIP.time.day) || {}).told]")})'): return
    pg.ev("goToDeck(5)"); pg.step(5)
    pg.ev("(() => { const P = player.obj.position; P.x += 30; })()"); pg.step(3)   # away first (trkDoneCheck's rule)
    pg.ev("(() => { const w = ixGoalWorld(IX_GOAL), c = nearestOpen(w.x, w.z, player); player.obj.position.copy(cellPos(...c)); player.stop(); })()"); pg.step(5)
    r2 = pg.ev("(() => { const g = IX_GOAL; return g ? g.label : null; })()")
    print('  drill:', r, '-> in the Works bay:', r2)
    check(r2 is not None and not r['trk'], f'drill: the arrow stays up once you reach the Works bay (no trk tag; FX2\'s stop arrows follow) ({r}, {r2})')

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

def arrows_off(src):                                 # the build with the teaching arrows switched off (as before 0.92.0), for the parts that test "off"
    return src.replace('const POINT_ON = true;', 'const POINT_ON = false;', 1).replace('var GUIDE_ON = true;', 'var GUIDE_ON = false;', 1)

with sync_playwright() as pw:
    path = sys.argv[1] if len(sys.argv) > 1 else 'starship-cadet.html'
    src = arrows_off(pathlib.Path(path).read_text())
    if check('const POINT_ON = false;' in src and 'function guideShift' in src, 'the build has piece D (guideShift) and the pointer switch'):
        on = WORK / 'test' / ('_d_on_' + RUN_ID + pathlib.Path(path).name)
        on.write_text(src.replace('const POINT_ON = false;', 'const POINT_ON = true;', 1))
        off = WORK / 'test' / ('_d_off_' + RUN_ID + pathlib.Path(path).name); off.write_text(src); path = str(off)
        b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
        ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
        for name, fn, p, guide in (('off', part_off, path, False), ('on: S2, S3, pass-over, S7', part_on, str(on), True), ('on: S5, S8, S6, S9', part_on2, str(on), True), ('tick', part_tick, str(on), True), ('the drill arrow', part_drill, path, False)):
            print('==', name)
            try:
                pg = Page(ctx, p, 'on' if guide else 'off'); pg.day9(guide); fn(pg)
                check(not pg.errors, f'{name}: page errors {pg.errors[:3]}')
                pg.page.close()
            except Exception as e: check(False, f'{name}: stopped: {str(e)[:300]}')
        b.close()

print('arrows_d_check: OK' if ok else 'arrows_d_check: FAILED')
sys.exit(0 if ok else 1)
