# Starship Cadet: social check (keep in the repo, next to day_check.py)
# Runs the crew's social life (section 20) on paper with ?nosave and nothing drawn, and checks:
#   the same start gives the same social life: 14 ship days hour by hour, twice, with a stand-in player who chats
#   to Tomas and eats with him every day, chats to Pell every other day and hears the news Rina knows
#   one big jump over two days comes out the same as those days hour by hour
#   the save: its size, and that saving and loading gives back the same thing
#   sensible numbers: how crew affinity moved (friends and rivals), the news born of each kind and how far it
#   spread, and your tiers with Tomas (a friend after two weeks) and Pell (an acquaintance)
# Setup and environment as for cadet_test.py.
# Run:  python3 social_check.py BUILD.html [DAYS]     (DAYS defaults to 14)
import sys, json
exec(open(__file__.replace('social_check.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright

DAYS = int(sys.argv[2]) if len(sys.argv) > 2 else 14
SAVE_MAX = 20000               # bytes of the save's social part

# run `days` days from Day 1 06:00 hour by hour (or in one jump), with or without the stand-in player
RUN = r"""(({ days, player, jump }) => {
  const h0 = 6, h1 = h0 + days * 24, stats = { born: {}, spread: [] };
  setShipNow(h0 * 60); SHIP_DAYS.clear(); if (typeof machinesNow === 'function') machinesNow();   // an earlier clock: machines afresh
  socInit(); socReset(h0);
  const watch = () => { for (const x of NEWS) stats.born[x.id] = x.kind; };
  if (jump) { setShipNow(h1 * 60); socialTo(h1 * 60); watch(); }
  else for (let h = h0 + 1; h <= h1; h++) {
    setShipNow(h * 60); socialTo(h * 60); watch();
    for (const x of NEWS) if (h * 60 - x.born >= 720 && h * 60 - x.born < 780) stats.spread.push([x.kind, x.seed.length, SHIP.knows[x.id].size]);
    if (player && h % 24 === 12) { relAdd('tomas', 'chat', REL_PTS.chat); if ((h / 24 | 0) % 2) relAdd('pell', 'chat', REL_PTS.chat); for (const x of newsKnownBy('rina')) playerHeard(x.id, 'rina'); }
    if (player && h % 24 === 18) relAdd('tomas', 'meal', REL_PTS.meal);
  }
  const s = socSave(), a = Array.from(SHIP.aff), n = SOC.n, start = [];
  for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) start.push(affStart(SOC.crew[i], SOC.crew[j]));
  const sorted = a.slice().sort((x, y) => x - y), moved = a.map((v, k) => v - start[k]);
  return { key: JSON.stringify(s), size: JSON.stringify(s).length, pairs: a.length, n,
    aff: { min: sorted[0], mid: sorted[sorted.length >> 1], max: sorted[sorted.length - 1], friends: a.filter(v => v >= 60).length, rivals: a.filter(v => v <= -40).length,
           startFriends: start.filter(v => v >= 60).length, startRivals: start.filter(v => v <= -40).length, meanMove: moved.reduce((x, y) => x + y, 0) / a.length,
           up: moved.filter(v => v > 0).length, down: moved.filter(v => v < 0).length },
    born: stats.born, spread: stats.spread, news: NEWS.length, heard: SHIP.heard.length,
    rel: Object.fromEntries(Object.entries(SHIP.rel).map(([k, r]) => [k, [r.pts, REL_NAMES[r.tier]]])),
    sample: NEWS.slice(-6).map(x => x.lines[0]) };
})"""

ok = True
def fail(msg):
    global ok
    ok = False
    print('  FAIL', msg)

with sync_playwright() as pw:
    g = Game(pw, sys.argv[1])
    g.ev("window.__realTick = tickShip; tickShip = () => {}; socialTick = () => {}")   # we drive the clock ourselves
    print(f"{g.ev('socInit().n')} crew, {DAYS} days on paper")
    run = lambda **k: g.page.evaluate("([s, a]) => window.__sc(s)(a)", [RUN, k])

    # 1. the same start, twice
    a = run(days=DAYS, player=True, jump=False)
    b = run(days=DAYS, player=True, jump=False)
    print('The same twice:', a['key'] == b['key'])
    if a['key'] != b['key']: fail('the social life came out differently the second time')

    # 2. sensible numbers
    f = a['aff']
    print(f"Affinity, {a['pairs']} pairs: lowest {f['min']}, middle {f['mid']}, highest {f['max']}; friends (60+) {f['startFriends']} -> {f['friends']}, rivals (-40 or less) {f['startRivals']} -> {f['rivals']}")
    print(f"  moved: {f['up']} pairs friendlier, {f['down']} cooler, average {f['meanMove']:+.2f}")
    if not (0 < f['meanMove'] < 15): fail(f"affinity drifted {f['meanMove']:+.2f} on average (expected slowly friendlier)")
    if f['friends'] > a['pairs'] * .3: fail(f"{f['friends']} friendly pairs is too many")
    kinds = {}
    for k in a['born'].values(): kinds[k] = kinds.get(k, 0) + 1
    print('News born:', ', '.join(f"{k} {v}" for k, v in sorted(kinds.items())), f"| on the books at the end {a['news']}")
    for k in ('birthday', 'tradition') + (('habit',) if DAYS >= 9 else ()):
        if not kinds.get(k): fail(f"no {k} news in {DAYS} days")
    sp = a['spread']
    if sp:
        grew = sum(1 for x in sp if x[2] > x[1]) / len(sp)
        print(f"  12 hours after it's born, a piece of news is known by {sum(x[2] for x in sp) / len(sp):.1f} people on average (it started with {sum(x[1] for x in sp) / len(sp):.1f}); {grew:.0%} had spread")
        if grew < .3: fail('news hardly spreads')
    print('  latest:', ' | '.join(a['sample']))
    print('You:', ', '.join(f"{k} {v[0]} ({v[1]})" for k, v in sorted(a['rel'].items())), f"| news heard {a['heard']}")
    if a['rel'].get('tomas', [0, ''])[1] != 'friend': fail(f"Tomas should be a friend after {DAYS} days of chats and dinners: {a['rel'].get('tomas')}")
    if a['rel'].get('pell', [0, ''])[1] not in ('acquaintance', 'colleague'): fail(f"Pell should be an acquaintance: {a['rel'].get('pell')}")

    # 3. the save: size, and back again
    print(f"Save: social part {a['size']} bytes (limit {SAVE_MAX})")
    if a['size'] > SAVE_MAX: fail('the save is too big')
    rt = g.ev("(() => { const s = JSON.stringify(socSave()); socLoad(JSON.parse(s)); return s === JSON.stringify(socSave()); })()")
    print('Save and load give back the same:', rt)
    if not rt: fail('save and load differ')

    # 4. one jump over two days against the same two days hour by hour (no player)
    c = run(days=2, player=False, jump=False)
    d = run(days=2, player=False, jump=True)
    print('Two days in one jump the same as hour by hour:', c['key'] == d['key'])
    if c['key'] != d['key']: fail('a time jump gives a different social life')

    # 5. the query API (0.36.20): what the dialogue engine's line conditions read; pure, and right on a known state
    q = g.ev(r"""(() => {
      const out = {}, works = SOC.crew.find(p => p.dept === 'works' && p.rank !== 'chief'), tomas = SOC.crew[SOC.idx.get('tomas')];
      const before = JSON.stringify(socSave());
      out.missing = ['mem', 'warmth', 'affBand', 'bondOf', 'moodOf', 'beatOf', 'knowsNews', 'repBand', 'repShip', 'knownFor', 'cue', 'socialFill', 'memTold'].filter(f => { try { return typeof eval(f) !== 'function'; } catch (e) { return true; } });
      out.band = [affBand('tomas', 'pell'), affinity('tomas', 'pell')];
      out.bandsOk = SOC.crew.slice(0, 20).every(p => SOC.crew.slice(0, 20).every(q => { const v = affinity(p, q), b = affBand(p, q); return b === (v <= -40 ? 'rival' : v >= 60 ? 'friend' : 'neutral'); }));
      out.mood = ['low', 'ok', 'high'].includes(moodOf(tomas)) && moodOf('nobody') === 'ok';
      out.rep = [repBand('works'), repBand('galley'), repShip('work'), knownFor().length];
      out.warm = warmth('tomas');
      const n = NEWS.find(x => SHIP.knows[x.id].size); out.news = n ? [knowsNews([...SHIP.knows[n.id]][0], n.id), knowsNews([...SHIP.knows[n.id]][0], n.id.split(':')[0])] : null;
      out.fill = { me: socialFill(tomas, 'me'), nick: socialFill(tomas, 'nick'), boss: socialFill(works, 'boss'), thing: socialFill(tomas, 'thing', { mem: 'fixed.oven' }), none: socialFill(tomas, 'rival') };
      out.memNone = mem('tomas', 'fav') === null && bondOf('tomas', 'best') === null;
      out.pure = JSON.stringify(socSave()) === before;
      socNote('repair', { who: 'you', kind: 'oven', deck: 3 }); socNote('repair', { who: 'pell', kind: 'fan', deck: 5 });
      out.cue = [!!cue('repair.oven'), !!cue('repair.oven.you'), !!cue('repair.fan'), !!cue('repair.fan.you'), !!cue('repair'), cue('repair.lift') === null];
      const s = JSON.stringify(socSave()); socLoad(JSON.parse(s)); out.cueSaved = s === JSON.stringify(socSave()) && !!cue('repair.oven.you');
      setShipNow(shipNow() + 3 * 1440); out.cueGone = cue('repair.oven') === null; setShipNow(shipNow() - 3 * 1440);
      return out;
    })()""")
    print('Query API:', json.dumps(q))
    if q['missing']: fail(f"query functions missing: {q['missing']}")
    if not q['bandsOk'] or not q['mood'] or not q['pure']: fail('affBand, moodOf or purity wrong')
    if q['rep'][:3] != ['known', 'new', 'ok'] : fail(f"repBand/repShip defaults wrong: {q['rep']}")
    if q['news'] and q['news'] != [True, True]: fail(f"knowsNews wrong: {q['news']}")
    if q['fill']['boss'] is None or q['fill']['none'] is not None or q['fill']['thing'] is None: fail(f"socialFill wrong: {q['fill']}")
    if q['cue'] != [True, True, True, False, True, True] or not q['cueSaved'] or not q['cueGone']: fail(f"cues wrong: {q['cue']} saved {q['cueSaved']} gone {q['cueGone']}")

    print('errors', g.errors[:5])
    if g.errors: ok = False
    print('SOCIAL CHECK OK' if ok else 'SOCIAL CHECK FAILED')
    g.close()
