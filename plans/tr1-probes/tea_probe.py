# TR1 probe, note 10: the 13:00 tea and biscuits in the Deck 5 tea corner (room 't'). Usage: tea_probe.py BUILD.html [day]
# You stand in the tea corner from 12:55; each ship minute or so: who is there for tea, where (place, tile, settled, pose),
# how many crew stand inside the room, and whether you can walk out (findPath from your tile to the Works bay).
import sys, json
sys.argv, ARGS = sys.argv[:1], sys.argv[1:]
exec(open("/home/user/cadet-game/cadet_test.py").read().split("a, shots = run(")[0].replace("timeout=60000", "timeout=240000"))
build = ARGS[0]; d = int(ARGS[1]) if len(ARGS) > 1 else 3
LOOK = """JSON.stringify((() => { const tl = ROOM_TILES['t'] || [], set = new Set(tl.map(t => t.join(',')));
  const inRoom = DECK_CREW.filter(a => set.has(cellAt(a.x, a.z).join(',')));
  const tea = DECK_CREW.filter(a => /tea/.test(a.tag || '') || (a.spot && /^5-tea-/.test(a.spot.id)) || (a.goalId && /^5-tea-/.test(a.goalId)));
  const me = player.here(), out = [20, 1];
  let path = null; try { path = findPath(me, out); } catch (x) { path = 'err ' + x; }
  return { m: Math.round(SHIP.time.min), room: tl, me, inRoom: inRoom.map(a => a.p.id + '@' + cellAt(a.x, a.z).join(',') + ':' + (a.pose || '') + (a.settled ? '' : '~')),
    tea: tea.map(a => [a.p.id, a.tag, a.spot && a.spot.id, a.goalId || null, a.settled, a.pose, cellAt(a.x, a.z).join(',')]),
    path: Array.isArray(path) ? path.length : path }; })())"""
with sync_playwright() as pw:
    g = Game(pw, build, 900, 760)
    g.ev("(() => { skipTo(%d * 1440 + 12 * 60 + 52); goToDeck(5, null); SHIP.device.settings.tips = false; const tl = ROOM_TILES['t'], c = cellPos(...tl[Math.floor(tl.length / 2)]); player.obj.position.set(c.x, 0, c.z); player.stop(); })()" % (d - 1)); g.step(10)
    print('doors/edges of t:', g.ev("JSON.stringify(ROOM_TILES['t'])"))
    last = None
    for k in range(500):
        g.step(30); x = json.loads(g.ev(LOOK))
        sig = json.dumps([x['inRoom'], x['path']])
        if sig != last: print(x['m'], 'path out', x['path'], 'in room', x['inRoom']); last = sig
        if k % 20 == 0: print('   tea:', x['tea'])
        if x['m'] >= 13 * 60 + 55: break
    pass
    print('errors', g.errors[:3]); g.close()
