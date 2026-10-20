import pp
from pp import *
g = start('?nosave&debug'); g.step(5)
g.ev("(() => { skipTo(450); goToDeck(4); const sp = placeSpot('4-toilet-p1'); player.obj.position.copy(cellPos(...sp.walk)); player.obj.position.x += 1.5; target.copy(player.obj.position).setY(.7); return 1; })()")
g.secs(1)
for i in range(40):
    g.secs(1)
    r = g.ev(r"""(() => { const v = new THREE.Vector3(); return STALL_CAP.list.filter(c => c.m.visible).map(c => { c.m.getWorldPosition(v); v.project(camera); return [c.id, Math.round((v.x + 1) * innerWidth / 2), Math.round((1 - v.y) * innerHeight / 2), clockText()]; }); })()""")
    if r and 0 < r[0][1] < 390 and 0 < r[0][2] < 844:
        print(r); g.page.screenshot(path='/tmp/rv/shots/08-red.png')
        from PIL import Image
        x, y = r[0][1], r[0][2]
        Image.open('/tmp/rv/shots/08-red.png').crop((max(0, x-80), max(0, y-60), x+80, y+60)).resize((640, 480), Image.NEAREST).save('/tmp/rv/shots/08-red-crop.png'); break
    elif r: print('offscreen', r)
g.close()
