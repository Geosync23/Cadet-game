# Starship Cadet: how often head-scratcher cases come (FX30 for lead 49, backlog JB2-3, 0.99.6; a measurement, not a check)
# On each build given, in the real game (the real crew doing their jobs, the real machines wearing), Days 5-40 (or to CASE_TO) an hour
# at a time: the player promoted on the plan's days (junior to Day 9, officer to 15, senior to 22, then specialist) and
# each head-scratcher kind's ladder row counted open from its plan day; the staged first cases left out (they're the
# training, not the roll); each row's tool given on its plan day and the row trained by the next day (a diligent player). A case posted is taken as solved 3 ship hours later (its job done), so the open limit holds
# about as it would in play. Prints, per build: repairs offered to the case engine, rolled, posted, fallbacks, and the
# cases per ship week and per rank. Nothing is changed in the game.
# Run:  [CASE_TO=61] python3 caserate_probe.py BUILD.html [BUILD2.html ...]
import sys, json
exec(open(__file__.replace('caserate_probe.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
import os
END = int(os.environ.get('CASE_TO', '40'))   # the last ship day (CASE_TO=61: eight weeks)

RUN = r"""(() => {
  if (!SHIP.works) { if (shipNow() < WORKS_START) setShipNow(WORKS_START); worksInit(); }
  const W = SHIP.works, C = caseState(); C.open = []; C.done = []; C.n = 0; for (const k in CASE_STATS) CASE_STATS[k] = k === 'why' ? {} : 0;
  C.first = 'none'; C.p1 = 'none'; C.p2 = 'none'; for (const k of ['p4', 'p5', 'p9', 'p6', 'p7', 'p8']) flagSet('case.' + k + '.first', 'none');
  const rankOf = d => d < 10 ? 'junior' : d < 16 ? 'officer' : d < 23 ? 'senior' : 'specialist', tierOf = { junior: 1, officer: 2, senior: 3, specialist: 4 };
  const ladders = new Set(Object.values(CASE_KINDS).map(K => K.ladder).filter(Boolean)), rows = CAREER_LADDER.filter(r => ladders.has(r.id));
  const t0 = 4 * 1440 + 360, end = __END * 1440;
  MACH_HOUR = null; MACH_SEEN = -1; setShipNow(t0); machinesNow();
  const out = { cases: [], perRank: {}, perWeek: {}, rows: rows.map(r => r.id + '@' + r.day), eventDays: [] }, seen = new Map();
  for (let t = t0; t <= end; t += 60) {
    const d = Math.floor(t / 1440) + 1; W.rank = rankOf(d); W.tier = tierOf[W.rank];
    for (const r of rows) if (r.day <= d && !worksIsOpen(r.id)) (W.op[r.day] = W.op[r.day] || []).push(r.id);
    for (const r of CAREER_LADDER) if (r.day <= d) { if (r.tool && WORK_TOOLS[r.tool] && !W.tools[r.tool]) W.tools[r.tool] = [r.day, 0]; if (r.day < d && W.tr[r.id] === undefined) W.tr[r.id] = r.day; }   // a diligent player: each row's tool on its day, trained by the next
    if (t % 1440 === 360 && typeof eventDay === 'function' && eventDay(d)) out.eventDays.push(d);
    const before = { ...CASE_STATS }; setShipNow(t); machinesNow();
    const r = out.perRank[W.rank] = out.perRank[W.rank] || { offered: 0, rolled: 0, posted: 0, fallback: 0 };
    for (const k in r) r[k] += CASE_STATS[k] - before[k];
    for (const c of C.open.slice()) {
      if (!seen.has(c.id)) { seen.set(c.id, t); const wk = 'Days ' + (5 + 7 * Math.floor((d - 5) / 7)) + '-' + (11 + 7 * Math.floor((d - 5) / 7));
        out.perWeek[wk] = (out.perWeek[wk] || 0) + 1; out.cases.push([d, Math.floor(t % 1440 / 60), W.rank, c.kind, (caseJob(c) || {}).machine]); }
      else if (seen.get(c.id) <= t - 180) { const j = caseJob(c); caseClose(c, 0); if (j && j.status !== 'done') { delete j.case; jobFinish(j, t, null); } }
    }
  }
  out.stats = { ...CASE_STATS, why: { ...CASE_STATS.why } };
  return out;
})()"""

with sync_playwright() as pw:
    for path in sys.argv[1:]:
        g = Game(pw, path, 390, 844); g.step(3)
        R = g.ev(RUN.replace('__END', str(END)))
        print('==', path)
        print('  case kinds open from:', R['rows'], ' event days (no cases):', R['eventDays'])
        s = R['stats']; print(f"  Days 5-{END}: offered {s['offered']}, rolled {s['rolled']}, posted {s['posted']}, fallback {s['fallback']}  (why {s['why']})")
        print('  per rank:', R['perRank'])
        print('  per week:', R['perWeek'])
        print('  cases:', R['cases'])
        pe = [e for e in g.errors if e.startswith('pageerror')]
        if pe: print('  page errors:', pe[:3])
        g.close()
