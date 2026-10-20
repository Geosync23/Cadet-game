import sys, os, json
os.environ.setdefault('CADET_CHROME','/opt/pw-browsers/chromium')
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1], 390, 844); g.step(3)
    r = g.ev(r"""(() => {
      skipTo(2 * 1440 + 15 * 60 + 40);               // Day 3, Wednesday 15:40
      const now = shipNow(), d = SHIP.time.day, ppl = ROSTER.filter(p => p.id);
      const snap = () => { const o = {}; for (const p of ppl) { const pl = planDay(p, d) || []; o[p.id] = { past: JSON.stringify(pl.filter(s => s.to <= now)), now: JSON.stringify(whereIs(p, now)), eve: JSON.stringify(pl.filter(s => s.from >= now)) }; } return o; };
      const a = snap();
      // what DP1's hook would do: a Dev-list tradition today (film-like, in 20 minutes), then today's plans made again (eventOneOff's path)
      SHIP.events.oneOffs.push({ id: 'dr1-test', name: 'Test night', day: d, at: [now % 1440 + 20, now % 1440 + 140], where: [{ deck: 3, room: 'Bow lounge', types: ['lounge-seat'] }], chance: .6 });
      SCHED_DATA = null; EV_DAYS.clear(); for (const k of [...SHIP_DAYS.keys()]) if (k >= d) SHIP_DAYS.delete(k);
      const b = snap();
      let past = 0, nowc = 0, eve = 0; const ex = [];
      for (const id in a) { if (a[id].past !== b[id].past) { past++; if (ex.length < 3) ex.push([id, a[id].past.slice(-300), b[id].past.slice(-300)]); } if (a[id].now !== b[id].now) nowc++; if (a[id].eve !== b[id].eve) eve++; }
      return { clock: clockText(), crew: ppl.length, pastChanged: past, whereNowChanged: nowc, eveningChanged: eve, ex, going: eventsOn(d).filter(e => e.id === 'dr1-test').length };
    })()""")
    print(json.dumps(r, indent=1)[:3000]); print(g.errors[:3]); g.close()
