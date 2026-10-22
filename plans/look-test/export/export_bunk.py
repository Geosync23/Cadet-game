# Exports Bunk 1 (Deck 4, room 'a': the player's bunk room, bed 4-B1-4) from the running game into ../bunk1.json.
# Run from anywhere (needs playwright and three r128 in $CADET_WORK/three, as for cadet_test.py):
#   CADET_CHROME=/opt/pw-browsers/chromium python3 plans/look-test/export/export_bunk.py
# Morning, Day 1 06:05: you at your wardrobe, Tomas up by his bunk, Tran asleep on the top berth over him, Lukas asleep
# in the far bottom berth; Santos and Quaye have gone to wash. Every person in the room is drawn as a full figure.
# The same room is then lit as the game lights it at night (applyLight(1): lamps up, sky light and sun down), and those
# lights are saved beside the day's.
import os, json, pathlib
HERE = pathlib.Path(__file__).parent
os.environ.setdefault('CADET_CHROME', '/opt/pw-browsers/chromium')
exec(open(HERE / '../../../cadet_test.py').read().split("import sys, json, hashlib")[0])
RG = "window.__RG = { x0: X0(6) - .12, x1: X0(11) + .12, z0: Z0(0) - .75, z1: Z0(4) + .11 }; window.__KEEP_PLAYER = true"
STAGE = r"""(() => { crewDetail = () => {};
  const at = (id, x, z, y, face, pose) => { const a = DECK_CREW.find(a => a.p.id === id); if (!a) return id + '?';
    a.path = []; a.x = x; a.z = z; a.y = y; a.face = face; a.pose = pose; a.settled = true;
    if (!a.h.full) { a.remove(); a.h = new FullPerson(rosterSpec(a.p), a.p.id); } a.h.set({ x, y, z }, face, pose); return id; };
  const bed = id => placeSpot(id);
  const b2 = bed('4-B1-2'), b5 = bed('4-B1-5');
  const out = [at('tomas', X0(6) + .55, Z0(2) + .55, 0, Math.PI * .85, 'stand'), at('tran-chloe', b2.x, b2.z, b2.y, b2.face, 'lie'), at('dlamini-lukas', b5.x, b5.z, b5.y, b5.face, 'lie')];
  for (const id of ['santos-zofia', 'quaye-hiro']) { const a = DECK_CREW.find(a => a.p.id === id); if (a) { a.path = []; a.x = 30; a.z = 30; a.settled = true; a.h.set({ x: 30, y: -40, z: 30 }, 0, 'stand'); } }
  player.obj.position.set(X0(7) + .15, 0, Z0(3) + .25); player.obj.rotation.y = -Math.PI / 2 + .35;
  target.set(X0(8) + .5, .7, Z0(2)); camera.zoom = 1.62; camera.updateProjectionMatrix(); applyLight(0);
  return out; })()"""
with sync_playwright() as pw:
    g = Game(pw, str(HERE / '../../../starship-cadet.html'), w=412, h=960)
    g.ev("goToDeck(4)"); g.step(3)
    g.ev("window.__realTick = tickShip; tickShip = () => {}; player.steer = null; player.stop(); applyLight = (k => { const f = applyLight; return f; })(applyLight)")
    print(g.ev(STAGE)); g.step(8); print(g.ev(STAGE)); g.ev("updateClock = () => {}; nightAt = () => 0; nightT = 0; applyLight(0)"); g.step(4); g.ev("nightT = 0; applyLight(0)")
    g.shot(str(HERE / '../shots/bunk_game_day_412x960.png'))
    g.ev(RG)
    day = json.loads(g.ev(open(HERE / 'export.js').read()))
    g.ev("nightAt = () => 1; nightT = 1; applyLight(1)"); g.step(2); g.ev("nightT = 1; applyLight(1)")
    g.shot(str(HERE / '../shots/bunk_game_night_412x960.png'))
    g.ev("window.__LIGHTS_ONLY = true")
    night = json.loads(g.ev(open(HERE / 'export.js').read()))
    day['night'] = night
    (HERE / '../bunk1.json').write_text(json.dumps(day, separators=(',', ':')))
    print(len(day['meshes']), 'meshes', sum(1 for m in day['meshes'] if m['c']), 'crew meshes;', day['game'], g.errors[:3])
    for L in day['lights']: print('day', L['type'], L['intensity'], hex(L['color']), [round(v, 2) for v in L['pos']])
    for L in night['lights']: print('night', L['type'], L['intensity'], hex(L['color']))
    print('sprites', len(day['sprites']), len(night['sprites']), 'lamps', g.ev('LAMPS.length'))
    print('exp', day['renderer']['exp'], night['exp'], hex(day['bg']), hex(night['bg']))
    g.close()
