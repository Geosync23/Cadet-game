import sys, os
os.chdir(sys.argv[1])
exec(open('cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
JS = r"""(() => {
  socInit(); const out = {};
  // a stranger, early in the game, once the any-tier pool is used up: is "done" possible though tier-gated talks wait?
  SHIP.talks = { fired: {}, small: {} };
  for (const tk of TALKS.pool) if (!tk.when || !tk.when.tier) SHIP.talks.fired[tk.id] = [1, 'x'];
  const p = SOC.crew[SOC.idx.get('abara-rosa')]; relGet(p.id).tier = 0;
  let dn = 0, sm = 0, left = TALKS.pool.filter(tk => !SHIP.talks.fired[tk.id]).length;
  for (let d = 2; d < 60; d++) { const pk = talkPackPick(p, d * 1440 + 720); if (pk && pk.small) { sm++; if (pk.done) dn++; } delete SHIP.talks.small[p.id]; }
  out.stranger = { unfiredPoolTalks: left, smallTalkDays: sm, doneOpeners: dn };
  // longest greeting + opener on the card
  const starts = (LINES['talk.start'] || []).concat(LINES['talk.sit'] || []).map(e => e.text).sort((a, b) => b.length - a.length)[0];
  let longest = ''; for (const tk of TALKS.pool.concat(...Object.values(TALKS.own))) if (tk.lines[0].text.length > longest.length) longest = tk.lines[0].text;
  const line = starts + ' ' + longest;
  CHAT = { p, line: { text: line, say: true }, ask: false, fav: null, at: shipNow(), reach: 99, checked: 1e12,
    talk: { mins: 0, last: shipNow(), lineAt: 0, pts: 0, gained: 0, topic: null, said: [], ask: false, asked: true, reply: null, end: null, sits: false, pack: { small: true, lines: [line], i: 1 } } };
  chatShow(); const r = document.getElementById('chat').getBoundingClientRect();
  out.combined = { chars: line.length, line, rect: [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)], vw: innerWidth, vh: innerHeight };
  return out;
})()"""
with sync_playwright() as pw:
    g = Game(pw, 'starship-cadet.html', w=390, h=844, errors=[])
    g.step(3); print(g.ev(JS)); g.shot(os.path.join(sys.argv[2], 'combined.png')); g.close()
