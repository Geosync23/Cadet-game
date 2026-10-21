(() => { const out = {}; const h = s => { let x = 0; for (let i = 0; i < s.length; i++) x = (x * 31 + s.charCodeAt(i)) | 0; return x; };
  for (let d = 1; d <= 30; d++) { let s = ''; for (const p of schedPeople()) s += p.id + JSON.stringify(planDay(p, d)); out[d] = h(s) + ' ' + JSON.stringify(galleyMenu(d)).length + ' ' + eventsOn(d).map(e => e.id + e.from + '-' + e.to).join(','); }
  return out; })()
