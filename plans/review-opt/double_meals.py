# OR2: every crew member's plan, Days A..B: meals planned as two separate runs (a second dinner or breakfast)
import sys
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("import sys, json, hashlib")[0])
from playwright.sync_api import sync_playwright
A, B = int(sys.argv[2]), int(sys.argv[3])
JS = r"""(d => { const out = [], day = shipDay(d);
  for (const [id, plan] of day.plans) for (const m of ['breakfast', 'dinner']) {
    let runs = 0, last = -1e9, tags = [];   // a run of that meal's segments; a gap under 10 minutes (a walk to the seat) is the same meal
    for (const s of plan) if (s.act === m) { if (s.from - last >= 10) { runs++; tags.push((s.tag || '-') + '@' + Math.round(s.from)); } last = s.to; }
    if (runs > 1) out.push(id + ' ' + m + ' ' + runs + ' ' + tags.join(','));
  }
  return [day.plans.size, out]; })"""
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844); tot = 0
    print('keys', g.ev('JSON.stringify(Object.keys(shipDay(1).plans.values().next().value[0]))'))
    for d in range(A, B + 1):
        n, out = g.ev(f'({JS})({d})'); tot += len(out)
        print(d, n, len(out), out[:6], flush=True)
    g.close()
print('DOUBLE MEALS', tot)
