# BAL1: the Step 6 story beats for slower careers (lead 42's question): runs career_sim's paper player to DAYS and dumps
# the Tier 4 promotion record (pu.t4), Basil's day, Calder's question, the ending's week, the occasions booked, and the
# Mail by day. Run: python3 balance/story_probe.py BUILD DAYS plan...
import sys, json, pathlib, os
HERE = pathlib.Path(__file__).resolve().parent
sys.argv_ = sys.argv; import importlib.util
spec = importlib.util.spec_from_file_location('cs', HERE / 'career_sim.py'); cs = importlib.util.module_from_spec(spec)
sys.argv = [sys.argv_[0], sys.argv_[1]]; spec.loader.exec_module(cs); sys.argv = sys.argv_
from playwright.sync_api import sync_playwright
DUMP = r"""(() => { const W = SHIP.works || {}, d = x => x == null ? null : Math.floor(x / 1440) + 1, hm = x => x == null ? null : hhmm(x % 1440);
  return { t4: W.pu ? JSON.parse(JSON.stringify(W.pu.t4 || null)) : null, mt: W.mt || null, end: W.end || null, home: W.home, tr: W.tr,
    endWeek: typeof endWeek === 'function' ? endWeek() : null, endState: SHIP.end ? JSON.parse(JSON.stringify(SHIP.end)) : null,
    occ: SHIP.occasions.map(r => [r.id, d(r.at), hm(r.at), r.status || null, !!r.met]),
    mail: (SHIP.mail || []).map(m => [d(m.t != null ? m.t : m.at), (m.from || '') + ': ' + String(m.subject || m.title || m.text || '').slice(0, 90)]) }; })()"""
if __name__ == '__main__':
    path, days, plans = sys.argv[1], int(sys.argv[2]), sys.argv[3:]
    with sync_playwright() as pw:
        g = cs.Game(pw, path); ev = g.ev
        ev("if (typeof GUIDE_ON !== 'undefined' && GUIDE_ON) { GUIDE.tq.length = 0; guideToast = () => false; }")
        S = cs.build(cs.SUM)
        for plan in plans:
            ev("SHIP.end = null")
            r = ev(f"({S})({{ plan: '{plan}', days: {days}, t2: 'real' }})")
            x = ev(DUMP)
            (HERE / 'data' / f'story_{plan}.json').write_text(json.dumps(x, indent=1))
            print('==', plan, 't4', x['t4'], '\n  mt', x['mt'], '\n  end', x['end'], '\n  endWeek', x['endWeek'], 'home', x['home'])
            print('  occasions:', [o for o in x['occ'] if o[1] and o[1] >= 20])
            print('  mail >= Day 20:'); [print('   ', m) for m in x['mail'] if m[0] and m[0] >= 20]
        print('errors', g.errors[:3])
