# Days 2-4 carried with arrows_check's follower (queue on), then Day 5 08:00-18:00 logged on each change: arrow, training,
# your job, its case (wait, calls, clues), the staged first case. AC2, for p3. Run: python3 plans/arrows-tools/p_week_day5.py BUILD.html
import sys
sys.argv = ['arrows_check.py', sys.argv[1], 'none', 'guide']
src = open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..', '..', 'arrows_check.py')).read()
src = src.split("GUIDE = 'guide' in sys.argv[2:]")[0]
exec(src)
GUIDE = True
from playwright.sync_api import sync_playwright
DAY = int(sys.argv_day) if False else 9
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME'), args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 390, 'height': 844})
    pg = Page(ctx, sys.argv[1]); real_game(pg, 2); f = Follower(pg)
    for d in (2, 3, 4):
        f.run((d - 1) * 1440 + 21 * 60 + 30); f.night(d)
    last = None
    for k in range(0, 600, 3):
        n = len(f.acts); f.run(4 * 1440 + 8 * 60 + k)
        s = pg.ev("""(() => { GUIDE.key=''; const g = goalNow(), j = myJob(), c = j && caseOf(j), C = caseState(), W = SHIP.works;
          return [clockText(), g && g.label, W.cur && W.cur.id + ':' + W.cur.st, j && j.id + (j.scan ? ' scanned' : '') + (j.train ? ' train:' + j.train : ''), c ? JSON.stringify({ wait: c.wait, calls: c.calls.length, got: c.got.length, clues: c.clues.length, told: c.told, m7: c.m7 }) : null,
            C.first || null, (C.open || []).filter(x => x.train).map(x => x.job + ':' + (SHIP.jobs.find(y => y.id === x.job) || {}).claimedBy).join(','), DEV.open ? DEV.app + '/' + WORKS_TAB : '-', JSON.stringify(W.tr)]; })()""")
        if s[1:7] != last: print(s, [a[1][:60] for a in f.acts[n:]][-3:], flush=True); last = s[1:7]
