import sys, json, os
os.chdir('/home/user/Cadet-game')
exec(open('cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844)
    print(g.ev(r"""(() => { setShipNow(1440 * 2 + 600); goToDeck(7);
      const T = (deckDef.places || []).filter(q => q.type === 'toilet' || q.type === 'basin').map(q => q.id);
      const v = new THREE.Vector3(), its = ITEMS.filter(i => /^toilet$|^basins$/i.test(i.t)).map(i => { i.hit.getWorldPosition(v); return i.t + '@' + (v.x + OX).toFixed(2) + ',' + (v.z + OZ).toFixed(2); });
      const spots = T.map(id => { const s = placeSpot(id); return id + ' walk ' + s.walk + ' xy ' + (s.x + OX).toFixed(2) + ',' + (s.z + OZ).toFixed(2); });
      return JSON.stringify({ T, its, spots }); })()"""))
    g.step(5)
    print('caps', g.ev("JSON.stringify(STALL_CAP.list.filter(c => c.root === deckRoot).map(c => c.id))"))
    # use one: the first toilet, as a tap on its stall would
    print(g.ev(r"""(() => { SHIP.player.needs.bathroom = 20; const it = ITEMS.find(i => /^toilet$/i.test(i.t)), at = new THREE.Vector3(); it.hit.getWorldPosition(at);
      return 'tap ' + playerTap(it, at, at.clone()); })()"""))
    for k in range(40):
        g.step(30)
        r = g.ev("JSON.stringify({ act: ACT && ACT.kind, place: ACT && ACT.placeId, b: Math.round(SHIP.player.needs.bathroom), p: [player.obj.position.x + OX, player.obj.position.z + OZ].map(v => +v.toFixed(2)), busy: PLAYER_PLACE, cap: STALL_CAP.list.filter(c => c.root === deckRoot && c.m.visible).map(c => c.id) })")
        if k == 12: print('body', g.ev('JSON.stringify(ACT && [ACT.x + OX, ACT.z + OZ, ACT.phase])'))
        if k % 4 == 0 or '"act":null' in r and k > 3: print(k, r)
        if '"act":null' in r and k > 3: break
    pass
    print(g.ev(r"""(() => { const it = ITEMS.find(i => /^basins$/i.test(i.t)), at = new THREE.Vector3(); it.hit.getWorldPosition(at); return 'basin tap ' + playerTap(it, at, at.clone()); })()"""))
    for k in range(20):
        g.step(30); r = g.ev("JSON.stringify({ act: ACT && ACT.kind, place: ACT && ACT.placeId })")
        if k % 4 == 0: print(k, r)
    print('errors', g.errors[:5])
    g.close()
