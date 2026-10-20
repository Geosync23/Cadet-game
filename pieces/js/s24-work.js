// =====================================================================
// 24. WORK
// Pillar 5, your Works career (the Works career engineer, 0.44.x; plans/mechanics/foundation.html, "section 24
// core"; plans/pillar5-plan.md Part 1). 24 core first: the ladder of new kinds of work, training moments, tools,
// skill in words, your Works reputation and "What's next", and the device's Works app. Then one sub-block per
// mechanic (// 24a ROUNDS ...), each removable on its own: a sub-block registers WORK_MECH[id] for its ladder row,
// and a row whose sub-block isn't in the build never opens (nor blocks the rows after it, except by its own needs).
// Lazy: SHIP.works is made the first time anything asks after Day 1's shift (worksInit), never at load. Nothing here
// calls R(); choices come from schedU keys 850-854 (850 a training's meeting time; 851 which "What's next" line
// today, display only; 852-854 spare). A sub-block keeps its own data in SHIP.works under its own key and reads it back
// from the save itself (worksClean keeps only 24 core's fields), as 24k and 24f do.
//   SHIP.works (saved as ship.works) = { v: 1, tier, rank, xp (since your last promotion), tr: { ladder id: day
//   trained }, use: { id: uses }, op: { day: [ids opened (or offered again) that day] }, tools: { id: [day given,
//   wear 0-1] }, sk: { machine kind: jobs turned in }, log: [[job id, day, flags, kind, who noticed?], ... the last
//   30] (flags: 1 found by you, 2 right first time, 4 clever), test: null | { tier, day, tries, passed }, home,
//   done, ms (Step 3's promotion page), said ({ ladder id: day }, 24k's P2), cur: null | the training under way { id, st: 'ask' | 'meet' | 'watch' | 'do'
//   | 'again', d: its day, by: the teacher, occ: the occasion's key, j: the training job, w: minutes watched } }
// The hooks other sections give it (DEV_NOTES "Hook register"): section 12's main loop calls worksCareerTick() (24's own
// line); section 14's escortPlanOf asks worksEscort(p, t); section 19's Record asks worksRecordHead(); section 15b's
// locker asks worksLockerText(); section 17 reads worksBand() (the hold order) and calls ladderTick(h) from jobsHour
// (harmless twice: the ladder opens once a day). It reads section 17's jobs (jobReserve, jobFinish, SHIP.jobs,
// j.foundBy, j.rightFirst, j.clever), 20's OCCASIONS and occasionAdd, 13's notes, 15's mailSend, 21's SHIP.intro.
const WORK_RANKS = ['junior', 'officer', 'senior', 'specialist'];   // (section 17 has RANKS too, the same)
const RANK_TITLE = { junior: 'Junior Technician', officer: 'Works Officer', senior: 'Senior Officer', specialist: 'Engine Specialist' };
const WORKS_START = 1020;                                // Day 1's shift ends (17:00): SHIP.works can be made from then
const WORKS_ASK = [360, 630];                            // a big ladder row opens (its ask) on a workday between 06:00 and 10:30
const WORKS_SMALL = 960;                                 // a small one any hour from 06:00 to 16:00 (a word on the job itself)
const WORKS_LOG = 30;                                    // the work log keeps your last 30 jobs
// the ladder (Steps 1 and 2; later steps add their rows). needs: { intro: 'shadow' } Day 1's shadow shift done (or,
// with the intro skipped, any job of yours turned in) | { mech, uses } | { trained } | { rep: band } | { work: n }
// (Pillar 4's SHIP.rep.ship.work) | { flag } | a list, all of them. by: the teacher (the first on shift that day).
// (m7 and p3: Torres is off on Fridays, so Emeka Halloran teaches them on Day 5, Calder the last fallback: the designer
// and the lead, 210b86f.) where: the meeting place. job: the training job's kind (jobReserve, or the sub-block's own reserve). stages: the
// first is the main path; later ones open with use. fixed: { wd: weekday, Monday 1, at } for rows set in the week.
// xp: Works reputation for each use (the drill and the inspection, attended).
const CAREER_LADDER = [
  { id: 'm1', name: 'Rounds', size: 'big', day: 2, tier: 1, rank: 'junior', needs: { intro: 'shadow' }, by: ['torres-zeke'], where: { deck: 5, room: 'w' }, job: 'round', tool: 'clipboard', stages: [{ uses: 0 }, { uses: 5 }, { mech: 'm7' }] },
  { id: 'm4', name: 'Hauling and stores', size: 'big', day: 3, tier: 1, rank: 'junior', needs: { mech: 'm1', uses: 1 }, by: ['esposito-yara'], where: { deck: 5, room: 'r' }, job: 'haul', stages: [{ uses: 0 }, { uses: 2 }] },   // stage 1 (0.45.13, step4-stages): after 2 runs, from Day 10, you choose the order
  { id: 'm3d', name: 'The drill', size: 'small', day: 3, tier: 1, rank: 'junior', needs: null, by: ['calder'], fixed: { wd: 3, at: 900 }, xp: 1, stages: [{ uses: 0 }] },
  { id: 'm5', name: 'Tuning', size: 'big', day: 4, tier: 1, rank: 'junior', needs: { mech: 'm4', uses: 1 }, by: ['calder', 'brennan'], where: { deck: 3, room: 'K' }, job: 'tune', stages: [{ uses: 0 }, { uses: 5 }] },
  { id: 'm3i', name: 'The inspection', size: 'small', day: 4, tier: 1, rank: 'junior', needs: null, by: ['tomas'], fixed: { wd: 4, at: 390 }, xp: 1, stages: [{ uses: 0 }] },
  { id: 'm7', name: 'The scanner', size: 'big', day: 5, tier: 1, rank: 'junior', needs: { mech: 'm5', uses: 1 }, by: ['torres-zeke', 'halloran-emeka', 'calder'], where: { deck: 5, room: 'w' }, job: 'scan', tool: 'scanner', stages: [{ uses: 0 }, { uses: 5 }] },
  { id: 'p3', name: 'What\'s been tried?', size: 'small', day: 5, tier: 1, rank: 'junior', needs: { trained: 'm7' }, by: ['torres-zeke', 'halloran-emeka', 'calder'], stages: [{ uses: 0 }] },
  { id: 'm6', name: 'Making it safe', size: 'big', day: 8, tier: 1, rank: 'junior', needs: { mech: 'm7', uses: 1 }, by: ['calder'], where: { deck: 5, room: 'o' }, job: 'incident', stages: [{ uses: 0 }, { uses: 3 }] },
  { id: 'm2', name: 'Your work uniform', size: 'small', day: 8, tier: 1, rank: 'junior', needs: { flag: 'works.oily' }, by: ['torres-zeke'], stages: [{ uses: 0 }] },
  { id: 't2', name: 'Your Tier 2 test job', size: 'big', day: 9, tier: 1, rank: 'junior', needs: [{ rep: 'relied' }, { trained: 'm6' }], by: ['calder', 'vance'], where: { deck: 5, room: 'o' }, job: 'test', stages: [{ uses: 0 }] },
  // Step 3, Tier 2 (0.44.22: rows here so worksClean keeps their state; their sub-blocks are 24h's m8 and 24k's p1/p2;
  // m9 is 24i's, here too so a reload keeps it). m8 opens once you're an officer (Day 11 for a steady player: promoted on Day 10)
  { id: 'm8', name: 'Team jobs', size: 'big', day: 11, tier: 2, rank: 'officer', needs: { trained: 't2' }, by: ['torres-zeke', 'halloran-emeka', 'calder'], where: { deck: 3, room: 'R' }, job: 'team', stages: [{ uses: 0 }, { uses: 2 }] },
  { id: 'm9', name: 'Tracing', size: 'big', day: 12, tier: 2, rank: 'officer', needs: null, by: ['calder', 'halloran-emeka'], where: { deck: 5, room: 'w' }, job: 'trace', tool: 'pipekit', stages: [{ uses: 0 }] },   // M3's 24i
  { id: 'p1', name: 'When does it happen?', size: 'small', day: 12, tier: 2, rank: 'officer', needs: { trained: 'm9' }, by: ['calder', 'halloran-emeka'], stages: [{ uses: 0 }] },
  { id: 'p2', name: 'Who saw what?', size: 'small', day: 15, tier: 2, rank: 'officer', needs: null, by: ['tomas', 'torres-zeke'], stages: [{ uses: 0 }] },
  // Step 4's side jobs (0.45.8, E1 in 24 core's slot; each row as its seat sent it, inert until its sub-block registers WORK_MECH[id]).
  // m15 (rewiring, E2) and the fault-finder ticket's row come with their builds; cabin touches and star logging (24t) have none
  { id: 'm10', name: 'The workshop', size: 'small', day: 12, tier: 2, rank: 'officer', needs: null, by: ['torres-zeke', 'halloran-emeka', 'calder'], where: { deck: 5, room: 'f' }, stages: [{ uses: 0 }, { uses: 3 }, { uses: 6 }] },   // E3's 24j
  { id: 'm11', name: 'Tool upkeep', size: 'small', day: 12, tier: 2, rank: 'officer', needs: null, by: ['torres-zeke', 'halloran-emeka'], where: { deck: 5, room: 'w' }, stages: [{ uses: 0 }, { uses: 2 }, { uses: 4 }] },   // E1's 24m: the scanner; the pipe kit and logger (as each arrives); the team's rack after 4 upkeeps
  { id: 'm12', name: 'The logbook', size: 'small', day: 12, tier: 2, rank: 'officer', needs: null, by: ['calder'], where: { deck: 5, room: 'w' }, stages: [{ uses: 0 }, { uses: 5 }, { uses: 10 }] },   // E1's 24n: a line a shift; flag a machine after 5; your notes come back after 10
  { id: 'm13', name: 'Leak hunting', size: 'small', day: 12, tier: 2, rank: 'officer', needs: null, by: ['torres-zeke', 'halloran-emeka', 'calder'], job: 'leak', stages: [{ uses: 0 }, { uses: 3 }] },   // E2's 24o
  { id: 'm14', name: 'Garden irrigation', size: 'small', day: 13, tier: 2, rank: 'officer', needs: null, by: ['cruz-tove', 'oneill-imani', 'hart-ravi'], job: 'nozzle', stages: [{ uses: 0 }, { uses: 2 }, { uses: 4 }] },   // E2's 24q (the garden crew; 24r may set its own at its first posting)
  { id: 'm15', name: 'Rewiring', size: 'big', day: 17, tier: 2, rank: 'officer', needs: null, by: ['calder'], where: { deck: 4, room: '-' }, job: 'rewire', tool: 'tester', stages: [{ uses: 0 }, { uses: 3 }] },   // E2's 24q (0.45.11)
  { id: 'm17', name: 'The lift roof', size: 'big', day: 18, tier: 2, rank: 'officer', needs: null, by: ['halloran-emeka'], stages: [{ uses: 0 }, { uses: 2 }] },   // E3's 24s
];
const WORK_MECH = {};                                    // the sub-blocks: WORK_MECH[ladder id] = { open?(row, day), offer?(row, cur, day, t) -> bool (its own ask), at?(day) -> earliest meeting minute, reserve?(day, at, slot, o) -> job id, noJob?, watch? (minutes), hold? }
const WORK_TOOLS = {
  clipboard: { name: 'the round clipboard', mech: 'm1', wearPerUse: .01 },
  scanner: { name: 'the scanner', mech: 'm7', wearPerUse: 0 },     // these three wear at the use (toolWear: a scan 4, a trace 5,
  pipekit: { name: 'the pipe kit', mech: 'm9', wearPerUse: 0 },     // a use 3 of 100; M11, 0.45.7), not again on worksUse (with tracing, M3's m9, Day 12)
  logger: { name: 'the data logger', mech: 'p5', wearPerUse: 0 },
  tester: { name: 'the conduit tester', mech: 'm15', wearPerUse: .02 },
  calrig: { name: 'the test rig', mech: 'm10', wearPerUse: 0, bench: true },   // a bench in the machine shop, not carried
};
// your Works reputation in your rank: five words; numbers stay inside. Tier 1 is tuned by career_check (a steady
// player reaches "Relied on" by the end of Day 8, a very busy one not before Day 5); later tiers get theirs on their steps' pages
const WORK_BANDS = { 1: [[0, 'new'], [8, 'steady'], [18, 'reliable'], [30, 'trusted'], [40, 'relied']], 2: [[0, 'new'], [12, 'steady'], [28, 'reliable'], [45, 'trusted'], [60, 'relied']] };   // 2: C2's 0.44.19 numbers, kept by Step 4's page (0.45.7): about a dozen steady workdays to "Relied on" as an officer; side jobs add +2 a day at most (worksSideXp)   // the page's; with section 17's real faults in (0.44.10): steady 45-48 by the end of Day 8, a very busy player 35 at the end of Day 4
const BAND_WORD = { new: 'New', steady: 'Steady', reliable: 'Reliable', trusted: 'Trusted', relied: 'Relied on' };
const WORK_XP = { service: 1, repair: 2, overhaul: 3, missed: -3, abandoned: -2 };
const WORKS_RIGHT_FROM = 5;                              // "right first time" counts from Day 5 (the scanner)
const ladderRow = id => CAREER_LADDER.find(r => r.id === id) || null;
const worksDay = t => Math.floor(t / 1440) + 1;
const worksName = id => { try { const p = evPerson(id); return p ? p.name : id; } catch (e) { return id; } };
const worksFirst = id => worksName(id).replace(/^(Chief|Chef|Commander|Captain)\s+/, '').split(' ')[0];
// the Works writer's words (content/works/*.lines; keys in content/works/keys-p5.md), else the stand-in; {x} filled from
// vars; k picks among several (What's next: one a day)
function worksText(key, fallback, vars, k = 0) {
  const L = typeof LINES !== 'undefined' && LINES[key], e = Array.isArray(L) && L.length ? L[k % L.length] : null;
  const t = e && typeof e.text === 'string' ? e.text : fallback;
  return typeof t === 'string' ? t.replace(/\{(\w+)\}/g, (m, x) => x === 'me' ? (() => { try { return chatName(); } catch (y) { return 'you'; } })() : vars && vars[x] != null ? String(vars[x]) : m) : t;
}
const worksHas = key => typeof LINES !== 'undefined' && Array.isArray(LINES[key]) && LINES[key].length > 0;
const mechName = id => worksText('works.mech.' + id, (ladderRow(id) || { name: id }).name);
function worksVoice(id, flagKey) {                       // a teacher's own lines under a flag (kind 'work'), in order, or null
  try { const v = typeof VOICE !== 'undefined' && VOICE[id], who = typeof linesWho === 'function' ? linesWho(id) : null;
    const out = ((v && v.lines && v.lines.work) || []).filter(x => x.flag === flagKey).map(e => who && typeof linesFill === 'function' ? linesFill(e.text, who, { t: shipNow(), flags: { [flagKey]: true } }) : e.text).filter(Boolean);
    return out.length ? out : null; } catch (e) { return null; }
}
// a teacher's words at a step, for the sub-blocks too: their own lines under flag train.<mech>.<key> (key e.g.
// 'lead.look', 'follow.hold'), else the fallback; said in their bubble (or a toast). Returns what was said, or null
function worksTeach(mech, who, key, fallback) { const l = worksVoice(who, 'train.' + mech + '.' + key) || (fallback ? [].concat(fallback) : null); if (l) worksSayAll(who, l); return l; }
function worksSayAll(id, lines) { (lines || []).forEach((l, i) => { if (!i) worksSay(id, l); else if (typeof simTimeout === 'function') simTimeout(() => worksSay(id, l), 5200 * i); }); }
SHIP.works = null;
(() => { const s = SAVED && SAVED.ship && SAVED.ship.works; if (s && typeof s === 'object' && s.v === 1) SHIP.works = worksClean(s); })();
// a save's ship.works read back: unknown keys dropped, numbers clamped, the log cut to 30; a junk save means none
function worksClean(s) {
  try {
    const int = (v, lo, hi, x) => Number.isInteger(v) ? Math.max(lo, Math.min(hi, v)) : x, obj = o => o && typeof o === 'object' && !Array.isArray(o);
    const ids = new Set(CAREER_LADDER.map(r => r.id)), days = o => { const out = {}; if (obj(o)) for (const k in o) if (ids.has(k) && Number.isInteger(o[k])) out[k] = Math.max(0, o[k]); return out; };
    const op = {}; if (obj(s.op)) for (const k in s.op) if (/^\d{1,4}$/.test(k) && Array.isArray(s.op[k])) op[k] = s.op[k].filter(x => ids.has(x)).slice(0, 6);
    const tools = {}; if (obj(s.tools)) for (const k in s.tools) { const v = s.tools[k]; if (WORK_TOOLS[k] && Array.isArray(v) && Number.isInteger(v[0])) tools[k] = [v[0], Math.max(0, Math.min(1, +v[1] || 0))]; }
    const sk = {}; if (obj(s.sk)) for (const k of Object.keys(s.sk).slice(0, 60)) if (k.length <= 24 && Number.isInteger(s.sk[k])) sk[k] = Math.max(0, Math.min(9999, s.sk[k]));
    const log = Array.isArray(s.log) ? s.log.filter(e => Array.isArray(e) && typeof e[0] === 'string' && Number.isInteger(e[1])).slice(-WORKS_LOG)
      .map(e => [e[0].slice(0, 80), e[1], int(e[2], 0, 255, 0), typeof e[3] === 'string' ? e[3].slice(0, 24) : ''].concat(typeof e[4] === 'string' ? [e[4].slice(0, 40)] : [])) : [];
    const c = s.cur, cur = obj(c) && ids.has(c.id) && /^(ask|meet|watch|do|again|held)$/.test(c.st) ? { id: c.id, st: c.st, d: int(c.d, 0, 99999, 0), by: typeof c.by === 'string' ? c.by : null,
      occ: typeof c.occ === 'string' ? c.occ : null, j: typeof c.j === 'string' ? c.j : null, w: int(c.w, 0, 999, 0), ...(c.hold ? { hold: true } : {}), ...(typeof c.told === 'boolean' ? { told: c.told } : {}), ...(typeof c.mail === 'string' ? { mail: c.mail.slice(0, 80) } : {}) } : null;
    const t = s.test, test = obj(t) ? { tier: int(t.tier, 1, 4, 2), day: int(t.day, 0, 99999, 0), tries: int(t.tries, 0, 99, 0), passed: !!t.passed } : null;
    return { v: 1, tier: int(s.tier, 1, 4, 1), rank: WORK_RANKS.includes(s.rank) ? s.rank : 'junior', xp: isFinite(s.xp) ? Math.max(0, Math.min(9999, +s.xp)) : 0,
      tr: days(s.tr), use: (() => { const u = {}; if (obj(s.use)) for (const k in s.use) if (ids.has(k) && Number.isInteger(s.use[k])) u[k] = Math.max(0, Math.min(9999, s.use[k])); return u; })(),
      op, tools, sk, log, test, home: typeof s.home === 'string' ? s.home.slice(0, 16) : 'bunk',
      done: Array.isArray(s.done) ? s.done.filter(x => typeof x === 'string').slice(0, 40) : [], said: days(s.said),   // said: { ladder id: day } (24k's P2: Tomas's word; 0.44.22)
      ms: Array.isArray(s.ms) ? s.ms.filter(e => Array.isArray(e) && typeof e[0] === 'string' && Number.isInteger(e[1])).slice(0, 40).map(e => [e[0].slice(0, 40), e[1]]) : [], cur,
      side: obj(s.side) && JSON.stringify(s.side).length < 65536 ? s.side : {} };   // side: Step 4's side jobs, kept whole (each sub-block reads its own key defensively; E1 0.45.7)
  } catch (e) { return null; }
}
SAVE_EXTRA.push(s => { if (SHIP.works) s.ship.works = SHIP.works; });
onSim('newGame', () => { SHIP.works = null; WORKS_TICK.h = -1; WORKS_TICK.m = -1; WORKS_TAB = 'training'; });
function worksInit(now = shipNow()) {
  if (SHIP.works) return SHIP.works;
  if (now < WORKS_START) return null;                    // not before Day 1's shift has ended
  return SHIP.works = { v: 1, tier: 1, rank: 'junior', xp: 0, tr: {}, use: {}, op: {}, tools: {}, sk: {}, log: [], test: null, home: 'bunk', done: [], said: {}, ms: [], cur: null, side: {} };   // side: Step 4's side jobs, right after cur so a reload keeps the key order (BM7, 0.45.11)
}
// ---- the ladder ----
const worksOpened = (W = SHIP.works) => new Set(W ? Object.values(W.op).flat() : []);
const worksIsOpen = id => worksOpened().has(id);       // a row has opened (its kind is "open": a head-scratcher kind counts from here, not from trained)
function ladderNeeds(n, W) {                             // are a row's needs met (from saved state only)
  if (!n) return true;
  if (Array.isArray(n)) return n.every(x => ladderNeeds(x, W));
  if (n.intro) return worksShadowDone(W);
  if (n.mech) return (W.use[n.mech] || 0) >= (n.uses || 1);
  if (n.trained) return W.tr[n.trained] !== undefined;
  if (n.rep) { const B = WORK_BANDS[W.tier] || WORK_BANDS[1], k = B.findIndex(b => b[1] === n.rep); return k >= 0 && W.xp >= B[k][0]; }
  if (n.work) return typeof careerWork === 'function' ? careerWork() >= n.work : true;
  if (n.flag) return !!(typeof flag === 'function' && flag(n.flag));
  return false;
}
function worksShadowDone(W = SHIP.works) {               // Day 1's shadow shift (section 21), or with the intro skipped or off any job of yours turned in
  const I = SHIP.intro; if (I && I.done && (I.done['d1-shadow:job'] !== undefined || I.done['d1-shadow'] !== undefined && !(I.missed || []).includes('d1-shadow'))) return true;
  return !!(W && W.log.length) || (SHIP.jobs || []).some(j => j.status === 'done' && j.doneBy === 'you');
}
const ladderTeacher = (row, d) => (row.by || []).find(id => { try { return occOnShift(id, d); } catch (e) { return false; } }) || null;
// once a ship hour (worksTick; section 17's jobsHour may call it too): on a workday of yours from 06:00 (a big one by
// 10:30, a small one by 16:00), open the first big and the first small row whose day has come and whose needs are met; at most one of each a day; none
// on a day off. A training not finished is offered again (that day's big one). Returns the ids opened.
function ladderTick(h) {
  const t = h * 60, d = worksDay(t), m = t - (d - 1) * 1440, W = worksInit(t), out = [];
  if (!W || m < WORKS_ASK[0] || m > WORKS_SMALL || !playerShiftOn(d) || d < worksDay(shipNow())) return out;   // never for a day already past (section 17's catch-up after a load runs jobsHour from long ago)
  const today = W.op[d] || [], has = size => today.some(id => (ladderRow(id) || {}).size === size), opened = worksOpened(W);
  const c = W.cur;
  if (c && c.st === 'held' && c.d < d) worksEscortEnd(c.id);   // a hold left from an earlier day: trained now (the ladder never stalls)
  if (c && c.d < d && (c.st === 'ask' || c.st === 'again') && !has('big') && m <= WORKS_ASK[1]) { const row = ladderRow(c.id); if (row && trainOffer(row, c, d, t)) { (W.op[d] = W.op[d] || []).push(row.id); out.push(row.id); } }
  for (const size of ['big', 'small']) {
    if ((W.op[d] || []).some(id => (ladderRow(id) || {}).size === size) || (size === 'big' && (W.cur || m > WORKS_ASK[1]))) continue;
    const row = CAREER_LADDER.find(r => r.size === size && !opened.has(r.id) && WORK_MECH[r.id] && d >= r.day && r.tier <= W.tier && (!r.fixed || weekday(d) + 1 === r.fixed.wd) && ladderNeeds(r.needs, W));
    if (row && ladderOpen(row, d, t)) out.push(row.id);
  }
  return out;
}
function ladderOpen(row, d, t) {
  const W = SHIP.works;
  if (row.size === 'big') {
    const by = ladderTeacher(row, d); if (!by) return false;   // the teacher isn't on shift today: it waits for a day they are
    W.cur = { id: row.id, st: 'ask', d, by, occ: null, j: null, w: 0 };
    if (!trainOffer(row, W.cur, d, t)) { W.cur = null; return false; }
  }
  (W.op[d] = W.op[d] || []).push(row.id);
  try { if (WORK_MECH[row.id].open) WORK_MECH[row.id].open(row, d); } catch (e) { console.error(e); }
  simNote('ladder', { mech: row.id, size: row.size, day: d });
  return true;
}
// uses (each sub-block calls worksUse when you finish one: a round walked, a run delivered): counts, wears the tool,
// any reputation the row gives (the drill, the inspection), and a small row's first use is its training
function worksUse(mech, n = 1) {
  const W = worksInit(); if (!W || !ladderRow(mech)) return 0;
  const row = ladderRow(mech); W.use[mech] = (W.use[mech] || 0) + n;
  if (row.xp) worksXp(row.xp * n);
  for (const k in WORK_TOOLS) if (WORK_TOOLS[k].mech === mech && W.tools[k]) W.tools[k][1] = Math.min(1, W.tools[k][1] + WORK_TOOLS[k].wearPerUse * n);
  if (row.size === 'small' && W.tr[mech] === undefined && worksOpened(W).has(mech)) worksTrained(mech);
  return W.use[mech];
}
function worksStage(mech) {                              // the highest stage whose condition holds (stage 0 once trained or used)
  const W = SHIP.works, row = ladderRow(mech); if (!W || !row) return -1;
  let k = -1; (row.stages || [{ uses: 0 }]).forEach((s, i) => { if (s.mech ? W.tr[s.mech] !== undefined : (W.use[mech] || 0) >= (s.uses || 0) && (W.tr[mech] !== undefined || W.use[mech])) k = i; });
  return k;
}
// ---- training moments: the ask (toast, Mail, an appointment with the teacher, the goal arrow), the meeting
// (MEETING_SCRIPTS['train.' + id]), they lead a training job and you watch, then you do one and they follow, then
// trained. Not there? It's offered again the next workday; nothing is missed. ----
const TRAIN_WATCH = 15;                                  // ship minutes watching the teacher work before your turn
const TRAIN_NEAR = 3;                                    // tiles from the job's spot that count as watching
function trainSetup(row) {                               // made when first asked (never at load): the occasion
  const id = 'works.' + row.id;
  if (!OCCASIONS[id]) OCCASIONS[id] = { title: 'Training: ' + row.name.charAt(0).toLowerCase() + row.name.slice(1), kind: 'meeting', by: row.by[0], deck: (row.where || {}).deck || 5, room: (row.where || {}).room || 'w', at: 540, len: 30, script: 'train.' + row.id, due: () => false, mail: null };
  return OCCASIONS[id];
}
function trainScript(row, by) {                          // the writer's meeting for who teaches (train.<id>.<teacher>), else a stand-in made now
  const id = 'train.' + row.id + '.' + by; if (MEETING_SCRIPTS[id]) return id;
  if (MEETING_SCRIPTS['train.' + row.id]) return 'train.' + row.id;
  MEETING_SCRIPTS[id] = { title: row.name, from: worksName(by), stub: true,
    gist: worksFirst(by) + ' waited for you. ' + row.name + ' will keep: they\'ll ask again on your next workday.',
    lines: [{ who: by, text: row.size === 'big' ? 'Right. ' + row.name + '. I\'ll do one, you watch; then you do one and I watch.' : row.name + '. Watch how it\'s done.' },
      { who: by, text: row.size === 'big' ? 'Come on, follow me.' : 'That\'s all there is to it.' }] };
  return id;
}
for (const r of SHIP.occasions) if (/^works\./.test(r.id) && ladderRow(r.id.slice(6))) { const row = ladderRow(r.id.slice(6)), o = trainSetup(row); o.script = trainScript(row, r.by || row.by[0]); }   // a reload: its occasion closes and its meeting plays
function trainOffer(row, c, d, t) {                      // the ask, or the ask again: an appointment today at a time in both shifts
  const m = t - (d - 1) * 1440, by = ladderTeacher(row, d); if (!by) return false;
  c.by = by; c.d = d; c.w = 0;
  if (c.st === 'again') return trainWatch(row, c, t, true);
  const M = WORK_MECH[row.id] || {}; if (M.offer) { try { return !!M.offer(row, c, d, t); } catch (e) { console.error(e); return false; } }   // the sub-block's own ask (24f: m6's urgent call); it sets c.st = 'meet', c.occ, c.by
  let early = 0; try { early = M.at ? +M.at(d) || 0 : 0; } catch (e) { early = 0; }   // a sub-block's earliest meeting (24d: m4 after the delivery's unload)
  const at = Math.min(Math.max(900, early), Math.max(m + 60, 510, early) + Math.ceil(schedU(machSeed(row.id), d, 850) * 6) * 10), o = trainSetup(row);
  o.by = by; o.script = trainScript(row, by); const r = occasionAdd('works.' + row.id, (d - 1) * 1440 + at, false, o.len);
  if (!r) return false;
  c.st = 'meet'; c.occ = r.key; c.told = false;
  const place = DECKS[o.deck] && DECKS[o.deck].rooms[o.room] ? DECKS[o.deck].rooms[o.room].name : 'the Works bay', when = hhmm(at);
  const where = place.replace(/^Works Chief's office$/, 'the Chief\'s office') + ' on ' + deckIn(o.deck), ask = worksText('works.ask.' + row.id, '', { time: when, place: where, name: worksName(by) }), cut = ask.indexOf(' | ');
  let subject = 'Training: ' + mechName(row.id), body = 'Meet me in the ' + where.replace(/^the /, '') + ' at ' + when + '. I\'ll show you ' + mechName(row.id).replace(/^./, x => x.toLowerCase()) + '.';
  if (cut > 0) { subject = ask.slice(0, cut); body = ask.slice(cut + 3); if (body.indexOf(when) < 0) body += ' (' + when + ', ' + where + '.)'; }   // the writer's words; the time and place if they don't say
  if (typeof mailSend === 'function') mailSend({ at: t, from: worksName(by), subject, body, quiet: true });
  c.mail = subject.slice(0, 80);                         // trainTell shows this Mail, not another from the same person
  if (t >= shipNow() - 1) trainTell(row, c);              // in play now; asked during a sleep, it's told when you're up (trainTick)
  return true;
}
function trainTell(row, c) {                             // the ask in play: a toast and the goal arrow to the meeting
  const r = SHIP.occasions.find(x => x.key === c.occ); c.told = true; if (!r) return;
  const o = OCCASIONS['works.' + row.id], place = (DECKS[r.deck].rooms[r.room] || { name: 'the Works bay' }).name, when = hhmm(r.at % 1440);
  const m = (SHIP.mail || []).find(x => x.from === worksName(c.by) && x.subject === c.mail);
  try { toast(worksName(c.by), m ? m.body : 'Meet me in the ' + place + ' at ' + when + '.'); } catch (e) { /* no UI */ }
  if (typeof setGoal === 'function' && !(SHIP.player && SHIP.player.track)) setGoal({ deck: r.deck, room: r.room, label: mechName(row.id) + ' with ' + worksFirst(c.by) + ', ' + when });
}
function trainSpot(j) {                                  // where a training job is done: { deck, tile, room }
  if (!j) return null;
  const m = j.machine && typeof machineById === 'function' ? machineById(j.machine) : null;
  if (m) return { deck: m.deck, tile: m.panel.slice(), room: m.room };
  try { const st = jobStops(j).filter(x => x.step !== 'fetch'), s = st[st.length - 1], pl = s && s.places[0] && placeById(s.places[0]); if (pl) return { deck: pl.deck, tile: pl.at.slice(), room: pl.room }; } catch (e) { /* none */ }
  return null;
}
function trainWatch(row, c, t, again) {                  // the teacher's training job: they lead, you watch
  const W = SHIP.works, d = worksDay(t), slot = 10 + Math.max(0, CAREER_LADDER.filter(r => r.size === 'big').indexOf(row)) % 10, M = WORK_MECH[row.id] || {};
  if (M.noJob) { worksTrained(row.id); return true; }
  if (M.self) return trainDo(row, c, t);                 // the talk, then yours on the board, the arrow and tips leading (0.45.9: playtest 2, item 1)
  if (!M.reserve && !MACHINE_KINDS[row.job]) { worksTrained(row.id); return true; }   // no sub-block reserve and no machine kind: trained at the meeting (reviewer R: no stand-in faults)
  let id = null; try { id = M.reserve ? M.reserve(d, t - (d - 1) * 1440, slot, { train: row.id }) : jobReserve(row.job, d, t - (d - 1) * 1440, slot, { train: row.id }); } catch (e) { id = null; }
  if (!id) { c.st = 'again'; c.d = d; return false; }
  c.st = 'watch'; c.j = id; c.w = 0;
  const j = SHIP.jobs.find(x => x.id === id); if (j) j.train = row.id;
  worksSayAll(c.by, worksVoice(c.by, 'train.' + row.id + '.lead.take') || [again ? 'Let\'s try that again. Follow me, and watch.' : 'Follow me. Watch this one.']);
  return true;
}
function trainDo(row, c, t) {                            // your turn: the same slot, held for you; the teacher follows
  const d = worksDay(t), slot = 10 + Math.max(0, CAREER_LADDER.filter(r => r.size === 'big').indexOf(row)) % 10, M = WORK_MECH[row.id] || {};
  let id = null; try { id = M.reserve ? M.reserve(d, t - (d - 1) * 1440, slot, { train: row.id, yours: true }) : jobReserve(row.job, d, t - (d - 1) * 1440, slot, { train: row.id }); } catch (e) { id = null; }
  if (!id) { c.st = 'again'; return false; }
  c.st = 'do'; c.j = id; const j = SHIP.jobs.find(x => x.id === id); if (j) j.train = row.id;
  if (M.hold) c.hold = true;                             // the teacher stays with you until worksEscortEnd (24g's m7: until P3's case is called)
  if (!M.self) worksSayAll(c.by, worksVoice(c.by, 'train.' + row.id + '.lead.done') || ['Your turn. It\'s on the board for you; I\'ll be right behind you.']);
  return true;
}
function trainNear(spot) {                               // you're watching: on its deck, in its room or within a few tiles of it
  try {
    if (!spot || !deckDef || deckDef.num !== spot.deck || !player) return false;
    const [c, r] = player.here(); return roomAt(c, r) === spot.room || Math.hypot(c - spot.tile[0], r - spot.tile[1]) <= TRAIN_NEAR;
  } catch (e) { return false; }
}
function trainTick(now) {                                // once a ship minute in play
  const W = SHIP.works, c = W && W.cur; if (!c) return;
  const row = ladderRow(c.id); if (!row) { W.cur = null; return; }
  if (c.st === 'meet') {
    const r = SHIP.occasions.find(x => x.key === c.occ);
    if (r && c.told === false && now < r.at + r.len) trainTell(row, c);   // asked while you slept: told now you're up
    if (!r) { c.st = 'ask'; return; }
    if ((r.met || r.status === 'kept') && !(typeof DIALOGUE !== 'undefined' && DIALOGUE)) trainWatch(row, c, now, false);
    else if (r.status === 'missed') c.st = 'ask';        // offered again on your next workday
    return;
  }
  if (c.st === 'held') { if (!worksCaseOpen(c.j)) worksEscortEnd(c.id); return; }   // waiting on worksEscortEnd (the teacher stays with you), or its case closing
  if (c.st !== 'watch' && c.st !== 'do') return;
  const j = SHIP.jobs.find(x => x.id === c.j);
  if (c.st === 'watch') {
    if (j && j.claimedBy === 'you') { c.st = 'do'; return; }   // you went ahead and took it: the teacher follows instead
    if (!j || j.status === 'done' || !heldForYou(j)) { c.st = 'again'; return; }
    if (trainNear(trainSpot(j))) c.w++;
    if (c.w >= ((WORK_MECH[row.id] || {}).watch || TRAIN_WATCH)) {
      if (typeof jobFinish === 'function') jobFinish(j, now, c.by); else { j.status = 'done'; j.doneAt = now; j.doneBy = c.by; }
      if (typeof MACH_REV !== 'undefined') MACH_REV++;
      trainDo(row, c, now);
    }
    return;
  }
  if (j && j.status === 'done' && j.doneBy === 'you') { worksDone(row.id, now); return; }
  if (!j || j.status === 'done' || (!heldForYou(j) && j.claimedBy !== 'you')) c.st = 'again';
}
function worksTrained(id, t = shipNow()) {               // trained: the Training page, the tool, the note
  const W = worksInit(t), row = ladderRow(id); if (!W || !row || W.tr[id] !== undefined) return false;
  W.tr[id] = worksDay(t);
  if (row.tool) toolGive(row.tool, t);
  const by = W.cur && W.cur.id === id && W.cur.by || ladderTeacher(row, worksDay(t)) || row.by[0];
  const sc = MEETING_SCRIPTS['train.' + id + '.' + by] ? 'train.' + id + '.' + by : 'train.' + id;   // (small rows: never a stand-in)
  if (row.size === 'small' && MEETING_SCRIPTS[sc] && !MEETING_SCRIPTS[sc].stub && typeof dialogueShow === 'function' && !(typeof DIALOGUE !== 'undefined' && DIALOGUE)) dialogueShow(sc);   // a word on the job itself
  try { toast(worksName(by), worksText('works.trained', 'Trained: {mech}, with {name}.', { mech: mechName(id).replace(/^./, x => x.toLowerCase()), name: worksName(by) }) + (row.tool ? ' ' + toolName(row.tool).replace(/^./, x => x.toUpperCase()) + ' is yours now.' : '')); } catch (e) { /* no UI */ }
  if (W.cur && W.cur.id === id) W.cur = null;
  simNote('trained', { mech: id });
  return true;
}
// your training job turned in: trained, unless something holds the teacher with you (worksEscortHold: the designer's
// Day 5, where Torres's scanner lesson runs on into the P3 training case); worksEscortEnd(id) then trains you
const worksCaseOpen = jobId => { const C = SHIP.works && SHIP.works.cases; return !!(C && Array.isArray(C.open) && C.open.some(x => x && x.job === jobId)); };   // 24k's case on that job still open
function worksDone(id, t) { const c = SHIP.works && SHIP.works.cur; if (c && c.id === id && c.hold && worksCaseOpen(c.j)) { c.st = 'held'; return; } if (id === 't2' && typeof promoPassed === 'function') { promoPassed(t); return; } worksTrained(id, t); }   // 24p: the test job is passed, not trained   // held only while its case is still open
function worksEscortHold(id) { const c = SHIP.works && SHIP.works.cur; if (!c || c.id !== id || !/^(watch|do|meet|ask|again)$/.test(c.st)) return false; c.hold = true; return true; }
function worksEscortEnd(id) {
  const c = SHIP.works && SHIP.works.cur; if (!c || c.id !== id) return false;
  delete c.hold; if (c.st === 'held') worksTrained(id); return true;
}
onSim('caseCalled', n => { const c = SHIP.works && SHIP.works.cur; if (n && n.train && c && c.hold) worksEscortEnd(c.id); });   // 24k: the training case is called
// the teacher's walk (section 14's escortPlanOf asks): lead you to the training job while you watch, follow you while you do one
function worksEscort(p, t) {
  { const pe = p && typeof promoEscort === 'function' ? promoEscort(p, t) || promoMoveEscort(p, t) || promoCerEscort(p, t) : null; if (pe) return pe; }   // 24p: Calder comes to find you for the summons; the walk to your cabin; up to the ceremony
  const W = SHIP.works, c = W && W.cur; if (!c || !p || p.id !== c.by || (c.st !== 'watch' && c.st !== 'do' && c.st !== 'held') || worksDay(t) !== c.d) return null;
  const j = SHIP.jobs.find(x => x.id === c.j), spot = trainSpot(j);
  if (c.st === 'held') return spot ? { mode: 'follow', to: { deck: spot.deck, tile: spot.tile } } : null;   // they stay with you
  if (!j || j.status === 'done' || !spot || j.found > t) return null;   // (not before the job's due: 24p's test job is held from 09:00)
  if (c.st === 'do' && j.workDone && !c.hold) return null;   // done: they go back to their own work while you turn it in
  if (c.st === 'do' && (WORK_MECH[c.id] || {}).self) return null;   // a self-led training (m1, 0.45.9): the arrow and tips lead you, not the teacher
  return { mode: c.st === 'watch' ? 'lead' : 'follow', to: { deck: spot.deck, tile: spot.tile } };
}
function worksSay(id, text) {                            // the teacher says it in a bubble if they're on your deck, else a toast
  if (!text) return;
  try { const a = (typeof DECK_CREW !== 'undefined' ? DECK_CREW : []).find(x => x.p && x.p.id === id); if (a && typeof bubbleSay === 'function') { bubbleSay(a.h, text, 5); return; } toast(worksName(id), text); } catch (e) { /* no UI */ }
}
// ---- tools: they come with their training, live on the device's Tools page and in your locker; never in your hands ----
const hasTool = id => !!(SHIP.works && SHIP.works.tools[id]);
function toolGive(id, t = shipNow()) { const W = worksInit(t); if (!W || !WORK_TOOLS[id] || W.tools[id]) return false; W.tools[id] = [worksDay(t), 0]; simNote('tool', { id }); return true; }
// ---- tool wear (M11 tool upkeep's core, Step 4; built by E1 on C's behalf, 0.45.7). Wear stays 0-1 used (0 like new, so
// old saves load as they were); the page's numbers are charge = 100 - 100 x wear: the scanner 4 a scan, the pipe kit 5 a
// trace, the logger 3 a use; "Due" under 30, "Getting low" under 60. toolWear(id, n) wears it by n of 100 (none: just reads)
// and returns the wear; toolState(id) 'charged' | 'low' | 'due' (null: not yours); toolSlow(id) 1.25 for a due tool (a step
// takes a quarter longer, never blocked) and says so once a ship day. Upkeep at your bench (24m) puts the wear back to 0 ----
const toolUpkeepOn = () => !!SHIP.works && worksOpened().has('m11');   // wear counts only once M11 tool upkeep is open (Day 12, its row; reviewer R4 on 0.45.7): tools arrive charged
function toolWear(id, n) {
  if (!hasTool(id)) return 0; const v = SHIP.works.tools[id];
  if (n > 0 && toolUpkeepOn()) v[1] = Math.min(1, v[1] + n / 100);
  return v[1];
}
const TOOL_DUE = 30, TOOL_LOW = 60;
const toolCharge = id => hasTool(id) ? Math.round(100 - 100 * SHIP.works.tools[id][1]) : null;
const toolState = id => { const c = toolCharge(id); return c === null ? null : c < TOOL_DUE ? 'due' : c < TOOL_LOW ? 'low' : 'charged'; };
const toolStateWord = id => { const s = toolState(id); return s ? worksText('works.toolstate.' + s, { charged: 'Charged', low: 'Getting low', due: 'Due' }[s]) : ''; };
const TOOL_SLOW_SAY = { scanner: 'Your scanner\'s charge is low.', pipekit: 'Your pipe kit\'s seals are grubby.', logger: 'Your data logger\'s clip is worn.' };
function toolSlow(id) {
  if (toolState(id) !== 'due' || !toolUpkeepOn()) return 1;
  const S = worksSide(), d = worksDay(shipNow()), said = S && (S.slow && typeof S.slow === 'object' ? S.slow : (S.slow = {}));
  if (said && said[id] !== d && !SIM_AT) {
    said[id] = d;
    toast(toolName(id).replace(/^the /, '').replace(/^./, x => x.toUpperCase()), worksText('tool.due.' + id, (TOOL_SLOW_SAY[id] || 'Your ' + toolName(id).replace(/^the /, '') + ' wants looking after.') + ' Bench, when you can.'));   // W2's tool.due.<id>
  }
  return 1.25;
}
// ---- Step 4's side jobs (E1 on C's behalf, 0.45.7): their data lives under SHIP.works.side (worksClean keeps it whole;
// each sub-block reads its own key defensively, a missing one is its default). worksSideXp(n, why): Works reputation from a
// side job, +2 a ship day at most across all of them (so they help but never rush a promotion); returns what it gave
const SIDE_XP_DAY = 2, WORKS_SIDE_KINDS = new Set();   // side-job kinds (sub-blocks add theirs at load: WORKS_SIDE_KINDS.add('leak')): their turn-in reputation goes through the cap
const worksSide = () => { const W = SHIP.works; if (!W) return null; if (!W.side || typeof W.side !== 'object' || Array.isArray(W.side)) W.side = {}; return W.side; };
function worksSideXp(n, why) {
  const S = worksSide(); if (!S || !(n > 0)) return 0;
  const d = worksDay(shipNow()), x = S.xp && S.xp.day === d && Number.isFinite(S.xp.n) ? S.xp : (S.xp = { day: d, n: 0 }), give = Math.min(n, SIDE_XP_DAY - x.n);
  if (give <= 0) return 0;
  x.n += give; worksXp(give); simNote('sideXp', { why: String(why || '').slice(0, 24), n: give });
  return give;
}
const toolWord = w => w < .25 ? worksText('works.toolwear.new', 'like new') : w < .5 ? worksText('works.toolwear.good', 'in good order') : w < .75 ? worksText('works.toolwear.worn', 'well used') : worksText('works.toolwear.tired', 'wants looking after');
const toolName = id => worksText('works.tool.' + id, WORK_TOOLS[id] ? WORK_TOOLS[id].name : id);
function worksLockerText() {                             // section 15b's locker tap, one line (or null)
  const W = SHIP.works, ts = W ? Object.keys(W.tools).filter(k => !WORK_TOOLS[k].bench) : [];
  return ts.length ? worksText('works.locker', 'Your tools: {tools}.', { tools: ts.map(toolName).join(', ') }) : null;
}
// your locker (0.44.5): the Kit lockers in the Works bay ("Yours has your name on a strip of tape") say what tools are in
// yours, through section 15's PLAYER_TAPS (first in line, only once you have a tool). Bunk 1's wardrobe is section 21b's tap.
if (typeof PLAYER_TAPS !== 'undefined') PLAYER_TAPS.unshift((it, at) => {
  if (!it || it.t !== 'Kit lockers' || !worksLockerText() || typeof approach !== 'function') return false;
  approach(at.clone(), it.front, it.depth, () => toast(it.t, it.x + ' ' + worksLockerText())); return true;
});
// ---- skill in words (section 15's careerSpeed reads SHIP.works.sk; this counts and words it) ----
function skillWord(kind) { const n = SHIP.works && SHIP.works.sk[kind] || 0; return n >= 15 ? worksText('works.skill.know', 'you know these well') : n >= 5 ? worksText('works.skill.hang', 'getting the hang of these') : worksText('works.skill.new', 'new to you'); }
// ---- your Works reputation in your rank ----
function worksXp(n) { const W = worksInit(); if (!W || !n) return; W.xp = Math.max(0, W.xp + n); }
function worksBand() {                                   // 'new' ... 'relied', or null before SHIP.works (section 17 keeps today's order)
  const W = SHIP.works; if (!W) return null;
  const B = WORK_BANDS[W.tier] || WORK_BANDS[1]; let b = B[0][1]; for (const [x, k] of B) if (W.xp >= x) b = k; return b;
}
const worksBandWord = () => { const b = worksBand() || 'new', W = SHIP.works; return b === 'new' && W && W.rank !== 'junior' ? worksText('works.band.newofficer', 'New ' + (W.rank === 'specialist' ? 'specialist' : 'officer')) : worksText('works.band.' + b, BAND_WORD[b]); };
const worksRankTitle = (W = SHIP.works) => worksText('works.rank.' + (W ? W.rank : 'junior'), RANK_TITLE[W ? W.rank : 'junior']);
// your jobs turned in (simNote('job', { step: 'turnin' })): reputation, skill by machine kind, the work log
onSim('job', n => {
  if (!n || n.step !== 'turnin') return;
  const W = worksInit(n.t); if (!W) return;
  const j = (SHIP.jobs || []).find(x => x.id === n.id) || null, d = worksDay(n.t);
  const kind = n.job || (j && (j.chore || j.kind)) || '', m = n.machine && typeof machineById === 'function' ? machineById(n.machine) : null;
  const found = !!(j && (j.foundBy === 'you' || (n.machine && simNotes('found', (j.posted || 0) - 1).some(x => x.machine === n.machine && x.by === 'you'))));
  const right = !!(j && j.rightFirst && d >= WORKS_RIGHT_FROM), clever = !!(j && j.clever);
  const side = WORKS_SIDE_KINDS.has(kind) || j && WORKS_SIDE_KINDS.has(j.kind), xp = side ? (WORK_XP[kind] ?? 1) + (right ? 1 : 0) : (WORK_XP[kind] || 1) + (found ? 1 : 0) + (right ? 1 : 0) + (clever ? 1 : 0);
  if (j && j.xp === 0) { /* paid elsewhere (E2's leak joint: the leak's +1) */ } else if (side) worksSideXp(xp, j && j.kind || kind); else worksXp(xp);   // a side job's: flat (+1 more right first time: rewiring, 0.45.14), capped, +2 a day in all (0.45.7; flat 0.45.11, E2/R4)
  if (m) W.sk[m.kind] = (W.sk[m.kind] || 0) + 1;
  W.log.push([String(n.id).slice(0, 80), d, (found ? 1 : 0) | (right ? 2 : 0) | (clever ? 4 : 0), String(kind).slice(0, 24)]); if (W.log.length > WORKS_LOG) W.log.splice(0, W.log.length - WORKS_LOG);
  const c = W.cur; if (c && c.st === 'do' && c.j === n.id) worksDone(c.id, n.t);
});
onSim('job', n => {                                      // the teacher's word at each step of your training job
  const c = SHIP.works && SHIP.works.cur; if (!n || !c || c.st !== 'do' || n.id !== c.j || n.step === 'turnin') return;
  const key = n.step === 'stop' ? ({ job: 'hold', pickup: 'carry', drop: 'carry', cart: 'carry', load: 'carry', unload: 'carry', return: 'carry' }[n.tag] || n.tag || 'hold') : n.step;
  const say = worksVoice(c.by, 'train.' + c.id + '.follow.' + key) || [{ take: 'Good. Take your time.', done: 'Done. Turn it in at the board.' }[key] || (n.step === 'stop' ? 'That\'s it. Next.' : null)].filter(Boolean);
  worksSayAll(c.by, say);
});
onSim('shiftMissed', n => worksXp(WORK_XP.missed));
onSim('jobAbandoned', n => worksXp(WORK_XP.abandoned));
function worksNoticed(jobId, who) {                      // someone noticed a job of yours (section 20 may call it): the log shows who
  const e = SHIP.works && SHIP.works.log.find(x => x[0] === jobId); if (!e || typeof who !== 'string') return false; e[4] = who.slice(0, 40); return true;
}
// "What's next": one sentence, always true (the writer's content/works/next.lines, one a day if several): the training
// under way (next.wait.<id>), the test job when it's open (next.t2), else the next row that can open (next.<id>), else
// a word for where you stand (next.band.<band>)
function worksNext() {
  const W = SHIP.works, k = Math.floor(schedU(851, SHIP.time.day, 851) * 8);
  if (!W) return worksText('next.band.new', 'Keep at it: Calder\'s watching your work.', null, k);
  const c = W.cur, row = c && ladderRow(c.id), low = s => s.replace(/^./, x => x.toLowerCase());
  if (row) { const who = worksFirst(c.by || row.by[0]), r = c.occ && SHIP.occasions.find(x => x.key === c.occ), v = { name: worksName(c.by || row.by[0]), first: who, mech: low(mechName(row.id)) };
    const say = c.st === 'meet' && r ? who + ' wants to show you ' + v.mech + ': ' + hhmm(r.at % 1440) + ', ' + (DECKS[r.deck].rooms[r.room] || { name: 'the Works bay' }).name + '.'
      : c.st === 'watch' ? who + ' is showing you ' + v.mech + '. Watch closely.' : c.st === 'do' ? 'Your turn at ' + v.mech + ', with ' + who + ' watching.'
      : who + ' will show you ' + v.mech + ' on your next workday.';
    return c.st === 'meet' || c.st === 'again' || c.st === 'ask' ? worksText('next.wait.' + row.id, say, v, k) : say; }
  const opened = worksOpened(W);
  if (opened.has('t2') && !(W.test && W.test.passed)) return worksText('next.t2', 'Calder has your test job ready.', null, k);
  if (W.test && W.test.passed && typeof promoDone === 'function') {   // 24p: the promotion's steps (W2's next.summons / move / ceremony)
    const nx = (key, fb) => worksText('next.' + key, worksText('next.wait.' + key, fb, null, k), null, k);   // (either of the writer's names)
    if (!promoDone('summons2')) return nx('summons', 'Calder will want a word about your test job.');
    if (!promoDone('move2')) return nx('move', 'Your own cabin, 4-23, after the shift.');
    if (!promoDone('ceremony2')) return nx('ceremony', 'Your commission: the observation room, 17:15 tomorrow.'); }
  const next = CAREER_LADDER.find(r => !opened.has(r.id) && WORK_MECH[r.id] && r.tier <= W.tier && r.size === 'big');
  if (next) return worksText('next.' + next.id, worksFirst(next.by[0]) + ' will show you ' + mechName(next.id).replace(/^./, x => x.toLowerCase()) + ' when you\'re ready.', { name: worksName(next.by[0]), mech: mechName(next.id) }, k);
  return worksText('next.band.' + (worksBand() || 'new'), 'Keep at it: Calder\'s watching your work.', null, k);
}
// the Record's first lines (section 19 asks): your rank, your Works reputation and "What's next"
function worksRecordHead() {                             // null before SHIP.works (Days 0-1 keep the Record's old line)
  const W = SHIP.works; if (!W) return null; const tier = W.tier, v = { title: worksText('works.title.t' + tier, 'tier ' + tier), rank: worksRankTitle(W), band: worksBandWord(), next: worksNext() };
  const com = (W.ms.find(x => x[0] === 'commissioned') || [])[1], st = (W.ms.find(x => x[0] === 'stars') || [])[1];   // 24p: the ceremony; 24t: star logger (E3, 0.45.11)
  const ff = W.ms.filter(x => /^ff[1-3]$/.test(x[0])).sort((a, b) => a[0] < b[0] ? 1 : -1)[0], gr = ff ? +ff[0][2] : 0;   // E2's fault-finder grade (the highest)
  return { kind: 'text', mark: 'hot', text: worksText('works.record', '{rank}, {title}. Works reputation: {band}. What\'s next: {next}', v) + (com ? ' ' + worksText('works.ms.commissioned', worksText('works.record.commissioned', 'Commissioned Officer, Day {n}.', { day: com, n: com }), { n: com }) : '') + (st ? ' ' + worksText('works.ms.stars', 'Star logger, Day {n}.', { n: st }) : '') + (gr ? ' ' + worksText('works.ms.grade', 'Fault-finder grade: {grade}.', { grade: worksText('works.grade.' + gr, ['', 'Fault-finder', 'Senior fault-finder', 'Master fault-finder'][gr]), n: ff[1] }) : '') };
}
// ---- the device's Works app: Training, Work log, Tools; other sections add tabs with worksTabAdd (24k: Fault notes and
// the Chief's notes): worksTabAdd({ id, title, order, view() -> [blocks], act?(verb, arg), badge?() -> number }); the
// app's act passes any verb but 'tab' to the tab on show (else to the first tab with an act that takes it); badges add up ----
var WORKS_TAB = 'training';
var WORKS_TABS;                                         // var, so worksTabAdd works from anywhere in the file (24k may load first)
function worksTabAdd(def) {
  if (!def || typeof def.id !== 'string' || typeof def.view !== 'function') return false;
  if (!WORKS_TABS) WORKS_TABS = [];
  const i = WORKS_TABS.findIndex(x => x.id === def.id); if (i >= 0) WORKS_TABS.splice(i, 1);
  WORKS_TABS.push({ order: 50, title: def.id, ...def }); WORKS_TABS.sort((a, b) => a.order - b.order || (a.id < b.id ? -1 : 1));
  if (typeof deviceRefresh === 'function') try { deviceRefresh(); } catch (e) { /* the device isn't up yet */ }
  return true;
}
function worksLogTitle(e) {                              // a log row's title, from the job if it's still on the list, else its id
  const j = (SHIP.jobs || []).find(x => x.id === e[0]);
  try { if (j) { const [title] = jobCard(j), verb = { service: 'Service', repair: 'Repair', overhaul: 'Overhaul' }[j.kind]; return verb ? verb + ': ' + title : title; } } catch (x) { /* gone */ }
  const mid = String(e[0]).replace(/^reserve\d+:/, '').split('@')[0], m = typeof machineById === 'function' ? machineById(mid) : null;
  const verb = { service: 'Service', repair: 'Repair', overhaul: 'Overhaul' }[e[3]];
  if (m && MACHINE_KINDS[m.kind]) return (verb ? verb + ': ' : '') + MACHINE_KINDS[m.kind].name;
  return e[3] ? e[3].charAt(0).toUpperCase() + e[3].slice(1) : 'A job';
}
worksTabAdd({ id: 'training', title: worksText('works.tab.training', 'Training'), order: 10, view() {
  const W = SHIP.works, B = [], say = (text, mark) => B.push({ kind: 'text', text, mark });
  say(worksRankTitle(W) + '. Works reputation: ' + (W ? worksBandWord() : worksText('works.band.new', 'New')) + '.', 'hot');
  say(worksText('works.training.next', 'What\'s next:') + ' ' + worksNext());
  const rows = [];
  if (worksShadowDone(W)) rows.push({ text: mechName('job').replace(/^job$/, 'The job loop'), sub: 'with Zeke Torres, Day 1' });
  if (W) for (const r of CAREER_LADDER) if (W.tr[r.id] !== undefined) rows.push({ text: mechName(r.id), sub: 'Day ' + W.tr[r.id] });
  say('Trained', 'head'); if (rows.length) B.push({ kind: 'list', rows }); else say(worksText('works.training.none', 'Nothing yet. Torres will start you off.'));
  const kinds = W ? Object.keys(W.sk).filter(k => W.sk[k] >= 5 && MACHINE_KINDS[k]) : [];
  if (kinds.length) { say('What you know', 'head'); B.push({ kind: 'list', rows: kinds.map(k => { const machine = MACHINE_KINDS[k].name.replace(/^./, x => x.toUpperCase()).replace(/([^s])$/, '$1s');
    return { text: worksText('works.skill.row', '{machine}: {skill}.', { machine, skill: skillWord(k) }) }; }) }); }
  return B;
} });
worksTabAdd({ id: 'log', title: worksText('works.tab.log', 'Work log'), order: 20, view() {
  const W = SHIP.works, L = W ? W.log.slice().reverse() : [];
  if (!L.length) return [{ kind: 'text', text: worksText('works.log.none', 'Your jobs will be listed here as you turn them in.') }];
  return [{ kind: 'list', rows: L.map(e => ({ text: worksLogTitle(e), sub: ['Day ' + e[1]].concat(e[2] & 1 ? [worksText('works.log.found', 'found by you')] : [], e[2] & 2 ? [worksText('works.log.first', 'right first time')] : [],
    e[2] & 4 ? [worksText('works.log.clever', 'a clever fix')] : [], e[4] ? [worksText('works.log.noticed', '{name} noticed', { name: worksFirst(e[4]) })] : []).join(' · ') })) }];
} });
worksTabAdd({ id: 'tools', title: worksText('works.tab.tools', 'Tools'), order: 30, view() {
  const W = SHIP.works, ts = W ? Object.keys(W.tools) : [];
  if (!ts.length) return [{ kind: 'text', text: worksText('works.tools.none', 'No tools of your own yet. They come with the work that needs them.') }];
  return [{ kind: 'list', rows: ts.map(k => ({ text: toolName(k).replace(/^the /, '').replace(/^./, x => x.toUpperCase()), sub: (WORK_TOOLS[k].bench ? 'In the machine shop' : 'In your locker') + ' · ' + (TOOL_SLOW_SAY[k] ? toolStateWord(k) : toolWord(W.tools[k][1])) + ' · since Day ' + W.tools[k][0] })) }];
} });
function worksView() {
  const T = WORKS_TABS || [], tab = T.find(x => x.id === WORKS_TAB) || T[0], B = [{ kind: 'buttons', items: T.map(x => { const n = worksBadge(x); return { label: x.title + (n ? ' (' + n + ')' : ''), on: x === tab, action: { app: 'works', do: 'tab', arg: x.id } }; }) }];
  let more = []; try { more = tab ? tab.view() || [] : []; } catch (e) { more = [{ kind: 'text', text: 'Nothing to show.' }]; }
  return { title: worksText('works.app.title', 'Works'), blocks: B.concat(more) };
}
function worksTabShow(id) { if ((WORKS_TABS || []).some(x => x.id === id)) WORKS_TAB = id; if (typeof deviceShow === 'function') deviceShow('works'); }
function worksBadge(x) { try { const n = typeof x.badge === 'function' ? x.badge() : x.badge; return Number.isFinite(n) && n > 0 ? n : 0; } catch (e) { return 0; } }
if (typeof deviceApp === 'function') deviceApp({ id: 'works', title: worksText('works.app.title', 'Works'), short: 'Works', icon: 'wrench', order: 31, view: worksView, hidden: () => !SHIP.works,   // from Day 1's evening (nothing changes Days 0-1)
  badge: () => (WORKS_TABS || []).reduce((a, x) => a + worksBadge(x), 0) || null,
  act(verb, arg) { const T = WORKS_TABS || []; if (verb === 'tab') { if (T.some(x => x.id === arg)) WORKS_TAB = arg; return; }
    if (verb === 'open') { const id = arg && (arg.tab || arg.arg); if (T.some(x => x.id === id)) WORKS_TAB = id; return; }   // deviceDo({ app: 'works', tab }) opens on that tab
    const tab = T.find(x => x.id === WORKS_TAB); if (tab && tab.act) return tab.act(verb, arg);
    const any = T.find(x => x.act && /:/.test(verb) && verb.split(':')[0] === (x.verbs || x.id)) || null; if (any) return any.act(verb, arg); } });
// ---- the clock: worksCareerTick() from the main loop (section 12) each frame; it acts once a ship minute (the training)
// and once a ship hour (the ladder). After a skip or a sleep the ladder catches up (training needs you there). ----
const WORKS_TICK = { m: -1, h: -1 };
// sub-blocks' clocks (WORK_TICKS.push(f)): f(now, false) once a ship minute in play (from Day 1 17:00); after a skip or
// a sleep, f(t, true) once for each ship hour skipped
const WORK_TICKS = [];
function worksCareerTick(now = shipNow()) {   // (not worksTick: that's section 17's job board and cart docks)
  const m = Math.floor(now); if (m === WORKS_TICK.m) return; WORKS_TICK.m = m;
  if (!SHIP.works && now < WORKS_START) return;
  const h = Math.floor(now / 60); if (h !== WORKS_TICK.h) { WORKS_TICK.h = h; ladderTick(h); }
  trainTick(now);
  for (const f of WORK_TICKS) try { f(now, false); } catch (e) { console.error(e); }
  if (typeof caseTick === 'function') caseTick();       // 24k's head-scratchers (seat H)
}
SIM_ADVANCE.push((from, to) => { for (let h = Math.floor(from / 60) + 1; h <= Math.floor(to / 60); h++) { const t = h * 60, m = t % 1440; if (m >= WORKS_ASK[0] && m <= WORKS_SMALL) ladderTick(h); if (t >= WORKS_START) for (const f of WORK_TICKS) try { f(t, true); } catch (e) { console.error(e); } } WORKS_TICK.h = Math.floor(to / 60); });

// ---------------------------------------------------------------------
// 24a ROUNDS (M1, seat M1, 0.45.x; plans/mechanics/m1-rounds.html). Walk a route of 4-6 machines on one deck, look
// at each (a `look` step: stand a moment, read its sign, mark it fine / worn / something's off). A worn machine you
// mark worn or off, or a faulty-or-worse one you mark off or worn, gets its job "found by you" (section 17's
// machineFound): a quick service now instead of a repair later. Marking wrong costs nothing: a healthy one marked
// gets "Looks all right to me". Taught by Torres on Day 2 (ladder row m1: he looks at the first two, you watch; then
// you look at the rest of the route while he watches); from the next workday a morning round is on the board at
// 07:00, held for you to 11:00 (j.leave, so never against HOLD_MAX), then the crew's. The crew's own inspection round
// (CHORES.round) runs as before. Removable: without this block the ladder's m1 row never opens.
// Saved on the job: j.route (machine ids), j.marks ({ id: 'fine' | 'worn' | 'off' }). Nothing else.
// No R(): the route is schedU 860, the sign's wording schedU 861. Lines: content/works/step2.lines (round.*),
// signs.lines (sign.<kind>.<state>), Torres's train.m1.* (the stand-ins below are the writer's first lines).
const ROUND_DECKS = [4, 3, 5];                           // the decks take turns by day; the training round is Deck 4
const ROUND_AT = 420, ROUND_HELD = 120;                  // posted 07:00 on your workdays; held for you 120 minutes of the shift (to 11:00; 180 until the 09:00 shift, 0.44.15)
const ROUND_LOOK = 2;                                    // ship minutes at each machine (the crew's round: crew.mins)
const ROUND_MARKS = [['fine', 'Fine'], ['worn', 'Worn'], ['off', 'Something\'s off']];
const roundText = (key, fb, ctx = {}) => String(worksText(key, fb)).replace(/\{(\w+)\}/g, (x, k) => ctx[k] !== undefined ? ctx[k] : x);
// the machines a round can visit on a deck: at your tier, with a panel place, not the engine's
const roundPool = n => machineList().filter(m => m.deck === n && !m.stub && panelPlace(m.id) && jobTier({ machine: m.id }) <= playerTier() && !ENGINE_KINDS.has(m.kind));
function roundDeck(day, train) {                         // the deck by day (4, 3, 5), skipping one with fewer than 4 machines to look at
  if (train) return 4;
  for (let k = 0; k < ROUND_DECKS.length; k++) { const n = ROUND_DECKS[(day + k) % ROUND_DECKS.length]; if (roundPool(n).length >= 4) return n; }
  return 4;
}
// roundRoute(day, train) -> machine ids: 4-6 of the deck's machines, picked by the day, in walking order from the lift
function roundRoute(day, train) {
  const n = roundDeck(day, train), pool = roundPool(n), D = DECKS[n];
  const want = Math.min(pool.length, 4 + Math.floor(schedU(day, 0, 860) * 3));
  const pick = pool.slice().sort((a, b) => schedU(a.seed, day, 860) - schedU(b.seed, day, 860) || (a.id < b.id ? -1 : 1)).slice(0, want);
  const out = roundWalk(pick, D);
  const w = train ? out.findIndex(id => machineById(id).kind === 'washer') : -1;   // Torres starts at a washer (his first line is about one)
  if (w > 0) out.unshift(out.splice(w, 1)[0]);
  return out;
}
function roundWalk(ms, D) {                              // machines in walking order: the nearest next, from the lift (0.45.16: roundRoute's own, shared with stage 2's picks)
  const pick = ms.slice(), out = []; let at = D && D.lift ? D.lift : pick.length ? pick[0].panel : [0, 0];
  while (pick.length) {
    let k = 0; pick.forEach((m, i) => { const a = Math.hypot(m.panel[0] - at[0], m.panel[1] - at[1]), b = Math.hypot(pick[k].panel[0] - at[0], pick[k].panel[1] - at[1]); if (a < b || a === b && m.id < pick[k].id) k = i; });
    out.push(pick[k].id); at = pick[k].panel; pick.splice(k, 1);
  }
  return out;
}
const roundState = id => { const s = SHIP.machines[id]; return s ? s.state : 'healthy'; };
const roundSignState = st => st === 'healthy' || st === 'worn' ? st : 'faulty';
const ROUND_SIGN = {                                     // stand-ins until the writer's signs.lines are baked (theirs win)
  healthy: 'Clean and quiet. Nothing to see.', worn: 'Something\'s a little tired about it.', faulty: 'Not right at all: it\'s labouring.' };
// roundSign(id, day): what you see at the machine, from its kind and its state now; the same machine in the same state the same day says the same
function roundSign(id, day) {
  const m = machineById(id), st = roundSignState(roundState(id)), L = typeof LINES !== 'undefined' && m && LINES['sign.' + m.kind + '.' + st];
  if (Array.isArray(L) && L.length) { const e = L[Math.floor(schedU(machSeed(id), day, 861) * L.length) % L.length]; if (e && typeof e.text === 'string') return e.text; }
  return ROUND_SIGN[st];
}
// a mark is right: worn on a worn machine, worn or off on a faulty-or-worse one
const roundRight = (pick, st) => st !== 'healthy' && (pick === 'off' || pick === 'worn');
// a machine's job found now: section 17's machineFound(id, by) -> { id, fresh } | null (fresh: it wasn't on the board
// before, so it's found by `by`: j.foundBy and simNote('found')). Nothing without it
const roundFound = (id, by) => typeof machineFound === 'function' ? machineFound(id, by) : null;
// your mark at stop k: found by you on a right mark, a word from the teacher on a training round. Returns the words
// for after the step (section 15 shows a kind's stepDone text before "Done here", 0.28.73), or null
function roundMark(j, k, pick) {
  const id = (j.route || [])[k]; if (!id || !ROUND_MARKS.some(x => x[0] === pick)) return null;
  const st = roundState(id), right = roundRight(pick, st), first = !(j.marks && j.marks[id]);
  (j.marks = j.marks || {})[id] = pick; if (!j.train && typeof roundLast === 'function') roundLast()[id] = worksDay(shipNow());   // stage 2's "last looked" (0.45.16)
  const f = right && first ? roundFound(id, 'you') : null;
  let said = null;
  if (f && f.fresh) { worksXp(1); said = roundText('round.found', 'Found by you: {machine}.', { machine: machineLabel(machineById(id)).split(',')[0] }); }
  const c = SHIP.works && SHIP.works.cur, by = j.train && c && c.id === j.train ? c.by : null;
  const say = right ? ['mark.right', 'Good eye.'] : st === 'healthy' && pick !== 'fine' ? ['mark.okay', 'Looks all right to me. Better safe, though.'] : st !== 'healthy' && pick === 'fine' ? ['mark.wrong', 'Mm. Listen again.'] : null;
  if (say && by) worksTeach('m1', by, say[0], say[1]);
  else if (say && st === 'healthy' && pick !== 'fine') said = roundText('round.okay', 'Looks all right to me.');
  return said;
}
// a round finished: someone else's (the teacher's, the crew's) finds what's worn on it; yours counts as a use
function roundDone(j, t, by) {
  if (by && by !== 'you') for (const id of j.route || []) if (roundState(id) !== 'healthy') roundFound(id, by);
  if (by === 'you') { worksUse('m1'); try { toast('Round', roundText('round.done', 'Round done. Anything worn is on the board, found by you.')); } catch (e) { /* no UI */ } }
  if (by === 'you' && !j.train && typeof roundPicks === 'function' && roundPicks() && (j.route || []).filter(id => roundState(id) === 'worn' && roundRight((j.marks || {})[id], 'worn')).length >= 2) {   // stage 2: two or more worn found (0.45.16)
    worksSayAll('torres-zeke', worksVoice('torres-zeke', 'round.two') || ['Two worn on one round? You\'ve got the eye now.']); worksSideXp(1, 'round');
  }
}
// a round job on the list: { kind: 'rounds', route, marks, deck, room, title }. o.train: the training's, held for you
// (reserved slot): since 0.45.9 (playtest 2) the whole route is yours after Torres's talk (o.yours); a teacher's round
// (no o.yours) would take the first two stops. Else the morning round
function roundJob(day, at, o = {}) {
  const all = roundRoute(day, !!o.train), route = o.train ? (o.yours ? all : all.slice(0, 2)) : all;
  if (route.length < (o.train ? 1 : 4)) return null;
  const m0 = machineById(route[0]), n = m0.deck, t = (day - 1) * 1440 + at;
  const j = jobMake('rounds', { id: 'round' + (o.slot ? o.slot : '') + '-d' + n + '@' + Math.floor(t / 60) + (o.yours ? 'y' : ''), deck: n, room: m0.room, h: Math.floor(t / 60),
    title: o.train ? roundText('round.title.first', 'Your first round, Deck {deck}', { deck: n }) : roundText('round.title', 'Morning round, Deck {deck}', { deck: n }), route, marks: {}, ...(o.slot ? { reserved: o.slot, until: (day - 1) * 1440 + DAY_SHIFT[1] } : { leave: ROUND_HELD }) });
  j.posted = j.found = t; j.shareSeen = true;            // held to 11:00 as the page says: never shared out early (section 17's shareOut)
  return j;
}
if (typeof jobKindAdd === 'function') jobKindAdd('rounds', { tier: 1, junior: false, work: 0, hold: 'datapad',   // the round clipboard in your hand (15b's ixHold, 0.28.73)
  post(h, jobs) {                                        // workdays at 07:00 once trained (not the day you're trained): one round, held for you to 11:00
    const d = Math.floor(h / 24) + 1, W = SHIP.works;
    if ((h % 24 + 24) % 24 !== ROUND_AT / 60 || !W || W.tr.m1 === undefined || W.tr.m1 >= d || !playerShiftOn(d)) return;
    if (jobs.some(j => j.kind === 'rounds' && !j.reserved && j.status !== 'done' && Math.floor(j.posted / 1440) + 1 === d)) return;
    const j = roundJob(d, ROUND_AT); if (j) jobs.push(j);
  },
  stops: j => (j.route || []).map(id => { const m = machineById(id); return { deck: m.deck, placeId: panelPlace(id), mins: ROUND_LOOK, tag: 'look', how: 'look',
    opts: { secs: 4, text: roundSign(id, worksDay(shipNow())), marks: ROUND_MARKS.map(([x, label]) => ({ id: x, label: roundText('round.mark.' + x, label) })) } }; }),
  stepDone: (j, k, res) => { const said = roundMark(j, k, res && res.pick); return typeof roundDoor === 'function' ? roundDoor(j, k, said) : said; },   // stage 3: the doorway (0.45.16)
  done: roundDone,
  crew: { can: p => !!p.work && p.work.place === 'work:works', mins: 25 } });
// the ladder row (m1): the training's two rounds are this block's own (reserve), held in the teacher's slot. Only
// with section 17's job kinds in the build (without them a round can't be posted, so the row never opens)
if (typeof jobKindAdd === 'function') WORK_MECH.m1 = {
  at: () => 625,                                         // Torres's ask after the 10:30 tea (24 core books the meeting from 10:35; the page)
  reserve(d, at, slot, o = {}) {
    const j = roundJob(d, at, { train: o.train || 'm1', yours: !!o.yours, slot }); if (!j) return null;
    SHIP.jobs = SHIP.jobs.filter(x => !(x.reserved === slot && heldForYou(x) && !x.claimedBy));
    SHIP.jobs.push(j); if (typeof MACH_REV !== 'undefined') MACH_REV++;
    return j.id;
  },
  watch: 10,                                             // ship minutes watching Torres look at his two (before 0.45.9)
  self: true,                                            // playtest 2, item 1 (0.45.9): Torres explains at the meeting, then your first round is on the board; the arrow and green tips walk you through it
};
// stages 2 and 3 (0.45.16, E6; step4-stages). Stage 2 (row m1's stage 1, after 5 rounds): taking a morning round, the
// clipboard lists the deck's machines, the longest unlooked first, with "last looked" days (W2's round.last /
// round.last.never; SHIP.works.side.round.last = { machine id: ship day }, kept by your marks); you pick 4 to 6 (j.pick,
// then j.route in walking order; refused before 4: the day's route stays). Two or more worn ones found on a round of
// yours: Torres's round.two and +1 through worksSideXp. Stage 3 (the scanner: stage 2 and 5 rounds): at a room's first
// machine one look reads every machine in that room (round.doorway; the route's marked as they are, their stops done;
// the room's others too, 0.45.18; the unhealthy found by you), for one scan's charge (toolWear('scanner', 4)). The training round is neither
const roundLast = () => { const S = worksSide(); if (!S) return {}; const r = S.round && typeof S.round === 'object' && !Array.isArray(S.round) ? S.round : (S.round = {}); return r.last && typeof r.last === 'object' && !Array.isArray(r.last) ? r.last : (r.last = {}); };
const roundPicks = () => !!SHIP.works && worksStage('m1') >= 1;
const roundDoorway = () => !!SHIP.works && worksStage('m1') >= 2 && (SHIP.works.use.m1 || 0) >= 5 && typeof toolState === 'function' && !!toolState('scanner');
function roundLastText(id, d) {
  const L = roundLast(), n = Number.isFinite(L[id]) ? d - L[id] : null;
  return n === null ? worksText('round.last.never', 'not looked at yet') : n <= 0 ? 'looked at today' : roundText('round.last', 'last looked {n} days ago', { n }).replace(/\b1 days\b/, '1 day');
}
function roundPicked(j) {                                // your picks as the route, in walking order (before any look)
  if ((j.pick || []).length >= 4 && !(j.stepsDone || []).length) {
    j.route = roundWalk(j.pick.map(id => machineById(id)).filter(Boolean), DECKS[j.deck]); j.marks = {};
    j.stops = kindStops(j).map(plainStop); if (typeof MACH_REV !== 'undefined') MACH_REV++;
  }
  delete j.pick;
}
function roundPickAsk(j) {                               // one machine at a time; from the fourth, "That's my round"
  const d = worksDay(shipNow()), L = roundLast(), pool = roundPool(j.deck).map(m => m.id).filter(id => !j.pick.includes(id));
  if (j.pick.length >= 6 || !pool.length) return roundPicked(j);
  pool.sort((a, b) => (Number.isFinite(L[a]) ? L[a] : -1) - (Number.isFinite(L[b]) ? L[b] : -1) || (a < b ? -1 : 1));
  const choices = pool.map(id => machineLabel(machineById(id)).split(',')[0] + ' · ' + roundLastText(id, d)).concat(j.pick.length >= 4 ? ['That\'s my round'] : []);
  const shown = deviceChoose({ title: 'Round', text: j.pick.length ? 'And next?' : roundText('round.pick.some', 'Pick a handful to look at today: four to six.'), choices }, i => {
    if (!pool[i]) return roundPicked(j);
    j.pick.push(pool[i]); if (typeof simTimeout === 'function') simTimeout(() => roundPickAsk(j), 400); else roundPickAsk(j);
  });
  if (!shown) roundPicked(j);                            // the device busy: what you've picked if it's four, else the day's route
}
if (WORK_MECH.m1) WORK_TICKS.push((now, skip) => {
  if (skip || typeof myJob !== 'function') return; const j = myJob();
  if (!j || j.kind !== 'rounds' || j.reserved || j.train || j.picked || !roundPicks() || (j.stepsDone || []).length) return;
  j.picked = true; j.pick = []; roundPickAsk(j);
});
// stage 3: the look at stop k reads the rest of its room from the doorway; returns the words after the step
function roundDoor(j, k, said) {
  const id = (j.route || [])[k], m = id && machineById(id); if (!m || j.reserved || j.train || !roundDoorway()) return said;
  const done = new Set(j.stepsDone || []), ks = j.route.map((x, i) => i).filter(i => i !== k && !done.has(i) && !(j.marks || {})[j.route[i]] && machineById(j.route[i]) && machineById(j.route[i]).deck === m.deck && machineById(j.route[i]).room === m.room);
  const off = roundPool(m.deck).filter(x => x.room === m.room && !j.route.includes(x.id)).map(x => x.id).sort();   // the room's machines off the route: read too (the page: "every machine in it"; lead 17, 0.45.18)
  if (!ks.length && !off.length) return said;
  const out = said ? [said] : [], pickOf = x => { const st = roundState(x); return st === 'healthy' ? 'fine' : st === 'worn' ? 'worn' : 'off'; };
  const line = (x, pick) => roundText('round.doorway', 'From the doorway: {machine}, {word}.', { machine: machineLabel(machineById(x)).split(',')[0], word: roundText('round.mark.' + pick, ROUND_MARKS.find(r => r[0] === pick)[1]).toLowerCase() });
  for (const i of ks) {
    const x = j.route[i], pick = pickOf(x), f = roundMark(j, i, pick);
    (j.res || (j.res = {}))[i] = { pick, door: true }; done.add(i);
    out.push(line(x, pick)); if (f) out.push(f);
  }
  for (const x of off) {                                 // no stop of the round's: read, last looked, the unhealthy found by you
    const pick = pickOf(x); out.push(line(x, pick)); roundLast()[x] = worksDay(shipNow());
    const f = pick !== 'fine' ? roundFound(x, 'you') : null;
    if (f && f.fresh) { worksXp(1); out.push(roundText('round.found', 'Found by you: {machine}.', { machine: machineLabel(machineById(x)).split(',')[0] })); }
  }
  j.stepsDone = [...done].sort((a, b) => a - b); toolWear('scanner', 4);
  return out.join(' ');
}
// the training round's walk-through (0.45.9, for U's arrow and green tips: the writer's tip.round.<step>, {machine}):
// roundTrainStep() -> null, or { step: 'take' | 'go' | 'look' | 'mark' | 'next' | 'done', job, machine (its name), deck, place }
// take: on the board, not yours yet; go / next: walk to the first / next machine; look: at it (tap to look, or looking);
// mark: looked, choose a mark; done: every stop marked, turn it in at the board
function roundTrainStep() {
  const c = SHIP.works && SHIP.works.cur; if (!c || c.id !== 'm1' || c.st !== 'do') return null;
  const j = SHIP.jobs.find(x => x.id === c.j && x.kind === 'rounds'); if (!j || j.status === 'done') return null;
  const base = { job: j.id };
  if (j.claimedBy !== 'you') return { ...base, step: 'take' };
  const st = jobStops(j), k = st.findIndex(s => !s.done); if (k < 0 || j.workDone) return { ...base, step: 'done' };
  const id = j.route[k], m = machineById(id), pid = panelPlace(id), name = machineLabel(m).split(',')[0];
  const at = { ...base, machine: name, deck: m.deck, place: pid }, w = typeof wsFind === 'function' ? wsFind(j.id, k) : null;
  if (typeof ACT !== 'undefined' && ACT && ACT.kind === 'workStep' && ACT.o.job === j.id) return { ...at, step: 'look' };
  if (w && w.done > 0) return { ...at, step: 'mark' };
  let near = false;
  try { const s = PLACE_OF.has(pid) && placeSpot(pid), p = player.obj.position; near = !!s && deckDef && deckDef.num === m.deck && Math.hypot(s.x - p.x, s.z - p.z) < 2.5; } catch (e) { near = false; }
  return { ...at, step: near ? 'look' : k ? 'next' : 'go' };
}
// while Torres leads (the teacher's round), his words at the machines once you're with him: the writer's train.m1.lead.look
let ROUND_TAUGHT = null;
if (WORK_MECH.m1) WORK_TICKS.push((now, skip) => {
  const c = SHIP.works && SHIP.works.cur; if (skip || !c || c.id !== 'm1' || c.st !== 'watch' || ROUND_TAUGHT === c.j) return;
  const j = SHIP.jobs.find(x => x.id === c.j); if (!j || !trainNear(trainSpot(j))) return;
  ROUND_TAUGHT = c.j; worksTeach('m1', c.by, 'lead.look', ['Hear that? End of the spin. Bearing\'s going. Worn.', 'Low, even hum. That\'s a happy one. Fine.']);
});

// ---------------------------------------------------------------------
// 24b YOUR WORK UNIFORM (M2, seat M1, 0.45.x; plans/mechanics/m2-uniform.html). From Day 8, oily jobs make your uniform
// grubby: each oily repair or overhaul you turn in adds .35 grime, an oily service .2, anything else .05 (section 15c's
// clothes keep the number and say grubby from .6, so two oily repairs; a change at your wardrobe clears it, a shower
// doesn't: clothesGrime and uniformState are 15c's, read typeof-guarded). The first oily job turned in on Day 8 or later
// sets flag works.oily, which opens the small ladder row m2: Torres's word (the writer's train.m2.torres-zeke meeting,
// played by 24 core when you're trained; his two lines in a bubble or by Mail if it isn't baked). Grubby, you look a shade
// duller: the player's body only, swapped to a second cached copy of the characters' material (no new material per
// frame, no new draw calls). Not yet: stage 2 (a worn washer's service held for you while your wash runs).
const OILY = new Set(['oven', 'range', 'extractor', 'galleyplant', 'cartdock', 'lift', 'pump', 'heatpump', 'fan', 'irrigation']);
const GRIME_FROM = 8;                                    // oily jobs count from Day 8 (the ladder's m2 day)
const GRIME_ADD = { oily: { repair: .35, overhaul: .35, service: .2 }, other: .05 };
const grimeFor = (kind, machineKind) => OILY.has(machineKind) ? GRIME_ADD.oily[kind] || GRIME_ADD.other : GRIME_ADD.other;
onSim('job', n => {                                      // your job turned in: grime, and the first oily one opens m2
  if (!n || n.step !== 'turnin' || worksDay(n.t) < GRIME_FROM) return;
  const j = (SHIP.jobs || []).find(x => x.id === n.id), m = n.machine && typeof machineById === 'function' ? machineById(n.machine) : null, kind = n.job || (j && j.kind) || '';
  if (typeof clothesGrime === 'function') clothesGrime(grimeFor(kind, m && m.kind));
  if (m && OILY.has(m.kind) && typeof flagSet === 'function' && !(typeof flag === 'function' && flag('works.oily'))) flagSet('works.oily', worksDay(n.t));
});
if (typeof uniformState === 'function') WORK_MECH.m2 = {
  open(row, d) {                                         // Torres's word, and trained (a small row's first use)
    const sc = MEETING_SCRIPTS['train.m2.torres-zeke'] || MEETING_SCRIPTS['train.m2'];
    if (!sc || sc.stub) {
      const L = ['You\'ve got half a machine on you. Change before tea. Calder notices.', 'Shower won\'t shift it. Wardrobe will.'];
      const near = (typeof DECK_CREW !== 'undefined' ? DECK_CREW : []).some(x => x.p && x.p.id === 'torres-zeke');
      if (near) worksSayAll('torres-zeke', L);
      else if (typeof mailSend === 'function') mailSend({ at: shipNow(), from: worksName('torres-zeke'), subject: 'Your uniform', body: L.join(' ') });
    }
    worksUse('m2');
  },
};
// the look: grubby, the player's body meshes use a second copy of the characters' material, a shade darker (col())
let UNIFORM_MAT = null;
function playerUniformTint(k) {
  if (typeof player === 'undefined' || !player || !player.rig || typeof CHAR_MAT === 'undefined') return false;
  if (!UNIFORM_MAT) { UNIFORM_MAT = CHAR_MAT.clone(); UNIFORM_MAT.color = col('#e1ded9'); }   // about 12% darker, a touch warmer grey
  const to = k ? UNIFORM_MAT : CHAR_MAT, props = new Set(player.propMeshes || []); let n = 0;
  player.rig.root.traverse(o => { if (o.isMesh && !props.has(o) && (o.material === CHAR_MAT || o.material === UNIFORM_MAT) && o.material !== to) { o.material = to; n++; } });
  return n;
}
WORK_TICKS.push((now, skip) => {                         // once a ship minute: the tint follows uniformState (cheap when nothing changed)
  if (skip || typeof uniformState !== 'function') return;
  const want = uniformState() === 'grubby' && !PLAYER_SPEC.kit ? 1 : 0;   // rec kit is clean (0.81.0)
  if (want || UNIFORM_MAT) playerUniformTint(want);
});

// ---------------------------------------------------------------------
// 24c DRILL AND INSPECTION (M3, seat M1, 0.45.x; plans/mechanics/m3-drill-inspection.html). Two small ladder rows
// fixed in the week. The drill (m3d, Wednesday 15:00): a toast at 14:50, your drill job by the week's kind (fire: the
// extinguisher from its bracket, stand by the hatch; pressure: dog the bulkhead door, four turns; power: stand by the
// breaker cabinet), the all-clear at 15:15, Calder's word on the time. The inspection (m3i, Thursday 06:30): a clean
// uniform, your bed made, your locker tidy; the duty officer's nod or remark (in person if you're in the bunk room,
// else Mail at 07:00); +1 reputation each attended (the rows' xp, through worksUse). Never a fail. Places from the
// Pillar 5 deck architect (DECKS[5].drill, DECKS[4].inspect). Hash key 864 (the duty officer's rota). No R().
const DRILL_KINDS = ['fire', 'pressure', 'power'];
const drillKind = d => DRILL_KINDS[Math.floor((d - 1) / 7) % 3];   // week 1 (Day 3) fire, then pressure, then power
const DRILL_AT = 900, DRILL_TOAST = 890, DRILL_END = 915;      // 15:00, the toast at 14:50, the all-clear at 15:15
const INSPECT_AT = 390, INSPECT_MAIL = 420, BED_FROM = 330;     // 06:30 the walk, 07:00 the Mail if you weren't there; the bed from 05:30
// the duty officer: Calder on your first, else an officer on shift that day by the week's rota (key 864)
function inspectOfficer(d) {
  const W = SHIP.works; if (!W || W.use.m3i === undefined) return 'calder';
  const os = schedPeople().filter(p => OFFICER_RANKS.has(p.rank) && p.rank !== 'captain' && p.rank !== 'xo' && occOnShift(p.id, d)).map(p => p.id).sort();
  return os.length ? os[Math.floor(schedU(machSeed('inspect'), Math.floor((d - 1) / 7), 864) * os.length) % os.length] : 'calder';
}
// the three items now: { uniform, bed, locker } (true is right). A clean uniform: changed today (0.60.7's wardrobe) and
// not grubby (M2, section 15's uniformState, from Day 8); the bed made this morning; the locker tidy (15b's lockerTidy)
function inspectItems(d = SHIP.time.day) {
  const C = typeof SHIP.clothes === 'object' && SHIP.clothes, P = SHIP.player || {};
  const grubby = typeof uniformState === 'function' && /grub|dirt/.test(String(uniformState()));
  return { uniform: !!C && C.changed === d && !grubby, bed: 'bedMade' in P ? P.bedMade === d : true, locker: typeof lockerTidy === 'function' ? !!lockerTidy() : true };   // (no bed or locker action in the build yet: counted as right)
}
const inspectResult = it => { const bad = ['uniform', 'bed', 'locker'].filter(k => !it[k]); return bad.length === 0 ? 'nod' : bad.length === 1 ? bad[0] : bad.length === 2 ? 'two' : 'none'; };
const INSPECT_SAY = { nod: 'Good. Carry on.', uniform: 'Uniform\'s seen better days, cadet.', bed: 'Make the bed before you go, please.', locker: 'Locker. Things go in it, not on it.',
  two: 'Two out of three. Let\'s get to three next week.', none: 'Uniform, bed and locker. All three. Next Thursday, please.' };
const INSPECT_MAILS = { nod: 'Your berth was in good order this morning. Nothing to add.', uniform: 'Your berth was tidy. Next time, a clean uniform, please.',
  bed: 'Your locker and uniform were fine. Next time, make the bed, please.', locker: 'Uniform and bed were fine. Next time, a tidy locker, please.',
  two: 'Two of the three weren\'t right this morning. Uniform, bed, locker: all three next week.', none: 'Your berth wasn\'t ready this morning. Uniform, bed, locker: next Thursday, please.' };
// you're at your berth for the walk: in your own bunk room on Deck 4
function inspectHere() {
  try { const bed = placeById(playerBed()); if (!bed || !deckDef || deckDef.num !== bed.deck || !player) return false; const [c, r] = player.here(); return roomAt(c, r) === bed.room; } catch (e) { return false; }
}
// the walk: Thursdays at 06:30 on your workdays while you're a junior, from the day the row (m3i) opens. In the bunk
// room: the duty officer's line now; else Mail at 07:00 (and after a sleep through it). Turning up, or all three right
// while you were out, counts as the inspection attended (worksUse: the row's reputation, and the first is the training)
function inspectDue(d) {
  const W = SHIP.works;
  return !!W && W.rank === 'junior' && weekday(d) === 3 && playerShiftOn(d) && worksOpened(W).has('m3i') && !simNotes('inspection', (d - 1) * 1440 - 1).some(n => n.day === d);
}
function inspectRun(d, here) {
  const it = inspectItems(d), res = inspectResult(it), by = inspectOfficer(d);
  simNote('inspection', { day: d, uniform: it.uniform, bed: it.bed, locker: it.locker, result: res, by, here });
  if (here) worksSay(by, worksText('inspect.' + res, INSPECT_SAY[res]));
  else if (typeof mailSend === 'function') mailSend({ at: (d - 1) * 1440 + INSPECT_MAIL, from: worksName(by), subject: worksText('inspect.mail.subject', 'This morning\'s inspection'), body: worksText('inspect.mail.' + res, INSPECT_MAILS[res]) });
  if (here || res === 'nod') worksUse('m3i');
  return res;
}
WORK_TICKS.push((now, skip) => {
  const d = worksDay(now), m = now - (d - 1) * 1440;
  if (m < INSPECT_AT || m >= INSPECT_AT + 60 || !inspectDue(d)) return;
  if (!skip && m < INSPECT_MAIL && inspectHere()) inspectRun(d, true);
  else if (skip || m >= INSPECT_MAIL - 1) inspectRun(d, false);
});
WORK_MECH.m3i = {};                                      // a small row: opens on Thursday, trained by the first inspection
// the drill job: a side job (beside any board job you hold, never the crew's), posted for you at 14:50 on Wednesdays
// you're on shift as a junior, from the day the row (m3d) opens; yours at once (claimed for you), over at 15:15 whatever
// the state (the all-clear). Places: DECKS[5].drill (the Pillar 5 deck architect's); a kind's stops left out till they're in
const drillPlace = k => { const D = DECKS[5] && DECKS[5].drill, id = D && D[k]; return id && placeById(id) ? id : null; };
function drillStops(kind) {
  const st = (k, mins, tag, more) => ({ deck: 5, placeId: drillPlace(k), mins, tag, ...more });
  if (kind === 'fire') return [st('ext', 1, 'take', { opts: { text: 'You lift the extinguisher off its bracket.' } }), st('hatch', 10, 'stand', { opts: { text: 'You stand by the hatch with it.' } }), st('ext', 1, 'putback', { opts: { text: 'Back on its bracket.' } })];
  if (kind === 'pressure') return [st('door', 1, 'dog', { how: 'turn', opts: { label: 'The bulkhead wheel', v: 0, min: 0, max: 4, by: 1, onTurn: v => v >= 4 ? 'Dogged tight.' : ['Stiff.', 'A quarter turn.', 'Half way.', 'Nearly there.'][v] || null, ok: v => v >= 4 } }), st('door', 10, 'stand', { opts: { text: 'You stand by the door.' } })];
  return [st('breaker', 2, 'reserve', { opts: { text: 'The junior wing to reserve.' } }), st('breaker', 8, 'stand', { opts: { text: 'Back to main.' } })];
}
const drillDue = d => { const W = SHIP.works; return !!W && !!WORK_MECH.m3d && W.rank === 'junior' && weekday(d) === 2 && playerShiftOn(d) && (worksOpened(W).has('m3d') || W.tr.m3d !== undefined); };
const drillJobOf = d => SHIP.jobs.find(x => x.kind === 'drill' && Math.floor(x.posted / 1440) + 1 === d) || null;
if (typeof jobKindAdd === 'function') jobKindAdd('drill', { tier: 1, work: 0, side: true, text: 'The drill',
  hold: j => { if (j.drill !== 'fire') return null; const st = jobStops(j), a = st.find(x => x.step === 'take'), b = st.find(x => x.step === 'putback'); return a && a.done && !(b && b.done) ? 'extinguisher' : null; },   // the extinguisher in your hand (8b's prop, this block's)
  post(h, jobs) {                                        // Wednesdays at 14:00's hour, found at 14:50
    const d = Math.floor(h / 24) + 1; if ((h % 24 + 24) % 24 !== 14 || !drillDue(d) || jobs.some(x => x.kind === 'drill' && Math.floor(x.posted / 1440) + 1 === d)) return;
    const kind = drillKind(d), t = (d - 1) * 1440 + DRILL_TOAST, j = jobMake('drill', { id: 'drill-' + kind + '@' + d, deck: 5, room: 'w', h, title: worksText('drill.kind.' + kind, kind.charAt(0).toUpperCase() + kind.slice(1) + ' drill'),
      drill: kind, reserved: true, until: (d - 1) * 1440 + DRILL_END });
    j.posted = j.found = t; j.claimedBy = 'you'; j.status = 'claimed'; j.start = t; jobs.push(j);   // yours from the start: never on the board for anyone to take (BM5's trial: claimJob took it beside a board job)
  },
  stops: j => drillStops(j.drill).filter(x => x.placeId),
  stepDone(j, k, res, t) {
    if (j.reached === undefined) j.reached = Math.round((t !== undefined ? t : shipNow()) - (Math.floor(j.posted / 1440) * 1440 + DRILL_AT));   // minutes from 15:00 to your first stop
    const tag = (jobStops(j)[k] || {}).step;
    if (tag === 'take' && typeof drillExtShow === 'function') drillExtShow(false);
    if (tag === 'putback' && typeof drillExtShow === 'function') drillExtShow(true);
  },
  done(j, t, by) { if (by === 'you') j.drilled = true; },
  crew: { can: () => false, mins: 0 } });
// Calder's word on the time (her lines drill.time.fast | ok | slow): words, never the number unless she says it
function drillTimeWord(mins) { return mins === undefined || mins === null ? 'slow' : mins <= 3 ? 'fast' : mins <= 6 ? 'ok' : 'slow'; }
function drillSay(key, fb) { try { const l = typeof lineFor === 'function' ? lineFor('calder', key) : null; worksSay('calder', l && l.text || fb); } catch (e) { worksSay('calder', fb); } }
WORK_TICKS.push((now, skip) => {
  const d = worksDay(now), m = now - (d - 1) * 1440;
  for (const x of SHIP.jobs) if (x.kind === 'drill' && x.status !== 'done' && now >= x.until && Math.floor(x.posted / 1440) + 1 !== d) drillClose(x, now, true);   // an earlier day's drill after a jump: closed quietly
  const j = weekday(d) === 2 ? drillJobOf(d) : null; if (!j) return;
  if (!skip && m >= DRILL_TOAST && m < DRILL_END && !j.told) {   // 14:50: the toast, the job yours, the arrow
    j.told = true;
    try { toast(worksName('calder'), worksText('drill.toast', 'Drill in ten minutes. Muster at the Works bay.') + ' ' + worksText('drill.job.' + j.drill, '')); } catch (e) { /* no UI */ }
    if (typeof setGoal === 'function') setGoal({ deck: 5, room: 'w', label: worksText('drill.kind.' + j.drill, 'Drill') + ', 15:00' });
  }
  if (m >= DRILL_END && j.status !== 'done') drillClose(j, now, skip);
});
// the all-clear: the drill is over whatever the state (no lapse, no abandoned job); quiet when skipped past or from an earlier day
function drillClose(j, now, quiet) {
  {
    const did = !!j.workDone, mins = j.reached;
    j.status = 'done'; j.doneAt = now; j.doneBy = did ? 'you' : null; if (typeof MACH_REV !== 'undefined') MACH_REV++;
    if (typeof drillExtShow === 'function') drillExtShow(true);
    simNote('drill', { kind: j.drill, mins: mins === undefined ? null : mins, you: did });
    if (did || mins !== undefined) worksUse('m3d');      // you turned up: the row's reputation (and the first is the training)
    if (!quiet) { try { toast(worksName('calder'), worksText('drill.allclear', 'All clear. Drill over.')); } catch (e) { /* no UI */ } const w = drillTimeWord(mins);
      drillSay('drill.time.' + w, { fast: 'Two minutes ten. Better.', ok: 'Three minutes. Fine. We\'ll do better.', slow: 'Four and a half minutes. We\'ll talk about it.' }[w]); }
  }
}
// the device's Calendar names the week's drill (its fixed Wednesday line, section 19's DEV_WEEK, read as a getter: no edit there)
// and, on the Friday tea after a quick drill you turned up to, Calder says so (Pillar 4's tradition: works-tea, or new-hands-tea)
function drillCalendar() {
  const e = typeof DEV_WEEK !== 'undefined' && DEV_WEEK[2] && DEV_WEEK[2].find(x => x.at === DRILL_AT); if (!e || Object.getOwnPropertyDescriptor(e, 'title').get) return;
  const plain = e.title;
  Object.defineProperty(e, 'title', { configurable: true, enumerable: true, get() {
    const d0 = SHIP.time.day, d = d0 + ((2 - weekday(d0)) + 7) % 7;   // this week's Wednesday, today or next
    return drillDue(d) ? worksText('drill.cal', 'Drill at 15:00: {drill}').replace('{drill}', worksText('drill.kind.' + drillKind(d), drillKind(d).replace(/^./, x => x.toUpperCase()) + ' drill')) + '. Muster at the Works bay' : plain; } });
}
const DRILL_TEA = /^(works-tea|new-hands-tea)$/;
WORK_TICKS.push((now, skip) => {
  const d = worksDay(now), m = now - (d - 1) * 1440; if (skip || weekday(d) !== 4 || m < 1125 || m > 1170 || !WORK_MECH.m3d) return;
  const tea = typeof eventsOn === 'function' && eventsOn(d).find(e => DRILL_TEA.test(e.id)); if (!tea || typeof deckDef === 'undefined' || !deckDef || deckDef.num !== 5) return;
  if (simNotes('drillTea', now - 2880).some(n => n.day === d)) return;
  const dr = simNotes('drill', now - 3 * 1440).filter(n => n.you).pop(); if (!dr || drillTimeWord(dr.mins) !== 'fast') return;
  simNote('drillTea', { day: d }); drillSay('drill.tea', 'Wednesday\'s drill was quick. Well done, all of you.');
});
if (typeof jobKindAdd === 'function' && drillPlace('ext') && drillPlace('hatch') && drillPlace('door') && drillPlace('breaker')) { WORK_MECH.m3d = {}; drillCalendar(); }   // a small row: opens on Wednesday, trained by the first drill; only with the drill's places in the build

// ---------------------------------------------------------------------
// 24d HAULING (M4, seat M1, 0.45.x; plans/mechanics/m4-hauling.html). The Wednesday delivery has a few crates for the
// rest of the ship (section 17's SHIP.manifest = [{ id, dest, n }], 0.33.50: linen, medical, store, galley, bridge).
// A manifest run takes them: a hover cart from the Cart bay, load each crate in the hold (a tap, a minute each), ride
// the lift, drop each where it goes, the cart back. A junior job, at most CART_CRATES a run (more: a second run).
// Yara Esposito teaches it on Day 3 once the delivery's in (ladder row m4: she takes the cart and loads the first crate
// while you watch; you take the rest). Once trained, each Wednesday's run is held for you to 16:00 after the unload
// (or from 13:00), then the crew's; before that the crew do it. Saved on the job: j.crates ([{ id, dest }]), j.got
// (crate ids loaded). Hash keys: section 17's 866-867 (the manifest, the misplaced part). Stage 2 (choose the order,
// 0.45.13) and stage 3 (the Thursday stocktake, 0.45.15, with SHIP.misplaced) below; 1026 the stocktake's short shelf.
const HAUL_FROM = 780, HAUL_UNTIL = 960, HAUL_TRAIN = 660;   // posted by 13:00 (after the unload), held to 16:00; Yara's meeting from 11:00
const haulDay = d => weekday(d) === DELIVERY.day + (typeof deliveryLate === 'function' ? deliveryLate(d) : 0);
const haulDock = () => CART_AT.find(id => placeById(id)) || null;
const haulLoadAt = () => HOLD_AT.find(id => placeById(id)) || null;
const haulName = c => c.part ? String(c.id).replace(/^./, x => x.toUpperCase()) : worksText('haul.crate.' + c.id, ({ laundry: 'Linen', medical: 'Medical supplies', infirmary: 'Medical supplies', store: 'Crew store stock', galley: 'Dry goods', bridge: 'Bridge spares' })[c.id] || 'A crate');
const haulWhere = c => { const p = placeById(c.dest); return p ? (roomName(p.deck, p.room) || 'the room') + ', ' + deckIn(p.deck) : 'its stop'; };
// a run's crates from what's left of the manifest: up to CART_CRATES, by deck from the hold upward (4, 3, 2, 1): fewest rides
function haulCrates(max = CART_CRATES) {
  const out = []; for (const c of SHIP.manifest || []) for (let i = 0; i < (c.n || 0); i++) out.push({ id: c.id, dest: c.dest });
  const dk = c => (placeById(c.dest) || { deck: 0 }).deck;
  return out.sort((a, b) => dk(b) - dk(a) || (a.id < b.id ? -1 : 1)).slice(0, max);
}
const haulOpen = () => SHIP.jobs.some(j => j.kind === 'haul' && !j.src && j.status !== 'done');   // (a parts run, j.src, isn't the manifest's)
function haulJob(t, crates, o = {}) {
  const j = jobMake('haul', { id: 'haul' + (o.slot || '') + '@' + Math.floor(t / 60) + (o.yours ? 'y' : ''), deck: 5, room: 'r', h: Math.floor(t / 60),
    title: roundText('haul.title', 'Manifest run: {n} crates', { n: crates.length }).replace(/: 1 crates$/, ': 1 crate'), crates, got: [],
    ...(o.slot ? { reserved: o.slot, until: Math.floor(t / 1440) * 1440 + DAY_SHIFT[1] } : o.crew ? { released: true } : { leave: Math.max(30, HAUL_UNTIL - Math.max(t % 1440, DAY_SHIFT[0])) }) });
  j.posted = j.found = t; j.shareSeen = true;            // held for you as the page says: never shared out to the crew early (section 17's shareOut)
  return j;
}
// the stops: the cart, a load per crate, a drop per crate (unless o.only: the teacher's run is the cart and the first load), the cart back
function haulStops(j) {
  const dock = haulDock(), hold = haulLoadAt(), cs = (j.crates || []).slice(), out = [];
  if (!dock || !hold) return out;
  const from = c => c.part ? (typeof shelfOf === 'function' && shelfOf(c.id) && placeById(shelfOf(c.id)) ? shelfOf(c.id) : FETCH_AT[0]) : hold;   // a parts run (manifestRun): from its shelf in main storage
  out.push({ deck: 5, placeId: dock, mins: 2, tag: 'cart', hold: 'cart', opts: { text: 'You take a hover cart from its dock.' } });
  cs.forEach(c => out.push({ deck: 5, placeId: from(c), mins: 1, tag: 'load', hold: 'cartfull', crate: c.key || c.id, opts: { text: haulName(c) + ' for ' + haulWhere(c) + ': on the cart.' } }));
  if (j.only !== 'load') {
    if (Array.isArray(j.order) && j.order.length === cs.length) cs.sort((a, b) => j.order.indexOf(a.key || a.id) - j.order.indexOf(b.key || b.id));   // stage 2: your order (cs is a copy below)
    cs.forEach(c => { const p = placeById(c.dest); if (p) out.push({ deck: p.deck, placeId: c.dest, mins: 2, tag: 'deliver', hold: 'cartfull', crate: c.key || c.id, opts: { text: haulName(c) + ' delivered.' } }); });
    out.push({ deck: 5, placeId: dock, mins: 2, tag: 'return', hold: 'cart', opts: { text: 'The cart back on its dock.' } });
  }
  return out;
}
function haulTake(j, id) {                               // a crate off the hold's stack onto this run's cart (once); a part from its shelf (manifestRun)
  if (!id || (j.got || []).includes(id)) return false;
  (j.got = j.got || []).push(id); const c = (j.crates || []).find(x => (x.key || x.id) === id);
  if (c && c.part) { if (typeof takePart === 'function' && !takePart(c.id)) (j.empty = j.empty || []).push(id); } else if (typeof manifestTake === 'function') manifestTake(id);
  return true;
}
if (typeof jobKindAdd === 'function' && typeof haulOn === 'function') jobKindAdd('haul', { tier: 1, junior: true, work: 0, text: 'Manifest run',
  hold: j => { const st = jobStops(j), last = st.reduce((a, s, k) => s.step === 'deliver' ? k : a, -1), first = st.findIndex(s => s.step === 'load');
    return first >= 0 && st[first].done && !(last >= 0 && st[last].done) ? 'cartfull' : 'cart'; },
  post(h, jobs) {                                        // delivery days: once the unload's done (or from 13:00), the manifest's run
    const d = Math.floor(h / 24) + 1, m = (h % 24 + 24) % 24 * 60, W = SHIP.works;
    if (!haulDay(d) || m < DELIVERY.hour * 60 + 60 || m > DAY_SHIFT[1] || !(SHIP.manifest || []).length || jobs.some(j => j.kind === 'haul' && !j.src && j.status !== 'done')) return;
    const unloading = jobs.some(j => j.kind === 'restock' && j.cargo === 'stores' && j.status !== 'done');
    if (unloading && m < HAUL_FROM) return;
    if (W && W.cur && W.cur.id === 'm4' && W.cur.d === d) return;   // Yara's training run has them today
    const crates = haulCrates(); if (!crates.length) return;
    jobs.push(haulJob(h * 60, crates, { crew: !(W && W.tr.m4 !== undefined) || playerRank() !== 'junior' && !haulFree(d) }));   // an officer at stage 2 keeps it to 16:00 (D3)
  },
  stops: haulStops,
  stepDone(j, k, res, t) {
    const st = haulStops(j), s = st[k]; if (!s) return null;
    const c = (j.crates || []).find(x => (x.key || x.id) === s.crate);
    if (s.tag === 'load') { haulTake(j, s.crate); return c ? ((j.empty || []).includes(s.crate) ? 'No ' + c.id + ' on the shelf.' : haulName(c) + ' on the cart.') : null; }
    if (s.tag === 'deliver' && c) {
      simNote('haul', { stop: c.dest, id: c.id });
      if (j.src && !j.delivered && st.every((x, i) => x.tag !== 'deliver' || i === k || (j.stepsDone || []).includes(i))) {   // a parts run: all there
        j.delivered = t; simNote('manifestRun', { job: j.id, for: j.for || null, to: c.dest, parts: (j.crates || []).filter(x => !(j.empty || []).includes(x.key || x.id)).map(x => x.id) });   // what really came (an empty shelf's part didn't, 0.45.17)
      }
      return haulName(c) + ' delivered to ' + haulWhere(c) + '.';
    }
    return null;
  },
  done(j, t, by) {                                       // the crew's run takes what it hadn't loaded (Yara's load-only run leaves hers on the manifest: you deliver it); yours is a use of m4
    if (j.only !== 'load') for (const c of j.crates || []) haulTake(j, c.key || c.id);
    if (by === 'you' && j.only !== 'load') { if (Array.isArray(j.order)) haulTidy(j); worksUse('m4'); return; }
  },
  crew: { can: p => !!p.work && p.work.place === 'work:works', mins: j => 15 + 10 * (j.crates || []).length } });
// stage 2 (0.45.13; step4-stages and D3's answers): after 2 runs, from Day 10, the delivery stops are yours to order:
// taking a manifest run with crates for two or more stops, you pick them in turn (j.order, the crate keys; before any
// delivery). "A tidy run" (W2's haul.tidy) when your deck changes are the fewest possible; as an officer +1 (worksSideXp).
// After promotion the run stays the crew's, but once you're at stage 2 it's held for you to 16:00 (haulFree)
const haulFree = d => !!SHIP.works && worksStage('m4') >= 1 && d >= 10;
const haulDeck = c => (placeById(c.dest) || { deck: 5 }).deck;
function haulTidy(j) {
  const ds = (j.order || []).map(k => (j.crates || []).find(c => (c.key || c.id) === k)).filter(Boolean).map(haulDeck);
  let moves = 0, at = 5; for (const d of ds) { if (d !== at) moves++; at = d; }
  const best = new Set(ds.filter(d => d !== 5)).size; if (moves > best) return false;
  try { toast('Manifest run', worksText('haul.tidy', 'A tidy run.')); } catch (e) { /* no UI */ }
  if (SHIP.works && SHIP.works.rank !== 'junior') worksSideXp(1, 'haul');
  simNote('haulTidy', { job: j.id, moves }); return true;
}
function haulOrderAsk(j, got = []) {                     // pick the next stop until all are placed; Cancel keeps the rest as they are. The picks build up
  const cs = (j.crates || []).filter(c => !got.includes(c.key || c.id));   // apart and become j.order only when complete and nothing's delivered yet: the load
  const set = o => { if (!jobStops(j).some(s => s.step === 'deliver' && s.done)) j.order = o; };   // stops never move, the deliver stops only before the first (R5, 0.45.17)
  if (cs.length <= 1) return set(got.concat(cs.map(c => c.key || c.id)));
  const shown = deviceChoose({ title: 'Manifest run', text: got.length ? 'And next?' : 'Which stop first? Fewer lift rides makes a tidy run.', choices: cs.map(c => haulName(c) + ' · ' + haulWhere(c)) }, i => {
    if (!cs[i]) return set(got.concat(cs.map(c => c.key || c.id)));
    const next = got.concat([cs[i].key || cs[i].id]); if (typeof simTimeout === 'function') simTimeout(() => haulOrderAsk(j, next), 400); else haulOrderAsk(j, next);
  });
  if (!shown && got.length) set(got.concat(cs.map(c => c.key || c.id)));
}
if (typeof jobKindAdd === 'function' && typeof haulOn === 'function') WORK_TICKS.push((now, skip) => {
  if (skip || typeof myJob !== 'function') return; const j = myJob();
  if (!j || j.kind !== 'haul' || j.src || j.only || j.orderAsked || !haulFree(worksDay(now))) return;
  const st = jobStops(j); if (st.some(s => s.step === 'deliver' && s.done) || new Set((j.crates || []).map(c => c.dest)).size < 2) return;
  j.orderAsked = true; haulOrderAsk(j);
});
// manifestRun(list, to, o) -> job id | null (Step 4, 0.45.12; E2's 24h team parts call it): a run of parts (names, up to
// CART_CRATES) from their shelves in main storage to `to` (a place id, or a machine id: its panel), the cart there and back,
// as a 'haul' job (j.src 'stores') held for you only (reserved slot MANIFEST_SLOT, never the crew's) from o.at (default now)
// to o.until (default the shift's end), then withdrawn quietly if it isn't delivered. o.title, o.for (the asker's id).
// Delivered: j.delivered and simNote('manifestRun', { job, for, to, parts }); manifestRunDelivered(id), manifestRunEnd(id)
const MANIFEST_SLOT = 30;
function manifestRun(list, to, o = {}) {
  if (typeof jobMake !== 'function' || !JOB_KINDS.haul) return null;
  const parts = (Array.isArray(list) ? list : []).filter(p => typeof p === 'string' && p && !(p in STOCK && !(SHIP.stores[p] > 0))).slice(0, CART_CRATES);   // none on its shelf: not on the run (R5, 0.45.17)
  const m = typeof machineById === 'function' && to ? machineById(to) : null, dest = m ? panelPlace(m.id) : to;
  if (!parts.length || !dest || !placeById(dest) || !haulDock()) return null;
  const t = Number.isFinite(o.at) ? Math.floor(o.at) : Math.floor(shipNow()), until = Number.isFinite(o.until) ? o.until : Math.floor(t / 1440) * 1440 + DAY_SHIFT[1];
  const j = jobMake('haul', { id: 'parts' + (o.for ? '-' + String(o.for).replace(/[^a-z0-9-]/gi, '').slice(0, 30) : '') + '@' + t, deck: 5, room: 'r', h: Math.floor(t / 60),
    title: typeof o.title === 'string' ? o.title : roundText('haul.parts', 'Bring the parts: {parts}', { parts: parts.join(', ') }),
    crates: parts.map((p, i) => ({ id: p, dest, part: true, key: 'p' + i })), got: [], src: 'stores', ...(o.for ? { for: String(o.for) } : {}), reserved: MANIFEST_SLOT, until });
  j.posted = j.found = t; j.shareSeen = true;
  SHIP.jobs.push(j); if (typeof MACH_REV !== 'undefined') MACH_REV++;
  return j.id;
}
const manifestRunDelivered = id => !!(SHIP.jobs.find(x => x.id === id && x.src) || {}).delivered;
function manifestRunEnd(id, t = shipNow()) {             // withdrawn (not delivered): off the board, nothing more taken
  const j = SHIP.jobs.find(x => x.id === id && x.src && x.status !== 'done'); if (!j) return false;
  j.status = 'done'; j.doneAt = t; j.doneBy = null; if (SHIP.player && SHIP.player.work && SHIP.player.work.job === id) SHIP.player.work = null;
  if (typeof MACH_REV !== 'undefined') MACH_REV++; return true;
}
if (typeof jobKindAdd === 'function' && typeof haulOn === 'function') WORK_TICKS.push(now => {   // a parts run past its time: withdrawn
  for (const j of SHIP.jobs) if (j.kind === 'haul' && j.src && j.status !== 'done' && !j.delivered && now >= j.until) manifestRunEnd(j.id, now);
});
// stage 3, the stocktake (0.45.15, E6; step4-stages): Thursdays from Day 18, once you're an officer trained in hauling, a
// side job on the board at 13:30, held for you to 16:00 and then withdrawn (never the crew's): count each storage aisle
// (E3's 5-stock-1..4, a short hold each; W2's stock.count). One aisle is short of a part (schedU(week, 0..1, 1026),
// kept on the job: j.short = { aisle, part }): finding it (stock.short) moves what isn't there to the hold's order
// (SHIP.stores down, SHIP.hold up: section 17 posts the restock run, stock.job) and pays +1 through worksSideXp; the
// rest read stock.fine. Thursday's misplaced part (SHIP.misplaced) on an aisle you count goes back (stock.wrong,
// misplacedFix). Saved: SHIP.works.side.stock = { week, found } (read defensively).
const STOCK_AT = 810, STOCK_UNTIL = 960, STOCK_FROM = 18, STOCK_SLOT = 31, STOCK_SHORT = 2;
const STOCK_AISLES = FETCH_AT.map(id => SHELF_NAME[id]);   // the aisles of 5-parts-1..4 (section 17's shelf names), in order
const stockSpots = () => [1, 2, 3, 4].map(k => '5-stock-' + k).filter(id => placeById(id));
function stockShortFor(d) {                              // the week's short aisle and part (a part that's on its shelf), or null
  const wk = Math.floor((d - 1) / 7), a = Math.floor(STOCK_AISLES.length * schedU(wk, 0, 1026)) % STOCK_AISLES.length;
  const parts = ((placeById(FETCH_AT[a]) || {}).stock || []).filter(k => k in STOCK && SHIP.stores[k] > 0);
  return parts.length ? { aisle: a, part: parts[Math.floor(parts.length * schedU(wk, 1, 1026)) % parts.length] } : null;
}
function stockFound(j) {                                 // the short aisle found: the missing ones go on the hold's order; +1
  const s = j.short; if (!s || j.shortFound) return false; j.shortFound = true;
  const n = Math.min(STOCK_SHORT, SHIP.stores[s.part] || 0);
  if (n > 0) { SHIP.stores[s.part] -= n; SHIP.hold[s.part] = (SHIP.hold[s.part] || 0) + n; if (typeof MACH_REV !== 'undefined') MACH_REV++; }
  worksSideXp(1, 'stock'); simNote('stocktake', { job: j.id, aisle: s.aisle, part: s.part, n });
  try { toast('Stocktake', roundText('stock.job', 'Restock: {shelf}', { shelf: STOCK_AISLES[s.aisle] })); } catch (e) { /* no UI */ }
  return true;
}
if (typeof jobKindAdd === 'function' && typeof haulOn === 'function' && JOB_KINDS.haul && jobKindAdd('stocktake', { tier: 1, work: 0, side: true, text: 'Stocktake', hold: 'datapad',
  post(h, jobs) {                                        // Thursdays 13:00's hour, found at 13:30
    const d = Math.floor(h / 24) + 1, W = SHIP.works;
    if ((h % 24 + 24) % 24 !== 13 || weekday(d) !== 3 || d < STOCK_FROM || !W || W.tr.m4 === undefined || playerRank() === 'junior' || !stockSpots().length) return;
    if (jobs.some(x => x.kind === 'stocktake' && Math.floor(x.posted / 1440) + 1 === d)) return;
    const t = (d - 1) * 1440 + STOCK_AT, j = jobMake('stocktake', { id: 'stocktake@' + d, deck: 5, room: 'r', h, title: roundText('stock.title', 'Stocktake'),
      short: stockShortFor(d), reserved: STOCK_SLOT, until: (d - 1) * 1440 + STOCK_UNTIL, xp: 0 });   // xp 0: the +1 is the find's (stockFound)
    j.posted = j.found = t; j.shareSeen = true; jobs.push(j);
  },
  stops: j => stockSpots().map(id => { const a = +id.slice(-1) - 1; return { deck: 5, placeId: id, mins: 2, tag: 'count', opts: { text: roundText('stock.count', '{shelf}: count what\'s there.', { shelf: STOCK_AISLES[a] }) } }; }),
  stepDone(j, k) {
    const id = (kindStops(j)[k] || {}).placeId || '', a = +String(id).slice(-1) - 1, shelf = STOCK_AISLES[a]; if (!shelf) return null;
    const out = [], M = SHIP.misplaced;
    if (j.short && j.short.aisle === a && stockFound(j)) out.push(roundText('stock.short', '{shelf} is short of {part}.', { shelf, part: j.short.part }));
    else out.push(roundText('stock.fine', '{shelf}: all present.', { shelf }));
    if (M && M.on === FETCH_AT[a] && typeof misplacedFix === 'function') { out.push(roundText('stock.wrong', 'A {part} on the {shelf} shelf? That\'s not where it lives.', { part: M.part, shelf }), worksText('stock.moved', 'Back on its own shelf.')); misplacedFix(); }
    return out.join(' ');
  },
  done(j, t, by) { if (by !== 'you') return; const S = worksSide(); if (S) S.stock = { week: Math.floor(Math.floor(j.posted / 1440) / 7), found: !!j.shortFound }; },
  crew: { can: () => false, mins: 20 } })) {
  WORKS_SIDE_KINDS.add('stocktake');
  WORK_TICKS.push(stockWithdraw);
}
function stockWithdraw(now) {                            // 16:00 and not taken: withdrawn quietly
  for (const j of SHIP.jobs) if (j.kind === 'stocktake' && j.status === 'open' && !j.claimedBy && now >= j.until) { j.status = 'done'; j.doneAt = now; j.doneBy = null; if (typeof MACH_REV !== 'undefined') MACH_REV++; }
}
// the ladder row (m4): Yara's run is the cart and the first crate (you watch); yours is the rest, in the same slot
if (typeof jobKindAdd === 'function' && typeof haulOn === 'function' && JOB_KINDS.haul) WORK_MECH.m4 = {
  at: d => HAUL_TRAIN,                                   // after the 10:00 delivery's unload
  reserve(d, at, slot, o = {}) {
    const t = (d - 1) * 1440 + at, crates = haulCrates(o.yours ? CART_CRATES : 1); if (!crates.length || !haulDock() || !haulLoadAt()) return null;
    SHIP.jobs = SHIP.jobs.filter(x => !(x.reserved === slot && heldForYou(x) && !x.claimedBy));
    for (const x of SHIP.jobs) if (x.kind === 'haul' && x.status === 'open' && !x.claimedBy && !x.reserved) { x.status = 'done'; x.doneAt = t; x.doneBy = null; }   // an ordinary run waiting: this one stands for it
    const j = haulJob(t, crates, { slot, yours: !!o.yours }); if (!o.yours) j.only = 'load';
    SHIP.jobs.push(j); if (typeof MACH_REV !== 'undefined') MACH_REV++;
    return j.id;
  },
  watch: 10,
};

// =====================================================================
// 24m. TOOL UPKEEP (M11, seat E1, 0.45.x; plans/mechanics/m11-tool-upkeep.html on claude/p5-design)
// From Day 12 (the m11 row, an officer's) your tools wear with use (24 core's toolWear: the scanner 4 a scan, the pipe
// kit 5 a trace, the logger 3 a use) and you look after them at your bench in the Works bay (E3's 5-bench-you, "Your
// bench"): recharge the scanner (a wait: on charge for 5 ship minutes, you needn't stay), clean and re-seal the pipe kit
// (2 minutes there), check the logger (1). Each puts the tool back to "Charged". Never blocks a job. Your first upkeep is
// the lesson (24 core's small row: the Works officer on shift's train.m11.<id>; Torres is off Thursdays and Fridays). A
// week with your tools kept up (all charged after an upkeep): Works reputation +1, once a week (worksSideXp). Stage 3,
// after 4 upkeeps: the team's rack (the tool wall, E3's 5-tool-rack) once a week, 3 minutes there; Calder notices (her
// `work` line upkeep.rack). Saved: SHIP.works.side.upkeep = { done, kept, rack, charge } (read defensively). Only with
// E3's places in the build. Nothing drawn, no keys.
// =====================================================================
const TOOL_UPKEEP = { scanner: { wait: true, mins: 5, label: 'Recharge the scanner' }, pipekit: { mins: 2, label: 'Clean and re-seal the pipe kit' }, logger: { mins: 1, label: 'Check the logger' }, tester: { mins: 1, label: 'Check the conduit tester' } }, RACK_MINS = 3;   // the tester (m15) too, so "all charged" counts it (R5, 0.45.17)
const benchOn = () => (DECKS[5].places || []).some(p => p.id === '5-bench-you');   // (not placeById at load: its index is built once)
const benchWeek = (t = shipNow()) => Math.floor((worksDay(t) - 1) / 7);
const benchTools = () => Object.keys(TOOL_UPKEEP).filter(hasTool);
function benchData() {
  const S = worksSide(); if (!S) return null;
  const u = S.upkeep && typeof S.upkeep === 'object' && !Array.isArray(S.upkeep) ? S.upkeep : (S.upkeep = {});
  if (!Number.isInteger(u.done) || u.done < 0) u.done = 0;
  if (u.charge && !(Number.isFinite(u.charge.at) && hasTool('scanner'))) delete u.charge;
  return u;
}
Object.assign(PLAYER_ACTS, { benchHold: { mins: 2, pose: 'work', title: 'Your bench' } });
function benchDone(id, t = shipNow(), quiet = false) {   // the tool back to charged; the week's +1 if they're all kept up
  const u = benchData(); if (!u || !hasTool(id)) return;
  SHIP.works.tools[id][1] = 0; u.done++;
  const wk = benchWeek(t);
  if (u.kept !== wk && benchTools().every(k => toolState(k) === 'charged')) { u.kept = wk; worksSideXp(1, 'upkeep'); }
  simNote('upkeep', { tool: id });
  if (!quiet) try { toast(toolName(id).replace(/^the /, '').replace(/^./, x => x.toUpperCase()), worksText('bench.done', 'Good as new. Well, good as yesterday.')); } catch (e) { /* no UI */ }
  if (typeof MACH_REV !== 'undefined') MACH_REV++;
}
function benchStart(id) {                                // you chose a tool at the bench
  const u = benchData(), U = TOOL_UPKEEP[id]; if (!u || !U || !hasTool(id)) return false;
  worksUse('m11');                                       // a use (the first: the lesson, 24 core's small-row training)
  if (U.wait) {
    u.charge = { at: shipNow() + U.mins };
    toast('Your bench', worksText('bench.charging', 'The scanner\'s on charge. Ready at {time}; no need to wait.', { time: hhmm(u.charge.at % 1440) }));
    return true;
  }
  actStart('benchHold', '5-bench-you', { title: 'Your bench' });
  if (ACT && ACT.kind === 'benchHold') { ACT.def.mins = U.mins; ACT.def.title = worksText('bench.' + id, U.label); ACT.def.onDone = () => benchDone(id); }
  return true;
}
function benchTap() {                                    // "Your bench": which tool to see to
  const u = benchData(), ts = benchTools(); if (!u || !ts.length || typeof deviceChoose !== 'function') return false;
  const label = k => worksText('bench.' + k, TOOL_UPKEEP[k].label) + ' · ' + (k === 'scanner' && u.charge ? worksText('bench.charging.now', 'on charge') : toolStateWord(k));
  const open = ts.filter(k => !(k === 'scanner' && u.charge));
  if (!open.length) { toast('Your bench', worksText('bench.charging', 'The scanner\'s on charge. Ready at {time}; no need to wait.', { time: hhmm(u.charge.at % 1440) })); return true; }
  return deviceChoose({ title: 'Your bench', text: ts.map(label).join('. ') + '.', choices: open.map(k => worksText('bench.' + k, TOOL_UPKEEP[k].label)) }, i => { if (open[i]) benchStart(open[i]); }) || false;
}
function rackTap() {                                     // the team's rack (stage 3): once a week
  const u = benchData(); if (!u || worksStage('m11') < 2 || u.rack === benchWeek() || !(DECKS[5].places || []).some(p => p.id === '5-tool-rack')) return false;
  actStart('benchHold', '5-tool-rack', { title: 'The tool wall' });
  if (ACT && ACT.kind === 'benchHold') { ACT.def.mins = RACK_MINS; ACT.def.title = worksText('bench.rack', 'The team\'s tools'); ACT.def.onDone = () => {
    const v = benchData(); if (!v) return; v.rack = benchWeek(); simNote('upkeep', { tool: 'rack' });
    worksSayAll('calder', worksVoice('calder', 'upkeep.rack') || [worksText('bench.rack.done', 'Rack\'s tidy. Someone\'s been busy.')]); }; }
  return true;
}
if (typeof jobKindAdd === 'function' && benchOn()) {
  WORK_MECH.m11 = { noJob: true };                       // a small row: trained at your first upkeep
  WORK_TICKS.push((now, skip) => {                       // the scanner's charge
    const u = SHIP.works && worksSide() && benchData(); if (!u || !u.charge || now < u.charge.at) return;
    delete u.charge; benchDone('scanner', now, skip);
  });
  if (typeof PLAYER_TAPS !== 'undefined') PLAYER_TAPS.unshift((it, at) => {
    if (!it || !SHIP.works || !worksOpened().has('m11') || typeof deckDef === 'undefined' || !deckDef || deckDef.num !== 5) return false;
    if (it.t === 'Your bench') return benchTap();
    if (it.t === 'Tool wall') return rackTap();
    return false;
  });
}

// =====================================================================
// 24n. THE LOGBOOK (M12, seat E1, 0.45.x; plans/mechanics/m12-logbook.html on claude/p5-design)
// From Day 12 (the m12 row; Calder teaches it the first time: "Officers write it down"): on a workday 16:30-17:30, at
// the Works bay terminal (E3's 5-works-terminal, by the notice board: tap the board), "Write the log": one of three
// summaries of your real shift (logChoices: what you fixed, what you found, what's still open, from 24 core's work log
// and the found notes; the writer's log.* parts joined with "; "; their order schedU(day, 0, 1012)). An open job you wrote
// up is finished 10% faster by whoever takes it next (j.logged: section 15's jobMins and section 17's crew minutes).
// Works reputation +1 an entry (one a day, worksSideXp). Calder reads it at your progress talks (logLast(n), her `work`
// line log.talk). Stage 2, after 5 entries: flag one machine for the night crew, who look at it at 22:00 (on paper: a
// worn or faulty one's open job is done by them, else found). Stage 3, after 10: P3 reads SHIP.works.side.log for clues
// (24k's line, E2's). Saved: SHIP.works.side.log = [{ day, pick, jobs, flag }], the last 30 (read defensively).
// =====================================================================
const LOGBOOK = { from: 16 * 60 + 30, to: 17 * 60 + 30, keep: 30, bonus: .9, flagAt: 22 * 60 };
const logbookOn = () => (DECKS[5].places || []).some(p => p.id === '5-works-terminal');
function logbookData() {
  const S = worksSide(); if (!S) return null;
  if (!Array.isArray(S.log)) S.log = [];
  else if (S.log.some(e => !e || typeof e !== 'object' || !Number.isInteger(e.day) || typeof e.pick !== 'string')) S.log = S.log.filter(e => e && typeof e === 'object' && Number.isInteger(e.day) && typeof e.pick === 'string');
  if (S.log.length > LOGBOOK.keep) S.log.splice(0, S.log.length - LOGBOOK.keep);
  return S.log;
}
const logbookName = id => { const m = typeof machineById === 'function' && machineById(id); return m ? machineLabel(m).split(',')[0] : String(id); };
function logbookShows(j) {                               // what it does, in a few words, for log.found
  const m = j && j.machine && machineById(j.machine);
  try { const f = m && j.cause && typeof caseCauses === 'function' ? caseCauses(m).find(x => x.id === j.cause) : null; if (f && f.shows) return f.shows; } catch (e) { /* the plain words below */ }
  return m && SHIP.machines[m.id] && SHIP.machines[m.id].state === 'worn' ? 'is wearing' : 'is acting up';
}
// the shift's facts for day d: { fixed: [text], found: [[text, jobId, machine]], open: [[text, jobId, machine]] }
function logbookFacts(d) {
  const W = SHIP.works, t0 = (d - 1) * 1440, out = { fixed: [], found: [], open: [] }, seen = new Set();
  if (!W) return out;
  for (const e of W.log) {
    if (e[1] !== d) continue;
    const j = SHIP.jobs.find(x => x.id === e[0]), mid = j && j.machine || (String(e[0]).match(/^(\d-[a-z0-9-]+)@/) || [])[1];
    if (!mid || !machineById(mid)) continue;
    const part = j && Array.isArray(j.parts) && j.parts[0], kind = e[3] || (j && j.kind) || '';
    out.fixed.push(part && kind !== 'service' ? worksText('log.fixed', '{machine}: {part} replaced', { machine: logbookName(mid), part }) : worksText('log.serviced', '{machine} serviced', { machine: logbookName(mid) }));
  }
  const live = j => j && j.machine && j.status !== 'done';
  for (const n of simNotes('found', t0)) {
    if (n.by !== 'you' || n.t >= t0 + 1440 || seen.has(n.machine)) continue;
    const j = SHIP.jobs.find(x => x.machine === n.machine && live(x)); if (!j) continue;
    seen.add(n.machine); out.found.push([worksText('log.found', '{machine} {shows}, left for tomorrow', { machine: logbookName(n.machine), shows: logbookShows(j) }), j.id, n.machine]);
  }
  for (const j of SHIP.jobs) {
    if (!live(j) || seen.has(j.machine) || !(j.claimedBy === 'you' || j.foundBy === 'you')) continue;
    seen.add(j.machine); out.open.push([worksText('log.open', '{machine} still open', { machine: logbookName(j.machine) }), j.id, j.machine]);
  }
  return out;
}
// logChoices(day) -> three { text, jobs, machines }: fixed + found, fixed + open, found + open (three parts at most each)
function logChoices(d) {
  const F = logbookFacts(d), mk = (a, b) => {
    const parts = a.concat(b).slice(0, 3), txt = parts.map(p => Array.isArray(p) ? p[0] : p);
    return { text: txt.length ? txt.join('; ') : worksText('log.quiet', 'A quiet day. Nothing to report'), jobs: parts.filter(Array.isArray).map(p => p[1]), machines: parts.filter(Array.isArray).map(p => p[2]) };
  };
  const all = [mk(F.fixed, F.found), mk(F.fixed, F.open), mk(F.found, F.open)], k = Math.floor(schedU(d, 0, 1012) * 3) % 3;
  return all.slice(k).concat(all.slice(0, k));
}
const logLast = (n = 3) => { const L = SHIP.works && logbookData(); return L ? L.slice(-n).map(e => e.pick) : []; };
const logbookToday = d => (logbookData() || []).find(e => e.day === d) || null;
function logbookWrite(c, d = worksDay(shipNow())) {      // your entry: the handover bonus on its open jobs, the use, +1
  const L = logbookData(); if (!L || !c || logbookToday(d)) return null;
  const e = { day: d, pick: String(c.text).slice(0, 240), jobs: c.jobs.slice(0, 6), flag: null }; L.push(e); logbookData();
  for (const id of e.jobs) { const j = SHIP.jobs.find(x => x.id === id); if (j && j.status !== 'done') j.logged = d; }
  worksUse('m12'); worksSideXp(1, 'log'); simNote('logbook', { day: d, jobs: e.jobs.length });
  return e;
}
function logbookOpen() {                                 // "Write the log": the three, then (stage 2) a machine to flag
  const d = worksDay(shipNow()), cs = logChoices(d);
  return deviceChoose({ title: worksText('works.log.write', 'Write the log'), text: worksText('works.log.pick', 'Which one\'s your log for today?'), choices: cs.map(c => c.text) }, i => {
    const e = cs[i] && logbookWrite(cs[i], d); if (!e) return;
    toast('Works log', worksText('log.saved', 'Logged. Calder will read it. She reads everything.'));
    const ms = cs[i].machines.filter((m, k, a) => a.indexOf(m) === k);
    if (worksStage('m12') >= 1 && ms.length && typeof simTimeout === 'function') simTimeout(() => deviceChoose({ title: 'Works log', text: '', choices: ms.map(m => worksText('log.flag', 'Flag {machine} for the night crew', { machine: logbookName(m) })) }, k => {
      if (!ms[k]) return; e.flag = ms[k]; toast('Works log', worksText('log.flagged', 'Flagged. The night crew will look at 22:00.')); }), 600);
  }) || false;
}
const nightWorks = () => { try { const p = ROSTER.find(x => x.dept === 'works' && x.shift === 'night'); return p ? p.id : 'night crew'; } catch (e) { return 'night crew'; } };
function logbookTick(now, skip) {                        // 22:00: the night crew look at the flagged machine; Calder at your progress talk
  const L = SHIP.works && logbookData(); if (!L) return;
  const d = worksDay(now), e = L.find(x => x.day === d && x.flag && !x.looked);
  if (e && now % 1440 >= LOGBOOK.flagAt) {
    e.looked = true; const id = e.flag, st = SHIP.machines[id] && SHIP.machines[id].state, by = nightWorks();
    if (st === 'worn') {                                   // a worn one is serviced early (m12); never a faulty one, never a job held for you (R5, 0.45.14)
      const j = SHIP.jobs.find(x => x.machine === id && x.status !== 'done' && !x.claimedBy && !heldForYou(x));
      if (j && typeof jobFinish === 'function') jobFinish(j, now, by); else if (typeof machineFound === 'function') machineFound(id, by);
      if (typeof MACH_REV !== 'undefined') MACH_REV++;
    }
    simNote('logFlag', { machine: id, by, state: st || null });
  }
  const S = worksSide(), r = L.length && SHIP.occasions.find(x => x.id === 'progressTalk' && (x.met || x.status === 'kept') && Math.floor(x.at / 1440) + 1 === d);
  if (r && S.logTalk !== r.key && !skip) {
    S.logTalk = r.key; const last = L[L.length - 1], m = last.jobs.length ? (SHIP.jobs.find(x => x.id === last.jobs[0]) || {}).machine : null, name = m ? logbookName(m) : 'the washers';
    worksSayAll('calder', (worksVoice('calder', 'log.talk') || ['I read your log. {machine}: good catch.']).map(l => String(l).replace(/\{machine\}/g, name)));
  }
}
if (typeof jobKindAdd === 'function' && logbookOn()) {
  WORK_MECH.m12 = { noJob: true };                       // a small row: Calder's word at your first entry
  WORK_TICKS.push(logbookTick);
  if (typeof PLAYER_TAPS !== 'undefined') PLAYER_TAPS.unshift((it, at) => {
    if (!it || it.t !== 'Notice board' || !SHIP.works || !worksOpened().has('m12') || typeof deckDef === 'undefined' || !deckDef || deckDef.num !== 5) return false;
    const s = placeSpot('5-works-terminal'), d = worksDay(shipNow()), m = shipNow() % 1440;
    if (!s || !at || Math.hypot(s.x - at.x, s.z - at.z) > 3.5 || !playerShiftOn(d) || m < LOGBOOK.from || m >= LOGBOOK.to || logbookToday(d)) return false;
    return logbookOpen();
  });
}

// =====================================================================
// 24g. THE SCANNER (M7, seat H, 0.55.x; plans/mechanics/m7-scanner.html on claude/p5-design)
// Your first tool (Day 5, the ladder's m7 row). At a faulty machine's panel the look-over (section 15's) shows the
// scanner's panel when you have it and the job has a cause (section 17's j.cause): the machine's 3-5 parts with a
// reading each (a bar, a number and a word); you pick the part to fetch (scanPick). The readings are frozen on the
// job (j.scan) at the first look. A wrong pick costs a walk back: when you fit it, the machine says so, the part goes
// back on its shelf (Tier 1) and the job names the right part (scanFitted, through 24k's caseFitted). Nothing here
// calls R() or makes 3D objects. Hash keys 874 (a worn decoy or not), 875 (the readings; the training job's cause).
// =====================================================================
const SCAN_WORDS = [[25, 'failing'], [40, 'low'], [66, 'worn'], [101, 'good']];
const scanWord = v => (SCAN_WORDS.find(w => v < w[0]) || SCAN_WORDS[3])[1];
const scanHave = () => typeof hasTool === 'function' && hasTool('scanner');
const scanDay = j => Math.floor((j.posted || 0) / 1440) + 1;
// a job's machine by name ("Washer 2"), without the symptom section 17's job card may add after it
const caseMachName = j => { const m = j && j.machine && machineById(j.machine); if (!m) return jobCard(j)[0];
  if (typeof machineTitle === 'function') { try { const t = machineTitle(m.id); if (t) return t; } catch (e) { /* our own below */ } }   // section 17's (0.33.52)
  return MACHINE_KINDS[m.kind].name + (machineList().filter(x => x.kind === m.kind && x.deck === m.deck).length > 1 ? ' ' + m.id.split('-').pop() : ''); };
// a kind's parts as the scanner sees them: section 17's scanParts(kind), else the part causes in its fault table
function scanPartsOf(m) {
  if (typeof scanParts === 'function') { try { const p = scanParts(m.kind); if (Array.isArray(p) && p.length) return p; } catch (e) { /* the table's own */ } }
  const ps = [...new Set(caseCauses(m).filter(x => x.part).map(x => x.part))];
  return ps.length ? ps.slice(0, 5) : [MACHINE_KINDS[m.kind].part];
}
// the readings: [[part, value], ...], frozen on the job at the first look. The cause's part reads 12-35; the others
// 70-96, except (3 times in 10) one decoy with the same card and a different sign at 40-60, so what you see up close
// tells them apart (or, on Day 5's training case, fixed readings). On a head-scratcher's job every suspect's part reads 40-60. null if there's nothing to read (no
// scanner, no cause, no part cause)
function scanRead(jobId) {
  const j = SHIP.jobs.find(x => x.id === jobId); if (!j || !j.machine || !scanHave()) return null;
  if (j.scan) return j.scan;
  const cz = typeof caseOf === 'function' && caseOf(j); if (cz && CASE_KINDS[cz.kind] && CASE_KINDS[cz.kind].noScan) return null;   // P1: the scanner won't settle a line (24k, 0.55.14)
  const m = machineById(j.machine), f = m && caseCauses(m).find(x => x.id === j.cause); if (!f || !f.part) return null;
  const d = scanDay(j), seed = machSeed(m.id), parts = scanPartsOf(m); if (!parts.includes(f.part)) parts.unshift(f.part);
  const dec = caseCauses(m).filter(x => x.part && x.part !== f.part && x.shows === f.shows && x.sign !== f.sign).map(x => x.part);
  const worn = (dec.length && schedU(seed, d, 874) < .3 ? dec[Math.floor(schedU(seed, d, 875) * dec.length)] : null);
  // a head-scratcher (the designer, 1d87fc6): every suspect's part reads worn (40-60), whatever the cause, and the rest
  // good, so the scanner never gives the answer away; it isn't one of the case's clues
  const sus = j.case && typeof caseOf === 'function' && caseOf(j), sp = sus ? new Set(sus.sus.map(x => caseSus(sus, x).part).filter(x => x)) : null;
  const tr = sus && sus.train ? { [caseSus(sus, sus.cause).part]: 55 } : null;   // Day 5's training case: the cause never reads lowest (the designer), so the
  if (tr) sus.sus.filter(x => x !== sus.cause).forEach((x, i) => { tr[caseSus(sus, x).part] = [44, 49, 52][i] || 50; });   // first puzzle doesn't teach "pick the lowest bar"
  const val = (p, u) => tr && p in tr ? tr[p] : sp ? (sp.has(p) ? 40 + Math.round(u * 20) : 70 + Math.round(u * 26)) : p === f.part ? 12 + Math.round(u * 23) : p === worn ? 40 + Math.round(u * 20) : 70 + Math.round(u * 26);
  j.scan = parts.slice(0, 5).map((p, i) => [p, val(p, schedU(seed ^ Math.imul(i + 1, 40503), d, 875))]);
  if (typeof toolWear === 'function') toolWear('scanner', 4);   // M11: 4 of 100 a scan (E1, 0.45.7; in the hook register)
  MACH_REV++;
  return j.scan;
}
// the panel, as device blocks: one bar a part, then a Fetch button each (the job's case, if it has one, is called)
function scanView(jobId) {
  const j = SHIP.jobs.find(x => x.id === jobId), r = scanRead(jobId); if (!j || !r) return null;
  const m = machineById(j.machine), f = caseCauses(m).find(x => x.id === j.cause), name = caseMachName(j), room = (DECKS[m.deck].rooms[m.room] || {}).name;
  const B = [{ kind: 'text', text: 'Scanner · ' + name + (room ? ' (' + room + ')' : ''), mark: 'big' }, { kind: 'text', text: 'The job: ' + (f && f.shows || 'a fault') }];
  B.push({ kind: 'bars', items: r.map(([p, v]) => ({ label: p.replace(/^./, x => x.toUpperCase()) + ' · ' + scanWord(v), value: v, level: v < 40 ? 'low' : v < 66 ? 'mid' : '' })) });
  if (j.picked) B.push({ kind: 'text', text: 'Fetching: ' + j.picked + '.', mark: 'hot' });
  B.push({ kind: 'buttons', items: r.map(([p]) => ({ label: 'Fetch: ' + p, on: j.picked === p, action: { app: 'scanner', do: 'pick', arg: j.id + '|' + p } })) });
  return B;
}
// you pick the part to fetch: it goes on the job (or, on a head-scratcher, it's your call)
function scanPick(jobId, part) {
  const j = SHIP.jobs.find(x => x.id === jobId); if (!j || !j.scan || !j.scan.some(r => r[0] === part) || j.workDone) return false;
  const c = typeof caseOf === 'function' ? caseOf(j) : null;
  if (c) { const s = c.sus.find(x => caseSus(c, x).part === part); if (!s) return false; j.picked = part; return caseCall(c.id, s); }
  j.picked = part;
  if (!(typeof jobSetPart === 'function' && jobSetPart(j.id, part))) { j.parts = (j.parts || []).slice(); j.parts[0] = part; }
  j.stepsDone = (j.stepsDone || []).filter(k => k !== 0);   // the fetch again, for the part you picked
  MACH_REV++;
  return true;
}
// at the last stop (24k's caseFitted asks for jobs that aren't cases): a wrong pick keeps the machine as it was -> true
function scanFitted(j) {
  if (!j.scan || !j.picked) return false;
  const m = machineById(j.machine), f = caseCauses(m).find(x => x.id === j.cause); if (!f || !f.part) return false;
  if (j.picked === f.part) {
    j.rightFirst = !j.scanWrong;
    if (typeof simNote === 'function') simNote('scanned', { machine: j.machine, right: !j.scanWrong });
    if (typeof worksUse === 'function') worksUse('m7');
    return false;
  }
  const wrong = j.picked, shows = f.shows || 'acts up';
  if (!(CASE_SPENT.has(wrong) && jobTier(j) >= 2)) returnPart(wrong);   // Tier 1: back on its shelf unused
  const key = 'fault.still.' + m.kind + '.' + (caseCauses(m).find(x => x.part === wrong) || {}).id;
  const line = (typeof worksText === 'function' ? worksText(key, null) : null) || 'Fitted a new ' + wrong + '. Still ' + shows + ': it\'s the ' + f.part + '.';
  j.scanWrong = true; j.picked = f.part;
  if (!(typeof jobSetPart === 'function' && jobSetPart(j.id, f.part))) j.parts = [f.part];   // the job now names the right part
  j.stepsDone = []; j.touched = shipNow();
  if (typeof toast === 'function' && !SIM_AT) toast(caseMachName(j), line);
  return true;
}
const SCAN_UI = { job: null };
function scanOpen(jobId) {
  if (!scanRead(jobId)) return false; SCAN_UI.job = jobId;
  if (typeof caseTick === 'function') caseTick();       // Day 5: the reading on Washer 2 is where the teacher opens P3's case
  if (typeof deviceShow === 'function') deviceShow('scanner'); return true;
}
deviceApp({ id: 'scanner', title: 'Scanner', short: 'Scanner', icon: 'wrench', order: 33, hidden: () => true,   // opened by the look-over (scanOpen), never from the grid
  view: () => ({ title: 'Scanner', blocks: (SCAN_UI.job && scanView(SCAN_UI.job)) || [{ kind: 'text', text: 'Nothing to read. Look a faulty machine over at its panel.' }] }),
  act(verb, arg) { if (verb !== 'pick') return; const [id, p] = String(arg).split('|'); if (scanPick(id, p) && typeof toast === 'function') toast('Scanner', 'A ' + p + ' from main storage, Deck 5. Follow the marker.'); } });
// the training (the ladder's m7 row, 24 core's flow): the teacher's job, then yours, each a faulty Tier 1 machine on
// Deck 3 or 4 with a part cause, reserved (24 core's slot); yours comes with the scanner, so you read it yourself
function scanTrainMachine(d, not) {
  const ok = m => (m.deck === 3 || m.deck === 4) && !m.stub && panelPlace(m.id) && (m.tier || MACHINE_KINDS[m.kind].tier) <= 1 && caseCauses(m).some(x => x.part)
    && !not.has(m.id) && !SHIP.jobs.some(j => j.machine === m.id && j.status !== 'done');
  const all = machineList().filter(ok); if (!all.length) return null;
  return all[Math.floor(schedU(machSeed('m7'), d, 875) * all.length)];
}
const SCAN_TRAINED = new Set();                          // machines used for today's training (the teacher's first)
function scanTrainReserve(d, at, slot, o) {
    if (o && o.yours && typeof toolGive === 'function') toolGive('scanner');   // handed over at the board: yours to read with
    if (o && o.yours) {                                  // Day 5 (the designer, 6fb5c49): your reading is on Washer 2 itself, P3's training case
      const C = SHIP.works && caseState(), c = C && C.first && caseById(C.first), j = c && caseJob(c);
      if (c && c.train && j && j.status !== 'done' && !j.claimedBy) {
        c.m7 = true; MACH_REV++;
        if (typeof worksEscortHold === 'function') worksEscortHold('m7');   // the teacher stays with you till the case is called (24 core ends it on caseCalled)
        return j.id;
      }
    }
    const m = scanTrainMachine(d, SCAN_TRAINED); if (!m) return null;
    const cs = caseCauses(m).filter(x => x.part), f = cs[Math.floor(schedU(machSeed(m.id), d, 875) * cs.length)];
    const id = jobReserve(m.id, d, at, slot, { train: 'm7', tier: 1, cause: f.id }), j = id && SHIP.jobs.find(x => x.id === id); if (!j) return null;
    delete j.make; delete j.makeMins; j.cause = f.id; j.parts = [f.part]; SCAN_TRAINED.add(m.id);
    return id;
}
if (typeof WORK_MECH !== 'undefined') WORK_MECH.m7 = { reserve: scanTrainReserve };

// =====================================================================
// 24i. TRACING (M9, seat M3, 0.53.x; plans/mechanics/m9-tracing.html on claude/p5-design)
// Tier 2's new kind of thinking: a fault that shows in one place and starts somewhere else. Section 17 (seat S2,
// 0.33.59) keeps the lines (MACHINE_LINKS water, heat, air; lineOn, lineIds, lineDecks, linePath(line, id), lineFlow,
// flowWord) and posts traced faults: about half of an Officer's Tier 2 line repairs once you're trained in m9 carry
// j.symptom = { line, decks, deck }, and while traceHidden(j) its card names the symptom ("Showers weak on Deck 4") and
// no machine or place shows. This block is the doing of it. With the pipe kit you tap any machine on the line: a look
// at its panel (3 real seconds; section 15's workStep with the act's o.read) reads the flow there through section 17's
// traceMark(jobId, id) (before and after; kept in j.read; reading the job's own machine sets j.traceFound), shown in
// words and on the Pipe kit page; then it's an ordinary repair. A wrong turn costs a walk. The goal pointer leads to
// the line (the middle first among what you haven't read). Taught on Day 12 (ladder row m9, big, Officer, Calder): the
// row's opening holds 5-valve-2's traced repair for you (faulty, jobReserve slot 11); Calder reads the middle (the Deck
// 5 pumps, this block's small `tracedemo` kind) while you watch, then you read on and find it. The Maps app marks the
// line's machines (traceMarks). Removable: without this block nothing reads a traced job (the crew still fix them) and
// m9 never opens. Saved: nothing of its own (the job's symptom, read and traceFound are section 17's; ship.works.tools
// .pipekit, ship.works.use.m9). No R(), no 3D objects, no hash keys of its own (878 is section 17's; 879 spare).
// =====================================================================
const TRACE_SLOT = 11, TRACE_SECS = 3, TRACE_READ_K = 63;   // TRACE_READ_K: the reading's own slot in SHIP.player.wsteps (section 17 keeps the job's stops)
const TRACE_TRAIN = { line: 'water', machine: '5-valve-2', middle: '5-pump-1', cond: 40 };
const TRACE_LINE = { water: 'the water line', heat: 'the heating line', air: 'the air line', pool: 'the pool line' };   // pool: 0.84.5 (rec engineer B)
const TRACE_UI = { at: null, job: null, last: null };   // the machine being read; the job and reading the Pipe kit page shows
const traceLinesOn = () => typeof MACHINE_LINKS === 'object' && !!MACHINE_LINKS && typeof linePath === 'function' && typeof lineFlow === 'function'
  && typeof lineOn === 'function' && typeof lineIds === 'function' && typeof lineDecks === 'function' && typeof traceMark === 'function' && typeof traceHidden === 'function';
const traceHave = () => typeof hasTool === 'function' && hasTool('pipekit');
const traceWord = v => { const w = typeof flowWord === 'function' ? flowWord(v) : v >= .8 ? 'full' : v >= .5 ? 'low' : 'very low'; return worksText('trace.' + w.replace(' ', ''), w); };
const traceLineName = line => worksText('trace.line.' + line, TRACE_LINE[line] || 'the ' + line + ' line');
const traceName = id => (typeof machineTitle === 'function' && machineTitle(id)) || id;
// a line's steps from the top to a deck's end ([[ids], ...]; a side-by-side pair or a deck's two scrubbers is one step);
// [] when the line isn't on (section 17's lineOn: every machine on it real)
function tracePath(line, deck) {
  if (!traceLinesOn() || !lineOn(line)) return [];
  const ids = lineIds(line).filter(id => (lineDecks(line, id) || []).includes(deck)); if (!ids.length) return [];
  let p = null; try { p = linePath(line, ids[ids.length - 1]); } catch (e) { p = null; }
  return Array.isArray(p) ? p.map(s => [].concat(s)) : [];
}
const traceSteps = j => j && j.symptom ? tracePath(j.symptom.line, j.symptom.deck) : [];
const traceTraining = j => { const c = SHIP.works && SHIP.works.cur; return c && c.id === 'm9' && j && (c.j === j.id || j.train === 'm9') ? c : null; };
function traceSay(j, key, fallback) { const c = traceTraining(j); if (c && c.by) worksTeach('m9', c.by, 'follow.' + key, fallback); }

// ---- the reading (section 15's jobTap asks traceTap first; its workStepEnd hands a finished look whose act has o.read
// to traceRead, never to jobStepDone) ----
function traceTap(it, at) {
  const j = typeof myJob === 'function' ? myJob() : null;
  if (!traceLinesOn() || !traceHidden(j) || j.workDone || typeof deckDef === 'undefined' || !deckDef) return false;
  if (deckDef.num === 5 && roomAt(...cellAt(at.x, at.z)) === 'r' && !/tarp/i.test(it.t)) {   // main storage: no parts until you know the machine
    toast(it.t, worksText('trace.first', 'Find where it starts first: read the line with the pipe kit.')); return true;
  }
  const near = typeof MACHINE_NEAR !== 'undefined' ? MACHINE_NEAR : 1;
  const m = machineList().filter(x => x.deck === deckDef.num && !x.stub && x.at).map(x => {
    const p = cellPos(...x.at), pid = panelPlace(x.id), s = pid && PLACE_OF.has(pid) ? placeSpot(pid) : null;
    return [x, Math.min(Math.hypot(p.x - at.x, p.z - at.z), s ? Math.hypot(s.x - at.x, s.z - at.z) : Infinity)];
  }).filter(([, d]) => d < near).sort((a, b) => a[1] - b[1])[0];
  if (!m) return false;
  const id = m[0].id;
  if (!traceSteps(j).some(x => x.includes(id))) {
    if (!(typeof lineOf === 'function' && lineOf(id))) return false;   // nothing to do with the job: the machine's own tap
    toast(it.t, worksText('trace.wrongline', 'Not on this line. The job\'s on {line}.', { line: traceLineName(j.symptom.line) }));
    traceSay(j, 'wrong', 'Wrong line. Check the map: it\'s the ' + j.symptom.line + ' we want.');
    return true;
  }
  if (!traceHave()) { toast(it.t, worksText('trace.nokit', 'You need the pipe kit to read the flow.')); return true; }
  const pid = panelPlace(id), spot = pid && PLACE_OF.has(pid) ? placeSpot(pid) : null;
  if (!spot || typeof workStep !== 'function') return false;
  if (TRACE_UI.at !== id) SHIP.player.wsteps = SHIP.player.wsteps.filter(w => !(w.job === j.id && w.k === TRACE_READ_K));   // a fresh look at a new machine
  TRACE_UI.at = id;
  const st = { step: 'read', places: [pid], deck: m[0].deck, how: 'look', opts: { secs: TRACE_SECS, tool: 'pipekit', title: worksText('trace.kit', 'Pipe kit'), text: worksText('trace.clip', 'You clip the pipe kit on and read the flow.') } };
  if (!workStep(j, st, TRACE_READ_K, spot)) return false;
  if (ACT && ACT.kind === 'workStep') ACT.o.read = id;
  return true;
}
function traceRead(j, id) {
  if (TRACE_UI.at === id) TRACE_UI.at = null;
  const r = traceLinesOn() && traceHidden(j) ? traceMark(j.id, id) : null; if (!r) return false;
  const s = j.symptom, name = traceName(id); j.touched = shipNow();
  TRACE_UI.job = j.id; TRACE_UI.last = { id, before: r.before, after: r.after };
  const words = worksText('trace.before', 'Before: {word}', { word: traceWord(r.before) }) + ' · ' + worksText('trace.after', 'After: {word}', { word: traceWord(r.after) }) + '.';
  if (j.traceFound) {
    simNote('traceFound', { line: s.line, machine: j.machine, id: j.id });
    worksUse('m9'); if (typeof toolWear === 'function') toolWear('pipekit', 5);   // M11: 5 of 100 a trace (E1, 0.45.7)
    toast(name, words + ' ' + worksText('trace.found', 'Fine before {machine}, low after: that\'s where it starts.', { machine: traceName(j.machine) }));
    traceSay(j, 'found', 'There\'s your problem.');
  } else {
    const hint = r.after >= .8 ? worksText('trace.down', 'Full after it: the trouble is further down the line.') : r.before < .8 ? worksText('trace.up', 'Already low before it: the trouble is further up.') : '';
    toast(name, [words, hint].filter(Boolean).join(' '));
    traceSay(j, 'read', r.after >= .8 ? 'Full here. So it\'s further down, toward ' + deckIn(s.deck) + '. Halve it again.' : 'Low before it too. Back up the line.');
  }
  if (typeof ixGoalAt !== 'undefined') ixGoalAt = -1;
  if (typeof deviceShow === 'function') deviceShow('pipekit');
  return true;
}
// the goal pointer (15b's ixJobStep asks while traceHidden): the middle of the line first, among the machines not read yet
function traceGoal(j) {
  const dg = typeof poolDripGoal === 'function' ? poolDripGoal(j) : null; if (dg) return dg;   // 0.84.5 (rec engineer B): the pool leak's drip on Deck 5 first (24o's end)
  const steps = traceSteps(j), read = new Set(j.read || []), mid = Math.floor(steps.length / 2); if (!steps.length) return null;
  const ids = steps.map((x, k) => [x, Math.abs(k - mid)]).sort((a, b) => a[1] - b[1]).flatMap(([x]) => x).filter(id => !read.has(id) && panelPlace(id));
  const m = ids.length ? machineById(ids[0]) : null; if (!m) return null;
  return { deck: m.deck, place: panelPlace(m.id), label: worksText('trace.goal', 'Read {line}: try {machine}', { line: traceLineName(j.symptom.line), machine: traceName(m.id) }) };
}
// the Pipe kit page (opened by a reading, never from the grid): the last reading's two bars, then the line in order
// with what you've read on it
function traceView() {
  const j = SHIP.jobs.find(x => x.id === TRACE_UI.job), L = TRACE_UI.last; if (!j || !j.symptom || !L) return null;
  const s = j.symptom, title = typeof traceTitle === 'function' ? traceTitle(j) : '';
  const B = [{ kind: 'text', text: worksText('trace.title', 'Pipe kit · {machine}', { machine: traceName(L.id) }), mark: 'big' },
    { kind: 'text', text: [title, traceLineName(s.line)].filter(Boolean).join(' · ') },
    { kind: 'bars', items: [['before', L.before], ['after', L.after]].map(([k, v]) => ({ label: worksText('trace.' + k, (k === 'before' ? 'Before' : 'After') + ': {word}', { word: traceWord(v) }), value: Math.round(v * 100), level: v < .5 ? 'low' : v < .8 ? 'mid' : '' })) }];
  const read = new Set(j.read || []), rows = traceSteps(j).map(x => {
    const r = x.find(id => read.has(id)), v = r ? lineFlow(s.line, r) : null;
    return { text: x.map(traceName).join(' & '), sub: v === null ? 'not read' : traceWord(v), mark: x.includes(L.id) ? 'hot' : null };
  });
  B.push({ kind: 'text', text: worksText('trace.order', 'The line, upstream first'), mark: 'head' }, { kind: 'list', rows });
  if (j.traceFound) B.push({ kind: 'text', text: worksText('trace.found', 'Fine before {machine}, low after: that\'s where it starts.', { machine: traceName(j.machine) }), mark: 'hot' });
  return B;
}
deviceApp({ id: 'pipekit', title: 'Pipe kit', short: 'Pipe kit', icon: 'wrench', order: 34, hidden: () => true,
  view: () => ({ title: 'Pipe kit', blocks: traceView() || [{ kind: 'text', text: 'Nothing read yet. Tap a machine on the job\'s line to read the flow there.' }] }) });
// the Maps app (section 19): the machines of your traced job's line on this deck, marked ({ tiles, text } | null);
// the training's line from the row's opening
function traceMarks(n) {
  if (!traceLinesOn()) return null;
  const j = typeof myJob === 'function' ? myJob() : null, c = SHIP.works && SHIP.works.cur;
  const s = traceHidden(j) ? j.symptom : c && c.id === 'm9' && /^(watch|do)$/.test(c.st) ? { line: TRACE_TRAIN.line, deck: 4 } : null;
  if (!s) return null;
  const ms = tracePath(s.line, s.deck).flat().map(id => machineById(id)).filter(m => m && m.at), here = ms.filter(m => m.deck === n);
  const decks = [...new Set(ms.map(m => m.deck))].sort(); if (!decks.length) return null;
  return { tiles: here.map(m => m.at.slice()), text: traceLineName(s.line).replace(/^./, x => x.toUpperCase()) + (here.length ? ': its machines are marked.' : ' runs through ' + (decks.length > 1 ? 'Decks ' + decks.slice(0, -1).join(', ') + ' and ' + decks[decks.length - 1] : deckIn(decks[0])) + '.') };   // deckIn: 0.84.5 (rec engineer B), the pool line runs through the rec deck
}

// ---- the training (ladder row m9, 24 core's flow): Calder reads the middle while you watch (this block's own small
// job kind, never the crew's), then the traced valve is yours ----
if (traceLinesOn() && typeof jobKindAdd === 'function') jobKindAdd('tracedemo', { tier: 2, work: 5, text: 'Read the line',
  stops: () => [{ deck: (machineById(TRACE_TRAIN.middle) || { deck: 5 }).deck, placeId: panelPlace(TRACE_TRAIN.middle), mins: 5, tag: 'read', how: 'look' }],
  done(j, t, by) {                                       // you did Calder's reading yourself: on to the valve
    const c = SHIP.works && SHIP.works.cur; if (by !== 'you' || !c || c.id !== 'm9' || c.j !== j.id) return;
    const id = traceTrainJob(worksDay(t), t - (worksDay(t) - 1) * 1440); if (id) { c.j = id; c.st = 'do'; }
  },
  crew: { can: () => false, mins: 5 } });
// the training's traced job: 5-valve-2 faulty (if it isn't already worse) with a cause that cuts the water line, held
// for you in slot 11; its symptom from section 17 (Deck 4's showers)
function traceTrainJob(d, at) {
  const ex = SHIP.jobs.find(x => x.reserved === TRACE_SLOT && x.train === 'm9' && x.machine === TRACE_TRAIN.machine && x.status !== 'done');
  if (ex) return ex.id;
  if (!lineOn(TRACE_TRAIN.line) || !machineById(TRACE_TRAIN.machine)) return null;
  const s = SHIP.machines[TRACE_TRAIN.machine];
  if (typeof machineFault === 'function' && (!s || s.cond > TRACE_TRAIN.cond)) machineFault(TRACE_TRAIN.machine, TRACE_TRAIN.cond);
  const kind = machineById(TRACE_TRAIN.machine).kind, cause = (FAULT_CAUSES[kind] || []).find(c => c.line === TRACE_TRAIN.line && c.part);
  const id = jobReserve(TRACE_TRAIN.machine, d, at, TRACE_SLOT, { train: 'm9', tier: 2, ...(cause ? { cause: cause.id } : {}) }), j = id && SHIP.jobs.find(x => x.id === id); if (!j) return null;
  delete j.make; delete j.makeMins; if (!cause) j.parts = [MACHINE_KINDS[kind].part]; j.train = 'm9';
  j.symptom = typeof traceSymptom === 'function' ? traceSymptom(TRACE_TRAIN.line, TRACE_TRAIN.machine) : { line: TRACE_TRAIN.line, decks: [4, 5, 6], deck: 4 };
  if (typeof MACH_REV !== 'undefined') MACH_REV++;
  return id;
}
function traceDemoJob(d, at) {
  const t = (d - 1) * 1440 + at, pid = panelPlace(TRACE_TRAIN.middle); if (!pid || !JOB_KINDS.tracedemo) return null;
  SHIP.jobs = SHIP.jobs.filter(x => !(x.kind === 'tracedemo' && x.status !== 'done'));
  const j = jobMake('tracedemo', { id: 'tracedemo:' + TRACE_TRAIN.middle + '@' + t, deck: 5, room: (machineById(TRACE_TRAIN.middle) || {}).room || null, h: Math.floor(t / 60),
    title: worksText('trace.demo', 'Read the line with Calder'), tier: 2, reserved: TRACE_SLOT, until: (d - 1) * 1440 + DAY_SHIFT[1], train: 'm9' });
  j.posted = j.found = t; SHIP.jobs.push(j);
  if (typeof MACH_REV !== 'undefined') MACH_REV++;
  return j.id;
}
if (traceLinesOn() && JOB_KINDS.tracedemo && typeof CAREER_LADDER !== 'undefined') {
  if (!ladderRow('m9')) CAREER_LADDER.push({ id: 'm9', name: 'Tracing', size: 'big', day: 12, tier: 2, rank: 'officer', needs: null, by: ['calder', 'halloran-emeka'], where: { deck: 5, room: 'w' }, job: 'trace', tool: 'pipekit', stages: [{ uses: 0 }] });   // (24 core has it from 0.44.23)
  WORK_MECH.m9 = {
    open(row, d) { traceTrainJob(d, 360); },          // the showers on Deck 4 run weak from the row's opening (06:00 at the earliest)
    reserve(d, at, slot, o = {}) {
      if (typeof toolGive === 'function') toolGive('pipekit');   // handed over at the board, at the meeting
      if (!traceTrainJob(d, at)) return null;
      return o.yours ? traceTrainJob(d, at) : traceDemoJob(d, at);
    },
    watch: 10,                                           // ship minutes watching Calder read the Deck 5 pumps
  };
  if (typeof WORK_TOOLS !== 'undefined' && WORK_TOOLS.pipekit) WORK_TOOLS.pipekit.mech = 'm9';   // the pipe kit wears with tracing (24 core's own from 0.44.23)
  onSim('job', n => { const j = n && SHIP.jobs.find(x => x.id === n.id); if (n.step === 'done' && j && j.symptom && traceTraining(j)) traceSay(j, 'done', 'Showers on Deck 4 back to full. Good work.'); });
}
// the Chief's notes page (24k's CHIEF_NOTES, made after this block: added on the first tick); open once you're trained
const TRACE_CHIEF = { title: 'Tracing', key: 'chief.m9', open: () => !!(SHIP.works && SHIP.works.tr.m9 !== undefined), lines: [
  'Read the middle first. Halve the line each time.',
  'Fine before a machine and low after it: that machine is the cause. The symptom is only where it shows.'] };
if (typeof WORK_TICKS !== 'undefined') WORK_TICKS.push(() => { if (typeof CHIEF_NOTES === 'object' && CHIEF_NOTES && !CHIEF_NOTES.m9) CHIEF_NOTES.m9 = TRACE_CHIEF; });

// =====================================================================
// 24j. THE WORKSHOP AND TINKERING (M10, seat E3, 0.53.x; plans/mechanics/m10-workshop.html on claude/p5-design)
// Crew order little things at the machine shop and you make them. From Day 12, once you're a Works Officer, the order
// board (5-shop-board, the machine shop's north wall) gets one or two orders a week: one on Day 12 at 08:00, then
// Mondays at 08:00, each from crew who know you (an acquaintance or better; schedU(week, 0 | 2, 1010)) for a thing off
// WORKSHOP_ORDERS (schedU(week, 1 | 3, 1011)). Tap the board and take one: it becomes your side job (kind 'shop',
// beside your board job): at the lathe or the fabricator (5-shop-lathe / 5-shop-fab) a wait (10 ship minutes: set it
// going, come back) and a short hold to finish. Then the thing is in your hands to hand over: their chat card shows Give <thing>
// (section 20's two hook lines: shopGiveButton, shopGiveSay): a thank-you, a friendship step, and Works reputation +1
// (at most one a day here, and through 24 core's side-job cap, worksSideXp). An order you never take lapses after 7 days
// ("I made do"), no harm. The first order is ladder row m10 (small): the Works officer on shift (the row's by-list) says
// how, at the machine. Stage 2, after 3 orders: an order with a part takes one from main storage first (you fetch it off
// the shelf; none left, you make do with offcuts). Stage 3, after 6: two more things to tinker.
// Tinkering, from Day 6: with no board job, tap the lathe or the fabricator and pick something off TINKER_LIST to make
// from offcuts (scrap is free, one at a time); it goes into your hands as a gift (SOC_GIFTS gets the list, section 20's
// Give) or for your cabin (24t). Before Day 6 the machine shop makes section 20's GIFT_MAKES, as before.
// Hooks: one line in section 15's jobTap (shopTap, before its gift-making), two in section 20's chat card. Saved in
// SHIP.works.side.shop = { orders: [{ id, who, what, day, state, job?, part? }], made, tinkered: [ids], xpDay, taught }
// (24 core's worksSide(); read defensively, so old saves load). No R(); keys 1010-1011.
const SHOP_FROM = 12, TINKER_FROM = 6, SHOP_POST = 480, SHOP_LAPSE = 7, SHOP_WAIT = 10, SHOP_HOLD = 2, SHOP_STAGE = [3, 6];
// the orders: thing (what you make), ask (the order card), at (lathe | fab), part (stage 2: from main storage), thanks
const WORKSHOP_ORDERS = [
  { id: 'guitar-hook', thing: 'guitar hook', ask: 'A hook for my guitar, please.', at: 'lathe', thanks: 'It holds! The guitar finally has a home off the floor.' },
  { id: 'mug-rack', thing: 'mug rack', ask: 'A little rack for my mugs?', at: 'fab', thanks: 'Four mugs, one rack, no more mugs on the floor. Thank you.' },
  { id: 'book-stand', thing: 'book stand', ask: 'Something to hold a book open while I eat.', at: 'fab', thanks: 'Hands free for the soup. You\'re a marvel.' },
  { id: 'lamp-arm', thing: 'lamp arm', ask: 'A bendy arm for my reading lamp.', at: 'lathe', part: 'cable', thanks: 'It bends exactly where I want it. Reading in bed again!' },
  { id: 'plant-hanger', thing: 'plant hanger', ask: 'A hanger so my plant gets the light.', at: 'fab', thanks: 'It\'s already leaning towards the lamp. Thank you.' },
  { id: 'fan-spindle', thing: 'fan spindle', ask: 'My desk fan\'s spindle snapped. Could you turn a new one?', at: 'lathe', part: 'bearing', thanks: 'Whirring again. Quietly, too.' },
  { id: 'drawer-pull', thing: 'drawer pull', ask: 'A pull for my drawer. The old one came off in my hand.', at: 'lathe', thanks: 'Opens first time now. Small thing, big difference.' },
  { id: 'tablet-stand', thing: 'tablet stand', ask: 'A stand for my tablet, for calls home?', at: 'fab', part: 'seal', thanks: 'Mum says I look less like I\'m calling from a cupboard.' },
];
// tinkering: what you can make from offcuts (the last two from stage 3); all gifts (SOC_GIFTS) and cabin things (24t's cabin: the spot each fits)
const TINKER_LIST = [
  { item: 'little lamp', mins: 20, cabin: 'desk' }, { item: 'mug tree', mins: 15, cabin: 'ledge' }, { item: 'toy rocket', mins: 15, cabin: 'shelf' },
  { item: 'plant pot', mins: 10, cabin: 'ledge' }, { item: 'model ship', mins: 30, cabin: 'shelf', stage: 3 }, { item: 'woven rug', mins: 30, cabin: 'rug', stage: 3 },
];
if (typeof SOC_GIFTS === 'object' && SOC_GIFTS) for (const t of TINKER_LIST) if (!SOC_GIFTS[t.item]) SOC_GIFTS[t.item] = { tag: 'made', from: 'made' };
const shopDef = id => WORKSHOP_ORDERS.find(o => o.id === id) || null;
// your part of the save, cleaned (a missing or odd field is its default)
function shopData() {
  const S = typeof worksSide === 'function' ? worksSide() : null; if (!S) return null;
  const s = S.shop && typeof S.shop === 'object' ? S.shop : (S.shop = {});
  if (!Array.isArray(s.orders)) s.orders = [];
  s.orders = s.orders.filter(o => o && typeof o.id === 'string' && shopDef(o.what) && typeof o.who === 'string' && /^(posted|taken|made|given|lapsed)$/.test(o.state)).slice(-20);
  if (!Number.isInteger(s.made) || s.made < 0) s.made = 0;
  if (!Array.isArray(s.tinkered)) s.tinkered = []; s.tinkered = s.tinkered.filter(x => typeof x === 'string').slice(-20);
  for (const k of ['xpDay', 'taught', 'posted']) if (k in s && !Number.isInteger(s[k])) delete s[k];
  for (const o of s.orders) { if (!Number.isInteger(o.day)) o.day = 0; if (o.job !== undefined && typeof o.job !== 'string') delete o.job; if (o.part !== undefined && typeof o.part !== 'string') delete o.part; }
  return s;
}
const shopStage = s => s && s.made >= SHOP_STAGE[1] ? 3 : s && s.made >= SHOP_STAGE[0] ? 2 : 1;
const shopOn = (d = worksDay(shipNow())) => d >= SHOP_FROM && !!SHIP.works && SHIP.works.rank !== 'junior' && typeof jobKindAdd === 'function';
const shopWho = id => { try { return socP(id); } catch (e) { return null; } };
const shopName = id => { const p = shopWho(id); return p ? shortName(p) : worksFirst(id); };
const shopThing = o => (shopDef(o.what) || {}).thing || 'thing';
// who asks this week: crew who know you (acquaintance or better), not with an order open, in id order, picked by key 1010
function shopPick(week, k, taken) {
  socInit();
  let pool = SOC.crew.filter(p => p && p.id && !p.player && !taken.has(p.id) && relTier(p.id) >= 1).map(p => p.id).sort();
  if (!pool.length) pool = SOC.crew.filter(p => p && p.id && !p.player && !taken.has(p.id) && p.dept === 'works').map(p => p.id).sort();   // nobody yet: a Works colleague
  return pool.length ? pool[Math.floor(schedU(week, k, 1010) * pool.length)] : null;
}
function shopPost(d, s) {                                // one or two orders on the board (Day 12: one)
  const week = Math.floor((d - 1) / 7), open = s.orders.filter(o => o.state === 'posted' || o.state === 'taken' || o.state === 'made');
  const busy = new Set(open.map(o => o.who)), used = new Set(open.map(o => o.what)), n = d === SHOP_FROM ? 1 : schedU(week, 4, 1010) < .5 ? 2 : 1;
  for (let k = 0; k < n; k++) {
    const who = shopPick(week, 2 * k, busy), defs = WORKSHOP_ORDERS.filter(o => !used.has(o.id)); if (!who || !defs.length) break;
    const what = defs[Math.floor(schedU(week, 2 * k + 1, 1011) * defs.length)].id;
    s.orders.push({ id: 'o' + d + '-' + k, who, what, day: d, state: 'posted' }); busy.add(who); used.add(what);
  }
  s.posted = d;
}
// the side job: made when you take an order (yours from the start, like the drill), never on the board for the crew
const shopPlace = o => (shopDef(o.what) || {}).at === 'fab' ? '5-shop-fab' : '5-shop-lathe';
if (typeof jobKindAdd === 'function') jobKindAdd('shop', { tier: 2, work: 0, side: true, text: 'Workshop order',
  stops: j => [{ deck: 5, placeId: j.place, mins: 0, tag: 'make', how: 'wait', opts: { mins: SHOP_WAIT, text: 'You set the ' + (j.place === '5-shop-fab' ? 'fabricator' : 'lathe') + ' going on the ' + j.thing + '.' } },
               { deck: 5, placeId: j.place, mins: SHOP_HOLD, tag: 'finish' }],
  done(j, t, by) { const s = shopData(), o = s && s.orders.find(x => x.id === j.order); if (o && o.state === 'taken') o.state = 'made'; },
  crew: { can: () => false, mins: 0 } });
const shopJobOf = o => o && o.job ? SHIP.jobs.find(j => j.id === o.job && j.status === 'claimed' && j.claimedBy === 'you') || null : null;
function shopTake(o) {
  if (typeof jobMake !== 'function' || o.state !== 'posted') return false;
  const s = shopData(), def = shopDef(o.what), t = shipNow(), part = shopStage(s) >= 2 && def.part ? def.part : null;
  const j = jobMake('shop', { id: 'shop:' + o.id, deck: 5, room: 'f', title: 'Make the ' + def.thing + ' for ' + shopName(o.who), order: o.id, place: shopPlace(o), thing: def.thing, parts: part ? [part] : [] });
  j.claimedBy = 'you'; j.status = 'claimed'; j.start = t; SHIP.jobs.push(j);
  o.state = 'taken'; o.job = j.id; if (part) o.part = part; MACH_REV++;
  if (typeof flagSet === 'function' && !(typeof flag === 'function' && flag('works.shop'))) flagSet('works.shop', worksDay(t));   // opens ladder row m10
  return true;
}
// the board: the orders up, to take one
function shopBoard(it) {
  const s = shopData(); if (!s) return false;
  const up = s.orders.filter(o => o.state === 'posted'), mine = s.orders.filter(o => o.state === 'taken' || o.state === 'made'), P = SHIP.player;
  for (const o of mine) if (o.state === 'made' && !P.carry.includes(shopThing(o)) && P.carry.length < CARRY_MAX) { P.carry.push(shopThing(o)); toast(it.t, 'The ' + shopThing(o) + ' for ' + shopName(o.who) + ' was waiting by the board. It\'s in your hands.'); return true; }
  const yours = mine.length ? ' Yours: ' + mine.map(o => 'the ' + shopThing(o) + ' for ' + shopName(o.who) + (o.state === 'made' ? ' (made: hand it over)' : '')).join('; ') + '.' : '';
  if (!shopOn()) { toast(it.t, 'Little orders from the crew, for the machine shop. Officers take them.'); return true; }
  if (!up.length) { toast(it.t, 'Nothing new pinned up. Orders go up on Mondays.' + yours); return true; }
  const ok = deviceChoose({ title: 'Order board', text: 'Take an order: make it here, then hand it over in person.' + yours,
    choices: up.slice(0, 5).map(o => shopName(o.who) + ': ' + worksText('works.order.ask.' + o.what, shopDef(o.what).ask)) }, i => {
    const o = up[i]; if (!o || !shopTake(o)) return;
    toast('Order board', 'You take ' + shopName(o.who) + '\'s order: the ' + shopThing(o) + '. ' + (o.part ? 'It needs ' + partList([o.part]) + ' from main storage, then the ' : 'At the ') + (shopPlace(o) === '5-shop-fab' ? 'fabricator' : 'lathe') + '.');
    if (typeof device === 'object' && device && device.refresh) device.refresh();
  });
  if (!ok) toast(it.t, 'Your device is busy; try again in a moment.');
  return true;
}
// at the machine: the first time, the officer on shift says how (ladder row m10's word)
function shopTeach(s) {
  if (s.taught) return; s.taught = worksDay(shipNow());
  const row = typeof ladderRow === 'function' && ladderRow('m10'), by = row && (ladderTeacher(row, s.taught) || row.by[0]);
  if (by) worksTeach('m10', by, 'lead', ['Set it going, then go and do something useful. It\'ll be ready in ten.', 'Finish it by hand. That\'s the part they\'ll notice.']);
}
const shopMachineOf = it => /^lathe$/i.test(it.t) ? '5-shop-lathe' : /fabricator/i.test(it.t) ? '5-shop-fab' : null;
function shopStep(j, it, at) {                           // your order's next stop, at the machine it needs
  const st = jobStops(j), k = st.findIndex(x => !x.done), x = st[k]; if (!x) return false;
  const P = SHIP.player, s = shopData(), o = s && s.orders.find(y => y.id === j.order);
  if (x.step === 'fetch') { toast(it.t, 'The ' + j.thing + ' needs ' + partList(j.parts) + ' from main storage next door first.'); return true; }
  if (shopMachineOf(it) !== j.place) return false;
  const pid = x.places[0], spot = pid && PLACE_OF.has(pid) ? placeSpot(pid) : null;
  shopTeach(s);
  if (x.step === 'finish' && P.carry.length >= CARRY_MAX) { toast(it.t, 'Your hands are full (' + partList(P.carry) + '): free one to take the ' + j.thing + '.'); return true; }
  if (x.step === 'make') {
    const w = typeof wsFind === 'function' && wsFind(j.id, k);
    if (j.parts.length && !(w && w.at !== null)) { const i = P.carry.indexOf(j.parts[0]); if (i >= 0) P.carry.splice(i, 1); }   // the part goes in as you set it going
    return workStep(j, { ...x, how: 'wait', opts: { mins: SHOP_WAIT, text: 'You set the ' + (j.place === '5-shop-fab' ? 'fabricator' : 'lathe') + ' going on the ' + j.thing + '.' } }, k, spot);
  }
  actStart('shopFinish', null, { title: it.t, job: j.id, ws: k, spot: spot ? { ...spot, id: null, pose: 'stand' } : null, after: 'You finish the ' + j.thing + ' by hand.' });
  if (ACT && ACT.kind === 'shopFinish') ACT.def.until = A => {
    if (A.done < SHOP_HOLD) return false; if (A.o.fin) return true; A.o.fin = true;
    const r = jobStepDone(A.o.job, A.o.ws);
    if (r && r.done) { const jj = SHIP.jobs.find(y => y.id === A.o.job); if (jj && jj.status === 'claimed') jobFinish(jj, shipNow(), 'you');
      if (o) { SHIP.player.carry.push(shopThing(o)); toast('Machine shop', 'The ' + shopThing(o) + ' is done, and in your hands. Hand it to ' + shopName(o.who) + ' in person.'); } }
    if (typeof device === 'object' && device && device.refresh) device.refresh();
    return true;
  };
  return true;
}
function shopFetch(j, it, at) {                          // stage 2: the order's part off a storage shelf
  const st = jobStops(j), k = st.findIndex(x => !x.done), x = st[k]; if (!x || x.step !== 'fetch') return false;
  const P = SHIP.player, part = j.parts[0];
  if (P.carry.includes(part)) { jobStepDone(j.id, k); toast(it.t, 'You have the ' + part + '. Now the ' + (j.place === '5-shop-fab' ? 'fabricator' : 'lathe') + '.'); return true; }
  if (P.carry.length >= CARRY_MAX) { toast(it.t, 'Your hands are full (' + partList(P.carry) + ').'); return true; }
  if (takePart(part)) { P.carry.push(part); toast(it.t, 'You take ' + partList([part]) + ' for the ' + j.thing + '.'); }
  else { j.offcuts = true; toast(it.t, 'No ' + part + ' left on the shelf. You\'ll make do with offcuts.'); }   // the part list stays, so the stops don't shift
  jobStepDone(j.id, k); return true;
}
// tinkering: a short list, one at a time, from offcuts
function shopTinker(it, at) {
  const P = SHIP.player, s = shopData(), d = worksDay(shipNow());
  if (d < TINKER_FROM || !shopMachineOf(it)) return false;
  const held = P.carry.find(x => TINKER_LIST.some(t => t.item === x));
  if (held) { toast(it.t, 'One at a time: give the ' + held + ' to someone, or find it a spot in your cabin, first.'); return true; }
  if (P.carry.length >= CARRY_MAX) { toast(it.t, 'Your hands are full (' + partList(P.carry) + ').'); return true; }
  const list = TINKER_LIST.filter(t => !t.stage || shopStage(s) >= t.stage), pl = jobPlaceNear('storage', 'f', at);
  if (!pl) return false;
  const ok = deviceChoose({ title: 'Tinker', text: 'Make something from offcuts: a gift, or something for your cabin.', choices: list.map(t => t.item.charAt(0).toUpperCase() + t.item.slice(1)) }, i => {
    const t = list[i]; if (!t) return;
    actStart('craft', pl.id, { title: it.t, flavour: it.x, gift: t.item, needs: null, after: 'You make ' + partList([t.item]) + ' from offcuts: about ' + taskMins(t.mins) + ' minutes.' });
    if (ACT && ACT.kind === 'craft') { ACT.def.mins = t.mins; ACT.def.until = A => { if (A.done < t.mins) return false; if (!A.o.tk) { A.o.tk = true; if (s) s.tinkered = s.tinkered.concat([t.item]).slice(-20); if (typeof leisureAdd === 'function') leisureAdd(4, 'tinker'); } return true; }; }
  });
  if (!ok) toast(it.t, 'Your device is busy; try again in a moment.');
  return true;
}
// section 15's jobTap asks this first (mw: your machine job under way, or null). Your board job comes first where it needs
// the place: its shelves in main storage, its part to make in the machine shop; tinkering only with no machine job
function shopTap(it, at, mw) {
  if (typeof deckDef === 'undefined' || deckDef.num !== 5) return false;
  const room = roomAt(...cellAt(at.x, at.z)), s = shopData(), P = SHIP.player;
  if (room === 'f' && /^order board$/i.test(it.t)) return shopBoard(it);
  const j = s && s.orders.map(shopJobOf).find(Boolean);
  if (j && room === 'r' && !(mw && typeof shelfNeeds === 'function' && shelfNeeds(mw.j, mw.w, P.carry).length) && shopFetch(j, it, at)) return true;
  const held = room === 'r' && !mw && s && s.orders.find(o => o.state === 'made' && P.carry.includes(shopThing(o)));
  if (held) { toast(it.t, 'The ' + shopThing(held) + ' isn\'t for the shelves: it\'s ' + shopName(held.who) + '\'s. Hand it over in person.'); return true; }
  if (room !== 'f') return false;
  if (j && !(mw && (mw.w.make || typeof jobNeeds === 'function' && jobNeeds(mw.j, mw.w, P.carry).length)) && shopStep(j, it, at)) return true;
  return !mw && shopTinker(it, at);
}
Object.assign(PLAYER_ACTS, { shopFinish: { mins: SHOP_HOLD, pose: 'work', title: 'Machine shop' } });
// section 20's chat card: Give <thing> to whoever ordered it, once it's made
function shopGiveButton(p) { const s = shopData(), o = s && p && s.orders.find(x => x.who === p.id && x.state === 'made' && SHIP.player.carry.includes(shopThing(x))); return o ? { id: 'shop-give', label: 'Give the ' + shopThing(o) } : null; }
function shopGiveSay(p) {
  const s = shopData(), P = SHIP.player, o = s && p && s.orders.find(x => x.who === p.id && x.state === 'made' && P.carry.includes(shopThing(x))); if (!o) return null;
  const d = worksDay(shipNow()); o.state = 'given'; o.given = d; s.made++; P.carry.splice(P.carry.indexOf(shopThing(o)), 1);
  if (typeof relAdd === 'function') relAdd(p.id, 'favour', 6);
  if (s.xpDay !== d) { s.xpDay = d; if (typeof worksSideXp === 'function') worksSideXp(1, 'shop'); }
  worksUse('m10');
  return worksText('works.order.thanks.' + o.what, shopDef(o.what).thanks, { name: shortName(p) });
}
if (typeof WORK_TICKS !== 'undefined') WORK_TICKS.push(now => {   // Day 12 and Mondays at 08:00: orders go up; a week untaken, one lapses
  const d = worksDay(now), m = now - (d - 1) * 1440; if (!shopOn(d)) return;
  const s = shopData(); if (!s) return;
  if (m >= SHOP_POST && s.posted !== d && (d === SHOP_FROM || weekday(d) === 0 && d > SHOP_FROM)) shopPost(d, s);
  for (const o of s.orders) if (o.state === 'posted' && d - o.day >= SHOP_LAPSE) {
    o.state = 'lapsed';
    if (typeof mailSend === 'function') mailSend({ at: now, from: worksName(o.who), subject: 'The ' + shopThing(o), body: worksText('works.order.lapse', 'I made do, don\'t worry. Another time!'), quiet: true });
  }
  for (const o of s.orders) if (o.state === 'taken' && !SHIP.jobs.some(j => j.id === o.job && j.status !== 'done')) o.state = SHIP.jobs.some(j => j.id === o.job) ? 'made' : 'posted';   // a job lost to a reload: back on the board
});
if (typeof WORK_MECH !== 'undefined') WORK_MECH.m10 = { open() { /* the word comes at the machine, with your first order (shopTeach) */ } };

// =====================================================================
// 24t. OFF SHIFT: CABIN TOUCHES AND STAR LOGGING (seat E3, 0.53.x; plans/mechanics/off-shift.html on claude/p5-design)
// Cabin touches: once cabin 4-23 is yours (SHIP.works.home), its four spots (DECKS[4].cabinSpots['4-23']: rug, desk,
// shelf beside the keepsakes, ledge) take things from your hands that fit them (CABIN_FITS: what you tinker at 24j's
// machine shop, a few things from the crew store). Tap a spot: what's in your hands goes there (what was there comes
// back to your hands if there's room); with nothing that fits, a spot with a thing gives it back. Each placed thing is
// drawn small (one merged mesh per spot in the thing's colour, so at most 4 draw calls; built when you're on Deck 4 and
// 4-23 is yours, after a deck change within a ship minute). Two or more touches: you wake a little happier (leisure at
// 06:00 if you slept in 4-23; cabinMood() for section 15 to read).
// Star logging: from Day 6, 20:00-23:30, at the observatory's telescope (Deck 2), one a night: three points through the
// eyepiece, two on your chart, pick the new one (schedU(day, k, 1024) the points, schedU(day, 0, 1025) the new one); a
// wrong pick, look again. Every third log Survey warms to you (a friendship step with Dr. Sato, then Mori, in turn, and
// their cue line stars.talk); ten logs: a Record line (SHIP.works.ms 'stars'; 24 core shows works.ms.stars). starsLogged()
// for Day 19's lesson (M20). The writer's keys: cabin.spot.*, star.* (claude/writer-p5 b00e08b).
// Saved in SHIP.works.side.cabin = { rug, desk, shelf, ledge } (item names) and .stars = { n, last } (24 core's
// worksSide(); read defensively). No R(); every colour through col() (dressMat); keys 1024-1025.
const CABIN_SPOTS = ['rug', 'desk', 'shelf', 'ledge'];
const CABIN_FITS = { rug: ['woven rug'], desk: ['little lamp'], shelf: ['toy rocket', 'model ship', 'paper novel', 'puzzle book', 'pocket puzzle', 'metal puzzle'], ledge: ['plant pot', 'little plant', 'mug tree', 'flower'] };
const CABIN_NAME = { rug: 'The floor', desk: 'The desk', shelf: 'The shelf', ledge: 'The ledge' };
const CABIN_LOOK = {                                     // each thing's shape: [w, h, d] boxes or [r, h] cylinders from its spot's point, and its colour
  'woven rug': { c: '#b5603d', box: [[1.1, .012, .75, 0, .006, 0]] }, 'little lamp': { c: '#e3c27a', cyl: [[.06, .03, 0, .017], [.012, .26, 0, .16], [.09, .1, 0, .31]] },
  'toy rocket': { c: '#d9534f', cyl: [[.035, .16, 0, .08], [.012, .05, 0, .185]] }, 'model ship': { c: '#9aa7b4', box: [[.24, .06, .08, 0, .03, 0], [.08, .05, .06, .02, .085, 0]] },
  'plant pot': { c: '#c0703e', cyl: [[.06, .1, 0, .05]] }, 'little plant': { c: '#5c9a4a', cyl: [[.06, .09, 0, .045], [.08, .1, 0, .14]] }, 'mug tree': { c: '#8a6a4a', cyl: [[.03, .02, 0, .01], [.008, .16, 0, .1]], box: [[.1, .01, .01, 0, .13, 0]] },   // (0.53.11: was 'mug rack', which an M10 order makes too)
  'flower': { c: '#d98bb0', cyl: [[.03, .14, 0, .07]] },
  'paper novel': { c: '#3f6e8c', box: [[.1, .15, .03, 0, .075, -.03]] }, 'puzzle book': { c: '#c9a24a', box: [[.14, .025, .1, 0, .0125, -.05]] },   // (E4, R5's fix 2: these four had no look)
  'pocket puzzle': { c: '#d9534f', box: [[.06, .06, .06, 0, .03, -.05]] }, 'metal puzzle': { c: '#9aa7b4', cyl: [[.045, .02, 0, .01]], box: [[.02, .07, .02, 0, .055, 0]] },
};
const cabinMine = () => typeof worksHome === 'function' && worksHome() === '4-23' && !!(DECKS[4].cabinSpots && DECKS[4].cabinSpots['4-23']);
function cabinData() {
  const S = typeof worksSide === 'function' ? worksSide() : null; if (!S) return null;
  const c = S.cabin && typeof S.cabin === 'object' && !Array.isArray(S.cabin) ? S.cabin : (S.cabin = {});
  if (c.ledge === 'mug rack') c.ledge = 'mug tree';      // a save from before 0.53.11
  for (const k of Object.keys(c)) if (!CABIN_SPOTS.includes(k) || typeof c[k] !== 'string' || !CABIN_FITS[k].includes(c[k])) delete c[k];
  return c;
}
const cabinPlaced = id => { const c = cabinData(); return !!c && Object.values(c).includes(id); };   // for section 15b's locker
// things placed in your cabin count as put away (the page): tidy if you've bought or made nothing since you last placed one
const cabinPutAway = () => { const S = typeof worksSide === 'function' ? worksSide() : null, a = S && S.cabinPut, P = SHIP.player; return cabinMine() && Array.isArray(a) && (P.bought || 0) <= a[0] && (P.crafted || 0) <= a[1]; };
const cabinTouches = () => { const c = cabinData(); return c ? Object.keys(c).length : 0; };
const cabinMood = () => cabinMine() && cabinTouches() >= 2 ? 1 : 0;
// the spots' taps and the things on them, rebuilt when the deck or what's placed changes
const CAB = { root: null, key: '', g: null, items: [], woke: 0 };
function cabinClear() {
  if (CAB.g) { CAB.g.parent && CAB.g.parent.remove(CAB.g); CAB.g.traverse(o => { if (o.geometry) o.geometry.dispose(); }); }
  if (CAB.items.length) { ITEMS = ITEMS.filter(it => !CAB.items.includes(it)); if (typeof refreshPickables === 'function') refreshPickables(); }
  CAB.g = null; CAB.items = []; CAB.key = '';
}
function cabinDraw() {
  if (typeof deckRoot === 'undefined' || !deckRoot || typeof deckDef === 'undefined') return;
  const on = deckDef.num === 4 && cabinMine(), c = on ? cabinData() : null, key = on ? JSON.stringify(c) : '';
  if (CAB.root === deckRoot && CAB.key === key) return;
  if (CAB.root !== deckRoot) { CAB.g = null; CAB.items = []; CAB.root = deckRoot; }   // a new deck: the old group went with it
  cabinClear(); if (!on || !c) return;
  const spots = DECKS[4].cabinSpots['4-23'], g = new THREE.Group(); CAB.g = g; CAB.key = key; deckRoot.add(g);
  for (const k of CABIN_SPOTS) {
    const sp = spots[k], [x, y, z] = sp.at, wx = x - OX, wz = z - OZ, s = new THREE.Group(); s.position.set(wx, y, wz); g.add(s);
    const L = c[k] && CABIN_LOOK[c[k]], m = L && dressMat(L.c);
    if (L) {
      for (const [w, h, d, ox, oy, oz] of L.box || []) { const b = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), m); b.position.set(ox, oy + .002, oz); s.add(b); }
      for (const [r, h, ox, oy] of L.cyl || []) { const b = new THREE.Mesh(new THREE.CylinderGeometry(r * .8, r, h, 12), m); b.position.set(ox, oy + .002, 0); s.add(b); }
      if (k === 'ledge') { const b = new THREE.Mesh(new THREE.BoxGeometry(.13, .03, .32), m); b.position.set(.03, -.015, 0); s.add(b); }   // the ledge, on the west wall
      if (k === 'shelf') {                               // a little wooden shelf on two dark brackets beside the keepsake plank, clear of the wall's rib (R5's fix 1; the lead's look, 0.53.15)
        const b = new THREE.Mesh(new THREE.BoxGeometry(.3, .035, .24), dressMat('#9a7350')); b.position.set(.09, -.0175, -.1); s.add(b);   // back edge a little into the wall
        for (const x of [-.02, .2]) { const br = new THREE.Mesh(new THREE.BoxGeometry(.025, .1, .2), dressMat('#2f3640')); br.position.set(x, -.08, -.11); s.add(br); }
      }
      if (typeof mergeMeshes === 'function') mergeMeshes(s);
      s.traverse(o => { if (o.isMesh) { o.castShadow = false; o.receiveShadow = true; } });
    }
    const hit = new THREE.Mesh(new THREE.BoxGeometry(k === 'rug' ? 1.0 : .5, k === 'rug' ? .1 : .5, k === 'rug' ? .7 : .4), HIT_MAT); hit.userData.noMerge = true;
    hit.position.set(0, k === 'rug' ? .05 : .2, 0); s.add(hit);
    const it = { t: CABIN_NAME[k], x: c[k] ? 'Your ' + c[k] + '.' : 'A spot for something of yours.', hit, g: s, front: 0, depth: .6, wall: false, cabin: k }; hit.userData.item = it;
    ITEMS.push(it); CAB.items.push(it);
  }
  if (typeof refreshPickables === 'function') refreshPickables();
}
function cabinTap(it, at) {                              // you walk up to the spot first (R5's fix 3); with no point (the checks), at once
  if (!it || !it.cabin || !cabinMine() || !cabinData()) return false;
  if (at && typeof approach === 'function') approach(at.clone(), it.front, it.depth, () => cabinPut(it)); else cabinPut(it);
  return true;
}
function cabinPut(it) {
  const k = it.cabin, c = cabinData(), P = SHIP.player; if (!c || !cabinMine()) return false;
  const fit = P.carry.find(x => CABIN_FITS[k].includes(x)), had = c[k] || null;
  if (fit) {
    if (had && P.carry.length >= CARRY_MAX && !P.carry.includes(fit)) { toast(it.t, 'Your hands are full.'); return true; }
    P.carry.splice(P.carry.indexOf(fit), 1); c[k] = fit; if (had) P.carry.push(had);
    worksSide().cabinPut = [P.bought || 0, P.crafted || 0];   // put away: section 15b's lockerTidy asks cabinPutAway()
    toast(it.t, worksText('cabin.spot.' + k, 'You put the ' + fit + ' there. It looks like yours now.') + (had ? ' The ' + had + ' is back in your hands.' : ''));
  } else if (had) {
    if (P.carry.length >= CARRY_MAX) { toast(it.t, 'Your ' + had + ' is here. Your hands are full, so it stays.'); return true; }
    delete c[k]; P.carry.push(had); toast(it.t, 'You take the ' + had + ' down. It\'s in your hands.');
  } else toast(it.t, 'Nothing in your hands fits here. Something like ' + CABIN_FITS[k].slice(0, 2).map(x => 'a ' + x).join(' or ') + ': make one in the machine shop or buy one at the crew store.');
  cabinDraw(); return true;
}
// ---- star logging ----
const STAR_FROM = 6, STAR_HOURS = [1200, 1410], STAR_TEN = 10, STAR_FRIENDS = ['sato', 'mori'];
const STAR_POINTS = ['high on the left', 'low on the left', 'just above the middle', 'just below the middle', 'high on the right', 'low on the right', 'right at the top', 'near the bottom edge'];
function starsData() {
  const S = typeof worksSide === 'function' ? worksSide() : null; if (!S) return null;
  const s = S.stars && typeof S.stars === 'object' && !Array.isArray(S.stars) ? S.stars : (S.stars = {});
  if (!Number.isInteger(s.n) || s.n < 0) s.n = 0; if (!Number.isInteger(s.last)) s.last = 0;
  return s;
}
const starsLogged = () => { const s = starsData(); return s ? s.n : 0; };   // Day 19's lesson (M20) reads it
function starSky(d) {                                    // tonight's three points (in the eyepiece's order) and which one is new
  const idx = STAR_POINTS.map((p, i) => [schedU(d, i, 1024), i]).sort((a, b) => a[0] - b[0]).slice(0, 3).map(x => x[1]);
  return { pts: idx.map(i => STAR_POINTS[i]), fresh: Math.floor(schedU(d, 0, 1025) * 3) };
}
function starCue(id, flag, fb) {                         // their own cue line (the writer's kind 'cue'), else the stand-in
  try { const v = typeof VOICE !== 'undefined' && VOICE[id], e = v && v.lines && (v.lines.cue || []).find(x => x.flag === flag), who = typeof linesWho === 'function' ? linesWho(id) : null;
    if (e) return who && typeof linesFill === 'function' ? linesFill(e.text, who, { t: shipNow(), flags: { [flag]: true } }) : e.text; } catch (e) { /* the stand-in */ }
  return fb;
}
function starLog(it) {
  const s = starsData(), d = worksDay(shipNow()); if (!s) return false;
  const sky = starSky(d), chart = sky.pts.filter((p, i) => i !== sky.fresh);
  return deviceChoose({ title: worksText('star.title', 'Star log'), text: worksText('star.pick', 'Your chart shows two stars here: {a} and {b}. Through the eyepiece there are three. Which one is new?', { a: chart[0], b: chart[1] }),
    choices: sky.pts.map(p => p.charAt(0).toUpperCase() + p.slice(1)) }, i => {
    if (i < 0) return;
    if (i !== sky.fresh) { toast(worksText('star.title', 'Star log'), worksText('star.wrong', 'That one\'s already on the chart. Look again.')); return; }
    s.n++; s.last = d; const name = worksText('star.name', 'Wren {n}', { n: s.n });
    toast(worksText('star.title', 'Star log'), worksText('star.right', 'Logged: {star}. Survey will see it in the morning.', { star: name }));
    if (s.n % 3 === 0) { const id = STAR_FRIENDS[(s.n / 3 - 1) % 2]; if (typeof relAdd === 'function') relAdd(id, 'help', 6); worksSay(id, starCue(id, 'stars.talk', 'Your star log came through. Keep them coming: you\'ve a good eye.')); }
    if (s.n >= STAR_TEN && SHIP.works && Array.isArray(SHIP.works.ms) && !SHIP.works.ms.some(x => x[0] === 'stars')) { SHIP.works.ms.push(['stars', d]); toast(worksText('star.title', 'Star log'), worksText('star.done', 'Ten stars logged. Survey has put your name in the catalogue.')); }
  });
}
function starTap(it, at) {
  if (typeof deckDef === 'undefined' || deckDef.num !== 2 || !/telescope/i.test(it.t) || roomAt(...cellAt(at.x, at.z)) !== 'J') return false;
  const s = starsData(), now = shipNow(), d = worksDay(now), m = now - (d - 1) * 1440;
  if (!s || d < STAR_FROM || m < STAR_HOURS[0] || m > STAR_HOURS[1] || s.last === d) return false;   // not now: the telescope does what it always did
  approach(at.clone(), it.front, it.depth, () => { if (!starLog(it)) toast(it.t, 'Your device is busy; try again in a moment.'); });
  return true;
}
if (typeof PLAYER_TAPS !== 'undefined') PLAYER_TAPS.unshift(cabinTap, starTap);
if (typeof WORK_TICKS !== 'undefined') WORK_TICKS.push(now => {   // the cabin's things on the deck; 06:00: waking in a cabin that feels like yours
  cabinDraw();
  const d = worksDay(now), m = Math.floor(now - (d - 1) * 1440), c = cabinData();
  if (m === 360 && c && CAB.woke !== d && cabinMood() && typeof playerBed === 'function' && playerBed() === '4-23') { CAB.woke = d; if (typeof leisureAdd === 'function') leisureAdd(4, 'cabin'); }
});
// visitors notice (E4, 0.53.11): crew in your cabin while you're there say something about what's in it (the writer's bank
// cabin.remark, by flag: cabin.lamp, .rug, .plant, .shelf, .made with two or more things you made), each once a day, one
// every few minutes at most; a bubble. Not saved (a reload may let someone say it again)
const CAB_REMARK = { day: 0, said: new Set(), at: -99 };
function cabinRemark(now) {
  if (typeof deckDef === 'undefined' || deckDef.num !== 4 || !cabinMine() || typeof DECK_CREW === 'undefined' || typeof lineFor !== 'function' || now - CAB_REMARK.at < 5) return;
  const c = cabinData(), room = DECKS[4].cabinSpots['4-23'].room || 'W'; if (!c || !Object.keys(c).length || roomAt(...player.here()) !== room) return;
  const d = worksDay(now); if (CAB_REMARK.day !== d) { CAB_REMARK.day = d; CAB_REMARK.said = new Set(); }
  const a = DECK_CREW.find(x => x.p && !CAB_REMARK.said.has(x.p.id) && roomAt(...x.here()) === room); if (!a) return;
  const made = Object.values(c).filter(x => TINKER_LIST.some(t => t.item === x)).length;
  const flags = { 'cabin.lamp': !!c.desk, 'cabin.rug': !!c.rug, 'cabin.plant': /plant/.test(c.ledge || ''), 'cabin.shelf': !!c.shelf, 'cabin.made': made >= 2 };
  const l = lineFor(a.p.id, 'cabin.remark', { t: now, flags }); CAB_REMARK.said.add(a.p.id); if (!l || !l.text) return;
  CAB_REMARK.at = now; if (typeof bubbleSay === 'function') bubbleSay(a.h, l.text, 5);
}
if (typeof WORK_TICKS !== 'undefined') WORK_TICKS.push((now, skip) => { if (!skip && !SIM_AT) cabinRemark(now); });

// =====================================================================
// 24s. THE LIFT ROOF (M17, seat E4, 0.53.x; plans/mechanics/m17-lift-roof.html on claude/p5-design)
// Thursdays 15:30-16:30 from Day 18, once you're trained: tap the main lift on the top deck (Deck 1) and choose to climb
// onto the car's roof (a hold of ROOF_CLIMB ship minutes). From then till 16:30 the car is held (section 11's liftHold):
// nobody can call it, and crew who need another deck wait by the lift on the deck they were on (roofWait, asked by
// section 14's whereIs) till 16:30, never by the ladder. The car rides slowly down the spine (the shaft, drawn lazily
// on the first ride ROOF_X m east of the deck, about 10 draw calls with the two near walls hidden; hidden after) and
// stops at each deck's guide, where you grease it (ROOF_GREASE ship minutes, the 'work' pose: 8b has no 'grease' pose
// yet). At the bottom you step off on Deck 6: Works reputation +1 (worksSideXp), a use of m17, and the lift runs a
// little smoother (its condition up ROOF_COND). Step off part way (drag away, a time skip) and you're out of the car on
// the deck it was at. The ladder row (m17, big): Halloran's Mail and a meeting at the lift at 15:30 on a Thursday he's
// on shift (WORK_MECH.m17.offer); trained at the meeting (noJob); he rides with you until stage 2 (after 2 rides).
// The writer's keys (content/works/keys-p5.md "Step 4", E3 M17): meeting train.m17.halloran-emeka; Halloran's work
// flags roof.climb, roof.grease, roof.view, roof.done; roof.held, roof.result, roof.resume (after loading a save made on the
// roof); E4's own new lines in the same style: roof.card, roof.up, roof.free (16:30). Saved in SHIP.works.side.roof = { rides, last, on? } (on: the day, while you're on the roof; 24 core's worksSide(); read
// defensively, so old saves load); the hold itself isn't saved: a save mid-ride loads with you on the top deck (where you
// stood in the car), the lift let go, and roof.resume says so. No R(); every colour through col() (std); no keys.
const ROOF_FROM = 18, ROOF_WD = 3, ROOF_HOURS = [930, 990], ROOF_CLIMB = 1, ROOF_GREASE = 1, ROOF_DROP = 2, ROOF_WHO = 'halloran-emeka', ROOF_COND = 6;
const ROOF_X = 400, ROOF_DH = 4, ROOF_W = 3, ROOF_D = 4, ROOF_FADE = .4;   // the shaft: this far east of the deck, a deck every 4 m, the car's well 3 m by 4
const roofDecks = () => DECK_ORDER.filter(n => DECKS[n]);   // top to bottom (the rec deck only when it's on)
const roofLen = () => { const n = roofDecks().length; return ROOF_CLIMB + n * ROOF_GREASE + (n - 1) * ROOF_DROP; };
function roofData() {
  const S = typeof worksSide === 'function' ? worksSide() : null; if (!S) return null;
  const r = S.roof && typeof S.roof === 'object' && !Array.isArray(S.roof) ? S.roof : (S.roof = {});
  for (const k of Object.keys(r)) if (k !== 'rides' && k !== 'last' && k !== 'on') delete r[k];
  if (!Number.isInteger(r.rides) || r.rides < 0) r.rides = 0; if (!Number.isInteger(r.last) || r.last < 0) r.last = 0; if ('on' in r && !Number.isInteger(r.on)) delete r.on;
  return r;
}
const roofTrained = () => !!(SHIP.works && SHIP.works.tr && SHIP.works.tr.m17 !== undefined);
const roofMate = () => roofTrained() && worksStage('m17') < 1 && schedPeople().some(p => p.id === ROOF_WHO);   // Halloran rides with you till stage 2
function roofOpen(t = shipNow()) {                       // can you climb on now? (a Thursday, trained, from 15:30 while there's time for the whole spine, once a day)
  const d = worksDay(t), m = t - (d - 1) * 1440;
  if (!roofTrained() || d < ROOF_FROM || weekday(d) !== ROOF_WD || m < ROOF_HOURS[0] || m > ROOF_HOURS[1] - roofLen()) return false;
  const r = roofData(); return !!r && r.last !== d;       // (side.roof made only when it could matter)
}
function roofSay(flag, fb) { const l = worksVoice(ROOF_WHO, flag); toast(worksName(ROOF_WHO), l ? l[0] : fb); }   // a toast: his bubble would be on the deck, not in the shaft
// section 14's whereIs, while the car is held: someone whose plan has them on another deck than at the hold's start waits
// by the lift there (a lift-wait place, by their id) till it's let go. ROOF_WAIT: each one's deck at the start, per hold
const ROOF_WAIT = { of: null, at: new Map() }; let ROOF_BUSY = false;
function roofWait(p, t) {
  if (ROOF_BUSY || !p || !LIFT_HOLD) return null;
  ROOF_BUSY = true;
  try {
    const H = LIFT_HOLD; if (ROOF_WAIT.of !== H) { ROOF_WAIT.of = H; ROOF_WAIT.at = new Map(); }
    let d0 = ROOF_WAIT.at.get(p.id); if (d0 === undefined) { const w0 = whereIs(p, H.from); d0 = w0 ? w0.deck : null; ROOF_WAIT.at.set(p.id, d0); }
    const w = whereIs(p, t); if (!w || d0 == null || !DECKS[d0] || w.deck === d0) return null;
    const lw = (DECKS[d0].places || []).filter(q => q.type === 'lift-wait'), pl = lw.length ? lw[idHash(p.id) % lw.length] : null;
    return { deck: d0, act: 'off', type: 'lift-wait', placeId: pl ? pl.id : null, moving: false, from: H.from, until: H.until, tag: 'lift' };
  } finally { ROOF_BUSY = false; }
}
// the lift's door or panel (section 11's enterLift asks first): the offer on the top deck, or "held" while it is
function roofLiftTap() {
  if (typeof deckDef === 'undefined' || ACT && ACT.kind === 'roofRide') return false;
  if (deckDef.num === roofDecks()[0] && roofOpen()) {
    const shown = deviceChoose({ title: mechName('m17'), text: worksText('roof.card', 'The lift\'s maintenance hour. Climb up through the hatch and ride the roof down the spine, greasing each deck\'s guide on the way?'),
      choices: ['Climb onto the roof', 'Ride inside'] }, i => { if (i === 0) roofClimb(); else if (i === 1 && !liftHeld()) toPanel(openLiftPanel); });
    if (shown) return true;
  }
  if (liftHeld()) { toast('Main lift', worksText('roof.shut', 'Held for maintenance till 16:30. Nobody\'s going anywhere for a bit.')); return true; }
  return false;
}
function roofClimb() {                                   // into the car (its tile nearest the middle), then up through the hatch
  const mid = (ROOM_TILES['@'] || []).filter(c => free(...c)).map(c => [c, cellPos(...c)]).sort((a, b) => Math.hypot(a[1].x - LIFT_AT[0], a[1].z - LIFT_AT[1]) - Math.hypot(b[1].x - LIFT_AT[0], b[1].z - LIFT_AT[1]))[0];
  if (!mid) return false;
  actStart('roofRide', null, { title: mechName('m17'), follow: true, spot: { walk: mid[0], x: mid[1].x, z: mid[1].z, y: 0, face: player.face, pose: 'work', id: null },
    after: worksText('roof.up', 'You open the hatch in the car\'s ceiling and climb up onto the roof.') });
  return true;
}
// the shaft, made on the first ride and kept (hidden) after: the car (still), the spine (the walls, each deck's slab and
// guides, the trunks and the ladder; it rises as the car goes down), a glint on the guide you're greasing
const ROOF = { g: null, spine: null, walls: [], glint: null, mate: null, r: null, say: null };
function roofShaft() {
  if (ROOF.g) return ROOF.g;
  const n = roofDecks().length, H = (n - 1) * ROOF_DH + 28, yMid = -(n - 1) * ROOF_DH / 2 + 6, W2 = ROOF_W / 2, D2 = ROOF_D / 2;
  const M = { wall: std('#46525f', .9, 0, { emissive: col('#151b24') }), slab: std('#6b7887', .8, 0, { emissive: col('#151b24') }), rail: std('#9aa3ad', .4, .5), brass: std('#c9a24a', .5, .3), pipeA: std('#7d8c99', .5, .3), pipeB: std('#b5703d', .5, .3), pipeC: std('#4f6f8f', .6), car: std('#59636e', .7), safety: std('#d9a441', .6),
    lamp: new THREE.MeshBasicMaterial({ color: col('#ffe6a8') }) };
  const box = (grp, m, w, h, d, x, y, z) => { const b = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), m); b.position.set(x, y, z); grp.add(b); return b; };
  const cyl = (grp, m, r, h, x, y, z) => { const c = new THREE.Mesh(new THREE.CylinderGeometry(r, r, h, 10), m); c.position.set(x, y, z); grp.add(c); return c; };
  const g = new THREE.Group(); g.position.set(ROOF_X, 0, 0); scene.add(g); ROOF.g = g;
  const spine = new THREE.Group(); g.add(spine); ROOF.spine = spine;
  // four walls, each its own group (the near two are hidden each frame); n: which way it faces out from the well
  for (const [nx, nz] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
    const w = new THREE.Group(), side = nx !== 0, len = (side ? ROOF_D : ROOF_W) + 8, at = (side ? W2 : D2) + .1;
    const P = (u, y, v, sw, sh, sd) => side ? [sd, sh, sw, nx * (at - v), y, u] : [sw, sh, sd, u, y, nz * (at - v)];   // u along the wall, v in from its face
    const B = (m, u, y, v, sw, sh, sd) => { const [a, b, c, x, yy, z] = P(u, y, v, sw, sh, sd); return box(w, m, a, b, c, x, yy, z); };
    B(M.wall, 0, yMid, 0, len, side ? H + .1 : H, .2);   // (the side walls a touch taller: no shared top faces at the corners)
    for (let k = 0; k < n; k++) {
      const y0 = -k * ROOF_DH - 2.75;                     // deck k's slab, where the car's floor sits at its stop
      B(M.slab, 0, y0, .06, len + .02, side ? .3 : .28, .3);
      B(M.lamp, side ? -1.2 : -1, y0 + 2.2, .16, .3, .1, .06);
      if (side) B(M.brass, 0, y0 + 3.6, .2, .3, .32, .26);   // the guide shoes on the rails at roof height: yours west, Halloran's east
      if (!side && nz > 0) { B(M.slab, -.8, y0 + 1.26, .1, .12, 2.2, .26); B(M.slab, .8, y0 + 1.26, .1, .12, 2.2, .26); B(M.slab, 0, y0 + 2.4, .1, 1.74, .12, .26); }   // the deck's lift doors, from behind
    }
    if (side) B(M.rail, 0, yMid, .2, .12, H, .14);       // the guide rail, the whole height
    if (!side && nz < 0) {                               // the back: the spine's trunks
      for (const [u, r, m] of [[-.9, .12, M.pipeA], [-.55, .09, M.pipeB], [.75, .14, M.pipeC]]) cyl(w, m, r, H, u, yMid, -(D2 - r - .04));
      B(M.slab, .2, yMid, .08, .34, H, .14);             // a cable tray
    }
    if (side && nx > 0) {                                // the east wall: the spine ladder (two rails, a rung every 30 cm)
      for (const u of [1.3, 1.75]) B(M.rail, u, yMid, .18, .06, H, .06);
      for (let y = -H / 2 + .2; y < H / 2; y += .3) B(M.rail, 1.525, yMid + y, .18, .45, .04, .04);
    }
    mergeMeshes(w); w.traverse(o => { if (o.isMesh) o.castShadow = false; });
    spine.add(w); ROOF.walls.push({ g: w, n: [nx, nz] });
  }
  // the car: its roof at y 0 (a hatch, the safety rail along three sides, a work lamp), its body below
  const car = new THREE.Group(); g.add(car);
  box(car, M.car, ROOF_W - .5, 2.6, ROOF_D - .5, 0, -1.3, 0);
  box(car, M.slab, .8, .04, .8, .35, .02, .6);
  for (const [x, z, w, d] of [[0, -(D2 - .3), ROOF_W - .6, .06], [-(W2 - .3), 0, .06, ROOF_D - .6], [W2 - .3, 0, .06, ROOF_D - .6]]) { const h = w > d ? .05 : .04; box(car, M.safety, w, h, d, x, .95, z); box(car, M.safety, w, h, d, x, .5, z); }
  for (const [x, z] of [[-(W2 - .3), -(D2 - .3)], [W2 - .3, -(D2 - .3)], [-(W2 - .3), D2 - .3], [W2 - .3, D2 - .3]]) box(car, M.safety, .08, .98, .08, x, .49, z);   // (posts a touch above the rail tops: no shared faces)
  box(car, M.lamp, .22, .12, .12, 0, 1.0, -(D2 - .3));
  mergeMeshes(car); car.traverse(o => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; } });
  const gl = new THREE.Mesh(new THREE.SphereGeometry(.12, 10, 8), new THREE.MeshBasicMaterial({ color: col('#fff3c4') })); gl.visible = false; g.add(gl); ROOF.glint = gl;
  return g;
}
// the ride, each frame of the activity (section 15's def.until): climb, fade, grease and drop deck by deck, fade, out on the bottom deck
Object.assign(PLAYER_ACTS, { roofRide: { mins: 600, pose: 'work', title: 'The lift roof', until: roofStep } });
function roofStep(A) {
  const now = performance.now(), R = A.o.r || (A.o.r = { st: 'climb', k: 0, t0: 0, real: now, said: {} }), rt = (now - R.real) / 1000;
  const dt = Math.min(.1, (now - (R.last || now)) / 1000); R.last = now;
  const decks = roofDecks(), n = decks.length, to = st => { R.st = st; R.real = now; R.t0 = A.done; };
  if (R.st === 'climb') {
    if (A.done >= ROOF_CLIMB) {
      const d = worksDay(shipNow()), rd = roofData(); if (!liftHeld()) liftHold(true, (d - 1) * 1440 + ROOF_HOURS[1]);   // (back on after stepping off: the same hold, its start too, so nobody jumps decks)
      ROOF.r = R; R.mate = roofMate(); if (rd) rd.on = d;   // on: a save from now has you back at the top (roof.resume)
      if (R.mate) roofSay('roof.climb', 'Clip on, hands inside the rail. I\'ll take the east guides, you take the west.');
      to('dark');
    }
  } else if (R.st === 'dark') {
    fadeEl.style.opacity = Math.min(1, rt / ROOF_FADE);
    if (rt >= ROOF_FADE) {
      roofShaft().visible = true; ROOF.spine.position.y = 0; R.inShaft = true;
      A.x = ROOF_X - .8; A.z = 0; A.y = 0; A.face = -Math.PI / 2; target.x = A.x; target.z = A.z;
      to('light');
    }
  } else if (R.st === 'light') {
    fadeEl.style.opacity = Math.max(0, 1 - rt / ROOF_FADE);
    if (rt >= ROOF_FADE) { fadeEl.style.opacity = 0; to('grease'); }
  } else if (R.st === 'grease') {
    A.pose = 'work'; A.face = -Math.PI / 2;
    ROOF.glint.visible = Math.floor(rt * 3) % 2 === 0; ROOF.glint.position.set(-(ROOF_W / 2 - .3), .85, 0);
    if (A.done - R.t0 >= ROOF_GREASE) {
      ROOF.glint.visible = false;
      if (R.mate && R.k === 0) roofSay('roof.grease', 'One long stroke down the shoe. Not too much: it only drips on the next car.');
      to(R.k >= n - 1 ? 'end' : 'drop');
    }
  } else if (R.st === 'drop') {
    A.pose = 'stand'; const p = Math.min(1, (A.done - R.t0) / ROOF_DROP);
    ROOF.spine.position.y = (R.k + p * p * (3 - 2 * p)) * ROOF_DH;
    if (R.mate && R.k === 1 && p >= .5 && !R.said.view) { R.said.view = 1; roofSay('roof.view', 'Look up. Seven decks of her, and nobody else gets to see it like this.'); }
    if (p >= 1) { R.k++; to('grease'); }
  } else if (R.st === 'end') {
    if (!R.done) { R.done = true; roofDone(R); }
    fadeEl.style.opacity = Math.min(1, rt / ROOF_FADE);
    if (rt >= ROOF_FADE && !R.off) {                      // out on the bottom deck, by section 11's ride from its darkest point
      R.off = true; A.o.follow = false; ROOF.g.visible = false; roofMateGone();
      ride = { n: decks[n - 1], t: RIDE.dark - .01, at: null, face: -Math.PI / 2, swapped: false };
    }
  }
  if (R.inShaft && !R.off) roofMateStep(A, R, dt);
  return false;                                          // never by itself: the deck change (or stepping off) ends it
}
function roofMateStep(A, R, dt) {                        // Halloran on the roof beside you, on the east guides
  if (!R.mate) return;
  if (!ROOF.mate) { const p = schedPeople().find(q => q.id === ROOF_WHO); if (!p) { R.mate = false; return; } ROOF.mate = new FullPerson(rosterSpec(p), p.id); }
  const g = R.st === 'grease';
  ROOF.mate.set({ x: ROOF_X + .8, y: 0, z: .3 }, g ? Math.PI / 2 : Math.atan2(A.x - ROOF_X - .8, A.z - .3), g ? 'work' : 'stand');
  ROOF.mate.update(dt, performance.now() / 1000);
}
function roofMateGone() { if (ROOF.mate) { ROOF.mate.dispose(); ROOF.mate = null; } }
function roofDone(R) {                                   // every guide greased: the ride counts, the lift runs smoother
  const r = roofData(), d = worksDay(shipNow()); if (!r) return;
  r.rides++; r.last = d; delete r.on;
  if (typeof worksUse === 'function') worksUse('m17');
  if (typeof worksSideXp === 'function') worksSideXp(1, 'roof');
  if (typeof machinesNow === 'function') {
    machinesNow(); const s = SHIP.machines && SHIP.machines['5-mainlift-1'];
    if (s) { s.cond = Math.min(100, s.cond + ROOF_COND); s.state = machineState(s.cond); MACH_REV++; if (MACH_HOUR !== null) machRecord(MACH_HOUR - 1); }
  }
  const l = R.mate && worksVoice(ROOF_WHO, 'roof.done');
  ROOF.say = R.mate ? [worksName(ROOF_WHO), l ? l[0] : 'That\'s her done for the week. Hear how quiet she runs now? Good work.']
    : [mechName('m17'), worksText('roof.result', 'Every guide greased, top to bottom. The lift runs a little smoother.')];
}
// each frame: only the far walls show; stepped off part way (dragged away, a time skip), you're out of the car on the
// deck it was at; once the ride's over, the last word
function roofFrame() {
  requestAnimationFrame(roofFrame);
  if (ROOF.say && typeof ride !== 'undefined' && !ride) { const [a, b] = ROOF.say; ROOF.say = null; toast(a, b); }
  { const R = ROOF.r; if (R && !R.off && !R.inShaft && !(ACT && ACT.kind === 'roofRide' && ACT.o.r === R)) {   // ended in the fade before the shaft (R5): no shaft to leave, just undo the fade
    R.off = true; if (!ride) fadeEl.style.opacity = 0; const rd = roofData(); if (rd) delete rd.on; } }
  if (!ROOF.g || !ROOF.g.visible) return;
  const A = ACT, R = ROOF.r;
  if (A && A.kind === 'roofRide' && A.o.r === R && R.inShaft && !R.off) {
    const cx = Math.sin(az), cz = Math.cos(az);
    for (const w of ROOF.walls) w.g.visible = w.n[0] * cx + w.n[1] * cz < .25;
    return;
  }
  ROOF.g.visible = false; roofMateGone();
  if (R && R.inShaft && !R.off) {
    R.off = true; fadeEl.style.opacity = 1; target.copy(player.obj.position).setY(.7); const rd = roofData(); if (rd) delete rd.on;
    if (!ride) ride = { n: roofDecks()[Math.min(R.k, roofDecks().length - 1)], t: RIDE.dark - .01, at: null, face: player.face, swapped: false };
  }
}
requestAnimationFrame(roofFrame);
if (typeof WORK_TICKS !== 'undefined') WORK_TICKS.push(now => {   // 16:30: the car's let go (section 11 keeps the hold's record); loaded from a save made on the roof: back at the top
  if (LIFT_HOLD && LIFT_HOLD.until <= now && LIFT_HOLD.until > now - 2 && !LIFT_HOLD.said && !SIM_AT) { LIFT_HOLD.said = true; toast('Main lift', worksText('roof.free', 'Half four: the lift\'s back in service.')); }
  // (read only: no side.roof in saves that never rode)
  const S = worksSide(), rd = S && S.roof && S.roof.on !== undefined ? roofData() : null; if (rd && rd.on !== undefined && !(ROOF.r && !ROOF.r.off)) { delete rd.on; if (!SIM_AT) toast(mechName('m17'), worksText('roof.resume', 'You\'d saved on the lift roof. You\'re back at the top deck.')); }
  const o = typeof OCCASIONS !== 'undefined' && OCCASIONS['works.m17']; if (o && (o.deck !== 1 || o.room !== '+')) { o.deck = 1; o.room = '+'; }   // after a reload trainSetup makes it in the Works bay
});
// crew waiting by the held lift say so now and then (the writer's bank roof.wait): someone roofWait keeps on your deck,
// within 8 m of you, one every 6 ship minutes at most, each once a hold; a bubble (E4, 0.53.11)
const ROOF_TALK = { of: null, said: new Set(), at: -99 };
function roofTalk(now) {
  if (!liftHeld(now) || ROOF.r && !ROOF.r.off || typeof DECK_CREW === 'undefined' || typeof lineFor !== 'function' || now - ROOF_TALK.at < 6) return;
  if (ROOF_TALK.of !== LIFT_HOLD) { ROOF_TALK.of = LIFT_HOLD; ROOF_TALK.said = new Set(); }
  const p = player.obj.position, a = DECK_CREW.find(x => x.p && !ROOF_TALK.said.has(x.p.id) && Math.hypot(x.x - p.x, x.z - p.z) < 8 && roofWait(x.p, now)); if (!a) return;
  ROOF_TALK.said.add(a.p.id); const l = lineFor(a.p.id, 'roof.wait', { t: now, keep: e => !/stairs/i.test(e.text || '') });   // (the lead's call: nobody takes the ladder, so W2's "Stairs it is" line is left out)
  if (!l || !l.text) return;   // (merge fix, 0.63.4: this guard sat inside the comment above)
  ROOF_TALK.at = now; if (typeof bubbleSay === 'function') bubbleSay(a.h, l.text, 5);
}
if (typeof WORK_TICKS !== 'undefined') WORK_TICKS.push((now, skip) => { if (!skip && !SIM_AT && LIFT_HOLD) roofTalk(now); });
onSim('newGame', () => { LIFT_HOLD = null; ROOF.r = null; ROOF.say = null; });
// the ladder row: Halloran's ask is for a Thursday he's on shift, at the lift on Deck 1 at 15:30; trained at the meeting
if (typeof WORK_MECH !== 'undefined') WORK_MECH.m17 = {
  noJob: true,
  offer(row, c, d, t) {
    const m = t - (d - 1) * 1440, by = ROOF_WHO;
    if (weekday(d) !== ROOF_WD || m > ROOF_HOURS[0] - 30 || !occOnShift(by, d)) return false;   // not a Thursday (it asks again tomorrow, and so on)
    const sid = 'train.m17.' + by;
    if (!MEETING_SCRIPTS[sid]) MEETING_SCRIPTS[sid] = { title: row.name, from: worksName(by), stub: true,
      gist: worksFirst(by) + ' waited for you at the lift. The roof will keep: next Thursday.',
      lines: [{ who: by, text: 'Thursday, half three: the lift\'s maintenance hour. The car\'s ours till half four.' },
        { who: by, text: 'We ride the roof down the spine and grease every guide on the way. Up through the hatch: after you.' }] };
    const o = trainSetup(row); o.by = by; o.deck = 1; o.room = '+'; o.script = sid;
    const r = occasionAdd('works.m17', (d - 1) * 1440 + ROOF_HOURS[0], true, 20); if (!r) return false;
    c.by = by; c.d = d; c.w = 0; c.st = 'meet'; c.occ = r.key; c.told = false;
    const ask = worksText('works.ask.m17', '', { time: hhmm(ROOF_HOURS[0]), place: 'the Bridge lobby on Deck 1', name: worksName(by) }), cut = ask.indexOf(' | ');
    let subject = 'Training: ' + mechName('m17'), body = 'It\'s the lift\'s maintenance hour on Thursday afternoons. Meet me at the lift on Deck 1 at ' + hhmm(ROOF_HOURS[0]) + ': we\'re riding the roof.';
    if (cut > 0) { subject = ask.slice(0, cut); body = ask.slice(cut + 3); }
    if (typeof mailSend === 'function') mailSend({ at: t, from: worksName(by), subject, body, quiet: true });
    c.mail = subject.slice(0, 80);
    if (t >= shipNow() - 1) trainTell(row, c);
    return true;
  },
};

