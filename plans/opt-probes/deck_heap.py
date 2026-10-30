# Deck change time per deck (goToDeck, then the first drawn frame), and a heap snapshot summary after opening.
import sys, os, re, time, json, collections
src = open('/home/user/Cadet-game/cadet_test.py').read().split("import sys, json, hashlib")[0]
exec(src)
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844)
    g.page.evaluate("window.__realNow = (() => { const f = Object.getPrototypeOf(performance).now.bind(performance); return () => f(); })()")
    decks = g.ev("Object.keys(DECKS).map(Number)")
    for lap in (1, 2):
        row = []
        for n in decks + [4]:
            r = g.page.evaluate(f"() => {{ const a = __realNow(); __sc('goToDeck({n})'); const b = __realNow(); window.__skip = false; __step(1, 33); const c = __realNow(); return [b - a, c - b, __sc('renderer.info.render.calls')]; }}")
            row.append(f"D{n} build {r[0]:.0f} ms + frame {r[1]:.0f} ms")
        print(f'lap {lap}:', '; '.join(row), flush=True)
    g.close()
    g = Game(pw, sys.argv[1], 390, 844)
    cdp = g.page.context.new_cdp_session(g.page); cdp.send('HeapProfiler.collectGarbage')
    print('heap used MB', g.ev('Math.round(performance.memory.usedJSHeapSize/1048576)'))
    chunks = []
    cdp.on('HeapProfiler.addHeapSnapshotChunk', lambda e: chunks.append(e['chunk']))
    cdp.send('HeapProfiler.takeHeapSnapshot', {'reportProgress': False})
    snap = json.loads(''.join(chunks)); g.close()
m = snap['snapshot']['meta']; nf = m['node_fields']; F = len(nf); types = m['node_types'][0]; strings = snap['strings']; nodes = snap['nodes']
it, iname, isz = nf.index('type'), nf.index('name'), nf.index('self_size')
by = collections.Counter(); cnt = collections.Counter()
for i in range(0, len(nodes), F):
    t = types[nodes[i + it]]; nm = strings[nodes[i + iname]]
    key = t + ':' + (nm[:40] if t in ('object', 'native', 'closure', 'hidden', 'array', 'code') else '')
    by[key] += nodes[i + isz]; cnt[key] += 1
tot = sum(by.values()); print(f'snapshot self sizes total {tot/1e6:.1f} MB, {len(nodes)//F} objects')
for k, v in by.most_common(40): print(f'  {v/1e6:7.1f} MB  x{cnt[k]:<8} {k}')
