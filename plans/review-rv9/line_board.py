import sys, json
exec(open('cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
J = r"""(() => {
  const t0 = (SHIP_START.day - 1) * 1440 + SHIP_START.min; JOBS_ON = true; MACH_HOUR = null; MACH_SEEN = -1;
  const out = {}, seen = new Set();
  for (let t = t0; t < t0 + 7 * 1440; t += 60) { setShipNow(t); machinesNow(); const d = SHIP.time.day, h = Math.floor(SHIP.time.min / 60);
    const o = out[d] = out[d] || { kinds: {}, shiftHoursWithJob: 0, newJobs: 0 };
    const js = openJobs(); if (h >= 9 && h < 17 && js.length) o.shiftHoursWithJob++;
    for (const x of js) { if (!seen.has(x.id)) { seen.add(x.id); o.newJobs++; o.kinds[x.kind] = (o.kinds[x.kind] || 0) + 1; } } }
  return { norm: typeof MACH_NORM !== 'undefined' ? MACH_NORM : null, days: out };
})()"""
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1]); r = g.ev(J); g.close()
    n = r['norm']; print(sys.argv[1], 'machNorm sample', (json.dumps(n)[:160] if n is not None else None))
    for d, o in r['days'].items(): print('  day', d, 'shift hours with a job you could take', o['shiftHoursWithJob'], '/ 8; new', o['newJobs'], o['kinds'])
