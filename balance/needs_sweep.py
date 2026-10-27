# BAL1: what-ifs on needs_sim.py's model (nothing in the game changes): share of waking time under 25 for the
# 'average' and 'diligent' players with one number changed at a time
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent)); import needs_sim as N
def red(style, days=28):
    p = N.P(); p.t = 0
    for d in range(days): N.day(p, d, style, d % 7 < 5)
    aw = mins = None; out = {}
    tot = sum(x[0] - y[0] for y, x in zip(p.log, p.log[1:]) if not x[1])
    for k in N.K: out[k] = round(sum(x[0] - y[0] for y, x in zip(p.log, p.log[1:]) if not x[1] and x[3][k] < 25) / tot * 100)
    out['walkslow'] = round(sum(x[0] - y[0] for y, x in zip(p.log, p.log[1:]) if not x[1] and N.eff(x[3])['walk'] < 1) / tot * 100)
    return out
base = dict(N.DRAIN)
res = {}
for name, change in [('as built', {}), ('fitness 1.0/h awake', {'fitness': (1.0, .35)}), ('fitness 0.9/h awake', {'fitness': (.9, .3)}),
                     ('hunger asleep 4/h', {'hunger': (4, 4)}), ('leisure 1.8/h awake', {'leisure': (1.8, 0)})]:
    N.DRAIN = dict(base); N.DRAIN.update(change)
    res[name] = {s: red(s) for s in ('diligent', 'average', 'skipper')}
    print(name, res[name])
N.DRAIN = dict(base)
# work hunger 2 instead of 3 (patch: N.day reads +3 at work inside P.drain)
src = pathlib.Path(N.__file__).read_text()
(pathlib.Path(__file__).parent / 'data' / 'needs_sweep.json').write_text(json.dumps(res))
