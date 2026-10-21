# PR4: EV3's storm S1 (the new hours). With EVENTS_ON on in a copy, a real save on Day 11 13:30:
#  A. the briefing's notice at 13:45, Calder's briefing at 14:00 in the Works bay, a job picked there, the storm jobs up
#     at 14:12 with your pick held;
#  B. Day 14: the result settled at 10:00 (threads stop), the all-clear with the Captain's line to you, your commendation
#     at 10:12 (one storm job + the all-clear), a save mid-way reloaded: the commendation comes once;
#  C. Calder's debrief Mail on Monday 18:00, once; the event ends at Monday midnight, nothing sent twice.
# Phone shots at 390x844 in plans/review-4/shots/. Run: python3 s1_hours.py ON.html
import os, sys, json, re, pathlib
os.environ.setdefault('CADET_WORK', '/tmp/work-RV4')
exec(open('/home/user/cadet-game/plans/review-4/pp.py').read())
path = sys.argv[1]; OUT = pathlib.Path('/home/user/cadet-game/plans/review-4/shots'); OUT.mkdir(exist_ok=True)
save = {'v': 2, 'build': 'x', 'time': {'day': 11, 'min': 810}, 'player': {'deck': 5, 'tile': [20, 4], 'facing': 0}, 'ship': {'decks': {}, 'eventLog': []}, 'crew': {}}
pw = sync_playwright().start()
b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME'), args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
ctx = b.new_context(viewport={'width': 390, 'height': 844}, has_touch=True); pg = ctx.new_page(); errs = []
pg.on('pageerror', lambda e: errs.append(str(e)))
pg.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
pg.add_init_script(INIT + "try { if (!sessionStorage.getItem('seeded')) { sessionStorage.setItem('seeded', '1'); localStorage.clear(); localStorage.setItem('starship-cadet-save', " + json.dumps(json.dumps(save)) + "); localStorage.setItem('starship-cadet-arrived', '1'); } } catch (e) {}")
(WORK / 'test').mkdir(parents=True, exist_ok=True)
tmp = WORK / 'test' / '_s1_on.html'; tmp.write_text(instrument(pathlib.Path(path).read_text()))
def load():
    pg.goto('file://' + str(tmp) + '?debug'); pg.wait_for_function('window.__sc !== undefined || window.__err', timeout=90000)
    pg.add_style_tag(content='.bub{animation:none!important}')
ev = lambda s: pg.evaluate('s => window.__sc(s)', s)
step = lambda n: pg.evaluate(f'window.__step({n}, 1000/30)')
GO = """(id => { const m = MEETINGS.find(x => x.id === id); if (!m) return 'no meeting'; const d = m.where.deck; if (deckDef.num !== d) goToDeck(d);
  const key = evRoomKey(d, m.where.room), pl = DECKS[d].places.find(p => p.room === key) || DECKS[d].places.find(p => p.type === 'jobboard');
  const c = pl.at, P = cellPos(...c), o = nearestOpen(P.x, P.z, player) || c; player.obj.position.copy(cellPos(...o)); player.path.length = 0; target.copy(player.obj.position).setY(.7); return [d, key, m.at % 1440]; })"""
ST = "(() => ({ t: clockText(), dlg: DIALOGUE && DIALOGUE.id, i: DIALOGUE && DIALOGUE.i, ev: SHIP.event && SHIP.event.id, mine: SHIP.event && SHIP.event.mine, th: SHIP.event && SHIP.event.threads }))()"
MAIL = "SHIP.mail.map(m => [Math.floor(m.at / 1440) + 1, m.at % 1440, m.from, m.subject])"
def go(id):
    return ev(GO + "('" + id + "')")
def wait_dialogue(n=400):
    for k in range(n):
        step(15)
        if ev("!!DIALOGUE"): return True
    return False
def view(): return ev("DIALOGUE && dialogueView()")
res = {}
load(); step(20); print('loaded', ev("clockText()"), ev("EV_STORM_ON"), flush=True)
# ---- A
ev("skipTo(10 * 1440 + 13 * 60 + 40)"); step(5)
print('meeting at', ev("(() => { const m = MEETINGS.find(x => x.id === 'stormBriefing'); return [m.at % 1440, m.len, m.notify]; })()"), flush=True)
go('stormBriefing')
told = None
for k in range(600):
    step(10)
    if ev("!!(SHIP.event && SHIP.event.mine['told:stormBriefing'])") and told is None: told = ev("clockText()")
    if ev("!!DIALOGUE"): break
res['A_told'] = told; res['A_start'] = ev("clockText()"); print('notice at', told, 'briefing opens', res['A_start'], ev("DIALOGUE && DIALOGUE.id"), flush=True)
pg.screenshot(path=str(OUT / 's1_briefing.png')); picked = None; lines = []
for k in range(80):
    if not ev("!!DIALOGUE"): break
    v = view(); lines.append((v.get('name'), v.get('text'), v.get('choices')))
    l = ev("(() => { const l = DIALOGUE.queue[DIALOGUE.i]; return l && l.choice ? l.choice.map(c => c.job || null) : null; })()")
    if l:
        k2 = next((i for i, j in enumerate(l) if j), 0); picked = l[k2]; pg.screenshot(path=str(OUT / 's1_briefing_choice.png')); ev(f"dialogueChoose({k2})")
    else: ev("dialogueNext()")
    step(2)
res['A_end'] = ev("clockText()"); print('briefing ends', res['A_end'], 'picked', picked, flush=True)
for l in lines: print('   ', l)
ev("skipTo(10 * 1440 + 14 * 60 + 14)"); step(5)
jobs = ev("SHIP.jobs.filter(j => j.event === 'ionStorm').map(j => [j.eventJob, j.posted % 1440, j.status, j.claimedBy || null])")
print('storm jobs', jobs, flush=True); res['A_jobs'] = jobs
res['A_ok'] = told == '13:45' and res['A_start'] >= '14:00' and all(j[1] == 852 for j in jobs) and len(jobs) > 0 and (picked is None or any(j[0] == picked and j[3] == 'you' for j in jobs))
# 17:00-18:30 Thursday: nothing from the storm (no meeting/moment/mail stamped there)
ev("skipTo(10 * 1440 + 18 * 60 + 40)"); step(3)
q = ev("SHIP.mail.filter(m => m.at >= 10*1440+1020 && m.at < 10*1440+1110).map(m => [m.at % 1440, m.from, m.subject])")
print('Thu 17:00-18:30 mail', q, flush=True)
# ---- B
ev("skipTo(13 * 1440 + 9 * 60 + 50)"); step(5)
ev("(() => { const e = SHIP.event; e.mine.jobs = 1; })()")   # one storm job done (the job path itself is S4's)
th0 = ev("({ ...SHIP.event.threads })"); print('Sun 09:50', ev(ST)['mine'].get('settled'), th0, flush=True)
go('allClear')
if not wait_dialogue(): print('no all-clear dialogue', ev(ST))
st = ev(ST); res['B_settled'] = st['mine'].get('settled'); print('all-clear opens', st['t'], 'settled', st['mine'].get('settled'), st['th'], flush=True)
capt = None
for k in range(80):
    if not ev("!!DIALOGUE"): break
    v = view()
    if v.get('id') == 'marrow' and v.get('text') and ('commendation' in v['text'] or 'share' in v['text'] or 'queue' in v['text']) and capt is None:
        capt = v; pg.screenshot(path=str(OUT / 's1_allclear_you.png'))
    print('   ', v.get('name'), '|', v.get('to'), '|', v.get('text'), v.get('choices'))
    if v.get('choices'): ev("dialogueChoose(0)")
    else: ev("dialogueNext()")
    step(2)
res['B_capt'] = capt and capt['text']; res['B_end'] = ev("clockText()"); print('all-clear ends', res['B_end'], flush=True)
# save before 10:12 (if still before), reload, run to 10:14: one commendation
tnow = ev("shipNow() % 1440"); print('now', tnow, flush=True)
if tnow < 612:
    ev("saveGame()"); load(); step(30)
    print('reloaded', ev(ST)['t'], ev(ST)['mine'].get('settled'), flush=True)
ev("skipTo(13 * 1440 + 10 * 60 + 14)"); step(5)
c1 = ev("[SHIP.commendations.length, SHIP.mail.filter(m => /Commendation/.test(m.subject)).map(m => [m.at % 1440, m.subject, m.body])]")
print('commendation', c1, flush=True)
ev("saveGame()"); load(); step(30); ev("skipTo(13 * 1440 + 22 * 60)"); step(3)
c2 = ev("[SHIP.commendations.length, SHIP.mail.filter(m => /Commendation/.test(m.subject)).length]")
th1 = ev("({ ...SHIP.event.threads })"); print('Sun 22:00 commendations', c2, 'threads', th1, flush=True)
res['B_ok'] = bool(res['B_settled']) and c1[0] == 1 and len(c1[1]) == 1 and c1[1][0][0] == 612 and c2 == [1, 1]
res['B_threads_frozen'] = th1 == ev("SHIP.event.threads") and all(th1.get(k) == v for k, v in st['th'].items())
# ---- C
ev("skipTo(14 * 1440 + 18 * 60 + 5)"); step(5)
d1 = ev("SHIP.mail.filter(m => /how it went/.test(m.subject)).map(m => [Math.floor(m.at/1440)+1, m.at % 1440, m.from, m.body])")
print('debrief', d1, flush=True)
pg.screenshot(path=str(OUT / 's1_mon_1805.png'))
ev("skipTo(15 * 1440 + 60)"); step(5)
d2 = ev("[SHIP.event && SHIP.event.id, SHIP.eventLog.map(l => [l.id, l.startDay, l.endDay, l.band]), SHIP.mail.filter(m => /how it went/.test(m.subject)).length, SHIP.commendations.length]")
print('Tue 01:00', d2, flush=True)
res['C_ok'] = len(d1) == 1 and d1[0][:2] == [15, 1080] and d2[0] is None and d2[2] == 1 and d2[3] == 1
# the Mail app, opened, for a shot of the commendation and debrief
ev("typeof deviceOpen === 'function' && deviceOpen('mail')"); step(10); pg.screenshot(path=str(OUT / 's1_mail.png'))
print('mail', ev(MAIL)[:12])
print('RESULT', res); print('errors', errs[:5])
print('S1', 'OK' if res['A_ok'] and res['B_ok'] and res['C_ok'] and not errs else 'CHECK')
b.close(); pw.stop()
