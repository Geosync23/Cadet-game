# RV6: Day 2's Rounds meeting with the queue on (or off): where the player, Zeke and the arrow are each ship minute 10:20-11:20
import sys
src = open('/home/user/Cadet-game/arrows_check.py').read().split("GUIDE = 'guide' in")[0]
BUILD = sys.argv[1]; ON = 'off' not in sys.argv; sys.argv = [sys.argv[0]]
exec(src); GUIDE = ON
L = r"""(() => { const g = goalNow(), c = SHIP.works.cur, r = c && SHIP.occasions.find(x => x.key === c.occ), z = DECK_CREW.find(a => a.p && a.p.id === 'esposito-yara'), h = player.here();
  return [clockText(), g ? g.label : null, c ? c.st : null, r ? r.status + (r.met ? '/met' : '') + ' at ' + r.deck + r.room + ' ' + hhmm(r.at % 1440) : null, deckDef.num + ':' + h.join(',') + ' room ' + roomAt(...h),
    z ? 'zeke ' + Math.round(z.x) + ',' + Math.round(z.z) + ' room ' + roomAt(...nearestOpen(z.x, z.z, player)) : 'zeke not on deck', !!DIALOGUE, g && g.crew ? 'crew-goal' : '', IX_GOAL ? 'IX:' + IX_GOAL.label : '', (myJob() || {}).id || 'no job', String(ixJobGoal && ixJobGoal.label)]; })()"""
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
    pg = Page(ctx, BUILD); real_game(pg, 3); f = Follower(pg)
    f.run(2 * 1440 + 12 * 60 + 10); last = None
    while pg.ev('shipNow()') < 2 * 1440 + 12 * 60 + 50:
        f.run(pg.ev('shipNow()') + 1); s = pg.ev(L)
        if s[1:] != last: print(' | '.join(str(x) for x in s)); last = s[1:]
    print('acts', f.acts[-40:]); print('trained', pg.ev("JSON.stringify(SHIP.works.tr)")); print('errors', pg.errors[:4])
