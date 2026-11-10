# RV35: does the Monday briefing's "a shutdown" raise still book one on Day 22 for Day 23 with TP9991_SD_ON?
import sys, json, pathlib
G = '/home/user/Cadet-game/'
exec(open(G + 'cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
P = r"""(() => { const d = 22; introSkip(); SHIP.works = null; SHIP.jobs = []; setShipNow((d - 1) * 1440 + 510); machinesNow(); const W = worksInit(); W.tier = 3; W.rank = 'senior'; W.tr.m18 = 18;
  const id = jobReserve('6-junction-1', d, 600, 43, { tier: 3 }); sdMark(shipNow()); const j = SHIP.jobs.find(x => x.id === id); j.shut = true; j.status = 'waiting';
  const pre = { shut: !!j.shut, status: j.status, held: heldForYou(j), sdDay: j.sdDay };
  const said = m21Raise(0, shipNow()); const b = (sdData().book || []).find(x => x.job === id);
  return { pre, said, booked: b ? { day: b.day, at: b.at } : null, on: typeof TP9991_SD_ON !== 'undefined' && TP9991_SD_ON }; })()"""
for path in sys.argv[1:]:
    with sync_playwright() as pw:
        g = Game(pw, path, 390, 844); g.step(3); g.ev('localStorage.clear()')
        print(pathlib.Path(path).name, json.dumps(g.ev(P)))
