const LINE_TIER = [0, 1, 2, 3, 4], LINE_SRC = { own: 300, tpl: 200, bank: 100 };
const LINE_WORDS = { hi: ['Hi'], bye: ['See you'], yes: ['Sure'], thanks: ['Thanks'], wow: ['Wow'], sigh: ['Oh well'] };   // when neither card nor template has one
const LINE_ACTS = { meal: ['breakfast', 'dinner'], free: ['leisure', 'off'], call: ['callhome', 'call'] };   // act: groups (call: section 14's callhome)
const LINE_TIMES = { morning: [360, 720], afternoon: [720, 1020], evening: [1020, 1320], night: [1320, 360] };
const LINE_DAYS = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'];
const LINE_PLACES = { mess: 'mess hall', commons: 'junior common room', lounge: 'bow lounge', booths: 'call-home booths', overlook: 'engine overlook',
  teacorner: 'tea corner', worksbay: 'works bay', chartroom: 'chart room', musicroom: 'music room' };   // place: aliases for rooms with spaces
const LINE_RANKS = ['junior', 'officer', 'senior', 'chief', 'xo', 'captain'];
const LINE_REP = ['new', 'known', 'well', 'theirs'], LINE_SHIP = ['low', 'ok', 'high'];   // rep: and ship.*: bands, lowest first
const LINE_RECENT = [];                                   // [{ id, who, h }] the last lines said (not saved)
// section 20's and 13's queries by name, each typeof-guarded (they're consts, so not on window; a missing one gives undefined)
function lineQ(name, ...a) {
  let f = null;
  try {                                                   // one name at a time, so a missing (or not yet loaded) one can't blank the others
    switch (name) {
      case 'relTier': f = typeof relTier === 'function' && relTier; break;
      case 'mem': f = typeof mem === 'function' && mem; break;
      case 'memTold': f = typeof memTold === 'function' && memTold; break;
      case 'memThing': f = typeof memThing === 'function' && memThing; break;
      case 'warmth': f = typeof warmth === 'function' && warmth; break;
      case 'affBand': f = typeof affBand === 'function' && affBand; break;
      case 'bondOf': f = typeof bondOf === 'function' && bondOf; break;
      case 'moodOf': f = typeof moodOf === 'function' && moodOf; break;
      case 'beatOf': f = typeof beatOf === 'function' && beatOf; break;
      case 'knowsNews': f = typeof knowsNews === 'function' && knowsNews; break;
      case 'repBand': f = typeof repBand === 'function' && repBand; break;
      case 'repShip': f = typeof repShip === 'function' && repShip; break;
      case 'knownFor': f = typeof knownFor === 'function' && knownFor; break;
      case 'cue': f = typeof cue === 'function' && cue; break;
      case 'flag': f = typeof flag === 'function' && flag; break;
      case 'inWeek1': f = typeof inWeek1 === 'function' && inWeek1; break;
      case 'leavingSoon': f = typeof leavingSoon === 'function' && leavingSoon; break;
      case 'newHere': f = typeof newHere === 'function' && newHere; break;
      case 'movedOff': f = typeof movedOff === 'function' && movedOff; break;
      case 'socialFill': f = typeof socialFill === 'function' && socialFill; break;
      case 'season': f = typeof season === 'function' && season; break;
      case 'eventNow': f = typeof eventNow === 'function' && eventNow; break;
      case 'habitsOn': f = typeof habitsOn === 'function' && habitsOn; break;
    }
    if (f && name === 'cue') {                            // the same answer while the clock and the cue list stand still (0.43.26): one line pick asks it hundreds of times
      const now = shipNow(), arr = typeof SHIP !== 'undefined' && SHIP.social ? SHIP.social.cues : null;   // the list itself: section 20 replaces it on every new cue (0.43.28)
      if (LINE_CUE.now !== now || LINE_CUE.arr !== arr) { LINE_CUE.now = now; LINE_CUE.arr = arr; LINE_CUE.m.clear(); }
      if (!LINE_CUE.m.has(a[0])) LINE_CUE.m.set(a[0], f(...a));
      return LINE_CUE.m.get(a[0]);
    }
    return f ? f(...a) : undefined;
  } catch (e) { return undefined; }
}
const LINE_CUE = { now: null, arr: null, m: new Map() };   // in practice the answers last a frame (the clock moves every frame)
function linesWho(who) {
  if (who && typeof who === 'object') return who;
  if (typeof ROSTER === 'undefined') return null;
  return ROSTER.find(p => p.id === who) || (typeof ROSTER_GUESTS !== 'undefined' && ROSTER_GUESTS.find(p => p.id === who))
    || (typeof GUESTS !== 'undefined' && Array.isArray(GUESTS) && GUESTS.find(p => p.id === who)) || null;   // event guests and visitors too
}
const linesName = p => p ? (typeof shortName === 'function' ? shortName(p) : p.name.split(' ')[0]) : null;
const linesMe = () => (typeof ROSTER_PLAYER !== 'undefined' && ROSTER_PLAYER.first) || 'cadet';
// one condition: key, wanted value (a string, 'a|b' for either), the speaker, ctx -> true / false
function lineCond(k, v, p, ctx) {
  const t = ctx.t, any = (x, f) => { const s = String(x); return s.indexOf('|') < 0 ? f(s) : s.split('|').some(f); }, id = p.id;
  switch (k) {
    case 'mem': return any(v, x => lineQ('mem', id, x) != null);
    case 'told': return any(v, x => { const m = lineQ('mem', id, x); return m != null && !m.told; });
    case 'warmth': return any(v, x => lineQ('warmth', id) === x);
    case 'aff': return any(v, x => { const i = x.lastIndexOf(':'); if (i > 0) return lineQ('affBand', id, x.slice(0, i)) === x.slice(i + 1); return !!ctx.other && lineQ('affBand', id, ctx.other.id || ctx.other) === x; });   // aff:band (with ctx.other) or aff:<crewId>:band
    case 'bond': return any(v, x => lineQ('bondOf', id, x) != null);
    case 'mood': return any(v, x => lineQ('moodOf', p) === x);
    case 'beat': return any(v, x => { const i = x.lastIndexOf('.'); return (lineQ('beatOf', x.slice(0, i)) || 0) >= +x.slice(i + 1); });   // at least n told
    case 'beatIs': return any(v, x => { const i = x.lastIndexOf('.'); return (lineQ('beatOf', x.slice(0, i)) || 0) === +x.slice(i + 1); });   // beat=arc.n: exactly n told
    case 'news': return any(v, x => !!lineQ('knowsNews', p, x));
    case 'rep': return any(v, x => LINE_REP.indexOf(lineQ('repBand', p.dept)) >= LINE_REP.indexOf(x));   // this band or better (!rep:well = below well)
    case 'ship.work': case 'ship.kindness': case 'ship.spirit': return any(v, x => LINE_SHIP.indexOf(lineQ('repShip', k.slice(5))) >= LINE_SHIP.indexOf(x));   // this or better
    case 'you': return any(v, x => (lineQ('knownFor') || []).includes(x.replace(/_/g, ' ')));   // you:night_owl: _ for a space
    case 'cue': return any(v, x => { const [k, at] = x.split('@'), c = lineQ('cue', k); return !!c && (!at || (at === 'me' ? c.who === id : at === 'dept' ? c.dept === p.dept : false)); });   // cue:gift.you@me: about the speaker; @dept: their department's
    case 'flag': return any(v, x => ctx.flags && x in ctx.flags ? !!ctx.flags[x] : !!lineQ('flag', x));   // ctx.flags: { key: true } answers for those keys (onboarding asks for a step's lines)
    case 'week1': { const on = !!lineQ('inWeek1'); return any(v, x => (x === 'true') === on); }
    case 'leaving': return any(v, x => x === 'soon' ? !!lineQ('leavingSoon', id) : x === 'you' ? !!ctx.goodbye : false);
    case 'newhere': return any(v, x => (x === 'true') === !!lineQ('newHere', id));
    case 'moved': return any(v, x => !!lineQ('movedOff', x));
    case 'guide': return any(v, x => (x === 'true') === !!lineQ('flag', 'guide.active'));
    case 'time': { const m = ((t % 1440) + 1440) % 1440; return any(v, x => { const r = LINE_TIMES[x]; return !!r && (r[0] < r[1] ? m >= r[0] && m < r[1] : m >= r[0] || m < r[1]); }); }
    case 'weekday': return any(v, x => LINE_DAYS[weekday(Math.floor(t / 1440) + 1)] === x);
    case 'season': return any(v, x => lineQ('season', Math.floor(t / 1440) + 1) === x);
    case 'place': return any(v, x => { if (x === 'calm') return !!ctx.place && typeof CALM_TYPES !== 'undefined' && [].concat(CALM_TYPES.has ? [...CALM_TYPES] : CALM_TYPES).includes(ctx.place);   // calm: section 20's CALM_TYPES
      const r = (LINE_PLACES[x] || x.replace(/_/g, ' ')).toLowerCase(); return ctx.place === x || (ctx.room || '').toLowerCase().replace(/^the /, '') === r; });   // a room: its name with _ for spaces, or a short alias
    case 'deck': { const d = ctx.deck != null ? ctx.deck : typeof deckDef !== 'undefined' && deckDef ? deckDef.num : null; return any(v, x => String(d) === x); }   // the scene's deck (where you are), not the speaker's home deck
    case 'event': return any(v, x => { const [ev, ph] = x.split('.'), n = lineQ('eventNow', t); return !!n && n.id === ev && (!ph || n.phase === ph); });
    case 'trad': return any(v, x => ctx.trad === x || ctx.tradId === x || (x === 'today' && !!ctx.trad));   // ctx.tradId: the id when ctx.trad is the name (0.28.50)
    case 'gift': return any(v, x => ctx.how === x || ctx.tag === x);
    case 'came': return any(v, x => !!ctx.trad && (x === 'any' || ctx.trad === x || ctx.tradId === x));   // you went to a tradition lately (the caller passes ctx.trad)
    case 'friend': return any(v, x => !!ctx.friend && (x === 'any' || ctx.friendId === x));   // you have a friend aboard (ctx.friend: their name)   // the gift being thanked: how it landed (loved|liked|polite, ctx.how) or its tag (ctx.tag)
    case 'who': return any(v, x => id === x);   // the speaker is this crew member (overheard: speaker A)
    case 'with': { const o = ctx.other && (ctx.other.id || ctx.other); return !!o && any(v, x => o === x); }   // the other person in the scene
    case 'dept': return any(v, x => p.dept === x);
    case 'rank': return any(v, x => p.rank === x);
    case 'trait': return any(v, x => (p.traits || []).includes(x.replace(/_/g, ' ')));   // trait:dry_humour
    case 'habit': { const hs = lineQ('habitsOn', p, Math.floor(t / 1440) + 1) || p.habits || []; return any(v, x => hs.includes(x)); }   // today's habits (habit shifts too)
    case 'act': return any(v, x => (LINE_ACTS[x] || [x]).includes(ctx.act));
    case 'birthday': return any(v, x => x === 'me' ? !!(typeof isBirthday === 'function' && isBirthday(p, t)) : x === 'you' ? !!(typeof isBirthday === 'function' && typeof ROSTER_PLAYER !== 'undefined' && isBirthday(ROSTER_PLAYER, t)) : false);
    case 'topic': return !ctx.topic || any(v, x => ctx.topic === x);
    case 'pair': return linePair(v, p, ctx.other && linesWho(ctx.other));
  }
  return false;
}
// pair:x+y (x for speaker A, y for B: a department, a rank, a crew id, or 'any') or pair:same|bunk|friend|rival|senior|couple|best|mentor|mentee
function linePair(v, a, b) {
  if (!b) return false;
  return String(v).split('|').some(x => {
    if (x === 'same') return a.dept === b.dept;
    if (x === 'bunk') return !!a.bed && !!b.bed && a.bed.split('-').slice(0, 2).join('-') === b.bed.split('-').slice(0, 2).join('-');
    if (x === 'friend' || x === 'rival') return lineQ('affBand', a.id, b.id) === x;
    if (x === 'couple') return lineQ('bondOf', a.id, 'couple') === b.id;   // a couple living quietly in the background
    if (x === 'best') return lineQ('bondOf', a.id, 'best') === b.id;       // best friends (0.43.27, social B2's goodbyes)
    if (x === 'mentor') return lineQ('bondOf', a.id, 'mentor') === b.id;   // B is A's mentor (0.43.29: one way, as the writers' goodbyes read)
    if (x === 'mentee') return lineQ('bondOf', a.id, 'mentee') === b.id;   // B is A's mentee
    if (x === 'senior') return LINE_RANKS.indexOf(a.rank) > LINE_RANKS.indexOf(b.rank);
    const [s, o] = x.split('+'), side = (q, w) => !w || w === 'any' || q.dept === w || q.rank === w || q.id === w;   // a department, a rank or a crew id
    return side(a, s) && side(b, o);
  });
}
const LINE_META = new Set(['text', 'id', 'tone', 'w', 'odds', 'not', 'old', 'lines', 'flavour', 'reply', 'sets', 'memo']);   // data, not conditions
// the cheap conditions first (0.43.26, the performance pass): who, with, act, time, deck, weekday and place need no
// social query (and cue's answers are kept while the clock and the cue list stand still), so a line failing one is dropped before linesOk asks section 20 anything. The same answer as linesOk
// alone (all conditions must hold either way), only sooner
const LINE_FAST = new Set(['who', 'with', 'act', 'time', 'deck', 'weekday', 'place', 'cue']);   // cue: lineQ keeps its answers while the clock stands still
function lineQuick(e, p, ctx) {
  for (const k in e) if (LINE_FAST.has(k)) { const v = e[k]; if (Array.isArray(v) ? !v.every(x => lineCond(k, x, p, ctx)) : !lineCond(k, v, p, ctx)) return false; }
  return true;
}
function linesOk(e, p, ctx) {
  for (const k in e) {
    if (LINE_META.has(k)) continue;
    if (k === 'tier') { const r = lineQ('relTier', p.id) || 0; if (r < e.tier[0] || r > e.tier[1]) return false; continue; }
    const vs = Array.isArray(e[k]) ? e[k] : [e[k]];
    if (!vs.every(v => lineCond(k, v, p, ctx))) return false;
  }
  if (e.not) for (const k in e.not) {
    if (k === 'tier') { const r = lineQ('relTier', p.id) || 0; if (r >= e.not.tier[0] && r <= e.not.tier[1]) return false; continue; }
    const vs = Array.isArray(e.not[k]) ? e.not[k] : [e.not[k]];
    if (vs.some(v => lineCond(k, v, p, ctx))) return false;
  }
  if (e.odds != null && schedU(p.seed || 0, Math.floor(ctx.t / 60), 770 + (lineHash(e.id) % 28)) >= e.odds) return false;
  return true;
}
const lineHash = s => { let h = 0; for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) >>> 0; return h; };
const lineSpec = e => Object.keys(e).filter(k => !LINE_META.has(k)).length + (e.not ? Object.keys(e.not).length : 0) + (e.tier ? (4 - e.tier[1] + e.tier[0]) / 10 : 0);   // a narrower tier is a little more specific
// a voice token from the speaker's card, else their template's, else the plain word; picked by person and hour
function lineWord(p, tok, h, i) {
  const v = typeof VOICE !== 'undefined' && VOICE[p.id], tp = v && typeof VOICE_TEMPLATES !== 'undefined' && VOICE_TEMPLATES[v.tpl || p.tpl];
  if (tok === 'nick') { const n = (v && v.words && v.words.nick) || (tp && tp.words && tp.words.nick), x = n && n[lineQ('relTier', p.id) || 0]; return x || '{me}'; }
  const a = (v && v.words && v.words[tok]) || (tp && tp.words && tp.words[tok]) || LINE_WORDS[tok];
  return a[Math.floor(schedU(p.seed || 0, h, 760 + i % 10) * a.length)];
}
// fill a line for speaker p: voice tokens, then placeholders. null when a placeholder can't be filled
function linesFill(text, p, ctx = {}) {
  const t = ctx.t != null ? ctx.t : shipNow(), h = Math.floor(t / 60);
  const cap = (x, off, str) => x && (off === 0 || /[.!?]\s+$/.test(str.slice(0, off))) ? x[0].toUpperCase() + x.slice(1) : x;   // a word filled in at a sentence's start gets a capital
  let i = 0, s = text.replace(/\{(hi|bye|yes|thanks|wow|sigh|nick)\}/g, (m, k, off, str) => { const f = k === 'nick' && lineQ('socialFill', p, 'nick', ctx); const x = f || lineWord(p, k, h, i++); return x === '{me}' ? x : cap(x, off, str); });
  const bond = k => { const id = lineQ('bondOf', p.id, k); return id ? linesName(linesWho(id)) : null; };
  const chief = () => typeof ROSTER !== 'undefined' && ROSTER.find(q => q.dept === p.dept && q.rank === 'chief' && q !== p);
  const LINE_ROSTER_FILL = ['kin', 'lost', 'hobbyNoun'];   // ready to drop into a line, from the roster (crew designer 3)
  const SOCIAL_FILL = ['me', 'partner', 'friend', 'best', 'rival', 'mentor', 'mentee', 'boss', 'thing', 'trad', 'home', 'family', 'hobby', 'since'];   // section 20's socialFill fills these when it's there ({since} grows with the game: social 0.36.60)
  const val = k => {
    if (ctx[k] != null && typeof ctx[k] !== 'object') return String(ctx[k]);
    if (SOCIAL_FILL.includes(k) && typeof socialFill === 'function') { const x = lineQ('socialFill', p, k, ctx); return x == null ? null : String(x); }
    if (LINE_ROSTER_FILL.includes(k) && typeof socialFill === 'function') { const x = lineQ('socialFill', p, k, ctx); if (x != null) return String(x); }   // social's answer if it has one, else the roster's own
    switch (k) {
      case 'me': return linesMe();
      case 'name': return linesName(p);
      case 'first': { const w = p.name.split(' '); return /^(Captain|Commander|Dr\.|Chief|Chef|Lt\.?|Lieutenant|Ensign)$/.test(w[0]) && w.length > 2 ? w[1] : w[0]; }
      case 'friend': case 'best': case 'rival': case 'partner': case 'mentor': case 'mentee': return bond(k === 'partner' ? 'couple' : k);
      case 'boss': { const c = chief(); return c ? linesName(c) : null; }
      case 'missed': return bond('missed');                // the close friend, partner or mentor who moved on (section 20c's bondOf, 0.39.14)
      case 'other': return ctx.other ? linesName(linesWho(ctx.other)) : null;
      case 'weekday': return WEEKDAYS[weekday(Math.floor(t / 1440) + 1)];
      case 'home': case 'family': case 'hobby': case 'since': return p[k] ? String(p[k]) : null;
      case 'kin': case 'lost': case 'hobbyNoun': return typeof p[k] === 'string' && p[k] ? p[k] : null;   // the roster's line-ready forms (0.43.24: "my gran", "my wife", "the piano")
      case 'thing': { const k = ctx.mem; return k ? lineQ('memThing', k) || null : null; }   // from the memory the line matched (mem: or told:)
    }
    return null;
  };
  let ok = true;
  for (let n = 0; n < 2 && ok; n++) s = s.replace(/\{([a-zA-Z]+)\}/g, (m, k, off, str) => { const x = val(k); if (x == null) ok = false; return x == null ? m : cap(x, off, str); });   // twice: {nick} can give {me}
  return ok ? s : null;
}
function lineFor(who, kind, ctx = {}) {
  const p = linesWho(who); if (!p || typeof LINES === 'undefined') return null;
  const t = ctx.t != null ? ctx.t : shipNow(), h = Math.floor(t / 60), c = { ...ctx, t };
  const v = VOICE[p.id], tp = VOICE_TEMPLATES[(v && v.tpl) || p.tpl];
  const pool = [];
  for (const [src, list] of [['own', v && v.lines && v.lines[kind]], ['tpl', tp && tp.lines && tp.lines[kind]], ['bank', LINES[kind]]])
    for (const e of list || []) if ((!ctx.keep || ctx.keep(e)) && lineQuick(e, p, c) && linesOk(e, p, c)) pool.push({ e, sc: LINE_SRC[src] + 10 * lineSpec(e) });
  if (!pool.length) return null;
  const mine = LINE_RECENT.filter(r => r.who === p.id).slice(-6), all = LINE_RECENT.slice(-12);
  for (const x of pool) {
    if (mine.some(r => r.id === x.e.id && r.h !== h)) x.sc -= 15;
    if (all.some(r => r.id === x.e.id && r.who !== p.id)) x.sc -= 8;
  }
  pool.sort((x, y) => y.sc - x.sc);                       // stable: the pool's order within a score
  let best = [];
  for (let i = 0; i < pool.length && !best.length;) {     // fill only the top-scoring lines, the next score down if none of them fill (0.43.26)
    const top = pool[i].sc;
    for (; i < pool.length && pool[i].sc === top; i++) {
      const x = pool[i], mk = [].concat(x.e.told || x.e.mem || [])[0];
      x.text = linesFill(x.e.text, p, mk && !c.mem ? { ...c, mem: mk } : c);
      if (x.text != null) best.push(x);
    }
  }
  if (!best.length) return null;
  const sum = best.reduce((s, x) => s + (x.e.w || 1), 0);
  let r = schedU(p.seed || 0, h, 750) * sum, pick = best[best.length - 1];
  for (const x of best) { r -= x.e.w || 1; if (r < 0) { pick = x; break; } }
  const e = pick.e;
  if (!ctx.peek) {
    if (!LINE_RECENT.some(x => x.id === e.id && x.who === p.id && x.h === h)) { LINE_RECENT.push({ id: e.id, who: p.id, h }); if (LINE_RECENT.length > 40) LINE_RECENT.shift(); }
    for (const k of [].concat(e.told || [])) lineQ('memTold', p.id, k);
  }
  const out = { text: pick.text, id: e.id, kind, tone: e.tone || 'light' }; if (e.cue) out.cue = e.cue;   // a reaction's cue: [its kind, ...]
  return out;
}
// a conversation between two crew: CONVOS whose pair and conditions hold (read for speaker A, with B as ctx.other),
// picked by the pair and hour (schedU k 751). Wave 2 plays them as alternating bubbles and keeps the saved ring.
function overheardFor(a, b, ctx = {}) {
  a = linesWho(a); if (b) { b = linesWho(b); if (!b) return null; } if (!a || typeof CONVOS === 'undefined') return null;   // no b: one speaker's lines (only A:, a call home)
  const t = ctx.t != null ? ctx.t : shipNow(), h = Math.floor(t / 60), ca = { ...ctx, t, other: b }, cb = { ...ctx, t, other: a };
  const skip = new Set(ctx.skip || []);
  const pool = CONVOS.filter(e => !skip.has(e.id) && (!ctx.keep || ctx.keep(e)) && !(ctx.noSerious && e.tone === 'serious') && !b === e.lines.every(l => l.who === 'A') && lineQuick(e, a, ca) && linesOk(e, a, ca))
    .map(e => ({ e, sc: lineSpec(e) })).sort((x, y) => y.sc - x.sc);   // stable: file order within a score
  let best = [];
  for (let i = 0; i < pool.length && !best.length;) {     // fill only the most specific ones, the next score down if none of them fill
    const top = pool[i].sc;
    for (; i < pool.length && pool[i].sc === top; i++) {
      const e = pool[i].e, lines = e.lines.map(l => ({ who: l.who === 'B' ? b.id : a.id, text: linesFill(l.text, l.who === 'B' ? b : a, l.who === 'B' ? cb : ca) }));
      if (lines.every(l => l.text != null)) best.push({ e, lines });
    }
  }
  if (!best.length) return null;
  const x = best[Math.floor(schedU((a.seed || 0) ^ (b ? b.seed || 0 : 0), h, 751) * best.length)];
  return Object.assign(x.lines, { id: x.e.id, tone: x.e.tone || 'light' });   // the lines, with the conversation's id and tone
}
// ---- overheard conversations, played (0.43.12). linesTick() runs every frame (section 20's socialTick calls it).
// Once a ship minute, now and then (OVH_ODDS, schedU k 752), two crew awake and in place within OVH_PAIR tiles of each
// other, both within section 20's CHATTER_NEAR of you and well on screen, talk: overheardFor's lines as alternating
// speech bubbles (section 8b's bubbleSay), one every OVH_STEP real seconds. Pairs are tried in a seeded order (k 753).
// The voice budget: one conversation at a time; none starts while a bubble shows or within section 20's chatter gap
// (CHATTER_AT, which each line here sets too, so the chatter waits until the conversation is over); none while a chat
// card (CHAT), a meeting (DIALOGUE) or sleep is on, and one playing stops (its bubbles go) when one opens or a speaker
// walks off; at most one #serious conversation a ship day. Failing a pair, one of them can say a one-speaker
// conversation (only A: lines, e.g. on a call home in the booths). Kept cheap: odds first, at most OVH_NEAR people
// (in the seeded order) and OVH_TRIES pairs or singles a ship minute; overheardFor fills only its top-scoring group. The saved ring (SHIP.lines, in the save as save.lines): a
// conversation you've heard isn't played again within LINES_RING_DAYS ship days.
const OVH_ODDS = .3, OVH_GAP = 20, OVH_STEP = 3.2, OVH_PAIR = 2.5, OVH_NEAR = 6, OVH_TRIES = 8, LINES_RING_DAYS = 7, LINES_RING_MAX = 300;
let OVH = null, OVH_MIN = -1, OVH_AT = -1e9;              // OVH: the conversation playing { a, b, lines, i, next, bub }
function linesState() {                                   // SHIP.lines = { ring: [[id, day], ...], serious: the day of the last #serious }
  if (typeof SHIP === 'undefined') return null;
  if (!SHIP.lines) {
    const s = typeof SAVED !== 'undefined' && SAVED && SAVED.lines;
    const ok = s && Array.isArray(s.ring) && s.ring.every(r => Array.isArray(r) && typeof r[0] === 'string' && Number.isInteger(r[1]));
    SHIP.lines = { ring: ok ? s.ring.slice(-LINES_RING_MAX) : [], serious: ok && Number.isInteger(s.serious) ? s.serious : 0, reacted: {}, bye: {} };
    const by = ok && s.bye && typeof s.bye === 'object' ? s.bye : {};   // { 'a:b': day }: goodbyes said
    for (const k in by) if (Number.isInteger(by[k])) SHIP.lines.bye[k] = by[k];
    const r = ok && s.reacted && typeof s.reacted === 'object' ? s.reacted : {};   // { crewId: { day, kinds: [...] } }
    for (const id in r) if (r[id] && Number.isInteger(r[id].day) && Array.isArray(r[id].kinds)) SHIP.lines.reacted[id] = { day: r[id].day, kinds: r[id].kinds.filter(k => typeof k === 'string') };
  }
  return SHIP.lines;
}
if (typeof SAVE_EXTRA !== 'undefined') SAVE_EXTRA.push(s => {
  const L = SHIP.lines; if (!L) return;
  const day = Math.floor(shipNow() / 1440) + 1, reacted = {};
  for (const id in L.reacted || {}) if (L.reacted[id].day === day) reacted[id] = L.reacted[id];   // only today's count
  s.lines = { ring: L.ring.slice(-LINES_RING_MAX), serious: L.serious, reacted, bye: L.bye || {} };
});
function linesNew() { if (typeof SHIP !== 'undefined') SHIP.lines = { ring: [], serious: 0, reacted: {}, bye: {} }; OVH = null; OVH_SCAN = null; OVH_AT = -1e9; REACT_AT = -1e9; LINE_RECENT.length = 0; }   // a new game (section 13's simNote('newGame'))
// the ids heard within the ring's days (an entry from a later day than today is from an earlier game: it doesn't count)
function linesRing(day) { const L = linesState(); return L ? L.ring.filter(r => r[1] <= day && day - r[1] < LINES_RING_DAYS).map(r => r[0]) : []; }
function linesHeard(id, day, tone) {
  const L = linesState(); if (!L) return;
  L.ring.push([id, day]); if (L.ring.length > LINES_RING_MAX) L.ring.shift();
  if (tone === 'serious') L.serious = day;
}
const linesHush = () => (typeof CHAT !== 'undefined' && !!CHAT) || (typeof DIALOGUE !== 'undefined' && !!DIALOGUE) || (typeof sleeping !== 'undefined' && sleeping);
// the minute's tries (goodbyes, reactions, then conversations) are worked in the minute's own frame, before section 20's
// chatter rolls (0.43.28, reviewer 2b: 0.43.26 spread them over frames, so the chatter could speak in between and a
// conversation was lost). Each try is about half the cost it was (0.43.26), and performance engineer 2 found section 22
// in none of the slow frames. OVH_SCAN stays the queue's shape; OVH_PER_FRAME = Infinity works it all at once
const OVH_PER_FRAME = Infinity;
let OVH_SCAN = null;                                      // { t, day, tries: [{ x, y, ctx } | { x, react: true }], i }
function linesTick() {
  if (OVH) { linesTalk(); return; }
  if (OVH_SCAN) { linesScan(); return; }
  const m = Math.floor(shipNow()); if (m === OVH_MIN) return; OVH_MIN = m;
  if (typeof bubbleSay !== 'function' || typeof bubbles === 'undefined' || typeof DECK_CREW === 'undefined') return;
  const t = shipNow(), ovh = typeof CONVOS !== 'undefined' && CONVOS.length > 0 && schedU(m, 0, 752) < OVH_ODDS;
  const react = typeof LINES !== 'undefined' && !!LINES.cue && LINES.cue.length > 0 && (t - REACT_AT < REACT_FRESH || schedU(m, 0, 754) < REACT_ODDS);
  const now = simNow(), gap = typeof CHATTER_AT !== 'undefined' ? now - CHATTER_AT < CHATTER_GAP * 1000 : false;
  const byes = typeof CONVOS !== 'undefined' && CONVOS.some(e => e.leaving);   // goodbye conversations exist (leaving:soon)
  if (!(ovh || react || byes) || now - OVH_AT < OVH_GAP * 1000 || gap || bubbles.list.length || linesHush()) return;
  const day = Math.floor(t / 1440) + 1, P = player.obj.position, v = new THREE.Vector3();
  const onScreen = a => { v.set(a.x, (a.y || 0) + 1.6, a.z).project(camera); return Math.abs(v.x) < .7 && v.y < .8 && v.y > -.9; };   // as section 20's chatter
  const around = DECK_CREW.filter(a => a.h && a.p && !a.p.player && Math.hypot(a.x - P.x, a.z - P.z) <= (typeof CHATTER_NEAR !== 'undefined' ? CHATTER_NEAR : 7) && onScreen(a))
    .map(a => ({ a, w: whereIs(a.p, t) })).filter(x => x.w && !x.w.moving && x.w.act !== 'sleep' && x.w.act !== 'wash')
    .sort((x, y) => schedU(x.a.p.seed, m, 753) - schedU(y.a.p.seed, m, 753));
  const near = around.slice(0, OVH_NEAR);                 // the first OVH_NEAR in the seeded order; goodbyes look at everyone around
  // goodbyes first (0.43.27, social B2): someone leaving soon (section 20's leavingSoon) with someone close by gets their
  // goodbye conversation (one with leaving:), whatever the odds, once per pair (SHIP.lines.bye, saved)
  const tries = [], Lb = linesState(), bye = Lb && (Lb.bye || (Lb.bye = {}));
  if (byes && bye) for (const x of around) {
    if (lineQ('leavingSoon', x.a.p.id) == null) continue;
    const r = typeof roomAt === 'function' ? roomAt(...x.a.here()) : null;
    for (const y of around) {
      if (y === x || x.w.act === 'callhome' || y.w.act === 'callhome' || Math.hypot(x.a.x - y.a.x, x.a.z - y.a.z) > OVH_PAIR || bye[linesPairKey(x.a.p, y.a.p)]) continue;
      tries.push({ x, y, bye: true, ctx: { t, act: x.w.act, place: x.w.type, room: r && ROOMS[r] ? ROOMS[r].name : '', deck: deckDef.num, keep: e => !!e.leaving, skip: linesRing(day), noSerious: Lb.serious === day } });
    }
  }
  if (react) tries.push(...near.map(x => ({ x, react: true })));
  if (ovh) {
    const L = linesState(), skip = linesRing(day), noSerious = L && L.serious === day, call = w => w.act === 'callhome';   // someone on a call home talks to home, not to the next booth
    let n = OVH_TRIES;
    for (const x of near) {
      if (n <= 0) break;
      const r = typeof roomAt === 'function' ? roomAt(...x.a.here()) : null;
      const ctx = { t, act: x.w.act, place: x.w.type, room: r && ROOMS[r] ? ROOMS[r].name : '', deck: deckDef.num, skip, noSerious };
      for (const y of near.filter(y => y !== x && !call(x.w) && !call(y.w) && Math.hypot(x.a.x - y.a.x, x.a.z - y.a.z) <= OVH_PAIR).concat(null)) {   // with each one close by, then alone
        if (n-- <= 0) break;
        tries.push({ x, y, ctx });
      }
    }
  }
  if (tries.length) { OVH_SCAN = { t, day, tries, i: 0 }; linesScan(); }
}
const linesPairKey = (a, b) => [a.id, b.id].sort().join(':');   // one goodbye a pair, whoever starts it
function linesScan() {
  const S = OVH_SCAN;
  if (linesHush() || bubbles.list.length) { OVH_SCAN = null; return; }   // the budget says no (someone else spoke meanwhile)
  for (let k = 0; k < OVH_PER_FRAME && S.i < S.tries.length; k++) {
    const q = S.tries[S.i++];
    if (q.react) { if (linesReact([q.x], S.t, S.day)) { OVH_SCAN = null; return; } continue; }
    const lines = overheardFor(q.x.a.p, q.y && q.y.a.p, q.ctx); if (!lines) continue;
    OVH_SCAN = null; linesHeard(lines.id, S.day, lines.tone);
    OVH = { a: q.x.a, b: q.y && q.y.a, lines, i: 0, next: 0, bub: [], bye: q.bye ? linesPairKey(q.x.a.p, q.y.a.p) : null, day: S.day }; linesTalk(); return;
  }
  if (S.i >= S.tries.length) OVH_SCAN = null;
}
// the conversation playing: the next line when it's due; it ends after the last, or stops when the budget says hush
function linesTalk() {
  const o = OVH, now = simNow();
  const gone = s => !DECK_CREW.includes(s) || !s.h, apart = !!o.b && Math.hypot(o.a.x - o.b.x, o.a.z - o.b.z) > OVH_PAIR + 1.5;
  if (linesHush() || gone(o.a) || (o.b && gone(o.b)) || apart) { for (const b of o.bub) { b.el.remove(); const k = bubbles.list.indexOf(b); if (k >= 0) bubbles.list.splice(k, 1); } OVH = null; OVH_AT = now; return; }
  if (now < o.next) return;
  if (o.i >= o.lines.length) {                            // said to the end: a goodbye is marked only now (0.43.29), so one cut short can come again
    if (o.bye) { const L = linesState(); if (L) (L.bye || (L.bye = {}))[o.bye] = o.day; }
    OVH = null; OVH_AT = now; return;
  }
  const l = o.lines[o.i++], s = o.b && l.who === o.b.p.id ? o.b : o.a;
  const b = bubbleSay(s.h, l.text, OVH_STEP + .8); if (b) o.bub.push(b);
  o.next = now + OVH_STEP * 1000;
  if (typeof CHATTER_AT !== 'undefined') CHATTER_AT = now;   // section 20's chatter waits while two are talking
}
// ---- reactions (0.43.16): someone near you says a line about something that really happened: the reaction bank
// (LINES.cue, content/reactions/*.lines), whose cue: conditions read section 20's cues, which social makes from section
// 13's ship notes. linesTick tries one before an overheard conversation: within REACT_FRESH ship minutes of a note
// (onSim('*'): a kind social makes a cue of, SOC_CUE_OF), else now and then while the cue lasts (REACT_ODDS a ship
// minute, schedU k 754); someone awake and in place near you and on screen, in linesTick's seeded order; one bubble,
// under the same voice budget. Each person reacts to a kind (a reaction line's first cue: repair, gift,
// event.ionStorm...) at most once a ship day (SHIP.lines.reacted, saved with today's only), and a line you've heard
// goes in the ring like a conversation (not again within 7 ship days); #serious ones count towards the day's one.
const REACT_ODDS = .2, REACT_FRESH = 30, REACT_SECS = 4.5;
let REACT_AT = -1e9;                                      // the ship minute of the last note worth reacting to
if (typeof onSim === 'function') onSim('newGame', () => linesNew());   // section 13's New game: nothing heard yet
if (typeof onSim === 'function') onSim('*', n => { if (n && isFinite(n.t) && (typeof SOC_CUE_OF === 'undefined' || SOC_CUE_OF[n.kind])) REACT_AT = Math.max(REACT_AT, n.t); });
const reactKind = e => [].concat(e.cue || [])[0] || null;
function linesReact(near, t, day) {
  const L = linesState(); if (!L) return false;
  const ring = new Set(linesRing(day)), done = L.reacted || (L.reacted = {});
  for (const x of near) {
    const p = x.a.p, mine = done[p.id] && done[p.id].day === day ? done[p.id].kinds : [];
    const keep = e => !ring.has(e.id) && !mine.includes(reactKind(e)) && !(L.serious === day && e.tone === 'serious');
    const r = typeof roomAt === 'function' ? roomAt(...x.a.here()) : null;
    const l = lineFor(p, 'cue', { t, act: x.w.act, place: x.w.type, room: r && ROOMS[r] ? ROOMS[r].name : '', deck: deckDef.num, keep });
    if (!l || !bubbleSay(x.a.h, l.text, REACT_SECS)) continue;
    const k = reactKind(l); done[p.id] = { day, kinds: k ? mine.concat(k) : mine };
    linesHeard(l.id, day, l.tone);
    const now = simNow(); OVH_AT = now; if (typeof CHATTER_AT !== 'undefined') CHATTER_AT = now;
    return true;
  }
  return false;
}
// the baked meetings into MEETING_SCRIPTS (section 18 calls this once, right after declaring it): a text with {me} becomes
// c => text with c.you, the shape section 18's dialogue already plays
function linesMeetings(into) {
  if (typeof MEETINGS_BAKED === 'undefined') return;
  const fix = l => l && typeof l.text === 'string' && l.text.includes('{me}') ? { ...l, text: (s => c => s.replace(/\{me\}/g, c.you))(l.text) } : l;
  for (const id in MEETINGS_BAKED) { const sc = MEETINGS_BAKED[id]; into[id] = { ...sc, lines: sc.lines.map(l => l.choice ? { choice: l.choice.map(ch => ({ ...fix(ch), reply: fix(ch.reply) })) } : fix(l)) }; }
}
// section 20's old lists (0.43.0), in their old shapes, from the lines marked old (content/banks/old.lines), so its
// picking (and cadet_test) stays exactly as it was until it asks lineFor: 'greet' -> [tier 0 lines, ... tier 4];
// 'near' -> [[w => test, lines], ...]; 'life' -> { habit: line }; 'dept' -> { dept: line }; 'smalltalk' -> { act: lines }
function linesLegacy(kind) {
  const old = (LINES[kind === 'dept' ? 'life' : kind] || []).filter(e => e.old);
  if (kind === 'greet') return LINE_TIER.map(n => old.filter(e => e.tier && e.tier[0] <= n && e.tier[1] >= n).map(e => e.text));
  if (kind === 'near') {
    const groups = [];
    for (const e of old) { const g = groups[groups.length - 1]; if (g && g[2] === (e.act || '')) g[1].push(e.text); else groups.push([null, [e.text], e.act || '']); }
    return groups.map(([, a, act]) => [w => !act || act.split('|').includes(w.act), a]);
  }
  const by = kind === 'life' ? 'habit' : kind === 'dept' ? 'dept' : 'act', o = {};
  for (const e of old) if (e[by]) { if (kind === 'smalltalk') (o[e[by]] = o[e[by]] || []).push(e.text); else o[e[by]] = e.text; }
  return o;
}

