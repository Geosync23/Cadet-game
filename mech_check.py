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
  if ((row.tier || 1) > W.tier) { W.tier = row.tier; W.rank = row.rank || W.rank; }   // a Tier 2 row (m8, m9): you're an Officer by then (M3, 0.53.0)
  for (const r of CAREER_LADDER.slice(0, CAREER_LADDER.indexOf(row))) { W.tr[r.id] = 1; W.use[r.id] = 9; (W.op[1] = W.op[1] || []).push(r.id); }   // everything before it, done
  if (row.needs) for (const n of [].concat(row.needs)) { if (n.flag) flagSet(n.flag, 1); if (n.rep) W.xp = 999; }
  const seen = [], doJob = jid => { if (!claimJob(jid)) return false; const j = SHIP.jobs.find(x => x.id === jid);
    const cs = SHIP.works && SHIP.works.cases && (SHIP.works.cases.open || []).find(c => c.job === jid);   // a head-scratcher (24k): call it right first
    if (cs && typeof caseCall === 'function') caseCall(cs.id, cs.cause);
    jobStops(j).forEach((s, k) => jobStepDone(jid, k)); return turnInJob(jid); };
  let teacher = null, yours = null;
  for (let m = 360; m < 1020; m += 10) {
    const t = (d - 1) * 1440 + m; setShipNow(t); machinesNow(); worksCareerTick(t);
    if (typeof DIALOGUE !== 'undefined' && DIALOGUE && typeof dialogueEnd === 'function') dialogueEnd(true);   // read through
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

# 24a rounds (seat M1): Day 3's morning round on paper. Trained on Day 2; at 07:00 a round is posted, held for you;
# half its machines are worn by hand. You take it, look at each stop and mark it (right on the worn ones, "worn" on one
# healthy one too): the worn ones' jobs are found by you (xp, foundBy), the healthy one gets nothing. Then a day you
# don't take it: at 11:00 it's the crew's and they finish it (the worn ones found by them). Stage 2 after 5 rounds.
# The route and signs the same twice.
M1_RUN = r"""(() => {
  SHIP.works = null; SHIP.occasions.length = 0; SHIP.notes = []; SHIP.flags = {}; SHIP.jobs = []; SHIP.mail = [];
  MACH_HOUR = null; MACH_SEEN = -1; WORKS_TICK.m = WORKS_TICK.h = -1;
  const run = (from, to) => { for (let m = from; m <= to; m += 10) { setShipNow(m); machinesNow(); worksCareerTick(m); } };
  setShipNow(1440 + 300); machinesNow(); const W = worksInit(); W.tr.m1 = 2; W.use.m1 = 1; W.op[2] = ['m1']; W.op[1] = ['m1'];
  const d = 3, t0 = (d - 1) * 1440;
  run(t0 + 300, t0 + 430);
  const j = SHIP.jobs.find(x => x.kind === 'rounds' && x.status === 'open'), out = { posted: !!j };
  if (!j) return out;
  out.route = j.route.slice(); out.held = j.found <= shipNow() && shipNow() < leaveEnd(j); out.leaveEnd = leaveEnd(j) - t0;
  out.signs = j.route.map(id => roundSign(id, d));
  const worn = j.route.filter((id, i) => i % 2 === 0), healthy = j.route.filter((id, i) => i % 2 === 1);
  for (const id of j.route) { const s = SHIP.machines[id]; s.cond = worn.includes(id) ? 60 : 95; s.state = machineState(s.cond); }
  SHIP.jobs = SHIP.jobs.filter(x => !(x.machine && j.route.includes(x.machine)));   // no jobs on them yet
  out.claimed = claimJob(j.id); const xp0 = W.xp;
  out.stops = jobStops(j).map(s => [s.how, s.places[0] || null, (s.opts && s.opts.marks || []).length]);
  const mark = (x, k) => jobStepDone(x.id, k, { pick: worn.includes(x.route[k]) ? 'worn' : k === 1 ? 'worn' : 'fine' });
  mark(j, 0); mark(j, 1);
  // a save and reload mid-round: the jobs as saved (JSON), section 17's tidy, then on with the rest
  SHIP.jobs = JSON.parse(JSON.stringify(SHIP.jobs)); if (typeof jobsTidy === 'function') jobsTidy();
  const jr = SHIP.jobs.find(x => x.id === j.id); out.reload = jr ? [jr.claimedBy, (jr.stepsDone || []).length, Object.keys(jr.marks || {}).length, jobStops(jr).length] : null;
  if (!jr) return out;
  for (let k = 2; k < jr.route.length; k++) mark(jr, k);
  out.workDone = !!jr.workDone; out.turnin = turnInJob(jr.id);
  out.found = worn.map(id => { const x = SHIP.jobs.find(y => y.machine === id && y.status !== 'done'); return x ? [x.kind, x.foundBy || null, x.found <= shipNow()] : null; });
  out.healthyJobs = healthy.filter(id => SHIP.jobs.some(y => y.machine === id && y.status !== 'done')).length;
  out.xp = W.xp - xp0; out.use = W.use.m1; out.marks = jr.marks;
  // Day 4: nobody takes it; at 11:00 it's the crew's, and they finish it by evening
  const d2 = 4, t2 = (d2 - 1) * 1440;
  run(t0 + 440, t2 + 430);
  const j2 = SHIP.jobs.find(x => x.kind === 'rounds' && Math.floor(x.posted / 1440) + 1 === d2);
  out.posted2 = !!j2;
  if (j2) { for (const id of j2.route) { const s = SHIP.machines[id]; s.cond = 60; s.state = 'worn'; } SHIP.jobs = SHIP.jobs.filter(x => !(x.machine && j2.route.includes(x.machine)));
    run(t2 + 440, t2 + 1080); out.crew = [j2.status, j2.claimedBy || j2.doneBy, j2.doneBy !== 'you' && j2.status === 'done'];
    out.crewFound = j2.route.filter(id => SHIP.jobs.some(y => y.machine === id && y.found <= shipNow())).length + '/' + j2.route.length; }
  W.use.m1 = 5; out.stage5 = worksStage('m1'); W.use.m1 = 4; out.stage4 = worksStage('m1');
  out.off = [6, 7].map(dd => { SHIP.jobs = []; MACH_HOUR = null; run((dd - 1) * 1440 + 400, (dd - 1) * 1440 + 430); return SHIP.jobs.some(x => x.kind === 'rounds' && Math.floor(x.posted / 1440) + 1 === dd); });
  return out;
})()"""
M1_ASK = r"""(() => { SHIP.works = null; SHIP.occasions.length = 0; SHIP.jobs = []; WORKS_TICK.m = WORKS_TICK.h = -1; setShipNow(1440 + 300); machinesNow();
  const W = worksInit(); W.log.push(['x', 1, 0, 'service']); for (let m = 1440 + 360; m <= 1440 + 700; m += 10) { setShipNow(m); machinesNow(); worksCareerTick(m); }
  const r = SHIP.occasions.find(x => x.id === 'works.m1'); return r ? r.at % 1440 : null; })()"""
def m1_part(g):
    at = g.ev(M1_ASK)
    print('  24a: Day 2\'s meeting with Torres at', at)
    check(at is not None and at >= 635, f"m1: Day 2's meeting at {at} (after the 10:30 tea, 10:35 or later)")
    a = g.ev(M1_RUN)
    b = g.ev(M1_RUN)
    print('  24a rounds:', json.dumps({k: a.get(k) for k in ('posted', 'route', 'leaveEnd', 'stops', 'found', 'healthyJobs', 'xp', 'use', 'crew', 'crewFound', 'stage4', 'stage5', 'off')}))
    print('  signs:', a.get('signs'))
    if not check(a['posted'], 'm1: no morning round posted on Day 3'): return
    check(4 <= len(a['route']) <= 6, f"m1: route of {len(a['route'])} (4-6 expected)")
    check(a['held'] and a['leaveEnd'] == 660, f"m1: held for you to 11:00 (ends {a['leaveEnd']})")
    check(a['claimed'] and all(s[0] == 'look' and s[1] and s[2] == 3 for s in a['stops']), f"m1: stops {a['stops']}")
    check(a.get('reload') and a['reload'][0] == 'you' and a['reload'][1] == 2 and a['reload'][2] == 2 and a['reload'][3] == len(a['route']), f"m1: reloaded mid-round {a.get('reload')}")
    check(a['workDone'] and a['turnin'], 'm1: the round not done and turned in')
    check(all(f and f[1] == 'you' and f[2] for f in a['found']), f"m1: worn machines found by you: {a['found']}")
    check(a['healthyJobs'] == 0, f"m1: {a['healthyJobs']} jobs posted for healthy machines")
    check(a['xp'] >= len(a['found']), f"m1: reputation +{a['xp']} for {len(a['found'])} found")
    check(a['use'] == 2, f"m1: uses {a['use']} (2 expected)")
    check(a['posted2'] and a.get('crew') and a['crew'][2], f"m1: an untaken round done by the crew: {a.get('crew')}")
    check(a.get('crewFound', '0/1').split('/')[0] == a.get('crewFound', '0/1').split('/')[1], f"m1: the crew's round found {a.get('crewFound')}")
    check(a['stage4'] == 0 and a['stage5'] == 1, f"m1: stage {a['stage4']} after 4 rounds, {a['stage5']} after 5")
    check(not any(a['off']), f"m1: a round posted on a day off {a['off']}")
    check(json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True), 'm1: the round differs the second time')
PARTS['m1'] = m1_part

# 24c the drill (seat M1): Wednesdays 14:50-15:15, the week's kind (fire Day 3, pressure Day 10, power Day 17): the job
# is yours at 14:50, its stops at the deck architect's places (skipped if they aren't in the build), done by you, over
# at 15:15 (the all-clear) with the note and the row's use; the same twice
M3D_RUN = r"""((kindDay) => {
  SHIP.works = null; SHIP.occasions.length = 0; SHIP.notes = []; SHIP.flags = {}; SHIP.jobs = []; SHIP.mail = [];
  MACH_HOUR = null; MACH_SEEN = -1; WORKS_TICK.m = WORKS_TICK.h = -1;
  const run = (from, to, f) => { for (let m = from; m <= to; m++) { setShipNow(m); machinesNow(); worksCareerTick(m); if (f) f(m); } };
  setShipNow(1440 + 300); machinesNow(); const W = worksInit(); W.tr.m1 = 2; W.use.m1 = 1; W.use.m4 = 1; W.op[1] = ['m1'];
  const d = kindDay, t0 = (d - 1) * 1440, out = { kind: drillKind(d) };
  run(t0 + 360, t0 + 880);
  out.opened = worksOpened(W).has('m3d'); const j = drillJobOf(d); out.posted = !!j;
  if (!j) return out;
  out.stops = jobStops(j).map(s => [s.step, s.how || 'hold', s.places[0] || null]);
  run(t0 + 881, t0 + 892); out.mine = j.claimedBy;
  run(t0 + 893, t0 + 902, m => { if (m === t0 + 902) jobStops(j).forEach((s, k) => jobStepDone(j.id, k, s.how === 'turn' ? { value: 4 } : {})); });
  out.reached = j.reached; out.workDone = !!j.workDone;
  run(t0 + 903, t0 + 920);
  out.status = [j.status, j.doneBy]; out.note = simNotes('drill', t0).map(n => [n.kind, n.mins, n.you]); out.tr = W.tr.m3d; out.use = W.use.m3d; out.xp = W.xp;
  return out;
})"""
def m3d_part(g):
    want = {3: 'fire', 10: 'pressure', 17: 'power'}
    places = g.ev("!!(DECKS[5].drill && placeById(DECKS[5].drill.ext))")
    for d, kind in want.items():
        a = g.ev(f"({M3D_RUN})({d})"); b = g.ev(f"({M3D_RUN})({d})")
        print(f'  24c drill Day {d}:', json.dumps(a))
        check(a['kind'] == kind and a['posted'] and a['mine'] == 'you', f"m3d Day {d}: {a['kind']} posted {a['posted']} yours {a.get('mine')}")
        if places: check(a['workDone'] and a['status'] == ['done', 'you'] and a['use'] == 1, f"m3d Day {d}: done {a.get('status')} use {a.get('use')}")
        else: print('  (the drill places are not in this build: stops skipped)')
        check(a.get('status', [None])[0] == 'done', f"m3d Day {d}: not over at 15:15")
        check(json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True), f'm3d Day {d}: differs the second time')
def m3d_jump(g):
    # a drill you never came to, then a jump to a later day (a test skip, a long sleep): closed on the next tick, quietly
    r = g.ev(f"""(() => {{ ({M3D_RUN.replace('run(t0 + 893', 'false && run(t0 + 893').replace('run(t0 + 903, t0 + 920);', '')})(3); const j = drillJobOf(3); const before = j && j.status;
      setShipNow(10 * 1440 + 780); for (const f of WORK_TICKS) try {{ f(shipNow(), false); }} catch (e) {{}}
      return [before, j && j.status, SHIP.jobs.filter(x => x.kind === 'drill' && x.status !== 'done').length]; }})()""")
    print('  24c drill, missed then a jump to Day 11:', r)
    check(r[0] == 'claimed' and r[1] == 'done' and r[2] == 0, f"m3d: a missed drill is closed after a jump {r}")
def m3d_both(g):
    m3d_part(g); m3d_jump(g)
PARTS['m3d'] = m3d_both

# 24c the inspection (seat M1): Thursday 06:30. Each set of items gives its remark (nod, one, two, none); in the bunk
# room it's said, away it's Mail at 07:00; turning up (or a nod while out) is the row's use; none on a day off
M3I_RUN = r"""((items, here) => {
  SHIP.works = null; SHIP.notes = []; SHIP.mail = []; WORKS_TICK.m = WORKS_TICK.h = -1;
  setShipNow(3 * 1440 + 300); const W = worksInit(); W.op[1] = ['m1']; W.op[4] = ['m3i'];
  SHIP.clothes.changed = items.uniform ? 4 : 3; SHIP.player.bedMade = items.bed ? 4 : null;
  const res = inspectRun(4, here), mail = SHIP.mail.filter(m => m.at === 3 * 1440 + INSPECT_MAIL).length;
  return { res, mail, use: W.use.m3i || 0, off: inspectDue(6) || inspectDue(7) };
})"""
def m3i_part(g):
    cases = [({'uniform': 1, 'bed': 1}, True, 'nod', 1), ({'uniform': 0, 'bed': 1}, True, 'uniform', 1), ({'uniform': 1, 'bed': 0}, False, 'bed', 0),
             ({'uniform': 0, 'bed': 0}, False, 'two', 0), ({'uniform': 1, 'bed': 1}, False, 'nod', 1)]
    for items, here, want, use in cases:
        a = g.ev(f"({M3I_RUN})({json.dumps(items)}, {'true' if here else 'false'})")
        print('  24c inspection', items, 'here' if here else 'away', json.dumps(a))
        check(a['res'] == want and a['use'] == use and a['mail'] == (0 if here else 1) and not a['off'], f"m3i {items} {here}: {a}")
PARTS['m3i'] = m3i_part

# 24d hauling (seat M1): Day 10 (a Wednesday), trained. The delivery's manifest lands at 10:00; the unload done by hand;
# the run is posted after it, held for you to 16:00; you do every stop: each crate taken once and delivered once, the
# manifest empty, the cart never over 4, a use of m4. Then a planted manifest of 5: two runs (4, then 1). Then Day 17 with
# nobody taking it: the crew do it by evening. The same twice.
M4_RUN = r"""(() => {
  SHIP.works = null; SHIP.notes = []; SHIP.flags = {}; SHIP.jobs = []; SHIP.mail = []; SHIP.manifest = [];
  MACH_HOUR = null; MACH_SEEN = -1; WORKS_TICK.m = WORKS_TICK.h = -1;
  const run = (from, to, f) => { for (let m = from; m <= to; m += 10) { setShipNow(m); machinesNow(); worksCareerTick(m); if (f) f(m); } };
  setShipNow(8 * 1440 + 300); machinesNow(); const W = worksInit(); for (const r of CAREER_LADDER) if (r.id !== 'm4') { W.tr[r.id] = 1; W.use[r.id] = 9; (W.op[1] = W.op[1] || []).push(r.id); }
  W.tr.m4 = 3; W.use.m4 = 1; (W.op[3] = []).push('m4');
  const d = 10, t0 = (d - 1) * 1440, out = {};
  run(t0 + 360, t0 + 610);
  out.manifest = (SHIP.manifest || []).map(c => [c.id, c.dest, c.n]); out.crates = manifestCrates();
  for (const j of SHIP.jobs) if (j.kind === 'restock' && j.cargo === 'stores' && j.status !== 'done') jobFinish(j, shipNow(), 'crew');
  run(t0 + 620, t0 + 680);
  const j = SHIP.jobs.find(x => x.kind === 'haul' && x.status !== 'done'); out.posted = !!j;
  if (!j) return out;
  out.held = shipNow() < leaveEnd(j) && leaveEnd(j) - t0 >= 900; out.junior = !!j.junior;
  out.claimed = claimJob(j.id);
  out.stops = jobStops(j).map(s => [s.step, s.places[0] || null]);
  out.holds = []; jobStops(j).forEach((s, k) => { out.holds.push(JOB_KINDS.haul.hold(j)); jobStepDone(j.id, k, {}); });
  out.workDone = !!j.workDone; out.turnin = turnInJob(j.id); out.left = manifestCrates(); out.got = j.got.slice(); out.use = W.use.m4;
  out.notes = simNotes('haul', t0).map(n => n.id);
  // five crates: two runs
  SHIP.manifest = ['linen', 'medical', 'store', 'galley', 'bridge'].map(id => ({ id, dest: (DELIVERIES.find(r => r.key === id) || {}).to, n: 1 })).filter(c => placeById(c.dest));
  out.five = manifestCrates(); const runs = [];
  run(t0 + 690, t0 + 1000, m => { const x = SHIP.jobs.find(y => y.kind === 'haul' && y.status === 'open' && !y.claimedBy); if (x && claimJob(x.id)) { runs.push(x.crates.length); jobStops(x).forEach((s, k) => jobStepDone(x.id, k, {})); turnInJob(x.id); } });
  out.runs = runs; out.leftFive = manifestCrates(); out.hauls = SHIP.jobs.filter(x => x.kind === 'haul').map(x => [x.id, x.crates.length, x.status, x.claimedBy, x.doneBy]);
  // Day 17: nobody takes it
  let d2 = 17; while (!haulDay(d2) || !playerShiftOn(d2)) d2++; const t2 = (d2 - 1) * 1440; out.d2 = d2;
  run(t0 + 1010, t2 + 610);
  for (const x of SHIP.jobs) if (x.kind === 'restock' && x.cargo === 'stores' && x.status !== 'done') jobFinish(x, shipNow(), 'crew');
  const m2 = manifestCrates(); out.d17 = [haulDay(d2), SHIP.jobs.filter(x => x.kind === 'restock').map(x => [x.id, x.status]), SHIP.manifest]; run(t2 + 620, t2 + 1300);
  const j2 = SHIP.jobs.filter(x => x.kind === 'haul' && Math.floor(x.posted / 1440) + 1 === d2);
  out.crew = [m2, j2.map(x => [x.status, x.doneBy]), manifestCrates()];
  return out;
})()"""
def m4_part(g):
    g.ev(f"({TRAIN})('m4')")   # Yara's training again: every crate of the day's training runs reaches its stop
    tr = g.ev("(() => { const js = SHIP.jobs.filter(x => x.kind === 'haul' && x.train === 'm4'), all = [...new Set(js.flatMap(x => x.crates.map(c => c.id)))]; return { runs: js.map(x => [x.only || 'yours', x.crates.length, x.doneBy]), all, delivered: [...new Set(simNotes('haul', 0).map(n => n.id))], left: manifestCrates() }; })()")
    print('  24d training runs:', json.dumps(tr))
    check(tr['all'] and sorted(tr['delivered']) == sorted(tr['all']) and tr['left'] == 0, f"m4: the training's crates all delivered {tr}")
    a = g.ev(M4_RUN); b = g.ev(M4_RUN)
    print('  24d hauling:', json.dumps(a))
    if not check(a.get('posted'), f"m4: no manifest run posted on Day 10 ({a.get('manifest')})"): return
    check(a['held'] and a['junior'] and a['claimed'], f"m4: held for you to 16:00, a junior job, taken ({a['held']}, {a['junior']}, {a['claimed']})")
    st = [s[0] for s in a['stops']]
    check(st[0] == 'cart' and st[-1] == 'return' and st.count('load') == st.count('deliver') == a['crates'] and all(s[1] for s in a['stops']), f"m4: stops {a['stops']}")
    check(a['holds'][0] == 'cart' and 'cartfull' in a['holds'], f"m4: the cart in hand {a['holds']}")
    check(a['workDone'] and a['turnin'] and a['left'] == 0 and len(a['got']) == a['crates'] == len(set(a['got'])) and len(a['notes']) == a['crates'] and a['use'] == 2, f"m4: every crate once ({a['got']}, left {a['left']}, notes {a['notes']}, use {a['use']})")
    check(a['five'] == 5 and a['runs'] == [4, 1] and a['leftFive'] == 0, f"m4: five crates in two runs {a['runs']} (left {a['leftFive']})")
    check(a['crew'][0] > 0 and a['crew'][1] and all(x[0] == 'done' and x[1] not in (None, 'you') for x in a['crew'][1]) and a['crew'][2] == 0, f"m4: the crew's run when you don't {a['crew']}")
    check(json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True), 'm4: differs the second time')
PARTS['m4'] = m4_part

# 24b your work uniform (seat M1): with clothes on (CLOTHES_ON, off at test URLs), oily jobs turned in from Day 8 add grime
# (.35 an oily repair, .2 an oily service, .05 anything else), nothing before Day 8; two oily repairs make you grubby
# (15c's uniformState) and set flag works.oily; the tint follows uniformState; the ladder's m2 opens on the next workday
# hour and trains you with Torres's word
M2_RUN = r"""(() => {
  const was = CLOTHES_ON; CLOTHES_ON = true; SHIP.works = null; SHIP.notes = []; SHIP.flags = {}; SHIP.mail = []; SHIP.clothes.grime = 0;
  WORKS_TICK.m = WORKS_TICK.h = -1; const out = {};
  const turn = (d, kind, mk, n) => { const m = machineList().find(x => x.kind === mk); setShipNow((d - 1) * 1440 + 600 + n); simNote('job', { step: 'turnin', id: 'mc' + d + n, machine: m && m.id, job: kind }); return SHIP.clothes.grime; };
  setShipNow(6 * 1440 + 300); const W = worksInit(); for (const r of CAREER_LADDER) if (r.id !== 'm2') { W.tr[r.id] = 1; W.use[r.id] = 9; (W.op[1] = W.op[1] || []).push(r.id); }
  out.before = [turn(7, 'repair', 'oven', 1), !!flag('works.oily')];
  out.steps = [turn(8, 'service', 'washer', 1), turn(8, 'repair', 'oven', 2), turn(8, 'service', 'range', 3)].map(x => Math.round(x * 100) / 100);
  out.state1 = uniformState(); out.flag = flag('works.oily');
  out.grubby = [turn(8, 'repair', 'galleyplant', 4), uniformState()];
  for (const f of WORK_TICKS) try { f(shipNow(), false); } catch (e) {}
  out.tint = player.rig.root.children.length ? (() => { let n = 0; player.rig.root.traverse(o => { if (o.isMesh && o.material === UNIFORM_MAT) n++; }); return n; })() : -1;
  SHIP.clothes.grime = 0; for (const f of WORK_TICKS) try { f(shipNow(), false); } catch (e) {}
  out.untint = (() => { let n = 0; player.rig.root.traverse(o => { if (o.isMesh && o.material === UNIFORM_MAT) n++; }); return n; })();
  CLOTHES_ON = was; return out;
})()"""
def m2_part(g):
    a = g.ev(M2_RUN); b = g.ev(M2_RUN)
    print('  24b uniform:', json.dumps(a))
    check(a['before'] == [0, False], f"m2: nothing before Day 8 {a['before']}")
    check(a['steps'] == [0.05, 0.4, 0.6] and a['flag'], f"m2: grime steps {a['steps']} (.05, +.35, +.2) and the oily flag {a['flag']}")
    check(a['grubby'][1] == 'grubby' and a['tint'] > 0 and a['untint'] == 0, f"m2: grubby and the tint ({a['grubby']}, {a['tint']} meshes, {a['untint']} after a change)")
    check(json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True), 'm2: differs the second time')
PARTS['m2'] = m2_part

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


# 24i tracing (seat M3): on paper, with the line functions of section 17 (MACHINE_LINKS, linePath, lineFlow; skipped,
# listed, when they aren't in the build). Day 12's training ends at 5-valve-2; a traced job hides its machine (card,
# stops, openJobs) until it's found; reading the middle (the Deck 5 pumps) then the valve finds it in two readings, a
# machine off the line or another line's says so; the job is then an ordinary repair, and fixing it clears the
# symptom; the crew fix one you leave; about half of an Officer's Tier 2 line repairs are traced; the Maps marks; the
# save (a junk symptom is not hidden); the air line's fan trace when the air line is in; the same twice.
M9 = r"""(() => {
  if (typeof traceLinesOn !== 'function' || !traceLinesOn()) return { lines: false };
  const out = { lines: true, air: tracePath('air', 4).length > 0 };
  const reset = t => { SHIP.works = null; SHIP.occasions.length = 0; SHIP.notes = []; SHIP.flags = {}; SHIP.jobs = []; SHIP.mail = []; MACH_HOUR = null; MACH_SEEN = -1; WORKS_TICK.m = WORKS_TICK.h = -1;
    setShipNow(t); machinesNow(); for (const id in SHIP.machines) { const s = SHIP.machines[id]; s.cond = 90; s.state = machineState(90); } MACH_REV++;
    const W = worksInit(); W.tier = 2; W.rank = 'officer'; W.tr.m9 = 12; return W; };
  const read = (j, id) => { TRACE_UI.at = id; const r = traceReading(j, id); traceRead(j); return r ? [id, traceKey(r.before), traceKey(r.after), !!j.traced] : [id, null]; };
  // a traced repair of 5-valve-2 on Day 13 (the training's machine, by hand)
  reset(12 * 1440 + 480);
  SHIP.machines['5-valve-2'].cond = 40; SHIP.machines['5-valve-2'].state = machineState(40); MACH_REV++;
  const id = jobReserve('5-valve-2', 13, 480, 19, { tier: 2 }), j = SHIP.jobs.find(x => x.id === id); delete j.make; j.parts = ['valve']; j.symptom = { line: 'water', deck: 4 };
  out.hidden = traceHidden(j); out.card = jobCard(j); out.stops = jobStops(j).map(s => [s.step, s.how, s.places.length, !!(s.opts && s.opts.read)]);
  out.open = openJobs().filter(x => x.id === id).map(x => [x.title, x.at, x.room]);
  out.path = tracePath('water', 4);
  out.claimed = claimJob(id); toolGive('pipekit');
  out.marks5 = (traceMarks(5) || {}).tiles; out.marks3 = (traceMarks(3) || {}).text;
  out.reads = [read(j, '5-pump-1'), read(j, '5-valve-2')];
  out.after = [traceHidden(j), jobCard(j)[0], jobStops(j).map(s => s.step)];
  out.save = (() => { const k = JSON.parse(JSON.stringify(j)); return [k.symptom, !!k.traced, k.read]; })();
  out.junk = [{ symptom: 'x' }, { symptom: { line: 'water', deck: 9 } }, { symptom: { line: 'lava', deck: 4 } }].map(x => traceHidden({ ...j, traced: null, ...x }));
  out.used = SHIP.works.use.m9; out.note = SHIP.notes.filter(n => n.kind === 'traced').map(n => n.line + ':' + n.machine);
  jobStops(j).forEach((s, k) => jobStepDone(id, k)); out.fixed = [!!j.workDone, SHIP.machines['5-valve-2'].state, traceFlow('water', '5-valve-2') >= .8];
  // upstream first: reading below the cause says "low before"; another line's machine and a machine off the lines
  reset(13 * 1440 + 480); SHIP.machines['3-uv-1'].cond = 30; SHIP.machines['3-uv-1'].state = machineState(30); MACH_REV++;
  const j2 = SHIP.jobs[SHIP.jobs.push({ id: 'uv@t', machine: '3-uv-1', deck: 3, kind: 'repair', urgency: 1, posted: shipNow(), found: shipNow(), claimedBy: null, parts: ['uv lamp'], status: 'open', symptom: { line: 'water', deck: 2 } }) - 1];
  claimJob('uv@t'); toolGive('pipekit');
  out.flows = tracePath('water', 2).map(st => traceKey(traceFlow('water', st[0])));
  out.reads2 = [read(j2, '5-valve-1'), read(j2, '3-pump-1'), read(j2, '3-filter-1'), read(j2, '3-uv-1')];
  out.offline = traceReading(j2, '4-heater-1');
  // the crew fix one you leave: an open traced job on Deck 5's pump, from 09:00 to 13:00
  reset(13 * 1440 + 540); SHIP.machines['5-pump-2'].cond = 35; SHIP.machines['5-pump-2'].state = machineState(35); MACH_REV++;
  const j3 = SHIP.jobs[SHIP.jobs.push({ id: 'p2@t', machine: '5-pump-2', deck: 5, kind: 'repair', urgency: 1, posted: shipNow(), found: shipNow(), claimedBy: null, parts: ['pump'], status: 'open', symptom: { line: 'water', deck: 5 } }) - 1];
  for (let m = 540; m <= 900; m += 60) { setShipNow(13 * 1440 + m); machinesNow(); }
  out.crew = [j3.status, j3.doneBy && j3.doneBy !== 'you' ? 'crew' : j3.doneBy, SHIP.machines['5-pump-2'].state];
  // how many are traced: every Tier 2 line machine's repair over 20 days (an Officer trained in m9), and none untrained
  let n = 0, tr = 0, un = 0, lines = {}; const W = reset(14 * 1440);
  for (let d = 14; d < 34; d++) for (const m of machineList()) {
    if (!Object.keys(MACHINE_LINKS).some(l => traceDecks(l, m.id).length)) continue;
    const jj = { id: 'x', machine: m.id, kind: 'repair' }; n++; if (traceOffer(jj, (d - 1) * 24 + 9)) { tr++; lines[jj.symptom.line] = (lines[jj.symptom.line] || 0) + 1; }
  }
  delete W.tr.m9; for (const m of machineList()) if (traceOffer({ id: 'y', machine: m.id, kind: 'repair' }, 14 * 24 + 9)) un++;
  out.share = [n, tr, lines, un];
  // the air line, once it's in: stuffy air on Deck 4 with a bad damper 2, from the middle (the fan) in two readings
  if (out.air) {
    reset(15 * 1440 + 480); SHIP.machines['5-damper-2'].cond = 35; SHIP.machines['5-damper-2'].state = machineState(35); MACH_REV++;
    const j4 = SHIP.jobs[SHIP.jobs.push({ id: 'd2@t', machine: '5-damper-2', deck: 5, kind: 'repair', urgency: 1, posted: shipNow(), found: shipNow(), claimedBy: null, parts: ['relay'], status: 'open', symptom: { line: 'air', deck: 4 } }) - 1];
    claimJob('d2@t'); toolGive('pipekit'); out.airReads = [read(j4, '5-fan-1'), read(j4, '5-damper-2')];
  }
  return out;
})()"""
def part_m9(g):
    tr = g.ev("SHIP.jobs.filter(x => x.train === 'm9').map(x => [x.kind, x.machine, x.symptom, x.doneBy])")   # the frame's training run, just before
    a = g.ev(M9)
    if not a['lines']:
        print('  m9: section 17\'s lines (MACHINE_LINKS, linePath, lineFlow) are not in this build: nothing traced')
        return
    b = g.ev(M9)
    print('  m9 training jobs:', tr)
    check(any(x[0] == 'tracedemo' and x[3] not in (None, 'you') for x in tr) and any(x[1] == '5-valve-2' and x[2] == {'line': 'water', 'deck': 4} and x[3] == 'you' for x in tr), 'm9: Day 12\'s training: Calder reads the line, then the traced 5-valve-2 is yours')
    print('  m9 path:', a['path'])
    print('  m9 card:', a['card'], 'stops:', a['stops'], 'board:', a['open'])
    print('  m9 reads:', a['reads'], '| upstream:', a['flows'], a['reads2'])
    print('  m9 after:', a['after'], 'fixed:', a['fixed'], 'crew:', a['crew'], 'share:', a['share'])
    check(a['hidden'] and 'Deck 4' in a['card'][0] and 'alve' not in a['card'][0], 'm9: the card names the symptom, not the valve')
    check(a['stops'] == [['read', 'look', len([1 for st in a['path'] for x in st]), True]], f"m9: one read stop at every machine on the line ({a['stops']})")
    check(a['open'] and a['open'][0][1] != [29, 15] and 'alve' not in a['open'][0][0], 'm9: the board doesn\'t point at the valve')
    check(a['marks5'] and [29, 15] in a['marks5'] and a['marks3'], 'm9: the Maps app marks the line')
    check(a['reads'] == [['5-pump-1', 'full', 'full', False], ['5-valve-2', 'full', 'low', True]], f"m9: middle then valve: found in two readings ({a['reads']})")
    check(a['after'][0] is False and 'Pipe valves' in a['after'][1] and a['after'][2][-1] == 'job', 'm9: found, it\'s an ordinary repair')
    check(a['save'][0] == {'line': 'water', 'deck': 4} and a['save'][1] and a['save'][2] == ['5-pump-1', '5-valve-2'], 'm9: the job saves its symptom and readings')
    check(a['junk'] == [False, False, False], 'm9: a junk symptom is not hidden')
    check(a['used'] == 1 and a['note'] == ['water:5-valve-2'], 'm9: a use and the traced note')
    check(a['fixed'] == [True, 'healthy', True], 'm9: fixing the cause clears the flow')
    check(a['flows'][:2] == ['full', 'full'] and a['flows'][2] != 'full' and all(f != 'full' for f in a['flows'][2:]), 'm9: the flow falls only downstream of the bad machine')
    check([r[3] for r in a['reads2']] == [False, False, False, True], 'm9: reading up from the end finds the UV steriliser')
    check(a['offline'] is None, 'm9: a machine off the job\'s line has no reading')
    check(a['crew'][0] == 'done' and a['crew'][1] == 'crew', 'm9: the crew fix a traced job you leave')
    n, t, lines, un = a['share']
    check(n and .35 <= t / n <= .65 and un == 0, f'm9: about half traced ({t} of {n}), none untrained ({un})')
    if a['air']: print('  m9 air:', a.get('airReads')); check([r[3] for r in a.get('airReads', [])] == [False, True], f"m9: stuffy air from the fan in two readings ({a.get('airReads')})")
    else: print('  m9: the air line is not in this build (the deck architect\'s turn): its trace skipped')
    check(json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True), 'm9: differs the second time')
PARTS['m9'] = part_m9

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
