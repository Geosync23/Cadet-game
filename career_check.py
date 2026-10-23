# Starship Cadet: career check (keep in the repo, next to cadet_test.py and the other checks)
# Checks Pillar 5's Works career, section 24 core (the Works career engineer, 0.44.x; plans/mechanics/foundation.html
# "For the builder · tests"), on paper: each run steps ship hours, calling the game's own functions at the hours they'd
# run (machinesNow, worksTick: the ladder each hour, the training each minute), with no walking; the player takes jobs
# off the real board with claimJob / jobStepDone / turnInJob.
#   (a) Step 1 as built: with no mechanic sub-block in the build, no row ever opens (Days 2-14), nothing trains, and
#       the Works app stays hidden until Day 1's shift has ended
#   (b) a steady player (the board's top job each hour of the shift, each trained mechanic used once a workday, the drill
#       and the inspection attended), with every row given a stand-in sub-block: the ladder opens as the table (each
#       row on its day), never more than one big and one small on a workday, nothing on Days 6-7; training: the
#       ask (an appointment and Mail), the meeting, the teacher's job (done by them), then yours, then trained; tools
#       given; "Relied on" by the end of Day 8 and the test job on Day 9
#   (c) a very busy player (every job on the board, every hour, weekends too) never reaches "Relied on" before Day 5
#   (d) a lazy player (one job a workday, misses the first ask of each training, uses things every other workday):
#       each row later, none lost
#   (e) reputation bands from xp, careerSpeed's words (skillWord), tools and their wear, missed shifts and abandoned jobs
#   (f) the save: worksClean round trip mid-training, junk, a real reload mid-training (saving on), an old save
#       loading as Tier 1 with nothing trained and the ladder opening from its day; ship.works under 3 KB by Day 30
#   (g) the whole steady run twice, identical
# Not yet (waiting for section 17's 17.2, seat S): reserved-rank jobs never taken below their rank, crew or you.
# Setup and environment as for cadet_test.py.
#   (p) FX1's fixes in the real game: the guidance (tracking after a job, the meeting arrow's window)
#   (q) FX1's arrow and tracking lifecycle (new game, Tracked, device go, On shift, clock out, empty board, shower, asks)
# Run:  python3 career_check.py BUILD.html     (--fx: only parts (p) and (q))
import sys, json, os, re, pathlib
exec(open(__file__.replace('career_check.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright

ok = True
def fail(msg):
    global ok
    ok = False
    print('FAIL', msg)
def check(cond, msg):
    if not cond: fail(msg)
    return cond

# one run on paper. plan: 'none' (no sub-blocks), 'steady', 'busy', 'lazy'. Returns the day-by-day story.
PAPER = r"""(({ plan, days, t2 }) => {
  const t0 = (SHIP_START.day - 1) * 1440 + SHIP_START.min;
  SHIP.works = null; SHIP.occasions.length = 0; SHIP.notes = []; SHIP.flags = {}; SHIP.jobs = []; SHIP.mail = []; SHIP.rep = null;
  JOBS_ON = true; MACH_HOUR = null; MACH_SEEN = -1; WORKS_TICK.m = WORKS_TICK.h = -1;
  if (WORK_MECH.t2 && WORK_MECH.t2.offer) window.__realT2 = WORK_MECH.t2;   // 24p's own test job (0.44.18), kept for t2: 'real' | 'late'
  for (const k in WORK_MECH) delete WORK_MECH[k];
  if (plan !== 'none') for (const r of CAREER_LADDER) WORK_MECH[r.id] = r.id === 't2' ? { noJob: true } : { reserve: (d, at, slot, o) => jobReserve('washer', d, at, slot, o) };   // stand-ins: the default training job
  if (plan !== 'none' && t2 && window.__realT2) WORK_MECH.t2 = window.__realT2;
  const promo = []; const stopP = onSim('promoTest', n => promo.push([n.step, Math.floor(n.t / 1440) + 1, n.day]));
  const at = t => { setShipNow(t); machinesNow(); };
  const days_ = [], trained = {}, asks = {}, teach = {}, mails = [], band = {}, seen = { meet: 0, watch: 0, do: 0 }, bad = [];
  const stop = [onSim('trained', n => { trained[n.mech] = Math.floor(n.t / 1440) + 1; })];
  const doJob = id => { if (!claimJob(id)) return false; const j = SHIP.jobs.find(x => x.id === id);
    if (j.train === 'm7' && typeof scanRead === 'function') { scanRead(id); if (typeof caseTick === 'function') caseTick(); }   // the scanner's training: you read it first (it shows Day 5's case; p5-fix2)
    const cs = SHIP.works && SHIP.works.cases && (SHIP.works.cases.open || []).find(c => c.job === id);   // a head-scratcher (24k): call it right first
    if (cs && typeof caseCall === 'function') caseCall(cs.id, cs.cause);
    jobStops(j).forEach((s, k) => jobStepDone(id, k)); return turnInJob(id); };
  const lazySkip = new Set();                            // the lazy player misses each training's first ask
  let firstJob = null;
  for (let d = 1; d <= days; d++) {
    let jobs = 0, used = [];
    const work = playerShiftOn(d), wd = weekday(d);
    for (let h = 6; h <= 22; h++) {
      const t = (d - 1) * 1440 + h * 60; at(t);
      if (plan === 'none' && h === 18) { worksCareerTick(t); continue; }
      worksCareerTick(t);
      if (typeof DIALOGUE !== 'undefined' && DIALOGUE && typeof dialogueEnd === 'function') dialogueEnd(true);   // the player reads it through (a meeting on screen holds the training)
      const W = SHIP.works, c = W && W.cur;
      if (c && c.mail && !mails.includes(c.by + ': ' + c.mail)) mails.push(c.by + ': ' + c.mail);
      // the training: be there for the meeting, watch, do your one
      if (c && c.st === 'meet') { const r = SHIP.occasions.find(x => x.key === c.occ);
        if (r) { asks[c.id] = asks[c.id] || []; if (!asks[c.id].includes(d)) asks[c.id].push(d); }
        if (r && t >= r.at && t < r.at + r.len + 60) {
          if (plan === 'lazy' && !lazySkip.has(c.id)) { lazySkip.add(c.id); }
          else { r.met = true; seen.meet++; }
        }
        if (r && t >= r.at + r.len) { occasionsTick(t, true); }
        worksCareerTick(t + 1);
      }
      const c2 = W && W.cur;
      if (c2 && c2.st === 'watch') { c2.w = TRAIN_WATCH; seen.watch++; worksCareerTick(t + 2); const j = SHIP.jobs.find(x => x.id !== c2.j && x.train === c2.id && x.status === 'done');
        teach[c2.id] = teach[c2.id] || {}; const dj = SHIP.jobs.filter(x => x.train === c2.id && x.status === 'done').pop(); if (dj) teach[c2.id].by = dj.doneBy; }
      const c3 = SHIP.works && SHIP.works.cur;
      const skipT2 = c3 && c3.id === 't2' && t2 === 'late' && SHIP.works.test && SHIP.works.test.tries === 1;   // the late player leaves the first test job
      if (c3 && c3.st === 'do' && work && h >= 8 && h < 17 && !skipT2) { seen.do++; if (!myJob() && doJob(c3.j)) { jobs++; (teach[c3.id] = teach[c3.id] || {}).you = (SHIP.jobs.find(x => x.id === c3.j) || {}).doneBy; } worksCareerTick(t + 3); }
      // the player's own work
      const shift = work && h >= 8 && h < 17;
      const leave = j => t2 === 'late' && (SHIP.jobs.find(x => x.id === j.id) || {}).reserved === 20 && SHIP.works && SHIP.works.test && SHIP.works.test.tries === 1;   // the late player leaves the first test job on the board too
      if (plan === 'steady' && shift && !myJob()) { const x = openJobs('you').filter(j => !leave(j))[0]; if (x && doJob(x.id)) { jobs++; if (!firstJob) firstJob = d; } }
      if (plan === 'busy') for (let k = 0; k < 3 && !myJob(); k++) { const x = openJobs('you')[0]; if (x && doJob(x.id)) jobs++; else break; }
      if (plan === 'lazy' && shift && jobs === 0 && h === 10 && !myJob()) { const x = openJobs('you')[0]; if (x && doJob(x.id)) jobs++; }
      // using what you're trained in (a sub-block calls worksUse); the drill and the inspection, attended
      if (SHIP.works && work && h === 14 && plan !== 'none' && (plan !== 'lazy' || d % 2 === 0))
        for (const r of CAREER_LADDER) if (r.size === 'big' && SHIP.works.tr[r.id] !== undefined && r.id !== 't2') { worksUse(r.id); used.push(r.id); }
      if (SHIP.works && plan !== 'none' && (plan !== 'lazy' || d % 2 === 0)) for (const r of CAREER_LADDER) if (r.fixed && h * 60 <= r.fixed.at && r.fixed.at < h * 60 + 60 && worksOpened().has(r.id) && weekday(d) + 1 === r.fixed.wd) { worksUse(r.id); used.push(r.id); }
      if (SHIP.works && plan !== 'none' && h === 16 && work && d >= (plan === 'lazy' ? 9 : 5)) flagSet('works.oily', d);   // an oily job turned in (the uniform's sub-block will say)
      if (SHIP.works && SHIP.works.tr.p3 === undefined && worksOpened().has('p3') && h === 15) { worksUse('p3'); used.push('p3'); }
      if (SHIP.works && SHIP.works.tr.m2 === undefined && worksOpened().has('m2') && h === 16) { worksUse('m2'); used.push('m2'); }
    }
    const W = SHIP.works;
    if (W) band[d] = worksBand();
    days_.push({ d, wd, work, jobs, op: W ? (W.op[d] || []) : [], xp: W ? Math.round(W.xp) : null, band: W ? worksBand() : null, cur: W && W.cur ? W.cur.id + ':' + W.cur.st : null, used });
  }
  stop.forEach(f => f()); stopP();
  const W = SHIP.works;
  const occ = SHIP.occasions.filter(r => /^works\./.test(r.id)).map(r => ({ id: r.id, day: Math.floor(r.at / 1440) + 1, at: hhmm(r.at % 1440), by: r.by, status: r.status }));
  return { days: days_, trained, asks, teach, seen, occ, firstJob, mail: mails, promo, test: W ? W.test : null, testJob: SHIP.jobs.filter(j => j.reserved === 20).map(j => [j.machine, j.status, j.doneBy, hhmm(j.found % 1440), hhmm(j.until % 1440)]),
    works: W ? JSON.parse(JSON.stringify(W)) : null, size: W ? JSON.stringify(W).length : 0, head: (worksRecordHead() || { text: null }).text, locker: worksLockerText(),
    view: W ? ['training', 'log', 'tools'].map(tab => { WORKS_TAB = tab; return worksView().blocks.filter(b => b.kind !== 'buttons').map(b => b.text || (b.rows || []).map(r => r.text + ' (' + r.sub + ')').join('; ')).join(' | '); }) : null };
})"""

LADDER = {'m1': 2, 'm4': 3, 'm3d': 3, 'm5': 4, 'm3i': 4, 'm7': 5, 'p3': 5, 'm6': 8, 'm2': 8, 't2': 9}

def story(r):
    for x in r['days']:
        print(f"    Day {x['d']} ({'MTWTFSS'[x['wd']]}{'' if x['work'] else ', off'}): jobs {x['jobs']}, opened {x['op']}, xp {x['xp']} ({x['band']}), training {x['cur']}, used {x['used']}")

def opened_on(r):
    out = {}
    for x in r['days']:
        for i in x['op']:
            out.setdefault(i, x['d'])
    return out

def pacing(r, name):
    from collections import Counter
    for x in r['days']:
        sizes = Counter()
        for i in dict.fromkeys(x['op']):
            sizes[next(s for s in (('big' if i in ('m1', 'm4', 'm5', 'm7', 'm6', 't2', 'm8', 'm9') else 'small'),))] += 1
        check(sizes['big'] <= 1 and sizes['small'] <= 1, f"{name}: Day {x['d']} opened {x['op']} (more than one big or one small)")
        check(x['work'] or not x['op'], f"{name}: Day {x['d']} is a day off and opened {x['op']}")

# (p) FX1 (patch-p5-fix1): the guidance in the real game, a fresh page with the real sub-blocks. Bug 1: a job taken and
# turned in leaves tracking on with nothing tracked (it kept the old job's id, so the training ask never put its arrow
# up). Bug 2: the meeting's arrow is up only from 15 ship minutes before the meeting until it has started or it's over
# (it was up from the ask all day); in its room before it starts it says wait here, out of it it leads back.
FX_LOOK = "(() => { const c = SHIP.works && SHIP.works.cur, r = c && c.occ && SHIP.occasions.find(x => x.key === c.occ); return [c ? c.id + ':' + c.st : null, r ? r.at : null, r ? r.len : null, r ? r.deck : null, r ? r.room : null, IX_GOAL ? IX_GOAL.label : null, typeof DIALOGUE !== 'undefined' && DIALOGUE ? DIALOGUE.id : null]; })()"
def fx_guidance(pw):
    print('(p) FX1, the guidance in the real game (bugs 1-2: tracking after a job, the meeting arrow\'s window):')
    g = Game(pw, sys.argv[1]); ev = g.ev
    ev("setShipNow(1020)"); g.step(2)
    ev("setShipNow(1440 + 480)"); g.step(2)
    tk = ev("(() => { const o = openJobs('you')[0]; if (!o || !ixBoard.take(o.id)) return null; const j = myJob(); jobStops(j).forEach((s, k) => jobStepDone(j.id, k)); ixBoard.turnIn(j.id); return j.id; })()")
    g.step(1)
    tr = ev("SHIP.player.track === undefined ? 'on' : SHIP.player.track")
    print('   a job taken and turned in:', tk, '-> tracking', tr)
    check(tk and tr == 'on', f"bug 1: after turning in a tracked job, tracking is on with nothing tracked (track {tr})")
    ask = None; r = None; m = 481
    while m < 1020:                                       # to the training ask (in 5-minute steps)
        ev(f"setShipNow({1440 + m})"); g.step(1); s = ev(FX_LOOK)
        if s[0] and s[0].endswith(':meet') and s[1]: ask = [m, s]; break
        m += 5
    if not check(ask, 'bug 2: no training ask on Day 2'): g.close(); return
    at, ln, dk, rm = ask[1][1] - 1440, ask[1][2], ask[1][3], ask[1][4]
    print('   the ask at', ask[0], 'for', ask[1][0], 'at', at, 'Deck', dk, rm, '| arrow at the ask:', ask[1][5])
    look = {}
    def go(mm, where=None):
        if where == 'in': ev(f"(() => {{ if (deckDef.num !== {dk}) goToDeck({dk}); const t = ROOM_TILES['{rm}'][0]; player.obj.position.copy(cellPos(...t)); }})()")
        if where == 'out': ev(f"(() => {{ const k = Object.keys(ROOM_TILES).find(k => k !== '{rm}' && ROOM_TILES[k].length > 4); player.obj.position.copy(cellPos(...ROOM_TILES[k][0])); }})()")
        ev(f"setShipNow({1440 + mm})"); g.step(1); g.step(1); look[mm] = ev(FX_LOOK); return look[mm]
    early = go(min(ask[0] + 5, at - 16)); lead = go(at - 14); inr = go(at - 10, 'in'); ev("setGoal({ deck: 3, room: 'M', label: 'Food' })"); lent = go(at - 8); ev('clearGoal()'); gave = go(at - 7); outr = go(at - 5, 'out'); back = go(at - 2, 'in'); start = go(at + 1)
    if start[6]: ev("dialogueEnd(true)")
    after = [go(at + 3)[5], go(at + 20)[5], go(at + ln + 5)[5]]
    print('   before the lead:', early[5], '| 14 before:', lead[5], '| in the room:', inr[5], '| out again:', outr[5], '| back in:', back[5], '| started:', start[0], start[6], '| after:', after)
    check(ask[1][5] is None and early[5] is None, f"bug 2: no meeting arrow at the ask nor before the lead time ({ask[1][5]}, {early[5]})")
    check(lead[5] and ' with ' in lead[5] and lead[5][0].isupper(), f"bug 2: the meeting arrow is up 14 minutes before ({lead[5]})")
    check((inr[5] or '').startswith('Wait here') and outr[5] == lead[5] and (back[5] or '').startswith('Wait here'), f"bug 2: in the room it says wait here (your job's arrow doesn't lead you off), out of it it leads back ({inr[5]}, {outr[5]}, {back[5]})")
    check(lent[5] == 'Food' and (gave[5] or '').startswith('Wait here'), f"bug 2 (PR9): another arrow borrows it, and once that's gone the meeting's is back ({lent[5]}, {gave[5]})")
    check(start[6] and not any(x and ' with ' in x for x in after), f"bug 2: the meeting plays with you there; its arrow never comes back after it ({start[6]}, {after})")
    if g.errors: fail('(p) page errors: ' + ' | '.join(g.errors[:5]))
    g.close()

# (p2) FX4 (p5-fix4): with the arrow queue off, a job you hold keeps the arrow from a training meeting (the playtest patch
# 1, #7) only if you took it before the meeting's arrow window opened (15 minutes before); one taken inside the window
# (turned one in and took the next at the board) doesn't: the meeting's arrow comes up (Day 5's scanner was missed till Monday)
def fx_window_job(pw):
    print('(p2) FX4, a job taken inside the meeting arrow\'s window (queue off):')
    g = Game(pw, sys.argv[1]); ev = g.ev
    ev("setShipNow(1020)"); g.step(2); ev("setShipNow(1440 + 480)"); g.step(2)
    ev("(() => { const o = openJobs('you')[0]; if (!o || !ixBoard.take(o.id)) return; const j = myJob(); jobStops(j).forEach((s, k) => jobStepDone(j.id, k)); ixBoard.turnIn(j.id); })()"); g.step(1)   # a job of yours done, as (p): the ladder's first row needs one
    ask = None; m = 481
    while m < 1020:
        ev(f"setShipNow({1440 + m})"); g.step(1); s = ev(FX_LOOK)
        if s[0] and s[0].endswith(':meet') and s[1]: ask = [m, s]; break
        m += 5
    if not check(ask, '(p2) no training ask on Day 2'): g.close(); return
    at = ask[1][1] - 1440
    TAKE = "(() => { const o = openJobs('you').find(x => !x.train); return o && ixBoard.take(o.id) ? myJob().id : null; })()"
    DONE = "(() => { const j = myJob(); if (!j) return null; jobStops(j).forEach((s, k) => jobStepDone(j.id, k)); ixBoard.turnIn(j.id); return j.id; })()"
    def go(mm): ev(f"setShipNow({1440 + mm})"); g.step(1); g.step(1); return ev(FX_LOOK)[5]
    ev(f"setShipNow({1440 + at - 20})"); g.step(1); a = ev(TAKE); before = go(at - 14)
    ev(DONE); b = ev(TAKE); inside = go(at - 11)
    print('   job taken before the window:', a, '-> arrow at 14 before:', before, '| turned in, next taken at 12 before:', b, '-> arrow:', inside)
    check(a and not (before and ' with ' in before), f"(p2) a job taken before the window keeps the arrow (the playtest patch 1, #7) ({before})")
    check(b and inside and ' with ' in inside, f"(p2) a job taken inside the window should not keep the meeting's arrow away ({inside})")
    if g.errors: fail('(p2) page errors: ' + ' | '.join(g.errors[:5]))
    g.close()

# (p3) FX4 (p5-fix4): Calder's call (m6, Day 8, 10:30; queue off): its arrow cleared the moment you came into her office, so
# your job's arrow came straight back and led you out before the meeting began (up to a ship minute later). Now in the
# room it stays (as "Wait here for Calder" once a minute ticks) until the meeting starts; then her walk to the pipe takes it
def fx_inc_wait(pw):
    print('(p3) FX4, Calder\'s call: the arrow stays in her office until the meeting starts (queue off):')
    g = Game(pw, sys.argv[1]); ev = g.ev
    ev("setShipNow(1020)"); g.step(2); t0 = 7 * 1440 + 9 * 60; ev(f"setShipNow({t0})"); g.step(2)
    ok0 = ev(f"""(() => {{ if (!WORK_MECH.m6) return null; const W = worksInit(), row = ladderRow('m6'); W.cur = {{ id: 'm6', st: 'ask', d: 8, by: 'calder', occ: null, j: null, w: 0 }}; return trainOffer(row, W.cur, 8, {t0}); }})()""")
    if not check(ok0, f'(p3) no m6 call set for Day 8 ({ok0})'): g.close(); return
    LOOK = "(() => { const c = SHIP.works.cur, r = c && c.occ && SHIP.occasions.find(x => x.key === c.occ); return [c ? c.st : null, r ? !!r.met : null, IX_GOAL ? IX_GOAL.label : null, typeof DIALOGUE !== 'undefined' && DIALOGUE ? DIALOGUE.id : null]; })()"
    PUT = "(io => { const o = OCCASIONS['works.m6']; if (deckDef.num !== o.deck) goToDeck(o.deck); const k = io ? o.room : Object.keys(ROOM_TILES).find(k => k !== o.room && ROOM_TILES[k].length > 4); player.obj.position.copy(cellPos(...ROOM_TILES[k][0])); })"
    def at(m): ev(f"setShipNow({7 * 1440 + m})"); g.step(1); g.step(1); return ev(LOOK)
    ev(f"{PUT}(false)")
    for m in range(620, 632): call = at(m)
    ev(f"{PUT}(true)"); g.step(3); arrive = ev(LOOK)
    met = at(632)
    if met[3]: ev("dialogueEnd(true)")
    after = [at(m)[2] for m in range(633, 636)]
    print('   the call, out of the room:', call, '| into her office (same minute):', arrive, '| next minute:', met, '| after:', after)
    check(call[2] and 'Calder' in call[2], f"(p3) the call's arrow is up at 10:30 ({call})")
    check(arrive[2] and 'Calder' in arrive[2], f"(p3) coming into her office before the meeting starts, the call's arrow should stay (it cleared: {arrive})")
    check(met[1] and any(a and a.startswith('Follow') for a in after), f"(p3) the meeting plays, then her walk to the pipe takes the arrow ({met}, {after})")
    if g.errors: fail('(p3) page errors: ' + ' | '.join(g.errors[:5]))
    g.close()

# (q) FX1 (patch-p5-fix1): the arrow and tracking lifecycle, a fresh page, on paper. A new game starts with job tracking
# on; tracking your bunk, or a device "go" (the Jobs app's board), no longer switches it off (and a "go" clears itself on
# arrival); tracking "On shift" is your job's arrow (the clock, not the bay's middle); at 17:00 with a job in hand the
# arrow says clock out; an empty board says so, once; the shower arrow from Deck 5 goes to the junior washroom, not a
# cabin's; a lesson asked at 06:00 is never before 09:15; a training on Tracked names its teacher, time and place; the
# test job's arrow goes when its time is up; a tap on Deck 5's light relays (your job) starts the work.
FX_LIFE = r"""(() => {
  const out = {}, P = SHIP.player, said = [], kt = toast; toast = (a, b) => said.push(a + ': ' + b);
  try {
  P.track = null; newGameStart(false); simFlush && simFlush(); out.fresh = P.track === undefined ? 'on' : P.track;
  P.track = undefined; clearGoal(); trkTap('place:bed'); out.bed = [P.track === null ? 'off' : 'on', IX_GOAL && IX_GOAL.label]; clearGoal();
  P.track = undefined; DEVICE_APPS.get('jobs').act('board'); out.go = [P.track === null ? 'off' : 'on', IX_GOAL && IX_GOAL.trk]; clearGoal();
  careerInit(); let d = 2; while (!playerShiftOn(d)) d++; out.d = d;
  setShipNow((d - 1) * 1440 + 450); P.track = undefined;
  const sh = trkItems().find(x => /^shift:/.test(x.key)); out.shiftRow = sh ? [sh.title, !!sh.work, sh.sub] : null;
  out.shiftOn = sh ? trkOn(sh) : null; setGoal({ deck: 3, room: 'M', label: 'x', trk: 'meal:x' }); if (sh) trkTap(sh.key); out.shiftTap = [P.track === null ? 'off' : 'on', IX_GOAL && IX_GOAL.label];
  setShipNow((d - 1) * 1440 + 490); out.at0810 = (goalNow() && goalNow().label) || ((ixJobStep() || {}).label); clearGoal();
  careerClock(shipNow()); const o = openJobs('you')[0]; if (o) ixBoard.take(o.id);
  setShipNow((d - 1) * 1440 + 1025); out.out1705 = (ixJobStep() || {}).label;
  const mj = myJob(); if (mj) dropJob(mj.id);
  { setShipNow((d - 1) * 1440 + 600); const ci0 = SHIP.career.ci; SHIP.career.ci = Math.max(1, Math.floor(shipNow())); const rts = roundTrainStep, js = openJobs('you');   // the round's arrow: free hands only (RV6)
    roundTrainStep = () => ({ step: 'take', job: js[0] && js[0].id }); clearGoal(); RG_LAST = ''; roundGuide(); const free = IX_GOAL && IX_GOAL.label;
    clearGoal(); RG_LAST = ''; if (js[1]) ixBoard.take(js[1].id); roundGuide(); out.round = [free, IX_GOAL ? IX_GOAL.label : null, !!myJob()];
    const mj2 = myJob(); if (mj2) dropJob(mj2.id); roundTrainStep = rts; RG_LAST = ''; clearGoal(); SHIP.career.ci = ci0; }
  setShipNow((d - 1) * 1440 + 600); const keep = SHIP.jobs; const oj = openJobs; openJobs = () => []; said.length = 0; out.emptyStep = (ixWorkStep() || {}).label || null; out.emptyOpen = openJobs('you').length; out.empty = said.slice(); ixWorkStep(); out.emptyTwice = said.length; openJobs = oj; SHIP.jobs = keep;
  goToDeck(5); clearGoal(); NEED_GOAL = null; needGoal('hygiene'); out.shower = IX_GOAL && [IX_GOAL.deck, IX_GOAL.place, IX_GOAL.label]; needGoalClear(); clearGoal();
  { SHIP.works = null; SHIP.occasions.length = 0; setShipNow((d - 1) * 1440 + 360); const W = worksInit(); W.log.push(['x', d, 0, 'service']); const c = { id: 'm5', st: 'ask' }; W.cur = c;
    trainOffer(ladderRow('m5'), c, d, (d - 1) * 1440 + 360); const r = SHIP.occasions.find(x => x.key === c.occ); out.ask0600 = r ? hhmm(r.at % 1440) : null;
    const it = r && trkItems().find(x => x.sec === 'on' && x.goal && /Training/.test(x.title)); out.occ = it && [it.title, it.sub, it.goal.label];
    const items = trkItems().filter(x => x.sec === 'on').map(x => x.title); out.order = items;
    SHIP.works = null; SHIP.occasions.length = 0; }
  { const m = machineList().find(x => x.deck === 4) || machineList()[0], t = shipNow(); const j = { id: 'fx-test', machine: m.id, deck: m.deck, room: m.room, kind: 'service', status: 'open', posted: t, found: t, until: t + 30, parts: [], title: 'Test' }; SHIP.jobs.push(j);
    clearGoal(); promoTestTell({ j: 'fx-test', by: 'calder' }); out.test = IX_GOAL && [IX_GOAL.label, IX_GOAL.trk, IX_GOAL.trkTo === j.until];
    setShipNow(t + 31); trkDoneCheck(); out.testAfter = IX_GOAL && IX_GOAL.label; SHIP.jobs = SHIP.jobs.filter(x => x !== j); clearGoal(); }
  { goToDeck(5); clearGoal(); const t = shipNow(), m = machineById('5-junction-1');   // the light relays' own tap starts the work (arrows_check: "Repair the light relays" up all day)
    const j = { id: 'fx-relays', machine: m.id, deck: m.deck, room: m.room, kind: 'chore', chore: 'fault', target: m.id, title: 'Reset a tripped breaker: light relays', parts: [], stops: [{ tag: 'fault', placeId: '5-junction-1-svc', mins: 10 }], status: 'claimed', claimedBy: 'you', posted: t, found: t, start: t };
    SHIP.jobs = SHIP.jobs.filter(x => !(x.claimedBy === 'you' && x.status === 'claimed')); SHIP.jobs.push(j); MACH_REV++; actEnd(true);
    const it = ITEMS.find(i => i.t === 'Light relays'), p = it && it.hit.getWorldPosition(new THREE.Vector3()), s = placeSpot(panelPlace(m.id)); player.obj.position.set(s.x, 0, s.z);
    out.relays = [!!it && !!playerTap(it, p.clone(), p.clone()), ACT ? ACT.kind : null]; actEnd(true); SHIP.jobs = SHIP.jobs.filter(x => x !== j); MACH_REV++; }
  } catch (e) { out.err = String(e && e.stack || e).slice(0, 300); }
  toast = kt; return out;
})()"""
def fx_lifecycle(pw):
    print('(q) FX1, the arrow and tracking lifecycle (a fresh page):')
    g = Game(pw, sys.argv[1]); r = g.ev(FX_LIFE); print('  ', json.dumps(r))
    check(not r.get('err'), f"(q) stopped: {r.get('err')}")
    check(r.get('fresh') == 'on', f"a new game starts with job tracking on ({r.get('fresh')})")
    check(r.get('bed') == ['on', 'Your bunk'] and r.get('go') == ['on', 'go:The job board, in the Works bay'], f"tracking your bunk or a device go keeps job tracking on; a go clears on arrival ({r.get('bed')}, {r.get('go')})")
    check(r.get('shiftRow') and r['shiftRow'][1] and r.get('shiftOn') and r.get('shiftTap') == ['on', None] and r.get('at0810') == 'Clock in at the time clock', f"On shift is your job's arrow: the clock at 08:10 ({r.get('shiftRow')}, {r.get('shiftTap')}, {r.get('at0810')})")
    check(r.get('out1705') == 'Shift over: clock out at the time clock', f"17:05 with a job in hand: clock out ({r.get('out1705')})")
    check(r.get('emptyStep') is None and len(r.get('empty') or []) == 1 and 'board' in r['empty'][0].lower() and r.get('emptyTwice') == 1, f"an empty board says so, once ({r.get('empty')}, {r.get('emptyTwice')})")
    check(r.get('shower') and r['shower'][1].startswith('4-shower-'), f"the shower arrow from Deck 5: the junior washroom ({r.get('shower')})")
    check(r.get('ask0600') and r['ask0600'] >= '09:15', f"a lesson asked at 06:00 is after the shift starts ({r.get('ask0600')})")
    check(r.get('occ') and ' with ' in r['occ'][0] and ' with ' in r['occ'][2] and ':' in r['occ'][2], f"a training on Tracked names its teacher, time and place ({r.get('occ')})")
    check(r.get('test') == ['Your test job', 'career:test', True] and r.get('testAfter') is None, f"the test job's arrow goes when its time is up ({r.get('test')}, {r.get('testAfter')})")
    check(r.get('round') and r['round'][0] == 'Take your first round at the job board' and r['round'][1] is None and r['round'][2], f"the round's arrow with free hands; holding another job, that job leads ({r.get('round')})")
    check(r.get('relays') == [True, 'job'], f"a tap on the light relays starts your job there ({r.get('relays')})")
    if g.errors: fail('(q) page errors: ' + ' | '.join(g.errors[:5]))
    g.close()

with sync_playwright() as pw:
    if '--fx' in sys.argv:                                # only part (p): python3 career_check.py BUILD.html --fx
        fx_guidance(pw); fx_window_job(pw); fx_inc_wait(pw); fx_lifecycle(pw); print('CAREER CHECK OK' if ok else 'CAREER CHECK FAILED'); sys.exit(0 if ok else 1)
    g = Game(pw, sys.argv[1])
    errors = g.errors
    ev = g.ev

    print('(a) Step 1 as built: no sub-blocks, nothing opens:')
    hidden = ev("deviceApps().some(a => a.id === 'works')")
    r = ev(f"({PAPER})({{ plan: 'none', days: 14 }})")
    ops = [x['op'] for x in r['days'] if x['op']]
    print(f"  the Works app on Day 1 morning: {'shown' if hidden else 'hidden'}; opened {ops}, trained {r['trained']}, head: {r['head']}")
    check(not hidden, 'the Works app shows before Day 1\'s shift has ended')
    check(not ops and not r['trained'] and not r['occ'], 'with no mechanic in the build a ladder row opened')
    check(r['works'] is not None, 'SHIP.works not made after Day 1')
    shown = ev("deviceApps().some(a => a.id === 'works')")
    check(shown, 'the Works app is hidden once SHIP.works exists')

    print('(b) A steady player, every row with a stand-in sub-block, Days 1-9:')
    st = ev(f"({PAPER})({{ plan: 'steady', days: 9 }})")
    story(st)
    op = opened_on(st)
    print(f"  opened: {op}\n  trained: {st['trained']}\n  asked on: {st['asks']}\n  teacher's job and yours: {st['teach']}\n  meetings: {st['occ']}\n  Mail: {st['mail']}")
    print(f"  Record: {st['head']}\n  locker: {st['locker']}\n  Works app: {st['view']}")
    for k, d in LADDER.items():
        check(op.get(k) == d, f"steady: {k} opened on Day {op.get(k)}, the table says Day {d}")
    pacing(st, 'steady')
    for k in ('m1', 'm4', 'm5', 'm7', 'm6'):
        t = st['teach'].get(k, {})
        check(k in st['trained'], f'steady: {k} never trained')
        check(t.get('by') not in (None, 'you') and t.get('you') == 'you', f"steady: {k}'s training: the teacher's job then yours ({t})")
    check(st['teach'].get('m7', {}).get('by') == 'halloran-emeka', f"steady: the scanner on Day 5 is Emeka Halloran's to teach ({st['teach'].get('m7')})")
    check(st['works']['tools'].get('clipboard') and st['works']['tools'].get('scanner'), f"steady: tools given {st['works']['tools']}")
    check(len(st['mail']) >= 5 and len(st['occ']) >= 5 and all(o['status'] != 'missed' for o in st['occ']), f"steady: an ask (Mail and appointment) for each big training: {st['occ']}")
    b = {x['d']: x['band'] for x in st['days']}
    check(b.get(8) == 'relied', f"steady: not 'Relied on' by the end of Day 8 ({b.get(8)}, xp {st['days'][7]['xp']})")
    check(b.get(4) != 'relied', 'steady: "Relied on" before Day 5')
    check('Relied on' in (st['head'] or '') or b.get(9) == 'relied', 'the Record says the band')

    print('(c) A very busy player:')
    bz = ev(f"({PAPER})({{ plan: 'busy', days: 8 }})")
    print('   ', ', '.join(f"Day {x['d']}: {x['jobs']} jobs, xp {x['xp']} {x['band']}" for x in bz['days']))
    check(all(x['band'] != 'relied' for x in bz['days'] if x['d'] <= 4), 'busy: "Relied on" before Day 5')
    pacing(bz, 'busy')

    print('(d) A lazy player, Days 1-28:')
    lz = ev(f"({PAPER})({{ plan: 'lazy', days: 28 }})")
    lop = opened_on(lz)
    print(f"  opened: {lop}\n  trained: {lz['trained']}\n  asked on: {lz['asks']}")
    pacing(lz, 'lazy')
    for k, d in LADDER.items():
        if k == 't2': continue
        check(k in lop and lop[k] >= d, f'lazy: {k} lost or early ({lop.get(k)})')
        check(k in lz['trained'], f'lazy: {k} never trained')
    check(any(len(v) >= 2 for v in lz['asks'].values()), f"lazy: a missed ask isn't offered again: {lz['asks']}")
    check(sum(lop.values()) > sum(op.get(k, 0) for k in lop), 'lazy: no later than the steady player')

    print('(e) Bands, skill words, tools, penalties:')
    e = ev("""(() => { SHIP.works = null; setShipNow(1440 + 600); const W = worksInit(), out = {};
      out.bands = [0, 7, 8, 17, 18, 29, 30, 39, 40, 90].map(x => { W.xp = x; return worksBand(); });
      W.rank = 'officer'; W.xp = 0; out.officer = worksBandWord(); W.rank = 'junior';
      out.words = [0, 4, 5, 14, 15].map(n => { W.sk.oven = n; return skillWord('oven'); });
      out.give = toolGive('scanner'); out.again = toolGive('scanner'); out.has = hasTool('scanner'); W.tr.m7 = 5; for (let k = 0; k < 10; k++) worksUse('m7'); out.useWear = toolWear('scanner'); (W.op[99] = W.op[99] || []).push('m11'); for (let k = 0; k < 10; k++) toolWear('scanner', 2); delete W.op[99]; out.wear = toolWear('scanner');   // M11 (0.45.7): a use doesn't wear the scanner, a scan does (toolWear(id, n of 100))
      W.xp = 10; simNote('shiftMissed', { day: 2 }); out.missed = W.xp; simNote('jobAbandoned', { machine: null, id: 'x' }); out.aband = W.xp; W.xp = 1; simNote('shiftMissed', { day: 3 }); out.floor = W.xp;
      out.before = (() => { SHIP.works = null; setShipNow(1000); return worksInit(); })();
      SHIP.works = null; return out; })()""")
    print('  ', e)
    check(e['bands'] == ['new', 'new', 'steady', 'steady', 'reliable', 'reliable', 'trusted', 'trusted', 'relied', 'relied'], f"bands {e['bands']}")
    check(e['officer'] == 'New officer', 'after a promotion the band reads "New officer"')
    check(e['words'] == ['new to you', 'new to you', 'getting the hang of these', 'getting the hang of these', 'you know these well'], f"skill words {e['words']}")
    check(e['give'] and not e['again'] and e['has'] and e.get('useWear') == 0 and abs(e['wear'] - .2) < 1e-9, 'tools: given once, worn by its scans (toolWear), not again by worksUse')
    check(e['missed'] == 7 and e['aband'] == 5 and e['floor'] == 0, 'a missed shift -3, an abandoned job -2, never below 0')
    check(e['before'] is None, 'SHIP.works made before Day 1\'s shift ended')
    # the first promotion's gatherings (section 14's crewGather, TS3: a planted fault left them standing nobody anywhere):
    # your box on Day 10 at 17:05, Tomas and Pell each on their own open tile by Cabin 4-23's door; and the career-beat
    # guard: with the events base off, no day is an event day
    pg = ev("""(() => { const t0 = shipNow(); setShipNow(9 * 1440 + 17 * 60 + 5);
      const ids = typeof boxCarry === 'function' ? boxCarry(shipNow() + 40) : null, sc = (ids || []).map(id => CREW_SCENE.get(id)), tiles = sc.map(s => s && s.to && s.to.tile ? s.to.tile.join(',') : null);
      (ids || []).forEach(id => crewSceneEnd(id)); setShipNow(t0);
      const ev = typeof eventDay !== 'function' || typeof EV_GUARD_ON === 'undefined' || EV_GUARD_ON ? null : Array.from({ length: 60 }, (_, i) => i + 1).filter(d => eventDay(d));
      return { ids, tiles, ev }; })()""")
    print('  the promotion\'s box carriers:', pg['ids'], pg['tiles'], '| event days with the events base off:', pg['ev'])
    if pg['ids'] is not None:
        check(sorted(pg['ids']) == ['pell', 'tomas'] and all(pg['tiles']) and len(set(pg['tiles'])) == 2, f"the box on Day 10: Tomas and Pell each wait on their own tile by your door ({pg})")
    check(pg['ev'] in (None, []), f"with the events base off the career-beat guard sees no event day (Days 1-60: {pg['ev']})")

    tb = ev("""(() => { const r = worksTabAdd({ id: 'test', title: 'Test', order: 40, view: () => [{ kind: 'text', text: 'hello' }], act: (v, a) => { window.__tabAct = v + ':' + a; } });
      WORKS_TAB = 'test'; const v = worksView(); deviceDo({ app: 'works', do: 'poke', arg: 7 }); const got = window.__tabAct;
      WORKS_TABS.splice(WORKS_TABS.findIndex(x => x.id === 'test'), 1); WORKS_TAB = 'training';
      return { r, tabs: v.blocks[0].items.map(x => x.label), body: v.blocks[1] && v.blocks[1].text, got }; })()""")
    print('  worksTabAdd:', tb)
    check(tb['r'] and tb['tabs'][:3] == ['Training', 'Work log', 'Tools'] and tb['tabs'][-1] == 'Test' and tb['body'] == 'hello' and tb['got'] == 'poke:7', 'worksTabAdd: a tab shows, in order, and gets its verbs')

    eh = ev("""(() => { SHIP.works = null; setShipNow(4 * 1440 + 600); const W = worksInit(); W.cur = { id: 'm7', st: 'do', d: 5, by: 'halloran-emeka', occ: null, j: 'jx', w: 15 }; W.cases = { open: [{ id: 'cjx', job: 'jx' }], done: [] };
      const out = { hold: worksEscortHold('m7') }; worksDone('m7', shipNow()); out.st = W.cur && W.cur.st; out.trainedEarly = W.tr.m7 !== undefined;
      out.esc = (() => { SHIP.jobs.push({ id: 'jx', machine: machineList()[0].id, status: 'done', doneBy: 'you' }); const e = worksEscort({ id: 'halloran-emeka' }, shipNow()); return e && e.mode; })();
      out.clean = JSON.stringify(worksClean(JSON.parse(JSON.stringify(W))).cur) === JSON.stringify(W.cur);
      W.cases.open = []; simNote('caseCalled', { train: true }); out.after = W.tr.m7; out.cur = W.cur; SHIP.works = null; SHIP.jobs = SHIP.jobs.filter(j => j.id !== 'jx'); return out; })()""")
    print('  the escort hold (Day 5):', eh)
    check(eh['hold'] and eh['st'] == 'held' and not eh['trainedEarly'] and eh['esc'] == 'follow' and eh['clean'] and eh['after'] == 5 and eh['cur'] is None, 'worksEscortHold / caseCalled')

    rv = ev("""(() => { SHIP.works = null; SHIP.occasions.length = 0; SHIP.mail = []; for (const r of CAREER_LADDER) WORK_MECH[r.id] = { reserve: (d, at, slot, o) => jobReserve('washer', d, at, slot, o) };
      setShipNow(1440 + 300); const W = worksInit(); W.log.push(['x', 1, 0, 'service']); const out = {}; clearGoal();
      skipTo(1440 + 460); WORKS_TICK.m = -1; out.st = W.cur && W.cur.st; out.toldAsleep = W.cur && W.cur.told;
      worksCareerTick(shipNow() + 1); out.toldUp = W.cur && W.cur.told; out.goalAtAsk = !!(IX_GOAL && / with /.test(IX_GOAL.label));
      { const r = SHIP.occasions.find(x => x.key === W.cur.occ); if (r) worksCareerTick(r.at - 10); out.goal = !!(IX_GOAL && / with /.test(IX_GOAL.label)); clearGoal(); }   // FX1: its arrow from 15 minutes before the meeting
      W.cur = { id: 'm7', st: 'held', d: 2, by: 'calder', occ: null, j: null, w: 0, hold: true }; ladderTick(Math.floor((2 * 1440 + 400) / 60)); out.heldTrained = W.tr.m7;
      deviceDo({ app: 'works', tab: 'tools' }); out.tab = WORKS_TAB; WORKS_TAB = 'training';
      for (const k in WORK_MECH) delete WORK_MECH[k]; SHIP.works = null; return out; })()""")
    print('  asked while asleep, told when up; a stale hold; open on a tab:', rv)
    check(rv['st'] == 'meet' and rv['toldAsleep'] is False and rv['toldUp'] is True and rv['goal'] and not rv['goalAtAsk'], f"an ask made during a sleep is told (toast) when you are up; its arrow comes 15 minutes before the meeting ({rv})")
    check(rv['heldTrained'] is not None, 'a hold left from an earlier day trains you on the next workday')
    check(rv['tab'] == 'tools', 'the Works app opens on a given tab')

    print('(f) The save:')
    sv = ev(f"""(() => {{ const r = ({PAPER})({{ plan: 'steady', days: 2 }}); const W = SHIP.works;
      W.cur = {{ id: 'm4', st: 'do', d: 3, by: 'esposito-yara', occ: 'works.m4@3', j: 'reserve11:x@1', w: 15 }};
      const core = Object.fromEntries(Object.entries(W).filter(([k]) => k in worksClean({{ v: 1 }}))), raw = JSON.stringify(core), back = JSON.stringify(worksClean(JSON.parse(raw)));   // 24 core's fields (sub-blocks keep their own)
      const junk = worksClean({{ v: 1, tier: 'x', rank: 'admiral', xp: -5, tr: {{ m1: 'a', zz: 3 }}, log: 5, tools: {{ bogus: [1, 2], scanner: [3, 7] }}, op: {{ 2: ['m1', 'nope'], x: [] }}, cur: {{ id: 'm1', st: 'eh' }} }});
      return {{ same: raw === back, raw: raw.length, junk, bad: worksClean(null) }}; }})()""")
    print('  round trip:', sv['same'], f"({sv['raw']} bytes); junk:", sv['junk'])
    check(sv['same'], 'worksClean changes a good save')
    j = sv['junk']
    check(j and j['tier'] == 1 and j['rank'] == 'junior' and j['xp'] == 0 and j['tr'] == {} and j['log'] == [] and j['tools'] == {'scanner': [3, 1]} and j['op'] == {'2': ['m1']} and j['cur'] is None, 'worksClean on junk')
    check(sv['bad'] is None, 'worksClean(null) should be none')
    # a real reload, saving on: mid-training, then an old save (no ship.works)
    tmp = WORK / 'test' / '_career_save.html'
    tmp.write_text(instrument(pathlib.Path(sys.argv[1]).read_text()))
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    page = b.new_page(viewport={'width': 600, 'height': 500})
    page.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
    page.add_init_script(INIT)
    page.on('pageerror', lambda e: errors.append(f'pageerror (save): {e}'))
    def load():
        page.goto('file://' + str(tmp)); page.wait_for_function('window.__sc !== undefined', timeout=60000)
        return lambda s: page.evaluate('s => window.__sc(s)', s)
    ev2 = load(); ev2("localStorage.clear()"); ev2 = load()
    w0 = ev2(f"""(() => {{ for (const r of CAREER_LADDER) WORK_MECH[r.id] = {{}}; setShipNow(1440 + 400); const W = worksInit(); W.xp = 12; W.sk.oven = 6; W.log.push(['oven-2@30', 2, 1, 'repair']);
      W.tr.m1 = 2; W.use.m1 = 1; W.op[2] = ['m1']; toolGive('clipboard'); setShipNow(2 * 1440 + 400); WORKS_TICK.h = -1; worksCareerTick();
      const c = W.cur; saveGame(); return {{ works: JSON.stringify(W), cur: c && c.st, occ: SHIP.occasions.filter(r => /^works/.test(r.id)).length }}; }})()""")
    ev2 = load()
    w1 = ev2("(() => { const W = SHIP.works; return { works: JSON.stringify(W), occ: OCCASIONS['works.m4'] ? 'made' : 'missing', ok: !!W } })()")
    print(f"  reload mid-training ({w0['cur']}, {w0['occ']} appointment): same {w0['works'] == w1['works']}, its occasion {w1['occ']}")
    check(w0['cur'] == 'meet' and w0['works'] == w1['works'], 'a reload mid-training changes SHIP.works')
    check(w1['occ'] == 'made', "a reload mid-training loses the training's occasion")
    ev2("localStorage.setItem(SAVE_KEY, JSON.stringify({ v: 2, build: '0.60.7', time: { day: 10, min: 300 }, player: { deck: 4, tile: [7, 3], facing: 0 }, ship: { decks: {} }, crew: {} })); Storage.prototype.setItem = () => {}")
    ev2 = load()
    old = ev2("""(() => { const out = { works: SHIP.works }; for (const r of CAREER_LADDER) WORK_MECH[r.id] = { reserve: (d, at, slot, o) => jobReserve('washer', d, at, slot, o) }; SHIP.jobs.push({ id: 'old', status: 'done', doneBy: 'you', kind: 'service' });
      WORKS_TICK.h = -1; setShipNow(9 * 1440 + 360); worksCareerTick(); const W = SHIP.works; out.tier = W && W.tier; out.tr = W && W.tr; out.op = W && W.op; return out; })()""")
    print('  an old save on Day 10:', old)
    check(old['tier'] == 1 and old['tr'] == {} and old['op'].get('10', [None])[0] == 'm1' and list(old['op']) == ['10'], 'an old save loads as Tier 1, nothing trained, rounds on its next workday')
    ev2("localStorage.clear()"); b.close()
    lg = ev(f"(() => {{ const r = ({PAPER})({{ plan: 'busy', days: 30 }}); return {{ size: r.size, log: r.works.log.length }}; }})()")
    print(f"  ship.works after 30 busy days: {lg['size']} bytes, log {lg['log']}")
    check(lg['size'] < 3000 and lg['log'] == 30, 'ship.works over 3 KB by Day 30, or the log not cut to 30')

    print('(g) The steady run twice:')
    again = ev(f"({PAPER})({{ plan: 'steady', days: 9 }})")
    same = json.dumps(again, sort_keys=True) == json.dumps(st, sort_keys=True)
    print('  identical:', same)
    check(same, 'the steady run differs the second time')

    print('(i) The Tier 2 test job (24p, Step 3):')
    if not ev("typeof promoPassed === 'function'"): print('  not in this build')
    else:
        tr = ev(f"({PAPER})({{ plan: 'steady', days: 9, t2: 'real' }})")
        print('   steady:', tr['promo'], tr['test'], tr['testJob'], 'Mail', [m for m in tr['mail'] if 'test' in m.lower()])
        check(tr['test'] and tr['test']['passed'] and tr['test']['day'] == 9 and tr['test']['tries'] == 1, f"steady: the test job passed on Day 9, first try: {tr['test']}")
        check(any(p[0] == 'set' and p[1] == 8 for p in tr['promo']), f"steady: told \"tomorrow, your test job\" on Day 8: {tr['promo']}")
        check(tr['testJob'] and tr['testJob'][0][0].startswith('4-scrubber') and tr['testJob'][0][3] == '09:00' and tr['testJob'][0][4] == '15:00' and tr['testJob'][0][2] == 'you', f"steady: the test job, a Deck 4 scrubber held 09:00-15:00, done by you: {tr['testJob']}")
        check(tr['works']['tr'].get('t2') == 9 and tr['works']['cur'] is None and tr['works']['tier'] == 1, f"steady: t2 done, nothing under way, still Tier 1 until the summons: {tr['works']['tr'].get('t2')}, {tr['works']['cur']}")
        lt = ev(f"({PAPER})({{ plan: 'steady', days: 14, t2: 'late' }})")
        print('   late:', lt['promo'], lt['test'])
        dl = [p for p in lt['promo'] if p[0] == 'delayed']
        check(dl and dl[0][1] == 9 and dl[0][2] == 11 and lt['test']['passed'] and lt['test']['tries'] == 2 and lt['test']['day'] == 11, f"late: the test left on Day 9 is set again two workdays on (Day 11) and passed then: {lt['promo']}, {lt['test']}")
        check(all(p[1] >= 9 for p in lt['promo'] if p[0] == 'start'), 'a test job before Day 9')

    print('(j) The summons and the promotion (24p):')
    if not ev("typeof promoPromote === 'function'"): print('  not in this build')
    else:
        SUM = PAPER.replace("      const W = SHIP.works, c = W && W.cur;\n", """      { const r = SHIP.occasions.find(x => x.id === 'promoSummons' && x.status === 'asked');   // the summons: there at 11:00 (t2: 'real'), or not ('away')
        if (r && t >= r.at && t < r.at + r.len && t2 === 'real' && !r.met) { r.met = true; const sc = MEETING_SCRIPTS['promo.officer']; sc.onPick(2, {}); sc.onEnd(true); }
        if (r && t2 === 'away') for (let m = 0; m < 60; m += 5) worksCareerTick(t + m);
        const q = SHIP.occasions.find(x => x.id === 'promoCeremony' && x.status === 'asked');   // the ceremony: there at 17:15, or not
        if (q && t2 === 'real' && t >= q.at - 15 && t < q.at + q.len && !q.met) { worksCareerTick(q.at); q.met = true; const sc = MEETING_SCRIPTS['promo.ceremony']; sc.onPick(0, {}); sc.onEnd(true); }
        if (q && t2 === 'away') for (let m = 0; m < 60; m += 5) worksCareerTick(t + m); }
      const W = SHIP.works, c = W && W.cur;\n""")
        def run(mode, days):
            return ev(f"""(() => {{ window.__xpAt = null; const pn = {{ promoted: [], moved: [], commissioned: [] }}, keep = k => n => pn[k].push(n); const st = onSim('promoted', () => {{ window.__xpAt = [SHIP.works.xp, worksBandWord()]; }}), sts = Object.keys(pn).map(k => onSim(k, keep(k))); const out = ({SUM})({{ plan: 'steady', days: {days}, t2: '{mode}' }});
              out.rank = [SHIP.works.tier, SHIP.works.rank, Math.round(SHIP.works.xp), worksBandWord ? worksBandWord() : null, playerTier(), playerRank()];
              out.plan = promoPlan(); out.reply = flag('promo.reply'); out.promoted = pn.promoted.map(n => [Math.floor(n.t / 1440) + 1, hhmm(n.t % 1440), n.how]);
              out.summ = SHIP.occasions.filter(r => r.id === 'promoSummons').map(r => [Math.floor(r.at / 1440) + 1, hhmm(r.at % 1440), r.status, !!(r.f && r.f.warn), r.f && r.f.seek ? hhmm(r.f.seek % 1440) : null]);
              out.juniorHeld = forYou({{ urgency: 0, kind: 'haul', junior: true, tier: 1 }}); out.mailC = SHIP.mail.filter(m => /Calder|Marrow/.test(m.from)).map(m => m.subject);
              out.home = [SHIP.works.home, SHIP.works.done.slice(), typeof worksHomeOpen === 'function' && worksHomeOpen(4, 'W'), doorOpenFor('W', 'player', shipNow(), 4), doorOpenFor('V', 'player', shipNow(), 4)];
              out.moved = pn.moved.map(n => [Math.floor(n.t / 1440) + 1, hhmm(n.t % 1440), n.how]);
              out.cer = SHIP.occasions.filter(r => r.id === 'promoCeremony').map(r => [Math.floor(r.at / 1440) + 1, hhmm(r.at % 1440), r.deck + '/' + r.room, r.f && r.f.seek ? hhmm(r.f.seek % 1440) : null]);
              out.com = pn.commissioned.map(n => [Math.floor(n.t / 1440) + 1, n.how]); out.pip = [PLAYER_SPEC.rank, player.spec.rank];
              out.keep = (SHIP.social && SHIP.social.keepsakes || []).filter(k => k.from === 'marrow').map(k => k.what); out.guests = promoGuests(); out.head = (worksRecordHead() || {{}}).text;
              out.mailCer = SHIP.mail.filter(m => /Captain/.test(m.from)).map(m => m.subject);
              const W = SHIP.works, C = worksClean(JSON.parse(JSON.stringify(W))); out.clean = ['tier', 'rank', 'xp', 'test', 'home', 'done', 'ms'].every(k => JSON.stringify(C[k]) === JSON.stringify(W[k]));
              out.xpAt = window.__xpAt; st(); sts.forEach(f => f()); return out; }})()""")
        sm = run('real', 12)
        print('   there:', sm['summ'], sm['promoted'], sm['rank'], 'reply', sm['reply'], sm['plan'])
        check(sm['summ'] and sm['summ'][0][:2] == [10, '11:00'] and sm['summ'][0][3], f"the summons: Day 10 at 11:00 in Calder's office, warned at 10:30: {sm['summ']}")
        check(sm['promoted'] and sm['promoted'][0][0] == 10 and sm['promoted'][0][2] == 'met' and len(sm['promoted']) == 1, f"promoted once, on Day 10 at the scene: {sm['promoted']}")
        check(sm['rank'][:2] == [2, 'officer'] and sm['xpAt'] == [0, 'New officer'] and sm['rank'][4] == 2 and sm['rank'][5] == 'officer' and sm['reply'] == 3, f"Tier 2 officer, xp from 0 (New officer), the reply remembered: {sm['rank']}, {sm['xpAt']}, {sm['reply']}")
        check(sm['works']['done'][:1] == ['summons2'] and ['officer', 10] in sm['works']['ms'] and sm['plan']['move']['day'] == 10 and sm['plan']['ceremony']['day'] == 11, f"done and milestones, the plan: {sm['works']['done']}, {sm['works']['ms']}, {sm['plan']}")
        check(not sm['juniorHeld'], 'a junior job is still held for you as an officer')
        print('   the move:', sm['moved'], sm['home'])
        check(sm['home'][0] == '4-23' and 'move2' in sm['home'][1] and sm['home'][2] and sm['home'][3] and not sm['home'][4], f"the move: 4-23 is yours (home, done, its door opens for you, not the other spare's): {sm['home']}")
        check(sm['moved'] and sm['moved'][0][0] == 10 and sm['moved'][0][1] <= '17:30' and len(sm['moved']) == 1, f"moved once, on Day 10 by 17:30: {sm['moved']}")
        print('   the ceremony:', sm['cer'], sm['com'], 'pip', sm['pip'], sm['keep'], sm['guests'], sm['mailCer'])
        check(sm['cer'] and sm['cer'][0][:3] == [11, '17:15', '1/O'] and sm['com'] == [[11, 'met']], f"the ceremony on Day 11 at 17:15 in the observation room, commissioned once: {sm['cer']}, {sm['com']}")
        check(sm['pip'] == [1, 1] and sm['keep'] and 'commissioned officer, day 11' in (sm['head'] or '').lower() and 'ceremony2' in sm['works']['done'] and ['commissioned', 11] in sm['works']['ms'], f"the pip, the framed commission, the Record: {sm['pip']}, {sm['keep']}, {sm['head']}")
        check(sm['guests'][:4] == ['marrow', 'vance', 'calder', 'torres-zeke'] and len(sm['guests']) <= 7, f"the ceremony's guests: {sm['guests']}")
        check(sm['clean'], 'the save: worksClean keeps tier, rank, xp, test, home, done and ms after the promotion')
        sm2 = run('real', 12)
        check(json.dumps([sm2[k] for k in ('summ', 'promoted', 'moved', 'cer', 'com', 'guests', 'test')], sort_keys=True) == json.dumps([sm[k] for k in ('summ', 'promoted', 'moved', 'cer', 'com', 'guests', 'test')], sort_keys=True), 'the promotion run twice differs')
        aw = run('away', 12)
        print('   away:', aw['summ'], aw['promoted'], aw['mailC'])
        print('   away, the ceremony:', aw['cer'], aw['com'])
        check(aw['cer'] and aw['cer'][0][3] == '17:30' and aw['com'] == [[11, 'mail']], f"away: Calder sets off to walk you up at 17:30; commissioned by Mail by 19:00 anyway: {aw['cer']}, {aw['com']}")
        ev("promoPip()")
        check(aw['summ'] and aw['summ'][0][4] == '11:15' and aw['promoted'] and aw['promoted'][0][0] == 10 and aw['promoted'][0][2] == 'mail' and aw['rank'][1] == 'officer', f"away: Calder sets off to find you at 11:15; promoted by Mail the same day anyway: {aw['summ']}, {aw['promoted']}")

    print('(k) The turn-in card\'s gains (Step 3, for the HUD engineer):')
    tg = ev("""(() => { const j = { id: 'gaintest@1', kind: 'chore', machine: null, title: 'Test', stops: [], parts: [], status: 'claimed', claimedBy: 'you', workDone: true, meters: [{ key: 'air', name: 'Air', gain: 2.5 }, { key: 'power', name: 'Power', gain: 0 }] };
      SHIP.jobs.push(j); careerJobIn({ id: j.id, step: 'turnin', machine: null }); careerJobIn({ id: j.id, step: 'turnin', machine: null }); const g = j.gains; SHIP.jobs = SHIP.jobs.filter(x => x !== j); return g || null; })()""")
    print('  ', tg)
    check(tg and tg['rep'] and len(tg['rep']) == 1 and tg['rep'][0]['dept'] == 'works' and 'add' not in tg['rep'][0] and tg['meters'] == [{'sys': 'air', 'name': 'Air', 'add': 2.5}], f"turn-in gains: rep in words (no number), the ship meters it raised: {tg}")

    print('(l) Clock-in and clock-out reminders (playtest patch 1, note 20, section 15\'s clockRemindTick):')
    if not ev("typeof clockRemindTick === 'function'"): print('  not in this build')
    else:
        # on paper, minute by minute from 06:00 to 19:00 on workdays after the first week: the player on Deck 4 (so off
        # Deck 5 after the shift), nothing on screen; toasts and Mail caught as they come
        ck = ev("""(() => {
          const was = toast, seen = []; toast = (t, x) => { seen.push([SHIP.time.day, hhmm(Math.floor(SHIP.time.min)), t, x]); };
          SHIP.career = null; SHIP.rep = null; SHIP.mail = []; SHIP.occasions.length = 0; SHIP.notes = []; SHIP.player.clockRm = { d: 0, s: 0, n: 0, o: 0, a: 0 }; CLOCK_RM_LOG.length = 0;
          const at = (d, m) => { setShipNow((d - 1) * 1440 + m); return shipNow(); }, out = { days: [] };
          const day = (d, act) => { const s0 = seen.length, l0 = CLOCK_RM_LOG.length, m0 = SHIP.mail.length; let trk = {};
            for (let m = 360; m <= 1140; m++) { const t = at(d, m); TOAST_AT = -1e9; POP.busy = false; document.getElementById('toast').classList.remove('show'); careerTick(t); if (act) act(m, t); clockRemindTick(t);
              if (m === 560 || m === 1015 || m === 1030) { const it = clockTrkItem(); trk[hhmm(m)] = it ? it.title + ' @' + it.tag : null; } }
            const r = { d, shift: playerShiftOn(d), stages: CLOCK_RM_LOG.slice(l0).map(x => hhmm(x[1]) + ' ' + x[2]), toasts: seen.slice(s0).filter(x => x[2] === 'Time clock').map(x => x[1] + ' ' + x[3]),
              mail: SHIP.mail.filter(x => Math.floor(x.at / 1440) + 1 === d).map(x => x.from + ': ' + x.subject), run: SHIP.player.clockRm.n, trk }; out.days.push(r); return r; };
          let d = 9; const work = () => { while (!careerRota(d) || careerOff(d) || friShort(d)) d++; return d++; };
          out.late = day(work(), (m, t) => { if (m === 605) careerClock(t); if (m === 1015) goToDeck(5); if (m === 1022) goToDeck(4); });   // late in, at the bay at five, off Deck 5 at 17:02 without clocking out
          for (let k = 0; k < 3; k++) day(work(), (m, t) => { if (m === 535 || m === 1025) careerClock(t); });   // three good days
          out.easy = day(work(), (m, t) => { if (m === 535 || m === 1025) careerClock(t); });  // eased off
          out.slip = day(work(), (m, t) => { if (m === 1025) careerClock(t); });               // forgot to clock in: back to full
          out.after = day(work(), (m, t) => { if (m === 535 || m === 1025) careerClock(t); });
          const C = SHIP.player.clockRm, sv = {}; SAVE_EXTRA.forEach(f => { try { f(sv.ship ? sv : Object.assign(sv, { ship: {}, player: {} })); } catch (e) {} });
          out.saved = sv.player && sv.player.clockRm; out.size = JSON.stringify(out.saved || {}).length;
          // held: a dialogue on screen keeps the late reminder back until it's over, and nothing on a day off or on leave
          SHIP.player.clockRm = { d: 0, s: 0, n: 0, o: 0, a: 0 }; const dh = work(); careerTick(at(dh, 360));
          POP.busy = true; TOAST_AT = -1e9; const heldSt = clockRemindTick(at(dh, 556)); POP.busy = false; const freeSt = clockRemindTick(at(dh, 557));
          let off = d; while (careerRota(off)) off++; careerTick(at(off, 360)); const offSt = [540, 556, 1030].map(m => { TOAST_AT = -1e9; return clockRemindTick(at(off, m)); });
          // never over an answer toast (CR6's find on 0.64.15: a busy washer's "Washer 2 is free" replaced by "Still not clocked in"):
          // held while it's on screen and for the gap after it, then said
          const te = document.getElementById('toast'); SHIP.player.clockRm = { d: 0, s: 0, n: 0, o: 0, a: 0 }; const da = work(); careerTick(at(da, 360));
          was('Washer 3', 'Washer 3 is busy. Washer 2 is free.'); const ans = [];
          ans.push(clockRemindTick(at(da, 600)), document.getElementById('tx').textContent);
          TOAST_AT = performance.now() - 20000; ans.push(clockRemindTick(at(da, 601)), document.getElementById('tx').textContent);   // its stamp is old but it's still showing
          te.classList.remove('show'); TOAST_AT = performance.now() - 12000; ans.push(clockRemindTick(at(da, 602)));   // gone, inside the gap
          TOAST_AT = performance.now() - 16000; ans.push(clockRemindTick(at(da, 603)));   // gone, gap over
          out.held = [heldSt, freeSt]; out.off = offSt; out.answer = ans;
          toast = was; SHIP.career = null; SHIP.mail = []; SHIP.player.clockRm = { d: 0, s: 0, n: 0, o: 0, a: 0 }; return out; })()""")
        for r in ck['days']: print(f"   Day {r['d']}: {r['stages']} Mail {r['mail']} run {r['run']} Tracked {r['trk']}")
        print('   held by a dialogue, then free:', ck['held'], '| a day off:', ck['off'], '| saved:', ck['saved'], ck['size'], 'bytes')
        L, E, S, A = ck['late'], ck['easy'], ck['slip'], ck['after']
        check(L['stages'][:4] == ['08:30 pre', '09:00 start', '09:15 late', '10:00 later'] and any('clocked in' in t.lower() for t in L['toasts'] if t.startswith('09:15')), f"late to clock in: reminders before, at the start, 15 minutes and an hour in ({L['stages']}, {L['toasts'][:4]})")
        check('16:50 end0' in L['stages'] and '17:00 end' in L['stages'] and '17:02 left' in L['stages'] and any(t.startswith('17:02') and 'without clocking out' in t for t in L['toasts']), f"leaving without clocking out: told as you leave Deck 5 ({L['stages']}, {L['toasts']})")
        check(any('clock out' in m.lower() for m in L['mail']) and L['trk'].get('09:20') == 'Clock in @Now' and L['trk'].get('16:55') == 'Clock out @17:00', f"the auto clock-out Mails you; Tracked shows Clock out from 16:50 ({L['mail']}, {L['trk']})")
        check(E['run'] >= 3 and E['stages'] == [] and E['trk'] == {'09:20': None, '16:55': None, '17:10': None}, f"eased off after three good days: no reminders, no Tracked row on a good day ({E})")
        check(S['stages'][:2] == ['09:15 late', '10:00 later'] and '12:00 last' in S['stages'] and '12:30 mailIn' in S['stages'] and S['run'] == 0 and any('clock-in' in m.lower() for m in S['mail']), f"eased off, forgetting still reminds (late, later, last call, Mail) and ends the run ({S})")
        check(A['stages'][:1] == ['08:30 pre'] and '16:50 end0' in A['stages'] and '17:00 end' in A['stages'] and A['run'] == 1, f"after a slip, the full reminders come back ({A})")
        check(ck['held'] == [None, 'late'] and ck['off'] == [None, None, None], f"held by something on screen, then said; nothing on a day off ({ck['held']}, {ck['off']})")
        print('   an answer toast up, then gone:', ck['answer'])
        check(ck['answer'] == [None, 'Washer 3 is busy. Washer 2 is free.', None, 'Washer 3 is busy. Washer 2 is free.', None, 'later'], f"a reminder never covers a toast on screen, nor in the gap after it ({ck['answer']})")
        check(ck['saved'] is not None and ck['size'] < 60, f"the save: player.clockRm under 60 bytes ({ck['saved']})")

    print('(h) The bridge, by invitation (Step 3):')
    br = ev("""(() => {
      if (typeof bridgeBarred !== 'function') return null;
      const out = {}, was = SHIP.bridgeInvited, log = SHIP.eventLog.slice();
      goToDeck(1); const lob = ROOM_TILES['+'][0], into = ROOM_TILES['B'].find(c => c[0] >= 14 && c[1] >= 4 && c[1] <= 7) || ROOM_TILES['B'][5];
      player.obj.position.copy(cellPos(...lob));
      SHIP.bridgeInvited = false; SHIP.flags['bridge.invited'] = undefined; delete SHIP.flags['bridge.invited'];
      out.youShut = !findPath(lob, into, null, player);
      const crew = { p: { id: 'marrow', dept: 'command' } }; out.crewOpen = !!findPath(lob, into, null, crew);
      out.obsOpen = !!findPath(lob, ROOM_TILES['O'][3], null, player); out.washOpen = !!findPath(lob, ROOM_TILES['w'][0], null, player);
      const bk = [...EDGES.values()].find(e => bridgeBarred(e)); out.tap = bk ? bridgeDoorTap(bk.key) : null; out.tapLobby = bridgeDoorTap('v,6,5');
      SHIP.eventLog = []; out.readyNoEvent = bridgeInviteReady(30); SHIP.eventLog = [{ id: 'ionStorm', startDay: 10, endDay: 16 }]; out.readyAfter = [bridgeInviteReady(16), bridgeInviteReady(17)];
      flagSet('bridge.invited', true); bridgeTick(shipNow()); out.invited = SHIP.bridgeInvited; out.youOpen = !!findPath(lob, into, null, player);
      const sv = {}; SAVE_EXTRA.forEach(f => { try { f(sv.ship ? sv : Object.assign(sv, { ship: {}, player: {} })); } catch (e) {} }); out.saved = sv.ship.bridgeInvited;
      SHIP.bridgeInvited = false; player.obj.position.copy(cellPos(...into)); out.insideOut = !!findPath(into, lob, null, player);
      SHIP.bridgeInvited = was; SHIP.eventLog = log; goToDeck(4);
      return out; })()""")
    print('  ', br)
    if br is None: print('  not in this build')
    else:
        check(br['youShut'] and br['crewOpen'] and br['obsOpen'] and br['washOpen'], f"the bridge shut to you only (crew, the observation room and the washroom open): {br}")
        check(br['tap'] and 'permission' in br['tap']['x'] and br['tapLobby'] is None, f"the bridge door's tap says you need permission (and only that door): {br['tap']}")
        check(br['readyAfter'] == [False, True], f"the invite waits for the first ship-wide event to end: {br['readyAfter']}")
        check(br['invited'] and br['youOpen'] and br['saved'] is True, 'invited: SHIP.bridgeInvited follows bridge.invited, the bridge opens, the save keeps it')
        check(br['insideOut'], 'never shut in: already on the bridge, you can walk out')

    # the Record's "What's next" before the test job (FX3, AR1's play of 0.64.15): with Making it safe done it said "Calder
    # has a test job for you" though no test was set and you weren't "Relied on"; and a junior read "Junior Technician · Junior Officer"
    rn = ev(r"""(() => { const was = SHIP.works; SHIP.works = null; setShipNow(9 * 1440 + 600); const W = worksInit(), out = {};
      for (const r of CAREER_LADDER) if (r.id !== 't2' && r.tier === 1 && WORK_MECH[r.id]) { W.tr[r.id] = 1; (W.op[1] = W.op[1] || []).push(r.id); }
      W.xp = 10; out.low = worksNext(); out.head = worksRecordHead().text;
      W.xp = 999; out.ready = worksNext(); W.test = { tier: 2, day: SHIP.time.day + 1, tries: 0, passed: false }; out.set = worksNext();
      W.rank = 'officer'; W.tier = 2; out.officer = worksRecordHead().text; SHIP.works = was; return out; })()""")
    print('  what\'s next before the test:', rn)
    check('test job for you' not in rn['low'] and 'rely' in rn['low'], f"not Relied on yet: say so, not \"a test job for you\" ({rn['low']})")
    check('test job for you' not in rn['ready'] and 'tomorrow' in rn['set'], f"ready, then set for tomorrow: the real state ({rn['ready']} / {rn['set']})")
    check('Junior Technician · Junior Officer' not in rn['head'] and rn['head'].startswith('Junior Technician.') and rn['officer'].startswith('Technician · Officer.'), f"the Record's title ({rn['head'][:40]} / {rn['officer'][:40]})")

    # your reputation shown changing (FX3, AR1): its word changing is said; a missed shift says what it cost; the turn-in
    # card's chips name yours and the Works team's differently; the Record says "Your reputation"
    rp = ev(r"""(() => { const was = SHIP.works; SHIP.works = null; setShipNow(9 * 1440 + 600); const W = worksInit(), out = {}, tt = () => document.getElementById('tt').textContent + ': ' + document.getElementById('tx').textContent;
      W.xp = 7; document.getElementById('tt').textContent = ''; worksXp(1); out.up = tt();
      W.xp = 8; document.getElementById('tt').textContent = ''; const m0 = SHIP.mail.length; simNote('shiftMissed', { day: 9 }); simFlush(); out.down = tt(); out.mail = SHIP.mail.slice(m0).map(x => x.subject + ': ' + x.body);
      const j = { id: 'fx3-rep', kind: 'service', machine: null, status: 'done', parts: [] }; SHIP.jobs.push(j); simNote('job', { id: 'fx3-rep', step: 'turnin', job: 'service', machine: null, t: shipNow() }); simFlush();
      out.chips = typeof turnInGains === 'function' ? turnInGains(j, null).map(c => c.text) : null; SHIP.jobs = SHIP.jobs.filter(x => x !== j);
      out.head = worksRecordHead().text; SHIP.works = was; return out; })()""")
    print('  your reputation:', rp)
    check('Your reputation' in rp['up'] and 'Steady' in rp['up'], f"its word going up is said ({rp['up']})")
    check('Your reputation' in rp['down'] and 'New' in rp['down'] and any('reputation' in m for m in rp['mail']), f"a missed shift: said and in Mail ({rp['down']} / {rp['mail']})")
    check(rp['chips'] is None or (rp['chips'][:1] == ['Your reputation up'] and len(set(rp['chips'])) == len(rp['chips']) and not any(c == 'Works reputation up' for c in rp['chips'])), f"the turn-in's chips: yours first, the team's under its own name ({rp['chips']})")
    check('Your reputation: ' in rp['head'], f"the Record names it as yours ({rp['head'][:60]})")

    ev("for (const k in WORK_MECH) delete WORK_MECH[k]; SHIP.works = null")
    if errors: fail('page errors: ' + ' | '.join(errors[:5]))
    g.close()
    fx_guidance(pw)
    fx_window_job(pw)
    fx_inc_wait(pw)
    fx_lifecycle(pw)

print('CAREER CHECK OK' if ok else 'CAREER CHECK FAILED')
sys.exit(0 if ok else 1)
