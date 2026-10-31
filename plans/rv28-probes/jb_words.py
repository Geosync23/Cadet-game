# RV28: SW4's tour words (7e30feb, baked in a scratch copy): does the tour read them? (stand-in vs baked)
import sys, os, types, json
from playwright.sync_api import sync_playwright
src = open(sys.argv[1] + '/cadet_test.py').read(); src = src[:src.index('import sys, json, hashlib')]
ct = types.ModuleType('ct'); exec(src, ct.__dict__)
JS = r"""(() => { const out = {}; const tour = checkTour(3); out.tour = tour.map(id => [id, roundSpot(id).name, roundSign(id, 3).slice(0, 90)]);
  for (const s of ['take', 'go', 'look', 'mark', 'next', 'done']) out['tip.' + s] = (typeof careerText === 'function' && careerText('tip.tour.' + s)) || null;
  out.title = roundText('round.title.tour', 'STANDIN'); out.ask = roundText('round.tour.ask', 'STANDIN'); out.checked = roundText('round.tour.checked', 'STANDIN');
  out.read = ['healthy', 'worn', 'faulty'].map(st => worksText('round.read.' + st, 'STANDIN'));
  out.standins = CHECK_ROWS.filter(s => { const [id, , , , r] = s.split('|'); return worksText('round.check.' + id, 'STANDIN') === 'STANDIN'; }).length;
  out.meet = (MEETING_SCRIPTS['train.m1.torres-zeke.tour'] || {}).lines ? MEETING_SCRIPTS['train.m1.torres-zeke.tour'].lines.length : null;
  return out; })()"""
with sync_playwright() as pw:
    g = ct.Game(pw, sys.argv[2]); print(json.dumps(g.ev(JS), indent=0)[:3500]); print('errors', g.errors[:3]); g.close()
