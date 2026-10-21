# PR4: EV2's storm S4 (your help counts). With EVENTS_ON on in a copy, a real save on Day 11 13:30, two runs:
#  none: the storm left alone; all: the three prep jobs (ballasts, batteries, booth rota) marked done by you at 15:00
#  Thursday (before the front), with a save and reload on Saturday 12:00 (the done jobs are tidied off at load: the
#  help must be kept on the event). Both skipped to Sunday 10:05 (the result settled at the all-clear).
# Expect: none = bumpy (EV2: 117 / 6 / 4.8), all = smooth (59 / 3 / 2.9), helped:* kept through the reload.
import os, sys, json, re, pathlib
os.environ.setdefault('CADET_WORK', '/tmp/work-RV4')
exec(open('/home/user/cadet-game/plans/review-4/pp.py').read())
path = sys.argv[1]
save = {'v': 2, 'build': 'x', 'time': {'day': 11, 'min': 810}, 'player': {'deck': 5, 'tile': [20, 4], 'facing': 0}, 'ship': {'decks': {}, 'eventLog': []}, 'crew': {}}
pw = sync_playwright().start()
b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME'), args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
(WORK / 'test').mkdir(parents=True, exist_ok=True)
tmp = WORK / 'test' / '_s4_on.html'; tmp.write_text(instrument(pathlib.Path(path).read_text()))
def run(help):
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, has_touch=True); pg = ctx.new_page(); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
    pg.add_init_script(INIT + "try { if (!sessionStorage.getItem('seeded')) { sessionStorage.setItem('seeded', '1'); localStorage.clear(); localStorage.setItem('starship-cadet-save', " + json.dumps(json.dumps(save)) + "); localStorage.setItem('starship-cadet-arrived', '1'); } } catch (e) {}")
    def load():
        pg.goto('file://' + str(tmp) + '?debug'); pg.wait_for_function('window.__sc !== undefined || window.__err', timeout=90000)
    ev = lambda s: pg.evaluate('s => window.__sc(s)', s)
    step = lambda n: pg.evaluate(f'window.__step({n}, 1000/30)')
    load(); step(20)
    ev("skipTo(10 * 1440 + 14 * 60 + 20)"); step(3)
    jobs = ev("SHIP.jobs.filter(j => j.event === 'ionStorm').map(j => j.eventJob)")
    out = {'jobs': jobs}
    if help:
        ev("skipTo(10 * 1440 + 15 * 60)"); step(3)
        out['marked'] = ev("""(() => { const t = shipNow(), ids = ['stormBallasts', 'stormBatteries', 'stormRota'], got = [];
          for (const j of SHIP.jobs) if (j.event === 'ionStorm' && ids.includes(j.eventJob)) { Object.assign(j, { claimedBy: 'you', status: 'done', doneBy: 'you', doneAt: t }); got.push(j.eventJob); }
          MACH_REV++; return got; })()""")
        step(5)
        out['kept_thu'] = ev("Object.keys(SHIP.event.mine).filter(k => /^helped:/.test(k)).sort()")
        ev("skipTo(12 * 1440 + 12 * 60)"); step(3); ev("saveGame()"); load(); step(30)
        out['after_reload'] = [ev("Object.keys(SHIP.event.mine).filter(k => /^helped:/.test(k)).sort()"), ev("SHIP.jobs.filter(j => j.event === 'ionStorm').length")]
    ev("skipTo(13 * 1440 + 10 * 60 + 5)"); step(3)
    out['threads'] = ev("({ ...SHIP.event.threads })"); out['band'] = ev("SHIP.event.mine.settled || eventBand('ionStorm', SHIP.event.threads)")
    out['help'] = ev("['blackout', 'bridgeHungry', 'calls'].map(t => !!eventHelp(t))")
    out['errs'] = errs[:3]; ctx.close(); return out
A = run(False); print('none', A, flush=True)
B = run(True); print('all ', B, flush=True)
ok = A['band'] == 'bumpy' and B['band'] == 'smooth' and len(B['after_reload'][0]) == 3 and B['help'] == [True] * 3 and A['help'] == [False] * 3 \
     and all(B['threads'][k] < A['threads'][k] for k in ('blackout', 'bridgeHungry', 'calls')) and not A['errs'] and not B['errs']
print('S4', 'OK' if ok else 'CHECK'); b.close(); pw.stop()
