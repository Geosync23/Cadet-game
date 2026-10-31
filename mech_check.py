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
  const seen = [], doJob = jid => { const j0 = SHIP.jobs.find(x => x.id === jid); if (j0 && j0.kind === 'team') return teamDo(jid); if (!(j0 && j0.claimedBy === 'you') && !claimJob(jid)) return false; const j = SHIP.jobs.find(x => x.id === jid);
    if (j.train === 'm7' && typeof scanRead === 'function') { scanRead(jid); if (typeof caseTick === 'function') caseTick(); }   // the scanner's training: you read it first (it shows Day 5's case; p5-fix2)
    const cs = SHIP.works && SHIP.works.cases && (SHIP.works.cases.open || []).find(c => c.job === jid);   // a head-scratcher (24k): call it right first
    if (cs && typeof caseCall === 'function') caseCall(cs.id, cs.cause);
    jobStops(j).forEach((s, k) => jobStepDone(jid, k, j.kind === 'rewire' && s.step === 'wire' ? { pick: rewRight(j, k) } : j.kind === 'arraycal' ? (s.how === 'turn' ? { value: 0 } : s.how === 'choose' ? { pick: arrStars(j)[0].id } : undefined) : undefined)); return turnInJob(jid); };   // 24x: a star picked, the dial settled   // 24q: a rewire's pairs answered from its chart
  let teacher = null, yours = null;
  for (let m = 360; m < 1020; m += 10) {
    const t = (d - 1) * 1440 + m; setShipNow(t); machinesNow(); worksCareerTick(t);
    if (typeof DIALOGUE !== 'undefined' && DIALOGUE && typeof dialogueEnd === 'function') dialogueEnd(true);   // read through
    const c = SHIP.works.cur;
    if (c) seen.push(c.st);
    if (c && c.st === 'meet') { const r = SHIP.occasions.find(x => x.key === c.occ); if (r && t >= r.at) { r.met = true; worksCareerTick(t + 1); } }
    if (c && c.st === 'watch') { c.w = TRAIN_WATCH; worksCareerTick(t + 2); const dj = SHIP.jobs.filter(x => x.train === id && x.status === 'done').pop(); teacher = dj ? dj.doneBy : null; }
    if (c && c.st === 'do' && (!myJob() || myJob().id === c.j || (SHIP.jobs.find(x => x.id === c.j) || {}).kind === 'team') && doJob(c.j)) yours = (SHIP.jobs.find(x => x.id === c.j) || {}).doneBy;
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
  const ms = j.route.filter(id => SHIP.machines[id]);   // JB2 (note 15): a round's check points (chk:...) are no machines
  out.kinds = new Set(j.route.map(id => typeof roundSpot === 'function' ? roundSpot(id).kind : machineById(id).kind)).size; out.checks = j.route.length - ms.length;
  const worn = ms.filter((id, i) => i % 2 === 0), healthy = ms.filter((id, i) => i % 2 === 1);
  for (const id of ms) { const s = SHIP.machines[id]; s.cond = worn.includes(id) ? 60 : 95; s.state = machineState(s.cond); }
  SHIP.jobs = SHIP.jobs.filter(x => !(x.machine && j.route.includes(x.machine)));   // no jobs on them yet
  out.claimed = claimJob(j.id); const xp0 = W.xp;
  out.stops = jobStops(j).map((s, k) => [s.how, s.places[0] || null, (s.opts && s.opts.marks || []).length, !!SHIP.machines[j.route[k]]]);
  const mark = (x, k) => jobStepDone(x.id, k, { pick: !SHIP.machines[x.route[k]] ? 'fine' : worn.includes(x.route[k]) ? 'worn' : k === 1 ? 'worn' : 'fine' });
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
  if (j2) { const m2 = j2.route.filter(id => SHIP.machines[id]); for (const id of m2) { const s = SHIP.machines[id]; s.cond = 60; s.state = 'worn'; } SHIP.jobs = SHIP.jobs.filter(x => !(x.machine && j2.route.includes(x.machine)));
    run(t2 + 440, t2 + 1080); out.crew = [j2.status, j2.claimedBy || j2.doneBy, j2.doneBy !== 'you' && j2.status === 'done'];
    out.crewFound = m2.filter(id => SHIP.jobs.some(y => y.machine === id && y.found <= shipNow())).length + '/' + m2.length; }
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
  const j = SHIP.jobs.find(x => x.id === c.j), sp = id => typeof roundSpot === 'function' ? roundSpot(id) : machineById(id); out.job = j && [j.kind, j.train, j.route.length, sp(j.route[0]).kind, j.title, j.claimedBy || null, heldForYou(j)];
  out.tour = typeof CHECKS_ON !== 'undefined' && CHECKS_ON;   // JB2 (note 14): the first rounds a tour of checks
  if (j && out.tour) { const S = j.route.map(sp); out.tourOf = { kinds: new Set(S.map(x => x.kind)).size, checks: S.filter(x => x.check).length, decks: S.map(x => x.deck), marks: jobStops(j).map(x => (x.opts.marks || []).length), text: jobStops(j).every(x => typeof x.opts.text === 'string' && x.opts.text.length > 5) }; }
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
        if s1.get('tour'):   # JB2 (patch 0.99.5 note 14): five checks, three on Deck 5 then two on Deck 4, no kind twice, two machines, one button each, a reading each
            to = s1.get('tourOf') or {}
            check(jb[0] == 'rounds' and jb[1] == 'm1' and jb[2] == 5 and jb[5] is None and jb[6] and 'tour' in jb[4], f"m1: the first rounds, a tour of checks, held for you, not yet taken ({jb})")
            check(to.get('kinds') == 5 and to.get('checks') == 3 and to.get('decks') == [5, 5, 5, 4, 4] and to.get('marks') == [1] * 5 and to.get('text'), f"m1: the tour: five different things, two machines, Decks 5 then 4, one button and a reading each ({to})")
        else:
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
    check(a['claimed'] and all(s[0] == 'look' and s[1] and s[2] == (3 if s[3] else 1) for s in a['stops']), f"m1: stops {a['stops']}")
    check(a['kinds'] == len(a['route']) and (a['checks'] == 2 or not g.ev("typeof CHECKS_ON !== 'undefined' && CHECKS_ON")) or not g.ev("typeof CHECKS_ON !== 'undefined' && CHECKS_ON"), f"m1: a morning round has no kind twice and two check points (JB2, note 15: kinds {a['kinds']} of {len(a['route'])}, checks {a['checks']})")
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
# the fire drill played by taps (p5-fix2: a side job, so myJob() left it out and the taps did nothing; Calder always said
# "Four and a half minutes", it never counted, the arrow stayed up and the Calendar named the crew's lift lobbies): Day 3
# at 14:52 on Deck 5, tap the extinguisher, stand at the hatch (a tap on the floor there), tap it again to put it back;
# each a stop done, the extinguisher in your hand between, the arrow on to each next stop and off after; the all-clear
# by you, trained; the Calendar's Wednesday names the Works bay
M3D_TAPS = r"""(() => {
  SHIP.works = null; SHIP.occasions.length = 0; SHIP.notes = []; SHIP.flags = {}; SHIP.jobs = []; SHIP.mail = [];
  MACH_HOUR = null; MACH_SEEN = -1; WORKS_TICK.m = WORKS_TICK.h = -1;
  const run = (from, to) => { for (let m = from; m <= to; m++) { setShipNow(m); machinesNow(); worksCareerTick(m); } };
  setShipNow(1440 + 300); machinesNow(); const W = worksInit(); W.tr.m1 = 2; W.use.m1 = 1; W.use.m4 = 1; W.op[1] = ['m1'];
  run(2 * 1440 + 360, 2 * 1440 + 860); if (deckDef.num !== 5) goToDeck(5);
  const it = ITEMS.filter(i => i.t === 'Fire extinguisher').map(i => { i.hit.getWorldPosition(_wp); return [i, _wp.clone()]; })[0], gl = nearestOpen(it[1].x, it[1].z, player);   // 14:20, before Calder's call: a tap only reads it (AR2's A1)
  player.obj.position.copy(cellPos(...gl)); player.stop(); playerTap(it[0], it[1].clone(), it[1].clone()); const early = [ACT && ACT.kind, (drillJobOf(3).stepsDone || []).length]; if (ACT) actEnd(true);
  run(2 * 1440 + 861, 2 * 1440 + 892);
  const e = DEV_WEEK[2].find(x => x.at === 900);
  return [!!drillJobOf(3), IX_GOAL && IX_GOAL.label, e && e.where, early];
})()"""
M3D_TAP = r"""(({ title, place }) => {
  if (place) { const s = placeSpot(place), gl = nearestOpen(s.x, s.z, player); player.obj.position.copy(cellPos(...gl)); player.stop(); return [jobSpotTap(new THREE.Vector3(s.x, 0, s.z)), ACT && ACT.kind]; }
  const it = ITEMS.filter(i => i.t === title).map(i => { i.hit.getWorldPosition(_wp); return [i, _wp.clone()]; })[0]; if (!it) return ['no item'];
  const gl = nearestOpen(it[1].x, it[1].z, player); player.obj.position.copy(cellPos(...gl)); player.stop();
  return [playerTap(it[0], it[1].clone(), it[1].clone()), ACT && ACT.kind];
})"""
M3D_SEE = "(() => { const j = drillJobOf(3); return [(j.stepsDone || []).slice(), typeof ixHold === 'function' ? ixHold() : null, IX_GOAL ? IX_GOAL.label : null]; })()"
def m3d_taps(g):
    if not g.ev("!!(DECKS[5].drill && placeById(DECKS[5].drill.ext))"): return
    keep = g.ev("JSON.stringify({ t: shipNow(), deck: deckDef.num, pos: [player.obj.position.x, player.obj.position.z], needs: SHIP.player.needs, carry: SHIP.player.carry })")
    a = g.ev(M3D_TAPS); seen = [a]
    def wait():
        for k in range(300):
            g.step(10)
            if not g.ev("ACT && ACT.kind"): break
    for t in ({'title': 'Fire extinguisher'}, {'place': '5-drill-hatch'}, {'title': 'Fire extinguisher'}):
        r = g.ev(f"({M3D_TAP})({json.dumps(t)})"); wait(); seen.append([r, g.ev(M3D_SEE)])
    for k in range(80):
        g.step(30)
        if g.ev("drillJobOf(3).status") == 'done': break
    g.step(5)
    end = g.ev("(() => { const j = drillJobOf(3); return [j.status, j.doneBy, SHIP.works.tr.m3d !== undefined, IX_GOAL ? IX_GOAL.label : null, simNotes('drill', 2880).map(n => n.you)]; })()")
    print('  24c drill by taps:', json.dumps(seen), json.dumps(end))
    check(a[0] and a[2] and 'Works bay' in a[2], f"m3d taps: the Calendar's drill place is the Works bay ({a[2]})")
    check(a[3] == [None, 0], f"m3d taps: a tap on the extinguisher at 14:20, before the call, starts nothing ({a[3]})")
    check([x[0][0] for x in seen[1:]] == [True, True, True], f"m3d taps: each tap starts the stop ({[x[0] for x in seen[1:]]})")
    check([x[1][0] for x in seen[1:]] == [[0], [0, 1], [0, 1, 2]], f"m3d taps: each stop done in turn ({[x[1][0] for x in seen[1:]]})")
    check([x[1][1] for x in seen[1:]] == ['extinguisher', 'extinguisher', None], f"m3d taps: the extinguisher in your hand till it's back ({[x[1][1] for x in seen[1:]]})")
    check(seen[1][1][2] and seen[2][1][2] and seen[3][1][2] is None, f"m3d taps: the arrow on to each stop, off after the last ({[x[1][2] for x in seen[1:]]})")
    check(end[:4] == ['done', 'you', True, None] and end[4] == [True], f"m3d taps: done by you, trained, no arrow left ({end})")
    g.ev(f"(() => {{ const k = {keep}; setShipNow(k.t); if (deckDef.num !== k.deck) goToDeck(k.deck); player.obj.position.x = k.pos[0]; player.obj.position.z = k.pos[1]; Object.assign(SHIP.player.needs, k.needs); SHIP.player.carry = k.carry; clearGoal(); }})()")   # as it was, for the parts after
def m3d_both(g):
    m3d_part(g); m3d_jump(g); m3d_taps(g)
PARTS['m3d'] = m3d_both

# 24g the scanner's training played by taps (p5-fix2: the Day 5 job listed the washer's pump, so after Take it the arrow
# said "Fetch a pump", the pump went in as a plain repair, the head-scratcher closed unseen, and you were trained without
# a scan; and a repair at the panel never asked the case, so an uncalled head-scratcher was "fixed"): to the training
# job's "do", take it; the arrow says look it over; the look-over is the scan and shows the case; a repair before a call
# leaves it faulty; the right call, the fetch, the fit, the turn-in: trained. Then on paper, the job finished without a
# scan: not trained
M7_SETUP = TRAIN.replace("if (c && c.st === 'do' && (!myJob()", "if (c && c.st === 'do') break; if (false && (!myJob()").replace("const st0 = worksStage(id);", "const st0 = 0; const c = SHIP.works.cur; window.__m7j = c && c.j; return { st: c && c.st };")
M7_WATCH = TRAIN.replace("if (c && c.st === 'watch') {", "if (c && c.st === 'watch') break; if (false) {").replace("const st0 = worksStage(id);", "const st0 = 0; const c = SHIP.works.cur; return { st: c && c.st, board: !!c && jobsBoard().some(x => x.id === c.j), took: !!c && claimJob(c.j) };")
M7_LATER = r"""(() => { const W = SHIP.works; if (!W.tr.m7) W.tr.m7 = 5; toolGive('scanner'); const use0 = W.use.m7 || 0;
  const m = machineList().find(x => !x.stub && (x.deck === 3 || x.deck === 4) && panelPlace(x.id) && caseCauses(x).some(f => f.part) && !SHIP.jobs.some(j => j.machine === x.id && j.status !== 'done'));
  const f = caseCauses(m).find(x => x.part), id = jobReserve(m.id, worksDay(shipNow()), shipNow() % 1440, 21, { tier: 1, cause: f.id }), j = SHIP.jobs.find(x => x.id === id);
  delete j.make; delete j.makeMins; j.cause = f.id; j.parts = [f.part]; delete j.case; claimJob(id);
  const before = ixJobStep().label; scanRead(id); SHIP.player.carry = []; const after = ixJobStep().label;
  jobStops(j).forEach((x, k) => jobStepDone(id, k)); turnInJob(id);
  return { before, scan: !!j.scan, after, use0, use: W.use.m7 || 0 }; })()"""
M7_SEE = "(() => { const j = SHIP.jobs.find(x => x.id === window.__m7j) || {}, cs = ((SHIP.works.cases || {}).open || []).find(c => c.job === j.id), g = ixJobStep(); return { goal: g && g.label, scan: !!j.scan, shown: cs ? !cs.wait : null, work: !!j.workDone, st: j.status, tr: SHIP.works.tr.m7 !== undefined }; })()"
M7_PANEL = r"""(() => { const j = myJob(), m = machineById(j.machine); if (deckDef.num !== m.deck) goToDeck(m.deck); const s = placeSpot(panelPlace(m.id)), gl = nearestOpen(s.x, s.z, player); player.obj.position.copy(cellPos(...gl)); player.stop(); return jobSpotTap(new THREE.Vector3(s.x, 0, s.z)); })()"""
M7_FETCH = r"""(() => { if (deckDef.num !== 5) goToDeck(5); const need = jobNeeds(myJob(), myWork().w, SHIP.player.carry), it = ITEMS.find(i => i.t === shelfName(shelfOf(need[0]))); if (!it) return false; it.hit.getWorldPosition(_wp); const gl = nearestOpen(_wp.x, _wp.z, player); player.obj.position.copy(cellPos(...gl)); player.stop(); return playerTap(it, _wp.clone(), _wp.clone()); })()"""
# patch 0.92.5 (DS1; the user's playtest notes 11 and 15): from Day 4 a lesson meets at 09:00 or 09:15 (the first few
# days as before: 09:15 plus a wait); a lesson not finished by the shift's end ends there, the teacher stops following
# (worksEscort), a training job in your hands goes back to the board, and it's offered again on the next workday
P925_OPEN = r"""((id) => {
  const row = ladderRow(id);
  SHIP.works = null; SHIP.occasions.length = 0; SHIP.notes = []; SHIP.flags = {}; SHIP.jobs = []; SHIP.mail = [];
  MACH_HOUR = null; MACH_SEEN = -1; WORKS_TICK.m = WORKS_TICK.h = -1;
  let d = Math.max(row.day, 2); while (!playerShiftOn(d) || (row.fixed && weekday(d) + 1 !== row.fixed.wd)) d++;
  setShipNow((d - 1) * 1440 + 300); machinesNow(); const W = worksInit();
  W.log.push(['earlier', 1, 0, 'service']);
  for (const r of CAREER_LADDER.slice(0, CAREER_LADDER.indexOf(row))) { W.tr[r.id] = 1; W.use[r.id] = 9; (W.op[1] = W.op[1] || []).push(r.id); }
  if (row.needs) for (const n of [].concat(row.needs)) { if (n.flag) flagSet(n.flag, 1); if (n.rep) W.xp = 999; }
  W.tier = Math.max(W.tier, row.tier || 1); if (row.rank) W.rank = row.rank;
  if (row.needs) for (const n of [].concat(row.needs)) if (n.trained && !ladderRow(n.trained)) W.tr[n.trained] = 1;
  const opened = ladderTick(Math.floor(((d - 1) * 1440 + WORKS_ASK[0]) / 60)), c = W.cur, r = c && SHIP.occasions.find(x => x.key === c.occ);
  return { d, opened, st: c && c.st, at: r ? r.at - (d - 1) * 1440 : null };
})"""
P925_LAPSE = r"""((took) => {
  const W = SHIP.works, c = W.cur; if (!c) return null; const j = SHIP.jobs.find(x => x.id === c.j), st0 = c.st, by = c.by;
  if (took && j && !j.claimedBy) claimJob(j.id);
  const p = ROSTER.find(x => x.id === by), t = (c.d - 1) * 1440 + dayShiftEnd(c.d) + 1, before = worksEscort(p, t - 30);
  setShipNow(t); trainTick(t);
  const j2 = SHIP.jobs.find(x => x.id === c.j), st = W.cur && W.cur.st, after = (e => e && e.mode)(worksEscort(p, t + 1)), lapse = simNotes('trainLapse').length;
  let d2 = c.d + 1; while (!playerShiftOn(d2)) d2++;
  setShipNow((d2 - 1) * 1440 + WORKS_ASK[0]); machinesNow(); ladderTick(Math.floor(((d2 - 1) * 1440 + WORKS_ASK[0]) / 60));   // the next workday's ask
  return { st0, st, before: before && before.mode, after, mine: !!j2 && j2.claimedBy === 'you', lapse, next: W.cur && W.cur.id === c.id ? W.cur.st + ' Day ' + W.cur.d : null };
})"""
# (FX15, the user, patch 0.92.5 #22: "all training and lessons need it") every training job held for you on the board: the
# row marked and named, the pointer on its Take it, the arrow naming it. A look at the board for one job: its row, the
# board's line, the pointer's words and the arrow's (the guide entry whose id starts with `arrow`, its goal's label)
P925L_LOOK = r"""((jid, arrow) => {
  ixBoard.open(); const row = [...document.querySelectorAll('#ixBoardL .ixjob')].find(r => r.dataset.job === jid), sub = document.getElementById('ixBoardX').textContent; ixBoard.close();
  SHIP.device.pointsSeen = {}; SHIP.guide.seen = {}; POINT_Q.length = 0; GUIDE.list.length = 0; guideTrain(); guideShift();
  const q = POINT_Q.find(x => /^p:board:lesson:/.test(x.id)), e = arrow && GUIDE.list.find(x => x.id.indexOf(arrow) === 0); let a = null; try { a = e ? e.goal() : null; } catch (x) { a = null; }
  return { lesson: boardLesson() === jid, row: row ? row.textContent.slice(0, 140) : null, marked: !!row && /lesson/.test(row.className), take: !!row && !!row.querySelector('button'), sub, pointer: q ? q.path.map(s => s.label || '').join('|') : null, arrow: a ? a.label : null };
})"""
P925L_T2 = M7_SETUP.replace("W.log.push(['earlier', 1, 0, 'service']);", "W.log.push(['earlier', 1, 0, 'service']); if (id === 't2') { W.xp = 999; W.test = { tier: 2, day: d, tries: 0, passed: false }; }")
P925L_CASE = r"""(() => {   // a head-scratcher lesson's first case (24k's p3Stage, by hand): Washer 2's pump, held for you, its case shown
  const d = SHIP.time.day, id = jobReserve('4-washer-2', d, SHIP.time.min, 20, { train: 'p3', tier: 1, cause: 'pump', until: shipNow() + 1440 }), j = SHIP.jobs.find(x => x.id === id); if (!j) return null;
  delete j.make; delete j.makeMins; j.cause = 'pump'; j.parts = ['pump']; j.train = 'p3'; SHIP.works.cur = null;
  const c = { id: 'c' + j.id, job: j.id, kind: 'p3', k: 0, band: 'T1', cause: 'pump', sus: ['pump'], clues: [], got: [], crossed: [], known: [], calls: [], posted: shipNow(), until: 0, wait: false, taken: false, train: true, told: true, title: '' };
  caseState().open.push(c); j.case = c.id; if (j.found > shipNow()) setShipNow(j.found); return j.id; })()"""
P925L_DAY1 = r"""((slot) => {   // the arrival week's jobs (section 21's INTRO_JOBS): Day 1, the intro on, the job held for you on the board
  const I = SHIP.intro, keep = { on: I.on, ended: I.ended, done: { ...I.done } }; window.__p925l = keep;
  I.on = true; I.ended = false; SHIP.works.cur = null; SHIP.jobs = []; const at = slot === 1 ? 540 : 780;
  setShipNow(at + 10); machinesNow(); const id = jobReserve(slot === 1 ? 'lights' : 'washer', 1, at, slot), j = SHIP.jobs.find(x => x.id === id);
  if (j && j.found > shipNow()) setShipNow(j.found + 1);
  return id; })"""
P925L_ARROW = r"""(() => {   // the intro's board arrow (section 21's introArrowTick): clocked in, told, the tea done, no arrow of anyone else's
  const I = SHIP.intro, d = 1; I.done['arrow:clock'] = I.done['arrow:clock'] ?? shipNow(); I.done['tea:end'] = shipNow(); I.done['call:end'] = shipNow(); I.done['arrow:eat'] = I.done['arrow:eat'] ?? shipNow();
  if (!careerClockedIn(d)) careerClock(shipNow(), true); if (typeof clearGoal === 'function') clearGoal(); INTRO_UI.arrowAt = 0; introArrowTick();
  return { want: introArrowWant(Math.floor(shipNow())), goal: IX_GOAL ? IX_GOAL.label : null }; })()"""
def part_p925l(g):
    print('p925l (patch 0.92.5 #22: every training job on the board marked, pointed at and named by the arrow):')
    t2 = g.ev(f"(() => {{ ({P925L_T2})('t2'); const c = SHIP.works.cur, j = c && SHIP.jobs.find(x => x.id === c.j); if (j && j.found > shipNow()) setShipNow(j.found); return c && c.st === 'do' ? c.j : null; }})()")
    a = g.ev(f"({P925L_LOOK})({json.dumps(t2)}, null)") if t2 else None
    print(f'  the Tier 2 test job: {a}')
    check(bool(a) and a['marked'] and 'Your Tier 2 test job: take this one' in (a['row'] or '') and 'lesson' not in (a['row'] or '').split('Your Tier 2 test job')[1][:8] and a['pointer'] and (a['pointer'].endswith('Take this one: your Tier 2 test job') or a['pointer'].endswith('Your Tier 2 test: take it')),   # (FX28's words with PROMO_BEATS_ON)
          f'#22: the Tier 2 test job is named as itself on the board and by the pointer, not "tier 2 test job lesson" ({a})')
    cj = g.ev(P925L_CASE)
    b = g.ev(f"({P925L_LOOK})({json.dumps(cj)}, 'train:board:')") if cj else None
    print(f'  a head-scratcher lesson\'s first case: {b}')
    check(bool(b) and b['lesson'] and b['marked'] and 'Your head-scratcher lesson: take this one' in (b['row'] or '') and 'head-scratcher lesson' in b['sub'] and (b['pointer'] or '').endswith('Take this one: your head-scratcher lesson') and b['arrow'] == 'Your head-scratcher lesson',
          f'#22: a head-scratcher lesson\'s case job is marked, its Take it pointed at, and the arrow names it ({b})')
    m6 = g.ev(f"(() => {{ ({M7_SETUP})('m6'); const c = SHIP.works.cur, j = c && SHIP.jobs.find(x => x.id === c.j); if (j && j.found > shipNow()) setShipNow(j.found); if (j && j.claimedBy) {{ j.claimedBy = null; j.status = 'open'; }} return c && c.st === 'do' ? c.j : null; }})()")
    c6 = g.ev(f"({P925L_LOOK})({json.dumps(m6)}, null)") if m6 else None
    print(f'  Making it safe\'s job left on the board (taken at the pipe, not here): {c6}')
    check(bool(c6) and not c6['lesson'] and not c6['marked'] and 'take this one' not in (c6['row'] or '') and not c6['pointer'], f'#22: a lesson job you can\'t take at the board isn\'t marked "take this one" ({c6})')
    for slot, name in ((1, 'shadow job'), (2, 'job to lead')):
        jid = g.ev(f"({P925L_DAY1})({slot})")
        d1 = g.ev(f"({P925L_LOOK})({json.dumps(jid)}, null)") if jid else None
        if slot == 2 and d1: g.ev("SHIP.intro.done['arrow:board'] = shipNow() - 240")   # the morning's board arrow long done (you took the shadow job)
        ar = g.ev(P925L_ARROW) if d1 else None
        g.ev("(() => { const k = window.__p925l; if (k) { Object.assign(SHIP.intro, { on: k.on, ended: k.ended, done: k.done }); } if (typeof clearGoal === 'function') clearGoal(); INTRO_UI.arrow = null; })()")
        print(f'  Day 1, slot {slot}: {d1}; the intro\'s arrow: {ar}')
        check(bool(d1) and d1['marked'] and f'Your {name}: take this one' in (d1['row'] or '') and (d1['pointer'] or '').endswith(f'Take this one: your {name}') and ar and ar['goal'] == f'Your {name}: take it at the board',
              f'#22: Day 1\'s {name} is marked on the board, its Take it pointed at, and the intro\'s arrow names it ({d1}, {ar})')

def part_p925(g):
    print('p925 (patch 0.92.5: lessons at 09:00/09:15 from Day 4; the lesson\'s job named on the board; an unfinished lesson ends with the shift):')
    early = [g.ev(f"({P925_OPEN})('{i}')") for i in ('m1', 'm4')]
    late = [g.ev(f"({P925_OPEN})('{i}')") for i in ('m5', 'm7')]   # (m6's is its own urgent call at the pipe, 24f: not a booked meeting)
    print(f'  meets, the first days: {[(e["d"], e["at"]) for e in early]}; from Day 4: {[(e["d"], e["at"]) for e in late]}')
    check(all(e['st'] == 'meet' and e['at'] is not None and e['at'] >= 9 * 60 + 25 for e in early), f'#11: the first few days\' lessons meet as before (09:15 and a wait): {early}')
    check(all(e['st'] == 'meet' and e['at'] in (9 * 60, 9 * 60 + 15) for e in late), f'#11: from Day 4 a lesson meets at 09:00 or 09:15: {late}')
    bd = g.ev(f"""(() => {{ ({M7_SETUP})('m7'); const c = SHIP.works.cur, d = SHIP.time.day;
      if (SHIP.career) SHIP.career.ci = 0;   // not clocked in yet: you're at the board first
      ixBoard.open(); const row = [...document.querySelectorAll('#ixBoardL .ixjob')].find(r => r.dataset.job === c.j), sub = document.getElementById('ixBoardX').textContent;
      SHIP.device.pointsSeen = SHIP.device.pointsSeen || {{}}; SHIP.device.pointsSeen['p:board:lesson:m7'] = 1;   // rung once before: rung again
      POINT_Q.length = 0; guideShift(); const q = POINT_Q.find(x => x.id === 'p:board:lesson:m7'), lab = q ? q.path.map(s => s.label || '').join('|') : null; ixBoard.close();
      return {{ st: c.st, clocked: careerClockedIn(d), row: row ? row.textContent.slice(0, 120) : null, lesson: !!row && /lesson/.test(row.className), sub, pointer: lab }}; }})()""")
    print(f'  the scanner lesson at the board: {bd}')
    check(bd['st'] == 'do' and bd['row'] and 'Your scanner lesson: take this one' in bd['row'] and bd['lesson'] and 'scanner lesson' in bd['sub'],
          f'#12: the board names the lesson\'s job: "Your scanner lesson: take this one", and its line says so ({bd})')
    check(bool(bd['pointer']) and 'scanner lesson' in bd['pointer'] and not bd['clocked'], f'#12: the pointer rings the lesson\'s Take it again, before you\'ve clocked in, naming the lesson ({bd})')
    do = g.ev(f"(() => {{ ({M7_SETUP})('m7'); return ({P925_LAPSE})(true); }})()")
    print(f'  your turn (the scanner), its job in your hands at 17:01: {do}')
    check(bool(do) and do['st0'] == 'do' and do['before'] and do['st'] == 'again' and not do['after'] and not do['mine'] and do['lapse'] >= 1 and (do['next'] or '').split(' ')[0] in ('watch', 'meet', 'do'),
          f'#15: an unfinished lesson ends at the shift\'s end: offered again, the teacher stops following, the job back on the board ({do})')
    hd = g.ev(f"""(() => {{ ({M7_SETUP})('m7'); const W = SHIP.works, c = W.cur, j = SHIP.jobs.find(x => x.id === c.j); if (!c || !j) return null;
      j.status = 'done'; j.doneBy = 'you'; c.st = 'held'; c.hold = true; const open = worksCaseOpen(c.j), p = ROSTER.find(x => x.id === c.by), t = (c.d - 1) * 1440 + dayShiftEnd(c.d) + 1;
      const before = (e => e && e.mode)(worksEscort(p, t - 30)); setShipNow(t); trainTick(t);
      return {{ open, before, cur: W.cur && W.cur.st, trained: W.tr.m7 !== undefined, after: (e => e && e.mode)(worksEscort(p, t + 1)) }}; }})()""")
    print(f'  held (its job turned in, its case open) at 17:01: {hd}')
    check(bool(hd) and hd['before'] == 'follow' and hd['trained'] and not hd['cur'] and not hd['after'], f'#15: a lesson held at the shift\'s end (job done, case open) is trained and the teacher goes ({hd})')
    wa = g.ev(f"(() => {{ ({M7_WATCH})('m7'); const c = SHIP.works.cur; if (c && c.st !== 'watch') {{ c.st = 'watch'; }} return ({P925_LAPSE})(false); }})()")
    print(f'  watching at 17:01: {wa}')
    check(bool(wa) and wa['st0'] == 'watch' and wa['st'] == 'again' and not wa['after'], f'#15: a lesson still at its watching ends at the shift\'s end, the teacher off ({wa})')

def m7_taps(g):
    keep = g.ev("JSON.stringify({ t: shipNow(), deck: deckDef.num, pos: [player.obj.position.x, player.obj.position.z], needs: SHIP.player.needs, carry: SHIP.player.carry })")
    def wait():
        for k in range(300):
            g.step(10)
            if not g.ev("ACT && ACT.kind"): break
    for rid in ('m7', 'm4', 'm5'):                         # any training's watch job (AR2: Yara's load-only run, Calder's oven)
        watch = g.ev(f"({M7_WATCH})('{rid}')")
        print(f'  the teacher\'s job while you watch ({rid}):', watch)
        check(watch['st'] == 'watch' and not watch['board'] and not watch['took'], f"{rid}: the teacher's job isn't on your board and can't be taken ({watch})")
    g.ev("window.__kt = toast; window.__said = []; toast = (a, b) => { window.__said.push(a + ' | ' + b); return window.__kt(a, b); }")
    st = g.ev(f"({M7_SETUP})('m7')"); took = g.ev("claimJob(window.__m7j)"); seen = [g.ev(M7_SEE)]
    for f in (M7_PANEL, M7_PANEL):
        r = g.ev(f); wait(); seen.append([r, g.ev(M7_SEE)])
    call = g.ev("(() => { const c = SHIP.works.cases.open.find(x => x.job === window.__m7j); return !!c && caseCall(c.id, c.cause); })()")
    for f in (M7_FETCH, M7_PANEL):
        r = g.ev(f); wait(); seen.append([r, g.ev(M7_SEE)])
    g.ev("turnInJob(window.__m7j)"); g.step(60); end = g.ev(M7_SEE)
    # FX5: Day 5's case is the scanner job, so it's solved before the p3 row can open (it needs m7 trained); the row then
    # opens within the next ship hours and that solve trains you (it was lost: p3 never learned on Day 5)
    p3 = g.ev("(() => { const t0 = shipNow(), W = SHIP.works, use = W.use.p3 || 0; for (let m = 1; m <= 150 && W.tr.p3 === undefined; m++) { setShipNow(t0 + m); worksCareerTick(t0 + m); } const r = { use, open: worksIsOpen('p3'), tr: W.tr.p3, at: clockText(), ask: flag('works.ask.p3') }; setShipNow(t0); return r; })()")
    print('  24k Day 5\'s case solved on the scanner job, then the p3 row:', p3)
    check(p3['use'] == 1 and p3['open'] and p3['tr'] is not None and not p3['ask'], f"p3: the training case solved on Day 5's scanner job trains you once the p3 row opens, with no ask to go to the board (FX5) ({p3})")
    said = g.ev("(() => { toast = window.__kt; return window.__said.filter(x => /clue|undefined/.test(x)); })()")
    print('  24g the clue toasts:', said)
    check(said and not any('undefined' in x for x in said), f"m7: the clue toasts have a title and a line, no 'undefined' ({said})")
    after = g.ev(M7_LATER)
    print('  24g an ordinary job once you have the scanner:', after)
    check(after['before'] and after['before'].startswith('Look over') and after['scan'] and after['after'] and after['after'].startswith('Fetch') and after['use'] == after['use0'] + 1,
          f"m7: scan first on any faulty job (look it over, then the part), and the use counts with no Fetch pressed ({after})")
    print('  24g scanner training by taps:', st, took, json.dumps(seen), call, json.dumps(end))
    check(st['st'] == 'do' and took and seen[0]['goal'].startswith('Look over') and not seen[0]['scan'], f"m7 taps: after Take it the arrow says look it over ({seen[0]['goal']})")
    check(seen[1][0] and seen[1][1]['scan'] and seen[1][1]['shown'], f"m7 taps: the look-over is the scan, and the head-scratcher shows ({seen[1]})")
    check(seen[2][0] and not seen[2][1]['work'], f"m7 taps: a repair before the call leaves it faulty ({seen[2]})")
    check(call and seen[3][0] and seen[4][0] and seen[4][1]['work'], f"m7 taps: called, fetched and fitted: the work's done ({seen[3:]})")
    check(end['st'] == 'done' and end['tr'], f"m7 taps: turned in, trained ({end})")
    paper = g.ev(f"""(() => {{ ({M7_SETUP})('m7'); const id = window.__m7j; claimJob(id); const j = SHIP.jobs.find(x => x.id === id);
      jobStops(j).forEach((x, k) => jobStepDone(id, k)); const t = turnInJob(id); for (let m = 1; m <= 30; m++) worksCareerTick(shipNow() + m);
      return [t, !!j.scan, SHIP.works.tr.m7 !== undefined]; }})()""")
    print('  24g scanner training finished without a scan:', paper)
    check(paper[0] and not paper[1] and not paper[2], f"m7: a training job finished without a scan doesn't train you ({paper})")
    g.ev(f"(() => {{ const k = {keep}; setShipNow(k.t); if (deckDef.num !== k.deck) goToDeck(k.deck); player.obj.position.x = k.pos[0]; player.obj.position.z = k.pos[1]; Object.assign(SHIP.player.needs, k.needs); SHIP.player.carry = k.carry; clearGoal(); }})()")   # as it was, for the parts after
PARTS['m7'] = m7_taps

# p5-fix2 C: what the career's notes say. The Tuning ask names one time, the meeting's real one (the writer's line had
# 10:15 fixed and the code added the real time after it); the Hauling ask names where the meeting is (Main storage, not
# "the hold"); a Tune job's arrow says Tune, not Repair; the Calendar's Thursday inspection is at 06:30, the walk's time
C_ASK = TRAIN.replace("if (c && c.st === 'meet') {", "if (c && c.st === 'meet') break; if (false) {").replace("const st0 = worksStage(id);", """const st0 = 0; const c = SHIP.works.cur, r = c && SHIP.occasions.find(x => x.key === c.occ);
  const m = c && ((SHIP.mail || []).find(x => x.subject === c.mail) || TRAIN_HELD.mail);
  return { st: c && c.st, at: r ? hhmm(r.at % 1440) : null, room: r ? DECKS[r.deck].rooms[r.room].name : null, subject: m && m.subject, body: m && m.body };""")
def part_fix2_c(g):
    import re
    for rid in ('m5', 'm4'):
        a = g.ev(f"({C_ASK})('{rid}')")
        print(f'  the {rid} ask:', a)
        times = re.findall(r'\b\d\d:\d\d\b', (a.get('subject') or '') + ' | ' + (a.get('body') or ''))
        check(a['st'] == 'meet' and a['body'] and set(times) == {a['at']}, f"{rid}: the ask names the meeting's time, and only that ({times} vs {a['at']})")
        check(a['room'] and a['room'].lower() in a['body'].lower() and 'the hold' not in a['body'], f"{rid}: the ask names where the meeting is ({a['room']}: {a['body']})")
    t = g.ev("""(() => { SHIP.works = null; SHIP.jobs = []; setShipNow(4 * 1440 + 600); machinesNow(); const W = worksInit(); W.tr.m5 = 4;
      const m = machineList().find(x => x.kind === 'oven'); const j = tuneJob(m.id, shipNow()); if (!j) return null; SHIP.jobs.push(j); claimJob(j.id);
      const g = ixJobStep(); dropJob(j.id); SHIP.jobs = []; SHIP.works = null; return g && g.label; })()""")
    print('  a tune job\'s arrow:', t)
    check(t and t.startswith('Tune the'), f"m5: a tune job's arrow says Tune ({t})")
    cal = g.ev("(() => { const e = DEV_WEEK[3][0]; return [e.at, e.title]; })()")
    print('  the Calendar\'s Thursday:', cal)
    check(cal[0] == 390, f"m3i: the Calendar's inspection is at 06:30, the walk ({cal})")

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
   for (let t = 15 * 1440 + 900; t <= 16 * 1440 + 760; t += 5) { setShipNow(t); machinesNow(); for (const f of WORK_TICKS) f(t, false); const j = SHIP.jobs.find(x => x.kind === 'team'); if (j && act) act(j, t, r); if (j && j.status === 'done' && r.right === undefined) r.right = j.machines.every(id => SHIP.machines[id].cond >= TEAM_RESTORE); }   // right when it's done (FX6, 0.92.1: with the Line on the plan picks the washers, which wear under 90 again within the hour)
   const j = SHIP.jobs.find(x => x.kind === 'team');
   r.job = j && { team: j.team.length + (j.you ? 1 : 0), you: !!j.you && !j.youOut, status: j.status, by: j.doneBy, late: j.late, mins: j.doneAt - j.start, posted: j.posted - j.start };
   if (r.right === undefined) r.right = j ? j.machines.every(id => SHIP.machines[id].cond >= TEAM_RESTORE) : null; r.restore = TEAM_RESTORE; r.rep = SHIP.works.xp; r.uses = SHIP.works.use.m8 || 0; return r; };
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
    check((c.get('restore') or 0) >= 98, f"m8: a team job leaves its machines close to new (TEAM_RESTORE {c.get('restore')}, want 98 or more; the user, 2026-10-23)")
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
    for (let d = 14; d < 34; d++) for (const m of machineList()) { const l = lineOf(m.id); if (!l || !lineOn(l) || jobTier({ machine: m.id }) > playerTier()) continue; n++;   // (B2, S5-3: only line machines at your tier: the power line's are Tier 3)
      const t = traceFor(m, (d - 1) * 24 + 9); if (t) { tr++; lines[t] = (lines[t] || 0) + 1; } }
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

# 24w shutdowns (S5-4, B3; P5_M18): the training on Day 18 (Calder's talk at the port junction, the planning screen opens
# on a real job marked for a shutdown, the quietest hour, the kept rooms, the first booking trains you), the 22:00 settle,
# Day 19's shutdown (the job opens with a level-1 arrow, taken in the hour: power off, the work done: back on; missed: it
# lapses, Calder's Mail, the job waits for a new booking); the crew's plan for the booked hour (the mess empties of
# diners, the same day planned before 22:00, after it, and fresh after it: the last two identical); the save's sd read back
SD_RUN = r"""((miss) => {
  const out = { log: [] }, L = x => out.log.push(x);
  for (const e of guideList()) if (/^sd:/.test(e.id)) guideDrop(e.id); Object.assign(SD_UI, { job: null, branch: null, at: null, keep: [], warned: [], inPerson: [], all: false });   // the check's own leftovers from a run before
  SHIP.works = null; SHIP.occasions.length = 0; SHIP.notes = []; SHIP.flags = {}; SHIP.jobs = []; SHIP.mail = [];
  MACH_HOUR = null; MACH_SEEN = -1; WORKS_TICK.m = WORKS_TICK.h = -1;
  const row = ladderRow('m18'); let d = 18; while (!playerShiftOn(d)) d++; out.day = d;
  setShipNow((d - 1) * 1440 + 300); machinesNow(); const W = worksInit(); W.log.push(['earlier', 1, 0, 'service']); W.tier = 3; W.rank = 'senior';
  for (const r of CAREER_LADDER.slice(0, CAREER_LADDER.indexOf(row))) { W.tr[r.id] = 1; W.use[r.id] = 9; (W.op[1] = W.op[1] || []).push(r.id); }
  let booked = null;
  for (let m = 360; m < 1020; m += 5) {
    const t = (d - 1) * 1440 + m; setShipNow(t); machinesNow(); worksCareerTick(t);
    if (typeof DIALOGUE !== 'undefined' && DIALOGUE && typeof dialogueEnd === 'function') dialogueEnd(true);
    const c = SHIP.works.cur; if (c && out.log[out.log.length - 1] !== c.st) L(c.st);
    if (c && c.st === 'meet') { const r = SHIP.occasions.find(x => x.key === c.occ); if (r && t >= r.at) { r.met = true; worksCareerTick(t + 1); } }
    if (c && c.st === 'do' && !booked) { out.screen = sdView().filter(b => b.kind === 'text').map(b => b.text).slice(1, 2).join(' / '); out.badge = (WORKS_TABS.find(x => x.id === 'shut') || {}).badge(); sdAct('sd:quiet', 0); out.keep0 = sdAffected(d + 1, SD_UI.branch, SD_UI.at, []).length;
      const kk = sdBranches()[SD_UI.branch].keep.map(sdRoomKey); for (const k of kk) sdAct('sd:keep', k); out.keep1 = sdAffected(d + 1, SD_UI.branch, SD_UI.at, SD_UI.keep).length; sdAct('sd:book', c.j); booked = sdData().book.find(x => x.job === c.j) || null; }
    if (W.tr.m18 !== undefined) break;
  }
  out.trained = W.tr.m18; out.booked = booked && [booked.day, hhmm(booked.at), booked.branch];
  out.guide = guideList().filter(e => /^sd:/.test(e.id)).map(e => e.id + ' L' + e.level);
  const B2 = d * 1440;
  for (let t = shipNow(); t <= B2 + 300; t += 30) { setShipNow(t); machinesNow(); worksCareerTick(t); }
  out.set = (SHIP.works.sd.set[d + 1] || []).map(x => [x.day, x.at, x.branch, x.keep.length]); out.round = JSON.stringify(sdClean(JSON.parse(JSON.stringify(SHIP.works.sd)))) === JSON.stringify(SHIP.works.sd); out.items = sdItems(d + 1).map(x => x.title + ' ' + hhmm(x.from) + ' ' + x.where);
  const b = SHIP.works.sd.set[d + 1][0], j = SHIP.jobs.find(x => x.id === b.job); out.before = [j.status, j.why]; out.askB = !!b.askB;   // 05:00: still waiting
  for (let t = B2 + 300; t < B2 + b.at - 15; t += 5) { setShipNow(t); machinesNow(); worksCareerTick(t); }
  out.morning = j.status;   // open from 06:00, to fetch the parts
  setShipNow(B2 + b.at - 14); machinesNow(); worksCareerTick(shipNow()); out.atOpen = [j.status, guideList().filter(e => /^sd:/.test(e.id)).map(e => e.id + ' L' + e.level + (e.shown ? ' shown' : ''))];
  if (miss !== true) { out.claim = claimJob(j.id); setShipNow(B2 + b.at + 1); machinesNow(); worksCareerTick(shipNow()); out.st0 = b.st || null;   // in the hour, parts not in hand: the power stays on
    jobStops(j).forEach((s, k) => { if (s.step === 'fetch' || s.step === 'make') jobStepDone(j.id, k); }); setShipNow(B2 + b.at + 2); machinesNow(); worksCareerTick(shipNow()); out.st1 = b.st;
    if (!miss) { jobStops(j).forEach((s, k) => jobStepDone(j.id, k)); setShipNow(B2 + b.at + 30); machinesNow(); worksCareerTick(shipNow()); out.st2 = b.st; out.turnin = turnInJob(j.id); }
    else { for (let t = B2 + b.at + 5; t <= B2 + b.at + 70; t += 5) { setShipNow(t); machinesNow(); worksCareerTick(t); } out.st = b.st; out.after = [j.status, j.why, j.claimedBy || null]; out.over = SHIP.notes.some(n => n.kind === 'sdLapsed' && n.over); } }
  else { for (let t = B2 + b.at; t <= B2 + b.at + 70; t += 5) { setShipNow(t); machinesNow(); worksCareerTick(t); } out.st = b.st; out.after = [j.status, j.why]; out.mail = SHIP.mail.some(x => /shutdown/i.test(x.subject) && /came and went|never came/.test(x.body)); out.settledMail = SHIP.mail.some(x => /shutdown/i.test(x.subject) && /Settled/.test(x.body)); }
  out.sd = JSON.stringify({ done: SHIP.works.sd.done, miss: SHIP.works.sd.miss }); out.use = W.use.m18; out.xp = W.xp;
  out.notes = [...new Set(SHIP.notes.filter(n => /^sd/.test(n.kind)).map(n => n.kind))]; out.grumble = SHIP.notes.some(n => n.kind === 'sdGrumble');
  return out;
})"""
SD_PLAN = r"""(() => {
  const out = {}, B = 17 * 1440;
  SHIP.works = null; SHIP.jobs = []; SHIP.occasions.length = 0; MACH_HOUR = null; MACH_SEEN = -1; WORKS_TICK.m = WORKS_TICK.h = -1;
  setShipNow(B + 600); machinesNow(); const W = worksInit(); W.tier = 3; W.rank = 'senior'; W.tr.m18 = 18;
  const id = jobReserve('6-junction-1', 18, 600, 43, { tier: 3 }); sdMark(shipNow());
  const sig = d => { const day = shipDay(d), a = []; for (const [pid, segs] of day.plans) a.push(pid + ':' + segs.map(s => s.from + '-' + s.to + '@' + s.placeId).join(',')); return a.join(';'); };
  const inMess = d => { let n = 0; for (const [pid, segs] of shipDay(d).plans) for (const s of segs) { const pl = s.placeId && placeById(s.placeId); if (pl && pl.deck === 3 && pl.room === 'M' && s.act !== 'work' && s.from < (d - 1) * 1440 + 1140 && (d - 1) * 1440 + 1080 < s.to) n++; } return n; };
  out.messBefore = inMess(19); const s0 = sig(19);
  out.book = !!sdBook(id, 1080, 'galley', []); out.same = sig(19) === s0;
  for (let t = B + 610; t <= B + 1325; t += 5) { setShipNow(t); machinesNow(); worksCareerTick(t); }
  out.messAfter = inMess(19); const s1 = sig(19); out.changed = s1 !== s0;
  SHIP_DAYS.clear(); MACH_USE.clear(); out.again = sig(19) === s1;
  out.saved = JSON.stringify(SHIP.works.sd.set[19].map(x => [x.at, x.branch]));
  return out;
})()"""
def part_m18(g):
    a = g.ev(SD_RUN + '(false)'); b = g.ev(SD_RUN + '(true)'); a2 = g.ev(SD_RUN + '(false)'); o = g.ev(SD_RUN + "('over')")
    print(f"  m18: Day {a['day']}: steps {a['log']}, screen '{a['screen']}', badge {a['badge']}, quiet hour booked {a['booked']}, affected {a['keep0']} -> {a['keep1']} with the kept rooms; settled {a['set']}; Day 19: {a['before']} -> {a['atOpen']}; taken: {a['st1']} -> {a['st2']}, turned in {a['turnin']}, uses {a['use']}; notes {a['notes']}")
    print(f"  m18 missed: {b['st']}, the job {b['after']}, Mail {b['mail']}, {b['sd']}")
    check(a['trained'] == a['day'] and a['booked'] and a['booked'][0] == a['day'] + 1, f"m18: trained by the first booking for the next day ({a['trained']}, {a['booked']})")
    check(a['screen'].startswith('1. ') and 'junction' in a['screen'] and a['badge'] == 1, f"m18: the screen opens on the job, its badge ({a['screen']}, {a['badge']})")
    check(a['keep1'] <= a['keep0'], f"m18: keeping rooms on leaves no more people affected ({a['keep0']} -> {a['keep1']})")
    check(a['round'], "m18: the save's sd reads back the same (sdClean)")
    check(a['before'][0] == 'waiting' and a['atOpen'][0] == 'open' and any(x.startswith('sd:day:') and ' L1' in x for x in a['atOpen'][1]), f"m18: the booked hour opens the job with a level-1 arrow ({a['before']} -> {a['atOpen']})")
    check(a['st1'] == 'off' and a['st2'] == 'done' and a['turnin'] and a['use'] == 1 and json.loads(a['sd'])['done'] == [a['day'] + 1], f"m18: power off, back on, done ({a['st1']}, {a['st2']}, {a['sd']})")
    print(f"  m18 parts: open from 06:00 {a['morning']}; in the hour without the parts {a['st0']}, with them {a['st1']}; over the hour unfinished: {o['st']}, power back on {o['over']}, the job {o['after']}; Brennan asked {a['askB']}, grumbled {a['grumble']}")
    check(a['morning'] == 'open' and a['st0'] is None, f"m18: the job open from 06:00 for its parts; the power stays on till you have them ({a['morning']}, {a['st0']})")
    check(o['st1'] == 'off' and o['st'] == 'lapsed' and o['over'] and o['after'][0] == 'waiting' and o['after'][2] is None, f"m18: never off past the hour: back on, the job to book again ({o})")
    check(a['grumble'] == (a['askB'] and True), f"m18: Brennan grumbles only when the screen asked you to tell him ({a['askB']}, {a['grumble']})")
    check(b['settledMail'] and b['st'] == 'lapsed' and b['after'][0] == 'waiting' and b['mail'] and json.loads(b['sd'])['miss'] == [b['day'] + 1], f"m18: a missed hour lapses, says so and waits for a new booking ({b['st']}, {b['after']}, {b['mail']}, {b['sd']})")
    check(json.dumps(a, sort_keys=True) == json.dumps(a2, sort_keys=True), "m18: the same twice")
    p = g.ev(SD_PLAN)
    print(f"  m18 plan: diners in the mess 18:00-19:00 on Day 19: {p['messBefore']} before the settle, {p['messAfter']} after; booking alone changed nothing {p['same']}; changed at 22:00 {p['changed']}; fresh plan the same {p['again']}; settled {p['saved']}")
    check(p['book'] and p['same'] and p['changed'] and p['again'] and p['messBefore'] > 0 and p['messAfter'] == 0, f"m18: the booked hour in the crew's plans ({p})")
PARTS['m18'] = part_m18

# manifestRun (seat E1, 0.45.12; E2's team parts call it): two parts from their shelves to a machine's panel, held for
# you only; taken, every stop done in turn: the parts off the shelves once, delivered (j.delivered, the note), turned in;
# a second run nobody takes is withdrawn at its time; the Wednesday manifest still posts beside an open parts run
MRUN = r"""(() => {
  SHIP.works = null; SHIP.notes = []; SHIP.jobs = []; setShipNow(17 * 1440 + 600); machinesNow(); const W = worksInit(), out = {};
  SHIP.stores.filter = 3; SHIP.stores.pump = 3; SHIP.stores.lamp = 3;   // on the shelves (the lamp too, for the withdrawn run below: by Day 17 the crew's repairs and the visit's lamp job have used the shelf's lamps; EV1, 0.96.0)
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
M12 = r"""(() => {
  SHIP.works = null; SHIP.notes = []; SHIP.jobs = []; MACH_HOUR = null; MACH_SEEN = -1; setShipNow(11 * 1440 + 990); machinesNow(); ACT = null;   // the machines replayed from the start, whatever the part before left (BM8, 0.63.5)
  SHIP.jobs = SHIP.jobs.filter(j => !/^4-washer-[123]$/.test(j.machine || ''));   // the shift below is the only work on Washers 1-3 (patch 1 F: the replay can post a real Washer 3 job by Day 12, which the logbook and the night crew rightly take first)
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
  // a wait step keeps its start when you come back before it's ready (wsOf: the step under way, not a fresh one; TS3, a planted fault)
  { SHIP.player.wsteps = []; ACT = null; const j = { id: 'probe@w', title: 'Probe' }, st = { step: 'wait', places: [], how: 'wait', opts: { mins: 30 } }, t0 = shipNow();
    workStep(j, st, 5, null); const at1 = (wsFind(j.id, 5) || {}).at; setShipNow(t0 + 10); workStep(j, st, 5, null); const at2 = (wsFind(j.id, 5) || {}).at;
    out.wait = [at1 === t0, at2 === at1]; SHIP.player.wsteps = []; ACT = null; setShipNow(t0); }
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
    check(a.get('wait') == [True, True], f"side: a wait step keeps its start when you come back before it's ready ({a.get('wait')})")
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
 let W = reset(27 * 1440 + 300); const seen = new Map(); for (let t = 27 * 1440 + 360; t <= 48 * 1440 + 500; t += 10) { setShipNow(t); machinesNow(); for (const f of WORK_TICKS) f(t, false); for (const x of SHIP.jobs) if (x.kind === 'rewire') seen.set(x.id, x); }
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
 W = reset(28 * 1440 + 480); j = rewJob('4-junction-1', shipNow(), { key: 96 }); SHIP.jobs.push(j); out.held = leaveEnd(j) - 28 * 1440;   /* (BM19) Day 29, past the nights (Days 22-25 have no day shift with Step 6 on, any rank; lead 42) */
 tick(28 * 1440 + 490, 29 * 1440 + 900); out.crew = [j.status, j.doneBy !== 'you' && !!j.doneBy];
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

# ---- M19 power and relays (24v, mechanics seat A, S5-3): the lesson on Day 17 at 11:00 with its beats (an urgent notice at
# 10:30, a level 1 arrow and its ring line from 10:45); the conduit tester given once, whichever of M15 and M19 comes first
# (Calder's "You'll want this" only when it's new); then one job a week, 08:00 on a workday of yours, a relay swap or a
# battery cell check by the week; read, pick, swap, test: a wrong pick opens that stop again (never a fail); done puts the
# machine right and is a use; a repair of yours on a relay is a use too; stages at 3 and 6 uses; not taken, the crew's
# the next day; the save cleaned; the same twice
M19 = r"""(() => { const out = {}, W0 = JSON.stringify(SHIP.works), O0 = JSON.stringify(SHIP.occasions);
 const reset = t => { machinesNew(); SHIP.jobs = []; SHIP.flags = {}; SHIP.occasions.length = 0; SHIP.career = null;   /* (N6) the career afresh too: its misses and let-go day decide your workdays (playerShiftOn), so a run must not inherit the last one's */ MACH_HOUR = null; MACH_SEEN = -1; WORKS_TICK.m = WORKS_TICK.h = -1; setShipNow(t); machinesNow(); SHIP.works = null; const W = worksInit(t); W.tier = 3; W.rank = 'senior'; for (const r of CAREER_LADDER.slice(0, CAREER_LADDER.indexOf(ladderRow('m19')))) { W.tr[r.id] = 1; W.use[r.id] = 9; (W.op[1] = W.op[1] || []).push(r.id); } W.xp = 999; delete worksSide().pwrOk; worksSide().pwr = null; W.inc = { plan: {}, open: null }; return W; };
 const tick = (a, b, s = 10) => { for (let t = a; t <= b; t += s) { setShipNow(t); machinesNow(); worksCareerTick(t); } };
 // the lesson's beats on Day 17: asked at 06:00 for 11:00 in the relay room; the notice at 10:30, the level 1 arrow from 10:45
 const said = [], kn = promoNotice; promoNotice = (x, f) => said.push([Math.round(shipNow() % 1440), x]);
 let W = reset(16 * 1440 + 300); for (const k of ['m15', 'm17']) { delete W.tr[k]; delete W.use[k]; for (const d in W.op) W.op[d] = W.op[d].filter(x => x !== k); } delete W.tools.tester; tick(16 * 1440 + 350, 16 * 1440 + 600);   // a steady Senior: Rewiring and the lift roof not trained by hand (EP2's ladder order, B1's 24 core; RV20's M1)
 const c = W.cur, r = c && SHIP.occasions.find(x => x.key === c.occ); out.ask = c && r ? [c.id, c.st, r.at % 1440, r.deck, r.room, c.by] : null;
 tick(16 * 1440 + 601, 16 * 1440 + 646, 1); const e = GUIDE.list.find(x => x.id === 'm19:meet:17'); let g = null; try { g = e && e.goal(); } catch (x) { g = null; }
 out.notice = said.slice(); out.arrow = e ? [e.level, e.from % 1440, g && g.deck, g && g.room, g && g.label] : null;
 promoNotice = kn;
 // the tester: new with M19 (Calder's line), or already M15's (no second one)
 const teach = []; const kt = worksTeach; worksTeach = (m, w, k, f) => { teach.push(m + '.' + k); return f; };
 W.cur = { id: 'm19', st: 'do', d: 17, by: 'calder', occ: null, j: null, w: 0 }; worksTrained('m19'); simFlush(); out.tester = [hasTool('tester'), teach.slice()]; out.fold = [W.tr.m15 === W.tr.m19, worksOpened(W).has('m15')];
 W = reset(16 * 1440 + 300); W.tr.m15 = 17; toolGive('tester'); const day0 = W.tools.tester[0]; W.cur = { id: 'm19', st: 'do', d: 17, by: 'calder', occ: null, j: null, w: 0 }; teach.length = 0; worksTrained('m19'); simFlush();
 out.tester2 = [W.tools.tester[0] === day0, teach.slice(), Object.keys(W.tools).filter(k => k === 'tester').length];
 worksTeach = kt;
 // the weeks: one job a week from the week after the lesson, 08:00 on a workday of yours, relay and battery by turns
 W = reset(17 * 1440 + 300); W.tr.m19 = 17; const seen = new Map();
 for (let t = 17 * 1440 + 360; t <= 38 * 1440 + 500; t += 10) { setShipNow(t); machinesNow(); for (const f of WORK_TICKS) f(t, false); for (const x of SHIP.jobs) if (/^(relayswap|battcell)$/.test(x.kind)) seen.set(x.id, x); }
 out.weeks = [...seen.values()].map(x => [worksDay(x.posted), weekday(worksDay(x.posted)), Math.round(x.posted % 1440), x.kind, machineById(x.machine).kind, jobTier(x)]);
 // a relay swap: read, a wrong pick (opens again), the right pick, swap, test; the machine put right; a use
 W = reset(19 * 1440 + 480); W.tr.m19 = 17; W.use.m19 = 0; const rel = machineList().find(m => m.kind === 'relay' && panelPlace(m.id));
 let j = pwrJob('relayswap', rel.id, shipNow(), { key: 91 }); SHIP.jobs.push(j); SHIP.machines[rel.id].cond = 30;
 out.board = !!openJobs().find(x => x.id === j.id); out.claimed = claimJob(j.id); let S = jobStops(j); out.stops = S.map(s => s.step + ':' + s.how);
 out.early = jobStepDone(j.id, 1, { pick: 'x' + j.bad }).ok; jobStepDone(j.id, 0, {});
 out.wrong = jobStepDone(j.id, 1, { pick: 'x' + ((j.bad + 1) % 6) }); out.right = jobStepDone(j.id, 1, { pick: 'x' + j.bad }).ok;
 jobStepDone(j.id, 2, {}); out.test = jobStepDone(j.id, 3, {}).ok; out.turnin = turnInJob(j.id);
 out.after = [SHIP.machines[rel.id].cond >= 90, W.use.m19, worksSide().pwr.done, worksSide().pwr.wrongs, j.rightFirst];
 // a battery cell check, right first time
 const bat = machineList().find(m => m.kind === 'battery' && panelPlace(m.id)); j = pwrJob('battcell', bat.id, shipNow(), { key: 92 }); SHIP.jobs.push(j); claimJob(j.id); S = jobStops(j);
 S.forEach((s, k) => jobStepDone(j.id, k, s.step === 'pick' ? { pick: 'x' + j.bad } : {})); out.batt = [S.map(s => s.step + ':' + s.how).join(' '), (S[1].opts.options || []).length, turnInJob(j.id), j.rightFirst, W.use.m19];
 // an ordinary repair of yours on a relay counts; stages at 3 and 6
 const rj = { id: 'pwr-test-repair', machine: rel.id, deck: rel.deck, kind: 'repair', urgency: 1, posted: shipNow(), found: shipNow(), claimedBy: 'you', status: 'done', doneBy: 'you', parts: [] }; SHIP.jobs.push(rj);
 simNote('job', { step: 'turnin', id: rj.id, t: shipNow(), machine: rel.id, job: 'repair' }); simFlush(); out.repairUse = W.use.m19;
 out.stages = [0, 2, 3, 5, 6].map(n => { W.use.m19 = n; return worksStage('m19'); });
 // not taken: the crew's the next day
 // (N6: Days 18-19, a Thursday and Friday before Step 6's nights; Day 23 has no day shift with P5_NIGHT on, and a later
 // pair ran the weekly plan into a week the second run then saw)
 W = reset(17 * 1440 + 480); W.tr.m19 = 17; j = pwrJob('relayswap', rel.id, shipNow(), { key: 93 }); SHIP.jobs.push(j); out.held = leaveEnd(j) - 17 * 1440;
 for (let t = 17 * 1440 + 490; t <= 18 * 1440 + 900; t += 10) { setShipNow(t); machinesNow(); for (const f of WORK_TICKS) f(t, false); } out.crew = [j.status, j.doneBy !== 'you' && !!j.doneBy];
 worksSide().pwr = { done: 'x', wrongs: -4 }; delete worksSide().pwrOk; out.save = JSON.stringify(pwrState()); worksSide().pwr = { done: 3, wrongs: 1, week: 4 }; delete worksSide().pwrOk; out.save2 = JSON.stringify(pwrState());
 SHIP.works = JSON.parse(W0); SHIP.occasions.length = 0; for (const o of JSON.parse(O0)) SHIP.occasions.push(o); SHIP.jobs = []; return out; })()"""
def part_m19(g):
    a, b = g.ev(M19), g.ev(M19)
    print('  m19 ask', a['ask'], 'notice', a['notice'], 'arrow', a['arrow'])
    print('  m19 tester', a['tester'], a['tester2'], 'weeks', a['weeks'])
    print('  m19 stops', a['stops'], 'wrong', a['wrong'], 'after', a['after'], 'batt', a['batt'], 'repair use', a['repairUse'], 'stages', a['stages'], 'held', a['held'], 'crew', a['crew'])
    check(a['ask'] and a['ask'][:6] == ['m19', 'meet', 660, 1, 'u', 'calder'], f"m19: a steady Senior (Rewiring and the lift roof untrained) asked on Day 17 for 11:00 in the relay room, Deck 1, with Calder ({a['ask']}; another lesson first means 24 core's ladder order, B1's, isn't in this build)")
    check(len(a['notice']) == 1 and a['notice'][0][0] == 630 and 'Power and relays' in a['notice'][0][1], f"m19: one urgent notice at 10:30 naming it ({a['notice']})")
    check(a['arrow'] and a['arrow'][0] == 1 and a['arrow'][1] == 645 and a['arrow'][2] == 1 and a['arrow'][3] == 'u' and a['arrow'][4].startswith('Power and relays with Calder, 11:00'), f"m19: a level 1 arrow from 10:45 to the relay room, its ring line naming it ({a['arrow']})")
    check(a.get('fold') == [True, True], f"m19: Rewiring folds into it: trained (and counted open) with it ({a.get('fold')})")
    check(a['tester'][0] and a['tester'][1] == ['m19.tester'], f"m19: the tester given with the lesson, Calder's word with it ({a['tester']})")
    check(a['tester2'][0] and a['tester2'][1] == [] and a['tester2'][2] == 1, f"m19: M15 gave it first: no second tester, no word ({a['tester2']})")
    W = a['weeks']
    check(3 <= len(W) <= 4 and all(e[0] > 17 and e[1] <= 4 and e[2] == 480 and e[5] == 3 for e in W), f"m19: one a week after the lesson, 08:00 on a weekday, Tier 3 ({W})")
    check(all((e[3] == 'relayswap') == (e[4] == 'relay') for e in W) and {e[3] for e in W} == {'relayswap', 'battcell'}, f"m19: relay swaps and battery checks by turns, each on its own kind of machine ({W})")
    check(a['board'] and a['claimed'] and not a['early'], "m19: offered to a Senior Officer; read before you pick")
    check(a['stops'] == ['read:look', 'pick:choose', 'swap:hold', 'test:look'], f"m19: the steps ({a['stops']})")
    check(a['wrong'].get('retry') and a['right'] and a['test'] and a['turnin'], f"m19: a wrong pick opens the stop again, the right one goes on ({a['wrong']})")
    check(a['after'] == [True, 1, 1, 1, False], f"m19: done puts the relay right, a use, the wrong pick kept (not right first time) ({a['after']})")
    check(a['batt'][0] == 'read:look pick:choose swap:hold test:look' and a['batt'][1] == 4 and a['batt'][2] and a['batt'][3] is True and a['batt'][4] == 2, f"m19: a battery check, four pairs of cells, right first time ({a['batt']})")
    check(a['repairUse'] == 3, f"m19: a repair of yours on a relay counts as a use ({a['repairUse']})")
    check(a['stages'] == [0, 0, 1, 1, 2], f"m19: stages at 3 and 6 uses ({a['stages']})")
    check(a['held'] == 1440 + 600 and a['crew'] == ['done', True], f"m19: not taken, the crew's the next day ({a['held']}, {a['crew']})")
    check(json.loads(a['save']) == {'done': 0, 'wrongs': 0, 'week': -1} and json.loads(a['save2']) == {'done': 3, 'wrongs': 1, 'week': 4}, 'm19: the save read back, junk cleaned')
    if json.dumps(a, sort_keys=True) != json.dumps(b, sort_keys=True): print('  m19 differs in:', [k for k in a if json.dumps(a.get(k), sort_keys=True) != json.dumps(b.get(k), sort_keys=True)], {k: (a.get(k), b.get(k)) for k in a if json.dumps(a.get(k), sort_keys=True) != json.dumps(b.get(k), sort_keys=True)})
    check(json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True), 'm19: differs the second time')
# turn 2: stage 2's conduit runs (the tester's reading, a wrong feed opens it again, the note for P5), the weeks with
# them joining at 3 uses, the power line and its fault rows, and the Senior's part of the Wednesday drill (posted at
# 14:50 for a Senior trained in M19, three calls in order, a wrong one opens again, the crew answer, the all-clear at
# 15:15; none for an Officer)
M19B = r"""(() => { const out = {}, W0 = JSON.stringify(SHIP.works);
 const reset = t => { machinesNew(); SHIP.jobs = []; SHIP.flags = {}; SHIP.notes = []; MACH_HOUR = null; MACH_SEEN = -1; WORKS_TICK.m = WORKS_TICK.h = -1; setShipNow(t); machinesNow(); SHIP.works = null; const W = worksInit(t); W.tier = 3; W.rank = 'senior'; W.tr.t3 = 15; W.tr.m19 = 17; W.use.m19 = 3; toolGive('tester'); delete worksSide().pwrOk; worksSide().pwr = null; W.inc = { plan: {}, open: null }; return W; };
 // the line and the faults
 out.line = [lineOn('power'), lineOf('5-inverter-1'), lineOf('6-junction-2'), JSON.stringify(lineDecks('power', '6-conduit-1')), JSON.stringify(lineDecks('power', '2-junction-1')), (linePath('power', '1-junction-1') || []).length];
 out.faults = ['battery', 'inverter', 'conduit', 'junction', 'powerjunction'].map(k => [k, (FAULT_CAUSES[k] || []).length, (FAULT_CAUSES[k] || []).some(c => c.line === 'power'), (FAULT_CAUSES[k] || []).every(c => !c.part || (STOCK && Object.prototype.hasOwnProperty.call(STOCK, c.part)))]);
 out.symptom = SYMPTOM_TEXT.power || null;
 // a conduit run: open, the tester's readings, a wrong feed, the right one, tag; the conduit right, a use, the note
 let W = reset(22 * 1440 + 480); const n0 = W.use.m19; let j = runJob('conduitrun', '6-conduit-1', shipNow(), { key: 81 }); SHIP.jobs.push(j); SHIP.machines['6-conduit-1'].cond = 30;
 out.runBoard = !!openJobs().find(x => x.id === j.id); claimJob(j.id); let S = jobStops(j); out.runStops = S.map(s => s.step + ':' + s.how); out.runOpts = (S[1].opts.options || []).map(o => o.label); out.runText = S[1].opts.text;
 jobStepDone(j.id, 0, {}); out.runWrong = !!jobStepDone(j.id, 1, { pick: 'x' + ((j.bad + 1) % 3) }).retry; out.runRight = jobStepDone(j.id, 1, { pick: 'x' + j.bad }).ok; jobStepDone(j.id, 2, {});
 out.runTurnin = turnInJob(j.id); simFlush(); out.runAfter = [SHIP.machines['6-conduit-1'].cond >= 90, W.use.m19 - n0, simNotes('conduitRun', 0).filter(x => x.id === j.id).map(x => x.deck)[0]];
 // the weeks from 3 uses: conduit runs join
 W = reset(17 * 1440 + 300); const seen = new Map();
 for (let t = 17 * 1440 + 360; t <= 38 * 1440 + 500; t += 10) { setShipNow(t); machinesNow(); for (const f of WORK_TICKS) f(t, false); for (const x of SHIP.jobs) if (/^(relayswap|battcell|conduitrun)$/.test(x.kind)) seen.set(x.id, x); }
 out.weeks = [...seen.values()].map(x => x.kind); out.stage2 = flag('m19.stage2') || null;
 // the Senior's drill on a Wednesday
 let wed = 22; while (weekday(wed) !== 2 || !playerShiftOn(wed)) wed++;
 W = reset((wed - 1) * 1440 + 800); const said = [], ks = worksSay; worksSay = (who, x) => said.push(who + ': ' + x);
 for (let t = (wed - 1) * 1440 + 840; t <= (wed - 1) * 1440 + 892; t += 1) { setShipNow(t); machinesNow(); worksCareerTick(t); }
 j = pdrillJobOf(wed); out.drill = j ? [j.claimedBy, Math.round(j.found % 1440), j.drill, jobStops(j).length, jobStops(j)[0].how] : null;
 const g = GUIDE.list.find(x => x.id === 'm19:drill:' + wed); let gg = null; try { gg = g && g.goal(); } catch (e) { gg = null; } out.drillArrow = g ? [g.level, gg && gg.label] : null;
 if (j) { out.drillEarly = !!jobStepDone(j.id, 1, { pick: 'c1' }).retry; out.drillWrong = !!jobStepDone(j.id, 0, { pick: 'c2' }).retry; [0, 1, 2].forEach(k => jobStepDone(j.id, k, { pick: 'c' + k })); out.drillDone = !!j.workDone; }
 for (let t = (wed - 1) * 1440 + 893; t <= (wed - 1) * 1440 + 920; t += 1) { setShipNow(t); machinesNow(); worksCareerTick(t); }
 out.drillEnd = j ? [j.status, j.doneBy, j.wrongs] : null; out.said = said.slice(); worksSay = ks;
 // an Officer gets none (24c's drill is the juniors'; an Officer has no part yet)
 W = reset((wed + 6) * 1440 + 800); W.rank = 'officer'; W.tier = 2; delete W.tr.m19; const w2 = wed + 7;
 for (let t = (w2 - 1) * 1440 + 840; t <= (w2 - 1) * 1440 + 900; t += 10) { setShipNow(t); machinesNow(); worksCareerTick(t); }
 out.officer = !!pdrillJobOf(w2);
 SHIP.works = JSON.parse(W0); SHIP.jobs = []; return out; })()"""
def part_m19b(g):
    a, b = g.ev(M19B), g.ev(M19B)
    print('  m19 line', a['line'], 'faults', a['faults'], 'symptom', a['symptom'])
    print('  m19 run', a['runStops'], a['runOpts'], a['runText'], 'after', a['runAfter'], 'weeks', a['weeks'], 'stage2 word', a['stage2'])
    print('  m19 drill', a['drill'], a['drillArrow'], 'end', a['drillEnd'], 'said', a['said'], 'officer', a['officer'])
    L = a['line']
    check(L[0] and L[1] == 'power' and L[2] == 'power' and L[3] == '[1,2,3]' and L[4] == '[2]' and L[5] == 4, f"m19: the power line (batteries, inverter, the conduits as branches, each deck's junction after) ({L})")
    check(all(f[1] >= 2 and f[2] and f[3] for f in a['faults']) and a['symptom'], f"m19: fault rows for the power kinds, some cutting the line, parts in stock ({a['faults']})")
    check(a['runBoard'] and a['runStops'] == ['open:look', 'test:choose', 'tag:hold'] and a['runOpts'] == ['Deck 1', 'Deck 2', 'Deck 3'] and 'Deck 2:' in a['runText'], f"m19: a conduit run, its feeds by the tester ({a['runStops']}, {a['runOpts']})")
    check(a['runWrong'] and a['runRight'] and a['runTurnin'] and a['runAfter'][0] and a['runAfter'][1] == 1 and a['runAfter'][2] in (1, 2, 3), f"m19: a wrong feed opens it again; done, the conduit right, a use, the note names the deck ({a['runAfter']})")
    check('conduitrun' in a['weeks'] and a['stage2'], f"m19: from 3 uses the conduit runs join the weeks, Calder says so once ({a['weeks']}, {a['stage2']})")
    d = a['drill']
    check(d and d[0] == 'you' and d[1] == 890 and d[3] == 3 and d[4] == 'choose', f"m19: the Senior's drill, yours at 14:50, three calls ({d})")
    check(a['drillArrow'] and a['drillArrow'][0] == 1 and a['drillArrow'][1] == 'Run the Works part of the drill', f"m19: a level 1 arrow with its ring line ({a['drillArrow']})")
    check(a.get('drillEarly') and a.get('drillWrong') and a.get('drillDone'), "m19: the calls in order; a wrong call opens it again")
    check(a['drillEnd'] == ['done', 'you', 1] and any(s.startswith('torres-zeke:') for s in a['said']) and any(s.startswith('halloran-emeka:') for s in a['said']), f"m19: the crew answer; the all-clear ends it ({a['drillEnd']})")
    check(a['officer'] is False, "m19: no Senior's drill for an Officer")
    check(json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True), 'm19 (turn 2): differs the second time: ' + str([(k, a[k], b.get(k)) for k in a if a[k] != b.get(k)][:3]))
def part_m19_all(g):
    part_m19(g); part_m19b(g)
PARTS['m19'] = part_m19_all

# 24x the sensor array (S5-5, B3; P5_M20): Day 19's ask (10:00 in the array room, Deck 2; Calder teaches, as Mori is off on
# Fridays, and Mori is booked in with her at the array's panel), the urgent notice at 09:30, the level 1 arrow from 09:45 with
# its ring line; a calibration job: pick a star (any of the three; your logged star among them), the dial (only settled
# counts), the rack's amber module, turned in: a use, the star saved; the weekly job (a full sweep, three dials, from 2
# uses); stage 3's word from Mori; the save read back, junk cleaned; the same twice
M20 = r"""(() => { const out = {};
 const reset = t => { machinesNew(); SHIP.jobs = []; SHIP.flags = {}; SHIP.notes = []; SHIP.mail = []; SHIP.occasions.length = 0; if (SHIP.device) SHIP.device.appts = []; MACH_HOUR = null; MACH_SEEN = -1; WORKS_TICK.m = WORKS_TICK.h = -1;
   for (const e of guideList()) if (/^m20:/.test(e.id)) guideDrop(e.id); setShipNow(t); machinesNow(); SHIP.works = null; const W = worksInit(); W.log.push(['x', 1, 0, 'service']); W.tier = 3; W.rank = 'senior';
   for (const r of CAREER_LADDER) if (r.id !== 'm20') { W.tr[r.id] = 1; W.use[r.id] = 9; (W.op[1] = W.op[1] || []).push(r.id); } return W; };
 // the ask and the beats
 let W = reset(18 * 1440 + 300); const notes = [], pn = promoNotice; promoNotice = (text) => notes.push([Math.floor(shipNow()) % 1440, text]);
 try { for (let t = 18 * 1440 + 300; t <= 18 * 1440 + 598; t += 1) { setShipNow(t); machinesNow(); worksCareerTick(t); if (DIALOGUE && typeof dialogueEnd === 'function') dialogueEnd(true); } } finally { promoNotice = pn; }
 const c = W.cur, r = c && SHIP.occasions.find(x => x.key === c.occ), g = guideList().find(e => /^m20:meet:/.test(e.id)), ap = (SHIP.device.appts || []).filter(a => r && (a.occ === r.key || a.occ === r.key + ':2'));
 out.ask = c && r ? [c.id, c.st, r.at % 1440, r.deck, r.room, c.by] : null; out.notice = notes;
 out.arrow = g ? [g.level, g.from % 1440] : null; out.mail = SHIP.mail.filter(x => /sensor array/i.test(x.subject)).map(x => Math.floor(x.at) % 1440); worksTrained('m20'); out.later = flag('m20.mori.later') || null; out.appt = ap.length ? [ap.flatMap(a => a.with).sort(), ap[0].at % 1440, [...new Set(ap.map(a => a.where))].length] : null;
 // a job of yours
 W = reset(22 * 1440 + 480); let j = arrJob(shipNow(), { key: 81 }); SHIP.jobs.push(j);
 out.board = !!openJobs().find(x => x.id === j.id); out.claimed = claimJob(j.id);
 let S = jobStops(j); out.stops = S.map(s => s.step + ':' + s.how); const opts = S[0].opts.options.map(o => o.id);
 out.badPick = jobStepDone(j.id, 0, { pick: 'zz' }).ok === true; out.pick = jobStepDone(j.id, 0, { pick: opts[1] }).ok;
 out.dialOff = jobStepDone(j.id, 1, { value: 2 }).ok === true; out.dialOn = jobStepDone(j.id, 1, { value: 0 }).ok;
 jobStepDone(j.id, 2, {}); jobStepDone(j.id, 3, {}); out.turnin = turnInJob(j.id); simFlush();
 const A = arrState(); out.after = [SHIP.machines['2-array-1'].cond >= 90, W.use.m20 || 0, A.star === S[0].opts.options[1].label, A.day];
 // your logged star among the three
 SHIP.works.side.cabin = SHIP.works.side.cabin || {}; const sd = starsData(); if (sd) { sd.n = 3; sd.last = 20; }
 out.yours = arrStars({ key: 81 }).map(o => o.label).includes(worksText('star.name', 'Wren {n}', { n: 3 }));
 // the weeks: one a week after the lesson, a full sweep from 2 uses, Mori's word from 4
 W = reset(18 * 1440 + 300); W.tr.m20 = 19; W.use.m20 = 0; (W.op[19] = ['m20']); const weeks = [];
 for (let t = 19 * 1440 + 300; t <= 40 * 1440; t += 60) { setShipNow(t); machinesNow(); worksCareerTick(t);
   for (const x of SHIP.jobs) if (x.kind === 'arraycal' && x.status !== 'done' && !x.seen) { x.seen = true; weeks.push([worksDay(x.posted), x.posted % 1440, !!x.sweep, (x.offs || []).length]); x.status = 'done'; x.doneAt = t; W.use.m20 = (W.use.m20 || 0) + 1; } }
 out.weeks = weeks; out.stages = [0, 2, 4].map(n => { W.use.m20 = n; return worksStage('m20'); });
 W.use.m20 = 4; j = arrJob(41 * 1440 + 480, { key: 99 }); SHIP.jobs.push(j); setShipNow(41 * 1440 + 490); claimJob(j.id);
 const said = []; const ws = worksTeach, wv = worksVoice; worksTeach = (m, who, k, fb) => { said.push(m + '.' + k); return fb; }; worksVoice = () => null;
 try { jobStops(j).forEach((s2, k) => jobStepDone(j.id, k, s2.how === 'turn' ? { value: 0 } : s2.how === 'choose' ? { pick: arrStars(j)[0].id } : {})); turnInJob(j.id); } finally { worksTeach = ws; worksVoice = wv; }
 out.survey = said;
 // the save: junk cleaned
 const side = SHIP.works.side; side.ar = { star: 7, sweeps: 'x', day: 3, week: 'y' }; delete side.arOk; out.save = JSON.stringify(arrState());
 return out; })()"""
def part_m20(g):
    a, b = g.ev(M20), g.ev(M20)
    print(f"  m20 ask {a['ask']}, notice {a['notice']}, arrow {a['arrow']}, appt {a['appt']}")
    print(f"  m20 job: stops {a['stops']}, after {a['after']}, your star listed {a['yours']}; weeks {a['weeks']}; stages {a['stages']}; stage 3 {a['survey']}; save {a['save']}")
    check(a['ask'] and a['ask'][:5] == ['m20', 'meet', 600, 2, 'A'], f"m20: asked on Day 19 for 10:00 in the array room, Deck 2 ({a['ask']})")
    check(len(a['notice']) == 1 and a['notice'][0][0] == 570 and 'sensor array' in a['notice'][0][1], f"m20: one urgent notice at 09:30 naming it ({a['notice']})")
    check(a['arrow'] == [1, 585], f"m20: a level 1 arrow from 09:45 ({a['arrow']})")
    check(a['appt'] and a['appt'][0] == ['calder'] and a['appt'][1] == 595, f"m20: Calder (Mori is off on Fridays) booked at the array's panel from 09:55; Mori not brought in on her day off ({a['appt']})")
    check(len(a['mail']) == 1 and a['mail'][0] >= 570, f"m20: one Mail, after the 09:30 notice (no Mail at the ask) ({a['mail']})")
    check(a['later'] == 1, f"m20: Mori's word saved for the next time you meet her ({a['later']})")
    check(a['board'] and a['claimed'], 'm20: a calibration job on the board for a Senior Officer, taken')
    check(a['stops'] == ['pick:choose', 'turn:turn', 'look:look', 'module:hold'], f"m20: the steps ({a['stops']})")
    check(not a['badPick'] and a['pick'] and not a['dialOff'] and a['dialOn'] and a['turnin'], f"m20: a star picked, only a settled dial counts, turned in")
    check(a['after'][:3] == [True, 1, True], f"m20: the array put right, a use, the star saved ({a['after']})")
    check(a['yours'], "m20: your last logged star is one of the three")
    W = a['weeks']
    check(len(W) >= 3 and all(e[1] == 480 for e in W) and not W[0][2] and W[0][3] == 1 and any(e[2] and e[3] == 3 for e in W), f"m20: one a week at 08:00, a full sweep (three dials) from 2 uses ({W})")
    check(a['stages'] == [0, 1, 2], f"m20: stages at 2 and 4 uses ({a['stages']})")
    check(a['survey'] == ['m20.survey'], f"m20: from 4 uses, Mori's word on Survey's chart ({a['survey']})")
    check(json.loads(a['save']) == {'star': None, 'sweeps': 0, 'day': 3, 'week': -1}, f"m20: the save read back, junk cleaned ({a['save']})")
    check(json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True), 'm20: differs the second time')
PARTS['m20'] = part_m20
# 28b M21 the Monday briefing (S6-2, MA6): on paper, Day 22 from 05:00 for a Senior Officer. Booked at 05:00 (the Captain
# and the chiefs on shift, a seat each at the conference table, 08:30 for 45 minutes), never through the ladder (W.cur
# stays the ladder's); the notice once you're up, the Mail after it, the hourly notice while you hold a job, the level 1
# arrow from 08:15; the meeting's three choices and what each does (a shutdown booked for tomorrow, or none to book; an
# inspection job held for you on your worst machine; the parts on the shelves on Thursday at 10:00); trained at the first;
# the short one the next Monday (20 minutes); a missed one keeps the full one; none for an Officer; the save cleaned.
M21 = r"""((k, opt) => {
  opt = opt || {};
  const out = { notices: [], mails: [], book: null, appt: null, arrow: null, cur: [], reply: [], effect: null };
  const reset = () => { SHIP.works = null; SHIP.occasions.length = 0; SHIP.notes = []; SHIP.flags = {}; SHIP.jobs = []; SHIP.mail = []; SHIP.device.appts.length = 0; MEETINGS.length = 0;
    MACH_HOUR = null; MACH_SEEN = -1; WORKS_TICK.m = WORKS_TICK.h = -1; if (typeof DIALOGUE !== 'undefined' && DIALOGUE) dialogueEnd(true); GUIDE.list = []; };
  reset();
  const pn = promoNotice; promoNotice = (text) => out.notices.push([shipNow() % 1440, text]);
  try {
    const d = opt.day || 22; setShipNow((d - 1) * 1440 + 240); machinesNow(); const W = worksInit(); W.tier = opt.tier || 3; W.rank = W.tier >= 3 ? 'senior' : 'officer';
    if (opt.first) m21State().first = opt.first;
    if (opt.held) { const m = machineList().find(x => !x.stub && x.deck === 4 && panelPlace(x.id)); SHIP.jobs.push({ id: 'held:x', machine: m.id, deck: 4, kind: 'repair', urgency: 0, posted: shipNow(), found: shipNow(), claimedBy: 'you', status: 'claimed', parts: [], start: shipNow() }); }
    if (opt.shut) SHIP.jobs.push({ id: 'shut:x', machine: '6-junction-1', deck: 6, kind: 'repair', urgency: 0, posted: shipNow(), found: shipNow(), claimedBy: null, status: 'waiting', shut: true, reserved: SD_SLOT, parts: [] });
    for (let m = 240; m <= 510; m++) {
      const t = (d - 1) * 1440 + m; setShipNow(t); worksCareerTick(t); occasionsTick(t);
      if (SHIP.works.cur) out.cur.push(SHIP.works.cur.id);
      const r = m21Rec(d); if (r && !out.book) out.book = [m, r.id, r.at % 1440, r.len, r.deck, r.room];
      if (!out.arrow && (GUIDE.list || []).some(x => x.id === 'm21:meet:' + d)) out.arrow = [(GUIDE.list.find(x => x.id === 'm21:meet:' + d)).level, m];
    }
    out.mails = SHIP.mail.filter(x => /briefing/i.test(x.subject || '')).map(x => [x.at % 1440, x.from, x.subject]);
    const r = m21Rec(d); if (!r) return out;
    const a = apptList().find(x => x.occ === r.key); out.appt = a ? [a.with.slice(), a.places || null, a.at % 1440, a.len] : null;
    const mt = MEETINGS.find(x => x.id === r.key); out.script = mt ? mt.script : null;
    if (opt.miss) { for (let m = 511; m <= 560; m++) { const t = (d - 1) * 1440 + m; setShipNow(t); worksCareerTick(t); occasionsTick(t); } out.status = r.status; out.tr = SHIP.works.tr.m21 === undefined ? null : SHIP.works.tr.m21; return out; }
    dialogueShow(mt.script, mt); r.met = true;
    for (let n = 0; n < 30 && DIALOGUE; n++) { const l = DIALOGUE.queue[DIALOGUE.i]; if (l.choice) { out.choices = l.choice.map(c => c.text); dialogueChoose(k); const nx = DIALOGUE.queue.slice(DIALOGUE.i); out.reply = nx.slice(0, 2).map(x => [x.who, typeof x.text === 'string' ? x.text : '']); } else dialogueNext(); }
    out.tr = SHIP.works.tr.m21 === undefined ? null : SHIP.works.tr.m21; out.side = JSON.parse(JSON.stringify(m21State()));
    out.op = Object.values(SHIP.works.op).flat().includes('m21');
    if (k === 0) { const b = sdPeek().book[0]; out.effect = b ? [b.day, b.at, b.branch, b.job] : null; }
    if (k === 1) { const j = SHIP.jobs.find(x => x.reserved === M21_SLOT); out.effect = j ? [j.m21, heldForYou(j), j.machine, Math.round((j.until - shipNow()) / 1440), !!j.cause] : null;
      const cond = id => SHIP.machines[id].cond; out.worst = j ? machineList().filter(x => !x.stub && SHIP.machines[x.id] && panelPlace(x.id) && !ENGINE_KINDS.has(x.kind) && jobTier({ machine: x.id }) <= playerTier() && x.id !== j.machine && !SHIP.jobs.some(y => y !== j && y.machine === x.id && y.status !== 'done')).every(x => cond(x.id) >= cond(j.machine)) : null; }
    if (k === 2) { const before = M21_PARTS.map(p => SHIP.stores[p] || 0); const seen = [];
      for (let h = (d - 1) * 24 + 10; h <= (d + 3) * 24; h++) { const t = h * 60; for (const f of WORK_TICKS) try { f(t, true); } catch (e) { } if (!seen.length && (SHIP.stores[M21_PARTS[0]] || 0) !== before[0]) seen.push([Math.floor(t / 1440) + 1, t % 1440]); }
      out.effect = [m21State().order, m21State().got, M21_PARTS.map((p, i) => (SHIP.stores[p] || 0) - before[i]), seen[0] || null, SHIP.mail.filter(x => x.from === 'Stores' && /parts order/i.test(x.subject)).length]; }
    return out;
  } finally { promoNotice = pn; }
})"""
M21_SAVE = r"""(() => { SHIP.works = null; setShipNow(21 * 1440 + 300); const W = worksInit(); W.side = { m21: { first: 'x', last: -4, pick: 7, order: 25.5, got: 3, sd: null, junk: 1 } }; return JSON.stringify(m21State()); })()"""
def part_m21(g):
    on = g.ev("typeof P5_M21 !== 'undefined' && P5_M21 && typeof m21Raise === 'function'")
    if not on: print('  m21: not in this build (P5_M21 off)'); return
    r = [g.ev(f"({M21})({k})") for k in range(3)]
    a = r[0]
    print(f"  m21 booked {a['book']}, appt {a['appt']}, notices {a['notices']}, Mail {a['mails']}, arrow {a['arrow']}, script {a['script']}")
    check(a['book'] and a['book'][:6] == [300, 'm21.brief', 510, 45, 1, 'O'], f"m21: Day 22's briefing booked at 05:00 for 08:30, 45 minutes, the observation room ({a['book']})")
    ap = a['appt'] or [[], {}, 0, 0]
    check(ap[0][:1] == ['marrow'] and {'vance', 'calder', 'sato', 'holt'} <= set(ap[0]) and ap[2] == 510 and ap[3] == 45, f"m21: the Captain, Vance and the chiefs at 08:30 ({ap})")
    check(ap[1] and all(ap[1].get(p, '').startswith('1-conf-') for p in ap[0]) and len(set(ap[1].values())) == len(ap[0]) and '1-conf-10' not in ap[1].values(), f"m21: a seat each at the table, yours (1-conf-10) left free ({ap[1]})")
    check('m21' not in a['cur'] and not a['op'], f"m21: never through the ladder ({set(a['cur'])}, opened {a['op']})")
    check(len(a['notices']) == 1 and a['notices'][0][0] == 360 and 'briefing' in a['notices'][0][1], f"m21: one notice once you're up, 06:00 ({a['notices']})")
    check(len(a['mails']) == 1 and a['mails'][0][0] >= 360, f"m21: one Mail, the record, after the notice ({a['mails']})")
    check(a['arrow'] == [1, 495], f"m21: a level 1 arrow from 08:15 ({a['arrow']})")
    check(a['choices'] and len(a['choices']) == 3, f"m21: three choices ({a.get('choices')})")
    check(a['tr'] == 22 and a['side']['first'] == 22, f"m21: trained at the first briefing ({a['tr']}, {a['side']})")
    print(f"  m21 shutdown, no job: {a['reply']}; worry: {r[1]['effect']} {r[1]['reply'][:1]}; parts: {r[2]['effect']} {r[2]['reply']}")
    check(a['effect'] is None and a['reply'] and a['reply'][0][0] == 'marrow', f"m21: a shutdown with no job waiting: approved, nothing booked ({a['effect']})")
    s = g.ev(f"({M21})(0, {{ shut: true }})")
    nt = g.ev("typeof P5_NIGHT !== 'undefined' && P5_NIGHT")
    print(f"  m21 shutdown with a job waiting: {s['effect']} {s['reply'][:1]}")
    check(s['effect'] and s['effect'][0] == 23 and s['effect'][1] == (1200 if nt else 600) and s['effect'][3] == 'shut:x', f"m21: the job waiting for a shutdown booked for tomorrow ({'20:00, before the night' if nt else '10:00'}) ({s['effect']})")
    w = r[1]['effect']
    check(w and w[0] == 22 and w[1] and w[3] == 3 and w[4] and r[1]['worst'], f"m21: the worry: an inspection job on your worst machine, held for you three days ({w}, worst {r[1]['worst']})")
    p = r[2]['effect']
    check(p and p[0] == 0 and p[1] == 25 and all(x == 2 for x in p[2]) and p[3] == [25, 600] and p[4] == 1, f"m21: the parts order on the shelves on Thursday (Day 25), two of each, Stores' Mail ({p})")
    h = g.ev(f"({M21})(2, {{ held: true }})")
    print(f"  m21 holding a job: notices {[n[0] for n in h['notices']]}")
    check([n[0] for n in h['notices']] == [360, 420, 480], f"m21: holding another job, a notice each hour till the briefing ({h['notices']})")
    n = g.ev(f"({M21})(2, {{ day: 29, first: 22 }})")
    check(n['book'] and n['book'][1:4] == ['m21.short', 510, 20], f"m21: the next Monday the short one, 08:30-08:50 ({n['book']})")
    m = g.ev(f"({M21})(2, {{ miss: true }})")
    check(m['status'] == 'missed' and m['tr'] is None, f"m21: missed: not trained ({m.get('status')}, {m.get('tr')})")
    m2 = g.ev(f"({M21})(2, {{ day: 29 }})")
    check(m2['book'] and m2['book'][1] == 'm21.brief', f"m21: after a missed first one, the full one again ({m2['book']})")
    o = g.ev(f"({M21})(2, {{ tier: 2 }})")
    check(o['book'] is None and not o['notices'], f"m21: none for an Officer ({o['book']})")
    t = g.ev(f"({M21})(1, {{ day: 23 }})")
    check(t['book'] is None, "m21: none on a Tuesday")
    dr = g.ev("(() => { const r = m21Door(); return r ? [r.deck, DECKS[1].map[r.tile[1]][r.tile[0]]] : null; })()")
    check(dr == [1, 'O'], f"m21: Calder's spot at the briefing's end (28a's night.on): a tile of the observation room by its way out ({dr})")
    sv = json.loads(g.ev(M21_SAVE))
    check(sv == {'first': 0, 'last': 0, 'pick': -1, 'order': 0, 'got': 3, 'sd': 0}, f"m21: the save read back, junk cleaned ({sv})")
    b = [g.ev(f"({M21})({k})") for k in range(3)]
    check(json.dumps(r, sort_keys=True) == json.dumps(b, sort_keys=True), 'm21: differs the second time')
PARTS['m21'] = part_m21
# 28d M24 leading a team (S6-6, MA6): on paper, night 3 (Day 24) for an Engine Specialist. The beats from 21:00 (the
# notice, the Mail after it, the level 1 arrows: pick, book, spots); the picks (Keane, the one engine tech aboard, says
# yes; a Watch rating "after my round", 20 minutes); booking only on the bridge and only with a team; the Watch's hour;
# spots that follow onto the job before the start and not after; a good team (Keane on the lifting frame, a ready Watch
# rating on the coupling) and quick calls finish early, a poor pick (both spots wrong) runs over the hour, never fails;
# not coming: Keane finishes it, not trained; trained by the first you led; Schedule rows; none for a Senior with the
# promotion on, none another day; the save cleaned; the same twice.
M24 = r"""((opt) => {
  opt = opt || {};
  const out = { notices: [], arrows: [] };
  SHIP.works = null; SHIP.notes = []; SHIP.flags = {}; SHIP.jobs = []; SHIP.mail = []; MACH_HOUR = null; MACH_SEEN = -1; WORKS_TICK.m = WORKS_TICK.h = -1; GUIDE.list = [];
  const pn = promoNotice; promoNotice = (text) => { if (/coil swap/i.test(text)) out.notices.push([shipNow() % 1440, text]); };   // (24u's own notices aside)
  try {
    const d = opt.day || 24; setShipNow((d - 1) * 1440 + 1250); machinesNow(); const W = worksInit(); W.tier = opt.tier || 4; W.rank = W.tier >= 4 ? 'specialist' : 'senior';
    for (const r of CAREER_LADDER) if (r.id !== 'm24') { W.tr[r.id] = 1; W.use[r.id] = 9; (W.op[1] = W.op[1] || []).push(r.id); }   // every other lesson done: nothing else asks tonight
    out.on = m24On(); out.crew = m24Crew();
    const n = d === 24 && m24Night() || { from: (d - 1) * 1440 + 1260 };
    const tick = (a, b) => { for (let t = a; t <= b; t++) { setShipNow(t); machinesNow(); worksCareerTick(t); for (const e of GUIDE.list || []) if (/^m24:/.test(e.id) && !out.arrows.some(x => x[0] === e.id)) out.arrows.push([e.id, e.level, t % 1440]); } };
    tick(n.from - 10, n.from + 5);
    out.mails = SHIP.mail.filter(x => /coil swap/i.test(x.subject)).map(x => [x.at % 1440, x.subject]);
    if (!out.on || d !== 24) return out;
    out.bookEarly = !!m24Book(shipNow(), true);
    const keane = 'keane-davi', rating = out.crew.find(id => id !== keane);
    out.said = [m24Pick(keane), m24Pick(rating)];
    out.notHere = !!m24Book(shipNow(), false);
    if (opt.good) { m24SpotSet(keane, 2); tick(shipNow() + 1, (m24State().ready[rating] || 0) + 1); }
    const j = m24Book(shipNow(), true); if (!j) return out;
    out.job = [j.start % 1440, j.start - shipNow() >= 45, j.team.slice().sort(), j.spots.you];
    out.spots0 = [j.spots[keane], j.spots[rating]]; out.sp = m24Spots();
    if (opt.swap) { m24SpotSet(keane, m24State().spots[keane] === 1 ? 2 : 1); out.spots1 = [j.spots[keane], j.spots[rating], j.seq.filter(s => s.part === 'lift')[0].who]; }
    tick(shipNow() + 1, j.start - 1);
    let t = j.start, calls = 0;
    for (; t < j.start + 240 && j.status !== 'done'; t++) { setShipNow(t); machinesNow(); worksCareerTick(t); if (!opt.away) { j.youIn = true;
      const mine = j.seq.map((s, i) => s.who === 'you' ? i : -1).filter(i => i >= 0), k = mine.indexOf(j.cur); if (k >= 0 && !(j.stepsDone || []).includes(k)) { jobStepDone(j.id, k, {}); calls++; } } }
    out.lateSpot = m24SpotSet(keane, 1);
    const S = m24State(); out.end = [j.status, S.mins, calls, S.done > 0, W.tr.m24 === undefined ? null : W.tr.m24, !!j.youOut];
    out.mailDone = SHIP.mail.filter(x => x.subject === 'The coil swap').length;
    return out;
  } finally { promoNotice = pn; }
})"""
M24_ITEMS = r"""(() => { SHIP.works = null; SHIP.jobs = []; setShipNow(23 * 1440 + 1250); const W = worksInit(); W.tier = 4; const a = m24Items(24).map(x => [x.from, x.title]);
  m24Pick('keane-davi'); m24Pick(m24Crew()[1]); const j = m24Book(shipNow(), true); const b = m24Items(24).concat(m24Items(25)).map(x => [x.from, x.title]); return [a, b, j && j.start % 1440]; })()"""
M24_SAVE = r"""(() => { SHIP.works = null; setShipNow(23 * 1440 + 300); const W = worksInit(); W.side = { m24: { day: 24, pick: ['keane-davi', 7, 'x'], said: { 'keane-davi': 'yes', x: 'maybe' }, ready: { a: -3, b: 40 }, slot: 'z', spots: { 'keane-davi': 2, y: 9 }, job: 5, done: 1.5, mins: 30 } }; return JSON.stringify(m24State()); })()"""
def part_m24(g):
    on = g.ev("typeof P5_M24 !== 'undefined' && P5_M24 && typeof m24Book === 'function'")
    if not on: print('  m24: not in this build (P5_M24 off)'); return
    good, poor = g.ev(f"({M24})({{ good: true }})"), g.ev(f"({M24})({{}})")
    a = good
    print(f"  m24 crew {a['crew']}, notices {a['notices']}, Mail {a['mails']}, arrows {a['arrows']}, said {a['said']}")
    print(f"  m24 good team: job {a.get('job')}, spots {a.get('spots0')}, end {a.get('end')}; poor pick: spots {poor.get('spots0')}, end {poor.get('end')}")
    check(a['on'] and a['crew'][:1] == ['keane-davi'] and len(a['crew']) >= 2, f"m24: Keane, then the night Watch ratings, to pick from ({a['crew']})")
    check(len(a['notices']) == 1 and a['notices'][0][0] == 1260 and 'coil swap' in a['notices'][0][1], f"m24: one notice as the night starts, 21:00 ({a['notices']})")
    check(len(a['mails']) == 1 and a['mails'][0][0] >= 1260, f"m24: one Mail, the record, after the notice ({a['mails']})")
    check(['m24:pick', 1, 1260] in a['arrows'], f"m24: a level 1 arrow to pick your team from 21:00 ({a['arrows']})")
    check(any(x[0] == 'm24:book' and x[1] == 1 for x in a['arrows']) and any(x[0] == 'm24:spots' and x[1] == 1 for x in a['arrows']), f"m24: level 1 arrows to book with the Watch and for the spots ({a['arrows']})")
    check(a['said'] == ['yes', 'later'], f"m24: Keane says yes, a Watch rating after their round ({a['said']})")
    check(not a['bookEarly'] and not a['notHere'], "m24: no booking before the team is picked, nor off the bridge")
    check(a.get('job') and a['job'][1] and a['job'][2] == sorted(['keane-davi', a['crew'][1]]), f"m24: the Watch's hour at least 45 minutes on, the two you picked ({a.get('job')})")
    sp = a.get('sp') or ['?', '?', '?']   # [the coupling, the lifting frame, yours]: S6-4's team spots with P5_DECK6, else the engine places
    check(a.get('spots0') == [sp[1], sp[0]] and poor.get('spots0') == [sp[0], sp[1]] and a['job'][3] == sp[2], f"m24: the spots on the job as you gave them, yours the drive panel's ({a.get('spots0')}, {poor.get('spots0')}, {sp})")
    e, p = a.get('end') or [], poor.get('end') or []
    check(e[:1] == ['done'] and e[1] <= 55 and e[2] == 6 and e[3] and e[4] == 24, f"m24: a good team and quick calls: done early (55 minutes or less), six calls, trained ({e})")
    check(p[:1] == ['done'] and p[1] > 60 and p[3], f"m24: a poor pick runs over the hour, and is still done ({p})")
    check(not a['lateSpot'], "m24: no spot change once the run has started")
    check(a['mailDone'] == 1, f"m24: one Mail at the end ({a['mailDone']})")
    s = g.ev(f"({M24})({{ swap: true }})")
    check(s.get('spots1') and s['spots1'][0] == (s.get('sp') or [None, None])[1] and s['spots1'][2] == 'keane-davi', f"m24: a spot changed before the start: the job follows ({s.get('spots1')})")
    w = g.ev(f"({M24})({{ away: true }})")
    print(f"  m24 not coming: {w.get('end')}")
    check(w.get('end') and w['end'][0] == 'done' and w['end'][5] and w['end'][4] is None, f"m24: not there: Keane finishes it, not trained ({w.get('end')})")
    o = g.ev(f"({M24})({{ tier: 3 }})")
    check(not o['on'] and not o['notices'] and not o['arrows'], "m24: none for a Senior Officer (the promotion's on)")
    o2 = g.ev(f"({M24})({{ day: 23 }})")
    check(not o2['notices'] and not o2['arrows'] and not o2['mails'], f"m24: nothing on another night ({o2})")
    it = g.ev(M24_ITEMS)
    check(it[0] and it[0][0][1].startswith('Plan the coil swap') and any('coil swap' in x[1] and x[0] == it[2] for x in it[1]), f"m24: Schedule rows: the planning, then the slot ({it})")
    cl = g.ev("(() => { SHIP.works = null; setShipNow(24 * 1440 + 100); const W = worksInit(); W.tier = 4; const S = m24State(); S.pick = ['keane-davi']; S.ready = { 'keane-davi': 0 }; return [m24SlotFor(24 * 1440 + 30) % 1440, m24SlotFor(24 * 1440 + 60) % 1440]; })()")
    check(cl[0] == 75 and cl[1] == 210, f"m24: the Watch's hour keeps clear of night 3's incident, 02:30-03:30 (booked at 00:30: 01:15 = {cl[0]}; at 01:00, 01:45 would cross it, so 03:30 = {cl[1]})")
    sv = json.loads(g.ev(M24_SAVE))
    check(sv == {'day': 24, 'pick': ['keane-davi', 'x'], 'said': {'keane-davi': 'yes'}, 'ready': {'b': 40}, 'slot': 0, 'spots': {'keane-davi': 2}, 'job': None, 'done': 0, 'mins': 30}, f"m24: the save read back, junk cleaned ({sv})")
    good2 = g.ev(f"({M24})({{ good: true }})")
    check(json.dumps(good, sort_keys=True) == json.dumps(good2, sort_keys=True), 'm24: differs the second time')
PARTS['m24'] = part_m24

# m23 (S6-5, DA6; 28c's own nights, never through the ladder): night 1 with Reyes on Day 22 from 22:45: the job yours as
# the night starts (a side job), one notice, every stop in order (a wrong loop is looked at again, coil 2 can't be settled
# before coil 1), the coil serviced, the Mail; nothing for a Senior Officer (the promotion on) nor on another night
M23 = r"""((opt) => {
  opt = opt || {};
  const out = { notices: [], steps: [] };
  SHIP.works = null; SHIP.notes = []; SHIP.flags = {}; SHIP.jobs = []; SHIP.mail = []; MACH_HOUR = null; MACH_SEEN = -1; WORKS_TICK.m = WORKS_TICK.h = -1; GUIDE.list = [];
  const pn = promoNotice; promoNotice = (text) => { if (/Reyes|reactor|permit|badge/i.test(text)) out.notices.push([shipNow() % 1440, text]); };
  try {
    const d = opt.day || 22; setShipNow((d - 1) * 1440 + 1350); machinesNow(); const W = worksInit(); W.tier = opt.tier || 4; W.rank = W.tier >= 4 ? 'specialist' : 'senior';
    for (const r of CAREER_LADDER) if (r.id !== 'm23') { W.tr[r.id] = 1; W.use[r.id] = 9; (W.op[1] = W.op[1] || []).push(r.id); }
    out.on = m23On(d);
    for (let t = shipNow(); t <= (d - 1) * 1440 + 1375; t++) { setShipNow(t); machinesNow(); worksCareerTick(t); }
    const j = SHIP.jobs.find(x => x.kind === 'm23night'); out.job = j ? [j.claimedBy, j.status, j.start % 1440, j.coil] : null;
    out.arrowBefore = !!SHIP.works.ns && (GUIDE.list || []).some(e => e.id === 'm23:n1');   // S6-1's clock-in first
    if (SHIP.works.ns) { SHIP.works.ns[d] = Object.assign(SHIP.works.ns[d] || {}, { in: shipNow() }); setShipNow(shipNow() + 1); machinesNow(); worksCareerTick(shipNow()); }
    const ar = (GUIDE.list || []).find(e => e.id === 'm23:n1'), g0 = ar && ar.goal(); out.arrow = ar ? [ar.level, g0 && g0.place] : null;
    if (!j || opt.day) return out;
    const stops = jobStops(j); out.n = stops.length; out.mine = !!myJob() === false;
    out.early = jobStepDone(j.id, 2, {}).ok;              // out of order
    out.balEarly = jobStepDone(j.id, stops.length - 1, { value: 0 }).ok;   // coil 2 before coil 1
    for (let k = 0; k < stops.length; k++) {
      const st = stops[k], tag = st.step || st.tag;
      if (tag === 'loop') { const bad = 'l' + ((j.loop + 1) % 3); out.wrong = jobStepDone(j.id, k, { pick: bad }); }
      if (tag === 'bal0') { out.gauge0 = st.opts.gauge(); out.balTurn = st.opts.onTurn(1); out.balOk = [st.opts.ok(1), st.opts.ok(0)]; st.opts.onTurn(0); }
      if (tag === 'bal1') { out.gauge1 = jobStops(j)[k].opts.gauge(); jobStops(j)[k].opts.onTurn(0); }
      const r = jobStepDone(j.id, k, tag === 'loop' ? { pick: 'l' + j.loop } : tag.startsWith('bal') ? { value: 0 } : {});
      out.steps.push([tag, r.ok]);
      setShipNow(shipNow() + 5); machinesNow(); worksCareerTick(shipNow());
    }
    const S = m23State(); out.end = [j.status, !!j.workDone, S.d1 > 0, (SHIP.machines[j.coil] || {}).cond >= 96, j.wrongs];
    out.mails = SHIP.mail.filter(x => /Night 1/.test(x.subject)).length;
    return out;
  } finally { promoNotice = pn; }
})"""
def part_m23(g):
    on = g.ev("typeof P5_M23 !== 'undefined' && P5_M23 && typeof m23Post === 'function'")
    if not on: print('  m23: not in this build (P5_M23 off)'); return
    a = g.ev(f"({M23})({{}})")
    print(f"  m23 night 1: on {a['on']}, job {a.get('job')}, notices {a['notices']}, {a.get('n')} stops {a.get('steps')}, end {a.get('end')}, Mail {a.get('mails')}")
    print(f"  m23 balance: {a.get('gauge0')!r} -> {a.get('balTurn')!r}; then {a.get('gauge1')!r}")
    check(a['on'] and a.get('job') and a['job'][0] == 'you' and a['job'][1] == 'claimed' and a['job'][2] == 1365, f"m23: night 1's job yours as the night starts, 22:45 ({a.get('job')})")
    check(a.get('mine'), "m23: a side job (your board job, if any, stays yours)")
    check(not a.get('arrowBefore'), "m23: no arrow of ours before you've clocked in for the night (S6-1's arrow leads)")
    check(a.get('arrow') == [1, a['job'][3] + '-svc'], f"m23: a level 1 arrow to the coil's panel, the first stop (a side job has no job pointer) ({a.get('arrow')})")
    check(len(a['notices']) == 1 and a['notices'][0][0] == 1365, f"m23: one notice as the night starts ({a['notices']})")
    check(a.get('n') == 11 and all(ok for _, ok in a['steps']), f"m23: eleven stops, each done in order ({a.get('steps')})")
    check(not a.get('early'), "m23: a stop can't be done before the one before it")
    check(a.get('wrong') and a['wrong'].get('retry'), f"m23: a wrong loop is looked at again, never a fail ({a.get('wrong')})")
    check(a.get('balEarly') is False and a.get('balOk') == [False, True], f"m23: coil 2 waits for coil 1; settled at 0 ({a.get('balEarly')}, {a.get('balOk')})")
    check(a.get('gauge0') != a.get('balTurn') and a['gauge0'].split('. ')[1] != a['balTurn'].split('. ')[1], f"m23: turning coil 1 moves coil 2's reading too ({a.get('gauge0')!r} -> {a.get('balTurn')!r})")
    e = a.get('end') or []
    check(e[:4] == ['done', True, True, True] and e[4] == 1, f"m23: done where you finish it, night 1 logged, the coil serviced ({e})")
    check(a.get('mails') == 1, f"m23: one Mail, the record ({a.get('mails')})")
    o = g.ev(f"({M23})({{ tier: 3 }})")
    check(not o['on'] and not o['job'] and not o['notices'], f"m23: none for a Senior Officer (the promotion's on) ({o})")
    o2 = g.ev(f"({M23})({{ day: 24 }})")
    check(not o2['job'] and not o2['notices'], f"m23: nothing on night 3 ({o2})")

# night 2 (Day 23 from 21:00): the door shut without a permit (and without a badge, and before the Watch is told), each
# step's arrow in order, the cards' steps, the visit, the Watch's word when the badge isn't back after half an hour,
# trained and the Mail once it is
M23N2 = r"""((opt) => {
  opt = opt || {};
  const out = { notices: [], arrows: [], door: {} };
  SHIP.works = null; SHIP.notes = []; SHIP.flags = {}; SHIP.jobs = []; SHIP.mail = []; MACH_HOUR = null; MACH_SEEN = -1; WORKS_TICK.m = WORKS_TICK.h = -1; GUIDE.list = [];
  DOSI = { out: null, mesh: [] };
  const pn = promoNotice; promoNotice = (text, from) => { if (/reactor|permit|badge|Watch/i.test(text)) out.notices.push([shipNow() % 1440, from || '', text.slice(0, 40)]); };
  const dc = deviceChoose; deviceChoose = () => false;   // the cards are played by calling their steps here (controller_check plays them by pad)
  try {
    const d = 23; setShipNow((d - 1) * 1440 + 1200); machinesNow(); const W = worksInit(); W.tier = 4; W.rank = 'specialist';
    for (const r of CAREER_LADDER) if (r.id !== 'm23') { W.tr[r.id] = 1; W.use[r.id] = 9; (W.op[1] = W.op[1] || []).push(r.id); }
    const tick = (a, b) => { for (let t = a; t <= b; t++) { setShipNow(t); machinesNow(); worksCareerTick(t); for (const e of GUIDE.list || []) if (/^m23:/.test(e.id) && !out.arrows.some(x => x[0] === e.id)) out.arrows.push([e.id, e.level, t % 1440]); } };
    const door = () => doorOpenFor('R', 'player', shipNow(), 6);
    tick(shipNow(), (d - 1) * 1440 + 1265);
    out.door.none = door();
    dosiUse(); out.door.badgeOnly = door(); dosiUse();      // a badge, no permit: still shut
    out.tellEarly = m23Tell(shipNow(), false);
    m23Permit(shipNow()); tick(shipNow() + 1, shipNow() + 3);
    out.door.permitOnly = door();
    out.tellNoBadge = m23Tell(shipNow(), false);
    dosiUse(); tick(shipNow() + 1, shipNow() + 3);
    out.door.notTold = door();
    m23Tell(shipNow(), true);                               // out before in: nothing
    m23Tell(shipNow(), false); tick(shipNow() + 1, shipNow() + 3);
    out.door.told = door();
    const S = m23State(), j = SHIP.jobs.find(x => x.id === S.j2); out.job = j ? [j.claimedBy, j.status, jobStops(j).length] : null;
    if (j) for (let k = 0; k < jobStops(j).length; k++) { jobStepDone(j.id, k, {}); tick(shipNow() + 1, shipNow() + 2); }
    out.outEarly = !!S.out;
    m23Tell(shipNow(), true); tick(shipNow() + 1, shipNow() + 2);
    out.door.outside = door();
    tick(shipNow() + 1, shipNow() + (opt.late ? 35 : 5));
    out.word = S.word > 0;
    dosiUse(); tick(shipNow() + 1, shipNow() + 2);
    out.end = [S.d2 > 0, W.tr.m23 === undefined ? null : W.tr.m23, SHIP.mail.filter(x => x.subject === 'The reactor').length, j && j.status];
    out.step = m23Night2Step(S);
    return out;
  } finally { promoNotice = pn; deviceChoose = dc; }
})"""
def part_m23n2(g):
    a = g.ev(f"({M23N2})({{}})")
    print(f"  m23 night 2: door {a['door']}, notices {a['notices']}, arrows {a['arrows']}, job {a.get('job')}, end {a.get('end')}")
    dr = a['door']
    check(not dr['none'] and not dr['badgeOnly'] and not dr['permitOnly'] and not dr['notTold'], f"m23: the reactor door stays shut without a permit, a badge and the Watch told ({dr})")
    check(dr['told'] and not dr['outside'], f"m23: it opens with all three, and shuts once you're out ({dr})")
    check(not a['tellEarly'] and not a['tellNoBadge'], "m23: no telling the Watch before the permit and the badge")
    check([x[0] for x in a['arrows']] == ['m23:permit', 'm23:badge', 'm23:tell', 'm23:reactor', 'm23:outcard', 'm23:return'] and all(x[1] == 1 for x in a['arrows']), f"m23: a level 1 arrow for each step, in order ({a['arrows']})")
    check(a['arrows'][:1] and a['arrows'][0][2] == 1260, f"m23: the first arrow at 21:00 ({a['arrows'][:1]})")
    n = a['notices']
    check(n[:1] and n[0][0] == 1230 and len([x for x in n if x[1] == 'The Watch']) == 2, f"m23: the notice at 20:30, the Watch told in and out ({n})")
    check(a.get('job') and a['job'][0] == 'you' and a['job'][2] == 3 and not a['outEarly'], f"m23: the visit, yours, three stops ({a.get('job')})")
    check(not a['word'], "m23: no word from the Watch when the badge is back in time")
    check(a['end'][:4] == [True, 23, 1, 'done'] and a['step'] is None, f"m23: trained on Day 23 with the badge back, one Mail ({a['end']})")
    b = g.ev(f"({M23N2})({{ late: true }})")
    check(b['word'] and len([x for x in b['notices'] if 'badge' in x[2].lower()]) >= 1, f"m23: the badge not back after half an hour: a word from the Watch ({b['notices']})")
def part_m23_all(g): part_m23(g); part_m23n2(g)
PARTS['m23'] = part_m23_all

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
 // head-scratchers are offered on ordinary workdays: with the events base off, the career-beat guard sees no event day (caseOffer asks eventDay; TS3)
 out.evDays = typeof eventDay !== 'function' || typeof EV_GUARD_ON === 'undefined' || EV_GUARD_ON ? null : Array.from({ length: 60 }, (_, i) => i + 1).filter(d => eventDay(d));
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
    check(a.get('evDays') in (None, []), f"ff: with the events base off no day is an event day, so cases are offered (Days 1-60: {a.get('evDays')})")
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
TPARTS = r"""(() => { const out = {}, W0 = JSON.stringify(SHIP.works), S0 = { ...SHIP.stores };
 // each run starts with the team parts on the shelves: an empty shelf rightly means no parts run (R5), and how many
 // are left by Day 18 depends on the crew's plans (FLC_ON's tradition used up the last bearing: BM11, 0.64.7)
 const reset = (t, uses) => { SHIP.works = JSON.parse(W0); machinesNew(); SHIP.jobs = []; SHIP.mail = []; MACH_HOUR = null; MACH_SEEN = -1; setShipNow(t); machinesNow(); SHIP.works = null; const W = worksInit(t);
   W.team = { plan: {} }; W.inc = { plan: {}, open: null }; W.tier = 2; W.rank = 'officer'; W.tr.t2 = 10; W.tr.m8 = 11; W.use.m8 = uses; if (worksSide()) worksSide().parts = 0; for (const k of Object.values(TEAM_PARTS).flat()) SHIP.stores[k] = Math.max(SHIP.stores[k] || 0, 3); return W; };
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
 SHIP.works = JSON.parse(W0); SHIP.stores = S0; return out; })()"""
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
  const onJob = ppl.map(p => ts.some(t => { const w = whereIs(p, t); return !!w && w.tag === 'job'; }));   // crew out on a repair job (EV6, storm S10): left out, since the jobs come from the machines' state at the time (the storm's wear leaves more by Day 18, done by the second pass)
  setShipNow(B + 935); liftHold(true, B + 990);
  let movers = 0, bad = [], waiting = 0, after = 0;
  ppl.forEach((p, i) => {
    if (onJob[i]) return;
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
    # (FX17-3, lead 36) after the rides the lift runs smoother, so the machines' repair jobs (and the plans around them: whoever
    # took a job, and the knock-ons) can rightly differ from the first read: compare the roof's rules and the hold's (open,
    # once a day, held 15:35-16:30, nobody off the rule, the talk, the saves), not the day's crowd counts (movers, waiting)
    rules = lambda x: {**x, 'talk': 0, 'hold': {k: v for k, v in x['hold'].items() if k not in ('movers', 'waiting')}}
    check(json.dumps(rules(a2), sort_keys=True) == json.dumps(rules(a), sort_keys=True), 'm17: the paper part differs after the rides (%s)' % [k for k in a if rules(a).get(k) != rules(a2).get(k)])
    g.ev(f"(() => {{ const k = {keep}; LIFT_HOLD = null; setShipNow(k.t); if (deckDef.num !== k.deck) goToDeck(k.deck); player.obj.position.x = k.pos[0]; player.obj.position.z = k.pos[1]; Object.assign(SHIP.player.needs, k.needs); SHIP.player.carry = k.carry; }})()")   # as it was, for the parts after
PARTS['m17'] = part_m17


# ---- FX3 (AR1's play of 0.64.15) ----
# Making it safe (m6, Day 8): a word before the 10:30 call (Mail when it's set, a toast ten minutes before); after the talk
# the arrow follows Calder to the pipe on Deck 4; not following for 30 minutes, the crew make it safe and she says the next
# try's day, 10:30 and place; that day it's the 10:30 call again (not "Let's try that again" at 06:00); followed, your turn
# is yours at once and points at the pipe. Small lessons: the drill's and the inspection's talks before them and readable
# (not closed by the meetings tick within a minute), their asks sent (the drill's that morning, the inspection's the day before)
FX3M6 = r"""(() => {
  SHIP.works = null; SHIP.occasions.length = 0; SHIP.notes = []; SHIP.flags = {}; SHIP.jobs = []; SHIP.mail = [];
  MACH_HOUR = null; MACH_SEEN = -1; WORKS_TICK.m = WORKS_TICK.h = -1; clearGoal(); if (DIALOGUE) dialogueEnd(true); goToDeck(5);   // you, far from the pipe
  const row = ladderRow('m6'); let d = row.day; while (!playerShiftOn(d) || !ladderTeacher(row, d)) d++;
  setShipNow((d - 1) * 1440 + 300); machinesNow(); const W = worksInit(); W.log.push(['earlier', 1, 0, 'service']);
  for (const r of CAREER_LADDER.slice(0, CAREER_LADDER.indexOf(row))) { W.tr[r.id] = 1; W.use[r.id] = 9; (W.op[1] = W.op[1] || []).push(r.id); }
  const said = [], kt = toast; toast = (a, b) => said.push(a + ': ' + b);
  const run = (a, b, f) => { for (let t = a; t <= b; t++) { setShipNow(t); machinesNow(); worksCareerTick(t); if (DIALOGUE) dialogueEnd(true); if (f && f(t)) return t; } return null; };
  const T = m => (d - 1) * 1440 + m, out = { day: d };
  run(T(359), T(600)); out.st0 = W.cur && W.cur.st; out.warnMail = SHIP.mail.map(x => x.subject + ': ' + x.body).filter(x => /10:30/.test(x));
  run(T(601), T(625)); out.soon = said.filter(x => /Ten minutes/.test(x)).length;
  const c = W.cur; run(T(626), T(640), t => { const r = SHIP.occasions.find(x => x.key === c.occ); if (r && t >= r.at && !r.met) { r.met = true; worksCareerTick(t + .5); } return c.st === 'watch'; });
  const seen = () => { if (typeof GUIDE_ON !== 'undefined' && GUIDE_ON && typeof goalNow === 'function') { GUIDE.key = ''; return goalNow(); } return IX_GOAL; };   // the arrow you see: with the teaching arrows on (0.92.0) the burst's follow is the queue's inc:m6 entry
  const sg = seen(); out.watch = c.st; out.goal = sg ? [sg.deck, sg.place, sg.label] : null;
  const t1 = shipNow(); run(t1 + 1, t1 + 40, () => c.st !== 'watch');
  out.after = c.st; out.goalAfter = !!seen(); out.open = W.inc.open; out.again = SHIP.mail.filter(x => /Next time/.test(x.subject)).map(x => x.body);
  let d2 = d + 1; while (!playerShiftOn(d2)) d2++;
  const U = m => (d2 - 1) * 1440 + m; run(U(300), U(400)); const r2 = SHIP.occasions.find(x => x.key === c.occ);
  out.next = [worksDay(shipNow()), c.st, r2 ? r2.at % 1440 : null, said.filter(x => /try that again/i.test(x)).length];
  run(U(401), U(640), t => { const r = SHIP.occasions.find(x => x.key === c.occ); if (r && t >= r.at && !r.met) { r.met = true; worksCareerTick(t + .5); } return c.st === 'watch'; });
  setGoal({ deck: 3, place: '3-grab-1', label: 'Food, Deck 3' });   // another section's arrow (a need's) put up meanwhile: never cleared by this one (PR9)
  const tv = shipNow(), vp = (DECKS[3].places || []).find(p => p.type === 'lift-wait');   // a job you hold when your turn comes (RV6/lead 28: the burst leads, it waits)
  SHIP.jobs.push({ id: 'fx3-held', machine: null, deck: 3, room: vp.room, kind: 'chore', chore: 'vent', title: 'Clean a vent: test', tier: 1, urgency: 1, posted: tv, found: tv, claimedBy: null, parts: [], status: 'open', stops: [{ deck: 3, placeId: vp.id, mins: 20, tag: 'vent' }] }); MACH_REV++;
  out.heldTaken = claimJob('fx3-held');
  c.w = 1; const t2 = Math.floor(shipNow()) + 1; run(t2, t2 + 1);
  const mj = myJob(); out.yours = [c.st, mj && mj.id === c.j, mj && (ixJobStep() || {}).deck, IX_GOAL ? IX_GOAL.label : null];
  out.parked = (SHIP.jobs.find(x => x.id === 'fx3-held') || {}).claimedBy;
  if (mj && mj.id === c.j) { jobFinish(mj, shipNow(), 'you'); const t3 = Math.floor(shipNow()) + 1; run(t3, t3 + 1); }
  out.back = (myJob() || {}).id || null;
  toast = kt; SHIP.works = null; SHIP.jobs = []; clearGoal(); return out;
})()"""
FX3SMALL = r"""(() => {
  SHIP.works = null; SHIP.occasions.length = 0; SHIP.notes = []; SHIP.flags = {}; SHIP.jobs = []; SHIP.mail = [];
  MACH_HOUR = null; MACH_SEEN = -1; WORKS_TICK.m = WORKS_TICK.h = -1; if (DIALOGUE) dialogueEnd(true);
  const out = {}, open = m => !!(DIALOGUE && DIALOGUE.id.startsWith('train.' + m));
  setShipNow(1440 + 1080); machinesNow(); const W = worksInit(); W.log.push(['earlier', 1, 0, 'service']); W.tr.m1 = W.tr.m4 = 2; W.use.m1 = W.use.m4 = 1; (W.op[2] = ['m1', 'm4']);
  let wed = 2; while (weekday(wed) !== 2 || !playerShiftOn(wed) || !playerShiftOn(wed + 1)) wed++;
  const at = m => (wed - 1) * 1440 + m, tick = t => { setShipNow(t); machinesNow(); worksCareerTick(t); };
  for (let t = at(300); t <= at(400); t += 10) tick(t);
  out.drillAsk = SHIP.mail.filter(x => /Drill at three/.test(x.subject)).length; out.m3dOpen = worksOpened(W).has('m3d');
  for (let t = at(880); t <= at(DRILL_TOAST + 1); t++) tick(t);
  out.brief = open('m3d'); meetingsTick(shipNow()); meetingsTick(shipNow() + 1); out.briefStays = open('m3d'); if (DIALOGUE) dialogueEnd(true);
  goToDeck(5); for (let t = at(DRILL_TOAST + 2); t <= at(1200); t += 5) tick(t);   // you're not in your bunk room: no word from Tomas in person, so his Mail at 21:30
  out.inspectEarly = SHIP.mail.filter(x => /Inspection tomorrow/.test(x.subject)).length;
  for (let t = at(1205); t <= at(1300); t += 5) tick(t);
  out.inspectAsk = SHIP.mail.filter(x => /Inspection tomorrow/.test(x.subject)).length;
  const bed = placeById(playerBed()); goToDeck(bed.deck); player.obj.position.copy(cellPos(...bed.at));
  const th = m => wed * 1440 + m; for (let t = th(300); t <= th(375); t += 5) tick(t);
  out.m3iOpen = worksOpened(W).has('m3i'); out.tomas = open('m3i'); meetingsTick(shipNow()); out.tomasStays = open('m3i'); if (DIALOGUE) dialogueEnd(true);
  // the inspection morning's arrows (the week guide's Day 4, lead 29): wardrobe, bed, locker, then your berth if you've left it
  const gq0 = typeof GUIDE_ON !== 'undefined' && GUIDE_ON; if (gq0) GUIDE_ON = false;   // FX3's direct arrows: the queue off (on from 0.92.0, the queue's own path is the week guide's Day 4, AC2's F2)
  const C = SHIP.clothes, P = SHIP.player, lab = () => { const g = goalNow(); return g ? g.label : null; }; clearGoal(); out.arrows = [];
  goToDeck(5); const keep = [C && C.changed, P.bedMade, P.untidy]; if (C) C.changed = null; P.bedMade = null; P.untidy = true;
  let t9 = th(376); tick(t9); out.arrows.push(lab());
  if (C) C.changed = wed + 1; tick(++t9); out.arrows.push(lab()); P.bedMade = wed + 1; tick(++t9); out.arrows.push(lab()); P.untidy = false; tick(++t9); out.arrows.push(lab());
  goToDeck(bed.deck); player.obj.position.copy(cellPos(...bed.at)); tick(++t9); out.arrows.push(lab());
  goToDeck(5); tick(++t9); out.arrows.push(lab()); setGoal({ deck: 3, place: '3-galley-1', label: 'someone else' }); P.bedMade = null; tick(++t9); out.arrows.push(lab()); clearGoal();
  const gq = typeof GUIDE_ON === 'undefined' ? null : GUIDE_ON, setQ = v => { if (gq === null) window.GUIDE_ON = v; else GUIDE_ON = v; };   // the arrow queue on: the arrows step aside (AC2's piece F2 asks the queue)
  setQ(true); tick(++t9); out.queued = lab(); if (gq === null) delete window.GUIDE_ON; else GUIDE_ON = gq;
  tick(++t9); for (let t = t9; t <= th(INSPECT_AT); t++) tick(t); out.arrows.push(lab());
  if (gq0) { GUIDE_ON = true; guideStart(); }
  if (C) C.changed = keep[0]; P.bedMade = keep[1]; P.untidy = keep[2]; goToDeck(bed.deck); player.obj.position.copy(cellPos(...bed.at));
  const n0 = SHIP.mail.length; worksTrained('m3i'); out.again = open('m3i'); if (DIALOGUE) dialogueEnd(true);
  W.tr.m2 = undefined; delete W.tr.m2; worksTrained('m2'); out.m2 = open('m2'); meetingsTick(shipNow()); out.m2Stays = open('m2'); if (DIALOGUE) dialogueEnd(true);
  goToDeck(4); SHIP.works = null; SHIP.jobs = []; return out;
})()"""
FX3M4 = r"""(() => {
  SHIP.works = null; SHIP.occasions.length = 0; SHIP.notes = []; SHIP.flags = {}; SHIP.jobs = []; SHIP.mail = []; SHIP.manifest = [];
  MACH_HOUR = null; MACH_SEEN = -1; WORKS_TICK.m = WORKS_TICK.h = -1; clearGoal(); if (DIALOGUE) dialogueEnd(true); goToDeck(5);
  const row = ladderRow('m4'); let d = row.day; while (haulDay(d) || !playerShiftOn(d) || !ladderTeacher(row, d)) d++;   // a day with no delivery
  setShipNow((d - 1) * 1440 + 300); machinesNow(); const W = worksInit(); W.log.push(['earlier', 1, 0, 'service']); W.tr.m1 = 1; W.use.m1 = 1; (W.op[1] = W.op[1] || []).push('m1');
  SHIP.manifest = []; const out = { day: d, wd: weekday(d) }, run = (a, b, f) => { for (let t = a; t <= b; t++) { setShipNow(t); machinesNow(); worksCareerTick(t); if (DIALOGUE) dialogueEnd(true); if (f && f(t)) return t; } return null; };
  const T = m => (d - 1) * 1440 + m; run(T(359), T(400)); const c = W.cur; out.st0 = c && c.id + ':' + c.st;
  run(T(401), T(900), t => { const r = c && SHIP.occasions.find(x => x.key === c.occ); if (r && t >= r.at && !r.met) { r.met = true; worksCareerTick(t + .5); } return c && c.st !== 'meet'; });
  out.watch = c && c.st; const wj = c && SHIP.jobs.find(x => x.id === c.j); out.watchJob = wj ? (wj.crates || []).length : 0;
  if (c && c.st === 'watch') { c.w = 99; const t2 = Math.floor(shipNow()) + 1; run(t2, t2 + 1); }
  const yj = c && c.st === 'do' && SHIP.jobs.find(x => x.id === c.j); out.yours = yj ? (yj.crates || []).length : 0;
  out.labels = [];
  if (yj && claimJob(yj.id)) { const n = jobStops(yj).length; for (let k = 0; k < n; k++) { out.labels.push((ixJobStep() || {}).label || null); jobStepDone(yj.id, k); } }
  // a lesson that didn't happen: asked again at its own time on the next workday, not restarted at 06:00
  W.tr.m4 = undefined; delete W.tr.m4; W.cur = { id: 'm4', st: 'again', d, by: row.by[0], occ: null, j: null, w: 0 }; SHIP.jobs = [];
  let d2 = d + 1; while (!playerShiftOn(d2) || !ladderTeacher(row, d2)) d2++; WORKS_TICK.h = -1; run((d2 - 1) * 1440 + 359, (d2 - 1) * 1440 + 362);
  const r2 = SHIP.occasions.find(x => x.key === W.cur.occ); out.again = [W.cur.st, r2 ? r2.at % 1440 : null];
  SHIP.works = null; SHIP.jobs = []; SHIP.manifest = []; clearGoal(); return out;
})()"""
FX3PROMO = r"""(() => {
  if (typeof promoSeekTick !== 'function') return null;
  SHIP.works = null; SHIP.occasions.length = 0; SHIP.flags = {}; SHIP.jobs = []; if (DIALOGUE) dialogueEnd(true); goToDeck(5);
  const now = Math.floor(shipNow()), p = player.obj.position, fake = { p: { id: 'calder' }, x: p.x, z: p.z }, say = worksSayAll;
  SHIP.occasions.push({ id: 'promoSummons', key: 'promoSummons@' + worksDay(now), at: now - 20, len: 30, deck: 5, room: 'o', by: 'calder', kind: 'meeting', status: 'asked', f: { seek: now - 5 } });
  DECK_CREW.push(fake); worksSayAll = () => {}; let out = null;
  const sid = OCCASIONS.promoSummons.script;   // promo.result with PROMO_BEATS_ON (FX28)
  try { promoSeekTick(now); const a = !!(DIALOGUE && DIALOGUE.id === sid); meetingsTick(now); meetingsTick(now + 1); out = [a, !!(DIALOGUE && DIALOGUE.id === sid)]; }
  finally { worksSayAll = say; DECK_CREW.splice(DECK_CREW.indexOf(fake), 1); DIALOGUE = null; if (typeof deviceDialogue === 'function') deviceDialogue(null); SHIP.occasions.length = 0; SHIP.works = null; }
  return out;
})()"""
def part_fx3(g):
    pr = g.ev(FX3PROMO); print('  the promotion talk where she finds you:', pr)
    check(pr is None or pr == [True, True], f"promo: Calder's talk where she finds you stays to be read ({pr})")
    h = g.ev(FX3M4); print('  m4 off a delivery day:', h)
    check(h['watch'] == 'watch' and h['watchJob'] == 1, f"m4: off a delivery day Yara's lesson still has its crates ({h})")
    check(h['yours'] >= 2, f"m4: your run after it, with the rest of the crates ({h})")
    check(len(h['labels']) >= 4 and h['labels'][0].startswith('Take a hover cart') and any(l and l.startswith('Load the') and '(1 of' in l for l in h['labels']) and any(l and ' to ' in l and 'Deck' in l for l in h['labels']) and h['labels'][-1].startswith('Cart back'), f"m4: each stop's own words on the arrow ({h['labels']})")
    check(h['again'][0] == 'meet' and h['again'][1] and h['again'][1] >= 660, f"m4: a lesson that didn't happen is asked again at its own time after the delivery, not at 06:00 ({h['again']})")

    a = g.ev(FX3M6); print('  m6 flow:', a)
    check(a['st0'] == 'meet' and a['warnMail'], f"m6: a Mail when the training's set, naming 10:30 ({a['warnMail']})")
    check(a['soon'] == 1, f"m6: a word ten minutes before the call ({a['soon']})")
    check(a['watch'] == 'watch' and a['goal'] and a['goal'][0] == 4 and a['goal'][1] == '4-valve-panel' and 'Follow' in a['goal'][2], f"m6: after the talk the arrow follows the teacher to the pipe ({a['goal']})")
    gl = (a['goal'] or [None, None, ''])[2] or ''   # no crash when there's no arrow (FX3)
    check('Calder' in gl and 'Ines' not in gl, f"m6: the label calls her Calder, as everywhere else (RV6) ({gl})")
    check(a.get('heldTaken') and a.get('parked') == 'you-parked' and a.get('back') == 'fx3-held', f"m6: a job you hold waits while the burst pipe leads, and comes back after it ({a.get('heldTaken')}, {a.get('parked')}, {a.get('back')})")
    check(a['after'] == 'ask' and not a['goalAfter'] and a['open'] is None and a['again'] and '10:30' in a['again'][0], f"m6: not followed: the crew make it safe, the next try with its day, time and place ({a['after']}, {a['again']})")
    check(a['next'][1] == 'meet' and a['next'][2] == 630 and a['next'][3] == 0, f"m6: the next try is the 10:30 call again, not a 06:00 restart ({a['next']})")
    check(a['yours'][0] == 'do' and a['yours'][1] and a['yours'][2] == 4 and a['yours'][3] == 'Food, Deck 3', f"m6: followed, your turn is yours at once and points at the pipe; another section's arrow left alone ({a['yours']})")
    b = g.ev(FX3SMALL); print('  small lessons:', b)
    A = b.get('arrows') or []
    check(A[:4] == ['Fresh uniform for inspection: your wardrobe', 'Make your bed: your bunk', 'Tidy your locker: your bunk', 'Inspection at 06:30: your berth'] and A[4] is None
          and A[5] == 'Inspection at 06:30: your berth' and A[6] == 'someone else' and A[7] is None and b.get('queued') is None,
          f'fx3: the inspection morning\'s arrows lead through wardrobe, bed and locker to your berth, never over another arrow, none with the arrow queue on, gone at 06:30 ({A}, queue on: {b.get("queued")})')
    check(b['m3dOpen'] and b['drillAsk'] == 1, f"m3d: Calder's ask the morning of your first drill ({b})")
    check(b['brief'] and b['briefStays'], f"m3d: her briefing before the drill, and it stays to be read ({b})")
    check(b['inspectEarly'] == 0 and b['inspectAsk'] == 1, f"m3i: Tomas's ask the evening before your first inspection (in person in your bunk room, else Mail at 21:30) ({b})")
    check(b['m3iOpen'] and b['tomas'] and b['tomasStays'] and not b['again'], f"m3i: his talk before the walk, readable, and not again after it ({b})")
    check(b['m2'] and b['m2Stays'], f"m2: Torres's word stays to be read ({b})")

# ---- the work steps by tap (B2 for lead 39, RV20's M3): a registered job kind on a machine with more than one stop (24q's
# rewiring) is played stop by stop when you tap its machine at phone size, never section 15's plain timed repair: the look,
# each wire's card (the right terminal picked), the test; then turned in, the junction put right. JOB_TAP_EXTRA lets a later
# piece add its own kinds (24v's relay swap) as [setup JS returning { id, deck }, pick JS (j, k) -> option index]
WSTAP_SETUP = r"""(() => { const d = 23; skipTo((d - 1) * 1440 + 570); machinesNow(); if (DIALOGUE) dialogueEnd(true);
  const W = worksInit(); W.tier = Math.max(W.tier, 2); W.rank = W.rank === 'junior' ? 'officer' : W.rank; W.tr.t2 = W.tr.t2 || 10; W.tr.m15 = W.tr.m15 || 17;
  SHIP.jobs = SHIP.jobs.filter(x => x.claimedBy !== 'you'); SHIP.machines['4-junction-1'].cond = 40;
  const j = rewJob('4-junction-1', shipNow(), { key: 77 }); SHIP.jobs.push(j); if (!claimJob(j.id)) return null;
  if (ACT && typeof actEnd === 'function') actEnd(true); if (DEV.choose) devChosen(-1); goToDeck(4); return { id: j.id, mach: '4-junction-1' }; })()"""
WSTAP_PICK = "((j, k) => { const want = rewRight(j, k); return jobStops(j)[k].opts.options.findIndex(o => o.id === want); })"
WSTAP_TAP = r"""((id) => { const m = machineById(id), p = cellPos(...m.at), v = new THREE.Vector3(); if (deckDef.num !== m.deck) return ['not on its deck', false];
  let best = null, bd = 1e9; for (const it of ITEMS) { if (!it.hit) continue; it.hit.getWorldPosition(v); const dd = Math.hypot(v.x - p.x, v.z - p.z); if (dd < bd) { bd = dd; best = it; } }
  player.obj.position.copy(cellPos(...m.panel)); player.stop(); const at = new THREE.Vector3(p.x, 0.8, p.z); return [best && best.t, playerTap(best, at, at.clone())]; })"""
WSTAP_NOW = "((id) => { const j = SHIP.jobs.find(x => x.id === id) || {}; return { done: (j.stepsDone || []).slice(), n: jobStops(j).length, work: !!j.workDone, act: ACT ? ACT.kind : null, ws: ACT && ACT.o ? ACT.o.ws : null, card: !!DEV.choose }; })"
def wstap_play(g, setup, pick, tag):
    s = g.ev(setup); g.step(40)   # the deck's things in place before the first tap
    if not check(s, f'{tag}: the job could not be set up'): return None
    acts, taps = set(), 0
    for n in range(60):
        st = g.ev(f"({WSTAP_NOW})({json.dumps(s['id'])})")
        if st['act']: acts.add(st['act'])
        if st['work']: break
        if st['card'] and st['ws'] is not None:
            i = g.ev(f"(() => {{ const j = SHIP.jobs.find(x => x.id === {json.dumps(s['id'])}); return ({pick})(j, {st['ws']}); }})()")
            g.ev(f"devChosen({i})"); g.step(10); continue
        if not st['act']: g.ev(f"({WSTAP_TAP})({json.dumps(s['mach'])})"); taps += 1
        g.step(30)
    st = g.ev(f"({WSTAP_NOW})({json.dumps(s['id'])})")
    turned = g.ev(f"turnInJob({json.dumps(s['id'])})") if st['work'] else False
    print(f'  {tag}: {taps} taps, stops done {st["done"]} of {st["n"]}, work done {st["work"]}, turned in {turned}, activities {sorted(acts)}')
    check('job' not in acts, f'{tag}: a tap on its machine ran section 15\'s plain repair (activity "job"), not its steps ({sorted(acts)})')
    check(st['work'] and len(st['done']) == st['n'] and 'workStep' in acts, f'{tag}: its steps should play by tap to the end ({st})')
    return st
JOB_TAP_EXTRA = {}
JOB_TAP_EXTRA['relayswap'] = (r"""(() => { const d = 23; skipTo((d - 1) * 1440 + 600); machinesNow(); if (DIALOGUE) dialogueEnd(true);
  const W = worksInit(); W.tier = 3; W.rank = 'senior'; W.tr.t3 = 15; W.tr.m19 = 17; toolGive('tester');
  SHIP.jobs = SHIP.jobs.filter(x => x.claimedBy !== 'you'); const j = pwrJob('relayswap', '1-relay-1', shipNow(), { key: 91 }); SHIP.jobs.push(j); if (!claimJob(j.id)) return null;
  if (ACT && typeof actEnd === 'function') actEnd(true); if (DEV.choose) devChosen(-1); goToDeck(1); return { id: j.id, mach: '1-relay-1' }; })()""", "((j, k) => j.bad)")   # 24v (S5-3): a relay swap by tap, the failing relay picked
JOB_TAP_EXTRA['arraycal'] = (r"""(() => { const d = 23; skipTo((d - 1) * 1440 + 600); machinesNow(); if (DIALOGUE) dialogueEnd(true);
  const W = worksInit(); W.tier = 3; W.rank = 'senior'; W.tr.t3 = 15; W.tr.m20 = 19;
  SHIP.jobs = SHIP.jobs.filter(x => x.claimedBy !== 'you'); const j = arrJob(shipNow(), { key: 91 }); SHIP.jobs.push(j); if (!claimJob(j.id)) return null;
  if (ACT && typeof actEnd === 'function') actEnd(true); if (DEV.choose) devChosen(-1); goToDeck(2); return { id: j.id, mach: '2-array-1' }; })()""",
  "((j, k) => { const st = jobStops(j)[k]; if (st.how !== 'turn') return 0; const w = SHIP.player.wsteps.find(x => x.job === j.id && x.k === k); return w && w.v > 0 ? 0 : 1; })")   # 24x (S5-5): a calibration by tap: the first star, the dial turned toward 0 (− or +)
def part_wstap(pw):
    g = Game(pw, sys.argv[1], 390, 844)
    try:
        if g.ev("typeof rewJob === 'function' && !!JOB_KINDS.rewire"): wstap_play(g, WSTAP_SETUP, WSTAP_PICK, 'rewiring (24q) by tap')
        else: print('  rewiring not in this build')
        for k, (setup, pick) in JOB_TAP_EXTRA.items():
            if g.ev(f"!!JOB_KINDS[{json.dumps(k)}]"): wstap_play(g, setup, pick, k + ' by tap')
            else: print(f'  {k}: not in this build (not yet)')
        if g.errors: fail('wstap: page errors: ' + ' | '.join(g.errors[:3]))
    finally: g.close()

# ---- a team job's turn arrow (B2 for lead 40, RV20's S2): your turn's arrow goes when the lead starts without you, when
# the step moves on and at the end; another section's arrow is never cleared (24h's teamGoalOff)
TEAMGOAL = r"""(() => { setShipNow(22 * 1440 + 540); machinesNow(); const W = worksInit(); W.tier = 2; W.rank = 'officer'; if (typeof GUIDE_ON !== 'undefined') GUIDE.key = '';
  clearGoal(); const part = Object.keys(TEAM_PART)[0], pl = (DECKS[4].places || []).find(p => p.machine) || DECKS[4].places[0], t = shipNow();
  const j = { id: 'repro-team', kind: 'team', team_kind: Object.keys(TEAM_NAME)[0], machine: pl.machine || null, deck: 4, status: 'claimed', claimedBy: 'you', lead: 'torres-zeke', team: ['torres-zeke', 'halloran-emeka'],
    seq: [{ who: 'torres-zeke', part, mins: 5 }, { who: 'you', part, mins: 5 }, { who: 'halloran-emeka', part, mins: 5 }], cur: 0, stepAt: t, start: t, spots: { you: pl.id }, title: 'Repro team job', parts: [], stepsDone: [], mins: 15, done: t + 15, end: t + 15, segsBy: { 'torres-zeke': [], 'halloran-emeka': [] }, machines: [] };
  SHIP.jobs.push(j);
  teamNext(j, t); const turn = IX_GOAL ? IX_GOAL.label : null;
  teamLate(j, t + 16); const late = IX_GOAL ? IX_GOAL.label : null;
  for (let k = 0; k < 4 && j.cur < j.seq.length; k++) teamNext(j, t + 20 + k); const end = IX_GOAL ? IX_GOAL.label : null;
  // another section's arrow is never cleared by the team job
  setGoal({ deck: 3, place: '3-grab-1', label: 'Food, Deck 3' }); const j2 = { ...j, id: 'repro-team-2', cur: 0, seq: j.seq.map(s => ({ ...s, who: s.who === 'torres-zeke' ? s.who : 'you' })), status: 'claimed', claimedBy: 'you', youOut: false, late: false, workDone: null, segsBy: { 'torres-zeke': [], 'halloran-emeka': [] } }; SHIP.jobs.push(j2); teamLate(j2, t + 30); const other = IX_GOAL ? IX_GOAL.label : null;
  SHIP.jobs = SHIP.jobs.filter(x => !/^repro-team/.test(x.id)); clearGoal();
  return { turn, late, end, other }; })()"""
def part_teamgoal(g):
    a = g.ev(TEAMGOAL); print('  team turn arrow:', a)
    check(a['turn'] and a['late'] is None and a['end'] is None and a['other'] == 'Food, Deck 3', f"m8: your turn's arrow goes when the lead starts without you and at the end, never another's ({a})")

only = set(sys.argv[2:])
# ---- ps, Power safety (S5-1 turn 2, B1; plans/p5-step5-spec.html question 2 and its beats table): with P5_STEP5 on,
# an Officer on Day 12 (Tier 1 and Team jobs done; Tracing's lesson may be under way: ps doesn't wait for it): ps is the
# day's one small row; Calder's ask, an appointment at 09:00 or 09:15 at the Deck 6 port junction (6/j) with her Mail; the
# level 1 arrow there from 15 minutes before; the talk (met) and trained, no job of yours, its after-word marked given;
# missed, asked again the next workday; the same twice. With the switch off: "not yet".
PS_RUN = r"""(() => {
  SHIP.works = null; SHIP.occasions.length = 0; SHIP.notes = []; SHIP.flags = {}; SHIP.jobs = []; SHIP.mail = [];
  MACH_HOUR = null; MACH_SEEN = -1; WORKS_TICK.m = WORKS_TICK.h = -1; if (typeof GUIDE !== 'undefined') { GUIDE.list.length = 0; GUIDE.counted.clear(); }
  const d = 12, t0 = (d - 1) * 1440; setShipNow(t0 - 1440 + 1200); machinesNow(); const W = worksInit();
  for (const r of CAREER_LADDER) if (r.tier === 1 || r.id === 'm8') { W.tr[r.id] = r.id === 'm8' ? 11 : 1; W.use[r.id] = 9; (W.op[1] = W.op[1] || []).push(r.id); }
  W.tier = 2; W.rank = 'officer'; W.xp = 10; W.test = { tier: 2, day: 9, tries: 1, passed: true };
  const out = { arrow: null };
  for (let m = t0 + 300; m <= t0 + 660; m += 5) {
    setShipNow(m); machinesNow(); worksCareerTick(m);
    if (typeof DIALOGUE !== 'undefined' && DIALOGUE && typeof dialogueEnd === 'function') dialogueEnd(true);
    const r = SHIP.occasions.find(x => x.id === 'works.ps' && x.status === 'asked' && !x.met);
    if (r) { out.occ = [r.deck, r.room, hhmm(r.at % 1440), r.len, r.by];
      const g = typeof GUIDE !== 'undefined' ? GUIDE.list.find(x => x.id === 'ps:meet:' + d) : null;
      if (g && !out.arrow) { const gl = g.goal(); out.arrow = [g.level, hhmm(m % 1440), gl && gl.deck, gl && gl.room, gl && gl.label]; }
      if (m >= r.at) { r.met = true; worksCareerTick(m + 1); } }
    if (W.tr.ps !== undefined) break;
  }
  out.opened = (W.op[d] || []).slice(); out.trained = W.tr.ps; out.brief = flag('works.brief.ps');
  out.jobs = SHIP.jobs.filter(j => j.train === 'ps').length; out.mail = SHIP.mail.filter(m => /Calder/.test(m.from)).map(m => m.subject);
  { const r = SHIP.occasions.find(x => x.id === 'works.ps'); out.told = r && r.f ? r.f.told || null : null; }
  { // in person (the user's rule): Calder walks over (worksEscort's 24u part) and says it when she reaches you; the Mail after
    SHIP.occasions = SHIP.occasions.filter(x => x.id !== 'works.ps'); SHIP.mail = []; const t1 = (d + 2) * 1440 + 400; setShipNow(t1); psAsk(d + 3, t1);
    const r = SHIP.occasions.find(x => x.id === 'works.ps'); const P = player.obj.position, fake = { p: { id: r.by }, h: {}, x: P.x, z: P.z }, said = [], keep = worksSayAll;
    out.escort = [JSON.stringify(worksEscort({ id: r.by }, t1)), SHIP.mail.length];
    DECK_CREW.unshift(fake); worksSayAll = (id, l) => said.push([id, l[0]]);   /* (W6) first in the list: psTellTick finds the first Calder, and the real one is on the deck when an earlier part left you there */ try { psTellTick(t1); } finally { worksSayAll = keep; DECK_CREW.splice(DECK_CREW.indexOf(fake), 1); }
    out.inPerson = [r.f.told, said.length ? said[0][0] : null, said.length && /Power safety/.test(said[0][1]), SHIP.mail.map(m => m.subject), JSON.stringify(worksEscort({ id: r.by }, t1))];
    SHIP.occasions = SHIP.occasions.filter(x => x.id !== 'works.ps'); }
  out.script = OCCASIONS['works.ps'] ? OCCASIONS['works.ps'].script : null; out.cur = W.cur && W.cur.id === 'ps' ? 'ps:' + W.cur.st : null;
  return out;
})()"""
def part_ps(g):
    print('ps (Power safety, S5-1):')
    if not g.ev("typeof P5_STEP5 !== 'undefined' && P5_STEP5 && !!WORK_MECH.ps"):
        print('  not yet (P5_STEP5 off)'); return
    guide = g.ev("typeof GUIDE_ON !== 'undefined' && GUIDE_ON")
    a, b = g.ev(PS_RUN), g.ev(PS_RUN)
    print('  ', json.dumps(a))
    smalls = g.ev("JSON.parse(JSON.stringify(CAREER_LADDER.filter(r => r.size === 'small').map(r => r.id)))")
    check([i for i in a['opened'] if i in smalls] == ['ps'], f"ps: the day's one small row on Day 12 ({a['opened']})")
    check(a.get('occ') and a['occ'][:2] == [6, 'j'] and a['occ'][2] in ('09:00', '09:15') and a['occ'][4] == 'calder', f"ps: Calder's appointment at the Deck 6 port junction, 09:00 or 09:15 ({a.get('occ')})")
    check(any('Power safety' in s for s in a['mail']), f"ps: Calder's Mail for the lesson ({a['mail']})")
    if guide: check(a['arrow'] and a['arrow'][0] == 1 and a['arrow'][2:4] == [6, 'j'], f"ps: the level 1 arrow to the junction before the talk ({a['arrow']})")
    check(a['trained'] == 12 and a['jobs'] == 0 and a['brief'] and a['cur'] is None, f"ps: trained at the talk on Day 12, no job of yours, the after-word marked given ({a['trained']}, {a['jobs']}, {a['brief']}, {a['cur']})")
    check(a.get('told') == 'notice', f"ps: not reached, told by the notice 20 minutes before ({a.get('told')})")
    ip = a.get('inPerson') or []
    check(a.get('escort') and '"follow"' in (a['escort'][0] or '') and a['escort'][1] == 0, f"ps: Calder walks over to you before she's said it, no Mail yet ({a.get('escort')})")
    check(ip[:3] == ['met', 'calder', True] and ip[3] == ['Power safety'] and ip[4] == 'null', f"ps: in person, Calder says it, then the Mail as the record, and she stops walking over ({ip})")
    check(a['script'] == 'train.ps.calder', f"ps: the talk is train.ps.calder ({a['script']})")
    check(json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True), 'ps: differs the second time')
    ms = g.ev(PS_RUN.replace("if (m >= r.at) { r.met = true; worksCareerTick(m + 1); } }", "if (window.__psMiss ? false : m >= r.at) { r.met = true; worksCareerTick(m + 1); } }")
      .replace("const out = { arrow: null };", "const out = { arrow: null }; window.__psMiss = true;")
      .replace("  out.opened = (W.op[d] || []).slice();", "  window.__psMiss = false; occasionsTick(t0 + 700, true); const again = []; for (let m = t0 + 700; m <= t0 + 4 * 1440 + 660; m += 10) { setShipNow(m); machinesNow(); worksCareerTick(m); occasionsTick(m, true); } out.again = SHIP.occasions.filter(x => x.id === 'works.ps').map(x => [Math.floor(x.at / 1440) + 1, x.status]);\n  out.opened = (W.op[d] || []).slice();"))
    print('   missed:', ms.get('again'))
    nxt = g.ev("(() => { let d = 13; while (!playerShiftOn(d)) d++; return d; })()")
    check(ms.get('again') and ms['again'][0] == [12, 'missed'] and len(ms['again']) >= 2 and ms['again'][1][0] == nxt, f"ps: missed on Day 12, asked again on the next workday, Day {nxt} ({ms.get('again')})")


with sync_playwright() as pw:
    g = Game(pw, sys.argv[1])
    ev = g.ev
    sr = ev(ROW_STAND)                                     # E2's rows (m13, m14) live in 24 core's table (E1); a stand-in only in a build without it
    if sr: print('stand-in ladder rows (24 core\'s table not in this build):', sr)
    rows = ev("CAREER_LADDER.map(r => ({ id: r.id, name: r.name, size: r.size, inBuild: !!WORK_MECH[r.id], stages: (r.stages || []).length }))")
    def row_check(g, ev, r):
        if r['id'] == 't2' and ev("typeof promoPassed === 'function'"):   # 24p's test job (0.44.18) is no training: career_check (i)-(j) tests it
            print(f"t2 ({r['name']}): 24p's test job, not a training (career_check (i) and (j))")
            return
        if r['id'] == 't4' and ev("typeof pu4Ready === 'function'"):   # (S6-3) 24u's Tier 4 test job, no training either: promo_beats_check's t4 parts test it
            print(f"t4 ({r['name']}): 24u's test job, not a training (promo_beats_check t4before ...)")
            return
        if r['id'] == 'm21' and ev("!!(WORK_MECH.m21 && WORK_MECH.m21.own)"):   # 28b's own briefing (S6-2): never through the ladder, trained at the first briefing
            print(f"m21 ({r['name']}): 28b's own briefing, not a training (its part below)")
            PARTS['m21'](g)
            return
        if r['id'] == 'm23' and ev("!!(WORK_MECH.m23 && WORK_MECH.m23.own)"):   # 28c's own nights (S6-5): never through the ladder
            print(f"m23 ({r['name']}): 28c's own engine work on your nights, not a training (its part below)")
            PARTS['m23'](g)
            return
        if r['id'] == 'm25' and ev("!!(WORK_MECH.m25 && WORK_MECH.m25.own)"):   # (S6-7) 28e's own day with Basil, never through the ladder: promo_beats_check's mt parts test it
            print(f"m25 ({r['name']}): 28e's own day with Basil, not a training (promo_beats_check mt)")
            return
        if r['id'] == 'm24' and ev("!!(WORK_MECH.m24 && WORK_MECH.m24.own)"):   # 28d's own night 3 (S6-6): never through the ladder, trained by the first swap you led
            print(f"m24 ({r['name']}): 28d's own coil swap on night 3, not a training (its part below)")
            PARTS['m24'](g)
            return
        if r['id'] == 't3' and ev("typeof puPassed === 'function'"):   # 24u's Tier 3 test job (S5-2) is no training either: promo_beats_check's t3 parts test it
            print(f"t3 ({r['name']}): 24u's test job, not a training (promo_beats_check t3before ... t3toast)")
            return
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
    for r in rows:
        if only and r['id'] not in only: continue
        if not r['inBuild']:
            print(f"{r['id']} ({r['name']}): not in this build")
            continue
        row_check(g, ev, r)
    # (RV21's S1) Pillar 5 Step 5's rows exist only with P5_STEP5 on: with it off in this build, they're run on a copy with
    # it switched on (as saves_check's and controller_check's Step 5 parts do), so the round tests them before the switch-on
    P5_LINE = "const P5_STEP5 = URL_FLAGS.has('p5s5');"
    src0 = pathlib.Path(sys.argv[1]).read_text()
    if P5_LINE in src0 and (not only or only & {'ps', 't3', 'm19', 'm18', 'm20', 'p4', 'p5', 'p9', 'mys'}):
        cp = WORK / 'test' / ('_mech_p5_' + str(os.getpid()) + '_' + pathlib.Path(sys.argv[1]).name); cp.write_text(src0.replace(P5_LINE, 'const P5_STEP5 = true;', 1))
        try:
            g5 = Game(pw, str(cp)); rows5 = g5.ev("CAREER_LADDER.map(r => ({ id: r.id, name: r.name, size: r.size, inBuild: !!WORK_MECH[r.id], stages: (r.stages || []).length }))")
            base = {r['id'] for r in rows}
            for r in rows5:
                if r['id'] in base or (only and r['id'] not in only): continue
                if not r['inBuild']: print(f"{r['id']} ({r['name']}): not in this build (P5_STEP5 on)"); continue
                print(f"(on a copy with P5_STEP5 switched on)"); row_check(g5, g5.ev, r)
            if g5.errors: fail('page errors (P5_STEP5 copy): ' + ' | '.join(g5.errors[:5]))
            g5.close()
        finally: cp.unlink(missing_ok=True)
    # Pillar 5 Step 6's rows (S6-2 on: m21) exist only with P5_STEP6 on: with it off in this build, run on a copy with it on
    P6_LINE = "const P5_STEP6 = P5_STEP5 && URL_FLAGS.has('p5s6');"
    if (P6_LINE in src0 or re.search(r'^const P5_STEP6 = P5_STEP5 && true;', src0, re.M)) and (not only or only & {'m21', 'm23', 'm24'}):   # (BM19) or already on (0.95.0): a fresh copy either way
        cp = WORK / 'test' / ('_mech_p6_' + str(os.getpid()) + '_' + pathlib.Path(sys.argv[1]).name); cp.write_text(src0.replace(P6_LINE, 'const P5_STEP6 = P5_STEP5 && true;', 1))
        try:
            g6 = Game(pw, str(cp)); rows6 = g6.ev("CAREER_LADDER.map(r => ({ id: r.id, name: r.name, size: r.size, inBuild: !!WORK_MECH[r.id], stages: (r.stages || []).length }))")
            base = {r['id'] for r in rows}
            for r in rows6:
                if r['id'] in base or (only and r['id'] not in only) or r['id'] not in {'m21', 'm23', 'm24'}: continue   # (each Step 6 piece adds its id here)
                if not r['inBuild']: print(f"{r['id']} ({r['name']}): not in this build (P5_STEP6 on)"); continue
                print(f"(on a copy with P5_STEP6 switched on)"); row_check(g6, g6.ev, r)
            if g6.errors: fail('page errors (P5_STEP6 copy): ' + ' | '.join(g6.errors[:5]))
            g6.close()
        finally: cp.unlink(missing_ok=True)
    if not only or 'ps' in only: part_ps(g)
    if (not only or 'side' in only) and ev("typeof worksSideXp === 'function'"):
        print('side (Step 4\'s core: tool wear, the side-job cap, the texts):'); part_side(g)
    if (not only or 'side' in only or 'm4' in only) and ev("typeof manifestRun === 'function' && !!JOB_KINDS.haul"):
        part_mrun(g); part_haul2(g)
        if ev("!!JOB_KINDS.stocktake"): part_stock(g)
    if (not only or 'side' in only or 'm1' in only) and ev("typeof roundDoor === 'function'"):
        part_round23(g)
    for k, f in EXTRA.items():                             # parts that aren't ladder rows (24l's favour cases)
        if (not only or k in only) and ev(f"!!JOB_KINDS['{k}'] || (typeof ffState === 'function' && '{k}' === 'ff') || (typeof teamParts === 'function' && '{k}' === 'tparts')"): print(k + ':'); f(g)
    if not only or 'fix2' in only: print('fix2 (the notes\' words):'); part_fix2_c(g)
    if not only or 't24' in only: part_t24(g)
    if not only or 'fx3' in only: print('fx3 (Making it safe\'s flow, the small lessons):'); part_fx3(g)
    if (not only or only & {'m8', 'teamgoal'}) and ev("typeof teamGoalOff === 'function' || typeof teamNext === 'function'"): print('teamgoal (a team job\'s turn arrow):'); part_teamgoal(g)
    if not only or 'p925' in only: part_p925(g)
    if not only or 'p925l' in only: part_p925l(g)
    ev("SHIP.works = null")
    if g.errors: fail('page errors: ' + ' | '.join(g.errors[:5]))
    g.close()
    if not only or only & {'m13', 'm14', 'm15', 'fcase', 'ff', 'side', 'tparts'}:
        print('side (E2\'s saved parts):'); side_save(pw)
    if not only or only & {'wstap', 'm15', 'm19'}:
        print('wstap (the work steps by tap, at phone size):'); part_wstap(pw)

print('MECH CHECK OK' if ok else 'MECH CHECK FAILED')
sys.exit(0 if ok else 1)
