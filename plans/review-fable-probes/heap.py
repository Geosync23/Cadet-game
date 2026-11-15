import sys; sys.path.insert(0, '' + __import__('os').path.dirname(__import__('os').path.abspath(__file__)) + ''); from g import *
import collections
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], q=sys.argv[2] if len(sys.argv) > 2 else '?nosave&debug'); g.step(60)
    print('usedJSHeap after gc MB', g.heap() / 1e6, 'Runtime.getHeapUsage', g.cdp.send('Runtime.getHeapUsage'))
    chunks = []; g.cdp.on('HeapProfiler.addHeapSnapshotChunk', lambda e: chunks.append(e['chunk'])); g.cdp.send('HeapProfiler.takeHeapSnapshot', {'reportProgress': False})
    s = json.loads(''.join(chunks)); m = s['snapshot']['meta']; nf = m['node_fields']; N = len(nf); nodes = s['nodes']; strs = s['strings']; types = m['node_types'][0]
    it, inn, iss = nf.index('type'), nf.index('name'), nf.index('self_size')
    byt = collections.Counter(); byname = collections.Counter(); cnt = collections.Counter(); big = []
    for i in range(0, len(nodes), N):
        t = types[nodes[i + it]]; sz = nodes[i + iss]; byt[t] += sz; nm = strs[nodes[i + inn]]
        key = t + ':' + (nm[:40] if t not in ('string', 'concatenated string', 'sliced string', 'code', 'number', 'hidden') else ''); byname[key] += sz; cnt[key] += 1
        if sz > 400000: big.append((sz, t, nm[:80]))
    tot = sum(byt.values()); print('snapshot total MB', tot / 1e6)
    for t, v in byt.most_common(): print(f'  {t:<22}{v / 1e6:8.2f} MB')
    print('top groups:'); [print(f'  {k:<60}{v / 1e6:8.2f} MB  x{cnt[k]}') for k, v in byname.most_common(28)]
    print('objects over 400 KB:'); [print('  ', round(a / 1e6, 2), b, c.replace('\n', ' ')) for a, b, c in sorted(big, reverse=True)[:25]]
    g.close()
