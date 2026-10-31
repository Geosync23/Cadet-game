# RV29: JB2 F1: the scanner's first job (fixScanTick's jobReserve with tier 2) for a Tier 1 player: on the board, takeable, minutes.
import sys, json, types
from playwright.sync_api import sync_playwright
src = open(sys.argv[1] + '/cadet_test.py').read(); src = src[:src.index('import sys, json, hashlib')]
ct = types.ModuleType('ct'); exec(src, ct.__dict__)
JS = r"""(() => { const out = []; for (const d of [6, 9, 14, 17]) { SHIP.jobs = SHIP.jobs.filter(j => !j.claimedBy); for (const j of SHIP.jobs) if (j.claimedBy === 'you') j.claimedBy = null;
  setShipNow((d - 1) * 1440 + FIX_SCAN_AT + 1); machinesNow();
  const id = jobReserve(fixScanMachine(d), d, FIX_SCAN_AT, FIX_SCAN_SLOT, { cause: 'pump', tier: 2, until: (d - 1) * 1440 + dayShiftEnd(d) });
  const j = SHIP.jobs.find(x => x.id === id), row = openJobs('you').find(o => o.id === id);
  const took = claimJob(id), mins = jobMins(j), mk = makeMins(j);
  out.push({ jm: j.makeMins, mk: j.make, parts: j.parts, d, id, tier: playerTier(), jobTier: jobTier(j), onBoard: !!row, boardMins: row && row.mins, took, work: Math.round(mins), make: mk, cause: (faultCause(j) || {}).id || j.cause || null });
  if (took) { j.claimedBy = null; j.status = 'open'; } }
  return out; })()"""
with sync_playwright() as pw:
    g = ct.Game(pw, sys.argv[2]); print(json.dumps(g.ev(JS))); print('errors', g.errors[:3]); g.close()
