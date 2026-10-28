# Starship Cadet: the Tier 2 test and the promotion as pronounced moments (FX28, the user's playtest notes 2026-10-26;
# lead 38's plan A-G). On paper, in one page (the game's own functions at the times they'd run, no walking):
#   off:     PROMO_BEATS_ON false: PROMO's times and the summons' script as before (11:00, promo.officer), the old words'
#            keys, the ceremony the next day at 17:15, no new Schedule rows, the test's pointer not forced
#   pointer: switch on, Teaching arrows Off: the board's ring on the test's Take it all the same, "Your Tier 2 test: take
#            it", seen on screen with the board open; the world arrow to the board is level 1
#   before:  the offer (Day 8, 18:30): the Schedule and Tracked have "Your Tier 2 test" for tomorrow; friends' Mails at
#            20:00; the morning notice; Calder's word in the bay; the crew's talk (pb.soon by days aboard, pb.luck)
#   passed:  the result held (still Tier 1), Calder's word, the Mail and the notice name the result's day and 08:15; the
#            result's row the evening before
#   result:  the result day: the Mail at 06:00, the summons booked at 08:15 as "Your results", script promo.result; at its
#            end you're promoted and the Captain's ceremony is booked the same day at 16:30 (17:15 on a Friday), its
#            invite naming the time; Brennan's cake after it; Dev mode's beats in order
#   cabin:   the walk waits for the pip, your dinner and your leaving the mess; it starts after; 20:00 at the latest
# The Tier 3 parts (S5-2, B5; the Senior Officer promotion, 24u, behind P5_PROMO3; plans/p5-step5-spec.html "The beats"):
#   t3off:    with P5_PROMO3 off (the build as shipped): no offer, no Tier 3 rows, no t3 record, nothing said; with it on: skipped
#   t3before: (switch on) Day 14: Calder comes to find you (her escort follows you) and, beside you, her scene; at the
#             storm's party in the bow lounge the party's twin; only then the test is set (Day 15), the urgent notice and
#             the Mail; Schedule and Tracked rows, the Training tab and What's next; two friends' Mails at 20:00; the
#             talk's beats (luck the evening before and the test morning); not found by 22:00: by Mail
#   t3pointer: (switch on) the test morning's notice, the level 1 arrow to the bay from 08:30; at 09:00 the job held for you
#             on the worse Deck 6 junction (slot 25), the board's ring forced with Teaching arrows Off, "Your Tier 3 test:
#             take it", the world arrow level 1; the Schedule's row; an hourly notice while you hold another job
#   t3passed: (switch on) the test, taken: Calder's word; level 1 arrows to each step; the plan names the two to warn; the switch
#             refused before both know; "About the shutdown" on them in the chat card, their answer; one not found in 30
#             minutes, Calder tells them; the breaker, back on, the junction put right; turned in: passed, still Tier 2,
#             Calder's word, the Mail and the notice name tomorrow 08:15, the result's row; the crew watch, then talk of it.
#             Not taken by 15:00: set again in two workdays, never failed
#   t3result: (switch on) the result's day: the Mail at 06:00, the notice once you're up, booked at 08:15 in her office,
#             What's next, a level 1 arrow from 08:00; not there at 08:30 she comes to find you and it plays where you are;
#             at its end Tier 3, Senior Officer, xp 0, the Record's line, the friends' Mail, the bar booked the same day
#   t3bar:    (switch on) the Captain's invite, the guests on the ceremony spots, the notice at 16:00 and Calder's "Go.",
#             the level 1 arrow; the scene with the pin; the bar on your collar (spec.bar, the kit's mark), the certificate; the cake
#             after it ("Take a slice", Brennan's line); on a Friday at 17:15; missed: by Mail by 18:15
#   seated:   (switch on) Calder's offer finds you sitting the game's own way (lounge and mess seats), live
#   blocked:  (switch on) a guard: you on a seat's own blocked tile, she still arrives (W7's escort fix; fails on 0.94.0)
#   t3toast:  (switch on) the next day at 19:00 in her quarters: the invite, the notice at 18:30, the arrow, the scene,
#             the framed menu; the Training tab's rows done and gone; missed: by Mail
# The Tier 3 parts need a build with the switch on for everything but t3off: python3 promo_beats_check.py ON.html t3before
# (ON.html: P5_STEP5 = true in a copy, plans/handover-b5.md).
# Setup and environment as for cadet_test.py (CADET_WORK, CADET_CHROME).
# Run:  python3 promo_beats_check.py BUILD.html [part ...]   Good is PROMO BEATS CHECK OK (exit 0); a failure exits 1.
import sys, pathlib
exec(open(__file__.replace('promo_beats_check.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
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
  window.__notes = []; deviceNotify = o => { window.__notes.push(String(o && o.text)); };
  window.__said = []; worksSay = (id, t) => { window.__said.push(id + ': ' + t); };
  if (typeof GUIDE !== 'undefined') GUIDE.tq.length = 0;
  window.__w = (day, min, o = {}) => { SHIP.works = null; SHIP.mail = []; SHIP.flags = {}; SHIP.occasions.length = 0; setShipNow((day - 1) * 1440 + min);
    try { repInit().ship.work = 70; } catch (e) { /* no social */ } const W = worksInit(); W.log.push(['x', 1, 0, 'service']); W.cur = null; Object.assign(W.tr, o.tr || {}); W.xp = o.xp || 0; if (o.test) W.test = o.test;
    __toasts.length = 0; __notes.length = 0; __said.length = 0; if (typeof GUIDE !== 'undefined') GUIDE.list.length = 0; return W; };
  window.__friends = () => { for (const id of ['tomas', 'pell', 'rina']) { const r = relGet(id); r.pts = 999; r.tier = relTierOf(999); } };
  window.__mail = () => SHIP.mail.map(m => m.from + ': ' + m.subject + ' | ' + m.body);
  window.__tick = (skip = false) => { for (const f of WORK_TICKS) try { f(shipNow(), skip); } catch (e) { console.error(e); } };
  window.__bay = () => { if (deckDef.num !== 5) goToDeck(5); player.obj.position.copy(cellPos(...ROOM_TILES['w'][0])); };
  window.__rows = d => devDay(d).filter(x => x.kind === 'beat' || x.kind === 'occasion').map(x => hhmm(x.from) + ' ' + x.title);
  return true;
})()"""

def part_off(g):
    print('(off) PROMO_BEATS_ON false:')
    r = g.ev("""(() => { PROMO_BEATS_ON = false; promoBeatsApply(); const W = __w(10, 300, { xp: 5, test: { tier: 2, day: 9, tries: 1, passed: true } });
      return { at: PROMO.summonsAt, occ: OCCASIONS.promoSummons.at, script: OCCASIONS.promoSummons.script, title: OCCASIONS.promoSummons.title, key: promoBK('promo.mail'), cer: promoCerTimes(10), rows: __rows(9).concat(__rows(10)),
        cake: promoCakeWin(10), wait: promoBeatsWalkWait(10 * 1440 - 1440 + 1030), ptr: promoBeatsPtr('t2'), plan: promoPlan() }; })()""")
    print('   ', {k: r[k] for k in ('at', 'occ', 'script', 'key', 'cer', 'rows', 'cake', 'ptr')})
    check(r['at'] == 660 and r['occ'] == 660 and r['script'] == 'promo.officer' and r['title'] == "The Chief's office", f"off: the summons at 11:00, promo.officer, as before ({r})")
    check(r['key'] == 'promo.mail' and r['cer']['at'] == 1035 and r['cake'] == [990, 1020] and not r['wait'] and r['ptr'] == {}, f"off: the old keys, 17:15, the cake 16:30, no wait, no forced pointer ({r})")
    check(not [x for x in r['rows'] if 'Tier 2' in x or 'result' in x or 'pip' in x or 'cabin' in x], f"off: no new Schedule rows ({r['rows']})")
    p = r['plan'] or {}
    check(p and p.get('ceremony', {}).get('at') == 1035 and p['ceremony']['day'] == p['summons']['day'] + 1 and p['summons']['at'] == 660, f"off: promoPlan as before ({p})")

def part_pointer(g):
    print('(pointer) switch on, Teaching arrows Off:')
    g.ev("PROMO_BEATS_ON = true; promoBeatsApply()")
    r = g.ev("""(() => { const W = __w(9, 300, { xp: 45, tr: { m6: 8 }, test: { tier: 2, day: 9, tries: 0, passed: false } });
      setShipNow(8 * 1440 + 541); machinesNow(); careerClock(shipNow(), true); const row = ladderRow('t2'), c = { id: 't2', st: 'ask', by: 'calder', d: 9 }; W.cur = c;
      const okd = WORK_MECH.t2.offer(row, c, 9, shipNow()); const j = SHIP.jobs.find(x => x.id === c.j); if (j && j.found > shipNow()) setShipNow(j.found + 1);
      SHIP.device.settings.teach = 'off'; SHIP.device.pointsSeen = {}; POINT_Q.length = 0; GUIDE.list.length = 0;
      __bay(); ixBoard.open(); guideShift(); __tick();
      const q = POINT_Q.find(x => x.id === 'p:board:lesson:t2'), e = GUIDE.list.find(x => /^promo:test:/.test(x.id));
      return { okd, q: q ? { force: !!q.force, label: q.path.map(s => s.label || '').join('|') } : null, level: e ? e.level : null, rows: __rows(9) }; })()""")
    print('   ', r)
    check(r['q'] and r['q']['force'] and r['q']['label'].endswith('Your Tier 2 test: take it'), f"pointer: the ring on the test's Take it, forced, named ({r['q']})")
    check(r['level'] == 1, f"pointer: the world arrow to the board is level 1 ({r['level']})")
    check(any('09:00 Your Tier 2 test' == x for x in r['rows']), f"pointer: the Schedule's row on the day ({r['rows']})")
    s = g.ev("""(() => { pointFrame(); const cur = POINT.cur && POINT.cur.id, el = document.querySelector('#ptr .ptlab'); const r = { cur, lab: el ? el.textContent : null, shown: !!POINT.el && !POINT.el.hidden }; ixBoard.close(); SHIP.device.settings.teach = 'first'; return r; })()""")
    print('    on screen:', s)
    check(s['cur'] == 'p:board:lesson:t2' and s['shown'] and 'Tier 2 test' in (s['lab'] or ''), f"pointer: drawn on screen with Teaching arrows Off ({s})")

def part_before(g):
    print('(before) the offer, the evening, the morning:')
    r = g.ev("""(() => { const W = __w(8, 1110, { xp: 45, tr: { m6: 8 } }); __friends(); __tick(); const t = W.test;
      const rows = trkItems().filter(x => /Tier 2/.test(x.title)).map(x => (x.later ? 'later ' : '') + x.tag + ' ' + x.title);
      setShipNow(7 * 1440 + 1201); __tick(); const m = __mail();
      __bay(); __said.length = 0; setShipNow(8 * 1440 + 400); __notes.length = 0; __tick(); const n = __notes.slice();
      const s = __said.slice();
      return { t, rows, mail: m, notes: n, said: s }; })()""")
    print('    test', r['t'], '| rows', r['rows'])
    print('    mail', r['mail'])
    print('    morning', r['notes'], r['said'])
    check(r['t'] and r['t']['day'] == 9, f"before: offered on Day 8 at 18:30 for Day 9 ({r['t']})")
    check(any(x.startswith('later 09:00 Your Tier 2 test') for x in r['rows']), f"before: Tracked has the test for tomorrow, from the evening before ({r['rows']})")
    check(len([m for m in r['mail'] if 'Good luck' in m or 'Tomorrow |' in m]) == 2, f"before: two friends wish you luck by Mail at 20:00 ({r['mail']})")
    check(any('Tier 2 test, 09:00' in n for n in r['notes']), f"before: the test morning's notice ({r['notes']})")
    check(any(x.startswith('calder:') and 'Nine' in x for x in r['said']), f"before: Calder's word in the bay that morning ({r['said']})")
    k = g.ev("""(() => { const W = __w(8, 1150, { xp: 45, tr: { m6: 8 }, test: { tier: 2, day: 9, tries: 0, passed: false } }); const a = promoTalkKind(shipNow());
      setShipNow(7 * 1440 + 1300); const b = promoTalkKind(shipNow()); setShipNow(8 * 1440 + 480); const c = promoTalkKind(shipNow()); setShipNow(8 * 1440 + 600); const d = promoTalkKind(shipNow());
      const p = SOC.crew.find(x => x.id === 'pell'), l1 = socLine(p, 'pb.soon', { t: 8 * 1440 + 600, act: 'work', tier: 1, bubble: true }), l2 = socLine(p, 'pb.luck', { t: 8 * 1440 + 480, act: 'breakfast', tier: 3, bubble: true });
      const t15 = socLine(p, 'pb.soon', { t: 14 * 1440 + 600, act: 'work', tier: 1, bubble: true });
      return { kinds: [a, b, c, d].map(x => x && x[0]), soon: l1 && l1.text, luck: l2 && l2.text, soon15: t15 && t15.text }; })()""")
    print('    talk:', k)
    check(k['kinds'] == ['pb.luck', 'pb.luck', 'pb.luck', 'pb.soon'], f"before: the talk's beats: luck (friends; the others how fast) from the offer's evening and that morning, then the day ({k['kinds']})")
    check(k['soon'] and k['luck'] and k['soon15'] and k['soon'] != k['soon15'], f"before: the crew have lines for it, by days aboard ({k})")

def part_passed(g):
    print('(passed) the result held:')
    r = g.ev("""(() => { const W = __w(9, 700, { xp: 45, tr: { m6: 8 }, test: { tier: 2, day: 9, tries: 1, passed: false } }); W.cur = { id: 't2', st: 'do', by: 'calder', d: 9, j: 'x' };
      promoPassed(shipNow()); const sd = promoSummonsDay(); return { tier: W.tier, passed: W.test.passed, said: __said.slice(), mail: __mail(), notes: __notes.slice(), sd, rows: __rows(sd), kind: (promoTalkKind(shipNow()) || [])[0] }; })()""")
    print('   ', r)
    check(r['tier'] == 1 and r['passed'], f"passed: still Tier 1 till the result ({r['tier']})")
    check(any(x.startswith('calder:') for x in r['said']) and any('tomorrow' in m for m in r['mail']) and any('08:15' in m for m in r['mail']) and any('08:15' in n for n in r['notes']), f"passed: Calder's word; the Mail and the notice name tomorrow, 08:15 ({r})")
    check(any(x.startswith('08:15') and 'result' in x for x in r['rows']) and any('pip' in x for x in r['rows']) and any('cabin' in x for x in r['rows']), f"passed: the result day's rows (result, pip, cabin) ({r['rows']})")
    check(r['kind'] == 'pb.passed', f"passed: the crew's talk ({r['kind']})")

def part_result(g):
    print('(result) next shift, the pip the same day:')
    r = g.ev("""(() => { const W = __w(10, 300, { xp: 45, tr: { m6: 8 }, test: { tier: 2, day: 9, tries: 1, passed: true } }); W.tr.t2 = 9; __friends();
      __tick(); const occ = SHIP.occasions.find(x => x.id === 'promoSummons'); setShipNow(9 * 1440 + 361); __tick(); const m1 = __mail();
      const sc = OCCASIONS.promoSummons.script, has = !!MEETING_SCRIPTS[sc]; setShipNow(9 * 1440 + 520); promoPromote(shipNow(), 'met'); __tick();
      const cer = SHIP.occasions.find(x => x.id === 'promoCeremony'); return { occ: occ && [hhmm(occ.at % 1440), OCCASIONS.promoSummons.title], m1, sc, has, tier: W.tier, cer: cer && hhmm(cer.at % 1440), cerDay: cer && Math.floor(cer.at / 1440) + 1,
        mail: __mail(), cake: promoCakeWin(10), steps: devmodePromoSteps().map(s => s.label + ' ' + Math.floor(s.at / 1440 + 1) + ' ' + hhmm(s.at % 1440)), rows: __rows(10) }; })()""")
    print('   ', {k: r[k] for k in ('occ', 'sc', 'has', 'tier', 'cer', 'cerDay', 'cake', 'steps', 'rows')})
    print('    mail', r['mail'])
    check(r['occ'] and r['occ'][0] == '08:15' and 'result' in r['occ'][1], f"result: booked for 08:15, \"Your result\" ({r['occ']})")
    check(any('Your result' in m and '08:15' in m for m in r['m1']), f"result: the Mail at 06:00 ({r['m1']})")
    check(r['sc'] == 'promo.result' and r['has'], f"result: Calder's results scene ({r['sc']}, {r['has']})")
    check(r['tier'] == 2 and r['cer'] == '16:30' and r['cerDay'] == 10, f"result: promoted, the Captain's pip the same day at 16:30 ({r})")
    check(any('16:30' in m and 'pip' in m for m in r['mail']) and any('this afternoon' in m for m in r['mail']), f"result: the invite and the Captain's Mail name this afternoon, 16:30 ({r['mail']})")
    check(r['cake'] == [1020, 1050], f"result: Brennan's cake after the pip ({r['cake']})")
    gw = g.ev("""(() => { const t = 9 * 1440 + 995, a = apptList().find(x => /^promoCeremony@/.test(String(x.occ || x.id))); if (a) ceremonySeat(10);
      return { appt: a ? hhmm(a.at % 1440) : null, with: a ? a.with : [], at: (a ? a.with : []).map(id => { const w = whereIs(evPerson(id), t); return id + ' ' + (w ? w.deck + ' ' + (w.placeId || w.room || '') : '-'); }) }; })()""")
    print('    the guests at 16:35:', gw)
    check(gw['appt'] == '16:30' and gw['with'] and all(' 1 ' in x for x in gw['at']), f"result: the ceremony's guests are booked and on Deck 1 at 16:35 ({gw})")
    f = g.ev("""(() => { let d = 10; while (weekday(d) !== 4) d++; return [d, promoCerTimes(d).at]; })()""")
    check(f[1] == 1035, f"result: on a Friday the pip at 17:15, after the address's hold ({f})")

def part_cabin(g):
    print('(cabin) after dinner:')
    r = g.ev("""(() => { const W = __w(10, 1020, { xp: 5, test: { tier: 2, day: 9, tries: 1, passed: true } }); W.tier = 2; W.rank = 'officer'; W.done.push('summons2'); W.ms.push(['officer', 10]); W.home = 'bunk'; delete W.mv;
      const B = 9 * 1440, out = {}; __bay();
      promoMoveTick(B + 1021); out.beforePip = !!W.mv; W.done.push('ceremony2');
      setShipNow(B + 1060); promoMoveTick(B + 1060); out.noDinner = !!W.mv;
      goToDeck(3); player.obj.position.copy(cellPos(...ROOM_TILES['M'][0])); ACT = { kind: 'eat', o: { fed: true } }; setShipNow(B + 1100); __tick(); out.ate = flag('pb.ate'); ACT = null;
      promoMoveTick(B + 1110); out.inMess = !!W.mv;
      __bay(); setShipNow(B + 1120); promoMoveTick(B + 1120); out.left = !!W.mv; out.mail = __mail().filter(m => /cabin/i.test(m));
      delete W.mv; flagSet('pb.ate', null); setShipNow(B + 1201); promoMoveTick(B + 1201); out.at20 = !!W.mv; return out; })()""")
    print('   ', r)
    check(not r['beforePip'] and not r['noDinner'] and r['ate'] == 10 and not r['inMess'], f"cabin: she waits for the pip, your dinner and your leaving the mess ({r})")
    check(r['left'] and r['at20'], f"cabin: the walk starts once you're out of the mess, or at 20:00 ({r})")

def part_talk(g):
    print('(talk) someone near you in the bay says it:')
    g.ev("(() => { setShipNow(7 * 1440 + 990); socInit(); __bay(); deckCrewFill(); })()"); g.step(10)   # the bay on shift: the crew on the deck drawn (their bubbles' anchors)
    r = g.ev("""(() => { const out = {}, P = player.obj.position, said = [], bs = bubbleSay; bubbleSay = (h, t) => { said.push(t); return true; };
      try { for (const [day, min, test] of [[8, 990, 9], [9, 900, 9]]) {
          __w(day, min, { xp: 45, tr: { m6: 8 }, test: { tier: 2, day: test, tries: 0, passed: false } }); if (day === 9) { const W = SHIP.works; W.test.passed = true; } __bay(); deckCrewFill();
          PB_TALK.at = -1e9; PB_TALK.said.clear(); CHATTER_AT = -1e9; CHAT = null; DIALOGUE = null;
          const a = DECK_CREW.find(x => x.p && x.p.id !== 'calder' && SOC.idx.has(x.p.id)); if (!a) { out[day] = "nobody on the deck (" + DECK_CREW.length + " here, deck " + deckDef.num + ", " + hhmm(shipNow() % 1440) + ")"; continue; }
          const keep = { x: a.x, z: a.z }; a.x = P.x + .6; a.z = P.z; said.length = 0;
          const w = whereIs(a.p, shipNow()); const t = promoTalkTick(shipNow()); Object.assign(a, keep);
          out[day] = { who: a.p.id, act: w && w.act, t: t || null, said: said.slice() }; }
        return out; } finally { bubbleSay = bs; } })()""")
    print('   ', r)
    for day, kind in (('8', 'the evening before'), ('9', 'the test passed')):
        x = r.get(day)
        check(isinstance(x, dict) and x['t'] and x['said'] == [x['t']], f"talk: {kind}, a line from someone beside you in the bay ({x})")

def part_review(g):
    print('(review) RV19 fixes: the result arrow at level 1, she comes out to you in the bay, the 09:00 word, the walk comes to you first:')
    r = g.ev("""(() => { const out = {}; const W = __w(10, 300, { xp: 45, tr: { m6: 8 }, test: { tier: 2, day: 9, tries: 1, passed: true } }); W.tr.t2 = 9;
      __tick(); __bay(); setShipNow(9 * 1440 + 470); GUIDE.list.length = 0; promoGuide(shipNow()); const e = GUIDE.list.find(x => x.id === 'promo:summons'); out.level = e ? e.level : null;
      setShipNow(9 * 1440 + 511); __tick(); const sm = SHIP.occasions.find(x => x.id === 'promoSummons'); out.seek = !!(sm && sm.f && sm.f.seek);
      const W2 = __w(9, 300, { xp: 45, tr: { m6: 8 }, test: { tier: 2, day: 9, tries: 0, passed: false } }); setShipNow(8 * 1440 + 361); machinesNow(); const c = { id: 't2', st: 'ask', by: 'calder', d: 9 }; W2.cur = c;
      __said.length = 0; WORK_MECH.t2.offer(ladderRow('t2'), c, 9, shipNow()); out.early = __said.filter(x => /There it is/.test(x)).length;
      setShipNow(8 * 1440 + 541); __tick(); out.at9 = __said.filter(x => /There it is/.test(x)).length; __tick(); out.at9b = __said.filter(x => /There it is/.test(x)).length;
      const W3 = __w(10, 1201, { xp: 5, test: { tier: 2, day: 9, tries: 1, passed: true } }); W3.tier = 2; W3.rank = 'officer'; W3.done.push('summons2', 'ceremony2'); W3.ms.push(['officer', 10]); W3.home = 'bunk'; delete W3.mv;
      __bay(); __notes.length = 0; promoMoveTick(shipNow()); out.notes = __notes.slice(); out.esc1 = (promoMoveEscort({ id: W3.mv && W3.mv.by }, shipNow()) || {}).mode;
      setShipNow(9 * 1440 + 1217); __tick(); out.esc2 = (promoMoveEscort({ id: W3.mv && W3.mv.by }, shipNow()) || {}).mode; return out; })()""")
    print('   ', r)
    check(r['level'] == 1, f"review M1: the result's arrow is level 1 ({r['level']})")
    check(r['seek'], f"review M2: waiting in the Works bay at 08:31, she comes out to you ({r['seek']})")
    check(r['early'] == 0 and r['at9'] == 1 and r['at9b'] == 1, f"review S1: her \"on the board\" word at 09:00, once, not at 06:01 ({r})")
    check(r['esc1'] == 'follow' and r['esc2'] == 'lead' and any('coming to find you' in n for n in r['notes']), f"review S4: the walk after dinner: she comes to you first, then leads ({r})")

T3 = "typeof P5_PROMO3 !== 'undefined' && P5_PROMO3"
def t3on(g, name):
    on = g.ev(T3)
    if not on: print(f'({name}) P5_PROMO3 off in this build: skipped (run it on a copy with the switch on)')
    return on

def part_t3off(g):
    if g.ev(T3):   # (W6) the build ships it on from 0.94.0: the off part on a copy with P5_STEP5 switched off
        src = pathlib.Path(sys.argv[1]).read_text(); off = re.sub(r"^const P5_STEP5 = true;", 'const P5_STEP5 = false;', src, count=1, flags=re.M)
        if off == src: print('(t3off) P5_PROMO3 on in this build and no switch line to turn off: skipped'); return
        cp = WORK / 'test' / f'_pb_t3off_{os.getpid()}_{pathlib.Path(sys.argv[1]).name}'; cp.write_text(off); _RUN_FILES.append(cp)
        print('(t3off) on a copy with P5_STEP5 switched off'); h = Game(pw, str(cp)); h.step(2); check(h.ev(SETUP), 'setup (t3off copy)')
        try: part_t3off(h)
        finally: h.close()
        return
    print('(t3off) P5_PROMO3 off: nothing of the Senior Officer promotion:')
    r = g.ev("""(() => { const W = __w(14, 1146, { xp: 60, tr: { ps: 12, t2: 9 } }); W.tier = 2; W.rank = 'officer'; __friends(); __bay();
      for (const t of [13 * 1440 + 500, 13 * 1440 + 1146, 13 * 1440 + 1201, 13 * 1440 + 1330, 14 * 1440 + 400]) { setShipNow(t); __tick(); }
      return { mech: !!WORK_MECH.t3, ready: typeof puReady === 'function' && puReady(14), pu: SHIP.works.pu || null, rows: __rows(15).filter(x => /Tier 3/.test(x)),
        flags: Object.keys(SHIP.flags).filter(k => /pu3/.test(k)), mail: __mail().filter(m => /Tier 3/.test(m)), notes: __notes.filter(n => /Tier 3/.test(n)), said: __said.filter(x => /Tier 3|Relied on/.test(x)), dlg: DIALOGUE && DIALOGUE.id }; })()""")
    print('   ', r)
    check(not r['mech'] and not r['ready'] and not r['pu'] and not r['rows'] and not r['flags'] and not r['mail'] and not r['notes'] and not r['said'] and not r['dlg'], f"t3off: nothing happens ({r})")

T3_W = "const W = __w(14, 470, { xp: 60, tr: { ps: 12, t2: 9 } }); W.tier = 2; W.rank = 'officer'; __friends();"
def part_t3before(g):
    if not t3on(g, 't3before'): return
    print('(t3before) the offer in person, then the record; the evening; the morning:')
    r = g.ev("""(() => { """ + T3_W + """ __bay(); const out = { party: puPartyAt(14) };
      setShipNow(13 * 1440 + 500); __tick(); out.earlySeek = !!PU_LIVE.seek;   // the party's day: she waits for the party
      setShipNow(13 * 1440 + 1146); goToDeck(3); player.obj.position.copy(cellPos(...ROOM_TILES['L'][0])); __tick();
      out.seek = !!PU_LIVE.seek; out.esc = (puEscort({ id: 'calder' }, shipNow()) || {}).mode; out.before = !!puT3();
      const keep = puNearMe; puNearMe = id => id === 'calder' ? true : keep(id); __tick(); puNearMe = keep;
      out.dlg = DIALOGUE ? DIALOGUE.m.id : null; out.first = DIALOGUE ? DIALOGUE.queue[0].text : null; out.during = !!puT3();
      let n = 0; while (DIALOGUE && n++ < 30) { const l = DIALOGUE.queue[DIALOGUE.i]; dialogueStep(l && l.choice ? 1 : undefined); }
      out.t3 = puT3(); out.reply = flag('pu3.reply'); out.notes = __notes.filter(x => /Tier 3/.test(x)); out.mail = __mail().filter(m => /Tier 3/.test(m));
      out.rows = __rows(15); out.trk = trkItems().filter(x => /Tier 3/.test(x.title)).map(x => (x.later ? 'later ' : '') + x.tag + ' ' + x.title);
      out.next = worksNext(); out.tab = JSON.stringify(puCheck()); out.esc2 = (puEscort({ id: 'calder' }, shipNow()) || {}).mode || null;
      setShipNow(13 * 1440 + 1201); __tick(); out.luck = __mail().filter(m => /Good luck|Tomorrow \\|/.test(m));
      out.kinds = [puTalkKind(13 * 1440 + 1100), puTalkKind(14 * 1440 + 480), puTalkKind(14 * 1440 + 600)].map(x => x && x[0]);
      const p = SOC.crew.find(x => x.id === 'pell'), l1 = socLine(p, 'pu3.soon', { t: 13 * 1440 + 600, act: 'work', tier: 1, bubble: true }), l2 = socLine(p, 'pu3.luck', { t: 14 * 1440 + 480, act: 'breakfast', tier: 3, bubble: true });
      out.lines = [l1 && l1.text, l2 && l2.text]; return out; })()""")
    for k in ('party', 'earlySeek', 'seek', 'esc', 'before', 'dlg', 'first', 'during', 't3', 'reply', 'notes', 'rows', 'trk', 'next', 'esc2', 'kinds', 'lines'): print('   ', k, r[k])
    print('    mail', r['mail'] + r['luck'])
    check(r['party'] == 1140 and not r['earlySeek'] and r['seek'] and r['esc'] == 'follow' and not r['before'], f"t3before: on the party's day she comes to find you at the party (her escort follows you), the test not set yet ({r})")
    check(r['dlg'] == 'pu3.offer.party' and r['first'] and not r['during'], f"t3before: next to you, her party scene, in person first ({r['dlg']}, {r['first']})")
    check(r['t3'] and r['t3']['day'] == 15 and r['t3']['tries'] == 0 and not r['t3']['passed'] and r['reply'] == 2 and r['esc2'] is None, f"t3before: at its end the test is set for Day 15, your reply kept, she stops following ({r['t3']})")
    check(any('tomorrow, 09:00' in n for n in r['notes']) and any(m.startswith('Chief Ines Calder: Your Tier 3 test |') and 'tomorrow' in m for m in r['mail']), f"t3before: then the urgent notice and the Mail, the record ({r['notes']}, {r['mail']})")
    check('09:00 Your Tier 3 test' in r['rows'] and any(x.startswith('later 09:00 Your Tier 3 test') for x in r['trk']), f"t3before: the Schedule and Tracked have the test ({r['rows']}, {r['trk']})")
    check('Tier 3 test' in r['next'] and 'Test job: tomorrow, 09:00' in r['tab'] and 'Power safety' in r['tab'], f"t3before: What's next and the Training tab ({r['next']}, {r['tab']})")
    check(len(r['luck']) == 2, f"t3before: two friends wish you luck by Mail at 20:00 ({r['luck']})")
    check(r['kinds'] == ['pu3.luck', 'pu3.luck', 'pu3.soon'] and all(r['lines']), f"t3before: the talk: luck from friends the evening before and the morning, then how fast it came; the crew have lines ({r['kinds']}, {r['lines']})")
    r = g.ev("""(() => { """ + T3_W + """ __bay(); const out = {}; setShipNow(14 * 1440 + 490); __tick(); out.mon = PU_LIVE.seek && PU_LIVE.seek.d;   // Day 15, no party: from 08:00
      const keep = puNearMe; puNearMe = id => id === 'calder' ? true : keep(id); __tick(); puNearMe = keep; out.dlg = DIALOGUE ? DIALOGUE.m.id : null; while (DIALOGUE) dialogueStep(0);
      out.t3 = puT3(); (() => { """ + T3_W + """ })(); __bay(); setShipNow(14 * 1440 + 490); __tick(); setShipNow(14 * 1440 + 1321); __tick(); out.late = puT3(); out.lateMail = __mail().filter(m => /I came to find you/.test(m)).length; return out; })()""")
    print('   ', r)
    check(r['mon'] == 15 and r['dlg'] == 'pu3.offer' and r['t3'] and r['t3']['day'] == 16, f"t3before: on a later day, from 08:00, \"tomorrow\" ({r})")
    check(r['late'] and r['late']['day'] == 16 and r['lateMail'] == 1, f"t3before: not found by 22:00, it comes by Mail ({r})")

# ---- Step 6, S6-3 (W6): the Engine Specialist promotion. t4off on the build as shipped (P5_STEP6 off: nothing); the rest
# on a copy with P5_STEP6 switched on (const P5_STEP6 = P5_STEP5 && true;)
T4 = "typeof P5_PROMO4 !== 'undefined' && P5_PROMO4"
def t4on(g, name):
    on = g.ev(T4)
    if not on: print(f'({name}) P5_PROMO4 off in this build: skipped (run it on a copy with P5_STEP6 on)')
    return on
T4_W = "const W = __w(19, 470, { xp: 60, tr: { ps: 12, t2: 9, t3: 15, m19: 17 } }); W.tier = 3; W.rank = 'senior'; __friends();"
def part_t4off(g):
    if g.ev(T4):   # (BM19) switched on in 0.95.0: the off part on a copy with P5_STEP6 back to its off line
        src = pathlib.Path(sys.argv[1]).read_text(); off = re.sub(r"^const P5_STEP6 = P5_STEP5 && true;", "const P5_STEP6 = P5_STEP5 && URL_FLAGS.has('p5s6');", src, count=1, flags=re.M)
        if off == src: print('(t4off) P5_PROMO4 on in this build and no switch line to turn off: skipped'); return
        cp = WORK / 'test' / f'_pb_t4off_{os.getpid()}_{pathlib.Path(sys.argv[1]).name}'; cp.write_text(off); _RUN_FILES.append(cp)
        print('(t4off) on a copy with P5_STEP6 switched off'); h = Game(pw, str(cp)); h.step(2); check(h.ev(SETUP), 'setup (t4off copy)')
        try: part_t4off(h)
        finally: h.close()
        return
    print('(t4off) P5_PROMO4 off: nothing of the Engine Specialist promotion:')
    r = g.ev("""(() => { """ + T4_W + """ __bay();
      for (const t of [18 * 1440 + 500, 18 * 1440 + 900, 20 * 1440 + 1090, 20 * 1440 + 1330]) { setShipNow(t); __tick(); }
      return { ready: typeof pu4Ready === 'function' && pu4Ready(19), t4: !!(SHIP.works.pu && SHIP.works.pu.t4), rows: __rows(22).filter(x => /Tier 4/.test(x)),
        flags: Object.keys(SHIP.flags).filter(k => /pu4/.test(k)), mail: __mail().filter(m => /Tier 4/.test(m)), notes: __notes.filter(n => /Tier 4/.test(n)), dlg: DIALOGUE && DIALOGUE.id, tab: JSON.stringify(puCheck()) }; })()""")
    print('   ', r)
    check(not r['ready'] and not r['t4'] and not r['rows'] and not r['flags'] and not r['mail'] and not r['notes'] and not r['dlg'] and 'Tier 4' not in r['tab'], f"t4off: nothing happens ({r})")
def part_t4before(g):
    if not t4on(g, 't4before'): return
    print('(t4before) the offer in person (Friday), the record, the rows; the weekend: Sunday dinner; by Mail at 22:00:')
    r = g.ev("""(() => { """ + T4_W + """ __bay(); const out = { ready18: pu4Ready(18), ready: pu4Ready(19) };
      setShipNow(18 * 1440 + 470); __tick(); out.early = !!PU4_LIVE.seek; setShipNow(18 * 1440 + 481); __tick(); out.held = !!PU4_LIVE.seek; setShipNow(18 * 1440 + 501); __tick();   // Friday 08:00-08:20 is the Senior briefing's held hour: after it
      out.seek = !!PU4_LIVE.seek; out.esc = (p5Escort({ id: 'calder' }, shipNow()) || {}).mode; out.before = !!puT4();
      const keep = puNearMe; puNearMe = id => id === 'calder' ? true : keep(id); __tick(); puNearMe = keep;
      out.dlg = DIALOGUE ? DIALOGUE.m.id : null; out.during = !!puT4();
      let n = 0; while (DIALOGUE && n++ < 30) { const l = DIALOGUE.queue[DIALOGUE.i]; dialogueStep(l && l.choice ? 1 : undefined); }
      out.t4 = puT4(); out.reply = flag('pu4.reply'); out.notes = __notes.filter(x => /Tier 4/.test(x)); out.mail = __mail().filter(m => /Tier 4/.test(m));
      out.rows = __rows(22); out.next = worksNext(); out.tab = JSON.stringify(puCheck()); out.esc2 = (p5Escort({ id: 'calder' }, shipNow()) || {}).mode || null;
      setShipNow(20 * 1440 + 1201); __tick(); out.luck = __mail().filter(m => /Good luck/.test(m)).length;
      const keep2 = JSON.stringify(SHIP.works.pu || {}); const c = pu4Clean(JSON.parse(keep2).t4); out.clean = JSON.stringify(c) === JSON.stringify(puT4()); out.junk = pu4Clean({ day: 'x' });
      return out; })()""")
    for k in ('held', 'ready18', 'ready', 'early', 'seek', 'esc', 'before', 'dlg', 'during', 't4', 'reply', 'notes', 'mail', 'rows', 'next', 'tab', 'esc2', 'luck', 'clean', 'junk'): print('   ', k, r[k])
    check(not r['ready18'] and r['ready'] and not r['early'] and not r['held'] and r['seek'] and r['esc'] == 'follow' and not r['before'], f"t4before: from Friday Day 19, 08:00 (after the briefing's hold to 08:20), she comes to find you (her escort follows you), the test not set yet ({r})")
    check(r['dlg'] == 'pu4.offer' and not r['during'], f"t4before: next to you, her scene, in person first ({r['dlg']})")
    check(r['t4'] and r['t4']['day'] == 22 and r['t4']['tries'] == 0 and not r['t4']['passed'] and r['reply'] == 2 and r['esc2'] is None, f"t4before: at its end the test is set for Monday Day 22, your reply kept, she stops following ({r['t4']})")
    check(any('Tier 4' in n and '09:30' in n for n in r['notes']) and any(m.startswith('Chief Ines Calder: Your Tier 4 test |') for m in r['mail']), f"t4before: then the urgent notice and the Mail, the record ({r['notes']}, {r['mail']})")
    check(any('09:30' in x and 'Tier 4' in x for x in r['rows']) and 'Tier 4' in r['next'] and 'Power and relays' in r['tab'] and 'Test job' in r['tab'], f"t4before: the Schedule, What's next and the Training tab ({r['rows']}, {r['next']}, {r['tab']})")
    check(r['luck'] == 2 and r['clean'] and r['junk'] is None, f"t4before: two friends' Mail at 20:00 on Sunday; the save's record read back, junk dropped ({r['luck']}, {r['clean']}, {r['junk']})")
    r = g.ev("""(() => { const out = {}; (() => { """ + T4_W + """ })(); __bay();
      setShipNow(19 * 1440 + 600); __tick(); out.sat = !!PU4_LIVE.seek;   // Saturday: she waits for Sunday dinner
      setShipNow(20 * 1440 + 600); __tick(); out.sunAm = !!PU4_LIVE.seek; setShipNow(20 * 1440 + 1081); __tick(); out.sunDinner = !!PU4_LIVE.seek;
      setShipNow(20 * 1440 + 1321); __tick(); out.late = puT4(); out.lateMail = __mail().filter(m => /Tier 4/.test(m)).length; return out; })()""")
    print('   ', r)
    check(not r['sat'] and not r['sunAm'] and r['sunDinner'], f"t4before: Trusted at the weekend, she comes at Sunday dinner, not before ({r})")
    check(r['late'] and r['late']['day'] == 22 and r['lateMail'] == 1, f"t4before: not found by 22:00, it comes by Mail, the test still Monday ({r})")

T4_TEST = """const W = __w(22, 300, { xp: 60, tr: { ps: 12, t2: 9, t3: 15, m19: 17 } }); W.tier = 3; W.rank = 'senior'; __friends();
      for (const r of CAREER_LADDER) if (r.id !== 't4' && r.tier <= 3 && r.day <= 21) { W.tr[r.id] = W.tr[r.id] || 9; (W.op[9] = W.op[9] || []).push(r.id); }
      pu4Set(22); flagSet('pu4.told', 19); flagSet('pu4.notice', 19); setShipNow(21 * 1440 + 361); machinesNow(); careerClock(shipNow(), true); __bay();"""
def part_t4test(g):
    if not t4on(g, 't4test'): return
    print('(t4test) the test morning, the board, each step, passing; set again if not taken:')
    r = g.ev("""(() => { """ + T4_TEST + """ __tick(); const out = { notes: __notes.filter(x => /Tier 4/.test(x)) };
      setShipNow(21 * 1440 + 545); __tick(); out.day = GUIDE.list.filter(e => /^pu4/.test(e.id)).map(e => e.id + ' L' + e.level);
      setShipNow(21 * 1440 + 571); __tick(); const c = W.cur, j = c && SHIP.jobs.find(x => x.id === c.j);
      out.cur = c && c.id + ' ' + c.st; out.job = j && { slot: j.reserved, mach: j.mach, kind: j.kind, found: hhmm(j.found % 1440), until: hhmm(j.until % 1440), part: SHIP.stores['coil winding'] };
      out.ptr = puPtr('t4'); out.board = GUIDE.list.filter(e => /^pu4:test:/.test(e.id)).map(e => (e.goal() || {}).label);
      if (!j) return out;
      const arrow = () => GUIDE.list.filter(e => /^pu4:step/.test(e.id)).map(e => (e.goal() || {}).label || '').join('|');
      __said.length = 0; out.take = claimJob(j.id); __tick(); out.said = __said.slice(); out.esc = (worksEscort({ id: 'calder' }, shipNow()) || {}).mode; out.a0 = arrow();
      out.stops = jobStops(j).map(x => x.step); SHIP.player.carry.push('coil winding');
      out.order = jobStepDone(j.id, 2).ok;   // the winding before the reading: refused
      out.r = jobStops(j).map((x, k) => jobStepDone(j.id, k).ok); out.done = !!j.workDone; out.cond = SHIP.machines[j.mach].cond; out.a1 = arrow();
      __said.length = 0; __notes.length = 0; out.turnin = turnInJob(j.id); __tick(); out.t4 = puT4(); out.tr = W.tr.t4; out.cur2 = W.cur; out.passed = __said.slice();
      out.mail = __mail().filter(m => /Your test/.test(m)); out.notes2 = __notes.slice(); return out; })()""")
    for k, v in r.items(): print('   ', k, v)
    check(any('Tier 4' in n for n in r['notes']) and r['day'] and r['day'][0].startswith('pu4:testday:22 L1'), f"t4test: the morning's notice and a level 1 arrow to the board from 09:00 ({r['notes']}, {r['day']})")
    check(r['cur'] == 't4 do' and r['job'] and r['job']['slot'] == 26 and r['job']['mach'] in ('6-coil-1', '6-coil-2', '6-coil-3') and r['job']['kind'] == 'tier4' and r['job']['found'] == '09:30' and r['job']['until'] == '12:30' and r['job']['part'] >= 1, f"t4test: 09:30, the test on the board, held for you to 12:30 in slot 26, on a drive coil, its winding on the shelf ({r['cur']}, {r['job']})")
    check(r['ptr'] and r['ptr']['force'] and 'Tier 4' in r['ptr']['label'] and r['board'] == ['Your Tier 4 test: take it'], f"t4test: the board's ring and the arrow: take it ({r['ptr']}, {r['board']})")
    check(r['take'] and r['esc'] == 'follow' and r['said'] and 'winding' in r['a0'], f"t4test: taken, Calder's word, she follows you, the arrow to the winding ({r['said']}, {r['esc']}, {r['a0']})")
    check(r['stops'] == ['fetch', 'isolate', 'read', 'wind', 'cycle'] and not r['order'] and all(r['r']) and r['done'] and r['cond'] >= 95 and r['a1'] == 'Turn it in', f"t4test: fetch, off the cycle, read, wind, back in: in order; the coil put right ({r['stops']}, {r['order']}, {r['r']}, {r['cond']}, {r['a1']})")
    check(r['turnin'] and r['t4']['passed'] and r['tr'] == 22 and r['cur2'] is None and any('I\'ll find you' in x for x in r['passed']) and r['mail'] and any('Tier 4' in n for n in r['notes2']), f"t4test: turned in: passed, Calder's \"I'll find you\", the Mail and the notice ({r['t4']}, {r['passed']}, {r['mail']}, {r['notes2']})")
    r = g.ev("""(() => { """ + T4_TEST + """ __tick(); setShipNow(21 * 1440 + 571); __tick(); const out = {};
      for (let t = 21 * 1440 + 600; t <= 21 * 1440 + 1100; t += 30) { setShipNow(t); machinesNow(); worksCareerTick(t); __tick(); }
      out.t4 = puT4(); out.cur = W.cur && W.cur.id + ' ' + W.cur.st; out.mail = __mail().filter(m => /^Chief Ines Calder: Again/.test(m)).length; out.jobs = SHIP.jobs.filter(x => x.kind === 'tier4' && x.status !== 'done').length; return out; })()""")
    print('   ', r)
    check(r['t4'] and not r['t4']['passed'] and r['t4']['day'] > 22 and r['mail'] == 1 and r['jobs'] == 0, f"t4test: not taken: never failed, set again two workdays on, by her word and Mail ({r})")

T3_TEST = """const W = __w(15, 300, { xp: 60, tr: { ps: 12, t2: 9 } }); W.tier = 2; W.rank = 'officer'; __friends();
      for (const r of CAREER_LADDER) if (r.id !== 't3' && r.tier <= 2) { W.tr[r.id] = W.tr[r.id] || 9; (W.op[9] = W.op[9] || []).push(r.id); }
      puSet(15); flagSet('pu3.told', 14); flagSet('pu3.notice', 14); setShipNow(14 * 1440 + 361); machinesNow(); careerClock(shipNow(), true); __bay();"""
# ---- S6-3 turn 3 (W7): the result when your shift starts (Day 22, 22:40), and the Captain's engine badge
T4_RES = """if (typeof DIALOGUE !== 'undefined' && DIALOGUE) dialogueEnd(false); DIALOGUE = null; if (typeof P5N_SEEK !== 'undefined') P5N_SEEK.kind = null;   /* an earlier part (t4test) may leave 28a's night word open */
      const W = __w(22, 760, { xp: 60, tr: { ps: 12, t2: 9, t3: 15, m19: 17, t4: 22 } }); W.tier = 3; W.rank = 'senior'; __friends();
      const T = pu4Set(22); T.passed = true; T.tries = 1; flagSet('p5n.on', 22);"""
def part_t4passed(g):
    if not t4on(g, 't4passed'): return
    print('(t4passed) the result at 22:40: Calder finds you and says it; asleep, a knock; not found, by Mail:')
    r = g.ev("""(() => { """ + T4_RES + """ const out = { when: hhmm(pu4ResWhen() % 1440) }; setShipNow(21 * 1440 + 1300); __bay(); __tick();
      out.next = worksNext(); out.rows = __rows(22).filter(x => /result/i.test(x));
      setShipNow(21 * 1440 + 1361); goToDeck(1); __tick(); out.seek = !!PU4_LIVE.rseek; out.esc = (worksEscort({ id: 'calder' }, shipNow()) || {}).mode;
      out.fetch = typeof pu4Fetches === 'function' && pu4Fetches(shipNow()); out.n1 = __notes.filter(n => /Night shift now/.test(n)).length;
      const keep = puNearMe; puNearMe = (id, r) => id === 'calder' ? true : keep(id, r); __said.length = 0; __tick();
      out.walk = !!PU4_LIVE.walk; out.dlg0 = DIALOGUE && DIALOGUE.id; out.found = __said.filter(x => /^calder/.test(x)); out.lead = JSON.stringify((worksEscort({ id: 'calder' }, shipNow()) || {}).to || null);
      if (PU4_LIVE.walk && typeof p5nNight === 'function') { p5nNight(22).in = shipNow(); } out.lead2 = JSON.stringify((worksEscort({ id: 'calder' }, shipNow()) || {}).to || null);
      goToDeck(6); setShipNow(21 * 1440 + 1370); __tick(); puNearMe = keep;
      out.dlg = DIALOGUE && DIALOGUE.id; """ + dlg_run(0) + """
      out.w = [W.tier, W.rank, W.xp]; out.t4 = puT4(); out.ms = W.ms.filter(x => /^specialist/.test(x[0])); out.mail = __mail().filter(m => /^Chief Ines Calder: Your result/.test(m)).length;
      out.invite = __mail().filter(m => /^Captain Odile Marrow: Your badge/.test(m)); out.badge = SHIP.occasions.filter(x => x.id === 'pu4Badge').map(x => hhmm(x.at % 1440) + ' day ' + (Math.floor(x.at / 1440) + 1));
      const a = apptList().find(x => /^pu4Badge@/.test(String(x.occ))); out.places = a && a.places; out.next2 = worksNext(); out.rec = worksRecordHead().text;
      """ + T4_RES.replace('const W =', 'const W2 =').replace('W.', 'W2.').replace('const T = pu4Set', 'const T2 = pu4Set').replace('T.passed', 'T2.passed').replace('T.tries', 'T2.tries') + """
      __notes.length = 0; setShipNow(21 * 1440 + 1361); sleeping = true; __tick(true); sleeping = false; out.knock = [W2.tier, (puT4() || {}).res, __notes.filter(n => /knock/i.test(n)).length];
      """ + T4_RES.replace('const W =', 'const W3 =').replace('W.', 'W3.').replace('const T = pu4Set', 'const T3 = pu4Set').replace('T.passed', 'T3.passed').replace('T.tries', 'T3.tries') + """
      setShipNow(21 * 1440 + 1361); __tick(); setShipNow(21 * 1440 + 1392); __tick(); out.late = [W3.tier, (puT4() || {}).res, __mail().filter(m => /Your result/.test(m)).length]; return out; })()""")
    for k, v in r.items(): print('   ', k, v)
    check(r['when'] == '22:40' and '22:40' in r['next'] and r['rows'] and r['rows'][0].startswith('22:40'), f"t4passed: the result when the night starts, 22:40; What's next and the Schedule say so ({r['when']}, {r['next']}, {r['rows']})")
    check(r['seek'] and r['esc'] == 'follow' and r['dlg'] == 'pu4.stairs', f"t4passed: 22:40, she comes to find you where you are; her words in person ({r['seek']}, {r['esc']}, {r['dlg']})")
    if r['walk']: check(r['fetch'] and r['n1'] == 0 and not r['dlg0'] and r['found'] and '"deck":5' in r['lead'] and '"deck":6' in r['lead2'], f"t4passed (nights on): night 1's own notice held back, she finds you and walks you down: the time clock first, then the engine room; her words on the way ({r['fetch']}, {r['n1']}, {r['dlg0']}, {r['found']}, {r['lead']}, {r['lead2']})")
    check(r['w'] == [4, 'specialist', 0] and r['t4']['res'] == 22 and r['ms'] == [['specialist', 22]] and r['mail'] == 1, f"t4passed: Tier 4, Engine Specialist, xp 0, the milestone, the Mail as the record ({r['w']}, {r['ms']}, {r['mail']})")
    check(r['badge'] == ['16:30 day 23'] and r['invite'] and '16:30' in r['invite'][0] and r['places'] and r['places'].get('marrow') == '1-ceremony-captain' and len(r['places']) == 4, f"t4passed: the badge booked for 16:30 the next day, the Captain's invite, the four on their spots ({r['badge']}, {r['invite']}, {r['places']})")
    check('engine badge' in r['next2'] and 'Specialist · ' not in r['rec'], f"t4passed: What's next names the badge; the Record says Engine Specialist once ({r['next2']}, {r['rec']})")
    check(r['knock'] == [4, 22, 1], f"t4passed: asleep at 22:40, she knocks: a notice, the night is yours ({r['knock']})")
    check(r['late'] == [4, 22, 1], f"t4passed: not found in 30 minutes, by Mail ({r['late']})")

def part_t4welcome(g):
    if not t4on(g, 't4welcome'): return
    if not g.ev("typeof P5_NIGHT !== 'undefined' && P5_NIGHT"): print('(t4welcome) P5_NIGHT off: no welcome (skipped)'); return
    print('(t4welcome) Day 23 06:00, the shift change: both crews, Torres\'s speech, the certificate signed; missed: by Mail:')
    r = g.ev("""(() => { """ + T4_RES + """ const out = {}; pu4Promote(21 * 1440 + 1361, 'met'); p5nNight(22).in = 21 * 1440 + 1366;
      setShipNow(22 * 1440 + 346); __tick(); out.occ = SHIP.occasions.filter(x => x.id === 'pu4Welcome').map(x => hhmm(x.at % 1440) + ' day ' + (Math.floor(x.at / 1440) + 1));
      out.arrow = GUIDE.list.filter(e => e.id === 'pu4:welcome').map(e => e.level + ' ' + (e.goal() || {}).label); const a = apptList().find(x => /^pu4Welcome@/.test(String(x.occ))); out.with = a && a.with;
      setShipNow(22 * 1440 + 361); goToDeck(6); player.obj.position.copy(cellPos(...ROOM_TILES['E'][Math.floor(ROOM_TILES['E'].length / 2)])); occasionsTick(shipNow()); meetingsTick(shipNow());
      out.dlg = DIALOGUE && DIALOGUE.id; """ + dlg_run(1) + """ out.signed = flag('pu4.signed'); pu4Badge(22 * 1440 + 1000, 'met'); out.keep = (SHIP.social && SHIP.social.keepsakes || []).map(k => k.what).filter(k => /Specialist/.test(k));
      """ + T4_RES.replace('const W =', 'const W2 =').replace('W.', 'W2.').replace('const T = pu4Set', 'const T2 = pu4Set').replace('T.passed', 'T2.passed').replace('T.tries', 'T2.tries') + """
      pu4Promote(21 * 1440 + 1361, 'met'); p5nNight(22).in = 21 * 1440 + 1366; setShipNow(22 * 1440 + 346); __tick(); setShipNow(22 * 1440 + 391); __tick();
      out.missed = [flag('pu4.signed'), __mail().filter(m => /We signed it anyway/.test(m)).length];
      """ + T4_RES.replace('const W =', 'const W3 =').replace('W.', 'W3.').replace('const T = pu4Set', 'const T3 = pu4Set').replace('T.passed', 'T3.passed').replace('T.tries', 'T3.tries') + """
      pu4Promote(21 * 1440 + 1361, 'mail'); setShipNow(22 * 1440 + 361); __tick(); out.none = SHIP.occasions.filter(x => x.id === 'pu4Welcome').length; return out; })()""")
    for k, v in r.items(): print('   ', k, v)
    check(r['occ'] == ['06:00 day 23'] and r['arrow'] and r['arrow'][0].startswith('1 ') and r['with'] and 'reyes-alejandro' in r['with'] and 'torres-zeke' in r['with'], f"t4welcome: booked for 06:00, both crews, a level 1 arrow from 05:45 ({r['occ']}, {r['arrow']}, {r['with']})")
    check(r['dlg'] == 'pu4.welcome' and r['signed'] == 23 and r['keep'] and 'signed' in r['keep'][0], f"t4welcome: the speech, the certificate signed, the signed one at the badge ({r['dlg']}, {r['signed']}, {r['keep']})")
    check(r['missed'] == [23, 1] and r['none'] == 0, f"t4welcome: missed: Torres's Mail; night 1 not worked: no welcome ({r['missed']}, {r['none']})")

def part_t4badge(g):
    if not t4on(g, 't4badge'): return
    print('(t4badge) the Captain pins your engine badge; your Deck 2 quarters said there first:')
    r = g.ev("""(() => { """ + T4_RES + """ const out = {}; pu4Promote(21 * 1440 + 1361, 'met');
      __notes.length = 0; setShipNow(22 * 1440 + 800); __bay(); __tick(); out.wake = __notes.slice(); out.rows = __rows(23).filter(x => /badge/.test(x));
      __notes.length = 0; __said.length = 0; setShipNow(22 * 1440 + 961); __tick(); out.notice = __notes.slice();
      setShipNow(22 * 1440 + 976); goToDeck(4); __tick(); out.arrow = GUIDE.list.filter(e => e.id === 'pu4:badge').map(e => e.level + ' ' + (e.goal() || {}).label + ' ' + (e.goal() || {}).place);
      setShipNow(22 * 1440 + 991); goToDeck(1); player.obj.position.copy(cellPos(...PLACE_OF.get('1-ceremony-you').at)); occasionsTick(shipNow()); meetingsTick(shipNow());
      out.dlg = DIALOGUE && DIALOGUE.id; out.pin = 0; """ + dlg_run(0) + """ out.t4 = puT4(); out.keep = (SHIP.social && SHIP.social.keepsakes || []).map(k => k.what);
      out.quarters = __mail().filter(m => /^Chief Ines Calder: Your quarters/.test(m)); out.rec = worksRecordHead().text;
      """ + T4_RES.replace('const W =', 'const W2 =').replace('W.', 'W2.').replace('const T = pu4Set', 'const T2 = pu4Set').replace('T.passed', 'T2.passed').replace('T.tries', 'T2.tries') + """
      pu4Promote(21 * 1440 + 1361, 'met'); setShipNow(22 * 1440 + 1006); sleeping = true; __tick(true); sleeping = false;
      out.wait = [flag('pu4.badge.wait'), pu4BadgeDay(), SHIP.occasions.filter(x => x.id === 'pu4Badge' && x.status === 'asked').map(x => Math.floor(x.at / 1440) + 1)];
      setShipNow(23 * 1440 + 1096); __tick(); out.missed = [(puT4() || {}).badge, __mail().filter(m => /^Captain Odile Marrow: Your badge \\| We missed/.test(m)).length]; return out; })()""")
    for k, v in r.items(): print('   ', k, v)
    check(any('16:30' in n and 'badge' in n for n in r['wake']) and r['rows'] and r['rows'][0].startswith('16:30'), f"t4badge: the notice as you wake, the Schedule's row ({r['wake']}, {r['rows']})")
    check(any('Go now' in n for n in r['notice']) and r['arrow'] and r['arrow'][0].startswith('1 ') and '1-ceremony-you' in r['arrow'][0], f"t4badge: 16:00 'Go now', a level 1 arrow from 16:15 to your spot ({r['notice']}, {r['arrow']})")
    check(r['dlg'] == 'pu4.badge' and r.get('pin') and r['t4']['badge'] == 23 and r['t4']['move'] and r['t4']['move']['ready'] == 25, f"t4badge: the scene with the pin; your quarters ready for Thursday Day 25 ({r['dlg']}, {r['t4']})")
    check(r['quarters'] and 'Thursday' in r['quarters'][0] and any('Engine Specialist' in k for k in r['keep']) and 'Senior Officer, Engine Specialist, Day 23' in r['rec'], f"t4badge: Calder's Mail as the record, the certificate, the Record's line ({r['quarters']}, {r['keep']}, {r['rec']})")
    check(r['wait'][0] == 1 and r['wait'][1] == 24 and 24 in r['wait'][2], f"t4badge: asleep at 16:45, the Captain waits until the next afternoon ({r['wait']})")
    check(r['missed'] == [24, 1], f"t4badge: awake and not there, by Mail by 18:15 ({r['missed']})")

# ---- S6-3 turn 4 (W7): your quarters on Deck 2, Vance's walk after dinner; open till 22:00, then the next day; laundry collected
T4_MOVE = """const W = __w(25, 300, { xp: 10, tr: { ps: 12, t2: 9, t3: 15, m19: 17, t4: 22 } }); W.tier = 4; W.rank = 'specialist'; __friends();
      const T = pu4Set(22); T.passed = true; T.tries = 1; T.res = 22; T.badge = 23; T.move = { ready: 25, walked: null, refit: false }; PU4_LIVE.mv = null; flagSet('p5n.on', 22); flagSet('p5n.off', 25);"""
def part_t4move(g):
    if not t4on(g, 't4move'): return
    print('(t4move) Thursday: the notice, the Mail, Vance after dinner, room B on Deck 2; late: the next day; laundry collected:')
    r = g.ev("""(() => { """ + T4_MOVE + """ const out = {}; setShipNow(24 * 1440 + 400); __bay(); __tick(); out.wake = __notes.slice(); out.rows = __rows(25).filter(x => /quarters/.test(x)); out.next = worksNext();
      setShipNow(24 * 1440 + 1021); __tick(); out.mail = __mail().filter(m => /^Chief Ines Calder: Tonight/.test(m)).length;
      setShipNow(24 * 1440 + 1100); __tick(); out.early = !!PU4_LIVE.mv; flagSet('pu4.ate', 25); __notes.length = 0; __tick(); out.mv = !!PU4_LIVE.mv; out.notice = __notes.slice();
      out.esc = (worksEscort({ id: 'vance' }, shipNow()) || {}).mode; out.open0 = worksHomeOpen(2, 'B');
      const keep = puNearMe; puNearMe = (id, r) => id === 'vance' ? true : keep(id, r); __said.length = 0; setShipNow(24 * 1440 + 1102); __tick(); puNearMe = keep;
      out.met = PU4_LIVE.mv && PU4_LIVE.mv.met; out.esc2 = (worksEscort({ id: 'vance' }, shipNow()) || {}).mode; out.arrow = GUIDE.list.filter(e => /^pu4:move/.test(e.id)).map(e => e.level + ' ' + (e.goal() || {}).label);
      goToDeck(2); player.obj.position.copy(cellPos(...PLACE_OF.get('2-B').at)); setShipNow(24 * 1440 + 1110); __tick();
      out.home = W.home; out.t4 = puT4(); out.bed = playerBed(); out.open = [worksHomeOpen(2, 'B'), worksHomeOpen(4, 'W')]; out.said = __said.filter(x => /^vance/.test(x)); out.next2 = worksNext();
      """ + T4_MOVE.replace('const W =', 'const W2 =').replace('W.', 'W2.').replace('const T = pu4Set', 'const T2 = pu4Set').replace(' T.', ' T2.') + """
      __bay(); setShipNow(24 * 1440 + 1201); __tick(); out.by20 = !!PU4_LIVE.mv; setShipNow(24 * 1440 + 1321); __tick(); out.gone22 = !PU4_LIVE.mv && !puT4().move.walked;
      const e26 = dayShiftEnd(26); setShipNow(25 * 1440 + e26 - 5); __tick(); out.before26 = !!PU4_LIVE.mv; setShipNow(25 * 1440 + e26 + 1); __tick(); out.next26 = !!PU4_LIVE.mv;
      CLOTHES_ON = true; W2.home = '2-B'; SHIP.clothes.clean = 2; SHIP.clothes.hamper = null; delete SHIP.clothes.coll; setShipNow(25 * 1440 + 601); __tick(); out.coll = SHIP.clothes.coll;
      setShipNow(26 * 1440 + 361); __tick(true); out.back = [SHIP.clothes.clean, SHIP.clothes.coll]; return out; })()""")
    for k, v in r.items(): print('   ', k, v)
    check(any('After dinner' in n for n in r['wake']) and r['rows'] and r['rows'][0].startswith('19:00') and 'Deck 2' in r['next'] and r['mail'] == 1, f"t4move: the notice as you wake, the Schedule's row, What's next, Calder's Mail at 17:00 ({r['wake']}, {r['rows']}, {r['next']}, {r['mail']})")
    check(not r['early'] and r['mv'] and any('Vance' in n for n in r['notice']) and r['esc'] == 'follow' and r['open0'], f"t4move: not before your dinner; then the urgent notice, Vance comes to you, the door opens for the walk ({r})")
    check(r['met'] and r['esc2'] == 'lead' and r['arrow'] and r['arrow'][0].startswith('1 Go with Vance'), f"t4move: met, he leads; a level 1 arrow 'Go with Vance' ({r['esc2']}, {r['arrow']})")
    check(r['home'] == '2-B' and r['t4']['move']['walked'] == 25 and r['bed'] == '2-B' and r['open'][0] is True and not r['open'][1] and any('regulation six' in x for x in r['said']) and 'Deck 2' not in (r['next2'] or ''), f"t4move: stepped in: room B is yours, your bed, your door, Vance's lines ({r['home']}, {r['bed']}, {r['open']}, {r['said']})")
    check(r['by20'] and r['gone22'] and not r['before26'] and r['next26'], f"t4move: no dinner, at 20:00 anyway; open till 22:00, then the next day at your shift's end ({r})")
    check(r['coll'] == 26 and r['back'] == [5, None], f"t4move: laundry collected at 10:00, back clean the next morning ({r['coll']}, {r['back']})")

# ---- S6-3 turn 4b (W7): Dev mode's Tier 4 rows, steps, career arrow and presets; forYou's engine line
def part_t4dev(g):
    if not t4on(g, 't4dev'): return
    print('(t4dev) Dev mode: the career table to Day 25, the promotion list, the career arrow, the presets; engine jobs by day:')
    r = g.ev("""(() => { const out = {}; const c = n => { const x = devmodeCareerFor(n); return [x.tier, x.rank, x.home, JSON.stringify(x.pu && x.pu.t4 || null), x.ms.map(m => m[0]).filter(k => /^specialist/.test(k)).join(',')]; };
      out.c21 = c(21); out.c22 = c(22); out.c23 = c(23); out.c25 = c(25); out.later = DM_CAREER.filter(r => r.later).map(r => r.later);
      out.beats = DM_BEATS.map(b => b.id + ' ' + b.day + ' ' + hhmm(b.at));
      """ + T4_RES + """ out.steps = devmodePromoSteps().filter(x => /Tier 4|engine|Deck 2/.test(x.label)).map(x => x.label + ' ' + hhmm(x.at % 1440) + (x.done ? ' done' : ''));
      setShipNow(21 * 1440 + 900); out.next1 = (puDevNext() || { g: {} }).g.label; pu4Promote(21 * 1440 + 1361, 'met'); out.next2 = (puDevNext() || { g: {} }).g.label; pu4Badge(22 * 1440 + 1000, 'met'); out.next3 = (puDevNext() || { g: {} }).g.label;
      out.steps2 = devmodePromoSteps().filter(x => /Tier 4|engine|Deck 2/.test(x.label)).map(x => x.label + (x.done ? ' done' : ''));
      setShipNow(23 * 1440 + 600); out.eng24 = pu4EngineByDay(); setShipNow(24 * 1440 + 600); out.eng25 = pu4EngineByDay() && /pu4EngineByDay/.test(String(forYou)); return out; })()""")
    for k, v in r.items(): print('   ', k, v)
    check(r['c21'][0] == 3 and r['c22'][:2] == [4, 'specialist'] and '"badge":null' in r['c22'][3] and '"badge":23' in r['c23'][3] and r['c25'][2] == '2-B' and '"walked":25' in r['c25'][3] and r['c23'][4] == 'specialist,specialist.badge' and not any('Engine Specialist' in l for l in r['later']), f"t4dev: the career table: Tier 4 from Day 22, the badge Day 23, Deck 2 from Day 25 ({r['c21']}, {r['c22']}, {r['c23']}, {r['c25']}, {r['later']})")
    check([b.split()[0] for b in r['beats'] if b.startswith('t4')] == ['t4', 't4res', 't4badge', 't4move'], f"t4dev: the presets for Days 22, 22, 23, 25 ({r['beats']})")
    check(r['steps'] == ['Your Tier 4 test 09:30 done', 'Your Tier 4 result 22:40'] and 'result' in r['next1'] and 'badge' in r['next2'] and 'Vance' in r['next3'] and r['steps2'][-1] == 'Your Deck 2 quarters', f"t4dev: the promotion list and the career arrow ({r['steps']}, {r['next1']}, {r['next2']}, {r['next3']}, {r['steps2']})")
    check(r['eng24'] is False and r['eng25'] is True, f"t4dev: engine jobs yours by day after the nights, not before ({r})")

# (W8, lead 42's t3 question) the same as t4carry for Step 5's Tier 3 test (Day 15): a lesson of Tier 2 (Tracing, m9)
# asked and missed before (W.cur 'm9:ask' from Day 13), or never asked; on Day 15 the test opens. In the game as shipped
# (Step 6 off) the lesson holds it: this part reports "held (the game as shipped)" there and checks only with the Step 6
# switch on, where 24 core's MA6-2 fix (ladderTestDue, a due test row ahead of a lesson of its tier) covers every test row
def part_t3carry(g):
    if not g.ev("typeof puSet === 'function' && typeof ladderRow === 'function' && !!ladderRow('t3') && !!ladderRow('m9')"): print('(t3carry) no Tier 3 test or Tracing in this build: skipped'); return
    print('(t3carry) a lesson missed before the Tier 3 test on Day 15:')
    base = T3_TEST.replace("r.id !== 't3' && r.tier <= 2", "r.id !== 't3' && r.id !== 'm9' && r.tier <= 2")
    r = g.ev("""(() => { """ + base.replace("puSet(15);", "puSet(15); W.cur = { id: 'm9', st: 'ask', d: 13, by: 'calder', occ: null, j: null, w: 0 }; (W.op[13] = W.op[13] || []).push('m9');") + """
      const out = { on: typeof P5_PROMO4 !== 'undefined' && !!P5_PROMO4 }; for (let h = 6; h <= 10; h++) { setShipNow(14 * 1440 + h * 60); careerClock(shipNow(), true); __tick(); }
      out.cur = W.cur && W.cur.id + ' ' + W.cur.st; out.op15 = W.op[15] || []; return out; })()""")
    r2 = g.ev("""(() => { """ + base + """ return { cur: W.cur && W.cur.id + ' ' + W.cur.st, op15: W.op[15] || [] }; })()""")
    print('    carried:', r, '| never asked:', r2)
    held, held2 = not (r['cur'] or '').startswith('t3'), not (r2['cur'] or '').startswith('t3')
    if not r['on']: print(f"    the game as shipped (Step 6 off): carried {'held' if held else 'not held'}, never asked {'held' if held2 else 'not held'}"); return
    check(not held and 't3' in r['op15'], f"t3carry: with Step 6, Day 15 opens the Tier 3 test, not the carried lesson ({r})")
    check(not held2 and 'm9' not in r2['op15'], f"t3carry: with Step 6, an untaken lesson of Tier 2 never goes ahead of the Tier 3 test ({r2})")

# (W8, PZ6's arrows find) the test day's evening: level 1 arrows from the 16:45 wake to dinner, then the comet in the
# observation room, till Calder's 22:40 (read through goalNow: what the screen shows)
def part_t4eve(g):
    if not t4on(g, 't4eve'): return
    print('(t4eve) the evening of the Tier 4 test: dinner, then the comet, till Calder comes:')
    r = g.ev("""(() => { """ + T4_RES + """ const out = {}, at = m => { setShipNow(21 * 1440 + m); GUIDE.list.length = 0; __tick(); const x = goalNow(); return x ? (x.deck || '') + ' ' + (x.label || '') : null; };
      out.e1000 = at(1000); out.e1010 = at(1010); out.e1150 = at(1150); out.e1300 = at(1300); out.e1365 = at(1365);
      goToDeck(3); player.obj.position.copy(cellPos(...ROOM_TILES['M'][0])); out.inMess = at(1020); T.res = 22; out.told = at(1300); PU4_LIVE.rseek = null; PU4_LIVE.walk = null; GUIDE.list.length = 0; return out; })()""")
    for k, v in r.items(): print('   ', k, v)
    ok1 = r['e1010'] and r['e1010'].startswith('3 Dinner') and r['e1150'] and r['e1150'].startswith('1 The comet, 21:30') and 'Calder finds you at 22:40' in r['e1150'] and r['e1300'] and r['e1300'].startswith('1 The comet: the observation room')
    check(ok1, f"t4eve: from 16:45 a level 1 arrow to dinner, then the comet in the observation room, Calder at 22:40 ({r['e1010']}, {r['e1150']}, {r['e1300']})")
    check(not (r['e1000'] or '').startswith('3 Dinner') and not (r['e1365'] or '').startswith('1 The comet') and not (r['inMess'] or '').startswith('3 Dinner') and not (r['told'] or '').startswith('1 The comet'), f"t4eve: none before 16:45 or after 22:40, in the mess, or once told ({r['e1000']}, {r['e1365']}, {r['inMess']}, {r['told']})")

# (W8, S6-3's refit; DA6's 2-B asks) the refit odd job: posted once a board window from Day 23 till you move in, held for
# you, never in the odd jobs' stream; done by you: T.move.refit, one more touch to pick, your cabin touches in room B
# after the move (24t's cabinHome), room B named yours on the HUD; not done: no touches up there; the crew's done one: no more
def part_refit(g):
    if not t4on(g, 'refit'): return
    if not g.ev("typeof P5_DECK6 !== 'undefined' && P5_DECK6 && typeof pu4RefitTick === 'function'"): print('(refit) not in this build: skipped'); return
    print('(refit) the refit odd job, your touches up to room B:')
    r = g.ev("""(() => { """ + T4_MOVE + """ const out = {}; SHIP.jobs = SHIP.jobs.filter(j => !pu4RefitJob(j)); W.side.cabin = { rug: 'woven rug', ledge: 'little plant' };
      const refits = () => SHIP.jobs.filter(pu4RefitJob); setShipNow(21 * 1440 + 500); pu4RefitTick(shipNow(), false); out.before23 = refits().length;
      setShipNow(25 * 1440 + 550); __notes.length = 0; pu4RefitTick(shipNow(), false); pu4RefitTick(shipNow() + 30, false); const j = refits()[0];
      out.n = refits().length; out.title = j && j.title; out.board = j && boardForYou(j, shipNow()); out.notes = __notes.filter(n => /refit/i.test(n)).length; out.stream = fixTable().o.some(r => r.id === 'oj-d2suite-refit'); out.row = !!fixRow('oj-d2suite-refit');
      out.home0 = !!cabinHome(); const keepC = deviceChoose; window.__ch = null; deviceChoose = (o, cb) => { window.__ch = o.choices; cb(1); return true; };
      claimJob(j.id); jobStops(j).forEach((x, k) => jobStepDone(j.id, k)); out.turnin = turnInJob(j.id); for (let i = 0; i < 5; i++) { setShipNow(shipNow() + 1); __tick(); if (typeof simFlush === 'function') simFlush(); }
      if (!puT4().move.refit) pu4Refitted(shipNow()); deviceChoose = keepC; out.refit = puT4().move.refit; out.choices = window.__ch; out.cabin = JSON.stringify(cabinData());
      out.homeB4 = !!cabinHome(); pu4Moved(shipNow(), 'check'); const H = cabinHome(); out.home = H && H.deck + ' ' + H.home; out.name = DECKS[2].rooms.B.name;
      pu4RefitTick(shipNow() + 1440, false); out.after = refits().filter(x => x.status === 'open').length;
      """ + T4_MOVE.replace('const W =', 'const W2 =').replace(' W.', ' W2.').replace('const T =', 'const T2 =').replace(' T.', ' T2.') + """ SHIP.jobs = SHIP.jobs.filter(j => !pu4RefitJob(j)); setShipNow(25 * 1440 + 550); pu4RefitTick(shipNow(), false); pu4Moved(shipNow() + 600, 'check'); out.noRefit = [!!cabinHome(), DECKS[2].rooms.B.name];
      pu4RefitTick(shipNow() + 1440, false); out.dropped = SHIP.jobs.filter(j => pu4RefitJob(j) && j.status === 'open').length;
      """ + T4_MOVE.replace('const W =', 'const W3 =').replace(' W.', ' W3.').replace('const T =', 'const T3 =').replace(' T.', ' T3.') + """ SHIP.jobs = SHIP.jobs.filter(j => !pu4RefitJob(j)); setShipNow(25 * 1440 + 550); pu4RefitTick(shipNow(), false); SHIP.jobs.filter(pu4RefitJob).forEach(x => { x.status = 'done'; x.doneBy = 'kovac-zainab'; });
      pu4RefitTick(shipNow() + 1440, false); out.crew = [SHIP.jobs.filter(j => pu4RefitJob(j) && j.status === 'open').length, puT4().move.refit]; return out; })()""")
    for k, v in r.items(): print('   ', k, v)
    check(r['before23'] == 0 and r['n'] == 1 and r['title'] == "Refit the visitors' suite" and r['board'] and r['notes'] == 1 and not r['stream'] and r['row'], f"refit: from Day 23, one a window, held for you, its row by id only ({r['before23']}, {r['n']}, {r['title']}, {r['board']}, notes {r['notes']}, stream {r['stream']})")
    check(not r['home0'] and r['turnin'] and r['refit'] and r['choices'] and len(r['choices']) == 2 and '"shelf":"model ship"' in r['cabin'], f"refit: done by you, the refit kept, one more touch to pick among the empty spots ({r['turnin']}, {r['refit']}, {r['choices']}, {r['cabin']})")
    check(r['home'] == '2 2-B' and r['name'] == 'Your quarters' and r['after'] == 0, f"refit: moved in, your touches in room B, named yours, no more refit jobs ({r['home']}, {r['name']}, {r['after']})")
    check(r['noRefit'] == [False, 'Your quarters'] and r['dropped'] == 0, f"refit: not taken: no touches up there, the job gone once you've moved ({r['noRefit']}, {r['dropped']})")
    check(r['crew'] == [0, False], f"refit: the crew's done it: no more posted, not yours ({r['crew']})")

# (W8, MA6-2) a Tier 3 lesson asked on Friday Day 19 and missed (W.cur 'm20:ask') never holds Day 22's Tier 4 test: on
# Day 22 the test opens; the lesson goes back to unopened and is asked again on a later day
def part_t4carry(g):
    if not t4on(g, 't4carry'): return
    print('(t4carry) a lesson missed on Day 19 and the Tier 4 test on Day 22:')
    r = g.ev("""(() => { """ + T4_TEST.replace("r.id !== 't4' && r.tier <= 3", "r.id !== 't4' && r.id !== 'm20' && r.tier <= 3").replace("pu4Set(22);", "pu4Set(22); W.cur = { id: 'm20', st: 'ask', d: 19, by: 'calder', occ: null, j: null, w: 0 }; (W.op[19] = W.op[19] || []).push('m20');") + """
      const out = {}; out.m20 = !!WORK_MECH.m20; for (let h = 6; h <= 10; h++) { setShipNow(21 * 1440 + h * 60); careerClock(shipNow(), true); __tick(); }
      out.cur = W.cur && W.cur.id + ' ' + W.cur.st; out.job = SHIP.jobs.some(j => j.reserved === 26); out.op19 = (W.op[19] || []).includes('m20'); out.op22 = W.op[22] || [];
      out.again = []; for (let d = 23; d <= 30 && !out.again.length; d++) for (let h = 6; h <= 10; h++) { setShipNow((d - 1) * 1440 + h * 60); if (W.cur && W.cur.id === 't4') { W.tr.t4 = 22; W.cur = null; } ladderTick((d - 1) * 24 + h); if (W.cur && W.cur.id === 'm20') { out.again = [d, W.cur.st]; break; } }
      return out; })()""")
    for k, v in r.items(): print('   ', k, v)
    r2 = g.ev("""(() => { """ + T4_TEST.replace("r.id !== 't4' && r.tier <= 3", "r.id !== 't4' && r.id !== 'm20' && r.tier <= 3") + """ return { cur: W.cur && W.cur.id + ' ' + W.cur.st, op22: W.op[22] || [] }; })()""")
    print('    never asked:', r2)
    check(r2['cur'] and r2['cur'].startswith('t4') and 'm20' not in r2['op22'], f"t4carry: an untaken lesson of Tier 3 never goes ahead of the Tier 4 test on Day 22 ({r2})")
    if not r['m20']: print('    (no M20 in this build: the carried lesson is a stand-in name only)')
    check(r['cur'] and r['cur'].startswith('t4') and r['job'] and 't4' in r['op22'] and not r['op19'], f"t4carry: Day 22 opens the Tier 4 test, not the carried lesson ({r['cur']}, job {r['job']}, op22 {r['op22']}, op19 {r['op19']})")
    if r['m20']: check(r['again'] and r['again'][0] > 22, f"t4carry: the lesson is asked again on a later day ({r['again']})")

# ---- S6-7 turn 1 (W7): Basil's day with you, settled at 22:00 the evening before; his work in the Works bay; the notices
def part_mt(g):
    if not g.ev("typeof P5_M25 !== 'undefined' && P5_M25"): print('(mt) P5_M25 off: skipped'); return
    print('(mt) mentoring: settled at 22:00 on Thursday, Basil\'s work in the bay 09:00-15:30, the notice, the row, the arrow:')
    r = g.ev("""(() => { const W = __w(25, 1300, { xp: 10, tr: { ps: 12, t2: 9, t3: 15, m19: 17, t4: 22 } }); W.tier = 4; W.rank = 'specialist'; flagSet('p5n.on', 22); flagSet('p5n.off', 25);
      const out = {}, bas = schedPeople().find(p => p.id === 'bramwell-basil'), seg = () => planDay(bas, 26).filter(x => x.to > 25 * 1440 + 540 && x.from < 25 * 1440 + 930 && /^work/.test(x.type || '')).map(x => x.deck + '|' + (placeById(x.placeId) || {}).room);
      out.before = [...new Set(seg())]; __tick(); out.early = !!SHIP.works.mt;
      setShipNow(24 * 1440 + 1321); __tick(); out.mt = SHIP.works.mt; out.mail = __mail().filter(m => /^Chief Ines Calder: Tomorrow/.test(m)).length; out.next = worksNext();
      out.after = [...new Set(seg())]; out.rows = __rows(26).filter(x => /Basil/.test(x));
      out.clean = JSON.stringify(mtClean(JSON.parse(JSON.stringify(SHIP.works.mt)))) === JSON.stringify(SHIP.works.mt); out.junk = mtClean({ day: 'x' });
      __notes.length = 0; setShipNow(25 * 1440 + 400); __tick(); out.wake = __notes.slice(); setShipNow(25 * 1440 + 536); goToDeck(3); __tick(); out.arrow = GUIDE.list.filter(e => /^mt:bay/.test(e.id)).map(e => e.level + ' ' + (e.goal() || {}).label);
      const W2 = __w(25, 1300, { xp: 10 }); W2.tier = 2; W2.rank = 'officer'; setShipNow(24 * 1440 + 1321); __tick(); out.officer = !!SHIP.works.mt; return out; })()""")
    for k, v in r.items(): print('   ', k, v)
    check(not r['early'] and r['mt'] and r['mt']['day'] == 26 and r['mt']['set'] == 25 and r['mail'] == 1 and 'Basil' in r['next'], f"mt: settled at 22:00 on Thursday for Friday Day 26, Calder's Mail, What's next ({r['mt']}, {r['mail']}, {r['next']})")
    check(r['after'] and all(x == '5|w' for x in r['after']), f"mt: Basil's work 09:00-15:30 in the Works bay once settled ({r['before']} -> {r['after']})")
    check(r['rows'] and r['rows'][0].startswith('09:00') and any('Basil' in n for n in r['wake']) and r['arrow'] and r['arrow'][0].startswith('1 '), f"mt: the row, the notice as you wake, a level 1 arrow from 08:55 ({r['rows']}, {r['wake']}, {r['arrow']})")
    check(r['clean'] and r['junk'] is None and not r['officer'], f"mt: the save's record read back, junk dropped; not a Senior: no day ({r})")

MT_DAY = """const W = __w(25, 1300, { xp: 10, tr: { ps: 12, t2: 9, t3: 15, m19: 17, t4: 22 } }); W.tier = 4; W.rank = 'specialist'; flagSet('p5n.on', 22); flagSet('p5n.off', 25); setShipNow(24 * 1440 + 1321); __tick();"""
def part_mt2(g):
    if not g.ev("typeof P5_M25 !== 'undefined' && P5_M25"): print('(mt2) P5_M25 off: skipped'); return
    print('(mt2) Basil\'s hello, he watches you (follows) through a job, you watch him at the bench:')
    r = g.ev("""(() => { """ + MT_DAY + """ const out = {}; setShipNow(25 * 1440 + 541); __bay();
      const keep = puNearMe; puNearMe = (id, r) => id === 'bramwell-basil' ? true : keep(id, r); __tick(); out.dlg1 = DIALOGUE && DIALOGUE.id; """ + dlg_run(0) + """
      const M = SHIP.works.mt; out.met = M.steps.met !== undefined; out.esc1 = (worksEscort({ id: 'bramwell-basil' }, shipNow()) || {}).mode;
      __tick(); out.arrow1 = GUIDE.list.filter(e => /^mt:watch/.test(e.id)).map(e => e.level + ' ' + (e.goal() || {}).label);
      simNote('job', { id: 'x', step: 'turnin' }); out.watch = M.steps.watch !== undefined; out.esc2 = JSON.stringify(worksEscort({ id: 'bramwell-basil' }, shipNow()));
      for (let i = 0; i < 11; i++) { setShipNow(25 * 1440 + 600 + i); __tick(); } out.dw = M.steps.dw; out.dlg2 = DIALOGUE && DIALOGUE.id; { """ + dlg_run(1) + """ } out.do = M.steps.do !== undefined; out.reply = flag('mt.do');
      out.arrow2 = GUIDE.list.filter(e => /^mt:do/.test(e.id)).map(e => e.level + ' ' + (e.goal() || {}).label); puNearMe = keep;
      """ + MT_DAY.replace('const W =', 'const W2 =').replace('W.', 'W2.') + """ SHIP.works.mt.steps.met = 25 * 1440 + 545; __said.length = 0; setShipNow(25 * 1440 + 781); __bay(); __tick(); out.late = [SHIP.works.mt.steps.watch !== undefined, __said.filter(x => /^calder/.test(x)).length]; return out; })()""")
    for k, v in r.items(): print('   ', k, v)
    check(r['dlg1'] == 'mt.hello' and r['met'] and r['esc1'] == 'follow' and r['arrow1'] and r['arrow1'][0].startswith('1 '), f"mt2: the hello in the bay, then he follows you; a level 1 arrow to take a job ({r['dlg1']}, {r['esc1']}, {r['arrow1']})")
    check(r['watch'] and '"wait"' in r['esc2'] and '5-bench-2' in r['esc2'] and r['dw'] >= 10 and r['dlg2'] == 'mt.do' and r['do'] and r['reply'] == 2, f"mt2: a job turned in, he goes to the bench; ten minutes watching him, his scene, your reply ({r})")
    check(r['late'] == [True, 1], f"mt2: no job by 13:00, Calder sends him to the bench ({r['late']})")

def part_mt3(g):
    if not g.ev("typeof P5_M25 !== 'undefined' && P5_M25"): print('(mt3) P5_M25 off: skipped'); return
    print('(mt3) the stuck clue (you point him to one), the late talk (three replies); not helped: he works it out:')
    r = g.ev("""(() => { """ + MT_DAY + """ const out = {}, M = SHIP.works.mt; Object.assign(M.steps, { met: 36540, watch: 36560, dw: 10, do: 36600 }); setShipNow(25 * 1440 + 650); __bay();
      const keep = puNearMe; puNearMe = (id, r) => id === 'bramwell-basil' ? true : keep(id, r); __said.length = 0; __tick();
      out.stuck = __said.filter(x => /^bramwell/.test(x)); out.arrow = GUIDE.list.filter(e => /^mt:clue/.test(e.id)).map(e => e.level + ' ' + (e.goal() || {}).label); out.esc1 = JSON.stringify(worksEscort({ id: 'bramwell-basil' }, shipNow()));
      out.point = typeof CASE_UI !== 'undefined' && CASE_UI.point ? CASE_UI.point.key : null; out.dlg1 = DIALOGUE && DIALOGUE.id;
      if (out.point) { out.pick = CASE_UI.point.pick.slice(); casePointPick(out.point); out.pointed = __said.filter(x => /^bramwell/.test(x)).length > out.stuck.length; } else { """ + dlg_run(0) + """ } out.clue = M.clue; out.key = M.clueKey;
      setShipNow(25 * 1440 + 780); out.lunch = worksEscort({ id: 'bramwell-basil' }, shipNow()); setShipNow(25 * 1440 + 816); out.esc2 = (worksEscort({ id: 'bramwell-basil' }, shipNow()) || {}).mode; __tick();
      out.dlg2 = DIALOGUE && DIALOGUE.id; { """ + dlg_run(2) + """ } out.late = [M.late, M.steps.late !== undefined]; out.esc3 = (worksEscort({ id: 'bramwell-basil' }, shipNow()) || {}).mode; puNearMe = keep;
      out.clean = JSON.stringify(mtClean(JSON.parse(JSON.stringify(M)))) === JSON.stringify(M);
      """ + MT_DAY.replace('const W =', 'const W2 =').replace('W.', 'W2.') + """ Object.assign(SHIP.works.mt.steps, { met: 1, watch: 2, dw: 10, do: 3 }); setShipNow(25 * 1440 + 746); __tick(); out.self = SHIP.works.mt.clue; return out; })()""")
    for k, v in r.items(): print('   ', k, v)
    pz = g.ev("typeof casePoint === 'function'")   # PZ6's case panel in point mode: then the clue is one of its three, the key kept (mt.clueKey); without it the stand-in scene
    hit = (r['point'] and r['clue'] == r['point'] and r['key'] is True and len(r['pick']) == 3 and r['pointed']) if pz else (r['dlg1'] == 'mt.clue' and r['clue'] == 'meter')
    check(r['stuck'] and r['arrow'] and r['arrow'][0].startswith('1 ') and '5-bench-2' in r['esc1'] and hit, f"mt3: stuck at the bench, a level 1 arrow, you point him to a clue ({'casePoint' if pz else 'stand-in'}: {r['stuck']}, {r['arrow']}, {r['dlg1']}, {r.get('point')}, {r['clue']})")
    if pz:   # casePoint with no fair case: the stand-in scene instead
        r2 = g.ev("""(() => { """ + MT_DAY + """ const out = {}, M = SHIP.works.mt; Object.assign(M.steps, { met: 36540, watch: 36560, dw: 10, do: 36600 }); setShipNow(25 * 1440 + 650); __bay(); MT_LIVE.case = 0;
          const keep = puNearMe, cp = casePoint; puNearMe = (id, r) => id === 'bramwell-basil' ? true : keep(id, r); casePoint = () => false; __tick(); out.dlg = DIALOGUE && DIALOGUE.id; { """ + dlg_run(1) + """ } out.clue = M.clue; casePoint = cp; puNearMe = keep; return out; })()""")
        check(r2['dlg'] == 'mt.clue' and r2['clue'] == 'label', f"mt3: casePoint with no fair case, the stand-in scene ({r2})")
    check(r['lunch'] is None and r['esc2'] == 'follow' and r['dlg2'] == 'mt.late' and r['late'] == [2, True] and r['esc3'] == 'wait' and r['clean'], f"mt3: lunch as planned; late, he hurries to you; three replies, yours kept; back to the bench ({r})")
    check(r['self'] == 'self', f"mt3: not helped by 12:25, he works it out himself ({r['self']})")

def part_mt4(g):
    if not g.ev("typeof P5_M25 !== 'undefined' && P5_M25"): print('(mt4) P5_M25 off: skipped'); return
    print('(mt4) Calder gives Basil his first job alone; the Record line; missed: her Mail; the Dev preset:')
    r = g.ev("""(() => { """ + MT_DAY + """ const out = {}, M = SHIP.works.mt; Object.assign(M.steps, { met: 1, watch: 2, dw: 10, do: 3, clue: 4, late: 5 }); M.clue = 'meter'; M.late = 0;
      setShipNow(25 * 1440 + 896); __bay(); __tick(); out.arrow = GUIDE.list.filter(e => /^mt:first/.test(e.id)).map(e => e.level + ' ' + (e.goal() || {}).label); out.esc = (worksEscort({ id: 'bramwell-basil' }, shipNow()) || {}).mode;
      const keep = puNearMe; puNearMe = (id, r) => id === 'bramwell-basil' || id === 'calder' ? true : keep(id, r); setShipNow(25 * 1440 + 901); __tick(); puNearMe = keep;
      out.dlg = DIALOGUE && DIALOGUE.id; { """ + dlg_run(1) + """ } out.done = M.steps.done !== undefined; out.tr = SHIP.works.tr.m25; out.rec = worksRecordHead().text; out.next = worksNext();
      """ + MT_DAY.replace('const W =', 'const W2 =').replace('W.', 'W2.') + """ setShipNow(25 * 1440 + 925); __tick(); out.mail = [SHIP.works.mt.steps.done !== undefined, __mail().filter(m => /^Chief Ines Calder: Basil/.test(m)).length];
      out.preset = DM_BEATS.filter(b => b.id === 'mt').map(b => b.day + ' ' + hhmm(b.at)); return out; })()""")
    for k, v in r.items(): print('   ', k, v)
    check(r['arrow'] and r['arrow'][0].startswith('1 ') and r['esc'] == 'wait' and r['dlg'] == 'mt.first' and r['done'] and r['tr'] == 26 and 'Mentored Basil, Day 26' in r['rec'] and 'Basil' not in r['next'], f"mt4: Calder's scene at the bench, the row trained, the Record's line ({r})")
    check(r['mail'] == [True, 1] and r['preset'] == ['26 08:50'], f"mt4: not there by 15:20, by Mail; the Dev preset Day 26 08:50 ({r['mail']}, {r['preset']})")

CQ_DAY = """const W = __w(25, 1300, { xp: 10, tr: { ps: 12, t2: 9, t3: 15, m19: 17, t4: 22, m25: 26 } }); W.tier = 4; W.rank = 'specialist'; W.ns = { 22: { in: 1, out: 2, jobs: 0, inc: 0, late: 0 }, 23: { in: 1, out: 2, jobs: 0, inc: 0, late: 0 }, 24: { in: 1, out: 2, jobs: 0, inc: 0, late: 0 } };
  W.ms.push(['specialist', 22], ['specialist.badge', 23], ['mentor', 26]); if (DIALOGUE) dialogueEnd(false); DIALOGUE = null; MT_LIVE.said = {}; setShipNow(24 * 1440 + 1321); out.settle = cqSettle(26); CQ_LIVE.seat = null; CQ_LIVE.sitAt = 0; CQ_LIVE.said = {};
  const __tea = () => { if (deckDef.num !== 5) goToDeck(5); player.obj.position.copy(cellPos(...ROOM_TILES['t'][0])); };"""
def part_cq(g):
    if not g.ev("typeof P5_END !== 'undefined' && P5_END"): print('(cq) P5_END off: skipped'); return
    print('(cq) Calder\'s question at Four weeks aboard: the Mail the evening before, the notice, the arrow, the cake and her story, she sits, the question, your answer, the Record:')
    for pick in range(4):
        r = g.ev("""(() => { const out = {}; """ + CQ_DAY + """ const E = SHIP.works.end; out.end0 = JSON.stringify(E); out.mail0 = __mail().filter(m => /^Chief Ines Calder: Four weeks, tomorrow/.test(m)).length;
          const tabs = () => (WORKS_TABS || []).filter(x => !x.show || x.show()).map(x => x.id); out.tab0 = tabs().includes('career'); out.rows = __rows(26); setShipNow(25 * 1440 + 600); out.next = worksNext();
          setShipNow(25 * 1440 + 1101); __bay(); __tick(); out.notes = __notes.filter(n => /Four weeks/.test(n));
          setShipNow(25 * 1440 + 1116); __tick(); out.arrow = GUIDE.list.filter(e => /^end:tea/.test(e.id)).map(e => e.level + ' ' + (e.goal() || {}).label);
          __tea(); const keep = puNearMe; puNearMe = (id, r) => id === 'calder' ? true : keep(id, r); setShipNow(25 * 1440 + 1121); __tick(); out.d40 = DIALOGUE && DIALOGUE.id; setShipNow(25 * 1440 + 1126); __tick(); out.dlg1 = DIALOGUE && DIALOGUE.id; { """ + dlg_run(1) + """ } out.story = E.steps.story !== undefined;
          setShipNow(25 * 1440 + 1130); __tick(); out.early = DIALOGUE && DIALOGUE.id;
          PLAYER_PLACE = null; setShipNow(25 * 1440 + 1146); __said.length = 0; __tick(); out.seat = CQ_LIVE.seat; out.sitSaid = __said.filter(x => /^calder/.test(x)).length; out.come = COME_TO.has('calder') && COME_TO.get('calder').placeId;
          out.arrow2 = GUIDE.list.filter(e => /^end:sit/.test(e.id)).map(e => e.level + ' ' + (e.goal() || {}).label + ' ' + (e.goal() || {}).place); out.dlg2 = DIALOGUE && DIALOGUE.id;
          PLAYER_PLACE = '5-tea-1'; setShipNow(25 * 1440 + 1147); __tick(); out.dlg3 = DIALOGUE && DIALOGUE.id; { """ + dlg_run(pick) + """ } puNearMe = keep; PLAYER_PLACE = null;
          out.answer = E.answer; out.asked = E.steps.asked !== undefined; out.ms = SHIP.works.ms.filter(x => /nights|question/.test(x[0])).map(x => x.join(' '));
          out.tab1 = tabs().includes('career'); out.page = cqPage().map(b => b.text || (b.rows || []).map(r => r.text + ' (' + r.sub + ')').join('; ')).join(' / '); out.toast = __toasts.filter(t => /Your career/.test(t[0])).length;
          out.mail = __mail().filter(m => /What you said/.test(m)).length; out.rec = worksRecordHead().text; out.clean = JSON.stringify(cqClean(JSON.parse(JSON.stringify(E)))) === JSON.stringify(E);
          setShipNow(25 * 1440 + 1200); __tick(); out.after = (worksEscort({ id: 'calder' }, shipNow()) || {}).mode || null; out.nextAfter = worksNext(); return out; })()""")
        if pick == 0:
            for k, v in r.items(): print('   ', k, v)
        else: print(f"    answer {pick}: {r['answer']}; Record: ...{r['rec'][-90:]}")
        if pick == 0:
            check(r['settle'] and '"day":26' in r['end0'] and r['mail0'] == 1 and any('Calder' in x and '18:40' in x for x in r['rows']) and 'Friday tea' in r['next'], f"cq: settled at 22:00 the evening before, Calder's Mail, the Schedule's row, What's next ({r['settle']}, {r['mail0']}, {r['rows']}, {r['next']})")
            check(r['notes'] and r['arrow'] and r['arrow'][0].startswith('1 ') and 'tea corner' in r['arrow'][0], f"cq: the notice at 18:20, a level 1 arrow to the tea corner from 18:35 ({r['notes']}, {r['arrow']})")
            check(not r['d40'] and r['dlg1'] == 'end.story' and r['story'] and not r['early'], f"cq: there from 18:40; the cake and her story from 18:45 (the guests have come); nothing more until it thins out ({r['d40']}, {r['dlg1']}, {r['story']}, {r['early']})")
            check(r['seat'] == '5-tea-2' and r['come'] == '5-tea-2' and r['sitSaid'] and r['arrow2'] and r['arrow2'][0].startswith('1 ') and '5-tea-1' in r['arrow2'][0] and not r['dlg2'], f"cq: at 19:05 she sits, says so, the arrow shows you the seat beside her ({r['seat']}, {r['come']}, {r['arrow2']}, {r['dlg2']})")
            check(r['dlg3'] == 'end.ask' and r['asked'] and r['ms'] == ['nights 24', 'question 26'] and r['mail'] == 1 and 'Night shift on the engines, to Day 24' in r['rec'] and r['clean'], f"cq: sat, her question; your answer kept, the milestones, the Mail as the record, the Record's lines ({r['dlg3']}, {r['ms']}, {r['mail']}, {r['rec']})")
            check(not r['tab0'] and r['tab1'] and r['toast'] == 1 and 'Calder\'s question (Day 26)' in r['page'] and 'The last of your night shifts (Day 24)' in r['page'] and 'You told Calder' in r['page'], f"cq: the Works app's last page, Your career, once you've answered ({r['tab0']}, {r['tab1']}, {r['page']})")
            check(r['after'] is None and 'Friday tea' not in r['nextAfter'], f"cq: asked: she doesn't come looking, What's next moves on ({r['after']}, {r['nextAfter']})")
        check(r['answer'] == ['engines', 'bridge', 'teach', 'unsure'][pick] and 'asked what you want next' in r['rec'], f"cq: answer {pick} kept and on the Record ({r['answer']}, {r['rec'][-100:]})")

def part_cq2(g):
    if not g.ev("typeof P5_END !== 'undefined' && P5_END"): print('(cq2) P5_END off: skipped'); return
    print('(cq2) not sat by her for three minutes: she asks anyway; missed at the tea: she comes to find you, that evening and the next day; not yet an Engine Specialist: nothing:')
    r = g.ev("""(() => { const out = {}; """ + CQ_DAY + """ const E = SHIP.works.end; __tea(); const keep = puNearMe; puNearMe = (id, r) => id === 'calder' ? true : keep(id, r);
      E.steps.story = 25 * 1440 + 1125; PLAYER_PLACE = null; setShipNow(25 * 1440 + 1146); __tick(); out.d0 = DIALOGUE && DIALOGUE.id; setShipNow(25 * 1440 + 1149); __tick(); out.d1 = DIALOGUE && DIALOGUE.id; { """ + dlg_run(3) + """ } out.a = E.answer;
      SHIP.works.end = { day: 26, set: 25, steps: {}, answer: null }; const E2 = SHIP.works.end; GUIDE.list.length = 0; SHIP.flags = {}; puNearMe = keep; __bay();
      setShipNow(25 * 1440 + 1175); out.esc1 = (worksEscort({ id: 'calder' }, shipNow()) || {}).mode || null; __notes.length = 0; __tick(); out.find = __notes.filter(n => /Calder/.test(n)); out.arrow = GUIDE.list.filter(e => /^end:find/.test(e.id)).map(e => e.level + ' ' + (e.goal() || {}).crew + ' ' + (e.goal() || {}).deck); out.screen = (goalNow() || {}).label || null;
      out.other = DIALOGUE && DIALOGUE.id; if (DIALOGUE) dialogueEnd(false); DIALOGUE = null; setShipNow(25 * 1440 + 1330); out.esc2 = (worksEscort({ id: 'calder' }, shipNow()) || {}).mode || null; setShipNow(26 * 1440 + 610); out.esc3 = (worksEscort({ id: 'calder' }, shipNow()) || {}).mode || null;
      puNearMe = (id, r) => id === 'calder' ? true : keep(id, r); __tick(); out.d2 = DIALOGUE && DIALOGUE.id; { """ + dlg_run(2) + """ } puNearMe = keep; out.a2 = E2.answer; out.dayA = (E2.steps.asked - (E2.steps.asked % 1440)) / 1440 + 1;
      const W3 = __w(25, 1300, {}); W3.tier = 3; W3.rank = 'senior'; out.senior = cqSettle(26); out.none = !SHIP.works.end; out.preset = DM_BEATS.filter(b => b.id === 'cq').map(b => b.day + ' ' + hhmm(b.at)); return out; })()""")
    for k, v in r.items(): print('   ', k, v)
    check(r['d0'] is None and r['d1'] == 'end.ask' and r['a'] == 'unsure', f"cq2: not on the seat, after three minutes by her she asks anyway ({r['d0']}, {r['d1']}, {r['a']})")
    check(r['esc1'] == 'follow' and r['find'] and r['arrow'] and r['arrow'][0].startswith('1 calder ') and r['arrow'][0].split()[-1].isdigit() and r['screen'] == 'Calder wants a word' and r['esc2'] is None and r['esc3'] == 'follow' and r['d2'] == 'end.ask' and r['a2'] == 'teach' and r['dayA'] == 27, f"cq2: missed, she comes to find you till 22:00 and the next day; asked then ({r})")
    check(r['senior'] is False and r['none'], f"cq2: not yet an Engine Specialist, no question settled ({r['senior']})")
    check(r['preset'] == ['26 18:35'], f"cq2: the Dev preset, Day 26 18:35 by the tea corner ({r['preset']})")

def part_t3pointer(g):
    if not t3on(g, 't3pointer'): return
    print('(t3pointer) the test morning and the board:')
    r = g.ev("""(() => { """ + T3_TEST + """ __tick(); const out = { notes: __notes.slice() };
      setShipNow(14 * 1440 + 515); goToDeck(4); __tick(); out.bay = GUIDE.list.filter(e => /^pu3/.test(e.id)).map(e => e.id + ' L' + e.level + ' ' + ((e.goal() || {}).label || ''));
      __bay(); setShipNow(14 * 1440 + 541); __tick(); const c = W.cur, j = c && SHIP.jobs.find(x => x.id === c.j);
      out.cur = c && c.id + ' ' + c.st; out.job = j && { slot: j.reserved, mach: j.mach, found: hhmm(j.found % 1440), until: hhmm(j.until % 1440), who: j.t3.who.length, store: SHIP.stores.breaker };
      out.worse = puJunction() === (j && j.mach); out.rows = __rows(15);
      SHIP.device.settings.teach = 'off'; SHIP.device.pointsSeen = {}; POINT_Q.length = 0; GUIDE.list.length = 0; ixBoard.open(); guideShift(); __tick();
      const q = POINT_Q.find(x => x.id === 'p:board:lesson:t3'); out.ring = q ? { force: !!q.force, label: q.path.map(s => s.label || '').join('|') } : null;
      const e = GUIDE.list.find(x => x.id === 'pu3:test:15'); out.level = e ? e.level : null; pointFrame(); const el = document.querySelector('#ptr .ptlab'); out.screen = el ? el.textContent : null; ixBoard.close(); SHIP.device.settings.teach = 'first';
      const oid = jobReserve('washer', 15, 541, 98, { until: 14 * 1440 + 1000 }), o = SHIP.jobs.find(x => x.id === oid); __notes.length = 0; if (o && claimJob(o.id)) { setShipNow(14 * 1440 + 600); __tick(); setShipNow(14 * 1440 + 610); __tick(); setShipNow(14 * 1440 + 661); __tick(); out.busy = __notes.filter(n => /waits on the job board/.test(n)).length; dropJob(o.id); } else out.busy = 'no other job to hold';
      return out; })()""")
    print('   ', r)
    check(any('Tier 3 test, 09:00' in n for n in r['notes']), f"t3pointer: the morning's notice once you're up ({r['notes']})")
    check(any(x.startswith('pu3:testday:15 L1') and 'Works bay' in x for x in r['bay']), f"t3pointer: a level 1 arrow to the Works bay from 08:30 ({r['bay']})")
    check(r['cur'] == 't3 do' and r['job'] and r['job']['slot'] == 25 and r['job']['found'] == '09:00' and r['job']['until'] == '15:00' and r['job']['who'] == 2 and r['job']['store'] >= 1 and r['worse'], f"t3pointer: the job held for you 09:00-15:00 in slot 25 on the worse junction, its breaker set aside, two to warn ({r['cur']}, {r['job']})")
    check(r['ring'] and r['ring']['force'] and r['ring']['label'].endswith('Your Tier 3 test: take it') and r['level'] == 1 and 'Tier 3 test' in (r['screen'] or ''), f"t3pointer: the board's ring forced with Teaching arrows Off, named, on screen; the arrow level 1 ({r})")
    check('09:00 Your Tier 3 test' in r['rows'], f"t3pointer: the Schedule's row ({r['rows']})")
    check(r['busy'] == 2, f"t3pointer: one notice an hour while you hold another job: 10:00, not 10:10, 11:01 ({r['busy']})")

def part_t3passed(g):
    if not t3on(g, 't3passed'): return
    print('(t3test) the test, step by step:')
    r = g.ev("""(() => { """ + T3_TEST + """ __tick(); setShipNow(14 * 1440 + 541); __tick(); const c = W.cur, j = SHIP.jobs.find(x => x.id === c.j), out = {};
      const st = () => jobStops(j).map(s => s.step + (s.done ? '+' : '-')).join(' '), arrow = () => GUIDE.list.filter(e => /^pu3:step/.test(e.id)).map(e => (e.goal() || {}).label || '').join('|');
      __said.length = 0; out.take = claimJob(j.id); __tick(); out.said = __said.slice(); out.esc = (worksEscort({ id: 'calder' }, shipNow()) || {}).mode; out.a0 = arrow();
      SHIP.player.carry.push('breaker'); jobStepDone(j.id, 0); out.a1 = arrow(); __said.length = 0; __toasts.length = 0; jobStepDone(j.id, 1); out.plan = __said.slice(); out.who = __toasts.slice(-1); out.a2 = arrow();
      out.off = jobStepDone(j.id, 2).retry; out.offSay = __toasts.slice(-1);
      const p0 = evPerson(j.t3.who[0]), p1 = evPerson(j.t3.who[1]); out.btn = (puChatButton(p0) || {}).label; out.say0 = puChatSay(p0); out.after = puChatButton(p0);
      setShipNow(14 * 1440 + 541 + 31); __tick(); out.told = j.t3.told.slice(); out.by = j.t3.by; out.a3 = arrow();
      out.r = [2, 3, 4].map(k => jobStepDone(j.id, k).ok); out.st = st(); out.done = !!j.workDone; out.cond = SHIP.machines[j.mach].cond; out.a4 = arrow();
      out.watch = (() => { j.workDone = null; const k = (puTalkKind(shipNow()) || [])[0]; j.workDone = shipNow(); return k; })();
      __said.length = 0; __notes.length = 0; out.turnin = turnInJob(j.id); __tick(); out.t3 = puT3(); out.tier = W.tier; out.cur = W.cur; out.passed = __said.slice();
      out.mail = __mail().filter(m => /result/i.test(m)); out.notes = __notes.slice(); out.rows = __rows(16); out.next = worksNext(); out.kind = (puTalkKind(shipNow()) || [])[0]; return out; })()""")
    for k, v in r.items(): print('   ', k, v)
    check(r['take'] and any('Deck 6' in x for x in r['said']) and r['esc'] == 'follow', f"t3test: taken, Calder's word, she follows you ({r['said']}, {r['esc']})")
    check('breaker from main storage' in r['a0'] and 'plan it with Calder' in r['a1'], f"t3test: the arrow names each step: the breaker, the plan ({r['a0']}, {r['a1']})")
    check(len(r['plan']) >= 1 and r['who'] and 'Warn' in r['who'][0][1] and r['a2'].startswith('Warn '), f"t3test: the plan: Calder's talk, the two named, the arrow to the first ({r['plan']}, {r['who']}, {r['a2']})")
    check(r['off'] and 'warn' in r['offSay'][0][1].lower(), f"t3test: the switch refused before both know ({r['offSay']})")
    check(r['btn'] == 'About the shutdown' and r['say0'] and r['after'] is None, f"t3test: \"About the shutdown\" on them, their answer, then gone ({r['btn']}, {r['say0']})")
    check(len(r['told']) == 2 and list(r['by'].values()).count('you') == 1 and list(r['by'].values()).count('calder') == 1, f"t3test: one not found in 30 minutes: Calder tells them ({r['by']})")
    check(all(r['r']) and r['done'] and r['cond'] >= 95 and r['a4'] == 'Turn it in' and r['a3'] == 'Switch it off', f"t3test: switch off, the breaker, back on: the junction put right, the arrow to turn it in ({r['st']}, {r['cond']}, {r['a3']}, {r['a4']})")
    check(r['watch'] == 'pu3.watch', f"t3test: the crew watch you at it ({r['watch']})")
    check(r['turnin'] and r['t3']['passed'] and r['tier'] == 2 and r['cur'] is None and r['passed'], f"t3test: turned in: passed, still Tier 2 till the result, Calder's word ({r['t3']}, {r['passed']})")
    check(any('tomorrow' in m and '08:15' in m for m in r['mail']) and any('tomorrow' in n and '08:15' in n for n in r['notes']), f"t3test: the Mail and the notice name tomorrow, 08:15 ({r['mail']}, {r['notes']})")
    check(any(x.startswith('08:15') and 'result' in x.lower() for x in r['rows']) and 'result' in r['next'].lower() and r['kind'] == 'pu3.passed', f"t3test: the result's row, What's next, the crew's talk ({r['rows']}, {r['next']}, {r['kind']})")
    r = g.ev("""(() => { """ + T3_TEST + """ __tick(); setShipNow(14 * 1440 + 541); __tick(); const c = W.cur;
      for (const t of [14 * 1440 + 900, 14 * 1440 + 901, 14 * 1440 + 960]) { setShipNow(t); machinesNow(); trainTick(t); __tick(); }
      return { t3: puT3(), cur: W.cur && W.cur.st, jobs: SHIP.jobs.filter(x => x.kind === 'tier3' && x.status !== 'done').length, mail: __mail().filter(m => /^Chief Ines Calder: Again/.test(m)), notes: __notes.filter(n => /set again/.test(n)) }; })()""")
    print('   ', r)
    check(r['t3'] and r['t3']['day'] == 17 and not r['t3']['passed'] and r['jobs'] == 0 and r['cur'] == 'ask' and r['mail'] and r['notes'], f"t3test: not taken by 15:00: set again in two workdays (Day 17), the job gone, never failed ({r})")

T3_RES = """const W = __w(16, 300, { xp: 60, tr: { ps: 12, t2: 9, t3: 15 } }); W.tier = 2; W.rank = 'officer'; __friends();
      for (const r of CAREER_LADDER) if (r.id !== 't3' && r.tier <= 2) { W.tr[r.id] = W.tr[r.id] || 9; (W.op[9] = W.op[9] || []).push(r.id); }
      const T = puSet(15); T.passed = true; T.tries = 1;"""
def dlg_run(pick):
    return "let n = 0; while (DIALOGUE && n++ < 40) { const l = DIALOGUE.queue[DIALOGUE.i]; if (l && l.pin) out.pin = n; dialogueStep(l && l.choice ? " + str(pick) + " : undefined); }"
def part_t3result(g):
    if not t3on(g, 't3result'): return
    print('(t3result) the result, first thing:')
    r = g.ev("""(() => { """ + T3_RES + """ const out = { rd: puResultDay() }; setShipNow(15 * 1440 + 361); __bay(); __tick();
      out.occ = SHIP.occasions.filter(x => /^pu3/.test(x.id)).map(x => x.id + ' ' + hhmm(x.at % 1440)); out.mail = __mail().filter(m => /result/i.test(m)); out.notes = __notes.slice(); out.next = worksNext();
      setShipNow(15 * 1440 + 482); __tick(); out.arrow = GUIDE.list.filter(e => /^pu3:result/.test(e.id)).map(e => e.level + ' ' + (e.goal() || {}).label);
      setShipNow(15 * 1440 + 511); goToDeck(3); __tick(); out.seek = !!PU_LIVE.rseek; out.esc = (worksEscort({ id: 'calder' }, shipNow()) || {}).mode;
      const keep = puNearMe; puNearMe = (id, r) => id === 'calder' ? true : keep(id, r); __tick(); puNearMe = keep;
      out.dlg = DIALOGUE && DIALOGUE.id; """ + dlg_run(0) + """
      out.w = [W.tier, W.rank, W.xp]; out.t3 = puT3(); out.rec = worksRecordHead().text; out.bar = SHIP.occasions.filter(x => x.id === 'pu3Bar').map(x => hhmm(x.at % 1440) + ' day ' + (Math.floor(x.at / 1440) + 1));
      out.kind = (puTalkKind(shipNow()) || [])[0]; const f0 = __mail().filter(m => /^(Pell|Tomas|Rina)/.test(m)).length; setShipNow(15 * 1440 + 751); __tick(); out.friends = __mail().filter(m => /^(Pell|Tomas|Rina)/.test(m)).length - f0 + (f0 ? 100 : 0);   // filed at lunch, none before
      """ + T3_RES.replace('const W =', 'const W2 =').replace('W.', 'W2.').replace('const T = puSet', 'const T2 = puSet').replace('T.passed', 'T2.passed').replace('T.tries', 'T2.tries') + """
      setShipNow(15 * 1440 + 400); __tick(); setShipNow(15 * 1440 + 556); __tick(); out.late = [W2.tier, (puT3() || {}).res, __mail().filter(m => /You weren't about/.test(m)).length]; return out; })()""")
    for k, v in r.items(): print('   ', k, v)
    check(r['rd'] == 16 and 'pu3Result 08:15' in r['occ'] and any('08:15' in m for m in r['mail']) and any('08:15' in n for n in r['notes']) and 'today, 08:15' in r['next'], f"t3result: the Mail at 06:00, the notice, booked for 08:15, What's next ({r['occ']}, {r['mail']}, {r['notes']}, {r['next']})")
    check(r['arrow'] and r['arrow'][0].startswith('1 ') and "Calder's office" in r['arrow'][0], f"t3result: a level 1 arrow to her office from 08:00 ({r['arrow']})")
    check(r['seek'] and r['esc'] == 'follow' and r['dlg'] == 'pu3.result', f"t3result: not there at 08:30, she comes to find you, the scene where you are ({r})")
    check(r['w'] == [3, 'senior', 0] and r['t3']['res'] == 16 and 'Senior Officer, Day 16' in r['rec'], f"t3result: Tier 3, Senior Officer, xp 0, the Record's line ({r['w']}, {r['rec']})")
    check(r['bar'] == ['16:30 day 16'] and r['friends'] == 2 and r['kind'] == 'pu3.senior', f"t3result: the bar booked for 16:30 that day, two friends' Mail, the crew's news ({r['bar']}, {r['friends']}, {r['kind']})")
    check(r['late'] == [3, 16, 1], f"t3result: never missed: by Mail by 09:15 ({r['late']})")

def part_t3bar(g):
    if not t3on(g, 't3bar'): return
    print('(t3bar) the Captain pins your bar; the cake:')
    r = g.ev("""(() => { """ + T3_RES + """ const out = {}; setShipNow(15 * 1440 + 520); __bay(); puPromote(shipNow(), 'met');
      out.invite = __mail().filter(m => /^Captain Odile Marrow: Your bar/.test(m)); const a = apptList().find(x => /^pu3Bar@/.test(String(x.occ))); out.places = a && a.places; out.with = a && a.with;
      out.next = worksNext(); __notes.length = 0; __said.length = 0; setShipNow(15 * 1440 + 961); __tick(); out.notice = __notes.slice(); out.go = __said.slice();
      setShipNow(15 * 1440 + 976); goToDeck(4); __tick(); out.arrow = GUIDE.list.filter(e => e.id === 'pu3:bar').map(e => e.level + ' ' + (e.goal() || {}).label + ' ' + (e.goal() || {}).place);
      setShipNow(15 * 1440 + 991); goToDeck(1); player.obj.position.copy(cellPos(...PLACE_OF.get('1-ceremony-you').at)); occasionsTick(shipNow()); meetingsTick(shipNow());
      out.dlg = DIALOGUE && DIALOGUE.id; """ + dlg_run(1) + """ out.t3 = puT3(); out.pip = PLAYER_SPEC.rank; out.barMark = !!PLAYER_SPEC.bar; out.keep = (SHIP.social && SHIP.social.keepsakes || []).map(k => k.what);
      setShipNow(15 * 1440 + 1021); __bay(); __tick(); out.cake = GUIDE.list.filter(e => e.id === 'pu3:cake').map(e => e.level + ' ' + (e.goal() || {}).label);
      const keep = puNearMe; puNearMe = (id, r) => id === 'brennan' ? true : keep(id, r); __said.length = 0; __tick(); puNearMe = keep; out.slice = puT3().cake; out.brennan = __said.filter(x => /^brennan/.test(x));
      let fd = 16; while (weekday(fd) !== 4) fd++; out.fri = [fd, promoCerTimes(fd).at];
      """ + T3_RES.replace('const W =', 'const W2 =').replace('W.', 'W2.').replace('const T = puSet', 'const T2 = puSet').replace('T.passed', 'T2.passed').replace('T.tries', 'T2.tries') + """
      setShipNow(15 * 1440 + 520); puPromote(shipNow(), 'met'); setShipNow(15 * 1440 + 1096); __tick(); out.missed = [(puT3() || {}).bar, __mail().filter(m => /^Captain Odile Marrow: Your bar \\| We missed/.test(m)).length]; return out; })()""")
    for k, v in r.items(): print('   ', k, v)
    check(r['invite'] and '16:30' in r['invite'][0] and r['places'] and r['places'].get('marrow') == '1-ceremony-captain' and len(r['places']) >= 4 and 'vance' in r['with'], f"t3bar: the Captain's invite that morning; the guests on the ceremony spots ({r['invite']}, {r['places']})")
    check('16:30' in r['next'] and any('16:30' in n for n in r['notice']) and any(x.startswith('calder:') for x in r['go']), f"t3bar: What's next, the notice at 16:00, Calder's word in the bay ({r['next']}, {r['notice']}, {r['go']})")
    check(r['arrow'] and r['arrow'][0].startswith('1 ') and '1-ceremony-you' in r['arrow'][0], f"t3bar: a level 1 arrow from 16:15 to your spot ({r['arrow']})")
    check(r['dlg'] == 'pu3.bar' and r.get('pin') and r['t3']['bar'] == 16 and r['pip'] == 2 and r['barMark'] and any('certificate' in k.lower() for k in r['keep']), f"t3bar: the scene with the pin; the bar on your collar (spec.bar, the kit's mark), the certificate ({r})")
    check(r['cake'] and r['cake'][0] == '1 Take a slice' and r['slice'] == 16 and r['brennan'], f"t3bar: the cake after: \"Take a slice\", Brennan's line ({r['cake']}, {r['slice']}, {r['brennan']})")
    check(r['fri'][1] == 1035, f"t3bar: on a Friday at 17:15 ({r['fri']})")
    check(r['missed'] == [16, 1], f"t3bar: missed, by Mail by 18:15 ({r['missed']})")

def part_t3toast(g):
    if not t3on(g, 't3toast'): return
    print('(t3toast) the Captain\'s toast, the next day:')
    r = g.ev("""(() => { """ + T3_RES + """ const out = {}; setShipNow(15 * 1440 + 520); __bay(); puPromote(shipNow(), 'met'); puBar(15 * 1440 + 1010, 'met');
      out.day = puToastDay(); out.rows = __rows(17); setShipNow(16 * 1440 + 481); __tick(); out.occ = SHIP.occasions.filter(x => x.id === 'pu3Toast').map(x => hhmm(x.at % 1440));
      const a = apptList().find(x => /^pu3Toast@/.test(String(x.occ))); out.places = a && a.places; out.mail = __mail().filter(m => /^Captain Odile Marrow: The toast/.test(m)); out.next = worksNext();
      __notes.length = 0; setShipNow(16 * 1440 + 1111); __tick(); out.notice = __notes.slice(); setShipNow(16 * 1440 + 1126); goToDeck(4); __tick(); out.arrow = GUIDE.list.filter(e => e.id === 'pu3:toast').map(e => e.level + ' ' + (e.goal() || {}).label);
      setShipNow(16 * 1440 + 1141); goToDeck(2); player.obj.position.copy(cellPos(...PLACE_OF.get('2-captable-1').at)); occasionsTick(shipNow()); meetingsTick(shipNow()); out.dlg = DIALOGUE && DIALOGUE.id;
      """ + dlg_run(0) + """ out.t3 = puT3(); out.keep = (SHIP.social && SHIP.social.keepsakes || []).map(k => k.what); out.tab = puCheck(); out.next2 = worksNext();
      """ + T3_RES.replace('const W =', 'const W2 =').replace('W.', 'W2.').replace('const T = puSet', 'const T2 = puSet').replace('T.passed', 'T2.passed').replace('T.tries', 'T2.tries') + """
      setShipNow(15 * 1440 + 520); puPromote(shipNow(), 'met'); puBar(15 * 1440 + 1010, 'met'); setShipNow(16 * 1440 + 481); __tick(); setShipNow(16 * 1440 + 1201); __tick();
      out.missed = [(puT3() || {}).toast, __mail().filter(m => /^Captain Odile Marrow: Tonight/.test(m)).length]; return out; })()""")
    for k, v in r.items(): print('   ', k, v)
    check(r['day'] == 17 and '19:00 The toast, 19:00' in r['rows'] and r['occ'] == ['19:00'] and r['places'] and r['places'].get('marrow'), f"t3toast: the next day, 19:00, her quarters, seats at her table ({r['day']}, {r['rows']}, {r['occ']}, {r['places']})")
    check(r['mail'] and 'toast' in r['next'].lower() and r['notice'] and r['arrow'] and r['arrow'][0].startswith('1 '), f"t3toast: the invite, What's next, the notice at 18:30, a level 1 arrow ({r['mail']}, {r['notice']}, {r['arrow']})")
    check(r['dlg'] == 'pu3.toast' and r['t3']['toast'] == 17 and any('menu' in k.lower() for k in r['keep']) and r['tab'] == [] and 'toast' not in r['next2'].lower(), f"t3toast: the scene, the framed menu, the Training tab's rows gone ({r['dlg']}, {r['t3']}, {r['keep']}, {r['tab']})")
    check(r['missed'] == [17, 1], f"t3toast: missed: by Mail, the menu all the same ({r['missed']})")

def part_t3shoulds(g):
    if not t3on(g, 't3shoulds'): return
    print('(t3shoulds) RV20\'s shoulds: the friends\' Mail at lunch, no "reputation down" at the promotion, the presets\' order:')
    r = g.ev("""(() => { """ + T3_RES + """ const out = {}; setShipNow(15 * 1440 + 496); __bay(); GUIDE_SHIFT.band = worksBand(); GUIDE_SHIFT.tier = 2;
      puPromote(shipNow(), 'met'); __toasts.length = 0; guideShiftWords(Math.floor(shipNow()), false); out.toasts = __toasts.map(t => t.join(': '));
      const early = SHIP.mail.filter(m => /^(Pell|Tomas|Rina)/.test(m.from)).length; setShipNow(15 * 1440 + 751); __tick();
      out.friends = SHIP.mail.filter(m => /^(Pell|Tomas|Rina)/.test(m.from)).map(m => hhmm(m.at % 1440) + (m.at > shipNow() ? ' future' : '')); out.early = early;
      const c = devmodeCareerFor(18); out.pre = ['m15', 'm17', 'm19'].map(k => k + ':' + (c.tr[k] === undefined ? '-' : c.tr[k])); return out; })()""")
    print('   ', r)
    check(not any('down' in t for t in r['toasts']), f"t3shoulds: no \"reputation down\" as you're promoted ({r['toasts']})")
    check(r['early'] == 0 and len(r['friends']) == 2 and all(x >= '12:30' and 'future' not in x for x in r['friends']), f"t3shoulds: the friends' Mail filed at lunch, dated then, none before ({r['early']}, {r['friends']})")
    check(r['pre'] == ['m15:17', 'm17:-', 'm19:17'], f"t3shoulds: the Day 18 preset follows the ladder (m15 with m19 on Day 17, no m17) ({r['pre']})")

# seated / blocked (PZ6 for lead 42; W7's escort-follow-fix 87d62f22): Calder's Tier 3 offer comes to find you (a 'follow'
# escort) on Day 15 from 08:00, live, frame by frame:
#   seated:  you sit the game's own way (actStart 'sit') at a lounge seat and a mess seat: she walks over and her offer
#            scene plays. Seated, you stay on the seat's walk tile, which is open, so this passed before the fix too: it
#            guards against the fix breaking the real case
#   blocked: you stand ON a seat's own tile (blocked: no real-play way there is known; W7's and RV23's repro put you there
#            directly): she must aim for the open tile beside you and still arrive. Fails on 0.94.0 6f1915cb (no path, she
#            waits in the corridor), passes from the fix on
SEAT_T = r"""((seat, how) => { if (typeof DIALOGUE !== 'undefined' && DIALOGUE) dialogueEnd(true); actEnd(true);
  const W = __w(14, 470, { xp: 60, tr: { ps: 12, t2: 9 } }); W.tier = 2; W.rank = 'officer'; __friends();
  goToDeck(3); const pl = placeById(seat), w = cellPos(...(pl.walk || pl.at)), s = placeSpot(seat);
  if (how === 'stand') player.obj.position.set(s.x, player.obj.position.y, s.z); else player.obj.position.set(w.x, player.obj.position.y, w.z);
  target.copy(player.obj.position).setY(.7); player.stop(); for (const k of NEED_KEYS) SHIP.player.needs[k] = 90;
  setShipNow(14 * 1440 + 476); if (how === 'sit') actStart('sit', seat);
  const c = cellAt(player.obj.position.x, player.obj.position.z); return { cell: c, open: free(...c) }; })"""
SEAT_ST = r"""(() => { const a = DECK_CREW.find(x => x.p && x.p.id === 'calder'), P = player.obj.position, c = cellAt(P.x, P.z);
  return { t: hhmm(shipNow() % 1440), seek: !!PU_LIVE.seek, act: ACT && ACT.kind, phase: ACT && ACT.phase, open: free(...c), dlg: DIALOGUE ? DIALOGUE.m.id : null,
    calder: a ? Math.round(Math.hypot(a.x - P.x, a.z - P.z) * 10) / 10 : null }; })()"""
def seat_run(g, seat, how):
    s0 = g.ev(f"({SEAT_T})('{seat}', '{how}')"); last = None; sat = None
    for k in range(30):
        g.step(150); last = g.ev(SEAT_ST)
        if last['act'] == 'sit' and last['phase'] == 'do' and sat is None: sat = last['open']
        if last['dlg']: break
    g.ev("if (DIALOGUE) dialogueEnd(true); actEnd(true)")
    return s0, sat, last
def part_seated(g):
    if not t3on(g, 'seated'): return
    print('(seated) Calder finds you while you sit, the game\'s own way:')
    for seat in ('3-lounge-24', '3-mess-9'):
        s0, sat, last = seat_run(g, seat, 'sit'); print('   ', seat, s0, 'seated on an open tile:', sat, last)
        check(sat is True and last['act'] in ('sit', None) and last['dlg'] == 'pu3.offer', f"seated at {seat}: you sit (on its open walk tile), she walks over and her offer plays ({sat} {last})")
def part_blocked(g):
    if not t3on(g, 'blocked'): return
    print('(blocked) a guard: you standing on a seat\'s own (blocked) tile, she still arrives (W7\'s fix; no known real-play path):')
    s0, sat, last = seat_run(g, '3-lounge-24', 'stand'); print('   ', s0, last)
    check(s0['open'] is False and last['dlg'] == 'pu3.offer' and last['seek'] is not None, f"blocked: on a blocked tile, she aims beside you and her offer plays ({s0} {last})")

with sync_playwright() as pw:
    g = Game(pw, sys.argv[1])
    g.step(2)
    check(g.ev(SETUP), 'setup')
    for name, fn in [('off', part_off), ('pointer', part_pointer), ('before', part_before), ('passed', part_passed), ('result', part_result), ('cabin', part_cabin), ('talk', part_talk), ('review', part_review), ('t3off', part_t3off), ('t3before', part_t3before), ('t3pointer', part_t3pointer), ('t3passed', part_t3passed), ('t3result', part_t3result), ('t3bar', part_t3bar), ('t3toast', part_t3toast), ('t3shoulds', part_t3shoulds), ('t4off', part_t4off), ('t4before', part_t4before), ('t4test', part_t4test), ('t4passed', part_t4passed), ('t4welcome', part_t4welcome), ('t4badge', part_t4badge), ('t4move', part_t4move), ('t4dev', part_t4dev), ('seated', part_seated), ('blocked', part_blocked), ('t4carry', part_t4carry), ('refit', part_refit), ('t4eve', part_t4eve), ('t3carry', part_t3carry), ('mt', part_mt), ('mt2', part_mt2), ('mt3', part_mt3), ('mt4', part_mt4), ('cq', part_cq), ('cq2', part_cq2)]:
        if ONLY and name not in ONLY: continue
        try: fn(g)
        except Exception as e: fail(f'{name}: {e}')
    if g.errors: fail('page errors: ' + ' | '.join(g.errors[:5]))
    g.close()
print('PROMO BEATS CHECK OK' if ok else 'PROMO BEATS CHECK FAILED')
sys.exit(0 if ok else 1)
