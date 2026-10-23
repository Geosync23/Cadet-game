# RV10 probe: FX5's day0-stay. With the live goodnight at FREE: non-diners changed, what each diner does after the table,
# and any Deck 3 lounge seat or bench held by two people at once
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
      const snap = () => { const o = {}; for (const [id, s] of shipDay(0).plans) o[id] = JSON.stringify(s.map(x => [x.from, x.to, x.placeId || null, x.act || null])); return o; };
      delete SHIP.intro.done.free; const A = snap();
      SHIP.intro.done.free = B + FREE; const P = shipDay(0).plans, Bp = snap();
      const diners = []; for (const [id, s] of P) if (s.some(x => /^ev-sunday-table/.test(x.tag || ''))) diners.push(id);
      const others = Object.keys(Bp).filter(k => Bp[k] !== A[k] && !diners.includes(k));
      const after = { bunk: 0, lounge: 0, bench: 0, about: 0, mess: 0, deck3bunk: 0, unchanged: 0 }, waits = [];
      for (const id of diners) { const s = P.get(id), i = s.findIndex(x => /^ev-sunday-table/.test(x.tag || '')); let k = i; while (s[k + 1] && s[k + 1].placeId === s[i].placeId) k++; const n = s[k + 1];
        if (Bp[id] === A[id]) { after.unchanged++; continue; }
        if (!n) continue; if (n.act === 'commute') after.bunk++; else if (n.type === 'bed') after.deck3bunk++; else if (n.type === 'lounge-seat') after.lounge++; else if (n.type === 'bench') after.bench++; else if (n.act === 'off' && n.to - n.from >= 60) after.about++; else after.mess++;
        waits.push(Math.round(n ? (n.act === 'commute' ? s[k + 3].to - n.from : n.to - n.from) : 0)); }
      const hold = new Map(), dbl = [];
      for (const [id, s] of P) for (const x of s) if (x.placeId && /^3-(lounge|bench)/.test(x.placeId)) { const L = hold.get(x.placeId) || []; for (const [y0, y1, who] of L) if (who !== id && y0 < x.to && x.from < y1) dbl.push([x.placeId, who, id, Math.round(Math.max(y0, x.from) - B)]); L.push([x.from, x.to, id]); hold.set(x.placeId, L); }
      let gaps = 0; for (const id of diners) { const s = P.get(id); for (let q = 1; q < s.length; q++) if (Math.abs(s[q].from - s[q - 1].to) > .5) gaps++; }
      return { diners: diners.length, others, after, bunkWaits: waits, doubleBooked: dbl.slice(0, 8), nDouble: dbl.length, gaps };
    })(__F__)""".replace('__F__', str(FREE)))
    print(json.dumps(r)); g.close()
