(() => { const out = {}, W0 = JSON.stringify(SHIP.works);
 const reset = (t, uses) => { setShipNow(t); SHIP_DAYS.clear(); machinesNew(); SHIP.jobs = []; SHIP.mail = []; MACH_HOUR = null; MACH_SEEN = -1; setShipNow(t); machinesNow(); SHIP.works = null; const W = worksInit(t);
   W.team = { plan: {} }; W.inc = { plan: {}, open: null }; W.tier = 2; W.rank = 'officer'; W.tr.t2 = 10; W.tr.m8 = 11; W.use.m8 = uses; if (worksSide()) worksSide().parts = 0; return W; };
 const run = (t0, t1, uses, bring, d0 = 18) => { const W = reset(t0, uses), r = {}; let j = null;
   for (let t = t0; t <= t1; t += 5) { setShipNow(t); machinesNow(); for (const f of WORK_TICKS) f(t, false);
     j = j || SHIP.jobs.find(x => x.kind === 'team' && x.claimedBy === 'you' && worksDay(x.start) >= d0); if (!j || j.status === 'done') continue;
     const R = j.partsRun && SHIP.jobs.find(x => x.id === j.partsRun);
     if (R && !r.run) r.run = [R.kind, R.reserved, R.until === j.start, (R.crates || []).map(c => c.id).join('+'), R.crates.every(c => c.dest === panelPlace(j.machine))];
     if (bring && R && !R.delivered && t >= j.start - 60 && R.status !== 'done') { claimJob(R.id); jobStops(R).forEach((s, k) => jobStepDone(R.id, k, {})); r.delivered = manifestRunDelivered(R.id); turnInJob(R.id); }
     if (t >= j.start - 5) j.youIn = true;
     const mine = j.seq.map((s, i) => s.who === 'you' ? i : -1).filter(i => i >= 0), k = mine.indexOf(j.cur);
     if (k >= 0) { if (r.first === undefined) r.first = j.stepAt - j.start; jobStepDone(j.id, k, j.seq[j.cur].how === 'turn' ? { value: 3 } : {}); for (const f of WORK_TICKS) f(t, false); } }
   const R = j && j.partsRun && SHIP.jobs.find(x => x.id === j.partsRun);
   r.mach = j && [j.machine, j.id, worksDay(j.start), j.start % 1440, j.lead]; r.teams = SHIP.jobs.filter(x => x.kind === 'team').map(x => [x.machine, x.claimedBy, worksDay(x.start)]); r.job = j && { day: worksDay(j.start), status: j.status, by: j.doneBy, late: j.late, partsLate: j.partsLate === undefined ? null : j.partsLate, mins: j.doneAt - j.start, run: !!j.partsRun };
   r.left = R ? [R.status, !!R.delivered] : null; r.parts = worksSide() ? worksSide().parts || 0 : null;
   r.mail = SHIP.mail.filter(m => j && m.from === worksName(j.lead) && (m.subject === 'Bring the parts' || Object.values(TEAM_NAME).includes(m.subject))).map(m => m.subject); return r; };
 out.not0 = run(16 * 1440 + 900, 18 * 1440 + 800, 2, false); out.bring = run(16 * 1440 + 900, 18 * 1440 + 800, 2, true);
 out.not = run(16 * 1440 + 900, 18 * 1440 + 800, 2, false);
 out.stage0 = run(16 * 1440 + 900, 18 * 1440 + 800, 0, false);
 out.early = run(14 * 1440 + 900, 16 * 1440 + 800, 2, false, 0);
 worksSide().parts = 'x'; out.junk = teamPartsN(); worksSide().parts = 3; out.three = teamPartsN();
 SHIP.works = JSON.parse(W0); return out; })()