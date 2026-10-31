# RV30 probe (0.99.5 round, arrows_check week "Unstick a gym locker" stayed up 3 h): the odd job oj-d3gym-locker (place
# 3-gym-1, a treadmill) held by you, at three times of Day 8 with the real crew: you put at its spot, a real screen tap on the
# floor there (interactions_check's own MKJ/HOLD/SCR/PUT), then what started and who is on the treadmill.
# Usage: odd_gym.py WORKTREE BUILD [row ...]
import sys, os
wt = sys.argv[1]; os.chdir(wt); ROWS = sys.argv[3:] or ['oj-d3gym-locker']
exec(open('cadet_test.py').read().split('a, shots = run(')[0])
MKJ = r"""((kind) => { const t = shipNow(), out = []; SHIP.stores.lamp = Math.max(SHIP.stores.lamp || 0, 9);
  const add = j => { if (j) { SHIP.jobs.push(j); out.push(j.id); } };
  if (kind === 'lamp') choreWhere('lamp').forEach(c => add({ id: 'ixtap-' + c.key, machine: null, deck: c.deck, room: c.room, kind: 'chore', chore: 'lamp', target: c.key, title: c.title, tier: 1,
    stops: c.stops.map(x => ({ ...x })), urgency: 0, posted: t, found: t, claimedBy: null, parts: ['lamp'], status: 'open' }));
  if (kind === 'event' && typeof SHIP_EVENTS !== 'undefined') for (const id of ['stormBallasts', 'veyliLamp']) {
    const E = (Array.isArray(SHIP_EVENTS) ? SHIP_EVENTS : Object.values(SHIP_EVENTS)).find(e => e.jobs && Object.values(e.jobs).some(l => Array.isArray(l) && l.some(x => x.id === id)));
    if (E) add(eventJob(Object.values(E.jobs).flat().find(x => x && x.id === id), E.id, t, 'ixtap-' + id)); }
  if (kind === 'machine') { const m = machineList().find(m => m.id === '3-oven-1');
    if (m) add({ id: 'ixtap-oven', machine: m.id, deck: m.deck, room: m.room, kind: Object.keys(JOB_TYPES)[0], urgency: 1, posted: t, found: t, claimedBy: null, parts: ['seal'], status: 'open', title: 'Repair the oven' }); }
  if (kind === 'fix' && typeof fixTable === 'function') { const T = fixTable(), one = new Set();   // FX10's small repairs: one in each room they're in
    for (const r of T.s.concat(T.p)) { const pl = placeById(r.place); if (!pl || (pl.deck === 7 && !REC_DECK) || one.has(pl.deck + pl.room)) continue; one.add(pl.deck + pl.room);
      if (r.part) SHIP.stores[r.part] = Math.max(SHIP.stores[r.part] || 0, 9);
      add({ id: 'ixtap-fix-' + r.id, machine: null, deck: pl.deck, room: pl.room, kind: 'chore', chore: 'fix', target: r.id, title: r.title, tier: 1, stops: [{ deck: pl.deck, placeId: r.place, mins: r.mins, tag: 'fix' }],
        urgency: 0, posted: t, found: t, claimedBy: null, parts: r.part ? [r.part] : [], status: 'open', fix: r.id, fixS: pl.deck === 2 ? 's' : 'p', tool: r.tool }); } }
  if (kind.startsWith('odd') && typeof fixTable === 'function' && fixTable().o) { const one = new Set();   // FX20's odd jobs (ODD_ON): one in each room ('odd'), or every row ('oddall', a probe)
    const only = kind.startsWith('odd:') ? kind.slice(4).split(',') : null;   // odd:<id>,<id>: just those rows
    for (const r of fixTable().o) { const pl = placeById(r.place); if (!pl || (pl.deck === 7 && !REC_DECK) || (kind === 'odd' && one.has(pl.deck + pl.room)) || (only && !only.includes(r.id))) continue; one.add(pl.deck + pl.room);
      if (r.part) SHIP.stores[r.part] = Math.max(SHIP.stores[r.part] || 0, 9);
      add({ id: 'ixtap-odd-' + r.id, machine: null, deck: pl.deck, room: pl.room, kind: 'chore', chore: 'fix', target: r.id, title: r.title, tier: 1, stops: [{ deck: pl.deck, placeId: r.place, mins: r.mins, tag: 'fix' }],
        urgency: 0, posted: t, found: t, claimedBy: null, parts: r.part ? [r.part] : [], status: 'open', fix: r.id, fixS: 'o', tool: r.tool }); } }
  MACH_REV++; return out; })"""
HOLD = r"""((id) => { for (const j of SHIP.jobs) if (j.claimedBy === 'you' && j.status === 'claimed') { j.claimedBy = null; j.status = 'open'; }
  actEnd(true); SHIP.player.work = null; const j = SHIP.jobs.find(x => x.id === id); j.claimedBy = 'you'; j.status = 'claimed'; j.start = shipNow(); MACH_REV++;   // claimed by hand: the tier doesn't matter here
  SHIP.player.carry = j.parts.slice(0, 2); jobStops(j).forEach((x, k) => { if (x.step === 'fetch' && j.kind === 'chore') jobStepDone(j.id, k); });
  const nx = jobStops(j).find(x => !x.done && x.step !== 'fetch'); return nx ? [nx.step, nx.deck, nx.places[0]] : null; })"""
SCR = r"""((pid) => { const s = placeSpot(pid), scr = (dx, dz) => { const v = new THREE.Vector3(s.x + dx, .02, s.z + dz).project(camera); return [(v.x + 1) / 2 * innerWidth, (1 - v.y) / 2 * innerHeight]; };
  for (const [dx, dz] of [[0, 0], [.4, 0], [-.4, 0], [0, .4], [0, -.4], [.4, .4], [-.4, .4], [.4, -.4], [-.4, -.4], [.8, 0], [-.8, 0], [0, .8], [0, -.8]]) { const p = scr(dx, dz); if (!crewAtScreen(...p)) return p; }
  return scr(0, 0); })"""
PUT = r"""((pid) => { const s = placeSpot(pid), gl = nearestOpen(s.x, s.z, player); player.obj.position.copy(cellPos(...gl)); player.stop(); })"""
ST = "(() => ({ act: ACT ? [ACT.kind, ACT.placeId || null, ACT.phase] : null, toast: ((document.getElementById('toast') || {}).textContent || '').slice(0, 120), busy: (() => { const a = DECK_CREW.find(c => c.goalId === '3-gym-1' || (c.spot && c.spot.id === '3-gym-1')); return a ? a.p.id : null; })() }))()"
with sync_playwright() as pw:
    g = Game(pw, sys.argv[2]); g.step(10)
    for row in ROWS:
        for hm in [9 * 60 + 30, 13 * 60, 19 * 60 + 30]:
            g.ev(f"(() => {{ for (const j of SHIP.jobs) if (String(j.id).startsWith('ixtap-')) j.status = 'done'; SHIP.jobs = SHIP.jobs.filter(j => !String(j.id).startsWith('ixtap-')); actEnd(true); skipTo(7 * 1440 + {hm}); }})()"); g.step(60)
            jid = g.ev(f"({MKJ})('odd:{row}')")
            if not jid: print(row, 'no such odd job here'); break
            nx = g.ev(f"({HOLD})('{jid[0]}')"); step, deck, pid = nx
            if g.ev('deckDef.num') != deck: g.ev(f"goToDeck({deck})"); g.step(3)
            g.ev(f"({PUT})('{pid}')"); g.step(60); before = g.ev(ST)
            x, y = g.ev(f"({SCR})('{pid}')"); g.page.mouse.click(x, y); g.step(90); s = g.ev(ST)
            print(f'{row} Day 8 {hm // 60:02d}:{hm % 60:02d} stop {step} {pid}: on the treadmill before {before["busy"]}; tap -> act {s["act"]}, toast {s["toast"]!r}')
    print('errors', [e for e in g.errors if 'pageerror' in e][:3]); g.close()
