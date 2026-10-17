import sys
exec(open('cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1]); ev = g.ev
    # the miss refund when the sick roll lands after a miss was counted (a skip past 12:30 in one go)
    print('refund:', ev("""(() => { const at = (d, m) => { SHIP.time.day = d; SHIP.time.min = m; return (d - 1) * 1440 + m; };
      SHIP.career = null; SHIP.rep = null; repInit(); SHIP.rep.ship.work = 30; careerTick(at(50, 600)); const c = SHIP.career; c.sd = 0;
      const w0 = careerWork(); careerMissed(50); const w1 = careerWork(); careerSick(50); return { before: w0, afterMiss: w1, afterSick: careerWork() }; })()"""))
    # the same sick days in every game?
    print('first sick days, fresh game:', ev("""(() => { const out = []; SHIP.career = null; careerInit((0) * 1440 + 360); const c = SHIP.career; for (let d = 1; d <= 200; d++) if (sickDue(d)) { out.push(d); c.sd = d; } return out; })()"""))
    # walking speed when unwell and tired
    print('worst walk:', ev("""(() => { const at = (d, m) => { SHIP.time.day = d; SHIP.time.min = m; return (d - 1) * 1440 + m; };
      SHIP.career = null; careerInit(at(51, 200)); const c = SHIP.career; c.sd = 51; c.sh = 0; at(51, 900); const n = SHIP.player.needs, e0 = { ...n };
      n.energy = 10; n.fitness = 10; const w = needEffects().walk; Object.assign(n, e0); return Math.round(w * 100) / 100; })()"""))
    for e in g.errors: print('page error', e)
    g.close()
