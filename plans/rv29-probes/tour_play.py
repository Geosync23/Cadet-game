# RV29: JB2 note 14 in the real game: Dev jump to Day 2 08:40 in the Works bay, Zeke's rounds talk, take the tour at the
# board, walk to each stop, look, press the button; save and reload after stop 2 (TOUR_RELOAD=0 to skip); then turn in.
# usage: python3 tour_play.py WORKTREE BUILD.html [OUT_DIR]   (env CADET_WORK, CADET_CHROME)
import sys, os, json, pathlib
WT, BUILD = sys.argv[1], sys.argv[2]; OUT = pathlib.Path(sys.argv[3] if len(sys.argv) > 3 else '.')
sys.argv = [sys.argv[0], BUILD]
src = open(WT + '/devmode_check.py').read().split("\ndef part_off")[0].replace("__file__.replace('devmode_check.py', 'cadet_test.py')", repr(WT + '/cadet_test.py'))
exec(src)
S = """(() => { const c = SHIP.works && SHIP.works.cur, j = c && SHIP.jobs.find(x => x.id === c.j), v = typeof dialogueView === 'function' && DIALOGUE ? dialogueView() : null;
  return { t: hhmm(SHIP.time.min), day: SHIP.time.day, deck: deckDef.num, cur: c ? [c.id, c.st, c.by] : null,
    job: j ? { id: j.id, title: j.title, route: j.route, marks: j.marks, by: j.claimedBy, done: j.stepsDone, wd: !!j.workDone, st: j.status } : null,
    step: typeof roundTrainStep === 'function' ? roundTrainStep() : null, goal: IX_GOAL ? IX_GOAL.label : null,
    tips: TIP_Q.map(t => t.text), dlg: v ? (v.name || '') + ': ' + (v.text || '') + (v.choices ? ' [' + v.choices.map(x => x.text || x).join(' / ') + ']' : '') : null,
    choose: (() => { const d = document.getElementById('devDlg'); return d && !d.hidden ? d.innerText.replace(/\\s+/g, ' ').slice(0, 400) : null; })(), said: (window.__said || []).splice(0),
    bubbles: typeof BUBBLES !== 'undefined' ? [...(BUBBLES.values ? BUBBLES.values() : [])].map(b => b.text).slice(0, 4) : null }; })()"""
HOOK = """(() => { if (window.__hooked) return; window.__hooked = 1; window.__said = []; const ws = worksSay, ts = toast;
  worksSay = (id, t) => { window.__said.push('SAY ' + id + ': ' + t); return ws(id, t); }; toast = (a, b, ...r) => { window.__said.push('TOAST ' + a + ': ' + b); return ts(a, b, ...r); }; })()"""
def show(pg, tag=''):
    s = pg.ev(S); print(tag, json.dumps(s)[:1500]); return s
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get('CADET_CHROME'), args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
    pg = Page(ctx, '#dev'); pg.sign(); pg.step(20)
    print('jump', pg.ev("devmodeRun('Jump', () => devmodeSetCareerTo(2, { id: 'rv29', label: 'Day 2 tour', day: 2, by: 1, at: 515, where: { deck: 5, room: 'w' } }))")); pg.step(10)
    pg.ev("(() => { SHIP.device.settings.tips = true; })()"); pg.ev(HOOK)
    said = []
    for i in range(240):                       # the talk: wait for it, read every card at ~2 s
        pg.step(30); s = pg.ev(S)
        if s['dlg']:
            said.append(s['dlg']); pg.ev("(() => { const v = dialogueView(); if (v && v.choices) dialogueChoose(1); else dialogueNext(); })()")
        if s['cur'] and s['cur'][1] == 'do' and s['job'] and not s['dlg']: break
    print('TALK'); [print('  ', x[:220]) for x in said]
    s = show(pg, 'after talk')
    pg.shot(str(OUT / 'tour_0_board.png'))
    # take it from the board, as the device's button does
    pg.ev("device.open && device.open('jobs')"); pg.step(10); print('BOARD UI', pg.ev("(() => { const d = document.getElementById('device') || document.body; return d.innerText.replace(/\\s+/g, ' ').slice(0, 700); })()")); pg.ev("device.close && device.close()"); pg.step(5)
    jid = s['job']['id']; print('openJobs top', json.dumps(pg.ev("openJobs('you').slice(0, 3).map(o => [o.title, o.mins, o.deck, o.room])")))
    print('clock', pg.ev("careerClock(shipNow(), true)")); pg.step(5)
    print('claim', pg.ev(f"claimJob({json.dumps(jid)})")); pg.step(10); show(pg, 'taken')
    k = 0; reloaded = False
    while k < 8:
        st = pg.ev(f"(() => {{ const j = SHIP.jobs.find(x => x.id === {json.dumps(jid)}), S = jobStops(j), k = S.findIndex(s => !s.done); return k < 0 ? null : {{ k, deck: S[k].deck, pid: S[k].places[0], opts: S[k].opts }}; }})()")
        if not st: break
        pg.ev(f"devmodeMove({st['deck']}, () => placeSpot({json.dumps(st['pid'])}).walk ? cellPos(...placeSpot({json.dumps(st['pid'])}).walk) : placeSpot({json.dumps(st['pid'])}), () => true)"); pg.step(20)
        show(pg, f'at stop {st["k"]} (before walk)')
        pg.ev(f"playerGo(placeSpot({json.dumps(st['pid'])}).walk)")
        for w in range(40):
            pg.step(15)
            if pg.ev(f"(() => {{ const s = placeSpot({json.dumps(st['pid'])}), p = player.obj.position; return Math.hypot(s.x - p.x, s.z - p.z) < 1.6; }})()"): break
        s = show(pg, f'arrived {st["k"]}')
        r = pg.ev(f"(() => {{ const j = SHIP.jobs.find(x => x.id === {json.dumps(jid)}); return workStep(j, jobStops(j)[{st['k']}], {st['k']}); }})()")
        for w in range(40):
            pg.step(15); s = pg.ev(S)
            if s['choose']: break
        print('  CARD', json.dumps(s['choose']), '| goal', s['goal'], '| tips', s['tips'][:2])
        pg.shot(str(OUT / f'tour_{st["k"] + 1}_card.png'))
        pg.ev("devChosen(0)"); pg.step(30); s = show(pg, f'  marked {st["k"]}')
        k += 1
        if k == 2 and not reloaded and os.environ.get('TOUR_RELOAD', '1') == '1':
            reloaded = True; print('save', pg.ev("(() => { saveGame(); return true; })()")); pg.reload(); pg.ev(HOOK); pg.step(30); show(pg, 'RELOADED')
    show(pg, 'all stops')
    print('board after', json.dumps(pg.ev("openJobs('you').slice(0, 5).map(o => [o.title, o.mins])")))
    pg.step(200); show(pg, 'later'); print('turnin', pg.ev(f"turnInJob({json.dumps(jid)})")); pg.step(60); show(pg, 'turned in')
    print('errors', pg.errors[:5]); b.close()
