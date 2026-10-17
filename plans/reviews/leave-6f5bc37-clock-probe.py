import sys, json
exec(open('cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
# The time clock (0.61.13-0.61.16) against section 14's shift note and the career's miss count, on paper.
# Each case: a fresh career on a weekday past the grace; what the player does; then shiftTick at 10:00 and careerTick
# to the end of the day. Prints the shiftStart note section 20 scores, and whether the career counted a miss.
CASE = r"""((name, steps) => {
  const at = (d, m) => { SHIP.time.day = d; SHIP.time.min = m; return (d - 1) * 1440 + m; };
  let d = 15; while (weekday(d) !== 1) d++;            // a Tuesday past the grace
  SHIP.career = null; careerTick(at(d - 1, 1439)); const c = SHIP.career; c.sd = 99999; c.e = d - 1; const ms0 = c.ms;
  flagSet('shiftSent', 0); const notes = []; const off = onSim('shiftStart', n => notes.push({ late: n.late, missed: !!n.missed }));
  for (const [m, what] of steps) { at(d, m); if (what === 'in' || what === 'out') careerClock(at(d, m)); if (what === 'repair') simNote('repair', { who: 'you', t: at(d, m), machine: null }); shiftTick(); careerTick(at(d, m)); }
  for (const m of [600, 610, 750, 1100, 1439]) { at(d, m); shiftTick(); careerTick(at(d, m)); }
  if (typeof off === 'function') off();
  return JSON.stringify({ name, note: notes[0] || null, careerMiss: c.ms - ms0, ci: c.ci % 1440, co: c.co % 1440 });
})"""
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1]); ev = g.ev
    for name, steps in [('in 07:55', [(475, 'in')]), ('in 09:30', [(570, 'in')]), ('in 10:30', [(630, 'in')]),
                        ('in 12:00', [(720, 'in')]), ('in 03:00', [(180, 'in')]), ('in 07:01, out 07:02', [(421, 'in'), (422, 'out')]),
                        ('no clock, a repair at 09:00', [(540, 'repair')]), ('nothing', [])]:
        print(ev(CASE + f"({json.dumps(name)}, {json.dumps(steps)})"))
    for e in g.errors: print('page error', e)
    g.close()
