# Starship Cadet: the promotion in sight and your trade on the board (FX19, patch 0.92.6 items 18, 14 and 11)
# On paper, in one page (the game's own functions at the times they'd run, no walking):
#   off:    with PROMO_SIGHT_ON and BOARD_TRADE_ON false (as shipped until review), nothing new: no beat, no flag, no Mail,
#           the reputation toast and "What's next" as before, no trade job on the board over a shift
#   sight:  switch on. Reliable (Day 6, out of the bay): the toast names the test; one Mail from Calder naming the steps,
#           once; "What's next" names Relied on and Making it safe (not "rely on you"); the Training tab's list. Trusted:
#           the toast says one more step. The ship word turning "dependable": one Mail. Relied on before Day 8: one Mail
#           (from the second Monday). Day 8 without Making it safe: one Mail. Trained: promoAnnounce's beat, a Mail naming
#           tomorrow (and not the old announce Mail), the urgent notice, the list's "Test set". A save already past the
#           offer: nothing said. The test morning (arrow queue on): the 08:30 arrow to the Works bay
#   trade:  switch on. Day 9, trained in Rounds and Tuning, a machine drifted by one: over the shift the top-up posts your
#           trade (a tune, an afternoon round from 13:00), at most 3 and one an hour, xp 0, held to the shift's end; the
#           simple ones still come (at least BOARD_MIN not of your trade); the held list keeps your trade first
#   move:   the walk to 4-23 (the user, 05:20 UTC): off, the old 17:30; on, it starts at 17:00 with a notice; she waits through a
#           talk, an activity, sleep; on another deck it starts; open past 17:30; by 22:00 (or a load the next morning) the
#           cabin's yours (bed, door, Mail), then a notice, an arrow to it and the Training tab's line, done once you're in
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
    print('(sight) PROMO_SIGHT_ON:')
    a = g.ev("""(() => { PROMO_SIGHT_ON = true; const W = __w(6, 600, { xp: 17 }); __toasts.length = 0; worksXp(1); __tick(); __tick(); return __look(); })()""")
    print('    Reliable:', a)
    check(a['toasts'] and 'Tier 2 test' in a['toasts'][0][1], f"sight: the Reliable toast names the test ({a['toasts']})")
    check(len(a['mail']) == 1 and 'Relied on' in a['mail'][0] and a['mail'][0].startswith('Chief Ines Calder'), f"sight: one Mail from Calder naming the steps ({a['mail']})")
    check('promo.sight' in a['flags'], f"sight: the flag ({a['flags']})")
    check('Relied on' in a['next'] and 'Making it safe' in a['next'], f"sight: What's next names the steps ({a['next']})")
    check(len(a['check']) == 2 and 'Not yet' in a['check'][1], f"sight: the Training tab's list ({a['check']})")
    b = g.ev("""(() => { const W = SHIP.works; __toasts.length = 0; W.xp = 29; worksXp(1); __tick(); return __look(); })()""")
    print('    Trusted:', b['toasts'], b['flags'], len(b['mail']))
    check(b['toasts'] and 'One more step' in b['toasts'][0][1] and 'promo.sight.trusted' in b['flags'] and len(b['mail']) == 1, f"sight: Trusted, the toast and the flag, no new Mail ({b['toasts']}, {b['flags']}, {b['mail']})")
    c = g.ev("""(() => { SHIP.rep.ship.work = 61; __tick(); __tick(); return __look(); })()""")
    check(len(c['mail']) == 2 and 'dependable' in c['mail'][0].lower(), f"sight: dependable, one Mail ({c['mail'][:2]})")
    d = g.ev("""(() => { SHIP.works.xp = 41; __tick(); __tick(); return __look(); })()""")
    check(len(d['mail']) == 3 and 'promo.sight.day' in d['flags'], f"sight: Relied on before Day 8, one Mail ({d['mail'][:1]}, {d['flags']})")
    e = g.ev("""(() => { setShipNow(7 * 1440 + 601); __tick(); __tick(); return __look(); })()""")
    print('    Day 8, no m6:', e['mail'][0])
    check(len(e['mail']) == 4 and 'Making it safe' in e['mail'][0] and 'promo.sight.m6' in e['flags'], f"sight: Day 8 without Making it safe, one Mail ({e['mail'][:1]})")
    f = g.ev("""(() => { const W = SHIP.works; W.tr.m6 = 8; __toasts.length = 0; setShipNow(7 * 1440 + 602); __tick(); __tick(); return { ...__look(), test: W.test }; })()""")
    print('    trained:', f['mail'][0], f['test'], f['check'])
    check(f['test'] and f['test']['day'] == 9, f"sight: the test set for Day 9 ({f['test']})")
    check(len(f['mail']) == 5 and 'tomorrow' in f['mail'][0] and not any('Sleep' in m for m in f['mail']), f"sight: the ready Mail names tomorrow, not the old announce Mail ({f['mail'][:2]})")
    check(any('09:00' in t[1] for t in f['toasts']), f"sight: the notice ({f['toasts']})")
    check(any('09:00' in x for x in f['check']), f"sight: the list's test line ({f['check']})")
    h = g.ev("""(() => { const W = __w(9, 300, { xp: 45, tr: { m6: 8 }, test: { tier: 2, day: 9, tries: 0, passed: false } }); __tick(); return __look(); })()""")
    check(not h['mail'] and 'promo.sight' in h['flags'], f"sight: a save past the offer, nothing said ({h['mail']}, {h['flags']})")
    k = g.ev("""(() => { if (!promoQueue()) return 'no queue'; setShipNow(8 * 1440 + 515); __tick(); const e = GUIDE.list.find(x => x.id === 'promo:testday:9'); return e ? e.goal().label : null; })()""")
    print('    the test morning:', k)
    check(k and 'Works bay' in k, f"sight: the 08:30 arrow on the test morning ({k})")

def part_trade(g):
    print('(trade) BOARD_TRADE_ON:')
    r = g.ev("""(() => { BOARD_TRADE_ON = true; const W = __w(9, 360, { xp: 20, tr: { m1: 2, m5: 4 } }); SHIP.jobs.length = 0;
      const ms = machineList().filter(m => TUNABLE.has(m.kind) && !ENGINE_KINDS.has(m.kind) && jobTier({ machine: m.id }) <= 1 && m.deck !== 1);
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
    check(all(not k.startswith('rounds') or int(k.split('@')[1].split()[0]) >= 13 for k in r['kinds']), f"trade: rounds only from 13:00 ({r['kinds']})")
    check(all(' xp0 ' in k for k in r['kinds']), f"trade: no Works reputation ({r['kinds']})")
    check(all(p[2] >= 2 for p in r['per'] if p[0] >= 9 and p[0] <= 15), f"trade: the simple ones still come ({r['per']})")
    s = g.ev("""(() => { BOARD_TRADE_ON = true; const a = { kind: 'tune' }, b = { kind: 'service' }; return [boardTrade(a), boardTrade(b)]; })()""")
    check(s == [True, False], f"trade: boardTrade knows your trade ({s})")

MOVE = r"""(() => { window.__mv = (on, min, o = {}) => { PROMO_SIGHT_ON = on; const W = __w(10, min, { xp: 5 }); W.tier = 2; W.rank = 'officer'; W.test = { tier: 2, day: 9, tries: 1, passed: true };
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
