# Starship Cadet: mechanics check (keep in the repo, next to career_check.py)
# Pillar 5's mechanics, one part per mechanic (plans/pillar5-plan.md "Test changes"; the frame is the Works career
# engineer's, 0.44.0; each mechanic engineer adds their part below). For every ladder row whose sub-block is in the
# build (WORK_MECH[id]), the frame itself checks, on paper:
#   - the training: opened on a workday, the ask (an appointment), the meeting, the teacher's job then yours, trained
#     (big rows); a small row trains on its first use
#   - its stages: stage 0 once trained, later stages only as their conditions come (uses, another mechanic trained)
#   - the same twice
# and then runs the mechanic's own part, PARTS[id](g), if there is one: its steps end to end, its stages, the crew
# doing it when you don't, the same twice. A part prints what it saw and calls fail() for anything wrong.
# Rows with no sub-block are listed as "not in this build" (not failures).
# Setup and environment as for cadet_test.py.
# Run:  python3 mech_check.py BUILD.html [ID ...]     (IDs: only those rows, e.g. m1 m4)
import sys, json
exec(open(__file__.replace('mech_check.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright

ok = True
def fail(msg):
    global ok
    ok = False
    print('FAIL', msg)
def check(cond, msg):
    if not cond: fail(msg)
    return cond

# the frame's training run for one row, on paper: the row's needs are met by hand, its day comes, you're always there
TRAIN = r"""((id) => {
  const row = ladderRow(id), t0 = (Math.max(row.day, 2) - 1) * 1440;
  SHIP.works = null; SHIP.occasions.length = 0; SHIP.notes = []; SHIP.flags = {}; SHIP.jobs = []; SHIP.mail = [];
  MACH_HOUR = null; MACH_SEEN = -1; WORKS_TICK.m = WORKS_TICK.h = -1;
  let d = Math.max(row.day, 2); while (!playerShiftOn(d) || (row.fixed && weekday(d) + 1 !== row.fixed.wd)) d++;
  setShipNow((d - 1) * 1440 + 300); machinesNow(); const W = worksInit();
  W.log.push(['earlier', 1, 0, 'service']);                 // a job of yours already turned in (Day 1's shadow shift, for m1)
  for (const r of CAREER_LADDER.slice(0, CAREER_LADDER.indexOf(row))) { W.tr[r.id] = 1; W.use[r.id] = 9; (W.op[1] = W.op[1] || []).push(r.id); }   // everything before it, done
  if (row.needs) for (const n of [].concat(row.needs)) { if (n.flag) flagSet(n.flag, 1); if (n.rep) W.xp = 999; }
  const seen = [], doJob = jid => { if (!claimJob(jid)) return false; const j = SHIP.jobs.find(x => x.id === jid); jobStops(j).forEach((s, k) => jobStepDone(jid, k)); return turnInJob(jid); };
  let teacher = null, yours = null;
  for (let m = 360; m < 1020; m += 10) {
    const t = (d - 1) * 1440 + m; setShipNow(t); machinesNow(); worksCareerTick(t);
    const c = SHIP.works.cur;
    if (c) seen.push(c.st);
    if (c && c.st === 'meet') { const r = SHIP.occasions.find(x => x.key === c.occ); if (r && t >= r.at) { r.met = true; worksCareerTick(t + 1); } }
    if (c && c.st === 'watch') { c.w = TRAIN_WATCH; worksCareerTick(t + 2); const dj = SHIP.jobs.filter(x => x.train === id && x.status === 'done').pop(); teacher = dj ? dj.doneBy : null; }
    if (c && c.st === 'do' && !myJob() && doJob(c.j)) yours = (SHIP.jobs.find(x => x.id === c.j) || {}).doneBy;
    if (row.size === 'small' && worksOpened().has(id) && W.tr[id] === undefined) worksUse(id);
    if (W.tr[id] !== undefined) break;
  }
  const st0 = worksStage(id);
  return { day: d, opened: worksOpened().has(id), trained: W.tr[id], teacher, yours, states: [...new Set(seen)], stage: st0, works: JSON.stringify(W) };
})"""

# the mechanics' own parts: PARTS['m1'] = lambda g: ... (each mechanic engineer adds theirs; see the header)
PARTS = {}

# ---- M5 tuning (24e, seat M2): a drifted machine settles only at 0, each press moves the real setting (so the look
# follows), the words on the card, yours counts a use, the crew settle what you leave, the row's opening drifts both
# ovens; the same twice. (Drift itself, its rate and save are section 17's: machine_check.)
M5 = r"""(() => {
  const out = {}, id = '3-oven-2', reset = d => { machinesNew(); SHIP.jobs = []; MACH_HOUR = null; MACH_SEEN = -1; setShipNow((d - 1) * 1440 + 600); machinesNow(); };
  reset(11); for (const x of ['3-oven-1', '3-oven-2']) tuneSet(x, 0);
  WORK_MECH.m5.open(); out.opened = ['3-oven-1', '3-oven-2'].map(machineDrift);
  tuneSet('3-oven-1', 0); tuneSet(id, 2);
  const j = tuneJob(id, shipNow()); SHIP.jobs.push(j); MACH_REV++;
  out.claimed = claimJob(j.id);
  const sts = jobStops(j), k = sts.findIndex(s => s.how === 'turn'), o = sts[k].opts; out.start = o.v; out.seq = [];
  for (const v of [3, 2, 1, 0, -1, -2, 0]) { const txt = o.onTurn(v); out.seq.push([v, machineDrift(id), o.ok(v), txt]); }
  const uses = SHIP.works.use.m5 || 0;
  out.step = jobStepDone(j.id, k, { value: 0 }); out.turnin = turnInJob(j.id); out.uses = (SHIP.works.use.m5 || 0) - uses; out.after = machineDrift(id);
  tuneSet(id, -2); const j2 = tuneJob(id, shipNow()); SHIP.jobs.push(j2); jobFinish(j2, shipNow(), 'tomas'); out.crew = machineDrift(id);
  out.words = [2, 1, 0, -1, -2].map(v => tuneWord('oven', v)).concat([tuneWord('lights', 2), tuneWord('cartdock', -2)]);
  return out;
})()"""
def part_m5(g):
    a, b = g.ev(M5), g.ev(M5)
    print('  m5:', json.dumps({k: a[k] for k in ('opened', 'start', 'uses', 'after', 'crew')}), a['words'])
    check(a['opened'] == [2, 2], f"m5: the row's opening drifts both ovens two hot ({a['opened']})")
    check(a['claimed'] and a['start'] == 2, 'm5: your tune job starts at the real drift')
    check([s[1] for s in a['seq']] == [s[0] for s in a['seq']], 'm5: each press sets the machine (the look follows)')
    check([s[2] for s in a['seq']] == [s[0] == 0 for s in a['seq']], 'm5: settled only at 0')
    check(a['step']['done'] and a['turnin'] and a['uses'] == 1 and a['after'] == 0, 'm5: settled, turned in, one use')
    check(a['crew'] == 0, 'm5: the crew settle a tune job')
    check(not any(any(ch.isdigit() for ch in w) for w in a['words']), 'm5: words, not numbers')
    check(json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True), 'm5: differs the second time')
PARTS['m5'] = part_m5

# ---- M6 incidents (24f, seat M2): the plan over four weeks (about one a week, never a day off, a weekend, a ship-wide
# event day, at night or before Day 8; mornings on a tradition evening); each incident's steps in order (a wrong valve
# doesn't make it safe), the fix posted, the lift freed; the crew clear one you don't come to; a skipped hour's is
# cleared by the crew; the save's part read back; the same twice
M6 = r"""(() => {
  const out = {}, W = SHIP.works, reset = t => { machinesNew(); SHIP.jobs = []; MACH_HOUR = null; MACH_SEEN = -1; setShipNow(t); machinesNow(); W.inc = { plan: {}, open: null }; };
  reset(14 * 1440 + 300);
  out.plan = [2, 3, 4, 5].map(w => incPlan(w)); W.inc.plan = {}; out.plan2 = [2, 3, 4, 5].map(w => incPlan(w));
  out.planOk = out.plan.map(P => !P.length ? 'none' : [weekday(P[1]) < 5, playerShiftOn(P[1]), !incShipEvent(P[1]), P[2] >= 540 && P[2] <= (incEvening(P[1]) ? 690 : 930), P[1] >= 15, incWeek(P[1])].join());
  out.kinds = {}; W.tr.m6 = W.tr.m6 || 8;
  for (const [kind, deck] of [['burst', 4], ['burst', 3], ['burst', 5], ['lift', 5], ['alarm', 3]]) {
    reset(16 * 1440 + 600); const r = out.kinds[kind + deck] = {};
    for (const id of ['3-galleyplant-1', '5-mainlift-1']) { SHIP.machines[id].cond = 100; SHIP.machines[id].state = 'healthy'; SHIP.jobs = SHIP.jobs.filter(x => x.machine !== id); }   // fault-free first, so the fix is the incident's
    const O = incStart(kind, deck, shipNow(), false), j = SHIP.jobs.find(x => x.id === O.j);
    r.held = j.leave; r.top = j.urgency; r.lift = !!liftStuckNow(); r.claimed = claimJob(j.id);
    const st = jobStops(j); r.steps = st.map(s => s.step + ':' + s.how + '@' + (s.places[0] || '-'));
    if (kind === 'burst') { const line = DECKS[deck].valveLine; r.wrong = jobStepDone(j.id, 0, { pick: line[0] }); r.wrongSafe = W.inc.open.safe; r.vetoed = !(j.stepsDone || []).includes(0); j.stepsDone = (j.stepsDone || []).filter(k => k !== 0); r.right = jobStepDone(j.id, 0, { pick: line[line.length - 1] }).ok; }
    else r.right = jobStepDone(j.id, 0, kind === 'lift' ? { value: 3 } : {}).ok;
    r.safe = W.inc.open.safe; r.liftAfter = !!liftStuckNow();
    for (let k = 1; k < st.length; k++) jobStepDone(j.id, k, {});
    r.turnin = turnInJob(j.id); r.open = W.inc.open;
    const fx = SHIP.jobs.filter(x => x.id === j.fix && x.status !== 'done').map(x => (x.chore || x.kind) + ':' + (x.machine || x.target) + ':' + (x.foundBy || '') + ':' + (x.leave || 0));
    r.fix = fx;
    const F = SHIP.jobs.find(x => x.id === j.fix); if (F) { F.status = 'done'; F.doneBy = 'you'; } const n0 = new Set(simNotes('incident')); for (const f of WORK_TICKS) f(shipNow(), false); r.fixedNote = simNotes('incident').filter(n => !n0.has(n)).filter(n => n.step === 'fixed').map(n => n.step + ':' + n.by).join(); r.fixAfter = !!W.inc.fix;
  }
  reset(16 * 1440 + 600); delete W.tr.m6;               // not trained: the crew's
  const O = incStart('burst', 4, shipNow(), false), cj = SHIP.jobs.find(x => x.id === O.j); out.crewHeld = cj.leave;
  for (let m = 610; m <= 780; m += 10) { setShipNow(16 * 1440 + m); machinesNow(); for (const f of WORK_TICKS) f(shipNow(), false); }
  out.crew = { by: cj.doneBy && cj.doneBy !== 'you' ? 'crew' : cj.doneBy, status: cj.status, open: W.inc.open, fix: SHIP.jobs.filter(x => x.chore === 'joint').length };   // (which crew member depends on the parts run before)
  reset(14 * 1440 + 300); W.tr.m6 = 8; const P = incPlan(3); out.skipPlan = P;
  if (P.length) { const t = (P[1] - 1) * 1440 + Math.ceil(P[2] / 60) * 60; setShipNow(t); machinesNow(); for (const f of WORK_TICKS) f(t, true); out.skip = { done: P[4], open: W.inc.open, jobs: SHIP.jobs.filter(x => x.kind === 'incident').map(x => x.status + ':' + x.doneBy) }; }
  W.inc.open = { kind: 'lift', deck: 5, at: 23000, train: false, safe: false, j: 'x' }; W.inc.plan[9] = ['alarm', 64, 600, 3, 1]; W.inc.plan[1] = ['burst', 8, 630, 4, 1];
  out.save = JSON.stringify(incClean(JSON.parse(JSON.stringify(W.inc)), 60)); out.saveOld = JSON.stringify(incClean(undefined));
  return out;
})()"""
def part_m6(g):
    a, b = g.ev(M6), g.ev(M6)
    print('  m6 plan:', a['plan'], a['planOk'])
    check(a['plan'] == a['plan2'], 'm6: the plan the same when made again')
    check(sum(1 for P in a['plan'] if P) >= 3, 'm6: about one a week over four weeks')
    for P, okk, w in zip(a['plan'], a['planOk'], [2, 3, 4, 5]):
        if P: check(okk == f'true,true,true,true,true,{w}', f'm6: week {w} plan {P}: {okk}')
    for k, r in a['kinds'].items():
        print(f"  m6 {k}: held {r['held']}, steps {r['steps']}, safe {r['safe']}, fix {r['fix']}")
        check(r['fixedNote'] == 'fixed:you' and not r['fixAfter'], f"m6 {k}: the 'fixed' note when the fix is done ({r['fixedNote']})")
        check(r['claimed'] and r['held'] == 30 and r['top'] == 2, f'm6 {k}: on the board, top, held for you 30 minutes')
        check(all('@-' not in s for s in r['steps']), f'm6 {k}: every step has its place')
        check(r['right'] and r['safe'] and r['turnin'] and r['open'] is None and len(r['fix']) == 1, f'm6 {k}: safe, clean, cleared, one fix posted')
        if k.startswith('burst'):
            check(not r['wrongSafe'], f'm6 {k}: a wrong valve doesn\'t make it safe')
            if not r['vetoed']: print(f'  m6 {k}: (the wrong valve\'s stop was marked done: section 17\'s def.veto not in this build)')
        if k == 'lift5': check(r['lift'] is True and r['liftAfter'] is False, 'm6 lift: stuck, then freed at the brake')
    print('  m6 crew:', a['crew'], 'skip:', a.get('skip'))
    check(a['crewHeld'] == 1 and a['crew']['status'] == 'done' and a['crew']['by'] == 'crew' and a['crew']['open'] is None and a['crew']['fix'] == 1, 'm6: the crew clear one you\'re not trained for')
    if a['skipPlan']: check(a['skip']['done'] == 1 and a['skip']['open'] is None and a['skip']['jobs'] and a['skip']['jobs'][0].startswith('done'), 'm6: a skipped hour\'s incident cleared by the crew')
    s = json.loads(a['save'])
    check(s['open'] and s['open']['kind'] == 'lift' and '9' in s['plan'] and '1' not in s['plan'], 'm6: the save read back (old weeks dropped)')
    check(json.loads(a['saveOld']) == {'plan': {}, 'open': None}, 'm6: a save with no incidents reads as none')
    if not check(json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True), 'm6: differs the second time'):
        for k in a:
            if json.dumps(a[k], sort_keys=True) != json.dumps(b[k], sort_keys=True):
                if isinstance(a[k], dict) and isinstance(b[k], dict):
                    for s in a[k]:
                        if json.dumps(a[k].get(s), sort_keys=True) != json.dumps(b[k].get(s), sort_keys=True): print('   ', k, s, json.dumps(a[k].get(s), sort_keys=True)[:400], '|', json.dumps(b[k].get(s), sort_keys=True)[:400])
                else: print('   ', k, json.dumps(a[k], sort_keys=True)[:300], '|', json.dumps(b[k], sort_keys=True)[:300])
PARTS['m6'] = part_m6

only = set(sys.argv[2:])
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1])
    ev = g.ev
    rows = ev("CAREER_LADDER.map(r => ({ id: r.id, name: r.name, size: r.size, inBuild: !!WORK_MECH[r.id], stages: (r.stages || []).length }))")
    for r in rows:
        if only and r['id'] not in only: continue
        if not r['inBuild']:
            print(f"{r['id']} ({r['name']}): not in this build")
            continue
        a = ev(f"({TRAIN})('{r['id']}')")
        b = ev(f"({TRAIN})('{r['id']}')")
        print(f"{r['id']} ({r['name']}, {r['size']}): opened Day {a['day']}, trained Day {a['trained']}, steps {a['states']}, teacher's job by {a['teacher']}, yours by {a['yours']}, stage {a['stage']}")
        check(a['opened'] and a['trained'] is not None, f"{r['id']}: never trained")
        if r['size'] == 'big' and not ev(f"!!WORK_MECH['{r['id']}'].noJob"):
            check(a['states'][:3] == ['meet', 'watch', 'do'] or 'meet' in a['states'], f"{r['id']}: the training's steps {a['states']}")
            check(a['teacher'] not in (None, 'you') and a['yours'] == 'you', f"{r['id']}: the teacher's job, then yours")
        check(a['stage'] == 0, f"{r['id']}: stage {a['stage']} once trained (0 expected)")
        check(json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True), f"{r['id']}: the training differs the second time")
        if r['id'] in PARTS:
            PARTS[r['id']](g)
    ev("SHIP.works = null")
    if g.errors: fail('page errors: ' + ' | '.join(g.errors[:5]))
    g.close()

print('MECH CHECK OK' if ok else 'MECH CHECK FAILED')
sys.exit(0 if ok else 1)
