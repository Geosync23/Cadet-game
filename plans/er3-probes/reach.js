(() => { skipTo(6 * 1440 + 1080); goToDeck(3); const B = 6 * 1440, br = schedPeople().find(p => p.id === 'brennan'), out = {};
  const qs = [['L0', cellPos(33,6)], ['L3', cellPos(33,3)], ['L5', cellPos(32,2)], ['L7', cellPos(30,2)], ['29,6', cellPos(29,6)]];
  const LINE = typeof LINE_AT !== 'undefined' ? LINE_AT.map(x => x) : null;
  for (let t = 1085; t < 1155; t += 5) { const w = whereIs(br, B + t), s = w && w.placeId && placeSpot(w.placeId);
    out[hhmm(t)] = (w && w.placeId) + ' ' + qs.map(([id, q]) => id + ':' + (s ? Math.hypot(s.x - q.x, s.z - q.z).toFixed(1) : '-')).join(' '); }
  out.lineAt = LINE && JSON.stringify(LINE.slice(0, 8));
  return out; })()
