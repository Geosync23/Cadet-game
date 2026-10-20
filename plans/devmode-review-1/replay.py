# DR1's replay probe: a steady player like DP1/DJ1's description, in two modes:
#   nosave  : ?nosave&debug (how the plan measured)
#   devsave : a scratch copy with SAVE_KEY/INTRO_KEY '-dev' and no nosave (how Dev mode will run), fresh storage
import sys, os, time, json, hashlib, pathlib, re
os.environ.setdefault('CADET_CHROME','/opt/pw-browsers/chromium')
WORKDIR = os.environ.setdefault('CADET_WORK','/tmp/cadet-work')
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("class Game")[0])
from playwright.sync_api import sync_playwright
GAME, MODE, DAYS = sys.argv[1], sys.argv[2], int(sys.argv[3])
STEP = int(os.environ.get('STEP', 30))
html = pathlib.Path(GAME).read_text()
if MODE == 'devsave':
    html = html.replace("const SAVE_KEY = 'starship-cadet-save'", "const SAVE_KEY = 'starship-cadet-save-dev'").replace("const INTRO_KEY = 'starship-cadet-arrived'", "const INTRO_KEY = 'starship-cadet-arrived-dev'")
html = instrument(html)
tmp = pathlib.Path(WORKDIR) / 'test' / ('_dr1_' + MODE + '.html'); tmp.write_text(html)
REPLAY = r"""(({ days, step, from }) => {
  const out = { days: [] }; TIPS_OFF = true;
  const doJob = id => { if (!claimJob(id)) return false; const j = SHIP.jobs.find(x => x.id === id);
    const cs = SHIP.works && SHIP.works.cases && (SHIP.works.cases.open || []).find(c => c.job === id);
    if (cs && typeof caseCall === 'function') caseCall(cs.id, cs.cause);
    jobStops(j).forEach((s, k) => jobStepDone(id, k)); return turnInJob(id); };
  for (let d = from; d <= days; d++) {
    for (let m = 360; m <= 1320; m += step) {
      const t = (d - 1) * 1440 + m; if (t > shipNow()) skipTo(t);
      try { worksTick(); eventsTick(); socialTick(); worksCareerTick(t); } catch (e) { out.err = String(e); }
      if (typeof DIALOGUE !== 'undefined' && DIALOGUE && typeof dialogueEnd === 'function') dialogueEnd(true);
      if (m === 480) careerClock(t, true);
      if (m === 1020) careerClock(t, true);
      const W = SHIP.works, c = W && W.cur;
      if (c && c.st === 'meet') { const r = SHIP.occasions.find(x => x.key === c.occ); if (r && t >= r.at - step && t < r.at + r.len) r.met = true; }
      if (c && c.st === 'watch') c.w = TRAIN_WATCH;
      if (playerShiftOn(d) && m >= 540 && m < 1020 && !myJob()) {
        const c3 = SHIP.works && SHIP.works.cur;
        if (c3 && c3.st === 'do' && c3.j) doJob(c3.j); else { const x = openJobs('you')[0]; if (x) doJob(x.id); }
      }
    }
    sleepUntil(360);
    const W = SHIP.works, C = SHIP.career;
    out.days.push([d, W ? W.rank : null, W ? Math.round(W.xp) : null, W ? Object.keys(W.tr).join(',') : '', C ? C.ms : null, C ? C.sd : null]);
  }
  const decks = {}; for (const n in SHIP.decks) if (SHIP.decks[n].open.size) decks[n] = { open: [...SHIP.decks[n].open] };
  const save = { time: { day: SHIP.time.day, min: SHIP.time.min }, ship: { decks }, crew: crewState(SHIP.time.day), flags: SHIP.flags, notes: SHIP.notes, player: {} };
  for (const f of SAVE_EXTRA) f(save);
  const gs = save.ship.career ? save.ship.career.gs : null; if (save.ship.career) save.ship.career.gs = 0;
  out.gs = gs; out.size = JSON.stringify(save).length; out.json = JSON.stringify(save); out.clothes = CLOTHES_ON; out.intro = !!(SHIP.intro && SHIP.intro.on);
  out.mail = SHIP.mail.length; out.log = SHIP.eventLog.map(l => l.id + ':' + l.band);
  return out;
})"""
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ['CADET_CHROME'], args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
    page = b.new_page(viewport={'width':390,'height':844})
    errs = []; page.on('pageerror', lambda e: errs.append(str(e)))
    page.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
    page.add_init_script(INIT)
    page.goto('file://' + str(tmp) + ('?nosave&debug' if MODE == 'nosave' else '?debug'))
    page.wait_for_function('window.__sc !== undefined || window.__err', timeout=90000)
    ev = lambda s: page.evaluate('s => window.__sc(s)', s)
    page.evaluate('window.__step(5, 33)')
    # both modes start the same way: New game, Monday 06:00 (skip the arrival)
    print('start', ev("(newGameStart(false), typeof introSkip === 'function' && introSkip(), clockText())"), 'storage keys', ev("Object.keys(localStorage)"))
    t0 = time.time()
    r = ev(f"({REPLAY})({{ days: {DAYS}, step: {STEP}, from: 1 }})")
    dt = time.time() - t0
    fp = hashlib.sha256(r['json'].encode()).hexdigest()[:12]
    print(f"MODE {MODE} days {DAYS} step {STEP}: {dt:.1f}s gs={r['gs']} clothes={r['clothes']} size={r['size']} fp(gs zeroed)={fp} log={r['log']} err={r.get('err')}")
    for row in r['days']: print('  ', row)
    print('storage keys after', ev("Object.keys(localStorage).map(k => k + ':' + localStorage.getItem(k).length)"))
    print('pageerrors', errs[:3])
    pathlib.Path(f'replay_{MODE}_{os.getpid()}.json').write_text(r['json'])
    b.close()
