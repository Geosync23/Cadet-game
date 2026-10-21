# OR2: a fingerprint of every crew member's plan for Days A..B (events as the build has them); prints one line a day
import sys, json
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("import sys, json, hashlib")[0])
from playwright.sync_api import sync_playwright
JS = r"""(d => { const day = shipDay(d), out = {}; let rec = 0;
  for (const [id, plan] of day.plans) { out[id] = JSON.stringify(plan); rec += plan.filter(s => s.deck === 7 && s.from < 1440 && s.to > 1020).length; }
  return [out, rec]; })"""
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844); res = {}
    for d in range(int(sys.argv[2]), int(sys.argv[3]) + 1): res[d] = g.ev(f'({JS})({d})')
    g.close()
json.dump(res, open(sys.argv[4], 'w'))
