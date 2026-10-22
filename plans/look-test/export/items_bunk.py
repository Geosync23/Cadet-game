import os, pathlib
HERE = pathlib.Path(__file__).parent
os.environ.setdefault('CADET_CHROME','/opt/pw-browsers/chromium')
exec(open(HERE / '../../../cadet_test.py').read().split("import sys, json, hashlib")[0])
with sync_playwright() as pw:
    g = Game(pw, str(HERE / '../../../starship-cadet.html'), w=412, h=960)
    g.ev("goToDeck(4)"); g.step(3)
    for r in g.ev("ITEMS.map(i => { const b = new THREE.Box3().setFromObject(i.g); return [i.t, !!i.wall, [b.min.x,b.min.y,b.min.z,b.max.x,b.max.y,b.max.z].map(v=>+v.toFixed(2))]; }).filter(r => r[2][0] > -19.3 && r[2][3] < -13.7 && r[2][2] > -10.8 && r[2][5] < -5.6)"): print(r)
    g.close()
