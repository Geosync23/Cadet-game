# Starship Cadet: Lightdisc check (keep in the repo, next to the other checks)
# Checks section 23b (the Lightdisc engineer, 0.82.x): Lightdisc on the rec deck's court (plans/recdeck-plan.html section 4).
#   the rules on paper: section 23b never calls R() or Math.random; the same seed plays the same game twice (each level);
#   games end (first to 7 win by 2, the quick game to 5); balance: the sharp autopilot against each crew level
#   frame rate: a live game run at 60, 30 and 20 frames a second is the same game, step for step (fixed 60 Hz steps)
#   the save: save.disc round-trips; a save from before 0.82 (no disc) loads as a fresh record; junk is ignored
#   on the deck: Ask someone to play brings one free crew member down by lift to the stern baseline and the game starts;
#   the ship's clock stands still while you play and the notice says so; the game view stays under 200 draw calls;
#   How to play on your first game; Leave mid-game isn't counted and the clock runs again; a whole game (your side on
#   the autopilot) ends with the result (Again, Quick game, Done), the record and the social; Done ends the activity and
#   your opponent goes back to their own plans; in quiet hours nobody comes; the page has no errors
# Setup and environment as for cadet_test.py.
# Run:  python3 disc_check.py BUILD.html [GAMES]   (GAMES per level for the balance table, default 40)
import sys, json, re
exec(open(__file__.replace('disc_check.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright

ok = True
def check(cond, msg):
    global ok
    print(('ok   ' if cond else 'FAIL ') + msg)
    if not cond: ok = False
    return cond

build = sys.argv[1]; GAMES = int(sys.argv[2]) if len(sys.argv) > 2 else 40
src = pathlib.Path(build).read_text()
if re.search(r'^const REC_DECK = false;', src, re.M):   # 0.63.2r: the rec deck is dormant in the main build; Lightdisc is checked with it switched on
    src = re.sub(r'^const REC_DECK = false;', 'const REC_DECK = true; ', src, count=1, flags=re.M)
    build = str(WORK / 'test' / ('_recon_' + pathlib.Path(build).name)); pathlib.Path(build).write_text(src)
    print('     (REC_DECK is off in this build: checking a copy with it switched on)')
i = src.find('// 23b. LIGHTDISC'); j = src.find('// 24. WORK', i); sec = src[i:j] if i >= 0 and j > i else ''
check(len(sec) > 1000, 'section 23b is there')
code = re.sub(r'//[^\n]*', '', sec)   # the comments say so; the code mustn't
check(not re.search(r'\bR\(', code) and 'Math.random' not in code, 'section 23b never calls R() or Math.random')

TO_EVENING = "(() => { skipTo((SHIP.time.day - 1) * 1440 + 19 * 60); goToDeck(7, null); return deckDef.num; })()"
STATE = "JSON.stringify({ g: !!DISC.g, phase: DISC.g && DISC.g.phase, score: DISC.g && DISC.g.score, step: DISC.g && DISC.g.step, act: ACT && ACT.kind, st: ACT && ACT.o && ACT.o.st, frozen: FREEZE.frozen, min: SHIP.time.min, view: !!DISC.view })"

def wait_game(g, n=60):
    for k in range(n):
        g.step(30)
        s = json.loads(g.ev(STATE))
        if s['g']: return s
    return json.loads(g.ev(STATE))

with sync_playwright() as pw:
    g = Game(pw, build, 390, 844)
    # ---- on paper ----
    r = json.loads(g.ev("""JSON.stringify(['easy', 'steady', 'sharp'].map(l => { const o = { seed: 77, you: LD_LEVEL.sharp, them: LD_LEVEL[l] }; return [ldPaper(o), ldPaper(o)]; }))"""))
    check(all(json.dumps(a) == json.dumps(b) for a, b in r), 'the same seed plays the same game twice, at each level')
    q = json.loads(g.ev("JSON.stringify(ldPaper({ seed: 5, quick: true, you: LD_LEVEL.sharp, them: LD_LEVEL.steady }))"))
    hi, lo = max(q['score']), min(q['score'])
    check(hi >= 5 and hi - lo >= 2 and (hi == 5 or hi - lo == 2), 'the quick game goes to 5, win by 2 (%d-%d)' % (hi, lo))
    bal = json.loads(g.ev("""JSON.stringify(['pell', 'holt', 'vance', 'rina', 'easy', 'steady', 'sharp'].map(k => { const L = LD_CREW[k] || LD_LEVEL[k]; let w = 0, steps = 0, rally = 0, n = 0;
      for (let s = 1; s <= %d; s++) { const x = ldPaper({ seed: s * 7919, you: LD_LEVEL.sharp, them: L }); if (x.winner === 0) w++; steps += x.steps; rally += x.rallies.reduce((a, b) => a + b, 0); n += x.rallies.length; }
      return [k, w, Math.round(steps / %d / 60), +(rally / n).toFixed(1)]; }))""" % (GAMES, GAMES)))
    allend = json.loads(g.ev("JSON.stringify([1,2,3,4,5,6,7,8].map(s => ldPaper({ seed: s, you: LD_LEVEL.sharp, them: LD_LEVEL.sharp })).every(x => x.winner >= 0 && Math.max(...x.score) >= 7 && Math.abs(x.score[0] - x.score[1]) >= 2))"))
    check(allend, 'games end, first to 7 win by 2')
    print('     balance, the sharp autopilot against each (games won of %d, minutes a game, returns a point):' % GAMES)
    for k, w, m, ra in bal: print('       %-7s %3d   %4.1f min   %4.1f' % (k, w, m / 60, ra))
    B = {k: w for k, w, m, ra in bal}
    check(B['pell'] >= B['holt'] and B['pell'] >= B['rina'] and B['easy'] >= B['sharp'], 'easy is easier than sharp, and Pell than Holt and Rina')
    # ---- the save ----
    rt = g.ev("""(() => { const a = { played: 3, won: 2, lost: 1, games: 4, taught: true, vs: { rina: [1, 1], pell: [1, 0] }, relDay: { rina: 2 }, beatRina: 2 };
      const b = discLoad(JSON.parse(JSON.stringify({ disc: a }))); return JSON.stringify(a) === JSON.stringify(b); })()""")
    check(rt, 'save.disc round-trips')
    old = json.loads(g.ev("JSON.stringify([discLoad({}), discLoad(null), discLoad({ disc: { played: -4, vs: { x: 'no', y: [1] }, taught: 'yes', won: 'a' } })])"))
    check(all(o['played'] == 0 and o['vs'] == {} and o['taught'] is False for o in old), 'a save from before 0.82 (no disc) loads as a fresh record; junk is ignored')
    check(g.ev("(() => { const s = {}; SAVE_EXTRA.find(f => /s\\.disc =/.test(String(f)))(s); return !!s.disc && s.disc.played === SHIP.disc.played; })()"), 'the save carries disc')
    # ---- on the deck: ask someone ----
    check(g.ev(TO_EVENING) == 7, 'on the rec deck at 19:00')
    g.step(30)
    g.ev("discAsk()")
    s = json.loads(g.ev(STATE)); who = g.ev("ACT && ACT.o && ACT.o.opp")
    check(s['act'] == 'disc' and s['st'] == 'wait' and who and g.ev("COME_TO.has(ACT.o.opp)"), 'Ask someone to play: you go to your baseline and %s is on the way' % who)
    s = wait_game(g)
    check(s['g'] and s['view'], 'they come down by lift to the stern baseline and the game starts')
    crew = json.loads(g.ev("JSON.stringify(DECK_CREW.map(a => a.p.id))"))
    check(who in crew and crew.count(who) == 1, 'the one you asked is on the rec deck, once (%s)' % crew)   # 0.64.0: with the rec deck's crew use on, others are there too (their own visits)
    m0 = s['min']; g.step(300); s2 = json.loads(g.ev(STATE))
    check(s2['frozen'] and s2['min'] == m0 and s2['step'] > s['step'] + 500, "the ship's clock stands still while you play (%s, game step %d)" % (hhmm if False else s2['min'], s2['step']))
    check('paused while you play' in g.ev("document.querySelector('#ld .pz').textContent") and g.ev("getComputedStyle(document.querySelector('#ld .pz')).display") != 'none', 'the notice says the clock is paused')
    calls = g.ev("(() => { window.__skip = false; window.__step(1, 33); return renderer.info.render.calls; })()")
    check(0 < calls < 200, 'the game view draws in %d calls (under 200)' % calls)
    check(g.ev("DISC.how === 0 && !document.querySelector('#ld .how').classList.contains('hide')"), 'How to play shows on your first game')
    check(g.ev("getComputedStyle(document.querySelector('.hud')).visibility") == 'hidden', 'the game view has the screen (the HUD steps aside)')
    g.shot('ld-1-play.png')
    # Leave mid-game: not counted
    g.ev("document.querySelector('#ld .lv').click()")
    g.step(30); s = json.loads(g.ev(STATE))
    check(not s['g'] and not s['frozen'] and s['act'] != 'disc' and g.ev("SHIP.disc.played") == 0, 'Leave mid-game: not counted, the clock runs again, you step off')
    check(g.ev("!document.getElementById('ld') && !document.body.classList.contains('ld-on')"), 'the overlay goes with it')
    g.step(300)
    check(not g.ev("COME_TO.has(%s)" % json.dumps(who)), 'your opponent goes back to their own plans')
    # a whole game, your side on the autopilot
    g.ev("discAsk()"); s = wait_game(g, 90)
    check(s['g'], 'ask again: someone comes (%s)' % g.ev("DISC.opp"))
    soc0 = g.ev("SHIP.player.needs.social")
    g.ev("DISC.g.p[0].ai = LD_LEVEL.sharp")
    for k in range(80):
        g.step(600)
        if g.ev("!DISC.g || DISC.g.phase === 'over'"): break
    s = json.loads(g.ev(STATE))
    check(s['phase'] == 'over' and s['frozen'], 'the game plays to the end (%s); the clock waits through the result' % s['score'])
    check(g.ev("!document.querySelector('#ld .res').classList.contains('hide') && [...document.querySelectorAll('#ld .res button')].map(b => b.textContent).join() === 'Again,Quick game,Done'"), 'the result: Again, Quick game, Done')
    rec = json.loads(g.ev("JSON.stringify(SHIP.disc)"))
    check(rec['played'] == 1 and rec['won'] + rec['lost'] == 1 and sum(rec['vs'][g.ev('DISC.opp')]) == 1 and rec['taught'], 'the record: one game, against them (%s)' % rec['vs'])
    check(g.ev("SHIP.player.needs.social") > soc0, 'the social comes at the end')
    g.step(5); g.shot('ld-2-result.png')
    g.ev("[...document.querySelectorAll('#ld .res button')].find(b => b.textContent === 'Quick game').click()")
    g.step(30); s = json.loads(g.ev(STATE))
    check(s['g'] and s['phase'] in ('serve', 'live') and g.ev("DISC.g.target") == 5 and s['frozen'], 'Quick game starts a game to 5 with the same opponent')
    check(g.ev("DISC.how") == -1, 'How to play only the first time')
    g.ev("document.querySelector('#ld .lv').click()"); g.step(30)
    check(g.ev("ACT === null || ACT.kind !== 'disc'"), 'Done/Leave ends the activity')
    # quiet hours
    g.ev("skipTo((SHIP.time.day) * 1440 + 30)"); g.ev("goToDeck(7, null)"); g.step(10)
    g.ev("discAsk()")
    check(g.ev("!(ACT && ACT.kind === 'disc') && !DISC.g"), 'after hours nobody comes')
    check(not g.errors, 'no errors: ' + ' | '.join(g.errors[:5]))
    g.close()

    # ---- the frame rate doesn't change the game: a live game copied at its start, then stepped on paper, matches ----
    def live(fps):
        h = Game(pw, build, 390, 844)
        h.ev(TO_EVENING); h.step(30); h.ev("discAsk()")
        wait_game(h)
        h.ev("DISC.g.p[0].ai = LD_LEVEL.sharp; window.__snap = ldClone(DISC.g)")
        h.step(int(40 * fps), 1000 / fps)
        out = json.loads(h.ev("""(() => { const S = window.__snap, G = DISC.g, k = G.step - S.step; for (let i = 0; i < k; i++) { ldStep(S, null); S.ev.length = 0; }
          const pick = x => JSON.stringify({ step: x.step, score: x.score, d: x.d, p: x.p.map(p => [p.x, p.z, p.hits]), rs: x.rs });
          return JSON.stringify({ k, same: pick(S) === pick(G), score: G.score }); })()"""))
        h.close(); return out
    for fps in (60, 30, 20):
        o = live(fps)
        check(o['same'] and abs(o['k'] - 2400) <= 3, '%d frames a second: %d steps in 40 s, the same game as on paper (%s)' % (fps, o['k'], o['score']))
print('ALL OK' if ok else 'FAILED')
sys.exit(0 if ok else 1)   # so a failing check fails for the computer too (split rehearsal SX1; SR2 N1)
