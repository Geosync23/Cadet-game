# Starship Cadet: CR1's check (the 0.99.7 playtest patch, notes 25, 48, 49, 55, 56; plans/patch-0997.md; 24p's slot).
# On paper in a real page, each part with its switch on and then off (the switches are vars, flipped at run time):
#   check  (49, CR_DAY8_ON) the Training tab's "Your promotion" list: on Day 8 with no test, nothing says Done but what
#          is; the day row "The test from Day 8 = Reached" (Day 7: Not yet). Off: as 0.99.6 ("The test from Day 9 = Done")
#   day8   (55, CR_DAY8_ON) Making it safe learned on Day 8 by 12:30: the test is Day 8, 13:00-16:00; the Mail and
#          Calder's word say today; at 12:30 the test opens (Calder's held job on a scrubber, held to 16:00). Learned at
#          12:40: Day 9, 09:00 as before. Off: Day 9
#   redo   (56, INC_REDO_ON) Making it safe's training job, open on the board: a Take it (ixBoard.doable), the board's
#          lesson, named "Make it safe training job"; another incident: no Take it until it's one you put back. Off: none
#   cart   (48, CART_FIRST_ON) the garden crates: the Cart bay dock first and last, the arrow "Take a hover cart from the
#          Cart bay", no cart in hand till it's taken, full after the pick-up; hauling: no cart before the dock. Off: as before
#   mix    (25, BOARD_NEW_ON) with a repair of your trade on the board, a tune and a round still come (FX19 posted none);
#          newest learned first; a round learned lately from 10:00; at most one an hour, 4 a shift. Off: FX19 as before
# Run:  python3 cr1_check.py BUILD.html [part ...]   (about 1 minute)   Good is CR1 CHECK OK (exit 0).
import sys, json
exec(open(__file__.replace('cr1_check.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
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
  window.__w = (day, min, o = {}) => { SHIP.works = null; SHIP.mail = []; SHIP.flags = {}; SHIP.occasions.length = 0; SHIP.jobs.length = 0; setShipNow((day - 1) * 1440 + min);
    try { repInit().ship.work = 50; } catch (e) { /* no social */ } const W = worksInit(); W.log.push(['x', 1, 0, 'service']); W.cur = null; Object.assign(W.tr, o.tr || {}); W.xp = o.xp || 0; if (o.test) W.test = o.test; return W; };
  window.__tick = () => { for (const f of WORK_TICKS) try { f(shipNow(), false); } catch (e) { console.error(e); } };
  window.__sw = on => { CR_DAY8_ON = INC_REDO_ON = CART_FIRST_ON = BOARD_NEW_ON = on; };
  window.__rows = () => (promoCheck()[1] || { rows: [] }).rows.map(r => r.text + (r.sub ? ' = ' + r.sub : ''));
  return true;
})()"""

def part_check(g):
    for on in (True, False):
        r = g.ev(f"""(() => {{ __sw({'true' if on else 'false'}); const out = {{}}; __w(8, 540, {{ xp: 20 }}); out.d8 = __rows(); __w(7, 600, {{ xp: 20 }}); out.d7 = __rows();
          __w(8, 540, {{ xp: 20, tr: {{ m6: 8 }}, test: {{ tier: 2, day: 8, tries: 0, passed: false }} }}); out.set = __rows(); return out; }})()""")
        print(f'  (check, {"on" if on else "off"})', r)
        if on:
            check('The test from Day 8 = Reached' in r['d8'] and not any(x.endswith('= Done') and 'Reliable' not in x for x in r['d8']), f"check: Day 8, no test: only what's done says Done; the day row Reached ({r['d8']})")
            check('The test from Day 8 = Not yet' in r['d7'], f"check: Day 7: the day row Not yet ({r['d7']})")
            check('Test job: today, 13:00' in r['set'], f"check: the test today names 13:00 ({r['set']})")
        else:
            check('The test from Day 9 = Done' in r['d8'], f"check off: as 0.99.6 ({r['d8']})")

def part_day8(g):
    r = g.ev("""(() => { __sw(true); const out = {}; const W = __w(8, 650, { xp: 20, tr: { m6: 8 } }); __tick();
      out.day = W.test && W.test.day; out.at = PROMO.jobAt; out.until = PROMO.until; out.mail = SHIP.mail.map(m => m.subject + ' | ' + m.body); out.say = __toasts.map(t => t[1]);
      setShipNow(7 * 1440 + 750); __tick(); const c = W.cur, j = c && SHIP.jobs.find(x => x.id === c.j); out.cur = c ? c.id + ':' + c.st : null; out.job = j ? [j.machine, j.found % 1440, j.until % 1440] : null;
      const V = __w(8, 760, { xp: 20, tr: { m6: 8 } }); __tick(); out.late = V.test && V.test.day; out.lateAt = PROMO.jobAt;
      __sw(false); const X = __w(8, 650, { xp: 20, tr: { m6: 8 } }); __tick(); out.off = X.test && X.test.day; out.offAt = PROMO.jobAt; __sw(true); return out; })()""")
    print('  (day8)', r)
    check(r['day'] == 8 and r['at'] == 780 and r['until'] == 960, f"day8: Making it safe by 12:30, the test that day 13:00-16:00 ({r['day']}, {r['at']}, {r['until']})")
    check(any('today' in m and '13:00' in m for m in r['mail']), f"day8: the Mail says today, 13:00 ({r['mail']})")
    check(any('today, 13:00' in s for s in r['say']), f"day8: Calder's word says today, 13:00 ({r['say']})")
    check(not any('09:00' in s or 'Nine' in s for s in r['say']), f"day8: no word of a 09:00 test ({r['say']})")
    check(r['cur'] == 't2:do' and r['job'] and 'scrubber' in r['job'][0] and r['job'][1] == 780 and r['job'][2] == 960, f"day8: at 12:30 the test job on a scrubber, 13:00 to 16:00 ({r['cur']}, {r['job']})")
    check(r['late'] == 9 and r['lateAt'] == 540, f"day8: learned at 12:40, Day 9 at 09:00 as before ({r['late']}, {r['lateAt']})")
    check(r['off'] == 9 and r['offAt'] == 540, f"day8 off: Day 9 at 09:00 ({r['off']}, {r['offAt']})")

def part_redo(g):
    r = g.ev("""(() => { const out = {}; for (const on of [true, false]) { __sw(on); const W = __w(8, 640, { xp: 20, tr: { m5: 4, m7: 5 } }); const t = shipNow();
        const j = incJob('burst', 4, t, { slot: 16, train: 'm6' }); SHIP.jobs.push(j); W.cur = { id: 'm6', st: 'do', d: 8, by: 'calder', occ: null, j: j.id, w: 0 };
        const k = incJob('alarm', 3, t, { held: true }); SHIP.jobs.push(k); W.tr.m6 = 8;
        const o = { train: ixBoard.doable(j), lesson: boardLesson() === j.id, name: boardLessonName(j.id), other: ixBoard.doable(k) };
        CR_PUT.add(k.id); o.put = ixBoard.doable(k); CR_PUT.delete(k.id); out[on ? 'on' : 'off'] = o; } __sw(true); return out; })()""")
    print('  (redo)', r)
    on, off = r['on'], r['off']
    check(on['train'] and on['lesson'] and on['name'] == 'Make it safe training job', f"redo: the training job has a Take it, is the board's lesson, named ({on})")
    check(not on['other'] and on['put'], f"redo: another incident only once you've put it back ({on})")
    check(not off['train'] and not off['lesson'] and not off['put'] and off['name'] != 'Make it safe training job', f"redo off: as before ({off})")

def part_cart(g):
    r = g.ev("""(() => { const out = {}; for (const on of [true, false]) { __sw(on); __w(8, 600, { xp: 20 }); const id = gardenCarry({ at: shipNow(), crates: 2 }), j = SHIP.jobs.find(x => x.id === id);
        const o = { tags: j.stops.map(s => s.tag), bring: j.bring };
        j.claimedBy = 'you'; j.status = 'claimed'; o.hold0 = ixHold(); o.goal0 = (ixJobStep() || {}).label || null;
        if (on) { jobStepDone(j.id, 0); o.hold1 = ixHold(); o.goal1 = (ixJobStep() || {}).label || null; jobStepDone(j.id, 1); o.hold2 = ixHold(); }
        const hj = haulJob(shipNow(), [{ id: 'linen', dest: '4-linen-1' }]); o.haul0 = JOB_KINDS.haul.hold(hj);
        j.claimedBy = null; j.status = 'done'; out[on ? 'on' : 'off'] = o; } __sw(true); return out; })()""")
    print('  (cart)', r)
    on, off = r['on'], r['off']
    check(on['tags'] == ['cart', 'pickup', 'drop', 'return'] and 'hover cart' not in (on['bring'] or ''), f"cart: the dock first and last ({on['tags']}, {on['bring']})")
    check(on['goal0'] == 'Take a hover cart from the Cart bay' and on['hold0'] is None, f"cart: the arrow to the Cart bay, nothing in hand yet ({on['goal0']}, {on['hold0']})")
    check(on['hold1'] == 'cart' and (on['goal1'] or '').startswith('Pick up') and on['hold2'] == 'cartfull', f"cart: your cart after the dock, full after the pick-up ({on})")
    check(on['haul0'] is None and off['haul0'] == 'cart', f"cart: hauling, no cart before the dock (off: as before) ({on['haul0']}, {off['haul0']})")
    check(off['tags'] == ['pickup', 'drop'] and off['bring'].startswith('a hover cart'), f"cart off: as before ({off})")

MIX = """(() => { __sw(%s); const W = __w(%d, 360, { xp: 20, tr: %s }); SHIP.jobs.length = 0;
  const ms = machineList().filter(m => TUNABLE.has(m.kind) && !ENGINE_KINDS.has(m.kind) && jobTier({ machine: m.id }) <= 1 && m.deck !== 1 && !JOB_FOR[(SHIP.machines[m.id] || {}).state]);
  for (const m of ms) SHIP.machines[m.id].drift = 0; if (ms[0]) SHIP.machines[ms[0].id].drift = 1; if (ms[1]) SHIP.machines[ms[1].id].drift = -1;
  const rm = machineList().find(m => !ms.slice(0, 2).includes(m) && !ENGINE_KINDS.has(m.kind) && !m.stub && jobTier({ machine: m.id }) <= 1 && panelPlace(m.id));
  const rp = jobMake('repair', { id: 'cr1-repair', machine: rm.id, deck: rm.deck, room: rm.room, h: 0, urgency: 0, leave: 2000 }); rp.posted = rp.found = shipNow() - 60; SHIP.jobs.push(rp);
  const per = [], d = %d;
  for (let h = (d - 1) * 24 + 8; h < (d - 1) * 24 + 17; h++) { setShipNow(h * 60); boardTopUp(h, SHIP.jobs); per.push([h %% 24, SHIP.jobs.filter(j => j.trade && j.found === h * 60).map(j => j.kind)]); }
  return { per, rep: boardTrade(rp) && boardForYou(rp, shipNow()), kinds: SHIP.jobs.filter(j => j.trade).map(j => j.kind + '@' + Math.floor(j.found / 60) %% 24), order: typeof boardNewKinds === 'function' ? boardNewKinds(d).map(k => k.kind + (k.fresh ? '*' : '')) : null }; })()"""

def part_mix(g):
    fresh = g.ev(MIX % ('true', 9, "{ m1: 2, m5: 4, m7: 5 }", 9))
    old = g.ev(MIX % ('true', 22, "{ m1: 2, m5: 4, m7: 5 }", 22))
    off = g.ev(MIX % ('false', 9, "{ m1: 2, m5: 4, m7: 5 }", 9))
    for k, v in (('fresh', fresh), ('old', old), ('off', off)): print(f'  (mix, {k})', v)
    hr = lambda k: int(k.split('@')[1])
    check(fresh['rep'] and any(k.startswith('tune') for k in fresh['kinds']) and any(k.startswith('rounds') for k in fresh['kinds']), f"mix: with a repair of yours up, a tune and a round still come ({fresh['kinds']})")
    check(fresh['order'] == ['tune*', 'rounds*'], f"mix: the newest learned first ({fresh['order']})")
    check(any(k.startswith('rounds') and hr(k) < 13 for k in fresh['kinds']), f"mix: a round learned lately before 13:00 ({fresh['kinds']})")
    check(all(len(p[1]) <= 1 for p in fresh['per']) and len(fresh['kinds']) <= 4 and all(10 <= hr(k) <= 15 for k in fresh['kinds']), f"mix: one an hour, 4 a shift, 10:00 to 15:00 ({fresh['per']})")
    check(old['order'] == ['tune', 'rounds'] and all(not k.startswith('rounds') or 13 <= hr(k) < 15 for k in old['kinds']), f"mix: learned long ago, a round 13:00-15:00 as before ({old['order']}, {old['kinds']})")
    check(not off['kinds'], f"mix off: FX19, none while a repair of your trade is up ({off['kinds']})")
    hook = g.ev("""(() => { __sw(true); boardNewAdd({ mech: 'm9', kind: 'crtest', make: c => ({ id: 'crtest@' + c.h, machine: null, deck: 5, room: 'w', kind: 'chore', chore: 'crtest', target: 'x', title: 'A test chore', tier: 1,
        stops: [{ deck: 5, placeId: '5-timeclock-1', mins: 5, tag: 'x' }], urgency: 0, posted: c.t, found: c.t, claimedBy: null, parts: [], status: 'open', ...c.o }) });
      const W = __w(9, 360, { xp: 20, tr: { m1: 2, m5: 4, m9: 8 } }); const out = { order: boardNewKinds(9).map(k => k.kind) };
      setShipNow(8 * 1440 + 600); boardNewPost(8 * 24 + 10, SHIP.jobs, shipNow(), 600, 1020); out.first = SHIP.jobs.filter(j => j.trade).map(j => j.chore || j.kind);
      BOARD_NEW_MAKE.splice(BOARD_NEW_MAKE.findIndex(e => e.kind === 'crtest'), 1); return out; })()""")
    print('  (mix, another seat\'s kind)', hook)
    check(hook['order'][:1] == ['crtest'] and hook['first'] == ['crtest'], f"mix: another seat's kind (boardNewAdd), newest learned, posted first ({hook})")

with sync_playwright() as pw:
    g = Game(pw, sys.argv[1])
    g.step(2)
    check(g.ev(SETUP), 'setup')
    for name, fn in [('check', part_check), ('day8', part_day8), ('redo', part_redo), ('cart', part_cart), ('mix', part_mix)]:
        if ONLY and name not in ONLY: continue
        try: fn(g)
        except Exception as e: fail(f'{name}: {str(e)[:400]}')
    if g.errors: fail('page errors: ' + ' | '.join(g.errors[:5]))
    g.close()
print('CR1 CHECK OK' if ok else 'CR1 CHECK FAILED')
sys.exit(0 if ok else 1)
