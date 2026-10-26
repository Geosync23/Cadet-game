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

with sync_playwright() as pw:
    g = Game(pw, sys.argv[1])
    g.step(2)
    check(g.ev(SETUP), 'setup')
    for name, fn in [('off', part_off), ('pointer', part_pointer), ('before', part_before), ('passed', part_passed), ('result', part_result), ('cabin', part_cabin), ('talk', part_talk)]:
        if ONLY and name not in ONLY: continue
        try: fn(g)
        except Exception as e: fail(f'{name}: {e}')
    if g.errors: fail('page errors: ' + ' | '.join(g.errors[:5]))
    g.close()
print('PROMO BEATS CHECK OK' if ok else 'PROMO BEATS CHECK FAILED')
sys.exit(0 if ok else 1)
