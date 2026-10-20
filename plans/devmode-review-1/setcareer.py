# DR1: a crude "Set career" as v3 describes, to see what breaks. MODE: 'op' (op filled) or 'noop' (only tr)
import sys, os, time, json, pathlib, re
os.environ.setdefault('CADET_CHROME','/opt/pw-browsers/chromium')
WORKDIR = os.environ.setdefault('CADET_WORK','/tmp/cadet-work')
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("class Game")[0])
from playwright.sync_api import sync_playwright
GAME, MODE, N = sys.argv[1], sys.argv[2], int(sys.argv[3])
html = pathlib.Path(GAME).read_text().replace("const SAVE_KEY = 'starship-cadet-save'", "const SAVE_KEY = 'starship-cadet-save-dev'").replace("const INTRO_KEY = 'starship-cadet-arrived'", "const INTRO_KEY = 'starship-cadet-arrived-dev'")
tmp = pathlib.Path(WORKDIR) / 'test' / '_dr1_setcareer.html'; tmp.write_text(instrument(html))
SET = r"""(({ N, mode }) => {
  window.__ngs = []; const _ng = newGameStart; newGameStart = a => { window.__ngs.push(new Error().stack.split('\n').slice(1,6).join(' | ') + ' @' + clockText()); return _ng(a); };
  const errs = [], mail0 = SHIP.mail.length, t0 = shipNow();
  const I = SHIP.intro;
  // mark the arrival steps and the first week's beats done (as v3 says)
  for (const s of INTRO_STEPS) if (I.done[s.id] === undefined) I.done[s.id] = t0;
  for (const b of INTRO_WEEK) { if (b.meeting) I.done[b.id + ':met'] = t0; if (I.done[b.id] === undefined) I.done[b.id] = t0; }
  const setCareer = d => {
    if (!SHIP.works && d >= 2) worksInit((d - 1) * 1440 + 360);
    const W = SHIP.works; if (!W) return;
    for (const r of CAREER_LADDER) if (r.day < d && (r.tier === 1 || d > 10) && W.tr[r.id] === undefined) {
      W.tr[r.id] = r.day; W.use[r.id] = W.use[r.id] || 1; if (r.tool && !W.tools[r.tool]) W.tools[r.tool] = [r.day, 0];
      if (mode === 'op') (W.op[r.day] = W.op[r.day] || []).push(r.id);
    }
    if (d >= 10 && W.tier === 1) { W.test = { tier: 2, day: 9, tries: 1, passed: true }; W.tier = 2; W.rank = 'officer'; W.xp = 0; W.home = PROMO.home; W.done.push('summons2', 'ceremony2', 'move2'); W.ms.push(['officer', 10]); }
  };
  const C = careerInit();
  for (let d = 1; d <= N; d++) {
    if (careerRota(d) && !C.b.includes(d)) C.b.push(d);   // stands in for the Dev "excused" list (careerOff reads c.b)
    for (let m = (d === 1 ? 0 : 360); m <= 1440 + 360; m += 30) { const t = (d - 1) * 1440 + m; if (t > shipNow()) try { skipTo(t); } catch (e) { errs.push(String(e).slice(0, 120)); } if (m >= 1440) break; }
    setCareer(d + 1);
  }
  C.b = [];                                              // excusing stops: play Day N+1 as a player who doesn't turn up
  const W = SHIP.works, now = shipNow(), d0 = SHIP.time.day;
  const before = { clock: clockText(), rank: W && W.rank, tier: W && W.tier, tr: W ? Object.keys(W.tr).length : 0, cur: W && W.cur, ms: C.ms, missed: SHIP.intro.missed };
  // the next workday, from 06:00 to 18:00, with the frame ticks
  const opened = [];
  for (let m = 360; m <= 1080; m += 10) { const t = (d0 - 1) * 1440 + m; if (t > shipNow()) skipTo(t); try { worksTick(); eventsTick(); socialTick(); worksCareerTick(t); introTick && introTick(); } catch (e) { errs.push(String(e).slice(0, 120)); }
    const c = SHIP.works && SHIP.works.cur; if (c && !opened.includes(c.id + ':' + c.st)) opened.push(c.id + ':' + c.st); }
  // save and read back (worksClean keeps it?)
  saveGame(); const s = JSON.parse(localStorage.getItem(SAVE_KEY)), back = worksClean(JSON.parse(JSON.stringify(s.ship.works)));
  return { before, after: { clock: clockText(), cur: SHIP.works.cur, opToday: SHIP.works.op[d0] || [], opened, ms: C.ms },
    mail: SHIP.mail.slice(mail0).map(m => (m.from || '') + ': ' + (m.subject || '')), settle: SHIP.intro.settle, step: SHIP.intro.step, flags: INTRO_FLAGS.map(f => f + '=' + flag(f)), escortToday: (() => { try { return JSON.stringify(escortPlanOf ? null : null); } catch (e) { return null; } })(), notesMissed: SHIP.notes.filter(n => /miss/i.test(n.kind)).map(n => n.kind + '@' + Math.floor(n.t/1440+1)), introOn: !!SHIP.intro.on, ended: SHIP.intro.ended, week1: flag('week1.done'),
    saved: { rank: back.rank, tier: back.tier, home: back.home, tr: Object.keys(back.tr).length, done: back.done }, errs: errs.slice(0, 5), ngs: window.__ngs, playerBed: playerBed() };
})"""
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ['CADET_CHROME'], args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
    page = b.new_page(viewport={'width':390,'height':844}); errs = []
    page.on('pageerror', lambda e: errs.append(str(e)[:200])); page.on('console', lambda m: m.type == 'error' and errs.append(m.text[:200]))
    page.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
    page.add_init_script(INIT); page.goto('file://' + str(tmp) + '?debug')
    page.wait_for_function('window.__sc !== undefined || window.__err', timeout=90000)
    ev = lambda s: page.evaluate('s => window.__sc(s)', s)
    page.evaluate('window.__step(5, 33)')
    print('start', ev("(INTRO_BOOT = false, newGameStart(true), TIPS_OFF = true, clockText() + ' intro ' + !!(SHIP.intro && SHIP.intro.on) + ' clothes ' + CLOTHES_ON)"))
    t = time.time(); r = ev(f"({SET})({{ N: {N}, mode: '{MODE}' }})")
    print(MODE, N, round(time.time() - t, 1), 's'); print(json.dumps(r, indent=1)[:4000]); print('pageerrors', errs[:5]); b.close()
