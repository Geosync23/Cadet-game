# RV9: the dinner part, scripted events only (Zeke, Calder, Tomas, you; scenes, the message box, Mail, steps), timed from
# the moment he leads off to the mess (the end of the device hand-over: its last line, the panel or the bubbles)
import json, sys
SCRIPT = ('Zeke Torres', 'Chief Ines Calder', 'Tomas Lind', 'Sam')
def load(f):
    d = json.load(open(f)); L = d['log']
    # the lead-off: the last event of the hand-over (the old panel 'introDevice', or the new bubbles' after-lines)
    k0 = max(k for k, e in enumerate(L) if ('introDevice' in str(e[4])) or (e[3] == 'say' and ('Brennan doesn\'t hold plates' in str(e[4]))))
    t0 = L[k0][0]; out = []; prev = None
    for e in L[k0 + 1:]:
        k, x = e[3], str(e[4])
        if k == 'say' and not any(x.startswith(s + ' |') for s in SCRIPT): continue   # crew chatter: who's about at that hour
        if k == 'goal' and x == prev: continue
        if k == 'goal': prev = x
        if k == 'dlg':
            try: v = json.loads(x.split(' | ', 1)[1]); x = x.split(' | ')[0] + ' | ' + (v.get('name') or '') + ': ' + (v.get('text') or '') + ' ' + '/'.join(v.get('choices') or [])
            except Exception: pass
        out.append((round(e[0] - t0, 1), e[2], k, x[:150]))
    steps = [(round(e[0] - t0, 1), e[2]) for j, e in enumerate(L) if j > k0 and e[2] != L[j - 1][2]]
    return t0, out, steps, L[k0][1]
ta, A, sa, ca = load(sys.argv[1]); tb, B, sb, cb = load(sys.argv[2])
print(f'lead-off: before {ca}, after {cb}; scripted events {len(A)} vs {len(B)}')
print('steps after the lead-off, before:', sa); print('steps after the lead-off, after: ', sb)
ka = [(x[1], x[2], x[3]) for x in A]; kb = [(x[1], x[2], x[3]) for x in B]
print('same events in the same order (steps, kinds, words):', ka == kb)
dt = [(x, y) for x, y in zip(A, B) if (x[1], x[2], x[3]) == (y[1], y[2], y[3]) and abs(x[0] - y[0]) > 1.01]
print('same events more than a ship minute apart:', len(dt))
for x, y in dt[:20]: print('   ', x, '|', y[0])
if ka != kb:
    import difflib
    for l in list(difflib.unified_diff([str(x) for x in ka], [str(x) for x in kb], lineterm='', n=0))[:50]: print('   ', l[:220])
