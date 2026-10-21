(() => { const d = 7, B = 6 * 1440, P = schedPeople().filter(p => aboard(p, d)), r = {};
  const din = p => planDay(p, d).filter(s => s.from >= B + 1020 && s.from < B + 1260 && (s.act === 'dinner' || /sunday-table/.test(s.tag || '') || s.act === 'grab' || s.tag === 'staff'));
  r.noDinner = P.filter(p => !din(p).length).map(p => p.id + '/' + p.shift + '/' + p.dept);
  r.plainDinner = P.filter(p => din(p).length && !din(p).some(s => /sunday-table/.test(s.tag || ''))).map(p => p.id + ':' + din(p).map(s => hhmm(s.from % 1440) + ' ' + (s.tag || s.act) + '@' + s.placeId).join(','));
  const ev = EV_SHIPWIDE.find(x => x.id === 'sunday-table'), dd = EV_DAY_DRESS.get('sunday-table@7');
  r.dress = dd && JSON.stringify(dd.o);
  const mess = t => P.filter(p => { const w = whereIs(p, B + t); return w && w.deck === 3 && /^3-mess-/.test(w.placeId || '') && !w.moving; }).length;
  for (const t of [1090, 1110, 1125, 1140]) r['messSeats' + t] = mess(t);
  r.trayStand = []; for (let t = 1080; t < 1170; t += 5) for (const p of P) { const w = whereIs(p, B + t); if (w && /sunday-table/.test(w.tag||'') && w.placeId && !/^3-mess-/.test(w.placeId)) r.trayStand.push(hhmm(t) + p.id + w.placeId); }
  return r; })()
