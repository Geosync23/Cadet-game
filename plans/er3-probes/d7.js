(() => { const d = 7, B = 6 * 1440, P = schedPeople(), r = {};
  r.aboard = P.filter(p => aboard(p, d)).length; r.guests = P.filter(p => aboard(p, d) && p.rank === 'guest').map(p => p.id);
  r.first = [...lineFirst()]; r.firstAboard = P.filter(p => lineFirst().has(p.id) && aboard(p, d)).length;
  r.cast = evSlotCrew('first', 2, d, ['marrow','brennan']).map(p => p.id);
  r.workAt1430 = P.filter(p => { const w = whereIs(p, B + 870); return w && w.act === 'work'; }).length;
  const cer = t => P.filter(p => { const w = whereIs(p, B + t); return w && /^ev-(lineCeremony|crossingLine)/.test(w.tag || '') && !w.moving; });
  for (const t of [870, 875, 880, 885, 895, 905, 914]) r['cer' + t] = cer(t).length;
  r.inLounge1440 = P.filter(p => { const w = whereIs(p, B + 880); return w && w.deck === 3 && w.placeId && /lounge|bow-lounge/.test(w.placeId); }).map(p => p.id + ':' + (w => w.tag)(whereIs(p, B + 880)) + ':' + whereIs(p, B + 880).placeId);
  r.everCer = P.filter(p => planDay(p, d).some(s => /^ev-lineCeremony|^ev-crossingLine/.test(s.tag || ''))).length;
  r.easy = P.filter(p => lineEasy(p, d, { from: 870, to: 915 })).map(p => p.id + '/' + p.dept);
  r.easyCame = P.filter(p => lineEasy(p, d, { from: 870, to: 915 }) && cer(885).includes(p)).length;
  r.saruth = whereIs(P.find(p => p.id === 'saruth'), B + 885);
  r.ulla = P.filter(p => /ulla/i.test(p.id + p.name)).map(p => p.id + ':' + JSON.stringify(whereIs(p, B + 885)));
  const tom = P.find(p => p.id === 'tomas'); r.tomas = planDay(tom, d).filter(s => s.from >= B + 400 && s.from < B + 1440).map(s => [hhmm(s.from % 1440), hhmm(s.to % 1440), s.placeId, s.tag || s.act]);
  r.front = P.filter(p => { const w = whereIs(p, B + 885); return w && /front/.test(w.placeId || ''); }).map(p => p.id + (lineFirst().has(p.id) ? '*' : ''));
  r.lead = ['marrow','brennan',...r.cast].map(id => { const w = whereIs(P.find(p => p.id === id), B + 885); return id + '@' + (w && w.placeId); });
  r.firstAtCer = cer(885).filter(p => lineFirst().has(p.id)).length;
  r.firstNotThere = P.filter(p => lineFirst().has(p.id) && aboard(p, d) && !cer(885).includes(p)).map(p => p.id + ':' + ((w => w && (w.tag || w.act) + '@' + w.placeId)(whereIs(p, B + 885))));
  // supper
  const sup = t => P.filter(p => { const w = whereIs(p, B + t); return w && /sunday-table/.test(w.tag || ''); });
  for (const t of [1080, 1100, 1110, 1120, 1135, 1150, 1170]) r['sup' + t] = sup(t).length + ' st:' + sup(t).filter(p => { const w = whereIs(p, B + t); return w.placeId && !/mess-|seat|bench|table/.test(w.placeId); }).map(p => whereIs(p, B + t).placeId).join('|');
  r.supEver = P.filter(p => planDay(p, d).some(s => /sunday-table/.test(s.tag || ''))).length;
  r.supPlaces = [...new Set(P.flatMap(p => planDay(p, d).filter(s => /sunday-table/.test(s.tag || '') && s.placeId).map(s => s.placeId.replace(/\d+$/, ''))))];
  r.menu = galleyMenu(7);
  r.cal = EV_CALENDAR.map(x => JSON.stringify(x)).join(' ; ');
  return r; })()
