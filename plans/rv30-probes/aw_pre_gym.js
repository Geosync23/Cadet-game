(() => { const mk = ((kind) => { const t = shipNow(), out = []; SHIP.stores.lamp = Math.max(SHIP.stores.lamp || 0, 9);
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
  MACH_REV++; return out; }), hold = ((id) => { for (const j of SHIP.jobs) if (j.claimedBy === 'you' && j.status === 'claimed') { j.claimedBy = null; j.status = 'open'; }
  actEnd(true); SHIP.player.work = null; const j = SHIP.jobs.find(x => x.id === id); j.claimedBy = 'you'; j.status = 'claimed'; j.start = shipNow(); MACH_REV++;   // claimed by hand: the tier doesn't matter here
  SHIP.player.carry = j.parts.slice(0, 2); jobStops(j).forEach((x, k) => { if (x.step === 'fetch' && j.kind === 'chore') jobStepDone(j.id, k); });
  const nx = jobStops(j).find(x => !x.done && x.step !== 'fetch'); return nx ? [nx.step, nx.deck, nx.places[0]] : null; }); for (const j of SHIP.jobs) if (j.claimedBy === 'you' && j.status === 'claimed') { j.claimedBy = null; j.status = 'open'; } const ids = mk('odd:oj-d3gym-locker'); return [ids, hold(ids[0])]; })()