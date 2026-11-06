# Starship Cadet: TP1's probe for the 0.99.7 notes 6, 7, 9, 11, 28, 33, 53, 54 (plans/patch-0997.md; TP997_ON).
# Makes its own copy with the switch on (and runs the same steps on the build as given, the switch off, where it says so).
# Phone size 390x844 throughout. Each part prints ok / FAIL; the last line says OK or FAILED.
# Run:  python3 plans/tp1-probes/tp997_probe.py BUILD.html
import sys, json, os, pathlib
G = str(pathlib.Path(__file__).resolve().parents[2]) + '/'
exec(open(G + 'cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
ok = True
def check(cond, msg):
    global ok
    print('ok  ' if cond else 'FAIL', msg)
    if not cond: ok = False
    return cond

TIPS = "(() => { window.__tips = []; const o = tipShow; tipShow = function (id, t) { const r = o.apply(this, arguments); if (r) window.__tips.push([clockText(), id, t]); return r; }; })()"
def new_game(g):
    g.ev('localStorage.clear()'); g.ev('newGameStart(true)'); g.step(5)
    g.page.fill('form input[maxlength="24"]', 'Sam'); g.page.click('form button'); g.step(5)
    g.ev("introFlagSet('intro.device')"); g.step(2)          # the device yours, as at the arrival evening's end (Torres hands it over)
def dialogue_through(g, n=80):
    for i in range(n):
        if not g.ev('!!DIALOGUE'): return
        g.ev('(() => { const l = DIALOGUE.queue[DIALOGUE.i]; if (l && l.choice) dialogueChoose(0); else dialogueNext(); })()'); g.step(10)

def lift_row(g):     # the lift panel on Deck 3: the rec deck's row, its line and whether it fits
    g.ev("goToDeck(3)"); g.step(20); g.ev("closeLiftPanel(); openLiftPanel()"); g.step(2)
    r = g.ev("""(() => { const b = [...document.querySelectorAll('#liftList button')].find(x => /Recreation/.test(x.textContent)); const sm = b && b.querySelector('small');
      return b ? { text: sm.textContent, fits: b.scrollWidth <= b.clientWidth + 1 && sm.scrollWidth <= sm.clientWidth + 1, h: Math.round(b.getBoundingClientRect().height) } : null; })()""")
    g.ev("closeLiftPanel()"); return r

def run_on(path, shots):
    out = {}
    with sync_playwright() as pw:
        g = Game(pw, path, 390, 844); g.step(3)
        # 28: the lift panel
        out['lift'] = lift_row(g)
        g.page.screenshot(path=shots + '_lift.png') if False else None
        g.ev("openLiftPanel()"); g.step(2); g.page.screenshot(path=shots + '_lift.png'); g.ev("closeLiftPanel()")
        # 54: Mark all as read, by real taps
        g.ev("(() => { for (let k = 0; k < 3; k++) mailSend({ at: shipNow(), from: 'Probe', subject: 'Probe ' + k, body: 'x' }); })()"); g.step(2)
        g.ev("deviceShow('mail')"); g.step(3)
        b = g.page.locator('#devBody button', has_text='Mark all as read')
        out['mailBtn'] = b.count(); out['unread0'] = g.ev('mailUnread()')
        g.page.screenshot(path=shots + '_mail.png')
        if b.count(): b.first.click(); g.step(3)
        out['unread1'] = g.ev('mailUnread()'); out['mailBtn1'] = g.page.locator('#devBody button', has_text='Mark all as read').count()
        out['badge'] = g.ev("document.getElementById('devMail').hidden")
        g.ev('deviceClose()'); g.step(2)
        # 7: nearest bathroom from several decks; the real tap on Deck 3
        L = {}
        for d, tile in [(3, None), (4, None), (5, None), (6, None), (7, None), (2, None), (1, None)]:
            g.ev(f"goToDeck({d})"); g.step(20)
            L[d] = g.ev("(() => { const it = trkItems().find(x => x.key === 'place:loo'); return it ? { sub: it.sub, goal: it.goal && [it.goal.deck, it.goal.place] } : null; })()")
        out['loo'] = L
        g.ev("goToDeck(3)"); g.step(20); g.ev("player.obj.position.copy(cellPos(28, 2))"); g.step(5)
        g.page.click('#trkBtn'); g.step(3)
        g.page.screenshot(path=shots + '_tracker.png')
        row = g.page.locator('#trkList button', has_text='Nearest bathroom')
        out['looRow'] = row.count()
        if row.count(): row.first.click(); g.step(5)
        out['looGoal'] = g.ev("IX_GOAL ? { label: IX_GOAL.label, place: IX_GOAL.place, deck: IX_GOAL.deck, trk: IX_GOAL.trk } : null")
        g.page.screenshot(path=shots + '_looarrow.png')
        g.ev("clearGoal()")
        # 53: every tradition's tip and notice, as tradJoin and tradJoinMinute would make them
        out['join'] = g.ev(r"""(() => { const out = []; for (const id of Object.keys(TRAD_JOIN)) { const s = TRAD_JOIN[id]; const ev = SHIP_TRADITIONS.find(x => x.id === id);
            const e = { id, day: 9, ev: ev || {}, name: ev ? ev.name : 'An appointment' }, name = 'Tomas';
            const label = tradWords(e, 'tip', { name }) || (s.act === 'beam' ? 'Tap the beam to paint your name' : 'Tap ' + name + ' to ' + s.verb);
            const tip = label + (s.act === 'beam' ? '' : tp997More(label)), notice = tradWords(e, 'notice', { name }) || tp997Notice(e, s);
            out.push([id, tip, notice]); } return out; })()""")
        out['mail53'] = g.ev("(() => { const e = { name: 'Lap of the Wren' }; return 'Good to see you at ' + (TP997.n53 ? e.name.replace(/^The /, 'the ') : e.name.toLowerCase()) + '.'; })()")
        # 33: buy a snack at the till (the basket and the pay step), Pockets lists it, eat it; the save keeps it
        g.ev("goToDeck(3)"); g.step(20)
        r = g.ev("""(() => { SHIP.player.credits = 50; SHIP.player.needs.hunger = 40; basket = { kind: 'snack', name: 'a honey flapjack', price: 2, gain: 7, gift: null };
          actStart('pay', null, { title: 'Counter', after: 'x' }); if (ACT) ACT.done = ACT.def.mins; return !!ACT; })()"""); g.step(30)
        out['pack'] = g.ev("SHIP.player.pack.slice()"); out['hunger0'] = g.ev("Math.round(SHIP.player.needs.hunger)")
        out['payToast'] = g.ev("document.getElementById('tx').textContent")
        out['save'] = g.ev("(() => { const s = { player: {} }; for (const f of SAVE_EXTRA) try { f(s); } catch (e) {} return s.player.pack || null; })()")
        g.ev("deviceShow('pockets')"); g.step(3)
        g.page.screenshot(path=shots + '_pockets.png')
        eb = g.page.locator('#devBody button', has_text='Eat'); out['eatBtn'] = eb.count()
        if eb.count(): eb.first.click(); g.step(3)
        out['pack1'] = g.ev("SHIP.player.pack.slice()"); out['hunger1'] = g.ev("Math.round(SHIP.player.needs.hunger)")
        out['eatToast'] = g.ev("document.getElementById('tx').textContent")
        g.ev("deviceShow('pockets')"); g.step(2); out['emptyText'] = g.ev("document.getElementById('devBody').textContent")[:160]
        g.ev('deviceClose()'); g.step(2)
        out['errors'] = [e for e in g.errors if e.startswith('pageerror')]
        g.close()
    # 6, 9, 11: tips in a new game
    with sync_playwright() as pw:
        g = Game(pw, path, 390, 844); g.step(3); new_game(g); g.ev(TIPS)
        g.ev("skipTo(introAbs(1, 6 * 60 + 10))")
        for i in range(60):                                # a tip card closes on a real-time timer: close the ones waiting, as a reader would
            g.step(30); g.ev("while (TIP_Q.length && !/^t:tp997/.test(TIP_Q[0].id)) tipDone()")
            if g.ev("!!SHIP.device.tipsSeen['t:tp997-trk']"): break
        out['d1tips'] = g.ev("window.__tips.map(x => x.slice(0, 2))")
        g.ev("skipTo(introAbs(1, 9 * 60 + 20))"); g.step(10); dialogue_through(g)
        g.ev("(() => { const j = SHIP.jobs.find(x => x.reserved === 1); if (j.claimedBy !== 'you') claimJob(j.id); goToDeck(5); })()"); g.step(30)
        g.ev("""(() => { const pl = [...PLACE_OF.values()].find(p => p.room === 'f' && p.type === 'storage'); const s = placeSpot(pl.id); player.obj.position.set(s.x, 0, s.z);
          const P = SHIP.player, j = myJob(); P.work = { job: j.id, fitted: [], done: 0, seen: false, make: { part: j.make, done: 0 } }; actStart('make', pl.id, { title: 'Machine shop', part: j.make, after: 'x' }); if (ACT) ACT.def.mins = 30; window.__mk = clockText(); })()""")
        for i in range(12):
            g.step(30)
            if any(t[1] == 't:devwork' for t in g.ev('window.__tips')): break
        out['makeAt'] = g.ev('window.__mk'); out['devwork'] = [t[:2] for t in g.ev('window.__tips') if t[1] == 't:devwork']
        out['devworkUp'] = g.ev("TIP_Q.length && TIP_Q[0].id")
        g.page.screenshot(path=shots + '_devwork.png')
        g.ev("actEnd(true)"); g.ev("SHIP.intro.done['d1-shadow:job'] = introAbs(1, 11 * 60)")
        g.ev("skipTo(introAbs(2, 19 * 60 + 2))"); g.step(10); dialogue_through(g)
        for i in range(20):
            g.step(60)
            if any(t[1] == 't:tp997-call' for t in g.ev('window.__tips')): break
        out['call'] = [t for t in g.ev('window.__tips') if t[1] == 't:tp997-call']; out['eveSeen'] = g.ev("!!SHIP.device.tipsSeen['t:eve-call']")
        g.page.screenshot(path=shots + '_call.png')
        out['errors2'] = [e for e in g.errors if e.startswith('pageerror')]
        g.close()
    return out

src = pathlib.Path(sys.argv[1]).read_text(); OFF = "var TP997_ON = false || URL_FLAGS.has('tp997');"
if OFF not in src: print('FAIL no TP997_ON switch line (off) in this build'); sys.exit(1)
on = WORK / 'test' / f'_tp997_on_{os.getpid()}.html'; on.parent.mkdir(parents=True, exist_ok=True); on.write_text(src.replace(OFF, OFF.replace('false', 'true'), 1))
shots = os.environ.get('TP_SHOTS', str(WORK / 'test' / 'tp997'))
try:
    A = run_on(str(on), shots)
    for k, v in A.items():
        if k != 'join': print(k, json.dumps(v)[:400])
    check(A['lift'] and 'flight sim' in A['lift']['text'] and A['lift']['fits'] and 'Deck 7' not in A['lift']['text'], f"28: the lift panel's rec deck line names the flight sim and fits at 390 px: {A['lift']}")
    check(A['mailBtn'] == 1 and A['unread0'] >= 3 and A['unread1'] == 0 and A['mailBtn1'] == 0 and A['badge'], f"54: Mark all as read at the top of Mail: {A['unread0']} unread -> {A['unread1']}, button gone after, badge hidden {A['badge']}")
    L = {str(k): v for k, v in A['loo'].items()}
    check(L['3']['goal'][0] == 3 and L['4']['goal'][0] == 4 and L['5']['goal'][0] == 5 and L['2']['goal'] == [2, '2-wctoilet-1'] or L['2']['goal'] == [2, '2-wctoilet-2'], f"7: nearest bathroom on decks with one is on that deck (2's the public washroom, not a cabin's): {L}")
    check(L['6']['goal'][0] == 5 and L['7']['goal'][0] in (4, 5), f"7: from Engineering (no washroom) the nearest deck's (5); from the rec deck 4 or 5: {L['6']}, {L['7']}")
    check(A['looRow'] == 1 and A['looGoal'] and A['looGoal']['trk'] == 'place:loo' and A['looGoal']['deck'] == 3 and str(A['looGoal']['place']).startswith('3-toilet-'), f"7: a real tap on the row sets the arrow to a Deck 3 toilet: {A['looGoal']}")
    bad = [r for r in A['join'] if any(x in (r[1] + ' ' + r[2]) for x in ['undefined', 'null', ': six weeks', ': twelve weeks', 'will do: you join', '?'])]
    check(not bad, f"53: no tip or notice with 'undefined', a doubled colon or the old 'Anyone taking part will do' ({len(A['join'])} traditions): {bad[:4]}")
    two = [r for r in A['join'] if r[2].count(':') > 1]
    check(not two, f"53: no notice with two colons: {two[:4]}")
    check(A['mail53'] == 'Good to see you at Lap of the Wren.', f"53: the thanks Mail keeps the name's capitals: {A['mail53']}")
    check(A['pack'] == ['a honey flapjack'] and A['save'] == ['a honey flapjack'] and A['hunger0'] == 40, f"33: a bought flapjack goes in your pocket, not eaten (hunger {A['hunger0']}), and into the save: {A['pack']} {A['save']} {A['payToast']!r}")
    check(A['eatBtn'] >= 1 and A['pack1'] == [] and A['hunger1'] == 47, f"33: Eat in Pockets: pocket {A['pack1']}, hunger 40 -> {A['hunger1']}: {A['eatToast']!r}")
    check('empty' in A['emptyText'], f"33: an empty Pockets says so: {A['emptyText']!r}")
    check(any(t[1] == 't:tp997-trk' for t in A['d1tips']), f"9: the Schedule tracker tip on Day 1's morning: {A['d1tips']}")
    check(len(A['devwork']) == 1 and A['devworkUp'] == 't:devwork', f"11: the device-at-work tip as the make step starts ({A['makeAt']}): {A['devwork']}, on screen {A['devworkUp']}")
    check(len(A['call']) == 1 and A['eveSeen'], f"6: Day 2's one-call-a-day tip after the booths' evening: {[c[:2] for c in A['call']]}, Day 4's marked seen {A['eveSeen']}")
    check(not A['errors'] and not A['errors2'], f"no page errors: {A['errors']} {A['errors2']}")
finally:
    on.unlink(missing_ok=True)
print('TP997 PROBE OK' if ok else 'TP997 PROBE FAILED')
sys.exit(0 if ok else 1)
