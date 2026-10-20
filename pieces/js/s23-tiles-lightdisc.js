// =====================================================================
// 23. TILES
// The Tiles game (plans/tiles-plan.html, approved by the user 2026-10-17): a two-player tile game you play against
// crew at the Tiles station in the bow lounge or a lounge table on Tiles night. Checkers-style moves, block-matching
// scores: STEP diagonally forward, JUMP an opponent's tile into your hold, LAUNCH from your hold onto your home rows;
// three or more of your tiles of one mark touching edge to edge DOCK for a point each. First to 7 (or the quick game
// to 5, with equal turns). The rules and the crew's play are pure functions: nothing here draws on the 3D scene,
// calls R() or Math.random. Crew choices come from schedU keys 800-829:
//   800 a game's seed (tilesRng)  801 Tiles night pairings  802 Tiles night rolls  803-806 a crew member's style
//   (bold, patient, chatty, level)  807 chatter picks  (808-829 free)
// No top-level name TILES here: the deck architect's board kit is TILES_KIT (claude/decks-p3).
// ---- rules (pure: no DOM, no three.js, no Math.random) ----
// Board: 36 cells, i = y*6 + x; y 0 is the player's home row (seat 0, bottom), y 5 the opponent's.
// A tile is o*3 + m + 1 (o: seat 0|1, m: 0 Planet, 1 Ship, 2 Star); 0 is empty.
const TL_N = 6, TL_MARKS = ['Planet', 'Ship', 'Star'], TL_SYM = ['●', '▲', '★'];
const TL_MODES = { full: { target: 7, turns: 14, finish: false }, quick: { target: 5, turns: 12, finish: true } };
const TL_TEACH = [1, 0, 2, 1, 2, 0, 0, 2, 1, 0, 1, 2];   // the teaching layout's marks, rows 1 then 2, a to f
const tlO = t => (t - 1) / 3 | 0, tlM = t => (t - 1) % 3, tlT = (o, m) => o * 3 + m + 1;
function tilesRng(seed) {   // mulberry32: one game's stream of decisions, seeded from schedU
  let a = (seed >>> 0) || 1;
  return () => { a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
}
function tilesGroup(b, i) {   // the touching group of same-owner, same-mark tiles round cell i
  const t = b[i], seen = [i], st = [i];
  while (st.length) {
    const c = st.pop(), x = c % TL_N, y = c / TL_N | 0;
    for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
      const nx = x + dx, ny = y + dy, n = ny * TL_N + nx;
      if (nx >= 0 && nx < TL_N && ny >= 0 && ny < TL_N && b[n] === t && seen.indexOf(n) < 0) { seen.push(n); st.push(n); }
    }
  }
  return seen;
}
function tilesDeal(rng, teach) {   // 12 tiles a side, mirrored; no three of a mark touching at the start
  for (;;) {
    const b = new Array(36).fill(0);
    for (let k = 0; k < 12; k++) {
      const m = teach ? TL_TEACH[k] : (rng() * 3) | 0, x = k % 6, y = k / 6 | 0;
      b[y * 6 + x] = tlT(0, m); b[(5 - y) * 6 + (5 - x)] = tlT(1, m);
    }
    if (teach || !b.some((t, i) => t && tilesGroup(b, i).length >= 3)) return b;
  }
}
function tilesNew(mode, rng, teach, first) {   // first: the seat that moves first (0 unless given)
  const f = first ? 1 : 0;
  return { b: tilesDeal(rng, teach), hold: [[], []], sc: [0, 0], p: f, first: f, plies: 0, last: -1, mode: TL_MODES[mode] ? mode : 'full',
           over: false, win: -1, why: '', reached: -1 };
}
function tilesMoves(s, p) {   // { k: 's'tep | 'j'ump | 'l'aunch, from, to, over, m }
  const out = [], b = s.b, f = p ? -1 : 1;
  for (let i = 0; i < 36; i++) {
    const t = b[i]; if (!t || tlO(t) !== p) continue;
    const x = i % 6, y = i / 6 | 0;
    for (const dx of [-1, 1]) {
      const nx = x + dx, ny = y + f;
      if (nx >= 0 && nx < 6 && ny >= 0 && ny < 6 && !b[ny * 6 + nx]) out.push({ k: 's', from: i, to: ny * 6 + nx });
    }
    for (const [dx, dy] of [[-1, 1], [1, 1], [-1, -1], [1, -1]]) {
      const mx = x + dx, my = y + dy, nx = x + 2 * dx, ny = y + 2 * dy;
      if (nx < 0 || nx > 5 || ny < 0 || ny > 5 || b[ny * 6 + nx]) continue;
      const o = b[my * 6 + mx];
      if (o && tlO(o) !== p) out.push({ k: 'j', from: i, to: ny * 6 + nx, over: my * 6 + mx });
    }
  }
  const h = s.hold[p];
  if (h.length) {
    const rows = p ? [5, 4] : [0, 1], seenM = [];
    for (const m of h) {
      if (seenM.indexOf(m) >= 0) continue; seenM.push(m);
      for (const y of rows) for (let x = 0; x < 6; x++) if (!b[y * 6 + x]) out.push({ k: 'l', m, to: y * 6 + x });
    }
  }
  return out;
}
function tilesCount(s, p) { let n = s.hold[p].length; for (const t of s.b) if (t && tlO(t) === p) n++; return n; }
// apply one move for the side to move; returns { s: new state, take: mark | -1, dock: [cells], pts }
function tilesApply(s, mv) {
  const p = s.p, b = s.b.slice(), hold = [s.hold[0].slice(), s.hold[1].slice()];
  let take = -1;
  if (mv.k === 'l') { hold[p].splice(hold[p].indexOf(mv.m), 1); b[mv.to] = tlT(p, mv.m); }
  else {
    b[mv.to] = b[mv.from]; b[mv.from] = 0;
    if (mv.k === 'j') { take = tlM(b[mv.over]); hold[p].push(take); b[mv.over] = 0; }
  }
  const g = tilesGroup(b, mv.to), dock = g.length >= 3 ? g : [];
  for (const c of dock) b[c] = 0;
  const sc = s.sc.slice(); sc[p] += dock.length;
  return { s: { b, hold, sc, p, first: s.first | 0, plies: s.plies, last: dock.length ? p : s.last, mode: s.mode, over: false, win: -1, why: '', reached: s.reached },
           take, dock, pts: dock.length };
}
// a whole turn: apply, pass the turn, and end the game when it's over
function tilesStep(s, mv) {
  const r = tilesApply(s, mv), n = r.s, R = TL_MODES[n.mode], p = n.p;
  n.plies++; n.p = 1 - p;
  if (n.reached < 0 && n.sc[p] >= R.target) n.reached = p;
  let end = '';
  if (n.reached >= 0) {
    // equal turns (quick game): if the first player got there, the second has one last turn
    const second = 1 - (n.first | 0);
    if (!R.finish || n.reached === second || p === second) end = 'target';
  }
  if (!end && n.plies >= R.turns * 2) end = 'turns';
  if (!end && !tilesMoves(n, n.p).length) end = 'stuck';
  if (end) tilesFinish(n, end);
  r.s = n; return r;
}
function tilesFinish(n, why) {
  const R = TL_MODES[n.mode];
  n.over = true; n.why = why;
  if (n.sc[0] !== n.sc[1]) { n.win = n.sc[0] > n.sc[1] ? 0 : 1; return; }
  n.why += '-tie';
  if (R.finish && n.reached >= 0) {   // quick game: more tiles left, else whoever reached the target first
    const a = tilesCount(n, 0), c = tilesCount(n, 1);
    n.win = a === c ? n.reached : (a > c ? 0 : 1); return;
  }
  if (n.last >= 0) { n.win = n.last; return; }
  const a = tilesCount(n, 0), c = tilesCount(n, 1);
  n.win = a === c ? -1 : (a > c ? 0 : 1);
}
// ---- crew play: three levels, plus a little personality (bold likes jumps, patient builds pairs) ----
function tilesVal(s, p) { return 0.3 * (tilesCount(s, p) - tilesCount(s, 1 - p)); }
function tilesBest(s, p) {   // the best immediate gain for p (used by Hard to read the reply)
  let best = -1e9; const q = s.p === p ? s : Object.assign({}, s, { p });
  for (const o of tilesMoves(q, p)) { const r = tilesApply(q, o), w = r.pts + tilesVal(r.s, p); if (w > best) best = w; }
  return best;
}
function tilesAI(s, level, rng, style) {
  const p = s.p, ms = tilesMoves(s, p);
  if (!ms.length) return null;
  if (level === 'easy' && rng() < 0.5) return ms[(rng() * ms.length) | 0];
  const st = style || {};
  let bv = -1e9, best = ms[0];
  for (const m of ms) {
    const r = tilesApply(s, m); let v = r.pts + tilesVal(r.s, p);
    if (level === 'hard') {
      const w = tilesBest(Object.assign({}, r.s, { p: 1 - p }), 1 - p);
      if (w > -1e9) v -= 0.9 * (w - tilesVal(r.s, 1 - p));
    }
    if (st.bold && m.k === 'j') v += 0.25;
    if (st.patient && !r.pts) { const t = r.s.b[m.to]; if (t) v += 0.1 * (tilesGroup(r.s.b, m.to).length - 1); }
    v += rng() * 0.01;
    if (v > bv) { bv = v; best = m; }
  }
  return best;
}
// one whole game on paper between two levels (tiles_check and the balance numbers)
function tilesSimGame(mode, a, c, seed, styles) {
  const rng = tilesRng(seed); let s = tilesNew(mode, rng, false);
  while (!s.over) {
    const mv = tilesAI(s, s.p ? c : a, rng, styles && styles[s.p]);
    if (!mv) { tilesFinish(s, 'stuck'); break; }
    s = tilesStep(s, mv).s;
  }
  return s;
}
// a crew member's way of playing, the same every game: level and leanings seeded from who they are
const TL_STYLE = { rina: { level: 'hard', bold: true, patient: false, chatty: false }, tomas: { level: 'easy', bold: false, patient: true, chatty: true } };
function tilesStyle(p) {
  if (!p) return { level: 'medium', bold: false, patient: false, chatty: false };
  if (TL_STYLE[p.id]) return TL_STYLE[p.id];
  const u = k => schedU(p.seed | 0, 0, k), lv = u(806), comp = (p.traits || []).some(t => /competitive/i.test(t));
  return { level: comp || lv > .8 ? 'hard' : lv > .3 ? 'medium' : 'easy', bold: u(803) < .35, patient: u(804) < .3, chatty: u(805) < .4 };
}
// ---- the board on your device (0.46.1): the Tiles app. A game in play draws as a 6 x 6 board in the device's
// phosphor screen; tap a tile, then where it goes (legal squares glow, a square that docks shows a spark); tap your
// hold to launch. The crew member answers a moment later. No timers on you, no drag, words for every move.
SHIP.tiles = { played: 0, won: 0, lost: 0, taught: false, vs: {}, first: {}, relDay: {}, firstWin: null, beatRina: null, night: { last: null, rina: 0, games: [] } };   // read from save.tiles below
let TL_GAME = null;   // { s, opp, name, style, rng, where, teach, hint, sel, log: [lines], fx, timer }
const TL_TALK = {   // stand-ins until the writers' lines (lineFor(who, 'tiles.<kind>')) arrive
  start: { rina: ['Best of one. Try to keep up.'], chatty: ['Oh good, a game. Did I tell you about the hydroponics leak?', 'Go easy on me. Or don\'t, I\'ll learn more.'], any: ['Your move.', 'Let\'s see what you\'ve got.'] },
  dock:  { rina: ['That\'s three.', 'Docked.'], chatty: ['Ooh, look at that!', 'Three in a row, well, three in a lump.'], any: ['Docked.', 'There we go.'] },
  miss:  { chatty: ['Ooh, you could\'ve docked there.'], any: [] },
  win:   { rina: ['Good game. Again?'], chatty: ['I won? I never win! Well, sometimes.'], any: ['Good game.', 'Close one.'] },
  lose:  { rina: ['...Again. Now.'], chatty: ['You\'re a natural! I knew it.'], any: ['Well played.', 'You got me.'] },
};
// How to play (0.28.51, the user's "we also need a tiles tutorial"): short steps in a card above the board, on your first
// game (with the teaching layout) and whenever you press How to play. A step with `wait` moves on by itself when you do
// it (select a tile, step, jump, launch, dock); every step has Next and Skip, so it never holds you up.
// t(name, mode) -> its text, a line or two on a phone.
const TL_TUT = [
  { t: n => 'Yours are the solid tiles. ' + n + '’s are dashed.' },
  { t: () => 'Marks: ● ▲ ★. Three of one touching DOCK: a point each.' },
  { t: () => 'Tap one of your tiles to see where it can go.', wait: 'sel' },
  { t: () => 'STEP: tap a lit square, one diagonal forward.', wait: 's' },
  { t: n => 'JUMP over ' + n + '’s tile to take it into your hold.', wait: 'j' },
  { t: () => 'LAUNCH: tap your hold, then a free home square.', wait: 'l' },
  { t: () => 'A spark on a square means it docks. Go for it!', wait: 'dock' },
  { t: (n, R) => 'First to ' + R.target + ' wins, or most after ' + R.turns + ' turns. Have fun!' },
];
function tilesTut(did) {   // something happened: the step waiting for it moves on
  const G = TL_GAME; if (!G || G.tut < 0) return;
  const st = TL_TUT[G.tut]; if (st && st.wait === did) G.tut = G.tut + 1 >= TL_TUT.length ? -1 : G.tut + 1;
}
function tilesTalk(kind) {
  const G = TL_GAME; if (!G) return null;
  if (typeof lineFor === 'function') { try { const l = lineFor(G.opp, 'tiles.' + kind, {}); if (l && l.text) return l.text; } catch (e) { /* no line yet */ } }
  const bank = TL_TALK[kind] || {}, l = bank[G.opp] || (G.style.chatty && bank.chatty) || bank.any || [];
  if (!l.length) return null;
  return l[Math.floor(G.talk() * l.length)];
}
const tlName = (t, mine) => (mine ? 'your ' : 'their ') + TL_MARKS[tlM(t)];
function tilesSay(text) { const G = TL_GAME; if (!G || !text) return; G.log.push(text); if (G.log.length > 3) G.log.shift(); }
// start a game: opponentId (a crew id), where (a place id or null), mode 'full' | 'quick'
// the opponent stays in their seat while you play (0.46.6, folded into 0.28.51): section 10's crewHold(p, placeId) (sim engineer 3) keeps a
// walker at its place until the release it returns is called: when you press Done, walk off, start again or a new game
function tilesUnhold(G) { if (G && G.hold) { const f = G.hold; G.hold = null; try { f(); } catch (e) { /* the walker's gone */ } } }
function tilesHold(G, p) {
  if (typeof crewHold !== 'function' || typeof DECK_CREW === 'undefined') return;
  const a = DECK_CREW.find(x => x.p && x.p.id === p.id); if (a && a.goalId) G.hold = crewHold(p, a.goalId);
}
function tilesPlay(opponentId, where, mode, tut) {   // tut: run the How to play steps (0.28.51; your first game always does)
  if (TL_GAME && TL_GAME.timer) clearTimeout(TL_GAME.timer);
  tilesUnhold(TL_GAME);
  const T = SHIP.tiles, p = (typeof ROSTER !== 'undefined' && ROSTER.find(x => x.id === opponentId)) || { id: opponentId || 'tomas', name: 'Tomas Lind', seed: 7 };
  const teach = !T.played, style = teach ? Object.assign({}, tilesStyle(p), { level: 'easy' }) : tilesStyle(p);
  const seed = Math.floor(schedU((p.seed | 0) ^ (T.played * 7919), SHIP.time.day, 800) * 4294967296);
  const rng = tilesRng(seed), first = teach ? 0 : (T.first[p.id] | 0);   // you go first in your first game, then turn about with each opponent (saved)
  const talk = tilesRng(Math.floor(schedU((p.seed | 0) ^ (T.played * 7919), SHIP.time.day, 807) * 4294967296));   // its own stream: lines never shift the moves
  TL_GAME = { s: tilesNew(mode === 'quick' ? 'quick' : 'full', rng, teach, first), opp: p.id, name: (p.name || p.id).split(' ')[0], style, rng, talk, where: where || null,
              teach, hint: teach, sel: null, log: [], fx: null, timer: 0, done: false, hold: null, tut: tut || TL_UI.teachNext || (!T.played && !T.taught) ? 0 : -1 };   // TL_UI.teachNext: the Tiles app's How to play
  TL_UI.teachNext = false;
  if (TL_GAME.tut === 0) T.taught = true;
  tilesHold(TL_GAME, p);
  tilesSay(TL_GAME.name + ': ' + (tilesTalk('start') || 'Your move.'));
  if (first) tilesCrewSoon();
  deviceShow('tiles');
  try { while (TIP_Q.length) tipDone(); if (DEV.hu) devHeadsDo('done'); } catch (e) { /* no device yet */ }   // nothing left frozen on top of the board (0.28.51)
  return TL_GAME;
}
function tilesCrewSoon() {
  const G = TL_GAME; if (!G || G.s.over || G.s.p !== 1) return;
  if (G.timer) clearTimeout(G.timer);
  G.timer = setTimeout(() => { G.timer = 0; tilesCrewMove(); }, 700);
}
function tilesCrewMove() {   // the crew member's turn (tiles_check calls it directly)
  const G = TL_GAME; if (!G || G.s.over || G.s.p !== 1) return;
  const mv = tilesAI(G.s, G.style.level, G.rng, G.style);
  if (!mv) { tilesFinish(G.s, 'stuck'); tilesOver(); return; }
  tilesDo(mv);
}
// one move by whoever's turn it is, with the words and the effects
function tilesDo(mv) {
  const G = TL_GAME, s0 = G.s, p = s0.p, who = p ? G.name : 'You', mine = p === 0, t = mv.k === 'l' ? tlT(p, mv.m) : s0.b[mv.from];
  if (mine && G.style.chatty) {   // Tomas notices a dock you passed up (once a game)
    const could = tilesMoves(s0, 0).some(m => tilesApply(s0, m).pts);
    G.missOk = G.missOk === undefined ? true : G.missOk;
    if (could && G.missOk && !tilesApply(s0, mv).pts) { const l = tilesTalk('miss'); if (l) { G.missLater = l; G.missOk = false; } }
  }
  const r = tilesStep(s0, mv); G.s = r.s; G.sel = null;
  const ghosts = {}; for (const c of r.dock) ghosts[c] = c === mv.to ? t : s0.b[c] || t;
  if (mv.k === 'j') ghosts[mv.over] = s0.b[mv.over];
  G.fx = { to: mv.to, from: mv.k === 'l' ? -1 : mv.from, dock: r.dock.slice(), over: mv.k === 'j' ? mv.over : -1, ghosts, big: r.dock.length >= 4 };
  let line = mv.k === 'l' ? who + ' launched ' + (mine ? 'a ' : 'a ') + TL_MARKS[mv.m] + ' from ' + (mine ? 'your' : 'their') + ' hold.'
    : mv.k === 'j' ? who + ' jumped ' + tlName(s0.b[mv.over], !mine) + ' and took it.' : who + ' stepped ' + (mine ? 'your ' : 'their ') + TL_MARKS[tlM(t)] + '.';
  if (r.pts) line += ' Dock! ' + r.pts + ' point' + (r.pts > 1 ? 's' : '') + '.';
  tilesSay(line);
  if (!mine && r.pts) { const l = tilesTalk('dock'); if (l) tilesSay(G.name + ': ' + l); }
  if (mine && G.missLater) { tilesSay(G.name + ': ' + G.missLater); G.missLater = null; }
  if (G.hint && mv.k === 'j' && mine) G.hint = false;
  if (mine) { tilesTut(mv.k); if (r.pts) tilesTut('dock'); }
  setTimeout(() => { if (TL_GAME === G && G.fx && G.fx.to === mv.to) { G.fx = null; tilesDraw(); } }, 520);
  if (G.s.over) tilesOver(); else tilesCrewSoon();
  tilesDraw();
}
function tilesOver() {   // the end of a game: the words, the tally, what it gives (tilesReward)
  const G = TL_GAME; if (!G || G.done) return; G.done = true;
  const s = G.s, you = s.win === 0, T = SHIP.tiles;
  T.played++; if (you) T.won++; else if (s.win === 1) T.lost++;
  T.first[G.opp] = 1 - (s.first | 0);   // the other one starts next time
  const v = T.vs[G.opp] || (T.vs[G.opp] = [0, 0]); if (you) v[0]++; else if (s.win === 1) v[1]++;
  const how = s.why.indexOf('tie') >= 0 ? ' (level on points: ' + (s.why.indexOf('target') >= 0 || TL_MODES[s.mode].finish ? 'decided by tiles left' : 'whoever docked last wins') + ')' : '';
  tilesSay((you ? 'You win, ' : s.win === 1 ? G.name + ' wins, ' : 'A draw, ') + s.sc[0] + ' to ' + s.sc[1] + '.' + how);
  const l = tilesTalk(you ? 'lose' : 'win'); if (l && s.win >= 0) tilesSay(G.name + ': ' + l);
  tilesReward(G, you);
  if (typeof simNote === 'function') simNote('tiles', { opp: G.opp, win: you, sc: s.sc.slice(), mode: s.mode, where: G.where });
}
function tilesTap(c) {   // a tap on square c (0-35), or on the hold ('h' + mark)
  const G = TL_GAME; if (!G || G.s.over || G.s.p !== 0 || tilesLeft()) return;
  const ms = tilesMoves(G.s, 0);
  if (typeof c === 'string') { const m = +c.slice(1); G.sel = G.sel && G.sel.h === m ? null : { h: m }; if (G.sel) tilesTut('sel'); tilesDraw(); return; }
  if (G.sel) {
    const mv = ms.find(m => m.to === c && (G.sel.h !== undefined ? m.k === 'l' && m.m === G.sel.h : m.from === G.sel.c));
    if (mv) { tilesDo(mv); return; }
  }
  const t = G.s.b[c];
  G.sel = t && tlO(t) === 0 && ms.some(m => m.from === c) && !(G.sel && G.sel.c === c) ? { c } : null;
  if (G.sel) tilesTut('sel');
  tilesDraw();
}
const TL_CSS = `
.tlx{margin:2px 0 8px}
.tlx .tl-sc{display:flex;flex-wrap:wrap;justify-content:space-between;gap:2px 8px;margin:2px 0 2px;font-variant-numeric:tabular-nums}
.tlx .tl-sc b{color:var(--crt-hot);font-weight:700}
.tlx .tl-pz{width:max-content;max-width:100%;margin:2px auto 4px;padding:1px 10px;border:1px solid var(--crt-dim);border-radius:10px;font-size:15px;line-height:1.35;text-align:center}   /* 0.72.2 (HUD U): the paused clock, as Lightdisc's line under its score */
.tlx .tl-pz[hidden]{display:none}
.tlx .tl-bd{display:grid;grid-template-columns:repeat(6,1fr);width:min(100%,336px,max(264px,calc(66vh - 230px)));margin:4px auto 8px;border:2px solid var(--crt-dim);border-radius:10px;overflow:hidden;touch-action:manipulation}
.tlx .tl-c{position:relative;min-height:44px;aspect-ratio:1;padding:0;margin:0;border:0;border-radius:0;background:transparent}
.tlx .tl-c.dk{background:rgba(255,255,255,.045)}
.tlx .tl-c.home{box-shadow:inset 0 -2px 0 rgba(255,255,255,.06)}
.tlx .tl-t{position:absolute;inset:11%;border-radius:20%;display:flex;align-items:center;justify-content:center;color:var(--crt-bg)}
.tlx .tl-t.o0{background:var(--crt-ink);box-shadow:0 0 6px var(--crt-glow)}
.tlx .tl-t.o1{border:2px dashed var(--crt-ink);background:var(--crt-bg);color:var(--crt-ink)}
.tlx .tl-t.o1.m2{color:var(--crt-hot)}
.tlx .tl-t::after{content:"";width:56%;height:56%;background:currentColor}
.tlx .tl-t.m0::after{border-radius:50%;width:48%;height:48%}
.tlx .tl-t.m1::after{clip-path:polygon(50% 4%,97% 92%,3% 92%)}
.tlx .tl-t.m2::after{clip-path:polygon(50% 0,61% 35%,98% 35%,68% 57%,79% 91%,50% 70%,21% 91%,32% 57%,2% 35%,39% 35%)}
.tlx .tl-c.sel .tl-t{outline:3px solid var(--crt-hot);outline-offset:1px}
.tlx .tl-c.to::before{content:"";position:absolute;inset:34%;border-radius:50%;border:2px solid var(--crt-hot)}
.tlx .tl-c.to.dock::before{background:var(--crt-hot);inset:30%;clip-path:polygon(50% 0,62% 38%,100% 50%,62% 62%,50% 100%,38% 62%,0 50%,38% 38%);border:0;border-radius:0}
.tlx .tl-c.last{box-shadow:inset 0 0 0 2px var(--crt-dim)}
.tlx .tl-c.hint .tl-t{animation:tlhint 1.2s ease-in-out infinite}
.tlx .tl-t.arrive{animation:tlin .28s ease-out}
.tlx .tl-t.gone{animation:tldock .5s ease-out forwards}
.tlx .tl-t.gone.big{animation-name:tldock2}
.tlx .tl-t.taken{animation:tltake .5s ease-in forwards}
.tlx .tl-hd{display:flex;flex-wrap:wrap;align-items:center;gap:8px;min-height:48px;margin:0 0 6px}
.tlx .tl-hd button{position:relative;width:48px;height:48px;padding:0}
.tlx .tl-hd button.sel{border-color:var(--crt-hot)}
.tlx .tl-now{margin:2px 0 4px;min-height:2.7em}
.tlx .tl-log{margin:4px 0;color:var(--crt-dim)}
.tlx .tl-log p{margin:2px 0}
.tlx .tl-card{color:var(--crt-dim);margin:6px 0}
.tlx .tl-tut{display:flex;align-items:center;gap:8px;border:2px solid var(--crt-ink);border-radius:8px;padding:6px 8px;margin:0 0 6px;box-shadow:0 0 8px var(--crt-glow)}
.tlx .tl-tut[hidden]{display:none}
.tlx .tl-tut p{flex:1;min-width:0;margin:0;color:var(--crt-hot)}
.tlx .tl-tut .btns{flex:none;flex-direction:column;gap:6px}
.tlx .tl-tut p b{color:var(--crt-dim);font-weight:400;margin-right:6px}
.tlx.tut .tl-bd{width:min(100%,336px,max(264px,calc(66vh - 300px)))}
.tlx .tl-tut .btns,.tlx .tl-end,.tlx .tl-play{display:flex;flex-wrap:wrap;gap:8px}
.tlx .tl-play{margin:6px 0}
@keyframes tlin{from{transform:scale(.6);opacity:.4}to{transform:none;opacity:1}}
@keyframes tldock{0%{transform:none;opacity:1;box-shadow:0 0 0 0 var(--crt-glow)}100%{transform:translateY(-30%) scale(1.15);opacity:0;box-shadow:0 0 0 12px transparent}}
@keyframes tldock2{0%{transform:none;opacity:1;box-shadow:0 0 0 0 var(--crt-glow),0 0 0 0 var(--crt-glow)}100%{transform:translateY(-40%) scale(1.25);opacity:0;box-shadow:0 0 0 10px transparent,0 0 0 20px transparent}}
@keyframes tltake{to{transform:translateY(60%) scale(.5);opacity:0}}
@keyframes tlhint{50%{transform:scale(1.08)}}
@media (prefers-reduced-motion:reduce){.tlx .tl-t{animation:none!important}.tlx .tl-t.gone,.tlx .tl-t.taken{display:none}}
`;
const TL_UI = { root: null };
function tilesDraw() {   // draw the game into its persistent element (the device's dom block re-attaches it)
  const G = TL_GAME; if (!G) return null;
  if (!TL_UI.root) {
    const st = document.createElement('style'); st.textContent = TL_CSS; document.head.appendChild(st);
    const root = document.createElement('div'); root.className = 'tlx';
    root.innerHTML = '<p class="tl-sc"></p><p class="tl-pz" hidden>⏸ The ship\'s clock is paused while you play</p><p class="tl-now hot" aria-live="polite"></p><div class="btns tl-end"></div><div class="tl-bd" role="grid" aria-label="Tiles board"></div><div class="tl-tut" role="status" aria-live="polite" aria-label="How to play" hidden></div><div class="tl-hd"></div><div class="tl-log"></div><div class="btns tl-play"></div><p class="tl-card">STEP diagonally forward · JUMP to take a tile · LAUNCH from your hold · 3 of a mark touching = DOCK. First to <span></span>.</p>';
    const bd = root.querySelector('.tl-bd');
    for (let y = 5; y >= 0; y--) for (let x = 0; x < 6; x++) {
      const c = y * 6 + x, b = document.createElement('button'); b.type = 'button'; b.className = 'tl-c' + ((x + y) % 2 ? '' : ' dk') + (y < 2 ? ' home' : '');
      b.dataset.c = c; bd.appendChild(b);
    }
    root.onclick = e => {
      e.stopPropagation(); const b = e.target.closest('button'); if (!b) return;
      if (b.dataset.c !== undefined) tilesTap(+b.dataset.c);
      else if (b.dataset.h !== undefined) tilesTap('h' + b.dataset.h);
      else if (b.dataset.end) tilesEnd(b.dataset.end);
    };
    TL_UI.root = root;
  }
  const root = TL_UI.root, s = G.s, ms = !s.over && s.p === 0 ? tilesMoves(s, 0) : [], R = TL_MODES[s.mode], fx = G.fx;
  const sel = G.sel, tos = sel ? ms.filter(m => sel.h !== undefined ? m.k === 'l' && m.m === sel.h : m.from === sel.c) : [];
  const hintC = G.hint ? (ms.find(m => m.k === 'j') || {}).from : undefined;
  const sc = root.querySelector('.tl-sc'); sc.textContent = '';
  const turnTxt = s.over ? 'Game over' : s.p === 0 ? 'Your turn' : G.name + '’s turn';
  const pts = document.createElement('span'), B = n => Object.assign(document.createElement('b'), { textContent: n });
  pts.append('You ', B(s.sc[0]), ' · ' + G.name + ' ', B(s.sc[1]));
  const clk = Object.assign(document.createElement('span'), { textContent: 'Ship time ' + hhmm(SHIP.time.min) });   // held while you play (PAUSE.tiles, below); it runs again on the result screen
  { let pz = false; try { pz = !!(PAUSE.tiles && PAUSE.tiles()); } catch (e) { pz = false; } const pe = root.querySelector('.tl-pz'); pe.hidden = !pz; if (pz && !pe.dataset.t) { let t = null; try { t = careerText('tiles.paused'); } catch (e) { t = null; } pe.dataset.t = 1; if (t) pe.textContent = (/^⏸/.test(t) ? '' : '⏸ ') + t; } }   // 0.72.2 (HUD U, the user's Step 3 ask): say so under the score, exactly while it's held
  sc.append(pts,
            Object.assign(document.createElement('span'), { textContent: turnTxt + ' · ' + Math.min(R.turns, Math.floor(s.plies / 2) + 1) + '/' + R.turns }), clk);
  for (const b of root.querySelectorAll('.tl-c')) {
    const c = +b.dataset.c, t = s.b[c], ghost = fx && fx.ghosts[c], to = tos.find(m => m.to === c);
    b.classList.toggle('sel', !!(sel && sel.c === c)); b.classList.toggle('to', !!to); b.classList.toggle('dock', !!(to && tilesApply(s, to).pts));
    b.classList.toggle('last', !!(fx && (c === fx.to || c === fx.from))); b.classList.toggle('hint', hintC === c);
    const show = t || ghost;
    b.textContent = '';
    if (show) {
      const i = document.createElement('i'); i.className = 'tl-t o' + tlO(show) + ' m' + tlM(show);
      if (!t && ghost) i.classList.add(fx.over === c ? 'taken' : 'gone'); if (!t && ghost && fx.big) i.classList.add('big');
      if (t && fx && c === fx.to) i.classList.add('arrive');
      b.appendChild(i);
    }
    const x = 'abcdef'[c % 6] + (Math.floor(c / 6) + 1);
    b.setAttribute('aria-label', x + ': ' + (t ? tlName(t, tlO(t) === 0) : 'empty') + (to ? ', move here' + (b.classList.contains('dock') ? ', docks' : '') : ''));
  }
  const hd = root.querySelector('.tl-hd'); hd.textContent = '';
  hd.appendChild(Object.assign(document.createElement('span'), { textContent: s.hold[0].length ? 'Your hold:' : 'Your hold is empty.' }));
  s.hold[0].forEach(m => {
    const b = document.createElement('button'); b.type = 'button'; b.dataset.h = m; b.className = sel && sel.h === m ? 'sel' : '';
    b.setAttribute('aria-label', 'Launch a ' + TL_MARKS[m] + ' from your hold');
    const i = document.createElement('i'); i.className = 'tl-t o0 m' + m; b.appendChild(i); hd.appendChild(b);
  });
  if (s.hold[1].length) hd.appendChild(Object.assign(document.createElement('span'), { textContent: '· ' + G.name + ' holds ' + s.hold[1].length }));
  const lg = root.querySelector('.tl-log'); lg.textContent = '';   // the latest line above the board, the two before it below
  const lines = G.hint && hintC !== undefined ? G.log.concat(['Jump their tile to take it. It’s yours now.']) : G.log;
  root.querySelector('.tl-now').textContent = lines[lines.length - 1] || '';
  const tutOn = G.tut >= 0 && !s.over; root.querySelector('.tl-now').hidden = tutOn; root.classList.toggle('tut', tutOn);   // a How to play step stands in for it (the line shows below)
  for (const l of (tutOn ? lines : lines.slice(0, -1)).reverse()) lg.appendChild(Object.assign(document.createElement('p'), { textContent: l }));
  root.querySelector('.tl-card').hidden = SHIP.tiles.played >= 3 && !G.teach;
  root.querySelector('.tl-card span').textContent = R.target;
  const end = root.querySelector('.tl-end'); end.textContent = '';
  const btn = (box, k, label) => { const b = document.createElement('button'); b.type = 'button'; b.className = 'act'; b.dataset.end = k; b.textContent = label; box.appendChild(b); };
  if (s.over) for (const [k, label] of [['full', 'Again'], ['quick', 'Quick game (to 5)'], ['done', 'Done']]) btn(end, k, label);
  const pb = root.querySelector('.tl-play'); pb.textContent = '';
  if (!s.over) { if (G.tut < 0) btn(pb, 'teach', 'How to play'); btn(pb, 'leave', 'Leave game'); }   // 0.28.51, under the board: the steps again; get up mid-game (not counted)
  const tu = root.querySelector('.tl-tut'), st = G.tut >= 0 && TL_TUT[G.tut];   // How to play (0.28.51)
  tu.hidden = !st || s.over; tu.textContent = '';
  if (st && !s.over) {
    const tp = document.createElement('p'); tp.append(Object.assign(document.createElement('b'), { textContent: (G.tut + 1) + '/' + TL_TUT.length }), st.t(G.name, R)); tu.appendChild(tp);
    const bx = document.createElement('div'); bx.className = 'btns'; btn(bx, 'tnext', G.tut + 1 < TL_TUT.length ? 'Next ▸' : 'Got it'); if (G.tut + 1 < TL_TUT.length) btn(bx, 'tskip', 'Skip'); tu.appendChild(bx);
    if (G.tutSeen !== G.tut) { G.tutSeen = G.tut; requestAnimationFrame(() => { try { if (!tu.hidden && tu.isConnected) tu.scrollIntoView({ block: 'nearest' }); } catch (e) { /* old browser */ } }); }   // the step, with your rows above it
  }
  return root;
}
function tilesEnd(k) {
  const G = TL_GAME; if (!G) return;
  if (k === 'done') { tilesUnhold(G); TL_GAME = null; deviceRefresh(); return; }
  if (k === 'leave') { if (G.timer) clearTimeout(G.timer); tilesUnhold(G); TL_GAME = null; toast('Tiles', 'You leave the game. ' + G.name + ' tidies the tiles away.'); deviceRefresh(); return; }   // mid-game (0.28.51): not counted
  if (k === 'teach') { G.tut = 0; SHIP.tiles.taught = true; tilesDraw(); return; }
  if (k === 'tnext' || k === 'tskip') { G.tut = k === 'tskip' || G.tut + 1 >= TL_TUT.length ? -1 : G.tut + 1; tilesDraw(); return; }
  tilesPlay(G.opp, G.where, k);
}
deviceApp({ id: 'tiles', title: 'Tiles', short: 'Tiles', icon: 'dot', order: 75,
  view: () => {
    tilesLeft();
    if (TL_GAME) return { title: 'Tiles with ' + TL_GAME.name, blocks: [{ kind: 'dom', render: box => { const r = tilesDraw(); if (r) box.appendChild(r); } }] };
    const T = SHIP.tiles, blocks = [{ kind: 'text', text: 'Sit at the Tiles station in the bow lounge (or a Tiles table on Tiles night) and whoever’s free comes over to play. While you play, the ship waits.' }];
    blocks.push({ kind: 'buttons', items: [{ label: TL_UI.teachNext ? 'How to play: next game' : 'How to play', action: { app: 'tiles', do: 'teach' } }] });   // 0.28.51: the steps again, at your next game
    blocks.push({ kind: 'text', text: T.played ? 'Played ' + T.played + ', won ' + T.won + ', lost ' + T.lost + '.' : 'You haven’t played yet.' });
    const vs = Object.keys(T.vs).filter(k => T.vs[k][0] + T.vs[k][1]).map(k => { let p = null; try { p = ROSTER.find(x => x.id === k); } catch (e) { /* before section 9 loads */ } return (p ? p.name.split(' ')[0] : k) + ' ' + T.vs[k][0] + '-' + T.vs[k][1]; });
    if (vs.length) blocks.push({ kind: 'text', text: 'Against: ' + vs.join(', ') + '.' });
    if (T.firstWin !== null) blocks.push({ kind: 'text', text: 'Your first win: day ' + T.firstWin + '.' });
    if (T.beatRina !== null) blocks.push({ kind: 'text', mark: 'hot', text: 'You beat Rina on day ' + T.beatRina + '.' });
    if (T.night && T.night.last !== null && T.night.games.length) {   // the last Tiles night (0.46.3)
      const nm = id => { try { const p = ROSTER.find(x => x.id === id); return p ? p.name.split(' ')[0] : id; } catch (e) { return id; } };
      blocks.push({ kind: 'text', mark: 'head', text: 'Last Tiles night, day ' + T.night.last });
      for (const [a, b, w] of T.night.games) blocks.push({ kind: 'text', text: nm(w) + ' beat ' + nm(w === a ? b : a) + '.' });
      if (T.beatRina === null && T.night.rina > 1) blocks.push({ kind: 'text', text: 'Rina hasn’t lost in ' + T.night.rina + ' Tuesdays.' });
    }
    return { title: 'Tiles', blocks };
  },
  act: verb => { if (verb === 'teach') { if (TL_GAME) tilesEnd('teach'); else { TL_UI.teachNext = !TL_UI.teachNext; toast('Tiles', TL_UI.teachNext ? 'How to play will run at your next game.' : 'No walkthrough next game.'); } deviceRefresh(); } } });
// ---- sitting down to play (0.46.2; 0.28.51, the user's "You sit down and someone will come up if available. If not,
// the game tells you no one can play"): tap a Tiles table, station or board and you sit at a free seat. Someone already
// sitting at the board plays you; otherwise the best free crew member on the deck (tilesFind: off duty or at leisure,
// not asleep, eating, on an appointment, escorting or visiting; someone who likes Tiles or has played you, then a
// friend, then whoever's nearest) walks over (section 14's crewComeTo) and sits opposite, and the game opens as they
// sit. Nobody free: a toast says so and you just sit. The game is the 'tiles' activity (sit:play pose): it lasts until
// you press Done or Leave game, and walking away leaves the game.
// Playing stops time (the user's "Playing tiles stops time"): while a game is on (not yet over) PAUSE.tiles freezes the
// ship like Pause, without the overlay; it runs again on the result screen. No ship minutes pass while you play, so the
// game's social comes in one go at its end (TL_GAIN, by your bond with them, like the other activities).
const TL_ITEM = /^Tiles (table|station|board)\b/i, TL_NEAR = 2.4, TL_FAR = 40, TL_WAIT = 30, TL_GAIN = 12, TL_AGAIN = .25;   // TL_FAR metres on the deck; TL_WAIT ship minutes for them to come
const tlSecond = id => { try { const p = ROSTER.find(x => x.id === id); return p ? p.name.split(' ')[0] : id; } catch (e) { return id; } };
Object.assign(PLAYER_ACTS, { tiles: { need: null, mins: 20, pose: 'sit:play', title: 'Playing Tiles', done: 'You get up from the board.',
  until: A => tilesSeatTick(A) } });
function tilesSeatTick(A) {   // the 'tiles' activity while you sit: find someone, wait for them, play; true ends it
  const o = A.o;
  if (o.st === 'play') return !TL_GAME || TL_GAME.where !== A.placeId;
  const seats = (o.board || []).filter(id => id !== A.placeId), here = a => a && a.settled && a.p && a.p.id && ROSTER.some(x => x.id === a.p.id);
  if (!o.st) {
    const sat = seats.map(id => heldBy(id)).find(here);   // someone already at the board
    if (sat) return tilesBegin(A, sat.p.id);
    const seat = seats.filter(id => !heldBy(id)).map(id => [id, placeSpot(id)]).filter(x => x[1])
      .sort((m, n) => Math.hypot(n[1].x - A.spot.x, n[1].z - A.spot.z) - Math.hypot(m[1].x - A.spot.x, m[1].z - A.spot.z))[0];   // the seat across from you: the farthest free one
    const a = seat && tilesFind(seat[1]);
    if (!a) { tilesNobody(A); return false; }
    o.st = 'wait'; o.opp = a.p.id; o.seat = seat[0]; o.since = shipNow(); o.here = false;
    const go = crewComeTo(a.p, seat[0], () => { o.here = true; }, { until: shipNow() + TL_WAIT + 30 }), prev = A.release;
    A.release = () => { if (prev) prev(); go(); };     // actEnd lets them go back to their own plans
    let said = null; try { const l = typeof lineFor === 'function' && lineFor(a.p.id, 'tiles.anytime', {}); said = l && l.text; } catch (e) { said = null; }   // the head writer's tiles.anytime, when it's in
    toast('Tiles', shortName(a.p) + ' sees you at the board and comes over to play.' + (said ? ' "' + said + '"' : ''));
    return false;
  }
  if (o.st === 'wait') {
    const a = DECK_CREW.find(x => x.p && x.p.id === o.opp), sp = placeSpot(o.seat);
    const there = a && a.settled && (o.here || sp && Math.hypot(a.x - sp.x, a.z - sp.z) < .6);
    if (there) return tilesBegin(A, o.opp);
    if (!a || shipNow() - o.since > TL_WAIT) { if (A.release) A.release(); A.release = null; tilesNobody(A, tlSecond(o.opp) + ' couldn’t make it after all.'); }
  }
  return false;
}
function tilesBegin(A, id) { A.o.st = 'play'; A.o.opp = id; tilesPlay(id, A.placeId, A.o.mode); return false; }
function tilesNobody(A, why) {   // nobody to play: you stay sat, as on any seat
  toast('Tiles', (why ? why + ' ' : '') + 'Nobody’s around to play right now. Try in the evening, or on a day off.');
  A.kind = 'sit'; A.def = { ...PLAYER_ACTS.sit }; A.o.st = 'none';
}
// who'd come and play: free now (whereIs), on this deck, not already wanted elsewhere; quiet hours (21:45-06:00) nobody
function tilesFind(at) {
  const now = shipNow(), m = ((now % 1440) + 1440) % 1440; if (m >= 1305 || m < 360) return null;
  const T = SHIP.tiles; let best = null, bs = -1e9;
  for (const a of DECK_CREW) {
    const p = a.p; if (!p || !p.id || !ROSTER.some(x => x.id === p.id)) continue;
    if (typeof CHAT !== 'undefined' && CHAT && CHAT.p === p || COME_TO.has(p.id) || CREW_HELD.has(p.id)) continue;
    let w = null; try { w = whereIs(p, now); } catch (e) { w = null; }
    if (!w || (w.act !== 'off' && w.act !== 'leisure') || w.deck !== deckDef.num) continue;
    const d = Math.hypot(a.x - at.x, a.z - at.z); if (d > TL_FAR) continue;
    const v = typeof VOICE !== 'undefined' && VOICE[p.id], plays = !!(v && Array.isArray(v.invites) && v.invites.includes('tiles')) || !!T.vs[p.id];
    let tier = 0; try { tier = typeof relTier === 'function' ? relTier(p.id) : 0; } catch (e) { tier = 0; }
    const sc = (plays ? 30 : 0) + tier * 8 - d;
    if (sc > bs || sc === bs && best && p.id < best.p.id) { bs = sc; best = a; }
  }
  return best;
}
PAUSE.tiles = () => !!(TL_GAME && !TL_GAME.s.over && tilesSeated());   // section 13: a game on stops the ship
PAUSE.tilesTap = () => { if (!TL_GAME) return; deviceShow('tiles'); toast('Tiles', 'Your game with ' + TL_GAME.name + ' is waiting. Leave game on the board gets you up.'); };
const tilesSeated = () => !!(TL_GAME && (!TL_GAME.where || (ACT && ACT.kind === 'tiles' && ACT.placeId === TL_GAME.where)));
function tilesLeft() {   // you walked away mid-game: the game is left as it was, not counted
  const G = TL_GAME; if (!G || tilesSeated()) return false;
  if (G.timer) clearTimeout(G.timer);
  tilesUnhold(G); TL_GAME = null; if (!G.s.over) toast('Tiles', 'You leave the game. ' + G.name + ' tidies the tiles away.');
  return true;
}
// the Tiles station is always open; tables and boards are for Tiles night (the lead, 0.46.4), and are plain seats otherwise
function tilesNightNow() {
  if (typeof eventsOn !== 'function') return false;
  const m = SHIP.time.min; try { return eventsOn(SHIP.time.day).some(e => /^tiles/i.test(e.id) && m >= e.from && m < e.to); } catch (e) { return false; }
}
function tilesWorldTap(it, at, point) {
  if (!it || !TL_ITEM.test(it.t || '')) return false;
  const jcr = /^Tiles table\b/i.test(it.t) && roomAt(...cellAt(at.x, at.z)) === 'j' && deckDef.num === 4;   // the junior common room's table: any time (0.28.62, the 0.60.7 plan)
  if (!/^Tiles station\b/i.test(it.t) && !jcr && !tilesNightNow()) return false;
  if (TL_GAME && tilesSeated()) { deviceShow('tiles'); return true; }
  const room = roomAt(...cellAt(at.x, at.z));
  const seats = [...PLACE_OF.values()].map(pl => [pl, placeSpot(pl.id)])
    .filter(([pl, s]) => s && (!room || pl.room === room) && (s.pose || pl.pose) === 'sit' && !privatePlace(pl) && ixDist(it, s) < TL_NEAR);
  if (!seats.length) return false;
  const free = seats.filter(([pl]) => !heldBy(pl.id)).sort((m, n) => Math.hypot(m[1].x - point.x, m[1].z - point.z) - Math.hypot(n[1].x - point.x, n[1].z - point.z))[0];
  if (!free) { toast(it.t, 'Every seat at the board is taken.'); return true; }
  const sat = seats.map(([pl]) => heldBy(pl.id)).find(a => a && a.p && a.p.id && ROSTER.some(x => x.id === a.p.id));
  actStart('tiles', free[0].id, { pose: 'sit:play', title: 'Tiles', flavour: sat ? 'You sit down across from ' + shortName(sat.p) + '.' : 'You sit down at the board.', board: seats.map(([pl]) => pl.id), mode: 'full' });   // then tilesSeatTick finds you someone (0.28.51)
  return true;
}
PLAYER_TAPS.unshift(tilesWorldTap);   // ahead of section 15b's ixTap, which would make the table's stools a plain sit
// what a game gives (0.46.2): a little friendship either way (more for a win), a memory, and a first-time line on your
// Tiles record; beating Rina is news ("Rina lost! To the new hand!"), a big memory for her, and the day is kept
function tilesReward(G, you) {
  const T = SHIP.tiles, day = SHIP.time.day, first = G.name;
  try {   // the game's social (0.28.51): in one go, as no ship minutes passed while you played; by your bond, with your needs' effects
    const N = SHIP.player.needs, fx = typeof playerFx === 'function' ? playerFx() : null, bm = typeof bondMult === 'function' ? bondMult(G.opp) : 1;
    const once = T.relDay[G.opp] !== day ? 1 : TL_AGAIN;
    if (typeof leisureAdd === 'function') leisureAdd(10 * once, 'tiles');   // a game of Tiles: +10 leisure (0.28.64), a quarter for more with them that day   // the full gain for your first game with them each ship day, a quarter after (the lead, 0.28.54: no filling social in no time)
    N.social = needClamp(N.social + TL_GAIN * once * (fx && typeof fxR === 'function' ? fxR(fx, 'social') : 1) * bm);
  } catch (e) { /* needs not there (tests on paper) */ }
  if (T.relDay[G.opp] !== day) {   // friendship and the memory once a ship day per opponent, like a chat; later games still count
    T.relDay[G.opp] = day;
    if (typeof relAdd === 'function') relAdd(G.opp, 'tiles', typeof REL_PTS !== 'undefined' && REL_PTS.chat || 2);
    if (typeof memAdd === 'function') memAdd(G.opp, 'came.tiles');
  }
  if (you && T.firstWin === null) { T.firstWin = day; toast('Tiles', 'Your first win at Tiles, against ' + first + '.'); }
  if (you && G.opp === 'rina' && T.beatRina === null) {
    T.beatRina = day;
    // the trophy on your keepsake shelf: the deck architect's DECK_DRESS 'tilesTrophy', shown from section 18's lasting traces
    if (typeof traceAdd === 'function') traceAdd('tilesTrophy', day);
    else if (Array.isArray(SHIP.traces) && !SHIP.traces.some(x => (x && x.id || x) === 'tilesTrophy')) SHIP.traces.push('tilesTrophy');
    if (typeof memAdd === 'function') memAdd('rina', 'moment.tiles');
    if (typeof newsAdd === 'function') newsAdd({ id: 'tiles-rina-beaten', about: 'you', lines: ['Rina lost! To the new hand!', 'Somebody finally beat Rina at Tiles.'], seed: ['rina', 'tomas'], weight: .9, life: 6 });
    toast('Tiles', 'You beat Rina. People are going to hear about this.');
  }
}
function tilesLoad(s) {   // save.tiles, read defensively
  const d = s && s.tiles && typeof s.tiles === 'object' ? s.tiles : {}, n = k => Number.isFinite(d[k]) && d[k] >= 0 ? Math.floor(d[k]) : 0, vs = {};
  if (d.vs && typeof d.vs === 'object') for (const k in d.vs) { const v = d.vs[k]; if (Array.isArray(v) && v.length === 2 && k.length < 40) vs[k] = [Math.max(0, v[0] | 0), Math.max(0, v[1] | 0)]; }
  const day = k => Number.isFinite(d[k]) ? Math.floor(d[k]) : null;
  const nt = d.night && typeof d.night === 'object' ? d.night : {}, games = Array.isArray(nt.games) ? nt.games.filter(g => Array.isArray(g) && g.length === 3 && g.every(x => typeof x === 'string' && x.length < 40)).slice(0, 20) : [];
  const night = { last: Number.isFinite(nt.last) ? Math.floor(nt.last) : null, rina: Number.isFinite(nt.rina) && nt.rina >= 0 ? Math.floor(nt.rina) : 0, games };
  const first = {}, relDay = {};
  if (d.first && typeof d.first === 'object') for (const k in d.first) if (k.length < 40 && (d.first[k] === 0 || d.first[k] === 1)) first[k] = d.first[k];
  if (d.relDay && typeof d.relDay === 'object') for (const k in d.relDay) if (k.length < 40 && Number.isFinite(d.relDay[k])) relDay[k] = Math.floor(d.relDay[k]);
  return { played: n('played'), won: n('won'), lost: n('lost'), taught: d.taught === true, vs, first, relDay, firstWin: day('firstWin'), beatRina: day('beatRina'), night };
}
SHIP.tiles = tilesLoad(SAVED);
SAVE_EXTRA.push(s => { s.tiles = JSON.parse(JSON.stringify(SHIP.tiles)); });
onSim('newGame', () => { SHIP.tiles = tilesLoad(null); if (TL_GAME && TL_GAME.timer) clearTimeout(TL_GAME.timer); tilesUnhold(TL_GAME); TL_GAME = null; });
// ---- Tiles night on paper (0.46.3): when the tradition ends (section 18's simNote('tradition'), id tilesNight), the
// crew who came are paired (seeded by the day, key 801) and each pairing is settled by a seeded roll (key 802) from
// their levels: the same level is even, Hard beats Medium 68%, Medium beats Easy 70%, Hard beats Easy 83% (tiles_check's
// numbers). Rina's story rule (the user, 2026-10-17): she wins every crew game until you beat her. One odd one out
// watches. The results are news the next morning, and the Tiles app keeps the last night.
const TL_ODDS = { easy: { easy: .5, medium: .3, hard: .17 }, medium: { easy: .7, medium: .5, hard: .32 }, hard: { easy: .83, medium: .68, hard: .5 } };
function tilesNight(d, came) {   // came: crew ids at the night; returns { day, games: [{ a, b, win }], out, rina }
  const ids = [...new Set((came || []).filter(id => typeof id === 'string' && id !== 'you'))];
  const P = id => { try { return ROSTER.find(x => x.id === id) || { id, seed: socHash(id) }; } catch (e) { return { id, seed: 0 }; } };
  const order = ids.map(id => [id, schedU(P(id).seed | 0, d, 801)]).sort((a, b) => a[1] - b[1] || (a[0] < b[0] ? -1 : 1)).map(x => x[0]);
  if (order.includes('rina') && order.length > 1) { order.splice(order.indexOf('rina'), 1); order.unshift('rina'); }   // the champion always gets a game
  const games = [];
  for (let i = 0; i + 1 < order.length; i += 2) {
    const a = order[i], b = order[i + 1], pa = P(a), pb = P(b), la = tilesStyle(pa).level, lb = tilesStyle(pb).level;
    let win;
    if ((a === 'rina' || b === 'rina') && SHIP.tiles.beatRina === null) win = 'rina';
    else win = schedU((pa.seed | 0) ^ (pb.seed | 0), d, 802) < TL_ODDS[la][lb] ? a : b;
    games.push({ a, b, win });
  }
  return { day: d, games, out: order.length % 2 ? order[order.length - 1] : null };
}
function tilesNightNews(r, you) {   // the night's results into the save and the news
  const T = SHIP.tiles, N = T.night || (T.night = { last: null, rina: 0, games: [] });
  if (N.last === r.day) return;   // once a night
  const rg = r.games.find(g => g.a === 'rina' || g.b === 'rina');
  if (rg) N.rina = rg.win === 'rina' ? N.rina + 1 : 0;
  N.last = r.day; N.games = r.games.map(g => [g.a, g.b, g.win]);
  if (typeof newsAdd !== 'function' || !r.games.length) return;
  const name = id => { try { const p = ROSTER.find(x => x.id === id); return p ? shortName(p) : id; } catch (e) { return id; } };
  const lines = [];
  if (rg && rg.win === 'rina') lines.push(N.rina > 1 ? 'Rina won again at Tiles. That’s ' + N.rina + ' Tuesdays running.' : 'Rina won at Tiles night, of course.');
  else if (rg) lines.push(name(rg.win) + ' beat Rina at Tiles night!');
  const lvl = id => { let p = null; try { p = ROSTER.find(x => x.id === id); } catch (e) { /* before section 9 */ } return tilesStyle(p || { id, seed: 0 }).level; };
  const up = r.games.find(g => g !== rg && TL_ODDS[lvl(g.win)][lvl(g.win === g.a ? g.b : g.a)] < .5);   // an upset: the weaker player won
  if (up) lines.push(name(up.win) + ' beat ' + name(up.win === up.a ? up.b : up.a) + ' at Tiles. Nobody saw that coming.');
  const other = r.games.find(g => g !== rg && g !== up);
  if (other && lines.length < 2) lines.push(name(other.win) + ' beat ' + name(other.win === other.a ? other.b : other.a) + ' at Tiles night.');
  if (you) lines.push('The new hand turned up to Tiles night.');
  newsAdd({ id: 'tiles-night:' + r.day, kind: 'gossip', weight: .6, life: 3, seed: r.games.flatMap(g => [g.a, g.b]).slice(0, 6), lines });
}
onSim('tradition', d => { if (!d || !/^tiles/i.test(d.id || '')) return; tilesNightNews(tilesNight(d.day, d.came || []), !!d.you); });
const tilesTrophy = () => SHIP.tiles.beatRina !== null;   // for the deck architect: the trophy on your bunk shelf once you've beaten Rina

// =====================================================================
// 23b. LIGHTDISC (the Lightdisc engineer, 0.82.x; plans/recdeck-plan.html section 4; the user approved the prototype,
// lightdisc-proto.html on claude/lightdisc-proto ba6b4ac, and this is that game on the rec deck's court)
// =====================================================================
// A Tron-style disc and tennis game, live on the court in 3D: you only move, returns are automatic. Off-centre sends
// the disc back steeper (up to 60°), moving as it meets you curves it, three returns in a row charge the next one, and
// it speeds up 10% a return to a cap (0.82.2, the user: shorter games; the prototype's was 5% to 10.5). First to 7, win by 2 (a quick game to 5). Ask someone to play at the court's gate:
// one free crew member comes down to the rec dec (a crewComeTo visit, the one exception to the deck's playerOnly), plays
// you, then goes back to their own plan. The ship's clock stops while you play (section 13's freeze, as for Tiles).
// The rules are pure: game space is x across the court (+ is your right), z along it (+ is your end, the bow), no DOM,
// no three.js, no R() and no Math.random. A game's stream is seeded from the save (schedU key 830); 831 picks a crew
// member's level when they have no personality of their own. Fixed 60 steps a second, whatever the frame rate.
const LD_DT = 1 / 60, LD_S0 = 5.0, LD_CAP = 13.5, LD_UP = 1.1, LD_REACH = .9, LD_MAXA = Math.PI / 3, LD_CURVE = .5, LD_CURL = 1.5, LD_CHARGE = 4 / 3, LD_YOU = 9;
const LD_HX = 2.38, LD_BASE = 5.6, LD_ZONE = 1.9, LD_OUT = 6.3, LD_R = .2;   // the court (DA6's recCourt): fields at ±2.38, baselines at 5.9, your zone to 3.9
// the crew's levels (plan section 4): reaction, speed, how often they misjudge, how wide, how often they curve, how off-centre they aim
const LD_LEVEL = {
  easy:   { react: .5, speed: 4.2, miss: .3, missAmt: .9, curve: .5, aim: [0, .5], aimRand: 1 },
  steady: { react: .38, speed: 5.0, miss: .14, missAmt: .6, curve: .1, aim: [0, .3] },
  sharp:  { react: .27, speed: 6.0, miss: .09, missAmt: .5, curve: .3, aim: [.3, .6] },
};
const LD_CREW = {   // the four with a personality of their own (the plan's): the rest play their level plainly
  pell:  { lvl: 'easy', react: .5, speed: 4.2, miss: .3, missAmt: .9, curve: .85, aim: [0, .5], aimRand: 1 },
  holt:  { lvl: 'steady', react: .38, speed: 5.0, miss: .14, missAmt: .6, curve: 0, aim: [0, .15] },
  vance: { lvl: 'sharp', react: .27, speed: 6.0, miss: .09, missAmt: .5, curve: .25, aim: [.3, .6] },
  rina:  { lvl: 'sharp', react: .24, speed: 6.4, miss: .065, missAmt: .4, curve: .45, aim: [.45, .8] },
};
function ldLevel(id) {   // { lvl, react, speed, ... } for a crew member (the same every time)
  if (LD_CREW[id]) return LD_CREW[id];
  const u = schedU(typeof idHash === 'function' ? idHash(String(id)) : 0, 0, 831), lvl = u < .35 ? 'easy' : u < .75 ? 'steady' : 'sharp';
  return { lvl, ...LD_LEVEL[lvl] };
}
function ldNext(g) {   // the game's own stream: mulberry32 on g.rs
  const a = g.rs = (g.rs + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
}
function ldClone(g) { const c = JSON.parse(JSON.stringify({ ...g, rng: null })); c.rng = () => ldNext(c); return c; }
function ldRng(seed) {   // mulberry32, as the prototype and Tiles (the view's chatter stream)
  let a = (seed >>> 0) || 1;
  return () => { a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
}
// o: { seed, quick, you: level or null (null: you play by input), them: level }. Side 0 is you (+z), side 1 them (-z).
function ldNew(o) {
  const g = { seed: (o.seed >>> 0) || 1, target: o.quick ? 5 : 7, step: 0, phase: 'serve', timer: 1, score: [0, 0], rally: 0, log: [], over: false, winner: -1, trail: [], ev: [] };
  g.rs = g.seed; g.rng = () => ldNext(g);              // the stream's state is plain data (g.rs), so a game can be copied (ldClone)
  const pl = (side, ai) => ({ side, ai, x: 0, z: side * LD_BASE, vx: 0, streak: 0, swing: 0, plan: null, hits: 0 });
  g.p = [pl(1, o.you || null), pl(-1, o.them)];
  g.server = g.rng() < .5 ? 0 : 1;
  g.d = { x: 0, z: 0, vx: 0, vz: 0, spd: LD_S0, curl: 0, boost: 1, owner: g.server, charged: false };
  ldServe(g);
  return g;
}
function ldServe(g) {
  const sp = g.p[g.server], d = g.d;
  d.x = sp.x; d.z = sp.z - sp.side * .7; d.vx = d.vz = 0; d.curl = 0; d.spd = LD_S0; d.boost = 1; d.owner = g.server; d.charged = false;
  for (const p of g.p) { p.streak = 0; p.plan = null; }
  g.rally = 0; g.trail = [];
}
function ldDisc(d) {   // one step of the disc; returns 1 or -1 when it bounces off a side field
  d.vx += d.curl * LD_DT; d.curl *= Math.exp(-LD_CURL * LD_DT);
  const sp = d.spd * d.boost, m = Math.hypot(d.vx, d.vz) || 1;
  d.vx *= sp / m; d.vz *= sp / m;
  if (Math.abs(d.vz) < .45 * sp) { d.vz = Math.sign(d.vz || 1) * .45 * sp; d.vx = Math.sign(d.vx) * Math.sqrt(sp * sp - d.vz * d.vz); }
  d.x += d.vx * LD_DT; d.z += d.vz * LD_DT;
  const lim = LD_HX - LD_R;
  if (d.x > lim) { d.x = 2 * lim - d.x; d.vx = -Math.abs(d.vx); d.curl *= -.4; return 1; }
  if (d.x < -lim) { d.x = -2 * lim - d.x; d.vx = Math.abs(d.vx); d.curl *= -.4; return -1; }
  return 0;
}
function ldPredict(d, z) {   // where the disc will cross z (the crew's reading, before their error)
  const c = { ...d };
  for (let n = 0; n < 400; n++) { const b = c.z; ldDisc(c); if ((b - z) * (c.z - z) <= 0) return c.x; }
  return c.x;
}
function ldPlan(g) {
  for (const p of g.p) {
    if (!p.ai) continue;
    const L = p.ai, r = g.rng, d = g.d;
    if (d.vz * p.side <= 0) { p.plan = { at: g.step + Math.round(L.react * 30), home: true }; continue; }
    // misjudging: likelier as the disc speeds up, and on a charged or curving disc; a misjudge really misses
    const k = .5 + 2.6 * (d.spd - LD_S0) / (LD_CAP - LD_S0) + (d.charged ? .8 : 0) + (Math.abs(d.curl) > .3 ? .6 : 0);
    const err = r() < L.miss * k ? (r() < .5 ? -1 : 1) * (LD_REACH + .05 + r() * L.missAmt) : (r() * 2 - 1) * .12;
    const other = g.p[p === g.p[0] ? 1 : 0], mag = L.aim[0] + r() * (L.aim[1] - L.aim[0]);
    let sgn = Math.abs(other.x) > .3 ? -Math.sign(other.x) : (r() < .5 ? -1 : 1);
    if (L.aimRand) sgn = r() < .5 ? -1 : 1;
    const curve = r() < L.curve ? (r() < .5 ? -1 : 1) : 0;
    p.plan = { at: g.step + Math.round(L.react / LD_DT), err, off: mag * sgn, curve, x: null };
  }
}
function ldAI(g, p) {
  const L = p.ai, d = g.d;
  let tx = p.x;
  if (g.phase !== 'live') tx = p.x * .98;
  else if (p.plan && g.step >= p.plan.at) {
    if (p.plan.home) tx = 0;
    else {
      if (p.plan.x === null) p.plan.x = ldPredict(d, p.z);
      tx = p.plan.x + p.plan.err - p.plan.off * LD_REACH * .8;
      const tt = (p.z - d.z) / (d.vz || 1e-3);
      if (p.plan.curve) tx += p.plan.curve * (tt < .18 ? .5 : -.5);   // wait to one side, then sweep through it so it meets them moving
    }
  }
  const lim = LD_HX - .25, k = p.plan && p.plan.home ? .6 : 1;
  tx = Math.max(-lim, Math.min(lim, tx));
  p.x += Math.max(-L.speed * k * LD_DT, Math.min(L.speed * k * LD_DT, tx - p.x));
  const tz = p.side * LD_BASE; p.z += Math.max(-2 * LD_DT, Math.min(2 * LD_DT, tz - p.z));
}
// you, by input: inp = { tx, tz } a target (thumb or mouse; null: stay) and { kx, kz } keys held (-1, 0, 1)
function ldYou(g, p, inp) {
  const lim = LD_HX - .25;
  if (inp.kx || inp.kz) { p.x += inp.kx * 6 * LD_DT; p.z += inp.kz * 4 * LD_DT; }
  else {
    if (inp.tx != null) p.x += Math.max(-LD_YOU * LD_DT, Math.min(LD_YOU * LD_DT, inp.tx - p.x));
    if (inp.tz != null) p.z += Math.max(-5 * LD_DT, Math.min(5 * LD_DT, inp.tz - p.z));
  }
  p.x = Math.max(-lim, Math.min(lim, p.x));
  p.z = Math.max(LD_BASE - LD_ZONE + .2, Math.min(LD_BASE + .45, p.z));
}
function ldStep(g, inp) {   // one fixed step; events go on g.ev ({ k: 'hit' | 'wall' | 'net' | 'point' | 'serve' | 'over', ... })
  g.step++;
  const d = g.d;
  for (const p of g.p) {
    const ox = p.x;
    if (p.ai) ldAI(g, p); else ldYou(g, p, inp || {});
    p.vx = (p.x - ox) / LD_DT; p.swing = Math.max(0, p.swing - LD_DT * 3.5);
  }
  if (g.phase === 'serve') {
    const sp = g.p[g.server]; d.x = sp.x; d.z = sp.z - sp.side * .7;
    if ((g.timer -= LD_DT) <= 0) {
      const a = (g.rng() * 2 - 1) * (Math.PI / 6);
      d.vx = Math.sin(a) * d.spd; d.vz = -sp.side * Math.cos(a) * d.spd; g.phase = 'live'; ldPlan(g); g.ev.push({ k: 'serve' });
    }
    return;
  }
  if (g.phase === 'point') {
    if ((g.timer -= LD_DT) <= 0) { if (g.over) { g.phase = 'over'; g.ev.push({ k: 'over' }); } else { g.phase = 'serve'; g.timer = 1; ldServe(g); } }
    return;
  }
  if (g.phase !== 'live') return;
  const bz = d.z, w = ldDisc(d);
  g.trail.unshift(d.x, d.z); if (g.trail.length > 28) g.trail.length = 28;
  if (w) g.ev.push({ k: 'wall', side: w, x: d.x, z: d.z });
  if (bz * d.z <= 0) g.ev.push({ k: 'net', x: d.x });
  for (let i = 0; i < 2; i++) {
    const p = g.p[i];
    if (d.vz * p.side <= 0) continue;
    const dx = d.x - p.x;
    if (Math.abs(d.z - p.z) < .45 && Math.abs(dx) < LD_REACH) { ldHit(g, i, dx); break; }
  }
  for (let i = 0; i < 2; i++) if (d.z * g.p[i].side > LD_OUT) { ldPoint(g, 1 - i); break; }
}
function ldHit(g, i, dx) {
  const p = g.p[i], d = g.d, off = Math.max(-1, Math.min(1, dx / LD_REACH)), a = off * LD_MAXA;
  d.spd = Math.min(LD_CAP, d.spd * LD_UP);
  p.streak++;
  const charged = p.streak >= 4;                         // after three returns in a row, the next one is charged
  if (charged) p.streak = 0;
  d.boost = charged ? LD_CHARGE : 1; d.charged = charged;
  d.vx = Math.sin(a) * d.spd; d.vz = -p.side * Math.cos(a) * d.spd;   // as in Pong: off-centre sends it on toward that side
  const curved = Math.abs(p.vx) > 1.0;
  d.curl = curved ? Math.max(-8, Math.min(8, p.vx)) * LD_CURVE : 0;
  d.z = p.z - p.side * .46; d.owner = i;
  p.swing = 1; p.hits++; g.rally++; g.p[1 - i].streak = 0;
  ldPlan(g);
  g.ev.push({ k: 'hit', i, charged, curved });
}
function ldPoint(g, w) {
  g.score[w]++; g.server = 1 - w; g.phase = 'point'; g.timer = 1.1;
  const [a, b] = g.score;
  if ((a >= g.target || b >= g.target) && Math.abs(a - b) >= 2) { g.over = true; g.winner = a > b ? 0 : 1; g.timer = 1.4; }
  g.log.push({ step: g.step, w, rally: g.rally });
  g.ev.push({ k: 'point', w });
}
function ldPaper(o) {   // a whole game with no drawing (disc_check, and crew games worked out off-screen)
  const g = ldNew(o);
  while (g.phase !== 'over' && g.step < 60 * 60 * 30) { ldStep(g, null); g.ev.length = 0; }
  return { score: g.score.slice(), steps: g.step, winner: g.winner, rallies: g.log.map(l => l.rally) };
}
// ---- on the rec deck: the court, the two baselines (places a crew visit can walk to), the saved record ----
const LD_COURT = [10.5, 15.5];                           // the court's centre in deck tiles: game z runs along deck x (+ is the bow), game x across it (+ is deck -z)
const ldWorld = (gx, gz) => ({ x: LD_COURT[0] + gz - OX, z: LD_COURT[1] - gx - OZ });
DECKS[7].places.push(
  { id: '7-disc-1', type: 'rec:disc', at: [16, 15], xy: [16.1, 15.5], face: 'w', pose: 'stand', room: 'C' },   // yours, at the bow end
  { id: '7-disc-2', type: 'rec:disc', at: [4, 15], xy: [4.9, 15.5], face: 'e', pose: 'stand', room: 'C' });    // theirs, at the stern end
function discLoad(s) {   // save.disc, read defensively (saves from before 0.82 have none)
  const d = s && s.disc && typeof s.disc === 'object' ? s.disc : {}, n = k => Number.isFinite(d[k]) && d[k] >= 0 ? Math.floor(d[k]) : 0, vs = {}, relDay = {};
  if (d.vs && typeof d.vs === 'object') for (const k in d.vs) { const v = d.vs[k]; if (Array.isArray(v) && v.length === 2 && k.length < 40) vs[k] = [Math.max(0, v[0] | 0), Math.max(0, v[1] | 0)]; }
  if (d.relDay && typeof d.relDay === 'object') for (const k in d.relDay) if (k.length < 40 && Number.isFinite(d.relDay[k])) relDay[k] = Math.floor(d.relDay[k]);
  return { played: n('played'), won: n('won'), lost: n('lost'), games: n('games'), taught: d.taught === true, vs, relDay, beatRina: Number.isFinite(d.beatRina) ? Math.floor(d.beatRina) : null };
}
SHIP.disc = discLoad(SAVED);
SAVE_EXTRA.push(s => { s.disc = JSON.parse(JSON.stringify(SHIP.disc)); });
// who'd come down and play: anyone aboard who's off or at leisure now, on any deck; nobody in quiet hours or with the deck shut
function discFind() {
  const now = shipNow(), m = ((now % 1440) + 1440) % 1440; if (m >= 1290 || m < DECKS[7].open[0] * 60) return null;
  const D = SHIP.disc; let best = null, bs = -1e9;
  for (const p of schedPeople()) {
    if (!p || !p.id || !ROSTER.some(x => x.id === p.id) || COME_TO.has(p.id) || CREW_HELD.has(p.id)) continue;
    if (typeof CHAT !== 'undefined' && CHAT && CHAT.p === p) continue;
    let w = null; try { w = whereIs(p, now); } catch (e) { w = null; }
    if (!w || w.act !== 'off' && w.act !== 'leisure') continue;
    const v = typeof VOICE !== 'undefined' && VOICE[p.id], likes = !!(v && Array.isArray(v.invites) && v.invites.some(x => /disc|lightdisc/i.test(x))) || !!D.vs[p.id] || !!LD_CREW[p.id];
    let tier = 0; try { tier = relTier(p.id) || 0; } catch (e) { tier = 0; }
    const sc = (likes ? 30 : 0) + tier * 8 + (w.deck === 7 ? 4 : 0) + schedU(idHash(p.id), SHIP.time.day, 832) * 3;   // a little seeded variety among equals
    if (sc > bs || sc === bs && best && p.id < best.id) { bs = sc; best = p; }
  }
  return best;
}
// ---- asking someone, the wait, the game, the end ----
const DISC = { g: null, opp: null, name: '', agent: null, view: null, cam: null, acc: 0, last: 0, inp: { tx: null, tz: null, kx: 0, kz: 0 }, how: -1, ease: null, quick: false };
Object.assign(PLAYER_ACTS, { disc: { need: null, mins: 30, pose: 'stand', title: 'Lightdisc', done: 'You step off the court.', until: A => discTick(A) } });
const LD_WAIT = 40;                                      // ship minutes to come down before they give up
function discAsk(who) {   // who: someone in particular (Winner Stays On's champion, 0.83.1 RA), else whoever discFind picks
  if (DISC.g) return;
  if (!recOpen()) { toast('Lightdisc', 'The rec deck\'s closed till six.'); return; }
  const p = who || discFind();
  if (!p) { toast('Lightdisc', 'Nobody\'s around to play right now. Try in the evening, or on a day off.'); return; }
  actStart('disc', '7-disc-1', { title: 'Lightdisc', st: 'wait', opp: p.id, since: shipNow(), here: false });
  const A = ACT; if (!A || A.kind !== 'disc') return;
  const go = crewComeTo(p, '7-disc-2', () => { A.o.here = true; }, { until: shipNow() + LD_WAIT + 60 }), prev = A.release;
  A.release = () => { if (prev) prev(); go(); };          // actEnd lets them go back to their own plans
  toast('Lightdisc', shortName(p) + ' is on the way down to play you. Wait on your baseline.');
}
function discTick(A) {   // the 'disc' activity: true ends it
  const o = A.o;
  if (o.st === 'play') return !DISC.g;
  const a = DECK_CREW.find(x => x.p && x.p.id === o.opp), sp = placeSpot('7-disc-2');
  if (a && a.settled && (o.here || sp && Math.hypot(a.x - sp.x, a.z - sp.z) < .6)) { o.st = 'play'; discBegin(a, false); return false; }
  if (shipNow() - o.since > LD_WAIT) { toast('Lightdisc', tlSecond(o.opp) + ' couldn\'t make it after all.'); return true; }
  return false;
}
function discBegin(a, quick) {
  const D = SHIP.disc; D.games++;
  DISC.opp = a.p.id; DISC.name = shortName(a.p); DISC.agent = a; DISC.quick = !!quick;
  DISC.short = DISC.name.split(' ').length > 1 && /^(Captain|Commander|Dr\.|Chief|Chef|Lt\.?|Lieutenant|Ensign)$/.test(DISC.name.split(' ')[0]) ? DISC.name.split(' ').pop() : DISC.name;   // on the score: Vance, not Commander Vance
  DISC.g = ldNew({ seed: Math.floor(schedU(D.games, SHIP.time.day, 830) * 4294967296), quick, you: null, them: ldLevel(a.p.id) });
  DISC.how = D.taught ? -1 : 0; DISC.moved = 0;
  discViewOn();
}
PAUSE.disc = () => !!(DISC.g && DISC.view);              // section 13: a game on (and its result) stops the ship's clock
function discOver() {   // the end of a game: the tally and what it gives
  const G = DISC.g, D = SHIP.disc, won = G.winner === 0, id = DISC.opp;
  D.played++; if (won) D.won++; else D.lost++;
  const v = D.vs[id] || (D.vs[id] = [0, 0]); v[won ? 0 : 1]++;
  D.taught = true;
  const once = D.relDay[id] !== SHIP.time.day ? 1 : .25;
  try {   // as for Tiles: the social in one go (no ship minutes passed), a quarter for later games with them that day; a little energy, some leisure
    const N = SHIP.player.needs, fx = playerFx();
    leisureAdd(10 * once, 'disc');
    N.social = needClamp(N.social + 12 * once * fxR(fx, 'social') * bondMult(id));
    N.energy = needClamp(N.energy - 3); N.fitness = needClamp(N.fitness + 10 * fxR(fx, 'fitness'));   // 0.82.5: fitness, about ten gym minutes a game
  } catch (e) { /* needs not there (checks on paper) */ }
  if (D.relDay[id] !== SHIP.time.day) {
    D.relDay[id] = SHIP.time.day;
    if (typeof relAdd === 'function') relAdd(id, 'disc', REL_PTS.chat || 2);
    if (typeof memAdd === 'function') memAdd(id, 'came.disc');
  }
  if (won && id === 'rina' && D.beatRina === null) {   // crew talk about a good win
    D.beatRina = SHIP.time.day;
    if (typeof newsAdd === 'function') newsAdd({ id: 'disc-rina-beaten', about: 'you', lines: ['Rina lost at Lightdisc! To the new hand!', 'Somebody beat Rina on the court.'], seed: ['rina', 'pell'], weight: .8, life: 6 });
  }
  if (typeof saveGame === 'function') saveGame();
}
function discEnd(again) {   // Again / Quick game / Done from the result, or Leave mid-game (not counted)
  const a = DISC.agent;
  if (again && a && DECK_CREW.includes(a)) { discViewOff(true); discBegin(a, again === 'quick'); return; }
  discViewOff(false);
  DISC.g = null; DISC.agent = null;
  if (ACT && ACT.kind === 'disc') actEnd();
}
onSim('newGame', () => { SHIP.disc = discLoad(null); if (DISC.view) discViewOff(false); DISC.g = null; DISC.agent = null; });
// ---- the game view: a perspective camera behind and above your baseline (the prototype's fit), the disc, its ring,
// trail and flashes, the live scoreboard, and the overlay (score, the paused clock, Leave, How to play, the result).
// Made when a game starts and freed when it ends: nothing here exists at load, so no kit and no R().
const LD_CSS = `
#ld{position:fixed;inset:0;z-index:60;touch-action:none;user-select:none;-webkit-user-select:none;font:15px/1.35 system-ui,-apple-system,sans-serif;color:#e8f2f5}
#ld .top{position:absolute;left:0;right:0;top:calc(env(safe-area-inset-top) + 8px);display:flex;flex-direction:column;align-items:center;gap:5px;pointer-events:none}
#ld .sc{background:rgba(5,8,14,.72);border:1px solid rgba(255,255,255,.14);border-radius:999px;padding:4px 14px;font-weight:600;font-variant-numeric:tabular-nums}
#ld .sc .a{color:#50e6ff}#ld .sc .b{color:#ffa03c}
#ld .pz{background:rgba(5,8,14,.72);border:1px solid #ffd166;color:#ffe3a3;border-radius:999px;padding:2px 12px;font-size:12.5px}
#ld button{font:inherit;color:#e8f2f5;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.18);border-radius:999px;padding:8px 16px;cursor:pointer}
#ld button.go{background:#0f3440;border-color:#50e6ff;color:#dffaff;font-weight:600}
#ld .lv{position:absolute;right:12px;bottom:calc(env(safe-area-inset-bottom) + 12px);font-size:13px;padding:6px 14px;background:rgba(5,8,14,.6)}
#ld .call{position:absolute;left:0;right:0;top:34%;text-align:center;font-size:22px;font-weight:700;text-shadow:0 0 12px rgba(0,0,0,.9);pointer-events:none}
#ld .tag,#ld .say{position:absolute;transform:translate(-50%,-100%);white-space:nowrap;pointer-events:none}
#ld .tag{font-size:12px;font-weight:600;padding:1px 7px;border-radius:6px;background:rgba(5,8,14,.55)}
#ld .say{font-size:13px;padding:4px 9px;border-radius:10px;background:#f3efe4;color:#1b1f24}
#ld .how{position:absolute;left:10px;right:10px;bottom:calc(env(safe-area-inset-bottom) + 50px);max-width:520px;margin:0 auto;display:flex;align-items:center;gap:8px;background:rgba(8,12,20,.92);border:1px solid #50e6ff;border-radius:14px;padding:9px 10px 9px 14px;pointer-events:none}
#ld .how .t{flex:1}#ld .how .n{color:#50e6ff;font-size:12px;display:block}#ld .how button{pointer-events:auto;padding:6px 12px;font-size:13px}
#ld .res{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;padding:16px}
#ld .card{background:rgba(8,12,20,.92);border:1px solid rgba(255,255,255,.14);border-radius:18px;padding:18px;width:100%;max-width:420px;box-sizing:border-box}
#ld .card h2{margin:0 0 4px;font-size:24px}#ld .card .s{color:#9fb2b8;font-size:13.5px}#ld .card .b{display:flex;flex-wrap:wrap;gap:10px;margin-top:14px}
#ld .hide{display:none!important}
body.ld-on .hud,body.ld-on .controls,body.ld-on #devBtn,body.ld-on #devMail,body.ld-on #needStrip,body.ld-on #devHu,body.ld-on #toast,body.ld-on #devTip{visibility:hidden}`;
const LD_HOW = [
  () => matchMedia('(pointer: coarse)').matches ? 'Put your thumb down and drag: you go where your thumb goes.' : 'Move the mouse, or use the arrow keys, to move.',
  () => 'No button to hit: stand in the disc\'s way and it goes back.',
  () => 'Be moving as the disc meets you and it curves that way.',
  () => 'Three returns in a row and your next one is charged.',
];
const LD_TALK = {   // fallbacks: the writers' lines (lineFor(who, 'disc.<kind>'), content/lines and banks/disc.lines) come first
  charged: { vance: ['By the book, Cadet.', 'Page forty: the charged return.', 'Keep up.'] },
  curve: { pell: ['Swerve!', 'Did you see that curve?', 'Where\'s it going? Who knows.'] },
  point: { rina: ['Fine.', 'Again?', 'You\'ll get there.'], holt: ['Steady.', 'Hm.', 'Straight and simple.'] },
  win: { rina: ['That\'s the game. Fine.'], holt: ['Good game, Cadet.'], vance: ['Regulation result.'], pell: ['Pell takes it!'] },
};
function discTalk(kind) {   // the opponent says something (a stream of its own, so talk never shifts the game)
  const G = DISC.g, V = DISC.view; if (!G || !V) return;
  let text = null; try { const l = typeof lineFor === 'function' && lineFor(DISC.opp, 'disc.' + kind, {}); text = l && l.text; } catch (e) { text = null; }
  const L = !text && LD_TALK[kind] && LD_TALK[kind][DISC.opp];
  if (!text && L) text = L[Math.floor(V.chat() * L.length)];
  if (text) V.say = { text, t: 2 };
}
const ldEl = (tag, cls, parent, text) => { const e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; if (parent) parent.appendChild(e); return e; };
function discGlow(ring) {   // a radial glow (or ring) texture, made when the view opens
  return tex(64, 64, (c, w, h) => {
    const r = c.createRadialGradient(32, 32, 0, 32, 32, 32);
    if (ring) { r.addColorStop(0, 'rgba(255,255,255,0)'); r.addColorStop(.62, 'rgba(255,255,255,0)'); r.addColorStop(.8, 'rgba(255,255,255,1)'); r.addColorStop(1, 'rgba(255,255,255,0)'); }
    else { r.addColorStop(0, 'rgba(255,255,255,1)'); r.addColorStop(.25, 'rgba(255,255,255,.55)'); r.addColorStop(1, 'rgba(255,255,255,0)'); }
    c.fillStyle = r; c.fillRect(0, 0, w, h);
  });
}
function discViewOn() {
  const V = DISC.view = { grp: new THREE.Group(), fx: [], chat: ldRng(DISC.g.seed ^ 0x5bd1e995), say: null, callT: 0, pulseT: 1, flashes: [], camT: 0, rm: matchMedia('(prefers-reduced-motion: reduce)').matches };
  const add = (m, mat) => { const o = new THREE.Mesh(m, mat); V.grp.add(o); return o; };
  const glow = discGlow(false), ring = discGlow(true); V.tex = [glow, ring];
  const basic = (c, o = {}) => new THREE.MeshBasicMaterial({ color: col(c), toneMapped: false, ...o });
  const addB = { transparent: true, depthWrite: false, blending: THREE.AdditiveBlending };
  V.discMat = basic('#ffffff'); V.disc = add(new THREE.CylinderGeometry(LD_R, LD_R, .05, 20), V.discMat);
  V.halo = new THREE.Sprite(new THREE.SpriteMaterial({ map: glow, color: col('#50e6ff'), ...addB, toneMapped: false })); V.halo.scale.setScalar(1.1); V.disc.add(V.halo);
  V.ringMat = basic('#ffffff', { transparent: true, opacity: .55, depthWrite: false }); V.ring = add(new THREE.RingGeometry(.24, .32, 24).rotateX(-Math.PI / 2), V.ringMat);
  const TRN = 14, tg = new THREE.BufferGeometry();
  tg.setAttribute('position', new THREE.Float32BufferAttribute(new Float32Array(TRN * 6), 3)); tg.setAttribute('color', new THREE.Float32BufferAttribute(new Float32Array(TRN * 6), 3));
  const idx = []; for (let i = 0; i < TRN - 1; i++) { const a = i * 2; idx.push(a, a + 1, a + 2, a + 1, a + 3, a + 2); } tg.setIndex(idx);
  V.trail = add(tg, new THREE.MeshBasicMaterial({ vertexColors: true, side: THREE.DoubleSide, toneMapped: false, ...addB })); V.trail.frustumCulled = false; V.TRN = TRN;
  V.pulse = new THREE.Sprite(new THREE.SpriteMaterial({ map: ring, color: col('#50e6ff'), ...addB, toneMapped: false })); V.pulse.visible = false; V.grp.add(V.pulse);
  for (let i = 0; i < 3; i++) { const f = new THREE.Sprite(new THREE.SpriteMaterial({ map: glow, color: col('#ffffff'), ...addB, toneMapped: false })); f.visible = false; f.scale.set(1.4, 1.1, 1); V.grp.add(f); V.flashes.push({ s: f, t: 1 }); }
  for (const o of V.grp.children) o.userData.noShadow = true;
  scene.add(V.grp);
  V.pose = [0, 1].map(() => ({ lx: 0, ph: 0, side: 1, swing: 0, pump: 0 }));
  const who = ROSTER.find(x => x.id === DISC.opp);
  if (who) { V.opp = new FullPerson(rosterSpec(who), who.id); V.opp.rig.root.traverse(o => { if (o.isMesh) o.castShadow = true; }); }
  V.cam = DISC.cam = new THREE.PerspectiveCamera(50, innerWidth / innerHeight, .3, 120);
  V.azWas = azT; azT = Math.PI / 2;                       // the cutaway drops the walls between the bow and you
  // the overlay
  if (!document.getElementById('ld-css')) { const s = ldEl('style', null, document.head, LD_CSS); s.id = 'ld-css'; }
  const R = V.root = ldEl('div', null, document.body); R.id = 'ld'; document.body.classList.add('ld-on');   // the game view owns the screen: nothing else on it
  const top = ldEl('div', 'top', R); V.sc = ldEl('div', 'sc', top); ldEl('div', 'pz', top, '⏸ The ship\'s clock is paused while you play');
  V.call = ldEl('div', 'call hide', R);
  V.tags = [ldEl('div', 'tag', R, 'You'), ldEl('div', 'tag', R, DISC.short)]; V.tags[0].style.color = '#9fe3ff'; V.tags[1].style.color = '#ffd2a0';
  V.sayEl = ldEl('div', 'say hide', R);
  V.leave = ldEl('button', 'lv', R, 'Leave'); V.leave.onclick = e => { e.stopPropagation(); discEnd(false); };
  V.how = ldEl('div', 'how hide', R); const ht = ldEl('div', 't', V.how); V.howN = ldEl('span', 'n', ht); V.howX = ldEl('span', null, ht);
  V.howNext = ldEl('button', null, V.how, 'Next'); V.howNext.onclick = e => { e.stopPropagation(); discHowDone(DISC.how); };
  ldEl('button', null, V.how, 'Skip').onclick = e => { e.stopPropagation(); DISC.how = -1; SHIP.disc.taught = true; discHowShow(); };
  V.res = ldEl('div', 'res hide', R);
  // input: where your thumb (or the mouse) is, you go; the keys too
  let drag = null; const inp = DISC.inp; inp.tx = inp.tz = null; inp.kx = inp.kz = 0;
  const aimX = cx => (cx / innerWidth * 2 - 1) * (LD_HX - .25) * 1.12;
  R.addEventListener('pointerdown', e => { if (e.target.tagName === 'BUTTON' || !DISC.g || DISC.g.over) return; drag = { id: e.pointerId, y0: e.clientY, z0: DISC.g.p[0].z }; inp.tx = aimX(e.clientX); try { R.setPointerCapture(e.pointerId); } catch (x) { /* fine */ } });
  R.addEventListener('pointermove', e => { if (!DISC.g) return; if (drag && drag.id === e.pointerId) { inp.tx = aimX(e.clientX); inp.tz = drag.z0 + (e.clientY - drag.y0) / innerHeight * 5; } else if (e.pointerType === 'mouse') inp.tx = aimX(e.clientX); });
  const lift = e => { if (drag && drag.id === e.pointerId) { drag = null; if (DISC.g && e.pointerType !== 'mouse') { inp.tx = DISC.g.p[0].x; inp.tz = DISC.g.p[0].z; } } };
  R.addEventListener('pointerup', lift); R.addEventListener('pointercancel', lift);
  const KEYS = { ArrowLeft: ['kx', -1], a: ['kx', -1], A: ['kx', -1], ArrowRight: ['kx', 1], d: ['kx', 1], D: ['kx', 1], ArrowUp: ['kz', -1], w: ['kz', -1], W: ['kz', -1], ArrowDown: ['kz', 1], s: ['kz', 1], S: ['kz', 1] };
  V.kd = e => { const k = KEYS[e.key]; if (k) { inp[k[0]] = k[1]; e.preventDefault(); e.stopPropagation(); } };
  V.ku = e => { const k = KEYS[e.key]; if (k && inp[k[0]] === k[1]) inp[k[0]] = 0; };
  addEventListener('keydown', V.kd, true); addEventListener('keyup', V.ku, true);
  // the camera eases in from your usual view (a dolly-zoom from the flat view), or cuts with reduced motion
  discFit();
  const from = new THREE.Vector3().subVectors(camera.position, target).normalize();
  V.ease = { t: V.rm ? 1 : 0, T0: target.clone(), d0: from, h0: (camera.top - camera.bottom) / camera.zoom, back: false };
  V.resize = () => discFit(); addEventListener('resize', V.resize);
  DISC.acc = 0; DISC.last = performance.now();
  discBoard(); discHowShow();
}
function discViewOff(keep) {   // keep: a new game follows at once (Again): the view's pieces are remade
  const V = DISC.view; if (!V) return;
  scene.remove(V.grp);
  V.grp.traverse(o => { if (o.geometry) o.geometry.dispose(); if (o.material) o.material.dispose(); });
  for (const t of V.tex) t.dispose();
  V.root.remove(); document.body.classList.remove('ld-on'); removeEventListener('keydown', V.kd, true); removeEventListener('keyup', V.ku, true); removeEventListener('resize', V.resize);
  azT = V.azWas; DISC.view = null; DISC.cam = null;
  if (V.opp) V.opp.dispose();
  const a = DISC.agent, sp = placeSpot('7-disc-2');      // they stand back on their baseline (their own body again); you on yours
  if (a && sp) { a.x = sp.x; a.z = sp.z; a.face = Math.PI / 2; a.h.set({ x: a.x, y: 0, z: a.z }, a.face, 'stand'); if (a.h.full) a.h.rig.root.visible = true; else crowd.update(0, 0); }
  const ys = placeSpot('7-disc-1'); if (ys) { player.obj.position.set(ys.x, 0, ys.z); player.face = -Math.PI / 2; }
  if (!keep) discBoard(true);
}
// the game view's camera, fitted as in the prototype: from about 55° (42° held sideways), lowered only as far as it
// must for the scoreboard to show above the far end; your player a fifth of the way up so your thumb sits below.
function discFit() {
  const V = DISC.view; if (!V) return;
  const asp = innerWidth / innerHeight, port = asp < 1, c = new THREE.PerspectiveCamera(50, asp, .3, 120), v = new THREE.Vector3(), dir = new THREE.Vector3();
  const ndc = (x, y, z) => v.set(x, y, z).project(c), goalY = port ? -.56 : -.5, boardTop = H - .11;
  const place = (dist, tz) => { c.position.set(0, 0, tz).addScaledVector(dir, dist); c.lookAt(0, 0, tz); c.updateMatrixWorld(); };
  let best = null;
  for (let deg = port ? 55 : 42; deg >= 30 && !best; deg--) for (const fov of port ? [52, 58] : [44, 50]) {
    if (best) break;
    const el = deg * Math.PI / 180; dir.set(0, Math.sin(el), Math.cos(el)); c.fov = fov; c.updateProjectionMatrix();
    for (let dist = 5; dist < 40; dist += .25) {
      let lo = -14, hi = LD_BASE;
      for (let k = 0; k < 40; k++) { const mid = (lo + hi) / 2; place(dist, mid); if (ndc(0, .9, LD_BASE).y > goalY) hi = mid; else lo = mid; }
      const tz = (lo + hi) / 2; place(dist, tz);
      if (Math.abs(ndc(0, .9, LD_BASE).y - goalY) > .01) continue;
      const w = Math.abs(ndc(LD_HX + .3, 0, LD_BASE + .4).x), top = ndc(0, port ? boardTop : boardTop - .5, -6.45).y, near = ndc(0, 0, LD_OUT + .2).y;
      if (w <= .98 && top <= (port ? .88 : .9) && near > -.98) { best = { dist, tz, el, fov }; break; }
    }
  }
  if (!best) best = { dist: 18, tz: 0, el: .8, fov: 50 };
  // game space to the deck: game z runs along deck x, game x along deck -z
  const tw = ldWorld(0, best.tz), cw = ldWorld(0, best.tz + best.dist * Math.cos(best.el));
  V.fit = { T: new THREE.Vector3(tw.x, 0, tw.z), P: new THREE.Vector3(cw.x, best.dist * Math.sin(best.el), cw.z), fov: best.fov };
  V.cam.aspect = asp; V.cam.updateProjectionMatrix();
}
function discBoard(reset) {   // the stern wall's scoreboard (WALL_KIT.recScoreboard's canvas), live while you play
  const t = REC_BOARD.tex; if (!t || !t.image) return;
  const c = t.image.getContext('2d'), w = t.image.width, h = t.image.height, G = DISC.g;
  const sa = reset || !G ? 0 : G.score[1], sb = reset || !G ? 0 : G.score[0];
  c.fillStyle = '#05070b'; c.fillRect(0, 0, w, h); c.strokeStyle = '#2a3340'; c.lineWidth = 6; c.strokeRect(3, 3, w - 6, h - 6);
  c.textAlign = 'center'; c.fillStyle = '#e8eef0'; c.font = '700 30px system-ui,sans-serif'; c.fillText(G && G.over && !reset ? 'FINAL' : 'LIGHTDISC', w / 2, 44);
  c.font = '800 112px system-ui,sans-serif'; c.fillStyle = '#ff9a3c'; c.fillText(String(sa), w * .27, 168); c.fillStyle = '#50e6ff'; c.fillText(String(sb), w * .73, 168);
  c.fillStyle = '#e8eef0'; c.font = '800 80px system-ui,sans-serif'; c.fillText(':', w / 2, 158);
  c.font = '600 20px system-ui,sans-serif'; c.fillStyle = '#ff9a3c'; c.fillText(reset || !G ? 'STERN' : DISC.short.toUpperCase(), w * .27, 204); c.fillStyle = '#50e6ff'; c.fillText(reset || !G ? 'BOW' : 'YOU', w * .73, 204);
  t.needsUpdate = true;
}
function discHowShow() {
  const V = DISC.view; if (!V) return;
  if (DISC.how < 0 || DISC.how > 3) { V.how.classList.add('hide'); return; }
  V.how.classList.remove('hide'); V.howN.textContent = 'How to play · ' + (DISC.how + 1) + ' of 4'; V.howX.textContent = LD_HOW[DISC.how]();
  V.howNext.textContent = DISC.how === 3 ? 'Done' : 'Next';
}
function discHowDone(k) { if (DISC.how !== k) return; DISC.how = k === 3 ? -1 : k + 1; if (DISC.how < 0) SHIP.disc.taught = true; discHowShow(); }
function discResult() {
  const V = DISC.view, G = DISC.g; if (!V) return;
  const won = G.winner === 0, hi = Math.max(...G.score), lo = Math.min(...G.score), v = SHIP.disc.vs[DISC.opp] || [0, 0];
  V.res.innerHTML = ''; const card = ldEl('div', 'card', V.res);
  ldEl('h2', null, card, won ? 'You win ' + hi + '–' + lo : DISC.name + ' wins ' + hi + '–' + lo);
  ldEl('div', 's', card, 'Your record against ' + DISC.name + ': ' + v[0] + '–' + v[1] + '. Longest rally: ' + Math.max(0, ...G.log.map(l => l.rally)) + '.');
  const b = ldEl('div', 'b', card);
  const btn = (t, f, go) => { const e = ldEl('button', go ? 'go' : null, b, t); e.onclick = ev => { ev.stopPropagation(); f(); }; };
  btn('Again', () => discEnd('full'), true); btn('Quick game', () => discEnd('quick')); btn('Done', () => discEnd(false));
  V.res.classList.remove('hide'); V.how.classList.add('hide'); V.leave.classList.add('hide');
}
// the players' moves (plan v5 section 8, "disc ready / side-step / return"), posed straight onto a full rig each frame:
// a low ready stance, quick side steps when moving across, a forehand or backhand throw on each return (right-handed:
// a disc on your left is a backhand), a fist pump on a point. a: { lx: speed toward the figure's own left (+x), side:
// where the disc is (+1 its left), swing 0..1 (1 at the return), pump 0..1, ph: the step phase }. Nothing here calls R().
function discPose(rig, a, T) {
  const TAU = Math.PI * 2, w = Math.min(1, Math.abs(a.lx) / 3), crouch = .1 + .02 * Math.sin(T * 3.1);
  const hipY = HIP_Y - crouch + Math.abs(Math.sin(a.ph * Math.PI)) * .03 * w;
  rig.hips.position.set(Math.sin(a.ph * Math.PI) * .03 * w * Math.sign(a.lx || 1), hipY, 0);
  rig.hips.rotation.set(0, 0, 0);
  for (let i = 0; i < rig.legs.length; i++) {
    const leg = rig.legs[i], lead = Math.sign(a.lx || 1) === leg.side;   // the leg on the side you're stepping toward leads
    const st = Math.sin(a.ph * TAU + (lead ? 0 : Math.PI)), lift = Math.max(0, st) * .08 * w;
    const ang = legIK(leg, ANK + lift - (hipY - HIP_OFF), .02);
    leg.thigh.rotation.z = leg.side * (.13 + .12 * w * (lead ? Math.max(0, st) : .3)); leg.ankle.rotation.x = -ang;
  }
  rig.torso.rotation.set(.18, 0, -.06 * w * Math.sign(a.lx));
  const sw = a.swing, back = a.side > 0;                 // the throwing arm is the right (side -1)
  rig.chest.rotation.set(0, (back ? .55 : -.55) * sw, 0); rig.head.rotation.set(-.12, (back ? -.4 : .4) * sw, 0);
  for (const arm of rig.arms) {
    let sx = -.55, ex = -1.15, sz = .28;                 // ready: both hands up in front
    if (arm.side < 0 && sw > 0) {
      if (back) { sx = L(-.55, -1.35, sw); ex = L(-1.15, -.25, sw); sz = L(.28, -.75, sw); }   // backhand: across the body and out
      else { sx = L(-.55, -1.55, sw); ex = L(-1.15, -.2, sw); sz = L(.28, .55, sw); }          // forehand: a long reach forward
    }
    if (a.pump > 0 && arm.side < 0) { const k = Math.min(1, a.pump * 3); sx = L(sx, -2.75 + .35 * Math.sin(T * 16), k); ex = L(ex, -1.35, k); sz = L(sz, .15, k); }
    arm.sh.rotation.set(sx, 0, arm.side * sz); arm.el.rotation.x = ex; arm.hand.rotation.x = 0;
  }
}
// once a frame from the main loop (frozen or not): the game's fixed steps on real time, then the scene
function discFrame() {
  const V = DISC.view, G = DISC.g; if (!V || !G) return;
  const now = performance.now(), rdt = Math.min(.1, (now - DISC.last) / 1000); DISC.last = now;
  const T = now / 1000;
  if (G.phase !== 'over') {
    DISC.acc += rdt; let n = 0;
    while (DISC.acc >= LD_DT && n < 6) {
      const ox = G.p[0].x;
      ldStep(G, DISC.inp); DISC.acc -= LD_DT; n++;
      if (DISC.how === 0) { DISC.moved += Math.abs(G.p[0].x - ox); if (DISC.moved > 1.6) discHowDone(0); }
      for (const e of G.ev) discEvent(e);
      G.ev.length = 0;
    }
    if (n === 6) DISC.acc = 0;
  }
  // the people: you and your opponent where the game has you, animated (discPose) on full rigs
  G.p.forEach((p, i) => {
    const w = ldWorld(p.x, p.z), face = i ? Math.PI / 2 : -Math.PI / 2, lx = i ? p.vx : -p.vx, dx = i ? G.d.x - p.x : p.x - G.d.x, A = V.pose[i];
    A.lx += (lx - A.lx) * Math.min(1, rdt * 12); A.ph += Math.abs(A.lx) * rdt * 1.6; A.swing = p.swing; A.pump = Math.max(0, A.pump - rdt);
    if (p.swing > .95) A.side = Math.sign(dx) || 1;      // which side the disc was on as it came: forehand or backhand
    const body = i ? V.opp : ACT && ACT.kind === 'disc' && ACT.body;   // you: the activity's stand-in (section 15 hides player.obj while you're at one)
    if (!i) { player.obj.position.set(w.x, 0, w.z); player.face = face; if (ACT && ACT.kind === 'disc') { ACT.x = w.x; ACT.z = w.z; ACT.face = face; } }
    const rig = body ? body.rig : !i && player.rig, root = body ? body.rig.root : player.obj;
    if (!rig) return;
    root.position.set(w.x, 0, w.z); root.rotation.y = face;
    discPose(rig, A, T);
  });
  const a = DISC.agent;                                  // their own (crowd or full) body stays out of sight while the game's rig plays
  if (a && DECK_CREW.includes(a)) { if (a.h.full) a.h.rig.root.visible = false; else { a.h.set({ x: a.x, y: -40, z: a.z }, a.face, 'stand'); crowd.update(rdt, T); } }
  // the disc, its ring and trail
  const d = G.d, w = ldWorld(d.x, d.z), live = G.phase === 'live' || G.phase === 'serve', dc = d.charged ? '#ffffff' : d.owner === 0 ? '#50e6ff' : '#ffa03c';
  V.disc.visible = V.ring.visible = G.phase !== 'over';
  V.disc.position.set(w.x, .9 + (G.phase === 'serve' && !V.rm ? Math.sin(T * 8) * .06 : 0), w.z); V.disc.rotation.y += rdt * 12;
  V.discMat.color.copy(col(d.charged ? '#ffffff' : d.owner === 0 ? '#d8fbff' : '#ffe6cc'));
  V.halo.material.color.copy(col(dc)); V.halo.scale.setScalar(d.charged ? 1.8 : 1.15);
  V.ring.position.set(w.x, .03, w.z); V.ringMat.color.copy(col(dc));
  const pa = V.trail.geometry.attributes.position.array, ca = V.trail.geometry.attributes.color.array, tc = col(dc), tr = G.phase === 'live' ? G.trail : [];
  const pt = i => { const k = Math.min(i, tr.length / 2 - 1) * 2; return tr.length ? ldWorld(tr[k], tr[k + 1]) : w; };
  for (let i = 0; i < V.TRN; i++) {
    const a = pt(i), b = pt(i + 1); let nx = -(b.z - a.z), nz = b.x - a.x; const nl = Math.hypot(nx, nz) || 1; nx /= nl; nz /= nl;
    const wd = LD_R * (1 - i / V.TRN) * (d.charged ? 1.4 : 1), k = tr.length ? (1 - i / V.TRN) * (d.charged ? 1 : .6) : 0;
    pa.set([a.x + nx * wd, .9, a.z + nz * wd, a.x - nx * wd, .9, a.z - nz * wd], i * 6);
    ca.set([tc.r * k, tc.g * k, tc.b * k, tc.r * k, tc.g * k, tc.b * k], i * 6);
  }
  V.trail.geometry.attributes.position.needsUpdate = V.trail.geometry.attributes.color.needsUpdate = true;
  if (V.pulse.visible) { V.pulseT += rdt / .3; V.pulse.scale.setScalar(.6 + V.pulseT * 2.2); V.pulse.material.opacity = Math.max(0, 1 - V.pulseT); if (V.pulseT >= 1) V.pulse.visible = false; }
  for (const f of V.flashes) if (f.s.visible) { f.t += rdt / .35; f.s.material.opacity = Math.max(0, 1 - f.t); if (f.t >= 1) f.s.visible = false; }
  // the camera: eased in (or out) as a dolly-zoom from the flat view, then the fitted game view
  const E = V.ease, F = V.fit, cam = V.cam;
  E.t = Math.min(1, E.t + rdt / .8); const e = E.t * E.t * (3 - 2 * E.t), k = E.back ? 1 - e : e;
  const d1 = F.P.distanceTo(F.T), h1 = 2 * d1 * Math.tan(F.fov * Math.PI / 360), D0 = 200;
  const dist = Math.exp(Math.log(D0) + (Math.log(d1) - Math.log(D0)) * k), h = E.h0 + (h1 - E.h0) * k;
  const dir = E.d0.clone().lerp(F.P.clone().sub(F.T).normalize(), k).normalize(), tgt = E.T0.clone().lerp(F.T, k);
  cam.position.copy(tgt).addScaledVector(dir, dist); cam.fov = 2 * Math.atan(h / 2 / dist) * 180 / Math.PI;
  cam.near = Math.max(.3, dist - 40); cam.far = dist + 40; cam.aspect = innerWidth / innerHeight; cam.updateProjectionMatrix(); cam.lookAt(tgt);
  if (E.back && E.t >= 1) { const f = E.done; E.done = null; DISC.cam = null; if (f) f(); return; }
  // labels and talk
  const v = new THREE.Vector3(), at = (x, y, z, el) => { v.set(x, y, z).project(cam); if (v.z > 1) { el.classList.add('hide'); return; } el.style.left = ((v.x + 1) / 2 * innerWidth) + 'px'; el.style.top = ((1 - v.y) / 2 * innerHeight) + 'px'; el.classList.remove('hide'); };
  const show = E.t >= 1 && G.phase !== 'over';
  G.p.forEach((p, i) => { const q = ldWorld(p.x, p.z); if (show) at(q.x, 2.1, q.z, V.tags[i]); else V.tags[i].classList.add('hide'); });
  if (V.say && (V.say.t -= rdt) > 0 && show) { const q = ldWorld(G.p[1].x, G.p[1].z); V.sayEl.textContent = V.say.text; at(q.x, 2.85, q.z, V.sayEl); } else { V.say = null; V.sayEl.classList.add('hide'); }
  if (V.callT > 0 && (V.callT -= rdt) <= 0) V.call.classList.add('hide');
  V.sc.innerHTML = '<span class="a">You ' + G.score[0] + '</span> · <span class="b">' + G.score[1] + ' ' + DISC.short + '</span>' + (G.target === 5 ? ' <small style="color:#9fb2b8">to 5</small>' : '');
}
function discEvent(e) {
  const V = DISC.view, G = DISC.g;
  if (e.k === 'hit') {
    const p = G.p[e.i], q = ldWorld(G.d.x, G.d.z);
    if (!V.rm) { V.pulse.visible = true; V.pulseT = 0; V.pulse.position.set(q.x, .9, q.z); V.pulse.material.color.copy(col(e.i === 0 ? '#50e6ff' : '#ffa03c')); }
    if (e.i === 1) { if (e.charged) discTalk('charged'); else if (e.curved && V.chat() < .35) discTalk('curve'); }
    if (e.i === 0 && !p.ai) { if (DISC.how === 1) discHowDone(1); else if (DISC.how === 2 && e.curved) discHowDone(2); else if (DISC.how === 3 && e.charged) discHowDone(3); }
  }
  if ((e.k === 'wall' || e.k === 'net') && !V.rm) {
    const f = V.flashes.find(x => !x.s.visible) || V.flashes[0], q = ldWorld(e.k === 'wall' ? e.side * LD_HX : e.x, e.k === 'wall' ? e.z : 0);
    f.s.visible = true; f.t = 0; f.s.position.set(q.x, .7, q.z); f.s.material.color.copy(col(e.k === 'net' ? '#e8f4ff' : e.z > 0 ? '#50e6ff' : '#ffa03c'));
  }
  if (e.k === 'point') {
    discBoard(); V.pose[e.w].pump = 1.2;                 // a fist pump
    V.call.textContent = G.over ? (e.w === 0 ? 'Game: You' : 'Game: ' + DISC.short) : 'Point: ' + (e.w === 0 ? 'You' : DISC.short);
    V.call.style.color = e.w === 0 ? '#50e6ff' : '#ffa03c'; V.call.classList.remove('hide'); V.callT = 1.1;
    if (e.w === 1) { if (G.over) discTalk('win'); else if (V.chat() < .45) discTalk('point'); } else if (G.over) discTalk('lose');   // lose: W3's disc.lose (0.83.2)
  }
  if (e.k === 'over') { discOver(); discBoard(); discResult(); }
}

