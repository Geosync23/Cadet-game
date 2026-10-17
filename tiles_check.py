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

def run(path, games):
    src = open(path).read(); sec = section23(src)
    check(len(sec) > 1000, 'section 23 is there')
    code = re.sub(r'//[^\n]*', '', sec)
    check('Math.random' not in code, 'section 23 never calls Math.random')
    check(not re.search(r'(?<![\w.])R\(\)', code), 'section 23 never calls R()')
    check(not re.search(r'^(const|let|var|function)\s+TILES\b', src, re.M), 'no top-level TILES')
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
        for mode, p1max, plmax in (('full', .52, 24), ('quick', .53, 16)):
            b = g.ev(BAL + f"('{mode}', {games}, 12345)")
            print(f'  {mode} game:')
            for lv in ('easy', 'medium', 'hard'):
                x = b[lv]
                print(f'    {lv:6s} {x["n"]:5d} games: first player {x["p1"]*100:.1f}%, draws {x["draw"]*100:.2f}%, {x["plies"]:.1f} turns, tie-break wins by seat {x["tie"]}')
                e = 1.96 * (x['p1'] * (1 - x['p1']) / x['n']) ** .5   # sampling noise: the 95% band must reach the target
                check(x['p1'] + e >= .48 and x['p1'] - e <= p1max, f'{mode} {lv}: first player within 48-{round(p1max*100)}% (give or take {e*100:.1f} for sampling): {x["p1"]:.3f}')
                check(x['draw'] < .01, f'{mode} {lv}: draws under 1%: {x["draw"]:.4f}')
                check(x['plies'] < plmax, f'{mode} {lv}: games under {plmax} turns: {x["plies"]:.1f}')
            for k in ('hard>medium', 'medium>easy'):
                print(f'    {k}: {b[k]*100:.0f}%'); check(b[k] > .6, f'{mode} {k} over 60%: {b[k]:.3f}')
        same = g.ev("(() => { const a = tilesSimGame('full', 'hard', 'easy', 4242), c = tilesSimGame('full', 'hard', 'easy', 4242); return JSON.stringify(a) === JSON.stringify(c); })()")
        check(same, 'the same seed plays the same game twice')
        sty = g.ev("[tilesStyle({ id: 'rina' }).level, tilesStyle({ id: 'tomas' }).level, JSON.stringify(tilesStyle({ id: 'x', seed: 99, traits: [] })) === JSON.stringify(tilesStyle({ id: 'x', seed: 99, traits: [] }))]")
        check(sty == ['hard', 'easy', True], f'crew styles: Rina hard, Tomas easy, the same every time: {sty}')
        check(not g.errors, f'no page errors: {g.errors[:3]}')
        g.close()

if __name__ == '__main__':
    run(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 4000)
    print('ALL OK' if ok else 'SOME CHECKS FAILED')
    sys.exit(0 if ok else 1)
