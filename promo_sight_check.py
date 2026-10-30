# Starship Cadet: the promotion in sight and your trade on the board (FX19, patch 0.92.6 items 18, 14 and 11)
# On paper, in one page (the game's own functions at the times they'd run, no walking):
#   off:    with PROMO_SIGHT_ON and BOARD_TRADE_ON false (as shipped until review), nothing new: no beat, no flag, no Mail,
#           the reputation toast and "What's next" as before, no trade job on the board over a shift
#   sight:  off, the old gate (Relied on, shift hours). Switch on (the user, 05:25 UTC: the test the day after Reliable): the
#           need is Reliable; Steady's toast names the next step, the list from Steady, "dependable" one Mail; Reliable
#           without Making it safe: the toast, one Mail saying what's left, no test; Making it safe done (Day 8 18:30): the
#           offer that moment, the test Day 9, the ready Mail naming tomorrow (not the old announce Mail), the notice, the
#           list's line; Friday evening: the test on Monday; in the bay no "Tomorrow" on a Friday;
#           Calder no cheer line (RV15); a save past the offer: nothing; the 08:30 arrow; Dev mode's needs
#   trade:  switch on. Day 9, trained in Rounds and Tuning, a machine drifted by one: over the shift the top-up posts your
#           trade (a tune, an afternoon round from 13:00), at most 3 and one an hour, xp 0, held to the shift's end; the
#           simple ones still come (at least BOARD_MIN not of your trade); the held list keeps your trade first
#   move:   the walk to 4-23 (the user, 05:20 UTC): off, the old 17:30; on, it starts at 17:00 with a notice; she waits through a
#           talk, an activity, sleep; on another deck it starts; open past 17:30; by 22:00 (or a load the next morning) the
#           cabin's yours (bed, door, Mail), then a notice, an arrow to it and the Training tab's line, done once you're in;
#           and she still walks you there the next day (after the ceremony; a day off from 09:00), again if missed
# Setup and environment as for cadet_test.py (CADET_WORK, CADET_CHROME).
# Run:  python3 promo_sight_check.py BUILD.html [part ...]   Good is PROMO SIGHT CHECK OK (exit 0); a failure exits 1.
import sys, pathlib
exec(open(__file__.replace('promo_sight_check.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright

ok = True
def fail(msg):
    global ok
    ok = False
    print('FAIL', msg)
def check(cond, msg):
    if not cond: fail(msg)
    return cond

ONLY = set(sys.argv[2:])
SETUP = r"""(() => {
  window.__toasts = []; toast = (a, b) => { window.__toasts.push([String(a), String(b || '')]); };
  if (typeof GUIDE !== 'undefined') GUIDE.tq.length = 0;
  window.__w = (day, min, o = {}) => { SHIP.works = null; SHIP.mail = []; SHIP.flags = {}; SHIP.occasions.length = 0; setShipNow((day - 1) * 1440 + min);
    try { repInit().ship.work = 50; } catch (e) { /* no social */ } const W = worksInit(); W.log.push(['x', 1, 0, 'service']); W.cur = null; Object.assign(W.tr, o.tr || {}); W.xp = o.xp || 0; if (o.test) W.test = o.test; return W; };
  window.__look = () => ({ mail: SHIP.mail.map(m => m.from + ': ' + m.subject + ' | ' + m.body), flags: Object.keys(SHIP.flags).filter(k => /^promo\./.test(k)).sort(),
    toasts: window.__toasts.slice(), next: worksNext(), check: (typeof promoCheck === 'function' ? promoCheck() : []).map(b => b.text || (b.rows || []).map(r => r.text + (r.sub ? ' = ' + r.sub : '')).join(' ; ')) });
  window.__out = () => { if (deckDef.num !== 5) goToDeck(5); player.obj.position.copy(cellPos(...ROOM_TILES['w'][0])); };   // into the Works bay
  window.__tick = () => { for (const f of WORK_TICKS) try { f(shipNow(), false); } catch (e) { console.error(e); } };
  return true;
})()"""

def part_off(g):
    print('(off) both switches off:')
    r = g.ev("""(() => { PROMO_SIGHT_ON = false; BOARD_TRADE_ON = false; const W = __w(6, 600, { xp: 17 }); __toasts.length = 0; worksXp(1); __tick();
      SHIP.rep.ship.work = 70; __tick(); W.xp = 41; __tick(); return __look(); })()""")
    print('   ', r)
    check(not r['mail'] and not r['flags'] and not r['check'], f"off: no Mail, flag or list ({r['mail']}, {r['flags']}, {r['check']})")
    check(r['toasts'] and 'People are noticing' in r['toasts'][0][1], f"off: the toast as before ({r['toasts']})")
    t = g.ev("""(() => { BOARD_TRADE_ON = false; const W = __w(9, 360, { xp: 20, tr: { m1: 2, m5: 4 } }); SHIP.jobs.length = 0;
      const ms = machineList().filter(m => TUNABLE.has(m.kind) && m.deck !== 1); if (ms[0]) SHIP.machines[ms[0].id].drift = 1;
      for (let h = 8 * 24 + 8; h < 8 * 24 + 17; h++) { setShipNow(h * 60); boardTopUp(h, SHIP.jobs); }
      return SHIP.jobs.filter(j => j.trade).length; })()""")
    check(t == 0, f"off: no trade job on the board ({t})")

def part_sight(g):
    print('(sight) PROMO_SIGHT_ON (the test the day after Reliable, the user 05:25 UTC):')
    o = g.ev("""(() => { PROMO_SIGHT_ON = false; const W = __w(8, 1110, { xp: 20, tr: { m6: 8 } }); __tick(); const a = !!W.test; setShipNow(7 * 1440 + 620); __tick(); return [a, !!W.test, ladderRow('t2').needs[0].rep]; })()""")
    check(o == [False, False, 'relied'], f"sight off: Reliable with Making it safe on Day 8 gets no test (the old Relied on) ({o})")
    a = g.ev("""(() => { PROMO_SIGHT_ON = true; const W = __w(4, 600, { xp: 7 }); __toasts.length = 0; worksXp(1); SHIP.rep.ship.work = 61; __tick(); __tick(); return { ...__look(), rep: ladderRow('t2').needs[0].rep }; })()""")
    print('    Steady:', a)
    check(a['rep'] == 'reliable', f"sight: the test's need is Reliable ({a['rep']})")
    check(a['toasts'] and 'Reliable' in a['toasts'][0][1] and 'Tier 2' in a['toasts'][0][1], f"sight: the Steady toast names the next step ({a['toasts']})")
    check(len(a['mail']) == 1 and 'dependable' in a['mail'][0].lower(), f"sight: dependable before Reliable, one Mail ({a['mail']})")
    check(len(a['check']) == 2 and 'Not yet' in a['check'][1], f"sight: the Training tab's list from Steady ({a['check']})")
    st = g.ev("promoSteps(0)")
    check('Reliable' in st and 'Making it safe' in st, f"sight: What's next names the needs ({st})")
    b = g.ev("""(() => { const W = SHIP.works; __toasts.length = 0; W.xp = 17; worksXp(1); __tick(); __tick(); return { ...__look(), test: W.test }; })()""")
    print('    Reliable, Day 4:', b['toasts'][:1], b['mail'][:1])
    check(b['toasts'] and 'Tier 2' in b['toasts'][0][1], f"sight: the Reliable toast names the test ({b['toasts']})")
    check(len(b['mail']) == 2 and 'Making it safe' in b['mail'][0] and not b['test'], f"sight: Reliable without Making it safe, one Mail saying what's left, no test yet ({b['mail'][:1]}, {b['test']})")
    f = g.ev("""(() => { const W = SHIP.works; W.tr.m6 = 8; __toasts.length = 0; setShipNow(7 * 1440 + 1110); __tick(); __tick(); return { ...__look(), test: W.test }; })()""")
    print('    Making it safe done, Day 8 18:30:', f['mail'][0], f['test'], f['check'])
    check(f['test'] and f['test']['day'] == 9, f"sight: offered the moment all hold (18:30), the test on Day 9 ({f['test']})")
    check(len(f['mail']) == 3 and 'tomorrow' in f['mail'][0] and not any('Sleep' in m for m in f['mail']), f"sight: the ready Mail names tomorrow, not the old announce Mail ({f['mail'][:2]})")
    check(any('09:00' in t[1] for t in f['toasts']), f"sight: the notice ({f['toasts']})")
    check(any('09:00' in x for x in f['check']), f"sight: the list's test line ({f['check']})")
    w = g.ev("""(() => { const W = __w(12, 1200, { xp: 18, tr: { m6: 8 } }); __tick(); return { ...__look(), test: W.test }; })()""")
    check(w['test'] and w['test']['day'] == 15 and w['mail'] and 'Monday' in w['mail'][0], f"sight: qualified Friday evening, the test on Monday (Day 15) ({w['test']}, {w['mail'][:1]})")
    fb = g.ev("""(() => { const said = [], ws = worksSay, wa = worksSayAll; worksSay = (id, t) => said.push(t); worksSayAll = (id, L) => said.push(...L); try {
      const r = {};
      __w(12, 990, { xp: 18, tr: { m6: 8 } }); __out(); __tick(); r.fri = said.slice(); said.length = 0;
      __w(8, 990, { xp: 18, tr: { m6: 8 } }); __out(); __tick(); r.thu = said.slice(); return r; } finally { worksSay = ws; worksSayAll = wa; } })()""")
    print('    in the bay, Friday and Monday 16:30:', fb)
    check(fb['fri'] and not any('omorrow' in t for t in fb['fri']), f"sight: a Friday offer in the bay never says \"Tomorrow\" (RV15) ({fb['fri']})")
    check(len(fb['thu']) == 2 and 'omorrow' in fb['thu'][1], f"sight: a Monday (Day 8) offer in the bay: the ready line, then \"Tomorrow, your test job\" ({fb['thu']})")
    g.ev("__out()"); g.step(20)   # the crew on the deck drawn (their bubbles' anchors)
    ch = g.ev("""(() => { const P = player.obj.position, a = { p: evPerson('calder'), h: {}, x: P.x + .5, z: P.z, pose: 'stand' }, b = DECK_CREW.find(x => x.p && x.p.id !== 'calder' && x.h);
      const said = [], bs = bubbleSay, keep = b && { x: b.x, z: b.z, pose: b.pose }; bubbleSay = (h, t) => said.push(h === a.h ? 'calder: ' + t : 'other: ' + t); DECK_CREW.push(a);
      try { if (b) { b.x = P.x - .5; b.z = P.z; b.pose = 'stand'; } CHEER = { ids: ['calder'].concat(b ? [b.p.id] : []), said: new Set(), until: shipNow() + 30 };
        cheerTick(SHIP.time.min); cheerTick(SHIP.time.min); return said.length ? said : ['(none) b ' + (b ? b.p.id + ' h ' + !!b.h + ' d ' + Math.hypot(b.x - P.x, b.z - P.z).toFixed(1) + ' pose ' + b.pose : 'none') + ' deck ' + deckDef.num + ' until ' + (shipNow() + 30)]; }
      finally { bubbleSay = bs; CHEER = null; DECK_CREW.splice(DECK_CREW.indexOf(a), 1); if (b) Object.assign(b, keep); } })()""")
    print('    the cheer, Calder beside you:', ch)
    check(isinstance(ch, list) and not any(x.startswith('calder') for x in ch) and any(x.startswith('other') for x in ch), f"sight: Calder says no cheer line after the summons (no \"well done\"; RV15), the others still cheer ({ch})")
    h = g.ev("""(() => { const W = __w(9, 300, { xp: 45, tr: { m6: 8 }, test: { tier: 2, day: 9, tries: 0, passed: false } }); __tick(); return __look(); })()""")
    check(not h['mail'] and 'promo.sight' in h['flags'], f"sight: a save past the offer, nothing said ({h['mail']}, {h['flags']})")
    k = g.ev("""(() => { if (!promoQueue()) return 'no queue'; __w(9, 515, { xp: 20, tr: { m6: 8 }, test: { tier: 2, day: 9, tries: 0, passed: false } }); __tick(); const e = GUIDE.list.find(x => x.id === 'promo:testday:9'); return e ? e.goal().label : null; })()""")
    print('    the test morning:', k)
    check(k and 'Works bay' in k, f"sight: the 08:30 arrow on the test morning ({k})")
    dv = g.ev("devmodeTestNeeds(SHIP.works, 9, 515).map(x => x[0]).join(' | ')")
    check('Reliable' in dv, f"sight: Dev mode's test needs name Reliable ({dv})")

def part_trade(g):
    print('(trade) BOARD_TRADE_ON:')
    r = g.ev("""(() => { BOARD_TRADE_ON = true; const W = __w(9, 360, { xp: 20, tr: { m1: 2, m5: 4 } }); SHIP.jobs.length = 0;
      const ms = machineList().filter(m => TUNABLE.has(m.kind) && !ENGINE_KINDS.has(m.kind) && jobTier({ machine: m.id }) <= 1 && m.deck !== 1 && !JOB_FOR[(SHIP.machines[m.id] || {}).state]);   // a machine in good order (a worn one gets a real job)
      for (const m of ms) SHIP.machines[m.id].drift = 0; if (ms[0]) SHIP.machines[ms[0].id].drift = 1;
      const per = [];
      for (let h = 8 * 24 + 8; h < 8 * 24 + 17; h++) { setShipNow(h * 60); boardTopUp(h, SHIP.jobs); per.push([h % 24, SHIP.jobs.filter(j => j.trade && j.found === h * 60).map(j => j.kind), SHIP.jobs.filter(j => boardForYou(j, h * 60) && !j.trade).length]); }
      const tr = SHIP.jobs.filter(j => j.trade);
      return { per, kinds: tr.map(j => j.kind + '@' + Math.floor(j.found / 60) % 24 + ' xp' + j.xp + ' leave' + j.leave), n: tr.length, tune: ms[0] && ms[0].id }; })()""")
    print('   ', r['kinds'], '| per hour (h, trade, simple for you):', r['per'])
    hours = [p[0] for p in r['per'] if p[1]]
    check(1 <= r['n'] <= 3, f"trade: one to three trade jobs a shift ({r['n']})")
    check(len(hours) == len(set(hours)) and all(len(p[1]) <= 1 for p in r['per']), f"trade: at most one an hour ({r['per']})")
    check(any(k.startswith('tune') for k in r['kinds']), f"trade: a tune on the machine drifted by one ({r['kinds']})")
    hr = lambda k: int(k.split('@')[1].split()[0])
    check(all(not k.startswith('rounds') or 13 <= hr(k) < 15 for k in r['kinds']), f"trade: rounds only 13:00-15:00 ({r['kinds']})")
    check(all(hr(k) <= 15 for k in r['kinds']), f"trade: none with under two hours of the shift left ({r['kinds']})")
    check(all(' xp0 ' in k for k in r['kinds']), f"trade: no Works reputation ({r['kinds']})")
    check(all(p[2] >= 2 for p in r['per'] if p[0] >= 9 and p[0] <= 15), f"trade: the simple ones still come ({r['per']})")
    s = g.ev("""(() => { BOARD_TRADE_ON = true; const a = { kind: 'tune' }, b = { kind: 'service' }; return [boardTrade(a), boardTrade(b)]; })()""")
    check(s == [True, False], f"trade: boardTrade knows your trade ({s})")

MOVE = r"""(() => { window.__mv = (on, min, o = {}) => { PROMO_SIGHT_ON = on; if (typeof PROMO_BEATS_ON !== 'undefined') { PROMO_BEATS_ON = false; promoBeatsApply(); }   /* FX28: FX19's 17:00 walk (after dinner: promo_beats_check.py) */ const W = __w(10, min, { xp: 5 }); W.tier = 2; W.rank = 'officer'; W.test = { tier: 2, day: 9, tries: 1, passed: true };
    W.done.push('summons2'); W.ms.push(['officer', 10]); W.home = 'bunk'; delete W.mv; __toasts.length = 0; if (typeof GUIDE !== 'undefined') GUIDE.list.length = 0; return W; };
  window.__mvLook = () => { const W = SHIP.works; return { mv: !!W.mv, moved: promoDone('move2'), home: W.home, bed: playerBed(), door: worksHomeOpen(4, 'W'), mail: SHIP.mail.map(m => m.subject),
    toasts: __toasts.map(t => t[1]), guide: (GUIDE.list.find(x => x.id === 'promo:home') || {}).id || null, seen: !!flag('promo.sight.home'), line: promoHomeLine().map(b => b.text) }; };
  window.__out = () => { if (deckDef.num !== 5) goToDeck(5); player.obj.position.copy(cellPos(...ROOM_TILES['w'][0])); };
  return true; })()"""

def part_move(g):
    print('(move) the walk to 4-23 can\'t be missed:')
    check(g.ev(MOVE), 'move setup')
    t17, t1740, t2200 = 9 * 1440 + 1020, 9 * 1440 + 1060, 9 * 1440 + 1320
    a = g.ev(f"""(() => {{ __out(); const W = __mv(false, 1020); promoMoveTick({t17}); delete W.mv; setShipNow({9 * 1440 + 1051}); promoMoveTick(shipNow()); return __mvLook(); }})()""")
    print('    off, 17:31 away from it:', a)
    check(a['moved'] and not a['line'], f"move off: as before, moved by 17:30 ({a})")
    b = g.ev(f"""(() => {{ __out(); __mv(true, 1020); promoMoveTick({t17}); return __mvLook(); }})()""")
    print('    17:00, free, in the Works bay:', b)
    check(b['mv'] and any('4-23' in t for t in b['toasts']), f"move: the walk starts at 17:00 with the notice ({b})")
    c = g.ev(f"""(() => {{ __out(); __mv(true, 1020); DIALOGUE = DIALOGUE || {{ id: 'x' }}; const was = DIALOGUE; promoMoveTick({t17}); const r1 = __mvLook(); DIALOGUE = null;
      setShipNow({t1740}); promoMoveTick({t1740}); const r2 = __mvLook(); setShipNow({t1740 + 5}); promoMoveTick({t1740 + 5}); return [r1, r2, __mvLook()]; }})()""")
    print('    in a talk at 17:00, free at 17:40:', c[0]['mv'], c[1]['mv'], c[2]['moved'])
    check(not c[0]['mv'] and c[1]['mv'] and not c[2]['moved'], f"move: a talk at 17:00, she waits; the walk at 17:40, still open after 17:30 ({c})")
    d = g.ev(f"""(() => {{ __out(); __mv(true, 1020); ACT = {{ kind: 'eat' }}; promoMoveTick({t17}); const r1 = __mvLook(); ACT = null; return r1; }})()""")
    check(not d['mv'] and not d['moved'], f"move: in an activity (eating), she waits ({d})")
    e = g.ev(f"""(() => {{ __out(); __mv(true, 1080); promoMoveTick({9 * 1440 + 1080}, true); return __mvLook(); }})()""")
    check(not e['mv'] and not e['moved'], f"move: asleep (time skipping) at 18:00, she waits ({e})")
    f = g.ev(f"""(() => {{ goToDeck(3); player.obj.position.copy(cellPos(...ROOM_TILES[Object.keys(ROOM_TILES).find(k => ROOM_TILES[k].length > 4)][0])); __mv(true, 1020); promoMoveTick({t17}); return __mvLook(); }})()""")
    check(f['mv'], f"move: on another deck, the walk starts ({f})")
    h = g.ev(f"""(() => {{ __out(); __mv(true, 1320); promoMoveTick({t2200}); setShipNow({t2200 + 1}); promoHomeTick({t2200 + 1}, false); return __mvLook(); }})()""")
    print('    not walked by 22:00:', h)
    check(h['moved'] and h['bed'] == '4-23' and h['door'] and 'Your cabin' in h['mail'], f"move: by 22:00 4-23 is yours (bed, door, Mail) ({h})")
    check(any('4-23' in t for t in h['toasts']) and h['guide'] == 'promo:home' and h['line'], f"move: then the notice, the arrow to your cabin and the Training tab's line ({h})")
    k = g.ev(f"""(() => {{ __out(); __mv(true, 1440 + 480); promoMoveTick({10 * 1440 + 480}); setShipNow({10 * 1440 + 481}); promoHomeTick({10 * 1440 + 481}, false); return __mvLook(); }})()""")
    check(k['moved'] and k['guide'] == 'promo:home' and k['bed'] == '4-23', f"move: a save loaded the next morning, the cabin yours and the arrow to it ({k})")
    m = g.ev(f"""(() => {{ goToDeck(4); player.obj.position.copy(cellPos(...ROOM_TILES['W'][0])); promoHomeTick({10 * 1440 + 482}, false); const r = __mvLook(); r.live = guideLive({10 * 1440 + 483}).some(x => x.id === 'promo:home'); return r; }})()""")
    check(m['seen'] and not m['live'], f"move: stepping into 4-23, the arrow's done ({m})")
    n = g.ev(f"""(() => {{ const W = SHIP.works, r = {{ miss: flag('promo.sight.walk') }}; __out(); __toasts.length = 0; setShipNow({10 * 1440 + 1021}); promoWalkAgainTick(shipNow(), false); r.cer = !!(W.mv && W.mv.again);
      W.done.push('ceremony2'); promoWalkAgainTick(shipNow(), false); r.mv = !!(W.mv && W.mv.again); r.toasts = __toasts.map(t => t[1]); r.esc = !!promoMoveEscort({{ id: W.mv ? W.mv.by : 'x' }}, shipNow());
      r.guide = GUIDE.list.some(x => x.id === 'promo:move:again'); goToDeck(4); player.obj.position.copy(cellPos(...ROOM_TILES['W'][0])); promoWalkAgainTick(shipNow() + 1, false); r.after = !!W.mv; r.missAfter = flag('promo.sight.walk') || null; return r; }})()""")
    print('    the walk the next day:', n)
    check(n['miss'] == 10, f"move: missed on Day 10, the walk owed ({n['miss']})")
    check(not n['cer'] and n['mv'] and any('4-23' in t for t in n['toasts']) and n['esc'] and n['guide'], f"move: the next day after the ceremony, she walks you (notice, her lead, the arrow) ({n})")
    check(not n['after'] and n['missAfter'] is None, f"move: in your cabin with her, the walk done ({n})")
    q = g.ev(f"""(() => {{ const W = SHIP.works; flagSet('promo.sight.walk', 12); __out(); setShipNow({12 * 1440 + 545}); promoWalkAgainTick(shipNow(), false); const r = {{ off: !playerShiftOn(13), mv: !!(W.mv && W.mv.again) }};
      setShipNow({12 * 1440 + 1321}); promoWalkAgainTick(shipNow(), false); r.late = !!W.mv; r.miss = flag('promo.sight.walk'); return r; }})()""")
    check(q['off'] and q['mv'] and not q['late'] and q['miss'] == 12, f"move: a day off, from 09:00; not there by 22:00, owed again ({q})")

with sync_playwright() as pw:
    g = Game(pw, sys.argv[1])
    g.step(2)
    check(g.ev(SETUP), 'setup')
    for name, fn in [('off', part_off), ('sight', part_sight), ('trade', part_trade), ('move', part_move)]:
        if ONLY and name not in ONLY: continue
        try: fn(g)
        except Exception as e: fail(f'{name}: {e}')
    if g.errors: fail('page errors: ' + ' | '.join(g.errors[:5]))
    g.close()
print('PROMO SIGHT CHECK OK' if ok else 'PROMO SIGHT CHECK FAILED')
sys.exit(0 if ok else 1)
