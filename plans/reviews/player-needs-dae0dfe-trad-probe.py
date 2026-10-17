# reviewer 1f: every tradition's "done" post (onSim('tradition')) and the feed's "today" posts name the tradition, never its id
import sys, json, re
exec(open('cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
JS = r"""(() => {
  const ids = (typeof SHIP_TRADITIONS !== 'undefined' ? SHIP_TRADITIONS : []).map(e => e.id), out = [];
  SHIP.news = []; SHIP.newsUsed = [];
  let t = 3 * 1440 + 600;
  for (const id of ids) { t += 400; const n0 = SHIP.news.length; simNote('tradition', { id, at: t }); const x = SHIP.news.find(q => q.at === t && q.src === 'trad'); out.push([id, x ? x.text : null]); }
  // and the "today" posts over four weeks, ticked every ship minute
  SHIP.news = []; SHIP.newsUsed = []; SHIP.newsAt = null; SHIP.newsRows = {}; const all = {};
  for (let m = 2 * 1440; m < 30 * 1440; m++) { newsTick(m); for (const x of SHIP.news) if (x.src === 'trad') all[x.at + x.text] = x.text; }
  return JSON.stringify({ ids, done: out, today: Object.values(all) });
})()"""
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1]); r = json.loads(g.ev(JS)); g.close()
ids = [i for i in r['ids'] if '-' in i]
bad = lambda s: s and any(re.search(r'\b' + re.escape(i) + r'\b', s) for i in ids)
print('traditions:', len(r['ids']))
for id_, x in r['done']: print('  done', id_, '->', x)
print('today posts:', len(r['today']))
for x in r['today'][:12]: print('  today ->', x)
print('posts with an id in them:', [x for _, x in r['done'] if bad(x)] + [x for x in r['today'] if bad(x)])
print('done posts missing:', [i for i, x in r['done'] if not x])
