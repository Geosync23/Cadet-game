# reviewer 1d probe for claude/leave: rotas, casual-late, old-save upgrade, the q overwrite, summons on leave, New game from the card
import sys, json
exec(open('cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1]); ev = g.ev
    print('rotas (days 8-35 off-shift):', ev("""(() => { const o = {}; for (const id of ['calder','marrow','torres-zeke','pell']) { o[id] = []; for (let d = 8; d <= 35; d++) if (!occOnShift(id, d)) o[id].push(d); } return o; })()"""))
    # casual-late: 40 min late every workday, k jobs a day, never misses; 16 weeks
    for jobs in (0, 1):
        r = ev("""((jobs) => { SHIP.career = null; SHIP.rep = null; SHIP.occasions.length = 0; SHIP.flags = {}; SHIP.notes = [];
          const at = (d, m) => { SHIP.time.day = d; SHIP.time.min = m; return (d - 1) * 1440 + m; }; const steps = [];
          const off = onSim('careerStep', n => steps.push([n.step, Math.floor(n.t / 1440) + 1])); let lo = 99, wk = [];
          for (let d = 1; d <= 112; d++) { careerTick(at(d, 0)); if (weekday(d) === 6) { repWeek(Math.floor(at(d, 240) / 60)); careerTick(at(d, 240)); }
            if (playerShiftOn(d)) { at(d, 520); simNote('shiftStart', { late: 40 }); careerTick(at(d, 520)); for (let k = 0; k < jobs; k++) { at(d, 600); repAdd('works', 3, { work: 2 }, 'jobs'); } }
            careerTick(at(d, 750)); careerTick(at(d, 900)); careerTick(at(d, 1439)); lo = Math.min(lo, careerWork()); if (weekday(d) === 4) wk.push(Math.round(careerWork())); }
          off(); return { lo: Math.round(lo * 10) / 10, fridays: wk, steps }; })(""" + str(jobs) + ")")
        print(f'late 40 min every workday, {jobs} job(s) a day:', r)
    # old save upgrade: you started at 08:00 (pre-0.61 build: shiftSent today, a good shiftStart), the save loads at 11:00 with no career, you're on Deck 4
    r = ev("""(() => { SHIP.career = null; SHIP.rep = null; SHIP.occasions.length = 0; SHIP.flags = {}; SHIP.notes = [];
      const at = (d, m) => { SHIP.time.day = d; SHIP.time.min = m; return (d - 1) * 1440 + m; };
      const d = 10; at(d, 480); flagSet('shiftSent', d); simNote('shiftStart', { late: 0 }); SHIP.career = null;   // the old build saw this; then the upgrade
      const w0 = careerWork(); careerTick(at(d, 660)); careerTick(at(d, 750)); careerTick(at(d, 760));
      return { atWork: careerAtWork(), w0, w1: careerWork(), on: SHIP.career.on, e: SHIP.career.e, k: SHIP.career.k }; })()""")
    print('old save loaded at 11:00 after a 08:00 start:', r)
    # the q overwrite: the Chief's step due but not yet booked (Calder off / after 15:00), work falls under 12
    r = ev("""(() => { SHIP.career = null; SHIP.rep = null; SHIP.occasions.length = 0; SHIP.flags = {}; SHIP.notes = [];
      const at = (d, m) => { SHIP.time.day = d; SHIP.time.min = m; return (d - 1) * 1440 + m; }; repInit(); const steps = [];
      const off = onSim('careerStep', n => steps.push([n.step, Math.floor(n.t / 1440) + 1]));
      careerTick(at(15, 960)); const c = SHIP.career; c.e = 15; c.z = 14; c.on = 15;
      SHIP.rep.ship.work = 20; careerTick(at(15, 961)); const a = { st: c.st, q: c.q };   // under 25 at 16:01: due, can't book till tomorrow 07:00
      SHIP.rep.ship.work = 10; careerTick(at(15, 962)); const b = { st: c.st, q: c.q };   // a further fall before 07:00
      for (let d = 16; d <= 60; d++) { careerTick(at(d, 0)); careerTick(at(d, 420)); c.on = 0; careerTick(at(d, 750)); careerTick(at(d, 1000)); SHIP.rep.ship.work = 2; }
      off(); return { a, b, after: { st: c.st, q: c.q, n: c.n, go: c.go }, steps, occ: SHIP.occasions.map(r => r.key) }; })()""")
    print('Chief due, then under 12 before it is booked:', r)
    # a summons booked on your leave day?
    r = ev("""(() => { SHIP.career = null; SHIP.rep = null; SHIP.occasions.length = 0; SHIP.flags = {}; SHIP.notes = [];
      const at = (d, m) => { SHIP.time.day = d; SHIP.time.min = m; return (d - 1) * 1440 + m; }; repInit();
      careerTick(at(15, 1300)); const c = SHIP.career; c.e = 15; c.z = 14; SHIP.rep.ship.work = 20; careerTick(at(15, 1301));   // due at 21:41, Calder books at 07:00
      careerBook(16, at(15, 1302)); careerTick(at(16, 0)); careerTick(at(16, 420));
      return { leave16: careerOn(16), shift16: playerShiftOn(16), occ: SHIP.occasions.map(r => r.key + ' ' + hhmm(r.at % 1440)) }; })()""")
    print('summons on a leave day:', r)
    # the closing card's New game (test URL: NOSAVE)
    r = ev("""(() => { SHIP.career = null; careerInit(); SHIP.career.go = 20; SHIP.career.end = true; careerCard(true);
      const el = document.getElementById('careerEnd'), shown = !el.hidden, z = getComputedStyle(el).zIndex; el.querySelector('button').click();
      const nx = SHIP.time.day; return { shown, z, hiddenAfter: el.hidden, career: SHIP.career, day: SHIP.time.day, min: SHIP.time.min, shiftNextWorkday: playerShiftOn(nx + (weekday(nx) >= 5 ? 7 - weekday(nx) : 0)) }; })()""")
    print('New game from the card:', r)
    for e in g.errors: print('page error', e)
    g.close()
