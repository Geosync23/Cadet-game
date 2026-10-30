# opt #5: what holds the array storage kept after a deck tour. Two heap snapshots of one page (on Deck 4 after load, and on
# Deck 4 after a tour of every deck); array buffers in the second that aren't in the first, summed by who holds them
# (the shortest retaining path from the roots, its last named hops).
import sys, os, re, json, collections
src = open('/home/user/Cadet-game/cadet_test.py').read().split("import sys, json, hashlib")[0]
exec(src)
from playwright.sync_api import sync_playwright
def snap(cdp):
    chunks = []
    cdp.on('HeapProfiler.addHeapSnapshotChunk', lambda e: chunks.append(e['chunk']))
    cdp.send('HeapProfiler.collectGarbage'); cdp.send('HeapProfiler.takeHeapSnapshot', {'reportProgress': False})
    return json.loads(''.join(chunks))
def parse(S):
    m = S['snapshot']['meta']; nf = m['node_fields']; ef = m['edge_fields']; NF, EF = len(nf), len(ef)
    ntypes = m['node_types'][0]; etypes = m['edge_types'][0]; strs = S['strings']; N = S['nodes']; E = S['edges']
    iT, iN, iI, iS, iE = nf.index('type'), nf.index('name'), nf.index('id'), nf.index('self_size'), nf.index('edge_count')
    eT, eN, eTo = ef.index('type'), ef.index('name_or_index'), ef.index('to_node')
    n = len(N) // NF; first = [0] * (n + 1); k = 0
    for i in range(n): first[i] = k; k += N[i * NF + iE]
    first[n] = k
    return dict(NF=NF, EF=EF, n=n, N=N, E=E, first=first, strs=strs, ntypes=ntypes, etypes=etypes, iT=iT, iN=iN, iI=iI, iS=iS, eT=eT, eN=eN, eTo=eTo)
def info(P, i):
    N, NF = P['N'], P['NF']
    return P['ntypes'][N[i * NF + P['iT']]], P['strs'][N[i * NF + P['iN']]], N[i * NF + P['iI']], N[i * NF + P['iS']]
def tree(P):                                             # BFS from the root, strong edges only: parent node and edge name
    n, E, EF, NF, first = P['n'], P['E'], P['EF'], P['NF'], P['first']
    par = [-1] * n; pe = [''] * n; seen = bytearray(n); seen[0] = 1; q = collections.deque([0])
    while q:
        i = q.popleft()
        for k in range(first[i], first[i + 1]):
            b = k * EF; t = P['etypes'][E[b + P['eT']]]
            if t == 'weak' or t == 'shortcut': continue
            j = E[b + P['eTo']] // NF
            if seen[j]: continue
            seen[j] = 1; par[j] = i; nm = E[b + P['eN']]
            pe[j] = P['strs'][nm] if t in ('property', 'context', 'internal', 'shortcut') else ('[' + str(nm) + ']' if t == 'element' else t + ':' + str(nm) if t != 'hidden' else 'hidden')
            q.append(j)
    return par, pe
def path(P, par, pe, i, hops=9):
    out = []; x = i
    while x > 0 and len(out) < 40:
        t, nm, _, _ = info(P, x); out.append((pe[x], t, nm)); x = par[x]
    out.reverse()
    # keep named hops: properties and object names
    sig = []
    for e, t, nm in out:
        if t in ('object', 'closure') and nm not in ('Object', 'Array', 'system / Context', ''): sig.append(f'{nm}.{e}' if e else nm)
        elif e and not e.startswith('[') and e not in ('hidden', 'elements', 'properties', 'backing_store', 'buffer', 'array'): sig.append(e)
    return ' > '.join(sig[-hops:])
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844); g.ev("window.__realTick = tickShip; tickShip = () => {}")
    cdp = g.page.context.new_cdp_session(g.page); cdp.send('HeapProfiler.enable')
    g.step(3); A = parse(snap(cdp))
    for n in (3, 5, 2, 1, 6, 7, 4): g.ev(f'goToDeck({n})'); g.step(3)
    B = parse(snap(cdp))
    g.close()

def top(P, par, pe, i):                                  # the game's variable the buffer hangs from: the edge after the first 'context'
    x = i; chain = []
    while x > 0: chain.append(pe[x]); x = par[x]
    chain.reverse()
    for k, e in enumerate(chain):
        if e == 'context' and k + 1 < len(chain):
            nxt = chain[k + 1]; return nxt + (' > ' + chain[k + 2] if k + 2 < len(chain) and nxt in ('crowd', 'DECKS', 'CROWD_KEPT') else '')
    return '(' + ' > '.join(chain[:4]) + ')'
def sums(P):
    par, pe = tree(P); c = collections.Counter(); n = collections.Counter()
    for i in range(P['n']):
        t, nm, nid, sz = info(P, i)
        if 'JSArrayBufferData' not in nm: continue
        k = top(P, par, pe, i); c[k] += sz; n[k] += 1
    return c, n
ca, na = sums(A); cb, nb = sums(B)
print(f'array buffer data: after load {sum(ca.values()) / 1048576:.1f} MB, after the tour {sum(cb.values()) / 1048576:.1f} MB')
keys = sorted(set(ca) | set(cb), key=lambda k: -(cb[k] - ca[k]))
print('by the top-level name that holds it (after load -> after the tour, MB, buffers):')
for k in keys[:25]: print(f'  {ca[k] / 1048576:7.2f} -> {cb[k] / 1048576:7.2f}  ({(cb[k] - ca[k]) / 1048576:+7.2f})  {na[k]:5d} -> {nb[k]:5d}  {k}')
print('largest after the tour:')
for k, v in cb.most_common(12): print(f'  {v / 1048576:7.2f} MB  {k}')
