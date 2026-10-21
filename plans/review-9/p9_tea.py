# PR9: why Soto and Calder still plan 5-tea-1 on Day 5 13:15/13:30 under Halloran's d5-mug hold (e18844f).
# A new game (intro on); Day 5's occ.res on the tea seats, introPlan for Halloran then and now, the tea corner's plans 12:45-14:00.
import sys, json, os
exec(open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[1])), 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1])
    g.ev('localStorage.clear()'); g.ev('newGameStart(true)'); g.step(5)
    g.page.fill('form input[maxlength="24"]', 'Sam'); g.page.click('form button'); g.step(5)
    r = g.ev("""(() => { const out = {};
      const p = ROSTER.find(q => q.id === 'halloran-emeka'), old = introPlan, log = [];
      introPlan = function (q, d) { let r, err = null; try { r = old.apply(this, arguments); } catch (e) { err = String(e); throw e; } finally { if (q.id === 'halloran-emeka' && d === 5) log.push([err, JSON.stringify(r)]); } return r; };
      for (let d = 1; d <= 5; d++) shipDay(d);
      introPlan = old;
      const day = shipDay(5);
      out.calls = log;
      out.res = ['5-tea-1', '5-tea-2', '5-tea-3'].map(id => [id, (day.occ.res.get(id) || []).map(([x, y, ev]) => [x % 1440, y % 1440, ev])]);
      out.plans = [];
      for (const [id, plan] of day.plans) for (const s of plan) if (/^5-tea/.test(s.placeId || '') && s.to % 1440 > 765 && s.from % 1440 < 840) out.plans.push([id, s.placeId, s.tag, s.from % 1440, s.to % 1440]);
      out.plans.sort((a, b) => a[3] - b[3]);
      return out; })()""")
    print(json.dumps(r, indent=1)); print('page errors', g.errors[:4]); g.close()
