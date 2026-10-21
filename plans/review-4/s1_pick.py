# PR4: S1 pick-held repro: Calder.s briefing at 14:00, pick the battery run, look at the storm jobs at once and as they post (14:12).
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
pg.screenshot(path=str(OUT / 's1p_briefing.png')); picked = None; lines = []
for k in range(80):
    if not ev("!!DIALOGUE"): break
    v = view(); lines.append((v.get('name'), v.get('text'), v.get('choices')))
    l = ev("(() => { const l = DIALOGUE.queue[DIALOGUE.i]; return l && l.choice ? l.choice.map(c => c.job || null) : null; })()")
    if l:
        k2 = next((i for i, j in enumerate(l) if j), 0); picked = l[k2]; pg.screenshot(path=str(OUT / 's1p_briefing_choice.png')); ev(f"dialogueChoose({k2})")
    else: ev("dialogueNext()")
    step(2)
res['A_end'] = ev("clockText()"); print('briefing ends', res['A_end'], 'picked', picked, flush=True)
for l in lines: print('   ', l)

print('after pick', ev("[shipNow() % 1440, MACH_HOUR, SHIP.event.mine['wants:stormBatteries'], SHIP.jobs.filter(j => j.event === 'ionStorm').map(j => [j.eventJob, j.posted % 1440, j.status, j.claimedBy || null]), jobsBoard().filter(j => j.event === 'ionStorm').map(j => j.eventJob)]"), flush=True)
for k in range(40): step(30)
print('later', ev("[shipNow() % 1440, SHIP.jobs.filter(j => j.event === 'ionStorm').map(j => [j.eventJob, j.posted % 1440, j.status, j.claimedBy || null]), jobsBoard().filter(j => j.event === 'ionStorm').map(j => j.eventJob)]"), flush=True)
b.close(); pw.stop()
