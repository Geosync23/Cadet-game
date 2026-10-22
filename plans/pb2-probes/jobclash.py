# PB2's job-booking scan (backlog PB2-3): fast-forwards the machines on paper, Days 1-60, hour by hour (machinesNow),
# and lists every place two different jobs book at overlapping times (the crew's job walks: segs / segsBy).
# Run from the repo:  CADET_CHROME=/opt/pw-browsers/chromium python3 plans/pb2-probes/jobclash.py BUILD.html     (prints [] when clear)
import sys, json
exec(open(__file__.replace('plans/pb2-probes/jobclash.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1])
    print(json.dumps(g.ev(r"""(() => { const seen = new Map();
      for (let h = 0; h < 60 * 24; h++) { setShipNow(h * 60 + 30); machinesNow();
        const segs = [];
        for (const j of SHIP.jobs) { if (j.status === 'done' && !j.segs && !j.segsBy) continue; const all = j.segsBy ? Object.entries(j.segsBy).flatMap(([c, ss]) => ss.map(s => [c, s])) : (j.segs || []).map(s => [j.claimedBy, s]);
          for (const [c, s] of all) if (s.placeId && s.act !== 'commute') segs.push([j.id, c, s]); }
        for (let a = 0; a < segs.length; a++) for (let b = a + 1; b < segs.length; b++) { const [ja, ca, x] = segs[a], [jb, cb, y] = segs[b];
          if (ja !== jb && ca !== cb && x.placeId === y.placeId && x.from < y.to && y.from < x.to) { const k = x.placeId + ' ' + ja + '/' + jb; if (!seen.has(k)) seen.set(k, 'day ' + (Math.floor(Math.max(x.from, y.from) / 1440) + 1) + ' ' + hhmm(Math.max(x.from, y.from) % 1440) + ' ' + k + ' (' + ca + '/' + cb + ')'); } }
      } return [...seen.values()]; })()"""), indent=0))
    g.close()
