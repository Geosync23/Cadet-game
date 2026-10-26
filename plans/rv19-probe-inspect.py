# RV19: live probe of the bunk inspection. python3 plans/rv19-probe-inspect.py GAME.html DAY [bunk]  (OUT=dir for shots; own CADET_WORK)
import sys, os, json
sys.argv = [sys.argv[0]] + sys.argv[1:]
GAME, DAY, MODE = sys.argv[1], int(sys.argv[2]), sys.argv[3] if len(sys.argv) > 3 else 'bunk'
exec(open('/home/user/Cadet-game/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
OUT = os.environ.get('OUT', '.')
with sync_playwright() as pw:
    g = Game(pw, GAME, 390, 844)
    # set up: Day DAY 06:00, the player at their bunk (works open as on a real Day 4)
    print(g.ev(f"""(() => {{ setShipNow(({DAY} - 1) * 1440 + 6 * 60); needsT = null; actEnd(true);
      if (typeof DIALOGUE !== 'undefined' && DIALOGUE) dialogueEnd(true);
      return {{ day: SHIP.time.day, deck: deckDef.num, rank: SHIP.works && SHIP.works.rank, due: inspectDue({DAY}), opened: [...worksOpened(SHIP.works)].join(','), walker: inspectWalker({DAY}), on: INSPECT_ON }}; }})()"""))
    if MODE == 'bunk':
        g.ev("(() => { const s = placeSpot(playerBed()), c = cellPos(...s.walk); player.obj.position.copy(c); player.stop(); })()")
    g.step(3)
    seen = []; last = None; shots = 0
    # bubbles and toasts: hook worksSay and toast
    g.ev("(() => { window.__said = []; const ws = worksSay; worksSay = (id, t) => { window.__said.push([Math.floor(shipNow()) % 1440, 'say', id, t]); return ws(id, t); }; const tt = toast; toast = (a, b) => { window.__said.push([Math.floor(shipNow()) % 1440, 'toast', String(a), String(b || '')]); return tt(a, b); }; })()")
    for i in range(700):
        g.step(10)
        st = g.ev(f"""(() => {{ const m = Math.floor(shipNow()) % 1440, by = inspectOfficer({DAY}), a = DECK_CREW.find(x => x.p && x.p.id === by);
          let room = null; try {{ room = a ? roomAt(...cellAt(a.x, a.z)) : null; }} catch (e) {{}}
          const stand = DECK_CREW.filter(x => x.spot && /-stand$/.test(x.spot.id || '')).length;
          const standAt = DECK_CREW.filter(x => x.spot && /-stand$/.test(x.spot.id || '') && Math.hypot(x.x - placeSpot(x.spot.id).x, x.z - placeSpot(x.spot.id).z) < .6).length;
          const ps = a && a.spot ? placeSpot(a.spot.id) : null, dist = ps ? Math.round(Math.hypot(a.x - ps.x, a.z - ps.z) * 10) / 10 : null;
          return {{ m, by, dist, present: !!a, room, spot: a && a.spot && a.spot.id, anim: a && a.anim, at: inspectWalkerAt({DAY}), stand, standAt, due: inspectDue({DAY}), notes: simNotes('inspection', ({DAY} - 1) * 1440 - 1).map(n => [n.result, n.here, n.by]) }}; }})()""")
        key = (st['room'], st['spot'], st['at'], st['due'], st['m'] if st['m'] >= 400 else 0)
        if key != last: print(st); last = key
        if st['m'] in (391, 393, 397, 402) and shots < 4 and MODE == 'bunk':
            g.page.screenshot(path=f"{OUT}/insp_d{DAY}_{st['m']}.png", timeout=180000); shots += 1
        if st['m'] >= 440: break
    for s in g.ev("window.__said"): print(' ', s)
    print('mail:', g.ev("(SHIP.mail || []).filter(m => /inspect/i.test(m.subject || '')).map(m => [m.from, m.subject, m.body])") if g.ev("typeof SHIP.mail") != 'undefined' else None)
    print('errors', g.errors[:5])
