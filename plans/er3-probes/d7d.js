(() => { const r = {};
  for (const d of [7, 14, 21]) { const B = (d - 1) * 1440, P = schedPeople().filter(p => aboard(p, d));
    const segs = p => planDay(p, d).filter(s => s.from >= B + 960 && s.from < B + 1320);
    r['sup' + d] = P.filter(p => segs(p).some(s => /sunday-table|lanternSupper/.test(s.tag || ''))).length;
    r['nullDinner' + d] = P.filter(p => segs(p).some(s => s.act === 'dinner' && !s.placeId && s.tag !== 'queue' && s.to - s.from > 4)).map(p => p.id + ' ' + segs(p).filter(s => s.act === 'dinner').map(s => hhmm(s.from % 1440) + '-' + hhmm(s.to % 1440) + ':' + (s.tag || '') + '@' + s.placeId).join(','));
    r['twoDinners' + d] = P.filter(p => segs(p).filter(s => s.act === 'dinner' && s.tag !== 'queue' && s.placeId && !/queue/.test(s.placeId)).length + segs(p).filter(s => s.act === 'dinner' && !s.placeId && s.tag !== 'queue' && s.to - s.from > 4).length > 1).map(p => p.id);
  }
  return r; })()
