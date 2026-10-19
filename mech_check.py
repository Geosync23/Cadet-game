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
  W.tier = Math.max(W.tier, row.tier || 1); if (row.rank) W.rank = row.rank;   // a Tier 2 row needs an Officer
  if (row.needs) for (const n of [].concat(row.needs)) if (n.trained && !ladderRow(n.trained)) W.tr[n.trained] = 1;   // a row it needs that isn't in this build
  const teamDo = jid => {                                   // a team job (24h): your turns as the lead calls them, the clock running
    const j = SHIP.jobs.find(x => x.id === jid); let t = Math.max(shipNow(), j.start - 5);
    for (let n = 0; n < 240 && j.status !== 'done'; n++, t++) { setShipNow(t); machinesNow(); worksCareerTick(t); for (const f of WORK_TICKS) f(t, false); if (j.seq && t >= j.start - 5) j.youIn = true; const mine = (j.seq || []).map((s, i) => s.who === 'you' ? i : -1).filter(i => i >= 0), k = mine.indexOf(j.cur); if (k >= 0 && !(j.stepsDone || []).includes(k)) jobStepDone(jid, k, j.seq[j.cur].how === 'turn' ? { value: 3 } : {}); }
    return j.status === 'done';
  };
  const seen = [], doJob = jid => { const j0 = SHIP.jobs.find(x => x.id === jid); if (j0 && j0.kind === 'team') return teamDo(jid); if (!claimJob(jid)) return false; const j = SHIP.jobs.find(x => x.id === jid);
    const cs = SHIP.works && SHIP.works.cases && (SHIP.works.cases.open || []).find(c => c.job === jid);   // a head-scratcher (24k): call it right first
    if (cs && typeof caseCall === 'function') caseCall(cs.id, cs.cause);
    jobStops(j).forEach((s, k) => jobStepDone(jid, k, j.kind === 'rewire' && s.step === 'wire' ? { pick: rewRight(j, k) } : undefined)); return turnInJob(jid); };   // 24q: a rewire's pairs answered from its chart
  let teacher = null, yours = null;
  for (let m = 360; m < 1020; m += 10) {
    const t = (d - 1) * 1440 + m; setShipNow(t); machinesNow(); worksCareerTick(t);
    if (typeof DIALOGUE !== 'undefined' && DIALOGUE && typeof dialogueEnd === 'function') dialogueEnd(true);   // read through
    const c = SHIP.works.cur;
    if (c) seen.push(c.st);
    if (c && c.st === 'meet') { const r = SHIP.occasions.find(x => x.key === c.occ); if (r && t >= r.at) { r.met = true; worksCareerTick(t + 1); } }
    if (c && c.st === 'watch') { c.w = TRAIN_WATCH; worksCareerTick(t + 2); const dj = SHIP.jobs.filter(x => x.train === id && x.status === 'done').pop(); teacher = dj ? dj.doneBy : null; }
    if (c && c.st === 'do' && (!myJob() || (SHIP.jobs.find(x => x.id === c.j) || {}).kind === 'team') && doJob(c.j)) yours = (SHIP.jobs.find(x => x.id === c.j) || {}).doneBy;
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
# the training since 0.45.9 (playtest 2, item 1): Torres's talk, then the first round is yours on the board (the whole
# training route, a washer first), nobody's leading or following; roundTrainStep() walks it: take, go, mark, next, done
M1_SELF = r"""(() => {
  SHIP.works = null; SHIP.occasions.length = 0; SHIP.notes = []; SHIP.flags = {}; SHIP.jobs = []; SHIP.mail = [];
  MACH_HOUR = null; MACH_SEEN = -1; WORKS_TICK.m = WORKS_TICK.h = -1;
  setShipNow(1440 + 300); machinesNow(); const W = worksInit(); W.log.push(['x', 1, 0, 'service']); const out = { steps: [] };
  for (let m = 1440 + 360; m <= 1440 + 900; m += 5) {
    setShipNow(m); machinesNow(); worksCareerTick(m);
    if (typeof DIALOGUE !== 'undefined' && DIALOGUE && typeof dialogueEnd === 'function') dialogueEnd(true);
    const c = W.cur; if (c && c.st === 'meet') { const r = SHIP.occasions.find(x => x.key === c.occ); if (r && m >= r.at) { r.met = true; worksCareerTick(m + 1); } }
    if (c && c.st === 'do') break;
  }
  const c = W.cur; out.st = c && c.st; if (!c || c.st !== 'do') return out;
  setShipNow(shipNow() + 2); machinesNow();   // it's posted for the next minute
  const j = SHIP.jobs.find(x => x.id === c.j); out.job = j && [j.kind, j.train, j.route.length, machineById(j.route[0]).kind, j.title, j.claimedBy || null, heldForYou(j)];
  out.teacherJobs = SHIP.jobs.filter(x => x.train === 'm1' && x.id !== j.id).length;
  out.board = openJobs('you').some(x => x.id === j.id);
  const st = () => { const r = roundTrainStep(); out.steps.push(r ? r.step + (r.machine ? ':' + r.machine : '') : null); return r; };
  st(); out.claimed = claimJob(j.id); st();
  const p = SHIP.people && SHIP.people.find ? null : null; out.escort = worksEscort({ id: c.by }, shipNow());
  for (let k = 0; k < j.route.length; k++) { jobStepDone(j.id, k, { pick: 'fine' }); st(); }
  out.turnin = turnInJob(j.id); out.trained = W.tr.m1; out.after = roundTrainStep();
  return out;
})()"""
def m1_part(g):
    s1 = g.ev(M1_SELF)
    s2 = g.ev(M1_SELF)
    print('  24a training (0.45.9):', json.dumps(s1))
    if check(s1.get('st') == 'do' and s1.get('job'), f"m1: after Torres's talk your first round is posted ({s1.get('st')})"):
        jb = s1['job']
        check(jb[0] == 'rounds' and jb[1] == 'm1' and 4 <= jb[2] <= 6 and jb[3] == 'washer' and jb[5] is None and jb[6], f"m1: the whole training route, a washer first, held for you, not yet taken ({jb})")
        check(s1['teacherJobs'] == 0 and s1['board'], 'm1: no teacher\'s round; yours is on the board')
        check(s1['claimed'] and s1['escort'] is None, 'm1: taken from the board; Torres doesn\'t follow')
        stp = [x.split(':')[0] if x else x for x in s1['steps']]
        check(stp[0] == 'take' and stp[1] == 'go' and all(x == 'next' for x in stp[2:-1]) and stp[-1] == 'done' and len(stp) == jb[2] + 2, f"m1: the walk-through steps {s1['steps']}")
        check(s1['turnin'] and s1['trained'] == 2 and s1['after'] is None, 'm1: turned in, trained on Day 2, no more steps')
    check(json.dumps(s1, sort_keys=True) == json.dumps(s2, sort_keys=True), 'm1: the training differs the second time')
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
  const invited = SHIP.bridgeInvited; SHIP.bridgeInvited = true;   // the planted manifest has a bridge crate: yours only once invited (S2's 0.33.57, C2's 0.44.17)
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
  SHIP.bridgeInvited = invited;
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

# ---- M8 team jobs (24h, seat M2): the rota over four weeks (Day 11 the recycler, Day 12 free, Tue/Thu 09:30, Fri 14:00 in
# even ship weeks, never one machine twice a week, a busy day moved within the week); a crew-only job runs on paper and
# puts the machines right; with you: your turns in order (out of turn refused), finished by you, +rep; late: your steps go
# to the lead and it runs slower; the save's part read back; the same twice
M8 = r"""(() => { const out = {}, W0 = JSON.stringify(SHIP.works);
 const reset = t => { machinesNew(); SHIP.jobs = []; MACH_HOUR = null; MACH_SEEN = -1; setShipNow(t); machinesNow(); SHIP.works = null; worksInit(t); SHIP.works.team = { plan: {} }; SHIP.works.inc = { plan: {}, open: null }; };
 reset(9 * 1440 + 300);
 out.plans = [1, 2, 3, 4].map(w => teamPlan(w).map(e => [e[0], weekday(e[0]), e[1], e[3]]));
 SHIP.works.team.plan = {}; out.again = JSON.stringify([1, 2, 3, 4].map(w => teamPlan(w).map(e => [e[0], weekday(e[0]), e[1], e[3]])));
 const run = (rank, act) => { reset(15 * 1440 + 900); SHIP.works.rank = rank; const r = {};
   for (let t = 15 * 1440 + 900; t <= 16 * 1440 + 760; t += 5) { setShipNow(t); machinesNow(); for (const f of WORK_TICKS) f(t, false); const j = SHIP.jobs.find(x => x.kind === 'team'); if (j && act) act(j, t, r); }
   const j = SHIP.jobs.find(x => x.kind === 'team');
   r.job = j && { team: j.team.length + (j.you ? 1 : 0), you: !!j.you && !j.youOut, status: j.status, by: j.doneBy, late: j.late, mins: j.doneAt - j.start, posted: j.posted - j.start };
   r.right = j ? j.machines.every(id => SHIP.machines[id].cond >= 90) : null; r.rep = SHIP.works.xp; r.uses = SHIP.works.use.m8 || 0; return r; };
 out.crew = run('junior');
 out.late = run('officer');
 out.you = run('officer', (j, t, r) => { if (j.status === 'done') return; if (t >= j.start - 5) j.youIn = true; const mine = j.seq.map((s, i) => s.who === 'you' ? i : -1).filter(i => i >= 0), k = mine.indexOf(j.cur);
   if (!r.early && JOB_KINDS.team.veto && j.cur >= 0 && k !== 0) r.early = jobStepDone(j.id, 0, {}).ok === false;
   if (k >= 0) { (r.turns = r.turns || []).push(jobStepDone(j.id, k, j.seq[j.cur].how === 'turn' ? { value: 3 } : {}).ok); for (const f of WORK_TICKS) f(t, false); } });
 SHIP.works.team.plan[9] = [[64, 570, 'x', 'washer']]; SHIP.works.team.plan[1] = [[11, 570, 'y', 'recycler']];
 out.save = JSON.stringify(teamClean(JSON.parse(JSON.stringify(SHIP.works.team)), 60)); out.saveOld = JSON.stringify(teamClean(undefined));
 SHIP.works = JSON.parse(W0); return out; })()"""
def part_m8(g):
    a, b = g.ev(M8), g.ev(M8)
    print('  m8 plan:', a['plans'])
    print('  m8 crew:', a['crew']['job'], 'late:', a['late']['job'], 'you:', a['you']['job'], a['you'].get('turns'), 'early refused', a['you'].get('early'))
    P = a['plans']
    check(P[0] == [[11, 3, 570, 'recycler']], 'm8: Day 11 the recycler at 09:30, Day 12 free')
    for w, wk in zip([2, 3, 4], P[1:]):
        check(2 <= len(wk) <= 3 and len(set(e[3] for e in wk)) == len(wk) and all(e[1] <= 4 for e in wk), f'm8: week {w + 1}: {wk}')
        check(any(e[2] == 840 and e[1] == 4 for e in wk) == ((w + 1) % 2 == 0) or (w + 1) % 2 == 0, f'm8: week {w + 1}: Fridays only in even ship weeks')
    check(P == json.loads(a['again']), 'm8: the plan the same when made again')
    c, l, y = a['crew'], a['late'], a['you']
    check(c['job'] and c['job']['status'] == 'done' and not c['job']['you'] and c['right'], 'm8: a crew-only team job runs and puts the machines right')
    check(l['job'] and l['job']['status'] == 'done' and l['job']['late'] and l['job']['mins'] > c['job']['mins'], 'm8: without you it starts after 15 minutes and runs slower')
    check(y['job'] and y['job']['by'] == 'you' and y.get('turns') == [True, True, True] and y['uses'] == 1 and y['rep'] >= 2, 'm8: your three turns in order, finished by you, +2')
    if not y.get('early'): print('  m8: (a turn out of order is not refused: section 17\'s stepDone hook not in this build)')
    s = json.loads(a['save'])
    check('9' in s['plan'] and '1' not in s['plan'] and json.loads(a['saveOld']) == {'plan': {}}, 'm8: the save read back (old weeks dropped)')
    check(json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True), 'm8: differs the second time')
PARTS['m8'] = part_m8

# 24i tracing (seat M3): on paper, with section 17's lines and traced faults (seat S2, 0.33.59: MACHINE_LINKS, linePath,
# lineFlow, traceHidden, traceMark, traceFor; skipped, listed, when they aren't in the build). Day 12's training ends at
# 5-valve-2 after Calder's reading; a traced job hides its machine (card, board, goal pointer) until it's found; reading
# the middle (the Deck 5 pumps) then the valve finds it in two readings; reading up from the end; a machine off the line
# has no reading; the job is then an ordinary repair, and fixing it clears the flow; the crew fix one you leave; about
# half of an Officer's line repairs are traced, none untrained; the save; the air line's fan trace; the same twice.
M9 = r"""(() => {
  if (typeof traceLinesOn !== 'function' || !traceLinesOn()) return { lines: false };
  const out = { lines: true, air: tracePath('air', 4).length > 0 };
  const reset = t => { SHIP.works = null; SHIP.occasions.length = 0; SHIP.notes = []; SHIP.flags = {}; SHIP.jobs = []; SHIP.mail = []; MACH_HOUR = null; MACH_SEEN = -1; WORKS_TICK.m = WORKS_TICK.h = -1;
    setShipNow(t); machinesNow(); for (const id in SHIP.machines) { const s = SHIP.machines[id]; s.cond = 90; s.state = machineState(90); } MACH_REV++;
    const W = worksInit(); W.tier = 2; W.rank = 'officer'; W.tr.m9 = 12; return W; };
  const key = v => flowWord(v).replace(' ', '');
  const read = (j, id) => { const b = lineFlow(j.symptom.line, id, true), a = lineFlow(j.symptom.line, id); TRACE_UI.at = id; const ok = traceRead(j, id); return ok ? [id, key(b), key(a), !!j.traceFound] : [id, null]; };
  const post = (id, deck, line, parts) => { SHIP.machines[id].state = machineState(SHIP.machines[id].cond); MACH_REV++;
    return SHIP.jobs[SHIP.jobs.push({ id: id + '@t', machine: id, deck: machineById(id).deck, kind: 'repair', urgency: 1, posted: shipNow(), found: shipNow(), claimedBy: null, parts, status: 'open', symptom: traceSymptom(line, id) }) - 1]; };
  // a traced repair of 5-valve-2 on Day 13 (the training's machine, by hand)
  reset(12 * 1440 + 480); SHIP.machines['5-valve-2'].cond = 40;
  const j = post('5-valve-2', 4, 'water', ['valve']), id = j.id;
  out.sym = j.symptom; out.hidden = traceHidden(j); out.card = jobCard(j);
  out.open = openJobs().filter(x => x.id === id).map(x => [x.title, x.at, x.room]);
  out.path = tracePath('water', 4);
  out.claimed = claimJob(id); toolGive('pipekit');
  const g = ixJobStep(); out.goal = g && [g.deck, g.place];
  out.marks5 = (traceMarks(5) || {}).tiles; out.marks3 = (traceMarks(3) || {}).text;
  out.reads = [read(j, '5-pump-1'), read(j, '5-valve-2')];
  out.after = [traceHidden(j), jobCard(j)[0], jobStops(j).map(s => s.step)];
  out.save = (() => { const k = JSON.parse(JSON.stringify(j)); return [k.symptom.deck, !!k.traceFound, k.read]; })();
  out.used = SHIP.works.use.m9; out.note = SHIP.notes.filter(n => n.kind === 'traceFound').map(n => n.line + ':' + n.machine);
  jobStops(j).forEach((s, k) => jobStepDone(id, k)); out.fixed = [!!j.workDone, SHIP.machines['5-valve-2'].state, lineFlow('water', '5-valve-2') >= .8];
  // upstream: reading up from the end; a machine off the line
  reset(13 * 1440 + 480); SHIP.machines['3-uv-1'].cond = 30;
  const j2 = post('3-uv-1', 2, 'water', ['uv lamp']); j2.symptom = { line: 'water', decks: [1, 2, 3], deck: 2 };
  claimJob(j2.id); toolGive('pipekit');
  out.flows = tracePath('water', 2).map(st => key(lineFlow('water', st[0])));
  out.reads2 = [read(j2, '5-valve-1'), read(j2, '3-pump-1'), read(j2, '3-filter-1'), read(j2, '3-uv-1')];
  out.offline = [traceMark(j2.id, '4-heater-1'), traceSteps(j2).some(x => x.includes('4-heater-1'))];
  // the crew fix one you leave: an open traced job on Deck 5's pump, from 09:00 to 15:00
  reset(13 * 1440 + 540); SHIP.machines['5-pump-2'].cond = 35;
  const j3 = post('5-pump-2', 5, 'water', ['pump']);
  for (let m = 540; m <= 900; m += 60) { setShipNow(13 * 1440 + m); machinesNow(); }
  out.crew = [j3.status, j3.doneBy && j3.doneBy !== 'you' ? 'crew' : j3.doneBy, SHIP.machines['5-pump-2'].state];
  // how many would be traced (section 17's traceFor): every line machine over 20 days, trained and not
  let n = 0, tr = 0, un = 0, lines = {}; const W = reset(14 * 1440);
  if (typeof traceFor === 'function') {
    for (let d = 14; d < 34; d++) for (const m of machineList()) { const l = lineOf(m.id); if (!l || !lineOn(l)) continue; n++; const t = traceFor(m, (d - 1) * 24 + 9); if (t) { tr++; lines[t] = (lines[t] || 0) + 1; } }
    out.trainedAfter = W.tr.m9; delete W.tr.m9; for (const m of machineList()) if (traceFor(m, 14 * 24 + 9)) un++; out.trainedBy = W.tr.m9;
  }
  out.share = [n, tr, lines, un];
  if (out.air) {
    reset(15 * 1440 + 480); SHIP.machines['5-damper-2'].cond = 35;
    const j4 = post('5-damper-2', 4, 'air', ['relay']); j4.symptom = { line: 'air', decks: [4], deck: 4 };
    claimJob(j4.id); toolGive('pipekit'); out.airReads = [read(j4, '5-fan-1'), read(j4, '5-damper-2')];
  }
  return out;
})()"""
def part_m9(g):
    tr = g.ev("SHIP.jobs.filter(x => x.train === 'm9').map(x => [x.kind, x.machine, x.symptom ? x.symptom.line + ':' + x.symptom.deck : null, x.doneBy])")   # the frame's training run, just before
    a = g.ev(M9)
    if not a['lines']:
        print('  m9: section 17\'s lines (MACHINE_LINKS, lineFlow, traceMark ...) are not in this build: nothing traced')
        return
    b = g.ev(M9)
    print('  m9 training jobs:', tr)
    check(any(x[0] == 'tracedemo' and x[3] not in (None, 'you') for x in tr) and any(x[1] == '5-valve-2' and x[2] == 'water:4' and x[3] == 'you' for x in tr), 'm9: Day 12\'s training: Calder reads the line, then the traced 5-valve-2 is yours')
    print('  m9 path:', a['path'], 'symptom:', a['sym'])
    print('  m9 card:', a['card'], 'board:', a['open'], 'goal:', a['goal'])
    print('  m9 reads:', a['reads'], '| upstream:', a['flows'], a['reads2'])
    print('  m9 after:', a['after'], 'fixed:', a['fixed'], 'crew:', a['crew'], 'share:', a['share'])
    check(a['hidden'] and 'Deck 4' in a['card'][0] and 'alve' not in a['card'][0], 'm9: the card names the symptom, not the valve')
    check(a['open'] and a['open'][0][1] is None and 'alve' not in a['open'][0][0], 'm9: the board doesn\'t point at the valve')
    check(a['goal'] and a['goal'][1] and '5-valve-2' not in a['goal'][1], f"m9: the goal pointer leads to the line, not the valve ({a['goal']})")
    check(a['marks5'] and [29, 15] in a['marks5'] and a['marks3'], 'm9: the Maps app marks the line')
    check(a['reads'] == [['5-pump-1', 'full', 'full', False], ['5-valve-2', 'full', 'low', True]], f"m9: middle then valve: found in two readings ({a['reads']})")
    check(a['after'][0] is False and 'Pipe valves' in a['after'][1] and a['after'][2][-1] == 'job', 'm9: found, it\'s an ordinary repair')
    check(a['save'] == [4, True, ['5-pump-1', '5-valve-2']], f"m9: the job keeps its symptom and readings ({a['save']})")
    check(a['used'] == 1 and a['note'] == ['water:5-valve-2'], 'm9: a use and the traceFound note')
    check(a['fixed'] == [True, 'healthy', True], 'm9: fixing the cause clears the flow')
    check(a['flows'][:2] == ['full', 'full'] and all(f != 'full' for f in a['flows'][2:]), f"m9: the flow falls only downstream of the bad machine ({a['flows']})")
    check([r[3] for r in a['reads2']] == [False, False, False, True], 'm9: reading up from the end finds the UV steriliser')
    check(a['offline'][1] is False, 'm9: a machine off the job\'s line isn\'t on its path')
    check(a['crew'][0] == 'done' and a['crew'][1] == 'crew', 'm9: the crew fix a traced job you leave')
    n, t, lines, un = a['share']
    if n:
        check(.35 <= t / n <= .65 and un == 0, f'm9: about half traced ({t} of {n}), none untrained ({un})')
        check(a.get('trainedBy') is None, 'm9: asking whether a repair is traced never trains you (section 17\'s traceFor)')
    else: print('  m9: section 17\'s traceFor not in this build: the share skipped')
    if a['air']: print('  m9 air:', a.get('airReads')); check([r[3] for r in a.get('airReads', [])] == [False, True], f"m9: stuffy air from the fan in two readings ({a.get('airReads')})")
    else: print('  m9: the air line is not in this build: its trace skipped')
    check(json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True), 'm9: differs the second time')
PARTS['m9'] = part_m9

# manifestRun (seat E1, 0.45.12; E2's team parts call it): two parts from their shelves to a machine's panel, held for
# you only; taken, every stop done in turn: the parts off the shelves once, delivered (j.delivered, the note), turned in;
# a second run nobody takes is withdrawn at its time; the Wednesday manifest still posts beside an open parts run
MRUN = r"""(() => {
  SHIP.works = null; SHIP.notes = []; SHIP.jobs = []; setShipNow(17 * 1440 + 600); machinesNow(); const W = worksInit(), out = {};
  SHIP.stores.filter = 3; SHIP.stores.pump = 3;   // on the shelves
  const s0 = { ...SHIP.stores }, id = manifestRun(['filter', 'pump'], '5-scrubber-1', { for: 'team-x', until: shipNow() + 120 });
  const j = SHIP.jobs.find(x => x.id === id); out.job = j && [j.kind, j.src, j.reserved, heldForYou(j), j.crates.length, jobStops(j).map(x => x.step + ':' + x.places[0])];
  out.claimed = claimJob(id); jobStops(j).forEach((x, k) => jobStepDone(id, k));
  out.took = ['filter', 'pump'].map(p => s0[p] - SHIP.stores[p]);
  out.delivered = [manifestRunDelivered(id), SHIP.notes.filter(n => n.kind === 'manifestRun').map(n => n.for + ':' + n.to + ':' + n.parts.join('+'))];
  out.turnin = turnInJob(id);
  const id2 = manifestRun(['lamp'], '4-washer-1', { until: shipNow() + 30 }), j2 = SHIP.jobs.find(x => x.id === id2);
  for (let m = 1; m <= 40; m++) { const t = shipNow() + 1; setShipNow(t); for (const f of WORK_TICKS) f(t, true); }
  out.withdrawn = [j2.status, j2.doneBy || null, manifestRunDelivered(id2)];
  out.bad = [manifestRun([], '4-washer-1'), manifestRun(['lamp'], 'nowhere')];
  // R5 (0.45.17): a part with none on its shelf isn't on the run; one emptied after asking says so at its load and isn't in the note
  SHIP.stores.valve = 0; SHIP.stores.filter = 2; SHIP.stores.pump = 1; SHIP.notes = [];
  const id3 = manifestRun(['valve', 'filter', 'pump'], '5-scrubber-1', { for: 'team-y' }), j3 = SHIP.jobs.find(x => x.id === id3);
  claimJob(id3); SHIP.stores.pump = 0; const says = jobStops(j3).map((x, k) => (jobStepDone(id3, k) || {}).say || '');
  out.empty = [j3.crates.map(c => c.id), says.filter(x => x.startsWith('No ')), SHIP.notes.filter(n => n.kind === 'manifestRun').map(n => n.parts.join('+'))];
  SHIP.works = null; return out;
})()"""
def part_mrun(g):
    a = g.ev(MRUN)
    b = g.ev(MRUN)
    print('  manifestRun:', json.dumps(a))
    jb = a['job']
    check(jb and jb[0] == 'haul' and jb[1] == 'stores' and jb[3] and jb[4] == 2 and jb[5][0].startswith('cart') and jb[5][-1].startswith('return') and sum(1 for x in jb[5] if x.startswith('deliver:5-scrubber-1')) == 2, f"manifestRun: a held parts run, shelves to the scrubber's panel ({jb})")
    check(a['claimed'] and a['took'] == [1, 1], f"manifestRun: each part off its shelf once ({a['took']})")
    check(a['delivered'][0] and a['delivered'][1] == ['team-x:5-scrubber-1-svc:filter+pump'] or (a['delivered'][0] and len(a['delivered'][1]) == 1 and a['delivered'][1][0].startswith('team-x:')), f"manifestRun: delivered, the note ({a['delivered']})")
    check(a['empty'] == [['filter', 'pump'], ['No pump on the shelf.'], ['filter']], f"manifestRun: an empty shelf's part not carried, said, not in the note ({a['empty']})")
    check(a['turnin'], 'manifestRun: turned in')
    check(a['withdrawn'] == ['done', None, False], f"manifestRun: one nobody takes is withdrawn at its time ({a['withdrawn']})")
    check(a['bad'] == [None, None], 'manifestRun: nothing for an empty list or an unknown place')
    check(json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True), 'manifestRun: differs the second time')

# hauling stage 2 (seat E1, 0.45.13; D3's answers on step4-stages): from 2 runs and Day 10 the delivery order is yours
# (j.order: the stops follow it); a tidy order (the fewest deck changes) says "A tidy run" and gives an officer +1, an
# untidy one nothing; after promotion the Wednesday run is held for you at stage 2, the crew's before it
HAUL2 = r"""(() => {
  SHIP.works = null; SHIP.notes = []; SHIP.jobs = []; setShipNow(16 * 1440 + 700); machinesNow(); const W = worksInit(), out = {};
  W.tr.m4 = 3; W.use.m4 = 2; (W.op[3] = []).push('m4'); W.rank = 'officer'; W.tier = 2;
  out.free = [haulFree(17), haulFree(9)];
  const mk = () => { const j = haulJob(shipNow(), [{ id: 'linen', dest: '4-laundry-drop' }, { id: 'store', dest: '3-store-drop' }, { id: 'galley', dest: '3-galley-drop' }], { yours: true }); SHIP.jobs.push(j); return j; };
  const j = mk(), deliver = x => jobStops(x).filter(s => s.step === 'deliver').map(s => s.places[0]);
  out.before = deliver(j); j.order = ['store', 'linen', 'galley']; out.after = deliver(j);
  const x0 = W.xp; j.order = ['linen', 'store', 'galley']; out.tidy = [haulTidy(j), W.xp - x0];
  j.order = ['store', 'linen', 'galley']; out.untidy = [haulTidy(j), W.xp - x0];
  // R5 (0.45.17): the load stops never move; the picks become j.order only when complete and before any delivery
  const loads = x => jobStops(x).filter(s => s.step === 'load').map(s => s.places[0] + ':' + (kindStops(x)[jobStops(x).indexOf(s)] || {}).crate);
  const dc = deviceChoose, stt = simTimeout; let pend = null; simTimeout = fn => fn(); deviceChoose = (v, f) => { pend = f; return true; };
  const j5 = mk(); j5.claimedBy = 'you'; j5.status = 'claimed'; const l0 = loads(j5); haulOrderAsk(j5); const mid = j5.order; pend(1); pend(0);
  out.order = [JSON.stringify(l0) === JSON.stringify(loads(j5)), mid === undefined, j5.order];
  const j6 = mk(); j6.claimedBy = 'you'; j6.status = 'claimed'; haulOrderAsk(j6); pend(2); const kd = jobStops(j6).findIndex(s => s.step === 'deliver'); j6.stepsDone = [0, 1, 2, 3, kd]; pend(0); out.order.push(j6.order === undefined);
  deviceChoose = dc; simTimeout = stt; SHIP.jobs = SHIP.jobs.filter(x => x !== j5 && x !== j6);
  W.rank = 'junior'; j.order = ['linen', 'galley', 'store']; const x1 = W.xp; out.junior = [haulTidy(j), W.xp - x1]; W.rank = 'officer';
  // the Wednesday run after promotion: held for you at stage 2, the crew's before it
  const post = use => { SHIP.jobs = []; W.use.m4 = use; SHIP.manifest = [{ id: 'linen', dest: '4-laundry-drop', n: 1 }, { id: 'store', dest: '3-store-drop', n: 1 }]; JOB_KINDS.haul.post(9 * 24 + 14, SHIP.jobs); const h = SHIP.jobs.find(x => x.kind === 'haul'); return h ? (h.released ? 'crew' : 'held') : null; };
  out.posts = [post(2), post(1)];
  SHIP.works = null; SHIP.manifest = []; return out;
})()"""
# hauling stage 3, the stocktake (seat E6, 0.45.15; step4-stages): Thursdays from Day 18, an officer trained in hauling:
# a side job at 13:30 held to 16:00; counting the aisles finds the week's short one (2 of its part move from stores to
# the hold's order, +1 capped), Thursday's misplaced part goes back, the turn-in pays nothing more; side.stock kept; one
# nobody takes is withdrawn at 16:00; a junior, a Wednesday and Day 11 get none
STOCKT = r"""(() => {
  SHIP.works = null; SHIP.notes = []; SHIP.jobs = []; setShipNow(17 * 1440 + 700); machinesNow(); SHIP.stores = { ...STOCK }; SHIP.hold = {};
  const W = worksInit(), out = {}; W.tr.m4 = 3; W.use.m4 = 2; (W.op[3] = []).push('m4'); W.rank = 'officer'; W.tier = 2;
  const post = (d, rank) => { W.rank = rank; const js = []; JOB_KINDS.stocktake.post((d - 1) * 24 + 13, js); W.rank = 'officer'; return js[0] || null; };
  out.none = [post(17, 'officer'), post(11, 'officer'), post(18, 'junior')].map(x => !!x);
  const j = post(18, 'officer'); SHIP.jobs.push(j);
  out.job = [j.posted - 17 * 1440, j.until - 17 * 1440, j.reserved, JOB_KINDS.stocktake.side, jobStops(j).map(s => s.places[0]), j.short && j.short.part];
  const p = j.short.part, s0 = SHIP.stores[p], aisle = FETCH_AT[j.short.aisle], other = FETCH_AT.find(x => x !== aisle);
  const mp = ((placeById(FETCH_AT.find(x => x !== other)) || {}).stock || []).find(k => k in STOCK);   // a part from another shelf, sitting on this one
  setShipNow(17 * 1440 + 840); machinesNow(); SHIP.misplaced = { part: mp, on: other }; j.claimedBy = 'you'; j.status = 'claimed'; j.start = shipNow();
  const x0 = W.xp, says = jobStops(j).map((st, k) => (jobStepDone(j.id, k, null) || {}).say || '');
  out.says = says; out.moved = [s0 - SHIP.stores[p], SHIP.hold[p] || 0, SHIP.misplaced]; out.xp = W.xp - x0;
  setShipNow(17 * 1440 + 900); machinesNow(); out.restock = SHIP.jobs.some(x => x.kind === 'restock' && x.cargo === 'stores');
  const x1 = W.xp; out.turnin = [turnInJob(j.id), W.xp - x1, JSON.stringify(W.side.stock)];
  const j2 = post(25, 'officer'); SHIP.jobs.push(j2); stockWithdraw(24 * 1440 + 959); const a = j2.status; stockWithdraw(24 * 1440 + 960); out.withdrawn = [a, j2.status, j2.doneBy];
  out.saved = JSON.stringify(worksClean(JSON.parse(JSON.stringify(W))).side.stock) === JSON.stringify(W.side.stock);
  SHIP.works = null; SHIP.misplaced = null; return out;
})()"""
# rounds stages 2 and 3 (seat E6, 0.45.16; step4-stages): after 5 rounds, taking a morning round asks you to pick 4-6 of
# the deck's machines, the longest unlooked first with "last looked" days; the route becomes your picks in walking
# order; two worn found on it: +1 (capped) and Torres's word. With the scanner (stage 2 and 5 rounds) the look at a
# room's first machine reads the rest of the route in that room (their stops done, the worn found by you, one scan's
# charge); the training round neither
ROUND23 = r"""(() => {
  SHIP.works = null; SHIP.notes = []; SHIP.jobs = []; setShipNow(11 * 1440 + 430); machinesNow(); ACT = null;
  const W = worksInit(), out = {}; W.tr.m1 = 2; W.use.m1 = 5; (W.op[2] = []).push('m1'); (W.op[12] = []).push('m11');
  for (const id in SHIP.machines) { const x = SHIP.machines[id]; x.cond = 95; x.state = 'healthy'; }
  const dc = deviceChoose, st = simTimeout, asked = []; simTimeout = (fn) => fn();
  deviceChoose = (v, f) => { asked.push(v.choices.slice()); const k = v.choices.indexOf("That's my round"); f(k >= 0 ? k : 0); return true; };
  const claim = j => { SHIP.jobs.push(j); j.claimedBy = 'you'; j.status = 'claimed'; j.start = shipNow(); };
  const pool = roundPool(4).map(m => m.id); roundLast()[pool[0]] = 10;
  const j = roundJob(12, 420); j.deck = 4; claim(j); out.before = j.route.slice();
  for (const f of WORK_TICKS) try { f(shipNow(), false); } catch (e) { }
  out.asked = asked.map(c => c.length); out.first = asked[0] && [asked[0][0], asked[0].find(x => x.includes(pool[0] ? machineLabel(machineById(pool[0])).split(',')[0] : '?'))];
  out.route = [j.route.length, j.route.every(id => machineById(id).deck === 4), JSON.stringify(j.route) === JSON.stringify(roundWalk(j.route.map(id => machineById(id)), DECKS[4])), j.stops.length, !!j.picked, j.pick === undefined];
  // two worn found: +1 and Torres
  for (const id of j.route.slice(0, 2)) { const x = SHIP.machines[id]; x.cond = 60; x.state = machineState(60); }
  const x0 = W.xp; jobStops(j).forEach((s, k) => jobStepDone(j.id, k, { pick: roundState(j.route[k]) === 'healthy' ? 'fine' : 'worn' }));
  out.two = [!!j.workDone, SHIP.notes.filter(n => n.kind === 'sideXp').map(n => n.why + n.n), Object.keys(roundLast()).filter(id => roundLast()[id] === 12).length];
  // stage 3: the doorway
  toolGive('scanner'); W.tr.m7 = 5; out.door = [roundDoorway()];
  setShipNow(12 * 1440 + 430); machinesNow(); const room = machineList().filter(m => m.deck === 4 && m.kind === 'washer' && panelPlace(m.id)).map(m => m.id).sort();
  for (const id in SHIP.machines) { const x = SHIP.machines[id]; x.cond = 95; x.state = 'healthy'; }
  for (const k of [1, 3]) { SHIP.machines[room[k]].cond = 60; SHIP.machines[room[k]].state = machineState(60); }   // room[3]: off the route, read from the doorway too (0.45.18)
  const j3 = roundJob(13, 420); j3.route = room.slice(0, 3).concat(j3.route.filter(id => !room.includes(id)).slice(0, 1)); j3.stops = kindStops(j3).map(plainStop); j3.picked = true; claim(j3);
  const c0 = toolCharge('scanner'), r3 = jobStepDone(j3.id, 0, { pick: 'fine' });
  out.door.push(room.length, r3.say || '', (j3.stepsDone || []).slice(), c0 - toolCharge('scanner'), (SHIP.jobs.find(x => x.machine === room[1] && x.status !== 'done') || {}).foundBy || null, (SHIP.jobs.find(x => x.machine === room[3] && x.status !== 'done') || {}).foundBy || null);
  // the training round: no doorway
  const jt = roundJob(13, 430, { train: 'm1', yours: true, slot: 1 }); jt.route = room.slice(); jt.stops = kindStops(jt).map(plainStop); claim(jt); jobStepDone(jt.id, 0, { pick: 'fine' }); out.train = (jt.stepsDone || []).slice();
  out.saved = JSON.stringify(worksClean(JSON.parse(JSON.stringify(W))).side.round) === JSON.stringify(W.side.round);
  deviceChoose = dc; simTimeout = st; SHIP.works = null; SHIP.jobs = []; return out;
})()"""
def part_round23(g):
    a = g.ev(ROUND23)
    b = g.ev(ROUND23)
    print('  rounds stages 2-3:', json.dumps(a))
    check(len(a['asked']) == 5 and a['asked'][0] > 4 and a['first'][0].endswith('not looked at yet') and a['first'][1] and a['first'][1].endswith('last looked 2 days ago'), f"round23: four asks, the unlooked first, last looked days ({a['asked']}, {a['first']})")
    check(a['route'] == [4, True, True, 4, True, True], f"round23: your four picks are the route, in walking order ({a['route']})")
    check(a['two'][0] and a['two'][1] == ['round1'] and a['two'][2] == 4, f"round23: two worn found: +1; last looked kept ({a['two']})")
    d = a['door']
    check(d[0] and d[1] == 4 and d[2].count('From the doorway') == 3 and d[2].count(', worn.') == 2 and d[3] == [0, 1, 2] and d[4] == 4 and d[5] == 'you' and d[6] == 'you', f"round23: one look reads every machine in the room (two on the route, one off it), the worn ones found by you, one scan's charge ({d})")
    check(a['train'] == [0], f"round23: the training round has no doorway ({a['train']})")
    check(a['saved'], 'round23: side.round kept by the save')
    check(json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True), 'round23: differs the second time')

def part_stock(g):
    a = g.ev(STOCKT)
    b = g.ev(STOCKT)
    print('  stocktake:', json.dumps(a))
    check(a['none'] == [False, False, False], f"stock: none on a Wednesday, before Day 18, for a junior ({a['none']})")
    jb = a['job']
    check(jb[0] == 810 and jb[1] == 960 and jb[2] and jb[3] and jb[4] == ['5-stock-1', '5-stock-2', '5-stock-3', '5-stock-4'] and jb[5], f"stock: a side job at 13:30 held to 16:00, one hold per aisle ({jb})")
    check(sum('is short of' in x for x in a['says']) == 1 and sum('all present' in x for x in a['says']) == 3 and sum('not where it lives' in x for x in a['says']) == 1, f"stock: one aisle short, three fine, the misplaced part found ({a['says']})")
    check(a['moved'] == [2, 2, None] and a['xp'] == 1 and a['restock'], f"stock: two of the part on the hold's order, the misplaced part back, +1 ({a['moved']}, {a['xp']})")
    check(a['turnin'][0] and a['turnin'][1] == 0 and a['turnin'][2] == '{"week": 2, "found": true}'.replace(' ', '') and a['saved'], f"stock: the turn-in pays nothing more; side.stock kept ({a['turnin']})")
    check(a['withdrawn'] == ['open', 'done', None], f"stock: withdrawn at 16:00 if nobody takes it ({a['withdrawn']})")
    check(json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True), 'stock: differs the second time')

def part_haul2(g):
    a = g.ev(HAUL2)
    b = g.ev(HAUL2)
    print('  hauling stage 2:', json.dumps(a))
    check(a['free'] == [True, False], f"haul2: from 2 runs and Day 10 ({a['free']})")
    check(a['before'] != a['after'] and a['after'] == ['3-store-drop', '4-laundry-drop', '3-galley-drop'], f"haul2: the stops follow your order ({a['after']})")
    check(a['tidy'] == [True, 1] and a['untidy'] == [False, 1] and a['junior'] == [True, 0], f"haul2: tidy +1 as an officer, untidy nothing, a junior's tidy no +1 ({a['tidy']}, {a['untidy']}, {a['junior']})")
    check(a['order'] == [True, True, ['store', 'linen', 'galley'], True], f"haul2: the load stops never move; the order set only when complete, never after a delivery ({a['order']})")
    check(a['posts'] == ['held', 'crew'], f"haul2: an officer's run held at stage 2, the crew's before ({a['posts']})")
    check(json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True), 'haul2: differs the second time')

# 24m tool upkeep (seat E1, 0.45.11): Day 12, an officer with the scanner and pipe kit; worn by use to "Due" (a quarter
# slower); at your bench: the pipe kit's hold puts it back, the scanner charges 5 minutes on its own; the first upkeep
# trains m11; +1 for a week kept up, once; after 4 upkeeps the team's rack once a week; saved; the same twice
M11 = r"""(() => {
  SHIP.works = null; SHIP.notes = []; SHIP.jobs = []; setShipNow(11 * 1440 + 600); machinesNow(); ACT = null;
  const W = worksInit(), out = {}; W.tier = 2; W.rank = 'officer'; W.op[12] = ['m11']; toolGive('scanner'); toolGive('pipekit');
  for (let i = 0; i < 18; i++) { toolWear('scanner', 4); toolWear('pipekit', 5); }
  out.due = [toolState('scanner'), toolState('pipekit'), toolSlow('pipekit')];
  const hold = () => { const a = ACT; const r = a && a.kind === 'benchHold' ? [a.def.mins, a.placeId] : null; if (a && a.def.onDone) a.def.onDone(a); ACT = null; return r; };
  const x0 = W.xp; out.tap = benchTools(); out.kit = [benchStart('pipekit'), hold(), toolState('pipekit'), W.tr.m11 || null];
  out.charge = [benchStart('scanner'), benchData().charge.at - shipNow()];
  const tick = t => { setShipNow(t); for (const f of WORK_TICKS) f(t, true); };
  tick(shipNow() + 4); out.mid = toolState('scanner'); tick(shipNow() + 1); out.end = [toolState('scanner'), !!benchData().charge];
  out.xp = W.xp - x0; benchStart('pipekit'); hold(); out.xp2 = W.xp - x0;
  out.rack0 = rackTap(); ACT = null; W.use.m11 = 4; out.stage = worksStage('m11');
  out.rack = [rackTap(), hold(), benchData().rack, rackTap()]; ACT = null;
  const c = worksClean(JSON.parse(JSON.stringify(W))); out.saved = JSON.stringify(c.side.upkeep) === JSON.stringify(W.side.upkeep);
  out.notes = SHIP.notes.filter(n => n.kind === 'upkeep').map(n => n.tool);
  SHIP.works = null; return out;
})()"""
def part_m11(g):
    a = g.ev(M11)
    b = g.ev(M11)
    print('  24m:', json.dumps(a))
    check(a['due'] == ['due', 'due', 1.25], f"m11: worn to due by use, a quarter slower ({a['due']})")
    check(a['tap'] == ['scanner', 'pipekit'], 'm11: the bench offers your two tools')
    check(a['kit'][0] and a['kit'][1] == [2, '5-bench-you'] and a['kit'][2] == 'charged' and a['kit'][3] == 12, f"m11: the pipe kit's 2 minutes at your bench, charged, trained Day 12 ({a['kit']})")
    check(a['charge'] == [True, 5] and a['mid'] == 'due' and a['end'] == ['charged', False], f"m11: the scanner on charge 5 minutes, you needn't stay ({a['charge']}, {a['mid']}, {a['end']})")
    check(a['xp'] == 1 and a['xp2'] == 1, f"m11: +1 for the week's tools kept up, once ({a['xp']}, {a['xp2']})")
    check(a['rack0'] is False and a['stage'] == 2 and a['rack'][0] and a['rack'][1] == [3, '5-tool-rack'] and a['rack'][2] == 1 and a['rack'][3] is False, f"m11: the team's rack after 4 upkeeps, once a week ({a['rack0']}, {a['stage']}, {a['rack']})")
    check(a['saved'] and a['notes'] == ['pipekit', 'scanner', 'pipekit', 'rack'], f"m11: saved, notes {a['notes']}")
    check(json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True), 'm11: differs the second time')
PARTS['m11'] = part_m11

# 24n the logbook (seat E1, 0.45.11): Day 12 an officer's shift (a pump fitted on Washer 2, Washer 3 found and left, Washer
# 1 still yours): three summaries from it in the day's order; an entry once a day (+1, a use, the open jobs logged and 10%
# quicker for whoever takes them); stage 2's flag looked at by the night crew at 22:00; logLast; saved; the same twice
M12 = r"""(() => {   // the machines afresh, then only the jobs staged here: the catch-up can post its own (X3: a real Washer 3 job with 0.71.5's crew)
  SHIP.works = null; setShipNow(11 * 1440 + 990); machinesNew(); MACH_HOUR = null; MACH_SEEN = -1; setShipNow(11 * 1440 + 990); machinesNow(); SHIP.jobs = []; SHIP.notes = []; ACT = null;
  const W = worksInit(), out = {}, t = shipNow(); W.tier = 2; W.rank = 'officer'; W.op[12] = ['m12'];
  SHIP.jobs.push({ id: '4-washer-2@x', machine: '4-washer-2', deck: 4, kind: 'repair', parts: ['pump'], status: 'done', doneBy: 'you', posted: t - 300, found: t - 300 });
  W.log.push(['4-washer-2@x', 12, 0, 'repair']);
  SHIP.jobs.push({ id: '4-washer-3@x', machine: '4-washer-3', deck: 4, kind: 'service', parts: [], status: 'open', claimedBy: null, posted: t - 100, found: t - 100, urgency: 1 });
  simNote('found', { machine: '4-washer-3', by: 'you' });
  SHIP.jobs.push({ id: '4-washer-1@x', machine: '4-washer-1', deck: 4, kind: 'repair', parts: ['belt'], status: 'claimed', claimedBy: 'you', posted: t - 200, found: t - 200, urgency: 1 });
  out.choices = logChoices(12).map(c => c.text);
  const x0 = W.xp, j3 = SHIP.jobs.find(x => x.id === '4-washer-3@x'), m0 = jobMins(j3);
  const cs = logChoices(12), pick = cs.find(c => c.jobs.includes('4-washer-3@x')) || cs[0];
  out.entry = logbookWrite(pick, 12); out.again = logbookWrite(pick, 12);
  out.logged = [j3.logged || null, Math.round(jobMins(j3) / m0 * 100) / 100]; out.xp = W.xp - x0; out.trained = W.tr.m12 || null;
  out.last = logLast(1);
  W.use.m12 = 5; out.stage = worksStage('m12'); out.entry.flag = '4-washer-3';
  const s = SHIP.machines['4-washer-3']; s.cond = 60; s.state = 'worn';
  for (let m = 1000; m <= 1330; m += 10) { setShipNow(11 * 1440 + m); logbookTick(shipNow(), true); }
  out.night = [j3.status, j3.doneBy, SHIP.notes.filter(n => n.kind === 'logFlag').map(n => n.machine)];
  const again = (id, st, held) => {                      // R5 (0.45.14): only a worn machine, never a job held for you
    const jx = { id: id + '@y', machine: id, deck: 4, kind: 'repair', parts: [], status: 'open', claimedBy: null, posted: t - 50, found: t - 50, urgency: 1, ...(held ? { reserved: 30 } : {}) };
    SHIP.jobs.push(jx); SHIP.machines[id].state = st; out.entry.flag = id; out.entry.looked = false;
    setShipNow(11 * 1440 + 1330); logbookTick(shipNow(), true); return jx.status; };
  out.night2 = [again('4-washer-1', 'failing', false), again('4-washer-2', 'worn', true)];
  const c = worksClean(JSON.parse(JSON.stringify(W))); out.saved = JSON.stringify(c.side.log) === JSON.stringify(W.side.log);
  SHIP.works = null; return out;
})()"""
def part_m12(g):
    a = g.ev(M12)
    b = g.ev(M12)
    print('  24n:', json.dumps(a))
    ch = a['choices']
    check(len(ch) == 3 and any('Washer 2' in c and 'pump' in c for c in ch) and any('Washer 3' in c for c in ch) and any('Washer 1' in c for c in ch), f"m12: three summaries of the real shift ({ch})")
    check(a['entry'] and a['again'] is None and a['xp'] == 1 and a['trained'] == 12, f"m12: one entry a day, +1, trained Day 12 ({a['again']}, {a['xp']}, {a['trained']})")
    check(a['logged'] == [12, 0.9], f"m12: the open job written up is 10% quicker ({a['logged']})")
    check(a['last'] and a['last'][0] == a['entry']['pick'], 'm12: logLast reads it back')
    check(a['night2'] == ['open', 'open'], f"m12: the night crew leave a faulty machine and a job held for you ({a['night2']})")
    check(a['stage'] == 1 and a['night'][0] == 'done' and a['night'][1] not in (None, 'you') and a['night'][2] == ['4-washer-3'], f"m12: the flagged machine seen to by the night crew at 22:00 ({a['night']})")
    check(a['saved'], 'm12: saved')
    if not check(json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True), 'm12: differs the second time'): print('  m12 twice:', [k for k in a if a[k] != b.get(k)], json.dumps(b)[:600])
PARTS['m12'] = part_m12

# Step 4's core (seat E1, 0.45.7, on C's behalf): tool wear in the page's numbers (charge 100 - wear: the scanner 4 a
# scan; "Getting low" under 60, "Due" under 30), a due tool a quarter slower with its toast once a day, never blocking;
# worksUse no longer wears the three again; the side-job cap (+2 Works reputation a ship day in all); SHIP.works.side kept
# by the save's tidy (worksClean), an old save without it and a junk one; section 15's Bunk 1 texts name your cabin's room
# after the move (playerBed() follows SHIP.works.home). The same twice. Run alone: mech_check.py BUILD side
SIDE = r"""(() => {
  const out = {}; SHIP.works = null; SHIP.notes = []; SHIP.jobs = []; setShipNow(11 * 1440 + 540); const W = worksInit();
  out.order = Object.keys(W).slice(-2).join(',');   // worksInit: side right after cur, as worksClean makes it
  toolGive('scanner'); toolGive('pipekit');
  for (let i = 0; i < 20; i++) toolWear('scanner', 4); out.early = [toolCharge('scanner'), toolSlow('scanner')];   // before M11 opens: no wear (R4)
  (W.op[12] = W.op[12] || []).push('m11');   // M11 open (Day 12)
  out.fresh = [toolState('scanner'), toolCharge('scanner'), toolSlow('scanner'), toolStateWord('scanner')];
  for (let i = 0; i < 11; i++) toolWear('scanner', 4);
  out.low = [toolState('scanner'), toolCharge('scanner'), toolSlow('scanner')];
  for (let i = 0; i < 7; i++) toolWear('scanner', 4);
  out.due = [toolState('scanner'), toolCharge('scanner'), toolSlow('scanner'), toolSlow('scanner'), toolStateWord('scanner')];
  out.said = W.side && W.side.slow && W.side.slow.scanner;
  out.none = [toolState('logger'), toolSlow('logger'), toolWear('logger', 3)];
  worksUse('m9'); worksUse('m7'); out.uses = [toolCharge('pipekit'), toolCharge('scanner')];
  // a look step with a due tool: a quarter longer, and still a step (never blocked)
  const look = tool => { SHIP.player.wsteps = []; ACT = null; const j = { id: 'probe@s4', title: 'Probe' };
    const st = { step: 'read', places: [], how: 'look', opts: { secs: 4, ...(tool ? { tool } : {}) } };
    const took = workStep(j, st, 63, null); const m = ACT && ACT.def ? ACT.def.mins : null; ACT = null; SHIP.player.wsteps = []; return [took, m]; };
  for (let i = 0; i < 18; i++) toolWear('pipekit', 5);
  const a = look(null), b = look('pipekit'); out.look = [a[0], b[0], a[1] && b[1] ? Math.round(b[1] / a[1] * 100) / 100 : null];
  // the cap
  const x0 = W.xp; out.xp = [worksSideXp(1, 'a'), worksSideXp(3, 'b'), worksSideXp(1, 'c'), worksSideXp(-1, 'd')]; out.gain = W.xp - x0;
  setShipNow(12 * 1440 + 540); out.xp2 = worksSideXp(3, 'e');
  WORKS_SIDE_KINDS.add('probe'); setShipNow(13 * 1440 + 540); const x1 = W.xp; for (const k of ['p1', 'p2', 'p3']) simNote('job', { step: 'turnin', id: k, job: 'probe' });
  simNote('job', { step: 'turnin', id: 'p4', job: 'service' }); out.turnin = W.xp - x1; WORKS_SIDE_KINDS.delete('probe'); out.notes = SHIP.notes.filter(n => n.kind === 'sideXp').map(n => n.why + n.n);
  // R5 (0.45.14): a side kind turned in right first time pays +1 more; j.xp 0 pays nothing; found by you adds nothing to a side kind
  WORKS_SIDE_KINDS.add('probe'); const pay = (day, j) => { setShipNow(day * 1440 + 540); SHIP.jobs.push({ status: 'done', ...j }); const x = W.xp; simNote('job', { step: 'turnin', id: j.id, job: 'probe' }); return W.xp - x; };
  out.right = [pay(14, { id: 'q1', kind: 'probe', rightFirst: true }), pay(15, { id: 'q2', kind: 'probe', rightFirst: true, xp: 0 }), pay(16, { id: 'q3', kind: 'probe', foundBy: 'you' })];
  WORKS_SIDE_KINDS.delete('probe'); SHIP.jobs = SHIP.jobs.filter(x => !/^q\d$/.test(x.id));
  // the save's tidy
  const c = worksClean(JSON.parse(JSON.stringify(W))); out.kept = !!c && JSON.stringify(c.side) === JSON.stringify(W.side) && JSON.stringify(c.tools) === JSON.stringify(W.tools);
  const old = JSON.parse(JSON.stringify(W)); delete old.side; const c2 = worksClean(old); out.old = !!c2 && JSON.stringify(c2.side) === '{}' && Object.keys(c2).indexOf('side') === Object.keys(c2).indexOf('cur') + 1;   // an old save: side {} right after cur (BM7: the key order)
  const junk = JSON.parse(JSON.stringify(W)); junk.side = [1, 2]; out.junk = JSON.stringify((worksClean(junk) || {}).side) === '{}';
  // Bunk 1's texts
  const P = SHIP.player, e0 = P.needs.energy; P.needs.energy = 5;
  out.bunk = [bedText('Your bunk\'s in Bunk 1 on Deck 4.'), needsLine().includes('Bunk 1')];
  W.home = '4-23'; out.bunk.push(playerBed(), bedText('Your bunk\'s in Bunk 1 on Deck 4.'), needsLine().includes('Bunk 1'), needsLine().includes(myBedRoom()));
  P.needs.energy = e0; SHIP.works = null;
  return out;
})()"""
def part_side(g):
    a = g.ev(SIDE)
    b = g.ev(SIDE)
    print('  side tools:', a['fresh'], a['low'], a['due'], 'none:', a['none'], 'uses:', a['uses'], 'look:', a['look'])
    print('  side rep:', a['xp'], a['gain'], a['xp2'], a['notes'], '| save:', a['kept'], a['old'], a['junk'], '| bunk:', a['bunk'])
    check(a['early'] == [100, 1], f"side: no wear before M11 tool upkeep is open ({a['early']})")
    check(a['fresh'][:3] == ['charged', 100, 1] and a['fresh'][3] == 'Charged', f"side: a new tool is charged ({a['fresh']})")
    check(a['low'] == ['low', 56, 1], f"side: eleven scans: getting low, not slower ({a['low']})")
    check(a['due'][:4] == ['due', 28, 1.25, 1.25] and a['due'][4] == 'Due', f"side: eighteen scans: due, a quarter slower ({a['due']})")
    check(a['said'] == 12, 'side: the toast once on the day (Day 12)')
    check(a['none'] == [None, 1, 0], 'side: a tool you don\'t have has no state and doesn\'t slow you')
    check(a['uses'] == [100, 28], f"side: worksUse doesn't wear the scanner or the pipe kit again ({a['uses']})")
    check(a['look'][0] and a['look'][1] and a['look'][2] == 1.25, f"side: a look step with a due tool takes a quarter longer and still starts ({a['look']})")
    check(a['xp'] == [1, 1, 0, 0] and a['gain'] == 2 and a['xp2'] == 2, f"side: side jobs give at most +2 a day ({a['xp']}, {a['xp2']})")
    check(a['notes'] == ['a1', 'b1', 'e2', 'probe1', 'probe1'], f"side: the sideXp notes ({a['notes']})")
    check(a['turnin'] == 3, f"side: side-job kinds turned in at the board are capped too (+2), an ordinary job isn't (+1) ({a['turnin']})")
    check(a['right'] == [2, 0, 1], f"side: a side kind right first time pays 2, j.xp 0 pays 0, found by you pays 1 ({a['right']})")
    check(a.get('order') == 'cur,side', f"side: a new SHIP.works has side right after cur ({a.get('order')})")
    check(a['kept'] and a['old'] and a['junk'], 'side: SHIP.works.side kept by the save\'s tidy; an old save loads without it; junk dropped')
    check(a['bunk'][0] == 'Your bunk\'s in Bunk 1 on Deck 4.' and a['bunk'][1] and a['bunk'][2] == '4-23' and a['bunk'][3] == 'Your bunk\'s in Cabin 4-23 on Deck 4.' and not a['bunk'][4] and a['bunk'][5],
          f"side: the texts name Bunk 1 before the move and your cabin after ({a['bunk']})")
    check(json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True), 'side: differs the second time')
# ---- M13 leak hunting (24o, seat E2): stand-ins first, where a seat's piece isn't in this build (24 core's worksSide, E3's
# leak joints: printed). The week's day (a workday of yours, Day 12 on, not the incident's day) the same twice; the first
# leak at 08:00 once the row is open, the board saying only the deck; the puddle first (the damp and the joint refused
# before it), then the joint tightened: found by you, the puddle gone, trained; a worn joint posts its replacement, held
# for you; not taken, the crew fix it the next day; after 3 leaks the galleries too; junk in the save cleaned; the look
# (puddle and damp) on the deck only while a leak is open; the same twice
M13_STAND = r"""(() => { const out = [];
  if (typeof worksSide !== 'function') { window.worksSide = () => SHIP.works ? (SHIP.works.side = SHIP.works.side || {}) : null; out.push('worksSide'); }
  if (![3, 4, 5].some(n => (DECKS[n].leakJoints || []).length)) { out.push('leakJoints');
    for (const n of [3, 4, 5]) { const v = placeById(n + '-valve-1'), w = placeById(n + '-wet-1'), w2 = placeById(n + '-wet-2');
      DECKS[n].leakJoints = [{ place: n + '-valve-1', room: v.room, wall: 'n', joint: [v.at[0] + .5, 1.6, v.at[1]], damp: [v.at[0], v.at[1], 'n'], puddle: w.at.slice(), puddlePlace: n + '-wet-1' },
        { place: n + '-valve-3', room: v.room, wall: 'n', joint: [v.at[0] + 1.5, 1.6, v.at[1]], damp: [v.at[0] + 1, v.at[1], 'n'], puddle: w2.at.slice(), puddlePlace: n + '-wet-2', ...(n === 5 ? { gallery: true, works: true } : {}) }]; } }
  return out; })()"""
M13 = r"""(() => { const out = {}, W0 = JSON.stringify(SHIP.works);
 const reset = t => { machinesNew(); SHIP.jobs = []; MACH_HOUR = null; MACH_SEEN = -1; setShipNow(t); machinesNow(); SHIP.works = null; const W = worksInit(t); W.tier = 2; W.rank = 'officer'; W.tr.t2 = 10; (W.op[12] = W.op[12] || []).push('m13'); W.inc = { plan: {}, open: null }; worksSide().leaks = []; return W; };
 const tick = (a, b, skip) => { for (let t = a; t <= b; t += 10) { setShipNow(t); machinesNow(); for (const f of WORK_TICKS) f(t, !!skip); } };
 let W = reset(11 * 1440 + 300);
 out.days = [1, 2, 3, 4, 5].map(w => { const d = leakDay(w); return d === null ? null : [d, weekday(d), playerShiftOn(d), (incPlan(w)[1] || 0) !== d]; });
 tick(11 * 1440 + 360, 11 * 1440 + 470); out.before8 = SHIP.jobs.filter(x => x.kind === 'leak').length;
 tick(11 * 1440 + 480, 11 * 1440 + 490);
 let j = SHIP.jobs.find(x => x.kind === 'leak'); out.posted = j ? [j.title, j.deck, Math.round(j.posted % 1440)] : null; if (!j) return out;
 const ob = openJobs().find(x => x.id === j.id); out.board = ob ? [ob.place, ob.room, ob.deck] : null;
 out.claimed = claimJob(j.id); const st = jobStops(j); out.stops = st.map(s => s.step + ':' + s.how + '@' + (s.places[0] || '-'));
 out.early = jobStepDone(j.id, 2, { value: 3 }).ok;
 out.puddle = jobStepDone(j.id, 0, {}).ok; out.after = jobStops(j).map(s => s.places[0] || '-');
 out.damp = jobStepDone(j.id, 1, {}).ok; out.joint = jobStepDone(j.id, 2, j.worn ? {} : { value: 3 }).ok;
 const xp0 = W.xp; out.turnin = turnInJob(j.id); out.xp = [W.xp - xp0, typeof WORKS_SIDE_KINDS !== 'undefined']; out.entry = JSON.parse(JSON.stringify(worksSide().leaks[0])); out.open = leakOpen(); out.trained = W.tr.m13; out.uses = W.use.m13; out.wornFix = j.fix || null;
 // a worn joint: its replacement posted, held for you
 W = reset(15 * 1440 + 480); leakPost(15 * 1440 + 480, 2); j = SHIP.jobs.find(x => x.kind === 'leak'); j.worn = 1; claimJob(j.id);
 jobStops(j).forEach((s, k) => jobStepDone(j.id, k, {})); turnInJob(j.id);
 const F = SHIP.jobs.find(x => x.id === j.fix); out.worn = F ? [F.chore, F.target === j.joint, F.parts.join(), F.xp, forYou(F) && leaveEnd(F) > shipNow()] : null;
 // not taken: held to 10:00 the next workday, then the crew's (the long way)
 W = reset(15 * 1440 + 480); leakPost(15 * 1440 + 480, 2); j = SHIP.jobs.find(x => x.kind === 'leak'); out.held = leaveEnd(j) - 15 * 1440;
 tick(15 * 1440 + 490, 16 * 1440 + 900); out.crew = [j.status, j.doneBy && j.doneBy !== 'you', (worksSide().leaks[0] || {}).found !== null, leakOpen()];
 // the galleries after 3 leaks
 W = reset(15 * 1440 + 300); const pick = () => [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13].map(w => leakPick(w)).filter(Boolean).map(P => !!P.J.gallery);
 out.gal0 = pick().filter(Boolean).length; worksSide().leaks = [1, 2, 3].map(k => ({ id: 'leak:x' + k, joint: '4-valve-1', room: 'x', deck: 4, day: 12, worn: 0, found: 'you' })); out.gal3 = pick().filter(Boolean).length;
 W.use.m13 = 3; out.stage = worksStage('m13');
 // the save: junk dropped
 worksSide().leaks = [{ id: 'leak:a', joint: '3-valve-1', deck: 3, day: 15, worn: 1, found: null }, { id: 7 }, null, { id: 'b', joint: 'x', deck: 9, day: 1 }, 'junk'];
 delete worksSide().leaksOk; Object.defineProperty(worksSide(), 'leaksOk', { value: false, configurable: true });
 out.save = JSON.stringify(leakList()); worksSide().leaks = 'junk'; out.saveJunk = JSON.stringify(leakList());
 SHIP.works = JSON.parse(W0); return out; })()"""
M13_FX = r"""(() => { if (typeof deckDef === 'undefined' || !deckDef || ![3, 4, 5].includes(deckDef.num)) return null;
 const W0 = JSON.stringify(SHIP.works), n = deckDef.num, J = DECKS[n].leakJoints[0]; if (!SHIP.works) worksInit(shipNow());
 const S = worksSide(); S.leaks = [{ id: 'leak:fx', joint: J.place, room: J.room, deck: n, day: 12, worn: 0, found: null }];
 leakFx(); const on = [!!LEAK_FX.wet, !!LEAK_FX.damp, !!(LEAK_FX.wet && LEAK_FX.wet.parent), LEAK_FX.wet ? LEAK_FX.wet.count : 0];
 S.leaks[0].found = 'you'; leakFx(); const off = [!!LEAK_FX.wet, !!LEAK_FX.damp];
 SHIP.works = JSON.parse(W0); leakFx(); return { deck: n, on, off }; })()"""
def part_m13(g):
    check(g.ev(ROW_AGREE)['m13'], 'm13: the ladder row (24 core) and 24o disagree (day, stages, by)')
    st = g.ev(M13_STAND)
    if st: print('  m13 stand-ins:', st)
    a, b = g.ev(M13), g.ev(M13)
    print('  m13 days:', a['days'], 'posted', a['posted'], 'board', a['board'], 'stops', a['stops'], 'then', a['after'])
    for e in a['days']:
        if e: check(e[0] >= 12 and e[1] <= 4 and e[2] and e[3], f'm13: the week\'s day {e}')
    check(a['before8'] == 0 and a['posted'] and a['posted'][2] == 480 and 'Deck' in a['posted'][0], 'm13: the first leak at 08:00, the board says the deck')
    check(a['board'] and a['board'][0] is None and a['board'][1] is None, f"m13: the board doesn't say where ({a['board']})")
    check(a['stops'] and a['stops'][0].startswith('puddle:look@') and '@-' not in a['stops'][0] and a['stops'][1].endswith('@-') and a['stops'][2].endswith('@-'), 'm13: the puddle shown, the damp and the joint not yet')
    check(not a['early'] and a['puddle'] and '-' not in a['after'], 'm13: the joint refused before the puddle; then the trail shows')
    check(a['damp'] and a['joint'] and a['turnin'] and a['entry']['found'] == 'you' and a['open'] is None, 'm13: found by you, fixed, the puddle gone')
    check(a['trained'] is not None and a['uses'] == 1, 'm13: trained on the first')
    if a['xp'][1]: check(a['xp'][0] == 1, f"m13: a leak found by you pays +1 reputation in all (the page; {a['xp'][0]})")
    else: print(f"  m13: (the leak's +1 not checked: 24 core's side-job turn-in not in this build; paid {a['xp'][0]} here)")
    print('  m13 worn:', a['worn'], 'held', a['held'], 'crew', a['crew'], 'galleries', a['gal0'], '->', a['gal3'], 'stage', a['stage'])
    check(a['worn'] and a['worn'][0] == 'joint' and a['worn'][1] and a['worn'][2] == 'seal' and a['worn'][3] == 0 and a['worn'][4], 'm13: a worn joint posts its replacement, held for you, no rep of its own')
    check(a['held'] == 1440 + 600, f"m13: held till 10:00 the next day ({a['held']})")
    check(a['crew'][0] == 'done' and a['crew'][1] and a['crew'][2] and a['crew'][3] is None, 'm13: not taken, the crew fix it the next day')
    check(a['gal0'] == 0 and a['gal3'] > 0 and a['stage'] == 1, 'm13: the galleries only after 3 leaks')
    check(len(json.loads(a['save'])) == 1 and json.loads(a['saveJunk']) == [], 'm13: junk in the save dropped')
    check(json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True), 'm13: differs the second time')
    fx = g.ev(M13_FX)
    if fx: check(fx['on'][:3] == [True, True, True] and fx['off'] == [False, False], f'm13: the puddle and the damp only while open ({fx})')
    else: print('  m13: (the look not checked: not on Decks 3-5)')
PARTS['m13'] = part_m13

# ---- M14 irrigation (24r, seat E2): on the first harvest morning from Day 13 the job goes up when the crew start picking;
# 2-4 clogged nozzles over the racks (a hold each rack); the first trains the row; cleared ones make the next harvest's
# bonus (all cleared: 0.1; none: 0, never lower); section 16's harvest reads it; left alone the job goes at midnight;
# flushing from 2 harvests, the plant's look from 4; junk in the save cleaned; the same twice
M14_STAND = r"""(() => { const out = [];
  if (typeof worksSide !== 'function') { window.worksSide = () => SHIP.works ? (SHIP.works.side = SHIP.works.side || {}) : null; out.push('worksSide'); }
  if (!(DECKS[3].growRacks || []).length) { out.push('growRacks'); DECKS[3].growRacks = DECKS[3].places.filter(p => /garden|plot|tend/.test(p.id)).slice(0, 3).map(p => ({ place: p.id, rack: p.at.slice() })); }
  return out; })()"""
M14 = r"""(() => { const out = {}, W0 = JSON.stringify(SHIP.works);
 const reset = t => { machinesNew(); SHIP.jobs = []; MACH_HOUR = null; MACH_SEEN = -1; setShipNow(t); machinesNow(); SHIP.works = null; const W = worksInit(t); W.tier = 2; W.rank = 'officer'; W.tr.t2 = 10; (W.op[13] = W.op[13] || []).push('m14'); delete worksSide().nozOk; worksSide().nozzles = null; return W; };
 const tick = (a, b) => { for (let t = a; t <= b; t += 10) { setShipNow(t); machinesNow(); for (const f of WORK_TICKS) f(t, false); } };
 let d = 13; while (!gardenHarvestDay(d)) d++; let d2 = d + 1; while (!gardenHarvestDay(d2)) d2++;
 out.days = [d, d2, weekday(d)];
 let W = reset((d - 1) * 1440 + 300); tick((d - 1) * 1440 + 360, (d - 1) * 1440 + 660);
 let j = SHIP.jobs.find(x => x.kind === 'nozzle'); out.posted = j ? [Math.round(j.posted % 1440), j.title, j.clogged.length, jobStops(j).map(s => s.step + ':' + s.how + ':' + (s.places[0] || '-'))] : null; if (!j) return out;
 out.claimed = claimJob(j.id); jobStops(j).forEach((s, k) => jobStepDone(j.id, k, {})); out.turnin = turnInJob(j.id);
 let N = worksSide().nozzles; out.after = [N.cleared.length, N.clogged.length, N.harvests, W.tr.m14 !== undefined, W.use.m14];
 W.use.m14 = 2;                                         // the stage rose since (R4's fix 1): no flush was offered, so no penalty
 tick((d - 1) * 1440 + 670, (d2 - 1) * 1440 + 660); N = worksSide().nozzles;
 out.bonus = [irrigationBonus(d2), irrigationBonus(d2 + 1), N.day === d2];
 const j2 = SHIP.jobs.find(x => x.kind === 'nozzle' && worksDay(x.posted) === d2); tick((d2 - 1) * 1440 + 670, d2 * 1440 + 20);
 out.lapsed = j2 ? [j2.status, j2.doneBy] : null;
 let d3 = d2 + 1; while (!gardenHarvestDay(d3)) d3++; nozPost((d3 - 1) * 1440 + 600); out.none = irrigationBonus(d3);
 out.hook = [...document.scripts].some(s => s.textContent.includes("typeof irrigationBonus === 'function' ? 1 + irrigationBonus(d) : 1"));
 W.use.m14 = 2; out.st1 = nozStops({ clogged: ['0.1'], stage: worksStage('m14') }).map(s => s.step || s.tag);
 W.use.m14 = 4; out.st2 = nozStops({ clogged: ['0.1'], stage: worksStage('m14') }).map(s => s.tag);
 out.clog = [13, 14, 15, 16, 17, 18].map(x => nozClogged(x).length);
 worksSide().nozzles = { day: 'x', clogged: ['0.1', 7, '9.99', '1.2'], cleared: 'no', harvests: -3, bonus: 5 }; delete worksSide().nozOk;
 out.save = JSON.stringify(nozState());
 SHIP.works = JSON.parse(W0); return out; })()"""
def part_m14(g):
    check(g.ev(ROW_AGREE)['m14'], 'm14: the ladder row (24 core) and 24r disagree (day, stages, by)')
    st = g.ev(M14_STAND)
    if st: print('  m14 stand-ins:', st)
    a, b = g.ev(M14), g.ev(M14)
    if not a.get('after'): fail(f'm14: no job ({a})'); return
    print('  m14 harvests', a['days'], 'posted', a['posted'], 'after', a['after'], 'bonus', a['bonus'], 'lapsed', a['lapsed'], 'none', a['none'], 'stages', a['st1'], a['st2'], 'clogged', a['clog'])
    check(a['posted'] and 540 <= a['posted'][0] < 690 and 2 <= a['posted'][2] <= 4 and all(s.split(':')[2] != '-' for s in a['posted'][3]), 'm14: the job on the harvest morning, 2-4 nozzles, every rack a place')
    check(a['claimed'] and a['turnin'] and a['after'][0] == a['after'][1] and a['after'][2] == 1 and a['after'][3] and a['after'][4] == 1, 'm14: cleared, trained, a use')
    check(abs(a['bonus'][0] - .1) < 1e-9 and a['bonus'][1] == 0 and a['bonus'][2], 'm14: the next harvest a tenth bigger, that day only')
    check(a['lapsed'] == ['done', None] and a['none'] == 0, 'm14: left alone it goes at midnight; uncleared never lowers it')
    check(a['hook'], "m14: section 16's harvest reads irrigationBonus")
    check('flush' in a['st1'] and 'plant' not in a['st1'] and 'plant' in a['st2'], 'm14: flushing from 2 harvests, the plant from 4')
    check(all(2 <= n <= 4 for n in a['clog']), 'm14: 2-4 clogged a harvest')
    s = json.loads(a['save'])
    check(s['day'] == 0 and s['clogged'] == ['0.1', '1.2'] and s['cleared'] == [] and s['harvests'] == 0 and s['bonus'] == .1, f'm14: junk in the save cleaned ({s})')
    check(json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True), 'm14: differs the second time')
PARTS['m14'] = part_m14

ROW_STAND = r"""(() => { const out = [];
  if (typeof worksSide !== 'function') { window.worksSide = () => SHIP.works ? (SHIP.works.side = SHIP.works.side || {}) : null; out.push('worksSide'); }
  if (typeof LEAK_FROM !== 'undefined' && !ladderRow('m13')) { CAREER_LADDER.push({ id: 'm13', name: 'Leak hunting', size: 'small', day: LEAK_FROM, tier: 2, rank: 'officer', needs: null, by: LEAK_BY.slice(), job: 'leak', stages: [{ uses: 0 }, { uses: LEAK_GALLERY }] }); out.push('m13'); }
  if (typeof NOZ_FROM !== 'undefined' && !ladderRow('m14')) { CAREER_LADDER.push({ id: 'm14', name: 'Garden irrigation', size: 'small', day: NOZ_FROM, tier: 2, rank: 'officer', needs: null, by: NOZ_BY.slice(), job: 'nozzle', stages: [{ uses: 0 }, { uses: 2 }, { uses: 4 }] }); out.push('m14'); }
  if (typeof REW_FROM !== 'undefined' && !ladderRow('m15')) { CAREER_LADDER.push({ id: 'm15', name: 'Rewiring', size: 'big', day: REW_FROM, tier: 2, rank: 'officer', needs: null, by: ['calder'], where: { deck: 4, room: '-' }, job: 'rewire', tool: 'tester', stages: [{ uses: 0 }, { uses: REW_FADE }] }); out.push('m15'); }
  return out; })()"""
# the rows (24 core's, E1) and E2's sub-blocks agree: a retune on either side fails here instead of drifting (R4)
ROW_AGREE = r"""(() => { const r13 = ladderRow('m13'), r14 = ladderRow('m14'), same = (a, b) => JSON.stringify(a) === JSON.stringify(b);
  return { m13: !r13 || (r13.day === LEAK_FROM && r13.tier === 2 && r13.size === 'small' && (r13.stages || [])[1] && r13.stages[1].uses === LEAK_GALLERY && same(r13.by, LEAK_BY)),
           m15: typeof REW_FROM === 'undefined' || !ladderRow('m15') || (ladderRow('m15').day === REW_FROM && ladderRow('m15').size === 'big' && ladderRow('m15').tier === 2 && (ladderRow('m15').stages || [])[1] && ladderRow('m15').stages[1].uses === REW_FADE && ladderRow('m15').by[0] === 'calder'),
           m14: !r14 || (r14.day === NOZ_FROM && r14.tier === 2 && r14.size === 'small' && same((r14.stages || []).map(x => x.uses), [0, 2, 4]) && same(r14.by, NOZ_BY)) }; })()"""
# ---- M15 rewiring (24q, seat E2): one a week from Day 17 once trained, 08:00 on a workday of yours, a junction job at Tier
# 2; open the box, a pair per wire, test: right first time puts the junction right; a wrong pair pops at the test and
# only that pair opens again (never a fail); from 3 a faded chart wants the lights flicked first; not taken, the crew's
# the next day; junk in the save cleaned; the same twice
M15 = r"""(() => { const out = {}, W0 = JSON.stringify(SHIP.works);
 const reset = t => { machinesNew(); SHIP.jobs = []; MACH_HOUR = null; MACH_SEEN = -1; setShipNow(t); machinesNow(); SHIP.works = null; const W = worksInit(t); W.tier = 2; W.rank = 'officer'; W.tr.t2 = 10; W.tr.m15 = 17; W.use.m15 = 1; delete worksSide().rewOk; worksSide().rewire = null; W.inc = { plan: {}, open: null }; return W; };
 const tick = (a, b) => { for (let t = a; t <= b; t += 10) { setShipNow(t); machinesNow(); for (const f of WORK_TICKS) f(t, false); } };
 let W = reset(20 * 1440 + 300); const seen = new Map(); for (let t = 20 * 1440 + 360; t <= 41 * 1440 + 500; t += 10) { setShipNow(t); machinesNow(); for (const f of WORK_TICKS) f(t, false); for (const x of SHIP.jobs) if (x.kind === 'rewire') seen.set(x.id, x); }
 const js = [...seen.values()]; out.weeks = js.map(x => [worksDay(x.posted), weekday(worksDay(x.posted)), Math.round(x.posted % 1440), x.machine, jobTier(x), x.chart.length, x.status]);
 const right = (j, k) => ({ pick: rewRight(j, k) });
 W = reset(22 * 1440 + 480); let j = rewJob('4-junction-1', shipNow(), { key: 99 }); SHIP.jobs.push(j); SHIP.machines['4-junction-1'].cond = 40;
 out.board = !!openJobs().find(x => x.id === j.id); out.claimed = claimJob(j.id);
 let S = jobStops(j); out.stops = S.map(s => s.step + ':' + s.how); out.ordered = [90, 91, 92, 93, 94, 95].some(k => { const x = rewChart(k, 0).order; return x.some((v, i) => v !== i); });
 out.early = jobStepDone(j.id, 1, right(j, 1)).ok;
 jobStepDone(j.id, 0, {}); S.forEach((s, k) => { if (s.step === 'wire') jobStepDone(j.id, k, right(j, k)); });
 out.test = jobStepDone(j.id, S.length - 1, {}).ok; const xp0 = W.xp; out.turnin = turnInJob(j.id); out.xp = [W.xp - xp0, typeof WORKS_SIDE_KINDS !== 'undefined']; out.right = [j.rightFirst, j.wrongs, SHIP.machines['4-junction-1'].cond >= 90, worksSide().rewire.done];
 // a wrong pair: the fuse pops, only that pair opens again
 j = rewJob('4-junction-2', shipNow(), { key: 98 }); SHIP.jobs.push(j); claimJob(j.id); S = jobStops(j); jobStepDone(j.id, 0, {});
 S.forEach((s, k) => { if (s.step === 'wire') jobStepDone(j.id, k, k === 2 ? { pick: rewRight(j, 2) === 'T1' ? 'T2' : 'T1' } : right(j, k)); });
 out.pop = jobStepDone(j.id, S.length - 1, {}).ok; out.open = S.map((s, k) => (j.stepsDone || []).includes(k) ? 1 : 0); out.wrongs = j.wrongs;
 jobStepDone(j.id, 2, right(j, 2)); out.retest = jobStepDone(j.id, S.length - 1, {}).ok; out.turnin2 = turnInJob(j.id); out.after = [j.rightFirst, worksSide().rewire.wrongs];
 // stage 1: a faded chart, the lights first
 W.use.m15 = 3; j = rewJob('4-junction-1', shipNow(), { key: 97, stage: worksStage('m15') }); SHIP.jobs.push(j); claimJob(j.id); S = jobStops(j); jobStepDone(j.id, 0, {});
 out.faded = [j.faded.length, S[1].step, jobStepDone(j.id, 2, right(j, 2)).ok, jobStepDone(j.id, 1, {}).ok, jobStepDone(j.id, 2, right(j, 2)).ok];
 // not taken: the crew's the next day
 W = reset(22 * 1440 + 480); j = rewJob('4-junction-1', shipNow(), { key: 96 }); SHIP.jobs.push(j); out.held = leaveEnd(j) - 22 * 1440;
 tick(22 * 1440 + 490, 23 * 1440 + 900); out.crew = [j.status, j.doneBy !== 'you' && !!j.doneBy];
 worksSide().rewire = { done: 'x', wrongs: -4 }; delete worksSide().rewOk; out.save = JSON.stringify(rewState()); worksSide().rewire = { done: 3, wrongs: 1, week: 4 }; delete worksSide().rewOk; out.save2 = JSON.stringify(rewState());
 SHIP.works = JSON.parse(W0); return out; })()"""
def part_m15(g):
    check(g.ev(ROW_AGREE)['m15'], 'm15: the ladder row (24 core) and 24q disagree (day, stages, by)')
    a, b = g.ev(M15), g.ev(M15)
    print('  m15 weeks:', a['weeks'])
    print('  m15 stops', a['stops'], 'right', a['right'], 'pop', a['pop'], a['open'], 'wrongs', a['wrongs'], 'after', a['after'], 'faded', a['faded'], 'held', a['held'], 'crew', a['crew'])
    check(3 <= len(a['weeks']) <= 4 and all(e[1] <= 4 and e[2] == 480 and e[4] == 2 and 4 <= e[5] <= 6 for e in a['weeks']), 'm15: one a week, 08:00 on a weekday, Tier 2, 4-6 wires')
    check(a['board'] and a['claimed'] and not a['early'], 'm15: offered to an Officer; the box opened first')
    check(a['test'] and a['turnin'] and a['right'][0] is True and a['right'][1] == 0 and a['right'][2] and a['right'][3] == 1, 'm15: right first time, the junction put right')
    check(not a['pop'] and a['wrongs'] == 1 and a['open'][2] == 0 and sum(a['open']) == len(a['open']) - 2, 'm15: a wrong pair pops at the test, only that pair opens again')
    if a['xp'][1]: check(a['xp'][0] == 2, f"m15: right first time pays +1, +1 more (the page; {a['xp'][0]})")
    else: print(f"  m15: (the pay not checked: 24 core's side-job turn-in not in this build; paid {a['xp'][0]} here)")
    check(a['retest'] and a['turnin2'] and a['after'][0] is False and a['after'][1] == 1, 'm15: redone, finished, not right first time (never a fail)')
    check(a['faded'] == [1, 'check', False, True, True], 'm15: a faded chart from 3 (one colour): the lights first')
    check(a.get('ordered'), 'm15: the wires come in a seeded order, not the chart\'s (the chart must be read)')
    check(a['held'] == 1440 + 600 and a['crew'] == ['done', True], 'm15: not taken, the crew\'s the next day')
    check(json.loads(a['save']) == {'done': 0, 'wrongs': 0, 'week': -1} and json.loads(a['save2']) == {'done': 3, 'wrongs': 1, 'week': 4}, 'm15: the save read back, junk cleaned')
    check(json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True), 'm15: differs the second time')
PARTS['m15'] = part_m15

# ---- favour cases (24l, seat E2 on H's behalf; not a ladder row, so it runs after the rows as EXTRA['fcase']): every
# script has three clue places and its answer (sus.1) among the options; a friend asks (Mail, an offered favour) on the
# week's evening; accepted, the side job: the clues before the call, a wrong pick refused (never a fail), the right one
# gives the fix its place; fixed and handed back, done; another not taken lapses in 3 days, no harm; the same twice
EXTRA = {}
FC = r"""(() => { const out = {}, W0 = JSON.stringify(SHIP.works), R0 = JSON.stringify(SHIP.rel || {});
 const reset = t => { machinesNew(); SHIP.jobs = []; SHIP.mail = []; MACH_HOUR = null; MACH_SEEN = -1; setShipNow(t); machinesNow(); SHIP.works = null; const W = worksInit(t); W.tier = 2; W.rank = 'officer'; W.tr.t2 = 10; delete worksSide().fcOk; worksSide().favours = []; W.inc = { plan: {}, open: null }; return W; };
 const tick = (a, b) => { for (let t = a; t <= b; t += 10) { setShipNow(t); machinesNow(); for (const f of WORK_TICKS) f(t, false); } };
 out.scripts = FC_IDS.map(c => { const j = { fcase: c, bed: schedPeople().find(p => p.bed && placeById(p.bed)).bed, order: [3, 1, 2], from: 'calder' }, S = fcStops(j);
   return [c, S.length, S.slice(0, 3).every(x => x.how === 'look' && placeById(x.placeId)), S[3].how, S[3].opts.options.map(o => o.id).includes('sus1')]; });
 const friends = schedPeople().filter(p => p.bed && placeById(p.bed)).sort((a, b) => (a.id < b.id ? -1 : 1)).slice(0, 6);
 for (const p of friends) { const r = relGet(p.id); r.pts = Math.max(r.pts, REL_TIERS[FC_TIER]); r.tier = Math.max(r.tier, FC_TIER); }
 let W = reset(14 * 1440 + 300); const w = incWeek(15), P = fcPlan(w); out.plan = P && [P.d, P.at];
 tick(14 * 1440 + 360, (P.d - 1) * 1440 + P.at + 10);
 let e = worksSide().favours[0]; out.asked = e ? [e.case, e.state, e.day, !!SHIP.mail.length] : null; if (!e) return out;
 let F = favourById(e.id); out.offered = [F.status, F.stops[0].placeId]; out.accept = favourAccept(e.id);
 tick(shipNow() + 10, shipNow() + 20); let j = SHIP.jobs.find(x => x.kind === 'fcase'); out.side = j ? [j.claimedBy, j.status, jobStops(j).map(s => s.step + ':' + s.how + ':' + (s.places[0] ? 'P' : '-'))] : null; if (!j) return out;
 out.early = jobStepDone(j.id, 3, { pick: 'sus1' }).ok;
 for (let k = 0; k < 3; k++) jobStepDone(j.id, k, {});
 out.wrong = jobStepDone(j.id, 3, { pick: 'sus2' }).ok; out.right = jobStepDone(j.id, 3, { pick: 'sus1' }).ok; out.sideDone = [j.workDone ? 1 : 0, turnInJob(j.id) || j.status];
 F = favourById(e.id); out.fixPlace = F.stops[0].placeId; out.fix = jobStepDone(e.id, 0, {}).ok; out.turnin = favourTurnIn(e.id);
 tick(shipNow() + 10, shipNow() + 20); out.state = worksSide().favours[0].state;
 // another, never taken: lapses in 3 days
 W = reset(21 * 1440 + 300); const w2 = incWeek(22), P2 = fcPlan(w2); tick(21 * 1440 + 360, (P2.d - 1) * 1440 + P2.at + 10);
 const e2 = worksSide().favours[0]; tick(shipNow() + 10, shipNow() + 4 * 1440); out.lapse = e2 ? [e2.state, (favourById(e2.id) || { status: 'gone' }).status] : null;
 worksSide().favours = [{ id: 'f1', who: 'calder', case: 'lamp', day: 15, state: 'weird' }, { id: 2 }, { id: 'f3', who: 'x', case: 'nope', day: 1 }]; delete worksSide().fcOk; out.save = JSON.stringify(fcList());
 SHIP.works = JSON.parse(W0); SHIP.rel = JSON.parse(R0); return out; })()"""
def extra_fcase(g):
    a, b = g.ev(FC), g.ev(FC)
    print('  fcase scripts', a['scripts'])
    print('  fcase plan', a['plan'], 'asked', a.get('asked'), 'offered', a.get('offered'), 'side', a.get('side'), 'early', a.get('early'), 'wrong', a.get('wrong'), 'right', a.get('right'), a.get('sideDone'), 'fix', a.get('fixPlace'), a.get('fix'), a.get('turnin'), a.get('state'), 'lapse', a.get('lapse'))
    check(all(x[1] == 4 and x[2] and x[3] == 'choose' and x[4] for x in a['scripts']), 'fcase: every script: three clue places, the answer among the options')
    if not check(a.get('asked') and a['asked'][1] == 'asked' and a['asked'][3], 'fcase: a friend asks on the week\'s evening (Mail, an offered favour)'): return
    check(a['offered'][0] == 'offered' and a['offered'][1] is None and a['accept'], 'fcase: offered; the fix has no place yet')
    check(a['side'] and a['side'][0] == 'you' and a['side'][2][:3] == ['clue:look:P'] * 3, 'fcase: accepted, the side job with three clue places')
    check(not a['early'] and not a['wrong'] and a['right'], 'fcase: the call after the clues; a wrong pick refused, the right one taken')
    check(a['fixPlace'] and a['fix'] and a['turnin'] and a['state'] == 'done', 'fcase: the fix gets its place; fixed, handed back, done')
    check(a['lapse'] and a['lapse'][0] == 'lapsed', 'fcase: not taken in 3 days, it lapses')
    s = json.loads(a['save'])
    check(len(s) == 1 and s[0]['state'] == 'asked', 'fcase: junk in the save cleaned')
    check(json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True), 'fcase: differs the second time')
EXTRA['fcase'] = extra_fcase

# ---- fault-finder tickets (24l, seat E2): Calder's Mail on Day 13; a ticket at 08:00 on a workday (a Tier 2 machine's
# fault, held in slot 23, a T2 case); solved right first time: grade 1 (W.ms ff1); a wrong call: "Not yet. Next week."
# (the next a week on, the job a plain repair); junk in the save cleaned; the same twice
FF = r"""(() => { const out = {}, W0 = JSON.stringify(SHIP.works);
 const reset = t => { machinesNew(); SHIP.jobs = []; SHIP.mail = []; MACH_HOUR = null; MACH_SEEN = -1; setShipNow(t); machinesNow(); SHIP.works = null; const W = worksInit(t); W.tier = 2; W.rank = 'officer'; W.tr.t2 = 10;
   for (const r of CAREER_LADDER) if (r.tier === 1 || ['p1', 'p2', 'm9'].includes(r.id)) { W.tr[r.id] = 5; (W.op[5] = W.op[5] || []).push(r.id); }
   delete worksSide().ffOk; worksSide().ff = null; W.inc = { plan: {}, open: null }; W.cases = { open: [], done: [], n: 0 }; return W; };
 const tick = (a, b) => { for (let t = a; t <= b; t += 10) { setShipNow(t); machinesNow(); for (const f of WORK_TICKS) f(t, false); } };
 const solve = (j, right) => { const c = caseState().open.find(x => x.job === j.id); if (!c) return 'nocase';
   if (c.wait) { c.wait = false; caseShow(c, j); } claimJob(j.id); caseCall(c.id, right ? c.cause : c.sus.find(x => x !== c.cause));
   jobStops(j).forEach((s, k) => jobStepDone(j.id, k)); return [c.band, c.kind, !!c.ticket, turnInJob(j.id)]; };
 const rigN = () => { let m = 0, v = 0; player.rig.root.traverse(o => { if (o.isMesh) { m++; v += o.geometry.attributes.position.count; } }); return [m, v]; };
 delete PLAYER_SPEC.pin; delete player.spec.pin; playerRigRebuild(); out.rig0 = rigN();
 let W = reset(12 * 1440 + 300); out.kinds = caseKindsOpen();
 tick(12 * 1440 + 480, 12 * 1440 + 500); out.mail = [SHIP.mail.filter(x => /Calder/.test(x.from || '')).length, worksSide().ff.mail];
 tick(14 * 1440 + 470, 14 * 1440 + 490); let j = SHIP.jobs.find(x => x.ticket);
 out.posted = j ? [worksDay(j.posted), Math.round(j.posted % 1440), j.reserved, jobTier(j), j.title] : null; if (!j) return out;
 out.solved = solve(j, true); tick(shipNow() + 10, shipNow() + 20);
 out.grade = [worksSide().ff.grade, W.ms.find(x => x[0] === 'ff1') || null];
 out.pin = [PLAYER_SPEC.pin || 0, player.spec.pin || 0, !!player.rig.root.parent, rigN()]; delete PLAYER_SPEC.pin; delete player.spec.pin; playerRigRebuild();   // the pin on, then off
 for (const f of WORK_TICKS) f(shipNow(), false); out.pinBack = [PLAYER_SPEC.pin || 0, rigN()];   // a reload: back on from the grade (24l's tick)
 tick(15 * 1440 + 470, 15 * 1440 + 490); out.after = SHIP.jobs.filter(x => x.ticket && worksDay(x.posted) === 16).length;
 W = reset(14 * 1440 + 300); tick(14 * 1440 + 470, 14 * 1440 + 490); j = SHIP.jobs.find(x => x.ticket);
 out.wrong = j ? solve(j, false) : null; tick(shipNow() + 10, shipNow() + 20);
 out.wrongAfter = [worksSide().ff.grade, worksSide().ff.tries, worksSide().ff.next, worksSide().ff.job];
 tick(15 * 1440 + 470, 15 * 1440 + 490); out.notYet = SHIP.jobs.filter(x => x.ticket && worksDay(x.posted) === 16).length;
 worksSide().ff = { grade: 9, tries: 'x', next: 22, job: 5 }; delete worksSide().ffOk; out.save = JSON.stringify(ffState());
 SHIP.works = JSON.parse(W0); delete PLAYER_SPEC.pin; delete player.spec.pin; playerRigRebuild(); out.rig1 = rigN(); return out; })()"""
def extra_ff(g):
    a, b = g.ev(FF), g.ev(FF)
    print('  ff kinds', a['kinds'], 'mail', a['mail'], 'posted', a.get('posted'), 'solved', a.get('solved'), 'grade', a.get('grade'), 'after', a.get('after'), 'wrong', a.get('wrong'), a.get('wrongAfter'), 'notYet', a.get('notYet'))
    check(a['mail'] == [1, 1], "ff: Calder's Mail on Day 13")
    if not check(a.get('posted') and a['posted'][0] == 15 and a['posted'][1] == 480 and a['posted'][2] == 23 and a['posted'][3] == 2, 'ff: a ticket at 08:00 on the next workday, Tier 2, held in slot 23'): return
    check(a['solved'][0] == 'T2' and a['solved'][2] and a['solved'][3], 'ff: a T2 case, solved and turned in')
    check(a['grade'][0] == 1 and a['grade'][1], 'ff: right first time: grade 1, the Record\'s ff1')
    check(a['after'] == 0, 'ff: no more tickets once graded (grades 2-3 are later steps)')
    print('  ff pin: rig before', a['rig0'], 'graded', a['pin'], 'after a reload', a['pinBack'], 'cleared', a['rig1'])
    check(a['pin'][:3] == [1, 1, True], f"ff: the pin on your uniform ({a.get('pin')})")
    check(a['pin'][3][0] == a['rig0'][0] and a['pin'][3][1] > a['rig0'][1], 'ff: the pin merged into the chest (no extra mesh, so no extra draw call)')
    check(a['pinBack'][0] == 1 and a['pinBack'][1] == a['pin'][3], 'ff: the pin back on after a reload (the grade)')
    check(a['rig1'] == a['rig0'], 'ff: no grade, no pin')
    check(a['wrongAfter'][0] == 0 and a['wrongAfter'][1] == 1 and a['wrongAfter'][2] == 22 and a['wrongAfter'][3] is None and a['notYet'] == 0, 'ff: a wrong call: not yet, the next a week on')
    check(json.loads(a['save']) == {'grade': 3, 'tries': 0, 'next': 22, 'job': None, 'mail': 0}, f"ff: the save cleaned ({a['save']})")
    check(json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True), 'ff: differs the second time')
EXTRA['ff'] = extra_ff

# ---- M8 stage 2, team parts (24h, seat E5 for M2; step4-stages): from Day 18 after two team jobs, the team job's Mail
# asks you to bring the parts (24d's manifestRun, E1: held for you till the start); brought: on time, side.parts + 1;
# not brought: the run withdrawn, the lead fetches them, 10 minutes late, never a fail; before stage 2 or Day 18 the
# old Mail and no run; the same twice
TPARTS = r"""(() => { const out = {}, W0 = JSON.stringify(SHIP.works);
 // the Works first, then the machines' catch-up: it runs the jobs hour by hour, and read the last run's (or the fresh game's) Works before (X3: the first run picked another team job)
 const reset = (t, uses) => { setShipNow(t); SHIP.works = null; const W = worksInit(t);
   W.team = { plan: {} }; W.inc = { plan: {}, open: null }; W.tier = 2; W.rank = 'officer'; W.tr.t2 = 10; W.tr.m8 = 11; W.use.m8 = uses;
   machinesNew(); SHIP.jobs = []; SHIP.mail = []; MACH_HOUR = null; MACH_SEEN = -1; setShipNow(t); machinesNow(); if (worksSide()) worksSide().parts = 0; return W; };
 const run = (t0, t1, uses, bring, d0 = 18) => { const W = reset(t0, uses), r = {}; let j = null;
   for (let t = t0; t <= t1; t += 5) { setShipNow(t); machinesNow(); for (const f of WORK_TICKS) f(t, false);
     j = j || SHIP.jobs.find(x => x.kind === 'team' && x.claimedBy === 'you' && worksDay(x.start) >= d0); if (!j || j.status === 'done') continue;
     const R = j.partsRun && SHIP.jobs.find(x => x.id === j.partsRun);
     if (R && !r.run) r.run = [R.kind, R.reserved, R.until === j.start, (R.crates || []).map(c => c.id).join('+'), R.crates.every(c => c.dest === panelPlace(j.machine))];
     if (bring && R && !R.delivered && t >= j.start - 60 && R.status !== 'done') { claimJob(R.id); jobStops(R).forEach((s, k) => jobStepDone(R.id, k, {})); r.delivered = manifestRunDelivered(R.id); turnInJob(R.id); }
     if (t >= j.start - 5) j.youIn = true;
     const mine = j.seq.map((s, i) => s.who === 'you' ? i : -1).filter(i => i >= 0), k = mine.indexOf(j.cur);
     if (k >= 0) { if (r.first === undefined) r.first = j.stepAt - j.start; jobStepDone(j.id, k, j.seq[j.cur].how === 'turn' ? { value: 3 } : {}); for (const f of WORK_TICKS) f(t, false); } }
   const R = j && j.partsRun && SHIP.jobs.find(x => x.id === j.partsRun);
   r.job = j && { day: worksDay(j.start), status: j.status, by: j.doneBy, late: j.late, partsLate: j.partsLate === undefined ? null : j.partsLate, mins: j.doneAt - j.start, run: !!j.partsRun };
   r.left = R ? [R.status, !!R.delivered] : null; r.parts = worksSide() ? worksSide().parts || 0 : null;
   r.mail = SHIP.mail.filter(m => j && m.from === worksName(j.lead) && (m.subject === 'Bring the parts' || Object.values(TEAM_NAME).includes(m.subject))).map(m => m.subject); return r; };
 out.bring = run(16 * 1440 + 900, 18 * 1440 + 800, 2, true);
 out.not = run(16 * 1440 + 900, 18 * 1440 + 800, 2, false);
 out.stage0 = run(16 * 1440 + 900, 18 * 1440 + 800, 0, false);
 out.early = run(14 * 1440 + 900, 16 * 1440 + 800, 2, false, 0);
 worksSide().parts = 'x'; out.junk = teamPartsN(); worksSide().parts = 3; out.three = teamPartsN();
 SHIP.works = JSON.parse(W0); return out; })()"""
def extra_tparts(g):
    if not g.ev("typeof manifestRun === 'function' && !!JOB_KINDS.haul && typeof worksSide === 'function'"):
        print("  tparts: (not checked: 24d's manifestRun (E1) not in this build)"); return
    a, b = g.ev(TPARTS), g.ev(TPARTS)
    for k in ('bring', 'not', 'stage0', 'early'): print('  tparts', k, a[k])
    B, N, S, E = a['bring'], a['not'], a['stage0'], a['early']
    if not check(B['job'] and B['job']['run'] and B['job']['day'] >= 18, f"tparts: a team job from Day 18 you're in asks for the parts ({B['job']})"): return
    check(B['run'][0] == 'haul' and B['run'][2] and B['run'][4] and B['run'][3] and 'Bring the parts' in B['mail'], f"tparts: the Mail asks you; a manifest run to the machine, held till the start ({B['run']}, {B['mail']})")
    check(B['delivered'] and B['job']['partsLate'] is False and S['first'] == B['first'] and B['parts'] == 1 and B['job']['status'] == 'done', 'tparts: brought: it starts on time, side.parts 1')
    check(N['job']['partsLate'] is True and N['first'] == B['first'] + 10 and N['left'] == ['done', False] and N['parts'] == 0 and N['job']['status'] == 'done' and N['job']['mins'] == B['job']['mins'] + 10, 'tparts: not brought: the run withdrawn, the lead fetches them, 10 minutes late, never a fail')
    check(S['job'] and not S['job']['run'] and S['job']['partsLate'] is None and 'Bring the parts' not in S['mail'], 'tparts: before two team jobs, the old Mail and no run')
    check(E['job'] and E['job']['day'] < 18 and not E['job']['run'], 'tparts: none before Day 18')
    check(a['junk'] == 0 and a['three'] == 3, 'tparts: side.parts read defensively')
    check(json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True), 'tparts: differs the second time')
EXTRA['tparts'] = extra_tparts

# ---- E2's saved parts through a real save and reload (R4's fix 2): SHIP.works.side's leaks, nozzles, rewire, favours
# and ff (and 24h's team parts count), written by saveGame (saving on) and read back by the sub-blocks after a reload; needs 24 core's worksClean to
# keep `side` (E1), else it says so
SIDE_SET = r"""(() => { if (typeof worksSide !== 'function') window.worksSide = () => SHIP.works ? (SHIP.works.side = SHIP.works.side || {}) : null;
  setShipNow(12 * 1440 + 600); machinesNow(); const W = worksInit(); W.tier = 2; W.rank = 'officer';
  const S = worksSide(); S.leaks = [{ id: 'leak:4-leak-1@300', joint: '4-leak-1', room: 'k', deck: 4, day: 12, worn: 1, found: 'you' }];
  S.nozzles = { day: 20, clogged: ['0.1', '2.3'], cleared: ['0.1'], flushed: 1, harvests: 2, stage: 1, bonus: .05, told: 20 };
  S.rewire = { done: 2, wrongs: 1, week: 3 }; S.favours = [{ id: 'favour:cruz-tove@1', who: 'cruz-tove', case: 'lamp', day: 15, state: 'done' }]; S.ff = { grade: 1, tries: 1, next: 22, job: null, mail: 1 }; S.parts = 2;
  for (const k of ['leaksOk', 'nozOk', 'rewOk', 'fcOk', 'ffOk']) delete S[k];
  SHIP.jobs = []; const rj = rewJob('4-junction-1', shipNow(), { key: 99 }); SHIP.jobs.push(rj); claimJob(rj.id); jobStepDone(rj.id, 0, {});
  jobStops(rj).forEach((x, k) => { if (x.step === 'wire') jobStepDone(rj.id, k, { pick: k === 1 ? (rewRight(rj, 1) === 'T1' ? 'T2' : 'T1') : rewRight(rj, k) }); }); jobStepDone(rj.id, jobStops(rj).length - 1, {});   // a wrong pair popped
  const P = schedPeople().find(p => p.bed && placeById(p.bed)), fid = favourPost({ from: P.id, title: 'x', stops: [{ deck: placeById(P.bed).deck, placeId: null, mins: 10, tag: 'fcase' }] }), F = favourById(fid); F.fcase = 'lamp'; favourAccept(fid);
  const fj = jobMake('fcase', { id: 'fcase:' + fid, deck: placeById(P.bed).deck, h: 300, title: 'x', fcase: 'lamp', favour: fid, from: P.id, bed: P.bed, order: [2, 3, 1] }); fj.claimedBy = 'you'; fj.status = 'claimed'; SHIP.jobs.push(fj); jobStepDone(fj.id, 0, {});
  S.favours.push({ id: fid, who: P.id, case: 'lamp', day: 13, state: 'taken' });
  window.__ids = [rj.id, fid, fj.id];
  const read = () => { const r = SHIP.jobs.find(x => x.kind === 'rewire'), f = SHIP.jobs.find(x => x.kind === 'favour'), q = SHIP.jobs.find(x => x.kind === 'fcase');
    return JSON.stringify([leakList(), nozState(), rewState(), fcList(), ffState(), r && [r.pairs, r.wrongs, r.stepsDone, r.order, r.chart, r.claimedBy], f && [f.fcase, f.status, f.claimedBy], q && [q.fcase, q.order, q.stepsDone, q.claimedBy, q.favour], typeof teamPartsN === 'function' ? teamPartsN() : null]); };
  window.__read = read; const before = read(); saveGame();
  return { before, keeps: JSON.stringify(worksClean({ v: 1, side: { a: 1 } }) || {}).includes('side') }; })()"""
SIDE_GET = r"""(() => { if (typeof worksSide !== 'function') window.worksSide = () => SHIP.works ? (SHIP.works.side = SHIP.works.side || {}) : null;
  const r = SHIP.jobs.find(x => x.kind === 'rewire'), f = SHIP.jobs.find(x => x.kind === 'favour'), q = SHIP.jobs.find(x => x.kind === 'fcase');
  return SHIP.works ? JSON.stringify([leakList(), nozState(), rewState(), fcList(), ffState(), r && [r.pairs, r.wrongs, r.stepsDone, r.order, r.chart, r.claimedBy], f && [f.fcase, f.status, f.claimedBy], q && [q.fcase, q.order, q.stepsDone, q.claimedBy, q.favour], typeof teamPartsN === 'function' ? teamPartsN() : null]) : null; })()"""
def side_save(pw):
    tmp = WORK / 'test' / '_mech_save.html'
    tmp.write_text(instrument(pathlib.Path(sys.argv[1]).read_text()))
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    page = b.new_page(viewport={'width': 600, 'height': 500})
    page.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
    page.add_init_script(INIT)
    def load():
        page.goto('file://' + str(tmp)); page.wait_for_function('window.__sc !== undefined', timeout=60000)
        return lambda s: page.evaluate('s => window.__sc(s)', s)
    ev2 = load(); ev2("localStorage.clear()"); ev2 = load()
    a = ev2(SIDE_SET); ev2 = load(); after = ev2(SIDE_GET)
    b.close()
    print('  side save: before', a['before'][:160], '... after', (after or '')[:160])
    A, B = json.loads(a['before']), json.loads(after or 'null') or [None] * 8
    check(A[5:8] == B[5:8] and A[5] and A[7], 'side save: a rewire job after a wrong pair, an accepted favour and its side job through a real save and reload')
    if not a['keeps']: print("  side save: (24 core's worksClean doesn't keep `side` in this build: E1's; side not checked)"); return
    if after != a['before']:
        for x, y in zip(json.loads(a['before']), json.loads(after or '[]')):
            if x != y: print('   differs:', x, '|', y)
    check(after == a['before'], 'side save: leaks, nozzles, rewire, favours and ff through a real save and reload')
# 24j the workshop (seat E3, M10): on paper. Day 12, an Officer who knows three crew: one order goes up at 08:00 (from
# one of them); you take it (your side job: a wait, then a hold, at the lathe or the fabricator); made, it's handed over
# (a thank-you, a friendship step, a use, reputation once a day). Monday's orders: one left a week lapses with a Mail.
# Stage 2 (3 made): an order with a part starts at the shelves. Tinkering's things are gifts. The same twice.
M10 = r"""(() => {
  SHIP.works = null; SHIP.occasions.length = 0; SHIP.notes = []; SHIP.flags = {}; SHIP.jobs = []; SHIP.mail = [];
  MACH_HOUR = null; MACH_SEEN = -1; WORKS_TICK.m = WORKS_TICK.h = -1; socInit(); SHIP.rel = {};
  const run = (from, to) => { for (let m = from; m <= to; m += 10) { setShipNow(m); machinesNow(); worksCareerTick(m); } };
  setShipNow(11 * 1440 + 300); machinesNow(); const W = worksInit(); W.tier = 2; W.rank = 'officer';
  const know = SOC.crew.filter(p => !p.player).map(p => p.id).sort().slice(0, 3); for (const id of know) relAdd(id, 'chat', 15);
  const out = { side: typeof worksSide === 'function', know };
  if (!out.side) return out;
  run(11 * 1440 + 300, 11 * 1440 + 470); const s0 = worksSide().shop; out.before = s0 ? s0.orders.length : 0;
  run(11 * 1440 + 480, 11 * 1440 + 500); const s = worksSide().shop;
  out.posted = s.orders.map(o => [o.who, o.what, o.day, o.state]);
  const o = s.orders[0]; if (!o) return out;
  out.fromKnown = know.includes(o.who);
  out.take = shopTake(o); const j = SHIP.jobs.find(x => x.id === o.job);
  out.job = j ? [j.kind, j.claimedBy, j.status, jobSide(j), !myJob()] : null;
  out.stops = j ? jobStops(j).map(x => [x.step, x.how, x.places[0] || null, x.mins]) : null;
  const xp0 = W.xp; out.btn0 = shopGiveButton(socP(o.who));
  jobStops(j).forEach((x, k) => jobStepDone(j.id, k)); if (j.status === 'claimed') jobFinish(j, shipNow(), 'you');
  run(11 * 1440 + 510, 11 * 1440 + 520);
  out.made = o.state; out.btnNoHands = shopGiveButton(socP(o.who)); const keep = SHIP.player.carry.slice(); SHIP.player.carry = [shopThing(o)];
  out.btn = shopGiveButton(socP(o.who)); const r0 = SHIP.rel[o.who].pts;
  out.thanks = shopGiveSay(socP(o.who)); out.after = [o.state, s.made, Math.round((SHIP.rel[o.who].pts - r0) * 10) / 10 > 0, W.use.m10 || 0, W.xp - xp0];
  out.btnAfter = shopGiveButton(socP(o.who)); out.handsAfter = SHIP.player.carry.length; SHIP.player.carry = keep;
  run(11 * 1440 + 530, 14 * 1440 + 500);                   // Monday, Day 15: one or two up
  out.monday = s.orders.filter(x => x.day === 15).map(x => [x.who, x.what]);
  const mail0 = SHIP.mail.length; run(14 * 1440 + 510, 21 * 1440 + 490);
  out.lapsed = s.orders.filter(x => x.day === 15).map(x => x.state); out.mails = SHIP.mail.filter(m => s.orders.some(x => x.day === 15 && m.subject === 'The ' + shopThing(x))).length;
  s.made = 3; const op = WORKSHOP_ORDERS.find(x => x.part); s.orders.push({ id: 'oT-0', who: know[1], what: op.id, day: 22, state: 'posted' });
  const o2 = s.orders[s.orders.length - 1]; shopTake(o2); const j2 = SHIP.jobs.find(x => x.id === o2.job);
  out.stage2 = [shopStage(s), j2 ? jobStops(j2).map(x => x.step) : null, o2.part || null];
  if (j2) { const had = SHIP.stores[o2.part]; SHIP.stores[o2.part] = 0; shopFetch(j2, { t: 'Shelf' }, null); SHIP.stores[o2.part] = had; out.emptyShelf = jobStops(j2).map(x => [x.step, x.done]); }   // R4: an empty shelf ticks the fetch, not the lathe's wait
  out.gifts = TINKER_LIST.map(t => !!giftOf(t.item)); out.tinker = TINKER_LIST.filter(t => !t.stage || shopStage({ made: 6 }) >= t.stage).length;
  // an old save: no side.shop at all loads as empty; a junk one is cleaned
  worksSide().shop = { orders: [{ id: 1 }, { id: 'x', who: 'y', what: 'nope', state: 'posted' }], made: -4, tinkered: 'z' }; const c = shopData();
  out.clean = [c.orders.length, c.made, Array.isArray(c.tinkered)]; delete worksSide().shop; out.empty = shopData().orders.length;
  return out;
})()"""
def part_m10(g):
    a = g.ev(M10)
    if not a.get('side'):
        print('  m10: 24 core\'s worksSide is not in this build: skipped'); return
    b = g.ev(M10)
    print('  m10 posted:', a['posted'], 'job:', a['job'], 'stops:', a['stops'])
    print('  m10 hand over:', a['btn'], a['thanks'], a['after'], '| Monday:', a['monday'], a['lapsed'], 'mails', a['mails'])
    print('  m10 stage 2:', a['stage2'], 'tinker:', a['tinker'], a['gifts'], 'clean:', a['clean'], a['empty'])
    check(a['before'] == 0 and len(a['posted']) == 1 and a['posted'][0][2] == 12 and a['fromKnown'], 'm10: one order at 08:00 on Day 12, from someone who knows you')
    check(a['take'] and a['job'] and a['job'][0] == 'shop' and a['job'][1] == 'you' and a['job'][3] and a['job'][4], 'm10: taken, it\'s your side job, not your board job')
    check(a['stops'] and [x[1] for x in a['stops']] == ['wait', 'hold'] and a['stops'][0][2] in ('5-shop-lathe', '5-shop-fab'), f"m10: a wait then a hold at the machine ({a['stops']})")
    check(a['btn0'] is None and a['made'] == 'made' and a['btnNoHands'] is None and a['btn'] and a['btn']['id'] == 'shop-give', 'm10: Give appears once it\'s made and in your hands')
    check(a.get('handsAfter') == 0, 'm10: handing it over takes it from your hands')
    check(a.get('emptyShelf') == [['fetch', True], ['make', False], ['finish', False]], f"m10: an empty shelf ticks the fetch only ({a.get('emptyShelf')})")
    check(a['after'][0] == 'given' and a['after'][1] == 1 and a['after'][2] and a['after'][3] == 1 and a['after'][4] in (1, 0) and a['btnAfter'] is None, f"m10: handed over: a friendship step, a use ({a['after']})")
    check(1 <= len(a['monday']) <= 2 and all(x == 'lapsed' for x in a['lapsed']) and a['mails'] == len(a['lapsed']), 'm10: Monday\'s orders, a week untaken, lapse with a Mail')
    check(a['stage2'][0] == 2 and a['stage2'][1][0] == 'fetch' and a['stage2'][2], 'm10: stage 2: a part from main storage first')
    check(all(a['gifts']) and a['tinker'] == 6, 'm10: tinkering\'s things are gifts; stage 3 adds two')
    check(a['clean'] == [0, 0, True] and a['empty'] == 0, 'm10: an odd or missing save part loads as empty')
    check(json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True), 'm10: differs the second time')
PARTS['m10'] = part_m10

# 24t off shift (seat E3, not a ladder row: run when its functions are in the build): cabin 4-23's spots take things that
# fit from your hands and give them back; two touches give the waking bonus; an odd save part is cleaned. Star logging: one
# a night from Day 6, 20:00-23:30; three points, the new one by keys 1024-1025; every third log a friendship step with Survey;
# ten give the Record's 'stars'. The same twice.
T24 = r"""(() => {
  SHIP.works = null; SHIP.jobs = []; SHIP.rel = {}; setShipNow(12 * 1440 + 600); machinesNow(); const W = worksInit(); W.tier = 2; W.rank = 'officer'; W.home = '4-23';
  const P = SHIP.player, out = {}, keep = P.carry.slice();
  P.carry = ['little lamp', 'toy rocket']; const tap = k => cabinTap({ t: k, cabin: k }, null);
  out.tap = [tap('rug'), P.carry.length, tap('desk'), tap('shelf'), P.carry.length, cabinTouches(), cabinMood(), cabinPlaced('toy rocket')];
  P.carry = ['plant pot']; tap('ledge'); out.four = cabinTouches(); tap('desk'); out.back = [P.carry.slice(), cabinTouches()];
  worksSide().cabin = { rug: 'banana', desk: 'little lamp', shelf: 7, nope: 'x' }; out.clean = JSON.stringify(cabinData());
  W.home = 'bunk'; out.notMine = [cabinMine(), cabinMood()]; W.home = '4-23';
  const s = starsData(); s.n = 0; s.last = 0; out.sky = [12, 13, 14].map(d => JSON.stringify(starSky(d)));
  out.sato0 = relGet('sato').pts; for (let n = 0; n < 10; n++) { s.n++; if (s.n % 3 === 0) relAdd(['sato', 'mori'][(s.n / 3 - 1) % 2], 'help', 6); }
  out.friends = [relGet('sato').pts > out.sato0, relGet('mori').pts > 0];
  P.carry = keep; return out;
})()"""
T24B = r"""(() => {
  SHIP.works = null; SHIP.jobs = []; SHIP.rel = {}; setShipNow(11 * 1440 + 1230); machinesNow(); const W = worksInit(); W.tier = 2; W.rank = 'officer'; W.home = '4-23'; W.ms = [];
  const out = {}, s = starsData(); s.n = 0; s.last = 0;
  goToDeck(2); const it = ITEMS.find(x => /telescope/i.test(x.t) && x.hit && (() => { const p = new THREE.Vector3(); x.hit.getWorldPosition(p); return roomAt(...cellAt(p.x, p.z)) === 'J'; })());
  const at = new THREE.Vector3(); if (it) it.hit.getWorldPosition(at);
  const tapAt = t => { setShipNow(t); const r = starTap(it, at.clone()); if (ACT) actEnd(true); player.stop(); return r; };
  out.found = !!it;
  out.hours = [tapAt(11 * 1440 + 1199), tapAt(4 * 1440 + 1230)];   // 19:59; Day 5 (before Day 6)
  const pick = k => { if (!starLog(it)) return false; devChosen(k); return true; }, d = 12, sky = starSky(d);
  setShipNow(11 * 1440 + 1230);
  out.tap = tapAt(11 * 1440 + 1230);
  out.wrong = [pick((sky.fresh + 1) % 3), s.n];
  out.right = [pick(sky.fresh), s.n, s.last];
  out.again = tapAt(11 * 1440 + 1300);                      // one a night
  out.next = tapAt(12 * 1440 + 1230);
  setShipNow(11 * 1440 + 1230); const sato0 = relGet('sato').pts; s.n = 2; s.last = 0; pick(sky.fresh); out.third = [s.n, relGet('sato').pts > sato0];
  s.n = 9; s.last = 0; pick(sky.fresh); out.ten = [s.n, W.ms.some(x => x[0] === 'stars')];
  // the save's own path: SAVE_EXTRA builds it, JSON, then worksClean as at load
  worksSide().cabin = { rug: 'woven rug', shelf: 'metal puzzle' };
  const save = { ship: {} }; for (const f of SAVE_EXTRA) { try { f(save); } catch (e) { /* not ours */ } }
  const back = worksClean(JSON.parse(JSON.stringify(save.ship.works)));
  out.trip = [JSON.stringify(back.side.cabin), JSON.stringify(back.side.stars)];
  out.looks = CABIN_SPOTS.map(k => CABIN_FITS[k].every(x => !!CABIN_LOOK[x]));
  out.clash = WORKSHOP_ORDERS.filter(o => TINKER_LIST.some(t => t.item === o.thing)).map(o => o.thing);   // R5: an order's thing never shares a tinkered thing's name
  worksSide().cabin = { ledge: 'mug rack' }; out.oldRack = cabinData().ledge;
  const P2 = SHIP.player, kc = P2.carry.slice(), ku = P2.untidy, kb = P2.bought; delete worksSide().cabinPut;
  P2.untidy = true; P2.bought = (P2.bought || 0) + 1; const t0 = lockerTidy(); P2.carry = ['plant pot']; delete worksSide().cabin.ledge; cabinTap({ t: 'ledge', cabin: 'ledge' }, null);
  const t1 = lockerTidy(); P2.bought++; out.tidy = [t0, t1, lockerTidy()]; P2.carry = kc; P2.untidy = ku; P2.bought = kb;
  // visitors notice: a stand-in line and someone in your cabin (the writer's bank may not be baked in yet)
  const keepL = LINES['cabin.remark'], keepB = bubbleSay, said = []; LINES['cabin.remark'] = [{ text: 'Nice lamp.', id: 'tst1', flag: 'cabin.lamp' }, { text: 'Good rug.', id: 'tst2', flag: 'cabin.rug' }];
  bubbleSay = (h, t) => said.push(t); worksSide().cabin = { desk: 'little lamp' }; goToDeck(4); player.obj.position.copy(cellPos(40, 11));
  const who = schedPeople()[0], fake = { p: who, h: {}, here: () => [40, 11], x: 0, z: 0 }; DECK_CREW.push(fake); CAB_REMARK.at = -99; CAB_REMARK.day = 0;
  cabinRemark(shipNow()); cabinRemark(shipNow() + 10); DECK_CREW.splice(DECK_CREW.indexOf(fake), 1); LINES['cabin.remark'] = keepL; bubbleSay = keepB;
  out.remark = said;
  return out;
})()"""
def part_t24(g):
    if not g.ev("typeof cabinTap === 'function' && typeof starTap === 'function'"):
        print('24t (off shift): not in this build'); return
    a = g.ev(T24); b = g.ev(T24)
    print('24t cabin:', a['tap'], a['four'], a['back'], a['clean'], a['notMine'], '| stars:', a['sky'], a['friends'])
    check(a['tap'] == [True, 2, True, True, 0, 2, 1, True] and a['four'] == 3 and a['back'] == [['little lamp'], 2], f"24t: spots take what fits and give it back ({a['tap']} {a['back']})")
    check(a['clean'] == '{"desk":"little lamp"}' and a['notMine'] == [False, 0], '24t: an odd save part is cleaned; not your cabin, no bonus')
    check(len(set(a['sky'])) == 3 and all(len(json.loads(x)['pts']) == 3 for x in a['sky']), '24t: three points a night, different nights differ')
    check(all(a['friends']), '24t: Survey warms to you (Sato, then Mori)')
    check(json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True), '24t: differs the second time')
    c = g.ev(T24B)
    print('24t stars driven:', c)
    check(c['found'] and c['hours'] == [False, False] and c['tap'], f"24t: the telescope offers the log from Day 6, 20:00 on ({c['hours']}, {c['tap']})")
    check(c['wrong'] == [True, 0] and c['right'] == [True, 1, 12] and c['again'] is False and c['next'], f"24t: a wrong pick, look again; the right one logs; one a night ({c['wrong']} {c['right']} {c['again']})")
    check(c['third'] == [3, True] and c['ten'] == [10, True], '24t: every third log Survey warms to you; ten give the Record line')
    check(c['trip'] == ['{"rug":"woven rug","shelf":"metal puzzle"}', '{"n":10,"last":12}'], f"24t: cabin and stars round-trip through the save ({c['trip']})")
    check(all(c['looks']), '24t: every thing that fits a spot has a look')
    check(c['clash'] == [] and c['oldRack'] == 'mug tree', f"24t: no order shares a tinkered thing's name; an old save's mug rack on the ledge is the mug tree ({c['clash']}, {c['oldRack']})")
    check(c['tidy'] == [False, True, False], f"24t: a thing placed in your cabin counts as put away, until you buy or make another ({c['tidy']})")
    check(c['remark'] == ['Nice lamp.'], f"24t: a visitor in your cabin notices the lamp, once a day ({c['remark']})")

# 24s the lift roof (M17, seat E4): on paper, when you can climb on (Thursdays from Day 18, trained, 15:30 till there's time for
# the whole spine, once a day); the hold: crew whose plan takes them to another deck wait by the lift on the deck they were
# on until 16:30, then follow their plan; the ride itself, frame by frame: a stop at every deck's guide, out on the bottom
# deck, a ride and a use counted, the lift a little smoother, the car held till 16:30 and let go then; draw calls in the
# shaft; stepping off part way leaves you on that deck; a save mid-ride has you on the top deck in the car, the hold not
# saved; an old or odd save part loads as the default. The same twice.
M17P = r"""(() => {
  SHIP.works = null; SHIP.jobs = []; LIFT_HOLD = null; const B = 17 * 1440; setShipNow(B + 900); machinesNow(); const W = worksInit(); W.tier = 2; W.rank = 'officer';
  const out = { untrained: roofOpen(B + 935) }; W.tr.m17 = 18; const r = roofData(); r.rides = 0; r.last = 0;
  out.open = [roofOpen(B + 929), roofOpen(B + 930), roofOpen(B + 990 - roofLen()), roofOpen(B + 991 - roofLen()), roofOpen(B - 1440 + 935), roofOpen(B + 7 * 1440 + 935), roofOpen(B - 7 * 1440 + 935)];
  r.last = 18; out.twice = roofOpen(B + 935); r.last = 0;
  const ppl = schedPeople(), ts = []; for (let m = 935; m <= 1010; m += 5) ts.push(B + m);
  const base = ppl.map(p => ts.map(t => { const w = whereIs(p, t); return w ? w.deck : null; }));
  setShipNow(B + 935); liftHold(true, B + 990);
  let movers = 0, bad = [], waiting = 0, after = 0;
  ppl.forEach((p, i) => {
    const d0 = base[i][0]; let moved = false;
    ts.forEach((t, k) => { const w = whereIs(p, t), dk = w ? w.deck : null;
      if (t < B + 990) { if (base[i][k] !== d0) { moved = true; if (dk !== d0 || w.type !== 'lift-wait') bad.push(p.id + '@' + hhmm(t % 1440)); else waiting++; } else if (dk !== base[i][k]) bad.push(p.id + '~' + hhmm(t % 1440)); }
      else { if (dk !== base[i][k]) bad.push(p.id + '>' + hhmm(t % 1440)); else after++; } });
    if (moved) movers++;
  });
  out.hold = { movers, waiting, bad: bad.slice(0, 6), held: [liftHeld(B + 935), liftHeld(B + 989), liftHeld(B + 990), liftHeld(B + 934)] };
  let fake = null; const mover = ppl.find((p, i) => base[i].slice(0, 11).some(dk => dk !== base[i][0])), keepL = LINES['roof.wait'], keepB = bubbleSay, said = [];
  if (mover) { fake = { p: mover, h: {}, x: player.obj.position.x, z: player.obj.position.z }; DECK_CREW.unshift(fake); DECK_CREW.splice(DECK_CREW.indexOf(fake), 1); LINES['roof.wait'] = [{ text: 'Lift\'s held again.', id: 'tstw' }]; bubbleSay = (h, t) => said.push(h === fake.h ? t : 'someone else'); ROOF.r = null; ROOF_TALK.at = -99;
    const t1 = ppl.indexOf(mover), k = base[t1].findIndex(dk => dk !== base[t1][0]);
    DECK_CREW.unshift(fake); roofTalk(ts[k]); roofTalk(ts[k] + 7); DECK_CREW.splice(DECK_CREW.indexOf(fake), 1); LINES['roof.wait'] = keepL; bubbleSay = keepB; }
  out.talk = said.filter(x => x !== 'someone else');
  LIFT_HOLD = null;
  delete worksSide().roof; out.old = JSON.stringify(roofData()); worksSide().roof = { rides: -3, last: 'x', foo: 1 }; out.junk = JSON.stringify(roofData());
  worksSide().roof = { rides: 2, last: 11 }; out.trip = JSON.stringify(worksClean(JSON.parse(JSON.stringify(SHIP.works))).side.roof);
  return out;
})()"""
M17SET = r"""((day) => {
  const B = (day - 1) * 1440; LIFT_HOLD = null; setShipNow(B + 935); machinesNow();
  goToDeck(1); const c = nearestOpen(LIFT_AT[0] + 2.5, LIFT_AT[1], player); player.obj.position.copy(cellPos(...c));
  window.__m17 = { cond: Math.round(SHIP.machines['5-mainlift-1'].cond), stops: [], calls: 0 };
  const a = roofLiftTap(); devChosen(0); return [a, ACT && ACT.kind];
})"""
M17WATCH = r"""(() => { const A = ACT, R = A && A.kind === 'roofRide' && A.o.r, M = window.__m17;
  if (R && R.st === 'grease' && !M.stops.includes(R.k)) M.stops.push(R.k);
  if (R && R.inShaft && !R.off) M.calls = Math.max(M.calls, renderer.info.render.calls);
  return R ? [R.st, R.k, !!R.inShaft, player.deck, roomAt(...player.here()), ROOF.r === R, roofData().on || 0] : A && A.kind === 'roofRide' ? ['in', 0, false, player.deck, roomAt(...player.here())] : null; })()"""
def part_m17(g):
    if not g.ev("typeof roofStep === 'function'"):
        print('  m17: 24s is not in this build'); return
    keep = g.ev("JSON.stringify({ t: shipNow(), deck: deckDef.num, pos: [player.obj.position.x, player.obj.position.z], needs: SHIP.player.needs, carry: SHIP.player.carry })")
    a = g.ev(M17P); b = g.ev(M17P)
    print('  m17 open:', a['untrained'], a['open'], a['twice'], '| hold:', a['hold'], '| saves:', a['old'], a['junk'], a['trip'])
    check(a['untrained'] is False and a['open'] == [False, True, True, False, False, True, False] and a['twice'] is False, f"m17: you can climb on Thursdays from Day 18, 15:30 while there's time, once a day ({a['open']})")
    h = a['hold']
    check(h['held'] == [True, True, False, False] and not h['bad'], f"m17: held 15:35-16:30; crew who'd change deck wait by the lift, then follow their plan ({h['bad']})")
    check(a['talk'] == ["Lift's held again."], f"m17: someone waiting by the held lift says so, once a hold ({a['talk']})")
    check(a['old'] == '{"rides":0,"last":0}' and a['junk'] == '{"rides":0,"last":0}' and a['trip'] == '{"rides":2,"last":11}', 'm17: an old or odd save part loads as the default; it round-trips')
    check(json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True), 'm17: differs the second time')
    runs = []
    for day, off in ((18, None), (25, 2)):
        g.ev("SHIP.works = null"); g.ev("(() => { setShipNow(17 * 1440 + 900); const W = worksInit(); W.tier = 2; W.rank = 'officer'; W.tr.m17 = 18; })()")
        if day == 25: g.ev("(() => { const r = roofData(); r.rides = 1; r.last = 18; SHIP.works.use.m17 = 1; })()")
        start = g.ev(f"({M17SET})({day})"); seen = []; mid = None
        for n in range(200):
            g.step(10); w = g.ev(M17WATCH)
            if w and (not seen or seen[-1][:2] != w[:2]): seen.append(w)
            if w and w[2] and mid is None: mid = w
            if off is not None and w and w[0] == 'drop' and w[1] == off: g.ev("actEnd(true)"); g.step(60); break
            if w is None: g.step(60); break
        res = g.ev("[deckDef.num, ACT && ACT.kind, ROOF.g && ROOF.g.visible, JSON.stringify(roofData()), SHIP.works.use.m17 || 0, Math.round(SHIP.machines['5-mainlift-1'].cond), liftHeld(), Math.round(shipNow() % 1440), JSON.stringify(window.__m17), roofDecks()]")
        held = g.ev(f"[liftHeld({(day - 1) * 1440 + 989}), liftHeld({(day - 1) * 1440 + 990}), 'LIFT_HOLD' in JSON.parse(JSON.stringify(SHIP.works))]")
        runs.append([start, seen, mid, res, held])
        print(f'  m17 ride Day {day}:', start, '| mid', mid, '| end', res, held)
    (s1, seen1, mid1, r1, h1), (s2, seen2, mid2, r2, h2) = runs
    m1 = json.loads(r1[8]); decks = r1[9]
    check(s1 == [True, 'roofRide'] and mid1 and mid1[3] == 1 and mid1[4] == '@' and mid1[5] is True and mid1[6] == 18, f"m17: you climb on (the ride is the roof's, side.roof.on set); mid-ride a save has you on Deck 1 in the car ({mid1})")
    check(m1['stops'] == list(range(len(decks))) and r1[0] == decks[-1] and r1[1] is None and not r1[2], f"m17: a stop at every deck's guide, out on the bottom deck ({m1['stops']}, Deck {r1[0]})")
    check(r1[3] == '{"rides":1,"last":18}' and r1[4] == 1 and r1[5] > m1['cond'], f"m17: the ride counts, the lift runs smoother ({r1[3]} use {r1[4]} cond {m1['cond']} -> {r1[5]})")
    check(r1[6] and h1[:2] == [True, False] and not h1[2], 'm17: the car is held till 16:30, let go then; the hold is not saved')
    check(0 < m1['calls'] < 160, f"m17: draw calls in the shaft {m1['calls']}")
    check(r2[0] == decks[2] and r2[1] is None and not r2[2] and r2[3] == '{"rides":1,"last":18}', f"m17: stepping off part way leaves you on that deck, no ride counted ({r2[0]}, {r2[3]})")
    g.ev(f"({M17SET})(32)"); fade = None   # R5: walking off in the fade before the shaft: the fade goes, no "saved on the roof" left behind
    for n in range(120):
        g.step(5); w = g.ev(M17WATCH)
        if w and w[0] == 'dark': g.ev("actEnd(true)"); g.step(20); fade = g.ev("[+fadeEl.style.opacity, ROOF.r.off, 'on' in roofData(), ACT && ACT.kind]"); break
    check(fade == [0, True, False, None], f"m17: stepping away in the fade before the shaft undoes the fade ({fade})")
    res = g.ev("(() => { const kt = toast, said = []; toast = (a, b) => said.push(b); ROOF.r = null; roofData().on = 32; const S = worksSide(); for (const f of WORK_TICKS) { try { f(shipNow(), false); } catch (e) {} } for (const f of WORK_TICKS) { try { f(shipNow() + 1, false); } catch (e) {} } toast = kt; return [said.filter(x => /saved on the lift roof|back at the top/i.test(x)).length, 'on' in roofData()]; })()")
    check(res == [1, False], f"m17: loaded from a save made on the roof, roof.resume once ({res})")
    a2 = g.ev(M17P)
    check(json.dumps({**a2, 'talk': 0}, sort_keys=True) == json.dumps({**a, 'talk': 0}, sort_keys=True), 'm17: the paper part differs after the rides')
    g.ev(f"(() => {{ const k = {keep}; LIFT_HOLD = null; setShipNow(k.t); if (deckDef.num !== k.deck) goToDeck(k.deck); player.obj.position.x = k.pos[0]; player.obj.position.z = k.pos[1]; Object.assign(SHIP.player.needs, k.needs); SHIP.player.carry = k.carry; }})()")   # as it was, for the parts after
PARTS['m17'] = part_m17

only = set(sys.argv[2:])
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1])
    ev = g.ev
    sr = ev(ROW_STAND)                                     # E2's rows (m13, m14) live in 24 core's table (E1); a stand-in only in a build without it
    if sr: print('stand-in ladder rows (24 core\'s table not in this build):', sr)
    rows = ev("CAREER_LADDER.map(r => ({ id: r.id, name: r.name, size: r.size, inBuild: !!WORK_MECH[r.id], stages: (r.stages || []).length }))")
    for r in rows:
        if only and r['id'] not in only: continue
        if not r['inBuild']:
            print(f"{r['id']} ({r['name']}): not in this build")
            continue
        if r['id'] == 't2' and ev("typeof promoPassed === 'function'"):   # 24p's test job (0.44.18) is no training: career_check (i)-(j) tests it
            print(f"t2 ({r['name']}): 24p's test job, not a training (career_check (i) and (j))")
            continue
        a = ev(f"({TRAIN})('{r['id']}')")
        b = ev(f"({TRAIN})('{r['id']}')")
        print(f"{r['id']} ({r['name']}, {r['size']}): opened Day {a['day']}, trained Day {a['trained']}, steps {a['states']}, teacher's job by {a['teacher']}, yours by {a['yours']}, stage {a['stage']}")
        check(a['opened'] and a['trained'] is not None, f"{r['id']}: never trained")
        if r['size'] == 'big' and not ev(f"!!WORK_MECH['{r['id']}'].noJob") and not ev(f"!!WORK_MECH['{r['id']}'].oneJob") and not ev(f"!!WORK_MECH['{r['id']}'].self"):
            check(a['states'][:3] == ['meet', 'watch', 'do'] or 'meet' in a['states'], f"{r['id']}: the training's steps {a['states']}")
            check(a['teacher'] not in (None, 'you') and a['yours'] == 'you', f"{r['id']}: the teacher's job, then yours")
        check(a['stage'] == 0, f"{r['id']}: stage {a['stage']} once trained (0 expected)")
        check(json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True), f"{r['id']}: the training differs the second time")
        if r['id'] in PARTS:
            PARTS[r['id']](g)
    if (not only or 'side' in only) and ev("typeof worksSideXp === 'function'"):
        print('side (Step 4\'s core: tool wear, the side-job cap, the texts):'); part_side(g)
    if (not only or 'side' in only or 'm4' in only) and ev("typeof manifestRun === 'function' && !!JOB_KINDS.haul"):
        part_mrun(g); part_haul2(g)
        if ev("!!JOB_KINDS.stocktake"): part_stock(g)
    if (not only or 'side' in only or 'm1' in only) and ev("typeof roundDoor === 'function'"):
        part_round23(g)
    for k, f in EXTRA.items():                             # parts that aren't ladder rows (24l's favour cases)
        if (not only or k in only) and ev(f"!!JOB_KINDS['{k}'] || (typeof ffState === 'function' && '{k}' === 'ff') || (typeof teamParts === 'function' && '{k}' === 'tparts')"): print(k + ':'); f(g)
    if not only or 't24' in only: part_t24(g)
    ev("SHIP.works = null")
    if g.errors: fail('page errors: ' + ' | '.join(g.errors[:5]))
    g.close()
    if not only or only & {'m13', 'm14', 'm15', 'fcase', 'ff', 'side', 'tparts'}:
        print('side (E2\'s saved parts):'); side_save(pw)

print('MECH CHECK OK' if ok else 'MECH CHECK FAILED')
sys.exit(0 if ok else 1)
