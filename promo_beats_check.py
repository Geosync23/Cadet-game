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
    if g.ev(T3): print('(t3off) P5_PROMO3 on in this build: skipped'); return
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

T3_TEST = """const W = __w(15, 300, { xp: 60, tr: { ps: 12, t2: 9 } }); W.tier = 2; W.rank = 'officer'; __friends();
      for (const r of CAREER_LADDER) if (r.id !== 't3' && r.tier <= 2) { W.tr[r.id] = W.tr[r.id] || 9; (W.op[9] = W.op[9] || []).push(r.id); }
      puSet(15); flagSet('pu3.told', 14); flagSet('pu3.notice', 14); setShipNow(14 * 1440 + 361); machinesNow(); careerClock(shipNow(), true); __bay();"""
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
      out.friends = __mail().filter(m => /^(Pell|Tomas|Rina)/.test(m)).length; out.kind = (puTalkKind(shipNow()) || [])[0];
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
      out.friends = SHIP.mail.filter(m => /^(Pell|Tomas|Rina)/.test(m.from)).map(m => hhmm(m.at % 1440));
      const c = devmodeCareerFor(18); out.pre = ['m15', 'm17', 'm19'].map(k => k + ':' + (c.tr[k] === undefined ? '-' : c.tr[k])); return out; })()""")
    print('   ', r)
    check(not any('down' in t for t in r['toasts']), f"t3shoulds: no \"reputation down\" as you're promoted ({r['toasts']})")
    check(len(r['friends']) == 2 and all(x >= '12:30' for x in r['friends']), f"t3shoulds: the friends' Mail at lunch, as their words say ({r['friends']})")
    check(r['pre'] == ['m15:17', 'm17:-', 'm19:17'], f"t3shoulds: the Day 18 preset follows the ladder (m15 with m19 on Day 17, no m17) ({r['pre']})")

with sync_playwright() as pw:
    g = Game(pw, sys.argv[1])
    g.step(2)
    check(g.ev(SETUP), 'setup')
    for name, fn in [('off', part_off), ('pointer', part_pointer), ('before', part_before), ('passed', part_passed), ('result', part_result), ('cabin', part_cabin), ('talk', part_talk), ('review', part_review), ('t3off', part_t3off), ('t3before', part_t3before), ('t3pointer', part_t3pointer), ('t3passed', part_t3passed), ('t3result', part_t3result), ('t3bar', part_t3bar), ('t3toast', part_t3toast), ('t3shoulds', part_t3shoulds)]:
        if ONLY and name not in ONLY: continue
        try: fn(g)
        except Exception as e: fail(f'{name}: {e}')
    if g.errors: fail('page errors: ' + ' | '.join(g.errors[:5]))
    g.close()
print('PROMO BEATS CHECK OK' if ok else 'PROMO BEATS CHECK FAILED')
sys.exit(0 if ok else 1)
