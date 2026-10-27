# BAL1 balance research: the Works career on paper for several player styles, Days 1..N.
# Built on career_check.py's own paper run (its PAPER/SUM text and s6_src, read from the file, never edited),
# with a time budget per shift hour (each job: its minutes + 20 walking, +60 if a part must be made), and
# extra per-day records: xp, band, tier, jobs, minutes worked, credits earned (JOB_PAY a job), ship meters.
# Run: python3 balance/career_sim.py BUILD.html DAYS plan [plan...]  -> balance/data/career_<plan>.json
import sys, json, os, pathlib, re
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parent
src = (ROOT / 'career_check.py').read_text()
pre = src.split('with sync_playwright() as pw:')[0]
pre = pre.replace("exec(open(__file__.replace('career_check.py', 'cadet_test.py')).read()", "exec(open(str(ROOT / 'cadet_test.py')).read()")
sys_argv = sys.argv; sys.argv = [str(ROOT / 'career_check.py'), sys_argv[1]]
exec(pre)
sys.argv = sys_argv
PLAYERS = r"""
      if (['quick', 'relaxed', 'half', 'slacker', 'skipper'].includes(plan)) {
        const skip = (plan === 'slacker' && work && (wd === 0 || wd === 4) && d >= 3) || (plan === 'skipper' && work && d >= 3 && d % 3 === 0);   // the slacker misses Mondays and Fridays (from Day 3)
        if (skip && h === 13 && !__miss[d]) { __miss[d] = 1; if (typeof careerInit === 'function') careerInit(); careerMissed(d); }
        if (plan === 'slacker' && h === 22 && typeof careerDayEnd === 'function') { const c = careerInit(); if (!skip && work) { c.on = d; } try { careerDayEnd(d, t); } catch (e) {} }
        if (shift && !skip) {
          const per = plan === 'quick' ? 60 : plan === 'half' ? 30 : plan === 'skipper' ? 55 : 45;
          __budget = Math.min(__budget, 60) + per;
          for (let k = 0; k < 6 && __budget > 0 && !myJob(); k++) {
            const x = openJobs('you').filter(j => !leave(j))[0]; if (!x) { __idle += Math.max(0, __budget); __budget = 0; break; }
            const cost = (x.mins || 30) + 20 + (x.parts && x.parts.length && !(typeof partStock === 'function') ? 0 : 0);
            if (doJob(x.id)) { jobs++; __mins += cost; __budget -= cost; __kinds[x.kind] = (__kinds[x.kind] || 0) + 1; if (!firstJob) firstJob = d; } else break;
          }
        }
      }
"""
def build(SUM):
    S = s6_src(SUM)
    anchor = "      if (plan === 'steady' && shift && !myJob())"
    assert anchor in S
    S = S.replace(anchor, PLAYERS + anchor, 1)
    S = S.replace("  const lazySkip = new Set();", "  const lazySkip = new Set(); const __miss = {}; let __budget = 0, __mins = 0, __idle = 0, __kinds = {};", 1)
    S = S.replace("    days_.push({ tier:", "    days_.push({ mins: __mins, idle: __idle, kinds: JSON.stringify(__kinds), meters: typeof shipMeters === 'function' ? shipMeters() : null, career: SHIP.career ? { st: SHIP.career.st, n: SHIP.career.n, go: SHIP.career.go, ms: SHIP.career.ms, work: typeof careerWork === 'function' ? Math.round(careerWork()) : null } : null, health: typeof shipHealth === 'function' ? shipHealth() : null, srep: SHIP.rep && SHIP.rep.ship ? JSON.parse(JSON.stringify(SHIP.rep.ship)) : null, tier:", 1)
    S = S.replace("    let jobs = 0, used = [];", "    let jobs = 0, used = []; __mins = 0; __idle = 0; __kinds = {};", 1)
    return S

if __name__ == '__main__':
    path, days, plans = sys.argv[1], int(sys.argv[2]), sys.argv[3:]
    with sync_playwright() as pw:
        g = Game(pw, path); ev = g.ev
        ev("if (typeof GUIDE_ON !== 'undefined' && GUIDE_ON) { GUIDE.tq.length = 0; guideToast = () => false; }")
        S = build(SUM)
        if os.environ.get('BANDS3'): ev(f"WORK_BANDS[3] = {os.environ['BANDS3']}"); print('what-if: WORK_BANDS[3] =', os.environ['BANDS3'])
        tag = os.environ.get('TAG', '')
        pay = ev("JOB_PAY")
        for plan in plans:
            r = ev(f"({S})({{ plan: '{plan}', days: {days}, t2: 'real' }})")
            out = {'plan': plan, 'pay': pay, 'trained': r['trained'], 'promo': r['promo'], 'days': r['days'], 'mail': r['mail'][:80], 'errors': g.errors[:5]}
            (HERE / 'data' / f'career_{plan}{tag}.json').write_text(json.dumps(out, indent=1))
            print(plan, ' '.join(f"D{x['d']}:T{x['tier']}/{x['xp']}/{x['band']}/{x['jobs']}j" for x in r['days']), flush=True)
        print('errors', g.errors[:3])
