import sys
exec(open('cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1]); ev = g.ev
    print('repNote wired to shiftStart now?', ev("(() => { SHIP.rep = null; repInit(); simNote('shiftStart', { late: 40 }); return SHIP.rep.ship.work; })()"))
    for jobs in (0, 1):
        r = ev("""((jobs) => { SHIP.career = null; SHIP.rep = null; SHIP.occasions.length = 0; SHIP.flags = {}; SHIP.notes = [];
          const at = (d, m) => { SHIP.time.day = d; SHIP.time.min = m; return (d - 1) * 1440 + m; }; const steps = [];
          const off = onSim('careerStep', n => steps.push([n.step, Math.floor(n.t / 1440) + 1])); let lo = 99, wk = [];
          for (let d = 1; d <= 112; d++) { careerTick(at(d, 0)); if (weekday(d) === 6) { repWeek(Math.floor(at(d, 240) / 60)); careerTick(at(d, 240)); }
            if (playerShiftOn(d)) { at(d, 520); simNote('shiftStart', { late: 40 }); repNote('shiftStart', { late: 40 }); careerTick(at(d, 520)); for (let k = 0; k < jobs; k++) { at(d, 600); repAdd('works', 3, { work: 2 }, 'jobs'); } }
            careerTick(at(d, 750)); careerTick(at(d, 900)); careerTick(at(d, 1439)); lo = Math.min(lo, careerWork()); if (weekday(d) === 4) wk.push(Math.round(careerWork())); }
          off(); return { lo: Math.round(lo * 10) / 10, fridays: wk, steps }; })(""" + str(jobs) + ")")
        print(f'late 40 min every workday (repNote applied), {jobs} job(s) a day:', r)
    g.close()
