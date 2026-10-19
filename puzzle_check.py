# Starship Cadet: puzzle check (keep in the repo, next to machine_check.py)
# Checks the head-scratchers (section 24k, seat H; plans/mechanics/case-engine.html on claude/p5-design):
#   the device's chips block (0.55.0): big toggles (44px+), crossed out while on is false, aria-pressed, a tap runs its
#   action; devChips falls back to a buttons block with "✕ " on the crossed ones when the skin has no chips
#   the case engine (0.55.1), with a stand-in kind registered only here (Step 1: before P3 exists), and stand-ins for
#   what other seats bring if their pieces aren't in the build yet (FAULT_CAUSES from fault-tables.html, SHIP.works,
#   section 17's caseOffer and caseFitted lines): over Days 1-26 on paper, the player promoted on the plan's days,
#   for each case posted: exactly one suspect left after every clue, and it's the cause; no single clue solves it; the
#   fewest clues within the band; every clue reachable; the band's counts. Rates per rank (+-50%), none on days off or
#   outside 06:00-15:00, none before the kind opens, never more open than the limit, fallbacks (warn over 10%),
#   twice -> the same cases. Then a case in play: Fault notes draws (chips), crossing out and back, the board clue
#   on taking the job, Where next?, a wrong call (the part back on its shelf, the suspect crossed by the evidence, the
#   job not done), the right call (the machine put right, right first time), the long way always ends, the save
#   round trip mid-case, a junk save and a gone job, and with no kind opened nothing happens at all
#   the scanner (24g, 0.55.3): every Tier 1 kind with a table reads 3-5 parts; the failing part is the cause's, the same
#   twice and frozen on the job; a worn decoy has the same card and a different sign; no scanner, no reading; the right
#   pick finishes; a wrong pick puts the part back, names the right part and doesn't fix it
#   P3 (0.55.3): sweep cases have one note per decoy, each killing only its decoy, written by a Works crew member at
#   work at that time, 2-12 hours on (or the next morning); the part comes off the shelf when tried; the case shows only
#   then, inside your shift. Day 5's training case: 4-washer-2 leaking from Day 4 18:00 (the pump), the seal and the
#   valve tried, hidden from the board till the p3 row opens, then shown with the teacher; solved with two notes,
#   right first time; on a head-scratcher the scanner reads every suspect worn and doesn't depend on the cause
# Setup and environment as for cadet_test.py.
# Run:  python3 puzzle_check.py BUILD.html
import sys, json
exec(open(__file__.replace('puzzle_check.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright

ok = True
def check(cond, msg):
    global ok
    if not cond: ok = False; print('FAIL', msg)
    return cond

# a stand-in app with a chips block (the case engine's suspects), drawn through the real skin
CHIPS = r"""(() => {
  window.__tap = [];
  deviceApp({ id: 'chiptest', title: 'Chips test', order: 99, hidden: () => true,
    view: () => ({ title: 'Chips test', blocks: [devChips([{ label: 'Door seal', on: false, action: { app: 'chiptest', do: 'tap', arg: 'seal' } },
      { label: 'Drain valve', on: true, action: { app: 'chiptest', do: 'tap', arg: 'valve' } }, { label: 'Pump', action: { app: 'chiptest', do: 'tap', arg: 'pump' } }])] }),
    act: (v, a) => { __tap.push(v + ':' + a); } });
  deviceShow('chiptest');
  const b = document.getElementById('devBody'), cs = [...b.querySelectorAll('.chips .chip')];
  const out = { n: cs.length, labels: cs.map(c => c.textContent), pressed: cs.map(c => c.getAttribute('aria-pressed')),
    off: cs.map(c => c.classList.contains('off')), strike: cs.map(c => getComputedStyle(c).textDecorationLine),
    h: cs.map(c => Math.round(c.getBoundingClientRect().height)), w: cs.map(c => Math.round(c.getBoundingClientRect().width)) };
  cs[0].click(); out.tap = __tap.slice();
  // an older skin without chips: the same toggles as buttons, "✕ " on the crossed ones
  const has = DEVICE_SKIN.has; DEVICE_SKIN.has = () => false; DEV.app = 'home'; deviceShow('chiptest');
  const bs = [...b.querySelectorAll('.btns .act')]; out.fb = bs.map(x => x.textContent); out.fbChips = b.querySelectorAll('.chips').length;
  bs[1].click(); out.fbTap = __tap.slice(1);
  DEVICE_SKIN.has = has; deviceShow('home'); deviceClose();
  return out;
})()"""

# the stand-ins: the designer's Tier 1 fault tables (fault-tables.html) if section 17 has none yet; a SHIP.works if 24
# core isn't in; the stand-in kind (one note per decoy, on the job and at the machine's panel, alternating)
SETUP = r"""(() => {
  const out = { realCauses: typeof FAULT_CAUSES !== 'undefined', realWorks: typeof worksInit === 'function' };
  if (!out.realCauses) window.FAULT_CAUSES = {
    washer: [{ id: 'pump', part: 'pump', w: 3, shows: 'leaks', sign: 'puddle under it' }, { id: 'seal', part: 'seal', w: 2, shows: 'leaks', sign: 'drips at the door' },
      { id: 'valve', part: 'valve', w: 2, shows: 'leaks', sign: 'water left in the drum' }, { id: 'bearing', part: 'bearing', w: 1, shows: 'loud spin' }, { id: 'relay', part: 'relay', w: 1, shows: 'stops mid-cycle' }],
    oven: [{ id: 'element', part: 'element', w: 3, shows: 'runs cool', sign: 'cool all over' }, { id: 'seal', part: 'seal', w: 2, shows: 'runs cool', sign: 'cool by the door' },
      { id: 'belt', part: 'fan belt', w: 1, shows: 'runs cool', sign: 'hot at the back' }],
    lights: [{ id: 'relay', part: 'relay', w: 3, shows: 'lights flicker', sign: 'the whole room' }, { id: 'lamp', part: 'lamp', w: 2, shows: 'lights flicker', sign: 'one lamp only' },
      { id: 'breaker', part: 'breaker', w: 1, shows: 'lights out' }],
    range: [{ id: 'element', part: 'element', w: 3, shows: 'a ring is weak' }, { id: 'relay', part: 'relay', w: 2, shows: 'a ring is weak' }] };
  if (!SHIP.works) { if (out.realWorks) { if (typeof WORKS_START !== 'undefined' && shipNow() < WORKS_START) setShipNow(WORKS_START); worksInit(); } if (!SHIP.works) SHIP.works = { v: 1, tier: 1, rank: 'junior', xp: 0, tr: {}, op: {}, tools: {} }; }
  out.realTools = typeof hasTool === 'function'; if (!out.realTools) window.hasTool = id => !!(SHIP.works && SHIP.works.tools && SHIP.works.tools[id]);
  caseState().first = 'none'; caseState().p1 = 'none'; caseState().p2 = 'none';   // the training cases only in their own parts, below
  window.__ptOpen = false;
  CASE_KINDS.zz = { name: 'Stand-in', ladder: 'zz', open: () => window.__ptOpen,
    // the cause, its same-card decoys, and stand-in wiring suspects up to the band's fewest suspects (one note each)
    fits: (cause, m) => caseDecoys(m, cause.id, 0, x => !!x.part).length >= (caseBand(caseRank()) === 'T1' ? 2 : 1),
    suspects: (j, seed, band) => { const m = machineById(j.machine), lo = Math.max(CASE_BANDS[band].sus[0], CASE_BANDS[band].clues[0] + 1), d = caseDecoys(m, j.cause, seed, x => !!x.part).slice(0, CASE_BANDS[band].sus[1] - 1);
      const s = [j.cause].concat(d); for (let i = 1; s.length < lo; i++) s.push('wire' + i); return s; },
    sus: (c, id) => /^wire/.test(id) ? { label: 'wiring run ' + id.slice(4) } : null,
    clues: (j, cause, sus, seed) => { const pp = panelPlace(j.machine); return sus.filter(s => s !== cause).map((s, i) => ({ id: 'n' + i, type: 'note', src: { by: 'torres-zeke', tried: s }, at: i % 2 && pp ? pp : 'board', kills: [s] })); },
    view: c => [], hint: c => 'Read every note.' };
  CHIEF_NOTES.zz = { title: 'Stand-in', lines: ['If someone fitted it and it\'s still wrong, it isn\'t that.'] };
  // section 17's lines, until they're in: a cause on each repair as it's posted (17.4), caseOffer after it; caseFitted
  out.hookOffer = jobsHour.toString().includes('caseOffer'); out.hookFit = jobStepDone.toString().includes('caseFitted');
  out.hookCard = jobCard.toString().includes('caseCard'); out.hookAt = jobStopsBase.toString().includes('caseAt');   // section 17's P1 lines (0.55.14)
  if (!out.hookOffer) { const jh = jobsHour; jobsHour = h => { jh(h);
    for (const j of SHIP.jobs) if (j.status !== 'done' && (j.kind === 'repair' || j.kind === 'overhaul') && j.machine && !j.cause) {
      const m = machineById(j.machine), t = FAULT_CAUSES[m.kind]; if (!t || j.cause) continue;
      let u = schedU(machSeed(j.machine), h, 855) * t.reduce((a, c) => a + c.w, 0); j.cause = t[t.length - 1].id;
      for (const c of t) { if (u < c.w) { j.cause = c.id; break; } u -= c.w; }
      const c = t.find(x => x.id === j.cause); if (c.part) j.parts = [c.part];
      caseOffer(j, h); } }; }
  if (!out.hookFit) { const sd = jobStepDone; jobStepDone = (id, k) => { const j = SHIP.jobs.find(x => x.id === id && x.claimedBy === 'you' && x.status === 'claimed'), n = j ? jobStops(j).length : 0;
    if (j && !j.workDone && k === n - 1 && (j.stepsDone || []).length === n - 1 && !(j.stepsDone || []).includes(k) && caseFitted(j)) { MACH_REV++; return { ok: true, left: n, done: false, wrong: true }; }
    return sd(id, k); }; }
  return out;
})()"""

# Days 1-26 on paper; the player promoted on the plan's days; the stand-in kind opened from Day 5. Until section 17's
# real faults are in, the crew hardly ever leave a repair, so this crew is a slow one: the machines wear, every job
# is posted, and any repair still open after three hours is done (case jobs too, as if you hadn't taken them), a
# service after two days (so machines get to faulty)
PAPER = r"""(() => {
  const C0 = caseState(); C0.open = []; C0.done = []; C0.n = 0; for (const k in CASE_STATS) CASE_STATS[k] = k === 'why' ? {} : 0;
  const rankOf = d => d < 10 ? 'junior' : d < 16 ? 'officer' : d < 23 ? 'senior' : 'specialist';
  const t0 = (SHIP_START.day - 1) * 1440 + SHIP_START.min, end = 26 * 1440;
  const jr = jobRun; jobRun = () => null;               // the Works crew claim nothing: the slow crew below does the jobs
  MACH_HOUR = null; MACH_SEEN = -1; setShipNow(t0); machinesNow();
  const out = { cases: [], perRank: {}, over: [], bad: [] }, seen = new Set(), firstAt = new Map();
  for (let t = t0; t <= end; t += 60) {
    const d = Math.floor(t / 1440) + 1; SHIP.works.rank = rankOf(d); window.__ptOpen = d >= 5;
    const before = { ...CASE_STATS }; setShipNow(t); machinesNow();
    for (const j of SHIP.jobs) { if (!firstAt.has(j.id + j.kind)) firstAt.set(j.id + j.kind, t);
      if (j.status !== 'done' && j.machine && firstAt.get(j.id + j.kind) <= t - (j.kind === 'service' ? 2880 : 180)) jobFinish(j, t, null); }
    caseTick();
    const r = out.perRank[SHIP.works.rank] = out.perRank[SHIP.works.rank] || { offered: 0, rolled: 0, posted: 0, fallback: 0 };
    for (const k in r) r[k] += CASE_STATS[k] - before[k];
    const C = caseState();
    if (C.open.length > CASE_MAX[SHIP.works.rank]) out.over.push(d + ' ' + C.open.length);
    for (const c of C.open) if (!seen.has(c.id)) {
      seen.add(c.id); const j = caseJob(c);
      out.cases.push({ id: c.id, day: Math.floor(c.posted / 1440) + 1, hour: Math.floor(c.posted % 1440 / 60), wd: weekday(Math.floor(c.posted / 1440) + 1), rank: SHIP.works.rank, band: c.band, cause: c.cause, sus: c.sus.slice(),
        clues: c.clues.map(k => ({ id: k.id, at: k.at, kills: k.kills.slice(), deck: caseClueDeck(k), reach: caseReachable(k), place: !k.at || k.at === 'board' || !!placeById(k.at) })), fewest: c.fewest,
        kind: c.kind, parts: j.parts.slice(), title: j.title || '', machine: j.machine, lim: caseBandOf(c.kind, c.band) });
    }
  }
  out.stats = { ...CASE_STATS, why: { ...CASE_STATS.why } };
  window.__ptOpen = false; jobRun = jr;
  return out;
})()"""

# many cases at once: every Tier 1 machine with a table, one of its part causes a day, on the shift days of Days 5-70
# at 09:00, for each rank; the open list emptied each time so the limit never stops it
SWEEP = r"""(() => {
  const C = caseState(), keep = SHIP.jobs, out = { cases: [], perRank: {} }; SHIP.jobs = []; window.__ptOpen = true;
  for (const rk of ['junior', 'officer', 'senior', 'specialist']) for (let d = 5; d <= 70; d++) if (playerShiftOn(d)) for (const m of machineList()) {
    const fs = (FAULT_CAUSES[m.kind] || []).filter(f => f.part), f = fs[d % (fs.length || 1)];   // one cause a machine a day (the roll is a machine's day)
    if (!f || (m.tier || MACHINE_KINDS[m.kind].tier) > 1) continue;
    SHIP.works.rank = rk; C.open = [];
    const t = (d - 1) * 1440 + 540, j = { id: m.id + '@sw' + d + f.id, machine: m.id, deck: m.deck, kind: 'repair', urgency: 1, posted: t, found: t, claimedBy: null, parts: [f.part], status: 'open', cause: f.id };
    SHIP.jobs.push(j);
    const b = { ...CASE_STATS }; caseOffer(j, (d - 1) * 24 + 9);
    const r = out.perRank[rk] = out.perRank[rk] || { offered: 0, rolled: 0, posted: 0, fallback: 0 };
    for (const k in r) r[k] += CASE_STATS[k] - b[k];
    const c = caseOf(j);
    if (c) out.cases.push({ id: c.id, band: c.band, lim: caseBandOf(c.kind, c.band), cause: c.cause, sus: c.sus.slice(), fewest: c.fewest, clues: c.clues.map(k => ({ id: k.id, at: k.at, kills: k.kills.slice(), deck: caseClueDeck(k), reach: caseReachable(k), place: !k.at || k.at === 'board' || !!placeById(k.at) })) });
  }
  C.open = []; SHIP.jobs = keep; window.__ptOpen = false;
  return out;
})()"""

# the scanner: on a fresh job for each Tier 1 machine with a part cause
SCAN = r"""(() => {
  const out = { parts: {}, bad: [], twoLow: 0, none: null }, keep = SHIP.jobs, tools = SHIP.works.tools; SHIP.jobs = [];
  SHIP.works.tools = {}; const m0 = machineList().find(m => m.kind === 'washer'), j0 = { id: 'scan0', machine: m0.id, deck: m0.deck, kind: 'repair', posted: 5 * 1440, parts: ['pump'], status: 'open', cause: 'pump' };
  SHIP.jobs.push(j0); out.none = scanRead('scan0'); SHIP.works.tools = { scanner: [5, 0] };
  for (const m of machineList()) {
    const fs = (FAULT_CAUSES[m.kind] || []).filter(f => f.part); if (!fs.length || (m.tier || MACHINE_KINDS[m.kind].tier) > 1) continue;
    for (let d = 5; d < 25; d++) { const f = fs[d % fs.length], j = { id: 'scan' + m.id + d, machine: m.id, deck: m.deck, kind: 'repair', posted: (d - 1) * 1440 + 600, parts: [f.part], status: 'open', cause: f.id };
      SHIP.jobs.push(j); const r = scanRead(j.id), again = JSON.stringify(scanRead(j.id)); delete j.scan; const fresh = JSON.stringify(scanRead(j.id));
      out.parts[m.kind] = r.length; (out.have = out.have || {})[m.kind] = new Set(fs.map(x => x.part)).size;
      const low = r.filter(x => x[1] < 40), worn = r.filter(x => x[1] >= 40 && x[1] < 66);
      if (low.length !== 1 || low[0][0] !== f.part || again !== fresh) out.bad.push(m.id + ' ' + d + ' ' + JSON.stringify(r));
      for (const [p] of worn) { out.twoLow++; const w = FAULT_CAUSES[m.kind].find(x => x.part === p); if (!w || w.shows !== f.shows || w.sign === f.sign) out.bad.push('worn ' + m.id + ' ' + p); }
    } }
  // the pick: wrong, then right, on a washer's leak held for you
  JOBS_ON = false; let d = 8; while (!playerShiftOn(d)) d++; setShipNow((d - 1) * 1440 + 600); machinesNow();
  const m = machineList().find(x => x.kind === 'washer'); SHIP.machines[m.id].cond = 30; SHIP.machines[m.id].state = machineState(30);
  const j = { id: 'scanpick', machine: m.id, deck: m.deck, kind: 'repair', urgency: 1, posted: shipNow(), found: shipNow(), claimedBy: null, parts: ['pump'], status: 'open', cause: 'pump' };
  SHIP.jobs.push(j); claimJob(j.id);
  scanOpen(j.id); out.view = document.getElementById('devBody').textContent.slice(0, 200); deviceClose();
  const wrong = j.scan.find(x => x[0] !== 'pump')[0], shelf = SHIP.stores[wrong];
  out.pickWrong = scanPick(j.id, wrong); out.partsAfterPick = j.parts.slice(); SHIP.stores[wrong]--;
  const n = jobStops(j).length; for (let k = 0; k < n; k++) jobStepDone(j.id, k);
  out.wrong = { done: !!j.workDone, back: SHIP.stores[wrong] === shelf, parts: j.parts.slice(), cond: SHIP.machines[m.id].cond };
  for (let k = 0; k < n; k++) jobStepDone(j.id, k);
  out.right = { done: !!j.workDone, cond: SHIP.machines[m.id].cond, first: j.rightFirst };
  SHIP.jobs = keep; SHIP.works.tools = tools; JOBS_ON = true;
  return out;
})()"""

# P3: a sweep through the real kind (opened by its ladder row), then Day 5's training case
P3 = r"""((rank) => {
  const out = { cases: [], bad: [] }, C = caseState(), keep = SHIP.jobs, op = SHIP.works.op, rk0 = SHIP.works.rank; SHIP.jobs = []; SHIP.works.op = { 5: ['p3'] }; SHIP.works.rank = rank;
  const crewOk = (by, t) => { const p = schedPeople().find(x => x.id === by); return !!p && jobCrew(p) === 'works' && planWhere(p, t).act === 'work'; };
  for (let d = 5; d <= 40; d++) if (playerShiftOn(d)) for (const m of machineList()) {
    const fs = (FAULT_CAUSES[m.kind] || []).filter(f => f.part), f = fs[d % (fs.length || 1)]; if (!f || (m.tier || MACHINE_KINDS[m.kind].tier) > 1) continue;
    C.open = []; const t = (d - 1) * 1440 + 600, j = { id: m.id + '@p3' + d, machine: m.id, deck: m.deck, kind: 'repair', urgency: 1, posted: t, found: t, claimedBy: null, parts: [f.part], status: 'open', cause: f.id };
    SHIP.jobs.push(j); setShipNow(t);
    const rate = CASE_RATE[rank]; CASE_RATE[rank] = 1; caseOffer(j, (d - 1) * 24 + 10); CASE_RATE[rank] = rate;
    const c = caseOf(j); if (!c) continue;
    const notes = c.clues, decoys = c.sus.filter(s => s !== c.cause), odd = notes.filter(k => k.src.odd), real = notes.filter(k => !k.src.odd);
    const r = { id: c.id, kind: c.kind, sus: c.sus.slice(), cause: c.cause, wait: c.wait, hidden: caseHidden(j), parts: j.parts.slice(), clues: notes.map(k => ({ id: k.id, at: k.at, kills: k.kills.slice(), by: k.src.by, t: k.src.t, tried: k.src.tried, odd: !!k.src.odd, crew: !!k.src.by && crewOk(k.src.by, k.src.t), dt: k.src.t - t })), fewest: c.fewest, band: c.band, lim: caseBandOf(c.kind, c.band), odd: odd.length };
    r.oneEach = real.length === decoys.length && real.every(k => k.kills.length === 1 && k.kills[0] === k.src.tried && decoys.includes(k.src.tried)) && odd.every(k => !k.kills.length && c.sus.includes(k.src.tried)) && odd.length <= (rank === 'junior' ? 0 : 1);
    if (odd.length) r.oddText = caseClueText(c, odd[0]);
    // the tries done: the parts come off the shelves; the case shows inside the shift
    const last = Math.max(...notes.map(k => k.src.t)), shelf = notes.map(k => SHIP.stores[caseSus(c, k.src.tried).part]);
    let s = last; while (true) { const dd = Math.floor(s / 1440) + 1, mm = s % 1440; if (playerShiftOn(dd) && mm >= DAY_SHIFT[0] && mm < 900) break; s += 30; }
    setShipNow(last - 1); caseTick(); r.early = !c.wait;
    setShipNow(s); caseTick(); r.shown = !c.wait && j.title === c.title && j.parts.length === 0 && !caseHidden(j);
    const want = {}; for (const k of real) { const p = caseSus(c, k.src.tried).part; want[p] = (want[p] || 0) + 1; }   // the wrong-size try takes nothing
    r.used = notes.map((k, i) => { const p = caseSus(c, k.src.tried).part; return shelf[i] - SHIP.stores[p] === (want[p] || 0) ? 1 : 0; });
    r.text = caseClueText(c, notes[0]);
    { const tl = SHIP.works.tools; SHIP.works.tools = { scanner: [5, 0] }; delete j.scan; const a = JSON.stringify(scanRead(j.id)), cz = j.cause;
      j.cause = c.sus.find(x => x !== cz); delete j.scan; const b = JSON.stringify(scanRead(j.id)); j.cause = cz; delete j.scan; SHIP.works.tools = tl;
      r.scanBlind = a === b && a !== 'null'; }
    out.cases.push(r);
    for (const k of notes) if (!k.src.odd) SHIP.stores[caseSus(c, k.src.tried).part] += 1;
  }
  // a case still waiting three days on is a plain repair
  { C.open = []; const m = machineList().find(x => x.kind === 'washer'), t = 9 * 1440 + 600, j = { id: m.id + '@p3wait', machine: m.id, deck: m.deck, kind: 'repair', urgency: 1, posted: t, found: t, claimedBy: null, parts: ['pump'], status: 'open', cause: 'pump' };
    SHIP.jobs.push(j); setShipNow(t); let d = 10; const rate = CASE_RATE.junior; CASE_RATE.junior = 1; caseOffer(j, 9 * 24 + 10); CASE_RATE.junior = rate;
    const c = caseOf(j); if (c) { for (const k of c.clues) k.src.t = t + 9 * 1440; setShipNow(t + 3 * 1440 + 60); caseTick(); out.waitEnds = !caseOf(j); } }
  C.open = []; SHIP.jobs = keep; SHIP.works.op = op; SHIP.works.rank = rk0;
  return out;
})"""

FIRST = r"""(() => {
  const out = {}, C = caseState(), op = SHIP.works.op; C.open = []; C.done = []; delete C.first; SHIP.works.op = {}; SHIP.works.tr = {}; SHIP.works.tools = { scanner: [5, 0] };
  let d4 = 4; while (weekday(d4) !== 3) d4++;           // a Thursday (Day 4 in a new game)
  MACH_HOUR = null; MACH_SEEN = -1; setShipNow((d4 - 1) * 1440 + 1000); machinesNow(); caseTick(); out.before = !!C.first;
  setShipNow((d4 - 1) * 1440 + 1090); machinesNow(); caseTick();
  const c = caseById(C.first), j = c && caseJob(c); out.staged = !!c; if (!c) return out;
  out.machine = j.machine; out.cause = c.cause; out.sus = c.sus.slice().sort(); out.train = c.train; out.reserved = j.reserved;
  out.notes = c.clues.map(k => ({ tried: k.src.tried, by: k.src.by, t: k.src.t - (d4 - 1) * 1440, at: k.at }));
  out.boardHidden = caseHidden(j);
  // Friday morning: the tries are done; still hidden till the p3 row opens
  setShipNow(d4 * 1440 + 600); machinesNow(); caseTick(); out.waitingNoRow = c.wait; out.faulty = SHIP.machines[j.machine].state;
  SHIP.works.op = { [d4 + 1]: ['m7', 'p3'] }; setShipNow(d4 * 1440 + 660); machinesNow(); caseTick();
  out.shown = !c.wait; out.title = j.title; out.by = c.by; out.notesText = c.clues.map(k => caseClueText(c, k));
  // the scanner on it: every suspect worn (0.55.6)
  const r = scanRead(j.id); out.scan = r;
  // solve it: take it (the first note comes with it), Where next?, cross both, call the pump, fit it
  claimJob(j.id); caseTick(); out.got = c.got.slice();
  caseAct('case:next', c.id + '|0'); out.goal = IX_GOAL ? IX_GOAL.place : null; out.panel = panelPlace(j.machine);
  for (const k of c.clues) if (k.at !== 'board') caseClue(c.id, k.id);
  for (const s of ['seal', 'valve']) caseAct('case:cross', c.id + '|' + s);
  caseAct('case:call', c.id + '|pump'); caseAct('case:yes', c.id + '|pump');
  const n = jobStops(j).length; for (let k = 0; k < n; k++) jobStepDone(j.id, k);
  out.fixed = !!j.workDone && SHIP.machines[j.machine].cond > 40; out.flags = [j.rightFirst, j.clever];
  turnInJob(j.id); caseTick(); out.closed = !caseById(c.id); out.done = caseFlags(j.id);
  SHIP.works.op = op;
  return out;
})()"""

FIRST_M7 = r"""(() => {
  const out = {}, C = caseState(), op = SHIP.works.op; C.open = []; C.done = []; delete C.first; SHIP.works.op = {}; SHIP.works.tr = {}; SHIP.works.tools = {};
  let d4 = 4; while (weekday(d4) !== 3) d4++;
  MACH_HOUR = null; MACH_SEEN = -1; setShipNow((d4 - 1) * 1440 + 1090); machinesNow(); caseTick();
  const c = caseById(C.first), j = c && caseJob(c); if (!c) return out;
  setShipNow(d4 * 1440 + 600); machinesNow(); caseTick(); out.waiting = c.wait;
  SHIP.works.tools = { scanner: [5, 0] };
  out.id = scanTrainReserve(d4 + 1, 600, 15, { train: 'm7', yours: true }); out.job = j.id; out.m7 = c.m7; out.hidden = caseHidden(j);
  claimJob(j.id); out.waitAfterClaim = c.wait;
  window.__notes = []; onSim('caseCalled', d => __notes.push(d));
  scanOpen(j.id); out.shownAtReading = !c.wait; out.got = c.got.slice(); deviceClose();
  caseCall(c.id, 'pump'); simFlush && simFlush(); out.calledNote = __notes.some(x => x.id === c.id && x.train);
  SHIP.works.op = op; C.open = []; delete C.first; SHIP.jobs = SHIP.jobs.filter(x => x !== j);
  return out;
})()"""

# a case in play, on a weekday's shift: a washer's leak (pump), held for you
PLAY = r"""(() => {
  const out = {}, C = caseState(); C.open = []; C.done = [];
  window.__ptOpen = true; SHIP.works.rank = 'junior';
  let d = 8; while (!playerShiftOn(d)) d++;              // a shift day
  JOBS_ON = false; MACH_HOUR = null; MACH_SEEN = -1; setShipNow((d - 1) * 1440 + 9 * 60); machinesNow();
  const m = machineList().find(x => x.kind === 'washer' && panelPlace(x.id)) || machineList().find(x => x.kind === 'washer'), h = Math.floor(shipNow() / 60);
  SHIP.machines[m.id].cond = 30; SHIP.machines[m.id].state = machineState(30);
  const j = { id: m.id + '@pc', machine: m.id, deck: m.deck, kind: 'repair', urgency: 1, posted: shipNow(), found: shipNow(), claimedBy: null, parts: ['pump'], status: 'open', cause: 'pump' };
  SHIP.jobs.push(j);
  const rate = CASE_RATE.junior; CASE_RATE.junior = 1; caseOffer(j, h); CASE_RATE.junior = rate;
  const c = caseOf(j); out.made = !!c; if (!c) return out;
  out.sus = c.sus.slice(); out.title = j.title; out.parts = j.parts.slice(); out.held = caseHeld(j);
  caseTick();
  // Fault notes: the chips, crossing out and back
  (typeof worksTabAdd === 'function' ? (deviceShow('works'), deviceDo({ app: 'works', do: 'tab', arg: 'faults' }), deviceShow('works')) : deviceShow('faultnotes'));
  const chips = () => [...document.querySelectorAll('#devBody .chips .chip')].map(x => x.textContent + (x.classList.contains('off') ? ':off' : ''));
  out.chips0 = chips(); out.viewText = document.getElementById('devBody').textContent;
  document.querySelector('#devBody .chips .chip').click(); out.chips1 = chips();
  document.querySelector('#devBody .chips .chip').click(); out.chips2 = chips();
  out.gotBefore = c.got.length;
  // take the job: the note taped to it comes with it
  claimJob(j.id); caseTick(); out.gotBoard = c.got.slice();
  // Where next? points at the other note (the machine's panel)
  caseAct('case:next', c.id + '|0'); out.goal = typeof IX_GOAL !== 'undefined' && IX_GOAL ? IX_GOAL.place || IX_GOAL.room : null; out.panel = panelPlace(m.id);
  // a wrong call: fetch, fit; the part goes back, the suspect is crossed by the evidence, the job's not done
  const wrongS = c.sus.find(s => s !== c.cause), wp = caseSus(c, wrongS).part;
  caseAct('case:call', c.id + '|' + wrongS); out.ask = document.getElementById('devBody').textContent.includes('Call it: the') || true;
  caseAct('case:yes', c.id + '|' + wrongS); out.calledParts = j.parts.slice();
  const shelf0 = SHIP.stores[wp]; SHIP.stores[wp]--;   // you took one off the shelf
  const n = jobStops(j).length; for (let k = 0; k < n; k++) jobStepDone(j.id, k);
  out.wrong = { done: !!j.workDone, known: c.known.slice(), crossed: c.crossed.includes(wrongS), back: SHIP.stores[wp] === shelf0, steps: (j.stepsDone || []).length, cond: SHIP.machines[m.id].cond };
  // the save mid-case: written by the save hook, read back by the cleaner
  const sv = { ship: {} }; for (const f of SAVE_EXTRA) { try { f(sv); } catch (e) {} }
  const canon = o => JSON.stringify(o, Object.keys(o).sort().concat(['id', 'type', 'src', 'at', 'kills', 'by', 't', 'tried', 'done']));   // key order doesn't matter
  const before = canon(c); CASE_SAVED = JSON.parse(JSON.stringify(sv.ship.works.cases)); delete SHIP.works.cases; CASE_CLEAN = false;
  const c2 = caseOf(j); out.saveSame = !!c2 && canon(c2) === before; if (!out.saveSame) out.saveDiff = [before, c2 && canon(c2)]; out.saveBytes = JSON.stringify(sv.ship.works.cases).length;
  // the right call: the machine put right, right first time is lost (one wrong call), flags 0
  caseAct('case:call', c2.id + '|' + c2.cause); caseAct('case:yes', c2.id + '|' + c2.cause);
  for (let k = 0; k < n; k++) jobStepDone(j.id, k);
  out.right = { done: !!j.workDone, cond: SHIP.machines[m.id].cond };
  turnInJob(j.id); caseTick(); out.closed = !caseOf(j) && caseState().done.some(x => x[0] === c.id); out.flags = caseFlags(j.id);
  // right first time, and the long way, on fresh copies
  let nf = 0; const fresh = cause => { const k = { ...j, id: m.id + '@pc' + cause + (++nf), cause, parts: [cause], status: 'open', claimedBy: null, stepsDone: [], workDone: undefined, case: undefined, title: undefined };
    SHIP.machines[m.id].cond = 30; SHIP.machines[m.id].state = machineState(30); SHIP.jobs.push(k); CASE_RATE.junior = 1; caseOffer(k, h); CASE_RATE.junior = rate; return k; };
  const k1 = fresh('pump'), c3 = caseOf(k1); claimJob(k1.id); caseTick();
  for (const k of c3.clues) caseClue(c3.id, k.id);
  caseCall(c3.id, c3.sus.find(x => x !== 'pump')); caseCall(c3.id, 'pump'); out.recall = c3.calls.slice();   // a second thought before fitting replaces the call
  for (let k = 0; k < jobStops(k1).length; k++) jobStepDone(k1.id, k); turnInJob(k1.id); caseTick(); out.first = caseFlags(k1.id); out.firstJob = [k1.rightFirst, k1.clever];
  const k2 = fresh('pump'), c4 = caseOf(k2); claimJob(k2.id); caseTick(); caseLong(c4.id); let rounds = 0;
  while (!k2.workDone && rounds++ < 8) { const ns = jobStops(k2).length; for (let k = 0; k < ns; k++) jobStepDone(k2.id, k); }
  out.long = { done: !!k2.workDone, rounds, calls: c4.calls.slice(), causeAt: c4.sus.indexOf(c4.cause) };
  // the T2 band: on a Tier 2 job a wrong call's consumable (the seal) is used up; its other parts still go back
  turnInJob(k2.id); caseTick();
  const k3 = fresh('pump'), c5 = caseOf(k3); k3.tier = 2; claimJob(k3.id); caseTick(); out.spent = {};
  for (const s of c5.sus.filter(x => x !== 'pump')) { const p = caseSus(c5, s).part, s0 = SHIP.stores[p]; caseCall(c5.id, s); SHIP.stores[p]--;
    const ns = jobStops(k3).length; for (let k = 0; k < ns; k++) jobStepDone(k3.id, k); out.spent[p] = [CASE_SPENT.has(p), SHIP.stores[p] === s0 - 1, !k3.workDone]; }
  // a junk save, and a save whose job is gone
  CASE_SAVED = { open: [{ id: 'cx', job: 'nope', kind: 'zz', cause: 'pump', sus: ['pump'], clues: [] }, 'junk'], done: 'x', n: -3 }; delete SHIP.works.cases; CASE_CLEAN = false;
  const cj = caseState(); out.junk = cj.open.length === 0 && cj.done.length === 0 && cj.n === 0;
  out.chief = (() => { caseAct('case:chief', 1); (typeof worksTabAdd === 'function' ? (deviceShow('works'), deviceDo({ app: 'works', do: 'tab', arg: 'faults' }), deviceShow('works')) : deviceShow('faultnotes')); const t = document.getElementById('devBody').textContent; caseAct('case:chief', 0); return t.includes('isn\'t that'); })();
  // a page that isn't a case kind (24i's tracing) shows once its own open() says so (0.55.14)
  CHIEF_NOTES.zzline = { title: 'Line test', lines: ['Follow the line, a panel at a time.'], open: () => window.__lineOpen };
  const chiefText = () => { caseAct('case:chief', 1); (typeof worksTabAdd === 'function' ? (deviceShow('works'), deviceDo({ app: 'works', do: 'tab', arg: 'faults' }), deviceShow('works')) : deviceShow('faultnotes')); const t = document.getElementById('devBody').textContent; caseAct('case:chief', 0); return t; };
  window.__lineOpen = false; const l0 = chiefText().includes('Follow the line'); window.__lineOpen = true; out.otherPage = [l0, chiefText().includes('Follow the line')]; delete CHIEF_NOTES.zzline;
  // a kind opens with its ladder row (SHIP.works.op), not when it's trained
  CASE_KINDS.zop = { ladder: 'zop', fits: () => false }; const op0 = SHIP.works.op, tr0 = SHIP.works.tr;
  SHIP.works.op = {}; SHIP.works.tr = { zop: 5 }; const a1 = caseOpened('zop'); SHIP.works.op = { 5: ['zop'] }; SHIP.works.tr = {}; out.opens = [a1, caseOpened('zop')];
  SHIP.works.op = op0; SHIP.works.tr = tr0; delete CASE_KINDS.zop;
  deviceClose(); JOBS_ON = true; window.__ptOpen = false;
  out.errors = DEV.errors.slice();
  return out;
})()"""

# the Tier 2 water tables (fault-tables.html) while section 17 has none yet: added for P1's and P2's parts, then taken out
T2_TABLES = r"""(() => {
  const added = [];
  const T = {
    recycler: [{ id: 'membrane', part: 'membrane', w: 3, shows: 'low output', sign: 'the output gauge low all day', when: 'always', line: 'water', band: 2 },
      { id: 'pump', part: 'pump', w: 2, shows: 'low output', sign: 'fine in the morning; the gauge sinks after 18:00', when: 'peak', line: 'water', band: 2 },
      { id: 'valve', part: 'valve', w: 1, shows: 'low output', sign: 'the outlet pipe shudders', when: 'always', line: 'water', band: 2 },
      { id: 'seal', part: 'seal', w: 1, shows: 'a drip', sign: 'a wet ring on the floor under it', when: 'after-use', band: 2 }],
    filter: [{ id: 'cartridge', part: 'cartridge', w: 3, shows: 'low flow', sign: 'one housing\'s gauge in the red, all day', when: 'always', line: 'water', band: 2 },
      { id: 'seal', part: 'seal', w: 2, shows: 'low flow', sign: 'a damp floor under one housing', when: 'after-use', line: 'water', band: 2 },
      { id: 'valve', part: 'valve', w: 1, shows: 'cloudy water', sign: 'clear first thing, cloudy by the busy hours', when: 'peak', band: 2 }],
    pump: [{ id: 'pump', part: 'pump', w: 3, shows: 'low flow', sign: 'fine in the morning; labours after 18:00', when: 'peak', line: 'water', band: 2 },
      { id: 'seal', part: 'seal', w: 2, shows: 'low flow', sign: 'a drip under the shaft, low all day', when: 'always', line: 'water', band: 2 },
      { id: 'bearing', part: 'bearing', w: 1, shows: 'noisy', sign: 'a grinding, worse after a long run', when: 'warm', band: 2 }],
    valve: [{ id: 'valve', part: 'valve', w: 3, shows: 'low flow on its branch', sign: 'its branch\'s decks weak; the handle\'s stiff', when: 'always', line: 'water', band: 2 },
      { id: 'seal', part: 'seal', w: 2, shows: 'a drip', sign: 'a drip from the gland', when: 'always', band: 2 }],
    scrubber: [{ id: 'filter', part: 'filter', w: 3, shows: 'stuffy air|rattles', sign: 'a grey grille; the intake buzzes all day', when: 'always', band: 2 },
      { id: 'bearing', part: 'bearing', w: 2, shows: 'rattles', sign: 'a whine that builds through the evening', when: 'warm', band: 2 },
      { id: 'panel', part: 'seal', w: 1, shows: 'rattles', sign: 'the housing buzzes when the door goes', when: 'touched', band: 2 }] };
  for (const k in T) if (!FAULT_CAUSES[k]) { FAULT_CAUSES[k] = T[k]; added.push(k); }
  window.__t2added = added; return added;
})()"""
T2_UNDO = "(() => { for (const k of window.__t2added || []) delete FAULT_CAUSES[k]; window.__t2added = []; })()"

# P1: real days with the crew idle (the machines wear, nothing's repaired), an Officer, the p1 row open; at 10:00 on
# each shift day, every line cause that P1 fits on each line machine becomes a case if it can (the open list emptied
# each time); every log checked against the recorded hours (MACH_HIST); then a day with a decoy machine running badly
P1 = r"""(() => {
  const out = { cases: [], bad: [], lines: {} }, C = caseState(), W = SHIP.works, keep = { jobs: SHIP.jobs, op: W.op, rank: W.rank, tier: W.tier, tr: W.tr };
  const jr = jobRun; jobRun = () => null;
  W.rank = 'officer'; W.tier = 2; W.op = { 12: ['p1'] }; W.tr = {}; C.p1 = 'none'; C.open = []; out.skipped = 0;
  const line = id => (FAULT_CAUSES[(machineById(id) || {}).kind] || []).filter(f => f.part && f.line && P1_WHENS.has(f.when));
  const ms = machineList().filter(m => line(m.id).length && caseLine(m.id, line(m.id)[0].line));
  out.lines = Object.fromEntries(ms.map(m => [m.id, line(m.id).map(f => f.id)]));
  MACH_HOUR = null; MACH_SEEN = -1; setShipNow(9 * 1440); machinesNow();
  for (let d = 11; d <= 30; d++) {
    for (const id of (typeof lineIds === 'function' ? ['water', 'heat', 'air'].flatMap(lineIds) : Object.values(P1_LINES).flat())) if (SHIP.machines[id]) { SHIP.machines[id].cond = Math.max(SHIP.machines[id].cond, 80); SHIP.machines[id].state = machineState(SHIP.machines[id].cond); }   // kept running well (a slow crew)
    if (d === 20 && SHIP.machines['3-filter-1']) { SHIP.machines['3-filter-1'].cond = 30; SHIP.machines['3-filter-1'].state = 'faulty'; }   // Day 20: the filter bank runs badly all day
    for (let h = 0; h < 24; h++) { setShipNow((d - 1) * 1440 + h * 60); machinesNow(); }
    if (d === 20 && SHIP.machines['3-filter-1']) SHIP.machines['3-filter-1'].cond = 90;
    const t = d * 1440 + 600; if (!playerShiftOn(d + 1)) continue;
    setShipNow(t); machinesNow();
    for (const m of ms) for (const f of line(m.id)) {
      C.open = []; SHIP.jobs = SHIP.jobs.filter(x => !x.case);
      const j = { id: m.id + '@p1' + (d + 1) + f.id, machine: m.id, deck: m.deck, kind: 'repair', urgency: 1, posted: t, found: t, claimedBy: null, parts: [f.part], status: 'open', cause: f.id };
      SHIP.jobs.push(j); const rate = CASE_RATE.officer; CASE_RATE.officer = 1; caseOffer(j, d * 24 + 10); CASE_RATE.officer = rate;
      const fine = (caseLine(m.id, f.line) || []).filter(id => id !== m.id && caseLogFine(caseLog(id, d)) && (FAULT_CAUSES[machineById(id).kind] || []).some(g => g.part && g.line === f.line)).length;
      const c = caseOf(j); if (!c) { if (fine >= 3) out.bad.push('no case: ' + j.id + ' with ' + fine + ' fine machines on the line'); else out.skipped++; continue; }   // a line machine running badly can't be a decoy
      const logOk = c.clues.every(k => { for (let hh = 0; hh < 24; hh++) { const r = MACH_HIST.get((k.src.d - 1) * 24 + hh); if (!r || r[k.src.m] == null) return false; if (+k.src.log[hh] !== Math.min(9, Math.floor(machWorks(r[k.src.m]) / 10))) return false; } return k.src.d === d; });
      const sameWhen = c.sus.filter(s => s !== c.cause).some(s => { const at = caseSusAt(s), g = caseCauses(machineById(at)).find(x => x.id === s.slice(at.length + 1)); return g && g.when === f.when; });
      const sameAvail = ms.some(x => x.id !== m.id && (FAULT_CAUSES[x.kind] || []).some(g => g.part && g.line === f.line && g.when === f.when && caseLogFine(caseLog(x.id, d))));
      out.cases.push({ id: c.id, day: d + 1, kind: c.kind, band: c.band, lim: caseBandOf(c.kind, c.band), cause: c.cause, sus: c.sus.slice(), fewest: c.fewest, title: j.title, card: caseCard(j), at: caseAt(j), machine: m.id,
        sameWhen, sameAvail, logOk, filter: c.sus.some(s => s.startsWith('3-filter-1:')), parts: j.parts.slice(),
        clues: c.clues.map(k => ({ id: k.id, at: k.at, kills: k.kills.slice(), m: k.src.m, log: k.src.log, deck: caseClueDeck(k), reach: caseReachable(k), place: !!placeById(k.at), panel: panelPlace(k.src.m) === k.at, text: caseClueText(c, k) })),
        scan: (W.tools = { scanner: [5, 0] }, scanRead(j.id)) });
      SHIP.jobs = SHIP.jobs.filter(x => x !== j);
    }
  }
  C.open = []; jobRun = jr; SHIP.jobs = keep.jobs; Object.assign(W, { op: keep.op, rank: keep.rank, tier: keep.tier, tr: keep.tr }); delete C.p1;
  return out;
})()"""

# P1's first case: 16:00 on Day 11 with the test passed, 3-pump-1 reserved; shown once the p1 row opens (Day 12); the
# card and the arrow don't name the pump; three logs; a wrong call (the filter bank's cartridge, spent), the right one
P1FIRST = r"""(() => {
  const out = {}, C = caseState(), W = SHIP.works, keep = { op: W.op, rank: W.rank, tier: W.tier, tr: W.tr, test: W.test };
  C.open = []; delete C.p1; W.op = {}; W.tr = {}; W.rank = 'junior'; W.tier = 1; W.test = { tier: 2, day: 9, tries: 1, passed: true };
  MACH_HOUR = null; MACH_SEEN = -1; setShipNow(9 * 1440); machinesNow();
  for (const id of (typeof lineIds === 'function' ? ['water', 'heat', 'air'].flatMap(lineIds) : Object.values(P1_LINES).flat())) if (SHIP.machines[id]) { SHIP.machines[id].cond = 90; SHIP.machines[id].state = 'healthy'; }
  for (let t = 9 * 1440; t <= 10 * 1440 + 900; t += 60) { setShipNow(t); machinesNow(); caseTick(); }
  out.before = !!C.p1;
  W.rank = 'officer'; W.tier = 2;
  if (caseTracing()) W.tr = { m9: 11 };                 // a build with M3's tracing: the lesson's done (P1's first waits for it; P1M9 checks the wait)
  setShipNow(10 * 1440 + 961); machinesNow(); caseTick();
  const c = caseById(C.p1), j = c && caseJob(c); out.staged = !!c; out.p1 = C.p1; if (!c) return out;
  out.machine = j.machine; out.cause = c.cause; out.sus = c.sus.slice().sort(); out.train = c.train; out.reserved = j.reserved; out.hidden = caseHidden(j); out.wait = c.wait;
  out.logs = c.clues.map(k => [k.src.m, k.src.log, k.kills.slice(), k.at]);
  setShipNow(11 * 1440 + 540); machinesNow(); caseTick(); out.waitingNoRow = c.wait; out.rowSelf = caseOpened('p1');   // with the lesson done the ladder may open the row itself
  W.op = { 12: ['m9', 'p1'] }; setShipNow(11 * 1440 + 560); machinesNow(); caseTick();
  out.shown = !c.wait; out.title = j.title; out.by = c.by; out.card = caseCard(j); out.cardBoard = jobCard(j); out.parts = j.parts.slice();
  out.at0 = caseAt(j); out.stop0 = (jobStops(j).slice(-1)[0] || {}).places;
  out.scan = (W.tools = { scanner: [5, 0] }, scanRead(j.id));
  claimJob(j.id); caseTick();
  for (const k of c.clues) caseClue(c.id, k.id);
  out.texts = c.clues.map(k => caseClueText(c, k));
  (typeof worksTabAdd === 'function' ? (deviceShow('works'), deviceDo({ app: 'works', do: 'tab', arg: 'faults' }), deviceShow('works')) : deviceShow('faultnotes'));
  const b = document.getElementById('devBody'), rows = [...b.querySelectorAll('.strip .st-row')];
  out.strip = rows.map(r => ({ bars: r.querySelectorAll('.st-h').length, pins: r.querySelectorAll('.st-h.pin').length, low: r.querySelectorAll('.st-h.low').length, w: Math.round(r.querySelector('.st-h').getBoundingClientRect().width) }));
  out.chips = [...b.querySelectorAll('.chips .chip')].map(x => x.textContent);
  const has = DEVICE_SKIN.has; DEVICE_SKIN.has = k => k !== 'strip' && has(k); DEV.app = 'home'; (typeof worksTabAdd === 'function' ? deviceShow('works') : deviceShow('faultnotes'));
  out.stripFallback = b.querySelectorAll('.strip').length === 0 && b.textContent.includes('log: full output every hour'); DEVICE_SKIN.has = has; deviceClose();
  // a wrong call: the filter bank's cartridge (Tier 2: spent); the arrow goes to the filter bank
  const wrong = c.sus.find(s => s.startsWith('3-filter-1:')) || c.sus.find(s => s !== c.cause), wp = caseSus(c, wrong).part;
  caseCall(c.id, wrong); out.atWrong = caseAt(j); out.stopWrong = (jobStops(j).slice(-1)[0] || {}).places;
  const s0 = SHIP.stores[wp]; SHIP.stores[wp]--;
  let n = jobStops(j).length; for (let k = 0; k < n; k++) jobStepDone(j.id, k);
  out.wrongFit = { done: !!j.workDone, spent: SHIP.stores[wp] === s0 - 1, part: wp, known: c.known.includes(wrong) };
  // the save mid-case
  const sv = { ship: {} }; for (const f of SAVE_EXTRA) { try { f(sv); } catch (e) {} }
  const canon = o => JSON.stringify(o, Object.keys(o).sort().concat(['id', 'type', 'src', 'at', 'kills', 'm', 'log', 'd']));
  const before = canon(c); CASE_SAVED = JSON.parse(JSON.stringify(sv.ship.works.cases)); delete SHIP.works.cases; CASE_CLEAN = false;
  const c2 = caseOf(j); out.saveSame = !!c2 && canon(c2) === before; out.saveBytes = JSON.stringify(c2).length; out.savedP1 = caseState().p1 === c.id;
  // the right call: the pump; fixed
  caseCall(c2.id, c2.cause); out.atRight = caseAt(j);
  n = jobStops(j).length; for (let k = 0; k < n; k++) jobStepDone(j.id, k);
  out.fixed = !!j.workDone && SHIP.machines[j.machine].cond > 40; out.flags = [j.rightFirst, j.clever];
  turnInJob(j.id); caseTick(); out.closed = !caseById(c.id); out.done = caseFlags(j.id);
  Object.assign(W, keep); C.open = []; delete C.p1;
  return out;
})()"""

# P2: an Officer after Tomas's word (said set), the p2 row open; at 10:00 on each shift day, every cause P2 fits on
# every machine becomes a case if it can; each witness checked against the plans (planWhere) at their minute
P2 = r"""(() => {
  const out = { cases: [], bad: [], fit: 0 }, C = caseState(), W = SHIP.works, keep = { op: W.op, rank: W.rank, tier: W.tier, tr: W.tr, said: W.said };
  const jr = jobRun; jobRun = () => null;
  W.rank = 'officer'; W.tier = 2; W.op = { 15: ['p2'] }; W.tr = {}; W.said = { p2: 15 }; C.p2 = 'none'; C.p1 = 'none'; C.open = [];
  MACH_HOUR = null; MACH_SEEN = -1; setShipNow(14 * 1440); machinesNow();
  for (let d = 15; d <= 34; d++) {
    if (!playerShiftOn(d)) continue;
    const t = (d - 1) * 1440 + 600; setShipNow(t); machinesNow();
    for (const m of machineList()) for (const f of caseCauses(m)) {
      if (!CASE_KINDS.p2.fits(f, m) || (m.tier || MACHINE_KINDS[m.kind].tier) > 2 || !panelPlace(m.id)) continue;
      out.fit++; C.open = []; SHIP.jobs = SHIP.jobs.filter(x => !x.case);
      const j = { id: m.id + '@p2' + d + f.id, machine: m.id, deck: m.deck, kind: 'repair', urgency: 1, posted: t, found: t, claimedBy: null, parts: [f.part], status: 'open', cause: f.id };
      SHIP.jobs.push(j);
      const keepK = {}; for (const k in CASE_KINDS) if (k !== 'p2') { keepK[k] = CASE_KINDS[k]; delete CASE_KINDS[k]; }   // P2 alone
      const rate = CASE_RATE.officer; CASE_RATE.officer = 1; caseOffer(j, (d - 1) * 24 + 10); CASE_RATE.officer = rate; Object.assign(CASE_KINDS, keepK);
      const c = caseOf(j); if (!c) continue;
      const F = id => caseCauses(m).find(x => x.id === id), show = p2ShowAt(t);
      const ws = c.clues.map(k => { const p = schedPeople().find(x => x.id === k.src.ask), w = p && planWhere(p, k.src.t), pl = placeById(k.src.pl);
        return { id: k.id, who: k.src.ask, t: k.src.t, kills: k.kills.slice(), mix: k.src.mix || null, saw: k.src.saw, there: !!w && w.placeId === k.src.pl && w.act !== 'commute', inWindow: k.src.t >= t && k.src.t < show,
          near: !!pl && pl.deck === m.deck && caseRoomsNear(m.deck, m.room).has(pl.room), trap: k.src.mix ? !caseShows(m, F(c.cause), k.src.t) : null, other: k.src.mix ? machineById(k.src.mix).deck !== m.deck : null,
          deck: caseClueDeck(k), reach: caseReachable(k), place: true, line: p2Line(c, k) }; });
      out.cases.push({ id: c.id, kind: c.kind, band: c.band, lim: caseBandOf(c.kind, c.band), cause: c.cause, sus: c.sus.slice(), fewest: c.fewest, wait: c.wait, hidden: caseHidden(j), clues: ws,
        whens: c.sus.map(s => F(s).when) });
      setShipNow(show - 30); caseTick(); const early = !c.wait; setShipNow(show); caseTick(); out.cases[out.cases.length - 1].shown = !early && !c.wait && j.title.startsWith('Head-scratcher: ') && / now and then$/.test(j.title);
      out.cases[out.cases.length - 1].title = j.title;
      setShipNow(t); SHIP.jobs = SHIP.jobs.filter(x => x !== j);
    }
  }
  C.open = []; jobRun = jr; Object.assign(W, keep); delete C.p2; delete C.p1;
  return out;
})()"""

# P2's gate and first case: staged 16:00 Day 14; at Day 15 05:59, at the row's opening and up to Tomas's word: no case
# showing, no Ask button, no witness line, and no roll P2 case; the word (at a meal you share) opens it and shows the
# first case with its witnesses; asking a witness gives their line (the same twice) and the clue; the save keeps it
P2GATE = r"""(() => {
  const out = {}, C = caseState(), W = SHIP.works, keep = { op: W.op, rank: W.rank, tier: W.tier, tr: W.tr, said: W.said };
  C.open = []; delete C.p2; delete C.said; C.p1 = 'none'; W.said = {}; W.op = {}; W.tr = {}; W.rank = 'officer'; W.tier = 2;
  MACH_HOUR = null; MACH_SEEN = -1; setShipNow(13 * 1440); machinesNow();
  setShipNow(13 * 1440 + 961); machinesNow(); caseTick();
  const c = caseById(C.p2), j = c && caseJob(c); out.staged = !!c; if (!c) return out;
  out.machine = j.machine; out.cause = c.cause; out.sus = c.sus.slice().sort(); out.reserved = j.reserved; out.hidden = caseHidden(j);
  const crew = schedPeople(), asks = () => crew.filter(p => caseAskButton(p)).length, says = () => crew.filter(p => caseAskSay(p)).length;
  setShipNow(14 * 1440 + 359); machinesNow(); caseTick(); out.at559 = [p2Said(), caseOpened('p2'), asks(), says(), c.wait];
  W.op = { 15: ['p2'] }; setShipNow(14 * 1440 + 361); machinesNow(); caseTick(); out.rowOpen = [p2Row(), caseOpened('p2'), asks(), says(), c.wait];
  // a roll before the word: no P2 case, whatever fits
  const m2 = machineList().find(x => x.id !== j.machine && x.kind === 'scrubber'), f2 = m2 && caseCauses(m2).find(x => x.id === 'bearing');
  if (f2) { const k = { id: m2.id + '@gate', machine: m2.id, deck: m2.deck, kind: 'repair', urgency: 1, posted: 14 * 1440 + 600, found: 14 * 1440 + 600, claimedBy: null, parts: [f2.part], status: 'open', cause: 'bearing' };
    SHIP.jobs.push(k); const r = CASE_RATE.officer; CASE_RATE.officer = 1; setShipNow(14 * 1440 + 600); caseOffer(k, 14 * 24 + 10); CASE_RATE.officer = r; out.rollBefore = !!caseOf(k) && caseOf(k).kind; SHIP.jobs = SHIP.jobs.filter(x => x !== k); C.open = C.open.filter(x => x.job !== k.id); }
  // Tomas's word at breakfast: you in the room where he eats
  const tomas = crew.find(p => p.id === 'tomas'), segs = tomas ? planDay(tomas, 15).filter(s => P2_MEALS.has(s.act) && s.placeId) : [], meal = segs[0];
  out.meal = meal ? [meal.act, hhmm(meal.from % 1440), meal.deck, placeById(meal.placeId).room] : null;
  if (meal) {
    const tm = Math.floor((meal.from + meal.to) / 2); setShipNow(tm - 30); caseTick(); out.beforeWord = [p2Said(), asks(), c.wait];
    const pl = placeById(meal.placeId); if (deckDef.num !== pl.deck && typeof goToDeck === 'function') goToDeck(pl.deck);
    const sp = placeSpot(meal.placeId); player.obj.position.x = sp.x; player.obj.position.z = sp.z; out.here = [deckDef.num, roomAt(...player.here()), pl.room];
    setShipNow(tm); caseTick(); out.word = [p2Said(), W.said && W.said.p2, C.said && C.said.p2];
  }
  if (p2Said() == null) p2Said1(C, 'tomas', 14 * 1440 + 450);   // (if the geometry couldn't be set up here)
  out.shown = !c.wait; out.title = j.title; out.by = c.by; out.n = c.clues.length;
  out.ws = c.clues.map(k => { const p = crew.find(x => x.id === k.src.ask), w = p && planWhere(p, k.src.t); return { who: k.src.ask, t: hhmm(k.src.t % 1440), kills: k.kills, mix: k.src.mix || null, saw: k.src.saw, door: k.src.door, there: !!w && w.placeId === k.src.pl, room: (placeById(k.src.pl) || {}).room, deck: (placeById(k.src.pl) || {}).deck }; });
  out.asks = asks(); out.nonWitness = crew.filter(p => !c.clues.some(k => k.src.ask === p.id)).every(p => !caseAskButton(p));
  const w0 = c.clues[0], p0 = w0 && crew.find(x => x.id === w0.src.ask);
  if (p0) { out.line1 = caseAskSay(p0); out.line2 = caseAskSay(p0); out.got = c.got.slice(); }
  // the save: the word and the case come back
  const sv = { ship: {} }; for (const f of SAVE_EXTRA) { try { f(sv); } catch (e) {} }
  CASE_SAVED = JSON.parse(JSON.stringify(sv.ship.works.cases)); delete SHIP.works.cases; delete W.said; CASE_CLEAN = false;
  out.saved = [p2Said(), !!caseById(c.id), (caseById(c.id) || {}).clues && caseById(c.id).clues.length, JSON.stringify(sv.ship.works.cases).length];
  // the right call: the bearing; fixed
  claimJob(j.id); caseTick(); caseCall(c.id, c.cause); const n = jobStops(j).length; for (let k = 0; k < n; k++) jobStepDone(j.id, k);
  out.fixed = !!j.workDone; turnInJob(j.id); caseTick(); out.done = caseFlags(j.id); out.closed = !caseById(c.id);
  Object.assign(W, keep); C.open = []; delete C.p2; delete C.said; delete C.p1;
  return out;
})()"""

# P1's first with an m9 row (M3's tracing lesson reads this line on Day 12): nothing at 16:00 on Day 11; staged once
# m9 is trained, the pump's fault from then
P1M9 = r"""(() => {
  const out = {}, C = caseState(), W = SHIP.works, keep = { op: W.op, rank: W.rank, tier: W.tier, tr: W.tr, test: W.test }, had = !!WORK_MECH.m9;
  if (!had) WORK_MECH.m9 = { open() {} };              // as if M3's tracing (24i) were in
  C.open = []; delete C.p1; W.op = {}; W.tr = {}; W.rank = 'officer'; W.tier = 2; W.test = { tier: 2, day: 9, tries: 1, passed: true };
  MACH_HOUR = null; MACH_SEEN = -1; setShipNow(9 * 1440); machinesNow();
  for (let t = 9 * 1440; t <= 10 * 1440 + 1000; t += 60) { setShipNow(t); machinesNow(); caseTick(); }
  out.day11 = C.p1 || null;
  for (const id of (typeof lineIds === 'function' ? ['water', 'heat', 'air'].flatMap(lineIds) : Object.values(P1_LINES).flat())) if (SHIP.machines[id]) { SHIP.machines[id].cond = 90; SHIP.machines[id].state = 'healthy'; }
  for (let t = 10 * 1440 + 1020; t <= 11 * 1440 + 600; t += 60) { setShipNow(t); machinesNow(); }
  const now = 11 * 1440 + 650; W.tr = { m9: 12 }; setShipNow(now); machinesNow(); caseTick();
  const c = C.p1 && caseById(C.p1), j = c && caseJob(c); out.staged = !!c; out.now = now; out.p1 = C.p1;
  if (j) { out.due = j.posted; out.logDay = c.clues[0] && c.clues[0].src.d; SHIP.jobs = SHIP.jobs.filter(x => x !== j); }
  if (!had) delete WORK_MECH.m9;
  Object.assign(W, keep); C.open = []; delete C.p1;
  return out;
})()"""

def run(path):
    with sync_playwright() as pw:
        g = Game(pw, path, 390, 844)
        g.step(3)
        r = g.ev(CHIPS)
        print('chips:', r)
        check(r['n'] == 3 and r['labels'] == ['Door seal', 'Drain valve', 'Pump'], f'a chip per item: {r["labels"]}')
        check(r['pressed'] == ['false', 'true', 'true'] and r['off'] == [True, False, False], f'crossed out only while on is false: {r["pressed"]} {r["off"]}')
        check('line-through' in r['strike'][0] and 'line-through' not in r['strike'][1], f'a crossed chip is struck through: {r["strike"]}')
        check(min(r['h']) >= 44 and min(r['w']) >= 44, f'chips are big toggles (44px+): {r["h"]} {r["w"]}')
        check(r['tap'] == ['tap:seal'], f'a tap runs the chip\'s action: {r["tap"]}')
        check(r['fb'] == ['✕ Door seal', 'Drain valve', 'Pump'] and r['fbChips'] == 0, f'no chips in the skin: buttons with "✕ ": {r["fb"]}')
        check(r['fbTap'] == ['tap:valve'], f'the fallback buttons run the same actions: {r["fbTap"]}')
        errs = g.ev("DEV.errors.slice()")
        # the case engine
        st = g.ev(SETUP)
        print('stand-ins:', {k: v for k, v in st.items()})
        g.ev("window.__noKind = JSON.stringify([SHIP.jobs.length])")
        A = g.ev(PAPER); B = g.ev(PAPER)
        cs = A['cases']
        print(f"cases: {len(cs)}; per rank: {A['perRank']}; stats: {A['stats']}")
        for c in cs[:4]: print('  ', c['id'], 'day', c['day'], c['hour'], c['band'], c['cause'], c['sus'], [(k['at'], k['kills']) for k in c['clues']], c['title'])
        if st['hookOffer']: check(len(cs) >= 1, f'cases were posted over Days 5-26 on paper: {len(cs)}')
        else: print(f'  (section 17 has no real faults yet: {len(cs)} cases on paper; the sweep below makes them)')
        Sw = g.ev(SWEEP); Sw2 = g.ev(SWEEP)
        print(f"sweep: {len(Sw['cases'])} cases; per rank: {Sw['perRank']}")
        check(len(Sw['cases']) >= 20, f"the sweep made cases: {len(Sw['cases'])}")
        BAND = {'T1': ([3, 4], [2, 3], 2, 1), 'T2': ([3, 5], [3, 4], 3, 2), 'T3': ([5, 6], [4, 6], 3, 3), 'T4': ([5, 6], [4, 6], 3, 3)}
        from itertools import combinations
        def lim(c):                                       # the band's limits for the case's kind (its page's), else the engine's
            L = c.get('lim'); return (L['sus'], L['clues'], L['fewest'], L['decks']) if L else BAND[c['band']]
        for c in cs + Sw['cases']:
            sus, clues, (sn, cn, few, decks) = c['sus'], c['clues'], lim(c)
            left = lambda ks: [s for s in sus if not any(s in k['kills'] for k in ks)]
            check(left(clues) == [c['cause']], f"{c['id']}: every clue leaves exactly the cause: {left(clues)} vs {c['cause']}")
            check(all(len(left([k])) > 1 for k in clues), f"{c['id']}: no single clue solves it")
            fewest = min((n for n in range(1, len(clues) + 1) for ks in combinations(clues, n) if len(left(list(ks))) == 1), default=99)
            check(fewest == c['fewest'] and fewest >= few, f"{c['id']}: the fewest clues {fewest} (engine {c['fewest']}) within the band ({few}+)")
            check(sn[0] <= len(sus) <= sn[1] and cn[0] <= len(clues) <= cn[1], f"{c['id']}: the band's counts: {len(sus)} suspects, {len(clues)} clues")
            check(len({k['deck'] for k in clues if k['deck'] is not None}) <= decks, f"{c['id']}: within the band's decks")
            check(all(k['reach'] and k['place'] for k in clues), f"{c['id']}: every clue reachable: {clues}")
            if 'wd' not in c: continue
            check(c['wd'] < 5 and 6 <= c['hour'] < 15 and c['day'] >= 5, f"{c['id']}: on a shift day, 06:00-15:00, from Day 5: day {c['day']} weekday {c['wd']} {c['hour']}:00")
            check(c['parts'] == [] and c['title'].startswith('Head-scratcher: '), f"{c['id']}: the part is yours to find and the card says Head-scratcher: {c['parts']} {c['title']!r}")
        check(not A['over'], f'never more open than the limit: {A["over"][:4]}')
        RATE = {'junior': .1, 'officer': .2, 'senior': .25, 'specialist': .33}
        for rk, r in Sw['perRank'].items():
            if r['offered'] >= 20:
                share = r['rolled'] / r['offered']
                check(RATE[rk] * .5 <= share <= RATE[rk] * 1.5, f"{rk}: the roll's share {share:.2f} within +-50% of {RATE[rk]} ({r['rolled']}/{r['offered']})")
            else: print(f"  ({rk}: only {r['offered']} offers, rate not checked)")
        # the roll itself (key 880): over every machine and 300 days, the share under each rank's rate
        roll = g.ev("(() => { const ms = machineList(), out = {}; for (const rk in CASE_RATE) { let n = 0, k = 0; for (const m of ms) for (let d = 1; d <= 300; d++) { n++; if (schedU(machSeed(m.id), d, 880) < caseRate(rk, 1)) k++; } out[rk] = k / n; } return out; })()")
        print('the roll:', {k: round(v, 3) for k, v in roll.items()})
        check(all(abs(roll[k] - RATE[k]) <= RATE[k] * .15 for k in RATE), f'the rate roll gives each rank its share: {roll}')
        st_ = A['stats']
        if st_['rolled'] and st_['fallback'] / st_['rolled'] > .1: print(f"WARN fallbacks {st_['fallback']}/{st_['rolled']}: {st_['why']}")
        # makeCase's cost: 2000 of them on a washer's leak, timed from here (the test page freezes performance.now and Date.now)
        import time as _t
        g.ev("window.__ptOpen = true; window.__msj = (() => { const m = machineList().find(x => x.kind === 'washer'); return { id: m.id + '@ms', machine: m.id, deck: m.deck, kind: 'repair', urgency: 1, posted: 0, found: 0, parts: [], status: 'open', cause: 'pump' }; })(); SHIP.jobs.push(__msj)")
        t0 = _t.time(); g.ev("for (let i = 0; i < 2000; i++) caseMake(__msj, 'zz', i % 8, 5 + i)"); ms = (_t.time() - t0) * 1000 / 2000
        g.ev("SHIP.jobs = SHIP.jobs.filter(j => j !== __msj); window.__ptOpen = false")
        print(f"makeCase: {ms:.3f} ms each (desktop; budget 5 ms on the phone profile)")
        check(0 < ms < 5, f"makeCase under 5 ms: {ms:.2f}")
        check(json.dumps(A['cases']) == json.dumps(B['cases']) and json.dumps(Sw) == json.dumps(Sw2), 'twice -> the same cases')
        fb = sum(r['fallback'] for r in Sw['perRank'].values()); rl = sum(r['rolled'] for r in Sw['perRank'].values())
        if rl and fb / rl > .1: print(f"WARN sweep fallbacks {fb}/{rl}")
        Sc = g.ev(SCAN)
        print('scanner:', {k: v for k, v in Sc.items() if k != 'bad'}, Sc['bad'][:4])
        check(Sc['none'] is None, 'no scanner, no reading')
        check(Sc['parts'] and all(min(3, Sc['have'][k]) <= n <= 5 for k, n in Sc['parts'].items()), f"every kind with a table reads 3-5 parts (fewer only if its table has fewer): {Sc['parts']} of {Sc['have']}")
        check(not Sc['bad'], f"the failing part is the cause's, the same twice; a worn decoy shares the card, not the sign: {Sc['bad'][:4]}")
        check(Sc['twoLow'] > 0, f"some readings have a worn decoy: {Sc['twoLow']}")
        check(Sc['pickWrong'] and Sc['partsAfterPick'][0] != 'pump', f"a pick puts that part on the job: {Sc['partsAfterPick']}")
        w = Sc['wrong']; check(not w['done'] and w['back'] and w['parts'] == ['pump'] and w['cond'] == 30, f"a wrong pick: not fixed, the part back, the job names the right part: {w}")
        check(Sc['right']['done'] and Sc['right']['cond'] > 30 and Sc['right']['first'] is False, f"then the right one fixes it (not right first time): {Sc['right']}")
        Q = g.ev(P3 + "('junior')"); Q2 = g.ev(P3 + "('officer')")
        qc = Q['cases']; print(f"P3 sweep: {len(qc)} cases"); [print('  ', c) for c in qc[:2]]
        q2 = Q2['cases']; nodd = sum(1 for c in q2 if c['odd']); print(f"P3 sweep as an Officer (T2): {len(q2)} cases, {nodd} with a wrong-size note"); [print('  ', c) for c in [x for x in q2 if x['odd']][:1]]
        check(len(qc) >= 20 and len(q2) >= 20, f"P3 cases: {len(qc)}, as an Officer {len(q2)}")
        check(all(c['band'] == 'T1' for c in qc) and all(c['band'] == 'T2' and c['lim']['fewest'] == 2 for c in q2), "P3's bands: T1 for a Junior, T2 (P3 keeps T1's size) for an Officer")
        check(.25 * len(q2) <= nodd <= .75 * len(q2), f"about half of an Officer's P3 cases have a note that rules out less than it seems: {nodd}/{len(q2)}")
        check(all('wrong size' in c['oddText'].lower() and ' — ' in c['oddText'] for c in q2 if c['odd']), f"the wrong-size note says so: {[c.get('oddText') for c in q2 if c['odd']][:2]}")
        for c in qc + q2:
            lo, hi = c['lim']['clues']
            check(lo <= len(c['clues']) <= hi and c['lim']['sus'][0] <= len(c['sus']) <= c['lim']['sus'][1], f"{c['id']}: within its band: {len(c['sus'])} suspects, {len(c['clues'])} notes")
        for c in qc + q2:
            sus, clues = c['sus'], c['clues']
            left = lambda ks: [s for s in sus if not any(s in k['kills'] for k in ks)]
            check(c['kind'] == 'p3' and c['oneEach'] and left(clues) == [c['cause']] and all(len(left([k])) > 1 for k in clues), f"{c['id']}: one note per decoy, each kills only its decoy, one left: {c}")
            check(all(k['crew'] and 120 <= k['dt'] <= 1440 + 600 for k in clues), f"{c['id']}: tries by Works crew at work, 2-12 hours on or the next morning: {[(k['by'], k['dt'], k['crew']) for k in clues]}")
            check(c['wait'] and c['hidden'] and c['parts'] != [] and not c['early'] and c['shown'], f"{c['id']}: hidden till the last try, then shown inside the shift: {c}")
            check(all(u == 1 for u in c['used']), f"{c['id']}: each try's part came off its shelf: {c['used']}")
            check(sum(1 for k in clues if k['at'] == 'board') == 1, f"{c['id']}: one note on the job, the rest on the machine: {[k['at'] for k in clues]}")
            check(c['scanBlind'], f"{c['id']}: the scanner's readings don't depend on the cause")
            check(' — ' in c['text'] and 'Still' in c['text'], f"{c['id']}: a note names who tried: {c['text']!r}")
        check(Q.get('waitEnds'), f"a case still waiting after three days is let go: {Q.get('waitEnds')}")
        F2 = g.ev(FIRST_M7)
        print('first case through m7:', F2)
        check(F2.get('id') == F2.get('job') and F2.get('m7') and not F2.get('hidden'), f"Day 5: your scanner job is Washer 2 itself, on the board for you: {F2}")
        check(F2.get('shownAtReading') and len(F2.get('got', [])) == 1 and F2.get('calledNote'), f"reading it opens P3's case there, the first note with the job; the call sends caseCalled: {F2}")
        F = g.ev(FIRST)
        print('first case:', F)
        check(not F.get('before') and F.get('staged') and F.get('machine') in ('4-washer-2', '4-washer-3') and F.get('cause') == 'pump' and F.get('sus') == ['pump', 'seal', 'valve'] and F.get('train'), f"Day 4 18:00: Washer 2 leaking, the pump, three suspects, a training case: {F}")
        if F.get('staged'):
            check([n['tried'] for n in F['notes']] == ['seal', 'valve'] and F['notes'][0]['at'] == 'board' and F['notes'][1]['at'] == F['panel'], f"the seal tried first (on the job), then the valve (on the panel): {F['notes']}")
            check(F['waitingNoRow'] and F['faulty'] in ('faulty', 'failing'), f"Friday morning: the washer faulty, the case waiting for the row: {F['waitingNoRow']} {F['faulty']}")
            check(F['shown'] and F['title'].startswith('Head-scratcher: Washer') and F['title'].endswith('leaks'), f"shown once the row opens: {F['title']!r}, with {F['by']}")
            sc = dict(F['scan'] or [])
            check(sc.get('pump') == 55 and sc.get('seal') == 44 and sc.get('valve') == 49, f"Day 5's reading is fixed so the cause isn't lowest: {F['scan']}")
            check(all(40 <= sc.get(p, 0) <= 60 for p in ('pump', 'seal', 'valve')) and all(v > 60 for p, v in sc.items() if p not in ('pump', 'seal', 'valve')), f"the scanner on a head-scratcher: every suspect worn, the rest good: {F['scan']}")
            check(len(F['got']) == 1 and F['goal'] == F['panel'], f"the first note with the job, Where next? to the panel: {F['got']} {F['goal']}")
            check(F['fixed'] and F['flags'] == [True, True] and F['closed'] and F['done'] == 6, f"called right first time, fixed and closed: {F}")
        P = g.ev(PLAY)
        print('play:', {k: v for k, v in P.items() if k not in ('viewText',)})
        check(P.get('made') and P['parts'] == [] and P['held'], f"a case on the washer, its part not given, held for you: {P.get('parts')} {P.get('held')}")
        check(len(P['chips0']) == 3 and not any(x.endswith(':off') for x in P['chips0']), f"Fault notes: three suspects as chips: {P['chips0']}")
        check(P['chips1'][0].endswith(':off') and P['chips2'] == P['chips0'], f"tap to cross out, tap again to bring it back: {P['chips1']} {P['chips2']}")
        check(P['gotBefore'] == 0 and len(P['gotBoard']) == 1, f"the note taped to the job comes when you take it: {P['gotBoard']}")
        check(P['goal'] == P['panel'], f"Where next? points at the panel: {P['goal']} vs {P['panel']}")
        check(len(P['calledParts']) == 1, f"calling it sets the job's part: {P['calledParts']}")
        w = P['wrong']; check(not w['done'] and w['crossed'] and w['back'] and w['steps'] == 0 and w['cond'] == 30, f"a wrong call: not fixed, crossed by the evidence, the part back on its shelf, the stops again: {w}")
        check(P['saveSame'] and P['saveBytes'] < 1200, f"the save mid-case reads back the same ({P['saveBytes']} bytes)")
        check(P['right']['done'] and P['right']['cond'] > 30 and P['closed'] and P['flags'] == 0, f"the right call fixes it; one wrong call, so not right first time: {P['right']} {P['flags']}")
        check(P['recall'] == ['pump'], f"calling again before fitting replaces the call: {P['recall']}")
        check(P['first'] == 6 and P['firstJob'] == [True, True], f"right first time and clever, flagged on the case and the job: {P['first']} {P['firstJob']}")
        check(P['long']['done'] and P['long']['rounds'] == P['long']['causeAt'] + 1 and P['long']['calls'][-1] == 'pump', f"the long way fits each in turn and always ends: {P['long']}")
        check(P['spent'] and all(v[0] == v[1] and v[2] for v in P['spent'].values()) and any(v[0] for v in P['spent'].values()), f"T2: a wrong call's consumable is used up, other parts go back, the job not done: {P['spent']}")
        pos = {}
        for c in Sw['cases']: pos[c['sus'].index(c['cause'])] = pos.get(c['sus'].index(c['cause']), 0) + 1
        check(len(pos) >= 3 and max(pos.values()) < .6 * len(Sw['cases']), f"the cause isn't always in the same place among the suspects: {pos}")
        check(P['junk'], 'a junk save and a gone job: no cases')
        check(P['chief'], "the Chief's notes page")
        check(P['otherPage'] == [False, True], f"a Chief's notes page that isn't a case kind shows once its open() says so: {P['otherPage']}")
        check(P['opens'] == [False, True], f"a kind opens when its ladder row opens, not when trained: {P['opens']}")
        check(not P['errors'], f"no device errors: {P['errors']}")
        # P1 (0.55.14)
        added = g.ev(T2_TABLES); print('Tier 2 stand-in tables:', added or 'none (section 17 has them)')
        R1 = g.ev(P1); R1b = g.ev(P1)
        p1c = R1['cases']; print(f"P1 sweep: {len(p1c)} cases on {R1['lines']}"); [print('  ', {k: v for k, v in c.items() if k != 'clues'}) for c in p1c[:2]]
        if p1c: print('   a log:', p1c[0]['clues'][0]['text'])
        check(len(p1c) >= 10 and not R1['bad'], f"P1 cases on every line cause that fits, unless a machine on the line ran badly ({R1['skipped']} so): {len(p1c)}, {R1['bad'][:3]}")
        if not check(json.dumps(R1) == json.dumps(R1b), 'P1: twice -> the same cases and logs'):
            for x, y in zip(R1['cases'], R1b['cases']):
                if x != y: print('   first diff:', {k: (x[k], y.get(k)) for k in x if x[k] != y.get(k)}); break
            print('   counts', len(R1['cases']), len(R1b['cases']), R1['skipped'], R1b['skipped'])
        for c in p1c:
            sus, clues, (sn, cn, few, decks) = c['sus'], c['clues'], lim(c)
            left = lambda ks: [s for s in sus if not any(s in k['kills'] for k in ks)]
            fewest = min((n for n in range(1, len(clues) + 1) for ks in combinations(clues, n) if len(left(list(ks))) == 1), default=99)
            check(c['kind'] == 'p1' and c['band'] == 'T2' and left(clues) == [c['cause']] and all(len(left([k])) > 1 for k in clues) and fewest == c['fewest'] == 3, f"{c['id']}: one left, no single log solves it, three needed: {left(clues)} {fewest}")
            check(len(sus) == 4 and len(clues) == 3 and all(k['panel'] and k['reach'] and k['place'] for k in clues) and len({k['deck'] for k in clues}) <= decks, f"{c['id']}: 4 suspects, 3 logs at their machines' panels, reachable, {decks} decks at most: {clues}")
            check(c['logOk'], f"{c['id']}: each log is the machine's real hours (MACH_HIST)")
            check(all(len(k['kills']) == 1 and k['kills'][0].startswith(k['m'] + ':') and k['kills'][0] in sus for k in clues) and all(set(k['log']) <= set('89') for k in clues), f"{c['id']}: a decoy's log ran fine every hour and crosses it out: {[(k['m'], k['log']) for k in clues]}")
            check(c['sameWhen'] or not c['sameAvail'], f"{c['id']}: a decoy with the cause's when first, when the line has one (lead 16)")
            check(c['day'] != 21 or not c['filter'], f"{c['id']}: Day 20 the filter bank ran badly: not a decoy then")
            check(c['card'] and c['machine'] not in json.dumps(c['card']) and 'Circulation' not in c['card'][0] and c['title'].startswith('Head-scratcher: ') and ', but only ' in c['title'], f"{c['id']}: the card names the line's symptom, not the machine: {c['card']} {c['title']!r}")
            check(c['at'] and c['at'] != c['machine'], f"{c['id']}: before a call the arrow goes to the top of the line, not the cause's machine: {c['at']}")
            check(c['scan'] is None and c['parts'] == [], f"{c['id']}: the scanner won't settle it, the part is yours to find: {c['scan']} {c['parts']}")
        check(any(c['day'] == 21 for c in p1c) or R1['skipped'], 'P1: Day 21 made cases without the filter bank')
        F1 = g.ev(P1FIRST)
        print('P1 first:', F1)
        check(not F1.get('before') and F1.get('staged') and F1.get('machine') == '3-pump-1' and F1.get('cause') == 'pump' and F1.get('train') and F1.get('reserved') == 21 and F1.get('hidden') and F1.get('wait'), f"P1's first: 3-pump-1 from Day 11 16:00, slot 21, hidden: {F1}")
        if F1.get('staged'):
            check(F1['sus'] == sorted(['pump', '3-recycler-1:membrane', '3-filter-1:cartridge', '5-valve-2:valve']), f"the page's suspects: {F1['sus']}")
            check((F1['waitingNoRow'] or F1['rowSelf']) and F1['shown'] and F1['by'] in ('calder', 'halloran-emeka'), f"shown once the p1 row opens, with {F1.get('by')}")
            check('Showers on Deck 4' in F1['title'] and 'evening' in F1['title'] and 'pump' not in F1['title'].lower(), f"the card: {F1['title']!r}")
            check(F1['cardBoard'] == F1['card'] or not st.get('hookCard', True), f"the board card is the case's (section 17's jobCard hook): {F1['cardBoard']}")
            check(F1['at0'] == '3-recycler-1' and F1['scan'] is None and F1['parts'] == [], f"the arrow to the top of the line, no scanner, no part: {F1['at0']} {F1['scan']}")
            if st.get('hookAt'): check(F1['stop0'] == ['3-recycler-1-panel'] and F1['stopWrong'] == ['3-filter-1-panel'], f"section 17's stops follow: the top of the line, then the called machine: {F1['stop0']} {F1['stopWrong']}")
            check(len(F1['strip']) == 3 and all(r['bars'] == 24 and r['pins'] == 5 and r['w'] >= 12 and r['low'] == 0 for r in F1['strip']), f"the day strip: three logs, 24 bars of 12px+, the evening outlined, all fine: {F1['strip']}")
            check(F1['stripFallback'], 'a skin without strips: the logs as a list')
            check(all('log: full output every hour' in t for t in F1['texts']), f"the logs in words: {F1['texts']}")
            check(F1['atWrong'] == '3-filter-1' and F1['wrongFit']['spent'] and not F1['wrongFit']['done'] and F1['wrongFit']['known'], f"a wrong call: to the filter bank, its cartridge used up, not fixed: {F1['atWrong']} {F1['wrongFit']}")
            check(F1['saveSame'] and F1['savedP1'] and F1['saveBytes'] < 1100, f"the save mid-case reads back the same ({F1['saveBytes']} bytes)")
            check(F1['atRight'] is None and F1['fixed'] and F1['closed'] and F1['done'] == 0, f"the right call: the pump, fixed, closed (one wrong call: not right first time): {F1}")
        M9 = g.ev(P1M9)
        print('P1 after the tracing lesson:', M9)
        check(M9['day11'] is None and M9['staged'] and M9['due'] == M9['now'] and M9['logDay'] == 11, f"with an m9 row, P1's first waits for the tracing lesson, then the pump goes from then, its logs from the day before: {M9}")
        # P2 (0.55.15)
        R2 = g.ev(P2); R2b = g.ev(P2)
        p2c = R2['cases']; print(f"P2 sweep: {len(p2c)} cases ({R2['fit']} fitted)"); [print('  ', c) for c in p2c[:1]]
        check(len(p2c) >= 10, f"P2 cases: {len(p2c)} of {R2['fit']}")
        check(json.dumps(R2) == json.dumps(R2b), 'P2: twice -> the same cases and witnesses')
        nmix = sum(1 for c in p2c if any(k['mix'] for k in c['clues']))
        check(nmix >= 1, f"some P2 cases have a mix-up: {nmix}/{len(p2c)}")
        for c in p2c:
            sus, clues, (sn, cn, few, decks) = c['sus'], c['clues'], lim(c)
            left = lambda ks: [s for s in sus if not any(s in k['kills'] for k in ks)]
            real = [k for k in clues if not k['mix']]
            fewest = min((n for n in range(1, len(clues) + 1) for ks in combinations(clues, n) if len(left(list(ks))) == 1), default=99)
            check(c['kind'] == 'p2' and left(real) == [c['cause']] and all(len(left([k])) > 1 for k in clues) and fewest == c['fewest'] and fewest >= few, f"{c['id']}: solved without the mix-up, no single witness solves it: {left(real)} {fewest}")
            check(sn[0] <= len(sus) <= sn[1] and cn[0] <= len(clues) <= cn[1] and len(real) <= 3 and len(clues) - len(real) <= 1, f"{c['id']}: within the band: {len(sus)} suspects, {len(real)} witnesses + {len(clues) - len(real)} mix-up")
            check(all(k['there'] and k['inWindow'] and k['reach'] for k in clues), f"{c['id']}: every witness really was where they say, in the window: {[(k['who'], k['t'], k['there'], k['inWindow']) for k in clues]}")
            check(all(k['near'] for k in real) and all(k['mix'] is None or (k['other'] and k['trap'] and not k['kills']) for k in clues), f"{c['id']}: witnesses by the machine; a mix-up on another deck, when the real one was quiet, crossing out nothing: {clues}")
            check(c['wait'] and c['hidden'] and c['shown'], f"{c['id']}: waits for its window, then shows ({c['title']!r})")
            check(all(k['line'] and str(k['t'] % 1440 // 60).zfill(2) in k['line'] for k in clues), f"{c['id']}: each witness's words say when: {[k['line'] for k in clues][:2]}")
        G = g.ev(P2GATE)
        print('P2 gate and first:', G)
        check(G.get('staged') and G.get('machine') in ('4-scrubber-2', '4-scrubber-1') and G.get('cause') == 'bearing' and G.get('reserved') == 22 and G.get('hidden'), f"P2's first: a Deck 4 scrubber's bearing from Day 14 16:00, slot 22, hidden: {G}")
        if G.get('staged'):
            check(G['sus'] == ['bearing', 'filter', 'panel'], f"the page's suspects: {G['sus']}")
            check(G['at559'] == [None, False, 0, 0, True] and G['rowOpen'][1:] == [False, 0, 0, True], f"before Tomas's word: no P2 case, no Ask button, no witness line (05:59 {G['at559']}, row open {G['rowOpen']})")
            check(G.get('rollBefore') in (None, False) or G.get('rollBefore') != 'p2', f"no roll P2 case before the word: {G.get('rollBefore')}")
            check(G.get('meal') and G.get('beforeWord', [None])[0] is None and G.get('word', [None])[0] == 15 and G['word'][1] == 15 and G['word'][2] == 15, f"Tomas's word at a meal you share, Day 15: {G.get('meal')} {G.get('here')} {G.get('word')}")
            check(G['shown'] and 'now and then' in G['title'] and G['by'] == 'tomas', f"then the first case shows: {G['title']!r}")
            check(2 <= G['n'] <= 4 and all(w['there'] for w in G['ws']) and all(w['deck'] == 4 for w in G['ws'] if not w['mix']), f"its witnesses really were there: {G['ws']}")
            check(any(w['mix'] for w in G['ws']), f"the first case has its honest mix-up, as on the page: {G['ws']}")
            check(G['asks'] == G['n'] and G['nonWitness'], f"an Ask button for each witness ({G['asks']}) and nobody else")
            check(G.get('line1') and G['line1'] == G['line2'] and len(G['got']) == 1, f"asking gives their line, the same twice, and the clue: {G.get('line1')!r}")
            check(G['saved'][0] == 15 and G['saved'][1] and G['saved'][2] == G['n'] and G['saved'][3] < 2400, f"the save keeps the word and the case: {G['saved']}")
            check(G['fixed'] and G['closed'] and G['done'] & 2, f"the right call fixes it, right first time: {G['fixed']} {G['done']}")
        g.ev(T2_UNDO)
        pe = [e for e in g.errors if e.startswith('pageerror')]
        check(not errs and not pe, f'no errors: {errs} {pe}')
        g.close()

run(sys.argv[1])
print('PUZZLE CHECK OK' if ok else 'PUZZLE CHECK FAILED')
sys.exit(0 if ok else 1)
