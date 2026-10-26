#!/usr/bin/env python3
"""fridays_check.py: Short Fridays and the Captain's address (section 18f, the Fridays builder FR1;
plans/fridays-build-brief.md), on paper, about a minute a build.

  CADET_CHROME=/opt/pw-browsers/chromium python3 fridays_check.py BUILD.html

With SHORT_FRIDAY off (the build as it is): no short Friday, no address in the traditions, the day shift ends at
17:00 every day. With it on (a test copy is made with the switch line flipped): the day shift ends at 15:30 on
Fridays; the address is on every Friday from Day 5 at 16:00-16:50 and on no other day; it sits inside the events
base's Friday hold (EV_BEATS' 'fridayAddress' row, when the build has it); no other tradition overlaps Friday
15:30-17:00; Marrow and Vance plan the lectern, nobody of the Friday skeleton comes, and the auditorium fills
(Days 5 and 12); the Thursday Mail is the first week's on Day 4 and the usual one after.
The speech (turn 6): every line of every address (content/addresses/, baked as FRI_ADDRESSES) fills or is left out,
never showing a { or a stray ?, at most 90 characters, under every rank, with the events base's readers there and
missing; each Friday's speech has 9-22 lines (the weekly one 9-14), and the weekly pools don't repeat a line within 6
weeks while another fits; in the auditorium on Day 5 the lines come over Marrow and Vance in order, one each turn, the
crowd hushed; a reload mid-speech says the line of the moment, never from the top; anyone not there gets the banner and
the Mail at 16:50 (once); off: nothing new in the save. Prints FRIDAYS CHECK OK.
"""
import os, sys, re, json, pathlib

GAME = sys.argv[1] if len(sys.argv) > 1 else 'starship-cadet.html'
ROOT = pathlib.Path(__file__).resolve().parent
src = open(ROOT / 'cadet_test.py').read().split("a, shots = run(")[0]
exec(src)
from playwright.sync_api import sync_playwright

fails = []
def check(ok, what):
    if not ok: fails.append(what); print('  FAIL', what)
    return ok

text = pathlib.Path(GAME).read_text()
if not re.search(r'^const SHORT_FRIDAY = (true|false);', text, re.M):
    print('FRIDAYS CHECK FAILED: no SHORT_FRIDAY switch in', GAME); sys.exit(1)
work = WORK / 'test'; work.mkdir(parents=True, exist_ok=True)
copies = {}
for on in (False, True):
    p = work / ('_fri_' + ('on' if on else 'off') + '.html')
    p.write_text(re.sub(r'^const SHORT_FRIDAY = (true|false);', 'const SHORT_FRIDAY = %s;' % ('true' if on else 'false'), text, flags=re.M))
    copies[on] = p

PAPER = r"""(() => {
  const out = {}, ppl = schedPeople(), A = 'captains-address';
  out.inTable = SHIP_TRADITIONS.some(e => e.id === A);
  out.ends = [4, 5, 6, 12].map(d => [d, dayShiftEnd(d)]);
  out.on = []; for (let d = 1; d <= 40; d++) { const e = eventsOn(d).find(x => x.id === A); if (e) out.on.push([d, e.from, e.to]); }
  let hold = null; try { const b = EV_BEATS.find(x => x.id === 'fridayAddress'); if (b) hold = { at: b.at, fromDay: b.fromDay, weekday: b.weekday }; } catch (e) { hold = 'none'; }
  out.hold = hold;
  out.clash = [];
  for (let d = 1; d <= 40; d++) if (weekday(d) === 4) for (const e of eventsOn(d)) if (e.id !== A && e.from < 1020 && e.to > 930) out.clash.push([d, e.id, e.from, e.to]);
  out.days = {};
  for (const d of [5, 12]) {
    const at = (d - 1) * 1440 + 970, here = [], lect = [];
    for (const p of ppl) { const w = planWhere(p, at); if (!w || w.deck !== 7) continue; if (w.type === 'rec:lectern') lect.push(p.id); else if (w.type === 'rec-aud' || /^ev-captains-address/.test(w.tag || '')) here.push(p.id); }
    out.days[d] = { here: here.length, lect, skel: ppl.filter(p => friSkeleton(p, d)).map(p => p.id), skelHere: ppl.filter(p => friSkeleton(p, d) && (here.includes(p.id) || lect.includes(p.id))).map(p => p.id),
      night: ppl.filter(p => p.shift === 'night' && here.includes(p.id)).length, nights: ppl.filter(p => p.shift === 'night').length,
      storm: !!eventOn(d), double: ['marrow', 'vance'].filter(id => { const p = ppl.find(q => q.id === id); return p && schedFrame(p, d).double; }) };
  }
  const e5 = eventsOn(5).find(x => x.id === A), e12 = eventsOn(12).find(x => x.id === A);
  out.mail = [e5 && e5.ev.mail ? evText(e5.ev.mail, e5) : null, e12 && e12.ev.mail ? evText(e12.ev.mail, e12) : null];
  out.week1 = friText('mail.fri.week1');
  out.errors = TRAD_ERRORS.filter(x => /captains/.test(x));
  return out;
})()"""

# the speech on paper (turn 6): every line, every rank, the events base's readers there (stubbed) and missing
SPEECH = r"""(() => {
  const out = { bad: [], never: [], counts: {}, repeats: [], weekly: [], save: null, rot21: typeof ROSTER_ROTATIONS !== 'undefined' && ROSTER_ROTATIONS.some(r => r.day > 19 && r.day <= 21 && (r.out || []).length), storm: typeof EV_STORM_ON !== 'undefined' && !!EV_STORM_ON, swap: typeof EV_SWAP_ON !== 'undefined' && !!EV_SWAP_ON, comet: typeof EV_COMET_ON !== 'undefined' && !!EV_COMET_ON && !!SHIP_EVENTS.comet };
  const ranks = ['junior', 'officer', 'senior', 'specialist'], A = FRI_ADDRESSES, filled = new Set();
  // the events base's readers (stubbed: which storm jobs were done, and by you), the ship health boards, your repair
  // cue, a job of yours on the board, the Tiles ladder joined: each way, so every line gets its chance
  const DONE = [[], ['stormBallasts', 'stormBatteries'], ['stormBallasts', 'stormBallasts.you'], ['stormBatteries', 'stormBatteries.you']];
  // (since 0.64.8 the game has its own readers, which a window stub can't shadow: they're swapped for the stubs here,
  // missing = undefined, and put back after; a build without them gets globals, as before)
  const R0 = [typeof eventBandOf === 'function' ? eventBandOf : undefined, typeof eventJobDone === 'function' ? eventJobDone : undefined, typeof eventJobsCount === 'function' ? eventJobsCount : undefined];
  const set = (b, j, c) => { eventBandOf = b; eventJobDone = j; eventJobsCount = c; };
  const stub = (on, k) => on ? set(() => window.__band, (j, you) => DONE[k % 4].includes(j + (you ? '.you' : '')), () => 12) : set(undefined, undefined, undefined);
  const rows0 = shipHealthRows, health = ['fine', 'worn', 'poor'];
  if (!SHIP.works) SHIP.works = { rank: 'junior' };
  const rank0 = SHIP.works.rank, com0 = SHIP.commendations, jobs0 = SHIP.jobs, cues0 = SHIP.social && SHIP.social.cues, joined0 = SHIP.events.joined;
  socInit();
  let k = 0;
  for (const st of [false, true]) for (const band of ['smooth', 'bumpy', 'rough']) for (const rank of ranks) for (const com of [false, true]) {
    k++; stub(st, k); window.__band = band; SHIP.works.rank = rank; SHIP.commendations = com ? [{ event: 'ionStorm', day: 14 }] : [];
    shipHealthRows = () => [{ state: health[k % 3] }];
    SHIP.jobs = com ? [{ id: 'x', status: 'done', doneBy: 'you' }] : [];
    SHIP.social.cues = com ? [{ key: 'repair.fan', you: true, at: 0, until: 1e9 }] : [];
    for (const [id, a] of Object.entries(A)) for (const d of a.day ? [a.day] : Array.from({ length: 52 }, (_, i) => 33 + 7 * i)) for (const b of a.beats) for (const l of b.lines) {
      SHIP.events.joined = com ? Array.from({ length: 7 }, (_, i) => 'tiles-ladder@' + (d - i)) : [];
      const t = friFill(l, d); if (t == null) continue; filled.add(l.id);
      if (/[{}]/.test(t) || /^\s*\?/.test(t) || t.length > 90 || !['marrow', 'vance'].includes(l.who)) out.bad.push([id, d, t]);
    }
  }
  for (const [id, a] of Object.entries(A)) for (const b of a.beats) for (const l of b.lines) if (!filled.has(l.id)) out.never.push([id, l.text, l.if || []]);
  // each Friday's speech, readers there, a junior then an officer; the weekly speech over 12 weeks in order
  stub(true, 1); window.__band = 'bumpy';
  for (const rank of ['junior', 'officer']) {
    SHIP.works.rank = rank; FRI.ring = []; FRI.today = null; FRI_SPEECH = null;
    for (let d = 5; d <= 96; d += 7) {
      const L = friSpeech(d) || []; out.counts[rank + ' ' + d] = L.length;
      for (const l of L) if (/[{}]/.test(l.text) || l.text.length > 90) out.bad.push(['speech', d, l.text]);
      if (rank === 'junior' && d >= 33) out.weekly.push([d, L.map(l => l.text)]);
    }
    // repeats: a weekly line again within 6 weeks while its pool had a line it hadn't used then
    const W = FRI_ADDRESSES['friday-weekly'], seen = {};
    // (pools whose lines always fit and have 7 a pick or more: hello, thought)
    for (const r of FRI.ring) for (const id of r.slice(1)) { const b = W.beats.find(b => b.lines.some(l => l.id === id)); if (seen[id] != null && r[0] - seen[id] < 7 && b && b.lines.length >= 7 * b.pick && b.lines.every(l => !l.if)) out.repeats.push([rank, r[0], b.id, id]); seen[id] = r[0]; }
  }
  out.full = JSON.stringify(FRI).length;                  // the save's fri part after 13 weeks
  set(...R0); shipHealthRows = rows0; SHIP.works.rank = rank0; SHIP.commendations = com0; SHIP.jobs = jobs0; SHIP.social.cues = cues0; SHIP.events.joined = joined0; FRI.ring = []; FRI.today = null; FRI_SPEECH = null;
  const sv = { ship: { decks: {} }, player: {}, crew: {}, flags: SHIP.flags, notes: [] }; for (const f of SAVE_EXTRA) try { f(sv); } catch (e) {} out.save = 'fri' in sv ? JSON.stringify(sv.fri).length : null;
  // turn 8: Zeke's goodnight keys and lines, Halloran's after the mug, the breakfast flag (set, never saved), the clock
  const b5 = INTRO_WEEK.find(b => b.id === 'd5-mug'), SD = SHIP.time.day; SHIP.time.day = 5;
  out.e = { keys: friNightKeys(), night: friNightKeys().map(k => (introWriterLine(k, 'torres-zeke') || [null])[0]), beat: friBeatLines(b5), flag: flag('shortFriday'), saved: 'shortFriday' in (sv.flags || {}), still: flag('shortFriday'), clock: friClock('didout', 940) };
  SHIP.time.day = SD;
  return out;
})()"""
SAVE_OFF = "(() => { const sv = { ship: { decks: {} }, player: {}, crew: {}, flags: {}, notes: [] }; for (const f of SAVE_EXTRA) try { f(sv); } catch (e) {} SHIP.time.day = 5; return ['fri' in sv, typeof friAddressTick, typeof FRI_ADDRESSES === 'object' && Object.keys(FRI_ADDRESSES).length, friNightKeys().length, friBeatLines(INTRO_WEEK.find(b => b.id === 'd5-mug')).length, flag('shortFriday') === undefined, friClock('didout', 940)]; })()"

def aud(g):   # you in the middle of the auditorium (Deck 7's room A)
    g.ev("goToDeck(7)"); g.step(5)
    g.ev("(() => { const M = DECKS[7].map, c = []; for (let j = 0; j < M.length; j++) for (let i = 0; i < M[j].length; i++) if (M[j][i] === 'A') c.push([i, j]); const t = cellPos(...c[Math.floor(c.length / 2)]); player.obj.position.set(t.x, 0, t.z); })()")
    g.step(10)

# PR8's find 3: a save without the fri part (every save from the published game) loaded on a Friday (Day 5, its
# localStorage as a player's), then played on (Deck 4, never in the auditorium): [mailed, heard, work, address count,
# address Mails] at the load and at the end
def old_save(pw, path, day, mn, frames):
    sv = {'v': 2, 'build': 'x', 'time': {'day': day, 'min': mn}, 'player': {'deck': 4, 'tile': [20, 4], 'facing': 0}, 'ship': {'decks': {}, 'eventLog': []}, 'crew': {}}
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    pg = b.new_page(viewport={'width': 390, 'height': 844}); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
    pg.add_init_script(INIT + "try { if (!sessionStorage.getItem('seeded')) { sessionStorage.setItem('seeded', '1'); localStorage.clear(); localStorage.setItem('starship-cadet-save', " + json.dumps(json.dumps(sv)) + "); localStorage.setItem('starship-cadet-arrived', '1'); } } catch (e) {}")
    tmp = work / '_fri_oldsave.html'; tmp.write_text(instrument(pathlib.Path(path).read_text()))
    pg.goto('file://' + str(tmp) + '?debug', timeout=240000); pg.wait_for_function('window.__sc !== undefined || window.__err', timeout=240000)
    ev = lambda x: pg.evaluate('s => window.__sc(s)', x)
    got = "[FRI.mailed, FRI.heard, repInit().ship.work, repInit().cnt.address || 0, (SHIP.mail || []).filter(m => m.subject === FRI_ADDRESSES['friday-d5'].mail[0]).length, clockText()]"
    pg.evaluate('window.__step(2, 1000/30)'); r0 = ev(got)
    for k in range(frames): pg.evaluate('window.__step(20, 1000/30)')
    r = [r0, ev(got), errs[:3]]; b.close(); return r

LIVE = "[shipNow() % 1440, bubbles.list.map(b => [(bubblePerson(b.who) || {}).id, b.text]), FRI_SAID && FRI_SAID[1], simNow() - CHATTER_AT]"

with sync_playwright() as pw:
    res = {}
    for on in (False, True):
        g = Game(pw, str(copies[on]), 390, 844)
        res[on] = g.ev(PAPER)
        res[on]['speech'] = g.ev(SPEECH) if on else g.ev(SAVE_OFF)
        if g.errors: check(False, ('on' if on else 'off') + ': page errors ' + str(g.errors[:3]))
        g.b.close()
    # the room fills in real play (PR3's turn-5 fix): from 15:45 on Day 5, frames played on the rec deck (no jump into the
    # address), who's seated in the auditorium at 16:00 and 16:05, and who's at the lectern
    g = Game(pw, str(copies[True]), 390, 844)
    g.ev("skipTo((5 - 1) * 1440 + 945)"); aud(g)
    CNT = "(() => { const l = DECKS[7].places.find(p => p.type === 'rec:lectern'), L = cellPos(...l.at); let s = 0, lec = []; for (const a of DECK_CREW) { const dd = Math.hypot(a.x - L.x, a.z - L.z); if (dd < 12 && /sit/.test(a.pose || '')) s++; if (dd < 2.5 && a.p) lec.push(a.p.id); } return [Math.floor(shipNow() % 1440), s, lec.sort()]; })()"
    fill = {}
    for k in range(600):
        g.step(10); r = g.ev(CNT)
        for want in (960, 964, 965):
            if r[0] >= want and want not in fill: fill[want] = r[1:]
        if r[0] >= 966: break
    # on to 17:11: who's still waiting for the rec deck's lift (Deck 7) at 16:52 and 17:10
    # [the minute, standing within 4 tiles of the rec deck's lift (a queue), still on the deck while their plan has them
    # elsewhere (on the walk out: the auditorium to the lift is about 10 ship minutes)]
    LIFTQ = "(() => { const t = shipNow(), c = cellPos(...DECKS[7].lift); return [Math.floor(t % 1440), DECK_CREW.filter(a => Math.hypot(a.x - c.x, a.z - c.z) < 4 && !/walk/.test(a.pose || '')).length, DECK_CREW.filter(a => { const w = a.p && whereIs(a.p, t); return w && w.deck !== 7; }).length]; })()"
    lift = {}
    for k in range(1500):
        g.step(10); m, *n = g.ev(LIFTQ)
        for want in (1012, 1030):
            if m >= want and want not in lift: lift[want] = n
        if m >= 1031: break
    planned = g.ev("schedPeople().filter(p => planWhere(p, 4 * 1440 + 970) && planWhere(p, 4 * 1440 + 970).deck === 7 && /captains/.test(planWhere(p, 4 * 1440 + 970).tag || '')).length")
    fill['planned'] = planned
    g2 = Game(pw, str(copies[True]), 390, 844)
    if g.errors: check(False, 'on: page errors in the fill run ' + str(g.errors[:3]))
    g.b.close()
        # turn 7, dinner after the address (on paper): each goer's dinner start, and who washes first
    # PR5's 3b: on paper on Day 5, section 14's late joiners (in after 16:00) leave with the rest, by 16:52 (16:50 and the
    # planner's 2 minutes before the walk out); anyone else may sit on until their later plans (a dinner), but not past 17:20
    late = g2.ev("schedPeople().flatMap(p => planDay(p, 5).filter(s => /captains/.test(s.tag || '') && s.to > 4 * 1440 + (s.from > 4 * 1440 + 960 ? 1012 : 1040)).map(s => [p.id, s.from - 4 * 1440, s.to - 4 * 1440]))")
    sit_on = g2.ev("(() => { const t = schedPeople().flatMap(p => planDay(p, 5).filter(s => /captains/.test(s.tag || '')).map(s => s.to - 4 * 1440)); return [t.filter(x => x <= 1012).length, t.filter(x => x > 1012).length, Math.max(...t)]; })()")
    dinner = g2.ev("""(() => { const b = 4 * 1440, st = [], wash = [];
      for (const p of schedPeople()) { const P = planDay(p, 5); if (!P.some(s => /captains/.test(s.tag || ''))) continue;
        const dn = P.find(s => s.act === 'dinner' && s.from >= b + 1000); if (dn) st.push(dn.from - b);
        const a = P.findIndex(s => /captains/.test(s.tag || '')); if (P.slice(a + 1).some(s => s.act === 'wash' && s.deck === 4 && (!dn || s.from < dn.from))) wash.push(p.id); }
      st.sort((x, y) => x - y); return { n: st.length, spread: [st[0], st[Math.floor(st.length * .8)]], median: st[st.length >> 1], by10: st.filter(x => x < 1030).length, wash: wash.length }; })()""")
    g2.b.close()
        # the speech in the auditorium on Day 5 (on): in order, over its speakers, the crowd hushed; then a reload mid-speech
    g = Game(pw, str(copies[True]), 390, 844)
    g.ev("skipTo((5 - 1) * 1440 + 958)"); aud(g)
    speech = g.ev("friSpeech(5).map(l => [l.who, l.text])")
    said, hush, idx = [], 0, []
    for k in range(420):
        g.step(20)
        m, bub, i, gap = g.ev(LIVE)
        for who, t in bub:
            if [who, t] in speech and (not said or said[-1] != [who, t]): said.append([who, t])
        if 962 <= m < 1008 and gap > 1000: hush += 1
        if i is not None and (not idx or idx[-1] != i): idx.append(i)
        if m >= 1012: break
    live = { 'n': len(speech), 'said': len(said), 'order': said == [x for x in speech if x in said], 'hush': hush, 'idx': idx[:3], 'heard': g.ev('FRI.heard'), 'mailed': g.ev('FRI.mailed') }
    # a reload mid-speech (the save's today list kept, the line shown forgotten): the line of the moment, not the first
    g.ev("skipTo((19 - 1) * 1440 + 958)"); aud(g); g.step(40)
    g.ev("skipTo((19 - 1) * 1440 + 985)"); aud(g)
    keep = g.ev("JSON.stringify(FRI.today)")
    g.ev("FRI_SPEECH = null; FRI_SAID = null; bubbleClear()"); g.step(10)
    live['reload'] = g.ev("[FRI_SAID && FRI_SAID[1], Math.floor((shipNow() % 1440 - FRI_TALK[0]) * friSpeech(19).length / (FRI_TALK[1] - FRI_TALK[0])), JSON.stringify(FRI.today)]")
    live['reloadKeep'] = keep == live['reload'][2]
    # missed (Day 26 on Deck 4 all afternoon): the banner and the Mail at 16:50, once
    g.ev("goToDeck(4)"); g.ev("skipTo((26 - 1) * 1440 + 1005)"); g.step(5)
    g.ev("if (typeof GUIDE_ON !== 'undefined' && GUIDE_ON) { GUIDE.tq.length = 0; guideToast = () => false; }")   # every pop-up shows at once (the queue is arrows_check's): with it, a queued banner was shown later by a second toast() call and counted twice (FX4, 0.92.0's round)
    g.ev("window.__toasts = []; { const t0 = toast; toast = (t, x) => { window.__toasts.push([t, x]); t0(t, x); }; }")
    live['w26'] = g.ev("[repInit().ship.work, repInit().cnt.address || 0, playerShiftOn(26)]")
    for k in range(40): g.step(20)
    live['missed'] = g.ev("[FRI.mailed, FRI.heard, window.__toasts.filter(x => /missed/.test(x[1])).length]")
    live['dip'] = g.ev("[window.__w0 = repInit().ship.work, repInit().cnt.address || 0]")
    # turn 7: missed it on a shift day (Day 26 just now): a dip the size of being late; on a leave day (Day 33): none
    g.ev("goToDeck(4)"); g.ev("skipTo((33 - 1) * 1440 + 400)"); g.step(5)
    g.ev("careerInit(); SHIP.career.b.push(33)")
    g.ev("skipTo((33 - 1) * 1440 + 1005)"); g.step(5)
    w33 = g.ev("[repInit().ship.work, repInit().cnt.address || 0, playerShiftOn(33)]")
    for k in range(40): g.step(20)
    live['leave'] = [w33, g.ev("[repInit().ship.work, repInit().cnt.address || 0, FRI.mailed]")]
    live['mails'] = g.ev("(SHIP.mail || []).filter(m => m.subject === FRI_ADDRESSES['friday-d26'].mail[0] && m.at >= 25 * 1440 + 1000 && m.at < 26 * 1440).length")
    # PR5's turn-6 fix 2: a jump across Friday's 16:50 (Day 40, 15:00 to Saturday 07:00, as a sleep would): the banner,
    # the Mail (stamped 16:50) and the dip all the same, once
    g.ev("goToDeck(4)"); g.ev("skipTo((40 - 1) * 1440 + 900)"); g.step(5)
    w40 = g.ev("window.__toasts = []; [repInit().ship.work, repInit().cnt.address || 0, playerShiftOn(40)]")
    g.ev("skipTo((41 - 1) * 1440 + 420)"); g.step(5)
    live['skip'] = [w40, g.ev("[repInit().ship.work, repInit().cnt.address || 0, FRI.mailed, window.__toasts.filter(x => /missed/.test(x[1])).length, (SHIP.mail || []).filter(m => m.at === 39 * 1440 + 1010).length]")]
    # PR5's 3a: a weekly speech (Day 47) reloaded with the cache cleared and a condition changed (your rank) keeps its
    # lines (the save's FRI.today), not a fresh pick: only lines of the day's list, in its order (a rank line may drop)
    live['weekly'] = g.ev("(() => { SHIP.works.rank = 'junior'; FRI_SPEECH = null; const a = friSpeech(47).map(l => l.id); FRI_SPEECH = null; SHIP.works.rank = 'senior'; const b = friSpeech(47).map(l => l.id); return [a.length, b.length, b.every((id, i) => a.includes(id) && (i === 0 || a.indexOf(id) > a.indexOf(b[i - 1])))]; })()")
    live['errors'] = g.errors[:3]
    g.b.close()
    live['old'] = old_save(pw, copies[True], 5, 18 * 60, 30)      # after the address: nothing missed
    live['oldBefore'] = old_save(pw, copies[True], 5, 16 * 60 + 47, 40)   # before its end: missed at 16:50 as usual

off, on = res[False], res[True]
print('off:', json.dumps({k: off[k] for k in ('inTable', 'ends', 'on')}))
check(not off['inTable'] and not off['on'], 'off: the address is in the game')
check(all(e == 1020 for _, e in off['ends']), 'off: a shift ending before 17:00 %s' % off['ends'])

print('on: ends', on['ends'], '| address on', on['on'][:6], '| hold', on['hold'])
check(on['inTable'], 'on: the address is not in the traditions')
check(dict(on['ends']) == {4: 1020, 5: 930, 6: 1020, 12: 930}, 'on: shift ends %s' % on['ends'])
days = [d for d, _, _ in on['on']]
check(days == [d for d in range(5, 41) if (d - 1) % 7 == 4], 'on: the address on days %s (want every Friday from Day 5)' % days)
check(all(f == 960 and t == 1010 for _, f, t in on['on']), 'on: the address not at 16:00-16:50 %s' % on['on'])
h = on['hold']
if isinstance(h, dict):
    check(h['weekday'] == 4 and h['at'][0] <= 960 and h['at'][1] >= 1010 and h['fromDay'] <= 5, 'on: the address is outside the Friday hold %s' % h)
else:
    print('  (no EV_BEATS in this build: the hold is checked once the events base is in)')
check(not on['clash'], 'on: traditions overlapping Friday 15:30-17:00 %s' % on['clash'])
for d, x in on['days'].items():
    print('  Day %s at 16:10: %d in the seats, lectern %s, skeleton %s (here: %s), night shift %d of %d' % (d, x['here'], x['lect'], x['skel'], x['skelHere'], x['night'], x['nights']))
    if x['storm'] and x['double'] and not x['lect']:
        print('  (Day %s: %s on the storm\'s double shift: the events base\'s storm update exempts them for the address, EV1)' % (d, x['double']))
    else:
        check(sorted(x['lect']) == ['marrow', 'vance'], 'on: Day %s lectern %s' % (d, x['lect']))
    check(not x['skelHere'], 'on: Day %s skeleton at the address %s' % (d, x['skelHere']))
    check(len(x['skel']) == 3, 'on: Day %s skeleton %s' % (d, x['skel']))
    check(40 <= x['here'] <= 76, 'on: Day %s %d in the seats (want 40-76)' % (d, x['here']))
print('  Mail:', on['mail'])
check(on['mail'][0] == on['week1'] and on['week1'], 'on: Day 4 Mail is not the first week\'s')
check(on['mail'][1] and on['mail'][1] != on['week1'], 'on: Day 11 Mail is the first week\'s')
check(not on['errors'], 'on: tradition errors %s' % on['errors'])
so = off['speech']
check(so[0] is False and so[1] == 'function' and so[2] == 5, 'off: the save gains fri, or the speech isn\'t baked %s' % so)
check(so[3:] == [4, 0, True, None], 'off: part E is on (goodnight keys, Halloran\'s lines, the breakfast flag, the clock words) %s' % so[3:])
e = on['speech']['e']
print('  part E (on): goodnight %s; Halloran %s; flag %s (saved: %s); clock: %s' % (e['night'], e['beat'], e['flag'], e['saved'], e['clock']))
check(len(e['keys']) == 6 and all(e['night']) and len(e['beat']) == 3 and e['flag'] is True and not e['saved'] and e['still'] is True and e['clock'] and '15:40' in e['clock'], 'on: part E %s' % e)
sp = on['speech']
print('  speech lines a Friday:', sp['counts'])
print('  the weekly speech, Day 33:', len(sp['weekly'][0][1]), 'lines;', sp['weekly'][0][1][:3], '...')
print('  lines that never fill (want only myshift:night\'s, and the storm\'s while it is off):', sp['never'])
print('  the save\'s fri part: %s bytes fresh, %s with a full ring (7 weeks)' % (sp['save'], sp['full']))
check(sp['full'] < 1200, 'on: the save\'s fri part is %s bytes' % sp['full'])
check(not sp['bad'], 'on: lines showing a slot or a ?, too long, or not Marrow\'s or Vance\'s %s' % sp['bad'][:4])
# never: your night shifts (Pillar 5's); the Day 19 leavers ({sunleavers}: none before the first rotation, Day 35 until
# claude/patch-crew brings it to Day 21); with the storm update
# off (EV_STORM_ON, or none in the build), its own lines: done:storm*, band: and {stormjobs} (the game's readers say nothing)
stormy = lambda x: not sp['storm'] and (any(re.search(r'(^|[ !|])(done:storm|band:)', c) for c in x[2]) or '{stormjobs}' in x[1])
swapped = lambda x: ('swap' in x[2] and not sp.get('swap')) or ('!swap' in x[2] and sp.get('swap')) or ('comet' in x[2] and not sp.get('comet')) or ('!comet' in x[2] and sp.get('comet'))   # the event swap (0.93.2): its lines while off, today's while on (CR6's find)
never = [x[1] for x in sp['never'] if not any('myshift:night' in c for c in x[2]) and not (x[0] == 'friday-d19' and ('{sunleavers}' in x[1] or 'arriving' in x[2]) and not sp['rot21']) and not stormy(x) and not swapped(x)]
check(not never, 'on: lines that never fill %s' % never)
check(all(9 <= n <= 22 for n in sp['counts'].values()) and all(9 <= len(t) <= 14 for _, t in sp['weekly']), 'on: a speech with too few or many lines %s' % sp['counts'])
check(not sp['repeats'], 'on: weekly lines repeated within 6 weeks %s' % sp['repeats'][:4])
print('  Day 5 in real play from 15:45: at 16:00 %d seated, lectern %s; at 16:04 %s; at 16:05 %d seated, lectern %s (%d planned there at 16:10)' % (fill[960][0], fill[960][1], fill[964][1], fill[965][0], fill[965][1], fill['planned']))
# Marrow by 16:00; Vance's command shift runs to 15:44 on a Friday and the walk from the lift is about 17 minutes, so the
# speech (FRI_TALK) starts at 16:04, when he's there
check('marrow' in fill[960][1], 'on: Day 5, Marrow not at the lectern at 16:00 %s' % fill[960][1])
check(fill[964][1] == ['marrow', 'vance'], 'on: Day 5, the lectern at 16:04 %s (want Marrow and Vance)' % fill[964][1])
check(fill[965][0] >= .8 * fill['planned'], 'on: Day 5, %d of %d seated by 16:05' % (fill[965][0], fill['planned']))
print('  Day 5 in the auditorium:', {k: live[k] for k in ('n', 'said', 'order', 'hush', 'idx', 'heard', 'mailed')})
check(live['said'] == live['n'] and live['order'], 'on: Day 5, %d of %d lines said in order' % (live['said'], live['n']))
check(live['hush'] == 0, 'on: Day 5, the chatter not hushed in %d samples' % live['hush'])
check(live['heard'] == 5 and live['mailed'] != 5, 'on: Day 5, heard %s mailed %s' % (live['heard'], live['mailed']))
print('  a reload at 16:25 on Day 19:', live['reload'][:2], 'kept the speech:', live['reloadKeep'])
check(live['reload'][0] == live['reload'][1] and live['reload'][0] > 0, 'on: a reload mid-speech said line %s, not %s' % tuple(live['reload'][:2]))
check(live['reloadKeep'], 'on: a reload changed the speech')
print('  missed on Day 26 (mailed, heard, banners):', live['missed'], 'mails', live['mails'])
check(live['missed'][0] == 26 and live['missed'][1] != 26 and live['missed'][2] == 1 and live['mails'] == 1, 'on: the missed banner and Mail %s %s' % (live['missed'], live['mails']))
print('  missed it on Day 26 (work, count, shift day): before %s, after %s' % (live['w26'], live['dip']))
# (the dip is repAdd's work -2, as being late; near the bottom of the scale it counts for less, so only its count and direction)
check(live['w26'][2] and live['dip'][1] == live['w26'][1] + 1 and live['dip'][0] < live['w26'][0], 'on: missing the address on a shift day: work %s -> %s' % (live['w26'], live['dip']))
print('  missed it on a leave day (Day 33): before %s, after %s' % tuple(live['leave']))
check(live['leave'][0][2] is False and live['leave'][1][:2] == live['leave'][0][:2] and live['leave'][1][2] == 33, 'on: a dip (or no Mail) on a leave day %s' % live['leave'])
print('  dinner after the address, Day 5 (planned; spread: first and 80th percentile; the rest have later plans): %s' % dinner)
check(dinner['n'] >= 30 and dinner['spread'][0] >= 1020 and dinner['spread'][1] <= 1080 and dinner['by10'] <= .45 * dinner['n'], 'on: Day 5 dinner after the address not spread over 17:00-17:50 %s' % dinner)
print('  the rec deck lift after the address, Day 5 in play [queued at the lift, still walking out]: at 16:52 %s, at 17:10 %s' % (lift.get(1012), lift.get(1030)))
check(lift.get(1030, [99])[0] <= 3, 'on: Day 5, %s queued at the rec deck lift at 17:10' % lift.get(1030))
print('  a jump across 16:50 on Day 40 (work, count, shift day | work, count, mailed, banners, Mails at 16:50):', live['skip'])
sk0, sk1 = live['skip']
check(sk1[2] == 40 and sk1[3] == 1 and sk1[4] == 1 and (sk1[1] == sk0[1] + 1 if sk0[2] else sk1[1] == sk0[1]), 'on: a jump across Friday 16:50 without the banner, Mail or dip %s' % live['skip'])
print('  the weekly speech on Day 47 reloaded with your rank changed (lines before, after, only the day\'s in order):', live['weekly'])
check(live['weekly'][0] >= 9 and live['weekly'][2], 'on: a reload of the weekly speech picked again %s' % live['weekly'])
print('  the address on Day 5, planned stays (gone by 16:52, sitting on until later plans, the last minute):', sit_on, 'too late:', late)
check(not late, 'on: people planned in the address too long on Day 5 (a late joiner past 16:52, anyone past 17:20) %s' % late[:6])
print('  an old save (no fri) loaded on Day 5 at 18:00, then played [mailed, heard, work, count, Mails, clock] at load / later:', live['old'][:2])
o0, o1, oe = live['old']
check(o0[0] == 5 and o1[:5] == o0[:5] and o0[3] == 0 and o0[4] == 0 and not oe, 'on: an old save loaded on a Friday evening got the missed address %s' % live['old'])
print('  the same loaded at 16:47 and played past 16:50:', live['oldBefore'][:2])
b0, b1, be = live['oldBefore']
check(b0[0] == 0 and b1[0] == 5 and b1[4] == 1 and not be, 'on: an old save loaded before 16:50 not missed at 16:50 %s' % live['oldBefore'])
check(not live['errors'], 'on: page errors in the live run %s' % live['errors'])
print('FRIDAYS CHECK OK' if not fails else 'FRIDAYS CHECK FAILED (%d)' % len(fails))
sys.exit(1 if fails else 0)
