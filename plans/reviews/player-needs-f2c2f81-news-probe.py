import sys, json
exec(open('cadet_test.py').read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
# The News feed with head writer 3's real bank baked in: posts a day, texts, determinism (no R(), no Math.random),
# the same feed whether ticked every minute or caught up after 10-hour skips, and with chats in between.
RUN = r"""((step, chats) => {
  const s0 = seed, mr = Math.random; let rnd = 0; Math.random = () => { rnd++; return mr(); };
  SHIP.news = []; SHIP.newsUsed = []; SHIP.newsAt = null; SHIP.newsRows = {};
  const d0 = 3, days = 14, all = {}; let t = (d0 - 1) * 1440 + 300;
  newsTick(t);
  while (t < (d0 - 1 + days) * 1440) { t += step; if (chats && t % 1440 > 600 && t % 1440 < 700) for (const p of ROSTER.slice(0, 6)) try { lineFor(p.id, 'greet', { t }); } catch (e) {}
    newsTick(t); for (const x of SHIP.news) all[x.at + '|' + x.src + '|' + x.text] = x; }
  Math.random = mr;
  const xs = Object.values(all).sort((a, b) => a.at - b.at), per = {};
  for (const x of xs) { const d = Math.floor(x.at / 1440) + 1; per[d] = (per[d] || 0) + 1; }
  return JSON.stringify({ seedSame: seed === s0, rnd, per, n: xs.length, list: xs.map(x => [x.at, x.src, x.id, x.text]) });
})"""
with sync_playwright() as pw:
    g = Game(pw, sys.argv[1]); ev = g.ev
    print('bank kinds:', ev("JSON.stringify(Object.keys(NEWS_SRC).map(k => [k, (LINES['news.' + k] || []).length]))"))
    a = json.loads(ev(RUN + "(1, false)"))
    b = json.loads(ev(RUN + "(600, true)"))
    c = json.loads(ev(RUN + "(1, false)"))
    print('per day (every minute):', a['per'], 'total', a['n'], 'seed same', a['seedSame'], 'Math.random calls', a['rnd'])
    print('per day (10-hour skips, chats between):', b['per'], 'total', b['n'], 'seed same', b['seedSame'])
    print('every minute run twice the same:', a['list'] == c['list'])
    print('minute vs 10-hour skips the same:', a['list'] == b['list'])
    if a['list'] != b['list']:
        sa, sb = set(map(tuple, a['list'])), set(map(tuple, b['list']))
        print('  only minute:', sorted(sa - sb)[:6]); print('  only skips:', sorted(sb - sa)[:6])
    L = a['list']
    srcs = {}
    for x in L: srcs[x[1]] = srcs.get(x[1], 0) + 1
    print('sources:', srcs)
    print('unfilled {..}:', [x for x in L if '{' in x[3]][:3])
    print('over 90 chars:', [x[3] for x in L if len(x[3]) > 90][:3])
    ids = {}
    for x in L:
        if x[2]: ids.setdefault(x[2], []).append(x[0] // 1440)
    print('ids repeated within 7 days:', {k: v for k, v in ids.items() if any(v[i] - v[i - 1] < 7 for i in range(1, len(v)))})
    txt = {}
    for x in L: txt.setdefault(x[3], []).append(x[0] // 1440)
    print('same text twice:', {k[:50]: v for k, v in txt.items() if len(v) > 1})
    for x in L[:40]: print('  ', 'day', x[0] // 1440 + 1, '%02d:%02d' % (x[0] % 1440 // 60, x[0] % 60), x[1], '|', x[3])
    for e in g.errors: print('page error', e)
    g.close()
