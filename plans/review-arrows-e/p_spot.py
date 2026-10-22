import sys
src = open('/home/user/Cadet-game/arrows_check.py').read().split("GUIDE = 'guide' in")[0]
BUILD = sys.argv[1]; sys.argv = [sys.argv[0]]
exec(src); GUIDE = True
L = r"""(() => { const g = goalNow(); if (!g) return null; const w = ixGoalWorld(g), z = DECK_CREW.find(a => a.p && a.p.id === g.crew), p = player.obj.position, room = ixGoalWorld({ room: g.room });
  const tw = w && nearestOpen(w.x, w.z, player);
  return [clockText(), g.label, 'arrow at ' + (w ? w.x.toFixed(1) + ',' + w.z.toFixed(1) + ' tile ' + tw + ' room ' + roomAt(...tw) : null), 'room spot ' + (room ? room.x.toFixed(1) + ',' + room.z.toFixed(1) : null),
    'zeke ' + (z ? z.x.toFixed(1) + ',' + z.z.toFixed(1) + ' mesh ' + (z.obj || z.g || z.mesh ? JSON.stringify((z.obj || z.g || z.mesh).position) : '?') : 'none'), 'me ' + p.x.toFixed(1) + ',' + p.z.toFixed(1) + ' tile ' + player.here() + ' room ' + roomAt(...player.here()), 'door ' + occasionDoorOpen(5, 'w')]; })()"""
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
    pg = Page(ctx, BUILD); real_game(pg, 2); f = Follower(pg)
    f.run(1440 + 10 * 60 + 29)
    while pg.ev('shipNow()') < 1440 + 10 * 60 + 52:
        f.run(pg.ev('shipNow()') + 1); print(pg.ev(L))
    print('crew keys', pg.ev("Object.keys(DECK_CREW.find(a => a.p && a.p.id === 'torres-zeke') || {})"))
    print('acts', f.acts[-12:])
