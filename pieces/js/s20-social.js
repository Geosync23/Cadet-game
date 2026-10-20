// =====================================================================
// 20. SOCIAL
// The crew as people you know, and as people who know each other (plans/pillar3-plan.md, Part 3 and "How news
// spreads"). On paper so far (0.36.0): nothing here draws anything or calls R().
//   SHIP.rel[crewId] = { pts, tier, met, lastTalk, known: [] }   you and each crew member, made on first use (saved)
//   relAdd(crewId, why, pts) -> the tier after; relTier(crewId) -> 0..4 (REL_NAMES); points never drop
//   SHIP.aff: Int8Array, one number per pair of crew (pairIdx, i < j in ROSTER order), -100..100; affinity(a, b)
//   NEWS: [{ id, about, lines, weight, seed, born, kind, event, life }]; SHIP.knows[newsId] = Set of crew ids
//   newsAdd(item)            a piece of news (the events engineer's too): its seed know it at once; [] if it's known
//   newsKnownBy(p, t)        -> the news that person knows at minute t, the freshest and weightiest first
//   playerHeard(newsId, from)  you heard it: SHIP.heard (the Ship app's feed); told first by a crew member, +1
//   socialTo(t)              run the ship's social hours up to minute t (the main loop, every time jump, social_check)
//   chatLine(p, t), chatOpen(p), chatClose()   the chat card when you tap someone (0.36.1; section 10's tapCrew)
// Hour by hour, from who is where (planWhere, section 14, at the half hour): people awake in the same room spend
// time together, though in a big room each hour only a few of them do. Affinity drifts with that time (most pairs
// slowly friendlier, pairs with clashing traits the other way) and news passes on (friends more readily). Gossip is
// born from the ship: a machine going faulty (section 17's hourly record), habit changes (habitWeek, 09:00 that
// day), birthdays and the day's ship traditions (07:00, section 18), and pairs becoming friends or falling out.
// Every choice is schedU (k 600-639), so the same ship gives the same social life however it's played (one big jump
// or hour by hour); the hours already run are kept in the save (SHIP.social.hour), and a clock earlier than that
// (New game) starts afresh. Everything waits for its first use: ROSTER (section 9) comes later in the file.
// =====================================================================
const REL_TIERS = [0, 10, 30, 60, 100], REL_NAMES = ['stranger', 'acquaintance', 'colleague', 'friend', 'close friend'];
const REL_PTS = { work: 6, meal: 3, chat: 2, favour: 8, news: 1, appt: 3, birthday: 3, hello: 1, talk: 1, reply: [1, 2] };   // hello: Say hello; talk: each TALK_EVERY minutes of Talk a while; reply: its choice, [another, the one that suits them] (0.36.82)   // the plan's starting numbers, to tune
// traits that rub each other up the wrong way: anyone with one from the first list and one from the second
const SOC_CLASH = [[['meticulous', 'precise', 'exacting', 'tidy', 'organised', 'formal'], ['messy', 'easygoing', 'forgetful', 'absent-minded', 'dreamy', 'unhurried', 'playful']],
  [['blunt', 'sarcastic', 'gruff'], ['nervous', 'shy', 'gentle']], [['competitive'], ['competitive']], [['chatty', 'sociable'], ['private', 'quiet']]];
const SOC_SYMPTOM = { scrubber: 'rattling', fan: 'rattling', airplant: 'wheezing', lights: 'flickering', junction: 'buzzing', relay: 'buzzing', databus: 'dropping out',
  washer: 'leaving the laundry damp', oven: 'running cold', range: 'running cold', chiller: 'struggling to keep cold', lift: 'juddering', heater: 'clanking',
  heatpump: 'clanking', recycler: 'gurgling', filter: 'gurgling', pump: 'humming', extractor: 'roaring', irrigation: 'sputtering', uv: 'flickering' };
const NEWS = [];
let SOC = null, SOC_MIN = -1;
SHIP.rel = {}; SHIP.aff = null; SHIP.knows = {}; SHIP.heard = []; SHIP.social = { hour: 0, fault: {}, pairs: {}, mail: [], feuds: {}, courtesy: {}, cues: [] };
const socRoom = p => { const b = String(p.bed).split('-'); return b.length > 2 ? b.slice(0, 2).join('-') : b.join('-'); };   // '4-B1-2' -> '4-B1'; a cabin is its own
const socHash = s => { let h = 2166136261; for (let i = 0; i < s.length; i++) h = Math.imul(h ^ s.charCodeAt(i), 16777619); return h | 0; };
const pairIdx = (i, j) => { if (i > j) [i, j] = [j, i]; return i * (2 * SOC.n - i - 1) / 2 + j - i - 1; };
const pairSeed = (i, j) => (SOC.crew[i].seed * 31 + SOC.crew[j].seed) | 0;
const socPick = (a, n, seed, h, k) => a.map(x => [schedU(seed ^ socHash(x.id || x), h, k), x]).sort((x, y) => x[0] - y[0]).slice(0, n).map(x => x[1]);
function socClash(p, q) {
  const a = p.traits || [], b = q.traits || [], has = (t, l) => t.some(x => l.includes(x));
  return SOC_CLASH.some(([x, y]) => (has(a, x) && has(b, y)) || (has(a, y) && has(b, x)));
}
function affStart(p, q) {                                // where a pair starts: work, bunk, habits and traits in common
  if (p.partner === q.id || q.partner === p.id) return 90;   // a couple (B6: the roster's partners, together from the start)
  let v = 0;
  if (p.dept === q.dept) v += 12;
  if (socRoom(p) === socRoom(q)) v += 18;
  if (p.shift === q.shift) v += 3;
  for (const h of p.habits || []) if ((q.habits || []).includes(h)) v += 5;
  for (const t of p.traits || []) if ((q.traits || []).includes(t) && t !== 'competitive') v += 4;
  if (socClash(p, q)) v -= 24;                           // 0.36.32: was 12 (the deep plan: a handful of rivalries in two weeks)
  v += Math.round(16 * (schedU((p.seed * 31 + q.seed) | 0, 0, 600) - .5));
  return Math.max(-100, Math.min(100, v));
}
function socReset(hour) {
  const { crew, n } = SOC, a = new Int8Array(n * (n - 1) / 2);
  for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) a[pairIdx(i, j)] = affStart(crew[i], crew[j]);
  SHIP.aff = a; SHIP.rel = {}; SHIP.knows = {}; SHIP.heard = []; NEWS.length = 0; SHIP.mem = {}; SHIP.rep = null;
  SHIP.social = { hour, fault: {}, pairs: {}, mail: [], feuds: {}, courtesy: {}, cues: [], bonds: {}, affWeek: null, stories: {} };
}
// the save: social = { ids, hour, aff (base64), news: [{ ...item, k: hex bits of who knows }], heard, fault, pairs,
// rel: { id: [pts, met, lastTalk, known, chatDay, mealDay, workDay, favDay, seekDay, arc, arcDay, showDay, giftWeek, ..., talkDay] } }, mail (story Mail to come), cues, mentor,
// given, keepsakes, memKeys and mem (Pillar 4). A save made with a different crew list keeps everything keyed by id and moves affinity across by id (idl)
const bitsOf = set => { const b = new Uint8Array(Math.ceil(SOC.n / 8)); for (const id of set) { const i = SOC.idx.get(id); if (i !== undefined) b[i >> 3] |= 1 << (i & 7); } return [...b].map(x => x.toString(16).padStart(2, '0')).join(''); };
const setOf = hex => { const s = new Set(); for (let i = 0; i < SOC.n; i++) if (parseInt(hex.substr((i >> 3) * 2, 2), 16) >> (i & 7) & 1) s.add(SOC.crew[i].id); return s; };
const setOfIds = (hex, ids) => { const s = new Set(); ids.forEach((id, i) => { if (SOC.idx.has(id) && parseInt(hex.substr((i >> 3) * 2, 2), 16) >> (i & 7) & 1) s.add(id); }); return s; };
// 20c's bonds packed for the save (0.36.67): [a, b, kind, since, peak, seen(, other fields)] by crew index, kinds by
// SOC_BOND_KINDS; about a third of the size of the 'a:b' object form, which older saves have and still load
function bondsPack(B) {
  if (typeof storyBondsPack === 'function') { const v = storyBondsPack(B); if (v) return v; }   // 20c's compact form
  const l = []; for (const k in B || {}) { const [a, b] = k.split(':'), x = B[k], i = SOC.idx.get(a), j = SOC.idx.get(b), ki = SOC_BOND_KINDS.indexOf(x.kind);
    if (i === undefined || j === undefined || ki < 0) continue;
    const { kind, since, peak, seen, ...rest } = x, r = [i, j, ki, since ?? null, peak ?? null, seen ?? null]; if (Object.keys(rest).length) r.push(rest); l.push(r); }
  return { v: 1, l };
}
function bondsUnpack(o, ids) {                            // ids: the save's crew list (idl)
  if (!o || typeof o !== 'object') return {};
  if (o.v === 2 && typeof storyBondsUnpack === 'function') return storyBondsUnpack(o, ids);   // 20c's compact form
  if (o.v !== 1 || !Array.isArray(o.l)) return JSON.parse(JSON.stringify(o));   // the older form
  const B = {}; for (const r of o.l) { if (!Array.isArray(r)) continue; const a = ids[r[0]], b = ids[r[1]], kind = SOC_BOND_KINDS[r[2]]; if (!a || !b || !kind || !SOC.idx.has(a) || !SOC.idx.has(b)) continue;
    const x = { kind }; if (r[3] != null) x.since = r[3]; if (r[4] != null) x.peak = r[4]; if (r[5] != null) x.seen = r[5]; if (r[6] && typeof r[6] === 'object') Object.assign(x, r[6]); B[a + ':' + b] = x; }
  return B;
}
// what you've heard, for the save (0.36.75): everything about news still going round (it decides what crew still tell you,
// so picks never change), and the HEARD_FEED latest of the rest for the Ship app's feed; in heard order, as short arrays
const HEARD_FEED = 12;
// what you know about someone, for the save (0.36.76, by text hash since 0.36.78): their roster lines as '#xxxx' (a hash), the rest as written
const knownLines = p => p ? (p.about || []).map(x => x && x.text).concat(p.life || []).filter(x => typeof x === 'string') : [];
const knownTag = x => '#' + ((socHash(x) >>> 0) % 1679616).toString(36).padStart(4, '0');   // four characters of a hash of the fact's text: a roster edit can't show a fact you weren't told
function knownPack(id, K) { const L = knownLines(SOC.idx.has(id) && SOC.crew[SOC.idx.get(id)]), T = L.map(knownTag);
  return K.map(k => { const i = L.indexOf(k); return i >= 0 && T.indexOf(T[i]) === T.lastIndexOf(T[i]) ? T[i] : k; }); }   // two of their lines with the same tag: kept as written
function knownUnpack(id, K) { const p = SOC.idx.has(id) && SOC.crew[SOC.idx.get(id)], L = knownLines(p), H = new Map(L.map(x => [knownTag(x), x]));
  return K.map(k => { if (typeof k !== 'string' || k[0] !== '#') return k; if (/^#[0-9a-z]{4}$/.test(k)) return H.get(k) || null;   // a line the roster no longer has is forgotten
    const m = /^#([al])(\d+)$/.exec(k); if (!m) return k; const x = m[1] === 'a' ? p && p.about && p.about[+m[2]] && p.about[+m[2]].text : p && p.life && p.life[+m[2]]; return x || null; }).filter(k => typeof k === 'string'); }   // '#a3' / '#l1': 0.36.76's saves
const PAIRS_MAX = 300, MOVED_MAX = 24;                    // the pair news already told, and who moved on, at most (oldest go first; 04:00 each day)
function socTrim() {
  const P = SHIP.social.pairs, ks = Object.keys(P); for (let k = 0; k < ks.length - PAIRS_MAX; k++) delete P[ks[k]];
  const M = SHIP.social.moved; if (M && M.length > MOVED_MAX) M.splice(0, M.length - MOVED_MAX);
}
function heardKept() {
  const live = new Set(NEWS.map(x => x.id)), H = SHIP.heard.slice(-60), old = H.filter(h => !live.has(h.id)).slice(-HEARD_FEED);
  const keep = new Set(old); return H.filter(h => live.has(h.id) || keep.has(h)).map(h => live.has(h.id) ? [h.id, h.from, h.at] : [h.id, h.from, h.at, h.line]);   // [id, from, at(, line)]: a live item's line comes back from NEWS on load
}
// news items and cues as short rows for the save (0.36.81): the known fields by position, anything else in a trailing object
const NEWS_F = ['id', 'about', 'lines', 'weight', 'born', 'kind', 'event', 'life'], CUE_F = ['key', 'at', 'until', 'you', 'deck', 'who', 'dept', 'room'];
const rowOf = (x, F) => { const r = F.map(f => x[f] ?? null), rest = Object.fromEntries(Object.entries(x).filter(([f]) => !F.includes(f))); while (r.length && r[r.length - 1] === null) r.pop(); if (Object.keys(rest).length) { while (r.length < F.length) r.push(null); r.push(rest); } return r; };
const newsSaved = ({ seed, ...x }) => rowOf({ ...x, k: bitsOf(SHIP.knows[x.id] || []) }, NEWS_F.concat('k'));   // who first knew it only matters when it's born
const newsRow = r => { const o = { id: r[0], about: r[1] ?? null, lines: r[2], weight: r[3], seed: [], born: r[4], kind: r[5], event: r[6] ?? null, life: r[7], k: r[8] }; return r[9] && typeof r[9] === 'object' ? { ...o, ...r[9] } : o; };
const cueRow = c => rowOf({ ...c, you: c.you ? 1 : null }, CUE_F);
const cueObj = r => ({ key: r[0], at: r[1], until: r[2], you: !!r[3], deck: r[4] ?? null, who: r[5] ?? null, dept: r[6] ?? null, room: r[7] ?? null, ...(r[8] && typeof r[8] === 'object' ? r[8] : {}) });
const cueSaved = c => Object.fromEntries(Object.entries(c).filter(([, v]) => v !== null && v !== false && v !== undefined));   // empty fields left off (socLoad puts them back)
function pairsLoad(E, old) {                             // crew positions moved across by id when the save's crew list differs (none known: dropped)
  if (!old) return Object.fromEntries(E);
  const P = {}; for (const [k, v] of E) { const [a, b] = k.split('-').map(Number), x = SOC.idx.get(old[a]), y = SOC.idx.get(old[b]); if (x !== undefined && y !== undefined) P[Math.min(x, y) + '-' + Math.max(x, y)] = v; }
  return P;
}
const pairsSaved = P => Object.entries(P).map(([k, v]) => k + v).join(',');   // '12-45f,3-9r': the pair news already told
// crew affinity for the save (0.36.81): 'd:' + base64 of each pair's change from where it started (affStart, from the
// roster alone), zigzag varints, a run of unchanged pairs as 0 then its length; most pairs never move far, so about a
// third of the raw byte-a-pair form, which older saves have and still load
function affStarts(P) { const n = P.length, v = new Int16Array(n * (n - 1) / 2); for (let i = 0, k = 0; i < n; i++) for (let j = i + 1; j < n; j++, k++) v[k] = P[i] && P[j] ? affStart(P[i], P[j]) : 0; return v; }
let AFF_START = null;                                     // today's crew's starting values, made once ({ soc, v })
function affPack() {
  const a = SHIP.aff, st = AFF_START && AFF_START.soc === SOC ? AFF_START.v : (AFF_START = { soc: SOC, v: affStarts(SOC.crew) }).v, out = [];
  const vi = x => { while (x > 127) { out.push(x & 127 | 128); x >>>= 7; } out.push(x); };
  for (let k = 0; k < a.length;) {
    const d = a[k] - st[k];
    if (!d) { let r = 0; while (k < a.length && a[k] === st[k]) { r++; k++; } out.push(0); vi(r); }
    else { vi(d > 0 ? 2 * d : -2 * d - 1); k++; }        // zigzag, never 0 (0 starts a run)
  }
  let bin = ''; for (const x of out) bin += String.fromCharCode(x); return 'd:' + btoa(bin);
}
function affVals(str, ids) {                              // the saved affinity as values in pair order for that crew list (NaN: unknown), or null
  if (typeof str !== 'string') return null;
  if (!str.startsWith('d:')) { const bin = atob(str), v = new Array(bin.length); for (let i = 0; i < bin.length; i++) v[i] = bin.charCodeAt(i) << 24 >> 24; return v; }   // the raw form (before 0.36.81)
  if (!ids) return null;
  const P = ids.map(id => SOC.idx.has(id) ? SOC.crew[SOC.idx.get(id)] : null), st = affStarts(P), bin = atob(str.slice(2)), v = new Array(st.length);
  let p = 0; const vi = () => { let x = 0, sh = 0, b; do { b = bin.charCodeAt(p++); x |= (b & 127) << sh; sh += 7; } while (b & 128); return x; };
  let k = 0;
  while (k < st.length && p < bin.length) {
    const z = vi();
    if (!z) { const r = vi(); if (k + r > st.length) return null; for (let q = 0; q < r; q++, k++) v[k] = st[k]; }
    else { v[k] = st[k] + (z & 1 ? -(z + 1) / 2 : z / 2); k++; }
  }
  if (k !== st.length || p !== bin.length) return null;   // cut short or too long: refused, like the raw form's wrong length
  const gone = P.some(x => !x); for (let k = 0; k < v.length; k++) { if (v[k] === undefined) v[k] = NaN; else if (gone) { const i = pairOf(k, P.length); if (!P[i[0]] || !P[i[1]]) v[k] = NaN; } }
  return v;
}
function pairOf(k, n) { let i = 0; while (k >= n - 1 - i) { k -= n - 1 - i; i++; } return [i, i + 1 + k]; }   // the k-th pair of n people, in pair order
function socSave() {
  socInit();
  const rel = {}; for (const id in SHIP.rel) { const r = SHIP.rel[id]; rel[id] = [r.pts, r.met, r.lastTalk, knownPack(id, r.known), r.chatDay || 0, r.mealDay || 0, r.workDay || 0, r.favDay || 0, r.seekDay || 0, r.arc || 0, r.arcDay || 0, r.showDay || 0, r.giftWeek || 0, r.inviteDay || 0, r.visitDay || 0, r.bye || 0, r.hostDay || 0, r.talkDay === SHIP.time.day ? r.talkDay : 0 /* talkDay only matters today (reviewer 0607) */]; const x = rel[id]; while (x.length > 4 && !x[x.length - 1]) x.pop(); }   // trailing zeros left off (they load as 0)
  return { ids: socHash(SOC.ids), idl: SOC.ids, hour: SHIP.social.hour, aff: affPack(), news: NEWS.map(newsSaved),
           heard: heardKept(), fault: { ...SHIP.social.fault }, pairs: pairsSaved(SHIP.social.pairs), mail: SHIP.social.mail.map(x => ({ ...x })), feuds: JSON.parse(JSON.stringify(SHIP.social.feuds)), courtesy: { ...SHIP.social.courtesy }, cues: SHIP.social.cues.map(cueRow), mentor: SHIP.social.mentor || null, given: (SHIP.social.given || []).map(x => ({ ...x })), keepsakes: (SHIP.social.keepsakes || []).map(x => ({ ...x })), rep: SHIP.rep ? JSON.parse(JSON.stringify(SHIP.rep)) : null, invites: (SHIP.social.invites || []).map(x => ({ ...x })), notes: (SHIP.social.notes || []).map(x => ({ ...x })), visitDay: SHIP.social.visitDay || 0, moved: (SHIP.social.moved || []).map(x => ({ ...x, mem: x.mem.slice() })), bonds: bondsPack(SHIP.social.bonds), affWeek: typeof SHIP.social.affWeek === 'string' ? SHIP.social.affWeek : null, stories: JSON.parse(JSON.stringify(SHIP.social.stories || {})), noteq: JSON.parse(JSON.stringify(SHIP.social.noteq || [])), seekAsks: (SHIP.social.seekAsks || []).map(x => ({ id: x.id, from: x.from, until: x.until, why: x.why, done: !!x.done })), guide: SHIP.social.guide ? { ...SHIP.social.guide } : null, rel: Object.entries(rel).map(([id, r]) => [SOC.idx.get(id), ...r]), ...memSave() }   // rel: [[crew index, pts, met, ...]] (0.36.81; an object by id before);
}
function socLoad(s) {
  try {
    if (!s || !Number.isInteger(s.hour) || typeof s.aff !== 'string') return false;
    // a save made with a different crew list (the reserve arriving, the roster changing): everything keyed by id is kept;
    // pair affinity and who knows what are moved across by id when the save has its id list (idl), else start afresh
    const same = s.ids === socHash(SOC.ids), old = !same && typeof s.idl === 'string' ? s.idl.split(',') : null;
    const vals = affVals(s.aff, same ? SOC.crew.map(p => p.id) : old), a = new Int8Array(SOC.n * (SOC.n - 1) / 2);
    if (same) { if (!vals || vals.length !== a.length) return false; for (let i = 0; i < a.length; i++) a[i] = vals[i]; }
    else {
      for (let i = 0; i < SOC.n; i++) for (let j = i + 1; j < SOC.n; j++) a[pairIdx(i, j)] = affStart(SOC.crew[i], SOC.crew[j]);
      if (old && vals && vals.length === old.length * (old.length - 1) / 2) for (let i = 0, k = 0; i < old.length; i++) for (let j = i + 1; j < old.length; j++, k++) {
        const x = SOC.idx.get(old[i]), y = SOC.idx.get(old[j]); if (x !== undefined && y !== undefined && Number.isFinite(vals[k])) a[pairIdx(x, y)] = vals[k];
      }
    }
    SHIP.aff = a; SHIP.social = { hour: s.hour, fault: { ...(s.fault || {}) }, pairs: pairsLoad(typeof s.pairs === 'string' ? s.pairs.split(',').filter(Boolean).map(x => [x.slice(0, -1), x.slice(-1)]) : Object.entries(s.pairs || {}), same ? null : old || []), mail: Array.isArray(s.mail) ? s.mail.filter(x => x && isFinite(x.at) && typeof x.body === 'string') : [], feuds: s.feuds && typeof s.feuds === 'object' ? JSON.parse(JSON.stringify(s.feuds)) : {}, courtesy: s.courtesy && typeof s.courtesy === 'object' ? { ...s.courtesy } : {}, cues: Array.isArray(s.cues) ? s.cues.map(x => Array.isArray(x) ? cueObj(x) : x).filter(x => x && typeof x.key === 'string' && isFinite(x.until)).map(x => ({ key: x.key, at: x.at, until: x.until, you: x.you ?? false, deck: x.deck ?? null, who: x.who ?? null, dept: x.dept ?? null, room: x.room ?? null })) : [], mentor: typeof s.mentor === 'string' && SOC.idx.has(s.mentor) ? s.mentor : null,
      given: Array.isArray(s.given) ? s.given.filter(x => x && typeof x.from === 'string').map(x => ({ ...x })) : [], keepsakes: Array.isArray(s.keepsakes) ? s.keepsakes.filter(x => x && typeof x.from === 'string').slice(0, 8).map(x => ({ ...x })) : [],
      invites: Array.isArray(s.invites) ? s.invites.filter(x => x && typeof x.from === 'string' && isFinite(x.day)).map(x => ({ ...x })) : [],
      notes: Array.isArray(s.notes) ? s.notes.filter(x => x && typeof x.from === 'string' && typeof x.text === 'string').map(x => ({ ...x })) : [], visitDay: s.visitDay | 0,
      moved: Array.isArray(s.moved) ? s.moved.filter(x => x && typeof x.id === 'string' && Array.isArray(x.mem)).map(x => ({ ...x, mem: x.mem.slice() })) : [],
      bonds: bondsUnpack(s.bonds, typeof s.idl === 'string' ? s.idl.split(',') : SOC.crew.map(p => p.id)), affWeek: typeof s.affWeek === 'string' && (typeof s.idl !== 'string' || s.idl === SOC.ids) ? s.affWeek : null, stories: s.stories && typeof s.stories === 'object' ? JSON.parse(JSON.stringify(s.stories)) : {},
      seekAsks: Array.isArray(s.seekAsks) ? s.seekAsks.filter(x => x && typeof x.id === 'string' && isFinite(x.from)).map(x => ({ ...x })) : [],
      guide: s.guide && typeof s.guide.id === 'string' && isFinite(s.guide.day) ? { ...s.guide } : null,
      noteq: Array.isArray(s.noteq) ? s.noteq.filter(x => Array.isArray(x) && isFinite(x[0]) && typeof x[1] === 'string').map(x => JSON.parse(JSON.stringify(x))) : [] };   // 20c's bonds, weekly snapshot and moment state ride here
    NEWS.length = 0; SHIP.knows = {};
    for (const x0 of Array.isArray(s.news) ? s.news : []) { const x = Array.isArray(x0) ? newsRow(x0) : x0; if (x && typeof x.id === 'string' && Array.isArray(x.lines) && typeof x.k === 'string' && (same || old)) {
      const { k, ...it } = x; if (!Array.isArray(it.seed)) it.seed = []; NEWS.push(it); SHIP.knows[it.id] = same ? setOf(k) : setOfIds(k, old);
    } }
    SHIP.heard = Array.isArray(s.heard) ? s.heard.map(h => Array.isArray(h) ? { id: h[0], from: h[1] ?? null, at: h[2], line: h.length > 3 ? h[3] : (NEWS.find(x => x.id === h[0]) || { lines: [null] }).lines[0] } : h).filter(h => h && typeof h.id === 'string').slice(-60) : [];   // arrays since 0.36.75, objects before
    SHIP.rel = {};
    const relIn = Array.isArray(s.rel) ? Object.fromEntries(s.rel.filter(x => Array.isArray(x)).map(([i, ...r]) => [(same || !old ? SOC.crew.map(p => p.id) : old)[i], r]).filter(([id]) => id)) : s.rel || {};
    for (const id in relIn) { const r = relIn[id]; if (SOC.idx.has(id) && Array.isArray(r) && isFinite(r[0])) SHIP.rel[id] = { pts: +r[0], tier: 0, met: r[1] ?? null, lastTalk: r[2] ?? null, known: Array.isArray(r[3]) ? knownUnpack(id, r[3]) : [], chatDay: r[4] | 0, mealDay: r[5] | 0, workDay: r[6] | 0, favDay: r[7] | 0, seekDay: r[8] | 0, arc: r[9] | 0, arcDay: r[10] | 0, showDay: r[11] | 0, giftWeek: r[12] | 0, inviteDay: r[13] | 0, visitDay: r[14] | 0, bye: r[15] | 0, hostDay: r[16] | 0, talkDay: r[17] | 0 }; }
    for (const id in SHIP.rel) SHIP.rel[id].tier = relTierOf(SHIP.rel[id].pts);
    memLoad(s);
    SHIP.rep = s.rep && typeof s.rep === 'object' && s.rep.dept && s.rep.ship ? JSON.parse(JSON.stringify(s.rep)) : null;
    if (SHIP.rep) for (const [k, v] of Object.entries({ cnt: {}, wk: {}, day: {}, streak: 0, bands: {}, notes: [], thanks: [] })) if (!(k in SHIP.rep)) SHIP.rep[k] = v;
    return true;
  } catch (e) { return false; }
}
function socInit() {
  if (SOC) return SOC;
  const crew = ROSTER.filter(p => !p.player).concat(typeof ROSTER_RESERVE !== 'undefined' && Array.isArray(ROSTER_RESERVE) ? ROSTER_RESERVE.filter(p => p && p.id && !p.player && !ROSTER.includes(p)) : []);   // the reserve too (A9): the save's shape never changes
  SOC = { crew, n: crew.length, idx: new Map(crew.map((p, i) => [p.id, i])), ids: crew.map(p => p.id).join(',') };
  if (!socLoad(SAVED && SAVED.social)) socReset(Math.floor(shipNow() / 60));
  return SOC;
}
SAVE_EXTRA.push(s => { s.social = socSave(); });

// ---- you and the crew ----
const relTierOf = pts => { let t = 0; while (t < 4 && pts >= REL_TIERS[t + 1]) t++; return t; };
function relGet(id) {                                   // made on first meeting; strangers start a little warmer where your name is known (reputation)
  socInit(); if (SHIP.rel[id]) return SHIP.rel[id];
  const p = SOC.idx.has(id) && SOC.crew[SOC.idx.get(id)], warm = p && SHIP.rep && REP_DEPTS_ALL.includes(p.dept) ? REP_WARM[repBand(p.dept)] : 0;   // only a standing you've earned
  return SHIP.rel[id] = { pts: warm, tier: 0, met: null, lastTalk: null, known: [] };
}
const relTier = id => (socInit(), SHIP.rel[id] ? SHIP.rel[id].tier : 0);
function relAdd(id, why, pts) {
  socInit(); if (!SOC.idx.has(id)) return -1;
  const r = relGet(id), now = Math.floor(shipNow());
  // friends of your friends warm to you a little faster
  if (pts > 0 && Object.keys(SHIP.rel).some(f => f !== id && SHIP.rel[f].tier >= 3 && affinity(f, id) >= 40)) pts *= 1.25;
  if (typeof relGain === 'function') pts = relGain(id, why, pts);   // openness (20c): guarded people warm slower, open ones faster
  r.pts = Math.max(REL_TIERS[r.tier], Math.round((r.pts + pts) * 100) / 100);   // never below the tier you've reached
  if (r.met === null) r.met = now;
  if (why !== 'news') r.lastTalk = now;
  const was = r.tier; r.tier = relTierOf(r.pts);
  if (r.tier > was && typeof deviceNotify === 'function') {   // a badge on the device's Crew app (section 19)
    const p = SOC.crew[SOC.idx.get(id)];
    deviceNotify({ app: 'crew', text: r.tier === 1 ? 'You and ' + shortName(p) + ' know each other now.' : 'You and ' + shortName(p) + ' are ' + REL_NAMES[r.tier] + 's now.', urgent: false });   // a badge only: the chat card says it in person
  }
  if (r.tier > was && typeof simNote === 'function') simNote('tierUp', { id, tier: r.tier });   // for the others on the bus (the Settling-in list, the device)
  return r.tier;
}
function affinity(a, b) {
  socInit(); const i = SOC.idx.get(a && a.id || a), j = SOC.idx.get(b && b.id || b);
  return i === undefined || j === undefined || i === j ? 0 : SHIP.aff[pairIdx(i, j)];
}
// what section 14 plans with (seating by friendship): pure, so a day planned early or again after a reload comes out
// the same. For now the pair's starting affinity (affStart: roster data and a seed only); d is kept for later
const AFF_PLAN = new Map();
function affinityPlan(a, b, d) {
  socInit(); const i = SOC.idx.get(a && a.id || a), j = SOC.idx.get(b && b.id || b);
  if (i === undefined || j === undefined || i === j) return 0;
  if (typeof affPlanWeek === 'function') { const v = affPlanWeek(i, j, d); if (v !== undefined) return v; }   // the weekly snapshot (20c)
  const k = pairIdx(i, j); if (!AFF_PLAN.has(k)) AFF_PLAN.set(k, affStart(SOC.crew[Math.min(i, j)], SOC.crew[Math.max(i, j)]));
  return AFF_PLAN.get(k);
}

// ---- the query API (0.36.20, Pillar 4: plans/social-deep-plan.md, Part 6) ----
// Pure: what the dialogue engine's line conditions read (section 22's lineFor). None of them changes anything.
//   mem(id, key)      -> their heaviest memory of you whose key is key or starts with key + '.', { key, day, w, told }, or null
//   warmth(id)        -> 'warm' (memories weighing 40+, or you talked in the last 3 days) or 'cold'
//   affBand(a, b)     -> 'rival' (-40 or less), 'friend' (60+) or 'neutral'
//   bondOf(id, kind)  -> the crewmate they have that bond with (an id), or null: friends, best, rivals, mentor, mentee,
//                        drifting, couple (SHIP.social.bonds, filled by 20c; 'couple' also reads the roster's partner)
//   moodOf(p)         -> 'low' (under 40), 'ok', 'high' (70+): crewMood now
//   beatOf(arcId)     -> how many beats of that story arc you've been told (arcBeat is "the next beat due")
//   knowsNews(p, id)  -> whether they know that news (an exact id, or a prefix ending before a ':')
//   repBand(dept)     -> 'new' / 'known' / 'well' / 'theirs': that department's standing with you (SHIP.rep, A6)
//   repShip(kind)     -> 'low' / 'ok' / 'high' for 'work', 'kindness', 'spirit'
//   aboard(p, d)      is section 14's (the sim engineer: guests now, crew coming and going later), not defined here
//   knownFor()        -> your tags ('reliable', 'kind', 'quiz regular', ...; the reputation step, 0.36.25)
//   memTold(id, key)  -> marks that memory told (the one state change here: lineFor calls it after a callback line)
//   cue(kind)         -> a ship note still talked about (SHIP.social.cues, from the bus), or null; kind matches by prefix,
//                        and a trailing '.you' wants one you did: cue('repair.oven'), cue('repair.oven.you')
//   socialFill(p, name, ctx) -> the words for a social placeholder ({me}, {nick}, {partner}, {friend}, {best}, {rival},
//                        {mentor}, {mentee}, {boss}, {thing}, {trad}, {home}, {family}, {hobby}, {since}), or null when it can't be filled (skip the line)
SHIP.mem = {}; SHIP.rep = null;
const REP_START = {},                   // a new arrival has no reputation anywhere, your own Works included (the lead's call, 0.36.43)
      REP_DEPTS = ['command', 'helm', 'comms', 'works', 'watch', 'survey', 'infirmary', 'galley', 'store'];
const REP_BANDS = [[70, 'theirs'], [40, 'well'], [20, 'known'], [0, 'new']];
const socId = x => x && x.id || x;
function mem(id, key) {
  socInit(); const l = SHIP.mem[socId(id)]; if (!l || !key) return null;
  let best = null;
  for (const [k, day, w, told] of l) if ((k === key || k.startsWith(key + '.')) && (!best || w > best.w)) best = { key: k, day, w, told: !!told };
  return best;
}
function memTold(id, key) {                              // a line called that memory back: it's not said again
  socInit(); const l = SHIP.mem[socId(id)]; if (!l || !key) return false;
  const m = l.filter(x => !x[3] && (x[0] === key || x[0].startsWith(key + '.'))).sort((x, y) => y[2] - x[2])[0];
  if (m) m[3] = 1; return !!m;
}
function warmth(id, now = shipNow()) {
  socInit(); id = socId(id);
  const l = SHIP.mem[id] || [], r = SHIP.rel[id];
  return l.reduce((a, m) => a + m[2], 0) >= 40 || (r && r.lastTalk !== null && now - r.lastTalk < 3 * 1440) ? 'warm' : 'cold';
}
const affBand = (a, b) => { const v = affinity(a, b); return v <= -40 ? 'rival' : v >= 60 ? 'friend' : 'neutral'; };
// the bond kinds, spelt once (shared with 20c and the line conditions bond:<kind>); BOND_FILL: placeholder -> kind
const SOC_BOND_KINDS = ['friends', 'best', 'rivals', 'mentor', 'mentee', 'drifting', 'couple'], BOND_ALIAS = { friend: 'friends', rival: 'rivals', partner: 'couple' };
const BOND_FILL = { partner: 'couple', friend: 'friends', best: 'best', rival: 'rivals', mentor: 'mentor', mentee: 'mentee' };
function bondOf(id, kind) {
  socInit(); id = socId(id); kind = BOND_ALIAS[kind] || kind;
  if (kind === 'mentor' && SHIP.social.guide && SHIP.social.guide.id === id && SHIP.social.guide.on && SHIP.social.guide.end !== 'handed') return 'you';   // you guide a newcomer (A10), before 20c's
  if (typeof socBondOf === 'function') { const b = socBondOf(id, kind); if (b !== undefined) return b; }   // 20c's, when it has an answer
  if (kind === 'couple') { const p = SOC.idx.has(id) && SOC.crew[SOC.idx.get(id)]; if (p && p.partner && SOC.idx.has(p.partner)) return p.partner; }
  if (kind === 'mentee' && SHIP.social.mentor && SHIP.social.mentor === id) return 'you';   // your escort mentors you (A4)
  const B = SHIP.social.bonds || {}, want = kind === 'mentee' ? 'mentor' : kind;
  for (const k in B) {                                   // 'a:b' -> { kind, since }; for 'mentor', a is the mentor and b the mentee
    const [a, b] = k.split(':'); if (B[k].kind !== want) continue;
    if (kind === 'mentor' ? b === id : kind === 'mentee' ? a === id : a === id || b === id) return a === id ? b : a;
  }
  return null;
}
const moodOf = p => { socInit(); const q = p && p.id ? p : SOC.crew[SOC.idx.get(p)]; if (!q) return 'ok'; const m = crewMood(q, shipNow()); return m < 40 ? 'low' : m >= 70 ? 'high' : 'ok'; };
function beatOf(arcId) {                                // beats told of an arc; an arc id isn't always a crew id ('torres' is torres-zeke's): 20c's arcCrew, else the roster's thread 'arc:<id>'
  if (typeof homeBeatOf === 'function' && /^home\./.test(arcId)) return homeBeatOf(arcId);   // calls home (20c): home arcs aren't crew
  socInit(); let id = typeof arcCrew === 'function' ? arcCrew(arcId) : null;
  if (!id || !SOC.idx.has(id)) { const p = SOC.crew.find(q => q.thread === 'arc:' + arcId); id = p ? p.id : arcId; }
  return SHIP.rel[id] ? SHIP.rel[id].arc || 0 : 0;
}
function knowsNews(p, newsId) {
  socInit(); const id = socId(p);
  if (SHIP.knows[newsId]) return SHIP.knows[newsId].has(id);
  return NEWS.some(x => x.id.startsWith(newsId + ':') && SHIP.knows[x.id] && SHIP.knows[x.id].has(id));
}
const repOf = dept => SHIP.rep && SHIP.rep.dept && isFinite(SHIP.rep.dept[dept]) ? SHIP.rep.dept[dept] : REP_START[dept] || 10;
const repBand = dept => (REP_BANDS.find(([v]) => repOf(dept) >= v) || REP_BANDS[REP_BANDS.length - 1])[1];
const repShip = kind => { const v = SHIP.rep && SHIP.rep.ship && isFinite(SHIP.rep.ship[kind]) ? SHIP.rep.ship[kind] : 50; return v < 35 ? 'low' : v >= 65 ? 'high' : 'ok'; };
function knownFor() {                                   // up to three tags with the most behind them (REP_TAGS: [tag, counter, how many it takes])
  const c = SHIP.rep && SHIP.rep.cnt || {};
  return REP_TAGS.filter(([, k, n]) => (c[k] || 0) >= n).sort((a, b) => c[b[1]] / b[2] - c[a[1]] / a[2] || (a[0] < b[0] ? -1 : 1)).slice(0, 3).map(x => x[0]);
}
function cue(kind) {
  socInit(); const you = /\.you$/.test(kind), k = you ? kind.slice(0, -4) : kind, now = shipNow();
  for (let i = SHIP.social.cues.length - 1; i >= 0; i--) {
    const c = SHIP.social.cues[i];
    if (c.until > now && c.at <= now && (c.key === k || c.key.startsWith(k + '.')) && (!you || c.you)) return c;
  }
  return null;
}
// the ship notes bus (section 13's simNote / onSim; inert without it): what happened becomes a cue that's talked about
// for a day or two. SOC_CUE_OF: note kind -> [the cue's key from its data, days it lasts]. Memories (A2) and
// reputation (A6) listen here too
const SOC_CUE_OF = {
  repair: [d => 'repair.' + ((typeof machineById === 'function' && d.machine && machineById(d.machine) || {}).kind || d.job || (d.kind !== 'repair' && d.kind) || 'machine'), 2],   // the machine's own kind first (the bus's note has its own `kind`)
  tradition: [d => 'tradition.' + d.id, 1], eventPhase: [d => 'event.' + d.id + '.' + d.phase, 1], favour: [d => 'favour' + (d.fav ? '.' + d.fav : ''), 1],
  gift: [d => 'gift' + (d.tag ? '.' + d.tag : ''), 1], harvest: [d => 'harvest', 2], lateMeal: [d => 'lateMeal', 1],
};
const CUE_MAX = 24;                                    // ship notes kept at once (0.36.78: was 30)
function socNote(kind, d) {
  socInit(); d = d || {};
  const c = SOC_CUE_OF[kind]; if (!c) return;
  const now = Math.floor(socNow()), key = c[0](d), you = d.who === 'you' || d.from === 'you' || d.you === true || (Array.isArray(d.came) && d.came.includes('you'));
  const m = kind === 'repair' && typeof machineById === 'function' && d.machine ? machineById(d.machine) : null;   // who it's about (the dialogue engineer's cue:...@me)
  const who = kind === 'gift' ? d.who || d.to || null : kind === 'favour' ? d.from || d.for || null : kind === 'repair' ? (d.who !== 'you' ? d.who : null) || null : null;
  SHIP.social.cues.push({ key, at: now, until: now + c[1] * 1440, you, deck: d.deck || (m && m.deck) || null, who, dept: m ? repDeptOf(m) : null, room: m ? m.room || null : null });
  SHIP.social.cues = SHIP.social.cues.filter(x => x.until > now).sort((a, b) => a.at - b.at || (a.key < b.key ? -1 : a.key > b.key ? 1 : 0) || (String(a.who) < String(b.who) ? -1 : String(a.who) > String(b.who) ? 1 : 0) || (a.you === b.you ? 0 : a.you ? -1 : 1)).slice(-CUE_MAX);   // in time order, whatever order they came in
}
// notes are queued and applied when the social hour they happened in runs (socialHour), at their own time (SOC_T), so one
// big time jump and the same hours played one by one come out the same (0.36.49)
let SOC_T = null;
const socNow = () => SOC_T != null ? SOC_T : shipNow(), socDay = () => Math.floor(socNow() / 1440) + 1;
const SOC_HEARS = ['repair', 'tradition', 'eventPhase', 'favour', 'gift', 'harvest', 'lateMeal', 'choice', 'introStep', 'jobAbandoned', 'jobUnclaimed', 'shiftStart', 'moment'];
function socHear(kind, d) {
  socInit(); d = d || {}; const t = isFinite(d.t) ? d.t : shipNow(), Q = SHIP.social.noteq || (SHIP.social.noteq = []);
  if (t < (SOC_IN != null ? SOC_IN : SHIP.social.hour) * 60) { socApply(kind, d, t); return; }   // its hour has already run (a late note): now, at its own time
  Q.push([t, kind, JSON.parse(JSON.stringify(d))]);
}
function socApply(kind, d, t) {
  const was = SOC_T; SOC_T = t;
  try { if (SOC_CUE_OF[kind]) socNote(kind, d); memNote(kind, d); if (kind === 'introStep') socIntroNote(d); repNote(kind, d); } finally { SOC_T = was; }
}
function socNotesTo(tEnd) {                              // apply the queued notes before tEnd, oldest first (arrival order on a tie)
  const Q = SHIP.social.noteq; if (!Q || !Q.length) return;
  const due = Q.filter(x => x[0] < tEnd).sort((a, b) => a[0] - b[0]); if (!due.length) return;
  SHIP.social.noteq = Q.filter(x => x[0] >= tEnd);
  for (const [t, kind, d] of due) socApply(kind, d, t);
}
if (typeof onSim === 'function') for (const k of SOC_HEARS) onSim(k, d => socHear(k, d));
const SOC_THING = { fav: 'the favour', 'fav.lamp': 'the lamp', 'fav.fetch': 'you fetching my things', fixed: 'the repair', came: 'you coming along', gift: 'the present', visit: 'the visit', bday: 'my birthday',
  show: 'the show', 'show.pell-show': 'the music boxes', appt: 'our catch-ups', mended: 'you patching things up', helped: 'your help' };
function memThing(key) {                                 // {thing}: a memory's object in words ('fixed.oven' -> 'the oven'), or null
  if (typeof key !== 'string' || !key) return null;
  const mk = /^fixed\.(.+)/.exec(key), kind = mk && typeof MACHINE_KINDS !== 'undefined' && MACHINE_KINDS[mk[1]];
  if (kind) return 'the ' + kind.name.toLowerCase();
  const mc = /^came\.(.+)/.exec(key), tr = mc && typeof SHIP_TRADITIONS !== 'undefined' && SHIP_TRADITIONS.find(x => x.id === mc[1]);   // came.quiz -> 'the quiz night'
  if (tr) return 'the ' + tr.name.toLowerCase();
  for (let s = key; s; s = s.includes('.') ? s.slice(0, s.lastIndexOf('.')) : '') if (SOC_THING[s]) return SOC_THING[s];
  return null;
}
// place:calm (and moments' readiness) is the places' own: CALM_TYPES and placeCalm(p) in DECKS' kit (the deck architect, 0.38.9)
const SOC_NUM = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty'];
function socDays(phrase) {                               // 'six years' / 'eight months' / 'one week' / 'a year' -> days, or null
  const m = typeof phrase === 'string' && /^\s*(\d+|an?|[a-z]+)\s+(day|week|month|year)s?\b/i.exec(phrase); if (!m) return null;
  const w = m[1].toLowerCase(), n = /^\d+$/.test(w) ? +w : w === 'a' || w === 'an' ? 1 : SOC_NUM.indexOf(w); if (n < 0) return null;
  return n * { day: 1, week: 7, month: 30, year: 365 }[m[2].toLowerCase()];
}
function socDuration(n) {                                // days -> words: 'a day or two', 'three days', 'a week', 'five weeks', 'eighteen months', 'twelve years'
  const W = x => SOC_NUM[x] || String(x), wk = Math.floor(n / 7), mo = Math.round(n / 30), yr = Math.round(n / 365);
  return n < 2 ? 'a day or two' : n < 7 ? W(n) + ' days' : wk < 9 ? (wk === 1 ? 'a week' : W(wk) + ' weeks') : n < 610 ? (mo <= 1 ? 'a month' : W(mo) + ' months') : n < 730 ? 'nearly two years' : W(yr) + ' years';   // SOC_NUM goes to twenty
}
const SOC_HOBBY = { musician: 'playing music', music: 'listening to records', gardener: 'gardening', 'garden-lover': 'pottering in the garden', runner: 'running', stargazer: 'stargazing',
  'gym-regular': 'training in the gym', shopper: 'browsing the store', 'quiet-corner': 'reading in quiet corners', 'lounge-regular': 'playing Tiles in the lounge', 'common-room': 'playing games in the common room', 'window-seat': 'watching the stars go by' };
function socialFill(p, name, ctx = {}) {
  socInit(); const tier = relTier(p.id), nameOf = id => id === 'you' ? chatName() : id && SOC.idx.has(id) ? shortName(SOC.crew[SOC.idx.get(id)]) : null;
  if (name === 'me') return chatName();
  if (name === 'nick') {
    const n = typeof VOICE !== 'undefined' && VOICE[p.id] && VOICE[p.id].words && VOICE[p.id].words.nick, v = Array.isArray(n) ? n[tier] : null;
    return v ? v.replace('{me}', chatName()) : tier >= 2 ? chatName() : 'cadet';
  }
  if (BOND_FILL[name]) return nameOf(bondOf(p.id, BOND_FILL[name]));
  if (name === 'boss') {
    const top = SOC.crew.filter(q => q.dept === p.dept && q !== p && (q.rank === 'chief' || q.rank === 'captain'));
    return top.length ? shortName(top[0]) : null;
  }
  if (name === 'thing') return memThing(ctx.mem && (ctx.mem.key || ctx.mem));
  // theme fill-ins from the roster (the writers' {home}: a place, {family}: "my <someone>", {hobby}: an -ing activity, {since}: a duration)
  if (name === 'home') return typeof p.home === 'string' && p.home ? p.home : null;
  if (name === 'family') return typeof p.family === 'string' && p.family.trim() ? p.family.trim() : null;   // as written (writers say "my {family}")
  if (name === 'hobby') { if (typeof p.hobby === 'string' && p.hobby) return p.hobby; const h = (p.habits || []).map(x => SOC_HOBBY[x]).find(Boolean); return h || null; }
  if (name === 'kin' || name === 'lost' || name === 'hobbyNoun') { const v = p[name]; return typeof v === 'string' && v.trim() ? v.trim() : null; }   // the roster's short theme fields as written ("my gran", "my wife", "chess"); "" is none
  if (name === 'since') {                                // how long they've been aboard, growing with the game: from their arrival day, or the roster's since (at day 1) plus the days since
    const a = arriveDay(p), d = SHIP.time.day;
    if (a != null && a > 1) return d >= a ? socDuration(d - a) : null;
    const base = socDays(p.since); return base == null ? (typeof p.since === 'string' && p.since ? p.since : null) : socDuration(base + Math.max(0, d - 1));
  }
  if (name === 'trad') {
    const id = ctx.trad, d = SHIP.time.day, es = typeof eventsOn === 'function' ? eventsOn(d) : [];
    const e = id ? es.find(x => x.id === id) || (typeof SHIP_TRADITIONS !== 'undefined' ? SHIP_TRADITIONS.find(x => x.id === id) : null) : es.find(x => !x.honorees || !x.honorees.length);
    return e && e.name || null;
  }
  return null;
}

// lines through the dialogue engine (0.36.22, A3): section 20 picks which kind of line matters most (chatLine's order),
// section 22's lineFor(p, kind, ctx) -> { text, id, kind } | null finds the words (the person's own lines, their voice
// template's, the shared bank; plans/social-deep-plan.md Part 6). Null, or no engine yet: chatLine goes on down its
// order, and the lists below are the fallback, so without section 22 every line is as before. ctx: { t, tier, peek,
// act, room, placeId, warmth, talk, bubble }; peek means only looking ahead, so the engine should note nothing
// (recently said, memTold) for it. New kinds in the order: hint (a moment ready, 20c's momentReady), callback (a memory,
// 60%), cue (a ship note, 50%), joy and about (a bonded crewmate), and near, life, greet and smalltalk ahead of the lists
const SOC_LEGACY = new Set(['greet', 'near', 'life', 'smalltalk']);   // kinds the old lists still answer (section 22's linesLegacy): the engine only for people with their own lines
function socLine(p, kind, ctx = {}) {
  if (typeof lineFor !== 'function') return null;
  if (SOC_LEGACY.has(kind) && !(typeof VOICE !== 'undefined' && VOICE[p.id] && VOICE[p.id].lines)) return null;
  try { const l = lineFor(p, kind, ctx); return l && typeof l.text === 'string' && l.text ? l : null; } catch (e) { return null; }
}

const socGreet = (p, t = shipNow(), peek = false) => { const l = socLine(p, 'greet', { t, tier: relTier(p.id), warmth: warmth(p.id), peek }); return l ? { text: l.text, kind: 'greet', say: true, line: l } : chatGreet(p, t); };   // greet: the engine first, else chatGreet's list

// ---- memories with decay (0.36.21, A2; plans/social-deep-plan.md Part 2) ----
// Each crew member keeps up to MEM_MAX memories of you: SHIP.mem[id] = [[key, day, w, told, half], ...] (saved). key is
// 'kind.arg' (fav.lamp, fixed.oven, came.quiz, appt.social, missed.<apptId>, grubby, ...); w its weight, 0-100, from its
// class (MEM_CLASS: [starting weight, half-life in days], 0 = kept for good); half the class's half-life. Every ship
// day at 04:00 (socialHour) each memory fades by its half-life and is forgotten below MEM_FORGET; a ninth memory pushes
// out the lightest. Nothing here takes points away: sour memories only change words. A big memory is heard of by up to
// three of their friends (affinity 40+), who keep a small heard.<key> memory of it.
//   memAdd(id, key, { w, cls }) -> the memory (a repeat refreshes it: today, and the heavier weight)
const MEM_CLASS = { small: [30, 7], medium: [60, 21], big: [90, 60], core: [100, 0], sour: [40, 4] };
const MEM_KIND = { chat: 'small', came: 'small', meeting: 'small', heard: 'small', fav: 'medium', fixed: 'medium', appt: 'medium', visit: 'medium', introduced: 'medium',
  bday: 'medium', mended: 'medium', talk: 'medium', gift: 'medium', moment: 'big', show: 'big', helped: 'big', readyroom: 'big', guide: 'big', hosted: 'big', intro: 'core', keepsake: 'core', missed: 'sour', grubby: 'sour' };
const MEM_MAX = 8, MEM_FORGET = 10;
const memClass = key => { for (let s = key; s; s = s.includes('.') ? s.slice(0, s.lastIndexOf('.')) : '') if (MEM_KIND[s]) return MEM_KIND[s]; return 'small'; };
function memAdd(id, key, o = {}) {
  socInit(); id = socId(id); if (!SOC.idx.has(id) || typeof key !== 'string' || !key) return null;
  const cls = MEM_CLASS[o.cls] ? o.cls : memClass(key), [w0, half] = MEM_CLASS[cls], w = isFinite(o.w) ? Math.max(0, Math.min(100, o.w)) : w0;
  const day = socDay(), l = SHIP.mem[id] || (SHIP.mem[id] = []);
  let m = l.find(x => x[0] === key);
  if (m) { m[1] = day; m[2] = Math.max(m[2], w); m[4] = half && m[4] ? Math.max(m[4], half) : 0; }
  else {
    l.push(m = [key, day, w, 0, half]);
    if (l.length > MEM_MAX) { let k = 0; for (let i = 1; i < l.length; i++) if (l[i][2] < l[k][2] || (l[i][2] === l[k][2] && l[i][1] < l[k][1])) k = i; l.splice(k, 1); }
  }
  if (cls === 'big' && !key.startsWith('heard.')) {          // their friends hear about it
    const fr = SOC.crew.filter(q => q.id !== id && affinity(id, q) >= 40)
      .sort((a, b) => affinity(id, b) - affinity(id, a) || (a.id < b.id ? -1 : 1)).slice(0, 3);
    for (const q of fr) if (!(SHIP.mem[q.id] || []).some(x => x[0] === 'heard.' + key)) memAdd(q.id, 'heard.' + key, { cls: 'small' });
  }
  return l.includes(m) ? m : null;
}
function memSave() {                                    // mem: { id: [[key index, day, w, told, half]] } with the keys stored once
  const keys = [], ki = new Map(), mem = {};
  for (const id in SHIP.mem) mem[id] = SHIP.mem[id].map(([k, d, w, t, h]) => { if (!ki.has(k)) { ki.set(k, keys.length); keys.push(k); } return [ki.get(k), d, w, t ? 1 : 0, h]; });
  return { memKeys: keys, mem };
}
function memLoad(s) {
  SHIP.mem = {}; const keys = Array.isArray(s.memKeys) ? s.memKeys : [];
  for (const id in s.mem && typeof s.mem === 'object' ? s.mem : {}) if (SOC.idx.has(id) && Array.isArray(s.mem[id]))
    SHIP.mem[id] = s.mem[id].filter(m => Array.isArray(m) && typeof keys[m[0]] === 'string' && isFinite(m[2])).slice(0, MEM_MAX).map(([k, d, w, t, h]) => [keys[k], d | 0, +w, t ? 1 : 0, +h || 0]);
}
function memFade() {                                     // once a ship day, at 04:00 (socialHour)
  for (const id in SHIP.mem) {
    const l = SHIP.mem[id];
    for (const m of l) if (m[4]) m[2] = Math.round(m[2] * Math.pow(.5, 1 / m[4]) * 100) / 100;
    SHIP.mem[id] = l.filter(m => !m[4] || m[2] >= MEM_FORGET);
    if (!SHIP.mem[id].length) delete SHIP.mem[id];
  }
}
// a repair you finished (the bus's repair note): the people who use that machine remember it, those who spent time in its
// room today, the ones who know you best first, at most six
function memRepair(d) {
  if (d.who !== 'you' || typeof machineById !== 'function') return;
  const m = d.machine && machineById(d.machine); if (!m || !m.room) return;
  const S = schedData(), day = socDay();
  const users = SOC.crew.filter(p => planDay(p, day).some(s => { const pl = s.placeId && S.byId.get(s.placeId); return pl && pl.deck === m.deck && pl.room === m.room; }))
    .sort((a, b) => relTier(b.id) - relTier(a.id) || schedU(a.seed, day, 644) - schedU(b.seed, day, 644)).slice(0, 6);
  for (const p of users) memAdd(p.id, 'fixed.' + m.kind);
}
function memNote(kind, d) {
  if (kind === 'repair') memRepair(d);
  else if (kind === 'tradition' && Array.isArray(d.came) && (d.you || d.came.includes('you')))   // you came: those there who know you
    for (const id of d.came) if (id !== 'you' && SHIP.rel[id] && SHIP.rel[id].met !== null) memAdd(id, 'came.' + d.id);
  if (kind === 'choice' && d.script) for (const id of [].concat(d.who || [])) memAdd(id, typeof d.mem === 'string' && d.mem ? d.mem : 'meeting.' + d.script + '.' + (d.k ?? 0));   // the choice's own mem key when the script gives one
}

// ---- the first week (0.36.23, A4; plans/social-deep-plan.md Part 7) ----
// Onboarding (section 21) runs the arrival and week 1 and sets flags in section 13's store (flag / flagSet). While its
// intro is running (SHIP.intro, not done or skipped, and no week1.done flag), social features wait for their day:
// chat cards always; favours from week1.d2 (Tuesday), friends waving you over from week1.d3, invitations from week1.d5,
// moments and bunk visits once week1.done (socGate('d2' | 'd3' | 'd5' | 'done'), for 20c too). With no intro (older
// saves, test URLs, skip-intro's end state) everything is open. introStep notes on the bus give core memories (the
// arrival and the shadow shift with the escort, the dinner with Calder and the escort), and the escort becomes your
// mentor (SHIP.social.mentor, saved; bondOf(escort, 'mentee') -> 'you'): week-1 lines first on their card, and an
// evening check-in, a wave from them each evening of week 1.
// socialInvite({ trad | kind, day, from, at, where, len }) -> an appointment id, or null: an invitation you accept or
// decline on the device (Appointments, status 'asked', kind 'invite'). For a tradition, it's where and when the host's
// plan has them there that day (their 'ev-<trad>' block), so the host keeps their own day; else at / where as given.
const INTRO_MEM = { hello: 'intro.arrival', bunk: 'intro.arrival', arrival: 'intro.arrival', chief: 'intro.dinner', dinner: 'intro.dinner', shadow: 'intro.shadowShift', shadowShift: 'intro.shadowShift', 'd1-shadow': 'intro.shadowShift' };   // section 21's step ids
function socIntroOn() {                                 // the first week is running: section 21's introOn() when it's there (it stays on after skip-intro: the week still runs), else SHIP.intro or an escort flag; never after week1.done
  if (typeof flag === 'function' && flag('week1.done')) return false;
  try { if (typeof introOn === 'function') return !!introOn(); } catch (e) { return false; }   // inside the try: section 21's const is later in the file
  return SHIP.intro && typeof SHIP.intro === 'object' ? SHIP.intro.on !== false && !SHIP.intro.ended : !!escortId();
}
const inWeek1 = () => socIntroOn();                        // the line condition week1:true (the frozen vocabulary)
const socGate = stage => !socIntroOn() || (typeof flag === 'function' && !!flag(stage === 'done' ? 'week1.done' : 'week1.' + stage));
function escortId() {                                   // SHIP.intro.escort, else the flag escort.<roster id> (section 21 sets escort.torres-zeke)
  socInit(); const e = SHIP.intro && SHIP.intro.escort; if (e && SOC.idx.has(e)) return e;
  if (SHIP.social.mentor) return SHIP.social.mentor;
  if (typeof flag === 'function') for (const p of SOC.crew) if (flag('escort.' + p.id)) return p.id;
  return null;
}
function socIntroNote(d) {                                  // the bus's introStep { step, who, missed }
  socInit(); if (socGuideStep(d)) return;   // a newcomer's step while you guide them (A10)
  const e = escortId(); if (e && !SHIP.social.mentor) SHIP.social.mentor = e;
  if (d.missed) return;                                  // a step you missed leaves no memory
  const key = INTRO_MEM[d.step]; if (!key) return;
  for (const id of [].concat(d.who || [], INTRO_MEM[d.step] === 'intro.dinner' && SOC.idx.has('calder') ? ['calder'] : [], e ? [e] : [])) memAdd(id, key, { cls: 'core' });
}
function socialInvite(o = {}) {
  socInit(); const from = o.from, p = SOC.idx.has(from) ? SOC.crew[SOC.idx.get(from)] : null;
  if (!p || !SHIP.device || !Array.isArray(SHIP.device.appts)) return null;
  const day = o.day || SHIP.time.day, D = SHIP.device;
  let at = isFinite(o.at) ? (o.at < 1440 ? (day - 1) * 1440 + o.at : o.at) : null, where = o.where || null, len = o.len || 60;
  if (o.trad) {
    const seg = planDay(p, day).find(s => s.placeId && s.tag && (s.tag === 'ev-' + o.trad || s.tag.startsWith('ev-' + o.trad + '-')));
    if (!seg) return null;                               // they aren't going after all
    at = seg.from; where = seg.placeId; len = Math.min(60, seg.to - seg.from);   // plans are in absolute ship minutes
  }
  if (!isFinite(at) || !where || at < shipNow()) return null;
  if (D.appts.some(a => a.by === from && a.kind === 'invite' && Math.abs(a.at - at) < 60 && a.status !== 'no')) return null;   // asked already
  const id = D.appts.reduce((m, x) => Math.max(m, x.id || 0), 0) + 1;
  D.appts.push({ id, with: [from], at, len, where, kind: 'invite', status: 'asked', by: from, trad: o.trad || null, inv: o.kind || (o.trad ? 'trad' : 'personal') });
  if (typeof simNote === 'function') simNote('invite', { from, id, trad: o.trad || null });
  if (typeof deviceNotify === 'function') deviceNotify({ app: 'appointments', text: shortName(p) + ' has invited you' + (o.trad ? ' along' : '') + '.', urgent: false });
  return id;
}

// ---- small gifts (0.36.24, A5; plans/social-deep-plan.md Part 4) ----
// A gift is something in your hands (SHIP.player.carry, section 15: item names, at most CARRY_MAX) that SOC_GIFTS knows:
// bought at the crew store, picked in the garden on harvest days, or made in the machine shop (GIFT_MAKES, for the
// sections that sell, grow and make them: they call giftAdd(item)). With one in your hands the chat card shows Give
// <item>, once per person per ship week (rel.giftWeek, saved). How it lands comes from their loves and likes (the
// voice card's VOICE[id].loves / likes once 20c reads them, else giftTaste from their habits and work): loved +10 and
// a big memory (and "Loves <tag>" in what you know), liked +6 and a medium one, anything else +2 and a small one;
// double on their birthday. Never less. Crew give you things too: at most one a ship week across the ship, from a
// friend, as a note in Mail (SHIP.social.given, saved, for the device's locker view); a keepsake (giftKeepsake, from
// 20c's resolution moments) goes on the shelf by your bunk (keepsakes(), at most 8; the shelf and its props are the deck
// architect's and the performance engineer's).
const SOC_GIFTS = {
  'tin of tea': { tag: 'tea', from: 'store' }, 'biscuits': { tag: 'sweet', from: 'store' }, 'postcard': { tag: 'star', from: 'store' }, 'little plant': { tag: 'plant', from: 'store' },
  'puzzle book': { tag: 'book', from: 'store' }, 'herbs': { tag: 'garden', from: 'garden' }, 'tomato': { tag: 'garden', from: 'garden' }, 'flower': { tag: 'plant', from: 'garden' },
  'bar of chocolate': { tag: 'sweet', from: 'store' }, 'paper novel': { tag: 'book', from: 'store' }, 'music chip': { tag: 'music', from: 'store' }, 'pocket puzzle': { tag: 'game', from: 'store' },
  'spare tiles set': { tag: 'game', from: 'store' }, 'tin whistle': { tag: 'music', from: 'made' }, 'metal puzzle': { tag: 'game', from: 'made' },
  'keyring': { tag: 'made', from: 'made' }, 'bookend': { tag: 'made', from: 'made' }, 'gear pendant': { tag: 'made', from: 'made' },
};
const GIFT_MAKES = [{ item: 'keyring', mins: 10, needs: 'scrap' }, { item: 'bookend', mins: 20, needs: 'scrap' }, { item: 'gear pendant', mins: 15, needs: 'scrap' }, { item: 'tin whistle', mins: 15, needs: 'scrap' }, { item: 'metal puzzle', mins: 20, needs: 'scrap' }];   // the machine shop's (section 15/17 build the making)
const GIFT_PTS = { loved: 10, liked: 6, polite: 2 }, GIFT_MEM = { loved: 'big', liked: 'medium', polite: 'small' };
const GIFT_HABIT = { 'tea-break': 'tea', 'garden-lover': 'garden', gardener: 'plant', stargazer: 'star', 'window-seat': 'star', music: 'music', musician: 'music', shopper: 'sweet',
  'lingers-at-meals': 'sweet', 'quiet-corner': 'book', 'lounge-regular': 'game', 'common-room': 'game', workaholic: 'made', 'bar-regular': 'sweet', runner: 'tea', 'gym-regular': 'tea' };
const GIFT_NOTES = [['a biscuit, wrapped in a napkin', 'Saved you one. Don\'t tell the others.'], ['a little sketch of the Wren', 'Drew this on my break. It\'s you, by the lift. Sort of.'],
  ['a cutting from the garden', 'It\'ll root if you keep it wet. Put it by your bunk.'], ['a cup of tea, gone cold', 'Made you a tea and you weren\'t here. It\'s the thought that counts.'], ['a folded paper star', 'Found the instructions in an old book. Took me six tries.']];
const giftOf = item => { const k = item && (item.name || item); return typeof k === 'string' && SOC_GIFTS[k.toLowerCase()] ? { item: k.toLowerCase(), ...SOC_GIFTS[k.toLowerCase()] } : null; };
const socWeek = (d = socDay()) => Math.floor((d - 1) / 7);
const GIFT_TAG_ALIAS = { card: 'star', postcard: 'star', books: 'book', games: 'game', plants: 'plant', sweets: 'sweet' };   // writers' words -> SOC_GIFTS tags
function giftTaste(p) {                                  // { loves: [tags], likes: [tags] }
  const v = typeof VOICE !== 'undefined' && VOICE[p.id], tag = x => GIFT_TAG_ALIAS[x] || x;
  if (v && (Array.isArray(v.loves) || Array.isArray(v.likes))) return { loves: (v.loves || []).map(tag), likes: (v.likes || []).map(tag) };
  const tags = [...new Set((p.habits || []).map(h => GIFT_HABIT[h]).filter(Boolean).concat(p.dept === 'works' ? ['made'] : p.dept === 'galley' ? ['garden'] : p.dept === 'survey' ? ['star'] : []))];
  return { loves: tags.slice(0, 1), likes: tags.slice(1).concat(tags.includes('sweet') ? [] : ['sweet']) };
}
function giftAdd(item) {                                 // into your hands: true, or false when they're full or it isn't a gift
  const g = giftOf(item); if (!g || !SHIP.player || !Array.isArray(SHIP.player.carry) || SHIP.player.carry.length >= (typeof CARRY_MAX !== 'undefined' ? CARRY_MAX : 2)) return false;
  SHIP.player.carry.push(g.item); return true;
}
const giftInHands = () => SHIP.player && Array.isArray(SHIP.player.carry) ? SHIP.player.carry.find(x => giftOf(x)) || null : null;
function giftGive(p, item) {                             // -> { how: 'loved' | 'liked' | 'polite', text } or null
  socInit(); const g = giftOf(item), r = relGet(p.id), wk = socWeek();
  if (!g || r.giftWeek === wk + 1) return null;          // giftWeek: the week given in, plus one (0 means never)
  const i = SHIP.player.carry.indexOf(g.item); if (i < 0) return null;
  SHIP.player.carry.splice(i, 1); r.giftWeek = wk + 1;
  const t = giftTaste(p), how = t.loves.includes(g.tag) ? 'loved' : t.likes.includes(g.tag) ? 'liked' : 'polite', bday = isBirthday(p, shipNow());
  relAdd(p.id, 'gift', GIFT_PTS[how] * (bday ? 2 : 1)); repAdd(null, 0, { kindness: 2 }, 'kind');
  memAdd(p.id, 'gift.' + g.tag, { cls: GIFT_MEM[how] });
  if (how === 'loved') { const k = 'Loves ' + ({ tea: 'tea', sweet: 'sweet things', star: 'the stars', plant: 'plants', book: 'a good book', garden: 'anything from the garden', made: 'things made by hand', music: 'music', game: 'a game' }[g.tag] || g.tag) + '.'; if (!r.known.includes(k)) r.known.push(k); }
  if (typeof simNote === 'function') simNote('gift', { who: p.id, to: p.id, from: 'you', item: g.item, tag: g.tag, how });   // who: the one who got it
  const l = socLine(p, 'gift', { how, item: g.item, tag: g.tag, bday }), U = k => schedU(p.seed, Math.floor(shipNow() / 60), k);
  const text = l ? l.text : how === 'loved' ? ['Oh! How did you know? I love these.', 'For me? This is perfect. Thank you!', 'You absolute star. This is exactly my thing.'][Math.floor(U(648) * 3)]
    : how === 'liked' ? ['That\'s really kind. Thank you.', 'Oh, nice! Thanks, ' + chatName() + '.', 'You didn\'t have to. I\'ll enjoy this.'][Math.floor(U(648) * 3)]
    : ['Oh! That\'s... thoughtful. Thank you.', 'For me? Well. Thank you.', 'That\'s kind of you.'][Math.floor(U(648) * 3)];
  return { how, text: text + (bday ? ' On my birthday, too.' : '') };
}
function giftKeepsake(p, what) {                         // 20c's resolution moment: a keepsake for your shelf (at most 8)
  socInit(); const K = SHIP.social.keepsakes || (SHIP.social.keepsakes = []);
  if (K.some(x => x.from === p.id) || K.length >= 8) return false;
  const v = typeof VOICE !== 'undefined' && VOICE[p.id];
  K.push({ from: p.id, what: what || (v && v.keepsake) || 'a small keepsake', day: SHIP.time.day }); memAdd(p.id, 'keepsake', { cls: 'core' });
  return true;
}
const keepsakes = () => (socInit(), (SHIP.social.keepsakes || []).map(x => ({ ...x, name: SOC.idx.has(x.from) ? SOC.crew[SOC.idx.get(x.from)].name : x.from })));
function socCrewGift(h) {                                // once a ship day at 19:00 (socialHour): now and then a friend leaves you something
  const d = Math.floor(h / 24) + 1, wk = socWeek(d), G = SHIP.social.given || (SHIP.social.given = []);
  if (G.some(x => socWeek(x.day) === wk) || schedU(wk, d, 649) >= .2) return;
  const fr = SOC.crew.filter(p => relTier(p.id) >= 3 && warmth(p.id, h * 60 + 30) === 'warm').sort((a, b) => schedU(a.seed, d, 650) - schedU(b.seed, d, 650));
  if (!fr.length) return;
  const p = fr[0], [what, note] = GIFT_NOTES[Math.floor(schedU(p.seed, d, 651) * GIFT_NOTES.length)];
  G.push({ from: p.id, what, day: d }); if (G.length > 20) G.shift();
  SHIP.social.mail.push({ at: h * 60 + 30, from: p.name, subject: 'Left you something', body: 'There\'s ' + what + ' on your bunk. ' + note + ' ' + shortName(p) });
}

// ---- reputation (0.36.25, A6; plans/social-deep-plan.md Part 8) ----
// Two layers, cozy: nothing here takes a tier or a friend away, and good work always lifts it again.
// SHIP.rep = { dept: { <dept>: 0-100 }, ship: { work, kindness, spirit }: 0-100, cnt: { known-for counters }, wk: { <dept>: the
// week its tradition last counted }, day: { <what>: the day it last counted }, streak (favours declined in a row),
// bands: { <dept>: the band last seen }, notes: [{ day, from, text }] (the Record's), thanks: [<dept>] } (saved).
// Each department starts at 10 (the lowest band, 'new'; Works too) and never drops below its floor: 5 for each close friend there (at most 25);
// below that it climbs 1 a week. The ship standings start at 50 and each Sunday pull 10% back toward 50, so they follow
// the last few weeks. Sources (repAdd): your repairs (the machine's department, repDeptOf: +3, +5 if it was failing;
// Work +2 or +3), favours (+2 their department, Kindness +3), traditions you join (+1 a week to the host's department,
// Spirit +3), gifts (Kindness +2), a mended feud (Kindness +3), a birthday chat (Spirit +2), chatting outside Works
// (Spirit +.5), kept appointments (Kindness +1); gentle dips: a job of theirs you took and left (jobAbandoned, -2 and
// Work -3), one of their machines failing while its job sat unclaimed in your free shift time (jobUnclaimed, -1 at most
// once a day), a missed appointment (Kindness -2; -1 to an officer's department), well late for shift (shiftStart late
// 20+: Work -2; on time +1), three favours declined in a row (Kindness -2).
// Consequences: strangers start warmer (REP_WARM by band: 4 'known', 8 'well' and up), favours 50% more often at 'well',
// repAskedFor(dept) for the job board's "asked for you" (section 17), Calder's notes and a department's thank-you in the
// Record (repNotes), reputation gossip each Sunday (news about you), and repView() for the Record's Reputation page.
// knownFor() -> up to three tags with the most behind them (REP_TAGS).
const REP_DEPTS_ALL = ['command', 'helm', 'comms', 'works', 'watch', 'survey', 'infirmary', 'galley', 'store', 'garden'];
const REP_WARM = { new: 0, known: 4, well: 8, theirs: 8 };
const REP_NAMES = { new: 'New face', known: 'They know your name', well: 'Well thought of', theirs: 'One of theirs' };
const REP_SYS = { food: 'galley' };                       // a machine nobody works beside: its department by system, else Works
const REP_TAGS = [['reliable', 'jobs', 6], ['kind', 'kind', 6], ['chatty', 'chats', 12], ['quiz regular', 'trad.quiz', 3], ['gym rat', 'trad.running', 3], ['always at the garden', 'trad.garden', 3],
  ['the one who fixes ovens', 'fix.oven', 3], ['good with newcomers', 'newcomer', 1], ['night owl', 'night', 5]];
const REP_SHIP_WORDS = { work: ['still finding your feet', 'steady', 'dependable', 'the one they call'], kindness: ['keeps to yourself', 'a good shipmate', 'kind', 'the one people go to'],
  spirit: ['not often seen at things', 'turns up now and then', 'often seen at things', 'part of the furniture (in a good way)'] };
function repInit() {
  if (SHIP.rep && SHIP.rep.dept) return SHIP.rep;
  const dept = {}; for (const d of REP_DEPTS_ALL) dept[d] = REP_START[d] || 10;
  return SHIP.rep = { dept, ship: { work: 50, kindness: 50, spirit: 50 }, cnt: {}, wk: {}, day: {}, streak: 0, bands: {}, notes: [], thanks: [] };
}
const repFloor = d => Math.min(25, 5 * SOC.crew.filter(p => p.dept === d && relTier(p.id) >= 4).length);
function repAdd(dept, n, ship, why) {                    // n to the department (if any), ship: { work, kindness, spirit } deltas
  socInit(); const R = repInit();
  if (dept && isFinite(R.dept[dept]) && n) R.dept[dept] = Math.round(Math.max(repFloor(dept), Math.min(100, R.dept[dept] + n)) * 100) / 100;
  for (const k in ship || {}) if (isFinite(R.ship[k]) && ship[k]) { const x = R.ship[k], n = ship[k] * (ship[k] > 0 ? (x > 50 ? (100 - x) / 50 : 1) : (x < 50 ? x / 50 : 1));   // A12: harder to climb near the top (and to fall near the bottom)
    R.ship[k] = Math.round(Math.max(0, Math.min(100, x + n)) * 100) / 100; }
  if (why) R.cnt[why] = (R.cnt[why] || 0) + 1;
  if (dept) repBandCheck(dept);
}
const repOnce = (what, day = socDay()) => { const R = repInit(); if (R.day[what] === day) return false; R.day[what] = day; return true; };
const REP_DEPT_OF = new Map();
function repDeptOf(m) {                                  // the department that uses a machine: who works in its room (day 1's plans), else by system
  if (!m) return 'works'; if (REP_DEPT_OF.has(m.id)) return REP_DEPT_OF.get(m.id);
  const S = schedData(), n = {};
  for (const p of SOC.crew) for (const s of planDay(p, 1)) { const pl = s.act === 'work' && s.placeId && S.byId.get(s.placeId); if (pl && pl.deck === m.deck && pl.room === m.room) n[p.dept] = (n[p.dept] || 0) + 1; }
  const best = Object.keys(n).filter(d => REP_DEPTS_ALL.includes(d)).sort((a, b) => n[b] - n[a] || (a < b ? -1 : 1))[0];
  const d = best || REP_SYS[(MACHINE_KINDS[m.kind] || {}).sys] || 'works'; REP_DEPT_OF.set(m.id, d); return d;
}
const tradDept = id => { const e = typeof SHIP_TRADITIONS !== 'undefined' && SHIP_TRADITIONS.find(x => x.id === id), p = e && e.from && SOC.crew.find(q => q.name === e.from); return p ? p.dept : null; };
function repNote(kind, d) {                              // from the bus
  socInit(); d = d || {};
  if (kind === 'repair' && d.who === 'you') {
    const m = typeof machineById === 'function' && machineById(d.machine), bad = /failing|broken/.test(d.state || d.was || '') || d.failing === true;
    repAdd(m ? repDeptOf(m) : d.dept || 'works', bad ? 5 : 3, { work: bad ? 3 : 2 }, 'jobs');
    if (m) repInit().cnt['fix.' + m.kind] = (repInit().cnt['fix.' + m.kind] || 0) + 1;
  } else if (kind === 'tradition' && (d.you || (Array.isArray(d.came) && d.came.includes('you')))) {
    const dp = tradDept(d.id), R = repInit(), wk = socWeek();
    if (dp && R.wk[dp] !== wk) { R.wk[dp] = wk; repAdd(dp, 1); }
    repAdd(null, 0, { spirit: 3 }, 'trad.' + d.id);
  } else if (kind === 'jobAbandoned') {
    const m = typeof machineById === 'function' && machineById(d.machine); repAdd(d.dept || (m ? repDeptOf(m) : 'works'), -2, { work: -3 });
  } else if (kind === 'jobUnclaimed') {
    const m = typeof machineById === 'function' && machineById(d.machine), dp = d.dept || (m ? repDeptOf(m) : 'works'); if (repOnce('unclaimed.' + dp, 'w' + socWeek())) repAdd(dp, -1);   // A12: once a ship week a department (was daily)
  } else if (kind === 'shiftStart' && isFinite(d.late)) {
    if (d.late >= 20) { repAdd(null, 0, { work: -2 }); repInit().cnt.late = (repInit().cnt.late || 0) + 1; } else repAdd(null, 0, { work: 1 });
  } else if (kind === 'moment' && d.flavour === 'listen') repAdd(null, 0, { kindness: 2 }, 'kind');
}
function repBandCheck(dept) {                            // a band changed: a quiet badge on the Record; reaching 'theirs', their thank-you
  const R = repInit(), b = repBand(dept); if (R.bands[dept] === b) return;
  const was = R.bands[dept]; R.bands[dept] = b;
  if (!was) return;
  if (typeof deviceNotify === 'function') deviceNotify({ app: 'record', text: 'Reputation: ' + dept[0].toUpperCase() + dept.slice(1) + ', ' + REP_NAMES[b].toLowerCase() + '.', urgent: false });
  if (b === 'theirs' && !R.thanks.includes(dept)) {
    R.thanks.push(dept);
    const chief = SOC.crew.find(p => p.dept === dept && (p.rank === 'chief' || p.rank === 'captain')) || SOC.crew.find(p => p.dept === dept);
    if (chief) {
      SHIP.social.mail.push({ at: Math.floor(socNow()) + 30, from: chief.name, subject: 'From all of us', body: 'The ' + dept + ' crew asked me to say thank you. You\'ve been a real help to us. Consider yourself one of ours. ' + shortName(chief) });
      if (dept !== 'works') repNoteAdd(chief.name, shortName(chief) + ' told Chief Calder you\'ve been a great help to ' + dept + '.');
    }
  }
}
function repNoteAdd(from, text) { const R = repInit(); R.notes.push({ day: socDay(), from, text }); if (R.notes.length > 20) R.notes.shift(); }
function repWeek(h) {                                    // Sunday 04:00 (socialHour): the pull to the middle, floors, Calder's note, gossip about you
  const R = repInit(), d = Math.floor(h / 24) + 1;
  for (const k in R.ship) R.ship[k] = Math.round((R.ship[k] + (50 - R.ship[k]) * .1) * 100) / 100;
  for (const dp in R.dept) { const f = repFloor(dp); if (R.dept[dp] < f) R.dept[dp] = Math.min(f, R.dept[dp] + 1); }
  const late = R.cnt.late || 0, lateWas = R.cnt.lateSeen || 0; R.cnt.lateSeen = late;
  if (late - lateWas >= 2) repNoteAdd('Chief Ines Calder', (late - lateWas === 2 ? 'Two' : 'A few') + ' late starts this week. Let\'s not make it a habit.');
  else if (repShip('work') === 'high' && !R.notes.some(n => n.day > d - 28 && /good work/i.test(n.text))) repNoteAdd('Chief Ines Calder', 'Good work this month. People have noticed.');
  // what the ship says about you: one piece of news a week at most, from your highest or lowest standing
  const me = chatName(), works = SOC.crew.filter(p => p.dept === 'works').map(p => p.id);
  const say = repShip('work') === 'high' ? ['Ask ' + me + ', they always turn up.', 'That cadet in Works? Reliable as the lift.']
    : repShip('work') === 'low' ? ['The new tech\'s been missing shift starts. Calder\'s noticed.', 'Is the new cadet ever on time?']
    : repShip('kindness') === 'high' ? [me + '\'s the one to go to if you need a hand.', 'Have you met ' + me + '? Kind as anything.']
    : repShip('spirit') === 'high' ? ['You see ' + me + ' at everything these days.', me + ' never misses a quiz night.'] : null;
  if (say && SOC.crew.length) newsAdd({ id: 'rep:' + d, about: 'you', kind: 'rep', weight: .5, life: 5, born: h * 60 + 30, seed: socPick(SOC.crew.filter(p => works.includes(p.id) || relTier(p.id) >= 2), 3, d, d, 652).map(p => p.id), lines: say });
}
// ---- invitations (0.36.26, A7; plans/social-deep-plan.md Part 5) ----
// Each ship day at 07:00 (socialHour), once week 1 allows (socGate('d5')), at most INVITE_MAX invitations are picked:
// first to the day's traditions (eventsOn), from someone colleague-or-better whose plan takes them there, the host first
// (the tradition's invite: { host, odds, line } when section 18 gives one; else its `from`, odds INVITE_ODDS); then
// personal ones from friends (tier 3+, once each every INVITE_GAP days, rel.inviteDay): dinner together, the observatory
// after dark, the lounge, the garden, a game (the voice card's invites, else their habits), at the place their plan has
// them that evening. Each becomes an appointment you accept or decline on the device (socialInvite), and their tap line
// (kind 'invite') until it's said; one not said by 15:00 comes as a short Mail. Keeping one: +3 (appointments) and a
// medium memory (came.<trad> or appt.invite), +2 more for a tradition with the person who asked. SHIP.social.invites
// (saved): [{ day, from, trad, kind, appt, said }]
const INVITE_MAX = 2, INVITE_ODDS = .5, INVITE_PERSONAL = .12, INVITE_GAP = 4;
const INVITE_HABIT = { stargazer: 'observatory', 'lounge-regular': 'lounge', 'garden-lover': 'garden', gardener: 'garden', 'common-room': 'game', music: 'music', 'lingers-at-meals': 'dinner' };
const INVITE_WHERE = { dinner: s => s.act === 'dinner', observatory: s => /observ/i.test(s.room || ''), lounge: s => /lounge/i.test(s.room || ''), garden: s => /garden/i.test(s.room || ''),
  game: s => /common|lounge/i.test(s.room || ''), music: s => /music/i.test(s.room || ''), tiles: s => /common|lounge/i.test(s.room || ''), running: s => /gym/i.test(s.room || ''), gym: s => /gym/i.test(s.room || '') };
const INVITE_ASK = { dinner: 'Eat with me tonight? I\'ll save you a seat.', observatory: 'Come up to the observatory after dark? The view\'s worth it.', lounge: 'Drink in the lounge later? My shout.',
  garden: 'I\'m in the garden this evening. Come and get your hands dirty?', game: 'Fancy a game this evening?', music: 'I\'ll be in the music room tonight. Come and listen?', tiles: 'Tiles tonight? I\'ll go easy on you. Probably.', running: 'Run with me later?', quarters: 'Come round to my quarters tonight, about eight? There\'s something I want to show you.' };
function socInvites(h) {
  const d = Math.floor(h / 24) + 1, I = SHIP.social.invites || (SHIP.social.invites = []), t = h * 60 + 30;
  for (let k = I.length - 1; k >= 0; k--) if (I[k].day < d - 7) I.splice(k, 1);
  if (!socGate('d5') || !SHIP.device || I.some(x => x.day === d)) return;
  let n = 0; const S = schedData();
  const going = (p, id) => planDay(p, d).some(s => s.tag && (s.tag === 'ev-' + id || s.tag.startsWith('ev-' + id + '-')));
  for (const e of typeof eventsOn === 'function' ? eventsOn(d) : []) {
    if (n >= INVITE_MAX || (e.honorees && e.honorees.length)) continue;
    const iv = e.ev && e.ev.invite || {}, odds = isFinite(iv.odds) ? iv.odds : INVITE_ODDS; if (schedU(socHash(e.id), d, 653) >= odds) continue;
    const hostId = iv.host || (SOC.crew.find(q => q.name === (e.ev && e.ev.from)) || {}).id;
    const who = SOC.crew.filter(p => relTier(p.id) >= 2 && going(p, e.id)).sort((a, b) => (b.id === hostId) - (a.id === hostId) || relTier(b.id) - relTier(a.id) || schedU(a.seed, d, 654) - schedU(b.seed, d, 654))[0];
    if (!who) continue;
    const appt = socialInvite({ trad: e.id, day: d, from: who.id }); if (!appt) continue;
    I.push({ day: d, from: who.id, trad: e.id, kind: 'trad', appt, said: false, line: iv.line || (e.ev && e.ev.ask) || null }); n++;
  }
  for (const p of SOC.crew.filter(q => relTier(q.id) >= 3).sort((a, b) => schedU(a.seed, d, 655) - schedU(b.seed, d, 655))) {
    if (n >= INVITE_MAX) break;
    const r = SHIP.rel[p.id]; if ((r.inviteDay || 0) > d - INVITE_GAP || schedU(p.seed, d, 656) >= INVITE_PERSONAL * (warmth(p.id, t) === 'warm' ? 1.5 : 1)) continue;
    const v = typeof VOICE !== 'undefined' && VOICE[p.id], kinds = (v && Array.isArray(v.invites) && v.invites.length ? v.invites : [...new Set((p.habits || []).map(x => INVITE_HABIT[x]).filter(Boolean))]).concat(['dinner']);
    let hit = null;
    const trad = kinds.map(k => (typeof eventsOn === 'function' ? eventsOn(d) : []).find(e => e.id === k && going(p, e.id))).find(Boolean);   // a voice card's invites may name a tradition: they ask you along when they're going
    if (trad && !I.some(x => x.day === d && x.trad === trad.id)) { const appt = socialInvite({ trad: trad.id, day: d, from: p.id }); if (appt) { r.inviteDay = d; I.push({ day: d, from: p.id, trad: trad.id, kind: 'trad', appt, said: false, line: (trad.ev && trad.ev.invite && trad.ev.invite.line) || (trad.ev && trad.ev.ask) || null }); n++; continue; } }
    const bed = S.byId.get(p.bed), at8 = (d - 1) * 1440 + 1200, w8 = planWhere(p, at8);   // close friends ask you round to their quarters (doorOpenFor lets you in)
    if (relTier(p.id) >= 4 && bed && w8 && !w8.moving && (w8.act === 'leisure' || w8.act === 'off') && schedU(p.seed, d, 662) < .3) hit = { k: 'quarters', seg: { from: at8, to: at8 + 45, placeId: bed.id } };
    if (!hit) for (const k of kinds) {
      const test = INVITE_WHERE[k]; if (!test) continue;
      const seg = planDay(p, d).find(s => s.placeId && s.from - (d - 1) * 1440 >= 1020 && s.from - (d - 1) * 1440 < 1320 && (s.act === 'leisure' || s.act === 'dinner') && test({ act: s.act, room: (() => { const pl = S.byId.get(s.placeId); return pl && ((DECKS[pl.deck].rooms || {})[pl.room] || {}).name; })() }));
      if (seg) { hit = { k, seg }; break; }
    }
    if (!hit) continue;
    const appt = socialInvite({ kind: hit.k, day: d, from: p.id, at: hit.seg.from, where: hit.seg.placeId, len: Math.min(60, hit.seg.to - hit.seg.from) }); if (!appt) continue;
    r.inviteDay = d; I.push({ day: d, from: p.id, trad: null, kind: hit.k, appt, said: false, line: null }); n++;
  }
}
const inviteFor = (p, d = SHIP.time.day) => (SHIP.social.invites || []).find(x => x.day === d && x.from === p.id && !x.said && apptList().some(a => a.id === x.appt && a.status === 'asked')) || null;
function inviteLine(p, x) {
  const name = x.trad ? socialFill(p, 'trad', { trad: x.trad }) : null, l = socLine(p, 'invite', { trad: x.trad, kind: x.kind, t: shipNow(), tier: relTier(p.id) });
  return l ? l.text : x.line || (x.trad ? (name || 'Something on') + ' tonight. Come with me? It\'s in your Appointments.' : INVITE_ASK[x.kind] || 'Doing anything tonight? Come and find me.');
}
function socInviteMail(now) {                            // not said in person by 15:00: a short Mail instead (socialTick)
  const d = SHIP.time.day; if (SHIP.time.min < 900) return;
  for (const x of SHIP.social.invites || []) if (x.day === d && !x.said && x.appt) {
    x.said = true; const p = SOC.idx.has(x.from) && SOC.crew[SOC.idx.get(x.from)]; if (!p || !apptList().some(a => a.id === x.appt && a.status === 'asked')) continue;
    if (typeof mailSend === 'function') mailSend({ at: now, from: p.name, subject: x.trad ? 'Tonight?' : 'This evening?', body: inviteLine(p, x) + ' ' + shortName(p) });
  }
}
// ---- bunk visits and notes (0.36.27, A8; plans/social-deep-plan.md Part 5) ----
// Once week 1 is done (socGate('done')), between 19:00 and 21:30, a friend (tier 3+) who's free may drop by your bunk
// room: if you're there and awake, a prompt at the screen's edge ("Rina knocks at the door."); tap it and they come in
// (section 10's crewComeTo(p, placeId, onArrive) walks them to your bunk when it's there and they're on your deck) and
// the card opens with a visit line, or a moment's hint when one is ready. Ignore it and they go with a kind word. If
// you're out, sometimes they leave a note on your bunk instead (SHIP.social.notes, saved; a Mail "A note on your bunk",
// and bunkNote() for section 15's bunk tap). At most one visit or note a ship day (SHIP.social.visitDay), once a friend
// every VISIT_GAP days (rel.visitDay), likelier when they're warm. Visitors leave at 22:00 (quiet hours). On paper
// nobody's plan changes. A kept visit: +3 and a medium visit memory, Kindness +1.
const VISIT_FROM = 1140, VISIT_TO = 1290, VISIT_END = 1320, VISIT_GAP = 5, VISIT_ODDS = .02, NOTE_ODDS = .006;
const VISIT_LINES = ['Thought I\'d see how you\'re settling in.', 'I was passing. Well, I wasn\'t, but I am now.', 'Got a minute? Nothing important. Just fancied the company.',
  'Brought you a tea. It\'s probably cold. The lift was slow.', 'Your bunk\'s tidier than mine. Don\'t tell anyone.'];
const NOTE_LINES = ['Came by to say hello. You were out, saving the ship I expect.', 'Knocked, nobody home. Come and find me tomorrow?', 'Popped round with news. It\'ll keep. Find me!',
  'Was going to drag you to the lounge. Next time.'];
let VISIT = null;                                        // { p, until, inside }
function playerInBunk() {
  if (typeof deckDef === 'undefined' || typeof playerBed !== 'function' || typeof roomAt !== 'function') return false;
  const id = playerBed(), d = deckOf(id), bed = DECKS[d] && (DECKS[d].places || []).find(q => q.id === id); if (!bed || deckDef.num !== d) return false;
  const P = player.obj.position; return roomAt(Math.floor(P.x + OX), Math.floor(P.z + OZ)) === bed.room;
}
function socialVisit(m) {
  const min = SHIP.time.min, day = SHIP.time.day;
  if (VISIT) {
    if (!VISIT.inside && simNow() > VISIT.until) { const p = VISIT.p; seekEnd(); VISIT = null; toast(shortName(p), '"' + ['No answer. I\'ll catch you tomorrow.', 'Must be asleep. Night!', 'Another time, then.'][Math.floor(schedU(p.seed, day, 657) * 3)] + '" They head off.'); }
    if (VISIT && VISIT.inside && (min >= VISIT_END || !CHAT || CHAT.p !== VISIT.p)) { const p = VISIT.p; VISIT = null; if (min >= VISIT_END && CHAT && CHAT.p === p) { chatSay('Is that the time? Quiet hours. Night, ' + chatName() + '.'); setTimeout(() => { if (CHAT && CHAT.p === p) chatClose(); }, 2500); } }
    return;
  }
  if (!socGate('done') || min < VISIT_FROM || min >= VISIT_TO || SHIP.social.visitDay === day || CHAT || SEEK || sleeping) return;
  const home = playerInBunk(); if (schedU(day, m, 658) >= (home ? VISIT_ODDS : NOTE_ODDS)) return;
  const t = shipNow(), who = SOC.crew.filter(p => { const r = SHIP.rel[p.id]; if (!r || r.tier < 3 || (r.visitDay || 0) > day - VISIT_GAP) return false; const w = whereIs(p, t); return w && !w.moving && (w.act === 'leisure' || w.act === 'off'); })
    .sort((a, b) => (typeof momentWantsVisit === 'function' ? momentWantsVisit(b, t) - momentWantsVisit(a, t) : 0) || (warmth(b.id) === 'warm') - (warmth(a.id) === 'warm') || schedU(a.seed, day, 659) - schedU(b.seed, day, 659));
  const p = who[0]; if (!p) return;
  SHIP.social.visitDay = day; relGet(p.id).visitDay = day;
  if (!home) {                                           // you're out: a note on your bunk
    const l = socLine(p, 'note', { t, tier: relTier(p.id) }), text = l ? l.text : NOTE_LINES[Math.floor(schedU(p.seed, day, 660) * NOTE_LINES.length)];
    const N = SHIP.social.notes || (SHIP.social.notes = []); N.push({ from: p.id, day, text, read: false }); if (N.length > 10) N.shift();
    if (typeof mailSend === 'function') mailSend({ at: t, from: p.name, subject: 'A note on your bunk', body: text + ' ' + shortName(p) });
    return;
  }
  const el = seekEl(); el.innerHTML = ''; const b = document.createElement('b'); b.textContent = shortName(p); el.appendChild(b);
  el.appendChild(document.createTextNode(' knocks at the door.')); el.hidden = false;
  SEEK = { p, until: simNow() + SEEK_SECS * 1000, visit: true }; VISIT = { p, until: SEEK.until, inside: false };
}
function visitIn() {                                     // you tapped "knocks at the door": they come in
  const p = VISIT && VISIT.p; if (!p) return;
  VISIT.inside = true; seekEnd();
  const id = playerBed(), open = () => { const t = shipNow(), mo = typeof momentReady === 'function' ? momentReady(p, t) : null, l = mo ? null : socLine(p, 'visit', { t, tier: relTier(p.id), warmth: warmth(p.id) });
    chatOpen(p, false, mo ? null : { text: l ? l.text : VISIT_LINES[Math.floor(schedU(p.seed, Math.floor(t / 60), 661) * VISIT_LINES.length)], kind: 'visit', say: true });
    if (CHAT) CHAT.visit = true; relAdd(p.id, 'visit', REL_PTS.appt); memAdd(p.id, 'visit'); repAdd(null, 0, { kindness: 1 }); };
  const a = typeof DECK_CREW !== 'undefined' && DECK_CREW.find(x => x.p === p);
  if (a && typeof crewComeTo === 'function') { try { crewComeTo(p, id, open, { until: (SHIP.time.day - 1) * 1440 + VISIT_END }); return; } catch (e) { } }   // they walk in; gone by 22:00
  open();
}
function bunkNote() {                                    // section 15's bunk tap: the oldest unread note, marked read, or null
  socInit(); const n = (SHIP.social.notes || []).find(x => !x.read); if (!n) return null;
  n.read = true; const p = SOC.idx.has(n.from) && SOC.crew[SOC.idx.get(n.from)];
  return { from: p ? p.name : n.from, text: n.text };
}
// ---- your own room (0.36.66, A11; plans/social-deep-plan.md Part 5) ----
// Once you're promoted (flag 'promoted') and week 1 is done, a friend's card (tier 3+) has Come over: an appointment
// ('social', host: true, by 'you') at your quarters (a place in your bed's room, not the bed when there's another) at
// 19:30 tonight, or the next half hour 45 minutes on (21:00 at the latest), else tomorrow; section 14's apptReply says
// whether they're free (or offers a later time). They walk there and wait like any appointment (section 14's apptWhere;
// doorOpenFor lets them in); when you come (kept) the card opens with a host line (the engine's 'host' kind, else
// HOST_LINES) and stays till you close it or 22:00, and they keep a 'hosted' memory, +3 for the appointment and +2,
// Kindness +1 and Spirit +1. Once a ship day each (rel.hostDay, saved). Bunk visits come to your quarters already
// (playerBed() is wherever you sleep).
const HOST_FROM = 1170, HOST_LAST = 1260;
const HOST_LINES = ['So this is how the officers live. I could get used to it.', 'Nice place. You\'ve even got a chair that isn\'t a crate.', 'I brought biscuits. House rules: you make the tea.',
  'Look at you, with a door that shuts. Proud of you, you know.', 'Your own window and everything. Don\'t let it go to your head.'];
function hostSpot() {                                     // a place in your quarters for a guest: not the bed when there's another
  if (typeof playerBed !== 'function') return null;
  const id = playerBed(), d = deckOf(id), L = DECKS[d] && DECKS[d].places || [], bed = L.find(q => q.id === id); if (!bed) return null;
  return (L.find(q => q.room === bed.room && q.id !== id && Array.isArray(q.at) && !/bed/.test(q.type || '')) || bed).id;
}
const hostOk = p => typeof flag === 'function' && !!flag('promoted') && socGate('done') && relTier(p.id) >= 3 && !!SHIP.device && Array.isArray(SHIP.device.appts) && !!hostSpot();
function socialHost(p) {                                  // Come over: -> the text they say
  if (!hostOk(p)) return null;
  const r = relGet(p.id), now = shipNow(), day0 = (SHIP.time.day - 1) * 1440, where = hostSpot(), D = SHIP.device;
  let at = day0 + HOST_FROM; if (at < now + 45) at = Math.ceil((now + 45) / 30) * 30; if (at > day0 + HOST_LAST) at = day0 + 1440 + HOST_FROM;
  const a = { id: D.appts.reduce((m, x) => Math.max(m, x.id || 0), 0) + 1, with: [p.id], at, len: 60, where, kind: 'social', status: 'asked', by: 'you', host: true };
  const rp = typeof apptReply === 'function' ? apptReply(p, a) : { answer: 'yes', at };
  r.hostDay = SHIP.time.day;
  if (rp.answer === 'no' || !isFinite(rp.at)) return 'Not tonight, I\'m afraid. Ask me again another night?';
  a.at = rp.at; a.status = 'yes'; D.appts.push(a);
  if (typeof deviceNotify === 'function') deviceNotify({ app: 'appointments', text: shortName(p) + ' is coming over at ' + hhmm(a.at % 1440) + '.', urgent: false });
  return (rp.answer === 'later' ? 'Can\'t then. ' : 'Your place? Go on then. ') + 'See you at ' + hhmm(a.at % 1440) + (a.at >= day0 + 1440 ? ' tomorrow' : '') + '.';
}
function hostCame(a, p) {                                 // a Come over kept: the card opens with their host line
  memAdd(p.id, 'hosted'); relAdd(p.id, 'visit', 2); repAdd(null, 0, { kindness: 1, spirit: 1 }, 'hosted');
  if (CHAT) return;
  const t = shipNow(), l = socLine(p, 'host', { t, tier: relTier(p.id), warmth: warmth(p.id) });
  chatOpen(p, false, { text: l ? l.text : HOST_LINES[Math.floor(schedU(p.seed, Math.floor(t / 60), 667) * HOST_LINES.length)], kind: 'host', say: true });
  if (CHAT) { CHAT.visit = true; VISIT = { p, until: 0, inside: true }; }   // stays till you close it, or 22:00 (socialVisit)
}
// ---- crew come and go (0.36.28, A9; plans/social-deep-plan.md Part 8b) ----
// The roster's reserve (ROSTER_RESERVE, section 9, the crew designer) is in SOC.crew from day one, so affinity, memories
// and the save never change shape; each person's aboard: [fromDay, toDay] (null ends: always) says when they're on the
// ship (socAboard; section 14's aboard(p, d) too, when it knows). Off the ship, they're left out of the hours on paper,
// news and the Crew app. A leaver's transfer is news 10 days ahead ("transferring to the Halcyon": the roster's
// transferTo); a day or two before, anyone who knows you comes to say goodbye (their card's first line, kind 'goodbye':
// 20c's goodbyeMoment(p) when there is one, else the engine's goodbye line, else one built from their heaviest memories
// of you); on the day, a farewell at the shuttle bay at 15:00 (section 18's eventOneOff, booked ten days ahead) and, if you
// didn't say goodbye, a Mail. After, friends write now and then (letters, every two weeks for six weeks, then every six;
// the engine's letter kind, else built from your memories), and they're under "Moved on" in the Crew app
// (SHIP.social.moved, saved). Arrivals are news a week ahead, and new for their first week (newHere: ctx.newHere).
const socP = x => x && x.id ? x : (socInit(), SOC.idx.has(x) ? SOC.crew[SOC.idx.get(x)] : null);   // a person, from a person or an id
const leaveDay = p => { if (typeof crewLeaving === 'function') { try { const v = crewLeaving(p); if (v != null) return v; } catch (e) { } } return Array.isArray(p.aboard) && p.aboard[1] != null ? p.aboard[1] : null; };   // section 14's (the sim picks leavers), else the roster's window
const arriveDay = p => { if (typeof crewArriving === 'function') { try { const v = crewArriving(p); if (v != null) return v; } catch (e) { } } return Array.isArray(p.aboard) && p.aboard[0] != null ? p.aboard[0] : null; };
const socAboard = (p, d = SHIP.time.day) => { if (!p) return false; const a = arriveDay(p), l = leaveDay(p); if ((a != null && d < a) || (l != null && d > l)) return false; return typeof aboard !== 'function' || aboard(p, d); };
const leavingSoon = (x, d = SHIP.time.day, p = socP(x)) => { const l = p && leaveDay(p); return l != null && d <= l && l - d <= 10 ? l - d : null; };
const newHere = (x, d = SHIP.time.day, p = socP(x)) => { const a = p && arriveDay(p); return a != null && a > 1 && d >= a && d - a < 7; };
function socTransfers(h) {                               // 07:00 each ship day (socialHour)
  const d = Math.floor(h / 24) + 1, t = h * 60 + 30, M = SHIP.social.moved || (SHIP.social.moved = []);
  for (const p of SOC.crew) {
    const L = leaveDay(p), A = arriveDay(p); if (L == null && A == null) continue;
    const n = shortName(p), to = p.transferTo ? 'the ' + p.transferTo.replace(/^the /i, '') : 'another ship', near = SOC.crew.filter(q => q !== p && socAboard(q, d) && (q.dept === p.dept || socRoom(q) === socRoom(p)));
    if (L != null && d === L - 10 && typeof eventOneOff === 'function') {   // their farewell at the shuttle bay on the day (section 18 plans it like a tradition, host first): 14:00 on a Sunday (rotation day: the shuttle leaves at 15:00), else 19:45 when the day shift can come (the best turnout on paper)
      try { eventOneOff({ id: 'farewell-' + p.id, name: 'Farewell for ' + shortName(p), day: L, at: weekday(L) === 6 ? [840, 870] : [1185, 1230], venue: 'shuttle-bay', where: [{ deck: 5, room: 'Shuttle bay', types: ['event'] }], host: p.id, hostAnim: 'talk', chance: .2, anim: 'talk',
        ask: weekday(L) === 6 ? 'Coming to see me off at the shuttle? Two o\'clock, before I board.' : 'Coming to see me off at the shuttle tonight? Quarter to eight.', here: 'I\'ll miss this old ship.', thanks: 'You see ' + shortName(p) + ' off at the shuttle bay. Hugs, a few tears, a joke about the coffee.' }); } catch (e) { }
    }
    if (L != null && d === L - 10) newsAdd({ id: 'leaving:' + p.id, about: p.id, kind: 'transfer', weight: .8, life: 10, born: t, seed: socPick(near, 4, p.seed, d, 663).map(q => q.id),
      lines: ['Did you hear? ' + n + '\'s transferring to ' + to + '.', n + ' is leaving us. ' + to[0].toUpperCase() + to.slice(1) + ', in ten days.', 'Ten days and ' + n + '\'s off to ' + to + '. Can you believe it?'] });
    if (A != null && A > 1 && d === A - 7) newsAdd({ id: 'arriving:' + p.id, about: p.id, kind: 'arrival', weight: .6, life: 8, born: t, seed: socPick(SOC.crew.filter(q => q.dept === p.dept && socAboard(q, d)), 3, p.seed, d, 664).map(q => q.id),
      lines: ['We\'ve got a new ' + (p.role || 'crew member').toLowerCase() + ' coming next week.', 'Someone new is joining ' + p.dept + ' next week. ' + n + ', I think.'] });
    if (L != null && d === L && !M.some(x => x.id === p.id && x.day === d)) {
      const r = SHIP.rel[p.id], tier = r ? r.tier : 0, mem = (SHIP.mem[p.id] || []).slice().sort((a, b) => b[2] - a[2]).slice(0, 3).map(m => m[0]);
      M.push({ id: p.id, day: d, tier, mem, letters: 0, next: tier >= 3 ? d + 14 : null });
      if (tier >= 1 && !(r.bye >= d - 2)) SHIP.social.mail.push({ at: (d - 1) * 1440 + 960, from: p.name, subject: 'Sorry I missed you', body: 'Sorry I missed you at the shuttle. ' + byeLine(p, true) + ' ' + shortName(p) });
    }
  }
  for (const x of M) if (x.next && d >= x.next) {           // letters from friends who moved on
    const p = SOC.idx.has(x.id) && SOC.crew[SOC.idx.get(x.id)]; if (!p) { x.next = null; continue; }
    x.letters++; x.next = d + (x.letters < 3 ? 14 : 42);
    const l = socLine(p, 'letter', { t, tier: x.tier, mem: x.mem[0] || null }), thing = x.mem[0] && socialFill(p, 'thing', { mem: x.mem[0] });
    SHIP.social.mail.push({ at: t + 600, from: p.name + (p.transferTo ? ', ' + p.transferTo.replace(/^the /i, 'the ') : ''), subject: ['News from out here', 'Hello from ' + (p.transferTo || 'my new ship'), 'Thinking of the Wren'][x.letters % 3],
      body: (l ? l.text : 'The new ship\'s fine. Bigger, colder, nobody makes tea like Brennan.' + (thing ? ' I still think about ' + thing + '.' : '') + ' Say hello to everyone for me.') + ' ' + shortName(p) });
  }
}
function byeLine(p, mail) {                              // a goodbye that talks about your friendship, from their heaviest memories of you
  const l = socLine(p, 'goodbye', { t: shipNow(), tier: relTier(p.id), mail: !!mail }); if (l) return l.text;
  const things = (SHIP.mem[p.id] || []).slice().sort((a, b) => b[2] - a[2]).map(m => socialFill(p, 'thing', { mem: m[0] })).filter(Boolean).slice(0, 2);
  const tier = relTier(p.id), you = chatName();
  return (tier >= 3 ? 'I\'m going to miss you, ' + you + '. ' : 'I\'m off soon. ') + (things.length ? things.map(x => x[0].toUpperCase() + x.slice(1)).join('. ') + '. I won\'t forget that. ' : '') + (tier >= 3 ? 'Write to me?' : 'Look after the old Wren.');
}
const movedOff = id => (socInit(), (SHIP.social.moved || []).some(x => x.id === socId(id)));   // moved:<id>: they've left the Wren
// ---- leave, missed shifts and being let go (0.61.0, the career engineer; design-doc "Leave, missed shifts and being
// let go", and "One fail state": this is the game's only way to end) ----
// Leave: CAREER.leave days to start, one more every CAREER.every ship days (days 29, 57...), at most CAREER.max held.
// Book a workday from the Schedule until 08:30 that day (careerBook); cancel by then to get it back. A leave day, or a
// sick day (careerSick(d), the hook for an illness system: days in the infirmary never count), is a day off to section
// 14's playerShiftOn, so the shift, its start note and the jobs held for you all treat it as one.
// Missing a shift: a workday without leave where you haven't started by CAREER.missBy (12:30, over half of 09:00-17:00)
// is a big hit to Works and ship-wide work (repAdd: softened near the bottom, pulled to the middle each Sunday); being
// late stays section 20's small dip. Started: in a Works room on Deck 5 (shiftTick's test), or a repair of yours. Your
// first week aboard is a grace (days up to CAREER.grace never count as missed).
// The ladder: CAREER.chiefRun workday shifts missed in a row (days off, leave and sick days neither count nor break
// the run; the user's rule, 0.61.4), or SHIP.rep.ship.work under CAREER.chiefLow (0.61.6), bring the Chief's talk, the
// run again after each worked shift; then, once it's been held,
// SHIP.rep.ship.work under CAREER.captain brings the Captain's reprimand. Each is an occasion (appointment, Mail, meeting), booked at 07:00 on a day its person is on shift (or
// after CAREER.wait days anyway), the Captain's only once the Chief's has been held, so the Mail can say "today". The
// Captain's comes again only once you recover (CAREER.rearm; back to rearm.chief clears both steps). When it's booked, a tip (a warning: shown even with tips off) and up to
// CAREER.worried friends (tier 2+) come and find you, worried. Under CAREER.bottom at the end of a workday, once the
// Captain's reprimand has been held (kept or missed), is a day at the bottom (days off and leave neither count nor
// reset); CAREER.days in a row and you're let go, so it always comes after both talks: the notice day (Mail and tip,
// Calder's last words in her office, friends come to say goodbye), then your last day (no shift; friends find you
// again; they, Torres, Pell and Calder stand with you in the shuttle bay 14:30-15:00, section 14's farewell, where
// the send-off plays), and at 15:00 (or when the send-off ends) the closing card. The save is marked ended (a reload
// shows the card), with New game the only way on.
//   SHIP.career (saved) = { l: leave held, w: grants so far, b: [booked days], s: [sick days], st: 0 | 1 Chief | 2
//   Captain, n: bottom days in a row, on: the last day you started your shift, e: the last day checked for a miss,
//   z: the last day whose end is counted, k: once-only warnings (1 late, 2 missed), ms: missed shifts in a row, ca: 1
//   once the Chief's step has been taken for this run (cleared by a worked shift), q: a step waiting to be booked (1,
//   2), qd: the day it fell due, fl: the goodbye's steps done (1 the notice, 2 the last morning), go: the notice day,
//   f: [who stands with you at the send-off], end }
// The words are head writer 4's (content/meetings/careerChief|careerCaptain|careerLetGo|careerSendoff.meet, the bank
// content/banks/career.lines and each voice's content/career/*.lines).
// Nothing here calls R().
const CAREER = { leave: 3, every: 28, max: 5, bookBy: 510, missBy: 750, grace: 7, hitDept: 6, hitWork: 15, clockIn: 480,   // clockIn: the time clock opens (08:00; the shift is DAY_SHIFT, 09:00-17:00 from 0.44.14)
  chiefRun: 3, chiefLow: 15, captain: 12, clockOut: 1020, earlyOut: 900, autoOut: 1080, clockSeed: 4421, remarkOdds: .5, bottom: 5, rearm: { chief: 40, captain: 25 }, days: 3, worried: 3, sendOff: 4, wait: 3,
  chiefAt: 930, captainAt: 660, letGoAt: 600, sendOffAt: 870, seeOff: ['torres-zeke', 'pell', 'calder'] };
SHIP.career = null;
(() => { const s = SAVED && SAVED.ship && SAVED.ship.career; if (s && typeof s === 'object' && Number.isInteger(s.l)) SHIP.career = careerClean(s); })();
function careerClean(s) {
  const days = a => Array.isArray(a) ? a.filter(Number.isInteger).slice(-8) : [], int = (v, x) => Number.isInteger(v) ? v : x;
  return { l: int(s.l, CAREER.leave), w: int(s.w, 0), b: days(s.b), s: days(s.s), st: int(s.st, 0), n: int(s.n, 0), on: int(s.on, 0), e: int(s.e, 0), z: int(s.z, 0),
    k: int(s.k, 0), ci: int(s.ci, 0), co: int(s.co, 0), rm: int(s.rm, 0), gs: int(s.gs, 0), md: int(s.md, 0), mx: isFinite(s.mx) ? +s.mx : 0, sd: int(s.sd, 0), sh: int(s.sh, 0), ss: int(s.ss, -1), sc: int(s.sc, 0), ms: int(s.ms, 0), ca: int(s.ca, 0), q: int(s.q, 0), qd: int(s.qd, 0), fl: int(s.fl, 0), go: int(s.go, null), f: Array.isArray(s.f) ? s.f.filter(x => typeof x === 'string').slice(0, 8) : [], end: !!s.end };
}
SAVE_EXTRA.push(s => { if (SHIP.career) s.ship.career = SHIP.career; });
onSim('newGame', () => { SHIP.career = null; careerCard(false); });
function careerInit(now = shipNow()) {
  if (SHIP.career) return SHIP.career;
  const d = Math.floor(now / 1440) + 1, m = now - (d - 1) * 1440;   // an older save starts here: no back pay of leave, no misses before today
  const sent = simNotes('shiftStart').filter(n => Math.floor(n.t / 1440) + 1 === d), on = (sent.length ? sent.some(n => !n.missed) : flag('shiftSent') === d) ? d : 0;   // already started today (reviewer 1d)
  return SHIP.career = { l: CAREER.leave, w: Math.max(0, Math.floor((d - 1) / CAREER.every)), b: [], s: [], st: 0, n: 0, on, e: m >= CAREER.missBy ? d : d - 1, z: d - 1, k: 0, ci: 0, co: 0, rm: 0, gs: NOSAVE ? 0 : (Date.now() ^ Math.floor(Math.random() * 2147483647)) | 0, md: 0, mx: 0, sd: 0, sh: 0, ss: -1, sc: 0, ms: 0, ca: 0, q: 0, qd: 0, fl: 0, go: null, f: [], end: false };
}
const careerWork = () => SHIP.rep && SHIP.rep.ship && isFinite(SHIP.rep.ship.work) ? SHIP.rep.ship.work : 50;
const careerRota = d => { try { return isWorkDay(ROSTER_PLAYER, d); } catch (e) { return weekday(d) < 5; } };   // your rota alone (playerShiftOn without leave)
const careerOn = d => !!SHIP.career && SHIP.career.b.includes(d);   // a booked leave day
function careerSick(d, on = true) {                      // a sick day: excused (a booked leave day comes back; a miss already counted is undone)
  const c = careerInit(); c.s = c.s.filter(x => x !== d); if (!on) return; c.s.push(d); c.s = c.s.slice(-8);
  if (c.b.includes(d)) { c.b = c.b.filter(x => x !== d); c.l++; }
  if (c.md > 0 && c.md === d) { c.md = 0; c.ms = Math.max(0, c.ms - 1); repAdd('works', CAREER.hitDept, null, 'sickNote'); if (SHIP.rep && SHIP.rep.ship) SHIP.rep.ship.work = Math.min(100, careerWork() + (c.mx || 0)); }   // reviewer 1d: the work it took, not more
}
function careerOff(d) {                                  // no shift that day: leave, sick, or let go (section 14's playerShiftOn asks)
  const c = SHIP.career; return !!c && (c.b.includes(d) || c.s.includes(d) || (c.go != null && d >= c.go));
}
const careerDeadline = d => (d - 1) * 1440 + CAREER.bookBy;
function careerCanBook(d, now = shipNow()) {             // 'book', 'cancel' or null
  const c = careerInit(); if (c.go != null || now >= careerDeadline(d) || !careerRota(d) || c.s.includes(d)) return null;
  return c.b.includes(d) ? 'cancel' : c.l > 0 ? 'book' : null;
}
function careerBook(d, now = shipNow()) {                // the Schedule's button: book a leave day, or cancel one
  const c = careerInit(), can = careerCanBook(d, now); if (!can) return false;
  if (can === 'book') { c.l--; c.b.push(d); c.b = c.b.filter(x => x >= SHIP.time.day - 1); } else { c.b = c.b.filter(x => x !== d); c.l++; }   // back, even at the cap: it was earned
  simNote('leave', { day: d, booked: can === 'book' });
  return true;
}
function careerText(kind, k = 0) {                       // a text from content (tips, Mail, the card; variant k), {me} filled, or null
  const L = typeof LINES !== 'undefined' && LINES[kind], e = Array.isArray(L) && L.length ? L[k % L.length] : null;
  return e && typeof e.text === 'string' ? e.text.replace(/\{me\}/g, () => chatName()) : null;
}
const careerSplit = (kind, from) => { const t = careerText(kind) || '', i = t.indexOf(' | '); return i < 0 ? null : { from, subject: t.slice(0, i), body: t.slice(i + 3) }; };
function careerTip(key) {                                // a warning: shown even with tips off (like the low-need ones); once a save (0.72.5, playtest 2 item 17: "green tips shouldn't repeat")
  const text = careerText('career.tip.' + key), id = 'career.' + key, seen = typeof SHIP.device !== 'undefined' && SHIP.device && SHIP.device.tipsSeen;
  if (!text || typeof TIP_Q === 'undefined' || typeof DEVICE_SKIN === 'undefined' || TIP_Q.some(x => x.id === id) || seen && seen[id]) return false;
  if (seen) seen[id] = true;   // the device's saved tipsSeen, as every other tip
  TIP_Q.push({ id, text }); if (TIP_Q.length === 1) DEVICE_SKIN.tip(TIP_Q[0]); return true;
}
function careerFriends(n) {                              // your friends aboard (tier 2+), closest first
  socInit(); return SOC.crew.filter(p => relTier(p.id) >= 2 && socAboard(p) && p.rank !== 'guest').sort((a, b) => (SHIP.rel[b.id].pts || 0) - (SHIP.rel[a.id].pts || 0) || (a.id < b.id ? -1 : 1)).slice(0, n);
}
function careerSeek(why, from, until, n) { for (const p of careerFriends(n)) socialSeekAsk(p.id, { from, until, why: 'career:' + why }); }
function careerSeekLine(p, why) {                        // the chip's line when a career ask finds you (section 20's seekShow)
  const k = /^career:(\w+)$/.exec(why || ''); if (!k) return null;
  const kind = k[1] === 'eve' || k[1] === 'day' ? 'farewell.' + k[1] : k[1] === 'nudge' ? 'sick.nudge' : 'worried.' + k[1], l = socLine(p, kind, { t: shipNow(), tier: relTier(p.id) });
  return l ? { text: l.text, kind, say: true } : null;
}
const careerHeld = (id, now) => { const r = SHIP.occasions.filter(x => x.id === id).pop(); return !!r && now >= r.at + r.len; };   // its latest one is over (kept or missed)
function careerDue(now) {                                // a step waiting: booked at 07:00 on a day its person is on shift, the Captain's after the Chief's
  const c = SHIP.career, d = Math.floor(now / 1440) + 1, m = now - (d - 1) * 1440; if (!c.q || c.go != null) return;
  const step = c.q === 1 ? 'chief' : 'captain', id = c.q === 1 ? 'careerChief' : 'careerCaptain', o = OCCASIONS[id];
  if (m < 420 || m > o.at - 30 || !playerShiftOn(d) || (!occOnShift(o.by, d) && d < c.qd + CAREER.wait) || (c.q === 2 && !careerHeld('careerChief', now))) return;   // only on your workdays (reviewer 1d)
  o.mail = careerSplit('career.mail.' + step, c.q === 1 ? 'Chief Ines Calder' : 'Commander Teo Vance');
  occasionAdd(id, (d - 1) * 1440 + o.at); c.q = 0;
  careerTip(step); careerSeek(step, now + 60, now + 1440, CAREER.worried);
  simNote('careerStep', { step });
}
OCCASIONS.careerChief = { title: 'A word with the Chief', kind: 'summons', by: 'calder', deck: 5, room: 'o', at: CAREER.chiefAt, len: 20, script: 'careerChief', due: () => false, mail: null };
OCCASIONS.careerCaptain = { title: 'The Captain\'s ready room', kind: 'summons', by: 'marrow', deck: 1, room: 'R', at: CAREER.captainAt, len: 20, script: 'careerCaptain', due: () => false, mail: null };
OCCASIONS.careerLetGo = { title: 'The Chief\'s office', kind: 'summons', by: 'calder', deck: 5, room: 'o', at: CAREER.letGoAt, len: 20, script: 'careerLetGo', due: () => false, mail: null };
OCCASIONS.careerSendoff = { title: 'Your send-off', kind: 'meeting', by: 'torres-zeke', with: ['pell', 'calder'], deck: 5, room: 'S', at: CAREER.sendOffAt, len: 30, script: 'careerSendoff', due: () => false, mail: null };
// ---- the bridge, by invitation (Pillar 5 Step 3, the user's): until you're invited (SHIP.bridgeInvited, saved; old
// saves false, or true if they already hold bridge.invited), the bridge itself is shut to you. Only you: the crew come and go
// as before, and the lobby, the washroom, the observation room and Deck 1's other hatches are as they were. The doors stay shut as
// you come up (bridgeBarred, asked by the deck architect's YOU_LOCKS[1] in section 4's edgeBlocks and section 11's door loop,
// 0.47.12), a tap on them or walking up to them says why (bridgeDoorTap, YOU_LOCKS' tap; BRIDGE_LOCK.near), and an appointment or job in there or in
// the ready room behind it still lets you through (doorOpenFor). The invite: Vance's chance meeting (OCCASIONS.bridgeInvite,
// the day before a bridge hour) once the first ship-wide event has ended (SHIP.eventLog), or from BRIDGE_LOCK.standIn in a
// build with no events; it sets bridge.invited, which opens bridge hour's gate, and SHIP.bridgeInvited follows it.
// Words: the head writer's bridge.locked (the door) and bridgeInvite (the meeting). Section 17 (S2) reads
// SHIP.bridgeInvited to keep bridge-room jobs off your board until then.
const BRIDGE_LOCK = { deck: 1, room: 'B', behind: ['R'], standIn: 15, near: 1.3 };
SHIP.bridgeInvited = (() => { const s = SAVED && SAVED.ship; return !!(s && s.bridgeInvited === true) || !!(s && s.flags && s.flags['bridge.invited']); })();
SAVE_EXTRA.push(s => { s.ship.bridgeInvited = !!SHIP.bridgeInvited; });
const bridgeInviteReady = d => (SHIP.eventLog || []).some(e => e.endDay < d) || (!EVENT_ORDER.some(id => SHIP_EVENTS[id]) && d >= BRIDGE_LOCK.standIn);
function bridgeBarred(e) {                               // is this door shut to you? A door or hatch into the bridge while you're not invited
  // (SHIP.bridgeInvited is false only once this section has set it at load), the crawl's hatch up by the Works station
  // too, or the relay room and the crawl would be a way round
  if (SHIP.bridgeInvited !== false || !e || (e.type !== 'door' && e.type !== 'hatch') || typeof deckDef === 'undefined' || deckDef.num !== BRIDGE_LOCK.deck) return false;
  const rs = edgeTiles(e.key).map(c => roomAt(...c)); if (!rs.includes(BRIDGE_LOCK.room) || rs.every(r => r === BRIDGE_LOCK.room)) return false;
  try { if (roomAt(...player.here()) === BRIDGE_LOCK.room) return false; } catch (x) { /* no player yet */ }   // already in there (an old save, a summons that ran over): never shut in
  return ![BRIDGE_LOCK.room, ...BRIDGE_LOCK.behind].some(r => doorOpenFor(r, 'player'));
}
const bridgeLockedText = () => careerText('bridge.locked') || 'The bridge. The duty crew only: you need the Captain\'s permission to go in.';
function bridgeDoorTap(key) {                            // the deck architect's door tap: { t, x } for a shut bridge door, else null
  return bridgeBarred(EDGES.get(key)) ? { t: 'Bridge', x: bridgeLockedText() } : null;
}
let BRIDGE_SAID = 0;                                     // walking up to the shut doors says it once a visit to Deck 1
function bridgeTick(now) {
  if (!SHIP.bridgeInvited && flag('bridge.invited')) SHIP.bridgeInvited = true;
  if (SHIP.bridgeInvited || typeof deckDef === 'undefined' || deckDef.num !== BRIDGE_LOCK.deck || typeof player === 'undefined') { BRIDGE_SAID = 0; return; }
  if (BRIDGE_SAID) return;
  const p = player.obj.position;
  for (const e of EDGES.values()) if (bridgeBarred(e) && Math.hypot(p.x - e.cx, p.z - e.cz) < BRIDGE_LOCK.near) { BRIDGE_SAID = now; toast('Bridge', bridgeLockedText()); return; }
}
SIM_ADVANCE.push((from, to) => bridgeTick(to));
function careerStarted(t) {                              // you started your shift (from 08:00, CAREER.clockIn, until it counts as missed)
  const c = careerInit(), d = Math.floor(t / 1440) + 1, m = t - (d - 1) * 1440; if (m >= CAREER.clockIn && m < CAREER.missBy) c.on = d;
}
onSim('shiftStart', n => { if (!n.missed) careerStarted(n.t); else return;
  const c = careerInit(); if (n.late >= 20 && !(c.k & 1)) { c.k |= 1; careerTip('late'); } });
onSim('repair', n => { if (n.who === 'you' && Math.floor(n.t / 1440) + 1 <= CAREER.grace) careerStarted(n.t); });   // a repair starts your day only in your first week; after that, the clock (reviewer 1e)
// at work: clocked in at the time clock (0.61.13, the user's); in your first week (the grace) being in a Works room on Deck
// 5 still counts, while you learn the clock (section 14's shiftTick asks this too)
function careerAtWork() {
  if (careerClockedIn()) return true; if (SHIP.time.day > CAREER.grace) return false;
  try { return deckDef.num === 5 && (DECKS[5].places || []).some(pl => pl.type === 'work:works' && pl.room === roomAt(...player.here())); } catch (e) { return false; }
}
// ---- the time clock (0.61.13, the user's: "clock in and out for work... something on the wall"): on the Works bay's
// north wall past the tool wall, by the tea corner door, along from the job board (WALL_KIT.timeClock, place 5-timeclock-1, where the Works crew stop at the start and end of their
// shift). Tap it to clock in (ci) and later out (co). Clocking in from 08:00 (CAREER.clockIn) starts your shift (careerStarted: late
// after 09:00, DAY_SHIFT[0], missed if not by 12:30); forget to clock out and it signs you out at 17:00 (after CAREER.autoOut), no
// harm done. Leave and sick days need none. About one time in two a Works crew member near you says something
// (clock.in / out / monday / friday / back / late, from content; careerRemark). The Schedule shows today's hours.
const careerClockedIn = (d = SHIP.time.day) => !!SHIP.career && SHIP.career.ci > 0 && Math.floor(SHIP.career.ci / 1440) + 1 === d;
const careerClockedOut = (d = SHIP.time.day) => careerClockedIn(d) && SHIP.career.co > SHIP.career.ci;
const careerFullDay = d => d <= CAREER.grace || !careerClockedIn(d) || !careerClockedOut(d) || SHIP.career.co % 1440 >= CAREER.earlyOut;   // not a short shift (no clock record: the first week, or on paper)
function careerClock(now = shipNow(), quiet) {           // -> 'in' | 'out' | null, with a toast (quiet: the time clock's screen says it instead, 0.28.63)
  const toast = quiet ? () => {} : TOAST_FN;
  const c = careerInit(now), d = Math.floor(now / 1440) + 1, m = now - (d - 1) * 1440;
  if (!playerShiftOn(d)) { toast('Time clock', careerOn(d) ? 'You\'re on leave today. No need to clock in.' : sickToday(d) ? 'You\'re off sick. No need to clock in.' : 'No shift today. The clock can wait.'); return null; }
  if (!careerClockedIn(d)) {
    if (m >= CAREER.clockOut) { toast('Time clock', 'The day shift is over. See you tomorrow.'); return null; }
    if (m < CAREER.clockIn) { toast('Time clock', 'Too early: the clock opens at 08:00. The shift starts at 09:00.'); return null; }   // reviewer 1e
    c.ci = Math.floor(now); c.co = 0; careerStarted(now); toast('Time clock', 'Clocked in at ' + hhmm(m) + '.');
    careerRemark('in', now, m - DAY_SHIFT[0]); simNote('clock', { what: 'in' }); return 'in';
  }
  if (careerClockedOut(d)) { toast('Time clock', 'You\'re clocked out for the day.'); return null; }
  c.co = Math.floor(now); const h = c.co - c.ci, early = m < CAREER.earlyOut;
  if (SHIP.player.clockLog) SHIP.player.clockLog[d] = h;   // every clock-out counts for the screen's hours (0.28.65, reviewer 0607)
  if (early) repAdd(null, 0, { work: -2 }, 'early');   // a short shift: a small dip, like being late, never a missed shift (the user's choice, 0.61.18)
  toast('Time clock', 'Clocked out at ' + hhmm(m) + '. ' + Math.floor(h / 60) + 'h ' + String(h % 60).padStart(2, '0') + 'm today.' + (early ? ' An early finish: it\'s noted.' : ''));
  careerRemark(early ? 'early' : 'out', now); simNote('clock', { what: 'out' }); return 'out';
}
function careerClockTap(it, at) {                        // section 15's PLAYER_TAPS: walk up to the clock and use it
  if (it.t !== 'Time clock' || typeof approach !== 'function') return false;
  approach(at.clone(), it.front, it.depth, () => clockScreen()); return true;   // its screen (0.28.63, the user's: in the device's style)
}
// ---- the time clock's screen (0.28.63, the user's "a device-style pop-up screen at the time clock: clock in / clock out
// / your hours"): the device's phosphor look, in the strip at the foot of the screen. What's on today, Clock in or Clock
// out (out before CAREER.earlyOut asks first), your hours today and this week. careerClock does the clocking (quiet).
// SHIP.player.clockLog = { day: minutes } for the last 14 days, saved. Words: the head writer's clock.screen.*
const TOAST_FN = (...a) => toast(...a);
const csText = (k, fb, ctx) => { let t = null; try { t = careerText('clock.screen.' + k); } catch (e) { t = null; } t = t || fb; for (const x in ctx || {}) t = t.split('{' + x + '}').join(ctx[x]); return t; };
SHIP.player.clockLog = (() => { const l = SAVED && SAVED.player && SAVED.player.clockLog, out = {}; if (l && typeof l === 'object') for (const k in l) if (/^\d+$/.test(k) && Number.isFinite(l[k]) && l[k] >= 0) out[k] = Math.min(1440, Math.floor(l[k])); return out; })();
SAVE_EXTRA.push(s => { const L = SHIP.player.clockLog, d = SHIP.time.day; for (const k in L) if (+k < d - 14) delete L[k]; (s.player || (s.player = {})).clockLog = { ...L }; });
const hrs = mins => (Math.round(mins / 6) / 10).toString();
function clockScreen(said, ask) {
  let el = document.getElementById('clockScreen');
  if (!el) {
    el = document.createElement('div'); el.id = 'clockScreen'; el.className = 'devdlg'; el.setAttribute('role', 'dialog'); el.setAttribute('aria-label', 'Time clock');
    el.addEventListener('pointerdown', e => e.stopPropagation()); document.body.appendChild(el);
    addEventListener('keydown', e => { if (e.key === 'Escape' && !el.hidden) el.hidden = true; });
  }
  const now = shipNow(), d = SHIP.time.day, m = SHIP.time.min, C = SHIP.career, mk = (t, c, x) => { const e = document.createElement(t); if (c) e.className = c; if (x !== undefined) e.textContent = x; return e; };
  const on = playerShiftOn(d), inn = careerClockedIn(d), out = careerClockedOut(d), wd = weekday(d);
  const st = said || (!on ? (careerOn(d) ? csText('leave', 'On leave today. Enjoy it.') : sickToday(d) ? csText('sick', 'Off sick. Get well.') : csText('offday', 'Day off. No clocking today.'))
    : out ? (wd === 4 ? csText('weekend', 'Shift done. See you Monday.') : csText('done', 'Shift done. See you tomorrow.')) : inn ? csText('onshift', 'On shift since {time}.', { time: hhmm(C.ci % 1440) })
    : m >= CAREER.clockOut ? csText('done', 'Shift done. See you tomorrow.') : csText('ready', 'Shift starts at {time}. Tap to clock in.', { time: hhmm(DAY_SHIFT[0]) }));
  el.dataset.ph = SHIP.device.settings.phosphor; el.textContent = ''; el.hidden = false;
  const x = mk('button', 'x', '×'); x.type = 'button'; x.setAttribute('aria-label', csText('close', 'Close')); x.onclick = e => { e.stopPropagation(); el.hidden = true; };
  el.append(x, mk('small', '', csText('title', 'WORKS TIME CLOCK') + ' · ' + csText('sub', 'CSV Wren · Works bay')), mk('p', '', ask ? csText('early', 'Before 17:00. Clock out early?') : st));
  const today = inn ? (out ? C.co : Math.floor(now)) - C.ci : 0;
  let week = today; for (let k = d - wd; k < d; k++) week += SHIP.player.clockLog[k] || 0;
  el.append(mk('small', '', csText('hours', 'YOUR HOURS')), mk('p', '', csText('today', 'Today: {hours} h', { hours: hrs(today) }) + ' · ' + csText('week', 'This week: {hours} h', { hours: hrs(week) })));
  const row = mk('div', 'btns'), act = (label, f) => { const b = mk('button', 'act', label); b.type = 'button'; b.onclick = e => { e.stopPropagation(); f(); }; row.appendChild(b); return b; };
  if (on && !out && !(inn ? false : m >= CAREER.clockOut || m < CAREER.clockIn)) {
    if (!inn) act(csText('in', 'Clock in'), () => { const r = careerClock(shipNow(), true); clockScreen(r ? (SHIP.time.min - DAY_SHIFT[0] > 5 ? csText('late', 'Clocked in at {time}. A little late. It happens.', { time: hhmm(SHIP.time.min) }) : csText('didin', 'Clocked in at {time}. Have a good shift.', { time: hhmm(SHIP.time.min) })) : null); });
    else if (SHIP.time.min < CAREER.clockOut && !ask) act(csText('out', 'Clock out'), () => clockScreen(null, true));   // before the shift ends (17:00): asks first
    else act(csText('out', 'Clock out'), () => { const r = careerClock(shipNow(), true); clockScreen(r ? csText('didout', 'Clocked out at {time}. Evening\'s yours.', { time: hhmm(SHIP.time.min) }) : null); });
  }
  act(csText('close', 'Close'), () => { el.hidden = true; }).classList.add('next');
  el.appendChild(row);
  try { (row.querySelector('button') || x).focus(); } catch (e) { /* no focus */ }
}
if (typeof PLAYER_TAPS !== 'undefined') PLAYER_TAPS.unshift(careerClockTap);
// ---- reputation you can see (0.61.15, the user's: "when you complete a job, rep goes up a little; we need a visual
// indication"): when you turn a job in, a small chip floats up from you, "+ Works reputation" in the department's
// colour (section 15's needFloat; words only, never numbers), and the Record app gets a quiet mark once until you look.
// One at a time (REP_CHIP_GAP real seconds apart), and none while a conversation or a meeting is on screen. A repair is
// scored by section 20 (repNote 'repair'); any other job you turn in (a restock, a chore, a run) now counts a little too
const REP_CHIP_GAP = 8, REP_DEPT_COL = { works: '#f0b24a', galley: '#e98b5a', garden: '#8fd08a', infirmary: '#8fd3e8', store: '#d9b3f0', command: '#e9e2c8',
  helm: '#9bb8ff', comms: '#9be0c8', watch: '#c8c0ff', survey: '#ffd27f' };
let REP_CHIP_AT = -1e9;
function careerJobIn(n) {
  if (!n || n.step !== 'turnin') return;
  const m = n.machine && typeof machineById === 'function' ? machineById(n.machine) : null, dept = m && typeof repDeptOf === 'function' ? repDeptOf(m) : 'works';
  if (!n.machine && typeof repAdd === 'function') repAdd(dept, 1, { work: 1 }, 'jobs');   // a job with no machine: section 20 has no repair for it
  const j = (SHIP.jobs || []).find(x => x.id === n.id);   // Step 3 (0.44.22, the user's): the HUD engineer's turn-in card reads j.gains (it runs after turnInJob, which flushes this note)
  if (j) { const g = j.gains || (j.gains = {});
    const R = g.rep || (g.rep = []); if (!R.some(x => x.dept === dept)) R.push({ dept, name: worksText('works.turnin.rep', '{dept} reputation', { dept: dept[0].toUpperCase() + dept.slice(1) }) });   // words only, never a number (0.61.15); once a department, however often the note comes
    if (!g.meters && Array.isArray(j.meters)) g.meters = j.meters.filter(m => m && m.gain > 0).map(m => ({ sys: m.key, name: m.name, add: m.gain })); }   // the systems engineer's points per ship meter (0.33.57)
  if (typeof turnInShow === 'function') { if (typeof DEV !== 'undefined' && DEV.notes && !DEV.notes.record) DEV.notes.record = 1; return; }   // the card says it: no chip as well
  const now = performance.now(); if (now - REP_CHIP_AT < REP_CHIP_GAP * 1000 || (typeof DIALOGUE !== 'undefined' && DIALOGUE) || CHAT || typeof needFloat !== 'function') return;
  REP_CHIP_AT = now; needFloat('+ ' + dept[0].toUpperCase() + dept.slice(1) + ' reputation');
  const f = typeof FLOATS !== 'undefined' && FLOATS[FLOATS.length - 1]; if (f && f[0]) { f[0].style.color = REP_DEPT_COL[dept] || ''; f[0].style.borderColor = REP_DEPT_COL[dept] || ''; }
  if (typeof DEV !== 'undefined' && DEV.notes && !DEV.notes.record) DEV.notes.record = 1;   // the Record's badge, once until you look
}
onSim('job', careerJobIn);
const CLOCK_SAID = {};                                   // what -> the day a remark was last said (one each way a day)
function careerBack(d) {                                 // your last workday before d was leave or sick
  const c = SHIP.career; for (let k = d - 1; k >= d - 10 && k > 0; k--) if (careerRota(k)) return c.b.includes(k) || c.s.includes(k); return false;
}
function careerRemark(what, now, late = 0) {             // a Works crew member near you says something, about one time in two
  if (typeof DECK_CREW === 'undefined' || typeof bubbleSay !== 'function') return null;
  const d = Math.floor(now / 1440) + 1; if (CLOCK_SAID[what] === d || schedU(CAREER.clockSeed, Math.floor(now), what === 'in' ? 951 : 952) >= CAREER.remarkOdds) return null;
  const P = player.obj.position, dist = x => Math.hypot(x.x - P.x, x.z - P.z);
  const a = DECK_CREW.filter(x => x.p && x.p.dept === 'works' && dist(x) < 5).sort((x, y) => dist(x) - dist(y))[0]; if (!a) return null;
  const wd = weekday(d), kinds = what === 'in' ? [careerBack(d) && 'clock.back', late >= 20 && 'clock.late', wd === 0 && 'clock.monday', 'clock.in'] : what === 'early' ? ['clock.early', 'clock.out'] : [wd === 4 && 'clock.friday', 'clock.out'];
  for (const k of kinds.filter(Boolean)) { const l = socLine(a.p, k, { t: now, tier: relTier(a.p.id) }); if (l) { CLOCK_SAID[what] = d; bubbleSay(a.h, l.text); return k; } }
  return null;
}
function careerMissed(d) {
  const w0 = careerWork(); repAdd('works', -CAREER.hitDept, { work: -CAREER.hitWork }, 'missed');
  const c = careerInit(); c.md = d; c.mx = Math.round((w0 - careerWork()) * 100) / 100;   // what it took, so a sick note gives back exactly that
  if (!(c.k & 2)) { c.k |= 2; careerTip('missed'); }
  simNote('shiftMissed', { day: d });
}
function careerDayEnd(d, now) {                          // a workday ends: at the bottom (after the Captain) or not
  const c = careerInit(); if (c.go != null || !careerRota(d) || careerOff(d)) return;
  if (c.on === d && careerFullDay(d)) { c.ms = 0; c.ca = 0; }   // a full day's work (a short shift, out before 15:00, counts neither way: the user's choice, 0.61.18)
  c.n = c.st >= 2 && !c.q && careerHeld('careerCaptain', now) && careerWork() < CAREER.bottom ? c.n + 1 : 0;   // only once the reprimand has been held
  if (c.n === 1) { careerTip('bottom'); careerSeek('last', now, now + 1440, CAREER.worried); }
  if (c.n >= CAREER.days) careerLetGo(d + 1, now);
}
function careerLadder(now) {
  const c = careerInit(), w = careerWork();
  const st = c.st; if (c.st >= 1 && w >= CAREER.rearm.chief) c.st = 0; else if (c.st >= 2 && w >= CAREER.rearm.captain) c.st = 1;   // recovered: the steps come again
  if (c.st < st) { if (c.q > c.st) c.q = 0; careerTip('up'); }
  if (c.go != null || c.q) return;                       // a step waiting is booked by careerDue
  const d = Math.floor(now / 1440) + 1;
  if (c.st <= 1 && !c.ca && (c.ms >= CAREER.chiefRun || (c.st === 0 && w < CAREER.chiefLow))) { c.ca = 1; c.st = 1; c.q = 1; c.qd = d; }   // the Chief: missed shifts in a row (0.61.4), or work under chiefLow (0.61.6; the user's rules)
  else if (c.st === 1 && w < CAREER.captain && careerHeld('careerChief', now)) { c.st = 2; c.q = 2; c.qd = d; }   // the Captain: very low standing, after the Chief's talk
}
function careerLetGo(d, now) {                           // notice on day d, the last day d + 1
  const c = careerInit(), see = CAREER.seeOff.filter(id => { const p = socP(id); return p && socAboard(p, d + 1); });
  c.go = d; c.f = [...new Set(careerFriends(CAREER.sendOff).map(p => p.id).concat(see))];
  c.b = []; c.n = 0; c.q = 0;                             // booked leave is moot now
  occasionAdd('careerLetGo', (d - 1) * 1440 + CAREER.letGoAt); occasionAdd('careerSendoff', d * 1440 + CAREER.sendOffAt);   // Calder's last words; the shuttle bay
  if (typeof SHIP_DAYS !== 'undefined') { SCHED_DATA = null; SHIP_DAYS.clear(); }   // the last day's plans pick up the send-off (as section 18's eventOneOff does)
  simNote('letGo', { day: d + 1 });
}
const careerSendOff = d => SHIP.career && SHIP.career.go != null && d === SHIP.career.go + 1 && !SHIP.career.end ? SHIP.career.f : [];   // section 14's farewell friends for you
function careerGoTick(now) {                             // the notice, the last day and the shuttle
  const c = SHIP.career; if (!c || c.go == null || c.end) return;
  const d = Math.floor(now / 1440) + 1, m = now - (d - 1) * 1440, L = c.go + 1;
  if (d >= c.go && m >= 420 && !(c.fl & 1)) { c.fl |= 1;  // 07:00 on notice day: Mail, the warning, friends come to say goodbye
    const ml = careerSplit('career.mail.notice', 'Chief Ines Calder'); if (ml && typeof mailSend === 'function') mailSend({ at: Math.min(now, (c.go - 1) * 1440 + 420), ...ml });
    careerTip('notice'); careerSeek('eve', now, (c.go - 1) * 1440 + 1320, CAREER.sendOff);
  }
  if (d >= L && m >= 420 && !(c.fl & 2)) { c.fl |= 2; careerSeek('day', now, (L - 1) * 1440 + 870, CAREER.sendOff); }
  const off = (L - 1) * 1440 + ROTA_OFF, saying = typeof DIALOGUE !== 'undefined' && DIALOGUE && DIALOGUE.id === 'careerSendoff';
  if (now >= off && (!saying || now >= off + 30)) {     // the shuttle leaves at 15:00, once the send-off is said
    c.end = true; simNote('careerEnd', { day: L }); saveGame(); careerCard(true);
  }
}
// once a ship minute (section 13's tickShip) and after a skip: leave earned, today's start, the misses and day ends
// passed, the ladder and the goodbye
function careerTick(now = shipNow()) {
  const c = careerInit(now); if (c.end) return;
  const d = Math.floor(now / 1440) + 1, m = now - (d - 1) * 1440;
  const g = Math.max(0, Math.floor((d - 1) / CAREER.every)); while (c.w < g) { c.w++; c.l = Math.min(CAREER.max, c.l + 1); }
  if (c.on !== d && m >= CAREER.clockIn && m < CAREER.missBy && careerRota(d) && !careerOff(d) && careerAtWork()) c.on = d;
  if (c.ci > 0 && !(c.co > c.ci)) { const cd = Math.floor(c.ci / 1440) + 1;   // forgot to clock out: signed out at 17:00, no harm done
    if (cd < d || m >= CAREER.autoOut) { c.co = (cd - 1) * 1440 + CAREER.clockOut; if (SHIP.player.clockLog) SHIP.player.clockLog[cd] = c.co - c.ci; if (cd === d) toast('Time clock', careerText('clock.auto', d) || 'You forgot to clock out. The clock signed you out at 17:00.'); } }   // the auto clock-out counts for the time clock screen's hours too (0.28.65)
  if (c.rm !== d && d > CAREER.grace && m >= CAREER.clockIn && m < CAREER.clockOut && playerShiftOn(d) && !careerClockedIn(d)) {   // in the Works bay, not clocked in: a reminder, once a day
    let inBay = false; try { inBay = deckDef.num === 5 && roomAt(...player.here()) === 'w'; } catch (e) { inBay = false; }
    if (inBay) { c.rm = d; toast('Time clock', 'Don\'t forget to clock in: the time clock is past the tool wall, by the tea corner.'); }
  }
  if (!(c.k & 8) && m >= CAREER.clockIn && playerShiftOn(d)) { let inBay = false; try { inBay = deckDef.num === 5 && roomAt(...player.here()) === 'w'; } catch (e) { inBay = false; }
    if (inBay && typeof tipShow === 'function') { c.k |= 8; tipShow('career.clock', careerText('career.tip.clock') || 'Clock in at the time clock in the Works bay (past the tool wall) when your shift starts, and out when it ends. Leave and sick days need none.'); } }
  for (let k = Math.min(c.e, c.z) + 1; k <= d; k++) {
    if (c.e < k && (k < d || m >= CAREER.missBy)) { c.e = k; if (k > CAREER.grace && careerRota(k) && !careerOff(k) && c.on !== k) { c.ms++; careerMissed(k); } }   // a full worked shift ends the run and re-arms the Chief at the day's end (careerDayEnd); days off, leave and sick days do neither
    careerLadder(now);
    if (c.z < k && k < d) { c.z = k; careerDayEnd(k, now); }
  }
  careerDue(now); careerGoTick(now); sickTick(now);
}
SIM_ADVANCE.push((from, to) => careerTick(to));
// ---- being sick (0.61.5, the career engineer; the user's design via the lead) ----
// Rarely you wake up unwell: a seeded roll at 05:00 (schedU(SICK.seed, day, 901) under SICK.odds), never in your first
// week (day > CAREER.grace) and never within SICK.gap days of the last time: about once every 7 ship weeks. That day
// is a sick day (careerSick): excused, a day off to playerShiftOn, no hit for lateness or a missed shift, and a booked
// leave day comes back. When you're up, a card says so (Infirmary or My bunk set the goal arrow) and, the first time,
// a tip (a warning, shown even with tips off). Untreated it gets worse through the day (SICK.stages: slower and slower,
// then doubled over, section 15's crouch; energy drains faster), with a toast at each step and a friend who may come
// and find you to nudge you. Two cures: the infirmary (in the Infirmary or the Exam room on Deck 3, an exam plays:
// Rina's when she's on shift, else a medic on duty's; it ends with the medicine) or your bunk (lying down sleeps it off
// by day, SICK.nap minutes). Crew who see you say a get-well line, and the next day or two they're glad you're better.
//   SHIP.career (saved) adds gs: the game's own seed (made once with the career, Date.now and Math.random; never R();
//   0 with ?nosave, so the checks are the same every run), sd: the last sick day, sh: how it ended (0 not yet, 1 Rina, 2 a medic on duty, 3 slept it
//   off), ss: the last stage told, sc: the day the card was shown
// The words are head writer 4's (career.sick.*, career.tip.sick, sick.getwell / sick.nudge / sick.better, the meetings
// sickExam1-3 and sickExamCover). Nothing here calls R().
const SICK = { seed: 7919, odds: 1 / 28, gap: 21, rollAt: 300, nap: 180, floor: .4, stages: [[0, .85], [150, .7], [300, .55], [450, .4]], drain: 1.5 };
const sickToday = (d = SHIP.time.day) => !!SHIP.career && SHIP.career.sd > 0 && SHIP.career.sd === d;   // sd 0 is 'never', not day 0 (the arrival)
const sickNow = () => sickToday() && !SHIP.career.sh;    // unwell and untreated, right now
function sickDue(d) {                                   // seeded by the day and the game's own seed (gs), so each game has its own sick days (reviewer 1d)
  const c = SHIP.career, seed = SICK.seed ^ (c && c.gs || 0);
  return d > CAREER.grace && (!c || !c.sd || d - c.sd >= SICK.gap) && schedU(seed, d, 901) < SICK.odds;
}
function sickStage(now = shipNow()) {                    // 0-3 while unwell (by minutes since 06:00), else -1
  if (!sickNow()) return -1; const m = now - (SHIP.time.day - 1) * 1440 - WAKE_AT; let k = 0;
  for (let i = 0; i < SICK.stages.length; i++) if (m >= SICK.stages[i][0]) k = i; return k;
}
function sickFx() {                                      // section 15's needEffects asks: { walk, drain, note } or null
  const k = sickStage(); return k < 0 ? null : { walk: SICK.stages[k][1], drain: SICK.drain, note: 'unwell: see the infirmary, or rest in your bunk' };
}
const sickBent = () => sickStage() >= SICK.stages.length - 1;   // doubled over (section 15's crouch)
function sickStart(d, now) {
  const c = careerInit(); c.sd = d; c.sh = 0; c.ss = -1; careerSick(d);
  simNote('sick', { day: d });
}
function sickCure(how) {                                 // 1 Rina, 2 a medic on duty, 3 slept it off
  const c = SHIP.career; if (!c || !sickNow()) return false;
  c.sh = how; const t = careerText(how === 3 ? 'career.sick.well' : 'career.sick.cured');
  if (t) toast(how === 3 ? 'Your bunk' : 'Infirmary', t);
  if (typeof setGoal === 'function' && typeof IX_GOAL !== 'undefined' && IX_GOAL && /infirmary|bunk/i.test(IX_GOAL.label || '')) setGoal(null);
  simNote('sickCured', { how }); return true;
}
function sickExamTick(now) {                             // in the infirmary while unwell: the exam plays (once a ship minute)
  if (!sickNow() || sleeping || typeof DIALOGUE === 'undefined' || DIALOGUE || typeof dialogueShow !== 'function') return;
  const where = { deck: 3, room: /^(Infirmary|Exam room)$/ };
  try { if (deckDef.num !== 3 || !where.room.test((ROOMS[roomAt(...player.here())] || {}).name || '')) return; } catch (e) { return; }
  const d = SHIP.time.day, rina = socP('rina'), w = rina && typeof whereIs === 'function' ? whereIs(rina, now) : null, hers = !!(w && w.act === 'work' && w.deck === 3);
  const base = hers ? MEETING_SCRIPTS['sickExam' + (1 + d % 3)] || MEETING_SCRIPTS.sickExam1 : MEETING_SCRIPTS.sickExamCover; if (!base) { sickCure(hers ? 1 : 2); return; }
  const id = 'moment:sick:' + d;                         // 'moment:': an exam never counts toward a commendation (section 18's dialogueShow)
  MEETING_SCRIPTS[id] = { ...base, onEnd: done => { delete MEETING_SCRIPTS[id]; if (done) sickCure(hers ? 1 : 2); } };
  dialogueShow(id, { id, who: hers ? ['rina'] : ['infirmary:1'], where, at: now });
}
function sickNote(title, body, buttons) {                // the waking card: a panel with buttons, closed by any of them
  let el = document.getElementById('sickCard');
  if (!el) {
    el = document.createElement('div'); el.id = 'sickCard';
    el.style.cssText = 'position:fixed;left:50%;top:50%;transform:translate(-50%,-50%);z-index:55;width:min(380px,calc(100vw - 32px));padding:18px;border-radius:14px;background:rgba(8,20,26,.96);border:1px solid #6fa8b0;color:#e6f0f1;text-align:center';
    document.body.appendChild(el);
  }
  el.innerHTML = '<h3 style="margin:0 0 8px;font-weight:600"></h3><p style="margin:0 0 14px;line-height:1.45"></p><div style="display:flex;gap:8px;justify-content:center;flex-wrap:wrap"></div>';
  el.querySelector('h3').textContent = title; el.querySelector('p').textContent = body;
  for (const [label, fn] of buttons) { const b = document.createElement('button'); b.type = 'button'; b.textContent = label;
    b.style.cssText = 'font:inherit;padding:8px 16px;border-radius:10px;border:1px solid #6fa8b0;background:#16323a;color:#e6f0f1';
    b.onclick = () => { el.hidden = true; try { fn(); } catch (e) { } }; el.querySelector('div').appendChild(b); }
  el.hidden = false;
}
onSim('newGame', () => { const el = document.getElementById('sickCard'); if (el) el.hidden = true; });
function sickTick(now) {                                 // from careerTick: the roll, the card, worse, the nudge, the exam
  const c = SHIP.career, d = Math.floor(now / 1440) + 1, m = now - (d - 1) * 1440;
  if (c.go == null && c.sd !== d && m >= SICK.rollAt && sickDue(d)) sickStart(d, now);
  if (!sickToday(d)) return;
  const awake = typeof sleeping === 'undefined' || !sleeping;
  if (c.sc !== d && awake && m >= WAKE_AT && typeof document !== 'undefined') {
    c.sc = d; const t = careerText('career.sick.card', d) || 'Not feeling well | You wake up unwell. See the infirmary on Deck 3, or rest in your bunk.', i = t.indexOf(' | ');
    const bed = (DECKS[deckOf(playerBed())].places || []).find(p => p.id === playerBed());
    sickNote(i < 0 ? 'Not feeling well' : t.slice(0, i), i < 0 ? t : t.slice(i + 3), [
      ['Infirmary, Deck 3', () => setGoal({ deck: 3, room: 'I', label: 'The infirmary, Deck 3' })],
      ['My bunk', () => bed && setGoal({ deck: deckOf(bed.id), room: bed.room, label: 'Your bunk' })]]);
    if (!(c.k & 4)) { c.k |= 4; careerTip('sick'); }
  }
  const k = sickStage(now);
  if (k > 0 && k > c.ss) { c.ss = k; const t = careerText('career.sick.worse', k - 1); if (t && awake) toast('Unwell', t); if (k === 2) careerSeek('nudge', now, now + 240, 1); }
  sickExamTick(now);
}
// what crew say when you chat: get well while you're unwell; glad you're better the day or two after (section 20's chatLine asks)
const SICK_SAID = new Set();
function sickChatLine(p, t, peek) {
  const c = SHIP.career, d = Math.floor(t / 1440) + 1; if (!c || !c.sd || d - c.sd > 2 || SICK_SAID.has(p.id + '@' + d)) return null;
  const kind = sickNow() ? 'sick.getwell' : c.sh || d > c.sd ? 'sick.better' : null; if (!kind) return null;
  const l = socLine(p, kind, { t, tier: relTier(p.id) }); if (!l) return null;
  if (!peek) SICK_SAID.add(p.id + '@' + d); return { text: l.text, kind };
}
// the closing card: your time on the Wren is over. New game is the only way on (as the HUD's button: arrive or skip)
function careerCard(on) {
  let el = document.getElementById('careerEnd');
  if (!on) { if (el) el.hidden = true; return; }
  if (!el) {
    el = document.createElement('div'); el.id = 'careerEnd';
    el.style.cssText = 'position:fixed;inset:0;z-index:60;display:flex;align-items:center;justify-content:center;padding:16px;background:rgba(4,10,14,.94);color:#e6f0f1;text-align:center';
    document.body.appendChild(el);
  }
  const t = careerText('career.card', SHIP.career ? SHIP.career.go || 0 : 0) || 'Your time on the Wren is over | ', i = t.indexOf(' | ');
  el.innerHTML = '<div style="max-width:420px"><h2 style="margin:0 0 12px;font-weight:600"></h2><p style="margin:0 0 20px;line-height:1.5"></p><button type="button" style="display:block;margin:0 auto;font:inherit;padding:10px 22px;border-radius:10px;border:1px solid #6fa8b0;background:#16323a;color:#e6f0f1">New game</button></div>';
  el.querySelector('h2').textContent = i < 0 ? t : t.slice(0, i); el.querySelector('p').textContent = i < 0 ? '' : t.slice(i + 3);
  el.querySelector('button').onclick = () => { el.hidden = true;
    if (NOSAVE || typeof introArrived !== 'function' || !introArrived() || typeof deviceChoose !== 'function') return newGameStart(!NOSAVE && typeof introArrived === 'function');
    deviceChoose({ title: 'New game', text: 'How do you want to start?', choices: ['Arrive by shuttle (Sunday evening)', 'Skip to Monday morning'] },
      k => { if (k === 0) newGameStart(true); else { newGameStart(false); if (typeof introSkip === 'function') introSkip(); } }); };
  el.hidden = false;
}
if (SHIP.career && SHIP.career.end) careerCard(true);    // a save that ended: the card again
const movedOn = () => (socInit(), (SHIP.social.moved || []).map(x => { const p = SOC.idx.has(x.id) && SOC.crew[SOC.idx.get(x.id)]; return p ? { id: x.id, name: p.name, role: p.role, day: x.day, to: p.transferTo || null } : null; }).filter(Boolean));
// ---- guiding a newcomer (0.36.65, A10; plans/social-deep-plan.md Part 8b) ----
// Only after you've been promoted (the user's rule: the flag 'promoted', onboarding's and mine; off in normal play until
// promotion exists). When a new cadet (the roster's cadet: true) is due within a week, you've been aboard four ship weeks by
// their arrival day and Works knows your name (repBand('works') 'known' or better), Calder assigns them to you: her card's
// first line, else a Mail at 15:30, and simNote('guideAssigned', { id, day }) (day: their arrival) so onboarding can plan the
// arrival. On the day (07:00) socialGuide(id) starts it: onboarding's introGuide(id) runs the arrival steps the other way
// round (you the escort, them following), the flag guide.active is set (the line condition guide:true), they know you
// (acquaintance) and you're their mentor (bondOf(id, 'mentor') -> 'you'). Their introStep notes (who: them) give them core
// and big memories of you and a little Kindness. Each ship day of their first week their card asks you something (the
// engine's newcomer lines, else GUIDE_QS) with three answers (helpful, funny, honest), all fine. A week on they've settled:
// Works +4, Kindness +3, "good with newcomers", Calder's thank-you. Calder's card has "Hand <name> back" any time, no
// penalty (onboarding's introGuideEnd(id) when it's there). SHIP.social.guide { id, day, at, told, on, qs, qDay, end }, saved.
const GUIDE_WEEKS = 4, GUIDE_AHEAD = 7, GUIDE_LONG = 7;
const GUIDE_QS = [
  ['Where\'s the mess? I\'ve walked past the same door three times.', ['Down by the galley. Follow the smell of toast.', 'Follow anyone holding a mug. Works every time.', 'I got lost for two days. You\'ll get it.']],
  ['Who\'s the scary one? Everyone looks at me like I should know.', ['Be on time and nobody\'s scary. Fair crew.', 'Whoever\'s mug you just borrowed.', 'Nobody, really. They just remember being new.']],
  ['Is the food always this good?', ['Mostly. Get there early for the good bread.', 'Only when Calder\'s eating with us.', 'It is. One of the best things about the Wren.']],
  ['What do people do in the evenings?', ['Check the Schedule on your device. There\'s always something.', 'Pretend not to be revising for quiz night.', 'Some nights, nothing much. That\'s allowed too.']],
  ['What if I break something on my first job?', ['Tell your Chief and log it. That\'s all anyone wants.', 'Then you\'re officially one of us.', 'You probably will. I did. Nobody minded.']],
  ['Does it get less strange, being out here?', ['Give it a week. Find one place on the ship that\'s yours.', 'No. You just get used to strange.', 'It does. Slowly, then all at once.']],
  ['How do I get people to like me?', ['Say yes to a favour or two. Turn up to things.', 'Biscuits. Bribery works.', 'Just be around. They\'ll come to you.']],
  ['Can I come and ask you things, if I get stuck?', ['Any time. Find me, or send a message.', 'Only on Tuesdays. Kidding. Any time.', 'Please do. Someone did that for me.']]];
const GUIDE_ANS = [['Thanks. That actually helps.', 'Right. Got it. Thank you.'], ['Ha! Okay. Noted.', 'You\'re ridiculous. Thanks, though.'], ['That\'s... really good to know. Thank you.', 'Oh. That helps more than you think.']];
const GUIDE_GEN = ['Here, let me show you.', 'Ha. Welcome aboard.', 'Honestly? It gets easier.'];   // answers for the engine's own newcomer lines
const guideOn = () => { const g = SHIP.social && SHIP.social.guide; return g && g.on && !g.end ? g : null; };
function socGuideDay(h) {                                  // 07:00 each ship day (socialHour): assign, start, settle
  if (typeof flag !== 'function' || !flag('promoted')) return;
  const d = Math.floor(h / 24) + 1, t = h * 60 + 30, G = SHIP.social.guide, cal = SOC.idx.has('calder') ? SOC.crew[SOC.idx.get('calder')] : null;
  if (G && !G.end && !G.on && d >= G.day) socialGuide(G.id);
  if (G && G.on && !G.end && d >= G.day + GUIDE_LONG) {
    const p = socP(G.id); G.end = 'settled'; if (typeof flagSet === 'function') flagSet('guide.active', false);
    if (p) { memAdd(p.id, 'guide.settled', { cls: 'core' }); repAdd('works', 4, { kindness: 3 }, 'newcomer');
      if (cal) SHIP.social.mail.push({ at: t + 600, from: cal.name, subject: shortName(p) + '\'s settled in', body: shortName(p) + '\'s settled in well. That\'s your doing, more than you know. Thank you. ' + shortName(cal) }); }
  }
  if (G && !G.end) return;                                 // one at a time
  if (!['known', 'well', 'theirs'].includes(repBand('works'))) return;
  const p = SOC.crew.find(q => { const A = q.cadet && arriveDay(q); return A > 1 && A - 1 >= GUIDE_WEEKS * 7 && A - d >= 1 && A - d <= GUIDE_AHEAD && !(G && G.id === q.id); });
  if (!p) return;
  SHIP.social.guide = { id: p.id, day: arriveDay(p), at: d, told: false, on: false, qs: 0, qDay: 0, end: null };
  if (typeof simNote === 'function') simNote('guideAssigned', { id: p.id, day: arriveDay(p) });
}
function socGuideMail(h) {                                 // 15:00's hour: Calder didn't catch you, so a Mail
  const G = SHIP.social.guide, cal = SOC.idx.has('calder') ? SOC.crew[SOC.idx.get('calder')] : null;
  if (!G || G.told || G.end || !cal) return; G.told = true;
  SHIP.social.mail.push({ at: h * 60 + 30, from: cal.name, subject: 'A newcomer for you', body: guideAskLine(G) + ' ' + shortName(cal) });
}
function guideAskLine(G) {
  const p = socP(G.id), m = SHIP.social.mentor && socP(SHIP.social.mentor), wd = typeof weekday === 'function' ? ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][weekday(G.day)] : null;
  return 'A new cadet comes aboard ' + (wd ? 'on ' + wd : 'soon') + ': ' + (p ? p.name + ', ' + (p.role || 'cadet').toLowerCase() : 'one of ours') + '. I\'d like you to meet them at the ramp and show them round, the way ' + (m ? shortName(m) + ' did' : 'you were shown') + ' for you. Hand them back to me any time, no harm done.';
}
function socialGuide(id) {                                 // you start guiding them: onboarding's introGuide runs the steps
  socInit(); const p = socP(id), G = SHIP.social.guide; if (!p || !G || G.id !== p.id || G.end) return false;
  if (G.on) return true;
  G.on = true; if (typeof flagSet === 'function') flagSet('guide.active', true);
  const r = relGet(p.id); if (r.pts < REL_TIERS[1]) { r.pts = REL_TIERS[1]; r.tier = relTierOf(r.pts); } if (r.met === null) r.met = Math.floor(socNow());
  memAdd(p.id, 'guide.met', { cls: 'core' });
  if (typeof introGuide === 'function') { try { introGuide(p.id); } catch (e) { } }
  return true;
}
function socialGuideEnd(why = 'handed') {                   // Hand them back (Calder's card): no penalty
  const G = guideOn() || (SHIP.social.guide && !SHIP.social.guide.end ? SHIP.social.guide : null); if (!G) return false;
  G.end = why; if (typeof flagSet === 'function') flagSet('guide.active', false);
  if (typeof introGuideEnd === 'function') { try { introGuideEnd(G.id); } catch (e) { } }
  return true;
}
function socGuideStep(d) {                                 // introStep { step, who: the newcomer } while you guide them
  const G = guideOn(); if (!G || d.missed || ![].concat(d.who || []).includes(G.id)) return false;
  memAdd(G.id, 'guide.' + d.step, { cls: INTRO_MEM[d.step] === 'intro.arrival' ? 'core' : 'big' });
  if (repOnce('guide.' + d.step)) repAdd(null, 0, { kindness: 1 });
  return true;
}
function guideQuestion(p, t, eng) {                        // their card's first line in their first week: something they ask you
  const G = guideOn(), d = Math.floor(t / 1440) + 1; if (!G || G.id !== p.id || G.qDay === d || d < G.day || d >= G.day + GUIDE_LONG) return null;
  const l = eng('newcomer'), q = GUIDE_QS[G.qs % GUIDE_QS.length];
  return l ? { ...l, kind: 'newcomer', answers: GUIDE_GEN } : { text: q[0], kind: 'newcomer', answers: q[1], say: true };
}
function guideAnswer(p, k) {                               // 0 helpful, 1 funny, 2 honest: all fine
  const G = guideOn(); if (!G || G.id !== p.id) return null;
  G.qDay = SHIP.time.day; G.qs++; relAdd(p.id, 'guide', 3); repAdd(null, 0, { kindness: .5 });
  if (G.qs === 1) memAdd(p.id, 'guide.asked');
  const a = GUIDE_ANS[k] || GUIDE_ANS[0]; return a[Math.floor(schedU(p.seed, SHIP.time.day, 666) * a.length)];
}
const repAskedFor = dept => ['well', 'theirs'].includes(repBand(dept));
const repNotes = () => (repInit().notes || []).slice().reverse();
function repView() {                                     // the Record's Reputation page (section 19 draws it): words only, never numbers
  socInit(); const R = repInit(), w = k => REP_SHIP_WORDS[k][R.ship[k] < 35 ? 0 : R.ship[k] < 60 ? 1 : R.ship[k] < 80 ? 2 : 3];
  return { depts: REP_DEPTS_ALL.map(d => ({ dept: d, band: repBand(d), name: REP_NAMES[repBand(d)] })),
           ship: { work: 'Work: ' + w('work'), kindness: 'Kindness: ' + w('kindness'), spirit: 'Spirit: ' + w('spirit') }, knownFor: knownFor(), notes: repNotes() };
}

// ---- news ----
const NEWS_MAX = 16;                                   // news going round at most (0.36.78: a bound for the save)
function newsAdd({ id, about = null, lines, weight = .6, seed = [], born = Math.floor(shipNow()), kind = 'gossip', event = null, life = 4 }) {
  socInit(); if (!id || !Array.isArray(lines) || !lines.length || NEWS.some(x => x.id === id)) return null;
  // seed: crew ids, or 'dept:<dept>' and 'all' (the events engineer's tokens)
  seed = [...new Set(seed.flatMap(s => s === 'all' ? SOC.crew.map(p => p.id) : /^dept:/.test(s) ? SOC.crew.filter(p => p.dept === s.slice(5)).map(p => p.id) : [s]))];
  const it = { id, about, lines: lines.slice(), weight, seed: seed.filter(s => SOC.idx.has(s) && socAboard(SOC.crew[SOC.idx.get(s)])), born, kind, event, life };
  NEWS.push(it); SHIP.knows[id] = new Set(it.seed);
  const wt = n => +n.weight || 0;                        // a hard cap: the least of it goes first (a tradition's chatter, then a fault), the oldest of those, never the one just added (0.71.1: an arrival's news, weight .6, fell off behind a run of faults)
  while (NEWS.length > NEWS_MAX) { let k = NEWS[0] === it ? 1 : 0; for (let i = k + 1; i < NEWS.length; i++) if (NEWS[i] !== it) if (wt(NEWS[i]) < wt(NEWS[k]) || wt(NEWS[i]) === wt(NEWS[k]) && (NEWS[i].born < NEWS[k].born || (NEWS[i].born === NEWS[k].born && NEWS[i].id < NEWS[k].id))) k = i; delete SHIP.knows[NEWS[k].id]; NEWS.splice(k, 1); }
  return it;
}
function newsKnownBy(p, t = shipNow()) {
  socInit(); const id = p && p.id || p;
  return NEWS.filter(x => x.born <= t && SHIP.knows[x.id] && SHIP.knows[x.id].has(id))
    .sort((a, b) => (b.weight - (t - b.born) / 1440 * .2) - (a.weight - (t - a.born) / 1440 * .2) || (a.id < b.id ? -1 : 1));
}
const heardIt = n => SHIP.heard.some(h => h.id === n.id && h.at >= n.born);   // you've heard this one (not just an older item of the same id)
function playerHeard(newsId, from, overheard) {        // overheard: in passing (chatter), so no nudge for the teller
  socInit(); const it = NEWS.find(x => x.id === newsId);
  if (!it || SHIP.heard.some(x => x.id === newsId && x.at >= it.born)) return false;   // heard since this one was born (a pair's second friendship is news again)
  SHIP.heard.push({ id: newsId, from: from || null, at: Math.floor(shipNow()), line: it.lines[0] });
  if (SHIP.heard.length > 60) SHIP.heard.splice(0, SHIP.heard.length - 60);
  if (from && !overheard && SOC.idx.has(from)) relAdd(from, 'news', REL_PTS.news);
  return true;
}
// the day's gossip, born at its hour: birthdays and ship traditions at 07:00, habit changes at 09:00
function socBorn(h, rooms) {
  const d = Math.floor(h / 24) + 1, hr = socHr(h), t = h * 60 + 30, crew = SOC.crew;
  const near = p => crew.filter(q => q !== p && (socRoom(q) === socRoom(p) || q.dept === p.dept));   // who'd know first
  if (hr === 7 && typeof birthdaysOn === 'function') for (const p of birthdaysOn(d)) if (SOC.idx.has(p.id)) {
    const n = shortName(p);
    newsAdd({ id: 'bday:' + p.id + ':' + d, about: p.id, kind: 'birthday', weight: .8, life: 1, born: t, seed: socPick(near(p), 4, p.seed, d, 601).map(q => q.id),
      lines: ['It\'s ' + n + '\'s birthday today.', 'Did you know it\'s ' + n + '\'s birthday?', 'Don\'t forget, it\'s ' + n + '\'s birthday.'] });
  }
  if (hr === 9 && d > 7 && typeof habitWeek === 'function') for (const c of habitWeek(Math.floor((d - 1) / 7))) if (c.day === d && SOC.idx.has(c.id)) {
    const p = crew[SOC.idx.get(c.id)];
    newsAdd({ id: 'habit:' + c.id + ':' + d, about: c.id, kind: 'habit', weight: .5, life: 5, born: t, seed: socPick(near(p), 2, p.seed, d, 602).map(q => q.id),
      lines: [c.text, 'Have you noticed? ' + c.text, 'Funny thing: ' + c.text] });
  }
  if (hr === 7 && typeof eventsOn === 'function') for (const e of eventsOn(d)) if (!e.honorees.length) {
    const going = crew.filter(p => planDay(p, d).some(s => s.tag && (s.tag === 'ev-' + e.id || s.tag.startsWith('ev-' + e.id + '-')))), when = e.from >= 1020 ? 'tonight' : 'today';
    newsAdd({ id: 'trad:' + e.id + ':' + d, about: e.id, kind: 'tradition', weight: .4, life: Math.max(.1, (e.to - 450) / 1440), born: t,   // gone once it's over seed: socPick(going, 4, socHash(e.id), d, 603).map(q => q.id),
      lines: [e.name + ' ' + when + ' at ' + hhmm(e.from) + '.', 'Are you coming? ' + e.name + ' starts at ' + hhmm(e.from) + '.', e.id === 'quiz' ? 'Quiz night tonight. I\'ve been revising.' : e.name + ' ' + when + '. Should be good.'] });
  }
  // machines going faulty or worse (section 17's record of the hour); whoever is on that deck notices first
  const rec = typeof MACH_HIST !== 'undefined' ? MACH_HIST.get(h) : null;
  if (rec && typeof machineList === 'function') for (const m of machineList()) {
    const st = machineState(rec[m.id] ?? 100), lvl = MACHINE_SEV[st] ? st : null, seen = SHIP.social.fault[m.id];
    if (!lvl) { if (seen) delete SHIP.social.fault[m.id]; continue; }
    if (seen === lvl || (seen && MACHINE_SEV[seen] > MACHINE_SEV[lvl])) continue;
    const there = []; for (const [k, l] of rooms) if (k.startsWith(m.deck + '|')) there.push(...l.map(i => crew[i]));
    if (!there.length) continue;                         // nobody about to notice: it's news when someone is
    SHIP.social.fault[m.id] = lvl;
    const name = MACHINE_KINDS[m.kind].name.toLowerCase(), s = SOC_SYMPTOM[m.kind] || 'playing up', where = 'the ' + name + ' on ' + deckIn(m.deck);
    newsAdd({ id: 'fault:' + m.id + ':' + h, about: m.id, kind: 'fault', weight: lvl === 'faulty' ? .5 : lvl === 'failing' ? .7 : .9, life: 3, born: t,
      seed: socPick(there, 3, socHash(m.id), h, 604).map(q => q.id),
      lines: ['The ' + name + ' on ' + deckIn(m.deck) + ' has been ' + s + ' all week.', 'Someone should look at ' + where + '. It keeps ' + s + '.', 'Have you heard? ' + where[0].toUpperCase() + where.slice(1) + ' is ' + s + ' again.'] });
  }
}
// ---- one ship hour on paper: who spent time together, affinity drifting, news passing on ----
const RIVAL_COOL = .4, RIVAL_FLOOR = -45, RIVAL_HEAL = -25, RIVAL_HEAL_DAYS = 2;   // A12: clashing pairs cool a point in 40% of their hours together, no lower than -45; below -25, a point back every other night
function socHeal(h) { if ((Math.floor(h / 24) + 1) % RIVAL_HEAL_DAYS) return; const a = SHIP.aff; for (let x = 0; x < a.length; x++) if (a[x] < RIVAL_HEAL) a[x]++; }   // time heals: a falling-out eases unless they keep meeting
const socHr = h => ((h % 24) + 24) % 24;               // the hour of the day, also on Day 0 (negative ship hours)
let SOC_IN = null;                                      // the hour socialHour is running (SHIP.social.hour is already the next one)
function socialHour(h) {
  SOC_IN = h;
  const { crew, n } = SOC, t = h * 60 + 30, S = schedData(), rooms = new Map(), aff = SHIP.aff;
  if (typeof machinesNow === 'function' && typeof MACH_HIST !== 'undefined' && !MACH_HIST.has(h) && t <= shipNow()) machinesNow();
  for (let i = 0; i < n; i++) {
    if (!socAboard(crew[i], Math.floor(h / 24) + 1)) continue;   // off the ship (crew coming and going, guests away)
    const w = planWhere(crew[i], t); if (!w || w.moving || w.act === 'sleep' || !w.placeId) continue;
    const pl = S.byId.get(w.placeId), k = w.deck + '|' + (pl && pl.room || w.placeId);
    (rooms.get(k) || rooms.set(k, []).get(k)).push(i);
  }
  const FR = new Uint8Array(n), CAP = crew.map(p => typeof friendCap === 'function' ? friendCap(p) : 4);   // friends (60+) each has, and how many they make room for (20c's friendCap: 3-5 by traits)
  for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) if (aff[pairIdx(i, j)] >= 60) { FR[i]++; FR[j]++; }
  const pairs = [];                                      // [i, j] who spent time together this hour
  for (const g of rooms.values()) {
    if (g.length < 2) continue;
    const q = Math.min(1, 3 / (g.length - 1));           // in a crowd, each person really talks to about three
    for (let a = 0; a < g.length; a++) for (let b = a + 1; b < g.length; b++) {
      const i = Math.min(g[a], g[b]), j = Math.max(g[a], g[b]), ps = pairSeed(i, j);
      if (q < 1 && schedU(ps, h, 605) >= q) continue;
      pairs.push([i, j]);
      const x = pairIdx(i, j), v0 = aff[x], u = schedU(ps, h, 606), clash = socClash(crew[i], crew[j]);
      let v = v0;
      if (!clash && v < 90 && u < .7 && (v >= 60 || (FR[i] < CAP[i] && FR[j] < CAP[j]))) v++; else if (clash && v > RIVAL_FLOOR && u < RIVAL_COOL) v--;
      aff[x] = v;
      const key = i + '-' + j, P = SHIP.social.pairs;
      if (v0 < 60 && v >= 60 && P[key] !== 'f') { delete P[key]; P[key] = 'f'; socPairNews(i, j, true, t); }
      if (v0 > -40 && v <= -40 && P[key] !== 'r') { delete P[key]; P[key] = 'r'; socPairNews(i, j, false, t); }
    }
  }
  // news passes on between people who spent time together (decided against the hour's start, so it never runs
  // through a whole room in one hour); friends tell each other more readily, people who don't get on hardly at all
  const learnt = [];
  for (const it of NEWS) {
    if (it.born > t) continue;
    const K = SHIP.knows[it.id], hs = socHash(it.id);
    for (const [i, j] of pairs) {
      const ki = K.has(crew[i].id), kj = K.has(crew[j].id); if (ki === kj) continue;
      const a = aff[pairIdx(i, j)], c = .2 * it.weight * (a >= 40 ? 1.5 : a <= -20 ? .3 : 1);
      if (schedU(pairSeed(i, j) ^ hs, h, 607) < c) learnt.push([K, crew[ki ? j : i].id]);
    }
  }
  for (const [K, id] of learnt) K.add(id);
  socBorn(h, rooms);
  socCourtesy(h, rooms);
  if (typeof storyHour === 'function') storyHour(h, pairs);   // bonds between crew (20c)
  if (socHr(h) === 4) { memFade(); socHeal(h); socTrim(); }
  if (socHr(h) === 19) socCrewGift(h);
  if (socHr(h) === 7) { socTransfers(h); socInvites(h); socGuideDay(h); }
  if (socHr(h) === 15) socGuideMail(h);
  if (socHr(h) === 4 && (Math.floor(h / 24) + 1) % 7 === 0) repWeek(h);   // Sundays
  for (let k = NEWS.length - 1; k >= 0; k--) if (t - NEWS[k].born > NEWS[k].life * 1440) { delete SHIP.knows[NEWS[k].id]; NEWS.splice(k, 1); }   // old news is dropped
  while (NEWS.length > 40) { delete SHIP.knows[NEWS[0].id]; NEWS.shift(); }
  for (const k in SHIP.social.feuds) if (SHIP.social.feuds[k].until <= t) delete SHIP.social.feuds[k];   // a feud nobody smoothed over just fades
  socNotesTo((h + 1) * 60);                               // the bus notes of this hour, at their own times, once the hour has run
  SOC_IN = null;
}
// the diplomatic visit's 'discourtesy' thread (0.36.16, for section 18; lower is better). guestWarmth(p, t): how kindly
// someone feels toward the guests, from their mood, less for prickly traits (suspicious 30, gruff, blunt, sarcastic
// 15), more if they're your friend (tier 3+, 15) and if you chatted with them today (10): you can soften Holt. While the
// guests are aboard (eventMod('effect', 'guests')), at 20:00 each day Holt under 45 adds 1, and so does a day when a
// guest of the event shared a room with a crew member under 35. At most one of each a day (SHIP.social.courtesy,
// saved). Inert without section 18's eventScore and eventMod
const COURTESY_PRICKLY = { suspicious: 30, gruff: 15, blunt: 15, sarcastic: 15 };
function guestWarmth(p, t) {
  const r = SHIP.rel[p.id];
  return crewMood(p, t) - (p.traits || []).reduce((a, x) => a + (COURTESY_PRICKLY[x] || 0), 0) + (r && r.tier >= 3 ? 15 : 0) + (r && r.chatDay === Math.floor(t / 1440) + 1 ? 10 : 0);
}
function socCourtesy(h, rooms) {
  if (typeof eventScore !== 'function' || typeof eventMod !== 'function') return;
  const t = h * 60 + 30, d = Math.floor(h / 24) + 1, C = SHIP.social.courtesy;
  let on = null; try { on = eventMod('effect', 'guests', t); } catch (e) { on = null; }
  if (!on) return;
  const ev = typeof eventNow === 'function' ? eventNow(t) : null;
  const guests = typeof GUESTS !== 'undefined' ? schedPeople().filter(q => GUESTS.some(g => g.id === q.id && (!ev || !g.event || g.event === ev.id))) : [];
  if (guests.length && C.meet !== d) {                   // a guest in a room with someone prickly or low, this hour
    const S = schedData();
    for (const g of guests) {
      const w = planWhere(g, t); if (!w || w.moving || !w.placeId) continue;
      const pl = S.byId.get(w.placeId), here = rooms.get(w.deck + '|' + (pl && pl.room || w.placeId)) || [];
      const sour = here.map(i => SOC.crew[i]).find(q => guestWarmth(q, t) < 35);
      if (sour) { C.meet = d; eventScore('discourtesy', 1); break; }
    }
  }
  if (socHr(h) === 20 && C.holt !== d && SOC.idx.has('holt') && guestWarmth(SOC.crew[SOC.idx.get('holt')], t) < 45) { C.holt = d; eventScore('discourtesy', 1); }
}
function socPairNews(i, j, friends, t) {
  const a = shortName(SOC.crew[i]), b = shortName(SOC.crew[j]);
  newsAdd({ id: (friends ? 'friends:' : 'rivals:') + SOC.crew[i].id + ':' + SOC.crew[j].id, about: SOC.crew[i].id + ',' + SOC.crew[j].id, kind: friends ? 'friends' : 'rivals',
    weight: .6, life: 4, born: t, seed: [SOC.crew[i].id, SOC.crew[j].id],
    lines: friends ? [a + ' and ' + b + ' are always together these days.', 'Have you noticed ' + a + ' and ' + b + '? Best of friends now.', a + ' and ' + b + ' have become thick as thieves.']
                   : [a + ' and ' + b + ' aren\'t speaking.', 'There\'s a chill between ' + a + ' and ' + b + ' lately.', 'Did you hear ' + a + ' and ' + b + ' had words?'] });
  if (!friends) SHIP.social.feuds[SOC.crew[i].id + ':' + SOC.crew[j].id] = { until: t + 3 * 1440, talked: [] };   // a falling-out you can smooth over
}
// small dramas (0.36.11): a pair who fall out (rivals, above) is a feud for three days. Each of them grumbles about
// the other on their card (feudOf); chat with both while it lasts and they make it up: their affinity goes back to
// -10, it's news ("X and Y have made up"), and each gives you REL_PTS.chat extra. SHIP.social.feuds, saved
function feudOf(id, t = shipNow()) {
  for (const k in SHIP.social.feuds) { const f = SHIP.social.feuds[k], [a, b] = k.split(':'); if (f.until > t && (a === id || b === id)) return { k, f, other: a === id ? b : a }; }
  return null;
}
function feudTalk(p) {                                   // you chatted with someone in a feud
  const o = feudOf(p.id); if (!o) return null;
  if (!o.f.talked.includes(p.id)) o.f.talked.push(p.id);
  if (o.f.talked.length < 2) return null;
  const [a, b] = o.k.split(':'), i = SOC.idx.get(a), j = SOC.idx.get(b), t = Math.floor(shipNow());
  delete SHIP.social.feuds[o.k]; SHIP.aff[pairIdx(i, j)] = -10; { const k = Math.min(i, j) + '-' + Math.max(i, j); delete SHIP.social.pairs[k]; SHIP.social.pairs[k] = 'm'; }
  const na = shortName(SOC.crew[i]), nb = shortName(SOC.crew[j]);
  newsAdd({ id: 'madeup:' + o.k + ':' + t, about: a + ',' + b, kind: 'madeup', weight: .5, life: 3, born: t, seed: [a, b],
    lines: [na + ' and ' + nb + ' have made up.', 'Saw ' + na + ' and ' + nb + ' having dinner together. About time.', 'Looks like ' + na + ' and ' + nb + ' are talking again.'] });
  relAdd(a, 'chat', REL_PTS.chat); relAdd(b, 'chat', REL_PTS.chat); memAdd(a, 'mended.' + b); memAdd(b, 'mended.' + a); repAdd(null, 0, { kindness: 3 }, 'kind');
  return 'You talk it over, and you can tell something\'s shifted. ' + shortName(SOC.crew[SOC.idx.get(o.other)]) + ' must have said something too.';
}
function socialTo(t) {
  socInit(); const h1 = Math.floor(t / 60);
  if (h1 < SHIP.social.hour) { socReset(h1); return; }   // a clock earlier than ours: a new game
  if (h1 - SHIP.social.hour > 24 * 14) SHIP.social.hour = h1 - 24 * 14;   // never more than two weeks at once
  while (SHIP.social.hour < h1) socialHour(SHIP.social.hour++);
}
function socialTick() {                                  // the main loop: the chat card every frame, the hours once a ship minute
  chatTick();
  if (typeof linesTick === 'function') linesTick();       // section 22: overheard conversations (0.43.12)
  const m = Math.floor(shipNow()); if (m === SOC_MIN) return;
  const step = SOC_MIN >= 0 && m > SOC_MIN && m - SOC_MIN < 30 ? m - SOC_MIN : 0;
  SOC_MIN = m; socialTo(m); socialTogether(step); promoTick(); socialSeek(m); socialChatter(m); socialMail(m); socialAppts(); socInviteMail(m); socialVisit(m);
}
// chatter you overhear (0.36.5) in the performance engineer's speech bubbles (section 8b: bubbleSay(who, text, secs),
// at most two on screen; inert without it). Now and then (CHATTER_ODDS a ship minute, at most one every CHATTER_GAP
// real seconds) someone awake within CHATTER_NEAR tiles says a line: news they know that you haven't heard (you hear
// it: playerHeard, no relationship nudge for eavesdropping), else, more rarely, small talk by what they're doing.
// No bubbles while a chat card is open (the voice budget: bubbles.hidden)
const CHATTER_NEAR = 7, CHATTER_ODDS = .35, CHATTER_GAP = 12;
const CHATTER_IDLE = linesLegacy('smalltalk');            // small talk between crew, by what they're doing (content/banks/old.lines)
let CHATTER_AT = -1e9;
const CHATTER_LAST = [];                                 // the last few lines said, so nobody repeats one
// the Works crew's cheer (0.71.2, worksGather): one of them a ship minute says well done, as they stand by the board;
// team jobs (m8): the team talk while they work (section 22's kind 'team', else TEAM_TALK), ahead of news and small talk
const TEAM_TALK = ['Mind your fingers.', 'Nearly there.', 'Hold it... hold it...', 'Easy does it.', 'Who\'s got the spanner?', 'That\'s it. Lovely.'];
const CHEER_LINES = ['Well done, Officer!', 'Told you you\'d do it.', 'Officer! Look at you.', 'About time too. Well done.', 'Three cheers, then!'];
let CHEER = null;                                        // { ids, until, said: Set }
function cheerTick(m) {
  const C = CHEER; if (!C) return false; if (shipNow() >= C.until) { CHEER = null; return false; }
  const P = player.obj.position;
  for (const id of C.ids) {
    if (C.said.has(id)) continue;
    const a = DECK_CREW.find(x => x.p.id === id); if (!a || !a.h || a.pose !== 'stand' || Math.hypot(a.x - P.x, a.z - P.z) > CHATTER_NEAR) continue;
    const l = socLine(a.p, 'promoted', { t: shipNow(), tier: relTier(id), bubble: true, flags: { 'promo.gather': true } });
    bubbleSay(a.h, l ? l.text : CHEER_LINES[(Math.floor(schedU(a.p.seed, m, 640) * CHEER_LINES.length) + C.said.size) % CHEER_LINES.length]); C.said.add(id); CHATTER_AT = simNow(); return true;
  }
  return false;
}
const teamJobOf = (w) => w && w.job && (SHIP.jobs || []).find(j => j.id === w.job && Array.isArray(j.team)) || null;
function socialChatter(m) {
  if (typeof bubbleSay !== 'function' || typeof DECK_CREW === 'undefined') return;
  if (typeof bubbles !== 'undefined' && bubbles) bubbles.hidden = !!CHAT;
  if (!CHAT && !sleeping && cheerTick(m)) return;
  if (CHAT || sleeping || simNow() - CHATTER_AT < CHATTER_GAP * 1000 || schedU(m, 0, 635) >= CHATTER_ODDS) return;
  const t = shipNow(), heard = new Set(SHIP.heard.map(x => x.id)), P = player.obj.position;
  const v = new THREE.Vector3(), onScreen = a => { v.set(a.x, (a.y || 0) + 1.6, a.z).project(camera); return Math.abs(v.x) < .7 && v.y < .8 && v.y > -.9; };   // well inside the screen, so the bubble fits
  const near = DECK_CREW.filter(a => a.h && SOC.idx.has(a.p.id) && Math.hypot(a.x - P.x, a.z - P.z) <= CHATTER_NEAR && onScreen(a))
    .sort((a, b) => schedU(a.p.seed, m, 636) - schedU(b.p.seed, m, 636));
  for (const a of near) {
    const w = whereIs(a.p, t); if (!w || w.act === 'sleep' || w.act === 'wash') continue;
    const tj = teamJobOf(w); if (tj) {                   // at a team job: work talk first (m8, 0.71.2)
      const l = socLine(a.p, 'team', { t, act: 'work', bubble: true, flags: { 'team.on': true } }), text = l ? l.text : TEAM_TALK[Math.floor(schedU(a.p.seed, m, 641) * TEAM_TALK.length)];
      if (!CHATTER_LAST.includes(text) && bubbleSay(a.h, text)) { CHATTER_AT = simNow(); CHATTER_LAST.push(text); if (CHATTER_LAST.length > 8) CHATTER_LAST.shift(); return; }
    }
    const n = newsKnownBy(a.p, t).find(x => !heardIt(x) && !(x.about === a.p.id && x.kind !== 'fault'));
    let text = n ? n.lines[Math.floor(schedU(a.p.seed, m, 637) * n.lines.length)] : null;
    if (!text && schedU(a.p.seed, m, 638) < .3) { const k = w.act === 'breakfast' || w.act === 'dinner' ? 'meal' : w.act === 'work' ? 'work' : w.act === 'leisure' || w.act === 'off' ? 'free' : null;
      const l = k && socLine(a.p, 'smalltalk', { t, act: w.act, talk: k, bubble: true }); if (l) text = l.text; else if (k) text = CHATTER_IDLE[k][Math.floor(schedU(a.p.seed, m, 639) * CHATTER_IDLE[k].length)]; }
    if (!text || CHATTER_LAST.includes(text)) continue;
    if (bubbleSay(a.h, text)) { CHATTER_AT = simNow(); CHATTER_LAST.push(text); if (CHATTER_LAST.length > 8) CHATTER_LAST.shift(); if (n) playerHeard(n.id, a.p.id, true); }
    return;
  }
}
// friends come and find you (0.36.4): a friend (tier 3+) in their free time on your deck, within SEEK_NEAR tiles,
// now and then (SEEK_ODDS a ship minute, schedU k 633) waves you over: a small prompt at the screen's edge, never one
// you must answer. Tap it for the chat card; it goes on its own after SEEK_SECS real seconds or when they go. Once a
// friend a ship day (rel.seekDay), one prompt at a time, none while a card is open.
// 0.71.0 (the user's playtest note): nobody calls out across the room any more. They walk up (section 10's seekStep,
// SEEK_COME while on the way, at most SEEK_COME_SECS real seconds), stop beside you facing you, and say their opener
// (section 22's kind 'seek', addressed to you) in a bubble and the chip; they stay by you while the chip is up. When it
// happens is seeded per save (seekSalt: the career's game seed gs), so it differs between new games, same for one save
const SEEK_NEAR = 10, SEEK_ODDS = .06, SEEK_SECS = 25, SEEK_COME_SECS = 30, SEEK_BESIDE = 1.3;
let SEEK = null, SEEK_COME = null;                        // { p, el, until, line, come }; { p, m, why, until } on the way
const seekSalt = () => SHIP.career && SHIP.career.gs | 0 || 0;
const SEEK_PRIVATE = new Set(['bathroom', 'shower', 'toilet', 'wash', 'hands']);   // reviewer 2's LOW on 0.71.0: nobody walks up while you wash, or in a washroom
const seekPrivate = () => { if (typeof ACT !== 'undefined' && ACT && SEEK_PRIVATE.has(ACT.kind)) return true; try { const r = (deckDef.rooms || {})[roomAt(...player.here())]; return !!r && /washroom|shower|toilet/i.test(r.name || ''); } catch (e) { return false; } };
const seekBusy = p => typeof TJ_WALK !== 'undefined' && !!TJ_WALK && !!TJ_WALK.roles && TJ_WALK.roles.has(p.id);   // in a tradition's walk with you (section 18's tap to join): not taken off it
const seekWho = p => !seekBusy(p) && !!(SEEK_COME && SEEK_COME.p === p || SEEK && SEEK.come && SEEK.p === p && !CHAT);
const SEEK_OPEN = ['Got a minute? I was hoping I\'d catch you.', 'There you are. Have you got a moment?', 'Oh good, it\'s you. Come and talk to me a minute.', 'Hey, you. Got a second for me?'];   // until section 22 has 'seek' lines
function seekCome(p, a, m, why) {                         // a: their agent on this deck; none (not here): the chip as before
  if (!a) { seekShow(p, m, why); return; }
  SEEK_COME = { p, m, why: why || null, until: simNow() + SEEK_COME_SECS * 1000 };
}
function seekArrive(a) { const c = SEEK_COME; SEEK_COME = null; if (c && !CHAT && !SEEK) seekShow(c.p, c.m, c.why, a); }
function seekEl() {
  let el = document.getElementById('seek'); if (el) return el;
  const st = document.createElement('style');
  st.textContent = '#seek{position:fixed;right:12px;top:50%;transform:translateY(-50%);z-index:3;max-width:min(220px,60vw);background:var(--glass);border:1px solid var(--line);border-radius:12px;padding:8px 12px;font-size:13px;color:#e6f0f1;line-height:1.35;cursor:pointer;-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px)}#seek b{color:#bdeee6;font-weight:600}';
  document.head.appendChild(st);
  el = document.createElement('div'); el.id = 'seek'; el.hidden = true; document.body.appendChild(el);
  el.onclick = () => { if (SEEK && SEEK.visit) { visitIn(); return; } const s = SEEK; seekEnd(); if (s) { const a = DECK_CREW.find(x => x.p === s.p); if (a) { a.talking = 6; player.stop(); player.face = Math.atan2(a.x - player.obj.position.x, a.z - player.obj.position.z); } chatOpen(s.p, !s.line, s.line || undefined); } };
  return el;
}
function seekShow(p, m, why, a) {                       // the chip (why: an ask's, for its line: the career engineer's worried friends and goodbyes, 0.61.0); a: they've walked up (0.71.0)
  if (!p) return;
  const el = seekEl(), U = k => schedU(p.seed ^ seekSalt(), m, k);
  let line = why && typeof careerSeekLine === 'function' ? careerSeekLine(p, why) : null;
  if (!line && a) { const l = chatLine(p, shipNow(), true); if (l && TALK_KEEP.has(l.kind)) line = l; }   // something that matters (a goodbye, a missed appointment): that's what they came to say
  if (!line) { const l = socLine(p, 'seek', { t: shipNow(), tier: relTier(p.id), warmth: warmth(p.id) }); line = { text: l ? l.text : SEEK_OPEN[Math.floor(U(634) * SEEK_OPEN.length)], kind: 'seek', say: true }; }
  el.innerHTML = ''; const b = document.createElement('b'); b.textContent = shortName(p); el.appendChild(b);
  el.appendChild(document.createTextNode(a ? ': "' + line.text + '"' : ' would like a word: "' + line.text + '"'));
  if (a) bubbleSay(a.h, line.text, 6);
  el.hidden = false; SEEK = { p, until: simNow() + SEEK_SECS * 1000, line, come: !!a };
}
function seekEnd() { SEEK = null; SEEK_COME = null; const el = document.getElementById('seek'); if (el) el.hidden = true; }
// socialSeekAsk(id, { from, until, why }) (0.36.58, for section 21's first week): between from and until (absolute ship
// minutes), when that person is on your deck, near you and free (not at work, asleep or washing), they wave you over
// once, whatever your tier and the odds. A why with 'favour' in it also has them offer a favour that day. SHIP.social.seekAsks (saved)
function socialSeekAsk(id, o = {}) {
  socInit(); if (!SOC.idx.has(id) || !isFinite(o.from) || !isFinite(o.until)) return false;
  const A = SHIP.social.seekAsks || (SHIP.social.seekAsks = []);
  if (A.some(a => a.id === id && a.from === o.from)) return true;
  for (let k = A.length - 1; k >= 0; k--) if (A[k].until < shipNow() - 1440) A.splice(k, 1);   // asks over a day ago are gone (a bound for the save)
  A.push({ id, from: o.from, until: o.until, why: o.why || null, done: false }); return true;
}
const seekAskFor = (id, t) => (SHIP.social.seekAsks || []).find(a => a.id === id && !a.done && t >= a.from && t < a.until) || null;
// the asked-for waves (section 21): the person comes and finds you (section 10's crewComeTo walks them to a place by you,
// by lift from another deck), then waves you over; if they can't reach you within SEEK_WALK ship minutes, or you're
// busy when they arrive, they try again SEEK_RETRY minutes later, while the window lasts
const SEEK_WALK = 30, SEEK_RETRY = 20;
function socialSeekAsks(m) {
  const A = SHIP.social.seekAsks; if (!A || !A.length || typeof DECK_CREW === 'undefined' || typeof deckDef === 'undefined') return false;
  if (sleeping) return false;                           // not while you sleep (reviewer 1b)
  const t = shipNow(), P = player.obj.position;
  for (const ask of A) {
    if (ask.done || t < ask.from || t >= ask.until || !SOC.idx.has(ask.id)) continue;
    if (ask.walking) { if (t > ask.walkUntil) { ask.walking = false; ask.next = t + SEEK_RETRY; if (ask.stop) { try { ask.stop(); } catch (e) { } } } continue; }
    if (ask.next && t < ask.next) continue;
    const p = SOC.crew[SOC.idx.get(ask.id)], w = whereIs(p, t);
    if (!w || w.moving || ['work', 'sleep', 'wash'].includes(w.act)) { ask.next = t + 5; continue; }
    const a = DECK_CREW.find(x => x.p === p);
    if (a && Math.hypot(a.x - P.x, a.z - P.z) <= SEEK_NEAR) { if (CHAT || SEEK || SEEK_COME || sleeping) continue; ask.done = true; relGet(p.id).seekDay = SHIP.time.day; seekCome(p, a, m, ask.why); return true; }
    if (typeof crewComeTo !== 'function') continue;
    const pl = seekSpot(); if (!pl) continue;
    ask.walking = true; ask.walkUntil = t + SEEK_WALK;
    try {
      ask.stop = crewComeTo(p, pl.id, ag => {
        ask.walking = false;
        if (CHAT || SEEK || SEEK_COME || sleeping) { ask.next = shipNow() + 5; return; }
        if (ask.stop) { try { ask.stop(); } catch (e) { } }   // the visit's done its job: the last few steps are the walk-up's
        ask.done = true; relGet(p.id).seekDay = SHIP.time.day; seekCome(p, ag || DECK_CREW.find(x => x.p === p), Math.floor(shipNow()), ask.why);
      }, { until: t + SEEK_WALK });
    } catch (e) { ask.walking = false; ask.next = t + SEEK_RETRY; }
    if (ask.done) return true;                            // they were already there: the chip is up
  }
  return false;
}
function seekSpot() {                                    // somewhere by you for someone to walk to: a free seat (section 10's seatsBeside), else the nearest sitting place nobody's using
  const P = player.obj.position, L = (DECKS[deckDef.num] && DECKS[deckDef.num].places || []).filter(q => Array.isArray(q.at));
  const SEAT = ['mess-seat', 'lounge-seat', 'bench', 'common-room', 'garden', 'music'], used = new Set(DECK_CREW.map(a => a.goalId || (a.spot && a.spot.id)).concat([PLAYER_PLACE]).filter(Boolean));   // never your own seat
  let near = null, bd = 1e9; for (const q of L) { const c = cellPos(...q.at), d = Math.hypot(c.x - P.x, c.z - P.z); if (d < bd) { bd = d; near = q; } }
  if (near && typeof seatsBeside === 'function') { try { const id = seatsBeside(near.id, 1)[0], q = id && L.find(x => x.id === id); if (q && !used.has(q.id) && Math.hypot(cellPos(...q.at).x - P.x, cellPos(...q.at).z - P.z) <= SEEK_NEAR && Math.hypot(cellPos(...q.at).x - P.x, cellPos(...q.at).z - P.z) > .5) return q; } catch (e) { } }
  let best = null; bd = 1e9;                             // never a bed, a work station or a spot someone holds
  for (const q of L) { if (!SEAT.includes(q.type) || used.has(q.id)) continue; const c = cellPos(...q.at), d = Math.hypot(c.x - P.x, c.z - P.z); if (d > .5 && d < bd) { bd = d; best = q; } }   // not right on top of you
  return best && bd <= SEEK_NEAR ? best : null;
}
function socialSeek(m) {
  if (typeof DECK_CREW === 'undefined') return;
  if (SEEK_COME) { const a = DECK_CREW.find(x => x.p === SEEK_COME.p); if (!a || CHAT || SEEK || sleeping || seekPrivate() || simNow() > SEEK_COME.until) SEEK_COME = null; return; }   // on their way over (0.71.0); you went to wash: they leave it
  if (!SEEK && seekPrivate()) return;                    // none starts while you wash (0.71.1)
  if (!SEEK && socialSeekAsks(m)) return;
  const near = a => Math.hypot(a.x - player.obj.position.x, a.z - player.obj.position.z) <= SEEK_NEAR;
  if (SEEK) { if (SEEK.visit) return; const a = DECK_CREW.find(x => x.p === SEEK.p); if (!a || !near(a) || simNow() > SEEK.until || CHAT || SEEK.come && seekPrivate()) seekEnd(); return; }
  if (CHAT || sleeping) return;
  const day = SHIP.time.day;
  for (const a of DECK_CREW) {
    const p = a.p, mentor = socIntroOn() && p.id === SHIP.social.mentor && SHIP.time.min >= 1080 && SHIP.time.min < 1290;   // week 1: the escort checks in each evening
    const bye = relTier(p.id) >= 1 && (leavingSoon(p) ?? 99) <= 2 && !(SHIP.rel[p.id] && SHIP.rel[p.id].bye >= day - 1);   // leaving soon: they come to say goodbye
    if (seekAskFor(p.id, shipNow()) || seekBusy(p)) continue;   // an asked-for wave: socialSeekAsks brings them
    if (!SOC.idx.has(p.id) || !near(a) || !(mentor || bye || (relTier(p.id) >= 3 && socGate('d3')))) continue;
    const r = relGet(p.id); if (r.seekDay === day || schedU(p.seed ^ seekSalt(), m, 633) >= (mentor || bye ? .25 : SEEK_ODDS)) continue;
    const w = whereIs(p, shipNow()); if (!w || !(w.act === 'leisure' || w.act === 'off') || w.tag === 'tea') continue;
    r.seekDay = day; seekCome(p, a, m);
    return;
  }
}
// time together (0.36.2), as you play: eating with crew at your table (settled at mess seats within COMPANY_NEAR,
// section 15) or working near crew who are at work (within SOC_WORK_NEAR tiles of you while you do a job). After
// SOC_TOGETHER ship minutes with someone they get REL_PTS.meal or .work, once each a ship day (rel.mealDay, .workDay)
const SOC_TOGETHER = 10, SOC_WORK_NEAR = 3, SOC_WITH = new Map();   // crew id -> minutes together, this meal or job
function socialTogether(step) {
  const A = typeof ACT !== 'undefined' ? ACT : null, kind = A && A.phase === 'do' ? (A.kind === 'eat' ? 'meal' : ['job', 'fetch', 'make', 'stow'].includes(A.kind) ? 'work' : null) : null;
  if (!kind || typeof DECK_CREW === 'undefined') { SOC_WITH.clear(); return; }
  const day = SHIP.time.day, at = A.spot || player.obj.position, now = shipNow(), here = new Set();
  for (const a of DECK_CREW) {
    if (!SOC.idx.has(a.p.id) || !a.settled || Math.hypot(a.x - at.x, a.z - at.z) >= (kind === 'meal' ? COMPANY_NEAR : SOC_WORK_NEAR)) continue;
    if (kind === 'meal' ? (PLACE_OF.get(a.goalId) || {}).type !== 'mess-seat' : whereIs(a.p, now).act !== 'work') continue;
    here.add(a.p.id);
    const k = kind + ':' + a.p.id, n = (SOC_WITH.get(k) || 0) + step; SOC_WITH.set(k, n);
    const r = relGet(a.p.id), dk = kind + 'Day';
    if (n >= SOC_TOGETHER && r[dk] !== day) { r[dk] = day; relAdd(a.p.id, kind, REL_PTS[kind]); }
  }
  for (const k of [...SOC_WITH.keys()]) if (!here.has(k.slice(k.indexOf(':') + 1))) SOC_WITH.delete(k);
}
function socialNew() { socInit(); socReset(Math.floor(shipNow() / 60)); }   // section 13's New game

// ---- for the device's apps (0.36.6; section 19 draws them): plain data, nothing drawn here ----
// crewContacts() -> everyone you've met (or all with { all: true }), closest first: [{ id, name, role, dept, tier,
//   tierName, pts, toNext (points to the next tier, or null), met, lastTalk, known: [what you know], where }].
//   where: { deck, room, act, placeId } only for acquaintances and up, or anyone on duty in a public place (the plan: Maps
//   shows people once you're acquaintances, or on public duty); else null
// newsFeed() -> what you've heard, newest first: [{ id, line, from (name or null), at, kind }]
const PUBLIC_WORK = new Set(['galley', 'infirmary', 'works']);   // on duty where anyone may find them
function crewWhere(p, t = shipNow()) {
  const w = whereIs(p, t); if (!w || w.moving || w.act === 'sleep' || w.act === 'wash') return null;   // asleep or washing: private (as the device's Maps)
  const pl = w.placeId && schedData().byId.get(w.placeId), rm = pl && DECKS[pl.deck] && (DECKS[pl.deck].rooms || {})[pl.room];
  return { deck: w.deck, room: rm ? rm.name : null, act: w.act, placeId: w.placeId || null };
}
function crewContacts({ all = false } = {}) {
  socInit(); const t = shipNow(), out = [];
  for (const p of SOC.crew) {
    const r = SHIP.rel[p.id]; if (!all && !(r && r.met !== null)) continue;
    if (!socAboard(p)) continue;                          // moved on, or not here yet: movedOn() lists those who left
    const tier = relTier(p.id), pts = r ? r.pts : 0, w = whereIs(p, t);
    const show = tier >= 1 || (w && w.act === 'work' && PUBLIC_WORK.has(p.dept));
    out.push({ id: p.id, name: p.name, role: p.role, dept: p.dept, tier, tierName: REL_NAMES[tier], pts, toNext: tier < 4 ? Math.ceil(REL_TIERS[tier + 1] - pts) : null,
               met: r ? r.met : null, lastTalk: r ? r.lastTalk : null, known: r ? r.known.filter(k => k !== 'news' && k !== 'work' && k[0] !== '@') : [], where: show ? crewWhere(p, t) : null });
  }
  return out.sort((a, b) => b.pts - a.pts || (a.name < b.name ? -1 : 1));
}
function newsFeed() {
  socInit();
  return SHIP.heard.slice().reverse().map(h => { const it = NEWS.find(x => x.id === h.id), p = h.from && SOC.idx.has(h.from) ? SOC.crew[SOC.idx.get(h.from)] : null;
    return { id: h.id, line: h.line, from: p ? p.name : null, at: h.at, kind: it ? it.kind : (h.id.split(':')[0] || 'news') }; });
}
// the Crew app (0.36.8), on the device engineer's deviceApp (section 19; nothing without it): the people you've met,
// closest first, with where they are when you may know it; tap one for what you know about them
let CREW_PICK = null;
const shipNews = (limit = 20) => newsFeed().slice(0, limit).map(x => ({ text: x.line, from: x.from, at: x.at }));   // the Ship app's news feed (section 19)
if (typeof deviceApp === 'function') deviceApp({ id: 'crew', title: 'Relationships', short: 'People', icon: 'people', order: 50,   // 'Crew' until 0.28.44 (the user's); the tile says People (0.28.57: Relationships overflowed it)
  view: () => {
    const c = CREW_PICK && crewContacts({ all: true }).find(x => x.id === CREW_PICK);
    if (c) return { title: c.name, blocks: [
      { kind: 'text', text: c.role + '. ' + c.tierName[0].toUpperCase() + c.tierName.slice(1) + (c.toNext !== null ? ' (' + c.toNext + ' more to ' + REL_NAMES[c.tier + 1] + ')' : '') + '.' },
      ...(typeof knowBlocks === 'function' ? knowBlocks(c.id) : [{ kind: 'list', rows: c.known.length ? c.known.map(k => ({ text: k })) : [{ text: 'Nothing yet. Ask them about themselves.' }] }]),   // what you know, by section (20c)
      { kind: 'buttons', items: [{ label: 'Where are they?', action: { app: 'roster', who: c.id } }].concat(c.met !== null ? [{ label: 'Meet up', action: { app: 'appointments', with: c.id } }] : [], [{ label: 'Back', action: { app: 'crew', do: 'back' } }]) }] };
    const cs = crewContacts(), mo = movedOn(), gone = mo.length ? [{ kind: 'text', text: 'Moved on', mark: 'head' }, { kind: 'list', rows: mo.map(x => ({ text: x.name, sub: x.to ? 'Now on the ' + x.to.replace(/^the /i, '') : 'Transferred', mark: 'past' })) }] : [];
    return { title: 'Relationships', blocks: (cs.length ? [{ kind: 'list', rows: cs.map(x => ({ text: x.name, sub: x.tierName + (x.where ? ' · ' + deckWord(x.where.deck) + (x.where.room ? ', ' + x.where.room : '') : ''), mark: x.tier >= 3 ? 'up' : null, action: { app: 'crew', do: 'show', arg: x.id } })) }]
      : [{ kind: 'text', text: 'Nobody yet. Tap someone aboard to say hello.' }]).concat(gone) };
  },
  act: (verb, arg) => { CREW_PICK = verb === 'show' ? arg : null; } });
SIM_ADVANCE.push((from, to) => { socialTo(to); });
// ---- chat cards (0.36.1): tap a crew member ----
// chatLine(p, t) -> { text, kind, news?, say }: one line, picked in order of what matters: news they know that you
// haven't heard → how they feel (crewFeeling, told as what you notice) → something about where they are → a life
// detail (acquaintances and up) → a greeting by how well they know you. say: false when it's what you notice, not
// what they say. Lines are templates filled from the simulation, picked with schedU per person, day and hour, so a
// second tap in the same hour says the same and the next hour moves on.
// chatOpen(p) shows the card (section 10's crew tap): their name, role and tier, the line, and the buttons Chat
// (once a ship day: social for you through playerChat, +2), Ask about (news, work, home: each fills a line of
// SHIP.rel[id].known for the Crew app), Help? (favourOf: a favour to accept in person, or "Done: here you go" to hand
// one back) and Meet up (Appointments with them picked, once the device has it). The look is a plain panel for now;
// the device engineer's skin (section 19) takes it over through CHAT_SKIN.
const CHAT_GREET = linesLegacy('greet');                 // by tier (content/banks/old.lines, section 22)
// where they are: [test on whereIs, lines]; {room} is the room's name
const CHAT_NEAR = linesLegacy('near');
// a life detail by habit (acquaintances and up), then by department
const CHAT_LIFE = linesLegacy('life');
const CHAT_DEPT = linesLegacy('dept');
const chatName = () => (typeof ROSTER_PLAYER !== 'undefined' && ROSTER_PLAYER.first) || 'cadet';
// the first story arcs (0.36.10; plans/pillar3-plan.md "Story crew arcs"): Tomas (homesick, and a call home that goes
// wrong), Pell (a hobby that becomes a little show in the music room) and Rina (a worry about her gran). Four beats
// each, opening at acquaintance, colleague, friend and close friend: beat i is told the first time their card opens
// once you're at tier i + 1, at most one a ship day (rel.arc beats told, rel.arcDay). mail: a message from them
// `after` ship minutes later (SHIP.social.mail, sent by socialTick). They never contradict the roster's details.
const STORY_ARCS = {
  tomas: [
    { say: 'Do you ever miss home? I keep staring at that star map above my bunk. Every place on it is somewhere I\'ve never been.' },
    { say: 'My brother\'s birthday is on Thursday. I\'m going to call him from the booths on Deck 3. First proper call since I left.' },
    { say: 'The call dropped halfway through. Relay lag. He thought I hung up on him. Now he won\'t answer.',
      mail: { after: 180, subject: 'Sorry about earlier', body: 'Sorry I was so quiet. The call home really got to me. Thanks for listening, though. It helped more than you know. Tomas' } },
    { say: 'He wrote back! He\'s taped a star map to his ceiling, same as mine. Says we can look at the same sky now. Sort of.',
      mail: { after: 60, subject: 'Observatory?', body: 'If you\'re free on observatory night, come up to Deck 2. I want to show you where home is on the big window. Tomas' } },
  ],
  pell: [
    { say: 'Want to see something? I made this out of my tin of spare screws. It plays a tune. Badly.' },
    { say: 'I found an old music box at the swap meet. Rusted solid. I\'ve nearly got the chime working again.' },
    { say: 'Brennan says I can show my music boxes in the music room after dinner one night. Is that mad? You\'d come, right?',
      mail: { after: 120, subject: 'Music boxes!', body: 'It\'s happening: my music boxes, in the Deck 4 music room after dinner some night this week. Bring people. Or just you. Pell' },
      show: { id: 'pell-show', name: 'Pell\'s music boxes', at: [1230, 1290], where: [{ deck: 4, pool: 'music' }], hostAnim: 'play', chance: .12,
              mail: 'Tomorrow at 20:30 in the Deck 4 music room: my music boxes, all of them, wound up at once. Bring people. Or just you. Pell',
              ask: 'Coming to see my music boxes tonight?', here: 'This one plays a waltz. Mostly.', thanks: 'You watch Pell wind up his music boxes one by one. The little room laughs and claps.' } },
    { afterShow: true, say: p => { const n = showCrowd(p, 'pell-show'), w = n > 12 ? n : ['Nobody', 'One person', 'Two people', 'Three people', 'Four people', 'Five people', 'Six people', 'Seven people', 'Eight people', 'Nine people', 'Ten people', 'Eleven people', 'Twelve people'][n];
      return n ? w + (n > 12 ? ' people' : '') + ' came to see the music boxes. ' + (n > 3 ? n + '! ' : '') + 'I think they actually liked them.' + (showJoined(p, 'pell-show') ? ' And you came. That meant a lot.' : '') : 'Hardly anyone came to the music boxes. That\'s fine. I\'ll try again some time.'; } },
  ],
  rina: [
    { say: 'My gran taught me Tiles. Cheated the whole time. She hasn\'t been well lately.' },
    { say: 'My sister says Gran\'s gone into hospital. She\'s the doctor in the family. I\'m just the one who worries.' },
    { say: 'No news from the station for two days. I haven\'t slept. Talk to me about anything else, would you?',
      mail: { after: 240, subject: 'Thank you', body: 'Thanks for keeping me company today. Still no news, but I feel steadier. You\'re a good one. Rina' } },
    { say: 'Gran\'s home! First night back she beat my sister at Tiles. Cheated, obviously. I\'ve never been so happy to hear it.',
      mail: { after: 30, subject: 'Tiles?', body: 'Gran sends her love, apparently, to "the friend who listened". Come and lose to me at Tiles in the common room some evening. Rina' } },
  ],
};
// how many crew went to a beat's show (their plans that day), and whether you joined in (section 18's SHIP.events.joined)
function showCrowd(p, id) {
  const d = SHIP.rel[p.id] && SHIP.rel[p.id].showDay; if (!d) return 0;
  return SOC.crew.filter(q => q !== p && planDay(q, d).some(s => s.tag && (s.tag === 'ev-' + id || s.tag.startsWith('ev-' + id + '-')))).length;
}
const showJoined = (p, id) => { const d = SHIP.rel[p.id] && SHIP.rel[p.id].showDay; return !!(d && SHIP.events && SHIP.events.joined.includes(id + '@' + d)); };
function arcBeat(p, t = shipNow()) {
  const arc = STORY_ARCS[p.id], r = SHIP.rel[p.id]; if (!arc || !r) return null;
  const n = r.arc || 0, day = Math.floor(t / 1440) + 1;
  if (typeof momentOwnsBeat === 'function' && momentOwnsBeat(p.id, n)) return null;   // a moment tells it (20c)
  if (arc[n] && arc[n].afterShow && r.showDay && day <= r.showDay) return null;   // Pell's last beat waits for his show
  return n < arc.length && r.tier >= n + 1 && (r.arcDay || 0) < day ? arc[n] : null;
}
function arcTold(p, beat = arcBeat(p)) {                  // the card showed their next beat, or 20c's moment told it (beat given)
  if (!beat) return;
  const r = SHIP.rel[p.id]; r.arc = (r.arc || 0) + 1; r.arcDay = SHIP.time.day;
  if (beat.afterShow && showJoined(p, 'pell-show')) memAdd(p.id, 'show.pell-show');   // you came to their show
  // a beat with a show: a real one-off gathering the next evening (section 18's eventOneOff), which sends its own Mail
  if (beat.show && typeof eventOneOff === 'function' && eventOneOff({ ...beat.show, day: SHIP.time.day + 1, host: p.id, from: p.name })) { r.showDay = SHIP.time.day + 1; return; }
  if (beat.mail) SHIP.social.mail.push({ at: Math.floor(shipNow()) + beat.mail.after, from: p.name, subject: beat.mail.subject, body: beat.mail.body });
}
// appointments (0.36.13; the device's Appointments, section 19, and the crew side, section 14's apptList): one you
// kept gives REL_PTS.appt to each person in it, once (a.socKept); one you missed costs nothing, but the next time you
// tap them they mention it (apptMissedBy, a.socSaid), within three days. The two flags ride on the appointment, saved
// with the device's part of the save
function socialAppts() {
  if (typeof apptList !== 'function') return;
  for (const a of apptList()) {
    if (a.occ) continue;                                 // section 18's occasions (summons, the Captain's table, Calder's talk) have their own effects and words
    if (a.status === 'kept' && !a.socKept && Array.isArray(a.with)) { a.socKept = true; for (const id of a.with) if (SOC.idx.has(id)) { relAdd(id, 'appt', REL_PTS.appt); memAdd(id, a.kind === 'invite' && a.trad ? 'came.' + a.trad : 'appt.' + (a.kind || 'social'), { cls: 'medium' }); if (a.kind === 'invite' && a.trad) relAdd(id, 'appt', 2); if (a.host) hostCame(a, SOC.crew[SOC.idx.get(id)]); } repAdd(null, 0, { kindness: 1 }); }
    if (a.status === 'missed' && !a.socMem && Array.isArray(a.with)) { a.socMem = true; repAdd(null, 0, { kindness: -2 });
      for (const id of a.with) if (SOC.idx.has(id)) { memAdd(id, 'missed.' + a.id); const q = SOC.crew[SOC.idx.get(id)]; if (['officer', 'chief', 'xo', 'captain'].includes(q.rank)) repAdd(q.dept, -1); } }
  }
}
function apptMissedBy(p, t = shipNow()) {
  if (typeof apptList !== 'function') return null;
  return apptList().find(a => a.status === 'missed' && !a.occ && !a.socSaid && Array.isArray(a.with) && a.with.includes(p.id) && t - a.at < 3 * 1440 && t >= a.at) || null;
}
function apptRemark(p, a, t = shipNow()) {
  const pl = typeof apptPlace === 'function' ? apptPlace(a) : null, rm = pl && ((DECKS[pl.deck].rooms || {})[pl.room] || {}).name;
  const when = Math.floor(a.at / 1440) === Math.floor(t / 1440) ? 'earlier' : Math.floor(a.at / 1440) === Math.floor(t / 1440) - 1 ? 'yesterday' : 'the other day';
  const at = rm ? ' at the ' + rm.toLowerCase() : '';
  return ['Waited for you' + at + ' ' + when + '. No harm done.', 'I was' + at + ' ' + when + '. Thought you\'d forgotten me!', 'Missed you' + at + ' ' + when + '. Another time?'][Math.floor(schedU(p.seed, Math.floor(t / 60), 642) * 3)];
}
function socialMail(now) {                               // story Mail that's due (socialTick)
  const due = SHIP.social.mail.filter(x => x.at <= now); if (!due.length || typeof mailSend !== 'function') return;
  SHIP.social.mail = SHIP.social.mail.filter(x => x.at > now);
  for (const x of due) mailSend(x);
}
function chatLine(p, t = shipNow(), peek = false) {    // peek: only looking ahead (Chat's next thing), so the dialogue engine notes nothing
  socInit();
  { const sl = typeof sickChatLine === 'function' ? sickChatLine(p, t, peek) : null; if (sl) return sl; }   // get well / glad you're better (0.61.5)
  const h = Math.floor(t / 60), U = k => schedU(p.seed, h, k), pick = (a, k) => a[Math.floor(U(k) * a.length)], tier = relTier(p.id);
  const ctx = { t, tier, peek, newHere: newHere(p, Math.floor(t / 1440) + 1), leaving: leavingSoon(p, Math.floor(t / 1440) + 1) }, eng = (kind, x) => { const l = socLine(p, kind, x ? { ...ctx, ...x } : ctx); return l ? { text: l.text, kind, say: true, line: l } : null; };
  const fill = s => s.replace('{me}', chatName());
  const missed = apptMissedBy(p, t); if (missed) return { text: apptRemark(p, missed, t), kind: 'missed', appt: missed.id, say: true };
  if (p.id === 'holt' && typeof eventMod === 'function' && (() => { try { return eventMod('effect', 'guests', t); } catch (e) { return null; } })())
    return { text: ['Veyli on my ship. Don\'t expect me to smile about it.', 'I\'m keeping an eye on our guests. Someone has to.', 'The Captain wants courtesy. I\'m being courteous. This is my courteous face.'][Math.floor(schedU(p.seed, Math.floor(t / 60), 643) * 3)], kind: 'guests', say: true };
  const lv = ctx.leaving, rb = SHIP.rel[p.id]; if (lv !== null && lv <= 2 && tier >= 1 && !(rb && rb.bye >= Math.floor(t / 1440) - 1)) {   // leaving in a day or two: their goodbye
    const gm = typeof goodbyeMoment === 'function' ? goodbyeMoment(p, t) : null; return { text: gm ? (gm.hint || byeLine(p)) : byeLine(p), kind: 'goodbye', moment: gm ? gm.id : undefined, say: true }; }
  if (socIntroOn()) { const l = eng('week1', { escort: p.id === SHIP.social.mentor }); if (l) return l; }   // onboarding's week-1 lines
  const G = SHIP.social.guide; if (p.id === 'calder' && G && !G.told && !G.end) return { text: guideAskLine(G), kind: 'guide', say: true };   // A10: Calder assigns you a newcomer
  const gq = guideQuestion(p, t, eng); if (gq) return gq;   // the newcomer you guide asks you something
  const mo = typeof momentReady === 'function' && socGate('done') ? momentReady(p, t) : null;   // a moment is ready (20c): its hint, and Sit with them
  if (mo) { const hint = typeof momentHint === 'function' ? momentHint(mo) : typeof MOMENTS !== 'undefined' && MOMENTS[mo] && MOMENTS[mo].hint, l = hint ? null : eng('hint');
    return { text: hint || (l ? l.text : 'Got a minute? Properly, I mean.'), kind: 'hint', moment: mo, say: true, line: l ? l.line : undefined }; }
  const beat = arcBeat(p, t); if (beat) return { text: typeof beat.say === 'function' ? beat.say(p) : beat.say, kind: 'story', say: true };
  const fd = feudOf(p.id, t); if (fd && !fd.f.talked.includes(p.id)) { const o = shortName(SOC.crew[SOC.idx.get(fd.other)]);
    return { text: ['Don\'t get me started on ' + o + '.', o + ' and I had words. I\'d rather not talk about it.', 'If you see ' + o + ', tell them... no, never mind.'][Math.floor(schedU(p.seed, Math.floor(t / 60), 640) * 3)], kind: 'feud', say: true }; }
  if (isBirthday(p, t)) return { text: pick(['It\'s my birthday today!', 'Guess whose birthday it is?', 'Another year older today. Don\'t tell anyone.'], 610), kind: 'birthday', say: true };
  const inv = inviteFor(p, Math.floor(t / 1440) + 1); if (inv) return { text: inviteLine(p, inv), kind: 'invite', invite: inv, say: true };
  if ((SHIP.mem[p.id] || []).some(m => !m[3]) && U(645) < .6) { const l = eng('callback'); if (l) return l; }   // a memory of you, said once
  const heard = new Set(SHIP.heard.map(x => x.id));
  const news = newsKnownBy(p, t).find(x => !heardIt(x) && !(x.about === p.id && x.kind !== 'fault') && x.about !== 'you');
  if (news && U(611) < .8) return { text: pick(news.lines, 612), kind: 'news', news: news.id, say: true };
  if (SHIP.social.cues.length && U(646) < .5) { const l = eng('cue'); if (l) return l; }   // what happened on the ship
  const f = crewFeeling(p, t); if (f && !/birthday/.test(f) && U(613) < .7) return { text: f, kind: 'feel', say: false };
  const w = typeof whereIs === 'function' ? whereIs(p, t) : null;
  if (w && U(614) < .45) {
    const pl = w.placeId && schedData().byId.get(w.placeId), rm = pl && DECKS[pl.deck] && DECKS[pl.deck].rooms && DECKS[pl.deck].rooms[pl.room];
    const l = eng('near', { act: w.act, room: rm ? rm.name : null, placeId: w.placeId || null }); if (l) return l;
    const lines = CHAT_NEAR.find(([test]) => test(w))[1].filter(s => rm || !/\{room\}/.test(s));
    if (lines.length) return { text: pick(lines, 615).replace('{room}', rm ? rm.name.toLowerCase() : ''), kind: 'near', say: true };
  }
  if (tier >= 1 && U(616) < .6) {
    const e = eng('life'); if (e) return e;
    const hs = (typeof habitsOn === 'function' ? habitsOn(p, Math.floor(t / 1440) + 1) : p.habits || []).filter(x => CHAT_LIFE[x]);
    const l = hs.length && U(617) < .75 ? CHAT_LIFE[pick(hs, 618)] : CHAT_DEPT[p.dept];
    if (l) return { text: l, kind: 'life', say: true };
  }
  if (tier >= 1 && U(647) < .3) { const l = eng('joy') || (['best', 'friend', 'partner', 'mentor', 'mentee'].some(k => socialFill(p, k)) ? eng('about') : null); if (l) return l; }   // their joy, or a crewmate they're close to
  return socGreet(p, t, peek);
}
const chatGreet = (p, t = shipNow()) => { const own = typeof lineFor === 'function' && VOICE[p.id] && VOICE[p.id].lines && lineFor(p, 'greet', { t, peek: Math.floor(t / 60) !== Math.floor(shipNow() / 60) }); if (own) return { text: own.text, kind: 'greet', say: true }; const a = CHAT_GREET[relTier(p.id)]; return { text: a[Math.floor(schedU(p.seed, Math.floor(t / 60), 619) * a.length)].replace('{me}', chatName()), kind: 'greet', say: true }; };
// favours (0.36.2 fills this in): the favour that person has for you, or null
// favours (0.36.3) on the systems engineer's job list (section 17: favourPost / favourAccept / favourDecline /
// favourTurnIn / favoursOf / favourById; inert until it's there). favourOf(p) -> their open favour (offered or
// yours), else today's idea for one (not yet posted: { idea: true, title, ask, post }), else null. Ideas come from
// their life: something left behind where they spent yesterday's free time (fetch it back to them), or a lamp over
// their work station that needs swapping (the 'lamp' chore). Acquaintances and up ask; the better they know you,
// the more often (FAVOUR_ODDS per ship day, schedU k 624-628), and only one a day each.
const FAVOUR_ODDS = [0, .2, .3, .4, .45];
const FAVOUR_THINGS = ['datapad', 'mug', 'jacket', 'notebook', 'glasses case', 'stylus', 'scarf', 'water bottle'];
function favourOf(p) {
  if (typeof favourPost !== 'function' || typeof favoursOf !== 'function') return null;
  const open = favoursOf(p.id)[0]; if (open) return open;
  if (!socGate('d2')) return null;                       // the first week: favours from Tuesday
  const r = relGet(p.id), d = SHIP.time.day, U = k => schedU(p.seed, d, k), tier = relTier(p.id);
  const asked = (SHIP.social.seekAsks || []).some(a => a.id === p.id && /favour/.test(a.why || '') && Math.floor(a.from / 1440) + 1 === d);   // section 21: their favour that day
  if (r.favDay === d || (!asked && U(624) >= FAVOUR_ODDS[tier] * (repAskedFor(p.dept) ? 1.5 : 1))) return null;   // 50% more often where you're well thought of
  const S = schedData(), left = planDay(p, d - 1).filter(s => s.placeId && SOCIAL_TYPES.has(s.type) && s.type !== 'servery-queue').map(s => S.byId.get(s.placeId)).filter(pl => pl && DECKS[pl.deck]);
  if (left.length && U(625) < .6) {
    const pl = left[Math.floor(U(626) * left.length)], room = ((DECKS[pl.deck].rooms || {})[pl.room] || {}).name || 'the ' + pl.type, thing = FAVOUR_THINGS[Math.floor(U(627) * FAVOUR_THINGS.length)];
    return { idea: true, title: 'Fetch ' + shortName(p) + '\'s ' + thing, ask: 'I think I left my ' + thing + ' in the ' + room.toLowerCase() + ' yesterday. Could you bring it to me?',
             post: { from: p.id, title: 'Fetch ' + shortName(p) + '\'s ' + thing + ' (' + room + ', ' + deckIn(pl.deck) + ')', bring: thing, stops: [{ deck: pl.deck, placeId: pl.id, mins: 2, tag: 'pickup' }] } };
  }
  if (p.work && p.work.place && U(628) < .7)
    return { idea: true, title: 'A lamp for ' + shortName(p), ask: 'The lamp over my station keeps flickering. Could you swap it when you get a chance?',
             post: { from: p.id, title: 'Swap the lamp at ' + shortName(p) + '\'s station', kind: 'lamp', where: p.work.place, deck: p.work.deck, parts: ['lamp'] } };
  return null;
}
// the card. CHAT_SKIN.draw(el, view) is the device engineer's hook: view = { who, role, tier, line, say, buttons:
// [{ id, label }] }; until there is one, chatDraw below draws a plain panel like the toast
let CHAT = null;
const CHAT_SKIN = { draw: null };
function chatEl() {
  let el = document.getElementById('chat');
  if (el) return el;
  const st = document.createElement('style');
  st.textContent = '#chat{position:fixed;left:50%;bottom:18px;transform:translateX(-50%);width:min(440px,calc(100% - 24px));z-index:3;background:var(--glass);border:1px solid var(--line);border-radius:14px;padding:12px 16px;-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px)}'
    + '#chat b{display:block;font-size:14.5px;color:#bdeee6;font-weight:600}#chat small{display:block;font-size:12px;color:#8fa6ab;margin:1px 0 6px}'
    + '#chat p{margin:0 0 10px;font-size:13.5px;color:#cfd9dc;line-height:1.45}#chat p.feel{font-style:italic;color:#a9bcc0}'
    + '#chat .row{display:flex;gap:6px;flex-wrap:wrap}#chat button{flex:1 1 auto;min-height:36px;padding:6px 10px;border-radius:10px;border:1px solid var(--line);background:rgba(255,255,255,.06);color:#e6f0f1;font:inherit;font-size:13px}'
    + '#chat button:disabled{opacity:.45}#chat .x{position:absolute;top:6px;right:8px;flex:none;min-height:0;border:0;background:none;font-size:18px;color:#8fa6ab}';
  document.head.appendChild(st);
  el = document.createElement('div'); el.id = 'chat'; el.hidden = true; document.body.appendChild(el);
  el.addEventListener('pointerdown', e => e.stopPropagation());   // taps on the card never reach the deck
  return el;
}
function chatDraw(el, v) {
  el.innerHTML = '';
  const add = (tag, txt, cls) => { const e = document.createElement(tag); if (txt !== undefined) e.textContent = txt; if (cls) e.className = cls; el.appendChild(e); return e; };
  add('button', '×', 'x').onclick = () => chatClose();
  add('b', v.who); add('small', v.role + ' · ' + v.tier);
  add('p', v.say ? '"' + v.line + '"' : v.line, v.say ? '' : 'feel');
  const row = add('div', undefined, 'row');
  for (const b of v.buttons) { const e = document.createElement('button'); e.textContent = b.label; e.disabled = !!b.off; e.onclick = () => chatDo(b.id); row.appendChild(e); }
}
function chatShow() {
  const C = CHAT, p = C.p, r = relGet(p.id), today = SHIP.time.day;
  const f = C.fav, ready = f && !f.idea && f.status === 'claimed' && f.claimedBy === 'you' && (f.workDone || !f.stops.length);
  const intro = C.ask === 'intro' && typeof introOptions === 'function' ? introOptions(p) : [];   // "Do you know...?" (20c's introductions)
  const buttons = C.ask === 'intro' ? intro.slice(0, 3).map(x => ({ id: 'intro:' + x.id, label: x.name })).concat([{ id: 'back', label: 'Back' }])
    : C.ask ? [{ id: 'ask-news', label: 'News' }, { id: 'ask-work', label: 'Their work' }, { id: 'ask-home', label: 'Home' }].concat(typeof introOptions === 'function' && introOptions(p).length ? [{ id: 'ask-intro', label: 'Do you know…?' }] : [], [{ id: 'back', label: 'Back' }])
    : C.offer ? [{ id: 'fav-yes', label: 'I\'ll do it' }, { id: 'fav-no', label: 'Not now' }]
    : C.talk && !C.talk.end ? (C.talk.ask ? TALK_REPLIES.map(k => ({ id: 'reply:' + k, label: talkReply(C, k) })) : [{ id: 'talk-stop', label: talkText('talk.button.stop', 'Stop') }])   // Talk a while (0.36.82): the replies, else Stop
    : [{ id: 'chat', label: r.chatDay === today ? talkText('talk.done.hello', 'Said hello today') : talkText('talk.button.hello', 'Say hello'), off: r.chatDay === today },
       { id: 'talk', label: r.talkDay === today ? talkText('talk.done.talk', 'Talked today') : talkText('talk.button.talk', 'Talk a while'), off: r.talkDay === today || !!C.going }, { id: 'ask', label: 'Ask about…' },
       { id: 'help', label: ready ? 'Done: here you go' : 'Help?' }, { id: 'meet', label: 'Meet up' }];
  const talking = C.talk && !C.talk.end;   // while you talk, only the talk's own buttons
  if (!C.ask && !C.offer && !talking && C.line.kind === 'newcomer' && Array.isArray(C.line.answers)) buttons.splice(0, buttons.length, ...C.line.answers.slice(0, 3).map((a, k) => ({ id: 'nq:' + k, label: a })));   // A10: helpful, funny, honest
  if (!C.ask && !C.offer && !talking && C.line.kind !== 'newcomer' && hostOk(p)) buttons.push(r.hostDay === today ? { id: 'host', label: 'Asked over', off: true } : { id: 'host', label: 'Come over' });   // A11: your own room
  if (!C.ask && !C.offer && !talking && p.id === 'calder' && guideOn()) buttons.push({ id: 'guide-back', label: 'Hand ' + shortName(socP(guideOn().id)) + ' back' });
  if (!C.ask && !C.offer && !talking && C.line.moment && typeof momentShow === 'function') buttons.splice(1, 0, { id: 'sit', label: 'Sit with them' });   // a moment is ready (20c)
  const gift = !C.ask && !C.offer && !talking && giftInHands(); if (gift) buttons.push(r.giftWeek === socWeek() + 1 ? { id: 'give', label: 'Given this week', off: true } : { id: 'give', label: 'Give ' + gift });
  if (!C.ask && !C.offer && !talking && typeof caseAskButton === 'function') { const cb = caseAskButton(p); if (cb) buttons.push(cb); }
  if (!C.ask && !C.offer && !talking && typeof shopGiveButton === 'function') { const sb = shopGiveButton(p); if (sb) buttons.push(sb); }   // 24j: Give the thing you made them (M10)   // 24k P2: Ask about the fault (only a witness, only after Tomas's word)
  const v = { who: p.name, role: p.role, tier: REL_NAMES[relTier(p.id)], line: C.line.text, say: C.line.say !== false, buttons };
  const el = chatEl(); el.hidden = false;
  (CHAT_SKIN.draw || chatDraw)(el, v);
  if (C.talk) talkMeter(el, C.talk);                     // the Talk a while meter, over the buttons (either skin)
}
function chatOpen(p, greet, line) {                       // greet: they came to you (socialSeek), so they say hello first; line: one to open with (a visit)
  if (!p || !p.id) return false;
  socInit(); if (!SOC.idx.has(p.id)) return false;
  const w = typeof whereIs === 'function' ? whereIs(p, shipNow()) : null;
  if (w && w.act === 'sleep') { chatClose(); toast(p.name, p.role + '. Fast asleep. Better not wake them.'); return true; }
  const r = relGet(p.id); if (r.met === null) r.met = Math.floor(shipNow());
  const a = typeof DECK_CREW !== 'undefined' && DECK_CREW.find(x => x.p === p), d = a ? Math.hypot(a.x - player.obj.position.x, a.z - player.obj.position.z) : 0;
  CHAT = { p, line: line || (greet ? socGreet(p) : chatLine(p)), ask: false, fav: favourOf(p), at: shipNow(), reach: Math.max(4, d + 1.5) };   // walk off further than that and it closes
  if (CHAT.line.news) playerHeard(CHAT.line.news, p.id);
  if (CHAT.line.kind === 'story') arcTold(p);
  if (CHAT.line.kind === 'invite') CHAT.line.invite.said = true;
  if (CHAT.line.kind === 'goodbye') relGet(p.id).bye = SHIP.time.day;
  if (CHAT.line.kind === 'guide') SHIP.social.guide.told = true;
  if (CHAT.line.kind === 'missed') { const a = apptMissedBy(p); if (a) a.socSaid = true; }
  if (TALK_KEEP.has(CHAT.line.kind)) CHAT.checked = Math.floor(shipNow());   // something that matters first; "got to go" can wait a minute
  else talkGoCheck(CHAT, false);                         // their shift's in five: they say so (0.36.82)
  if (typeof toastEl !== 'undefined') toastEl.classList.remove('show');
  chatShow();
  return true;
}
function chatClose() { if (CHAT && CHAT.talk && !CHAT.talk.end) talkEnd(CHAT, 'walk', true); CHAT = null; const el = document.getElementById('chat'); if (el) el.hidden = true; }
const chatSay = (text, say = true) => { CHAT.line = { text, say }; chatShow(); };
function chatDo(id) {
  const C = CHAT; if (!C) return;
  const p = C.p, r = relGet(p.id), U = k => schedU(p.seed, Math.floor(shipNow() / 60), k), pick = (a, k) => a[Math.floor(U(k) * a.length)];
  if (id === 'chat') {
    if (r.chatDay === SHIP.time.day) return;
    r.chatDay = SHIP.time.day;
    if (typeof playerChat === 'function') playerChat(p);  // section 15: social for you (half when you're grubby)
    const before = r.tier, after = relAdd(p.id, 'chat', REL_PTS.hello);   // Say hello, the old Chat: +1 (0.36.82; was REL_PTS.chat)
    const grubby = SHIP.player && SHIP.player.needs && typeof NEED_LOW !== 'undefined' && SHIP.player.needs.hygiene < NEED_LOW;
    memAdd(p.id, grubby ? 'grubby' : 'chat'); if (isBirthday(p, shipNow())) { memAdd(p.id, 'bday'); repAdd(null, 0, { spirit: 2 }); }
    repAdd(null, 0, p.dept !== 'works' ? { spirit: .5 } : null, 'chats'); if (SHIP.time.min >= 1380 || SHIP.time.min < 300) repInit().cnt.night = (repInit().cnt.night || 0) + 1;
    const fd = feudOf(p.id), made = fd ? feudTalk(p) : null;   // a falling-out: talking it over (small dramas)
    let l = null;                                       // the next thing on their mind: something they say, not the same again
    if (made) l = { text: made, say: false };
    else if (fd) l = { text: ['Maybe I was a bit hard on ', 'I suppose I should talk to ', 'It\'s silly, really. I miss chatting with '][Math.floor(schedU(p.seed, SHIP.time.day, 641) * 3)] + shortName(SOC.crew[SOC.idx.get(fd.other)]) + '.', say: true };
    let kk = 0; for (let k = 1; k <= 6 && (!l || l.say === false || l.text === C.line.text) && !fd; k++) { l = chatLine(p, shipNow() + 60 * k, true); kk = k; }
    const hl = !fd && !TALK_KEEP.has(l.kind) && l.kind !== 'week1' && l.kind !== 'callback' ? socLine(p, 'hello', { t: shipNow(), tier: after, warmth: warmth(p.id) }) : null;   // their answer to hello (0.36.82), unless something matters more
    if (hl) l = { text: hl.text, kind: 'hello', say: true };
    else if (kk && l.line) l = chatLine(p, shipNow() + 60 * kk);   // the dialogue engine's line that's said: now it may note it
    if (l.news) playerHeard(l.news, p.id);
    if (l.kind === 'story') arcTold(p);
    if (l.kind === 'missed') { const a = apptMissedBy(p); if (a) a.socSaid = true; }
    if (l.kind === 'guide') SHIP.social.guide.told = true;
    if (l.kind === 'newcomer') { C.line = l; return chatShow(); }   // their question, with your answers
    chatSay((l.say === false ? 'You chat for a while. ' + l.text : l.text) + (grubby ? ' ' + shortName(p) + ' wrinkles their nose a little.' : '') + (after > before ? ' (You\'re ' + REL_NAMES[after] + 's now.)' : ''), l.say !== false && !grubby && after <= before);
  } else if (id === 'talk') talkStart(C);
  else if (id === 'talk-stop') talkEnd(C, 'stop');
  else if (id.startsWith('reply:')) talkAnswer(C, id.slice(6));
  else if (id === 'ask') { C.ask = true; chatShow(); }
  else if (id === 'shop-give') chatSay((typeof shopGiveSay === 'function' && shopGiveSay(p)) || 'Thanks.');   // 24j: an order handed over (M10)
  else if (id === 'case-ask') chatSay((typeof caseAskSay === 'function' && caseAskSay(p)) || 'Didn\'t notice a thing. Sorry.');   // 24k P2: their witness line
  else if (id === 'give') { const g = giftInHands(), res = g && giftGive(p, g); if (res) chatSay(res.text); }
  else if (id === 'sit') { const mo = C.line.moment; if (mo && typeof momentShow === 'function') { chatClose(); momentShow(mo); } }
  else if (id === 'back') { C.ask = false; chatShow(); }
  else if (id === 'host') { if (r.hostDay !== SHIP.time.day) chatSay(socialHost(p) || 'Another time.'); }
  else if (id.startsWith('nq:')) chatSay(guideAnswer(p, +id.slice(3)) || 'Thanks.');
  else if (id === 'guide-back') { const G = guideOn(), n = G && shortName(socP(G.id)); if (socialGuideEnd('handed')) chatSay('Of course. I\'ll look after ' + n + ' from here. Thank you for what you did.'); }
  else if (id === 'ask-intro') { C.ask = 'intro'; chatSay(pick(['Who did you have in mind?', 'Go on, who?', 'Introduce me to someone? All right.'], 665)); }
  else if (id.startsWith('intro:')) { const l = typeof introDo === 'function' ? introDo(p, id.slice(6)) : null; C.ask = true; chatSay(l || 'Maybe another time.'); }
  else if (id === 'ask-news') {
    const heard = new Set(SHIP.heard.map(x => x.id)), n = newsKnownBy(p).find(x => !heardIt(x) && !(x.about === p.id && x.kind !== 'fault') && x.about !== 'you');
    if (n) { playerHeard(n.id, p.id); chatSay(pick(n.lines, 620)); } else chatSay(pick(['Nothing new, really.', 'Quiet week. I\'ll let you know.', 'Not that I\'ve heard.'], 621));
    if (!r.known.includes('news')) r.known.push('news');
  } else if (id === 'ask-work' || id === 'ask-home') {
    // the crew designer's life details (ROSTER[i].about: [{ tier, topic, text }], third person; topic work for
    // Their work, anything else for Home) up to how well they know you; Home falls back to their `life` lines once
    // you're acquaintances, Their work to a line about their department. Each one told goes into rel.known
    const work = id === 'ask-work', tier = relTier(p.id), mine = x => x && x.text && (x.topic === 'work') === work;
    const all = (p.about || []).filter(x => mine(x) && (x.tier || 0) <= tier).map(x => x.text).concat(!work && tier >= 1 ? p.life || [] : []);
    const life = all.filter(x => !r.known.includes(x)), more = (p.about || []).some(x => mine(x) && (x.tier || 0) > tier) || (!work && tier < 1 && (p.life || []).length);
    if (life.length) { const x = life[0]; r.known.push(x); chatSay(/^([A-Z][a-z]*s|Grew|Ran|Got|Brought|Joined|Was|Left|Spent|Came|Lost|Won|Once|Used)\b/.test(x) ? shortName(p) + ' ' + x[0].toLowerCase() + x.slice(1) : 'About ' + shortName(p) + ': ' + x, false); }
    else if (work) { chatSay((CHAT_DEPT[p.dept] || 'Work\'s work.') + ' ' + (p.role ? 'I\'m ' + (/^[aeiou]/i.test(p.role) ? 'an ' : 'a ') + p.role.toLowerCase().replace(/^the /, '') + '.' : '')); if (!r.known.includes('work')) r.known.push('work'); }
    else chatSay(more ? pick(['Maybe when we know each other better.', 'Oh, there\'s not much to tell.', 'Ha. Another time.'], 622) : 'You\'ve heard all my stories by now.');
  } else if (id === 'help') {
    const f = C.fav = favourOf(p);
    if (!f) chatSay(pick(['I\'m all right for now, thanks.', 'Nothing I need, but thanks for asking.', 'Kind of you. Nothing right now.'], 623));
    else if (f.idea || f.status === 'offered') { C.offer = true; chatSay(f.idea ? f.ask : 'Still could use a hand: ' + f.title.toLowerCase() + '.'); }
    else if (f.workDone || !f.stops.length) {          // handing it back, face to face
      if (favourTurnIn(f.id)) { relAdd(p.id, 'favour', REL_PTS.favour); const fk = f.chore === 'lamp' || f.kind === 'lamp' ? 'lamp' : f.bring ? 'fetch' : 'job'; memAdd(p.id, 'fav.' + fk); repAdd(p.dept, 2, { kindness: 3 }, 'kind');   // section 17 keeps the favour's own kind in chore
        if (typeof simNote === 'function') simNote('favour', { who: 'you', from: p.id, for: p.id, fav: fk, id: f.id });   // a favour you did for them
        C.fav = null; chatSay(pick(['You\'re a star. Thank you!', 'Oh, brilliant. I owe you one.', 'Perfect. Thanks, ' + chatName() + '.', 'You didn\'t have to, but thank you.'], 629)); }
      else chatSay('Hmm, not quite done yet, is it?');
    } else chatSay(pick(['No rush. Whenever you can.', 'Thanks for doing that, by the way.', 'Any luck yet?'], 630));
  } else if (id === 'fav-yes' || id === 'fav-no') {
    const f = C.fav; C.offer = false;
    if (f && f.idea) { const fid = favourPost(f.post); C.fav = fid ? favourById(fid) : null; r.favDay = SHIP.time.day; }
    if (!C.fav) { chatSay('Never mind, it\'s sorted.'); return; }
    const R = repInit(); if (id === 'fav-yes') R.streak = 0; else if (++R.streak >= 3) { R.streak = 0; repAdd(null, 0, { kindness: -2 }); }   // only a run of noes counts
    if (id === 'fav-yes' && favourAccept(C.fav.id)) chatSay(pick(['Thank you! Find me when it\'s done.', 'You\'re a lifesaver. I\'ll be around.', 'Brilliant, thanks.'], 631) + ' (It\'s in your Jobs.)');
    else { if (typeof favourDecline === 'function') favourDecline(C.fav.id); C.fav = null; chatSay(pick(['No worries, I\'ll manage.', 'That\'s fine. Another time.', 'Sure, no problem.'], 632)); }
  } else if (id === 'meet') {
    if (typeof deviceDo === 'function') { chatClose(); deviceDo({ app: 'appointments', with: p.id }); }
    else chatSay('Appointments come with the new device. Soon.', false);
  }
}
// ---- staying while you talk, Say hello and Talk a while (0.36.82, plans/plan-0607.html "Talking") ----
// While the card is open they stay (section 10's a.talking, topped up each frame), up to CHAT_STAY ship minutes (about
// a minute) if you leave it sitting there, and for the whole of a Talk a while. They only go for what they can't miss
// (socMustGo: their shift within TALK_GO minutes, bedtime, a tradition they host) and say so (talk.go.*), then the card
// closes CHAT_GO minutes later. Talk a while (once a day each): TALK_MINS ship minutes (about 25 real seconds) with a
// meter in the card; you stand together, or sit beside them if they're sitting (section 15's playerSitNear). Social
// fills by TALK_SOCIAL over the talk (needEffects' socialGain; friendGain, when section 15 has it, on the friendship),
// friendship +REL_PTS.talk every TALK_EVERY minutes, and at TALK_ASK minutes the clock stops for a choice of three
// replies (listen, share, cheer): the one that suits them (their voice card's needs; practical counts as listen)
// gives REL_PTS.reply[1], the others [0]. Their lines come up every TALK_LINE minutes from one topic (the head writer's
// talk.<topic>.* kinds, content/keys-0607.md), else their usual chat lines. Walk off or Stop: you keep what you got.
// Saved: rel.talkDay. Nothing here calls R(); the topic is schedU k 668.
const CHAT_STAY = 36, CHAT_GO = 3, TALK_GO = 10;
const TALK_MINS = 15, TALK_SOCIAL = 30, TALK_EVERY = 5, TALK_ASK = 7, TALK_LINE = 2;
const TALK_TOPICS = ['hobby', 'home', 'day', 'work', 'food', 'news', 'tradition', 'crew', 'ship', 'plans'];
const TALK_REPLIES = ['listen', 'share', 'cheer'];
const TALK_KEEP = new Set(['story', 'news', 'missed', 'guide', 'newcomer', 'invite', 'hint', 'goodbye', 'birthday', 'visit', 'host', 'feud']);   // lines that matter more than hello or "got to go"
const talkText = (kind, dflt, k = 0) => { const L = typeof LINES !== 'undefined' && LINES[kind], e = Array.isArray(L) && L.length ? L[k % L.length] : null; return e && typeof e.text === 'string' && e.text ? e.text : dflt; };
const talkCtx = (p, x) => ({ t: shipNow(), tier: relTier(p.id), warmth: warmth(p.id), ...x });
function talkSays(C, kind, x) {                          // a line of theirs not yet said in this talk, noted as said
  const T = C.talk, l = socLine(C.p, kind, talkCtx(C.p, { keep: e => !T || !T.said.includes(e.id), ...x }));
  if (l && T) T.said.push(l.id); return l ? l.text : null;
}
function socMustGo(p, t = shipNow()) {                   // -> { why: 'shift' | 'bed' | 'trad', trad } when they must go within TALK_GO minutes, else null
  if (typeof planDay !== 'function') return null;
  const d = Math.floor(t / 1440) + 1, m = t - (d - 1) * 1440, w = typeof whereIs === 'function' ? whereIs(p, t) : null;
  if (!w || w.escort || w.visit) return null;            // with you (section 21's escort) or on a visit: not going anywhere
  const segs = planDay(p, d).concat(m > 1440 - TALK_GO ? planDay(p, d + 1) : []);   // plan times are ship minutes (eventPlan's are from midnight)
  for (const s of segs) {
    if (s.from <= t || s.from > t + TALK_GO) continue;
    if (s.act === 'work' && w.act !== 'work' && !['tea', 'toilet', 'hands'].includes(s.tag)) return { why: 'shift' };
    if (s.act === 'sleep' && w.act !== 'sleep') return { why: 'bed' };
  }
  if (typeof eventPlan === 'function') for (const e of eventPlan(p, d) || []) if (e.host && e.from - 5 > m && e.from - 5 <= m + TALK_GO) {
    const ev = typeof eventsOn === 'function' && eventsOn(d).find(x => x.id === e.id); return { why: 'trad', trad: ev && ev.name || 'the tradition' };
  }
  return null;
}
const TALK_GO_SAY = { shift: ['Shift in five. Catch me later?', 'I\'m on shift in a minute. Later?'], bed: ['I\'m off to bed. Tomorrow?', 'Bedtime for me. Night!'],
  trad: ['I\'m running {trad} in a minute. Come along?', 'Got to set up {trad}. See you there?'] };
function talkGoCheck(C, show = true) {                    // once a ship minute: do they have to go? They say so, and leave CHAT_GO minutes later
  const t = shipNow(); C.checked = Math.floor(t); if (C.going || C.visit) return false;
  const g = socMustGo(C.p, t); if (!g) return false;
  if (C.talk && !C.talk.end) talkEnd(C, 'go', true);
  const l = socLine(C.p, 'talk.go.' + g.why, talkCtx(C.p, { trad: g.trad })), a = TALK_GO_SAY[g.why];
  C.going = t + CHAT_GO; C.ask = false; C.offer = false;
  C.line = { text: l ? l.text : a[Math.floor(schedU(C.p.seed, Math.floor(t / 60), 669) * a.length)].replace('{trad}', g.trad), kind: 'go', say: true };
  if (show) chatShow(); return true;
}
function talkStart(C) {
  const p = C.p, r = relGet(p.id), today = SHIP.time.day;
  if (r.talkDay === today || C.going) return;
  r.talkDay = today; if (r.chatDay !== today) r.chatDay = today;   // a talk is a hello and more
  const a = typeof DECK_CREW !== 'undefined' && DECK_CREW.find(x => x.p === p), sits = !!(a && a.settled && a.spot && a.spot.pose === 'sit');
  const U = k => schedU(p.seed, today, k), start = Math.floor(U(668) * TALK_TOPICS.length);
  let topic = null; for (let i = 0; i < TALK_TOPICS.length && !topic; i++) { const k = TALK_TOPICS[(start + i) % TALK_TOPICS.length]; if (socLine(p, 'talk.' + k + '.open', talkCtx(p, { peek: true }))) topic = k; }
  C.talk = { mins: 0, last: shipNow(), lineAt: 0, pts: 0, gained: 0, topic, said: [], ask: false, asked: false, reply: null, end: null, sits: false };
  C.ask = false; C.offer = false;
  const seated = typeof ACT !== 'undefined' && ACT && ACT.phase === 'do' && (ACT.kind === 'eat' || ACT.kind === 'sit');   // already at a table: you talk from your seat, still eating (playtest 1)
  if (seated) { C.talk.sits = true; C.reach = Math.max(C.reach, 5); }
  else if (sits && typeof playerSitNear === 'function' && playerSitNear(deckDef.num, cellAt(a.x, a.z), 'Talking with ' + shortName(p))) { C.talk.sits = true; C.reach = Math.max(C.reach, 5); }   // a seat beside them
  const open = topic && talkSays(C, 'talk.' + topic + '.open'), hi = talkSays(C, sits ? 'talk.sit' : 'talk.start');
  if (typeof playerChat === 'function') playerChat(p);   // the hello's little social (section 15)
  memAdd(p.id, 'talk' + (topic ? '.' + topic : ''));
  chatSay([hi, open].filter(Boolean).join(' ') || talkNext(C) || 'Go on then. What\'s new?');
}
function talkNext(C) {                                    // their next line while you talk: the topic's, a filler, else their usual chat
  const T = C.talk, p = C.p;
  const l = (T.topic && talkSays(C, 'talk.' + T.topic + '.more')) || talkSays(C, 'talk.filler');
  if (l) return l;
  for (let k = 1; k <= 8; k++) { const c = chatLine(p, shipNow() + 60 * k, true); if (c && c.say !== false && !TALK_KEEP.has(c.kind) && c.kind !== 'greet' && c.kind !== 'go' && !T.said.includes(c.text)) { T.said.push(c.text); return c.text; } }
  return null;
}
function talkSuits(p) {                                   // the reply that suits them: their voice card's needs (practical counts as listen)
  const v = typeof VOICE !== 'undefined' && VOICE[p.id], tp = v && typeof VOICE_TEMPLATES !== 'undefined' && VOICE_TEMPLATES[v.tpl || p.tpl];
  const n = (v && v.needs) || (tp && tp.needs) || TALK_REPLIES[socHash(p.id) % 3];
  return n === 'practical' ? 'listen' : TALK_REPLIES.includes(n) ? n : 'listen';
}
const TALK_REPLY_SAY = { listen: 'Tell me more.', share: 'That reminds me of home.', cheer: 'Ha! Go on.' };
function talkReply(C, k) {
  const tx = C.talk.topic && talkText('talk.' + C.talk.topic + '.reply.' + k, null, schedU(C.p.seed, SHIP.time.day, 670) * 7 | 0);
  return (tx || TALK_REPLY_SAY[k]).replace(/\{name\}/g, C.p.name).replace(/\{first\}/g, shortName(C.p));
}
function talkAnswer(C, k) {
  const T = C.talk; if (!T || !T.ask || !TALK_REPLIES.includes(k)) return;
  T.ask = false; T.reply = k; T.last = shipNow();
  const good = talkSuits(C.p) === k, pts = REL_PTS.reply[good ? 1 : 0] * talkBoost();
  relAdd(C.p.id, 'talk', pts); T.pts += pts;
  chatSay((T.topic && talkSays(C, 'talk.' + T.topic + '.ans.' + k)) || (good ? 'Exactly. You get it.' : 'Ha. Maybe.'));
}
const talkBoost = () => { const fx = typeof needEffects === 'function' ? needEffects() : null; return fx && fx.friendGain > 0 ? fx.friendGain : 1; };   // section 15's leisure: "In good spirits" talks warm faster
function talkEnd(C, why, quiet) {                         // why: 'full' | 'stop' | 'walk' | 'go'
  const T = C.talk; if (!T || T.end) return; T.end = why; T.ask = false;
  if (why === 'full') { if (typeof leisureAdd === 'function') try { leisureAdd(5, 'talk'); } catch (e) { /* section 15's */ } if (typeof simNote === 'function') simNote('talk', { id: C.p.id, mins: TALK_MINS }); }
  if (quiet) return;
  const l = talkSays(C, why === 'full' ? 'talk.end' : 'talk.stop');
  chatSay(l || (why === 'full' ? 'That was nice. Let\'s do it again.' : 'Another time, then.'));
}
function talkStep(C) {                                    // every frame while you talk
  const T = C.talk, t = shipNow(), dm = Math.max(0, Math.min(1, t - T.last)); T.last = t;
  if (T.ask || T.end || !dm) return;
  const was = T.mins; T.mins = Math.min(TALK_MINS, T.mins + dm);
  const P = SHIP.player, fx = typeof needEffects === 'function' ? needEffects() : { socialGain: 1 }, g = (T.mins - was) / TALK_MINS * TALK_SOCIAL * (fx.socialGain || 1);
  if (P && P.needs && typeof needClamp === 'function') { P.needs.social = needClamp(P.needs.social + g); T.gained += g; }
  for (let k = Math.floor(was / TALK_EVERY) + 1; k <= Math.floor(T.mins / TALK_EVERY); k++) { const pts = REL_PTS.talk * talkBoost(); relAdd(C.p.id, 'talk', pts); T.pts += pts; }
  if (T.mins >= TALK_MINS) { talkEnd(C, 'full'); return; }
  if (!T.asked && T.mins >= TALK_ASK) { T.asked = true; T.ask = true; T.askAt = t; chatSay((T.topic && talkSays(C, 'talk.' + T.topic + '.ask')) || 'What do you think?'); return; }
  if (T.mins - T.lineAt >= TALK_LINE) { T.lineAt = T.mins; const l = talkNext(C); if (l) { C.line = { text: l, say: true }; chatShow(); return; } }
  talkMeter(document.getElementById('chat'), T);
}
function talkMeter(el, T) {                               // the meter in the card, like eating's bar (section 15's actBar)
  if (!el) return;
  let m = el.querySelector('.talkm');
  if (!m) { m = document.createElement('div'); m.className = 'talkm'; m.style.cssText = 'margin:0 0 9px;font-size:11.5px;opacity:.85';
    m.innerHTML = '<span></span><i style="display:block;height:4px;margin-top:3px;border-radius:2px;background:rgba(150,200,196,.22);overflow:hidden"><b style="display:block;height:100%;background:var(--teal,#5fc9bd);transform-origin:left center"></b></i>';
    const row = el.querySelector('.row, .btns'); el.insertBefore(m, row || null); }
  m.style.display = typeof ACT !== 'undefined' && ACT && ACT.kind === 'eat' && ACT.phase === 'do' ? 'none' : '';   // eating too: section 15's one bar says both (playtest 1)
  const f = T.mins / TALK_MINS, txt = T.end ? (T.end === 'full' ? 'A good talk' : 'You talked a while') : T.ask ? 'Your turn' : 'Talking · ' + Math.max(1, Math.ceil(TALK_MINS - T.mins)) + ' min';
  if (m.children[0].textContent !== txt) m.children[0].textContent = txt;
  m.children[1].children[0].style.transform = 'scaleX(' + f.toFixed(3) + ')';
}
// the card closes when you walk off or they leave the deck (socialTick, every frame); while it's open they stay put
function chatTick() {
  const C = CHAT; if (!C) return;
  if (C.visit) { if (C.talk && !C.talk.end) talkStep(C); return; }   // a visitor in your bunk room stays till you close it (or 22:00); a talk with them still runs
  const a = typeof DECK_CREW !== 'undefined' && DECK_CREW.find(x => x.p === C.p);
  if (!a || Math.hypot(a.x - player.obj.position.x, a.z - player.obj.position.z) > C.reach) { chatClose(); return; }
  const t = shipNow();
  if (C.going) { if (t >= C.going) chatClose(); else a.talking = Math.max(a.talking || 0, .25); return; }
  const T = C.talk, on = T && !T.end && !(T.ask && t - T.askAt > CHAT_STAY);   // a reply left unanswered: after a minute they drift off
  if (on || t - C.at < CHAT_STAY) a.talking = Math.max(a.talking || 0, .25);   // they stay (section 10 stops them while talking > 0)
  if (Math.floor(t) !== C.checked && talkGoCheck(C)) return;
  if (C.talk && !C.talk.end) talkStep(C);
}

// ---------------------------------------------------------------------
// 20c. SOCIAL STORIES (social engineer B, 0.39.x; plans/social-deep-plan.md, steps B1-B8)
// Voice cards and steps (0.39.0), crew-to-crew bonds, introductions and the weekly snapshot (0.39.1), moments
// (0.39.3), goodbyes (0.39.4), couples and the story arcs (0.39.5-0.39.6), calls home (0.39.7-0.39.11). Lazy like the rest
// of section 20 (ROSTER comes later in the file); nothing here draws anything or calls R(). schedU keys 672-699.
//   voiceOf(id) -> the person's voice card: the writers' VOICE[id] (baked from content/voices), over the crew
//     designer's generated fields on the roster (tpl, loves, likes, joy, thread, needs, openness, keepsake, mentors), over
//     their template (VOICE_TEMPLATES, else VOICE_FALLBACK here), over a guess from their traits and habits.
//     Always complete: { id, tpl, words, needs, openness, loves, likes, invites, joy, thread, keepsake, avoid, mentors, lines }
//   voiceWord(id, token, t) -> one of their words for {hi} {bye} {yes} {thanks} {wow} {sigh}, or {nick} (what they
//     call you: 'cadet' as strangers, your name, then their nickname for you as friends)
//   voiceFill(id, text, t) -> the text with their voice tokens and {me} filled (picked per person and ship hour)
//   relGain(id, why, pts) -> pts after openness (section 20's relAdd asks): guarded people warm 20% slower, open
//     ones 20% faster, once their card's openness is written (roster or VOICE), not guessed; their moments the other
//     way round (OPENNESS.moment, used by the moments engine)
//   metDays(id, t), stepGate(id, tone, t, last) -> whether a light / heartfelt / resolution moment may open yet
//     (STEP_GATES: tier, days known, days since their last moment)
//   knowSections(id) -> [{ title, items }] what you know about them, by section (Work, Home, Hobby, Past, Their
//     story), no counts; knowBlocks(id) -> the Crew app's blocks for it
// ---------------------------------------------------------------------
const VOICE_TOKENS = ['hi', 'bye', 'yes', 'thanks', 'wow', 'sigh'];
// the ten templates' words, until the writers' VOICE_TEMPLATES are baked in. nick by tier (stranger .. close
// friend); null means the usual for that tier: 'cadet', then your name
const VOICE_FALLBACK = {
  warm:    { needs: 'share', words: { hi: ['Hello, love', 'Hiya'], bye: ['Take care', 'Look after yourself'], yes: ['Of course', 'Happily'], thanks: ['Thank you, really', 'Bless you'], wow: ['Oh, lovely'], sigh: ['Oh dear'], nick: [null, null, null, 'love', 'love'] } },
  dry:     { needs: 'cheer', words: { hi: ['Oh, it\'s you', 'Hey'], bye: ['Off you go', 'Don\'t break anything'], yes: ['Fine', 'Go on then'], thanks: ['Ta', 'You\'re all right, you'], wow: ['Well, look at that'], sigh: ['Honestly'], nick: [null, null, null, 'trouble', 'trouble'] } },
  shy:     { needs: 'listen', words: { hi: ['Oh! Hi', 'Um, hello'], bye: ['See you', 'Bye, then'], yes: ['Okay', 'If you like'], thanks: ['Thanks. Really'], wow: ['Oh, wow'], sigh: ['Oh'], nick: [null, null, null, null, null] } },
  brisk:   { needs: 'practical', words: { hi: ['Morning', 'Right then'], bye: ['Carry on', 'Right. Back to it'], yes: ['Agreed', 'Very well'], thanks: ['Noted. Thank you', 'Good work'], wow: ['Impressive'], sigh: ['Hm'], nick: [null, 'cadet', null, null, null] } },
  chatty:  { needs: 'share', words: { hi: ['Hey hey!', 'Oh, hi!'], bye: ['Catch you later!', 'Right, I\'ll let you go'], yes: ['Yes! Totally', 'Oh, go on'], thanks: ['You\'re a star', 'Thanks a million'], wow: ['No way!'], sigh: ['Ugh'], nick: [null, null, null, 'pal', 'pal'] } },
  earnest: { needs: 'listen', words: { hi: ['Hi!', 'Oh, hello'], bye: ['See you soon', 'Good luck out there'], yes: ['Definitely', 'Yes, of course'], thanks: ['Thank you so much'], wow: ['That\'s amazing'], sigh: ['Oh, no'], nick: [null, null, null, null, null] } },
  gruff:   { needs: 'practical', words: { hi: ['Hm. You', 'There you are'], bye: ['Off with you', 'Right'], yes: ['Fine', 'If I must'], thanks: ['Hm. Thanks'], wow: ['Huh'], sigh: ['Typical'], nick: [null, 'cadet', 'cadet', 'kid', 'kid'] } },
  dreamy:  { needs: 'share', words: { hi: ['Oh, hello there', 'Hi'], bye: ['Mind the stars', 'See you around'], yes: ['Mm, why not', 'I suppose so'], thanks: ['That\'s kind'], wow: ['Oh, how lovely'], sigh: ['Ah, well'], nick: [null, null, null, 'friend', 'friend'] } },
  steady:  { needs: 'practical', words: { hi: ['Hello', 'All right?'], bye: ['See you', 'Take it easy'], yes: ['Sure', 'Sounds good'], thanks: ['Thanks'], wow: ['Not bad at all'], sigh: ['Well'], nick: [null, null, null, null, null] } },
  playful: { needs: 'cheer', words: { hi: ['Oi oi', 'Look who it is'], bye: ['Don\'t be a stranger', 'Laters'], yes: ['Go on, then', 'You bet'], thanks: ['Cheers'], wow: ['Get in!'], sigh: ['Ah, nuts'], nick: [null, null, null, 'champ', 'champ'] } },
};
// a guess from the roster until the crew designer's fields arrive: the first of their traits that names a template
const VOICE_BY_TRAIT = { gruff: 'gruff', suspicious: 'gruff', blunt: 'gruff', 'dry humour': 'dry', dry: 'dry', sarcastic: 'dry', wry: 'dry', 'quietly funny': 'dry',
  chatty: 'chatty', sociable: 'chatty', 'easy laugh': 'chatty', playful: 'playful', cheerful: 'playful', optimistic: 'playful', easygoing: 'playful',
  shy: 'shy', nervous: 'shy', quiet: 'shy', private: 'shy', discreet: 'shy', 'a little lost': 'shy', homesick: 'shy',
  meticulous: 'brisk', precise: 'brisk', exacting: 'brisk', formal: 'brisk', organised: 'brisk', brisk: 'brisk', serious: 'brisk', ambitious: 'brisk', competitive: 'brisk', proud: 'brisk', 'sharp-eyed': 'brisk',
  kind: 'warm', warm: 'warm', generous: 'warm', gentle: 'warm', patient: 'warm', dreamy: 'dreamy', 'absent-minded': 'dreamy', thoughtful: 'dreamy', unhurried: 'dreamy', forgetful: 'dreamy', curious: 'dreamy',
  earnest: 'earnest', loyal: 'earnest', reliable: 'earnest', dependable: 'earnest' };
const VOICE_GUARDED = ['shy', 'quiet', 'private', 'discreet', 'suspicious', 'nervous', 'serious', 'watchful', 'gruff'];
const VOICE_OPEN = ['chatty', 'sociable', 'cheerful', 'easy laugh', 'warm', 'playful', 'optimistic', 'generous'];
const VOICE_MENTOR = ['patient', 'kind', 'steady'];
// habits -> gift tags they'd love, and the light thing they'd share early (joy)
const VOICE_HABIT = { stargazer: ['star', 'the observatory at night'], music: ['music', 'music evenings'], musician: ['music', 'playing in the music room'],
  'garden-lover': ['plant', 'the garden'], gardener: ['garden', 'tending the garden'], 'tea-break': ['tea', 'a proper tea break'], 'common-room': ['game', 'games in the common room'],
  'quiet-corner': ['book', 'a quiet corner and a book'], 'lounge-regular': ['sweet', 'evenings in the lounge'], 'bar-regular': ['sweet', 'a drink at the bar'],
  'calls-home': ['card', 'calls home'], shopper: ['made', 'browsing the crew store'], runner: ['sweet', 'a morning run'], 'gym-regular': ['sweet', 'the gym'], 'window-seat': ['star', 'a seat by the window'] };
// struggle themes for generated crew (social-deep-plan Part 1), guessed from traits and habits until the generator
// writes `thread`; story crew with an arc keep their own id
// Frozen spellings (with the crew designer's generator, 0.16.12): the twelve themes below, and 'arc:<arcId>' for story
// crew. The writers' theme files are named after them (content/themes/<theme>.arc)
const VOICE_THEME_BY = [['homesick', 'homesick'], ['calls-home', 'homesick'], ['nervous', 'exams'], ['meticulous', 'notgood'], ['exacting', 'notgood'], ['restless', 'stuck'],
  ['workaholic', 'burnout'], ['shy', 'lonely'], ['quiet', 'lonely'], ['musician', 'talent'], ['competitive', 'rivalry'], ['private', 'startover'], ['stubborn', 'rivalry']];
const VOICE_THEMES = ['homesick', 'exams', 'family', 'stuck', 'notgood', 'lonely', 'loss', 'talent', 'burnout', 'leaving', 'rivalry', 'startover'];
const OPENNESS = { guarded: { pts: .8, moment: 1.5 }, normal: { pts: 1, moment: 1 }, open: { pts: 1.2, moment: .75 } };
const VOICE_CARD = new Map();
let VOICE_SRC = null;                                     // the writers' data the cached cards were made from
const voiceData = () => { try { return [typeof VOICE !== 'undefined' && VOICE || null, typeof VOICE_TEMPLATES !== 'undefined' && VOICE_TEMPLATES || null]; } catch (e) { return [null, null]; } };   // not yet declared: none
function voiceOf(id) {
  id = id && id.id || id;
  const D = voiceData(); if (!VOICE_SRC || VOICE_SRC[0] !== D[0] || VOICE_SRC[1] !== D[1]) { VOICE_SRC = D; VOICE_CARD.clear(); }   // new data baked in: cards again
  if (VOICE_CARD.has(id)) return VOICE_CARD.get(id);
  socInit(); const p = SOC.idx.has(id) ? SOC.crew[SOC.idx.get(id)] : null;
  const W = D[0] && D[0][id] || {}, T = D[1] || {};
  const traits = p && p.traits || [], habits = p && p.habits || [], has = l => traits.some(x => l.includes(x));
  const tpl = [W.tpl, p && p.tpl].find(x => x && (T[x] || VOICE_FALLBACK[x])) || (traits.map(x => VOICE_BY_TRAIT[x]).find(Boolean)) || 'steady';
  const base = T[tpl] || VOICE_FALLBACK[tpl], fb = VOICE_FALLBACK[tpl] || VOICE_FALLBACK.steady;
  const words = {}; for (const k of VOICE_TOKENS.concat('nick')) words[k] = (W.words && W.words[k]) || (base.words && base.words[k]) || fb.words[k];
  const tags = habits.map(h => VOICE_HABIT[h]).filter(Boolean);
  const pickV = (k, guess) => W[k] !== undefined ? W[k] : p && p[k] !== undefined ? p[k] : guess;
  const arc = (typeof STORY_ARCS !== 'undefined' && STORY_ARCS[id]) || (p && p.story) ? 'arc:' + id : null,   // story crew: their own arc (written or to come)
    theme = (VOICE_THEME_BY.find(([x]) => traits.includes(x) || habits.includes(x)) || [])[1];
  const card = { id, tpl, words,
    needs: pickV('needs', base.needs || fb.needs),
    openness: pickV('openness', has(VOICE_GUARDED) ? 'guarded' : has(VOICE_OPEN) ? 'open' : 'normal'),
    loves: pickV('loves', [...new Set(tags.map(x => x[0]))].slice(0, 2)), likes: pickV('likes', ['tea', 'sweet']),
    invites: pickV('invites', []), joy: pickV('joy', tags.length ? tags[0][1] : null),
    thread: /^arc:/.test(W.thread || '') ? W.thread : p && p.thread ? p.thread : arc || theme || (p ? VOICE_THEMES[Math.floor(schedU(p.seed, 0, 672) * VOICE_THEMES.length)] : null),   // the writers' VOICE decides story arcs only; the roster decides themes (the lead, 0.39.17)
    keepsake: pickV('keepsake', null), avoid: pickV('avoid', []), mentors: pickV('mentors', has(VOICE_MENTOR)), lines: W.lines || {},
    opennessSet: W.openness !== undefined || !!(p && p.openness !== undefined) };   // written, not guessed: only then does it change points
  if (!OPENNESS[card.openness]) card.openness = 'normal';
  if (p) VOICE_CARD.set(id, card);                       // the data is fixed for a game, so once is enough
  return card;
}
function voiceWord(id, token, t = shipNow()) {
  const v = voiceOf(id), p = SOC.idx.has(v.id) ? SOC.crew[SOC.idx.get(v.id)] : null, U = k => schedU(p ? p.seed : 0, Math.floor(t / 60), k);
  if (token === 'nick') {
    const tier = relTier(v.id), n = Array.isArray(v.words.nick) ? v.words.nick[tier] : null;
    return n ? n.replace('{me}', chatName()) : tier ? chatName() : 'cadet';
  }
  const a = v.words[token]; if (!Array.isArray(a) || !a.length) return null;
  return a[Math.floor(U(673 + VOICE_TOKENS.indexOf(token)) * a.length)];
}
function voiceFill(id, text, t = shipNow()) {          // section 22's linesFill when it's there (one filler for every line), else the tokens here
  if (typeof linesFill === 'function') { try { const p = socP(id && id.id || id), r = p && linesFill(String(text), p, { t }); if (typeof r === 'string') return r; } catch (e) { /* fall back */ } }
  return String(text).replace(/\{(hi|bye|yes|thanks|wow|sigh|nick)\}/g, (m, k) => voiceWord(id, k, t) || '').replace(/\{me\}/g, chatName()).replace(/([!?])\./g, '$1');   // 'Hey hey!' + '.' -> 'Hey hey!'
}
function relGain(id, why, pts) {                         // openness, for section 20's relAdd; onboarding's numbers and moments stay as given
  const v = voiceOf(id); if (!(pts > 0) || !v.opennessSet || /^(intro:|moment)/.test(String(why))) return pts;   // a guessed openness changes nothing
  return pts * OPENNESS[v.openness].pts;
}
// steps: what each tier lets happen also needs time known (social-deep-plan Part 1, starting numbers to tune). gap:
// days since their last moment (for resolution, the last heartfelt one), passed in by the moments engine
const STEP_GATES = { light: { tier: 2, met: 3, gap: 0 }, heartfelt: { tier: 3, met: 7, gap: 2 }, serious: { tier: 3, met: 7, gap: 2 }, resolution: { tier: 4, met: 0, gap: 3 } };
function metDays(id, t = shipNow()) { socInit(); const r = SHIP.rel[id && id.id || id]; return r && r.met !== null ? Math.floor((t - r.met) / 1440) : -1; }
function stepGate(id, tone, t = shipNow(), last = null) {
  const g = STEP_GATES[tone]; if (!g) return false;
  return relTier(id && id.id || id) >= g.tier && metDays(id, t) >= g.met && (last === null || (t - last) / 1440 >= g.gap);
}
// what you know about someone, in sections (the Crew app's page; no counts). rel.known holds what they've told you:
// the roster's `about` texts (their topic gives the section), their `life` lines (Home, as Ask about tells them),
// and '@<section>:<text>' entries the moments and gifts add later
const KNOW_SECTIONS = [['work', 'Work'], ['home', 'Home'], ['hobby', 'Hobby'], ['past', 'Past'], ['secret', 'Their story'], ['story', 'Their story'], ['loves', 'Loves']];
function knowSections(id) {
  socInit(); id = id && id.id || id; const r = SHIP.rel[id], p = SOC.idx.has(id) ? SOC.crew[SOC.idx.get(id)] : null;
  if (!r || !p) return [];
  const by = {};
  for (const k of r.known) {
    if (k === 'news' || k === 'work') continue;
    const m = /^@(\w+):(.+)$/.exec(k), a = !m && (p.about || []).find(x => x.text === k);
    const sec0 = m ? m[1] : a ? a.topic || 'home' : 'home', sec = KNOW_SECTIONS.some(([x]) => x === sec0) ? sec0 : 'home', text = m ? m[2] : k;   // a topic we've no section for: Home
    (by[sec] || (by[sec] = [])).push(text);
  }
  const out = [];
  for (const [k, title] of KNOW_SECTIONS) if (by[k]) { const s = out.find(x => x.title === title); if (s) s.items.push(...by[k]); else out.push({ title, items: by[k].slice() }); }
  return out;
}
function knowBlocks(id) {                                // for the Crew app (section 20's view)
  const s = knowSections(id);
  if (!s.length) return [{ kind: 'list', rows: [{ text: 'Nothing yet. Ask them about themselves.' }] }];
  return s.flatMap(x => [{ kind: 'text', text: x.title, mark: 'head' }, { kind: 'list', rows: x.items.map(t => ({ text: t })) }]);
}
// ---- crew with each other: labelled bonds (0.39.1) ----
// SHIP.social.bonds['a:b'] = { kind, since, peak, seen } for the pairs that matter (section 20 saves it). a:b in
// ROSTER order, except a mentor's, which is 'mentor:mentee'. Kinds: friends (affinity BOND_AT.friends+), best (each
// person's mutual closest friend, BOND_AT.best+; at most one each), rivals (BOND_AT.rivals or less, until it climbs
// past rivalsOff), drifting (friends whose affinity fell BOND_AT.drift below its peak; ends at driftOff, or friends
// again), mentor (same department, a rank or more apart, the senior's voice card mentors, BOND_AT.mentor+; at most
// BOND_MENTEES each, one mentor each, mentees juniors or officers; until mentorOff). One bond a pair (best > mentor >
// the rest). Friends who haven't spent time together for BOND_APART days drift down a point a day, which is how
// friendships fade when shifts or bunks move people apart. storyHour(h, pairs) runs it each ship hour (section 20's socialHour
// hands over who spent time together). socBondOf(id, kind) answers section 20's bondOf. Changes go on the ship notes
// bus: simNote('bond', { a, b, kind, was })
const BOND_AT = { friends: 60, best: 65, rivals: -40, rivalsOff: -25, drift: 15, driftOff: 20, mentor: 40, mentorOff: 25 };
const BOND_MENTEES = 2, BOND_APART = 4, BOND_MENTEE_RANKS = ['junior', 'officer'], COUPLE_AFF = 90;
// hard bounds by design (0.39.21, the lead's long-play rule): no new bond for someone with BOND_MAX already (9 is the most
// anyone had in 280 days; a frozen bond that wakes when its pair are both aboard again can take them one or two over) and at
// most BOND_GONE_MAX frozen with people who moved on (the oldest let go first): about n * (BOND_MAX + BOND_GONE_MAX) / 2 bonds
// in all. STORY_CAP (not saved; cleared when the clock goes back, a new game) counts refused tries an hour and when each first bound
const BOND_MAX = 10, BOND_GONE_MAX = 4, STORY_CAP = { full: 0, gone: 0, firstFull: null, firstGone: null, h: -Infinity };
const STORY_BONDS = ['friends', 'best', 'rivals', 'mentor', 'mentee', 'drifting', 'couple'];   // section 20's frozen BOND_KINDS
// how many friends (60+) someone makes room for: section 20's hourly drift stops new friendships climbing past 60
// once either of the pair has this many (the designer's numbers)
const FRIEND_CAP_OPEN = ['chatty', 'sociable', 'warm', 'cheerful'], FRIEND_CAP_SHY = ['shy', 'private', 'quiet'];
const friendCap = p => { const t = p && p.traits || []; return t.some(x => FRIEND_CAP_OPEN.includes(x)) ? 5 : t.some(x => FRIEND_CAP_SHY.includes(x)) ? 3 : 4; };
function storyHour(h, pairs) {
  const { crew, n } = SOC, t = h * 60 + 30, aff = SHIP.aff, B = SHIP.social.bonds || (SHIP.social.bonds = {}), rank = p => RANK_ORDER.indexOf(p.rank);
  const cnt = new Map(), cntAdd = (k, d) => { for (const x of k.split(':')) cnt.set(x, (cnt.get(x) || 0) + d); };
  const set = (k, kind, extra) => { const b = B[k], was = b ? b.kind : null; if (was === kind) return;
    if (!b && k.split(':').some(x => (cnt.get(x) || 0) >= BOND_MAX)) { STORY_CAP.full++; if (STORY_CAP.firstFull === null) STORY_CAP.firstFull = Math.floor(h / 24) + 1; return; }   // full: a new bond waits
    if (!b) cntAdd(k, 1); B[k] = Object.assign({ kind, since: t }, extra);
    if (typeof simNote === 'function') { const [a, c] = k.split(':'); simNote('bond', { a, b: c, kind, was }); } };
  const drop = k => { const b = B[k]; if (!b) return; delete B[k]; if (!b.gone) cntAdd(k, -1); if (typeof simNote === 'function') { const [a, c] = k.split(':'); simNote('bond', { a, b: c, kind: null, was: b.kind }); } };
  if (h < STORY_CAP.h) Object.assign(STORY_CAP, { full: 0, gone: 0, firstFull: null, firstGone: null }); STORY_CAP.h = h;   // a new game
  affWeekTake(h);
  homeMsgHour(h);
  for (const [i, j] of pairs || []) { const b = B[crew[i].id + ':' + crew[j].id]; if (b) b.seen = h; }
  // crew come and go (0.39.14): a bond with someone not aboard (transferred off, or not arrived) is frozen as it was,
  // marked gone (the day it froze) and skipped below: no fading, drifting, best friends or mentors across the hull;
  // it wakes again if they're both aboard. socBondOf(id, 'missed') is their closest friend who moved on
  const day = Math.floor(h / 24) + 1, on = crew.map(p => socAboard(p, day)), both = (i, j) => on[i] && on[j];
  for (const k in B) { const [a, c] = k.split(':'), i = SOC.idx.get(a), j = SOC.idx.get(c); if (i === undefined || j === undefined) continue;
    if (!both(i, j)) { if (!B[k].gone) B[k].gone = day; } else if (B[k].gone) delete B[k].gone; }
  const goneOf = new Map();
  for (const k in B) { if (!B[k].gone) { cntAdd(k, 1); continue; } for (const x of k.split(':')) { const i = SOC.idx.get(x); if (i !== undefined && on[i]) (goneOf.get(x) || goneOf.set(x, []).get(x)).push(k); } }
  for (const [, ks] of goneOf) if (ks.length > BOND_GONE_MAX) {   // the oldest frozen bonds of someone still aboard are let go
    ks.sort((a, b) => B[a].gone - B[b].gone || (a < b ? -1 : 1));
    for (const k of ks.slice(0, ks.length - BOND_GONE_MAX)) if (B[k]) { delete B[k]; STORY_CAP.gone++; if (STORY_CAP.firstGone === null) STORY_CAP.firstGone = day; } }
  // couples (B6): the roster's partners are a couple from the start and stay one, at COUPLE_AFF or more; no story of
  // their own, never involving you. Their bond outranks the others, so they're never best friends, rivals or mentor
  for (let i = 0; i < n; i++) { const q = crew[i].partner, j = q !== undefined ? SOC.idx.get(q) : undefined; if (j === undefined || j <= i || !both(i, j)) continue;
    const k = crew[i].id + ':' + crew[j].id; delete B[crew[j].id + ':' + crew[i].id]; if (!B[k] || B[k].kind !== 'couple') set(k, 'couple');
    if (aff[pairIdx(i, j)] < COUPLE_AFF) aff[pairIdx(i, j)] = COUPLE_AFF; }
  // friends long apart fade a little, once a day at 04:00
  if (h % 24 === 4) for (const k in B) { const b = B[k]; if ((b.kind !== 'friends' && b.kind !== 'best' && b.kind !== 'drifting') || b.gone) continue;
    const [a, c] = k.split(':'), i = SOC.idx.get(a), j = SOC.idx.get(c); if (i === undefined || j === undefined) continue;
    if (h - (b.seen ?? Math.floor(b.since / 60)) > BOND_APART * 24) aff[pairIdx(i, j)] = Math.max(-100, aff[pairIdx(i, j)] - 1); }
  // friends, rivals and drifting, pair by pair
  for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) {
    if (!both(i, j)) continue;
    const k = crew[i].id + ':' + crew[j].id, b = B[k], v = aff[pairIdx(i, j)], cur = b ? b.kind : null;
    if (cur === 'mentor' || cur === 'couple' || B[crew[j].id + ':' + crew[i].id]) continue;   // a mentor's key, the other way round
    if (b && b.spar && v < BOND_AT.friends) continue;     // a sparring partner stays one until they're friends
    if (v <= BOND_AT.rivals || (cur === 'rivals' && v <= BOND_AT.rivalsOff)) set(k, 'rivals');
    else if (cur === 'friends' || cur === 'best') { if (v > b.peak) b.peak = v; if (v <= b.peak - BOND_AT.drift) set(k, 'drifting', { seen: b.seen }); }
    else if (v >= BOND_AT.friends) set(k, 'friends', { peak: v, seen: b ? b.seen : h });
    else if (cur === 'drifting') { if (v < BOND_AT.driftOff) drop(k); }
    else if (cur) drop(k);
  }
  // best friends: each person's closest friend, when it's mutual
  const top = new Map();
  for (const k in B) { const b = B[k]; if ((b.kind !== 'friends' && b.kind !== 'best') || b.gone) continue;
    const [a, c] = k.split(':'), v = affinity(a, c);
    for (const [x, y] of [[a, c], [c, a]]) { const o = top.get(x); if (!o || v > o[1] || (v === o[1] && y < o[0])) top.set(x, [y, v]); } }
  for (const k in B) { const b = B[k]; if ((b.kind !== 'friends' && b.kind !== 'best') || b.gone) continue;
    const [a, c] = k.split(':'), best = top.get(a)[0] === c && top.get(c)[0] === a && affinity(a, c) >= BOND_AT.best;
    if (best && b.kind !== 'best') set(k, 'best', { peak: b.peak, seen: b.seen }); else if (!best && b.kind === 'best') set(k, 'friends', { peak: b.peak, seen: b.seen }); }
  // sparring partners (0.39.14, the rivalry theme; the lead and head writer 3): someone whose thread is rivalry and who
  // has no rival gets one once a day, friendly-competitive: the aboard crewmate they get on with least (their
  // department first), not a partner, mentor or friend. Kept until they're friends (the theme's happy end)
  if (h % 24 === 4) for (let i = 0; i < n; i++) {
    const p = crew[i]; if (!on[i] || (voiceOf(p.id).thread || '') !== 'rivalry' || socBondOf(p.id, 'rivals')) continue;
    let pick = null, pv = 1e9;
    for (let j = 0; j < n; j++) { if (j === i || !on[j] || crew[j].rank === 'guest') continue; const q = crew[j], sk = i < j ? p.id + ':' + q.id : q.id + ':' + p.id, sb = B[sk] || B[i < j ? q.id + ':' + p.id : p.id + ':' + q.id];
      if (sb && !sb.gone && sb.kind !== 'drifting') continue;
      const v = aff[pairIdx(i, j)] - (q.dept === p.dept ? 1000 : 0); if (v < pv || (v === pv && q.id < pick[0].id)) { pick = [q, sk]; pv = v; } }
    if (pick) set(pick[1], 'rivals', { spar: true });
  }
  // mentors: kept while they get on; new ones once a day, the warmest senior first
  for (const k in B) { if (B[k].kind !== 'mentor' || B[k].gone) continue; const [a, c] = k.split(':'); if (affinity(a, c) < BOND_AT.mentorOff) drop(k); }
  if (h % 24 === 4) {
    const has = new Set(), count = new Map();
    for (const k in B) if (B[k].kind === 'mentor' && !B[k].gone) { const [a, c] = k.split(':'); has.add(c); count.set(a, (count.get(a) || 0) + 1); }
    for (let j = 0; j < n; j++) {
      const q = crew[j]; if (!on[j] || has.has(q.id) || !BOND_MENTEE_RANKS.includes(q.rank)) continue;
      let pick = null, pv = BOND_AT.mentor - 1;
      for (let i = 0; i < n; i++) { const p = crew[i];
        if (!on[i] || p.dept !== q.dept || p.rank === 'guest' || rank(p) < 0 || rank(q) - rank(p) < 1 || (count.get(p.id) || 0) >= BOND_MENTEES || !voiceOf(p.id).mentors) continue;
        const v = aff[pairIdx(i, j)], sk = (i < j ? p.id + ':' + q.id : q.id + ':' + p.id), sb = B[sk];
        if (v > pv && !(sb && (sb.kind === 'best' || sb.kind === 'rivals' || sb.kind === 'couple'))) { pick = [p, sk]; pv = v; } }
      if (pick) { if (B[pick[1]] && !B[pick[1]].gone) cntAdd(pick[1], -1); delete B[pick[1]]; set(pick[0].id + ':' + q.id, 'mentor', { seen: h }); has.add(q.id); count.set(pick[0].id, (count.get(pick[0].id) || 0) + 1); }
    }
  }
}
function socBondOf(id, kind) {                           // for section 20's bondOf: a crewmate, null for none, undefined for "not mine"; friends includes best
  if (kind === 'missed') return socMissed(id);
  if (!STORY_BONDS.includes(kind)) return undefined;
  socInit(); id = id && id.id || id; const B = SHIP.social.bonds || {};
  let pick = null, pv = -1e9;
  for (const k in B) {
    const b = B[k], [a, c] = k.split(':'); if ((a !== id && c !== id) || b.gone) continue;   // someone who moved on isn't a bond today ('missed' is)
    const ok = kind === 'friends' ? b.kind === 'friends' || b.kind === 'best' : kind === 'mentor' ? b.kind === 'mentor' && c === id : kind === 'mentee' ? b.kind === 'mentor' && a === id : b.kind === kind;
    if (!ok) continue;
    const o = a === id ? c : a, v = affinity(id, o); if (v > pv || (v === pv && o < pick)) { pick = o; pv = v; }
  }
  if (!pick && (kind === 'mentee' || kind === 'couple')) return undefined;   // section 20's own: you as the escort's mentee, and a partner from the roster before the first hour
  return pick;
}
function socMissed(id) {                                   // their closest friend, best friend, partner or mentor who moved on (0.39.14), else null
  socInit(); id = id && id.id || id; const B = SHIP.social.bonds || {}; let pick = null, pv = -1e9;
  for (const k in B) { const b = B[k], [a, c] = k.split(':'); if ((a !== id && c !== id) || !b.gone || !['friends', 'best', 'couple', 'mentor'].includes(b.kind)) continue;
    const o = a === id ? c : a; if (socAboard(socP(o))) continue;   // the one who's still here misses the one who left
    const v = affinity(id, o); if (v > pv || (v === pv && o < pick)) { pick = o; pv = v; } }
  return pick;
}
// the weekly snapshot for planning (0.39.1, sparse since 0.39.3): section 14 seats people by affinityPlan(a, b, d),
// which must give the same answer however often a day is planned. At the start of each ship week (the first
// storyHour in it) the pairs whose live affinity is AFF_SNAP or more either way (seating's lines: next to friends at
// 30+, away from people at -30 or less) are copied into SHIP.social.affWeek, '<week>:<crew count>:<base64 of [i, j,
// v] bytes>', this week's and last week's joined by ';' (section 20 saves it), so its size follows the friendships,
// not the square of the crew. A day in week W reads the snapshot taken at the start of week W-1: fixed and saved a
// week before any day that might be planned ahead. A pair not in it reads 0 (between the lines). No snapshot for
// that week (a new game's first two, a save from before, a crew list of another size) gives undefined, so
// affinityPlan keeps its pure starting affinity. affPlanWeek(i, j, d) -> affinity or undefined (i, j: ROSTER indexes)
const AFF_SNAP = 30, AFF_SNAP_MAX = 600;                 // pairs at |affinity| 30+ (the rule); the strongest 600 only as a safety net for the save (0.39.20, the lead: about 4.8 KB for both weeks; with 86 crew it never binds before day 140)
const AFF_WEEK = { src: null, map: new Map() };           // decoded snapshots: week -> Map(pairIdx -> v)
const affCrewTag = () => (socHash(SOC.crew.map(p => p.id).join(',')) >>> 0).toString(36);   // which crew list (and order) a snapshot's pairs index (0.39.22)
function affWeeks() {
  const s = SHIP.social.affWeek || null;
  if (AFF_WEEK.src !== s) { AFF_WEEK.src = s; AFF_WEEK.map = new Map();
    for (const part of (s || '').split(';')) { const m = /^(-?\d+):(\d+):(?:([0-9a-z]+)\/(?=~))?(.*)$/.exec(part); if (!m || +m[2] !== SOC.n || (m[3] && m[3] !== affCrewTag())) continue;   // another crew list (same size, other order): not this crew's
      try { const P = new Map();
        if (m[4][0] === '~') {                                // 0.39.21: a bit per pair (in i < j order), then the values of those set
          const bin = atob(m[4].slice(1)), n = SOC.n, nb = Math.ceil(n * (n - 1) / 2 / 8); let q = 0, v = nb;
          for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++, q++) if (bin.charCodeAt(q >> 3) >> (q & 7) & 1) P.set(pairIdx(i, j), bin.charCodeAt(v++) << 24 >> 24);
        } else { const bin = atob(m[4]); for (let k = 0; k + 2 < bin.length; k += 3) P.set(pairIdx(bin.charCodeAt(k), bin.charCodeAt(k + 1)), bin.charCodeAt(k + 2) << 24 >> 24); }   // the older form: [i, j, v] triples
        AFF_WEEK.map.set(+m[1], { P, raw: part }); }
      catch (e) { /* a bad snapshot is ignored */ } } }
  return AFF_WEEK.map;
}
function affWeekTake(h) {                                // storyHour: the first hour of a new ship week
  const w = Math.floor(Math.floor(h / 24) / 7), M = affWeeks(); if (M.has(w) || [...M.keys()].some(k => k > w)) return;
  const { n } = SOC, aff = SHIP.aff; let bin = '';
  let L = [];
  for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) { const v = aff[pairIdx(i, j)]; if (v >= AFF_SNAP || v <= -AFF_SNAP) L.push([i, j, v]); }
  if (L.length > AFF_SNAP_MAX) L = L.sort((a, b) => Math.abs(b[2]) - Math.abs(a[2]) || a[0] - b[0] || a[1] - b[1]).slice(0, AFF_SNAP_MAX).sort((a, b) => a[0] - b[0] || a[1] - b[1]);   // the strongest, back in pair order
  const bits = new Uint8Array(Math.ceil(n * (n - 1) / 2 / 8)), on = new Set(L.map(([i, j]) => i * n + j)); let q = 0, vals = '';   // a bit per pair, then the values in pair order (0.39.21: about 40% smaller)
  for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++, q++) if (on.has(i * n + j)) bits[q >> 3] |= 1 << (q & 7);
  for (const [, , v] of L) vals += String.fromCharCode(v & 255);
  for (const b of bits) bin += String.fromCharCode(b);
  const keep = [...M.keys()].filter(k => k === w - 1).map(k => M.get(k).raw);
  SHIP.social.affWeek = keep.concat(w + ':' + n + ':' + affCrewTag() + '/~' + btoa(bin + vals)).join(';');
}
function affPlanWeek(i, j, d) {
  if (!Number.isFinite(d)) return undefined;              // no day: the starting affinity, as before
  socInit(); const a = affWeeks().get(Math.floor((d - 1) / 7) - 1);
  return a ? a.P.get(pairIdx(i, j)) ?? 0 : undefined;
}
// you as the connector (0.39.1): "Do you know …?" on the chat card's Ask about. introOptions(p) -> up to three people
// you know at colleague or better (as well as p) whom p hardly knows (affinity under INTRO_UNDER, not rivals),
// your closest first. introDo(p, otherId) -> what p says: if they'd get on, their affinity rises by INTRO_PTS (to at
// least INTRO_UNDER, so they aren't offered again), both remember it (memAdd 'introduced.<other>'), and it's news;
// if their traits clash, a polite "we've met" and nothing changes
const INTRO_UNDER = 20, INTRO_PTS = 15;
function introOptions(p) {
  socInit(); if (!p || !SOC.idx.has(p.id) || relTier(p.id) < 2) return [];
  return SOC.crew.filter(q => q !== p && relTier(q.id) >= 2 && affinity(p, q) < INTRO_UNDER && socBondOf(p.id, 'rivals') !== q.id)
    .sort((a, b) => SHIP.rel[b.id].pts - SHIP.rel[a.id].pts || (a.id < b.id ? -1 : 1)).slice(0, 3).map(q => ({ id: q.id, name: shortName(q) }));
}
function introDo(p, otherId) {
  if (!introOptions(p).some(x => x.id === otherId)) return null;
  const q = SOC.crew[SOC.idx.get(otherId)], i = SOC.idx.get(p.id), j = SOC.idx.get(otherId), n = shortName(q), t = Math.floor(shipNow());
  if (socClash(p, q)) return 'We\'ve met. We\'re… different. But thanks.';
  SHIP.aff[pairIdx(i, j)] = Math.min(100, Math.max(INTRO_UNDER, SHIP.aff[pairIdx(i, j)] + INTRO_PTS));
  if (typeof memAdd === 'function') { memAdd(p.id, 'introduced.' + q.id); memAdd(q.id, 'introduced.' + p.id); }
  newsAdd({ id: 'intro:' + p.id + ':' + q.id + ':' + t, about: p.id + ',' + q.id, kind: 'introduced', weight: .4, life: 3, born: t, seed: [p.id, q.id],
    lines: [shortName(p) + ' and ' + n + ' got talking. Turns out they get on.', 'Have you seen ' + shortName(p) + ' and ' + n + '? New friends, by the look of it.', shortName(p) + ' and ' + n + ' were chatting for ages at dinner.'] });
  if (typeof simNote === 'function') simNote('introduced', { a: p.id, b: q.id, you: true });
  return voiceFill(p.id, ['{wow}. I\'ll say hello to ' + n + ' next time.', n + '? I\'ve seen them about. I\'ll go and say hi.', 'Oh, ' + n + '! {thanks}, I will.'][Math.floor(schedU(p.seed, Math.floor(t / 60), 681) * 3)]);
}
// ---- moments (0.39.3, B3; plans/social-deep-plan.md Part 1 "Moments" and Part 6 "Moment scripts") ----
// A moment is a short scene in section 18's dialogue panel: a few lines, one choice of replies (flavours listen,
// cheer, practical, share), then a closing line. Each person's thread (voiceOf(id).thread) has beats: a story arc
// ('arc:<id>') uses section 20's STORY_ARCS beats, the first a card line and beats 2 on moments; a theme (homesick,
// ...) has three, light at colleague, heartfelt at friend, resolution at close friend. Scripts come from the writers'
// baked MOMENTS['<crewId>:<beat>'] or MOMENT_THEMES[theme][beat - 1], else MOMENTS_BUILTIN here (Tomas, Pell and Rina,
// from their Pillar 3 arcs), never declared here. momentReady(p, t, ctx) -> id when the next beat may open: the tier
// and time gates (STEP_GATES, or the script's tier / metDays / gapDays), they're off duty somewhere calm (a seat in
// SIT_TYPES, or visiting you), not the same day as their last moment, at most one serious moment a ship day for you
// (tone heartfelt, serious or resolution), and no ship crisis's onset (unless the script says crisis: true). Section 20
// shows its hint and the "Sit with them" button. momentShow(id) plays it; the reply picked counts once it's picked:
// relAdd(id, 'moment', points by tone, +MOMENT_FIT when the flavour is the one they need, times OPENNESS.moment once
// openness is written), memAdd 'moment.<thread>.<beat>.<flavour>' (core for a resolution), simNote('moment'), what
// you learnt ('@story:' in rel.known), a resolution's keepsake (giftKeepsake), the script's after (a Mail) and, for a
// story arc, section 20's arcTold (its Mail, Pell's show). State: SHIP.social.stories (section 20 saves it):
// { serious: day of the last serious moment, m: { crewId: { b: theme beats told, at, hf: minute of the last moment and
// of the last heartfelt one } } }
const MOMENT_PTS = { light: 3, heartfelt: 5, serious: 5, resolution: 6 }, MOMENT_FIT = 4;
const MOMENT_TONE = ['light', 'heartfelt', 'resolution'];   // a theme's beats 1-3
// the story crew's Pillar 3 arcs as moments (beats 2-4; beat 1 stays section 20's card line). `say: n` opens with
// STORY_ARCS[who][n].say. Placeholder words for the head writer to replace through content/arcs
const MOMENTS_BUILTIN = {
  'tomas:2': { tone: 'light', hint: 'Got a minute? I need to rehearse something.', lines: [{ say: 1 },
    { who: 'tomas', text: 'I keep writing down what to say. Like he won\'t recognise me otherwise.' },
    { choice: [{ text: 'What\'s he like, your brother?', flavour: 'listen', reply: 'Loud. Funny. Eats cereal for dinner. I miss the noise, honestly.' },
               { text: 'Open with a terrible joke. Works on me.', flavour: 'cheer', reply: 'Ha! Okay. I\'ve got one about a scrubber. He\'ll hate it.' },
               { text: 'I rehearse calls home too. Every time.', flavour: 'share', reply: 'Really? That helps, actually. It\'s not just me.' }] },
    { who: 'tomas', text: 'Thanks, {me}. Thursday, then. Wish me luck.' }], learn: 'His brother\'s birthday is on a Thursday, and he called him from the booths.' },
  'tomas:3': { tone: 'heartfelt', hint: 'Got a minute? Properly, I mean.', lines: [{ say: 2 },
    { who: 'tomas', text: 'I sat in the booth for an hour after. Just in case he called back.', pose: 'sigh' },
    { choice: [{ text: 'I\'m here. How was it, before it dropped?', flavour: 'listen', reply: 'Good. Really good. He laughed at the scrubber joke. Then nothing.' },
               { text: 'Let\'s ask Comms when the relay\'s clearest. Try again.', flavour: 'practical', reply: 'You\'d do that? ...Yeah. Yeah, let\'s.' },
               { text: 'He\'ll come round. Brothers always do.', flavour: 'cheer', reply: 'You think? I hope so. He\'s stubborn. Like me.' }] },
    { who: 'tomas', text: 'Sorry. I didn\'t mean to unload all that. Thanks for sitting with me.' }], learn: 'A call home to his brother dropped halfway, and it hurt.' },
  'tomas:4': { tone: 'resolution', hint: 'You have to hear this.', keepsake: 'his spare star map', lines: [{ say: 3 },
    { who: 'tomas', text: 'I wanted you to be the first to know. You were there when it went wrong.' },
    { choice: [{ text: 'Show me where home is on the map.', flavour: 'share', reply: 'Here. That faint one. Not much to look at, but it\'s ours.' },
               { text: 'Same sky. That\'s brilliant.', flavour: 'cheer', reply: 'Isn\'t it? He\'s named a star after me. The dim one, obviously.' },
               { text: 'Tell me everything he said.', flavour: 'listen', reply: 'He said he\'s proud of me. He\'s never said that before.' }] },
    { who: 'tomas', text: 'Here. My spare star map. I want you to have it.' }], learn: 'He and his brother look at the same star map now.' },
  'pell:2': { tone: 'light', hint: 'Come and look at this. Carefully.', lines: [{ say: 1 },
    { who: 'pell', text: 'The chime\'s the tricky bit. One wrong tooth and it plays a funeral march.' },
    { choice: [{ text: 'A funeral march could be a hit.', flavour: 'cheer', reply: 'Ha! The Pell Okafor Sad Hour. Front row seats.' },
               { text: 'Want a hand with the tiny screws?', flavour: 'practical', reply: 'Your hands are steadier than mine. Go on, hold this.' },
               { text: 'Where did you learn to fix these?', flavour: 'listen', reply: 'My grandad\'s shed. He fixed clocks. I mostly broke them.' }] },
    { who: 'pell', text: 'Right. Back to it, before the chime notices I\'ve stopped.' }], learn: 'He mends old music boxes, the way his grandad mended clocks.' },
  'pell:3': { tone: 'heartfelt', hint: 'Can I ask you something? Don\'t laugh.', lines: [{ say: 2 },
    { who: 'pell', text: 'Honestly? I\'m terrified nobody turns up.', pose: 'sigh' },
    { choice: [{ text: 'What are you really worried about?', flavour: 'listen', reply: 'That they\'ll think it\'s daft. That I\'m daft. Grown man, tin boxes.' },
               { text: 'I\'ll bring the whole Watch shift.', flavour: 'cheer', reply: 'Ha! Don\'t threaten me with a good time.' },
               { text: 'I\'ll be there. Front row.', flavour: 'share', reply: 'Promise? Okay. Okay, I can do this.' }] },
    { who: 'pell', text: '{thanks}, {nick}. I mean it.' }], learn: 'He was nervous about showing his music boxes to the ship.' },
  'pell:4': { tone: 'resolution', hint: 'Got a sec? I owe you one.', keepsake: 'his smallest music box', lines: [{ say: 3 },
    { who: 'pell', text: 'I couldn\'t have done it without you nagging me.' },
    { choice: [{ text: 'Encore next month?', flavour: 'cheer', reply: 'Don\'t tempt me. I\'ve got three more boxes rusting.' },
               { text: 'Best night I\'ve had aboard.', flavour: 'share', reply: 'Yeah? ...Me too, actually.' },
               { text: 'How did it feel, up there?', flavour: 'listen', reply: 'Like everyone was listening to my grandad\'s shed. In a good way.' }] },
    { who: 'pell', text: 'Here. The smallest one. It plays the waltz. Mostly.' }], learn: 'His music boxes had their night in the music room.' },
  'rina:2': { tone: 'light', hint: 'Got a minute? Don\'t make a fuss.', lines: [{ say: 1 },
    { who: 'rina', text: 'Don\'t look at me like that. I\'m fine. Mostly.' },
    { choice: [{ text: 'Tiles. Now. You need beating.', flavour: 'cheer', reply: 'You? Beat me? Ha. Go on, then.' },
               { text: 'Tell me about her.', flavour: 'listen', reply: 'She cheats at Tiles. Tells me to drink water. Sound familiar?' },
               { text: 'Want me to cover your evening jobs?', flavour: 'practical', reply: 'That\'s... actually kind. No. But thanks.' }] },
    { who: 'rina', text: '{bye}. And thanks.' }], learn: 'Her gran went into hospital, and her sister keeps her posted.' },
  'rina:3': { tone: 'heartfelt', hint: 'Got a minute? Properly, I mean.', lines: [{ say: 2 },
    { who: 'rina', text: 'Gran used to say worrying is just praying with your hands tied.', pose: 'sigh' },
    { choice: [{ text: 'I\'m here. Tell me about her.', flavour: 'listen', reply: 'She taught me to cheat at Tiles before she taught me to play. Let me tell you...' },
               { text: 'Want to lose to me at Tiles? Distraction.', flavour: 'cheer', reply: 'You? Beat me? Ha. Go on, then.' },
               { text: 'I can ask Comms to watch for station traffic.', flavour: 'practical', reply: 'Would you? That would really help.' }] },
    { who: 'rina', text: 'Thanks, {me}. Really.' }], learn: 'Two days without news of her gran, she didn\'t sleep.' },
  'rina:4': { tone: 'resolution', hint: 'Guess what. No, guess.', keepsake: 'a Tiles piece, the cheating one', lines: [{ say: 3 },
    { who: 'rina', text: 'She asked about you. I may have mentioned you. Once or twice.' },
    { choice: [{ text: 'Tell her I want a rematch.', flavour: 'cheer', reply: 'She\'ll destroy you. I can\'t wait.' },
               { text: 'I\'m so glad. I was worried too.', flavour: 'share', reply: 'I know. I could tell. ...Thanks for that.' },
               { text: 'How is she, really?', flavour: 'listen', reply: 'Tired. Cheeky. Herself. That\'s all I wanted.' }] },
    { who: 'rina', text: 'Here. Gran\'s cheating piece. She says you\'ll need it.' }], learn: 'Her gran came home, and beat her sister at Tiles.' },
};
const momentBaked = () => { try { return [typeof MOMENTS !== 'undefined' && MOMENTS || null, typeof MOMENT_THEMES !== 'undefined' && MOMENT_THEMES || null]; } catch (e) { return [null, null]; } };   // section 22's baked blocks
function momentDef(id) {                                 // '<crewId>:<beat>' -> { who, beat, thread, tone, ... , lines } | null
  if (/:bye$/.test(String(id))) return goodbyeDef(String(id).slice(0, -4));   // a goodbye (B5)
  const m = /^(.+):(\d+)$/.exec(String(id)); if (!m) return null;
  const who = m[1], beat = +m[2], [MO, TH] = momentBaked(), thread = voiceOf(who).thread || '';
  let d = MO && MO[id] || MOMENTS_BUILTIN[id] || null;
  if (!d && !thread.startsWith('arc:') && TH && Array.isArray(TH[thread])) d = TH[thread].find(x => x && x.beat === beat) || null;
  if (!d || !Array.isArray(d.lines)) return null;
  const p = socP(who), has = f => { if (p[f] != null && p[f] !== '') return true; try { return typeof socialFill === 'function' && socialFill(p, f, {}) != null; } catch (e) { return false; } };
  if (Array.isArray(d.needs) && (!p || !d.needs.every(has))) return null;   // a theme beat needs details they have: the roster's, or what section 20's socialFill can say ({hobby} from their habits, {since} from their arrival)
  return Object.assign({ who, beat, thread, tone: thread.startsWith('arc:') ? 'heartfelt' : MOMENT_TONE[beat - 1] || 'heartfelt' }, d, { who, beat });
}
const STORY_M0 = Object.freeze({ b: 0, at: null, hf: null });
const storyPeek = id => { const S = SHIP.social && SHIP.social.stories, M = S && S.m; return (M && M[id]) || STORY_M0; };   // read-only (queries never write the save; reviewer 1b, 0.39.19)
const storyM = id => { const S = SHIP.social.stories || (SHIP.social.stories = {}), M = S.m || (S.m = {}); return M[id] || (M[id] = { b: 0, at: null, hf: null }); };
function momentNextId(p) {                               // the next beat's id that has a script, ready or not (writers' beats may have gaps)
  const v = voiceOf(p.id), th = v.thread || '', r = SHIP.rel[p.id];
  const n = th.startsWith('arc:') ? (r ? r.arc || 0 : 0) : storyPeek(p.id).b;   // beats told so far (rel.arc for arcs)
  if (th.startsWith('arc:') && n < 1 && STORY_ARCS[p.id]) return null;   // an arc with card lines tells beat 1 on the card
  for (let b = n + 1; b <= n + 6; b++) if (momentDef(p.id + ':' + b)) return p.id + ':' + b;
  return null;
}
const ARC_CREW = new Map();
function arcCrew(arcId) {                                 // whose story an arc is: the crew member whose thread is 'arc:<arcId>' (Torres's is 'torres', his id 'torres-zeke'), else the id itself
  if (!ARC_CREW.size || (VOICE_SRC && ARC_CREW.src !== VOICE_SRC)) { ARC_CREW.clear(); ARC_CREW.src = VOICE_SRC; socInit(); for (const p of SOC.crew) { const th = voiceOf(p.id).thread || ''; if (th.startsWith('arc:') && !ARC_CREW.has(th.slice(4))) ARC_CREW.set(th.slice(4), p.id); } }
  return ARC_CREW.get(arcId) || arcId;
}
const momentOwnsBeat = (id, n) => n >= 1 && (voiceOf(id).thread || '').startsWith('arc:') && !!momentDef(id + ':' + (n + 1));   // section 20's arcBeat leaves it to a moment
const momentHint = id => { const d = momentDef(id); return d && d.hint ? voiceFill(d.who, d.hint) : null; };
const MOMENT_SERIOUS = new Set(['heartfelt', 'serious', 'resolution']);
const momentVisit = p => typeof VISIT !== 'undefined' && !!VISIT && VISIT.inside && VISIT.p === p;   // section 20's bunk visit, they're in
const momentAppt = (p, t) => apptList().some(a => (typeof apptOn !== 'function' || apptOn(a)) && Array.isArray(a.with) && a.with.includes(p.id) && t >= a.at && t < a.at + (a.len || 30));
function momentCalm(p, t, duty) {                        // off duty (or on, for a script with duty) somewhere you could sit and talk, visiting you, or your appointment
  if (momentVisit(p) || momentAppt(p, t)) return true;
  const w = typeof whereIs === 'function' ? whereIs(p, t) : null; if (!w || w.moving || !(w.act === 'leisure' || w.act === 'off' || (duty && w.act === 'work'))) return false;
  const pl = w.placeId && schedData().byId.get(w.placeId);
  return !!pl && (typeof SIT_TYPES === 'undefined' || SIT_TYPES.has(pl.type) || (duty && w.act === 'work'));
}
function momentWhere(p, t, d) {                          // the script's where: 'calm' (default), 'visit', 'appt', 'meal' (at a mess table at breakfast or dinner), 'any' (played in place), or a room's name
  return (Array.isArray(d.where) ? d.where : [d.where || 'calm']).some(x => {
    if (x === 'any') return true;
    if (x === 'meal') { const w = typeof whereIs === 'function' ? whereIs(p, t) : null, pl = w && !w.moving && w.placeId && schedData().byId.get(w.placeId); return !!pl && (w.act === 'breakfast' || w.act === 'dinner') && pl.type === 'mess-seat'; }   // sitting with them at a meal
    if (x === 'calm') return momentCalm(p, t, d.duty);
    if (x === 'visit') return momentVisit(p);
    if (x === 'appt') return momentAppt(p, t);
    const w = typeof whereIs === 'function' ? whereIs(p, t) : null; if (!w || w.moving || !(w.act === 'leisure' || w.act === 'off' || (d.duty && w.act === 'work'))) return false;
    const pl = w.placeId && schedData().byId.get(w.placeId), rm = pl && DECKS[pl.deck] && (DECKS[pl.deck].rooms || {})[pl.room];
    return !!rm && String(rm.name || '').toLowerCase().includes(String(x).toLowerCase());
  });
}
const momentTrad = t => { const d = Math.floor(t / 1440) + 1, m = t - (d - 1) * 1440; let es = []; try { es = typeof eventsOn === 'function' ? eventsOn(d) : []; } catch (e) { es = []; } const e = es.find(x => m >= x.from && m < x.to); return e ? e.id : null; };   // the tradition on now (trad: conditions)
function momentCtx(p, t, id) {                             // the scene's ctx for a beat's when: the tradition on now, and the deck you're on (theirs: you're with them)
  const w = typeof whereIs === 'function' ? whereIs(p, t) : null, pl = w && w.placeId && schedData().byId.get(w.placeId);
  return { t, moment: id, trad: momentTrad(t), deck: pl ? pl.deck : w && w.deck != null ? w.deck : undefined };   // walking: the deck they're on
}
// momentWantsVisit(p, t) -> their next beat wants a bunk visit (where: visit) and its when holds now: section 20's
// evening visits pick them first (Tomas's Wednesday exam night)
function momentWantsVisit(p, t = shipNow()) {
  socInit(); p = socP(p); if (!p || !SOC.idx.has(p.id)) return false;
  const id = momentNextId(p), d = id && momentDef(id); if (!d || ![].concat(d.where || []).includes('visit')) return false;
  return momentReady(p, t, { anywhere: true }) === id;   // every gate but the place (they'd be visiting): a beat that can't open tonight doesn't take the evening's visit
}
function momentReady(p, t = shipNow(), ctx = {}) {
  socInit(); p = socP(p); if (!p || !SOC.idx.has(p.id) || (typeof DIALOGUE !== 'undefined' && DIALOGUE)) return null;
  const id = momentNextId(p), d = id && momentDef(id); if (!d) return null;
  const g = STEP_GATES[d.tone] || STEP_GATES.heartfelt, st = storyPeek(p.id), day = Math.floor(t / 1440) + 1, S = SHIP.social.stories || {};
  if (relTier(p.id) < (d.tier ?? g.tier) || metDays(p.id, t) < (d.metDays ?? g.met)) return null;
  const last = d.tone === 'resolution' ? st.hf : st.at; if (last !== null && (t - last) / 1440 < (d.gapDays ?? g.gap)) return null;
  if (st.at !== null && Math.floor(st.at / 1440) + 1 === day) return null;   // one moment a day each
  const ab = (d.thread || '').startsWith('arc:') && STORY_ARCS[p.id] && STORY_ARCS[p.id][d.beat - 1], r = SHIP.rel[p.id];
  if (ab && ((ab.afterShow && r.showDay && day <= r.showDay) || (r.arcDay || 0) >= day)) return null;   // Pell's last beat waits for his show; one beat a day
  if (MOMENT_SERIOUS.has(d.tone) && S.serious === day) return null;          // one serious moment a day for you
  if (!d.crisis) { let ev = null; try { ev = typeof eventNow === 'function' ? eventNow(t) : null; } catch (e) { ev = null; } if (ev && ev.phase === 'onset') return null; }
  if (d.when) { let ok = false; try { ok = typeof linesOk === 'function' ? !!linesOk(d.when, p, momentCtx(p, t, id)) : false; } catch (e) { ok = false; } if (!ok) return null; }   // the writers' conditions, judged by section 22 as for lines
  if (!ctx.anywhere && !momentWhere(p, t, d)) return null;
  return id;
}
function momentShow(id) {
  socInit(); const d = momentDef(id), p = d && socP(d.who); if (!d || !p || typeof MEETING_SCRIPTS === 'undefined' || typeof dialogueShow !== 'function') return false;
  if (typeof DIALOGUE !== 'undefined' && DIALOGUE) return false;
  const t = shipNow(), arc = STORY_ARCS[p.id], fill = s => voiceFill(p.id, typeof s === 'function' ? s(p) : s, t);
  const who = w => !w || w === 'them' ? p.id : w;        // a theme's speaker is whoever has the theme
  const say = (x, w) => typeof x === 'object' && x ? { who: who(x.who || w), text: fill(x.text), pose: x.pose } : { who: who(w), text: fill(x) };   // a reply as text, or { who, text, pose }
  const lines = d.lines.map(l => l.choice ? { choice: l.choice.map(c => ({ text: fill(c.text), flavour: c.flavour, fit: c.flavour === voiceOf(p.id).needs, c,
      reply: c.reply ? say(c.reply) : null })) }
    : { who: who(l.who), text: fill(l.say !== undefined && arc && arc[l.say] ? arc[l.say].say : l.text), pose: l.pose, to: l.to });
  let picked = null;
  MEETING_SCRIPTS['moment:' + id] = { title: shortName(p), lines,
    onPick: (k, c) => { picked = c; if (c.fit && c.c.warm) c.reply = say(c.c.warm); },   // the reply that fits them best can have a warmer answer
    onEnd: () => { delete MEETING_SCRIPTS['moment:' + id]; if (picked) momentDone(p, d, picked); } };
  return dialogueShow('moment:' + id, { id: 'moment:' + id, who: [p.id], at: t, where: hereWhere() });
}
// favours that matter (0.39.6, B4): a moment's practical reply with `favour: <id>` starts one of these on section 20's
// favour types (the lead's ruling: no new jobs), accepted at once (you offered), in your Jobs, handed back on their
// card ("Done: here you go"). Any other favour id, or one done in the scene itself (holt.invite), is just a flag.
// STORY_FAVOURS[id](p) -> the favourPost argument, or null
const storyPlace = (type, deck) => { const S = schedData(); for (const pl of S.byId.values()) if (pl.type === type && (deck === undefined || pl.deck === deck)) return pl; return null; };
const STORY_FAVOURS = {
  brennanSage: p => { const pl = storyPlace('garden', 3); return pl && { from: p.id, title: 'Sage from the garden for ' + shortName(p) + ' (Deck 3)', bring: 'a bunch of sage', stops: [{ deck: pl.deck, placeId: pl.id, mins: 3, tag: 'pickup' }] }; },
  pellPractice: p => { const pl = p.work && storyPlace(p.work.place, p.work.deck); return pl && { from: p.id, title: 'Help ' + shortName(p) + ' practise for his certification (' + deckIn(pl.deck) + ')', stops: [{ deck: pl.deck, placeId: pl.id, mins: 15, tag: 'favour' }] }; },
  liftBrakes: p => { const pl = p.work && storyPlace(p.work.place, p.work.deck); return pl && { from: p.id, title: 'Check the lift brakes with ' + shortName(p) + ' (' + deckIn(pl.deck) + ')', stops: [{ deck: pl.deck, placeId: pl.id, mins: 15, tag: 'favour' }] }; },   // a stop at their station (reviewer 1: not a lamp swap)
};
function storyFavour(p, id) {
  const mk = STORY_FAVOURS[id]; if (!mk || typeof favourPost !== 'function') return false;
  let post = null; try { post = mk(p); } catch (e) { post = null; } if (!post) return false;
  const fid = favourPost(post); if (!fid) return false;
  if (typeof favourAccept === 'function') favourAccept(fid);
  return true;
}
function momentDone(p, d, c) {                           // the reply was picked: the moment counts
  const t = Math.floor(shipNow()), day = Math.floor(t / 1440) + 1, st = storyM(p.id), S = SHIP.social.stories, v = voiceOf(p.id), r = relGet(p.id);
  if (d.tone === 'goodbye') return goodbyeDone(p, d, c);
  const th = (d.thread || '').replace(/^arc:/, ''), flavour = c.flavour || 'listen';
  st.at = t; if (MOMENT_SERIOUS.has(d.tone)) { S.serious = day; if (d.tone !== 'resolution') st.hf = t; }
  if (!(d.thread || '').startsWith('arc:')) st.b = Math.max(st.b, d.beat);
  const pts = ((MOMENT_PTS[d.tone] || 5) + (c.fit ? MOMENT_FIT : 0)) * (v.opennessSet ? OPENNESS[v.openness].moment : 1);
  relAdd(p.id, 'moment', pts);
  const word = c.c && c.c.mem || d.mem;                 // the writers' memory word (moment.<arc>.<word>), else one made from the beat
  memAdd(p.id, 'moment.' + th + '.' + (word || d.beat + '.' + flavour), d.tone === 'resolution' ? { cls: 'core' } : {});
  if (typeof flagSet === 'function') for (const f of [d.flag, c.c && c.c.flag, c.c && c.c.favour]) if (f) flagSet(f);   // the beat's flag, the reply's, and a favour done in the scene itself, for later beats
  if (c.c && c.c.favour) storyFavour(p, c.c.favour);   // a favour that matters, in your Jobs
  if (d.learn && !r.known.includes('@story:' + d.learn)) r.known.push('@story:' + d.learn);
  if (typeof simNote === 'function') simNote('moment', { id: p.id + ':' + d.beat, who: p.id, beat: d.beat, flavour, tone: d.tone, fit: !!c.fit });
  if (d.tone === 'resolution' && typeof giftKeepsake === 'function') giftKeepsake(p, d.keepsake || v.keepsake);
  if (d.after && d.after.mail) SHIP.social.mail.push({ at: t + (d.after.mail.after || 60), from: p.name, subject: d.after.mail.subject, body: voiceFill(p.id, d.after.mail.body) });
  const arc = (d.thread || '').startsWith('arc:') && STORY_ARCS[p.id], n = d.beat - 1;
  if (arc && arc[n] && (r.arc || 0) === n) {             // section 20's arc goes on: its count, Mail and Pell's show
    if (typeof arcTold === 'function') arcTold(p, arc[n]);
    if ((r.arc || 0) === n) { r.arc = n + 1; r.arcDay = SHIP.time.day; if (arc[n].mail) SHIP.social.mail.push({ at: t + arc[n].mail.after, from: p.name, subject: arc[n].mail.subject, body: arc[n].mail.body }); }   // an older arcTold that takes no beat
  } else if ((d.thread || '').startsWith('arc:') && (r.arc || 0) < d.beat) { r.arc = d.beat; r.arcDay = SHIP.time.day; }   // beats past section 20's card lines, and the new story crew's
}
// ---- goodbyes (0.39.4, B5; plans/social-deep-plan.md Part 8b "Goodbyes") ----
// A day or two before someone is transferred off, section 20's card leads with their goodbye (anyone at acquaintance
// or better) and asks goodbyeMoment(p, t) -> { id: '<crewId>:bye', hint } | null; "Sit with them" plays it on the
// moments engine, anywhere (they came to find you; no gates, never counted as the day's serious moment). The scene
// talks about your friendship: the writers' own MOMENTS['<crewId>:bye'] when there is one, else goodbyeDef builds it
// from where they're going and when, their heaviest memories of you (section 20's memThing: "the oven, the quiz"), a
// moment you shared, and how close you are; one choice of four flavours; a close friend gives you their keepsake.
// After: relAdd 'moment' (GOODBYE_PTS, +MOMENT_FIT for the flavour they need), memAdd 'moment.bye.<flavour>' (core),
// simNote('moment', { tone: 'goodbye' }), and storyM(id).bye = the day (said once)
const GOODBYE_PTS = 3;
const GOODBYE_WHEN = ['today', 'tomorrow', 'the day after tomorrow'];
function goodbyeMoment(p, t = shipNow()) {
  socInit(); p = socP(p); if (!p || !SOC.idx.has(p.id) || storyPeek(p.id).bye) return null;
  const left = typeof leavingSoon === 'function' ? leavingSoon(p, Math.floor(t / 1440) + 1) : null; if (left === null || left > 2) return null;
  const d = goodbyeDef(p.id); if (!d) return null;
  return { id: p.id + ':bye', hint: voiceFill(p.id, d.hint, t) };
}
function goodbyeDef(id) {
  const p = socP(id); if (!p) return null;
  const [MO] = momentBaked(), own = MO && MO[id + ':bye'];
  if (own && Array.isArray(own.lines)) return Object.assign({ who: id, beat: 'bye', thread: voiceOf(id).thread || '', hint: 'Got a minute? Before I go.' }, own, { who: id, beat: 'bye', tone: 'goodbye' });
  const tier = relTier(id), left = typeof leavingSoon === 'function' ? leavingSoon(p) : null, when = GOODBYE_WHEN[left] || 'soon';
  const to = p.transferTo ? 'the ' + String(p.transferTo).replace(/^the /i, '') : 'another ship';
  const mem = (SHIP.mem[id] || []).slice().sort((a, b) => b[2] - a[2] || (a[0] < b[0] ? -1 : 1));
  const things = [...new Set(mem.map(m => typeof memThing === 'function' ? memThing(m[0]) : null).filter(Boolean))].slice(0, 2);
  const sat = mem.some(m => /^moment\./.test(m[0]) && !/\.bye\./.test(m[0]));
  const lines = [{ who: id, text: (tier >= 3 ? 'I wanted to catch you properly. ' : '') + 'I\'m off to ' + to + ' ' + when + '. Transferred.' }];
  if (things.length) lines.push({ who: id, text: 'I keep thinking about ' + things.join(', and ') + '. You were part of all that.' });
  else lines.push({ who: id, text: tier >= 2 ? 'We didn\'t get as much time as I\'d have liked. You made the place friendlier, though.' : 'We only just got to know each other. Shame, that.' });
  if (sat && tier >= 3) lines.push({ who: id, text: 'And that evening you sat with me. I won\'t forget it.', pose: 'sigh' });
  lines.push({ choice: [
    { text: 'I\'ll miss you. Tell me about where you\'re going.', flavour: 'listen', reply: 'A bigger ship. More people. I\'ll get lost for a week, I expect.' },
    { text: 'Who\'s going to keep me in line now?', flavour: 'cheer', reply: 'Ha! You\'ll manage. Mostly.' },
    { text: 'Write to me. I mean it.', flavour: 'practical', reply: 'Every couple of weeks. You\'d better write back.' },
    { text: 'You made this place feel like home.', flavour: 'share', reply: 'So did you. Honestly.' }].filter((c, k) => tier >= 2 || k !== 3) });
  lines.push({ who: id, text: tier >= 4 ? 'Here. I want you to have this. So you don\'t forget me.' : tier >= 3 ? '{bye}, {nick}. Look after yourself.' : '{bye}. Look after the old Wren.' });
  return { who: id, beat: 'bye', thread: voiceOf(id).thread || '', tone: 'goodbye', hint: tier >= 3 ? 'Got a minute? There\'s something I need to tell you properly.' : 'Before I go, have you got a minute?', keepsake: tier >= 4 ? voiceOf(id).keepsake : null, lines };
}
function goodbyeDone(p, d, c) {
  const v = voiceOf(p.id), flavour = c.flavour || 'listen';
  storyM(p.id).bye = SHIP.time.day;
  relAdd(p.id, 'moment', (GOODBYE_PTS + (c.fit ? MOMENT_FIT : 0)) * (v.opennessSet ? OPENNESS[v.openness].moment : 1));
  memAdd(p.id, 'moment.bye.' + flavour, { cls: 'core' });
  if (typeof simNote === 'function') simNote('moment', { id: p.id + ':bye', who: p.id, beat: 'bye', flavour, tone: 'goodbye', fit: !!c.fit });
  if (relTier(p.id) >= 4 && typeof giftKeepsake === 'function') giftKeepsake(p, d.keepsake || v.keepsake);
}
// ---- bonds in the save, compact (0.39.21, the lead's headroom job) ----
// section 20's socSave asks storyBondsPack(B) for SHIP.social.bonds and bondsUnpack hands { v: 2 } back to
// storyBondsUnpack(o, ids): 12 bytes a bond in base64 (i, j: crew indexes in the save's id list; kind; since, 3 bytes,
// 0xFFFFFF for none; peak, a signed byte, -128 for none; seen, 2 bytes, 0xFFFF for none; flags: 1 spar; gone, 2 bytes,
// 0 for none), and any other field a bond carries in x: [[row, { ... }]]. Every value is a whole number (affinity is an
// Int8Array, times are ship minutes and hours), so a load gives back exactly what was saved
const BOND_T0 = 20160, BOND_H0 = 336;                    // since (minutes) and seen (hours) are stored with this added: a game that starts with the day-0 arrival makes its couples before minute 0 (two weeks of room)
function storyBondsPack(B) {
  if (SOC.n > 255) return null;                         // a crew index is one byte: a bigger crew saves in section 20's own form
  let bin = ''; const x = [], b3 = v => String.fromCharCode(v >> 16 & 255, v >> 8 & 255, v & 255), b2 = v => String.fromCharCode(v >> 8 & 255, v & 255);
  for (const k in B || {}) { const [a, c] = k.split(':'), o = B[k], i = SOC.idx.get(a), j = SOC.idx.get(c), ki = SOC_BOND_KINDS.indexOf(o.kind);
    if (i === undefined || j === undefined || ki < 0) continue;
    const { kind, since, peak, seen, spar, gone, ...rest } = o, ok = (v, z, top) => v == null || (Number.isInteger(v) && v + z >= 0 && v + z < top);
    if (!ok(since, BOND_T0, 0xFFFFFF) || !ok(seen, BOND_H0, 0xFFFF) || (gone != null && (!Number.isInteger(gone) || gone < 1 || gone > 0xFFFF)) || (peak != null && (!Number.isInteger(peak) || peak < -127 || peak > 127)) || (spar != null && spar !== true)) return null;   // not a shape this form holds: section 20's own form
    if (Object.keys(rest).length) x.push([bin.length / 12, rest]);
    bin += String.fromCharCode(i, j, ki) + b3(since == null ? 0xFFFFFF : since + BOND_T0) + String.fromCharCode((peak ?? -128) & 255) + b2(seen == null ? 0xFFFF : seen + BOND_H0) + String.fromCharCode(spar ? 1 : 0) + b2(gone ?? 0); }
  return x.length ? { v: 2, z: 1, b: btoa(bin), x } : { v: 2, z: 1, b: btoa(bin) };   // z: the offsets above (0.39.22)
}
function storyBondsUnpack(o, ids) {
  const B = {}, z = o.z === 1, T0 = z ? BOND_T0 : 0, H0 = z ? BOND_H0 : 0; let bin = ''; try { bin = atob(o.b || ''); } catch (e) { return B; }
  const X = new Map((Array.isArray(o.x) ? o.x : []).filter(r => Array.isArray(r) && r[1] && typeof r[1] === 'object').map(r => [r[0], r[1]]));
  for (let r = 0, k = 0; k + 11 < bin.length; r++, k += 12) {
    const u = q => bin.charCodeAt(k + q), a = ids[u(0)], c = ids[u(1)], kind = SOC_BOND_KINDS[u(2)];
    if (!a || !c || !kind || !SOC.idx.has(a) || !SOC.idx.has(c)) continue;
    const since = u(3) << 16 | u(4) << 8 | u(5), peak = u(6) << 24 >> 24, seen = u(7) << 8 | u(8), gone = u(10) << 8 | u(11), b = { kind };
    if (since !== 0xFFFFFF) b.since = since - T0; if (peak !== -128) b.peak = peak; if (seen !== 0xFFFF) b.seen = seen - H0; if (u(9) & 1) b.spar = true; if (gone) b.gone = gone;
    if (X.has(r)) Object.assign(b, X.get(r));
    B[a + ':' + c] = b;
  }
  return B;
}
// ---- farewells (0.39.16, the overnight plan; social-deep-plan Part 8b "On the day") ----
// Who comes to the shuttle bay to see a leaver off on their last day (rotation days: crewLeaving), for section 14's
// plans: their closest friends aboard by the weekly snapshot (affinityPlan, so a day planned twice agrees; never live
// bonds), FAREWELL_AT or more, up to FAREWELL_MAX, closest first; each one's partner beside them and the leaver's own
// partner (couples stand together). Not the player (you choose to come), nobody leaving that day themselves.
//   farewellCrew(leaver, d) -> [crewId]
const FAREWELL_AT = 60, FAREWELL_MAX = 4;
function farewellCrew(leaver, d) {
  socInit(); const p = socP(leaver); if (!p) return [];
  const here = q => !!q && q !== p && q.rank !== 'guest' && socAboard(q, d) && leaveDay(q) !== d;
  const near = SOC.crew.filter(here).map(q => [q, affinityPlan(p, q, d)]).filter(x => x[1] >= FAREWELL_AT)
    .sort((a, b) => b[1] - a[1] || (a[0].id < b[0].id ? -1 : 1)).slice(0, FAREWELL_MAX).map(x => x[0]);
  const out = new Set(near.map(q => q.id)), mate = q => q.partner && SOC.idx.has(q.partner) ? socP(q.partner) : null;
  for (const q of [...near, p]) { const m = mate(q); if (here(m)) out.add(m.id); }
  return [...out];
}
// ---- calls home (0.39.7, B8; the user's design, head writer 2's call files, the dialogue engineer's baked shapes) ----
// Your people back home: Mum, Gran, Jo and Sam (HOME_CONTACTS, baked from content/home/<contact>.call; Jo and Sam are
// "they"; home stays unnamed). At a call-home booth, section 15's "Calling home" asks homeBooth(): whom to call, any day,
// ONE call a ship day in all (the user's rule, 0.62.0: H.call is the day of your last call). A call plays their next arc
// beat when it's due (HOME_MOMENTS['<contact>:<n>']), else an everyday call (a HOME_CHAT scene, homeChatPick). Calls are
// one-sided (the user, 0.62.0): only they speak, you listen; no choices (HOME_SEND is no longer used).
// Pacing: beat 1 on your first call to them; each later beat on your first call to them HOME_GAP (7) or more days after
// the one before, any day. A `via: live` beat is a call on a clear line (no lag); the rest come over the relay. (Before
// 0.62.0 the live beats waited for Letters evening, a Sunday hour with the booths full, so most players never heard
// past beat 2; the user scratched Letters evening.) The booth says who has news. State in SHIP.social.stories.home (saved by section 20) =
// { day, call, f: { <flag>: 1 }, learn: [], c: { <contact>: { b, at, chat, day, mem: [], h: [scene tags heard, last 16],
// news: [news scenes heard], msg } } } (older saves also carry last and sent, unused now).
//   homeBooth(t) -> the booth's picker, then the call, in one dialogue (false if one is up)   homeCall(contact, t) -> one call
//   homeCallable(t) -> [{ contact, name, due, hint }] whom you can call now ([] once you've called today)   homeCalledToday(t)
//   homeBeatOf('home.mum') -> beats told   homeKnown() -> what you've learned about home   homeFlags() -> the home flags
//   After a beat heard to the end: its flag (here and section 13's flagSet), memory word, learn, keepsake, Mail;
//   simNote('homeCall', { contact, who, beat, tone, via, live, flavour })
const HOME_GAP = 7;                                      // days between one person's beats
const HOME_ORDER = ['mum', 'gran', 'jo', 'sam'], HOME_DAYS = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'];
const HOME_META = new Set(['text', 'id', 'tone', 'flavour', 'reply', 'sets', 'memo', 'lines', 'w', 'odds', 'old']);
const homeBaked = () => { const g = f => { try { return f() || null; } catch (e) { return null; } };   // section 22's baked blocks (not there yet: none)
  return [g(() => typeof HOME_CONTACTS !== 'undefined' && HOME_CONTACTS), g(() => typeof HOME_MOMENTS !== 'undefined' && HOME_MOMENTS), g(() => typeof HOME_SEND !== 'undefined' && HOME_SEND), g(() => typeof HOME_CHAT !== 'undefined' && HOME_CHAT)]; };
const homeState = () => { socInit(); const S = SHIP.social.stories || (SHIP.social.stories = {}); return S.home || (S.home = { day: null, f: {}, learn: [], c: {} }); };
const homeC = k => { const H = homeState(); return H.c[k] || (H.c[k] = { b: 0, at: null, chat: null, day: null, last: null, sent: [], mem: [] }); };
const HOME_NONE = Object.freeze({ day: null, f: Object.freeze({}), learn: Object.freeze([]), c: Object.freeze({}) }), HOME_C0 = Object.freeze({ b: 0, at: null, chat: null, day: null, last: null, sent: Object.freeze([]), mem: Object.freeze([]) });
const homePeek = () => (SHIP.social && SHIP.social.stories && SHIP.social.stories.home) || HOME_NONE;   // read-only: queries (line conditions, the device) never write the save
const homePeekC = k => homePeek().c[k] || HOME_C0;
const homeP = hc => ({ id: hc.id, name: hc.name, pron: hc.pron || null, seed: socHash(hc.id) });   // a home person for section 22's linesOk / linesFill
const homeBeatOf = arcId => { const m = /^home\.(.+)$/.exec(String(arcId)); return m ? homePeekC(m[1]).b : 0; };
const homeFlags = () => ({ ...homePeek().f });
const homeKnown = () => homePeek().learn.slice();
const homeCalledToday = (t = shipNow()) => homePeek().call === Math.floor(t / 1440) + 1;   // one call home a ship day, in all
function homeCtx(t) {                                    // the call's ctx: home flags, the tradition you went to lately (last 3 days), your closest friend aboard
  const H = homePeek(), d = Math.floor(t / 1440) + 1, ctx = { t, flags: { ...H.f } };
  const J = ((SHIP.events && SHIP.events.joined) || []).map(k => /^(.+)@(\d+)$/.exec(k)).filter(m => m && +m[2] <= d && +m[2] >= d - 3).pop();
  if (J) { let tr = typeof SHIP_TRADITIONS !== 'undefined' ? SHIP_TRADITIONS.find(x => x.id === J[1]) : null; try { tr = tr || (typeof eventsOn === 'function' ? eventsOn(+J[2]).find(x => x.id === J[1]) : null); } catch (e) { }
    if (tr && tr.name) { ctx.trad = tr.name.toLowerCase(); ctx.tradId = J[1]; } }
  let best = null; for (const id in SHIP.rel) { const r = SHIP.rel[id]; if (r && r.tier >= 3 && SOC.idx.has(id) && (!best || r.pts > best[1].pts)) best = [id, r]; }
  if (best) { ctx.friend = shortName(socP(best[0])); ctx.friendId = best[0]; }
  return ctx;
}
function homeOk(e, hp, ctx) {                            // a beat's when, a chat's when, a send line: home beats here, the rest by section 22's linesOk
  if (!e) return true;
  const o = { ...e }, beat = o.beat; delete o.beat;
  const told = x => { const i = x.lastIndexOf('.'), a = x.slice(0, i); return (a.startsWith('home.') ? homeBeatOf(a) : typeof beatOf === 'function' ? beatOf(a) || 0 : 0) >= +x.slice(i + 1); };
  if (beat !== undefined && ![].concat(beat).every(v => String(v).split('|').some(told))) return false;
  for (const k of HOME_META) delete o[k];                // a send line's data (reply, flavour, sets, memo...) isn't a condition, whichever section 22 judges it
  if (typeof linesOk === 'function') { try { return !!linesOk(o, hp, ctx); } catch (e2) { return false; } }
  for (const k in o) {                                   // no dialogue engine yet: flags, weekdays, came: and friend:; anything else waits for it
    if (HOME_META.has(k)) continue;
    const all = f => [].concat(o[k]).every(v => String(v).split('|').some(f));
    if (k === 'flag') { if (!all(x => x in ctx.flags ? !!ctx.flags[x] : typeof flag === 'function' && !!flag(x))) return false; }
    else if (k === 'weekday') { if (!all(x => HOME_DAYS[weekday(Math.floor(ctx.t / 1440) + 1)] === x)) return false; }
    else if (k === 'came') { if (!all(x => !!ctx.trad && (x === 'any' || ctx.tradId === x))) return false; }
    else if (k === 'friend') { if (!all(() => !!ctx.friend)) return false; }
    else return false;
  }
  return true;
}
function homeFill(text, hp, ctx) {                       // section 22's linesFill (null: a placeholder it can't fill), else {me}, {trad}, {friend}
  if (typeof linesFill === 'function') { try { return linesFill(text, hp, ctx); } catch (e) { return null; } }
  let ok = true; const s = String(text).replace(/\{([a-z]+)\}/g, (m, k) => { const x = k === 'me' ? (typeof ROSTER_PLAYER !== 'undefined' && ROSTER_PLAYER.first) || 'cadet' : ctx[k]; if (x == null) ok = false; return x == null ? m : String(x); });
  return ok ? s : null;
}
function homeNext(k, t) {                                // their next beat if its time has come ('<contact>:<n>'); else null
  const [HC, HM] = homeBaked(), hc = HC && HC[k]; if (!hc || !HM) return null;
  const c = homePeekC(k), id = k + ':' + (c.b + 1), d = HM[id];
  if (!d || !Array.isArray(d.lines)) return null;
  if (c.b > 0 && (c.at === null || (t - c.at) / 1440 < HOME_GAP)) return null;   // beat 1 on the first call; then 7+ days after the last beat
  return homeOk(d.when, homeP(hc), homeCtx(t)) ? id : null;
}
const homeDue = (k, t = shipNow()) => homeNext(k, t);    // the beat a call now plays
function homeCallable(t = shipNow()) {
  const [HC, HM] = homeBaked(); if (!HC || homeCalledToday(t)) return [];
  let ev = null; try { ev = typeof eventNow === 'function' ? eventNow(t) : null; } catch (e) { ev = null; } if (ev && ev.phase === 'onset') return [];   // the relay's down while a ship-wide event starts
  const ord = k => HOME_ORDER.includes(k) ? HOME_ORDER.indexOf(k) : 99;
  return Object.keys(HC).sort((a, b) => ord(a) - ord(b) || (a < b ? -1 : 1)).filter(k => homeNext(k, t) || homeChatPick(k, t)).map(k => {   // only someone with something to play (reviewer 1c)
    const n = homeNext(k, t), d = n && HM[n];
    return { contact: k, name: HC[k].name, due: !!d, first: homePeekC(k).b === 0, hint: d && d.hint ? homeFill(d.hint, homeP(HC[k]), homeCtx(t)) || d.hint : null };
  });
}
// One-sided calls (the user, 0.62.0): only they speak; you listen. A beat's `? choice` lines (old content) are left
// out, with their replies. An ordinary call is one HOME_CHAT scene, picked without repeats (homeChatPick): a news
// reaction first (a scene whose when: uses cue:, came:, friend: or flag:intro.*: each plays once, c.news), else a scene
// whose when: holds and that's not among the last HOME_HEARD you heard from them (c.h), ones about another person's
// story first (their window is short), then ones with a when: (the arc stage, the day), else the one heard longest ago. Old scenes' `send` markers are left out.
const HOME_HEARD = 16, HOME_NEWS_MAX = 8;               // scenes remembered per person: the last 16 heard, the 8 newest news reactions
const homeTag = e => socHash(JSON.stringify(e.lines)).toString(36);
const homeIsNews = e => !!e.when && Object.keys(e.when).some(k => k === 'cue' || k === 'came' || k === 'friend' || (k === 'flag' && [].concat(e.when.flag).some(v => /^intro\./.test(String(v)))));
function homeChatPick(k, t, msg) {                       // the ordinary scene a call (or a recorded message: msg, no news) plays now, or null
  const [HC, , , HCH] = homeBaked(), hc = HC && HC[k]; if (!hc) return null;
  const hp = homeP(hc), ctx = homeCtx(t), c = homePeekC(k), heard = c.h || [], told = c.news || [], day = Math.floor(t / 1440) + 1;
  const pool = ((HCH && HCH[k]) || []).filter(e => e && Array.isArray(e.lines) && e.lines.some(l => l.text) && homeOk(e.when, hp, ctx));
  const rnd = a => a.length ? a[Math.floor(schedU(hp.seed, day, 683) * a.length)] : null;
  const news = msg ? null : rnd(pool.filter(e => homeIsNews(e) && !told.includes(homeTag(e)))); if (news) return news;
  const plain = pool.filter(e => !homeIsNews(e)), fresh = plain.filter(e => !heard.includes(homeTag(e)));
  const cross = e => !!e.when && [...JSON.stringify(e.when).matchAll(/home\.([a-z]+)\./g)].some(m => m[1] !== k);   // about someone else's story (Jo watering Gran's marrow): its window is short
  return rnd(fresh.filter(cross)) || rnd(fresh.filter(e => e.when)) || rnd(fresh) || plain.slice().sort((x, y) => heard.indexOf(homeTag(x)) - heard.indexOf(homeTag(y)))[0] || null;
}
function homeLines(k, t) {                               // one call: { d (the beat, or null), e (the scene), title, live, lines } for section 18's panel
  const [HC, HM] = homeBaked(), hc = HC && HC[k]; if (!hc) return null;
  const hp = homeP(hc), ctx = homeCtx(t), id = homeDue(k, t), d = id && HM[id], live = !!d && d.via === 'live', name = hc.name;
  const fill = s => homeFill(s, hp, ctx) ?? String(s), who = w => !w || w === 'them' || w === hc.id ? name : w;   // section 18 shows a name it doesn't know as it is
  const say = l => ({ who: who(l.who), text: fill(l.text), pose: l.pose });
  const title = name + (live ? ', on a clear line' : ', on the relay');
  const e = d ? null : homeChatPick(k, t); if (!d && !e) return null;
  return { d, e, title, live, lines: (d || e).lines.filter(l => l.text).map(say) };
}
function homeScript(k, t) {                              // the call as a script with onEnd; null if you can't call them now
  if (!homeCallable(t).some(x => x.contact === k)) return null;
  const L = homeLines(k, t); if (!L) return null;
  const c = homeC(k); c.day = homeState().call = Math.floor(t / 1440) + 1; if (!L.d) c.chat = Math.floor(t);   // they picked up: your one call home today
  if (L.e) { const g = homeTag(L.e); if (homeIsNews(L.e)) { c.news = c.news || []; if (!c.news.includes(g)) c.news = c.news.concat(g).slice(-HOME_NEWS_MAX); }   // heard: news once, the rest not again soon
    else c.h = (c.h || []).filter(x => x !== g).concat(g).slice(-HOME_HEARD); }
  if (c.msg && !c.msg.done) c.msg.done = true;            // a call answers their recorded message
  return { title: L.title, lines: L.lines, onEnd: f => { delete MEETING_SCRIPTS['home:' + k]; homeDone(k, L, f, t); } };
}
function homeCall(k, t = shipNow()) {
  if (typeof MEETING_SCRIPTS === 'undefined' || typeof dialogueShow !== 'function' || (typeof DIALOGUE !== 'undefined' && DIALOGUE)) return false;
  const s = homeScript(k, t); if (!s) return false;
  MEETING_SCRIPTS['home:' + k] = s;
  return dialogueShow('home:' + k, { id: 'home:' + k, who: [], at: t, where: HOME_WHERE });
}
// where a call is (0.62.5, the user's "the menu to call someone disappears"): section 18's meetingsTick closes a dialogue
// once a ship minute (under 2 real seconds) when you're not in its meeting's place (inMeeting(m), by m.where); without a
// where that's never true, so every call, recorded message and moment closed by itself. Calls happen at the booths
// (walk out and the call ends); a moment is wherever you are (any room on this deck, as section 21's introAsk does); a
// recorded message plays on your device anywhere, through doorways and the lift (0.62.6, reviewer 1e: where.any).
const HOME_WHERE = { deck: 3, room: /^Call-home booths$/ };
const hereWhere = () => ({ deck: typeof deckDef !== 'undefined' && deckDef ? deckDef.num : 3, room: /./ });
const HOME_FIRST = 'Your first call home. Four names on the screen, and a little lag on the line. Who first?';
function homeBooth(t = shipNow()) {                      // the booth: whom to call (the only choice), then the call, in one dialogue
  if (typeof MEETING_SCRIPTS === 'undefined' || typeof dialogueShow !== 'function' || (typeof DIALOGUE !== 'undefined' && DIALOGUE)) return false;
  const [HC] = homeBaked(), can = homeCallable(t), hint = can.find(x => x.hint), news = can.filter(x => x.due && !x.first), H = homePeek();
  const and = a => a.length < 2 ? a.join('') : a.slice(0, -1).join(', ') + ' and ' + a[a.length - 1];
  const text = !HC ? 'The screen says the relay\'s busy. Try again later.'
    : homeCalledToday(t) ? 'You\'ve had your call home today: the relay gives everyone aboard one call a day. ' + and(HOME_ORDER.filter(k => HC[k]).map(k => HC[k].name)) + ' will be there tomorrow.'
    : !can.length ? 'The relay\'s down for a bit while the ship sorts itself out. Try again later.'
    : !Object.values(H.c).some(c => c.day != null) ? HOME_FIRST   // never called anyone yet
    : hint ? hint.hint + ' One call a day.' : news.length ? and(news.map(x => x.name)) + (news.length > 1 ? ' have' : ' has') + ' news. One call a day on the relay.' : 'The relay\'s up, with a little lag. One call a day.';
  const lines = [{ who: 'Booth', text }]; let call = null;
  lines.push({ choice: can.map(x => ({ text: 'Call ' + x.name + (x.due && !x.first ? ' (news)' : ''), k: x.contact })).concat([{ text: can.length ? 'Not now' : 'Hang up', k: null }]) });
  MEETING_SCRIPTS['home:booth'] = { title: 'Calling home', lines,
    onPick: (i, c) => { if (call) return; const s = c.k && homeScript(c.k, t); if (!s || !DIALOGUE) return;
      call = s; MEETING_SCRIPTS['home:booth'].title = s.title; DIALOGUE.queue.splice(DIALOGUE.i + 1, 0, ...s.lines); },   // the call goes on in the same panel
    onEnd: f => { delete MEETING_SCRIPTS['home:booth']; if (call) call.onEnd(f); } };
  return dialogueShow('home:booth', { id: 'home:booth', who: [], at: t, where: HOME_WHERE });
}
function homeDone(k, L, f, t) {                          // the call ended: a beat counts once heard to the end (hung up early, it plays next time)
  const hc = homeBaked()[0][k], c = homeC(k), H = homeState(), d = L.d, now = Math.floor(t);
  const on = x => { if (!x) return; H.f[x] = 1; if (typeof flagSet === 'function') flagSet(x); };
  const told = !!(d && f);
  if (told) {
    c.b = Math.max(c.b, d.beat); c.at = now; H.day = Math.floor(t / 1440) + 1;
    on(d.flag); if (d.mem && !c.mem.includes(d.mem)) c.mem.push(d.mem);
    if (d.learn && !H.learn.includes(d.learn)) H.learn.push(d.learn);
    if (d.keepsake) { const K = SHIP.social.keepsakes || (SHIP.social.keepsakes = []); if (!K.some(q => q.from === hc.name) && K.length < 8) K.push({ from: hc.name, what: d.keepsake, day: SHIP.time.day }); }   // your shelf (section 20's keepsakes)
    if (d.after && d.after.mail) SHIP.social.mail.push({ at: now + (d.after.mail.after || 60), from: hc.name, subject: d.after.mail.subject, body: homeFill(d.after.mail.body, homeP(hc), homeCtx(t)) ?? d.after.mail.body });
  }
  if (typeof simNote === 'function') simNote('homeCall', { contact: k, who: hc.id, beat: told ? d.beat : null, tone: d ? d.tone : 'chat', via: d ? d.via || 'reply' : null, live: !!L.live, flavour: null });
}
// recorded messages (0.39.8, the user's extra): someone you haven't called for HOME_MSG.quiet days records a message
// (one of their everyday calls, HOME_CHAT) at noon (storyHour), at most one message a ship day and each person every
// HOME_MSG.every days, half the time. It comes in Mail with `play: 'home:<contact>'`; the device's Play (section 19 asks
// mailPlay(m)) plays it, one-sided like a call (0.62.0: no reply to record); heard to the end, it's done, and a call to
// them answers it too. It isn't a call (no limit). State: c.msg = { day, i (the HOME_CHAT call), done }, home.msgDay.
//   mailPlay(m) -> plays a recorded message from home (by its sender and subject, or `play: 'home:<contact>'`), else a
//     Mail's `play` moment id (momentShow); mailPlayable(m) -> whether there's anything to play; homeFolks() -> their names
const HOME_MSG = { quiet: 3, every: 5, hour: 12, odds: .5, back: 1440 };
function homeMsgHour(h) {                                // storyHour, every ship hour
  if (h % 24 !== HOME_MSG.hour) return;
  const [HC, , , HCH] = homeBaked(); if (!HC || !HCH) return;
  const t = h * 60, day = Math.floor(t / 1440) + 1, ord = k => HOME_ORDER.includes(k) ? HOME_ORDER.indexOf(k) : 99;
  if (homePeek().msgDay === day) return;
  for (const k of Object.keys(HC).sort((a, b) => ord(a) - ord(b) || (a < b ? -1 : 1))) {
    const c = homePeekC(k), hp = homeP(HC[k]);
    if (!c.b || (c.msg && !c.msg.done) || (c.msg && day - c.msg.day < HOME_MSG.every) || (c.day !== null && day - c.day < HOME_MSG.quiet)) continue;   // called once, not lately, no message waiting
    if (schedU(hp.seed, day, 685) >= HOME_MSG.odds) continue;
    const e = homeChatPick(k, t, true), i = e ? HCH[k].indexOf(e) : -1; if (i < 0) continue;   // a scene, no news reaction (those are for calls)
    const ctx = homeCtx(t), first = e.lines.find(l => l.text);
    homeC(k).msg = { day, i, done: false }; homeState().msgDay = day;   // only now does the save change
    SHIP.social.mail.push({ at: t, from: HC[k].name, subject: HOME_MSG_SUBJECT, play: 'home:' + k,
      body: (first ? '"' + (homeFill(first.text, hp, ctx) ?? first.text) + '" ' : '') + '(Recorded at home. Play it to hear the rest.)' });
    return;
  }
}
const HOME_MSG_SUBJECT = 'A recorded message';
const homeFolks = () => { const HC = homeBaked()[0]; return HC ? Object.values(HC).map(x => x.name) : []; };   // for section 19's "From home" heading
function homeMailOf(m) {                                 // the contact whose recorded message a Mail is (Mail keeps no extra fields: by sender and subject), else null
  if (!m) return null; const HC = homeBaked()[0]; if (!HC) return null;
  if (m.play) { const hm = /^home:(.+)$/.exec(String(m.play)); return hm && HC[hm[1]] ? hm[1] : null; }
  return m.subject === HOME_MSG_SUBJECT ? Object.keys(HC).find(k => HC[k].name === m.from) || null : null;
}
const mailPlayable = m => { const k = homeMailOf(m), c = k && homePeekC(k); return !!(c && c.msg && !c.msg.done) || !!(m && m.play && !homeMailOf(m)); };   // section 19 shows Play while it's true
function mailPlay(m) {
  const k = homeMailOf(m); if (k) return homeMessage(k);
  return m && m.play && typeof momentShow === 'function' ? momentShow(m.play) : false;
}
function homeMessage(k, t = shipNow()) {                 // their message, one-sided; heard to the end, it's done
  if (typeof MEETING_SCRIPTS === 'undefined' || typeof dialogueShow !== 'function' || (typeof DIALOGUE !== 'undefined' && DIALOGUE)) return false;
  const [HC, , , HCH] = homeBaked(), hc = HC && HC[k], c = hc && homePeekC(k), e = c && c.msg && !c.msg.done && HCH && HCH[k] && HCH[k][c.msg.i]; if (!e) return false;
  const hp = homeP(hc), ctx = homeCtx(t), say = x => ({ who: hc.name, text: homeFill(x.text, hp, ctx) ?? String(x.text), pose: x.pose });
  MEETING_SCRIPTS['home:msg:' + k] = { title: hc.name + ', recorded', lines: e.lines.filter(l => l.text).map(say),
    onEnd: f => { delete MEETING_SCRIPTS['home:msg:' + k]; if (!f) return; const C = homeC(k), m = C.msg; if (m) m.done = true;
      const g = homeTag(e); C.h = (C.h || []).filter(x => x !== g).concat(g).slice(-HOME_HEARD);
      if (typeof simNote === 'function') simNote('homeCall', { contact: k, who: hc.id, beat: null, tone: 'message', via: 'message', live: false, flavour: null }); } };
  return dialogueShow('home:msg:' + k, { id: 'home:msg:' + k, who: [], at: t, where: { any: true } });
}
// ---- end of 20c ----

