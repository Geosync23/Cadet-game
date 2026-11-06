import sys
exec(open("/home/user/Cadet-game/cadet_test.py").read().split("a, shots = run(")[0])
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1]); g.step(2)
    print(g.ev("""(() => {
      const t0 = (SHIP_START.day - 1) * 1440 + SHIP_START.min, log = [], seen = {};
      JOBS_ON = true; MACH_HOUR = null; MACH_SEEN = -1; SHIP.galley = null; setShipNow(t0); machinesNow(); galleyAdvance(t0);
      for (let t = t0 + 1440; t <= t0 + 7 * 1440; t += 10) {
        setShipNow(t); galleyAdvance(t); machinesNow();
        for (const j of SHIP.jobs) if (j.cargo === 'meals') { const k = j.id + j.status + (j.claimedBy || ''); if (!seen[k]) { seen[k] = 1; log.push('D' + SHIP.time.day + ' ' + hhmm(t % 1440) + ' ' + j.id + ' ' + j.status + ' ' + (j.claimedBy || '') + ' leaveEnd ' + hhmm(leaveEnd(j) % 1440) + ' cold ' + Math.round(SHIP.galley.cold.meals)); } }
      }
      setShipNow(t0); SHIP.galley = null; return log.join('\\n'); })()"""))
    g.close()
