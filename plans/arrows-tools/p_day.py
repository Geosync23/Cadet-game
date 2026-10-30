# Day 5 with the arrows_check follower: log the arrow, the activity and the Scanner. p_day5.py BUILD [guide]
import sys, os
BUILD = sys.argv[1]; G = "guide" in sys.argv; DAY = int(sys.argv[2]); sys.argv = [sys.argv[0], BUILD]
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'arrows_check.py')).read().split("GUIDE = 'guide' in")[0]
exec(src); GUIDE = G
LOG = r"""(() => { const g = goalNow(), W = SHIP.works, c = W && W.cur, j = typeof myJob === 'function' && myJob();
  return [clockText(), g ? g.label : null, c ? c.id + ':' + c.st : null, j ? j.id + (j.scan ? ' scanned' : '') + (j.picked ? ' picked ' + j.picked : '') : '-', ACT ? ACT.kind + '/' + (ACT.def && ACT.def.title || '') + '/' + ACT.phase : '-',
    DEV.open ? 'dev:' + DEV.app : '-', deckDef.num, player.here().join(','), typeof pointNow === 'function' ? pointNow() || '-' : '-']; })()"""
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
    pg = Page(ctx, BUILD); real_game(pg, DAY)
    f = Follower(pg); last = None; end = (DAY - 1) * 1440 + 17 * 60 + 10
    while pg.ev('shipNow()') < end:
        n = len(f.acts); f.run(pg.ev('shipNow()') + 2)
        s = pg.ev(LOG); key = tuple(s[1:6]) + (s[8],)
        if key != last: print(' | '.join(str(x) for x in s)); last = key
        for a in f.acts[n:]:
            if 'scan' in str(a).lower() or 'look' in str(a).lower() or 'pointer' in str(a).lower() or 'tap' in str(a)[:40]: print('    act', a)
    print('trained:', pg.ev("JSON.stringify(SHIP.works.tr)")); print('errors:', pg.errors[:5])
