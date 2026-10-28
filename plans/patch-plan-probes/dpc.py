from pp import *
import json
src = open(REPO + '/player_check.py').read()
PAPER = src.split('PAPER = r"""')[1].split('"""')[0]
g = start('?nosave&debug'); g.step(5)
for lab, d in [('today', {}), ('social 2.5/.5', {'social':[2.5,.5]}), ('hunger 4 (work x1.75 not modelled)', {})]:
    r = g.ev(f"(() => {{ const D0 = JSON.parse(JSON.stringify(NEED_DRAIN)); Object.assign(NEED_DRAIN, {json.dumps(d)}); const r = ({PAPER})({{ normal: true }}); Object.assign(NEED_DRAIN, D0); return r; }})()")
    print(lab, r['lo'], r['ends'])
g.close()
