from pp import *
g = start('?nosave&debug')
g.step(5)
print(g.ev(r"""(() => { const at = id => { for (const n in DECKS) { const q = (DECKS[n].places || []).find(q => q.id === id); if (q) return q.walk || q.at; } return null; };
 let n = 0, reach = 0, nolast = 0; const byDeck = {};
 for (const p of schedPeople()) { const S = planDay(p, 1); S.forEach((s, i) => { if (s.tag !== 'toilet') return; n++;
   let j = i - 1; while (j >= 0 && !S[j].placeId && S[j].act !== 'commute') j--;
   const prev = j >= 0 ? S[j] : null; let from = prev && prev.placeId ? at(prev.placeId) : null;
   if (prev && prev.act === 'commute') from = DECKS[s.deck].lift;
   const to = at(s.placeId); if (!from || !to) { nolast++; return; }
   const tiles = Math.abs(from[0] - to[0]) + Math.abs(from[1] - to[1]), walk = tiles * 0.6 / 1.15 * 1.1;
   const ok = walk + 1 < s.to - s.from; if (ok) reach++; const b = byDeck[s.deck] || (byDeck[s.deck] = [0, 0]); b[0]++; if (ok) b[1]++; }); }
 return { n, reach, nolast, byDeck }; })()"""))
g.close()
