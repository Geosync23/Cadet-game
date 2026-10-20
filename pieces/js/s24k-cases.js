// =====================================================================
// 24k. CASES: head-scratchers (Pillar 5, seat H, 0.55.x; plans/mechanics/case-engine.html on claude/p5-design)
// Some faults don't show their cause. A real fault at your tier may become a case when section 17 posts it
// (caseOffer(j, h), one line there): its suspects are the cause and decoys from FAULT_CAUSES (section 17.4), its
// clues come from what really happened on the ship, and each clue rules out (kills) some suspects. The solver
// (caseSolve) checks there's exactly one answer, that it needs thinking and that every clue can be reached; then the
// case is frozen in SHIP.works.cases and never checked again. Fault notes (a tab of 24 core's Works app, or its own
// app until that exists) shows it; you collect clues by going to them (caseTick) and cross suspects out yourself;
// Call it (caseCall) sets the job's part and the job's normal loop runs. A wrong call shows when you fit the part
// (caseFitted, from section 17's jobStepDone); the job is held for you till your shift ends (caseHeld, from
// heldForYou), then goes to the crew, who do it the long way. Puzzle kinds register in CASE_KINDS: { name, ladder,
// fits(cause, m), suspects(j, seed, band), clues(j, cause, sus, seed, band), view(c), hint(c), text?(c, clue),
// tick?(c, j) }; the engine knows none of them, and is inert until one is opened (its ladder row opened:
// worksIsOpen(ladder)). Pure functions and state: nothing here calls R() or makes 3D objects.
// Hash keys 880 (the rate roll), 881 (which kind), 882-889 (the eight sub-seeds), 892 (caseDecoys' order, for the
// kinds), 893 (the order suspects are shown in); 890-891 and 1002 are P3's, 1000-1001 and 894 P1's and P2's (1003-1004 spare).
// =====================================================================
const CASE_KINDS = {};
const CASE_BANDS = {                                    // suspects, clues (reachable), the fewest clues that solve it, decks
  T1: { sus: [3, 4], clues: [2, 3], fewest: 2, decks: 1 },    // Junior (Days 5-9)
  T2: { sus: [3, 5], clues: [3, 4], fewest: 3, decks: 2 },    // Officer
  T3: { sus: [5, 6], clues: [4, 6], fewest: 3, decks: 3 },    // Senior Officer
  T4: { sus: [5, 6], clues: [4, 6], fewest: 3, decks: 3 } };  // Engine Specialist
const CASE_RANK_BAND = { junior: 'T1', officer: 'T2', senior: 'T3', specialist: 'T4' };
const CASE_RATE = { junior: .1, officer: .2, senior: .25, specialist: .33 }, CASE_MAX = { junior: 1, officer: 1, senior: 2, specialist: 2 };
const CASE_WAIT_MAX = 3 * 1440;                         // a case still waiting (P3's tries) after three days is a plain repair
const CASE_TRIES = 8, CASE_DONE_KEEP = 20, CASE_SPENT = new Set(['seal', 'cartridge', 'filter', 'membrane', 'oxygen cell', 'uv lamp']);   // from Tier 2 a wrong call's consumable is used up (the T2 band: the user's seal or cartridge, and the other NO_MAKE parts)
const CASE_STATS = { offered: 0, rolled: 0, posted: 0, fallback: 0, ms: 0, why: {} };   // for puzzle_check
const caseRank = () => (SHIP.works && SHIP.works.rank) || 'junior';
const caseBand = rank => CASE_RANK_BAND[rank] || 'T1';
// a band's limits for a kind: its own (kind.bands[band], from its page: P2's T2 needs two witnesses, P3 keeps T1's size), else the engine's
const caseBandOf = (kid, band) => { const K = CASE_KINDS[kid]; return K && K.bands && K.bands[band] || CASE_BANDS[band] || CASE_BANDS.T1; };
const caseRate = (rank, ownTier) => rank === 'senior' && ownTier >= 3 ? .33 : CASE_RATE[rank] || CASE_RATE.junior;
const caseTier = () => typeof playerTier === 'function' ? playerTier() : PLAYER_TIER;
const caseNow = () => SIM_AT != null ? SIM_AT : shipNow();   // inside section 17's hour, that hour
const caseApp = () => typeof worksTabAdd === 'function' ? 'works' : 'faultnotes';
const caseCauses = m => (typeof FAULT_CAUSES !== 'undefined' && m && FAULT_CAUSES[m.kind]) || [];
// a kind is opened once its ladder row has opened (24 core's worksIsOpen, else SHIP.works.op lists it; not trained:
// tr.p3 is only set once the training case is solved), or by its own open()
const caseOpened = id => { const K = CASE_KINDS[id]; try { if (K.open) return !!K.open(); if (typeof worksIsOpen === 'function') return !!worksIsOpen(K.ladder);
  return Object.values((SHIP.works && SHIP.works.op) || {}).some(ids => Array.isArray(ids) && ids.includes(K.ladder)); } catch (e) { return false; } };
const caseKindsOpen = () => Object.keys(CASE_KINDS).sort().filter(caseOpened);
// the cases (SHIP.works.cases = { open: [frozen case], done: [[id, day, flags]], n }), cleaned once the first time
// they're asked for: from 24 core's copy, or the save's own (a cleaner there may drop keys it doesn't know)
let CASE_SAVED = SAVED && SAVED.ship && SAVED.ship.works && SAVED.ship.works.cases || null, CASE_CLEAN = false;
function caseState() {
  const W = SHIP.works; if (!W || typeof W !== 'object') return null;
  if (!CASE_CLEAN || !W.cases) { W.cases = caseClean(W.cases || CASE_SAVED); CASE_SAVED = null; CASE_CLEAN = true; }
  return W.cases;
}
function caseClean(x) {
  const out = { open: [], done: [], n: 0 }, o = x && typeof x === 'object' ? x : {}, ids = a => Array.isArray(a) ? a.filter(s => typeof s === 'string').slice(0, 8) : [];
  out.n = Number.isInteger(o.n) && o.n >= 0 ? o.n : 0;
  if (typeof o.first === 'string') out.first = o.first;  // Day 5's training case: its id once staged, 'none' if there won't be one
  for (const k of ['p1', 'p2']) if (typeof o[k] === 'string') out[k] = o[k].slice(0, 80);   // P1's and P2's first cases, the same way (0.55.14)
  if (o.said && typeof o.said === 'object' && Number.isInteger(o.said.p2)) out.said = { p2: Math.max(0, o.said.p2) };   // Tomas's word (P2), kept here too (0.55.15)
  if (Array.isArray(o.done)) out.done = o.done.filter(d => Array.isArray(d) && typeof d[0] === 'string' && Number.isInteger(d[1]) && Number.isInteger(d[2])).slice(-CASE_DONE_KEEP);
  for (const c of Array.isArray(o.open) ? o.open : []) {
    if (!c || typeof c.id !== 'string' || typeof c.job !== 'string' || !CASE_KINDS[c.kind] || typeof c.cause !== 'string') continue;
    const j = SHIP.jobs.find(y => y.id === c.job); if (!j || j.status === 'done') continue;   // the case's job is gone: so is the case
    const clues = (Array.isArray(c.clues) ? c.clues : []).filter(k => k && typeof k.id === 'string' && typeof k.type === 'string')
      .map(k => ({ id: k.id, type: k.type, src: k.src && typeof k.src === 'object' ? k.src : {}, at: typeof k.at === 'string' ? k.at : null, kills: ids(k.kills) }));
    const sus = ids(c.sus); if (!sus.includes(c.cause) || (!clues.length && !(c.wait && c.train && c.kind === 'p2'))) continue;   // P2's first finds its witnesses when it shows
    const keep = a => ids(a).filter(s => sus.includes(s)), cl = clues.map(k => k.id);
    out.open.push({ id: c.id, job: c.job, kind: c.kind, k: Number.isInteger(c.k) ? c.k : 0, band: CASE_BANDS[c.band] ? c.band : 'T1', cause: c.cause, sus,
      fewest: Number.isInteger(c.fewest) ? c.fewest : 2, clues, got: ids(c.got).filter(s => cl.includes(s)), crossed: keep(c.crossed), known: keep(c.known), calls: keep(c.calls),
      fits: Number.isInteger(c.fits) ? c.fits : 0, ...(ids(c.doubt).some(s => cl.includes(s)) ? { doubt: ids(c.doubt).filter(s => cl.includes(s)) } : {}), posted: isFinite(c.posted) ? +c.posted : 0, until: isFinite(c.until) ? +c.until : 0, by: typeof c.by === 'string' ? c.by : undefined, m7: c.m7 ? true : undefined, wait: !!c.wait, taken: !!c.taken, talk: !!c.talk, long: !!c.long, train: !!c.train, told: !!c.told, title: typeof c.title === 'string' ? c.title : '' });
    if (!j.case) j.case = c.id;
  }
  return out;
}
SAVE_EXTRA.push(s => { const c = SHIP.works && SHIP.works.cases; if (c) (s.ship.works = s.ship.works || {}).cases = c; });
onSim('newGame', () => { CASE_SAVED = null; CASE_CLEAN = false; CASE_UI.ask = null; CASE_UI.at = null; });
const caseOf = j => { const C = j && j.case && SHIP.works && caseState(); return C ? C.open.find(c => c.id === j.case) || null : null; };
const caseById = id => { const C = SHIP.works && caseState(); return C ? C.open.find(c => c.id === id) || null : null; };
const caseJob = c => SHIP.jobs.find(j => j.id === c.job) || null;
// a suspect in words: { id, label, part, still } from the machine's fault table, else the kind's own (a junction, a setting)
function caseSus(c, id) {
  const j = caseJob(c), m = j && machineById(j.machine), f = caseCauses(m).find(x => x.id === id), K = CASE_KINDS[c.kind];
  const own = K && K.sus ? K.sus(c, id) : null;          // the kind's own words first (P1 names each suspect's machine), else the table's
  if (own) return { id, label: own.label || id, part: own.part || null, still: own.still || null };
  return { id, label: f && (f.name || f.label) || (f && f.part) || id, part: f && f.part || null, still: f && f.still || null, shows: f && f.shows };
}
// decoys for a kind: the machine's other causes with the same card, in an order fixed by the seed (no R())
function caseDecoys(m, cause, seed, ok) {
  const all = caseCauses(m), c = all.find(x => x.id === cause); if (!c) return [];
  return all.filter(x => x.id !== cause && x.shows === c.shows && (!ok || ok(x))).map((x, i) => [schedU(seed, i, 892), x.id]).sort((a, b) => a[0] - b[0]).map(x => x[1]);
}

// ---- posting: section 17 calls caseOffer(j, h) where a repair or overhaul gets its j.cause ----
function caseOffer(j, h) {
  if (!j || !j.machine || j.case || j.reserved || (j.kind !== 'repair' && j.kind !== 'overhaul')) return;
  const kinds = caseKindsOpen(); if (!kinds.length) return;
  if (!SHIP.works && typeof worksInit === 'function') worksInit();
  const C = caseState(); if (!C) return;
  const old = C.open.find(c => c.job === j.id); if (old) { j.case = old.id; return; }   // the machines replayed from an earlier hour: the same job, the same case
  const d = Math.floor(h / 24) + 1, hr = h % 24, m = machineById(j.machine), cause = caseCauses(m).find(x => x.id === j.cause);
  if (!m || !cause || hr < 6 || hr >= 15 || !playerShiftOn(d) || (typeof eventDay === 'function' && eventDay(d))) return;
  const rank = caseRank(), own = m.tier || MACHINE_KINDS[m.kind].tier;
  if (jobTier(j) > caseTier() || C.open.length >= (CASE_MAX[rank] || 1)) return;
  const fit = kinds.filter(id => { try { return !!CASE_KINDS[id].fits(cause, m); } catch (e) { return false; } });
  if (!fit.length) return;
  CASE_STATS.offered++;
  if (schedU(machSeed(j.machine), d, 880) >= caseRate(rank, own)) return;
  CASE_STATS.rolled++;
  // which kind: the newest-opened one counts double for its first week
  const opened = {}; for (const [dy, ids] of Object.entries((SHIP.works && SHIP.works.op) || {})) for (const x of Array.isArray(ids) ? ids : []) if (!(x in opened)) opened[x] = +dy;
  const tr = opened, newest = Math.max(...fit.map(id => tr[CASE_KINDS[id].ladder] ?? -1));   // the day each row opened
  const w = fit.map(id => { const t = tr[CASE_KINDS[id].ladder]; return t === newest && t >= 0 && d - t < 7 ? 2 : 1; }), sum = w.reduce((a, b) => a + b, 0);
  let u = schedU(machSeed(j.machine), d, 881) * sum, kid = fit[fit.length - 1];
  for (let i = 0; i < fit.length; i++) { if (u < w[i]) { kid = fit[i]; break; } u -= w[i]; }
  const t0 = typeof performance !== 'undefined' ? performance.now() : 0;
  let c = null;
  for (let k = 0; k < CASE_TRIES && !c; k++) {
    const r = caseMake(j, kid, k, d);
    if (r.why) CASE_STATS.why[r.why] = (CASE_STATS.why[r.why] || 0) + 1; else c = r.c;
  }
  if (t0) CASE_STATS.ms = Math.max(CASE_STATS.ms, performance.now() - t0);
  if (!c) { CASE_STATS.fallback++; return; }             // no fair case: a plain fault
  CASE_STATS.posted++; C.n++;
  if (c.band !== 'T1' && !c.by) c.by = caseTalker(d);    // from the T2 band you talk it through with Torres when he's on, else Calder or Halloran
  C.open.push(c); j.case = c.id;
  if (!c.wait) caseShow(c, j);
}
const CASE_TALK = ['torres-zeke', 'calder', 'halloran-emeka'];
const caseTalker = d => CASE_TALK.find(id => { try { return occOnShift(id, d); } catch (e) { return false; } }) || 'calder';
// one try at a case (k = 0..7, key 882 + k): suspects and clues from the kind, then the solver. -> { c } | { why }
function caseMake(j, kid, k, d) {
  const K = CASE_KINDS[kid], seed = schedU(machSeed(j.machine), d, 882 + k) * 4294967296 | 0, band = caseBand(caseRank()), cause = j.cause;
  let sus, clues;
  try { sus = K.suspects(j, seed, band); clues = K.clues(j, cause, sus, seed, band); } catch (e) { return { why: 'kind' }; }
  if (!Array.isArray(sus) || !Array.isArray(clues)) return { why: 'kind' };
  sus = sus.map((s, i) => [schedU(seed, i, 893), s]).sort((a, b) => a[0] - b[0]).map(x => x[1]);   // shown in an order that gives nothing away (key 893)
  const r = caseSolve(sus, clues, band, cause, kid);
  if (r.why) return r;
  const t = caseNow();
  return { c: { id: 'c' + j.id, job: j.id, kind: kid, k, band, cause, sus: sus.slice(), fewest: r.fewest,
    clues: clues.map(x => ({ id: x.id, type: x.type, src: x.src || {}, at: x.at || null, kills: x.kills.slice() })),
    got: [], crossed: [], known: [], calls: [], posted: t, until: 0, wait: !!(K.wait && K.wait(j)), taken: false, talk: false, long: false, train: !!j.train, told: false, title: '' } };
}
// on the board: the head-scratcher card, held for you to the end of the shift it appears in
function caseShow(c, j) {
  const t = caseNow(), m = machineById(j.machine), f = caseCauses(m).find(x => x.id === c.cause);
  c.wait = false; c.until = Math.floor(t / 1440) * 1440 + DAY_SHIFT[1]; c.posted = t;
  j.parts = []; j.stepsDone = (j.stepsDone || []).filter(k => k !== 0);   // the part is yours to find
  const shows = f && f.shows || 'acts up', fb = 'Head-scratcher: ' + caseMachName(j) + ' ' + shows;
  c.title = (typeof worksText === 'function' && worksText('case.title', null) || '').replace('{machine}', caseMachName(j)).replace('{shows}', shows).replace(/\.$/, '') || fb;   // a card's title: no full stop
  const K = CASE_KINDS[c.kind]; let kt = null; try { kt = K && K.title ? K.title(c, j) : null; } catch (e) { kt = null; }   // a kind's own (P1: the line's symptom, not the machine)
  if (kt) c.title = String(kt).replace(/\.$/, '');
  if (!/^Head-scratcher/.test(c.title)) c.title = 'Head-scratcher: ' + c.title;
  j.title = c.title;
}

// ---- the solver: exactly one answer, needs thinking, every clue reachable, in its band. -> { fewest } | { why } ----
function caseSolve(sus, clues, band, cause, kid) {
  const B = caseBandOf(kid, band), n = clues.length;
  if (!sus.includes(cause) || new Set(sus).size !== sus.length || sus.length < B.sus[0] || sus.length > B.sus[1]) return { why: 'suspects' };
  if (n < B.clues[0] || n > B.clues[1] || n > 6 || clues.some(c => !c || !Array.isArray(c.kills))) return { why: 'clues' };
  if (clues.some(c => c.kills.includes(cause))) return { why: 'answer' };
  const left = mask => { let k = 0; for (const s of sus) if (!clues.some((c, i) => (mask >> i & 1) && c.kills.includes(s))) k++; return k; };
  if (left((1 << n) - 1) !== 1) return { why: 'answer' };
  let fewest = 99;
  for (let mask = 1; mask < 1 << n; mask++) if (left(mask) === 1) { let b = 0; for (let x = mask; x; x >>= 1) b += x & 1; fewest = Math.min(fewest, b); }
  if (fewest < B.fewest) return { why: 'easy' };
  if (new Set(clues.map(caseClueDeck).filter(x => x != null)).size > B.decks) return { why: 'decks' };
  if (!clues.every(caseReachable)) return { why: 'reach' };
  return { fewest };
}
// where a clue is: a place id (its deck counts), 'board' (taped to the job: the board doesn't count as a deck), or a person
const caseClueDeck = c => { if (!c.at || c.at === 'board') return null; const p = placeById(c.at); return p ? p.deck : -1; };
function caseReachable(c) {
  if (c.at && c.at !== 'board') { const p = placeById(c.at); if (!p || placeTier(c.at) > caseTier()) return false; }
  const by = c.src && c.src.ask;                         // a clue you ask someone for: they're aboard and on the roster
  if (by && (!schedPeople().some(p => p.id === by) || (typeof movedOff === 'function' && movedOff(by)))) return false;
  const tool = c.src && c.src.tool;
  if (tool && !(typeof hasTool === 'function' && hasTool(tool))) return false;
  return true;
}

// ---- held for you (section 17's heldForYou asks): till the shift it showed in ends, or you drop it ----
function caseHeld(j) {
  const c = caseOf(j); if (!c) return false;
  if (c.wait) return true;
  if (j.claimedBy === 'you') return caseNow() < c.until;   // yours till the shift ends; then the board's usual rules
  if (c.taken || caseNow() >= c.until) { caseRelease(c, j); return false; }
  return true;
}
// a case not ready yet (P3's tries under way) keeps its job off the board (section 17's board and openJobs ask)
function caseHidden(j) { const c = caseOf(j); return !!(c && c.wait && !c.m7); }   // Day 5's washer is on the board as your scanner job
// to the crew, who do it the long way (a part at a time, on paper): no remark
function caseRelease(c, j) {
  const parts = c.sus.filter(s => !c.known.includes(s)).map(s => caseSus(c, s).part).filter(p => p);
  j.parts = parts.length ? parts : j.parts; delete j.title;
  caseClose(c, 0, 'crew');
}
function caseClose(c, flags) {
  const C = caseState(); if (!C) return;
  C.open = C.open.filter(x => x !== c);
  C.done.push([c.id, Math.floor(caseNow() / 1440) + 1, flags]); if (C.done.length > CASE_DONE_KEEP) C.done.splice(0, C.done.length - CASE_DONE_KEEP);
  if (CASE_UI.at === c.id) CASE_UI.at = null;
}
// the work log's flags for a job: 2 right first time, 4 a clever fix; 0 if it wasn't a case (also on the job as
// j.rightFirst and j.clever, which 24 core reads at turn-in)
// a suspect on another machine is 'machine:cause' (P1's, along a line): its machine id, else null
const caseSusAt = s => { const i = typeof s === 'string' ? s.indexOf(':') : -1; return i > 0 && machineById(s.slice(0, i)) ? s.slice(0, i) : null; };
// section 17's stops ask (jobStopsBase, one line): the machine a case's job takes you to, if not its own: the called
// suspect's (P1), or before a call a kind's start (P1: the top of the line, so the arrow doesn't give the cause away)
function caseAt(j) {
  const c = j && j.case && caseOf(j); if (!c || c.wait) return null;
  const s = c.calls[c.calls.length - 1];
  if (s && !c.known.includes(s)) return caseSusAt(s);
  const K = CASE_KINDS[c.kind]; try { return K && K.start ? K.start(c, j) || null : null; } catch (e) { return null; }
}
// section 17's board card asks (jobCard, one line): a kind's own card [title, where, state, priority] (P1's names the
// line's symptom), else null and the card is as before
function caseCard(j) {
  const c = j && j.case && caseOf(j), K = c && !c.wait && CASE_KINDS[c.kind]; if (!K || !K.card) return null;
  try { return K.card(c, j) || null; } catch (e) { return null; }
}
function caseFlags(jobId) { const C = SHIP.works && caseState(), d = C && C.done.find(x => x[0] === 'c' + jobId); return d ? d[2] : 0; }

// ---- clues: collected where they are; a quiet toast and a badge on Fault notes ----
function caseClue(caseId, clueId) {
  const c = caseById(caseId), k = c && c.clues.find(x => x.id === clueId);
  if (!k || c.wait || c.got.includes(clueId)) return false;
  c.got.push(clueId);
  const who = k.src && (k.src.by || k.src.ask), p = who && schedPeople().find(x => x.id === who);
  const name = p ? p.name.split(' ').slice(-1)[0] : k.type === 'log' ? 'the log' : k.type;
  if (typeof toast === 'function') toast('+ clue: ' + name);
  if (typeof deviceNotify === 'function') deviceNotify({ app: caseApp(), text: '+ clue: ' + name });
  MACH_REV++;
  return true;
}
// asking someone about the fault (P2's chat step, later): their clue if they have one for this case
function caseAsk(caseId, who) { const c = caseById(caseId), k = c && c.clues.find(x => x.src && x.src.ask === who && !c.got.includes(x.id)); return k ? caseClue(caseId, k.id) : false; }
// a clue in words, built when you read it: the kind's own text (the Works writer's templates), else plain
function caseClueText(c, k) {
  const K = CASE_KINDS[c.kind]; try { const t = K.text && K.text(c, k); if (t) return t; } catch (e) { /* the plain words */ }
  const p = k.src && k.src.by && schedPeople().find(x => x.id === k.src.by), s = k.src && k.src.tried && caseSus(c, k.src.tried);
  if (k.type === 'note' && s) return (s.part ? 'New ' + s.part + ' in.' : 'Tried the ' + s.label + '.') + ' No change.' + (p ? ' — ' + p.name.split(' ').slice(-1)[0] : '');
  return k.type === 'log' ? 'The machine\'s log.' : 'A clue.';
}
const CASE_MARK = { note: 'note', log: 'clock', person: 'person', gauge: 'gauge', calendar: 'calendar' };
// once a ship minute (24 core's tick, else the clock's): taped clues when the job is yours, clues within reach, the
// kind's own tick, and cases whose job finished
function caseTick() {
  const C = SHIP.works && caseState(); if (!C) return;
  if (typeof p3Stage === 'function') p3Stage(C);        // Day 5's training case (P3, below)
  if (typeof p1Stage === 'function') p1Stage(C);        // Day 11's (P1)
  if (typeof p2Stage === 'function') { p2Stage(C); p2Word(C); }   // Day 14's (P2), and Tomas's word that opens it
  if (!C.open.length) return;
  for (const c of C.open.slice()) {
    const j = caseJob(c), K = CASE_KINDS[c.kind];
    if (!j) { caseClose(c, 0); continue; }
    if (K && K.tick) { try { K.tick(c, j); } catch (e) { /* a kind's tick never stops the game */ } }
    if (c.wait && (j.status === 'done' || (!c.train && shipNow() > c.posted + CASE_WAIT_MAX) || (c.train && j.until && shipNow() > j.until))) { caseClose(c, 0); continue; }   // never held for ever
    if (c.wait) { if (j.claimedBy === 'you' && !c.train) caseClose(c, 0); continue; }   // you took it before the case was ready: a plain repair
    if (!c.told) { c.told = true; if (typeof deviceNotify === 'function') deviceNotify({ app: caseApp(), text: c.title }); }   // shown inside section 17's hour: told here
    if (j.status === 'done') { caseDone(c, j); continue; }
    if (j.claimedBy === 'you') { c.taken = true; for (const k of c.clues) if (k.at === 'board') caseClue(c.id, k.id); }
    if (!c.taken) continue;
    for (const k of c.clues) if (k.at && k.at !== 'board' && !c.got.includes(k.id) && caseNear(k.at)) caseClue(c.id, k.id);
  }
}
function caseNear(placeId) {
  try {
    const p = placeById(placeId); if (!p || deckDef.num !== p.deck || typeof placeSpot !== 'function') return false;
    const s = placeSpot(placeId); if (!s) return false;
    return Math.hypot(s.x - player.obj.position.x, s.z - player.obj.position.z) < JOB_REACH + .5;
  } catch (e) { return false; }
}
// the job's finished: right first time (one call, the right one), a clever fix (and no talking it through, no more
// clues than the fewest + 1); the work log asks caseFlags
function caseDone(c, j) {
  const you = j.doneBy === 'you', first = you && c.calls.length === 1 && c.calls[0] === c.cause && !c.long;
  const clever = first && !c.talk && c.got.length <= c.fewest + 1;
  caseClose(c, (first ? 2 : 0) | (clever ? 4 : 0));
  if (you && typeof worksUse === 'function') worksUse(CASE_KINDS[c.kind] ? CASE_KINDS[c.kind].ladder : c.kind);   // a use of the row (a small row's first is its training)
  if (clever && typeof simNote === 'function') simNote('cleverFix', { machine: j.machine, kind: c.kind });
}

// ---- calling it: the suspect's part goes on the job; the job's normal loop runs ----
function caseCall(caseId, susId) {
  const c = caseById(caseId), j = c && caseJob(c);
  if (!c || !j || c.wait || !c.sus.includes(susId) || c.known.includes(susId)) return false;
  const s = caseSus(c, susId);
  if (c.calls.length > (c.fits || 0)) c.calls.pop();     // called again before fitting: it replaces the last call (it was never tried)
  c.calls.push(susId);
  if (typeof simNote === 'function') simNote('caseCalled', { id: c.id, job: j.id, train: !!c.train });   // 24 core's escort ends on the training case's call
  if (!(typeof jobSetPart === 'function' && s.part && jobSetPart(j.id, s.part))) j.parts = s.part ? [s.part] : [];   // section 17's needs a part already there
  j.stepsDone = (j.stepsDone || []).filter(k => k !== 0);   // the fetch again, now there's a part to fetch
  MACH_REV++;
  return true;
}
// section 17's jobStepDone asks at the last stop: a wrong call (or none yet) keeps the machine as it was -> true
function caseFitted(j) {
  const c = caseOf(j); if (!c) return typeof scanFitted === 'function' ? scanFitted(j) : false;   // not a case: the scanner's pick, if any (24g)
  if (c.wait) return false;
  const last = c.calls[c.calls.length - 1];
  if (last) c.fits = c.calls.length;                     // this call has now been fitted
  if (last === c.cause) {                               // right: the job finishes as any repair; 24 core's work log reads the flags at turn-in
    j.rightFirst = c.calls.length === 1 && !c.long; j.clever = j.rightFirst && !c.talk && c.got.length <= c.fewest + 1;
    return false;
  }
  const m = machineById(j.machine), f = caseCauses(m).find(x => x.id === c.cause), shows = f && f.shows || 'acts up';
  let line = 'You look it over: it still ' + shows + '. Fault notes has the suspects.';
  if (last) {
    const s = caseSus(c, last);
    if (!c.known.includes(last)) c.known.push(last);
    if (!c.crossed.includes(last)) c.crossed.push(last);
    const spent = s.part && CASE_SPENT.has(s.part) && jobTier(j) >= 2;
    if (s.part && !spent) returnPart(s.part);           // Tier 1: back on its shelf unused
    const said = s.still && typeof faultWords === 'function' ? faultWords(s.still) : null, K = CASE_KINDS[c.kind];
    let own = null; try { own = K && K.wrong ? K.wrong(c, last) : null; } catch (e) { own = null; }   // a kind's own words (P1: the line's symptom)
    line = own || said || (s.part ? 'New ' + s.part + ' in.' : 'Done.') + ' Still ' + shows + '.';
    if (spent) line += ' ' + caseText('case.wrong.t2', 'The {part} is used up.', { part: s.part });   // the T2 band: it was fitted and used
  }
  const into = last && caseSusAt(last);                  // the machine the part went into (P1's suspects are along the line)
  j.stepsDone = []; j.parts = []; j.touched = shipNow();
  if (typeof toast === 'function' && !SIM_AT) toast(caseMachName(into ? { machine: into } : j), line);
  const wrong = c.calls.filter(x => x !== c.cause).length;
  if (wrong === 2 && !c.talk && typeof toast === 'function' && !SIM_AT) toast('Fault notes', (c.by ? schedPeople().find(p => p.id === c.by) || { name: 'Calder' } : { name: 'Calder' }).name.split(' ')[0] + ' can talk it through with you: it\'s on Fault notes.');
  if (c.long) caseLongNext(c);
  return true;
}
// hints: the Chief's notes (always); a Works hand says which kind of clue you're missing; talking it through crosses
// one decoy out with you (no clever fix); the long way fits each suspect in turn (always ends)
function caseHint(caseId) {
  const c = caseById(caseId); if (!c) return null; const K = CASE_KINDS[c.kind];
  if (c.ticket && c.got.length < 3) return worksText('ticket.nohint', 'It\'s a ticket: no hints till you\'ve looked at three things yourself.');   // 24l (E2, standing in for H): a ticket's hints after your third clue
  const miss = c.clues.find(k => !c.got.includes(k.id));
  if (!miss) return 'You\'ve got every clue there is. Cross out what they rule out.';
  try { const h = K.hint && K.hint(c); if (h) return h; } catch (e) { /* the plain words */ }
  return { note: 'Have you read the notes on the job?', log: 'Have you looked at its log on the panel?', person: 'Ask around: someone saw it.', gauge: 'Have you read the gauge?', calendar: 'Check the calendar.' }[miss.type] || 'There\'s more to find.';
}
function caseTalk(caseId) {
  const c = caseById(caseId); if (!c || c.talk) return false;
  const d = c.sus.find(s => s !== c.cause && !c.crossed.includes(s)) || c.sus.find(s => s !== c.cause && !c.known.includes(s));
  c.talk = true; if (d && !c.crossed.includes(d)) c.crossed.push(d); if (d && !c.known.includes(d)) c.known.push(d);
  return true;
}
function caseLong(caseId) { const c = caseById(caseId); if (!c) return false; c.long = true; caseLongNext(c); return true; }
function caseLongNext(c) { const s = c.sus.find(x => !c.known.includes(x)); if (s) caseCall(c.id, s); }

// ---- Fault notes and the Chief's notes on the device ----
// CHIEF_NOTES[kind] = { title, lines }: a page each, added when a kind opens (the Works writer's words); more lines
// for machine kinds you know well later
const CHIEF_NOTES = {};
const CASE_UI = { at: null, ask: null, chief: false };
function caseView() {
  const C = SHIP.works && SHIP.works.cases && caseState(), open = C ? C.open.filter(c => !c.wait) : [];
  const B = [];
  if (CASE_UI.chief) {
    B.push({ kind: 'text', text: 'The Chief\'s notes', mark: 'big' });
    const other = Object.keys(CHIEF_NOTES).filter(k => !CASE_KINDS[k] && typeof CHIEF_NOTES[k].open === 'function' && (() => { try { return !!CHIEF_NOTES[k].open(); } catch (e) { return false; } })()).sort();   // pages that aren't case kinds (24i's tracing: M3's ask), open by their own open()
    const pages = caseKindsOpen().map(id => CHIEF_NOTES[id]).concat(other.map(k => CHIEF_NOTES[k])).filter(p => p);
    if (!pages.length) B.push({ kind: 'text', text: 'Nothing here yet.' });
    for (const p of pages) B.push({ kind: 'text', text: p.title, mark: 'hot' }, { kind: 'list', rows: p.lines.map((l, i) => ({ text: (p.key && typeof worksText === 'function' && worksText(p.key + '.' + (i + 1), null)) || l })) });   // the writer's chief.<kind>.N, else the stand-in
    B.push({ kind: 'buttons', items: [{ label: 'Back to the fault', action: { app: caseApp(), do: 'case:chief', arg: 0 } }] });
    return { title: 'Fault notes', blocks: B };
  }
  if (!open.length) {
    B.push({ kind: 'text', text: 'No head-scratchers open. When the board has one, its notes are here.' },
      { kind: 'buttons', items: [{ label: 'The Chief\'s notes', action: { app: caseApp(), do: 'case:chief', arg: 1 } }] });
    return { title: 'Fault notes', blocks: B };
  }
  const c = open.find(x => x.id === CASE_UI.at) || open[0], K = CASE_KINDS[c.kind], A = (v, arg) => ({ app: caseApp(), do: 'case:' + v, arg: c.id + '|' + arg });
  if (open.length > 1) B.push({ kind: 'buttons', items: open.map((x, i) => ({ label: 'Case ' + (i + 1), on: x === c, action: { app: caseApp(), do: 'case:at', arg: x.id } })) });
  B.push({ kind: 'text', text: c.title.replace(/^Head-scratcher: /, ''), mark: 'big' }, { kind: 'text', text: 'Suspects (tap to cross out)' });
  B.push(devChips(c.sus.map(s => ({ label: caseSus(c, s).label.replace(/^./, x => x.toUpperCase()), on: !c.crossed.includes(s), action: A('cross', s) }))));
  try { const v = K.view && K.view(c); if (Array.isArray(v)) B.push(...v); } catch (e) { /* the kind's view is extra */ }
  const got = c.clues.filter(k => c.got.includes(k.id)), left = c.clues.length - got.length;
  B.push({ kind: 'text', text: 'Clues' }, { kind: 'list', rows: got.map(k => ({ text: caseClueText(c, k), sub: CASE_MARK[k.type] || k.type })).concat(left ? [{ text: left === 1 ? 'One more to find.' : 'More to find.', mark: 'new' }] : []) });
  if (CASE_UI.ask && CASE_UI.ask.c === c.id) {
    const s = CASE_UI.ask.s;
    B.push({ kind: 'text', text: 'Call it: the ' + caseSus(c, s).label + '?', mark: 'hot' }, { kind: 'buttons', items: [{ label: 'Yes', action: A('yes', s) }, { label: 'Not yet', action: A('no', s) }] });
  } else {
    const items = [];
    if (left) items.push({ label: 'Where next?', action: A('next', 0) });
    const can = c.sus.filter(s => !c.crossed.includes(s) && !c.known.includes(s));
    if (!c.long) for (const s of can) items.push({ label: 'Call it: ' + caseSus(c, s).label, action: A('call', s) });
    B.push({ kind: 'buttons', items });
  }
  const last = c.calls[c.calls.length - 1];
  if (last && !c.known.includes(last)) B.push({ kind: 'text', text: 'Called: the ' + caseSus(c, last).label + '. Fetch it and fit it.', mark: 'hot' });
  const wrong = c.calls.filter(x => x !== c.cause).length, hints = [{ label: 'The Chief\'s notes', action: { app: caseApp(), do: 'case:chief', arg: 1 } }];
  if (wrong >= 2 && !c.talk) hints.push({ label: 'Talk it through', action: A('talk', 0) });
  if (!c.long) hints.push({ label: 'Fit them one by one', action: A('long', 0) });
  B.push({ kind: 'buttons', items: hints });
  return { title: 'Fault notes', blocks: B };
}
function caseAct(verb, arg) {
  const v = String(verb).replace(/^case:/, ''), [id, s] = String(arg).split('|');
  if (v === 'chief') { CASE_UI.chief = !!+arg; return; }
  if (v === 'at') { CASE_UI.at = arg; CASE_UI.ask = null; return; }
  const c = caseById(id); if (!c) return;
  CASE_UI.at = c.id;
  if (v === 'cross') { if (c.known.includes(s)) return; const i = c.crossed.indexOf(s); if (i < 0) c.crossed.push(s); else c.crossed.splice(i, 1); }
  else if (v === 'call') CASE_UI.ask = { c: c.id, s };
  else if (v === 'no') CASE_UI.ask = null;
  else if (v === 'yes') { CASE_UI.ask = null; if (caseCall(c.id, s)) { const p = caseSus(c, s).part; if (p && typeof toast === 'function') toast('Called it', 'A ' + p + ' from main storage, Deck 5. Follow the marker.'); } }
  else if (v === 'next') {
    const k = c.clues.find(x => !c.got.includes(x.id)), p = k && k.at && k.at !== 'board' && placeById(k.at);
    if (p && typeof setGoal === 'function') { SHIP.player.track = null; setGoal({ deck: p.deck, place: p.id, label: (roomName(p.deck, p.room) || 'The clue') + (p.deck !== deckDef.num ? ', ' + deckIn(p.deck) : '') }); }
    else if (k && k.src && k.src.ask && typeof setGoal === 'function') {   // a person: where they are now
      const p = schedPeople().find(x => x.id === k.src.ask), w = p && whereIs(p, shipNow());
      if (w && w.placeId && placeById(w.placeId)) { SHIP.player.track = null; setGoal({ deck: w.deck, place: w.placeId, label: shortName(p) + (w.deck !== deckDef.num ? ', ' + deckIn(w.deck) : '') }); }
      else if (typeof toast === 'function') toast('Fault notes', caseHint(c.id));
    }
    else if (k && k.at === 'board' && typeof setGoal === 'function') { SHIP.player.track = null; setGoal({ deck: 5, room: 'w', label: 'The job board, in the Works bay' }); }
    else if (k && typeof toast === 'function') toast('Fault notes', caseHint(c.id));
  }
  else if (v === 'doubt') { c.doubt = c.doubt || []; const i = c.doubt.indexOf(s); if (i < 0) c.doubt.push(s); else c.doubt.splice(i, 1); }   // P2: a witness marked "doesn't fit" (yours, kept)
  else if (v === 'talk') caseTalk(c.id);
  else if (v === 'long') caseLong(c.id);
  MACH_REV++;
}
// a tab of 24 core's Works app when it has tabs (worksTabAdd), else its own app (faultnotes), hidden till a kind opens
const CASE_BADGE = () => { const C = SHIP.works && SHIP.works.cases; return C && C.open.some(c => !c.wait && !c.got.length) ? 1 : null; };
if (typeof worksTabAdd === 'function') worksTabAdd({ id: 'faults', verbs: 'case', title: 'Fault notes', order: 40, view: () => caseView().blocks, act: caseAct, badge: CASE_BADGE });
else deviceApp({ id: 'faultnotes', title: 'Fault notes', short: 'Faults', icon: 'wrench', order: 32, hidden: () => !caseKindsOpen().length, badge: CASE_BADGE, view: caseView, act: caseAct });

// ---- 24k P3. What's been tried? (Day 5; plans/mechanics/p3-whats-been-tried.html). The crew have had a go already:
// one try per decoy, by a Works crew member really on shift, 2-12 ship hours after the fault is posted (keys 890 the
// times, 891 who), each using the decoy's part off the shelf and leaving a note ("New door seal in. Still leaks. —
// Kovac"). Each note rules out what was tried. The case shows when the last try is done, during your shift. The
// first (Day 5's training case) is fixed: Washer 2 in the junior wing's laundry leaking from 18:00 on Day 4 (the
// pump), a door seal and a drain valve tried overnight, shown once the ladder's p3 row opens, the teacher with you.
// The tries are on paper here (who and when worked out at posting, the part off its shelf at that time); they become
// the crew's real try jobs once section 17's jobKindAdd is in. ----
const P3_NOTE = (c, k) => {
  const j = caseJob(c), m = j && machineById(j.machine), s = caseSus(c, k.src.tried), f = m && caseCauses(m).find(x => x.id === c.cause), p = k.src.by && schedPeople().find(x => x.id === k.src.by);
  const shows = f && f.shows || 'acts up', odd = k.src.odd;   // odd: the try that rules out less than it seems (the wrong size, never seated)
  const fb = odd ? 'Put in ' + (s.part ? 'a ' + s.part : 'a new ' + s.label) + ' from the old stock: the wrong size, it never seated. Still ' + shows + '.'
    : (s.part ? 'New ' + s.part + ' in.' : 'Tried the ' + s.label + '.') + ' Still ' + shows + '.';
  const t = (typeof worksText === 'function' && m ? (odd ? worksText('fault.tried.odd', fb, { part: s.part || s.label, shows }) : worksText('fault.tried.' + m.kind + '.' + k.src.tried, fb)) : fb) || fb;
  return t + (p ? ' — ' + p.name.split(' ').slice(-1)[0] : '');
};
// who tries, and when: the times from 2 to 12 hours after `t`, in order; whoever of the Works crew is at work then
// (key 891 if several); none on shift: the first Works hand at work the next morning, 06:00-08:00
function p3Tries(j, decoys, seed, t) {
  const crew = schedPeople().filter(p => jobCrew(p) === 'works').sort((a, b) => a.id < b.id ? -1 : 1), pp = panelPlace(j.machine);
  const at = (p, x) => { try { return planWhere(p, x).act === 'work'; } catch (e) { return false; } };
  const times = decoys.map((s, i) => t + 120 + Math.round(schedU(seed, i, 890) * 600)).sort((a, b) => a - b);
  let last = t, prev = null;
  return decoys.map((s, i) => {
    let x = Math.max(times[i], last + 15), on = crew.filter(p => at(p, x));
    if (!on.length) {                                    // nobody at work: the next morning from 06:00, a Works hand if one's in by 09:00, else whoever is
      const m0 = (Math.floor(x / 1440) + (x % 1440 >= 360 ? 1 : 0)) * 1440 + 360, hand = y => crew.filter(p => at(p, y) && p.rank !== 'chief');
      let y = m0; while (y <= m0 + 180 && !hand(y).length) y += 15;
      if (y <= m0 + 180) { x = y; on = hand(y); } else { for (x = m0; x <= m0 + 180 && !(on = crew.filter(p => at(p, x))).length; x += 15); if (!on.length) x = m0; }
    }
    last = x;
    const pref = on.filter(p => p.id !== prev && p.rank !== 'chief'), pool = pref.length ? pref : on;   // a Works hand, not the one before, if there's one
    const by = pool.length ? pool[Math.floor(schedU(seed, i, 891) * pool.length)].id : null; prev = by;
    return { id: 'n' + i, type: 'note', src: { by, t: x, tried: s, done: false }, at: i && pp ? pp : 'board', kills: [s] };   // the first on the job, the rest on the machine
  });
}
// a P3 case's notes: one per decoy; from the T2 band, half the time (key 1002) one more that rules out less than it
// seems: a suspect's part tried but the wrong size (it never seated), so it kills nothing and takes nothing off the shelf
function p3Clues(j, cause, sus, seed, band) {
  const decoys = sus.filter(s => s !== cause), odd = band !== 'T1' && decoys.length < 3 && schedU(seed, 0, 1002) < .5;
  const on = odd ? sus[Math.floor(schedU(seed, 1, 1002) * sus.length)] : null, notes = p3Tries(j, odd ? decoys.concat([on]) : decoys, seed, caseNow());
  if (odd) { const k = notes[notes.length - 1]; k.kills = []; k.src.odd = 1; }   // the last try (p3Tries keeps the list's order)
  return notes;
}
// once a ship minute (24k's caseTick): the tries whose time has come are done (the part comes off its shelf); when all
// are, the case shows on the board, inside your shift (a training case once its ladder row has opened)
function p3Tick(c, j) {
  if (!c.wait) return;
  const now = shipNow();
  for (const k of c.clues) if (!k.src.done && now >= k.src.t) {
    k.src.done = true; const p = !k.src.odd && caseSus(c, k.src.tried).part;   // the wrong-size one wasn't from the shelf
    if (p && SHIP.stores[p] > 0) { SHIP.stores[p]--; MACH_REV++; }
  }
  if (c.clues.some(k => !k.src.done)) return;
  const d = Math.floor(now / 1440) + 1, mn = now % 1440;
  const here = c.m7 && j.claimedBy === 'you' && !!j.scan;   // Day 5: you've read Washer 2 with the scanner, the teacher beside you
  if (!here && (!playerShiftOn(d) || mn < DAY_SHIFT[0] || mn >= 900 || (c.train && !caseOpened('p3')))) return;
  if (c.train) { const W = SHIP.works, row = typeof ladderRow === 'function' && ladderRow('p3'); c.by = (here && W && W.cur && W.cur.by) || (row && typeof ladderTeacher === 'function' && ladderTeacher(row, d)) || 'calder'; }
  caseShow(c, j);
  if (c.train && typeof worksSay === 'function') worksSay(c.by, (typeof worksText === 'function' && worksText('works.train.p3.start', null)) || 'Here\'s a funny one. ' + c.title + '. Open Fault notes: the first note\'s taped to the job.');
}
CASE_KINDS.p3 = { name: 'What\'s been tried?', ladder: 'p3',
  fits: (cause, m) => !!cause.part && caseDecoys(m, cause.id, 0, x => !!x.part).length >= 2,
  suspects: (j, seed) => { const d = caseDecoys(machineById(j.machine), j.cause, seed, x => !!x.part); return [j.cause].concat(d.slice(0, d.length >= 3 && schedU(seed, 0, 890) < .4 ? 3 : 2)); },
  clues: (j, cause, sus, seed, band) => p3Clues(j, cause, sus, seed, band),
  bands: { T2: { sus: [3, 4], clues: [2, 3], fewest: 2, decks: 1 } },   // the gentle kind keeps its size for an Officer (a machine has at most three causes with one card)
  wait: () => true, tick: p3Tick, text: P3_NOTE, view: () => [],
  hint: c => (typeof worksText === 'function' && worksText('case.hint.p3.1', null)) || 'Have you read every note? One\'s on the machine.' };
CHIEF_NOTES.p3 = { title: 'What\'s been tried', key: 'chief.p3', lines: [
  'If someone fitted it and it\'s still wrong, it isn\'t that.',
  'Read every note. One\'s on the job; the others are on the machine.',
  'What nobody has tried yet is your best bet.'] };
if (typeof WORK_MECH !== 'undefined') WORK_MECH.p3 = { open() { /* the training case is already staged (p3Stage); it shows at the next tick */ } };
// Day 5's training case, staged at 18:00 on Day 4 (or the first 18:00 from Day 4 the ship gets to without it): held
// for you (24 core's slot 20) till the row opens, so it's never on the crew's board
function p3Stage(C) {
  if (C.first || !SHIP.works) return;
  if (SHIP.works.tr && SHIP.works.tr.p3 !== undefined || caseOpened('p3')) { C.first = 'none'; return; }   // an older save past it
  const now = shipNow(), t18 = Math.floor((now - 1080) / 1440) * 1440 + 1080, d = Math.floor(t18 / 1440) + 1;
  if (now < 1080 || d < 4) return;
  const mine = SHIP.clothes && SHIP.clothes.hamper, washing = id => !!(mine && mine.at === 'washer' && mine.washer === id);   // your own wash in it: the next one
  const m = ['4-washer-2', '4-washer-3'].map(machineById).find(x => x && !washing(x.id) && !SHIP.jobs.some(j => j.machine === x.id && j.status !== 'done' && j.claimedBy === 'you'));
  if (!m || !caseCauses(m).some(x => x.id === 'pump')) { C.first = 'none'; return; }
  const id = jobReserve(m.id, d, 1080, 20, { train: 'p3', tier: 1, until: t18 + 7 * 1440, cause: 'pump' }), j = id && SHIP.jobs.find(x => x.id === id);
  if (!j) return;
  delete j.make; delete j.makeMins; j.cause = 'pump'; j.parts = ['pump']; j.train = 'p3';   // its suspects all read worn on the scanner
  const sus = ['pump', 'seal', 'valve'].filter(s => caseCauses(m).some(x => x.id === s && x.part));
  const clues = p3Tries(j, sus.filter(s => s !== 'pump'), machSeed('p3-first'), t18), r = caseSolve(sus, clues, 'T1', 'pump');
  if (r.why) { C.first = 'none'; return; }
  const c = { id: 'c' + j.id, job: j.id, kind: 'p3', k: 0, band: 'T1', cause: 'pump', sus, fewest: r.fewest, clues, got: [], crossed: [], known: [], calls: [], posted: t18, until: 0,
    wait: true, taken: false, talk: false, long: false, train: true, told: false, title: '' };
  C.open.push(c); j.case = c.id; C.first = c.id; C.n++;
  MACH_REV++;
}

// ---- 24k P1. When does it happen? (Day 12, a word from Calder; plans/mechanics/p1-when-does-it-happen.html). A fault
// on a line (water, heat or air: the cause has a `line`, and shows only at some hours: peak, warm, after-use or
// at-time) becomes a case whose card names the line's symptom, not the machine ("Showers on Deck 4 run weak, but only
// in the evening"). Its suspects are the cause and one cause on each of three other machines on the line (an id
// 'machine:cause'); each of those machines keeps a log at its panel: how it ran each hour of the day before (machWorks
// of its recorded condition, MACH_HIST). A machine that ran fine every hour isn't what cuts the flow, so its log
// crosses its suspect out; decoys are only picked on machines whose log really is fine. A roll case puts a second
// cause with the same `when` first when the line has one (lead 16), so the card alone doesn't settle it. Fault notes
// shows the logs you've read as a day strip (devStrip), the symptom's hours outlined. The job's card (caseCard) and its
// stop before a call (caseAt: the top of the line) don't name the machine; a call sends you to the suspect's machine.
// The first (from 16:00 on Day 11 once your Tier 2 test is passed; shown once the p1 row opens on Day 12, after the
// tracing lesson, with Calder's word) is fixed: 3-pump-1 can't keep up in the evening, the recycler's membrane, the
// filter bank's cartridge and the Deck 4-6 branch valve the decoys. Lines: section 17's MACHINE_LINKS once it's in,
// else P1_LINES. Key 1000: the busiest hours, on ties. ----
const P1_LINES = { water: ['3-recycler-1', '3-filter-1', '3-pump-1', '5-valve-2'] };   // stand-in for a build without section 17's MACHINE_LINKS (0.33.59)
const P1_LINE = { water: { deck: 4, where: 'Showers on Deck {deck}', shows: 'run weak' }, heat: { deck: 2, where: 'Cabins on Deck {deck}', shows: 'run cold' },
  air: { deck: 4, where: 'The air on Deck {deck}', shows: 'is stuffy' } };
const P1_WHEN = { evening: 'in the evening', morning: 'in the morning', peak: 'at the busy hours', night: 'at night', after: 'after the busy hours' };
const P1_WHENS = new Set(['peak', 'warm', 'after-use', 'at-time']);
const P1_FIRST = { machine: '3-pump-1', cause: 'pump', decoys: ['3-recycler-1:membrane', '3-filter-1:cartridge', '5-valve-2:valve'], hours: [18, 19, 20, 21, 22] };
const P1_FINE = 8;                                       // a log hour at 80% or more: it ran fine
const P1_BAND = { sus: [4, 4], clues: [3, 3], fewest: 3, decks: 2 };   // the page's T2: one line, 4 suspects, 3 logs (its later bands come with their steps)
const caseDay = t => Math.floor(t / 1440) + 1;
const caseText = (key, fb, vars) => typeof worksText === 'function' ? worksText(key, fb, vars) : String(fb).replace(/\{(\w+)\}/g, (m, x) => vars && vars[x] != null ? String(vars[x]) : m);
// the deck a fault on machine id is felt on (the card's): Deck 4 if the line feeds it there, else the first it feeds
// (section 17's lineDecks), else the stand-in's
function caseLineDeck(id, line) {
  try { if (typeof lineDecks === 'function' && typeof MACHINE_LINKS !== 'undefined' && MACHINE_LINKS[line]) { const ds = lineDecks(line, id) || []; if (ds.length) return ds.includes(4) ? 4 : ds[0]; } } catch (e) { /* the stand-in */ }
  return (P1_LINE[line] || P1_LINE.water).deck;
}
// the machines between the top of a machine's line and the deck its fault is felt on, in order (section 17's
// MACHINE_LINKS: its steps through the branch that feeds that deck and the machines after it, 0.33.59; else the
// stand-in), or null if it isn't on that line
function caseLine(id, line) {
  try {
    if (typeof MACHINE_LINKS !== 'undefined' && MACHINE_LINKS[line] && typeof linePath === 'function') {
      const D = caseLineDeck(id, line), S = MACHINE_LINKS[line].find(x => x && typeof x === 'object' && !Array.isArray(x));
      const b = S && Object.keys(S).find(k => (S[k] || []).includes(D)), ends = b && typeof LINE_ENDS !== 'undefined' && (LINE_ENDS[line] || {})[b] || [];
      const p = b ? linePath(line, ends.length ? ends[ends.length - 1] : b) : MACHINE_LINKS[line].map(x => typeof x === 'string' ? [x] : x);
      const ids = (p || []).flat().filter(x => typeof x === 'string');
      return ids.includes(id) ? ids : null;
    }
  } catch (e) { /* the stand-in */ }
  const ids = P1_LINES[line]; return ids && ids.includes(id) ? ids.slice() : null;
}
// the hours of day d a cause shows in (24 flags): always; peak: the machine's six busiest hours (its kind's use
// counter, else water on the water line, else the people on its deck; key 1000 on ties); after-use: the hour after
// each busy run; warm: 18:00-24:00 (after hours of busy use); at-time: 22:00-06:00. touched and with: none here (they
// follow something else: the door, another machine)
function caseWhenHours(m, when, d) {
  const out = new Array(24).fill(0);
  if (when === 'always') return out.fill(1);
  if (when === 'warm') { for (let h = 18; h < 24; h++) out[h] = 1; return out; }
  if (when === 'at-time') { for (let h = 0; h < 24; h++) out[h] = h >= 22 || h < 6 ? 1 : 0; return out; }
  if (when !== 'peak' && when !== 'after-use') return out;
  const K = MACHINE_KINDS[m.kind], u = machUseDay(d), k = K.use || (K.sys === 'water' ? 'water' : 'heads'), v = (k === 'heads' ? u.heads[m.deck] : u[k]) || [];
  const top = [...Array(24).keys()].filter(h => v[h] > 0).sort((a, b) => v[b] - v[a] || schedU(m.seed, d * 24 + a, 1000) - schedU(m.seed, d * 24 + b, 1000)).slice(0, 6);
  for (const h of top) if (when === 'peak') out[h] = 1; else if (h < 23 && !top.includes(h + 1)) out[h + 1] = 1;
  return out;
}
const caseWhenWord = (when, hrs) => { const on = hrs.map((x, h) => x ? h : -1).filter(h => h >= 0);
  return when === 'at-time' ? 'night' : when === 'after-use' ? 'after' : when === 'warm' || on.length && on.every(h => h >= 17) ? 'evening' : on.length && on.every(h => h < 12) ? 'morning' : 'peak'; };
// a machine's log for day d: 24 digits, how it ran each hour (machWorks of its recorded condition; an hour not
// recorded reads as it is now), 9 meaning 90-100%
function caseLog(id, d) {
  const s0 = SHIP.machines[id]; let out = '';
  for (let h = 0; h < 24; h++) { const r = MACH_HIST.get((d - 1) * 24 + h), c = r && r[id] != null ? r[id] : s0 ? machEff(s0) : 100; out += Math.min(9, Math.max(0, Math.floor(machWorks(c) / 10))); }
  return out;
}
const caseLogFine = log => typeof log === 'string' && log.length === 24 && [...log].every(x => +x >= P1_FINE);
// the decoys: another machine on the line, with a panel at your tier, whose log for day d is fine, and its part causes
// that cut the same line; in the seed's order (key 892), those in `prefer` first; a roll case's first decoy a cause
// with the same `when` as the cause if the line has one (lead 16), the rest a different `when` where they can
function p1Pick(j, seed, band, prefer) {
  const m = machineById(j.machine), cause = caseCauses(m).find(x => x.id === j.cause), d = caseDay(caseNow()) - 1, n = caseBandOf('p1', band).sus[1] - 1;
  const pool = [];
  for (const id of caseLine(m.id, cause.line) || []) {
    const x = id !== m.id && machineById(id), pp = x && panelPlace(id);
    if (!pp || placeTier(pp) > caseTier() || !caseLogFine(caseLog(id, d))) continue;
    const fs = caseCauses(x).filter(f => f.part && f.line === cause.line && !f.load);
    if (fs.length) pool.push({ id, fs, pre: prefer ? prefer.findIndex(s => s.startsWith(id + ':')) : -1 });
  }
  const order = pool.map((x, i) => [x.pre >= 0 ? x.pre - 9 : schedU(seed, i, 892), x]).sort((a, b) => a[0] - b[0]).map(x => x[1]);
  const out = [], same = !prefer && order.find(x => x.fs.some(f => f.when === cause.when));
  if (same) out.push(same.id + ':' + same.fs.find(f => f.when === cause.when).id);
  for (const x of order) {
    if (out.length >= n) break; if (x === same) continue;
    const f = x.pre >= 0 && x.fs.find(f => prefer[x.pre] === x.id + ':' + f.id) || x.fs.find(f => f.when !== cause.when) || x.fs[0]; out.push(x.id + ':' + f.id);
  }
  return out;
}
// one log per decoy, at its machine's panel; a fine log crosses its decoy out
function p1Clues(j, cause, sus) {
  const d = caseDay(caseNow()) - 1;
  return sus.filter(s => s !== cause).map((s, i) => { const id = caseSusAt(s), log = caseLog(id, d); return { id: 'l' + i, type: 'log', src: { m: id, log, d }, at: panelPlace(id), kills: caseLogFine(log) ? [s] : [] }; });
}
function p1Sus(c, id) {                                  // every suspect named with its machine ("Water filter bank: cartridge")
  const at = caseSusAt(id), j = caseJob(c), x = machineById(at || (j && j.machine)), cid = at ? id.slice(at.length + 1) : id, f = x && caseCauses(x).find(y => y.id === cid);
  return x && f ? { label: caseMachName({ machine: x.id }) + ': ' + (f.name || f.part || f.id), part: f.part || null, still: null } : null;
}
const p1Cause = c => { const j = caseJob(c), m = j && machineById(j.machine); return { j, m, f: m && caseCauses(m).find(x => x.id === c.cause) }; };
function p1Hours(c) {                                    // the symptom's hours (the card's): the first case's are the evening's
  if (c.train) return P1_FIRST.hours.slice();
  const { m, f } = p1Cause(c), k = c.clues.find(x => x.src && x.src.d); if (!f) return [];
  return caseWhenHours(m, f.when, k ? k.src.d : caseDay(c.posted) - 1).map((x, h) => x ? h : -1).filter(h => h >= 0);
}
function p1Where(c) { const { j, f } = p1Cause(c), line = f && f.line || 'water', L = P1_LINE[line] || P1_LINE.water, deck = j && j.symptom && j.symptom.deck || (j ? caseLineDeck(j.machine, line) : L.deck);
  return { line, deck, where: caseText('case.line.' + line, L.where, { deck }), shows: caseText('case.line.' + line + '.shows', L.shows) }; }
function p1Title(c) {
  const { f } = p1Cause(c), P = p1Where(c), hrs = new Array(24).fill(0); for (const h of p1Hours(c)) hrs[h] = 1;
  const w = c.train ? 'evening' : caseWhenWord(f.when, hrs), when = caseText('case.when.' + w, P1_WHEN[w]);
  return caseText('case.title.p1', '{machine} {shows}, but only {when}', { machine: P.where, shows: P.shows, when });
}
function p1Card(c, j) {                                  // the board card: the line's symptom and where it's felt, never the machine
  const P = p1Where(c), who = j.claimedBy === 'you' ? 'you' : j.claimedBy ? ((schedPeople().find(p => p.id === j.claimedBy) || {}).name || '').split(' ')[0] : null;
  return [c.title.replace(/^Head-scratcher: /, ''), deckWord(P.deck) + ' · the ' + P.line + ' line', 'head-scratcher' + (who ? ', ' + who + ' on it' : ', asked for you'), JOB_PRI[j.urgency] || 'routine'];
}
function p1Start(c, j) { const { f } = p1Cause(c), ids = f && caseLine(j.machine, f.line) || []; return ids.find(id => id !== j.machine && panelPlace(id)) || null; }   // the top of the line
function p1Wrong(c, s) { const x = p1Sus(c, s), P = p1Where(c); return caseText('case.wrong.p1', 'New {part} in. {where} still {shows}.', { part: x && x.part || 'part', where: P.where, shows: P.shows }); }
function p1Runs(log) { const out = []; for (let h = 0; h < 24; h++) { const low = +log[h] < P1_FINE, r = out[out.length - 1]; if (r && r[2] === low) r[1] = h + 1; else out.push([h, h + 1, low]); } return out; }
function p1Text(c, k) {
  if (k.type !== 'log' || !k.src || !k.src.log) return null;
  const nm = caseMachName({ machine: k.src.m }), runs = p1Runs(k.src.log), hh = h => String(h).padStart(2, '0');
  const said = runs.length === 1 && !runs[0][2] ? caseText('case.strip.allday', 'full output every hour, evenings too')
    : runs.map(([a, b, low]) => caseText(low ? 'case.strip.low' : 'case.strip.fine', (low ? 'low ' : 'fine ') + '{from}-{to}', { from: hh(a), to: hh(b) })).join(', ');
  return caseText('case.strip.title', '{machine}\'s log', { machine: nm }) + ': ' + said + '.';
}
function p1View(c) {
  const pins = p1Hours(c), rows = c.clues.filter(k => c.got.includes(k.id) && k.src && k.src.log).map(k => ({ label: caseText('case.strip.title', '{machine}\'s log', { machine: caseMachName({ machine: k.src.m }) }), hours: [...k.src.log].map(x => (+x + .5) / 10), pins, words: p1Text(c, k) }));
  if (!rows.length) return [];
  return [{ kind: 'text', text: caseText('case.strip.head', 'Yesterday, hour by hour (the hours it shows outlined)') }, devStrip(rows, r => r.words.replace(/^[^:]*: /, ''))];
}
// once a ship minute (24k's caseTick): the first case shows once the p1 row has opened, inside your shift, with the teacher's word
function p1Tick(c, j) {
  if (!c.wait || !c.train) return;
  const now = shipNow(), d = caseDay(now), mn = now % 1440;
  if (!caseOpened('p1') || !playerShiftOn(d) || mn < DAY_SHIFT[0] || mn >= 900) return;
  const row = typeof ladderRow === 'function' && ladderRow('p1');
  c.by = (row && typeof ladderTeacher === 'function' && ladderTeacher(row, d)) || 'calder';
  caseShow(c, j);
  const said = typeof worksVoice === 'function' && worksVoice(c.by, 'train.p1.word');
  if (said && typeof worksSayAll === 'function') worksSayAll(c.by, said);
  else if (typeof worksSay === 'function') worksSay(c.by, 'Here\'s one the pipe kit won\'t settle. ' + c.title.replace(/^Head-scratcher: /, '') + '. When does it happen? That\'s the question. The logs are at the panels.');
}
CASE_KINDS.p1 = { name: 'When does it happen?', ladder: 'p1', noScan: true,
  fits: (cause, m) => !!cause.part && !!cause.line && P1_WHENS.has(cause.when) && caseBand(caseRank()) !== 'T1' && (caseLine(m.id, cause.line) || []).length >= 4,
  suspects: (j, seed, band) => [j.cause].concat(p1Pick(j, seed, band)),
  clues: (j, cause, sus) => p1Clues(j, cause, sus),
  bands: { T2: P1_BAND, T3: P1_BAND, T4: P1_BAND },
  sus: p1Sus, title: p1Title, card: p1Card, start: p1Start, wrong: p1Wrong, text: p1Text, view: p1View, tick: p1Tick,
  hint: c => caseText('case.hint.p1.1', 'Read the logs along the line: a machine that ran fine every hour isn\'t it.') };
CHIEF_NOTES.p1 = { title: 'When does it happen?', key: 'chief.p1', lines: [
  'Bad all day: something\'s worn. Bad at the busy hours: something can\'t keep up.',
  'Read the logs along the line. A machine that ran fine every hour isn\'t what\'s cutting it.'] };
if (typeof WORK_MECH !== 'undefined') WORK_MECH.p1 = { open() { /* the first case is staged (p1Stage); it shows at the next tick */ } };
if (typeof CAREER_LADDER !== 'undefined' && typeof ladderRow === 'function' && !ladderRow('p1'))   // 24 core's row, if it hasn't one (C2 may own it)
  CAREER_LADDER.push({ id: 'p1', name: 'When does it happen?', size: 'small', day: 12, tier: 2, rank: 'officer', needs: { trained: 'm9' }, by: ['calder', 'halloran-emeka'], stages: [{ uses: 0 }] });
const caseTracing = () => typeof WORK_MECH !== 'undefined' && !!WORK_MECH.m9;   // M3's tracing (24i) is in the build, not just its ladder row (C2's)
// the first case, staged at 16:00 on Day 11 (or the first 16:00 after, once your Tier 2 test is passed): 3-pump-1
// reserved (slot 21, held a week), its fault the pump; the logs from the day before. Busy, or no fault table yet: none,
// and the first roll case that fits is your first
function p1Stage(C) {
  if (C.p1 || !SHIP.works) return;
  const W = SHIP.works;
  if (W.tr && W.tr.p1 !== undefined || caseOpened('p1')) { C.p1 = 'none'; return; }   // an older save past it
  const now = shipNow(), m9 = caseTracing() && W.tr && W.tr.m9 !== undefined, t16 = m9 ? now : Math.floor((now - 960) / 1440) * 1440 + 960, d = caseDay(t16);   // after the lesson: from now
  if (now < 960 || d < 11 || !(W.rank !== 'junior' || W.test && W.test.passed)) return;
  if (caseTracing() && !(W.tr && W.tr.m9 !== undefined)) return;   // not before the tracing lesson's done: it reads this line on Day 12 (M3's ask)
  const m = machineById(P1_FIRST.machine), f = m && caseCauses(m).find(x => x.id === P1_FIRST.cause);
  if (!f || !f.line || !f.part || SHIP.jobs.some(j => j.machine === m.id && j.status !== 'done' && (j.claimedBy || j.case || j.reserved))) { C.p1 = 'none'; return; }
  const id = jobReserve(m.id, d, t16 % 1440, 21, { train: 'p1', tier: 2, until: t16 + 7 * 1440, cause: f.id }), j = id && SHIP.jobs.find(x => x.id === id);
  if (!j) return;
  delete j.make; delete j.makeMins; j.cause = f.id; j.parts = [f.part]; j.train = 'p1';
  const seed = machSeed('p1-first'), sus = [f.id].concat(p1Pick(j, seed, 'T2', P1_FIRST.decoys)).map((s, i) => [schedU(seed, i, 893), s]).sort((a, b) => a[0] - b[0]).map(x => x[1]);
  const clues = p1Clues(j, f.id, sus), r = caseSolve(sus, clues, 'T2', f.id, 'p1');
  if (r.why) { C.p1 = 'none'; jobRelease(21); return; }   // a decoy's log not fine and no other on the line: a plain repair
  const c = { id: 'c' + j.id, job: j.id, kind: 'p1', k: 0, band: 'T2', cause: f.id, sus, fewest: r.fewest, clues, got: [], crossed: [], known: [], calls: [], fits: 0, posted: t16, until: 0,
    wait: true, taken: false, talk: false, long: false, train: true, told: false, title: '' };
  C.open.push(c); j.case = c.id; C.p1 = c.id; C.n++;
  MACH_REV++;
}

// ---- 24k P2. Who saw what? (Day 15, a word from Tomas; plans/mechanics/p2-who-saw-what.html). A fault that comes and
// goes, that the crew noticed and you didn't: its suspects are causes on the same machine with a card in common and a
// different `when` (always, warm, peak, after-use, at-time, touched: shows only when the machine room's door goes).
// Witnesses are crew whose real plan had them awake in the machine's room or the next one (DECKS[n].map: rooms that
// touch it) during the fault's window: their minute is the middle of their stay (going to bed: as they settle); what
// they say is whether it was playing up then (the cause's real when) and whether the door went. "Playing up at t"
// crosses out the suspects that couldn't show then; "quiet at t" those that would have. At most one is mixed up (key
// 894): their plan had them by a machine of the same system on another deck when the real one was quiet, so what
// they say is about that one and crosses out nothing (the Roster shows where they were). Asked on their chat card
// ("Ask about the fault": caseAskButton and caseAskSay, section 20's chat card asks), the same answer every time
// (their lines from content/cases/p2.lines, by the minute they were there). Witnesses from key 1001. A roll case
// waits (the window is the next 12 hours to a minute in your shift, read from the plans when it's posted) and then
// shows. **Shut until Tomas's word** (the user's): no P2 case, Ask button or witness line until SHIP.works.said.p2 is
// set, when he (or Torres) has had his word with you at a meal you share from the day the p2 row opens. The first
// (staged at 16:00 on Day 14 once you're an Officer: 4-scrubber-2, or -1, slot 22, the bearing) shows then. ----
const P2_BAND = { sus: [3, 4], clues: [2, 4], fewest: 2, decks: 1 };   // the page's T2: 3-4 suspects, 2-3 witnesses and at most one mix-up (its later bands with their steps)
const P2_WAIT = 720, P2_MEALS = new Set(['breakfast', 'lunch', 'dinner']);
const P2_FIRST = { machines: ['4-scrubber-2', '4-scrubber-1'], cause: 'bearing', decoys: ['filter', 'panel'] };
const caseShares = (a, b) => String(a.shows).split('|').some(s => String(b.shows).split('|').includes(s));   // two causes with a card in common
// rooms on deck n that touch room r (and r): who'd hear a machine in it
const CASE_NEAR = new Map();
function caseRoomsNear(n, r) {
  const k = n + '|' + r; if (CASE_NEAR.has(k)) return CASE_NEAR.get(k);
  const map = DECKS[n] && DECKS[n].map || [], rooms = DECKS[n] && DECKS[n].rooms || {}, out = new Set([r]);
  map.forEach((row, j) => { for (let i = 0; i < row.length; i++) if (row[i] === r) for (const [a, b] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
    const c = (map[j + b] || '')[i + a]; if (c && c !== r && rooms[c] && !rooms[c].void && !rooms[c].spine && c !== '@') out.add(c); } });
  CASE_NEAR.set(k, out); return out;
}
// did the door of a machine's room go at minute t (someone came or went within five minutes, from the plans)
const CASE_DOOR = new Map();
function caseDoor(m, t) {
  const d = caseDay(t), k = m.deck + '|' + m.room + '|' + d;
  if (!CASE_DOOR.has(k)) {
    const xs = [];
    for (const p of schedPeople()) for (const s of planDay(p, d)) { const pl = s.deck === m.deck && s.placeId && placeById(s.placeId); if (pl && pl.room === m.room) xs.push(s.from, s.to); }
    CASE_DOOR.set(k, xs); if (CASE_DOOR.size > 40) CASE_DOOR.delete(CASE_DOOR.keys().next().value);
  }
  return CASE_DOOR.get(k).some(x => Math.abs(x - t) <= 5);
}
// is cause f playing up at minute t
const caseShows = (m, f, t) => !!f && (f.when === 'touched' ? caseDoor(m, t) : !!caseWhenHours(m, f.when, caseDay(t))[Math.floor((t % 1440) / 60)]);
const p2Said = () => { const W = SHIP.works, C = W && caseState(), a = W && W.said && W.said.p2, b = C && C.said && C.said.p2; return Number.isInteger(a) ? a : Number.isInteger(b) ? b : null; };
const p2Row = () => { try { return typeof worksIsOpen === 'function' ? worksIsOpen('p2') : Object.values((SHIP.works && SHIP.works.op) || {}).some(x => Array.isArray(x) && x.includes('p2')); } catch (e) { return false; } };
const p2Decoys = (m, f) => caseCauses(m).filter(x => x.id !== f.id && x.part && !x.load && !x.setting && x.when && x.when !== f.when && !/^with:/.test(x.when) && caseShares(x, f));
// crew awake in the machine's room or the next during [t0, t1): { p, t, pl }, one per stay
function p2Seen(m, t0, t1) {
  const near = caseRoomsNear(m.deck, m.room), out = [];
  for (const p of schedPeople()) {
    if (typeof movedOff === 'function' && movedOff(p.id)) continue;
    for (let d = caseDay(t0); d <= caseDay(t1 - 1); d++) for (const s of planDay(p, d)) {
      if (s.deck !== m.deck || s.act === 'commute' || (s.act === 'sleep' && s.from % 1440 === 0)) continue;   // a sleep carried over midnight: asleep
      const pl = s.placeId && placeById(s.placeId); if (!pl || !near.has(pl.room)) continue;
      const a = Math.max(s.from, t0), b = Math.min(s.to, t1); if (b - a < 10) continue;
      if (s.act === 'sleep' && s.from < t0) continue;   // asleep already
      out.push({ p: p.id, t: s.act === 'sleep' ? s.from + 3 : Math.floor((a + b) / 10) * 5, pl: pl.id });
    }
  }
  return out;
}
// the witnesses for a case on job j over [t0, t1): each crosses out something new and none alone settles it; then
// at most one mix-up (first: always if there is one; else key 894 half the time)
function p2Witnesses(j, cause, sus, seed, t0, t1, first) {
  const m = machineById(j.machine), F = id => caseCauses(m).find(x => x.id === id), fc = F(cause), decoys = sus.filter(s => s !== cause);
  const all = p2Seen(m, t0, t1).map((x, i) => [schedU(seed, i, 1001), x]).sort((a, b) => a[0] - b[0]).map(x => x[1]);
  const got = new Set(), used = new Set(), out = [];
  for (const x of all) {
    if (used.has(x.p) || got.size === decoys.length || out.length >= 3) continue;
    const saw = caseShows(m, fc, x.t), kills = decoys.filter(s => caseShows(m, F(s), x.t) !== saw);
    if (!kills.length || kills.length === decoys.length || kills.every(s => got.has(s))) continue;
    out.push({ id: 'w' + out.length, type: 'person', src: { ask: x.p, t: x.t, saw: saw ? 1 : 0, door: caseDoor(m, x.t) ? 1 : 0, pl: x.pl }, at: null, kills });
    used.add(x.p); kills.forEach(s => got.add(s));
  }
  if (first || schedU(seed, 0, 894) < .5) {
    const sys = MACHINE_KINDS[m.kind].sys, others = machineList().filter(o => o.deck !== m.deck && o.room && MACHINE_KINDS[o.kind].sys === sys);
    const mix = [];
    for (const o of others) for (const x of p2Seen(o, t0, t1)) if (!used.has(x.p) && !caseShows(m, fc, x.t)) mix.push({ ...x, o: o.id });   // there when the real one was quiet
    const same = mix.filter(x => machineById(x.o).kind === m.kind), pool = same.length ? same : mix;   // the same kind of machine first
    if (pool.length) { const x = pool[Math.floor(schedU(seed, 1, 894) * pool.length)]; out.push({ id: 'x0', type: 'person', src: { ask: x.p, t: x.t, saw: 1, door: 0, pl: x.pl, mix: x.o }, at: null, kills: [] }); }
  }
  return out;
}
// the first minute 12 hours on that's in your shift: a roll case's window ends and it shows
function p2ShowAt(t0) { let t = Math.ceil((t0 + P2_WAIT) / 30) * 30; for (let n = 0; n < 400; n++, t += 30) { const mn = t % 1440; if (playerShiftOn(caseDay(t)) && mn >= DAY_SHIFT[0] && mn < 900) return t; } return t; }
// a witness's words: their own line from content/cases/p2.lines (by the minute they were there, so the same every
// time), else plain
function p2Line(c, k) {
  if (k.type !== 'person' || !k.src || !k.src.ask) return null;
  const s = k.src, pl = placeById(s.pl), mm = machineById(s.mix || (caseJob(c) || {}).machine);
  const rn = pl ? roomName(pl.deck, pl.room) || 'corridor' : 'corridor', place = /^(bunk|cabin|guest cabin|quarters)\b/.test(rn) ? rn.replace(/^./, x => x.toUpperCase()) : 'the ' + rn, machine = 'the ' + (mm ? MACHINE_KINDS[mm.kind].name.toLowerCase() : 'machine'), time = hhmm(s.t % 1440);
  const kind = s.mix ? 'ask.mixup' : (s.saw ? 'ask.saw.' : 'ask.quiet.') + (s.door ? 'door' : 'still');
  let l = null; try { l = typeof lineFor === 'function' ? lineFor(s.ask, kind, { t: s.t, time, place, machine, peek: true }) : null; } catch (e) { l = null; }
  if (l && l.text) return l.text;
  return s.mix ? 'It was playing up at ' + time + '! I was in ' + place + '. Heard ' + machine + ' clear as day.'
    : s.saw ? (s.door ? 'It was playing up at ' + time + ', just as someone came through the door.' : 'It was playing up at ' + time + '. I was in ' + place + '. Nobody came or went.')
    : s.door ? 'Quiet at ' + time + ', and people were in and out of ' + place + '.' : 'Quiet as anything at ' + time + ', in ' + place + '.';
}
// the chat card's button and answer (section 20 asks, one line each): only while a P2 case is showing and the person
// is one of its witnesses (or its mix-up), and never before Tomas's word
function p2CaseOf(pid) {
  if (p2Said() == null) return null;
  const C = SHIP.works && caseState(); if (!C) return null;
  for (const c of C.open) if (c.kind === 'p2' && !c.wait) { const k = c.clues.find(x => x.src && x.src.ask === pid); if (k) return { c, k }; }
  return null;
}
function caseAskButton(p) { return p && p2CaseOf(p.id) ? { id: 'case-ask', label: caseText('case.ask', 'Ask about the fault') } : null; }
function caseAskSay(p) {
  const x = p && p2CaseOf(p.id); if (!x) return p2Said() != null ? caseText('case.ask.none', 'Didn\'t notice a thing. Sorry.') : null;
  caseClue(x.c.id, x.k.id);
  return p2Line(x.c, x.k);
}
function p2Title(c, j) {                                 // "Air scrubber 2 on Deck 4 rattles now and then": the card the suspects share
  const m = machineById(j.machine), fs = c.sus.map(s => caseCauses(m).find(x => x.id === s)).filter(Boolean);
  const shows = (String(fs[0] && fs[0].shows || 'acts up').split('|').find(s => fs.every(f => String(f.shows).split('|').includes(s))) || 'acts up');
  return caseText('case.title.p2', '{machine} on Deck {deck} {shows} now and then', { machine: caseMachName(j), deck: m.deck, shows });
}
function p2View(c) {
  const got = c.clues.filter(k => c.got.includes(k.id) && k.src && k.src.ask); if (!got.length) return [];
  const nm = id => { const p = schedPeople().find(x => x.id === id); return p ? shortName(p) : id; };
  return [{ kind: 'text', text: caseText('case.p2.head', 'What people said (tap a name if it doesn\'t fit)') },
    devChips(got.map(k => ({ label: nm(k.src.ask) + ', ' + hhmm(k.src.t % 1440), on: !(c.doubt || []).includes(k.id), action: { app: caseApp(), do: 'case:doubt', arg: c.id + '|' + k.id } })))];
}
// once a ship minute: a roll case shows once its window has passed; the first waits for Tomas's word (p2Word)
function p2Tick(c, j) {
  if (!c.wait || c.train) return;
  const now = shipNow(), mn = now % 1440;
  if (now >= p2ShowAt(c.posted) && playerShiftOn(caseDay(now)) && mn >= DAY_SHIFT[0] && mn < 900) caseShow(c, j);
}
CASE_KINDS.p2 = { name: 'Who saw what?', ladder: 'p2', open: () => p2Row() && p2Said() != null,   // the user's gate: never before Tomas's word
  fits: (cause, m) => !!cause.part && !!cause.when && !/^with:/.test(cause.when) && caseBand(caseRank()) !== 'T1' && p2Decoys(m, cause).length >= 2,
  suspects: (j, seed, band) => { const m = machineById(j.machine), f = caseCauses(m).find(x => x.id === j.cause), n = caseBandOf('p2', band).sus[1] - 1;
    return [j.cause].concat(p2Decoys(m, f).map((x, i) => [schedU(seed, i, 892), x.id]).sort((a, b) => a[0] - b[0]).map(x => x[1]).slice(0, n)); },
  clues: (j, cause, sus, seed) => { const t0 = caseNow(); return p2Witnesses(j, cause, sus, seed, t0, p2ShowAt(t0), false); },
  bands: { T2: P2_BAND, T3: P2_BAND, T4: P2_BAND },
  wait: () => true, tick: p2Tick, title: p2Title, text: p2Line, view: p2View,
  hint: c => caseText('case.hint.p2.1', 'Ask who was there, and check they were: the Roster says where people really were.') };
CHIEF_NOTES.p2 = { title: 'Who saw what?', key: 'chief.p2', lines: [
  'Ask who was there, and check they were.',
  'Nobody lies; someone may be mixed up. The Roster says where they really were.'] };
if (typeof WORK_MECH !== 'undefined') WORK_MECH.p2 = { open() { /* Tomas's word comes at the next meal you share (p2Word) */ } };
if (typeof CAREER_LADDER !== 'undefined' && typeof ladderRow === 'function' && !ladderRow('p2'))   // 24 core's row, if it hasn't one (C2 may own it)
  CAREER_LADDER.push({ id: 'p2', name: 'Who saw what?', size: 'small', day: 15, tier: 2, rank: 'officer', needs: null, by: ['tomas', 'torres-zeke'], stages: [{ uses: 0 }] });
// the first case, staged at 16:00 on Day 14 (or the first 16:00 after) once you're an Officer: 4-scrubber-2 (or 1),
// slot 22, held a week, its fault the bearing; its witnesses are found when it shows, at Tomas's word
function p2Stage(C) {
  if (C.p2 || !SHIP.works) return;
  const W = SHIP.works;
  if (W.tr && W.tr.p2 !== undefined || p2Said() != null) { C.p2 = 'none'; return; }   // an older save past it
  const now = shipNow(), t16 = Math.floor((now - 960) / 1440) * 1440 + 960, d = caseDay(t16);
  if (now < 960 || d < 14 || W.rank === 'junior') return;
  const busy = id => SHIP.jobs.some(j => j.machine === id && j.status !== 'done' && (j.claimedBy || j.case || j.reserved));
  const m = P2_FIRST.machines.map(machineById).find(x => x && !busy(x.id)), f = m && caseCauses(m).find(x => x.id === P2_FIRST.cause);
  const sus = f ? [f.id].concat(P2_FIRST.decoys.filter(s => p2Decoys(m, f).some(x => x.id === s))) : [];
  if (!f || !f.part || sus.length < 3) { C.p2 = 'none'; return; }
  const id = jobReserve(m.id, d, 960, 22, { train: 'p2', tier: 2, until: t16 + 7 * 1440, cause: f.id }), j = id && SHIP.jobs.find(x => x.id === id);
  if (!j) return;
  delete j.make; delete j.makeMins; j.cause = f.id; j.parts = [f.part]; j.train = 'p2';
  const seed = machSeed('p2-first'), order = sus.map((s, i) => [schedU(seed, i, 893), s]).sort((a, b) => a[0] - b[0]).map(x => x[1]);
  const c = { id: 'c' + j.id, job: j.id, kind: 'p2', k: 0, band: 'T2', cause: f.id, sus: order, fewest: 2, clues: [], got: [], crossed: [], known: [], calls: [], fits: 0, posted: t16, until: 0,
    wait: true, taken: false, talk: false, long: false, train: true, told: false, title: '' };
  C.open.push(c); j.case = c.id; C.p2 = c.id; C.n++;
  MACH_REV++;
}
// Tomas's word (or Torres's), once the p2 row has opened: at a meal you share (you in the room where they're eating),
// from the day the row opened; then SHIP.works.said.p2 = today, and the first case shows with its witnesses
function p2Word(C) {
  if (p2Said() != null || !p2Row() || typeof player === 'undefined' || !player || !deckDef) return;
  const row = typeof ladderRow === 'function' && ladderRow('p2'), now = shipNow();
  let here = null; try { const [ci, cj] = player.here(); here = roomAt(ci, cj); } catch (e) { return; }
  for (const id of row ? row.by : ['tomas', 'torres-zeke']) {
    const p = schedPeople().find(x => x.id === id), w = p && planWhere(p, now), pl = w && w.placeId && placeById(w.placeId);
    if (!pl || !P2_MEALS.has(w.act) || w.deck !== deckDef.num || pl.room !== here) continue;
    p2Said1(C, id, now);
    return;
  }
}
function p2Said1(C, by, now) {
  const W = SHIP.works, d = caseDay(now); W.said = W.said || {}; W.said.p2 = d; C.said = { ...(C.said || {}), p2: d };   // also in the cases, while 24 core's cleaner doesn't keep said
  const said = typeof worksVoice === 'function' && worksVoice(by, 'train.p2.word');
  const c = C.p2 && caseById(C.p2), j = c && caseJob(c), thing = j && machineById(j.machine) ? MACHINE_KINDS[machineById(j.machine).kind].name.toLowerCase().replace(/^air /, '') : 'fault';
  if (said && typeof worksSayAll === 'function') worksSayAll(by, said);
  else if (typeof worksSay === 'function') worksSay(by, 'You\'re asking around about the ' + thing + '? Ask who sleeps near it. And check they were in.');
  if (c && j && c.wait) p2ShowFirst(C, c, j, now);
  MACH_REV++;
}
function p2ShowFirst(C, c, j, now) {                     // its witnesses over [16:00 the day before, now); none fair: a plain repair
  c.by = c.by || 'tomas';
  for (let k = 0; k < CASE_TRIES; k++) {
    const seed = schedU(machSeed(j.machine), caseDay(now), 882 + k) * 4294967296 | 0, clues = p2Witnesses(j, c.cause, c.sus, seed, c.posted, now, true), r = caseSolve(c.sus, clues, 'T2', c.cause, 'p2');
    if (!r.why) { c.clues = clues; c.fewest = r.fewest; c.k = k; caseShow(c, j); return true; }
  }
  caseClose(c, 0); delete j.case; if (typeof jobRelease === 'function') jobRelease(22); C.p2 = 'none';
  return false;
}

// ---------------------------------------------------------------------
// 24e TUNING (M5, seat M2, 0.51.x; plans/mechanics/m5-tuning.html). Some faults are a machine out of adjustment: an
// oven running hot, a light relay chattering, a cart dock charging slow. Section 17 (seat S) keeps the drift
// (SHIP.machines[id].drift, -3..+3, 0 settled; machineDrift(id), tuneSet(id, v)) and posts a 'tune' job for a drift of
// 2+; this block is the job: at the machine's panel a `turn` step (section 15) with − and +, each press moving the real
// setting one step so the machine's look answers on the deck (flicker, dim, blink); settled (0) and it's done. The card
// shows words only. Taught on Day 4 (ladder row m5): the row's opening drifts both ovens two steps hot; the teacher
// tunes Oven 1 while you watch, then Oven 2 is yours. The crew tune what you leave (section 17's crew walk, 15 minutes).
// Removable: without this block (or without section 17's tuneSet) no tune job is ever made and m5 never opens.
// Saved: nothing of its own (the drift is section 17's, the job in ship.jobs, the uses in ship.works.use.m5). No R().
// Stage 2 (a scrubber's two settings, Officer) and stage 3 (the scanner) come with Step 3.
const TUNE_STEPS = [-3, 3];
const TUNE_WORD = {                                      // words on the card, by kind (the writer's tune.word.<kind>.<n> win)
  oven: ['cold', 'a little cool', 'steady', 'a little hot', 'running hot'], range: ['cold', 'a little cool', 'steady', 'a little hot', 'running hot'],
  lights: ['dim', 'a little dim', 'steady', 'flickering a little', 'flickering fast'], cartdock: ['charging slow', 'a little slow', 'steady', 'blinking a little', 'blinking fast'] };
const tuneDrift = id => typeof machineDrift === 'function' ? machineDrift(id) || 0 : 0;
function tuneWord(kind, v) {
  const k = Math.max(0, Math.min(4, v + 2)), w = (TUNE_WORD[kind] || TUNE_WORD.oven)[k];
  return worksText('tune.word.' + kind + '.' + (v > 0 ? '+' : '') + Math.max(-2, Math.min(2, v)), w);
}
// the job's one stop: the machine's panel, a turn from the real drift; each press sets the machine at once
function tuneStops(j) {
  const m = machineById(j.machine); if (!m) return [];
  const label = machineLabel(m).split(',')[0];
  return [{ deck: m.deck, placeId: panelPlace(m.id), mins: 1, tag: 'job', how: 'turn',
    opts: { label, v: tuneDrift(m.id), min: TUNE_STEPS[0], max: TUNE_STEPS[1], by: 1,
      text: worksText('tune.card', 'Watch the machine, not the dial. It\'s {word}.', { word: tuneWord(m.kind, tuneDrift(m.id)) }),
      onTurn: v => { if (typeof tuneSet === 'function') tuneSet(m.id, v); return label + ': ' + tuneWord(m.kind, v) + '.'; },
      ok: v => v === 0, gauge: null } }];
}
// finished: the crew's (or the teacher's) settle it; yours counts as a use (the training's too)
function tuneDone(j, t, by) {
  if (by !== 'you') { if (typeof tuneSet === 'function') tuneSet(j.machine, 0); return; }
  worksUse('m5');
  const c = SHIP.works && SHIP.works.cur;
  if (j.train === 'm5' && c && c.id === 'm5') worksTeach('m5', 'brennan', 'do.done', ['There. That\'s my oven back.', 'Here. Have a biscuit, you\'ve earned it.']);
}
// a tune job, ready to push (section 17 posts its own with jobMake('tune', { machine, deck, room, h, found }))
function tuneJob(id, t, o = {}) {
  const m = machineById(id); if (!m) return null;
  const j = jobMake('tune', { id: 'tune' + (o.slot || '') + ':' + id + '@' + Math.floor(t / 60), machine: id, deck: m.deck, room: m.room, h: Math.floor(t / 60),
    title: worksText('tune.title', 'Tune: {machine} ({word})', { machine: machineLabel(m).split(',')[0], word: tuneWord(m.kind, tuneDrift(id)) }), tier: MACHINE_KINDS[m.kind].tier || 1,
    ...(o.slot ? { reserved: o.slot, until: (worksDay(t) - 1) * 1440 + DAY_SHIFT[1] } : {}), ...(o.train ? { train: o.train } : {}) });
  j.posted = j.found = t;
  return j;
}
if (typeof jobKindAdd === 'function' && typeof tuneSet === 'function') jobKindAdd('tune', { tier: 1, work: 0, text: 'Tune',
  stops: tuneStops, done: tuneDone,
  crew: { can: p => !!p.work && p.work.place === 'work:works', mins: 15 } });
// the ladder row (m5): opening it drifts both ovens two steps hot (Brennan's "runs hot"); the training's two jobs are
// this block's own, held in the teacher's slot: Oven 1 the teacher's, Oven 2 yours
const TUNE_TRAIN = ['3-oven-1', '3-oven-2'];
if (JOB_KINDS.tune) WORK_MECH.m5 = {
  open() { for (const id of TUNE_TRAIN) if (machineById(id) && Math.abs(tuneDrift(id)) < 2) tuneSet(id, 2); },
  reserve(d, at, slot, o = {}) {
    const id = TUNE_TRAIN[o.yours ? 1 : 0], t = (d - 1) * 1440 + at; if (!machineById(id)) return null;
    if (!tuneDrift(id)) tuneSet(id, 2);                  // (a reload, or the crew got there first: drifted again for the lesson)
    SHIP.jobs = SHIP.jobs.filter(x => !(x.reserved === slot && heldForYou(x) && !x.claimedBy) && !(x.kind === 'tune' && x.machine === id && x.claimedBy !== 'you' && x.status !== 'done'));   // the oven's own tune job, even one a crew member took: the lesson stands for it
    const j = tuneJob(id, t, { slot, train: o.train || 'm5' }); if (!j) return null;
    SHIP.jobs.push(j); if (typeof MACH_REV !== 'undefined') MACH_REV++;
    return j.id;
  },
  watch: 10,                                             // ship minutes watching the teacher settle Oven 1
};

// ---------------------------------------------------------------------
// 24f INCIDENTS (M6, seat M2, 0.51.x; plans/mechanics/m6-incidents.html). About once a week, a small incident from
// the machines, an hour or two on one deck: make it safe (a valve chosen from the pipe, the lift's brake turned, the
// galley plant's alarm held), clean up (mop the puddle, check the car, clear the air), then fix the cause (an ordinary
// job: a joint at the burst, or the lift's or the galley plant's repair, found by whoever cleared it). Your first is
// the training (ladder row m6, Day 8, a burst pipe on Deck 4 at 10:30, Calder: an urgent call, not a Mail
// appointment; she walks you to the pipe, then it's yours, and you're trained when the joint is fitted). After that
// the week's incident (workdays 09:00-15:30, never an event day, the morning on a tradition evening's day, never a
// test-job day) is on the board, held for you 30 minutes when you're on shift, then the crew's (25-40 minutes). The
// stuck lift is the fallback from the page (the lead's call): the lift stalls, nobody inside; "check the car".
// Section 17's machine side (seat S): machineFault(id, cond), liftStuck(on), jointJobPost({ deck, placeId }).
// Drawn: a puddle (two flat discs, one instanced draw call) and a smoke wisp (instanced quads, one draw call), only
// during an incident on your deck. Saved: SHIP.works.inc = { plan: { week: [kind, day, minute, deck, done] },
// open: null | { kind, deck, at, train, safe, j }, fix?: { id, kind } (the fix to note when it's done) } (ship.works.inc;
// old weeks dropped). Hash keys 870-873. No R(). (Step 3: promotion days to be kept clear like test-job days.)
const INC_KINDS = ['burst', 'lift', 'alarm'];
const INC_FIRST = { day: 8, at: 630, kind: 'burst', deck: 4 };   // your first: Day 8 (a Monday), 10:30, Deck 4
const INC_WIN = [540, 930], INC_MORNING = 690;           // 09:00-15:30; before 11:30 on a tradition evening's day
const INC_HELD = 30, INC_LIFT = 20;                      // held for you 30 minutes; the lift stays stuck at most 20
const INC_LIFT_M = '5-mainlift-1', INC_ALARM_M = '3-galleyplant-1';
const INC_TITLE = { burst: 'Burst pipe, Deck {deck}', lift: 'The main lift is stuck', alarm: 'Galley alarm' };
const incWorks = p => !!p.work && p.work.place === 'work:works';
const incWeek = d => Math.floor((d - 1) / 7);
const incPlace = ids => [].concat(ids).find(id => placeById(id)) || null;
const incAlarmAt = () => incPlace(['3-galleyplant-alarm', '3-extractor-alarm']);
function incState() {
  const W = SHIP.works; if (!W) return null;
  if (!W.inc || typeof W.inc !== 'object') W.inc = { plan: {}, open: null };
  return W.inc;
}
// a save's inc read back (24 core's worksClean keeps only its own keys, so this block reads its part itself)
function incClean(s, d = worksDay(shipNow())) {
  const out = { plan: {}, open: null }; if (!s || typeof s !== 'object') return out;
  if (s.fix && typeof s.fix.id === 'string' && INC_KINDS.includes(s.fix.kind)) out.fix = { id: s.fix.id.slice(0, 80), kind: s.fix.kind };
  if (s.plan && typeof s.plan === 'object') for (const w in s.plan) { const e = s.plan[w]; if (/^\d{1,4}$/.test(w) && +w >= incWeek(d) && Array.isArray(e) && (e.length === 0 || INC_KINDS.includes(e[0]) && Number.isInteger(e[1]) && Number.isInteger(e[2]) && [3, 4, 5].includes(e[3]))) out.plan[w] = e.length ? [e[0], e[1], e[2], e[3], e[4] ? 1 : 0] : []; }
  const o = s.open; if (o && typeof o === 'object' && INC_KINDS.includes(o.kind) && [3, 4, 5].includes(o.deck) && Number.isFinite(o.at))
    out.open = { kind: o.kind, deck: o.deck, at: o.at, train: !!o.train, safe: !!o.safe, j: typeof o.j === 'string' ? o.j : null };
  return out;
}
(() => { const s = SAVED && SAVED.ship && SAVED.ship.works; if (SHIP.works && s && s.inc) SHIP.works.inc = incClean(s.inc); })();
// is a day out: a ship-wide event (not a tradition), your day off, a test job's day
const incShipEvent = d => { try { return eventsOn(d).some(e => e.ev && e.ev.when && e.ev.when.ship); } catch (e) { return false; } };
const incEvening = d => { try { return eventsOn(d).some(e => Array.isArray(e.at) && e.at[0] >= 1020); } catch (e) { return false; } };
const incDayOk = (d, W) => weekday(d) < 5 && playerShiftOn(d) && !incShipEvent(d) && !(W.test && W.test.day === d);
const incWear = id => { const s = SHIP.machines[id]; return s ? (100 - s.cond) / 100 : 0; };
function incWeights() {                                  // by the machines' wear: the pipe valves, the lift, the galley plant
  const vs = machineList().filter(m => m.kind === 'valve'), v = vs.length ? vs.reduce((a, m) => a + incWear(m.id), 0) / vs.length : 0;
  return { burst: 1 + v, lift: 1 + incWear(INC_LIFT_M), alarm: 1 + incWear(INC_ALARM_M) };
}
// the week's incident, planned once (the first time it's asked in that week) and saved: [kind, day, minute, deck, done]
// or [] (none that week). Week 1 (Days 8-14) has your first, the training's, so no other
function incPlan(w) {
  const I = incState(); if (!I) return null;
  if (I.plan[w]) return I.plan[w];
  const W = SHIP.works, days = [0, 1, 2, 3, 4].map(k => w * 7 + 1 + k).filter(d => incDayOk(d, W));
  if (w < 2 || !days.length) return I.plan[w] = [];
  const seed = machSeed('incident'), d = days[Math.floor(schedU(seed, w, 870) * days.length) % days.length];
  const hi = incEvening(d) ? INC_MORNING : INC_WIN[1], at = INC_WIN[0] + Math.floor(schedU(seed, w * 7 + 1, 870) * ((hi - INC_WIN[0]) / 10 + 1)) * 10;
  const wt = incWeights(), sum = INC_KINDS.reduce((a, k) => a + wt[k], 0); let u = schedU(seed, w, 871) * sum, kind = INC_KINDS[0];
  for (const k of INC_KINDS) { if (u < wt[k]) { kind = k; break; } u -= wt[k]; }
  const deck = kind === 'burst' ? [3, 4, 5][Math.floor(schedU(seed, w, 872) * 3) % 3] : kind === 'lift' ? 5 : 3;
  return I.plan[w] = [kind, d, Math.min(at, hi), deck, 0];
}
// the incident's stops: make it safe, clean up (the burst's fix is posted at the end; the alarm's hood looked at)
function incStops(j) {
  const n = j.deck, wet = (DECKS[n] && DECKS[n].wet) || [n + '-wet-1', n + '-wet-2'];
  if (j.walk) return [{ deck: n, placeId: incPlace(n + '-valve-panel'), mins: 1, tag: 'walk', how: 'look', opts: { secs: 3, text: worksText('inc.walk', 'Water across the corridor floor. The pipe runs along the wall to the valves.') } }];
  if (j.inc === 'burst') {
    const line = (DECKS[n] && DECKS[n].valveLine) || [1, 2, 3].map(k => n + '-valve-' + k);
    return [{ deck: n, placeId: incPlace(n + '-valve-panel'), mins: 1, tag: 'safe', how: 'choose', opts: { title: worksText('inc.burst.safe.title', 'Which valve?'),
        text: worksText('inc.burst.safe', 'The pipe runs from valve 1 to valve {n}, then on down the corridor to the wet. Close one.', { n: line.length }),
        options: line.map((id, k) => ({ id, label: worksText('inc.valve', 'Valve {k}', { k: k + 1 }) })) } },
      ...wet.filter(id => placeById(id)).map(id => ({ deck: n, placeId: id, mins: 3, tag: 'clean', how: 'hold' }))];
  }
  if (j.inc === 'lift') return [{ deck: 5, placeId: incPlace('5-lift-brake'), mins: 1, tag: 'safe', how: 'turn', opts: { label: worksText('inc.lift.brake', 'Brake release'), v: 0, min: 0, max: 3, by: 1,
        onTurn: v => v >= 3 ? worksText('inc.lift.free', 'The brake lets go. The car settles to Deck 4.') : v > 0 ? worksText('inc.lift.turning', 'The wheel turns. Keep going.') : null, ok: v => v >= 3, gauge: null } },
      { deck: 4, placeId: incPlace(['4-lift-1', '4-lift-2']), mins: 2, tag: 'clean', how: 'hold' }];
  return [{ deck: 3, placeId: incAlarmAt(), mins: 1, tag: 'safe', how: 'hold' },
    { deck: 3, placeId: incPlace('3-vent-1'), mins: 1, tag: 'clean', how: 'wait', opts: { mins: 5, label: worksText('inc.alarm.vent', 'Vents open: the air clears in a few minutes') } },
    { deck: 3, placeId: incPlace(['3-vent-1']), mins: 1, tag: 'clean', how: 'look', opts: { secs: 3, text: worksText('inc.alarm.hood', 'The hood\'s scorched but sound. The galley plant\'s filter is choked.') } }];
}
// a step of yours: the right valve (the nearest upstream of the wet: the last on the line); a wrong one leaves it
// running (section 17's def.veto: the stop stays undone) and you pick again
function incStepDone(j, k, res) {
  const st = incStops(j)[k], I = incState(), O = I && I.open; if (!st) return true;
  if (st.tag === 'safe' && j.inc === 'burst') {
    const line = (DECKS[j.deck] && DECKS[j.deck].valveLine) || [], pick = res && res.pick, right = pick === line[line.length - 1];
    const say = right ? null : line.includes(pick) ? ['safe.wrong', 'Still running. That one shuts the whole wing. Follow the pipe: the closest one upstream of the wet.'] : null;
    if (say) { const c = SHIP.works.cur; if (j.train && c && c.id === 'm6') worksTeach('m6', c.by, say[0], say[1]); else try { toast(j.title, worksText('inc.burst.' + say[0], say[1])); } catch (e) { /* no UI */ } return false; }
  }
  if (st.tag === 'safe' && O && O.j === j.id) { O.safe = true; if (j.inc === 'lift' && typeof liftStuck === 'function') liftStuck(false); simNote('incident', { id: j.inc, step: 'safe', by: 'you' }); worksXp(j.train ? 0 : 2); }   // first on the scene: +2
  if (st.tag === 'safe' && j.train) worksTeach('m6', SHIP.works.cur && SHIP.works.cur.by || 'calder', 'do.safe', ['Good. That\'s it off. Now the mop.']);
  return true;
}
// the incident cleared (by you or the crew): the puddle and the smoke go, the lift runs, the fix is posted
function incDone(j, t, by) {
  const I = incState(); if (j.walk || !I) return;
  const O = I.open && I.open.j === j.id ? I.open : null; I.open = O ? null : I.open;
  if (typeof liftStuck === 'function' && j.inc === 'lift') liftStuck(false);
  simNote('incident', { id: j.inc, step: 'clean', by });
  let fix = null;
  if (j.inc === 'burst') { const wet = incPlace((DECKS[j.deck] && DECKS[j.deck].wet) || [j.deck + '-wet-1']); fix = typeof jointJobPost === 'function' && wet ? jointJobPost({ placeId: wet, incident: j.inc }) : null; }
  else { const f = typeof machineFound === 'function' ? machineFound(j.inc === 'lift' ? INC_LIFT_M : INC_ALARM_M, by) : null; fix = f && f.id; }
  j.fix = fix || null;                                  // the fix's job id (saved with the job)
  if (fix) I.fix = { id: fix, kind: j.inc };            // simNote('incident', { step: 'fixed' }) when it's turned in (the clock)
  if (by === 'you') {
    worksUse('m6');
    const F = fix && SHIP.jobs.find(x => x.id === fix), c = SHIP.works.cur;
    if (F) { F.leave = Math.max(INC_HELD, (worksDay(t) - 1) * 1440 + DAY_SHIFT[1] - t); F.incFix = j.inc; }
    if (F && j.train && c && c.id === 'm6' && c.j === j.id) { F.reserved = j.reserved; F.until = j.until; F.train = 'm6'; c.j = F.id;   // the training ends at the fix: trained when it's turned in
      worksTeach('m6', c.by, 'do.fix', ['Now the cause. A seal from stores, and fit it at the burst. I\'ll watch.']); }
  }
  if (typeof MACH_REV !== 'undefined') MACH_REV++;
  incFx();
}
// an incident's job, ready to push: { kind: 'incident', inc, deck, first?, walk? } (o.slot: held in the training's slot)
function incJob(kind, deck, t, o = {}) {
  const j = jobMake('incident', { id: 'incident' + (o.slot || '') + ':' + kind + deck + (o.walk ? 'w' : '') + '@' + Math.floor(t / 60), inc: kind, deck, room: null, h: Math.floor(t / 60), urgency: 2,
    title: '! ' + worksText('inc.title.' + kind, INC_TITLE[kind], { deck }) + (o.walk ? ': ' + worksText('inc.with', 'with {name}', { name: worksFirst(o.by || 'calder') }) : ''),
    ...(o.walk ? { walk: true } : {}), ...(o.slot ? { reserved: o.slot, until: (worksDay(t) - 1) * 1440 + DAY_SHIFT[1] } : { leave: o.held ? INC_HELD : 1 }), ...(o.train ? { train: o.train } : {}) });
  j.posted = j.found = t;
  const P = placeById(jobStops(j).map(s => s.places && s.places[0]).find(Boolean)); if (P) j.room = P.room;
  return j;
}
// an incident starts: the machine side, the look, and (unless it's the training's, which holds its own) the job on the
// board, held for you if you're trained and on shift (the toast, the top card), else the crew's
function incStart(kind, deck, t, train) {
  const I = incState(); if (!I || I.open) return null;
  I.open = { kind, deck, at: t, train: !!train, safe: false, j: null };
  if (kind === 'lift') { if (typeof machineFault === 'function') machineFault(INC_LIFT_M, 40); if (typeof liftStuck === 'function') liftStuck(true, t + INC_LIFT); }
  if (kind === 'alarm' && typeof machineFault === 'function') machineFault(INC_ALARM_M, 40);
  simNote('incident', { id: kind, step: 'start', deck, by: null });
  if (!train) incPost(t);
  if (typeof MACH_REV !== 'undefined') MACH_REV++;
  incFx(); return I.open;
}
function incPost(t, by) {                                // the open incident's job on the board
  const I = incState(), O = I && I.open; if (!O || O.j) return null;
  const W = SHIP.works, d = worksDay(t), mine = W.tr.m6 !== undefined && playerShiftOn(d) && t - (d - 1) * 1440 < DAY_SHIFT[1];
  const j = incJob(O.kind, O.deck, t, { held: mine });
  SHIP.jobs.push(j); O.j = j.id;
  if (mine && t >= shipNow() - 1) try { toast(j.title, worksText('inc.call.' + O.kind, 'It\'s on the board, top of the list.')); } catch (e) { /* no UI */ }
  return j.id;
}
if (typeof jobKindAdd === 'function') jobKindAdd('incident', { tier: 1, work: 0, text: 'Incident',
  stops: incStops, stepDone: incStepDone, done: incDone, veto: true,
  crew: { can: incWorks, mins: j => j.walk ? 5 : 25 + Math.floor(schedU(machSeed(j.id), worksDay(j.posted), 873) * 16) } });
// the ladder row (m6): the training is an urgent call, not an appointment by Mail: offer (24 core's hook) makes the
// meeting at the incident's minute with no Mail; then reserve gives the teacher's walk to the pipe (watch 1 minute
// there), then the incident's job, yours
function incOffer(row, c, d, t) {
  const m = t - (d - 1) * 1440, by = ladderTeacher(row, d); if (!by) return false;
  const at = m <= INC_FIRST.at - 10 ? INC_FIRST.at : Math.min(INC_WIN[1], m + 10), o = trainSetup(row);
  o.by = by; o.script = trainScript(row, by);
  const r = occasionAdd('works.' + row.id, (d - 1) * 1440 + at, true, 15); if (!r) return false;
  c.by = by; c.d = d; c.w = 0; c.st = 'meet'; c.occ = r.key;
  return true;
}
if (JOB_KINDS.incident) WORK_MECH.m6 = {
  offer: incOffer,
  reserve(d, at, slot, o = {}) {
    const t = (d - 1) * 1440 + at, I = incState(); if (!I) return null;
    if (!I.open) incStart(INC_FIRST.kind, INC_FIRST.deck, t, true);
    const O = I.open; if (!O || !O.train) return null;
    SHIP.jobs = SHIP.jobs.filter(x => !(x.reserved === slot && heldForYou(x) && !x.claimedBy));
    const c = SHIP.works.cur, j = incJob(O.kind, O.deck, t, { slot, train: o.train || 'm6', walk: !o.yours, by: c && c.by });
    if (o.yours) O.j = j.id;
    SHIP.jobs.push(j); if (typeof MACH_REV !== 'undefined') MACH_REV++;
    return j.id;
  },
  watch: 1,                                              // a minute at the pipe with Calder, then it's yours
};
// the clock: the training's call at its minute; the week's incident at its minute; the stuck lift lets go after 20
// minutes; a training incident nobody's coming to goes to the crew. After a skip or a sleep, an incident in the hours
// skipped happened and the crew cleared it
if (WORK_MECH.m6) WORK_TICKS.push((now, skip) => {
  const I = incState(); if (!I) return;
  const d = worksDay(now), m = now - (d - 1) * 1440, c = SHIP.works.cur, O = I.open;
  if (I.fix) { const F = SHIP.jobs.find(x => x.id === I.fix.id); if (!F || F.status === 'done') { simNote('incident', { id: I.fix.kind, step: 'fixed', by: F ? F.doneBy : null }); I.fix = null; } }
  const R0 = c && c.id === 'm6' && c.st === 'meet' ? SHIP.occasions.find(x => x.key === c.occ) : null;   // the call at the meeting's minute
  if (R0 && now >= R0.at && now < R0.at + 60 && !O && !skip) {
    incStart(INC_FIRST.kind, INC_FIRST.deck, now, true);
    const line = worksTeach('m6', c.by, 'call', ['Burst pipe, junior wing. With me.']);
    if (typeof setGoal === 'function') { const o = OCCASIONS['works.m6']; if (o) setGoal({ deck: o.deck, room: o.room, label: worksText('inc.goal', 'Meet {name}', { name: worksFirst(c.by) }) }); }
    if (!line) try { toast(worksName(c.by), 'Burst pipe, junior wing. With me.'); } catch (e) { /* no UI */ }
  }
  if (O) {
    if (O.kind === 'lift' && !O.safe && now >= O.at + INC_LIFT && typeof liftStuck === 'function') { O.safe = true; liftStuck(false); }
    const busy = O.train && c && c.id === 'm6' && /^(meet|watch|do)$/.test(c.st);
    if (!O.j && !busy && now >= O.at + 5) incPost(now);
    const j = O.j && SHIP.jobs.find(x => x.id === O.j); if (O.j && (!j || j.status === 'done') && I.open === O) { I.open = null; incFx(); }
    return;
  }
  const w = incWeek(d), P = w >= 2 ? incPlan(w) : null;
  if (!P || !P.length || P[4] || P[1] !== d || m < P[2]) return;
  P[4] = 1;
  const S = incStart(P[0], P[3], now, false);
  if (S && skip) { const j = SHIP.jobs.find(x => x.id === S.j); if (j) jobFinish(j, now, 'crew'); }
});
// a reload with the lift stuck: section 17 doesn't save it, so it's set again here
WORK_TICKS.push(() => { const I = SHIP.works && SHIP.works.inc, O = I && I.open; if (O && O.kind === 'lift' && !O.safe && !INC_FX.lift && typeof liftStuck === 'function') { liftStuck(true, O.at + INC_LIFT); INC_FX.lift = true; } });
// ---- the look: a puddle on the wet corridor (two flat discs 1.2 cm off the floor, never coplanar) and a smoke wisp by
// the galley's vent (six soft quads), each one instanced draw call, made the first time they're needed on a deck (in
// deckRoot, so the deck's unload frees them), shown only during an incident on your deck ----
const INC_FX = { root: null, wet: null, smoke: null, lift: false };
function incFx() {
  try {
    if (typeof deckRoot === 'undefined' || !deckRoot || !deckDef) return;
    const O = SHIP.works && SHIP.works.inc && SHIP.works.inc.open, here = O && O.deck === deckDef.num;
    if (INC_FX.root !== deckRoot) { INC_FX.root = deckRoot; INC_FX.wet = INC_FX.smoke = null; }
    const wetOn = !!here && O.kind === 'burst', smokeOn = !!here && O.kind === 'alarm';
    if (wetOn && !INC_FX.wet) {
      const ids = (DECKS[O.deck].wet || []).filter(id => placeById(id));
      if (ids.length) {
        const g = new THREE.CircleGeometry(.62, 18); g.rotateX(-Math.PI / 2);
        const im = new THREE.InstancedMesh(g, new THREE.MeshBasicMaterial({ color: col('#4f86a8'), transparent: true, opacity: .55, depthWrite: false }), ids.length), M4 = new THREE.Matrix4();
        ids.forEach((id, k) => { const p = placeById(id); M4.makeScale(k ? .8 : 1.15, 1, k ? .9 : 1); M4.setPosition(X0(p.xy[0]), .012, Z0(p.xy[1])); im.setMatrixAt(k, M4); });
        im.userData.noMerge = true; deckRoot.add(im); INC_FX.wet = im;
      }
    }
    if (smokeOn && !INC_FX.smoke) {
      const p = placeById('3-vent-1');
      if (p) {
        const g = new THREE.PlaneGeometry(.7, .7), im = new THREE.InstancedMesh(g, new THREE.MeshBasicMaterial({ color: col('#b8b4ae'), transparent: true, opacity: .28, depthWrite: false, side: THREE.DoubleSide }), 6), M4 = new THREE.Matrix4(), Q = new THREE.Quaternion(), E = new THREE.Euler();
        for (let k = 0; k < 6; k++) { E.set(0, k * Math.PI / 3, 0); Q.setFromEuler(E); const s = .8 + .12 * (k % 3); M4.compose(new THREE.Vector3(X0(p.xy[0]) - .3 - .08 * k, 1.5 + .22 * k, Z0(p.xy[1]) + .05 * (k % 2)), Q, new THREE.Vector3(s, s, s)); im.setMatrixAt(k, M4); }
        im.userData.noMerge = true; deckRoot.add(im); INC_FX.smoke = im;
      }
    }
    if (INC_FX.wet) INC_FX.wet.visible = wetOn;
    if (INC_FX.smoke) INC_FX.smoke.visible = smokeOn;
  } catch (e) { console.error(e); }
}
WORK_TICKS.push((now, skip) => { if (!skip) incFx(); });

// ---------------------------------------------------------------------
// 24h TEAM JOBS (M8, seat M2, 0.51.x; plans/mechanics/m8-team-jobs.html). A big job three or four Works crew do at once at
// a set time: each step names who does it; a crew member's step takes its minutes on paper, yours waits for you (a toast
// and the goal pointer) and you do it at your spot (section 15's hold or turn). As an Officer you're one pair of hands.
// It waits for you 15 minutes at the start; then your steps go to the lead and it runs 20% slower. Never a fail.
// The rota (the user, 2026-10-18): Tuesdays and Thursdays 09:30, and Fridays 14:00 in even ship weeks (Day 12 skipped:
// the tracing lesson); from Day 11 (the recycler, the training). A day with an incident, a ship-wide event or your test
// job moves to the next free workday that week, or drops; never one machine twice a week. Posted at 16:00 the day before,
// with Mail if you're in it. Finishing puts the machines right (an overhaul). Ladder row m8 (24 core's table): the
// training is the Day 11 recycler with Halloran (or the first Works officer on shift). Section 17 (S2, 0.33.58) owns the
// 'team' kind: teamJobPost (the job, the crew at their spots, your stops), teamYouOut (you didn't come), the finish (the
// machine put right, your meters' step). 24h adds the plan, the step sequence and its clock: j.seq ([{ who, part, how,
// mins }], crew and yours), j.cur (the step under way), j.stepAt, j.late; j.youIn when you're at your spot. Saved:
// SHIP.works.team = { plan: { week: [[day, minute, job id, kind], ...] } } (ship.works.team, old weeks dropped); the job in
// ship.jobs. Hash keys 876 (the machine on ties), 877 (the team). No R().
const TEAM_JOBS = {                                      // steps: [who (0 the lead, 1.. the crew, 'you'), part, how, minutes]
  recycler: { machines: ['3-recycler-1'], n: 4, deck: 3, steps: [[1, 'drain', 'turn', 6], ['you', 'brace', 'hold', 2], [0, 'hold', 'hold', 8], ['you', 'pass', 'hold', 2], [2, 'hold', 'hold', 10], ['you', 'brace', 'hold', 2], [0, 'open', 'turn', 5]] },
  washer: { machines: ['4-washer-1', '4-washer-2', '4-washer-3', '4-washer-4'], n: 3, deck: 4, steps: [[0, 'drain', 'turn', 6], ['you', 'tip', 'hold', 2], [1, 'hold', 'hold', 8], ['you', 'pass', 'hold', 2], [0, 'hold', 'hold', 10], ['you', 'crank', 'turn', 3], [1, 'open', 'turn', 4]] },
  manifold: { machines: ['5-manifold-1'], n: 3, deck: 5, steps: [['you', 'valves', 'turn', 3], [0, 'hold', 'hold', 8], ['you', 'hold', 'hold', 2], [1, 'pass', 'hold', 8], [0, 'hold', 'hold', 8], ['you', 'open', 'turn', 3]] },
  heater: { machines: ['4-heater-1'], n: 3, deck: 4, steps: [['you', 'drain', 'turn', 3], [0, 'hold', 'hold', 6], ['you', 'hold', 'hold', 2], [1, 'pass', 'hold', 8], ['you', 'pass', 'hold', 2], [0, 'open', 'turn', 6]] },
  scrubber: { machines: ['4-scrubber-1', '4-scrubber-2'], n: 3, deck: 4, steps: [[0, 'drain', 'turn', 4], ['you', 'hold', 'hold', 2], [1, 'pass', 'hold', 8], ['you', 'pass', 'hold', 2], [0, 'hold', 'hold', 10], ['you', 'hold', 'hold', 2], [1, 'open', 'turn', 4]] } };
const TEAM_NAME = { recycler: 'Recycler membrane change', washer: 'Washer overhaul', manifold: 'Manifold valve bank', heater: 'Heating plant pump swap', scrubber: 'Scrubber fan change' };
const TEAM_PART = { brace: 'brace the housing', pass: 'pass the part', hold: 'hold it steady', crank: 'crank the drum', tip: 'tip and hold', valves: 'close the valves in order', open: 'open up again', drain: 'drain it down' };
const TEAM_ROTA = [[1, 570], [3, 570]], TEAM_FRI = [4, 840];   // Tue and Thu 09:30; Fri 14:00 in even ship weeks
const TEAM_FIRST = { day: 11, kind: 'recycler', at: 570 }, TEAM_SKIP = [12];
const TEAM_POST = 960;                                   // posted 16:00 the day before (section 17's TEAM_WAIT, 15 minutes, and TEAM_SLOW, 1.2)
const teamWeek = d => Math.floor((d - 1) / 7);           // (ship week number = this + 1; "even weeks" are odd here)
const teamText = (key, fb, v) => worksText(key, fb, v);
function teamState() { const W = SHIP.works; if (!W) return null; if (!W.team || typeof W.team !== 'object') W.team = { plan: {} }; return W.team; }
function teamClean(s, d = worksDay(shipNow())) {
  const out = { plan: {} }; if (!s || typeof s !== 'object' || !s.plan || typeof s.plan !== 'object') return out;
  for (const w in s.plan) if (/^\d{1,4}$/.test(w) && +w >= teamWeek(d) && Array.isArray(s.plan[w])) out.plan[w] = s.plan[w].filter(e => Array.isArray(e) && Number.isInteger(e[0]) && Number.isInteger(e[1]) && TEAM_JOBS[e[3]]).slice(0, 4).map(e => [e[0], e[1], typeof e[2] === 'string' ? e[2].slice(0, 80) : null, e[3]]);
  return out;
}
(() => { const s = SAVED && SAVED.ship && SAVED.ship.works; if (SHIP.works && s && s.team) SHIP.works.team = teamClean(s.team); })();
// the washer's and the scrubbers' other machines put right too (section 17's finish does j.machine)
function teamOthersRight(j, t) {
  machinesNow();
  for (const id of (j.machines || []).slice(1)) { const s = SHIP.machines[id]; if (s) { s.cond = Math.max(s.cond, TEAM_RESTORE); s.state = machineState(s.cond); s.lastService = t; } }
  if (typeof MACH_REV !== 'undefined') MACH_REV++;
}
// ---- the plan ----
const teamYouIn = (W = SHIP.works) => !!W && (W.rank !== 'junior' || W.tr.m8 !== undefined || !!(W.cur && W.cur.id === 'm8'));
const teamBusy = (d, W) => (typeof incPlan === 'function' && (() => { const P = incPlan(teamWeek(d)); return P && P.length && P[1] === d; })()) || (typeof incShipEvent === 'function' && incShipEvent(d)) || !!(W.test && W.test.day === d);
function teamNeed(kind) { const ms = TEAM_JOBS[kind].machines.filter(id => SHIP.machines[id]); return ms.length ? ms.reduce((a, id) => a + SHIP.machines[id].cond, 0) / ms.length : 101; }
// teamPlan(w): [[day, minute, job id | null, kind], ...]: the rota's days that week (from Day 11), a clash moved to the
// next free workday or dropped, each the TEAM_JOBS machine most in need not yet used that week (key 876 on ties)
function teamPlan(w) {
  const T = teamState(), W = SHIP.works; if (!T) return [];
  if (T.plan[w]) return T.plan[w];
  const slots = TEAM_ROTA.slice(); if ((w + 1) % 2 === 0) slots.push(TEAM_FRI);
  const out = [], used = new Set(), taken = new Set();
  for (const [wd, at] of slots) {
    let d = w * 7 + 1 + wd; if (d < TEAM_FIRST.day || TEAM_SKIP.includes(d)) continue;
    while (d <= w * 7 + 5 && (taken.has(d) || TEAM_SKIP.includes(d) || teamBusy(d, W))) d++;
    if (d > w * 7 + 5) continue;
    let kind = d === TEAM_FIRST.day ? TEAM_FIRST.kind : null;
    if (!kind) { const ks = Object.keys(TEAM_JOBS).filter(k => !used.has(k) && TEAM_JOBS[k].machines.some(id => SHIP.machines[id])); if (!ks.length) continue;
      kind = ks.sort((a, b) => teamNeed(a) - teamNeed(b) || schedU(machSeed(a), w, 876) - schedU(machSeed(b), w, 876))[0]; }
    used.add(kind); taken.add(d); out.push([d, d === TEAM_FIRST.day ? TEAM_FIRST.at : at, null, kind]);
  }
  return T.plan[w] = out;
}
// the team: Works crew on shift that day, not busy at another team job, in the key-877 order; n (one fewer when you're in)
function teamCrew(d, n, w) {
  const busy = new Set(SHIP.jobs.filter(j => j.kind === 'team' && j.status !== 'done' && Math.floor(j.start / 1440) + 1 === d).flatMap(j => j.team || []));
  const ps = schedPeople().filter(p => jobCrew(p) === 'works' && !busy.has(p.id) && (() => { try { return occOnShift(p.id, d); } catch (e) { return false; } })());
  const os = ps.filter(p => OFFICER_RANKS.has(p.rank)), lead = (typeof ladderRow === 'function' && ladderRow('m8') ? ladderRow('m8').by : ['torres-zeke', 'halloran-emeka', 'calder']).find(id => ps.some(p => p.id === id)) || (os[0] && os[0].id) || (ps[0] && ps[0].id);
  const rest = ps.filter(p => p.id !== lead).sort((a, b) => schedU(machSeed(a.id), d, 877) - schedU(machSeed(b.id), d, 877) || (a.id < b.id ? -1 : 1)).map(p => p.id);
  return lead ? [lead].concat(rest).slice(0, n) : [];
}
// a team job posted (section 17's teamJobPost): the crew (the lead first), you if you're in, your stops at your spot;
// then 24h's sequence on it (j.seq), each step's who from the crew section 17 kept (one left out: the lead does theirs)
function teamJob(kind, d, at, o = {}) {
  const T = TEAM_JOBS[kind], ms = T.machines.filter(id => machineById(id)); if (!ms.length || typeof teamJobPost !== 'function') return null;
  const you = o.you !== undefined ? o.you : teamYouIn() && playerShiftOn(d), crew = teamCrew(d, T.n - (you ? 1 : 0)); if (crew.length < 2) return null;
  const t = (d - 1) * 1440 + at, mins = T.steps.reduce((a, s) => a + s[3], 0), m0 = machineById(ms[0]), sp = teamSpots(ms[0]), spotYou = sp[crew.length] || sp[sp.length - 1] || panelPlace(ms[0]);
  const mine = T.steps.filter(s => s[0] === 'you').map(([, part, how, mm]) => ({ deck: m0.deck, placeId: spotYou, mins: how === 'hold' ? mm : 1, tag: 'team', how,
    opts: how === 'turn' ? { label: TEAM_PART[part], v: 0, min: 0, max: 3, by: 1, onTurn: v => v >= 3 ? null : teamText('team.turning', 'Keep going.'), ok: v => v >= 3, gauge: null } : null }));
  const id = teamJobPost({ id: 'team:' + kind + '@' + d, machine: ms[0], start: t, mins, team: crew, lead: crew[0], you, ...(you ? { steps: mine, spots: { you: spotYou } } : {}), found: Math.min(shipNow(), t),
    title: teamText('team.card', '{job}, {time}, Deck {deck}, a team of {n}', { job: teamText('team.name.' + kind, TEAM_NAME[kind]), time: hhmm(at), deck: m0.deck, n: crew.length + (you ? 1 : 0) }) });
  const j = id && SHIP.jobs.find(x => x.id === id); if (!j) return null;
  j.seq = T.steps.map(([who, part, how, mm]) => ({ who: who === 'you' ? (j.claimedBy === 'you' ? 'you' : j.lead) : j.team[who] || j.lead, part, how, mins: mm }));
  Object.assign(j, { team_kind: kind, machines: ms, cur: -1, stepAt: null, late: false, ...(o.train ? { train: o.train } : {}), ...(o.slot ? { reserved: o.slot, until: (d - 1) * 1440 + DAY_SHIFT[1] } : {}) });
  return j;
}
function teamPost(P, w, t) {                             // a plan entry posted (16:00 the day before): the job, the crew's plans, Mail
  const [d, at, , kind] = P; if (P[2] && SHIP.jobs.some(j => j.id === P[2])) return null;
  const j = teamJob(kind, d, at); if (!j) { P[2] = 'none'; return null; }
  P[2] = j.id; if (typeof MACH_REV !== 'undefined') MACH_REV++;
  const pr = teamParts(j, t);                            // stage 2: bring the parts (the Mail says so instead)
  if (pr && typeof mailSend === 'function') { const m = teamText('mail.team.parts', 'Bring the parts | {job} tomorrow at {time}. {name} asks you to bring the parts from stores: {parts}.', { job: teamLabel(j), time: hhmm(at), name: worksFirst(j.lead), parts: TEAM_PARTS[kind].join(', ') }), i = m.indexOf(' | ');
    mailSend({ at: t, from: worksName(j.lead), subject: i > 0 ? m.slice(0, i) : teamLabel(j), body: i > 0 ? m.slice(i + 3) : m }); }
  else if (j.claimedBy === 'you' && typeof mailSend === 'function') mailSend({ at: t, from: worksName(j.lead), subject: teamText('team.name.' + kind, TEAM_NAME[kind]),
    body: teamText('mail.team', '{job}, {time} tomorrow, Deck {deck}. You\'re one of the team. — {name}', { job: teamText('team.name.' + kind, TEAM_NAME[kind]), time: hhmm(at), deck: j.deck, name: worksFirst(j.lead) }) });
  return j;
}
// ---- the run: the sequence in order; a crew step its minutes on paper, yours waits for you ----
const teamYours = j => j.claimedBy === 'you' && !j.youOut;
const teamStepMins = (j, s) => Math.ceil(s.mins * (j.late ? TEAM_SLOW : 1));
const teamLabel = j => teamText('team.name.' + j.team_kind, TEAM_NAME[j.team_kind]);
function teamNext(j, t) {                                // the next step (or the end)
  j.cur++; j.stepAt = t;
  if (j.cur >= j.seq.length) return teamEnd(j, t);
  const s = j.seq[j.cur];
  simNote('team', { id: j.id, step: j.cur, by: s.who, kind: s.who === 'you' ? 'turn' : 'step' });
  if (s.who === 'you') {
    try { toast(teamLabel(j), teamText('team.turn.' + s.part, 'Your turn: ' + TEAM_PART[s.part] + '.', { job: teamLabel(j) })); } catch (e) { /* no UI */ }
    const pl = placeById(j.spots && j.spots.you); if (pl && typeof setGoal === 'function') setGoal({ deck: pl.deck, room: pl.room, label: TEAM_PART[s.part] });
  } else if (teamYours(j)) worksTeach('m8', j.lead, 'call.' + s.part, null);
  return true;
}
// the sequence done: the other machines right, then section 17's finish (yours if you were in it: your stops are done)
function teamEnd(j, t) {
  j.cur = j.seq.length; teamOthersRight(j, t);
  const you = teamYours(j);
  simNote('team', { id: j.id, step: j.seq.length, by: you ? 'you' : j.lead, kind: 'done' });
  if (you) worksTeach('m8', j.lead, 'done', [teamText('team.done', 'That\'s it. Good work, all.')]);
  if (j.status !== 'done') jobFinish(j, t, you ? 'you' : j.lead);
  if (you) { worksXp(2); worksUse('m8'); const c = SHIP.works.cur; if (c && c.id === 'm8' && c.j === j.id) worksTrained('m8', t); }   // (trained here: the finished job can be tidied off the list before the training's minute)
  if (typeof MACH_REV !== 'undefined') MACH_REV++;
  return true;
}
// you didn't come (15 minutes, or section 17's own at the hour): your steps are the lead's, the rest 20% slower
function teamLate(j, t) {
  if (!j.youOut && typeof teamYouOut === 'function') teamYouOut(j.id);
  j.late = true; for (const s of j.seq) if (s.who === 'you') s.who = j.lead;
  simNote('team', { id: j.id, step: j.cur, by: j.lead, kind: 'late' });
  try { toast(teamLabel(j), teamText('team.late', '{name} started without you.', { name: worksFirst(j.lead) })); } catch (e) { /* no UI */ }
}
function teamAtSpot(j) {
  try { const pl = placeById(j.spots && j.spots.you); if (!pl || !deckDef || deckDef.num !== pl.deck || !player) return false; const [c, r] = player.here(); return Math.hypot(c - pl.at[0], r - pl.at[1]) <= 3; } catch (e) { return false; }
}
function teamTick(j, now, skip) {
  if (j.status === 'done' || !j.seq || now < j.start - 10) return;
  if (teamYours(j) && !j.youIn && !skip && teamAtSpot(j)) j.youIn = true;
  if (j.youOut && !j.late) teamLate(j, now);
  if (now < j.start) return;
  if (j.partsRun && j.partsLate === undefined) teamPartsCheck(j, j.start, skip);
  if (j.cur < 0 && now < teamT0(j)) return;
  if (j.cur < 0) { simNote('team', { id: j.id, step: 0, by: j.lead, kind: 'start' }); if (teamYours(j) && !skip) worksTeach('m8', j.lead, 'call.start', null); teamNext(j, teamT0(j)); }
  for (let guard = 0; guard < 20 && j.status !== 'done' && j.cur < j.seq.length; guard++) {
    const s = j.seq[j.cur];
    if (s.who === 'you') {
      const k = j.seq.slice(0, j.cur).filter(x => x.who === 'you').length;   // your stop for this step: done already (no stepDone hook)? on with the job
      if ((j.stepsDone || []).includes(k)) { j.youIn = true; teamNext(j, now); continue; }
      if (skip || now >= teamT0(j) + TEAM_WAIT && !j.youIn) { teamLate(j, now); continue; } break; }
    const t = j.stepAt + teamStepMins(j, s); if (now < t) break;
    teamNext(j, t);
  }
}
// your stop k (section 17's stepDone hook): only when it's your step under way; out of turn it's refused (its veto)
function teamStepDone(j, k, res, t) {
  if (!j.seq) return true;
  const mine = j.seq.map((s, i) => s.who === 'you' ? i : -1).filter(i => i >= 0), i = mine[k];
  if (i === undefined || i !== j.cur) { try { toast(j.title, teamText('team.wait', 'Not yet: wait for {name}\'s call.', { name: worksFirst(j.lead) })); } catch (e) { /* no UI */ } return false; }
  j.youIn = true; simNote('team', { id: j.id, step: i, by: 'you', kind: 'step' });
  teamNext(j, t !== undefined ? t : shipNow());
  return true;
}
// ---- team parts (M8 stage 2, Step 4; plans/mechanics/step4-stages.html; seat E5 for M2): from Day 18, once you've done
// two team jobs (m8's stage 1), the Mail of a team job you're in asks you to bring the parts: a manifest run (24d's
// manifestRun, E1) from stores to the machine, held for you till the start. Not there at the start: the run withdrawn,
// the lead fetches them and it starts TEAM_PARTS_LATE minutes late (team.parts.late). Never a fail. j.partsRun the run's
// id, j.partsLate (false: brought) on the job; SHIP.works.side.parts = how many times you've brought them. No R().
const TEAM_PARTS = { recycler: ['membrane', 'seal'], washer: ['pump', 'bearing'], manifold: ['valve', 'seal'], heater: ['pump', 'seal'], scrubber: ['filter', 'fan belt'] };
const TEAM_PARTS_DAY = 18, TEAM_PARTS_LATE = 10;
const teamT0 = j => j.start + (j.partsLate ? TEAM_PARTS_LATE : 0);   // when the first step starts
const teamPartsN = () => { const S = typeof worksSide === 'function' && worksSide(), n = S && S.parts; return Number.isInteger(n) && n > 0 ? Math.min(n, 9999) : 0; };
function teamParts(j, t) {                               // the parts ask on a team job you're in -> the run's id | null
  if (typeof manifestRun !== 'function' || !j || j.claimedBy !== 'you' || j.partsRun || !TEAM_PARTS[j.team_kind]) return null;
  if (worksDay(j.start) < TEAM_PARTS_DAY || typeof worksStage !== 'function' || worksStage('m8') < 1) return null;
  const id = manifestRun(TEAM_PARTS[j.team_kind], j.machine, { at: t, until: j.start, for: j.lead }); if (id) j.partsRun = id;
  return id || null;
}
function teamPartsCheck(j, t, skip) {                    // at the start: brought (one more), or the lead fetches them
  j.partsLate = !(typeof manifestRunDelivered === 'function' && manifestRunDelivered(j.partsRun));
  if (!j.partsLate) { const S = typeof worksSide === 'function' && worksSide(); if (S) S.parts = teamPartsN() + 1; return; }
  if (typeof manifestRunEnd === 'function') manifestRunEnd(j.partsRun, t);
  if (!skip) try { toast(teamLabel(j), teamText('team.parts.late', '{name} fetched the parts. Ten minutes late. Nobody minds. Much.', { name: worksFirst(j.lead) })); } catch (e) { /* no UI */ }
}
// the clock: the week's plan posted at 16:00 the day before; each team job's steps run
if (typeof teamJobPost === 'function') WORK_TICKS.push((now, skip) => {
  const d = worksDay(now), w = teamWeek(d);
  if (d < TEAM_FIRST.day - 1 || !teamState()) return;   // (nothing saved before Day 10: the first is posted on Day 10 at 16:00)
  for (const ww of [w, w + 1]) for (const P of teamPlan(ww)) if (!P[2] && (P[0] - 2) * 1440 + TEAM_POST <= now && now < (P[0] - 1) * 1440 + P[1]) teamPost(P, ww, Math.max(now, (P[0] - 2) * 1440 + TEAM_POST));
  for (const j of SHIP.jobs) if (j.kind === 'team' && j.status !== 'done') teamTick(j, now, skip);
});
// the ladder row (m8, 24 core's table): the teacher's Mail at 08:05 (works.ask.m8) and the meeting at the recycler at 09:30;
// the training's job is the Day 11 team job itself (you in it), held in the slot; trained when it's done with you in it
function teamOffer(row, c, d, t) {
  const by = ladderTeacher(row, d); if (!by) return false;
  const o = trainSetup(row); o.by = by; o.script = trainScript(row, by); o.deck = 3; o.room = 'R';
  const r = occasionAdd('works.' + row.id, (d - 1) * 1440 + TEAM_FIRST.at - 10, true, 15); if (!r) return false;
  c.by = by; c.d = d; c.w = 0; c.st = 'meet'; c.occ = r.key;
  if (typeof mailSend === 'function') mailSend({ at: Math.max(t, (d - 1) * 1440 + 485), from: worksName(by), subject: mechName('m8'),
    body: worksText('works.ask.m8', 'Recycler\'s membrane bank, 09:30, Deck 3. Need four. You\'re the fourth. — {name}', { name: worksFirst(by) }) });
  return true;
}
if (typeof teamJobPost === 'function') WORK_MECH.m8 = {
  offer: teamOffer,
  reserve(d, at, slot, o = {}) {
    const P = teamPlan(teamWeek(d)).find(e => e[0] === d) || null;
    let j = P && P[2] && SHIP.jobs.find(x => x.id === P[2] && x.status !== 'done');
    if (j && j.claimedBy !== 'you') { SHIP.jobs = SHIP.jobs.filter(x => x !== j); j = null; }
    if (!j) { j = teamJob(P ? P[3] : TEAM_FIRST.kind, d, P ? P[1] : Math.max(at + 20, TEAM_FIRST.at), { you: true, slot, train: 'm8' }); if (!j) return null; if (P) P[2] = j.id; }
    j.reserved = slot; j.until = (d - 1) * 1440 + DAY_SHIFT[1]; j.train = 'm8';
    if (typeof MACH_REV !== 'undefined') MACH_REV++;
    return j.id;
  },
  watch: 0,
  oneJob: true,                                          // the teacher leads the same job you're in (no teacher's job first)
};

// ---------------------------------------------------------------------
// 24l FAVOUR CASES (Pillar 5 Step 4, seat E2 on H's behalf; plans/mechanics/favour-cases.html: scripted cases on the
// favours system, D3 de012aa, not the case engine). From Day 13, an Officer's, off shift: about once a week a crew
// friend (FC_TIER: friend or closer) brings you a little mystery of their own, at an evening minute (18:00-21:00): their Mail
// (mail.favour.<id>) and their open favour in the chat card (section 17's favourPost: offered, never on the board; the
// chat's "help" accepts it). Accepted: a side job (the 'fcase' kind, beside your board job) in and around their cabin:
// three clues (a look each: favour.<id>.clue.1-3, at their bed, or the junction, the laundry or the scrubber the clue
// is about), then "What's causing it?" (a choose from sus.1-3, shuffled; a wrong pick: "Not that.", pick again, never
// a fail). Solved (favour.<id>.solved): the favour's own stop (the fix, a hold at their bed) gets its place, then hand
// it back in the chat card as any favour (friendship, reputation). Not taken in 3 days, they ask someone else
// (favour.lapse, no harm). The six scripts are FAVOUR_CASES (W2's lines); sus.1 is always the answer. Saved:
// SHIP.works.side.favours = [{ id, who, case, day, state }] (the last 12; state: asked, taken, solved, done, lapsed),
// cleaned on read; the side job in ship.jobs. Hash keys 1019 (who asks), 1020 (which case), 1021 (which evening). No R().
const FAVOUR_CASES = {                                    // where each clue is looked at (bed: their cabin)
  lamp: ['bed', 'bed', 'junction'], cold: ['bed', 'bed', 'bed'], squeak: ['bed', 'bed', 'bed'],
  shower: ['bed', 'bed', 'laundry'], clock: ['bed', 'bed', 'bed'], speaker: ['bed', 'scrubber', 'bed'] };
const FC_TIER = 3;                                       // who asks: friend or closer (relTier; lead 17: the user may lower it to 2, colleague)
const FC_IDS = Object.keys(FAVOUR_CASES), FC_FROM = 13, FC_EVE = [1080, 1260], FC_KEEP = 12, FC_DAYS = 3, FC_FIX = 10;
function fcList() {                                      // side.favours, cleaned (a save may hold junk)
  const s = typeof worksSide === 'function' ? worksSide() : null; if (!s) return null;
  if (!Array.isArray(s.favours) || !s.fcOk) {
    s.favours = (Array.isArray(s.favours) ? s.favours : []).filter(e => e && typeof e.id === 'string' && typeof e.who === 'string' && FC_IDS.includes(e.case) && Number.isInteger(e.day))
      .slice(-FC_KEEP).map(e => ({ id: e.id.slice(0, 80), who: e.who.slice(0, 40), case: e.case, day: e.day, state: ['asked', 'taken', 'solved', 'done', 'lapsed'].includes(e.state) ? e.state : 'asked' }));
    Object.defineProperty(s, 'fcOk', { value: true, enumerable: false, configurable: true });
  }
  return s.favours;
}
const fcSeed = () => machSeed('favourcase');
const fcText = (c, k, fb) => worksText('favour.' + c + '.' + k, fb);
// the week's ask: an evening of week w (any day from Day 13), a friend with a cabin, a case not done yet (else any)
function fcPlan(w) {
  const seed = fcSeed(), d = Math.max(FC_FROM, w * 7 + 1 + Math.floor(schedU(seed, w, 1021) * 7) % 7);
  if (incWeek(d) !== w) return null;
  const at = FC_EVE[0] + Math.floor(schedU(seed, w * 7 + 1, 1021) * ((FC_EVE[1] - FC_EVE[0]) / 10)) * 10;
  return { d, at };
}
function fcWho(w) {
  let ps = []; try { ps = schedPeople().filter(p => p.bed && placeById(p.bed) && relTier(p.id) >= FC_TIER && !(typeof favoursOf === 'function' && favoursOf(p.id).length)).sort((a, b) => (a.id < b.id ? -1 : 1)); } catch (e) { return null; }
  return ps.length ? ps[Math.floor(schedU(fcSeed(), w, 1019) * ps.length) % ps.length] : null;
}
function fcCase(w) {
  const L = fcList() || [], left = FC_IDS.filter(c => !L.some(e => e.case === c && e.state === 'done')), from = left.length ? left : FC_IDS;
  return from[Math.floor(schedU(fcSeed(), w, 1020) * from.length) % from.length];
}
// a clue's place: their bed, or the deck's junction panel, the laundry's washer, the scrubber (else their bed)
function fcPlace(where, bed) {
  const B = placeById(bed), pp = id => machineById(id) ? panelPlace(id) : null;
  const P = where === 'junction' ? (B && machineList().filter(m => /junction/.test(m.id) && m.deck === B.deck).map(m => panelPlace(m.id)).find(Boolean))
    : where === 'laundry' ? pp('4-washer-1') : where === 'scrubber' ? pp('4-scrubber-1') : null;
  return P && placeById(P) ? P : bed;
}
function fcAsk(w, t) {
  const L = fcList(), p = fcWho(w); if (!L || !p || typeof favourPost !== 'function') return null;
  const c = fcCase(w), B = placeById(p.bed);
  const fid = favourPost({ from: p.id, title: fcText(c, 'title', 'A favour'), stops: [{ deck: B.deck, placeId: null, mins: FC_FIX, tag: 'fcase' }], expires: t + FC_DAYS * 1440 });
  const F = fid && favourById(fid); if (!F) return null;
  F.fcase = c;
  L.push({ id: fid, who: p.id, case: c, day: worksDay(t), state: 'asked' }); if (L.length > FC_KEEP) L.splice(0, L.length - FC_KEEP);
  const mail = worksText('mail.favour.' + c, 'A favour | ' + fcText(c, 'ask', 'Could you take a look at something for me?')), cut = mail.indexOf(' | ');
  if (typeof mailSend === 'function') mailSend({ at: t, from: worksName(p.id), subject: cut > 0 ? mail.slice(0, cut) : 'A favour', body: cut > 0 ? mail.slice(cut + 3) : mail });
  simNote('favourCase', { id: fid, case: c, from: p.id, step: 'ask' });
  return fid;
}
// the side job (made when you accept): three clue looks, then the choose
function fcStops(j) {
  const S = FAVOUR_CASES[j.fcase], B = placeById(j.bed); if (!S || !B) return [];
  const opts = (j.order || [1, 2, 3]).map(n => ({ id: 'sus' + n, label: fcText(j.fcase, 'sus.' + n, 'sus ' + n) }));
  return [...S.map((where, k) => { const pl = fcPlace(where, j.bed), P = placeById(pl); return { deck: P.deck, placeId: pl, mins: 1, tag: 'clue', how: 'look', opts: { secs: 3, text: fcText(j.fcase, 'clue.' + (k + 1), '...') } }; }),
    { deck: B.deck, placeId: j.bed, mins: 1, tag: 'call', how: 'choose', opts: { title: worksText('favour.call', 'What\'s causing it?'), text: fcText(j.fcase, 'title', ''), options: opts } }];
}
function fcStepDone(j, k, res, t) {
  const st = fcStops(j)[k]; if (!st || st.tag !== 'call') return true;
  if (![0, 1, 2].every(i => (j.stepsDone || []).includes(i))) return false;   // the clues first
  if (!res || res.pick !== 'sus1') { j.wrong = (j.wrong || 0) + 1; try { toast(fcText(j.fcase, 'title', 'A favour'), worksText('favour.not', 'Not that. Look again.')); } catch (e) { /* no UI */ } return false; }
  return true;
}
function fcDone(j, t, by) {
  const F = typeof favourById === 'function' ? favourById(j.favour) : null, e = (fcList() || []).find(x => x.id === j.favour);
  if (F && F.stops[0]) { F.stops[0].placeId = j.bed; if (typeof MACH_REV !== 'undefined') MACH_REV++; }   // the fix can be done now
  if (e) e.state = 'solved';
  try { toast(fcText(j.fcase, 'title', 'A favour'), fcText(j.fcase, 'solved', 'That\'s it.')); } catch (err) { /* no UI */ }
  simNote('favourCase', { id: j.favour, case: j.fcase, from: j.from, step: 'solved', wrong: j.wrong || 0 });
}
if (typeof jobKindAdd === 'function') jobKindAdd('fcase', { tier: 1, work: 0, text: 'Favour', side: true, stops: fcStops, stepDone: fcStepDone, done: fcDone, veto: true, crew: { can: () => false, mins: 30 } });
if (typeof WORKS_SIDE_KINDS !== 'undefined' && WORKS_SIDE_KINDS.add) WORKS_SIDE_KINDS.add('fcase');   // (never turned in at the board: finished when solved; the favour's hand-back is the reward)
// the clock: the week's ask at its evening minute (an Officer, Day 13 on); an accepted favour gets its side job (yours at
// once, the suspects shuffled by its id); a fixed and handed-back favour is done; one that lapsed, they ask someone else
if (JOB_KINDS.fcase) WORK_TICKS.push((now, skip) => {
  const W = SHIP.works, L = W && fcList(); if (!L || W.rank === 'junior') return;
  const d = worksDay(now), m = now - (d - 1) * 1440, w = incWeek(d);
  for (const e of L) {
    if (e.state === 'done' || e.state === 'lapsed') continue;
    const F = typeof favourById === 'function' ? favourById(e.id) : null;
    if (!F || (F.status === 'done' && F.doneBy !== 'you')) {
      e.state = 'lapsed';
      for (const x of SHIP.jobs) if (x.kind === 'fcase' && x.favour === e.id && x.status !== 'done') { x.status = 'done'; x.doneAt = now; x.doneBy = null; }   // its side job goes too
      if (!skip) try { toast(worksName(e.who), worksText('favour.lapse', '{name} asked someone else. No harm done.', { name: worksFirst(e.who) })); } catch (err) { /* no UI */ }
      continue;
    }
    if (F.status === 'done') { e.state = 'done'; continue; }
    for (const x of SHIP.jobs) if (x.kind === 'fcase' && x.favour === e.id && x.workDone && x.status !== 'done') jobFinish(x, now, 'you');   // solved: done, no board turn-in (R5)
    if (e.state === 'asked' && F.status === 'claimed' && F.claimedBy === 'you' && !SHIP.jobs.some(x => x.kind === 'fcase' && x.favour === e.id)) {
      const P = typeof schedPeople === 'function' ? schedPeople().find(p => p.id === e.who) : null; if (!P) continue;
      const order = [1, 2, 3].map(n => [schedU(machSeed(e.id), n, 1020), n]).sort((a, b) => a[0] - b[0]).map(x => x[1]);
      const j = jobMake('fcase', { id: 'fcase:' + e.id, deck: placeById(P.bed).deck, h: Math.floor(now / 60), title: fcText(e.case, 'title', 'A favour'), fcase: e.case, favour: e.id, from: e.who, bed: P.bed, order });
      j.posted = j.found = now; j.claimedBy = 'you'; j.status = 'claimed'; j.start = now; SHIP.jobs.push(j); e.state = 'taken';
      F.expires = Math.max(F.expires || 0, now + 14 * 1440);   // accepted: it doesn't lapse mid-case
      if (typeof MACH_REV !== 'undefined') MACH_REV++;
    }
  }
  if (d < FC_FROM || L.some(e => incWeek(e.day) === w)) return;
  const P = fcPlan(w); if (!P || P.d !== d || m < P.at || m > FC_EVE[1]) return;
  fcAsk(w, now);
});

// ---- fault-finder tickets (24l, E2 on H's behalf; favour-cases.html "Fault-finder tickets"). Day 13: Calder's Mail
// (mail.ticket.first). From then, on a workday shift of yours, a ticket on the Works board at 08:00: a Tier 2 machine's
// real fault (key 1022 the machine, 1023 the fault) held for you in slot 23 till 17:00, with a T2 head-scratcher made
// by 24k's caseMake for a kind that's open (c.ticket: hints only after your third clue, 24k's caseHint). Solved right
// first time: you're a Fault-finder (grade 1): W.ms ['ff1', day] (24 core's Record line, E1), the pin on your uniform
// (section 8's s.pin, rebuilt by 24 core's playerRigRebuild), ticket.solved and works.pin. A wrong call fitted: "Not yet. Next
// week." (ticket.wrong): the ticket's over for this week, the job a plain repair; the next one a week on. Not taken: the
// crew fix it at 17:00 and it's back the next workday. Saved: SHIP.works.side.ff = { grade, tries, next, job, mail }
// (cleaned on read). Grades 2 and 3 (Days 19 and 24) are Steps 5 and 6 on this machinery.
const FF_FROM = 13, FF_SLOT = 23, FF_POST = 480, FF_MAIL = 490;   // (a ticket's hints after three clues: 24k's caseHint)
function ffState() {
  const s = typeof worksSide === 'function' ? worksSide() : null; if (!s) return null;
  const F = s.ff, n = (v, lo, hi, d) => Number.isInteger(v) ? Math.max(lo, Math.min(hi, v)) : d;
  if (!F || typeof F !== 'object' || !s.ffOk) {
    s.ff = { grade: n(F && F.grade, 0, 3, 0), tries: n(F && F.tries, 0, 999, 0), next: n(F && F.next, 0, 9999, FF_FROM), job: F && typeof F.job === 'string' ? F.job.slice(0, 80) : null, mail: F && F.mail ? 1 : 0 };
    Object.defineProperty(s, 'ffOk', { value: true, enumerable: false, configurable: true });
  }
  return s.ff;
}
const ffSeed = () => machSeed('ticket');
// the machine and its fault: a Tier 2 machine with no job of yours, the crew's or a case on it, a part fault that an open
// case kind fits
function ffPick(d) {
  const kinds = caseKindsOpen(), ok = (m, f) => f.part && kinds.some(id => { try { return !!CASE_KINDS[id].fits(f, m); } catch (e) { return false; } });
  const ms = machineList().filter(m => (m.tier || MACHINE_KINDS[m.kind].tier) === 2 && !ENGINE_KINDS.has(m.kind) && caseCauses(m).some(f => ok(m, f))
    && !SHIP.jobs.some(j => j.machine === m.id && j.status !== 'done' && (j.claimedBy || j.case || j.reserved))).sort((a, b) => (a.id < b.id ? -1 : 1));
  if (!ms.length) return null;
  const m = ms[Math.floor(schedU(ffSeed(), d, 1022) * ms.length) % ms.length], fs = caseCauses(m).filter(f => ok(m, f));
  return { m, f: fs[Math.floor(schedU(ffSeed(), d, 1023) * fs.length) % fs.length] };
}
function ffPost(t) {
  const F = ffState(), C = typeof caseState === 'function' ? caseState() : null, d = worksDay(t); if (!F || !C || typeof jobReserve !== 'function') return null;
  const P = ffPick(d); if (!P) return null;
  const { m, f } = P, id = jobReserve(m.id, d, t % 1440, FF_SLOT, { tier: 2, until: (d - 1) * 1440 + DAY_SHIFT[1], cause: f.id }), j = id && SHIP.jobs.find(x => x.id === id);
  if (!j) return null;
  delete j.make; delete j.makeMins; j.cause = f.id; j.parts = [f.part]; j.ticket = true;
  const kinds = caseKindsOpen().filter(k => { try { return !!CASE_KINDS[k].fits(f, m); } catch (e) { return false; } });
  let c = null;
  for (const kid of kinds) for (let k = 0; k < CASE_TRIES && !c; k++) { const r = caseMake(j, kid, k, d); if (!r.why) c = r.c; }
  if (!c) { jobRelease(FF_SLOT); return null; }         // no fair case on it today: a plain repair; a ticket tomorrow
  c.ticket = true; c.by = c.by || caseTalker(d); C.n++; C.open.push(c); j.case = c.id; F.job = j.id;
  if (!c.wait) caseShow(c, j);
  j.title = worksText('ticket.card', 'Ticket: {machine} ({shows})', { machine: caseMachName(j), shows: String(f.shows || '').split('|')[0] });
  if (typeof MACH_REV !== 'undefined') MACH_REV++;
  return j.id;
}
function ffGrade(n, t) {                                 // a grade: the Record's line, the pin, the words
  const W = SHIP.works, F = ffState(); if (!W || !F || F.grade >= n) return false;
  F.grade = n; if (!W.ms.some(x => x[0] === 'ff' + n)) W.ms.push(['ff' + n, worksDay(t)]);
  ffPin(); if (typeof flagSet === 'function') flagSet('ticket.solved', 1);   // Calder's line (calder.lines, flag ticket.solved)
  try { toast(worksName('calder'), worksText('ticket.solved', 'Calder signs it off. You\'re a Fault-finder.')); toast(worksText('works.grade.' + n, 'Fault-finder'), worksText('works.pin', 'A small pin for your uniform.')); } catch (e) { /* no UI */ }
  simNote('faultFinder', { grade: n });
  return true;
}
// the player's figure rebuilt from PLAYER_SPEC (24l owns it, lead 17; E1's 24 core never declares one): the old rig
// removed and freed, makeCharacter again, the props reset, the grubby tint put back (as 24p's promoPip does for the pip)
function playerRigRebuild() {
  if (typeof player === 'undefined' || !player || !player.rig) return false;
  const w = player, old = w.rig;
  w.obj.remove(old.root); old.root.traverse(o => { if (o.isMesh) o.geometry.dispose(); });
  w.rig = makeCharacter(w.spec); w.obj.add(w.rig.root); w.rig.root.traverse(o => { o.userData.walker = w; });
  w.propMeshes = []; w.propKey = ''; w.bodyProps = null;
  if (typeof ACT !== 'undefined' && ACT && ACT.body && typeof recBody === 'function') recBody(ACT);   // the stand-in at a place too (as playerKit does; E5)
  const grubby = typeof uniformState === 'function' && uniformState() === 'grubby' && !PLAYER_SPEC.kit;
  if (typeof playerUniformTint === 'function' && (grubby || (typeof UNIFORM_MAT !== 'undefined' && UNIFORM_MAT))) playerUniformTint(grubby ? 1 : 0);
  return true;
}
function ffPin() {                                       // your uniform's pin (section 8's s.pin), from your grade
  const F = ffState(), g = F ? F.grade : 0;
  try { if (typeof playerRigRebuild !== 'function' || typeof player === 'undefined' || !player || (PLAYER_SPEC.pin || 0) === g) return false;
    PLAYER_SPEC.pin = player.spec.pin = g; playerRigRebuild(); return true; } catch (e) { return false; }
}
// the clock: Calder's Mail on Day 13 (or the first day after, for an Officer); a ticket at 08:00 on a workday of yours
// once it's due; a wrong call ends this week's; solved, grade 1
if (typeof caseMake === 'function') WORK_TICKS.push((now, skip) => {
  const W = SHIP.works, F = W && W.rank !== 'junior' && ffState(); if (!F) return;
  const d = worksDay(now), m = now - (d - 1) * 1440, C = caseState();
  if (!F.mail && d >= FF_FROM && m >= FF_MAIL && m < 1260) {
    F.mail = 1;
    const mail = worksText('mail.ticket.first', 'A ticket | A ticket case, when you\'re ready. On the Works board, any shift. — Calder'), cut = mail.indexOf(' | ');
    if (typeof mailSend === 'function') mailSend({ at: now, from: worksName('calder'), subject: cut > 0 ? mail.slice(0, cut) : 'A ticket', body: cut > 0 ? mail.slice(cut + 3) : mail });
  }
  const j = F.job && SHIP.jobs.find(x => x.id === F.job), c = j && C && (C.open.find(x => x.job === j.id) || null);
  if (F.job && j) {
    if (c && c.fits > 0 && !j.workDone) {                // a wrong call fitted (crossing suspects out on the notepad isn't one): not yet, next week (the job a plain repair)
      F.tries++; F.next = d + 7; F.job = null; if (typeof caseRelease === 'function') caseRelease(c, j); jobRelease(FF_SLOT);
      if (!skip) try { toast(j.title, worksText('ticket.wrong', 'Not yet. Next week.')); } catch (e) { /* no UI */ }
      simNote('ticket', { step: 'wrong', tries: F.tries });
      return;
    }
    if (j.status === 'done') { F.job = null; if (j.doneBy === 'you' && j.rightFirst !== false) ffGrade(1, now); return; }
    if (!heldForYou(j) && j.claimedBy !== 'you') F.job = null;   // released at 17:00: the crew's; back tomorrow
    return;
  }
  if (F.job && !j) F.job = null;
  if (F.grade >= 1 || d < Math.max(FF_FROM, F.next) || !playerShiftOn(d) || m < FF_POST || m > DAY_SHIFT[1] - 120) return;
  if (SHIP.jobs.some(x => x.ticket && worksDay(x.posted) === d)) return;   // one a day
  ffPost(now);
});
WORK_TICKS.push(() => { if (SHIP.works && SHIP.works.side && SHIP.works.side.ff && SHIP.works.side.ff.grade && typeof player !== 'undefined' && player && (PLAYER_SPEC.pin || 0) !== SHIP.works.side.ff.grade) ffPin(); });   // a reload: the pin back on

// ---------------------------------------------------------------------
// 24o LEAK HUNTING (M13, seat E2 (M2's), 0.51.x; plans/mechanics/m13-leak-hunting.html). A side job from Day 12, an
// Officer's: about once a week (a workday of yours, posted 08:00) a pipe joint starts to drip and the board says only "A
// pipe drips somewhere on Deck 4". Find it: a puddle on the floor and a damp patch on the wall show the room; look at the
// puddle ("coming from above, along the north wall"), then the damp, then the joint: tighten it (a turn), or if it's worn
// through, a joint from stores (section 17's jointJobPost, held for you). Ladder row m13 (24 core's table, E1: small, Day 12 = LEAK_FROM, stages at 0 and LEAK_GALLERY uses, by LEAK_BY; its first use is the
// training, at the puddle: the Works officer on shift finds it with you, the writer's meeting train.m13.<id>). Not taken
// by the end of your shift: held till 09:00 the next workday, then the crew find it the long way (an hour). Stages: 0 a
// public room; 1 after 3 leaks also the Deck 5 pipe galleries (works: true places behind their panels); with the pipe kit
// (24i's, M9) the puddle's look adds the kit's damp reading. The joints are E3's places (DECKS[n].leakJoints, n-leak-k
// and n-leakp-k, Decks 3-5): on Decks 3-4 the joint itself wears (no machine), on Deck 5 a gallery joint by a worn valve
// is likelier and likelier worn through. Drawn: the puddle (flat discs 1.2 cm up, one instanced draw call) and the damp
// patch (discs 1.5 cm off the wall, one more), only while a leak is open on your deck. Saved: SHIP.works.side.leaks =
// [{ id, joint, room, deck, day, worn, found }] (the last 12; found: 'you', a crew id, or null while open), read back
// defensively (24 core's worksSide keeps side whole). Hash keys 1013 (which joint, worn through), 1014 (which day). No R().
const LEAK_FROM = 12, LEAK_POST = 480, LEAK_LAST = 900, LEAK_KEEP = 12;   // from Day 12; posted 08:00 (the first by 15:00)
const LEAK_CREW = 60, LEAK_GALLERY = 3;                  // the crew's long way (minutes); the galleries after 3 leaks of yours
const LEAK_BY = ['torres-zeke', 'halloran-emeka', 'calder'];
const leakSide = () => typeof worksSide === 'function' ? worksSide() : null;
function leakList() {                                    // side.leaks, cleaned the first time it's read (a save may hold junk)
  const s = leakSide(); if (!s) return null;
  if (!Array.isArray(s.leaks) || !s.leaksOk) {
    s.leaks = (Array.isArray(s.leaks) ? s.leaks : []).filter(e => e && typeof e.id === 'string' && typeof e.joint === 'string' && [3, 4, 5].includes(e.deck) && Number.isInteger(e.day))
      .slice(-LEAK_KEEP).map(e => ({ id: e.id.slice(0, 80), joint: e.joint.slice(0, 40), room: typeof e.room === 'string' ? e.room.slice(0, 4) : null, deck: e.deck, day: e.day, worn: e.worn ? 1 : 0, found: typeof e.found === 'string' ? e.found.slice(0, 40) : null }));
    Object.defineProperty(s, 'leaksOk', { value: true, enumerable: false, configurable: true });   // (not saved)
  }
  return s.leaks;
}
const leakJoints = () => [3, 4, 5].flatMap(n => ((DECKS[n] && DECKS[n].leakJoints) || []).filter(J => J && placeById(J.place)).map(J => ({ ...J, deck: n })));
const leakJoint = id => leakJoints().find(J => J.place === id) || null;
const leakFound = () => (leakList() || []).filter(e => e.found === 'you').length;
const leakOpen = () => (leakList() || []).find(e => !e.found) || null;
const leakSeed = () => machSeed('leak');
const LEAK_WALL = { n: 'north', s: 'south', e: 'east', w: 'west' };
function leakValveWear(J) {                              // a gallery joint by a worn valve (Deck 5's 5-valve-1/-2): 0-1
  if (!J.gallery) return 0; const p = placeById(J.place); if (!p) return 0;
  const vs = machineList().filter(m => m.kind === 'valve' && m.deck === J.deck && Math.hypot(m.at[0] - p.at[0], m.at[1] - p.at[1]) <= 6);
  return vs.reduce((a, m) => Math.max(a, incWear(m.id)), 0);
}
// the week's leak day: a workday of yours, Day 12 on, not the week's incident day or a test job's day; null if none
function leakDay(w) {
  const W = SHIP.works; if (!W) return null; const P = incState() ? incPlan(w) : null;
  const days = [0, 1, 2, 3, 4].map(k => w * 7 + 1 + k).filter(d => d >= LEAK_FROM && playerShiftOn(d) && !(P && P.length && P[1] === d) && !(W.test && W.test.day === d));
  return days.length ? days[Math.floor(schedU(leakSeed(), w, 1014) * days.length) % days.length] : null;
}
// which joint drips (week w): public ones first; after 3 leaks the galleries too, by their valves' wear; worn through 1 in 3
function leakPick(w) {
  const all = leakJoints(), Js = all.filter(J => !J.gallery || leakFound() >= LEAK_GALLERY); if (!Js.length) return null;
  const wt = Js.map(J => J.gallery ? 2 + 2 * leakValveWear(J) : 1), sum = wt.reduce((a, b) => a + b, 0);
  let u = schedU(leakSeed(), w, 1013) * sum, J = Js[0];
  for (let k = 0; k < Js.length; k++) { if (u < wt[k]) { J = Js[k]; break; } u -= wt[k]; }
  return { J, worn: schedU(leakSeed(), w * 7 + 2, 1013) < .3 + .4 * leakValveWear(J) ? 1 : 0 };
}
function leakPost(t, w = incWeek(worksDay(t))) {
  const L = leakList(); if (!L || leakOpen()) return null;
  const P = leakPick(w); if (!P) return null;
  const { J, worn } = P, p = placeById(J.place), d = worksDay(t);
  const j = jobMake('leak', { id: 'leak:' + J.place + '@' + Math.floor(t / 60), deck: J.deck, room: null, h: Math.floor(t / 60), joint: J.place, worn, urgency: 1,
    title: worksText('leak.card', 'A pipe drips somewhere on Deck {deck}', { deck: J.deck }), leave: Math.max(60, (d - 1) * 1440 + DAY_SHIFT[1] - Math.max(t, (d - 1) * 1440 + DAY_SHIFT[0])) + 60 });
  j.posted = j.found = t;
  SHIP.jobs.push(j); L.push({ id: j.id, joint: J.place, room: p.room || null, deck: J.deck, day: d, worn, found: null });
  if (L.length > LEAK_KEEP) L.splice(0, L.length - LEAK_KEEP);
  simNote('leak', { id: j.id, step: 'drip', deck: J.deck });
  if (typeof MACH_REV !== 'undefined') MACH_REV++;
  leakFx(); return j.id;
}
// the stops: the puddle (a look), the damp on the wall (a look at the joint), the joint (a turn, or a look when it's worn
// through). The damp and the joint have no place till you've looked at the puddle (the board says only the deck); the
// crew know where it is once they've taken it (the long way)
function leakStops(j) {
  const J = leakJoint(j.joint); if (!J) return [];
  const pp = J.puddlePlace && placeById(J.puddlePlace) ? J.puddlePlace : J.place, open = (j.stepsDone || []).includes(0) || (!!j.claimedBy && j.claimedBy !== 'you');
  const wall = LEAK_WALL[(J.damp && J.damp[2]) || J.wall] || 'near', kit = typeof hasTool === 'function' && hasTool('pipekit') && worksStage('m13') >= 1;
  return [
    { deck: J.deck, placeId: pp, mins: 1, tag: 'puddle', how: 'look', opts: { ...(kit ? { tool: 'pipekit' } : {}), secs: 3, text: worksText('leak.look.above', 'It\'s coming from above, towards {place}.', { place: 'the ' + wall + ' wall' })
        + (kit ? ' ' + worksText('leak.look.warmer', 'Wetter here. You\'re close.') : '') } },
    { deck: J.deck, placeId: open ? J.place : null, mins: 1, tag: 'damp', how: 'look', opts: { secs: 3, text: worksText('leak.look.here', 'There. A joint, weeping.') } },
    j.worn ? { deck: J.deck, placeId: open ? J.place : null, mins: 2, tag: 'joint', how: 'look', opts: { secs: 3, text: worksText('leak.worn', 'Worn right through. Tightening won\'t hold it: it needs a new joint from stores.') } }
      : { deck: J.deck, placeId: open ? J.place : null, mins: 2, tag: 'joint', how: 'turn', opts: { label: worksText('leak.fix.tighten', 'Tighten the joint'), v: 0, min: 0, max: 3, by: 1,
        onTurn: v => v >= 3 ? worksText('leak.tight', 'Snug. The drip stops.') : v > 0 ? worksText('leak.turning', 'A quarter turn. Still a bead of water. A bit more.') : null, ok: v => v >= 3, gauge: null } },
  ];
}
function leakStepDone(j, k, res, t) {
  if (k > 0 && !(j.stepsDone || []).includes(0)) return false;   // the puddle first
  if (k === 0 && SHIP.works.tr.m13 === undefined) {      // your first: the Works officer on shift finds it with you (the writer's meeting train.m13.<id>, else a word); trained here
    const row = ladderRow('m13'), by = (row && ladderTeacher(row, worksDay(t))) || LEAK_BY[0];
    if (!MEETING_SCRIPTS['train.m13.' + by] && !MEETING_SCRIPTS['train.m13']) worksTeach('m13', by, 'puddle', ['Follow the wet, not the noise. Well, both.']);
    worksTrained('m13', t);
  }
  if (k === 0 && typeof hasTool === 'function' && hasTool('pipekit') && worksStage('m13') >= 1 && typeof toolWear === 'function') toolWear('pipekit', 5);   // the kit's damp reading (24 core's wear, E1)
  return true;
}
// fixed (by you: found by you, the worn joint's replacement posted, held for you; by the crew: the long way). The puddle goes
function leakDone(j, t, by) {
  const e = (leakList() || []).find(x => x.id === j.id); if (e) e.found = by || 'crew';
  if (by === 'you') {
    worksUse('m13');                                    // +1 a leak (lead 17): no foundBy, so no found-by-you bonus; side.leaks keeps found
    try { toast(j.title, worksText('leak.done', 'Dry. Found it yourself.')); } catch (e) { /* no UI */ }
    if (j.worn && typeof jointJobPost === 'function') {
      const p = placeById(j.joint), F = jointJobPost({ placeId: j.joint, title: worksText('leak.fix.replace', 'Replace the joint ({part})', { part: 'a seal' }) + ': ' + ((p && roomName(p.deck, p.room)) || 'corridor') }), J = F && SHIP.jobs.find(x => x.id === F);
      if (J) { J.leave = Math.max(60, (worksDay(t) - 1) * 1440 + DAY_SHIFT[1] - t); J.xp = 0; j.fix = F; }   // no rep of its own: the leak's +1 covers it (24 core skips j.xp === 0; lead 17)
    }
  } else if (SHIP.works.tr.m13 !== undefined && t >= shipNow() - 1) try { toast(worksText('leak.card', 'A pipe drips somewhere on Deck {deck}', { deck: j.deck }), worksText('leak.found.crew', 'The crew found the drip on Deck {deck}. The long way.', { deck: j.deck })); } catch (e) { /* no UI */ }
  simNote('leak', { id: j.id, step: 'fixed', by: by || null });
  if (typeof MACH_REV !== 'undefined') MACH_REV++;
  leakFx();
}
if (typeof jobKindAdd === 'function') jobKindAdd('leak', { tier: 2, work: 0, text: 'Leak', stops: leakStops, stepDone: leakStepDone, done: leakDone, veto: true,
  crew: { can: incWorks, mins: LEAK_CREW } });
if (typeof WORKS_SIDE_KINDS !== 'undefined' && WORKS_SIDE_KINDS.add) WORKS_SIDE_KINDS.add('leak');   // 24 core: a side job's reputation, capped
if (JOB_KINDS.leak) WORK_MECH.m13 = {};
// the clock: the first leak once the row is open (that day by 15:00, else the next workday's 08:00), then the week's on its
// day at 08:00 (a week with one already, none). After a skip the crew have it in time
if (WORK_MECH.m13) WORK_TICKS.push((now, skip) => {
  const W = SHIP.works, L = W && leakList(); if (!L || !worksOpened(W).has('m13')) return;
  const d = worksDay(now), m = now - (d - 1) * 1440, w = incWeek(d);
  if (leakOpen() || m < LEAK_POST || !playerShiftOn(d)) return;
  if (!L.length) { if (m <= LEAK_LAST || skip) leakPost(now, w); return; }
  if (L.some(e => incWeek(e.day) === w) || leakDay(w) !== d) return;
  leakPost(now, w);
});
// ---- the look: puddleAt(spots) (the puddle decal, M6's look: flat discs 1.2 cm off the floor, 3 mm apart) and the damp patch on the
// wall (discs 1.5 cm off its face, hidden with its wall when the cutaway lowers it), each one instanced draw call, made the first time a leak is open on your deck (in
// deckRoot, so the deck's unload frees them) ----
const LEAK_FX = { root: null, wet: null, damp: null, decor: null, at: null };
function puddleAt(spots, o = {}) {                       // spots: [[x, z, scale]] (tile units, a spot's centre); one instanced mesh in deckRoot
  const g = new THREE.CircleGeometry(.5, 18); g.rotateX(-Math.PI / 2);
  const im = new THREE.InstancedMesh(g, new THREE.MeshBasicMaterial({ color: col(o.color || '#4f86a8'), transparent: true, opacity: o.opacity || .5, depthWrite: false }), spots.length), M4 = new THREE.Matrix4();
  spots.forEach(([x, z, s], k) => { M4.makeScale(s || 1, 1, (s || 1) * .85); M4.setPosition(X0(x), .012 + .003 * k, Z0(z)); im.setMatrixAt(k, M4); });
  im.userData.noMerge = true; deckRoot.add(im); return im;
}
function leakFx() {
  try {
    if (typeof deckRoot === 'undefined' || !deckRoot || !deckDef) return;
    const e = leakOpen(), J = e && e.deck === deckDef.num ? leakJoint(e.joint) : null;
    if (LEAK_FX.root !== deckRoot || LEAK_FX.at !== (J && J.place)) {
      for (const k of ['wet', 'damp']) if (LEAK_FX[k] && LEAK_FX.root === deckRoot) { deckRoot.remove(LEAK_FX[k]); LEAK_FX[k].geometry.dispose(); LEAK_FX[k].material.dispose(); }
      if (LEAK_FX.decor) WALL_DECOR = WALL_DECOR.filter(x => x !== LEAK_FX.decor);
      LEAK_FX.root = deckRoot; LEAK_FX.wet = LEAK_FX.damp = LEAK_FX.decor = null; LEAK_FX.at = J ? J.place : null;
      if (J && J.puddle) LEAK_FX.wet = puddleAt([[J.puddle[0], J.puddle[1], 1.05], [J.puddle[0] + .35, J.puddle[1] - .2, .5]]);   // E3's puddle: a floor spot (tile units, centred)
      const dk = J && J.damp && FACING[J.damp[2]] !== undefined ? (([x, z, w]) => w === 'n' || w === 's' ? `h,${Math.floor(x)},${w === 'n' ? Math.floor(z) : Math.ceil(z)}` : `v,${w === 'w' ? Math.floor(x) : Math.ceil(x)},${Math.floor(z)}`)(J.damp) : null, de = dk && EDGES.get(dk);
      if (de && (de.type === 'wall' || de.type === 'hull')) {   // only on a solid wall (never a door or open floor)
        const [x, z, wall] = J.damp, y = Math.max(1.15, ((J.joint && J.joint[1]) || 1.2) + .5);   // on the wall's light panel above the joint, streaking down to it
        const pos = { n: [X0(x), Z0(Math.floor(z)) + T / 2], s: [X0(x), Z0(Math.ceil(z)) - T / 2], w: [X0(Math.floor(x)) + T / 2, Z0(z)], e: [X0(Math.ceil(x)) - T / 2, Z0(z)] }[wall];   // E3's damp: the joint's spot by its wall; the patch on the wall's face
        const g = new THREE.CircleGeometry(.32, 16), im = new THREE.InstancedMesh(g, new THREE.MeshBasicMaterial({ color: col('#3f4a4e'), transparent: true, opacity: .42, depthWrite: false }), 2), M4 = new THREE.Matrix4(), Q = new THREE.Quaternion().setFromEuler(new THREE.Euler(0, FACING[wall], 0));
        const ax = new THREE.Vector3(1, 0, 0).applyQuaternion(Q), nx = new THREE.Vector3(0, 0, 1).applyQuaternion(Q);   // along the wall, out of it
        [[0, 0, 1, 1.2, .015], [.05, -.4, .55, 1.1, .02]].forEach(([dx, dy, sx, sy, off], k) => { M4.compose(new THREE.Vector3(pos[0] + ax.x * dx + nx.x * off, y + dy, pos[1] + ax.z * dx + nx.z * off), Q, new THREE.Vector3(sx, sy, 1)); im.setMatrixAt(k, M4); });   // never coplanar: 5 mm apart
        im.userData.noMerge = true; deckRoot.add(im); LEAK_FX.damp = im;
        WALL_DECOR.push(LEAK_FX.decor = { g: im, e: de });   // the main loop hides it while the cutaway lowers its wall, as any wall piece
      }
    }
  } catch (err) { console.error(err); }
}
WORK_TICKS.push((now, skip) => { if (!skip) leakFx(); });
// ---- the pool plant's leak (0.84.5, rec engineer B; plans/recdeck-plan.html section 6, "A Works story for tracing (tier 2)"):
// section 17's pool line (MACHINE_LINKS.pool, only while REC_DECK is on) is traced like the others (traceFor; the filters'
// seal is the only cause on it) and its symptom is named on Deck 5 (LINE_SHOWS): it shows first as a drip in main storage,
// right under the pool plant. While a pool job is open a puddle (24o's puddleAt) lies in the aisle at POOL_DRIP, and 24i's
// goal pointer (traceGoal asks poolDripGoal) takes you there first; once you've stood by it (j.drip, saved with the job)
// it's an ordinary trace: up the spine ladder to the pool plant, the pipe kit's readings (traceMark), found at the job's
// own filter. Nothing here runs without a pool job (none while REC_DECK is off). No R(), no hash keys
const POOL_DRIP = { deck: 5, place: '5-aisle-2', spot: [30.55, 4.35], near: 1.6 };   // main storage's aisle by the Plumbing shelves, under 7-pool-filter-2 (Deck 7's tiles sit 2 columns and a row on from Deck 5's)
const POOL_FX = { root: null, wet: null };
const poolDripJob = () => SHIP.jobs.find(j => j.symptom && j.symptom.line === 'pool' && j.status !== 'done') || null;
const poolDripDue = j => !!(j && j.symptom && j.symptom.line === 'pool' && traceHidden(j) && !j.drip && placeById(POOL_DRIP.place));   // your pool job, the drip not seen yet
const poolDripGoal = j => poolDripDue(j) ? { deck: POOL_DRIP.deck, place: POOL_DRIP.place, label: worksText('trace.pool.goal', 'See where it drips: main storage') } : null;
function poolDripSeen(j, t) {                            // you've stood by the drip: the goal pointer goes on up the line
  j.drip = t; j.touched = t; if (typeof MACH_REV !== 'undefined') MACH_REV++; if (typeof ixGoalAt !== 'undefined') ixGoalAt = -1;
  try { toast(traceTitle(j), worksText('trace.pool.drip', 'A slow drip from the ceiling, over the aisle. The pool plant is right above it.') + ' ' + worksText('trace.pool.up', 'Take the spine ladder up to the rec deck and read the pool line with the pipe kit.')); } catch (e) { /* no UI */ }
}
function poolDripFx() {                                  // the puddle, while a pool job is open and you're on Deck 5 (in deckRoot: the deck's unload frees it)
  try {
    if (typeof deckRoot === 'undefined' || !deckRoot || !deckDef) return;
    const on = deckDef.num === POOL_DRIP.deck && !!poolDripJob(); if (POOL_FX.root === deckRoot && !!POOL_FX.wet === on) return;
    if (POOL_FX.wet && POOL_FX.root === deckRoot) { deckRoot.remove(POOL_FX.wet); POOL_FX.wet.geometry.dispose(); POOL_FX.wet.material.dispose(); }
    const [x, z] = POOL_DRIP.spot; POOL_FX.root = deckRoot; POOL_FX.wet = on ? puddleAt([[x, z, .8], [x + .22, z + .3, .4]]) : null;
  } catch (err) { console.error(err); }
}
WORK_TICKS.push((now, skip) => {
  if (skip) return; poolDripFx();
  const j = typeof myJob === 'function' ? myJob() : null; if (!poolDripDue(j) || typeof player === 'undefined' || !player || !deckDef || deckDef.num !== POOL_DRIP.deck || !PLACE_OF.has(POOL_DRIP.place)) return;
  const sp = placeSpot(POOL_DRIP.place), p = player.obj.position; if (sp && Math.hypot(sp.x - p.x, sp.z - p.z) < POOL_DRIP.near) poolDripSeen(j, now);
});

// ---------------------------------------------------------------------
// 24q REWIRING (M15, seat E2, 0.51.x; plans/mechanics/m15-rewiring.html). From Day 17, an Officer's, about once a week
// (posted 08:00 on a workday of yours): "Rewire junction 4-J2" (a junction job set to Tier 2 on the job itself; the
// junction kind is Tier 3 in section 17). At the box's panel: open it (a look: the colour chart, 4-6 wires), then a
// choose step a wire (this wire: which terminal?), then close up and test (a hold). A wrong pair pops a fuse at the
// test: only that pair's stop opens again (never a fail); "right first time" if none. Done by you: the junction put
// right (section 17's machine to 90 at least), a use. Stage 1 (after 3): one colour on the chart has faded; flick the
// room's lights first (a look) and the chart's filled in. Stage 2 leads into P7 (Step 6). Ladder row m15 (24 core's
// table, E1: big, Day 17 = REW_FROM, Calder, the tester; the lesson is W2's meeting train.m15.calder at the officers'
// corridor's starboard utility closet: Calder rewires 4-junction-2 while you watch, then 4-junction-1 is yours). Not
// taken: held to the end of your shift and an hour of the next, then the crew's (45 minutes). Saved:
// SHIP.works.side.rewire = { done, wrongs, week } (jobs turned in, wrong pairs ever, the last week posted), cleaned on read; the job's own chart
// in ship.jobs (j.chart: colours by terminal, j.faded, j.pairs: the pick per pair). Hash keys 1016 (which junction,
// the wire count and chart), 1017 (which colour fades). No R().
const REW_FROM = 17, REW_POST = 480, REW_CREW = 45, REW_FADE = 3, REW_KEEP = 90;
const REW_TRAIN = ['4-junction-2', '4-junction-1'];      // Calder's, then yours (the officers' corridor's closet first)
const REW_COLS = ['red', 'blue', 'yellow', 'green', 'white', 'black'];
const rewSeed = () => machSeed('rewire');
const rewBoxes = () => machineList().filter(m => /junction/.test(m.id) && panelPlace(m.id) && !SHIP.jobs.some(j => j.machine === m.id && j.status !== 'done'));   // not one with a job open
function rewState() {                                    // side.rewire, cleaned (a save may hold junk)
  const s = typeof worksSide === 'function' ? worksSide() : null; if (!s) return null;
  const R = s.rewire;
  if (!R || typeof R !== 'object' || !s.rewOk) {
    s.rewire = { done: R && Number.isInteger(R.done) ? Math.max(0, Math.min(9999, R.done)) : 0, wrongs: R && Number.isInteger(R.wrongs) ? Math.max(0, Math.min(9999, R.wrongs)) : 0, week: R && Number.isInteger(R.week) ? R.week : -1 };
    Object.defineProperty(s, 'rewOk', { value: true, enumerable: false, configurable: true });
  }
  return s.rewire;
}
const rewName = id => { const m = id.match(/^(\d)-junction-(\d+)$/); return m ? m[1] + '-J' + m[2] : id; };   // 4-junction-2 -> 4-J2
const rewWire = c => worksText('wire.' + c, c);
// the chart for a key (week, or a training's day): 4-6 colours in terminal order, and (stage 1 on) two that have faded
function rewChart(k, stage) {
  const seed = rewSeed(), n = 4 + Math.floor(schedU(seed, k, 1016) * 3) % 3;
  const chart = REW_COLS.map((c, i) => [schedU(seed, k * 8 + i, 1016), c]).sort((a, b) => a[0] - b[0]).slice(0, n).map(x => x[1]);
  const faded = stage >= 1 ? chart.map((c, i) => [schedU(seed, k * 8 + i, 1017), i]).sort((a, b) => a[0] - b[0]).slice(0, 1).map(x => x[1]) : [];   // one colour (the page; lead 17)
  const order = chart.map((c, i) => [schedU(seed, k * 8 + 10 + i, 1016), i]).sort((a, b) => a[0] - b[0]).map(x => x[1]);   // the order the wires come to hand: the chart must be read (R5)
  return { chart, faded, order };
}
// the week's day: a workday of yours from Day 17, not the incident's, the leak's or a test job's
function rewDay(w) {
  const W = SHIP.works; if (!W) return null; const P = incState() ? incPlan(w) : null, L = typeof leakDay === 'function' ? leakDay(w) : null;
  const days = [0, 1, 2, 3, 4].map(k => w * 7 + 1 + k).filter(d => d >= REW_FROM && playerShiftOn(d) && !(P && P.length && P[1] === d) && d !== L && !(W.test && W.test.day === d));
  return days.length ? days[Math.floor(schedU(rewSeed(), w, 1017) * days.length) % days.length] : null;
}
function rewJob(id, t, o = {}) {
  const m = machineById(id); if (!m) return null;
  const k = o.key !== undefined ? o.key : worksDay(t), { chart, faded, order } = rewChart(k, o.stage || 0);
  const j = jobMake('rewire', { id: 'rewire' + (o.slot || '') + ':' + id + '@' + Math.floor(t / 60), machine: id, deck: m.deck, room: m.room, h: Math.floor(t / 60), tier: 2, urgency: 0,
    title: worksText('rewire.card', 'Rewire junction {junction}', { junction: rewName(id) }), chart, faded, order, pairs: {}, wrongs: 0,
    ...(o.slot ? { reserved: o.slot, until: (worksDay(t) - 1) * 1440 + DAY_SHIFT[1] } : { leave: Math.max(60, (worksDay(t) - 1) * 1440 + DAY_SHIFT[1] - Math.max(t, (worksDay(t) - 1) * 1440 + DAY_SHIFT[0])) + 60 }),
    ...(o.train ? { train: o.train } : {}) });
  j.posted = j.found = t;
  return j;
}
// the stops, all at the box's panel: open it (the chart), flick the lights (faded charts only), a pair per wire, test
function rewStops(j) {
  const m = machineById(j.machine), pp = m && panelPlace(m.id); if (!pp) return [];
  const chart = j.chart || [], fadedOpen = (j.faded || []).length && !(j.stepsDone || []).includes(1);
  const shown = chart.map((c, i) => 'T' + (i + 1) + ' ' + ((j.faded || []).includes(i) && fadedOpen ? '?' : rewWire(c))).join(' · ');
  const out = [{ deck: m.deck, placeId: pp, mins: 1, tag: 'open', how: 'look', opts: { secs: 3, text: shown + ((j.faded || []).length ? ' ' + worksText('rewire.faded', 'This one\'s faded. Which colour was it?') : '') } }];
  if ((j.faded || []).length) out.push({ deck: m.deck, placeId: pp, mins: 1, tag: 'check', how: 'look', opts: { secs: 3, text: worksText('rewire.check', 'Flick the lights. See which one goes off.') + ' ' + chart.map((c, i) => 'T' + (i + 1) + ' ' + rewWire(c)).join(' · ') } });
  for (const i of rewOrder(j)) out.push({ deck: m.deck, placeId: pp, mins: 1, tag: 'wire', how: 'choose', opts: { title: rewWire(chart[i]).replace(/^./, x => x.toUpperCase()),
    text: shown, options: chart.map((_, i) => ({ id: 'T' + (i + 1), label: 'T' + (i + 1) })) } });
  out.push({ deck: m.deck, placeId: pp, mins: 2, tag: 'test', how: 'hold' });
  return out;
}
const rewFirst = j => (j.faded || []).length ? 2 : 1;   // the first pair's stop
const rewOrder = j => Array.isArray(j.order) && j.order.length === (j.chart || []).length ? j.order : (j.chart || []).map((_, i) => i);   // (an older job: chart order)
const rewRight = (j, k) => 'T' + (rewOrder(j)[k - rewFirst(j)] + 1);   // the stop's wire's terminal on the chart
function rewStepDone(j, k, res, t) {
  const st = rewStops(j)[k]; if (!st) return true;
  if (!j.pairs || typeof j.pairs !== 'object') j.pairs = {}; if (!Number.isFinite(j.wrongs)) j.wrongs = 0;   // (a junk job)
  const done = new Set(j.stepsDone || []);
  if (st.tag !== 'open' && !done.has(0)) return false;   // open the box first
  if (st.tag === 'wire') { if (rewFirst(j) === 2 && !done.has(1)) return false; j.pairs[k] = res && res.pick || null; return true; }   // a faded chart: the lights first
  if (st.tag === 'test') {
    const S = rewStops(j), wires = S.map((s, i) => s.tag === 'wire' ? i : -1).filter(i => i >= 0);
    if (wires.some(i => !done.has(i))) return false;     // every pair in first
    const wrong = wires.filter(i => j.pairs[i] !== rewRight(j, i));
    if (wrong.length) {                                  // a fuse pops: only those pairs open again
      j.wrongs += wrong.length; j.stepsDone = (j.stepsDone || []).filter(i => !wrong.includes(i));
      for (const i of wrong) delete j.pairs[i];
      try { toast(j.title, worksText('rewire.pop', 'Pop. That pair\'s wrong. Swap them and try again.')); } catch (e) { /* no UI */ }
      return false;
    }
    if (!j.wrongs) try { toast(j.title, worksText('rewire.right', 'Right first time.')); } catch (e) { /* no UI */ }
  }
  return true;
}
function rewDone(j, t, by) {
  const s = SHIP.machines && SHIP.machines[j.machine];
  if (s) { s.cond = Math.max(s.cond, REW_KEEP); s.state = machineState(s.cond); }
  if (by === 'you') {
    const R = rewState(); if (R) { R.done++; R.wrongs += j.wrongs || 0; }
    worksUse('m15'); j.rightFirst = !j.wrongs;            // right first time: 24 core's turn-in pays its +1 (once)
    try { toast(j.title, worksText('rewire.done', 'Junction {junction} rewired. Lights steady.', { junction: rewName(j.machine) })); } catch (e) { /* no UI */ }
  }
  simNote('rewire', { id: j.id, machine: j.machine, by: by || null, wrongs: j.wrongs || 0 });
  if (typeof MACH_REV !== 'undefined') MACH_REV++;
}
if (typeof jobKindAdd === 'function') jobKindAdd('rewire', { tier: 2, work: 0, text: 'Rewire', stops: rewStops, stepDone: rewStepDone, done: rewDone, veto: true,
  crew: { can: incWorks, mins: REW_CREW } });
if (typeof WORKS_SIDE_KINDS !== 'undefined' && WORKS_SIDE_KINDS.add) WORKS_SIDE_KINDS.add('rewire');
// the lesson (ladder row m15, big): Calder's job on 4-junction-2 while you watch, then 4-junction-1 is yours (both held in
// the row's slot, a clear chart)
if (JOB_KINDS.rewire) WORK_MECH.m15 = {
  reserve(d, at, slot, o = {}) {
    const id = REW_TRAIN[o.yours ? 1 : 0], t = (d - 1) * 1440 + at; if (!machineById(id)) return null;
    SHIP.jobs = SHIP.jobs.filter(x => !(x.reserved === slot && heldForYou(x) && !x.claimedBy) && !(x.kind === 'rewire' && x.machine === id && x.claimedBy !== 'you' && x.status !== 'done'));
    const j = rewJob(id, t, { slot, train: o.train || 'm15', key: d * 2 + (o.yours ? 1 : 0) }); if (!j) return null;
    SHIP.jobs.push(j); if (typeof MACH_REV !== 'undefined') MACH_REV++;
    return j.id;
  },
  watch: 10,
};
// the clock: the week's rewiring at 08:00 on its day once you're trained (a week with one already, none)
if (WORK_MECH.m15) WORK_TICKS.push((now, skip) => {
  const W = SHIP.works; if (!W || W.tr.m15 === undefined || !rewState()) return;
  const d = worksDay(now), m = now - (d - 1) * 1440, w = incWeek(d);
  if (d <= W.tr.m15 || m < REW_POST || !playerShiftOn(d) || rewDay(w) !== d) return;
  const R = rewState(); if (R.week >= w) return;
  const boxes = rewBoxes(); if (!boxes.length) return;
  const id = boxes[Math.floor(schedU(rewSeed(), w, 1016) * boxes.length) % boxes.length].id, j = rewJob(id, now, { key: w * 7 + 3, stage: worksStage('m15') });
  if (j) { SHIP.jobs.push(j); R.week = w; if (typeof MACH_REV !== 'undefined') MACH_REV++; }
});

// ---------------------------------------------------------------------
// 24r IRRIGATION (M14, seat E2, 0.51.x; plans/mechanics/m14-irrigation.html; 24r, not the page's old 24p, which is C2's
// promotion: D3, 2026-10-19). Off shift, an Officer's, optional: on a harvest morning (section 16's gardenHarvestDay, the
// first on or after Day 13) while the garden crew pick, walk the garden's three grow racks (E3's DECKS[3].growRacks,
// 3-rack-1..3) and clear the clogged nozzles (2 to 4 in all, a short hold each at its rack). The next harvest is a little
// bigger: irrigationBonus(d), 0 to 0.1, by the share you cleared (section 16's harvest pick reads it, one typeof-guarded
// line; uncleared nozzles never lower it). Ladder row m14 (24 core's table, E1: small, Day 13 = NOZ_FROM, stages at 0, 2, 4 uses, by NOZ_BY; the first is the training, at the first rack: the
// gardener leading the harvest, the writer's meeting train.m14.<id>). That evening's salad gets a mention. Stages: 0 the nozzles; 1 after 2 harvests flush a rack's line (a wait, 5 ship
// minutes); 2 after 4 the irrigation plant (3-irrigation-1) gets a look, and a worn one is found by you. Nobody else
// clears them: the job goes at midnight, no harm. A friendship step with the gardeners on duty each time. Saved:
// SHIP.works.side.nozzles = { day, clogged: [rack, nozzle] pairs as 'r.n', cleared: [...], flushed, harvests, stage (that day's job's), bonus }
// (bonus: what this harvest's pick gets, from the one before; told: the day its salad was mentioned). Hash key 1015 (which nozzles). No R().
const NOZ_BY = ['cruz-tove', 'oneill-imani', 'hart-ravi'];   // the gardeners (the writer's meetings train.m14.<id>)
const NOZ_FROM = 13, NOZ_PER = 4, NOZ_HOLD = 2, NOZ_FLUSH = 5, NOZ_MAX = .1, NOZ_PLANT = '3-irrigation-1';
const nozRacks = () => ((DECKS[3] && DECKS[3].growRacks) || []).filter(R => R && placeById(R.place));
function nozState() {                                    // side.nozzles, cleaned (a save may hold junk)
  const s = typeof worksSide === 'function' ? worksSide() : null; if (!s) return null;
  const N = s.nozzles, ok = a => Array.isArray(a) ? a.filter(x => typeof x === 'string' && /^\d\.\d$/.test(x)).slice(0, 12) : [];
  if (!N || typeof N !== 'object' || !s.nozOk) {
    s.nozzles = { day: N && Number.isInteger(N.day) ? N.day : 0, clogged: ok(N && N.clogged), cleared: ok(N && N.cleared), flushed: N && N.flushed ? 1 : 0,
      harvests: N && Number.isInteger(N.harvests) ? Math.max(0, Math.min(999, N.harvests)) : 0, stage: N && Number.isInteger(N.stage) ? Math.max(0, Math.min(2, N.stage)) : 0, told: N && Number.isInteger(N.told) ? N.told : 0, bonus: N && Number.isFinite(N.bonus) ? Math.max(0, Math.min(NOZ_MAX, N.bonus)) : 0 };
    Object.defineProperty(s, 'nozOk', { value: true, enumerable: false, configurable: true });
  }
  return s.nozzles;
}
// the harvest's share of a usual one more (section 16 multiplies the harvest pick by 1 + this): only on the day it was
// worked out for, from the harvest before
function irrigationBonus(d = worksDay(shipNow())) { const N = SHIP.works ? nozState() : null; return N && N.day === d ? N.bonus : 0; }
// which nozzles are clogged on day d: 2 to 4 of the racks' twelve, by key 1015
function nozClogged(d) {
  const Rs = nozRacks(); if (!Rs.length) return [];
  const all = Rs.flatMap((R, r) => [...Array(NOZ_PER)].map((_, k) => r + '.' + k)), seed = machSeed('nozzles'), n = 2 + Math.floor(schedU(seed, d, 1015) * 3) % 3;
  return all.map((id, k) => [schedU(seed, d * 16 + k, 1015), id]).sort((a, b) => a[0] - b[0]).slice(0, n).map(x => x[1]).sort();
}
const nozLead = d => { try { const c = gardenCrew(d) || []; return (c.find(x => x.harvest && x.lead) || c.find(x => x.harvest) || c[0] || {}).id || null; } catch (e) { return null; } };
function nozPost(t) {
  const N = nozState(), d = worksDay(t); if (!N || N.day === d) return null;
  const was = N.clogged.length ? N.cleared.length / N.clogged.length : 0, fl = N.flushed;
  N.bonus = Math.round(NOZ_MAX * Math.min(1, was) * (N.stage >= 1 && N.day ? (fl ? 1 : .8) : 1) * 1000) / 1000;   // that harvest's job offered a flush (stage 1 on): flushing makes up the last fifth
  N.day = d; N.clogged = nozClogged(d); N.cleared = []; N.flushed = 0; N.stage = Math.max(0, worksStage('m14'));
  if (!N.clogged.length) return null;
  const j = jobMake('nozzle', { id: 'nozzle:3@' + Math.floor(t / 60), deck: 3, room: (placeById(nozRacks()[0].place) || {}).room || null, h: Math.floor(t / 60), urgency: 0,
    title: worksText('irr.clear', 'Clear the nozzles'), clogged: N.clogged.slice(), stage: N.stage, leave: 1440 });
  j.posted = j.found = t; SHIP.jobs.push(j);
  if (typeof MACH_REV !== 'undefined') MACH_REV++;
  return j.id;
}
// the stops: each rack with clogged nozzles (a hold, 2 minutes a nozzle), then (stage 1 on) flush the first rack's line
// (a wait), then (stage 2 on) a look at the irrigation plant
function nozStops(j) {
  const Rs = nozRacks(), by = r => (j.clogged || []).filter(x => +x[0] === r).length, out = [];
  Rs.forEach((R, r) => { if (by(r)) out.push({ deck: 3, placeId: R.place, mins: NOZ_HOLD * by(r), tag: 'rack' + r, how: 'hold' }); });
  if (j.stage >= 1 && Rs.length) out.push({ deck: 3, placeId: Rs[0].place, mins: 1, tag: 'flush', how: 'wait', opts: { mins: NOZ_FLUSH, label: worksText('irr.flush', 'Flush the line') } });
  const pp = typeof panelPlace === 'function' && machineById(NOZ_PLANT) ? panelPlace(NOZ_PLANT) : null;
  if (j.stage >= 2 && pp) out.push({ deck: 3, placeId: pp, mins: 1, tag: 'plant', how: 'look', opts: { secs: 3, text: worksText('noz.plant', 'The irrigation plant hums along. You check its filter and the pressure while you\'re here.') } });
  return out;
}
function nozStepDone(j, k, res, t) {
  const st = nozStops(j)[k], N = nozState(); if (!st || !N || N.day !== worksDay(j.posted)) return true;
  if (SHIP.works.tr.m14 === undefined) {                // your first: the gardener leading the harvest shows you the first rack (the writer's meeting train.m14.<id>); trained here
    if (!NOZ_BY.some(id => MEETING_SCRIPTS['train.m14.' + id])) { const by = nozLead(worksDay(t)); if (by) worksTeach('m14', by, 'rack', ['The nozzles clog. Clear each one and watch the water run even.']); }
    worksTrained('m14', t);
  }
  if (/^rack/.test(st.tag)) {
    const r = +st.tag.slice(4);
    for (const x of j.clogged || []) if (+x[0] === r && !N.cleared.includes(x)) N.cleared.push(x);
    try { toast(worksText('irr.title', 'Rack {n} · nozzles', { n: r + 1 }), worksText('irr.cleared', 'Clear. The water runs even again.')); } catch (e) { /* no UI */ }
  }
  if (st.tag === 'flush') { N.flushed = 1; try { toast(worksText('irr.flush', 'Flush the line'), worksText('irr.flushed', 'Flushed. The racks drink properly now.')); } catch (e) { /* no UI */ } }
  if (st.tag === 'plant' && typeof machineFound === 'function') { const s = SHIP.machines[NOZ_PLANT]; if (s && s.cond < 70) machineFound(NOZ_PLANT, 'you'); }
  return true;
}
function nozDone(j, t, by) {
  const N = nozState(); if (by !== 'you' || !N) return;
  N.harvests++; worksUse('m14');
  try { for (const c of gardenCrew(worksDay(t)) || []) if (c.harvest) relAdd(c.id, 'work', 2); } catch (e) { /* no crew */ }
  simNote('irrigation', { step: 'cleared', n: N.cleared.length, of: N.clogged.length });
}
if (typeof jobKindAdd === 'function') jobKindAdd('nozzle', { tier: 2, work: 0, text: 'Nozzles', stops: nozStops, stepDone: nozStepDone, done: nozDone, crew: { can: () => false, mins: 30 } });
if (typeof WORKS_SIDE_KINDS !== 'undefined' && WORKS_SIDE_KINDS.add) WORKS_SIDE_KINDS.add('nozzle');
if (JOB_KINDS.nozzle) WORK_MECH.m14 = {};
// the clock: on a harvest morning once the row is open, the job goes up when the crew start picking (the harvest
// gardeners' first minute, else 10:00) and stays till midnight; a job left from an earlier day goes
if (WORK_MECH.m14) WORK_TICKS.push((now, skip) => {
  const W = SHIP.works; if (!W || !nozState()) return;
  const d = worksDay(now), m = now - (d - 1) * 1440;
  for (const j of SHIP.jobs) if (j.kind === 'nozzle' && j.status !== 'done' && worksDay(j.posted) < d) { if (j.claimedBy === 'you' && typeof dropJob === 'function') dropJob(j.id); j.status = 'done'; j.doneAt = now; j.doneBy = null; }
  const N = nozState();
  if (N.day === d && N.bonus > 0 && N.told !== d && m >= 1080 && m < 1260 && !skip) { N.told = d; try { toast(worksText('irr.clear', 'Clear the nozzles'), worksText('irr.salad', 'Tonight\'s salad is extra crunchy. The garden says thank you.')); } catch (e) { /* no UI */ } }   // that evening's salad (18:00-21:00)
  if (!worksOpened(W).has('m14') || d < NOZ_FROM || N.day === d || !gardenHarvestDay(d)) return;
  let from = 600; try { const c = (gardenCrew(d) || []).filter(x => x.harvest && x.pick); if (c.length) from = Math.min(...c.map(x => x.pick[0])); } catch (e) { /* no crew */ }
  if (m >= from && m < GARDEN.harvest) nozPost(now);
});

// 24p THE FIRST PROMOTION (Pillar 5 Step 3, the Works career engineer C2, 0.44.18+; plans/mechanics/promotion-officer.html
// on claude/p5-design). Part 1, the Tier 2 test job: once you're "Relied on" and trained to make things safe (ladder
// row t2's needs), on a workday from Day 8 (from 09:10, after the Monday briefing) Calder tells you "Tomorrow, your
// test job": in person if you're in the Works bay, else by Mail at 10:00 (SHIP.works.test = { tier: 2, day: the test's
// day, tries, passed }). On that day (never before Day 9) the ladder opens t2 (WORK_MECH.t2.offer, no meeting): a real
// Tier 2 job held for you (jobReserve slot 20, from 09:00 to 15:00) on one of Deck 4's air scrubbers (the one in the worse
// state; section 17 gives it its cause), Calder following you (worksEscort) with a word at each step (worksTeach, flags
// train.t2.<step>). Passed when you turn it in, however it went. Only ever delayed: not taken by 15:00, or dropped, and
// she says what to practise and sets another in two workdays (test.day), no limit. Words: the head writer's promo.*.
const PROMO = { from: 8, at: 550, mailAt: 600, jobAt: 540, until: 900, slot: 20, again: 2, machines: ['4-scrubber-1', '4-scrubber-2'] };
const promoWorkday = (d, n = 1) => { let k = d; for (let i = 0; i < 28 && n > 0; i++) { k++; if (playerShiftOn(k)) n--; } return k; };   // the n-th workday of yours after day d
function promoSay(id, key, fallback, vars) {             // a line from the writer (promo.<key>), in the speaker's bubble or a toast
  const text = worksText('promo.' + key, fallback, vars); if (text) worksSay(id, text); return text;
}
function promoInBay() { try { return deckDef.num === 5 && roomAt(...player.here()) === 'w'; } catch (e) { return false; } }
function promoAnnounce(now) {                            // Day 8 on: "Tomorrow, your test job"
  const W = SHIP.works, d = worksDay(now), m = now - (d - 1) * 1440, row = ladderRow('t2');
  if (!W || W.tier !== 1 || W.test || !row || !WORK_MECH.t2 || d < PROMO.from || !playerShiftOn(d) || m < PROMO.at || m >= DAY_SHIFT[1] || !ladderNeeds(row.needs, W)) return;
  const by = ladderTeacher(row, d) || 'calder', here = promoInBay();
  if (!here && m < PROMO.mailAt) return;
  W.test = { tier: 2, day: Math.max(row.day, promoWorkday(d)), tries: 0, passed: false };
  if (here) promoSay(by, 'announce', 'Tomorrow, your test job. Tier 2, with me watching. Nothing you haven\'t done.');
  else if (typeof mailSend === 'function') { const t = worksText('promo.announce.mail', 'Your test job | Tomorrow: your Tier 2 test job, with me watching. Be in the bay at nine. — C.'), i = t.indexOf(' | ');
    mailSend({ at: now, from: worksName(by), subject: i > 0 ? t.slice(0, i) : 'Your test job', body: i > 0 ? t.slice(i + 3) : t }); }
  simNote('promoTest', { step: 'set', day: W.test.day });
}
const promoMachine = () => { try { machinesNow(); } catch (e) { /* on paper */ } const ms = PROMO.machines.filter(id => typeof machineById === 'function' && machineById(id));
  return ms.sort((a, b) => ((SHIP.machines[a] || {}).cond || 100) - ((SHIP.machines[b] || {}).cond || 100) || (a < b ? -1 : 1))[0] || 'scrubber'; };   // the one in the worse state
WORK_MECH.t2 = {
  offer(row, c, d, t) {                                  // the test, on its day: the job held for you, Calder with you
    const W = SHIP.works; if (!W || !W.test || W.test.passed || d < W.test.day) return false;
    const m = t - (d - 1) * 1440; if (m >= PROMO.until - 60) return false;
    let id = null; try { id = jobReserve(promoMachine(), d, Math.max(m, PROMO.jobAt), PROMO.slot, { tier: 2, train: 't2', until: (d - 1) * 1440 + PROMO.until, cause: 'filter', drift: 2 }); } catch (e) { id = null; }
    if (!id) return false;
    c.st = 'do'; c.j = id; c.occ = null; c.told = true; W.test.tries++; W.test.day = d;
    const j = SHIP.jobs.find(x => x.id === id); if (j) j.train = 't2';
    if (t >= shipNow() - 1) promoTestTell(c);
    simNote('promoTest', { step: 'start', day: d, job: id });
    return true;
  },
  noJob: false,
};
function promoTestTell(c) {                              // the start in play: Calder's word (or a toast), the goal to the job
  promoSay(c.by, 'test.start', 'Your test job\'s on the board: one of Four\'s scrubbers. Take it when you\'re ready. I\'ll be with you.');
  const j = SHIP.jobs.find(x => x.id === c.j), m = j && typeof machineById === 'function' ? machineById(j.machine) : null;
  if (m && typeof setGoal === 'function' && !(SHIP.player && SHIP.player.track)) setGoal({ deck: m.deck, room: m.room, label: 'Your test job' });
}
function promoPassed(t) {                                // the test job turned in: passed, whatever it took
  const W = SHIP.works, c = W && W.cur; if (!W || !W.test || W.test.passed) return false;
  const by = (c && c.by) || 'calder';
  W.test.passed = true; W.test.day = worksDay(t); W.tr.t2 = worksDay(t); if (c && c.id === 't2') W.cur = null;
  promoSay(by, 'test.passed', 'Good. That\'s the test. Go and have your tea; I\'ll be in touch.');
  simNote('promoTest', { step: 'passed', day: worksDay(t) });
  return true;
}
function promoDelay(now) {                               // not taken by 15:00, or dropped: set again in two workdays
  const W = SHIP.works, c = W && W.cur; if (!c || c.id !== 't2' || c.st !== 'again' || !W.test || W.test.passed) return;
  const d = worksDay(now); W.test.day = promoWorkday(d, PROMO.again); c.st = 'ask'; c.d = d; c.j = null;
  const text = worksText('promo.test.again', 'Not today, then. Get a few more scrubbers\' worth of filters under your belt; we\'ll try again on {day}.', { day: dayName(W.test.day) });
  if (promoInBay()) worksSay(c.by, text); else if (typeof mailSend === 'function') mailSend({ at: now, from: worksName(c.by), subject: 'Your test job', body: text });
  simNote('promoTest', { step: 'delayed', day: W.test.day });
}
const dayName = d => { try { return ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][weekday(d)]; } catch (e) { return 'your next workday'; } };
onSim('job', n => {                                      // Calder's word at each step of the test
  const c = SHIP.works && SHIP.works.cur; if (!n || !c || c.id !== 't2' || c.st !== 'do' || n.id !== c.j) return;
  const key = n.step === 'stop' ? 'step.' + (n.tag || 'stop') : 'step.' + n.step;
  if (n.step === 'stop' && n.tag === 'job') { const j = SHIP.jobs.find(x => x.id === c.j);   // the filter in: then the fan's setting (S2's drift +2), settled as part of the job
    if (j && j.machine && typeof tuneSet === 'function') try { tuneSet(j.machine, 0); } catch (e) { /* no drift in this build */ }
    worksTeach('t2', c.by, 'step.tune', 'Filter\'s in. Now settle the fan: bring the setting back to the middle. That\'s it.'); }
  worksTeach('t2', c.by, key, { take: 'Right. Your job; I\'m only watching.', done: 'That\'s it settled. Turn it in at the board.' }[n.step] || null);
});
WORK_TICKS.push((now, skip) => { promoAnnounce(now); promoDelay(now); });
// Part 2, the summons and the promotion (0.44.19): the first workday after the test is passed (one Calder is on shift),
// an appointment in her office at 11:00 (OCCASIONS.promoSummons, booked at 06:00), an urgent toast at 10:30 with the goal
// arrow and Torres's nudge; not in the Works bay by 11:15 and she comes to find you (worksEscort 'follow') and says it
// where you are. The scene (MEETING_SCRIPTS['promo.officer'], the writer's; a stand-in here): she tells you you've
// passed, the badge and the pip, one reply of three that she remembers (flag promo.reply: 1 proud, 2 surprised, 3 about
// time). At its end, or by 12:00 whatever happens (asleep, a day off: her words by Mail), you're promoted: Tier 2,
// rank officer, xp 0 ("New officer"), simNote('promoted', { tier: 2, rank: 'officer' }), done 'summons2', ms
// ['officer', day]. promoPlan() says, from the save alone, when each step is (for the sim's gathering at the board
// 11:10-11:25, and the move and the ceremony to come): the crew side is the sim engineer's.
Object.assign(PROMO, { summonsAt: 660, warnAt: 630, seekAt: 675, latest: 720, gather: [670, 685], by: ['calder', 'vance'] });
OCCASIONS.promoSummons = { title: 'The Chief\'s office', kind: 'summons', by: 'calder', deck: 5, room: 'o', at: PROMO.summonsAt, len: 30, script: 'promo.officer', due: () => false, mail: null };
const promoDone = k => !!(SHIP.works && SHIP.works.done.includes(k));
function promoSummonsDay() {                             // the first workday after the test with Calder on shift (Vance if she's away a week)
  const W = SHIP.works; if (!W || !W.test || !W.test.passed) return null;
  for (let d = W.test.day + 1, n = 0; n < 14; d++, n++) if (playerShiftOn(d) && (n >= 7 || occOnShift('calder', d))) return d;
  return null;
}
function promoPlan() {                                   // pure, from the save: { summons, gather, move, ceremony } as { day, at } (or null)
  const W = SHIP.works, sd = promoSummonsDay(); if (!W || !sd) return null;
  const ms = d => (W.ms.find(x => x[0] === d) || [])[1];
  const od = ms('officer') || sd;
  return { summons: { day: sd, at: PROMO.summonsAt }, gather: { day: od, from: PROMO.gather[0], to: PROMO.gather[1] }, move: { day: od, at: DAY_SHIFT[1] }, ceremony: { day: od + 1, at: 1035 }, done: W.done.slice() };
}
function promoScript() {                                 // the writer's scene, or a stand-in; either way our hooks on it
  if (!MEETING_SCRIPTS['promo.officer']) MEETING_SCRIPTS['promo.officer'] = { title: 'The Chief\'s office', from: 'Chief Ines Calder', stub: true,
    gist: 'Chief Calder: you passed your test job. You\'re a Works Officer now, Technician, Tier 2. Your badge and your pip are with Torres.',
    lines: [
      { who: 'calder', text: 'Sit down. You passed. The scrubber, the filter, the fan: all of it.', to: 'you' },
      { who: 'calder', text: 'So. Technician\'s badge. And this is your Officer\'s pip. Collar, left side.', pose: 'gesture' },
      { choice: [
        { text: 'Thank you, Chief. I won\'t let you down.', reply: { who: 'calder', text: 'I know. That\'s why you\'ve got it.' } },
        { text: 'Me? Already?', reply: { who: 'calder', text: 'Already. Don\'t make me explain it twice.' } },
        { text: 'About time.', reply: { who: 'calder', text: 'Ha. Don\'t push your luck, Officer.' } },
      ] },
      { who: 'calder', text: 'The bay\'s waiting for you. Go on.' },
    ] };
  const sc = MEETING_SCRIPTS['promo.officer'];
  if (!sc.promoHooked) { const pick = sc.onPick, end = sc.onEnd; sc.promoHooked = true;
    sc.onPick = (k, c) => { if (typeof flagSet === 'function') flagSet('promo.reply', k + 1); if (pick) pick(k, c); };
    sc.onEnd = finished => { if (end) end(finished); promoPromote(shipNow(), finished ? 'met' : 'left'); }; }
  return sc;
}
if (SHIP.occasions.some(r => r.id === 'promoSummons')) promoScript();   // a reload with the summons booked
function promoPromote(now, how) {                        // you're an officer
  const W = SHIP.works; if (!W || W.tier !== 1 || !W.test || !W.test.passed) return false;
  const d = worksDay(now), r = SHIP.occasions.find(x => x.id === 'promoSummons' && x.status === 'asked'); if (r) r.met = true;
  W.tier = 2; W.rank = 'officer'; W.xp = 0;
  if (!W.done.includes('summons2')) W.done.push('summons2'); if (!W.ms.some(x => x[0] === 'officer')) W.ms.push(['officer', d]);
  if (how === 'mail' && typeof mailSend === 'function') { const t = worksText('promo.mail', 'You\'re an officer | You passed your test job: you\'re a Works Officer now, Technician, Tier 2. Your badge and pip are waiting in my office. Well done. — C.'), i = t.indexOf(' | ');
    mailSend({ at: now, from: 'Chief Ines Calder', subject: i > 0 ? t.slice(0, i) : 'You\'re an officer', body: i > 0 ? t.slice(i + 3) : t }); }
  if (typeof newsAdd === 'function') try { newsAdd({ id: 'promo.officer', about: 'you', lines: [worksText('promo.news', '{me}\'s been made a Works Officer. Calder says it was about time.')], seed: ['dept:works'], kind: 'gossip' }); } catch (e) { /* no social */ }
  if (typeof mailSend === 'function') { const t = worksText('promo.captain', 'Congratulations | Chief Calder tells me you\'ve passed your Tier 2 test. Congratulations, Officer. I look forward to the ceremony. — O. Marrow'), i = t.indexOf(' | ');
    mailSend({ at: now + 30, from: 'Captain Odile Marrow', subject: i > 0 ? t.slice(0, i) : 'Congratulations', body: i > 0 ? t.slice(i + 3) : t, quiet: true }); }
  promoFriendMail(now);
  if (typeof MACH_REV !== 'undefined') MACH_REV++;       // the board: Tier 2 jobs for you now, junior ones no longer held (forYou)
  simNote('promoted', { tier: 2, rank: 'officer', how });
  return true;
}
function promoFriendMail(now) {                         // a word from up to two friends (W2's mail.promo.friend, 'Subject | body' with {me})
  if (typeof mailSend !== 'function') return;
  promoGuests(worksDay(now)).slice(PROMO.guests.length, PROMO.guests.length + 2).forEach((id, k) => {
    const t = careerText('mail.promo.friend', k) || 'Officer! | Heard the news. Knew you would. Drinks on me in the lounge. ' + worksFirst(id) + '.', i = t.indexOf(' | ');
    mailSend({ at: now + 60 + 30 * k, from: worksName(id), subject: i > 0 ? t.slice(0, i) : 'Congratulations', body: i > 0 ? t.slice(i + 3) : t, quiet: true }); });
}
function promoSummonsTick(now) {                         // book it, warn at 10:30, find you at 11:15, promote by 12:00
  const W = SHIP.works; if (!W || W.tier !== 1 || !W.test || !W.test.passed) return;
  const sd = promoSummonsDay(), d = worksDay(now), m = now - (d - 1) * 1440; if (!sd || d < sd) return;
  let r = SHIP.occasions.find(x => x.id === 'promoSummons');
  if (!r && d === sd && m < PROMO.latest) { promoScript(); r = occasionAdd('promoSummons', (d - 1) * 1440 + PROMO.summonsAt, true, 30); }
  if (d > sd || m >= PROMO.latest || (r && r.status === 'missed')) { promoPromote(now, 'mail'); return; }   // never missed: by noon it's done
  if (!r) return;
  const f = r.f || (r.f = {});
  if (m >= PROMO.warnAt && !f.warn && now >= shipNow() - 1) { f.warn = 1;
    const text = worksText('promo.summons', 'Chief Calder: My office, 11:00. — C.');
    if (typeof deviceNotify === 'function') try { deviceNotify({ app: 'calendar', text, urgent: true }); } catch (e) { /* no device */ }
    try { toast('Chief Calder', text); } catch (e) { /* no UI */ }
    if (typeof setGoal === 'function') setGoal({ deck: 5, room: 'o', label: 'The Chief\'s office, 11:00' });
    if (promoInBay()) promoSay('torres-zeke', 'summons.torres', 'Go on. She doesn\'t bite. Usually.'); }
  if (m >= PROMO.seekAt && !f.seek && !r.met && !promoInBay() && !(typeof DIALOGUE !== 'undefined' && DIALOGUE)) f.seek = now;   // 11:15: she comes to you
}
function promoSeekTick(now) {                            // she's found you: the scene where you are
  const r = SHIP.occasions.find(x => x.id === 'promoSummons' && x.status === 'asked'); if (!r || !r.f || !r.f.seek || r.met || (typeof DIALOGUE !== 'undefined' && DIALOGUE)) return;
  try { const a = DECK_CREW.find(x => x.p && x.p.id === r.by), p = player.obj.position;
    if (a && Math.hypot(a.x - p.x, a.z - p.z) < 2.2) { worksSayAll(r.by, worksVoice(r.by, 'promo.fetch.summons') || ['There you are. My office was the idea, but this will do.']);   // her word as she reaches you, then the scene
      promoScript(); r.met = true; dialogueShow('promo.officer', { id: r.key, who: [r.by], at: now }); } } catch (e) { /* not in play */ }
}
function promoEscort(p, t) {                             // worksEscort's 24p part: Calder walking over to find you
  const r = SHIP.occasions.find(x => x.id === 'promoSummons' && x.status === 'asked');
  return r && r.f && r.f.seek && !r.met && p.id === r.by && t < r.at + r.len ? { mode: 'follow', to: null } : null;
}
WORK_TICKS.push((now, skip) => { promoSummonsTick(now); if (!skip) promoSeekTick(now); });
// Brennan's cake (the lead's: part of the promotion): on the promotion's day, 16:30-17:00 at the Works tea corner, before
// Calder's walk to your cabin. Brennan stands there with it (the sim engineer's crewScene, if it's in the build); a toast
// tells you, and coming within 3 m of her plays her lines (flag promo.cake, once). Optional: nothing waits on it.
Object.assign(PROMO, { cake: [990, 1020], cakeAt: '5-tea-3' });
function promoCakeTick(now) {
  const W = SHIP.works, od = W && (W.ms.find(x => x[0] === 'officer') || [])[1]; if (!od || promoDone('cake2')) return;
  const d = worksDay(now), m = now - (d - 1) * 1440; if (d > od || (d === od && m >= PROMO.cake[1])) { W.done.push('cake2'); return; }
  if (d < od || m < PROMO.cake[0]) return;
  if (!W.cake) { W.cake = 1; if (typeof crewScene === 'function') try { crewScene('brennan', { mode: 'wait', to: PROMO.cakeAt, until: (d - 1) * 1440 + PROMO.cake[1], hold: 'tray' }); } catch (e) { /* no scene */ }
    try { toast('Chef Auda Brennan', worksText('promo.cake.toast', 'There\'s cake at the Works tea corner. Your cake, Officer.')); } catch (e) { /* no UI */ } }
  try { const a = DECK_CREW.find(x => x.p && x.p.id === 'brennan'), p = player.obj.position;
    if (a && Math.hypot(a.x - p.x, a.z - p.z) < 3) { W.done.push('cake2'); worksSayAll('brennan', worksVoice('brennan', 'promo.cake') || ['Lemon, because Calder said you liked it. Don\'t tell her I asked.']); } } catch (e) { /* not in play */ }
}
WORK_TICKS.push((now, skip) => { if (!skip) promoCakeTick(now); });
// Part 3, the move to 4-23 (0.44.20): on the promotion's day at 17:00 (up to 30 minutes later if you're mid-job) Calder,
// or Commander Vance if she's off, walks you from wherever you are to cabin 4-23 at the quiet end of the officers' corridor
// (worksEscort 'lead' to Deck 4's spare W), talking about officers' ways as you go (promo.walk.*). It's yours when you get
// there, or at 17:30 at the latest whatever happens (her lines by Mail if you're asleep or away): SHIP.works.home =
// '4-23', done 'move2', simNote('moved', { home }) (Tomas and Pell with your box at the door, and his goodbye: the sim engineer's, on
// simNote('moveStart')). From then the cabin's door opens for you
// (worksHomeOpen, asked by section 14's doorOpenFor); your bed, wardrobe, door plate and things follow SHIP.works.home
// (the sim engineer's playerBed(), the player engineer's wardrobe, the deck architect's plate and shelf).
Object.assign(PROMO, { home: '4-23', homeRoom: { deck: 4, room: 'W' }, moveWait: 30, moveBy: 1050 });
const worksHome = () => (SHIP.works && SHIP.works.home !== 'bunk' && SHIP.works.home) || null;   // your cabin's number, or null in the bunk room
function worksHomeOpen(deck, room) {                     // is this your own cabin? (section 14's doorOpenFor)
  const W = SHIP.works; if (!W) return false;
  const walking = W.mv && !promoDone('move2');           // on the walk there: open as you arrive
  return (W.home === PROMO.home || walking) && deck === PROMO.homeRoom.deck && room === PROMO.homeRoom.room;
}
function promoMoveBy() {                                 // who walks you: Calder, or Vance on her day off
  const d = worksDay(shipNow()); try { return occOnShift('calder', d) ? 'calder' : 'vance'; } catch (e) { return 'calder'; }
}
function promoMoveTick(now) {
  const W = SHIP.works; if (!W || W.tier < 2 || promoDone('move2')) return;
  const od = (W.ms.find(x => x[0] === 'officer') || [])[1]; if (!od) return;
  const d = worksDay(now), m = now - (d - 1) * 1440;
  if (d > od || m >= PROMO.moveBy) { promoMoved(Math.min(now, (od - 1) * 1440 + PROMO.moveBy), W.mv ? 'late' : 'mail'); return; }   // never missed: by 17:30 it's done (a skip past it: at 17:30)
  if (d < od || m < DAY_SHIFT[1]) return;
  if (!W.mv) {
    if (myJob() && m < DAY_SHIFT[1] + PROMO.moveWait) return;   // mid-job: she waits a while
    W.mv = { by: promoMoveBy(), at: Math.floor(now), s: [] };
    if (!promoInBay()) promoWalkSay('promo.fetch.move', 'There you are. Come on: your cabin.');
    promoWalkSay('promo.walk.start', 'Right, Officer. Your cabin. Follow me.');
    simNote('moveStart', { by: W.mv.by });   // the sim engineer's box carry (Tomas and Pell at 4-23's door)
    if (typeof setGoal === 'function') setGoal({ deck: PROMO.homeRoom.deck, room: PROMO.homeRoom.room, label: 'Your cabin, ' + PROMO.home });
  }
  try { const rm = roomAt(...player.here()), n = deckDef.num, M = PROMO.homeRoom, bed = typeof PLACE_OF !== 'undefined' && PLACE_OF.get(PROMO.home), [c, r] = player.here();   // her lines along the way (W2's promo.walk.*)
    if (rm === '@') promoWalkSay('promo.walk.lift', 'Officers\' corridor\'s on Four, the far side from the bunks.');
    if (n === M.deck && rm !== M.room && ROOMS[rm] && ROOMS[rm].hall) promoWalkSay('promo.walk.corridor', 'Quiet hours after eleven up here. People knock; they don\'t walk in.');
    if (n === M.deck && bed && Math.hypot(c - bed.at[0], r - bed.at[1]) < 5) promoWalkSay('promo.walk.door', 'Your door. Your name\'s on it.');
    if (n === M.deck && rm === M.room) { promoWalkSay('promo.walk.inside', 'And when someone says "come over", they mean it. Goodnight, Officer.'); promoMoved(now, 'walked'); } } catch (e) { /* not in play */ }
}
function promoWalkSay(flagKey, fallback) {               // each of her walk lines once (her VOICE lines under that flag, else the stand-in)
  const W = SHIP.works, m = W && W.mv; if (!m || m.s.includes(flagKey)) return; m.s.push(flagKey);
  worksSayAll(m.by, worksVoice(m.by, flagKey) || (flagKey === 'promo.walk.start' && worksVoice(m.by, 'promo.walk')) || [flagKey === 'promo.walk.start' ? worksText('promo.walk', fallback) : fallback]);   // (the writer's one-flag set reads too)
}
function promoMoved(now, how) {                          // 4-23 is yours
  const W = SHIP.works; if (!W || promoDone('move2')) return false;
  W.home = PROMO.home; W.done.push('move2'); const by = (W.mv && W.mv.by) || promoMoveBy(); delete W.mv;
  if (how !== 'walked' && typeof mailSend === 'function') { const t = worksText('mail.promo.move', worksText('promo.move.mail', 'Your cabin | Cabin 4-23 is yours from tonight: your things are in, your name\'s on the door. Officers\' corridor, the quiet end. — C.')), i = t.indexOf(' | ');
    mailSend({ at: now, from: worksName(by), subject: i > 0 ? t.slice(0, i) : 'Your cabin', body: i > 0 ? t.slice(i + 3) : t }); }
  simNote('moved', { home: W.home, how, t: now });
  return true;
}
function promoMoveEscort(p, t) {                         // worksEscort's 24p part: the walk to your cabin
  const W = SHIP.works; return W && W.mv && !promoDone('move2') && p.id === W.mv.by ? { mode: 'lead', to: { deck: PROMO.homeRoom.deck, room: PROMO.homeRoom.room } } : null;
}
WORK_TICKS.push((now, skip) => promoMoveTick(now));
// Part 4, the officer ceremony (0.44.21): the day after your promotion, Mail from the Captain's office at 08:00, and at
// 17:15 in Deck 1's observation room (OCCASIONS.promoCeremony, booked that morning) the Captain reads your commission,
// pins your Officer's insignia (your collar shows a second pip: the character kit's rank pips, no new mesh), a
// handshake, one line from you, the Captain's tea. Guests (promoGuests: the sim engineer walks them there 17:10-17:40):
// the Captain, Vance, Calder, Torres, and up to three of your closest friends (relTier 2+, highest first; schedU key
// 852 on a tie). Grubby? The stand-in has Calder's look; nothing else changes. Not there by 17:30: Calder comes to find
// you and walks you up (worksEscort 'lead'; the window runs on to 18:30); never missed: by 19:00 the commission comes by
// Mail. Then: ms ['commissioned', day], done 'ceremony2', the framed commission on your shelf (section 20's keepsakes,
// from the Captain), the Record's line, simNote('commissioned', { day }).
Object.assign(PROMO, { cerAt: 1035, cerLen: 25, cerSeek: 1050, cerLate: 1110, cerBy: 1140, cerMailAt: 480, guests: ['marrow', 'vance', 'calder', 'torres-zeke'], friends: 3 });
OCCASIONS.promoCeremony = { title: 'Your commission', kind: 'meeting', by: 'marrow', with: ['vance', 'calder', 'torres-zeke'], deck: 1, room: 'O', at: PROMO.cerAt, len: PROMO.cerLen, script: 'promo.ceremony', due: () => false, mail: null };
const promoCerDay = () => { const W = SHIP.works, od = W && (W.ms.find(x => x[0] === 'officer') || [])[1]; return od ? od + 1 : null; };
function promoGuests(d = promoCerDay()) {                // who stands with you: the four, and up to three friends
  if (!d) return [];
  let fr = []; try { fr = (typeof SOC !== 'undefined' && typeof socInit === 'function' ? (socInit(), SOC.crew) : []).filter(p => !PROMO.guests.includes(p.id) && relTier(p.id) >= 2 && (typeof socAboard !== 'function' || socAboard(p)))
    .sort((a, b) => relTier(b.id) - relTier(a.id) || schedU(machSeed(a.id), d, 852) - schedU(machSeed(b.id), d, 852) || (a.id < b.id ? -1 : 1)).slice(0, PROMO.friends).map(p => p.id); } catch (e) { fr = []; }
  return PROMO.guests.concat(fr);
}
function promoCerScript() {                              // the writer's ceremony, or a stand-in; our hooks on it
  if (!MEETING_SCRIPTS['promo.ceremony']) MEETING_SCRIPTS['promo.ceremony'] = { title: 'Your commission', from: 'Captain Odile Marrow', stub: true,
    gist: 'Your commission was read in the observation room, and your Officer\'s insignia is on your collar. It\'s framed on your shelf.',
    lines: [
      { who: 'vance', text: 'Attention, please. The Captain.' },
      { who: 'marrow', text: c => 'By the authority of the Concord Service, ' + c.you + ' is commissioned an Officer of the CSV Wren, Works Department.', pose: 'gesture' },
      { who: 'calder', text: 'Shoulders back.' },
      { who: 'marrow', text: 'Your insignia. Hold still.', pin: true },
      { choice: [
        { text: 'Thank you, Captain. I\'m proud to serve on the Wren.', reply: { who: 'marrow', text: 'And the Wren is glad of you.' } },
        { text: 'I\'ll do my best.', reply: { who: 'marrow', text: 'That\'s all any of us can do. It\'s usually enough.' } },
        { text: '(A firm handshake.)', reply: { who: 'marrow', text: 'A good grip. Calder said you had one.' } },
      ] },
      { who: 'marrow', text: 'Tea, everyone. My own blend; be polite about it.' },
    ] };
  const sc = MEETING_SCRIPTS['promo.ceremony'];
  if (!sc.promoHooked) { const pick = sc.onPick, end = sc.onEnd; sc.promoHooked = true;
    sc.onPick = (k, c) => { promoCommission(shipNow(), 'met'); if (pick) pick(k, c); };   // the reply comes after the pin
    sc.onEnd = finished => { if (end) end(finished); promoCommission(shipNow(), 'met'); }; }
  return sc;
}
if (SHIP.occasions.some(r => r.id === 'promoCeremony')) promoCerScript();
function promoCommission(now, how) {                     // commissioned: once
  const W = SHIP.works; if (!W || W.tier < 2 || promoDone('ceremony2')) return false;
  const d = worksDay(now), r = SHIP.occasions.find(x => x.id === 'promoCeremony' && x.status === 'asked'); if (r) r.met = true;
  W.done.push('ceremony2'); if (!W.ms.some(x => x[0] === 'commissioned')) W.ms.push(['commissioned', d]);
  if (typeof giftKeepsake === 'function') try { giftKeepsake({ id: 'marrow' }, worksText('works.keepsake.commission', worksText('promo.keepsake', 'your framed commission'))); } catch (e) { /* no social */ }
  if (how === 'mail' && typeof mailSend === 'function') { const t = worksText('mail.promo.ceremony', worksText('promo.ceremony.mail', 'Your commission | We missed you in the observation room. Your commission is signed all the same, and framed on your shelf. Congratulations, Officer. — O. Marrow')), i = t.indexOf(' | ');
    mailSend({ at: now, from: 'Captain Odile Marrow', subject: i > 0 ? t.slice(0, i) : 'Your commission', body: i > 0 ? t.slice(i + 3) : t }); }
  promoPip();
  simNote('commissioned', { day: d, how });
  return true;
}
function promoPip() {                                    // your collar: one pip more once commissioned (the kit's rank pips: makeCharacter's s.rank)
  const want = promoDone('ceremony2') ? 1 : 0;
  try { if (typeof player === 'undefined' || !player || (PLAYER_SPEC.rank || 0) === want) return false;
    PLAYER_SPEC.rank = player.spec.rank = want; const w = player, old = w.rig;
    w.obj.remove(old.root); old.root.traverse(o => { if (o.isMesh) o.geometry.dispose(); });
    w.rig = makeCharacter(w.spec); w.obj.add(w.rig.root); w.rig.root.traverse(o => { o.userData.walker = w; });
    w.propMeshes = []; w.propKey = ''; w.bodyProps = null;
    const grubby = typeof uniformState === 'function' && uniformState() === 'grubby' && !PLAYER_SPEC.kit;
    if (typeof playerUniformTint === 'function' && (grubby || UNIFORM_MAT)) playerUniformTint(grubby ? 1 : 0);
    return true; } catch (e) { return false; }
}
function promoCerTick(now) {
  const d0 = promoCerDay(); if (!d0 || promoDone('ceremony2')) return;
  const d = worksDay(now), m = now - (d - 1) * 1440;
  let r = SHIP.occasions.find(x => x.id === 'promoCeremony');
  if (d > d0 || (d === d0 && m >= PROMO.cerBy)) { promoCommission(Math.min(now, (d0 - 1) * 1440 + PROMO.cerBy), 'mail'); return; }
  if (d < d0) return;
  if (!r && m >= PROMO.cerMailAt - 60) { promoCerScript(); OCCASIONS.promoCeremony.with = promoGuests(d).filter(id => id !== 'marrow'); r = occasionAdd('promoCeremony', (d - 1) * 1440 + PROMO.cerAt, true, PROMO.cerLen); }
  if (!r) return;
  const f = r.f || (r.f = {});
  if (m >= PROMO.cerMailAt && !f.mail && typeof mailSend === 'function') { f.mail = 1; const t = worksText('promo.ceremony.invite', 'Your commissioning | This evening at 17:15, the observation room, Deck 1. A clean uniform, please. — The Captain\'s office'), i = t.indexOf(' | ');
    mailSend({ at: Math.max(now, (d - 1) * 1440 + PROMO.cerMailAt), from: 'The Captain\'s office', subject: i > 0 ? t.slice(0, i) : 'Your commissioning', body: i > 0 ? t.slice(i + 3) : t }); }
  try { if (!f.gr && r.status === 'asked' && now >= r.at - 10 && deckDef.num === r.deck && roomAt(...player.here()) === r.room && typeof uniformState === 'function' && uniformState() === 'grubby') {
    f.gr = 1; worksSayAll('calder', worksVoice('calder', 'promo.grubby') || ['(Calder looks at your uniform, then at you, and says nothing.)']); } } catch (e) { /* not in play */ }   // a clean uniform matters (M2): her look, nothing else
  if (m >= PROMO.cerSeek && !f.seek && !r.met && r.status === 'asked') { f.seek = now; r.len = PROMO.cerLate - PROMO.cerAt + 20;   // 17:30: Calder walks you up; the room waits for you
    worksSayAll('calder', worksVoice('calder', 'promo.fetch.ceremony') || ['There you are. The Captain\'s waiting. Come on.']);
    if (typeof setGoal === 'function') setGoal({ deck: 1, room: 'O', label: 'Your commission, the observation room' }); }
}
function promoCerEscort(p, t) {                          // worksEscort's 24p part: Calder walking you up to the ceremony
  const r = SHIP.occasions.find(x => x.id === 'promoCeremony' && x.status === 'asked');
  return r && r.f && r.f.seek && !r.met && p.id === 'calder' && t < r.at + r.len ? { mode: 'lead', to: { deck: 1, room: 'O' } } : null;
}
WORK_TICKS.push((now, skip) => { promoCerTick(now); if (!skip && promoDone('ceremony2')) promoPip(); });


