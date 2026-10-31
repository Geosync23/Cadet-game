# RV28: stage 1's planner hook (storyCastGoes, read by section 18's evArrive) in two builds, switch as built.
# Prints storyCastGoes for Kovac at the Captain's address on Days 19 and 26, and her Day 19 / 26 plan around 15:00-16:30.
import sys, os, types, json
os.environ.setdefault('CADET_CHROME', '/opt/pw-browsers/chromium')
from playwright.sync_api import sync_playwright
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../cadet_test.py')).read(); src = src[:src.index('import sys, json, hashlib')]
ct = types.ModuleType('ct'); exec(src, ct.__dict__)
JS = r"""(() => { socInit(); const p = socP('kovac-zainab'); const out = { on: STORIES_ON, on2: typeof STORIES2_ON !== 'undefined' ? STORIES2_ON : null };
  for (const d of [19, 26]) { out['goes' + d] = storyCastGoes('captains-address', 'kovac-zainab', d);
    out['plan' + d] = planDay(p, d).filter(s => s.to > 900 && s.from < 1020 + 1440 * 0 + (d - 1) * 1440 * 0 + 99999).map(s => [hhmm(((s.from % 1440) + 1440) % 1440), hhmm(((s.to % 1440) + 1440) % 1440), s.act, s.tag || '', s.deck]).filter(r => r[0] >= '14:30' && r[0] <= '17:00'); }
  return out; })()"""
with sync_playwright() as pw:
    for f in sys.argv[1:]:
        g = ct.Game(pw, f)
        print(f[-60:]); print(json.dumps(g.ev(JS))[:3000]); print('errors', g.errors[:3]); g.close()
