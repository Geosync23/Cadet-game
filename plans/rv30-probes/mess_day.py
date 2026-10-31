# RV30 probe (note 4, MESS_SCALE): Day 2 in the mess hall at 12 times, the real crew (no forced head count): who is there,
# the voices and level the murmur gets, whether the scene plays and the level gain's value. Usage: mess_day.py WORKTREE [on]
import sys, os
wt = sys.argv[1]; os.chdir(wt)
exec(open('cadet_test.py').read().split('a, shots = run(')[0])
src = pathlib.Path('starship-cadet.html').read_text()
if len(sys.argv) > 2: src = src.replace('const MESS_SCALE = false;', 'const MESS_SCALE = true;', 1)
f = WORK / 'test' / f'_rv30_mess_{os.getpid()}.html'; f.write_text(src)
R3_AT = r"""(([t, deck, room]) => { skipTo(t); goToDeck(deck); const R = DECKS[deck].rooms, k = R[room] ? room : Object.keys(R).find(x => R[x].name === room);
  const tl = ROOM_TILES[k]; if (!tl || !tl.length) return 'no tiles for ' + room; player.obj.position.copy(cellPos(...tl[(tl.length / 2) | 0])); return k; })"""
with sync_playwright() as pw:
    g = Game(pw, str(f))
    g.page.goto('file://' + str(g.tmp) + '?nosave&debug&sound'); g.page.wait_for_function('window.__sc !== undefined', timeout=60000)
    g.step(30); g.page.mouse.click(450, 380); g.step(3)
    g.page.wait_for_function("window.__sc('SND._.state()') === 'running'", timeout=10000)
    print('MESS_SCALE', g.ev('MESS_SCALE'))
    for hm in ['06:40', '07:15', '08:30', '10:00', '12:10', '12:40', '14:30', '17:30', '18:20', '18:50', '20:30', '23:00']:
        h, m = map(int, hm.split(':')); g.ev(f"({R3_AT})([{1440 + h * 60 + m}, 3, 'Mess hall'])"); g.step(60)
        for _ in range(6): g.page.wait_for_timeout(400); g.step(2)
        r = g.ev("(M => [M.n, M.at(M.n).voices, M.at(M.n).level, !!M.scene, M.scene && M.scene.lvg ? Math.round(M.scene.lvg.gain.value * 100) / 100 : null])(SND.r3Mess)")
        print(f'  Day 2 {hm}: people {r[0]:2d}  voices {r[1]:2d}  level {r[2]}  scene {r[3]}  gain {r[4]}')
    print('page errors', [e for e in g.errors if e.startswith('pageerror')][:3]); g.close()
f.unlink(missing_ok=True)
