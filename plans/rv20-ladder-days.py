# RV20: which big lesson opens on which day, Day 14-26, with Step 5 on (paper; ladderTick at 06:00, each lesson trained the same day)
import sys, os, re, pathlib, json
GAME = sys.argv[1]
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'])
    page = b.new_context(viewport={'width': 390, 'height': 844}).new_page(); errs = []
    page.on('pageerror', lambda e: errs.append(str(e)))
    page.route(re.compile(r'.*three\.min\.js'), lambda r: r.fulfill(body=THREE, content_type='application/javascript'))
    tmp = pathlib.Path('/tmp/rv20/srv-ladder.html'); tmp.write_text(instrument(pathlib.Path(GAME).read_text()))
    page.add_init_script(INIT); page.goto('file://' + str(tmp) + '?p5s5&nosave')
    page.wait_for_function('window.__sc !== undefined', timeout=120000)
    ev = lambda s: page.evaluate('s => window.__sc(s)', s)
    out = ev("""(() => {
      const log = [];
      SHIP.jobs = []; SHIP.occasions.length = 0; setShipNow(13 * 1440 + 300); SHIP.works = null; const W = worksInit(shipNow());
      W.tier = 2; W.rank = 'officer'; W.xp = 999;
      for (const r of CAREER_LADDER) if (r.day <= 13 && r.tier <= 2 && r.id !== 't2') { W.tr[r.id] = 13; W.use[r.id] = 9; (W.op[13] = W.op[13] || []).push(r.id); }
      W.tr.t2 = 10; W.tier = 3; W.rank = 'senior'; W.tr.ps = 13; W.tr.t3 = 16; W.op[13].push('t2', 'ps', 't3');
      W.cur = null;
      for (let d = 14; d <= 30; d++) {
        const ids = [];
        for (let h = 6; h <= 15; h++) { const o = ladderTick((d - 1) * 24 + h); ids.push(...o); }
        const c = W.cur; const rec = [d, dayName ? dayName(d) : '', ids.join(','), c ? c.id + '@' + (SHIP.occasions.find(x => x.key === c.occ) || {}).at % 1440 : '-'];
        if (c) { W.tr[c.id] = d; W.cur = null; }
        for (const id of ids) if (W.tr[id] === undefined) W.tr[id] = d;
        log.push(rec);
      }
      return log; })()""")
    for r in out: print(r)
    print('errors', errs[:3])
    b.close()
