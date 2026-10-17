# reviewer 1f: veyliLamp opens the Captain's locked quarters while it's your next stop (jobDoorOpen, 0.28.52). Once the stop is done, can you still walk out?
import sys, json
src = open('cadet_test.py').read().split('import sys, json, hashlib')[0]
exec(src)
from playwright.sync_api import sync_playwright
SETUP = r"""(() => { const t = shipNow(); SHIP.stores.lamp = Math.max(SHIP.stores.lamp || 0, 9);
  const E = (Array.isArray(SHIP_EVENTS) ? SHIP_EVENTS : Object.values(SHIP_EVENTS)).find(e => e.jobs && Object.values(e.jobs).some(l => Array.isArray(l) && l.some(x => x.id === 'veyliLamp')));
  const j = eventJob(Object.values(E.jobs).flat().find(x => x && x.id === 'veyliLamp'), E.id, t, 'probe-veyli'); SHIP.jobs.push(j);
  for (const q of SHIP.jobs) if (q.claimedBy === 'you' && q.status === 'claimed') { q.claimedBy = null; q.status = 'open'; }
  j.claimedBy = 'you'; j.status = 'claimed'; j.start = t; MACH_REV++; SHIP.player.carry = j.parts.slice();
  const st = jobStops(j); st.forEach((x, k) => { if (x.step === 'fetch') jobStepDone(j.id, k); });
  const nx = jobStops(j).find(x => !x.done && x.step !== 'fetch'); return JSON.stringify([nx.deck, nx.places[0], jobStops(j).map(x => [x.step, x.done])]); })()"""
OUT = r"""((pid) => { const pl = PLACE_OF.get(pid), lw = [...PLACE_OF.values()].find(p => p.type === 'lift-wait'), here = player.here();
  return [!!findPath(here, lw.walk || lw.at, null, player), roomAt(...here), pl.room]; })"""
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1]); g.step(30)
    deck, pid, stops = json.loads(g.ev(SETUP)); print('stops', stops, 'next', deck, pid)
    g.ev(f"goToDeck({deck})"); g.step(5)
    g.ev(f"(() => {{ const s = placeSpot('{pid}'), gl = nearestOpen(s.x, s.z, player); player.obj.position.copy(cellPos(...gl)); player.stop(); }})()"); g.step(5)
    print('at the stop, job open: can walk out to the lift, room here, stop room:', g.ev(f"({OUT})('{pid}')"))
    g.ev("(() => { const j = SHIP.jobs.find(x => x.id === 'probe-veyli'); jobStops(j).forEach((x, k) => { if (!x.done) jobStepDone(j.id, k); }); MACH_REV++; })()"); g.step(5)
    print('stops done (job not turned in): can walk out:', g.ev(f"({OUT})('{pid}')"), g.ev("JSON.stringify(jobStops(SHIP.jobs.find(x => x.id === 'probe-veyli')).map(x => [x.step, x.done]))"))
    g.close()
