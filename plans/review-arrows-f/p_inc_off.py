# RV6: Day 8's burst pipe with the queue and pointer on, minute by minute 10:25-11:05: arrow, its spot, Calder, you, the incident
import sys
src = open(sys.argv[3]).read().split("GUIDE = 'guide' in")[0]
BUILD, DAY = sys.argv[1], int(sys.argv[2]); sys.argv = [sys.argv[0]]
exec(src); GUIDE = False
L = r"""(() => { const g = goalNow(), c = SHIP.works.cur, a = DECK_CREW.find(x => x.p && x.p.id === 'calder'), w = g && deckDef.num === g.deck ? ixGoalWorld(g) : null, I = typeof incState === 'function' ? incState() : null;
  let cw = null; try { const p = schedPeople().find(x => x.id === 'calder'); cw = p && whereIs(p, shipNow()); } catch (e) {}
  return [clockText(), g ? g.label : null, g && g.crew ? 'crew' : '', w ? 'spot ' + nearestOpen(w.x, w.z, player) : 'spot -', c ? c.st : null, 'me ' + deckDef.num + ':' + player.here() + ' ' + roomAt(...player.here()),
    a ? 'calder here ' + a.here() + ' ' + roomAt(...a.here()) : 'calder ' + JSON.stringify(cw), I && I.open ? 'inc ' + I.open.kind + ' d' + I.open.deck + ' j ' + (I.open.j || '') : 'no inc', (myJob() || {}).id || '-', !!ACT, !!DIALOGUE]; })()"""
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
    pg = Page(ctx, BUILD); real_game(pg, DAY); f = Follower(pg)
    f.run((DAY - 1) * 1440 + 10 * 60 + 25); last = None
    while pg.ev('shipNow()') < (DAY - 1) * 1440 + 11 * 60 + 5:
        f.run(pg.ev('shipNow()') + 1); s = pg.ev(L)
        if s[1:] != last: print(' | '.join(str(x) for x in s)); last = s[1:]
    print('acts', f.acts[-30:]); print('errors', pg.errors[:4])
