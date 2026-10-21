import sys
sys.argv=['x','on.html']
exec(open('/tmp/rv/ec/cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    g=Game(pw,'/tmp/rv/fr3/on.html')
    print(g.ev("""(() => { const r = {}; const set = (d, m) => { setShipNow((d-1)*1440+m); };
      r.end = [4,5,6,12].map(d => [d, dayShiftEnd(d), friAutoOut(d)]);
      set(5, 9*60); careerClock(shipNow(), true); r.inAt = careerClockedIn(5);
      set(5, 15*60+20); r.working1520 = workingNow();
      set(5, 15*60+45); careerTick(); r.co1545 = careerClockedOut(5);
      set(5, 16*60+1); careerTick(); r.co1601 = careerClockedOut(5); r.coMin = SHIP.player.career ? null : null;
      try { const C = careerInit(shipNow()); r.co = C.co % 1440; r.log = SHIP.player.clockLog && SHIP.player.clockLog[5]; } catch (e) { r.err = String(e); }
      set(12, 15*60+40); r.lateIn = careerClockedIn(12); careerClock(shipNow(), true); r.lateInAfter = careerClockedIn(12);
      return r; })()"""))
    print(g.ev("(() => { const out = []; for (const m of [920, 935, 960]) { setShipNow(4*1440+m); out.push([m, typeof workingNow === 'function' && workingNow()]); } return out; })()"))
    g.close()
