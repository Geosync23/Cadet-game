# PR9: c3b76f4's 'arriving' on paper: Day 19's welcome line (1tvwp26) and the {sunleavers} line with this build's rotations,
# then with the first rotation moved to Day 20, 21, 22 and with an out-only rotation on Day 21; and Day 26 (no rotation near)
import sys, json, os
exec(open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[1])), 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1])
    r = g.ev("""(() => { const A = FRI_ADDRESSES['friday-d19'].beats.flatMap(b => b.lines), W = A.find(l => l.id === '1tvwp26'), L = A.find(l => l.id === 'vwvwab'), first = ROSTER_ROTATIONS[0], out = [];
      const row = k => out.push([k, friCond('arriving', 19), friFill(W, 19), friFill(L, 19), friCond('arriving', 26)]);
      row('as built (first ' + first.day + ')');
      for (const d of [20, 21, 22]) { ROSTER_ROTATIONS[0] = { ...first, day: d }; row('day ' + d); }
      ROSTER_ROTATIONS[0] = { ...first, day: 21, in: [] }; row('day 21, out only');
      ROSTER_ROTATIONS[0] = { ...first, day: 21, out: [] }; row('day 21, in only');
      ROSTER_ROTATIONS[0] = first; return out; })()""")
    for x in r: print(json.dumps(x))
    print('page errors', g.errors[:4]); g.close()
