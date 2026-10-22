# RV6: Day 5 from 09:20 with queue and pointer on: every follower action, the activity, the device app, each minute; then
# (mode 'tap') no follower after the arrow reaches the holds: one real tap on the panel and wait it out
import sys
src = open(sys.argv[3]).read().split("GUIDE = 'guide' in")[0]
BUILD, MODE = sys.argv[1], sys.argv[2]; sys.argv = [sys.argv[0]]
exec(src); GUIDE = True
L = r"""(() => { const g = goalNow(), j = myJob(); return [clockText(), g ? g.label : null, deckDef.num + ':' + player.here(), ACT ? ACT.kind + '/' + (ACT.def && ACT.def.title) + '/' + ACT.phase : '-',
  DEV.open ? DEV.app : 'shut', j ? j.id + (j.scan ? ' scan' : '') + (j.picked ? ' picked' : '') + ((SHIP.player.work || {}).seen ? ' seen' : '') : '-', (pointNow() || {}).id || '-', SHIP.works.cur ? SHIP.works.cur.st : null]; })()"""
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('CADET_CHROME') or None, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
    pg = Page(ctx, BUILD); real_game(pg, 5); f = Follower(pg)
    f.run(4 * 1440 + 9 * 60 + 20); last = None; n0 = len(f.acts)
    if MODE == 'tap':
        while pg.ev("(goalNow() || {}).label || ''").startswith('Look over') is False and pg.ev('shipNow()') < 4 * 1440 + 11 * 60: f.run(pg.ev('shipNow()') + 1)
        for _ in range(30):                              # walk to the arrow (the follower's walk only), no taps
            r = pg.ev("(() => { const g = goalNow(); if (!g) return 'none'; if (deckDef.num !== g.deck) { goToDeck(g.deck); return 'lift'; } const w = ixGoalWorld(g), p = player.obj.position; if (Math.hypot(w.x - p.x, w.z - p.z) > 2.2) { player.obj.position.copy(cellPos(...nearestOpen(w.x, w.z, player))); player.stop(); return 'walk'; } return 'there'; })()")
            pg.step(10, 50)
            if r == 'there': break
        it = pg.ev("(() => { const g = goalNow(), w = ixGoalWorld(g); const its = ITEMS.map(i => { i.hit.getWorldPosition(_wp); return [i.t, Math.hypot(_wp.x - w.x, _wp.z - w.z)]; }).sort((a, b) => a[1] - b[1]); return its.slice(0, 3); })()")
        print('near the arrow:', it)
        xy = pg.ev("(() => { const g = goalNow(), w = ixGoalWorld(g); const v = new THREE.Vector3(w.x, .05, w.z).project(camera); return [(v.x + 1) / 2 * innerWidth, (1 - v.y) / 2 * innerHeight]; })()")
        pg.page.mouse.click(*xy); print('real tap at the pin', xy)
        end = pg.ev('shipNow()') + 40
        while pg.ev('shipNow()') < end:
            pg.step(10, 50); s = pg.ev(L)
            if s[1:] != last: print(' | '.join(str(x) for x in s)); last = s[1:]
    else:
        while pg.ev('shipNow()') < 4 * 1440 + 10 * 60 + 30:
            f.run(pg.ev('shipNow()') + 1); s = pg.ev(L)
            if s[1:] != last: print(' | '.join(str(x) for x in s)); last = s[1:]
        print('acts:'); [print('  ', a) for a in f.acts[n0:][:60]]
    print('diag', pg.ev("(() => { const j = myJob(); return { app: DEV.app, open: DEV.open, scanJob: typeof SCAN_UI !== 'undefined' ? SCAN_UI.job : 'no SCAN_UI', jid: j && j.id, scan: j && j.scan, picked: j && j.picked, caseOf: !!(j && caseOf(j)), tipq: typeof TIP_Q !== 'undefined' ? TIP_Q.length : null, tipUp: !!document.querySelector('#tip:not([hidden])'), watchers: POINT_WATCH.map(f => f.name), point: pointNow(), seen: JSON.stringify(SHIP.device && SHIP.device.point || null).slice(0, 200), bars: !!document.querySelector('#devBody .bars'), errs: DEV.errors.slice(-3) }; })()"))
    print('errors', pg.errors[:4])
