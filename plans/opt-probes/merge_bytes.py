# opt #10 proof: after each deck's build, a fingerprint of every mesh under deckRoot (in scene order): its kind, material,
# draw range, shadow flags, matrix, and every attribute's and the index's raw bytes (FNV-1a over the bytes); and the
# random seed. Two builds must print the same. Also the time of each build (3 builds, best).
import sys, os, re, json, hashlib
src = open('/home/user/Cadet-game/cadet_test.py').read().split("import sys, json, hashlib")[0]
exec(src)
from playwright.sync_api import sync_playwright
FP = r"""(() => {
  const h = a => { const u = new Uint8Array(a.buffer, a.byteOffset, a.byteLength); let x = 2166136261; for (let i = 0; i < u.length; i++) { x ^= u[i]; x = Math.imul(x, 16777619) >>> 0; } return x.toString(16) + ':' + u.length; };
  const out = []; deckRoot.traverse(o => { if (!o.geometry) return; const g = o.geometry, at = Object.keys(g.attributes).sort().map(k => k + '=' + h(g.attributes[k].array) + '/' + g.attributes[k].itemSize);
    out.push([o.type, (Array.isArray(o.material) ? o.material : [o.material]).map(m => m && m.type + m.color?.getHexString()).join(','), o.castShadow, o.receiveShadow, o.visible, JSON.stringify(g.drawRange), JSON.stringify(g.groups), g.index ? h(g.index.array) : '-', at.join(' '), o.matrixWorld.elements.map(v => v.toFixed(6)).join(',')].join('|')); });
  out.push('STAND ' + [...STAND].sort().join(' ')); out.push('MAP ' + MAP.join('/')); out.push('EDGES ' + edgeList.map(e => [e.key, e.wx, e.wz, e.sx].join(':')).join(' ')); out.push('TALL ' + TALL_ALL.map(b => JSON.stringify(b.ranges) + JSON.stringify(b.mesh.geometry.groups)).join(' '));
  return { n: out.length, all: out, seed, geos: renderer.info.memory.geometries };
})()"""
res = {}
with sync_playwright() as pw:
    for tag, path in (('old', sys.argv[1]), ('new', sys.argv[2])):
        g = Game(pw, path, 390, 844); g.ev("window.__realTick = tickShip; tickShip = () => {}")
        for n in (1, 2, 3, 4, 5, 6, 7):
            ms = g.page.evaluate("n => { const T = () => new Event('x').timeStamp; let best = 1e9; for (let k = 0; k < 5; k++) { const a = T(); __sc('goToDeck(' + n + ')'); best = Math.min(best, T() - a); if (k < 4) __sc('goToDeck(' + (n === 6 ? 5 : 6) + ')'); } return Math.round(best); }", n)
            fp = g.ev(FP); res[(tag, n)] = fp
            print(tag, f'D{n}', f'build {ms} ms', 'meshes', fp['n'], 'seed', fp['seed'], 'fp', hashlib.md5('\n'.join(fp['all']).encode()).hexdigest()[:12], flush=True)
        g.close()
bad = 0
for n in (1, 2, 3, 4, 5, 6, 7):
    a, b = res[('old', n)], res[('new', n)]
    if a['all'] != b['all'] or a['seed'] != b['seed']:
        bad += 1; diff = [i for i, (x, y) in enumerate(zip(a['all'], b['all'])) if x != y][:3]
        print(f'D{n} DIFFERS: meshes {a["n"]} vs {b["n"]}, seed {a["seed"]} vs {b["seed"]}, first rows', diff, (a['all'][diff[0]][:300], b['all'][diff[0]][:300]) if diff else '')
print('MERGED SHAPES IDENTICAL' if not bad else f'MERGED SHAPES DIFFER on {bad} deck(s)')
