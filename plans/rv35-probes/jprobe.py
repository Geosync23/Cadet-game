import sys, json
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
P = r"""(() => machineList().filter(m => /junction/.test(m.id) && panelPlace(m.id)).map(m => [m.id, jobTier({ machine: m.id, tier: 2, stops: [{ placeId: panelPlace(m.id) }] }), (() => { const j = rewJob(m.id, shipNow()); return j ? jobTier(j) : null; })()]))()"""
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844); g.step(3); print(json.dumps(g.ev(P)))
