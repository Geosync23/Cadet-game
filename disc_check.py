# Starship Cadet: Lightdisc check (keep in the repo, next to the other checks)
# Checks section 23b (the Lightdisc engineer, 0.82.x): Lightdisc on the rec deck's court (plans/recdeck-plan.html section 4).
#   the rules on paper: section 23b never calls R() or Math.random; the same seed plays the same game twice (each level);
#   games end (first to 7 win by 2, the quick game to 5); balance: the sharp autopilot against each crew level
#   frame rate: a live game run at 60, 30 and 20 frames a second is the same game, step for step (fixed 60 Hz steps)
#   the save: save.disc round-trips; a save from before 0.82 (no disc) loads as a fresh record; junk is ignored
#   on the deck: Ask someone to play brings one free crew member down by lift to the stern baseline and the game starts;
#   the ship's clock stands still while you play and the notice says so; the game view stays under 200 draw calls;
#   How to play on your first game; Leave mid-game isn't counted and the clock runs again; a whole game (your side on
#   the autopilot) ends with the result (Again, Done; your games first to 3 from 0.92.5), the record and the social; Done ends the activity and
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
    yours = json.loads(g.ev("JSON.stringify([1,2,3,4,5,6,7,8].map(s => ldPaper({ seed: s, to: typeof LD_YOURS !== 'undefined' ? LD_YOURS : undefined, you: LD_LEVEL.sharp, them: LD_LEVEL.steady }).score))"))
    check(all(max(x) == 3 and min(x) < 3 for x in yours) and any(abs(x[0] - x[1]) == 1 for x in yours), '0.92.5 #3: your games end at first to 3, no win by 2 (%s)' % yours)
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
    check(g.ev("!document.querySelector('#ld .res').classList.contains('hide') && [...document.querySelectorAll('#ld .res button')].map(b => b.textContent).join() === 'Again,Done'"), 'the result: Again, Done (0.92.5: no Quick game)')
    rec = json.loads(g.ev("JSON.stringify(SHIP.disc)"))
    check(rec['played'] == 1 and rec['won'] + rec['lost'] == 1 and sum(rec['vs'][g.ev('DISC.opp')]) == 1 and rec['taught'], 'the record: one game, against them (%s)' % rec['vs'])
    check(g.ev("SHIP.player.needs.social") > soc0, 'the social comes at the end')
    g.step(5); g.shot('ld-2-result.png')
    g.ev("[...document.querySelectorAll('#ld .res button')].find(b => b.textContent === 'Again').click()")
    g.step(30); s = json.loads(g.ev(STATE))
    check(s['g'] and s['phase'] in ('serve', 'live') and g.ev("DISC.g.target") == 3 and s['frozen'], 'Again starts a game to 3 with the same opponent (0.92.5 #3)')
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
    # ---- 0.92.3 (FX11): the pool's camera (#17), the lockers tip (#16), the crew's games you can see (#25) ----
    h = Game(pw, build, 390, 844)
    h.ev("(() => { skipTo(1440 + 600); goToDeck(7, null); TIP_Q.length = 0; delete SHIP.device.tipsSeen['rec.change']; delete SHIP.device.tipsSeen.recChange; return 1; })()")
    t1 = json.loads(h.ev("(() => { recTap({ t: 'Pool', x: '' }, null, null); return JSON.stringify({ q: TIP_Q.map(x => x.id), act: ACT && ACT.kind }); })()"))
    t2 = json.loads(h.ev("(() => { actEnd(true); TIP_Q.length = 0; DEVICE_SKIN.tip(null); playerKit(null); recTap({ t: 'River', x: '' }, null, null); return JSON.stringify({ q: TIP_Q.map(x => x.id), old: !!SHIP.device.tipsSeen.recChange, act: ACT && ACT.kind }); })()"))
    check(t1['q'] == ['rec.change'] and t1['act'] == 'recChange', '#16 your first swim: the lockers tip (rec.change) as you go to change (%s)' % t1)
    check('rec.change' not in t2['q'] and not t2['old'] and t2['act'] == 'recChange', '#16 your first paddle after it: no tip again, and never the old recChange (%s)' % t2)
    h.ev("(() => { actEnd(true); TIP_Q.length = 0; DEVICE_SKIN.tip(null); const c = recLocker(); player.obj.position.set(c.x, 0, c.z); playerKit('rec'); recStart('swim', 'Pool', null, null); return 1; })()")
    gaps = []
    for k in range(50):
        h.step(15)
        r = json.loads(h.ev("JSON.stringify({ ph: ACT && ACT.phase, k: ACT && ACT.kind, ax: ACT && ACT.x, az: ACT && ACT.z, tx: target.x, tz: target.z })"))
        if r['k'] == 'recSwim' and r['ph'] == 'do' and r['ax'] is not None: gaps.append(((r['ax'] - r['tx']) ** 2 + (r['az'] - r['tz']) ** 2) ** .5)
    check(len(gaps) > 20 and max(gaps) < .5, '#17 the camera swims with you: %d frames in the pool, the camera at most %.2f m from you' % (len(gaps), max(gaps) if gaps else -1))
    h.ev("(() => { actEnd(true); playerKit(null); skipTo(1440 + 1040); goToDeck(7, null); const c = placeSpot('7-disc-1'); player.obj.position.set(c.x - 5.6, 0, c.z + 2.6); return 1; })()")
    h.step(150)
    SEE = "JSON.stringify({ crew: DECK_CREW.filter(a => a.settled && a.spot && /^7-disc/.test(a.spot.id)).map(a => [a.spot.id, +a.h.pos.x.toFixed(3), +a.h.pos.z.toFixed(3)]).sort(), disc: typeof LD_CV !== 'undefined' && LD_CV.m && LD_CV.m.visible ? [+LD_CV.m.position.x.toFixed(3), +LD_CV.m.position.z.toFixed(3)] : null })"
    pair = [json.loads(h.ev(SEE)) for k in range(8) if h.step(9) is None]
    long = [json.loads(h.ev(SEE)) for k in range(16) if h.step(30) is None]   # 8 s: a look at 1.2 s can land on a serve, where the server stands in the middle
    both = all(len(x['crew']) == 2 for x in pair)
    check(both, '#25 Day 2 17:22: two crew on the court\'s baselines (%s)' % pair[0]['crew'])
    discs = [tuple(x['disc']) for x in pair if x['disc']]
    moves = [len(set(tuple(x['crew'][i][1:]) for x in long if len(x['crew']) == 2)) for i in (0, 1)]
    check(len(discs) >= 6 and len(set(discs)) >= 5, '#25 their game: the disc in the air and moving (%d of 8 looks, %d places)' % (len(discs), len(set(discs))))
    check(both and min(moves) >= 3, '#25 their game: both players move to meet it (%s places each in 8 s)' % moves)
    same = h.ev("typeof ldCrewRally === 'function' && [3.1, 9.7, 14.2, 22.5].every(t => JSON.stringify(ldCrewRally(12345, t, false)) === JSON.stringify(ldCrewRally(12345, t, false)))")
    check(same, '#25 a pair at a moment plays the same rally twice')
    h.ev("(() => { skipTo(1440 + 1210); goToDeck(7, null); const c = placeSpot('7-disc-1'); player.obj.position.set(c.x - 5.6, 0, c.z + 2.6); return 1; })()")   # 20:10 (0.92.5: late piano on Tuesdays moves the Captain's practice from 19:06 to 19:59-20:33)
    h.step(150)
    solo = [json.loads(h.ev(SEE)) for k in range(8) if h.step(9) is None]
    check(all(len(x['crew']) == 1 and x['crew'][0][0] == '7-disc-2' for x in solo) and sum(1 for x in solo if x['disc']) >= 6, '#25 Day 2 20:10: one alone at the stern practises, the disc in the air (%d of 8 looks)' % sum(1 for x in solo if x['disc']))
    h.ev("(() => { const c = placeSpot('7-disc-1'); player.obj.position.set(c.x - .6, 0, c.z); discAsk(recCourtWaiting()); return 1; })()"); s = wait_game(h); h.step(30)   # from your baseline (the walk from the lift works too, slower)
    hid = h.ev("!!DISC.g && !(typeof LD_CV !== 'undefined' && LD_CV.m && LD_CV.m.visible)")
    check(s['g'] and hid, '#25 during your own game the crew\'s disc is hidden')
    check(not h.errors, '0.92.3 parts: no errors: ' + ' | '.join(h.errors[:5]))
    h.close()
    # ---- 0.92.5 (FX11): the kayak's stroke (#2), the camera in an auditorium seat (#14), an auditorium seat with no timer (#17) ----
    h = Game(pw, build, 600, 600)
    h.ev("(() => { skipTo(1440 + 600); goToDeck(7, null); SHIP.device.settings.tips = false; playerKit('rec'); const c = recSpot([11, 6], 11.4, 5.75, Math.PI, 'stand'); player.obj.position.set(c.x, 0, c.z); recStart('kayak', 'River', null, null); return 1; })()")
    for k in range(40):
        h.step(15)
        if h.ev("ACT && ACT.phase === 'do' && !!ACT.mv && !!ACT.mv.go"): break
    h.step(20)
    KM = """(() => { const b = ACT.body, rig = b.rig, ch = rig.chest, pad = (b.propMeshes || []).find(m => m.parent === ch); rig.root.updateMatrixWorld(true);
      const hs = rig.arms.map(a => { const v = a.hand.getWorldPosition(new THREE.Vector3()); ch.worldToLocal(v); return [v.x, v.y, v.z]; });
      const e = [-.65, .65].map(x => pad.localToWorld(new THREE.Vector3(x, .1, .4))), d = e[1].clone().sub(e[0]);
      return JSON.stringify({ hs, tilt: Math.asin(d.y / d.length()), low: Math.min(e[0].y, e[1].y), water: ACT.y }); })()"""
    km = [json.loads(h.ev(KM)) for k in range(40) if h.step(2) is None]
    slide = max(max(sum((a - b) ** 2 for a, b in zip(r['hs'][i], km[0]['hs'][i])) ** .5 for r in km) for i in (0, 1))
    tilt = max(abs(r['tilt']) for r in km); low = min(r['low'] for r in km)
    check(slide < .02, '#2 the kayak: your hands stay on the paddle through the stroke (they move %.3f m on the shaft)' % slide)
    check(tilt > .42 and low < km[0]['water'] - .03, '#2 the kayak: each blade goes into the water (the paddle tilts to %.2f, its end %.2f m under the surface)' % (tilt, km[0]['water'] - low))
    h.close()
    h = Game(pw, build, 390, 844)
    h.ev("(() => { skipTo(4 * 1440 + 958); goToDeck(7, null); SHIP.device.settings.tips = false; const pl = [...PLACE_OF.values()].filter(p => p.type === 'rec:seat' && p.room === 'A' && !p.ring && !heldBy(p.id)); const sp = placeSpot(pl[pl.length - 1].id); recGo('seat', { x: sp.x, z: sp.z }, 'Seats', ''); return 1; })()")
    seat = []
    while h.ev("SHIP.time.min") < 1032:
        h.step(30); seat.append(json.loads(h.ev("JSON.stringify([SHIP.time.min, ACT ? ACT.kind + ':' + ACT.phase : null, ACT && ACT.body ? Math.hypot(target.x - ACT.x, target.z - ACT.z) : null, ACT && ACT.body ? Math.hypot(target.x - (42.2 - OX), target.z - (9 - OZ)) : null, ACT && ACT.body ? Math.hypot(ACT.x - (42.2 - OX), ACT.z - (9 - OZ)) : null])")))
    on = [r for r in seat if r[1] == 'recSeat:do']
    cam = [r for r in on if r[0] > on[0][0] + 2] if on else []
    check(bool(cam) and all(r[3] < r[4] - 2 and r[2] < r[4] for r in cam), '#14 seated in the auditorium, the camera centres between you and the stage (%s)' % ([[round(x, 1) for x in r[2:]] for r in cam[:1]]))
    check(bool(on) and on[-1][0] >= 1028, '#17 seated for the Captain\'s address: no timer, you\'re still seated after it ends at 16:50 (last seated %s)' % (round(on[-1][0]) if on else None))
    # no show: a seat in the auditorium at 10:00 on a weekday is any other seat: still seated an hour and a half on (0.92.4: up after 15 minutes)
    h.ev("(() => { skipTo(8 * 1440 + 600); goToDeck(7, null); const pl = [...PLACE_OF.values()].filter(p => p.type === 'rec:seat' && p.room === 'A' && !p.ring && !heldBy(p.id)); const sp = placeSpot(pl[0].id); recGo('seat', { x: sp.x, z: sp.z }, 'Seats', ''); return 1; })()")
    quiet = []
    while h.ev("SHIP.time.min") < 700:
        h.step(60); quiet.append(json.loads(h.ev("JSON.stringify([SHIP.time.min, ACT ? ACT.kind + ':' + ACT.phase : null])")))
    qon = [r for r in quiet if r[1] == 'recSeat:do']
    check(bool(qon) and qon[-1][0] >= 698 and qon[0][0] <= 630, '#17 no show on: you stay seated till you get up (seated %s to %s)' % (round(qon[0][0]) if qon else None, round(qon[-1][0]) if qon else None))
    # RV11's case: your seat taken before you sit, you're moved one along, and you still stay seated
    h.ev("(() => { skipTo(11 * 1440 + 962); goToDeck(7, null); return 1; })()"); h.step(200)
    taken = h.ev("""(() => { const pl = [...PLACE_OF.values()].filter(p => p.type === 'rec:seat' && p.room === 'A' && !p.ring && !heldBy(p.id)); if (pl.length < 2) return null;
      const id = pl[0].id; actStart('recSeat', id, { pose: 'sit', title: 'Seats' });
      DECK_CREW.push({ goalId: id, p: { id: 'stub' } }); try { actBegin(); } finally { DECK_CREW.pop(); }   // someone got there first, the moment you arrive
      return ACT && ACT.o.moved && ACT.placeId !== id ? ACT.placeId : null; })()""")
    check(bool(taken), '#17 (setup) your seat taken as you arrive: moved one along (%s)' % taken)
    mv = []
    while h.ev("SHIP.time.min") < 1032:
        h.step(30); mv.append(json.loads(h.ev("JSON.stringify([SHIP.time.min, ACT ? ACT.kind + ':' + ACT.phase : null, !!(ACT && ACT.o && ACT.o.moved)])")))
    mon = [r for r in mv if r[1] == 'recSeat:do']
    check(bool(mon) and mon[-1][2] and mon[-1][0] >= 1028, '#17 moved one seat along (yours taken first), you\'re still seated after the address (moved %s, last seated %s)' % (bool(mon) and mon[-1][2], round(mon[-1][0]) if mon else None))
    check(not h.errors, '0.92.5 parts: no errors: ' + ' | '.join(h.errors[:5]))
    h.close()
print('ALL OK' if ok else 'FAILED')
sys.exit(0 if ok else 1)   # so a failing check fails for the computer too (check_fast.sh, GitHub)
