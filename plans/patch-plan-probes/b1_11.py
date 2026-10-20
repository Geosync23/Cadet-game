from b1_common import *
import sys
track = sys.argv[1] == '1'
g = start(); to_day1(g, 8*60+20)
print(g.ev("clockText()"), g.ev("trkItems().map(x => x.key + ' -> ' + (x.goal ? x.goal.label : '-'))"))
if track:
    k = g.ev("(trkItems().find(x => /briefing/i.test(x.title)) || {}).key")
    print('tracking', k, g.ev(f"trkTap({json.dumps(k)})"))
tele(g, 5, [20, 4])
print(g.ev(GOAL))
for i in range(120):
    g.secs(2)
    d = g.ev(DLG)
    s = g.ev(GOAL)
    if i % 6 == 0 or d: print(s)
    if s['t'] >= 'Day 1, Monday 09:20': break
# clock in
print('clock', g.ev("careerClock()")); g.secs(3); print(g.ev(GOAL)); g.secs(5); print(g.ev(GOAL))
g.snap('11-after-briefing-' + ('tracked' if track else 'untracked'))
g.close()
