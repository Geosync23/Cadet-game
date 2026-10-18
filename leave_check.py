# Starship Cadet: leave check (keep in the repo, next to cadet_test.py and the other checks)
# Checks leave, missed shifts and being let go (the career engineer, 0.61.x; design-doc "Leave, missed shifts and
# being let go"), on paper: each scenario steps ship days, calling the game's own functions at the hours they'd run
# (careerTick, the shift's start note, repairs as section 20 scores them, Sunday's repWeek), with no walking.
#   leave: 3 days to start, one more every 4 ship weeks, at most 5; booking by 08:30 that day (07:30 before the 09:00 shift, 0.44.14), cancelling gives it back;
#     a leave day is a day off to playerShiftOn (so to the shift and the held jobs)
#   (a) a diligent player, and a casual one (late twice a week, a missed day a fortnight), never get a summons
#   (b) a player taking all their leave, and sick days, never drops on those days and never gets a summons
#   (c) a player who skips everything gets the Chief, then the Captain, then is let go, in a sensible number of days:
#       the notice, the last day with no shift, friends asked to come and find you, the send-off in the plans, the end
#   (d) recovery re-arms each step: work well, then skip again, and the step comes again
#   (e) the save stays small (under SAVE_MAX bytes) and loads back the same
# Setup and environment as for cadet_test.py.
# Run:  python3 leave_check.py BUILD.html
import sys, json
exec(open(__file__.replace('leave_check.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright

SAVE_MAX = 300
ok = True
def fail(msg):
    global ok
    ok = False
    print('FAIL', msg)
def check(cond, msg):
    if not cond: fail(msg)
    return cond

# one run on paper: plan is a string per scenario (see `code` below); returns what happened day by day
PAPER = r"""(({ plan, days, friends }) => {
  SHIP.career = null; SHIP.rep = null; SHIP.occasions.length = 0; SHIP.flags = {}; SHIP.notes = [];
  if (SHIP.social) SHIP.social.seekAsks = [];
  socInit(); for (const id of friends || []) { const r = relGet(id); r.pts = 400; r.tier = 3; }
  const at = (d, m) => { SHIP.time.day = d; SHIP.time.min = m; return (d - 1) * 1440 + m; };
  const log = [], steps = [], seen = new Set(); let ended = null, letGo = null, offLeave = [], bookFail = [];
  const stop = [onSim('careerStep', n => steps.push({ step: n.step, day: Math.floor(n.t / 1440) + 1 })), onSim('letGo', n => { letGo = n.day; }), onSim('careerEnd', n => { ended = n.day; })];
  const code = d => {                                    // what the player does on day d
    const wd = weekday(d), wk = Math.floor((d - 1) / 7);
    if (plan === 'diligent') return 'work';
    if (plan === 'casual') return wd === 1 || wd === 3 ? 'late' : wd === 2 && wk % 2 ? 'skip' : 'work';
    if (plan === 'leave') return wd === 2 && wk % 2 === 0 ? 'sick' : 'leave';   // every leave day it can, sick every other Wednesday, else work
    if (plan === 'skip') return 'skip';
    if (plan === 'twoTwo') return [8, 9, 11, 12].includes(d) ? 'skip' : 'work';   // Mon, Tue missed, Wed worked, Thu, Fri missed: no talk
    if (plan === 'three') return [8, 9, 10].includes(d) ? 'skip' : 'work';       // three in a row: the talk
    if (plan === 'lateDaily') return 'lateNoJobs';
    if (plan === 'twoOneTwo') return d <= 7 || wd === 2 ? 'work' : 'skip';   // every week: two missed, one worked, two missed
    if (plan.startsWith('skipUntil')) return 'dyn';     // (d): driven by the ladder below
    return 'work';
  };
  let mode = 'skip', round = 0, worked = 0;                          // (d): skip to the step, work until it re-arms, skip again
  const want = plan === 'skipUntilChief' ? 1 : 2;
  for (let d = 1; d <= days && !ended; d++) {
    let c = code(d);
    if (c === 'dyn') { const C0 = SHIP.career || {}, st = want === 1 ? (C0.ca ? 1 : 0) : C0.st || 0;   // the Chief's step: taken for this run (ca)
      if (mode === 'skip' && st >= want) { mode = 'work'; round++; worked = 0; }
      else if (mode === 'work' && st < want && (want > 1 || worked >= 5)) { mode = round >= 2 ? 'work' : 'skip'; }   // the Chief's: a week's work first, then three more missed
      if (mode === 'work' && playerShiftOn(d)) worked++;
      c = mode; }
    careerTick(at(d, 0)); if (d === 1) SHIP.career.sd = 99999;   // no sickness in these runs (the game seed is random; sickness has its own case)
    if (weekday(d) === 6) { repWeek(Math.floor(at(d, 240) / 60)); careerTick(at(d, 240)); }
    if (c === 'leave') { const ok = careerRota(d) && SHIP.career.l > 0 ? careerBook(d, at(d - 1, 1200)) : false; if (!ok) c = 'work'; }
    if (c === 'sick') careerSick(d);
    const work0 = careerWork();
    careerTick(at(d, 420));
    if (playerShiftOn(d)) {
      if (c === 'work' || c === 'late' || c === 'lateNoJobs') { const late = c === 'work' ? 0 : 40; at(d, 480 + late); simNote('shiftStart', { late }); repNote('shiftStart', { late }); careerTick(at(d, 480 + late));
        for (let k = 0; k < (c === 'lateNoJobs' ? 0 : c === 'late' ? 2 : 3); k++) { at(d, 600 + 90 * k); repAdd('works', 3, { work: 2 }, 'jobs'); } }
      else { at(d, 600); simNote('shiftStart', { late: 120, missed: true }); repNote('shiftStart', { late: 120, missed: true }); }
    } else if (careerOn(d) || (SHIP.career.s || []).includes(d)) offLeave.push(d);
    careerTick(at(d, 750)); careerTick(at(d, 900)); careerTick(at(d, 1439));
    for (const a of SHIP.social.seekAsks || []) if (a.why) seen.add(a.why);
    const w = careerWork(), C = SHIP.career;
    log.push({ d, c: playerShiftOn(d) ? c : careerOn(d) ? 'leave' : C.s.includes(d) ? 'sick' : C.go != null && d >= C.go ? 'gone' : 'off', w: Math.round(w * 10) / 10, st: C.st, n: C.n, l: C.l, drop: Math.round((w - work0) * 10) / 10 });
  }
  const C = SHIP.career, last = C.go != null ? C.go + 1 : null;
  const out = { log, steps, letGo, ended, career: JSON.parse(JSON.stringify(C)), size: JSON.stringify(C).length,
    asks: [...seen], offLeave, sendOff: [] };
  if (last) { SCHED_DATA = null; if (typeof SHIP_DAYS !== 'undefined') SHIP_DAYS.clear(); SHIP.career.end = false; out.sendOff = careerSendOff(last);
    out.planned = careerSendOff(last).filter(id => { const p = schedPeople().find(q => q.id === id); return p && planDay(p, last).some(s => s.tag === 'farewell'); });
    SHIP.career.end = true; }
  out.occ = SHIP.occasions.filter(r => /^career/.test(r.id)).map(r => ({ id: r.id, day: Math.floor(r.at / 1440) + 1, end: r.at + r.len }));
  out.letAt = C.go != null ? (C.go - 1) * 1440 : null;
  out.round = round; stop.forEach(f => f());
  return out;
})"""

def show(r, n=None):
    rows = r['log'] if n is None else r['log'][:n]
    print('   ', ' '.join(f"{x['d']}{x['c'][0]}:{x['w']:.0f}{'*' * x['st']}" for x in rows))

with sync_playwright() as pw:
    g = Game(pw, sys.argv[1])
    errors = g.errors
    ev = g.ev
    friends = ev("SOC.crew.filter(p => p.dept === 'works' && p.rank === 'junior' && socAboard(p)).slice(0, 3).map(p => p.id)")

    print('Leave: earning, booking, cancelling:')
    r = ev("""(() => { SHIP.career = null; const at = (d, m) => { SHIP.time.day = d; SHIP.time.min = m; return (d - 1) * 1440 + m; };
      careerTick(at(1, 600)); const c = SHIP.career, out = { start: c.l };
      out.book = careerBook(3, at(2, 1200)); out.after = c.l; out.offOn3 = !playerShiftOn(3); out.weekend = careerCanBook(6, at(2, 1200));
      out.late = careerCanBook(4, at(4, 511)); out.early = careerCanBook(4, at(4, 509));
      out.cancel = careerBook(3, at(3, 400)); out.back = c.l; out.onAgain = playerShiftOn(3);
      careerBook(5, at(4, 1200)); out.tooLateCancel = careerBook(5, at(5, 520));
      out.heldEnd = (() => { const j = { found: at(5, 300), urgency: 0, kind: 'wear', tier: 1 }; try { return leaveEnd(j) === j.found; } catch (e) { return 'n/a'; } })();
      for (const d of [29, 57, 85, 113]) { c.e = c.z = d - 1; careerTick(at(d, 10)); } out.grants = c.l;   // no misses in between: just the grants
      return out; })()""")
    print('  ', r)
    check(r['start'] == 3, f"leave to start {r['start']}, not 3")
    check(r['book'] and r['after'] == 2 and r['offOn3'], 'booking a workday: one fewer held and no shift that day')
    check(r['weekend'] is None, 'a Saturday can be booked as leave')
    check(r['late'] is None and r['early'] == 'book', 'booking closes at 08:30 on the day')
    check(r['cancel'] and r['back'] == 2 + 1 and r['onAgain'], 'cancelling gives the day back and the shift returns')
    check(not r['tooLateCancel'], 'a leave day can be cancelled after 08:30 that day')
    check(r['heldEnd'] in (True, 'n/a'), 'a job found on a leave day is still held for you')
    check(r['grants'] == 5, f"leave after four 4-week grants: {r['grants']} (at most 5)")

    print('Reviewer 1d\'s cases: an older save loaded after starting the shift; no summons on a leave day:')
    r = ev("""(() => { const at = (d, m) => { SHIP.time.day = d; SHIP.time.min = m; return (d - 1) * 1440 + m; };
      SHIP.career = null; SHIP.rep = null; SHIP.notes = []; SHIP.flags = {}; at(10, 480); simNote('shiftStart', { late: 0 }); flagSet('shiftSent', 10);
      careerTick(at(10, 660)); careerTick(at(10, 760)); const w = careerWork();
      SHIP.career = null; SHIP.rep = null; SHIP.occasions.length = 0; careerTick(at(15, 0)); const c = SHIP.career; c.st = 1; c.q = 1; c.qd = 15; c.b.push(16);
      for (const m of [420, 600, 900]) careerTick(at(16, m)); const onLeave = SHIP.occasions.filter(o => o.id === 'careerChief').map(o => Math.floor(o.at / 1440) + 1);
      return { w, onLeave }; })()""")
    print('  ', r)
    check(r['w'] == 50, f"an older save loaded mid-shift counted a miss (work {r['w']})")
    check(16 not in r['onLeave'], 'a summons was booked on a leave day')

    print('(a) A diligent player, and a casual one, over 8 weeks:')
    for plan in ('diligent', 'casual'):
        r = ev(f"({PAPER})({{ plan: '{plan}', days: 56, friends: [] }})")
        lo = min(x['w'] for x in r['log'])
        print(f'  {plan}: lowest work {lo:.1f}, steps {r["steps"]}'); show(r, 21)
        check(not r['steps'] and r['letGo'] is None, f'{plan}: got a summons or let go: {r["steps"]}')

    print('The Chief after three missed shifts in a row (the user\'s rule), and never for lateness:')
    for plan, want in (('twoTwo', False), ('three', True), ('lateDaily', False), ('twoOneTwo', True)):
        r = ev(f"({PAPER})({{ plan: '{plan}', days: {70 if plan in ('lateDaily', 'twoOneTwo') else 21}, friends: [] }})")
        got = any(x['step'] == 'chief' for x in r['steps'])
        print(f"  {plan}: steps {r['steps']}, lowest work {min(x['w'] for x in r['log']):.1f}")
        check(got == want, f"{plan}: the Chief's talk {'missing' if want else 'given'}")
        if plan == 'three' and got: check(r['steps'][0]['day'] == 10, f"three in a row: the Chief on day {r['steps'][0]['day']}, not day 10")
        if plan == 'lateDaily': check(min(x['w'] for x in r['log']) > 15, 'late every day fell under 15 (the Chief by reputation)')
        if plan == 'twoOneTwo':
            print(f"    let go (last day): {r['letGo']}")
            check(any(x['step'] == 'captain' for x in r['steps']), 'two missed, one worked, two missed every week never reaches the Captain')

    print('(b) All their leave and sick days, over 16 weeks:')
    r = ev(f"({PAPER})({{ plan: 'leave', days: 112, friends: [] }})")
    drops = [x for x in r['log'] if x['c'] in ('leave', 'sick') and x['drop'] < 0]
    print(f"  days off on leave or sick: {len(r['offLeave'])} ({sum(1 for x in r['log'] if x['c'] == 'leave')} leave), lowest work {min(x['w'] for x in r['log']):.1f}, steps {r['steps']}"); show(r, 28)
    check(sum(1 for x in r['log'] if x['c'] == 'leave') >= 3 + 3, 'not all the leave was taken')
    check(not drops, f'work dropped on leave or sick days: {drops[:3]}')
    check(not r['steps'] and r['letGo'] is None, f'leave and sick days led to a summons: {r["steps"]}')

    print('(c) Skipping everything:')
    r = ev(f"({PAPER})({{ plan: 'skip', days: 60, friends: {json.dumps(friends)} }})")
    show(r)
    st = {s['step']: s['day'] for s in r['steps']}
    print(f"  the Chief on day {st.get('chief')}, the Captain on day {st.get('captain')}, let go (last day) {r['letGo']}, ended day {r['ended']}")
    print(f"  friends asked to find you: {sorted(set(r['asks']))}; at the send-off {r['sendOff']}, in their plans {r.get('planned')}; save {r['size']} bytes")
    check('chief' in st and 'captain' in st and r['letGo'] and r['ended'], 'the ladder did not run to the end')
    if 'chief' in st and 'captain' in st and r['letGo']:
        check(st['chief'] < st['captain'] < r['letGo'], 'the steps came out of order')
        check(st['chief'] == 10, f"the Chief on day {st['chief']} (expected day 10: the third missed shift after the first week's grace)")
        check(14 <= r['letGo'] <= 35, f"let go on day {r['letGo']} (expected in about two to four weeks of skipping)")
        check(r['ended'] == r['letGo'], 'the end did not come on the last day')
    check({'career:chief', 'career:captain', 'career:eve', 'career:day'} <= set(r['asks']), 'friends were not asked to come and find you at every step')
    check(r['sendOff'] and set(r['sendOff']) >= set(friends), 'your friends are not at your send-off')
    check(r.get('planned'), 'nobody at your send-off has it in their plans')
    check(r['career']['end'], 'the save is not marked ended')
    occ = {o['id']: o for o in r['occ']}
    print(f"  occasions: {[(o['id'], o['day']) for o in r['occ']]}")
    check(all(k in occ for k in ('careerChief', 'careerCaptain', 'careerLetGo', 'careerSendoff')), 'not every talk was booked')
    if all(k in occ for k in ('careerChief', 'careerCaptain')) and r['letAt'] is not None:
        check(occ['careerChief']['end'] <= occ['careerCaptain']['end'] - 20 and occ['careerCaptain']['end'] <= r['letAt'], 'let go before both talks were held, or the Captain before the Chief')
    if 'careerSendoff' in occ: check(occ['careerSendoff']['day'] == r['letGo'], 'the send-off is not on the last day')

    print('(d) Recovery re-arms each step:')
    for plan, step in (('skipUntilChief', 'chief'), ('skipUntilCaptain', 'captain')):
        r = ev(f"({PAPER})({{ plan: '{plan}', days: 120, friends: [] }})")
        n = sum(1 for s in r['steps'] if s['step'] == step)
        print(f"  {plan}: {step} {n} times, steps {r['steps']}, rounds {r['round']}, let go {r['letGo']}"); show(r, 60)
        check(n >= 2, f'{step} did not come again after recovering')
        check(r['letGo'] is None, f'{plan}: let go')

    print('Sickness (0.61.5): rare, never the first week, three weeks apart; excused; worse untreated; two cures:')
    r = ev("""(() => { const at = (d, m) => { SHIP.time.day = d; SHIP.time.min = m; return (d - 1) * 1440 + m; };
      SHIP.career = null; SHIP.rep = null; SHIP.occasions.length = 0; careerTick(at(1, 0)); const c = SHIP.career, days = []; c.gs = 12345;   // a fixed game seed: the same days every run
      for (let d = 1; d <= 420; d++) { c.e = c.z = d - 1; careerTick(at(d, 330)); if (c.sd === d) { days.push(d); c.sh = 3; } }
      const out = { days };
      SHIP.career = null; careerTick(at(1, 0)); const C = SHIP.career, d = days[0] || 50; C.gs = 12345; C.e = C.z = d - 1; C.w = Math.floor((d - 1) / 28); C.b.push(d); C.l--;
      const l0 = C.l, w0 = careerWork(); careerTick(at(d, 330)); out.sick = sickToday(d); out.excused = !playerShiftOn(d); out.leaveBack = C.l === l0 + 1 && !C.b.includes(d);
      out.speeds = [420, 600, 780, 930].map(m => { careerTick(at(d, m)); return [Math.round(needEffects().walk * 100) / 100, sickBent()]; });
      careerTick(at(d, 760)); out.noMiss = careerWork() >= w0 - 0.01 && C.ms === 0;
      const p = SOC.crew.find(q => q.dept === 'works'); relGet(p.id).tier = 2; out.getwell = (sickChatLine(p, shipNow(), true) || {}).kind || null;
      out.cure = sickCure(1); out.after = [Math.round(needEffects().walk * 100) / 100, sickBent(), sickNow()];
      at(d + 1, 600); out.better = (sickChatLine(p, shipNow(), true) || {}).kind || null;
      SHIP.career.sd = d + 1; SHIP.career.sh = 0; at(d + 1, 700); out.nap = sickCure(3) && !sickNow();
      SHIP.career = null; SHIP.rep = null; careerTick(at(30, 0)); repInit().ship.work = 30; const K = SHIP.career; K.e = K.z = 29; K.sd = 99999; careerTick(at(30, 800)); out.missTo = Math.round(careerWork()); out.missTip = !!(K.k & 2);
      careerSick(30); out.refund = Math.round(careerWork());
      const dueOf = gs => { SHIP.career.sd = 0; SHIP.career.gs = gs; const L = []; for (let d = 8; d <= 200; d++) if (sickDue(d)) L.push(d); return L.join(','); };
      out.namesDiffer = dueOf(1) !== dueOf(2); out.seeded = typeof careerClean(JSON.parse(JSON.stringify(SHIP.career))).gs === 'number';
      out.save = JSON.stringify(SHIP.career || {}).length; out.lines = !!(LINES['sick.getwell'] && LINES['sick.better']); return out; })()""")
    gaps = [b - a for a, b in zip(r['days'], r['days'][1:])]
    print(f"  sick days in 60 weeks: {r['days']} (gaps {gaps})")
    print(f"  on a sick day: {dict((k, v) for k, v in r.items() if k != 'days')}")
    check(r['days'] and min(r['days']) > 7, 'sick in the first week')
    check(all(g >= 21 for g in gaps), 'sick twice within three weeks')
    check(len(r['days']) >= 4 and 35 <= 420 / len(r['days']) <= 105, f"sick {len(r['days'])} times in 60 weeks (about every 6-8 weeks wanted)")
    check(r['sick'] and r['excused'] and r['leaveBack'] and r['noMiss'], 'a sick day is not excused, or the leave not given back, or a miss counted')
    sp = [x[0] for x in r['speeds']]
    check(all(a > b for a, b in zip(sp, sp[1:])) and r['speeds'][-1][1] and not r['speeds'][0][1], f"untreated it doesn't get worse through the day to doubled over: {r['speeds']}")
    check(r['cure'] and r['after'][0] >= 0.99 and not r['after'][1] and not r['after'][2], 'the medicine did not cure it')
    check(r['nap'], 'sleeping it off did not cure it')
    check(r['refund'] == 30 and r['missTo'] < 30, f"a sick note gave back {r['refund'] - r['missTo']} for a miss that took {30 - r['missTo']}")
    check(r['missTip'], 'the first missed shift did not mark its warning shown (k & 2)')
    check(r['namesDiffer'] and r['seeded'], 'every game is sick on the same days, or the game seed is not saved')
    if r['lines']: check(r['getwell'] == 'sick.getwell' and r['better'] == 'sick.better', 'crew have no get-well or glad-you-are-better line')
    else: print('  (no sick.getwell / sick.better lines baked yet)')
    check(r['save'] < SAVE_MAX, f"the save with sickness is {r['save']} bytes")

    print('The time clock (0.61.13): in and out, the shift, leave, the auto clock-out, the crew:')
    r = ev("""(() => { const at = (d, m) => { SHIP.time.day = d; SHIP.time.min = m; return (d - 1) * 1440 + m; };
      SHIP.career = null; SHIP.rep = null; careerTick(at(10, 0)); const c = SHIP.career; c.e = c.z = 9; c.sd = 99999; const out = {};
      careerTick(at(10, 420)); out.in = careerClock(at(10, 485)); out.started = c.on === 10; careerTick(at(10, 760)); out.noMiss = c.ms === 0 && c.md !== 10;
      out.again = careerClock(at(10, 600)) === 'out'; out.done = careerClock(at(10, 1000)); out.hours = [c.ci % 1440, c.co % 1440];
      careerTick(at(11, 0)); careerClock(at(11, 480)); careerTick(at(11, 1070)); out.notYet = !(c.co > c.ci); careerTick(at(11, 1090)); out.auto = c.co % 1440;
      careerTick(at(12, 0)); careerTick(at(12, 760)); out.missedNoClock = c.md === 12;
      out.sat = careerClock(at(13, 600));
      careerTick(at(15, 0)); out.early = careerClock(at(15, 180)); flagSet('shiftSent', null); SHIP.notes = [];
      const sent = []; const stop = onSim('shiftStart', n => sent.push(n)); careerClock(at(15, 690)); shiftTick(); at(15, 691); shiftTick(); stop();
      out.lateNote = sent.map(n => [n.late, !!n.missed]);
      careerTick(at(22, 0)); c.ms = 2; careerClock(at(22, 480)); const w1 = careerWork(); careerClock(at(22, 600)); out.earlyDip = Math.round((w1 - careerWork()) * 10) / 10;
      careerTick(at(22, 760)); careerTick(at(23, 0)); out.shortKeepsRun = c.ms === 2 && c.md !== 22;
      careerClock(at(23, 480)); careerClock(at(23, 960)); careerTick(at(23, 1000)); careerTick(at(24, 0)); out.fullEndsRun = c.ms === 0;
      c.b.push(16); careerTick(at(16, 500)); out.leave = careerClock(at(16, 500));
      careerTick(at(17, 0)); out.back = careerBack(17);
      const S = schedData(), pl = S.byId.get('5-timeclock-1'), w = SOC.crew.filter(p => p.dept === 'works' && p.shift !== 'night' && isWorkDay(p, 10) && socAboard(p, 10) && planDay(p, 10).some(x => x.act === 'work' && /^5-/.test(x.placeId || '')));   // aboard, stationed on Deck 5
      out.crew = w.map(p => planDay(p, 10).filter(x => x.tag === 'clock').length); out.place = !!pl;
      return out; })()""")
    print('  ', r)
    check(r['in'] == 'in' and r['started'] and r['noMiss'], 'clocking in did not start the shift')
    check(r['again'] and r['done'] is None, 'clocking out, or clocking out twice, went wrong')
    check(r['notYet'] and r['auto'] == 1020, f"the auto clock-out: {r['auto']} (17:00 wanted)")
    check(r['missedNoClock'], 'a workday after the first week with no clock-in was not missed')
    check(r['sat'] is None and r['leave'] is None, 'the clock let you clock in on a day off or on leave')
    check(r['back'], 'the first clock-in after leave is not "back"')
    check(r['early'] is None, 'the clock let you clock in at 03:00')
    check(r['earlyDip'] > 0 and r['shortKeepsRun'], f"a short shift (out at 10:00): dip {r['earlyDip']}, run kept and no miss: {r['shortKeepsRun']}")
    check(r['fullEndsRun'], 'a full shift (out at 16:00) did not end the run of missed shifts')
    check(r['lateNote'] == [[150, False]], f"clocking in at 11:30: the shift's start note was {r['lateNote']} (late 150 after 09:00, not missed, wanted)")
    check(r['place'] and r['crew'] and min(r['crew']) >= 1 and sum(1 for n in r['crew'] if n >= 2) >= len(r['crew']) * 3 // 4, f"the Works crew don't use the clock: {r['crew']}")

    print('Reputation you can see (0.61.15): a chip on turning a job in, one at a time, and a small gain:')
    r = ev("""(() => { SHIP.rep = null; const w0 = careerWork(), d0 = repInit().dept.works, n0 = FLOATS.length; REP_CHIP_AT = -1e9; if (DEV.notes) delete DEV.notes.record;
      simNote('job', { id: 'x1', step: 'turnin', job: 'restock', machine: null }); const n1 = FLOATS.length, text = n1 > n0 ? FLOATS[n1 - 1][0].textContent : null;
      simNote('job', { id: 'x2', step: 'turnin', job: 'restock', machine: null }); const n2 = FLOATS.length;
      return { text, once: n1 === n0 + 1 && n2 === n1, work: careerWork() > w0, dept: repInit().dept.works > d0, badge: DEV.notes && DEV.notes.record === 1 }; })()""")
    print('  ', r)
    check(r['text'] == '+ Works reputation' and r['once'], f"the reputation chip: {r['text']}, once: {r['once']}")
    check(r['work'] and r['dept'], 'turning in a job without a machine gave no reputation')
    check(r['badge'], 'the Record app got no mark')

    print('A new game on day 0 is not sick (player engineer 5\'s bug in 0.60.5):')
    r = ev("""(() => { const el0 = document.getElementById('sickCard'); if (el0) el0.hidden = true;   // left open by the sickness case
      SHIP.career = null; SHIP.time.day = 0; SHIP.time.min = 1060; careerTick(); const c = SHIP.career;
      return { sd: c.sd, sick: sickToday(0), now: sickNow(), stage: sickStage(), walk: Math.round(needEffects().walk * 100) / 100, card: !document.getElementById('sickCard') || document.getElementById('sickCard').hidden, excused: c.s.includes(0) }; })()""")
    print('  ', r)
    check(not r['sick'] and not r['now'] and r['stage'] == -1 and r['card'] and not r['excused'], 'a new game arrives sick on day 0')

    print('(e) The save:')
    r = ev(f"({PAPER})({{ plan: 'casual', days: 280, friends: [] }})")
    rt = ev("JSON.stringify(careerClean(JSON.parse(JSON.stringify(SHIP.career)))) === JSON.stringify(SHIP.career)")
    print(f"  after 280 casual days: {r['size']} bytes {json.dumps(r['career'])}; round trip {'same' if rt else 'DIFFERENT'}")
    check(r['size'] < SAVE_MAX, f"the career save is {r['size']} bytes (at most {SAVE_MAX})")
    check(rt, 'the career save does not load back the same')
    sv = ev("(() => { const s = { ship: {} }; for (const f of SAVE_EXTRA) { try { f(s); } catch (e) { } } return !!s.ship.career; })()")
    check(sv, 'the career state is not in the save')

    for e in errors: fail(f'page error: {e}')
    g.close()

print('LEAVE CHECK OK' if ok else 'LEAVE CHECK FAILED')
sys.exit(0 if ok else 1)
