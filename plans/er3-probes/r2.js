(() => { const d = 7, B = 6 * 1440, P = schedPeople().filter(p => aboard(p, d)), r = {}, W = (id, t) => { const w = whereIs(P.find(p => p.id === id), B + t); return w && ((w.tag || w.act) + '@' + w.placeId + (w.moving ? ' moving' : '')); };
  const cer = t => P.filter(p => { const w = whereIs(p, B + t); return w && /^ev-(lineCeremony|crossingLine)/.test(w.tag || '') && !w.moving; });
  for (const t of [875, 880, 885, 895, 905]) r['cer' + t] = cer(t).length;
  r.captain = [870, 875, 880, 885].map(t => hhmm(t) + ' ' + W('marrow', t)); r.brennan = [880, 895].map(t => hhmm(t) + ' ' + W('brennan', t));
  r.firstAt = cer(885).filter(p => lineFirst().has(p.id)).length + '/' + P.filter(p => lineFirst().has(p.id)).length;
  r.firstNot = P.filter(p => lineFirst().has(p.id) && !cer(885).includes(p)).map(p => p.id + ':' + W(p.id, 885));
  r.saruth = W('saruth', 885); r.tomas = [870, 885, 900, 1240].map(t => hhmm(t) + ' ' + W('tomas', t)); r.ueda = W('ueda-vera', 885);
  const sup = t => P.filter(p => { const w = whereIs(p, B + t); return w && /sunday-table/.test(w.tag || '') && !w.moving; });
  let peak = 0; for (let t = 1080; t < 1200; t += 5) peak = Math.max(peak, sup(t).length); r.supPeak = peak;
  r.supCame = P.filter(p => planDay(p, d).some(s => /sunday-table/.test(s.tag || ''))).length;
  r.supStanding = []; for (let t = 1080; t < 1200; t += 5) for (const p of sup(t)) { const w = whereIs(p, B + t); if (!/^3-mess-/.test(w.placeId || '')) r.supStanding.push(hhmm(t) + p.id + w.placeId); }
  r.pell = planDay(P.find(p => p.id === 'pell'), d).filter(s => s.from >= B + 1050 && s.from < B + 1200).map(s => hhmm(s.from % 1440) + '-' + hhmm(s.to % 1440) + ' ' + (s.tag || s.act) + '@' + s.placeId);
  r.jobs = JSON.stringify((SHIP_EVENTS.crossingLine.jobs.warning || []).map(j => [j.id, j.hold]));
  return r; })()
