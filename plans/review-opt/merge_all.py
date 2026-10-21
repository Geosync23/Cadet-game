# OR1's probe for opt #10: every mergeMeshes call anywhere (deck, kit, cabin touches, the lift roof, ...) fingerprinted
# right after it merges (FNV-1a over each resulting mesh's attribute and index bytes, in traverse order), plus
# tallCombine's meshes and STAND/edges after each deck. Two builds must log the same.
#   python3 merge_all.py OLD.html NEW.html
import sys, os, re, pathlib, hashlib
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("import sys, json, hashlib")[0])
from playwright.sync_api import sync_playwright
HOOK_FN = r"""
function __fp(root) { const h = a => { const u = new Uint8Array(a.buffer, a.byteOffset, a.byteLength); let x = 2166136261; for (let i = 0; i < u.length; i++) { x ^= u[i]; x = Math.imul(x, 16777619) >>> 0; } return x.toString(16) + ':' + u.length; };
  const out = []; root.traverse(o => { if (!o.isMesh) return; const g = o.geometry; out.push(Object.keys(g.attributes).sort().map(k => k + '=' + h(g.attributes[k].array)).join(' ') + (g.index ? ' i=' + h(g.index.array) : '') + ' ' + JSON.stringify(g.groups) + ' ' + (Array.isArray(o.material) ? o.material.length : o.material.uuid ? 'm' : '-') + ' ' + o.castShadow); }); return out.join(';'); }
function mergeMeshes(root) { const r = mergeMeshes__(root); (window.__mlog = window.__mlog || []).push(__fp(root)); return r; }
function mergeMeshes__(root) {"""
def prep(path, tag):
    s = open(path).read(); n = s.count('function mergeMeshes(root) {'); assert n == 1, n
    s = s.replace('function mergeMeshes(root) {', HOOK_FN, 1)
    p = WORK / 'test' / f'_merge_{tag}.html'; p.write_text(s); return str(p)
RUN = r"""(() => { const L = window.__mlog || []; window.__mlog = []; return L; })()"""
DECK = r"""(() => { const t = TALL_ALL.map(b => __fp(b.mesh) + JSON.stringify(b.ranges)).join('|'); return [...STAND].sort().join(' ') + '#' + edgeList.map(e => [e.key, e.wx, e.wz, e.sx].join(':')).join(' ') + '#' + t + '#' + seed; })()"""
res = {}
with sync_playwright() as pw:
    for tag, path in (('old', sys.argv[1]), ('new', sys.argv[2])):
        errs = []; g = Game(pw, prep(path, tag), 390, 844, errs); log = [('load', x) for x in g.ev(RUN)]
        for n in (1, 2, 3, 5, 6, 7, 4, 3):
            g.ev(f'goToDeck({n})'); log += [(f'D{n}', x) for x in g.ev(RUN)]; log.append((f'D{n} deck', g.ev(DECK)))
        for extra in ('roofShaft()', 'cabinDraw()'):   # the lift roof's shaft and your cabin's touches, built on demand
            try: g.ev(f'goToDeck(4); {extra}'); log += [(extra, x) for x in g.ev(RUN)]
            except Exception as e: log.append((extra, 'ERR ' + str(e)[:80]))
        res[tag] = log; g.close()
        print(tag, 'calls', len(log), 'md5', hashlib.md5(repr(log).encode()).hexdigest()[:12], 'errors', errs[:3], flush=True)
a, b = res['old'], res['new']
bad = [i for i, (x, y) in enumerate(zip(a, b)) if x != y]
print('per place:', {k: sum(1 for t, _ in a if t == k) for k in dict.fromkeys(t for t, _ in a)})
print('MERGE ALL IDENTICAL' if not bad and len(a) == len(b) else f'MERGE DIFFERS at {bad[:5]} ({len(a)} vs {len(b)}): {a[bad[0]] if bad else ""} / {b[bad[0]] if bad else ""}'[:600])
