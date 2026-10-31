# RV28: JB2's fixScanMachine (note 15): which machines can have a pump fault, which a junior may work on, what it returns.
import sys, os, types, json
from playwright.sync_api import sync_playwright
src = open(sys.argv[1] + '/cadet_test.py').read(); src = src[:src.index('import sys, json, hashlib')]
ct = types.ModuleType('ct'); exec(src, ct.__dict__)
JS = r"""(() => { machinesNow(); const pumpKinds = Object.keys(FAULT_CAUSES).filter(k => (FAULT_CAUSES[k] || []).some(c => c.id === 'pump'));
  const all = machineList().filter(m => pumpKinds.includes(m.kind)).map(m => [m.id, m.kind, jobTier({ machine: m.id }), !!panelPlace(m.id), !!m.stub, ENGINE_KINDS.has(m.kind)]);
  const picks = []; for (let d = 6; d <= 30; d++) picks.push(d + ':' + fixScanMachine(d));
  return { tier: playerTier(), pumpKinds, all, picks }; })()"""
with sync_playwright() as pw:
    g = ct.Game(pw, sys.argv[2]); print(json.dumps(g.ev(JS))); print('errors', g.errors[:3]); g.close()
