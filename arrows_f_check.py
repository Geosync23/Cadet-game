# Starship Cadet: the arrows plan's pieces F3 and F4 (AC1): the scanner and Fault notes, the burst pipe.
# In a copy of the build with POINT_ON true and GUIDE_ON set true while it runs, at 390 x 844:
#   F4: the burst pipe's call and follow are level-1 queue entries (incGoalSet / incGoalClear), gone when cleared; its
#       stops say "Close the valve upstream of the wet" and "Mop up (1 of 2)"; on the "Which valve?" card the pointer
#       is on the last valve (the one nearest the wet), gone when picked
#   F3: the Scanner: the pointer on the bars, then on the low part's Fetch, gone when fetched; a head-scratcher: the
#       Device button, the Works tile, the Fault notes tab, a suspect a found note rules out, Where next? (its arrow a
#       queue entry that leaves your tracking alone, gone when the case is called), Call it once one is left
# And in the build as it is (both off): incGoalSet sets the arrow directly, no stop words, Where next? as before.
# Setup and environment as for cadet_test.py.  Run:  python3 arrows_f_check.py BUILD.html
import sys, json, pathlib
exec(open(__file__.replace('arrows_f_check.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
RUN_ID = f'p{os.getpid()}_'   # FX18-1: this run's copies carry the process id (two runs in one CADET_WORK never open each other's), gone at exit
__import__('atexit').register(lambda: [f.unlink(missing_ok=True) for f in (WORK / 'test').glob(f'*_{RUN_ID}*') if f.is_file()])
from playwright.sync_api import sync_playwright

ok = True
def check(cond, msg):
    global ok
    if not cond: ok = False; print('FAIL', msg)
    return cond

WHERE = r"""(() => { const g = document.getElementById('ptr'); if (!g || g.hidden) return { up: false, now: pointNow() };
  const a = POINT.aim; return { up: true, now: pointNow(), label: g.children[2].textContent, text: a ? a.textContent.slice(0, 40) : null }; })()"""

def arrows_off(src):                                 # the build with the teaching arrows switched off (as before 0.92.0), for the parts that test "off"
    return src.replace('const POINT_ON = true;', 'const POINT_ON = false;', 1).replace('var GUIDE_ON = true;', 'var GUIDE_ON = false;', 1)

def run(path):
    src = arrows_off(pathlib.Path(path).read_text())
    if not check('const POINT_ON = false;' in src and 'function incStopWord' in src and 'function caseNextGoal' in src, 'the build has F3 and F4'): return
    on = WORK / 'test' / ('_f34_on_' + RUN_ID + pathlib.Path(path).name)
    on.write_text(src.replace('const POINT_ON = false;', 'const POINT_ON = true;', 1))
    off = WORK / 'test' / ('_f34_off_' + RUN_ID + pathlib.Path(path).name); off.write_text(src); path = str(off)
    with sync_playwright() as pw:
        print('off (the build switched off):')
        g = Game(pw, path, 390, 844); g.step(3)
        r = g.ev("""(() => { clearGoal(); incGoalSet({ deck: 4, room: 'w', label: 'Follow test' }, 'calder'); const a = IX_GOAL && IX_GOAL.label; incGoalClear();
          const w = incStopWord({ kind: 'incident', inc: 'burst', deck: 4, id: 'x' }, 1), n = caseNextGoal({ calls: [] }, null) === setGoal;
          return { a, after: IX_GOAL && IX_GOAL.label, w, n, list: GUIDE.list.length }; })()""")
        print('  ', r)
        check(r['a'] == 'Follow test' and r['after'] is None and r['w'] is None and r['n'] and r['list'] == 0, f'off: as before ({r})')
        g.close()
        print('on:')
        g = Game(pw, str(on), 390, 844); g.step(3)
        where = lambda: g.ev(WHERE)
        g.ev("GUIDE_ON = true; guideStart(); SHIP.player.track = undefined; clearGoal(); worksInit(WORKS_START); while (TIP_Q.length) tipDone()")
        # ---- F4: the queue entries
        r = g.ev("""(() => { const lab = () => { GUIDE.key = ''; const x = goalNow(); return x ? x.label : null; };
          incGoalSet({ deck: 4, place: incPlace('4-valve-panel'), label: 'Follow Calder to the burst pipe, Deck 4' }, 'calder');
          const e = guideList().find(x => x.id === 'inc:m6'), a = lab(), direct = !!IX_GOAL; incGoalClear(); return { level: e && e.level, a, direct, after: lab(), live: guideList().some(x => x.id === 'inc:m6') }; })()""")
        print('  F4 follow:', r)
        check(r['level'] == 1 and r['a'] and r['a'].startswith('Follow Calder') and not r['direct'], f'F4: the follow is a level-1 queue entry, not a direct arrow ({r})')
        check(not r['live'] and not str(r['after'] or '').startswith('Follow'), f'F4: cleared, gone ({r})')
        far = g.ev("""(() => { const a = DECK_CREW.find(x => x.p); if (!a) return null; const q = { g: { deck: deckDef.num === 4 ? 5 : 4, room: 'w', label: 'x' }, by: a.p.id }, P = player.obj.position, keep = [P.x, P.z];
          P.x = a.x + 9; P.z = a.z; const far = incGoalNow(q); P.x = a.x + 1; P.z = a.z; const near = incGoalNow(q); P.x = keep[0]; P.z = keep[1];
          return { far: far.crew || null, farDeck: far.deck, near: near.crew || null, nearDeck: near.deck, who: a.p.id, here: deckDef.num }; })()""")
        print('  F4 follow target:', far)
        if far: check(far['far'] is None and far['near'] is None and far['farDeck'] != far['here'] and far['nearDeck'] != far['here'], f'F4: the follow points where the teacher is going (the pipe), never at her (RV6: that stalls the lesson) ({far})')
        check(g.ev("incWho('calder')") == 'Calder', 'F4: the call and the follow say "Calder", as the training arrows do')
        r = g.ev("""(() => { const j = { kind: 'incident', inc: 'burst', deck: 4, id: 'x' }; return [0, 1, 2].map(k => incStopWord(j, k)); })()""")
        print('  F4 stops:', r)
        check(r[0] == 'Close the valve upstream of the wet' and r[1] == 'Mop up (1 of 2)' and r[2] == 'Mop up (2 of 2)', f'F4: the stops\' words ({r})')
        n = g.ev("""(() => { const line = (DECKS[4] && DECKS[4].valveLine) || [1, 2, 3]; SHIP.jobs.push({ id: 'f4-inc', kind: 'incident', inc: 'burst', deck: 4, status: 'claimed', claimedBy: 'you', parts: [], posted: shipNow() });
          window.__vk = null; deviceChoose({ title: 'Which valve?', text: 'Close one.', choices: line.map((x, k) => 'Valve ' + (k + 1)) }, k => { __vk = k; }); return line.length; })()""")
        g.step(2); p = where(); g.shot(str(WORK / 'test' / 'f34-valve.png'))
        check(p['up'] and p['now'] == 'p:inc:valve' and p['text'] == f'Valve {n}', f'F4: the valve card: on the valve nearest the wet (Valve {n}) ({p})')
        g.ev(f"document.querySelectorAll('#devDlg .btns button')[{n - 1}].click()"); g.step(2); p = where()
        check(not p['up'] and g.ev('__vk') == n - 1, f'F4: picked, gone ({p})')
        g.ev("SHIP.jobs = SHIP.jobs.filter(j => j.id !== 'f4-inc')")
        # ---- F3: the Scanner
        sj = g.ev("""(() => { toolGive('scanner'); const m = machineList().find(m => !m.stub && caseCauses(m).some(x => x.part)), f = caseCauses(m).find(x => x.part);
          SHIP.jobs.push({ id: 'f3-scan', machine: m.id, deck: m.deck, kind: 'repair', cause: f.id, urgency: 1, posted: shipNow(), found: shipNow(), claimedBy: 'you', status: 'claimed', parts: [] });
          const ok = scanOpen('f3-scan'), J = SHIP.jobs.find(j => j.id === 'f3-scan'), low = J.scan.slice().sort((a, b) => a[1] - b[1])[0][0];
          J.scan.push(J.scan.splice(J.scan.findIndex(r => r[0] === low), 1)[0]); deviceRefresh(); while (TIP_Q.length) tipDone(); return { ok, low, cause: f.part }; })()""")
        g.step(2); p = where(); g.shot(str(WORK / 'test' / 'f34-scan-bars.png'))
        check(sj['ok'] and p['up'] and p['now'] == 'p:scan' and 'bars' in p['label'], f'F3: the Scanner: first on the bars ({sj}, {p})')
        g.step(110); p = where(); g.shot(str(WORK / 'test' / 'f34-scan-fetch.png'))   # over 3 seconds
        check(p['up'] and p['text'] == 'Fetch: ' + sj['low'] and sj['low'] == sj['cause'], f'F3: then on the low part\'s Fetch ({p}, {sj})')
        g.ev("(() => { const b = buttonFor({ app: 'scanner', do: 'pick', arg: 'f3-scan|' + " + json.dumps(sj['low']) + " }); b.click(); })()"); g.step(2); p = where()
        check(not p['up'] and g.ev("SHIP.jobs.find(j => j.id === 'f3-scan').picked") == sj['low'], f'F3: fetched, gone ({p})')
        g.ev("deviceClose(); SHIP.jobs = SHIP.jobs.filter(j => j.id !== 'f3-scan')"); g.step(2)
        # ---- F3: a head-scratcher in Fault notes
        cs = g.ev("""(() => { const m = machineList().find(x => x.kind === 'washer'), d = SHIP.time.day, C = caseState();
          const j = { id: 'f3-case', machine: m.id, deck: m.deck, kind: 'repair', urgency: 1, posted: shipNow(), found: shipNow(), parts: [], status: 'claimed', claimedBy: 'you', cause: 'pump' }; SHIP.jobs.push(j);
          let r = null; for (let k = 0; k < 40 && !(r && r.c); k++) r = caseMake(j, 'p3', k, d); if (!r || !r.c) return { why: r && r.why };
          const c = r.c; c.wait = false; caseShow(c, j); j.case = c.id; C.open.push(c);
          const k1 = c.clues.find(k => (k.kills || []).length && k.kills.some(s => s !== c.cause)); if (k1) c.got.push(k1.id);
          SHIP.player.track = 'f3-case'; while (TIP_Q.length) tipDone(); MACH_REV++; return { id: c.id, app: caseApp(), sus: c.sus.length, clues: c.clues.length, got: c.got.slice(), cause: c.cause }; })()""")
        print('  F3 case:', cs)
        if check(cs.get('id'), f'F3: a test head-scratcher made ({cs})'):
            sc = g.ev("(() => { delete SHIP.device.pointsSeen['p:scan']; const ok = scanOpen('f3-case'); return { ok, app: DEV.app }; })()"); g.step(2); p = where()
            check(sc['ok'] and p['now'] != 'p:scan', f'F3: no Scanner pointer on a head-scratcher (every suspect reads worn) ({sc}, {p})')
            g.ev("deviceClose(); while (TIP_Q.length) tipDone()"); g.step(2); p = where()
            check(p['up'] and p['now'] == 'p:case:open' and p['label'] == 'Open your device', f'F3: device shut: on the Device button ({p})')
            g.page.click('#devBtn'); g.ev("while (TIP_Q.length) tipDone()"); g.step(2); p = where()
            check(p['up'] and p['now'] == 'p:case:open' and 'head-scratcher' in p['label'].lower(), f'F3: then the Works tile ({p})')
            g.ev("tileFor('works').click()"); g.step(2); p = where()
            if cs['app'] == 'works': check(p['up'] and p['text'] and p['text'].startswith('Fault notes'), f'F3: then the Fault notes tab ({p})'); g.ev("buttonFor({ app: 'works', do: 'tab', arg: 'faults' }).click()"); g.step(2)
            p = where(); g.shot(str(WORK / 'test' / 'f34-case-cross.png'))
            check(p['up'] and p['now'] == 'p:case:cross', f'F3: in Fault notes: on a suspect a found note rules out ({p})')
            g.ev("(() => { const c = caseById(" + json.dumps(cs['id']) + "); const b = POINT.aim; b.click(); })()"); g.step(2); p = where()
            check(p['up'] and p['now'] == 'p:case:next', f'F3: crossed out: then Where next? ({p})')
            tr = g.ev("SHIP.player.track")
            g.ev("POINT.aim.click()"); g.step(2)
            nx = g.ev("""(() => { GUIDE.key = ''; const e = guideList().find(x => x.id.endsWith(':next')), g = goalNow(); return { e: e && e.level, lab: g && g.label, track: SHIP.player.track, direct: !!IX_GOAL }; })()""")
            check(nx['e'] == 2 and nx['track'] == tr and not nx['direct'], f'F3: Where next?\'s arrow is a level-2 queue entry and tracking is left alone ({nx}, track was {tr})')
            g.ev("""(() => { const c = caseById(""" + json.dumps(cs['id']) + """); for (const s of c.sus) if (s !== c.cause && !c.crossed.includes(s)) c.crossed.push(s); MACH_REV++; deviceRefresh(); })()""")
            g.step(2); p = where(); g.shot(str(WORK / 'test' / 'f34-case-call.png'))
            check(p['up'] and p['now'] == 'p:case:call' and p['text'] and p['text'].startswith('Call it'), f'F3: one suspect left: on Call it ({p})')
            g.ev("POINT.aim.click()"); g.step(2)
            g.ev("(() => { const b = [...document.querySelectorAll('#devBody button')].find(b => b.textContent === 'Yes'); if (b) b.click(); })()"); g.ev("ixGoalAt = -1"); g.step(2)
            after = g.ev("""(() => { GUIDE.key = ''; const g = goalNow(); const js = ixJobStep(); return { next: guideList().some(x => x.id.endsWith(':next')), lab: g && g.label, job: js && js.label, calls: caseById(""" + json.dumps(cs['id']) + """).calls.length, up: !document.getElementById('ptr').hidden }; })()""")
            check(g.ev("(() => { const c = caseById(" + json.dumps(cs['id']) + "); return c.clues.length > c.got.length; })()"), 'F3: (the call comes before every clue is found)')
            check(after['calls'] == 1 and not after['next'] and not after['up'], f'F3: called: Where next?\'s arrow gone, no pointer ({after})')
            check(after['lab'] and after['lab'] == after['job'], f'F3: after the call the job\'s own arrow is back ({after})')
        errs = g.ev("DEV.errors.filter(e => /pointer/.test(e))")
        check(not errs, f'no pointer errors {errs[:3]}')
        pe = [e for e in g.errors if 'pageerror' in e]
        check(not pe, f'no page errors {pe[:3]}')
        g.close()

run(sys.argv[1] if len(sys.argv) > 1 else 'starship-cadet.html')
print('arrows_f_check: OK' if ok else 'arrows_f_check: FAILED')
sys.exit(0 if ok else 1)
