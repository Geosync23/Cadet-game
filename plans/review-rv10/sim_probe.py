# RV10 probe: FX8's day0-sim. With the live goodnight at FREE: non-diners changed, diners' plans changed before they stand,
# what each diner does first after the table, any place held by two people at once (all places), gaps, the same twice,
# and how long shipDay(0) takes to build with and without the live minute
import sys, os, re, pathlib, json
GAME, CT = sys.argv[1], sys.argv[2]; FREE = int(sys.argv[3]) if len(sys.argv) > 3 else 1120
exec(open(CT + '/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    g = Game(pw, GAME, 390, 844); g.step(3)
    g.ev("localStorage.clear()"); g.ev("newGameStart(true)"); g.step(5)
    try: g.page.fill('form input[maxlength="24"]', 'Sam'); g.page.click('form button'); g.step(5)
    except Exception as e: print('sign:', str(e)[:80])
    r = g.ev("""(FREE => { const B = -1440;
      const snap = () => { const o = {}; for (const [id, s] of shipDay(0).plans) o[id] = s.map(x => [x.from, x.to, x.placeId || null, x.act || null, x.type || null]); return o; };
      const time = () => { SHIP_DAYS.clear(); EV_DAY.clear(); const t0 = performance.now(); shipDay(0); return Math.round(performance.now() - t0); };
      delete SHIP.intro.done.free; const tA = time(); const A = snap();
      SHIP.intro.done.free = B + FREE; const tB = time(); const Bp = snap(); const P = shipDay(0).plans;
      SHIP_DAYS.clear(); EV_DAY.clear(); const C = snap(); const same = JSON.stringify(C) === JSON.stringify(Bp);
      const diners = []; for (const [id, s] of P) if (s.some(x => /^ev-sunday-table/.test(x.tag || ''))) diners.push(id);
      const others = Object.keys(Bp).filter(k => JSON.stringify(Bp[k]) !== JSON.stringify(A[k]) && !diners.includes(k));
      const first = {}, early = [], upAt = [];
      for (const id of diners) { const s = P.get(id), i = s.findIndex(x => /^ev-sunday-table/.test(x.tag || '')); let k = i; while (s[k + 1] && s[k + 1].placeId === s[i].placeId) k++;
        const up = s[k].to; upAt.push(Math.round(up - B - FREE)); const n = s[k + 1]; const key = n ? (n.act + ':' + (n.type || (n.placeId || '').replace(/-\\d+$/, ''))) : 'none'; first[key] = (first[key] || 0) + 1;
        const pre = L => JSON.stringify(L.filter(x => x[0] < up - 2).map(x => [x[0], Math.min(x[1], up - 2), x[2]])); if (pre(A[id]) !== pre(Bp[id])) early.push(id); }
      const hold = new Map(), dbl = [];
      for (const [id, s] of P) for (const x of s) if (x.placeId && x.to > x.from) { const L = hold.get(x.placeId) || []; for (const [y0, y1, who] of L) if (who !== id && y0 < x.to - .01 && x.from < y1 - .01) dbl.push([x.placeId, who, id, Math.round(Math.max(y0, x.from) - B)]); L.push([x.from, x.to, id]); hold.set(x.placeId, L); }
      let gaps = 0, zero = 0; for (const id of diners) { const s = P.get(id); for (let q = 1; q < s.length; q++) { if (Math.abs(s[q].from - s[q - 1].to) > .5) gaps++; } for (const x of s) if (!(x.to > x.from)) zero++; }
      const dblOld = []; { const h2 = new Map(); for (const id in A) for (const x of A[id]) if (x[2] && x[1] > x[0]) { const L = h2.get(x[2]) || []; for (const [y0, y1, who] of L) if (who !== id && y0 < x[1] - .01 && x[0] < y1 - .01) dblOld.push(x[2]); L.push([x[0], x[1], id]); h2.set(x[2], L); } }
      const key = d => d[0] + '|' + [d[1], d[2]].sort().join('+');
      const plain = new Set(); { const h2 = new Map(); for (const id in A) for (const x of A[id]) if (x[2] && x[1] > x[0]) { const L = h2.get(x[2]) || []; for (const [y0, y1, who] of L) if (who !== id && y0 < x[1] - .01 && x[0] < y1 - .01) plain.add(x[2] + '|' + [who, id].sort().join('+')); L.push([x[0], x[1], id]); h2.set(x[2], L); } }
      const newDbl = dbl.filter(d => !plain.has(key(d)) && (diners.includes(d[1]) || diners.includes(d[2])));
      return { newDblWithDiners: newDbl.slice(0, 6), nNew: newDbl.length, msPlain: tA, msLive: tB, diners: diners.length, others, earlyChanged: early, firstAfter: first, upMinutesAfter: [Math.min(...upAt), Math.max(...upAt)], doubleBooked: dbl.slice(0, 6), nDouble: dbl.length, nDoubleWithoutLive: dblOld.length, gaps, zero, sameTwice: same };
    })(__F__)""".replace('__F__', str(FREE)))
    print(json.dumps(r)); g.close()
