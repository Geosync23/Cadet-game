# Exports the Deck 5 tea corner from the running game into plans/look-test/tea-corner.json.
# Run from the repo root (needs playwright and three r128 in $CADET_WORK/three, as for cadet_test.py):
#   CADET_CHROME=/opt/pw-browsers/chromium python3 plans/look-test/export/export.py
# It sets the clock to 13:08 on Day 1, seats Calder (armchair), Pell (stool) and Halloran (standing) at the
# tea corner's places 5-tea-1..3 as full rigs, then copies every triangle in the room from the game's meshes.
import os, pathlib
HERE = pathlib.Path(__file__).parent
os.chdir(HERE)
import sys, os
os.environ.setdefault('CADET_CHROME','/opt/pw-browsers/chromium')
src = open(HERE / '../../../cadet_test.py').read().split("import sys, json, hashlib")[0]
exec(src)
SEAT = """(() => { crewDetail = () => {}; const ids = ['calder','pell','halloran-emeka']; const sp = ['5-tea-1','5-tea-2','5-tea-3']; const out=[];
 ids.forEach((id,k) => { const a = DECK_CREW.find(a => a.p.id===id); const s = placeSpot(sp[k]); if(!a||!s) {out.push([id,!!a,!!s]); return;}
   a.path=[]; a.x=s.x; a.z=s.z; a.settled=true; a.spot = PLACE_OF.get(sp[k]); a.pose = PLACE_OF.get(sp[k]).pose; a.face=s.face; a.y=s.y; if (!a.h.full) { a.remove(); a.h = new FullPerson(rosterSpec(a.p), a.p.id); } a.h.set({ x: a.x, y: a.y, z: a.z }, a.face, a.pose); out.push([id, s.x, s.z, a.pose]); });
 return out; })()"""
with sync_playwright")[0])
with sync_playwright() as pw:
    g = Game(pw, str(HERE / '../../../starship-cadet.html'), w=412, h=960)
    g.ev("SHIP.time.min = 788"); g.ev("goToDeck(4)"); g.step(3); g.ev("goToDeck(5)"); g.step(3)
    g.ev("window.__realTick = tickShip; tickShip = () => {}; player.steer = null; player.stop()")
    g.ev(SEAT)
    g.ev("player.obj.position.set(X0(21)+.5,0,Z0(3)+.5); target.set(X0(22)+.5,.7,Z0(1)+.5); camera.zoom=1.62; camera.updateProjectionMatrix()"); g.step(10)
    g.shot(str(HERE / '../shots/game_412x960_reference.png'))
    s = g.ev(open('export.js').read())
    open(HERE / '../tea-corner.json','w').write(s)
    d = json.loads(s)
    print(len(s), len(d['meshes']), len(d['sprites']), len(d['mats']), len(d['texs']), d['skipped'][:10], d['renderer'], d['cam'], d['game'])
    for L in d['lights']: print(L)
    print(sum(len(m['p'])//3 for m in d['meshes']), 'verts')
    print([ (k, v['w'], v['h'], len(v['url'] or '')) for k,v in d['texs'].items()])
    print([m['type'] for m in d['mats'].values() if m['obc']])
    g.close()
