# TR1: every pack line on the chat card at 390 x 844 (fills each talk for a speaker who can say it)
import sys, os, json
W = sys.argv[1]
os.chdir(W)
exec(open('cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
JS = r"""(() => {
  socInit(); const people = SOC.crew.filter(p => p.id !== 'you'), out = [], t = shipNow();
  const ctx = { t, trad: talkPackTrad(t) || 'Tiles night' };
  const items = [];
  for (const tk of TALKS.pool) items.push([tk, null]); for (const w in (TALKS.work || {})) for (const tk of TALKS.work[w]) items.push([tk, null]);
  for (const id in TALKS.own) for (const tk of TALKS.own[id]) items.push([tk, id]);
  const measure = (p, line, replies, tag) => {
    CHAT = { p, line: { text: line, say: true }, ask: false, fav: null, at: shipNow(), reach: 99, checked: 1e12,
      talk: { mins: 7, last: shipNow(), lineAt: 7, pts: 0, gained: 0, topic: null, said: [], ask: !!replies, asked: true, reply: null, end: null, sits: false,
        pack: replies ? { replies, lines: [line], i: 1 } : { small: true, lines: [line], i: 1 } } };
    chatShow(); const el = document.getElementById('chat'), r = el.getBoundingClientRect(), bad = [];
    if (r.left < -1 || r.right > innerWidth + 1) bad.push('card off screen ' + Math.round(r.left) + '..' + Math.round(r.right));
    if (r.bottom > innerHeight + 1 || r.top < -1) bad.push('card off bottom/top ' + Math.round(r.top) + '..' + Math.round(r.bottom));
    for (const e of el.querySelectorAll('*')) { const b = e.getBoundingClientRect(); if (b.width && (b.right > innerWidth + 1 || b.left < -1)) { bad.push('element off screen: ' + e.tagName + ' ' + (e.textContent || '').slice(0, 40)); break; } }
    for (const b of el.querySelectorAll('button')) if (b.scrollWidth > b.clientWidth + 1 || b.scrollHeight > b.clientHeight + 2 && getComputedStyle(b).overflow !== 'visible') bad.push('button clipped: ' + b.textContent);
    if (!el.textContent.includes(line.slice(0, 30))) bad.push('line not shown');
    if (bad.length) out.push([tag, line, bad]);
    return [Math.round(r.height)];
  };
  let maxH = 0, n = 0, unfilled = [];
  for (const [tk, own] of items) {
    let p = own ? (SOC.crew[SOC.idx.get(own)] || (typeof ROSTER_GUESTS !== 'undefined' && ROSTER_GUESTS.find(g => g.id === own))) : null, said = null;
    for (const q of p ? [p] : people) { const s = talkPackFill(tk, q, ctx); if (s) { p = q; said = s; break; } }
    if (!said) { unfilled.push(tk.id); continue; }
    const reps = said.replies;
    for (const l of said.lines.concat([said.ask])) { const h = measure(p, l, null, tk.id)[0]; maxH = Math.max(maxH, h); n++; }
    for (const k of ['listen', 'share', 'cheer']) { const h = measure(p, said.ask, reps, tk.id + ' ask+buttons')[0]; maxH = Math.max(maxH, h); n++; const h2 = measure(p, reps[k].ans, null, tk.id + ' ans ' + k)[0]; maxH = Math.max(maxH, h2); n++; }
  }
  for (const k in TALKS.small) for (const e of TALKS.small[k]) { measure(people[0], linesFill(e.text, people[0], ctx) || e.text, null, 'small ' + k); n++; }
  chatClose();
  return { n, maxH, out, unfilled };
})()"""
with sync_playwright() as pw:
    errs = []
    g = Game(pw, 'starship-cadet.html', w=390, h=844, errors=errs)
    g.step(3)
    r = g.ev(JS)
    print('measured', r['n'], 'cards; tallest card', r['maxH'], 'px')
    print('unfilled for everyone:', r['unfilled'])
    for x in r['out'][:40]: print('BAD', x)
    print('problems:', len(r['out']), 'page errors:', errs[:5])
    # a screenshot of the longest ask with buttons
    g.close()
