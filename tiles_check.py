# Starship Cadet: Tiles check (keep in the repo, next to the other checks)
# Checks section 23 (the Tiles engineer): the Tiles game of plans/tiles-plan.html.
#   the rules: a mirrored deal with no three of a mark touching; the teaching layout; step, jump (the tile goes to the
#   hold), launch (home rows only); a dock after any move; the worked turn from the plan page, move for move
#   balance on paper, the plan's targets, for the full game (to 7) and the quick game (to 5, equal turns):
#   first player 48-52% at every crew level (allowing for sampling noise: the 95% band has to reach the target) (the quick game allows 53%, see the plan's Decided section), draws
#   under 1%, games under 24 turns (quick: under 16); tie-break wins reported by seat
#   skill: Hard beats Medium and Medium beats Easy more than 60% of the time, from both seats
#   the same seed plays the same game twice; crew styles are the same every time (Rina hard, Tomas easy)
#   section 23 never calls R() or Math.random and declares no top-level TILES; the page has no errors
#   the board (0.46.1): tilesPlay opens the Tiles app on the device; 36 squares at least 44px on a 320px phone and a
#   390px one, no text under 15px, no sideways scroll; tap a tile and its squares glow, tap one to move; the crew
#   member answers; a whole game played by taps ends with the result, Again / Quick game / Done, and a 'tiles' note;
#   the first game uses the teaching layout and points at a jump; opening it adds nothing to the 3D scene
#   sitting down (0.46.2, 0.46.4, 0.28.51): the Tiles station always, tables and boards only on Tiles night (else a plain seat);
#   you sit (the 'tiles' activity, sit:play) and a free crew member comes over (a visit) and sits opposite, and the game
#   opens; someone already at the table plays you at once; nobody free (quiet hours): a toast says so and you just sit;
#   playing stops ship time and a deck tap brings the board back; time runs again once it's over; How to play on your
#   first game (Next, by itself as you select and step, Skip, again from the board and the Tiles app; every step about
#   two lines); the game's social at its end (a quarter for later games with the same person that day, 0.28.54); Done and Leave game stand you up; walking
#   away leaves a game uncounted; a game adds friendship and a memory once a day per opponent; who goes first turns
#   about with each opponent (saved); beating Rina is news, once; save.tiles round-trips
#   Tiles night (0.46.3): tilesNight(day, came) pairs everyone (one watches when odd), the same every time; Rina always
#   has a game and wins it until you beat her; 2000 nights of rolls match the levels' odds; the end of the tradition
#   (simNote('tradition', { id: 'tilesNight' })) posts the news once and counts Rina's Tuesdays; the Tiles app shows it
# Setup and environment as for cadet_test.py.
# Run:  python3 tiles_check.py BUILD.html [GAMES]   (GAMES per level and mode, default 4000; Hard plays half as many)
import sys, json, re
exec(open(__file__.replace('tiles_check.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright

ok = True
def check(cond, msg):
    global ok
    if not cond: ok = False; print('FAIL', msg)
    return cond

def section23(src):
    i = src.find('// 23. TILES'); j = src.find('// 6. CAMERA', i)
    return src[i:j] if i >= 0 and j > i else ''

# plan page coordinates: a-f across, 1-6 up from your side; cell = y * 6 + x
def cell(s): return (int(s[1]) - 1) * 6 + 'abcdef'.index(s[0])

RULES = r"""(() => {
  const out = {}, P = 0, T = 1, at = s => (+s[1] - 1) * 6 + 'abcdef'.indexOf(s[0]);
  // the deal: mirrored, no group of three, 12 a side
  let bad = 0, mirror = 0;
  for (let g = 0; g < 300; g++) {
    const b = tilesDeal(tilesRng(77 + g), false);
    if (b.some((t, i) => t && tilesGroup(b, i).length >= 3)) bad++;
    for (let i = 0; i < 36; i++) { const t = b[i], u = b[35 - i]; if ((t && !u) || (t && (tlM(t) !== tlM(u) || tlO(t) === tlO(u)))) { mirror++; break; } }
    if (b.filter(t => t && tlO(t) === 0).length !== 12 || b.filter(t => t && tlO(t) === 1).length !== 12) bad++;
  }
  out.deal = { bad, mirror };
  const teach = tilesDeal(tilesRng(1), true);
  out.teach = { rows: [teach.slice(0, 6).map(tlM), teach.slice(6, 12).map(tlM)], groups: teach.some((t, i) => t && tilesGroup(teach, i).length >= 2) };
  // the worked turn (plan page, 'A worked turn')
  const b = new Array(36).fill(0), put = (c, o, m) => { b[at(c)] = tlT(o, m); };
  put('c6', T, 0); put('f6', T, 1); put('b5', T, 1); put('d5', T, 2); put('c4', P, 1); put('e4', T, 0);
  put('b3', P, 0); put('e2', P, 1); put('a1', P, 2); put('b1', P, 2); put('d1', P, 0);
  let s = { b, hold: [[], []], sc: [0, 0], p: 0, plies: 10, last: -1, mode: 'full', over: false, win: -1, why: '', reached: -1 };
  const ms = tilesMoves(s, 0), jump = ms.find(m => m.k === 'j' && m.from === at('c4') && m.to === at('e6'));
  out.jump = jump ? { to: jump.to, over: jump.over } : null;
  let r = tilesStep(s, jump); out.afterJump = { hold: r.s.hold[0], taken: r.take, sc: r.s.sc.slice(), d5: r.s.b[at('d5')] };
  const step = tilesMoves(r.s, 1).find(m => m.k === 's' && m.from === at('c6') && m.to === at('d5'));
  r = tilesStep(r.s, step);
  const launches = tilesMoves(r.s, 0).filter(m => m.k === 'l');
  out.launchRows = [...new Set(launches.map(m => m.to / 6 | 0))].sort();
  r = tilesStep(r.s, launches.find(m => m.to === at('c1') && m.m === 2));
  out.dock = { pts: r.pts, cells: r.dock.slice().sort((a, c) => a - c), sc: r.s.sc.slice(), left: [at('a1'), at('b1'), at('c1')].map(c => r.s.b[c]) };
  // a step onto a group docks too, and a step never goes backwards or straight
  const b2 = new Array(36).fill(0); b2[at('c2')] = tlT(0, 0); b2[at('c3')] = tlT(0, 0); b2[at('e2')] = tlT(0, 0); b2[at('a6')] = tlT(1, 1);
  const s2 = Object.assign({}, s, { b: b2, plies: 0 }), st = tilesMoves(s2, 0).filter(m => m.from === at('e2'));
  out.steps = st.map(m => m.to).sort((a, c) => a - c);
  out.stepDock = tilesApply(s2, st.find(m => m.to === at('d3'))).pts;
  // the quick game: the first player reaching 5 gives the second one last turn; the full game ends at once at 7
  const b3 = new Array(36).fill(0); b3[at('a1')] = tlT(0, 1); b3[at('b1')] = tlT(0, 1); b3[at('a6')] = tlT(1, 0); b3[at('f6')] = tlT(1, 2);
  let q = { b: b3, hold: [[1], []], sc: [2, 2], p: 0, plies: 4, last: -1, mode: 'quick', over: false, win: -1, why: '', reached: -1 };
  q = tilesStep(q, tilesMoves(q, 0).find(m => m.k === 'l' && m.to === at('c1'))).s;
  const mid = { sc: q.sc.slice(), over: q.over, p: q.p };
  q = tilesStep(q, tilesMoves(q, 1)[0]).s;
  let f = Object.assign({}, { b: b3.slice(), hold: [[1], []], sc: [4, 2], p: 0, plies: 4, last: -1, mode: 'full', over: false, win: -1, why: '', reached: -1 });
  f = tilesStep(f, tilesMoves(f, 0).find(m => m.k === 'l' && m.to === at('c1'))).s;
  out.quick = { mid, end: { over: q.over, win: q.win, why: q.why }, full: { over: f.over, win: f.win, sc: f.sc } };
  return out;
})()"""

BAL = r"""((mode, games, seed) => {
  const out = {};
  for (const lv of ['easy', 'medium', 'hard']) {
    const n = lv === 'hard' ? Math.ceil(games / 2) : games; let w = [0, 0, 0], pl = 0, tie = [0, 0], cb = 0, behind = 0;
    for (let g = 0; g < n; g++) {
      const s = tilesSimGame(mode, lv, lv, seed + g); w[s.win < 0 ? 2 : s.win]++; pl += s.plies;
      if (s.why.indexOf('tie') >= 0 && s.win >= 0) tie[s.win]++;
    }
    out[lv] = { n, p1: w[0] / n, draw: w[2] / n, plies: pl / n, tie };
  }
  for (const [a, c] of [['hard', 'medium'], ['medium', 'easy']]) {
    const n = Math.ceil(games / 6); let wa = 0;
    for (let g = 0; g < n; g++) { if (tilesSimGame(mode, a, c, seed + 50000 + g).win === 0) wa++; if (tilesSimGame(mode, c, a, seed + 90000 + g).win === 1) wa++; }
    out[a + '>' + c] = wa / (2 * n);
  }
  return out;
})"""


UI_PLAY = r"""(() => {
  const out = { log: [] }, bd = () => document.querySelector('#devBody .tlx .tl-bd');
  window.__tn = []; if (!window.__tnOn) { window.__tnOn = true; onSim('tiles', d => window.__tn.push(d)); }
  const G = TL_GAME; out.teach = G.teach && JSON.stringify(G.s.b.slice(0, 12).map(tlM)) === JSON.stringify(TL_TEACH);
  out.cells = bd() ? bd().querySelectorAll('.tl-c').length : 0;
  // tap a tile that can move: its squares glow; tap one: the move is made, and it's the crew's turn
  const ms = tilesMoves(G.s, 0), m = ms.find(x => x.k === 's');
  bd().querySelector(`.tl-c[data-c="${m.from}"]`).click();
  out.glow = [...bd().querySelectorAll('.tl-c.to')].map(b => +b.dataset.c).sort((a, c) => a - c);
  out.want = ms.filter(x => x.from === m.from).map(x => x.to).sort((a, c) => a - c);
  bd().querySelector(`.tl-c[data-c="${m.to}"]`).click();
  out.moved = G.s.b[m.to] !== 0 && G.s.b[m.from] === 0 && G.s.p === 1;
  if (G.timer) { clearTimeout(G.timer); G.timer = 0; } tilesCrewMove();
  out.answered = G.s.p === 0 && G.s.plies === 2;
  // the rest of the game by taps (the player plays Medium's choice through the board, the crew answer at once)
  let guard = 0;
  while (!G.s.over && guard++ < 80) {
    if (G.s.p === 1) { if (G.timer) { clearTimeout(G.timer); G.timer = 0; } tilesCrewMove(); continue; }
    const mv = tilesAI(G.s, 'medium', tilesRng(guard));
    if (mv.k === 'l') document.querySelector(`#devBody .tl-hd button[data-h="${mv.m}"]`).click();
    else bd().querySelector(`.tl-c[data-c="${mv.from}"]`).click();
    bd().querySelector(`.tl-c[data-c="${mv.to}"]`).click();
  }
  if (G.timer) { clearTimeout(G.timer); G.timer = 0; }
  out.over = G.s.over; out.sc = G.s.sc; out.win = G.s.win;
  out.end = [...document.querySelectorAll('#devBody .tl-end button')].map(b => b.textContent);
  out.now = document.querySelector('#devBody .tl-now').textContent;
  out.note = window.__tn.length; out.played = SHIP.tiles.played;
  return out;
})()"""
LOOKS = r"""(() => {
  const dev = document.getElementById('devBody'), cells = [...dev.querySelectorAll('.tl-c')].map(b => b.getBoundingClientRect());
  const small = [...dev.querySelectorAll('.tlx *')].filter(e => e.offsetParent !== null && [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()) && parseFloat(getComputedStyle(e).fontSize) < 15).map(e => e.textContent.slice(0, 20));
  return { minCell: Math.min(...cells.map(r => Math.min(r.width, r.height))), small: small.slice(0, 3), scroll: dev.scrollWidth - dev.clientWidth };
})()"""

def board(g, path):
    for name, w, h in (('phone 320', 320, 640), ('phone 390', 390, 844), ('wide', 1280, 800)):
        gg = Game(g, path, w, h); gg.step(3)
        MEM = "[scene.children.length, renderer.info.memory.geometries, renderer.info.memory.textures]"
        gg.ev("SHIP.device.tipsSeen.device = true; deviceShow('home')"); gg.step(2)   # the device's own first open uploads its prop once
        m0 = gg.ev(MEM)
        gg.ev("tilesPlay('tomas', null, 'full')"); gg.step(2)
        lk = gg.ev(LOOKS)
        check(lk['minCell'] >= 44 and not lk['small'] and lk['scroll'] <= 0, f'{name}: squares at least 44px ({lk["minCell"]:.1f}), no text under 15px {lk["small"]}, no sideways scroll ({lk["scroll"]})')
        check(gg.ev(MEM) == m0, f'{name}: opening the board adds nothing to the 3D scene')
        if name == 'phone 390':
            r = gg.ev(UI_PLAY)
            check(r['teach'] and r['cells'] == 36, f'the first game: teaching layout, 36 squares: {r["teach"]}, {r["cells"]}')
            check(r['glow'] == r['want'] and r['glow'], f'tapping a tile lights its squares: {r["glow"]} (want {r["want"]})')
            check(r['moved'] and r['answered'], f'tapping a lit square moves it; the crew member answers: {r["moved"]}, {r["answered"]}')
            check(r['over'] and r['end'] == ['Again', 'Quick game (to 5)', 'Done'] and r['note'] == 1 and r['played'] == 1, f'a whole game by taps: over, result and buttons, one tiles note: {r}')
            print(f'  a game by taps: {r["sc"][0]}-{r["sc"][1]}, "{r["now"]}"')
            gg.page.click('#devBody .tl-end button[data-end="quick"]'); gg.step(1)
            q = gg.ev("[TL_GAME.s.mode, TL_GAME.teach, TL_GAME.s.p, TL_GAME.s.first]")
            check(q[0] == 'quick' and not q[1] and q[3] == 1, f'Quick game: to 5, no teaching, the crew member goes first in your second game: {q}')
            gg.ev("if (TL_GAME.timer) { clearTimeout(TL_GAME.timer); TL_GAME.timer = 0; }")
            gg.page.click('#devClose'); gg.step(1)
        check(not gg.errors and not gg.ev("DEV.errors.length"), f'{name}: no errors: {gg.errors[:3]} {gg.ev("DEV.errors.slice(0, 3)")}')
        gg.close()

SEAT = r"""((stage) => {
  const its = ITEMS.filter(i => /^Tiles table$/.test(i.t)); if (!its.length) return { none: true };
  const it = its[0]; it.hit.getWorldPosition(_wp); const at = _wp.clone();
  const g = nearestOpen(at.x, at.z, player); player.obj.position.copy(cellPos(...g)); player.stop();
  if (stage) {   // a crew member settled on one of the stools (stand-in for the evening crowd)
    const a = DECK_CREW.find(x => x.p && x.p.id === stage) || DECK_CREW.find(x => x.p && x.p.id);
    window.__opp = a.p.id; window.__oppA = a; a.goalId = '4-common-8'; a.settled = true;
  }
  const r = playerTap(it, at.clone(), at.clone());
  return { tapped: r, act: ACT && [ACT.kind, ACT.placeId, ACT.o.opp], toast: document.getElementById('tx').textContent };
})"""

FINISH = """(() => { const G = TL_GAME; G.style = Object.assign({}, G.style, { level: 'easy' }); let n = 0;
      while (!G.s.over && n++ < 80) { if (G.timer) { clearTimeout(G.timer); G.timer = 0; } if (G.s.p === 0) tilesDo(tilesAI(G.s, 'hard', G.rng)); else tilesCrewMove(); }
      if (G.timer) { clearTimeout(G.timer); G.timer = 0; } })()"""
SEATED = "!!(ACT && ACT.kind === 'tiles' && ACT.phase === 'do' && TL_GAME)"
def wait_for(gg, cond, n=60, k=10):
    for _ in range(n):
        gg.step(k)
        if gg.ev(cond): return True
    return False

def seat(pw, path):
    gg = Game(pw, path, 390, 844); gg.step(3)
    r = gg.ev(SEAT + "('rina')")
    if r.get('none'): check(False, 'the Deck 4 Tiles table is there'); gg.close(); return
    check(r['act'] and r['act'][0] == 'tiles', f'the junior common room\'s Tiles table plays any time, not only on Tiles night (0.28.62): {r}')
    gg.ev("actEnd(true); tilesNightNow = () => true")   # Tiles night from here on (stand-in for section 18's tradition)
    # 0.28.51: you sit down, and a free crew member walks over and sits opposite (the user's "You sit down and someone will come up if available")
    gg.ev("setShipNow((SHIP.time.day - 1) * 1440 + 19 * 60); for (const a of DECK_CREW) a.settled = false"); gg.step(60)
    r = gg.ev(SEAT + "(null)")
    check(r['act'] and r['act'][0] == 'tiles' and not r['act'][2], f'nobody at the table: you go to sit, with nobody named yet: {r}')
    came = wait_for(gg, "!!(ACT && ACT.o.st === 'wait')", 40)
    w = gg.ev("[ACT && ACT.o.opp, ACT && ACT.o.seat, ACT && ACT.placeId, document.getElementById('tx').textContent, (() => { const p = ROSTER.find(x => x.id === (ACT && ACT.o.opp)); const w = p && whereIs(p, shipNow()); return w && w.act; })()]")
    check(came and w[0] and w[1] != w[2] and 'comes over to play' in w[3] and w[4] == 'visit', f'once you sit, someone free comes over to the other seat: {w}')
    ok_on = wait_for(gg, SEATED, 80)
    st = gg.ev("(() => { const a = DECK_CREW.find(x => x.p && x.p.id === TL_GAME.opp), sp = placeSpot(ACT.o.seat); return [ACT.phase, ACT.pose, TL_GAME.opp, TL_GAME.where === ACT.placeId, DEV.open, DEV.app, !!a && Math.hypot(a.x - sp.x, a.z - sp.z) < .8, !!a && a.settled]; })()")
    check(ok_on and st[2] == w[0] and st[3] and st[4] and st[5] == 'tiles' and st[6] and st[7], f'they sit opposite and the game opens on the device: {st}')
    # playing stops time (the user's "Playing tiles stops time"); a tap on the deck brings the board back
    t0 = gg.ev("[SHIP.time.min, FREEZE.frozen, SHIP.player.needs.social, (SHIP.rel[TL_GAME.opp] || {}).pts || 0]"); gg.ev("deviceClose()"); gg.step(150)
    gg.page.mouse.click(195, 300); gg.step(2)
    t1 = gg.ev("[SHIP.time.min, FREEZE.frozen, DEV.open, DEV.app, document.getElementById('tx').textContent]")
    check(t1[0] == t0[0] and t0[1] and t1[1], f'while you play, ship time stands still (5 seconds: {t0[0]} -> {t1[0]})')
    check(t1[2] and t1[3] == 'tiles' and 'is waiting' in t1[4], f'a tap on the deck mid-game brings the board back: {t1[2:]}')
    # How to play: your first game runs it; steps move on with Next, and by themselves when you do the thing
    tu = gg.ev("""(() => { const G = TL_GAME, txt = () => { const e = document.querySelector('#devBody .tl-tut'); return e && !e.hidden ? e.textContent : ''; }, out = [G.tut, txt()];
      document.querySelector('#devBody .tl-tut button[data-end="tnext"]').click(); out.push(G.tut);
      document.querySelector('#devBody .tl-tut button[data-end="tnext"]').click(); out.push(G.tut, txt());
      const c = G.s.b.findIndex((t, i) => t && tlO(t) === 0 && tilesMoves(G.s, 0).some(m => m.from === i)); tilesTap(c); out.push(G.tut);
      const mv = tilesMoves(G.s, 0).find(m => m.from === c && m.k === 's'); tilesTap(mv.to); out.push(G.tut);
      if (G.timer) { clearTimeout(G.timer); G.timer = 0; } tilesCrewMove(); if (G.timer) { clearTimeout(G.timer); G.timer = 0; }
      document.querySelector('#devBody .tl-tut button[data-end="tskip"]').click(); out.push(G.tut, txt(), !!document.querySelector('#devBody .tl-play button[data-end="teach"]'));
      document.querySelector('#devBody .tl-play button[data-end="teach"]').click(); out.push(G.tut, txt().slice(0, 4));
      const long = TL_TUT.map(x => x.t('Olu', TL_MODES.full)).filter(t => t.length > 62); out.push(long, SHIP.tiles.taught);
      G.tut = -1; tilesDraw(); return out; })()""")
    print('  How to play:', tu)
    check(tu[0] == 0 and tu[1].startswith('1/8') and tu[2] == 1 and tu[3] == 2 and tu[4].startswith('3/8'), f'the first game opens How to play at step 1; Next moves on: {tu[:5]}')
    check(tu[5] == 3 and tu[6] == 4, f'selecting a tile and stepping it move the walkthrough on by themselves: {tu[5:7]}')
    check(tu[7] == -1 and tu[8] == '' and tu[9] and tu[10] == 0 and tu[11].startswith('1/8'), f'Skip ends it; How to play on the board runs it again: {tu[7:12]}')
    check(not tu[12] and tu[13] is True, f'every step fits in about two lines on a phone (62 characters), and the save knows you were taught: {tu[12:]}')
    gg.ev(FINISH)
    res = gg.ev("[TL_GAME.s.win, SHIP.tiles.played, SHIP.tiles.won, SHIP.tiles.firstWin !== null, (SHIP.rel[TL_GAME.opp] || {}).pts || 0, (SHIP.mem[TL_GAME.opp] || []).map(m => m[0]), SHIP.player.needs.social, TL_GAME.opp]")
    gg.ev(f"window.__opp = {json.dumps(res[7])}")
    print(f'  seated game against {res[7]}: win {res[0]}, tally {res[1:4]}, friendship {res[4]}, memories {res[5]}, social {t0[2]:.1f} -> {res[6]:.1f}')
    check(res[1] == 1 and (res[0] != 0 or (res[2] == 1 and res[3])), f'the tally counts the game: {res}')
    check(res[4] > t0[3] and 'came.tiles' in res[5], f'a game adds friendship and a memory: {res}')
    check(res[6] >= min(100, t0[2] + 9), f'the game\'s social comes when it ends (no ship minutes passed): {t0[2]} -> {res[6]}')
    gg.step(30); t2 = gg.ev("[SHIP.time.min, FREEZE.frozen]")
    check(t2[0] > t1[0] and not t2[1], f'time runs again once the game is over: {t1[0]} -> {t2}')
    again = gg.ev("""(() => { const id = window.__opp, p0 = (SHIP.rel[id] || {}).pts, f0 = SHIP.tiles.first[id]; SHIP.player.needs.social = 20; const s0 = SHIP.player.needs.social;
      tilesPlay(id, null, 'quick'); const G = TL_GAME, first = G.s.first; let n = 0;
      while (!G.s.over && n++ < 80) { if (G.timer) { clearTimeout(G.timer); G.timer = 0; } if (G.s.p === 0) tilesDo(tilesAI(G.s, 'medium', G.rng)); else tilesCrewMove(); }
      if (G.timer) clearTimeout(G.timer); TL_GAME = null;
      return [p0, (SHIP.rel[id] || {}).pts, f0, first, SHIP.tiles.first[id], G.tut, SHIP.player.needs.social - s0, bondMult(id)]; })()""")
    check(again[6] > 0 and again[6] <= 12 * .25 * again[7] * 1.3 + .01, f'a second game with them the same day gives a quarter of the social (0.28.54): +{again[6]:.2f} (bond {again[7]})')
    check(again[1] == again[0], f'a second game the same day adds no more friendship: {again[:2]}')
    check(again[2] == 1 and again[3] == 1 and again[4] == 0, f'who goes first turns about with each opponent, saved: {again[2:5]}')
    check(again[5] == -1, f'How to play only runs by itself on your first game: {again[5]}')
    gg.step(30)
    st = gg.ev("[!!TL_GAME, ACT && ACT.kind, (() => { const p = ROSTER.find(x => x.id === window.__opp); const w = p && whereIs(p, shipNow()); return w && w.act; })()]")
    check(not st[0] and st[1] != 'tiles' and st[2] != 'visit', f'Done (the game gone) stands you up, and they go back to their own plans: {st}')
    # someone already at the table plays you at once
    r = gg.ev(SEAT + "('rina')")
    sat = gg.ev("(ACT.o.board || []).map(id => heldBy(id)).filter(a => a && a.settled && a.p && a.p.id).map(a => a.p.id)")
    on = wait_for(gg, SEATED, 40)
    st = gg.ev("[TL_GAME && TL_GAME.opp, ACT && ACT.o.since === undefined]")
    check(on and st[0] in sat and st[1], f'someone already at the table: you sit and play them, nobody sent for: {r} at the board {sat}, {st}')
    # Leave game mid-game: you get up, uncounted
    gg.ev("if (TL_GAME.timer) { clearTimeout(TL_GAME.timer); TL_GAME.timer = 0; } deviceShow('tiles')"); gg.step(1)
    gg.page.click('#devBody .tl-play button[data-end="leave"]'); gg.step(40)
    st = gg.ev("[!!TL_GAME, SHIP.tiles.played, ACT && ACT.kind, FREEZE.frozen]")
    check(not st[0] and st[1] == 2 and st[2] != 'tiles' and not st[3], f'Leave game: you get up, the game uncounted (two played before), time runs: {st}')
    # walk away mid-game: the game is left, uncounted
    gg.ev(SEAT + "('rina')"); wait_for(gg, SEATED, 40)
    gg.ev("if (TL_GAME.timer) { clearTimeout(TL_GAME.timer); TL_GAME.timer = 0; } actEnd(true); deviceRefresh()")
    st = gg.ev("[!!TL_GAME, SHIP.tiles.played]")
    check(not st[0] and st[1] == 2, f'walking away leaves the game uncounted (two played before): {st}')
    # nobody free (quiet hours): a toast says so and you just sit
    gg.ev("SHIP.time.min = 22 * 60 + 30; for (const a of DECK_CREW) a.settled = false"); gg.step(2)
    r = gg.ev(SEAT + "(null)")
    sat = wait_for(gg, "!!(ACT && ACT.phase === 'do' && ACT.o.st === 'none')", 40)
    st = gg.ev("[ACT && ACT.kind, !!TL_GAME, document.getElementById('tx').textContent]")
    check(sat and st[0] == 'sit' and not st[1] and 'Nobody’s around to play right now' in st[2], f'nobody free: a toast says so and you stay sat: {st}')
    gg.ev("actEnd(true)")
    # beating Rina: news once, her memory, the day kept
    gg.ev("tilesPlay('rina', null, 'full'); if (TL_GAME.timer) { clearTimeout(TL_GAME.timer); TL_GAME.timer = 0; } TL_GAME.s.sc = [6, 0]; TL_GAME.s.p = 0")
    gg.ev("""(() => { const G = TL_GAME; let n = 0; while (!G.s.over && n++ < 80) { if (G.timer) { clearTimeout(G.timer); G.timer = 0; } if (G.s.p === 0) tilesDo(tilesAI(G.s, 'hard', G.rng)); else { const mv = tilesMoves(G.s, 1).find(m => !tilesApply(G.s, m).pts) || tilesMoves(G.s, 1)[0]; tilesDo(mv); } } if (G.timer) clearTimeout(G.timer); })()""")
    b = gg.ev("[TL_GAME.s.win, SHIP.tiles.beatRina !== null, NEWS.filter(n => n.id === 'tiles-rina-beaten').length, (SHIP.mem.rina || []).some(m => m[0] === 'moment.tiles'), SHIP.traces.filter(x => (x && x.id || x) === 'tilesTrophy').length]")
    check(b == [0, True, 1, True, 1], f'beating Rina: news once, her memory, the day kept, the trophy trace once: {b}')
    ap = gg.ev("(() => { TL_GAME = null; deviceShow('tiles'); const b = [...document.querySelectorAll('#devBody button')].find(x => /How to play/.test(x.textContent)); if (b) b.click(); const on = TL_UI.teachNext; tilesPlay('tomas', null, 'full'); const t = TL_GAME.tut; if (TL_GAME.timer) clearTimeout(TL_GAME.timer); TL_GAME = null; deviceClose(); return [!!b, on, t, TL_UI.teachNext]; })()")
    check(ap == [True, True, 0, False], f'How to play in the Tiles app runs it at your next game: {ap}')
    sv = gg.ev("(() => { const s = { ship: {} }; for (const f of SAVE_EXTRA) f(s); const back = tilesLoad(JSON.parse(JSON.stringify(s))); return [JSON.stringify(back) === JSON.stringify(SHIP.tiles), JSON.stringify(tilesLoad({ tiles: { played: -3, vs: { x: 'no' }, beatRina: 'x', taught: 'yes' } }))]; })()")
    check(sv[0], f'save.tiles round-trips: {sv}')
    check(sv[1] == '{"played":0,"won":0,"lost":0,"taught":false,"vs":{},"first":{},"relDay":{},"firstWin":null,"beatRina":null,"night":{"last":null,"rina":0,"games":[]}}', f'a bad save.tiles reads safely: {sv[1]}')
    check(not gg.errors and not gg.ev("DEV.errors.length"), f'seating: no errors: {gg.errors[:3]}')
    gg.close()

NIGHT = r"""(() => {
  const out = {}, crew = ROSTER.filter(p => p.id !== 'rina').slice(0, 9).map(p => p.id), came = ['rina', ...crew];
  const a = tilesNight(8, came), b = tilesNight(8, came.slice().reverse());
  out.same = JSON.stringify(a) === JSON.stringify(b);
  out.games = a.games.length; out.out = a.out;
  out.everyone = new Set(a.games.flatMap(g => [g.a, g.b]).concat(a.out ? [a.out] : [])).size === came.length;
  out.rinaPlays = a.games.some(g => g.a === 'rina' || g.b === 'rina');
  let rinaWins = 0, rinaGames = 0;
  for (let d = 1; d < 400; d += 7) { const r = tilesNight(d, came); for (const g of r.games) if (g.a === 'rina' || g.b === 'rina') { rinaGames++; if (g.win === 'rina') rinaWins++; } }
  out.rina = [rinaWins, rinaGames];
  // the rolls follow the odds: count, per level pair, how often the first beat the second
  const tally = {}, P = id => ROSTER.find(x => x.id === id);
  for (let d = 1; d <= 2000; d++) for (const g of tilesNight(d, crew).games) {
    const la = tilesStyle(P(g.a)).level, lb = tilesStyle(P(g.b)).level, k = la + '>' + lb, t = tally[k] || (tally[k] = [0, 0]); t[1]++; if (g.win === g.a) t[0]++;
  }
  out.odds = Object.fromEntries(Object.entries(tally).filter(([, v]) => v[1] >= 200).map(([k, v]) => [k, [Math.round(v[0] / v[1] * 100) / 100, TL_ODDS[k.split('>')[0]][k.split('>')[1]], v[1]]]));
  // the end of the night: news once, Rina's Tuesdays
  const n0 = SHIP.tiles.night.rina;
  simNote('tradition', { id: 'tilesNight', day: 15, at: 1290, came, you: true, host: 'rina' });
  simNote('tradition', { id: 'tilesNight', day: 15, at: 1290, came, you: true, host: 'rina' });
  out.news = NEWS.filter(x => x.id === 'tiles-night:15').map(x => x.lines);
  out.streak = [n0, SHIP.tiles.night.rina, SHIP.tiles.night.last];
  simNote('tradition', { id: 'quiz', day: 16, at: 1290, came, you: false });
  out.quiz = SHIP.tiles.night.last;
  deviceShow('tiles'); out.app = document.getElementById('devBody').textContent; deviceClose();
  return out;
})()"""

def night(pw, path):
    gg = Game(pw, path, 900, 760); gg.step(3)
    r = gg.ev(NIGHT)
    check(r['same'] and r['games'] == 5 and r['out'] is None and r['everyone'] and r['rinaPlays'], f'Tiles night: 10 people, 5 games, everyone placed, the same whatever the order, Rina plays: {r["same"]}, {r["games"]}, {r["everyone"]}, {r["rinaPlays"]}')
    check(r['rina'][0] == r['rina'][1] > 50, f'Rina wins every crew game until you beat her: {r["rina"]}')
    for k, (got, want, n) in r['odds'].items():
        e = 2.2 * (want * (1 - want) / n) ** .5 + .01
        check(abs(got - want) <= e, f'night rolls {k}: {got} against the odds {want} ({n} games)')
    print('  night odds:', {k: v[:2] for k, v in r['odds'].items()})
    check(len(r['news']) == 1 and r['news'][0] and 'Rina' in r['news'][0][0], f'the end of the night posts the news once: {r["news"]}')
    check(r['streak'][1] == r['streak'][0] + 1 and r['streak'][2] == 15 and r['quiz'] == 15, f'Rina Tuesdays counted; other traditions ignored: {r["streak"]}, {r["quiz"]}')
    check('Last Tiles night' in r['app'] or 'LAST TILES NIGHT' in r['app'].upper(), f'the Tiles app shows the last night: {r["app"][:120]}')
    print('  night news:', r['news'][0] if r['news'] else None)
    check(not gg.errors and not gg.ev("DEV.errors.length"), f'night: no errors: {gg.errors[:3]}')
    gg.close()

def run(path, games):
    src = open(path).read(); sec = section23(src)
    check(len(sec) > 1000, 'section 23 is there')
    code = re.sub(r'//[^\n]*', '', sec)
    check('Math.random' not in code, 'section 23 never calls Math.random')
    check(not re.search(r'(?<![\w.])R\(\)', code), 'section 23 never calls R()')
    check(not re.search(r'^(const|let|var|function)\s+TILES\b', src, re.M), 'no top-level TILES')
    talk = sec[sec.find('function tilesTalk'):sec.find('const tlName')]
    check('G.rng' not in talk and 'G.talk()' in talk, 'crew lines draw from their own stream, never the moves\' (key 807)')
    with sync_playwright() as pw:
        g = Game(pw, path)
        g.step(2)
        r = g.ev(RULES)
        check(r['deal']['bad'] == 0 and r['deal']['mirror'] == 0, f'300 deals: mirrored, 12 a side, no three of a mark touching: {r["deal"]}')
        check(r['teach']['rows'] == [[1, 0, 2, 1, 2, 0], [0, 2, 1, 0, 1, 2]] and not r['teach']['groups'], f'the teaching layout as on the plan page, no two of a mark touching: {r["teach"]}')
        check(r['jump'] == {'to': cell('e6'), 'over': cell('d5')}, f'worked turn 1: the Ship on c4 can jump d5 to e6: {r["jump"]}')
        check(r['afterJump']['hold'] == [2] and r['afterJump']['taken'] == 2 and r['afterJump']['d5'] == 0 and r['afterJump']['sc'] == [0, 0], f'the Star goes to your hold: {r["afterJump"]}')
        check(r['launchRows'] == [0, 1], f'launches only onto your two home rows: {r["launchRows"]}')
        check(r['dock']['pts'] == 3 and r['dock']['cells'] == sorted([cell('a1'), cell('b1'), cell('c1')]) and r['dock']['sc'] == [3, 0] and r['dock']['left'] == [0, 0, 0], f'worked turn 3: launching the Star on c1 docks three, 3 points: {r["dock"]}')
        check(r['steps'] == sorted([cell('d3'), cell('f3')]), f'a step goes one square diagonally forward: {r["steps"]}')
        check(r['stepDock'] == 3, f'a step into an L of Planets docks three: {r["stepDock"]}')
        q = r['quick']
        check(q['mid'] == {'sc': [5, 2], 'over': False, 'p': 1} and q['end']['over'] and q['end']['win'] == 0, f'quick game: reaching 5 first gives the other player one last turn: {q}')
        check(q['full']['over'] and q['full']['win'] == 0 and q['full']['sc'] == [7, 2], f'full game: reaching 7 ends it at once: {q["full"]}')
        print('  the rules: deal, teaching layout, worked turn, steps', 'ok' if ok else '')
        judge = games >= 4000   # balance is only judged at the default count or more (fewer games would make the band too easy)
        if not judge: print(f'  ({games} games a level: balance shown, not judged; the default is 4000)')
        for mode, p1max, plmax in (('full', .52, 24), ('quick', .53, 16)):
            b = g.ev(BAL + f"('{mode}', {games}, 12345)")
            print(f'  {mode} game:')
            for lv in ('easy', 'medium', 'hard'):
                x = b[lv]
                print(f'    {lv:6s} {x["n"]:5d} games: first player {x["p1"]*100:.1f}%, draws {x["draw"]*100:.2f}%, {x["plies"]:.1f} turns, tie-break wins by seat {x["tie"]}')
                e = 1.96 * (x['p1'] * (1 - x['p1']) / x['n']) ** .5   # sampling noise: the 95% band must reach the target
                check(not judge or (x['p1'] + e >= .48 and x['p1'] - e <= p1max), f'{mode} {lv}: first player within 48-{round(p1max*100)}% (give or take {e*100:.1f} for sampling): {x["p1"]:.3f}')
                check(not judge or x['draw'] < .01, f'{mode} {lv}: draws under 1%: {x["draw"]:.4f}')
                check(x['plies'] < plmax, f'{mode} {lv}: games under {plmax} turns: {x["plies"]:.1f}')
            for k in ('hard>medium', 'medium>easy'):
                print(f'    {k}: {b[k]*100:.0f}%'); check(not judge or b[k] > .6, f'{mode} {k} over 60%: {b[k]:.3f}')
        same = g.ev("(() => { const a = tilesSimGame('full', 'hard', 'easy', 4242), c = tilesSimGame('full', 'hard', 'easy', 4242); return JSON.stringify(a) === JSON.stringify(c); })()")
        check(same, 'the same seed plays the same game twice')
        sty = g.ev("[tilesStyle({ id: 'rina' }).level, tilesStyle({ id: 'tomas' }).level, JSON.stringify(tilesStyle({ id: 'x', seed: 99, traits: [] })) === JSON.stringify(tilesStyle({ id: 'x', seed: 99, traits: [] }))]")
        check(sty == ['hard', 'easy', True], f'crew styles: Rina hard, Tomas easy, the same every time: {sty}')
        check(not g.errors, f'no page errors: {g.errors[:3]}')
        g.close()
        board(pw, path)
        seat(pw, path)
        night(pw, path)

if __name__ == '__main__':
    run(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 4000)
    print('ALL OK' if ok else 'SOME CHECKS FAILED')
    sys.exit(0 if ok else 1)
