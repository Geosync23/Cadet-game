# RV9: compare two Day 0 logs (addlog.py's RV9_LOG): lines lost, the front end's waits, the dinner part identical
import json, sys, re
A, B = (json.load(open(f)) for f in sys.argv[1:3])
def text(e):
    k, x = e[3], e[4]
    if x is None: return None
    if k == 'dlg':
        try: v = json.loads(x.split(' | ', 1)[1]); return (v.get('name') or '') + ': ' + (v.get('text') or '') + (' [' + ' / '.join(v.get('choices') or []) + ']' if v.get('choices') else '')
        except Exception: return x
    if k == 'say': return x.replace(' | ', ': ', 1)
    if k == 'toast': return x.replace(' | ', ': ', 1)
    return x
def lines(d, kinds=('say', 'dlg', 'toast', 'mail')): return [(e[0], e[1][-5:], e[2], e[3], text(e)) for e in d['log'] if e[3] in kinds and text(e)]
def body(s): return re.sub(r'^[^:]+: ', '', s)   # the words, whoever says them and however (a bubble, the box, a panel)
la, lb = lines(A), lines(B)
# 1. nothing lost: every line before is said or shown after (bubble, panel or box)
wb = {body(x[4]) for x in lb} | {x[4] for x in lb}
lost = [x for x in la if body(x[4]) not in wb and x[4] not in wb]
print(f'lines before {len(la)}, after {len(lb)}; lost (said before, nowhere after): {len(lost)}')
for x in lost: print('   LOST', x[1], x[2], x[3], x[4][:160])
new = [x for x in lb if body(x[4]) not in {body(y[4]) for y in la}]
print(f'new lines after: {len(new)}')
for x in new: print('   NEW ', x[1], x[2], x[3], x[4][:160])
# 2. how each line is given: kind changes (box -> bubble etc.)
ka = {body(x[4]): x[3] for x in la}
for x in lb:
    b = body(x[4])
    if b in ka and ka[b] != x[3]: print(f'   now {x[3]} (was {ka[b]}): {x[1]} {x[4][:120]}')
# 3. the dinner part: from the first event after the device step ends (step toMess, not the device panel) to 19:30
def dinner(d):
    L = [e for e in d['log'] if e[3] in ('say', 'dlg', 'toast', 'mail', 'goal')]
    i = next(k for k, e in enumerate(L) if e[2] in ('toMess', 'servery', 'table', 'free') and not (e[3] == 'dlg' and 'introDevice' in str(e[4])) and not (e[3] == 'toast' and 'hands you your device' in str(e[4])) and not any('introDevice' in str(f[4]) for f in L[k:k + 1]) and k > max([j for j, f in enumerate(L) if 'introDevice' in str(f[4])] or [0]))
    return L[i:], L[i][0]
da, ta = dinner(A); db, tb = dinner(B)
norm = lambda L, t0: [(e[0] - t0, e[2], e[3], text(e)) for e in L if e[3] != 'goal' or True]
na, nb = norm(da, ta), norm(db, tb)
print(f'dinner part: starts before at {da[0][1]}, after at {db[0][1]} (shift {tb - ta} ship min); events {len(na)} vs {len(nb)}')
same_rel = na == nb
abs_a = [(e[0], e[2], e[3], text(e)) for e in da]; abs_b = [(e[0], e[2], e[3], text(e)) for e in db]
print('  identical, relative to its start:', same_rel, '; identical in ship time:', abs_a == abs_b)
if not same_rel:
    import difflib
    for l in list(difflib.unified_diff([str(x) for x in na], [str(x) for x in nb], lineterm='', n=1))[:60]: print('   ', l[:200])
# 4. Zeke standing still (3+ samples at one tile), per step, before the dinner part
def still(d, upto):
    out, run = [], None
    for t, st, deck, me, esc, mode, dlg in d['pos']:
        k = (st, deck, tuple(esc) if esc else None)
        if run and run[0] == k: run[2] = t; run[3] += 1
        else:
            if run and run[3] >= 3: out.append((run[0][0], run[0][1], run[0][2], run[1][-5:], run[2][-5:], run[3]))
            run = [k, t, t, 1]
    return [o for o in out if o[0] in ('ramp', 'hello', 'haulway', 'works', 'lift', 'wing', 'bunk', 'stow', 'device')]
for name, d in (('before', A), ('after', B)):
    print(f'Zeke standing still, {name} (step, deck, tile, from, to, samples of 20 frames):')
    for o in still(d, None): print('   ', o)
steps = lambda d: [(e[1][-5:], e[2]) for k, e in enumerate(d['log']) if k == 0 or e[2] != d['log'][k - 1][2]]
print('steps before:', steps(A)); print('steps after: ', steps(B))
