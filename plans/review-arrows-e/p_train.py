# RV6 probe: arrows piece E with the queue on: play Day 2 (Rounds) and Day 3 (Hauling) following the arrow, logging each
# change of the arrow, the queue's entries, the training stage and any direct goal. Run: p_train.py BUILD.html DAY [notrack]
import sys
src = open('/home/user/Cadet-game/arrows_check.py').read().split("GUIDE = 'guide' in")[0]
BUILD, DAY = sys.argv[1], int(sys.argv[2]); NOTRACK = 'notrack' in sys.argv; sys.argv = [sys.argv[0]]
exec(src); GUIDE = True
LOG = r"""(() => { const g = goalNow(), W = SHIP.works, c = W && W.cur;
  return [clockText(), g ? g.label : null, GUIDE.shown, GUIDE.covered, c ? c.id + ':' + c.st : null, IX_GOAL ? IX_GOAL.label : null,
    guideList().map(e => e.id + '/L' + e.level + (e.shown ? '*' : '') + (e.covered ? '(covered)' : '')).join(' '), SHIP.player.track === null ? 'off' : (SHIP.player.track || '-'),
    deckDef.num, player.here().join(',')]; })()"""
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
    pg = Page(ctx, BUILD); real_game(pg, DAY)
    if NOTRACK: pg.ev("SHIP.player.track = undefined")
    f = Follower(pg); last = None; labels = set()
    end = (DAY - 1) * 1440 + 17 * 60 + 30
    while pg.ev('shipNow()') < end:
        f.run(pg.ev('shipNow()') + 2)
        s = pg.ev(LOG); key = tuple(s[1:8])
        if s[1]: labels.add(s[1])
        if key != last: print(' | '.join(str(x) for x in s)); last = key
    print('labels seen:', sorted(labels))
    print('trained:', pg.ev("JSON.stringify(SHIP.works.tr)"))
    print('errors:', pg.errors[:5])
