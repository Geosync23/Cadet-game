# Starship Cadet: leave check (keep in the repo, next to cadet_test.py and the other checks)
# Checks leave, missed shifts and being let go (the career engineer, 0.61.x; design-doc "Leave, missed shifts and
# being let go"), on paper: each scenario steps ship days, calling the game's own functions at the hours they'd run
# (careerTick, the shift's start note, repairs as section 20 scores them, Sunday's repWeek), with no walking.
#   leave: 3 days to start, one more every 4 ship weeks, at most 5; booking by 07:30 that day, cancelling gives it back;
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
    if (plan.startsWith('skipUntil')) return 'dyn';     // (d): driven by the ladder below
    return 'work';
  };
  let mode = 'skip', round = 0;                          // (d): skip to the step, work until it re-arms, skip again
  const want = plan === 'skipUntilChief' ? 1 : 2;
  for (let d = 1; d <= days && !ended; d++) {
    let c = code(d);
    if (c === 'dyn') { const st = (SHIP.career || {}).st || 0;
      if (mode === 'skip' && st >= want) { mode = 'work'; round++; }
      else if (mode === 'work' && st < want) { mode = round >= 2 ? 'work' : 'skip'; }
      c = mode; }
    careerTick(at(d, 0));
    if (weekday(d) === 6) { repWeek(Math.floor(at(d, 240) / 60)); careerTick(at(d, 240)); }
    if (c === 'leave') { const ok = careerRota(d) && SHIP.career.l > 0 ? careerBook(d, at(d - 1, 1200)) : false; if (!ok) c = 'work'; }
    if (c === 'sick') careerSick(d);
    const work0 = careerWork();
    careerTick(at(d, 420));
    if (playerShiftOn(d)) {
      if (c === 'work' || c === 'late') { const late = c === 'late' ? 40 : 0; at(d, 480 + late); simNote('shiftStart', { late }); careerTick(at(d, 480 + late));
        for (let k = 0; k < (c === 'late' ? 2 : 3); k++) { at(d, 600 + 90 * k); repAdd('works', 3, { work: 2 }, 'jobs'); } }
      else { at(d, 600); simNote('shiftStart', { late: 120, missed: true }); }
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
      out.late = careerCanBook(4, at(4, 451)); out.early = careerCanBook(4, at(4, 449));
      out.cancel = careerBook(3, at(3, 400)); out.back = c.l; out.onAgain = playerShiftOn(3);
      careerBook(5, at(4, 1200)); out.tooLateCancel = careerBook(5, at(5, 460));
      out.heldEnd = (() => { const j = { found: at(5, 300), urgency: 0, kind: 'wear', tier: 1 }; try { return leaveEnd(j) === j.found; } catch (e) { return 'n/a'; } })();
      for (const d of [29, 57, 85, 113]) { c.e = c.z = d - 1; careerTick(at(d, 10)); } out.grants = c.l;   // no misses in between: just the grants
      return out; })()""")
    print('  ', r)
    check(r['start'] == 3, f"leave to start {r['start']}, not 3")
    check(r['book'] and r['after'] == 2 and r['offOn3'], 'booking a workday: one fewer held and no shift that day')
    check(r['weekend'] is None, 'a Saturday can be booked as leave')
    check(r['late'] is None and r['early'] == 'book', 'booking closes at 07:30 on the day')
    check(r['cancel'] and r['back'] == 2 + 1 and r['onAgain'], 'cancelling gives the day back and the shift returns')
    check(not r['tooLateCancel'], 'a leave day can be cancelled after 07:30 that day')
    check(r['heldEnd'] in (True, 'n/a'), 'a job found on a leave day is still held for you')
    check(r['grants'] == 5, f"leave after four 4-week grants: {r['grants']} (at most 5)")

    print('(a) A diligent player, and a casual one, over 8 weeks:')
    for plan in ('diligent', 'casual'):
        r = ev(f"({PAPER})({{ plan: '{plan}', days: 56, friends: [] }})")
        lo = min(x['w'] for x in r['log'])
        print(f'  {plan}: lowest work {lo:.1f}, steps {r["steps"]}'); show(r, 21)
        check(not r['steps'] and r['letGo'] is None, f'{plan}: got a summons or let go: {r["steps"]}')

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
        check(8 <= st['chief'] <= 14, f"the Chief on day {st['chief']} (expected in the second week: the first is a grace)")
        check(14 <= r['letGo'] <= 35, f"let go on day {r['letGo']} (expected in about two to four weeks of skipping)")
        check(r['ended'] == r['letGo'], 'the end did not come on the last day')
    check({'career:chief', 'career:captain', 'career:eve', 'career:day'} <= set(r['asks']), 'friends were not asked to come and find you at every step')
    check(r['sendOff'] and set(r['sendOff']) >= set(friends), 'your friends are not at your send-off')
    check(r.get('planned'), 'nobody at your send-off has it in their plans')
    check(r['career']['end'], 'the save is not marked ended')

    print('(d) Recovery re-arms each step:')
    for plan, step in (('skipUntilChief', 'chief'), ('skipUntilCaptain', 'captain')):
        r = ev(f"({PAPER})({{ plan: '{plan}', days: 120, friends: [] }})")
        n = sum(1 for s in r['steps'] if s['step'] == step)
        print(f"  {plan}: {step} {n} times, steps {r['steps']}, rounds {r['round']}, let go {r['letGo']}"); show(r, 60)
        check(n >= 2, f'{step} did not come again after recovering')
        check(r['letGo'] is None, f'{plan}: let go')

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
