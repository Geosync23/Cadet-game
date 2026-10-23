# RV10 probe: FX5's Day 0 trickle on paper. Day 0's plans before and after a live goodnight at 18:40: who changes,
# whether anything before 18:40 changes (a jump at the re-plan), and the long table's seated count every 5 minutes
import sys, os, re, pathlib, json
GAME, CT = sys.argv[1], sys.argv[2]; FREE = int(sys.argv[3]) if len(sys.argv) > 3 else 1120
exec(open(CT + '/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    g = Game(pw, GAME, 390, 844); g.step(3)
    g.ev("localStorage.clear()"); g.ev("newGameStart(true)"); g.step(5)
    try: g.page.fill('form input[maxlength="24"]', 'Sam'); g.page.click('form button'); g.step(5)
    except Exception as e: print('sign:', str(e)[:80])
    r = g.ev("""(FREE => {
      const B = -1440, snap = () => { const o = {}; for (const [id, s] of shipDay(0).plans) o[id] = JSON.stringify(s.map(x => [x.from, x.to, x.placeId || null, x.act || null, x.tag || null])); return o; };
      const table = segsOf => { const out = []; for (let m = 1080; m <= 1260; m += 5) { let n = 0; for (const [id, s] of shipDay(0).plans) if (s.some(x => /^ev-sunday-table/.test(x.tag || '') || x.kept) && s.some(x => x.placeId && /^3-mess/.test(x.placeId) && x.from <= B + m && B + m < x.to && (x.tag && /^ev-sunday-table/.test(x.tag) || x.kept || x.act === 'dinner'))) n++; out.push([String(Math.floor(m / 60)).padStart(2, '0') + ':' + String(m % 60).padStart(2, '0'), n]); } return out; };
      const on = introOn(), had = SHIP.intro.done.free; delete SHIP.intro.done.free;
      const A = snap(), tA = table();
      SHIP.intro.done.free = B + FREE; const Bp = snap(), tB = table();
      const diners = new Set(), changed = [], early = [];
      for (const [id, s] of shipDay(0).plans) if (s.some(x => /^ev-sunday-table/.test(x.tag || ''))) diners.add(id);
      for (const id in Bp) if (Bp[id] !== A[id]) { changed.push(id); const a = JSON.parse(A[id] || '[]'), b = JSON.parse(Bp[id]); const pre = s => JSON.stringify(s.filter(x => x[0] < B + FREE).map(x => [x[0], Math.min(x[1], B + FREE), x[2]])); if (pre(a) !== pre(b)) early.push(id); }
      // again, the same minute: the same plans (a reload plans the same)
      SHIP_DAYS.clear(); EV_DAY.clear(); const C = snap(); const same = Object.keys(C).every(k => C[k] === Bp[k]);
      if (had === undefined) delete SHIP.intro.done.free; else SHIP.intro.done.free = had;
      const det = {}; for (const id of early.slice(0, 6)) { const a = JSON.parse(A[id]), b = JSON.parse(Bp[id]), f = x => [((x[0] - B) / 60).toFixed(2), ((x[1] - B) / 60).toFixed(2), x[2], x[3], x[4]]; det[id] = { before: a.filter(x => x[0] < B + FREE + 30 && x[1] > B + 900).map(f), after: b.filter(x => x[0] < B + FREE + 30 && x[1] > B + 900).map(f) }; }
      return { det, on, people: Object.keys(A).length, diners: diners.size, changed: changed.length, changedNotDiners: changed.filter(k => !diners.has(k)), earlyChanged: early, samePlanAgain: same, tableNoGoodnight: tA, tableLive: tB };
    })(__FREE__)""".replace("__FREE__", str(FREE)))
    print(json.dumps(r))
    g.close()
